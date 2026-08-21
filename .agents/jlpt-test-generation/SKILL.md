---
name: jlpt-test-generation
description: End-to-end workflow for generating a complete JLPT mock exam (N1-N5, primarily N2). Use this skill whenever the user asks to create, generate, or build a JLPT test, mock exam, 模擬試験, practice test, or any subset of one (言語知識, 文字・語彙, 文法, 読解, 聴解/choukai), or asks to regenerate/fix exam deliverables. This is the entry-point skill for generation — it owns the 4-stage pass structure and the per-stage reading map, and routes to the specialized skills. Consult it FIRST before any generated exam work, even for partial requests like "make a listening section" or "create N2 grammar questions". For importing an external PDF/past paper, use external-test-import instead.
---

# JLPT Test Generation (Orchestrator)

## Import vs generate

If the user wants to **import** an existing external exam (PDF booklet, past
paper under `refs/JLPT_N2_NEW/`, script PDF, listening MP3) into project
format → stop here and read `external-test-import/SKILL.md` instead. Those
tests live under `tests/imported-<slug>/`. This file is only for
**generating** new mocks.

## Read this file to the end before your first tool call

This is the entry point for **all generated** exam work, including partial
requests. `AGENTS.md` §0 states the compliance rule and what to report at
the end. Layout, deliverable filenames, and `refs/` paths: `AGENTS.md` §2–3.

## The 4-stage pipeline

**Run it as an orchestrator, not as a worker.** The context that owns the
request spawns subagents per the table below and does none of the content
work itself. State flows between stages only through files on disk — never
through the orchestrator paraphrasing content into a prompt, which is
exactly the "memory of what I meant" that shipped every historical mis-key.

Two context-isolation rules are non-negotiable, because both shipped failure
modes are context problems: (a) **no long single-run authoring** — defects
cluster in whatever one context writes last; (b) **QA is a context that
authored nothing** — an author cannot audit its own intent.

| Stage | Job | Contexts |
|-------|-----|----------|
| 1. Blueprint | Sample the pool (topics/scenarios authored directly from the draw — no web harvest) | 1 subagent |
| 2. Author | 文字・語彙 (問1–6) \| 文法 (問7–9) \| 読解 (問10–14) \| 聴解 (booklet §聴解 + script) | 4 subagents, **in parallel** |
| 3. Build + gate | Booklet HTML, MP3, 解答.html, `make check`, whole-paper topic table | 1 subagent |
| 4. QA | `exam-qa-review` in full — blind-solve first, all 101 items, root-cause table | 1 **fresh** subagent |
| 5. Model Answer (Final) | `詳細解説.json` → `make model-answer <id>` → `模範解答.html` — **MUST always be the final step** after QA PASS | 1 subagent |

Every QA finding adds a fix + re-review round: the fix may reuse an
authoring context; the re-review of the touched items must again be fresh
eyes. **Exception: a QA round returning FAIL with ≤3 findings total may be
fixed directly** — same rigor as the round-3 fallback below (root-cause,
verify `make check`, sanity-read the diff), stated explicitly in the final
report. The loop ends at `QA: PASS`, **capped at 3 fresh-eyes QA rounds
total.** Once PASS, proceed to Stage 5. If round 3 still FAILs, apply that
round's findings directly (same rigor) without a 4th fresh-eyes pass; ship
and say so explicitly — which findings were fixed without independent
re-verification, and why. PASS closes the *paper*, not the *generator*: an
open entry in QA's root-cause table blocks the next generation run until
applied or rejected with a reason.

**`make sample <next>` may not run while any test's QA is open** — not while a
round is being written, not while its findings are being applied. The ledger it
writes, `logs/ledger.json`, is the same file the open review is auditing, so
sampling underneath a reviewer invalidates the provenance half of the pass it is
reading (step 6) and reds `make check` for every finished paper on disk while it
does. `20260818_1` was sampled at 11:31 during round 3 of `20260817_3` and did
exactly that (R3-6). The next paper starts when the open paper's findings are
applied or rejected — that is the same gate the sentence above names, stated as
a command instead of as a principle.

**Fallback with no subagents:** approximate the table with new sessions,
one stage per session, handing off through disk. The one split that
survives every fallback: **authoring and QA in different contexts.**

## Per-stage reading map

Each subagent reads exactly these files at the START of its stage (from
disk, never from the orchestrator's summary), and nothing else:

| Stage | Reads | Writes |
|-------|-------|--------|
| 1 Blueprint | `exam-blueprint/SKILL.md` | `tests/<id>/test_spec.json`, `logs/ledger.json` |
| 2 文字・語彙 | `test_spec.json` + `question-authoring/SKILL.md` + `references/moji-goi.md` + `jlpt-exam-structure/SKILL.md` | 問1–6 fragment of `言語知識・読解.md` |
| 2 文法 | same, with `references/bunpou.md` | 問7–9 fragment |
| 2 読解 | same, with `references/dokkai.md` | 問10–14 fragment |
| 2 聴解 | `test_spec.json` + `question-authoring/SKILL.md` + `references/choukai-items.md` + `choukai-audio/SKILL.md` + `jlpt-exam-structure/SKILL.md` | `聴解.md` (incl. セクション構成表), `聴解スクリプト.txt` |
| 3 Build+gate | `exam-app/SKILL.md`, `choukai-audio/SKILL.md` (synthesis §), this file's topic-table § | `言語知識・読解.md` (merged), HTML/MP3, `logs/topics.json` row, gate report |
| 4 QA | `exam-qa-review/SKILL.md` (routes to what it needs) | `qa/qa-report-<id>.md` |
| 5 Model Answer | `exam-model-answer/SKILL.md` | `tests/<id>/詳細解説.json`, `tests/<id>/模範解答.html` |

Stage-2 authors write **section fragments** to
`tests/<id>/_sections/<問題range>.md` — booklet body, then its
answer-key/解説 rows under a literal `<!-- KEY -->` marker. Stage 3 merges
mechanically: all bodies in booklet order (問1→問14), then ONE key heading
at the END, followed by key tables in the same order — the sheet builder's
`strip_key()` truncates at that heading, so a fragment must never carry its
own. Parallel authors never write to the same file. The 聴解 author owns
both `聴解.md` and `聴解スクリプト.txt` complete (body + keys at end,
synchronized), finishing by writing its **セクション構成表** after the key
heading and checking its columns against `choukai-items.md`'s per-section
quotas — the only view in which a repeated key or a one-shape section is
visible.

### Subagent prompt template (all stages)

> Read, in full, from disk: [stage's reading-map row]. Your inputs are
> [files]; your only outputs are [files]. Author ONLY what
> `tests/<id>/test_spec.json` prescribes — items, topics, and
> `answer_positions` are the contract; do not substitute, and treat every
> `origin` field as binding. Report at the end: what you read, what you
> ran, what you wrote, and anything you skipped and why.
>
> (読解 subagent only) Your assigned closing-move shape for each surface in
> your range is: [surface → shape]. Write to that shape; note if a draft
> genuinely cannot fit its assignment and why.

## Stage 1 — blueprint rules

```bash
make sample <id> SEED=<n>          # -> tests/<id>/test_spec.json + ledger
```

- **The seed is an RNG output, never a number you write down** — run
  `python3 -c "import secrets; print(secrets.randbelow(10**8))"` and use it
  verbatim. Agent-"picked" seeds are date-shaped and collide across
  sessions. Must be a seed no previous test used (`logs/ledger.json`).
- No harvest/merge step. `test_spec.json`'s `reading_topics` and
  `listening_scenarios` are what every 読解/聴解 surface is authored from
  (`exam-blueprint` Part II).
- **Do not run this while another test's QA is open** — `make sample` writes
  `logs/ledger.json`, which the open review is auditing (§"The 4-stage
  pipeline"). Check for an unresolved `qa/qa-report-*.md` before sampling.

## Stage 2 — authoring rules

Construction rules live in `question-authoring` (core + the per-section
reference file from the reading map).

```bash
make scaffold-sections <id>        # -> pre-scaffolds tests/<id>/_sections/ templates
```

- Author ONLY items in `test_spec.json`; keys go where `answer_positions` says.
- **文字・語彙 stems are quota-bound too, not just its items** — 問題1/2/5 median
  17 JP chars with ≥9 of 15 comma-free, ≥7 of the 25 問題1–5 stems in です・ます
  with ≥1 first-person and ≤2 institution-actor stems, 問題4 median ≤30 and no
  stem past 44 (`moji-goi.md` Part 0 §"The stem"). Fourteen papers missed all of
  these before they were written down; `make check` now measures every one.
- For 問題1 & 問題2 2×2 matrices, build the grid BY HAND against
  `moji-goi.md`, then CHECK it with
  `python3 tools/matrix_helper.py validate --reading <かな> <4 options>`.
  The tool's two GENERATORS are hard-disabled — they had no 音訓 table and
  invented readings and glyphs (F4, qa-report-20260819_1).
- Tested items (grammar/vocab/kanji) are ALWAYS pool-sampled; the assigned
  `reading_topics`/`listening_scenarios` entry supplies scene/content only —
  you write the passage/dialogue from it yourself.
- Answer keys go at the END of each Markdown source, never inline.
- **Before spawning the 4 subagents, pre-assign each of the 13
  読解/cloze surfaces a closing-move shape** from
  `dokkai.md`'s named list, without exceeding its per-shape cap — 4
  subagents blind to each other's choices converge on the same "safe"
  default shape (documented 3 times over). Pass each 読解 subagent its
  assigned shapes as part of its prompt.

## Stage 3 — build + gate

```bash
make autofix <id> && make lint-draft <id> && make verify-scramble <id> && make booklet <id> && make mp3 <id> && make sheet <id> && make check
```

- Run `autofix`/`lint-draft` first: auto-applies conversational
  contractions, catches contractions/reaction-turns/abs-quantifiers/missing
  blanks at zero tokens before QA.
- `make check` validates every test on disk; **read every line, including
  WARN** — resolve each or justify it in the report. Fix failures before
  stage 4: a mis-keyed item is invisible once the MP3 is built.
- Then the **whole-paper topic pass** (below) — no script sees it — and
  **append this test's row to `logs/topics.json`**: `surfaces` (each 読解
  passage, 問題9, 問題14, every 聴解 item incl. 例, one noun phrase each) and
  `shapes` (each 聴解 item's errand shape). Row format:
  `exam-blueprint` §"logs/topics.json" — the next test's whole-paper pass reads it.

## One topic, one surface (whole-paper pass, stage 3)

The failure mode that survives every automated gate: the same content on
two surfaces of one paper, or recycled from recent papers. List every
surface's topic in ONE table — 問題9 cloze, each 問題10–13 passage, the
問題14 flyer, each 聴解 item — with one column per test (this one and the
two before it), plus a `theme` column and, for 読解 surfaces, a
closing-move column, and check:

- **The theme column is filled from the SHIPPED surface, for every
  surface.** Every entry carries its pool theme by construction, but a
  drafted passage can still wander off its tag — re-tag from what you
  actually wrote. Apply `exam-blueprint` §"The four theme rules" and write
  the counts into your report.
- **The closing-move column is a 読解 rule** — `dokkai.md` §"Thirteen
  surfaces, thirteen different essays". Two passages on unrelated subjects
  both ending 「〜だけでは足りない、〜こそが要る」 is one essay written twice;
  official ships that move 5–9 times per 読解 half.
- **No topic appears twice in this paper**, even in a different register.
  Avoid e.g. a 問題14 flyer spelling out a 聴解 item's keyed answer, or one
  subject serving both 問題9 and 問題10(1).
- **The drawn `quick_response` phrases are content too — put every one of them
  in the table as a row** (`test_spec.json["items"]["quick_response"]`, 11 in a
  current paper = 聴解問題4-1番〜11番), with the setting you invented for each. They are the surfaces nobody thinks of as
  topics because nobody *chose* their subject: the sampler hands over an idiom
  and the author invents a scene around it, so the scene never gets tagged and
  never gets compared. `20260817_3` wrote a 問題9 cloze whose thesis was
  「何をどう書けばよいのか分からないまま紙に向かう心細さ」 while its own drawn
  聴解問題4-1番 stimulus was 「この申請書の書き方がよく分からないのですが」 — an
  in-paper echo, and the 12 rows would have shown it in one read. A
  quick_response scene that restates another surface's subject is a repeat
  even though nobody chose it. Check them against 問題9's subject
  specifically — the cloze is the other unpooled surface (`exam-blueprint`
  §"The four theme rules" rule 4b).
- **No topic repeats the previous test**, especially in the same 聴解 slots.
  **Do this as a table read, not as a recollection:** build the slot × 3-paper
  table from `logs/topics.json` — it is already stored, so this is a lookup, not
  a re-derivation — and read each ROW across the columns. A shared domain in one
  row is a finding even when the errand keys differ and the theme tags differ.
  `20260818_1` put 自動車学校の危険予測運転 in 聴解問題3-4番 directly after
  `20260817_3`'s 問題3-4番 整備担当が運転の癖を伝える話 (tagged 教育 and 交通, so
  no tag matched) and put a house-move gas appointment in 問題2-1番 after a
  house-move quote in the same slot. The 問題2-1番 half was re-angled in the
  round-2 fix pass (same drawn errand, a tenant returning from a year abroad
  instead of a move); the 問題3-4番 half was closed before round 3 by the cheaper
  of its two repairs — its scenario 自動車学校:学科 is DRAWN, so the talk was
  RE-SLOTTED (swapped with 問題3-2番's), which costs a re-order of both items'
  spoken options so each key still lands where `answer_positions` says and a
  re-derivation of both 解説, and costs no new authoring. A reroll is the other
  route and is the dearer one: a fresh 220+-char 概要理解 talk plus four new
  topic-level options plus a scenario that must itself clear cooldown, theme and
  slot rules. `check_slot_theme_repeat()`
  WARNs the half a tag can see (**問題2/3/5 slots only** — 問題4's scenes are
  invented, so its tags measure the tagger, and 問題1's item mix is quota-bound,
  so 働き方 there measures the rule: R2-F7); the 運転 half is exactly what a tag
  cannot see, which is why this row read stays mandatory.
- **A topic/domain match in the 2-tests-back column is a minor finding**,
  not an automatic fail — note it so a domain doesn't become a recurring
  crutch one skip apart.
- **No condition/number/rule shared** between the 問題14 flyer and any 聴解
  item. Shared setting is tolerable; shared decisive detail is not.
- **Two 聴解 items may not run the same errand**, and errand archetypes
  (reschedule call, model choice at a store, campaign flyer…) must not
  repeat within the last two tests — including **both 聴解問題5 items**, each of
  which has its own fixed task shape:
  - **問題5-1番** — a multi-person meeting choosing among proposals.
  - **問題5-2番** — a two-person pick-one-from-a-shared-list decision.

  For **each** of them, vary the underlying DECISION STRUCTURE across
  consecutive papers, not just the subject: who proposes, in what order
  candidates are killed, and whether the adopted one is a late arrival, an
  opening proposal held pending a condition, or a plan someone reverses. The
  bullet named 2番 only until 2026-08-19, and 4 of 4 papers carrying a
  セクション構成表 documented 2番's structure against the last three papers while
  saying nothing about 1番 — so `20260818_1` shipped a 問題5-1番 with
  `20260817_3`'s exact archetype (a three-person local-association meeting that
  rejects three proposals on three grounds and adopts a NEW idea raised late) in
  the same slot, one paper apart, with the rule "already written"
  (`qa-report-20260818_1` F3). **The construction step, not the judgment:** the
  聴解 author writes the 問題5 構成表's structure note for **1番 as well as 2番**,
  each against the previous three papers by name — see
  `question-authoring/references/choukai-items.md` §統合理解.
- **問題12 (A/B) gets its own cross-test column** — one topic per paper.
- **A duplicated topic in the spec is a sampler defect**: `check_spec_blend`
  fails a repeated draw. `--reroll` the category; never invent a substitute
  by hand.

## Stage 4 — QA

Read `exam-qa-review/SKILL.md` in full and run it with fresh eyes. NOT
optional: generated papers can ship content defects through a green gate if
QA is skipped. A test that hasn't survived this pass is not done, whatever
the gate says.

## Stage 5 — Model Answer & Detailed Explanation (FINAL STEP)

```bash
make scaffold-explanations <id>    # -> auto-scaffold tests/<id>/詳細解説.json from markdown
make model-answer <id>             # -> tests/<id>/模範解答.html
```

- **MUST always be the final step** — run only AFTER Stage 4 returns
  `QA: PASS` and all item/option/audio fixes are frozen.
- Scaffold `詳細解説.json`, then author the explanations (`why_correct`,
  `options_analysis`, `points`). Stems/options/passages/audio scripts are
  auto-populated from the finalized markdown.
- **Pedagogical Quality & Furigana**: concise, natural, learner-friendly
  explanations; zero internal pipeline metadata leaks (`[kanji-n2.json]`,
  `[N1]`, etc.); all four options get concrete individual explanations (no
  placeholder text); mandatory furigana (`《...》`) on target kanji/stems/key vocabulary.
- Generating `模範解答.html` earlier is prohibited — any subsequent
  question/distractor/key fix during QA would desynchronize the explanations.
- Re-run `make check` after generating it, to confirm all file contracts
  remain green.

## Taking the exam (after QA and Model Answer)

`make serve` (no test id — one server lists every test), answer, press
「採点する」: the page saves `採点結果.json` + `ユーザー解答.json` into
`tests/<id>/`. CLI: `make grade <id>`. See `exam-app`.

## Invariants (every run)

- Japanese file names for all deliverables (table: `AGENTS.md` §2).
- Markdown is the single editable source. **Every source edit carries its
  rebuild in the same change**: `聴解スクリプト.txt` → `make mp3 <id>`;
  either `.md` → `make booklet <id> && make sheet <id>`. Artifacts carry the
  sha of the bytes they were built from, and the gate compares them — but
  the gate is the backstop, not the workflow. Never hand-edit a sha.
- `聴解.md` and `聴解スクリプト.txt` stay synchronized: printed 例 options ↔
  spoken 例; any script item change requires a key check.
- After script/audio edits, re-run the dry-run validators in `choukai-audio`.
- Never copy questions from the copyrighted textbooks in `refs/` —
  calibration only; all items original. The sampled topic gives WHAT to
  write about; compose the words yourself — no web fetch.
- Commit `tests/<test_id>/` and updated `logs/` together with the pipeline
  changes that produced them.
