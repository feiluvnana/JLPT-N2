#!/usr/bin/env python3
"""
Item Response Theory (IRT / 得点等化) Scaled Scoring Engine for JLPT N2.

Simulates official Japan Foundation scaled scores (0–60 per section, 0–180 total)
using 2-Parameter Logistic (2PL) IRT modeling with item discrimination (a)
and item difficulty (b) parameters calibrated to JLPT question types.

Usage:
    python3 tools/irt_scorer.py tests/20260814_1 --simulate 0.8
    python3 tools/irt_scorer.py tests/20260814_1
    make irt 20260814_1
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Calibrated IRT parameters by JLPT N2 Question Type (a = discrimination, b = difficulty)
# Higher 'a' means stronger ability discrimination; 'b' is ability theta centered at 0.0
SECTION_ITEM_PARAMS = {
    # 言語知識（文字・語彙）
    "問1": {"name": "漢字読み", "a": 1.2, "b": -0.4, "section": "言語知識"},
    "問2": {"name": "表記", "a": 1.1, "b": -0.3, "section": "言語知識"},
    "問3": {"name": "語形成", "a": 1.3, "b": 0.0, "section": "言語知識"},
    "問4": {"name": "文脈規定", "a": 1.4, "b": 0.2, "section": "言語知識"},
    "問5": {"name": "言い換え類義", "a": 1.3, "b": 0.1, "section": "言語知識"},
    "問6": {"name": "用法", "a": 1.6, "b": 0.5, "section": "言語知識"},
    # 言語知識（文法）
    "問7": {"name": "文法形式の判断", "a": 1.4, "b": 0.1, "section": "言語知識"},
    "問8": {"name": "文の組み立て（★）", "a": 1.7, "b": 0.6, "section": "言語知識"},
    "問9": {"name": "文章の文法", "a": 1.5, "b": 0.4, "section": "言語知識"},
    # 読解
    "問10": {"name": "内容理解（短文）", "a": 1.3, "b": 0.0, "section": "読解"},
    "問11": {"name": "内容理解（中文）", "a": 1.5, "b": 0.3, "section": "読解"},
    "問12": {"name": "統合理解", "a": 1.7, "b": 0.7, "section": "読解"},
    "問13": {"name": "主張理解（長文）", "a": 1.8, "b": 0.8, "section": "読解"},
    "問14": {"name": "情報検索", "a": 1.4, "b": 0.2, "section": "読解"},
    # 聴解
    "問題1": {"name": "課題理解", "a": 1.3, "b": -0.1, "section": "聴解"},
    "問題2": {"name": "ポイント理解", "a": 1.4, "b": 0.2, "section": "聴解"},
    "問題3": {"name": "概要理解", "a": 1.6, "b": 0.5, "section": "聴解"},
    "問題4": {"name": "即時応答", "a": 1.2, "b": 0.0, "section": "聴解"},
    "問題5": {"name": "統合理解", "a": 1.9, "b": 0.9, "section": "聴解"},
}

GENGO_RANGES = [
    ("問1", 1, 5), ("問2", 6, 10), ("問3", 11, 13), ("問4", 14, 20),
    ("問5", 21, 25), ("問6", 26, 30), ("問7", 31, 42), ("問8", 43, 47),
    ("問9", 48, 51), ("問10", 52, 56), ("問11", 57, 64), ("問12", 65, 66),
    ("問13", 67, 69), ("問14", 70, 71),
]


def logistic_prob(theta: float, a: float, b: float) -> float:
    """2PL probability of correct response given ability theta."""
    val = -a * (theta - b)
    if val > 30:
        return 0.0
    if val < -30:
        return 1.0
    return 1.0 / (1.0 + math.exp(val))


def estimate_theta(responses: list[tuple[float, float, bool]], max_iter: int = 25) -> float:
    """Maximum Likelihood / Newton-Raphson estimation of ability parameter theta."""
    if not responses:
        return 0.0

    n_correct = sum(1 for _, _, corr in responses if corr)
    n_total = len(responses)

    # Edge cases
    if n_correct == 0:
        return -3.0
    if n_correct == n_total:
        return 3.0

    p = n_correct / n_total
    theta = math.log(p / (1.0 - p))

    for _ in range(max_iter):
        score = 0.0
        info = 0.0
        for a, b, corr in responses:
            prob = logistic_prob(theta, a, b)
            u = 1.0 if corr else 0.0
            score += a * (u - prob)
            info += (a ** 2) * prob * (1.0 - prob)

        if info < 1e-6:
            break
        delta = score / info
        theta += delta
        if abs(delta) < 1e-4:
            break

    return max(-3.0, min(3.0, theta))


def theta_to_scaled_score(theta: float, min_score: int = 0, max_score: int = 60) -> int:
    """Convert ability theta (-3.0 to +3.0) to official section scaled score (0..60)."""
    norm = (theta + 3.0) / 6.0  # [0.0, 1.0]
    scaled = round(norm * (max_score - min_score) + min_score)
    return max(min_score, min(max_score, scaled))


def run_irt_grading(test_dir: Path, simulate_accuracy: float | None = None):
    test_dir = Path(test_dir)
    result_json_path = test_dir / "採点結果.json"

    detail_g = {}
    detail_c = {}

    if simulate_accuracy is not None:
        # Simulate responses with target accuracy
        print(f"Simulating test session with {simulate_accuracy*100:.0f}% accuracy...")
        for qn in range(1, 72):
            detail_g[str(qn)] = {"is_correct": (qn % 10) < (simulate_accuracy * 10)}
        for qn in range(1, 31):
            detail_c[f"問1-{qn}"] = {"is_correct": (qn % 10) < (simulate_accuracy * 10)}
    elif result_json_path.is_file():
        res = json.loads(result_json_path.read_text(encoding="utf-8"))
        detail_g = res.get("detail_gengo", {})
        detail_c = res.get("detail_choukai", {})
    else:
        print(f"Note: 採点結果.json not found in {test_dir}. Running baseline simulation (75% correct)...")
        return run_irt_grading(test_dir, simulate_accuracy=0.75)

    # 1. Collect responses for 言語知識 (問1-9, Q1-51)
    g_responses = []
    for code, start, end in GENGO_RANGES[:9]:
        params = SECTION_ITEM_PARAMS[code]
        for qn in range(start, end + 1):
            is_corr = detail_g.get(str(qn), {}).get("is_correct", True)
            g_responses.append((params["a"], params["b"], is_corr))

    # 2. Collect responses for 読解 (問10-14, Q52-71)
    d_responses = []
    for code, start, end in GENGO_RANGES[9:]:
        params = SECTION_ITEM_PARAMS[code]
        for qn in range(start, end + 1):
            is_corr = detail_g.get(str(qn), {}).get("is_correct", True)
            d_responses.append((params["a"], params["b"], is_corr))

    # 3. Collect responses for 聴解
    c_responses = []
    for key_id, item_detail in detail_c.items():
        m = re.search(r"問([1-5])", key_id)
        m_name = f"問題{m.group(1)}" if m else "問題1"
        params = SECTION_ITEM_PARAMS.get(m_name, {"a": 1.4, "b": 0.0})
        is_corr = item_detail.get("is_correct", True)
        c_responses.append((params["a"], params["b"], is_corr))

    theta_g = estimate_theta(g_responses)
    theta_d = estimate_theta(d_responses)
    theta_c = estimate_theta(c_responses)

    irt_scaled_g = theta_to_scaled_score(theta_g)
    irt_scaled_d = theta_to_scaled_score(theta_d)
    irt_scaled_c = theta_to_scaled_score(theta_c)
    irt_total = irt_scaled_g + irt_scaled_d + irt_scaled_c

    passed = (irt_total >= 90) and (irt_scaled_g >= 19) and (irt_scaled_d >= 19) and (irt_scaled_c >= 19)

    print(f"\n=======================================================")
    print(f"  JLPT N2 Item Response Theory (IRT) Scaled Scoring   ")
    print(f"  Test ID: {test_dir.name}")
    print(f"=======================================================")
    print(f"  Section 1: 言語知識 (文字・語彙・文法) : {irt_scaled_g:2d}/60 (Ability θ: {theta_g:+.2f})")
    print(f"  Section 2: 読解 (Reading Comprehension): {irt_scaled_d:2d}/60 (Ability θ: {theta_d:+.2f})")
    print(f"  Section 3: 聴解 (Listening)            : {irt_scaled_c:2d}/60 (Ability θ: {theta_c:+.2f})")
    print(f"-------------------------------------------------------")
    print(f"  TOTAL SCALED SCORE (尺度得点)          : {irt_total:2d}/180")
    print(f"  PASS / FAIL EVALUATION                 : {'🎉 PASS (合格)' if passed else '❌ FAIL (不合格)'}")
    print(f"  (Criteria: Total >= 90/180 and Sectional Scores >= 19/60 each)")
    print(f"=======================================================\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", help="Path to tests/<test_id>")
    ap.add_argument("--simulate", type=float, help="Simulate accuracy ratio (0.0 to 1.0)")
    args = ap.parse_args()
    run_irt_grading(Path(args.test_dir), simulate_accuracy=args.simulate)


if __name__ == "__main__":
    main()
