#!/usr/bin/env python3
"""Write a minimal 聴解_チャプター.json for an externally copied MP3.

Official/external audio has no TTS segment timeline. The interactive sheet
tolerates an empty chapters list; make check only requires the file to exist
alongside 聴解.mp3.

    python3 write_external_chapters.py tests/imported-n2-2025-12
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", type=Path, help="tests/<imported-…>/ directory")
    args = ap.parse_args()
    d = args.test_dir
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")
    mp3 = d / "聴解.mp3"
    if not mp3.is_file():
        sys.exit(f"missing {mp3} — copy the external MP3 first")

    duration = None
    try:
        from mutagen.mp3 import MP3  # optional
        duration = round(float(MP3(mp3).info.length), 2)
    except Exception:
        pass

    payload = {
        "duration": duration,
        "chapters": [],
        "source": "external",
        "note": "External/official MP3 — no TTS segment marks. "
                "Re-run make mp3 to synthesize chapter marks from 聴解スクリプト.txt.",
    }
    out = d / "聴解_チャプター.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} (duration={duration})")


if __name__ == "__main__":
    main()
