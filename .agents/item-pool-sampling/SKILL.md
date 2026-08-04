---
name: item-pool-sampling
description: Single owner of RANDOM, non-repeating selection of what each exam tests — grammar points, vocabulary, kanji, listening scenarios, reading topics, and answer-position balance. Use BEFORE authoring any questions, whenever generating a new test, whenever the user asks for "another test", "random questions", "different questions", or complains that tests repeat the same items. Never let the language model choose items from memory — model choices are heavily biased toward the same famous items and are NOT random; selection must come from scripts/sample_items.py.
---

# Item Pool Sampling

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
  re-checks this and aborts on any collision. This bug shipped once: test 3
  tested 〜に限らず in both 問題7 and 問題8.
- **Cooldown is by WORD, across categories.** The recency map used to be built
  per category, so an overlapping word could be tested in consecutive papers
  through a different 問題 — あらかじめ was test 3's 問題4 (context_words) and
  then test 4's 問題5 (paraphrase, spelled 「あらかじめ(前もって)」). Entries are
  now keyed by both the raw string and its head (everything before the
  disambiguating gloss), so either spelling counts as used.
- **Attribution.** Pass `--test-id <id>` so each draw records which test
  consumed it.

Keep every pool ≥ 2.5× the per-test draw; the script warns below that. Current
headroom is ≥7.9× everywhere (`listening_scenarios` is the tightest at 158/20).

## Workflow

```bash
python .agents/item-pool-sampling/scripts/sample_items.py --seed 20260803 --test-id 4
# omit --seed for a random one; -> writes logs/test_spec.json, updates logs/ledger.json
```

`logs/test_spec.json` is the authoring contract. It contains, per section, the
exact items to test (e.g., `"grammar_p7": ["〜に反して", "〜どころか", …]`),
the scenario list for listening, topics for reading, and the answer-position
sequence per 問題.

## Rules for the authoring step (binding)

- Author questions ONLY for the sampled items. Substituting a "better" item
  from memory defeats the whole mechanism — if an item is genuinely
  unusable, re-run the sampler with `--reroll <category>`.
- **Scan `listening_scenarios` for same-errand pairs before authoring.** The
  sampler draws scenarios independently, so two draws can land in one domain:
  test 3 drew 旅行代理店のプラン変更 AND ホテルのチェックイン変更, test 4 drew
  不動産屋の部屋探し AND 留学生の住居相談 — each pair authored into two 聴解
  items running the same errand, which QA fails ("two 聴解 items may not run
  the same errand"). If two scenarios share a domain or errand shape,
  `--reroll listening_scenarios` before writing anything.
- Place each correct answer at the position the spec dictates; design
  distractors around that position, not the other way.
- Record the seed in the exam's source file header (comment) so any test is
  reproducible and auditable.
- New items learned from reference books go INTO pools.json (the owner),
  never inlined ad hoc into a test.

## Pool maintenance

`pools.json` categories: kanji_reading, orthography, word_formation,
context_words, paraphrase, usage, grammar_p7, grammar_p8, quick_response,
listening_scenarios, reading_topics.

Pools may legitimately overlap (a word can be both a `context_words` and a
`usage` item) — the sampler keeps them apart *within a test*, so there is no
need to make the pools disjoint. What matters is depth: raise a pool as soon
as the script starts printing cooldown-relaxed notes for it.
