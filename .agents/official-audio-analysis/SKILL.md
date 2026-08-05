---
name: official-audio-analysis
description: Single owner of how to analyze official JLPT listening audio (MP3/CD tracks) to extract pacing, pause structure, and loudness for replication. Use whenever an official or sample choukai MP3 is provided, whenever the user says "learn from this audio", or whenever MP3 generation pacing needs calibration or verification. Output of this skill is a pacing table consumed by choukai-mp3-generation.
---

# Official Audio Analysis

## Locating Audio References (`refs/`)

Audio reference files live under `refs/` at the workspace root:

- **Official Exam Audio**: the 5 recent exams' MP3s in `refs/JLPT/`. Exact
  filenames are owned by **`AGENTS.md` section 3** — quote the path from there
  (they contain spaces, so always quote). The Dec 2025 file
  `"refs/JLPT/JLPT N2 12.2025 Choukai.mp3"` is the calibration baseline and is
  the one used in the commands below.
- **Textbook CD tracks**: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai-CD/`

## Step 1 — Basics & Multi-Exam Comparison

```bash
# Check basic audio parameters across official exam MP3s:
ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1 "refs/JLPT/JLPT N2 12.2025 Choukai.mp3"
ffmpeg -i "refs/JLPT/JLPT N2 12.2025 Choukai.mp3" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
```

Official N2 full exam audio is consistently ~50-52 min across all 5 recent exams. Mean volume averages -17 to -18 dB (target -17 LUFS for synthesis output).

## Step 2 — Long-pause histogram

```bash
ffmpeg -i "refs/JLPT/JLPT N2 12.2025 Choukai.mp3" -af silencedetect=noise=-35dB:d=2.5 -f null - 2>&1 \
  | grep -oP "silence_duration: \K[0-9.]+"
```

Bucket the durations. A full official N2 exam clusters as:
~3s (structural) / ~8s (answer time 問3・問4) / ~12s (answer time 問1・問2) /
~20s (問題2 option-READING time — easy to miss and critical).

## Step 3 — Timeline attribution

Print ordered `(start_time, duration)` pairs and read the sequence. Patterns
identify sections without hearing a word:

- `20s → …talk… → 12s` repeating → 問題2 (reading pause + answer pause)
- `3s, 3s, 3s, 8s` repeating → 問題3/5 spoken choices (3s apart) + answer time
- dense run of lone `8s` pauses → 問題4
- `10s` then `12s` near the end → 問題5 two-question item (質問1/質問2)

Measured on Dec 2025 (`silencedetect` at `d=2.5` then `d=0.4`), which is where
the constants in `choukai-mp3-generation` come from:

| Region | Signature | Section |
|---|---|---|
| 36.4–37.0 min | 3 × 3.0 s gaps → 4 spoken choices → 8.57 s answer pause | 問題3 |
| 38.7–44.7 min | internal gaps only 1.0–2.0 s (nothing ≥2.5 s) → 8.19 s answer pause, **11 items** over ~6 min | 問題4 |
| 47.3–51.4 min | 3 × 3.0 s gaps → 8.5 s; then 10.0 s + 12.3 s at the very end | 問題5 — **1番** (spoken choices), then **2番's** 質問1 / 質問2 |

**The 問題4 row is the load-bearing one**: its three choices are read
continuously, so the 3 s spoken-choice gap belongs to 問題3/問題5 ONLY. Whole-file
histogram for cross-checking a full N2: 7 × 20 s, 12 × ~12 s, 17 × ~8 s, 42 × ~3 s.

**The histogram is also the cheapest proof of the item counts** (re-measured on
the Dec 2025 file, total 51.4 min), because official audio gives an answer pause
after **scored items only** — never after an 例, which is followed straight by
the 「最もよいものは◯番です…」 confirmation:

- 12 × 12 s = 問題1 (5) + 問題2 (6) + the final 質問2 (1)
- 7 × 20 s = 問題2's option-reading time, 例 + 6 items
- 17 × 8 s = 問題3 (5) + 問題4 (**11**) + 問題5 1番 (1)
- so the paper is 5 / 6 / 5 / 11 / 3 = 30 answers, exactly the table in
  `jlpt-exam-structure` — and **not** the 2009 guidebook's 目安 (12 即時応答,
  4 統合理解). If a future measurement disagrees with those counts, re-measure
  before believing it; two earlier revisions of this file carried the
  guidebook's numbers as if they had been measured.

Note this is where our build deliberately deviates: `make_choukai_mp3.py`
appends `ANSWER_PAUSE` after **every** item block, 例 included, so a generated
MP3 has 13 × 12 s / 18 × 8 s where the official file has 12 / 17. See the
dry-run table in `choukai-mp3-generation`.

## Step 4 — Short gaps (dialogue pacing)

Re-run with `d=0.8` on a single-item track: gaps between dialogue turns in
official audio ≈ 1.0-1.5 s (use 1.3 s).

## Step 5 — Speech rate (not just pauses)

Pause structure alone does not prove the exam isn't underestimating N2 level —
a correctly-paced recording of speech that is itself too SLOW still makes the
exam easier than the real thing. This was never checked before it shipped
across 4 generated tests: `choukai-mp3-generation`'s `SPEAKER_MAP` rates
(−8% to +6% per character, −10% narrator) were chosen only to make voices
distinguishable from each other, never calibrated against measured official
speech tempo.

Measure rate in **morae/minute**, not characters/minute — kanji-heavy text
compresses multiple morae per character, so a raw character count
understates true speech density. Natural adult Japanese conversation runs
**~300–400+ morae/min**.

**Mind the level band: N2 is not N1.** The official 認定の目安 says N1 listens
to 「**自然な**スピードの、まとまりのある会話やニュース、講義」 while N2 listens
to 「**自然に近い**スピードの、まとまりのある会話やニュース」 (N3: 「やや自然に
近い」). So the target for N2 dialogue is at or a little below natural — not the
top of the natural band. Anything *noticeably* under it is still a real defect
(N4/N5 slow-for-beginners pacing makes the exam easier than it is), but do not
push rates upward to reach an N1 figure.

Verified for this repo's current voices (synthesize a representative line at
the exact production voice/rate, measure duration, count morae by hand):
- **Dialogue lines** (character voices, rate ±0–6%): a 43-mora line took
  6.816 s → **~378 morae/min** — within/above natural range. This is the
  actually-tested content; it is not underestimating N2 pace.
- **Narrator/announcer** (rate −10%): a 42-mora line took 8.544 s →
  **~295 morae/min** — more measured than the dialogue rate, but this only
  affects administrative instructions ("問題1では…"), never scored content.

Re-verify this whenever a voice or rate value changes in
`choukai-mp3-generation`'s `SPEAKER_MAP`/`NARRATOR` — a "faster to build" or
"clearer" rate tweak is exactly the kind of change that can silently drift
back toward underestimating difficulty without anyone noticing, since nothing
else in the pipeline checks rate.

## Deliverable

A pacing table in this exact shape (feed to choukai-mp3-generation):

| Parameter | Official value |
|---|---|
| gap between dialogue turns | 1.3 s |
| after question, before talk (問1) | 3 s |
| 問題2 option-reading pause | 20 s |
| between spoken choices (問3/5) | 3 s |
| answer pause 問1/問2 | 12 s |
| answer pause 問3/問4 | 8 s |
| answer pause 問5 (each item; the 質問1 → 質問2 gap is also 10 s) | 10 s |
| loudness target | −17 LUFS |
| dialogue speech rate (character voices) | ~300–400 morae/min; N2's 認定の目安 is 自然に**近い** speed, so sit at or just below natural (verified ~378 — already at the top of the band; do not raise) |
| narrator/announcer speech rate | more measured than dialogue is fine (verified ~295); never let it drift onto scored content |

Note: Step 3 measures 問題5's 1番/2番 answer pause at 8.5 s; the table adopts
10 s deliberately, aligning it with the 質問1→質問2 gap rather than the single
measured instance. The copy of this table in `choukai-mp3-generation/SKILL.md`
is the one `make check` diffs against the code — change values there (and in
the code) first, then mirror here.

