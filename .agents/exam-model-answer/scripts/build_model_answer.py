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
    """
    key_split = re.split(r"^#+\s*(?:解答|【?正解)", gengo_md_text, flags=re.M)
    exam_body = key_split[0]
    key_body = key_split[1] if len(key_split) > 1 else ""

    # Parse explanation table
    explanations = {}
    for line in key_body.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                q_str = re.sub(r"[^\d]", "", parts[0])
                ans_str = re.sub(r"[^\d]", "", parts[1])
                if q_str.isdigit() and ans_str.isdigit():
                    q_num = int(q_str)
                    explanations[q_num] = {
                        "ans": int(ans_str),
                        "raw_kaisetsu": parts[2]
                    }

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
            if len(parts) >= 3:
                q_label = parts[0].replace("*", "").strip()
                ans_str = re.sub(r"[^\d]", "", parts[1])
                if q_label in ("例", "番号", "問"):
                    continue
                if ans_str.isdigit():
                    ans_val = int(ans_str)
                    kaisetsu = parts[2]
                    key_id = None
                    if current_mondai in (1, 2, 3, 4):
                        m_digit = re.search(r"(\d+)", q_label)
                        if m_digit:
                            key_id = f"問{current_mondai}-{m_digit.group(1)}"
                    elif current_mondai == 5:
                        if "質問1" in q_label:
                            key_id = "問5-2-1"
                        elif "質問2" in q_label:
                            key_id = "問5-2-2"
                        elif "1" in q_label:
                            key_id = "問5-1"
                        elif "2" in q_label:
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
<html lang="ja">
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
  header.app-header, .sticky-nav, .tab-group, .search-box, #sticky-audio, .script-audio-jump {{ display: none !important; }}
  body {{ background: #fff; color: #000; font-size: 10pt; }}
  .q-card {{ page-break-inside: avoid; border: 1px solid #ccc; box-shadow: none; margin-bottom: 1.2cm; }}
}}
</style>
</head>
<body>

<header class="app-header">
  <div class="header-inner">
    <div class="header-top-row">
      <a href="解答.html?screen=result" class="header-back-btn">← 採点結果へ戻る</a>
      <span class="header-badge">JLPT N2 MODEL ANSWER & EXPLANATION</span>
    </div>
    <h1 class="title">日本語能力試験 N2 模範解答・詳細解説</h1>
    <div class="subtitle">テスト <strong>{test_id}</strong> ｜ 全101問（言語知識・読解 71問 ＋ 聴解 30問）完全網羅解説集</div>
  </div>
</header>

<div class="sticky-nav">
  <div class="nav-container">
    <div class="tab-group">
      <button class="tab-btn active" onclick="filterSection('all', this)">すべて (101)</button>
      <button class="tab-btn" onclick="filterSection('goi', this)">文字・語彙 (30)</button>
      <button class="tab-btn" onclick="filterSection('bunpou', this)">文法 (21)</button>
      <button class="tab-btn" onclick="filterSection('dokkai', this)">読解 (20)</button>
      <button class="tab-btn" onclick="filterSection('choukai', this)">聴解 (30)</button>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="問題番号・キーワード検索..." oninput="handleSearch()">
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
  if (status) status.innerText = '再生中: ' + label + ' (' + formatTime(seconds) + ')';
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
            ans_val = exp_info.get("ans", 1)
            raw_kaisetsu = exp_info.get("raw_kaisetsu", "")

            detail = detailed_data.get(str(q_num), {})
            
            raw_stem = detail.get("stem") or f"第 {q_num} 問"
            stem_text = apply_furigana(raw_stem)
            options = [apply_furigana(opt) for opt in (detail.get("options") or [f"選択肢 {i}" for i in range(1, 5)])]
            why_correct = apply_furigana(detail.get("why_correct") or raw_kaisetsu)
            options_analysis = detail.get("options_analysis") or []
            points = [apply_furigana(p) for p in (detail.get("points") or [])]
            
            passage_html = ""
            if detail.get("passage"):
                passage_content = format_passage_text(detail["passage"])
                passage_html = f'<div class="passage-box"><div class="passage-title">本文 / 資料</div>{passage_content}</div>'

            opt_items_html = []
            for i, opt in enumerate(options, 1):
                is_corr = (i == ans_val)
                cls = "opt-item is-correct" if is_corr else "opt-item"
                opt_items_html.append(f'<div class="{cls}"><span class="opt-num">{i}</span><span>{opt}</span></div>')

            opt_exp_li = []
            if options_analysis:
                for idx, opt_an in enumerate(options_analysis, 1):
                    tag = '<span class="opt-tag-correct">[正解]</span>' if idx == ans_val else '<span class="opt-tag-wrong">[不正解]</span>'
                    clean_an = clean_option_analysis_text(opt_an)
                    clean_an_furi = apply_furigana(clean_an)
                    opt_exp_li.append(f'<li><strong>{idx}.</strong> {tag} {clean_an_furi}</li>')
            else:
                opt_exp_li.append(f'<li>{apply_furigana(html.escape(raw_kaisetsu))}</li>')

            points_html = ""
            if points:
                pills = "".join(f'<span class="vocab-pill">{p}</span>' for p in points)
                points_html = f'<div class="exp-section-title">【重要語彙・文法ポイント】</div><div>{pills}</div>'

            card_html = f"""
            <div class="q-card" id="q-{q_num}" data-section="{sec_code}">
              <div class="q-header">
                <div class="q-meta">
                  <span class="q-num-badge">第 {q_num} 問</span>
                  <span class="q-type-badge">{tax_info["mondai"]} {tax_info["name"]}</span>
                </div>
                <div class="q-ans-badge">正解: {ans_val}</div>
              </div>
              <div class="q-body">
                {passage_html}
                <div class="q-stem">{stem_text}</div>
                <div class="options-grid">
                  {"".join(opt_items_html)}
                </div>
                <div class="explanation-box">
                  <div class="exp-heading">詳細解説</div>
                  <div class="exp-section-title">【正解の理由・根拠】</div>
                  <div class="exp-content">{why_correct}</div>
                  <div class="exp-section-title">【各選択肢の解説】</div>
                  <ul class="exp-options-list">
                    {"".join(opt_exp_li)}
                  </ul>
                  {points_html}
                </div>
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

    for key_id, exp_info in sorted(choukai_exps.items()):
        ans_val = exp_info.get("ans", 1)
        raw_kaisetsu = exp_info.get("raw_kaisetsu", "")
        safe_id = key_id.replace("問", "choukai-").replace("-", "_")

        detail = detailed_data.get(key_id, {})
        stem_text = apply_furigana(detail.get("stem") or f"{key_id} 聴解問題")
        options = [apply_furigana(opt) for opt in (detail.get("options") or [f"選択肢 {i}" for i in range(1, 5)])]
        script_snippet = apply_furigana(detail.get("script") or scripts.get(key_id, "（音声スクリプト参照）"))
        why_correct = apply_furigana(detail.get("why_correct") or raw_kaisetsu)
        options_analysis = detail.get("options_analysis") or []
        points = [apply_furigana(p) for p in (detail.get("points") or [])]

        opt_items_html = []
        for i, opt in enumerate(options, 1):
            is_corr = (i == ans_val)
            cls = "opt-item is-correct" if is_corr else "opt-item"
            opt_items_html.append(f'<div class="{cls}"><span class="opt-num">{i}</span><span>{opt}</span></div>')

        opt_exp_li = []
        if options_analysis:
            for idx, opt_an in enumerate(options_analysis, 1):
                tag = '<span class="opt-tag-correct">[正解]</span>' if idx == ans_val else '<span class="opt-tag-wrong">[不正解]</span>'
                clean_an = clean_option_analysis_text(opt_an)
                clean_an_furi = apply_furigana(clean_an)
                opt_exp_li.append(f'<li><strong>{idx}.</strong> {tag} {clean_an_furi}</li>')
        else:
            opt_exp_li.append(f'<li>{apply_furigana(html.escape(raw_kaisetsu))}</li>')

        points_html = ""
        if points:
            pills = "".join(f'<span class="vocab-pill">{p}</span>' for p in points)
            points_html = f'<div class="exp-section-title">【重要表現・リスニングポイント】</div><div>{pills}</div>'

        audio_jump_btn = ""
        if key_id in chapters_data:
            st = chapters_data[key_id]
            audio_jump_btn = f'<button class="script-audio-jump" onclick="playAt({st}, \'{key_id}\')">音声再生 ({int(st//60)}:{int(st%60):02d})</button>'

        card_html = f"""
        <div class="q-card" id="{safe_id}" data-section="choukai">
          <div class="q-header">
            <div class="q-meta">
              <span class="q-num-badge">{key_id}</span>
              <span class="q-type-badge">聴解セクション</span>
            </div>
            <div class="q-ans-badge">正解: {ans_val}</div>
          </div>
          <div class="q-body">
            <div class="script-box">
              <div class="passage-title">音声スクリプト</div>
              {script_snippet}
              {audio_jump_btn}
            </div>
            <div class="q-stem">{stem_text}</div>
            <div class="options-grid">
              {"".join(opt_items_html)}
            </div>
            <div class="explanation-box">
              <div class="exp-heading">詳細解説</div>
              <div class="exp-section-title">【正解の理由・聞き取りポイント】</div>
              <div class="exp-content">{why_correct}</div>
              <div class="exp-section-title">【各選択肢の解説】</div>
              <ul class="exp-options-list">
                {"".join(opt_exp_li)}
              </ul>
              {points_html}
            </div>
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
          <span style="font-weight:700; font-size:0.85rem;">聴解音声</span>
          <audio id="mainAudio" controls preload="metadata" src="聴解.mp3"></audio>
          <span id="audioStatus" class="audio-status">準備完了</span>
        </div>
        """

    rendered_html = HTML_TEMPLATE.format(
        test_id=test_id,
        audio_player_html=audio_player_html,
        content_html="\n".join(content_blocks)
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
