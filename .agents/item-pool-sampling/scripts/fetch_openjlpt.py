#!/usr/bin/env python3
"""Vendor OpenJLPT N1/N2/N3 vocab and kanji JSON (CC BY — see NOTICE.md)."""

from __future__ import annotations

import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "references" / "openjlpt"
BASE = "https://raw.githubusercontent.com/evanclan/OpenJLPT/main/data/json"

FILES = [
    "vocab/n2.json",
    "vocab/n1.json",
    "vocab/n3.json",
    "kanji/n2.json",
    "kanji/n1.json",
    "kanji/n3.json",
]
NOTICE = "https://raw.githubusercontent.com/evanclan/OpenJLPT/main/NOTICE.md"


def fetch(url: str, dest: Path) -> None:
    print(f"fetch {url} -> {dest.name}")
    with urllib.request.urlopen(url, timeout=60) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for rel in FILES:
        name = rel.replace("/", "-")
        fetch(f"{BASE}/{rel}", OUT / name)
    fetch(NOTICE, OUT / "NOTICE.md")
    print("done")


if __name__ == "__main__":
    main()
