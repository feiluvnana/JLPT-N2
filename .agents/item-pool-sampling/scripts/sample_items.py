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

# category -> items drawn per test (N2)
DRAW = {
    "kanji_reading": 5,
    "orthography": 5,
    "word_formation": 5,
    "context_words": 7,
    "paraphrase": 5,
    "usage": 5,
    "grammar_p7": 12,
    "grammar_p8": 5,
    "quick_response": 12,
    "listening_scenarios": 20,   # 5+6+5 items + 例×3 + 統合3 (author maps them)
    "reading_topics": 11,        # 5 short + 3 medium + 1 A/B + 1 long + 1 info
}

# answer-position plans: (section, count, positions)
ANSWER_SECTIONS = [
    ("問題1_語彙", 5, 4), ("問題2_語彙", 5, 4), ("問題3_語彙", 5, 4),
    ("問題4_語彙", 7, 4), ("問題5_語彙", 5, 4), ("問題6_語彙", 5, 4),
    ("問題7", 12, 4), ("問題8", 5, 4), ("問題9", 5, 4),
    ("問題10", 5, 4), ("問題11", 9, 4), ("問題12", 2, 4),
    ("問題13", 3, 4), ("問題14", 2, 4),
    ("聴解_問題1", 5, 4), ("聴解_問題2", 6, 4), ("聴解_問題3", 5, 4),
    ("聴解_問題4", 12, 3), ("聴解_問題5", 4, 4),
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
                rec.setdefault(item, ago)
                rec.setdefault(head(item), ago)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--reroll", default=None,
                    help="resample only this category, keep the rest")
    ap.add_argument("--test-id", default=None,
                    help="record which test consumed this draw (ledger attribution)")
    args = ap.parse_args()

    seed = args.seed if args.seed is not None else int(time.time())
    rng = random.Random(seed)

    pools = json.loads(POOLS.read_text(encoding="utf-8"))
    ledger = load_ledger()
    history = ledger["history"]

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
        if history and history[-1].get("seed") == spec.get("seed"):
            history[-1]["items"].pop(cat, None)
        taken = {x for c, xs in spec["items"].items() if c != cat for x in xs}
        picked = draw(rng, pools[cat], recency_map(history),
                      DRAW[cat], cat, taken)
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
            picked = draw(rng, pools[cat], recency_map(history), n, cat, taken)
            items[cat] = picked
            taken.update(picked)
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
        both = set(map(str, spec["items"][a])) & set(map(str, spec["items"][b]))
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
        reused = sum(1 for x in xs if x in rec)
        print(f"  {cat}: {len(xs)} items ({len(xs) - reused} never used before)")


if __name__ == "__main__":
    main()
