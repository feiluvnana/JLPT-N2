#!/usr/bin/env python3
"""
Promote approved adjunct staging rows into pools.json.

Usage:
    python promote_adjunct.py              # promote status=approved
    python promote_adjunct.py --approve ITEM --category context_words
    python promote_adjunct.py --list
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOLS = HERE.parent / "references" / "pools.json"
STAGING = HERE.parents[2] / "logs" / "adjunct_staging.json"

from level_data import head  # noqa: E402


def load_staging() -> dict:
    if not STAGING.is_file():
        return {"version": 1, "entries": []}
    return json.loads(STAGING.read_text(encoding="utf-8"))


def save_staging(data: dict) -> None:
    STAGING.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")


def pool_heads(pools: dict) -> set[str]:
    hs: set[str] = set()
    for xs in pools.values():
        for x in xs:
            hs.add(x)
            hs.add(head(x))
    return hs


def promote(entries: list[dict], pools: dict) -> int:
    n = 0
    existing = pool_heads(pools)
    for e in entries:
        if e.get("status") != "approved":
            continue
        cat = e.get("category")
        item = e.get("item")
        if not cat or not item or cat not in pools:
            print(f"  skip invalid: {e}", file=sys.stderr)
            continue
        if item in pools[cat] or head(item) in existing:
            e["status"] = "promoted"
            e["promoted_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            continue
        pools[cat].append(item)
        existing.add(item)
        existing.add(head(item))
        e["status"] = "promoted"
        e["promoted_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"  + {cat}: {item}")
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--approve", default=None, help="mark one item approved")
    ap.add_argument("--category", default=None)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    data = load_staging()
    entries = data.get("entries", [])

    if args.list:
        for e in entries:
            print(f"{e.get('status','?'):10} {e.get('category','?'):20} {e.get('item')}")
        return

    if args.approve:
        if not args.category:
            sys.exit("--category required with --approve")
        found = False
        for e in entries:
            if e.get("item") == args.approve and e.get("category") == args.category:
                e["status"] = "approved"
                found = True
                print(f"approved: {args.category} / {args.approve}")
        if not found:
            sys.exit(f"not in staging: {args.category} / {args.approve}")
        save_staging(data)
        return

    pools = json.loads(POOLS.read_text(encoding="utf-8"))
    n = promote(entries, pools)
    POOLS.write_text(json.dumps(pools, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
    save_staging(data)
    print(f"promoted {n} item(s) -> {POOLS.relative_to(HERE.parents[2])}")


if __name__ == "__main__":
    main()
