# N2 12/2018 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/9. N2 12-2018/9. Nghe N2 12-2018.mp3` (sha1 `9b75f496cb53`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 39:29.1 (39.5 min) | ~50–52 min |
| codec / sample rate / channels | mjpeg / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -19.2 dB | −17 to −18 dB |
| max volume | -0.0 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 23 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 10 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 5 | 問題2 option-reading time |
| **total** | **58** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 540 gaps; median **0.85 s**, mean 1.04 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:17.5 | 11.85 s |
| 2 | 2:40.4 | 11.89 s |
| 3 | 4:28.6 | 11.85 s |
| 4 | 5:59.6 | 4.22 s |
| 5 | 6:12.5 | 11.88 s |
| 6 | 7:54.0 | 11.88 s |
| 7 | 8:24.4 | 20.21 s |
| 8 | 9:44.7 | 4.19 s |
| 9 | 9:58.4 | 11.86 s |
| 10 | 10:27.9 | 20.23 s |
| 11 | 11:55.6 | 11.80 s |
| 12 | 12:21.0 | 20.20 s |
| 13 | 13:56.7 | 11.78 s |
| 14 | 14:24.3 | 20.25 s |
| 15 | 15:33.0 | 11.94 s |
| 16 | 15:58.4 | 20.18 s |
| 17 | 17:24.5 | 11.83 s |
| 18 | 18:46.4 | 3.07 s |
| 19 | 18:54.2 | 3.06 s |
| 20 | 19:00.7 | 3.07 s |
| 21 | 19:07.3 | 7.89 s |
| 22 | 20:31.8 | 3.06 s |
| 23 | 20:38.7 | 3.07 s |
| 24 | 20:45.9 | 3.05 s |
| 25 | 20:52.7 | 7.83 s |
| 26 | 21:59.4 | 3.07 s |
| 27 | 22:06.2 | 3.13 s |
| 28 | 22:13.2 | 3.12 s |
| 29 | 22:19.6 | 7.88 s |
| 30 | 23:30.8 | 3.04 s |
| 31 | 23:37.3 | 3.06 s |
| 32 | 23:44.5 | 3.11 s |
| 33 | 23:52.3 | 7.89 s |
| 34 | 25:02.7 | 3.06 s |
| 35 | 25:08.0 | 3.09 s |
| 36 | 25:14.2 | 3.09 s |
| 37 | 25:20.2 | 7.87 s |
| 38 | 25:50.9 | 8.03 s |
| 39 | 26:21.6 | 7.97 s |
| 40 | 26:53.4 | 7.99 s |
| 41 | 27:23.5 | 7.95 s |
| 42 | 27:56.2 | 8.05 s |
| 43 | 28:29.9 | 8.03 s |
| 44 | 29:02.6 | 7.95 s |
| 45 | 29:34.9 | 8.00 s |
| 46 | 30:06.8 | 8.08 s |
| 47 | 30:43.2 | 7.99 s |
| 48 | 31:18.2 | 8.00 s |
| 49 | 33:28.8 | 3.03 s |
| 50 | 33:34.1 | 3.04 s |
| 51 | 33:39.6 | 3.03 s |
| 52 | 33:44.8 | 7.75 s |
| 53 | 36:11.0 | 3.01 s |
| 54 | 36:18.3 | 3.02 s |
| 55 | 36:25.8 | 3.04 s |
| 56 | 36:33.3 | 7.70 s |
| 57 | 38:57.7 | 10.18 s |
| 58 | 39:17.6 | 11.45 s |
