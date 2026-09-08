# MIGRATION.md — N2-only → all five levels, and `JLPT-N2` → `JLPT`

**Status: analysis + decisions. No code has moved yet.** Written 2026-09-08
against commit `479e9f6`. This file is the single owner of the migration plan;
when a step lands, the rule it establishes moves to its permanent owner
(`AGENTS.md`, the level table, or the skill that owns that area) and the step
here is marked done with a pointer. Nothing in this file outlives the
migration.

## Goal

1. Generate and import exams at **N1, N2, N3, N4, N5** — N1 is the priority
   after N2.
2. Rename the GitHub repo `feiluvnana/JLPT-N2` → `feiluvnana/JLPT`.
3. Serve the Pages site as `…/JLPT/N2/`, `…/JLPT/N1/`, … with a level chooser
   at the root.

Each level gets its own `refs/` archive — the user is sourcing them, so the
calibration corpus is an input to this plan, not a blocker in it. What the plan
must guarantee is that a level with no archive yet **cannot go green by
skipping**: an absent corpus already `skip`s per `AGENTS.md` §3, and a skip is
not a pass.

## The one constraint that shapes every decision

`AGENTS.md` §4: *a measured number has one owner, and it is a script.* Adding
levels does not weaken that — it indexes it:

> **A measured number has one owner, it is a script, and it is per level.**

Every N2 band in this repo is a measurement over `refs/JLPT_N2_NEW/`. None of
them generalizes by scaling, interpolation, or recollection. An N1 band comes
from an N1 archive measured by the same profiler, or it does not exist. This is
the defect class `REPORT-GOI.md` §F10 records, and level migration is the
single best opportunity this repo will ever have to reproduce it at scale.

---

## 1. Layer inventory

### Layer 1 — already level-neutral. No work.

`build_booklet.py`, `serve_sheet.py`, `index_view.py`, `local_store.py`,
`build_pages.py`, the TTS engine in `make_choukai_mp3.py`, every `extract_*`
tool, `origin.py`. These move Markdown → HTML → browser and never ask the
level.

Two of them are the patterns to copy rather than invent:

- `grade_answers.py:45` — `GENGO_SHAPES` is a **shape table keyed by item
  count**, with the 大問 taxonomy *derived* from it (`gengo_taxonomy()`,
  `gengo_goi_cutoff()`). Built for the three-era N2 problem; it is already
  three-quarters of the per-level shape table.
- `origin.py` — a folder-name prefix as a first-class discriminator, parsed in
  exactly one file, consumed everywhere. `level` slots into the identical
  mechanism and should get a sibling module, not a second convention.

### Layer 2 — level-parameterizable. Mechanical.

| Site | What is hardcoded |
|---|---|
| `tools/goi_profile.py:36`, `dokkai_profile.py:32`, `choukai_profile.py:37`, `lexical_profile.py:69` | `ROOT/"refs"/"JLPT_N2_NEW"` — four copies of one path |
| `tools/check_consistency.py:8374` | the same archive path again |
| `.agents/exam-model-answer/scripts/build_model_answer.py:32-39` | 問題→`(start, end)` range map for the 71-item paper |
| `.agents/exam-app/scripts/build_interactive.py:745-751` | `else if (first === '57')` chain: question number → 大問 label |
| `.agents/exam-app/scripts/build_interactive.py:1351`, `build_model_answer.py:1427` | `feiluvnana/JLPT-N2/releases/download/audio/…`, twice |
| `logs/ledger.json`, `logs/topics.json` | one global rotation space for all levels |

The ledger is the one with teeth. Levels draw from different pools, so a shared
history lets an N1 draw consume an N2 cooldown slot, and
`check_draw_provenance()` — which requires every recorded draw to resolve to a
pool entry — starts failing against the wrong pool. **Namespace the history by
level before the first non-N2 `make sample` ever runs.**

### Layer 3 — genuinely per level. The bulk of the work.

| Asset | Size today | Per-level? |
|---|---|---|
| `.agents/jlpt-exam-structure/SKILL.md` | 341 lines, all N2 format facts | yes — structure differs at every level |
| `.agents/exam-blueprint/references/pools.json` | 4,600 entries; category names *are* N2 section names (`grammar_p7`, `grammar_p8`, `quick_response`) | yes |
| `.agents/question-authoring/references/` | ~230 KB (`moji-goi.md`, `bunpou.md`, `dokkai.md`, `choukai-items.md`, `official_calibration.md`, `level_band_grammar.txt`) | **split**: method is shared, bands are per level |
| `.agents/choukai-audio/references/` | 38 KB pacing + register measurements | **split**, same way |
| `tools/check_consistency.py` | 11,000 lines, 178 checks, dozens of measured constants (`DOKKAI_FLOOR`:1896, `P7_MEAN_BAND`:1042, `NOVEL_SHARE_*`:1995, `SPAN_JP_MAX`:1695, `WAGO_DIST`, `SECTION_MODE_DIST`) | **triage** — see §5 |
| `.agents/exam-blueprint/scripts/sample_items.py` | `DRAW`:645, `ANSWER_SECTIONS`:663, `MAX_SECTION_MODE`:738, `KATAKANA_TARGET_RATE`, `KUN_TARGET_RATE`, `TRAP_TARGET_RATE` — every one an archive measurement | yes, as data |

The "split method from bands" move is what keeps this from becoming five
divergent copies of a 60 KB prose file. How to write a distractor is
level-neutral and stays in one place. How long a 問題11 passage runs is a
measurement and lives in a per-level band file regenerated from `--baseline`
output, never retyped.

---

## 2. Decision: flat, level-prefixed test ids — do NOT nest `tests/`

**Adopted:** `tests/n1-20260907_1/`, `tests/imported-n1-2025-12/`. N2 keeps its
current bare ids; a missing level prefix means N2. `import_meta.json` already
carries `"level"`; generated `test_spec.json` gains it (it has none today).

**Rejected: `tests/N1/<id>/`.** It reads better and costs far more:

- ~10 sites in `check_consistency.py` walk `tests/` with `glob("*")` or
  `iterdir()` (:672, :3124, :6963, :8212, :8365, :13451, :13887, …), as do
  `build_pages.deployable()` and `serve_sheet`. Under nesting every one of them
  returns **level directories instead of tests** — no error, no failure, just
  zero per-test checks silently running.
- 10 `.gitignore` patterns are `tests/*/…` (`segments/`, `_extract/`,
  `_sections/`, `*.wav`) and stop matching. `tests/**/*.mp3` (:56) survives, but
  the pattern class that broke is exactly the one from `AGENTS.md` §2 where 16
  MP3s stayed tracked for ten days.
- Release assets are flat — `audio/<test_id>.mp3`. Nesting invites `N1/1` and
  `N2/1` colliding on one asset name and one `logs/upload_manifest.json` row.
- All levels share one browser origin under `/JLPT/`, so they share one
  `localStorage` (`local_store.py:27`, `STORAGE_PREFIX = "jlpt-mock/v1"`).
  Globally unique test ids make those keys unique for free; nested ids need the
  level threaded into the key schema.

**New owner:** `.agents/external-test-import/scripts/level.py` (beside
`origin.py`, same shape) — `level_of(test_id) -> "N1".."N5"`, `LEVEL_PREFIXES`,
and the id builder. Every reader goes through it, the way every reader goes
through `test_origin()`.

## 3. Decision: URL layout is separable from disk layout

`index_view.py:229` already emits **relative** links in Pages mode
(`MODE === 'local' ? 'tests/' : '/tests/'`), so the deployed tree can be
re-shaped without touching the app:

```
_site/index.html            level chooser (new)
_site/N2/index.html         today's test list, filtered to N2
_site/N2/tests/<id>/…       解答.html, 模範解答.html, 聴解.mp3
_site/N1/…
```

This is a change to `build_pages.py`'s output tree and one new root screen.
Nothing else learns about it. It can land before, after, or independently of
the level work — and it is the visible half of the request, so it is cheap to
ship early.

**Repo rename cost is two lines plus a base path.** The two hardcoded
`feiluvnana/JLPT-N2` audio fallbacks (`build_interactive.py:1351`,
`build_model_answer.py:1427`) become one `repo_url()` owner. GitHub redirects
the old repository path, so the `audio` and `refs` release tags survive the
rename — `AGENTS.md` §3's "never rename a tag" is about the tag, not the repo.
Pages base moves `/JLPT-N2/` → `/JLPT/`; already-deployed sheets keep working
through the redirect, but re-run `make pages` rather than relying on it.

## 4. Decision: `refs/` naming, and the two axes named `level`

**Archive:** `refs/JLPT_<LEVEL>_NEW/` — `refs/JLPT_N1_NEW/` beside today's
`refs/JLPT_N2_NEW/`. Same per-sitting layout, same `booklet.md` / `script.md` /
`key.md` / `audio_inspection.md` extracts, same `answer_keys.json`. The four
profiler constants become `ROOT/"refs"/f"JLPT_{level}_NEW"`, one f-string.
Release zips follow: one per top-level `refs/` folder is already the rule
(`AGENTS.md` §3), so `JLPT_N1_NEW.zip` needs no new mechanism.

**Textbooks:** PDF filenames already carry the level
(`Shin_Kanzen_Masuta_N2-Bunpou.pdf`), so volumes can sit side by side. The
**extracts cannot** — `refs/Shinkanzen/goi_reference.md` is a flat tracked name
that would collide. Put extracts under a level subfolder
(`refs/Shinkanzen/N1/goi_reference.md`) and give each `extract_*` tool a
`--level`.

**The trap: `level` already means something else in this repo.**
`level_data.py:19`'s `LEVELS = ("N1".."N5", "unknown")` is a **classification**
axis — *what level is this pool item?* — used by `level_band_grammar.txt` to
keep N2 pools inside the N2 band (`check_consistency.py:5904`). The new axis is
a **target**: *what level is this paper?* They are different, and for N1 the
band inverts — today's `TOO_HARD` list becomes the target and N2 entries become
`TOO_EASY`. Do not let one word carry both meanings. Suggested split:
`item_level` (classification, existing) vs `exam_level` (target, new).

## 5. The 178-check triage

`make check` is the gate for all of this, and it is where a half-migrated repo
will lie to you. Every check falls into one of three classes:

- **level-agnostic** — deliverable file contract, key-table parse, `詳細解説`
  terseness bands, MP3-tracked/manifest/deploy checks, ruby markup. Unchanged.
- **level-parameterized** — a threshold that becomes a lookup in that level's
  band file. Most of the measured constants in the Layer 3 table.
- **level-exclusive** — a check whose subject only exists at some levels (every
  問題3 語形成 check, if N1 has no 語形成 大問).

**Mechanism:** each check declares the levels it applies to; the runner routes
a non-applicable check through the existing `skip()` path so it still prints.
An invisible skip is how a level goes green with nothing verified, which is the
`AGENTS.md` §3 failure mode restated at a new scale. `make findings`
(`logs/findings.json`) should carry the level per record so a repair plan is
never ambiguous about which paper it is describing.

## 6. Structural divergences that break current contracts

Ordered by how much they cost, which is **not** the order you would guess:

1. **N4/N5 run two separate 言語知識 sittings** (文字・語彙 apart from
   文法・読解). `AGENTS.md` §2's deliverable table is a *fixed* file contract with
   one `言語知識・読解.md`. It has to become a **per-level deliverable
   manifest**, read by `build_booklet`, `build_interactive`,
   `build_model_answer`, `build_pages`, `verify_fidelity`, and the gate's file
   checks. This is the largest architectural change in the whole migration, and
   it arrives from N5 — not from N1.
2. **大問 counts and question numbering differ per level**, so every
   question-number → 大問 mapping must be table-driven (the three Layer 2
   sites). The generated-vs-imported item-count split that `grade_answers.py`
   already handles is the same problem one axis wider.
3. **Item totals and score bands are not 71+30=101 / 180 everywhere.** These
   are load-bearing literals in `serve_sheet.py:42`, `index_view.py:39`,
   `build_interactive.py` (:523, :869), `grade_answers.py` (:325, :462), and
   `check_consistency.py` (:851, :874). They all resolve to §7 step 2.
4. **The band inversion in §4** — N1 pools must pass a check that today
   asserts the opposite.

## 7. Sequencing

Each step keeps N2 fully working and green. No step depends on a level's
archive existing except the last.

**Step 1 — `level` becomes data.** `level.py` owner, `"level"` in
`test_spec.json`, level-prefixed ids accepted everywhere, per-level ledger and
topics namespaces, level on every `findings.json` record.
*Acceptance:* `make check` green; every existing N2 test resolves to `N2`
through `level_of()` with no id renamed.

**Step 2 — the machine-readable structure table.**
`.agents/jlpt-exam-structure/references/levels/N2.json`: section list (大問
number, type, item count, question range), section timing, deliverable
manifest, total items, scaled-score bands, 聴解 大問 shapes. Point the gate,
`grade_answers`, `build_model_answer`, `build_interactive` and `sample_items`
at it and **delete** the hardcoded 71 / 30 / 101 / 180 and the range maps.
`jlpt-exam-structure/SKILL.md` becomes prose that cites the table rather than
restating it — same relationship `moji-goi.md` has to `goi_profile.py`.
*Acceptance:* N2 still passes `make check` with every structural number read
from a file. **This step alone proves the design.** If it does not hold for N2
alone, no second level is worth starting.

**Step 3 — rename + Pages subroutes + `repo_url()` owner.** Independent of 1
and 2; ship whenever. *Acceptance:* `make pages` emits the level tree,
`make preview-pages` navigates root → level → test → result, and a deployed
sheet still streams its audio.

**Step 4 — triage the 178 checks.** Thresholds move into per-level band files
regenerated from `--baseline`; each check declares its levels; skips print.
*Acceptance:* N2 output is byte-identical in verdict to today, and a synthetic
empty `N1` level produces visible skips rather than silent green.

**Step 5 — per level, repeatable:** land `refs/JLPT_<LEVEL>_NEW/`, run
`make extract-archive` / `make extract-keys`, run the three profilers with
`--baseline` as the **founding measurement**, write that level's band files and
`levels/<LEVEL>.json`, build `pools/<LEVEL>.json` from that level's textbook
volumes, then split the calibration references into shared method + that
level's bands.
*Acceptance:* one generated paper at the new level survives `make check`
**and** a fresh-eyes `exam-qa-review` pass — green is the floor, per
`AGENTS.md` §0.5.

Steps 1–4 are days of work each. Step 5 is where the months are, and it is a
content problem, not an architecture problem — which is the point of doing 1–4
first.

## 8. Open questions

- **Does `pools.json` split by level or gain a level dimension?** Recommended:
  `references/pools/<LEVEL>.json`, one file per level, same schema. Its
  category names are N2 大問 names today, so per-level files also let a level
  name its own categories without a translation layer.
- **Cross-level topic rotation.** Should an N1 paper avoid a 読解 subject an N2
  paper used last week? A learner may sit both. Recommendation: keep the item
  ledger strictly per level (different pools) but make `logs/topics.json`
  **global**, since subject freshness is about the reader, not the item pool.
  Needs a decision before step 1 lands, because it decides the namespace shape.
- **`GENGO_SHAPES` era table × level.** N2 has three eras. Other levels will
  have their own. Key the table `(level, item_count)` or nest it under the
  level file? Prefer the level file — one owner per level, per §2's goal.
- **Does `exam-qa-review` need per-level defect classes**, or is its finding
  taxonomy level-neutral? Unknown until a second level has a paper to review.
