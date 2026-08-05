#!/usr/bin/env python3
"""
Classify a candidate item's JLPT level for staging / pool expansion.

Usage:
    python classify_level.py --item '措置'
    python classify_level.py --item '〜にあって' --category grammar_p7
    python classify_level.py --file candidates.json
    python classify_level.py --item '措置' --stage --category context_words

Output JSON: {item, category, level, confidence, evidence[], action}
action is allow_stage only when level == N2.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOGS = ROOT / "logs"
STAGING = LOGS / "adjunct_staging.json"

from level_data import (  # noqa: E402
    head,
    is_japanese_text,
    load_level_band,
    load_openjlpt,
    load_pool_heads,
    normalize_grammar,
)

GRAMMAR_CATS = {"grammar_p7", "grammar_p8"}
TOPIC_CATS = {"reading_topics", "listening_scenarios", "quick_response", "word_formation"}


def _grammar_band_hit(form: str, band: dict[str, list[str]]) -> str | None:
    hay = form.replace("〜", "").replace("～", "")
    for ban in band.get("TOO_HARD", []):
        b = ban.replace("〜", "").replace("～", "")
        if b and b in hay:
            if any(allow in hay and b in allow for allow in band.get("ALLOW", [])):
                continue
            return "TOO_HARD"
    for ban in band.get("TOO_EASY", []):
        b = ban.replace("〜", "").replace("～", "")
        if b and b in hay:
            return "TOO_EASY"
    return None


def classify_one(item: str, category: str | None = None) -> dict:
    item = str(item).strip()
    evidence: list[str] = []
    pool_heads = load_pool_heads()
    h = head(item)

    if item in pool_heads or h in pool_heads:
        return {
            "item": item,
            "category": category,
            "level": "N2",
            "confidence": "high",
            "evidence": ["pools.json (curated N2)"],
            "action": "allow_stage",
        }

    is_grammar = category in GRAMMAR_CATS or item.startswith("〜") or item.startswith("～")
    if is_grammar:
        form = normalize_grammar(item)
        band = load_level_band()
        hit = _grammar_band_hit(form, band)
        if hit == "TOO_HARD":
            return {
                "item": item,
                "category": category,
                "level": "N1",
                "confidence": "high",
                "evidence": ["level_band_grammar.txt TOO_HARD"],
                "action": "reject",
            }
        if hit == "TOO_EASY":
            return {
                "item": item,
                "category": category,
                "level": "N3",
                "confidence": "high",
                "evidence": ["level_band_grammar.txt TOO_EASY"],
                "action": "reject",
            }
        oj = load_openjlpt()
        for key in (form, h, form.lstrip("〜")):
            if key in oj["grammar"]:
                lv = oj["grammar"][key]
                evidence.append(f"openjlpt grammar {lv}")
                return _result(item, category, lv, evidence)

    oj = load_openjlpt()
    # Kanji single character
    if len(h) == 1 and re.match(r"[\u4e00-\u9fff]", h):
        if h in oj["kanji"]:
            lv = oj["kanji"][h]
            evidence.append(f"openjlpt kanji {lv}")
            return _result(item, category, lv, evidence)

    # Vocab: try head and kana/hiragana portions
    for probe in {h, item, re.sub(r"\([^)]*\)", "", item).strip()}:
        if not probe:
            continue
        if probe in oj["vocab"]:
            lv = oj["vocab"][probe]
            evidence.append(f"openjlpt vocab {lv}")
            return _result(item, category, lv, evidence)

    # Reading in parens e.g. 措置(そち)
    m = re.search(r"\(([ぁ-んァ-ンー]+)\)", item)
    if m and m.group(1) in oj["vocab"]:
        lv = oj["vocab"][m.group(1)]
        evidence.append(f"openjlpt vocab reading {lv}")
        return _result(item, category, lv, evidence)

    if not is_japanese_text(item):
        return {
            "item": item,
            "category": category,
            "level": "unknown",
            "confidence": "low",
            "evidence": ["no local match; not Japanese text"],
            "action": "reject",
        }

    if category in TOPIC_CATS:
        return {
            "item": item,
            "category": category,
            "level": "N2",
            "confidence": "medium",
            "evidence": ["curated topic/scenario (Japanese setting text)"],
            "action": "allow_stage",
        }

    return {
        "item": item,
        "category": category,
        "level": "unknown",
        "confidence": "low",
        "evidence": ["no match in pools.json, level_band, or openjlpt"],
        "action": "reject",
    }


def _result(item: str, category: str | None, level: str, evidence: list[str]) -> dict:
    # N1-only in OpenJLPT but not N2 list -> reject for N2 mock
    if level == "N2":
        action = "allow_stage"
        conf = "high"
    elif level in ("N1", "N3", "N4", "N5"):
        action = "reject"
        conf = "high"
    else:
        action = "reject"
        conf = "low"
    return {
        "item": item,
        "category": category,
        "level": level,
        "confidence": conf,
        "evidence": evidence,
        "action": action,
    }


def load_staging() -> dict:
    if not STAGING.is_file():
        return {"version": 1, "entries": []}
    return json.loads(STAGING.read_text(encoding="utf-8"))


def save_staging(data: dict) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    STAGING.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")


def stage_entry(result: dict, status: str = "ready") -> None:
    if result["action"] != "allow_stage":
        sys.exit(f"cannot stage: level={result['level']} action={result['action']}")
    if not result.get("category"):
        sys.exit("--category required when using --stage")
    data = load_staging()
    entries = data.setdefault("entries", [])
    for e in entries:
        if e.get("item") == result["item"] and e.get("category") == result["category"]:
            e.update({
                "level": result["level"],
                "evidence": result["evidence"],
                "status": status,
                "added_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            })
            save_staging(data)
            print(json.dumps(e, ensure_ascii=False, indent=2))
            return
    row = {
        "item": result["item"],
        "category": result["category"],
        "level": result["level"],
        "evidence": result["evidence"],
        "status": status,
        "added_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    entries.append(row)
    save_staging(data)
    print(json.dumps(row, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--item", default=None)
    ap.add_argument("--file", default=None, help="JSON list of {item, category?}")
    ap.add_argument("--category", default=None)
    ap.add_argument("--stage", action="store_true",
                    help="append to logs/adjunct_staging.json when N2")
    args = ap.parse_args()

    if args.file:
        rows = json.loads(Path(args.file).read_text(encoding="utf-8"))
        out = []
        for row in rows:
            item = row if isinstance(row, str) else row.get("item")
            cat = None if isinstance(row, str) else row.get("category", args.category)
            res = classify_one(item, cat)
            if args.stage and res["action"] == "allow_stage":
                stage_entry(res)
            out.append(res)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if not args.item:
        ap.error("provide --item or --file")

    res = classify_one(args.item, args.category)
    if args.stage:
        if res["action"] == "allow_stage":
            stage_entry(res)
        else:
            print(json.dumps(res, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
