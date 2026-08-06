# N2 12/2024 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/15. N2 12-2024/Nghe N2 T12-2024.mp3` (sha1 `4cf60c76d197`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 49:42.7 (49.7 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 192 kb/s | — |
| mean volume | -21.7 dB | −17 to −18 dB |
| max volume | -1.7 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 53 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 3 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 0 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **81** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 702 gaps; median **0.76 s**, mean 1.03 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:11.1 | 3.07 s |
| 2 | 1:24.1 | 3.05 s |
| 3 | 2:53.9 | 3.28 s |
| 4 | 4:10.5 | 2.69 s |
| 5 | 4:19.6 | 9.42 s |
| 6 | 5:43.1 | 2.61 s |
| 7 | 5:53.0 | 8.76 s |
| 8 | 7:14.4 | 2.58 s |
| 9 | 7:24.6 | 8.73 s |
| 10 | 8:32.2 | 2.61 s |
| 11 | 8:39.0 | 8.80 s |
| 12 | 10:01.1 | 2.76 s |
| 13 | 10:11.8 | 9.52 s |
| 14 | 10:47.6 | 3.05 s |
| 15 | 11:05.4 | 20.19 s |
| 16 | 12:40.0 | 3.35 s |
| 17 | 13:01.8 | 20.39 s |
| 18 | 14:12.6 | 2.61 s |
| 19 | 14:24.4 | 8.74 s |
| 20 | 14:52.0 | 19.88 s |
| 21 | 16:21.1 | 2.69 s |
| 22 | 16:34.1 | 8.66 s |
| 23 | 16:58.9 | 20.45 s |
| 24 | 18:02.8 | 2.66 s |
| 25 | 18:16.7 | 8.70 s |
| 26 | 18:38.9 | 20.44 s |
| 27 | 19:40.2 | 2.70 s |
| 28 | 19:51.9 | 8.61 s |
| 29 | 20:15.4 | 20.20 s |
| 30 | 21:19.1 | 2.67 s |
| 31 | 21:29.9 | 8.76 s |
| 32 | 21:57.2 | 19.54 s |
| 33 | 23:28.6 | 2.53 s |
| 34 | 23:40.5 | 9.73 s |
| 35 | 24:41.5 | 3.96 s |
| 36 | 25:20.1 | 3.07 s |
| 37 | 26:57.8 | 3.23 s |
| 38 | 27:56.1 | 3.09 s |
| 39 | 28:02.5 | 3.03 s |
| 40 | 28:09.3 | 2.98 s |
| 41 | 28:16.2 | 4.93 s |
| 42 | 29:17.2 | 2.59 s |
| 43 | 29:32.8 | 3.11 s |
| 44 | 29:39.4 | 3.03 s |
| 45 | 29:45.3 | 3.23 s |
| 46 | 29:52.8 | 4.67 s |
| 47 | 31:05.5 | 2.59 s |
| 48 | 31:21.4 | 2.90 s |
| 49 | 31:28.2 | 2.86 s |
| 50 | 31:35.1 | 2.93 s |
| 51 | 31:41.7 | 4.69 s |
| 52 | 32:57.3 | 2.98 s |
| 53 | 33:04.7 | 2.93 s |
| 54 | 33:11.4 | 3.00 s |
| 55 | 33:18.8 | 4.78 s |
| 56 | 34:39.4 | 2.97 s |
| 57 | 34:46.5 | 2.79 s |
| 58 | 34:53.4 | 2.94 s |
| 59 | 35:01.2 | 5.19 s |
| 60 | 35:29.9 | 3.05 s |
| 61 | 36:17.9 | 3.18 s |
| 62 | 36:49.0 | 5.02 s |
| 63 | 37:21.8 | 5.05 s |
| 64 | 37:55.1 | 4.84 s |
| 65 | 38:28.2 | 4.94 s |
| 66 | 39:01.0 | 5.17 s |
| 67 | 39:36.9 | 4.77 s |
| 68 | 40:12.6 | 4.79 s |
| 69 | 40:47.2 | 5.23 s |
| 70 | 41:23.1 | 4.97 s |
| 71 | 41:57.7 | 5.06 s |
| 72 | 42:36.8 | 5.31 s |
| 73 | 42:59.7 | 2.55 s |
| 74 | 43:19.8 | 3.06 s |
| 75 | 45:45.1 | 2.86 s |
| 76 | 45:53.2 | 2.83 s |
| 77 | 46:01.1 | 2.86 s |
| 78 | 46:07.8 | 5.10 s |
| 79 | 46:31.4 | 3.05 s |
| 80 | 48:45.5 | 9.84 s |
| 81 | 49:05.1 | 8.40 s |
