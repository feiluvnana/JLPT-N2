#!/usr/bin/env python3
"""Extract text from a PDF into a UTF-8 .txt file (import working cache).

    python3 extract_pdf_text.py booklet.pdf -o out.txt
    python3 extract_pdf_text.py booklet.pdf --pages 1-5 -o out.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


JP = re.compile(r"[぀-ヿ一-鿿]")
# CID-keyed fonts with no ToUnicode map decode to code points scattered through
# blocks a Japanese exam never uses (Bengali, CJK strokes, ideographic
# annotation, combining marks). Digits map into C0 controls and vanish outright.
MOJIBAKE = re.compile(r"[̀-ͯऀ-৿㆐-㇯]")


def jp_ratio(text: str) -> float:
    body = re.sub(r"\s", "", text)
    return len(JP.findall(body)) / len(body) if body else 0.0


def looks_like_mojibake(text: str) -> bool:
    """True when the text decoded to garbage rather than Japanese.

    A CID-keyed PDF with no ToUnicode map (Adobe-Japan1 + Identity-H, common in
    Japanese DTP output) extracts as non-empty nonsense, so the all-pages-empty
    guard below never fires and the caller happily "reads" the result.
    """
    body = re.sub(r"\s", "", text)
    if len(body) < 200:
        return False
    return len(MOJIBAKE.findall(body)) / len(body) > 0.02 and jp_ratio(text) < 0.30


def _pypdf_pages(pdf: Path) -> list[str]:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        sys.exit("pypdf is required: pip install pypdf\n" + str(e))
    return [p.extract_text() or "" for p in PdfReader(str(pdf)).pages]


def _pdfminer_pages(pdf: Path) -> list[str] | None:
    """Per-page text via pdfminer, which resolves predefined CID CMaps."""
    try:
        from pdfminer.high_level import extract_text
    except ImportError:
        return None
    # pdfminer separates pages with a form feed, and appends one after the last
    # page — drop that trailing empty chunk so page numbers keep matching pypdf.
    pages = extract_text(str(pdf)).split("\x0c")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def extract(pdf: Path, pages: list[int] | None, engine: str = "auto") -> str:
    per_page = None if engine == "pdfminer" else _pypdf_pages(pdf)
    used = "pypdf"

    if engine in ("auto", "pdfminer"):
        joined = "\n".join(per_page) if per_page else ""
        if engine == "pdfminer" or looks_like_mojibake(joined):
            alt = _pdfminer_pages(pdf)
            if alt is None:
                if engine == "pdfminer":
                    sys.exit("pdfminer.six is required: pip install pdfminer.six")
                print("warning: text looks like mojibake (CID-keyed font with no "
                      "ToUnicode) and pdfminer.six is not installed — install it "
                      "(pip install pdfminer.six) or OCR the file; do NOT author "
                      "from this output", file=sys.stderr)
            elif engine == "pdfminer" or jp_ratio("\n".join(alt)) > jp_ratio(joined):
                per_page, used = alt, "pdfminer"
                if engine == "auto":
                    print("note: pypdf returned mojibake (CID-keyed font); "
                          "used pdfminer instead", file=sys.stderr)

    n = len(per_page)
    indices = pages if pages is not None else list(range(1, n + 1))
    chunks: list[str] = []
    empty = 0
    for i in indices:
        if i < 1 or i > n:
            sys.exit(f"page {i} out of range 1..{n}")
        text = per_page[i - 1]
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
    if looks_like_mojibake(body):
        print(f"warning: output still looks like mojibake after the {used} pass "
              "— OCR the file instead of authoring from this text",
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
    ap.add_argument("--engine", choices=("auto", "pypdf", "pdfminer"),
                    default="auto",
                    help="auto (default) falls back to pdfminer when pypdf "
                         "returns mojibake from a CID-keyed font")
    args = ap.parse_args()
    if not args.pdf.is_file():
        sys.exit(f"not a file: {args.pdf}")
    text = extract(args.pdf, parse_pages(args.pages), args.engine)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output} ({len(text)} chars)")


if __name__ == "__main__":
    main()
