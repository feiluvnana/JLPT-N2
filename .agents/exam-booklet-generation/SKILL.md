---
name: exam-booklet-generation
description: Single owner of rendering exam Markdown sources into booklet HTML with correct Japanese typography (A4 print geometry preserved, so the browser prints it). Use whenever generating, regenerating, or fixing the exam booklets, or when the user reports formatting problems (answers squashed on one line, cramped spacing, broken kanji, furigana misaligned, tables splitting across pages). Also owns the shared CSS and ruby/furigana helpers that interactive-answer-sheet imports. NO PDF is produced — do not add a PDF step back.
---

# Exam Booklet Generation (HTML)

## Executable & File Paths

- **Script location**: `.agents/exam-booklet-generation/scripts/build_booklet.py`
- **Markdown sources**: `tests/<test_id>/言語知識・読解.md`, `tests/<test_id>/聴解.md`
- **HTML outputs**: `tests/<test_id>/言語知識・読解.html`, `tests/<test_id>/聴解.html`

## Pipeline

Markdown (source of truth) → python-markdown → styled booklet HTML. **That is
the whole pipeline. No PDF.**

```bash
python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/<test_id>/言語知識・読解.md tests/<test_id>/聴解.md
# or: make booklet <test_id>
```

### Why no PDF

`@page { size: A4 }` and the page-break rules are still in the CSS, so
**Cmd-P from the browser gives the same A4 booklet**. Removing the PDF step
removed a real defect class: the furigana CSS had to be tuned for one specific
renderer, and WeasyPrint and wkhtmltopdf laid the absolute-positioned `<rt>`
out differently, so whichever one happened to be on PATH silently changed the
output. The browser is now the only renderer. Do not reintroduce
weasyprint/wkhtmltopdf.

### The two Markdown files stay

`.md` remains the single source of truth and is never deleted — the grader
parses answer keys out of it and `interactive-answer-sheet` parses questions
out of it. Editing HTML by hand is always wrong; edit the Markdown and rebuild.

### Shared with interactive-answer-sheet

`CSS`, `widen()`, `fit_ruby()`, `mark_furigana_blocks()` and
`add_choukai_furigana()` are imported by `build_interactive.py` so the answer
sheet and the booklet render identically. Changing any of them changes both —
rebuild both after touching this file.

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
   into styled HTML. The stack is done by hand rather than with `ruby-position`,
   which the old PDF renderers ignored (`display: inline-table` dropped the base
   onto its own line *below* the reading — the original misalignment bug). Browsers
   would handle native ruby, but the manual layout is kept because it renders
   identically everywhere and `fit_ruby()` depends on it:
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

## Verification (automatic)

`build_booklet.py` runs `verify()` on every build and **aborts** on:

- **mojibake** — any `\ufffd` in the output;
- **`<ol>` in the output** — a stem used `N.` list syntax, which makes
  python-markdown restart numbering at 1 in every section. Stems must be bold
  `**6**`, `**11**` (see question-authoring);
- **a missing bold stem** for any of questions 1–75 in `言語知識・読解.html`,
  which is how a dropped or mis-numbered question gets caught.

Still check by eye: that the answer key and explanations render as
section-by-section tables at the end of both files, and that furigana sits
over its base. Open the HTML and Cmd-P to preview the A4 pagination.



## Environment

Requires only `python3 -m pip install markdown pykakasi` and the Noto CJK JP
fonts. **No PDF toolchain** — no weasyprint, no wkhtmltopdf, no poppler.

