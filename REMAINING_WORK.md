# remaining_work.md

Handoff note, 2026-08-05. Written after a consistency audit of the 14 skills +
`AGENTS.md` + the pipeline scripts, and after applying the doc/code fixes from
that audit. **Nothing is committed** — the working tree has 17 modified files
(see §0). This file lists only what is still OPEN.

Everything here was verified against the repo as it stands; where a claim needed
evidence, the command that produced it is included so a fresh context can
re-check in seconds instead of trusting this file.

---

## 0. State of the working tree

Modified, uncommitted:

```
.agents/choukai-mp3-generation/SKILL.md          .agents/question-authoring/SKILL.md
.agents/choukai-script-writing/SKILL.md          .agents/reference-book-reading/SKILL.md
.agents/exam-answer-grading/SKILL.md             .agents/web-topic-research/SKILL.md
.agents/exam-qa-review/SKILL.md                  .agents/web-topic-research/scripts/merge_seeds.py
.agents/external-test-import/SKILL.md            .agents/item-pool-sampling/SKILL.md
.agents/external-test-import/scripts/extract_pdf_text.py
.agents/item-pool-sampling/scripts/sample_items.py
.agents/jlpt-exam-structure/SKILL.md             AGENTS.md
.agents/official-audio-analysis/SKILL.md         Makefile
                                                 tools/check_consistency.py
```

Deleted earlier (untracked, never committed):
`.agents/jlpt-exam-structure/references/guidebook_s_j.pdf` — the 2009 概要版. Its
usable content was folded into `jlpt-exam-structure` (認定の目安, the list of rows
where the guidebook's 目安 disagrees with real papers), so nothing needs it back.

No test content, no `logs/`, and no generated deliverable was touched.

---

## 1. `make check` is RED — one line, on purpose. **Decision needed.**

```
FAILED — 1 problem(s):
  - no two tests share both a --seed and a web harvest: seed 20260804 shared by
    tests ['2', '3'], and ['2'] record no harvest_sha (unrecorded ≠ different)
```

This is the intended effect of tightening `check_rotation_inputs()`
(`tools/check_consistency.py`, "unrecorded ≠ different"). Tests 2 and 3 really do
share seed 20260804, and test 3 really did ship as a re-skin of test 2; the check
passed them for months only because test 2 predates the `harvest_sha` stamp and
`None` counted as "a different harvest".

```bash
python3 -c "import json;[print(e.get('test_id'),e.get('seed'),e.get('harvest_sha')) for e in json.load(open('logs/ledger.json'))['history']]"
```

Pick one:

- **(a) Accept red** as a truthful record until tests 2/3 are regenerated. Cheap,
  but every future `make check` reports a failure, which erodes the gate's
  signal (`AGENTS.md` §0.5 says green is the floor).
- **(b) Regenerate test 3** with a fresh seed and a fresh harvest. Fixes the
  underlying defect, costs a full generation cycle (7+ passes).
- **(c) Retire test 2 or 3** (move out of `tests/`, drop its ledger entry).
- **(d) Do NOT** hand-write a `harvest_sha`. It restores green and re-blinds the
  exact check that was just fixed.

Until this is settled, use `make check-tests` for per-test work — it passes
fully, because the rotation check lives in the doc/code half of the gate.

---

## 2. Test instruction wording drifts from the official booklets. **Own pass.**

`jlpt-exam-structure` now carries the canonical 問題N instruction lines
(§"問題N instruction lines", transcribed from `refs/JLPT/16. N2 07-2025.pdf`).
The tests on disk do not match them:

| Test(s) | Drift | Official |
|---|---|---|
| 1, `imported-n2-2025-07` | 問題2: 「問題用紙の**せんたくしを読んで**ください」 | 「問題用紙を**見て**ください」 |
| all 5 | 問題5: 「メモをとってもかまいません」 | 「**問題用紙に**メモをとってもかまいません」 |
| 4 | 「選び**なさい**」 (聴解), 「質問と**選択肢**」, 問題4 missing 「まず…それから」 | 「選んでください」, 「質問とせんたくしを」, 「まず文を聞いてください。それから…」 |
| 4 | 問題5 headings use `**1番**` | `## 1番` (as tests 1–3 and the import) |

`imported-n2-2025-07` is the serious one: an import must be verbatim, so this is
a fidelity bug, not a style choice.

Why it is not fixed here: `make check` requires each booklet `問題Nでは、…` line to
appear in the script verbatim, so **both files must change together**, which
invalidates the MP3. Full sequence per test:

```bash
# edit tests/<id>/聴解.md AND tests/<id>/聴解スクリプト.txt to the canonical text
make mp3 <id>        # network TTS, ~1 min; rewrites 聴解.mp3 + 聴解_チャプター.json
make booklet <id> && make sheet <id>
make check
```

Then a fresh-eyes review of the touched items per `AGENTS.md` §6 (fix pass +
re-review pass). Note `make check` compares booklet↔script only — it will never
tell you whether either matches the official wording, so diff against the
canonical table by hand.

---

## 3. `logs/ledger.json` data integrity. **Decision needed.**

- Two entries carry `test_id: 4`. The 2026-08-03 one (seed 20260803, harvest
  `legacy0803sh`) belongs to the **removed** first test 4 (removed in 9a794d5,
  last at b9b90de). Attribution for test 4 is therefore ambiguous, and
  `merge_seeds.unblend()` restores from whichever entry it iterates last.
- `tests/1` has no draw of its own: its items sit in the synthetic `"legacy"`
  entry (seed `null`) from the v1→v2 migration.

Left untouched deliberately: rewriting history changes the LRU cooldown window
for every future draw. If you do clean it, the least invasive edit is to rename
the removed test's `test_id` to something inert (e.g. `"4-removed"`) rather than
deleting the entry, so its items stay in the cooldown history.

---

## 4. `logs/test_spec.json` predates the current `DRAW`

The live spec (test 4) has **11 reading topics / 20 listening scenarios**; the
sampler now draws **12 / 21**.

```bash
python3 -c "import json;i=json.load(open('logs/test_spec.json'))['items'];print(len(i['reading_topics']),len(i['listening_scenarios']))"
```

Nothing to fix now — `check_answer_positions` zips over the questions that exist,
so the extra prescribed entries are inert, and re-sampling for an already-authored
test would rewrite the contract its 101 keys were placed against and turn the gate
red. **Just don't be surprised at the next `make sample`**: the new spec will have
one more reading topic and one more listening scenario (the fix for a long-standing
off-by-two where 問題5's two items got no sampled scenario). Documented in
`item-pool-sampling` §1.

---

## 5. Optional hardening, each with a real cost

- **Gate the instruction texts.** A check comparing each test's `問題Nでは、…`
  lines against the canonical table in `jlpt-exam-structure` would catch §2
  automatically. It will flag all five tests until §2 is done, so land §2 first
  or add it as a WARN.
- **Close the 例 answer-pause deviation.** `pause_after()` appends `ANSWER_PAUSE`
  after every item block including 例; the official recording goes straight from
  the 例 into the 「最もよいものは◯番です…」 confirmation. Our MP3s therefore have
  13 × 12 s / 18 × 8 s where official has 12 / 17. Fixing it means skipping the
  pause for `例。` blocks and regenerating every MP3 (and updating the dry-run
  table in `choukai-mp3-generation`, which `make check` asserts against the code).
  Documented as a known deviation in both audio skills; cosmetic, not a defect.
- **Align the 大問 rating bands** with the official 参考情報 (A ≥67% / B 34–67% /
  C <34%, 文字・語彙 and 文法 only). Currently 優 ≥80 / 良 60–79 / 要強化 <60 per
  大問, documented in `exam-answer-grading` §4 as a deliberate repo-internal
  diagnostic. If you change it, change both graders plus the `make check` parity
  test together.

---

## 6. Pre-existing WARNs, still unresolved

```
1: 読解 has substantial （注N） glosses (official July 2025 ≈50+; got 14)
4: 読解 has substantial （注N） glosses (official July 2025 ≈50+; got 10)
```

Real under-annotation, not false positives — the July 2025 booklet carries 60
`（注N）` and 3 `（中略）` (`pdfminer` over `refs/JLPT/16. N2 07-2025.pdf`).
Tests 2 and 3 clear the ≥15 threshold. Adding glosses is content work: edit
`言語知識・読解.md`, then `make booklet <id> && make sheet <id>`, then QA the
touched passages. `AGENTS.md` §0.5 requires each WARN to be resolved or
explicitly justified in a final report, so leaving them silently is not an option.

---

## 7. Reference provenance to confirm (low confidence, cheap to check)

`refs/JLPT/16. N2-7.2025 (script).pdf` and `refs/JLPT/16. N2 07-2025.pdf` are
labelled July 2025, but the script PDF's page headers read **「JLPT・N2・12/2024」**
— the same watermark as `15. script N2 12.2024.pdf`, whose content differs, so
they are distinct papers and the watermark is probably a vendor template artifact.

```bash
python3 -c "import re,sys;from pdfminer.high_level import extract_text;t=re.sub(r'\(cid:\d+\)','',extract_text(sys.argv[1]));print(sorted(set(re.findall(r'JLPT・N2・\d+/\d+',t))))" "refs/JLPT/16. N2-7.2025 (script).pdf"
```

It matters because `jlpt-exam-structure`, `question-authoring`,
`reference-book-reading`, and `exam-qa-review` all cite
`tests/imported-n2-2025-07` as the **July 2025** calibration snapshot (問題13
≈1050 JP chars, ≈50+ 注, 4×2 問題11). The measurements hold regardless; only the
date label is in question. Confirm against the booklet cover page and either
leave it or rename the import.

---

## 8. Environment gap

`poppler` is not installed, so every command in `reference-book-reading` steps
1–2 (`pdfinfo`, `pdffonts`, `pdftotext`, `pdftoppm`) fails, and the harness
cannot rasterize PDF pages — which is the documented strategy for the scanned
Shin Kanzen books in `refs/Shinkanzen/`.

```bash
which pdfinfo || brew install poppler
```

The text-layer path (`extract_pdf_text.py`, now with a pdfminer fallback for
CID-keyed fonts) covers everything in `refs/JLPT/`, but TOC calibration against
the scanned textbooks needs poppler.

---

## 9. How to verify the current state quickly

```bash
make check-tests   # expect: all pass, 5 skipped, 2 注-count warnings (§6)
make check         # expect: the single rotation failure in §1, nothing else
python3 -m py_compile tools/check_consistency.py \
  .agents/web-topic-research/scripts/merge_seeds.py \
  .agents/item-pool-sampling/scripts/sample_items.py \
  .agents/external-test-import/scripts/extract_pdf_text.py
python3 .agents/item-pool-sampling/scripts/sample_items.py --check-depth   # read-only
```

Audit facts worth keeping (all re-measured, not inherited):

- Official Dec 2025 audio = 51.4 min; long-silence histogram 7 × 20 s,
  12 × 12 s, 17 × 8 s, ~42 × 3 s. Because official gives an answer pause after
  **scored items only**, that decomposes to 問題1=5, 問題2=6, 問題3=5,
  **問題4=11**, 問題5=3 answers (1番 + 2番's 質問1/質問2) = 30. Both recent
  scripts confirm 1番–11番 and no 問題5 3番.
- Generated scripts: 43–46 blocks (tests 1–4: 46, 44, 43, 43; import 46);
  MP3s 41.1–46.7 min.
- July 2025 booklet: 71 questions, 問題11 body has passages (1)–(4) while the
  instruction prints `(1)から(3)`, 60 `（注N）`, 3 `（中略）`.
