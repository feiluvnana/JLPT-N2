# N2 7/2016 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/7. N2 7-2016/7. Nghe N2 7-2016.mp3` (sha1 `5b5f990940ed`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 42:28.7 (42.5 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 32000 Hz / 2 | — |
| bit rate | 73 kb/s | — |
| mean volume | -18.7 dB | −17 to −18 dB |
| max volume | -2.2 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 22 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 0 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **58** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 576 gaps; median **0.89 s**, mean 1.04 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:25.1 | 12.22 s |
| 2 | 2:41.4 | 12.21 s |
| 3 | 4:26.7 | 12.22 s |
| 4 | 6:20.7 | 12.24 s |
| 5 | 8:05.8 | 12.19 s |
| 6 | 8:31.9 | 20.19 s |
| 7 | 10:03.6 | 12.20 s |
| 8 | 10:29.2 | 20.19 s |
| 9 | 11:55.4 | 12.25 s |
| 10 | 12:24.0 | 20.19 s |
| 11 | 13:50.8 | 12.30 s |
| 12 | 14:19.6 | 20.22 s |
| 13 | 16:05.5 | 12.22 s |
| 14 | 16:35.6 | 20.21 s |
| 15 | 17:53.5 | 12.24 s |
| 16 | 18:21.0 | 20.20 s |
| 17 | 19:28.2 | 12.24 s |
| 18 | 20:42.7 | 3.02 s |
| 19 | 20:49.7 | 3.03 s |
| 20 | 20:56.1 | 3.03 s |
| 21 | 21:02.5 | 8.26 s |
| 22 | 22:13.3 | 3.03 s |
| 23 | 22:20.3 | 3.04 s |
| 24 | 22:27.4 | 3.03 s |
| 25 | 22:34.5 | 8.24 s |
| 26 | 23:48.2 | 3.03 s |
| 27 | 23:55.3 | 3.03 s |
| 28 | 24:01.8 | 3.04 s |
| 29 | 24:08.7 | 8.21 s |
| 30 | 25:31.0 | 3.03 s |
| 31 | 25:36.9 | 3.05 s |
| 32 | 25:43.5 | 3.08 s |
| 33 | 25:50.4 | 8.30 s |
| 34 | 27:08.3 | 3.03 s |
| 35 | 27:15.2 | 3.05 s |
| 36 | 27:22.0 | 3.03 s |
| 37 | 27:29.1 | 8.22 s |
| 38 | 27:59.4 | 8.25 s |
| 39 | 28:35.1 | 8.24 s |
| 40 | 29:09.8 | 8.22 s |
| 41 | 29:43.3 | 8.20 s |
| 42 | 30:22.5 | 8.24 s |
| 43 | 30:55.2 | 8.26 s |
| 44 | 31:31.9 | 8.28 s |
| 45 | 32:04.7 | 8.26 s |
| 46 | 32:40.1 | 8.26 s |
| 47 | 33:15.1 | 8.28 s |
| 48 | 33:49.8 | 8.22 s |
| 49 | 34:23.8 | 8.26 s |
| 50 | 37:04.0 | 3.04 s |
| 51 | 37:10.3 | 3.02 s |
| 52 | 37:16.8 | 3.03 s |
| 53 | 37:23.2 | 2.91 s |
| 54 | 39:12.8 | 3.04 s |
| 55 | 39:18.8 | 3.07 s |
| 56 | 39:25.7 | 3.05 s |
| 57 | 39:31.5 | 8.29 s |
| 58 | 42:21.0 | 7.69 s |
