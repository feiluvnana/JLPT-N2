#!/usr/bin/env python3
"""
Fast Deterministic Pre-Linter & Zero-Token Auto-Fixer for JLPT N2 Drafts.

Run this BEFORE invoking QA or committing a draft to instantly catch & auto-repair
mechanical flaws that would otherwise trigger costly QA review round-trips:
- Choukai script contraction rate (縮約形), reaction turns, and filler band
- Choukai banned formulas, split turns, and accidental answer reveals
- Dokkai absolute quantifier / categorical denial option markers
- Dokkai numbered marker and （注N） pairing
- Bunpou 問題7 blank presence, 問題8 scramble permutations, 問題9 cloze tagging
- Moji-Goi 4-choice uniqueness, 2x2 Cartesian matrix grid check, and distractor labels
- Ruby/Furigana format and nested accumulation checks

Usage:
    python3 tools/lint_draft.py tests/20260814_1
    python3 tools/lint_draft.py tests/20260814_1 --fix
    make lint-draft 20260814_1
"""

import argparse
import importlib.util
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

# Auto-fix replacement rules for conversational contractions in dialogue.
#
# TWO ladders, because 縮約形 and politeness are independent axes. The first cut
# of this table had one, and it dropped ます from whatever line it touched:
# 「かしこまりました、そちらは当店で承っておきますね」 became 「…承っとくね」 —
# a shop assistant talking down to a customer. That is F4's register drift
# committed by the tool meant to fix register. Official keigo dialogue DOES
# contract (service-role items measure 37.5 縮約形/10k): it just contracts to the
# polite form — 〜てます、〜ときます、〜ちゃいました.
AUTO_CONTRACTION_CASUAL = [
    (r"ています([。、ねよか])", r"てる\1"),
    (r"ていました([。、ねよか])", r"てた\1"),
    (r"ておきます([。、ねよか])", r"とく\1"),
    (r"ておいてください", r"といてください"),
    (r"てしまいました([。、ねよか])", r"ちゃった\1"),
    (r"てしまいます([。、ねよか])", r"ちゃう\1"),
    (r"なければなりません", r"なきゃいけません"),
    (r"なくてはいけません", r"なくちゃいけません"),
]
AUTO_CONTRACTION_POLITE = [
    (r"ています([。、ねよか])", r"てます\1"),
    (r"ていました([。、ねよか])", r"てました\1"),
    (r"ておきます([。、ねよか])", r"ときます\1"),
    (r"ておいてください", r"といてください"),
    (r"てしまいました([。、ねよか])", r"ちゃいました\1"),
    (r"てしまいます([。、ねよか])", r"ちゃいます\1"),
    (r"なければなりません", r"なきゃいけません"),
    (r"なくてはいけません", r"なくちゃいけません"),
]
AUTO_CONTRACTION_REPLACEMENTS = AUTO_CONTRACTION_CASUAL   # back-compat alias

# A turn is on the polite ladder if its speaker holds a service/expert role or
# the line itself carries keigo. Both tests are needed: 客 speaking TO a counter
# uses keigo without holding the role, and a 職員 line can be keigo-free.
KEIGO_ROLE_LABELS = ("店員", "職員", "係員", "担当者", "講師", "専門家", "医者",
                     "先生", "教授", "アナウンス", "アナウンサー", "レポーター",
                     "教室の人", "部長", "店長", "FP")
KEIGO_MARKER_RE = re.compile(r"ございま|いただ|ておりま|申し訳|伺|存じ|いらっしゃ|"
                             r"かしこまり|承り|承っ|くださ|ご[一-鿿]")


def contraction_ladder(label: str, text: str):
    """Which ladder this turn contracts on — politeness is not negotiable."""
    role = label.lstrip("男性女性") if label.startswith(("男性", "女性")) else label
    if role in KEIGO_ROLE_LABELS or KEIGO_MARKER_RE.search(text):
        return AUTO_CONTRACTION_POLITE
    return AUTO_CONTRACTION_CASUAL


class LintReport:
    def __init__(self, target_name: str):
        self.target_name = target_name
        self.errors = []
        self.warnings = []
        self.notices = []
        self.fixes = []

    def error(self, category: str, msg: str):
        self.errors.append((category, msg))

    def warn(self, category: str, msg: str):
        self.warnings.append((category, msg))

    def notice(self, category: str, msg: str):
        self.notices.append((category, msg))

    def fixed(self, category: str, msg: str):
        self.fixes.append((category, msg))

    def print_summary(self):
        print(f"\n=======================================================")
        print(f"  Pre-Lint & Zero-Token Auto-Fix Report: {self.target_name}")
        print(f"=======================================================")

        if self.fixes:
            print(f"\n[AUTO-FIXES APPLIED] ({len(self.fixes)} changes made):")
            for cat, msg in self.fixes:
                print(f"  [FIXED] [{cat}] {msg}")

        if self.errors:
            print(f"\n[FAIL / BLOCKING ERRORS] ({len(self.errors)} item(s) must be fixed before QA):")
            for cat, msg in self.errors:
                print(f"  [ERROR] [{cat}] {msg}")

        if self.warnings:
            print(f"\n[WARNINGS / MANUAL CHECKS] ({len(self.warnings)} item(s) to inspect):")
            for cat, msg in self.warnings:
                print(f"  [WARN]  [{cat}] {msg}")

        if self.notices:
            print(f"\n[STATS / OFFICIAL BENCHMARKS]:")
            for cat, msg in self.notices:
                print(f"  [INFO]  [{cat}] {msg}")

        if not self.errors and not self.warnings:
            print(f"\n✓ ALL CHECKS CLEAN. Draft is ready for QA blind-solve.")
        elif not self.errors:
            print(f"\n✓ No critical blocking errors. Passable to QA.")
        else:
            print(f"\n❌ Blocking errors detected. Fix them to avoid a QA rejection loop.")


def autofix_script(script_text: str, report: LintReport) -> str:
    """Apply zero-token automatic conversational contraction fixes to script."""
    new_lines = []
    fixed_count = 0
    for line in script_text.splitlines():
        # Only modify dialogue turns (starting with 男: or 女:), not announcer lines
        if re.match(r"^[男女AB１２34567890\w]+:", line.strip()) and not re.match(r"^(?:問題|第?\d+番|アナウンス)", line.strip()):
            mod_line = line
            label, _, body = line.strip().partition(":")
            for pattern, repl in contraction_ladder(label, body):
                if re.search(pattern, mod_line):
                    mod_line = re.sub(pattern, repl, mod_line)
                    fixed_count += 1
            new_lines.append(mod_line)
        else:
            new_lines.append(line)

    if fixed_count > 0:
        report.fixed("CHOUKAI-縮約形", f"Auto-applied {fixed_count} conversational contraction(s) to dialogue.")
    return "\n".join(new_lines)


def autofix_split_turns(script_text: str, report: LintReport) -> str:
    """Join two consecutive lines that carry the SAME speaker label.

    Deterministic by construction (REPORT-CHOUKAI.md §5.0.1): one turn is one
    line, so a repeated label is a split turn, and the repair is a join at 。 —
    no wording decision to make. It matters twice over: the split buys a turn
    gap where official has a 0.40 s within-turn pause, and it inflates the
    short-reaction rate without adding a reaction, since only the OTHER
    speaker's turn counts as one (`official_register.md` §7.3).
    """
    label = re.compile(r"^([^:：\s][^:：]{0,7})[:：](.*)$")
    out: list[str] = []
    joined = 0
    for line in script_text.splitlines():
        hit = label.match(line.strip())
        prev = label.match(out[-1].strip()) if out else None
        if hit and prev and hit.group(1) == prev.group(1) and hit.group(2).strip():
            head = out[-1].rstrip()
            if not head.endswith(("。", "、", "？", "！", "?", "!")):
                head += "。"
            out[-1] = head + hit.group(2).strip()
            joined += 1
            continue
        out.append(line)
    if joined:
        report.fixed("CHOUKAI-SPLIT-TURN",
                     f"Joined {joined} split turn(s) — one turn is one line "
                     f"(choukai-audio Part 1 §Block conventions).")
    # Keep the trailing newline: `validate_script()` splits on blank lines, and a
    # file that loses its final "\n" reads as an edit to the last block.
    return "\n".join(out) + ("\n" if script_text.endswith("\n") else "")


# Gendered role pairs from `SPEAKER_MAP` (Phase 4.1). A swap is only ever
# BETWEEN the two spellings of one role, so it can never introduce a label the
# synthesis map lacks — an unmapped label does not error, it silently falls
# through to the narrator voice.
def _synth():
    spec = importlib.util.spec_from_file_location(
        "_synth_map", Path(__file__).resolve().parents[1]
        / ".agents/choukai-audio/scripts/make_choukai_mp3.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_synth_map"] = mod
    spec.loader.exec_module(mod)
    return mod


FEMALE_BASE_F0, MALE_BASE_F0 = 210.0, 120.0
VOICE_MARGIN_ST = 1.9


def _semitones(base: float, p1: float, p2: float) -> float:
    import math
    f1, f2 = base + p1, base + p2
    return abs(12.0 * math.log2(f1 / f2)) if f1 > 0 and f2 > 0 else 0.0


def _min_margin(labels: list[str], smap: dict, female) -> float:
    """Smallest same-gender separation among an item's labels, in semitones."""
    worst = float("inf")
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            ca, cb = smap.get(a), smap.get(b)
            if not ca or not cb or ca["voice"] != cb["voice"]:
                continue
            base = FEMALE_BASE_F0 if ca["voice"] == female else MALE_BASE_F0
            worst = min(worst, _semitones(base,
                                          float(str(ca["pitch"]).replace("Hz", "")),
                                          float(str(cb["pitch"]).replace("Hz", ""))))
    return worst


def autofix_voice_margin(script_text: str, report: LintReport) -> str:
    """Recast ONE label of a too-close pair onto its gendered counterpart.

    Deterministic given Phase 4.1's pairs (§5.0.1), but only because the swap is
    SIMULATED first: the naive version of this fix — "an item with 女 plus a
    female role label gets the male role label" — moved `20260814_1` 問題5-2番
    from a 1.42 st female pair to a **1.12 st male** one, because the item
    already held 男. So every candidate swap is scored by the item's minimum
    same-gender separation and applied only when that minimum actually improves
    and clears the 1.9 st margin.

    Skipped when the narration names the speaker's gender (「〜の女の人」) — the
    one case where the swap would contradict the booklet, and `check_voice_casting`
    FAILs on it rather than warning.
    """
    smap = _synth().SPEAKER_MAP
    female = _synth().FEMALE
    pairs: dict[str, str] = {}
    for label in smap:
        for prefix, other in (("男性", "女性"), ("女性", "男性")):
            if label.startswith(prefix):
                counterpart = other + label[len(prefix):]
                bare = label[len(prefix):]
                if counterpart in smap:
                    pairs[label] = counterpart
                if bare in smap:
                    pairs.setdefault(bare, label if prefix == "男性" else counterpart)

    blocks = re.split(r"(\n\s*\n)", script_text)
    swapped = 0
    for i, block in enumerate(blocks):
        lines = [l for l in block.splitlines() if l.strip()]
        if len(lines) < 2 or not re.match(r"^(例|\d+番)。", lines[0].strip()):
            continue
        labels: list[str] = []
        for l in lines:
            hit = re.match(r"^([^:：\s][^:：]{0,7})[:：]", l.strip())
            if hit and hit.group(1) in smap and hit.group(1) not in labels:
                labels.append(hit.group(1))
        before = _min_margin(labels, smap, female)
        if before >= VOICE_MARGIN_ST:
            continue
        best = None
        for label in labels:
            target = pairs.get(label)
            if not target or target in labels:
                continue
            if re.search(rf"{re.escape(label)}の(男|女)の人|(男|女)の{re.escape(label)}", block):
                continue                      # narration fixes this speaker's gender
            after = _min_margin([target if x == label else x for x in labels], smap, female)
            if after > before and (best is None or after > best[1]):
                best = (label, after, target)
        if not best or best[1] < VOICE_MARGIN_ST:
            continue                          # no swap actually repairs this item
        label, _, target = best
        blocks[i] = re.sub(rf"^{re.escape(label)}([:：])", rf"{target}\1", block, flags=re.M)
        swapped += 1
    if swapped:
        report.fixed("CHOUKAI-VOICE-MARGIN",
                     f"Recast {swapped} item(s) onto a gendered role label so every "
                     f"same-gender pair clears {VOICE_MARGIN_ST} st (choukai-audio "
                     f"Part 2 §D2). Re-read those items' 聴解.md narration and 解説.")
    return "".join(blocks)


def lint_choukai_script(script_text: str, report: LintReport, fix: bool = False) -> str:
    if not script_text:
        return script_text

    # The deterministic subset of the 聴解 repair lanes (REPORT-CHOUKAI.md §5.0.1).
    # Everything else stays `assisted` on purpose: stripping 「〜について」 off a
    # 問題3 option is a writing decision, not a substitution, and a tool that
    # pretended otherwise would ship 20 malformed options and a green gate.
    if fix:
        script_text = autofix_split_turns(script_text, report)
        script_text = autofix_voice_margin(script_text, report)

    # 1. Opening & level check
    if "N2" in script_text:
        report.error("CHOUKAI-TTS", "Script contains 'N2' — TTS spelling must be 'Nに', never 'N2'.")

    # 2. Reveal in scored items
    lines = script_text.splitlines()
    for idx, line in enumerate(lines, 1):
        if "最もよいものは" in line and "例" not in line and "練習" not in line:
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
        if re.match(r"^[男女AB１２34567890\w]+:", line_s):
            dialogue_lines.append(line_s)
        elif is_dialogue:
            dialogue_lines.append(line_s)
        else:
            announcer_lines.append(line_s)

    full_dialogue = "\n".join(dialogue_lines)
    char_count = len(re.sub(r"\s+", "", full_dialogue))

    if char_count > 500:
        contractions = list(CONTRACTION_RE.finditer(full_dialogue))
        rate_per_10k = (len(contractions) / char_count) * 10000

        if rate_per_10k < 22.4:
            if fix:
                script_text = autofix_script(script_text, report)
                # Re-calculate after fix
                lines_fixed = script_text.splitlines()
                d_fixed = [l.strip() for l in lines_fixed if re.match(r"^[男女AB１２34567890\w]+:", l.strip())]
                full_d_fixed = "\n".join(d_fixed)
                c_fixed = len(re.sub(r"\s+", "", full_d_fixed))
                cont_fixed = list(CONTRACTION_RE.finditer(full_d_fixed))
                rate_fixed = (len(cont_fixed) / c_fixed) * 10000 if c_fixed else 0
                report.notice("CHOUKAI-縮約形", f"Contraction rate after auto-fix: {rate_fixed:.1f}/10k chars — PASS")
            else:
                report.error(
                    "CHOUKAI-縮約形",
                    f"Contraction rate is {rate_per_10k:.1f}/10k chars ({len(contractions)} in {char_count} chars). "
                    f"Official archive minimum is 22.4 (median 37.3). Run with --fix or add 〜てる/〜とく/〜ちゃう."
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
        if filler_count < 9:
            report.warn("CHOUKAI-FILLER", f"Total hesitation tokens: {filler_count}. Official median is 27 [band 9–48].")
        elif filler_count > 50:
            report.warn("CHOUKAI-FILLER", f"Total hesitation tokens: {filler_count} exceeds official ceiling (48).")
        else:
            report.notice("CHOUKAI-FILLER", f"Total hesitation tokens: {filler_count} (Official band: 9–48) — PASS")

    return script_text


def autofix_gengo_md(gengo_text: str, report: LintReport) -> str:
    """Auto-fix stem underline markdown formatting and spacing."""
    # Fix okurigana split bolding e.g. **生**じる -> **生じる** or **に生じる** -> に**生じる**
    # 1. Move leading particle outside bold: **に生じる** -> に**生じる**
    #    The tail MUST contain a kanji. Without that guard this rule corrupted an
    #    all-kana marked span: 問題2 prints the target word in kana (the examinee
    #    picks its kanji spelling), so 「重さを一グラム単位で**はかる**」 was rewritten
    #    to 「…では**かる**」, silently re-marking the item onto 「かる」
    #    (20260818_1, 2026-08-19). A kana-only span is never a particle + word.
    orig = gengo_text
    fixed_text = re.sub(
        r"\*\*([にへとでからよりがをもは])([ぁ-ゖ]*[一-鿿][一-鿿ぁ-ゖ]*)\*\*",
        r"\1**\2**",
        gengo_text,
    )
    if fixed_text != orig:
        report.fixed("GENGO-FORMAT", "Fixed leading particle inside bold underline span.")
    return fixed_text


def lint_gengo_dokkai(gengo_text: str, report: LintReport, fix: bool = False) -> str:
    if not gengo_text:
        return gengo_text

    if fix:
        gengo_text = autofix_gengo_md(gengo_text, report)

    # Check for forbidden <ruby> in gengo text
    if "<ruby>" in gengo_text or "<rt>" in gengo_text:
        report.error("GENGO-RUBY", "言語知識・読解.md contains '<ruby>' tags — examinees read raw kanji; use （注N） only.")

    # Check duplicate options in any question
    for m in re.finditer(r"\*\*(\d+)\*\*[ \t]*(.*?)(?=\n\*\*\d+\*\*|\n#|\Z)", gengo_text, re.S):
        q_num = m.group(1)
        block = m.group(2)
        opts = re.findall(r"[1-4][.．][ \t]*(.+?)(?=[ \t]+[1-4][.．]|\n|\Z)", block)
        if len(opts) == 4 and len(set(opts)) < 4:
            report.error("OPTION-DUPLICATE", f"Question {q_num} has duplicate choices: {opts}")

    # Check 問題7 stems for missing blank
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

    # Check Dokkai option length balance (max/min <= 1.30)
    for m in re.finditer(r"\*\*(\d+)\*\*[ \t]*(.*?)(?=\n\*\*\d+\*\*|\n#|\Z)", gengo_text, re.S):
        q_num = int(m.group(1))
        if 52 <= q_num <= 71:
            block = m.group(2)
            opts = re.findall(r"[1-4][.．][ \t]*(.+?)(?=[ \t]+[1-4][.．]|\n|\Z)", block)
            if len(opts) == 4:
                lens = [len(re.sub(r"[\s\d\.\(\)（）「」『』【】、。・/]", "", o)) for o in opts]
                mx, mn = max(lens), min(lens)
                if mn > 0 and mx / mn > 1.30:
                    report.error("DOKKAI-OPTION-RATIO",
                                 f"Question {q_num} option length ratio {mx/mn:.2f}x ({lens}) exceeds 1.30 cap.")

    return gengo_text


def lint_test_dir(test_dir: Path, fix: bool = False):
    test_dir = Path(test_dir)
    report = LintReport(test_dir.name)

    gengo_path = test_dir / "言語知識・読解.md"
    choukai_path = test_dir / "聴解.md"
    script_path = test_dir / "聴解スクリプト.txt"

    gengo_text = gengo_path.read_text(encoding="utf-8") if gengo_path.is_file() else ""
    script_text = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""

    if gengo_text:
        new_gengo = lint_gengo_dokkai(gengo_text, report, fix=fix)
        if fix and new_gengo != gengo_text and gengo_path.is_file():
            gengo_path.write_text(new_gengo, encoding="utf-8")

    if script_text:
        new_script = lint_choukai_script(script_text, report, fix=fix)
        if fix and new_script != script_text and script_path.is_file():
            script_path.write_text(new_script, encoding="utf-8")

    report.print_summary()
    return len(report.errors) == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target_path", help="Path to tests/<test_id>")
    ap.add_argument("--fix", action="store_true", help="Auto-apply zero-token conversational contractions and formatting fixes")
    args = ap.parse_args()

    target = Path(args.target_path)
    if not target.exists():
        print(f"Error: Path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    ok = lint_test_dir(target if target.is_dir() else target.parent, fix=args.fix)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
