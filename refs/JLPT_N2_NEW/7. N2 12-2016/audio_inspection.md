# N2 12/2016 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/7. N2 12-2016/7. Nghe N2 12-2016.mp3` (sha1 `436634f886c4`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 41:25.3 (41.4 min) | ~50–52 min |
| codec / sample rate / channels | mp3 / 44100 Hz / 2 | — |
| bit rate | 82 kb/s | — |
| mean volume | -19.1 dB | −17 to −18 dB |
| max volume | -1.3 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 24 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 12 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 6 | 問題2 option-reading time |
| **total** | **62** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 524 gaps; median **0.90 s**, mean 1.05 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 1:24.7 | 12.07 s |
| 2 | 2:50.1 | 2.95 s |
| 3 | 3:00.6 | 12.14 s |
| 4 | 4:42.3 | 12.11 s |
| 5 | 6:13.8 | 12.13 s |
| 6 | 8:02.3 | 12.10 s |
| 7 | 8:28.2 | 20.20 s |
| 8 | 9:45.9 | 12.06 s |
| 9 | 10:13.1 | 20.20 s |
| 10 | 11:41.7 | 12.07 s |
| 11 | 12:07.5 | 20.19 s |
| 12 | 13:39.8 | 12.08 s |
| 13 | 14:07.2 | 20.22 s |
| 14 | 15:24.7 | 3.32 s |
| 15 | 15:35.4 | 12.06 s |
| 16 | 16:02.3 | 20.19 s |
| 17 | 17:39.6 | 12.07 s |
| 18 | 18:06.0 | 20.22 s |
| 19 | 19:16.7 | 12.09 s |
| 20 | 20:32.9 | 3.04 s |
| 21 | 20:39.0 | 3.03 s |
| 22 | 20:46.7 | 3.02 s |
| 23 | 20:52.8 | 8.08 s |
| 24 | 22:08.4 | 3.06 s |
| 25 | 22:15.9 | 3.05 s |
| 26 | 22:22.2 | 3.08 s |
| 27 | 22:29.5 | 8.10 s |
| 28 | 23:44.3 | 3.11 s |
| 29 | 23:51.0 | 3.09 s |
| 30 | 23:58.3 | 3.03 s |
| 31 | 24:05.5 | 8.03 s |
| 32 | 25:00.7 | 3.59 s |
| 33 | 25:18.0 | 3.02 s |
| 34 | 25:23.9 | 3.02 s |
| 35 | 25:30.2 | 3.02 s |
| 36 | 25:36.1 | 8.06 s |
| 37 | 26:50.7 | 3.02 s |
| 38 | 26:58.0 | 3.05 s |
| 39 | 27:04.4 | 3.08 s |
| 40 | 27:10.9 | 8.06 s |
| 41 | 27:44.3 | 8.10 s |
| 42 | 28:18.5 | 8.09 s |
| 43 | 28:53.1 | 8.14 s |
| 44 | 29:25.9 | 8.12 s |
| 45 | 29:57.8 | 8.10 s |
| 46 | 30:32.4 | 8.12 s |
| 47 | 31:05.8 | 8.09 s |
| 48 | 31:39.1 | 8.12 s |
| 49 | 32:13.5 | 8.14 s |
| 50 | 32:46.6 | 8.11 s |
| 51 | 33:20.7 | 8.08 s |
| 52 | 33:54.8 | 8.13 s |
| 53 | 36:01.9 | 3.03 s |
| 54 | 36:07.3 | 3.02 s |
| 55 | 36:12.4 | 3.05 s |
| 56 | 36:17.5 | 8.07 s |
| 57 | 38:20.8 | 3.02 s |
| 58 | 38:26.9 | 3.02 s |
| 59 | 38:32.3 | 3.12 s |
| 60 | 38:38.5 | 8.13 s |
| 61 | 40:52.3 | 13.10 s |
| 62 | 41:14.0 | 11.31 s |
