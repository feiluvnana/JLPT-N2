#!/usr/bin/env python3
"""
N2 choukai exam MP3 generator (v2) — official-style audio.

Calibrated against a real JLPT-prep CD track:
  - Narrator/announcer: FEMALE voice (ja-JP-NanamiNeural), slightly slow,
    like the official test announcer.
  - ~1.3 s of air between utterances (measured from the sample track).
  - Answer pauses: 12 s after each question (8 s for 問題4 quick response).
  - Output loudness normalized to about -17 LUFS to match the sample level.

Setup (one time):
    pip install edge-tts
    # ffmpeg must be on PATH (macOS: brew install ffmpeg)

Run:
    python make_choukai_mp3.py 3_n2_choukai_tts_script.txt

Output:
    n2_choukai_exam.mp3   (full exam)
    segments/             (per-block mp3s for drilling single questions)

Re-running is cheap: already-synthesized lines are skipped (delete the
segments/ folder to force a full rebuild).
"""

import asyncio
import inspect
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


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep_segments = "--keep-segments" in sys.argv

    if args:
        src = Path(args[0])
    else:
        src = Path("聴解スクリプト.txt") if Path("聴解スクリプト.txt").exists() else Path("script.txt")

    out_dir = src.parent if src.parent != Path("") else Path(".")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", src.read_text(encoding="utf-8"))
              if b.strip()]

    seg = out_dir / "segments"
    seg.mkdir(exist_ok=True)

    silence_cache = {}

    def silence(seconds: float) -> Path:
        if seconds not in silence_cache:
            f = seg / f"_sil_{seconds:g}.wav"
            if not f.exists():
                make_silence_wav(seconds, f)
            silence_cache[seconds] = f
        return silence_cache[seconds]

    playlist = []
    section = ""
    for bi, block in enumerate(blocks):
        lines = [l for l in block.splitlines() if l.strip()]
        first = lines[0]
        if re.match(r"^問題\d+。", first):
            section = first.rstrip("。")
        print(f"[{bi + 1}/{len(blocks)}] {first[:34]}")

        is_item_block = bool(ITEM_RE.match(first))
        wavs = []
        prev_line = ""
        for li, line in enumerate(lines):
            spec, spoken = voice_for(line)
            if not spoken:
                continue
            mp3 = seg / f"b{bi:03d}_l{li:02d}.mp3"
            wav = mp3.with_suffix(".wav")
            if not wav.exists():
                await synth(spoken, spec["voice"], spec["rate"], mp3)
                to_wav(mp3, wav)
            if wavs:
                gap = gap_before_line(section, li, line, prev_line, is_item_block)
                wavs.append(silence(gap))
            wavs.append(wav)
            prev_line = line

        block_wav = seg / f"block_{bi:03d}.wav"
        concat_wavs(wavs, block_wav)
        wav_to_mp3(block_wav, seg / f"block_{bi:03d}.mp3")  # per-question drill file

        playlist.append(block_wav)
        playlist.append(silence(pause_after(first, section)))

    full_wav = out_dir / "_n2_full.wav"
    out_mp3 = out_dir / "聴解.mp3"
    concat_wavs(playlist, full_wav)
    wav_to_mp3(full_wav, out_mp3, normalize=True)
    if full_wav.exists():
        full_wav.unlink()

    # Cleanup temporary segments directory
    if not keep_segments and seg.exists():
        import shutil
        shutil.rmtree(seg)
        print(f"Cleaned up temporary directory: {seg}")

    print(f"\nDone -> {out_mp3}")




if __name__ == "__main__":
    asyncio.run(main())
