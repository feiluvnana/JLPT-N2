# N2 7/2013 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/4. N2 7-2013/4. Nghe N2 7-2013.mp3` (sha1 `29e3c42ba58c`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 37:08.4 (37.1 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 74 kb/s | — |
| mean volume | -21.0 dB | −17 to −18 dB |
| max volume | -0.8 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 23 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 10 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 5 | 問題2 option-reading time |
| **total** | **59** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 541 gaps; median **0.94 s**, mean 1.06 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:00.5 | 2.94 s |
| 2 | 1:10.8 | 12.58 s |
| 3 | 2:15.4 | 2.55 s |
| 4 | 2:24.5 | 12.62 s |
| 5 | 3:35.0 | 12.64 s |
| 6 | 5:12.6 | 12.61 s |
| 7 | 6:56.2 | 12.61 s |
| 8 | 7:22.4 | 20.20 s |
| 9 | 8:43.6 | 12.60 s |
| 10 | 9:11.4 | 20.20 s |
| 11 | 10:37.2 | 12.57 s |
| 12 | 11:03.5 | 20.20 s |
| 13 | 12:40.7 | 12.60 s |
| 14 | 13:08.5 | 20.23 s |
| 15 | 14:12.1 | 12.60 s |
| 16 | 14:40.8 | 20.18 s |
| 17 | 16:07.6 | 12.60 s |
| 18 | 17:09.7 | 3.07 s |
| 19 | 17:15.8 | 3.07 s |
| 20 | 17:21.6 | 3.06 s |
| 21 | 17:27.7 | 8.66 s |
| 22 | 18:42.0 | 3.05 s |
| 23 | 18:48.6 | 3.08 s |
| 24 | 18:55.8 | 3.07 s |
| 25 | 19:03.2 | 8.62 s |
| 26 | 20:14.7 | 3.06 s |
| 27 | 20:20.7 | 3.08 s |
| 28 | 20:27.5 | 3.09 s |
| 29 | 20:34.5 | 8.56 s |
| 30 | 21:55.6 | 3.05 s |
| 31 | 22:02.5 | 3.11 s |
| 32 | 22:09.2 | 3.04 s |
| 33 | 22:16.1 | 8.67 s |
| 34 | 23:38.7 | 3.05 s |
| 35 | 23:44.1 | 3.07 s |
| 36 | 23:50.3 | 3.05 s |
| 37 | 23:56.4 | 8.60 s |
| 38 | 24:28.1 | 8.58 s |
| 39 | 25:03.3 | 8.58 s |
| 40 | 25:38.0 | 8.61 s |
| 41 | 26:11.7 | 8.60 s |
| 42 | 26:43.9 | 8.61 s |
| 43 | 27:16.1 | 8.64 s |
| 44 | 27:49.7 | 8.56 s |
| 45 | 28:22.4 | 8.64 s |
| 46 | 28:58.9 | 8.64 s |
| 47 | 29:34.1 | 8.58 s |
| 48 | 30:07.0 | 8.62 s |
| 49 | 30:42.7 | 8.59 s |
| 50 | 32:37.6 | 3.05 s |
| 51 | 32:42.8 | 3.06 s |
| 52 | 32:48.1 | 3.07 s |
| 53 | 32:53.6 | 8.61 s |
| 54 | 34:32.3 | 3.05 s |
| 55 | 34:37.8 | 3.07 s |
| 56 | 34:43.3 | 3.04 s |
| 57 | 34:49.3 | 8.62 s |
| 58 | 36:37.3 | 10.21 s |
| 59 | 36:57.2 | 10.45 s |
