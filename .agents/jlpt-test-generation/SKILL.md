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
| 1. Blueprint | Sample the pool (topics/scenarios are authored directly from the draw — no web harvest) | 1 subagent |
| 2. Author | 文字・語彙 (問1–6) \| 文法 (問7–9) \| 読解 (問10–14) \| 聴解 (booklet §聴解 + script) | 4 subagents, **in parallel** |
| 3. Build + gate | Booklet HTML, MP3, 解答.html, `make check`, whole-paper topic table (below) | 1 subagent |
| 4. QA | `exam-qa-review` in full — blind-solve first, all 101 items, root-cause table | 1 **fresh** subagent |
| 5. Model Answer (Final) | `make model-answer <id>` → `模範解答.html` — **MUST always be the final step** after QA PASS | 1 subagent |

Every QA finding adds a fix + re-review round: the fix may reuse an authoring
context; the re-review of the touched items must again be fresh eyes.
**Exception: if a QA round returns FAIL with 3 or fewer findings total, the
orchestrator may apply the fixes directly without spawning a fresh re-review
round** — same rigor as the round-3 fallback below (root-cause each finding,
verify `make check`, sanity-read the diff), and state in the final report that
the low-count exception applied and how each finding was resolved. The loop
ends at `QA: PASS`, **capped at 3 fresh-eyes QA rounds total.** Once QA is PASS,
proceed to Stage 5 to build `模範解答.html`. If round 3 still
returns FAIL, the orchestrator applies that round's findings directly (same
rigor as any other fix — root-cause each one, verify `make check`, sanity-read
the diff) but does **not** spawn a 4th fresh-eyes QA pass; ship the paper and
say so explicitly in the final report — which findings were fixed without an
independent re-verification, and why (the cap, not a skipped step). PASS closes
the *paper*, not the *generator*: an open entry in QA's root-cause table blocks
the next generation run until applied or rejected with a reason, regardless of
which round found it.

**Fallback with no subagents:** approximate the table with new sessions, one
stage per session, handing off through disk. The one split that survives every
fallback: **authoring and QA in different contexts.**

## Per-stage reading map

Each subagent reads exactly these files at the START of its stage (from disk,
never from the orchestrator's summary), and nothing else:

| Stage | Reads | Writes |
|-------|-------|--------|
| 1 Blueprint | `exam-blueprint/SKILL.md` | `tests/<id>/test_spec.json`, `logs/ledger.json` |
| 2 文字・語彙 | `test_spec.json` + `question-authoring/SKILL.md` + its `references/moji-goi.md` + `jlpt-exam-structure/SKILL.md` | 問1–6 fragment of `言語知識・読解.md` |
| 2 文法 | same, with `references/bunpou.md` | 問7–9 fragment |
| 2 読解 | same, with `references/dokkai.md` | 問10–14 fragment |
| 2 聴解 | `test_spec.json` + `question-authoring/SKILL.md` + `references/choukai-items.md` + `choukai-audio/SKILL.md` + `jlpt-exam-structure/SKILL.md` | `聴解.md` (incl. the セクション構成表), `聴解スクリプト.txt` |
| 3 Build+gate | `exam-app/SKILL.md`, `choukai-audio/SKILL.md` (synthesis §), this file's topic-table § | `言語知識・読解.md` (merged), the HTML/MP3 artifacts, `logs/topics.json` row, gate report |
| 4 QA | `exam-qa-review/SKILL.md` (which routes to what it needs) | `qa/qa-report-<id>.md` |
| 5 Model Answer | `exam-model-answer/SKILL.md` | `tests/<id>/模範解答.html` |

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
end; they must stay synchronized — `choukai-audio`), and finishes each section by
writing its **セクション構成表** after the key heading and checking its columns
against the per-section quotas — the artifact and the quotas are defined in
`question-authoring/references/choukai-items.md`, and QA reads the table first.
Write it while the section is fresh: it is the only view in which a repeated key
or a one-shape section is visible, and both have shipped past every other check.

### Subagent prompt template (all stages)

> Read, in full, from disk: [stage's reading-map row]. Your inputs are
> [files]; your only outputs are [files]. Author ONLY what
> `tests/<id>/test_spec.json` prescribes — items, topics, and
> `answer_positions` are the contract; do not substitute, and treat every
> `origin` field as binding. Report at the end: what you read, what you ran,
> what you wrote, and anything you skipped and why.
>
> (読解 subagent only) Your assigned closing-move shape for each surface in
> your range is: [surface → shape, from the orchestrator's pre-spawn
> distribution above]. Write to that shape; note in your report if a draft
> genuinely cannot fit its assignment and why.

## Stage 1 — blueprint rules

Command (details in `exam-blueprint/SKILL.md`):

```bash
make sample <id> SEED=<n>          # -> tests/<id>/test_spec.json + ledger
```

- **The seed is an RNG output, never a number you write down** — run
  `python3 -c "import secrets; print(secrets.randbelow(10**8))"` (or any
  equivalent) and use the printed value verbatim. Agent-"picked" seeds are
  date-shaped and collide across sessions if agents choose the same date
  independently. It must also be a seed no previous test used
  (`logs/ledger.json` records them).
- There is no harvest/merge step. `test_spec.json`'s `reading_topics` and
  `listening_scenarios` are what every 読解/聴解 surface is authored from —
  see `exam-blueprint` Part II for how to write from them at N2 level.

## Stage 2 — authoring rules

The construction rules live in `question-authoring` (core + the per-section
reference file from the reading map). Binding here:

- Author ONLY items in `test_spec.json`; keys go where `answer_positions` says.
- Tested items (grammar/vocab/kanji) are ALWAYS the pool-sampled ones; the
  assigned `reading_topics`/`listening_scenarios` entry supplies scene and
  content only, and you write the passage/dialogue from it yourself
  (`exam-blueprint` Part II — no external source).
- Answer keys go at the END of each Markdown source, never inline
  (`jlpt-exam-structure` owns the key-table format).
- **Before spawning the 4 subagents, pre-assign each of the 13 読解/cloze
  surfaces (問題9 cloze + 問題10×5 + 問題11×4 + 問題12 + 問題13 + 問題14) a
  closing-move shape**, distributing `question-authoring/references/dokkai.md`'s
  named shape list across all 13 without exceeding its per-shape cap. Left to
  4 subagents blind to each other's choices, closings converge on the same
  "safe" default shape — a recurring failure (`dokkai.md` §"Thirteen surfaces,
  thirteen different essays" documents it 3 times over). Pass the 読解
  subagent its assigned shapes for its own surfaces as part of its prompt;
  this makes shape variety an authoring-time constraint instead of a
  post-hoc QA catch.

## Stage 3 — build + gate

```bash
make lint-draft <id> && make verify-scramble <id> && make booklet <id> && make mp3 <id> && make sheet <id> && make check
```

- Run `make lint-draft <id>` first: instantly catches contractions, reaction turns, abs-quantifiers, and missing blanks with zero tokens before invoking QA.
- `make check` validates every test on disk; **read every line, including
  WARN** — resolve each warning or justify it in the report. Fix failures
  before stage 4: a mis-keyed item is invisible once the MP3 is built.
- Then do the **whole-paper topic pass** (next section) — no script sees it —
  and **append this test's row to `logs/topics.json`** from the finished
  sources: `surfaces` (each 読解 passage, 問題9, 問題14, every 聴解 item incl.
  例, as one noun phrase each) and `shapes` (each 聴解 item's errand shape).
  Row format and why the file exists: `exam-blueprint` §"logs/topics.json" —
  the next test's whole-paper topic pass reads it to check for repeated
  subjects.

## One topic, one surface (whole-paper pass, stage 3)

The failure mode that survives every automated gate: the same content on two
surfaces of one paper, or recycled from recent papers. List every surface's
topic in ONE table — 問題9 cloze, each 問題10–13 passage, the 問題14 flyer,
each 聴解 item — with one column per test (this one and the two before it),
**plus a `theme` column and, for the 読解 surfaces, a closing-move column**,
and check:

- **The theme column is filled from the SHIPPED surface, for every surface.**
  Every `reading_topics`/`listening_scenarios` entry (including 問題9's) now
  carries its pool theme by construction, but a drafted passage can still
  wander off its tag — re-tag from what you actually wrote, not from the spec
  (20260810_1 shipped five `働き方` reading surfaces against a cap of 2 this
  way, back when the cloze and web seeds also arrived untagged). Then apply
  `exam-blueprint` §"The four theme rules" to that column and write the counts
  into your report. This is the column the spec-side WARN cannot produce,
  because the sampler cannot see which entry became which 問題.
- **The closing-move column is a 読解 rule with its own owner** —
  `question-authoring/references/dokkai.md` §"Thirteen surfaces, thirteen
  different essays". Two passages on unrelated subjects that both end
  「〜だけでは足りない、〜こそが要る」 are one essay written twice; official
  ships that move 5–9 times per 読解 half and 20260810_1 shipped it 33 times.

- **No topic appears twice in this paper**, even in a different register (an
  essay and a monologue on one subject are still a repeat). For example, avoid
  having the 問題14 flyer spell out a 聴解 item's keyed answer in its fine
  print, or having one デジタルデトックス essay serve both 問題9 and 問題10(1).
- **No topic repeats the previous test.** Avoid duplicating a topic from the
  previous paper, especially in the same 聴解 slots.
- **A topic/domain match found in the 2-tests-back column is a minor finding,
  not an automatic fail** — note it in the QA report even though it does not
  block the paper, so a domain (e.g., civic waste-sorting notices) doesn't
  become a recurring crutch across the pool one skip apart. The three-test
  table exists precisely to catch this column too, not just the immediate
  previous-test one. (Root-caused from `qa/qa-report-20260810_2.md` R2.)
- **No condition, number, or rule shared** between the 問題14 flyer and any
  聴解 item. Shared setting is tolerable; shared decisive detail is not.
- **Two 聴解 items may not run the same errand**, and errand **archetypes**
  (reschedule call, model choice at a store, campaign flyer…) must not repeat
  within the last two tests — add a shape column, not just a subject column
  (e.g., avoiding having a reschedule-an-appointment call run across
  consecutive tests). **This rule DOES apply to 聴解問題5-2番's fixed task
  shape** ("two people each pick a different option from a shared list by a
  stated attribute") even though that shape is inherent to the official
  統合理解 format — 3 consecutive generated papers ran it on a materially
  identical structure (menu choice, then rental listing, then course choice).
  The archetype constraint binds the SPECIFIC scenario category (a two-person
  pick-one-from-a-shared-list decision), not just literal repeated content —
  vary the underlying decision structure itself (e.g., one item that is a
  single person choosing among options with a change of mind, not always two
  people independently landing on two different picks) across consecutive
  papers, not only the subject matter.
- **問題12 (A/B) gets its own cross-test column** — it is one topic per paper
  and repeated three papers running (働き方) once already.
- **A duplicated topic in the spec is a sampler defect**: `check_spec_blend`
  (`tools/check_consistency.py`) fails a `reading_topics`/`listening_scenarios`
  draw that repeats an entry. `--reroll` the category; never invent a
  substitute topic for a surface by hand.

## Stage 4 — QA

Read `exam-qa-review/SKILL.md` in full and run it with fresh eyes. NOT
optional: generated papers can ship content defects through a green gate if QA is skipped.
A test that has not survived this pass is not done, whatever the gate says.

## Stage 5 — Model Answer & Detailed Explanation (FINAL STEP)

```bash
make scaffold-explanations <id>    # -> auto-scaffold tests/<id>/詳細解説.json from markdown (saves ~75% tokens)
make model-answer <id>             # -> tests/<id>/模範解答.html
```

- **MUST always be the final step**: run only AFTER Stage 4 QA has returned
  `QA: PASS` and all item, option, and audio fixes are frozen.
- Scaffold `詳細解説.json` with `make scaffold-explanations <id>`, then author the explanations (`why_correct`, `options_analysis`, `points`). Stems, options, reading passages, and audio scripts are automatically populated from the finalized markdown.
- **Pedagogical Quality & Furigana Rules**:
  - Explanations must be concise, natural, and learner-friendly.
  - Zero internal dataset/pipeline metadata leaks (no `[kanji-n2.json]`, `[同分野]`, `[N1]`, `〜れる一段動詞×4`, `送り仮名「れる」からは絞り込めない` etc.).
  - All options (1, 2, 3, 4) must receive concrete individual explanations (no placeholder text like "選択肢 1 は文脈・文法制約に合致しません").
  - Mandatory furigana (`《...》` or `｜漢字《かんじ》`) on target kanji, stems, and key vocabulary across explanations.
- Generating `模範解答.html` earlier in the pipeline is prohibited because any
  subsequent question, distractor, or key fixes during QA would cause explanations
  to drift and desynchronize.
- Re-run `make check` after generating `模範解答.html` to confirm all file contracts
  remain green.

## Taking the exam (after QA and Model Answer)

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
  only; all items original. The sampled topic gives WHAT to write about;
  compose the words yourself (`exam-blueprint` Part II) — no web fetch.
- Commit `tests/<test_id>/` and the updated `logs/` together with the pipeline
  changes that produced them.
