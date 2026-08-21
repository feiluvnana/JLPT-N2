#!/usr/bin/env python3
"""Extract Shin Kanzen マスター N2-漢字 別冊1 (漢字表) into readable Markdown.

    make extract-kanji-tables
    python3 tools/extract_kanji_tables.py --list
    python3 tools/extract_kanji_tables.py --only kunyomi_multi,onyomi_multi

Writes ONE file: `refs/Shinkanzen/kanji_tables.md`, beside the book it comes
from. The PDF itself is a read-only input and is never touched.

## Why this script exists

`AGENTS.md` §3 declares this book part of exam-blueprint's ONLY kanji/vocabulary
band authority for `pools.json`. It is a **scanned image with no text layer**,
so until now nothing in the pipeline could read it: no extract, no make target,
no per-entry citation. Two live problems in this repo have their answer sitting
in 別冊1 and nowhere else (REPORT-GOI.md §F11):

- `make matrix`'s two grid generators are **hard-disabled** because they had no
  音訓 table and emitted kana-skeleton-violating grids (`AGENTS.md` §4,
  qa-report-20260819_1 F4). 「音読みが二つ以上ある漢字」 plus the 音の変化 pages
  (清濁・長短・促音) are that table.
- The two-訓読み rule — key the lower-graded reading, never print the other —
  lost its gate on 2026-08-11 when the vendored OpenJLPT corpus was deleted, and
  is now author diligence with no list behind it. 「訓読みが二つ以上ある漢字」 is
  the list the rule is about.

## The 264 MB problem — chunk before you read

`Shin_Kanzen_Masuta_N2-Kanji.pdf` is **264 MB, well over the 100 MB per-file
PDF read cap**, so it cannot be opened whole by an agent and must not be
rasterised whole by a script either. This script never does: `refs_ocr`
rasterises `--chunk` pages at a time (default 8) and deletes each chunk's PNGs
before the next. If you need to *read* a section yourself — to check a line this
file got wrong — slice it first:

    python3 tools/extract_kanji_tables.py --only kunyomi_multi \
        --split-pdf /tmp/kanji --list

`--split-pdf DIR` writes each selected section as its own small PDF, under the
cap, which is the only way to open 別冊1 directly. The two Soumatome volumes
(漢字 173 MB, 語彙 103 MB) are over the cap the same way; Shin Kanzen 語彙 at
40 MB is the one that reads directly.

## Page map (established by OCR'ing the 目次 and the section boundaries)

別冊1 runs PDF pp.133–213 and its printed numbering restarts, so printed page =
PDF page − 133 inside it. The main book runs printed = PDF − 7. Both offsets are
in the section table below and printed beside every page heading.

## What this file is NOT

Secondary evidence. It corroborates band, family and reading; it never sets a
count or a length — `refs/JLPT_N2_NEW/` does. `refs_ocr.secondary_evidence_header()`
puts that in the output, along with the fence convention and the ruby caveat.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refs_ocr as R  # noqa: E402

PDF = R.ROOT / "refs" / "Shinkanzen" / "Shin_Kanzen_Masuta_N2-Kanji.pdf"
OUT = R.ROOT / "refs" / "Shinkanzen" / "kanji_tables.md"

# 別冊1 restarts its page numbering: printed = PDF − 133 (別冊1 p.71 is PDF 204).
BESSATSU = -133
# The main book: printed = PDF − 7 (「音の変化」 printed p.115 is PDF 122).
MAIN = -7

SECTIONS = [
    R.Section(
        key="bessatsu_toc",
        title="別冊1 漢字表 — 目次",
        pages=(134, 139),
        printed_offset=BESSATSU,
        note="What 別冊1 contains and where. The 回-by-回 index into 学習漢字リスト "
             "— use it to find which 回 a kanji is taught in, i.e. its band "
             "inside this book's own ステップ1/2/3 split.",
    ),
    R.Section(
        key="gakushuu_list",
        title="別冊1 学習漢字リスト（1,046字）",
        pages=(140, 202),
        printed_offset=BESSATSU,
        note="The book's whole N2 inventory: 1,046 kanji in three ステップ bands "
             "with every 音読み (katakana), 訓読み (hiragana) and 特別な読み方 it "
             "teaches, plus the 言葉 built from each. Ordered by 音読み (by 訓読み "
             "where there is none) within a ステップ. **This is the band list** — "
             "the ステップ a kanji sits in is this book's own difficulty grading, "
             "and its はじめに records that 28 former 旧1級 kanji were promoted "
             "into it, which is the source of the 「飢」/「饉」 band arguments. "
             "Two-column pages, and the 言葉 column carries furigana, so it is "
             "the most ruby-damaged section in this file: trust the kana "
             "readings, verify every kanji 言葉 against the PDF.",
    ),
    R.Section(
        key="special_readings",
        title="別冊1 特別な読み方をする漢字の言葉",
        pages=(203, 203),
        printed_offset=BESSATSU,
        note="The 39 irregular-reading words among this book's 1,046 kanji "
             "(熟字訓 and friends). A 問題1 target drawn from here is testing "
             "memorisation, not the on-reading grid — different item type, and "
             "the reason 問題1 needs a target-type mix at all.",
    ),
    R.Section(
        key="kunyomi_multi",
        title="別冊1 訓読みが二つ以上ある漢字",
        pages=(204, 208),
        printed_offset=BESSATSU,
        note="**The list the two-訓読み rule is about.** Every kanji in the book "
             "with two or more 訓読み, grouped so same-reading entries sit "
             "together, with the 送り仮名 and the 自動詞/他動詞 pairing marked "
             "「(がる・げる)」-style. This is what restores a gate for 「key the "
             "lower-graded reading; never print the other」 — deleted "
             "2026-08-11 with the OpenJLPT corpus. Readings are kana and come "
             "out clean; the example 言葉 carry ruby and do not.",
    ),
    R.Section(
        key="onyomi_multi",
        title="別冊1 音読みが二つ以上ある漢字",
        pages=(209, 213),
        printed_offset=BESSATSU,
        note="**The 音訓 table `make matrix` was hard-disabled for lacking.** "
             "First reading listed is the base 音読み; a second is given only "
             "where the old 出題基準 2級 list carried a word using it. That "
             "constraint is exactly what a 問題1 derivation grid needs: it says "
             "which second on-reading is real rather than invented, which is "
             "how the generators emitted kana-skeleton-violating grids "
             "(qa-report-20260819_1 F4).",
    ),
    R.Section(
        key="oto_no_henka",
        title="広がる広げる漢字の知識 ④ 音の変化（＋チャレンジ）",
        pages=(122, 124),
        printed_offset=MAIN,
        note="The 清濁・長短・促音 shifts a compound makes to its parts "
             "(学＋科→ガッカ). The other half of what a 問題1 derivation grid "
             "needs: 音読みが二つ以上ある漢字 says which readings exist, this "
             "says which mutations of one reading are real. Ruby-free prose — "
             "the cleanest OCR in this file.",
    ),
]


def build() -> R.Book:
    if not PDF.is_file():
        sys.exit(f"missing input: {R.rel(PDF)} (AGENTS.md §3)")
    return R.Book(
        path=PDF,
        label="新完全マスター漢字 日本語能力試験N2 — 別冊1 漢字表 ＋ 音の変化",
        out=OUT,
        sections=list(SECTIONS),
        pages_total=253,
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    R.add_common_args(ap)
    args = ap.parse_args()

    book = build()
    R.select(book, args.only)
    if args.list:
        R.print_sections([book])
        return
    if args.split_pdf:
        R.split_pdf(book.path, book.sections, Path(args.split_pdf))
    stats = R.extract_book(book, "tools/extract_kanji_tables.py", dpi=args.dpi,
                           chunk=args.chunk, keep_ruby=args.keep_ruby,
                           use_columns=not args.no_columns)
    print(f"wrote {R.rel(book.out)}: {stats.pages} pages, {stats.lines} lines, "
          f"mean confidence {stats.mean_conf():.2f}, "
          f"{stats.low_conf_share():.0%} below 0.50")


if __name__ == "__main__":
    main()
