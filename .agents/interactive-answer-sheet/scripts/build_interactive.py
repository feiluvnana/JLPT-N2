#!/usr/bin/env python3
"""
Build the MERGED problem+answer sheet: the exam booklet itself, with a radio
bubble beside every choice, solved in a browser.

    python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/1

Writes tests/<id>/言語知識・読解_解答.html and tests/<id>/聴解_解答.html.
Click through the exam, press 「📊 採点する」, and that half is graded in the
page: the report is shown inline and saved as 採点結果_<section>.md. No JSON
round-trip. 「解答JSONも保存」 is available for grade_answers.py, which combines
both halves into the 180-point 合否.

WHY A SEPARATE FILE from 言語知識・読解.html: that is the read-only booklet
page, rebuilt by build_booklet.py. This one adds the radio bubbles, the 聴解
audio player, and the grader.

SAFETY: the answer key lives at the end of the same Markdown. Everything from
the key heading onward is TRUNCATED out of the visible document — a sheet that
shows the answers while you solve is worse than no sheet. The key IS embedded
as JS data so grading can run offline; see the skill for that trade-off.

Typography/rendering is reused verbatim from exam-booklet-generation so the
sheet looks like the booklet, not like a form.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

_spec = importlib.util.spec_from_file_location(
    "build_booklet",
    ROOT / ".agents/exam-booklet-generation/scripts/build_booklet.py")
booklet = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(booklet)
import markdown  # noqa: E402  (after booklet, which asserts its deps)

# Everything from here down is the answer key — never rendered.
KEY_HEADING = re.compile(r"^#+\s*(解答|【?正解)", re.M)

# 言語知識: `**33** …` and 問題6's `**28 募集**`
GENGO_Q = re.compile(r"^\*\*(\d{1,2})(\*\*|\s)")
# 聴解 item headings: `**1番**`, `**質問1**`, `**例**`
CHOUKAI_ITEM = re.compile(r"^\*\*(例|\d{1,2}番|質問[12])\*\*\s*$")
# 聴解 inline bubble rows: `**1番** 1 ・ 2 ・ 3 ・ 4` (可 two per line)
CHOUKAI_INLINE = re.compile(r"\*\*(例|\d{1,2}番)\*\*\s*((?:[1-4]\s*・\s*)+[1-4])")
OPTION = re.compile(r"^\s+([1-4])\.\s*(.+)$")

EXTRA_CSS = """
.qa{display:flex;flex-wrap:wrap;gap:.2em 1.1em;margin:.15em 0 .5em 1.2em}
.qa label{display:inline-flex;align-items:center;gap:.28em;cursor:pointer;
  padding:.08em .45em;border:1px solid #bbb;border-radius:999px;font-size:10pt;
  background:#fff;line-height:1.5}
.qa label:hover{background:#eef4ff;border-color:#7aa7e8}
.qa input{margin:0;cursor:pointer}
.qa input:checked+span{font-weight:700}
.qa label:has(input:checked){background:#1d4ed8;border-color:#1d4ed8;color:#fff}
.qa .qid{border:none;background:none;color:#888;font-size:9pt;padding-left:0}
.opt{display:flex;align-items:flex-start;gap:.5em;margin:.1em 0}
.opt .b{flex:0 0 auto;margin-top:.25em}
#bar{position:sticky;top:0;z-index:99;background:#111;color:#fff;
  padding:.55em .9em;display:flex;gap:1em;align-items:center;
  font-family:sans-serif;font-size:11pt}
#bar button{font-size:11pt;padding:.35em .9em;cursor:pointer;border-radius:6px;
  border:1px solid #555;background:#fff;color:#111}
#bar .grow{flex:1}
#done{font-variant-numeric:tabular-nums}
#player{position:sticky;top:2.6em;z-index:98;background:#f3f4f6;
  border-bottom:1px solid #d1d5db;padding:.5em .9em;font-family:sans-serif}
#player audio{width:100%;height:34px;display:block}
.pctl{display:flex;flex-wrap:wrap;gap:.5em .8em;align-items:center;
  margin-top:.4em;font-size:10pt}
.pctl button,.pctl select{font-size:10pt;padding:.2em .5em;cursor:pointer}
.pctl .pick{cursor:pointer;color:#1d4ed8;text-decoration:underline}
.pctl .pick input{display:none}
#player.noaudio{background:#fee2e2}
#player.noaudio::after{content:"聴解.mp3 を読み込めません。「MP3を選ぶ」から指定してください。";
  display:block;font-size:10pt;color:#991b1b;margin-top:.3em}
#result:not(:empty){margin:2em 0 4em;padding:1em 1.2em;border:2px solid #1d4ed8;
  border-radius:8px;background:#f8fafc;font-family:sans-serif}
#result pre{white-space:pre-wrap;word-break:break-word;font-size:9.5pt;
  line-height:1.65;background:#fff;border:1px solid #e2e8f0;border-radius:6px;
  padding:.9em;max-height:60vh;overflow:auto}
#result .hint{font-size:10pt;color:#475569}
@media print{#bar,#player{display:none}.qa label{border-color:#666}}
"""

PLAYER_JS = """
const au = document.getElementById('au');
function nudge(s){ au.currentTime = Math.max(0, au.currentTime + s); }
function jump(t){ if(t!=="") { au.currentTime = +t; au.play(); } }
function pick(inp){
  const f = inp.files[0];
  if (f) { au.src = URL.createObjectURL(f); au.play(); }
}
(function(){
  const sel = document.getElementById('chap'), d = window.CHAPTERS;
  if (!d || !d.chapters || !d.chapters.length){
    document.getElementById('chapwrap').style.display = 'none';
    return;
  }
  sel.insertAdjacentHTML('beforeend', '<option value="">— 選択 —</option>');
  let sec = "";
  for (const c of d.chapters){
    if (c.type === 'section'){ sec = c.label; }
    const mm = String(Math.floor(c.start/60)).padStart(2,'0');
    const ss = String(Math.floor(c.start%60)).padStart(2,'0');
    const name = c.type === 'section' ? c.label : '　' + sec + ' ' + c.label;
    sel.insertAdjacentHTML('beforeend',
      '<option value="'+c.start+'">'+name+'  ('+mm+':'+ss+')</option>');
  }
  // Keep the dropdown following playback without fighting a manual choice.
  au.addEventListener('timeupdate', ()=>{
    if (document.activeElement === sel) return;
    let cur = "";
    for (const c of d.chapters){ if (au.currentTime >= c.start - 0.2) cur = String(c.start); }
    if (cur !== sel.value) sel.value = cur;
  });
})();
au.addEventListener('error', ()=>{
  document.getElementById('player').classList.add('noaudio');
});
"""

SCRIPT = """
const KEYS = %(keys)s, SECTION = "%(section)s", TESTID = "%(testid)s";
// ANSWER_KEY / TAXONOMY / ADVICE are serialized from grade_answers.py at build
// time — the Python module is the single source of truth, so the in-page
// grader can never disagree with `make grade`.
const ANSWER_KEY = %(answer_key)s, TAXONOMY = %(taxonomy)s, ADVICE = %(advice)s;
const SECTION_DEFS = %(section_defs)s;
const LS = "jlpt:"+TESTID+":"+SECTION;

function state(){
  const o = {};
  document.querySelectorAll('input[type=radio]:checked').forEach(r=>{
    o[r.name.slice(2)] = parseInt(r.value);
  });
  return o;
}
function refresh(){
  const n = Object.keys(state()).length;
  document.getElementById('done').textContent = n + " / " + KEYS.length;
  localStorage.setItem(LS, JSON.stringify(state()));
}
function restore(){
  let o = {};
  try { o = JSON.parse(localStorage.getItem(LS) || "{}"); } catch(e){}
  for (const k in o){
    const el = document.querySelector('input[name="q_'+CSS.escape(k)+'"][value="'+o[k]+'"]');
    if (el) el.checked = true;
  }
  refresh();
}
function clearAll(){
  if (!confirm("すべての解答を消去しますか？")) return;
  document.querySelectorAll('input[type=radio]').forEach(r=>r.checked=false);
  document.getElementById('result').innerHTML = "";
  refresh();
}

// One decimal place, matching Python's round(x, 1) so the two graders'
// reports are byte-comparable.
function pct(c, t){ return (t ? Math.round(c / t * 1000) / 10 : 0).toFixed(1); }

function buildReport(ans){
  // Per-section scoring, mirroring grade(): raw -> 0-60 proportional scale,
  // 19-point cutoff. Only THIS half is graded; 合否 needs both.
  const L = [];
  L.push("# JLPT N2 模擬試験 採点結果・弱点分析レポート ("+TESTID+")");
  L.push("");
  L.push("**対象セクション: " + (SECTION==="gengo" ? "言語知識（文字・語彙・文法）・読解" : "聴解") + "**");
  L.push("");
  L.push("> このレポートはこの解答用紙の担当分のみを採点したものです。"
       + "180点満点の総合判定には両方のセクションが必要です。");
  L.push("");
  L.push("## 1. 得点サマリー (得点等化スケールスコア 換算)");
  L.push("");
  L.push("| セクション | 素点 (正解数/全問) | 換算得点 | 基準点 (足切り) | 判定 |");
  L.push("|---|---|---|---|---|");

  let sectionTotal = 0;
  for (const sd of SECTION_DEFS){
    let c = 0;
    for (const k of sd.keys){ if (ans[k] !== undefined && ans[k] === ANSWER_KEY[k]) c++; }
    const scaled = Math.round(c / sd.keys.length * 60);
    sectionTotal += scaled;
    L.push("| **"+sd.name+"** | "+c+" / "+sd.keys.length+" | **"+scaled
         +" / 60** | 19点 | "+(scaled>=19 ? "基準点クリア" : "⚠️ 基準点未達")+" |");
  }
  L.push("| **このセクション計** | **-** | **"+sectionTotal+" / "
       + (SECTION_DEFS.length*60)+"** | - | - |");
  L.push("");

  L.push("## 2. 大問別（問題形式別）詳細分析");
  L.push("");
  L.push("| 分野 | 問題 | 大問名 | 正解率 | 正解数 / 問題数 | 評価 |");
  L.push("|---|---|---|---|---|---|");
  const weak = [];
  for (const t of TAXONOMY){
    let c = 0;
    for (const k of t.keys){ if (ans[k] !== undefined && ans[k] === ANSWER_KEY[k]) c++; }
    const p = pct(c, t.keys.length);
    let icon = p >= 80 ? "🟢 優 (Strong)" : p >= 60 ? "🟡 良 (Fair)" : "🔴 要強化 (Weak)";
    if (p < 60) weak.push({code:t.code, name:t.name, section:t.section, p:p});
    L.push("| "+t.section+" | **"+t.code+"** | "+t.name+" | **"+p+"%%** | "
         + c+" / "+t.keys.length+" | "+icon+" |");
  }
  L.push("");

  L.push("## 3. 弱点診断と今後の学習アドバイス");
  L.push("");
  if (weak.length){
    L.push("以下の分野は正解率が60%%未満となっています。重点的な復習を推奨します：");
    L.push("");
    for (const w of weak){
      L.push("### 📌 "+w.section+" "+w.code+": "+w.name+" (正解率: "+w.p+"%%)");
      if (ADVICE[w.code]) L.push("- **対策**: "+ADVICE[w.code]);
      L.push("");
    }
  } else {
    L.push("このセクションでは正解率60%%未満の大問はありません。この調子で演習を継続しましょう。");
    L.push("");
  }

  L.push("## 4. 全設問解答チェック表");
  L.push("");
  L.push("| 設問 | あなたの解答 | 正解 | 判定 |");
  L.push("|---|---|---|---|");
  for (const k of KEYS){
    const u = ans[k], correct = ANSWER_KEY[k];
    const mark = u === undefined ? "— 未解答" : (u === correct ? "⭕️" : "❌");
    L.push("| "+k+" | "+(u === undefined ? "-" : u)+" | "+correct+" | "+mark+" |");
  }
  L.push("");
  return L.join("\\n");
}

function save(){
  const ans = state();
  const unanswered = KEYS.filter(k => ans[k] === undefined).length;
  if (unanswered && !confirm(unanswered+"問が未解答です。このまま採点しますか？")) return;

  const md = buildReport(ans);
  const name = "採点結果_" + (SECTION==="gengo" ? "言語知識・読解" : "聴解") + ".md";
  const blob = new Blob([md], {type:"text/markdown;charset=utf-8"});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name; a.click();

  // Also show it immediately — downloading a file you then have to go open is
  // not "grading happened".
  const box = document.getElementById('result');
  box.innerHTML = '<h2 style="margin-top:0">採点結果</h2>'
    + '<p class="hint">↓ ' + name + ' としてダウンロードしました。'
    + ' <button type="button" onclick="saveJson()">解答JSONも保存</button></p>'
    + '<pre></pre>';
  box.querySelector('pre').textContent = md;
  box.scrollIntoView({behavior:'smooth'});
}

function saveJson(){
  // Still available for `grade_answers.py`, which combines BOTH halves into a
  // single 180-point 合否 judgement.
  const payload = SECTION === "gengo"
    ? {"言語知識_読解": state(), "聴解": {}}
    : {"言語知識_読解": {}, "聴解": state()};
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type:"application/json"});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = "user_answers_" + SECTION + ".json";
  a.click();
}
document.addEventListener('change', e=>{ if(e.target.type==='radio') refresh(); });
window.addEventListener('DOMContentLoaded', restore);
"""


def radios(qid: str, width: int, label: str = "") -> str:
    cells = "".join(
        f'<label><input type="radio" name="q_{qid}" value="{i}">'
        f'<span>{i}</span></label>'
        for i in range(1, width + 1))
    tag = f'<span class="qid">{label}</span>' if label else ""
    return f'<div class="qa">{tag}{cells}</div>'


def strip_key(md: str, src: Path) -> str:
    m = KEY_HEADING.search(md)
    if not m:
        sys.exit(f"{src}: could not find the answer-key heading — refusing to "
                 f"build an interactive sheet that might leak answers")
    md = md[:m.start()].rstrip() + "\n"
    # The booklet header promises the key is at the end of the file. It is not,
    # in this build — drop the line rather than tell the examinee to go find it.
    md = re.sub(r"^\*\*正解と解説は、.*$\n?", "", md, flags=re.M)
    return md


def inject_gengo(md: str):
    """Radios after each question's option block. Returns (md, question ids)."""
    out, ids = [], []
    cur, width = None, 0

    def flush():
        nonlocal cur, width
        if cur and width:
            out.append(radios(cur, width))
            ids.append(cur)
        cur, width = None, 0

    for line in md.split("\n"):
        m_opt = OPTION.match(line)
        if cur and m_opt:
            width = max(width, int(m_opt.group(1)))
            out.append(line)
            continue
        if line.strip():
            flush()
        m_q = GENGO_Q.match(line)
        if m_q:
            qid = m_q.group(1)
            # 問題9 puts all four options on the stem line itself:
            #   **50** 1. こと  2. だけ  3. ばかり  4. まで
            inline = re.findall(r"(?<![^\s（(])([1-4])\.\s*\S", line[m_q.end():])
            if len(inline) >= 2:
                out.append(line)
                out.append(radios(qid, max(int(i) for i in inline)))
                ids.append(qid)
                continue
            cur, width = qid, 0
        out.append(line)
    flush()
    return "\n".join(out), ids


def inject_choukai(md: str, keys: list):
    """聴解 has two shapes: printed options (問題1/2, 問題5 3番) and bare bubble
    rows `**1番** 1 ・ 2 ・ 3 ・ 4` (問題3/4, 問題5 1番・2番). Handle both, and
    map each to the key format grade_answers.py expects."""
    out, used = [], []
    section = None
    cur, width = None, 0

    def key_for(item: str, sub: str = "") -> str | None:
        if item == "例" or section is None:
            return None
        if sub:                                   # 問題5 3番 質問1/質問2
            return f"問5-3-{sub}"
        n = re.sub(r"\D", "", item)
        return f"問{section}-{n}" if n else None

    def flush():
        nonlocal cur, width
        if cur and width:
            out.append(radios(cur, width))
            used.append(cur)
        cur, width = None, 0

    pending_three = None   # 問題5 3番: 質問1/質問2 live under `## 3番`
    for line in md.split("\n"):
        m_sec = re.match(r"^#+\s*問題([1-5])", line)
        if m_sec:
            flush()
            section = m_sec.group(1)
            pending_three = None
            out.append(line)
            continue
        if re.match(r"^#+\s*3番", line) and section == "5":
            pending_three = True

        # bare bubble rows, possibly two per line
        if CHOUKAI_INLINE.search(line):
            flush()
            parts, last = [], 0
            for m in CHOUKAI_INLINE.finditer(line):
                parts.append(line[last:m.start()])
                item = m.group(1)
                w = len(re.findall(r"[1-4]", m.group(2)))
                k = key_for(item)
                if k:
                    parts.append(f"**{item}** " + radios(k, w))
                    used.append(k)
                else:
                    parts.append(m.group(0))     # 例: leave as printed text
                last = m.end()
            parts.append(line[last:])
            out.append("".join(parts))
            continue

        m_opt = OPTION.match(line)
        if cur and m_opt:
            width = max(width, int(m_opt.group(1)))
            out.append(line)
            continue
        if line.strip():
            flush()
        m_item = CHOUKAI_ITEM.match(line.strip())
        if m_item:
            lbl = m_item.group(1)
            if lbl.startswith("質問") and pending_three:
                cur, width = key_for("3番", lbl[-1]), 0
            else:
                cur, width = key_for(lbl), 0
        out.append(line)
    flush()
    return "\n".join(out), used


def player_html(d: Path) -> str:
    """Audio player for the 聴解 sheet: play the exam while answering it.

    The MP3 is referenced RELATIVELY (聴解.mp3, same folder) rather than
    embedded — a ~30 MB file base64-inlined would be ~40 MB of HTML. Some
    browsers refuse file:// media subresources, so a manual file picker is
    offered as a fallback; it never depends on a server.
    """
    chapters = d / "聴解_チャプター.json"
    data = "null"
    if chapters.is_file():
        data = chapters.read_text(encoding="utf-8")
    return (
        '<div id="player">'
        '<audio id="au" controls preload="metadata" src="聴解.mp3"></audio>'
        '<div class="pctl">'
        '<button type="button" onclick="nudge(-10)">◀ 10秒</button>'
        '<button type="button" onclick="nudge(10)">10秒 ▶</button>'
        '<label>速度 <select id="rate" onchange="au.playbackRate=+this.value">'
        '<option>0.75</option><option selected>1</option>'
        '<option>1.25</option><option>1.5</option></select></label>'
        '<span id="chapwrap">章 <select id="chap" onchange="jump(this.value)">'
        '</select></span>'
        '<label class="pick">MP3を選ぶ'
        '<input type="file" accept="audio/*" onchange="pick(this)"></label>'
        '</div>'
        f'<script>window.CHAPTERS = {data};</script>'
        '</div>')


def grading_data(gam, section: str, keys: list, answer_key: dict):
    """Serialize grade_answers.py's own taxonomy/advice/cutoffs for the page."""
    if section == "gengo":
        tax = [{"code": c, "name": s["name"], "section": s["section"],
                "keys": [str(q) for q in range(s["range"][0], s["range"][1] + 1)]}
               for c, s in gam.GENGO_QUESTION_TAXONOMY.items()]
        section_defs = [
            {"name": "言語知識（文字・語彙・文法）",
             "keys": [str(q) for q in range(1, 55)]},
            {"name": "読解", "keys": [str(q) for q in range(55, 76)]},
        ]
    else:
        tax = [{"code": c, "name": s["name"], "section": s["section"],
                "keys": [k for k in keys
                         if k.startswith("問" + c.replace("問題", "") + "-")]}
               for c, s in gam.CHOUKAI_QUESTION_TAXONOMY.items()]
        section_defs = [{"name": "聴解", "keys": list(keys)}]
    tax = [t for t in tax if t["keys"]]
    return {
        "answer_key": json.dumps({str(k): v for k, v in answer_key.items()},
                                 ensure_ascii=False),
        "taxonomy": json.dumps(tax, ensure_ascii=False),
        "advice": json.dumps(gam.ADVICE_FOR, ensure_ascii=False),
        "section_defs": json.dumps(section_defs, ensure_ascii=False),
    }


def render(md: str, src: Path, section: str, testid: str, keys: list,
           title: str, out_path: Path, gdata: dict, player: str = ""):
    md = "\n".join(booklet.widen(l) for l in md.splitlines())
    body = markdown.markdown(md, extensions=["tables", "nl2br"])
    body = booklet.mark_furigana_blocks(booklet.fit_ruby(body))
    bar = (f'<div id="bar"><b>{title}</b>'
           f'<span class="grow"></span>'
           f'<span>解答済み <b id="done">0 / 0</b></span>'
           f'<button onclick="clearAll()">消去</button>'
           f'<button onclick="save()">📊 採点する</button></div>')
    js = SCRIPT % {"keys": json.dumps(keys, ensure_ascii=False),
                   "section": section, "testid": testid, **gdata}
    out_path.write_text(
        f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title><style>{booklet.CSS}{EXTRA_CSS}</style></head>'
        f'<body>{bar}{player}{body}<div id="result"></div>'
        f'<script>{js}{PLAYER_JS if player else ""}</script>'
        f'</body></html>',
        encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_interactive.py tests/<test_id>")
    d = Path(sys.argv[1])
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")
    testid = d.name

    gengo_src, choukai_src = d / "言語知識・読解.md", d / "聴解.md"

    # The grader module is the single source of truth for keys, taxonomy and
    # advice; the sheet serializes ITS data so in-page grading and `make grade`
    # can never disagree.
    ga = importlib.util.spec_from_file_location(
        "ga", ROOT / ".agents/exam-answer-grading/scripts/grade_answers.py")
    gam = importlib.util.module_from_spec(ga)
    ga.loader.exec_module(gam)

    if gengo_src.is_file():
        md, ids = inject_gengo(strip_key(gengo_src.read_text(encoding="utf-8"),
                                         gengo_src))
        missing = [str(q) for q in range(1, 76) if str(q) not in ids]
        if missing:
            print(f"  warning: no radio group for question(s) {missing}")
        gkeys = gam.parse_gengo_keys(gengo_src)
        nokey = [q for q in ids if int(q) not in gkeys]
        if nokey:
            print(f"  warning: no answer key for question(s) {nokey} — "
                  f"they cannot be graded")
        out = d / "言語知識・読解_解答.html"
        render(md, gengo_src, "gengo", testid, ids,
               f"N2 言語知識・読解 ({testid})", out,
               grading_data(gam, "gengo", ids, gkeys))
        print(f"  {out}  ({len(ids)} questions, grades in-page)")

    if choukai_src.is_file():
        ckeys = gam.parse_choukai_keys(choukai_src)
        want = list(ckeys.keys())

        md, used = inject_choukai(
            strip_key(choukai_src.read_text(encoding="utf-8"), choukai_src), want)
        missing = [k for k in want if k not in used]
        extra = [k for k in used if k not in want]
        if missing:
            print(f"  warning: no radio group for {missing}")
        if extra:
            print(f"  warning: radio group with no answer key: {extra}")
        out = d / "聴解_解答.html"
        render(md, choukai_src, "choukai", testid, used,
               f"N2 聴解 ({testid})", out,
               grading_data(gam, "choukai", used, ckeys),
               player=player_html(d))
        has_mp3 = (d / "聴解.mp3").is_file()
        chap = d / "聴解_チャプター.json"
        note = "player" + ("" if has_mp3 else ", MP3 MISSING") + \
               (", chapters" if chap.is_file() else ", no chapter marks — "
                "re-run make_choukai_mp3.py to generate them")
        print(f"  {out}  ({len(used)} items, {note})")


if __name__ == "__main__":
    main()
