---
name: official-audio-analysis
description: Single owner of how to analyze official JLPT listening audio (MP3/CD tracks) to extract pacing, pause structure, and loudness for replication. Use whenever an official or sample choukai MP3 is provided, whenever the user says "learn from this audio", or whenever MP3 generation pacing needs calibration or verification. Output of this skill is a pacing table consumed by choukai-mp3-generation.
---

# Official Audio Analysis

## The answer is already measured — read it before you measure anything

**`references/official_pacing.md` holds the pacing band derived from all 31
official sittings (2010-07 … 2025-12), with per-sitting tables, sample counts,
method and coverage.** Read it first. Re-measure only to check a specific
claim or after adding recordings — not to re-derive what is already there from
one file, which is how three wrong numbers got into this skill (see below).

## Locating Audio References (`refs/`)

- **Official Exam Audio — the archive**:
  `refs/JLPT_N2_NEW/<n>. N2 <M>-<YYYY>/…mp3`, **31 sittings, 2010-07 to
  2025-12** (every sitting except July 2020, which was cancelled), each folder
  also holding the booklet PDF and the script PDF. This is the calibration
  corpus. Paths contain spaces and dots — always quote them, and find them with
  `find refs/JLPT_N2_NEW -name '*.mp3'` rather than typing them.
- **There is no second audio folder, and adding one is a defect.** A sibling
  folder under `refs/` once held five MP3s that were **byte-identical
  duplicates** (sha1-verified) of the archive's 2023-07 / 2023-12 / 2024-12 /
  2025-07 / 2025-12 entries. It has been deleted: a "five-recording"
  measurement over it plus the archive double-weighted the last three years.
  `refs/JLPT_N2_NEW/` is the whole calibration corpus — never re-add a copy.
- **`.rar` files** sit beside some MP3s (2019-07, 2022-07, 2025-12). Ignore
  them; the MP3 is already extracted.
- **Script PDFs are SCANS.** Text extraction yields only the typed
  situation/問い headers (~2.7 k chars over 20 pages), so a transcript mora
  count is not available for official audio. Measure rate acoustically (Step 5).
- **Textbook CD tracks**: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai-CD/` —
  weaker evidence than an official exam recording; label it as such if used.

## Step 1 — Basics

```bash
ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1 "refs/JLPT_N2_NEW/17.N2 12-2025/JLPT N2 12.2025 Choukai.mp3"
ffmpeg -i "refs/JLPT_N2_NEW/17.N2 12-2025/JLPT N2 12.2025 Choukai.mp3" \
  -af loudnorm=I=-15:TP=-1.0:LRA=11:print_format=json -f null -
```

Measured over all 31: runtime **36.6–52.1 min** (median 43.3), integrated
loudness **−15.0 LUFS** (p25 −15.5, p75 −14.3), true peak median −0.86 dBTP,
LRA 7.5–9.8.

Two corrections this archive forced, both from single-file measurements that
had been generalised:

- Runtime is **not** "consistently ~50-52 min". It is not consistent at all,
  and it is not a calibration target — the pauses are.
- **Use `loudnorm`, not `volumedetect`.** `mean_volume` reads −19 to −20 dB on
  these recordings because it is ungated flat RMS over the whole file, silence
  included; `loudnorm`'s `I` is gated and K-weighted and reads −15.0. Treating
  a `mean_volume` number as LUFS is what set the synthesis target to −17 and
  shipped every generated exam ~2 dB quiet.

## Step 2 — Long-pause histogram

```bash
ffmpeg -i "refs/JLPT_N2_NEW/17.N2 12-2025/JLPT N2 12.2025 Choukai.mp3" \
  -af silencedetect=noise=-35dB:d=2.5 -f null - 2>&1 \
  | grep -oE "silence_duration: [0-9.]+"
```

**A fixed threshold is not comparable across sittings.** Several recordings
(2023-12 and 2024-12 among them) lay a soft **~−34 dBFS marker tone** over the
last ~2.5 s of every answer pause. At `noise=-35dB` their 12 s pause reports as
9 s and their 8 s pause as 5 s, and the archive looks inconsistent when it is
not. Either run at `-30dB` as a cross-check, or use the two-threshold envelope
method in `references/official_pacing.md` §1, which is what the band was
measured with. Never read a constant off one threshold on one file.

Bucket the durations. A full official N2 exam clusters as:
~3s (structural) / ~8s (answer time 問3・問4) / ~12s (answer time 問1・問2) /
~20s (問題2 option-READING time — easy to miss and critical).

## Step 3 — Timeline attribution

Print ordered `(start_time, duration)` pairs and read the sequence. Patterns
identify sections without hearing a word:

- `20s → …talk… → 12s` repeating → 問題2 (reading pause + answer pause)
- `3s, 3s, 3s, 8s` repeating → 問題3/5 spoken choices (3s apart) + answer time
- dense run of lone `8s` pauses → 問題4
- `10s` then `12s` near the end → 問題5 two-question item (質問1/質問2)

Measured on Dec 2025 (`silencedetect` at `d=2.5` then `d=0.4`), which is where
the constants in `choukai-mp3-generation` come from:

| Region | Signature | Section |
|---|---|---|
| 36.4–37.0 min | 3 × 3.0 s gaps → 4 spoken choices → 8.57 s answer pause | 問題3 |
| 38.7–44.7 min | internal gaps only 1.0–2.0 s (nothing ≥2.5 s) → 8.19 s answer pause, **11 items** over ~6 min | 問題4 |
| 47.3–51.4 min | 3 × 3.0 s gaps → 8.5 s; then 10.0 s + 12.3 s at the very end | 問題5 — **1番** (spoken choices), then **2番's** 質問1 / 質問2 |

**The 問題4 row is the load-bearing one**: its three choices are read
continuously, so the 3 s spoken-choice gap belongs to 問題3/問題5 ONLY. Whole-file
histogram for cross-checking a full N2: 7 × 20 s, 12 × ~12 s, 17 × ~8 s, 42 × ~3 s.

**The histogram is also the cheapest proof of the item counts** (re-measured on
the Dec 2025 file, total 51.4 min), because official audio gives an answer pause
after **scored items only** — never after an 例, which is followed straight by
the 「最もよいものは◯番です…」 confirmation:

- 12 × 12 s = 問題1 (5) + 問題2 (6) + the final 質問2 (1)
- 7 × 20 s = 問題2's option-reading time, 例 + 6 items
- 17 × 8 s = 問題3 (5) + 問題4 (**11**) + 問題5 1番 (1)
- so the paper is 5 / 6 / 5 / 11 / 3 = 30 answers, exactly the table in
  `jlpt-exam-structure` — and **not** the 2009 guidebook's 目安 (12 即時応答,
  4 統合理解). If a future measurement disagrees with those counts, re-measure
  before believing it; two earlier revisions of this file carried the
  guidebook's numbers as if they had been measured.

Note this is where our build deliberately deviates: `make_choukai_mp3.py`
appends `ANSWER_PAUSE` after **every** item block, 例 included, so a generated
MP3 has 13 × 12 s / 18 × 8 s where the official file has 12 / 17. See the
dry-run table in `choukai-mp3-generation`.

## Step 4 — Short gaps (dialogue pacing)

**`silencedetect` cannot see a turn gap at all.** Official dialogue carries
room tone between turns, not digital silence, so a 44-second conversation
registers as one continuous run at any threshold near the noise floor. The
"≈1.0–1.5 s, use 1.3 s" figure this section used to carry came from that blind
measurement and was **too long by roughly a factor of two**.

Measure turn gaps by diarizing instead: take every gap below the extended
threshold inside a 問題1/問題2 dialogue span, and label each speaker-change or
same-speaker by comparing median F0 (autocorrelation) over the 0.6 s of speech
either side — male ~110–150 Hz vs female ~200–260 Hz separates cleanly, which
is what two-party items are built from. Over 11 sittings (2018–2025), n=465
turn boundaries:

| | median | p75 | p90 | max |
|---|---|---|---|---|
| **turn gap (speaker changes)** | **0.51 s** | 0.75 s | 1.08 s | 2.56 s |
| within-turn pause (same speaker) | 0.40 s | 0.53 s | 0.72 s | 2.65 s |

`GAP_BETWEEN_LINES` is now **0.9 s**, which lands the measured gap in our own
output at ≈0.72 s — the official p75. It is deliberately above the official
median: synthetic voices carry no prosodic turn-taking cues, so a little air
buys intelligibility without slipping to the 1.3 s that exceeded every
sitting's p75.

## Step 5 — Speech rate (not just pauses)

Pause structure alone does not prove the exam isn't underestimating N2 level —
a correctly-paced recording of speech that is itself too SLOW still makes the
exam easier than the real thing. This was never checked before it shipped
across 4 generated tests: `choukai-mp3-generation`'s `SPEAKER_MAP` rates
(−8% to +6% per character, −10% narrator) were chosen only to make voices
distinguishable from each other, never calibrated against measured official
speech tempo.

Measure rate in **morae/minute**, not characters/minute — kanji-heavy text
compresses multiple morae per character, so a raw character count
understates true speech density. Natural adult Japanese conversation runs
**~300–400+ morae/min**.

**Mind the level band: N2 is not N1.** The official 認定の目安 says N1 listens
to 「**自然な**スピードの、まとまりのある会話やニュース、講義」 while N2 listens
to 「**自然に近い**スピードの、まとまりのある会話やニュース」 (N3: 「やや自然に
近い」). So the target for N2 dialogue is at or a little below natural — not the
top of the natural band. Anything *noticeably* under it is still a real defect
(N4/N5 slow-for-beginners pacing makes the exam easier than it is), but do not
push rates upward to reach an N1 figure.

**The script PDFs are scans**, so there is no transcript to count morae from on
the official side. Measure rate acoustically — syllable nuclei (intensity peaks
with a 2 dB dip criterion), which in mora-timed Japanese track morae — and
apply the **same detector to both sides**, so no calibration constant enters the
comparison:

| Audio | syllable nuclei / min of speech |
|---|---|
| official archive, all 31 sittings | 250 – 281, median **271** |
| `tests/2/聴解.mp3` | 270.6 |
| `tests/1/聴解.mp3` | 279.7 |

**Our synthesized audio is inside the official band**, at its top. No rate
change is warranted; do not raise `SPEAKER_MAP` rates on the strength of the
300–400 morae/min figure above (converting nuclei to morae needs a ratio
calibrated on synthetic speech — 0.589 from `tests/1`+`tests/2`, where the text
is known exactly — and that ratio does not transfer to human speech, which
reduces more; it puts the archive at 425–478 morae/min, which is why the
converted number is indicative only).

Within the archive the announcer is consistently more measured than the
dialogue — opening narration estimates at 432 morae/min against 449–467 for the
five sections — the same relationship our −10 % narrator rate produces.

Older single-line verifications of this repo's voices, kept for reference:
dialogue (rate ±0–6 %) a 43-mora line in 6.816 s → ~378 morae/min; narrator
(−10 %) a 42-mora line in 8.544 s → ~295 morae/min.

Re-verify this whenever a voice or rate value changes in
`choukai-mp3-generation`'s `SPEAKER_MAP`/`NARRATOR` — a "faster to build" or
"clearer" rate tweak is exactly the kind of change that can silently drift
back toward underestimating difficulty without anyone noticing, since nothing
else in the pipeline checks rate.

## Deliverable

A pacing table in this exact shape (feed to choukai-mp3-generation). The
"official" column is the median over the sittings that segmented, with the
band in brackets; full per-sitting tables and sample counts are in
`references/official_pacing.md`.

| Parameter | Adopted value | Official (median [band], n) |
|---|---|---|
| gap between dialogue turns | 0.9 s | 0.51 s [p75 0.75, p90 1.08], n=465 |
| after question, before talk (問1) | 3 s | 2.80 s [2.5–4.6], n=74 |
| 問題2 option-reading pause | 20 s | 20.22 s [20.19–20.81], n=139 |
| between spoken choices (問3/5) | 3 s | 3.10 s [2.66–3.26], n=427 |
| answer pause 問1/問2 | 12 s | 12.22 s [12.1–12.5], n=242 |
| answer pause 問3/問4 | 8 s | 8.29 s [8.18–8.47], n=377 |
| answer pause 問5 (each item; the 質問1 → 質問2 gap is also 10 s) | 10 s | 1番 8.3 / 質問1 10.0 / 質問2 11.2 s, n=56 |
| loudness target | **−15 LUFS**, −1.0 dBTP | −15.01 LUFS [−15.5, −14.3]; TP −0.86 [−1.7, −0.3], n=31 |
| dialogue speech rate (character voices) | unchanged | our build 271–280 nuclei/min vs official 250–281 (median 271) — inside the band, at its top; N2's 認定の目安 is 自然に**近い** speed, so do not raise |
| narrator/announcer speech rate | unchanged (−10 %) | official narration is measurably slower than its dialogue (432 vs 449–467 est. morae/min) — the same relationship |

Notes:

- **問題5's three pauses are 8.3 / 10.0 / 11.2 s**, not one value; `ANSWER_PAUSE`
  is one number per 問題, so 10 s stays as the compromise — exact for the
  質問1→質問2 gap, between the other two.
- **Every adopted value except the turn gap was already inside the band**, and
  the band has not moved between 2010 and 2025 (|r| ≤ 0.22 against sitting
  date). Two things changed on this evidence: `GAP_BETWEEN_LINES` 1.3 → 0.9 s
  (Step 4) and the loudness target −17 → −15 LUFS (Step 1).
- The copy of this table in `choukai-mp3-generation/SKILL.md` is the one
  `make check` diffs against the code — change values there (and in the code)
  first, then mirror here.

