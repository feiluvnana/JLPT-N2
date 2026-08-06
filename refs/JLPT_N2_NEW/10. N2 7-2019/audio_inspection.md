# N2 7/2019 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/10. N2 7-2019/10. Nghe N2 7-2019.mp3` (sha1 `1b0d7fc26fe3`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 46:26.8 (46.4 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -22.9 dB | −17 to −18 dB |
| max volume | -2.1 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 38 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 4 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 9 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 5 | 問題2 option-reading time |
| **total** | **74** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 693 gaps; median **0.83 s**, mean 1.02 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:14.8 | 4.20 s |
| 2 | 0:39.5 | 2.51 s |
| 3 | 0:55.3 | 3.26 s |
| 4 | 1:22.2 | 3.80 s |
| 5 | 1:27.6 | 3.27 s |
| 6 | 2:44.7 | 12.22 s |
| 7 | 4:02.3 | 9.77 s |
| 8 | 5:30.5 | 12.24 s |
| 9 | 6:39.9 | 4.08 s |
| 10 | 6:52.6 | 12.24 s |
| 11 | 8:35.3 | 6.97 s |
| 12 | 8:42.5 | 9.82 s |
| 13 | 9:19.8 | 4.43 s |
| 14 | 9:44.8 | 20.09 s |
| 15 | 11:12.6 | 12.24 s |
| 16 | 11:38.5 | 20.10 s |
| 17 | 12:52.7 | 12.23 s |
| 18 | 13:22.1 | 20.11 s |
| 19 | 15:02.2 | 12.18 s |
| 20 | 15:34.1 | 20.06 s |
| 21 | 16:48.9 | 12.20 s |
| 22 | 17:18.2 | 20.09 s |
| 23 | 18:50.3 | 12.60 s |
| 24 | 19:03.1 | 4.69 s |
| 25 | 19:39.0 | 4.04 s |
| 26 | 20:21.3 | 3.15 s |
| 27 | 21:34.8 | 3.09 s |
| 28 | 21:40.8 | 3.07 s |
| 29 | 21:47.0 | 3.03 s |
| 30 | 21:53.6 | 8.21 s |
| 31 | 23:09.0 | 3.04 s |
| 32 | 23:16.6 | 3.05 s |
| 33 | 23:24.4 | 3.05 s |
| 34 | 23:32.2 | 8.20 s |
| 35 | 24:41.2 | 3.03 s |
| 36 | 24:47.7 | 3.06 s |
| 37 | 24:54.2 | 3.05 s |
| 38 | 25:00.7 | 8.25 s |
| 39 | 26:31.9 | 3.07 s |
| 40 | 26:38.7 | 3.03 s |
| 41 | 26:45.6 | 3.04 s |
| 42 | 26:53.2 | 8.18 s |
| 43 | 28:03.9 | 3.05 s |
| 44 | 28:10.8 | 3.05 s |
| 45 | 28:17.9 | 3.03 s |
| 46 | 28:25.2 | 8.59 s |
| 47 | 28:34.0 | 2.68 s |
| 48 | 29:00.1 | 4.06 s |
| 49 | 29:33.6 | 8.38 s |
| 50 | 30:10.0 | 8.38 s |
| 51 | 30:44.0 | 8.38 s |
| 52 | 31:18.0 | 8.39 s |
| 53 | 31:49.0 | 8.37 s |
| 54 | 32:21.7 | 8.36 s |
| 55 | 32:56.7 | 8.35 s |
| 56 | 33:32.3 | 8.34 s |
| 57 | 34:11.1 | 8.38 s |
| 58 | 34:47.0 | 8.39 s |
| 59 | 35:23.4 | 8.49 s |
| 60 | 35:32.1 | 4.10 s |
| 61 | 35:52.6 | 2.54 s |
| 62 | 36:16.3 | 3.08 s |
| 63 | 38:39.6 | 3.04 s |
| 64 | 38:45.2 | 3.07 s |
| 65 | 38:50.7 | 3.08 s |
| 66 | 38:56.5 | 8.08 s |
| 67 | 40:56.6 | 3.03 s |
| 68 | 41:02.9 | 3.03 s |
| 69 | 41:09.3 | 3.04 s |
| 70 | 41:15.6 | 9.60 s |
| 71 | 41:44.7 | 3.07 s |
| 72 | 44:00.6 | 10.22 s |
| 73 | 44:20.3 | 14.02 s |
| 74 | 44:41.0 | 2.87 s |
