#!/usr/bin/env python3
"""Extract text from a PDF into a UTF-8 .txt file (import working cache).

    python3 extract_pdf_text.py booklet.pdf -o out.txt
    python3 extract_pdf_text.py booklet.pdf --pages 1-5 -o out.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def extract(pdf: Path, pages: list[int] | None) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        sys.exit("pypdf is required: pip install pypdf\n" + str(e))

    reader = PdfReader(str(pdf))
    n = len(reader.pages)
    indices = pages if pages is not None else list(range(1, n + 1))
    chunks: list[str] = []
    empty = 0
    for i in indices:
        if i < 1 or i > n:
            sys.exit(f"page {i} out of range 1..{n}")
        text = reader.pages[i - 1].extract_text() or ""
        if not text.strip():
            empty += 1
        chunks.append(f"--- page {i}/{n} ---\n{text.rstrip()}\n")
    body = "\n".join(chunks)
    if empty == len(indices):
        sys.exit(
            f"no extractable text in {pdf} ({empty}/{len(indices)} pages empty) "
            "— likely a scan; OCR first, then re-run"
        )
    if empty:
        print(f"warning: {empty}/{len(indices)} pages had no text layer",
              file=sys.stderr)
    return body


def parse_pages(spec: str | None, n_hint: int | None = None) -> list[int] | None:
    if not spec:
        return None
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            lo, hi = int(a), int(b)
            if lo > hi:
                lo, hi = hi, lo
            out.extend(range(lo, hi + 1))
        else:
            out.append(int(part))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path, help="input PDF")
    ap.add_argument("-o", "--output", type=Path, required=True,
                    help="UTF-8 text output path")
    ap.add_argument("--pages", help="page list/ranges, e.g. 1-10,15")
    args = ap.parse_args()
    if not args.pdf.is_file():
        sys.exit(f"not a file: {args.pdf}")
    text = extract(args.pdf, parse_pages(args.pages))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output} ({len(text)} chars)")


if __name__ == "__main__":
    main()
