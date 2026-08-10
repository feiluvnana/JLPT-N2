# Official N2 listening pacing — measured across 31 sittings (2010-07 … 2025-12)

Source corpus: **`refs/JLPT_N2_NEW/`**, 31 official N2 listening MP3s — every
sitting from July 2010 to December 2025 except July 2020 (cancelled). The five
files in the older `refs/JLPT/` folder are **byte-identical duplicates** of the
2023-07 / 2023-12 / 2024-12 / 2025-07 / 2025-12 entries here (verified by
sha1), so they are not counted twice.

This file is the evidence behind the pacing table in
`choukai-audio/SKILL.md` (Part 3), which is the copy `make check` diffs against
the code. Change values there and in the code first, then mirror here.

Measured 2026-08-06 with ffmpeg 8.1.2 / ffprobe on macOS. Nothing under
`tests/` or `logs/` was touched; `refs/` was only read. No dialogue content was
transcribed — every number below comes from the amplitude envelope.

---

## 1. Method

**Why a naive `silencedetect` is not enough.** The distributed recordings are
not engineered alike. At a fixed `noise=-35dB` the 2023-12 and 2024-12 files
report their 12 s answer pause as 9 s and their 8 s pause as 5 s. Inspecting
the envelope shows why: those sittings lay a **soft ~-34 dBFS marker tone**
over the last ~2.5 s of every answer pause. The tone is not speech and takes
no answer time away, but it sits above the threshold. Reading the constants off
a single fixed-threshold run would have shortened two sittings by 3 s each and
made the archive look inconsistent when it is not.

So each file is decoded once to a 16 kHz mono, 20/10 ms RMS envelope, and
pauses are found with **two thresholds**:

| Threshold | Value | Role |
|---|---|---|
| core | −60 dBFS | literal silence. Every file is strongly bimodal — 33–41 % of frames are digital silence and speech sits above −40 dBFS — so −60 is inside the valley of all 31. |
| extended | min(−25, LUFS − 8) dBFS | the real speech offset→onset extent. Includes the marker tone; excludes nothing that is spoken. |

A pause = a maximal run below the extended threshold that contains ≥0.30 s of
core silence (so an inter-syllable dip can never become a pause). Reported
values are the extended ones. **Cost of the extension**: it also swallows very
quiet speech tails, so extended values run slightly long — but only slightly:
for the 問題1/2 answer pause the core median is 12.14 s against an extended
median of 12.23 s, i.e. **the bias is ≈0.1 s**, not the 0.5 s one might fear.

**Section attribution is structural, never content-based.** 問題2 is the only
section with a long option-READING pause before every item, so the run of
~20 s pauses brackets it; what precedes is 問題1; after it come 問題3 (items
1.5–2 min apart), 問題4 (the dense run, items 0.5–0.8 min apart) and 問題5 (the
trailing pauses). A file whose derived shape is not a sane N2 is reported
**NOT SEGMENTED** rather than folded in with guessed numbers — see §6.

**Turn gaps needed a third method.** Official dialogue carries room tone, not
digital silence, so the pause detector above cannot see turn boundaries at all
(a 44 s conversation registers as one continuous run). Turn gaps were measured
separately over the 問題1/問題2 dialogue spans of the 2018–2025 sittings: every
gap below the extended threshold was taken, and each was labelled
speaker-change / same-speaker by comparing median F0 (autocorrelation) over the
0.6 s of speech either side. Japanese male (~110–150 Hz) and female
(~200–260 Hz) separate cleanly, which is what two-party 問題1/2 items are built
from.

**Speech rate.** The script PDFs in the archive are **scans** — text extraction
yields only the typed situation/問い headers (~2.7 k chars over 20 pages) — so
a transcript mora count is *not available* for official audio. Rate is measured
acoustically by counting syllable nuclei (intensity peaks with a 2 dB dip
criterion), which in mora-timed Japanese tracks morae. The detector was
calibrated against this repo's own TTS output, where the text is known exactly
(`tests/1` and `tests/2`: 8 924 and 6 941 morae → 0.595 and 0.582 nuclei per
mora). Because that ratio is derived from synthetic speech and human speech
reduces more, **the absolute morae/min figures below are estimates**; the
raw nuclei/min comparison between official and our own audio is the sound one.

---

## 2. The band — this is what the constants must sit inside

Medians with the interquartile band; n is the number of individual pauses
measured, not the number of files.

| Parameter | All 22 segmented sittings | Recent 12 (2018–2025) | Current constant | Verdict |
|---|---|---|---|---|
| answer pause 問題1 | **12.23** [12.17–12.49] n=106 | 12.43 [12.21–12.58] n=57 | `ANSWER_PAUSE 問題1 = 12` | inside |
| answer pause 問題2 | **12.22** [12.09–12.50] n=136 | 12.36 [12.15–12.57] n=73 | `ANSWER_PAUSE 問題2 = 12` | inside |
| answer pause 問題3 | **8.32** [8.17–8.57] n=110 | 8.38 [8.15–8.69] n=64 | `ANSWER_PAUSE 問題3 = 8` | inside |
| answer pause 問題4 | **8.28** [8.19–8.43] n=267 | 8.32 [8.20–8.57] n=139 | `ANSWER_PAUSE 問題4 = 8` | inside |
| 問題2 option-reading | **20.22** [20.19–20.38] n=139 | 20.22 [20.19–20.42] n=77 | `GAP_OPTION_READING = 20` | inside |
| 問題1 question → conversation | **2.80** [2.74–2.91] n=74 | 2.80 [2.74–4.03] n=39 | `GAP_AFTER_PRE_QUESTION = 3` | inside |
| 問題1 conversation → repeat of question | 2.94 [2.81–3.19] n=74 | 3.02 [2.82–4.15] n=39 | (same constant) | inside |
| between spoken choices, 問題3 | **3.10** [2.66–3.26] n=427 | 3.13 [2.64–3.31] n=245 | `GAP_BETWEEN_SPOKEN_CHOICES = 3` | inside |
| between spoken choices, 問題5 | 3.07 [2.62–3.26] n=220 | 3.06 [2.63–3.25] n=102 | (same constant) | inside |
| 問題5 質問1 → 質問2 | **10.0** [range 7.8–12.4] n=20 | 10.0 | `GAP_AFTER_SHITSUMON1 = 10` | inside |
| **dialogue turn gap** | **0.51** [p25 0.30, p75 0.75, p90 1.08, max 2.56] n=465 | (2018–2025 only) | `GAP_BETWEEN_LINES` was 1.3 | **outside → changed to 0.9** |

Same-speaker (within-turn) pauses, for contrast: median 0.40, p75 0.53,
p90 0.72, n=181. Turn boundaries really are the longer class, and they are
still only half a second.

### The constants were right and the audio was still wrong

Every value above was inside its band while the shipped audio was **2× too
slow at every turn boundary**, because a gap is inserted BETWEEN segments and
both TTS engines pad each segment: edge-tts writes ~0.22 s of lead and
~0.85 s of tail silence into every utterance (Gemini ~0.26 s either side).
Measured in a shipped paper's 問題1 before the fix: turn gaps **1.88–2.09 s**
against `GAP_BETWEEN_LINES = 0.9`, and a mid-turn 。 running 0.97–1.04 s against
an official same-speaker p75 of 0.53.

`shape_pauses()` now trims each segment's leading/trailing silence to zero and
caps internal pauses above `SHAPE_PAUSE_FLOOR` (0.6 s) at
`GAP_WITHIN_TURN_MAX` (0.5 s), leaving shorter ones untouched so a ~0.1 s 促音
closure survives. Re-measured on the rendered MP3 after the fix:

| | before | after | official |
|---|---|---|---|
| turn gap, median | 1.88–2.09 s | **0.93 s** | 0.51 [p75 0.75, p90 1.08] |
| within-turn pause, median | 0.30 s, with 。 at 0.97 | **0.38–0.44 s** | 0.40 [p75 0.53] |
| runtime of one item, same lines | 87.1 s | **74.3 s** | — |

**The lesson is a method, not a number: verify a pacing constant on the
rendered MP3, not in the source.** A constants-only review passed this defect on
every paper it had.

### 問題5 is three different pauses, not one

| Position | n | min | median | max |
|---|---|---|---|---|
| 1番 (has spoken choices, like 問題3) | 16 | 6.1 | **8.3** | 8.9 |
| 質問1 → 質問2 | 20 | 7.8 | **10.0** | 12.4 |
| 質問2, the last pause of the paper | 20 | 8.4 | **11.2** | 19.8 |

`ANSWER_PAUSE` is one number per 問題, so 10 s remains the right compromise:
exact for the 質問1 gap, between the other two. The long tail on the final
pause is the recording running on into the closing announcement, not answer
time.

### Structure the generator does not reproduce

- **Spoken choices are read as 「1、」 + ~1.1 s + the option text**, then ~3.1 s
  before the next number. We speak each choice as one utterance, so only the
  ~3 s inter-choice gap exists in our audio. (Consistent in every segmented
  sitting; the 1.1 s sub-gap has n≈4 per item.)
- **問題4's three responses are read continuously** — the gaps before its answer
  pause cluster at 2.23 s [2.14–2.31] n=795, clearly below the 3.1 s of
  問題3/5. The 3 s spoken-choice gap belongs to 問題3 and 問題5 only, as
  `choukai-audio` Part 4 already says.
- **A single ~10 s rest sits between 問題2 and 問題3** in 5 of 22 segmented
  sittings (9.9 / 10.3 / 10.3 / 10.3 / 10.6 s), landing after the 問題3
  instruction and before its 例. In the other sittings it is absent or
  absorbed into the item run. Not reproduced by our build; low priority.

---

## 3. Drift 2010 → 2025: there is none

Correlation between sitting date and the measured value, over the 22 segmented
sittings:

| Quantity | r |
|---|---|
| 問題1 answer pause | +0.22 |
| 問題4 answer pause | +0.19 |
| 問題2 option-reading pause | +0.05 |
| speech rate | +0.15 |
| total runtime | +0.34 |
| integrated LUFS (all 31) | −0.01 |

The 問題2 reading pause is 20.2 s in **every single sitting from 2010 to 2025**;
the 問題1/2 answer pause never leaves 11.8–12.9 s; 問題3/4 never leaves
7.8–8.8 s. So "calibrate to recent practice" and "calibrate to the whole
archive" give the same answer, and a 2026 mock has no drift to chase.

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

**The narrator is female in all 31 recordings** — the lowest opening F0 in the
archive is 176 Hz (2018-12) and the median is 216 Hz, nowhere near a male range.
The `NARRATOR = FEMALE` rule in `choukai-audio` is confirmed on the
whole archive, not on one file.

**Runtime is NOT "consistently ~50–52 min".** That claim (previously in what
is now `choukai-audio` Part 4 step 1, measured on one file) is wrong even for the
old five, which run 42.2–51.4 min. Across the archive the spread is
36.6–52.1 min. Runtime is not a calibration target; the pauses are.

### The loudness target was a unit error

`volumedetect`'s `mean_volume` on official audio reads −19 to −20 dB — which is
where the old `I=-17` target came from, via the note "mean volume averages −17
to −18 dB (target −17 LUFS)". `mean_volume` is **ungated flat RMS over the
whole file, silence included**; `loudnorm`'s `I` is **gated and K-weighted**.
On the same recordings the two differ by ~4 dB, and the figure `loudnorm`
actually controls has a median of **−15.0 LUFS**, with 27 of 31 sittings above
−17. `I=-17` therefore shipped every generated exam ~2 dB quieter than the
reference material. Now `I=-15`.

True peak stays at −1.0 dBTP: the official median is −0.86 and several sittings
clip above 0 dBTP, which is not worth copying. LRA stays 11 — it is a ceiling
and official material (7.5–9.8) never reaches it.

---

## 5. Speech rate — our TTS is already inside the official band

Measured with one detector applied identically to both sides, so no calibration
constant is involved in the comparison:

| Audio | syllable nuclei / min of speech |
|---|---|
| official archive, 31 sittings | 250 – 281, median **271** |
| `tests/2/聴解.mp3` | 270.6 |
| `tests/1/聴解.mp3` | 279.7 |

Our synthesized audio sits at the top of the official band but inside it. The
`SPEAKER_MAP` rates need no change on this evidence, and the caution in
`choukai-audio` Part 4 step 5 stands: N2's 認定の目安 is 「自然に**近い**」
speed, so do not push rates up.

Converted through the TTS-derived 0.589 nuclei/mora ratio the archive estimates
at 425–478 morae/min, which is above the 300–400 "natural conversation" figure
quoted in the skill — that gap is the calibration ratio not transferring from
synthetic to human speech, so treat the converted number as indicative only and
prefer the nuclei comparison above.

Per-section rate (estimated morae/min, medians over segmented sittings):
問題1 467, 問題2 457, 問題3 466, 問題4 449, 問題5 466; the announcer's opening
25 s measures **432**, i.e. the narrator is consistently more measured than the
dialogue. Our −10 % narrator rate reproduces that relationship.

Section runtimes, median [range] over segmented sittings: 問題1 6.1 [4.3–6.9],
問題2 9.8 [7.6–11.0], 問題3 6.5 [4.6–9.2], 問題4 6.3 [4.6–8.0], 問題5 5.1
[2.6–6.2] min, measured from a section's first answer pause to the end of its
last.

---

## 6. Coverage — what was measured and what was not

Loudness, true peak, LRA, runtime, speech time, narrator F0 and speech rate:
**all 31 files**, no failures — every recording decoded cleanly.

Pause/section segmentation: **22 of 31**. The nine below are reported
unavailable rather than estimated, because a fabricated pause constant
silently mis-times every future exam. All nine are pre-2018 or duplicate a
neighbouring sitting's structure; excluding them does not move any median
(the recent-12 column in §2 agrees with the all-22 column to within 0.2 s).

| Sitting | Why it was not segmented |
|---|---|
| 2010-07, 2011-12, 2012-12, 2013-12, 2017-12, 2018-07, 2024-07 | 8–9 answer pauses attributed to 問題2 — an extra structural pause inside the option-reading run that the shape rules cannot safely assign |
| 2012-07 | densest item run is only 5 — no 問題4 signature (36.9 min, the most heavily edited copy in the archive) |
| 2022-12 | only 3 pauses in 問題1's answer class |

---

## 7. Reproducing this

The measurement scripts are not committed (they are one-shot analysis, and the
inputs are 2 GB of `refs/` audio). The pipeline is four steps and is fully
described above; the operative parameters are:

```
decode      ffmpeg -ac 1 -ar 16000 -f s16le          (20 ms RMS frames for pauses,
                                                      10 ms for nuclei/F0)
loudness    ffmpeg -af loudnorm=I=-15:TP=-1.0:LRA=11:print_format=json -f null -
pauses      core -60 dBFS (>=0.30 s) extended to min(-25, LUFS-8) dBFS
turn gaps   F0 by autocorrelation, 0.6 s either side, speaker change at >15 % Δ
nuclei      2 dB dip criterion, peak floor 22 dB below the 95th pct speech level
```
