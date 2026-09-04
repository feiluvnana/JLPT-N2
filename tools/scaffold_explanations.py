#!/usr/bin/env python3
"""
Scaffold or update tests/<test_id>/詳細解説.json with Knowledge-Assisted Linguistic Pre-Filling.

Why this exists:
Prevents AI models from having to duplicate stems, options, long reading passages,
and listening audio transcripts into JSON from scratch (saving ~75% of Stage 5 token cost).
Also auto-populates standard dictionary facts, grammar connection rules, and correct/distractor
tags to further reduce LLM generation tokens.

Usage:
    python3 tools/scaffold_explanations.py tests/20260814_1
    python3 tools/scaffold_explanations.py tests/20260814_1 --overwrite
    python3 tools/scaffold_explanations.py tests/20260814_1 --lean
    python3 tools/scaffold_explanations.py tests/20260814_1 --lang vi

Outputs:
    tests/<test_id>/詳細解説.json        (--lang ja, the default)
    tests/<test_id>/詳細解説.<lang>.json (any other language)

A non-`ja` scaffold is deliberately EMPTY and carries no exam wording — no
stem, no options, no passage, no script. 詳細解説.json is the single copy of
the booklet's own text; a second copy would be one more surface for it to drift
on, and `verify_fidelity.py` only knows how to police one. The author reads the
wording out of 詳細解説.json (or the booklet) and writes the prose here.

It is also NOT a translation template: the empty fields are there to be written
from the item, not from the Japanese pane beside them (exam-model-answer
"Two languages, two rewrites").

EVERY PRE-FILLED `options_analysis` LINE MUST BE REPLACED BEFORE
`make model-answer`. The `ja` scaffold does not leave those slots empty — it
writes one of four formulaic templates into each ("…は、文脈に合いません。",
"…は、音声の内容と異なります。", "…は、文脈および語用・文法制約に合致します。",
"…は、会話内容の結論に合致しています。"), which saves the author from re-typing
the option text but says nothing a reader could not get from the [不正解] tag.
Those lines are well-formed, correctly tagged and inside every terseness band,
so until 2026-09-05 the whole gate was blind to them and BOTH 2021 imports
shipped Japanese panes that were 100% of them (397/397 and 393/393 lines,
re-measured by re-running this script). `check_kaisetsu_no_scaffold_placeholders`
in tools/check_consistency.py now FAILs any paper that has reached the
model-answer stage and still carries one; its `KAISETSU_SCAFFOLD_TEMPLATES`
tuple is the same list as the four strings below, and **adding a template here
means adding it there** — a template that check does not know is a template
that ships.
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_SCRIPT = ROOT / ".agents/exam-model-answer/scripts/verify_fidelity.py"

_spec = importlib.util.spec_from_file_location("verify_fidelity", VERIFY_SCRIPT)
vf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vf)

BMA_SCRIPT = ROOT / ".agents/exam-model-answer/scripts/build_model_answer.py"
_bma_spec = importlib.util.spec_from_file_location("build_model_answer", BMA_SCRIPT)
bma = importlib.util.module_from_spec(_bma_spec)
_bma_spec.loader.exec_module(bma)


def auto_generate_linguistic_scaffold(q_num: int, raw_info: dict, exp_info: dict) -> dict:
    """Generate pre-filled linguistic explanation scaffolding for Moji/Goi & Bunpou."""
    stem = raw_info.get("stem", "")
    options = raw_info.get("options", [])
    ans_idx = exp_info.get("ans", 1)  # 1-indexed
    raw_kaisetsu = exp_info.get("raw_kaisetsu", "")

    # Tag options analysis with [正解] and [不正解]
    options_analysis = []
    for i, opt in enumerate(options, 1):
        if i == ans_idx:
            options_analysis.append(f"[正解] 選択肢{i}「{opt}」は、文脈および語用・文法制約に合致します。")
        else:
            options_analysis.append(f"[不正解] 選択肢{i}「{opt}」は、文脈に合いません。")

    points = []
    why_correct = raw_kaisetsu if raw_kaisetsu else ""

    # 1. 問題1 漢字読み (1..5)
    if 1 <= q_num <= 5:
        m = re.search(r"\*\*([^*]+)\*\*", stem)
        target = m.group(1) if m else ""
        correct_reading = options[ans_idx - 1] if 0 < ans_idx <= len(options) else ""
        if target and not why_correct:
            why_correct = f"「{target}」の正しい読み方は「{correct_reading}」です。"
        if target:
            points.append(f"【{target}（{correct_reading}）】の意味と用法。")

    # 2. 問題2 表記 (6..10)
    elif 6 <= q_num <= 10:
        m = re.search(r"\*\*([^*]+)\*\*", stem)
        target_kana = m.group(1) if m else ""
        correct_kanji = options[ans_idx - 1] if 0 < ans_idx <= len(options) else ""
        if target_kana and not why_correct:
            why_correct = f"文脈の「{target_kana}」に対応する正しい漢字表記は「{correct_kanji}」です。"
        if correct_kanji:
            points.append(f"【{correct_kanji}】の漢字構成と用例。")

    # 3. 問題3 語形成 (11..13)
    elif 11 <= q_num <= 13:
        correct_affix = options[ans_idx - 1] if 0 < ans_idx <= len(options) else ""
        if not why_correct:
            why_correct = f"文脈に最も適する接辞は「{correct_affix}」です。"
        points.append(f"接辞「{correct_affix}」の接続と意味用法。")

    # 4. 問題7 文法形式 (31..42)
    elif 31 <= q_num <= 42:
        correct_grammar = options[ans_idx - 1] if 0 < ans_idx <= len(options) else ""
        if not why_correct:
            why_correct = f"文脈の意味関係より、文法形式「{correct_grammar}」が適切です。"
        points.append(f"文法項目「{correct_grammar}」の接続と意味。")

    # 5. 問題8 文の組み立て (43..47)
    elif 43 <= q_num <= 47:
        if not why_correct and raw_kaisetsu:
            why_correct = f"正しい文の並び順は {raw_kaisetsu} となり、★の位置に入るのは選択肢 {ans_idx} です。"

    return {
        "why_correct": why_correct,
        "options_analysis": options_analysis,
        "points": points
    }


def stem_fallback(q_num: int) -> str:
    """The stem to show when the booklet prints none for this item.

    問9 (文章の文法) items are a bare numbered blank inside the passage, so the
    source really has no stem text. The fallback used to be the placeholder
    "第 48 問", which only repeats the number badge 模範解答.html already prints
    beside it. Name the blank instead — verify_fidelity.py documents this
    instruction-line shape as an expected, non-drift difference from the
    source, and it is what earlier papers carry by hand.
    """
    for info in bma.GENGO_TAXONOMY.values():
        lo, hi = info["range"]
        if lo <= q_num <= hi and info["name"] == "文章の文法":
            return (f"文章全体の趣旨を踏まえて、（　{q_num}　）に入る"
                    f"最もよいものを、1・2・3・4から一つ選びなさい。")
    return f"第 {q_num} 問"


def scaffold_test(test_dir: Path, lean: bool = False, merge_existing: bool = True) -> dict:
    test_dir = Path(test_dir)
    gengo_md, choukai_md, script_text = vf.load_sources(test_dir)
    gengo_raw = vf.derive_gengo_raw(gengo_md)
    choukai_raw = vf.derive_choukai_raw(choukai_md, script_text)

    _, gengo_exps = bma.parse_gengo_markdown(gengo_md)
    _, choukai_exps = bma.parse_choukai_markdown(choukai_md)

    dest_json = test_dir / "詳細解説.json"
    existing = {}
    if merge_existing and dest_json.is_file():
        try:
            existing = json.loads(dest_json.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    out = {}

    # 1. Gengo & Dokkai (1..N). N is the paper's own last question, not a
    # constant: a generated mock is 71, but an imported past paper may be a
    # 72- or 75-question sitting (jlpt-exam-structure's era table). Hard-coded
    # at 72 this loop silently dropped 7/2021's item 72, and every other
    # 詳細解説 gate line measures the entries that ARE present, so a missing one
    # is invisible everywhere except check_kaisetsu_item_coverage.
    last_q = max([*gengo_raw, *gengo_exps, 71])
    for q_num in range(1, last_q + 1):
        q_str = str(q_num)
        raw_info = gengo_raw.get(q_num, {})
        exp_info = gengo_exps.get(q_num, {})
        ex_item = existing.get(q_str, {})

        stem = ex_item.get("stem") or raw_info.get("stem") or stem_fallback(q_num)
        options = ex_item.get("options") or raw_info.get("options") or [f"選択肢 {i}" for i in range(1, 5)]
        passage = ex_item.get("passage") if "passage" in ex_item else raw_info.get("passage")
        ans_val = exp_info.get("ans", 1)

        auto_scaff = auto_generate_linguistic_scaffold(q_num, raw_info, exp_info)

        why_correct = ex_item.get("why_correct") or auto_scaff["why_correct"]
        options_analysis = ex_item.get("options_analysis") or auto_scaff["options_analysis"]
        points = ex_item.get("points") or auto_scaff["points"]

        item_dict = {}
        if not lean:
            item_dict["stem"] = stem
            item_dict["options"] = options
            if passage:
                item_dict["passage"] = passage

        item_dict["why_correct"] = why_correct
        item_dict["options_analysis"] = options_analysis
        item_dict["points"] = points

        out[q_str] = item_dict

    # 2. Choukai items
    for key_id in sorted(choukai_raw.keys()):
        raw_info = choukai_raw.get(key_id, {})
        exp_info = choukai_exps.get(key_id, {})
        ex_item = existing.get(key_id, {})

        stem = ex_item.get("stem") or raw_info.get("stem") or f"{key_id} 聴解問題"
        options = ex_item.get("options") or raw_info.get("options") or [f"選択肢 {i}" for i in range(1, 5)]
        script = ex_item.get("script") if "script" in ex_item else raw_info.get("script")
        ans_val = exp_info.get("ans", 1)
        raw_kaisetsu = exp_info.get("raw_kaisetsu", "")

        default_opt_analysis = []
        for i, opt in enumerate(options, 1):
            if i == ans_val:
                default_opt_analysis.append(f"[正解] 選択肢{i}「{opt}」は、会話内容の結論に合致しています。")
            else:
                default_opt_analysis.append(f"[不正解] 選択肢{i}「{opt}」は、音声の内容と異なります。")

        why_correct = ex_item.get("why_correct") or (raw_kaisetsu if raw_kaisetsu else "")
        options_analysis = ex_item.get("options_analysis") or default_opt_analysis
        points = ex_item.get("points") or []

        item_dict = {}
        if not lean:
            item_dict["stem"] = stem
            item_dict["options"] = options
            if script:
                item_dict["script"] = script

        item_dict["why_correct"] = why_correct
        item_dict["options_analysis"] = options_analysis
        item_dict["points"] = points

        out[key_id] = item_dict

    return out


def scaffold_secondary(test_dir: Path, existing: dict) -> dict:
    """The skeleton for a non-`ja` explanation set: keys, and nothing to copy.

    Item keys and the per-item option COUNT come from 詳細解説.json, so the two
    panes always describe the same 101 items with the same number of options —
    the parity the gate then enforces. Everything else is left empty on purpose.
    """
    ja_path = test_dir / "詳細解説.json"
    if not ja_path.is_file():
        raise FileNotFoundError(
            f"{ja_path} is missing — author the Japanese set first; it owns the "
            f"item keys and the booklet wording every other language is written against.")
    ja = json.loads(ja_path.read_text(encoding="utf-8"))

    out = {}
    for key, ja_item in ja.items():
        prev = existing.get(key, {})
        n_opts = len(ja_item.get("options_analysis") or ja_item.get("options") or []) or 4
        analysis = prev.get("options_analysis") or [""] * n_opts
        if len(analysis) != n_opts:          # the Japanese set gained or lost an option
            analysis = (analysis + [""] * n_opts)[:n_opts]
        out[key] = {
            "why_correct": prev.get("why_correct", ""),
            "options_analysis": analysis,
            "points": prev.get("points", []),
        }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", help="Path to tests/<test_id>")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite the existing file instead of merging into it")
    ap.add_argument("--lean", action="store_true", help="Exclude duplicate stem/options/passage/script (build_model_answer will pull from source markdown)")
    ap.add_argument("--lang", default="ja", help="Explanation language (default ja -> 詳細解説.json; anything else -> 詳細解説.<lang>.json)")
    ap.add_argument("--stdout", action="store_true", help="Print JSON to stdout without writing file")
    args = ap.parse_args()

    test_dir = Path(args.test_dir)
    if not test_dir.is_dir():
        print(f"Error: Directory not found: {test_dir}", file=sys.stderr)
        sys.exit(1)

    lang = args.lang.strip().lower()
    dest_file = test_dir / ("詳細解説.json" if lang == "ja" else f"詳細解説.{lang}.json")
    if dest_file.exists() and not args.overwrite and not args.stdout:
        print(f"File already exists: {dest_file}. Merging while preserving existing explanations...")

    existing = {}
    if dest_file.is_file() and not args.overwrite:
        try:
            existing = json.loads(dest_file.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    if lang == "ja":
        data = scaffold_test(test_dir, lean=args.lean, merge_existing=not args.overwrite)
    else:
        data = scaffold_secondary(test_dir, existing)

    if args.stdout:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    dest_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Knowledge-assisted scaffolding completed: {len(data)} items into {dest_file}")


if __name__ == "__main__":
    main()
