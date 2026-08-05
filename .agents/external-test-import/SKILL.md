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
never touches `logs/ledger.json` / `logs/seeds.json`, and never reuses a bare
numeric id like `tests/5/`.

## Origin flag (folder name) — NON-NEGOTIABLE

| Origin | Folder name | Example |
|--------|-------------|---------|
| **imported** | MUST start with `imported-` | `tests/imported-n2-2025-12/` |
| **generated** | anything else (no flag) | `tests/1/`, `tests/n2_mock_01/` |

- No prefix ⇒ **generated**. Do not invent a second flag for generated tests.
- Slug after the prefix: lowercase ASCII, digits, hyphens only
  (`imported-n2-202412`, `imported-shiken-a`). Reject spaces and `/`.
- Write `tests/<id>/import_meta.json` on every import (provenance). Generated
  tests do not get this file.

```bash
# scaffold + meta (does not author Markdown)
python3 .agents/external-test-import/scripts/init_imported_test.py \
  --slug n2-2025-12 \
  --booklet "refs/JLPT/17.N2 12-2025 _260603.pdf" \
  --script "refs/JLPT/17 (script) N2 12-2025 _260410.pdf" \
  --audio "refs/JLPT/JLPT N2 12.2025 Choukai.mp3"
```

## When to use this skill

- User provides / points at a PDF (or Markdown dump) of a full or partial exam
- User wants a past paper from `refs/JLPT/` playable via `make serve`
- User says import / convert / ingest / load external test

**Not** this skill: authoring a new mock → `jlpt-test-generation`.

## Copyright

Sources under `refs/` and user-supplied PDFs are often copyrighted. Import only
for the user's personal practice inside this workspace. Do not paste source
publisher text into skill docs or commit release notes that redistribute the
paper. Prefer linking paths under `refs/` or user-local files in
`import_meta.json` rather than copying PDFs into `tests/`.

## Workflow (run in order)

Read `jlpt-exam-structure/SKILL.md` before writing any Markdown — counts,
booklet conventions, and 例 mechanics are identical for imported tests.

### 1. Choose id and scaffold

```bash
python3 .agents/external-test-import/scripts/init_imported_test.py --slug <slug> \
  [--booklet PATH] [--script PATH] [--audio PATH] [--answer-key PATH] [--level N2]
```

Creates `tests/imported-<slug>/` and `import_meta.json`. Fails if the folder
exists or the slug is invalid.

### 2. Extract source text

```bash
python3 .agents/external-test-import/scripts/extract_pdf_text.py path/to/booklet.pdf \
  -o tests/imported-<slug>/_extract/booklet.txt
# optional:
python3 .agents/external-test-import/scripts/extract_pdf_text.py path/to/script.pdf \
  -o tests/imported-<slug>/_extract/script.txt
```

`_extract/` is a working cache (gitignored pattern recommended; leave untracked).
Scanned PDFs with no text layer need OCR first — say so and stop rather than
inventing content.

### 3. Author project Markdown from the extract

Write the standard deliverable sources (same shapes as generated tests):

| File | Role |
|------|------|
| `言語知識・読解.md` | 問題1–14, 71 keys at end under `# 解答…` |
| `聴解.md` | Booklet options + marksheet 例 + `# 【正解・解説】` (30 keys) |
| `聴解スクリプト.txt` | Spoken-only script (`choukai-script-writing` block rules) |

Mirror an existing test (e.g. `tests/1/`) for headings, option layout, and key
tables. Defer format facts to `jlpt-exam-structure`. Defer script block rules to
`choukai-script-writing`.

**Fidelity rules**

- Transcribe what the source says; do not “improve” items or swap keys.
- If the source is incomplete (missing keys, missing 聴解 half), import only
  what exists, state the gap in the final report, and do not invent answers.
- Partial imports still use the `imported-` prefix.
- 問題8: four blanks, ★ third; key = option that lands on ★ (same integrity
  rules as generated tests — `make check` enforces them).

### 4. Listening audio

**Prefer the external MP3** when the user supplies one (official timing):

```bash
cp "<audio.mp3>" "tests/imported-<slug>/聴解.mp3"
# minimal chapters so make check's "MP3 ⇒ chapters file" rule is satisfied
python3 .agents/external-test-import/scripts/write_external_chapters.py \
  tests/imported-<slug>
```

**Else** synthesize from the imported script:

```bash
make mp3 imported-<slug>
```

### 5. Build + gate

```bash
make booklet imported-<slug>
make sheet imported-<slug>
make check
```

Read every `make check` line. `answer_positions` checks skip when
`logs/test_spec.json` is not for this id (normal for imports). Fix format
failures in the Markdown/script; do not paper over them.

### 6. QA for imports (different from generated)

Do **not** run the generation-style “originality / topic reuse” pass as if you
authored the paper. Instead:

1. Spot-check ≥5 言語知識 items and ≥3 聴解 items against the source PDF/extract
   (stem, options, keyed answer).
2. Confirm booklet ↔ script option sync for 問題1–2 / 問題5-2番.
3. Open `make serve` → test list shows an **imported** badge → sheet loads →
   audio plays if present.

`exam-qa-review` still applies for **solvability / two-defensible-answer /
marksheet 例 sync** defects introduced by a bad transcription — run it on
touched items with fresh eyes after `make check` is green.

## What not to do

- Put an imported exam in `tests/1/` (or any id without `imported-`).
- Run `sample_items.py` / `merge_seeds.py` for an import, or append/update
  `logs/ledger.json`, `logs/seeds.json`, or `logs/test_spec.json` during import or QA.
- Run generation-style pool originality or cross-test topic rotation QA passes on imported tests.
- Skip `聴解スクリプト.txt` because an external MP3 exists — the gate and
  booklet sync still need the script.
- Treat `refs/Shinkanzen/` textbook PDFs as importable exams (calibration only).


## Downstream skills (after Markdown exists)

| Step | Skill / command |
|------|-----------------|
| Script shape | `choukai-script-writing` |
| Booklet HTML | `exam-booklet-generation` / `make booklet <id>` |
| TTS MP3 (if no external audio) | `choukai-mp3-generation` / `make mp3 <id>` |
| Answer sheet | `interactive-answer-sheet` / `make sheet <id>` |
| Gate | `make check` |
| Transcription QA | `exam-qa-review` (fidelity + solvability, not pool originality) |

## Final report (required)

State: source paths, `tests/imported-<slug>/`, what was extracted vs OCR-blocked,
whether audio was copied or synthesized, `make check` result, fidelity
spot-checks done, and anything skipped.
