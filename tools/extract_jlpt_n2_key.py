#!/usr/bin/env python3
"""Extract the JLPT N2 answer-key PDF in refs/JLPT_N2_NEW/ into machine-readable keys.

    python3 tools/extract_jlpt_n2_key.py            # write key.md + answer_keys.json
    python3 tools/extract_jlpt_n2_key.py --check    # parse and validate only, write nothing

The key PDF is a grid of small tables, two or three 大問 blocks abreast, and its
linear text extraction interleaves the rows of side-by-side blocks — so this
parses geometry, not text order. Two facts make that exact:

* answers are drawn in **red** (1, 0, 0) and question numbers in **black**, so
  the two are never confused even though both are bare digits;
* an answer sits exactly one row (~17 pt) below its question number and shares
  its column, so pairing is nearest-centre-x within that band.

Everything else (which 大問 a column belongs to, which section a 大問 is in) is
resolved by position too, then checked against the shape an N2 paper must have:
言語知識・読解 numbers run 1..N with no gaps and exactly one answer each, and
each 聴解 大問 restarts at 1. A parse that violates either is a bug, not a
paper — the script exits non-zero rather than writing a wrong key.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import pdfplumber
except ImportError:  # pragma: no cover - dependency guard
    sys.exit("pdfplumber is required: pip install pdfplumber")

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "refs" / "JLPT_N2_NEW"
# macOS stores the Vietnamese filename decomposed (NFD), so match on the
# normalised form rather than globbing the literal "ĐÁP ÁN".
KEY_PDF_MARK = "DAP AN JLPT N2"
JSON_OUT = ARCHIVE / "answer_keys.json"

# Section banners are printed in dark red; answers in pure red; everything else
# black. Compare loosely — the PDF stores them as floats.
RED_ANSWER = (1.0, 0.0, 0.0)
SECTIONS = ("文字・語彙", "文法", "読解", "聴解")
# 文字・語彙/文法/読解 are the three parts of the one 言語知識・読解 booklet, whose
# question numbers run continuously 1..N; 聴解 restarts at 1 inside every 大問.
GENGO_SECTIONS = ("文字・語彙", "文法", "読解")

HEADER_RE = re.compile(r"JLPT\s*[・･]?\s*N2\s*[・･]?\s*(\d{1,2})\s*/\s*(\d{4})")
# A 大問 label is the word 問題 with its number on the line below; the number may
# be full-width (１) or half-width (11), so fold width before reading it.
LABEL_WORD = "問題"

# Geometry, in PDF points, measured on the 2026-04 revision of the key PDF.
ROW_PITCH = 17.0          # one table row
PAIR_MIN, PAIR_MAX = 8.0, 26.0   # vertical gap from a number to its answer
PAIR_MAX_DX = 30.0        # horizontal centre drift allowed within a column
LABEL_DX = 16.0           # a 大問 number sits under its own 問題 word, not right of it
BAND = 3.0                # tolerance for "same row"
# How far a 大問 label may sit from the number row it owns. A label is centred
# vertically in its block, so a two-row 大問 (問題4's 1-12, 問題11's 60-68) puts
# it ~17 pt off its own rows — but the next band down is ~50 pt away, which is
# what keeps this from reaching into a neighbouring block.
ROW_GROUP = 40.0


def norm_digits(text: str) -> str:
    return unicodedata.normalize("NFKC", text).strip()


def strip_accents(text: str) -> str:
    """Fold 'ĐÁP ÁN' to 'DAP AN' so an NFD filename still matches."""
    folded = "".join(c for c in unicodedata.normalize("NFD", text)
                     if not unicodedata.combining(c))
    return folded.replace("Đ", "D").replace("đ", "d")


def centre(word: dict) -> float:
    return (word["x0"] + word["x1"]) / 2


def is_red(word: dict) -> bool:
    c = word.get("non_stroking_color")
    if not isinstance(c, (list, tuple)) or len(c) != 3:
        return False
    r, g, b = c
    return r > 0.9 and g < 0.2 and b < 0.2


def is_coloured(word: dict) -> bool:
    c = word.get("non_stroking_color")
    return isinstance(c, (list, tuple)) and len(c) == 3 and any(v > 0.01 for v in c)


class ParseError(RuntimeError):
    pass


def parse_page(page) -> dict:
    """Return one exam's key from one page of the answer-key PDF."""
    text = page.extract_text() or ""
    m = HEADER_RE.search(unicodedata.normalize("NFKC", text))
    if not m:
        raise ParseError("no 'JLPT N2 <month>/<year>' header")
    month, year = int(m.group(1)), int(m.group(2))

    words = page.extract_words(extra_attrs=["non_stroking_color"])

    # --- section banners: 文字・語彙 / 文法 / 読解 / 聴解, top to bottom ------------
    banners = sorted(
        ((w["top"], w["text"]) for w in words
         if w["text"] in SECTIONS and is_coloured(w) and not is_red(w)),
        key=lambda t: t[0],
    )
    if not banners:
        raise ParseError("no section banners found")

    def section_at(top: float) -> str:
        name = banners[0][1]
        for btop, bname in banners:
            if btop <= top + BAND:
                name = bname
        return name

    # --- 大問 labels: the word 問題 plus the number printed beneath it -----------
    labels = []
    for w in words:
        if w["text"] != LABEL_WORD:
            continue
        below = [
            c for c in words
            if c is not w
            and w["top"] + PAIR_MIN <= c["top"] <= w["top"] + PAIR_MAX
            and abs(c["x0"] - w["x0"]) < LABEL_DX
            and norm_digits(c["text"]).isdigit()
        ]
        if not below:
            raise ParseError(f"問題 label at y={w['top']:.0f} has no number under it")
        num = int(norm_digits(min(below, key=lambda c: c["top"])["text"]))
        labels.append({"n": num, "x0": w["x0"], "top": w["top"],
                       "digit_id": id(min(below, key=lambda c: c["top"])),
                       "section": section_at(w["top"])})
    if not labels:
        raise ParseError("no 問題 labels found")

    label_digit_ids = {lab["digit_id"] for lab in labels}

    def owner_of(num: dict):
        """The 大問 whose column block contains this question number.

        Column layout changes from band to band — 読解 puts 問題12/13/14 three
        abreast where every other band is two — so the block edges must be read
        off the labels of *this* band, never off the whole page.
        """
        near = [lab for lab in labels
                if abs(lab["top"] - num["top"]) <= ROW_GROUP and lab["x0"] <= num["x0"] + 5]
        if not near:
            raise ParseError(
                f"question number {num['text']!r} at "
                f"({num['x0']:.0f},{num['top']:.0f}) has no 問題 label to its left")
        return max(near, key=lambda lab: lab["x0"])

    # --- pair every red answer with the black question number above it ---------
    digits = [w for w in words if norm_digits(w["text"]).isdigit()]
    numbers = [w for w in digits if not is_red(w) and id(w) not in label_digit_ids]
    answers = [w for w in digits if is_red(w)]
    if not answers:
        raise ParseError("no red answer digits found")

    items = []
    for ans in answers:
        above = [
            n for n in numbers
            if PAIR_MIN <= ans["top"] - n["top"] <= PAIR_MAX
            and abs(centre(n) - centre(ans)) <= PAIR_MAX_DX
        ]
        if not above:
            raise ParseError(
                f"red answer {ans['text']!r} at ({ans['x0']:.0f},{ans['top']:.0f}) "
                "has no question number above it")
        num = min(above, key=lambda n: abs(centre(n) - centre(ans)))
        owner = owner_of(num)
        items.append({
            "section": owner["section"],
            "mondai": owner["n"],
            "no": int(norm_digits(num["text"])),
            "answer": int(norm_digits(ans["text"])),
            "_x": centre(ans), "_y": ans["top"],
        })

    items.sort(key=lambda it: (it["_y"], it["_x"]))
    return {
        "exam": f"N2 {month}/{year}",
        "month": month,
        "year": year,
        "items": items,
    }


def finalise(exam: dict) -> dict:
    """Validate the parsed shape and attach 質問1/質問2 sub-labels."""
    items = exam["items"]
    for it in items:
        if not 1 <= it["answer"] <= 4:
            raise ParseError(f"answer {it['answer']} out of range 1..4 "
                             f"({it['section']} 問題{it['mondai']} #{it['no']})")

    gengo = [it for it in items if it["section"] in GENGO_SECTIONS]
    choukai = [it for it in items if it["section"] == "聴解"]
    if not gengo or not choukai:
        raise ParseError("missing a 言語知識・読解 or 聴解 half")

    # 言語知識・読解 numbers are continuous across its three sections, one answer each.
    nums = sorted(it["no"] for it in gengo)
    if nums != list(range(1, len(nums) + 1)):
        missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        raise ParseError(f"言語知識・読解 numbering is not 1..{max(nums)} "
                         f"(missing {missing}, duplicated {dupes})")

    # 大問 numbers ascend without gaps across the whole paper.
    for half, expect_from in ((gengo, 1), (choukai, 1)):
        seen = sorted({it["mondai"] for it in half})
        if seen != list(range(expect_from, expect_from + len(seen))):
            raise ParseError(f"大問 numbers are not contiguous: {seen}")

    # Every 聴解 大問 restarts at 1. 問題5's last item carries two answers
    # (質問1 / 質問2), which is the one legitimate duplicate in the paper.
    for mondai in sorted({it["mondai"] for it in choukai}):
        block = [it for it in choukai if it["mondai"] == mondai]
        nums = [it["no"] for it in block]
        uniq = sorted(set(nums))
        if uniq != list(range(1, len(uniq) + 1)):
            raise ParseError(f"聴解 問題{mondai} numbering is not 1..N: {nums}")
        for n in uniq:
            same = [it for it in block if it["no"] == n]
            if len(same) == 1:
                continue
            if len(same) == 2 and mondai == max(choukai, key=lambda i: i["mondai"])["mondai"]:
                for k, it in enumerate(sorted(same, key=lambda i: i["_x"]), start=1):
                    it["sub"] = f"質問{k}"
                continue
            raise ParseError(f"聴解 問題{mondai} #{n} has {len(same)} answers")

    for it in items:
        it["part"] = "聴解" if it["section"] == "聴解" else "言語知識・読解"
        del it["_x"], it["_y"]
    exam["items"] = items
    return exam


def folder_for(month: int, year: int, folders: list[Path]) -> Path | None:
    """Match 'N2 7/2010' to the folder named '1. N2 7-2010'."""
    for d in folders:
        m = re.search(r"N2\s*[-. ]?\s*(\d{1,2})[-. ](\d{4})", d.name)
        if m and int(m.group(1)) == month and int(m.group(2)) == year:
            return d
    return None


def render_key_md(exam: dict, source: str, page_no: int) -> str:
    lines = [
        f"# {exam['exam']} — 解答（answer key）",
        "",
        "> Machine-extracted by `tools/extract_jlpt_n2_key.py` from",
        f"> `{source}`, page {page_no}. Regenerate rather than hand-edit.",
        "",
    ]
    for part in ("言語知識・読解", "聴解"):
        rows = [it for it in exam["items"] if it["part"] == part]
        if not rows:
            continue
        lines += [f"## {part}", ""]
        for section in SECTIONS:
            block = [it for it in rows if it["section"] == section]
            if not block:
                continue
            if part == "言語知識・読解":
                lines += [f"### {section}", ""]
            lines += ["| 大問 | 設問 → 解答 |", "| --- | --- |"]
            for mondai in sorted({it["mondai"] for it in block}):
                cells = [
                    f"{it['no']}{('（' + it['sub'] + '）') if it.get('sub') else ''}→**{it['answer']}**"
                    for it in sorted(block, key=lambda i: (i["no"], i.get("sub", "")))
                    if it["mondai"] == mondai
                ]
                lines.append(f"| 問題{mondai} | {' / '.join(cells)} |")
            lines.append("")
        flat = " ".join(
            f"{it['no']}{it.get('sub', '')}:{it['answer']}"
            for it in rows
        ) if part == "言語知識・読解" else " ".join(
            f"問{it['mondai']}-{it['no']}{it.get('sub', '')}:{it['answer']}"
            for it in rows
        )
        lines += [f"全解答（flat）: `{flat}`", ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, help="key PDF (default: the one in refs/JLPT_N2_NEW/)")
    ap.add_argument("--check", action="store_true",
                    help="parse and validate only; write nothing")
    args = ap.parse_args()

    pdf_path = args.pdf
    if pdf_path is None:
        found = sorted(p for p in ARCHIVE.glob("*.pdf")
                       if KEY_PDF_MARK in strip_accents(p.name).upper())
        if len(found) != 1:
            sys.exit(f"expected exactly one {KEY_PDF_MARK} PDF in {ARCHIVE}, "
                     f"found {len(found)}")
        pdf_path = found[0]
    if not pdf_path.is_file():
        sys.exit(f"not a file: {pdf_path}")

    rel = pdf_path.relative_to(ROOT).as_posix() if pdf_path.is_relative_to(ROOT) else str(pdf_path)
    sha = hashlib.sha1(pdf_path.read_bytes()).hexdigest()[:12]
    folders = sorted(d for d in ARCHIVE.iterdir() if d.is_dir())

    exams: dict[str, dict] = {}
    errors: list[str] = []
    unmatched: list[str] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            try:
                exam = finalise(parse_page(page))
            except ParseError as e:
                text = (page.extract_text() or "")
                if HEADER_RE.search(unicodedata.normalize("NFKC", text)):
                    errors.append(f"page {page_no}: {e}")
                continue  # cover page and anything else with no exam header
            folder = folder_for(exam["month"], exam["year"], folders)
            exam["key_page"] = page_no
            exam["folder"] = folder.name if folder else None
            key = folder.name if folder else exam["exam"]
            if key in exams:
                errors.append(f"page {page_no}: duplicate exam {key}")
            exams[key] = exam
            if folder is None:
                unmatched.append(exam["exam"])
            elif not args.check:
                (folder / "key.md").write_text(
                    render_key_md(exam, rel, page_no), encoding="utf-8")

    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    for u in unmatched:
        print(f"warning: no folder under {ARCHIVE.name}/ for {u} — key.md not written",
              file=sys.stderr)
    for d in folders:
        if not any(x.get("folder") == d.name for x in exams.values()):
            print(f"warning: no key page for folder {d.name!r}", file=sys.stderr)

    if not args.check:
        JSON_OUT.write_text(json.dumps({
            "generated_by": "tools/extract_jlpt_n2_key.py",
            "source_pdf": rel,
            "source_sha1": sha,
            "exams": exams,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total = sum(len(e["items"]) for e in exams.values())
    verb = "validated" if args.check else "wrote"
    print(f"{verb} {len(exams)} exams / {total} answers"
          + ("" if args.check else f" -> {JSON_OUT.relative_to(ROOT)} + per-test key.md"))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
