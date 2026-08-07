# N2 7/2024 — 聴解音声 inspection

> Machine-extracted by `tools/extract_jlpt_n2_new.py` (ffprobe + ffmpeg) from:
> - `refs/JLPT_N2_NEW/15. N2 7-2024/Nghe N2 T7-2024.mp3` (sha1 `c59af43d7b29`)
> Measured per `.agents/choukai-audio/SKILL.md` (`silencedetect=noise=-35dB`, one pass at `d=0.4`).
> Regenerate rather than hand-edit.

## Basics

| Parameter | Value | Official band |
| --- | --- | --- |
| duration | 48:05.6 (48.1 min) | ~50–52 min |
| codec / sample rate / channels | png / 44100 Hz / 2 | — |
| bit rate | 128 kb/s | — |
| mean volume | -19.7 dB | −17 to −18 dB |
| max volume | -0.8 dB | — |

## Long-pause histogram (≥2.5 s)

| Bucket | Count | Meaning |
| --- | --- | --- |
| ~3 s (2.5–5 s) | 41 | structural gap |
| ~8 s (5–9.5 s) | 19 | answer time 問題3・問題4 |
| ~10 s (9.5–11.5 s) | 1 | answer time 問題5 / 質問1→質問2 |
| ~12 s (11.5–16 s) | 0 | answer time 問題1・問題2 |
| ~20 s (16–60 s) | 7 | 問題2 option-reading time |
| **total** | **68** | 0 outside every bucket |

## Dialogue pacing (0.4–2.5 s gaps)

- 836 gaps; median **0.77 s**, mean 1.00 s (official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)

## Long-pause timeline

Ordered `(start, duration)`. Attribute sections from the signatures in `choukai-audio` §3 — a `20 s → talk → 12 s` cycle is 問題2, `3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s pauses is 問題4. Counts are measured, section labels are not.

| # | start | duration |
| --- | --- | --- |
| 1 | 0:11.1 | 3.07 s |
| 2 | 1:24.0 | 3.05 s |
| 3 | 2:53.8 | 3.28 s |
| 4 | 4:18.3 | 8.89 s |
| 5 | 5:42.0 | 8.89 s |
| 6 | 7:13.9 | 8.77 s |
| 7 | 8:43.0 | 8.84 s |
| 8 | 10:15.9 | 9.16 s |
| 9 | 10:51.3 | 3.05 s |
| 10 | 11:09.1 | 20.19 s |
| 11 | 12:43.7 | 3.34 s |
| 12 | 13:03.5 | 20.18 s |
| 13 | 14:34.7 | 8.76 s |
| 14 | 14:58.2 | 20.20 s |
| 15 | 16:50.9 | 8.78 s |
| 16 | 17:17.0 | 20.18 s |
| 17 | 18:49.0 | 8.76 s |
| 18 | 19:14.4 | 20.18 s |
| 19 | 21:11.8 | 8.76 s |
| 20 | 21:38.2 | 20.19 s |
| 21 | 23:05.0 | 8.78 s |
| 22 | 23:31.7 | 20.18 s |
| 23 | 24:48.0 | 9.22 s |
| 24 | 25:28.4 | 3.84 s |
| 25 | 26:06.9 | 3.07 s |
| 26 | 27:44.6 | 3.21 s |
| 27 | 28:39.8 | 3.03 s |
| 28 | 28:45.1 | 3.03 s |
| 29 | 28:51.4 | 3.04 s |
| 30 | 28:57.4 | 4.95 s |
| 31 | 30:13.8 | 3.01 s |
| 32 | 30:20.5 | 3.02 s |
| 33 | 30:27.6 | 3.03 s |
| 34 | 30:34.8 | 4.86 s |
| 35 | 31:48.5 | 3.01 s |
| 36 | 31:54.8 | 3.02 s |
| 37 | 32:01.2 | 3.02 s |
| 38 | 32:08.2 | 4.81 s |
| 39 | 33:06.7 | 3.02 s |
| 40 | 33:12.5 | 3.02 s |
| 41 | 33:18.8 | 3.01 s |
| 42 | 33:25.0 | 4.91 s |
| 43 | 34:26.9 | 3.03 s |
| 44 | 34:33.3 | 3.03 s |
| 45 | 34:39.8 | 3.02 s |
| 46 | 34:46.4 | 5.28 s |
| 47 | 35:15.2 | 3.05 s |
| 48 | 36:03.2 | 3.16 s |
| 49 | 36:33.2 | 4.99 s |
| 50 | 37:03.7 | 4.97 s |
| 51 | 37:34.0 | 5.01 s |
| 52 | 38:04.5 | 4.98 s |
| 53 | 38:32.9 | 4.97 s |
| 54 | 39:06.1 | 5.00 s |
| 55 | 39:39.7 | 4.97 s |
| 56 | 40:12.3 | 5.01 s |
| 57 | 40:45.0 | 5.03 s |
| 58 | 41:17.4 | 5.03 s |
| 59 | 41:48.0 | 5.30 s |
| 60 | 42:11.0 | 2.55 s |
| 61 | 42:31.1 | 3.06 s |
| 62 | 44:40.6 | 3.01 s |
| 63 | 44:47.5 | 3.02 s |
| 64 | 44:53.3 | 3.02 s |
| 65 | 44:59.2 | 5.14 s |
| 66 | 45:22.9 | 3.05 s |
| 67 | 47:29.6 | 10.01 s |
| 68 | 47:48.6 | 8.88 s |
