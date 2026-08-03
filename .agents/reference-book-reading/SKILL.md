---
name: reference-book-reading
description: Single owner of how to read JLPT reference-book PDFs (Shin Kanzen Master, Sou Matome, etc.) for difficulty calibration. Use whenever textbook PDFs are provided or mentioned, whenever the user asks to "check against N2 material", verify difficulty level, or calibrate exam content against a book. These books are typically SCANNED (no text layer) — normal text extraction returns nothing, so this skill's rasterize-the-TOC strategy is mandatory.
---

# Reference Book Reading (calibration strategy)

## Locating Reference Files (`refs/`)

All textbook reference files live in the `refs/` directory at the workspace root.
Standard naming patterns for Shin Kanzen Master PDFs:

- **Grammar**: `refs/Shin_Kanzen_Masuta_<level>-Bunpou.pdf` (e.g. `refs/Shin_Kanzen_Masuta_N2-Bunpou.pdf`)
- **Reading**: `refs/Shin_Kanzen_Masuta_<level>-Dokkai.pdf` (e.g. `refs/Shin_Kanzen_Masuta_N2-Dokkai.pdf`)
- **Listening**: `refs/Shin_Kanzen_Masuta_<level>-Choukai.pdf` (e.g. `refs/Shin_Kanzen_Masuta_N2-Choukai.pdf`)
- **Vocabulary**: `refs/Shin_Kanzen_Masuta_<level>-Goi.pdf` (e.g. `refs/Shin_Kanzen_Masuta_N2-Goi.pdf`)
- **Kanji**: `refs/Shin_Kanzen_Masuta_<level>-Kanji.pdf` (e.g. `refs/Shin_Kanzen_Masuta_N2-Kanji.pdf`)

## Step 1 — Diagnose before reading

```bash
pdfinfo refs/Shin_Kanzen_Masuta_N2-Bunpou.pdf   # page count, size (scanned books are 40-260 MB)
pdffonts refs/Shin_Kanzen_Masuta_N2-Bunpou.pdf  # EMPTY table = scanned = no text layer
```

If `pdffonts` shows no fonts, `pdftotext` is useless. Do NOT attempt OCR of
whole books (250+ pages); use the visual TOC strategy below.

## Step 2 — TOC-first calibration (the key move)

The tables of contents ARE the level inventory. Rasterize only those pages
and read them visually:

```bash
pdftoppm -jpeg -r 100 -f 2 -l 7 refs/Shin_Kanzen_Masuta_N2-Bunpou.pdf toc   # TOC is usually pages 2-7
# then view toc-003.jpg etc.
```

What each Shin Kanzen Master N2 TOC gives you:
- **文法**: the complete grammar-point inventory organized by 課
  (〜かねない, 〜ざるを得ない, 〜に先立って, 〜を契機に, 〜つつも, 〜ようがない,
  〜に限って, 〜ものの, 〜ばかりに, 〜わりに, 〜たところ, 〜末に …).
  Every grammar item in 問題7-9 must appear in this inventory.
- **語彙**: thematic chapter list (人間/生活/仕事/社会/科学/抽象概念/オノマトペ…).
  Vocabulary items should belong to these bands, not N3 basics.
- **漢字**: kanji bands for reading/writing questions.
- **聴解/読解**: question-type frameworks — verify your 問題 typology matches.

## Step 3 — Spot-check individual pages ONLY when needed

Rasterizing costs ~1,600 tokens/page. Budget: TOCs of all books ≈ 10-15 pages.
Only rasterize interior pages to settle a specific dispute (e.g., "is 妥協 in
the N2 band?").

## Rules

- Books in `refs/` are calibration references ONLY. Never copy their questions, example
  sentences, or passages — all exam content must be original.
- State the verification level honestly: "verified at TOC/inventory level"
  vs. page-level verification.
- Common N3-leakage to catch during calibration (reject these as N2 items):
  地域/原因/責任-tier kanji, 〜によると, 〜ば〜ほど, お〜ください-tier keigo,
  ぎりぎり/めったに-tier adverbs.

