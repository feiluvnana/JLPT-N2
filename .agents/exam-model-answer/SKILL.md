---
name: exam-model-answer
description: Single owner of generating the model answer and comprehensive explanation deliverable (模範解答.html). Generates a complete, interactive, pedagogically rich Japanese-language explanation document for every question in an exam (71 Language Knowledge & Reading questions + 30-31 Listening questions). Explains why the correct answer is right (with evidence, grammar rules, dictionary definitions, passage quotes, listening script evidence) and why each distractor option is incorrect. Use whenever generating 模範解答.html for a test, updating question explanations, reviewing model answers, or explaining exam solutions.
---

# Exam Model Answer & Explanation (模範解答・詳細解説)

This skill owns generating `tests/<test_id>/模範解答.html` — the model
answer and in-depth explanation deliverable — and `詳細解説.json`, the
Japanese explanations it renders.

**Any language other than Japanese belongs to `exam-answer-translation`**:
`詳細解説.<lang>.json`, the scaffold/merge tooling, the UI label set, and the
in-page switcher. `build_model_answer.py` discovers those files by glob and
renders one `.lang-pane` per language inside every explanation box, so the
page below is the Japanese layer of a possibly multilingual page. Which
languages a paper ships with is declared in `GENERATE.md`.

## Purpose & Pedagogical Quality

While `解答.html` is for taking the test and grading, `模範解答.html` is for
**deep post-exam study (復習・学習)**. For every question (all 101 items:
71 Gengo/Dokkai + 30-31 Choukai), it provides:

1. **Question Stem & Choices**: full context, options, correct-answer badge.
2. **Reading Passages & Audio Transcripts**: 読解 — full passage text with
   numbered markers (`①`, `②`, `（注1）`); 聴解 — full spoken transcript with
   speaker labels.
3. **Comprehensive & Concise Explanation**:
   - **Why the correct answer is selected**: direct quotes from the
     passage/audio, grammar rules, kanji breakdowns — concise, natural,
     clear for learners.
   - **Full option-by-option analysis**: a concrete explanation for EVERY
     choice (why it's correct or fails — contrary to text, unmentioned,
     wrong collocation/particle/verb form, wrong audio timing). Exactly ONE
     option tagged `[正解]` matching the official key, all others
     `[不正解]` — never all `[不正解]`, never a mismatched key. Generic
     placeholders ("選択肢1は文脈・文法制約に合致しません") are prohibited.
   - **Zero internal metadata leaks** — never `[kanji-n2.json]`, `[同分野]`,
     `[N1]`, `〜れる一段動詞×4`, or similar pipeline artifacts; explanations
     are strictly learner-facing.
   - **Mandatory furigana** (`｜漢字《かんじ》` or `<ruby>`) on all target
     kanji, difficult vocabulary, stems, and explanations.
     **pykakasi is a first draft, never the answer** — `詳細解説.json`
     furigana is hand-authored (`apply_furigana()` only converts existing
     `《…》` markup into `<ruby>`, it computes nothing). Check pykakasi
     output reading-by-reading before typing it in; known failure modes: a
     bare `人` reads `にん` (should be `ひと` — genuine `にん` compounds are
     always long enough that kakasi merges them into one token); `方` right
     after hiragana reads `ほう` (should be `かた` — genuine `ほう` compounds
     glue `方` to a preceding kanji, not hiragana); `小さい`/its conjugations
     get a stray chouon (`ちーさい` for `ちいさい`, a dictionary bug). A
     separate hand-authoring failure (found across a 2026-08 sweep, 216
     instances in one file): a compound split across a kanji-hiragana-kanji
     boundary (取り組み, 受け取る) sometimes gets the whole preceding
     reading re-prepended onto the second kanji's ruby (`取《と》り組
     《とりく》み` instead of `取《と》り組《く》み`) — each `《…》` must hold
     only that kanji's own reading. Treat unverified furigana as a defect;
     a word's reading must also stay internally consistent within one file.
   - **Important Vocabulary & Grammar** — a complete per-item study summary,
     not 1–2 vocab glosses: the tested word/pattern (reading, meaning,
     nuance, a distinct example use), any grammar form needed to parse the
     sentence, key vocabulary a learner likely doesn't know, any idiom
     involved. A `points` list with only 1–2 short entries signals the item
     was under-filled — reading/listening items still carry material worth
     surfacing even when the "point" is comprehension, not one word.
   - **Easy-to-understand Japanese** — `why_correct`/`options_analysis`/
     `points` are written FOR N2 learners: short, plain sentences, common
     vocabulary; keep and furigana an unavoidable technical term rather than
     inventing a vaguer paraphrase. Does not apply to `stem`/`options`/
     `passage`/`script` — the exam's actual wording, furigana'd only, never reworded.
   - **Emoji-free** — clean, professional typography throughout.

## Authoring `詳細解説.json` — scaffold directly, never type passages from scratch

```bash
make scaffold-explanations <id>   # -> scaffolds tests/<id>/詳細解説.json with stems/options/passages pre-populated
```

Then edit `詳細解説.json` to complete `why_correct`, `options_analysis`, and
`points` per item. Validate it parses
(`python3 -c "import json,sys; json.load(open(sys.argv[1]))" tests/<id>/詳細解説.json`),
then `make model-answer <id>`.

**Do not write a per-test "compiler" script** (a one-off Python file
building a literal `details = {...}` dict). Four such files accumulated in
`scripts/` before this rule existed — each 100–400KB, unreferenced by any
Makefile target, not re-runnable without clobbering hand-edits.
`詳細解説.json` is the artifact; a script that produced it once is not.

Instead use the shared fidelity tool:

```bash
python3 .agents/exam-model-answer/scripts/verify_fidelity.py tests/<id>
```

It re-derives `stem`/`options`/`passage`/`script` straight from
`言語知識・読解.md`, `聴解.md`, and `聴解スクリプト.txt` and reports every
place `詳細解説.json`'s wording has drifted (furigana differences ignored;
only wording compared). Run it before editing (to see existing drift) and
again when done (to confirm you introduced none) — report-only; read its
docstring for the expected mismatch shapes (問6/問9 stems keep their
instruction-line context; 聴解 `script` excludes the trailing restated
question). Every other reported mismatch is a real defect — most commonly
a passage left empty on a 2nd+ question sharing it, or wording that no
longer matches the booklet/script it was copied from.

## Deliverable Specification

| Deliverable | File Name | Description / Source |
| ----------- | --------- | -------------------- |
| Model Answer & Detailed Explanation | `模範解答.html` | Generated by `build_model_answer.py` from `言語知識・読解.md`, `聴解.md`, `聴解スクリプト.txt`, and `test_spec.json` |

## Execution & Mandatory Final Step Rule

> **CRITICAL INVARIANT**: Generating `模範解答.html` **MUST ALWAYS BE THE
> ABSOLUTE FINAL STEP** in both the generation and import pipelines.
>
> - **Generation**: run `make model-answer <id>` ONLY AFTER Stage 4 QA
>   returns `QA: PASS` and all question/option/script edits are frozen —
>   earlier is prohibited because subsequent QA fixes desynchronize the
>   explanations from the exam.
> - **Import**: run `make model-answer imported-<slug>` ONLY AFTER all 101
>   keys are verified against the official answer key and `make check` is
>   completely green.
> - **Translations**: `詳細解説.<lang>.json` is produced BETWEEN the frozen
>   `詳細解説.json` and this build (`exam-answer-translation`) — one page
>   carries every language, so the build still happens exactly once, last.

```bash
python3 .agents/exam-model-answer/scripts/build_model_answer.py tests/<id>
make model-answer <id>          # or: make explanation <id>
```

## Structure & Architecture

- **Script**: `.agents/exam-model-answer/scripts/build_model_answer.py`
- **Output**: `tests/<test_id>/模範解答.html`
- **UI Features**: Noto Serif/Sans CJK JP typography; section tabs
  (すべて/文字・語彙/文法/読解/聴解); a 1–71 + 聴解 1–30 quick-nav grid; a
  search/filter box; an embedded 聴解 audio player with chapter timestamps;
  print-friendly (`@media print`) and mobile-responsive layout.
