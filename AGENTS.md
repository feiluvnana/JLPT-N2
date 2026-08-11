# AGENTS.md — Workspace Guidelines

Shared by every agent harness used on this repo (Antigravity, Claude Code, …).
Claude Code reads it via `CLAUDE.md`, which imports this file.

This repository generates, calibrates, renders, and synthesizes
official-quality JLPT mock exams (primarily N2). Every rule below has exactly
one owner file; everything else points at it. When two statements disagree,
the owner wins — and the disagreement is a defect to fix, not to route around.

---

## 0. Read the rules in full before you touch anything — NON-NEGOTIABLE

Every defect this repo has shipped came from an agent that had the rule
available and did not read it. Not from a hard problem. From skipping.
(Past defects: duplicated options and mis-keyed 問題8 items despite the rules
already being written; a skipped harvest step that reused a previous seed and
shipped a re-skin of an earlier paper with every automated gate green.)

1. **Read `AGENTS.md` end to end before your first tool call.** All of it.
   It is short on purpose.
2. **For generating a mock, read `jlpt-test-generation/SKILL.md` end to end
   before ANY generation work** — including partial requests ("just the
   listening section", "just fix the MP3"). It owns the 4-stage pipeline and
   the per-stage reading map. **For importing an external PDF/past paper, read
   `external-test-import/SKILL.md` instead** (folder must be
   `tests/imported-<slug>/`).
3. **Read each specialist `SKILL.md` in full before you act in its area** —
   again, not from memory of a previous session. Partial reads are the failure
   mode: skimming to the code block skips the rules around it.
4. **Execute every stage of the workflow, in order.** A stage is not optional
   because its output file already exists — a previous test's
   `test_spec.json` looks exactly like yours. If a stage genuinely does not
   apply, say so in your final report.
5. **Run `make check` and read every line of its output** before reporting any
   work as done. Green is the floor, not the goal: it cannot see topic reuse,
   two-defensible-answer items, or a passage that repeats last test's subject.
6. **Do the whole-paper pass in `jlpt-test-generation` §"One topic, one
   surface"** — the cross-surface AND cross-test topic table. No script does
   this for you.
7. **State what you did in your final message**: which skills you read, which
   stages you ran, the seed you used, and anything you skipped and why. An
   unstated skip is the thing that keeps shipping.

If a rule here is wrong or blocks the work, say so and propose a change. Do
not route around it silently.

---

## 1. Skill Discovery & Execution Rules

- Skills are located in `.agents/<skill_name>/SKILL.md`.
- Before performing any specialized task, **read the corresponding `SKILL.md` file** (they are plain Markdown — open them with whatever file-reading tool your harness provides).
- **Claude Code**: the same 8 skills are exposed natively via symlinks in `.claude/skills/<skill_name>` → `.agents/<skill_name>`, so they are auto-discovered and invocable as `/<skill-name>`. `.agents/` remains the single copy — edit files there.
- **`jlpt-test-generation` is the entry point for generating mocks.** For importing an outside PDF/past paper, read `external-test-import` instead. For any other exam work, read `jlpt-test-generation` first — it routes to the other skills in order.
- Available Skills:
  1. `jlpt-test-generation`: End-to-end mock exam generation orchestrator — **read this one first** for generated exams. Owns the 4-stage pass structure and the per-stage reading map.
  2. `jlpt-exam-structure`: Official JLPT exam format facts — section layouts, question counts, timing, booklet printing conventions, answer-key table format.
  3. `exam-blueprint`: WHAT each exam tests — random non-repeating pool sampling (`sample_items.py`), answer-position balance. Runs before any authoring.
  4. `question-authoring`: HOW to write N2-calibrated items — distractors, item integrity, per-section construction rules (`references/moji-goi.md`, `bunpou.md`, `dokkai.md`, `choukai-items.md`), and calibration against `refs/` (`references/official_calibration.md`).
  5. `choukai-audio`: The listening audio end to end — TTS script format (`聴解スクリプト.txt`), MP3 synthesis with official pacing/voices (`make_choukai_mp3.py`), and the method for measuring official audio.
  6. `exam-app`: Rendering and running the exam — booklet HTML (`build_booklet.py`, no PDF), the merged answer sheet `解答.html` with in-page grading (`build_interactive.py`), the one server (`serve_sheet.py`), the static GitHub Pages build (`build_pages.py`), and CLI grading (`grade_answers.py`).
  7. `exam-qa-review`: The adversarial content QA pass every generated test must survive AFTER `make check` is green and BEFORE it is served or committed — run it with fresh eyes (a context that did not author the test). It also root-causes every finding back to the skill, script, or gate check that let it through, so the next test does not reproduce it.
  8. `external-test-import`: Import an external exam (PDF booklet ± script PDF ± MP3) into `tests/imported-<slug>/` project format — **use instead of generation** when the source already exists outside the pool pipeline.

---

## 2. Directory Layout & Japanese File Naming Standards

### Root Directories

- `refs/`: Reference input files (scanned PDFs and audio recordings). See §3.
- `tests/<test_id>/`: Output folder for each exam. **Origin is encoded in the folder name:** ids starting with `imported-` are external imports (e.g. `tests/imported-n2-2025-12/`); any other id is **generated** (e.g. `tests/1/`). See `external-test-import`.
- `logs/`: Item coverage ledger (`logs/ledger.json`), topic history (`logs/topics.json`), adjunct staging. Each generated test's blueprint lives at `tests/<test_id>/test_spec.json`.
- `.agents/`: The 8 skills — docs, scripts, and reference data.
- `tools/`: Repo-level tooling that is not a skill (`check_consistency.py`, the `refs/` archive extractors).
- `_site/`: **Build output only, gitignored.** The static GitHub Pages copy of the exam app, rebuilt from `tests/` by `make pages` and by CI on push. Never edit or commit it. See `exam-app`.

**`tests/` and `logs/` are tracked, on purpose** — they are the working folders
where exams get built and taken, and the ledger must persist because item
rotation depends on the history of past draws. Commit new tests and the updated
ledger together with the pipeline changes that produced them. Gitignored
build/cache paths: `tests/*/segments/`, `tests/*/_extract/`,
`tests/*/_sections/`, `qa/*/` (keyless renders — `qa/qa-report-*.md` stays
tracked), `_site/`.

### Deliverables Naming Convention (Japanese File Names Mandatory)

Inside `tests/<test_id>/` — this table is the single copy; skills point here:

| Deliverable                          | File Name                              | Description / Source                                                                   |
| ------------------------------------ | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Language Knowledge & Reading Booklet | `言語知識・読解.html`                  | Rendered from Markdown source `tests/<test_id>/言語知識・読解.md`                      |
| Listening Booklet                    | `聴解.html`                            | Rendered from Markdown source `tests/<test_id>/聴解.md`                                |
| Listening TTS Script                 | `聴解スクリプト.txt`                   | Pure official-style narration text                                                     |
| Listening Audio MP3                  | `聴解.mp3`                             | Synthesized audio generated from the TTS script                                        |
| Interactive Answer Sheet             | `解答.html`                            | Combined booklet (71 Gengo/Dokkai + 30 Choukai + Audio player); in-page 180pt grading |
| Listening Chapter Marks              | `聴解_チャプター.json`                 | Per-問題/per-item offsets in `聴解.mp3`, written by `make_choukai_mp3.py`              |
| User Answers Record                  | `ユーザー解答.json`                    | Saved automatically on submit from `解答.html`                                         |
| Combined Grading Result              | `採点結果.json`                        | Generated on submit from `解答.html` or written by `grade_answers.py`. There is no Markdown report — the result is data, read back by the result screen and by the test list |
| Import provenance (imported only)    | `import_meta.json`                     | Written by `external-test-import` for `tests/imported-<slug>/` only — generated tests must not have this file |

---

## 3. Reference Files (`refs/`)

All calibration inputs must be looked up in `refs/`:

- **Textbooks (`refs/Shinkanzen/`)**:
  - Grammar: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf`
  - Reading: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Dokkai.pdf`
  - Listening: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai.pdf`
  - Vocabulary: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Goi.pdf`
  - Kanji: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Kanji.pdf`
  - Textbook CDs: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai-CD/`
- **Textbooks (`refs/Soumatome/`) — 日本語総まとめ N2**:
  - Vocabulary: `refs/Soumatome/nihongo-soumatome-n2-goi.pdf`
  - Kanji: `refs/Soumatome/nihongo-soumatome-n2-kanji.pdf`
  - Together with Shinkanzen's Goi/Kanji volumes, these are exam-blueprint's
    ONLY vocabulary/kanji pool authority (`pools.json`'s `kanji_reading`,
    `context_words`, `paraphrase`, `usage`) — the vendored OpenJLPT JSON corpus
    was removed 2026-08-11 (exam-blueprint/SKILL.md). Both Soumatome PDFs are
    scanned images with no text layer (confirmed via `pdftotext`), same as
    Shinkanzen — read them via the pages-parameter PDF support, never assume a
    grep-able extract exists.
- **Official Past Exam Archive (`refs/JLPT_N2_NEW/`) — 31 Sittings (Booklet PDF, Script PDF, Audio MP3)**:
  - **July 2023**: Booklet `refs/JLPT_N2_NEW/14. N2 7-2023/14. N2 7-2023.pdf`, Script `refs/JLPT_N2_NEW/14. N2 7-2023/14. N2 7-2023 (script).pdf`, Audio `refs/JLPT_N2_NEW/14. N2 7-2023/File nghe N2 7-2023.mp3`
  - **Dec 2023**: Booklet `refs/JLPT_N2_NEW/14. N2 12-2023/14.N2 12-2023.pdf`, Script `refs/JLPT_N2_NEW/14. N2 12-2023/14. script N2 12-2023.pdf`, Audio `refs/JLPT_N2_NEW/14. N2 12-2023/14. Nghe N2 T12-2023.mp3`
  - **Dec 2024**: Booklet `refs/JLPT_N2_NEW/15. N2 12-2024/15. N2 12.2024 (update 260625).pdf`, Script `refs/JLPT_N2_NEW/15. N2 12-2024/15. script N2 12.2024.pdf`, Audio `refs/JLPT_N2_NEW/15. N2 12-2024/Nghe N2 T12-2024.mp3`
  - **July 2025**: Booklet `refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf`, Script `refs/JLPT_N2_NEW/16. N2 7-2025/16. N2-7.2025 (script).pdf`, Audio `refs/JLPT_N2_NEW/16. N2 7-2025/Nghe N2 T7-2025.mp3`
  - **Dec 2025**: Booklet `refs/JLPT_N2_NEW/17.N2 12-2025/17.N2 12-2025 _260603.pdf`, Script `refs/JLPT_N2_NEW/17.N2 12-2025/17 (script) N2 12-2025 _260410.pdf`, Audio `refs/JLPT_N2_NEW/17.N2 12-2025/JLPT N2 12.2025 Choukai.mp3`

Every folder also carries agent-readable extracts (`booklet.md`, `script.md`,
`key.md`, `audio_inspection.md`) written by `make extract-archive` /
`make extract-keys`. **`booklet.md` and `key.md` are exact; `script.md` is
partly OCR** — trust rules and mechanics:
`question-authoring/references/reading-reference-pdfs.md`.

---

## 4. Pipeline Execution Commands

Always run from the workspace root. Each command's rules and options live in
its owner skill — this table is the router, not the manual. Per-test targets
take the id positionally (`make sheet 1`) or as `TEST=1`; default `TEST=1`.

**Environment prerequisites and per-OS setup (macOS, Windows/WSL2) are owned by
`README.md`** — the interpreter and package versions, the external binaries
these commands shell out to, and the Git LFS/symlink/CRLF requirements. Do not
restate them here or in a skill; fix them there.

| Command | Runs | Owner skill |
| ------------------------- | ------------------------------------ | ----------- |
| `make check`              | `tools/check_consistency.py` — the read-only gate | (below) |
| `make check-tests`        | the same gate, per-test contracts only | (below) |
| `make sample <id> SEED=n` | `sample_items.py` → `test_spec.json` + ledger | `exam-blueprint` |
| `make booklet <id>`       | `build_booklet.py` on both Markdown sources | `exam-app` |
| `make mp3 <id>`           | `make_choukai_mp3.py` on `聴解スクリプト.txt` | `choukai-audio` |
| `make sheet <id>`         | `build_interactive.py` → `解答.html` | `exam-app` |
| `make keyless <id>`       | the QA blind-solve render → `qa/<id>/keyless.md` | `exam-app` |
| `make serve`              | `serve_sheet.py` — ONE server for every test (no id) | `exam-app` |
| `make grade <id>`         | `grade_answers.py --test-dir tests/<id>` | `exam-app` |
| `make pages [<id>]`       | `build_pages.py` — static GitHub Pages site → `_site/` | `exam-app` |
| `make preview-pages`      | serves `_site/` locally | `exam-app` |
| `make init-import SLUG=…` | `init_imported_test.py` — scaffold `tests/imported-<slug>/` | `external-test-import` |
| `make extract-pdf PDF=… OUT=…` | `extract_pdf_text.py` | `external-test-import` |
| `make extract-archive`    | `extract_jlpt_n2_new.py --all` — past-paper archive → Markdown | §3 above |
| `make extract-keys`       | `extract_jlpt_n2_key.py` — key PDF → `key.md` + JSON | §3 above |

The pool-growth tooling (classify/promote/expand/suggest/fetch) is parked in
`.agents/exam-blueprint/archive/` with no make targets — see its README.

### Consistency Gate (`make check`)

`tools/check_consistency.py` asserts the facts the docs duplicate from the
code, plus every item-integrity, blend, rotation, and app-deployment contract
that has ever shipped broken — each check exists because that exact
inconsistency shipped at least once, and **each check's docstring and failure
message are its own documentation**: when a line fails, the message tells you
the rule, the incident behind it, and the repair.

- **Run it after touching any script, skill doc, or test.** Read every line.
- FAIL blocks the work. **WARN is part of the output** (§0.5): warn-class
  checks exist where a rule cannot be decided by string matching — resolve
  each one or state in your final report why it is a false positive.
- Green is the floor, never the verdict on a paper — `exam-qa-review` is.
  Several binding authoring rules are read by QA only, not by the gate
  (`question-authoring` §"Answer keys — format pointers and the required
  artifacts" lists which of its required key-table artifacts the
  gate actually reads); do not skip one because `make check` is green.

---

## 5. Pass structure — orchestrate, don't work

The generation pipeline runs as **4 stages** — blueprint → 4 parallel
authoring sections → build+gate → fresh-eyes QA — each a subagent with a
bounded reading list, handing off through files on disk only.
`jlpt-test-generation` owns the stage table, the reading map, the prompt
template, and the fix→re-review loop; read it before any generation work.

The two context-isolation rules that are never optional, in any harness or
fallback: **no long single-run authoring** (defects cluster in whatever one
context writes last), and **QA in a context that authored nothing** (an author
cannot audit its own intent — every shipped mis-key survived its author's own
review). With no subagents available, approximate the stages with separate
sessions; the minimum split that survives every fallback is authoring vs QA,
two contexts.
