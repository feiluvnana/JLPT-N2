#!/usr/bin/env python3
"""
N2 choukai exam MP3 generator (v3) — official-style audio.

Calibrated against the official JLPT N2 exam audio archive in
refs/JLPT_N2_NEW/ (31 sittings, 2010-07 .. 2025-12 — see
.agents/choukai-audio/references/official_pacing.md):
  - Narrator/announcer: FEMALE voice, slightly slow, like the official test
    announcer (measured F0 176-254 Hz, 31/31 female).
  - ~0.9 s of air between utterances (official turn gaps: median 0.51 s,
    p75 0.75 s, p90 1.08 s over 465 diarized turn boundaries).
  - Answer pauses: 12 s after each question (8 s for 問題4 quick response).
  - Output loudness normalized to about -15 LUFS, the median integrated
    loudness of all 31 official recordings.

ONE engine: edge-tts (free, no key, native Japanese). Two paid alternatives were
implemented, measured on real keys and REMOVED — the evidence is kept in the
skill so nobody re-runs the experiment: ElevenLabs reaches only English-native
voices without a Creator-tier key (accented Japanese), and Gemini TTS caps the
free tier at 10–15 requests per DAY against a ~250-line script. Neither could
build a paper this repo would ship, and an unreliable engine in the default path
is worse than two ja-JP voices that always work.

Setup (one time):
    pip install edge-tts
    # ffmpeg must be on PATH (macOS: brew install ffmpeg)

Run:
    python make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
    python make_choukai_mp3.py … --jobs 4        # fewer parallel TTS requests

Output (written next to the input script):
    聴解.mp3               (full exam)
    聴解_チャプター.json    (per-問題/per-item offsets + script_sha + engine)
    segments/             (per-block mp3s for drilling single questions)

Re-running is cheap: already-synthesized lines are skipped (delete the
segments/ folder to force a full rebuild). A cold build synthesizes lines
concurrently — see TTS_JOBS.
"""

import array
import asyncio
import hashlib
import json
import inspect
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

try:
    import edge_tts
except ModuleNotFoundError:            # checked in main(); `make check` imports
    edge_tts = None                    # this module without needing to speak

FEMALE = "ja-JP-NanamiNeural"
MALE = "ja-JP-KeitaNeural"

# Narrator = official announcer: female, a touch slower.
NARRATOR = {"voice": FEMALE, "rate": "-10%"}

# Dialogue roles for the EDGE engine. edge-tts ships exactly two ja-JP voices,
# so identity has to come from rate and pitch on top of those two.
#   rate  is the calibrated speech rate (Part 4 step 5) — do not spend it on
#         telling speakers apart, or the paper's difficulty moves with the cast.
#   pitch is what separates two same-gender roles. It was added because a
#         rate-only split (男1 +4% vs 男2 -8%) is not a second person to the
#         ear: `check_voice_casting()` WARNed on exactly that pair. Kept modest
#         (≤20 Hz on a ~120 Hz male, ~25 Hz on a ~210 Hz female) — edge-tts
#         resynthesizes pitch, and large shifts buzz.
# **This map is also the gender contract**: `make check` reads it to confirm
# every 「〜の男の人」/「〜の女の人」 narration resolves to a voice of that gender.
SPEAKER_MAP = {
    "男":     {"voice": MALE,   "rate": "+0%", "pitch": "+0Hz"},
    "男1":    {"voice": MALE,   "rate": "+4%", "pitch": "+18Hz"},
    "男2":    {"voice": MALE,   "rate": "-8%", "pitch": "-16Hz"},
    "夫":     {"voice": MALE,   "rate": "+0%", "pitch": "-12Hz"},
    "学生":   {"voice": MALE,   "rate": "+6%", "pitch": "+14Hz"},
    "部長":   {"voice": MALE,   "rate": "-6%", "pitch": "-18Hz"},
    "店長":   {"voice": MALE,   "rate": "+0%", "pitch": "+10Hz"},
    "女":     {"voice": FEMALE, "rate": "+4%", "pitch": "+0Hz"},
    "妻":     {"voice": FEMALE, "rate": "+4%", "pitch": "+16Hz"},
    "店員":   {"voice": FEMALE, "rate": "+6%", "pitch": "+22Hz"},
    "先生":   {"voice": FEMALE, "rate": "+0%", "pitch": "-16Hz"},
    "医者":   {"voice": FEMALE, "rate": "+0%", "pitch": "-10Hz"},
    "専門家": {"voice": FEMALE, "rate": "+0%", "pitch": "-22Hz"},
    "レポーター": {"voice": FEMALE, "rate": "+6%", "pitch": "+25Hz"},
    "教室の人":   {"voice": FEMALE, "rate": "+0%", "pitch": "+12Hz"},
    # Added after validate_script() caught these being silently narrated.
    # Gender is chosen to contrast with the OTHER speaker named in the item's
    # narration (学生 and 男の人 are male), so the two voices stay distinguishable.
    "職員":   {"voice": FEMALE, "rate": "+0%", "pitch": "-14Hz"},   # vs 学生 (male)
    "係員":   {"voice": FEMALE, "rate": "+6%", "pitch": "+18Hz"},   # vs 男の人
    "担当者": {"voice": FEMALE, "rate": "+0%", "pitch": "-20Hz"},
    "講師":   {"voice": FEMALE, "rate": "+0%", "pitch": "-25Hz"},
    "アナウンス":   {"voice": FEMALE, "rate": "+0%", "pitch": "+8Hz"},
    "アナウンサー": {"voice": FEMALE, "rate": "+4%", "pitch": "+20Hz"},
    "教授":   {"voice": MALE,   "rate": "-6%", "pitch": "-20Hz"},   # vs 学生 (male)
    "FP":     {"voice": MALE,   "rate": "+0%", "pitch": "-14Hz"},
}

# Pacing (seconds) — measured across the 31-sitting official archive in
# refs/JLPT_N2_NEW/ (2010-2025).  See
# .agents/choukai-audio/references/official_pacing.md for the per-sitting
# tables, sample counts and method.  Every value below sits inside the
# measured band; do not guess new ones.
GAP_BETWEEN_LINES = 0.9        # ordinary gap between dialogue turns
GAP_AFTER_PRE_QUESTION = 3.0   # 問題1/2: after the question, before the talk
GAP_OPTION_READING = 20.0      # 問題2 only: time to read printed options
GAP_BETWEEN_SPOKEN_CHOICES = 3.0  # 問題3/5: between spoken choices 1〜4
GAP_AFTER_SHITSUMON1 = 10.0    # 問題5 two-question item: answer time for 質問1
# Placed BEFORE the 質問2 line, not after the 質問1 line. Those were the same
# point while 2番's options were printed and 質問1/質問2 sat adjacent. This repo
# now prints NOTHING for 問題5 (both items) and speaks 2番's four choices under
# each question, so keying the gap off 質問1 would drop 10 s of answer time
# between the question and its own choice 1, and leave choice 4 running straight
# into 質問2 with no answer time at all.

# Every gap above is inserted BETWEEN segments, so it is only the real gap if a
# segment starts and ends at its first and last sample of speech. Both engines
# pad: edge-tts writes ~0.22 s of lead and ~0.85 s of TAIL silence into every
# utterance, Gemini ~0.26 s either side. Unshaved, that made the measured turn
# gap in tests/20260810_2 **1.88–2.09 s** where the constant says 0.9 and
# official measures 0.51 [p75 0.75, p90 1.08] — i.e. the whole archive
# calibration was silently defeated by TTS padding, and the audio dragged.
# `shape_pauses()` trims both ends to zero so the numbers above mean what they
# say, and it caps over-long pauses INSIDE one utterance:
GAP_WITHIN_TURN_MAX = 0.5      # cap for a pause inside one turn (at 。 mostly)
SHAPE_PAUSE_FLOOR = 0.6        # only pauses longer than this get capped
# Why a cap and not a target: official same-speaker (within-turn) pauses
# measure median 0.40 s [p75 0.53, p90 0.72] (official_pacing.md §2), while
# edge-tts renders a mid-turn 。 as 0.97 s — twice the official p75. Pauses
# BELOW the floor are left exactly as the engine produced them: a Japanese 促音
# closure is a ~0.1 s silence, and "improving" it would eat the consonant.

ANSWER_PAUSE = {               # answer time appended after each item block
    "問題1": 12.0,
    "問題2": 12.0,
    "問題3": 8.0,
    "問題4": 8.0,
    "問題5": 10.0,
}
PAUSE_AFTER_INSTRUCTION = 3.0
PAUSE_DEFAULT = 1.5

SR = 24000  # both engines are native 24 kHz mono

# Parallelism. Synthesizing a line is a network round trip (0.6–1.9 s measured),
# so a cold build of a ~250-line script is latency-bound, not CPU-bound, and runs
# ~4x faster with a handful of requests in flight. The cap is deliberately low:
# the edge-tts endpoint throttles, and while synth() retries with backoff, the
# cap is what keeps 429s rare enough that retries stay invisible.
TTS_JOBS = 8
# ffmpeg calls are one core each, so bound them separately from the network work.
FFMPEG_JOBS = max(2, (os.cpu_count() or 4) - 2)
ITEM_RE = re.compile(r"^(例。|\d+番。)")
SPEAKER_RE = re.compile(r"^([^:: ]{1,6})[::](.*)$")

# edge-tts pitch support varies by version — only pass it if accepted.
_PITCH_OK = bool(edge_tts) and "pitch" in inspect.signature(
    edge_tts.Communicate.__init__).parameters


def source_sha(path: Path) -> str:
    """First 12 hex digits of sha1 over the file's raw BYTES.

    Stamped into 聴解_チャプター.json as `script_sha`, so an MP3 built from a
    superseded script is detectable from content alone. Deliberately NOT an
    mtime: mtimes are checkout-unstable — a git checkout has made a current
    聴解.mp3 look older than its script on disk, forcing a reviewer to reason
    from git history instead of the filesystem to tell it apart from audio
    that really was superseded.
    `build_booklet.py` stamps the same 12-hex convention into its HTML as
    `<!-- src_sha: <name>=<sha> -->`, and `make check` compares both.
    """
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12]


def run(cmd):
    subprocess.run(cmd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def to_wav(src: Path, dst: Path):
    run(["ffmpeg", "-y", "-i", str(src),
         "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(dst)])


def shape_pauses(path: Path, frame_ms: int = 10):
    """Trim a segment's leading/trailing silence and cap its internal pauses.

    Both TTS engines pad every utterance (edge-tts ~0.22 s lead + ~0.85 s tail;
    Gemini ~0.26 s), and that padding lands INSIDE the segment, on top of every
    gap the pacing table inserts between segments. Measured consequence before
    this function existed: turn gaps of 1.88–2.09 s in tests/20260810_2 against
    a `GAP_BETWEEN_LINES` of 0.9 and an official median of 0.51 — the audio
    dragged, and no gate could see it because the constants were "right".

    Two operations, both on 24 kHz mono s16 samples, speech untouched:
      1. drop leading and trailing silence entirely, so the inter-segment gap
         is exactly what the plan asked for;
      2. shorten any internal pause longer than `SHAPE_PAUSE_FLOOR` to
         `GAP_WITHIN_TURN_MAX` (official same-speaker pauses: median 0.40,
         p75 0.53). Anything shorter is left alone — a 促音 closure is a ~0.1 s
         silence and shortening or padding it would damage the consonant.

    Silence is decided per 10 ms frame against a floor 38 dB below the
    segment's own peak (and never above −50 dBFS absolute), which is inside the
    valley for both engines: their speech sits above −30 dBFS and their padding
    is digital zero.
    """
    with wave.open(str(path), "rb") as w:
        if w.getnchannels() != 1 or w.getsampwidth() != 2:
            return                                  # not our format; leave it
        sr = w.getframerate()
        samples = array.array("h", w.readframes(w.getnframes()))
    if not samples:
        return

    step = max(1, int(sr * frame_ms / 1000))
    peak = max(max(samples), -min(samples), 1)
    floor = max(peak * 10 ** (-38 / 20), 32767 * 10 ** (-50 / 20))

    loud = []
    for start in range(0, len(samples), step):
        chunk = samples[start:start + step]
        loud.append(max(max(chunk), -min(chunk)) >= floor)
    if not any(loud):
        return                                      # silence only — keep as is

    first, last = loud.index(True), len(loud) - 1 - loud[::-1].index(True)
    keep_floor = int(SHAPE_PAUSE_FLOOR * 1000 / frame_ms)
    keep_max = int(GAP_WITHIN_TURN_MAX * 1000 / frame_ms)

    out = array.array("h")
    i = first
    while i <= last:
        if loud[i]:
            out.extend(samples[i * step:(i + 1) * step])
            i += 1
            continue
        run_end = i
        while run_end <= last and not loud[run_end]:
            run_end += 1
        length = run_end - i
        keep = keep_max if length > keep_floor else length
        out.extend(array.array("h", [0]) * (keep * step))
        i = run_end
    # The tail of the last loud frame is partial when the file does not end on a
    # frame boundary; take the real samples rather than a truncated frame.
    out.extend(samples[(last + 1) * step:min(len(samples), (last + 2) * step)])

    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(out.tobytes())


def make_silence_wav(seconds: float, dst: Path):
    run(["ffmpeg", "-y", "-f", "lavfi",
         "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{seconds}",
         "-c:a", "pcm_s16le", str(dst)])


def concat_wavs(files, dst: Path):
    lst = dst.with_suffix(".list")
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files),
                   encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:a", "pcm_s16le", str(dst)])
    lst.unlink()


def wav_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def wav_to_mp3(src: Path, dst: Path, normalize=False):
    cmd = ["ffmpeg", "-y", "-i", str(src)]
    if normalize:
        # I: median integrated loudness of all 31 official recordings
        # (-15.0 LUFS; p25 -15.5, p75 -14.3).  TP: official median is
        # -0.86 dBTP and several sittings clip above 0, so we keep the safer
        # -1.0.  LRA is a ceiling — official material measures 7.5-9.8, well
        # under it, so it never engages.
        cmd += ["-af", "loudnorm=I=-15:TP=-1.0:LRA=11"]
    cmd += ["-c:a", "libmp3lame", "-b:a", "96k", str(dst)]
    run(cmd)


async def synth(text: str, cast: dict, out_wav: Path, retries: int = 3):
    """One line of script -> one shaped 24 kHz mono WAV.

    edge-tts returns MP3, so it is decoded before shaping; `shape_pauses` runs
    here, before the segment is cached, so a warm cache and a cold build produce
    byte-identical audio.
    """
    mp3 = out_wav.with_suffix(".mp3")
    for attempt in range(1, retries + 1):
        try:
            kwargs = {"voice": cast["voice"], "rate": cast["rate"]}
            if _PITCH_OK:
                kwargs["pitch"] = cast.get("pitch", "+0Hz")
            await edge_tts.Communicate(text, **kwargs).save(str(mp3))
            if mp3.stat().st_size:
                await asyncio.to_thread(to_wav, mp3, out_wav)
                await asyncio.to_thread(shape_pauses, out_wav)
                return
        except Exception as e:  # noqa: BLE001
            if attempt == retries:
                raise RuntimeError(f"TTS failed for: {text[:30]}…") from e
            await asyncio.sleep(2 * attempt)


def voice_for(line: str):
    """Split a line into (voice spec, spoken text).

    An unlabelled line is the narrator. A label with no entry in `SPEAKER_MAP`
    cannot reach here: `validate_script()` rejects it, because `voice_for` would
    otherwise silently narrate that speaker.
    """
    m = SPEAKER_RE.match(line)
    label = m.group(1) if m and m.group(1) in SPEAKER_MAP else None
    spoken = m.group(2).strip() if label else line.strip()
    return dict(NARRATOR if label is None else SPEAKER_MAP[label]), spoken


def pause_after(block_first_line: str, section: str) -> float:
    if ITEM_RE.match(block_first_line):
        return ANSWER_PAUSE.get(section, 12.0)
    if block_first_line.startswith("問題"):
        return PAUSE_AFTER_INSTRUCTION
    return PAUSE_DEFAULT


CHOICE_RE = re.compile(r"^[1-4]、")
SHITSUMON2_RE = re.compile(r"^質問2。")


def gap_before_line(section: str, line_index: int, line: str,
                    prev_line: str, is_item_block: bool) -> float:
    """Silence inserted BEFORE this line (i.e., after the previous one)."""
    if line_index == 0:
        return 0.0
    if SHITSUMON2_RE.match(line):
        return GAP_AFTER_SHITSUMON1          # 質問1 (+ its choices) -> answer -> 質問2
    if is_item_block and line_index == 1:
        if section == "問題2":
            return GAP_OPTION_READING        # printed-option reading time
        if section == "問題1":
            return GAP_AFTER_PRE_QUESTION    # beat before the talk starts
    # 3 s apart is the gap BETWEEN spoken choices, not before the first one:
    # official Dec 2025 audio measures exactly 3 gaps around 4 choices
    # (question -> ~1s natural pause -> choice1 -> 3.0s -> choice2 -> 3.0s ->
    # choice3 -> 3.0s -> choice4 -> answer pause). Applying it whenever the
    # CURRENT line is a choice — regardless of what preceded it — inserted a
    # 4th, extra 3 s gap between the repeated question and choice 1 in every
    # 問題3/5 item, silently lengthening that transition by ~2 s versus the
    # official recording. Require the PREVIOUS line to also be a choice.
    if (CHOICE_RE.match(line) and section in ("問題3", "問題5")
            and CHOICE_RE.match(prev_line or "")):
        return GAP_BETWEEN_SPOKEN_CHOICES    # spoken choices, 3 s apart
    return GAP_BETWEEN_LINES


# --- Script sanity gate (runs before any synthesis) ---------------------
# 「最もよいものは◯番です。」 is an 例-ONLY line: it belongs to the 問題1〜4
# practice confirmation, which always continues with 「解答用紙の…」. A bare
# reveal after a scored item speaks the answer aloud and ruins the exam.
REVEAL_RE = re.compile(r"^(?:質問[12]の)?最もよいものは\d番です。")
EXAMPLE_CONFIRM_RE = re.compile(
    r"^最もよいものは\d番です。解答用紙の問題\dの例のところを見てください。")
ANNOTATION_RE = re.compile(r"[（(]※")


# Required structure of a full N2 script. Counts INCLUDE the 例 where one exists.
# 問題5 has no 例 (「この問題には練習はありません。」) and its 2番 block carries two
# questions (質問1/質問2), giving 3 answers from 2 item blocks.
EXPECTED_ITEMS = {"問題1": 6, "問題2": 7, "問題3": 6, "問題4": 12, "問題5": 2}
NEEDS_EXAMPLE = ("問題1", "問題2", "問題3", "問題4")
OPENING = "これから、N2の聴解試験を始めます"
CLOSING = "これで、聴解試験を終わります。"
NO_PRACTICE = "この問題には練習はありません。"
TYPO_RE = re.compile(r"問題用紙になに印刷")   # 「何も印刷」 mistyped; TTS reads it wrong


def validate_script(blocks):
    """Fail fast on anything that would corrupt the exam. Two classes of check:

    (1) lines that must never be SPOKEN (answer reveals, authoring notes), and
    (2) STRUCTURE — the 例/practice machinery and item counts. A missing 例 or a
        missing announcer line is silent: the MP3 still builds and just quietly
        deviates from the official exam. Both classes shipped as real bugs, so
        both are enforced here rather than left to a reviewer's eye.
    """
    errors = []
    section = None
    items = {k: 0 for k in EXPECTED_ITEMS}
    examples = {k: 0 for k in EXPECTED_ITEMS}
    confirms = {k: 0 for k in EXPECTED_ITEMS}
    practice_cue = {k: 0 for k in EXPECTED_ITEMS}
    no_practice = {k: 0 for k in EXPECTED_ITEMS}
    text = "\n".join(blocks)

    for bi, block in enumerate(blocks):
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        first = lines[0]
        m = re.match(r"^(問題[1-5])。$", first)
        if m:
            section = m.group(1)
            if len(lines) > 1:
                errors.append(f"block {bi} — header 「{first}」 must be a single-line block (got {len(lines)} lines)")
        is_example = first.startswith("例。")
        if ITEM_RE.match(first) and section:
            items[section] += 1
            if is_example:
                examples[section] += 1

        for line in lines:
            # --- class 1: must never be spoken ---
            if ANNOTATION_RE.search(line):
                errors.append(f"block {bi} — authoring annotation would be read "
                              f"aloud: {line}")
            if TYPO_RE.search(line):
                errors.append(f"block {bi} — typo 「なに印刷」 (should be "
                              f"「何も印刷」): {line}")
            if REVEAL_RE.match(line):
                if EXAMPLE_CONFIRM_RE.match(line):
                    if section:
                        confirms[section] += 1
                    continue
                errors.append(
                    f"block {bi} — answer revealed for a scored item"
                    + (" (例 block, but not the full 解答用紙 confirmation)"
                       if is_example else "") + f": {line}")
            # --- class 2: structural cues ---
            if section:
                if "では、練習しましょう。" in line:
                    practice_cue[section] += 1
                if NO_PRACTICE in line:
                    no_practice[section] += 1

        # 問題5's two-question item must be ONE block, or the answer pause lands
        # between 質問1 and 質問2 instead of after the item.
        if "質問1。" in block and "質問2。" not in block:
            errors.append(f"block {bi} — 質問1 without 質問2 in the same block; "
                          f"the 問題5 two-question item must not be split")

        # Every item (例/N番) must carry its own dialogue/speech/options in the
        # SAME block, not just the opening narration+question. A stray blank
        # line between the marker line and the rest splits one item into
        # marker-only / dialogue / repeated-question blocks: the item's actual
        # content still gets synthesized (nothing is silently dropped), but
        # gap_before_line() and pause_after() key off each block's OWN first
        # line, so 問題2's option-reading pause disappears and — far worse —
        # the answer-time pause lands right after the question, BEFORE the
        # dialogue plays, instead of after it. This shipped silently in tests
        # 2 (問題2/3), 3, and 4 (問題1-5, entire listening section) because the
        # MP3 still built and sounded plausible in isolation. 問題4's stimulus
        # line itself is conventionally untagged (read by the narrator), so it
        # is checked for its spoken option lines instead of a speaker tag;
        # every other 問題's item — monologues included, e.g. 専門家:/講師: —
        # carries at least one speaker-tagged line in a valid script.
        if ITEM_RE.match(first) and section:
            rest = lines[1:]
            if section == "問題4":
                if sum(1 for l in rest if CHOICE_RE.match(l)) < 3:
                    errors.append(
                        f"block {bi} ({first[:30]}…) — item has fewer than 3 "
                        f"spoken option lines (`1、`/`2、`/`3、`) in the same "
                        f"block as its marker; they were likely split into a "
                        f"separate block by a stray blank line, which "
                        f"corrupts pause placement (see "
                        f"choukai-audio/SKILL.md 'Block conventions')")
            elif not any(SPEAKER_RE.match(l) for l in rest):
                errors.append(
                    f"block {bi} ({first[:30]}…) — item has no speaker-tagged "
                    f"line in the same block as its marker; the dialogue/speech "
                    f"was likely split into a separate block by a stray blank "
                    f"line, which corrupts pause placement (see "
                    f"choukai-audio/SKILL.md 'Block conventions')")

    # --- whole-file structure ---
    if OPENING not in text:
        errors.append(f"missing opening announcement 「{OPENING}…」")
    if blocks[-1].strip() != CLOSING:
        errors.append(f"the last block of the script must be exactly 「{CLOSING}」 on its own line")
    # 問題5 prints nothing for EITHER item in this repo, so BOTH 1番 and 2番 get
    # a spoken 「問題用紙に何も印刷されていません…」 lead-in of their own. While
    # 2番's options were printed it had no spoken lead-in at all and one block
    # was correct here; a paper carrying only one now leaves 2番's examinee with
    # neither printed options nor an instruction telling them the choices are
    # spoken. (問題3/4 also say the phrase, but inside a 「問題Nでは、…」 block,
    # so they never satisfy this startswith.)
    if "問題5。" in text:
        lead_ins = sum(1 for b in blocks
                       if b.strip().startswith("問題用紙に何も印刷されていません"))
        if lead_ins != 2:
            errors.append(
                f"問題5: {lead_ins} lead-in block(s) starting with 「問題用紙に何も"
                f"印刷されていません」, expected 2 (one before 1番, one before 2番)")

    for sec, want in EXPECTED_ITEMS.items():
        if f"{sec}。" not in text:
            errors.append(f"{sec} section header 「{sec}。」 missing")
            continue
        if items[sec] != want and not (sec == "問題5" and items[sec] in (2, 3)):
            errors.append(f"{sec}: {items[sec]} item block(s), expected {want}"
                          + (" (例 + scored items)" if sec in NEEDS_EXAMPLE else ""))
        if sec in NEEDS_EXAMPLE:
            if examples[sec] != 1:
                errors.append(f"{sec}: {examples[sec]} 例 block(s), expected exactly 1")
            if practice_cue[sec] != 1:
                errors.append(f"{sec}: 「では、練習しましょう。」 appears "
                              f"{practice_cue[sec]} time(s), expected exactly 1")
            if confirms[sec] != 1:
                errors.append(f"{sec}: {confirms[sec]} 例 confirmation line(s) "
                              f"(「最もよいものは◯番です。解答用紙の…」), expected exactly 1")
        else:
            if examples[sec]:
                errors.append(f"{sec} must have NO 例 ({NO_PRACTICE})")
            if no_practice[sec] != 1:
                errors.append(f"{sec}: 「{NO_PRACTICE}」 appears "
                              f"{no_practice[sec]} time(s), expected exactly 1")

    # --- speaker labels must all be in the voice map ---
    unmapped = set()
    for block in blocks:
        for line in block.split("\n"):
            m = SPEAKER_RE.match(line.strip())
            if m and m.group(1) not in SPEAKER_MAP:
                unmapped.add(m.group(1))
    if unmapped:
        errors.append(f"speaker label(s) not in SPEAKER_MAP (they would be read "
                      f"by the narrator voice): {sorted(unmapped)}")

    if errors:
        raise SystemExit(
            "Refusing to synthesize — the script violates the choukai contract.\n"
            "See .agents/choukai-audio/SKILL.md.\n\n  "
            + "\n  ".join(errors))
    print(f"  script OK: {len(blocks)} blocks, items "
          + ", ".join(f"{k}={items[k]}" for k in EXPECTED_ITEMS))


def build_plan(blocks, seg: Path):
    """Parse the script into an explicit build plan before anything is synthesized.

    Parsing is separated from assembly so that every line's TTS request can be
    dispatched at once instead of one per block. The plan is what makes that safe:
    it pins each line's segment path and each gap's exact duration up front, so
    the parallel passes only fill in files whose names and contents were already
    decided sequentially.
    """
    plan = []
    section = ""
    for bi, block in enumerate(blocks):
        lines = [l for l in block.splitlines() if l.strip()]
        first = lines[0]
        if re.match(r"^問題\d+。", first):
            section = first.rstrip("。")
        is_item_block = bool(ITEM_RE.match(first))

        entries = []
        prev_line = ""
        for li, line in enumerate(lines):
            spec, spoken = voice_for(line)
            if not spoken:
                continue
            # Cache key includes the text AND the full cast (voice, rate,
            # pitch), not just the position: keying on position alone silently
            # reuses stale audio when a line is reworded or a speaker is
            # remapped to a different voice.
            tag = hashlib.sha1(
                f"{spoken}|{spec['voice']}|{spec['rate']}|{spec.get('pitch', '+0Hz')}"
                .encode("utf-8")).hexdigest()[:10]
            wav = seg / f"b{bi:03d}_l{li:02d}_{tag}.wav"
            entries.append({
                "spoken": spoken, "spec": spec, "wav": wav,
                # None for the block's first spoken line: nothing precedes it.
                "gap": None if not entries else
                       gap_before_line(section, li, line, prev_line, is_item_block),
            })
            prev_line = line

        plan.append({"bi": bi, "first": first, "section": section,
                     "entries": entries, "pause": pause_after(first, section),
                     "wav": seg / f"block_{bi:03d}.wav"})
    return plan


async def synthesize_lines(plan, limit: int):
    """Synthesize every not-yet-cached line, `limit` requests in flight."""
    todo = [e for b in plan for e in b["entries"] if not e["wav"].exists()]
    cached = sum(len(b["entries"]) for b in plan) - len(todo)
    print(f"  synthesizing {len(todo)} line(s) with {limit} in parallel"
          + (f" ({cached} cached)" if cached else ""))
    if not todo:
        return

    sem = asyncio.Semaphore(limit)
    done = 0

    async def one(e):
        nonlocal done
        async with sem:
            await synth(e["spoken"], e["spec"], e["wav"])
        done += 1
        if done % 10 == 0 or done == len(todo):
            print(f"  [{done}/{len(todo)}] {e['spoken'][:40]}")

    await asyncio.gather(*(one(e) for e in todo))


async def make_silences(plan, seg: Path, limit: int):
    """Pre-create every silence file the plan needs, before parallel assembly.

    Creating them lazily during assembly would let two blocks shell out to ffmpeg
    for the same `_sil_1.3.wav` at once and leave one block with a truncated gap —
    a corruption no downstream check can see, since the file is still valid audio.
    """
    wanted = {e["gap"] for b in plan for e in b["entries"] if e["gap"]}
    wanted |= {b["pause"] for b in plan if b["pause"]}
    paths = {s: seg / f"_sil_{s:g}.wav" for s in sorted(wanted)}

    sem = asyncio.Semaphore(limit)

    async def one(seconds, path):
        async with sem:
            await asyncio.to_thread(make_silence_wav, seconds, path)

    await asyncio.gather(*(one(s, p) for s, p in paths.items()
                           if not p.exists()))
    return paths


async def assemble_blocks(plan, silences, seg: Path, limit: int):
    """Concat each block, encode its drill mp3, and measure it — blocks in parallel.

    Safe to parallelize because every input file already exists and each block
    writes only paths derived from its own index.
    """
    sem = asyncio.Semaphore(limit)

    async def one(b):
        wavs = []
        for e in b["entries"]:
            if e["gap"] is not None:
                wavs.append(silences[e["gap"]])
            wavs.append(e["wav"])
        async with sem:
            await asyncio.to_thread(concat_wavs, wavs, b["wav"])
            # per-question drill file
            await asyncio.to_thread(wav_to_mp3, b["wav"], seg / f"block_{b['bi']:03d}.mp3")
            return await asyncio.to_thread(wav_duration, b["wav"])

    print(f"  assembling {len(plan)} block(s) with {limit} in parallel")
    return await asyncio.gather(*(one(b) for b in plan))


async def main():
    keep_segments = "--keep-segments" in sys.argv
    tts_jobs = TTS_JOBS
    args = []
    skip_next = False
    for i, a in enumerate(sys.argv[1:]):
        if skip_next:
            skip_next = False
            continue
        if a == "--jobs":
            tts_jobs = max(1, int(sys.argv[i + 2]))
            skip_next = True
        elif a.startswith("--jobs="):
            tts_jobs = max(1, int(a.split("=", 1)[1]))
        elif not a.startswith("--"):
            args.append(a)

    if args:
        src = Path(args[0])
    else:
        src = Path("聴解スクリプト.txt") if Path("聴解スクリプト.txt").exists() else Path("script.txt")

    out_dir = src.parent if src.parent != Path("") else Path(".")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", src.read_text(encoding="utf-8"))
              if b.strip()]
    validate_script(blocks)

    if edge_tts is None:
        raise SystemExit("edge-tts is not installed — pip install edge-tts")
    seg = out_dir / "segments"
    seg.mkdir(exist_ok=True)
    plan = build_plan(blocks, seg)
    await synthesize_lines(plan, tts_jobs)
    silences = await make_silences(plan, seg, FFMPEG_JOBS)
    durations = await assemble_blocks(plan, silences, seg, FFMPEG_JOBS)

    # Chapter marks and the playlist are accumulated strictly in block order:
    # the offsets are a running sum, so this stays sequential even though the
    # durations feeding it were measured in parallel. Computed here rather than
    # recovered later with silence detection — the assembler knows the true
    # offsets, a detector only guesses them.
    playlist = []
    chapters = []
    clock = 0.0        # exact position in the assembled file, seconds
    for b, duration in zip(plan, durations):
        first, section = b["first"], b["section"]
        label = first.split("。")[0] + "。" if ITEM_RE.match(first) else None
        if re.match(r"^問題\d+。", first):
            chapters.append({"type": "section", "section": section,
                             "label": section, "start": round(clock, 2)})
        elif label:
            chapters.append({"type": "item", "section": section,
                             "label": label.rstrip("。"),
                             "start": round(clock, 2)})

        playlist.append(b["wav"])
        clock += duration
        playlist.append(silences[b["pause"]])
        clock += b["pause"]

    full_wav = out_dir / "_n2_full.wav"
    out_mp3 = out_dir / "聴解.mp3"
    concat_wavs(playlist, full_wav)
    wav_to_mp3(full_wav, out_mp3, normalize=True)
    if full_wav.exists():
        full_wav.unlink()

    # `script_sha` is the staleness stamp: it identifies the exact script bytes
    # this MP3 was built from, so a later edit to 聴解スクリプト.txt without a
    # rebuild becomes a `make check` failure instead of an invisible defect.
    # A script rewrite across several papers once regenerated the audio for
    # only one of them — the rest shipped speaking superseded 問題N
    # instructions and no gate could see it.
    sha = source_sha(src)
    chapters_path = out_dir / "聴解_チャプター.json"
    chapters_path.write_text(
        json.dumps({"script_sha": sha,
                    "duration": round(clock, 2), "chapters": chapters},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Chapters -> {chapters_path} ({len(chapters)} marks, "
          f"script_sha {sha})")

    # Cleanup temporary segments directory
    if not keep_segments and seg.exists():
        import shutil
        shutil.rmtree(seg)
        print(f"Cleaned up temporary directory: {seg}")

    print(f"\nDone -> {out_mp3} ({clock / 60:.1f} min)")




if __name__ == "__main__":
    asyncio.run(main())
