#!/usr/bin/env python3
"""
JLPT Mock Exam Grading & Diagnostic Script.

Grades user responses against official answer keys in tests/<test_id>/,
calculates standardized scaled scores (0-180), evaluates Pass/Fail criteria,
identifies weak sub-sections, and writes the structured result document
tests/<test_id>/採点結果.json.

Usage:
    # 1. Build the merged answer sheet (once per test, or `make sheet 1`):
    python3 .agents/exam-app/scripts/build_interactive.py tests/1

    # 2. Answer it in a browser (`make serve`, pick the test), press 「採点する」 —
    #    that already writes 採点結果.json and ユーザー解答.json. To re-grade from the CLI:
    python3 .agents/exam-app/scripts/grade_answers.py --test-dir tests/1 --user-answers tests/1/ユーザー解答.json

    # 3. Quick grade via CLI strings:
    python3 .agents/exam-app/scripts/grade_answers.py --test-dir tests/1 --answers-gengo "1:4,2:2,3:1..." --answers-choukai "問1-1:2,問1-2:3..."
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Sub-question mapping definitions for JLPT N2.
# AUTHORITY: these ranges MUST match .agents/jlpt-exam-structure/SKILL.md, which is
# the single owner of format facts. They previously did not (問1 was 1-8, 問11 was
# 60-64, 問14 was 71-75), so every 大問別 diagnostic attributed questions to the
# wrong 大問. Do not edit these without editing jlpt-exam-structure first.
GENGO_QUESTION_TAXONOMY = {
    # 言語知識（文字・語彙）
    "問1": {"name": "漢字読み (Kanji Reading)", "range": (1, 5), "section": "言語知識", "total": 5},
    "問2": {"name": "表記 (Orthography)", "range": (6, 10), "section": "言語知識", "total": 5},
    "問3": {"name": "語形成 (Word Formation)", "range": (11, 13), "section": "言語知識", "total": 3},
    "問4": {"name": "文脈規定 (Word in Context)", "range": (14, 20), "section": "言語知識", "total": 7},
    "問5": {"name": "言い換え類義 (Paraphrases)", "range": (21, 25), "section": "言語知識", "total": 5},
    "問6": {"name": "用法 (Correct Usage)", "range": (26, 30), "section": "言語知識", "total": 5},
    # 言語知識（文法）
    "問7": {"name": "文法形式の判断 (Grammar Form)", "range": (31, 42), "section": "言語知識", "total": 12},
    "問8": {"name": "文の組み立て (Sentence Composition ★)", "range": (43, 47), "section": "言語知識", "total": 5},
    "問9": {"name": "文章の文法 (Text Grammar / Cloze)", "range": (48, 51), "section": "言語知識", "total": 4},
    # 読解
    "問10": {"name": "内容理解・短文 (Short Passages)", "range": (52, 56), "section": "読解", "total": 5},
    "問11": {"name": "内容理解・中文 (Medium Passages)", "range": (57, 64), "section": "読解", "total": 8},
    "問12": {"name": "統合理解 (A/B Comparative Texts)", "range": (65, 66), "section": "読解", "total": 2},
    "問13": {"name": "主張理解・長文 (Long Essay)", "range": (67, 69), "section": "読解", "total": 3},
    "問14": {"name": "情報検索 (Information Retrieval)", "range": (70, 71), "section": "読解", "total": 2},
}

# Guard: the taxonomy must tile 1..71 exactly, with no gap and no overlap.
_covered = [q for s in GENGO_QUESTION_TAXONOMY.values()
            for q in range(s["range"][0], s["range"][1] + 1)]
assert sorted(_covered) == list(range(1, 72)), (
    "GENGO_QUESTION_TAXONOMY must tile questions 1-71 exactly "
    f"(got {len(_covered)} entries, duplicates/gaps present)")
assert all(s["total"] == s["range"][1] - s["range"][0] + 1
           for s in GENGO_QUESTION_TAXONOMY.values()), \
    "GENGO_QUESTION_TAXONOMY 'total' disagrees with its 'range'"

CHOUKAI_QUESTION_TAXONOMY = {
    "問題1": {"name": "課題理解 (Task Comprehension)", "section": "聴解"},
    "問題2": {"name": "ポイント理解 (Point Comprehension)", "section": "聴解"},
    "問題3": {"name": "概要理解 (Summary Comprehension)", "section": "聴解"},
    "問題4": {"name": "即時応答 (Quick Response)", "section": "聴解"},
    "問題5": {"name": "統合理解 (Integrated Comprehension)", "section": "聴解"},
}


# Weak-area study advice, keyed by 大問 group. Module level so that
# build_interactive.py (exam-app) can serialize the SAME strings into the in-page
# grader — one source of truth, no drift between the two implementations.
ADVICE = [
    (["問1", "問2", "問3"],
     "『新完全マスター単語N2』『新完全マスター漢字N2』の基本語彙・訓読み・複合語の復習を徹底しましょう。"),
    (["問4", "問5", "問6"],
     "語彙の文脈的意味やコロケーション（類義語・用法）の精度を高めましょう。単語カードでの例文暗記が効果的です。"),
    (["問7", "問8", "問9"],
     "『新完全マスター文法N2』で機能語の接続・意味の違いおよび文章全体の論理展開（接続詞・指示語）を復習しましょう。"),
    (["問10", "問11", "問12", "問13", "問14"],
     "『新完全マスター読解N2』を活用し、設問のキーワードのスキャニングおよび段落ごとの要旨把握のスキマ時間を増やしましょう。"),
    (["問題1", "問題2", "問題3", "問題4", "問題5"],
     "『新完全マスター聴解N2』CD音源によるシャドーイングおよび即時応答（問題4）の定型表現・敬語表現の反復練習を行いましょう。"),
]
ADVICE_FOR = {code: text for codes, text in ADVICE for code in codes}


def parse_gengo_keys(gengo_md_path: Path) -> dict:
    """Extract correct answers for Language Knowledge & Reading (Questions 1 to 71)."""
    if not gengo_md_path.is_file():
        raise FileNotFoundError(f"File not found: {gengo_md_path}")

    text = gengo_md_path.read_text(encoding="utf-8")
    answers = {}

    for line in text.splitlines():
        line_str = line.strip()
        if line_str.startswith("|") and line_str.endswith("|"):
            cells = [c.strip() for c in line_str.split("|")[1:-1]]
            # Iterate through cell pairs: (Q, Ans)
            for i in range(len(cells) - 1):
                q_clean = re.sub(r"[\*\s]", "", cells[i])
                a_clean = re.sub(r"[\*\s]", "", cells[i+1])
                if q_clean.isdigit() and a_clean.isdigit():
                    q_num = int(q_clean)
                    a_num = int(a_clean)
                    if 1 <= q_num <= 71 and 1 <= a_num <= 4:
                        answers[q_num] = a_num

    return answers


def parse_choukai_keys(choukai_md_path: Path) -> dict:
    """
    Extract correct answers for Listening (Choukai).
    Returns dict mapping item key (e.g. '問1-1', '問4-5', '問5-2-1') to correct answer option (1-4).
    """
    if not choukai_md_path.is_file():
        return {}

    text = choukai_md_path.read_text(encoding="utf-8")
    answers = {}

    # Find answer section after # 【正解・解説】 or # 解答・解説
    m = re.search(r"#+\s*【?正解[・\s]解説】?", text)
    ans_text = text[m.start():] if m else text

    current_mondai = None
    for line in ans_text.splitlines():
        line_str = line.strip()
        mondai_match = re.search(r"##\s*問題([1-5])", line_str)
        if mondai_match:
            current_mondai = int(mondai_match.group(1))
            continue

        if current_mondai and line_str.startswith("|"):
            # Table row parsing
            # Matches: | 1 | **2** | ... or | 1 | 2 | or | 3番-質問1 | 2 |
            cells = [c.strip() for c in line_str.split("|")[1:-1]]
            if len(cells) >= 2:
                q_label = re.sub(r"[\*\s]", "", cells[0])
                ans_str = re.sub(r"[\*\s]", "", cells[1])

                # Validate answer choice (1-4)
                if ans_str.isdigit() and 1 <= int(ans_str) <= 4:
                    ans_val = int(ans_str)
                    # Extract sub question label
                    if current_mondai in [1, 2, 3, 4]:
                        q_digit = re.search(r"(\d+)", q_label)
                        if q_digit:
                            answers[f"問{current_mondai}-{q_digit.group(1)}"] = ans_val
                    elif current_mondai == 5:
                        if re.search(r"質問1|2[-\s]*質問1|2番.*質問1", q_label):
                            answers["問5-2-1"] = ans_val
                        elif re.search(r"質問2|2[-\s]*質問2|2番.*質問2", q_label):
                            answers["問5-2-2"] = ans_val
                        elif re.search(r"^1$|^1番$|1番(?!.*質問)", q_label) or (
                                "1" in q_label and "質問" not in q_label and "2" not in q_label):
                            answers["問5-1"] = ans_val

    return answers


def grade(gengo_keys: dict, choukai_keys: dict, user_answers: dict) -> dict:
    """
    Grading engine.
    Calculates raw scores, scaled scores (0-60 for each section), Pass/Fail, and category stats.
    """
    user_gengo = user_answers.get("言語知識_読解", {})
    user_choukai = user_answers.get("聴解", {})

    # 1. Language Knowledge (Goi & Bunpou: Q1 - Q51)
    goi_bunpou_total = 51
    goi_bunpou_correct = 0
    gengo_detail = {}

    for q in range(1, 52):
        correct = gengo_keys.get(q)
        user_choice = user_gengo.get(str(q))
        if user_choice is not None:
            user_choice = int(user_choice)
        is_correct = (user_choice == correct) if correct is not None and user_choice is not None else False
        if is_correct:
            goi_bunpou_correct += 1
        gengo_detail[q] = {
            "correct": correct,
            "user": user_choice,
            "is_correct": is_correct
        }

    # 2. Reading (Dokkai: Q52 - Q71)
    dokkai_total = 20
    dokkai_correct = 0
    for q in range(52, 72):
        correct = gengo_keys.get(q)
        user_choice = user_gengo.get(str(q))
        if user_choice is not None:
            user_choice = int(user_choice)
        is_correct = (user_choice == correct) if correct is not None and user_choice is not None else False
        if is_correct:
            dokkai_correct += 1
        gengo_detail[q] = {
            "correct": correct,
            "user": user_choice,
            "is_correct": is_correct
        }

    # 3. Listening (Choukai)
    choukai_total = len(choukai_keys) if choukai_keys else 30
    choukai_correct = 0
    choukai_detail = {}

    for k, correct in choukai_keys.items():
        user_choice = user_choukai.get(k)
        if user_choice is not None:
            user_choice = int(user_choice)
        is_correct = (user_choice == correct) if user_choice is not None else False
        if is_correct:
            choukai_correct += 1
        choukai_detail[k] = {
            "correct": correct,
            "user": user_choice,
            "is_correct": is_correct
        }

    # Scaled Scores (JLPT Scale out of 60 per section)
    scaled_goi_bunpou = round((goi_bunpou_correct / goi_bunpou_total) * 60) if goi_bunpou_total > 0 else 0
    scaled_dokkai = round((dokkai_correct / dokkai_total) * 60) if dokkai_total > 0 else 0
    scaled_choukai = round((choukai_correct / choukai_total) * 60) if choukai_total > 0 else 0

    total_scaled_score = scaled_goi_bunpou + scaled_dokkai + scaled_choukai

    # Pass/Fail evaluation
    # Overall >= 90 AND Sectional Cutoffs >= 19 in each section
    cutoff_pass = (scaled_goi_bunpou >= 19) and (scaled_dokkai >= 19) and (scaled_choukai >= 19)
    overall_pass = total_scaled_score >= 90
    is_passed = overall_pass and cutoff_pass

    # Sub-category breakdown
    taxonomy_stats = {}
    for code, spec in GENGO_QUESTION_TAXONOMY.items():
        start, end = spec["range"]
        cat_correct = sum(1 for q in range(start, end + 1) if gengo_detail.get(q, {}).get("is_correct"))
        cat_total = (end - start + 1)
        taxonomy_stats[code] = {
            "name": spec["name"],
            "section": spec["section"],
            "correct": cat_correct,
            "total": cat_total,
            "percentage": round((cat_correct / cat_total) * 100, 1) if cat_total > 0 else 0
        }

    # Listening mondai breakdown
    choukai_mondai_stats = {f"問題{m}": {"correct": 0, "total": 0} for m in range(1, 6)}
    for k, item in choukai_detail.items():
        m = re.search(r"問([1-5])", k)
        if m:
            m_name = f"問題{m.group(1)}"
            choukai_mondai_stats[m_name]["total"] += 1
            if item["is_correct"]:
                choukai_mondai_stats[m_name]["correct"] += 1

    for m_name, stats in choukai_mondai_stats.items():
        tot = stats["total"]
        cor = stats["correct"]
        taxonomy_stats[m_name] = {
            "name": CHOUKAI_QUESTION_TAXONOMY.get(m_name, {}).get("name", m_name),
            "section": "聴解",
            "correct": cor,
            "total": tot,
            "percentage": round((cor / tot) * 100, 1) if tot > 0 else 0
        }

    return {
        "summary": {
            "passed": is_passed,
            "total_scaled_score": total_scaled_score,
            "max_scaled_score": 180,
            "cutoff_passed": cutoff_pass,
            "overall_threshold_passed": overall_pass,
            "sections": {
                "言語知識（文字・語彙・文法）": {
                    "raw_correct": goi_bunpou_correct,
                    "raw_total": goi_bunpou_total,
                    "scaled_score": scaled_goi_bunpou,
                    "cutoff": 19,
                    "passed_cutoff": scaled_goi_bunpou >= 19
                },
                "読解": {
                    "raw_correct": dokkai_correct,
                    "raw_total": dokkai_total,
                    "scaled_score": scaled_dokkai,
                    "cutoff": 19,
                    "passed_cutoff": scaled_dokkai >= 19
                },
                "聴解": {
                    "raw_correct": choukai_correct,
                    "raw_total": choukai_total,
                    "scaled_score": scaled_choukai,
                    "cutoff": 19,
                    "passed_cutoff": scaled_choukai >= 19
                }
            }
        },
        "taxonomy_stats": taxonomy_stats,
        "detail_gengo": gengo_detail,
        "detail_choukai": choukai_detail
    }


def result_payload(results: dict, test_id: str, graded_at: str | None = None) -> dict:
    """The 採点結果.json document.

    This is the ONLY report artifact — there is no Markdown report any more.
    The in-page grader in 解答.html builds the identical structure (the exam app
    saves it over POST /api/tests/<id>/submit), and `make check` compares the two
    documents field by field, so the shape here is a contract, not a preference.
    Entries with no items are dropped so a partially built test cannot show a
    大問 as 0% purely because it has no questions yet.
    """
    stats = {code: s for code, s in results["taxonomy_stats"].items() if s["total"]}
    weak = [{"code": code, "name": s["name"], "section": s["section"],
             "percentage": s["percentage"], "advice": ADVICE_FOR.get(code, "")}
            for code, s in stats.items() if s["percentage"] < 60]
    return {
        "test_id": test_id,
        "graded_at": graded_at or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": results["summary"],
        "taxonomy_stats": stats,
        "weak_areas": weak,
        "detail_gengo": {str(q): d for q, d in results["detail_gengo"].items()},
        "detail_choukai": results["detail_choukai"],
    }


def main():
    parser = argparse.ArgumentParser(description="Grade user responses for JLPT mock test.")
    parser.add_argument("--test-dir", required=True, help="Path to test output directory, e.g. tests/1")
    parser.add_argument("--user-answers",
                        help="Comma-separated user answer JSON file(s). "
                             "Default: ユーザー解答*.json in the test dir or cwd.")
    parser.add_argument("--answers-gengo", help="Quick gengo answers string like '1:4,2:2,3:1...'")
    parser.add_argument("--answers-choukai", help="Quick choukai answers string like '問1-1:2,問1-2:3...'")

    args = parser.parse_args()

    test_path = Path(args.test_dir)
    gengo_md = test_path / "言語知識・読解.md"
    choukai_md = test_path / "聴解.md"

    if not gengo_md.exists():
        print(f"Error: {gengo_md} not found.", file=sys.stderr)
        sys.exit(1)

    # 1. Parse correct answer keys
    gengo_keys = parse_gengo_keys(gengo_md)
    choukai_keys = parse_choukai_keys(choukai_md)

    print(f"Loaded answer keys for {test_path}:")
    print(f"  - 言語知識・読解: {len(gengo_keys)} questions parsed")
    print(f"  - 聴解: {len(choukai_keys)} questions parsed")

    # 2. Load user answers. Source of truth is the JSON saved by the merged
    #    answer sheet (解答.html), which covers both halves in one file. Several
    #    matching files still merge cleanly; CLI strings override.
    user_answers = {"言語知識_読解": {}, "聴解": {}}

    if args.user_answers:
        sources = [Path(x.strip()) for x in args.user_answers.split(",")]
    else:
        sources = sorted(test_path.glob("ユーザー解答*.json")) + \
                  sorted(Path.cwd().glob("ユーザー解答*.json"))

    for ua_path in sources:
        if not ua_path.exists():
            print(f"  warning: {ua_path} not found", file=sys.stderr)
            continue
        loaded = json.loads(ua_path.read_text(encoding="utf-8"))
        user_answers["言語知識_読解"].update(loaded.get("言語知識_読解", {}))
        user_answers["聴解"].update(loaded.get("聴解", {}))
        print(f"Loaded user answers from {ua_path}")
    if not sources:
        print("  no ユーザー解答*.json found — run `make serve`, pick this test "
              "from the list, answer, then press 「採点する」.", file=sys.stderr)

    if args.answers_gengo:
        pairs = args.answers_gengo.split(",")
        for pair in pairs:
            if ":" in pair:
                q, a = pair.strip().split(":")
                user_answers["言語知識_読解"][q.strip()] = int(a.strip())

    if args.answers_choukai:
        pairs = args.answers_choukai.split(",")
        for pair in pairs:
            if ":" in pair:
                q, a = pair.strip().split(":")
                user_answers["聴解"][q.strip()] = int(a.strip())

    # 3. Perform Grading
    results = grade(gengo_keys, choukai_keys, user_answers)

    # 4. Save the structured result document
    payload = result_payload(results, test_path.name)
    out_json = test_path / "採点結果.json"
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # 5. Print summary output to stdout
    summary = results["summary"]
    status_str = "PASSED (合格)" if summary["passed"] else "FAILED (不合格)"
    print(f"\n==========================================")
    print(f"       JLPT N2 GRADING RESULT ({test_path.name})")
    print(f"==========================================")
    print(f" Final Result    : {status_str}")
    print(f" Total Scaled    : {summary['total_scaled_score']} / 180 (Pass threshold: 90)")
    for sec_name, sec_data in summary["sections"].items():
        pass_cut = "OK" if sec_data["passed_cutoff"] else "FAIL (Cutoff < 19)"
        print(f"  - {sec_name:<16}: {sec_data['scaled_score']:2d}/60 (Raw: {sec_data['raw_correct']}/{sec_data['raw_total']}) [{pass_cut}]")
    if payload["weak_areas"]:
        print(" Weak areas (<60%): " +
              ", ".join(f"{w['code']} {w['percentage']}%" for w in payload["weak_areas"]))
    print(f"==========================================")
    print(f"Result document saved to: {out_json}\n")


if __name__ == "__main__":
    main()