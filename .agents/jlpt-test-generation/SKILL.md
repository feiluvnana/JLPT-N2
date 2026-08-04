---
name: jlpt-test-generation
description: End-to-end workflow for generating a complete JLPT mock exam (N1-N5, primarily N2). Use this skill whenever the user asks to create, generate, or build a JLPT test, mock exam, 模擬試験, practice test, or any subset of one (言語知識, 文字・語彙, 文法, 読解, 聴解/choukai), or asks to regenerate/fix exam deliverables. This is the entry-point skill — it routes to the specialized skills for each step. Consult it FIRST before any exam work, even for partial requests like "make a listening section" or "create N2 grammar questions".
---

# JLPT Test Generation (Orchestrator)

## Directory Structure & File Naming

All exam files follow a strict directory structure:

- **Reference inputs**: `refs/` directory at workspace root.
  - Textbooks (`refs/Shinkanzen/`): `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-<section>.pdf` (e.g. `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf`).
  - Official Past Exam Sets (`refs/JLPT/`): Booklets, listening scripts, and audio MP3s from the 5 nearest exams (e.g., `refs/JLPT/17.N2 12-2025 _260603.pdf`, `refs/JLPT/JLPT N2 12.2025 Choukai.mp3`).
  - Textbook Audio: `refs/Shinkanzen/Shin_Kanzen_Masuta_<level>-Choukai-CD/`.
- **Test outputs**: `tests/<test_id>/` directory (e.g., `tests/1/` or `tests/n2_mock_01/`).
- **Operational tracking**: `logs/` directory (`logs/ledger.json` for item history, `logs/test_spec.json` for current blueprint).
- **Internal execution scripts** (all are also wrapped by Makefile targets — see
  `make help`; every target takes the test id positionally, e.g. `make sheet 1`):
  - Item pool sampler: `.agents/item-pool-sampling/scripts/sample_items.py` (`make sample`)
  - Web seed blender: `.agents/web-topic-research/scripts/merge_seeds.py` (`make merge-seeds`)
  - Booklet HTML builder: `.agents/exam-booklet-generation/scripts/build_booklet.py` (`make booklet`)
  - Audio generator: `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py` (`make mp3`)
  - Answer-sheet builder: `.agents/interactive-answer-sheet/scripts/build_interactive.py` (`make sheet`)
  - Answer-sheet server: `.agents/interactive-answer-sheet/scripts/serve_sheet.py` (`make serve`)
  - Grader: `.agents/exam-answer-grading/scripts/grade_answers.py` (`make grade`)

### Standard Deliverables in `tests/<test_id>/` (Japanese File Names Mandatory)

| # | File Name | Description / Source |
|---|-----------|----------------------|
| 1 | `言語知識・読解.html` | Booklet rendered from Markdown source `tests/<test_id>/言語知識・読解.md` (no PDF) |
| 2 | `聴解.html` | Booklet rendered from Markdown source `tests/<test_id>/聴解.md` (no PDF) |
| 3 | `聴解スクリプト.txt` (or `script.txt`) | Pure official-style narration text |
| 4 | `聴解.mp3` | Listening audio generated from file 3 |
| 5 | `聴解_チャプター.json` | Per-問題/item offsets in the MP3 (written with it) |
| 6 | `解答.html` | The ONE merged problem+answer sheet — full 107-question exam with radio bubbles, audio player, in-page 180pt grading (`build_interactive.py`) |
| 7 | `採点結果.md`, `user_answers.json` | Written on 「採点する」 from `解答.html`, or by `grade_answers.py` |

## Workflow (follow in order)

1. **Load the format spec** → read `jlpt-exam-structure/SKILL.md`.
   Never write a single question before knowing section counts and booklet conventions.
2. **Calibrate difficulty & benchmark consistency** → read `reference-book-reading/SKILL.md`.
   Locate reference PDFs in `refs/Shinkanzen/` for vocabulary/grammar inventory, and benchmark passage length, distractor structure, and formatting against the 5 official past exams in `refs/JLPT/`.
   Run `official-audio-analysis/SKILL.md` across `refs/JLPT/*.mp3` to ensure pacing parameters match official standards.
3. **Sample item pool & answer key blueprint** → read `item-pool-sampling/SKILL.md`.
   Run: `python3 .agents/item-pool-sampling/scripts/sample_items.py --seed <seed>`
   This outputs `logs/test_spec.json` and updates `logs/ledger.json`.
3.5. **Research fresh topics (Optional / Web available)** → read `web-topic-research/SKILL.md`.
   Harvest 18-25 real-world topic seeds (≥4 source domains) into `logs/seeds.json` and run:
   `python3 .agents/web-topic-research/scripts/merge_seeds.py logs/seeds.json logs/test_spec.json`
   (or `make merge-seeds`, which uses exactly those two paths)
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
6. **Render the booklet HTML (no PDF)** → read `exam-booklet-generation/SKILL.md`.
   Run: `python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/<test_id>/言語知識・読解.md tests/<test_id>/聴解.md`
   (or `make booklet <test_id>`). The browser's Cmd-P is the only renderer — do
   not reintroduce weasyprint/wkhtmltopdf.
7. **Generate MP3 Audio** → read `choukai-mp3-generation/SKILL.md`.
   Run: `python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt` (or `script.txt`)
   Also writes `聴解_チャプター.json` (per-item offsets) for the answer sheet.
8. **Build the interactive answer sheet** → read `interactive-answer-sheet/SKILL.md`.
   Run: `python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/<test_id>`
   (or `make sheet <test_id>`). Produces the single merged `解答.html` — the whole
   booklet with a radio bubble per choice, an audio player for 聴解, and in-page
   180-point grading. Re-run after ANY Markdown edit, like the booklet HTML.
9. **Take the exam & grade** → read `exam-answer-grading/SKILL.md`.
   Serve the sheet (`make serve <test_id>`), answer, and press 「採点する」: the
   report renders in-page and saves `採点結果.md` + `user_answers.json` into
   `tests/<test_id>/`. CLI grading stays available for offline/batch runs:
   `make grade <test_id>` (= `grade_answers.py --test-dir tests/<test_id>`).

## Invariants (apply to every run)

- Japanese file names must be used for all files in `tests/<test_id>/` (`言語知識・読解.md`/`.html`, `聴解.md`/`.html`, `聴解スクリプト.txt`/`script.txt`, `聴解.mp3`, `解答.html`).
- Markdown files in `tests/<test_id>/` are the editable source; regenerate the booklet HTML **and** `解答.html` after ANY content edit.
- Answer keys live at the END of both Markdown sources (`言語知識・読解.md`, `聴解.md`), clearly separated, never inline. `build_interactive.py` aborts if it cannot find the key heading to truncate.
- The booklet (`聴解.md`) and the script (`聴解スクリプト.txt`/`script.txt`) must stay synchronized:
  printed 例 options ↔ spoken 例; any script item change requires a key check.
- After edits, always re-run the dry-run validators described in
  `choukai-script-writing` and `choukai-mp3-generation` (block count, speaker
  map coverage, pause distribution) before shipping.
- Never copy questions from copyrighted textbooks in `refs/`. They are
  calibration references only; all items must be original.


