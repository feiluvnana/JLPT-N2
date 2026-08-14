---
name: exam-model-answer
description: Single owner of generating the model answer and comprehensive explanation deliverable (模範解答.html). Generates a complete, interactive, pedagogically rich Japanese-language explanation document for every question in an exam (71 Language Knowledge & Reading questions + 30-31 Listening questions). Explains why the correct answer is right (with evidence, grammar rules, dictionary definitions, passage quotes, listening script evidence) and why each distractor option is incorrect. Use whenever generating 模範解答.html for a test, updating question explanations, reviewing model answers, or explaining exam solutions.
---

# Exam Model Answer & Explanation (模範解答・詳細解説)

This skill owns the generation of `tests/<test_id>/模範解答.html` — the official model answer and in-depth explanation deliverable.

## Purpose & Pedagogical Quality

While `解答.html` is designed for taking the test and grading score, `模範解答.html` is designed for **deep post-exam study and review (復習・学習)**. For every single question on the paper (all 101 items: 71 Gengo/Dokkai + 30-31 Choukai), it provides:

1. **Question Stem & Choices**: Complete question context, options, and clear correct answer badge.
2. **Reading Passages & Audio Transcripts**:
   - For **読解 (Reading)**: The full passage text with numbered markers (`①`, `②`, `（注1）`) and visual references.
   - For **聴解 (Listening)**: The full spoken transcript (`聴解スクリプト.txt`) with speaker labels and dialogue flow.
3. **Comprehensive & Concise Explanation (詳細・簡潔な解説)**:
   - **Why the correct answer is selected (`正解の根拠・理由`)**: Direct quotes from the passage/audio, grammar rules, conjunction constraints, kanji reading/component breakdowns. Written concisely, naturally, and clearly for Japanese learners.
   - **Full Option-by-Option Distractor Analysis (`全選択肢の個別解説・誤答分析`)**: Clear, concise, concrete explanation for EVERY choice (1, 2, 3, 4) explaining why it is correct or why it fails (contrary to text, unmentioned, wrong collocation, incorrect particle/verb form, wrong timing in audio). Generic placeholder sentences like "選択肢 1 は文脈・文法制約に合致しません" are strictly prohibited.
   - **Zero Internal Metadata Leaks**: Explanations must NEVER leak internal dataset or authoring pipeline metadata (e.g. `[kanji-n2.json]`, `[同分野]`, `[N1]`, `[N3]`, `〜れる一段動詞×4`, `送り仮名「れる」からは絞り込めない`, `※演じるはopenjlpt上...`). Explanations are strictly learner-facing.
   - **Mandatory Furigana Support (`ルビ・ふりがな付与`)**: Furigana notation `｜漢字《かんじ》` or `漢字《かんじ》` (or `<ruby>漢字<rt>かんじ</rt></ruby>`) MUST be used on all target kanji, difficult vocabulary, question stems, explanations, and vocabulary points to ensure maximum accessibility and pedagogical clarity for learners.
     - **pykakasi is a first draft, never the answer.** `詳細解説.json` furigana is hand-authored (there is no automated generator wired into `build_model_answer.py` — `apply_furigana()` only converts already-present `《…》`/`｜…《…》` markup into `<ruby>` tags; it does not compute readings). When pykakasi is used to speed up drafting, its output MUST be checked reading-by-reading before it is typed into the JSON — never pasted in blind. Two confirmed pykakasi failure modes, found by auditing this repo's own choukai booklets, that generalize beyond that one script:
       - A bare single-kanji `人` token is read `にん` by pykakasi, but every genuine `にん` compound (三人, 本人, 友人, 何人, …) is long enough that pykakasi already merges it into one multi-character token — so a standalone `人` in running text is essentially always `ひと` ("a/the person"), never `にん`.
       - A `方` token immediately after hiragana (a verb's renyoukei/stem: 伝わり方, 使い方, 考え方, 話し方, …) is the "method/way" reading `かた`, never `ほう` — genuine `ほう` compounds (一方, 先方, 双方, 四方, …) have `方` glued to a preceding *kanji*, not hiragana.
       - `小さい` and its conjugations (小さく, 小さかった, 小さすぎる, …) come back from pykakasi with a stray chouon mark (`ちーさい` instead of `ちいさい`) — a `kks.convert()` dictionary bug, not a context issue.
       - A hand-authoring failure mode distinct from pykakasi itself, found across a 2026-08 QA sweep of every existing test (216 instances in one file alone): when a compound splits across a kanji-hiragana-kanji boundary (取り組み, 受け取る, 言い換える, 担い手, 女の人, …), the SECOND kanji's ruby sometimes gets the *whole preceding reading re-prepended* instead of just its own reading — e.g. `取《と》り組《とりく》み` (garbled) instead of `取《と》り組《く》み`. Each kanji's `《…》` must contain only that kanji's own reading, never an accumulation of everything read so far in the word.
       - Treat any furigana you didn't personally verify as a defect, the same way a distractor rationale copy-pasted from a template is a defect. When in doubt, look the word up rather than trust either your own recollection or pykakasi's tokenizer. A word's reading must also be internally consistent within one file — the same word being read one way in one item and a different way in another (or even twice differently in the same script, as with 伝わり方) is itself a defect signal, independent of which reading is "more correct."
   - **Important Vocabulary & Grammar (`重要語彙・文法のポイント`)**: This is a **complete study summary for that single question**, not a couple of vocabulary glosses. For every item it MUST cover, when applicable: the tested word/pattern itself (reading, meaning, nuance, one short example use distinct from the question sentence), any grammar form appearing in the stem/passage/script that a learner needs to parse the sentence, key vocabulary in the passage/options that a learner is likely not to know, and any idiom or set phrase involved. A `points` list with only 1–2 short entries is a sign the item was under-filled, not a sign the question was simple — reading and listening items still carry grammar/vocabulary worth surfacing even when the "point" is comprehension rather than a single word. All furigana'd per the rule above.
   - **Easy-to-Understand Japanese (`わかりやすい日本語`)**: `why_correct`, `options_analysis`, and `points` are explanations *for* N2 learners, not native-level literary prose *about* the item. Prefer short, plain sentences and common vocabulary over difficult synonyms; when a technical term (文法用語, 品詞名) is unavoidable, keep it and furigana it rather than inventing a vaguer paraphrase. This does not apply to `stem`/`options`/`passage`/`script` — those are the exam's actual wording and must never be reworded, only furigana'd.
   - **Emoji-Free Design**: All UI elements, badges, and text use clean, professional typography without emojis.

## Authoring `詳細解説.json` — scaffold directly, never type passages from scratch

To save AI tokens and prevent drift, **first scaffold the template** from the finalized Markdown sources:

```bash
make scaffold-explanations <id>   # -> scaffolds tests/<id>/詳細解説.json with stems/options/passages pre-populated
```

Then edit `tests/<test_id>/詳細解説.json` to complete `why_correct`, `options_analysis`, and `points` for each item.
Validate it parses (`python3 -c "import json,sys; json.load(open(sys.argv[1]))" tests/<id>/詳細解説.json`),
and run `make model-answer <id>`.

**Do not write a per-test "compiler" script** (a one-off Python file that
builds a literal `details = {...}` dict and dumps it to
`詳細解説.json`). Four such files accumulated in `scripts/` before this rule
existed — each 100–400KB, none referenced by any Makefile target or by
`build_model_answer.py`, none re-runnable without clobbering later hand-edits
— and they read as part of the pipeline to a future agent when they were pure
historical scratch that had already drifted from the JSON it once produced.
`詳細解説.json` is the artifact; a script that happened to produce it once is
not.

Instead, use the shared fidelity verification tool:

```bash
python3 .agents/exam-model-answer/scripts/verify_fidelity.py tests/<id>
```

It re-derives `stem`/`options`/`passage`/`script` straight from
`言語知識・読解.md`, `聴解.md`, and `聴解スクリプト.txt` — the exam's own
source — and reports every place `詳細解説.json`'s wording has drifted from
that source (furigana differences are ignored; only wording is compared).
Run it before you start editing a test (to see existing drift) and again
before you consider the test done (to confirm you introduced none). It is
report-only — read its module docstring for the couple of mismatch shapes
that are expected by design (問6/問9 stems keep their instruction-line
context; 聴解 `script` intentionally excludes the trailing restated question)
so you don't "fix" those; every other reported mismatch is a real defect —
most commonly a reading passage left empty on the 2nd+ question that shares
it, or wording that no longer matches the booklet/script it was copied from.

## Deliverable Specification

| Deliverable | File Name | Description / Source |
| ----------- | --------- | -------------------- |
| Model Answer & Detailed Explanation | `模範解答.html` | Generated by `build_model_answer.py` from `言語知識・読解.md`, `聴解.md`, `聴解スクリプト.txt`, and `test_spec.json` |

## Execution & Mandatory Final Step Rule

> **CRITICAL INVARIANT**: Generating `模範解答.html` **MUST ALWAYS BE THE ABSOLUTE FINAL STEP** in both the generation (`jlpt-test-generation`) and import (`external-test-import`) pipelines.
> 
> - **In test generation**: Run `make model-answer <id>` ONLY AFTER Stage 4 QA has returned `QA: PASS` and all question/option/script edits are frozen. Generating it earlier is prohibited because subsequent QA fixes would cause the explanations to desynchronize from the exam.
> - **In test import**: Run `make model-answer imported-<slug>` ONLY AFTER all 101 keys are verified against the official answer key and `make check` is completely green.

```bash
# Generate 模範解答.html for a test:
python3 .agents/exam-model-answer/scripts/build_model_answer.py tests/<id>
# or using Makefile:
make model-answer <id>
# (alias: make explanation <id>)
```

## Structure & Architecture

- **Script**: `.agents/exam-model-answer/scripts/build_model_answer.py`
- **Output**: `tests/<test_id>/模範解答.html`
- **UI Features**:
  - Clean, modern layout using Noto Serif CJK JP / Noto Sans CJK JP typography.
  - Section tabs: `すべて (All)`, `文字・語彙 (Moji/Goi)`, `文法 (Bunpou)`, `読解 (Dokkai)`, `聴解 (Choukai)`.
  - Quick question navigation jump grid (1–71, 聴解 1–30).
  - Search & filter box to quickly find questions by keyword, grammar point, or number.
  - Embedded audio player for Choukai with chapter timestamps if available.
  - Print-friendly layout (`@media print`) and mobile-responsive viewport.
