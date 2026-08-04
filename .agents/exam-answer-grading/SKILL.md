---
name: exam-answer-grading
description: Grade user answers for JLPT mock exams (primarily N2), calculate standardized scaled scores (0-180), evaluate Pass/Fail criteria (overall >=90, section cutoffs >=19), analyze weaknesses by sub-question (問1-問14, 問題1-問題5), and generate detailed Markdown feedback reports (採点結果.md) with tailored reference-book study recommendations. Use this skill whenever the user asks to grade, score, check answers, evaluate test performance, 採点, 答え合わせ, or analyze exam results for a JLPT mock test.
---

# Exam Answer Grading (採点・弱点分析)

This skill automates the grading of examinee responses for JLPT mock tests, calculates official-style standardized scaled scores, evaluates pass/fail status against JLPT thresholds, identifies weak problem types, and generates comprehensive Japanese Markdown diagnostic reports.

---

## 1. Overview & Architecture

When a user submits their answers or asks to grade a completed JLPT test:

1. **Answer Key Extraction**: Automatically parses correct answer tables from the exam Markdown sources:
   - `tests/<test_id>/言語知識・読解.md` (Questions 1 to 75)
   - `tests/<test_id>/聴解.md` (Listening questions: 問1〜問5)
2. **User Input Ingestion**: Reads examinee responses from:
   - `user_answers*.json` saved by the **interactive answer sheets** (below) — the default source, auto-discovered in the test dir and cwd. Several files merge, so the 言語知識 and 聴解 halves can be saved separately.
   - Inline CLI arguments (`--answers-gengo` / `--answers-choukai`), which override.
3. **Scaled Score Calculation**: Converts raw section counts into JLPT standardized 0–60 scores:
   - **Language Knowledge (言語知識: 文字・語彙・文法)**: 54 questions max -> scaled to 60.
   - **Reading (読解)**: 21 questions max -> scaled to 60.
   - **Listening (聴解)**: 32 answers max (問題5 3番 yields two) -> scaled to 60.
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
   - Flags weak areas (accuracy < 60%) and provides targeted recommendations referencing _Shin Kanzen Masuta N2_ textbooks (`refs/Shin_Kanzen_Masuta_N2-*.pdf`).
6. **Artifact Output**:
   - Saves `tests/<test_id>/採点結果.md` (Detailed Markdown Report)

The interactive answer sheets are owned by the **`interactive-answer-sheet`**
skill. Those sheets grade their OWN half in-page on button press and emit
`採点結果_言語知識・読解.md` / `採点結果_聴解.md` with no file handling at all —
that is the normal path. **This skill is for the combined 180-point 合否**,
which needs both halves at once and therefore needs their exported JSON.

Their in-page grader is generated FROM this module's `GENGO_QUESTION_TAXONOMY`,
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
   → `tests/1/解答.html` (107 questions total: 75 Gengo/Dokkai + 32 Choukai with audio player).
2. Serve & answer in browser:
   ```bash
   make serve 1
   ```
3. Press **「採点する」** → the full 180-point exam is graded on the spot: the report is shown in the page and saved directly as `tests/1/採点結果.md` and `tests/1/user_answers.json`.
4. Command line grading remains available for batch/offline CLI workflows:
   ```bash
   make grade 1
   # or: python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1
   ```

**The answer key is truncated out of these files.** `build_interactive.py`
aborts if it cannot locate the key heading, rather than risk rendering a sheet
that shows the answers while you solve. Note `言語知識・読解_解答.html` is a
_deliverable_ and distinct from `言語知識・読解.html`, which is a throwaway
intermediate that `build_booklet.py` overwrites.

### Option B: Quick Inline CLI Grading

```bash
python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --answers-gengo "1:4,2:2,3:1,4:1,5:3..." --answers-choukai "問1-1:2,問1-2:3..."
```

---

## 3. Taxonomy Mapping & Scoring Table

These ranges are owned by `jlpt-exam-structure`; this table and
`GENGO_QUESTION_TAXONOMY` in `grade_answers.py` must mirror it exactly. The
script asserts that its ranges tile 1–75 with no gap or overlap at import.

| Section      | Problem | Sub-Category Name                     | Questions           | Raw Items | Scaled Max                  |
| ------------ | ------- | ------------------------------------- | ------------------- | --------- | --------------------------- |
| **言語知識** | 問1     | 漢字読み (Kanji Reading)              | 1–5                 | 5         | -                           |
|              | 問2     | 表記 (Orthography)                    | 6–10                | 5         | -                           |
|              | 問3     | 語形成 (Word Formation)               | 11–15               | 5         | -                           |
|              | 問4     | 文脈規定 (Word in Context)            | 16–22               | 7         | -                           |
|              | 問5     | 言い換え類義 (Paraphrases)            | 23–27               | 5         | -                           |
|              | 問6     | 用法 (Correct Usage)                  | 28–32               | 5         | -                           |
|              | 問7     | 文法形式の判断 (Grammar Form)         | 33–44               | 12        | -                           |
|              | 問8     | 文の組み立て (Sentence Composition ★) | 45–49               | 5         | -                           |
|              | 問9     | 文章の文法 (Text Grammar / Cloze)     | 50–54               | 5         | **60 (Combined, 54 items)** |
| **読解**     | 問10    | 内容理解・短文 (Short Passages)       | 55–59               | 5         | -                           |
|              | 問11    | 内容理解・中文 (Medium Passages)      | 60–68               | 9         | -                           |
|              | 問12    | 統合理解 (A/B Comparative Texts)      | 69–70               | 2         | -                           |
|              | 問13    | 主張理解・長文 (Long Essay)           | 71–73               | 3         | -                           |
|              | 問14    | 情報検索 (Information Retrieval)      | 74–75               | 2         | **60 (21 items)**           |
| **聴解**     | 問題1   | 課題理解 (Task Comprehension)         | 1番–5番             | 5         | -                           |
|              | 問題2   | ポイント理解 (Point Comprehension)    | 1番–6番             | 6         | -                           |
|              | 問題3   | 概要理解 (Summary Comprehension)      | 1番–5番             | 5         | -                           |
|              | 問題4   | 即時応答 (Quick Response)             | 1番–12番            | 12        | -                           |
|              | 問題5   | 統合理解 (Integrated Comprehension)   | 1番–3番 (4 answers) | 4         | **60 (32 items)**           |
| **合計**     |         |                                       |                     | **107**   | **180**                     |

---

## 4. Report Structure (`採点結果.md`)

The generated report contains 4 major sections:

1. **総合判定**: Pass/Fail status, reason for failure if any (overall score < 90 or sectional cutoff < 19).
2. **得点サマリー**: Table showing raw score, scaled score, sectional cutoffs, and overall total.
3. **大問別詳細分析**: Accuracy percentage and evaluation per大問 (`🟢 強 (>=80%)`, `🟡 普通 (60-79%)`, `🔴 要強化 (<60%)`).
4. **弱点診断 & 今後の学習アドバイス**: Targeted textbook practice recommendations for flagged weak areas referencing `refs/Shin_Kanzen_Masuta_N2-*.pdf`.
5. **全設問解答チェック表**: Complete comparison matrix comparing user selection vs correct answer key for every question.

---

## 5. Invariants & Rules

- **Strict Scale Calculation**: Raw scores must be converted proportionally to the 60-point scale per section to reflect real JLPT results accurately.
- **Sectional Cutoff Rules**: Always enforce the 19-point sectional cutoff rule. Even if the total is 120/180, if Reading is 18/60, the result is `不合格`.
- **Reference Integrity**: Advice for weak areas must map directly to the corresponding _Shin Kanzen Masuta N2_ study area (Vocab/Kanji/Grammar/Reading/Listening).
