---
name: reference-book-reading
description: Single owner of how to read JLPT reference PDFs (Shin Kanzen Master textbooks in refs/Shinkanzen/ and official past JLPT exam booklets & scripts in refs/JLPT/) for difficulty calibration and structural consistency. Use whenever reference PDFs are provided or mentioned, whenever the user asks to "check against N2 material", verify difficulty level, calibrate exam content, or compare with real JLPT exam booklets.
---

# Reference Book & Official Exam Reading (Calibration Strategy)

## Locating Reference Files (`refs/`)

All reference files live under `refs/` at the workspace root:

### 1. Textbook Inventories (`refs/Shinkanzen/`)
Standard naming patterns for Shin Kanzen Master PDFs:
- **Grammar**: `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-Bunpou.pdf`
- **Reading**: `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-Dokkai.pdf`
- **Listening**: `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-Choukai.pdf`
- **Vocabulary**: `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-Goi.pdf`
- **Kanji**: `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-Kanji.pdf`

### 2. Official Past Exam Booklets & Scripts (`refs/JLPT/`)
The 5 most recent official JLPT exam sets (Question Booklets & Listening Scripts):
- **July 2023**: `refs/JLPT/14. N2 7-2023.pdf` & `refs/JLPT/14. N2 7-2023 (script).pdf`
- **Dec 2023**: `refs/JLPT/14.N2 12-2023.pdf` & `refs/JLPT/14. script N2 12-2023.pdf`
- **Dec 2024**: `refs/JLPT/15. N2 12.2024 (update 260625).pdf` & `refs/JLPT/15. script N2 12.2024.pdf`
- **July 2025**: `refs/JLPT/16. N2 07-2025.pdf` & `refs/JLPT/16. N2-7.2025 (script).pdf`
- **Dec 2025**: `refs/JLPT/17.N2 12-2025 _260603.pdf` & `refs/JLPT/17 (script) N2 12-2025 _260410.pdf`

## Step 1 — Diagnose before reading

```bash
pdfinfo refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf   # page count, size
pdffonts refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf  # EMPTY table = scanned = no text layer
```

If `pdffonts` shows no fonts, `pdftotext` returns empty results. For scanned books and exam scans, use the visual/rasterize strategy below.

## Step 2 — Textbook TOC-first calibration

The tables of contents in `refs/Shinkanzen/` ARE the official level inventory. Rasterize TOC pages to extract target items:

```bash
pdftoppm -jpeg -r 100 -f 2 -l 7 refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf toc
```

- **文法**: complete grammar-point inventory organized by 課 (〜かねない, 〜ざるを得ない, 〜に先立って, 〜を契機に, 〜つつも, 〜ようがない, 〜に限って, 〜ものの, 〜ばかりに, 〜わりに, 〜たところ, 〜末に …). Every grammar item in 問題7-9 must appear in this inventory.
- **語彙**: thematic chapter list (人間/生活/仕事/社会/科学/抽象概念/オノマトペ…).
- **漢字**: kanji bands for reading/writing questions.
- **聴解/読解**: question-type frameworks.

## Step 3 — Official Exam Baseline Calibration (`refs/JLPT/`)

Use the 5 official past exam PDFs to calibrate overall exam feel, sentence structure, passage lengths, and question phrasing:
1. **Passage & Sentence Lengths**: Rasterize/sample reading passages from `refs/JLPT/` (中文 ~450 chars, 長文 ~700 chars) to ensure authoring matches official character density.
2. **Distractor Patterns**: Examine how official items create plausible distractors (e.g. 近義語 traps in 問題5, 誤用 types in 問題6, condition traps in 問題14).
3. **Furigana & Vocab Notes**: Benchmark `（注1）` explanations against official formatting in reading passages.
4. **Listening Script Phrasing**: Compare spoken option length and dialogue turns against the script PDFs in `refs/JLPT/`.

## Rules

- Files in `refs/` are calibration references ONLY. Never copy questions, example sentences, or passages — all exam content must be original.
- State the verification level honestly: "verified against Shin Kanzen inventory and 5 official JLPT past exams".
- Reject N3-leakage during calibration: 地域/原因/責任-tier kanji, 〜によると, 〜ば〜ほど, お〜ください-tier keigo, ぎりぎり/めったに-tier adverbs.

