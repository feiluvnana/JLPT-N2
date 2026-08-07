# N2 12/2019 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/10. N2 12-2019/10. Nghe N2 12-2019.mp3` (sha1 `d59649223514`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 41:08.5 (41.1 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -23.3 dB | −17 to −18 dB |
| max volume | -3.3 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 27 | structural gap |
| ~8 s (5–9.5 s) | 17 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 3 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 10 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **64** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 639 gaps; median **0.85 s**, mean 1.02 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:34.5 | 2.62 s |
| 2 | 1:56.4 | 12.30 s |
| 3 | 3:20.1 | 4.22 s |
| 4 | 3:32.3 | 12.33 s |
| 5 | 5:01.1 | 12.40 s |
| 6 | 6:41.0 | 12.29 s |
| 7 | 8:29.3 | 12.33 s |
| 8 | 8:58.9 | 20.22 s |
| 9 | 10:17.2 | 4.22 s |
| 10 | 10:30.4 | 12.35 s |
| 11 | 10:58.7 | 20.22 s |
| 12 | 12:27.6 | 12.29 s |
| 13 | 12:57.1 | 20.23 s |
| 14 | 14:27.1 | 12.32 s |
| 15 | 14:54.8 | 20.24 s |
| 16 | 16:05.0 | 4.20 s |
| 17 | 16:18.9 | 12.29 s |
| 18 | 16:45.5 | 20.21 s |
| 19 | 18:00.5 | 12.32 s |
| 20 | 19:16.7 | 4.20 s |
| 21 | 19:33.6 | 3.05 s |
| 22 | 19:40.6 | 3.10 s |
| 23 | 19:47.9 | 3.06 s |
| 24 | 19:54.4 | 8.30 s |
| 25 | 20:10.4 | 6.07 s |
| 26 | 20:53.1 | 4.20 s |
| 27 | 21:09.1 | 3.04 s |
| 28 | 21:15.3 | 3.05 s |
| 29 | 21:21.9 | 3.08 s |
| 30 | 21:28.5 | 8.30 s |
| 31 | 22:36.0 | 3.11 s |
| 32 | 22:42.5 | 3.03 s |
| 33 | 22:49.1 | 3.06 s |
| 34 | 22:55.4 | 8.30 s |
| 35 | 24:04.8 | 3.06 s |
| 36 | 24:12.1 | 3.09 s |
| 37 | 24:20.1 | 3.10 s |
| 38 | 24:28.0 | 8.29 s |
| 39 | 25:41.3 | 3.06 s |
| 40 | 25:47.5 | 3.08 s |
| 41 | 25:53.9 | 3.04 s |
| 42 | 26:00.2 | 11.30 s |
| 43 | 26:35.5 | 8.34 s |
| 44 | 27:07.1 | 8.30 s |
| 45 | 27:39.8 | 8.31 s |
| 46 | 28:11.6 | 8.37 s |
| 47 | 28:45.0 | 8.33 s |
| 48 | 29:16.9 | 8.28 s |
| 49 | 29:52.7 | 8.32 s |
| 50 | 30:26.9 | 8.34 s |
| 51 | 31:00.5 | 8.28 s |
| 52 | 31:33.4 | 8.35 s |
| 53 | 32:06.7 | 11.00 s |
| 54 | 34:49.1 | 3.03 s |
| 55 | 34:54.4 | 3.03 s |
| 56 | 35:00.2 | 3.03 s |
| 57 | 35:05.5 | 8.32 s |
| 58 | 37:16.3 | 3.06 s |
| 59 | 37:22.7 | 3.04 s |
| 60 | 37:29.4 | 3.08 s |
| 61 | 37:36.6 | 8.33 s |
| 62 | 39:52.9 | 10.22 s |
| 63 | 40:13.3 | 19.50 s |
| 64 | 40:39.0 | 29.54 s |
