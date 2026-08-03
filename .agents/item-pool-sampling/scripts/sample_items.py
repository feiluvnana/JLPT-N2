#!/usr/bin/env python3
"""
Sample a randomized test blueprint from the N2 item pools.

Usage:
    python sample_items.py                 # random seed
    python sample_items.py --seed 20260803 # reproducible
    python sample_items.py --reroll grammar_p7  # resample one category,
                                                # keep the rest of test_spec.json

Outputs test_spec.json (the authoring contract) and updates ledger.json
(items used by past tests — excluded from future draws until a pool is
exhausted, then that pool's history resets).
"""

import argparse
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
    while True:
        rng.shuffle(base)
        if all(not (base[i] == base[i + 1] == base[i + 2])
               for i in range(len(base) - 2)):
            return base


def draw(rng: random.Random, pool: list[str], used: list[str], n: int,
         name: str) -> tuple[list[str], list[str]]:
    fresh = [x for x in pool if x not in used]
    if len(fresh) < n:  # pool exhausted -> reset rotation for this category
        print(f"  note: pool '{name}' exhausted, resetting its rotation")
        used = []
        fresh = list(pool)
    if len(pool) < 2.5 * n:
        print(f"  warning: pool '{name}' is thin ({len(pool)} for draws of {n}) "
              f"— consider adding items from the reference books")
    picked = rng.sample(fresh, n)
    return picked, used + picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--reroll", default=None,
                    help="resample only this category, keep the rest")
    args = ap.parse_args()

    seed = args.seed if args.seed is not None else int(time.time())
    rng = random.Random(seed)

    pools = json.loads(POOLS.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() \
        else {k: [] for k in pools}

    if args.reroll:
        if not SPEC.exists():
            sys.exit("--reroll needs an existing test_spec.json")
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        cat = args.reroll
        # return the old picks to the pool's future, draw new ones
        ledger[cat] = [x for x in ledger.get(cat, [])
                       if x not in spec["items"][cat]]
        picked, ledger[cat] = draw(rng, pools[cat], ledger.get(cat, []),
                                   DRAW[cat], cat)
        spec["items"][cat] = picked
        spec["seed"] = f"{spec.get('seed')}+reroll({cat},{seed})"
    else:
        items = {}
        for cat, n in DRAW.items():
            items[cat], ledger[cat] = draw(rng, pools[cat],
                                           ledger.get(cat, []), n, cat)
        spec = {
            "seed": seed,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "items": items,
            "answer_positions": {
                name: balanced_positions(rng, count, width)
                for name, count, width in ANSWER_SECTIONS
            },
        }

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"seed={spec['seed']} -> {SPEC.relative_to(ROOT)} written, ledger updated at {LEDGER.relative_to(ROOT)}")
    for cat, xs in spec["items"].items():
        print(f"  {cat}: {len(xs)} items")


if __name__ == "__main__":
    main()
