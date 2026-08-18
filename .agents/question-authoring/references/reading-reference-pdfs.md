# Reading the reference PDFs (`refs/`) — mechanics and trust rules

Section reference for the `question-authoring` skill, absorbed from the retired
`reference-book-reading` skill (retired; absorbed here). Read the core `SKILL.md` §"Calibrate to the
BAND" first — it owns the calibration rules; this file owns the mechanics of
getting readable text out of the PDFs. **`AGENTS.md` §3 is the single owner of
the `refs/` path list** — read the paths there rather than copying them here
(`make check` verifies every path in that table exists).

## Read the archive as Markdown, not as PDF

`make extract-archive` / `make extract-keys` (`AGENTS.md` §4) write four
generated files into each `refs/JLPT_N2_NEW/` sitting directory:

| file | trust |
|---|---|
| `booklet.md` | **exact** — every booklet PDF has a full text layer |
| `key.md` | **exact** — colour-parsed from the key PDF, validated, cross-checked 365/365 against the script PDFs' `（正解:N）` |
| `script.md` | **mixed** — see below |
| `audio_inspection.md` | measured; its section LABELS are this repo's signatures, not measurements — attribute them yourself |

`script.md` is the one to be careful with. Thirty of the 31 script PDFs draw
their dialogue as 1-bit stencil bitmaps, so no extractor can reach it — only
the 問題/N番 setup lines and `（正解:N）` are real text. OCR fills the
dialogue in, fenced `[OCR ▼]` … `[OCR ▲]`. Those runs are ~98%
character-accurate, **not exact**, and errors land on exactly the kanji
that carry furigana (整理→軽理, 一応→一思). Read fenced runs for content and
structure, but **open the PDF before quoting one as official wording, and
never derive a calibration number from inside a fence** — everything
outside the fences is the exact text layer and safe to measure. Only
12/2023, 7/2024, and 12/2024 script PDFs have a text layer, so spoken-option
length isn't derivable from text — rasterize, or measure the MP3s via `choukai-audio`.

## Step 1 — Diagnose before reading

```bash
pdfinfo  refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf   # page count, size
pdffonts refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf   # EMPTY table = scanned = no text layer
```

If `pdffonts` shows no fonts, `pdftotext` returns empty results — use the
rasterize strategy below. All of this needs **poppler**
(`pdfinfo`/`pdffonts`/`pdftotext`/`pdftoppm`), which is NOT part of this repo's
documented environment: check `which pdfinfo`; install via
`brew install poppler` / `apt-get install poppler-utils`. Without poppler the
text-layer path still works for the `refs/JLPT_N2_NEW/` booklets (they have
one):

```bash
python3 .agents/external-test-import/scripts/extract_pdf_text.py \
  "refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf" --pages 1-8 -o /tmp/booklet.txt
python3 -c "import sys;from pdfminer.high_level import extract_text;print(extract_text(sys.argv[1])[:2000])" \
  "refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf"
```

**The CID-font trap** — a third state the two diagnoses above cannot see: a PDF
with a real text layer whose font is CID-keyed with **no ToUnicode map**
extracts as non-empty NONSENSE with the digits silently dropped — a 問題数
table reads as labels with no numbers. `extract_pdf_text.py` detects that and
falls back to pdfminer; see `external-test-import` step 2. Never calibrate off
a garbled extract.

## Step 2 — Rasterize fallback: TOC-first textbook calibration

The tables of contents in `refs/Shinkanzen/` ARE the official level inventory:
文法 grammar points organized by 課 (every 問題7–9 item must appear in it),
語彙 thematic chapters (人間/生活/仕事/社会/科学/抽象概念/オノマトペ…), 漢字
bands, and the 読解/聴解 question-type frameworks. Rasterize the TOC pages:

```bash
pdftoppm -jpeg -r 100 -f 2 -l 7 refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf toc
```

Shin Kanzen `N2-Bunpou` example sentences are multi-clause situational
carriers — usable as a second length check for 問題7–9 when a PDF is scanned
(rasterize a 課 page), never as copyable content: `refs/` is calibration-only
(core calibration rules).
