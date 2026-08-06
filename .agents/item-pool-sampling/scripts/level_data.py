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

# --- Themed pool categories (R13) ----------------------------------------
# reading_topics and listening_scenarios are the only categories whose pool
# entries are OBJECTS, not bare strings: {"topic"|"scenario": …, "theme": …}.
# THEMES is a CLOSED vocabulary — adding a value here is a deliberate edit of
# the taxonomy, not a per-entry decision. See item-pool-sampling/SKILL.md
# §"Topic themes".
THEMED_CATS = {"reading_topics": "topic", "listening_scenarios": "scenario"}

THEMES = (
    "睡眠・健康", "医療・福祉", "食", "環境", "防災", "交通", "住まい",
    "働き方", "教育", "子育て・家族", "地域活性化", "デジタル化",
    "消費・経済", "文化・伝統", "スポーツ・余暇", "人間関係",
    "行政・手続き", "メディア・情報", "旅行・観光", "科学・技術",
)


def entry_text(entry) -> str:
    """The testable/authorable string of a pool or spec entry.

    Pool entries are bare strings everywhere except the two themed categories,
    where they are {"topic"|"scenario": …, "theme": …}; spec entries add
    {"item": …} for adjunct rows. Every reader must go through this instead of
    str(entry), or a dict stringifies into `{'topic': …}` and silently poisons
    dedupe/recency sets.
    """
    if isinstance(entry, dict):
        for k in ("item", "topic", "scenario"):
            v = entry.get(k)
            if v:
                return str(v)
        return ""
    return str(entry)


def entry_theme(entry) -> str | None:
    """The theme tag of a themed pool/spec entry, or None if it carries none."""
    return entry.get("theme") if isinstance(entry, dict) else None


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
            t = entry_text(item)
            heads.add(t)
            heads.add(head(t))
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
