# N2 7/2014 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/5. N2 7-2014/5. Nghe N2 7-2014.mp3` (sha1 `a6e1106eff88`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 41:13.1 (41.2 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 80 kb/s | — |
| mean volume | -19.6 dB | −17 to −18 dB |
| max volume | -1.3 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 28 | structural gap |
| ~8 s (5–9.5 s) | 18 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 13 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **66** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 597 gaps; median **0.82 s**, mean 1.01 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:17.9 | 12.16 s |
| 2 | 2:50.8 | 4.19 s |
| 3 | 3:01.9 | 12.29 s |
| 4 | 4:18.7 | 12.13 s |
| 5 | 5:33.7 | 12.17 s |
| 6 | 6:56.4 | 12.15 s |
| 7 | 7:23.2 | 20.20 s |
| 8 | 8:36.3 | 12.13 s |
| 9 | 9:06.3 | 20.18 s |
| 10 | 10:12.3 | 12.17 s |
| 11 | 10:38.5 | 20.22 s |
| 12 | 12:06.7 | 12.15 s |
| 13 | 12:33.4 | 20.23 s |
| 14 | 13:51.4 | 4.19 s |
| 15 | 14:03.8 | 12.17 s |
| 16 | 14:29.9 | 20.19 s |
| 17 | 15:38.2 | 12.17 s |
| 18 | 16:05.2 | 20.21 s |
| 19 | 16:27.6 | 3.02 s |
| 20 | 17:35.6 | 3.00 s |
| 21 | 17:46.6 | 12.14 s |
| 22 | 18:57.1 | 3.09 s |
| 23 | 19:04.6 | 3.09 s |
| 24 | 19:11.9 | 3.06 s |
| 25 | 19:19.6 | 8.18 s |
| 26 | 20:28.7 | 3.12 s |
| 27 | 20:44.1 | 3.08 s |
| 28 | 20:51.2 | 3.10 s |
| 29 | 20:57.4 | 3.05 s |
| 30 | 21:04.6 | 8.18 s |
| 31 | 22:00.5 | 2.73 s |
| 32 | 22:13.1 | 3.12 s |
| 33 | 22:19.6 | 3.17 s |
| 34 | 22:26.4 | 3.06 s |
| 35 | 22:32.8 | 8.18 s |
| 36 | 23:46.7 | 3.09 s |
| 37 | 23:53.1 | 3.15 s |
| 38 | 24:00.6 | 3.10 s |
| 39 | 24:08.3 | 8.22 s |
| 40 | 26:01.2 | 3.06 s |
| 41 | 26:07.4 | 3.12 s |
| 42 | 26:13.5 | 3.11 s |
| 43 | 26:20.0 | 8.21 s |
| 44 | 26:55.6 | 8.13 s |
| 45 | 27:26.2 | 8.28 s |
| 46 | 27:57.0 | 8.26 s |
| 47 | 28:29.6 | 8.20 s |
| 48 | 29:02.8 | 8.24 s |
| 49 | 29:36.1 | 8.25 s |
| 50 | 30:10.1 | 8.26 s |
| 51 | 30:43.7 | 8.28 s |
| 52 | 31:18.3 | 8.16 s |
| 53 | 31:55.0 | 8.16 s |
| 54 | 32:28.7 | 8.19 s |
| 55 | 33:04.3 | 8.24 s |
| 56 | 35:18.4 | 3.07 s |
| 57 | 35:24.4 | 3.14 s |
| 58 | 35:30.3 | 3.17 s |
| 59 | 35:36.4 | 7.07 s |
| 60 | 37:55.9 | 3.09 s |
| 61 | 38:03.8 | 3.08 s |
| 62 | 38:10.8 | 3.05 s |
| 63 | 38:17.0 | 11.90 s |
| 64 | 40:22.8 | 3.67 s |
| 65 | 40:36.9 | 10.21 s |
| 66 | 40:58.2 | 11.74 s |
