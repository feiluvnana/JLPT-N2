---
name: choukai-audio
description: Single owner of the listening audio end to end — the TTS script 聴解スクリプト.txt whose block conventions the timing engine parses, MP3 synthesis via scripts/make_choukai_mp3.py with official pacing, voices, and loudness, and the method for measuring official JLPT audio in refs/ to calibrate that pacing. Use whenever creating or editing the listening script or narration text, whenever generating, fixing, or tuning the listening MP3 (voices sounding wrong, rushed pacing, missing answer pauses), and whenever an official or sample choukai MP3 needs analysis ("learn from this audio") or pacing needs calibration or verification. Do not write ad-hoc TTS loops — use scripts/make_choukai_mp3.py.
---

# Choukai Audio (script → synthesis → calibration)

## Executable & File Paths

- **Generator**: `.agents/choukai-audio/scripts/make_choukai_mp3.py`
- **Input**: `tests/<test_id>/聴解スクリプト.txt` — **always this name**
  (Japanese-file-names invariant; what `make mp3 <test_id>` passes).
  `script.txt` is only a legacy no-argument fallback in the generator.
- **Output**: `tests/<test_id>/聴解.mp3` + per-question files in `segments/`.
- **Chapters**: `tests/<test_id>/聴解_チャプター.json` — start offset of every
  問題 and 例/N番 item, accumulated by the assembler (exact by construction;
  never recover via `silencedetect`). Consumed by `exam-app`
  (chapter dropdown); regenerate the MP3 to refresh. Carries `"script_sha"`.
- **Measured pacing evidence**: `references/official_pacing.md` (this folder).
- **Measured REGISTER evidence**: `references/official_register.md` — the
  countable difference between official dialogue and generated dialogue
  (reaction density,
  fillers, how a wrong option gets killed, 問題4 reply shapes). Read it before
  writing any dialogue; Part 1's register section is its enforcement.

---

# Part 1 — The script file format

## Content rule: official narration ONLY

The file contains exactly what the announcer and voice actors say — no
headers, usage notes, or markers. Required elements (jlpt-exam-structure owns
the exact announcer lines): opening → per-section instruction →
「では、練習しましょう。」→ 例 → 「最もよいものは◯番です。…では、始めます。」→
items → … → 「これで、聴解試験を終わります。」 (問題5: 「この問題には練習はありません。」)

### TTS spelling: level is `Nに`, never `N2`

In `聴解スクリプト.txt` only, spell the exam level as **`Nに`** (not `N2`).
Edge-TTS reads digit `2` as English "two" / awkward Latin, so the opening must
be:

```
Nに聴解。これから、Nにの聴解試験を始めます。問題用紙にメモをとってもかまいません。
```

(Booklet titles in `聴解.md` / HTML may still say `N2` — that is print, not
TTS.) `validate_script()`'s `OPENING` substring is `これから、Nにの聴解試験を始めます`.
Never write `N2` anywhere in the TTS script.

Cross-check tone, turn length, announcer wording, and distractor flow against
the official script PDFs in `refs/JLPT_N2_NEW/` (paths in **`AGENTS.md` §3**):
3–5 exchanges for 問題1/2, monologues for 問題3, rapid single turn for 問題4.
**NO FURIGANA** — clean plain text, no `<ruby>` tags; furigana belongs only
in the booklet HTML.

## Register: write people talking, not a template being filled

**Evidence and inventories: `references/official_register.md`.** Read it before
the first line of dialogue. The four numbers that matter — the official archive
against generated papers written without this section:

| | Official | Generated papers | 
|---|---|---|
| turns that are short reactions (≤12 chars: 「はい。」「そうですか。」「うん。」) | **18 %** | 6 % |
| turns opening with a filler/reaction (はい・うん・ああ・ええ・あの・うーん・へえ・でも…) | **35 %** | 18 % |
| hesitation tokens per paper (あのう/えー/えっと/うーん/まあ) | **median 41**, in 31/31 sittings | 0–4 |
| flat contradiction 「〜ではありません」 per 10 k chars | **0.4** | 17.1 |

Four binding rules follow. They are not style advice: a paper that fails them
is solvable by pattern, which is a content defect.

1. **Every item gets reaction turns.** Aim for the official rate — roughly one
   short reaction turn in five. They are also what makes the audio breathe:
   each one is a 0.9 s turn gap (Part 3), which is half the answer to "the
   audio just talks without stopping".
2. **Hesitation is normal speech.** Use 「あのう」「えーと」「うーん」「まあ」
   「あ、」 where a real speaker would stall — asking a stranger a favour,
   weighing two options, being corrected. Zero fillers in a 45-minute recording
   is the single loudest tell that no human wrote it. Keep them OUT of the
   announcer's lines: the 問題N instructions and 例 confirmations are read text.
3. **Match the register to the relationship, and hold it.** Casual
   (うん / 〜だけど / 〜かな / 〜じゃない) for students, family, close
   colleagues; keigo (はい / ええ / 承知しました / おっしゃる) at a counter, to a
   部長, from a 医者. One speaker must not drift between them mid-item.
4. **Kill a wrong option the way official does.** Official order of preference
   is **reassign** it to a named third party, **defer** it (その前に / 先に /
   あとで / 後回しになってました), **refuse** it (難しい / 無理 / 見送), or note
   it is **already done** (もう〜てある) — flat 「〜ではありません」 is the last
   resort, 0.4 per 10 k chars — papers written without this rule have used it
   over forty times as often. Rotate the device
   across the items of a section; the grounding line still has to be quotable
   in the 解説 cell (see below), which reassignment and deferral satisfy.

### Banned formulas — each one shipped, with the count that banned it

| Never write | Official / 31 sittings | Generated papers |
|---|---|---|
| 「Xの話ではありませんし、Yについて論じているのでもありません。Zを取り上げているわけでもありません」 (問題3 close) | **0** | every 問題3 item |
| 「〜た方がいいですか」 as the examinee's every probe | 0 | every 問題1 probe |
| 「かしこまりました」 opening every service reply | 4 in 31 sittings | every service reply |
| 「わかりました。書きます。」 (or any identical closing turn reused) | 0 | reused across a section |
| 「なるほど、〜なんですね」 echo just before the answer | rare | once per 問題2 item |
| 問題4 replies opening はい / いいえ / では | **1.3 %** of replies | **over half** |

**The formula is the defect, not the phrase.** A 問題1 section has shipped
running 「すみません、〜んですが」→「かしこまりました。まず〜」→ two
「〜た方がいいですか」 probes, each refused →「まずは〜をお願いします」→
「わかりました。書きます。」 in **every one of its items**: a candidate who notices
that the last refused suggestion is never the answer scores the section without
Japanese. So:

- **No two items in a section may share their opening move, their probe shape,
  or their closing turn.** Write the section, then read only the first and last
  line of each item in a column — if they rhyme, rewrite.
- **Vary who drives.** Official 問題1 is as often 「an instruction giver assigns
  tasks」 (「〜してくれる？」) as 「a customer asks and is redirected」.
- 「まず」 is the 問題1 QUESTION's word (このあとまず何をしますか). Inside the
  dialogue it is a crutch: official uses it 5.6 per 10 k chars, and generated
  papers have run six times that.

### NEVER reveal an answer for a scored item (exam-breaking)

`最もよいものは◯番です。` is an **例-only** line, appearing ONLY inside the
例 confirmation of 問題1〜問題4, always in this full official form:

```
最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。最もよいものは◯番ですから、答えはこのように書きます。では、始めます。
```

- A bare `最もよいものは◯番です。` after `1番。`〜`12番。` is FORBIDDEN — it
  speaks the answer aloud (avoid speaking the answer aloud on scored items).
- `質問1の最もよいものは◯番です。` / `質問2の…` are FORBIDDEN anywhere. 問題5
  has no 例 and never carries a reveal or confirmation line; 問題1〜4 each get
  exactly one, after the 例. Answers live in the key tables of `聴解.md`.
- **No authoring annotations** (`（※選択肢3が受付…）` etc.) — Edge-TTS reads
  them aloud; rationale goes in the 解説 column of `聴解.md`.

`make_choukai_mp3.py` hard-fails on all of these before synthesizing.

## Block conventions (parser contract)

- Blocks are separated by ONE blank line. **One block = one audio unit.**
- Item blocks start with `例。` or `N番。` + situation + question ON THE SAME
  LINE: `1番。会社で女の人と男の人が話しています。…か。`
- Section markers (`問題1。`, with 。) and instruction text (問題1では、…) are
  each their own block.
- **EVERY item must be ONE block, start to finish**: marker line, all
  dialogue/monologue turns (for 問題4, all spoken options), and the repeated
  closing question, NO blank line inside. `gap_before_line()`/`pause_after()`
  key off each block's OWN first line, so a stray blank line mid-item silently
  relocates the pauses — 問題2's 20-second option-reading pause disappears and
  the ANSWER-TIME pause lands **before the dialogue has even played** (avoid stray
  blank lines mid-item). `validate_script()` requires every item
  block to contain a speaker-tagged line (問題1/2/3/5 — a monologue's own
  speech is tagged too, e.g. 専門家:) or, for 問題4, ≥3 spoken option lines.
- 問題1/2: repeat the question as the block's last line.
- 問題3/4/5 spoken choices: one per line, `1、…。` `2、…。` (読点 after the
  digit — the parser and pacing engine key on `^[1-4]、`).
- Japanese punctuation only: 、and 。 — an ASCII `,` or `.` in a spoken line
  makes edge-tts mis-time the pause (`?` is fine); `make check` rejects them.

## Spoken vs printed choices — do not speak the printed ones

jlpt-exam-structure's "Printed in booklet" column decides this (it owns the
問題5-2番 printed-options format facts and official evidence — defer to it):

| 問題 | Choices are |
|---|---|
| 1, 2 | PRINTED in `聴解.md` — never spoken |
| 3, 4 | SPOKEN only — booklet prints nothing |
| 5, 1番 | SPOKEN only |
| 5, 2番 | **SPOKEN only** — read after 質問1, then again after 質問2 |

**問題5 prints nothing at all in this repo**, so every one of its choices is
spoken. That is a house rule diverging from official (which prints 2番's four
options and reads none); `jlpt-exam-structure` §"問題5 prints nothing" owns it,
including what official does and why the divergence was accepted. What it means
for this file:

- **Both items get a spoken lead-in block, each before its `N番。` marker.**
  1番's ends 「では、始めます。」; 2番's does not. 2番's text is the
  `jlpt-exam-structure` instruction-line table's 問題5 2番 row, verbatim —
  「問題用紙に何も印刷されていません。まず話を聞いてください。それから、二つの質問と
  せんたくしを聞いて、それぞれ1から4の中から、最もよいものを一つ選んでください。」
- **`2番。` is followed by the SITUATION**, never by the lead-in — a lead-in
  glued onto the marker line gets read as part of the situation and lands the
  block's pauses wrong. Write `2番。<situation>。` on its own first line.
  (Official's model line is `2番。ラジオを聞いて男の人と女の人が話しています。`;
  under official rules 2番 got no lead-in at all, and all four generated papers
  broke *that* asymmetry by speaking the instruction from the marker line. The
  lead-in is now correct to speak — from its own block.)
- **The four choices are read TWICE**, `1、…。`〜`4、…。` after 質問1 and the same
  four after 質問2, all inside the one 2番 block. 12 spoken choice lines in
  問題5 total (4 for 1番 + 8 for 2番); `make check` counts them.

### 問題5 2番: read the choices in enumeration order, and decide by NAME, not by ordinal

Two rules (evidence owned by `jlpt-exam-structure` §"問題5 prints nothing"):

1. **Candidate *n* of the spoken enumeration must be spoken choice *n*.**
   Write the candidates first, in introduction order; build the read-back list
   from that order — never the reverse.
2. **The deciding line names a candidate attribute — never `Nつ目`/`N番目`.**
   In 31 sittings no 問題5 item speaks an ordinal back-reference.

An ordinal decider ties the answer to a numbered SLOT: re-ordering the choice
list silently re-keys the item, leaving two defensible answers. **A mis-keyed
問題5 2番 is fixed HERE**: re-enumerate so the dialogue introduces candidates in
the read-back order, replace any ordinal decider with the candidate's name, then
`make mp3 <test_id>`. Both halves being in one file removes the old booklet/audio
desync but not the defect — one edit to the read-back list still re-keys an item
whose dialogue decides by ordinal. `check_mondai5_enumeration()` fails both
rules; `check_mondai5_prints_nothing()` fails a booklet that prints an option
list under 問題5.

## Instructions are copied, not re-worded

The 問題N instruction must be **character-for-character** the one in `聴解.md`
(the script adds only 「では、練習しましょう。」); avoid drifting instruction wording between files. Take the canonical text from **`jlpt-exam-structure` §"問題N
instruction lines"** and paste it into both files — the gate compares booklet
against SCRIPT, not official wording, so both drifting the same way passes
green. Copy from that section.

## The 例 must be answerable, and its announced number must be the answer

`最もよいものは◯番です。` names a number in the BOOKLET's 例 option list, so the
two are one item split across two files (the 例 format fact belongs to
`jlpt-exam-structure`; the script consequence is this rule). Avoid unanswerable 例 items where options answer a different question
(e.g., asking 「このあとまず何をしますか」 against printed options answering a different question). Read
the printed options against the spoken 例 and its question, and confirm the
announced number is the option the dialogue supports — `make check` cannot.

## The 問題 decides the QUESTION TYPE, not just the topic

`tests/<test_id>/test_spec.json` hands you scenarios, not an assignment of
scenarios to 問題. The section's task type binds:

| 問題 | Task | Question shape | Shape of the item |
|---|---|---|---|
| 1 | 課題理解 | 〜は、このあとまず何をしますか | a conversation where one person must ACT |
| 2 | ポイント理解 | どうして〜か / 何が一番〜か / どのように説明していますか | conversation or monologue, no action required |
| 3 | 概要理解 | 〜は何について話していますか | monologue, gist only |

Ensure question types match section definitions (課題理解 vs ポイント理解 vs 概要理解) and options are ordered to match answer position specifications.

## The keyed option must be quotable, and every other option denied

**Construction order is binding: this file comes FIRST; the option sets in
`聴解.md` are harvested out of it.** Never write an option that has no line in
the script yet — an option set drafted first is a set of guesses, and the
dialogue gets bent to fit three of them and not the fourth. **Avoid shipping 聴解 options nobody says.**

Every wrong option must be **traceable to a line this file contains** — a
candidate the dialogue *raises* and then **reassigns**, **supersedes**, or
**denies** outright; never-mentioned plausible things are noise. The script
writer must record the grounding in the 解説 cell of `聴解.md`, one line per
wrong option, in exactly the `N ✗「script line as spoken」→ reason` format
that **`question-authoring`** defines and mandates. If a wrong option has no
quotable line, the fix is in THIS file: add the line that raises and kills it,
or replace the option. `make check`'s token-overlap check is a **WARN only**
(it flags official paraphrases too); the grounding lines are the real check —
their absence means the item is not shippable. Three critical rules:

- **Quotable.** 問題1-5番 keyed 「点検作業員に車移動の連絡をする」 while the
  script says 「事前に管理事務所へご連絡の上」 — the keyed action named the
  wrong party. Copy the deciding line into the 解説 cell; if you cannot, the
  item is wrong (`make check` WARNS on a 解説 quote nowhere in the script).
- **Denied.** A second TRUE statement is a second answer (問題2-6番): give
  each distractor its own denial line.
- **A 理由 question is keyed to the CAUSE, not the measure** (問題2-4番 keyed
  what was DONE about 運転手不足, not the cause itself).

## Required structure — every element is mandatory

A full N2 script is **exactly 33 item blocks** (`例。`/`N番。`) in the counts
below, plus 問題 headers, instructions, announcer lines and 例 confirmations.
**The TOTAL block count is not fixed** — scripts on disk typically run **43–46
blocks** — all valid; the difference is only
how instruction and announcer text is split, so do not treat any total as a
target: `validate_script()` enforces the 33 item blocks and their distribution
and merely *prints* the total. Missing pieces are otherwise SILENT — ensure every section includes its required 例.
`validate_script()` enforces every row below **except the two marked (eye)**:

| Element | Rule |
|---|---|
| Opening | 「これから、Nにの聴解試験を始めます…」 must be present (TTS spelling — never `N2`; see above) |
| 問題1〜5 headers | `問題N。` as its own block, all five. **(eye)** for own-block-ness and order — the code only tests the substring occurs |
| 問題1〜4 practice | each: instruction ending 「では、練習しましょう。」 → ONE `例。` item → ONE full confirmation line → items |
| 問題5 practice | NONE. Instruction must contain 「この問題には練習はありません。」; no `例。` block |
| 問題5 lead-ins | **TWO** blocks, each between the instruction/previous item and its own `N番。` marker, both starting 「問題用紙に何も印刷されていません」 — `validate_script()` counts exactly 2. 1番: 「…まず話を聞いてください。それから、質問とせんたくしを聞いて、1から4の中から、最もよいものを一つ選んでください。では、始めます。」 2番: 「…まず話を聞いてください。それから、二つの質問とせんたくしを聞いて、それぞれ1から4の中から、最もよいものを一つ選んでください。」 (no 「では、始めます。」). Do **not** merge them into a combined 「1番、2番。問題用紙に何も印刷されていません」 line — no official paper has it, and `ITEM_RE` would then mis-detect the item |
| Item counts (incl. 例) | 問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2 |
| Closing | file must END with 「これで、聴解試験を終わります。」 |
| Answer reveals | 例 confirmations only — see the section above |
| Annotations | none (`（※…）`) |
| Typo guard | 「問題用紙になに印刷」 → must be 「何も印刷」 |
| 質問1/質問2 | must sit in the SAME block |
| Speaker labels | every label must exist in `SPEAKER_MAP` |

問題5 has 2 item blocks but 3 answers — its 2番 carries 質問1 and 質問2.

## Speaker labels

Dialogue lines: `男:` `女:` `男1:` `男2:` `夫:` `妻:` `学生:` `先生:` `店員:`
`医者:` `部長:` `店長:` `専門家:` `レポーター:` `教室の人:` `職員:` `係員:`
`担当者:` `講師:` `アナウンス:` `アナウンサー:` `教授:` `FP:` — half or
full-width colon. Unlabeled lines = narrator. **An unmapped label does not
error at synthesis time — it silently falls through to the narrator voice.** `validate_script()` now rejects
any label missing from the map; add it to `SPEAKER_MAP` *before* using it,
choosing a voice that contrasts with the other speaker in that item's
narration (Part 2). Check by eye for mojibake (`�`), stray Latin/Cyrillic
words, and wrong speaker attribution inside 例 dialogues; the adversarial QA
pass of the finished section is owned by **`exam-qa-review`**.

---

# Part 2 — Casting: narration and `SPEAKER_MAP` are one decision

`SPEAKER_MAP` decides which voice reads a `label:` line; the narration tells
the examinee who is speaking. Nothing reconciles them — the author does:

- **A narration that states a gender must resolve to a voice of that gender.**
  「〜の男の人」 must map to `MALE` (Keita); 「〜の女的人」 to `FEMALE` (Nanami).
  Ensure narrations specifying a gender resolve to a voice of that gender. Resolve by rewording
  the narration or picking a label whose mapping already matches; **remapping
  an existing label is a last resort** — labels are shared across tests, a
  remap silently changes every other paper's already-built audio, `script_sha`
  cannot see it (the map is not hashed), so it means `make mp3` everywhere.
- **A two-party item whose two labels resolve to the SAME voice is a defect.**
  Same `voice` a few percent of `rate` apart is not a distinguishable second
  person — who said the deciding line is the whole task in 問題1/2/5. Avoid casting both speakers of a two-party item to the same voice. Cast one male and one
  female label per item; `男1`/`男2` rate-splitting is for the three-person
  conversation only.
- **Scan the WHOLE block for the narration, not its first line.** 問題5's 2番
  puts the situation on the block's **second** line — scan the full block so gender assignments are not missed.
- **Questions must name speakers unambiguously.** If they say 「男の学生は」/
  「女の学生は」, the item must contain exactly one of each (e.g. avoiding having two male students when asking 「男の学生は」).

`make check` fails the gender contradiction and WARNs on the one-voice pair,
but the lookup belongs in authoring: read `SPEAKER_MAP` before writing.

## Voice model (matches the official recording)

`SPEAKER_MAP` is the gender contract: `make check` reads it to confirm every
「〜の男の人」/「〜の女の人」 narration resolves to a voice of that gender.

- **Narrator/announcer = FEMALE** (`ja-JP-NanamiNeural`, rate −10 %). The
  official announcer is female in all 31 archive recordings; a male narrator was
  a real user complaint.
- **Identity comes from `pitch`, difficulty from `rate`.** edge-tts ships
  exactly two ja-JP voices, so two same-gender roles are separated by `pitch`
  (≤20 Hz on a ~120 Hz male, ~25 Hz on a ~210 Hz female) while `rate` stays on
  its calibrated value. The old rate-only split (男1 +4 % vs 男2 −8 %) is not a
  second person to the ear — `check_voice_casting()` WARNed on exactly that
  pair — and spending `rate` on identity moves the paper's difficulty.
- **Speech rate is verified, not just chosen for voice contrast** — it also
  decides whether the exam underestimates N2 level. Verified per Part 4 step
  5: dialogue (±0–6%) ~378 morae/min; narrator (−10%) ~295. **Re-verify any
  rate change against that step** — nothing else checks speech rate, and a TTS
  engine change moves it as much as a `rate` edit does.

---

# Part 3 — Synthesis (`make_choukai_mp3.py`)

## Execution

Prerequisites: `ffmpeg` on PATH and `pip install edge-tts` (free, no API key).

```bash
python .agents/choukai-audio/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
… --jobs 3             # fewer requests in flight
```

A cold build (~250 lines → ~45 min of audio) takes about a minute on edge; lines
are synthesized concurrently (`TTS_JOBS = 8`). The floor is the final `loudnorm`
encode (~35 s). On success `segments/` is deleted; `--keep-segments` keeps
per-question audio for drilling.

### One engine: edge-tts. Two paid ones were tried and rejected

Do not re-run these experiments — both were implemented against real keys and
measured, and the findings are the reason the code is gone:

| Engine | Why it is not here |
|---|---|
| **ElevenLabs** | Every Japanese-native voice is a shared-LIBRARY voice, and a free key gets `402 paid_plan_required` for all of them (Morioki / Asahi / Otani, every ja voice tried). The 21 reachable premade ids are English-native, so the Japanese came out **accented** — heard in a sample and rejected by the user. Needs a Creator-tier key *and* Japanese voice ids to be worth revisiting |
| **Gemini TTS** | The free tier allows only about ten requests per DAY against a ~250-line script, so it cannot finish a single paper. Prosody and Japanese quality looked promising (native-sounding, small padding, style prompts respected and not read aloud) — revisit only on a paid tier |

edge-tts stays because it is the only engine that speaks native Japanese AND
always finishes. If an engine is ever added back, two rules from that work hold:
a build must use **one** engine end to end (a paper whose 問題1 and 問題3 differ
in voice breaks every 「男の人は」 question), and **accent is an ear-only check** —
no gate hears anything, so listen to one item before adopting it.

## `script_sha`: the MP3 says which script it was built from

`聴解_チャプター.json` is `{"script_sha": …, "duration": …, "chapters": […]}`,
where `script_sha` is the **first 12 hex digits of sha1 over the raw bytes of
`聴解スクリプト.txt`** (`source_sha()`). `make check` recomputes it and fails
on disagreement — the only mechanical evidence that the audio on disk speaks
the script on disk. Always run `make mp3 <test_id>` whenever editing a script to ensure audio and script stay in sync.

- A **content** hash, deliberately not an mtime — mtimes are checkout-unstable.
- **Never hand-edit the sha.** The only way to make it agree is `make mp3
  <test_id>`; editing the script without rebuilding in the same change is a
  defect. The HTML deliverables carry the same 12-hex `<!-- src_sha: … -->`
  stamps.

## Pacing table (measured across 31 official sittings — do not guess new values)

Derived from the whole official archive in `refs/JLPT_N2_NEW/` (2010-07 ..
2025-12); per-sitting tables and method in `references/official_pacing.md`.
**This is the single copy `make check` diffs against the code** — change
values here and in the code together.

| Constant | Value | Official (median [band]) | Meaning |
|---|---|---|---|
| GAP_BETWEEN_LINES | 0.9 s | 0.51 s [p75 0.75, p90 1.08], n=465 turns | between dialogue turns |
| GAP_AFTER_PRE_QUESTION | 3 s | 2.80 s [2.5–4.6, bimodal ≈2.8 / ≈4.1], n=74 | 問1: question → conversation |
| GAP_OPTION_READING | **20 s** | 20.22 s [20.19–20.81], n=139 | 問2 only: read printed options (most-missed pause) |
| GAP_BETWEEN_SPOKEN_CHOICES | 3 s | 3.10 s [2.66–3.26], n=427 | 問3/問5 spoken choices |
| GAP_AFTER_SHITSUMON1 | 10 s | 10.0 s [7.8–12.4], n=20 | 問5: 質問1's answer time — inserted BEFORE the 質問2 line, i.e. after 質問1's four spoken choices |
| GAP_WITHIN_TURN_MAX | 0.5 s | 0.40 s [p75 0.53, p90 0.72], n=181 same-speaker | ceiling for a pause INSIDE one turn |
| SHAPE_PAUSE_FLOOR | 0.6 s | — (threshold, not a measurement) | only pauses above this are capped |
| ANSWER_PAUSE | 問1/2: 12 s, 問3/4: 8 s, 問5: 10 s | 12.2 s / 8.3 s / 8.3–12.3 s | after each item block |

**Every value is inside the measured band, and the band has not moved in 15
years** (|r| ≤ 0.22 against sitting year). Loudness target: **−15 LUFS,
−1.0 dBTP** (official median −15.01 [−15.5, −14.3], n=31).

### A gap is only real if the segments around it are trimmed

Every gap above is silence inserted BETWEEN segments, so it is the true gap only
if each segment starts and ends on speech. **TTS engines pad**: edge-tts writes
~0.22 s of lead and ~0.85 s of TAIL silence into every utterance. Unshaved, that
made the measured turn gap in shipped audio **about 2 s** against a
`GAP_BETWEEN_LINES` of 0.9 and an official median of 0.51 — the whole archive
calibration silently defeated by TTS padding, and no gate could see it because
the constants were "right". The same padding made a mid-turn 。 run near 1 s,
twice the official same-speaker p75.

`shape_pauses()` fixes both, on 24 kHz mono samples, leaving speech untouched:
trim leading/trailing silence to zero, and cap any internal pause longer than
`SHAPE_PAUSE_FLOOR` to `GAP_WITHIN_TURN_MAX`. Pauses **below** the floor are
left exactly as the engine produced them — a Japanese 促音 closure is a ~0.1 s
silence, and "improving" it would eat the consonant. Verified on the rendered
MP3 after the change: turn gaps ~0.93 s, mid-turn 。 ~0.5 s, and one item lost
about 15 % of its runtime, all of it dead air.

**Verify a pacing constant on the rendered MP3, never in the source.** A
constants-only review passed this defect on every paper it had.

Three knowing deviations from the archive:

- **問題5's three pauses are not one value.** Official gives 1番 ≈ 8.3 s
  (spoken choices, like 問題3), 質問1 → 質問2 = 10.0 s, final 質問2 ≈ 11.2 s;
  `ANSWER_PAUSE` is one number per 問題, so 10 s is the compromise.
- **問題5 2番 runs longer than official**, because this repo speaks its four
  choices twice where official prints them (§"Spoken vs printed choices"). Eight
  extra utterances plus six 3 s inter-choice gaps add roughly 35 s to the item.
  The pause CONSTANTS are unchanged and still measured — only how many segments
  sit between them. Do not shave a gap to buy the time back.
- **Official reads each spoken choice as 「1、」+ ~1.1 s + the option text**,
  then ~3.1 s before the next number; we speak the whole choice line as one
  utterance, so only the ~3 s inter-choice gap is reproduced.

To recalibrate, use Part 4 and update ONLY these constants.

## Engineering rules (each fixed a real bug)

- Synthesize per line → 24 kHz mono WAV → **shape pauses** → concat WAVs →
  encode MP3 ONCE with `loudnorm=I=-15:TP=-1.0:LRA=11` — never concat MP3
  segments directly. `I=-15` is the official median; it replaced `I=-17`, a
  `volumedetect` mean_volume reading mistaken for LUFS (Part 4 step 1).
- **Shape each segment as soon as it is synthesized, before it is cached**, so a
  warm cache and a cold build produce byte-identical audio.
- Retry synthesis (3×, backoff); cache segments in `tests/<test_id>/segments/`
  so re-runs skip finished lines. The cache key is a hash of
  **text + voice + rate + pitch**, not the line's position — position-keying
  meant a reworded line or a remapped speaker silently reused the old audio.
- **Parse into a plan, then synthesize, then assemble.** The plan pins every
  segment path and gap duration up front: parallel tasks never target the
  same file, and the output is byte-identical to a sequential build.
- **Silence files are all created before block assembly begins** — lazy
  creation let two blocks write the same `_sil_1.3.wav` concurrently; the
  loser got a truncated gap: valid audio, wrong length, undetectable.
- Chapter offsets stay a strictly in-order running sum: block durations are
  measured in parallel, but `clock` accumulates block by block.
- **Script validation is a hard gate.** `validate_script()` runs before any
  synthesis and refuses to build on a missing 例, wrong item count, answer
  spoken aloud, authoring annotation, or unmapped speaker label (Part 1); an
  unmapped label otherwise never raises — `voice_for()` falls back to the
  narrator.
- Item detection regex is `^(例。|\d+番。)` — WITH the 。, so a spoken choice
  「1、…」 or an enumerating lead-in 「1番、2番。…」 is not mistaken for an
  item (no official paper has that enumerating line; the guard is defensive).

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
| 12 s answer | 13 | 問題1 (6) + 問題2 (7) |
| 8 s answer | 18 | 問題3 (6) + 問題4 (12) |
| 10 s answer | 2 | 問題5 |
| 20 s option-reading | 7 | 問題2 only (例+6) |

**These counts describe OUR build, not the official file.** `pause_after()`
appends an answer pause after every item block, 例 included; official audio
pauses after **scored items only** (an 例 runs straight into the
「最もよいものは◯番です…」 confirmation), measuring 12 × 12 s and 17 × 8 s
where the table says 13 and 18 — that histogram is also the cheapest proof of
the official item counts (5/6/5/11/3 = 30 answers, `jlpt-exam-structure`'s
table). `make check` asserts the table against `EXPECTED_ITEMS`/`ANSWER_PAUSE`,
so do not "correct" it toward the official histogram — change `pause_after()`
first. Estimated length ≈ 40–45 min; official runtime (36.6–52.1 min, median
43.3) is **not a calibration target** — it varies with how much the actors
say, which is content, not pacing. Match the pause table, not the clock.

---

# Part 4 — Calibration: measuring official audio

**The answer is already measured — read `references/official_pacing.md`
first** (per-sitting tables, sample counts, method). Re-measure only to check
a specific claim or after adding recordings — never re-derive from one file,
which is how three wrong numbers once got in (runtime "~50–52 min",
`GAP_BETWEEN_LINES` 1.3 s, loudness −17).

The corpus is `refs/JLPT_N2_NEW/<n>. N2 <M>-<YYYY>/…mp3` — 31 sittings, every
one except the cancelled July 2020 (quote the paths). **Never add a second
audio folder** — a duplicate folder once double-weighted the last three
years. Ignore stray `.rar` files; the script PDFs are scans (no transcript
for mora counts); Shinkanzen CD tracks are weaker evidence — label them.
Five steps (full commands and caveats in the reference, §1):

1. **Basics** — `ffprobe` for duration/bitrate; loudness via
   `ffmpeg -af loudnorm=I=-15:TP=-1.0:LRA=11:print_format=json -f null -`.
   **Never `volumedetect`**: `mean_volume` is ungated flat RMS, ~4 dB below
   the gated K-weighted figure — treating it as LUFS shipped every generated
   exam ~2 dB quiet.
2. **Long-pause histogram** — `silencedetect=noise=-35dB:d=2.5`; buckets: ~3 s
   structural / ~8 s answer 問3・問4 / ~12 s answer 問1・問2 / ~20 s 問題2
   option-reading. **A fixed threshold is not comparable across sittings** —
   some recordings lay a soft ~−34 dBFS marker tone over the last ~2.5 s of
   each answer pause; cross-check at −30 dB or use the reference's
   two-threshold envelope method.
3. **Timeline attribution** — read ordered `(start, duration)` pairs:
   `20s → talk → 12s` repeating = 問題2; `3s,3s,3s,8s` = 問題3/5 spoken
   choices; a dense run of lone 8 s pauses = 問題4 (its responses are read
   continuously — the 3 s spoken-choice gap belongs to 問題3/5 ONLY); `10s`
   then `12s` at the end = 問題5's 質問1/質問2.
4. **Turn gaps** — `silencedetect` cannot see them: official dialogue carries
   room tone, not digital silence, so diarize — label each sub-threshold gap
   in a 問題1/2 dialogue span speaker-change vs same-speaker by median F0
   either side (465 boundaries: speaker-change median 0.51 s, p75 0.75, p90
   1.08). `GAP_BETWEEN_LINES = 0.9 s` sits deliberately above the median
   (synthetic voices carry no prosodic turn-taking cues), under every p90.
5. **Speech rate** — in morae/min, not characters/min; the script PDFs are
   scans, so measure acoustically: syllable nuclei (intensity peaks, 2 dB dip
   criterion) per minute of speech, **same detector on both sides**. Official:
   250–281 nuclei/min, median 271; our builds 270.6–279.7 — inside the band,
   at its top. **N2 is not N1** (認定の目安: 「自然に**近い**」 speed), so do
   not push `SPEAKER_MAP` rates up to a natural-speed figure. Re-verify
   whenever a voice or rate value changes — nothing else checks rate.

The deliverable is an updated pacing table in Part 3 plus the evidence
mirrored into `references/official_pacing.md` — table and code first, then
mirror.
