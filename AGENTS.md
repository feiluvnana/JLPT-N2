# AGENTS.md — Workspace Guidelines

Shared by every agent harness used on this repo (Antigravity, Claude Code, …).
Claude Code reads it via `CLAUDE.md`, which imports this file.

This repository is dedicated to generating, calibrating, rendering, and synthesizing official-quality JLPT mock exams (primarily N2). All agents must strictly follow the skills and rules documented below.

---

## 0. Read the rules in full before you touch anything — NON-NEGOTIABLE

Every defect this repo has shipped came from an agent that had the rule
available and did not read it. Not from a hard problem. From skipping.

- Test 2 shipped duplicated options and mis-keyed 問題8 items; the rules
  forbidding both were already written.
- Test 3 skipped pipeline step 3.5, left the previous test's
  `logs/seeds.json` in place, and reused the previous test's `--seed`. The
  result was a re-skin of test 2 — same web topics, several in the same
  slots. It also shipped all five 問題8 items unsolvable and an unfinished
  English word inside a Japanese passage.

So this is the first rule, and it binds every harness (Antigravity, Claude
Code, and any other):

1. **Read `AGENTS.md` end to end before your first tool call.** Not the
   section you think applies. All of it. It is short on purpose.
2. **Read `jlpt-test-generation/SKILL.md` end to end before ANY exam work** —
   including a partial request ("just the listening section", "just fix the
   MP3"). It routes to the other skills in order.
3. **Read each specialist `SKILL.md` in full before you act in its area**, and
   read it *again* rather than working from memory of a previous session.
   Partial reads are the failure mode: skimming to the code block and running
   the command skips the rules around it.
4. **Execute every numbered step of the workflow, in order.** A step is not
   optional because its output looks like it is already there.
   `logs/seeds.json` and `logs/test_spec.json` are always present — that is
   what makes skipping steps 3 and 3.5 invisible. If a step genuinely does not
   apply (no web access for 3.5), say so explicitly in your final report.
5. **Run `make check` and read every line of its output** before reporting any
   work as done. Green is the floor, not the goal: it cannot see topic reuse,
   two-defensible-answer items, or a passage that repeats last test's subject.
6. **Do the whole-paper pass in `jlpt-test-generation` §"One topic, one
   surface"** — the cross-surface AND cross-test topic table. No script does
   this for you.
7. **State what you did in your final message**: which skills you read, which
   workflow steps you ran, the seed and harvest you used, and anything you
   skipped and why. An unstated skip is the thing that keeps shipping.

If a rule here is wrong or blocks the work, say so and propose a change. Do
not route around it silently.

---

## 1. Skill Discovery & Execution Rules

- Skills are located in `.agents/<skill_name>/SKILL.md`.
- Before performing any specialized task, **read the corresponding `SKILL.md` file** (they are plain Markdown — open them with whatever file-reading tool your harness provides).
- **Claude Code**: the same 12 skills are exposed natively via symlinks in `.claude/skills/<skill_name>` → `.agents/<skill_name>`, so they are auto-discovered and invocable as `/<skill-name>`. `.agents/` remains the single copy — edit files there.
- **`jlpt-test-generation` is the entry point.** Read it FIRST for any exam work, even a partial request like "make a listening section"; it routes to the other skills in order.
- Available Skills:
  1. `jlpt-test-generation`: End-to-end mock exam generation orchestrator — **read this one first**.
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
- `tools/`: Repo-level tooling that is not a skill (`check_consistency.py`, run via `make check`).

`tests/` and `logs/` are committed to git (see §4) — the ledger in particular
must persist, since item rotation depends on the history of past draws.

### Deliverables Naming Convention (Japanese File Names Mandatory)

Inside `tests/<test_id>/`:

| Deliverable                          | File Name                              | Description / Source                                                                   |
| ------------------------------------ | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Language Knowledge & Reading Booklet | `言語知識・読解.html`                  | Rendered from Markdown source `tests/<test_id>/言語知識・読解.md`                      |
| Listening Booklet                    | `聴解.html`                            | Rendered from Markdown source `tests/<test_id>/聴解.md`                                |
| Listening TTS Script                 | `聴解スクリプト.txt`                   | Pure official-style narration text                                                     |
| Listening Audio MP3                  | `聴解.mp3`                             | Synthesized audio generated from the TTS script                                        |
| Interactive Answer Sheet             | `解答.html`                            | Combined booklet (75 Gengo/Dokkai + 32 Choukai + Audio player); in-page 180pt grading |
| Listening Chapter Marks              | `聴解_チャプター.json`                 | Per-問題/per-item offsets in `聴解.mp3`, written by `make_choukai_mp3.py`              |
| User Answers Record                  | `user_answers.json`                    | Saved automatically on submit from `解答.html`                                         |
| Combined Grading Report              | `採点結果.md`                          | Generated on submit from `解答.html` or written by `grade_answers.py`                  |

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
- **Official Past Exam Sets (`refs/JLPT/`) — 5 Nearest Exams (Booklet PDF, Script PDF, Audio MP3)**:
  - **July 2023**: Booklet `refs/JLPT/14. N2 7-2023.pdf`, Script `refs/JLPT/14. N2 7-2023 (script).pdf`, Audio `refs/JLPT/File nghe N2 7-2023.mp3`
  - **Dec 2023**: Booklet `refs/JLPT/14.N2 12-2023.pdf`, Script `refs/JLPT/14. script N2 12-2023.pdf`, Audio `refs/JLPT/14. Nghe N2 T12-2023.mp3`
  - **Dec 2024**: Booklet `refs/JLPT/15. N2 12.2024 (update 260625).pdf`, Script `refs/JLPT/15. script N2 12.2024.pdf`, Audio `refs/JLPT/Nghe N2 T12-2024.mp3`
  - **July 2025**: Booklet `refs/JLPT/16. N2 07-2025.pdf`, Script `refs/JLPT/16. N2-7.2025 (script).pdf`, Audio `refs/JLPT/Nghe N2 T7-2025.mp3`
  - **Dec 2025**: Booklet `refs/JLPT/17.N2 12-2025 _260603.pdf`, Script `refs/JLPT/17 (script) N2 12-2025 _260410.pdf`, Audio `refs/JLPT/JLPT N2 12.2025 Choukai.mp3`

---

## 4. Pipeline Execution Commands

Always run build/generation scripts from the workspace root.

### Makefile Shortcuts (equivalent to the raw commands below — see `make help`)

Every per-test target takes the test id positionally (`make sheet 1`) or as a
variable (`make sheet TEST=1`); it defaults to `1`.

| Command | Runs |
| ------------------------- | -------------------------------------------------- |
| `make check`              | `tools/check_consistency.py` — read-only consistency gate |
| `make sample`             | `sample_items.py --seed $(SEED)` (default `SEED=20260803`) |
| `make merge-seeds`        | `merge_seeds.py logs/seeds.json logs/test_spec.json` |
| `make booklet <test_id>`  | `build_booklet.py` on both Markdown sources        |
| `make mp3 <test_id>`      | `make_choukai_mp3.py` on `聴解スクリプト.txt`       |
| `make sheet <test_id>`    | `build_interactive.py` → `解答.html`               |
| `make serve <test_id>`    | `serve_sheet.py` (browser + direct saving)         |
| `make grade <test_id>`    | `grade_answers.py --test-dir tests/<test_id>`      |

`make sample` reuses the same default seed on every run and has no way to pass
`--test-id`. When generating a new test, either override the seed
(`make sample SEED=<n>`) or call the sampler directly with
`--seed <n> --test-id <id>` so the ledger records attribution — see
`item-pool-sampling/SKILL.md`.

**`tests/` and `logs/` are tracked, on purpose** — they are the working folders
where exams get built and taken, so committing them keeps every generated exam
and the item-rotation state (`logs/ledger.json`) with the repo. Only
`tests/*/segments/` (the temporary per-line audio cache) is gitignored. Commit
new tests and the updated ledger along with the pipeline changes that produced
them.

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

### Consistency Gate (`make check`)

`tools/check_consistency.py` asserts the facts the docs duplicate from the code,
because prose cannot be executed: every `refs/` path named in a doc exists; all
12 skills are listed here and symlinked under `.claude/skills/`; documented
deliverable names appear in the script that writes them and retired ones stay
retired; the choukai pacing table matches `ANSWER_PAUSE`/`GAP_*`; the 大問 table
matches `GENGO_QUESTION_TAXONOMY`; and for every test on disk the script
validates, 75+32 keys parse, the sheet has 107 correctly-sized radio groups, and
the in-page grader agrees with `grade_answers.py` on identical answers.

It also checks item integrity, which no other gate can see: no question offers
the same option twice; all 107 keys sit on the position `logs/test_spec.json`
prescribed; 問題8 stems have four blanks with ★ third, their keys name the
option that lands there, **and the stem does not already contain the words the
options supply**; the passages carry **no un-transliterated Latin words**; the
聴解 script's 問題N instructions match the booklet's verbatim; choices are
spoken only for the 問題 whose booklet prints none (so 問題5-3番's printed
options can't drift from the audio); and the script carries no ASCII `,`/`.`
for edge-tts to mis-time.

It also validates the **blend contract** the authoring step reads off
`logs/test_spec.json`: every surface gets a distinct topic (a repeated entry
silently starves one 問題, which then gets authored off-contract) and the pool
side keeps ≥40% of every blended surface. Both broke in test 4 because
`merge_seeds.py` had been run twice over its own output.

Some rules cannot be decided by matching, so the gate **warns** instead of
failing — currently: a 解説 that quotes text found in neither the passage nor
the script. Warnings are part of the output you must read (§0.5): resolve each
one, or state in your final report why it is a false positive. That warning is
what surfaced test 4's five invented 聴解 quotes, including a keyed option the
audio never speaks.

Finally it checks the **rotation inputs** — the two knobs that decide whether a
new test is actually new. Pool items rotate through the ledger, but the web
blend is a pure function of `(--seed, logs/seeds.json)`: no two tests may share
both, no harvest may be reused (`merge_seeds.py` stamps a `harvest_sha`), and
every `"origin": "web"` entry in the spec must trace back to a seed still
present in `logs/seeds.json`. Test 3 shipped as a re-skin of test 2 — same web
topics, several in the same slots — because it reused test 2's seed against
test 2's untouched harvest, and no other gate could see it.

**Run it after touching any script, skill doc, or test.** It is read-only and
takes a couple of seconds. Every check in it exists because that exact
inconsistency shipped at least once.

---

## 5. Quality Invariants

- **Markdown is single source of truth**: never deleted; the grader and the answer sheet both parse it. Regenerate the booklet HTML **and** the merged answer sheet (`解答.html`) after any content edit.
- **No PDFs**: the booklet is HTML. `@page` CSS is preserved so the browser prints A4. Do not reintroduce weasyprint/wkhtmltopdf.
- **Answer Keys at End**: Placed at the end of `言語知識・読解.md` and `聴解.md`.
- **Booklet ↔ Script Sync**: Options in `聴解.md` must match choices spoken in `聴解スクリプト.txt`.
- **Automatic Segments Cleanup**: Temporary `segments/` files produced during audio generation are automatically removed once `聴解.mp3` is generated.
- **Item Rotation via Ledger**: Always run `item-pool-sampling` before authoring a new test. Item usage is recorded in `logs/ledger.json` to exclude previously tested items from future draws.
- **Web Decorates, Pools Test**: Tested linguistic items (grammar points, vocabulary, kanji, idioms/keigo) are ALWAYS the pool-sampled, Shin-Kanzen-calibrated ones. Web seeds supply only topics, settings, and simplified facts around them — this preserves N2 level regardless of topic freshness.
- **Balanced Source Blend**: When web research runs, every touched surface stays a mix (30–60% web, ≥40% pool; ≤2 seeds per source domain). Provenance (`"origin": "web"|"pool"` + source URL) is recorded in `logs/test_spec.json` for every blended entry and must not be swapped during authoring. Carrier-sentence cap: at most 1 in 3 stems per 問題 may use web texture. Offline runs skip the blend entirely — the pure-pool pipeline remains valid.
- **No Copyright Infringement**: Reference books in `refs/` are for calibration only; questions must be original. Web sources give WHAT to write about, never the words — max one simplified fact per passage/dialogue, no reproduction of source sentences or article structure.
