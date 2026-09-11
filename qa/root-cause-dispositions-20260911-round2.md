# Root-cause dispositions — `qa/qa-report-20260911_1-round2.md` (`QA: PASS`)

`jlpt-test-generation` §"The fix loop" and `AGENTS.md` §0: a PASS closes the
PAPER, not the GENERATOR. An open row in a QA root-cause table blocks the next
generation run until applied or **explicitly rejected with a reason**. Round 2
returned PASS with three non-blocking findings; this file disposes of all three.
Written 2026-09-11 by the 20260911_1 orchestrator. The report is a RECORD and
was not edited.

Round 1's five rows were all applied during this run (F1–F5 in the paper, and
the systemic half in `tools/check_consistency.py`, `dokkai.md`,
`jlpt-test-generation/SKILL.md` and `exam-qa-review/SKILL.md`, each with a
founding-case run recorded by the context that applied it).

## NEW-3 — APPLIED

`tools/lint_draft.py`'s DOKKAI-MARKER scan read the whole file, 解答と解説 key
table included, so 問題6-28's sense-numbered 解説 cell (暗い＝①…②…③…) was
reported as two unreferenced passage markers on a compliant paper. The scan is
now bounded to the booklet body, using the same first-解答-heading boundary
`check_consistency.py` and the sheet builder use.

**Founding-case run:** `make lint-draft 20260911_1` went from two DOKKAI-MARKER
WARNs to `ALL CHECKS CLEAN`. **Negative control, because removing a WARN is not
the same as fixing it:** the body's own ① still resolves 1-to-1 against stem 68,
the excluded set is exactly `{②, ③}` (the 解説 cell), and an ④ planted in the
body with no stem reference still fires. A WARN that fires on a correct paper
trains the reader to scroll past the ones that do not — that is the whole reason
this was worth fixing rather than annotating.

## NEW-2 — APPLIED (report-level), with the class named

Round 1 resolved 問題4-19's option-set WARN by citing 恩 as attested "Soumatome
×2, Hajimete ×8, official ×3". Round 2 re-measured: **every one of those hits is
OCR noise** (感恩的／意恩／志恩／目恩品／買い恩), and 恩 appears 0 times in all 31
official booklets. The item is still sound on judgement — 恩 is 常用漢字, 小6
配当, and 「大きな恩を受ける」 is standard adult vocabulary — so **the paper does
not move**; what was wrong was the evidence.

The disposition is the rule, not the number: `refs/`'s `*_reference.md` and
`vocab_reference.md` are **OCR, not an index**. Round 1 wrote that absence is not
evidence of absence and then fell into the same trap in the opposite direction —
treating a raw grep count as evidence of PRESENCE. This is the third instance of
the class (REPORT-GOI §F10, round 1's own §S1, now this). The one-sentence rule
goes to `exam-qa-review` §2.5 and `moji-goi.md` Part 0: **quote the hit line, do
not count it** — a band claim citing a grep total with no line read is not a
measurement. Queued with NEW-1's doc edits below.

## NEW-1 — SPLIT: authority + gate APPLIED, fleet re-render REJECTED as a rider

**The defect, verified here rather than quoted:** every `聴解スクリプト.txt` on
disk opens 「**Nに聴解。これから、Nにの聴解試験を始めます。**」 — `N2` with only
the `2` transliterated into kana, leaving a non-sentence no announcer would say.
**37 of 37 papers** carry it (27 generated + 10 imported), and it is written as
the canonical string in `jlpt-exam-structure/SKILL.md:236` and
`choukai-audio/SKILL.md:298`. The official script PDFs do not print this
preamble at all, so those two files are its ONLY authority — which is exactly how
one typo reached every paper in the repo.

**Not a shipping blocker, and round 2 is right about why:** the line does not
reach the candidate. It appears in no `練習.html`, no `聴解.html`, no
`詳細解説.json` — unlike item dialogue, which does. And `exam-qa-review` §4
check 6 explicitly forbids repairing a drawn clip's text inside the paper that
drew it.

**APPLIED now** (the authority, so the next paper is born correct, plus the
detector):
- (a) the canonical string in both skills → 「N2聴解。これから、N2の聴解試験を
  始めます。問題用紙にメモをとってもかまいません。」
- (c) `check_choukai_script_latin()`, shipped **WARN**: a Latin run in
  `聴解スクリプト.txt` that is not a source-borne proper noun. It must fire on
  the `N` of 「Nに聴解」 and pass `IT` (山川IT専門学校) and `Web` (Webデザイン),
  which come from official bank records. **FAIL is not available to it while 37
  papers fire** — a gate line that reds the whole fleet is the defect class §6.5
  names, and lowering the fleet to green by weakening the predicate is worse.
- (d) the `exam-qa-review` §4 check-6 line: section preambles and the opening
  announcement ARE drawn clips, they are the one piece of script text that
  cannot be checked against the archive because the archive never printed it,
  and they are therefore the place a repo-authored typo survives indefinitely.
- (b-partial) the 10 imported papers' first line + `make choukai-bank`, so the
  bank records the corrected preamble and the NEXT composed paper gets it. **The
  bank, not the skill, is what a composed paper actually reads** — correcting the
  docs alone would have fixed nothing.

**REJECTED as a rider on this run:** re-rendering the **26 other generated
papers** (`--replay --no-audio` + `make sheet` + `make model-answer` each).
Reason, and it is the same one `qa/root-cause-dispositions-20260910.md` gave the
`listening_scenarios` row, which this run inherited and honoured: a 26-paper
mechanical rewrite at the tail of a generation run produces a diff nobody reads,
on papers this run never touched, to fix a string no candidate sees. The
20260909 deferral's phrasing is the precise objection — *doing it at the tail of
a generation run is how a green gate stops meaning anything.*

**Re-filed as a standalone task:** *"re-render the 26 generated papers' 聴解
scripts onto the corrected preamble"* — its own change, its own review, with the
new WARN as its progress meter (it goes to zero when the task is done). **The
next generation run inherits this rejection, not the row.** Trigger to do it
sooner: any paper whose preamble reaches a learner-visible artifact, which would
make it a content defect rather than a source-text one.

**This paper (`20260911_1`) is re-rendered as part of (b)** — it is the paper
under production, its bank records are being rebuilt anyway, and shipping the
run's own deliverable with a known non-sentence in it while correcting the rule
that produced it is not defensible.
