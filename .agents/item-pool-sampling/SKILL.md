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
3. **A coverage ledger** (`logs/ledger.json`, auto-managed) — items used by past
   tests are excluded until the pool is exhausted, then it resets. Across
   runs this guarantees rotation, not repetition.
4. **Answer-position balancing** — the script emits a pre-shuffled answer
   key per section (uniform 1-4, never 3+ identical in a row).

## Workflow

```bash
python .agents/item-pool-sampling/scripts/sample_items.py --seed 20260803        # omit --seed for random
# -> writes logs/test_spec.json, updates logs/ledger.json
```

`logs/test_spec.json` is the authoring contract. It contains, per section, the
exact items to test (e.g., `"grammar_p7": ["〜に反して", "〜どころか", …]`),
the scenario list for listening, topics for reading, and the answer-position
sequence per 問題.

## Rules for the authoring step (binding)

- Author questions ONLY for the sampled items. Substituting a "better" item
  from memory defeats the whole mechanism — if an item is genuinely
  unusable, re-run the sampler with `--reroll <category>`.
- Place each correct answer at the position the spec dictates; design
  distractors around that position, not the other way.
- Record the seed in the exam's source file header (comment) so any test is
  reproducible and auditable.
- New items learned from reference books go INTO pools.json (the owner),
  never inlined ad hoc into a test.

## Pool maintenance

`pools.json` categories: kanji_reading, orthography, word_formation,
context_words, paraphrase, usage, grammar_p7, grammar_p8, quick_response,
listening_scenarios, reading_topics. Keep every pool ≥ 2.5× the per-test
draw so the ledger has room to rotate (the script warns when a pool runs
thin).
