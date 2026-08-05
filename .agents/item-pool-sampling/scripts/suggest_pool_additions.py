#!/usr/bin/env python3
"""
Propose pool additions from OpenJLPT N2 not yet in pools.json.

Usage:
    python suggest_pool_additions.py
    python suggest_pool_additions.py --category context_words --limit 50
    python suggest_pool_additions.py --write-staging  # classify N2 -> staging
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOLS = HERE.parent / "references" / "pools.json"
OPENJLPT = HERE.parent / "references" / "openjlpt"

from level_data import head  # noqa: E402

# category -> how to format OpenJLPT vocab rows
VOCAB_CATS = {
    "context_words",
    "paraphrase",
    "usage",
    "orthography",
}
KANJI_CATS = {"kanji_reading", "orthography"}


def existing_heads(pools: dict) -> set[str]:
    hs: set[str] = set()
    for xs in pools.values():
        for x in xs:
            hs.add(head(str(x)))
            # kanji without reading
            m = re.match(r"^([\u4e00-\u9fff]+)", str(x))
            if m:
                hs.add(m.group(1))
    return hs


def load_vocab_n2() -> list[dict]:
    p = OPENJLPT / "vocab-n2.json"
    return json.loads(p.read_text(encoding="utf-8"))


def load_kanji_n2() -> list[dict]:
    p = OPENJLPT / "kanji-n2.json"
    return json.loads(p.read_text(encoding="utf-8"))


def suggest_vocab(category: str, limit: int, pools: dict) -> list[str]:
    seen = existing_heads(pools)
    out: list[str] = []
    for row in load_vocab_n2():
        w = (row.get("word") or "").strip()
        if not w or head(w) in seen:
            continue
        if category == "orthography":
            if not re.search(r"[\u4e00-\u9fff]", w):
                continue
            out.append(w)
        elif category in ("context_words", "usage"):
            if len(w) < 2:
                continue
            out.append(w)
        elif category == "paraphrase":
            if len(w) < 3:
                continue
            out.append(f"{w}({row.get('meanings',[''])[0][:20]})" if row.get("meanings") else w)
        if len(out) >= limit:
            break
        seen.add(head(w))
    return out


def suggest_kanji_reading(limit: int, pools: dict) -> list[str]:
    seen = existing_heads(pools)
    out: list[str] = []
    for row in load_kanji_n2():
        c = row.get("character", "")
        if not c or c in seen:
            continue
        on = (row.get("onyomi") or [""])[0].lower().replace(" ", "")
        kun = (row.get("kunyomi") or [""])[0]
        reading = kun if kun and re.search(r"[\u3040-\u30ff]", kun) else on
        if reading:
            out.append(f"{c}({reading})")
        else:
            out.append(c)
        seen.add(c)
        if len(out) >= limit:
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", default=None)
    ap.add_argument("--limit", type=int, default=80)
    ap.add_argument("--write-staging", action="store_true")
    args = ap.parse_args()

    pools = json.loads(POOLS.read_text(encoding="utf-8"))
    cats = [args.category] if args.category else [
        "kanji_reading", "orthography", "context_words", "paraphrase", "usage",
    ]

    proposals: dict[str, list[str]] = {}
    for cat in cats:
        if cat == "kanji_reading":
            proposals[cat] = suggest_kanji_reading(args.limit, pools)
        elif cat in VOCAB_CATS:
            proposals[cat] = suggest_vocab(cat, args.limit, pools)
        else:
            continue
        print(f"{cat}: {len(proposals[cat])} candidates")

    if args.write_staging:
        classify = HERE / "classify_level.py"
        for cat, items in proposals.items():
            for item in items:
                proc = subprocess.run(
                    [sys.executable, str(classify), "--item", item,
                     "--category", cat, "--stage"],
                    capture_output=True, text=True,
                )
                if proc.returncode != 0:
                    continue
        print("staged N2 candidates -> logs/adjunct_staging.json")
    else:
        print(json.dumps(proposals, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
