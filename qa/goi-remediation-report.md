# 文字・語彙 remediation — run 1 (2026-08-21)

Consumes `REPORT-GOI.md`. **Scope of this run: the pipeline half** — the
measurement script, the rule changes in every owner file, the gate lines that
make them observable, and the two literal rule breaches cheap enough to repair
without a re-draw. The per-paper repair passes (tier B stems ×14, tier C
re-draws ≈30 items) are queued below, not done.

Skills read in full before acting: `AGENTS.md`, `question-authoring/SKILL.md` +
`references/moji-goi.md` + `references/official_calibration.md`,
`exam-blueprint/SKILL.md` + `scripts/sample_items.py`, `exam-qa-review/SKILL.md`,
`exam-answer-translation/SKILL.md`, the 文字・語彙 half of
`tools/check_consistency.py`.

## Landed

| # | Finding | What changed |
|---|---|---|
| — | D1 | `tools/goi_profile.py` (new): one parser, both corpora, **954 of 964 archive items (98.9 %)** + all 420 generated items. `make goi-profile [BASELINE=1]`; `check_consistency.py` imports it, so thresholds and doc tables cannot drift. |
| F10.1 | 問題6 option length | `official_calibration.md` §7 said mean 25.0 / range 9–35 (n=136). Re-measured: current era **26.0 / 25 / 18–39 (n=136)**, all era 26.3 / 26 / 13–39 (n=608). The n and median reproduce (the window was the current era); the range does not — the advice 「a 9-char option is official」 is **withdrawn**, and `moji-goi.md` §問題6 carries the replacement. |
| F10.2 | longest-key baseline | Gate message said 15 % / 16 %. Measured **19 % both** (問題5 22/116, 問題6 29/151), 0–50 % per paper. The proposed 10 % floor is **refuted** — six official sittings run 0 %, so no floor was added; the ≤30 % ceiling is documented as a current-era envelope (max 22 %). |
| F10.3 | 訓読み evidence | The archive loses the underline, so `goi_profile` reports `target=None` for every official 問題1 item by design. The band is relabelled everywhere as **five sittings, hand-classified**, with a pointer to Shin Kanzen's typeset 模擬試験 as what would settle it. |
| F1/F2/F4/F7 | the stem contract | New `moji-goi.md` Part 0 §"The stem": median 15–22 (author 17), ≥9 of 15 comma-free, ≥2 (author 7) です・ます stems, ≥1 first-person, ≤7 (author ≤2) institution-actor, 問題4 median ≤37/author 30 with no stem past 47. Gate: `check_moji_stem_shape`, `check_moji_stem_register`, `check_moji4_stem_band`. Also in `jlpt-test-generation`'s authoring brief and `exam-qa-review` §3 (two counts, before solving). |
| F3 | 問題2 composition | ≥1 和語 target (author 2), ≤3 bare 2-kanji compounds — the archive's own bounds in 31 of 31 sittings. Draw-time: `sample_wago_floor()` samples the 和語 count from the archive's histogram (`WAGO_DIST` 1:1, 2:23, 3:7). Gate: `check_moji2_composition`. |
| F5 | 訓読み floor | `KUN_CAP` became a band 1–2 (`KUN_FLOOR`), enforced in `sample_kun_capped()` including `--reroll-one`, and `check_mondai1_reading_type_mix` prints both bounds. |
| F6 | option distinctness | The 問題5-only rule is now section-agnostic (`moji-goi.md` Part 0) and `check_mondai5_option_reuse` → **`check_moji_option_reuse` over 問題1–6**. Official: 0 repeats in 31 of 31 sittings, any 大問. |
| F8 | legacy queue | `check_legacy_item_repeats` prints all **eleven** live repeats by item and paper pair as a standing WARN; `exam-blueprint` "Rotation model" names them. The exemption keeps its skip, the queue stops being invisible. |
| F9 | 「頻繁に」 | **Repaired** on disk: `20260813_2` 問題1-5 now prints 「戸締まり…出入りが**頻繁**になった」 — the 「に」 belongs to 〜になる, and the options read 頻繁, so the marked span was wrong, not the option field. New gate `check_moji1_okurigana_exposure`, no exemptions. Rebuilt booklet + sheet + `詳細解説.json` + vi merge + 模範解答.html. |

`make check`: **green, 190 warnings** (138 before). Every new warning is a
grandfather line from the checks above plus the legacy queue; no pre-existing
warning disappeared (diffed against a clean HEAD worktree).

Two side effects of rebuilding `20260813_2`'s model answer with the current
builder, both improvements: seventeen bogus `passage-box` blocks (a mangled
問題7 stem pasted onto 問題7/8 cards) and one stale malformed 問5-2 card with
empty explanations were dropped.

## Declined, with the measurement

- **A 10 % floor under the 問題5/6 longest-key rate** (`REPORT-GOI` §D2's table).
  Per-paper official rates are 0/0/0/0/0/0/10/11/… — six sittings key no
  uniquely-longest option at all, so the floor would fail official papers, which
  `AGENTS.md` §0 makes the floor's defect and not the paper's.
- **The autonomy machinery** (`logs/goi_remediation_state.json`, the cron lease,
  §Phase R). Not built: this run was interactive and single-session. The queue
  below plus the gate's own grandfather sets are the state.

## Queued — the papers, in `REPORT-GOI` §D3 order

Every id below is named in a grandfather set in `tools/check_consistency.py`;
the set is the queue and shrinks only when the paper is repaired.

| Tier | Work | Papers |
|---|---|---|
| A | one 問題3 distractor each (F6) | `20260810_1` 半, `20260810_2` 半+総, `20260811_1` 各, `20260813_1` 性 |
| B | the stem contract, one rewrite per paper (F1/F2/F4/F7) | all 14 except `20260810_1` on shape; 9 on register; 5 on the 問題4 band (`20260811_1` first — median 64 against an archive max single stem of 47) |
| C | `orthography` re-draw for the 問題2 composition floor (F3) | 6 papers at zero 和語, 11 above the compound ceiling |
| C | `kanji_reading` re-draw for the 訓読み band (F5) | `20260817_3` (0), `20260807_1` (4), `20260810_1` (3), `20260817_2` (3) |
| C | the eleven legacy item repeats (F8) | `20260807_1`, `20260810_1`, `20260810_2`, `20260811_1`, `20260812_1`, `20260812_2`, `20260813_1` |

Not started, and it blocks tier C's band checks: **Phase 7**, the four scanned
books (`REPORT-GOI` §F11) — no extract, no make target, no `provenance` field in
`pools.json`. Until it lands, a re-drawn key's band is an author reading a
scanned page, and every re-drawn key must be named in the QA report with the
book and page that confirmed it (`exam-qa-review` §3).

Ordering rule for the queue, unchanged from the plan: **draw-time work (tier C)
before stem work (tier B) on the same paper** — a re-draw invalidates a stem
that was just rewritten. One paper per session, and each paper ends with the
Phase 4 rebuild chain (`booklet` → `sheet` → `詳細解説.json` → vi re-merge →
`model-answer`) plus `make check` read line by line.
