#!/usr/bin/env python3
"""
N2 choukai exam MP3 generator (v2) — official-style audio.

Calibrated against official JLPT N2 exam audio (in refs/JLPT/):
  - Narrator/announcer: FEMALE voice (ja-JP-NanamiNeural), slightly slow,
    like the official test announcer.
  - ~1.3 s of air between utterances (measured from official exam audio).
  - Answer pauses: 12 s after each question (8 s for 問題4 quick response).
  - Output loudness normalized to about -17 LUFS to match official exam levels.

Setup (one time):
    pip install edge-tts
    # ffmpeg must be on PATH (macOS: brew install ffmpeg)

Run:
    python make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
    python make_choukai_mp3.py … --jobs 4      # fewer parallel TTS requests

Output (written next to the input script):
    聴解.mp3               (full exam)
    聴解_チャプター.json    (per-問題/per-item offsets)
    segments/             (per-block mp3s for drilling single questions)

Re-running is cheap: already-synthesized lines are skipped (delete the
segments/ folder to force a full rebuild). A cold build synthesizes lines
concurrently — see TTS_JOBS.
"""

import asyncio
import hashlib
import json
import inspect
import os
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

FEMALE = "ja-JP-NanamiNeural"
MALE = "ja-JP-KeitaNeural"

# Narrator = official announcer: female, a touch slower.
NARRATOR = {"voice": FEMALE, "rate": "-10%"}

# Dialogue roles. Female roles use a normal-speed Nanami so the narrator
# (slower) still reads as a different "person". 男2 is slowed to separate
# him from 男1 in the three-person conversation.
SPEAKER_MAP = {
    "男":     {"voice": MALE,   "rate": "+0%"},
    "男1":    {"voice": MALE,   "rate": "+4%"},
    "男2":    {"voice": MALE,   "rate": "-8%"},
    "夫":     {"voice": MALE,   "rate": "+0%"},
    "学生":   {"voice": MALE,   "rate": "+6%"},
    "部長":   {"voice": MALE,   "rate": "-6%"},
    "店長":   {"voice": MALE,   "rate": "+0%"},
    "女":     {"voice": FEMALE, "rate": "+4%"},
    "妻":     {"voice": FEMALE, "rate": "+4%"},
    "店員":   {"voice": FEMALE, "rate": "+6%"},
    "先生":   {"voice": FEMALE, "rate": "+0%"},
    "医者":   {"voice": FEMALE, "rate": "+0%"},
    "専門家": {"voice": FEMALE, "rate": "+0%"},
    "レポーター": {"voice": FEMALE, "rate": "+6%"},
    "教室の人":   {"voice": FEMALE, "rate": "+0%"},
    # Added after validate_script() caught these being silently narrated.
    # Gender is chosen to contrast with the OTHER speaker named in the item's
    # narration (学生 and 男の人 are male), so the two voices stay distinguishable.
    "職員":   {"voice": FEMALE, "rate": "+0%"},   # vs 学生 (male)
    "係員":   {"voice": FEMALE, "rate": "+6%"},   # vs 男の人
    "担当者": {"voice": FEMALE, "rate": "+0%"},
    "講師":   {"voice": FEMALE, "rate": "+0%"},
    "アナウンス":   {"voice": FEMALE, "rate": "+0%"},
    "アナウンサー": {"voice": FEMALE, "rate": "+4%"},
    "教授":   {"voice": MALE,   "rate": "-6%"},   # vs 学生 (male, +6%) — split by rate
    "FP":     {"voice": MALE,   "rate": "+0%"},
}

# Pacing (seconds) — measured from the official Dec 2025 N2 exam audio.
GAP_BETWEEN_LINES = 1.3        # ordinary gap between dialogue turns
GAP_AFTER_PRE_QUESTION = 3.0   # 問題1/2: after the question, before the talk
GAP_OPTION_READING = 20.0      # 問題2 only: time to read printed options
GAP_BETWEEN_SPOKEN_CHOICES = 3.0  # 問題3/5: between spoken choices 1〜4
GAP_AFTER_SHITSUMON1 = 10.0    # 問題5 two-question item: after 質問1

ANSWER_PAUSE = {               # answer time appended after each item block
    "問題1": 12.0,
    "問題2": 12.0,
    "問題3": 8.0,
    "問題4": 8.0,
    "問題5": 10.0,
}
PAUSE_AFTER_INSTRUCTION = 3.0
PAUSE_DEFAULT = 1.5

SR = 24000  # edge-tts native sample rate

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
_PITCH_OK = "pitch" in inspect.signature(edge_tts.Communicate.__init__).parameters


def run(cmd):
    subprocess.run(cmd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def to_wav(src: Path, dst: Path):
    run(["ffmpeg", "-y", "-i", str(src),
         "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(dst)])


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
        cmd += ["-af", "loudnorm=I=-17:TP=-1.0:LRA=11"]
    cmd += ["-c:a", "libmp3lame", "-b:a", "96k", str(dst)]
    run(cmd)


async def synth(text: str, voice: str, rate: str, out_mp3: Path,
                retries: int = 3):
    for attempt in range(1, retries + 1):
        try:
            kwargs = {"voice": voice, "rate": rate}
            if _PITCH_OK:
                kwargs["pitch"] = "+0Hz"
            tts = edge_tts.Communicate(text, **kwargs)
            await tts.save(str(out_mp3))
            if out_mp3.stat().st_size > 0:
                return
        except Exception as e:  # noqa: BLE001
            if attempt == retries:
                raise RuntimeError(f"TTS failed for: {text[:30]}…") from e
            await asyncio.sleep(2 * attempt)


def voice_for(line: str):
    m = SPEAKER_RE.match(line)
    if m and m.group(1) in SPEAKER_MAP:
        return SPEAKER_MAP[m.group(1)], m.group(2).strip()
    return NARRATOR, line.strip()


def pause_after(block_first_line: str, section: str) -> float:
    if ITEM_RE.match(block_first_line):
        return ANSWER_PAUSE.get(section, 12.0)
    if block_first_line.startswith("問題"):
        return PAUSE_AFTER_INSTRUCTION
    return PAUSE_DEFAULT


CHOICE_RE = re.compile(r"^[1-4]、")
SHITSUMON1_RE = re.compile(r"^質問1。")


def gap_before_line(section: str, line_index: int, line: str,
                    prev_line: str, is_item_block: bool) -> float:
    """Silence inserted BEFORE this line (i.e., after the previous one)."""
    if line_index == 0:
        return 0.0
    if prev_line and SHITSUMON1_RE.match(prev_line):
        return GAP_AFTER_SHITSUMON1          # 質問1 -> answer time -> 質問2
    if is_item_block and line_index == 1:
        if section == "問題2":
            return GAP_OPTION_READING        # printed-option reading time
        if section == "問題1":
            return GAP_AFTER_PRE_QUESTION    # beat before the talk starts
    if CHOICE_RE.match(line) and section in ("問題3", "問題5"):
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

    # --- whole-file structure ---
    if OPENING not in text:
        errors.append(f"missing opening announcement 「{OPENING}…」")
    if not text.rstrip().endswith(CLOSING):
        errors.append(f"script must end with 「{CLOSING}」")

    for sec, want in EXPECTED_ITEMS.items():
        if f"{sec}。" not in text:
            errors.append(f"{sec} section header 「{sec}。」 missing")
            continue
        if items[sec] != want:
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
            "See .agents/choukai-script-writing/SKILL.md.\n\n  "
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
            # Cache key includes the text AND the voice/rate, not just the
            # position: keying on position alone silently reuses stale audio
            # when a line is reworded or a speaker is remapped to a new voice.
            tag = hashlib.sha1(
                f"{spoken}|{spec['voice']}|{spec['rate']}".encode("utf-8")
            ).hexdigest()[:10]
            mp3 = seg / f"b{bi:03d}_l{li:02d}_{tag}.mp3"
            entries.append({
                "spoken": spoken, "spec": spec,
                "mp3": mp3, "wav": mp3.with_suffix(".wav"),
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
            await synth(e["spoken"], e["spec"]["voice"], e["spec"]["rate"], e["mp3"])
            await asyncio.to_thread(to_wav, e["mp3"], e["wav"])
        done += 1
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

    chapters_path = out_dir / "聴解_チャプター.json"
    chapters_path.write_text(
        json.dumps({"duration": round(clock, 2), "chapters": chapters},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Chapters -> {chapters_path} ({len(chapters)} marks)")

    # Cleanup temporary segments directory
    if not keep_segments and seg.exists():
        import shutil
        shutil.rmtree(seg)
        print(f"Cleaned up temporary directory: {seg}")

    print(f"\nDone -> {out_mp3}")




if __name__ == "__main__":
    asyncio.run(main())
