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

Always cross-check dialogue tone, speaker turn length, announcer wording, and distractor flow against the 5 official listening script PDFs in `refs/JLPT/`:
- **07/2023**: `refs/JLPT/14. N2 7-2023 (script).pdf`
- **12/2023**: `refs/JLPT/14. script N2 12-2023.pdf`
- **12/2024**: `refs/JLPT/15. script N2 12.2024.pdf`
- **07/2025**: `refs/JLPT/16. N2-7.2025 (script).pdf`
- **12/2025**: `refs/JLPT/17 (script) N2 12-2025 _260410.pdf`

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

## Required structure — every element is mandatory

A full N2 script is **48 blocks** (35 item blocks + headers, instructions and
例 confirmations). Missing pieces are SILENT: the MP3 still builds and just
quietly stops being an official-format exam. Tests 2 and 3 shipped with no 例
at all for 問題3/問題4 and no 問題5 announcer line, and nothing caught it. All
of the following are now enforced by `validate_script()` in
`make_choukai_mp3.py` — note the 48 total is only *printed* by the validator
(`script OK: N blocks, …`), so check that number by eye:

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


