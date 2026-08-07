# N2 12/2014 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/5. N2 12-2014/5. Nghe N2 12-2014.mp3` (sha1 `74f74ce28754`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 41:22.2 (41.4 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 79 kb/s | — |
| mean volume | -19.6 dB | −17 to −18 dB |
| max volume | -1.7 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 22 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 12 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **60** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 552 gaps; median **0.91 s**, mean 1.07 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:24.3 | 12.10 s |
| 2 | 2:45.0 | 12.14 s |
| 3 | 3:57.8 | 12.16 s |
| 4 | 5:42.8 | 12.17 s |
| 5 | 7:28.1 | 12.15 s |
| 6 | 7:55.0 | 20.22 s |
| 7 | 9:20.5 | 12.18 s |
| 8 | 9:46.5 | 20.27 s |
| 9 | 11:07.9 | 12.12 s |
| 10 | 11:37.7 | 20.21 s |
| 11 | 13:07.9 | 12.10 s |
| 12 | 13:33.6 | 20.28 s |
| 13 | 14:56.4 | 4.16 s |
| 14 | 15:07.9 | 12.07 s |
| 15 | 15:39.7 | 20.23 s |
| 16 | 17:13.6 | 12.22 s |
| 17 | 17:41.0 | 20.26 s |
| 18 | 18:56.9 | 12.17 s |
| 19 | 20:20.7 | 3.09 s |
| 20 | 20:27.6 | 3.07 s |
| 21 | 20:35.8 | 3.07 s |
| 22 | 20:43.4 | 8.13 s |
| 23 | 21:44.8 | 3.05 s |
| 24 | 21:50.9 | 3.04 s |
| 25 | 21:58.1 | 3.07 s |
| 26 | 22:04.7 | 8.04 s |
| 27 | 23:12.5 | 3.07 s |
| 28 | 23:18.4 | 3.06 s |
| 29 | 23:25.0 | 3.07 s |
| 30 | 23:31.5 | 8.00 s |
| 31 | 24:49.4 | 3.02 s |
| 32 | 24:55.9 | 3.02 s |
| 33 | 25:02.7 | 3.04 s |
| 34 | 25:08.6 | 8.47 s |
| 35 | 26:16.5 | 3.08 s |
| 36 | 26:22.1 | 3.13 s |
| 37 | 26:28.1 | 3.16 s |
| 38 | 26:34.7 | 8.06 s |
| 39 | 27:08.4 | 8.17 s |
| 40 | 27:40.6 | 8.16 s |
| 41 | 28:14.5 | 8.18 s |
| 42 | 28:46.5 | 8.14 s |
| 43 | 29:18.9 | 8.10 s |
| 44 | 29:54.1 | 8.10 s |
| 45 | 30:28.2 | 8.08 s |
| 46 | 31:03.6 | 8.15 s |
| 47 | 31:36.4 | 8.15 s |
| 48 | 32:06.5 | 8.07 s |
| 49 | 32:39.7 | 8.21 s |
| 50 | 33:14.8 | 8.13 s |
| 51 | 35:24.9 | 3.06 s |
| 52 | 35:30.6 | 3.01 s |
| 53 | 35:36.1 | 3.02 s |
| 54 | 35:41.8 | 8.11 s |
| 55 | 37:58.8 | 3.04 s |
| 56 | 38:04.8 | 3.03 s |
| 57 | 38:11.1 | 3.04 s |
| 58 | 38:17.5 | 8.16 s |
| 59 | 40:50.0 | 10.25 s |
| 60 | 41:09.3 | 11.87 s |
