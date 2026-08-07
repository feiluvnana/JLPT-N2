# N2 12/2023 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/14. N2 12-2023/14. Nghe N2 T12-2023.mp3` (sha1 `f3c5d842eb0c`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 48:56.1 (48.9 min) | ~50–52 min |
| codec / sample rate / channels | png / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -19.2 dB | −17 to −18 dB |
| max volume | -0.8 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 31 | structural gap |
| ~8 s (5–9.5 s) | 27 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 3 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 0 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **68** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 825 gaps; median **0.78 s**, mean 1.01 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:11.1 | 3.07 s |
| 2 | 1:25.4 | 3.05 s |
| 3 | 2:55.4 | 3.28 s |
| 4 | 4:24.6 | 9.13 s |
| 5 | 5:54.3 | 9.13 s |
| 6 | 7:22.8 | 9.14 s |
| 7 | 8:56.1 | 9.12 s |
| 8 | 10:32.1 | 9.53 s |
| 9 | 11:07.9 | 3.05 s |
| 10 | 11:25.8 | 20.19 s |
| 11 | 13:00.4 | 3.34 s |
| 12 | 13:26.1 | 20.19 s |
| 13 | 14:50.8 | 9.16 s |
| 14 | 15:13.8 | 20.18 s |
| 15 | 16:46.2 | 9.20 s |
| 16 | 17:11.3 | 20.18 s |
| 17 | 18:22.8 | 9.12 s |
| 18 | 18:51.0 | 20.20 s |
| 19 | 20:23.0 | 9.11 s |
| 20 | 20:48.3 | 20.18 s |
| 21 | 22:37.5 | 9.15 s |
| 22 | 23:03.9 | 20.18 s |
| 23 | 24:26.4 | 9.54 s |
| 24 | 25:07.2 | 3.84 s |
| 25 | 25:45.9 | 3.06 s |
| 26 | 27:23.7 | 3.21 s |
| 27 | 28:32.4 | 3.02 s |
| 28 | 28:38.9 | 3.03 s |
| 29 | 28:45.7 | 3.03 s |
| 30 | 28:53.1 | 5.20 s |
| 31 | 30:16.8 | 3.01 s |
| 32 | 30:23.6 | 3.05 s |
| 33 | 30:30.0 | 3.08 s |
| 34 | 30:37.1 | 5.16 s |
| 35 | 31:57.7 | 3.01 s |
| 36 | 32:04.9 | 3.03 s |
| 37 | 32:11.5 | 3.02 s |
| 38 | 32:18.4 | 5.17 s |
| 39 | 33:30.5 | 3.04 s |
| 40 | 33:37.2 | 3.01 s |
| 41 | 33:44.3 | 3.02 s |
| 42 | 33:51.1 | 5.15 s |
| 43 | 35:09.8 | 3.03 s |
| 44 | 35:16.3 | 3.05 s |
| 45 | 35:23.5 | 3.03 s |
| 46 | 35:31.0 | 5.56 s |
| 47 | 36:00.2 | 3.05 s |
| 48 | 36:48.3 | 3.16 s |
| 49 | 37:17.7 | 5.13 s |
| 50 | 37:47.6 | 5.14 s |
| 51 | 38:18.8 | 5.14 s |
| 52 | 38:51.8 | 5.19 s |
| 53 | 39:23.5 | 5.12 s |
| 54 | 39:53.9 | 5.22 s |
| 55 | 40:25.2 | 5.13 s |
| 56 | 40:56.3 | 5.12 s |
| 57 | 41:29.5 | 5.15 s |
| 58 | 42:01.9 | 5.16 s |
| 59 | 42:34.2 | 5.49 s |
| 60 | 42:57.3 | 2.55 s |
| 61 | 43:17.4 | 3.06 s |
| 62 | 45:25.8 | 3.03 s |
| 63 | 45:30.6 | 3.02 s |
| 64 | 45:35.9 | 3.02 s |
| 65 | 45:40.8 | 5.45 s |
| 66 | 46:04.8 | 3.05 s |
| 67 | 48:19.2 | 10.01 s |
| 68 | 48:38.7 | 9.25 s |
