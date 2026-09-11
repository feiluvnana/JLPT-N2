# Root-cause dispositions — entering the 20260911_1 run

`jlpt-test-generation` §"The fix loop": an open row in a QA root-cause table
**blocks the next generation run until applied or explicitly rejected with a
reason.** This file is that disposition for every row in
`qa/qa-report-20260910_1-round2.md` §5. Written 2026-09-11 by the 20260911_1
orchestrator, **before `make sample`**. The report itself is a RECORD and was
not edited.

Each row's status below was **checked on disk, not read off the commit
message.**

## Verified already applied by the 20260910_1 run — no action

| row | evidence checked here |
|---|---|
| **F1(b)** doc: a declaration records the page it was typed from | `.agents/choukai-audio/SKILL.md:183` lists `source_page` in the hand-declaration procedure; `textbook_items.json` carries the field on its records |
| **F3** `GATE-WRONG` — 問題8 stem captured as a first line | `check_mondai8_dialogue_layout()` exists at `tools/check_consistency.py:1614` with the span capture and the grandfather set carrying the evidence |
| **S1** the rhetorical-MOVE cap names no move vocabulary | `.agents/jlpt-test-generation/SKILL.md` §"One topic, one surface" now carries the SKELETON paragraph, the 問題12(A)+(B)-as-one-surface rule and the 0–3 official band |
| **S2** `check_dokkai_belief_denial_monotony()` missing | present in `tools/check_consistency.py:2908` |

## Applied by this run, before `make sample`

**F1(a) — `check_textbook_script_grammaticality()`, APPLIED as a WARN.**
`tools/check_consistency.py`, called from the 聴解 bank block. A hand-declared
clip's TEXT is verified by nothing: the bank builder guards duration and char
rate, and `check_choukai_*` compares the script to the composed MP3's
segmentation. Neither reads the Japanese.

*The predicate is not the one the finding specified, and the difference was
measured, not argued.* The finding proposed "a `〜て` gerund immediately
followed by 言っ with no と/って between". That predicate cannot exist as
written: 「持って言った」 (wrong) and 「持つって言った」 (right) are the same
characters in the region it inspects, so no matching on っ/て/と separates them.
What DOES separate them is what sits before って — a quotative って attaches to a
plain form, so the correct text leaves a word tail there (「教室って言っても」),
and the mis-typed gerund leaves a BARE kanji stem (「持って言った」). The shipped
predicate is therefore a single kanji, not itself preceded by a kanji, run
straight into って言.

*Founding-case run, as the finding required.* Over the pre-repair
`textbook_items.json` (`git show 467bf5a^`) it fires on exactly
`kanzenmoshi:cd1-27` 「だから持って言ったじゃない。」 and nothing else; over the
repaired file (85 declared items) it is silent; over the whole bank's 82,193
characters of official script it is silent, where the looser `[kanji]って言`
fires 4 times, all legitimate nouns (2021-07 問題2-3, 2023-12 問題1-2, 2024-07
問題2-4, 2025-12 問題4-7).

*WARN, not FAIL, and the reason is in the docstring:* a single-kanji NOUN plus a
quotative って (「今って言われても」) is grammatical and would fire. The line
carries one signature; it does not claim to read Japanese.

**F1(c) — `exam-qa-review` §4 composed-paper check 6, APPLIED.** "Read every
hand-declared (non-`official`) clip's script aloud" — with the founding case,
and with what the new gate line does and does not cover. The block header now
says six checks and the re-composition clause covers 1–6.

## Rejected as a rider on this run, re-filed standalone

**F2 — pool vocabulary provenance** (`source` field on every
`kanji_reading`/`context_words`/`paraphrase`/`usage` entry,
`check_pool_vocab_provenance()`, and a backfill that deletes every entry
resolving to none of the four authorities).

**The defect is real and I am not disputing it.** Re-measured here rather than
quoted: `pools.json`'s `context_words` is a list of bare strings
(`["難航", "発足", …]`) with no provenance field, so nothing can assert a drawn
key is attested in Shin Kanzen, Soumatome, はじめての or the 31-sitting archive,
and 初霜 reached a shipped 問題4 key that way.

**Rejected as a rider, for the same decisive reason
`qa/root-cause-dispositions-20260910.md` gave the `listening_scenarios` row, and
it applies with more force here:** this is a change to `pools.json` and to the
sampler's inputs **immediately before `make sample`**, which would make this
paper the first output of an unverified blueprint. The backfill is not a
mechanical edit either — it is a per-entry lookup against four OCR extracts plus
31 sittings, and its failure mode is deletion of a legitimate entry, i.e. a
silently narrowed pool. That is a blueprint-level defect bought to close a
bookkeeping one.

**Harm while it is unbuilt, bounded and stated:** the exposure is a 問題1–6 key
that no authority attests. It is not unguarded in this run — `question-authoring`
requires per-key verification against the authorities at authoring time, and
stage 4's blind solve re-reads every key. That is a human check where F2 asks
for a machine one, which is exactly why F2 should be built; it is not nothing.

**Re-filed as a standalone task:** *"give `pools.json`'s four vocabulary
categories a `source` field, add `check_pool_vocab_provenance()` as a coverage
WARN, and backfill by scanning the four extracts + `refs/JLPT_N2_NEW/*/booklet.md`"*
— its own change, its own review, a corpus re-run over all 36 papers. **The next
generation run inherits this rejection, not the row.** Trigger to build it
before the next paper: a second off-band 問題1–6 key found by QA on any paper.

## Carried, unchanged, from 2026-09-10

1. *"A composed paper draws 32 pool entries it never spends"* — rejected as a
   rider on 2026-09-10 and **decided**, not re-deferred. This run inherits the
   rejection. Its stated trigger is a `draw()` relaxation note on
   `listening_scenarios` or `quick_response`; stage 1 must report whether one
   printed.
2. The two `tests/imported-n2-2024-12/` bank-source defects (all 29 clips give
   the keyed option the Vietnamese reason `"Đúng."`; `2024-12:問題2-3` calls
   山下選手 "anh"). A different test's deliverable; any paper drawing a 2024-12
   clip inherits them, so stage 5's Vietnamese author must not copy a banked
   `"Đúng."` line.
