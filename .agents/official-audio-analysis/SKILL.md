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
| 38.8–44.8 min | internal gaps only 1.0–2.0 s (nothing ≥2.5 s) → 8.19 s answer pause, 13 items over ~8 min | 問題4 |
| 47.4–51.2 min | 3 × 3.0 s gaps → 8.5 s; then 10 s + 12.3 s at the very end | 問題5 (1番/2番, then 3番's 質問1/質問2) |

**The 問題4 row is the load-bearing one**: its three choices are read
continuously, so the 3 s spoken-choice gap belongs to 問題3/問題5 ONLY. Whole-file
histogram for cross-checking a full N2: 7 × 20 s, 12 × ~12 s, 17 × ~8 s, 42 × ~3 s.

## Step 4 — Short gaps (dialogue pacing)

Re-run with `d=0.8` on a single-item track: gaps between dialogue turns in
official audio ≈ 1.0-1.5 s (use 1.3 s).

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

