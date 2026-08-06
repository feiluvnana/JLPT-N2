# N2 12/2020 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/11. N2 12-2020/11.Nghe N2 12-2020.mp3` (sha1 `2b7aa67adcef`)
> Measured per `.agents/official-audio-analysis/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 38:09.3 (38.2 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 48000 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -18.9 dB | −17 to −18 dB |
| max volume | -0.2 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 22 | structural gap |
| ~8 s (5–9.5 s) | 17 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 0 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 11 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **56** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 532 gaps; median **0.82 s**, mean 1.03 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:03.7 | 2.96 s |
| 2 | 1:04.2 | 3.10 s |
| 3 | 1:14.9 | 12.57 s |
| 4 | 3:03.1 | 12.56 s |
| 5 | 4:29.3 | 3.03 s |
| 6 | 4:43.2 | 12.44 s |
| 7 | 6:09.6 | 12.45 s |
| 8 | 7:23.8 | 12.49 s |
| 9 | 7:52.4 | 20.20 s |
| 10 | 9:19.7 | 12.48 s |
| 11 | 9:49.0 | 20.26 s |
| 12 | 11:05.3 | 12.41 s |
| 13 | 11:32.1 | 20.18 s |
| 14 | 12:55.1 | 12.43 s |
| 15 | 13:23.5 | 20.17 s |
| 16 | 14:53.7 | 12.42 s |
| 17 | 15:20.1 | 20.20 s |
| 18 | 16:28.5 | 12.33 s |
| 19 | 16:55.5 | 20.23 s |
| 20 | 18:31.5 | 12.42 s |
| 21 | 19:48.7 | 3.02 s |
| 22 | 19:57.0 | 3.02 s |
| 23 | 20:04.6 | 3.02 s |
| 24 | 20:11.1 | 8.39 s |
| 25 | 21:37.1 | 3.06 s |
| 26 | 21:43.7 | 3.03 s |
| 27 | 21:49.9 | 3.05 s |
| 28 | 21:56.9 | 8.39 s |
| 29 | 23:09.9 | 3.06 s |
| 30 | 23:16.5 | 3.08 s |
| 31 | 23:22.9 | 3.04 s |
| 32 | 23:30.1 | 8.30 s |
| 33 | 24:59.7 | 3.23 s |
| 34 | 25:15.7 | 3.06 s |
| 35 | 25:22.1 | 3.08 s |
| 36 | 25:28.9 | 3.05 s |
| 37 | 25:35.4 | 8.34 s |
| 38 | 26:47.3 | 3.01 s |
| 39 | 26:53.9 | 3.03 s |
| 40 | 26:59.9 | 3.02 s |
| 41 | 27:06.0 | 8.35 s |
| 42 | 27:38.4 | 8.37 s |
| 43 | 28:11.8 | 8.40 s |
| 44 | 28:47.3 | 8.43 s |
| 45 | 29:19.1 | 8.35 s |
| 46 | 29:51.0 | 8.36 s |
| 47 | 30:26.3 | 8.39 s |
| 48 | 31:02.8 | 8.35 s |
| 49 | 31:36.6 | 8.27 s |
| 50 | 32:10.9 | 8.43 s |
| 51 | 32:45.4 | 8.41 s |
| 52 | 33:21.1 | 8.41 s |
| 53 | 34:56.6 | 3.02 s |
| 54 | 35:02.1 | 3.02 s |
| 55 | 35:08.9 | 3.02 s |
| 56 | 35:15.2 | 8.48 s |
