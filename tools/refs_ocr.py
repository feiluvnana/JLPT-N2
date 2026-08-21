#!/usr/bin/env python3
"""Rasterise → Vision-OCR → fenced Markdown, for the scanned books in `refs/`.

Shared engine behind `tools/extract_kanji_tables.py` and
`tools/extract_shinkanzen_goi.py`. Not a command of its own; it has no
`main()` and no `make` target. Both callers `import refs_ocr` (they live in
`tools/`, so `python3 tools/extract_*.py` already puts this file on
`sys.path`).

## Why OCR at all

`AGENTS.md` §3 names four books as the ONLY vocabulary/kanji band authority
for `pools.json`. All four are **scanned images with no text layer**
(`pdffonts` prints an empty table for every one of them), so pypdf, pdfminer
and poppler all return nothing. The only reader available without a new
dependency is macOS Vision, which `tools/vision_ocr.swift` already wraps for
the `refs/JLPT_N2_NEW/` script PDFs — this module drives that same binary,
compiles it the same way, and fences its output the same way.

## Every line this module writes is SECONDARY EVIDENCE

A textbook corroborates **band, family and reading**. It never sets a count or
a length: the 31-sitting archive in `refs/JLPT_N2_NEW/` is the only measuring
stick for those, and it is exact where this is not. Callers must repeat that in
their output header — `secondary_evidence_header()` below is the single copy of
the wording.

## The 100 MB read cap, and why rendering is chunked

Two of the four books are over the 100 MB per-file PDF read cap
(`N2-Kanji.pdf` 264 MB, Soumatome 漢字 173 MB, Soumatome 語彙 103 MB; Shin
Kanzen 語彙 at 40 MB is the only one that reads directly), so **an agent cannot
open them whole and neither should a script**. `render_and_ocr()` therefore
rasterises in page chunks (`--chunk`, default 8): one `pdftoppm -f/-l` per
chunk into a temp dir, OCR that chunk, delete the PNGs, next chunk. Peak disk
stays a few tens of MB whatever the book weighs. `split_pdf()` writes the same
slices out as small PDFs when a human or an agent needs to *read* a section
under the cap.

## Mechanics worth knowing before changing anything here

- **300 DPI is the measured optimum**, the same figure `extract_jlpt_n2_new.py`
  settled on. 400 and 600 DPI were tried on 別冊1 p.71 (`訓読みが二つ以上ある
  漢字`) and recovered nothing extra — the scans' own resolution is the ceiling.
- **Ruby is the dominant error source, not resolution.** These books furigana
  almost everything, and Vision merges a ruby stroke into the kanji below it:
  `雨→龍`, `下→辛`, `家→蒙`. Prose set without ruby comes out near-perfect on
  the same page. `drop_ruby()` removes the ruby lines Vision *does* emit
  separately (they read as noise interleaved with the base text), but it cannot
  undo a merged glyph. This is why the output is fenced and why no count may be
  derived from inside a fence.
- **Column order.** Vision sorts top-to-bottom then left-to-right, which
  interleaves the two columns of every 漢字表 page into unreadable alternation.
  `split_columns()` finds the empty vertical gutter and emits one column at a
  time, which is the difference between a usable table and a shuffled one.
- **Underlines.** `underline_rules()` finds the printed underline under a
  問題1/問題5-style target — the one thing a text extract loses — and
  `mark_underlines()` annotates the line it sits under. Needs Pillow; without
  it the annotation is silently skipped and the header says so. The
  char-span estimate divides the line box by character count, so it is
  approximate and labelled as such on every line it writes.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR_SRC = ROOT / "tools" / "vision_ocr.swift"
OCR_BIN = ROOT / "tools" / ".build" / "vision_ocr"

# Measured, not guessed: 400 and 600 DPI recovered nothing 300 missed on the
# 別冊1 音訓 tables, and the archive extractor reached the same number.
OCR_DPI = 300
# Pages rasterised per pdftoppm call. The point is peak disk, not speed: a
# 264 MB book must never be turned into 253 PNGs at once.
CHUNK = 8

READ_CAP_MB = 100

# 1-bit scans of a printed page put the glyph body well under this.
INK = 140
# An underline runs at least this fraction of the page width. Shorter dark runs
# are the strokes of a kanji, a table rule cell, or a bullet.
MIN_RULE_W = 0.028
# A printed rule is a couple of pixels tall at 300 DPI; anything thicker is a
# filled box, a black band, or the scanner's edge.
MAX_RULE_H_FRAC = 0.004


# ---------------------------------------------------------------- OCR binary
def ensure_ocr_binary() -> Path | None:
    """Compile tools/vision_ocr.swift on first use. None if unavailable.

    Same contract as extract_jlpt_n2_new.ensure_ocr_binary(); duplicated
    rather than imported because that file is an entry point that opens the
    whole archive on import-time constants.
    """
    if OCR_BIN.is_file() and OCR_BIN.stat().st_mtime >= OCR_SRC.stat().st_mtime:
        return OCR_BIN
    if sys.platform != "darwin" or not shutil.which("swiftc"):
        return None
    OCR_BIN.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["swiftc", "-O", str(OCR_SRC), "-o", str(OCR_BIN)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"warning: could not build the OCR helper:\n{proc.stderr}", file=sys.stderr)
        return None
    return OCR_BIN


def require_poppler() -> None:
    if not shutil.which("pdftoppm"):
        sys.exit("pdftoppm (poppler) is required to rasterise a scanned PDF: "
                 "brew install poppler / apt-get install poppler-utils "
                 "(README.md §environment, row 11)")


# ---------------------------------------------------------------- data model
@dataclass
class Section:
    """One run of pages worth extracting, and how to render it."""

    key: str                       # --only selector
    title: str                     # Markdown heading
    pages: tuple[int, int]         # inclusive 1-based PDF page numbers
    note: str = ""                 # what this section is, in the output
    printed_offset: int | None = None   # printed page = pdf page + offset
    columns: bool = True           # split the page's vertical gutter
    underlines: bool = False       # look for printed underlines (needs Pillow)

    @property
    def page_list(self) -> list[int]:
        return list(range(self.pages[0], self.pages[1] + 1))

    def printed(self, pdf_page: int) -> str:
        if self.printed_offset is None:
            return ""
        return f" (printed p.{pdf_page + self.printed_offset})"


@dataclass
class Book:
    """A scanned book and the sections a caller wants out of it."""

    path: Path
    label: str                     # human title, for the output header
    out: Path                      # the .md this book's sections are written to
    sections: list[Section] = field(default_factory=list)
    pages_total: int = 0


@dataclass
class Stats:
    pages: int = 0
    lines: int = 0
    ruby_dropped: int = 0
    columns_split: int = 0
    underlines: int = 0
    conf: list[float] = field(default_factory=list)

    def mean_conf(self) -> float:
        return statistics.fmean(self.conf) if self.conf else float("nan")

    def low_conf_share(self, floor: float = 0.5) -> float:
        if not self.conf:
            return float("nan")
        return sum(1 for c in self.conf if c < floor) / len(self.conf)


# ---------------------------------------------------------------- rasterise + OCR
def _run_ocr(binary: Path, pngs: list[Path]) -> dict[str, list[dict]]:
    """OCR a batch of renders; {png name: [row, ...]} in 0..1 top-left coords."""
    proc = subprocess.run([str(binary)] + [str(p) for p in pngs],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"warning: OCR helper failed: {proc.stderr}", file=sys.stderr)
        return {}
    out: dict[str, list[dict]] = {}
    current = None
    for line in proc.stdout.splitlines():
        if line.startswith("--- ") and line.endswith(" ---"):
            current = Path(line[4:-4]).name
            out[current] = []
            continue
        parts = line.split("\t")
        if current is None or len(parts) != 6:
            continue
        x0, top, x1, bottom, conf, text = parts
        out[current].append({"x0": float(x0), "top": float(top), "x1": float(x1),
                             "bottom": float(bottom), "conf": float(conf),
                             "text": text.strip()})
    return out


def _page_number(png: Path) -> int:
    """pdftoppm -f/-l names its output by the real page number."""
    return int(re.search(r"(\d+)\.png$", png.name).group(1))


def render_and_ocr(pdf: Path, pages: list[int], *, dpi: int = OCR_DPI,
                   chunk: int = CHUNK, want_underlines: bool = False,
                   ) -> dict[int, dict]:
    """{page: {"rows": [...], "rules": [...]}} for the pages asked for.

    Rasterises `chunk` pages at a time and deletes each chunk's PNGs before the
    next, so a 264 MB book never becomes 253 PNGs on disk at once (see the
    module docstring on the 100 MB read cap).
    """
    require_poppler()
    binary = ensure_ocr_binary()
    if binary is None:
        sys.exit("no OCR helper: this needs macOS with swiftc (see "
                 "tools/vision_ocr.swift). These PDFs have no text layer, so "
                 "there is nothing to fall back to.")

    result: dict[int, dict] = {}
    todo = sorted(set(pages))
    for i in range(0, len(todo), chunk):
        block = todo[i:i + chunk]
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["pdftoppm", "-r", str(dpi), "-png",
                            "-f", str(block[0]), "-l", str(block[-1]),
                            str(pdf), f"{tmp}/pg"],
                           check=True, capture_output=True)
            pngs = sorted(Path(tmp).glob("pg-*.png"))
            wanted = [p for p in pngs if _page_number(p) in set(block)]
            ocr = _run_ocr(binary, wanted)
            for png in wanted:
                n = _page_number(png)
                result[n] = {"rows": ocr.get(png.name, []),
                             "rules": underline_rules(png) if want_underlines else []}
        print(f"  … pages {block[0]}–{block[-1]}", file=sys.stderr)
    return result


def split_pdf(pdf: Path, sections: list[Section], out_dir: Path) -> list[Path]:
    """Write each section out as its own small PDF, for reading under the cap.

    The books this module targets are up to 264 MB, well over the 100 MB
    per-file read cap, so "open the 別冊 and check" is only possible on a slice.
    """
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        sys.exit("pypdf is required for --split-pdf: pip install pypdf")
    out_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf))
    written = []
    for s in sections:
        writer = PdfWriter()
        for n in s.page_list:
            writer.add_page(reader.pages[n - 1])
        dest = out_dir / f"{pdf.stem}.{s.key}.p{s.pages[0]}-{s.pages[1]}.pdf"
        with dest.open("wb") as fh:
            writer.write(fh)
        written.append(dest)
        mb = dest.stat().st_size / 1e6
        flag = "" if mb <= READ_CAP_MB else f"  ** still over the {READ_CAP_MB} MB cap **"
        print(f"  {dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest} "
              f"({mb:.1f} MB){flag}")
    return written


# ---------------------------------------------------------------- page shaping
def drop_ruby(rows: list[dict]) -> tuple[list[dict], int]:
    """Remove the half-height lines Vision emits for furigana.

    Vision returns ruby as its own observation above the base text; interleaved
    into reading order it reads as noise (`あまど` on its own line above
    `あま雨戸`). Same rule as extract_jlpt_n2_new.merge_page(). It does NOT fix
    a kanji whose glyph the ruby corrupted — nothing here can.
    """
    heights = [r["bottom"] - r["top"] for r in rows]
    if not heights:
        return rows, 0
    median_h = statistics.median(heights)
    kept = [r for r in rows if (r["bottom"] - r["top"]) >= 0.6 * median_h]
    return kept, len(rows) - len(kept)


# A cut is only a gutter if this few lines cross it.
MAX_STRADDLE = 0.18


def split_columns(rows: list[dict], depth: int = 1) -> list[tuple[str, list[dict]]]:
    """Split a page at its vertical gutter(s), recursively. [(label, rows), …]

    Vision's reading order is top-to-bottom over the WHOLE page, so a
    two-column 漢字表 page comes back as left/right/left/right alternation.
    Finding the gutter and emitting one column at a time is the difference
    between a usable table and a shuffled one.

    **A "fully empty gutter" is the wrong test** and was the first version of
    this: almost every table page in these books opens with full-width heading
    or bullet lines, one of which crosses the gutter, so nothing split and the
    訓読み table stayed shuffled. Instead, pick the interior cut that the FEWEST
    lines straddle, require the straddlers to be a small minority, and emit them
    as their own leading block — which is where they belong anyway, since they
    are the section's heading.

    `depth` is 1 on purpose. Recursing found a second "gutter" inside a column —
    between a 漢字表 row's headword cell and its readings cell — and split a
    coherent table row in half. These books set two columns; one cut is right.
    """
    if depth <= 0 or len(rows) < 8:
        return [("", rows)]
    eps = 0.006
    best = None
    for k in range(28, 73):
        cut = k / 100
        straddle = [r for r in rows if r["x0"] < cut - eps and r["x1"] > cut + eps]
        left = [r for r in rows if r["x1"] <= cut + eps]
        right = [r for r in rows if r["x0"] >= cut - eps]
        if len(left) < 4 or len(right) < 4:
            continue
        key = (len(straddle), abs(cut - 0.5))
        if best is None or key < best[0]:
            best = (key, cut, straddle, left, right)
    if best is None or best[0][0] > MAX_STRADDLE * len(rows):
        return [("", rows)]
    _, _, straddle, left, right = best

    blocks: list[tuple[str, list[dict]]] = []
    if straddle:
        blocks.append(("full-width lines", straddle))
    cols = split_columns(left, depth - 1) + split_columns(right, depth - 1)
    n = 0
    for label, block in cols:
        if label:
            blocks.append((label, block))
        else:
            n += 1
            blocks.append((f"column {n}", block))
    return blocks


def order(rows: list[dict]) -> list[dict]:
    """Reading order: cluster into visual rows first, then left to right.

    Sorting on raw `top` looks right and is not: two observations printed on the
    same line come back 0.001–0.004 apart, so a bare sort interleaves the cells
    of a table row with the row above it. That scrambled the 模擬試験 answer key
    into unusable alternation before this clustered.
    """
    if not rows:
        return []
    heights = [r["bottom"] - r["top"] for r in rows]
    tol = 0.6 * statistics.median(heights)
    buckets: list[list[dict]] = []
    for r in sorted(rows, key=lambda r: r["top"]):
        if buckets and r["top"] - buckets[-1][0]["top"] <= tol:
            buckets[-1].append(r)
        else:
            buckets.append([r])
    out: list[dict] = []
    for b in buckets:
        out += sorted(b, key=lambda r: r["x0"])
    return out


# ---------------------------------------------------------------- underlines
def underline_rules(png: Path) -> list[dict]:
    """Printed underlines on a page render, as normalised boxes.

    The one thing a text extract cannot give: `booklet.md` and every OCR line
    lose the underline that marks a 問題1/問題5 target. A scan still has it as
    a long thin dark run, so find it in the pixels.

    Needs Pillow, which README.md does not require — returns [] without it, and
    the caller says so in the output header.
    """
    try:
        from PIL import Image
    except ImportError:
        return []
    im = Image.open(png).convert("L")
    w, h = im.size
    px = im.load()
    min_run = max(8, int(MIN_RULE_W * w))
    rows: list[tuple[int, int, int]] = []
    for y in range(h):
        best = cur = 0
        start = best_start = 0
        for x in range(w):
            if px[x, y] < INK:
                if cur == 0:
                    start = x
                cur += 1
                if cur > best:
                    best, best_start = cur, start
            else:
                cur = 0
        if best >= min_run:
            rows.append((y, best_start, best))
    # Merge vertically adjacent scan lines into one rule.
    out: list[dict] = []
    group: list[tuple[int, int, int]] = []
    for row in rows + [(10**9, 0, 0)]:
        if group and row[0] - group[-1][0] > 2:
            y0, y1 = group[0][0], group[-1][0]
            if (y1 - y0 + 1) <= max(2, int(MAX_RULE_H_FRAC * h)):
                out.append({"top": y0 / h, "bottom": (y1 + 1) / h,
                            "x0": min(g[1] for g in group) / w,
                            "x1": max(g[1] + g[2] for g in group) / w})
            group = []
        if row[0] != 10**9:
            group.append(row)
    return out


def mark_underlines(rows: list[dict], rules: list[dict]) -> dict[int, list[str]]:
    """{row index: [annotation, ...]} for every rule that sits under a line.

    The character span is ESTIMATED by dividing the OCR line's box by its
    character count. These books set CJK at a fixed pitch, so on a pure-CJK
    line that lands on the right characters; a line whose OCR text disagrees
    with the printed cell count — a mis-read circled item number becoming two
    ASCII digits is the common case — shifts it by one. Weighting half-width
    characters at half a cell was tried and measured WORSE, because the
    mis-reads are precisely in the half-width run. Every annotation says `≈`.
    """
    notes: dict[int, list[str]] = {}
    for rule in rules:
        best = None
        for i, r in enumerate(rows):
            gap = rule["top"] - r["bottom"]
            if not (-0.004 <= gap <= 0.012):
                continue
            overlap = min(rule["x1"], r["x1"]) - max(rule["x0"], r["x0"])
            if overlap <= 0.4 * (rule["x1"] - rule["x0"]):
                continue
            if best is None or gap < best[0]:
                best = (gap, i, r)
        if best is None:
            continue
        _, idx, row = best
        text = row["text"]
        span = row["x1"] - row["x0"]
        if not text or span <= 0:
            continue
        per = span / len(text)
        a = max(0, min(len(text) - 1, round((rule["x0"] - row["x0"]) / per)))
        b = max(a + 1, min(len(text), round((rule["x1"] - row["x0"]) / per)))
        notes.setdefault(idx, []).append(
            f"underline ≈ chars {a + 1}–{b} 「{text[a:b]}」")
    return notes


# ---------------------------------------------------------------- rendering
def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()[:12]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def secondary_evidence_header(book: Book, tool: str, stats: Stats,
                              *, dpi: int, pillow: bool) -> list[str]:
    """The header every file this module writes must carry. Single copy."""
    return [
        f"# {book.label} — extracted reference tables",
        "",
        f"> Machine-extracted by `{tool}` (rasterise + macOS Vision OCR at "
        f"{dpi} DPI) from:",
        f"> - `{rel(book.path)}` (sha1 `{sha1(book.path)}`, "
        f"{book.pages_total} pages, {book.path.stat().st_size / 1e6:.0f} MB)",
        "> Regenerate rather than hand-edit.",
        "",
        "## Trust rules — read before using a single line of this file",
        "",
        "**1. This is OCR, not quotable as exact wording.** This book is a "
        "scanned image with no text layer (`pdffonts` prints an empty table), "
        "so every line below was read out of pixels. Errors cluster on kanji "
        "that carry furigana, because Vision merges the ruby stroke into the "
        "glyph under it — `雨→龍`, `下→辛`, `家→蒙`. Ruby-free prose on the "
        "same page comes out near-perfect. **Open the PDF before quoting any "
        "of this as the book's wording.**",
        "",
        "**2. This is SECONDARY EVIDENCE.** A textbook corroborates **band, "
        "family and reading** — is this word in the N2 inventory, does this "
        "kanji have a second 訓読み, are these two words a same-shape pair. It "
        "**never sets a count or a length**: the 31 official sittings in "
        "`refs/JLPT_N2_NEW/` are the measuring stick for every number, and "
        "their `booklet.md`/`key.md` are exact where this file is not. Never "
        "derive a calibration number from inside a fence.",
        "",
        "**3. Everything is fenced `[OCR ▼]` … `[OCR ▲]`** for exactly that "
        "reason — the same convention as `refs/JLPT_N2_NEW/*/script.md`. Text "
        "outside a fence is this repo's own annotation, not the book.",
        "",
        f"**Measured quality of this run:** {stats.pages} pages, "
        f"{stats.lines} lines kept, "
        f"{stats.ruby_dropped} half-height ruby lines dropped, "
        f"{stats.columns_split} page-columns split at a gutter"
        + (f", {stats.underlines} printed underlines located."
           if pillow else
           ", underline detection OFF (no Pillow — `pip install pillow`)."),
        "",
        f"Vision's own confidence on this run: mean {stats.mean_conf():.2f}, "
        f"{stats.low_conf_share():.0%} of lines below 0.50. **Do not read that "
        "as an accuracy figure** — for Japanese, Vision quantises confidence "
        "coarsely (0.30 / 0.50 / 1.00) and plenty of 0.30 lines here are "
        "character-perfect while some 1.00 lines are not. It is a run-to-run "
        "comparator only; the real quality statement is section by section, in "
        "each section's note.",
        "",
    ]


def render_section(section: Section, pages: dict[int, dict], stats: Stats,
                   *, keep_ruby: bool = False, use_columns: bool = True,
                   ) -> list[str]:
    out = [f"## {section.title}", ""]
    if section.note:
        out += [section.note, ""]
    out += [f"PDF pages {section.pages[0]}–{section.pages[1]}"
            + (f" (printed pp.{section.pages[0] + section.printed_offset}–"
               f"{section.pages[1] + section.printed_offset})"
               if section.printed_offset is not None else ""),
            ""]

    for n in section.page_list:
        page = pages.get(n)
        out += [f"### PDF page {n}{section.printed(n)}", ""]
        rows = page["rows"] if page else []
        if not keep_ruby:
            rows, dropped = drop_ruby(rows)
            stats.ruby_dropped += dropped
        if not rows:
            out += ["*(no text recognised on this page)*", ""]
            continue
        notes = mark_underlines(order(rows), page["rules"]) if page["rules"] else {}
        if notes:
            stats.underlines += sum(len(v) for v in notes.values())
        blocks = (split_columns(rows) if (use_columns and section.columns)
                  else [("", rows)])
        if len(blocks) > 1:
            stats.columns_split += len(blocks)
        # mark_underlines indexes the whole ordered page, so re-derive per block
        index_of = {id(r): i for i, r in enumerate(order(rows))}
        out.append("[OCR ▼]")
        for label, block in blocks:
            if len(blocks) > 1:
                out.append(f"— {label or 'block'} —")
            for r in order(block):
                text = r["text"]
                if not text:
                    continue
                stats.lines += 1
                stats.conf.append(r["conf"])
                out.append(text)
                for note in notes.get(index_of[id(r)], []):
                    out.append(f"    ↳ {note} (estimated span — see trust rule 1)")
        out += ["[OCR ▲]", ""]
        stats.pages += 1
    return out


def extract_book(book: Book, tool: str, *, dpi: int = OCR_DPI, chunk: int = CHUNK,
                 keep_ruby: bool = False, use_columns: bool = True) -> Stats:
    """Render every section of one book and write book.out."""
    pillow = True
    try:
        import PIL  # noqa: F401
    except ImportError:
        pillow = False

    stats = Stats()
    body: list[str] = []
    for s in book.sections:
        print(f"{book.out.name}: {s.key} (PDF pp.{s.pages[0]}–{s.pages[1]})",
              file=sys.stderr)
        pages = render_and_ocr(book.path, s.page_list, dpi=dpi, chunk=chunk,
                               want_underlines=s.underlines and pillow)
        body += render_section(s, pages, stats, keep_ruby=keep_ruby,
                              use_columns=use_columns)

    head = secondary_evidence_header(book, tool, stats, dpi=dpi, pillow=pillow)
    toc = ["## Sections in this file", ""]
    toc += [f"- **{s.title}** — PDF pp.{s.pages[0]}–{s.pages[1]}"
            for s in book.sections]
    toc.append("")
    book.out.parent.mkdir(parents=True, exist_ok=True)
    book.out.write_text("\n".join(head + toc + body).rstrip() + "\n",
                        encoding="utf-8")
    return stats


def add_common_args(ap) -> None:
    """The flags both extractors share."""
    ap.add_argument("--only", default="",
                    help="comma-separated section keys (default: all); "
                         "--list prints them")
    ap.add_argument("--list", action="store_true",
                    help="print the section table and exit — no rasterising")
    ap.add_argument("--dpi", type=int, default=OCR_DPI,
                    help=f"render resolution (default {OCR_DPI}; 400 and 600 "
                         "were measured and recovered nothing extra)")
    ap.add_argument("--chunk", type=int, default=CHUNK,
                    help=f"pages per pdftoppm call (default {CHUNK}) — this is "
                         "the chunking the 100 MB read cap forces")
    ap.add_argument("--keep-ruby", action="store_true",
                    help="keep the half-height furigana lines (noisy)")
    ap.add_argument("--no-columns", action="store_true",
                    help="do not split pages at their vertical gutter")
    ap.add_argument("--split-pdf", metavar="DIR",
                    help="also write each section out as its own small PDF, so "
                         "a section of an over-cap book can be read directly")


def select(book: Book, only: str) -> None:
    if not only:
        return
    keys = {k.strip() for k in only.split(",") if k.strip()}
    unknown = keys - {s.key for s in book.sections}
    if unknown:
        sys.exit(f"unknown section key(s) for {book.path.name}: "
                 f"{', '.join(sorted(unknown))}")
    book.sections = [s for s in book.sections if s.key in keys]


def print_sections(books: list[Book]) -> None:
    for b in books:
        print(f"\n{b.label}\n  {rel(b.path)} → {rel(b.out)}")
        for s in b.sections:
            flags = []
            if not s.columns:
                flags.append("single column")
            if s.underlines:
                flags.append("underline scan")
            print(f"  {s.key:<22} PDF pp.{s.pages[0]:>3}–{s.pages[1]:<3} "
                  f"{s.title}" + (f"  [{', '.join(flags)}]" if flags else ""))
