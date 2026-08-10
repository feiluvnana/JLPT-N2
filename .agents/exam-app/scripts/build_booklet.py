#!/usr/bin/env python3
"""
Render JLPT exam Markdown sources to booklet HTML (A4-styled, print-ready).

Usage:
    python build_booklet.py tests/1/言語知識・読解.md tests/1/聴解.md

Requires: `pip install markdown pykakasi`, Noto CJK JP fonts installed.
No PDF toolchain needed — the browser is the renderer.
"""

import hashlib
import re
import sys

from pathlib import Path

import markdown

# Screen-only shell. `CSS` keeps the A4 print geometry (@page etc.) untouched
# so Cmd-P still yields the booklet; this just makes the page readable on a
# monitor, where an unbounded full-width line length is unusable.
SCREEN_CSS = """
@media screen {
  :root { --gutter: 1.6em; }
  body { max-width: 60em; margin: 0 auto; padding: 2.5em var(--gutter) 6em;
         background: #fff; }
  table { max-width: 100%; }
}
@media screen and (max-width: 48em) {
  :root { --gutter: 0.8em; }
  body { padding: 1.2em var(--gutter) 4em; font-size: 10pt; }
  table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  blockquote { padding: 8px 10px; margin: 8px 0; }
  h1 { font-size: 13.5pt; margin: 22px 0 10px; }
  h2 { font-size: 11pt; padding: 4px 8px; margin: 18px 0 10px; }
}
"""


CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Noto Serif JP", "Noto Serif CJK JP", serif; font-size: 10.5pt;
       line-height: 1.9; color: #1a1a1a; }
h1 { font-family: "Noto Sans JP", "Noto Sans CJK JP", sans-serif; font-size: 15pt;
     border-bottom: 2.5px solid #1a1a1a; padding-bottom: 5px;
     margin: 30px 0 14px; page-break-after: avoid; }
h2 { font-family: "Noto Sans JP", "Noto Sans CJK JP", sans-serif; font-size: 12pt;
     background: #efefef; border-left: 5px solid #444; padding: 5px 10px;
     margin: 26px 0 12px; page-break-after: avoid; }
h3 { font-family: "Noto Sans JP", "Noto Sans CJK JP", sans-serif; font-size: 11pt;
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
th { background: #f0f0f0; font-family: "Noto Sans JP", "Noto Sans CJK JP", sans-serif; }
blockquote { border: 1px solid #999; background: #fafafa; margin: 10px 0;
             padding: 10px 14px; page-break-inside: avoid; }
hr { border: none; border-top: 1px dashed #999; margin: 22px 0; }
strong { font-family: "Noto Sans JP", "Noto Sans CJK JP", sans-serif; }
"""


def source_sha(path: Path) -> str:
    """First 12 hex digits of sha1 over the file's raw BYTES.

    Same convention `make_choukai_mp3.py` stamps into \u8074\u89e3_\u30c1\u30e3\u30d7\u30bf\u30fc.json as
    `script_sha`. NOT an mtime: mtimes are checkout-unstable, so they cannot
    distinguish "rebuilt" from "merely re-checked-out".
    """
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12]


def src_sha_comments(sources) -> str:
    """`<!-- src_sha: <file name>=<12-hex sha1> -->`, one comment per input.

    Stamped into every generated HTML so an artifact built from a superseded
    Markdown source is detectable by content, and `make check` can fail on it.
    The precedent is on the audio side: a script rewrite across several
    \u8074\u89e3\u30b9\u30af\u30ea\u30d7\u30c8.txt files once rebuilt only one MP3, and nothing could see
    the rest. The HTML deliverables had exactly the same blind spot.
    `build_interactive.py` calls this helper too, so both builders emit one
    format. Each stamp gets its own line (the rest of the document is one long
    line) so it is greppable and shows up as a one-line diff on a rebuild.
    """
    return "".join(f"\n<!-- src_sha: {p.name}={source_sha(p)} -->\n"
                   for p in sources if p.is_file())


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
NOTE_ITEM = re.compile(r"（注\d+）[^（\n]*")


def split_vocab_note_line(line: str) -> str:
    """One （注N） gloss per line in vocabulary note blocks."""
    stripped = line.strip().rstrip("\\")
    if not stripped.startswith("（注"):
        return line
    items = NOTE_ITEM.findall(stripped)
    if len(items) <= 1:
        return line
    prefix = line[: len(line) - len(line.lstrip())]
    return "\n".join(prefix + item for item in items)


def format_vocab_notes(md: str) -> str:
    return "\n".join(split_vocab_note_line(l) for l in md.splitlines())


def mark_vocab_notes(html: str) -> str:
    """Tag gloss blocks so `.vocab-notes` styling applies."""

    def sub(m: re.Match) -> str:
        tag, inner = m.group(1), m.group(2)
        text = TAGS.sub("", inner).strip()
        if text.startswith("（注"):
            return f'<{tag} class="vocab-notes">{inner}</{tag}>'
        return m.group(0)

    return BLOCK.sub(sub, html)


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


FONT_TAGS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">'
)


def build(src: Path) -> Path:
    """Markdown source -> styled A4 HTML booklet.

    No PDF toolchain — browser `@page` geometry layout renders identical A4
    and the same CSS prints correctly straight from the browser."""
    md = src.read_text(encoding="utf-8")
    if "聴解" in src.name or "choukai" in src.name.lower():
        md = add_choukai_furigana(md)
    md = "\n".join(widen(l) for l in md.splitlines())
    md = format_vocab_notes(md)
    # nl2br is MANDATORY: keeps stacked answer options on separate lines.
    body = markdown.markdown(md, extensions=["tables", "nl2br"])
    body = mark_vocab_notes(mark_furigana_blocks(fit_ruby(body)))
    html_path = src.with_suffix(".html")
    html_path.write_text(
        f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'{FONT_TAGS}'
        f"<title>{src.stem}</title>"
        f"{src_sha_comments([src])}"
        f"<style>{CSS}{SCREEN_CSS}</style></head><body>{body}</body></html>",
        encoding="utf-8",
    )
    return html_path


def verify(html_path: Path, src: Path):
    """The checks that used to run against the PDF, now against the HTML."""
    html = html_path.read_text(encoding="utf-8")
    problems = []
    if "\ufffd" in html:
        problems.append("mojibake (U+FFFD) in output")
    # Question numbering must stay continuous across section boundaries. `N.`
    # list syntax makes python-markdown emit <ol> and restart at 1 in every
    # section, so question-authoring mandates bold `**N**` stems.
    if "<ol>" in html:
        problems.append("<ol> present — a stem used `N.` list syntax and will "
                        "renumber from 1; use `**N**` instead")
    if "言語知識" in src.name:
        nums = {int(m.group(1)) for m in
                re.finditer(r"<strong>(\d{1,2})(?:</strong>|\s)", html)}
        missing = [n for n in range(1, 72) if n not in nums]
        if missing:
            problems.append(f"no bold stem found for question(s) {missing}")
    if problems:
        raise SystemExit(f"{html_path}:\n  " + "\n  ".join(problems))
    print(f"  ok: {html_path} "
          f"({len(re.sub(r'<[^>]+>', '', html)):,} chars of text)")


if __name__ == "__main__":
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not argv:
        sys.exit("usage: build_booklet.py tests/<id>/言語知識・読解.md "
                 "[tests/<id>/聴解.md]")
    for arg in argv:
        src = Path(arg)
        if not src.is_file():
            sys.exit(f"not found: {src}")
        out = build(src)
        verify(out, src)
        print(f"built {out}")
