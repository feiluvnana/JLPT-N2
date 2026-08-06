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

### The `kanji_reading` validity rule (audited 2026-08-06)

Test 4 shipped three unanswerable 問題1 items — `領(えり)`, `線(すじ)`,
`爆(は.ぜる)` — because nothing checked that the printed kanji actually *has*
the keyed reading. The sentences were simply the wrong kanji (襟のシャツ,
この筋で), and for 線 the *distractor* せん was the right answer. Every
`kanji_reading` entry must now satisfy all four:

1. **Shape.** The entry reads `語(よみ)`. `語` contains at least one kanji;
   `よみ` is hiragana with **no `.` and no katakana**. A dot is a raw KANJIDIC
   kunyomi (`爆(は.ぜる)`) — i.e. a single kanji with its okurigana *detached*,
   which cannot be printed or underlined as a word. Katakana (`販(ハン)`,
   `歴(レキ)`) is a raw on-reading dump, a bound morpheme, not a word.
2. **Attested.** `(語, よみ)` appears as a headword + `reading` pair in
   `references/openjlpt/vocab-n1|n2|n3.json`. This is the decisive test for
   **single-kanji** entries, which have no fallback: `針(はり)` is a headword
   and is legitimate (official Dec 2012 問題1 tests exactly it); `領(えり)`,
   `線(すじ)`, `団(かたまり)`, `脳(のうずる)` are not headwords and are out.
3. **In band, if the corpus misses it.** A **multi-character** word absent from
   the corpus may be kept only when its reading is the ordinary dictionary
   reading on 常用 音訓 *and* the word is corroborated by the official archive
   under `refs/JLPT_N2_NEW/` (31 sittings, 2010–2025). Corpus absence is often
   a corpus gap — 概要, 更新, 潜む, 訪ねる, 抑える are all sound N2 items that
   openjlpt simply does not head. Zero hits in **both** sources is the removal
   signal, and it removed 却下, 侮る, 和らぐ, 損じる, 任じる, 講じる.
4. **Drawable.** Three distractors are writable (the rule above this one).

**Do NOT use `references/openjlpt/kanji-n*.json` as the 音訓 authority.** It is
KANJIDIC-derived and carries **表外** readings: it is where `領: えり` and
`線: すじ` come from in the first place, so a check built on it passes the exact
defects it was written to catch. It can refute an okurigana shape (`労` reads
いたわ.る, so `労わる` needs okurigana る, not わる — that is how 労わる was
caught); it can never *confirm* an entry.

Verify a candidate before adding it:

```bash
python3 - <<'PY'
import json, collections
ob = '.agents/item-pool-sampling/references/openjlpt/'
idx = collections.defaultdict(set)
for lv in ('n1', 'n2', 'n3'):
    for e in json.load(open(ob + f'vocab-{lv}.json')):
        for w in e.get('word', '').split('/'):
            idx[w.strip()].add(e.get('reading', ''))
print(idx.get('針'), idx.get('領'))     # {'はり'}  set()
PY
# and, for a corpus miss, check the official archive (calibration only —
# never copy an official item into the pool):
pdftotext -enc UTF-8 "refs/JLPT_N2_NEW/3. N2 12-2012/3. N2 12-2012.pdf" - | grep 概要
```

The 2026-08-06 audit removed **103** of 218 entries (97 single-kanji
non-headwords, 3 shape/word-form defects — `労わる(いたわる)`,
`報われる(むくわれる)` (an inflected passive, not a headword),
`じる(じる)` (no kanji at all) — and the 6 double-miss words above) and repaired
`免れる(まぬがれる)` → `免れる(まぬかれる)` (the 常用 reading; まぬがれる is not on
the 常用漢字表). 112 entries remain, 22× headroom over `DRAW` of 5.

**`kanji_reading` is the only category whose parenthetical is a reading.**
`orthography`'s `納める(税金)` is a disambiguating context, `paraphrase`'s
`詫びる(謝る)` a synonym, `word_formation`'s `諸〜(諸問題)` an example — this rule
does not apply to them.

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
  in `kanji_reading` and `交渉` in `orthography` (7 such `kanji_reading` ×
  `orthography` pairs after the 2026-08-06 audit; 98 head-identical
  cross-category pairs in all, 41 of them `context_words` × `usage`) can both be
  drawn into one paper — the same word in 問題1 and 問題2. The fix belongs in
  `sample_items.py` (`taken` should carry `head()` identity too), not in the
  data. **Still open**: the 2026-08-06 pass left it alone on purpose, because
  changing `taken` changes every draw and was outside its four work items.
- **`〜に過言ではない`** in `grammar_p7` is malformed Japanese; the form is
  `〜と言っても過言ではない`. Do not author from it until it is corrected.
- **`〜ずくめ(黒ずくめ)`** in `word_formation` matches `TOO_HARD` `ずくめ`. It is a
  問題3 affix, and `level_band_grammar.txt` governs 問題7–9 **keys**, so the band
  check must stay scoped to the grammar categories — running it over
  `word_formation` or `quick_response` produces 7 false hits (即時応答 prompts
  legitimately say 〜てください / 〜ませんか).

## Topic themes — the closed vocabulary (this skill owns it)

`reading_topics` and `listening_scenarios` are the only two pool categories
whose entries are **objects, not bare strings**:

```json
{"topic":    "在宅勤務と切り替え", "theme": "働き方"}
{"scenario": "会社:会議の準備",    "theme": "働き方"}
```

`theme` is drawn from a **CLOSED** list of twenty values, defined once in
`scripts/level_data.py` as `THEMES` and reproduced here:

| | | | |
|---|---|---|---|
| 睡眠・健康 | 医療・福祉 | 食 | 環境 |
| 防災 | 交通 | 住まい | 働き方 |
| 教育 | 子育て・家族 | 地域活性化 | デジタル化 |
| 消費・経済 | 文化・伝統 | スポーツ・余暇 | 人間関係 |
| 行政・手続き | メディア・情報 | 旅行・観光 | 科学・技術 |

**Never widen the list to make an entry fit** — a stretched label is worse than
a wrong one, because it looks like agreement. Pick the nearest value, or say the
entry does not belong in the pool. Adding a value is a deliberate edit of the
taxonomy: change `THEMES`, retag every entry the new value should own, and say
so in your report. `web-topic-research/SKILL.md` consumes these tags (its
one-surface-per-theme and cross-test repeat-budget rules) and defers to this
list; keep the two consistent.

**Why the tags exist.** `check_topic_reuse()` and the gate compare the *wording*
of a topic, so 「交替制勤務と睡眠の質」 and 「就寝前の刺激と生活習慣」 come out as
two different subjects — zero shared tokens, both pass, and the paper tests
sleep twice (tests 2 and 4 shipped exactly that pair). Under the tags both read
`睡眠・健康` and the collision is a lookup instead of a judgement.

**What the sampler enforces.** `check_pool_themes()` **fails** on any themed
entry that is a bare string, lacks a `theme`, or carries a value outside
`THEMES` — `expand_pools.py` and `promote_adjunct.py` still append bare strings,
so without a hard stop the tagging rots silently the first time either runs.
After the draw, `check_theme_spread()` **warns** when one theme takes more than
`THEME_CAP` entries (reading 2, listening 5). The caps sit above the expected
count on purpose; see the comment on `THEME_CAP` before retuning them.

**`THEME_CAP` is the machine half of `web-topic-research` rule 3.** The two
numbers are one decision recorded in two places: change either the constants
here or that rule's text, and change the other in the same pass. The
**asymmetry is deliberate** — rule 3 says a *third* reading surface on one theme
is a defect, while `check_theme_spread()` only WARNs at the same threshold. The
sampler cannot see which entry the author will map to which 問題, so it flags
the risk and the reviewer decides. Do **not** "fix" the mismatch by hardening
the WARN to a failure or by softening the prose to match the gate; the split
is the point.

**Scoped by surface prominence, not by origin.** A paper authors 12 reading +
21 listening surfaces = 33, against a 20-value vocabulary, so a flat "at most
one surface per theme" is *arithmetically impossible* and must not be written as
a gate. `web-topic-research` scopes it by **prominence** instead: five headline
surfaces (問題9 cloze, 問題12 A/B as one, 問題13 長文, 問題14 flyer, 聴解問題5)
must carry five different themes; a headline theme appears nowhere else in the
読解 half; everything else falls under the caps above; and across tests, no theme
headlines two consecutive papers. **That rule binds pool-origin and web-origin
surfaces alike.** Scoping it by origin instead would exempt an offline all-pool
paper from the theme rule entirely — and the pool draw is exactly where the
lopsidedness bites (`働き方` is 44 of 240 listening scenarios), so a pool-origin
問題13 beside a web-origin 問題9 on one theme is precisely the collision the tags
exist to catch. `web-topic-research` owns that rule's text; this file owns
`THEMES` and `THEME_CAP`.

Known residue (audited 2026-08-06): the themed pools are themselves lopsided —
`働き方` holds 44 of 240 listening scenarios and `科学・技術` only 2; reading is
flatter (23 max, 2 min). A draw therefore spreads worse than the vocabulary
suggests. Even the pools out when growing them rather than raising `THEME_CAP`.

## Rotation is proved in the spec, not promised in a constant

Test 4 redrew six items test 1 had already used (妥協・解消・〜ざるを得ない・
〜次第・〜をはじめ・〜ようがない). The root cause was **not** a broken filter: the
paper was sampled by the v1 sampler (`d53bcef`), whose `draw()` took a flat
`used` list and **cleared the whole category's history the moment a pool ran
short**. The v2 LRU cooldown that replaces it (`020b442`) does exclude all six —
replaying test 4's draw against test 1's ledger entry puts every one at `ago=0`.

Two things were still wrong, and both are fixed:

- **The number enforced was not the number documented.** `ago(x) > cool` at
  `cool = COOLDOWN = 2` excluded the last **three** draws, not two. It is now
  `ago(x) >= cool`, so `COOLDOWN = 2` means exactly "used in either of the last
  two ledger entries". `apply_adjunct` uses the same test.
- **Relaxation was invisible.** A thin pool drops the cooldown a step at a time
  and, at the bottom, draws with none — printing a line and nothing else. The
  level actually applied is now returned by `draw()` and **written into the
  spec**, so a paper drawn without rotation says so in a file rather than in a
  console nobody kept.

Every `tests/<test_id>/test_spec.json` therefore carries:

```json
"rotation": {
  "recency_source": "ledger",
  "history_len": 2,
  "cooldown": 2
}
```

| key | meaning |
|---|---|
| `recency_source` | always `"ledger"` — the exclusion was computed from `logs/ledger.json`. A future non-ledger source gets a different value; a spec without this key was written by a sampler that had no rotation. |
| `history_len` | how many **other tests'** draws the recency map covered (this test's own ledger entry is excluded). `0` means nothing was available to rotate against, so the draw proves nothing. |
| `cooldown` | the **weakest** level actually applied to any category: `COOLDOWN` normally, lower when a thin pool forced relaxation, `0` when a pool exhausted its rotation entirely. Read it as "no item in this paper appears in the last `cooldown` ledger entries". |

`assert_rotation()` re-checks that claim against the ledger before the spec is
written, comparing on both the raw string and `head()`. **A red line there means
`draw()` is broken — never lower `COOLDOWN` to make it green.**

## Answer positions are balanced across sections, not only inside them

Test 4 landed 31 keys on position 1 and 17 on position 4 across the 90
four-choice items. Nothing was random about it. Each section was built as
`[(i % width) + 1 …]`, which is even *within* a section but always hands the
`count % 4` remainder to the lowest positions; summed over the 18 four-choice
sections that is a structural +15 / +7 / +4 / +0 on positions 1/2/3/4.

`balanced_position_plan()` keeps the floor allocation per section (so no section
is itself lopsided) and gives each section's remainder to whichever positions
are furthest behind **paper-wide**. Realised totals land at 22/23/23/22.

```python
POSITION_BAND = (19, 27)   # each of 1-4, over the 90 four-choice items
```

**The band is PROVISIONAL.** 90/4 = 22.5 and ±4 is a working tolerance, not a
measurement; a parallel pass is measuring the real spread of the official papers
from `refs/JLPT_N2_NEW`'s answer-key PDF. If that disagrees, **change the two
numbers** — the algorithm does not care what they are — and do not reinterpret
the band to fit a draw. The sampler exits rather than emit a plan outside it.
聴解 問題4 (11 items, 3 choices) is balanced section-locally as before; it is not
part of the 90.

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
  cooldown relaxes one step at a time, says so, **and the level it settled on
  is written into the spec** — see §"Rotation is proved in the spec". The old
  behaviour cleared the *entire* history when a pool ran out, which let an item
  from the immediately-previous test reappear in the next one.
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

`tests/<test_id>/test_spec.json` is the authoring contract. It contains, per section, the
exact items to test (e.g., `"grammar_p7": ["〜に反して", "〜どころか", …]`),
the scenario list for listening, topics for reading, and the answer-position
sequence per 問題.

**It belongs to ONE test and may predate the current `DRAW`.** The spec on disk
is whatever the last `sample_items.py --test-id <id>` run wrote to
`tests/<test_id>/test_spec.json`, so after a format fix its cardinalities can
differ from the code's.
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

