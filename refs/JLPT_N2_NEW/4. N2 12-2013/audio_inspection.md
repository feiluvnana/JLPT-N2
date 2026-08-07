# N2 12/2013 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/4. N2 12-2013/4. Nghe N2 12-2013.mp3` (sha1 `805adf73009b`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 39:35.3 (39.6 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 78 kb/s | — |
| mean volume | -20.4 dB | −17 to −18 dB |
| max volume | -1.0 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 30 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **67** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 585 gaps; median **0.87 s**, mean 1.04 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:16.1 | 12.20 s |
| 2 | 1:41.4 | 4.19 s |
| 3 | 2:31.6 | 4.31 s |
| 4 | 2:43.5 | 12.21 s |
| 5 | 3:08.1 | 3.49 s |
| 6 | 4:10.1 | 4.30 s |
| 7 | 4:21.2 | 12.23 s |
| 8 | 6:06.9 | 12.23 s |
| 9 | 7:33.0 | 12.17 s |
| 10 | 7:57.6 | 20.17 s |
| 11 | 9:10.9 | 12.18 s |
| 12 | 9:37.9 | 20.18 s |
| 13 | 10:45.4 | 12.24 s |
| 14 | 11:11.3 | 20.21 s |
| 15 | 12:38.1 | 12.17 s |
| 16 | 13:04.4 | 20.23 s |
| 17 | 14:21.0 | 12.18 s |
| 18 | 14:47.4 | 20.21 s |
| 19 | 15:48.7 | 3.39 s |
| 20 | 15:59.3 | 12.19 s |
| 21 | 16:25.8 | 20.21 s |
| 22 | 17:28.9 | 3.25 s |
| 23 | 17:41.7 | 12.18 s |
| 24 | 18:58.4 | 3.05 s |
| 25 | 19:04.6 | 3.11 s |
| 26 | 19:11.2 | 3.07 s |
| 27 | 19:17.7 | 8.23 s |
| 28 | 20:31.1 | 3.10 s |
| 29 | 20:37.8 | 3.09 s |
| 30 | 20:45.3 | 3.11 s |
| 31 | 20:52.6 | 8.17 s |
| 32 | 21:59.8 | 3.07 s |
| 33 | 22:05.6 | 3.07 s |
| 34 | 22:11.6 | 3.07 s |
| 35 | 22:18.1 | 8.13 s |
| 36 | 23:29.5 | 3.04 s |
| 37 | 23:36.9 | 3.10 s |
| 38 | 23:43.2 | 3.09 s |
| 39 | 23:49.7 | 8.09 s |
| 40 | 25:05.0 | 3.08 s |
| 41 | 25:12.0 | 3.11 s |
| 42 | 25:19.0 | 3.07 s |
| 43 | 25:26.1 | 8.20 s |
| 44 | 25:59.2 | 8.19 s |
| 45 | 26:30.2 | 8.19 s |
| 46 | 27:04.1 | 3.07 s |
| 47 | 27:32.7 | 8.20 s |
| 48 | 28:02.1 | 8.20 s |
| 49 | 28:38.8 | 5.32 s |
| 50 | 29:07.4 | 8.33 s |
| 51 | 29:41.0 | 8.16 s |
| 52 | 30:11.7 | 8.18 s |
| 53 | 30:44.9 | 8.14 s |
| 54 | 31:15.5 | 7.95 s |
| 55 | 31:48.1 | 8.18 s |
| 56 | 32:04.5 | 2.64 s |
| 57 | 33:50.8 | 4.15 s |
| 58 | 34:05.4 | 3.03 s |
| 59 | 34:10.4 | 3.05 s |
| 60 | 34:15.6 | 3.07 s |
| 61 | 34:20.9 | 8.19 s |
| 62 | 36:07.0 | 3.05 s |
| 63 | 36:12.2 | 3.06 s |
| 64 | 36:17.7 | 3.07 s |
| 65 | 36:23.3 | 8.19 s |
| 66 | 39:03.5 | 10.23 s |
| 67 | 39:23.5 | 10.43 s |
