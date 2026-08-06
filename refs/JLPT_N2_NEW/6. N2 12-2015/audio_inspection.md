# N2 12/2015 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/6. N2 12-2015/6. Nghe N2 12-2015.mp3` (sha1 `6abdc685bea8`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 52:04.7 (52.1 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 48000 Hz / 2 | — |
| bit rate | 78 kb/s | — |
| mean volume | -18.6 dB | −17 to −18 dB |
| max volume | -0.2 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 42 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **81** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 775 gaps; median **0.86 s**, mean 1.04 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:17.6 | 3.07 s |
| 2 | 0:32.4 | 3.44 s |
| 3 | 1:35.3 | 3.05 s |
| 4 | 1:40.0 | 2.97 s |
| 5 | 3:08.0 | 3.28 s |
| 6 | 3:12.9 | 3.00 s |
| 7 | 4:23.1 | 11.81 s |
| 8 | 5:52.9 | 12.04 s |
| 9 | 7:18.1 | 11.90 s |
| 10 | 9:05.5 | 11.54 s |
| 11 | 10:50.3 | 11.85 s |
| 12 | 11:28.4 | 3.05 s |
| 13 | 11:33.1 | 3.08 s |
| 14 | 11:49.2 | 20.19 s |
| 15 | 13:23.8 | 3.34 s |
| 16 | 13:43.5 | 20.27 s |
| 17 | 14:56.1 | 3.68 s |
| 18 | 15:06.9 | 11.36 s |
| 19 | 15:34.4 | 20.21 s |
| 20 | 17:07.3 | 11.88 s |
| 21 | 17:33.3 | 20.24 s |
| 22 | 18:47.6 | 11.66 s |
| 23 | 19:13.9 | 20.19 s |
| 24 | 20:25.4 | 11.92 s |
| 25 | 20:52.6 | 20.21 s |
| 26 | 22:25.6 | 11.67 s |
| 27 | 22:50.9 | 20.19 s |
| 28 | 24:42.4 | 12.00 s |
| 29 | 25:25.6 | 3.84 s |
| 30 | 26:06.4 | 3.05 s |
| 31 | 27:46.1 | 3.20 s |
| 32 | 28:55.4 | 3.03 s |
| 33 | 29:02.7 | 3.06 s |
| 34 | 29:09.6 | 3.06 s |
| 35 | 29:16.5 | 7.83 s |
| 36 | 30:20.7 | 3.05 s |
| 37 | 30:26.7 | 3.09 s |
| 38 | 30:33.4 | 3.02 s |
| 39 | 30:40.2 | 8.14 s |
| 40 | 31:59.0 | 3.03 s |
| 41 | 32:05.1 | 3.04 s |
| 42 | 32:11.4 | 3.02 s |
| 43 | 32:18.3 | 8.15 s |
| 44 | 33:26.7 | 3.05 s |
| 45 | 33:33.5 | 3.03 s |
| 46 | 33:40.0 | 3.03 s |
| 47 | 33:46.5 | 7.97 s |
| 48 | 34:59.0 | 3.06 s |
| 49 | 35:05.0 | 3.03 s |
| 50 | 35:11.2 | 3.03 s |
| 51 | 35:16.8 | 7.76 s |
| 52 | 35:48.1 | 3.05 s |
| 53 | 35:52.7 | 2.89 s |
| 54 | 36:38.9 | 3.16 s |
| 55 | 36:43.8 | 2.74 s |
| 56 | 37:11.4 | 8.13 s |
| 57 | 37:41.8 | 7.75 s |
| 58 | 38:12.8 | 7.71 s |
| 59 | 38:46.9 | 7.67 s |
| 60 | 39:21.5 | 8.07 s |
| 61 | 39:57.0 | 7.59 s |
| 62 | 40:30.8 | 7.81 s |
| 63 | 41:02.0 | 7.62 s |
| 64 | 41:34.8 | 7.90 s |
| 65 | 42:09.4 | 7.34 s |
| 66 | 42:39.1 | 7.62 s |
| 67 | 43:13.5 | 8.25 s |
| 68 | 43:39.4 | 2.55 s |
| 69 | 44:02.1 | 3.05 s |
| 70 | 46:24.0 | 3.03 s |
| 71 | 46:29.6 | 3.03 s |
| 72 | 46:34.8 | 3.04 s |
| 73 | 46:40.2 | 7.61 s |
| 74 | 48:35.1 | 3.04 s |
| 75 | 48:41.1 | 3.05 s |
| 76 | 48:47.1 | 3.05 s |
| 77 | 48:52.5 | 7.39 s |
| 78 | 49:18.6 | 3.05 s |
| 79 | 49:23.0 | 2.86 s |
| 80 | 51:25.1 | 10.22 s |
| 81 | 51:44.8 | 12.11 s |
