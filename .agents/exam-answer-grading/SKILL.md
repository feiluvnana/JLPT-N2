---
name: exam-answer-grading
description: Grade user answers for JLPT mock exams (primarily N2), calculate standardized scaled scores (0-180), evaluate Pass/Fail criteria (overall >=90, section cutoffs >=19), analyze weaknesses by sub-question (問1-問14, 問題1-問題5), and write the structured result document (採点結果.json) with tailored reference-book study recommendations. Use this skill whenever the user asks to grade, score, check answers, evaluate test performance, 採点, 答え合わせ, or analyze exam results for a JLPT mock test.
---

# Exam Answer Grading (採点・弱点分析)

This skill automates the grading of examinee responses for JLPT mock tests, calculates official-style standardized scaled scores, evaluates pass/fail status against JLPT thresholds, identifies weak problem types, and writes the structured diagnostic document `採点結果.json`.

---

## 1. Overview & Architecture

When a user submits their answers or asks to grade a completed JLPT test:

1. **Answer Key Extraction**: Automatically parses correct answer tables from the exam Markdown sources:
   - `tests/<test_id>/言語知識・読解.md` (Questions 1 to 71)
   - `tests/<test_id>/聴解.md` (Listening questions: 問1〜問5)
2. **User Input Ingestion**: Reads examinee responses from:
   - `ユーザー解答*.json` saved by the **merged answer sheet** `解答.html` (below) — the default source, auto-discovered in the test dir and cwd. Several matching files merge, so hand-split halves also work.
   - Inline CLI arguments (`--answers-gengo` / `--answers-choukai`), which override.
3. **Scaled Score Calculation**: Converts raw section counts into JLPT standardized 0–60 scores:
   - **Language Knowledge (言語知識: 文字・語彙・文法)**: 51 questions max -> scaled to 60.
   - **Reading (読解)**: 20 questions max -> scaled to 60.
   - **Listening (聴解)**: 30 answers max (問題5 2番 yields two) -> scaled to 60.
   - **Total Score**: 180 points max.
4. **Pass / Fail Criteria Evaluation (JLPT N2 Standard)**:
   - **Overall Total**: $\ge 90 / 180$ points.
   - **Sectional Cutoffs (基準点)**: $\ge 19 / 60$ points in **ALL THREE** individual sections:
     - Language Knowledge $\ge 19$
     - Reading $\ge 19$
     - Listening $\ge 19$
   - _Note_: Failing any single sectional cutoff results in **不合格 (FAIL)** regardless of overall total score.
5. **Sub-Question Taxonomy Analysis & Diagnostics**:
   - Evaluates performance per大問 (問1〜問14 for Language/Reading, 問題1〜問題5 for Listening).
   - Flags weak areas (accuracy < 60%) and provides targeted recommendations referencing _Shin Kanzen Masuta N2_ textbooks (`refs/Shinkanzen/Shin_Kanzen_Masuta_N2-*.pdf`).
6. **Artifact Output**:
   - Saves `tests/<test_id>/採点結果.json` (the structured result document — see §4)

The merged answer sheet (`解答.html`) is owned by the
**`interactive-answer-sheet`** skill. It grades the whole 180-point exam in-page
on button press and writes `採点結果.json` + `ユーザー解答.json` itself — that is
the normal path. **This skill is the CLI equivalent**, for offline/batch runs
and for re-grading from a saved `ユーザー解答.json`.

Its in-page grader is generated FROM this module's `GENGO_QUESTION_TAXONOMY`,
`CHOUKAI_QUESTION_TAXONOMY` and `ADVICE_FOR` at build time, so the two can
never disagree. Keep those structures serializable, and re-run
`build_interactive.py` after changing any of them.

---

## 2. Command Execution

Run the execution script from the workspace root:

### Option A: Interactive answer sheet (the normal path)

The answer sheet is **merged into the problem sheet** — you answer inside the
booklet itself, not on a separate mark sheet. The old `マークシート.pdf` /
`マークシート.html` layer and its `--create-template` / `--user-pdf` flags were
removed; the `interactive-answer-sheet` skill replaces them.

1. Build the sheet (once per test, re-run after any edit to the Markdown):
   ```bash
   make sheet 1
   # or: python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/1
   ```
   → `tests/1/解答.html` (101 questions total: 71 Gengo/Dokkai + 30 Choukai with audio player).
2. Serve & answer in browser — one server covers every test, so no test id:
   ```bash
   make serve
   ```
   Pick the test from the list it opens on.
3. Press **「採点する」** → the full 180-point exam is graded on the spot: the page switches to its result screen and saves `tests/1/採点結果.json` and `tests/1/ユーザー解答.json`. The list then shows that score, and reopens the result screen on demand.
4. Command line grading remains available for batch/offline CLI workflows:
   ```bash
   make grade 1
   # or: python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1
   ```

**The answer key is truncated out of `解答.html`.** `build_interactive.py`
aborts if it cannot locate the key heading in either Markdown source, rather
than risk rendering a sheet that shows the answers while you solve. Note
`解答.html` is the _deliverable_ you solve on, distinct from the booklets
`言語知識・読解.html` / `聴解.html`, which `build_booklet.py` overwrites.

### Option B: Quick Inline CLI Grading

```bash
python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --answers-gengo "1:4,2:2,3:1,4:1,5:3..." --answers-choukai "問1-1:2,問1-2:3..."
```

---

## 3. Taxonomy Mapping & Scoring Table

These ranges are owned by `jlpt-exam-structure`; this table and
`GENGO_QUESTION_TAXONOMY` in `grade_answers.py` must mirror it exactly. The
script asserts that its ranges tile 1–71 with no gap or overlap at import.

| Section      | Problem | Sub-Category Name                     | Questions           | Raw Items | Scaled Max                  |
| ------------ | ------- | ------------------------------------- | ------------------- | --------- | --------------------------- |
| **言語知識** | 問1     | 漢字読み (Kanji Reading)              | 1–5                 | 5         | -                           |
|              | 問2     | 表記 (Orthography)                    | 6–10                | 5         | -                           |
|              | 問3     | 語形成 (Word Formation)               | 11–13               | 3         | -                           |
|              | 問4     | 文脈規定 (Word in Context)            | 14–20               | 7         | -                           |
|              | 問5     | 言い換え類義 (Paraphrases)            | 21–25               | 5         | -                           |
|              | 問6     | 用法 (Correct Usage)                  | 26–30               | 5         | -                           |
|              | 問7     | 文法形式の判断 (Grammar Form)         | 31–42               | 12        | -                           |
|              | 問8     | 文の組み立て (Sentence Composition ★) | 43–47               | 5         | -                           |
|              | 問9     | 文章の文法 (Text Grammar / Cloze)     | 48–51               | 4         | **60 (Combined, 51 items)** |
| **読解**     | 問10    | 内容理解・短文 (Short Passages)       | 52–56               | 5         | -                           |
|              | 問11    | 内容理解・中文 (Medium Passages)      | 57–64               | 8         | -                           |
|              | 問12    | 統合理解 (A/B Comparative Texts)      | 65–66               | 2         | -                           |
|              | 問13    | 主張理解・長文 (Long Essay)           | 67–69               | 3         | -                           |
|              | 問14    | 情報検索 (Information Retrieval)      | 70–71               | 2         | **60 (20 items)**           |
| **聴解**     | 問題1   | 課題理解 (Task Comprehension)         | 1番–5番             | 5         | -                           |
|              | 問題2   | ポイント理解 (Point Comprehension)    | 1番–6番             | 6         | -                           |
|              | 問題3   | 概要理解 (Summary Comprehension)      | 1番–5番             | 5         | -                           |
|              | 問題4   | 即時応答 (Quick Response)             | 1番–11番            | 11        | -                           |
|              | 問題5   | 統合理解 (Integrated Comprehension)   | 1番–2番 (3 answers) | 3         | **60 (30 items)**           |
| **合計**     |         |                                       |                     | **101**   | **180**                     |

---

## 4. Result Document (`採点結果.json`)

The result is **data, not prose** — there is no Markdown report. `解答.html` and
the test list both read this file back, and `result_payload()` in
`grade_answers.py` is its only definition on the Python side. The in-page
`computeResult()` builds the identical structure, and `make check` compares the
two documents field for field, so this shape is a contract:

```jsonc
{
  "test_id": "1",
  "graded_at": "2026-08-05T09:12:33+00:00",   // the ONLY field allowed to differ between graders
  "summary": {
    "passed": false,                           // overall >=90 AND every section >=19
    "total_scaled_score": 118, "max_scaled_score": 180,
    "cutoff_passed": true, "overall_threshold_passed": true,
    "sections": {                              // keyed by section name
      "言語知識（文字・語彙・文法）": {"raw_correct": 33, "raw_total": 51,
                                     "scaled_score": 39, "cutoff": 19, "passed_cutoff": true},
      "読解":   {"raw_correct": 14, "raw_total": 20, "scaled_score": 42, "cutoff": 19, "passed_cutoff": true},
      "聴解":   {"raw_correct": 20, "raw_total": 30, "scaled_score": 40, "cutoff": 19, "passed_cutoff": true}
    }
  },
  "taxonomy_stats": {                          // per 大問; empty 大問 are omitted
    "問1": {"name": "漢字読み (Kanji Reading)", "section": "言語知識",
            "correct": 3, "total": 5, "percentage": 60.0}
  },
  "weak_areas": [                              // percentage < 60, with the study advice
    {"code": "問3", "name": "…", "section": "言語知識", "percentage": 33.3, "advice": "…"}
  ],
  "detail_gengo":  {"1": {"correct": 4, "user": 2, "is_correct": false}},   // all 71
  "detail_choukai": {"問1-1": {"correct": 2, "user": null, "is_correct": false}}
}
```

The result **screen** renders that document into the five familiar parts —
総合判定, 得点サマリー, 大問別詳細分析, 弱点診断とアドバイス, 全設問解答チェック表.
Its 大問 ratings are exactly the labels both graders agree on: `優 (Strong)`
(>=80%), `良 (Fair)` (60-79%), `要強化 (Weak)` (<60%). Plain text, no emoji —
4cad944 removed emoji from the report symbols and both graders must stay in
lockstep.

---

## 5. Invariants & Rules

- **Strict Scale Calculation**: Raw scores must be converted proportionally to the 60-point scale per section to reflect real JLPT results accurately.
- **Sectional Cutoff Rules**: Always enforce the 19-point sectional cutoff rule. Even if the total is 120/180, if Reading is 18/60, the result is `不合格`.
- **Reference Integrity**: Advice for weak areas must map directly to the corresponding _Shin Kanzen Masuta N2_ study area (Vocab/Kanji/Grammar/Reading/Listening).
