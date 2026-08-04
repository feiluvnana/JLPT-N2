---
name: official-audio-analysis
description: Single owner of how to analyze official JLPT listening audio (MP3/CD tracks) to extract pacing, pause structure, and loudness for replication. Use whenever an official or sample choukai MP3 is provided, whenever the user says "learn from this audio", or whenever MP3 generation pacing needs calibration or verification. Output of this skill is a pacing table consumed by choukai-mp3-generation.
---

# Official Audio Analysis

## Locating Audio References (`refs/`)

Audio reference files live under `refs/` at the workspace root:

- **Official Exam Audio (`refs/JLPT/`) — 5 Recent Exams**:
  - July 2023: `"refs/JLPT/File nghe N2 7-2023.mp3"`
  - Dec 2023: `"refs/JLPT/14. Nghe N2 T12-2023.mp3"`
  - Dec 2024: `"refs/JLPT/Nghe N2 T12-2024.mp3"`
  - July 2025: `"refs/JLPT/Nghe N2 T7-2025.mp3"`
  - Dec 2025: `"refs/JLPT/JLPT N2 12.2025 Choukai.mp3"`
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
| answer pause 問5 (質問1 → 10s → 質問2 → 12s) | 10-12 s |
| loudness target | −17 LUFS |

