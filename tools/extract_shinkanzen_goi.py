#!/usr/bin/env python3
"""Extract the two N2 語彙 textbooks into readable Markdown.

    make extract-shinkanzen-goi
    python3 tools/extract_shinkanzen_goi.py --list
    python3 tools/extract_shinkanzen_goi.py --book shinkanzen --only mogi1,mogi2

Two front-ends, one script, one file each — written beside the book it came
from. Both PDFs are read-only inputs and are never touched.

| `--book`     | source                                        | output                            |
| ------------ | --------------------------------------------- | --------------------------------- |
| `shinkanzen` | `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Goi.pdf` (40 MB) | `refs/Shinkanzen/goi_reference.md` |
| `soumatome`  | `refs/Soumatome/nihongo-soumatome-n2-goi.pdf` (103 MB)  | `refs/Soumatome/goi_reference.md`  |

## Why this script exists

`AGENTS.md` §3 declares both books part of exam-blueprint's ONLY
vocabulary/kanji band authority for `pools.json`. Both are scanned images with
no text layer, so nothing in the pipeline could read either one: the authoring
rule 「check every 問題1–6 key against the books」 left no evidence on disk, and
key-table rows cite 「Shinkanzen N2漢字の見出し語」 with no page a later reader
could check (REPORT-GOI.md §F11).

Three of that report's open problems have their data only here:

- **問題6's multi-sense trap** (`20260811_1` 落ち着く: "person calms down" vs
  "value settles") was a per-item judgment with no list → 意味がたくさんある言葉,
  three 課 in Shin Kanzen and three days in Soumatome.
- **The two-branch distractor rule** needs same-field and same-shape families
  and had no source for them → 意味が似ている言葉 / 形が似ている言葉 /
  似ている言葉①②③.
- **The 問題1/問題2 target band** — words written in easy kanji whose reading is
  the trap → Soumatome 第5週 「やさしい漢字で書きますが…」, which is that band
  exactly (物事・日中・年月・夜中・世間・作業・一生・用心・見事・土地…).

## The 模擬試験 pages, and what they can and cannot settle

Shin Kanzen 語彙 pp.186 and 188 carry two complete, exactly typeset 語彙 papers
with 別冊 keys. They are the only place in `refs/` outside the official archive
where a full, marked 語彙 paper can be read — and this script runs a pixel scan
for the printed underline on them (`--book shinkanzen --only mogi1,mogi2`),
which is the one mark every text extract loses. **But read the caveat**: a 語彙
volume has no 漢字読み or 表記 section, so these two papers are 語形成 /
文脈規定 / 言い換え類義 / 用法 only — i.e. this repo's 問題3–問題6. Neither they
nor Soumatome's 実戦問題 (also 文脈規定-first) contain a single 問題1 item, and
the Shin Kanzen 漢字 volume's 総合問題 are write-the-reading exercises, not
four-option items. **問題1's target-type mix is not measurable from any textbook
in `refs/`.** It is measurable from the official archive — see the note this
script prints, and REPORT-GOI.md §F10.3.

## Page maps

Printed page = PDF page − 7 (Shin Kanzen 語彙; its 別冊 restarts, − 213) and
PDF page − 1 (Soumatome 語彙). Established by OCR'ing the 目次 against the
running footers; both offsets are in the section tables and printed beside every
page heading.

## What these files are NOT

Secondary evidence. They corroborate band, family and reading; they never set a
count or a length — `refs/JLPT_N2_NEW/` does.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refs_ocr as R  # noqa: E402

SK_PDF = R.ROOT / "refs" / "Shinkanzen" / "Shin_Kanzen_Masuta_N2-Goi.pdf"
SK_OUT = R.ROOT / "refs" / "Shinkanzen" / "goi_reference.md"
SM_PDF = R.ROOT / "refs" / "Soumatome" / "nihongo-soumatome-n2-goi.pdf"
SM_OUT = R.ROOT / "refs" / "Soumatome" / "goi_reference.md"

SK_MAIN = -7      # printed = PDF − 7  (第2部 opens printed p.88 at PDF 95)
SK_BESSATSU = -213  # the 別冊 restarts: 別冊 p.32 is PDF 245
SM_MAIN = -1      # printed = PDF − 1  (printed p.6 is PDF 7)

SHINKANZEN = [
    R.Section(
        key="ch1_multi_sense",
        title="第2部 性質別 1章 意味がたくさんある言葉（動詞①② / 形容詞・名詞）",
        pages=(95, 112),
        printed_offset=SK_MAIN,
        note="**The list behind 問題6's multi-sense trap.** One word, several "
             "senses, each with the collocations that select it — which is what "
             "makes a 用法 item defensible or double-keyed. `20260811_1` "
             "問題6-26 keyed 落ち着く on 「person calms down」 while an option "
             "used 「value settles」; both senses are in this chapter.",
    ),
    R.Section(
        key="ch2_similar_meaning",
        title="第2部 性質別 2章 意味が似ている言葉（副詞・形容詞 / 名詞・動詞）",
        pages=(113, 124),
        printed_offset=SK_MAIN,
        note="**Same-field families for the two-branch distractor rule.** Words "
             "close enough in meaning to be a real 言い換え類義 distractor, with "
             "the boundary that separates them.",
    ),
    R.Section(
        key="ch3_similar_form",
        title="第2部 性質別 3章 形が似ている言葉",
        pages=(125, 130),
        printed_offset=SK_MAIN,
        note="**Same-shape families for the other branch of the same rule** — "
             "pairs that look or sound alike, the raw material of a 問題2 "
             "orthography distractor and of a 形が似ている 文脈規定 trap.",
    ),
    R.Section(
        key="ch4_adverbs",
        title="第2部 性質別 4章 副詞（程度・時間・頻度 / 後ろに決まった表現 / まとめて）",
        pages=(131, 148),
        printed_offset=SK_MAIN,
        note="Adverbs by class, including the ones that REQUIRE a fixed "
             "sentence ending. That constraint is a distractor generator and an "
             "item-integrity check at once: an adverb option whose carrier "
             "sentence cannot host it is not a defensible distractor, it is a "
             "giveaway.",
    ),
    R.Section(
        key="ch5_onomatopoeia",
        title="第2部 性質別 5章 オノマトペ",
        pages=(149, 154),
        printed_offset=SK_MAIN,
        note="The N2 オノマトペ inventory with its carriers. Mostly kana, so this "
             "is among the cleanest OCR in the file.",
    ),
    R.Section(
        key="ch6_idioms",
        title="第2部 性質別 6章 慣用表現（体の言葉①②・その他）",
        pages=(155, 166),
        printed_offset=SK_MAIN,
        note="Body-part idioms and other fixed expressions, with the meaning "
             "gloss each one needs to be keyable.",
    ),
    R.Section(
        key="ch7_word_formation",
        title="第2部 性質別 7章 語形成（二語プラス / 前に漢字 / 後ろに漢字 / 形容詞から作る動詞・名詞）",
        pages=(167, 192),
        printed_offset=SK_MAIN,
        note="**The 問題3 語形成 pool authority** — the affixes and compounding "
             "patterns the exam's 語形成 items are built from, split the same "
             "four ways this repo's `word_formation` pool is.",
    ),
    R.Section(
        key="mogi1",
        title="模擬試験 第1回（typeset 語彙 paper, 50点）",
        pages=(193, 194),
        printed_offset=SK_MAIN,
        underlines=True,
        note="A complete, exactly typeset 語彙 paper: 語形成 5 / 文脈規定 5 / "
             "言い換え類義 5 / 用法 5, i.e. this repo's 問題3–問題6. **No 問題1 "
             "and no 問題2** — a 語彙 volume has no 漢字読み section, so this "
             "cannot settle 問題1's target-type mix (see the script docstring). "
             "The 言い換え類義 targets are marked with a printed underline, and "
             "this section is scanned for it in the pixels: look for the "
             "`↳ underline ≈` annotations. Keys: the 別冊 section below.",
    ),
    R.Section(
        key="mogi2",
        title="模擬試験 第2回（typeset 語彙 paper, 50点）",
        pages=(195, 196),
        printed_offset=SK_MAIN,
        underlines=True,
        note="The second paper, same four sections and the same caveat.",
    ),
    R.Section(
        key="mogi_answers",
        title="別冊解答 — 模擬試験 第1回・第2回 の解答",
        pages=(245, 245),
        printed_offset=SK_BESSATSU,
        columns=False,   # the key is a wide table; a gutter split shuffles it
        note="The keys for both 模擬試験, four rows per paper (1.=語形成, "
             "2.=文脈規定, 3.=言い換え類義, 4.=用法), five circled item numbers "
             "each. Circled digits are the weakest thing Vision reads here — "
             "`①` often lands as `日`/`口`/`1` — so the reading is answer-only: "
             "take the digit AFTER each marker in order, and check the page "
             "before quoting a key.",
    ),
]

SOUMATOME = [
    R.Section(
        key="week5_easy_kanji",
        title="第5週 やさしい漢字で書きますが…（＋7日目 実戦問題）",
        pages=(76, 91),
        printed_offset=SM_MAIN,
        underlines=True,
        note="**This is the 問題1/問題2 target band, exactly.** Words written "
             "with easy kanji whose READING is the trap — 物事・日中・年月・"
             "夜中・世間・作業・一生・用心・見事・土地・名字・発売・手品・合図・"
             "強気・本気・気楽・目安. If a 問題1 key is not the kind of word this "
             "week teaches, that is a band signal worth acting on. The 7日目 "
             "実戦問題 is a typeset 問題1(文脈規定)–問題4(用法) set; it too has "
             "no 漢字読み section.",
    ),
    R.Section(
        key="week6_katakana_similar",
        title="第6週 まとめて覚えましょう①（カタカナで書く言葉①②③ / 似ている言葉①②③）",
        pages=(92, 107),
        printed_offset=SM_MAIN,
        underlines=True,
        note="The katakana inventory, and three days of 似ている言葉 — the "
             "same-shape family source the two-branch distractor rule needs, "
             "as a second opinion on Shin Kanzen's 形が似ている言葉.",
    ),
    R.Section(
        key="week7_multi_sense",
        title="第7週 まとめて覚えましょう②（意味がたくさんある言葉①②③ / 言葉の前・後ろにつく語）",
        pages=(108, 123),
        printed_offset=SM_MAIN,
        underlines=True,
        note="Multi-sense words (second opinion on Shin Kanzen 1章) and the "
             "prefix/suffix lists — the 語形成 band from the other book.",
    ),
    R.Section(
        key="bessatsu_answers",
        title="別冊 実戦問題 解答・解説",
        pages=(152, 156),
        printed_offset=None,
        note="The 実戦問題 answers and explanations, with EN/ZH/KO glosses in the "
             "book. Note this scan carries only the tail of the 別冊 (it opens "
             "mid-way at 問題4 p.42), so earlier weeks' keys are not in the PDF "
             "at all — not an OCR failure, a missing-pages one.",
    ),
]


def books(which: str) -> list[R.Book]:
    out = []
    if which in ("shinkanzen", "both"):
        if not SK_PDF.is_file():
            sys.exit(f"missing input: {R.rel(SK_PDF)} (AGENTS.md §3)")
        out.append(R.Book(
            path=SK_PDF,
            label="新完全マスター語彙 日本語能力試験N2 — 第2部 性質別 ＋ 模擬試験",
            out=SK_OUT, sections=list(SHINKANZEN), pages_total=246))
    if which in ("soumatome", "both"):
        if not SM_PDF.is_file():
            sys.exit(f"missing input: {R.rel(SM_PDF)} (AGENTS.md §3)")
        out.append(R.Book(
            path=SM_PDF,
            label="日本語総まとめ N2 語彙 — 第5週〜第7週 ＋ 別冊解答",
            out=SM_OUT, sections=list(SOUMATOME), pages_total=156))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", choices=("shinkanzen", "soumatome", "both"),
                    default="both", help="which front-end to run (default both)")
    R.add_common_args(ap)
    args = ap.parse_args()

    selected = books(args.book)
    for book in selected:
        R.select(book, args.only)
    if args.list:
        R.print_sections(selected)
        return
    for book in selected:
        if args.split_pdf:
            R.split_pdf(book.path, book.sections, Path(args.split_pdf))
        stats = R.extract_book(book, "tools/extract_shinkanzen_goi.py",
                              dpi=args.dpi, chunk=args.chunk,
                              keep_ruby=args.keep_ruby,
                              use_columns=not args.no_columns)
        print(f"wrote {R.rel(book.out)}: {stats.pages} pages, {stats.lines} lines, "
              f"mean confidence {stats.mean_conf():.2f}, "
              f"{stats.low_conf_share():.0%} below 0.50, "
              f"{stats.underlines} underlines located")


if __name__ == "__main__":
    main()
