# Official N2 listening pacing — measured across 31 sittings (2010-07 … 2025-12)

Source corpus: `refs/JLPT_N2_NEW/`, 31 official N2 listening MP3s — every
sitting from July 2010 to December 2025 except July 2020 (cancelled). The
five files in the older `refs/JLPT/` folder are byte-identical duplicates
of the 2023-07/2023-12/2024-12/2025-07/2025-12 entries here (verified by
sha1) — not counted twice.

This file is the evidence behind the pacing table in `choukai-audio/SKILL.md`
Part 3, which is the copy `make check` diffs against the code. Change values
there and in the code first, then mirror here.

Measured 2026-08-06 with ffmpeg 8.1.2/ffprobe on macOS. Nothing under
`tests/`/`logs/` was touched; `refs/` was only read. No dialogue content was
transcribed — every number below comes from the amplitude envelope.

---

## 1. Method

**Why a naive `silencedetect` is not enough.** At a fixed `noise=-35dB` the
2023-12/2024-12 files report their 12s answer pause as 9s and their 8s pause
as 5s — those sittings lay a **soft ~-34 dBFS marker tone** over the last
~2.5s of every answer pause. Not speech, takes no answer time, but sits
above the threshold — a fixed-threshold run would have shortened two
sittings by 3s each and made the archive look inconsistent when it isn't.

So each file decodes to a 16kHz mono, 20/10ms RMS envelope, and pauses are
found with **two thresholds**:

| Threshold | Value | Role |
|---|---|---|
| core | −60 dBFS | literal silence — 33–41% of frames sit here, speech above −40 dBFS, so −60 is inside every file's valley |
| extended | min(−25, LUFS−8) dBFS | the real speech offset→onset extent, includes the marker tone, excludes nothing spoken |

A pause = a maximal run below the extended threshold containing ≥0.30s of
core silence. Reported values are the extended ones — the extension
swallows very quiet speech tails, but only slightly (問1/2 answer pause:
core median 12.14s vs extended 12.23s, bias ≈0.1s).

**Section attribution is structural, never content-based** — 問題2 is the
only section with a long option-reading pause before every item, so the
~20s run brackets it; before it is 問題1, after it 問題3 (1.5–2min apart),
問題4 (dense, 0.5–0.8min apart), 問題5. A file whose shape isn't a sane N2
is reported NOT SEGMENTED rather than folded in with guessed numbers (§6).

**Turn gaps needed a third method** — official dialogue carries room tone,
not digital silence, so the pause detector can't see turn boundaries at
all. Measured separately over 問題1/2 dialogue spans (2018–2025): every gap
below the extended threshold, labelled speaker-change/same-speaker by
median F0 (autocorrelation) over 0.6s either side — Japanese male
(~110–150Hz)/female (~200–260Hz) separate cleanly.

**Speech rate** — the script PDFs are scans (~2.7k chars of headers only,
no transcript for mora counts), so rate is acoustic: syllable nuclei
(intensity peaks, 2dB dip) per minute, calibrated against this repo's own
TTS output where text is known exactly (`tests/1`/`tests/2`: 0.595/0.582
nuclei per mora). That ratio is synthetic-derived and human speech reduces
more, so **absolute morae/min figures are estimates** — the raw nuclei/min
comparison is the sound one.

---

## 2. The band — this is what the constants must sit inside

Medians with interquartile band; n = individual pauses measured.

| Parameter | All 22 segmented | Recent 12 (2018–2025) | Current constant | Verdict |
|---|---|---|---|---|
| answer pause 問題1 | **12.23** [12.17–12.49] n=106 | 12.43 n=57 | `ANSWER_PAUSE 問1 = 12` | inside |
| answer pause 問題2 | **12.22** [12.09–12.50] n=136 | 12.36 n=73 | `= 12` | inside |
| answer pause 問題3 | **8.32** [8.17–8.57] n=110 | 8.38 n=64 | `= 8` | inside |
| answer pause 問題4 | **8.28** [8.19–8.43] n=267 | 8.32 n=139 | `= 8` | inside |
| 問題2 option-reading | **20.22** [20.19–20.38] n=139 | 20.22 n=77 | `GAP_OPTION_READING = 20` | inside |
| 問題1 question→conversation | **2.80** [2.74–2.91] n=74 | 2.80 n=39 | `GAP_AFTER_PRE_QUESTION = 3` | inside |
| 問題1 conversation→repeated question | 2.94 [2.81–3.19] n=74 | 3.02 n=39 | `GAP_BEFORE_REPEATED_QUESTION = 3` | inside — never applied until 2026-08-13, §2.1 |
| 問題4, between three replies | 2.23 [2.14–2.31] n=795 | — | `GAP_BETWEEN_SPOKEN_RESPONSES = 2.2` | inside — added 2026-08-13, §2.1 |
| between spoken choices, 問題3 | **3.10** [2.66–3.26] n=427 | 3.13 n=245 | `GAP_BETWEEN_SPOKEN_CHOICES = 3` | inside |
| between spoken choices, 問題5 | 3.07 [2.62–3.26] n=220 | 3.06 n=102 | same constant | inside |
| 問題5 質問1→質問2 | **10.0** [7.8–12.4] n=20 | 10.0 | `GAP_AFTER_SHITSUMON1 = 10` | inside |
| **dialogue turn gap** | **0.51** [p25 0.30, p75 0.75, p90 1.08, max 2.56] n=465 | 2018–2025 only | was 1.3 | **outside → changed to 0.9** |

Same-speaker (within-turn) pauses, for contrast: median 0.40, p75 0.53, p90
0.72, n=181 — turn boundaries are the longer class, still only half a second.

### The constants were right and the audio was still wrong

Every value above was inside its band while the shipped audio was **2× too
slow at every turn boundary** — a gap is inserted BETWEEN segments, and
both TTS engines pad each segment (edge-tts ~0.22s lead + ~0.85s tail
silence per utterance). Measured before the fix: turn gaps 1.88–2.09s
against `GAP_BETWEEN_LINES = 0.9`, mid-turn 。 running 0.97–1.04s against
official's 0.53 p75.

`shape_pauses()` now trims each segment's lead/tail silence to zero and caps
internal pauses above `SHAPE_PAUSE_FLOOR` (0.6s) at `GAP_WITHIN_TURN_MAX`
(0.5s), leaving shorter ones untouched (a ~0.1s 促音 closure survives).
Re-measured after the fix:

| | before | after | official |
|---|---|---|---|
| turn gap, median | 1.88–2.09s | **0.93s** | 0.51 [p75 0.75, p90 1.08] |
| within-turn pause, median | 0.30s, with 。 at 0.97 | **0.38–0.44s** | 0.40 [p75 0.53] |
| runtime of one item, same lines | 87.1s | **74.3s** | — |

**The lesson is a method, not a number: verify a pacing constant on the
rendered MP3, not in the source.** A constants-only review passed this
defect on every paper it had.

### 2.1 The constants were right, reachable, and applied — check all three

Measuring `20260813_2`'s rendered MP3 against the archive on 2026-08-13
found the next layer: two values this table already carried were **never
reached by the code**, and one pause the archive doesn't have was inserted.

| | this table said | the audio had | official |
|---|---|---|---|
| 問題4, reply→reply | "belongs to 問3/5 ONLY" — no constant existed | **0.900s** ×4 in 1番 | 2.23 [2.14–2.31] n=795 |
| 問題1/2, talk→question repeated | "(same constant)", verdict inside | **0.905s** | 2.94 [2.81–3.19] n=74 |
| after an 例 | our deviation, 13×12s/18×8s | 12s/8s | none — 例 runs into the confirmation |

`GAP_AFTER_PRE_QUESTION` was applied only at `line_index == 1`, so the
repeated question (the block's LAST line) fell through to
`GAP_BETWEEN_LINES`; the spoken-choice branch was gated on
`section in ("問題3","問題5")`, so every 問題4 gap did too. Both read
"inside" in every review, because a review checks the value, not whether
the branch can be reached — 問題4 was the expensive one (即時応答 is heard
once; 2.5× tighter replies raised the section above real-exam difficulty
for eight papers).

Two lessons, now enforced rather than remembered: **measure the rendered
MP3 against the ARCHIVE, not the table** (a silencedetect histogram over
one paper takes a minute and would have caught all three); and **a pacing
change makes every existing MP3 stale, and `script_sha` can't see it** — the
constants aren't in the script bytes. `pacing_sha` now stamps the GAP_/
PAUSE_/SHAPE_ values plus the source of `pause_after`/`gap_before_line`/
`shape_pauses` into `聴解_チャプター.json`; `make check` fails on disagreement.

### 問題5 is three different pauses, not one

| Position | n | min | median | max |
|---|---|---|---|---|
| 1番 (spoken choices, like 問題3) | 16 | 6.1 | **8.3** | 8.9 |
| 質問1→質問2 | 20 | 7.8 | **10.0** | 12.4 |
| 質問2, the last pause of the paper | 20 | 8.4 | **11.2** | 19.8 |

`ANSWER_PAUSE` is one number per 問題, so 10s is the right compromise —
exact for 質問1, between the other two. The long tail on the final pause is
the recording running into the closing announcement, not answer time.

### Structure the generator does not reproduce

- Official reads spoken choices as 「1、」+ ~1.1s + the option text, then
  ~3.1s before the next number — we speak each choice as one utterance, so
  only the ~3s inter-choice gap exists in our audio.
- 問題4's three responses are read continuously — gaps cluster at 2.23s
  [2.14–2.31] n=795, well below 問題3/5's 3.1s. Reproduced since 2026-08-13
  by `GAP_BETWEEN_SPOKEN_RESPONSES = 2.2`; before that every 問題4 gap was 0.9s.
- A single ~10s rest sits between 問題2 and 問題3 in 5 of 22 segmented
  sittings, landing after the 問題3 instruction and before its 例 — absent
  or absorbed elsewhere in the rest. Not reproduced; low priority.

---

## 3. Drift 2010 → 2025: there is none

Correlation between sitting date and measured value, over 22 segmented sittings:

| Quantity | r |
|---|---|
| 問題1 answer pause | +0.22 |
| 問題4 answer pause | +0.19 |
| 問題2 option-reading pause | +0.05 |
| speech rate | +0.15 |
| total runtime | +0.34 |
| integrated LUFS (all 31) | −0.01 |

The 問題2 reading pause is 20.2s in every single sitting 2010–2025; 問1/2
answer pause never leaves 11.8–12.9s; 問3/4 never leaves 7.8–8.8s. So
"calibrate to recent practice" and "calibrate to the whole archive" give
the same answer.

---

## 4. Loudness and runtime — all 31 recordings

| Quantity | min | p25 | median | p75 | max |
|---|---|---|---|---|---|
| integrated loudness (LUFS) | −18.33 | −15.48 | **−15.01** | −14.29 | −10.38 |
| true peak (dBTP) | −3.26 | −1.71 | **−0.86** | −0.33 | +0.81 |
| loudness range (LRA) | 7.50 | 8.10 | **8.30** | 8.90 | 9.80 |
| narrator F0 at the opening (Hz) | 175.8 | 209.2 | **216.2** | 225.4 | 254.0 |
| runtime (min) | 36.6 | 41.2 | **43.3** | 47.7 | 52.1 |
| speech time (min) | 14.8 | 17.3 | **18.7** | 20.2 | 23.1 |
| syllable nuclei / min of speech | 250 | — | **271** | — | 281 |

**The narrator is female in all 31 recordings** — lowest opening F0 is
176Hz (2018-12), median 216Hz — confirming `NARRATOR = FEMALE` on the whole
archive, not one file.

**Runtime is NOT "consistently ~50–52 min"** — that old claim (measured on
one file) is wrong even for the old five (42.2–51.4min); the archive spread
is 36.6–52.1min. Runtime is not a calibration target; the pauses are.

### The loudness target was a unit error

`volumedetect`'s `mean_volume` on official audio reads −19 to −20dB — where
the old `I=-17` target came from. `mean_volume` is ungated flat RMS over the
whole file, silence included; `loudnorm`'s `I` is gated and K-weighted — on
the same recordings they differ by ~4dB, and the figure `loudnorm` actually
controls has a median of **−15.0 LUFS** (27 of 31 above −17). `I=-17`
therefore shipped every generated exam ~2dB quieter than reference. Now `I=-15`.

True peak stays −1.0 dBTP (official median −0.86, several sittings clip
above 0). LRA stays 11 — a ceiling official material (7.5–9.8) never reaches.

---

## 5. Speech rate — our TTS is already inside the official band

One detector applied identically both sides, so no calibration constant is
involved in the comparison:

| Audio | syllable nuclei / min of speech |
|---|---|
| official archive, 31 sittings | 250–281, median **271** |
| `tests/2/聴解.mp3` | 270.6 |
| `tests/1/聴解.mp3` | 279.7 |

Our synthesized audio sits at the top of the band but inside it —
`SPEAKER_MAP` rates need no change on this evidence; N2's 認定の目安 is
「自然に**近い**」 speed, not natural speed, so don't push rates up.

Converted through the 0.589 nuclei/mora TTS-derived ratio, the archive
estimates 425–478 morae/min — above the 300–400 "natural conversation"
figure elsewhere, because that ratio doesn't transfer from synthetic to
human speech; treat it as indicative only, prefer the nuclei comparison.

Per-section rate (estimated morae/min, medians): 問題1 467, 問題2 457,
問題3 466, 問題4 449, 問題5 466; the announcer's opening 25s measures 432 —
the narrator is consistently more measured than the dialogue, which our
−10% narrator rate reproduces.

Section runtimes, median [range]: 問題1 6.1 [4.3–6.9], 問題2 9.8
[7.6–11.0], 問題3 6.5 [4.6–9.2], 問題4 6.3 [4.6–8.0], 問題5 5.1 [2.6–6.2]
min (first answer pause to end of last).

---

## 6. Coverage — what was measured and what was not

Loudness, true peak, LRA, runtime, speech time, narrator F0, speech rate:
all 31 files, no failures.

Pause/section segmentation: **22 of 31**. The nine below are reported
unavailable rather than estimated — a fabricated pause constant silently
mis-times every future exam. All nine are pre-2018 or duplicate a
neighbouring sitting's structure; excluding them moves no median (recent-12
agrees with all-22 to within 0.2s).

| Sitting | Why it was not segmented |
|---|---|
| 2010-07, 2011-12, 2012-12, 2013-12, 2017-12, 2018-07, 2024-07 | 8–9 answer pauses attributed to 問題2 — an extra structural pause the shape rules can't safely assign |
| 2012-07 | densest item run is only 5 — no 問題4 signature (most heavily edited copy in the archive) |
| 2022-12 | only 3 pauses in 問題1's answer class |

---

## 7. Reproducing this

Not committed (one-shot analysis, inputs are 2GB of `refs/` audio). Four
steps:

```
decode      ffmpeg -ac 1 -ar 16000 -f s16le          (20 ms RMS frames for pauses,
                                                      10 ms for nuclei/F0)
loudness    ffmpeg -af loudnorm=I=-15:TP=-1.0:LRA=11:print_format=json -f null -
pauses      core -60 dBFS (>=0.30 s) extended to min(-25, LUFS-8) dBFS
turn gaps   F0 by autocorrelation, 0.6 s either side, speaker change at >15 % Δ
nuclei      2 dB dip criterion, peak floor 22 dB below the 95th pct speech level
```
