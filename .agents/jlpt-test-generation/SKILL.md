---
name: jlpt-test-generation
description: End-to-end workflow for generating a complete JLPT mock exam (N1-N5, primarily N2). Use this skill whenever the user asks to create, generate, or build a JLPT test, mock exam, 模擬試験, practice test, or any subset of one (言語知識, 文字・語彙, 文法, 読解, 聴解/choukai), or asks to regenerate/fix exam deliverables. This is the entry-point skill — it routes to the specialized skills for each step. Consult it FIRST before any exam work, even for partial requests like "make a listening section" or "create N2 grammar questions".
---

# JLPT Test Generation (Orchestrator)

## Directory Structure & File Naming

All exam files follow a strict directory structure:

- **Reference inputs**: `refs/` directory at workspace root.
  - Textbooks: `refs/Shin_Kanzen_Masuta_<level>-<section>.pdf` (e.g. `refs/Shin_Kanzen_Masuta_N2-Bunpou.pdf`).
  - Audio: `refs/JLPT <level> <date> Choukai.mp3` (e.g. `refs/JLPT N2 12.2025 Choukai.mp3`) or `refs/Shin_Kanzen_Masuta_<level>-Choukai-CD/`.
- **Test outputs**: `tests/<test_id>/` directory (e.g., `tests/1/` or `tests/n2_mock_01/`).
- **Operational tracking**: `logs/` directory (`logs/ledger.json` for item history, `logs/test_spec.json` for current blueprint).
- **Internal execution scripts**:
  - Item pool sampler: `.agents/item-pool-sampling/scripts/sample_items.py`
  - PDF builder: `.agents/exam-pdf-generation/scripts/build_pdf.py`
  - Audio generator: `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py`

### Standard Deliverables in `tests/<test_id>/` (Japanese File Names Mandatory)

| # | File Name | Description / Source |
|---|-----------|----------------------|
| 1 | `言語知識・読解.pdf` | Rendered from Markdown source `tests/<test_id>/言語知識・読解.md` |
| 2 | `聴解.pdf` | Rendered from Markdown source `tests/<test_id>/聴解.md` |
| 3 | `聴解スクリプト.txt` (or `script.txt`) | Pure official-style narration text |
| 4 | `聴解.mp3` | Listening audio generated from file 3 |

## Workflow (follow in order)

1. **Load the format spec** → read `jlpt-exam-structure/SKILL.md`.
   Never write a single question before knowing section counts and booklet conventions.
2. **Calibrate difficulty & find refs** → read `reference-book-reading/SKILL.md`.
   Locate reference PDFs in `refs/` (e.g., `refs/Shin_Kanzen_Masuta_N2-*.pdf`).
   If audio samples are available in `refs/`, also run `official-audio-analysis/SKILL.md` to extract the pacing table.
3. **Sample item pool & answer key blueprint** → read `item-pool-sampling/SKILL.md`.
   Run: `python3 .agents/item-pool-sampling/scripts/sample_items.py --seed <seed>`
   This outputs `logs/test_spec.json` and updates `logs/ledger.json`.
3.5. **Research fresh topics (Optional / Web available)** → read `web-topic-research/SKILL.md`.
   Harvest 18-25 real-world topic seeds (≥4 source domains) into `seeds.json` and run:
   `python3 .agents/web-topic-research/scripts/merge_seeds.py seeds.json logs/test_spec.json`
   This blends web seeds across ALL surfaces (reading topics, listening scenarios,
   問題9 cloze topic, 問題14 flyer texture, 問題4 settings, 問題1-8 carrier-sentence
   texture) with enforced balance caps: web share 30-60% per surface, pool
   (Shin-Kanzen-calibrated) side always ≥40%, ≤2 seeds per source domain.
   Tested items (grammar/vocab/kanji/idioms) always remain pool-sampled.
   Check the printed blend report before authoring.
4. **Author the content** → read `question-authoring/SKILL.md`.
   Write Markdown sources (`言語知識・読解.md`, `聴解.md`) in `tests/<test_id>/`. Author ONLY items specified in `logs/test_spec.json` and set answer keys according to `answer_positions`.
5. **Write the listening script** → read `choukai-script-writing/SKILL.md`.
   Create `tests/<test_id>/聴解スクリプト.txt` (or `script.txt`). It must contain ONLY spoken exam text.
6. **Render PDFs** → read `exam-pdf-generation/SKILL.md`.
   Run: `python3 .agents/exam-pdf-generation/scripts/build_pdf.py tests/<test_id>/言語知識・読解.md tests/<test_id>/聴解.md`
7. **Generate MP3 Audio** → read `choukai-mp3-generation/SKILL.md`.
   Run: `python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt` (or `script.txt`)

## Invariants (apply to every run)

- Japanese file names must be used for all files in `tests/<test_id>/` (`言語知識・読解.md`/`.pdf`, `聴解.md`/`.pdf`, `聴解スクリプト.txt`/`script.txt`, `聴解.mp3`).
- Markdown files in `tests/<test_id>/` are the editable source; regenerate PDFs after ANY content edit.
- Answer keys live at the END of files 1 and 2, clearly separated, never inline.
- The booklet (file 2: `聴解.md`) and the script (file 3: `聴解スクリプト.txt`/`script.txt`) must stay synchronized:
  printed 例 options ↔ spoken 例; any script item change requires a key check.
- After edits, always re-run the dry-run validators described in
  `choukai-script-writing` and `choukai-mp3-generation` (block count, speaker
  map coverage, pause distribution) before shipping.
- Never copy questions from copyrighted textbooks in `refs/`. They are
  calibration references only; all items must be original.


