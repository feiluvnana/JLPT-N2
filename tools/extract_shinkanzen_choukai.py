#!/usr/bin/env python3
"""Extract the Shin Kanzen N2 聴解 textbook and 別冊 scripts into readable Markdown.

    make extract-shinkanzen
    python3 tools/extract_shinkanzen_choukai.py --list
    python3 tools/extract_shinkanzen_choukai.py --only bessatsu_mogi,bessatsu_script

Source: `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai.pdf` (202 MB, 161 pages)
Output: `refs/Shinkanzen/choukai_script.md`

## Why this script exists (REPORT-CHOUKAI.md §F11, §Phase 7)

`AGENTS.md` §3 lists `Shin_Kanzen_Masuta_N2-Choukai.pdf`. The book is a scanned
image with no text layer, and at 202 MB it exceeds the 100 MB PDF read cap.

This script extracts:
- **問題紹介・本書の使い方 (pp.1–15)** — layout, scoring structure, and task categories.
- **第1部 発音・縮約形・即時応答 (pp.16–45)** — 音の変化・縮約形 and response practice.
- **第2部 課題理解・ポイント理解・概要理解・統合理解 (pp.46–115)** — question types.
- **模擬試験 (pp.116–128)** — booklet layout.
- **別冊「解答とスクリプト」 (pp.129–161)** — complete transcripts of all practice tracks and 模擬試験.

## What this file is NOT

Secondary evidence. A textbook corroborates register, conversational forms,
and question types. It never sets a count or a length — `refs/JLPT_N2_NEW/`
(the 31 official sittings) is the sole measuring stick for counts and pacing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refs_ocr as R  # noqa: E402

SK_PDF = R.ROOT / "refs" / "Shinkanzen" / "Shin_Kanzen_Masuta_N2-Choukai.pdf"
SK_OUT = R.ROOT / "refs" / "Shinkanzen" / "choukai_script.md"

SK_MAIN = 0
SK_BESSATSU = 0

SECTIONS = [
    R.Section(
        key="intro",
        title="目次・問題紹介・本書の使い方",
        pages=(1, 15),
        printed_offset=SK_MAIN,
        note="Introduction, N2 聴解 format breakdown, and task types.",
    ),
    R.Section(
        key="part1_phonology",
        title="第1部 発音・縮約形・即時応答",
        pages=(16, 45),
        printed_offset=SK_MAIN,
        note="音の変化・縮約形 and immediate response patterns.",
    ),
    R.Section(
        key="part2_skills",
        title="第2部 課題理解・ポイント理解・概要理解・統合理解",
        pages=(46, 115),
        printed_offset=SK_MAIN,
        note="Four main listening task types and strategies.",
    ),
    R.Section(
        key="mogi_booklet",
        title="模擬試験（問題冊子）",
        pages=(116, 128),
        printed_offset=SK_MAIN,
        note="Typeset listening mock exam booklet.",
    ),
    R.Section(
        key="bessatsu_script",
        title="別冊 解答とスクリプト（練習問題＋模擬試験）",
        pages=(129, 161),
        printed_offset=SK_BESSATSU,
        columns=False,
        note="Full transcripts (スクリプト) and answer keys for all practice exercises and 模擬試験.",
    ),
]


def choukai_book() -> R.Book:
    if not SK_PDF.is_file():
        sys.exit(f"missing input: {R.rel(SK_PDF)} (AGENTS.md §3)")
    return R.Book(
        path=SK_PDF,
        label="新完全マスター聴解 日本語能力試験N2",
        out=SK_OUT,
        sections=list(SECTIONS),
        pages_total=161,
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    R.add_common_args(ap)
    args = ap.parse_args()

    book = choukai_book()
    R.select(book, args.only)
    if args.list:
        R.print_sections([book])
        return

    if args.split_pdf:
        R.split_pdf(book.path, book.sections, Path(args.split_pdf))
    stats = R.extract_book(book, "tools/extract_shinkanzen_choukai.py",
                          dpi=args.dpi, chunk=args.chunk,
                          keep_ruby=args.keep_ruby,
                          use_columns=not args.no_columns)
    print(f"wrote {R.rel(book.out)}: {stats.pages} pages, {stats.lines} lines, "
          f"mean confidence {stats.mean_conf():.2f}, "
          f"{stats.low_conf_share():.0%} below 0.50, "
          f"{stats.underlines} underlines located")


if __name__ == "__main__":
    main()
