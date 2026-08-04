#!/usr/bin/env python3
"""
Build the COMBINED problem+answer sheet: the full exam booklet (言語知識・読解 and 聴解)
merged into a single interactive file solved in a browser.

    python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/1

Writes tests/<id>/解答.html.
Click through the full exam, press 「採点する」, and the entire 180-point exam is graded
in the page: the combined report is shown inline and saved as 採点結果.md along with
user_answers.json directly into tests/<id>/.

SAFETY: answer keys live at the end of the source Markdowns. Everything from the
key heading onward is TRUNCATED out of the rendered document — keys are embedded
only as JS data for offline in-page grading.
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
#bar button.primary{background:#1d4ed8;color:#fff;border-color:#1d4ed8;font-weight:bold}
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
.section-divider{margin:3em 0;border:0;border-top:3px double #333}
.section-title{font-size:16pt;background:#1e293b;color:#fff;padding:.4em .8em;
  margin:2em 0 1em;border-radius:4px}
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
const KEYS = %(keys)s, TESTID = "%(testid)s";
const GENGO_KEYS = %(gengo_keys)s, CHOUKAI_KEYS = %(choukai_keys)s;
const ANSWER_KEY = %(answer_key)s, TAXONOMY = %(taxonomy)s, ADVICE = %(advice)s;
const LS = "jlpt:"+TESTID+":combined_answers";

function state(){
  const o = {};
  document.querySelectorAll('input[type=radio]:checked').forEach(r=>{
    o[r.name.slice(2)] = parseInt(r.value);
  });
  return o;
}
function refresh(){
  const ans = state();
  let gCount = 0, cCount = 0;
  for (const k of GENGO_KEYS){ if (ans[k] !== undefined) gCount++; }
  for (const k of CHOUKAI_KEYS){ if (ans[k] !== undefined) cCount++; }
  const total = gCount + cCount;
  document.getElementById('done').textContent =
    "言語: " + gCount + "/75 | 聴解: " + cCount + "/32 | 計: " + total + " / " + KEYS.length;
  localStorage.setItem(LS, JSON.stringify(ans));
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

function pct(c, t){ return (t ? Math.round(c / t * 1000) / 10 : 0).toFixed(1); }

function buildReport(ans){
  // Calculate scaled scores for 3 JLPT N2 sections
  // 1. Language Knowledge (Q1-54): 54 questions -> 60 scaled
  // 2. Reading (Q55-75): 21 questions -> 60 scaled
  // 3. Listening (問1-問5): 32 items -> 60 scaled
  let gengoCorrect = 0, dokkaiCorrect = 0, choukaiCorrect = 0;
  for (let q = 1; q <= 54; q++){
    if (ans[String(q)] !== undefined && ans[String(q)] === ANSWER_KEY[String(q)]) gengoCorrect++;
  }
  for (let q = 55; q <= 75; q++){
    if (ans[String(q)] !== undefined && ans[String(q)] === ANSWER_KEY[String(q)]) dokkaiCorrect++;
  }
  for (const k of CHOUKAI_KEYS){
    if (ans[k] !== undefined && ans[k] === ANSWER_KEY[k]) choukaiCorrect++;
  }

  const scaledGengo = Math.round(gengoCorrect / 54 * 60);
  const scaledDokkai = Math.round(dokkaiCorrect / 21 * 60);
  const scaledChoukai = Math.round(choukaiCorrect / 32 * 60);
  const totalScaled = scaledGengo + scaledDokkai + scaledChoukai;

  const passedGengo = scaledGengo >= 19;
  const passedDokkai = scaledDokkai >= 19;
  const passedChoukai = scaledChoukai >= 19;
  const passedOverall = totalScaled >= 90;
  const passedTotal = passedOverall && passedGengo && passedDokkai && passedChoukai;

  const passStr = passedTotal ? "**合格 (PASS)**" : "**不合格 (FAIL)**";

  const L = [];
  L.push("# JLPT N2 模擬試験 採点結果・弱点分析レポート (" + TESTID + ")");
  L.push("");
  L.push("## 総合判定: " + passStr);
  L.push("");

  if (!passedTotal){
    const reasons = [];
    if (!passedOverall) reasons.push("総合点 (" + totalScaled + "点) が合格ライン (90点) に届いていません。");
    const failedSecs = [];
    if (!passedGengo) failedSecs.push("言語知識");
    if (!passedDokkai) failedSecs.push("読解");
    if (!passedChoukai) failedSecs.push("聴解");
    if (failedSecs.length) reasons.push("基準点未達のセクションがあります: " + failedSecs.join("、") + " (各セクション19点以上が必要)。");
    L.push("> **判定理由**: " + reasons.join(" "));
    L.push("");
  }

  L.push("## 1. 得点サマリー (得点等化スケールスコア 換算)");
  L.push("");
  L.push("| セクション | 素点 (正解数/全問) | 換算得点 | 基準点 (足切り) | 判定 |");
  L.push("|---|---|---|---|---|");
  L.push("| **言語知識 (文字・語彙・文法)** | " + gengoCorrect + " / 54 | **" + scaledGengo + " / 60** | 19点 | " + (passedGengo ? "基準点クリア" : "基準点未達") + " |");
  L.push("| **読解** | " + dokkaiCorrect + " / 21 | **" + scaledDokkai + " / 60** | 19点 | " + (passedDokkai ? "基準点クリア" : "基準点未達") + " |");
  L.push("| **聴解** | " + choukaiCorrect + " / 32 | **" + scaledChoukai + " / 60** | 19点 | " + (passedChoukai ? "基準点クリア" : "基準点未達") + " |");
  L.push("| **総合計** | **-** | **" + totalScaled + " / 180** | **90点** | **" + passStr + "** |");
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
    L.push("| " + t.section + " | **" + t.code + "** | " + t.name + " | **" + p + "%%** | " + c + " / " + t.keys.length + " | " + icon + " |");
  }
  L.push("");

  L.push("## 3. 弱点診断と今後の学習アドバイス");
  L.push("");
  if (weak.length){
    L.push("以下の分野は正解率が60%%未満となっています。重点的な復習を推奨します：");
    L.push("");
    for (const w of weak){
      L.push("### " + w.section + " " + w.code + ": " + w.name + " (正解率: " + w.p + "%%)");
      if (ADVICE[w.code]) L.push("- **対策**: " + ADVICE[w.code]);
      L.push("");
    }
  } else {
    L.push("全セクションで高い正解率を維持できています！この調子で本試験に向けて実戦問題演習を継続しましょう。");
    L.push("");
  }

  L.push("## 4. 全設問解答チェック表");
  L.push("");
  L.push("### 言語知識・読解 (問1 〜 問75)");
  L.push("");
  L.push("| 問 | あなたの解答 | 正解 | 結果 | 問 | あなたの解答 | 正解 | 結果 |");
  L.push("|---|---|---|---|---|---|---|---|");

  for (let q1 = 1; q1 <= 38; q1++){
    const q2 = q1 + 38;
    const u1 = ans[String(q1)], c1 = ANSWER_KEY[String(q1)];
    const r1 = u1 === undefined ? "-" : (u1 === c1 ? "○" : "×");
    const u1Str = u1 === undefined ? "-" : String(u1);

    if (q2 <= 75){
      const u2 = ans[String(q2)], c2 = ANSWER_KEY[String(q2)];
      const r2 = u2 === undefined ? "-" : (u2 === c2 ? "○" : "×");
      const u2Str = u2 === undefined ? "-" : String(u2);
      L.push("| " + q1 + " | " + u1Str + " | " + c1 + " | " + r1 + " | " + q2 + " | " + u2Str + " | " + c2 + " | " + r2 + " |");
    } else {
      L.push("| " + q1 + " | " + u1Str + " | " + c1 + " | " + r1 + " | - | - | - | - |");
    }
  }

  L.push("");
  L.push("### 聴解");
  L.push("");
  L.push("| 問題 | あなたの解答 | 正解 | 結果 |");
  L.push("|---|---|---|---|");
  for (const k of CHOUKAI_KEYS){
    const u = ans[k], c = ANSWER_KEY[k];
    const r = u === undefined ? "-" : (u === c ? "○" : "×");
    L.push("| " + k + " | " + (u === undefined ? "-" : u) + " | " + c + " | " + r + " |");
  }

  return L.join("\\n");
}

function renderResult(md, msg, directSaved){
  const box = document.getElementById('result');
  let statusHtml = directSaved
    ? '<span style="color:#15803d;font-weight:bold;">✓ ' + msg + '</span>'
    : '<span class="hint">↓ ' + msg + '</span>';
  box.innerHTML = '<h2 style="margin-top:0">総合採点結果</h2>'
    + '<p class="hint">' + statusHtml + '</p>'
    + '<pre></pre>';
  box.querySelector('pre').textContent = md;
  box.scrollIntoView({behavior:'smooth'});
}

function save(){
  const ans = state();
  const unanswered = KEYS.filter(k => ans[k] === undefined).length;
  if (unanswered && !confirm(unanswered + "問が未解答です。このまま採点しますか？")) return;

  const md = buildReport(ans);
  const name = "採点結果.md";
  const jsonName = "user_answers.json";
  const gengoAns = {}, choukaiAns = {};
  for (const k of GENGO_KEYS){ if (ans[k] !== undefined) gengoAns[k] = ans[k]; }
  for (const k of CHOUKAI_KEYS){ if (ans[k] !== undefined) choukaiAns[k] = ans[k]; }
  const payloadJson = {"言語知識_読解": gengoAns, "聴解": choukaiAns};

  fetch('/api/submit', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      filename: name,
      content: md,
      json_filename: jsonName,
      json_data: payloadJson
    })
  }).then(r => r.ok ? r.json() : null).then(data => {
    if (data && data.success) {
      renderResult(md, data.message, true);
    } else {
      fallbackDownload(md, name, payloadJson, jsonName);
    }
  }).catch(() => {
    fallbackDownload(md, name, payloadJson, jsonName);
  });
}

function fallbackDownload(md, name, payloadJson, jsonName){
  const blobMd = new Blob([md], {type:"text/markdown;charset=utf-8"});
  const a1 = document.createElement('a');
  a1.href = URL.createObjectURL(blobMd); a1.download = name; a1.click();

  const blobJson = new Blob([JSON.stringify(payloadJson, null, 2)], {type:"application/json"});
  const a2 = document.createElement('a');
  a2.href = URL.createObjectURL(blobJson); a2.download = jsonName; a2.click();

  renderResult(md, name + " および " + jsonName + " としてダウンロードしました。", false);
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
    """聴解 has printed options and bare bubble rows. Inject radios."""
    out, used = [], []
    section = None
    cur, width = None, 0

    def key_for(item: str, sub: str = "") -> str | None:
        if item == "例" or section is None:
            return None
        if sub:
            return f"問5-3-{sub}"
        n = re.sub(r"\D", "", item)
        return f"問{section}-{n}" if n else None

    def flush():
        nonlocal cur, width
        if cur and width:
            out.append(radios(cur, width))
            used.append(cur)
        cur, width = None, 0

    pending_three = None
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
                    parts.append(m.group(0))
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
    """Audio player for the 聴解 section."""
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


def grading_data(gam, gids: list, ckeys: dict, combined_keys: dict):
    """Serialize grade_answers.py taxonomy/advice for in-page grading."""
    tax_gengo = [{"code": c, "name": s["name"], "section": s["section"],
                  "keys": [str(q) for q in range(s["range"][0], s["range"][1] + 1)]}
                 for c, s in gam.GENGO_QUESTION_TAXONOMY.items()]
    tax_choukai = [{"code": c, "name": s["name"], "section": s["section"],
                    "keys": [k for k in ckeys
                             if k.startswith("問" + c.replace("問題", "") + "-")]}
                   for c, s in gam.CHOUKAI_QUESTION_TAXONOMY.items()]

    combined_tax = [t for t in (tax_gengo + tax_choukai) if t["keys"]]

    return {
        "gengo_keys": json.dumps(gids, ensure_ascii=False),
        "choukai_keys": json.dumps(list(ckeys.keys()), ensure_ascii=False),
        "answer_key": json.dumps({str(k): v for k, v in combined_keys.items()}, ensure_ascii=False),
        "taxonomy": json.dumps(combined_tax, ensure_ascii=False),
        "advice": json.dumps(gam.ADVICE_FOR, ensure_ascii=False),
    }


def render_combined(gengo_md: str, choukai_md: str, testid: str, keys: list,
                    out_path: Path, gdata: dict, player: str = ""):
    gengo_md = "\n".join(booklet.widen(l) for l in gengo_md.splitlines())
    choukai_md = "\n".join(booklet.widen(l) for l in choukai_md.splitlines())

    gengo_body = booklet.mark_furigana_blocks(booklet.fit_ruby(markdown.markdown(gengo_md, extensions=["tables", "nl2br"])))
    choukai_body = booklet.mark_furigana_blocks(booklet.fit_ruby(markdown.markdown(choukai_md, extensions=["tables", "nl2br"])))

    title = f"N2 模擬試験 解答用紙 ({testid})"
    bar = (f'<div id="bar"><b>{title}</b>'
           f'<span class="grow"></span>'
           f'<span><b id="done">解答済み 0 / 107</b></span>'
           f'<button onclick="clearAll()">消去</button>'
           f'<button onclick="save()" class="primary">採点する</button></div>')

    body = (
        f'<div id="section-gengo">'
        f'<h1 class="section-title">JLPT N2 言語知識（文字・語彙・文法）・読解</h1>'
        f'{gengo_body}</div>'
        f'<hr class="section-divider">'
        f'<div id="section-choukai">'
        f'<h1 class="section-title">JLPT N2 聴解</h1>'
        f'{player}{choukai_body}</div>'
    )

    js = SCRIPT % {"keys": json.dumps(keys, ensure_ascii=False), "testid": testid, **gdata}
    out_path.write_text(
        f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title><style>{booklet.CSS}{EXTRA_CSS}</style></head>'
        f'<body>{bar}{body}<div id="result"></div>'
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
    if not gengo_src.is_file() or not choukai_src.is_file():
        sys.exit(f"Missing source markdowns in {d}")

    ga = importlib.util.spec_from_file_location(
        "ga", ROOT / ".agents/exam-answer-grading/scripts/grade_answers.py")
    gam = importlib.util.module_from_spec(ga)
    ga.loader.exec_module(gam)

    gmd, gids = inject_gengo(strip_key(gengo_src.read_text(encoding="utf-8"), gengo_src))
    gkeys = gam.parse_gengo_keys(gengo_src)

    ckeys = gam.parse_choukai_keys(choukai_src)
    cmd, cused = inject_choukai(strip_key(choukai_src.read_text(encoding="utf-8"), choukai_src), list(ckeys.keys()))

    combined_keys = {**{str(k): v for k, v in gkeys.items()}, **ckeys}
    all_keys = gids + cused

    out = d / "解答.html"
    gdata = grading_data(gam, gids, ckeys, combined_keys)
    render_combined(gmd, cmd, testid, all_keys, out, gdata, player=player_html(d))

    has_mp3 = (d / "聴解.mp3").is_file()
    chap = d / "聴解_チャプター.json"
    note = "player" + ("" if has_mp3 else ", MP3 MISSING") + \
           (", chapters" if chap.is_file() else ", no chapters")
    print(f"  {out}  ({len(all_keys)} items: 75 Gengo/Dokkai, 32 Choukai; {note})")


if __name__ == "__main__":
    main()
