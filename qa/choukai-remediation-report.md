# 聴解 remediation — run report

Plan: `REPORT-CHOUKAI.md` §"Remediation plan" (`plan_sha` ce11bf09d8f4).
State: `logs/choukai_remediation_state.json`. Required by Phase R.7 and
`AGENTS.md` §0.7.

---

## Run 2 — 2026-08-21: audit the first pass, then repair what it skipped

**Why this run exists.** Run 1 (commits `b41bcb9`, `b27071c`) reported the plan
as implemented. This run re-derived every claim by measuring the artifact rather
than trusting the report — Phase R.4.3's rule — and found that the *pipeline*
half had landed in outline while several of its load-bearing parts were wrong,
missing, or contradicted by the very script the plan built to end that class of
defect. The findings below are the audit; everything after is the repair.

### Skills read in full

`AGENTS.md` §0, `choukai-audio/SKILL.md`, `question-authoring/references/choukai-items.md`,
`jlpt-exam-structure/SKILL.md` (問題1 forms), `choukai-audio/references/official_pacing.md`,
`choukai-audio/references/official_register.md`, plus `REPORT-CHOUKAI.md` end to end.

### What the audit found

| # | Finding | Class |
|---|---|---|
| A1 | `check_choukai_q4_stimulus_register` read `lines[0].split("。")[1]` — the empty string for every well-formed block. Every paper measured **0 casual / 0 keigo / 11 neutral**, so the check could neither pass nor ever empty its grandfather set, while F4's real 44%-keigo drift stayed invisible. | gate measures nothing |
| A2 | `check_choukai_pause_distribution` — Phase 3's tenth row, the only gate on F8 — **did not exist**, so the jitter change had no verification at all. | missing |
| A3 | `PACING_SHA_GRANDFATHERED` carried **13 of 14 papers**: the Phase 4 rebuild was skipped and the resulting red silenced by grandfathering, where R.3 says record it as expected-red. | green by exemption |
| A4 | Doc numbers still not from the script (the exact D1 defect): 問題1 frame shares pasted from the report under a header claiming 31 sittings; 問題4 "49% casual / 13% keigo" against the profile's 20.7%/9.1%; `official_register.md` §7.4 still asserting median 305 where the profile reads 243; the gate's talk band [175, 450] matching neither. | measurement drift |
| A5 | `official_register.md` §6 still said "**Not committed as a script**" — Phase 2.4's single explicit instruction. | not done |
| A6 | `official_pacing.md` had neither the Shin Kanzen third corpus nor the distribution method (Phase 2.4); nothing documented the jitter ladder, while `SKILL.md` still described turn gaps as a flat `GAP_BETWEEN_LINES = 0.9` — a constant the code no longer used. | doc ↔ code |
| A7 | Seven new grandfather sets were named in the gate only. The plan's house rule: the owner doc names them too, or green stops being evidence. | half-landed |
| A8 | `SPEAKER_MAP` gained **both** naming schemes — `男性職員…` and the `職員2…` set the plan rejected — 8 duplicate unused labels for the same voices. | duplication |
| A9 | `tools/choukai_profile.py` carried a **hand copy of `SPEAKER_MAP`** that already lagged the labels Phase 4.1 had added, so voice balance and pitch margins were computed off a map the audio never used. The fourth copy of a number, in the file built to prevent exactly that. | duplication |
| A10 | Service-formula caps were hand-picked (2/1/0) and **two of seven were wrong in opposite directions**: 「かしこまりました」 allowed twice against an archive max of 1, and 「そうですね」 — which official uses at a median of **3 per paper**, five times our rate — capped at 1. A rule pushing papers away from official while reading as a register fix. | threshold invented |
| A11 | Phase 5.0's `--json` findings mode, `tools/choukai_repair_plan.py`, `make findings` and `make repair-plan` were **not built**; §5.0.1's two deterministic autofix lanes were not added. | not done |
| A12 | The Phase R state file and this report did not exist, so nothing on disk knew what remained. | not done |
| A13 | Phase 7 step 4 (feed the Shin Kanzen script to the profile as a third front-end) not done; `choukai-audio` Part 4 still implied no such script exists. | partial |

Phase 1's script itself, Phase 4.1's gendered labels, Phase 4.2's turn-gap
ladder, the D2 semitone margin, the Phase 7 extractor, the `20260807_1`
問題5-2番 casting repair and `20260817_2`'s 消去方法 cells **were all genuinely
done** and are recorded as such in the state file, each re-verified by
measurement (e.g. the repaired item now casts 男性係員 vs 夫 at 2.94 st).

### What this run changed

**Gate (`tools/check_consistency.py`).** Repaired A1 (stimulus read from the
spoken line, plus the ≥5-casual and ≤4-keigo WARN halves the plan asked for);
added A2 with the same `silencedetect` method as the audit; added the 70% WARN
band to voice balance; re-derived the 問題3 talk band from the profile —
**[150, 400]**, outside the current era's measured 158–397, replacing a floor of
175 that sat *inside* the archive's range (official ships a 158-char talk, so
official itself would have failed it) and a ceiling of 450 that came from no
measurement; added the 問題1 rare-frame targets; gated both pause ladders'
invariants; made service-formula bands measured (A10), with 「そうですね」 now
checked as a **floor**; extended the `FINDING_REPAIR` meta-check so an emitted
slug with no declaration FAILs and a declaration no check emits WARNs; added
`check_remediation_state` so a state file cannot drift from its plan.

**Measurement (`tools/choukai_profile.py`).** `SPEAKER_MAP` now loads from the
synthesis script (A9); `--baseline` extended to §§6–7 (問題5 speaker counts,
per-大問 voice balance, 問題1 single-speaker share and proposal load) and now
prints **the parse rule for every row**, which is what makes a doc refresh a
paste; per-formula archive bands added.

**Docs.** A4–A7 repaired: `jlpt-exam-structure` and `choukai-items.md` now carry
the profile's numbers, `choukai-items.md` names every grandfather set with its
removal condition, `official_register.md` §6 carries the command and §7.4 records
why 305 was wrong (it was one sitting's per-paper median), §1's "turn length is
already right" is corrected to the measured 27-vs-37, `official_pacing.md` gains
§6.1 (the distribution, the third corpus, and what the ladders can and cannot
fix), and `choukai-audio` Part 3 documents both ladders while Part 4 stops
implying the Shin Kanzen script does not exist.

**Audio (`make_choukai_mp3.py`).** Removed the duplicate `職員2` label set (A8).
Added `WITHIN_TURN_LADDER` — the turn-gap ladder alone left the spike share at
**46%** against a 35% cap, because ~480 within-turn pauses per paper were still
clamped to exactly 0.5 s against ~120 turn boundaries. Measured on `20260807_1`:
spikes **60% → 46% → 18%**.

**A plan number that did not survive measurement.** Phase 4.2 asks for a >1.05 s
tail of 10–25%. Only a turn *boundary* may exceed the 0.9 s gap — a within-turn
pause at or above it makes one speaker sound like two, which is a gated
invariant — and our papers hold ~120 boundaries against ~480 within-turn pauses
because our median turn is 27 chars where official's is 37. The reachable
ceiling is therefore **≈9%**, and the rest is script shape, i.e. authoring work
(F9), not a constant. The gate floor is 7% with the spike cap at 35%, and
`official_pacing.md` §6.1 records the reasoning. This is the same class of
correction as F3's 18% and F7's 305: a number nobody could reproduce, replaced
by one that a committed script prints.

**Tooling (A11).** `make findings` (gate `--json` → `logs/findings.json`, one
record per slugged finding with its artifact and derived tier), `make repair-plan
[<id>] [TIER=B]` → `qa/[<id>/]repair-plan.{json,md}` printing the rebuild set as
a command list, the deterministic subset as `make autofix` invocations, and every
declined paper with its reason. Slugs attached to 14 existing choukai checks.
`make autofix` gained the split-turn join and the voice-margin recast; the recast
**simulates** each candidate swap, because the naive version moved `20260814_1`
問題5-2番 from a 1.42 st female pair to a **1.12 st male** one. Its 縮約形 table
was also split into casual and polite ladders — the single table had been turning
keigo service lines into 「承っとくね」, F4's own drift committed by the tool
meant to fix register.

**Papers (Phase 5 tier B, the 6 non-C2 ids).** `20260814_1`, `20260817_1`,
`20260817_2`, `20260817_3`, `20260818_1`, `20260819_1`: every service formula
brought inside the measured archive band and 「そうですね」 raised to the archive
median; `20260814_1`'s short-reaction share 10.7% → **13.2%** by letting the
other speaker land a beat mid-explanation (never by adding a same-speaker line,
which is a split turn); `20260814_1` 例 and `20260819_1` 問題5-2番 recast onto
gendered role labels — and `20260819_1`'s 構成表, which had documented its 14 Hz
split as compliance, now records the 1.19 st shortfall and the 4.06 st repair.
Two 解説 quotes in `20260817_3` were re-synced to the lines they quote.

**Rebuild.** All 14 papers: `make mp3` → `make booklet` → `make sheet` → `make
pages`, emptying `PACING_SHA_GRANDFATHERED` (A3).

### Declines and open work, stated rather than skipped

- **Tier C is not done.** C1 (3 papers × 2–3 items) and C2 (8 papers × a whole
  聴解 section) plus §5D's QA/explanation tail are `todo` in the state file with
  their axis counts and dependency order. They are the half of the plan that
  changes what a learner gets, and they are authoring work at a scale one run
  cannot do honestly.
- **`20260807_1` moved out of C2 by measurement.** Its 問題3 axis dissolved when
  the talk floor was corrected (168–170 chars is inside the archive's range) and
  its casting axis is repaired, leaving one axis: no 構成表. Recorded in the
  state file rather than quietly dropped.
- **§5D's Vietnamese half no longer applies.** The per-language explanation
  pipeline was retired 2026-08-21 (`AGENTS.md` §5), so `詳細解説.vi.json` is not
  authored and `20260819_1`'s missing file is not a gap.
- **Phase 7 step 4** (Shin Kanzen as a third profile front-end) is `todo`.
- **No MP3 was listened to**, exactly as the audit itself noted. Every voice
  finding is from `SPEAKER_MAP` values and from silence measurement; the pitch
  margin is settled by D2's rule, and a listener may still overturn it.
