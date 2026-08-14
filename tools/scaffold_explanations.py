#!/usr/bin/env python3
"""
Scaffold or update tests/<test_id>/詳細解説.json directly from the exam source files
(言語知識・読解.md, 聴解.md, 聴解スクリプト.txt).

Why this exists:
Prevents AI models from having to duplicate stems, options, long reading passages,
and listening audio transcripts into JSON from scratch (saving ~75% of Stage 5 token cost).
Also eliminates manual copy-paste drift and transcription errors.

Usage:
    python3 tools/scaffold_explanations.py tests/20260813_2
    python3 tools/scaffold_explanations.py tests/20260813_2 --overwrite
    python3 tools/scaffold_explanations.py tests/20260813_2 --lean   # Scaffold explanation fields only

Outputs:
    tests/<test_id>/詳細解説.json
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

    # 1. Gengo & Dokkai (1..71)
    for q_num in range(1, 72):
        q_str = str(q_num)
        raw_info = gengo_raw.get(q_num, {})
        exp_info = gengo_exps.get(q_num, {})
        ex_item = existing.get(q_str, {})

        stem = ex_item.get("stem") or raw_info.get("stem") or f"第 {q_num} 問"
        options = ex_item.get("options") or raw_info.get("options") or [f"選択肢 {i}" for i in range(1, 5)]
        passage = ex_item.get("passage") if "passage" in ex_item else raw_info.get("passage")
        ans_val = exp_info.get("ans", 1)
        raw_kaisetsu = exp_info.get("raw_kaisetsu", "")

        why_correct = ex_item.get("why_correct") or (raw_kaisetsu if raw_kaisetsu else "")
        options_analysis = ex_item.get("options_analysis") or ["" for _ in range(len(options))]
        points = ex_item.get("points") or []

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
        raw_kaisetsu = exp_info.get("raw_kaisetsu", "")

        why_correct = ex_item.get("why_correct") or (raw_kaisetsu if raw_kaisetsu else "")
        options_analysis = ex_item.get("options_analysis") or ["" for _ in range(len(options))]
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", help="Path to tests/<test_id>")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing 詳細解説.json")
    ap.add_argument("--lean", action="store_true", help="Exclude duplicate stem/options/passage/script (build_model_answer will pull from source markdown)")
    ap.add_argument("--stdout", action="store_true", help="Print JSON to stdout without writing file")
    args = ap.parse_args()

    test_dir = Path(args.test_dir)
    if not test_dir.is_dir():
        print(f"Error: Directory not found: {test_dir}", file=sys.stderr)
        sys.exit(1)

    dest_file = test_dir / "詳細解説.json"
    if dest_file.exists() and not args.overwrite and not args.stdout:
        print(f"File already exists: {dest_file}. Merging while preserving existing explanations...")

    data = scaffold_test(test_dir, lean=args.lean, merge_existing=not args.overwrite)

    if args.stdout:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    dest_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Scaffolded {len(data)} items into {dest_file}")


if __name__ == "__main__":
    main()
