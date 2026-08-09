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
/* Wider than exam/result (60em): cards with many action buttons need the room. */
main{max-width:80em;margin:0 auto;padding:1.4em 1.2em 4em}
.lede{margin:0 0 1.4em;font-size:10.5pt;color:var(--muted)}
/* Equal card height. Meter uses display:contents so the track shares a row with
   the status chip (left-aligned); the lbl sits on the row under the track —
   flex + align-items:center was optically centering the whole meter block and
   made the bar look offset from the chip. */
.card{display:grid;grid-template-columns:20em auto minmax(12em,1fr) auto auto;
  grid-template-rows:1fr auto;column-gap:1em;row-gap:.2em;align-items:center;
  background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:.55em 1.2em;
  margin-bottom:.9em;box-sizing:border-box;height:5.1em;min-height:5.1em;
  max-height:5.1em;overflow:hidden}
.card h2{grid-column:1;grid-row:1/-1;margin:0;font-size:13pt;min-width:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;align-self:center}
.card .origin{grid-column:2;grid-row:1/-1;align-self:center}
.card .meter{display:contents}
.card .meter .track{grid-column:3;grid-row:1;align-self:center;width:100%;min-width:0}
.card .meter .lbl{grid-column:3;grid-row:2;text-align:left;margin:0;line-height:1.2;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .status{grid-column:4;grid-row:1/-1;align-self:center}
.acts{grid-column:5;grid-row:1/-1;display:flex;flex-wrap:nowrap;gap:.4em;
  align-self:center}
.acts .ui-btn{padding:.35em .75em;font-size:10.5pt;white-space:nowrap}
.empty{background:#fff;border:1px dashed var(--line);border-radius:10px;padding:2em;
  text-align:center;color:var(--muted)}
code{background:#f1f5f9;padding:.1em .4em;border-radius:4px;font-size:10pt}
.badge.origin-imp{background:#e0f2fe;color:#0369a1;border:1px solid #bae6fd}
.badge.origin-gen{background:#f1f5f9;color:#475569;border:1px solid #e2e8f0}
/* Pages-only: localStorage is the only copy of your answers, so the list owns
   the way to get them off this browser and back onto another one. */
.tools{display:flex;flex-wrap:wrap;gap:.5em;align-items:center;margin:0 0 1.4em}
.tools .note{font-size:10pt;color:var(--muted)}
.tools input[type=file]{display:none}
@media screen and (max-width: 54em){
  main{padding:1em .8em 3em}
  .card{grid-template-columns:1fr auto;grid-template-rows:auto auto auto auto auto;
    column-gap:.6em;row-gap:.4em;height:auto;min-height:auto;max-height:none;
    padding:.85em 1em;overflow:visible}
  .card h2{grid-column:1;grid-row:1;font-size:12pt;white-space:normal;overflow:visible}
  .card .origin{grid-column:2;grid-row:1;justify-self:end}
  .card .status{grid-column:1 / -1;grid-row:2;justify-self:start}
  .card .meter .track{grid-column:1 / -1;grid-row:3}
  .card .meter .lbl{grid-column:1 / -1;grid-row:4}
  .acts{grid-column:1 / -1;grid-row:5;justify-self:start;flex-wrap:wrap;
    margin-top:.2em;width:100%}
  .acts .ui-btn{padding:.4em .85em;font-size:10pt;min-height:36px}
  .tools{gap:.6em}
  .tools .ui-btn{width:100%;justify-content:center}
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
      id: t.id, origin: t.origin, total: TOTAL,
      has_sheet: t.has_sheet, has_audio: t.has_audio,
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
  var id = esc(t.id), base = sheetHref(t.id), acts = [];
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

function render(tests){
  var body = tests.length
    ? tests.map(cardHtml).join('')
    : '<div class="empty">tests/ にテストがありません。'
      + '<code>make sheet &lt;test_id&gt;</code> で解答用紙を生成してください。</div>';
  document.getElementById('cards').innerHTML = body;
  var graded = tests.filter(function(t){ return t.result; }).length;
  document.getElementById('counts').textContent =
    'テスト ' + tests.length + ' 件 / 採点済み ' + graded + ' 件';
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
  var btn = ev.target && ev.target.closest && ev.target.closest('[data-clear]');
  if (btn) clearTestProgress(btn.getAttribute('data-clear'));
});
// The list must be live: coming back from a graded exam has to show the score.
window.addEventListener('pageshow', refreshList);
"""


def index_js() -> str:
    return INDEX_JS % {"total": QUESTION_COUNT, "sheet": json.dumps(SHEET, ensure_ascii=False)}


LEDE_SERVER = ('受験するテストを選んでください。'
               '解答は選択するたびに保存され、採点結果は 採点結果.json に残ります。'
               '「結果を削除」で採点結果と解答の両方を消せます。')
LEDE_LOCAL = ('受験するテストを選んでください。解答と採点結果は'
              '<b>このブラウザ内（localStorage）にのみ</b>保存されます。'
              '別の端末やブラウザには引き継がれず、閲覧データを消去すると失われるため、'
              '残しておきたい結果は「バックアップを保存」で書き出してください。')

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
        # The same #bar as screens 2 and 3, from the same stylesheet.
        '<div id="bar"><b>JLPT N2 模擬試験</b><span class="grow"></span>'
        '<span class="sub" id="counts">読み込み中…</span></div>'
        f'<main><p class="lede">{LEDE_LOCAL if local else LEDE_SERVER}</p>'
        f'{TOOLS_LOCAL if local else ""}'
        '<div id="cards"></div></main>'
        f'<script>{index_js()}</script>'
        '<script>refreshList();</script></body></html>')
