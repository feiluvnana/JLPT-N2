---
name: exam-pdf-generation
description: Single owner of rendering exam Markdown sources into print-ready A4 PDFs with correct Japanese typography. Use whenever generating, regenerating, or fixing the exam PDFs, or when the user reports formatting problems (answers squashed on one line, cramped spacing, broken kanji, tables splitting across pages). Never hand-write reportlab for these documents — use the pipeline in scripts/build_pdf.py.
---

# Exam PDF Generation

## Executable & File Paths

- **Script location**: `.agents/exam-pdf-generation/scripts/build_pdf.py`
- **Markdown sources**: `tests/<test_id>/言語知識・読解.md`, `tests/<test_id>/聴解.md`
- **PDF outputs**: `tests/<test_id>/言語知識・読解.pdf`, `tests/<test_id>/聴解.pdf`

## Pipeline

Markdown (source of truth) → python-markdown → styled HTML → wkhtmltopdf → A4 PDF.

Run from workspace root:
```bash
python3 .agents/exam-pdf-generation/scripts/build_pdf.py tests/<test_id>/言語知識・読解.md tests/<test_id>/聴解.md
```

## Non-negotiables baked into the script (know WHY they exist)

1. **`nl2br` extension is mandatory.** Markdown joins consecutive lines into
   one paragraph; without nl2br every vertically-stacked option list collapses
   onto a single unreadable line. (This was a real user complaint.)
2. **CJK fonts**: body = Noto Serif CJK JP (real booklets are serif/明朝),
   headings/bold = Noto Sans CJK JP. Verify installed: `fc-list | grep -i "noto.*cjk"`.
3. **Option widening**: lines holding 3+ options (`1. ◯ 2. ◯ 3. ◯ 4. ◯`) get
   three IDEOGRAPHIC spaces (U+3000) inserted between options — HTML collapses
   ASCII spaces but preserves U+3000. Regular double-spaces are NOT enough.
4. **Table Styling**: `table { width: 100%; border-collapse: collapse; page-break-inside: avoid; }` for full-width exam tables.
5. **Page-break control**: `page-break-inside: avoid` on tables/blockquotes,
   `page-break-after: avoid` on headings. line-height ≥ 1.9 for Japanese.
6. Layout follows jlpt-exam-structure: horizontal options for 文字・語彙・文法,
   vertical for 聴解 and 問題6.
7. **Ruby Furigana**: HTML `<ruby>漢字<rt>かんじ</rt></ruby>` passes through Python-Markdown
   into styled HTML. **The renderer has no ruby layout at all** (WeasyPrint ignores
   `ruby-position`; `display: inline-table` drops the base onto its own line *below*
   the reading — that was the real misalignment bug). So the stack is done by hand:
   `ruby` is an `inline-block` (`position: relative; line-height: 1`) and `rt` is
   `position: absolute; bottom: calc(100% + 0.1em)` with `left/right: -0.6em`.
   Keep `line-height: 1` on `ruby` — anything taller grows its box and floats the
   reading away from the kanji. Two Python passes support this: `fit_ruby()` gives a
   ruby `min-width` when the reading is wider than its base (readings then can't
   collide with the next word's), and `mark_furigana_blocks()` adds `class="furi"`
   (line-height 2.1) only to blocks that contain ruby, so the reading clears the
   line above without loosening plain text.
8. **Vocabulary Notes**: notes (`（注1）...`) use `.vocab-notes` CSS styling
   (font-size: 9pt; line-height: 1.6; top dashed border) to replicate official
   JLPT Dokkai test layout.

## Verification (always, before shipping)

```bash
pdfinfo tests/<test_id>/言語知識・読解.pdf | grep Pages                 # sane page count (N2 file1 ≈ 10-15, file2 ≈ 5)
pdftotext -layout -f 1 -l 2 tests/<test_id>/言語知識・読解.pdf - | head -40   # check continuous numbering (1..75) and wide horizontal gaps
```

- **Verify Question Numbering**: Confirm questions are numbered continuously `1`, `2`, `3`, ..., `75` across section boundaries. (If numbers reset to `1` at Problem 2/3/etc., ensure Markdown source uses `**6**`, `**11**` bold syntax instead of `6.`, `11.` list syntax).
- **Grep for Mojibake**: Ensure zero `\ufffd` characters in output.
- **Answer Key & Explanations**: Confirm answer key and detailed explanations render in section-by-section tables at the end of both PDF documents (`言語知識・読解.pdf` and `聴解.pdf`).



## Environment

Requires: `wkhtmltopdf` **or** `weasyprint` (the script prefers wkhtmltopdf, falls
back to weasyprint — on this machine only weasyprint is installed, so that is what
the furigana CSS is tuned against), `python3 -m pip install markdown pykakasi`,
Noto CJK fonts. `pdftotext` is optional; verification falls back to `pypdf`.
No `pdftoppm` here — proof a page visually with
`gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r140 -dFirstPage=N -dLastPage=N -sOutputFile=p.png file.pdf`.

