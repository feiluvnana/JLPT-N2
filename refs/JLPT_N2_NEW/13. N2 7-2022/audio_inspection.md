# N2 7/2022 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/13. N2 7-2022/13. Nghe N2 T7-2022.mp3` (sha1 `0dd2124b7988`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 43:37.7 (43.6 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -20.1 dB | −17 to −18 dB |
| max volume | -1.0 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 40 | structural gap |
| ~8 s (5–9.5 s) | 17 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **75** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 650 gaps; median **0.82 s**, mean 1.00 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:00.0 | 4.36 s |
| 2 | 0:15.1 | 3.07 s |
| 3 | 0:30.0 | 4.11 s |
| 4 | 0:57.6 | 3.60 s |
| 5 | 1:20.5 | 3.06 s |
| 6 | 1:25.2 | 3.04 s |
| 7 | 2:26.0 | 12.23 s |
| 8 | 2:51.7 | 2.54 s |
| 9 | 3:39.7 | 4.18 s |
| 10 | 3:51.8 | 12.23 s |
| 11 | 4:18.0 | 2.55 s |
| 12 | 5:16.4 | 4.06 s |
| 13 | 5:27.3 | 12.20 s |
| 14 | 7:17.1 | 12.18 s |
| 15 | 8:47.7 | 12.32 s |
| 16 | 9:26.3 | 2.91 s |
| 17 | 9:30.8 | 2.95 s |
| 18 | 9:51.2 | 20.18 s |
| 19 | 11:40.0 | 12.23 s |
| 20 | 12:07.1 | 20.18 s |
| 21 | 13:27.2 | 12.19 s |
| 22 | 13:52.9 | 20.21 s |
| 23 | 15:24.7 | 12.23 s |
| 24 | 15:49.8 | 20.18 s |
| 25 | 16:59.0 | 12.22 s |
| 26 | 17:25.7 | 20.18 s |
| 27 | 19:26.4 | 12.17 s |
| 28 | 19:53.6 | 20.18 s |
| 29 | 21:14.4 | 12.51 s |
| 30 | 21:57.7 | 4.21 s |
| 31 | 22:39.0 | 2.97 s |
| 32 | 22:43.7 | 3.37 s |
| 33 | 23:52.3 | 3.01 s |
| 34 | 24:00.0 | 3.01 s |
| 35 | 24:07.0 | 3.02 s |
| 36 | 24:14.1 | 8.20 s |
| 37 | 25:32.5 | 3.01 s |
| 38 | 25:38.6 | 3.01 s |
| 39 | 25:45.0 | 3.02 s |
| 40 | 25:52.2 | 8.18 s |
| 41 | 27:08.6 | 3.01 s |
| 42 | 27:15.3 | 3.01 s |
| 43 | 27:22.3 | 3.01 s |
| 44 | 27:29.0 | 8.19 s |
| 45 | 28:36.4 | 3.01 s |
| 46 | 28:44.1 | 3.02 s |
| 47 | 28:51.3 | 3.02 s |
| 48 | 28:57.9 | 8.19 s |
| 49 | 30:36.1 | 3.02 s |
| 50 | 30:42.7 | 3.01 s |
| 51 | 30:50.0 | 3.01 s |
| 52 | 30:57.2 | 8.19 s |
| 53 | 31:28.9 | 3.11 s |
| 54 | 31:33.7 | 3.12 s |
| 55 | 32:01.9 | 8.21 s |
| 56 | 32:38.7 | 8.24 s |
| 57 | 33:12.0 | 8.19 s |
| 58 | 33:45.4 | 8.19 s |
| 59 | 34:16.6 | 8.21 s |
| 60 | 34:48.5 | 8.23 s |
| 61 | 35:19.6 | 8.22 s |
| 62 | 35:55.2 | 8.19 s |
| 63 | 36:33.6 | 8.19 s |
| 64 | 37:07.3 | 8.15 s |
| 65 | 37:40.0 | 8.25 s |
| 66 | 38:01.9 | 2.55 s |
| 67 | 38:22.0 | 3.06 s |
| 68 | 38:26.3 | 2.90 s |
| 69 | 40:12.0 | 3.01 s |
| 70 | 40:18.5 | 3.56 s |
| 71 | 40:25.2 | 3.01 s |
| 72 | 40:32.3 | 8.13 s |
| 73 | 40:59.0 | 3.05 s |
| 74 | 41:03.4 | 2.87 s |
| 75 | 43:03.3 | 10.01 s |
