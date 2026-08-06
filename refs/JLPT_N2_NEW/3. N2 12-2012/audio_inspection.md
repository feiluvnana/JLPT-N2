# N2 12/2012 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/3. N2 12-2012/3. Nghe N2 12-2012.mp3` (sha1 `5253649425b5`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 36:38.6 (36.6 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 75 kb/s | — |
| mean volume | -20.5 dB | −17 to −18 dB |
| max volume | -0.1 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 20 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **57** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 554 gaps; median **0.94 s**, mean 1.06 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:15.3 | 11.85 s |
| 2 | 2:38.5 | 12.10 s |
| 3 | 4:10.3 | 12.01 s |
| 4 | 5:17.7 | 12.11 s |
| 5 | 6:54.7 | 12.05 s |
| 6 | 7:22.9 | 20.20 s |
| 7 | 8:38.0 | 11.85 s |
| 8 | 9:04.0 | 20.22 s |
| 9 | 10:10.4 | 3.04 s |
| 10 | 10:21.7 | 12.15 s |
| 11 | 10:46.8 | 20.21 s |
| 12 | 11:49.6 | 3.19 s |
| 13 | 11:59.7 | 11.77 s |
| 14 | 12:24.9 | 20.20 s |
| 15 | 13:34.5 | 11.97 s |
| 16 | 13:59.6 | 20.19 s |
| 17 | 15:28.5 | 12.02 s |
| 18 | 15:53.9 | 20.20 s |
| 19 | 16:54.8 | 12.14 s |
| 20 | 18:10.1 | 3.05 s |
| 21 | 18:16.0 | 3.08 s |
| 22 | 18:22.6 | 3.05 s |
| 23 | 18:29.1 | 8.05 s |
| 24 | 19:45.9 | 3.07 s |
| 25 | 19:52.1 | 3.05 s |
| 26 | 19:57.8 | 3.04 s |
| 27 | 20:04.0 | 8.15 s |
| 28 | 21:13.6 | 3.06 s |
| 29 | 21:19.3 | 3.06 s |
| 30 | 21:25.6 | 3.05 s |
| 31 | 21:31.7 | 8.08 s |
| 32 | 22:45.4 | 3.08 s |
| 33 | 22:51.2 | 3.10 s |
| 34 | 22:57.8 | 3.07 s |
| 35 | 23:03.5 | 7.93 s |
| 36 | 23:34.3 | 7.88 s |
| 37 | 24:06.7 | 8.05 s |
| 38 | 24:39.0 | 8.03 s |
| 39 | 25:12.7 | 8.10 s |
| 40 | 25:45.7 | 7.98 s |
| 41 | 26:19.3 | 8.14 s |
| 42 | 26:55.0 | 7.99 s |
| 43 | 27:27.6 | 8.04 s |
| 44 | 28:02.5 | 7.98 s |
| 45 | 28:35.7 | 7.77 s |
| 46 | 29:08.6 | 7.85 s |
| 47 | 29:39.3 | 7.86 s |
| 48 | 31:37.4 | 3.05 s |
| 49 | 31:42.3 | 3.11 s |
| 50 | 31:47.8 | 3.10 s |
| 51 | 31:52.9 | 7.88 s |
| 52 | 33:59.9 | 3.05 s |
| 53 | 34:05.6 | 3.09 s |
| 54 | 34:11.3 | 3.12 s |
| 55 | 34:17.1 | 7.80 s |
| 56 | 36:08.1 | 10.22 s |
| 57 | 36:27.8 | 10.84 s |
