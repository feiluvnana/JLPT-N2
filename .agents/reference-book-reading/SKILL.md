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
The 5 most recent official JLPT exam sets (booklet + listening script + audio).
**`AGENTS.md` section 3 is the single owner of these filenames** — read the paths
from there rather than copying them here, so a renamed scan only has to be fixed
in one place. (`make check` verifies every path in that table exists.)

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
1. **Passage & Sentence Lengths**: Rasterize/sample reading passages from `refs/JLPT/` (短文 ~200–280, 中文 ~400–550, 長文 ~900–1100) to ensure authoring matches official character density. Prefer measuring a fresh import under `tests/imported-*` when one exists — July 2025 (`imported-n2-2025-07`) is the calibration snapshot: 問題13 ≈1050 JP chars, ≈50+ `（注N）`, multiple `（中略）`.
2. **Grammar carrier lengths (問題7–9)** — extract text from the booklet PDFs (they have a text layer) and count Japanese characters in each stem / cloze body. Measured across 07/2023–12/2025:
   - **問題7**: ~43 JP chars average per stem (median ~41; most items 33–54; occasional short ~25 and long ~70+ dialogue stems). Mock stems averaging under ~35, or a run of under-30 stems, are out of band — lengthen the situation (setting label, subordinate clause, short dialogue), not the tested form. Official papers also mix in `（会社で）` / dialogue-turn stems — pure monologue sets are under-shaped.
   - **問題8**: frames usually carry context around the blank run; assembled sentence (stem + four options) typically lands ~40–70 JP chars.
   - **問題9**: cloze passage body ~500–700 JP chars. A 150–200 char mini-paragraph is not official length.
   Shin Kanzen `N2-Bunpou` example sentences are also multi-clause situational carriers — use them as a second length check when the PDF is scanned (rasterize a 課 page), never as copyable content.
3. **読解 apparatus**: count `（注N）` and `（中略）` on an official paper before authoring. Generated tests that ship 0–2 notes and no 中略 fail this calibration even if passage topics look fine.
4. **Distractor Patterns**: Examine how official items create plausible distractors (e.g. 近義語 traps in 問題5, 誤用 types in 問題6, condition traps in 問題14).
5. **Furigana & Vocab Notes**: Benchmark `（注1）` explanations against official formatting in reading passages.
6. **Listening Script Phrasing**: Compare spoken option length and dialogue turns against the script PDFs in `refs/JLPT/`.

## Rules

- Files in `refs/` are calibration references ONLY. Never copy questions, example sentences, or passages — all exam content must be original.
- State the verification level honestly: "verified against Shin Kanzen inventory and 5 official JLPT past exams".
- Reject **off-level** items during calibration — both directions:
  - **Too easy (N3–N5):** 地域/原因/責任-tier kanji, 〜によると, 〜ば〜ほど, お〜ください-tier keigo, ぎりぎり/めったに-tier adverbs, 〜ことができる / 〜たいです as the tested point.
  - **Too hard (N1):** forms absent from Shin Kanzen N2 文法 TOC but headed in N1 lists (〜にあって, 〜をもって, 〜ともなると, 〜を皮切りに, 〜までもなく as productive grammar, …). See `exam-qa-review/references/level_band_grammar.txt`.
- The N2 mock may *expose* harder wording in 読解 with `（注N）`; it must not *key* on an off-level form.

