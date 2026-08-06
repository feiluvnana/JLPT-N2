# N2 7/2023 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/14. N2 7-2023/File nghe N2 7-2023.mp3` (sha1 `6b72e515d84a`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 45:14.3 (45.2 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -20.1 dB | −17 to −18 dB |
| max volume | -0.7 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 35 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **71** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 693 gaps; median **0.78 s**, mean 0.99 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:11.3 | 3.07 s |
| 2 | 0:26.2 | 4.11 s |
| 3 | 0:53.8 | 3.60 s |
| 4 | 1:16.8 | 3.06 s |
| 5 | 1:21.4 | 3.03 s |
| 6 | 3:02.4 | 12.21 s |
| 7 | 4:34.5 | 12.20 s |
| 8 | 6:13.2 | 12.16 s |
| 9 | 7:54.5 | 12.20 s |
| 10 | 9:01.0 | 12.29 s |
| 11 | 9:39.5 | 2.91 s |
| 12 | 9:44.0 | 2.96 s |
| 13 | 10:02.5 | 20.18 s |
| 14 | 11:38.0 | 12.22 s |
| 15 | 12:04.0 | 20.19 s |
| 16 | 13:45.0 | 12.16 s |
| 17 | 14:12.4 | 20.18 s |
| 18 | 15:56.2 | 12.17 s |
| 19 | 16:22.7 | 20.18 s |
| 20 | 18:03.0 | 12.14 s |
| 21 | 18:33.1 | 20.20 s |
| 22 | 19:45.9 | 12.24 s |
| 23 | 20:15.0 | 20.18 s |
| 24 | 21:36.1 | 12.49 s |
| 25 | 22:19.4 | 4.21 s |
| 26 | 23:00.7 | 2.97 s |
| 27 | 23:05.4 | 3.36 s |
| 28 | 24:18.0 | 3.01 s |
| 29 | 24:24.9 | 3.01 s |
| 30 | 24:31.1 | 3.02 s |
| 31 | 24:37.1 | 8.18 s |
| 32 | 25:40.8 | 3.03 s |
| 33 | 25:47.6 | 3.03 s |
| 34 | 25:55.1 | 3.03 s |
| 35 | 26:02.0 | 8.22 s |
| 36 | 27:46.4 | 3.01 s |
| 37 | 27:52.4 | 3.02 s |
| 38 | 27:58.5 | 3.01 s |
| 39 | 28:04.6 | 8.20 s |
| 40 | 29:14.4 | 3.01 s |
| 41 | 29:20.4 | 3.01 s |
| 42 | 29:26.4 | 3.02 s |
| 43 | 29:32.9 | 8.20 s |
| 44 | 31:00.1 | 3.02 s |
| 45 | 31:06.7 | 3.02 s |
| 46 | 31:12.6 | 3.02 s |
| 47 | 31:18.8 | 8.18 s |
| 48 | 31:50.5 | 3.11 s |
| 49 | 31:55.3 | 3.11 s |
| 50 | 32:24.0 | 8.23 s |
| 51 | 33:00.6 | 8.17 s |
| 52 | 33:33.6 | 8.15 s |
| 53 | 34:08.7 | 8.23 s |
| 54 | 34:40.8 | 8.18 s |
| 55 | 35:14.3 | 8.19 s |
| 56 | 35:48.6 | 8.17 s |
| 57 | 36:24.2 | 8.23 s |
| 58 | 37:00.1 | 8.23 s |
| 59 | 37:33.9 | 8.17 s |
| 60 | 38:08.5 | 8.16 s |
| 61 | 38:30.2 | 2.55 s |
| 62 | 38:50.4 | 3.06 s |
| 63 | 38:54.7 | 2.90 s |
| 64 | 41:00.0 | 3.01 s |
| 65 | 41:06.6 | 3.03 s |
| 66 | 41:13.3 | 3.01 s |
| 67 | 41:19.7 | 8.14 s |
| 68 | 41:46.4 | 3.05 s |
| 69 | 41:50.7 | 2.86 s |
| 70 | 43:59.8 | 10.01 s |
| 71 | 45:09.1 | 5.17 s |
