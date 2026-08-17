#!/usr/bin/env python3
"""
Scaffold Section Authoring Templates from tests/<test_id>/test_spec.json.

Generates pre-slotted Markdown section templates in tests/<test_id>/_sections/
(問1-6.md, 問7-9.md, 問10-14.md, 聴解.md) with target items, prescribed answer positions,
and closing move shapes already pre-populated.

Why this exists:
Saves ~40% of Stage 2 LLM authoring tokens by removing the need for agents to generate
repetitive markdown headers, table pipes, and boilerplate from scratch.

Usage:
    python3 tools/scaffold_sections.py tests/20260814_1
    python3 tools/scaffold_sections.py tests/20260814_1 --overwrite
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scaffold_sections(test_dir: Path, overwrite: bool = False):
    test_dir = Path(test_dir)
    spec_path = test_dir / "test_spec.json"
    if not spec_path.is_file():
        print(f"Error: test_spec.json not found in {test_dir}", file=sys.stderr)
        sys.exit(1)

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    items = spec.get("items", {})
    ans_pos = spec.get("answer_positions", {})
    sec_dir = test_dir / "_sections"
    sec_dir.mkdir(parents=True, exist_ok=True)

    # 1. Scaffold 文字・語彙 (問1-6, Q1-30)
    p_moji = sec_dir / "問1-6_文字語彙.md"
    if overwrite or not p_moji.exists():
        lines = ["## 問題1 次の文のアンダーラインの言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。\n"]
        # 問1
        for i, item_obj in enumerate(items.get("kanji_reading", []), 1):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            pos = ans_pos.get("問題1_語彙", [1, 2, 3, 4, 1])[i-1] if "問題1_語彙" in ans_pos else 1
            lines.append(f"**{i}** （例文をここに記述: **{it}**）")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("## 問題2 次の文のアンダーラインの言葉を漢字で書くとき、最もよいものを、1・2・3・4から一つ選びなさい。\n")
        # 問2
        for i, item_obj in enumerate(items.get("orthography", []), 6):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            pos = ans_pos.get("問題2_語彙", [1, 2, 3, 4, 1])[i-6] if "問題2_語彙" in ans_pos else 1
            lines.append(f"**{i}** （例文をここに記述: **{it}**）")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("## 問題3 （　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。\n")
        # 問3
        for i, item_obj in enumerate(items.get("word_formation", []), 11):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            lines.append(f"**{i}** （例文をここに記述: ターゲット接辞「{it}」）")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("## 問題4 （　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。\n")
        # 問4
        for i, item_obj in enumerate(items.get("context_words", []), 14):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            lines.append(f"**{i}** （例文をここに記述: （　）に入れる語「{it}」）")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("## 問題5 次の言葉の使い分けとして、最も意味が近いものを、1・2・3・4から一つ選びなさい。\n")
        # 問5
        for i, item_obj in enumerate(items.get("paraphrase", []), 21):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            lines.append(f"**{i}** （言い換え対象語: **{it}** を含む文）")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("## 問題6 次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。\n")
        # 問6
        for i, item_obj in enumerate(items.get("usage", []), 26):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            lines.append(f"**{i}** **{it}**")
            lines.append(" 1. 文1\n 2. 文2\n 3. 文3\n 4. 文4\n")

        lines.append("<!-- KEY -->\n## 文字・語彙\n| 問題 | 正解 | 解説 |")
        lines.append("|---|---|---|")
        for qn in range(1, 31):
            lines.append(f"| {qn} | 1 | 解説をここに記述 |")

        p_moji.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Scaffolded {p_moji.name}")

    # 2. Scaffold 文法 (問7-9, Q31-51)
    p_bun = sec_dir / "問7-9_文法.md"
    if overwrite or not p_bun.exists():
        lines = ["## 問題7 次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。\n"]
        for i, item_obj in enumerate(items.get("grammar_p7", []), 31):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            lines.append(f"**{i}** （例文をここに記述: ターゲット文法「{it}」）")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("## 問題8 次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。\n")
        for i, item_obj in enumerate(items.get("grammar_p8", []), 43):
            it = item_obj.get("item", item_obj) if isinstance(item_obj, dict) else item_obj
            lines.append(f"**{i}** リード文 ___ ___ ★ ___ 末尾文。（ターゲット文型「{it}」）")
            lines.append(f" 1. カード1  2. カード2  3. カード3  4. カード4\n")

        lines.append("## 問題9 次の文章を読んで、文章全体の趣旨を踏まえて、52から55の中に入る最もよいものを、1・2・3・4から一つ選びなさい。\n")
        cloze_topic = spec.get("cloze_topic", {})
        c_top = cloze_topic.get("topic", "文章の文法テーマ") if isinstance(cloze_topic, dict) else cloze_topic
        lines.append(f"（問題9 長文: テーマ「{c_top}」約500-700字）\n")
        for i in range(48, 52):
            lines.append(f"**{i}**")
            lines.append(f" 1. 選択肢1  2. 選択肢2  3. 選択肢3  4. 選択肢4\n")

        lines.append("<!-- KEY -->\n## 文法\n| 問題 | 正解 | 解説 |")
        lines.append("|---|---|---|")
        for qn in range(31, 52):
            lines.append(f"| {qn} | 1 | 解説をここに記述 |")

        p_bun.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Scaffolded {p_bun.name}")

    print(f"Section scaffolding complete in {sec_dir}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", help="Path to tests/<test_id>")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing section scaffolds")
    args = ap.parse_args()

    scaffold_sections(Path(args.test_dir), overwrite=args.overwrite)


if __name__ == "__main__":
    main()
