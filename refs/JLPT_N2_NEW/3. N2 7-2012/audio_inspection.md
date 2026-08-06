# N2 7/2012 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/3. N2 7-2012/3. Nghe N2 7-2012.mp3` (sha1 `87e55204bed5`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 36:56.3 (36.9 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 65 kb/s | — |
| mean volume | -21.2 dB | −17 to −18 dB |
| max volume | -1.8 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 39 | structural gap |
| ~8 s (5–9.5 s) | 15 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 4 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 0 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **64** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 624 gaps; median **0.87 s**, mean 1.03 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:09.2 | 2.63 s |
| 2 | 1:27.0 | 3.97 s |
| 3 | 2:54.8 | 9.02 s |
| 4 | 4:13.3 | 10.04 s |
| 5 | 5:35.1 | 7.14 s |
| 6 | 7:07.9 | 7.33 s |
| 7 | 7:27.9 | 20.20 s |
| 8 | 8:43.4 | 11.39 s |
| 9 | 9:11.0 | 20.20 s |
| 10 | 10:24.0 | 8.35 s |
| 11 | 10:47.5 | 20.19 s |
| 12 | 11:53.5 | 9.87 s |
| 13 | 12:17.5 | 20.19 s |
| 14 | 13:46.2 | 9.30 s |
| 15 | 14:08.8 | 20.20 s |
| 16 | 15:33.4 | 8.28 s |
| 17 | 15:54.5 | 20.20 s |
| 18 | 17:27.5 | 4.20 s |
| 19 | 17:38.9 | 9.23 s |
| 20 | 18:39.8 | 3.11 s |
| 21 | 18:53.2 | 3.07 s |
| 22 | 18:58.8 | 3.14 s |
| 23 | 19:04.7 | 3.06 s |
| 24 | 19:10.2 | 3.73 s |
| 25 | 20:19.4 | 3.11 s |
| 26 | 20:26.4 | 3.19 s |
| 27 | 20:33.3 | 3.12 s |
| 28 | 20:40.3 | 7.32 s |
| 29 | 21:55.4 | 3.04 s |
| 30 | 22:01.5 | 3.05 s |
| 31 | 22:07.8 | 3.04 s |
| 32 | 22:14.5 | 5.82 s |
| 33 | 23:04.2 | 4.18 s |
| 34 | 23:22.0 | 3.04 s |
| 35 | 23:28.9 | 3.12 s |
| 36 | 23:35.1 | 3.06 s |
| 37 | 23:41.2 | 6.57 s |
| 38 | 23:57.6 | 2.53 s |
| 39 | 24:40.5 | 3.12 s |
| 40 | 24:57.0 | 3.12 s |
| 41 | 25:02.7 | 3.20 s |
| 42 | 25:08.8 | 3.03 s |
| 43 | 25:14.6 | 6.69 s |
| 44 | 25:48.4 | 4.49 s |
| 45 | 26:16.6 | 5.61 s |
| 46 | 26:47.9 | 3.35 s |
| 47 | 27:13.7 | 2.66 s |
| 48 | 27:39.7 | 3.57 s |
| 49 | 28:10.6 | 4.13 s |
| 50 | 28:38.8 | 3.80 s |
| 51 | 29:06.4 | 2.65 s |
| 52 | 29:35.5 | 3.09 s |
| 53 | 30:05.5 | 4.29 s |
| 54 | 30:34.2 | 3.63 s |
| 55 | 32:10.2 | 3.05 s |
| 56 | 32:15.1 | 3.06 s |
| 57 | 32:20.1 | 3.03 s |
| 58 | 32:25.1 | 6.40 s |
| 59 | 34:21.0 | 3.05 s |
| 60 | 34:27.5 | 3.07 s |
| 61 | 34:33.2 | 3.03 s |
| 62 | 34:38.4 | 5.73 s |
| 63 | 36:31.0 | 5.57 s |
| 64 | 36:46.0 | 9.96 s |
