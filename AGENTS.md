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
shipped a re-skin of an earlier paper with every automated gate green; a QA
fix hand-substituted an undrawable 問題1 target instead of running
`--reroll <category>` as `question-authoring`/`exam-blueprint` already said
to, shipping a pool-item repeat — `make check`'s own rotation gate would not
have caught it anyway, since it checked every category against one spec-wide
weakest-cooldown number instead of each category's own window; see
`exam-blueprint/SKILL.md` "Rotation model", 2026-08-17.)

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
- **Claude Code**: the same 9 skills are exposed natively via symlinks in `.claude/skills/<skill_name>` → `.agents/<skill_name>`, so they are auto-discovered and invocable as `/<skill-name>`. `.agents/` remains the single copy — edit files there.
- **`jlpt-test-generation` is the entry point for generating mocks.** For importing an outside PDF/past paper, read `external-test-import` instead. For any other exam work, read `jlpt-test-generation` first — it routes to the other skills in order.
- Available Skills:
  1. `jlpt-test-generation`: End-to-end mock exam generation orchestrator — **read this one first** for generated exams. Owns the 4-stage pass structure and the per-stage reading map.
  2. `jlpt-exam-structure`: Official JLPT exam format facts — section layouts, question counts, timing, booklet printing conventions, answer-key table format.
  3. `exam-blueprint`: WHAT each exam tests — random non-repeating pool sampling (`sample_items.py`), answer-position balance. Runs before any authoring.
  4. `question-authoring`: HOW to write N2-calibrated items — distractors, item integrity, per-section construction rules (`references/moji-goi.md`, `bunpou.md`, `dokkai.md`, `choukai-items.md`), and calibration against `refs/` (`references/official_calibration.md`).
  5. `choukai-audio`: The listening audio end to end — **composed from real recordings** since 2026-09-08 (`tools/build_choukai_bank.py` builds the clip bank from the ten imported sittings plus `tools/build_textbook_bank.py`'s hand-declared textbook and mock-exam items (Shin Kanzen / Soumatome / 問題例集 / 完全模試), `tools/compose_choukai.py` draws and assembles a paper's whole 聴解 half), plus the pacing table those pauses come from and the method for measuring official audio. Exactly one paper is official-only; every other paper draws from the MIXED pool. Edge-TTS is retired.
  6. `exam-app`: Rendering and running the exam — booklet HTML (`build_booklet.py`, no PDF), the merged answer sheet `解答.html` with in-page grading (`build_interactive.py`), the one server (`serve_sheet.py`), the static GitHub Pages build (`build_pages.py`), and CLI grading (`grade_answers.py`).
  7. `exam-qa-review`: The adversarial content QA pass every generated test must survive AFTER `make check` is green and BEFORE it is served or committed — run it with fresh eyes (a context that did not author the test). It also root-causes every finding back to the skill, script, or gate check that let it through, so the next test does not reproduce it.
  8. `external-test-import`: Import an external exam (PDF booklet ± script PDF ± MP3) into `tests/imported-<slug>/` project format — **use instead of generation** when the source already exists outside the pool pipeline.
  9. `exam-model-answer`: Model answer & explanation generator — builds `模範解答.html` explaining every item (why the correct option is chosen and why each distractor is wrong) across Language Knowledge, Reading, and Listening. Two languages behind one segmented control (Japanese + Vietnamese), each **written**, not translated from the other, and each field inside the skill's terseness bands.

---

## 2. Directory Layout & Japanese File Naming Standards

### Root Directories

- `refs/`: Reference input files (scanned PDFs and audio recordings). See §3.
- `tests/<test_id>/`: Output folder for each exam. **Origin is encoded in the folder name:** ids starting with `imported-` are external imports (e.g. `tests/imported-n2-2025-12/`); any other id is **generated** (e.g. `tests/1/`). See `external-test-import`.
- `logs/`: Item coverage ledger (`logs/ledger.json`), topic history
  (`logs/topics.json`), adjunct staging, and any **remediation state file**
  (`logs/choukai_remediation_state.json`) — a long repair plan's resumable
  step list, tracked for the same reason the ledger is: the next run depends
  on it. A fresh context starts there, then re-derives what it claims by
  measuring the artifact, never by trusting the flag. `logs/choukai_bank.json`
  (the clip pool), `logs/choukai_draws.json` (which clips each paper spent, and
  its per-source mix) and `logs/choukai_number_calls.json` (the 11 harvested
  「N番。」 spans) are tracked for the same reason — the next draw depends on
  them. `logs/upload_manifest.json`
  is tracked for the same reason: it is what stops `make upload-files` from
  pushing 2.5 GB of unchanged binaries a second time, and a fresh clone that
  loses it re-uploads the archive. `logs/findings.json` is
  the gate's `--json` output and is gitignored — it is recomputed in seconds.
  Each generated test's blueprint lives at `tests/<test_id>/test_spec.json`.
- `.agents/`: The 9 skills — docs, scripts, and reference data.
- `tools/`: Repo-level tooling that is not a skill (`check_consistency.py`, the `refs/` archive extractors).
- `_site/`: **Build output only, gitignored.** The static GitHub Pages copy of the exam app, rebuilt from `tests/` by `make pages` and by CI on push. Never edit or commit it. See `exam-app`.

**`tests/` and `logs/` are tracked, on purpose** — they are the working folders
where exams get built and taken, and the ledger must persist because item
rotation depends on the history of past draws. Commit new tests and the updated
ledger together with the pipeline changes that produced them. Gitignored
build/cache paths: `tests/*/segments/`, `tests/*/_extract/`,
`tests/*/_sections/`, `qa/*/` (keyless renders —
`qa/qa-report-*.md` stays tracked), `_site/`. **`tests/*/聴解.mp3` is
gitignored too** — the audio is a release asset, not a committed deliverable
(§3). Ignoring a path does not untrack one already in the index, which is how
16 of them stayed tracked for ten days after LFS was dropped; `make check` now
fails on any that are, and the repair is
`git rm --cached -- 'tests/*/聴解.mp3'` (the files stay on disk).

### Deliverables Naming Convention (Japanese File Names Mandatory)

Inside `tests/<test_id>/` — this table is the single copy; skills point here:

| Deliverable                          | File Name                              | Description / Source                                                                   |
| ------------------------------------ | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Language Knowledge & Reading Booklet | `言語知識・読解.html`                  | Rendered from Markdown source `tests/<test_id>/言語知識・読解.md`                      |
| Listening Booklet                    | `聴解.html`                            | Rendered from Markdown source `tests/<test_id>/聴解.md`                                |
| Listening TTS Script                 | `聴解スクリプト.txt`                   | Pure official-style narration text                                                     |
| Listening Audio MP3                  | `聴解.mp3`                             | Synthesized audio generated from the TTS script                                        |
| Interactive Answer Sheet             | `解答.html`                            | Combined booklet (71 Gengo/Dokkai + 30 Choukai + Audio player); in-page 180pt grading |
| Listening Chapter Marks              | `聴解_チャプター.json`                 | Per-問題/per-item offsets in `聴解.mp3`, written by `tools/compose_choukai.py`         |
| User Answers Record                  | `ユーザー解答.json`                    | Written by `解答.html` on every click; also carries the sitting's `受験状態` (phase + the two clocks) — `exam-app` |
| Combined Grading Result              | `採点結果.json`                        | Generated on submit from `解答.html` or written by `grade_answers.py`. There is no Markdown report — the result is data, read back by the result screen and by the test list |
| Model Answer & Detailed Explanation  | `模範解答.html`                        | Comprehensive model answer and explanation document for all 101 items, rendered by `build_model_answer.py` |
| Model Answer Explanations (JA)        | `詳細解説.json`                        | Hand-authored per-item explanations — the source `模範解答.html` renders (`exam-model-answer`). Also the ONE copy of the exam wording (`stem`/`options`/`passage`/`script`) both language panes print |
| Model Answer Explanations (VI)        | `詳細解説.vi.json`                     | The Vietnamese pane. Explanations are **written from the items, never translated** from `詳細解説.json` (`exam-model-answer`). It carries no exam wording, with ONE deliberate exception: `passage_translation`, the Vietnamese rendering of a 読解 passage, on the FIRST item of each passage group |
| Import provenance (imported only)    | `import_meta.json`                     | Written by `external-test-import` for `tests/imported-<slug>/` only — generated tests must not have this file |

---

## 3. Reference Files (`refs/`)

**The source archive is NOT in git, on purpose.** `refs/` is 2.6 GB of scanned
PDFs and MP3s; tracking it through Git LFS exhausted the account's LFS budget,
and an exhausted budget makes the LFS API refuse *every* object — so
`actions/checkout` itself failed and CI could deploy nothing (2026-08-24;
`.gitignore` and `.gitattributes` carry the rule, `exam-app/SKILL.md` the CI
half). What a clone DOES get in git is the part these rules are measured
against: every `*.md` extract (`booklet.md`, `script.md`, `key.md`,
`audio_inspection.md`, the Shinkanzen/Soumatome reference extracts) plus
`answer_keys.json` — 3.7 MB, all tracked. Only re-extracting, opening a PDF
page, or listening to audio needs the binaries.

**Where the binaries live: GitHub Releases, via `make upload-files`.** Two
tags, both **fixed addresses, reused forever**: `audio` holds one
`<test_id>.mp3` per test, and
`refs` holds one zip per top-level `refs/` folder — `JLPT_N2_NEW.zip` (1.2 GB),
`Shinkanzen.zip` (1.0 GB), `Soumatome.zip` (0.3 GB), stored uncompressed since
PDFs and MP3s already are. Unzip one into `refs/` and that source's tree is
back. Never rename a tag: `build_interactive.py` and `build_model_answer.py`
hard-code `…/releases/download/audio/<test_id>.mp3` as the player's fallback,
so a new tag 404s every deployed sheet. **Uploads are incremental and that is
not optional** — `logs/upload_manifest.json` records each asset's fingerprint,
so a file goes over the wire once and a zip is rebuilt only when one of its
members changes. Add a binary, run `make upload-files`, commit the manifest with
it; never re-push the archive to "make sure" (`--dry-run` tells you what would
move, `--force` is for when you know the remote is wrong). Since git carries no
exam MP3, an un-uploaded one exists on exactly one disk and 404s for every other
reader — `make check` fails on any `聴解.mp3` whose bytes are not the ones the
manifest says went up. Uploading needs a `gh` account with push access to the
repo; the uploader now says so up front, because GitHub answers an unauthorized
asset overwrite with a 404 that reads like a corrupt release.

**If a binary you need is not on the machine, STOP and ask the user.** Name the
exact path (e.g. `refs/JLPT_N2_NEW/16. N2 7-2025/Nghe N2 T7-2025.mp3`), say what
you were going to measure, and offer the one-command restore — the archive is on
the `refs` release, so nothing has to be re-sourced:

```bash
gh release download refs --pattern 'JLPT_N2_NEW.zip' --dir /tmp   # or Shinkanzen / Soumatome
unzip -n /tmp/JLPT_N2_NEW.zip -d refs/                            # -n: never overwrite
```

It is a 1 GB download, so **ask before running it** — and then wait. The three
things you must NEVER do instead:

1. **Do not commit the archive back into git** (`git add -f refs/…`, a new
   `*.pdf`/`*.mp3` LFS rule) — that re-breaks CI for everyone.
2. **Do not substitute a number from memory, from another sitting, or from a
   textbook** for one the archive owns. Every band in these skills is a
   *measurement*; §4's "a measured number has one owner, and it is a script"
   applies here — an invented count is the defect class REPORT-GOI.md §F10
   records. `make check` `skip`s the archive checks on such a machine, and a
   skip is not a pass.
3. **Do not quietly drop the step.** Say in your final report that it was
   blocked on a missing source (§0.7).

`make check` distinguishes the two classes: a missing `*.md` extract FAILs (git
tracks it, so it is a real defect), a wholly absent archive `skip`s, and a
partly-present one WARNs — a source the docs cite under an old name is a doc
defect worth fixing.

All calibration inputs must be looked up in `refs/`:

- **Textbooks (`refs/Shinkanzen/`)**:
  - Grammar: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Bunpou.pdf`
  - Reading: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Dokkai.pdf` → extract
    `refs/Shinkanzen/dokkai_reference.md` (`make extract-shinkanzen-dokkai`)
  - Listening: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai.pdf` → extract
    `refs/Shinkanzen/choukai_script.md` (`make extract-shinkanzen`)
  - Vocabulary: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Goi.pdf` → extract
    `refs/Shinkanzen/goi_reference.md` (`make extract-shinkanzen-goi`)
  - Kanji: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Kanji.pdf` → extract
    `refs/Shinkanzen/kanji_tables.md` (`make extract-kanji-tables`)
  - Textbook CDs: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai-CD/`
- **Textbooks (`refs/Soumatome/`) — 日本語総まとめ N2**:
  - Vocabulary: `refs/Soumatome/nihongo-soumatome-n2-goi.pdf` → extract
    `refs/Soumatome/goi_reference.md` (`make extract-shinkanzen-goi`)
  - Kanji: `refs/Soumatome/nihongo-soumatome-n2-kanji.pdf` (no extract yet)
  - Together with Shinkanzen's Goi/Kanji volumes **and `refs/Hajimete/` below**,
    these are exam-blueprint's ONLY vocabulary/kanji pool authority (`pools.json`'s `kanji_reading`,
    `context_words`, `paraphrase`, `usage`) — the vendored OpenJLPT JSON corpus
    was removed 2026-08-11 (exam-blueprint/SKILL.md). All four PDFs are scanned
    images with no text layer (`pdffonts` prints an empty table), so
    `pdftotext` returns nothing.
  - **Read the three `*_reference.md` / `*_tables.md` extracts above first**;
    open a PDF only to verify a line one of them got wrong. Those files are
    **OCR, not exact**, and they are **secondary evidence**: a textbook
    corroborates band, family and reading, and never sets a count or a length —
    the 31-sitting archive below is the measuring stick for every number. Each
    extract's own header carries the full trust rules and the sections it
    covers. Three of the four books are over the **100 MB per-file PDF read
    cap** (漢字 264 MB, Soumatome 漢字 173 MB, Soumatome 語彙 103 MB; Shin
    Kanzen 語彙 at 40 MB is the only direct read) — slice one with
    `--split-pdf DIR` rather than trying to open it whole.
- **Vocabulary list (`refs/Hajimete/`) — はじめての日本語能力試験 N2単語 2500**:
  - `refs/Hajimete/はじめての日本語能力試験 N2単語 2500.pdf` (45 MB, 314 pp.) →
    extract `refs/Hajimete/vocab_reference.md` (`make extract-hajimete`).
  - Added 2026-09-07. A flat, numbered **2500-word N2 list** — headword, reading,
    part of speech, one example sentence, EN/ZH/VI glosses — where Shin Kanzen and
    Soumatome are graded exercise volumes whose headwords sit around the drills.
    It is the third vocabulary authority for `pools.json` and for
    `question-authoring`'s per-key verification, and it is a reference corpus for
    `tools/lexical_profile.py`'s 読解 lexical-load gate.
  - Scanned images, no text layer (`pdffonts` prints an empty table), like the
    other four books; 45 MB is under the 100 MB read cap, so a page can be opened
    directly to check a reading the OCR got wrong. **Same trust rules as every
    textbook extract: secondary evidence, never a count or a length.**

- **Mock-exam book (`refs/KanzenMoshi/`) — 『ゼッタイ合格！日本語能力試験 完全模試 N2』**:
  - Jリサーチ出版 2013, ISBN 978-4-86392-129-0. Three mock papers: 3 audio CDs
    (43 tracks each, one per paper), `JLPT_N2_Kanzen_Moshi-Mock Tests.pdf`
    (128 pp, 問題冊子) and `JLPT_N2_Kanzen_Moshi-Taisaku.pdf` (114 pp, 解答・解説
    with the full listening script, keys and CD track badges).
  - Added 2026-09-10 as the fourth 聴解 clip source. It is the first source that
    clears all five acceptance checks unaided — its recordings are pressed to
    **exam timing** (19.3–20.1 s 問題2 option-reading pause, spoken 「N番。」), so
    `build_textbook_bank.rate_band_for()` judges it against `CHAR_RATE_OFFICIAL`.
    Track map, measurements and what is still untranscribed:
    `choukai-audio/references/textbook_bank_plan.md` §8.
  - Both PDFs are scans with no text layer, like every other book here, and both
    are over the **100 MB read cap** — slice with pypdf before reading.

- **Free official web material (`refs/External/`)** — fetched from jlpt.jp
  2026-09-09, no account and no purchase. Three folders: the 公式問題集 第一集
  (2012) and 第二集 (2018), which are **re-releases of sittings the archive
  already holds** (7-2011 and 12-2016 — measured, `refs/External/README.md` §1)
  and therefore add no listening clip, only an EXACT born-digital text layer for
  two sittings the archive has as stencil scans; and the 問題例集 (2009), whose
  five-item sample MP3 IS new material and contributes four banked clips
  (`choukai-audio` / `textbook_bank_plan.md` §7). Zips to `External.zip` on the
  `refs` release like every other top-level folder. Its README also records what
  was searched and rejected, so the next agent does not re-run the search.
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
| `make goi-profile [BASELINE=1]` | `tools/goi_profile.py` — 文字・語彙 measurement (archive vs tests); `BASELINE=1` prints the doc tables | `question-authoring` |
| `make dokkai-profile [BASELINE=1]` | `tools/dokkai_profile.py` — 読解 measurement (archive vs tests); `BASELINE=1` prints the doc tables | `question-authoring` |
| `make choukai-profile [BASELINE=1]` | `tools/choukai_profile.py` — 聴解 measurement (archive vs tests); `BASELINE=1` prints the doc tables | `choukai-audio` |
| `make findings`           | the gate in `--json` mode → `logs/findings.json` (one record per slugged finding: slug, test id, artifact, tier) | (below) |
| `make repair-plan [<id>] [TIER=B]` | `tools/choukai_repair_plan.py` → `qa/[<id>/]repair-plan.{json,md}` — the 聴解 **and** 読解 work order, grouped by the ARTIFACT each finding declares (the tier follows from it), so a 読解 prose repair is never printed under a `make mp3` rebuild | `exam-qa-review` |
| `make sample <id> SEED=n` | `sample_items.py` → `test_spec.json` + ledger | `exam-blueprint` |
| `make scaffold-sections <id>` | `scaffold_sections.py` → scaffolds `_sections/` authoring templates | `question-authoring` |
| `make matrix`             | `matrix_helper.py` — **validate only**; both generators are hard-disabled (they had no 音訓 table and emitted kana-skeleton-violating grids — qa-report-20260819_1 F4) | `question-authoring` |
| `make booklet <id>`       | `build_booklet.py` on both Markdown sources | `exam-app` |
| `make mp3 <id> SEED=n`    | `tools/compose_choukai.py` — composes the whole 聴解 half from banked clips (script, booklet, MP3, chapters, both 詳細解説 panes). Edge-TTS is retired | `choukai-audio` |
| `make choukai-bank [CHECK=1]` | `tools/build_choukai_bank.py` → `logs/choukai_bank.json`; BOTH halves of the mixed pool — the ten imported sittings plus the textbook items | `choukai-audio` |
| `make textbook-bank`      | `tools/build_textbook_bank.py` — report-only: what the Shin Kanzen / Soumatome half measures, and which declared items the duration/rate guards refuse | `choukai-audio` |
| `make choukai-wear`       | `tools/choukai_wear.py` — how many papers spend each clip, measured and projected per 大問 and per source; the measurement `compose_choukai.TEXTBOOK_SLOTS` is set from, and it exits non-zero above the wear ceiling | `choukai-audio` |
| `make number-calls [CHECK=1]` | `tools/harvest_number_calls.py` → `logs/choukai_number_calls.json` — the 11 official 「N番。」 spans a textbook clip is given | `choukai-audio` |
| `make sheet <id>`         | `build_interactive.py` → `解答.html` | `exam-app` |
| `make model-answer <id>`  | `build_model_answer.py` → `模範解答.html` | `exam-model-answer` |
| `make scaffold-explanations <id> [LANG=vi]` | `scaffold_explanations.py` → scaffolds `詳細解説.json` (or an empty `詳細解説.<lang>.json`) | `exam-model-answer` |
| `make lint-draft <id>`    | `lint_draft.py` — fast deterministic pre-lint before QA | `exam-qa-review` |
| `make autofix <id>`       | `lint_draft.py --fix` — auto-fixes contractions and stem layout | `exam-qa-review` |
| `make verify-scramble <id>` | `verify_scramble.py` — topological & permutation validator for 問題8 | `question-authoring` |
| `make irt <id>`           | `irt_scorer.py` — 2PL Item Response Theory scaled score simulation | `exam-app` |
| `make qa-eval <id>`       | `qa_eval.py` — structured blind-solve evaluator & QA report generator | `exam-qa-review` |
| `make keyless <id>`       | the QA blind-solve render → `qa/<id>/keyless.md` | `exam-app` |
| `make serve`              | `serve_sheet.py` — ONE server for every test (no id) | `exam-app` |
| `make grade <id>`         | `grade_answers.py --test-dir tests/<id>` | `exam-app` |
| `make pages [<id>]`       | `build_pages.py` — static GitHub Pages site → `_site/` | `exam-app` |
| `make preview-pages`      | serves `_site/` locally | `exam-app` |
| `make init-import SLUG=…` | `init_imported_test.py` — scaffold `tests/imported-<slug>/` | `external-test-import` |
| `make extract-pdf PDF=… OUT=…` | `extract_pdf_text.py` | `external-test-import` |
| `make extract-archive`    | `extract_jlpt_n2_new.py --all` — past-paper archive → Markdown | §3 above |
| `make extract-keys`       | `extract_jlpt_n2_key.py` — key PDF → `key.md` + JSON | §3 above |
| `make extract-shinkanzen-dokkai` | `tools/extract_shinkanzen_dokkai.py` — Shin Kanzen Dokkai → Markdown | §3 above |
| `make extract-shinkanzen` | `tools/extract_shinkanzen_choukai.py` — Shin Kanzen Choukai → Markdown | §3 above |
| `make extract-hajimete`   | `tools/extract_hajimete.py` — はじめての N2単語 2500 → Markdown | §3 above |
| `make upload-files [TARGET=tests\|refs\|all [TEST=…]]` | `tools/upload_files.py` — push exam audio (release `audio`) and the `refs/` archive as one zip per folder (release `refs`); uploads each asset **once** and again only when it changes | §3 above |

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
- **A measured number has one owner, and it is a script.** `make goi-profile`
  measures 文字・語彙 on both corpora (archive + `tests/`) and
  `check_consistency.py` imports the same module, so a threshold here and a band
  in `moji-goi.md`/`official_calibration.md` cannot drift apart. Three numbers
  the 文字・語彙 rules were built on turned out to be unreproducible when someone
  finally re-measured them (REPORT-GOI.md §F10) — refresh a doc table from
  `--baseline` output, never by retyping.
- Green is the floor, never the verdict on a paper — `exam-qa-review` is.
  Several binding authoring rules are read by QA only, not by the gate
  (`question-authoring` §"Answer keys — format pointers and the required
  artifacts" lists which of its required key-table artifacts the
  gate actually reads); do not skip one because `make check` is green.

---

## 5. Pass structure — orchestrate, don't work

The generation pipeline runs as **4 stages + final model-answer step** — blueprint → 3 parallel
authoring sections → build+gate → fresh-eyes QA → model-answer generation (`make model-answer <id>`),
each a subagent with a bounded reading list, handing off through files on disk only.
**聴解 is no longer one of the authoring sections**: since 2026-09-08 the whole
listening half is composed from real recordings at build time by
`make mp3 <id> SEED=<rng>` (`choukai-audio` Part 0) — the ten imported official
sittings plus Shin Kanzen and Soumatome items, with exactly one paper kept
official-only — so there is nothing to author and no 聴解 subagent.
`jlpt-test-generation` owns the stage table, the reading map, the prompt
template, and the fix→re-review loop; read it before any generation work.

**Model answer generation (`make model-answer <id>`) MUST always be the final step**
(for both generated exams and imported exams) — run only after QA/fidelity verification
has passed and all questions, options, and keys are locked. The page carries TWO
explanation sets behind an in-page segmented control — `詳細解説.json` (Japanese)
and `詳細解説.vi.json` (Vietnamese) — **authored in separate contexts, one per
language, and written from the items rather than translated from each other**
(`exam-model-answer`). Both panes print the exam's own wording, stored once,
above the explanation. Every field is capped by that skill's terseness bands and
the gate enforces them.

The two context-isolation rules that are never optional, in any harness or
fallback: **no long single-run authoring** (defects cluster in whatever one
context writes last), and **QA in a context that authored nothing** (an author
cannot audit its own intent — every shipped mis-key survived its author's own
review). With no subagents available, approximate the stages with separate
sessions; the minimum split that survives every fallback is authoring vs QA,
two contexts.
