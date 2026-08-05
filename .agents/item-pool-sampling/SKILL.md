---
name: item-pool-sampling
description: Single owner of RANDOM, non-repeating selection of what each exam tests — grammar points, vocabulary, kanji, listening scenarios, reading topics, and answer-position balance. Use BEFORE authoring any questions, whenever generating a new test, whenever the user asks for "another test", "random questions", "different questions", or complains that tests repeat the same items. Never let the language model choose items from memory — model choices are heavily biased toward the same famous items and are NOT random; selection must come from scripts/sample_items.py.
---

# Item Pool Sampling

## Why this skill exists

Pool entries must stay inside the N2 band. Do not add N1-only forms
(〜にあって, 〜をもって, 〜ともなると, …) or N3–N5 drills (〜によると,
〜ことができる, …) to `references/pools.json` — see
`exam-qa-review/references/level_band_grammar.txt` and `question-authoring`.
`make check` fails generated papers whose 問題7–9 keys hit that list.

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

