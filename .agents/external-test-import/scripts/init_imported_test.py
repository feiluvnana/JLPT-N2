#!/usr/bin/env python3
"""Scaffold tests/imported-<slug>/ and write import_meta.json.

    python3 init_imported_test.py --slug n2-2025-12 \\
      --booklet path/to/booklet.pdf \\
      --script path/to/script.pdf \\
      --audio path/to/choukai.mp3
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from origin import IMPORTED_PREFIX, imported_id  # noqa: E402

ROOT = SCRIPT_DIR.parents[2]
TESTS = ROOT / "tests"


def rel_or_abs(path: Path | None) -> str | None:
    if path is None:
        return None
    path = path.expanduser().resolve()
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", required=True,
                    help="id suffix after imported- (e.g. n2-2025-12)")
    ap.add_argument("--level", default="N2")
    ap.add_argument("--booklet", type=Path, help="source booklet PDF/MD")
    ap.add_argument("--script", type=Path, help="source listening script PDF/txt")
    ap.add_argument("--audio", type=Path, help="source listening MP3")
    ap.add_argument("--answer-key", type=Path, help="optional separate key PDF")
    ap.add_argument("--force", action="store_true",
                    help="allow updating meta if the folder already exists")
    args = ap.parse_args()

    try:
        test_id = imported_id(args.slug)
    except ValueError as e:
        sys.exit(str(e))

    dest = TESTS / test_id
    if dest.exists() and not args.force:
        sys.exit(f"already exists: {dest} (pass --force to refresh import_meta.json)")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "_extract").mkdir(exist_ok=True)

    for label, p in (("booklet", args.booklet), ("script", args.script),
                     ("audio", args.audio), ("answer-key", args.answer_key)):
        if p is not None and not p.expanduser().exists():
            sys.exit(f"{label} not found: {p}")

    meta = {
        "origin": "imported",
        "test_id": test_id,
        "level": args.level,
        "imported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": {
            "booklet": rel_or_abs(args.booklet),
            "script": rel_or_abs(args.script),
            "audio": rel_or_abs(args.audio),
            "answer_key": rel_or_abs(args.answer_key),
        },
        "notes": (
            f"Folder flag `{IMPORTED_PREFIX}` marks origin=imported. "
            "Folders without that prefix are generated."
        ),
    }
    meta_path = dest / "import_meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    print(f"scaffolded {dest.relative_to(ROOT)}")
    print(f"meta      {meta_path.relative_to(ROOT)}")
    print("next: extract PDFs → author Markdown → make booklet/sheet → make check")


if __name__ == "__main__":
    main()
