# N2 12/2021 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/12. N2 12-2021/12. Nghe N2 12-2021.mp3` (sha1 `ce0aa70c385a`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 43:22.9 (43.4 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -20.1 dB | −17 to −18 dB |
| max volume | -0.9 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 35 | structural gap |
| ~8 s (5–9.5 s) | 16 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 2 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 13 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **72** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 653 gaps; median **0.76 s**, mean 1.00 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:00.0 | 3.52 s |
| 2 | 0:27.1 | 3.78 s |
| 3 | 0:32.5 | 2.89 s |
| 4 | 1:52.2 | 12.22 s |
| 5 | 2:58.4 | 4.19 s |
| 6 | 3:09.9 | 12.26 s |
| 7 | 4:55.7 | 12.21 s |
| 8 | 6:40.9 | 12.18 s |
| 9 | 8:22.1 | 14.70 s |
| 10 | 9:08.4 | 3.70 s |
| 11 | 9:13.8 | 3.20 s |
| 12 | 9:30.3 | 20.19 s |
| 13 | 10:47.7 | 12.16 s |
| 14 | 11:16.2 | 20.23 s |
| 15 | 12:44.7 | 12.24 s |
| 16 | 13:13.5 | 20.22 s |
| 17 | 14:30.3 | 12.25 s |
| 18 | 14:58.6 | 20.22 s |
| 19 | 16:24.0 | 4.21 s |
| 20 | 16:36.0 | 12.28 s |
| 21 | 17:01.1 | 20.19 s |
| 22 | 18:04.8 | 12.16 s |
| 23 | 18:30.6 | 20.20 s |
| 24 | 19:51.8 | 15.08 s |
| 25 | 20:38.1 | 3.98 s |
| 26 | 21:25.4 | 5.03 s |
| 27 | 21:32.1 | 3.33 s |
| 28 | 22:58.2 | 3.06 s |
| 29 | 23:04.3 | 3.03 s |
| 30 | 23:10.5 | 3.04 s |
| 31 | 23:17.0 | 5.14 s |
| 32 | 24:38.2 | 3.08 s |
| 33 | 24:45.1 | 3.06 s |
| 34 | 24:52.6 | 3.04 s |
| 35 | 25:00.1 | 5.17 s |
| 36 | 26:09.4 | 3.04 s |
| 37 | 26:16.1 | 3.03 s |
| 38 | 26:23.6 | 3.02 s |
| 39 | 26:30.4 | 8.25 s |
| 40 | 27:44.4 | 3.00 s |
| 41 | 27:50.1 | 3.02 s |
| 42 | 27:56.9 | 3.02 s |
| 43 | 28:02.9 | 8.16 s |
| 44 | 29:30.7 | 3.05 s |
| 45 | 29:36.3 | 3.03 s |
| 46 | 29:42.3 | 3.07 s |
| 47 | 29:48.9 | 11.35 s |
| 48 | 30:27.6 | 13.17 s |
| 49 | 30:42.5 | 2.82 s |
| 50 | 30:53.3 | 3.03 s |
| 51 | 31:09.2 | 5.23 s |
| 52 | 31:39.4 | 8.23 s |
| 53 | 32:15.1 | 8.25 s |
| 54 | 32:49.7 | 8.27 s |
| 55 | 33:24.4 | 8.22 s |
| 56 | 34:00.1 | 8.34 s |
| 57 | 34:36.0 | 8.28 s |
| 58 | 35:09.1 | 8.22 s |
| 59 | 35:43.8 | 8.18 s |
| 60 | 36:16.1 | 8.26 s |
| 61 | 36:35.1 | 3.09 s |
| 62 | 36:54.1 | 7.40 s |
| 63 | 37:13.8 | 2.64 s |
| 64 | 37:38.2 | 3.13 s |
| 65 | 37:43.0 | 2.63 s |
| 66 | 40:04.4 | 3.06 s |
| 67 | 40:11.8 | 3.04 s |
| 68 | 40:18.6 | 3.03 s |
| 69 | 40:25.4 | 12.15 s |
| 70 | 40:57.0 | 3.13 s |
| 71 | 41:01.7 | 3.40 s |
| 72 | 42:51.0 | 10.05 s |
