# N2 7/2021 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/12. N2 7-2021/12. Nghe N2 7-2021.mp3` (sha1 `4fbcb22fd625`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 43:19.1 (43.3 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -20.3 dB | −17 to −18 dB |
| max volume | -1.0 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 43 | structural gap |
| ~8 s (5–9.5 s) | 16 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 3 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 12 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **80** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 603 gaps; median **0.94 s**, mean 1.05 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:00.0 | 3.65 s |
| 2 | 0:22.5 | 3.12 s |
| 3 | 0:38.5 | 4.19 s |
| 4 | 1:03.2 | 2.89 s |
| 5 | 1:19.1 | 3.24 s |
| 6 | 1:45.9 | 3.78 s |
| 7 | 1:51.3 | 2.94 s |
| 8 | 2:56.6 | 3.57 s |
| 9 | 3:07.3 | 12.08 s |
| 10 | 4:59.8 | 2.96 s |
| 11 | 5:09.6 | 12.05 s |
| 12 | 6:39.5 | 12.09 s |
| 13 | 7:48.6 | 3.11 s |
| 14 | 7:59.6 | 12.08 s |
| 15 | 9:42.2 | 14.62 s |
| 16 | 10:28.4 | 3.70 s |
| 17 | 10:33.8 | 3.20 s |
| 18 | 10:49.5 | 20.20 s |
| 19 | 11:52.0 | 4.28 s |
| 20 | 12:02.4 | 12.06 s |
| 21 | 12:30.5 | 20.18 s |
| 22 | 13:57.3 | 12.07 s |
| 23 | 14:26.0 | 20.18 s |
| 24 | 15:59.0 | 12.06 s |
| 25 | 16:25.8 | 20.20 s |
| 26 | 18:03.8 | 12.08 s |
| 27 | 18:29.7 | 20.19 s |
| 28 | 19:31.3 | 12.08 s |
| 29 | 19:54.1 | 20.18 s |
| 30 | 20:59.3 | 15.01 s |
| 31 | 21:45.5 | 3.98 s |
| 32 | 22:32.8 | 5.03 s |
| 33 | 22:39.5 | 3.27 s |
| 34 | 23:47.8 | 3.08 s |
| 35 | 23:54.7 | 3.04 s |
| 36 | 24:02.2 | 3.04 s |
| 37 | 24:08.9 | 5.12 s |
| 38 | 25:29.2 | 3.01 s |
| 39 | 25:36.1 | 3.04 s |
| 40 | 25:43.1 | 3.03 s |
| 41 | 25:49.4 | 8.04 s |
| 42 | 27:00.1 | 3.00 s |
| 43 | 27:06.0 | 3.02 s |
| 44 | 27:12.8 | 3.02 s |
| 45 | 27:19.6 | 8.07 s |
| 46 | 28:28.9 | 3.02 s |
| 47 | 28:35.6 | 3.05 s |
| 48 | 28:41.8 | 3.01 s |
| 49 | 28:49.1 | 8.06 s |
| 50 | 30:08.5 | 3.01 s |
| 51 | 30:15.2 | 3.02 s |
| 52 | 30:22.2 | 3.03 s |
| 53 | 30:29.3 | 11.18 s |
| 54 | 31:07.9 | 13.17 s |
| 55 | 31:22.8 | 2.79 s |
| 56 | 31:36.0 | 3.07 s |
| 57 | 31:52.6 | 5.07 s |
| 58 | 32:20.0 | 8.11 s |
| 59 | 32:35.3 | 3.06 s |
| 60 | 32:50.7 | 5.08 s |
| 61 | 33:03.7 | 3.04 s |
| 62 | 33:21.1 | 5.06 s |
| 63 | 33:54.0 | 8.09 s |
| 64 | 34:30.2 | 8.07 s |
| 65 | 35:05.4 | 8.06 s |
| 66 | 35:38.7 | 8.08 s |
| 67 | 35:55.0 | 3.08 s |
| 68 | 36:12.2 | 5.10 s |
| 69 | 36:25.0 | 3.04 s |
| 70 | 36:42.3 | 5.09 s |
| 71 | 37:15.2 | 10.27 s |
| 72 | 37:59.8 | 3.13 s |
| 73 | 38:04.7 | 2.64 s |
| 74 | 39:55.4 | 3.01 s |
| 75 | 40:01.5 | 3.03 s |
| 76 | 40:08.2 | 3.03 s |
| 77 | 40:14.2 | 9.34 s |
| 78 | 40:43.2 | 3.13 s |
| 79 | 40:48.0 | 2.75 s |
| 80 | 42:44.4 | 10.00 s |
