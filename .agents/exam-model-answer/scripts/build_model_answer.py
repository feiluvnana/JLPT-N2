#!/usr/bin/env python3
"""
Generate the official Model Answer & In-Depth Explanation deliverable (模範解答.html)
for a JLPT mock exam.

Usage:
    python3 .agents/exam-model-answer/scripts/build_model_answer.py tests/20260807_1
    make model-answer 20260807_1

Outputs:
    tests/<test_id>/模範解答.html
"""

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# Sub-question taxonomy matching JLPT N2 specifications
GENGO_TAXONOMY = {
    "問1": {"mondai": "問題1", "name": "漢字読み", "en": "Kanji Reading", "range": (1, 5), "section": "文字・語彙"},
    "問2": {"mondai": "問題2", "name": "表記", "en": "Orthography", "range": (6, 10), "section": "文字・語彙"},
    "問3": {"mondai": "問題3", "name": "語形成", "en": "Word Formation", "range": (11, 13), "section": "文字・語彙"},
    "問4": {"mondai": "問題4", "name": "文脈規定", "en": "Contextual Use", "range": (14, 20), "section": "文字・語彙"},
    "問5": {"mondai": "問題5", "name": "言い換え類義", "en": "Paraphrases", "range": (21, 25), "section": "文字・語彙"},
    "問6": {"mondai": "問題6", "name": "用法", "en": "Usage in Context", "range": (26, 30), "section": "文字・語彙"},
    "問7": {"mondai": "問題7", "name": "文法形式の判断", "en": "Grammar Form", "range": (31, 42), "section": "文法"},
    "問8": {"mondai": "問題8", "name": "文の組み立て（★）", "en": "Sentence Composition", "range": (43, 47), "section": "文法"},
    "問9": {"mondai": "問題9", "name": "文章の文法", "en": "Text Grammar / Cloze", "range": (48, 51), "section": "文法"},
    "問10": {"mondai": "問題10", "name": "内容理解（短文）", "en": "Short Passages", "range": (52, 56), "section": "読解"},
    "問11": {"mondai": "問題11", "name": "内容理解（中文）", "en": "Medium Passages", "range": (57, 64), "section": "読解"},
    "問12": {"mondai": "問題12", "name": "統合理解", "en": "Comparative Reading (A/B)", "range": (65, 66), "section": "読解"},
    "問13": {"mondai": "問題13", "name": "主張理解（長文）", "en": "Long Essay / Thematic", "range": (67, 69), "section": "読解"},
    "問14": {"mondai": "問題14", "name": "情報検索", "en": "Information Retrieval", "range": (70, 71), "section": "読解"},
}

CHOUKAI_TAXONOMY = {
    "問題1": {"name": "課題理解", "en": "Task Comprehension", "section": "聴解"},
    "問題2": {"name": "ポイント理解", "en": "Point Comprehension", "section": "聴解"},
    "問題3": {"name": "概要理解", "en": "Summary Comprehension", "section": "聴解"},
    "問題4": {"name": "即時応答", "en": "Quick Response", "section": "聴解"},
    "問題5": {"name": "統合理解", "en": "Integrated Comprehension", "section": "聴解"},
}

# Every label the page prints outside the exam's own wording. The Japanese
# values here are the page's baseline AND the fallback for a language whose
# ui/<lang>.json omits a key; .agents/exam-answer-translation/ui/_template.json
# is a copy of this dict and make check asserts the two never drift apart.
JA_UI = {
    "title": "日本語能力試験 N2 模範解答・詳細解説",
    "subtitle": "全101問（言語知識・読解 71問 ＋ 聴解 30問）完全網羅解説集",
    "test_label": "テスト",
    "back_link": "← 採点結果へ戻る",
    "badge": "JLPT N2 MODEL ANSWER & EXPLANATION",
    "search_placeholder": "問題番号・キーワード検索...",
    "tab_all": "すべて",
    "tab_goi": "文字・語彙",
    "tab_bunpou": "文法",
    "tab_dokkai": "読解",
    "tab_choukai": "聴解",
    "question_label": "第 {n} 問",
    "answer_label": "正解",
    "passage_title": "本文 / 資料",
    "passage_trans_title": "本文の訳",
    "script_title": "音声スクリプト",
    "script_trans_title": "スクリプトの訳",
    "exp_heading": "詳細解説",
    "why_title": "【正解の理由・根拠】",
    "why_title_choukai": "【正解の理由・聞き取りポイント】",
    "options_title": "【各選択肢の解説】",
    "points_title": "【重要語彙・文法ポイント】",
    "points_title_choukai": "【重要表現・リスニングポイント】",
    "tag_correct": "[正解]",
    "tag_wrong": "[不正解]",
    "audio_label": "聴解音声",
    "audio_ready": "準備完了",
    "audio_playing": "再生中",
    "audio_jump": "音声再生",
}


def load_languages(test_dir: Path, detailed_data: dict) -> list:
    """[Japanese, *translations] — one entry per language the page will carry.

    Translations are discovered by glob (詳細解説.<lang>.json), never by a list
    of languages held here: which languages a paper ships with is declared in
    GENERATE.md, and this builder must not need editing to add one. A file
    whose _meta.lang disagrees with its filename is skipped rather than
    rendered under the wrong flag. See .agents/exam-answer-translation.
    """
    langs = [{"code": "ja", "html_lang": "ja", "label": "日本語",
              "ui": dict(JA_UI), "data": detailed_data}]
    for path in sorted(test_dir.glob("詳細解説.*.json")):
        code = path.name[len("詳細解説."):-len(".json")]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  ! skipped {path.name}: does not parse ({exc})")
            continue
        meta = data.pop("_meta", {}) or {}
        if meta.get("lang") and meta["lang"] != code:
            print(f"  ! skipped {path.name}: _meta.lang is {meta['lang']!r}, filename says {code!r}")
            continue
        ui = dict(JA_UI)
        ui.update(meta.get("ui") or {})
        langs.append({"code": code, "html_lang": meta.get("html_lang") or code,
                      "label": meta.get("label") or code, "ui": ui, "data": data})
    return langs


def apply_furigana_bold(text: str) -> str:
    """Convert Japanese furigana notation into HTML <ruby> tags and format markdown bold.
    No newline handling -- callers that may receive multi-line text pick their own
    line-break treatment (apply_furigana() for short fields, format_passage_text()
    for passages, which also has to tell paragraph breaks from table rows)."""
    if not text:
        return ""
    # 1. Convert markdown bold **word** -> <strong>word</strong>
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # 2. ｜漢字《かんじ》
    text = re.sub(r"｜([^《]+)《([^》]+)》", r"<ruby>\1<rt>\2</rt></ruby>", text)
    # 3. 漢字《かんじ》
    text = re.sub(r"([一-龥々]+)《([^》]+)》", r"<ruby>\1<rt>\2</rt></ruby>", text)
    return text


def apply_furigana(text: str) -> str:
    """apply_furigana_bold() plus literal newline -> <br>. For short fields that can
    legitimately span more than one line -- e.g. two-turn dialogue stems
    ('A「…」\\nB「…」') -- without which the turns run together on one line."""
    if not text:
        return ""
    return apply_furigana_bold(text).replace("\n", "<br>")


_TABLE_SEP_CELL = re.compile(r"^:?-{1,}:?$")


def _is_md_table_block(lines: list) -> bool:
    if len(lines) < 2:
        return False
    if not all(l.startswith("|") and l.endswith("|") for l in lines):
        return False
    sep_cells = [c.strip() for c in lines[1].strip("|").split("|")]
    return all(_TABLE_SEP_CELL.match(c) for c in sep_cells)


def _render_md_table(lines: list) -> str:
    rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines]
    header, _sep, *body = rows
    thead = "<tr>" + "".join(f"<th>{c}</th>" for c in header) + "</tr>"
    tbody = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body)
    return f"<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>"


def format_passage_text(text: str) -> str:
    """本文/資料 (reading passage) text -> HTML.

    詳細解説.json passages are hand-authored straight from 言語知識・読解.md and
    keep that source's blank-line paragraphs, single-\\n line continuations
    (business memos, addressed notices), and occasional markdown pipe tables
    (案内/お知らせ items) -- none of which apply_furigana() ever converted, so
    a passage rendered as one run-on paragraph, and a table rendered as raw
    `| pipe | text |`. This mirrors build_booklet.py's nl2br treatment of the
    same official wording and renders real tables into <table> (the CSS for
    .passage-box table already assumed one would exist).

    Skips straight to apply_furigana_bold() for passages some earlier pass
    already hand-patched with literal <br> tags (no bare \\n left) -- reprocessing
    those would misread a leading '### label' as an unterminated heading line
    spanning the whole passage.
    """
    if not text:
        return ""
    if "<br>" in text:
        return apply_furigana_bold(text)
    blocks = re.split(r"\n\s*\n", text.strip())
    rendered = []
    for block in blocks:
        lines = block.strip().splitlines()
        if _is_md_table_block(lines):
            rendered.append(_render_md_table(lines))
        else:
            rendered.append(block.replace("\n", "<br>"))
    return apply_furigana_bold("<br><br>".join(rendered))


def clean_option_analysis_text(text: str) -> str:
    """Strip redundant prefixes like '1. 不正解: ', '[不正解]', '正解: ', '誤り: ' to prevent repeated labels."""
    if not text:
        return ""
    # Remove leading number index like '1. ' or '2. '
    text = re.sub(r"^\s*\d+[\.、\s]\s*", "", text.strip())
    # Remove redundant tags like ○, ✗, [正解], [不正解], 誤用:, 正解:, 不正解:, 誤り:
    text = re.sub(r"^[○✗\s]*", "", text)
    text = re.sub(r"^(?:\[?(?:正解|不正解|誤用|誤り)\]?[:：\s]*|\(?(?:正解|不正解|誤用|誤り)\)?[:：\s]*)+", "", text)
    return text.strip()


def parse_gengo_markdown(gengo_md_text: str):
    """
    Parse questions, options, passages, and explanation table from 言語知識・読解.md.
    Supports 3-column (| 問 | 答 | 解説 |), 4-column, and 5-column (| 問題 | 番号 | 正解 | 出題語 | 解説 |) tables.
    """
    key_split = re.split(r"^#+\s*(?:解答|【?正解)", gengo_md_text, flags=re.M)
    exam_body = key_split[0]
    key_body = key_split[1] if len(key_split) > 1 else ""

    # Parse explanation table
    explanations = {}
    for line in key_body.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) < 2:
                continue
            # Skip separator rows like |---|---|
            if all(re.match(r"^:?-+:?$", c) for c in cells):
                continue

            # Look for adjacent (q_num, ans_val) cell pair
            for i in range(len(cells) - 1):
                q_clean = re.sub(r"[\*\s]", "", cells[i])
                a_clean = re.sub(r"[\*\s]", "", cells[i+1])
                if q_clean.isdigit() and a_clean.isdigit():
                    q_num = int(q_clean)
                    a_num = int(a_clean)
                    if 1 <= q_num <= 75 and 1 <= a_num <= 4:
                        kaisetsu = cells[-1] if len(cells) > (i + 1) else ""
                        if kaisetsu == cells[i] or kaisetsu == cells[i+1]:
                            kaisetsu = ""
                        explanations[q_num] = {
                            "ans": a_num,
                            "raw_kaisetsu": kaisetsu
                        }
                        break

    return exam_body, explanations


def parse_choukai_markdown(choukai_md_text: str):
    """
    Parse questions and explanations from 聴解.md.
    """
    key_split = re.split(r"^#+\s*【?正解[・\s]解説】?", choukai_md_text, flags=re.M)
    exam_body = key_split[0]
    key_body = key_split[1] if len(key_split) > 1 else ""

    explanations = {}
    current_mondai = None
    for line in key_body.splitlines():
        line = line.strip()
        m_mondai = re.search(r"##\s*問題([1-5])", line)
        if m_mondai:
            current_mondai = int(m_mondai.group(1))
            continue
        if current_mondai and line.startswith("|") and line.endswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 2:
                q_label = parts[0].replace("*", "").strip()
                ans_str = re.sub(r"[^\d]", "", parts[1])
                if q_label in ("例", "番号", "問", "項目"):
                    continue
                if ans_str.isdigit():
                    ans_val = int(ans_str)
                    kaisetsu = parts[2] if len(parts) >= 3 else ""
                    key_id = None
                    if current_mondai in (1, 2, 3, 4):
                        m_digit = re.search(r"(\d+)", q_label)
                        if m_digit:
                            key_id = f"問{current_mondai}-{m_digit.group(1)}"
                    elif current_mondai == 5:
                        if "質問1" in q_label:
                            key_id = "問5-3-1" if ("3" in q_label or "3番" in q_label) else "問5-2-1"
                        elif "質問2" in q_label:
                            key_id = "問5-3-2" if ("3" in q_label or "3番" in q_label) else "問5-2-2"
                        elif re.search(r"^1$|^1番$|1番(?!.*質問)", q_label) or (
                                "1" in q_label and "質問" not in q_label and "2" not in q_label):
                            key_id = "問5-1"
                        elif re.search(r"^2$|^2番$|2番(?!.*質問)", q_label) or (
                                "2" in q_label and "質問" not in q_label and "3" not in q_label):
                            key_id = "問5-2"
                    if key_id:
                        explanations[key_id] = {
                            "ans": ans_val,
                            "raw_kaisetsu": kaisetsu
                        }

    return exam_body, explanations


def parse_choukai_scripts(script_text: str):
    """
    Parse 聴解スクリプト.txt into question-keyed script snippets.
    """
    blocks = {}
    current_key = None
    cur_lines = []

    for line in script_text.splitlines():
        line_str = line.strip()
        m_mondai = re.match(r"^問題([1-5])\s*。", line_str)
        m_item = re.match(r"^(\d{1,2})番\s*。", line_str)

        if m_mondai:
            if current_key and cur_lines:
                blocks[current_key] = "\n".join(cur_lines)
            current_mondai = int(m_mondai.group(1))
            current_key = f"問題{current_mondai}"
            cur_lines = [line_str]
        elif m_item:
            if current_key and cur_lines:
                blocks[current_key] = "\n".join(cur_lines)
            item_num = int(m_item.group(1))
            if 'current_mondai' in locals():
                current_key = f"問{current_mondai}-{item_num}"
            cur_lines = [line_str]
        else:
            cur_lines.append(line_str)

    if current_key and cur_lines:
        blocks[current_key] = "\n".join(cur_lines)

    return blocks


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja" data-lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>テスト {test_id}（模範解答・詳細解説）</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Noto+Serif+JP:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --primary: #1e3a8a;
  --primary-light: #2563eb;
  --accent-correct: #059669;
  --accent-correct-bg: #ecfdf5;
  --accent-correct-border: #a7f3d0;
  --accent-wrong: #dc2626;
  --accent-wrong-bg: #fef2f2;
  --bg-main: #f8fafc;
  --card-bg: #ffffff;
  --border-color: #e2e8f0;
  --text-main: #1e293b;
  --text-muted: #64748b;
  --font-sans: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-serif: 'Noto Serif JP', 'Yu Mincho', serif;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: var(--font-sans);
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.75;
  padding-bottom: 5rem;
}}

/* Furigana Ruby Styling */
ruby {{
  ruby-align: center;
  font-family: inherit;
}}
ruby rt {{
  font-size: 0.58em;
  font-weight: 400;
  color: var(--text-muted);
  user-select: none;
}}

/* Modern Top Header */
header.app-header {{
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #fff;
  padding: 1.5rem 1.25rem 1.6rem;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}}
.header-inner {{
  max-width: 1050px;
  margin: 0 auto;
}}
.header-top-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}}
.header-back-btn {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #cbd5e1;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 0.35rem 0.85rem;
  border-radius: 6px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  transition: all 0.15s ease;
}}
.header-back-btn:hover {{
  background: rgba(255,255,255,0.18);
  color: #ffffff;
  border-color: rgba(255,255,255,0.3);
}}
.header-badge {{
  display: inline-block;
  background: rgba(255,255,255,0.12);
  color: #93c5fd;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  letter-spacing: 0.04em;
}}
h1.title {{
  font-size: 1.7rem;
  font-weight: 900;
  margin-bottom: 0.35rem;
  color: #ffffff;
}}
.subtitle {{
  color: #94a3b8;
  font-size: 0.92rem;
}}

/* Sticky Sub-navigation Bar */
.sticky-nav {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 0.65rem 1rem;
}}
.nav-container {{
  max-width: 1050px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}}
.tab-group {{
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}}
.tab-btn {{
  border: none;
  background: var(--bg-main);
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.45rem 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}}
.tab-btn:hover {{
  background: #e2e8f0;
  color: var(--text-main);
}}
.tab-btn.active {{
  background: var(--primary);
  color: #ffffff;
}}

.search-box {{
  display: flex;
  align-items: center;
  min-width: 230px;
}}
.search-box input {{
  width: 100%;
  padding: 0.45rem 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.85rem;
  outline: none;
}}
.search-box input:focus {{
  border-color: var(--primary-light);
  box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}}

/* Main Content Container */
.main-container {{
  max-width: 1050px;
  margin: 1.2rem auto;
  padding: 0 1rem;
}}

/* Section Banner */
.section-banner {{
  margin: 2.2rem 0 1rem;
  padding: 0.75rem 1.1rem;
  background: #1e293b;
  color: #fff;
  border-radius: 8px;
  font-size: 1.15rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}
.section-banner small {{
  font-size: 0.82rem;
  color: #94a3b8;
  font-weight: 400;
}}

/* Question Card */
.q-card {{
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 1.6rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  overflow: hidden;
  transition: border-color 0.2s ease;
}}
.q-card:hover {{
  border-color: #cbd5e1;
}}

.q-header {{
  padding: 0.8rem 1.1rem;
  background: #f8fafc;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.8rem;
  flex-wrap: wrap;
}}
.q-meta {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.q-num-badge {{
  background: var(--primary);
  color: #fff;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}}
.q-type-badge {{
  background: #e2e8f0;
  color: #334155;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}}
.q-ans-badge {{
  background: var(--accent-correct);
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.2rem 0.7rem;
  border-radius: 9999px;
}}

.q-body {{
  padding: 1.1rem 1.25rem;
}}
.q-stem {{
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.85;
  margin-bottom: 0.9rem;
  color: #0f172a;
}}
.q-stem b, .q-stem strong {{
  font-weight: 700;
  color: #1e3a8a;
  background: #eff6ff;
  padding: 0.05em 0.25em;
  border-radius: 3px;
}}

/* Options Grid */
.options-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1.1rem;
}}
.opt-item {{
  padding: 0.55rem 0.8rem;
  border-radius: 6px;
  font-size: 0.92rem;
  border: 1px solid var(--border-color);
  background: #ffffff;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}}
.opt-item.is-correct {{
  background: var(--accent-correct-bg);
  border-color: var(--accent-correct-border);
  color: #065f46;
  font-weight: 700;
}}
.opt-num {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.35rem;
  height: 1.35rem;
  border-radius: 50%;
  background: #e2e8f0;
  color: #334155;
  font-size: 0.78rem;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 0.1rem;
}}
.opt-item.is-correct .opt-num {{
  background: var(--accent-correct);
  color: #fff;
}}

/* Passage Box (Dokkai) */
.passage-box {{
  background: #fdfdfd;
  border: 1px solid #cbd5e1;
  border-left: 4px solid #3b82f6;
  border-radius: 6px;
  padding: 1.15rem;
  margin-bottom: 1.15rem;
  font-family: var(--font-serif);
  font-size: 1rem;
  line-height: 2.0;
  color: #1e293b;
  overflow-x: auto;
}}
.passage-title {{
  font-family: var(--font-sans);
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 0.65rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #e2e8f0;
}}
.passage-box table {{
  width: 100%;
  border-collapse: collapse;
  margin: 0.8rem 0;
}}
.passage-box th, .passage-box td {{
  border: 1px solid #cbd5e1;
  padding: 0.45rem 0.65rem;
  font-size: 0.9rem;
}}
.passage-box th {{
  background: #f1f5f9;
}}
.vocab-notes {{
  margin-top: 0.8rem;
  padding-top: 0.65rem;
  border-top: 1px dashed #cbd5e1;
  font-size: 0.85rem;
  color: var(--text-muted);
  font-family: var(--font-sans);
}}

/* Choukai Script Box */
.script-box {{
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-left: 4px solid #8b5cf6;
  border-radius: 6px;
  padding: 1rem 1.15rem;
  margin-bottom: 1.15rem;
  font-size: 0.92rem;
  line-height: 1.8;
}}
.script-audio-jump {{
  margin-top: 0.75rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #ede9fe;
  color: #5b21b6;
  border: 1px solid #c4b5fd;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}}
.script-audio-jump:hover {{
  background: #ddd6fe;
}}

/* Explanation Box */
.explanation-box {{
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 1rem 1.15rem;
  margin-top: 0.75rem;
}}
.exp-heading {{
  font-size: 0.92rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.5rem;
}}
.exp-section-title {{
  font-size: 0.85rem;
  font-weight: 700;
  color: #1e3a8a;
  margin: 0.75rem 0 0.3rem;
}}
.exp-content {{
  font-size: 0.92rem;
  line-height: 1.8;
  color: #334155;
}}
.exp-options-list {{
  list-style: none;
  margin-top: 0.35rem;
}}
.exp-options-list li {{
  padding: 0.35rem 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.9rem;
  line-height: 1.7;
}}
.exp-options-list li:last-child {{
  border-bottom: none;
}}
.opt-tag-correct {{
  display: inline-block;
  color: #065f46;
  background: #d1fae5;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-size: 0.78rem;
  font-weight: 700;
  margin-right: 0.35rem;
}}
.opt-tag-wrong {{
  display: inline-block;
  color: #991b1b;
  background: #fee2e2;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-size: 0.78rem;
  font-weight: 700;
  margin-right: 0.35rem;
}}
.vocab-pill {{
  display: inline-block;
  background: #e0f2fe;
  color: #0369a1;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  margin: 0.2rem 0.25rem 0.2rem 0;
}}

/* Sticky Audio Player */
#sticky-audio {{
  position: sticky;
  top: 3.5rem;
  z-index: 95;
  background: #1e293b;
  color: #fff;
  padding: 0.55rem 0.9rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}}
#sticky-audio audio {{
  flex: 1;
  height: 30px;
}}
.audio-status {{
  font-size: 0.8rem;
  color: #94a3b8;
  white-space: nowrap;
}}

/* Language switcher & per-language panes (exam-answer-translation) */
.lang-pane {{ display: none; }}
{lang_css}
.lang-group {{
  display: inline-flex;
  gap: 0.25rem;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  padding: 0.2rem;
}}
.lang-btn {{
  border: none;
  background: transparent;
  color: #cbd5e1;
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 0.28rem 0.7rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}}
.lang-btn:hover {{ color: #ffffff; background: rgba(255,255,255,0.12); }}
.lang-btn.active {{ background: #2563eb; color: #ffffff; }}
.header-right {{ display: inline-flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }}
.trans-block {{
  margin-top: 0.9rem;
  padding-top: 0.8rem;
  border-top: 1px dashed #cbd5e1;
  font-family: var(--font-sans);
  font-size: 0.95rem;
  line-height: 1.85;
  color: #334155;
}}
.trans-title {{
  font-size: 0.8rem;
  font-weight: 700;
  color: #7c3aed;
  letter-spacing: 0.02em;
  margin-bottom: 0.4rem;
}}

/* Footer */
footer {{
  text-align: center;
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-top: 3.5rem;
  padding: 1.5rem 1rem;
  border-top: 1px solid var(--border-color);
}}

@media print {{
  header.app-header, .sticky-nav, .tab-group, .search-box, #sticky-audio, .script-audio-jump, .lang-group {{ display: none !important; }}
  body {{ background: #fff; color: #000; font-size: 10pt; }}
  .q-card {{ page-break-inside: avoid; border: 1px solid #ccc; box-shadow: none; margin-bottom: 1.2cm; }}
}}
</style>
</head>
<body>

<header class="app-header">
  <div class="header-inner">
    <div class="header-top-row">
      <a href="解答.html?screen=result" class="header-back-btn" data-i18n="back_link">← 採点結果へ戻る</a>
      <div class="header-right">
        {lang_switcher_html}
        <span class="header-badge" data-i18n="badge">JLPT N2 MODEL ANSWER &amp; EXPLANATION</span>
      </div>
    </div>
    <h1 class="title" data-i18n="title">日本語能力試験 N2 模範解答・詳細解説</h1>
    <div class="subtitle"><span data-i18n="test_label">テスト</span> <strong>{test_id}</strong> ｜ <span data-i18n="subtitle">全101問（言語知識・読解 71問 ＋ 聴解 30問）完全網羅解説集</span></div>
  </div>
</header>

<div class="sticky-nav">
  <div class="nav-container">
    <div class="tab-group">
      <button class="tab-btn active" onclick="filterSection('all', this)"><span data-i18n="tab_all">すべて</span> (101)</button>
      <button class="tab-btn" onclick="filterSection('goi', this)"><span data-i18n="tab_goi">文字・語彙</span> (30)</button>
      <button class="tab-btn" onclick="filterSection('bunpou', this)"><span data-i18n="tab_bunpou">文法</span> (21)</button>
      <button class="tab-btn" onclick="filterSection('dokkai', this)"><span data-i18n="tab_dokkai">読解</span> (20)</button>
      <button class="tab-btn" onclick="filterSection('choukai', this)"><span data-i18n="tab_choukai">聴解</span> (30)</button>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="問題番号・キーワード検索..." data-i18n-placeholder="search_placeholder" oninput="handleSearch()">
    </div>
  </div>
</div>

<div class="main-container">
  {audio_player_html}

  {content_html}
</div>

<footer>
  JLPT N2 Mock Exam Model Answer & Comprehensive Explanation (模範解答.html)<br>
  Test ID: {test_id}
</footer>

<script>
const I18N = {i18n_json};

function setLang(code) {{
  if (!I18N[code]) code = 'ja';
  const entry = I18N[code];
  document.documentElement.setAttribute('data-lang', code);
  document.documentElement.setAttribute('lang', entry.html_lang || code);
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    let v = entry.ui[el.dataset.i18n];
    if (v === undefined) return;
    if (el.dataset.n !== undefined) v = v.replace('{{n}}', el.dataset.n);
    el.textContent = v;
  }});
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {{
    const v = entry.ui[el.dataset.i18nPlaceholder];
    if (v !== undefined) el.placeholder = v;
  }});
  document.querySelectorAll('.lang-btn').forEach(b => {{
    b.classList.toggle('active', b.dataset.langCode === code);
  }});
  try {{ localStorage.setItem('jlpt.modelAnswerLang', code); }} catch (e) {{}}
}}

(function initLang() {{
  let saved = null;
  try {{ saved = localStorage.getItem('jlpt.modelAnswerLang'); }} catch (e) {{}}
  setLang(saved && I18N[saved] ? saved : 'ja');
}})();

function filterSection(sec, btn) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const cards = document.querySelectorAll('.q-card');
  const banners = document.querySelectorAll('.section-banner');

  cards.forEach(card => {{
    if (sec === 'all' || card.dataset.section === sec) {{
      card.style.display = 'block';
    }} else {{
      card.style.display = 'none';
    }}
  }});

  banners.forEach(b => {{
    if (sec === 'all' || b.dataset.section === sec) {{
      b.style.display = 'flex';
    }} else {{
      b.style.display = 'none';
    }}
  }});
}}

function handleSearch() {{
  const query = document.getElementById('searchInput').value.trim().toLowerCase();
  const cards = document.querySelectorAll('.q-card');

  cards.forEach(card => {{
    if (!query) {{
      card.style.display = 'block';
      return;
    }}
    const text = card.innerText.toLowerCase();
    const qid = card.id.toLowerCase();
    if (text.includes(query) || qid.includes(query)) {{
      card.style.display = 'block';
    }} else {{
      card.style.display = 'none';
    }}
  }});
}}

function playAt(seconds, label) {{
  const audio = document.getElementById('mainAudio');
  if (!audio) return;
  audio.currentTime = seconds;
  audio.play();
  const status = document.getElementById('audioStatus');
  const code = document.documentElement.getAttribute('data-lang') || 'ja';
  const playing = (I18N[code] || I18N.ja).ui.audio_playing;
  if (status) status.innerText = playing + ': ' + label + ' (' + formatTime(seconds) + ')';
}}

function formatTime(sec) {{
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return m + ':' + (s < 10 ? '0' : '') + s;
}}
</script>

</body>
</html>
"""


def explanation_box_html(langs: list, item_key: str, ans_val: int,
                         raw_kaisetsu: str, choukai: bool = False) -> str:
    """One .explanation-box holding one .lang-pane per language.

    Every language renders the SAME item with the SAME [正解] position — the
    tag is applied by index against the official key, never taken from the
    translated text — so a translation cannot move the correct answer. A
    language missing this item falls back to the Japanese explanation rather
    than rendering an empty pane.
    """
    base = langs[0]["data"].get(item_key) or {}
    panes = []
    for lang in langs:
        ui = lang["ui"]
        detail = lang["data"].get(item_key) or {}
        why = apply_furigana(detail.get("why_correct") or base.get("why_correct") or raw_kaisetsu)
        analysis = detail.get("options_analysis") or base.get("options_analysis") or []
        points = [apply_furigana(pt) for pt in (detail.get("points") or base.get("points") or [])]

        opt_exp_li = []
        if analysis:
            for idx, opt_an in enumerate(analysis, 1):
                tag = (f'<span class="opt-tag-correct">{ui["tag_correct"]}</span>' if idx == ans_val
                       else f'<span class="opt-tag-wrong">{ui["tag_wrong"]}</span>')
                clean_an = apply_furigana(clean_option_analysis_text(opt_an))
                opt_exp_li.append(f'<li><strong>{idx}.</strong> {tag} {clean_an}</li>')
        else:
            opt_exp_li.append(f'<li>{apply_furigana(html.escape(raw_kaisetsu))}</li>')

        points_html = ""
        if points:
            pills = "".join(f'<span class="vocab-pill">{pt}</span>' for pt in points)
            title = ui["points_title_choukai"] if choukai else ui["points_title"]
            points_html = f'<div class="exp-section-title">{title}</div><div>{pills}</div>'

        panes.append(f"""<div class="lang-pane" data-lang="{lang["code"]}">
                  <div class="exp-heading">{ui["exp_heading"]}</div>
                  <div class="exp-section-title">{ui["why_title_choukai"] if choukai else ui["why_title"]}</div>
                  <div class="exp-content">{why}</div>
                  <div class="exp-section-title">{ui["options_title"]}</div>
                  <ul class="exp-options-list">
                    {"".join(opt_exp_li)}
                  </ul>
                  {points_html}
                </div>""")
    return f'<div class="explanation-box">{"".join(panes)}</div>'


def translation_blocks_html(langs: list, item_key: str, field: str, title_key: str,
                            formatter) -> str:
    """Translated 本文/スクリプト, rendered UNDER the Japanese one, never over it.

    The exam's own wording is fidelity-locked (verify_fidelity.py, make check),
    and it is also what the item tests — so a passage translation is an extra
    block inside the same box, visible only while its language is selected.
    """
    blocks = []
    for lang in langs[1:]:
        text = (lang["data"].get(item_key) or {}).get(field)
        if not text:
            continue
        blocks.append(
            f'<div class="lang-pane trans-block" data-lang="{lang["code"]}">'
            f'<div class="trans-title">{lang["ui"][title_key]}</div>'
            f'{formatter(text)}</div>')
    return "".join(blocks)


def build_model_answer(test_dir: Path, out_path: Path | None = None) -> Path:
    test_dir = Path(test_dir).resolve()
    if not test_dir.is_dir():
        raise FileNotFoundError(f"Test directory not found: {test_dir}")

    test_id = test_dir.name
    gengo_md_path = test_dir / "言語知識・読解.md"
    choukai_md_path = test_dir / "聴解.md"
    script_path = test_dir / "聴解スクリプト.txt"
    chapter_path = test_dir / "聴解_チャプター.json"

    if not gengo_md_path.is_file() or not choukai_md_path.is_file():
        raise FileNotFoundError(f"Markdown sources missing in {test_dir}")

    gengo_text = gengo_md_path.read_text(encoding="utf-8")
    choukai_text = choukai_md_path.read_text(encoding="utf-8")
    script_text = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""

    _, gengo_exps = parse_gengo_markdown(gengo_text)
    _, choukai_exps = parse_choukai_markdown(choukai_text)
    scripts = parse_choukai_scripts(script_text)

    # Canonical answer keys from grade_answers module
    canonical_gengo_keys = {}
    canonical_choukai_keys = {}
    try:
        exam_app_scripts = ROOT / ".agents/exam-app/scripts"
        if exam_app_scripts.is_dir() and str(exam_app_scripts) not in sys.path:
            sys.path.insert(0, str(exam_app_scripts))
        import grade_answers as ga
        canonical_gengo_keys = ga.parse_gengo_keys(gengo_md_path)
        canonical_choukai_keys = ga.parse_choukai_keys(choukai_md_path)
    except Exception:
        pass

    # Chapters
    chapters_data = {}
    if chapter_path.is_file():
        try:
            cjson = json.loads(chapter_path.read_text(encoding="utf-8"))
            for ch in cjson.get("chapters", []):
                sec = ch.get("section", "")
                lbl = ch.get("label", "")
                st = ch.get("start", 0)
                m_digit = re.search(r"(\d+)", lbl)
                if sec and m_digit:
                    k = f"問{sec.replace('問題', '')}-{m_digit.group(1)}"
                    chapters_data[k] = st
                elif sec == "問題5":
                    if "1" in lbl:
                        chapters_data["問5-1"] = st
                    elif "2" in lbl:
                        chapters_data["問5-2-1"] = st
                        chapters_data["問5-2-2"] = st
        except Exception:
            pass

    # Check for dedicated detailed explanation json
    detailed_json_path = test_dir / "詳細解説.json"
    detailed_data = {}
    if detailed_json_path.is_file():
        try:
            detailed_data = json.loads(detailed_json_path.read_text(encoding="utf-8"))
        except Exception:
            detailed_data = {}

    # Derive raw stems, options, passages, and scripts as fallback for lean explanation formats
    gengo_raw, choukai_raw = {}, {}
    try:
        vf_path = Path(__file__).resolve().parent / "verify_fidelity.py"
        if vf_path.is_file():
            _spec = importlib.util.spec_from_file_location("verify_fidelity", vf_path)
            vf = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(vf)
            gengo_raw = vf.derive_gengo_raw(gengo_text)
            choukai_raw = vf.derive_choukai_raw(choukai_text, script_text)
    except Exception as exc:
        print(f"  ! could not derive raw stems/options from the Markdown: {exc}")

    langs = load_languages(test_dir, detailed_data)
    if len(langs) > 1:
        print(f"  languages: {', '.join(l['code'] for l in langs)}")

    out_file = out_path if out_path else (test_dir / "模範解答.html")

    content_blocks = []

    # 1. Gengo & Dokkai
    current_sec = None
    for tax_key, tax_info in GENGO_TAXONOMY.items():
        sec_name = tax_info["section"]
        sec_code = "goi" if sec_name == "文字・語彙" else ("bunpou" if sec_name == "文法" else "dokkai")
        
        if current_sec != sec_name:
            current_sec = sec_name
            content_blocks.append(
                f'<div class="section-banner" data-section="{sec_code}">'
                f'<span>【{sec_name}】{tax_info["mondai"]} 〜</span>'
                f'<small>JLPT N2 {sec_name}</small></div>'
            )

        q_start, q_end = tax_info["range"]
        for q_num in range(q_start, q_end + 1):
            exp_info = gengo_exps.get(q_num, {})
            ans_val = exp_info.get("ans")
            if ans_val not in (1, 2, 3, 4):
                ans_val = canonical_gengo_keys.get(q_num, 1)
            raw_kaisetsu = exp_info.get("raw_kaisetsu", "")

            detail = detailed_data.get(str(q_num), {})
            raw_q = gengo_raw.get(q_num, {})
            
            raw_stem = detail.get("stem") or raw_q.get("stem") or f"第 {q_num} 問"
            stem_text = apply_furigana(raw_stem)
            raw_opts = detail.get("options") or raw_q.get("options") or [f"選択肢 {i}" for i in range(1, 5)]
            options = [apply_furigana(opt) for opt in raw_opts]
            passage_html = ""
            passage_text = detail.get("passage") if "passage" in detail else raw_q.get("passage")
            if passage_text:
                passage_content = format_passage_text(passage_text)
                passage_trans = translation_blocks_html(
                    langs, str(q_num), "passage", "passage_trans_title", format_passage_text)
                passage_html = (
                    f'<div class="passage-box">'
                    f'<div class="passage-title" data-i18n="passage_title">本文 / 資料</div>'
                    f'{passage_content}{passage_trans}</div>')

            opt_items_html = []
            for i, opt in enumerate(options, 1):
                is_corr = (i == ans_val)
                cls = "opt-item is-correct" if is_corr else "opt-item"
                opt_items_html.append(f'<div class="{cls}"><span class="opt-num">{i}</span><span>{opt}</span></div>')

            explanation_html = explanation_box_html(langs, str(q_num), ans_val, raw_kaisetsu)

            card_html = f"""
            <div class="q-card" id="q-{q_num}" data-section="{sec_code}">
              <div class="q-header">
                <div class="q-meta">
                  <span class="q-num-badge" data-i18n="question_label" data-n="{q_num}">第 {q_num} 問</span>
                  <span class="q-type-badge">{tax_info["mondai"]} {tax_info["name"]}</span>
                </div>
                <div class="q-ans-badge"><span data-i18n="answer_label">正解</span>: {ans_val}</div>
              </div>
              <div class="q-body">
                {passage_html}
                <div class="q-stem">{stem_text}</div>
                <div class="options-grid">
                  {"".join(opt_items_html)}
                </div>
                {explanation_html}
              </div>
            </div>
            """
            content_blocks.append(card_html)

    # 2. Choukai
    content_blocks.append(
        f'<div class="section-banner" data-section="choukai">'
        f'<span>【聴解】問題1〜問題5</span>'
        f'<small>JLPT N2 Choukai</small></div>'
    )

    all_choukai_keys = sorted(set(list(choukai_exps.keys()) + list(canonical_choukai_keys.keys()) + list(choukai_raw.keys())))
    for key_id in all_choukai_keys:
        exp_info = choukai_exps.get(key_id, {})
        ans_val = exp_info.get("ans")
        if ans_val not in (1, 2, 3, 4):
            ans_val = canonical_choukai_keys.get(key_id, 1)
        raw_kaisetsu = exp_info.get("raw_kaisetsu", "")
        safe_id = key_id.replace("問", "choukai-").replace("-", "_")

        detail = detailed_data.get(key_id, {})
        raw_c = choukai_raw.get(key_id, {})
        raw_stem = detail.get("stem") or raw_c.get("stem") or f"{key_id} 聴解問題"
        stem_text = apply_furigana(raw_stem)
        raw_opts = detail.get("options") or raw_c.get("options") or [f"選択肢 {i}" for i in range(1, 5)]
        options = [apply_furigana(opt) for opt in raw_opts]
        raw_script = detail.get("script") if "script" in detail else (raw_c.get("script") or scripts.get(key_id, "（音声スクリプト参照）"))
        script_snippet = apply_furigana(raw_script or "（音声スクリプト参照）")
        script_trans = translation_blocks_html(
            langs, key_id, "script", "script_trans_title", apply_furigana)
        explanation_html = explanation_box_html(langs, key_id, ans_val, raw_kaisetsu, choukai=True)

        opt_items_html = []
        for i, opt in enumerate(options, 1):
            is_corr = (i == ans_val)
            cls = "opt-item is-correct" if is_corr else "opt-item"
            opt_items_html.append(f'<div class="{cls}"><span class="opt-num">{i}</span><span>{opt}</span></div>')

        audio_jump_btn = ""
        if key_id in chapters_data:
            st = chapters_data[key_id]
            audio_jump_btn = (
                f'<button class="script-audio-jump" onclick="playAt({st}, \'{key_id}\')">'
                f'<span data-i18n="audio_jump">音声再生</span> '
                f'({int(st//60)}:{int(st%60):02d})</button>')

        card_html = f"""
        <div class="q-card" id="{safe_id}" data-section="choukai">
          <div class="q-header">
            <div class="q-meta">
              <span class="q-num-badge">{key_id}</span>
              <span class="q-type-badge">聴解セクション</span>
            </div>
            <div class="q-ans-badge"><span data-i18n="answer_label">正解</span>: {ans_val}</div>
          </div>
          <div class="q-body">
            <div class="script-box">
              <div class="passage-title" data-i18n="script_title">音声スクリプト</div>
              {script_snippet}
              {script_trans}
              {audio_jump_btn}
            </div>
            <div class="q-stem">{stem_text}</div>
            <div class="options-grid">
              {"".join(opt_items_html)}
            </div>
            {explanation_html}
          </div>
        </div>
        """
        content_blocks.append(card_html)

    # Sticky audio player if 聴解.mp3 exists
    audio_player_html = ""
    mp3_path = test_dir / "聴解.mp3"
    if mp3_path.is_file():
        audio_player_html = """
        <div id="sticky-audio">
          <span style="font-weight:700; font-size:0.85rem;" data-i18n="audio_label">聴解音声</span>
          <audio id="mainAudio" controls preload="metadata" src="聴解.mp3"></audio>
          <span id="audioStatus" class="audio-status" data-i18n="audio_ready">準備完了</span>
        </div>
        """

    lang_css = "\n".join(
        f'html[data-lang="{l["code"]}"] .lang-pane[data-lang="{l["code"]}"] {{ display: block; }}'
        for l in langs)
    lang_switcher_html = ""
    if len(langs) > 1:
        buttons = "".join(
            f'<button class="lang-btn" data-lang-code="{l["code"]}" '
            f'onclick="setLang(\'{l["code"]}\')">{html.escape(l["label"])}</button>'
            for l in langs)
        lang_switcher_html = f'<div class="lang-group">{buttons}</div>'
    i18n = {l["code"]: {"html_lang": l["html_lang"], "label": l["label"], "ui": l["ui"]}
            for l in langs}

    rendered_html = HTML_TEMPLATE.format(
        test_id=test_id,
        audio_player_html=audio_player_html,
        content_html="\n".join(content_blocks),
        lang_css=lang_css,
        lang_switcher_html=lang_switcher_html,
        i18n_json=json.dumps(i18n, ensure_ascii=False),
    )

    out_file.write_text(rendered_html, encoding="utf-8")
    print(f"✓ 模範解答.html successfully generated: {out_file}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Generate 模範解答.html model answer deliverable.")
    parser.add_argument("test_dir", help="Path to test directory (e.g. tests/20260807_1)")
    parser.add_argument("-o", "--out", help="Output file path (default: tests/<id>/模範解答.html)")
    args = parser.parse_args()

    test_path = Path(args.test_dir)
    out_path = Path(args.out) if args.out else None
    build_model_answer(test_path, out_path)


if __name__ == "__main__":
    main()
