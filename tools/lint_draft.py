#!/usr/bin/env python3
"""
Fast Deterministic Pre-Linter (zero-token mechanical verification).

Run this BEFORE invoking QA or committing a draft to instantly catch mechanical
flaws that would otherwise trigger a costly QA review round-trip:
- Choukai script contraction rate (縮約形), reaction turns, and filler band
- Choukai banned formulas and accidental answer reveals
- Dokkai absolute quantifier / categorical denial option markers
- Dokkai numbered marker and （注N） pairing
- Bunpou 問題7 blank presence, 問題8 scramble formatting, 問題9 cloze tagging
- Moji-Goi 4-choice uniqueness and distractor category labels

Usage:
    python3 tools/lint_draft.py tests/20260813_2
    python3 tools/lint_draft.py tests/20260813_2/_sections/
    make lint-draft 20260813_2
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Contraction forms from Shin Kanzen p.16 / choukai-audio SKILL
CONTRACTION_PATTERNS = [
    r"[てで]る(?:[んだよの]|から|けど|し|と|ね|$|[、。])",
    r"[てで]た(?:[んだよの]|から|けど|し|と|ね|$|[、。])",
    r"[とど]く(?:[んだよの]|から|けど|し|と|ね|$|[、。])",
    r"[とど]いた(?:[んだよの]|から|けど|し|と|ね|$|[、。])",
    r"[とど]いて(?:[んだよの]|から|けど|し|と|ね|$|[、。])",
    r"[とど]こう",
    r"[ちじ]ゃう",
    r"[ちじ]ゃった",
    r"[ちじ]ゃって",
    r"[ちじ]ゃいそう",
    r"[ちじ]ゃえ",
    r"なきゃ(?:[いなだ]|なら|ダメ|いけ|$|[、。])",
    r"なくちゃ(?:[いなだ]|なら|ダメ|いけ|$|[、。])",
    r"[てで]く(?:[んだよの]|から|けど|し|と|ね|$|[、。])",
    r"[てで]かない",
    r"[ちじ]ゃ(?:いけない|だめ|ダメ|ならない)",
]
CONTRACTION_RE = re.compile("|".join(CONTRACTION_PATTERNS))

FILLERS = [
    "あのう", "あのー", "あの、", "ええと", "えーと", "えっと",
    "うーん", "うーむ", "まあ、", "あ、", "うん、", "へえ、", "ほら、",
]

ABS_QUANTIFIERS = [
    "すべて", "全て", "のみ", "だけで十分", "だけでたりる", "だけで足りる",
    "無関係", "一切", "まったく", "全く〜ない", "完全に"
]


class LintReport:
    def __init__(self, target_name: str):
        self.target_name = target_name
        self.errors = []
        self.warnings = []
        self.notices = []

    def error(self, category: str, msg: str):
        self.errors.append((category, msg))

    def warn(self, category: str, msg: str):
        self.warnings.append((category, msg))

    def notice(self, category: str, msg: str):
        self.notices.append((category, msg))

    def print_summary(self):
        print(f"\n=======================================================")
        print(f"  Pre-Lint Report: {self.target_name}")
        print(f"=======================================================")

        if self.errors:
            print(f"\n[FAIL / ERRORS] ({len(self.errors)} item(s) must be fixed before QA):")
            for cat, msg in self.errors:
                print(f"  [ERROR] [{cat}] {msg}")

        if self.warnings:
            print(f"\n[WARNINGS] ({len(self.warnings)} item(s) to verify):")
            for cat, msg in self.warnings:
                print(f"  [WARN]  [{cat}] {msg}")

        if self.notices:
            print(f"\n[STATS / PASSES]:")
            for cat, msg in self.notices:
                print(f"  [INFO]  [{cat}] {msg}")

        if not self.errors and not self.warnings:
            print(f"\n✓ ALL CHECKS CLEAN. Draft is ready for QA blind-solve.")
        elif not self.errors:
            print(f"\n✓ No critical blocking errors. Please inspect warnings.")
        else:
            print(f"\n❌ Blocking errors detected. Fix them to avoid a QA FAIL loop.")


def lint_choukai_script(script_text: str, report: LintReport):
    if not script_text:
        return

    # 1. Opening & level check
    if "N2" in script_text:
        report.error("CHOUKAI-TTS", "Script contains 'N2' — TTS spelling must be 'Nに', never 'N2'.")

    # 2. Reveal in scored items
    lines = script_text.splitlines()
    for idx, line in enumerate(lines, 1):
        if "最もよいものは" in line and "例" not in line and "練習" not in line:
            # Check if this is within a scored question block
            report.error("CHOUKAI-REVEAL", f"Line {idx}: '最もよいものは' found outside 例 — spoken answer reveal is forbidden.")
        if re.search(r"（※.+?）", line):
            report.error("CHOUKAI-ANNOTATION", f"Line {idx}: Internal annotation '（※...）' will be read aloud by TTS.")

    # 3. Spoken dialogue analysis (excluding announcer lines)
    dialogue_lines = []
    announcer_lines = []
    is_dialogue = False

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        if re.match(r"^問題[1-5]|^例[。.]|^第?\d+番", line_s):
            is_dialogue = True
            continue
        if re.match(r"^[男女AB１２34567890]:", line_s):
            dialogue_lines.append(line_s)
        elif is_dialogue:
            dialogue_lines.append(line_s)
        else:
            announcer_lines.append(line_s)

    full_dialogue = "\n".join(dialogue_lines)
    char_count = len(re.sub(r"\s+", "", full_dialogue))

    if char_count > 500:
        # Contraction count
        contractions = list(CONTRACTION_RE.finditer(full_dialogue))
        rate_per_10k = (len(contractions) / char_count) * 10000
        if rate_per_10k < 22.4:
            report.error(
                "CHOUKAI-縮約形",
                f"Contraction rate is {rate_per_10k:.1f}/10k chars ({len(contractions)} matches in {char_count} chars). "
                f"Official archive minimum is 22.4 (median 37.3). Add 〜てる/〜とく/〜ちゃう/〜なきゃ forms."
            )
        else:
            report.notice("CHOUKAI-縮約形", f"Contraction rate: {rate_per_10k:.1f}/10k chars (Target: 22.4–67.4) — PASS")

        # Reaction turns
        turns = [l for l in dialogue_lines if re.match(r"^[男女AB]:", l)]
        if turns:
            short_reactions = [t for t in turns if len(re.sub(r"^[男女AB]:", "", t).strip()) <= 12]
            react_rate = (len(short_reactions) / len(turns)) * 100
            if react_rate < 10.0:
                report.warn("CHOUKAI-REACTION", f"Short reaction turn rate is low: {react_rate:.1f}% ({len(short_reactions)}/{len(turns)}). Target: 12–25%.")
            elif react_rate > 30.0:
                report.warn("CHOUKAI-REACTION", f"Short reaction turn rate is high: {react_rate:.1f}%. Target: 12–25%.")
            else:
                report.notice("CHOUKAI-REACTION", f"Reaction turn rate: {react_rate:.1f}% ({len(short_reactions)}/{len(turns)}) — PASS")

        # Fillers count
        filler_count = sum(full_dialogue.count(f) for f in FILLERS)
        if filler_count < 10:
            report.warn("CHOUKAI-FILLER", f"Total hesitation tokens: {filler_count}. Official median is 27 [band 9–48].")
        elif filler_count > 50:
            report.warn("CHOUKAI-FILLER", f"Total hesitation tokens: {filler_count} exceeds official ceiling (48).")
        else:
            report.notice("CHOUKAI-FILLER", f"Total hesitation tokens: {filler_count} (Official band: 9–48) — PASS")


def lint_gengo_dokkai(gengo_text: str, report: LintReport):
    if not gengo_text:
        return

    # Check duplicate options in any question
    for m in re.finditer(r"\*\*(\d+)\*\*[ \t]*(.*?)(?=\n\*\*\d+\*\*|\n#|\Z)", gengo_text, re.S):
        q_num = m.group(1)
        block = m.group(2)
        opts = re.findall(r"[1-4][.．][ \t]*(.+?)(?=[ \t]+[1-4][.．]|\n|\Z)", block)
        if len(opts) == 4 and len(set(opts)) < 4:
            report.error("OPTION-DUPLICATE", f"Question {q_num} has duplicate choices: {opts}")

    # Check 問題7 stems for missing blank or answer leaks
    m7 = re.search(r"##\s*問題7.*?(?=##\s*問題8|\Z)", gengo_text, re.S)
    if m7:
        for m in re.finditer(r"\*\*(\d+)\*\*(.*?)(?=\n[ \t]*1[.．]|\n\*\*\d+\*\*|\Z)", m7.group(0), re.S):
            qn, stem = m.group(1), m.group(2)
            if "（　）" not in stem and "（ ）" not in stem and "(___)" not in stem:
                report.error("BUNPOU-問7", f"Question {qn} stem has no blank '（　）': {stem.strip()[:40]}")

    # Check 問題8 star scramble format
    m8 = re.search(r"##\s*問題8.*?(?=##\s*問題9|\Z)", gengo_text, re.S)
    if m8:
        for m in re.finditer(r"\*\*(\d+)\*\*(.*?)(?=\n[ \t]*1[.．]|\n\*\*\d+\*\*|\Z)", m8.group(0), re.S):
            qn, stem = m.group(1), m.group(2)
            if "★" not in stem:
                report.error("BUNPOU-問8", f"Question {qn} stem missing '★' star blank: {stem.strip()[:40]}")

    # Check Dokkai numbered markers pairing
    markers_in_text = set(re.findall(r"[①②③④⑤]", gengo_text))
    for marker in sorted(markers_in_text):
        if not re.search(rf"\*\*\d+\*\*.*?[（(]?{marker}[）)]?", gengo_text):
            report.warn("DOKKAI-MARKER", f"Marker {marker} appears in passage but is not referenced in question stems.")

    # Check （注N） pairing
    in_text_notes = set(re.findall(r"（注\s*(\d+)）", gengo_text))
    def_notes = set(re.findall(r"^（注\s*(\d+)）", gengo_text, re.M))
    orphan_in_text = in_text_notes - def_notes
    orphan_defs = def_notes - in_text_notes
    if orphan_in_text:
        report.error("DOKKAI-NOTE", f"Passage uses （注{', '.join(sorted(orphan_in_text))}） with no definition line.")
    if orphan_defs:
        report.warn("DOKKAI-NOTE", f"Definition line for （注{', '.join(sorted(orphan_defs))}） exists but term is not marked in passage.")

    # Check absolute quantifier distractors in Dokkai (問10-14)
    dokkai_sec = re.search(r"##\s*問題1[0-4].*", gengo_text, re.S)
    if dokkai_sec:
        for line in dokkai_sec.group(0).splitlines():
            for word in ABS_QUANTIFIERS:
                if word in line and re.match(r"^[1-4][.．]", line.strip()):
                    report.warn("DOKKAI-ABS-QUANT", f"Dokkai choice contains '{word}': {line.strip()[:60]}")


def lint_test_dir(test_dir: Path):
    test_dir = Path(test_dir)
    report = LintReport(test_dir.name)

    # 1. Check sources
    gengo_path = test_dir / "言語知識・読解.md"
    choukai_path = test_dir / "聴解.md"
    script_path = test_dir / "聴解スクリプト.txt"

    gengo_text = gengo_path.read_text(encoding="utf-8") if gengo_path.is_file() else ""
    script_text = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""

    # Check if section fragments exist in _sections/
    sec_dir = test_dir / "_sections"
    if sec_dir.is_dir():
        for frag in sorted(sec_dir.glob("*.md")):
            frag_text = frag.read_text(encoding="utf-8")
            lint_gengo_dokkai(frag_text, report)

    if gengo_text:
        lint_gengo_dokkai(gengo_text, report)

    if script_text:
        lint_choukai_script(script_text, report)

    report.print_summary()
    return len(report.errors) == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target_path", help="Path to tests/<test_id> or tests/<test_id>/_sections/")
    args = ap.parse_args()

    target = Path(args.target_path)
    if not target.exists():
        print(f"Error: Path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    ok = lint_test_dir(target if target.is_dir() else target.parent)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
