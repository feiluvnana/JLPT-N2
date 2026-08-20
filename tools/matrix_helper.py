#!/usr/bin/env python3
"""
2x2 Cartesian Matrix VALIDATOR for JLPT N2 問題1 (漢字読み) and 問題2 (表記).

`validate` is the only working subcommand. The two GENERATORS were hard-disabled
2026-08-20 (qa-report-20260819_1 F4) — see `_GENERATOR_REMOVED` below for why.

Usage:
    python3 tools/matrix_helper.py validate --reading かいてん 回転 回体 同転 同体
    python3 tools/matrix_helper.py validate むじゅん むじゅう ぶじゅん ぶじゅう

`--reading <かな>` is REQUIRED whenever the options contain kanji (問題2 表記
grids): without it nothing checks the kana skeleton, which is the check
`moji-goi.md` §問題2 actually names. 問題1 reading grids are pure kana, so there
is no skeleton to derive and the Cartesian shape is all this tool can certify —
it says so in its own PASS string.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KANJI = re.compile(r"[㐀-䶿一-鿿]")
KATAKANA_TO_HIRAGANA = str.maketrans(
    "".join(chr(c) for c in range(0x30A1, 0x30F7)),
    "".join(chr(c - 0x60) for c in range(0x30A1, 0x30F7)))

# 連濁 (sequential voicing) and 半濁音: a compound's non-initial element may voice.
RENDAKU = {"か": "が", "き": "ぎ", "く": "ぐ", "け": "げ", "こ": "ご",
           "さ": "ざ", "し": "じ", "す": "ず", "せ": "ぜ", "そ": "ぞ",
           "た": "だ", "ち": "ぢ", "つ": "づ", "て": "で", "と": "ど",
           "は": "ば", "ひ": "び", "ふ": "ぶ", "へ": "べ", "ほ": "ぼ"}
HANDAKU = {"は": "ぱ", "ひ": "ぴ", "ふ": "ぷ", "へ": "ぺ", "ほ": "ぽ"}

_GENERATOR_REMOVED = """\
The `{cmd}` GENERATOR is disabled — it never had a 音訓 table, so it invented
readings and glyphs (qa-report-20260819_1 F4, Stage 2 handoff of 20260819_1):

  matrix_helper.py reading 方角 ほうがく  ->  {{ほう, ほ}} x {{がく, がう}}
      「ほ」 is not a reading of 方; 「がう」 is not a reading of 角.
  matrix_helper.py orthography 回転     ->  {{回, 同}} x {{転, 体}}
      同=ドウ, 体=タイ, so 同転/回体/同体 do not read かいてん — the exact
      運海/雲海 collapse `moji-goi.md` §問題2 documents as the 20260817_3
      問題2-9 defect. `COMPONENT_SUBSTITUTIONS` held 36 entries and fell back
      to 同/体 for the other ~2100 常用漢字.

Build the grid BY HAND against `question-authoring/references/moji-goi.md`
(§問題1 "the 2x2 Cartesian product matrix" / §問題2 "Procedure — write the
reading of each COMPONENT before you accept the grid"), then check it here:

  python3 tools/matrix_helper.py validate --reading <かな> <4 options>
"""


def _kanji_readings(ch: str) -> set[str] | None:
    """Every reading `pykakasi`'s kanwa dictionary carries for one kanji.

    `pykakasi` is already a REQUIRED dependency of this repo (README
    Prerequisites #2 — the booklet furigana pass reads it), so this adds no
    install step. Returns None when the character is not in the dictionary at
    all, which the caller treats as "cannot verify" and FAILS on: an unknown
    glyph must never certify a grid.
    """
    try:
        from pykakasi.kanji import Kanwa
    except Exception:                                   # pragma: no cover
        return None
    table = Kanwa().load(ch)
    if not table or ch not in table:
        return None
    out = set()
    for yomi, _ in table[ch]:
        y = str(yomi).translate(KATAKANA_TO_HIRAGANA)
        if y:
            out.add(y)
    return out or None


def _variants(reading: str, first: bool) -> set[str]:
    """`reading` plus the compound-internal alternations official actually uses."""
    out = {reading}
    if not first and reading[0] in RENDAKU:
        out.add(RENDAKU[reading[0]] + reading[1:])
    if not first and reading[0] in HANDAKU:
        out.add(HANDAKU[reading[0]] + reading[1:])
    if first and reading.endswith(("つ", "ち", "く", "き")):
        out.add(reading[:-1] + "っ")                    # 促音便: 出(しゅつ)荷 -> しゅっか
    return out


def reads_as(word: str, kana: str) -> tuple[bool, str]:
    """Can `word`'s characters be read as `kana`? -> (verdict, explanation).

    Segments `kana` across the characters of `word`, requiring each kanji to
    own its chunk in the 音訓 dictionary (allowing 連濁/半濁/促音便). Kana
    characters in `word` must match themselves.
    """
    kana = kana.translate(KATAKANA_TO_HIRAGANA)
    unknown = [c for c in word if KANJI.match(c) and _kanji_readings(c) is None]
    if unknown:
        return False, (f"no 音訓 entry for {'/'.join(unknown)} — this tool "
                       f"cannot certify a glyph it cannot read")
    trace: list[str] = []

    def rec(i: int, j: int) -> bool:
        if i == len(word):
            return j == len(kana)
        ch = word[i]
        if not KANJI.match(ch):
            if kana.startswith(ch, j):
                trace.append(f"{ch}={ch}")
                if rec(i + 1, j + len(ch)):
                    return True
                trace.pop()
            return False
        readings = _kanji_readings(ch) or set()
        for length in range(len(kana) - j, 0, -1):
            chunk = kana[j:j + length]
            if any(chunk in _variants(r, i == 0) for r in readings):
                trace.append(f"{ch}={chunk}")
                if rec(i + 1, j + length):
                    return True
                trace.pop()
        return False

    if rec(0, 0):
        return True, " ".join(trace)
    return False, f"「{word}」 has no reading segmentation that yields 「{kana}」"


def validate_matrix(options: list[str]) -> bool:
    """Do 4 options form a strict 2x2 Cartesian product {A,B} x {C,D}?"""
    if len(options) != 4 or len(set(options)) != 4:
        return False
    for split_idx in range(1, max(len(o) for o in options)):
        prefixes = {o[:split_idx] for o in options}
        suffixes = {o[split_idx:] for o in options}
        if len(prefixes) == 2 and len(suffixes) == 2:
            if {p + s for p in prefixes for s in suffixes} == set(options):
                return True
    return False


def validate_skeleton(options: list[str], reading: str) -> list[str]:
    """Every option must READ as `reading`. Returns the failures, one line each.

    THIS is the check `moji-goi.md` §問題2 calls "the check": 「A complete
    component grid is NOT the check; the kana skeleton is.」 `validate` used to
    return PASS on 回転/回体/同転/同体 — a perfect Cartesian grid in which three
    of four options cannot be read かいてん — so a 解説 could cite the tool as
    skeleton evidence it never produced (qa-report-20260819_1 F4).
    """
    bad = []
    for o in options:
        ok, why = reads_as(o, reading)
        if not ok:
            bad.append(f"「{o}」: {why}")
    return bad


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command")

    for cmd, helptext in (("reading", "DISABLED — build 問題1 grids by hand"),
                          ("orthography", "DISABLED — build 問題2 grids by hand")):
        p = sub.add_parser(cmd, help=helptext)
        p.add_argument("args", nargs="*")

    p_val = sub.add_parser(
        "validate", help="Check 4 options: Cartesian shape + (with --reading) kana skeleton")
    p_val.add_argument("opts", nargs=4, help="Four options to check")
    p_val.add_argument("--reading", default=None,
                       help="the stem kana every option must read as; REQUIRED "
                            "when the options contain kanji (問題2 表記 grids)")

    args = ap.parse_args()

    if args.command in ("reading", "orthography"):
        sys.exit(_GENERATOR_REMOVED.format(cmd=args.command))

    if args.command == "validate":
        cartesian = validate_matrix(args.opts)
        has_kanji = any(KANJI.search(o) for o in args.opts)
        if has_kanji and not args.reading:
            sys.exit("validate: --reading <かな> is REQUIRED for a grid whose "
                     "options contain kanji — without it nothing checks the kana "
                     "skeleton, and a complete Cartesian grid is NOT the check "
                     "(moji-goi.md §問題2). Example:\n"
                     "  matrix_helper.py validate --reading かいてん 回転 回体 同転 同体")
        skeleton = validate_skeleton(args.opts, args.reading) if args.reading else None

        if not cartesian:
            print("2x2 Cartesian Matrix Check: FAIL (Asymmetric Options)")
        if skeleton:
            print("Kana skeleton check: FAIL")
            for line in skeleton:
                print(f"  {line}")
        if cartesian and skeleton is None:
            print("2x2 Cartesian Matrix Check: PASS (Cartesian shape only — the "
                  "kana skeleton is NOT checked; pass --reading, or verify every "
                  "option by hand against moji-goi.md §問題1's RESOLVE procedure)")
        elif cartesian and not skeleton:
            print(f"2x2 Cartesian Matrix Check: PASS (Cartesian shape AND kana "
                  f"skeleton — all four options read 「{args.reading}」)")
            for o in args.opts:
                print(f"  {o}: {reads_as(o, args.reading)[1]}")
        sys.exit(0 if cartesian and not skeleton else 1)

    ap.print_help()


if __name__ == "__main__":
    main()
