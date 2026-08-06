---
name: reference-book-reading
description: Single owner of how to read JLPT reference PDFs (Shin Kanzen Master textbooks in refs/Shinkanzen/ and the official past-exam archive in refs/JLPT_N2_NEW/) for difficulty calibration and structural consistency, and owner of the measured calibration bands in references/official_calibration.md. Use whenever reference PDFs are provided or mentioned, whenever the user asks to "check against N2 material", verify difficulty level, calibrate exam content, or compare with real JLPT exam booklets.
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

### 2. Official Past Exam Booklets & Scripts
- `refs/JLPT_N2_NEW/` — the **archive: 31 official N2 sittings, 7/2010 – 12/2025**,
  one directory per sitting (booklet PDF + script PDF + MP3), plus the official
  answer keys for all 31 in `ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf`.

**`AGENTS.md` section 3 is the single owner of these filenames** — read the paths
from there rather than copying them here, so a renamed scan only has to be fixed
in one place. (`make check` verifies every path in that table exists.)

### 3. Read the archive as Markdown, not as PDF

`make extract-archive` and `make extract-keys` (see `AGENTS.md` §4) write four
generated files into each sitting's directory, so you can read a past paper with
a file tool instead of a PDF reader:

| file | trust |
|---|---|
| `booklet.md` | **exact** — every booklet PDF has a full text layer |
| `key.md` | **exact** — parsed by colour from the key PDF, validated, and cross-checked 365/365 against the `（正解:N）` in the script PDFs |
| `script.md` | **mixed** — see below |
| `audio_inspection.md` | measured; the *section labels* are this repo's signatures, not measurements |

`script.md` is the one to be careful with. Thirty of the 31 script PDFs draw
their dialogue as 1-bit stencil bitmaps, so no extractor can reach it — only the
問題/N番 setup lines and `（正解:N）` are real text. The dialogue is filled in by
OCR and fenced `[OCR ▼]` … `[OCR ▲]`. Those runs are ~98% character-accurate,
**not exact**, and the errors land on exactly the kanji this skill cares about —
ones carrying furigana (整理→軽理, 一応→一思). So: read OCR'd runs for content
and structure, but **open the PDF before quoting one as official wording, and
never derive a calibration number from inside a fence**. Everything outside the
fences is the exact text layer and is safe to measure.

## Calibrate against the BAND, not against one paper

**`references/official_calibration.md` in this skill folder is the measured
reference.** Every 読解 length, （注N） count, （中略） count, 問題7/8/9 length,
問題1 distractor convention, 問題11 pairing shape and answer-key position
distribution in it was measured across the archive — 31 sittings for the keys,
the last 15 for prose, and the **7 sittings 12/2022 – 12/2025** for anything
format-dependent.

Read it before quoting a number, and observe three rules it establishes:

1. **The exam has eras.** The current blueprint — 71 + 30 items, 問題11 in
   **four** passages of two questions — dates from **12/2022**. Papers before
   that are a different shape (問題11 was 3 passages; 2010–2018 papers carry
   75 + 32 items) and must not be averaged into a 読解 length band.
2. **One paper cannot tell a rule from a coincidence.** Several constants in
   `tools/check_consistency.py` and several rules in `question-authoring` were
   derived from July 2025 alone and fail other official papers — 問題11's
   "one 事実把握 + one 考え/主張 per passage" holds in **1 of 7** current
   sittings; the 問題10/13/14 length floors and the 問題8 option-mass floors each
   fail at least two. §9 of the reference file lists every one with a
   recommended replacement.
3. **Say what you could not measure.** 28 of the 31 script PDFs are image scans
   with no dialogue text, and no 例 appears anywhere in the corpus — those are
   recorded as unavailable in §0, and must not be back-filled with a guess.

## Step 1 — Diagnose before reading

```bash
pdfinfo refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf   # page count, size
pdffonts refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf  # EMPTY table = scanned = no text layer
```

If `pdffonts` shows no fonts, `pdftotext` returns empty results. For scanned books and exam scans, use the visual/rasterize strategy below.

**All of the above needs poppler** (`pdfinfo`/`pdffonts`/`pdftotext`/`pdftoppm`),
and it is NOT part of this repo's documented environment — on a machine without
it every command in this section fails, and the harness cannot rasterize PDF
pages either. Check with `which pdfinfo`; install via `brew install poppler` /
`apt-get install poppler-utils`. Without poppler you still have a text-layer
path, which is enough for the booklet PDFs in `refs/JLPT_N2_NEW/` (they have one):

```bash
python3 .agents/external-test-import/scripts/extract_pdf_text.py \
  "refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf" --pages 1-8 -o /tmp/booklet.txt
python3 -c "import sys;from pdfminer.high_level import extract_text;print(extract_text(sys.argv[1])[:2000])" \
  "refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf"
```

A third diagnosis the two commands above cannot make: a PDF with a real text
layer whose font is CID-keyed with no ToUnicode map extracts as **non-empty
nonsense with the digits silently dropped** — so a 問題数 table reads as labels
with no numbers. `extract_pdf_text.py` detects that and falls back to pdfminer;
see `external-test-import` step 2. Never calibrate off a garbled extract.

## Step 2 — Textbook TOC-first calibration

The tables of contents in `refs/Shinkanzen/` ARE the official level inventory. Rasterize TOC pages to extract target items:

```bash
pdftoppm -jpeg -r 100 -f 2 -l 7 refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf toc
```

- **文法**: complete grammar-point inventory organized by 課 (〜かねない, 〜ざるを得ない, 〜に先立って, 〜を契機に, 〜つつも, 〜ようがない, 〜に限って, 〜ものの, 〜ばかりに, 〜わりに, 〜たところ, 〜末に …). Every grammar item in 問題7-9 must appear in this inventory.
- **語彙**: thematic chapter list (人間/生活/仕事/社会/科学/抽象概念/オノマトペ…).
- **漢字**: kanji bands for reading/writing questions.
- **聴解/読解**: question-type frameworks.

## Step 3 — Official Exam Baseline Calibration (`refs/JLPT_N2_NEW/`)

Use the official past exam PDFs to calibrate overall exam feel, sentence structure, passage lengths, and question phrasing:
1. **Passage & Sentence Lengths**: the measured per-section and per-passage bands
   are in `references/official_calibration.md` §2, over the 7 sittings of the
   current format — use the band, and note that a single sitting (July 2025) is
   not the bar. **The band the GATE enforces still lives in one place only** —
   `question-authoring`'s measured length table, enforced by
   `check_dokkai_lengths()` in `tools/check_consistency.py`. Do not restate
   either here: the numbers were duplicated across four skill files, drifted,
   and the copy in this file carried `≈50+ （注N）` when the reference paper has
   **30 in-body glosses** — an author calibrating against that number could not
   have satisfied it. Where the gate's floor and the measured band disagree,
   `references/official_calibration.md` §9 is the reconciliation and says which
   floors fail an official paper.
2. **Grammar carrier lengths (問題7–9)** — extract text from the booklet PDFs (they have a text layer) and count Japanese characters in each stem / cloze body. Measured bands: `references/official_calibration.md` §7 (180 官方 問題7 stems, 64 問題8 items, 15 問題9 cloze bodies). Note before quoting a floor: **21% of official 問題7 stems are under 30 JP chars, 51% of official 問題8 options are under 5 chars, and bare adverbs on a 問題8 card are official practice** — several `check_consistency.py` floors here fail official papers (§9):
   - **問題7**: measure the per-stem average and the spread; the band and the floor are stated in `question-authoring` and gated by `make check`. What this step adds is the *shape* the numbers do not capture: official papers mix in `（会社で）` / dialogue-turn stems, so a pure monologue set is under-shaped regardless of length, and the fix for a short set is lengthening the situation, never changing the tested form.
   - **問題8**: frames carry context around the blank run — measure the assembled sentence (stem + four options), not the stem alone.
   - **問題9**: measure the cloze body against the band in `question-authoring`. A mini-paragraph is not official length.
   Shin Kanzen `N2-Bunpou` example sentences are also multi-clause situational carriers — use them as a second length check when the PDF is scanned (rasterize a 課 page), never as copyable content.
3. **読解 apparatus**: count `（注N）` and `（中略）` on an official paper before authoring. Count **in-body markers** — one per glossed term, on lines that are not definition lines — because each gloss also has a definition line and counting raw occurrences nearly doubles the figure. That confusion is why the gate reported tests 1–4 at 18/17/58/10 when they carry 9/6/29/5, and why three of them cleared a bar they should have failed. Measured band (§3 of the reference file): **27–61 in-body markers per paper, median 39**, of which 問題12 and 問題14 get **zero** and the count is earned in 問題11 (median 5.5 per 中文 passage) and 問題13 (median 7); **（中略） 2–5 per paper, never 0**. Generated tests that ship a handful of notes and no 中略 fail this calibration even if passage topics look fine.
4. **Distractor Patterns**: Examine how official items create plausible distractors (e.g. 近義語 traps in 問題5, 誤用 types in 問題6, condition traps in 問題14). The recipe, not just the label, is authoritative in `question-authoring`'s "Distractor plausibility" section. Structural conventions confirmed across the archive: 問題2 uses a 2×2 component matrix (swap each of 2 kanji independently, e.g. 傾向/頃向/傾高/頃高); 問題9's four blanks always test four distinct categories (connective / modal / content-inference / idiom), never two of the same; **問題14's 70 and 71 are BOTH person-scenario items in 7 of 7 current papers**, always combining ≥2 constraints, grounded in the printed text, and never phrased 「内容と合っているものはどれか」. **Do NOT carry over the old claim that 問題11 splits each passage into one factual + one opinion question** — measured over 28 official pairs it is 13 one-of-each, 13 two-事実, 2 two-考え, and July 2025 is the only sitting where the split holds for all four passages (§4). What does hold: at least one 考え/主張 stem per 問題11, the 事実把握 stem first, and none of the four banned retrieval shapes anywhere.
5. **Furigana & Vocab Notes**: Benchmark `（注1）` explanations against official formatting in reading passages. Official definition lines use 「ここでは、…」 freely — the repo's ban on that phrase is about glossing a basic word, not about the wording.
6. **Listening Script Phrasing**: Compare spoken option length and dialogue turns against the script PDFs. **Only 12/2023, 7/2024 and 12/2024 have a text layer**; the other 28 are image scans that yield the setup lines and 問い only, so length statistics for spoken options are not derivable from text — rasterize, or use `official-audio-analysis` on the MP3s. Two printed-side conventions are firm across the current format: 問題5's 2番 prints the **same four short labels in the same order** for 質問1 and 質問2 (venue/type/month/route names, never attributes or sentences), and 問題5's instruction has read 「この問題には練習はありません」 since 7/2023.

## Rules

- Files in `refs/` are calibration references ONLY. Never copy questions, example sentences, or passages — all exam content must be original.
- State the verification level honestly, and name the window: "verified against
  the Shin Kanzen inventory and the 7 current-format official sittings
  (12/2022–12/2025) in `refs/JLPT_N2_NEW/`", or whatever you actually measured.
  "5 official past exams" is no longer the corpus.
- **Never report a number you could not compute.** A fabricated calibration
  constant is worse than a missing one: every later paper is built on it.
  `references/official_calibration.md` §0 lists what this corpus cannot answer.
- Reject **off-level** items during calibration — both directions:
  - **Too easy (N3–N5):** 地域/原因/責任-tier kanji, 〜によると, 〜ば〜ほど, お〜ください-tier keigo, ぎりぎり/めったに-tier adverbs, 〜ことができる / 〜たいです as the tested point.
  - **Too hard (N1):** forms absent from Shin Kanzen N2 文法 TOC but headed in N1 lists (〜にあって, 〜をもって, 〜ともなると, 〜を皮切りに, 〜までもなく as productive grammar, …). See `exam-qa-review/references/level_band_grammar.txt`.
- The N2 mock may *expose* harder wording in 読解 with `（注N）`; it must not *key* on an off-level form.

