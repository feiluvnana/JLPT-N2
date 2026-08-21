# 読解 remediation — run report

Plan: `REPORT-DOKKAI.md` §"Remediation plan" (`plan_sha` 4e64cad44436).
State: `logs/dokkai_remediation_state.json`. Required by Phase R and
`AGENTS.md` §0.7.

---

## Run 2 — 2026-08-21: audit the first pass, then repair what it skipped

Run 1 (commit `b41bcb9`) reported the plan as implemented. This run re-derived
every claim by measuring the artifact instead of trusting the report. The
pipeline half had largely landed — and the part of it that owns every number,
`tools/dokkai_profile.py`, was measuring the archive wrong, which is worse than
not having it: the docs and the gate carried the audit's figures while the
committed script printed different ones, so D1's whole purpose was unmet.

### Skills read in full

`AGENTS.md` §0, `question-authoring/references/dokkai.md`,
`question-authoring/references/official_calibration.md`, `exam-blueprint/SKILL.md`,
`exam-qa-review/SKILL.md`, `jlpt-exam-structure/SKILL.md`, plus `REPORT-DOKKAI.md`
end to end.

### What the audit found

| # | Finding | Class |
|---|---|---|
| B1 | **`dokkai_profile.py`'s official parse was broken four ways.** Section starts took the LAST 「問題N」 mention on the page, so 7/2023 measured 問題10 at **0 chars**. Passage markers had to own their line, so 「(2) 以下は、…メールである。」 dropped every passage of its section. Item boundaries were any two-digit line, so 「14 時〜16 時」 cut the 問題14 flyer and two sittings measured a **26-char** 情報検索 section. Options were hunted in a joined string, so the 「3」 of 「3月19日」 read as option 3 and four options collapsed into two fragments plus a 698-char blob. | measurement wrong |
| B2 | **Stems were cut at their first line**, and in official 問題14 the QUESTION is usually the second one — so **all 14 official items classified as `other`** and the corpus that F4's rule is measured against looked as if it asked nothing. The 問題10–13 stem-bucket histograms (F6, F9) read the same truncated text. | measurement wrong |
| B3 | `classify_q14_target`'s families were too narrow besides: 「なければならない」 without か, 「しかた/方法」, and any noun before 「はどれか」 (including katakana) all fell through. Four generated papers' **named-choice** stems were being counted as generic truth-checks. | measurement wrong |
| B4 | Three checks shipped as **WARN-only where the plan specifies a FAIL edge** — rules that can never block and have no queue behind them: 問題14 stem target, span rate, 問題10 form mix. | gate too weak |
| B5 | The option-length **FAIL at 2.50 rejects official items**: 問題14's own range is 1.26–4.17 because its options are values and dates (12/2023 問70 prints 「3,500円」 beside a 25-character option). One threshold cannot serve 問題14 and 問題10–13 (1.03–2.00). | threshold vs archive |
| B6 | The top-overlap **WARN at 44% flags an official sitting** (45.0% under the repaired parser) — set at 44% precisely because it failed no official paper, on numbers that have since moved. | threshold vs archive |
| B7 | **Phase 2.3 was not done at all**: `exam-blueprint`'s theme table had no voice axis, so F3's quota — the finding with no overlap at all between the two corpora — had nowhere to live. | not done |
| B8 | Phase 2.4's blind-**strategy** pass was missing from `exam-qa-review` step 0 (the 問題14 named finding was there). Without it, F1/F2 are invisible to a human pass on a single paper. | not done |
| B9 | No dokkai slug was declared in `FINDING_REPAIR`, so `make findings` and `make repair-plan` saw only the 聴解 half. | not done |
| B10 | Phase R state file and this report did not exist. | not done |

**Genuinely done in run 1**, each re-verified here: the ≤1.30 clamp's
replacement by 1.65/2.50 (D2), the banned-retrieval scope fix over 問題10–14 plus
the three live breaches it caught (F5 — none remain on disk), the 問題10–14
question-form inventory (2.1), the eight other Phase 3 checks, the Shin Kanzen
読解 extractor and its pointers (Phase 7), and `20260819_1`'s model answer (P4.0).

### What this run changed

**Measurement (`tools/dokkai_profile.py`).** All four parse defects repaired plus
the stem fold: every sitting now yields **20 items**, section lengths land within
~3% of `official_calibration.md` §2's committed table, and the option-ratio
distribution reproduces the audit's own figures (median 1.25, p90 1.58) instead
of ratios up to 44. `classify_q14_target` now covers **14 of 14** official items —
5 value, 6 action, 3 choice, **0 truth-check**, which is F4's finding confirmed
from the committed script rather than from prose. `--baseline` names its parse and
states the ~3% gap against `passage_prose()`'s metric, so a threshold can be
checked against *both* ranges rather than moved onto one.

**Corrections the repaired measurement forced.** The ≤1.30 clamp's official breach
rate is **34.3%**, not the audit's 40.5% (that figure came from a parse whose
truncations inflated it). The archive's option-ratio maximum is 4.17, and both
items above 2.5 are 問題14 value items — so **問題14 is exempt** from the ratio
rule and the metric is printed length, not JP-only. The top-overlap WARN moved
44% → **46%**. `20260810_1` and `20260810_2` left the 問題14 grandfather set
without any edit, because their stems were named choices all along; the set went
from 10 papers to 6.

**Gate.** The three WARN-only checks gained their FAIL edges with grandfather sets
computed from the current measurement (問題14 both-truth-check: 6 ids; spans >4: 9
ids; zero 筆者の考え items: 5 ids), every dokkai slug is declared in
`FINDING_REPAIR` and emitted by a check (so `make repair-plan` covers 読解), and
`check_topics_voice_axis` was added for B7.

**Docs.** `dokkai.md`'s option-length and overlap rules re-derived with the parse
rule named; `official_calibration.md` §15's pasted baseline refreshed from
`--baseline`; `exam-blueprint` gained **Rule 5 (voice)** with the per-paper quotas
and a `voices` map in `logs/topics.json`; `exam-qa-review` step 0 now requires
both blind-strategy scores with 45% as the return-to-authoring line; the gate's
quoted bands updated to the re-measured ones.

**Papers — Phase 5 tier A on the three most recent, per D3's order.** All three
had **both** 問題14 stems truth-check shaped; all three now ask what the archive
asks, with every key kept at the position `test_spec.json` planned (so no re-key,
and rotation is untouched):

| paper | 70 | 71 |
|---|---|---|
| `20260819_1` | 「払う金額は、全部でいくらになるか」 — 千四百円 = 学生券600 + 特別展800 | 「日曜日にどの施設を回っておかなければならないか」 — the two 月曜休館 museums |
| `20260818_1` | 「受け取るときに持って行かなければならないものは何か」 — 申請時の受付番号 | 「どのように申し込まなければならないか」 — 窓口, the sister being under 15 |
| `20260817_3` | 「どのように申し込むことになるか」 — marathon only, with a guardian's consent form | 「どうすればこの大会に参加できるか」 — the walking event's same-day desk |

Each distractor is a real combination of flyer cells with one fact changed (F1's
construction rule), which is why one of them had to be re-worded again when the
gate caught 「五つの施設のすべて」 as an on-sight quantifier elimination. Both
`詳細解説.json` entries per paper were re-authored — stem, options and
options_analysis — and booklet, sheet and model answer rebuilt in that order.

### Declines and open work, stated rather than skipped

- **No blind solve has read the nine rewritten items.** No key moved, so this is
  not the autonomy contract's hard stop, but two stems and eight options per paper
  are new text. Queued as `P5Q-newest-3-q14` for a context that authored nothing —
  folding it into this one would not be blind (`AGENTS.md` §5).
- **Phase 5 is otherwise queued, not done**: 11 papers' tier A (問題14 shape,
  overlap/rank repairs, ※ trims — including the 6–8 ※ marks still on the three
  papers repaired above), 5 papers' tier B prose passes, and the tier C voice pass
  that all 14 papers need — every paper measures **0.0%** です・ます against
  official's 30–45%. The state file carries them with the re-measured matrix.
- **Every number in that matrix is this run's measurement, not the report's.**
  Several moved: `20260810_2`'s overlap margin from +0.078 to −0.071,
  `20260813_1`'s kanji density from 38.4% to 39.4%. Plan against the script.
- **Phase 7 step 4** (Shin Kanzen 読解 as a third profile front-end) is `todo`.
- **Two things no gate can judge**, per R.8: whether a rewritten passage reads as
  natural published Japanese, and whether an explanation is a good explanation.
  The nine items above are the review list this run produces.
