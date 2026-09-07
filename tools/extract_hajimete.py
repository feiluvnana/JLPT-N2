#!/usr/bin/env python3
"""Extract 「はじめての日本語能力試験 N2単語 2500」 into readable Markdown.

    make extract-hajimete
    python3 tools/extract_hajimete.py --list
    python3 tools/extract_hajimete.py --only body

| source | output |
| --- | --- |
| `refs/Hajimete/はじめての日本語能力試験 N2単語 2500.pdf` (45 MB, 314 pp.) | `refs/Hajimete/vocab_reference.md` |

## Why this script exists

Added 2026-09-07, when the book was placed in `refs/`. `AGENTS.md` §3 named Shin
Kanzen and Soumatome as `exam-blueprint`'s only vocabulary/kanji band authority;
this book is a third, and a differently shaped one. Shin Kanzen and Soumatome are
*graded exercise* volumes whose headwords have to be recovered from around the
drills. This is a flat, numbered **2500-word N2 list** — headword, reading, part
of speech, one example sentence, and EN/ZH/VI glosses per entry — which is the
shape a vocabulary authority actually wants.

Two consumers, and the second is the one that matters most:

1. **`question-authoring`'s per-key verification.** 「check every 問題1–6 key
   against the books」 gains a third book, and one whose entry list is
   enumerable rather than buried in exercises.
2. **`tools/lexical_profile.py`'s reference corpus.** That module decides whether
   a word in a 読解 passage is one an N2 candidate has met, and its reference is
   currently the official archive plus four OCR'd exercise volumes. A curated
   2500-word N2 list is a far better statement of "N2 vocabulary" than the
   incidental vocabulary of exercise prose, and it sharpens exactly the
   distinction the lexical gate is built on: an ordinary N2 word a reader knows
   versus specialist terminology they do not.

## What this file is NOT

Secondary evidence, like every other textbook extract (`AGENTS.md` §3). It
corroborates band, reading and part of speech; it never sets a count or a length
— `refs/JLPT_N2_NEW/` does. It is also **OCR, not exact**: the book prints
furigana above the headword and three translation columns beside it, and Vision
interleaves them, so an entry's Japanese is reliable and its glosses are not.
Read a page image before quoting a reading as decisive.

## Page map

The PDF is 314 pages: front matter and 目次 to p.~12, then the numbered entries
1–2500 in six chapters, then indices. No printed-page offset is asserted here —
the running heads carry the chapter and the entry-number range, which is what a
later reader needs to find an entry, and asserting an offset this script has not
verified against the 目次 would be the kind of invented number `AGENTS.md` §3
forbids.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refs_ocr as R  # noqa: E402

PDF = R.ROOT / "refs" / "Hajimete" / "はじめての日本語能力試験 N2単語 2500.pdf"
OUT = R.ROOT / "refs" / "Hajimete" / "vocab_reference.md"

# One section covering the whole body. The book is a flat numbered list, so a
# curated section map would be invented structure — the entry numbers in the
# running heads are the index, and they survive OCR.
SECTIONS = [
    R.Section(
        key="body",
        title="全編 — 見出し語 1〜2500(語義・例文・品詞)",
        pages=(1, 314),
        note="**The N2 word list itself.** Each entry prints the headword, its "
             "reading in furigana, a part-of-speech tag, one example sentence, "
             "and EN/ZH/VI glosses. The Japanese is the usable half: Vision "
             "interleaves the three translation columns, so a gloss here is a "
             "hint and the example sentence is the evidence. Consumers: "
             "`question-authoring` (per-key verification, a third book beside "
             "Shin Kanzen and Soumatome) and `tools/lexical_profile.py` "
             "(reference corpus for the 読解 lexical-load gate).",
        columns=True,
    ),
]

BOOK = R.Book(path=PDF, label="はじめての日本語能力試験 N2単語 2500",
              out=OUT, sections=SECTIONS, pages_total=314)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    R.add_common_args(ap)
    a = ap.parse_args()

    if not PDF.is_file():
        print(f"missing source: {R.rel(PDF)}\n"
              f"  It is not in git (AGENTS.md §3) — restore it from the refs "
              f"release, or ask the user for it. Do NOT substitute a number "
              f"from memory for one this book owns.", file=sys.stderr)
        return 2

    if a.list:
        R.print_sections([BOOK])
        return 0
    if a.split_pdf:
        R.split_pdf(PDF, BOOK.sections, Path(a.split_pdf))
        return 0

    R.select(BOOK, a.only)
    R.require_poppler()
    stats = R.extract_book(BOOK, tool="tools/extract_hajimete.py", dpi=a.dpi,
                           chunk=a.chunk, keep_ruby=a.keep_ruby,
                           use_columns=not a.no_columns)
    print(f"{R.rel(OUT)}: {stats.pages} page(s), {stats.lines} line(s), "
          f"mean confidence {stats.mean_conf():.2f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
