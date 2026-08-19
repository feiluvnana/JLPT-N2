#!/usr/bin/env python3
"""
Topological & Permutation Verifier for JLPT N2 問題8 (文の組み立て).

Extracts 問題8 scramble sentences (43..47) from 言語知識・読解.md, enumerates all
24 orderings, filters them through a SMALL list of impossible junctions, and
checks the keyed ★ against whatever survives.

WHAT THIS TOOL CAN AND CANNOT DECIDE — read before trusting a line of output.

`IMPOSSIBLE_JUNCTIONS` knows four patterns (stacked case particles, a handful of
conjugation clashes, a dangling particle before punctuation). Japanese
word-order uniqueness turns on semantics and on connective subcategorisation,
neither of which is in that list, so a surviving permutation is NOT a
grammatical sentence and 「24 permutations possible」 is NOT a finding. Until
2026-08-19 the tool printed exactly that line for every item of every paper —
`RESULT: WARNING (24 permutations possible)` — and returned success, so it read
the same for a sound item and for a broken one and decided nothing. A genuine
second defensible answer at 20260817_3 問題8-44 went straight through it
(qa-report-20260817_3 F1).

So the tool now decides TWO things, and says which is which:

  1. NEGATIVE evidence it really has: the keyed ★ is not among the surviving
     orderings, or the junction filter killed every ordering. Both are FAIL.
  2. The AUTHOR'S ARTIFACT: the item's 解説 must carry a per-card uniqueness
     proof that includes the LAST SLOT — for each card, why it cannot be the
     final card before the fixed tail. That is what 問題8-44's author never
     wrote and what the reviewer had to reconstruct by hand; it is required
     here, and a missing one is a FAIL.

Uniqueness itself is still the 解説's claim, not this tool's finding. When more
than one ordering survives the filter, the verdict is UNDECIDED, never WARNING.

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


# The 解説's uniqueness proof has to cover the LAST slot, not just the tested
# connective's own junction. 問題8-44 shipped with a proof that 「テ形『見て』は
# 『うえで』に接続できない」 — true, and it only blocks 見て BEFORE うえで; it
# never rules out 見て as the FINAL card, which is exactly the rival ordering QA
# found. One of these phrases must appear, and every card must be named.
LAST_SLOT_MARKERS = ("最終スロット", "最後のスロット", "末尾スロット", "最終位置",
                     "最後には立て", "最後に立て", "末尾に立て", "文末に置け",
                     "最終スロットの証明", "最後のカード")
PROOF_PREFIX = 4        # chars of a card that count as "the 解説 names it"


def missing_proof(item: dict) -> str:
    """'' when the 解説 carries a last-slot proof naming every card."""
    text = re.sub(r"\s", "", item.get("kaisetsu", ""))
    if not text:
        return "no 解説 cell for this item"
    gaps = []
    if not any(mk in text for mk in LAST_SLOT_MARKERS):
        gaps.append("no last-slot proof (say, per card, why it cannot be the "
                    "FINAL card before the fixed tail — a junction argument "
                    "about the tested connective does not cover slot 4)")
    unnamed = [o for o in item["options"]
               if re.sub(r"\s", "", o)[:PROOF_PREFIX] not in text]
    if unnamed:
        gaps.append("cards never named in the proof: "
                    + " / ".join(f"「{o}」" for o in unnamed))
    return "; ".join(gaps)


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
            lseg = left[-4:]
            pair_str = lseg + right[:4]
            boundary = len(lseg)
            # A junction defect is a clash AT THE SEAM between two adjacent
            # option strings — a match that lands entirely inside one side's
            # own text (e.g. こと's own と + a real trailing object/subject
            # particle: 「会議のことを」, 「両親のことが」) is not a junction at
            # all, and previously self-triggered a FAIL on both option's own
            # tail regardless of what actually sits next to it (20260817_1 QA
            # G-NEW-2: items 46/47, a common, grammatical ことを/ことが
            # construction, both flagged "0 valid permutations").
            if any(mo.start() < boundary < mo.end()
                   for mo in JUNCTION_RE.finditer(pair_str)):
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

    # The author's artifact, checked before the permutation verdict because it
    # is the only uniqueness EVIDENCE that exists (see the module docstring).
    missing = missing_proof(item)
    if missing:
        print(f"  => ARTIFACT: MISSING — {missing}")
    else:
        print(f"  => ARTIFACT: ok (解説 carries a last-slot proof naming every card)")

    matching_perms = [p for p in valid_perms if p[1] == key]
    if not valid_perms:
        print(f"  => RESULT: FAIL (0 orderings survive the junction filter — "
              f"the filter is crude, so this usually means a card was "
              f"mis-transcribed, not that the item is unsolvable)")
        return False
    if not matching_perms:
        print(f"  => RESULT: FAIL (the keyed ★={key} is not among the "
              f"{len(valid_perms)} surviving orderings — the key names a card "
              f"the tool cannot place in slot 3)")
        return False
    if len(valid_perms) == 1:
        print(f"  => RESULT: PASS (one ordering survives and its ★={key} "
              f"matches; uniqueness is still the 解説's claim, not this "
              f"tool's finding)")
        return not missing
    others = sorted({p[1] for p in valid_perms} - {key})
    print(f"  => RESULT: UNDECIDED — {len(valid_perms)} of 24 orderings survive "
          f"a filter that knows {len(IMPOSSIBLE_JUNCTIONS)} junction patterns, "
          f"so this tool has NOT verified uniqueness. Rival ★ values among the "
          f"survivors: {others or 'none'}. The 解説's per-card proof, including "
          f"the LAST slot, is the evidence — read it against these orderings.")
    return not missing


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

    print("\n-------------------------------------------------------------")
    print("This tool decides two things: whether the keyed ★ survives its own "
          "junction filter, and whether the 解説 carries the per-card "
          "last-slot proof. It does NOT decide uniqueness — read the module "
          "docstring before quoting an UNDECIDED line as a pass.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
