# N2 7/2025 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/16. N2 7-2025/Nghe N2 T7-2025.mp3` (sha1 `7f0144f99d9b`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 42:10.2 (42.2 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 48000 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -17.4 dB | −17 to −18 dB |
| max volume | -0.5 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 37 | structural gap |
| ~8 s (5–9.5 s) | 16 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **71** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 621 gaps; median **0.86 s**, mean 1.04 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:11.2 | 3.07 s |
| 2 | 0:26.0 | 4.04 s |
| 3 | 1:04.9 | 3.54 s |
| 4 | 1:27.8 | 3.15 s |
| 5 | 1:32.6 | 2.85 s |
| 6 | 2:41.6 | 12.31 s |
| 7 | 4:08.8 | 12.29 s |
| 8 | 5:40.9 | 12.29 s |
| 9 | 6:51.4 | 12.28 s |
| 10 | 8:20.2 | 12.75 s |
| 11 | 8:59.2 | 2.99 s |
| 12 | 9:03.9 | 2.82 s |
| 13 | 9:23.9 | 20.15 s |
| 14 | 10:37.3 | 12.40 s |
| 15 | 11:04.2 | 20.24 s |
| 16 | 12:24.1 | 12.59 s |
| 17 | 12:52.8 | 20.21 s |
| 18 | 14:26.9 | 12.37 s |
| 19 | 14:52.5 | 20.22 s |
| 20 | 16:24.2 | 12.36 s |
| 21 | 16:51.7 | 20.22 s |
| 22 | 18:23.6 | 12.35 s |
| 23 | 18:52.3 | 20.22 s |
| 24 | 20:09.5 | 12.90 s |
| 25 | 20:53.6 | 3.84 s |
| 26 | 21:35.4 | 3.06 s |
| 27 | 21:40.2 | 2.94 s |
| 28 | 22:38.5 | 3.07 s |
| 29 | 22:45.8 | 3.12 s |
| 30 | 22:52.7 | 3.11 s |
| 31 | 22:58.9 | 8.20 s |
| 32 | 24:06.1 | 3.11 s |
| 33 | 24:12.2 | 3.13 s |
| 34 | 24:18.1 | 3.12 s |
| 35 | 24:24.5 | 8.35 s |
| 36 | 25:47.7 | 3.13 s |
| 37 | 25:53.7 | 3.09 s |
| 38 | 26:00.2 | 3.16 s |
| 39 | 26:06.7 | 8.32 s |
| 40 | 27:07.7 | 3.09 s |
| 41 | 27:14.4 | 3.14 s |
| 42 | 27:21.3 | 3.08 s |
| 43 | 27:28.9 | 8.41 s |
| 44 | 28:48.5 | 3.09 s |
| 45 | 28:55.1 | 3.11 s |
| 46 | 29:02.2 | 3.08 s |
| 47 | 29:09.3 | 8.45 s |
| 48 | 29:41.3 | 3.12 s |
| 49 | 29:46.1 | 3.04 s |
| 50 | 30:14.6 | 8.12 s |
| 51 | 30:46.2 | 8.31 s |
| 52 | 31:17.7 | 8.23 s |
| 53 | 31:49.3 | 8.25 s |
| 54 | 32:24.3 | 8.34 s |
| 55 | 32:59.5 | 8.34 s |
| 56 | 33:32.8 | 8.21 s |
| 57 | 34:05.7 | 8.32 s |
| 58 | 34:40.4 | 8.30 s |
| 59 | 35:13.6 | 4.40 s |
| 60 | 35:44.9 | 8.69 s |
| 61 | 36:07.5 | 2.55 s |
| 62 | 36:27.6 | 3.05 s |
| 63 | 36:31.9 | 2.78 s |
| 64 | 38:56.7 | 3.02 s |
| 65 | 39:02.8 | 3.04 s |
| 66 | 39:08.8 | 3.08 s |
| 67 | 39:14.8 | 8.47 s |
| 68 | 39:41.8 | 3.05 s |
| 69 | 39:46.2 | 2.85 s |
| 70 | 41:36.7 | 2.83 s |
| 71 | 41:49.4 | 10.11 s |
