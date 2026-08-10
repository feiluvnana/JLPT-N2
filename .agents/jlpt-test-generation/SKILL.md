---
name: jlpt-test-generation
description: End-to-end workflow for generating a complete JLPT mock exam (N1-N5, primarily N2). Use this skill whenever the user asks to create, generate, or build a JLPT test, mock exam, 模擬試験, practice test, or any subset of one (言語知識, 文字・語彙, 文法, 読解, 聴解/choukai), or asks to regenerate/fix exam deliverables. This is the entry-point skill for generation — it owns the 4-stage pass structure and the per-stage reading map, and routes to the specialized skills. Consult it FIRST before any generated exam work, even for partial requests like "make a listening section" or "create N2 grammar questions". For importing an external PDF/past paper, use external-test-import instead.
---

# JLPT Test Generation (Orchestrator)

## Import vs generate

If the user wants to **import** an existing external exam (PDF booklet, past
paper under `refs/JLPT_N2_NEW/`, script PDF, listening MP3) into project format
→ stop here and read `external-test-import/SKILL.md` instead. Those tests live
under `tests/imported-<slug>/`. This file is only for **generating** new mocks.

## Read this file to the end before your first tool call

This is the entry point for **all generated** exam work, including partial
requests. `AGENTS.md` §0 states the compliance rule and what to report at the
end. Layout, deliverable filenames, and `refs/` paths: `AGENTS.md` §2–3.

## The 4-stage pipeline

**Run it as an orchestrator, not as a worker.** The context that owns the
request spawns subagents per the table below and does none of the content work
itself — no sampling, no authoring, no QA. State flows between stages only
through files on disk (`tests/<test_id>/test_spec.json`, the Markdown sources,
this repo's skills) — never through the orchestrator paraphrasing content into
a prompt, because a paraphrase is exactly the "memory of what I meant" that
shipped every historical mis-key.

Two context-isolation rules are non-negotiable, because both shipped failure
modes are context problems: (a) **no long single-run authoring** — defects
cluster in whatever one context writes last (e.g., swapping 問題 types, an
unanswerable 例, five phantom 解説 quotes); (b) **QA is a context that authored
nothing** — an author cannot audit its own intent, and every shipped mis-key
survived exactly that self-review.

| Stage | Job | Contexts |
|-------|-----|----------|
| 1. Blueprint | Sample the pool, harvest web seeds, merge, verify the blend report | 1 subagent |
| 2. Author | 文字・語彙 (問1–6) \| 文法 (問7–9) \| 読解 (問10–14) \| 聴解 (booklet §聴解 + script) | 4 subagents, **in parallel** |
| 3. Build + gate | Booklet HTML, MP3, 解答.html, `make check`, whole-paper topic table (below) | 1 subagent |
| 4. QA | `exam-qa-review` in full — blind-solve first, all 101 items, root-cause table | 1 **fresh** subagent |

Every QA finding adds a fix + re-review round: the fix may reuse an authoring
context; the re-review of the touched items must again be fresh eyes. The loop
ends only at `QA: PASS` — and PASS closes the *paper*, not the *generator*: an
open entry in QA's root-cause table blocks the next generation run until
applied or rejected with a reason.

**Fallback with no subagents:** approximate the table with new sessions, one
stage per session, handing off through disk. The one split that survives every
fallback: **authoring and QA in different contexts.**

## Per-stage reading map

Each subagent reads exactly these files at the START of its stage (from disk,
never from the orchestrator's summary), and nothing else:

| Stage | Reads | Writes |
|-------|-------|--------|
| 1 Blueprint | `exam-blueprint/SKILL.md` | `tests/<id>/test_spec.json`, `logs/ledger.json`, `logs/seeds.json` |
| 2 文字・語彙 | `test_spec.json` + `question-authoring/SKILL.md` + its `references/moji-goi.md` + `jlpt-exam-structure/SKILL.md` | 問1–6 fragment of `言語知識・読解.md` |
| 2 文法 | same, with `references/bunpou.md` | 問7–9 fragment |
| 2 読解 | same, with `references/dokkai.md` | 問10–14 fragment |
| 2 聴解 | `test_spec.json` + `question-authoring/SKILL.md` + `references/choukai-items.md` + `choukai-audio/SKILL.md` + `jlpt-exam-structure/SKILL.md` | `聴解.md`, `聴解スクリプト.txt` |
| 3 Build+gate | `exam-app/SKILL.md`, `choukai-audio/SKILL.md` (synthesis §), this file's topic-table § | `言語知識・読解.md` (merged), the HTML/MP3 artifacts, `logs/topics.json` row, gate report |
| 4 QA | `exam-qa-review/SKILL.md` (which routes to what it needs) | `qa/qa-report-<id>.md` |

Stage-2 authors write **section fragments** to separate files
(`tests/<id>/_sections/<問題range>.md`). Each fragment is two parts: the
booklet body for its 問題 range, then its answer-key/解説 table rows under a
literal marker line `<!-- KEY -->`. Stage 3 merges mechanically, no judgment:
all bodies in booklet order (問1→問14), then ONE key heading
(`jlpt-exam-structure` owns its format) at the END of `言語知識・読解.md`,
followed by the key tables in the same order — the sheet builder's
`strip_key()` truncates at that single heading, so a fragment must never carry
its own key heading. Parallel authors never write to the same file. The 聴解
author owns both `聴解.md` and `聴解スクリプト.txt` complete (body + keys at
end; they must stay synchronized — `choukai-audio`).

### Subagent prompt template (all stages)

> Read, in full, from disk: [stage's reading-map row]. Your inputs are
> [files]; your only outputs are [files]. Author ONLY what
> `tests/<id>/test_spec.json` prescribes — items, topics, and
> `answer_positions` are the contract; do not substitute, and treat every
> `origin` field as binding. Report at the end: what you read, what you ran,
> what you wrote, and anything you skipped and why.

## Stage 1 — blueprint rules

Commands (details in `exam-blueprint/SKILL.md`):

```bash
make sample <id> SEED=<n>          # -> tests/<id>/test_spec.json + ledger
# re-harvest logs/seeds.json (web research), then:
make merge-seeds <id>              # blend web seeds into every spec surface
```

- **The seed is an RNG output, never a number you write down** — run
  `python3 -c "import secrets; print(secrets.randbelow(10**8))"` (or any
  equivalent) and use the printed value verbatim. Agent-"picked" seeds are
  date-shaped and collide across sessions if agents choose the same date
  independently. It must also be a seed no previous test used
  (`logs/ledger.json` records them) — the blend is a pure function of
  `(seed, logs/seeds.json)`, and the gate only fails a reused seed against
  the SAME harvest, so a fresh seed is on you.
- **Re-harvest `logs/seeds.json` for every test** — it is a per-test input, not
  a repo fixture. Inheriting a previous test's harvest causes the paper to
  ship as a re-skin of past tests.
- Read the printed **blend report** before authoring: 30–60% web per surface,
  pool side ≥40%, ≤2 seeds per domain. Re-harvest and re-run if it warns.
- Offline: skip harvest/merge; the pure-pool spec is valid. Say so in the
  final report.

## Stage 2 — authoring rules

The construction rules live in `question-authoring` (core + the per-section
reference file from the reading map). Binding here:

- Author ONLY items in `test_spec.json`; keys go where `answer_positions` says.
- Tested items (grammar/vocab/kanji) are ALWAYS the pool-sampled ones; web
  seeds supply only topics, settings, and facts (`exam-blueprint`).
- Answer keys go at the END of each Markdown source, never inline
  (`jlpt-exam-structure` owns the key-table format).

## Stage 3 — build + gate

```bash
make booklet <id> && make mp3 <id> && make sheet <id> && make check
```

- `make check` validates every test on disk; **read every line, including
  WARN** — resolve each warning or justify it in the report. Fix failures
  before stage 4: a mis-keyed item is invisible once the MP3 is built.
- Then do the **whole-paper topic pass** (next section) — no script sees it —
  and **append this test's row to `logs/topics.json`** from the finished
  sources: `surfaces` (each 読解 passage, 問題9, 問題14, every 聴解 item incl.
  例, as one noun phrase each) and `shapes` (each 聴解 item's errand shape).
  Row format and why the file exists: `exam-blueprint` §"logs/topics.json" —
  the next test's `merge_seeds.py` reads it to refuse repeated subjects.

## One topic, one surface (whole-paper pass, stage 3)

The failure mode that survives every automated gate: the same content on two
surfaces of one paper, or recycled from recent papers. List every surface's
topic in ONE table — 問題9 cloze, each 問題10–13 passage, the 問題14 flyer,
each 聴解 item — with one column per test (this one and the two before it),
and check:

- **No topic appears twice in this paper**, even in a different register (an
  essay and a monologue on one subject are still a repeat). For example, avoid
  having the 問題14 flyer spell out a 聴解 item's keyed answer in its fine
  print, or having one デジタルデトックス essay serve both 問題9 and 問題10(1).
- **No topic repeats the previous test.** Avoid duplicating web topics from the
  previous paper, especially in the same 聴解 slots.
- **No condition, number, or rule shared** between the 問題14 flyer and any
  聴解 item. Shared setting is tolerable; shared decisive detail is not.
- **Two 聴解 items may not run the same errand**, and errand **archetypes**
  (reschedule call, model choice at a store, campaign flyer…) must not repeat
  within the last two tests — add a shape column, not just a subject column
  (e.g., avoiding having a reschedule-an-appointment call run across
  consecutive tests).
- **問題12 (A/B) gets its own cross-test column** — it is one topic per paper
  and repeated three papers running (働き方) once already.
- **A duplicated seed in the spec is a defect**: it means `merge_seeds.py` ran
  over its own output. Re-run it; never invent a topic for a starved surface.
  Each spec seed feeds exactly one surface, and `origin` is binding (a
  `"pool"` cloze must not borrow a web reading seed).

## Stage 4 — QA

Read `exam-qa-review/SKILL.md` in full and run it with fresh eyes. NOT
optional: generated papers can ship content defects through a green gate if QA is skipped.
A test that has not survived this pass is not done, whatever the gate says.

## Taking the exam (after QA)

`make serve` (no test id — one server lists every test), answer, press
「採点する」: the page saves `採点結果.json` + `ユーザー解答.json` into
`tests/<id>/`. CLI: `make grade <id>`. See `exam-app`.

## Invariants (every run)

- Japanese file names for all deliverables in `tests/<test_id>/`
  (table: `AGENTS.md` §2).
- Markdown is the single editable source. **Every source edit carries its
  rebuild in the same change**: `聴解スクリプト.txt` → `make mp3 <id>`; either
  `.md` → `make booklet <id> && make sheet <id>`. The artifacts carry the sha
  of the bytes they were built from (`script_sha`, `<!-- src_sha -->`) and the
  gate compares them — but the gate is the backstop, not the workflow. Never
  hand-edit a sha. (A single script rewrite across several papers once
  rebuilt only one MP3; the rest shipped speaking superseded instructions.)
- `聴解.md` and `聴解スクリプト.txt` stay synchronized: printed 例 options ↔
  spoken 例; any script item change requires a key check.
- After script/audio edits, re-run the dry-run validators in `choukai-audio`
  (block count, speaker-map coverage, pause distribution).
- Never copy questions from the copyrighted textbooks in `refs/` — calibration
  only; all items original. Web sources give WHAT to write about, never the
  words.
- Commit `tests/<test_id>/` and the updated `logs/` together with the pipeline
  changes that produced them.
