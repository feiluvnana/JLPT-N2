---
name: item-pool-sampling
description: Single owner of RANDOM, non-repeating selection of what each exam tests — grammar points, vocabulary, kanji, listening scenarios, reading topics, and answer-position balance. Use BEFORE authoring any questions, whenever generating a new test, whenever the user asks for "another test", "random questions", "different questions", or complains that tests repeat the same items. Never let the language model choose items from memory — model choices are heavily biased toward the same famous items and are NOT random; selection must come from scripts/sample_items.py.
---

# Item Pool Sampling

## Pool entries stay inside the N2 band

Do not add N1-only forms (〜にあって, 〜をもって, 〜ともなると, …) or N3–N5
drills (〜によると, 〜ことができる, …) to `references/pools.json` — see
`exam-qa-review/references/level_band_grammar.txt` and `question-authoring`.
`make check` fails generated papers whose 問題7–9 keys hit that list.

**A `kanji_reading` entry must come with a writable distractor set, or it is not
a pool entry.** `question-authoring`'s 問題1 rule requires three distractors that
share the target's word form and conjugation class and satisfy one of two
branches: a reading of the target's own kanji / a same-radical look-alike, or a
real N2 word in the same semantic field. For some entries that intersection is
**empty**, and an author who has already drawn the target invents non-words
instead of rejecting it — test 4 shipped 「労わる」 with もてあそわる/まねわる/
ひるがえわる (no such words), after an earlier round had shipped
ことわる/さわる/かわる (unrelated kanji, unrelated field). Neither set was
fixable, because 労 reads only ロウ/いたわ(る)/ねぎら(う), no look-alike kanji
yields a ～わる verb, and every real ～わる verb is unrelated to "care for".
So: before adding or keeping a `kanji_reading` entry, write its three
distractors with their source kanji next to it; if you cannot, the entry does
not belong in `references/pools.json`. Undrawable targets are a pool defect the
moment they are committed, exactly like a banned grammar form.

**A pool spelling must match its `references/openjlpt/vocab-n*.json` headword.**
問題1 tests a reading off a printed spelling, so the okurigana is part of the
item. `pools.json` carried `労わる` where the corpus heads `労る`; the paper
printed the non-standard form, and the extra 「わ」 is what locked its options to
the unsatisfiable ～わる class. Fix the pool, never just the paper.

**The pool itself is checked now, not only the paper.** `grammar_p8` shipped
`相対比較(〜ば〜ほど)` for four tests — `〜ば〜ほど` is on `level_band_grammar.txt`'s
`## TOO_EASY` list *and* in `question-authoring`'s banned-too-easy list — and test
3 keyed it at item 46. The paper-level band check could not see it: it matches the
keyed *option string*, which read 「触れるほど」. A banned form in the pool is a
defect the moment it is committed, not the moment it is drawn.

## One grammar point, one pool entry (no spelling variants)

Two entries for one grammar point are two chances to test it twice in one paper.
The sampler's cross-category `taken` guard compares **raw strings**, so two
spellings of the same point are, to the code, two different items:
`grammar_p7` carried `〜がち` + `〜がちだ` and `〜気味` + `〜ぎみだ`, and test 3
drew **both 気味 spellings into the same 問題7** — items 31 and 42 keyed one
grammar point twice.

Rules when adding or editing a grammar pool entry:

- **One spelling per point.** Not kanji *and* kana (`〜に伴って` / `〜にともなって`,
  `〜ざるを得ない` / `〜ざるをえない`), not with *and* without an optional tail
  (`〜つつも` / `〜つつ(も)`, `〜以上は` / `〜以上(は)`), not two conjugations of one
  verb (`〜に沿って` / `〜に沿う`, `〜に伴って` / `〜にともない`).
- **Cross-category overlap must be spelled identically.** Pools may overlap on
  purpose, and `taken` keeps an overlapping item to one 問題 per test — but only
  if the two entries are byte-identical. `〜わりに(は)` in `grammar_p7` beside
  `〜わりに` in `grammar_p8` defeated it; both now read `〜わりに`.
- **A parenthetical is a disambiguating gloss, never a variant.**
  `〜次第(で)` / `〜次第だ` / `〜次第` were three entries for two points; only
  `〜次第だ` (depends on) is in `grammar_p7` now, with bare `〜次第` (as soon as) in
  `grammar_p8`.

`make check` fails on a grammar entry that hits `TOO_HARD`/`TOO_EASY` without an
`ALLOW`, and on two entries in one category whose skeletons match after stripping
`〜`/`～` and parentheticals. **That skeleton rule is a floor**: it catches
`〜次第(で)` / `〜次第` but *not* `〜がち` / `〜がちだ` (differing tail) or
`〜気味` / `〜ぎみだ` (kanji vs kana) — the two pairs that actually shipped. Read
new entries against the three rules above; the gate only covers the easy case.

Known residue the gate does not see, left deliberately (audited 2026-08-06):

- **Cross-category same point, `grammar_p7` × `grammar_p8`, different spelling.**
  Five pairs where p8's labelled pattern contains p7's bare form —
  `〜ばかりに` / `原因理由構文(〜ばかりに…てしまった)`, `〜のみならず` /
  `限定表現(〜のみならず…も)`, `〜に沿って` / `基準準拠(〜に沿って…進める)`,
  `〜につれて` / `変化推移(〜につれて…ていく)`, `〜てたまらない` /
  `感情強調(〜てたまらない)`. Nothing stops one paper testing the point in 問題7
  and again in 問題8. Do not add more; when authoring, if a 問題8 pattern repeats
  a 問題7 point, `--reroll grammar_p8`.
- **`taken` is raw-string, `head()` is only used for recency.** So `交渉(こうしょう)`
  in `kanji_reading` and `交渉` in `orthography` (30 such cross-category pairs)
  can both be drawn into one paper — the same word in 問題1 and 問題2. The fix
  belongs in `sample_items.py` (`taken` should carry `head()` identity too), not
  in the data.
- **`〜に過言ではない`** in `grammar_p7` is malformed Japanese; the form is
  `〜と言っても過言ではない`. Do not author from it until it is corrected.
- **`〜ずくめ(黒ずくめ)`** in `word_formation` matches `TOO_HARD` `ずくめ`. It is a
  問題3 affix, and `level_band_grammar.txt` governs 問題7–9 **keys**, so the band
  check must stay scoped to the grammar categories — running it over
  `word_formation` or `quick_response` produces 7 false hits (即時応答 prompts
  legitimately say 〜てください / 〜ませんか).

## Why this skill exists

A language model asked to "pick 12 N2 grammar points" picks nearly the same
12 every time (〜ざるを得ない, 〜かねない, …), reuses the same scenarios
(会議, レストラン), and biases correct answers toward positions 2-3. That is
determinism wearing a randomness costume. True variety requires:

1. **Explicit pools** (`references/pools.json`) — the full N2 inventory as
   data, sourced from the reference-book calibration.
2. **Seeded RNG sampling** (`scripts/sample_items.py`) — code, not vibes.
3. **An LRU coverage ledger** (`logs/ledger.json`, auto-managed) — see below.
4. **Answer-position balancing** — the script emits a pre-shuffled answer
   key per section (uniform over the option count — 1-4, or 1-3 for 即時応答;
   never 3+ identical in a row).

## Rotation model (ledger v2 — LRU, not reset)

`logs/ledger.json` is `{"version": 2, "history": [ {test_id, seed, generated_at,
items{...}}, … ]}` — one entry per draw, newest last. A v1 flat ledger is
migrated automatically on first run (all legacy items collapse into one
synthetic oldest draw).

- **Cooldown, not exhaustion.** An item used within the last `COOLDOWN` (=2)
  draws is ineligible. If a pool can't fill a draw under that rule, the
  cooldown relaxes one step at a time and says so. The old behaviour cleared
  the *entire* history when a pool ran out, which let an item from the
  immediately-previous test reappear in the next one.
- **One item, one 問題 per test.** Categories are drawn in order against a
  shared `taken` set, so a word in both `context_words` and `usage` (there are
  41 such) can never be tested twice in the same paper. A post-draw assertion
  re-checks this and aborts on any collision.
- **Cooldown is by WORD, across categories.** Recency is tracked across categories by both raw string and `head()` identity so a word tested in one section cannot immediately reappear in another section in the next exam.
- **Attribution.** Pass `--test-id <id>` so each draw records which test
  consumed it.

Keep every pool ≥ 2.5× the per-test draw; inspect headroom with `sample_items.py --check-depth`.

### A draw count that disagrees with `DRAW` is a ledger defect, not history

The ledger is the rotation state, so an item recorded there is ineligible for the
next `COOLDOWN` draws whether or not the paper ever asked about it. `DRAW` was
corrected in three commits — `7638a2f` (`word_formation` 5→3, `quick_response`
12→11, `listening_scenarios` 20→19), `e0a9a04` (`reading_topics` 11→12),
`58a8c8b` (`listening_scenarios` 19→21) — and the entries written under the old
values are still on disk. Measured against today's `DRAW` on 2026-08-06:

| entry | `word_formation` | `quick_response` | `listening_scenarios` | `reading_topics` |
|---|---|---|---|---|
| **`DRAW`** | 3 | 11 | 21 | 12 |
| `2`, `4`, `4-removed` | **5** | **12** | **20** | **11** |
| `3` | 3 | 11 | 21 | 12 — **correct** |
| `legacy` | exempt (v1 migration collapses every past draw into one entry) | | | |

So each of those three entries burns cooldown on **two 語形成 items and one
即時応答 item that no question ever asked**, and under-records one 中文 reading
topic and one 聴解 scenario.

**Trim the over-recorded items from those entries; do not let them expire through
cooldown.** Waiting costs two more tests of rotation on items that were never
used, and it hides the discrepancy in the meantime — which is exactly how it
survived four tests. The `reading_topics` / `listening_scenarios` shortfalls are
not trimmable: record what the paper actually used. `make check` asserts every
history entry except `legacy` matches `sample_items.DRAW`, which is the check that
would have caught the old `DRAW` and will catch the next change; a red line there
means repair the ledger, never widen the check. (Repairing `logs/ledger.json` is
paper-repair work, not pool work — it does not belong to this skill's data.)

## Adjunct staging (non-pool items, Option A)

Pool growth and one-off draws share one gate: **classify → stage → promote** (or
a one-shot adjunct draw at sample time). Nothing enters a test without N2
evidence.

```bash
# Classify a candidate (OpenJLPT, level_band, or pools.json hit)
make classify ITEM='措置' CATEGORY=context_words
make classify ITEM='措置' CATEGORY=context_words STAGE=1   # -> logs/adjunct_staging.json

make promote-adjunct          # status=approved -> pools.json
make expand-pools             # batch OpenJLPT N2 + curated topics into pools.json
make fetch-openjlpt           # refresh vendored slices under references/openjlpt/
make suggest-pool WRITE_STAGING=1   # diff OpenJLPT vs pools, optional staging
```

`sample_items.py` may replace up to **20%** of each category's draw with
`status=ready` staging rows (`--no-adjunct` for pure pool). Adjunct records in
`test_spec.json` look like
`{"item": "…", "origin": "adjunct", "level": "N2", "evidence": [...]}`.
Author them like pool items; `make check` enforces the cap and provenance.

New items learned from reference books: run `classify_level.py`, stage, then
either `promote_adjunct.py` (permanent pool) or leave `ready` for adjunct draw.
Never inline an unclassified string into a test or `pools.json`.

## Workflow & Scripts Reference

### 1. Blueprint Sampling & Resampling (`scripts/sample_items.py`)

```bash
# General sampling with test-id attribution
python .agents/item-pool-sampling/scripts/sample_items.py --seed 20260803 --test-id 4

# Check pool depth and headroom multipliers
python .agents/item-pool-sampling/scripts/sample_items.py --check-depth

# Resample a single category (e.g. listening_scenarios) keeping the rest of test_spec.json
python .agents/item-pool-sampling/scripts/sample_items.py --reroll listening_scenarios --seed 99999
```

`logs/test_spec.json` is the authoring contract. It contains, per section, the
exact items to test (e.g., `"grammar_p7": ["〜に反して", "〜どころか", …]`),
the scenario list for listening, topics for reading, and the answer-position
sequence per 問題.

**It belongs to ONE test and may predate the current `DRAW`.** The spec on disk
is whatever the last `sample_items.py` run produced, so after a format fix its
cardinalities can differ from the code's. (The file in `logs/` right now is test
3's and matches `DRAW` in all 11 categories — measured 2026-08-06 — but tests 2
and 4 were sampled under the old values and their ledger entries still show it;
see "A draw count that disagrees with `DRAW`" above.)
`check_answer_positions` zips the prescribed positions against the questions that
exist, so extra prescribed entries are silently ignored and the mismatch is
invisible. Do not "reconcile" it by re-sampling for a test that is already
authored — that rewrites the contract its 101 keys were placed against and turns
the gate red. Re-sample when you start the NEXT test, and read the printed draw
counts then.

### 2. Level Classification (`scripts/classify_level.py`)

Validates candidate items against OpenJLPT N2 data, `pools.json`, and `level_band_grammar.txt`. Only items verified as N2 can be staged or added to pools.

### 3. Pool Expansion & Curation (`scripts/expand_pools.py`, `scripts/suggest_pool_additions.py`)

Proposes and appends verified N2 items from OpenJLPT and curated N2 affixes/topics into `references/pools.json`.

## Rules for the authoring step (binding)

- Author questions ONLY for the sampled items. Substituting a "better" item
  from memory defeats the whole mechanism — if an item is genuinely
  unusable, re-run the sampler with `--reroll <category>`.
- **Domain Collision Check for `listening_scenarios`:** `sample_items.py` automatically checks and warns if sampled scenarios share identical domain prefixes (e.g., two `不動産` or `旅行代理店` settings). If a warning is printed, check if the items run the same errand. If so, run `python .agents/item-pool-sampling/scripts/sample_items.py --reroll listening_scenarios` before writing anything.
- Place each correct answer at the position the spec dictates; design
  distractors around that position, not the other way.
- Record the seed in the exam's source file header (comment) so any test is
  reproducible and auditable.
- New items learned from reference books go INTO `pools.json` via classification and promotion, never inlined ad hoc into a test — use `classify_level.py` → staging → `promote_adjunct.py`.

## Pool maintenance

`pools.json` categories: kanji_reading, orthography, word_formation,
context_words, paraphrase, usage, grammar_p7, grammar_p8, quick_response,
listening_scenarios, reading_topics.

Pools may legitimately overlap (a word can be both a `context_words` and a
`usage` item) — the sampler keeps them apart *within a test*, so there is no
need to make the pools disjoint. What matters is depth: raise a pool as soon
as `sample_items.py --check-depth` or cooldown messages indicate a tight pool.

