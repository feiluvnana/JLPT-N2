#!/usr/bin/env python3
"""
Build the COMBINED problem+answer sheet: the full exam booklet (言語知識・読解 and 聴解)
merged into a single interactive file solved in a browser.

    python3 .agents/exam-app/scripts/build_interactive.py tests/1

Writes tests/<id>/解答.html — screens 2 and 3 of the unified server (`make serve`):
the exam itself, and the result view it switches to on 「採点する」. The whole
180-point exam is graded in the page; the structured result is saved as
採点結果.json along with ユーザー解答.json directly into tests/<id>/.

SAFETY: answer keys live at the end of the source Markdowns. Everything from the
key heading onward is TRUNCATED out of the rendered document — keys are embedded
only as JS data for offline in-page grading.

    python3 .agents/exam-app/scripts/build_interactive.py tests/1 --keyless

The same truncation, with no keys embedded anywhere: writes qa/1/keyless.md, the
full 101-question paper (+ 聴解スクリプト.txt) for `exam-qa-review`'s blind
solve. See build_keyless() for why that mode lives in this script.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# The localStorage backend (GitHub Pages) — one implementation, shared with the
# static test list. See local_store.py for why the backend is chosen at BUILD
# time rather than sniffed at runtime.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import local_store  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "build_booklet",
    ROOT / ".agents/exam-app/scripts/build_booklet.py")
booklet = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(booklet)

_style_spec = importlib.util.spec_from_file_location(
    "app_style", Path(__file__).resolve().with_name("app_style.py"))
app_style = importlib.util.module_from_spec(_style_spec)
_style_spec.loader.exec_module(app_style)

import markdown  # noqa: E402  (after booklet, which asserts its deps)

# Everything from here down is the answer key — never rendered.
KEY_HEADING = re.compile(r"^#+\s*(解答|【?正解)", re.M)

# 言語知識: `**33** …` and 問題6's `**28 募集**`
GENGO_Q = re.compile(r"^\*\*(\d{1,2})(\*\*|\s)")
# 聴解 item headings: `**1番**`, `**質問1**`, `**例**`
CHOUKAI_ITEM = re.compile(r"^\*\*(例|\d{1,2}番|質問[12])\*\*\s*$")
# 聴解 inline bubble rows: `**1番** 1 ・ 2 ・ 3 ・ 4` (可 two per line).
# 質問1/質問2 take this form too: 問題5 prints nothing for either of its items,
# so 2番's two questions are bubble rows exactly like 問題3/4's items, not the
# `**質問1**` + option-list shape CHOUKAI_ITEM handles.
CHOUKAI_INLINE = re.compile(
    r"\*\*(例|\d{1,2}番|質問[12])\*\*\s*((?:[1-4]\s*・\s*)+[1-4])")
OPTION = re.compile(r"^\s+([1-4])\.\s*(.+)$")
# 例 answers pre-marked on the 解答用紙 grid: `| 1 **(2)** 3 4 | …`
EXAMPLE_PREMARK = re.compile(r"\*\*[（(]([1-4])[)）]\*\*")
# Options numbered inside a line: ` 1. あ　2. い　3. う　4. え`. The lookbehind
# keeps 「（1）」-style references in prose from counting as options.
INLINE_OPT = re.compile(r"(?<![^\s（(])([1-4])\.\s*\S")


def option_run(text: str) -> int | None:
    """How many options this ONE line lists, when it lists several.

    問題1-8 print all four choices on a single line (question-authoring's
    horizontal layout). `OPTION` only reports the FIRST number on such a line,
    so keying the radio count off it emitted a single bubble and made every
    horizontally-laid-out question unanswerable except by choosing 1 — a real
    bug that shipped in every version of the sheet. Only accept a consecutive
    run 1..k so a decimal in option text (`1. 価格が3.5倍…`) is not miscounted.
    """
    nums = [int(n) for n in INLINE_OPT.findall(text)]
    if len(nums) >= 2 and nums == list(range(1, len(nums) + 1)):
        return len(nums)
    return None

# The chrome shared with screen 1 (the test list) lives in app_style.py — see the
EXTRA_CSS = app_style.APP_CSS + """
html.is-result-mode #screen-exam{display:none!important}
html.is-result-mode #screen-result{display:block!important}
html.is-result-mode #bar-controls{display:none!important}
html.is-result-mode #where{display:none!important}
.qa{display:flex;flex-wrap:wrap;gap:.25em 1.1em;margin:.25em 0 .65em 1.2em}
.qa label{display:inline-flex;align-items:center;gap:.32em;cursor:pointer;
  padding:.15em .6em;border:1px solid #cbd5e1;border-radius:9999px;font-size:10pt;
  background:#ffffff;line-height:1.5;transition:all .15s ease}
.qa label:hover{background:#eff6ff;border-color:#93c5fd}
.qa input{margin:0;cursor:pointer}
.qa input:checked+span{font-weight:700}
.qa label:has(input:checked){background:#2563eb;border-color:#2563eb;color:#ffffff;
  font-weight:700;box-shadow:0 2px 6px rgba(37,99,235,0.25)}
.qa .qid{border:none;background:none;color:#64748b;font-size:9pt;padding-left:0}
/* The 例 row is shown, not answerable — its answer is already marked, because
   the announcer says 「解答用紙の問題◯の例のところを見てください」. */
.qa.ex .mark{display:inline-flex;align-items:center;justify-content:center;
  min-width:2em;padding:.12em .6em;border:1px solid #cbd5e1;border-radius:9999px;
  font-size:10pt;background:#ffffff;line-height:1.5;color:#64748b}
.qa.ex .mark.on{background:#0f172a;border-color:#0f172a;color:#ffffff;font-weight:700}
.opt{display:flex;align-items:flex-start;gap:.5em;margin:.15em 0}
.opt .b{flex:0 0 auto;margin-top:.25em}
#done{font-variant-numeric:tabular-nums}
#player{position:sticky;top:3.4em;z-index:98;background:#1e293b;color:#ffffff;
  border-bottom:1px solid rgba(255,255,255,0.1);
  padding:.9em 1.2em;font-family:var(--ui);box-shadow:0 4px 12px rgba(0,0,0,0.1)}
#player audio{width:100%;height:36px;display:block}
.pctl{display:flex;flex-wrap:wrap;gap:.6em .9em;align-items:center;
  margin-top:.7em;font-size:9.5pt}
.pctl button,.pctl select{font-size:9.5pt;padding:.25em .65em;cursor:pointer;
  border-radius:6px;border:1px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.1);
  color:#ffffff;font-family:var(--ui);transition:all .15s ease}
.pctl button:hover,.pctl select:hover{background:rgba(255,255,255,0.2)}
.pctl select option{background:#1e293b;color:#ffffff}
.pctl .pick{cursor:pointer;color:#93c5fd;text-decoration:none;font-weight:700}
.pctl .pick:hover{text-decoration:underline}
.pctl .pick input{display:none}
#player.noaudio{background:#fef2f2;color:#991b1b;border-color:#fca5a5}
#player.noaudio::after{content:"聴解.mp3 を読み込めません。「MP3を選ぶ」から指定してください。";
  display:block;font-size:9.5pt;color:#991b1b;margin-top:.3em}
.section-divider{margin:3.5em 0;border:0;border-top:2px dashed #cbd5e1}
.section-title{font-size:15pt;font-weight:800;background:linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color:#ffffff;padding:.55em 1em;margin:2em 0 1.2em;border-radius:8px;
  box-shadow:0 2px 8px rgba(0,0,0,0.06)}
/* Screen 3 — the result view the sheet switches to on 採点する. Screen 1 is the
   test list served by serve_sheet.py; screen 2 is #screen-exam above. Both reuse
   APP_CSS above, so the three screens share one look. */
#screen-result{display:none;font-family:var(--ui);color:var(--ink);margin:1.4em 0 4em}
/* The result screen is app UI, not exam paper: undo the booklet's heading
   chrome (the gray 問題 bars, the ruled rules) so it matches screen 1. */
#screen-result h1,#screen-result h2,#screen-result h3{background:none;border:0;
  padding:0;color:var(--ink);font-family:var(--ui)}
#screen-result h1{font-size:16pt;font-weight:900;margin:.2em 0 .6em;color:#0f172a}
#screen-result h2{font-size:13pt;font-weight:800;margin:2em 0 .6em;border-bottom:2px solid #e2e8f0;
  padding-bottom:.35em;color:#1e293b}
#screen-result h3{font-size:11pt;font-weight:700;margin:1.4em 0 .4em;color:var(--muted)}
.rs-nav{display:flex;flex-wrap:wrap;gap:.6em;align-items:center;margin:2.5em 0 0;
  padding-top:1.4em;border-top:1px solid #e2e8f0}
.rs-head{display:flex;flex-wrap:wrap;gap:1em;align-items:center;padding:1.25em 1.5em;
  border-radius:10px;border:2px solid;box-shadow:0 2px 10px rgba(0,0,0,0.03)}
.rs-head.pass{background:#ecfdf5;border-color:#10b981}
.rs-head.fail{background:#fef2f2;border-color:#ef4444}
.rs-verdict{font-size:18pt;font-weight:900}
.rs-head.pass .rs-verdict{color:#065f46}
.rs-head.fail .rs-verdict{color:#991b1b}
.rs-score{font-size:26pt;font-weight:900;font-variant-numeric:tabular-nums;margin-left:auto}
.rs-score small{font-size:11pt;font-weight:500;color:var(--muted)}
.rs-why{flex-basis:100%;font-size:10.5pt;color:var(--muted);margin:0;line-height:1.6}
.rs-saved{font-size:9.5pt;color:var(--muted);margin:.3em 0 1.2em}
.rs-saved.ok{color:#059669;font-weight:700}
.rs-advice{border-left:4px solid #f59e0b;background:#fffbeb;padding:.8em 1.1em;
  margin:.8em 0;font-size:10.5pt;border-radius:0 6px 6px 0;line-height:1.6}
.rs-advice b{display:block;margin-bottom:.3em;color:#92400e}
.rs-grid{display:flex;flex-wrap:wrap;gap:.35em;margin:.6em 0 1.4em}
.rs-check-tools{display:flex;flex-wrap:wrap;gap:.6em;align-items:center;
  margin:.3em 0 .8em}
.rs-hint{font-size:9.5pt;color:var(--muted);margin:0}
.rs-all-detail{margin:.3em 0 1.6em}
.rs-all-detail[hidden]{display:none!important}
.rs-item{border:1px solid #e2e8f0;border-radius:10px;background:#ffffff;
  padding:1em 1.2em;margin:0 0 .85em;box-shadow:0 1px 3px rgba(0,0,0,0.02)}
.rs-detail-meta{display:flex;flex-wrap:wrap;gap:.5em 1.2em;align-items:center;
  font-size:10.5pt;margin:0 0 .75em}
.rs-detail-meta .tag{font-weight:700;padding:.15em .55em;border-radius:4px;
  border:1px solid}
.rs-detail-meta .tag.ok{background:#ecfdf5;border-color:#a7f3d0;color:#065f46}
.rs-detail-meta .tag.ng{background:#fef2f2;border-color:#fecaca;color:#991b1b}
.rs-detail-meta .tag.na{background:#f8fafc;border-color:var(--line);color:#64748b}
.rs-detail-body{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
  padding:.85em 1.1em;line-height:1.75;font-size:10.5pt}
.rs-detail-body .qa,.rs-detail-body input{display:none!important}
.rs-detail-body h1,.rs-detail-body h2,.rs-detail-body h3{background:none;border:0;
  padding:0;margin:.35em 0 .45em;font-size:11.5pt;color:var(--ink)}
.rs-detail-note{font-size:9.5pt;color:var(--muted);margin:.65em 0 0}
.rs-group{border:1px solid #cbd5e1;border-radius:10px;background:#f1f5f9;
  padding:1em 1.2em;margin:0 0 .85em}
.rs-group-shared{margin:0 0 .85em}
.rs-group-item{margin:0 0 .6em}
.rs-group-item:last-child{margin-bottom:0}
.rs-script-label{font-size:9.5pt;font-weight:700;color:var(--muted);
  margin:0 0 .35em;letter-spacing:.02em}
.rs-script{margin:.6em 0 0;padding:.75em .95em;background:#ffffff;
  border:1px solid #e2e8f0;border-radius:8px;font-size:10pt;line-height:1.7}
.rs-script p{margin:.2em 0}
@media print{#bar,#player,.rs-nav{display:none}.qa label{border-color:#666}}
@media screen{
  body{max-width:none;margin:0;padding:0;background:#f8fafc}
  #screen-exam,#screen-result{max-width:62em;margin:1.5em auto 4em;background:#ffffff;
    border-radius:12px;border:1px solid #e2e8f0;box-shadow:0 4px 16px rgba(0,0,0,0.03);
    padding:2.5em var(--gutter) 6em}
  /* The player is chrome too, so it spans its card and sticks under the bar;
     boot() sets its offset from the bar's measured height. */
  #player{margin:.2em calc(-1 * var(--gutter)) 1em;padding:.9em var(--gutter)}
}
@media screen and (max-width:48em){
  #screen-exam,#screen-result{padding:1.2em var(--gutter) 4em;margin:0 auto;border-radius:0;border:none}
  .qa{margin:.3em 0 .8em .2em;gap:.4em .6em}
  .qa label{padding:.35em .75em;font-size:11pt;min-height:40px;min-width:40px;
    justify-content:center;box-sizing:border-box;font-weight:500}
  .qa input{width:18px;height:18px}
  #player{padding:.6em var(--gutter)}
  .pctl{gap:.4em .6em;margin-top:.5em;font-size:9.5pt}
  .pctl button,.pctl select,.pctl .pick{min-height:36px;padding:.3em .65em;
    border-radius:6px}
  .pctl select#chap{max-width:100%;flex:1 1 auto}
  .rs-head{flex-direction:column;align-items:flex-start;gap:.4em;padding:.9em 1.1em}
  .rs-score{margin-left:0;font-size:22pt}
  .rs-verdict{font-size:16pt}
  .rs-nav{flex-direction:column;align-items:stretch;gap:.6em}
  .rs-nav .ui-btn{width:100%;text-align:center;justify-content:center}
  .rs-grid{gap:.35em}
  .rs-item,.rs-group{padding:.8em .95em}
  .rs-detail-meta{gap:.3em .8em;font-size:10pt}
  .rs-detail-body{padding:.7em .85em;font-size:10pt}
  .section-title{font-size:13.5pt;padding:.4em .7em;margin:1.5em 0 .8em}
}
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
const CHOUKAI_SCRIPTS = %(choukai_scripts)s;

// Where 「← テスト一覧」 and 「テスト一覧へ戻る」 go: the unified server's root, or
// the static list two levels up on GitHub Pages (which is served from /<repo>/).
const LIST_HREF = %(list_href)s;

/* ---------------------------------------------------------------- the store
   STORAGE is baked in at build time and exactly ONE backend is live per build —
   never both, and never sniffed at runtime (see local_store.py). Two live
   stores would let the test list and this sheet disagree about what you
   answered, which is the whole reason the answers had a single home.

     'server'  make serve — tests/<id>/ユーザー解答.json + 採点結果.json on disk
     'local'   GitHub Pages / file:// — the same two documents in localStorage

   Both backends expose the same four methods, so nothing below this block
   knows which one it is talking to. */
const STORAGE = "%(storage)s";
// Routes on the unified server (serve_sheet.py, `make serve`). Opened over
// file:// these fetches simply fail and grading falls back to a download.
const API = '/api/tests/' + encodeURIComponent(TESTID) + '/';

const StoreServer = {
  async loadAnswers(){
    try {
      const r = await fetch('ユーザー解答.json', {cache: 'no-store'});
      return r.ok ? await r.json() : null;
    } catch(e){ return null; }
  },
  saveAnswers(payload){
    return fetch(API + 'answers', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({answers: payload})
    }).then(()=>{}, ()=>{ /* file:// or offline: grade download only */ });
  },
  async loadResult(){
    try {
      const r = await fetch('採点結果.json', {cache: 'no-store'});
      return r.ok ? await r.json() : null;
    } catch(e){ return null; }
  },
  async submit(payload, res){
    try {
      const r = await fetch(API + 'submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({answers: payload, result: res})
      });
      const data = r.ok ? await r.json() : null;
      if (data && data.success) return {saved: true, message: data.message};
    } catch(e){}
    return {saved: false, message: ''};
  }
};

const StoreLocal = {
  async loadAnswers(){ return window.JLPTStore.answers(TESTID); },
  saveAnswers(payload){
    window.JLPTStore.setAnswers(TESTID, payload);
    return Promise.resolve();
  },
  async loadResult(){ return window.JLPTStore.result(TESTID); },
  async submit(payload, res){
    // A full localStorage (quota) returns false, and grading then falls back to
    // the download exactly as it does with no server. Both writes are attempted
    // before the verdict — && would skip the result on a failed answers write.
    const wroteAnswers = window.JLPTStore.setAnswers(TESTID, payload);
    const wroteResult = window.JLPTStore.setResult(TESTID, res);
    return (wroteAnswers && wroteResult) ? {saved: true,
                 message: 'このブラウザに保存しました（テスト一覧に反映されます）。'}
              : {saved: false, message: ''};
  }
};

const STORE = STORAGE === 'local' ? StoreLocal : StoreServer;
// Section labels are the keys grade_answers.py uses in its own result JSON —
// the two graders write the SAME 採点結果.json shape, and make check proves it.
const SEC_GENGO = "言語知識（文字・語彙・文法）", SEC_DOKKAI = "読解", SEC_CHOUKAI = "聴解";
const EXAM_TITLE = "テスト " + TESTID + "（受験）", RESULT_TITLE = "テスト " + TESTID + "（採点結果）";

function state(){
  const o = {};
  document.querySelectorAll('input[type=radio]:checked').forEach(r=>{
    o[r.name.slice(2)] = parseInt(r.value);
  });
  return o;
}
function answersPayload(ans){
  const gengoAns = {}, choukaiAns = {};
  for (const k of GENGO_KEYS){ if (ans[k] !== undefined) gengoAns[k] = ans[k]; }
  for (const k of CHOUKAI_KEYS){ if (ans[k] !== undefined) choukaiAns[k] = ans[k]; }
  return {"言語知識_読解": gengoAns, "聴解": choukaiAns};
}
let _saveTimer = null;
function persistAnswers(ans){
  // Single source of truth, whichever backend is live: tests/<id>/ユーザー解答.json
  // under make serve, the matching localStorage key on GitHub Pages. Screen 1
  // reads that same one place back to show progress — there is never a second
  // copy. Debounced so rapid clicks do not thrash the disk.
  clearTimeout(_saveTimer);
  _saveTimer = setTimeout(()=>{ STORE.saveAnswers(answersPayload(ans)); }, 250);
}
function updateCounter(ans){
  let gCount = 0, cCount = 0;
  for (const k of GENGO_KEYS){ if (ans[k] !== undefined) gCount++; }
  for (const k of CHOUKAI_KEYS){ if (ans[k] !== undefined) cCount++; }
  const total = gCount + cCount;
  document.getElementById('done').textContent =
    "言語: " + gCount + "/" + GENGO_KEYS.length + " | 聴解: " + cCount + "/" + CHOUKAI_KEYS.length + " | 計: " + total + " / " + KEYS.length;
}
function refresh(){
  const ans = state();
  updateCounter(ans);
  persistAnswers(ans);
}
function applyAnswers(o){
  for (const k in o){
    const el = document.querySelector('input[name="q_'+CSS.escape(k)+'"][value="'+o[k]+'"]');
    if (el) el.checked = true;
  }
}
function flattenSaved(data){
  const o = {};
  if (!data || typeof data !== 'object') return o;
  const g = data["言語知識_読解"] || data.gengo || {};
  const c = data["聴解"] || data.choukai || {};
  for (const k in g){ if (g[k] !== undefined && g[k] !== null) o[k] = parseInt(g[k], 10); }
  for (const k in c){ if (c[k] !== undefined && c[k] !== null) o[k] = parseInt(c[k], 10); }
  // also accept a flat map { "33": 2, "問1-1": 1 }
  if (!Object.keys(o).length){
    for (const k in data){
      if (k === "言語知識_読解" || k === "聴解") continue;
      if (typeof data[k] === 'number' || /^\\d+$/.test(String(data[k]))) o[k] = parseInt(data[k], 10);
    }
  }
  return o;
}
async function restore(){
  const o = flattenSaved(await STORE.loadAnswers());
  applyAnswers(o);
  // Apply without re-POSTing: refresh() would persistAnswers and race the load.
  updateCounter(state());
}
function clearAll(){
  if (!confirm("すべての解答を消去しますか？")) return;
  document.querySelectorAll('input[type=radio]').forEach(r=>r.checked=false);
  refresh();
}

/* ---------------------------------------------------------------- grading
   computeResult() is the ONLY scoring path in the page and it returns DATA,
   never markup — the same object grade_answers.py builds, so 採点結果.json has
   one shape whichever grader wrote it. Keep it pure (no DOM, no Date): make
   check runs this exact function under node and compares it with the Python
   grader on identical answers. */
function computeResult(ans){
  const detailGengo = {}, detailChoukai = {};
  let goi = 0, dokkai = 0, choukai = 0;
  const maxQ = GENGO_KEYS.length;
  const goiCutoff = maxQ > 71 ? 54 : 51;

  for (let q = 1; q <= maxQ; q++){
    const k = String(q);
    const correct = ANSWER_KEY[k] === undefined ? null : ANSWER_KEY[k];
    const user = ans[k] === undefined ? null : ans[k];
    const ok = correct !== null && user !== null && user === correct;
    if (ok){ if (q <= goiCutoff) goi++; else dokkai++; }
    detailGengo[k] = {correct: correct, user: user, is_correct: ok};
  }
  for (const k of CHOUKAI_KEYS){
    const correct = ANSWER_KEY[k] === undefined ? null : ANSWER_KEY[k];
    const user = ans[k] === undefined ? null : ans[k];
    const ok = correct !== null && user !== null && user === correct;
    if (ok) choukai++;
    detailChoukai[k] = {correct: correct, user: user, is_correct: ok};
  }

  // Raw section sizes: 51/54 / 20/21 / 30/32, each scaled to 60 (JLPT equating).
  const nGoi = goiCutoff, nDokkai = maxQ - goiCutoff, nChoukai = CHOUKAI_KEYS.length || 30;
  const sGoi = Math.round((goi / nGoi) * 60);
  const sDokkai = Math.round((dokkai / nDokkai) * 60);
  const sChoukai = Math.round((choukai / nChoukai) * 60);
  const totalScaled = sGoi + sDokkai + sChoukai;
  const cutoffPassed = sGoi >= 19 && sDokkai >= 19 && sChoukai >= 19;
  const overallPassed = totalScaled >= 90;

  function sec(correct, total, scaled){
    return {raw_correct: correct, raw_total: total, scaled_score: scaled,
            cutoff: 19, passed_cutoff: scaled >= 19};
  }
  const sections = {};
  sections[SEC_GENGO] = sec(goi, nGoi, sGoi);
  sections[SEC_DOKKAI] = sec(dokkai, nDokkai, sDokkai);
  sections[SEC_CHOUKAI] = sec(choukai, nChoukai, sChoukai);

  const taxonomy = {};
  for (const t of TAXONOMY){
    let c = 0;
    for (const k of t.keys){ if (ans[k] !== undefined && ans[k] === ANSWER_KEY[k]) c++; }
    const n = t.keys.length;
    taxonomy[t.code] = {name: t.name, section: t.section, correct: c, total: n,
                        percentage: n ? Math.round((c / n) * 100 * 10) / 10 : 0};
  }

  const weak = [];
  for (const t of TAXONOMY){
    const s = taxonomy[t.code];
    if (s.percentage < 60){
      weak.push({code: t.code, name: s.name, section: s.section,
                 percentage: s.percentage, advice: ADVICE[t.code] || ""});
    }
  }

  return {
    test_id: TESTID,
    graded_at: null,
    summary: {
      passed: overallPassed && cutoffPassed,
      total_scaled_score: totalScaled,
      max_scaled_score: 180,
      cutoff_passed: cutoffPassed,
      overall_threshold_passed: overallPassed,
      sections: sections
    },
    taxonomy_stats: taxonomy,
    weak_areas: weak,
    detail_gengo: detailGengo,
    detail_choukai: detailChoukai
  };
}

/* ------------------------------------------------------- screen 3: 採点結果 */
function rating(p){ return p >= 80 ? "優 (Strong)" : p >= 60 ? "良 (Fair)" : "要強化 (Weak)"; }

function chip(label, d){
  const cls = d.user === null ? 'na' : (d.is_correct ? 'ok' : 'ng');
  const body = d.user === null ? '未解答'
             : (d.is_correct ? String(d.user) : d.user + ' → ' + d.correct);
  return '<span class="chip ' + cls + '"><i>' + label + '</i>' + body + '</span>';
}

function _isQa(el){ return !!(el && el.classList && el.classList.contains('qa')); }
function _isBreak(el){ return !!(el && (/^H[12]$/.test(el.tagName) || el.tagName === 'HR')); }
function _isUnit(el){ return !!(el && el.tagName === 'H3'); }
function _isOptLine(el){
  return !!(el && el.tagName === 'P' && /^\\s*[1-4][.．]/.test(el.textContent || ''));
}
function _looksLikeStem(el){
  if (!el || el.tagName !== 'P') return false;
  const s = el.querySelector('strong');
  if (!s) return false;
  const t = (s.textContent || '').trim();
  return /^(?:\\d{1,2}\\b|例|[1-5]番|質問\\s*[12])/.test(t);
}

/** Live exam nodes for one scored item (stem + shared passage / 問題 heading),
 *  as node REFERENCES — not yet cloned. Kept as references (not HTML) so two
 *  items whose walks converge on the same preceding nodes can be detected by
 *  reference equality, which is how shared-passage GROUPING works below.
 *  Contiguous slices are wrong: walking back to h2 would drag in every earlier
 *  item in that 問題. Collect stem nodes, then prepend passage context while
 *  skipping other questions' stems/.qa blocks. */
function extractQuestionNodes(key){
  const inp = document.querySelector(
    '#screen-exam input[name="q_' + CSS.escape(key) + '"]');
  if (!inp) return [];
  const qa = inp.closest('.qa');
  if (!qa || !qa.parentElement) return [];
  const kids = Array.from(qa.parentElement.children);
  const qi = kids.indexOf(qa);
  if (qi < 0) return [];

  const nodes = [];
  let i = qi - 1;
  while (i >= 0 && (_looksLikeStem(kids[i]) || _isOptLine(kids[i]))){
    nodes.unshift(kids[i]);
    i--;
  }
  while (i >= 0){
    const n = kids[i];
    if (_isQa(n)){
      i--;
      while (i >= 0 && (_looksLikeStem(kids[i]) || _isOptLine(kids[i]))) i--;
      continue;
    }
    if (n.tagName === 'HR') break;
    if (n.tagName === 'H1' && n.classList.contains('section-title')) break;
    if (n.tagName === 'H1' || n.tagName === 'H2'){
      nodes.unshift(n);
      break;
    }
    if (_isUnit(n)){
      nodes.unshift(n);
      break;
    }
    nodes.unshift(n);
    i--;
  }
  return nodes;
}

function nodesToHtml(nodes){
  if (!nodes.length) return '';
  const wrap = document.createElement('div');
  nodes.forEach(n => wrap.appendChild(n.cloneNode(true)));
  wrap.querySelectorAll('input, .qa').forEach(el => el.remove());
  return wrap.innerHTML;
}

function extractQuestionHtml(key){
  return nodesToHtml(extractQuestionNodes(key));
}

function escapeHtml(s){
  return String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
}

function scriptBlockHtml(text, label){
  if (!text) return '';
  const lines = text.split("\\n").map(l => l.trim()).filter(l => l.length > 0);
  const formatted = lines.map(l => '<p>' + escapeHtml(l) + '</p>').join('');
  return '<div class="rs-script"><p class="rs-script-label">🎧 ' + escapeHtml(label) + '</p>'
    + formatted + '</div>';
}

/** Two adjacent items share a passage when their node-walks converge on the
 *  SAME preceding nodes by reference — but a bare 問題1-8 item's only shared
 *  ancestor is the whole-問題 H2 (prefix length 1), which is not a passage.
 *  Require either 2+ shared nodes, or exactly 1 that is itself an H3 unit
 *  (a passage numbered (1)〜(4) with nothing else before its first
 *  question) — this is what distinguishes a real shared passage/cloze essay
 *  from every item in a 問題 just sharing that 問題's own header. */
function sharedPrefixLen(a, b){
  const n = Math.min(a.length, b.length);
  let i = 0;
  while (i < n && a[i] === b[i]) i++;
  return i;
}
function isRealSharedPrefix(nodes, len){
  if (len >= 2) return true;
  if (len === 1) return _isUnit(nodes[0]);
  return false;
}

/** Group the 71 言語知識・読解 keys by shared passage/cloze essay. Singleton
 *  groups (no sharing) are the overwhelmingly common case (問1-8, 問10). */
function computeGengoGroups(){
  const maxQ = GENGO_KEYS.length;
  const nodesByKey = {};
  for (let q = 1; q <= maxQ; q++) nodesByKey[q] = extractQuestionNodes(String(q));
  const groups = [];
  let i = 1;
  while (i <= maxQ){
    let j = i;
    while (j < maxQ && isRealSharedPrefix(
        nodesByKey[j], sharedPrefixLen(nodesByKey[j], nodesByKey[j + 1]))) j++;
    const sharedLen = j > i ? sharedPrefixLen(nodesByKey[i], nodesByKey[i + 1]) : 0;
    groups.push({
      keys: Array.from({length: j - i + 1}, (_, k) => String(i + k)),
      sharedLen, nodesByKey
    });
    i = j + 1;
  }
  return groups;
}

/** 聴解 grouping is a fixed structural fact, not a heuristic: only 問5の2番
 *  carries two sub-answers (質問1/質問2) off ONE script — every other item
 *  is already 1 script : 1 key. */
function computeChoukaiGroups(){
  const groups = [];
  const seen = new Set();
  for (const k of CHOUKAI_KEYS){
    if (seen.has(k)) continue;
    if (k === '問5-2-1' && CHOUKAI_KEYS.includes('問5-2-2')){
      groups.push({keys: ['問5-2-1', '問5-2-2'], shared: true});
      seen.add('問5-2-1'); seen.add('問5-2-2');
    } else {
      groups.push({keys: [k], shared: false});
      seen.add(k);
    }
  }
  return groups;
}

function detailMetaHtml(key, d){
  const cls = d.user === null ? 'na' : (d.is_correct ? 'ok' : 'ng');
  const verdict = d.user === null ? '未解答'
                : (d.is_correct ? '正解' : '不正解');
  const user = d.user === null ? '—' : String(d.user);
  const correct = d.correct === null || d.correct === undefined ? '—' : String(d.correct);
  return '<div class="rs-detail-meta">'
    + '<span><b>設問 ' + key + '</b></span>'
    + '<span class="tag ' + cls + '">' + verdict + '</span>'
    + '<span>あなたの答え: <b>' + user + '</b></span>'
    + '<span>正解: <b>' + correct + '</b></span>'
    + '</div>';
}

function itemDetailHtml(key, d){
  let body = extractQuestionHtml(key);
  let script = '';
  let note = '';
  const isChoukai = !/^\\d+$/.test(key);
  if (isChoukai){
    script = scriptBlockHtml(CHOUKAI_SCRIPTS[key], '聴解スクリプト');
    note = '<p class="rs-detail-note">聴解の音声は「解答に戻ってやり直す」から'
      + '受験画面のプレイヤーで確認できます。</p>';
  }
  if (!body && !isChoukai){
    body = '<p>（この設問の問題文を画面から取得できませんでした。）</p>';
  }
  const bodyBlock = body ? '<div class="rs-detail-body">' + body + '</div>' : '';
  return '<div class="rs-item" id="rs-item-' + key + '">'
    + detailMetaHtml(key, d)
    + bodyBlock + script + note
    + '</div>';
}

/** A member's own-only markup: for 言語知識・読解, the node suffix beyond the
 *  group's shared passage prefix; for 聴解, whatever the DOM has for that
 *  specific sub-key (質問1/質問2 each have their own bubble row). */
function groupMemberHtml(key, d, ownHtml){
  const isChoukai = !/^\\d+$/.test(key);
  if (!ownHtml && !isChoukai){
    ownHtml = '<p>（この設問の問題文を画面から取得できませんでした。）</p>';
  }
  const bodyBlock = ownHtml ? '<div class="rs-detail-body">' + ownHtml + '</div>' : '';
  return '<div class="rs-item rs-group-item" id="rs-item-' + key + '">'
    + detailMetaHtml(key, d)
    + bodyBlock
    + '</div>';
}

function groupHeaderLabel(keys){
  if (!keys || !keys.length) return '';
  if (keys.length === 1) return '設問 ' + keys[0];
  const first = keys[0], last = keys[keys.length - 1];
  if (/^\\d+$/.test(first)){
    let sub = '';
    if (first === '48') sub = '（問題9 文章の文法）';
    else if (first === '57') sub = '（問題11 中文 (1)）';
    else if (first === '59') sub = '（問題11 中文 (2)）';
    else if (first === '61') sub = '（問題11 中文 (3)）';
    else if (first === '63') sub = '（問題11 中文 (4)）';
    else if (first === '65') sub = '（問題12 統合理解）';
    else if (first === '67') sub = '（問題13 長文）';
    else if (first === '70') sub = '（問題14 情報検索）';
    return '設問 ' + first + ' 〜 ' + last + sub;
  }
  return '設問 ' + keys.join(' ・ ') + '（問題5 2番 共通）';
}

function gengoGroupHtml(group, detailFor){
  const { keys, sharedLen, nodesByKey } = group;
  if (keys.length === 1 || sharedLen === 0){
    return keys.map(k => itemDetailHtml(k, detailFor(k))).join('');
  }
  const title = groupHeaderLabel(keys);
  const sharedHtml = nodesToHtml(nodesByKey[keys[0]].slice(0, sharedLen));
  const members = keys.map(k =>
    groupMemberHtml(k, detailFor(k), nodesToHtml(nodesByKey[k].slice(sharedLen)))
  ).join('');
  return '<div class="rs-group">'
    + '<div class="rs-group-title">' + title + '</div>'
    + '<div class="rs-group-shared rs-detail-body">' + sharedHtml + '</div>'
    + members + '</div>';
}

function choukaiGroupHtml(group, detailFor){
  if (!group.shared){
    return itemDetailHtml(group.keys[0], detailFor(group.keys[0]));
  }
  const title = groupHeaderLabel(group.keys);
  const sharedHtml = scriptBlockHtml(
    CHOUKAI_SCRIPTS[group.keys[0]], '聴解スクリプト（質問1・質問2 共通）');
  const members = group.keys.map(k =>
    groupMemberHtml(k, detailFor(k), extractQuestionHtml(k))
  ).join('');
  return '<div class="rs-group">'
    + '<div class="rs-group-title">' + title + '</div>'
    + '<div class="rs-group-shared">' + sharedHtml
    + '<p class="rs-detail-note">聴解の音声は「解答に戻ってやり直す」から'
    + '受験画面のプレイヤーで確認できます。</p></div>'
    + members + '</div>';
}

function buildAllDetailsHtml(res){
  const L = [];
  L.push('<h3>言語知識・読解 — 設問詳細</h3>');
  for (const g of computeGengoGroups()){
    L.push(gengoGroupHtml(g, k => res.detail_gengo[k] || {}));
  }
  L.push('<h3>聴解 — 設問詳細</h3>');
  for (const g of computeChoukaiGroups()){
    L.push(choukaiGroupHtml(g, k => res.detail_choukai[k] || {}));
  }
  return L.join('');
}

function setCheckExpanded(on, res){
  const panel = document.getElementById('rs-all-detail');
  const btn = document.getElementById('rs-expand-btn');
  if (!panel || !btn) return;
  if (on){
    if (!panel.dataset.built){
      panel.innerHTML = buildAllDetailsHtml(res);
      panel.dataset.built = '1';
    }
    panel.hidden = false;
    btn.textContent = '詳細を折りたたむ';
    btn.setAttribute('aria-expanded', 'true');
  } else {
    panel.hidden = true;
    btn.textContent = 'すべての設問詳細を展開';
    btn.setAttribute('aria-expanded', 'false');
  }
}

function bindResultExpand(res){
  const btn = document.getElementById('rs-expand-btn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    setCheckExpanded(!open, res);
  });
}

function resultHtml(res, msg, saved){
  const s = res.summary, cls = s.passed ? 'pass' : 'fail';
  const L = [];

  // Screen 3 carries the same sticky #bar as screens 1 and 2, so its own
  // buttons belong at the END of the page — after the report you came to read.
  L.push('<h1>JLPT N2 模擬試験 採点結果（テスト ' + res.test_id + '）</h1>');
  L.push('<p class="rs-saved' + (saved ? ' ok' : '') + '">' + msg + '</p>');
  L.push('<div class="rs-head ' + cls + '">'
    + '<span class="rs-verdict">' + (s.passed ? '合格 (PASS)' : '不合格 (FAIL)') + '</span>'
    + '<span class="rs-score">' + s.total_scaled_score
    + ' <small>/ ' + s.max_scaled_score + '</small></span>');
  if (!s.passed){
    const why = [];
    if (!s.overall_threshold_passed){
      why.push('総合点 (' + s.total_scaled_score + '点) が合格ライン (90点) に届いていません。');
    }
    const failed = Object.keys(s.sections).filter(k => !s.sections[k].passed_cutoff);
    if (failed.length){
      why.push('基準点未達のセクションがあります: ' + failed.join('、') + ' (各19点以上が必要)。');
    }
    L.push('<p class="rs-why"><b>判定理由:</b> ' + why.join(' ') + '</p>');
  }
  L.push('</div>');

  L.push('<h2>1. 得点サマリー (得点等化スケールスコア 換算)</h2>');
  L.push('<div class="ui-table-wrap"><table class="ui-table"><thead><tr><th>セクション</th><th>素点</th><th>換算得点</th>'
    + '<th>基準点</th><th>判定</th></tr></thead><tbody>');
  for (const name in s.sections){
    const d = s.sections[name];
    L.push('<tr><td>' + name + '</td>'
      + '<td class="n">' + d.raw_correct + ' / ' + d.raw_total + '</td>'
      + '<td class="n"><b>' + d.scaled_score + '</b> / 60</td>'
      + '<td class="n">' + d.cutoff + '点</td>'
      + '<td>' + (d.passed_cutoff ? '基準点クリア' : '基準点未達') + '</td></tr>');
  }
  L.push('<tr><td><b>総合計</b></td><td class="n">-</td>'
    + '<td class="n"><b>' + s.total_scaled_score + '</b> / 180</td>'
    + '<td class="n">90点</td><td><b>'
    + (s.passed ? '合格 (PASS)' : '不合格 (FAIL)') + '</b></td></tr>');
  L.push('</tbody></table></div>');

  L.push('<h2>2. 大問別（問題形式別）詳細分析</h2>');
  L.push('<div class="ui-table-wrap"><table class="ui-table"><thead><tr><th>分野</th><th>問題</th><th>大問名</th><th>正解率</th>'
    + '<th>正解数 / 問題数</th><th>評価</th></tr></thead><tbody>');
  for (const code in res.taxonomy_stats){
    const t = res.taxonomy_stats[code];
    L.push('<tr' + (t.percentage < 60 ? ' class="weak"' : '') + '>'
      + '<td>' + t.section + '</td><td><b>' + code + '</b></td><td>' + t.name + '</td>'
      + '<td class="n">' + t.percentage.toFixed(1) + '%%</td>'
      + '<td class="n">' + t.correct + ' / ' + t.total + '</td>'
      + '<td>' + rating(t.percentage) + '</td></tr>');
  }
  L.push('</tbody></table></div>');

  L.push('<h2>3. 全設問解答チェック表</h2>');
  L.push('<div class="rs-check-tools">'
    + '<button type="button" class="ui-btn" id="rs-expand-btn" aria-expanded="false">'
    + 'すべての設問詳細を展開</button>'
    + '<p class="rs-hint">展開すると全101問の問題文・選択肢・正誤が一覧で表示されます。</p>'
    + '</div>');
  const maxQ = GENGO_KEYS.length;
  L.push('<h3>言語知識・読解 (1 〜 ' + maxQ + ')</h3><div class="rs-grid">');
  for (let q = 1; q <= maxQ; q++){ L.push(chip(String(q), res.detail_gengo[String(q)])); }
  L.push('</div><h3>聴解</h3><div class="rs-grid">');
  for (const k of CHOUKAI_KEYS){ L.push(chip(k, res.detail_choukai[k])); }
  L.push('</div>');
  L.push('<div id="rs-all-detail" class="rs-all-detail" hidden></div>');

  // On GitHub Pages the result only exists inside this browser, so the way to
  // get 採点結果.json onto a disk has to be on the screen that shows it.
  L.push('<div class="rs-nav">'
    + '<button class="ui-btn primary" onclick="goList()">← テスト一覧へ戻る</button>'
    + '<button class="ui-btn" onclick="showScreen(\\'exam\\')">解答に戻ってやり直す</button>'
    + '<button class="ui-btn" onclick="location.href=\\'模範解答.html\\'">模範解答・解説</button>'
    + (STORAGE === 'local'
        ? '<button class="ui-btn" onclick="downloadCurrent()">採点結果を保存（JSON）</button>'
        : '')
    + '</div>');

  return L.join('');
}

function goList(){ location.href = LIST_HREF; }

function showScreen(name){
  const exam = name === 'exam';
  document.documentElement.classList.remove('is-result-mode');
  document.getElementById('screen-exam').style.display = exam ? 'block' : 'none';
  document.getElementById('screen-result').style.display = exam ? 'none' : 'block';
  // The bar itself never goes away — it is the same chrome on all three screens.
  // Only the solving controls (counter, 消去, 採点する) belong to screen 2.
  document.getElementById('bar-controls').style.display = exam ? '' : 'none';
  document.getElementById('where').style.display = exam ? '' : 'none';
  document.getElementById('bar-title').textContent = exam ? EXAM_TITLE : RESULT_TITLE;
  if (exam) updateSpy();
  const audio = document.getElementById('au');
  if (!exam && audio) audio.pause();
  // Drop ?screen=result once you go back to solving, so a reload does not
  // bounce you straight back into the (now stale) result view.
  if (exam && location.search) history.replaceState(null, '', location.pathname);
  window.scrollTo(0, 0);
}

let LAST_RESULT = null;

function showResult(res, msg, saved){
  LAST_RESULT = res;
  document.getElementById('screen-result').innerHTML = resultHtml(res, msg, saved);
  bindResultExpand(res);
  showScreen('result');
}

async function save(){
  const ans = state();
  const unanswered = KEYS.filter(k => ans[k] === undefined).length;
  if (unanswered && !confirm(unanswered + "問が未解答です。このまま採点しますか？")) return;

  const res = computeResult(ans);
  res.graded_at = new Date().toISOString();

  const out = await STORE.submit(answersPayload(ans), res);
  const msg = out.saved ? '✓ ' + out.message
                        : '↓ ' + downloadResult(res, answersPayload(ans));
  showResult(res, msg, out.saved);
}

function downloadCurrent(){
  if (LAST_RESULT) downloadResult(LAST_RESULT, answersPayload(state()));
}

function downloadResult(res, answers){
  // No server (file://): hand the two files to the browser instead.
  function dl(name, obj){
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(obj, null, 2)],
                                          {type: "application/json"}));
    a.download = name; a.click();
  }
  dl("採点結果.json", res);
  dl("ユーザー解答.json", answers);
  return "採点結果.json および ユーザー解答.json としてダウンロードしました。";
}

/* --------------------------------------------------- where am I in the paper
   The bar names the section and 大問 you are currently reading, from scroll
   position: the exam is one very long page, and 「問題7」 on screen 2 tells you
   which 大問 you are in without scrolling back to its heading. */
let SPOTS = [];

function initSpy(){
  const root = document.getElementById('screen-exam');
  if (!root) return;
  SPOTS = [...root.querySelectorAll('h1,h2,h3,h4')].map(el => {
    const t = el.textContent.trim();
    if (el.classList.contains('section-title')){
      return {el: el, sec: (t.indexOf('聴解') >= 0 && t.indexOf('読解') < 0)
                            ? '聴解' : '言語知識・読解', q: null};
    }
    const m = t.match(/^問題\\s*(\\d+)/);
    return m ? {el: el, sec: null, q: '問題' + m[1]} : null;
  }).filter(Boolean);
  window.addEventListener('scroll', updateSpy, {passive: true});
  updateSpy();
}

function updateSpy(){
  const where = document.getElementById('where');
  if (!where || !SPOTS.length) return;
  const bar = document.getElementById('bar');
  const edge = (bar ? bar.offsetHeight : 0) + 8;
  let sec = '', q = '';
  for (const s of SPOTS){
    if (s.el.getBoundingClientRect().top > edge) break;
    if (s.sec){ sec = s.sec; q = ''; } else { q = s.q; }
  }
  where.textContent = sec ? (q ? sec + ' ｜ ' + q : sec) : '';
}

function fitPlayer(){
  // The player sticks directly under the bar. Measure rather than guess: the
  // bar's height depends on the font and on whether its controls wrap.
  const bar = document.getElementById('bar'), p = document.getElementById('player');
  if (bar && p && bar.offsetHeight) p.style.top = bar.offsetHeight + 'px';
}

async function boot(){
  fitPlayer();
  initSpy();
  window.addEventListener('resize', fitPlayer);
  const isResult = location.search.indexOf('screen=result') !== -1;
  if (isResult){
    showScreen('result');
    const saved = await STORE.loadResult();
    if (saved) {
      showResult(saved, '保存済みの採点結果です。', true);
    } else {
      await restore();
      showScreen('exam');
    }
  } else {
    await restore();
  }
}

document.addEventListener('change', e=>{ if(e.target.type==='radio') refresh(); });
window.addEventListener('DOMContentLoaded', boot);
"""


def example_premarks(md: str) -> dict:
    """The 例 answer pre-marked on the 解答用紙 grid, per 問題.

    `jlpt-exam-structure`: each 問題1-4 opens with a practice 例 whose answer the
    announcer declares and the answer sheet shows ALREADY MARKED — one
    demonstration, seen and heard together. The grid this reads is truncated out
    of the sheet by strip_key (the sheet has its own bubbles), so the mark has to
    be carried over here or the 例 renders as three blank circles and the
    announcement 「解答用紙の例のところを見てください」 points at nothing.

    Only the grid writes `**(n)**`; the 解説 tables write `**n**`, so the first
    match under each `問題N` heading is unambiguous.
    """
    marks, section = {}, None
    for line in md.splitlines():
        m_sec = re.match(r"^#+\s*問題([1-5])", line)
        if m_sec:
            section = m_sec.group(1)
            continue
        if section and section not in marks:
            m = EXAMPLE_PREMARK.search(line)
            if m:
                marks[section] = int(m.group(1))
    return marks


def example_row(width: int, marked) -> str:
    """The 例's bubbles — shown, not answerable: the 例 is never scored."""
    cells = "".join(
        f'<span class="mark{" on" if i == marked else ""}">{i}</span>'
        for i in range(1, width + 1))
    return f'<div class="qa ex"><span class="qid">例</span>{cells}</div>'


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
            # a single line may hold the whole 1-4 run (horizontal layout)
            width = max(width, option_run(line) or int(m_opt.group(1)))
            out.append(line)
            continue
        m_q = GENGO_Q.match(line)
        if m_q:
            flush()
            qid = m_q.group(1)
            inline = option_run(line[m_q.end():])   # 問題9's all-on-one-line stem
            if inline:
                out.append(line)
                out.append(radios(qid, inline))
                ids.append(qid)
                continue
            cur, width = qid, 0
            out.append(line)
            continue
        # Multi-line 問題7 stems (setting on its own line, then each speaker
        # turn) must NOT flush — width is still 0 until the option row.
        # Only flush once options have been seen and non-option prose resumes
        # (読解 passage after a vertical option list, etc.).
        if cur and width and line.strip():
            flush()
        out.append(line)
    flush()
    return "\n".join(out), ids


def inject_choukai(md: str, keys: list, premarks: dict | None = None):
    """聴解 has printed options and bare bubble rows. Inject radios.

    The 例 of each 問題 gets a STATIC row with its answer already marked instead
    of radios — it is a demonstration, not a scored item.
    """
    premarks = premarks or {}
    out, used = [], []
    section = None
    cur, width, ex = None, 0, None

    last_item = "2番"
    def key_for(item: str, sub: str = "") -> str | None:
        if item == "例" or section is None:
            return None
        if sub:
            item_num = re.sub(r"\D", "", item) or "2"
            return f"問5-{item_num}-{sub}"
        n = re.sub(r"\D", "", item)
        return f"問{section}-{n}" if n else None

    def flush():
        nonlocal cur, width, ex
        if width:
            if ex:
                out.append(example_row(width, premarks.get(ex)))
            elif cur:
                out.append(radios(cur, width))
                used.append(cur)
        cur, width, ex = None, 0, None

    for line in md.split("\n"):
        m_sec = re.match(r"^#+\s*問題([1-5])", line)
        if m_sec:
            flush()
            section = m_sec.group(1)
            out.append(line)
            continue

        # 問題5's 2番 (質問1/質問2) is announced only by a `## N番` sub-heading,
        # never by a bare `**N番**` item line (its own answer row is the inline
        # bubble format instead, which does not update last_item below). Track
        # these headings directly so 質問1/質問2 resolve to the right N, not to
        # whatever 番 last set last_item in an earlier 問題 (a real bug: without
        # this, 問5-2-1/問5-2-2 were emitted as 問5-6-1/問5-6-2, keyed off 問題2's
        # last item, and the two questions got no radio group at all).
        m_item5_heading = re.match(r"^#+\s*(\d+)番\s*$", line.strip())
        if section == "5" and m_item5_heading:
            last_item = f"{m_item5_heading.group(1)}番"
            out.append(line)
            continue

        if CHOUKAI_INLINE.search(line):
            flush()
            parts, last = [], 0
            for m in CHOUKAI_INLINE.finditer(line):
                parts.append(line[last:m.start()])
                item = m.group(1)
                w = len(re.findall(r"[1-4]", m.group(2)))
                # 質問N always belongs to 問題5's 2番, never to an item called
                # 「1番」: key_for("質問1") would otherwise strip the label to its
                # digit and emit 問5-1, colliding with 1番's own group and
                # leaving 質問2 unanswerable.
                k = (key_for(last_item, item[-1])
                     if item.startswith("質問") and section == "5"
                     else key_for(item))
                if k:
                    parts.append(f"**{item}** " + radios(k, w))
                    used.append(k)
                elif item == "例":
                    parts.append(example_row(w, premarks.get(section)))
                else:
                    parts.append(m.group(0))
                last = m.end()
            parts.append(line[last:])
            out.append("".join(parts))
            continue

        m_opt = OPTION.match(line)
        if (cur or ex) and m_opt:
            width = max(width, option_run(line) or int(m_opt.group(1)))
            out.append(line)
            continue
        if line.strip():
            flush()
        m_item = CHOUKAI_ITEM.match(line.strip())
        if m_item:
            lbl = m_item.group(1)
            if lbl == "例":
                cur, width, ex = None, 0, section
            elif lbl.startswith("質問") and section == "5":
                # 問題5's multi-question item carries 質問1/質問2 (jlpt-exam-structure); keys are 問5-N-1/2.
                cur, width, ex = key_for(last_item, lbl[-1]), 0, None
            else:
                if lbl.endswith("番"):
                    last_item = lbl
                cur, width, ex = key_for(lbl), 0, None
        out.append(line)
    flush()
    return "\n".join(out), used


CHOUKAI_ITEM_RE = re.compile(r"^(例。|(\d+)番。)")
CHOUKAI_SECTION_RE = re.compile(r"^問題(\d+)。$")


def parse_choukai_scripts(script_path: Path) -> dict:
    """Map each 聴解 item key (問1-1 … 問5-2-2) to its own block of
    `聴解スクリプト.txt` — the narration/dialogue/options actually spoken for
    that item. Self-contained (no `make_choukai_mp3.py` import): that module
    requires `edge_tts`, a synthesis-only dependency this read-only display
    feature must not force on anyone who only wants to view a built test.
    Key numbering mirrors `grade_answers.parse_choukai_keys()` exactly — 例
    blocks are practice items and carry no key, so they are skipped without
    incrementing the ordinal.
    """
    if not script_path.is_file():
        return {}
    text = script_path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    scripts: dict[str, str] = {}
    section = None
    ordinal = 0
    for block in blocks:
        first = block.splitlines()[0].strip()
        m = CHOUKAI_SECTION_RE.match(first)
        if m:
            section = int(m.group(1))
            ordinal = 0
            continue
        if not (section and CHOUKAI_ITEM_RE.match(first)):
            continue
        if first.startswith("例。"):
            continue  # practice item — not scored, no key to attach it to
        ordinal += 1
        if section == 5:
            item_match = CHOUKAI_ITEM_RE.match(first)
            item_num = item_match.group(2) if (item_match and item_match.group(2)) else str(ordinal)
            if "質問1" in block or "質問2" in block:
                scripts[f"問5-{item_num}-1"] = block
                scripts[f"問5-{item_num}-2"] = block
            else:
                scripts[f"問5-{item_num}"] = block
        else:
            scripts[f"問{section}-{ordinal}"] = block
    return scripts


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


def grading_data(gam, gids: list, ckeys: dict, combined_keys: dict,
                  choukai_scripts: dict | None = None):
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
        "choukai_scripts": json.dumps(choukai_scripts or {}, ensure_ascii=False),
    }


# Where the sheet's 「← テスト一覧」 points, per deployment. The unified server
# serves the list at its root; GitHub Pages serves the whole site from /<repo>/,
# where an absolute `/` would leave the site altogether, so the static build
# links relatively out of tests/<id>/.
LIST_HREF = {"server": "/", "local": "../../index.html"}


def render_combined(gengo_md: str, choukai_md: str, testid: str, keys: list,
                    out_path: Path, gdata: dict, player: str = "",
                    sources=(), storage: str = "server"):
    gengo_md = booklet.box_passages(gengo_md)
    gengo_md = "\n".join(booklet.widen(l) for l in gengo_md.splitlines())
    choukai_md = booklet.add_choukai_furigana(choukai_md)
    choukai_md = "\n".join(booklet.widen(l) for l in choukai_md.splitlines())

    gengo_body = booklet.mark_furigana_blocks(booklet.fit_ruby(markdown.markdown(gengo_md, extensions=["tables", "nl2br"])))
    gengo_body = booklet.box_passages_html(gengo_body)
    choukai_body = booklet.mark_furigana_blocks(booklet.fit_ruby(markdown.markdown(choukai_md, extensions=["tables", "nl2br"])))

    if storage not in LIST_HREF:
        raise ValueError(f"unknown storage backend: {storage}")
    list_href = LIST_HREF[storage]

    title = f"N2 模擬試験 解答用紙 ({testid})"
    # The SAME bar as screen 1's, so the app reads as one thing. Opened as a bare
    # file (no server, no Pages deployment) that link is dead, which is the same
    # trade-off as the /api/ POSTs.
    bar = (f'<div id="bar"><a class="back" href="{list_href}">← テスト一覧</a>'
           f'<b id="bar-title">テスト {testid}（受験）</b>'
           f'<span class="sub" id="where"></span>'
           f'<span class="grow"></span>'
           f'<span id="bar-controls">'
           f'<span class="sub" id="done">解答済み 0 / 101</span> '
           f'<button onclick="clearAll()">消去</button> '
           f'<button onclick="save()" class="primary">採点する</button></span></div>'
           f'<script>if(document.documentElement.classList.contains("is-result-mode")){{'
           f'document.getElementById("bar-title").textContent="テスト {testid}（採点結果）";}}</script>')

    body = (
        f'<div id="screen-exam">'
        f'<div id="section-gengo">'
        f'<h1 class="section-title">JLPT N2 言語知識（文字・語彙・文法）・読解</h1>'
        f'{gengo_body}</div>'
        f'<hr class="section-divider">'
        f'<div id="section-choukai">'
        f'<h1 class="section-title">JLPT N2 聴解</h1>'
        f'{player}{choukai_body}</div>'
        f'</div>'
    )

    js = SCRIPT % {"keys": json.dumps(keys, ensure_ascii=False), "testid": testid,
                   "storage": storage,
                   "list_href": json.dumps(list_href, ensure_ascii=False), **gdata}
    # The localStorage backend is a shared snippet, included only where it is the
    # live one — a server build must not even be able to write a second copy.
    if storage == "local":
        js = local_store.LOCAL_STORE_JS + js
    out_path.write_text(
        f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<script>if(window.location.search&&window.location.search.indexOf("screen=result")!==-1){{'
        f'document.documentElement.classList.add("is-result-mode");}}</script>'
        f'{booklet.FONT_TAGS}'
        f'<title>{title}</title>'
        # Staleness stamps for every source whose CONTENT is baked into this
        # file — the two Markdowns and, because the 聴解 scripts are embedded
        # for the result screen, 聴解スクリプト.txt. Same 12-hex sha1 convention
        # as 聴解_チャプター.json's script_sha; see booklet.src_sha_comments.
        f'{booklet.src_sha_comments(sources)}'
        f'<style>{booklet.CSS}{booklet.SCREEN_CSS}{EXTRA_CSS}</style></head>'
        f'<body>{bar}{body}<div id="screen-result"></div>'
        f'<script>{js}{PLAYER_JS if player else ""}</script>'
        f'</body></html>',
        encoding="utf-8")


# ------------------------------------------------------------- QA blind-solve
# `exam-qa-review`'s first ground rule is "blind-solve before reading the keys",
# and until this mode existed it was not executable: the keys live at the END of
# the same two Markdown files the paper lives in, so one Read returns the paper
# AND its keys. This emits the paper
# alone, through the SAME strip_key() the sheet uses — one truncation parser, so
# a key that could reach this render could also reach 解答.html, and the missing
# heading aborts both builds identically instead of silently leaking.
#
# It is NOT a deliverable: it lands in qa/<id>/ beside the QA report, never in
# tests/<id>/, whose file list is a fixed contract (AGENTS.md §2), and it is
# regenerated from tests/<id>/ on demand.
KEYLESS_DIR = ROOT / "qa"
KEYLESS_NAME = "keyless.md"

KEYLESS_HEADER = """<!-- GENERATED by build_interactive.py --keyless. Do not edit; rebuild with `make keyless {testid}`. -->

# QA blind-solve render — テスト {testid}

The full 101-question paper, and nothing else. Everything from the answer-key
heading onward in each source is truncated away by the same `strip_key()` that
protects `解答.html`, so this file carries no keys, no key tables, no marked
answer grid and no explanation column. Solve from this file alone and write your
answers down BEFORE opening anything under `tests/{testid}/`
(`exam-qa-review` §"Ground rules" → blind-solve).

Source revision this render was made from (sha1[:12] over the raw bytes — quote
these in the report header, and rebuild if they have moved when you finish):

{shas}
"""

KEYLESS_SCRIPT_HEADING = """
---

# 聴解スクリプト（音声で読み上げられる本文）

Verbatim `聴解スクリプト.txt`. It is what the MP3 speaks, so it is part of the
paper, not part of the key — solve 聴解 from here (or from the audio) exactly as
an examinee hears it.
"""


def keyless_markdown(d: Path) -> str:
    """The paper with every key, key table, marked grid and explanation gone."""
    gengo_src, choukai_src = d / "言語知識・読解.md", d / "聴解.md"
    if not gengo_src.is_file() or not choukai_src.is_file():
        sys.exit(f"Missing source markdowns in {d}")
    script_src = d / "聴解スクリプト.txt"

    sources = [p for p in (gengo_src, choukai_src, script_src) if p.is_file()]
    shas = "\n".join(f"- `{p.name}` = `{booklet.source_sha(p)}`" for p in sources)

    parts = [KEYLESS_HEADER.format(testid=d.name, shas=shas),
             "\n---\n",
             strip_key(gengo_src.read_text(encoding="utf-8"), gengo_src),
             "\n---\n",
             strip_key(choukai_src.read_text(encoding="utf-8"), choukai_src)]
    if script_src.is_file():
        parts.append(KEYLESS_SCRIPT_HEADING)
        parts.append(script_src.read_text(encoding="utf-8"))
    return "\n".join(parts)


def build_keyless(d: Path, out_dir: Path | None = None) -> Path:
    """Write qa/<test_id>/keyless.md. Returns the path written."""
    dest = out_dir if out_dir is not None else KEYLESS_DIR / d.name
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / KEYLESS_NAME
    text = keyless_markdown(d)
    out.write_text(text, encoding="utf-8")
    leaks = [m.group(0).strip() for m in KEY_HEADING.finditer(text)]
    if leaks:
        sys.exit(f"{out}: key heading survived the strip ({leaks}) — refusing to "
                 f"hand a reviewer a 'keyless' render that still carries keys")
    print(f"  {out}  ({len(text.splitlines())} lines; keys, key tables, "
          f"marked grid and 解説 stripped)")
    return out


def build(d: Path, storage: str = "server", out_dir: Path | None = None) -> Path:
    """Build one test's 解答.html. Returns the path written.

    ``storage='server'`` is the sheet solved under `make serve`; ``'local'`` is
    the GitHub Pages build, which keeps the same two documents in localStorage.
    ``out_dir`` writes the sheet somewhere other than the test folder (the Pages
    build stages into _site/) — sources are always read from ``d``.
    """
    testid = d.name

    gengo_src, choukai_src = d / "言語知識・読解.md", d / "聴解.md"
    if not gengo_src.is_file() or not choukai_src.is_file():
        sys.exit(f"Missing source markdowns in {d}")

    ga = importlib.util.spec_from_file_location(
        "ga", ROOT / ".agents/exam-app/scripts/grade_answers.py")
    gam = importlib.util.module_from_spec(ga)
    ga.loader.exec_module(gam)

    gmd, gids = inject_gengo(strip_key(gengo_src.read_text(encoding="utf-8"), gengo_src))
    gkeys = gam.parse_gengo_keys(gengo_src)

    ckeys = gam.parse_choukai_keys(choukai_src)
    craw = choukai_src.read_text(encoding="utf-8")
    cmd, cused = inject_choukai(strip_key(craw, choukai_src), list(ckeys.keys()),
                                example_premarks(craw))

    combined_keys = {**{str(k): v for k, v in gkeys.items()}, **ckeys}
    all_keys = gids + cused

    script_src = d / "聴解スクリプト.txt"
    choukai_scripts = parse_choukai_scripts(script_src)

    dest = out_dir if out_dir is not None else d
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / "解答.html"
    gdata = grading_data(gam, gids, ckeys, combined_keys, choukai_scripts)
    # 聴解_チャプター.json is stamped as a FOURTH source because player_html()
    # embeds it verbatim: a rebuilt MP3 changes every chapter offset while the
    # Markdown stays byte-identical, so without this stamp a sheet that seeks to
    # the previous build's offsets is invisible to `make check`. The 2026-08-13
    # pacing fixes moved every offset in all eight papers.
    render_combined(gmd, cmd, testid, all_keys, out, gdata, player=player_html(d),
                    sources=[gengo_src, choukai_src, script_src,
                             d / "聴解_チャプター.json"], storage=storage)

    has_mp3 = (d / "聴解.mp3").is_file()
    chap = d / "聴解_チャプター.json"
    note = "player" + ("" if has_mp3 else ", MP3 MISSING") + \
           (", chapters" if chap.is_file() else ", no chapters")
    print(f"  {out}  ({len(all_keys)} items: 71 Gengo/Dokkai, 30 Choukai; "
          f"{note}; storage={storage})")
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Build the combined problem+answer sheet (解答.html) for one test.")
    ap.add_argument("test_dir", help="tests/<test_id>")
    ap.add_argument("--storage", choices=sorted(LIST_HREF), default="server",
                    help="where answers and results are kept: 'server' writes "
                         "ユーザー解答.json/採点結果.json into the test folder via "
                         "make serve (default); 'local' keeps the same two "
                         "documents in the browser's localStorage (GitHub Pages)")
    ap.add_argument("--out", type=Path, default=None,
                    help="write the output here instead of into its default "
                         "folder (tests/<id>/ for the sheet, qa/<id>/ for "
                         "--keyless)")
    ap.add_argument("--keyless", action="store_true",
                    help="instead of the sheet, write the QA blind-solve render "
                         "qa/<test_id>/keyless.md: the full 101-question paper "
                         "plus 聴解スクリプト.txt, with every answer key and "
                         "explanation truncated away (exam-qa-review)")
    args = ap.parse_args()

    d = Path(args.test_dir)
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")
    if args.keyless:
        if args.storage != "server":
            sys.exit("--storage applies to the sheet only; --keyless has no store")
        build_keyless(d, out_dir=args.out)
        return
    build(d, storage=args.storage, out_dir=args.out)


if __name__ == "__main__":
    main()
