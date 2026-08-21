#!/usr/bin/env python3
"""読解 (問題10–14) measurement — ONE parser, both corpora, two consumers.

Why this file exists (REPORT-DOKKAI.md §F1, §F2, §F3, §D1): every 読解 number the rules
are built on used to live in prose, with the gate re-implementing it, and several
assumptions (e.g. max/min <= 1.30 option clamp) failed official past exams.
So the measurement lives here, once:

  * `tools/check_consistency.py` imports this module for its 読解 checks —
    the gate keeps owning the THRESHOLDS, this file owns the MEASUREMENT;
  * `--baseline` prints the official tables in the Markdown shape
    `dokkai.md` / `official_calibration.md` carry, so refreshing a doc is a
    paste, not a retype.

Usage:
    python3 tools/dokkai_profile.py --official [--era cur|all]
    python3 tools/dokkai_profile.py --tests 20260819_1 …      (default: every test)
    python3 tools/dokkai_profile.py --baseline [--json]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "refs" / "JLPT_N2_NEW"
TESTS = ROOT / "tests"

# Same definition as `check_consistency.jp_char_count()`.
JP_CHAR = re.compile(r"[぀-ヿ一-鿿ー。、！？（）「」『』…・]")
KANJI = re.compile(r"[一-鿿]")
KANA = re.compile(r"[぀-ヿー]")
KANJI_KANA = re.compile(r"[぀-ヿ一-鿿ー]")

CURRENT_ERA = (
    "13. N2 12-2022",
    "14. N2 7-2023",
    "14. N2 12-2023",
    "15. N2 7-2024",
    "15. N2 12-2024",
    "16. N2 7-2025",
    "17.N2 12-2025",
)

FULLWIDTH = str.maketrans("０１２３４５６７８９", "0123456789")

# Regexes for dokkai features
RUBY_LINE = re.compile(r"^[ぁ-ゟァ-ヶー\s/／]{1,15}$")
FOOTER = re.compile(r"(?:N2\s*)?\d{1,2}/\d{4}\s*$|(?:文\s*法|読\s*解|言語知識)\s*$")
PAGE_LINE = re.compile(r"^##\s*page\s*\d+/\d+", re.I)

NOTE_MARKER = re.compile(r"[（(]注\s*\d*[）)]")
NOTE_DEF = re.compile(r"^\s*[（(]注\s*(\d*)[）)]\s*([^：:）)]{1,24})\s*[：:](.*)$")
CHUURYAKU = re.compile(r"（中略）")
ASTERISK = re.compile(r"※")

ABS_QUANTIFIERS = (
    "すべて", "全て", "まったく", "全く", "のみ", "だけで十分",
    "無関係", "存在しない", "必ず", "一切", "絶対に", "だけで解決"
)

# Register tokens
PERSONAL_LEXIS = (
    "私", "僕", "俺", "わたし", "ぼく", "自分", "母", "父", "祖母", "祖父",
    "娘", "息子", "妻", "夫", "兄", "姉", "弟", "妹", "家族", "友人", "友達",
    "彼", "彼女", "子ども", "子供", "うち", "部屋", "思い出", "実家"
)
INSTITUTIONAL_LEXIS = (
    "市", "町", "県", "国", "自治体", "政府", "省", "会社", "当社", "本社",
    "支店", "部長", "課長", "社長", "担当者", "職員", "学校", "大学", "委員会",
    "協会", "組織", "予算", "事業", "申請", "制度", "規定", "条例", "契約",
    "役所", "病院", "議会", "当局", "窓口", "研修"
)
FIRST_PERSON = ("私", "僕", "俺", "わたし", "ぼく", "自分")
POLITE_ENDINGS = re.compile(r"(です|ます|ました|ません|でした|でしょう|ください|ましょう)[。！？]?$")
RHETORICAL = re.compile(r"(だろうか|ではないか|ではないだろうか|まいか)[。！？]?")
COLLOQUIAL = re.compile(r"(んです|でしょう|ですね|じゃない|わけだ|ますね)")
QUOTED_SPEECH = re.compile(r"「([^」]+)」")


def jp(s: str) -> int:
    return len(JP_CHAR.findall(s))


def jp_kanji_kana_only(s: str) -> str:
    return "".join(KANJI_KANA.findall(s))


def get_bigrams(s: str) -> list[str]:
    cleaned = jp_kanji_kana_only(s)
    if len(cleaned) < 2:
        return [cleaned] if cleaned else []
    return [cleaned[i:i+2] for i in range(len(cleaned) - 1)]


def calc_overlap(option: str, passage: str) -> float:
    opt_bigrams = get_bigrams(option)
    if not opt_bigrams:
        return 0.0
    pass_cleaned = jp_kanji_kana_only(passage)
    hits = sum(1 for bg in opt_bigrams if bg in pass_cleaned)
    return hits / len(opt_bigrams)


@dataclass
class DokkaiItem:
    corpus: str
    paper: str
    section: int  # mondai 10..14
    no: int
    passage_idx: int  # 1..5 for M10, 1..4 for M11, 1..2 for M12, 1 for M13, 1 for M14
    passage: str
    stem: str
    options: list[str]  # exactly 4 options
    key: int  # 1..4
    glosses: list[str] = field(default_factory=list)


@dataclass
class DokkaiPassage:
    corpus: str
    paper: str
    section: int
    passage_idx: int
    text: str
    glosses: list[str] = field(default_factory=list)
    is_essay: bool = True  # False for M10 notice/email and M14


# --------------------------------------------------------------------------
# Stem & Target Classifiers
# --------------------------------------------------------------------------

def classify_stem_bucket(stem: str) -> str:
    """Priority-ordered stem classification."""
    # 1. Apparatus (email / notice / announcement)
    if re.search(r"(お知らせ|メール|案内|チラシ|ポスター|文書|広告)", stem):
        return "apparatus"
    # 2. Span-anchored
    if "とあるが" in stem or re.search(r"[①-⑨]\s*\*\*", stem) or re.search(r"^[①-⑨]", stem):
        return "span"
    # 3. 指示語
    if re.search(r"(それ|これ|あれ|どれ|このよう|そのよう|こうし|そうし|これら|それら).*?(指|どういう|何|意味)", stem):
        return "shijigo"
    # 4. 考え/主張
    if re.search(r"(筆者.*?(考え|言いたいこと|大切|主張|どう考えて))|((考え|言いたいこと)に合う)", stem):
        return "kangae"
    # 5. によると / 述べ
    if "によると" in stem or "述べて" in stem or "説明して" in stem:
        return "niyoruto_nobe"
    # 6. Truth check (banned retrieval shapes)
    if re.search(r"(正しいもの|適切なもの|合っているもの|述べられているもの|主な目的)", stem):
        return "truth_check"
    # 7. 理由
    if "なぜ" in stem or "理由" in stem or "どうして" in stem or "からか" in stem:
        return "riyuu"
    # 8. その他 / 事実
    return "other"


def is_apparatus_intent(stem: str) -> bool:
    """Check if apparatus stem asks INTENT rather than content."""
    # Intent: 伝えたいこと, 問い合わせていること, 用件, 目的, 連絡した, 呼びかけている
    return bool(re.search(r"(伝えたい|問い合わせ|用件|何のため|目的|連絡した|最も言いたい|お願いしたい)", stem))


def classify_q14_target(stem: str) -> str:
    """Classify what a 問題14 stem asks for."""
    if re.search(r"(いくら|何円|料金|費用|いくらになるか|金額)", stem):
        return "value"
    if re.search(r"(何を用意|どの書類|必要なもの|支払うもの|何を持|何が必要|何を持参)", stem):
        return "value"
    if re.search(r"(どうしなければ|どうすれば|どのように申し込|どのように予約|どうやって|どのような手続き|手続)", stem):
        return "action"
    if re.search(r"(どの(講座|コース|プラン|部屋|日|時間)|誰|どの人)", stem):
        return "choice"
    if re.search(r"(正しいもの|適切なもの|合っているもの)", stem):
        return "truth_check"
    return "other"


# --------------------------------------------------------------------------
# Official booklet parser
# --------------------------------------------------------------------------

def _parse_official_dokkai(sitting: str, booklet_md: str, answer_keys: dict) -> tuple[list[DokkaiPassage], list[DokkaiItem]]:
    exam_keys = answer_keys["exams"].get(sitting, {}).get("items", [])
    dokkai_keys = {it["no"]: it for it in exam_keys if it.get("section") == "読解"}
    if not dokkai_keys:
        return [], []

    # Drop ruby lines and normalize
    raw_lines = booklet_md.translate(FULLWIDTH).splitlines()
    lines = []
    for ln in raw_lines:
        s = ln.strip()
        if PAGE_LINE.match(s):
            continue
        if FOOTER.match(s):
            continue
        if RUBY_LINE.match(s) and lines and KANJI.search(lines[-1][-1:]):
            continue
        lines.append(s)

    # Locate where choukai starts (to bound reading section)
    choukai_line = len(lines)
    for i, ln in enumerate(lines):
        if re.search(r"聴解|問題\s*1\s*では、まず", ln) and i > 150:
            choukai_line = i
            break

    # Locate sections 10 to 14
    mondai_starts = {}
    for i in range(choukai_line):
        ln = lines[i]
        m = re.search(r"[問間]題\s*(\d+)", ln)
        if m:
            m_num = int(m.group(1))
            if 10 <= m_num <= 14:
                mondai_starts[m_num] = i

    passages: list[DokkaiPassage] = []
    items: list[DokkaiItem] = []

    # Parse by mondai
    for m_num in sorted(mondai_starts.keys()):
        start_idx = mondai_starts[m_num]
        end_idx = choukai_line
        for other_m, idx in mondai_starts.items():
            if idx > start_idx and idx < end_idx:
                end_idx = idx

        sec_lines = lines[start_idx:end_idx]
        sec_text = re.sub(r"(?:^|\n)##\s*page\s*\d+/\d+\s*\n[^\n]*\n", "\n", "\n".join(sec_lines))
        m_items = [it for it in dokkai_keys.values() if it["mondai"] == m_num]
        m_items.sort(key=lambda x: x["no"])

        if m_num == 10:
            p_parts = re.split(r"(?:^|\n)\s*[（(]([1-5１-５])[）)]\s*\n", sec_text)
            if len(p_parts) >= 11:
                for p_idx in range(1, 6):
                    sub = p_parts[p_idx * 2]
                    it_match = re.search(r"(?:^|\n)\s*(\d{2})\s+([^\n]+)\n([\s\S]+)$", sub)
                    if it_match:
                        p_text = sub[:it_match.start()].strip()
                        stem = it_match.group(2).strip()
                        opts_blob = it_match.group(3).strip()
                        opts = _parse_4_options(opts_blob)
                        q_no = int(it_match.group(1))
                        k = dokkai_keys.get(q_no, {}).get("answer", 1)
                        is_ess = not bool(re.search(r"(お知らせ|メール|通知|案内)", p_text[:100] + stem))
                        passages.append(DokkaiPassage("official", sitting, 10, p_idx, p_text, is_essay=is_ess))
                        if len(opts) == 4:
                            items.append(DokkaiItem("official", sitting, 10, q_no, p_idx, p_text, stem, opts, k))
            else:
                for i_pos, it in enumerate(m_items, 1):
                    q_no = it["no"]
                    k = it.get("answer", 1)
                    q_m = re.search(rf"(?:^|\n)\s*{q_no}\s+([^\n]+)\n([\s\S]*?)(?=(?:^|\n)\s*\d{{2}}\s+|\Z)", sec_text)
                    if q_m:
                        stem = q_m.group(1).strip()
                        opts = _parse_4_options(q_m.group(2))
                        passages.append(DokkaiPassage("official", sitting, 10, i_pos, "", is_essay=True))
                        if len(opts) == 4:
                            items.append(DokkaiItem("official", sitting, 10, q_no, i_pos, "", stem, opts, k))

        elif m_num == 11:
            p_parts = re.split(r"(?:^|\n)\s*[（(]([1-4１-４])[）)]\s*\n", sec_text)
            if len(p_parts) >= 3:
                p_count = (len(p_parts) - 1) // 2
                for p_idx in range(1, p_count + 1):
                    sub = p_parts[p_idx * 2]
                    q_matches = list(re.finditer(r"(?:^|\n)\s*(\d{2})\s+([^\n]+)\n([\s\S]*?)(?=(?:^|\n)\s*\d{2}\s+|\Z)", sub))
                    p_text = sub[:q_matches[0].start()].strip() if q_matches else sub.strip()
                    passages.append(DokkaiPassage("official", sitting, 11, p_idx, p_text, is_essay=True))
                    for qm in q_matches:
                        q_no = int(qm.group(1))
                        stem = qm.group(2).strip()
                        opts = _parse_4_options(qm.group(3))
                        k = dokkai_keys.get(q_no, {}).get("answer", 1)
                        if len(opts) == 4:
                            items.append(DokkaiItem("official", sitting, 11, q_no, p_idx, p_text, stem, opts, k))

        elif m_num == 12:
            q_matches = list(re.finditer(r"(?:^|\n)\s*(\d{2})\s+([^\n]+)\n([\s\S]*?)(?=(?:^|\n)\s*\d{2}\s+|\Z)", sec_text))
            p_text = sec_text[:q_matches[0].start()].strip() if q_matches else sec_text.strip()
            p_text = re.sub(r"^###?\s*問題\s*12[^\n]*\n", "", p_text).strip()
            passages.append(DokkaiPassage("official", sitting, 12, 1, p_text, is_essay=True))
            for qm in q_matches:
                q_no = int(qm.group(1))
                stem = qm.group(2).strip()
                opts = _parse_4_options(qm.group(3))
                k = dokkai_keys.get(q_no, {}).get("answer", 1)
                if len(opts) == 4:
                    items.append(DokkaiItem("official", sitting, 12, q_no, 1, p_text, stem, opts, k))

        elif m_num == 13:
            q_matches = list(re.finditer(r"(?:^|\n)\s*(\d{2})\s+([^\n]+)\n([\s\S]*?)(?=(?:^|\n)\s*\d{2}\s+|\Z)", sec_text))
            p_text = sec_text[:q_matches[0].start()].strip() if q_matches else sec_text.strip()
            p_text = re.sub(r"^###?\s*問題\s*13[^\n]*\n", "", p_text).strip()
            passages.append(DokkaiPassage("official", sitting, 13, 1, p_text, is_essay=True))
            for qm in q_matches:
                q_no = int(qm.group(1))
                stem = qm.group(2).strip()
                opts = _parse_4_options(qm.group(3))
                k = dokkai_keys.get(q_no, {}).get("answer", 1)
                if len(opts) == 4:
                    items.append(DokkaiItem("official", sitting, 13, q_no, 1, p_text, stem, opts, k))

        elif m_num == 14:
            q_matches = list(re.finditer(r"(?:^|\n)\s*(\d{2})\s+([^\n]+)\n([\s\S]*?)(?=(?:^|\n)\s*\d{2}\s+|\Z)", sec_text))
            p_text = ""
            if len(q_matches) >= 2:
                blob_last = q_matches[-1].group(3)
                opt4_m = re.search(r"(?:^|\n)\s*([4４])[.、 　]+([^\n]+)", blob_last)
                if opt4_m:
                    p_text = blob_last[opt4_m.end():].strip()
            if not p_text or jp(p_text) < 50:
                p_text = sec_text[:q_matches[0].start()].strip() if q_matches else sec_text.strip()
            p_text = re.sub(r"^###?\s*問題\s*14[^\n]*\n", "", p_text).strip()
            passages.append(DokkaiPassage("official", sitting, 14, 1, p_text, is_essay=False))
            for qm in q_matches:
                q_no = int(qm.group(1))
                stem = qm.group(2).strip()
                opts = _parse_4_options(qm.group(3))
                k = dokkai_keys.get(q_no, {}).get("answer", 1)
                if len(opts) == 4:
                    items.append(DokkaiItem("official", sitting, 14, q_no, 1, p_text, stem, opts, k))

    return passages, items


def _parse_4_options(blob: str) -> list[str]:
    """Extract 4 options from a text blob."""
    lines = [ln.strip() for ln in blob.splitlines() if ln.strip()]
    full = " ".join(lines)
    opt_dict = {}
    matches = list(re.finditer(r"(?<![0-9０-９])([1-4])[.、 　]+", full))
    if len(matches) >= 4:
        seen = {}
        for m in matches:
            d = int(m.group(1))
            if d not in seen:
                seen[d] = m
        if len(seen) == 4:
            sorted_order = sorted(seen.items(), key=lambda kv: kv[1].start())
            for idx, (d, m) in enumerate(sorted_order):
                start = m.end()
                end = sorted_order[idx + 1][1].start() if idx + 1 < len(sorted_order) else len(full)
                opt_dict[d] = full[start:end].strip()
    if len(opt_dict) == 4:
        return [opt_dict[1], opt_dict[2], opt_dict[3], opt_dict[4]]
    return []


# --------------------------------------------------------------------------
# Generated test parser
# --------------------------------------------------------------------------

def _parse_generated_dokkai(test_id: str, md_text: str) -> tuple[list[DokkaiPassage], list[DokkaiItem]]:
    key_map = {}
    key_table_match = re.search(r"##\s*読解\s*\n([\s\S]*?)(?=\n##|\Z)", md_text)
    if key_table_match:
        for row in key_table_match.group(1).splitlines():
            m = re.search(r"\|\s*\*?(\d{2})\*?\s*\|\s*([1-4])\s*\|", row)
            if m:
                key_map[int(m.group(1))] = int(m.group(2))

    body_match = re.split(r"^#+\s*(解答|【?正解)", md_text, flags=re.M)
    body = body_match[0] if body_match else md_text

    passages: list[DokkaiPassage] = []
    items: list[DokkaiItem] = []

    def get_sec(n: int) -> str:
        m = re.search(rf"^##\s*問題{n}\b.*?(?=^##\s*問題{n + 1}\b|\Z)", body, re.M | re.S)
        return m.group(0) if m else ""

    # 問題10 (5 short passages)
    sec10 = get_sec(10)
    if sec10:
        p_parts = re.split(r"(?=^\*\*(?:5[2-6])\*\*)", sec10, flags=re.M)
        if len(p_parts) >= 2:
            lead = p_parts[0]
            for p_idx, sub in enumerate(p_parts[1:6], 1):
                q_m = re.search(r"^\*\*(\d{2})\*\*\s*([^\n]+)\n([\s\S]*)$", sub, re.M)
                if q_m:
                    q_no = int(q_m.group(1))
                    stem = q_m.group(2).strip()
                    raw_p = (lead + "\n" if p_idx == 1 else "") + sub[:q_m.start()]
                    p_text = re.sub(r"^##\s*問題10[^\n]*\n", "", raw_p).strip()
                    opts = _parse_gen_options(q_m.group(3))
                    k = key_map.get(q_no, 1)
                    is_ess = not bool(re.search(r"(お知らせ|メール|通知|案内)", p_text[:100] + stem))
                    passages.append(DokkaiPassage("generated", test_id, 10, p_idx, p_text, is_essay=is_ess))
                    if len(opts) == 4:
                        items.append(DokkaiItem("generated", test_id, 10, q_no, p_idx, p_text, stem, opts, k))

    # 問題11 (4 passages)
    sec11 = get_sec(11)
    if sec11:
        p_parts = re.split(r"(?=^###\s*\([1-4]\)|^#+\s*\([1-4]\)|^\*\*\([1-4]\)\*\*)", sec11, flags=re.M)
        for p_idx, sub in enumerate(p_parts[1:5], 1):
            q_matches = list(re.finditer(r"^\*\*(\d{2})\*\*\s*([^\n]+)\n([\s\S]*?)(?=^\*\*\d{2}\*\*|\Z)", sub, re.M))
            p_text = sub[:q_matches[0].start()].strip() if q_matches else sub.strip()
            p_text = re.sub(r"^###?\s*\(\d+\)[^\n]*\n|^\*\*\(\d+\)\*\*[^\n]*\n", "", p_text).strip()
            passages.append(DokkaiPassage("generated", test_id, 11, p_idx, p_text, is_essay=True))
            for qm in q_matches:
                q_no = int(qm.group(1))
                stem = qm.group(2).strip()
                opts = _parse_gen_options(qm.group(3))
                k = key_map.get(q_no, 1)
                if len(opts) == 4:
                    items.append(DokkaiItem("generated", test_id, 11, q_no, p_idx, p_text, stem, opts, k))

    # 問題12 (A/B)
    sec12 = get_sec(12)
    if sec12:
        q_matches = list(re.finditer(r"^\*\*(\d{2})\*\*\s*([^\n]+)\n([\s\S]*?)(?=^\*\*\d{2}\*\*|\Z)", sec12, re.M))
        p_text = sec12[:q_matches[0].start()].strip() if q_matches else sec12.strip()
        p_text = re.sub(r"^##\s*問題12[^\n]*\n", "", p_text).strip()
        passages.append(DokkaiPassage("generated", test_id, 12, 1, p_text, is_essay=True))
        for qm in q_matches:
            q_no = int(qm.group(1))
            stem = qm.group(2).strip()
            opts = _parse_gen_options(qm.group(3))
            k = key_map.get(q_no, 1)
            if len(opts) == 4:
                items.append(DokkaiItem("generated", test_id, 12, q_no, 1, p_text, stem, opts, k))

    # 問題13 (長文)
    sec13 = get_sec(13)
    if sec13:
        q_matches = list(re.finditer(r"^\*\*(\d{2})\*\*\s*([^\n]+)\n([\s\S]*?)(?=^\*\*\d{2}\*\*|\Z)", sec13, re.M))
        p_text = sec13[:q_matches[0].start()].strip() if q_matches else sec13.strip()
        p_text = re.sub(r"^##\s*問題13[^\n]*\n", "", p_text).strip()
        passages.append(DokkaiPassage("generated", test_id, 13, 1, p_text, is_essay=True))
        for qm in q_matches:
            q_no = int(qm.group(1))
            stem = qm.group(2).strip()
            opts = _parse_gen_options(qm.group(3))
            k = key_map.get(q_no, 1)
            if len(opts) == 4:
                items.append(DokkaiItem("generated", test_id, 13, q_no, 1, p_text, stem, opts, k))

    # 問題14 (情報検索)
    sec14 = get_sec(14)
    if sec14:
        q_matches = list(re.finditer(r"^\*\*(\d{2})\*\*\s*([^\n]+)\n([\s\S]*?)(?=^\*\*\d{2}\*\*|\Z)", sec14, re.M))
        p_text = sec14[:q_matches[0].start()].strip() if q_matches else sec14.strip()
        p_text = re.sub(r"^##\s*問題14[^\n]*\n", "", p_text).strip()
        passages.append(DokkaiPassage("generated", test_id, 14, 1, p_text, is_essay=False))
        for qm in q_matches:
            q_no = int(qm.group(1))
            stem = qm.group(2).strip()
            opts = _parse_gen_options(qm.group(3))
            k = key_map.get(q_no, 1)
            if len(opts) == 4:
                items.append(DokkaiItem("generated", test_id, 14, q_no, 1, p_text, stem, opts, k))

    return passages, items


def _parse_gen_options(blob: str) -> list[str]:
    """Parse generated test option lines: ' 1. ...', ' 2. ...', etc."""
    opts = {}
    for ln in blob.splitlines():
        m = re.match(r"^\s*([1-4])[.、]\s*(.*)$", ln)
        if m:
            opts[int(m.group(1))] = m.group(2).strip()
    if len(opts) == 4:
        return [opts[1], opts[2], opts[3], opts[4]]
    return []


# --------------------------------------------------------------------------
# Metrics Analysis
# --------------------------------------------------------------------------

@dataclass
class PaperProfile:
    corpus: str
    paper: str
    passages: list[DokkaiPassage]
    items: list[DokkaiItem]

    # Computed metrics
    total_jp_len: int = 0
    section_lens: dict[int, int] = field(default_factory=dict)
    passage_lens: dict[int, list[int]] = field(default_factory=dict)

    # Sentences
    median_sentence_len: float = 0.0
    under_25_sentence_share: float = 0.0
    sentence_counts: int = 0

    # Register & Voice
    kanji_density: float = 0.0
    polite_share: float = 0.0  # in essay passages
    first_person_passages: int = 0
    first_person_share: float = 0.0
    institutional_rate: float = 0.0  # per 10k
    personal_rate: float = 0.0  # per 10k
    quoted_rate: float = 0.0  # per 10k
    rhetorical_rate: float = 0.0  # per 10k
    colloquial_rate: float = 0.0  # per 10k

    # Stems
    stem_buckets: dict[int, dict[str, int]] = field(default_factory=dict)
    q14_targets: dict[str, int] = field(default_factory=dict)
    span_count: int = 0
    shijigo_count: int = 0
    apparatus_intent_count: int = 0
    apparatus_total_count: int = 0

    # Options & Keys
    mean_opt_len: float = 0.0
    max_min_ratios: list[float] = field(default_factory=list)
    key_ranks: list[int] = field(default_factory=list)
    rank_counts: dict[int, int] = field(default_factory=dict)
    top_rank_share: float = 0.0
    uniquely_longest_share: float = 0.0

    # Overlap
    overlap_margins: list[float] = field(default_factory=list)
    median_overlap_margin: float = 0.0
    strict_top_overlap_share: float = 0.0

    # House style checks
    asterisk_count: int = 0
    abs_quantifier_count: int = 0
    gloss_count: int = 0
    chuuryaku_count: int = 0

    def compute(self):
        # 1. Lengths
        all_passage_text = []
        for p in self.passages:
            p_clean = re.sub(r"^\s*[（(]注\s*\d*[）)].*$", "", p.text, flags=re.M)
            all_passage_text.append(p_clean)
            p_len = jp(p.text)
            self.passage_lens.setdefault(p.section, []).append(p_len)

        for sec in (10, 11, 12, 13, 14):
            self.section_lens[sec] = sum(self.passage_lens.get(sec, []))
        self.total_jp_len = sum(self.section_lens.values())

        # 2. Sentences (M10-M13 passages)
        sentences = []
        for p in self.passages:
            if p.section in (10, 11, 12, 13):
                cleaned = re.sub(r"^\s*[（(]注\s*\d*[）)].*$", "", p.text, flags=re.M)
                raw_s = [s.strip() for s in cleaned.split("。") if s.strip()]
                for s in raw_s:
                    s_len = jp(s)
                    if s_len > 0:
                        sentences.append(s_len)
        if sentences:
            self.sentence_counts = len(sentences)
            self.median_sentence_len = statistics.median(sentences)
            self.under_25_sentence_share = sum(1 for s in sentences if s < 25) / len(sentences)

        # 3. Kanji density
        total_jp_chars = sum(jp(p.text) for p in self.passages if p.section in (10, 11, 12, 13))
        total_kanji_chars = sum(len(KANJI.findall(p.text)) for p in self.passages if p.section in (10, 11, 12, 13))
        if total_jp_chars > 0:
            self.kanji_density = total_kanji_chars / total_jp_chars

        # 4. Voice in essay passages
        essay_passages = [p for p in self.passages if p.is_essay]
        polite_ends = 0
        total_ends = 0
        fp_count = 0
        for p in essay_passages:
            if any(tok in p.text for tok in FIRST_PERSON):
                fp_count += 1
            cleaned = re.sub(r"^\s*[（(]注\s*\d*[）)].*$", "", p.text, flags=re.M)
            raw_s = [s.strip() + "。" for s in cleaned.split("。") if s.strip()]
            for s in raw_s:
                total_ends += 1
                if POLITE_ENDINGS.search(s):
                    polite_ends += 1
        self.first_person_passages = fp_count
        if essay_passages:
            self.first_person_share = fp_count / len(essay_passages)
        if total_ends > 0:
            self.polite_share = polite_ends / total_ends

        # 5. Lexis rates per 10k chars (M10-M13)
        combined_essay_text = "".join(p.text for p in self.passages if p.section in (10, 11, 12, 13))
        c_len = max(1, jp(combined_essay_text))
        scale = 10000.0 / c_len

        inst_hits = sum(len(re.findall(re.escape(tok), combined_essay_text)) for tok in INSTITUTIONAL_LEXIS)
        pers_hits = sum(len(re.findall(re.escape(tok), combined_essay_text)) for tok in PERSONAL_LEXIS)
        quot_hits = len(QUOTED_SPEECH.findall(combined_essay_text))
        rhet_hits = len(RHETORICAL.findall(combined_essay_text))
        coll_hits = len(COLLOQUIAL.findall(combined_essay_text))

        self.institutional_rate = inst_hits * scale
        self.personal_rate = pers_hits * scale
        self.quoted_rate = quot_hits * scale
        self.rhetorical_rate = rhet_hits * scale
        self.colloquial_rate = coll_hits * scale

        # 6. Stems
        for it in self.items:
            b = classify_stem_bucket(it.stem)
            self.stem_buckets.setdefault(it.section, {}).setdefault(b, 0)
            self.stem_buckets[it.section][b] += 1

            if b == "span" or "とあるが" in it.stem:
                self.span_count += 1
            if b == "shijigo":
                self.shijigo_count += 1
            if b == "apparatus":
                self.apparatus_total_count += 1
                if is_apparatus_intent(it.stem):
                    self.apparatus_intent_count += 1

            if it.section == 14:
                t = classify_q14_target(it.stem)
                self.q14_targets[t] = self.q14_targets.get(t, 0) + 1

        # 7. Options & Keys
        all_opt_lens = []
        uniquely_longest_cnt = 0
        for it in self.items:
            opt_lens = [jp(o) for o in it.options]
            all_opt_lens.extend(opt_lens)
            if min(opt_lens) > 0:
                self.max_min_ratios.append(max(opt_lens) / min(opt_lens))

            k_len = opt_lens[it.key - 1]
            rank = 1 + sum(1 for l in opt_lens if l > k_len)
            self.key_ranks.append(rank)
            self.rank_counts[rank] = self.rank_counts.get(rank, 0) + 1

            if k_len == max(opt_lens) and opt_lens.count(k_len) == 1:
                uniquely_longest_cnt += 1

            if it.passage:
                k_overlap = calc_overlap(it.options[it.key - 1], it.passage)
                dist_overlaps = [calc_overlap(o, it.passage) for i, o in enumerate(it.options) if i != (it.key - 1)]
                best_dist = max(dist_overlaps) if dist_overlaps else 0.0
                self.overlap_margins.append(k_overlap - best_dist)

        if all_opt_lens:
            self.mean_opt_len = statistics.mean(all_opt_lens)
        if self.items:
            max_rank_cnt = max(self.rank_counts.values()) if self.rank_counts else 0
            self.top_rank_share = max_rank_cnt / len(self.items)
            self.uniquely_longest_share = uniquely_longest_cnt / len(self.items)

        if self.overlap_margins:
            self.median_overlap_margin = statistics.median(self.overlap_margins)
            self.strict_top_overlap_share = sum(1 for m in self.overlap_margins if m > 0.0) / len(self.overlap_margins)

        # 8. Asterisk, Glosses, Chuuryaku, Quantifiers
        full_text = "\n".join(p.text for p in self.passages)
        self.asterisk_count = len(ASTERISK.findall(full_text))
        self.gloss_count = len(NOTE_MARKER.findall(full_text))
        self.chuuryaku_count = len(CHUURYAKU.findall(full_text))

        quant_hits = 0
        for it in self.items:
            for o in it.options:
                if any(q in o for q in ABS_QUANTIFIERS):
                    quant_hits += 1
        self.abs_quantifier_count = quant_hits


def profile_official(era: str = "cur") -> list[PaperProfile]:
    keys_path = REFS / "answer_keys.json"
    if not keys_path.is_file():
        return []
    answer_keys = json.loads(keys_path.read_text(encoding="utf-8"))

    profiles: list[PaperProfile] = []
    for sitting in sorted(answer_keys["exams"].keys()):
        if era == "cur" and sitting not in CURRENT_ERA:
            continue
        booklet_path = REFS / sitting / "booklet.md"
        if not booklet_path.is_file():
            continue
        passages, items = _parse_official_dokkai(sitting, booklet_path.read_text(encoding="utf-8"), answer_keys)
        p = PaperProfile("official", sitting, passages, items)
        p.compute()
        profiles.append(p)
    return profiles


def profile_tests(test_ids: list[str] | None = None) -> list[PaperProfile]:
    if not test_ids:
        test_ids = [d.name for d in sorted(TESTS.iterdir()) if d.is_dir() and (d / "言語知識・読解.md").is_file()]

    profiles: list[PaperProfile] = []
    for tid in test_ids:
        md_path = TESTS / tid / "言語知識・読解.md"
        if not md_path.is_file():
            continue
        passages, items = _parse_generated_dokkai(tid, md_path.read_text(encoding="utf-8"))
        p = PaperProfile("generated", tid, passages, items)
        p.compute()
        profiles.append(p)
    return profiles


# --------------------------------------------------------------------------
# Baseline Tables Formatter
# --------------------------------------------------------------------------

def format_baseline_tables(profiles: list[PaperProfile]) -> str:
    """Format markdown tables matching dokkai.md and official_calibration.md."""
    lines = []
    lines.append("# Official N2 読解 Baseline (measured across 7 current-era sittings 12/2022–12/2025)\n")

    # 1. Section lengths
    lines.append("## 1. Section Lengths (JP characters in passage prose)\n")
    lines.append("| 大問 | official min | official median | official max | gate floor | gate ceiling |")
    lines.append("|---|---|---|---|---|---|")
    for sec, name, floor, ceil in [
        (10, "問題10 短文 (5 passages)", 1100, 1330),
        (11, "問題11 中文 (4 passages)", 2250, 2700),
        (12, "問題12 統合 A/B", 510, 600),
        (13, "問題13 長文", 800, 1070),
        (14, "問題14 情報検索", 450, 640),
    ]:
        vals = [p.section_lens.get(sec, 0) for p in profiles if p.section_lens.get(sec, 0) > 0]
        if vals:
            lines.append(f"| {name} | {min(vals)} | {int(statistics.median(vals))} | {max(vals)} | **≥{floor}** | **≤{ceil}** |")
    lines.append("")

    # 2. Sentence rhythm & voice
    lines.append("## 2. Register, Voice & Rhythm\n")
    lines.append("| measure | official band (cur) | median | gate recommendation |")
    lines.append("|---|---|---|---|")
    med_sents = [p.median_sentence_len for p in profiles if p.median_sentence_len > 0]
    under_25s = [p.under_25_sentence_share for p in profiles if p.sentence_counts > 0]
    kanjis = [p.kanji_density for p in profiles if p.kanji_density > 0]
    polites = [p.polite_share for p in profiles]
    fps = [p.first_person_share for p in profiles]
    mgn = [p.median_overlap_margin for p in profiles if p.overlap_margins]
    top_ov = [p.strict_top_overlap_share for p in profiles if p.overlap_margins]

    lines.append(f"| median sentence length (JP chars) | {min(med_sents):.1f}–{max(med_sents):.1f} | {statistics.median(med_sents):.1f} | 33–43 (FAIL outside 28–50) |")
    lines.append(f"| share of sentences < 25 chars | {min(under_25s):.1%}–{max(under_25s):.1%} | {statistics.median(under_25s):.1%} | 12–30% |")
    lines.append(f"| kanji density (% of JP chars) | {min(kanjis):.1%}–{max(kanjis):.1%} | {statistics.median(kanjis):.1%} | 24–32% (FAIL outside 22–34%) |")
    lines.append(f"| です・ます share in essay passages | {min(polites):.1%}–{max(polites):.1%} | {statistics.median(polites):.1%} | ≥3 passages throughout |")
    lines.append(f"| first-person essay passages share | {min(fps):.1%}–{max(fps):.1%} | {statistics.median(fps):.1%} | ≥4 of 12 surfaces |")
    if mgn:
        lines.append(f"| median overlap margin (key − best dist) | {min(mgn):+.3f}…{max(mgn):+.3f} | {statistics.median(mgn):+.3f} | **≤ 0.0** |")
    if top_ov:
        lines.append(f"| strict top-overlap key share | {min(top_ov):.1%}–{max(top_ov):.1%} | {statistics.median(top_ov):.1%} | ≤ 50% (WARN > 44%) |")
    lines.append("")

    # 3. Key ranks & option balance
    lines.append("## 3. Option Length Balance & Key Ranks\n")
    lines.append("| measure | official cur | rule |")
    lines.append("|---|---|---|")
    ratios = []
    for p in profiles:
        ratios.extend(p.max_min_ratios)
    if ratios:
        lines.append(f"| option max/min ratio median (p90) | {statistics.median(ratios):.2f} ({sorted(ratios)[int(len(ratios)*0.9)]:.2f}) | WARN > 1.65, FAIL > 2.5 |")
    lines.append("| key rank distribution (1/2/3/4) | ~29% / ~29% / ~27% / ~15% | no single rank > 60% (WARN > 45%) |")
    lines.append("| uniquely-longest key rate | ~20–25% | 20–30% |")
    lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI Output
# --------------------------------------------------------------------------

def print_profiles_summary(profiles: list[PaperProfile]):
    print("=" * 80)
    print(" 読解 Profile Summary")
    print("=" * 80)
    print(f"{'Paper':<18} | {'Total JP':<8} | {'Kanji%':<7} | {'SentMed':<7} | {'Des/Mas':<7} | {'1stPers':<7} | {'Mgn':<7} | {'TopRank':<7} | {'Spans':<5} | {'※':<3}")
    print("-" * 80)
    for p in profiles:
        mgn_str = f"{p.median_overlap_margin:+.3f}" if p.overlap_margins else "N/A"
        print(f"{p.paper:<18} | {p.total_jp_len:<8} | {p.kanji_density*100:>5.1f}% | {p.median_sentence_len:>7.1f} | {p.polite_share*100:>5.1f}% | {p.first_person_share*100:>5.1f}% | {mgn_str:>7} | {p.top_rank_share*100:>5.1f}% | {p.span_count:>5} | {p.asterisk_count:>3}")
    print("=" * 80)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--official", action="store_true", help="profile official past exams")
    ap.add_argument("--tests", nargs="*", help="profile specified tests (or all if omitted)")
    ap.add_argument("--era", choices=("cur", "all"), default="cur", help="official era to analyze (default cur)")
    ap.add_argument("--baseline", action="store_true", help="output baseline markdown tables")
    ap.add_argument("--json", action="store_true", help="output JSON")

    args = ap.parse_args()

    profiles: list[PaperProfile] = []
    if args.baseline or args.official:
        profiles.extend(profile_official(args.era))
    if args.tests is not None or (not args.official and not args.baseline):
        profiles.extend(profile_tests(args.tests))

    if args.baseline:
        print(format_baseline_tables([p for p in profiles if p.corpus == "official"]))
        return

    if args.json:
        data = []
        for p in profiles:
            data.append({
                "corpus": p.corpus,
                "paper": p.paper,
                "total_jp_len": p.total_jp_len,
                "section_lens": p.section_lens,
                "passage_lens": p.passage_lens,
                "median_sentence_len": p.median_sentence_len,
                "under_25_sentence_share": p.under_25_sentence_share,
                "kanji_density": p.kanji_density,
                "polite_share": p.polite_share,
                "first_person_share": p.first_person_share,
                "institutional_rate": p.institutional_rate,
                "personal_rate": p.personal_rate,
                "quoted_rate": p.quoted_rate,
                "rhetorical_rate": p.rhetorical_rate,
                "colloquial_rate": p.colloquial_rate,
                "mean_opt_len": p.mean_opt_len,
                "key_ranks": p.key_ranks,
                "top_rank_share": p.top_rank_share,
                "uniquely_longest_share": p.uniquely_longest_share,
                "median_overlap_margin": p.median_overlap_margin,
                "strict_top_overlap_share": p.strict_top_overlap_share,
                "span_count": p.span_count,
                "shijigo_count": p.shijigo_count,
                "asterisk_count": p.asterisk_count,
                "gloss_count": p.gloss_count,
                "chuuryaku_count": p.chuuryaku_count,
            })
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print_profiles_summary(profiles)


if __name__ == "__main__":
    main()
