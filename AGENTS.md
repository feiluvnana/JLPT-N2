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
2. **For generating a mock, read `jlpt-test-generation/SKILL.md` end to
   end before ANY generation work** — including a partial request ("just the
   listening section", "just fix the MP3"). It routes to the other skills in
   order. **For importing an external PDF/past paper, read
   `external-test-import/SKILL.md` instead** (folder must be
   `tests/imported-<slug>/`).
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
- **Claude Code**: the same 14 skills are exposed natively via symlinks in `.claude/skills/<skill_name>` → `.agents/<skill_name>`, so they are auto-discovered and invocable as `/<skill-name>`. `.agents/` remains the single copy — edit files there.
- **`jlpt-test-generation` is the entry point for generating mocks.** For importing an outside PDF/past paper, read `external-test-import` instead. For any other exam work, read `jlpt-test-generation` first — it routes to the other skills in order.
- Available Skills:
  1. `jlpt-test-generation`: End-to-end mock exam generation orchestrator — **read this one first** for generated exams.
  2. `jlpt-exam-structure`: Official JLPT exam format spec, section layouts, question counts, booklet rules.
  3. `question-authoring`: Writing N2-calibrated exam questions, distractors, and answer keys.
  4. `reference-book-reading`: Reading/calibrating against reference books in `refs/`.
  5. `official-audio-analysis`: Extracting pacing, silence, and loudness parameters from official audio in `refs/`.
  6. `choukai-script-writing`: Authoring pure official-style listening TTS scripts (`.txt`).
  7. `exam-booklet-generation`: Rendering Markdown sources into booklet HTML with A4 print geometry; owns the shared CSS and furigana helpers. No PDF (`build_booklet.py`).
  8. `choukai-mp3-generation`: Synthesizing edge-tts speech audio into exam MP3s (`make_choukai_mp3.py`).
  9. `item-pool-sampling`: Sampling non-repeating items from pool & balancing answer positions (`sample_items.py`).
  10. `web-topic-research`: Sourcing fresh real-world topic seeds, factual texture, and collocation checks from the web, then blending them across ALL exam surfaces (reading, listening, cloze, 問14 flyer, 即時応答 settings, carrier sentences) under enforced balance caps (`merge_seeds.py`).
  11. `exam-answer-grading`: Grading user responses against answer keys, calculating scaled scores (0-180), evaluating Pass/Fail thresholds, analyzing sub-question weak points, and writing the structured result document `採点結果.json` (`grade_answers.py`).
  12. `interactive-answer-sheet`: Rendering the merged problem+answer sheet — the complete booklet with radio bubbles beside every choice, an in-page audio player for 聴解, **in-page 180-point grading** that saves `採点結果.json` directly (`build_interactive.py`), and the one server that lists every test and runs them (`serve_sheet.py`).
  13. `exam-qa-review`: The adversarial content QA pass every generated test must survive AFTER `make check` is green and BEFORE it is served or committed — run it with fresh eyes (a context that did not author the test). It also root-causes every finding back to the skill, script, or gate check that let it through (§6.5), so the next test does not reproduce it.
  14. `external-test-import`: Import an external exam (PDF booklet ± script PDF ± MP3) into `tests/imported-<slug>/` project format — **use instead of generation** when the source already exists outside the pool pipeline.

---

## 2. Directory Layout & Japanese File Naming Standards

### Root Directories

- `refs/`: Reference input files (scanned PDFs and audio recordings).
- `tests/<test_id>/`: Output folder for each exam. **Origin is encoded in the folder name:** ids starting with `imported-` are external imports (e.g. `tests/imported-n2-2025-12/`); any other id is **generated** (e.g. `tests/1/`, `tests/n2_mock_01/`). See `external-test-import`.
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
| `make check-tests`        | the same gate with `--tests` (per-test contracts only) |
| `make sample`             | `sample_items.py --seed $(SEED)` (default `SEED=20260803`) |
| `make classify ITEM=…`    | `classify_level.py` — optional `CATEGORY=`, `STAGE=1` |
| `make promote-adjunct`    | `promote_adjunct.py` — approved staging → `pools.json` |
| `make expand-pools`       | `expand_pools.py` — OpenJLPT N2 + curated topic growth |
| `make fetch-openjlpt`     | `fetch_openjlpt.py` — refresh vendored OpenJLPT slices |
| `make suggest-pool`       | `suggest_pool_additions.py` — optional `WRITE_STAGING=1` |
| `make merge-seeds`        | `merge_seeds.py logs/seeds.json logs/test_spec.json` |
| `make booklet <test_id>`  | `build_booklet.py` on both Markdown sources        |
| `make mp3 <test_id>`      | `make_choukai_mp3.py` on `聴解スクリプト.txt`       |
| `make sheet <test_id>`    | `build_interactive.py` → `解答.html`               |
| `make serve`              | `serve_sheet.py` — ONE server for every test (takes no test id) |
| `make grade <test_id>`    | `grade_answers.py --test-dir tests/<test_id>`      |
| `make init-import SLUG=…` | `init_imported_test.py --slug <slug>` — **slug only**; pass `--booklet/--script/--audio` with the raw command below |
| `make extract-pdf PDF=… OUT=…` | `extract_pdf_text.py` |

Every per-test target also has a `-<id>` form (`make sheet-1`, `make mp3-2`),
which is what to use when the target is not the first goal on the command line —
the positional form only works there.

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
# adjunct one-shots: classify → --stage, then sample (cap 20%); --no-adjunct for pure pool
python3 .agents/item-pool-sampling/scripts/classify_level.py --item '措置' --category context_words --stage
python3 .agents/item-pool-sampling/scripts/promote_adjunct.py
python3 .agents/item-pool-sampling/scripts/expand_pools.py
```

### Web Topic Research (Seed Merging — Optional / When Online)

Harvest 18–25 seeds across **≥6 distinct source domains** into `logs/seeds.json` (`MAX_PER_DOMAIN` is 2, so fewer domains cannot fund every surface's 30% floor — test 4's 聴解 landed at 20% web from a 5-domain harvest; see `web-topic-research/SKILL.md` for the arithmetic and N2-gate rules), then:

```bash
python3 .agents/web-topic-research/scripts/merge_seeds.py logs/seeds.json logs/test_spec.json
# optional tuning (both clamped to 0.30–0.60):
#   --reading-ratio 0.5 --listening-ratio 0.4
```

The script blends seeds into every surface of `logs/test_spec.json` (reading topics, listening scenarios, `cloze_topic` for 問9, `info_retrieval_texture` for 問14, `qr_situation_seeds` for 問4, `carrier_seeds` for 問1–8) and prints a **blend report**. Check the report before authoring: web share must sit within 30–60% per surface with the pool side ≥40%, and no source domain may dominate (≤2 topic-level seeds each). Re-harvest and re-run if it warns.

### External Test Import (PDF / past paper → project format)

Folder ids **must** start with `imported-` (e.g. `tests/imported-n2-2025-12/`). No prefix means **generated**. See `external-test-import/SKILL.md`.

```bash
python3 .agents/external-test-import/scripts/init_imported_test.py --slug n2-2025-12 \
  --booklet "path/to/booklet.pdf" --script "path/to/script.pdf" --audio "path/to.mp3"
python3 .agents/external-test-import/scripts/extract_pdf_text.py booklet.pdf \
  -o tests/imported-n2-2025-12/_extract/booklet.txt
# then author Markdown from the extract, then:
make booklet imported-n2-2025-12 && make sheet imported-n2-2025-12 && make check
```

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
#   -> tests/<test_id>/解答.html  (101 questions total)

# Step 2: serve & answer in a browser — ONE server covers every test, so no id here
make serve
#   or: python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py [--port 8765] [--no-open]
#   Screen 1 (`/`)                        the test list, with each test's progress and last score
#   Screen 2 (`/tests/<test_id>/解答.html`) the exam; every click saves ユーザー解答.json
#   Screen 3 (in page, after 「採点する」)   the result, saved as 採点結果.json, with a back button
#   A graded test opens straight on screen 3 from the list, and can still be redone.

# Step 3: command line grading (optional)
python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/<test_id>
#   auto-discovers ユーザー解答*.json in the test dir and cwd; writes 採点結果.json
```

The legacy `マークシート.pdf` / `マークシート.html` mark sheets are gone; the
answer sheet is merged into the problem sheet. The per-test server is gone too —
`make serve <id>` no longer exists, and so is the Markdown grading report, which
is now the JSON document both graders write.

---

### Consistency Gate (`make check`)

`tools/check_consistency.py` asserts the facts the docs duplicate from the code,
because prose cannot be executed: every `refs/` path named in a doc exists; all
14 skills are listed here and symlinked under `.claude/skills/`; documented
deliverable names appear in the script that writes them and retired ones stay
retired; the choukai pacing table matches `ANSWER_PAUSE`/`GAP_*`; the 大問 table
matches `GENGO_QUESTION_TAXONOMY`; and for every test on disk the script
validates, 71+30 keys parse, the sheet has 101 correctly-sized radio groups, and
the in-page grader agrees with `grade_answers.py` on identical answers.

It also checks item integrity, which no other gate can see: no question offers
the same option twice; all 101 keys sit on the position `logs/test_spec.json`
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

It also checks the **reading apparatus and the passage bodies**, all measured on
`tests/imported-n2-2025-07` (the July 2025 official paper is the reference bar —
a check that paper fails is a wrong check): `（注N）` markers and definitions pair
1-to-1 **per passage** (an orphan either way is an automatic QA fail, and tests
2 and 4 shipped both directions); every `（中略）` sits inside a 問題11–13 passage
rather than floating under an instruction line, and at least one passage is cut;
every 読解 section clears its length floor — 問題10 ≥1150, 問題11 ≥2250, 問題12
≥510, 問題13 ≥900, 問題14 ≥560 JP chars of passage prose, plus ≥200 per 問題10
passage and ≥400 per 問題11 passage (official measures 1274/2503/572/1005/622,
minima 222 and 554); no 問題11 stem uses a pure-retrieval shape
(`本文で述べられて` / `として正しいもの` / `主な目的は` / `内容と合っている`, which
appear in no official 中文 stem) and every 問題11 passage asks one 考え/主張
question; each 問題14 解説 quotes the **two** flyer cells its key combines; the
four 問題9 解説 cells carry four distinct category tags including exactly one
`[内容推論]`; no keyed 読解 option is ≥50 JP chars **and** ≥1.7× the mean of its
three distractors (a key findable by length alone — the message also says
whether it is a verbatim passage lift); and no `（注N）` definition line or `例。`
script block in a **generated** test is byte-identical to another test's (an
imported paper is what others copy, not the copier, so it is exempt).

On the 聴解 side it checks that **the audio and the booklet describe the same
people and the same paper**: 問題5's 2番 must not speak the 「まず話を聞いて…」
lead-in (official speaks only the situation, and the printed-options check is
anchored on `2番。` alone so it survives the deletion — it used to split on the
defect); narration saying `〈label〉の男/女の人` must agree with the voice
`SPEAKER_MAP` casts for that label, scanning the whole block because 問題5's 2番
puts its narration on the second line; `聴解_チャプター.json`'s `script_sha` must
equal `sha1(聴解スクリプト.txt)[:12]`, so an MP3 built from a superseded script
fails instead of shipping silently (skipped for `source: external` audio, which
has no TTS timeline); and the 問題1/2/4 target items `logs/test_spec.json` drew
must actually appear in the paper.

Outside the papers it checks the **inputs that decide them**: every
`pools.json` grammar entry stays inside the level band and no grammar category
lists one point under two spellings (`〜がち`/`〜がちだ`, `〜気味`/`〜ぎみだ` —
compared after folding kanji tails to kana and dropping a trailing だ); every
`logs/ledger.json` history entry records exactly `sample_items.DRAW[cat]` items;
and no two `logs/seeds.json` seeds cite the same source URL.

Some rules cannot be decided by matching, so the gate **warns** instead of
failing. There are seven warn classes: a 解説 that quotes text found in neither
the passage nor the script; fewer than 15 in-body `（注N）` glosses (official
July 2025 = 30); a gloss whose term is a headword in
`openjlpt/vocab-n2.json` (i.e. standard N2 — this replaced a 21-word
alternation that could never cover the class and missed 鑑賞/割引/便箋/蘇る); a
`（注N）` definition assembled from the term's own kanji; a 問題7 set with no
dialogue/setting-label stems; a two-party 聴解 item whose two labels resolve to
one voice; and built HTML with no `<!-- src_sha: … -->` stamp (a *stale* stamp
fails). Warnings are part of the output you must read (§0.5): resolve each one,
or state in your final report why it is a false positive. The quote warning is
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

For a shared seed, an **unrecorded** `harvest_sha` now fails too: `None` is not
evidence of a different harvest. That hole is why tests 2 and 3 (both seed
20260804) passed this check for as long as they did — test 2 predates the stamp.
Fix it by re-harvesting and re-running `merge_seeds.py` for the affected test,
never by hand-writing a sha.

It also checks **adjunct provenance**: `logs/adjunct_staging.json` exists,
OpenJLPT slices are on disk, and any `"origin": "adjunct"` row in
`test_spec.json` carries `item`, `level: N2`, `evidence`, and stays within the
20% per-category cap.

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

---

## 6. Pass structure — orchestrate the pipeline; one test is at least SEVEN passes, not one

**Run the pipeline as an orchestrator, not as a worker.** The context that
receives the request is the orchestrator: it spawns **one subagent per pass**
from the table below and does none of the passes' content work itself — no
sampling, no authoring, no QA. Its whole job is to sequence the passes, give
each subagent a bounded prompt (which SKILL.md files to read, which files on
disk are its inputs and outputs), read each subagent's report, decide the next
pass, and assemble the final report §0.7 requires from those reports.

A "pass" is one such subagent: a fresh context that reads its inputs **from
disk** at the start (`logs/test_spec.json`, `tests/<test_id>/…`, the relevant
`SKILL.md`), does one bounded job, reports what it read, ran, and skipped, and
hands off. State flows between passes only through files on disk — never
through the orchestrator paraphrasing content into the next prompt, because a
paraphrase is exactly the "memory of what I meant" that shipped every mis-key.

The pass count is a rule, not a style preference, because both shipped failure
modes are context problems:

- **Long single-run authoring degrades toward the end.** Test 4 was written in
  one run; its defects clustered in the listening half, written last — swapped
  問題 types, an unanswerable 例, five 解説 quotes the script never says.
- **An author cannot audit its own intent.** Tests 2–4 were all "reviewed" by
  the context that wrote them, against its memory of what it meant, and passed.
  Every mis-key survived exactly that review.

| # | Pass | Scope | Subagent rule |
|---|------|-------|---------------|
| 1 | Setup | Workflow steps 1–3.5: read the skills, sample the pool, harvest seeds, merge, verify the blend report | own subagent |
| 2–5 | Authoring ×4 | One per section — 文字・語彙 (問1–6), 文法 (問7–9), 読解 (問10–14), 聴解 (booklet + script). Each re-reads `logs/test_spec.json` and the relevant SKILL.md at its start instead of trusting a long context's memory | one subagent each; only in the no-subagent fallback may sections share a context, and then the spec + skill re-read between sections is the minimum |
| 6 | Build + gate | Steps 6–9: booklet HTML, MP3, `解答.html`, `make check` (read every line incl. WARN), whole-paper topic table | may share a subagent with pass 5 |
| 7 | QA | `exam-qa-review` in full — blind-solve first, all 101 items, report with verdict **and a root-cause table (§6.5) naming the skill/gate defect behind each finding** | **own subagent — must NOT be any authoring context, and the orchestrator must not leak authoring detail into its prompt** |
| 8+ | Fix → re-review | Repair findings in the sources, regenerate, re-gate; then the changed items and their whole 問題 re-reviewed | fix may reuse an authoring subagent; the re-review must again be fresh eyes |

**Floor: 7 passes** when QA finds nothing. Every QA finding adds a fix + re-
review round (passes 8 and 9, then 10 and 11, …); the loop ends only at a
`QA: PASS` report. Partial work scales the same way: "just fix the MP3" is
still fix (one pass) + fresh-eyes re-review of the touched items (another).

`QA: PASS` closes the *paper*, not the *generator*. QA's root-cause table
(`exam-qa-review` §6.5) is a second work list, aimed at the skills and at
`tools/check_consistency.py`, and an open entry on it **blocks the next
generation run** — the review of tests 1–4 found seven defect classes present in
all four papers, which is what carrying that list forward silently produces.
Apply each entry or reject it with a reason before authoring a new test.

**Fallbacks, in order.** If the harness cannot spawn subagents, the user acts
as the orchestrator's scheduler: approximate the table with new sessions, one
pass per session, handing off through disk exactly as a subagent would. If even
that is impossible, the one non-negotiable split is **authoring vs QA — two
contexts minimum**. A single context that samples, writes, builds, and approves
its own paper is how every defective test in this repo's history shipped.
