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
/* Furigana: WeasyPrint has NO ruby layout (and ignores ruby-position), so the
   reading is stacked manually. rt is taken out of flow and pinned above the
   base, which keeps the base glyphs on the text baseline and leaves line
   spacing untouched. Do NOT go back to display:inline-table -- WeasyPrint
   drops the base onto its own line under the reading. */
ruby {
  display: inline-block;
  position: relative;
  text-align: center;
  vertical-align: baseline;
  /* line-height 1 keeps the ruby box hugging its glyphs; with a taller
     inherited line-height the box grows and `bottom: 100%` would push the
     reading far above the text. */
  line-height: 1;
}
rb { display: inline; }
rt {
  position: absolute;
  bottom: calc(100% + 0.1em);
  left: -0.6em;
  right: -0.6em;
  font-size: 0.5em;
  line-height: 1;
  font-weight: normal;
  color: #333;
  white-space: nowrap;
  text-align: center;
}
rp { display: none; }
/* Only blocks that actually carry furigana get extra leading, so the reading
   clears the descenders of the line above without loosening plain text. */
p.furi, li.furi { line-height: 2.1; }
.vocab-notes { margin-top: 8px; font-size: 9pt; color: #333; line-height: 1.6; border-top: 1px dashed #aaa; padding-top: 6px; }
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


def add_choukai_furigana(md_content: str) -> str:
    """Add HTML ruby furigana to all kanji in listening test booklet text/options."""
    try:
        import pykakasi
    except ImportError:
        return md_content

    kks = pykakasi.kakasi()

    def token_to_ruby(orig: str, hira: str) -> str:
        if orig == '入っ' and hira == 'いっっ':
            return '<ruby>入<rt>はい</rt></ruby>っ'
        suffix = ''
        while orig and hira and orig[-1] == hira[-1] and not ('\u4e00' <= orig[-1] <= '\u9fff'):
            suffix = orig[-1] + suffix
            orig = orig[:-1]
            hira = hira[:-1]
        prefix = ''
        while orig and hira and orig[0] == hira[0] and not ('\u4e00' <= orig[0] <= '\u9fff'):
            prefix = prefix + orig[0]
            orig = orig[1:]
            hira = hira[1:]
        if orig and any('\u4e00' <= c <= '\u9fff' for c in orig):
            return f'{prefix}<ruby>{orig}<rt>{hira}</rt></ruby>{suffix}'
        return prefix + orig + suffix

    overrides = {
        '時間': '<ruby>時間<rt>じかん</rt></ruby>',
        '分': '<ruby>分<rt>ふん</rt></ruby>',
        '問題数': '<ruby>問題数<rt>もんだいすう</rt></ruby>',
        '問': '<ruby>問<rt>もん</rt></ruby>',
        '問題': '<ruby>問題<rt>もんだい</rt></ruby>',
        '例': '<ruby>例<rt>れい</rt></ruby>',
        '番': '<ruby>番<rt>ばん</rt></ruby>',
    }

    out_lines = []
    in_answer_key = False
    for line in md_content.splitlines():
        if '# 【正解・解説】' in line or '# 解答用紙' in line:
            in_answer_key = True
        if in_answer_key or line.startswith('#') or line.startswith('|') or '---' in line or '<ruby>' in line:
            out_lines.append(line)
            continue

        res = kks.convert(line)
        line_out = ''
        for item in res:
            orig = item['orig']
            hira = item['hira']
            if orig in overrides:
                line_out += overrides[orig]
            else:
                line_out += token_to_ruby(orig, hira)
        out_lines.append(line_out)

    return '\n'.join(out_lines)


RUBY_TAG = re.compile(r"<ruby>(.*?)<rt>(.*?)</rt>\s*</ruby>", re.S)
TAGS = re.compile(r"<[^>]+>")


def _em_width(text: str) -> float:
    """Approximate advance width in em: CJK/kana are full-width, ASCII half."""
    return sum(0.5 if ord(c) < 0x2E80 else 1.0 for c in text)


def fit_ruby(html: str) -> str:
    """Reserve room for readings wider than their base so furigana never
    collides with the neighbouring word's furigana.

    rt is absolutely positioned (see CSS), so a long reading would otherwise
    overhang its base. Widening the base box centres the kanji inside the space
    the reading needs -- the same thing furigana-heavy print books do.
    """
    def sub(m: re.Match) -> str:
        base, reading = m.group(1), m.group(2)
        need = _em_width(TAGS.sub("", reading)) * 0.5  # rt renders at 0.5em
        have = _em_width(TAGS.sub("", base))
        if need - have <= 0.05:
            return m.group(0)
        return f'<ruby style="min-width:{need:.2f}em">{base}<rt>{reading}</rt></ruby>'

    return RUBY_TAG.sub(sub, html)


BLOCK = re.compile(r"<(p|li)>(.*?)</\1>", re.S)


def mark_furigana_blocks(html: str) -> str:
    """Tag <p>/<li> holding ruby so CSS can give them furigana leading."""
    def sub(m: re.Match) -> str:
        tag, inner = m.group(1), m.group(2)
        cls = ' class="furi"' if "<ruby" in inner else ""
        return f"<{tag}{cls}>{inner}</{tag}>"

    return BLOCK.sub(sub, html)


def widen(line: str) -> str:
    """Lines carrying 3+ horizontal options get wide gaps between options."""
    if len(OPT.findall(line)) >= 3:
        return SEP.sub(WIDE + r"\1. ", line)
    return line


def build(src: Path) -> Path:
    md = src.read_text(encoding="utf-8")
    if "聴解" in src.name or "choukai" in src.name.lower():
        md = add_choukai_furigana(md)
    md = "\n".join(widen(l) for l in md.splitlines())
    # nl2br is MANDATORY: keeps stacked answer options on separate lines.
    body = markdown.markdown(md, extensions=["tables", "nl2br"])
    body = mark_furigana_blocks(fit_ruby(body))
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
