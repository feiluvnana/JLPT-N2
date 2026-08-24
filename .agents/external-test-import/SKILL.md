---
name: external-test-import
description: >-
  Imports an external JLPT exam (PDF booklet, optional script PDF, optional
  listening MP3) into this repo's Markdown/HTML/answer-sheet format under
  tests/imported-<slug>/. Use when the user asks to import, convert, ingest, or
  load an outside test/PDF/past paper into the project — not when generating a
  new mock from the item pool.
---

# External Test Import

Single owner of turning an **outside** exam into this repo's deliverables.
Generation stays in `jlpt-test-generation`. Import never samples the pool,
never touches `logs/ledger.json`, and never reuses a bare numeric id like
`tests/5/`.

The source content is authoritative — a real, already-administered exam, so
its questions and answers are correct by construction. Two things can still go
wrong: the **transcription** (OCR slips, mis-keyed rows, dropped notes,
mojibake) and the source **print itself** (a reprinted booklet carries typos).
Checking the copy against the source, and repairing what the source got
plainly wrong, is the whole of the middle step — it is never a
content-quality review of the exam.

## Origin flag (folder name) — NON-NEGOTIABLE

| Origin | Folder name | Example |
|--------|-------------|---------|
| **imported** | MUST start with `imported-` | `tests/imported-n2-2025-12/` |
| **generated** | anything else (no flag) | `tests/1/`, `tests/n2_mock_01/` |

No prefix ⇒ generated; don't invent a second flag. Slug after the prefix:
lowercase ASCII, digits, hyphens only. Every import writes
`tests/<id>/import_meta.json` (provenance); generated tests never get this file.

```bash
python3 .agents/external-test-import/scripts/init_imported_test.py \
  --slug n2-2025-12 \
  --booklet "refs/JLPT_N2_NEW/17.N2 12-2025/17.N2 12-2025 _260603.pdf" \
  --script "refs/JLPT_N2_NEW/17.N2 12-2025/17 (script) N2 12-2025 _260410.pdf" \
  --audio "refs/JLPT_N2_NEW/17.N2 12-2025/JLPT N2 12.2025 Choukai.mp3"
```

## When to use this skill

User provides/points at a PDF (or Markdown dump) of a full or partial exam;
wants a past paper from `refs/JLPT_N2_NEW/` playable via `make serve`; says
import/convert/ingest/load an external test. **Not** this skill: authoring a
new mock → `jlpt-test-generation`.

## Copyright

Sources under `refs/` and user-supplied PDFs are often copyrighted. Import
only for the user's personal practice inside this workspace — never paste
source publisher text into skill docs or redistribute the paper. Prefer
linking paths under `refs/` or user-local files in `import_meta.json` over
copying PDFs into `tests/`.

## The pipeline — three steps, in order

**原文 → 試験そのもの → 内容を目で確認 → 公式解答から模範解答**

1. **Source → the test itself.** Turn the booklet/script/audio into this
   repo's deliverables, transcribing rather than authoring.
2. **Check the content by hand.** Read the transcription against the source
   and repair what the source's own print/OCR got wrong. This is the gate.
3. **Model answer, last.** Only once the content is settled and all 101 keys
   are reconciled against the official key: solve each item from the source,
   confirm the key, then author `詳細解説.json` and render `模範解答.html`.

There is no fourth step. An import has no authored content to critique, so it
never runs the generation-side originality, topic-rotation, or
`exam-qa-review` content-quality passes (`## What not to do`).

Read `jlpt-exam-structure/SKILL.md` before writing any Markdown — counts,
booklet conventions, and 例 mechanics are identical for imported tests.

### Step 1 — Source → the test itself

```bash
python3 .agents/external-test-import/scripts/init_imported_test.py --slug <slug> \
  [--booklet PATH] [--script PATH] [--audio PATH] [--answer-key PATH] [--level N2]
python3 .agents/external-test-import/scripts/extract_pdf_text.py <booklet.pdf> \
  -o tests/imported-<slug>/_extract/booklet.txt
python3 .agents/external-test-import/scripts/extract_pdf_text.py <script.pdf> \
  -o tests/imported-<slug>/_extract/script.txt   # optional
```

`init_imported_test.py` creates `tests/imported-<slug>/` + `import_meta.json`
and fails if the folder exists or the slug is invalid. `_extract/` is an
untracked working cache.

**A sitting already in `refs/JLPT_N2_NEW/` is a shortcut, not an exception.**
`make extract-archive` / `make extract-keys` have already written
`booklet.md` (exact), `key.md` (exact) and `script.md` (**part OCR**) into its
folder — author from those and use the PDFs to settle disputes.
Trust rules: `question-authoring/references/reading-reference-pdfs.md`.

Three extraction failure modes: **no text layer** (a scan — OCR first, say so
and stop rather than inventing content); **mojibake from a CID-keyed font**
(nonsense text with the digits silently dropped — `extract_pdf_text.py`
detects it and retries with pdfminer; never author from a warned extract);
**clean text layer** (the normal path).

Then write the deliverables (same shapes as generated tests — mirror an
existing test for headings, layout and key tables):

| File | Role |
|------|------|
| `言語知識・読解.md` | 問題1–14, 71 keys at end under `# 解答…` |
| `聴解.md` | Booklet options + `# 【正解・解説】` (30 keys) |
| `聴解スクリプト.txt` | Spoken-only script (`choukai-audio` block rules) |

**Prefer the external MP3** (official timing) over synthesizing:

```bash
cp "<audio.mp3>" "tests/imported-<slug>/聴解.mp3"
python3 .agents/external-test-import/scripts/write_external_chapters.py \
  tests/imported-<slug>      # minimal chapters, so make check's MP3⇒chapters rule holds
```

Else `make mp3 imported-<slug>`. Either way the script file is still required
— the gate and the booklet↔script sync read it.

Transcription rules:

- Transcribe what the source says; never "improve" an item or swap a key.
- If the source is incomplete (missing keys, no 聴解 half, **no 例 items**),
  import only what exists and state the gap in the final report.
  Partial imports still use the `imported-` prefix.
- **Restore the lost underlining.** Raw extraction drops it: bold the tested
  word in 問題1/2/5/6 stems (`**相互**`), and bold every numbered passage
  marker (`①**…**`) plus its matching stem span, 1-to-1.
- Keep the source's apparatus — `（注N）`, `（中略）`, setting labels
  (`（旅館で）`), speaker line breaks, printed URLs. Dropping them is a
  fidelity bug, not cleanup.
- 問題8: four blanks, ★ third; key = the option on ★. The 解説 cell MUST open
  with the 1-4 permutation: `語(1)→語(4)→語(3)→語(2)。 「…」`.
- 問題11: official bodies are 4 passages × 2Q even when the instruction says
  `(1)から(3)` (a known print typo on several recent papers). Import BOTH the
  instruction as printed and all four passages — never delete passage (4).
- **問題5 keeps the source's printed 2番 list.** The house rule that 問題5
  prints nothing (`jlpt-exam-structure`) is a GENERATED-paper rule: it is safe
  there because the MP3 is synthesized from the script, so the choices still
  get spoken. An import ships the sitting's own MP3, which never reads 2番's
  choices aloud because official prints them — strip the list and the item
  becomes three unlabelled bubble rows. `check_mondai5_prints_nothing()` and
  `verify_fidelity.py` both skip/handle imports for this reason.

Build as you go: `make booklet imported-<slug> && make sheet imported-<slug>`.

### Step 2 — Check the content by hand

The source is authoritative — a real, already-administered exam — so its items
and answers are correct by construction. What can go wrong is the **copy**:
OCR slips, mis-transcribed digits, dropped notes, mojibake. And the source
print itself can carry an outright typo. Both are yours to fix; nothing else
is.

1. **Answer-key diff — all 101, mechanically.** Parse the 71 gengo + 30
   choukai keys out of the imported Markdown and diff them against the
   official sheet. Zero mismatches. A spot-check misses a mis-typed digit.
   - **Layout trap on official 聴解 answer grids:** 問題4's 7–11 answers often
     sit on the same visual row as 問題5's headers — that five-number run is
     NOT 問題5, which is the separate three-number run (`1番`, `2番 質問1`,
     `2番 質問2`). Prefer the sheet's assignment over a re-solved 解説.
   - After fixing a key, rewrite that row's 解説 from the script/booklet line
     that actually decides it (paste, don't paraphrase).
   - No answer-key source → skip and note the gap; don't invent a diff.
2. **Coverage, both directions.** Every 問題1–9 stem and option, every 読解
   passage opening, every `（注N）` label and `（中略）` marker must appear in
   the import; and every source line must appear in the import unless you
   deliberately changed it. Run it as a script over the extract, not by eye —
   the two directions catch different defects (a dropped note vs. an
   unintended edit).
3. **Repair the source's blatant errors — and only those.** A reprinted
   booklet/script carries real typos, and a learner meets them as nonsense.
   Fix one when the correction is *determined* by the surrounding text:
   a doubled token (`何を何を支え`), a wrong particle (`地元の人か` →
   `人が`), a dropped negation the official key requires (`うん` → `ううん`),
   an obvious mis-set kanji (`完店` → `売店`, `材料登` → `材料費`), a missing
   `に` in a stem. Every repair goes in the final report.
4. **When a line will not resolve, climb the ladder — and stop at the first
   rung that settles it.** The rungs get more expensive downward; never skip
   to the bottom, and never quietly give up above it.

   1. **Re-read the extract in context.** Most OCR damage is obvious once the
      sentence, the four options and the key are in front of you at the same
      time.
   2. **Cross-check inside the source.** The same fact usually appears twice:
      a 聴解 option restates the decisive line, `key.md` and the script PDF's
      own `（正解:N）` corroborate each other, a 読解 stem quotes the passage
      span. Two half-legible copies of one sentence often reconstruct it.
   3. **Rasterize the page and read the image yourself.** `script.md` is ~98%
      OCR and its errors land on exactly the kanji that carry furigana, so the
      text layer can be wrong where the ink is perfectly clear. Render the
      page and LOOK at it:

      ```bash
      pdftoppm -png -r 130 -f <page> -l <page> "<source.pdf>" out      # whole page
      pdftoppm -png -r 300 -f <page> -l <page> \
        -x <px> -y <px> -W <px> -H <px> "<source.pdf>" out             # one line, high dpi
      ```

      **This is the last resort: reading images is slow and expensive, so
      spend it on decisive lines only** — 問題5 統合理解, near-synonym
      place/reason options, any line the official key depends on, any word you
      would otherwise have to guess. Crop to the line and raise the dpi rather
      than re-reading whole pages; a 300 dpi crop settles a single character
      that a 130 dpi full page leaves ambiguous.

   Only after rung 3 has actually been spent may a line be **left as
   printed**. "I could not recover it" is a claim about the ink, so it has to
   be a claim you verified by looking at the ink — record it in the report as
   image-verified, with the page. Guessing at rung 1 and giving up at rung 2
   are the same defect: both ship a sentence nobody checked.
5. **Booklet↔script sync.** 聴解: the printed options for 問題1–2 (and 問題5
   2番) must match what the script says. The marksheet half is `make check`'s
   job; this half is yours.
6. **The gate, then the app.** `make check` — read every line, WARN included.
   `answer_positions` checks skip when there is no `test_spec.json` for this
   id (normal for imports). Then `make serve`: the imported badge renders, the
   audio plays, the sheet grades.

### Step 3 — Model answer from the official key (FINAL STEP)

Only after step 2 is clean and `make check` is green:

```bash
make scaffold-explanations imported-<slug>   # pre-fills stems/options/passages/scripts
# author 詳細解説.json: why_correct, options_analysis, points  (exam-model-answer)
python3 .agents/exam-model-answer/scripts/verify_fidelity.py tests/imported-<slug>
make model-answer imported-<slug>            # -> 模範解答.html
```

**Solve the item before you explain it — every item, one at a time.**
Writing `why_correct` means deriving the answer from the passage or the script
and landing on the keyed option. Do the deriving FIRST, from the source, then
compare with the official key, then write. An explanation written by starting
from the key and reasoning backwards will justify a wrong key as fluently as a
right one — that is the whole failure mode this step exists to catch, and it
is the last point in the pipeline where a mis-key is still cheap to find.

When your solve disagrees with the key:

- Re-read the item. Most disagreements are your own misreading of a
  distractor, or a line the transcription still has wrong — in which case the
  defect is in step 2's output and belongs back there.
- If the disagreement survives, climb step 2's ladder on the deciding line,
  image included. A mis-transcribed negation or particle is the usual cause.
- If it still survives, **the source wins** — key.md and the script PDF's
  `（正解:N）` are the exam's own answer, and an import never re-keys an
  official item. Write the explanation for the keyed option, grounded in the
  line that best supports it, and **report the disagreement**: which item,
  what the source's own text points to, and what you checked.
- Never write an explanation that argues for one option while the key column
  names another. `check_choukai_kaisetsu_keys()` fails that contradiction for
  聴解 automatically; for 言語知識・読解 it is on you.

`exam-model-answer` owns the rest of the quality bar (one `[正解]` per item
matching the official key, a real reason for every option, mandatory
hand-checked furigana, no placeholders, no pipeline metadata). Two things the
scaffold gets wrong on an import and you must fix by hand: 問題9's four stems,
and 問5 2番, which the scaffold emits as one `問5-2` entry where the answer key
needs `問5-2-1` and `問5-2-2`. Running it earlier is prohibited — later content fixes
desynchronize the explanations from the exam.

## What not to do

- Put an imported exam in `tests/1/` (or any id without `imported-`).
- Run `sample_items.py`, or append/update `logs/ledger.json` during import or QA.
- Run generation-style pool-originality, cross-test topic-rotation, or
  `exam-qa-review`'s content-quality QA on imported tests — step 2 is the gate.
- "Fix" an item you merely find odd. Step 2 repairs only what the surrounding
  text or the official key *determines*; anything you would have to guess is
  transcribed as printed and reported.
- Skip `聴解スクリプト.txt` because an external MP3 exists — the gate and
  booklet sync still need the script.
- Treat `refs/Shinkanzen/` textbook PDFs as importable exams (calibration only).

## Downstream skills (after Markdown exists)

| Step | Skill / command |
|------|-----------------|
| Script shape | `choukai-audio` |
| Booklet HTML | `exam-app` / `make booklet <id>` |
| TTS MP3 (if no external audio) | `choukai-audio` / `make mp3 <id>` |
| Answer sheet | `exam-app` / `make sheet <id>` |
| Gate | `make check` |
| Content check | Step 2 above — not `exam-qa-review` |
| Model Answer (Final) | `exam-model-answer` / `make model-answer <id>` |

## Final report (required)

State: source paths and `tests/imported-<slug>/`; what was extracted vs
OCR-blocked; whether audio was copied or synthesized; how the 101 keys
reconciled, and every item where your own solve disagreed with the official
key; **every repair made to the source's own text, and every doubtful line
left as printed — each of the latter named with the page you image-verified
it on**; the `make check` result; and anything skipped.
