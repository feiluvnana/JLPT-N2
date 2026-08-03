---
name: web-topic-research
description: Single owner of sourcing FRESH, real-world creative input for exam content — current topics, factual texture, seasonal context, and collocation checks — from the web instead of relying only on textbook inventories and static pools. Its output now flavors EVERY exam surface (reading, listening, cloze, carrier sentences, 即時応答 settings, 情報検索 flyers), always blended with the Shin-Kanzen-calibrated pools under hard balance caps so neither source dominates. Use whenever authoring any exam section, whenever the user says tests feel repetitive, stale, textbook-bound, or "not creative", and whenever web access is available during test generation. Runs AFTER item-pool-sampling and BEFORE question-authoring.
---

# Web Topic Research

## Why this skill exists

Pools guarantee rotation, but rotation inside a closed set is not creativity.
Real JLPT papers read as current because they are adapted from real columns,
essays, and news. This skill injects that freshness EVERYWHERE — not only in
reading passages: the web supplies TOPIC SEEDS and FACTUAL TEXTURE; the agent
writes 100% original prose around them.

## Two hard principles (read before harvesting)

1. **Web decorates, pools test.** Tested linguistic items — grammar points,
   vocabulary, kanji, idioms/keigo — ALWAYS come from `pools.json`, which is
   calibrated against the Shin Kanzen Master inventories. The web only ever
   supplies topics, settings, and facts to wrap around those items. This is
   how N2 level is preserved no matter how fresh the topic is.
2. **Balanced blend, never dominance.** Every surface the web touches stays a
   mix: web share is clamped to 30-60% (pool keeps ≥40%), no single source
   domain supplies more than 2 blended seeds, and with fewer than 3 distinct
   domains the ratios auto-shrink. A test that is all-NHK is as stale as a
   test that is all-textbook — the caps are enforced by `merge_seeds.py`,
   not left to judgment.

## Step 1 — Harvest topic seeds (18-25 per test; ~22 funds every surface at full ratios)

More surfaces need more seeds than before. Spread the harvest across at
least 3-4 distinct source domains. Good sources and query recipes (prefer
Japanese-language results):

- **NHK NEWS WEB EASY** — pre-simplified news; ideal difficulty reference and
  topic source. Query: `NHK news easy 今週`. Cap: NHK Easy alone must not be
  the majority of your seeds.
- **General news topics** — `日本 話題 ニュース <current month>`,
  `暮らし コラム`, `働き方 調査 結果`.
- **Survey/statistics releases** — `調査 結果 <topic>` (白書, 意識調査);
  numbers make excellent 問題14 flyers and ポイント理解 details.
- **Seasonal anchor** — always include 2-3 season-appropriate seeds for the
  generation date (12月→忘年会/大掃除/インフルエンザ, 6月→梅雨/衣替え).
- **Trend checks for scenario texture** — new shop formats, services, or
  habits (無人店舗, 置き配, キャッシュレス食券…) that make dialogues feel 2020s
  rather than 1990s.

Record each seed as:
`{"seed": "...", "facts": ["..."], "source": "url", "surfaces": ["reading"|"listening"|"carrier"|"info", ...]}`
in `seeds.json` (or `logs/seeds.json`). `surfaces` is an optional hint about
where the seed fits best (a survey with percentages → `["reading","info"]`;
a new service format → `["listening","carrier"]`); omit it for
anything-goes seeds. Facts are short paraphrased data points (a percentage,
a trend direction), never sentences copied from the page.

## Step 2 — Filter for exam suitability AND N2 level

JLPT content is deliberately neutral. REJECT seeds involving: politics and
elections, religion, war/crime/accidents with victims, discrimination
debates, celebrity gossip, or anything distressing. PREFER: daily life, work
customs, technology in daily use, food, travel, education, environment,
community, health habits (non-medical).

N2 gate — apply to every seed before it enters `seeds.json`:

- **Expressibility check**: mentally draft one sentence introducing the
  topic using only N2-and-below vocabulary. If the topic cannot be named
  without N1 jargon (専門用語), drop it or generalize it (e.g.,
  生成AIの著作権問題 → 新しい技術と仕事の変化).
- **Inventory check for doubtful words**: if a seed's key word MIGHT be
  above N2, verify it against the Shin Kanzen TOC inventories via
  `reference-book-reading` (thematic 語彙 chapter bands) before keeping it.
- **Fact simplification**: round numbers to N2-friendly forms at harvest
  time (`38.6%` → `約4割`), so no raw figure leaks into a passage later.

## Step 3 — Blend into the authoring contract

```bash
python3 .agents/web-topic-research/scripts/merge_seeds.py seeds.json logs/test_spec.json
# optional tuning (both clamped to 0.30-0.60):
#   --reading-ratio 0.5 --listening-ratio 0.4
```

The script now touches the whole spec, recording provenance
(`"origin": "web"` vs `"pool"`) on every blended entry so any test can be
audited:

| Spec field | Exam surface | Blend rule |
|---|---|---|
| `items.reading_topics` | 問題10-13 passages | ~50% replaced by web seeds (clamped 30-60%) |
| `items.listening_scenarios` | 聴解 問題1/2/3/5 | ~40% of scenario settings replaced (clamped 30-60%) |
| `cloze_topic` | 問題9 cloze passage | web or pool, 50/50 by seeded RNG |
| `info_retrieval_texture` | 問題14 flyer | one numeric-fact seed, if any seed has numbers |
| `qr_situation_seeds` | 問題4 即時応答 | ≤3 situational settings (the tested idiom/keigo stays pool-sampled) |
| `carrier_seeds` | 問題1-8 carrier sentences | ≤6 texture seeds; **binding cap: at most 1 in 3 carrier sentences per 問題 may use them** |

It prints a blend report (web/pool share per surface + domain histogram).
Read it: if any surface reports 0% web with seeds available, or the domain
histogram is a single domain, fix the harvest and re-run.

Pool topics remain the offline fallback: with no web access, skip this
skill entirely — the pipeline still works, just less fresh.

## Step 4 — Use during authoring (binding rules)

- Web sources give WHAT to write about, never the words to write. Compose
  passages from scratch; do not paraphrase a source article's structure.
- Honor provenance everywhere: an entry with `"origin": "web"` is written
  around that seed; an entry with `"origin": "pool"` is written from the
  pool topic as before. Do not swap origins to taste.
- One borrowed FACT per passage/dialogue is plenty
  (「ある調査によると、約4割が…」); all figures stay in the simplified form
  from Step 2.
- **Listening**: a web scenario entry is a SETTING seed (e.g., 無人店舗) —
  frame it into the standard 場所×出来事 shape yourself; dialogue mechanics
  (wrong options mentioned-then-eliminated, 「その前に」 traps) come from
  `question-authoring` unchanged.
- **Carrier sentences (問題1-8)**: at most 1 in 3 stems per 問題 may draw on
  `carrier_seeds`; the remainder use neutral/pool settings. The TESTED word
  or grammar point is always the sampled one — never substitute a fresher
  word from the web.
- **即時応答**: `qr_situation_seeds` may set the scene of an utterance; the
  tested idiom/keigo is always the pool-sampled item.
- Collocation check: for any sampled word the agent is unsure about, search
  `"<word>" 例文` or `"<word>" 使い方` and confirm the intended collocation
  exists before building a question on it (e.g., 交渉が難航する ✓).
- Good seeds discovered during research that fit the pools should be
  proposed as pool additions (`.agents/item-pool-sampling/references/pools.json`) — the web
  feeds the pools over time, keeping them alive.

## Creative recombination (works offline too)

When seeds run thin, force novelty combinatorially instead of asking the
model to "be creative": scenario = random(place) × random(complication) ×
random(constraint), e.g. 市役所 × 必要書類が足りない × 締め切りは今日中.
Roll these with the RNG seed from `logs/test_spec.json`, not by model preference.

## Integration note

Integrated into the orchestrator workflow (`.agents/jlpt-test-generation/SKILL.md`) between sampling and authoring:
`3.5 **Research fresh topics (Optional / Web available)** → read web-topic-research/SKILL.md`
and registered in `AGENTS.md` under section 1 (Available Skills) & section 4 (Pipeline Execution Commands).
