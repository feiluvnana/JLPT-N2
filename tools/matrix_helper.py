#!/usr/bin/env python3
"""
2x2 Cartesian Matrix Generator & Validator for JLPT N2 問題1 (漢字読み) and 問題2 (表記).

Provides deterministic 2x2 grid generation ({A, B} × {C, D} -> {AC, AD, BC, BD})
to guarantee official JLPT distractor structure, eliminate alien kanji glyphs,
and prevent option generation errors for zero AI tokens.

Usage:
    python3 tools/matrix_helper.py reading "矛盾" "むじゅん"
    python3 tools/matrix_helper.py orthography "下品"
    python3 tools/matrix_helper.py validate "下品" "下晶" "不品" "不晶"
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Common phonological variation pairs for on-reading compounds ({A, B} and {C, D})
ON_READING_VARIATIONS = {
    # Voicing (清濁) pairs
    "か": ["か", "が"], "き": ["き", "ぎ"], "く": ["く", "ぐ"], "け": ["け", "げ"], "こ": ["こ", "ご"],
    "さ": ["さ", "ざ"], "し": ["し", "じ"], "す": ["す", "ず"], "せ": ["せ", "ぜ"], "そ": ["そ", "ぞ"],
    "た": ["た", "だ"], "ち": ["ち", "じ"], "つ": ["つ", "づ"], "て": ["て", "で"], "と": ["と", "ど"],
    "は": ["は", "ば"], "ひ": ["ひ", "び"], "ふ": ["ふ", "ぶ"], "へ": ["へ", "べ"], "ほ": ["ほ", "ぼ"],
    # Length / gemination (長短・促音) pairs
    "しき": ["しき", "じき"], "しょう": ["しょう", "じょう"], "しゅん": ["しゅん", "じゅん"],
    "しゅく": ["しゅく", "じゅく"], "こう": ["こう", "ごう"], "かん": ["かん", "がん"],
    "けい": ["けい", "きょう"], "せい": ["せい", "しょう"], "とう": ["とう", "どう"],
    "ちょう": ["ちょう", "じょう"], "せん": ["せん", "ぜん"], "そう": ["そう", "ぞう"],
    "しん": ["しん", "じん"], "えい": ["えい", "えん"], "よう": ["よう", "ゆう"],
    "やく": ["やく", "えき"], "さく": ["さく", "さつ"], "そく": ["そく", "ぞく"],
}

# Common radical / component substitutions for N2 kanji orthography (問題2)
COMPONENT_SUBSTITUTIONS = {
    "下": ["下", "不"], "品": ["品", "晶"], "運": ["運", "雲"], "河": ["河", "海"],
    "駄": ["駄", "太"], "基": ["基", "規"], "盤": ["盤", "判"], "傾": ["傾", "経"],
    "向": ["向", "効"], "期": ["期", "基"], "地": ["地", "池"], "流": ["流", "留"],
    "威": ["威", "依"], "張": ["張", "貼"], "施": ["施", "設"], "設": ["設", "投"],
    "補": ["補", "捕"], "給": ["給", "級"], "拡": ["拡", "鉱"], "大": ["大", "太"],
    "縮": ["縮", "宿"], "小": ["小", "少"], "改": ["改", "政"], "善": ["善", "膳"],
    "障": ["障", "章"], "害": ["害", "割"], "快": ["快", "情"], "適": ["適", "敵"],
    "精": ["精", "清"], "密": ["密", "蜜"], "経": ["経", "軽"], "営": ["営", "管"],
    "採": ["採", "彩"], "用": ["用", "同"], "提": ["提", "題"], "供": ["供", "共"],
}


def generate_reading_matrix(target_word: str, reading: str) -> dict:
    """Generate 2x2 reading matrix for a 2-kanji on-reading compound."""
    # Split reading into two morae/components
    mid = len(reading) // 2
    if len(reading) >= 4 and reading[1] in "ょゅゃ":
        mid = 2
    elif len(reading) >= 4 and reading[2] in "ょゅゃ":
        mid = 3
    elif len(reading) == 3:
        mid = 1 if reading[0] in "あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわ" else 2

    c1 = reading[:mid]
    c2 = reading[mid:]

    # Find candidate variations
    var1 = ON_READING_VARIATIONS.get(c1, [c1, c1[:-1] + "う" if not c1.endswith("う") else c1[:-1]])
    var2 = ON_READING_VARIATIONS.get(c2, [c2, c2[:-1] + "う" if not c2.endswith("う") else c2[:-1]])

    if len(var1) < 2:
        if c1[0] in "かきくけこさしすせそたちつてとはひふへほ":
            voiced = {"か":"が","き":"ぎ","く":"ぐ","け":"げ","こ":"ご","さ":"ざ","し":"じ","す":"ず","せ":"ぜ","そ":"ぞ","た":"だ","ち":"じ","つ":"づ","て":"で","と":"ど","は":"ば","ひ":"び","ふ":"ぶ","へ":"べ","ほ":"ぼ"}[c1[0]]
            var1 = [c1, voiced + c1[1:]]
        else:
            var1 = [c1, c1 + "う" if len(c1) == 1 else c1[:-1]]

    if len(var2) < 2:
        if c2[0] in "かきくけこさしすせそたちつてとはひふへほ":
            voiced = {"か":"が","き":"ぎ","く":"ぐ","け":"げ","こ":"ご","さ":"ざ","し":"じ","す":"ず","せ":"ぜ","そ":"ぞ","た":"だ","ち":"じ","つ":"づ","て":"で","と":"ど","は":"ば","ひ":"び","ふ":"ぶ","へ":"べ","ほ":"ぼ"}[c2[0]]
            var2 = [c2, voiced + c2[1:]]
        else:
            var2 = [c2, c2[:-1] if c2.endswith("う") else c2 + "う"]

    a1, a2 = var1[0], var1[1]
    b1, b2 = var2[0], var2[1]

    options = [
        a1 + b1,  # Key (AC)
        a1 + b2,  # Distractor 1 (AD)
        a2 + b1,  # Distractor 2 (BC)
        a2 + b2,  # Distractor 3 (BD)
    ]

    return {
        "word": target_word,
        "key_reading": reading,
        "part1_variants": [a1, a2],
        "part2_variants": [b1, b2],
        "options": options,
        "matrix_formula": f"{{{a1}, {a2}}} × {{{b1}, {b2}}}",
    }


def generate_orthography_matrix(target_word: str) -> dict:
    """Generate 2x2 component matrix for a 2-kanji compound (問題2)."""
    if len(target_word) != 2:
        return {"error": "Orthography 2x2 generator requires a 2-kanji compound."}

    k1, k2 = target_word[0], target_word[1]
    c1_opts = COMPONENT_SUBSTITUTIONS.get(k1, [k1, "同"])
    c2_opts = COMPONENT_SUBSTITUTIONS.get(k2, [k2, "体"])

    a1, a2 = c1_opts[0], c1_opts[1]
    b1, b2 = c2_opts[0], c2_opts[1]

    options = [
        a1 + b1,  # Key (AC)
        a1 + b2,  # Distractor 1 (AD)
        a2 + b1,  # Distractor 2 (BC)
        a2 + b2,  # Distractor 3 (BD)
    ]

    return {
        "word": target_word,
        "part1_glyphs": [a1, a2],
        "part2_glyphs": [b1, b2],
        "options": options,
        "matrix_formula": f"{{{a1}, {a2}}} × {{{b1}, {b2}}}",
    }


def validate_matrix(options: list[str]) -> bool:
    """Validate whether 4 options form a strict 2x2 Cartesian product {A,B} x {C,D}."""
    if len(options) != 4:
        return False

    for split_idx in range(1, max(len(o) for o in options)):
        prefixes = {o[:split_idx] for o in options}
        suffixes = {o[split_idx:] for o in options}
        if len(prefixes) == 2 and len(suffixes) == 2:
            expected = {p + s for p in prefixes for s in suffixes}
            if expected == set(options):
                return True

    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command")

    # reading
    p_read = sub.add_parser("reading", help="Generate 2x2 reading matrix for 問題1")
    p_read.add_argument("word", help="Target kanji word (e.g. 矛盾)")
    p_read.add_argument("reading", help="Target reading (e.g. むじゅん)")

    # orthography
    p_orth = sub.add_parser("orthography", help="Generate 2x2 orthography matrix for 問題2")
    p_orth.add_argument("word", help="Target kanji word (e.g. 下品)")

    # validate
    p_val = sub.add_parser("validate", help="Validate 4 options against 2x2 Cartesian rule")
    p_val.add_argument("opts", nargs=4, help="Four options to check")

    args = ap.parse_args()

    if args.command == "reading":
        res = generate_reading_matrix(args.word, args.reading)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.command == "orthography":
        res = generate_orthography_matrix(args.word)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.command == "validate":
        ok = validate_matrix(args.opts)
        print(f"2x2 Cartesian Matrix Check: {'PASS (Valid Grid)' if ok else 'FAIL (Asymmetric Options)'}")
        sys.exit(0 if ok else 1)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
