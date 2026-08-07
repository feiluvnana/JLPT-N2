# N2 7/2015 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/6. N2 7-2015/6. Nghe N2 7-2015.mp3` (sha1 `e50c5203fe20`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 41:50.8 (41.8 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 79 kb/s | — |
| mean volume | -15.3 dB | −17 to −18 dB |
| max volume | 0.0 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 25 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 12 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **64** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 557 gaps; median **0.89 s**, mean 1.02 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:33.9 | 12.21 s |
| 2 | 3:05.8 | 12.32 s |
| 3 | 4:35.9 | 2.91 s |
| 4 | 4:47.5 | 12.22 s |
| 5 | 6:06.7 | 12.24 s |
| 6 | 7:20.8 | 12.21 s |
| 7 | 7:47.4 | 20.18 s |
| 8 | 8:48.2 | 3.30 s |
| 9 | 8:57.9 | 12.25 s |
| 10 | 9:23.6 | 20.20 s |
| 11 | 10:41.7 | 12.22 s |
| 12 | 11:08.8 | 20.18 s |
| 13 | 12:39.3 | 12.17 s |
| 14 | 13:07.0 | 20.17 s |
| 15 | 14:37.9 | 12.26 s |
| 16 | 15:06.5 | 20.19 s |
| 17 | 16:55.4 | 12.22 s |
| 18 | 17:23.3 | 20.17 s |
| 19 | 18:41.7 | 2.99 s |
| 20 | 18:53.4 | 12.39 s |
| 21 | 19:55.5 | 4.20 s |
| 22 | 20:12.3 | 3.05 s |
| 23 | 20:18.6 | 3.04 s |
| 24 | 20:25.3 | 3.03 s |
| 25 | 20:31.5 | 8.20 s |
| 26 | 21:49.3 | 3.01 s |
| 27 | 21:55.8 | 3.04 s |
| 28 | 22:03.2 | 3.01 s |
| 29 | 22:10.2 | 8.20 s |
| 30 | 23:24.7 | 3.04 s |
| 31 | 23:31.6 | 3.06 s |
| 32 | 23:39.5 | 3.03 s |
| 33 | 23:47.4 | 8.21 s |
| 34 | 25:11.0 | 3.01 s |
| 35 | 25:17.9 | 3.04 s |
| 36 | 25:24.9 | 3.02 s |
| 37 | 25:31.1 | 8.19 s |
| 38 | 26:41.7 | 3.07 s |
| 39 | 26:47.4 | 3.05 s |
| 40 | 26:53.5 | 3.01 s |
| 41 | 26:59.0 | 8.21 s |
| 42 | 27:30.9 | 8.22 s |
| 43 | 28:05.4 | 8.22 s |
| 44 | 28:39.0 | 8.21 s |
| 45 | 29:13.0 | 8.27 s |
| 46 | 29:46.2 | 8.23 s |
| 47 | 30:18.7 | 8.22 s |
| 48 | 30:52.9 | 8.28 s |
| 49 | 31:28.4 | 8.24 s |
| 50 | 32:05.1 | 8.24 s |
| 51 | 32:40.4 | 8.23 s |
| 52 | 33:15.9 | 8.26 s |
| 53 | 33:49.1 | 8.25 s |
| 54 | 36:05.3 | 3.06 s |
| 55 | 36:10.6 | 3.08 s |
| 56 | 36:16.2 | 3.07 s |
| 57 | 36:21.4 | 8.26 s |
| 58 | 38:13.8 | 3.05 s |
| 59 | 38:20.1 | 3.05 s |
| 60 | 38:26.0 | 3.04 s |
| 61 | 38:32.5 | 8.28 s |
| 62 | 40:49.6 | 10.17 s |
| 63 | 41:10.1 | 17.08 s |
| 64 | 41:37.4 | 13.35 s |
