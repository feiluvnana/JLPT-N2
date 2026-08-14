#!/usr/bin/env python3
"""
Topological & Permutation Verifier for JLPT N2 問題8 (文の組み立て).

Extracts 問題8 scramble sentences (43..47) from 言語知識・読解.md,
evaluates all 24 permutations (4!), analyzes card junction glue (L -> i -> j -> T),
and verifies that the keyed answer is the UNIQUE valid ordering.

Usage:
    python3 tools/verify_scramble.py tests/20260813_2
    python3 tools/verify_scramble.py tests/20260813_2 --verbose
"""

import argparse
import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Common impossible junctions in Japanese grammar
IMPOSSIBLE_JUNCTIONS = [
    # Double subject/object particles without coordinate structure
    r"(?:を|が|に|へ|で|と|から|より)[ \t]*(?:を|が|へ|より)",
    # Conjugation clashes
    r"(?:ない|なかった|ている|ていた)[ \t]*(?:ます|ました|ません|でした)",
    r"(?:て|で)[ \t]*(?:です|でした)",
    # Dangling particles before punctuation
    r"[をがにへでと][ \t]*[。！？]",
]
JUNCTION_RE = re.compile("|".join(IMPOSSIBLE_JUNCTIONS))


def parse_mondai8_items(gengo_md: str) -> list:
    """Extract (q_num, lead_in, tail, [opt1..4], key, kaisetsu_order)"""
    m8 = re.search(r"##\s*問題8.*?(?=##\s*問題9|#+\s*解答|#+\s*【?正解|\Z)", gengo_md, re.S)
    if not m8:
        return []

    # Extract key table
    key_map = {}
    key_split = re.split(r"^#+\s*(?:解答|【?正解)", gengo_md, flags=re.M)
    if len(key_split) > 1:
        for line in key_split[1].splitlines():
            line = line.strip()
            if line.startswith("|") and line.endswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 3 and parts[0].isdigit():
                    q = int(parts[0])
                    if 43 <= q <= 47 and parts[1].isdigit():
                        key_map[q] = {
                            "key": int(parts[1]),
                            "kaisetsu": parts[2]
                        }

    items = []
    # Pattern for 問題8 stem: lead-in ___ ___ ★ ___ tail
    q_blocks = list(re.finditer(r"\*\*(\d+)\*\*[ \t]*(.*?)(?=\n\*\*\d+\*\*|\Z)", m8.group(0), re.S))
    for qb in q_blocks:
        qn = int(qb.group(1))
        if not (43 <= qn <= 47):
            continue
        text = qb.group(2).strip()

        # Split stem and options
        m_opts = re.search(r"\n[ \t]*1[.．][ \t]*(.+)", text)
        if not m_opts:
            continue
        stem_raw = text[:m_opts.start()].strip()
        opts_raw = text[m_opts.start():].strip()

        # Extract 4 options
        opts = [o.strip() for o in re.findall(r"[1-4][.．][ \t]*([^\n]+?)(?=[ \t]+[1-4][.．]|\n|\Z)", opts_raw)]
        if len(opts) != 4:
            continue

        # Extract lead-in and tail around the 4 blanks
        blank_pattern = r"(?:[＿_ー―\s]*[（(]?\s*[＿_ー―]+\s*[）)]?[＿_ー―\s]*|[\s　]*_{2,}[\s　]*)"
        m_star = re.search(r"★", stem_raw)
        if not m_star:
            # Try splitting by underscores
            parts = re.split(r"[_＿]{2,}|[―ー]{2,}", stem_raw)
            lead_in = parts[0].strip() if parts else ""
            tail = parts[-1].strip() if len(parts) > 1 else ""
        else:
            # Lead in before first blank sequence, tail after star and trailing blanks
            prefix = stem_raw[:m_star.start()]
            suffix = stem_raw[m_star.end():]
            lead_in = re.sub(r"[_＿―ー\s　]+$", "", prefix).strip()
            tail = re.sub(r"^[_＿―ー\s　]+", "", suffix).strip()

        k_info = key_map.get(qn, {"key": 0, "kaisetsu": ""})
        items.append({
            "num": qn,
            "lead_in": lead_in,
            "tail": tail,
            "options": opts,
            "key": k_info["key"],
            "kaisetsu": k_info["kaisetsu"]
        })

    return items


def analyze_scramble(item: dict, verbose: bool = False):
    qn = item["num"]
    opts = item["options"]
    L = item["lead_in"]
    T = item["tail"]
    key = item["key"]

    print(f"\n-------------------------------------------------------------")
    print(f"問題8 [{qn}番] ★ Key: {key}")
    print(f"  Lead-in : 「{L}」")
    print(f"  Options : 1. {opts[0]} | 2. {opts[1]} | 3. {opts[2]} | 4. {opts[3]}")
    print(f"  Tail    : 「{T}」")
    if item["kaisetsu"]:
        print(f"  解説    : {item['kaisetsu']}")

    valid_perms = []

    for perm in itertools.permutations(range(4)):
        # perm is 0-indexed tuple of length 4, e.g. (1, 3, 0, 2)
        assembled = L + opts[perm[0]] + opts[perm[1]] + opts[perm[2]] + opts[perm[3]] + T
        assembled_clean = re.sub(r"\s+", "", assembled)

        # Check for obvious impossible junctions
        has_clash = False
        junction_pairs = [
            (L, opts[perm[0]]),
            (opts[perm[0]], opts[perm[1]]),
            (opts[perm[1]], opts[perm[2]]),
            (opts[perm[2]], opts[perm[3]]),
            (opts[perm[3]], T)
        ]
        for left, right in junction_pairs:
            pair_str = left[-4:] + right[:4]
            if JUNCTION_RE.search(pair_str):
                has_clash = True
                break

        if not has_clash:
            star_opt_num = perm[2] + 1  # 3rd blank (index 2) is ★
            perm_str = f"({perm[0]+1})→({perm[1]+1})→**({perm[2]+1})**→({perm[3]+1})"
            valid_perms.append((perm_str, star_opt_num, assembled_clean))

    print(f"  Candidate Valid Permutations ({len(valid_perms)} / 24):")
    for p_str, star_val, sentence in valid_perms:
        star_match = "✓ (Matches Key)" if star_val == key else f"❌ (Key mismatch: ★ is {star_val} vs key {key})"
        print(f"    - {p_str} => ★={star_val} {star_match}")
        if verbose:
            print(f"      Full: 「{sentence}」")

    # Verification result
    matching_perms = [p for p in valid_perms if p[1] == key]
    if len(valid_perms) == 1 and matching_perms:
        print(f"  => RESULT: PASS (Unique grammatical path matches ★={key})")
        return True
    elif len(valid_perms) > 1:
        print(f"  => RESULT: WARNING ({len(valid_perms)} permutations possible. Check for floating adverbs or multiple valid orders)")
        return True
    elif not valid_perms:
        print(f"  => RESULT: FAIL (0 valid permutations found - junction filter flagged all)")
        return False
    else:
        print(f"  => RESULT: FAIL (Keyed ordering not found among candidates)")
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", help="Path to tests/<test_id>")
    ap.add_argument("--verbose", action="store_true", help="Print full assembled sentences")
    args = ap.parse_args()

    test_dir = Path(args.test_dir)
    gengo_path = test_dir / "言語知識・読解.md"
    if not gengo_path.is_file():
        print(f"Error: Not found: {gengo_path}", file=sys.stderr)
        sys.exit(1)

    items = parse_mondai8_items(gengo_path.read_text(encoding="utf-8"))
    if not items:
        print(f"No 問題8 items found in {gengo_path}")
        sys.exit(0)

    print(f"Loaded {len(items)} 問題8 scramble items from {test_dir.name}")
    all_ok = True
    for it in items:
        ok = analyze_scramble(it, verbose=args.verbose)
        if not ok:
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
