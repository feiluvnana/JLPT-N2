#!/usr/bin/env python3
"""
Sample a randomized test blueprint from the N2 item pools.

Usage:
    python sample_items.py --test-id 4 --seed 20260803
    python sample_items.py --test-id 4 --reroll grammar_p7 --seed 99999

Outputs tests/<test_id>/test_spec.json (the authoring contract) and updates
ledger.json (v2 LRU cooldown: an item drawn within the last N draws is
ineligible, where N is PER-CATEGORY — long relative to how deep that
category's own pool is, see `cooldown_for()` — not a single flat constant;
when a pool cannot fill a draw the cooldown relaxes one step at a time and
says so — history is never reset). Once the cooldown window has excluded the
recently-used items, the pick among what remains is WEIGHTED by recency too
(`weighted_sample_no_replacement()`), not uniform — an item that cleared the
cooldown a moment ago is still less likely to be drawn than one unused for
much longer, so a draw does not cluster right at the cooldown boundary.
"""

import argparse
import itertools
import json
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOLS = HERE.parent / "references" / "pools.json"
ROOT = HERE.parents[2]
LOGS_DIR = ROOT / "logs"
LEDGER = LOGS_DIR / "ledger.json"
STAGING = LOGS_DIR / "adjunct_staging.json"

sys.path.insert(0, str(HERE))
from level_data import (  # noqa: E402
    THEMED_CATS, THEMES, entry_text as item_text, entry_theme,
)

ADJUNCT_CAP = 0.20  # max share of each category draw filled from staging

# R13: how many entries of one theme a single draw may hold before the mix is
# too narrow to give every 問題 its own subject. Warn, don't fail: the author
# maps scenarios to 問題, so only they can see whether two same-theme entries
# actually collide.
#
# The LISTENING cap is set ABOVE the expected count so the warning means
# "unusually concentrated", not "the pool is uneven": 働き方 holds 44/240
# listening entries -> 3.9 expected in a 21-draw, so a cap of 3 would fire on
# nearly every seed and be ignored within two tests. Re-derive it if the pool
# balance changes.
#
# READING is 1, and it is a floor the draw itself now meets rather than a
# warning the author is left to act on: every 読解 surface must sit on its own
# theme (`exam-blueprint` rule 3, `question-authoring/references/dokkai.md`
# §"Thirteen surfaces, thirteen different essays"). 20260810_1 shipped five
# workplace-institution reading surfaces under the old cap of 2 — the cap held
# on the draw and the paper still read as one essay repeated, because the cloze
# and the web seeds were never counted. The arithmetic works: 19 of the 20
# themes carry reading entries (行政・手続き carries none) against a 12-topic
# draw, so distinctness leaves 7 themes spare.
THEME_CAP = {"reading_topics": 1, "listening_scenarios": 5}

# Categories whose draw must hold at most one entry per theme, enforced during
# the draw by `sample_distinct_theme()` rather than warned about afterwards.
DISTINCT_THEME_CATS = {"reading_topics"}

# Target per-ITEM probability that a 問題5/6 draw slot is a katakana
# headword, enforced during the draw by `sample_katakana_capped()`.
# Measured against the 7 current-era sittings
# (`question-authoring/references/official_calibration.md` §12): the archive
# draws a katakana HEADWORD in only 3/35 (問題5, 8.6%) and 1/35 (問題6, 2.9%)
# items — never more than one per section in the same paper. `pools.json`'s
# `paraphrase` is 27.1% katakana-containing and `usage` is 32.7%; a plain
# `rng.sample()` reproduces that composition (~1.4 and ~1.6 expected katakana
# items per 5-draw) instead of the archive's near-zero norm. Three generated
# papers checked before this existed drew 3, 3 and 6 combined katakana
# headwords per paper against an official average of 0.57. These are the
# measured item-level rates, not the pool's native share — do not replace them
# with `len(katakana)/len(pool)` if the pool composition changes; re-measure
# the archive instead.
KATAKANA_TARGET_RATE = {"paraphrase": 3 / 35, "usage": 1 / 35}
KATAKANA_CAP = {"paraphrase": 1, "usage": 1}  # never observed 2 in one section


def is_katakana_headword(entry) -> bool:
    """True if the pool entry's headword (gloss stripped) is a katakana word.

    `head()` already strips the disambiguating `(...)`/`（...）` gloss —
    `怠る(サボる/なまける)`'s headword is `怠る`, not katakana, even though the
    gloss names a katakana synonym. Matches on any katakana character, same
    test used to measure the archive rate in official_calibration.md §12.
    """
    return bool(re.search(r"[゠-ヿ]", head(item_text(entry))))


def weighted_sample_no_replacement(rng: random.Random, items: list,
                                   weights: list[float], n: int) -> list:
    """Weighted sample of `n` items from `items`, no replacement.

    Efraimidis-Spirakis A-Res: give each item a key `u ** (1/w)` for
    `u ~ Uniform(0,1)`, keep the top-`n` keys. This is what lets `draw()`
    do more than exclude the cooldown window and then pick uniformly among
    what is left — heavier weight (a larger `ago`, i.e. longer since last
    use, or never used) makes an item more likely to win, so a draw does not
    cluster right at the cooldown boundary the instant an item clears it.
    `n` may equal `len(items)` — this then returns every item, weighted-shuffled
    (`sample_distinct_theme` relies on exactly that to order its greedy pass).
    """
    keyed = sorted(
        ((rng.random() ** (1.0 / w), it) for it, w in zip(items, weights)),
        key=lambda kv: kv[0], reverse=True,
    )
    return [it for _, it in keyed[:n]]


def sample_katakana_capped(rng: random.Random, eligible: list, n: int,
                           target_rate: float, cap: int, name: str,
                           weight_fn=None) -> list:
    """`n` entries whose katakana-headword count matches the archive's rate.

    §12's archive rate is near-zero per paper (0 in most sittings, 1 in a
    minority, never 2+ in one section) — a fixed quota that forces exactly
    `cap` katakana items every draw, or that only trims the pool's native ~30%
    share down to `cap` without lowering how OFTEN a katakana item appears at
    all, both reproduce a shape the archive doesn't have. So: run `n`
    independent Bernoulli(target_rate) trials to decide how many katakana
    slots this draw gets (capped at `cap`), then fill that many from the
    katakana subset and the rest from the non-katakana subset.

    `weight_fn`, when given, picks each subset by recency weight (see
    `weighted_sample_no_replacement`) instead of uniformly.
    """
    kata = [e for e in eligible if is_katakana_headword(e)]
    plain = [e for e in eligible if not is_katakana_headword(e)]
    k = min(cap, len(kata), sum(rng.random() < target_rate for _ in range(n)))

    def pick(pool: list, count: int) -> list:
        if count <= 0:
            return []
        if weight_fn:
            return weighted_sample_no_replacement(
                rng, pool, [weight_fn(e) for e in pool], count)
        return rng.sample(pool, count)

    if len(plain) < n - k:
        print(f"  warning: pool '{name}' has too few non-katakana entries "
              f"({len(plain)}) to fill {n - k} of {n} slots — falling back "
              f"to an uncapped draw; grow the non-katakana side of this pool")
        return pick(eligible, n)
    picked = pick(plain, n - k) + pick(kata, k)
    rng.shuffle(picked)
    return picked

# category -> items drawn per test (N2)
DRAW = {
    "kanji_reading": 5,
    "orthography": 5,
    "word_formation": 3,
    "context_words": 7,
    "paraphrase": 5,
    "usage": 5,
    "grammar_p7": 12,
    "grammar_p8": 5,
    "quick_response": 11,
    # 5+6+5 scored items + 例×3 + 統合2 = 21. This was 19 (and 20 before that):
    # the 統合 term was in the comment but never in the value, so 問題5's two
    # items got no sampled scenario and the author had to invent one.
    "listening_scenarios": 21,   # 5+6+5 items + 例×3 + 統合2 (author maps them)
    "reading_topics": 12,        # 5 short + 4 medium + 1 A/B + 1 long + 1 info
}

# answer-position plans: (section, count, positions)
ANSWER_SECTIONS = [
    ("問題1_語彙", 5, 4), ("問題2_語彙", 5, 4), ("問題3_語彙", 3, 4),
    ("問題4_語彙", 7, 4), ("問題5_語彙", 5, 4), ("問題6_語彙", 5, 4),
    ("問題7", 12, 4), ("問題8", 5, 4), ("問題9", 4, 4),
    ("問題10", 5, 4), ("問題11", 8, 4), ("問題12", 2, 4),
    ("問題13", 3, 4), ("問題14", 2, 4),
    ("聴解_問題1", 5, 4), ("聴解_問題2", 6, 4), ("聴解_問題3", 5, 4),
    ("聴解_問題4", 11, 3), ("聴解_問題5", 3, 4),
]


# R17: per-section evenness is not paper-level evenness. The old plan built
# each section as [(i % width) + 1 ...], so every section's REMAINDER always
# landed on the lowest positions: summed over the 18 four-choice sections that
# is +15 on position 1, +7 on 2, +4 on 3, +0 on 4, and a paper has shipped 31
# keys on position 1 against 17 on position 4. The remainders are now
# allocated across sections instead of inside them.
#
# PROVISIONAL BAND — retune, don't reinterpret. 90 four-choice items / 4 = 22.5,
# and ±4 is the working tolerance until the measured spread of the official
# papers (refs/JLPT_N2_NEW answer keys) replaces it. If that measurement
# disagrees, change these two numbers; the algorithm does not care what they are.
POSITION_BAND = (19, 27)


def shuffle_no_triple(rng: random.Random, base: list[int], name: str) -> list[int]:
    """Shuffle `base` until no position repeats three times in a row."""
    base = list(base)
    if len(set(base)) < 2 and len(base) >= 3:
        # No arrangement can satisfy the no-3-in-a-row rule; fail loudly rather
        # than spin forever in the shuffle loop.
        sys.exit(f"shuffle_no_triple: impossible constraint for {name} "
                 f"({len(base)} items over {len(set(base))} position(s))")
    for _ in range(10_000):
        rng.shuffle(base)
        if all(not (base[i] == base[i + 1] == base[i + 2])
               for i in range(len(base) - 2)):
            return base
    sys.exit(f"shuffle_no_triple: no valid arrangement after 10000 shuffles "
             f"for {name} ({len(base)} items)")


def balanced_positions(rng: random.Random, count: int, width: int) -> list[int]:
    """Near-uniform distribution over 1..width, never 3 identical in a row.

    Section-local: used for the width-3 section (聴解 問題4), which does not
    take part in the cross-section balancing below.
    """
    return shuffle_no_triple(rng, [(i % width) + 1 for i in range(count)],
                             f"{count}x{width}")


def balanced_position_plan(rng: random.Random,
                           sections: list[tuple[str, int, int]]
                           ) -> tuple[dict[str, list[int]], dict[int, int]]:
    """Answer positions for every section, balanced ACROSS the four-choice ones.

    Each section still gets floor(count/4) of every position, so no section is
    itself lopsided; only the leftover `count % 4` slots are contested, and they
    go to whichever positions are furthest behind paper-wide. Returns the plan
    and the realised per-position totals over the four-choice items.
    """
    quad = [s for s in sections if s[2] == 4]
    total = sum(c for _, c, _ in quad)
    lo, hi = POSITION_BAND
    alloc: dict[str, list[int]] = {}
    running: dict[int, int] = {}
    for _ in range(200):
        running = {p: 0 for p in (1, 2, 3, 4)}
        alloc = {}
        for name, count, _w in sorted(quad, key=lambda s: -s[1]):
            base, rem = divmod(count, 4)
            for p in running:
                running[p] += base
            # remainder -> the positions with the smallest running total,
            # ties broken randomly so the plan is not the same every seed
            extras = sorted((1, 2, 3, 4),
                            key=lambda p: (running[p], rng.random()))[:rem]
            for p in extras:
                running[p] += 1
            alloc[name] = [p for p in (1, 2, 3, 4)
                           for _ in range(base + (1 if p in extras else 0))]
        if all(lo <= running[p] <= hi for p in running):
            break
    else:
        sys.exit(f"balanced_position_plan: cannot keep all four positions "
                 f"inside {POSITION_BAND} over {total} four-choice items "
                 f"(got {running}) — the section table changed; retune "
                 f"POSITION_BAND or the section counts")

    plan = {}
    for name, count, width in sections:
        base = alloc[name] if width == 4 else [(i % width) + 1
                                               for i in range(count)]
        assert len(base) == count, (name, len(base), count)
        plan[name] = shuffle_no_triple(rng, base, name)
    return plan, running


# --- Ledger (v2): draw history, newest last ------------------------------
# v1 was a flat {category: [used items]} with an all-or-nothing reset — when a
# pool ran out, the ENTIRE history cleared, so an item from the immediately
# previous test could reappear in the very next one. v2 keeps per-draw history
# so rotation is LRU (least-recently-used) and degrades smoothly instead of
# resetting, and so each item can be attributed to the test that used it.

COOLDOWN_FLOOR = 2   # minimum cooldown even for the thinnest pool
COOLDOWN_MARGIN = 2  # draws of headroom left below full pool exhaustion, so
                     # the existing "relax one step when tight" path below
                     # still has room to degrade smoothly instead of jumping
                     # straight from a long cooldown to 0


def cooldown_for(cat: str, pool_size: int) -> int:
    """How many previous draws make an item in `cat` ineligible.

    A single flat COOLDOWN=2 protected every category as weakly as the
    thinnest one: word_formation's 85-entry pool (3 drawn/test, ~28 tests to
    exhaust) rotated no better than grammar_p8's 42-entry pool (5/test, ~8
    tests to exhaust) — proven when `〜好き(猫好き)` and `〜化(簡素化)` each
    repeated within 4-5 tests despite a pool deep enough to go ~28 tests
    without a repeat. Scale the window to each pool's OWN depth instead of a
    constant: a rich pool remembers for a long time, a tight one for less,
    and COOLDOWN_MARGIN keeps every pool's window a little short of full
    exhaustion so it can still relax gracefully (see `draw()`) rather than
    jump straight to cool=0 the moment the pool grows by a handful of items.
    """
    n = DRAW[cat]
    depth = pool_size // n if n else 0
    return max(COOLDOWN_FLOOR, depth - COOLDOWN_MARGIN)


def load_staging_ready() -> dict[str, list[dict]]:
    """category -> staging rows with status=ready and level=N2."""
    if not STAGING.is_file():
        return {}
    data = json.loads(STAGING.read_text(encoding="utf-8"))
    by_cat: dict[str, list[dict]] = {}
    for e in data.get("entries", []):
        if e.get("status") != "ready" or e.get("level") != "N2":
            continue
        cat = e.get("category")
        if cat:
            by_cat.setdefault(cat, []).append(e)
    return by_cat


def apply_adjunct(rng: random.Random, cat: str, picked: list,
                  staging_by_cat: dict[str, list[dict]], taken: set,
                  recency: dict, cool_max: int) -> list:
    """Replace up to ADJUNCT_CAP of pool draws with staged N2 adjunct items."""
    n = len(picked)
    cap = int(n * ADJUNCT_CAP)
    if cap < 1:
        return picked
    pool = staging_by_cat.get(cat, [])
    if not pool:
        return picked

    inf = 10 ** 9

    def ago(x: str) -> int:
        return min(recency.get(x, inf), recency.get(head(x), inf))

    eligible = []
    for e in pool:
        it = e.get("item", "")
        if not it or it in taken or head(it) in {head(t) for t in taken}:
            continue
        if ago(it) < cool_max:      # used within this category's cooldown
            continue
        eligible.append(e)
    if not eligible:
        return picked

    rng.shuffle(eligible)
    replace_n = min(cap, len(eligible))
    result = list(picked[: n - replace_n])
    for e in eligible[:replace_n]:
        result.append({
            "item": e["item"],
            "origin": "adjunct",
            "level": "N2",
            "evidence": e.get("evidence", []),
        })
        taken.add(e["item"])
    print(f"  note: {cat} used {replace_n} adjunct item(s) from staging")
    return result


def load_ledger() -> dict:
    if not LEDGER.exists():
        return {"version": 2, "history": []}
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    if data.get("version") == 2:
        return data
    # migrate v1 flat lists -> one synthetic oldest draw
    legacy = {k: v for k, v in data.items() if isinstance(v, list)}
    print("  note: migrating ledger v1 -> v2 (history-based LRU rotation)")
    return {"version": 2,
            "history": [{"test_id": "legacy", "seed": None,
                         "generated_at": None, "items": legacy}] if legacy else []}


def head(item: str) -> str:
    """Normalized identity of a pool entry, ignoring the disambiguating gloss.

    Pools spell the same word differently per category — 「あらかじめ」 in
    context_words, 「あらかじめ(前もって)」 in paraphrase — so a raw string
    comparison misses cross-category repeats.
    """
    return str(item).split("(")[0].split("（")[0].strip()


def recency_map(history: list) -> dict:
    """item -> how many draws ago it was last used (0 = most recent draw).

    Recency is tracked BY WORD, ACROSS CATEGORIES, not per category. Pools
    overlap on purpose (41 words are both context_words and usage items), and
    a category-local map let 「あらかじめ」 be tested in one paper's 問題4 and
    again in the next paper's 問題5 — consecutive papers testing the same word,
    with every gate green. `taken` stops that inside one test; this stops it
    across tests.
    Keys are both the raw string and its head(), so either spelling matches.
    """
    rec: dict = {}
    for ago, entry in enumerate(reversed(history)):
        for items in entry.get("items", {}).values():
            for item in items:
                t = item_text(item)
                rec.setdefault(t, ago)
                rec.setdefault(head(t), ago)
    return rec


def sample_distinct_theme(rng: random.Random, eligible: list, n: int,
                          name: str, weight_fn=None) -> list | None:
    """`n` entries, no two sharing a theme. None when the pool cannot.

    Greedy over a shuffle, which is uniform enough for this purpose and, unlike
    rejection sampling over `rng.sample`, terminates: the caller only needs SOME
    theme-distinct draw, not a uniformly-random one among all such draws.
    Untagged entries are treated as one shared theme so a category that lost its
    tags degrades to "one untagged entry", never to "distinctness is vacuous".

    `weight_fn`, when given, orders the shuffle by recency weight (see
    `weighted_sample_no_replacement`) so the greedy pass still favors
    longer-unused entries, not just a plain shuffle.
    """
    if weight_fn:
        shuffled = weighted_sample_no_replacement(
            rng, eligible, [weight_fn(e) for e in eligible], len(eligible))
    else:
        shuffled = list(eligible)
        rng.shuffle(shuffled)
    picked, used = [], set()
    for e in shuffled:
        th = entry_theme(e) or ""
        if th in used:
            continue
        picked.append(e)
        used.add(th)
        if len(picked) == n:
            return picked
    print(f"  warning: pool '{name}' cannot fill {n} distinct themes "
          f"({len(picked)} available) — falling back to a themed draw; grow "
          f"the thin themes rather than relaxing the rule")
    return None


def draw(rng: random.Random, pool: list, recency: dict, n: int,
         name: str, taken: set, cool_max: int) -> tuple[list, int]:
    """LRU draw. Returns (picked, cooldown_actually_applied).

    `cool_max` is this category's own cooldown ceiling (`cooldown_for()`) —
    a number of PREVIOUS DRAWS: at cool=cool_max nothing used in the last
    cool_max ledger entries can be drawn (ago 0 .. cool_max-1 excluded),
    which is what the docstring, the SKILL and `rotation.cooldown` all promise.
    The old test was `ago(x) > cool`, i.e. one draw stricter than documented —
    harmless in itself, but it meant the number written into the spec was not
    the number enforced, and a gate cannot check a promise nobody records.

    Relaxation is not silent any more either. cool=0 is the old "last resort"
    (no recency filter at all) and it is a value the caller RETURNS and records,
    so a paper drawn without rotation says so in its own spec instead of only
    in a console line nobody kept.
    """
    if len(pool) < 2.5 * n:
        print(f"  warning: pool '{name}' is thin ({len(pool)} for draws of {n}) "
              f"— consider adding items from the reference books")
    inf = 10 ** 9

    def ago(x) -> int:
        t = item_text(x)
        return min(recency.get(t, inf), recency.get(head(t), inf))

    def weight(x) -> float:
        # +1 so an item sitting right at the cooldown boundary (ago == cool,
        # the minimum eligible) never gets a zero/negative weight; everything
        # past that is weighted by how much LONGER it's gone unused, so a
        # draw does not cluster right at the boundary the moment it clears.
        return float(ago(x)) + 1.0

    for cool in range(cool_max, -1, -1):
        eligible = [x for x in pool
                    if item_text(x) not in taken and ago(x) >= cool]
        if len(eligible) >= n:
            if cool == 0:
                print(f"  WARNING: pool '{name}' exhausted its rotation — "
                      f"drawing with NO cooldown. Grow this pool.")
            elif cool < cool_max:
                print(f"  note: pool '{name}' is tight — cooldown relaxed to "
                      f"{cool} draw(s) (of {cool_max}); consider growing the pool")
            if name in DISTINCT_THEME_CATS:
                picked = sample_distinct_theme(rng, eligible, n, name,
                                               weight_fn=weight)
                if picked is not None:
                    return picked, cool
            if name in KATAKANA_CAP:
                return sample_katakana_capped(
                    rng, eligible, n, KATAKANA_TARGET_RATE[name],
                    KATAKANA_CAP[name], name, weight_fn=weight), cool
            return weighted_sample_no_replacement(
                rng, eligible, [weight(x) for x in eligible], n), cool
    remaining = len([x for x in pool if item_text(x) not in taken])
    sys.exit(f"pool '{name}' cannot supply {n} distinct items "
             f"({remaining} available after cross-category exclusion)")


COMMON_DOMAINS = [
    "会社", "大学", "病院", "不動産", "旅行", "市役所", "区役所", "図書館",
    "引っ越し", "ホテル", "アルバイト", "ジム", "駅", "美術館", "学校", "スーパー",
    "レストラン", "カフェ", "公園", "警察", "消防", "郵便局", "銀行", "防災",
]


def extract_domain(text: str) -> str:
    """Extract domain prefix or key entity from a scenario/topic string."""
    t = item_text(text)
    if ":" in t:
        return t.split(":")[0].strip()
    if "：" in t:
        return t.split("：")[0].strip()
    for d in COMMON_DOMAINS:
        if d in t:
            return d
    return ""


def check_domain_collisions(scenarios: list) -> list[str]:
    """Find pairs of scenarios sharing the same domain prefix/entity."""
    warnings = []
    seen: dict[str, list[str]] = {}
    for item in scenarios:
        d = extract_domain(item)
        if d:
            seen.setdefault(d, []).append(item_text(item))
    for dom, items in seen.items():
        if len(items) > 1:
            warnings.append(f"domain '{dom}': {items}")
    return warnings


def check_pool_themes(pools: dict) -> None:
    """R13: every themed pool entry carries a theme from the CLOSED vocabulary.

    Hard failure, not a warning. `expand_pools.py` and `promote_adjunct.py`
    still append bare strings to these categories, so without this the theme
    coverage silently rots the first time either runs, and the cross-test theme
    comparison the tags exist for goes quiet instead of red.
    """
    bad = []
    for cat, key in THEMED_CATS.items():
        for e in pools.get(cat, []):
            if not isinstance(e, dict) or not e.get(key):
                bad.append(f"{cat}: {e!r} is not {{'{key}': …, 'theme': …}}")
            elif e.get("theme") not in THEMES:
                bad.append(f"{cat}: 「{e[key]}」 theme={e.get('theme')!r}")
    if bad:
        sys.exit("pools.json themed entries are broken:\n  " +
                 "\n  ".join(bad) +
                 f"\n  valid themes: {', '.join(THEMES)}"
                 "\n  (exam-blueprint/SKILL.md §'Topic themes' — tag the "
                 "entry, never widen the vocabulary to fit it)")


def check_theme_spread(picked: list, cat: str) -> list[str]:
    """Warn when one theme takes too much of a themed draw.

    Surface strings cannot see that 「交替制勤務と睡眠の質」 and 「就寝前の刺激と
    生活習慣」 are one subject; the tags can. The sampler does not know which
    entry the author will map to which 問題, so this warns rather than rerolls.
    """
    cap = THEME_CAP.get(cat)
    if not cap:
        return []
    counts: dict[str, list[str]] = {}
    for e in picked:
        th = entry_theme(e)
        if th:
            counts.setdefault(th, []).append(item_text(e))
    return [f"theme '{th}' x{len(xs)} (cap {cap}): {xs}"
            for th, xs in counts.items() if len(xs) > cap]


def assert_rotation(spec_items: dict, history: list, cooldown: int) -> None:
    """R10 proof: nothing drawn may appear in the last `cooldown` ledger draws.

    The filter lives in draw(); this is the independent re-check, in the same
    spirit as the same-test collision assertion below. It compares on both the
    raw text and head(), which is how recency_map keys them.
    """
    if cooldown <= 0 or not history:
        return
    recent: dict[str, str] = {}
    for entry in history[-cooldown:]:
        tid = str(entry.get("test_id"))
        for xs in entry.get("items", {}).values():
            for x in xs:
                t = item_text(x)
                recent.setdefault(t, tid)
                recent.setdefault(head(t), tid)
    clashes = []
    for cat, xs in spec_items.items():
        for x in xs:
            t = item_text(x)
            tid = recent.get(t) or recent.get(head(t))
            if tid:
                clashes.append(f"{cat}:「{t}」 (test {tid})")
    if clashes:
        sys.exit(f"rotation broken: {len(clashes)} item(s) drawn inside the "
                 f"{cooldown}-draw cooldown: {'; '.join(clashes)} — this is a "
                 f"bug in draw(), not a reason to lower cooldown_for()")


def check_pool_depths(pools: dict) -> None:
    """Report pool sizes and headroom multipliers against draw requirements."""
    print("Pool Depth Health Check:")
    for cat, n in DRAW.items():
        size = len(pools.get(cat, []))
        ratio = size / n if n > 0 else 0
        status = "OK" if ratio >= 2.5 else "THIN"
        print(f"  [{status:4s}] {cat:20s}: {size:4d} items / {n:2d} draw ({ratio:5.1f}x headroom)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--reroll", default=None,
                    help="resample only this category, keep the rest")
    ap.add_argument("--test-id", required=True,
                    help="test id; writes tests/<test_id>/test_spec.json and "
                         "records ledger attribution")
    ap.add_argument("--no-adjunct", action="store_true",
                    help="pure pool draw; ignore logs/adjunct_staging.json")
    ap.add_argument("--check-depth", action="store_true",
                    help="check pool sizes and headroom multipliers without sampling")
    args = ap.parse_args()

    pools = json.loads(POOLS.read_text(encoding="utf-8"))
    check_pool_themes(pools)

    if args.check_depth:
        check_pool_depths(pools)
        return

    seed = args.seed if args.seed is not None else int(time.time())
    rng = random.Random(seed)
    spec_path = ROOT / "tests" / str(args.test_id) / "test_spec.json"

    ledger = load_ledger()
    history = ledger["history"]
    staging_by_cat = {} if args.no_adjunct else load_staging_ready()
    recency = recency_map(history)

    if args.reroll:
        cat = args.reroll
        if cat not in DRAW:
            sys.exit(f"unknown category '{cat}'. Valid: {', '.join(DRAW)}")
        if cat not in pools:
            sys.exit(f"category '{cat}' is in DRAW but missing from pools.json")
        if not spec_path.is_file():
            sys.exit(f"--reroll needs an existing {spec_path.relative_to(ROOT)}")
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        # Find THIS test's ledger entry by id — it is not necessarily the newest
        # one. An earlier test has been rerolled after a later test already
        # existed, and writing to history[-1] put the earlier test's picks into
        # the later test's entry, which then failed assert_rotation against
        # them. Drop this category from the entry so its own picks are not
        # counted against the redraw, and exclude everything the other
        # categories already hold.
        own_entry = None
        for e in reversed(history):
            if (str(e.get("test_id")) == str(spec.get("test_id")) or
                    str(e.get("seed")) == str(spec.get("seed"))):
                own_entry = e
                break
        if own_entry is not None:
            own_entry.setdefault("items", {}).pop(cat, None)
        taken_text = {item_text(x) for c, xs in spec["items"].items()
                      if c != cat for x in xs}
        updated_recency = recency_map(history)
        cool_max = cooldown_for(cat, len(pools[cat]))
        picked, cool = draw(rng, pools[cat], updated_recency,
                            DRAW[cat], cat, taken_text, cool_max)
        if staging_by_cat:
            picked = apply_adjunct(rng, cat, picked, staging_by_cat,
                                   taken_text, updated_recency, cool_max)
        spec["items"][cat] = picked
        spec["seed"] = f"{spec.get('seed')}+reroll({cat},{seed})"
        spec["rotation"] = {
            "recency_source": "ledger",
            "history_len": 0,          # filled in below, once this test's own
                                       # entry can be told from the others
            # a reroll can only make the paper's weakest cooldown weaker
            "cooldown": min(cool, spec.get("rotation", {}).get("cooldown", cool)),
        }
        if own_entry is not None:
            own_entry.setdefault("items", {})[cat] = picked
            own_entry["seed"] = spec["seed"]
        for w in check_theme_spread(picked, cat):
            print(f"  WARNING: {cat} draw is theme-heavy — {w}")
        # Only THIS category was freshly drawn — against "now" (the full
        # ledger's current end, via updated_recency above). Every other
        # category in spec["items"] is untouched, drawn at some earlier point
        # against whatever window existed then. Re-verifying the WHOLE spec
        # here compares old, already-valid picks against a "last cooldown
        # entries of right now" window that has nothing to do with when they
        # were drawn — for a test rerolled after later tests already exist,
        # that window is the tail of the ENTIRE ledger, not the entries that
        # preceded this test, and spuriously fails on categories the reroll
        # never touched (reproduces even at the old flat COOLDOWN=2). Verify
        # only what actually changed.
        rotation_check_items = {cat: picked}
    else:
        items = {}
        taken: set = set()          # cross-category: one item, one 問題 per test
        theme_warns: list[str] = []
        effective_cool = None
        for cat, n in DRAW.items():
            if cat not in pools:
                sys.exit(f"category '{cat}' is in DRAW but missing from pools.json")
            cool_max = cooldown_for(cat, len(pools[cat]))
            picked, cool = draw(rng, pools[cat], recency, n, cat, taken, cool_max)
            effective_cool = cool if effective_cool is None else min(effective_cool, cool)
            if staging_by_cat:
                picked = apply_adjunct(rng, cat, picked, staging_by_cat,
                                       taken, recency, cool_max)
            items[cat] = picked
            taken.update(item_text(x) for x in picked)
            theme_warns += [f"{cat}: {w}" for w in check_theme_spread(picked, cat)]
        positions, pos_totals = balanced_position_plan(rng, ANSWER_SECTIONS)
        spec = {
            "seed": seed,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_id": args.test_id,
            # R10: the rotation this draw actually enforced, so a gate can check
            # the paper against logs/ledger.json instead of trusting a constant.
            # cooldown is the WEAKEST level applied to any category (COOLDOWN
            # unless a thin pool forced relaxation; 0 = no rotation at all).
            "rotation": {
                "recency_source": "ledger",
                "history_len": len(history),
                "cooldown": effective_cool,
            },
            "items": items,
            "answer_positions": positions,
        }
        history.append({"test_id": args.test_id, "seed": seed,
                        "generated_at": spec["generated_at"], "items": items,
                        "draw": dict(DRAW)})
        print(f"  answer positions over the {sum(pos_totals.values())} "
              f"four-choice items: " +
              ", ".join(f"{p}x{pos_totals[p]}" for p in (1, 2, 3, 4)) +
              f"  (band {POSITION_BAND[0]}-{POSITION_BAND[1]})")
        for w in theme_warns:
            print(f"  WARNING: theme-heavy draw — {w}")
        # A fresh draw's entry sits at the true end of `history` (just
        # appended above), so every category in it was drawn against the same
        # "now" window — the whole spec is fair to re-verify at once.
        rotation_check_items = spec["items"]

    # Invariant: no item may be tested by two different 問題 in the same paper.
    collisions = {}
    for a, b in itertools.combinations(spec["items"], 2):
        both = {item_text(x) for x in spec["items"][a]} & {item_text(x) for x in spec["items"][b]}
        if both:
            collisions[f"{a} x {b}"] = sorted(both)
    if collisions:
        sys.exit(f"same-test collision (a bug in draw()): {collisions}")

    # R10: prove the cooldown the spec claims, against the ledger it claims it
    # from — everything recorded under a DIFFERENT test id. Do not reach for
    # history[-1] here: on the reroll path this test's entry can sit anywhere
    # in the list.
    prior_history = [h for h in history
                     if str(h.get("test_id")) != str(args.test_id)]
    spec["rotation"]["history_len"] = len(prior_history)
    assert_rotation(rotation_check_items, prior_history, spec["rotation"]["cooldown"])

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"seed={spec['seed']} -> {spec_path.relative_to(ROOT)} written, "
          f"ledger updated at {LEDGER.relative_to(ROOT)} "
          f"({len(history)} draw(s) recorded)")
    for cat, xs in spec["items"].items():
        rec = recency_map(history[:-1]) if history else {}
        reused = sum(1 for x in xs if item_text(x) in rec)
        print(f"  {cat}: {len(xs)} items ({len(xs) - reused} never used before)")

    # Same-domain scenario collision check
    scen_warns = check_domain_collisions(spec["items"].get("listening_scenarios", []))
    if scen_warns:
        print("\n  WARNING: listening_scenarios contains same-domain pair(s):")
        for w in scen_warns:
            print(f"    - {w}")
        print("  Consider --reroll listening_scenarios if two items share the same errand shape.")


if __name__ == "__main__":
    main()

