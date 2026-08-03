#!/usr/bin/env python3
"""
Render JLPT exam Markdown sources to print-ready A4 PDFs.

Usage:
    python build_pdf.py 1_n2_gengo_chishiki_dokkai.md 2_n2_choukai_answer_sheet.md

Requires: wkhtmltopdf on PATH, `pip install markdown`, Noto CJK JP fonts.
"""

import re
import subprocess
import sys
from pathlib import Path

import markdown

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Noto Serif CJK JP", serif; font-size: 10.5pt;
       line-height: 1.9; color: #1a1a1a; }
h1 { font-family: "Noto Sans CJK JP", sans-serif; font-size: 15pt;
     border-bottom: 2.5px solid #1a1a1a; padding-bottom: 5px;
     margin: 30px 0 14px; page-break-after: avoid; }
h2 { font-family: "Noto Sans CJK JP", sans-serif; font-size: 12pt;
     background: #efefef; border-left: 5px solid #444; padding: 5px 10px;
     margin: 26px 0 12px; page-break-after: avoid; }
h3 { font-family: "Noto Sans CJK JP", sans-serif; font-size: 11pt;
     margin: 20px 0 8px; page-break-after: avoid; }
p { margin: 12px 0; }
table { border-collapse: collapse; margin: 10px 0; width: 100%; page-break-inside: avoid; }
th, td { border: 1px solid #888; padding: 4px 9px; font-size: 9.5pt;
         line-height: 1.6; }
th { background: #f0f0f0; font-family: "Noto Sans CJK JP", sans-serif; }
blockquote { border: 1px solid #999; background: #fafafa; margin: 10px 0;
             padding: 10px 14px; page-break-inside: avoid; }
hr { border: none; border-top: 1px dashed #999; margin: 22px 0; }
strong { font-family: "Noto Sans CJK JP", sans-serif; }
"""

WIDE = "\u3000\u3000\u3000"  # ideographic spaces survive HTML whitespace collapsing
OPT = re.compile(r"[1-4]\.\s")
SEP = re.compile(r"\s+([2-4])\.\s")


def widen(line: str) -> str:
    """Lines carrying 3+ horizontal options get wide gaps between options."""
    if len(OPT.findall(line)) >= 3:
        return SEP.sub(WIDE + r"\1. ", line)
    return line


def build(src: Path) -> Path:
    md = src.read_text(encoding="utf-8")
    md = "\n".join(widen(l) for l in md.splitlines())
    # nl2br is MANDATORY: keeps stacked answer options on separate lines.
    body = markdown.markdown(md, extensions=["tables", "nl2br"])
    html_path = src.with_suffix(".html")
    html_path.write_text(
        f'<!DOCTYPE html><html><head><meta charset="utf-8">'
        f"<style>{CSS}</style></head><body>{body}</body></html>",
        encoding="utf-8",
    )
    pdf_path = src.with_suffix(".pdf")
    import shutil
    if shutil.which("wkhtmltopdf"):
        subprocess.run(
            ["wkhtmltopdf", "--encoding", "utf-8", "-q", str(html_path), str(pdf_path)],
            check=True,
        )
    elif shutil.which("weasyprint"):
        subprocess.run(
            ["weasyprint", str(html_path), str(pdf_path)],
            check=True,
        )
    else:
        from weasyprint import HTML
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    return pdf_path


def verify(pdf: Path):
    import shutil
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        assert "\ufffd" not in out, f"mojibake detected in {pdf}"
        print(f"  ok: {pdf} ({out.count(chr(12)) + 1} pages approx)")
    else:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf))
        out = "\n".join(page.extract_text() for page in reader.pages)
        assert "\ufffd" not in out, f"mojibake detected in {pdf}"
        print(f"  ok: {pdf} ({len(reader.pages)} pages approx)")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        pdf = build(Path(arg))
        verify(pdf)
        print(f"built {pdf}")
