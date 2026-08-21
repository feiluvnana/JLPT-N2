---
name: choukai-audio
description: Single owner of the listening audio end to end — the TTS script 聴解スクリプト.txt whose block conventions the timing engine parses, MP3 synthesis via scripts/make_choukai_mp3.py with official pacing, voices, and loudness, and the method for measuring official JLPT audio in refs/ to calibrate that pacing. Use whenever creating or editing the listening script or narration text, whenever generating, fixing, or tuning the listening MP3 (voices sounding wrong, rushed pacing, missing answer pauses), and whenever an official or sample choukai MP3 needs analysis ("learn from this audio") or pacing needs calibration or verification. Do not write ad-hoc TTS loops — use scripts/make_choukai_mp3.py.
---

# Choukai Audio (script → synthesis → calibration)

## Executable & File Paths

- **Generator**: `.agents/choukai-audio/scripts/make_choukai_mp3.py`
- **Input**: `tests/<test_id>/聴解スクリプト.txt` — **always this name**
  (`script.txt` is only a legacy no-argument fallback).
- **Output**: `tests/<test_id>/聴解.mp3` + per-question files in `segments/`.
- **Chapters**: `tests/<test_id>/聴解_チャプター.json` — start offset of every
  問題 and 例/N番 item, accumulated by the assembler (exact by construction;
  never recover via `silencedetect`). Consumed by `exam-app` (chapter
  dropdown); regenerate the MP3 to refresh. Carries `"script_sha"` and
  `"pacing_sha"`.
- **Measured pacing evidence**: `references/official_pacing.md`.
- **Measured REGISTER evidence**: `references/official_register.md` — the
  countable difference between official and generated dialogue (reaction
  density, fillers, how a wrong option gets killed, 問題4 reply shapes). Read
  it before writing any dialogue; Part 1's register section is its enforcement.

---

# Part 1 — The script file format

## Content rule: official narration ONLY

The file contains exactly what the announcer and voice actors say — no
headers, usage notes, or markers. Required elements (`jlpt-exam-structure`
owns the exact announcer lines): opening → per-section instruction →
「では、練習しましょう。」→ 例 → 「最もよいものは◯番です。…では、始めます。」→
items → … → 「これで、聴解試験を終わります。」 (問題5: 「この問題には練習はありません。」)

### TTS spelling: level is `Nに`, never `N2`

Edge-TTS reads digit `2` as English "two", so `聴解スクリプト.txt` spells the
level **`Nに`**:

```
Nに聴解。これから、Nにの聴解試験を始めます。問題用紙にメモをとってもかまいません。
```

(Booklet HTML may still say `N2` — that is print, not TTS.)
`validate_script()`'s `OPENING` substring is `これから、Nにの聴解試験を始めます`.

Cross-check tone, turn length, and distractor flow against the official script
PDFs in `refs/JLPT_N2_NEW/` (`AGENTS.md` §3): 3–5 exchanges for 問題1/2,
monologues for 問題3, rapid single turn for 問題4. **NO FURIGANA** — plain
text, no `<ruby>`; furigana belongs only in the booklet HTML.

### No sound effects — official recordings are dialogue-only (checked 2026-08-18)

Do not add chimes, bells, or ambient noise to `聴解.mp3`. Checked, not
assumed: all 31 `refs/JLPT_N2_NEW/*/script.md` extracts carry zero SFX/chime
notations, and the `audio_inspection.md` measurement files show nothing
consistent with a mixed-in effect. Official N2 choukai audio is the announcer
plus voice actors and nothing else, in all 31 sittings. **Adding SFX would be
a fidelity regression** — the synthesis pipeline (per-line TTS →
`shape_pauses()` → concat → one `loudnorm` pass) has no mixing stage and none
should be added.

## Register: write people talking, not a template being filled

**Evidence and inventories: `references/official_register.md`.** Read it
before the first line of dialogue.

| | Official | Generated papers (pre-rule) |
|---|---|---|
| turns that are short reactions (≤12 chars) | **18 %** | 6 % |
| turns opening with a filler/reaction | **35 %** | 18 % |
| hesitation tokens per paper | **median 27, band 9–48** | 0–4 |
| flat contradiction 「〜ではありません」 per 10k chars | **0.4** | 17.1 |
| 縮約形 per 10k chars | **37.3 [22.4–67.4]**, 31/31 sittings | 0.0–23.9 |

Seven binding rules. Not style advice — a paper that fails them is solvable
by pattern, or stops testing a skill the exam tests:

1. **Every item gets reaction turns** — aim for roughly one short reaction in
   five (also what makes the audio breathe: each is a 0.9 s turn gap, Part 3).
2. **Hesitation has a CEILING, not just a floor.** Use 「あのう」「えーと」
   「うーん」「まあ」「あ、」 where a real speaker would stall — never in the
   announcer's lines (read text). Official measures **27 per paper [9–48]**
   (`official_register.md` §7.1); over the ceiling reads as performed
   hesitancy. The actual deficit is elsewhere: official runs うん 11.3/paper
   vs our 4.2, あ、12.9 vs our 22.5 — **spend the budget on the OTHER speaker
   acknowledging, not the current speaker stalling.**
3. **Contract the verbs — 縮約形 is a TESTED skill** (Shin Kanzen 実力養成編
   p.16, 「音の変化や縮約形」): write 〜てる/〜とく/〜ちゃう/〜なきゃ/〜てく/〜ちゃ,
   never 〜ている/〜ておく/〜てしまう/〜なければ/〜ていく/〜では. Official runs
   22.4–67.4 per 10k spoken chars (median 37.3) in 31/31 sittings; keigo is
   not an excuse — official service-role items still measure 37.5. Keep them
   out of the ANNOUNCER's lines, same carve-out as fillers.
4. **Match the register to the relationship, and hold it.** Casual (うん /
   〜だけど / 〜かな) for students/family/close colleagues; keigo (はい / ええ /
   承知しました) at a counter or to a 部長. One speaker must not drift mid-item.
5. **Kill a wrong option the way official does**: **reassign** it to a named
   third party, **defer** it (その前に / 後回しになってました), **refuse** it
   (難しい / 無理 / 見送), or note it is **already done** (もう〜てある) — flat
   「〜ではありません」 is the last resort (0.4 vs 17.1 per 10k chars without
   this rule). Rotate the device across a section's items; the line still
   needs to be quotable in the 解説 (see `choukai-items.md`).
6. **問題1's deciding line must not always be the dialogue's last word before
   the repeated question, and must not always arrive through the same pivot — nor always first.**
   Found 2026-08-18 (`tests/20260817_2/聴解スクリプト.txt` 問題1): every one of
   its 6 items pivoted on the identical word 「それより」 straight into the
   correct action, one line before the repeated question — solvable by
   ignoring the dialogue. But banning "always last" caused the opposite
   monoculture: `20260818_1` and `20260819_1` placed 14 of 15 deciders in the
   first third (0.0–0.33) of the item. Official spreads deciders across all
   three buckets (first third, middle third, last third):
   - `16. N2 7-2025/script.md` 問題1-1番: the deciding line is the **first**
     instruction; two more turns follow (a task already claimed by the other
     speaker, then a third due next Friday) — the last-mentioned thing is not
     the answer.
   - `17.N2 12-2025/script.md` 問題1-2番: the deciding instruction sits
     **mid-turn**, immediately followed by a second, LATER instruction about
     what to do *after* — a real trailing task, not filler.
   - Rule: across a 大問, decider positions must not all fall in one third of
     their items. Spread them evenly across 冒頭 (first third), 中盤 (middle
     third), and 終盤 (last third). No more than 3 of 6 rows may share a position
     bucket in the 構成表.
7. **Some items should run a stated plan into an unexpected complication**,
   not just enumerate settled facts. Official routinely revises a plan
   mid-dialogue: `17.N2 12-2025/script.md` 問題1-5番 opens with a plan, then
   introduces genuinely NEW information mid-call
   (「締め切った後で…追加で4名認めたんです」) that forces re-prioritization;
   `16. N2 7-2025/script.md` 問題1-2番 opens flatly with a plan already changed
   by an external event (「ほかのイベントの都合で部屋を急に変更しなきゃ
   ならなくなった」). Write one or two 問題1/2 items per test where a
   first-mentioned plan (an email, a booking, an order) is complicated or
   reversed by a new fact one speaker didn't have at the start.

### Banned formulas — each one shipped, with the count that banned it

**Every band below is measured** by
`choukai_profile.service_formula_archive()` and read by the gate — the numbers
are per-paper counts over the 31 sittings, not estimates. Refresh by re-running,
never by retyping.

| Never write | Official: total / max per paper | Generated papers |
|---|---|---|
| 「Xの話ではありませんし、Yについて論じているのでもありません」 (問題3 close) | **0** | every 問題3 item |
| 「〜た方がいいですか」 (un-official probe) | **0 / 0** | 13× in 8/14 papers |
| 「かしこまりました」 transaction formula | 4× / **max 1** | **24× in 12/14 papers** |
| 「〜ていただけますか」 | 13× / max 2 | 39× in 12/14 papers |
| 「よろしいでしょうか」 | 6× / max 2 | 13× in 10/14 papers |
| 「あ、そうなんですね」 | 4× / max 2 | 36× in 8/14 papers |
| 「〜ておきましょうか」 | 1× / max 1 | 9× |
| 「わかりました。書きます。」 reused as every closing turn | 0 | reused across a section |
| 「なるほど、〜なんですね」 echo just before the answer | rare | once per 問題2 item |
| 問題4 replies opening はい / いいえ / では | **1.3 %** | over half |

**One row on this list is a FLOOR, not a ceiling.** 「そうですね」 appears
**83× across 29 of 31 sittings, median 3 per paper**, against a median of 1 in
ours: it is the human courtesy official reaches for, and the gate now WARNs when
a paper falls BELOW the archive median. The first cut of that check capped it at
1 — which would have pushed every paper further from official while reading as a
register fix. Before adding any phrase to this table, measure both directions.

**The formula is the defect, not the phrase** — a section that runs the same
opening move → probe shape → closing turn in every item is solvable by
noticing the pattern, without Japanese.

- **No two items in a section may share their opening move, probe shape, or
  closing turn.** Read only the first/last line of each item in a column —
  if they rhyme, rewrite.
- **Turn shape & ping-pong**: generated papers have drifted into short turns
  (median 27 chars vs official 38 chars) and higher turn counts (107–198 vs
  66–143). Write substantive dialogue turns rather than rapid transaction ping-pong.
- **Vary who drives.** Official 問題1 is as often an instruction-giver
  assigning tasks (「〜してくれる？」) as a customer being redirected.
- 「まず」 is the QUESTION's word (このあとまず何をしますか); inside the
  dialogue it's a crutch marking the answer. Official runs a median of **5.5
  per 10k chars, never above 19.1** (question lines removed); shipped papers
  have run 4.1–36.3. **Cap: stay under 19** — order tasks by content
  (「その前に」「〜が終わったら」) rather than by saying まず.

### NEVER reveal an answer for a scored item (exam-breaking)

`最もよいものは◯番です。` is an **例-only** line, always in the full official
form:

```
最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。最もよいものは◯番ですから、答えはこのように書きます。では、始めます。
```

- A bare `最もよいものは◯番です。` after any scored `N番。` is FORBIDDEN.
- `質問1の最もよいものは◯番です。` is FORBIDDEN anywhere; 問題5 has no 例 and
  never carries a reveal.
- **No authoring annotations** (`（※選択肢3が受付…）`) — Edge-TTS reads them
  aloud; rationale goes in 聴解.md's 解説 column.

`make_choukai_mp3.py` hard-fails on all of these before synthesizing.

## Block conventions (parser contract)

- Blocks are separated by ONE blank line. **One block = one audio unit.**
- **One turn = ONE line. Two consecutive lines may never carry the same
  speaker label.** A gap is inserted between every pair of lines
  (`turn_gap_jitter()`, median 0.9 s over a five-value ladder — Part 3
  §"Verify the pause DISTRIBUTION"); a same-speaker pause at a 。 is a within-turn
  pause instead (official median 0.40 s, p75 0.53; capped at
  `GAP_WITHIN_TURN_MAX`). Official has **0** consecutive same-label pairs in
  31 sittings — a same-speaker split turn silently inflates the reaction-turn
  rate without adding a real reaction, since **only the OTHER speaker's turn
  counts as a reaction** (`official_register.md` §7.3). To let one speaker
  pause mid-thought, write one line with a 。 in it, not two lines.
- Item blocks start with `例。` or `N番。` + situation + question ON THE SAME
  LINE: `1番。会社で女の人と男の人が話しています。…か。`
- Section markers (`問題1。`) and instruction text are each their own block.
- **EVERY item is ONE block, start to finish** — marker line through the
  repeated closing question, no blank line inside. `gap_before_line()`/
  `pause_after()` key off each block's own first line, so a stray blank line
  mid-item silently relocates the pauses (問題2's 20 s option-reading pause
  can disappear, or land before the dialogue plays). `validate_script()`
  requires every item block to contain a speaker-tagged line (or, for 問題4,
  ≥3 spoken option lines).
- 問題1/2: repeat the question as the block's last line.
- 問題3/4/5 spoken choices: one per line, `1、…。` `2、…。` (読点 after the
  digit — the parser keys on `^[1-4]、`).
- Japanese punctuation only (、。) in spoken lines — an ASCII `,`/`.`
  mis-times edge-tts's pause (`?` is fine); `make check` rejects them.

## Spoken vs printed choices — do not speak the printed ones

`jlpt-exam-structure`'s "Printed in booklet" column owns this fact:

| 問題 | Choices are |
|---|---|
| 1, 2 | PRINTED in `聴解.md` — never spoken |
| 3, 4 | SPOKEN only — booklet prints nothing |
| 5, 1番 | SPOKEN only |
| 5, 2番 | **SPOKEN only** — read after 質問1, then again after 質問2 |

**問題5 prints nothing at all in this repo** — a house-rule divergence from
official (`jlpt-exam-structure` §"問題5 prints nothing" owns why). For this
file:

- **Both 問題5 items get a spoken lead-in block**, each before its `N番。`
  marker. 1番's ends 「では、始めます。」; 2番's does not (its exact text is
  `jlpt-exam-structure`'s 問題5-2番 instruction row).
- **`2番。` is followed by the SITUATION**, never the lead-in — a lead-in
  glued onto the marker line lands the block's pauses wrong. Write
  `2番。<situation>。` on its own first line.
- **The four choices are read TWICE** (after 質問1, then again after 質問2),
  all inside the one 2番 block — 12 spoken choice lines in 問題5 total (4 for
  1番 + 8 for 2番); `make check` counts them.

### 問題5 2番: read the choices in enumeration order, decide by NAME not ordinal

1. **Candidate *n* of the spoken enumeration must be spoken choice *n*.**
   Write candidates first, in introduction order; build the read-back list
   from that order, never the reverse.
2. **The deciding line names a candidate attribute — never `Nつ目`/`N番目`.**
   No 問題5 item in 31 sittings speaks an ordinal back-reference; an ordinal
   decider ties the answer to a numbered SLOT, so re-ordering the choice list
   silently re-keys the item.

**A mis-keyed 問題5-2番 is fixed HERE**: re-enumerate so the dialogue
introduces candidates in the read-back order, replace any ordinal decider
with the candidate's name, then `make mp3 <test_id>`. `check_mondai5_enumeration()`
fails both rules; `check_mondai5_prints_nothing()` fails a booklet printing
options under 問題5.

## Instructions are copied, not re-worded

The 問題N instruction must be **character-for-character** the one in `聴解.md`
(the script adds only 「では、練習しましょう。」) — take the canonical text from
`jlpt-exam-structure` §"問題N instruction lines" and paste it into both files.
The gate compares booklet against SCRIPT, not official wording, so both
drifting the same way still passes green.

## The 例 must be answerable, and its announced number must be the answer

`最もよいものは◯番です。` names a number in the BOOKLET's 例 option list — the
two are one item split across two files. Avoid an unanswerable 例 where the
printed options answer a different question than the one asked; read the
printed options against the spoken 例 and confirm the announced number is
what the dialogue supports — `make check` cannot.

## The 問題 decides the QUESTION TYPE, not just the topic

| 問題 | Task | Question shape | Shape of the item |
|---|---|---|---|
| 1 | 課題理解 | 〜は、このあとまず何をしますか | a conversation where one person must ACT |
| 2 | ポイント理解 | どうして〜か / 何が一番〜か / どのように | conversation or monologue, no action required |
| 3 | 概要理解 | 〜は何について話していますか | monologue, gist only |

## The keyed option must be quotable, and every other option denied

**Construction order is binding: this file comes FIRST; `聴解.md`'s options are
harvested out of it.** Never write an option with no line in the script —
that bends the dialogue to fit three guesses and not the fourth.

Every wrong option must be traceable to a line in this file — a candidate the
dialogue *raises* and then reassigns, supersedes, or denies. The writer
records the grounding in `聴解.md`'s 解説 cell, one line per wrong option, in
the `N ✗「script line as spoken」→ reason` format `question-authoring` defines.
If a wrong option has no quotable line, fix it HERE: add the line that raises
and kills it, or replace the option. `make check`'s token-overlap check is a
**WARN only** (it flags official paraphrases too); the grounding lines are the
real check. Three critical rules: the keyed action must name the right party
(not just the right task); a second TRUE statement is a second answer, so
deny each distractor explicitly; a 理由 item is keyed to the CAUSE, not the
measure taken about it.

## Required structure — every element is mandatory

A full N2 script is **exactly 33 item blocks** (`例。`/`N番。`), plus 問題
headers, instructions, announcer lines and 例 confirmations. **The TOTAL
block count is not fixed** — scripts typically run 43–46 blocks, all valid;
`validate_script()` enforces the 33 item blocks and their distribution and
merely *prints* the total. Missing pieces are otherwise SILENT.
`validate_script()` enforces every row below **except the two marked (eye)**:

| Element | Rule |
|---|---|
| Opening | 「これから、Nにの聴解試験を始めます…」 must be present (never `N2`) |
| 問題1〜5 headers | `問題N。` as its own block, all five. **(eye)** for own-block-ness/order — code only tests the substring occurs |
| 問題1〜4 practice | instruction ending 「では、練習しましょう。」 → ONE `例。` → ONE full confirmation → items |
| 問題5 practice | NONE. Instruction must contain 「この問題には練習はありません。」; no `例。` block |
| 問題5 lead-ins | **TWO** blocks, each starting 「問題用紙に何も印刷されていません」 — `validate_script()` counts exactly 2. Do **not** merge into one combined line |
| Item counts (incl. 例) | 問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2 |
| Closing | file must END with 「これで、聴解試験を終わります。」 |
| Answer reveals | 例 confirmations only |
| Annotations | none (`（※…）`) |
| Typo guard | 「問題用紙になに印刷」 → must be 「何も印刷」 |
| 質問1/質問2 | must sit in the SAME block |
| Speaker labels | every label must exist in `SPEAKER_MAP` |

問題5 has 2 item blocks but 3 answers — its 2番 carries 質問1 and 質問2.

## Speaker labels

Dialogue lines: `男:` `女:` `男1:` `男2:` `夫:` `妻:` `学生:` `先生:` `店員:`
`医者:` `部長:` `店長:` `専門家:` `レポーター:` `教室の人:` `職員:` `係員:`
`担当者:` `講師:` `アナウンス:` `アナウンサー:` `教授:` `FP:`
plus gendered role pairs:
`男性職員:` `女性職員:` `男性係員:` `女性係員:` `男性担当者:` `女性担当者:`
`男性講師:` `女性講師:` `男性専門家:` `女性専門家:` `男性店員:` `女性店員:`
`男性医者:` `女性医者:` `男性アナウンサー:` `女性アナウンサー:`
— half or full-width colon. Unlabeled lines = narrator. **An unmapped label does not
error at synthesis — it silently falls through to the narrator voice.**
`validate_script()` rejects any label missing from the map; add it to
`SPEAKER_MAP` *before* using it, choosing a voice that contrasts with the
other speaker in that item (Part 2). Check by eye for mojibake, stray
Latin/Cyrillic, and wrong speaker attribution in 例 dialogues — the
adversarial pass is `exam-qa-review`'s.

---

# Part 2 — Casting: narration and `SPEAKER_MAP` are one decision

`SPEAKER_MAP` decides which voice reads a `label:` line; the narration tells
the examinee who is speaking. Nothing reconciles them — the author does:

- **A narration that states a gender must resolve to a voice of that
  gender.** 「〜の男の人」→`MALE` (Keita); 「〜の女の人」→`FEMALE` (Nanami).
  Use gendered role labels (`男性職員`, `女性係員`, etc.) whenever a role speaker's
  gender is mentioned in the situation or prompt.
- **A two-party item whose two labels resolve to the SAME voice is a
  defect** — who said the deciding line is the whole task in 問題1/2/5. Cast
  one male and one female label per item; `男1`/`男2` pitch-splitting is for
  the three-person conversation only.
- **Voice balance across each 大問**: turn share between male and female voices
  should remain balanced (target 40–60% per section; gate WARNs if >70% on one
  voice, FAILs if >85%).
- **問題5 needs a three-party item.** `choukai-items.md` §統合理解 requires
  問題5-1番 to be a ≥3-speaker discussion (official has one every sitting
  since 2020). edge-tts ships exactly two ja-JP voices, so the working build
  is **two same-gender labels split by `pitch` plus one of the other
  gender** — `男1`(+18 Hz) + `男2`(−16 Hz) + `女`, or `女1`/`女2` + `男`. Do
  **not** spend `rate` on the split (moves difficulty).
- **Voice separation margin (semitones)**:
  When two same-gender speakers share an item, pitch separation is measured in semitones:
  $$\Delta\text{st} = 12 \times \left|\log_2\left(\frac{f_{\text{base}} + \Delta f_1}{f_{\text{base}} + \Delta f_2}\right)\right|$$
  where $f_{\text{base}} = 210\text{ Hz}$ for female (`NanamiNeural`) and $120\text{ Hz}$ for male (`KeitaNeural`).
  Target: **$\ge 1.9\text{ st}$**. Gate FAILs if $< 1.0\text{ st}$, and WARNs between
  $1.0$ and $1.9\text{ st}$. The FAIL edge has been hit once: `20260807_1` 問題5-2番 cast
  係員(+18 Hz) beside 妻(+16 Hz) — **0.16 st**, inaudible — repaired 2026-08-21 by moving the
  enumerator to `男性係員` (2.94 st against 夫). Why semitones and not Hz: 18 Hz on a 120 Hz
  male voice is 2.42 st and plainly audible, 20 Hz on a 210 Hz female voice is 1.57 st and
  marginal, so the old Hz rule flagged the audible pair and passed the inaudible one
  (REPORT-CHOUKAI.md §D2; the reversed precedent is noted in `qa/qa-report-20260811_1.md` §6).
- **Scan the WHOLE block for the narration, not its first line** — 問題5's
  2番 puts the situation on the block's second line.
- **Questions must name speakers unambiguously** — if a question says
  「男の学生は」, the item must contain exactly one male and one female student.

`make check` fails the gender contradiction and low pitch margin, and WARNs on single-voice pairs.
Read `SPEAKER_MAP` before writing.

## Voice model (matches the official recording)

- **Narrator/announcer = FEMALE** (`ja-JP-NanamiNeural`, rate −10 %) — the
  official announcer is female in all 31 archive recordings.
- **Identity comes from `pitch`, difficulty from `rate`.** Two same-gender
  roles are separated by `pitch` (≤20 Hz on a ~120 Hz male, ~25 Hz on a
  ~210 Hz female) while `rate` stays on its calibrated value — a rate-only
  split (男1 +4% vs 男2 −8%) is not a second person to the ear.
- **Speech rate is verified, not just chosen for contrast** — it decides
  whether the exam underestimates N2 level. Verified per Part 4 step 5:
  dialogue (±0–6%) ~378 morae/min; narrator (−10%) ~295. Re-verify any rate
  change against that step — nothing else checks speech rate.

---

# Part 3 — Synthesis (`make_choukai_mp3.py`)

## Execution

Prerequisites: `ffmpeg` on PATH and `pip install edge-tts` (free, no API key).

```bash
python .agents/choukai-audio/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
… --jobs 3             # fewer requests in flight
```

A cold build (~250 lines → ~45 min of audio) takes about a minute (lines
synthesize concurrently, `TTS_JOBS = 8`); the floor is the final `loudnorm`
encode (~35 s). On success `segments/` is deleted; `--keep-segments` keeps
per-question audio for drilling.

### One engine: edge-tts. Two paid ones were tried and rejected — do not re-run

**ElevenLabs**: every Japanese-native voice is shared-LIBRARY, a free key gets
`402 paid_plan_required` for all of them, and the 21 reachable premade ids
are English-native (accented Japanese, rejected on listen). **Gemini TTS**:
free tier allows ~10 requests/day against a ~250-line script — cannot finish
one paper (revisit only on a paid tier; prosody looked promising). edge-tts
stays because it speaks native Japanese AND always finishes. If an engine is
ever added back: use **one** engine end to end (mixed voices break every
「男の人は」 question), and **accent is an ear-only check** — no gate hears
anything.

## `script_sha`: the MP3 says which script it was built from

`聴解_チャプター.json` is
`{"script_sha": …, "pacing_sha": …, "duration": …, "chapters": […]}`.

- **`script_sha`** — first 12 hex digits of sha1 over `聴解スクリプト.txt`'s
  raw bytes (`source_sha()`): mechanical evidence the audio on disk speaks
  the script on disk. Always run `make mp3 <test_id>` when editing a script.
- **`pacing_sha`** — same 12 hex digits over every `GAP_`/`PAUSE_`/`SHAPE_`
  constant plus the source of `pause_after`/`gap_before_line`/`shape_pauses`.
  Exists because `script_sha` covers the WORDS only — a pacing constant fix
  leaves every existing MP3 stale with nothing to show it, since the
  constants aren't in the script bytes and mtimes are checkout-unstable.
  Editing a constant now means `make mp3` for **every** test, or a red gate.

`make check` recomputes both and fails on disagreement. **Never hand-edit the
sha** — the only way to make it agree is `make mp3 <test_id>`. HTML
deliverables carry the same 12-hex `<!-- src_sha: … -->` stamps.

## Pacing table (measured across 31 official sittings — do not guess new values)

Derived from `refs/JLPT_N2_NEW/` (2010-07 .. 2025-12); per-sitting tables and
method in `references/official_pacing.md`. **This is the single copy `make
check` diffs against the code** — change values here and in the code together.

| Constant | Value | Official (median [band]) | Meaning |
|---|---|---|---|
| `turn_gap_jitter()` ladder | (0.65, **0.90**, 0.90, 1.15, 1.40) s | 0.51 s [p75 0.75, p90 1.08], n=465 | between dialogue turns — **median 0.90, with a tail** |
| GAP_BETWEEN_LINES | 0.9 s | same row | the pre-jitter constant; kept as the ladder's centre and as `pacing_sha` input |
| GAP_AFTER_PRE_QUESTION | 3 s | 2.80 s [2.5–4.6], n=74 | 問1: question → conversation |
| GAP_OPTION_READING | 20 s | 20.22 s [20.19–20.81], n=139 | 問2 only: read printed options |
| GAP_BETWEEN_SPOKEN_CHOICES | 3 s | 3.10 s [2.66–3.26], n=427 | 問3/問5 spoken choices |
| GAP_BETWEEN_SPOKEN_RESPONSES | 2.2 s | 2.23 s [2.14–2.31], n=795 | 問4 only: read continuously |
| GAP_BEFORE_REPEATED_QUESTION | 3 s | 2.94 s [2.81–3.19], n=74 | 問1/問2: talk → question repeated |
| GAP_AFTER_SHITSUMON1 | 10 s | 10.0 s [7.8–12.4], n=20 | 問5: 質問1's answer time, before 質問2 |
| `WITHIN_TURN_LADDER` | (0.40, 0.40, 0.60, **0.72**) s | 0.40 s [p75 0.53, p90 0.72], n=181 | a capped pause INSIDE one turn — rungs, not one value |
| GAP_WITHIN_TURN_MAX | 0.5 s | same row | the ladder's centre; still the invariant every rung stays under the turn gap |
| SHAPE_PAUSE_FLOOR | 0.6 s | threshold, not measured | only pauses above this are capped |
| ANSWER_PAUSE | 問1/2: 12 s, 問3/4: 8 s, 問5: 10 s | 12.2 s / 8.3 s / 8.3–12.3 s | after each item block |

Every value is inside the measured band, unmoved in 15 years (|r| ≤ 0.22
against sitting year). Loudness target: **−15 LUFS, −1.0 dBTP** (official
median −15.01 [−15.5, −14.3], n=31).

### Verify the pause DISTRIBUTION, not the median (F8)

Every constant above sat inside its measured band while the rendered audio was
still wrong, because a median says nothing about shape. Measured with
`silencedetect=noise=-35dB:d=0.30` over sub-2 s silences (longer ones are the
scripted answer pauses, not speech rhythm):

| corpus | median | p75 | p90 | in the 0.5/0.9 s spikes | > 1.05 s |
|---|---|---|---|---|---|
| ours, before the ladder (`20260819_1`) | 0.51 s | 0.92 s | 0.93 s | **60%** | **1%** |
| Shin Kanzen CD2, 17 mock tracks | 0.66 s | 1.04 s | 1.22 s | 19% | 24% |
| official 7/2025, full MP3 | 0.69 s | 1.00 s | 1.41 s | 20% | 21% |

Every turn gap was exactly `GAP_BETWEEN_LINES` and every within-turn pause was
capped at `GAP_WITHIN_TURN_MAX`, so the 1.1–1.4 s beat where a speaker thinks —
**one pause in five in both reference corpora** — did not exist in our audio at
all. `turn_gap_jitter()` restores it: a **five-value ladder indexed by
`sha1(line)[0] % 5`**, so a warm cache stays byte-identical to a cold build
(`make_silences()` pre-creates each value as `_sil_{s:g}.wav`, and a continuous
jitter would spawn hundreds of tiny WAVs).

**Two ladders, because the turn boundary was only half of it.**
`turn_gap_jitter()` spreads the gap BETWEEN turns; `WITHIN_TURN_LADDER` spreads
the same-speaker pause that `shape_pauses()` caps, which was the bigger half —
every internal pause above `SHAPE_PAUSE_FLOOR` used to be clamped to exactly
0.5 s. Measured on `20260807_1`: spikes 60% → 46% (turn gap only) → **18%**
(both).

**Rule:** after any pacing change, verify on the RENDERED MP3 that the two
spikes hold under 35% and the >1.05 s tail is at least 7%.
`check_choukai_pause_distribution` in `make check` does exactly that, per paper;
it is a WARN because it needs the audio and skips when it is absent. A paper
whose 聴解.mp3 predates the ladders is in `PACING_SHA_GRANDFATHERED` until
`make mp3 <id>` is re-run.

**Why 7% and not the reference corpora's 17–24%:** only a turn *boundary* may
exceed the 0.9 s gap — a within-turn pause at or above it makes one speaker
sound like two — and our papers carry ~120 boundaries against ~480 within-turn
pauses because our median turn is 27 chars against official's 37
(`official_register.md` §1). The tail is therefore capped near 9% by SCRIPT
SHAPE, and the way to lift it is fewer, longer turns, not a bigger constant
(`official_pacing.md` §6.1).

### A gap is only real if the segments around it are trimmed

Every gap is silence inserted BETWEEN segments, so it's a true gap only if
each segment starts/ends on speech. **TTS engines pad** — edge-tts writes
~0.22 s lead and ~0.85 s TAIL silence per utterance; unshaved, the measured
turn gap in shipped audio was ~2 s against a 0.9 s constant and 0.51 s
official median, and a mid-turn 。 ran ~1 s (twice official's p75).
`shape_pauses()` fixes both on 24 kHz mono samples: trim leading/trailing
silence to zero, cap internal pauses above `SHAPE_PAUSE_FLOOR` to
`GAP_WITHIN_TURN_MAX`. Pauses below the floor are left as the engine produced
them — a 促音 closure is a real ~0.1 s silence. **Verify a pacing constant on
the rendered MP3, never in the source** — a constants-only review passed this
defect on every paper it had.

### …and a constant that is never REACHED reads as correct too

Found 2026-08-13 by measuring `20260813_2`'s rendered MP3 against the archive
rather than this table. Three documented gaps were not in the audio: 問題4's
inter-reply gap fell through to `GAP_BETWEEN_LINES` (0.9 s measured, vs the
official 2.23 s — the branch was gated on `section in ("問題3","問題5")`,
excluding 問題4), the 問1/2 repeated-question gap likewise measured 0.9 s
against 2.94 s official (`GAP_AFTER_PRE_QUESTION` only applied at
`line_index == 1`, never the block's last line), and 例s were getting a full
answer pause (12 s/8 s of dead air) official never gives them. Both gaps now
have their own constant (`GAP_BETWEEN_SPOKEN_RESPONSES`,
`GAP_BEFORE_REPEATED_QUESTION`) and `pause_after()` skips the 例. **The
lesson: a review that reads the table's value, not whether the branch is
reachable, passes a constant that's never applied.** `pacing_sha` (above) now
makes a constants edit without `make mp3` a red gate instead of an invisible
defect.

Three knowing deviations from the archive: (1) 問題5's three pauses aren't
one value — official runs 1番 ≈8.3 s, 質問1→質問2 =10.0 s, final ≈11.2 s;
`ANSWER_PAUSE` is one number per 問題, so 10 s is the compromise. (2) 問題5
2番 runs longer than official because this repo speaks its four choices
twice where official prints them — do not shave a gap to buy the time back.
(3) Official reads each spoken choice as 「1、」+ ~1.1 s + text, then ~3.1 s
before the next number; we speak the whole line as one utterance, so only the
~3 s inter-choice gap is reproduced.

## Engineering rules (each fixed a real bug)

- Synthesize per line → 24 kHz mono WAV → shape pauses → concat WAVs → encode
  MP3 ONCE with `loudnorm=I=-15:TP=-1.0:LRA=11` — never concat MP3 segments
  directly. `I=-15` is the official median (replaced `I=-17`, a
  `volumedetect` mean_volume reading mistaken for LUFS — Part 4 step 1).
- **Shape each segment as soon as synthesized, before caching**, so a warm
  cache and cold build are byte-identical.
- Retry synthesis (3×, backoff); cache by hash of **text + voice + rate +
  pitch**, never line position — position-keying let a reworded line or
  remapped speaker silently reuse old audio.
- **Parse into a plan, then synthesize, then assemble** — the plan pins every
  segment path/gap up front so parallel tasks never collide.
- **Silence files are all created before block assembly begins** — lazy
  creation let two blocks write the same silence file concurrently, the
  loser getting a truncated (valid but wrong-length) gap.
- Chapter offsets stay a strictly in-order running sum even though block
  durations are measured in parallel.
- **Script validation is a hard gate** — `validate_script()` refuses to
  build on a missing 例, wrong item count, spoken-aloud answer, authoring
  annotation, or unmapped speaker label; an unmapped label otherwise falls
  through silently to the narrator voice.
- Item detection regex is `^(例。|\d+番。)` — WITH the 。, so a spoken choice
  「1、…」 is never mistaken for an item.

## Dry-run before synthesis (no network needed)

```bash
python3 -c "
import re,pathlib,importlib.util
s=importlib.util.spec_from_file_location('m','.agents/choukai-audio/scripts/make_choukai_mp3.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
b=[x.strip() for x in re.split(r'\n\s*\n', pathlib.Path('tests/<test_id>/聴解スクリプト.txt').read_text(encoding='utf-8')) if x.strip()]
m.validate_script(b)"
```

Expected pause counts, from `ANSWER_PAUSE` and the 33 item blocks (例 incl.):

| Pause | Count | Source |
|---|---|---|
| 12 s answer | 11 | 問題1 (5) + 問題2 (6), 例 excluded |
| 8 s answer | 16 | 問題3 (5) + 問題4 (11), 例 excluded |
| 10 s answer | 2 | 問題5 |
| 20 s option-reading | 7 | 問題2 only (例+6) |

**One answer pause per SCORED item** — an 例 gets the short instruction pause
instead, since official runs it straight into the confirmation. `make check`
derives this table from `EXPECTED_ITEMS`/`ANSWER_PAUSE` minus one 例 per
section in `NEEDS_EXAMPLE`.

**Open ±1 against the archive**: official measures one MORE pause than this
table in each of the 12s/8s bands (`official_pacing.md`'s histogram note) —
corroboration of something not yet identified, not a constant to match. Do
not restore an 例 pause to force 12/17 without first locating where that
extra pause sits. Estimated runtime ≈40–45 min; official's 36.6–52.1 min
(median 43.3) is **not a calibration target** — it varies with content, not
pacing.

---

# Part 4 — Calibration: measuring official audio

**The answer is already measured — read `references/official_pacing.md`
first.** Re-measure only to check a specific claim or after adding
recordings — never re-derive from one file (how three wrong numbers once got
in: runtime "~50–52 min", `GAP_BETWEEN_LINES` 1.3 s, loudness −17).

Corpus: `refs/JLPT_N2_NEW/<n>. N2 <M>-<YYYY>/…mp3` — 31 sittings, every one
except the cancelled July 2020. **Never add a second audio folder** (a
duplicate once double-weighted the last three years). Script PDFs are scans
(no transcript for mora counts); Shinkanzen CD tracks are weaker evidence.

**Shin Kanzen DOES have a script, and it is extracted.** The 別冊
「解答とスクリプト」 is bound into `Shin_Kanzen_Masuta_N2-Choukai.pdf` and carries
a complete 模擬試験 paper plus every practice dialogue — cleanly typeset, not an
OCR of a stencil. `make extract-shinkanzen` writes it to
`refs/Shinkanzen/choukai_script.md`. Use it for **register and rhythm** (the
音の変化・縮約形 and 間接的な答え方 chapters sit beside it) and its mock tracks for
pause distribution (`official_pacing.md` §6.1). It is **secondary evidence**: a
textbook corroborates shape, family and register, and never sets a count or a
length the 31-sitting archive can set instead (`AGENTS.md` §3).
Five steps (full commands in the reference, §1):

1. **Basics** — `ffprobe` for duration/bitrate; loudness via
   `ffmpeg -af loudnorm=...:print_format=json`. **Never `volumedetect`** —
   `mean_volume` is ~4 dB below the gated K-weighted figure.
2. **Long-pause histogram** — `silencedetect=noise=-35dB:d=2.5`; buckets ~3s
   structural / ~8s answer 問3・4 / ~12s answer 問1・2 / ~20s 問2 option-reading.
   A fixed threshold isn't comparable across sittings (some lay a soft
   ~−34dBFS marker tone over the last ~2.5s of an answer pause) — cross-check
   at −30dB or use the reference's two-threshold envelope method.
3. **Timeline attribution** — read ordered (start, duration) pairs: `20s →
   talk → 12s` repeating = 問2; `3s,3s,3s,8s` = 問3/5 spoken choices; a dense
   run of lone 8s pauses = 問4 (read continuously); `10s` then `12s` at the
   end = 問5's 質問1/質問2.
4. **Turn gaps** — `silencedetect` can't see them (room tone, not digital
   silence); diarize by median F0 either side of each sub-threshold gap
   (465 boundaries: speaker-change median 0.51 s, p75 0.75, p90 1.08).
5. **Speech rate** — morae/min via syllable-nuclei detection (2 dB dip
   criterion), same detector both sides. Official: 250–281 nuclei/min, median
   271; our builds 270.6–279.7 (inside the band, at its top). N2 is not N1 —
   do not push rates toward a natural-speed figure.

Deliverable: an updated pacing table in Part 3 plus the evidence mirrored
into `references/official_pacing.md` — table and code first, then mirror.
