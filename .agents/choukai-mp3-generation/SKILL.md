---
name: choukai-mp3-generation
description: Single owner of synthesizing the choukai exam MP3 from the TTS script — voice assignment, official pacing, silence insertion, concatenation, and loudness. Use whenever generating, fixing, or tuning the listening audio, whenever the user mentions the MP3, voices sounding wrong (e.g., male narrator instead of the official female announcer), rushed pacing, or missing answer pauses. Do not write ad-hoc TTS loops — use scripts/make_choukai_mp3.py.
---

# Choukai MP3 Generation

## Executable & File Paths

- **Script location**: `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py`
- **Input text script**: `tests/<test_id>/聴解スクリプト.txt` (canonical name — see choukai-script-writing)
- **Output audio**: `tests/<test_id>/聴解.mp3` + per-question files in `tests/<test_id>/segments/`
- **Output chapters**: `tests/<test_id>/聴解_チャプター.json` — the start offset
  of every 問題 and every 例/N番 item, accumulated by the assembler as it
  concatenates (exact by construction; never recover these with
  `silencedetect` after the fact). Consumed by `interactive-answer-sheet` to
  drive the chapter dropdown in `解答.html`. Regenerate the MP3 to
  refresh it.

## Execution

Prerequisites: `pip install edge-tts` (free, no key; ffmpeg required).

Run from workspace root:
```bash
python .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
```
→ Outputs `聴解.mp3` inside `tests/<test_id>/`.

A cold build of a full N2 script (~250 lines → ~45 min of audio) takes about a
minute. Lines are synthesized concurrently (`TTS_JOBS = 8`); lower it if the
endpoint starts throttling:
```bash
python .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt --jobs 3
```
The floor is the final `loudnorm` encode (~35 s for a 45-minute file) — that pass
reads the whole assembled stream, so it cannot be split.

## Cleanup & Segment Retention

- **Automatic Cleanup**: Upon successful generation of `聴解.mp3`, the temporary `segments/` directory is automatically cleaned up and deleted to save disk space.
- **Retaining Segments**: If you need to keep per-question audio blocks for debugging or drilling, pass the `--keep-segments` flag:
  ```bash
  python .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt --keep-segments
  ```



## Voice model (matches the official recording)

- **Narrator/announcer = FEMALE** (`ja-JP-NanamiNeural`, rate −10%). The
  official announcer is female; a male narrator was a real user complaint.
- Dialogue: male roles → `ja-JP-KeitaNeural`, female roles → Nanami at
  different rates so she is distinguishable from the narrator.
- 男1/男2 separated by rate (edge-tts free tier has only 2 ja-JP voices;
  `pitch` support varies by version — the script feature-detects it).

## Pacing table (from official Dec 2025 N2 audio — do not guess new values)

| Constant | Value | Meaning |
|---|---|---|
| GAP_BETWEEN_LINES | 1.3 s | between dialogue turns |
| GAP_AFTER_PRE_QUESTION | 3 s | 問1: question → conversation |
| GAP_OPTION_READING | **20 s** | 問2 only: read printed options (most-missed pause) |
| GAP_BETWEEN_SPOKEN_CHOICES | 3 s | 問3/問5 spoken choices |
| GAP_AFTER_SHITSUMON1 | 10 s | 問5: between 質問1 and 質問2 |
| ANSWER_PAUSE | 問1/2: 12 s, 問3/4: 8 s, 問5: 10 s | after each item block |

To recalibrate against official recordings in `refs/JLPT/`, use `official-audio-analysis`
and update ONLY these constants.

## Engineering rules (each fixed a real bug)

- Synthesize per line → convert to 24 kHz mono WAV → concat WAVs → encode MP3
  ONCE with `loudnorm=I=-17:TP=-1.0:LRA=11`. Never concat MP3 segments directly.
- Retry synthesis (3×, backoff); cache segments in `tests/<test_id>/segments/`
  so re-runs skip finished lines. The cache key is a hash of
  **text + voice + rate**, not the line's position — keying on position alone
  meant a reworded line or a remapped speaker silently reused the old audio.
- **Parse into a plan, then synthesize, then assemble — in that order.** The
  plan pins every segment path and every gap duration up front, which is what
  makes the parallel passes safe: two tasks can never target the same file, and
  the assembled output is byte-identical to a sequential build (verified by
  running both versions over one set of cached segments).
- **Silence files are all created before block assembly begins.** Creating them
  lazily let two blocks shell out to ffmpeg for the same `_sil_1.3.wav`
  simultaneously; the loser got a truncated gap. Nothing downstream can detect
  that — the file is still valid audio, just the wrong length.
- Chapter offsets stay a strictly in-order running sum. Block durations are
  measured in parallel, but `clock` must accumulate block by block.
- **Script validation is a hard gate.** `validate_script()` runs before any
  synthesis and refuses to build on a missing 例, a wrong item count, an
  answer spoken aloud, an authoring annotation, or an unmapped speaker label.
  See `choukai-script-writing/SKILL.md` for the full table.
- **Every speaker label must be in `SPEAKER_MAP`.** An unmapped label does not
  raise — `voice_for()` falls back to the narrator, so the line is read by the
  announcer instead of the character. The validator now catches this.
- Item detection regex is `^(例。|\d+番。)` — WITH the 。 so the 問題5 header
  line 「1番、2番。…」 is not mistaken for a question item.

## Dry-run before synthesis (no network needed)

Simulate block parsing + pause assignment. Expected for a full N2 — these
follow directly from `ANSWER_PAUSE` above and the 33 item blocks
(問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2, 例 included):

| Pause | Count | Source |
|---|---|---|
| 12 s answer | 13 | 問題1 (6) + 問題2 (7) |
| 8 s answer | 18 | 問題3 (6) + 問題4 (12) |
| 10 s answer | 2 | 問題5 |
| 20 s option-reading | 7 | 問題2 only (例+6) |

The 33 item blocks are fixed; the TOTAL block count is not (48 in test 1; the
first, since-removed test 4 — removed in 9a794d5, last at b9b90de — was 56;
the current test 4 is 113 — instruction splitting differs), so never treat it
as a target.
Estimated length ≈ 45 min with TTS at these rates — the four built tests
measure 41.6–45.7 min per their 聴解_チャプター.json (official ≈ 51 min;
human actors speak slower, and the remaining gap is acceptable).

