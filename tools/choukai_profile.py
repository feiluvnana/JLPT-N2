#!/usr/bin/env python3
"""聴解 (問題1–5) measurement — ONE parser, both corpora, two consumers.

Why this file exists (REPORT-CHOUKAI.md §F1, §F2, §F3, §F7, §D1): every 聴解 number
the rules are built on used to live in prose or uncommitted one-shot analyses,
with the gate re-implementing it, leading to measurement drift and unreproducible
targets. So the measurement lives here, once:

  * `tools/check_consistency.py` imports this module for its 聴解 checks —
    the gate keeps owning the THRESHOLDS, this file owns the MEASUREMENT;
  * `--baseline` prints the official tables in the Markdown shape
    `official_register.md` / `official_pacing.md` / `choukai-items.md` carry,
    so refreshing a doc is a paste, not a retype.

Usage:
    python3 tools/choukai_profile.py --official [--era cur|all]
    python3 tools/choukai_profile.py --tests [20260819_1 …]   (default: every generated test)
    python3 tools/choukai_profile.py --baseline [--json]
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import hashlib
import json
import math
import re
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "refs" / "JLPT_N2_NEW"
TESTS = ROOT / "tests"

JP_CHAR = re.compile(r"[぀-ヿ一-鿿ー。、！？（）「」『』…・]")
KANJI = re.compile(r"[一-鿿]")
KANA = re.compile(r"[぀-ヿー]")
HIRAGANA = re.compile(r"[ぁ-ゟ]")

FULLWIDTH = str.maketrans("０１２３４５６７８９", "0123456789")

CURRENT_ERA = (
    "13. N2 12-2022",
    "14. N2 7-2023",
    "14. N2 12-2023",
    "15. N2 7-2024",
    "15. N2 12-2024",
    "16. N2 7-2025",
    "17.N2 12-2025",
)

FILLERS = ("あのう", "あの、", "えー", "えっと", "ええと", "うーん", "まあ、", "あ、", "ああ、")
OPENER_TOKENS = (
    "はい", "うん", "ああ", "ええ", "あ、", "じゃ", "うーん", "あの", "へえ",
    "でも", "あのう", "えー", "いや", "まあ", "それが", "えっと", "ええと", "いえ"
)

CONTRACTION_RE = re.compile(r"(てる|てた|とく|といた|ちゃう|ちゃった|じゃう|じゃった|なきゃ|なきゃならない|てく|てかない|ちゃだめ|じゃだめ)")
DENIAL_RE = re.compile(r"(ではありません|じゃありません|必要は?ありません|しなくていい)")
P3_DENIAL_RE = re.compile(r"(話ではありません|論じているのでもありません|取り上げているわけでもありません|わけでもありません)")
ALREADY_DONE_RE = re.compile(r"(もう|すでに|既に|さっき|先ほど|今しがた|たった今)")
Q4_SHAPE_RE = re.compile(r"^(はい|いいえ|いえ|では)[、。]")
PROPOSAL_RE = re.compile(r"(ましょうか|ますか|はどうですか|はいかがですか|は。)[。？\?]?$")
REACTION_MAX_CH = 12

SERVICE_FORMULAS = {
    "かしこまりました": re.compile(r"かしこまりました"),
    "〜ていただけますか": re.compile(r"(ていただけますか|ていただけないでしょうか|ていただければ)"),
    "よろしいでしょうか": re.compile(r"よろしいでしょうか"),
    "あ、そうなんですね": re.compile(r"(あ、そうなんですね|そうなんですね)"),
    "〜た方がいいですか": re.compile(r"た方がいいですか"),
    "〜ておきましょうか": re.compile(r"(ておきましょうか|ときましょうか)"),
    "そうですね": re.compile(r"そうですね"),
}

FEMALE_BASE_F0 = 210.0
MALE_BASE_F0 = 120.0

SPEAKER_MAP_FALLBACK = {
    "男": {"voice": "MALE", "pitch": 0.0},
    "男1": {"voice": "MALE", "pitch": 18.0},
    "男2": {"voice": "MALE", "pitch": -16.0},
    "夫": {"voice": "MALE", "pitch": -12.0},
    "学生": {"voice": "MALE", "pitch": 14.0},
    "部長": {"voice": "MALE", "pitch": -18.0},
    "店長": {"voice": "MALE", "pitch": 10.0},
    "教授": {"voice": "MALE", "pitch": -20.0},
    "FP": {"voice": "MALE", "pitch": -14.0},
    "女": {"voice": "FEMALE", "pitch": 0.0},
    "妻": {"voice": "FEMALE", "pitch": 16.0},
    "店員": {"voice": "FEMALE", "pitch": 22.0},
    "先生": {"voice": "FEMALE", "pitch": -16.0},
    "医者": {"voice": "FEMALE", "pitch": -10.0},
    "専門家": {"voice": "FEMALE", "pitch": -22.0},
    "レポーター": {"voice": "FEMALE", "pitch": 25.0},
    "教室の人": {"voice": "FEMALE", "pitch": 12.0},
    "職員": {"voice": "FEMALE", "pitch": -14.0},
    "係員": {"voice": "FEMALE", "pitch": 18.0},
    "担当者": {"voice": "FEMALE", "pitch": -20.0},
    "講師": {"voice": "FEMALE", "pitch": -25.0},
    "アナウンス": {"voice": "FEMALE", "pitch": 8.0},
    "アナウンサー": {"voice": "FEMALE", "pitch": 20.0},
    "男性職員": {"voice": "MALE", "pitch": -14.0},
    "女性職員": {"voice": "FEMALE", "pitch": -14.0},
    "男性係員": {"voice": "MALE", "pitch": 8.0},
    "女性係員": {"voice": "FEMALE", "pitch": 18.0},
    "男性担当者": {"voice": "MALE", "pitch": -20.0},
    "女性担当者": {"voice": "FEMALE", "pitch": -20.0},
    "男性講師": {"voice": "MALE", "pitch": -24.0},
    "女性講師": {"voice": "FEMALE", "pitch": -25.0},
    "男性専門家": {"voice": "MALE", "pitch": -10.0},
    "女性専門家": {"voice": "FEMALE", "pitch": -22.0},
    "男性店員": {"voice": "MALE", "pitch": 12.0},
    "女性店員": {"voice": "FEMALE", "pitch": 22.0},
    "男性医者": {"voice": "MALE", "pitch": -8.0},
    "女性医者": {"voice": "FEMALE", "pitch": -10.0},
    "男性アナウンサー": {"voice": "MALE", "pitch": 6.0},
    "女性アナウンサー": {"voice": "FEMALE", "pitch": 20.0},
}


def jp(s: str) -> int:
    return len(JP_CHAR.findall(s))


def semitone_diff(voice: str, pitch1_hz: float, pitch2_hz: float) -> float:
    base = FEMALE_BASE_F0 if voice == "FEMALE" else MALE_BASE_F0
    f1 = base + pitch1_hz
    f2 = base + pitch2_hz
    if f1 <= 0 or f2 <= 0:
        return 0.0
    return abs(12.0 * math.log2(f1 / f2))


@dataclasses.dataclass
class Turn:
    speaker: str
    text: str

    @property
    def length(self) -> int:
        return jp(self.text)

    @property
    def is_short_reaction(self) -> bool:
        return self.length <= REACTION_MAX_CH

    @property
    def has_opener(self) -> bool:
        t = self.text.strip()
        return any(t.startswith(op) for op in OPENER_TOKENS)


@dataclasses.dataclass
class Item:
    test_id: str
    corpus: str  # "official" | "generated"
    section: int  # 1..5
    item_label: str  # "1番", "例", "2番-質問1"
    is_example: bool
    leadin: str
    question: str
    turns: list[Turn] = dataclasses.field(default_factory=list)
    options: list[str] = dataclasses.field(default_factory=list)
    key: int | None = None
    decider_quote: str | None = None
    decider_pos: float | None = None

    @property
    def dialogue_text(self) -> str:
        return "\n".join(f"{t.speaker}:{t.text}" for t in self.turns)

    @property
    def spoken_chars(self) -> int:
        return sum(t.length for t in self.turns)

    @property
    def proposal_turn_count(self) -> int:
        count = 0
        for t in self.turns:
            clean = re.sub(r"[。！？\?]+$", "", t.text.strip())
            if PROPOSAL_RE.search(clean) or t.text.strip().endswith(("ましょうか。", "ますか。", "はどうですか。", "はいかがですか。")):
                count += 1
        return count


@dataclasses.dataclass
class Sitting:
    test_id: str
    corpus: str
    items: list[Item] = dataclasses.field(default_factory=list)
    raw_text: str = ""

    def items_for_section(self, sec: int, scored_only: bool = True) -> list[Item]:
        return [it for it in self.items if it.section == sec and (not scored_only or not it.is_example)]


def classify_q1_form(question: str) -> str:
    """Classify 問題1 質問型 according to standard taxonomy."""
    q = question.strip()
    if re.search(r"まず|最初", q):
        return "まず"
    if re.search(r"どう直|どのように|どう変更|手直し|仕上げ", q):
        return "どう直す・方法"
    if re.search(r"どの(?:番号|順番|席|順|部屋)|どれを選", q):
        return "条件一致"
    if re.search(r"何を(?:持って|出|書|買|用意|提出)", q):
        return "物・提出"
    if re.search(r"いつ|いくら|どこ", q):
        return "時・額・場所"
    if re.search(r"何をし|何をしなければ", q):
        return "何をしますか"
    return "その他"


def classify_q2_form(question: str) -> str:
    """Classify 問題2 質問型 priority: 気持ち -> 理由 -> 一番 -> どのように -> 内容/発言."""
    q = question.strip()
    if re.search(r"気持ち|どうして怒|残念|心配|困っ", q):
        return "気持ち"
    if re.search(r"どうして|なぜ|理由", q):
        return "理由"
    if re.search(r"一番|最も|優先", q):
        return "一番・優先"
    if re.search(r"どのように", q):
        return "どのように"
    if re.search(r"何|どれ|どんな|と言っていますか|言っていますか", q):
        return "内容・発言"
    return "その他"


def classify_p3_speaker(leadin: str) -> str:
    """Classify 問題3 lead-in speaker type."""
    if re.search(r"担当者|職員|係員|講師|専門家|店長|アナウンス|アナウンサー|医師|医者|教授|館長|署長|レポーター|店員", leadin):
        return "institutional"
    if re.search(r"男の人|女の人|学生|会社員|男性|女性|住民|客|観光客|留学生|人", leadin):
        return "ordinary_person"
    return "other"


def classify_p4_stimulus(stimulus: str) -> str:
    """Classify 問題4 prompt register."""
    if re.search(r"ございます|いただ|ておりま|申し訳|伺|存じ|いらっしゃ|なさ|くださ|ご[一-鿿]{2,}をお願い", stimulus):
        return "keigo"
    if re.search(r"(だよ|だね|よね|んだ|かな|でしょ|じゃん|って|かい|ぞ|ない？|ないの？|いいの？)[。！？!?]?$", stimulus) or re.search(r"[だで]よ|[だで]ね|よね|んだよ|んだね", stimulus):
        return "casual"
    return "neutral"


# -----------------------------------------------------------------------------
# Parser 1: Official Scripts (refs/JLPT_N2_NEW/*/script.md)
# -----------------------------------------------------------------------------

def parse_official_sitting(script_path: Path) -> Sitting:
    sitting_name = script_path.parent.name
    text = script_path.read_text(encoding="utf-8").translate(FULLWIDTH)
    clean_lines = []
    for ln in text.splitlines():
        ln_s = ln.strip()
        if not ln_s or ln_s.startswith(("#", ">", "[OCR")):
            continue
        clean_lines.append(ln_s)

    items: list[Item] = []
    cur_sec = 0
    cur_item: Item | None = None

    sec_splits = re.split(r"^#+\s*問題\s*([1-5１-５])", text, flags=re.M)
    for i in range(1, len(sec_splits), 2):
        sec_num = int(sec_splits[i])
        sec_content = sec_splits[i + 1]

        item_blocks = re.split(r"(?:^|\n)(?:(\d+)\s*番|(例))\s*", sec_content)
        j = 1
        while j < len(item_blocks):
            label_num = item_blocks[j]
            label_ex = item_blocks[j + 1] if j + 1 < len(item_blocks) else None
            block_body = item_blocks[j + 2] if j + 2 < len(item_blocks) else ""
            j += 3

            is_ex = bool(label_ex)
            item_lab = "例" if is_ex else f"{label_num}番"

            lines = [l.strip() for l in block_body.splitlines() if l.strip() and not l.strip().startswith(("[OCR", ">"))]
            if not lines:
                continue

            leadin = lines[0]
            question = ""
            q_match = re.search(r"問い\s*(.*?)(?:（正解[：:]\s*([1-4])）|\Z)", block_body)
            key = None
            if q_match:
                question = q_match.group(1).strip()
                if q_match.group(2):
                    key = int(q_match.group(2))
            elif "？" in leadin or "か。" in leadin:
                question = leadin

            turns: list[Turn] = []
            cur_spk: str | None = None
            cur_txt: list[str] = []

            for l in lines:
                if l.startswith("問い"):
                    continue
                spk_match = re.match(r"^([^:：]{1,8})[：:](.*)$", l)
                if spk_match:
                    if cur_spk:
                        turns.append(Turn(cur_spk, "".join(cur_txt)))
                    cur_spk = spk_match.group(1).strip()
                    cur_txt = [spk_match.group(2).strip()]
                elif cur_spk:
                    if not re.match(r"^[1-4][、\.．]", l):
                        cur_txt.append(l.strip())

            if cur_spk:
                turns.append(Turn(cur_spk, "".join(cur_txt)))

            opts: list[str] = []
            for l in lines:
                om = re.match(r"^([1-4])[、\.．\s]+(.*)$", l)
                if om:
                    opts.append(om.group(2).strip())

            item = Item(
                test_id=sitting_name,
                corpus="official",
                section=sec_num,
                item_label=item_lab,
                is_example=is_ex,
                leadin=leadin,
                question=question,
                turns=turns,
                options=opts,
                key=key
            )
            items.append(item)

    return Sitting(test_id=sitting_name, corpus="official", items=items, raw_text=text)


# -----------------------------------------------------------------------------
# Parser 2: Generated Scripts (tests/<id>/聴解スクリプト.txt + 聴解.md)
# -----------------------------------------------------------------------------

def parse_generated_sitting(test_dir: Path) -> Sitting:
    test_id = test_dir.name
    st_path = test_dir / "聴解スクリプト.txt"
    ct_path = test_dir / "聴解.md"

    if not st_path.is_file():
        return Sitting(test_id=test_id, corpus="generated")

    st_text = st_path.read_text(encoding="utf-8")
    ct_text = ct_path.read_text(encoding="utf-8") if ct_path.is_file() else ""

    decider_quotes: dict[tuple[int, str], str] = {}
    if ct_text:
        for line in ct_text.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 3 and re.match(r"^(例|\d+番)", cells[0]):
                lab = cells[0]
                expl = cells[-1]
                quotes = re.findall(r"「([^」]+)」", expl)
                if quotes:
                    decider_quotes[(1, lab)] = quotes[-1]

    items: list[Item] = []
    blocks = [b.strip() for b in re.split(r"\n\s*\n", st_text) if b.strip()]

    cur_sec = 0
    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        first = lines[0]
        sec_m = re.match(r"^問題([1-5])。", first)
        if sec_m:
            cur_sec = int(sec_m.group(1))
            continue

        item_m = re.match(r"^(例|\d+番)。(.*)$", first)
        if item_m and cur_sec > 0:
            item_lab = item_m.group(1)
            is_ex = (item_lab == "例")
            leadin = item_m.group(2).strip()

            question = ""
            if "？" in leadin or "か。" in leadin:
                question = leadin
            if len(lines) > 1 and not re.match(r"^[1-4]、", lines[-1]) and not re.match(r"^[^:：]{1,6}[:：]", lines[-1]):
                question = lines[-1]

            turns: list[Turn] = []
            opts: list[str] = []
            for l in lines[1:]:
                spk_m = re.match(r"^([^:：]{1,6})[:：](.*)$", l)
                opt_m = re.match(r"^([1-4])、(.*)$", l)
                if spk_m:
                    turns.append(Turn(spk_m.group(1).strip(), spk_m.group(2).strip()))
                elif opt_m:
                    opts.append(opt_m.group(2).strip())

            decider_pos = None
            dec_q = decider_quotes.get((cur_sec, item_lab))
            if dec_q and turns:
                total_t = len(turns)
                for idx, t in enumerate(turns):
                    if dec_q[:10] in t.text or t.text[:10] in dec_q:
                        decider_pos = idx / max(total_t - 1, 1)
                        break

            item = Item(
                test_id=test_id,
                corpus="generated",
                section=cur_sec,
                item_label=item_lab,
                is_example=is_ex,
                leadin=leadin,
                question=question,
                turns=turns,
                options=opts,
                decider_quote=dec_q,
                decider_pos=decider_pos
            )
            items.append(item)

    return Sitting(test_id=test_id, corpus="generated", items=items, raw_text=st_text)


# -----------------------------------------------------------------------------
# Metric Calculations & Summaries
# -----------------------------------------------------------------------------

def calculate_sitting_profile(sitting: Sitting) -> dict[str, Any]:
    all_turns = [t for it in sitting.items for t in it.turns]
    total_turns = len(all_turns)
    turn_lengths = [t.length for t in all_turns]

    total_spoken_chars = sum(turn_lengths)
    denom_10k = max(total_spoken_chars / 10000.0, 1e-9)

    short_reactions = [t for t in all_turns if t.is_short_reaction]
    openers = [t for t in all_turns if t.has_opener]

    raw_text = sitting.raw_text
    fillers_count = sum(raw_text.count(f) for f in FILLERS)
    contractions_count = len(CONTRACTION_RE.findall(raw_text))
    denials_count = len(DENIAL_RE.findall(raw_text))
    san_count = len(re.findall(r"[一-鿿ぁ-ゖァ-ヶ]+さん\b", raw_text))
    ichiban_count = raw_text.count("一番")

    service_counts = {k: len(rx.findall(raw_text)) for k, rx in SERVICE_FORMULAS.items()}

    # 問題1
    q1_items = sitting.items_for_section(1, scored_only=True)
    q1_mazu_count = sum(1 for it in q1_items if "まず" in it.question or "最初" in it.question)
    q1_forms = collections.Counter(classify_q1_form(it.question) for it in q1_items)
    q1_single_speaker = sum(1 for it in q1_items if len(set(t.speaker for t in it.turns)) <= 1)
    q1_proposals = [it.proposal_turn_count for it in q1_items]
    q1_deciders = [it.decider_pos for it in q1_items if it.decider_pos is not None]

    # 問題2
    q2_items = sitting.items_for_section(2, scored_only=True)
    q2_forms = collections.Counter(classify_q2_form(it.question) for it in q2_items)

    # 問題3
    q3_items = sitting.items_for_section(3, scored_only=True)
    q3_speakers = collections.Counter(classify_p3_speaker(it.leadin) for it in q3_items)
    q3_lengths = [it.spoken_chars for it in q3_items]
    q3_suffixed = sum(1 for it in q3_items for o in it.options if o.endswith("について"))

    # 問題4
    q4_items = sitting.items_for_section(4, scored_only=True)
    q4_stimuli = collections.Counter(classify_p4_stimulus(it.leadin) for it in q4_items)
    q4_done_count = sum(1 for it in q4_items if any(ALREADY_DONE_RE.search(o) for o in it.options))
    q4_yes_no_replies = sum(1 for it in q4_items for o in it.options if Q4_SHAPE_RE.match(o))
    total_q4_replies = sum(len(it.options) for it in q4_items)

    # 問題5
    q5_items = sitting.items_for_section(5, scored_only=False)
    q5_3spk_count = sum(1 for it in q5_items if len(set(t.speaker for t in it.turns)) >= 3)

    # Voice balance per section
    voice_balance: dict[int, dict[str, int]] = collections.defaultdict(lambda: {"MALE": 0, "FEMALE": 0})
    for it in sitting.items:
        for t in it.turns:
            spk_info = SPEAKER_MAP_FALLBACK.get(t.speaker, {"voice": "FEMALE" if "女" in t.speaker or t.speaker in ("店員", "職員", "係員", "担当者", "講師", "専門家", "レポーター") else "MALE"})
            v = spk_info.get("voice", "FEMALE")
            voice_balance[it.section][v] += 1

    return {
        "test_id": sitting.test_id,
        "corpus": sitting.corpus,
        "total_turns": total_turns,
        "total_spoken_chars": total_spoken_chars,
        "turn_length_median": statistics.median(turn_lengths) if turn_lengths else 0,
        "turn_length_p25": statistics.quantiles(turn_lengths, n=4)[0] if len(turn_lengths) >= 4 else 0,
        "turn_length_p75": statistics.quantiles(turn_lengths, n=4)[2] if len(turn_lengths) >= 4 else 0,
        "turn_length_max": max(turn_lengths) if turn_lengths else 0,
        "short_reactions_count": len(short_reactions),
        "short_reactions_share": len(short_reactions) / max(total_turns, 1),
        "openers_count": len(openers),
        "openers_share": len(openers) / max(total_turns, 1),
        "fillers_count": fillers_count,
        "fillers_per_10k": fillers_count / denom_10k,
        "contractions_count": contractions_count,
        "contractions_per_10k": contractions_count / denom_10k,
        "denials_count": denials_count,
        "denials_per_10k": denials_count / denom_10k,
        "san_per_10k": san_count / denom_10k,
        "ichiban_per_10k": ichiban_count / denom_10k,
        "service_counts": service_counts,
        "q1_item_count": len(q1_items),
        "q1_mazu_count": q1_mazu_count,
        "q1_mazu_share": q1_mazu_count / max(len(q1_items), 1),
        "q1_forms": dict(q1_forms),
        "q1_single_speaker": q1_single_speaker,
        "q1_proposals_median": statistics.median(q1_proposals) if q1_proposals else 0,
        "q1_proposals_max": max(q1_proposals) if q1_proposals else 0,
        "q1_decider_pos": q1_deciders,
        "q2_item_count": len(q2_items),
        "q2_forms": dict(q2_forms),
        "q3_item_count": len(q3_items),
        "q3_speakers": dict(q3_speakers),
        "q3_length_median": statistics.median(q3_lengths) if q3_lengths else 0,
        "q3_length_min": min(q3_lengths) if q3_lengths else 0,
        "q3_length_max": max(q3_lengths) if q3_lengths else 0,
        "q3_suffixed_count": q3_suffixed,
        "q4_item_count": len(q4_items),
        "q4_stimuli": dict(q4_stimuli),
        "q4_done_count": q4_done_count,
        "q4_yes_no_replies": q4_yes_no_replies,
        "q4_yes_no_share": q4_yes_no_replies / max(total_q4_replies, 1),
        "q5_3spk_count": q5_3spk_count,
        "voice_balance": {sec: dict(vb) for sec, vb in voice_balance.items()},
    }


def format_baseline_markdown(official_profiles: list[dict[str, Any]], current_only: bool = False) -> str:
    n_sittings = len(official_profiles)
    all_turns = sum(p["total_turns"] for p in official_profiles)
    all_chars = sum(p["total_spoken_chars"] for p in official_profiles)
    all_denom_10k = all_chars / 10000.0

    all_reactions = sum(p["short_reactions_count"] for p in official_profiles)
    all_openers = sum(p["openers_count"] for p in official_profiles)
    all_fillers = [p["fillers_count"] for p in official_profiles]
    all_contractions = [p["contractions_per_10k"] for p in official_profiles]
    all_denials = [p["denials_per_10k"] for p in official_profiles]

    q1_total = sum(p["q1_item_count"] for p in official_profiles)
    q1_mazu_total = sum(p["q1_mazu_count"] for p in official_profiles)

    q2_totals = collections.Counter()
    for p in official_profiles:
        for k, v in p["q2_forms"].items():
            q2_totals[k] += v
    q2_total_items = sum(q2_totals.values()) or 1

    q3_medians = [p["q3_length_median"] for p in official_profiles if p["q3_length_median"] > 0]
    q3_speakers = collections.Counter()
    for p in official_profiles:
        for k, v in p["q3_speakers"].items():
            q3_speakers[k] += v
    q3_total_spk = sum(q3_speakers.values()) or 1

    q4_stimuli = collections.Counter()
    for p in official_profiles:
        for k, v in p["q4_stimuli"].items():
            q4_stimuli[k] += v
    q4_total_stim = sum(q4_stimuli.values()) or 1
    q4_yes_no = sum(p["q4_yes_no_replies"] for p in official_profiles)

    lines = []
    lines.append(f"# Official Choukai Baseline Table ({n_sittings} sittings, {all_chars:,} spoken chars, {all_turns:,} turns)\n")
    lines.append("## 1. Register & Pacing Counts\n")
    lines.append("| Measure | Official Measured | Target Band / Threshold |")
    lines.append("|---|---|---|")
    lines.append(f"| short reaction turns (≤12 chars) | **{all_reactions / max(all_turns, 1):.1%}** ({all_reactions}/{all_turns}) | target ≥ 18%, gate floor ≥ 12% |")
    lines.append(f"| turns opening with a filler/reaction | **{all_openers / max(all_turns, 1):.1%}** ({all_openers}/{all_turns}) | target ≥ 35% |")
    lines.append(f"| hesitation tokens per sitting | **median {statistics.median(all_fillers):.0f}**, min {min(all_fillers)}, max {max(all_fillers)} | band {min(all_fillers)}–{max(all_fillers)} (gate: 9–48) |")
    lines.append(f"| flat contradiction 「〜ではありません」/10k chars | **{sum(p['denials_count'] for p in official_profiles) / all_denom_10k:.1f}** | gate ceiling ≤ 6.0/10k |")
    lines.append(f"| 縮約形 per 10k chars | **median {statistics.median(all_contractions):.1f}** [{min(all_contractions):.1f}–{max(all_contractions):.1f}] | target ≥ 37.3, gate floor ≥ 22.4 |")
    lines.append(f"| 問題4 replies opening はい/いいえ/では | **{q4_yes_no / max(sum(p['q4_item_count']*3 for p in official_profiles), 1):.1%}** | gate ceiling ≤ 20% |")

    lines.append("\n## 2. 問題1 質問型 Mix\n")
    lines.append(f"Total 問題1 items analyzed: {q1_total} (まず/最初 present: **{q1_mazu_total / max(q1_total, 1):.1%}**)\n")
    lines.append("| Question Frame | Count | Share | Target Quota |")
    lines.append("|---|---|---|---|")
    q1_all_forms = collections.Counter()
    for p in official_profiles:
        for k, v in p["q1_forms"].items():
            q1_all_forms[k] += v
    for form, cnt in q1_all_forms.most_common():
        lines.append(f"| {form} | {cnt} | {cnt / max(q1_total, 1):.1%} | {'≤ 3 of 6' if form == 'まず' else '≥ 1 of 6' if form in ('どう直す・方法', '条件一致') else '—'} |")

    lines.append("\n## 3. 問題2 質問型 Mix\n")
    lines.append("| Question Type | Count | Share | Target Quota |")
    lines.append("|---|---|---|---|")
    for form, cnt in q2_totals.most_common():
        quota = "≥ 2 of 6" if form == "内容・発言" else "≤ 3 of 6" if form == "理由" else "≤ 2 of 6" if form == "一番・優先" else "≥ 1 of 6" if form == "気持ち" else "—"
        lines.append(f"| {form} | {cnt} | {cnt / q2_total_items:.1%} | {quota} |")

    lines.append("\n## 4. 問題3 概要理解\n")
    lines.append(f"- Speaker distribution: **{q3_speakers.get('institutional', 0) / q3_total_spk:.1%}** institutional vs **{q3_speakers.get('ordinary_person', 0) / q3_total_spk:.1%}** ordinary person (target: ≤2 institutional, ≥3 ordinary person)")
    lines.append(f"- Talk length (spoken chars): median **{statistics.median(q3_medians):.0f}**, min {min(p['q3_length_min'] for p in official_profiles if p['q3_length_min'] > 0)}, max {max(p['q3_length_max'] for p in official_profiles)} (target: 220–300 chars, gate floor: 175)")
    lines.append(f"- Options suffixed 「〜について」: **{sum(p['q3_suffixed_count'] for p in official_profiles)}** total (target: 0, gate: ≤ 2)")

    lines.append("\n## 5. 問題4 即時応答\n")
    lines.append(f"- Stimulus register: **{q4_stimuli.get('casual', 0) / q4_total_stim:.1%}** casual vs **{q4_stimuli.get('keigo', 0) / q4_total_stim:.1%}** keigo counter prompts (target: ≥5 casual, ≤2 keigo)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Choukai profile measurement tool.")
    parser.add_argument("--official", action="store_true", help="Analyze official past exam scripts")
    parser.add_argument("--tests", nargs="*", help="Analyze generated test IDs (default: all)")
    parser.add_argument("--baseline", action="store_true", help="Output markdown baseline table for official archive")
    parser.add_argument("--era", choices=["cur", "all"], default="all", help="Era filter for official sittings")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")
    args = parser.parse_args()

    official_sittings: list[Sitting] = []
    if args.official or args.baseline or (not args.tests and not args.official and not args.baseline):
        if REFS.is_dir():
            for p in sorted(REFS.glob("*/script.md")):
                if args.era == "cur" and p.parent.name not in CURRENT_ERA:
                    continue
                official_sittings.append(parse_official_sitting(p))

    test_sittings: list[Sitting] = []
    if args.tests is not None:
        test_ids = args.tests if len(args.tests) > 0 else sorted(p.name for p in TESTS.glob("*") if p.is_dir() and not p.name.startswith("imported-"))
        for tid in test_ids:
            tdir = TESTS / tid
            if tdir.is_dir():
                test_sittings.append(parse_generated_sitting(tdir))

    official_profiles = [calculate_sitting_profile(s) for s in official_sittings]
    test_profiles = [calculate_sitting_profile(s) for s in test_sittings]

    if args.baseline:
        if args.json:
            print(json.dumps(official_profiles, ensure_ascii=False, indent=2))
        else:
            print(format_baseline_markdown(official_profiles, current_only=(args.era == "cur")))
        return

    if args.json:
        out = {"official": official_profiles, "tests": test_profiles}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if official_profiles:
        print(f"=== Official Choukai Profile ({len(official_profiles)} sittings) ===")
        print(format_baseline_markdown(official_profiles))
        print()

    if test_profiles:
        print(f"=== Generated Choukai Profile ({len(test_profiles)} tests) ===")
        for tp in test_profiles:
            print(f"[{tp['test_id']}] {tp['total_turns']} turns, {tp['total_spoken_chars']} chars | "
                  f"reactions: {tp['short_reactions_share']:.1%}, openers: {tp['openers_share']:.1%}, "
                  f"fillers: {tp['fillers_count']} ({tp['fillers_per_10k']:.1f}/10k), 縮約形: {tp['contractions_per_10k']:.1f}/10k | "
                  f"Q1 mazu: {tp['q1_mazu_share']:.0%}, Q3 median len: {tp['q3_length_median']}")


if __name__ == "__main__":
    main()
