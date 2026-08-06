# N2 7/2018 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/9. N2 7-2018/9. Nghe N2 7-2018.mp3` (sha1 `e74070ae0c33`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 43:03.3 (43.1 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 192 kb/s | — |
| mean volume | -19.2 dB | −17 to −18 dB |
| max volume | -1.9 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 35 | structural gap |
| ~8 s (5–9.5 s) | 16 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 3 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 12 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **72** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 574 gaps; median **0.95 s**, mean 1.08 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:00.0 | 3.30 s |
| 2 | 1:14.6 | 12.28 s |
| 3 | 2:23.1 | 4.20 s |
| 4 | 2:35.6 | 12.32 s |
| 5 | 4:21.2 | 4.26 s |
| 6 | 4:32.5 | 12.22 s |
| 7 | 5:56.6 | 12.28 s |
| 8 | 7:18.7 | 14.59 s |
| 9 | 8:04.8 | 3.70 s |
| 10 | 8:10.2 | 3.19 s |
| 11 | 8:31.9 | 20.29 s |
| 12 | 9:54.2 | 12.29 s |
| 13 | 10:21.9 | 20.42 s |
| 14 | 11:44.3 | 3.22 s |
| 15 | 11:56.2 | 12.25 s |
| 16 | 12:22.7 | 20.29 s |
| 17 | 13:28.0 | 12.27 s |
| 18 | 13:56.8 | 20.21 s |
| 19 | 15:34.2 | 12.23 s |
| 20 | 16:01.9 | 20.31 s |
| 21 | 17:31.2 | 3.23 s |
| 22 | 17:43.0 | 15.01 s |
| 23 | 18:37.0 | 5.03 s |
| 24 | 18:43.6 | 3.26 s |
| 25 | 19:47.1 | 3.02 s |
| 26 | 19:52.8 | 3.07 s |
| 27 | 19:58.7 | 3.06 s |
| 28 | 20:05.3 | 8.23 s |
| 29 | 21:47.4 | 3.03 s |
| 30 | 21:54.0 | 3.09 s |
| 31 | 22:01.1 | 3.04 s |
| 32 | 22:07.8 | 8.22 s |
| 33 | 23:22.7 | 3.04 s |
| 34 | 23:28.7 | 3.04 s |
| 35 | 23:35.0 | 3.04 s |
| 36 | 23:41.3 | 8.19 s |
| 37 | 24:59.8 | 3.03 s |
| 38 | 25:07.0 | 3.03 s |
| 39 | 25:14.3 | 3.07 s |
| 40 | 25:21.5 | 8.32 s |
| 41 | 26:36.8 | 3.03 s |
| 42 | 26:43.2 | 3.05 s |
| 43 | 26:49.3 | 3.03 s |
| 44 | 26:56.2 | 11.05 s |
| 45 | 27:34.6 | 13.17 s |
| 46 | 27:49.4 | 3.25 s |
| 47 | 28:17.4 | 8.26 s |
| 48 | 28:50.6 | 8.25 s |
| 49 | 29:22.8 | 8.23 s |
| 50 | 29:53.3 | 8.21 s |
| 51 | 30:26.2 | 8.22 s |
| 52 | 30:59.0 | 8.24 s |
| 53 | 31:35.2 | 8.29 s |
| 54 | 32:09.5 | 8.24 s |
| 55 | 32:43.1 | 8.26 s |
| 56 | 33:17.7 | 8.28 s |
| 57 | 33:53.2 | 10.31 s |
| 58 | 34:15.8 | 2.64 s |
| 59 | 34:42.9 | 3.13 s |
| 60 | 34:47.7 | 3.20 s |
| 61 | 36:49.6 | 3.14 s |
| 62 | 36:54.9 | 3.05 s |
| 63 | 37:00.3 | 3.13 s |
| 64 | 37:05.9 | 7.93 s |
| 65 | 39:16.2 | 3.01 s |
| 66 | 39:23.0 | 3.05 s |
| 67 | 39:28.8 | 3.03 s |
| 68 | 39:35.0 | 11.93 s |
| 69 | 40:08.7 | 3.13 s |
| 70 | 40:13.5 | 3.24 s |
| 71 | 42:25.6 | 10.21 s |
| 72 | 42:45.9 | 17.33 s |
