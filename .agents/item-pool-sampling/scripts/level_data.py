#!/usr/bin/env python3
"""Shared level-classification data for item-pool-sampling."""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "references"
OPENJLPT = REF / "openjlpt"
POOLS_PATH = REF / "pools.json"
LEVEL_BAND = (
    HERE.parents[1]
    / "exam-qa-review"
    / "references"
    / "level_band_grammar.txt"
)

LEVELS = ("N1", "N2", "N3", "N4", "N5", "unknown")


def head(item: str) -> str:
    """Normalized identity ignoring disambiguating gloss."""
    s = str(item).strip()
    s = re.sub(r"^[〜～]+", "〜", s)
    return s.split("(")[0].split("（")[0].strip()


def load_level_band() -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {
        "TOO_HARD": [],
        "TOO_EASY": [],
        "ALLOW": [],
    }
    if not LEVEL_BAND.is_file():
        return sections
    cur = None
    for raw in LEVEL_BAND.read_text(encoding="utf-8").splitlines():
        if raw.lstrip().startswith("## "):
            name = raw.lstrip()[3:].split("#", 1)[0].strip().upper()
            cur = name if name in sections else None
            continue
        line = raw.split("#", 1)[0].strip()
        if line and cur:
            sections[cur].append(line)
    return sections


def load_openjlpt() -> dict[str, dict[str, str]]:
    """word/kanji/grammar -> level (N1..N5)."""
    out: dict[str, dict[str, str]] = {
        "vocab": {},
        "kanji": {},
        "grammar": {},
    }
    for path in sorted(OPENJLPT.glob("*.json")):
        if path.name == "NOTICE.md":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            continue
        m = re.match(r"(vocab|kanji|grammar)-n([1-5])", path.stem, re.I)
        if not m:
            continue
        kind, num = m.group(1), m.group(2)
        level = f"N{num}"
        for row in data:
            if kind == "vocab":
                w = (row.get("word") or "").strip()
                r = (row.get("reading") or "").strip()
                if w:
                    out["vocab"][w] = level
                if r:
                    out["vocab"][r] = level
            elif kind == "kanji":
                c = (row.get("character") or "").strip()
                if c:
                    out["kanji"][c] = level
            elif kind == "grammar":
                p = (row.get("pattern") or row.get("grammar") or "").strip()
                if p:
                    out["grammar"][p] = level
    return out


def load_pool_heads() -> set[str]:
    if not POOLS_PATH.is_file():
        return set()
    pools = json.loads(POOLS_PATH.read_text(encoding="utf-8"))
    heads: set[str] = set()
    for xs in pools.values():
        if not isinstance(xs, list):
            continue
        for item in xs:
            heads.add(str(item))
            heads.add(head(str(item)))
    return heads


def normalize_grammar(item: str) -> str:
    s = str(item).strip()
    if not s.startswith("〜") and not s.startswith("～"):
        if s.startswith("敬語:"):
            return s
        return f"〜{s}"
    return s


def is_japanese_text(s: str) -> bool:
    return bool(re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", s))
