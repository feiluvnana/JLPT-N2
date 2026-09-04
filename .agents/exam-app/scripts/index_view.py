"""Screen 1 — the test list, ONE implementation for both deployments.

The list exists twice over: `serve_sheet.py` serves it from disk (`make serve`),
and `build_pages.py` bakes it into a static `index.html` for GitHub Pages, where
progress lives in localStorage instead. Rendering it twice in two languages is
exactly how "the same" screen drifts, so the markup lives here once, in JS, and
both deployments feed it the SAME array of test objects:

    {id, origin, answered, total, has_sheet, has_audio,
     result: {passed, total_scaled_score, max_scaled_score, graded_at} | null}

`serve_sheet.py` produces that array in Python (`progress_of()`) and hands it
over `GET /api/tests`; the Pages build bakes a manifest of the static half
(`id/origin/has_sheet/has_audio`) and the page fills in the progress half from
localStorage. Only the *source* differs — the cards, the CSS and the actions are
this file.

The cards are not a flat list: they hang under two collapsible `<details>`
groups keyed on `origin` (imported past papers vs generated mocks), both shut on
load, plus a search box that filters on id/origin and force-opens whichever
group holds a hit.

Keep it dependency-free (see app_style.py): `make serve` must start without the
authoring dependencies installed.
"""

import json
import sys
from pathlib import Path

# These scripts are run by path (`python3 .agents/…/index_view.py`) from the repo
# root, not as a package, so the sibling modules are only importable once their
# directory is on the path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import app_style      # noqa: E402
import local_store    # noqa: E402

# 71 言語知識・読解 + 30 聴解. `make check` asserts 解答.html carries exactly this
# many radio groups, so it is safe to use as the progress denominator.
QUESTION_COUNT = 101

SHEET = "解答.html"

INDEX_CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f8fafc;color:var(--ink);font-family:var(--ui)}
header.app-header{
  background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color:#fff;
  padding:1.6rem 1.4rem 1.8rem;
  box-shadow:0 4px 14px rgba(0,0,0,0.06);
}
.header-inner{
  max-width:82em;
  margin:0 auto;
}
.header-top-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
  margin-bottom:0.65rem;
  flex-wrap:wrap;
}
.header-badge{
  display:inline-block;
  background:rgba(255,255,255,0.12);
  color:#93c5fd;
  font-size:0.8rem;
  font-weight:700;
  padding:0.25rem 0.75rem;
  border-radius:9999px;
  letter-spacing:0.04em;
}
h1.title{
  font-size:1.75rem;
  font-weight:900;
  margin:0 0 0.35rem;
  color:#ffffff;
}
.subtitle{
  color:#94a3b8;
  font-size:0.92rem;
}
/* Wider than exam/result (60em): cards with many action buttons need the room. */
main{max-width:82em;margin:0 auto;padding:1.8em 1.5em 5em}
.lede{margin:0 0 1.6em;font-size:10.5pt;color:var(--muted);line-height:1.6}
/* Equal card height. Meter uses display:contents so the track shares a row with
   the status chip (left-aligned); the lbl sits on the row under the track —
   flex + align-items:center was optically centering the whole meter block and
   made the bar look offset from the chip. */
.card{display:grid;grid-template-columns:16em auto minmax(9em,1fr) auto auto;
  grid-template-rows:1fr auto;column-gap:1em;row-gap:.2em;align-items:center;
  background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:.65em 1.2em;
  margin-bottom:1em;box-sizing:border-box;height:5.4em;min-height:5.4em;
  max-height:5.4em;overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,0.03);
  transition:all .18s ease}
.card:hover{border-color:#cbd5e1;box-shadow:0 4px 14px rgba(0,0,0,0.06)}
.card h2{grid-column:1;grid-row:1/-1;margin:0;font-size:13pt;font-weight:800;min-width:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;align-self:center;color:#0f172a}
.card .origin{grid-column:2;grid-row:1/-1;align-self:center}
.card .meter{display:contents}
.card .meter .track{grid-column:3;grid-row:1;align-self:center;width:100%;min-width:0}
.card .meter .lbl{grid-column:3;grid-row:2;text-align:left;margin:0;line-height:1.2;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:9.5pt}
.card .status{grid-column:4;grid-row:1/-1;align-self:center}
.acts{grid-column:5;grid-row:1/-1;display:flex;flex-wrap:nowrap;gap:.5em;
  align-self:center}
.acts .ui-btn{padding:.4em .85em;font-size:10pt;white-space:nowrap}
.empty{background:#fff;border:1px dashed var(--line);border-radius:10px;padding:3em 2em;
  text-align:center;color:var(--muted)}
code{background:#f1f5f9;padding:.15em .45em;border-radius:4px;font-size:9.5pt;border:1px solid #e2e8f0}
.badge.origin-imp{background:#e0f2fe;color:#0369a1;border:1px solid #bae6fd}
.badge.origin-gen{background:#f1f5f9;color:#475569;border:1px solid #e2e8f0}
/* Pages-only: localStorage is the only copy of your answers, so the list owns
   the way to get them off this browser and back onto another one. */
.tools{display:flex;flex-wrap:wrap;gap:.6em;align-items:center;margin:0 0 1.6em}
.tools .note{font-size:9.5pt;color:var(--muted)}
.tools input[type=file]{display:none}
/* Search box + the two origin groups. A group is a <details>: shut until it is
   clicked, so the list opens as two lines instead of twenty cards. A live query
   force-opens whichever group holds a hit — a match hidden inside a collapsed
   group reads as "no results". */
.searchbar{display:flex;flex-wrap:wrap;gap:.6em;align-items:center;margin:0 0 1.3em}
.searchbar input{flex:1 1 18em;min-width:0;font-family:var(--ui);font-size:11pt;
  padding:.6em .9em;border:1px solid #cbd5e1;border-radius:8px;background:#fff;
  color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,0.03)}
.searchbar input:focus{outline:none;border-color:var(--accent);
  box-shadow:0 0 0 3px rgba(37,99,235,.15)}
.searchbar .hits{font-size:9.5pt;color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums}
.group{background:#fff;border:1px solid #e2e8f0;border-radius:10px;margin-bottom:1em;
  box-shadow:0 1px 3px rgba(0,0,0,0.03);overflow:hidden}
.group>summary{display:flex;align-items:center;gap:.75em;cursor:pointer;
  padding:.9em 1.2em;font-size:12pt;font-weight:800;color:#0f172a;
  list-style:none;-webkit-user-select:none;user-select:none}
.group>summary::-webkit-details-marker{display:none}
.group>summary::before{content:"▶";flex:0 0 auto;font-size:8.5pt;color:var(--muted);
  transition:transform .15s ease}
.group[open]>summary::before{transform:rotate(90deg)}
.group>summary:hover{background:#f8fafc}
.group .g-count{font-size:9.5pt;font-weight:700;color:#475569;background:#f1f5f9;
  border:1px solid #e2e8f0;border-radius:9999px;padding:.15em .7em;
  font-variant-numeric:tabular-nums}
.group .g-sub{margin-left:auto;font-size:9.5pt;font-weight:500;color:var(--muted);
  font-variant-numeric:tabular-nums}
.group .g-body{padding:.9em 1.2em 1.1em;border-top:1px solid #f1f5f9}
.group .g-body .card{margin-bottom:.8em}
.group .g-body .card:last-child{margin-bottom:0}
.group .g-empty{padding:.4em .2em;color:var(--muted);font-size:10pt}
@media screen and (max-width: 54em){
  main{padding:1.2em 1em 4em}
  .card{grid-template-columns:1fr auto;grid-template-rows:auto auto auto auto auto;
    column-gap:.8em;row-gap:.45em;height:auto;min-height:auto;max-height:none;
    padding:1em 1.1em;overflow:visible}
  .card h2{grid-column:1;grid-row:1;font-size:12.5pt;white-space:normal;overflow:visible}
  .card .origin{grid-column:2;grid-row:1;justify-self:end}
  .card .status{grid-column:1 / -1;grid-row:2;justify-self:start}
  .card .meter .track{grid-column:1 / -1;grid-row:3}
  .card .meter .lbl{grid-column:1 / -1;grid-row:4}
  .acts{grid-column:1 / -1;grid-row:5;justify-self:start;flex-wrap:wrap;
    margin-top:.4em;width:100%}
  .acts .ui-btn{padding:.45em .9em;font-size:10pt;min-height:38px}
  .tools{gap:.7em}
  .tools .ui-btn{width:100%;justify-content:center}
  .searchbar .ui-btn{min-height:38px}
  .group>summary{padding:.85em .95em;font-size:11.5pt;flex-wrap:wrap}
  .group .g-sub{margin-left:0;width:100%}
  .group .g-body{padding:.8em .95em 1em}
}
"""


# --------------------------------------------------------------- the shared view
INDEX_JS = """
var MODE = window.LIST_MODE || 'server';
var TOTAL = %(total)d, SHEET = %(sheet)s;

function esc(s){
  return String(s).replace(/[&<>"']/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}

/* -------------------------------------------------------------- the two sources
   Server: the same disk read screen 1 always did, over GET /api/tests.
   Local:  the baked manifest of what was deployed + this browser's localStorage.
   Both return the SAME array shape, so everything below is source-agnostic. */
function countAnswered(saved){
  if (!saved || typeof saved !== 'object') return 0;
  var n = 0;
  ['言語知識_読解', '聴解'].forEach(function(half){
    var o = saved[half] || {};
    for (var k in o){ if (o[k] !== null && o[k] !== undefined) n++; }
  });
  return n;
}

function localTests(){
  // Mirrors serve_sheet.progress_of(): same fields, read out of localStorage.
  return (window.PAGES_TESTS || []).map(function(t){
    var res = window.JLPTStore.result(t.id), summary = res && res.summary;
    return {
      id: t.id, origin: t.origin, total: t.total || TOTAL,
      has_sheet: t.has_sheet, has_audio: t.has_audio,
      has_explanation: t.has_explanation,
      answered: countAnswered(window.JLPTStore.answers(t.id)),
      result: summary ? {
        passed: !!summary.passed,
        total_scaled_score: summary.total_scaled_score,
        max_scaled_score: summary.max_scaled_score === undefined ? 180
                          : summary.max_scaled_score,
        graded_at: res.graded_at
      } : null
    };
  });
}

async function loadTests(){
  if (MODE === 'local') return localTests();
  var r = await fetch('/api/tests', {cache: 'no-store'});   // never a stale list
  return (await r.json()).tests || [];
}

function sheetHref(id){
  // Pages is served from a repo subpath (/<repo>/), so every link is relative.
  var base = MODE === 'local' ? 'tests/' : '/tests/';
  return base + encodeURIComponent(id) + '/' + encodeURIComponent(SHEET);
}

function explanationHref(id){
  var base = MODE === 'local' ? 'tests/' : '/tests/';
  return base + encodeURIComponent(id) + '/模範解答.html';
}

/* ------------------------------------------------------------------- the cards */
function meterHtml(t){
  var ratio = !t.total ? 0 : Math.min(100, Math.round(t.answered / t.total * 100));
  var fill = t.answered >= t.total ? 'fill done' : 'fill';
  return '<div class="meter"><div class="track">'
       + '<div class="' + fill + '" style="width:' + ratio + '%%"></div></div>'
       + '<div class="lbl">解答済み ' + t.answered + ' / ' + t.total
       + '（' + ratio + '%%）</div></div>';
}

function originBadgeHtml(t){
  return t.origin === 'imported'
    ? '<span class="badge origin-imp">imported</span>'
    : '<span class="badge origin-gen">generated</span>';
}

function badgeHtml(t){
  if (!t.has_sheet) return '<span class="badge warn">解答.html 未生成</span>';
  if (!t.result) return '<span class="badge none">未採点</span>';
  var cls = t.result.passed ? 'pass' : 'fail';
  var label = t.result.passed ? '合格' : '不合格';
  return '<span class="badge ' + cls + '">' + label + ' '
       + t.result.total_scaled_score + ' / ' + t.result.max_scaled_score + '</span>';
}

function cardHtml(t){
  var id = esc(t.id), base = sheetHref(t.id), expHref = explanationHref(t.id), acts = [];
  if (!t.has_sheet){
    acts.push('<a class="ui-btn" href="#" onclick="return false" '
            + 'title="make sheet ' + id + ' を実行">受験する</a>');
  } else if (t.result){
    // Already graded: the result view is the default destination, but the exam
    // is one click away and keeps the saved answers, so it can be redone.
    acts.push('<a class="ui-btn primary" href="' + base + '?screen=result">結果を見る</a>');
    acts.push('<a class="ui-btn" href="' + base + '">もう一度解く</a>');
  } else {
    acts.push('<a class="ui-btn primary" href="' + base + '">'
            + (t.answered ? '続きから' : '受験する') + '</a>');
  }
  if (t.has_explanation){
    acts.push('<a class="ui-btn" href="' + expHref + '">解説を見る</a>');
  }
  // Clear progress whenever either store holds something — graded or mid-exam.
  if (t.result || t.answered){
    acts.push('<button type="button" class="ui-btn danger" data-clear="' + id
            + '">結果を削除</button>');
  }
  return '<div class="card"><h2 title="テスト ' + id + '">テスト ' + id + '</h2>'
       + '<span class="origin">' + originBadgeHtml(t) + '</span>'
       + meterHtml(t)
       + '<span class="status">' + badgeHtml(t) + '</span>'
       + '<div class="acts">' + acts.join('') + '</div></div>';
}

/* ------------------------------------------------------- groups and search
   Origin already decides the badge, so it decides the grouping too — the two
   halves of tests/ (imported past papers, generated mocks) are what a reader
   actually picks between. Each group is a <details>, shut on load: twenty cards
   opened flat is a scroll, two summary lines is a choice. */
var GROUPS = [
  {key: 'imported',  label: '公式過去問（imported）',
   test: function(t){ return t.origin === 'imported'; }},
  {key: 'generated', label: '模擬試験（generated）',
   test: function(t){ return t.origin !== 'imported'; }}
];
var TESTS = [];            // last rendered list, kept by render() itself
var QUERY = '';
/* Open/shut has to survive a re-render: refreshList() runs on every pageshow,
   so a group must not snap shut on the way back from a graded exam. Only a real
   click writes here — innerHTML builds an already-open <details>, which fires
   no toggle event. */
var OPEN = {imported: false, generated: false};

function matchesQuery(t){
  if (!QUERY) return true;
  var hay = (t.id + ' ' + (t.origin || '')).toLowerCase();
  return QUERY.split(/\\s+/).every(function(w){ return !w || hay.indexOf(w) >= 0; });
}

function groupHtml(g, tests){
  var graded = tests.filter(function(t){ return t.result; }).length;
  // A live query force-opens the groups holding its hits — a match left inside
  // a collapsed group reads as "nothing found".
  var open = ((QUERY && tests.length) || OPEN[g.key]) ? ' open' : '';
  var body = tests.length
    ? tests.map(cardHtml).join('')
    : '<div class="g-empty">該当するテストはありません。</div>';
  return '<details class="group" data-group="' + g.key + '"' + open + '>'
       + '<summary><span class="g-name">' + g.label + '</span>'
       + '<span class="g-count">' + tests.length + ' 件</span>'
       + '<span class="g-sub">採点済み ' + graded + ' 件</span></summary>'
       + '<div class="g-body">' + body + '</div></details>';
}

function render(tests){
  TESTS = tests;     // the search re-renders from here — one assignment, one place
  var shown = tests.filter(matchesQuery);
  var body = tests.length
    ? GROUPS.map(function(g){ return groupHtml(g, shown.filter(g.test)); }).join('')
    : '<div class="empty">tests/ にテストがありません。'
      + '<code>make sheet &lt;test_id&gt;</code> で解答用紙を生成してください。</div>';
  document.getElementById('cards').innerHTML = body;
  var graded = tests.filter(function(t){ return t.result; }).length;
  document.getElementById('counts').textContent =
    'テスト ' + tests.length + ' 件 / 採点済み ' + graded + ' 件';
  var hits = document.getElementById('hits');
  if (hits) hits.textContent = QUERY ? shown.length + ' 件が一致' : '';
}

function setQuery(v){
  QUERY = String(v || '').trim().toLowerCase();
  render(TESTS);
}

async function refreshList(){
  try { render(await loadTests()); }
  catch (e){
    document.getElementById('cards').innerHTML =
      '<div class="empty">テスト一覧を読み込めませんでした: ' + esc(e) + '</div>';
  }
}

/* ------------------------------------------------------------------- actions */
async function clearTestProgress(id){
  if (!confirm('テスト「' + id + '」の採点結果と保存済みの解答を削除しますか？\\n'
             + 'この操作は元に戻せません。')) return;
  if (MODE === 'local'){
    window.JLPTStore.clear(id);
    return refreshList();
  }
  try {
    var r = await fetch('/api/tests/' + encodeURIComponent(id) + '/clear', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'
    });
    var data = await r.json();
    if (!r.ok || !data.success){
      alert((data && data.error) || '削除に失敗しました。');
      return;
    }
    refreshList();
  } catch (e){
    alert('削除に失敗しました: ' + e);
  }
}

/* Pages has no disk, so the list is where answers leave and re-enter the
   browser: one JSON holding every test's 解答 and 採点結果. */
function exportAll(){
  var out = {};
  (window.PAGES_TESTS || []).map(function(t){ return t.id; })
    .concat(window.JLPTStore.ids())
    .forEach(function(id){
      if (out[id]) return;
      var a = window.JLPTStore.answers(id), r = window.JLPTStore.result(id);
      if (a || r) out[id] = {"ユーザー解答.json": a, "採点結果.json": r};
    });
  if (!Object.keys(out).length){ alert('保存された解答はありません。'); return; }
  var a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)],
                                        {type: 'application/json'}));
  a.download = 'jlpt-解答バックアップ.json';
  a.click();
}

function importAll(input){
  var f = input.files && input.files[0];
  if (!f) return;
  var reader = new FileReader();
  reader.onload = function(){
    var data;
    try { data = JSON.parse(reader.result); }
    catch (e){ alert('JSON を読み込めませんでした: ' + e); return; }
    var n = 0;
    for (var id in data){
      var rec = data[id] || {};
      if (rec['ユーザー解答.json']) window.JLPTStore.setAnswers(id, rec['ユーザー解答.json']);
      if (rec['採点結果.json']) window.JLPTStore.setResult(id, rec['採点結果.json']);
      n++;
    }
    input.value = '';
    alert(n + ' 件のテストを読み込みました。');
    refreshList();
  };
  reader.readAsText(f);
}

document.addEventListener('click', function(ev){
  var el = ev.target;
  if (!el || !el.closest) return;
  var btn = el.closest('[data-clear]');
  if (btn){ clearTestProgress(btn.getAttribute('data-clear')); return; }
  if (el.closest('#q-clear')){
    var box = document.getElementById('q');
    if (box){ box.value = ''; box.focus(); }
    setQuery('');
  }
});
document.addEventListener('input', function(ev){
  if (ev.target && ev.target.id === 'q') setQuery(ev.target.value);
});
// `toggle` does not bubble — capture it, and record only what the user clicked.
document.addEventListener('toggle', function(ev){
  var d = ev.target;
  if (d && d.classList && d.classList.contains('group')){
    OPEN[d.getAttribute('data-group')] = d.open;
  }
}, true);
// The list must be live: coming back from a graded exam has to show the score.
window.addEventListener('pageshow', refreshList);
"""


def index_js() -> str:
    return INDEX_JS % {"total": QUESTION_COUNT, "sheet": json.dumps(SHEET, ensure_ascii=False)}


GROUP_NOTE = ('テストは<b>公式過去問（imported）</b>と<b>模擬試験（generated）</b>の'
              '2グループに分かれています。見出しをクリックすると開きます。'
              '検索欄に入力すると、一致したテストを含むグループが自動で開きます。')

LEDE_SERVER = ('受験するテストを選んでください。'
               '解答は選択するたびに保存され、採点結果は 採点結果.json に残ります。'
               '「結果を削除」で採点結果と解答の両方を消せます。<br>' + GROUP_NOTE)
LEDE_LOCAL = ('受験するテストを選んでください。解答と採点結果は'
              '<b>このブラウザ内（localStorage）にのみ</b>保存されます。'
              '別の端末やブラウザには引き継がれず、閲覧データを消去すると失われるため、'
              '残しておきたい結果は「バックアップを保存」で書き出してください。<br>'
              + GROUP_NOTE)

# Static shell, outside #cards: re-rendering the list must not blow away the box
# the user is typing in (or its focus and caret).
SEARCHBAR = ('<div class="searchbar">'
             '<input id="q" type="search" autocomplete="off" spellcheck="false" '
             'aria-label="テストを検索" '
             'placeholder="テストを検索（テスト ID / imported / generated）">'
             '<button type="button" class="ui-btn" id="q-clear">クリア</button>'
             '<span class="hits" id="hits"></span>'
             '</div>')

TOOLS_LOCAL = ('<div class="tools">'
               '<button type="button" class="ui-btn" onclick="exportAll()">'
               'バックアップを保存</button>'
               '<label class="ui-btn">バックアップを読み込む'
               '<input type="file" accept="application/json,.json" '
               'onchange="importAll(this)"></label>'
               '<span class="note">全テストの解答・採点結果を 1 つの JSON で入出力します。</span>'
               '</div>')


FONT_TAGS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">'
)


def index_html(mode: str = "server", tests: list | None = None) -> str:
    """Screen 1 for either deployment.

    ``mode='server'``: an empty shell that fetches ``/api/tests`` — the disk stays
    the source of truth and the list is never cached.
    ``mode='local'``: the same shell plus a baked manifest, filled in from
    localStorage by the same JS.
    """
    if mode not in ("server", "local"):
        raise ValueError(f"unknown list mode: {mode}")
    local = mode == "local"
    boot = (f'<script>{local_store.LOCAL_STORE_JS}\n'
            f'window.PAGES_TESTS = {json.dumps(tests or [], ensure_ascii=False)};</script>'
            if local else '')
    return (
        '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'{FONT_TAGS}'
        '<title>JLPT N2 模擬試験 — テスト一覧</title>'
        f'<style>{app_style.APP_CSS}{INDEX_CSS}</style></head><body>'
        f'<script>window.LIST_MODE = "{mode}";</script>{boot}'
        '<header class="app-header">'
        '<div class="header-inner">'
        '<div class="header-top-row">'
        '<span class="header-badge">JLPT N2 MOCK EXAM PORTAL</span>'
        '<span class="sub" id="counts" style="color:#94a3b8;font-size:0.85rem;font-variant-numeric:tabular-nums;">読み込み中…</span>'
        '</div>'
        '<h1 class="title">日本語能力試験 N2 模擬試験</h1>'
        '<div class="subtitle">公式過去問アーカイブ ＆ 精選模擬試験プラットフォーム ｜ 全問詳細解説付き</div>'
        '</div></header>'
        f'<main><p class="lede">{LEDE_LOCAL if local else LEDE_SERVER}</p>'
        f'{TOOLS_LOCAL if local else ""}'
        f'{SEARCHBAR}'
        '<div id="cards"></div></main>'
        f'<script>{index_js()}</script>'
        '<script>refreshList();</script></body></html>')
