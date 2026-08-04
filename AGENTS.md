# AGENTS.md — Workspace Guidelines for Antigravity

This repository is dedicated to generating, calibrating, rendering, and synthesizing official-quality JLPT mock exams (primarily N2). All agents must strictly follow the skills and rules documented below.

---

## 1. Skill Discovery & Execution Rules

- Skills are located in `.agents/<skill_name>/SKILL.md`.
- Before performing any specialized task, **read the corresponding `SKILL.md` file using `view_file`**.
- Available Skills:
  1. `jlpt-test-generation`: End-to-end mock exam generation orchestrator.
  2. `jlpt-exam-structure`: Official JLPT exam format spec, section layouts, question counts, booklet rules.
  3. `question-authoring`: Writing N2-calibrated exam questions, distractors, and answer keys.
  4. `reference-book-reading`: Reading/calibrating against reference books in `refs/`.
  5. `official-audio-analysis`: Extracting pacing, silence, and loudness parameters from official audio in `refs/`.
  6. `choukai-script-writing`: Authoring pure official-style listening TTS scripts (`.txt`).
  7. `exam-booklet-generation`: Rendering Markdown sources into booklet HTML with A4 print geometry; owns the shared CSS and furigana helpers. No PDF (`build_booklet.py`).
  8. `choukai-mp3-generation`: Synthesizing edge-tts speech audio into exam MP3s (`make_choukai_mp3.py`).
  9. `item-pool-sampling`: Sampling non-repeating items from pool & balancing answer positions (`sample_items.py`).
  10. `web-topic-research`: Sourcing fresh real-world topic seeds, factual texture, and collocation checks from the web, then blending them across ALL exam surfaces (reading, listening, cloze, 問14 flyer, 即時応答 settings, carrier sentences) under enforced balance caps (`merge_seeds.py`).
  11. `exam-answer-grading`: Grading user responses against answer keys, calculating scaled scores (0-180), evaluating Pass/Fail thresholds, analyzing sub-question weak points, and generating diagnostic Markdown reports (`grade_answers.py`).
  12. `interactive-answer-sheet`: Rendering the merged problem+answer sheet — the complete booklet with radio bubbles beside every choice, an in-page audio player for 聴解, and **in-page 180-point grading** that saves `採点結果.md` directly (`build_interactive.py`).

---

## 2. Directory Layout & Japanese File Naming Standards

### Root Directories

- `refs/`: Reference input files (scanned PDFs and audio recordings).
- `tests/<test_id>/`: Output folder for each generated exam (e.g. `tests/1/`, `tests/n2_mock_01/`).
- `logs/`: Operational logs, item coverage ledger (`logs/ledger.json`), test blueprints (`logs/test_spec.json`), and web seed harvests (`logs/seeds.json`).
- `.agents/`: Internal skill definitions, guidelines, and execution scripts.

### Deliverables Naming Convention (Japanese File Names Mandatory)

Inside `tests/<test_id>/`:

| Deliverable                          | File Name                              | Description / Source                                                                   |
| ------------------------------------ | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Language Knowledge & Reading Booklet | `言語知識・読解.html`                  | Rendered from Markdown source `tests/<test_id>/言語知識・読解.md`                      |
| Listening Booklet                    | `聴解.html`                            | Rendered from Markdown source `tests/<test_id>/聴解.md`                                |
| Listening TTS Script                 | `聴解スクリプト.txt` (or `script.txt`) | Pure official-style narration text                                                     |
| Listening Audio MP3                  | `聴解.mp3`                             | Synthesized audio generated from the TTS script                                        |
| Interactive Answer Sheet             | `解答.html`                            | Combined booklet (75 Gengo/Dokkai + 32 Choukai + Audio player); in-page 180pt grading |
| Listening Chapter Marks              | `聴解_チャプター.json`                 | Per-問題/per-item offsets in `聴解.mp3`, written by `make_choukai_mp3.py`              |
| User Answers Record                  | `user_answers.json`                    | Saved automatically on submit from `解答.html`                                         |
| Combined Grading Report              | `採点結果.md`                          | Generated on submit from `解答.html` or written by `grade_answers.py`                  |

---

## 3. Reference Files (`refs/`)

All calibration inputs must be looked up in `refs/`:

- **Textbooks**:
  - Grammar: `refs/Shin_Kanzen_Masuta_N2-Bunpou.pdf`
  - Reading: `refs/Shin_Kanzen_Masuta_N2-Dokkai.pdf`
  - Listening: `refs/Shin_Kanzen_Masuta_N2-Choukai.pdf`
  - Vocabulary: `refs/Shin_Kanzen_Masuta_N2-Goi.pdf`
  - Kanji: `refs/Shin_Kanzen_Masuta_N2-Kanji.pdf`
- **Audio Recordings**:
  - Official audio: `refs/JLPT N2 12.2025 Choukai.mp3`
  - Textbook CDs: `refs/Shin_Kanzen_Masuta_N2-Choukai-CD/`

---

## 4. Pipeline Execution Commands

Always run build/generation scripts from the workspace root:

### Item Pool Sampling (Blueprint Generation & Item Rotation)

```bash
python3 .agents/item-pool-sampling/scripts/sample_items.py --seed 20260803
```

### Web Topic Research (Seed Merging — Optional / When Online)

Harvest 18–25 seeds across ≥4 source domains into `logs/seeds.json` (see `web-topic-research/SKILL.md` for the harvest and N2-gate rules), then:

```bash
python3 .agents/web-topic-research/scripts/merge_seeds.py logs/seeds.json logs/test_spec.json
# optional tuning (both clamped to 0.30–0.60):
#   --reading-ratio 0.5 --listening-ratio 0.4
```

The script blends seeds into every surface of `logs/test_spec.json` (reading topics, listening scenarios, `cloze_topic` for 問9, `info_retrieval_texture` for 問14, `qr_situation_seeds` for 問4, `carrier_seeds` for 問1–8) and prints a **blend report**. Check the report before authoring: web share must sit within 30–60% per surface with the pool side ≥40%, and no source domain may dominate (≤2 topic-level seeds each). Re-harvest and re-run if it warns.

### Booklet Generation (HTML — no PDF)

```bash
python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/<test_id>/言語知識・読解.md tests/<test_id>/聴解.md
```

### Listening MP3 Generation

```bash
python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
```

_(The generator automatically cleans up temporary `segments/` audio files upon successful completion. Pass `--keep-segments` if intermediate files are needed)._

### Exam Answer Grading & Diagnostics

```bash
# Step 1: build the interactive answer sheet (combined booklet + inline radio bubbles)
python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/<test_id>
#   -> tests/<test_id>/解答.html  (107 questions total)

# Step 2: serve & answer in a browser (with direct saving to tests/<test_id>/)
make serve <test_id>
#   or: python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py tests/<test_id>
#   Pressing 「採点する」 automatically saves 採点結果.md & user_answers.json directly into tests/<test_id>/.

# Step 3: command line grading (optional)
python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/<test_id>
#   auto-discovers user_answers*.json in the test dir and cwd
```

The legacy `マークシート.pdf` / `マークシート.html` mark sheets are gone; the
answer sheet is merged into the problem sheet.

---

## 5. Quality Invariants

- **Markdown is single source of truth**: never deleted; the grader and the answer sheet both parse it. Regenerate the booklet HTML **and** the interactive sheets after any content edit.
- **No PDFs**: the booklet is HTML. `@page` CSS is preserved so the browser prints A4. Do not reintroduce weasyprint/wkhtmltopdf.
- **Answer Keys at End**: Placed at the end of `言語知識・読解.md` and `聴解.md`.
- **Booklet ↔ Script Sync**: Options in `聴解.md` must match choices spoken in `聴解スクリプト.txt`.
- **Automatic Segments Cleanup**: Temporary `segments/` files produced during audio generation are automatically removed once `聴解.mp3` is generated.
- **Item Rotation via Ledger**: Always run `item-pool-sampling` before authoring a new test. Item usage is recorded in `logs/ledger.json` to exclude previously tested items from future draws.
- **Web Decorates, Pools Test**: Tested linguistic items (grammar points, vocabulary, kanji, idioms/keigo) are ALWAYS the pool-sampled, Shin-Kanzen-calibrated ones. Web seeds supply only topics, settings, and simplified facts around them — this preserves N2 level regardless of topic freshness.
- **Balanced Source Blend**: When web research runs, every touched surface stays a mix (30–60% web, ≥40% pool; ≤2 seeds per source domain). Provenance (`"origin": "web"|"pool"` + source URL) is recorded in `logs/test_spec.json` for every blended entry and must not be swapped during authoring. Carrier-sentence cap: at most 1 in 3 stems per 問題 may use web texture. Offline runs skip the blend entirely — the pure-pool pipeline remains valid.
- **No Copyright Infringement**: Reference books in `refs/` are for calibration only; questions must be original. Web sources give WHAT to write about, never the words — max one simplified fact per passage/dialogue, no reproduction of source sentences or article structure.
