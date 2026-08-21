#!/usr/bin/env python3
"""Extract the Shin Kanzen N2 読解 textbook into readable Markdown.

    make extract-shinkanzen-dokkai
    python3 tools/extract_shinkanzen_dokkai.py --list
    python3 tools/extract_shinkanzen_dokkai.py --only mogi,bessatsu

Source: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Dokkai.pdf` (109 MB, 238 pages)
Output: `refs/Shinkanzen/dokkai_reference.md`

## Why this script exists (REPORT-DOKKAI.md §F11, §Phase 7)

`AGENTS.md` §3 lists `Shin_Kanzen_Masuta_N2-Dokkai.pdf`. The book is a scanned
image with no text layer (`pdffonts` prints an empty table), and at 109 MB it
exceeds the 100 MB PDF read cap, so it cannot be read whole.

This script extracts:
- **第1部-1 文章のしくみを理解する** — five discourse devices:
  1) 対比 2) 言い換え 3) 比喩 4) 疑問提示文 5) 主張表現
- **第1部-2 問いを解く技術を身につける** — five question types:
  1) 指示語 2) だれが・何が・何を 3) 下線部の意味 4) 理由 5) 例
- **第2部 情報検索** — four source types: 広告 / お知らせ / 説明書き / 表・リスト
- **模擬試験 (p.181+)** — a complete, typeset N2 読解 paper
- **別冊「解答と解説」** — keys and per-item explanations

## What this file is NOT

Secondary evidence. A textbook corroborates register, structure, discourse
devices, and question types. It never sets a count or a length — `refs/JLPT_N2_NEW/`
(the 7 current-era sittings 12/2022–12/2025) is the sole measuring stick for counts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refs_ocr as R  # noqa: E402

SK_PDF = R.ROOT / "refs" / "Shinkanzen" / "Shin_Kanzen_Masuta_N2-Dokkai.pdf"
SK_OUT = R.ROOT / "refs" / "Shinkanzen" / "dokkai_reference.md"

SK_MAIN = -6       # printed p.2 is PDF 8
SK_BESSATSU = -210 # 別冊 p.1 is PDF 211

SECTIONS = [
    R.Section(
        key="toc",
        title="目次・本書をお使いになる方へ",
        pages=(1, 10),
        printed_offset=SK_MAIN,
        note="目次 and introduction explaining book structure and N2 読解 overview.",
    ),
    R.Section(
        key="part1_structure",
        title="第1部 評論・解説・エッセイなど 1. 文章のしくみを理解する",
        pages=(14, 43),
        printed_offset=SK_MAIN,
        note="**Five N2 discourse devices**: 対比, 言い換え, 比喩, 疑問提示文, 主張表現.",
    ),
    R.Section(
        key="part1_techniques",
        title="第1部 評論・解説・エッセイなど 2. 問いを解く技術を身につける",
        pages=(44, 77),
        printed_offset=SK_MAIN,
        note="**Five N2 question types**: 指示語, だれが・何が・何を, 下線部の意味, 理由, 例.",
    ),
    R.Section(
        key="part2_info",
        title="第2部 広告・お知らせ・説明書きなど（情報検索）",
        pages=(86, 123),
        printed_offset=SK_MAIN,
        note="**情報検索 by source type**: 広告, お知らせ, 説明書き, 表・リスト.",
    ),
    R.Section(
        key="mogi",
        title="模擬試験（typeset N2 読解 paper）",
        pages=(183, 198),
        printed_offset=SK_MAIN,
        underlines=True,
        note="Complete typeset N2 読解 paper with attributed passages and questions.",
    ),
    R.Section(
        key="bessatsu",
        title="別冊 解答と解説",
        pages=(211, 238),
        printed_offset=SK_BESSATSU,
        columns=False,
        note="Model answers and detailed explanations (別冊).",
    ),
]


def dokkai_book() -> R.Book:
    if not SK_PDF.is_file():
        sys.exit(f"missing input: {R.rel(SK_PDF)} (AGENTS.md §3)")
    return R.Book(
        path=SK_PDF,
        label="新完全マスター読解 日本語能力試験N2",
        out=SK_OUT,
        sections=list(SECTIONS),
        pages_total=238,
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    R.add_common_args(ap)
    args = ap.parse_args()

    book = dokkai_book()
    R.select(book, args.only)
    if args.list:
        R.print_sections([book])
        return

    if args.split_pdf:
        R.split_pdf(book.path, book.sections, Path(args.split_pdf))
    stats = R.extract_book(book, "tools/extract_shinkanzen_dokkai.py",
                          dpi=args.dpi, chunk=args.chunk,
                          keep_ruby=args.keep_ruby,
                          use_columns=not args.no_columns)
    print(f"wrote {R.rel(book.out)}: {stats.pages} pages, {stats.lines} lines, "
          f"mean confidence {stats.mean_conf():.2f}, "
          f"{stats.low_conf_share():.0%} below 0.50, "
          f"{stats.underlines} underlines located")


if __name__ == "__main__":
    main()
