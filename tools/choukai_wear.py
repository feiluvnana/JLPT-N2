#!/usr/bin/env python3
"""How hard the 聴解 clip pool is being mined, per 大問 and per source.

`TEXTBOOK_SLOTS` is the one knob that decides how much of a paper's listening
half comes from the textbook pool, and the number it should hold is not a
preference — it is this measurement. A clip spent five times across the suite
is a clip a learner hears in one paper out of five.

Two numbers, and they answer different questions:

**MEASURED wear** comes out of `logs/choukai_draws.json`: how many papers have
actually spent each clip. It is the truth about what is on disk, and it lags a
policy change until every paper is re-drawn.

**PROJECTED wear** comes out of the policy alone —
`slots x mixed papers / candidates` — so it can be read BEFORE a re-draw and is
what a proposed `TEXTBOOK_SLOTS` has to be judged on. For the official half the
divisor is per-slot: official draws are slot-preserving, so slot *k* of 問題N
competes only against slot *k* of the other sittings, and there are as many
candidates as sittings.

`WEAR_CEILING` is the bar. Above it, raise the pool
(`.agents/choukai-audio/references/textbook_items.json`), never the slot count.

Usage
-----
    python3 tools/choukai_wear.py            # the report
    python3 tools/choukai_wear.py --json     # the same numbers as data
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

BANK_PATH = ROOT / "logs" / "choukai_bank.json"
DRAWS_PATH = ROOT / "logs" / "choukai_draws.json"

# The most times one clip may be spent across the whole suite. Not a measured
# constant — a judgment about novelty, and the one this repo is held to: at 4,
# a learner working through every paper meets a given clip in one paper in six.
WEAR_CEILING = 4.0


def load_composer():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "compose_choukai", ROOT / "tools" / "compose_choukai.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure() -> dict:
    """Measured and projected wear, per 大問 and per source."""
    composer = load_composer()
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    index = {r["id"]: r for r in bank["records"]}

    official: dict[tuple[str, int], int] = Counter()
    textbook: Counter = Counter()
    for rec in bank["records"]:
        if rec["kind"] != "item":
            continue
        if rec.get("needs_number_call"):
            textbook[rec["section"]] += 1
        else:
            official[(rec["section"], rec["slot"])] += 1

    draws = (json.loads(DRAWS_PATH.read_text(encoding="utf-8"))["history"]
             if DRAWS_PATH.is_file() else [])
    papers = [row["test_id"] for row in draws]
    mixed = [t for t in papers if t not in composer.OFFICIAL_ONLY_TESTS]

    # --- measured: how many papers spent each clip, grouped by section+source
    spent: dict[str, Counter] = defaultdict(Counter)
    for row in draws:
        for rec_id in row["clips"].values():
            rec = index.get(rec_id)
            if rec is None:               # a clip the bank no longer carries
                continue
            spent[rec["section"]][rec_id] += 1

    out = {"papers": len(papers), "mixed_papers": len(mixed),
           "official_only": sorted(set(papers) & set(composer.OFFICIAL_ONLY_TESTS)),
           "ceiling": WEAR_CEILING, "sections": {}}

    for section, count in composer.SECTIONS.items():
        tb_slots = composer.TEXTBOOK_SLOTS.get(section, 0)
        tb_pool = textbook.get(section, 0)
        off_slots = count - tb_slots
        # Official candidates per slot; the same for every slot of a 大問.
        per_slot = min(official.get((section, s), 0)
                       for s in range(1, count + 1)) if count else 0

        proj_tb = (tb_slots * len(mixed) / tb_pool) if tb_pool else None
        # An official-only paper fills every slot from the official pool.
        off_uses = off_slots * len(mixed) + count * (len(papers) - len(mixed))
        proj_off = (off_uses / (per_slot * count)) if per_slot and count else None

        used = spent.get(section, Counter())
        def side(is_tb: bool) -> dict:
            vals = [n for rid, n in used.items()
                    if bool(index[rid].get("needs_number_call")) is is_tb]
            if not vals:
                return {"clips": 0}
            return {"clips": len(vals), "min": min(vals), "max": max(vals),
                    "mean": round(sum(vals) / len(vals), 2)}

        out["sections"][section] = {
            "slots": count,
            "textbook_slots": tb_slots, "textbook_pool": tb_pool,
            "official_candidates_per_slot": per_slot,
            "projected_textbook_wear": (round(proj_tb, 2) if proj_tb else None),
            "projected_official_wear": (round(proj_off, 2) if proj_off else None),
            "measured_textbook": side(True),
            "measured_official": side(False),
        }
    return out


def report(data: dict) -> int:
    print(f"聴解 clip wear — {data['papers']} composed paper(s), "
          f"{data['mixed_papers']} mixed, official-only "
          f"{data['official_only'] or '(none)'}; ceiling "
          f"{data['ceiling']:.1f} uses per clip\n")
    print(f"  {'大問':<6} {'slots':>5} {'tb':>3} {'pool':>5} {'proj':>6} "
          f"{'measured tb (min/mean/max)':>28}   "
          f"{'off/slot':>8} {'proj':>6} {'measured off':>22}")
    over = []
    for section, row in data["sections"].items():
        m, o = row["measured_textbook"], row["measured_official"]
        mt = (f"{m['clips']:2d} clips {m['min']}/{m['mean']}/{m['max']}"
              if m["clips"] else "                    —")
        mo = (f"{o['clips']:3d} clips {o['min']}/{o['mean']}/{o['max']}"
              if o["clips"] else "         —")
        pt = row["projected_textbook_wear"]
        po = row["projected_official_wear"]
        print(f"  {section:<6} {row['slots']:>5} {row['textbook_slots']:>3} "
              f"{row['textbook_pool']:>5} "
              f"{(f'{pt:.2f}' if pt else '   —'):>6} {mt:>28}   "
              f"{row['official_candidates_per_slot']:>8} "
              f"{(f'{po:.2f}' if po else '   —'):>6} {mo:>22}")
        if pt and pt > data["ceiling"]:
            over.append(f"{section} projects {pt:.2f} uses per textbook clip "
                        f"({row['textbook_slots']} slot(s) x "
                        f"{data['mixed_papers']} papers / "
                        f"{row['textbook_pool']} item(s))")
    for line in over:
        print(f"\nOVER  {line}")
    if over:
        print("      Grow the pool (textbook_items.json), never the slot count.")
    return 1 if over else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="print data, not a table")
    args = ap.parse_args(argv)
    if not BANK_PATH.is_file():
        sys.exit("no logs/choukai_bank.json — run `make choukai-bank`")
    data = measure()
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=1))
        return 0
    return report(data)


if __name__ == "__main__":
    raise SystemExit(main())
