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
2. **User Input Ingestion**: Reads examinee responses directly from:
   - Interactive PDF Mark Sheet: `tests/<test_id>/マークシート.pdf` (radio buttons selected in Preview / Acrobat / Chrome).
   - Inline CLI arguments (`--answers-gengo` / `--answers-choukai`).
3. **Scaled Score Calculation**: Converts raw section counts into JLPT standardized 0–60 scores:
   - **Language Knowledge (言語知識: 文字・語彙・文法)**: 54 questions max -> scaled to 60.
   - **Reading (読解)**: 21 questions max -> scaled to 60.
   - **Listening (聴解)**: 31–32 questions max -> scaled to 60.
   - **Total Score**: 180 points max.
4. **Pass / Fail Criteria Evaluation (JLPT N2 Standard)**:
   - **Overall Total**: $\ge 90 / 180$ points.
   - **Sectional Cutoffs (基準点)**: $\ge 19 / 60$ points in **ALL THREE** individual sections:
     - Language Knowledge $\ge 19$
     - Reading $\ge 19$
     - Listening $\ge 19$
   - *Note*: Failing any single sectional cutoff results in **不合格 (FAIL)** regardless of overall total score.
5. **Sub-Question Taxonomy Analysis & Diagnostics**:
   - Evaluates performance per大問 (問1〜問14 for Language/Reading, 問題1〜問題5 for Listening).
   - Flags weak areas (accuracy < 60%) and provides targeted recommendations referencing *Shin Kanzen Masuta N2* textbooks (`refs/Shin_Kanzen_Masuta_N2-*.pdf`).
6. **Artifact Output**:
   - Saves `tests/<test_id>/採点結果.md` (Detailed Markdown Report)

---

## 2. Command Execution

Run the execution script from the workspace root:

### Option A: Interactive PDF & HTML Mark Sheet

1. Generate the clean, multi-column interactive mark sheets (`マークシート.pdf` & `マークシート.html`):
   ```bash
   make template 1
   # or: python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --create-template
   ```
2. Open `tests/<test_id>/マークシート.pdf` or `tests/<test_id>/マークシート.html` in **Chrome, Apple Preview, or Adobe Acrobat**. Click the interactive radio choice bubbles to select your answers, then save/download the file.
3. Grade directly from the completed mark sheet file:
   ```bash
   make grade 1
   # or: python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --user-pdf tests/1/マークシート.pdf
   ```

### Option B: Quick Inline CLI Grading

```bash
python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --answers-gengo "1:4,2:2,3:1,4:1,5:3..." --answers-choukai "問1-1:2,問1-2:3..."
```

---

## 3. Taxonomy Mapping & Scoring Table

| Section | Problem | Sub-Category Name | Questions | Raw Items | Scaled Max |
|---|---|---|---|---|---|
| **言語知識** | 問1 | 漢字読み (Kanji Reading) | 1–8 | 8 | - |
| | 問2 | 表記 (Kanji Writing) | 9–13 | 5 | - |
| | 問3 | 語形成 (Word Formation) | 14–18 | 5 | - |
| | 問4 | 文脈指示 (Contextual Use) | 19–25 | 7 | - |
| | 問5 | 言い換え類義 (Paraphrases) | 26–30 | 5 | - |
| | 問6 | 用法 (Correct Usage) | 31–32 | 2 | - |
| | 問7 | 文の文法1 (Grammar Form) | 33–44 | 12 | - |
| | 問8 | 文の文法2 (Sentence Composition ★) | 45–49 | 5 | - |
| | 問9 | 文章の文法 (Text Grammar / Cloze) | 50–54 | 5 | **60 (Combined)** |
| **読解** | 問10 | 短文読解 (Short Passages) | 55–59 | 5 | - |
| | 問11 | 中文読解 (Medium Passages) | 60–64 | 5 | - |
| | 問12 | 長文読解 (Long Passage) | 65–67 | 3 | - |
| | 問13 | 統合理解 (Comparative Passages) | 68–70 | 3 | - |
| | 問14 | 主張理解/情報検索 (Info Retrieval) | 71–75 | 5 | **60** |
| **聴解** | 問題1 | 課題理解 (Task Comprehension) | 1–5 | 5 | - |
| | 問題2 | ポイント理解 (Point Comprehension) | 1–6 | 6 | - |
| | 問題3 | 概要理解 (Summary Comprehension) | 1–5 | 5 | - |
| | 問題4 | 即時応答 (Quick Response) | 1–12 | 12 | - |
| | 問題5 | 統合理解 (Integrated Comprehension) | 1–4 | 4 | **60** |
| **合計** | | | | **127** | **180** |

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
- **Reference Integrity**: Advice for weak areas must map directly to the corresponding *Shin Kanzen Masuta N2* study area (Vocab/Kanji/Grammar/Reading/Listening).
