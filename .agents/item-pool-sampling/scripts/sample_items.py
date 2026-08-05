#!/usr/bin/env python3
"""
Sample a randomized test blueprint from the N2 item pools.

Usage:
    python sample_items.py                 # random seed
    python sample_items.py --seed 20260803 # reproducible
    python sample_items.py --reroll grammar_p7  # resample one category,
                                                # keep the rest of test_spec.json

Outputs test_spec.json (the authoring contract) and updates ledger.json
(v2 LRU cooldown: an item drawn within the last COOLDOWN draws is ineligible;
when a pool cannot fill a draw the cooldown relaxes one step at a time and
says so — history is never reset).
"""

import argparse
import itertools
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOLS = HERE.parent / "references" / "pools.json"
ROOT = HERE.parents[2]
LOGS_DIR = ROOT / "logs"
LEDGER = LOGS_DIR / "ledger.json"
SPEC = LOGS_DIR / "test_spec.json"
STAGING = LOGS_DIR / "adjunct_staging.json"

ADJUNCT_CAP = 0.20  # max share of each category draw filled from staging

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


def balanced_positions(rng: random.Random, count: int, width: int) -> list[int]:
    """Near-uniform distribution over 1..width, never 3 identical in a row."""
    base = [(i % width) + 1 for i in range(count)]
    if width < 2 and count >= 3:
        # No arrangement can satisfy the no-3-in-a-row rule; fail loudly rather
        # than spin forever in the shuffle loop.
        sys.exit(f"balanced_positions: impossible constraint "
                 f"(count={count}, width={width})")
    for _ in range(10_000):
        rng.shuffle(base)
        if all(not (base[i] == base[i + 1] == base[i + 2])
               for i in range(len(base) - 2)):
            return base
    sys.exit(f"balanced_positions: no valid arrangement after 10000 shuffles "
             f"(count={count}, width={width})")


# --- Ledger (v2): draw history, newest last ------------------------------
# v1 was a flat {category: [used items]} with an all-or-nothing reset — when a
# pool ran out, the ENTIRE history cleared, so an item from the immediately
# previous test could reappear in the very next one. v2 keeps per-draw history
# so rotation is LRU (least-recently-used) and degrades smoothly instead of
# resetting, and so each item can be attributed to the test that used it.

COOLDOWN = 2  # do not redraw an item used within this many previous draws


def item_text(entry) -> str:
    """Extract the testable string from a pool string or adjunct record."""
    if isinstance(entry, dict):
        return str(entry.get("item") or entry.get("topic") or entry.get("scenario") or "")
    return str(entry)


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
                  recency: dict) -> list:
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
        if ago(it) <= COOLDOWN:
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
    a category-local map let 「あらかじめ」 be tested in test 3's 問題4 and again
    in test 4's 問題5 — consecutive papers testing the same word, with every
    gate green. `taken` stops that inside one test; this stops it across tests.
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


def draw(rng: random.Random, pool: list[str], recency: dict, n: int,
         name: str, taken: set) -> list[str]:
    """LRU draw: prefer items not used within COOLDOWN draws, never reusing an
    item already taken by another category in THIS test."""
    if len(pool) < 2.5 * n:
        print(f"  warning: pool '{name}' is thin ({len(pool)} for draws of {n}) "
              f"— consider adding items from the reference books")
    inf = 10 ** 9

    def ago(x: str) -> int:
        return min(recency.get(x, inf), recency.get(head(x), inf))

    for cool in range(COOLDOWN, -1, -1):
        eligible = [x for x in pool if x not in taken and ago(x) > cool]
        if len(eligible) >= n:
            if cool < COOLDOWN:
                print(f"  note: pool '{name}' is tight — cooldown relaxed to "
                      f"{cool} draw(s); consider growing the pool")
            return rng.sample(eligible, n)
    # Last resort: ignore recency, still honour cross-category exclusion.
    fallback = [x for x in pool if x not in taken]
    if len(fallback) < n:
        sys.exit(f"pool '{name}' cannot supply {n} distinct items "
                 f"({len(fallback)} available after cross-category exclusion)")
    print(f"  WARNING: pool '{name}' exhausted its rotation — drawing with "
          f"no cooldown. Grow this pool.")
    return rng.sample(fallback, n)


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
    ap.add_argument("--test-id", default=None,
                    help="record which test consumed this draw (ledger attribution)")
    ap.add_argument("--no-adjunct", action="store_true",
                    help="pure pool draw; ignore logs/adjunct_staging.json")
    ap.add_argument("--check-depth", action="store_true",
                    help="check pool sizes and headroom multipliers without sampling")
    args = ap.parse_args()

    pools = json.loads(POOLS.read_text(encoding="utf-8"))

    if args.check_depth:
        check_pool_depths(pools)
        return

    seed = args.seed if args.seed is not None else int(time.time())
    rng = random.Random(seed)

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
        if not SPEC.exists():
            sys.exit("--reroll needs an existing test_spec.json")
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        # The current spec is the newest history entry; drop this category from
        # it so its own picks are not counted against the redraw, and exclude
        # everything the other categories already hold.
        if history:
            last_entry = history[-1]
            if (str(last_entry.get("seed")) == str(spec.get("seed")) or
                    last_entry.get("test_id") == spec.get("test_id")):
                last_entry.setdefault("items", {}).pop(cat, None)
        taken_text = {item_text(x) for c, xs in spec["items"].items()
                      if c != cat for x in xs}
        updated_recency = recency_map(history)
        picked = draw(rng, pools[cat], updated_recency,
                      DRAW[cat], cat, taken_text)
        if staging_by_cat:
            picked = apply_adjunct(rng, cat, picked, staging_by_cat,
                                   taken_text, updated_recency)
        spec["items"][cat] = picked
        spec["seed"] = f"{spec.get('seed')}+reroll({cat},{seed})"
        if history:
            history[-1].setdefault("items", {})[cat] = picked
            history[-1]["seed"] = spec["seed"]
    else:
        items = {}
        taken: set = set()          # cross-category: one item, one 問題 per test
        for cat, n in DRAW.items():
            if cat not in pools:
                sys.exit(f"category '{cat}' is in DRAW but missing from pools.json")
            picked = draw(rng, pools[cat], recency, n, cat, taken)
            if staging_by_cat:
                picked = apply_adjunct(rng, cat, picked, staging_by_cat,
                                       taken, recency)
            items[cat] = picked
            taken.update(item_text(x) for x in picked)
        spec = {
            "seed": seed,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_id": args.test_id,
            "items": items,
            "answer_positions": {
                name: balanced_positions(rng, count, width)
                for name, count, width in ANSWER_SECTIONS
            },
        }
        history.append({"test_id": args.test_id, "seed": seed,
                        "generated_at": spec["generated_at"], "items": items})

    # Invariant: no item may be tested by two different 問題 in the same paper.
    collisions = {}
    for a, b in itertools.combinations(spec["items"], 2):
        both = {item_text(x) for x in spec["items"][a]} & {item_text(x) for x in spec["items"][b]}
        if both:
            collisions[f"{a} x {b}"] = sorted(both)
    if collisions:
        sys.exit(f"same-test collision (a bug in draw()): {collisions}")

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"seed={spec['seed']} -> {SPEC.relative_to(ROOT)} written, "
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

