# N2 12/2022 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/13. N2 12-2022/13. Nghe N2 T12-2022.mp3` (sha1 `eab55f4ed33b`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 45:05.4 (45.1 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 192 kb/s | — |
| mean volume | -19.2 dB | −17 to −18 dB |
| max volume | -0.5 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 30 | structural gap |
| ~8 s (5–9.5 s) | 17 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 3 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 10 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **67** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 675 gaps; median **0.87 s**, mean 1.04 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:19.5 | 3.11 s |
| 2 | 0:35.5 | 4.19 s |
| 3 | 1:00.3 | 2.88 s |
| 4 | 1:16.1 | 3.24 s |
| 5 | 1:42.9 | 3.78 s |
| 6 | 3:17.8 | 12.03 s |
| 7 | 4:40.5 | 12.33 s |
| 8 | 6:25.8 | 5.48 s |
| 9 | 7:54.8 | 12.30 s |
| 10 | 9:39.0 | 17.70 s |
| 11 | 10:28.3 | 3.70 s |
| 12 | 10:33.6 | 3.13 s |
| 13 | 10:55.5 | 20.26 s |
| 14 | 12:11.5 | 3.05 s |
| 15 | 12:23.4 | 12.30 s |
| 16 | 12:53.3 | 20.20 s |
| 17 | 14:11.4 | 12.30 s |
| 18 | 14:40.4 | 20.19 s |
| 19 | 16:05.5 | 3.13 s |
| 20 | 16:18.2 | 12.24 s |
| 21 | 16:44.8 | 20.22 s |
| 22 | 18:03.5 | 12.36 s |
| 23 | 18:34.1 | 20.19 s |
| 24 | 20:16.8 | 12.27 s |
| 25 | 20:45.9 | 20.19 s |
| 26 | 22:40.1 | 14.84 s |
| 27 | 23:26.5 | 3.64 s |
| 28 | 24:13.5 | 5.02 s |
| 29 | 25:33.4 | 3.06 s |
| 30 | 25:39.8 | 3.05 s |
| 31 | 25:46.7 | 3.05 s |
| 32 | 25:52.9 | 8.25 s |
| 33 | 27:12.3 | 3.04 s |
| 34 | 27:19.6 | 3.02 s |
| 35 | 27:26.6 | 3.03 s |
| 36 | 27:32.9 | 8.22 s |
| 37 | 28:49.9 | 3.02 s |
| 38 | 28:56.6 | 3.03 s |
| 39 | 29:03.6 | 3.03 s |
| 40 | 29:09.5 | 8.29 s |
| 41 | 30:24.8 | 3.01 s |
| 42 | 30:32.6 | 3.02 s |
| 43 | 30:40.0 | 3.04 s |
| 44 | 30:47.0 | 8.31 s |
| 45 | 32:12.0 | 3.03 s |
| 46 | 32:18.9 | 3.03 s |
| 47 | 32:25.7 | 3.03 s |
| 48 | 32:32.7 | 10.89 s |
| 49 | 33:11.0 | 9.86 s |
| 50 | 33:47.4 | 8.24 s |
| 51 | 34:20.9 | 8.27 s |
| 52 | 34:56.7 | 8.28 s |
| 53 | 35:31.9 | 8.31 s |
| 54 | 36:05.8 | 8.26 s |
| 55 | 36:38.8 | 5.72 s |
| 56 | 37:11.8 | 8.29 s |
| 57 | 37:48.1 | 8.25 s |
| 58 | 38:23.7 | 8.24 s |
| 59 | 38:56.6 | 8.32 s |
| 60 | 39:32.1 | 11.79 s |
| 61 | 39:56.2 | 2.64 s |
| 62 | 40:20.5 | 3.12 s |
| 63 | 42:13.5 | 3.01 s |
| 64 | 42:19.1 | 3.01 s |
| 65 | 42:25.4 | 3.02 s |
| 66 | 42:31.4 | 8.27 s |
| 67 | 44:46.3 | 10.01 s |
