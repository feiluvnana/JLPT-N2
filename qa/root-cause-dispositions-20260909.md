# Root-cause dispositions — entering the 20260909_1 run

`jlpt-test-generation` §"The fix loop": an open row in a QA root-cause table
**blocks the next generation run until applied or explicitly rejected with a
reason.** This file is that disposition for every open row of
`qa/qa-report-20260907_1-round2.md` §8. Written 2026-09-09 by the 20260909_1
orchestrator; the report itself is a RECORD and was not edited.

## Paper findings of 20260907_1 — all three verified CLOSED on disk

Round 2 reported "nothing was repaired", but the repairs landed between the
report and commit `1ff3316` (§4B of that report records the file moving twice
during the pass). Re-derived by measuring the artifact, not by reading a claim:

| id | state | measurement |
|---|---|---|
| R2-F1 | **closed** | 問題11(4) re-closed onto 「…また来年の話になった。」; the paper measures **1** on the new 〜ていない row (cap 1), passing ON MERIT |
| R2-F5 | **closed** | 問題10-55 key 2 is now 「市からの連絡を待たずに、集会所をいつ開けるかを町内会が決めるということ」; `check_verbatim_keys` with S-1 applied reports `ok` for the whole paper |
| R2-F6 | **closed** | `grep 文頭に固定 tests/20260907_1/` returns nothing |

## Root-cause rows

| row | disposition | what was done |
|---|---|---|
| **S-1** `GATE-WRONG` | **APPLIED** | `SequenceMatcher(..., autojunk=False)` in `check_verbatim_keys`. Corpus run at the fixed predicate moved exactly one id, as the report predicted: `20260827_1` item 67 (LCS 22 / 51 %). **Repaired, not grandfathered** — option 2 re-paraphrased to 「…あとで書き手がどう対応するかで決まるということ」 (LCS now 6). All ten official sittings stay at 0 |
| **R2-F5** (downstream) | **APPLIED** with S-1 | no separate edit, as the row says |
| **R2-F1** `GATE-BLIND` | **APPLIED** | `FINAL_SENTENCE_TEMPLATES` row 「〜ていない（不在の残り）」, `$`-anchored, with `FINAL_TEMPLATE_CAPS = 1`. **Corpus run as committed: zero ids move** — the founding pair was repaired before commit, so 20260907_1 measures 1 and passes on merit; 20260828_2 and 20260903_1 at 1; 31 papers and ALL TEN official sittings at 0. The row comment records both the founding-revision run (×2, FIRES) and the as-committed run |
| **NEW-2** `GATE-WRONG`, minor | **APPLIED** | correlation row widened from inflected forms to stems (`多\|少な\|大き\|…\|なってい`), so it stops going blind on the です・ます passages `dokkai.md` Axis 3 mandates. Corpus effect re-measured: nothing reaches 3, **zero ids move** |
| **concurrency** `PIPELINE-GAP` | **APPLIED** | `jlpt-test-generation` §"The 5-stage pipeline" now carries *one writer per test folder, at a time*: a QA pass records the source shas it read, and a build or repair that finds them moved re-runs the pass |
| **NEW-1** `RULE-MISSING` | **APPLIED** | `jlpt-test-generation` §"One topic, one surface" gains a rhetorical-MOVE column read across BOTH halves, cap 2, with the 読解 side always the one re-angled (the 聴解 item is lifted from a real sitting) |
| **round-1 F11** `RULE-UNENFORCEABLE` | **REJECTED, with the measurement** | see below |

## Why the F11 row is rejected as proposed

Proposal: convert `pools.json`'s `usage`/`context_words`/`paraphrase` entries to
`{"w": …, "src": "<book> p.<n>"}` and add `check_pool_band_source()` FAILing any
drawn 問題1–6 item whose entry has no `src`.

**Measured before deciding** — every pool headword grepped against all four
tracked extracts (`Shinkanzen/goi_reference.md`, `Shinkanzen/kanji_tables.md`,
`Soumatome/goi_reference.md`, `Hajimete/vocab_reference.md`):

```
usage           115/217  sourced (53%)
context_words   905/1380 sourced (66%)
paraphrase       81/143  sourced (57%)
kanji_reading   892/1526 sourced (58%)
```

The unsourced residue is not a band problem. It is 妥協, 発揮, 解消, 措置, 促す,
焦る, 把握 — words no one would dispute are in those volumes. **The extracts are
OCR** (AGENTS.md §3 says so in the same breath as "secondary evidence"), and a
`src` derived from grepping them would record OCR coverage while claiming to
record book authority. Shipping `check_pool_band_source()` on that basis would
FAIL roughly 40 % of every future draw for a reason that has nothing to do with
the item's band — and filling the gaps by hand from memory is precisely the
invented-number defect class AGENTS.md §3.2 and REPORT-GOI.md §F10 forbid.

**What would make it applicable** (not done here, and not blocking): page-level
`src` has to come from the PDFs themselves, which are on the `refs` release and
three of the four are over the 100 MB read cap — a sourcing project of its own,
with `--split-pdf`, not a side effect of a generation run. Until then the
re-litigation cost the row names is real but cheaper than a gate that fails
honest items.

---

# Part 2 — dispositions on `qa/qa-report-20260909_1.md` (this paper's own QA)

Round 1 returned `QA: FAIL (5 findings, 1 automatic)` on a 100/101 blind solve.
All five are repaired; the two skill findings are dispositioned below.

| id | disposition | what was done |
|---|---|---|
| **F1** (automatic fail) | **FIXED at the root** | A figure item printed as 「1. 1 / 2. 2 / 3. 3 / 4. 4」. Official 問題1 occasionally prints a picture and asks which REGION to act on; the composed booklet embeds no image, so the item was unanswerable. `build_choukai_bank.py` now sets `figure_dependent` (detected from the digits-only option set, the invariant — stem phrasings vary), and `compose_choukai.py` refuses to draw such a clip and PRINTS the exclusion. 2 of 402 records, so no 大問 loses candidates. Re-composed on the SAME seed; only 問題1-2 moved |
| **F2** | **FIXED** | 問題3-13's stem contained the key morpheme. Stem re-written around the same drawn 接頭語 target; the rest of 問題3–6 re-scanned, 0 further hits |
| **F3** | **FIXED** | 問題9 and 問題13 both closed on 「〜ておきたい」. 問題13 re-closed (chosen because its final is quoted by one item, where 問題9's is load-bearing for blank 51). Shape tally byte-identical |
| **F4** | **FIXED at the root** | `compose_choukai.py`'s least-used-first objective is GLOBAL and says nothing about slots, so a slot whose candidates were tied could take the same clip two papers running — **18 of 24 transitions did**. It now bars the previous paper's clip per slot, dropping the bar and printing a note only if that would starve the slot. This paper: **0** same-slot repeats against `20260907_1`. The whole-paper pass's "confirm no clip id repeats the previous paper in the same slot" was a verification of a condition the machinery never established; now it is established |
| **F5** | **FIXED, gate-side and paper-side** | `exam-qa-review` has required THREE fields on a re-authored record since 2026-09-04 and forbids resolving a gap by dropping one; the gate read only the note's presence. Measured: **53 of 53 entries across 19 papers had no `shipped_surface` — 100 %.** New `check_reauthored_shipped_surface()` FAILs it, with the 18 pre-rule papers exempt BY NAME (not retrofitted — writing 53 fields from prose nobody can re-verify manufactures machine-readable data out of a guess). This paper's two entries now carry it in both files |
| **S3** | **CORRECTED, narrower than filed** | QA read rule 3's "listening caps at ≤5 scenarios per theme" as broken by 23 of 25 papers. Re-measured and it reproduces — but the cap governs the **DRAW**, where the sampler and `check_spec_blend` both enforce it and every paper on disk holds (this one drew max 4). The 23/25 measures **shipped composed** themes the cap never governed, and 働き方 is the offender in **24 of 25** because 聴解問題4's eleven quick-response items are workplace exchanges by FORMAT. So the gate was right and the RULE'S WORDING was wrong; rule 3 now says the cap is draw-only and that a composed paper's shipped listening themes are a DRAW audit. No check changed — a correct check should not be edited to match a mis-stated rule |

## Open, DEFERRED with a measured reason — blocks the next generation run

**A composed paper draws 32 pool entries it never spends.** Every paper draws
21 `listening_scenarios` and 11 `quick_response` entries, and since the
2026-09-08 rework a composed 聴解 half authors **no surface from any of them** —
the items are clips lifted from real sittings. Both Stage 3 and QA found this
independently. Measured: 25 papers × (21 + 11) = **525 + 275 entries consumed**
by draws that shipped nothing, and rule 3's ≤5 listening draw cap is computed
over scenarios no paper uses.

**Why it is deferred rather than fixed here:** the repair is to stop drawing
those two categories for composed papers, which changes the shape of
`test_spec.json` — a blueprint-level contract that `check_spec_blend`,
`check_draw_provenance`, `check_surface_subjects`, the errand-coverage skips and
the theme-cap line all read. That is a `sample_items.py` change with a corpus-wide
blast radius, and doing it at the tail of a generation run, after the paper is
built and QA'd, is how a green gate stops meaning anything.

**Why it is safe to defer:** the harm is confined to bookkeeping for two
categories that no longer feed any authored surface. The pools that decide what
the paper actually TESTS — grammar, vocabulary, kanji, and `reading_topics` —
are untouched and rotate correctly.

Per `jlpt-test-generation` §"The fix loop", this row must be **applied or
explicitly rejected before the next `make sample`**.

---

# Part 3 — round 2, and what closed the paper

Round 2 returned `QA: FAIL (3 findings, 1 automatic)` on a **101/101** blind solve.
Round 2 is the fix-loop cap, so its findings were applied DIRECTLY
(`jlpt-test-generation`: "if round 2 still FAILs, apply its findings directly and
say explicitly which were fixed without independent re-verification").

| id | disposition | independently re-verified? |
|---|---|---|
| **R2-F3** — 聴解問題1 keyed 3,4,3,3,3 and 問題3 keyed 4,1,1,1,1 | **FIXED at the root.** `key_spread()` pooled 問題1/2/3/5 into one 19-key bucket, so a section could be a monoculture while the pooled distribution looked flat (penalty ≈0.16). Now scored per section. Baseline **re-measured by the orchestrator, not quoted**: across 30 official 4-option sections the modal key is 2 in 22 and 3 in 8 — **never 4**. 問題4 checked separately (official runs 4–5) and correctly excluded | **Yes** — measured on the shipped bytes: 問題1 mode 2 / 問題2 2 / 問題3 2 / 問題5 1 |
| **R2-F2** — 問題11(4) ↔ a 聴解 item on one subject, filed as an automatic fail | **OVERTURNED as a false positive**, by an independent adjudicator, then the stale rule that produced it was fixed. See below | **Yes** — separate context, adversarially briefed |
| **R2-F1** — `logs/topics.json` described a superseded listening half | **FIXED.** 116 fields re-derived from the shipped bytes | **Partly** — the gate's own 「…」-span check went from FAIL to `ok` (57 spans), which is machine verification of the load-bearing part; no fresh-eyes context re-read the prose |
| **NEW: 聴解問題4-6 ↔ 4-7** — one name, one errand, adjacent slots, both keyed 3 | **FIXED at the root** with a calibrated name-clash penalty. Two candidate predicates were MEASURED AND REFUTED first: script similarity scores the pair at 0.254, *below* the officials' own within-大問 max of 0.310; and a hard name ban fires on official 2025-07 (問題2-4/2-5 both name 山田). So it is a PENALTY and labelled a proxy — errand identity is not string-decidable | **Yes** — 0 within-大問 name clashes on the shipped bytes |
| **NEW: a three-way rhetorical-move overlap** (問題10(3) + 問題11(2) + 問題11(4)), cap 2 | **FIXED.** 問題11(2) re-authored. Found independently by TWO contexts, which is why it was treated as real rather than marginal | **Yes** — a bounded blind-solve of items 59/60 by a fresh context: keys matched, no second defensible answer, and the keyed options have the SHORTEST passage overlap on the surface (5 chars) while distractors hold the longest |

## The false automatic fail, and the documentation defect behind it

Round 2 filed 問題11(4) (authored: who managed to walk home when the trains
stopped) against 聴解問題4-6番 (a lifted one-line 即時応答, 「電車の事故で、昨日は
会社から歩いて帰ったんだ。」) citing `exam-qa-review` §5: *"Fail on: any subject
twice in this paper (any register)."*

**Adjudicated `legitimate`.** Only a domain is shared: the 読解 keys turn on
having pre-decided a rest stop, the 聴解 key turns on choosing a sympathetic
register, no number or condition crosses, and a solver gains nothing in either
direction. `jlpt-test-generation` §"One topic, one surface" — the OWNER — says
a 読解 passage may share a DOMAIN with a 聴解 item and that only a shared
**decisive detail** is a finding.

**Three clauses of `exam-qa-review` §5 were retired by the owner on 2026-09-08
and never updated here**, which is what made the false filing reachable as an
*automatic* fail: *two 聴解 items running the same errand*, *問題14-vs-聴解 detail
overlap*, and the 読解-vs-聴解 half of *any subject twice*. §5 and the
automatic-fail list are now scoped to AUTHORED surfaces and point at the owner
instead of restating it. The adjudicator also found a contradiction INSIDE the
owner — its line 248 retired 問題14-vs-聴解 overlap while line 258 kept
decisive-detail overlap as a finding, and 問題14 is authored and CAN be
re-angled — so 問題14 was removed from that retired list.

Also corrected in the owner: it justified the per-slot clip check as "the
composer already spends least-used clips first, so this is a verification, not a
repair." That was **false**, and F4 is the measurement that disproves it.

## Open, DEFERRED — carried into the next run

1. **32 unspent draws per composed paper** (Part 2). Unchanged: must be applied
   or rejected before the next `make sample`.
2. **NEW — the 2024-12 sitting's Vietnamese explanations are bare in the clip
   bank.** All **29** of its banked clips give the keyed option the reason
   `"Đúng."` and nothing else, which `exam-model-answer` prohibits in both panes.
   Any future paper drawing a 2024-12 clip inherits it. **This paper is clean**
   (0 bare or under-12-character option reasons in either pane — the three that
   landed here were repaired, and the fix belongs at source in
   `tests/imported-n2-2024-12/詳細解説.vi.json` + a bank rebuild, which is a
   different test's deliverable and not this run's scope).
3. **A bank-supplied 聴解 explanation misdescribed its own recording** —
   `2024-12:問題2-3` called 山下選手 "anh" where the shipped script gives her as
   `女:`. Repaired in this paper's pane; the bank source still carries it, same
   disposition as (2).
