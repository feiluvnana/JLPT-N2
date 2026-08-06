# N2 12/2010 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/1. N2 12-2010/1. Nghe N2 12-2010.mp3` (sha1 `7a1517e2c5a0`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 46:56.5 (46.9 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 32000 Hz / 2 | — |
| bit rate | 80 kb/s | — |
| mean volume | -17.9 dB | −17 to −18 dB |
| max volume | -1.8 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 40 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **79** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 721 gaps; median **0.97 s**, mean 1.05 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:09.6 | 3.28 s |
| 2 | 1:33.8 | 12.16 s |
| 3 | 2:53.8 | 12.15 s |
| 4 | 4:18.1 | 12.15 s |
| 5 | 5:54.0 | 12.15 s |
| 6 | 7:17.0 | 12.20 s |
| 7 | 7:57.4 | 3.10 s |
| 8 | 8:02.7 | 3.35 s |
| 9 | 8:19.1 | 20.16 s |
| 10 | 9:53.6 | 3.38 s |
| 11 | 9:58.6 | 3.24 s |
| 12 | 10:16.2 | 20.16 s |
| 13 | 11:19.8 | 12.16 s |
| 14 | 11:46.5 | 20.19 s |
| 15 | 12:57.9 | 12.18 s |
| 16 | 13:23.7 | 20.18 s |
| 17 | 14:38.9 | 12.18 s |
| 18 | 15:07.5 | 20.29 s |
| 19 | 16:15.9 | 12.18 s |
| 20 | 16:41.7 | 20.20 s |
| 21 | 17:51.1 | 12.19 s |
| 22 | 18:16.8 | 20.23 s |
| 23 | 19:44.2 | 12.23 s |
| 24 | 20:28.2 | 3.67 s |
| 25 | 21:11.3 | 3.08 s |
| 26 | 21:16.6 | 3.24 s |
| 27 | 22:52.6 | 3.23 s |
| 28 | 22:57.5 | 3.34 s |
| 29 | 23:51.7 | 3.07 s |
| 30 | 23:58.5 | 3.13 s |
| 31 | 24:05.2 | 3.10 s |
| 32 | 24:11.9 | 8.18 s |
| 33 | 25:22.6 | 3.07 s |
| 34 | 25:28.1 | 3.08 s |
| 35 | 25:33.7 | 3.08 s |
| 36 | 25:39.5 | 8.26 s |
| 37 | 27:01.0 | 3.04 s |
| 38 | 27:07.3 | 3.10 s |
| 39 | 27:14.6 | 3.11 s |
| 40 | 27:22.0 | 8.22 s |
| 41 | 28:35.8 | 3.07 s |
| 42 | 28:42.3 | 3.09 s |
| 43 | 28:48.3 | 3.10 s |
| 44 | 28:55.1 | 8.19 s |
| 45 | 30:13.8 | 3.08 s |
| 46 | 30:20.7 | 3.09 s |
| 47 | 30:27.5 | 3.05 s |
| 48 | 30:34.4 | 8.19 s |
| 49 | 31:07.6 | 3.12 s |
| 50 | 31:12.8 | 3.23 s |
| 51 | 31:59.4 | 3.20 s |
| 52 | 32:04.2 | 3.43 s |
| 53 | 32:33.3 | 8.19 s |
| 54 | 33:03.7 | 8.18 s |
| 55 | 33:35.6 | 8.20 s |
| 56 | 34:04.7 | 8.23 s |
| 57 | 34:34.8 | 8.22 s |
| 58 | 35:06.4 | 8.23 s |
| 59 | 35:39.3 | 8.17 s |
| 60 | 36:12.0 | 8.22 s |
| 61 | 36:43.3 | 8.25 s |
| 62 | 37:17.3 | 8.21 s |
| 63 | 37:49.6 | 8.20 s |
| 64 | 38:20.5 | 8.30 s |
| 65 | 38:44.7 | 2.55 s |
| 66 | 39:08.9 | 3.10 s |
| 67 | 39:13.6 | 3.31 s |
| 68 | 41:17.0 | 3.17 s |
| 69 | 41:22.4 | 3.14 s |
| 70 | 41:28.0 | 3.12 s |
| 71 | 41:33.4 | 8.27 s |
| 72 | 43:29.7 | 3.08 s |
| 73 | 43:35.4 | 3.10 s |
| 74 | 43:41.6 | 3.10 s |
| 75 | 43:47.6 | 8.21 s |
| 76 | 44:20.2 | 3.30 s |
| 77 | 44:36.3 | 2.64 s |
| 78 | 46:23.0 | 10.20 s |
| 79 | 46:42.6 | 10.57 s |
