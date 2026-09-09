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
