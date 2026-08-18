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
its questions and answers are correct by construction. What can still go
wrong is the **transcription**: OCR slips, mis-keyed rows, dropped notes,
mojibake. Everything after authoring is a mechanical check that the copy
matches the source and the project's format — not a content-quality review.

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

## Workflow (run in order)

Read `jlpt-exam-structure/SKILL.md` before writing any Markdown — counts,
booklet conventions, and 例 mechanics are identical for imported tests.

### 1. Choose id and scaffold

```bash
python3 .agents/external-test-import/scripts/init_imported_test.py --slug <slug> \
  [--booklet PATH] [--script PATH] [--audio PATH] [--answer-key PATH] [--level N2]
```

Creates `tests/imported-<slug>/` and `import_meta.json`. Fails if the
folder exists or the slug is invalid.

### 2. Extract source text

```bash
python3 .agents/external-test-import/scripts/extract_pdf_text.py path/to/booklet.pdf \
  -o tests/imported-<slug>/_extract/booklet.txt
python3 .agents/external-test-import/scripts/extract_pdf_text.py path/to/script.pdf \
  -o tests/imported-<slug>/_extract/script.txt   # optional
```

`_extract/` is a working cache, untracked. Three failure modes:

1. **No text layer** (a scan) — every page extracts empty. OCR first; say
   so and stop rather than inventing content.
2. **Mojibake from a CID-keyed font** (Adobe-Japan1 + Identity-H with no
   ToUnicode — ordinary Japanese DTP output). Text is nonsense, not empty,
   and digits vanish (a table "extracts" with no numbers). The script
   detects this and retries with pdfminer (`--engine pdfminer` forces it,
   `--engine pypdf` disables it); it warns if still garbage. Never author
   from a warned extract.
3. **Clean text layer** — the normal path.

### 3. Author project Markdown from the extract

Write the standard deliverable sources (same shapes as generated tests):

| File | Role |
|------|------|
| `言語知識・読解.md` | 問題1–14, 71 keys at end under `# 解答…` |
| `聴解.md` | Booklet options + marksheet 例 + `# 【正解・解説】` (30 keys) |
| `聴解スクリプト.txt` | Spoken-only script (`choukai-audio` block rules) |

Mirror an existing test (e.g. `tests/1/`) for headings/layout/key tables.
Defer format facts to `jlpt-exam-structure`; script block rules to `choukai-audio`.

**Fidelity rules**

- Transcribe what the source says; do not "improve" items or swap keys.
- If the source is incomplete (missing keys, missing 聴解 half), import
  only what exists, state the gap in the final report, never invent answers.
- Partial imports still use the `imported-` prefix.
- **Bold emphasis on tested words & passage markers**: raw PDF extraction
  loses underline formatting, so restore it manually — bold the target
  tested word in 問題1/2/5/6 stems (`**相互**`), and bold all numbered
  passage markers (`①**...**`) plus key target phrases in both the 読解
  body and the matching stem, 1-to-1.
- 問題8: four blanks, ★ third; key = option on ★ (same integrity rules as
  generated tests, `make check` enforces). Explanation cell MUST start with
  the 1-4 permutation: `語(1)→語(4)→語(3)→語(2)。 「...」`.
- （注N） definitions must never be circular (never define a term using its
  own kanji or same phrase).

### 4. Mechanical fidelity checklist (format/transcription verification only)

A copy-matches-source check, not a content review — the source is never
wrong; only the transcription can be. Run all of these before `make check`
in step 6.

1. **Answer-key diff.** When `import_meta.json → answer_key` is set, parse
   all 101 keys (71 gengo + 30 choukai) from the sheet and diff against the
   imported Markdown keys — zero mismatches. A full mechanical diff catches
   mis-transcribed digits a spot-check would miss.
   - **Layout trap on official 聴解 answer grids:** 問題4's 7–11 answers
     often sit on the same visual row as 問題5's headers — don't assign
     that five-number run to 問題5, which is the separate three-number run
     (`1番`, `2番 質問1`, `2番 質問2`). Prefer the sheet's assignment over a
     re-solved 解説.
   - After fixing a key, rewrite that row's 解説 from the script/booklet
     line that actually decides it (paste, don't paraphrase).
   - No answer-key PDF supplied → skip this step, note the gap in the final
     report; don't invent a diff.
2. **Stem/passage presence.** 言語知識: every 問題1–9 stem's distinctive
   12+ char span appears in the booklet extract; 問題6's four sentences
   each appear. 読解: passage openings and every `（注N）` label are
   present, `中略` markers kept.
3. **Booklet↔script sync.** 聴解: booklet options match the script for
   問題1–2 and 問題5-2番; 例 pre-mark = announcer number (the marksheet half
   is `make check`'s job, the dialogue-matches-options half is yours).
4. `make serve` → imported badge renders → audio plays.

**OCR / text-layer hygiene**

- Scanned script PDFs need OCR (`_extract/script_ocr.txt`).
- **Only** when working from an OCR'd scan or a step-2-flagged garbage
  extract: replay decisive listening lines against the external MP3 before
  trusting the transcription — especially 問題5 統合理解 and any near-
  synonym place/reason options. A clean text-layer extraction skips this.
- Clean obvious text-layer glitches when certain (doubled tokens like
  「何を何を支え」→「何を支え」); ambiguous ones (`人か愛着` vs `人が愛情`)
  need a rasterized page check — don't guess, flag it if unclear.
- Preserve source apparatus the project format supports (`（注N）`,
  `（中略）`, setting labels, dialogue turns) — dropping notes during
  transcription is a fidelity bug, not cleanup. When the booklet puts a
  place label on its own line and each speaker on the next, keep that line
  break — don't flatten to one line (the sheet parser accepts multi-line stems).
- 問題11: official bodies are 4 passages × 2Q even when the instruction
  says `(1)から(3)` (a known print typo on several recent papers). Import
  BOTH the instruction as printed and all four passages — never delete
  passage (4) to "match" the header.

### 5. Listening audio

**Prefer the external MP3** when supplied (official timing):

```bash
cp "<audio.mp3>" "tests/imported-<slug>/聴解.mp3"
python3 .agents/external-test-import/scripts/write_external_chapters.py \
  tests/imported-<slug>   # minimal chapters so make check's MP3⇒chapters rule is satisfied
```

**Else** synthesize from the imported script: `make mp3 imported-<slug>`.

### 6. Build + gate

```bash
make booklet imported-<slug>
make sheet imported-<slug>
make check
```

Read every `make check` line. `answer_positions` checks skip when
`test_spec.json` isn't for this id (normal for imports). Fix format
failures in the Markdown/script; don't paper over them.

### 7. QA for imports (different from generated)

Do **not** run the generation-style originality/topic-reuse pass, and do
**not** run `exam-qa-review`'s adversarial content-quality pass — both
exist to catch bad *authoring*, and an import has no authored content to
critique. The gate for an import is `make check` plus the §4 checklist.
When the official sheet and a re-solved 解説 disagree, the sheet wins.

### 8. Model Answer & Detailed Explanation (FINAL STEP)

```bash
make model-answer imported-<slug>  # -> tests/imported-<slug>/模範解答.html
```

**MUST always be the final step** — run only after all 101 keys/questions
are mechanically verified against the official source (§4), audio is
verified, and `make check` is completely green. Generates concise,
learner-friendly explanations with full option-by-option analysis and
mandatory furigana; no internal metadata leaks or placeholder text.

## What not to do

- Put an imported exam in `tests/1/` (or any id without `imported-`).
- Run `sample_items.py`, or append/update `logs/ledger.json` during import or QA.
- Run generation-style pool-originality, cross-test topic-rotation, or
  `exam-qa-review`'s content-quality QA on imported tests — §4 is the gate
  for transcription defects.
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
| Transcription QA | §4 above — not `exam-qa-review` |
| Model Answer (Final) | `exam-model-answer` / `make model-answer <id>` |

## Final report (required)

State: source paths, `tests/imported-<slug>/`, what was extracted vs
OCR-blocked, whether audio was copied or synthesized, `make check` result,
which §4 checklist items were run (and their results), and anything skipped.
