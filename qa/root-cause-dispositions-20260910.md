# Root-cause dispositions — entering the 20260910_1 run

`jlpt-test-generation` §"The fix loop": an open row in a QA root-cause table
**blocks the next generation run until applied or explicitly rejected with a
reason.** This file is that disposition for every row left open by
`qa/root-cause-dispositions-20260909.md` §"Open, DEFERRED" and by
`qa/qa-report-20260909_1-round2.md` §9.1. Written 2026-09-10 by the 20260910_1
orchestrator, **before `make sample`**. The reports themselves are RECORDS and
were not edited.

## Skill rows — all three APPLIED (they were written out verbatim and left unapplied)

| row | disposition | what was done |
|---|---|---|
| **R2-S1** `DOC-WRONG` | **APPLIED** | `.agents/choukai-audio/SKILL.md`, in the mixed-pool block: a fixed seed does NOT fix the draw across composer changes (`avoid_slot`, the figure exclusion and the wear counts all run inside the per-slot choice), so after any `make mp3` re-run the number of moved slots must be diffed out of `logs/choukai_draws.json` and reported. The founding false claim (「only 問題1-2 moved」, actual 25 of 29) is named in the rule |
| **R2-S2** `RULE-MISSING` | **APPLIED** | `.agents/exam-qa-review/SKILL.md` §4 composed-paper block gains **check 5**: the shipped 聴解 key balance is in scope even though the items are not authored here, no section may key one option more than 3 times (official max over 30 four-option sections is 3). This is the 聴解 counterpart of the 71-item `answer_positions` check the gate skips wholesale on a composed paper — the hole R2-F3 reached 8 papers through |
| **R2-S3** `DOC-DRIFT` | **APPLIED, with round 1's S2 updated rather than applied as written** | (a) round-1 **S1**: §6.2's "all 101 positions match `answer_positions`" now reads **71**, with the 30 聴解 positions exempt on a composed paper and check 5 named as the replacement. (b) round-1 **S2** is now stale in the opposite direction — the composer HAS a per-slot previous-paper bar since `d98f109` — so §4 check 1 was rewritten to "the composer bars the previous paper's clip per slot and prints a note if that would starve a slot; verify the bar held and report any starvation note", keeping the 18-of-24 measurement as the reason it is only now a verification. (c) §4 gains: **a re-composed listening half re-opens checks 1–5 in full** |

## The one paper-level row — REJECTED AS A RIDER ON THIS RUN, re-filed standalone

**Row:** *"A composed paper draws 32 pool entries it never spends"* — 21
`listening_scenarios` + 11 `quick_response` per paper, 525 + 275 across 25
papers, feeding no shipped surface since the 2026-09-08 composition rework.

**The defect is real and I am not disputing it.** Re-measured here rather than
quoted: `tests/20260909_1/test_spec.json` carries 21 authored-theme
`listening_scenarios` entries and 11 `quick_response` strings, and the shipped
聴解 half is 29 banked clips that use none of them.

**Rejected as a rider on this generation run, for a reason the 2026-09-09
deferral did not state.** That deferral's argument was positional — "doing it at
the tail of a generation run is how a green gate stops meaning anything" — and
this run is at the HEAD, so that argument does not apply and I did not reuse it.
The decisive reason is different and is a measurement:

1. **Blast radius, counted:** the two categories are read at **30 sites in
   `.agents/exam-blueprint/scripts/sample_items.py` and 85 in
   `tools/check_consistency.py`** (`grep -c`), across ~20 checks plus three
   id-keyed exemption tables (`ERRAND_ROTATION_CATEGORIES`, the pre-`quick_response_keys`
   exemptions, the errand-coverage skips). Changing the draw changes the shape of
   `test_spec.json`, which is the blueprint contract every one of those reads.
2. **The decisive one:** a sampler edited immediately before `make sample` makes
   **this paper the first output of an unverified sampler**. The corpus
   re-verification that change needs (25 generated + 10 imported papers, every
   rotation and blend check) is larger than the run it would ride on, and its
   failure mode — a spec that is subtly wrong but green — is exactly the class
   AGENTS.md §0 exists for. A bookkeeping defect is not worth buying with a
   blueprint-level one.
3. **Harm re-measured, and it is bounded:** `cooldown_for()` is
   `max(2, depth - 2)`, and `draw()` relaxes one step at a time and PRINTS the
   relaxation rather than failing. Unique entries consumed to date:
   `quick_response` 190, `listening_scenarios` 336 (both against a pool that has
   grown over the period, so the figures exceed current pool size and are an
   upper bound on pressure). So the burn costs rotation quality on two categories
   that decide nothing about what the paper TESTS; the grammar, vocabulary, kanji
   and `reading_topics` pools are untouched.
4. **`quick_response` is not wholly unspent, which the row does not say.** The
   drawn strings are still a live input to `check_consistency.py`'s 問題9
   option-collision haystack, so "stop drawing them" is not a pure deletion even
   for that half — another reason it needs its own change and its own review.

**Re-filed as a standalone task, named so the next run can see it:**
*"stop drawing `listening_scenarios`/`quick_response` for composed papers"* —
a `sample_items.py` + `check_consistency.py` change with a corpus re-run over all
35 papers, to be done on its own, not inside a generation run. **The next
generation run inherits this rejection, not the row**: it is decided, and
re-deferring it is not the same as re-opening it. If it is still unbuilt when the
pool pressure above stops being bounded (a `draw()` relaxation note on either
category), that note is the trigger to build it before the next paper.

## Also carried, unchanged, from 2026-09-09 (bank-source rows, not this paper's)

Both are defects in `tests/imported-n2-2024-12/` and in the clip bank built from
it, i.e. a different test's deliverable:

1. **All 29 of the 2024-12 sitting's banked clips give the keyed option the
   Vietnamese reason `"Đúng."`** and nothing else, which `exam-model-answer`
   prohibits. Any paper drawing a 2024-12 clip inherits it.
2. **`2024-12:問題2-3` calls 山下選手 "anh"** where the shipped script gives her
   as `女:`.

**Disposition for this run: repair at the point of use, and say so.** If
20260910_1 draws a 2024-12 clip, stage 5 must fix the inherited pane entries in
`tests/20260910_1/詳細解説.vi.json` and the final report must name which. The
source repair (`tests/imported-n2-2024-12/詳細解説.vi.json` + `make choukai-bank`)
stays out of scope for a generation run for the same reason as the row above.

---

# Round-2 dispositions — the two rows round 1 left open (written 2026-09-10, in the round-2 fix pass)

`qa-report-20260910_1-round2.md` §5 re-filed round 1's **F2-a** and **F2-b** as
**S1** and **S2** after verifying by `grep` that neither had been applied and
that this file said nothing about either. Per the fix loop an open row blocks
the NEXT generation run, so both are dispositioned here. **Both APPLIED**, and
each was applied as round 1 wrote it rather than re-derived.

| row | disposition | what was done |
|---|---|---|
| **F2-a / S1** `RULE-UNENFORCEABLE` — the rhetorical-MOVE cap names no move vocabulary, so a reviewer picks the label granularity and a fine granularity makes any monoculture read as "one over the cap" | **APPLIED** | `.agents/jlpt-test-generation/SKILL.md` §"One topic, one surface", MOVE bullet: read the column down the **SKELETON** before the label — 〈通説または自分の想定した原因 X → ところが／しかし／外れた／ではなかった → 実は Y〉 — every surface running it counts as ONE move however differently the ends are worded (前提の更新・部分最適の反転・予想外の受益者・常識の反転 are all it); **a label spread does not license a skeleton pile-up**; **問題12(A)+(B) count as ONE surface for this cap**. The three papers that went unfiled (`20260904_3` 8, `20260907_1` 7, `20260910_1` 7 on the passage proxy, against official 0–3) are named in the rule, and it points at the new check below as the marker-bearing half only |
| **F2-b / S2** `GATE-BLIND` — the two `not-A-but-B` checks read a marker family, and six of this paper's eight instances performed the reframe with no marker, so both printed green (2 matched / 0 of 13) | **APPLIED** | `check_dokkai_belief_denial_monotony()` in `tools/check_consistency.py`, over `dokkai_closing_scopes()`'s surfaces, counting a surface that carries **BOTH** a belief attribution and a denial pivot (the two regexes round 1 specified, verbatim). **WARN above 3, FAIL above 4**, 問題12 A/B folded to one surface per F2-a |

## Founding-case run for `check_dokkai_belief_denial_monotony()` (§6.5), all 36 papers on disk

| corpus | n | range |
|---|---|---|
| official `imported-n2-*` | 10 | **0–3** (max `imported-n2-2025-07`) |
| generated `20260807_1`…`20260909_1` | 25 | **0–4** |
| `20260910_1` (post round-1 F2 repair) | 1 | **1** |

**It fires on no official sitting, and re-classifies exactly one shipped paper:
`20260817_2` at 4 (問題11(2)/(3)/(4) + 問題13) — a WARN, not a FAIL.** Both
outcomes are what round 1 predicted for it, reproduced here by the landed code
rather than quoted. `make check` went 165 → 166 WARN on exactly that one line
and nothing else.

**The clause this run could NOT test, stated rather than glossed:** the check
landed AFTER `20260910_1`'s round-1 F2 repair, so its founding text is gone from
disk and *"fires on its own founding case"* rests on round 2's hand
re-derivation (6 pre-repair, 3 post on the separate-surface scale), not on a run
of this code. The landed predicate reads the repaired paper at **1**, narrower
than round 2's hand read — which is the caveat, not a contradiction: it sees
only the marker-bearing half of the skeleton. **A low number here is not a
verdict on the MOVE column**, and F2-a's text says so in the skill.

## Carried forward, unchanged

The paper-level row (a composed paper draws 21 `listening_scenarios` + 11
`quick_response` it never spends) is **still rejected as a rider**, on the same
measurement as above; `20260910_1` reproduced it (its spec draws 21 + 11, the
shipped 聴解 half is 29 banked clips using none of them) and round 2 re-recorded
it as an observation rather than a finding. No `draw()` relaxation note has been
printed on either category, so the trigger named above has not fired.
