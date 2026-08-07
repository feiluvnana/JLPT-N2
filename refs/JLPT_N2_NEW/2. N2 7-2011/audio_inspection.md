# N2 7/2011 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/2. N2 7-2011/2. Nghe N2 7-2011.mp3` (sha1 `b7b360f13f68`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 40:56.7 (40.9 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 71 kb/s | — |
| mean volume | -20.7 dB | −17 to −18 dB |
| max volume | 0.0 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 28 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **65** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 698 gaps; median **0.79 s**, mean 0.99 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:09.5 | 3.25 s |
| 2 | 1:13.0 | 12.22 s |
| 3 | 2:44.0 | 12.23 s |
| 4 | 4:06.5 | 12.22 s |
| 5 | 5:43.2 | 12.25 s |
| 6 | 7:07.6 | 12.23 s |
| 7 | 7:42.3 | 20.22 s |
| 8 | 8:57.0 | 12.21 s |
| 9 | 9:24.7 | 20.26 s |
| 10 | 11:00.7 | 12.32 s |
| 11 | 11:27.0 | 20.17 s |
| 12 | 12:47.4 | 12.22 s |
| 13 | 13:13.7 | 20.24 s |
| 14 | 14:31.9 | 12.17 s |
| 15 | 14:58.5 | 20.22 s |
| 16 | 16:24.8 | 12.20 s |
| 17 | 16:50.9 | 20.22 s |
| 18 | 18:16.8 | 12.23 s |
| 19 | 19:00.6 | 3.84 s |
| 20 | 19:13.7 | 2.64 s |
| 21 | 20:17.5 | 3.06 s |
| 22 | 20:23.0 | 3.10 s |
| 23 | 20:29.2 | 3.05 s |
| 24 | 20:35.8 | 8.20 s |
| 25 | 21:44.2 | 3.09 s |
| 26 | 21:50.2 | 3.10 s |
| 27 | 21:56.4 | 3.09 s |
| 28 | 22:02.7 | 8.24 s |
| 29 | 23:36.3 | 3.09 s |
| 30 | 23:42.9 | 3.11 s |
| 31 | 23:49.5 | 3.04 s |
| 32 | 23:55.7 | 8.20 s |
| 33 | 25:02.1 | 3.08 s |
| 34 | 25:09.3 | 3.08 s |
| 35 | 25:16.5 | 3.07 s |
| 36 | 25:24.0 | 8.23 s |
| 37 | 27:01.8 | 3.08 s |
| 38 | 27:09.8 | 3.11 s |
| 39 | 27:17.6 | 3.10 s |
| 40 | 27:25.0 | 8.40 s |
| 41 | 27:38.3 | 2.97 s |
| 42 | 28:06.1 | 8.24 s |
| 43 | 28:37.1 | 8.21 s |
| 44 | 29:08.9 | 8.23 s |
| 45 | 29:40.3 | 8.28 s |
| 46 | 30:12.0 | 8.23 s |
| 47 | 30:45.7 | 8.23 s |
| 48 | 31:18.9 | 8.42 s |
| 49 | 31:52.6 | 8.20 s |
| 50 | 32:25.3 | 8.23 s |
| 51 | 32:59.2 | 8.25 s |
| 52 | 33:31.7 | 7.81 s |
| 53 | 35:06.3 | 3.59 s |
| 54 | 35:22.6 | 3.09 s |
| 55 | 35:28.3 | 3.09 s |
| 56 | 35:34.3 | 3.08 s |
| 57 | 35:40.2 | 8.19 s |
| 58 | 37:25.7 | 3.08 s |
| 59 | 37:33.1 | 3.11 s |
| 60 | 37:41.0 | 3.10 s |
| 61 | 37:48.6 | 8.25 s |
| 62 | 38:17.2 | 3.07 s |
| 63 | 38:22.0 | 3.26 s |
| 64 | 40:26.6 | 10.23 s |
| 65 | 40:46.8 | 9.97 s |
