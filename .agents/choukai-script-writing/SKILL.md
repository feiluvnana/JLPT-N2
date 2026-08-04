---
name: choukai-script-writing
description: Single owner of the choukai TTS script file format — the .txt containing ONLY the text spoken in an official JLPT listening exam. Use whenever creating or editing the listening script, whenever the user mentions the TTS script, narration text, or the choukai audio source file. The MP3 generator's timing engine parses this file, so its block conventions are load-bearing — violating them silently corrupts the audio pacing.
---

# Choukai Script Writing

## File Location & Naming (Japanese File Names)

The TTS script file is written to the test folder:
- Path: `tests/<test_id>/聴解スクリプト.txt` — **always this name**, per the
  Japanese-file-names invariant. `make mp3 <test_id>` passes exactly this path,
  and every test in the repo's history has used it.
- `script.txt` exists only as a legacy fallback inside `make_choukai_mp3.py`:
  when invoked with NO argument it looks for `聴解スクリプト.txt` in the current
  directory and falls back to `script.txt`. Do not author new tests against it.

## Content rule: official narration ONLY

The file contains exactly what the announcer and voice actors say — nothing
else. No headers, no usage notes, no markers. Required elements (see
jlpt-exam-structure for the exact announcer lines):

opening line → per-section instruction → 「では、練習しましょう。」→ 例 →
「最もよいものは◯番です。…では、始めます。」→ items → … →
「これで、聴解試験を終わります。」

問題5 instead says 「この問題には練習はありません。」

## Calibrating against Official Past Exam Scripts (`refs/JLPT/`)

Always cross-check dialogue tone, speaker turn length, announcer wording, and
distractor flow against the 5 official listening script PDFs in `refs/JLPT/`.
Their exact filenames live in **`AGENTS.md` section 3** (the single owner);
`reference-book-reading` explains how to read the scans.

These real scripts define the standard dialogue rhythm (3-5 exchanges for 問題1/2, monologues for 問題3, rapid single turn for 問題4) and precise announcer phrasing.

- **NO FURIGANA in TTS Script**: The script file (`聴解スクリプト.txt`) MUST remain clean plain text WITHOUT any `<ruby>` tags or furigana annotations, ensuring natural Edge-TTS speech synthesis. Furigana is generated exclusively for the booklet HTML (`聴解.html`).

### NEVER reveal an answer for a scored item (exam-breaking)

`最もよいものは◯番です。` is an **例-only** line. It exists solely so the
announcer can demonstrate how to mark the answer sheet, and it appears ONLY
inside the 例 confirmation of 問題1〜問題4, always in the full official form:

```
最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。最もよいものは◯番ですから、答えはこのように書きます。では、始めます。
```

Therefore, in a valid script:

- A bare `最もよいものは◯番です。` after `1番。`〜`12番。` is FORBIDDEN — it
  speaks the correct answer aloud and makes the whole exam worthless. This
  bug shipped in `tests/2` and `tests/3`; every scored item announced its own
  answer.
- `質問1の最もよいものは◯番です。` / `質問2の最もよいものは◯番です。` are
  FORBIDDEN anywhere. 問題5 has no 例 at all
  (「この問題には練習はありません。」), so it can never carry a reveal line.
- 問題5 likewise never gets an 例 confirmation line. 問題1〜4 each get exactly
  one, and only after the 例 item.
- Answers live in the answer-key tables at the end of `聴解.md` — never in audio.

**No authoring annotations either.** Parentheticals such as
`（※選択肢3が受付、4が案内誘導）` or `（※「拝見しました」に対する自然な感謝の返し）`
are notes to yourself, not narration — Edge-TTS will read them out loud.
Nothing that the announcer or a voice actor would not say belongs in this
file; put rationale in the 解説 column of `聴解.md` instead.

`make_choukai_mp3.py` hard-fails on both of these before synthesizing, so a
violating script cannot produce an MP3.

## Block conventions (parser contract)

- Blocks are separated by ONE blank line. **One block = one audio unit.**
- Item blocks start with `例。` or `N番。` followed by the situation +
  question ON THE SAME LINE: `1番。会社で女の人と男の人が話しています。…か。`
- Section markers are their own blocks: `問題1。` (numbered, with 。).
- Instruction text (問題1では、…) is its own block.
- **The two-question 問題5 item must be ONE block**: instruction line,
  dialogue lines, 質問1。…, 質問2。… — a blank line inside it puts the
  12-second answer pause in the wrong place (this bug happened; don't repeat it).
- 問題1/2: repeat the question as the block's last line.
- 問題3/4/5 spoken choices: one per line, format `1、…。` `2、…。` (読点 after
  the digit — the parser and pacing engine key on `^[1-4]、`).
- Japanese punctuation only: 、and 。 An ASCII `,` or `.` in a spoken line makes
  edge-tts mis-time the pause. (`?` is fine and is used throughout for
  colloquial questions.) `make check` rejects ASCII commas/periods.

## Spoken vs printed choices — do not speak the printed ones

jlpt-exam-structure's "Printed in booklet" column decides this, and it is not
uniform inside 問題5:

| 問題 | Choices are |
|---|---|
| 1, 2 | PRINTED in `聴解.md` — never spoken |
| 3, 4 | SPOKEN only — booklet prints nothing |
| 5, 1番/2番 | SPOKEN only |
| 5, 3番 | **PRINTED** — the two-question item's options are in the booklet |

Speaking 問題5-3番's options is not a harmless extra: the printed and spoken
lists then drift, and test 2 shipped a 3番 whose booklet printed 学食 proposals
while the audio read out 「全自動モデル」「省エネモデル」「小型モデル」 —
leftovers from the 家電 item in 問題1, which made the answer guessable from the
booklet alone. `make check` now counts spoken choice lines per 問題 and fails on
any that belong in the booklet instead.

## Instructions are copied, not re-worded

The 問題N instruction in the script must be **character-for-character** the one
in `聴解.md` (the script adds only 「では、練習しましょう。」 after it). Test 2
drifted in three places — 「どのような内容か」 for 「どんな内容か」,
「文章がやや長くなります」 for 「長めの話を聞きます」, and a 問題4 instruction
missing 「まず…それから」 — so the examinee heard different wording than they
read. Take the canonical text from jlpt-exam-structure, paste it into both
files, and let `make check` confirm they match.

## The 例 must be answerable, and its announced number must be the answer

`最もよいものは◯番です。` names a number in the BOOKLET's 例 option list, so
the two are one item split across two files. Test 4's 問題1 例 played a
忘年会 dialogue ending 「君は店の予約をお願いできるかな」「すぐ電話します」,
asked 「このあとまず何をしますか」, and printed
`1. 忘年会をする / 2. 新年会をする / 3. 送別会をする / 4. 歓迎会をする` —
options that answer a different question, with the announcer declaring 2番
(新年会をする), which the dialogue never mentions. The demonstration of how to
mark the sheet was itself unanswerable, in the first thing the examinee hears.

Check every 例 by reading the printed options against the spoken 例 and its
question, then confirming the announced number is the option the dialogue
supports. `make check` cannot: 問題1/2 options are printed, so there is nothing
to compare them against.

## The 問題 decides the QUESTION TYPE, not just the topic

`logs/test_spec.json` hands you a list of scenarios, not an assignment of
scenarios to 問題. Placing one is your call, and the section's task type binds:

| 問題 | Task | Question shape | Shape of the item |
|---|---|---|---|
| 1 | 課題理解 | 〜は、このあとまず何をしますか | a conversation where one person must ACT |
| 2 | ポイント理解 | どうして〜か / 何が一番〜か / どのように説明していますか | conversation or monologue, no action required |
| 3 | 概要理解 | 〜は何について話していますか | monologue, gist only |

Test 4 shipped these swapped: a radio monologue asking 「夜間のエアコンの使用に
ついて、どのように説明していますか」 sat in 問題1, and a 課題理解 item asking
「これからまず何をしますか」 sat in 問題2. Both were repaired by exchanging the
two items (and re-ordering their options, since the key must land on the
position `answer_positions` prescribes for its new slot).

## The keyed option must be quotable, and every other option denied

Two separate rules, both broken by test 4:

- **Quotable.** 問題1-5番 keyed 「点検作業員に車移動の連絡をする」 while the
  script says 「事前に管理事務所へご連絡の上」 — the keyed action named the
  wrong party, so the keyed option was simply not what the audio said. Copy the
  deciding line out of the script into the 解説 cell; if you cannot, the item is
  wrong. (`make check` now WARNS when a 解説 quote is nowhere in the script —
  that warning is how test 4's invented 「本当ですか！ぜひお願いしたいです」 and
  four other phantom quotes were found. Warnings are not optional reading.)
- **Denied.** A wrong option must be raised and then killed, and a second TRUE
  statement is a second answer. 問題2-6番 asked why the student cannot take the
  day off, keyed 「申告期限を過ぎている」, and had the 店長 also say that nobody
  else can cover the shift — which option 1 stated. Give each distractor its
  own denial line (「その日に休みを希望している人も他にいない」).
- **A 理由 question must be keyed to the CAUSE, not to the measure.** 問題2-4番
  asked the reason for a timetable change; the script gave 運転手不足 as the
  cause and the key was 「利用者が少ない夜間の便を減らすため」, which is what was
  DONE about it — while another option named the actual cause.

## One voice per person, and questions that name them unambiguously

If an item's questions say 「男の学生は」/「女の学生は」, the item must contain
exactly one of each. Test 2's 問題5-3番 had 男1 and 男2 both speaking as students
while 質問1 asked about 「男の学生」 — unanswerable as posed. Either give the
item one speaker per gender/role, or word the questions so each maps to exactly
one voice.

**The narration must also agree with the VOICE the label gets.** The label
picks the voice out of `SPEAKER_MAP`; the narration tells the examinee who is
speaking; nothing checks that the two agree. Test 4 broke it both ways in one
paper: 問題5-3番 announced 「担当者の男の人」 while `担当者:` is mapped female,
and 問題2-6番 announced 「女の学生」 while `学生:` is mapped male. Look the label
up in the map before writing the narration, and prefer labels of contrasting
gender over two same-gender voices separated only by a few percent of rate
(問題1-4番 had 女 and 担当者 both on Nanami, 4% apart, in a two-person call).

## Required structure — every element is mandatory

A full N2 script is **exactly 35 item blocks** (`例。`/`N番。`) in the per-問題
counts below, plus the 問題 headers, instructions, announcer lines and 例
confirmations. **The TOTAL block count is not fixed** — test 1 is 48 blocks and
the retired test 4 (in git at b9b90de) was 56, both valid; the difference is
only how instruction and announcer text is split. So do not treat any total as a target: `validate_script()`
enforces the 35 item blocks and their distribution and merely *prints* the
total (`script OK: N blocks, …`).

Missing pieces are otherwise SILENT: the MP3 still builds and just quietly
stops being an official-format exam. Tests 2 and 3 shipped with no 例 at all
for 問題3/問題4 and no 問題5 announcer line, and nothing caught it. All of the
following are now enforced:

| Element | Rule |
|---|---|
| Opening | 「これから、N2の聴解試験を始めます…」 must be present |
| 問題1〜5 headers | `問題N。` as its own block, all five, in order |
| 問題1〜4 practice | each: instruction ending 「では、練習しましょう。」 → ONE `例。` item → ONE full confirmation line → items |
| 問題5 practice | NONE. Instruction must contain 「この問題には練習はありません。」 and there must be no `例。` block |
| 問題5 announcer | 「1番、2番。問題用紙に何も印刷されていません。…では、始めます。」 before 1番 |
| Item counts (incl. 例) | 問題1=6, 問題2=7, 問題3=6, 問題4=13, 問題5=3 |
| Closing | file must END with 「これで、聴解試験を終わります。」 |
| Answer reveals | 例 confirmations only — see the section above |
| Annotations | none (`（※…）`) |
| Typo guard | 「問題用紙になに印刷」 → must be 「何も印刷」 |
| 質問1/質問2 | must sit in the SAME block |
| Speaker labels | every label must exist in `SPEAKER_MAP` |

問題5 has 3 item blocks but 4 answers — its 3番 carries 質問1 and 質問2.

## Speaker labels

Dialogue lines: `男:` `女:` `男1:` `男2:` `夫:` `妻:` `学生:` `先生:` `店員:`
`医者:` `部長:` `店長:` `専門家:` `レポーター:` `教室の人:` `職員:` `係員:`
`担当者:` `講師:` `アナウンス:` `アナウンサー:` `教授:` `FP:` — half or
full-width colon. Unlabeled lines = narrator.

**An unmapped label does not error at synthesis time — it silently falls
through to the narrator voice**, so a 職員 or 教授 line gets read by the
announcer. That shipped in tests 2 and 3 across 10 labels. `validate_script()`
now rejects any label missing from the map; add it to `SPEAKER_MAP` in
choukai-mp3-generation *before* using it, choosing a voice that contrasts with
the other speaker named in that item's narration.

## Validation (automatic)

`make_choukai_mp3.py` runs `validate_script()` before synthesizing anything and
refuses to build on any violation above, printing every problem at once. To
check without building:

```bash
python3 -c "
import re,pathlib,importlib.util
s=importlib.util.spec_from_file_location('m','.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
b=[x.strip() for x in re.split(r'\n\s*\n', pathlib.Path('tests/1/聴解スクリプト.txt').read_text(encoding='utf-8')) if x.strip()]
m.validate_script(b)"
```

Still check by eye for what code can't judge: mojibake (`�`), stray
Latin/Cyrillic words, and wrong speaker attribution inside 例 dialogues.


