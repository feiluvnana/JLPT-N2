#!/usr/bin/env python3
"""
JLPT Mock Exam Grading & Diagnostic Script.

Grades user responses against official answer keys in tests/<test_id>/,
calculates standardized scaled scores (0-180), evaluates Pass/Fail criteria,
identifies weak sub-sections, and generates detailed Markdown diagnostic reports.

Usage:
    # 1. Create a user answer template file for a test:
    python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --create-template

    # 2. Grade user answers from JSON file:
    python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --user-answers tests/1/user_answers.json

    # 3. Quick grade via CLI strings:
    python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/1 --answers-gengo "1:4,2:2,3:1..." --answers-choukai "1:2,2:3..."
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Sub-question mapping definitions for JLPT N2
GENGO_QUESTION_TAXONOMY = {
    # 言語知識（文字・語彙）
    "問1": {"name": "漢字読み (Kanji Reading)", "range": (1, 8), "section": "言語知識", "total": 8},
    "問2": {"name": "表記 (Kanji Writing)", "range": (9, 13), "section": "言語知識", "total": 5},
    "問3": {"name": "語形成 (Word Formation)", "range": (14, 18), "section": "言語知識", "total": 5},
    "問4": {"name": "文脈指示 (Contextual Use)", "range": (19, 25), "section": "言語知識", "total": 7},
    "問5": {"name": "言い換え類義 (Paraphrases)", "range": (26, 30), "section": "言語知識", "total": 5},
    "問6": {"name": "用法 (Correct Usage)", "range": (31, 32), "section": "言語知識", "total": 2},
    # 言語知識（文法）
    "問7": {"name": "文の文法1 (Grammar Form)", "range": (33, 44), "section": "言語知識", "total": 12},
    "問8": {"name": "文の文法2 (Sentence Composition ★)", "range": (45, 49), "section": "言語知識", "total": 5},
    "問9": {"name": "文章の文法 (Text Grammar)", "range": (50, 54), "section": "言語知識", "total": 5},
    # 読解
    "問10": {"name": "短文読解 (Short Passages)", "range": (55, 59), "section": "読解", "total": 5},
    "問11": {"name": "中文読解 (Medium Passages)", "range": (60, 64), "section": "読解", "total": 5},
    "問12": {"name": "長文読解 (Long Passage)", "range": (65, 67), "section": "読解", "total": 3},
    "問13": {"name": "統合理解 (Comparative Passages)", "range": (68, 70), "section": "読解", "total": 3},
    "問14": {"name": "主張理解/情報検索 (Thematic & Info Retrieval)", "range": (71, 75), "section": "読解", "total": 5},
}

CHOUKAI_QUESTION_TAXONOMY = {
    "問題1": {"name": "課題理解 (Task Comprehension)", "section": "聴解"},
    "問題2": {"name": "ポイント理解 (Point Comprehension)", "section": "聴解"},
    "問題3": {"name": "概要理解 (Summary Comprehension)", "section": "聴解"},
    "問題4": {"name": "即時応答 (Quick Response)", "section": "聴解"},
    "問題5": {"name": "統合理解 (Integrated Comprehension)", "section": "聴解"},
}


def parse_gengo_keys(gengo_md_path: Path) -> dict:
    """Extract correct answers for Language Knowledge & Reading (Questions 1 to 75)."""
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
                    if 1 <= q_num <= 75 and 1 <= a_num <= 4:
                        answers[q_num] = a_num

    return answers


def parse_choukai_keys(choukai_md_path: Path) -> dict:
    """
    Extract correct answers for Listening (Choukai).
    Returns dict mapping item key (e.g. '問1-1', '問4-5', '問5-3-1') to correct answer option (1-4).
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
                        if "1" in q_label and "質問" not in q_label and "3" not in q_label:
                            answers["問5-1"] = ans_val
                        elif "2" in q_label and "質問" not in q_label and "3" not in q_label:
                            answers["問5-2"] = ans_val
                        elif "3" in q_label or "質問" in q_label:
                            q_sub = re.search(r"質問([12])|3番-(\d)", q_label)
                            if q_sub:
                                sub_num = q_sub.group(1) or q_sub.group(2)
                                answers[f"問5-3-{sub_num}"] = ans_val
                            elif "1" in q_label:
                                answers["問5-3-1"] = ans_val
                            elif "2" in q_label:
                                answers["問5-3-2"] = ans_val

    return answers


def generate_template(gengo_keys: dict, choukai_keys: dict, output_dir: Path):
    """Generate interactive PDF and HTML mark sheets for examinees."""
    html_sheet_path = output_dir / "マークシート.html"
    generate_html_sheet(gengo_keys, choukai_keys, html_sheet_path)

    pdf_sheet_path = output_dir / "マークシート.pdf"
    generate_pdf_marksheet(gengo_keys, choukai_keys, pdf_sheet_path)


def generate_html_sheet(gengo_keys: dict, choukai_keys: dict, output_path: Path):
    """Generate an interactive HTML bubble mark sheet for examinees."""
    gengo_col1 = [q for q in sorted(gengo_keys.keys()) if 1 <= q <= 25]
    gengo_col2 = [q for q in sorted(gengo_keys.keys()) if 26 <= q <= 50]
    gengo_col3 = [q for q in sorted(gengo_keys.keys()) if 51 <= q <= 75]

    def render_rows(q_list, prefix="g"):
        rows = ""
        for q in q_list:
            label_text = f"問 {q}" if prefix == "g" else str(q)
            rows += f"""
            <tr>
                <td class="q-num">{label_text}</td>
                <td class="b-cell"><input type="radio" id="{prefix}_{q}_1" name="{prefix}_{q}" value="1"><label for="{prefix}_{q}_1">1</label></td>
                <td class="b-cell"><input type="radio" id="{prefix}_{q}_2" name="{prefix}_{q}" value="2"><label for="{prefix}_{q}_2">2</label></td>
                <td class="b-cell"><input type="radio" id="{prefix}_{q}_3" name="{prefix}_{q}" value="3"><label for="{prefix}_{q}_3">3</label></td>
                <td class="b-cell"><input type="radio" id="{prefix}_{q}_4" name="{prefix}_{q}" value="4"><label for="{prefix}_{q}_4">4</label></td>
            </tr>"""
        return rows

    g1_html = render_rows(gengo_col1, "g")
    g2_html = render_rows(gengo_col2, "g")
    g3_html = render_rows(gengo_col3, "g")

    choukai_list = sorted(choukai_keys.keys())
    half = (len(choukai_list) + 1) // 2
    c_col1 = choukai_list[:half]
    c_col2 = choukai_list[half:]

    def render_choukai_rows(q_list):
        rows = ""
        for k in q_list:
            rows += f"""
            <tr>
                <td class="q-num">{k}</td>
                <td class="b-cell"><input type="radio" id="c_{k}_1" name="c_{k}" value="1"><label for="c_{k}_1">1</label></td>
                <td class="b-cell"><input type="radio" id="c_{k}_2" name="c_{k}" value="2"><label for="c_{k}_2">2</label></td>
                <td class="b-cell"><input type="radio" id="c_{k}_3" name="c_{k}" value="3"><label for="c_{k}_3">3</label></td>
                <td class="b-cell"><input type="radio" id="c_{k}_4" name="c_{k}" value="4"><label for="c_{k}_4">4</label></td>
            </tr>"""
        return rows

    c1_html = render_choukai_rows(c_col1)
    c2_html = render_choukai_rows(c_col2)

    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>JLPT N2 解答マークシート</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Meiryo", sans-serif; background: #f0f2f5; color: #1a1a1a; margin: 0; padding: 20px; }}
    .container {{ max-width: 1040px; margin: 0 auto; background: #fff; border-radius: 12px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
    h1 {{ text-align: center; border-bottom: 3px solid #2c3e50; padding-bottom: 12px; margin-top: 0; font-size: 1.6rem; color: #1a252f; }}
    .section-title {{ background: #2c3e50; color: #fff; padding: 8px 16px; border-radius: 6px; margin-top: 28px; margin-bottom: 12px; font-size: 1.05rem; font-weight: 600; }}
    .instructions {{ background: #eef7ed; border-left: 4px solid #27ae60; padding: 12px 16px; margin-bottom: 24px; font-size: 0.92rem; line-height: 1.5; border-radius: 0 6px 6px 0; }}
    
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
    
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e1e4e8; border-radius: 4px; overflow: hidden; }}
    th, td {{ border: 1px solid #e1e4e8; padding: 4px 6px; text-align: center; height: 26px; }}
    th {{ background: #f4f6f8; font-size: 0.82rem; font-weight: 700; color: #444; }}
    .q-num {{ font-weight: 700; width: 44px; text-align: left; background: #fcfcfc; padding-left: 8px; font-size: 0.82rem; color: #333; }}
    
    .b-cell input[type="radio"] {{ position: absolute; opacity: 0; width: 0; height: 0; }}
    .b-cell label {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        border: 1.5px solid #666;
        font-size: 0.78rem;
        font-weight: 700;
        cursor: pointer;
        user-select: none;
        transition: all 0.12s ease-in-out;
        background: #fff;
        color: #444;
        margin: 0 auto;
    }}
    .b-cell label:hover {{ border-color: #27ae60; color: #27ae60; background: #f0faf3; }}
    .b-cell input[type="radio"]:checked + label {{
        background: #1a252f;
        color: #fff;
        border-color: #1a252f;
        box-shadow: 0 0 0 2px rgba(26, 37, 47, 0.2);
        transform: scale(1.08);
    }}
    
    .actions {{ text-align: center; margin-top: 36px; padding-top: 20px; border-top: 1px solid #eee; }}
    .btn {{ background: #27ae60; color: white; border: none; padding: 13px 32px; font-size: 1.05rem; border-radius: 8px; cursor: pointer; font-weight: 700; box-shadow: 0 4px 10px rgba(39,174,96,0.25); transition: all 0.15s; }}
    .btn:hover {{ background: #219150; transform: translateY(-1px); box-shadow: 0 6px 14px rgba(39,174,96,0.3); }}
    
    @media (max-width: 840px) {{
        .grid-3, .grid-2 {{ grid-template-columns: 1fr; }}
    }}
</style>
</head>
<body>
<div class="container">
    <h1>JLPT N2 模擬試験 解答マークシート</h1>
    <div class="instructions">
        💡 <strong>使い方:</strong> 各設問の番号（1, 2, 3, 4）をタップ・クリックして選択してください。選択後、下部の「解答をJSONとして保存」ボタンを押すと、採点用ファイル <code>user_answers.json</code> がダウンロードされます。
    </div>
    <form id="sheetForm">
        <div class="section-title">言語知識・読解 (問1 〜 問75)</div>
        <div class="grid-3">
            <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{g1_html}</tbody></table>
            <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{g2_html}</tbody></table>
            <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{g3_html}</tbody></table>
        </div>

        <div class="section-title">聴解 (問題1 〜 問題5)</div>
        <div class="grid-2">
            <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{c1_html}</tbody></table>
            <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{c2_html}</tbody></table>
        </div>

        <div class="actions">
            <button type="button" class="btn" onclick="saveAnswers()">💾 解答をJSONとして保存 (user_answers.json)</button>
        </div>
    </form>
</div>
<script>
function saveAnswers() {{
    const formData = new FormData(document.getElementById('sheetForm'));
    const result = {{ "言語知識_読解": {{}}, "聴解": {{}} }};

    for (let q = 1; q <= 75; q++) {{
        const val = formData.get('g_' + q);
        if (val) result["言語知識_読解"][q.toString()] = parseInt(val);
    }}

    const choukaiKeys = {json.dumps(list(choukai_keys.keys()))};
    choukaiKeys.forEach(k => {{
        const val = formData.get('c_' + k);
        if (val) result["聴解"][k] = parseInt(val);
    }});

    const blob = new Blob([JSON.stringify(result, null, 2)], {{ type: "application/json" }});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = "user_answers.json";
    a.click();
}}
</script>
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    print(f"Created interactive HTML mark sheet: {output_path}")


def parse_user_pdf(pdf_path: Path) -> dict:
    """
    Extract user answers directly from a PDF file.
    Supports both AcroForm Interactive Radio buttons AND visual annotation extraction.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        print("Error: pypdf not installed.", file=sys.stderr)
        return {"言語知識_読解": {}, "聴解": {}}

    user_answers = {"言語知識_読解": {}, "聴解": {}}
    reader = PdfReader(str(pdf_path))

    # 1. Parse AcroForm Radio values (e.g., g_1=2, c_問1-1=3)
    if reader.get_fields():
        fields = reader.get_fields()
        for name, field in fields.items():
            val = field.get('/V')
            if val and val != '/Off':
                val_str = str(val).lstrip('/')
                if val_str.isdigit():
                    if name.startswith("g_"):
                        q_num = name[2:]
                        user_answers["言語知識_読解"][q_num] = int(val_str)
                    elif name.startswith("c_"):
                        k_name = name[2:]
                        user_answers["聴解"][k_name] = int(val_str)

    # 2. Check field annotations if not in top-level fields
    for page in reader.pages:
        if "/Annots" in page:
            for annot in page["/Annots"]:
                try:
                    obj = annot.get_object()
                    name = obj.get("/T")
                    val = obj.get("/V")
                    if name and val and val != "/Off":
                        name_str = str(name)
                        val_str = str(val).lstrip("/")
                        if val_str.isdigit():
                            if name_str.startswith("g_"):
                                q_num = name_str[2:]
                                user_answers["言語知識_読解"][q_num] = int(val_str)
                            elif name_str.startswith("c_"):
                                k_name = name_str[2:]
                                user_answers["聴解"][k_name] = int(val_str)
                except Exception:
                    pass

    return user_answers


def generate_pdf_marksheet(gengo_keys: dict, choukai_keys: dict, output_pdf_path: Path):
    """
    Generate an interactive PDF answer mark sheet (マークシート.pdf) with AcroForm radio buttons.
    Uses Weasyprint's exact box layout positions to align AcroForm fields perfectly centered
    inside every option cell.

    COORDINATE NOTE: WeasyPrint lays out boxes in CSS pixels (96/inch) but writes
    the PDF in points (72/inch). Layout coordinates must therefore be scaled by
    the px->pt factor (nominally 0.75) before being used as AcroForm /Rect
    values, or every widget drifts toward the top-right of the page and ends up
    scattered over the title instead of centered in its cell.
    """
    try:
        import weasyprint
        from pypdf import PdfWriter, PdfReader
        from pypdf.generic import (
            DictionaryObject, NameObject, NumberObject, ArrayObject,
            TextStringObject
        )
    except ImportError:
        print("Notice: weasyprint or pypdf missing. Skipping interactive PDF sheet generation.")
        return

    # 1. Build Page 1 (Gengo/Dokkai) HTML: 問1 〜 問75 in 3 columns
    def render_pdf_gengo_rows(q_range):
        rows = ""
        for q in q_range:
            opts = "".join(f'<td data-prefix="g" data-q="{q}" data-opt="{opt}"></td>' for opt in range(1, 5))
            rows += f'<tr><td class="q">問 {q}</td>{opts}</tr>'
        return rows

    col1_rows = render_pdf_gengo_rows(range(1, 26))
    col2_rows = render_pdf_gengo_rows(range(26, 51))
    col3_rows = render_pdf_gengo_rows(range(51, 76))

    # 2. Build Page 2 (Choukai) HTML: 問題1 〜 問題5 in 2 columns
    choukai_list = sorted(choukai_keys.keys())
    half = (len(choukai_list) + 1) // 2
    c_col1 = choukai_list[:half]
    c_col2 = choukai_list[half:]

    def render_pdf_choukai_rows(keys):
        rows = ""
        for k in keys:
            opts = "".join(f'<td data-prefix="c" data-q="{k}" data-opt="{opt}"></td>' for opt in range(1, 5))
            rows += f'<tr><td class="q">{k}</td>{opts}</tr>'
        return rows

    c_col1_rows = render_pdf_choukai_rows(c_col1)
    c_col2_rows = render_pdf_choukai_rows(c_col2)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{ size: A4; margin: 10mm 10mm; }}
body {{ font-family: 'Noto Sans CJK JP', sans-serif; font-size: 8.5pt; color: #111; margin: 0; }}
h1 {{ text-align: center; font-size: 13pt; margin: 0 0 4pt 0; padding-bottom: 2pt; border-bottom: 2pt solid #2c3e50; }}
.instructions {{ background: #eef7ed; border-left: 3pt solid #27ae60; padding: 4pt 8pt; margin-bottom: 8pt; font-size: 8pt; line-height: 1.4; }}
.columns {{ display: flex; justify-content: space-between; }}
.col-3 {{ width: 31.8%; }}
.col-2 {{ width: 48.5%; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 2pt; }}
th, td {{ border: 0.5pt solid #888; height: 18.5pt; text-align: center; font-size: 8pt; vertical-align: middle; padding: 0; }}
th {{ background: #e8ecef; font-weight: bold; height: 16pt; font-size: 8.5pt; }}
.q {{ font-weight: bold; width: 32pt; background: #fafafa; text-align: left; padding-left: 4pt; font-size: 8pt; }}
.page-break {{ page-break-after: always; }}
</style>
</head>
<body>

<!-- PAGE 1: 言語知識・読解 -->
<h1>JLPT N2 解答マークシート（言語知識・読解）</h1>
<div class="instructions">
💡 <b>マーク方法:</b> 各設問の選択肢（1・2・3・4）をラジオボタンでクリックして選択してください。保存後、<code>make grade 1</code> でそのまま採点できます。
</div>
<div class="columns">
  <div class="col-3">
    <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{col1_rows}</tbody></table>
  </div>
  <div class="col-3">
    <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{col2_rows}</tbody></table>
  </div>
  <div class="col-3">
    <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{col3_rows}</tbody></table>
  </div>
</div>

<div class="page-break"></div>

<!-- PAGE 2: 聴解 -->
<h1>JLPT N2 解答マークシート（聴解）</h1>
<div class="instructions">
💡 <b>マーク方法:</b> 聴解問題の選択肢（1・2・3・4）をラジオボタンでクリックして選択してください。
</div>
<div class="columns">
  <div class="col-2">
    <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{c_col1_rows}</tbody></table>
  </div>
  <div class="col-2">
    <table><thead><tr><th>設問</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody>{c_col2_rows}</tbody></table>
  </div>
</div>

</body>
</html>"""

    # 3. Render base PDF with Weasyprint and capture exact layout box positions
    doc = weasyprint.HTML(string=html).render()
    base_pdf_temp = output_pdf_path.parent / "_temp_base_sheet.pdf"
    doc.write_pdf(str(base_pdf_temp))

    # Read the rendered PDF now so the real page size (in POINTS) is known.
    # WeasyPrint layout coordinates are CSS pixels; derive the exact px->pt
    # scale per page from the PDF itself (robust across WeasyPrint versions;
    # nominally 72/96 = 0.75 on both axes).
    reader = PdfReader(str(base_pdf_temp))
    page_scales = []
    for p_idx, page_box in enumerate(doc.pages):
        mb = reader.pages[p_idx].mediabox
        page_scales.append((
            float(mb.width) / page_box.width,    # px -> pt, x axis
            float(mb.height) / page_box.height,  # px -> pt, y axis
            float(mb.height),                    # page height in POINTS
        ))

    # Extract cell coordinates per page: page_idx -> dict of (prefix, q, opt) -> (center_x_pt, center_y_pt)
    page_cell_map = {}

    def extract_cell_positions(box, page_idx):
        sx, sy, page_h_pt = page_scales[page_idx]
        target_elt = getattr(box, 'element', None)
        if target_elt is not None and hasattr(target_elt, 'attrib'):
            prefix = target_elt.attrib.get('data-prefix')
            q = target_elt.attrib.get('data-q')
            opt = target_elt.attrib.get('data-opt')
            if prefix and q and opt:
                # Convert layout px to PDF pt, then flip y (PDF origin is bottom-left)
                cx = (box.position_x + box.width / 2.0) * sx
                cy = page_h_pt - (box.position_y + box.height / 2.0) * sy
                if page_idx not in page_cell_map:
                    page_cell_map[page_idx] = {}
                key = (prefix, q, int(opt))
                page_cell_map[page_idx][key] = (cx, cy)
        for child in getattr(box, 'children', []):
            extract_cell_positions(child, page_idx)

    for p_idx, page_box in enumerate(doc.pages):
        extract_cell_positions(page_box._page_box, p_idx)

    # 4. Add AcroForm radio widgets over PDF using pypdf
    writer = PdfWriter()
    writer.append(reader)

    acro_form = DictionaryObject()
    fields_array = ArrayObject()
    acro_form[NameObject('/Fields')] = fields_array
    writer._root_object[NameObject('/AcroForm')] = acro_form

    # Page 1: Gengo/Dokkai
    if 0 in page_cell_map:
        p1 = writer.pages[0]
        p1_annots = ArrayObject()

        gengo_qs = [str(q) for q in range(1, 76)]
        for q_str in gengo_qs:
            radio_group = DictionaryObject()
            radio_group[NameObject('/FT')] = NameObject('/Btn')
            radio_group[NameObject('/Ff')] = NumberObject(49152) # Radio + NoToggleToOff
            radio_group[NameObject('/T')] = TextStringObject(f'g_{q_str}')
            radio_group[NameObject('/V')] = NameObject('/Off')
            rg_ref = writer._add_object(radio_group)
            fields_array.append(rg_ref)

            kids = ArrayObject()
            for opt in range(1, 5):
                pos = page_cell_map[0].get(('g', q_str, opt))
                if not pos:
                    continue
                cx, cy = pos
                widget = DictionaryObject()
                widget[NameObject('/Type')] = NameObject('/Annot')
                widget[NameObject('/Subtype')] = NameObject('/Widget')
                widget[NameObject('/Parent')] = rg_ref
                widget[NameObject('/Rect')] = ArrayObject([
                    NumberObject(cx - 6.5), NumberObject(cy - 6.5),
                    NumberObject(cx + 6.5), NumberObject(cy + 6.5)
                ])
                widget[NameObject('/F')] = NumberObject(4)

                ap = DictionaryObject()
                n = DictionaryObject()
                n[NameObject(f'/{opt}')] = DictionaryObject()
                n[NameObject('/Off')] = DictionaryObject()
                ap[NameObject('/N')] = n
                widget[NameObject('/AP')] = ap
                widget[NameObject('/AS')] = NameObject('/Off')

                w_ref = writer._add_object(widget)
                kids.append(w_ref)
                p1_annots.append(w_ref)

            radio_group[NameObject('/Kids')] = kids

        p1[NameObject('/Annots')] = p1_annots

    # Page 2: Choukai
    if 1 in page_cell_map and len(writer.pages) > 1:
        p2 = writer.pages[1]
        p2_annots = ArrayObject()

        for k in choukai_list:
            radio_group = DictionaryObject()
            radio_group[NameObject('/FT')] = NameObject('/Btn')
            radio_group[NameObject('/Ff')] = NumberObject(49152)
            radio_group[NameObject('/T')] = TextStringObject(f'c_{k}')
            radio_group[NameObject('/V')] = NameObject('/Off')
            rg_ref = writer._add_object(radio_group)
            fields_array.append(rg_ref)

            kids = ArrayObject()
            for opt in range(1, 5):
                pos = page_cell_map[1].get(('c', k, opt))
                if not pos:
                    continue
                cx, cy = pos
                widget = DictionaryObject()
                widget[NameObject('/Type')] = NameObject('/Annot')
                widget[NameObject('/Subtype')] = NameObject('/Widget')
                widget[NameObject('/Parent')] = rg_ref
                widget[NameObject('/Rect')] = ArrayObject([
                    NumberObject(cx - 6.5), NumberObject(cy - 6.5),
                    NumberObject(cx + 6.5), NumberObject(cy + 6.5)
                ])
                widget[NameObject('/F')] = NumberObject(4)

                ap = DictionaryObject()
                n = DictionaryObject()
                n[NameObject(f'/{opt}')] = DictionaryObject()
                n[NameObject('/Off')] = DictionaryObject()
                ap[NameObject('/N')] = n
                widget[NameObject('/AP')] = ap
                widget[NameObject('/AS')] = NameObject('/Off')

                w_ref = writer._add_object(widget)
                kids.append(w_ref)
                p2_annots.append(w_ref)

            radio_group[NameObject('/Kids')] = kids

        p2[NameObject('/Annots')] = p2_annots

    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

    if base_pdf_temp.exists():
        base_pdf_temp.unlink()

    print(f"Created interactive PDF mark sheet: {output_pdf_path}")


def grade(gengo_keys: dict, choukai_keys: dict, user_answers: dict) -> dict:
    """
    Grading engine.
    Calculates raw scores, scaled scores (0-60 for each section), Pass/Fail, and category stats.
    """
    user_gengo = user_answers.get("言語知識_読解", {})
    user_choukai = user_answers.get("聴解", {})

    # 1. Language Knowledge (Goi & Bunpou: Q1 - Q54)
    goi_bunpou_total = 54
    goi_bunpou_correct = 0
    gengo_detail = {}

    for q in range(1, 55):
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

    # 2. Reading (Dokkai: Q55 - Q75)
    dokkai_total = 21
    dokkai_correct = 0
    for q in range(55, 76):
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
    choukai_total = len(choukai_keys) if choukai_keys else 31
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


def render_report(results: dict, test_id: str) -> str:
    """Generate Markdown grading report with detailed diagnosis."""
    summary = results["summary"]
    pass_str = "🎉 **合格 (PASS)**" if summary["passed"] else "❌ **不合格 (FAIL)**"

    lines = []
    lines.append(f"# JLPT N2 模擬試験 採点結果・弱点分析レポート ({test_id})")
    lines.append("")
    lines.append(f"## 総合判定: {pass_str}")
    lines.append("")

    if not summary["passed"]:
        reasons = []
        if not summary["overall_threshold_passed"]:
            reasons.append(f"総合点 ({summary['total_scaled_score']}点) が合格ライン (90点) に届いていません。")
        if not summary["cutoff_passed"]:
            failed_secs = [k for k, v in summary["sections"].items() if not v["passed_cutoff"]]
            reasons.append(f"基準点未達のセクションがあります: {', '.join(failed_secs)} (各セクション19点以上が必要)。")
        lines.append(f"> ⚠️ **判定理由**: {' '.join(reasons)}")
        lines.append("")

    lines.append("## 1. 得点サマリー (得点等化スケールスコア 換算)")
    lines.append("")
    lines.append("| セクション | 素点 (正解数/全問) | 換算得点 | 基準点 (足切り) | 判定 |")
    lines.append("|---|---|---|---|---|")

    for sec_name, sec_data in summary["sections"].items():
        status = "基準点クリア" if sec_data["passed_cutoff"] else "⚠️ 基準点未達"
        lines.append(
            f"| **{sec_name}** | {sec_data['raw_correct']} / {sec_data['raw_total']} | **{sec_data['scaled_score']} / 60** | {sec_data['cutoff']}点 | {status} |"
        )

    lines.append(
        f"| **総合計** | **-** | **{summary['total_scaled_score']} / 180** | **90点** | **{pass_str}** |"
    )
    lines.append("")

    lines.append("## 2. 大問別（問題形式別）詳細分析")
    lines.append("")
    lines.append("| 分野 | 問題 | 大問名 | 正解率 | 正解数 / 問題数 | 評価 |")
    lines.append("|---|---|---|---|---|---|")

    weak_areas = []
    for code, stats in results["taxonomy_stats"].items():
        pct = stats["percentage"]
        if pct >= 80:
            eval_icon = "🟢 優 (Strong)"
        elif pct >= 60:
            eval_icon = "🟡 良 (Fair)"
        else:
            eval_icon = "🔴 要強化 (Weak)"
            weak_areas.append((code, stats))

        lines.append(
            f"| {stats['section']} | **{code}** | {stats['name']} | **{pct}%** | {stats['correct']} / {stats['total']} | {eval_icon} |"
        )

    lines.append("")

    lines.append("## 3. 弱点診断と今後の学習アドバイス")
    lines.append("")
    if weak_areas:
        lines.append("以下の分野は正解率が60%未満となっています。重点的な復習を推奨します：")
        lines.append("")
        for code, stats in weak_areas:
            lines.append(f"### 📌 {stats['section']} {code}: {stats['name']} (正解率: {stats['percentage']}%)")
            if code in ["問1", "問2", "問3"]:
                lines.append("- **対策**: 『新完全マスター単語N2』『新完全マスター漢字N2』の基本語彙・訓読み・複合語の復習を徹底しましょう。")
            elif code in ["問4", "問5", "問6"]:
                lines.append("- **対策**: 語彙の文脈的意味やコロケーション（類義語・用法）の精度を高めましょう。単語カードでの例文暗記が効果的です。")
            elif code in ["問7", "問8", "問9"]:
                lines.append("- **対策**: 『新完全マスター文法N2』で機能語の接続・意味の違いおよび文章全体の論理展開（接続詞・指示語）を復習しましょう。")
            elif code in ["問10", "問11", "問12", "問13", "問14"]:
                lines.append("- **対策**: 『新完全マスター読解N2』を活用し、設問のキーワードのスキャニングおよび段落ごとの要旨把握のスキマ時間を増やしましょう。")
            elif code in ["問題1", "問題2", "問題3", "問題4", "問題5"]:
                lines.append("- **対策**: 『新完全マスター聴解N2』CD音源によるシャドーイングおよび即時応答（問題4）の定型表現・敬語表現の反復練習を行いましょう。")
            lines.append("")
    else:
        lines.append("全セクションで高い正解率を維持できています！この調子で本試験に向けて実戦問題演習を継続しましょう。")
        lines.append("")

    lines.append("## 4. 全設問解答チェック表")
    lines.append("")
    lines.append("### 言語知識・読解 (問1 〜 問75)")
    lines.append("")
    lines.append("| 問 | あなたの解答 | 正解 | 結果 | 問 | あなたの解答 | 正解 | 結果 |")
    lines.append("|---|---|---|---|---|---|---|---|")

    g_detail = results["detail_gengo"]
    for q1 in range(1, 39):
        q2 = q1 + 38
        item1 = g_detail.get(q1, {})
        item2 = g_detail.get(q2, {})

        u1 = item1.get("user", "-")
        c1 = item1.get("correct", "-")
        r1 = "✅" if item1.get("is_correct") else "❌"

        if q2 <= 75:
            u2 = item2.get("user", "-")
            c2 = item2.get("correct", "-")
            r2 = "✅" if item2.get("is_correct") else "❌"
            lines.append(f"| {q1} | {u1} | {c1} | {r1} | {q2} | {u2} | {c2} | {r2} |")
        else:
            lines.append(f"| {q1} | {u1} | {c1} | {r1} | - | - | - | - |")

    lines.append("")
    lines.append("### 聴解")
    lines.append("")
    lines.append("| 問題 | あなたの解答 | 正解 | 結果 |")
    lines.append("|---|---|---|---|")
    for k, item in results["detail_choukai"].items():
        u = item.get("user", "-")
        c = item.get("correct", "-")
        r = "✅" if item.get("is_correct") else "❌"
        lines.append(f"| {k} | {u} | {c} | {r} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Grade user responses for JLPT mock test.")
    parser.add_argument("--test-dir", required=True, help="Path to test output directory, e.g. tests/1")
    parser.add_argument("--user-answers", help="Path to user answers JSON file")
    parser.add_argument("--user-pdf", help="Path to user completed/annotated PDF file")
    parser.add_argument("--create-template", action="store_true", help="Create template user_answers.json and マークシート.html file")
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

    # Handle template creation mode
    if args.create_template:
        generate_template(gengo_keys, choukai_keys, test_path)
        sys.exit(0)

    # 2. Parse user answers directly from PDF or CLI args
    user_answers = {"言語知識_読解": {}, "聴解": {}}

    # Default to tests/<test_id>/マークシート.pdf if no specific PDF or CLI answers provided
    target_pdf = Path(args.user_pdf) if args.user_pdf else (test_path / "マークシート.pdf")

    if args.user_answers:
        ua_path = Path(args.user_answers)
        if ua_path.exists():
            loaded = json.loads(ua_path.read_text(encoding="utf-8"))
            user_answers["言語知識_読解"].update(loaded.get("言語知識_読解", {}))
            user_answers["聴解"].update(loaded.get("聴解", {}))
            print(f"Loaded user answers from JSON: {ua_path}")
    elif target_pdf.exists():
        print(f"Extracting user answers from PDF: {target_pdf}...")
        user_answers = parse_user_pdf(target_pdf)
        print(f"  - Extracted {len(user_answers['言語知識_読解'])} Language/Reading answers from PDF")
        print(f"  - Extracted {len(user_answers['聴解'])} Listening answers from PDF")

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

    # 4. Save diagnostic Markdown report
    report_md = render_report(results, test_path.name)
    out_md = test_path / "採点結果.md"
    out_md.write_text(report_md, encoding="utf-8")

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
    print(f"==========================================")
    print(f"Detailed Markdown report saved to: {out_md}\n")


if __name__ == "__main__":
    main()