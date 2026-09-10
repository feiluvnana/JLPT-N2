#!/usr/bin/env python3
"""Build 練習.html — 練習モード: the same paper, flat, with the model answer one
click away per question.

    python3 .agents/exam-app/scripts/build_practice.py tests/1     # make practice 1

`解答.html` is a SITTING: two phases behind 開始する gates, a clock that submits
the section at 00:00, one grade when 聴解 goes in (exam-app §"Screen 2 is a
two-phase sitting"). That is the wrong shape for studying, and bending it into
one — a fourth phase with the clock switched off and the grader hidden — would
put "is this a sitting?" into every branch of `render()`. So practice is its own
page, built from the same Markdown by the same injectors:

  * all 101 questions on ONE page, both sections open from the start, the 聴解
    player at the top of its half;
  * no clock and no grading — nothing is timed, nothing is scored, nothing is
    submitted;
  * one 解説 button per question, revealing THAT item's model answer: the
    correct option, why it is right and what each distractor gets wrong, in
    Japanese or Vietnamese. The box is rendered by exam-model-answer's own
    `explanation_box_html()` out of 詳細解説.json / 詳細解説.vi.json — this
    script formats no explanation prose of its own, so the two study surfaces
    (模範解答.html and this page) cannot disagree about an item.

The way in is a button under 言語知識・読解's 開始する gate in `解答.html`
(`build_interactive.gate()`): the choice between the two modes is made at the
moment you would otherwise start the clock. `make sheet` writes BOTH pages, so
that button can never open a practice page built from a superseded paper.

**Practice keeps NO record.** A sitting lives in ユーザー解答.json (the answers
plus 受験状態); this page writes nothing, anywhere — no POST, no localStorage, no
download — and the marks you make here are gone on reload. Deliberately: there
is no score to keep, and a second answer store beside the sitting's is exactly
how the test list and the sheet would start disagreeing about what you have
answered (exam-app §"One store per build"). The one thing it reads from the
browser is the language the reader last picked on 模範解答.html
(`build_model_answer.LANG_STORE_KEY`), so the two study pages agree about that.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_interactive as bi   # noqa: E402  (sibling: the sheet's injectors)
import grade_answers as ga       # noqa: E402  (sibling: the canonical keys)

# exam-model-answer owns every explanation — its prose, its bands, its [正解]
# tagging by index, and the CSS that box is styled with. Imported rather than
# reimplemented: a second renderer is a second thing to keep in step with
# 詳細解説.json (AGENTS.md §"one owner per rule").
_ma_spec = importlib.util.spec_from_file_location(
    "build_model_answer",
    ROOT / ".agents/exam-model-answer/scripts/build_model_answer.py")
ma = importlib.util.module_from_spec(_ma_spec)
_ma_spec.loader.exec_module(ma)

OUT_NAME = "練習.html"

# Every label this page prints outside the exam's own wording and outside the
# explanation box, once per language — the same arrangement as
# build_model_answer.UI, which owns the labels INSIDE the box (and whose
# `ans_badge` this page reuses rather than retyping).
UI = {
    "ja": {
        "html_lang": "ja",
        "doc_title": "テスト {test_id}（練習モード）",
        "bar_title": "テスト {test_id}（練習モード）",
        "back": "← テスト一覧",
        "exam_mode": "試験モードへ",
        "model_answer": "模範解答をまとめて見る",
        "answered": "解答",
        "show": "解説を見る",
        "hide": "解説を閉じる",
        "open_all": "解説をすべて開く",
        "close_all": "解説をすべて閉じる",
        "correct": "正解",
        "wrong": "不正解",
        "script_title": "音声スクリプト",
        "pending": "この設問の解説はまだ用意されていません。",
        "note": "練習モードです。制限時間も採点もありません。"
                "全{n_all}問が1ページに並んでいます。各設問の「解説を見る」で、"
                "その設問の模範解答と解説だけを開けます。"
                "解答はどこにも保存されません（再読み込みで消えます）。",
    },
    "vi": {
        "html_lang": "vi",
        "doc_title": "Đề {test_id}（Luyện tập）",
        "bar_title": "Đề {test_id}（Luyện tập）",
        "back": "← Danh sách đề",
        "exam_mode": "Sang chế độ thi",
        "model_answer": "Xem toàn bộ đáp án mẫu",
        "answered": "Đã chọn",
        "show": "Xem giải thích",
        "hide": "Ẩn giải thích",
        "open_all": "Mở tất cả giải thích",
        "close_all": "Đóng tất cả giải thích",
        "correct": "Đúng",
        "wrong": "Sai",
        "script_title": "Lời thoại audio",
        "pending": "Giải thích cho câu này chưa được soạn.",
        "note": "Chế độ luyện tập: không giới hạn thời gian, không chấm điểm. "
                "Toàn bộ {n_all} câu nằm trên một trang. Bấm 「Xem giải thích」 ở "
                "mỗi câu để mở đáp án mẫu và giải thích của riêng câu đó. "
                "Lựa chọn của bạn không được lưu ở đâu cả (tải lại trang là mất).",
    },
}

# `#screen-exam` is reused as the container id ON PURPOSE: this page is the exam
# screen with the phase machine taken out, so the sheet's own layout, radio
# bubbles and player chrome (build_interactive.EXTRA_CSS) and its 「聴解 ｜ 問題2」
# read-out (CHROME_JS, which looks that id up) apply here unchanged. The rules in
# EXTRA_CSS that belong to the clock, the gates and the result screen are simply
# inert — none of those elements exists on this page.
PRACTICE_CSS = """
:root{--primary:#1e3a8a}
#bar .lang-switch{flex:0 0 auto}
.pr-note{font-family:var(--ui);font-size:10pt;line-height:1.8;color:#334155;
  background:#f1f5f9;border:1px solid #cbd5e1;border-left:4px solid #2563eb;
  border-radius:0 8px 8px 0;padding:.9em 1.1em;margin:0 0 1.6em}
.pr-note .pr-note-links{margin-top:.6em;display:flex;flex-wrap:wrap;gap:.5em}
/* One reveal per question, sitting directly under its bubble row. 問題3/4/5's
   bubble rows are inline in a paragraph, so this must be block-level itself. */
.pr{display:block;font-family:var(--ui);margin:.1em 0 1.1em 1.2em}
.pr-btn{font-size:9.5pt;font-weight:700;padding:.3em .9em;border-radius:9999px;
  border:1px solid #cbd5e1;background:#ffffff;color:#334155;cursor:pointer;
  font-family:var(--ui);min-height:32px;transition:all .15s ease}
.pr-btn:hover{background:#eff6ff;border-color:#93c5fd;color:#1e3a8a}
/* Two-state labels, both shipped as markup: the CSS picks by aria-expanded, so
   no JS writes a label and neither state can go missing in one language. Not
   scoped to .pr-btn — the bar's 解説をすべて開く button is the same pattern. */
.pr-lbl.hide,[aria-expanded="true"] .pr-lbl.show{display:none}
[aria-expanded="true"] .pr-lbl.hide{display:inline}
.pr-btn[aria-expanded="true"]{background:#1e3a8a;border-color:#1e3a8a;color:#ffffff}
/* The verdict appears only when the answer does — opening the box is the
   moment the item stops being a question. It is a per-item marker, never a
   score: nothing on this page adds them up. */
.pr-verdict{margin-left:.5em}
.pr-verdict .pv{display:none}
.pr-verdict[data-state="ok"] .pv.ok,.pr-verdict[data-state="ng"] .pv.ng{display:inline-flex}
.pr-panel{margin:.55em 0 0;max-width:52em}
/* The explanation box is styled by exam-model-answer, whose own page stacks
   furigana with `ruby-position`; here it sits on top of the booklet stylesheet,
   where <rt> is absolutely positioned above its base (exam-app §Booklet
   rendering, rule 7) and needs the line to be tall enough to hold it. */
.pr-panel .exp-content,.pr-panel .exp-options-list li,.pr-panel .vocab-pill,
.pr-script{line-height:2.05}
.pr-ans{font-size:10pt;font-weight:700;color:#065f46;background:#ecfdf5;
  border:1px solid #a7f3d0;border-radius:6px;padding:.3em .8em;display:inline-block}
.pr-script{margin:.6em 0 0;padding:.75em .95em;background:#ffffff;
  border:1px solid #e2e8f0;border-radius:8px;font-size:10pt;line-height:1.9}
.pr-script .pr-script-label{font-size:9pt;font-weight:700;color:var(--muted);
  display:block;margin-bottom:.3em;letter-spacing:.02em}
@media print{
  .pr-btn,.pr-verdict,.pr-note,#bar{display:none}
}
@media screen and (max-width:48em){
  .pr{margin-left:.2em}
  .pr-btn{min-height:36px;font-size:10pt}
}
"""

PRACTICE_JS = """
const ANS = %(answers)s, LANGS = %(langs)s, TOTAL = %(total)d;
const PR = {};

function setLang(lang){ applyLang(lang, LANGS, true); }

/* The reveal. Everything it changes is an attribute the CSS reads — the two
   button labels and both verdict chips ship as markup, one .lang-pane per
   language, so no label on this page is written by JS and none can go missing
   in one language (the same rule as build_model_answer's language switch). */
function toggleExp(btn){
  const pr = btn.closest('.pr');
  if (!pr) return;
  const open = btn.getAttribute('aria-expanded') === 'true';
  setExp(pr, !open);
}
function setExp(pr, on){
  const btn = pr.querySelector('.pr-btn'), panel = pr.querySelector('.pr-panel');
  if (!btn || !panel) return;
  btn.setAttribute('aria-expanded', on ? 'true' : 'false');
  panel.hidden = !on;
  if (on) markVerdict(pr);
}
function toggleAll(btn){
  const on = btn.getAttribute('aria-expanded') !== 'true';
  btn.setAttribute('aria-expanded', on ? 'true' : 'false');
  for (const k in PR) setExp(PR[k], on);
}

/* Your answer against the key, for ONE item, and only while its box is open.
   No total is kept anywhere: 採点 belongs to 解答.html. */
function markVerdict(pr){
  const v = pr.querySelector('.pr-verdict');
  if (!v) return;
  const sel = document.querySelector(
    'input[name="q_' + CSS.escape(pr.dataset.q) + '"]:checked');
  v.dataset.state = !sel ? 'none'
                  : (parseInt(sel.value, 10) === ANS[pr.dataset.q] ? 'ok' : 'ng');
}
function countAnswered(){
  const n = document.querySelectorAll('#screen-exam input[type=radio]:checked').length;
  const el = document.getElementById('done');
  if (el) el.textContent = n + ' / ' + TOTAL;
}

document.addEventListener('change', e => {
  if (e.target.type !== 'radio') return;
  countAnswered();
  // Re-check the verdict only where the answer is already on screen; an
  // unopened item stays a question.
  const pr = PR[e.target.name.slice(2)];
  if (pr && pr.querySelector('.pr-btn').getAttribute('aria-expanded') === 'true') {
    markVerdict(pr);
  }
});

window.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.pr').forEach(p => { PR[p.dataset.q] = p; });
  if (LANGS.length > 1) applyLang(savedLang(LANGS), LANGS, false);
  countAnswered();
  fitPlayer();
  initSpy();
  window.addEventListener('resize', fitPlayer);
});
"""


def collapse(html: str) -> str:
    """One line, no newlines — markdown's nl2br would otherwise sprinkle
    `<br />` through the injected block, which is appended INSIDE the source
    line that carries the bubble row. Explanation text has already had its own
    newlines turned into `<br>` by apply_furigana(), so nothing meaningful is
    lost."""
    return re.sub(r"\s*\n\s*", " ", html).strip()


def pane(langs: list, render) -> str:
    """build_model_answer's switching mechanism, verbatim — one `.lang-pane` per
    language, hidden by CSS. Re-exported here so this module's own labels go
    through the same door as the explanation box's."""
    return ma.pane(langs, render)


def label(langs: list, key: str, **fmt) -> str:
    return pane(langs, lambda lg: UI[lg][key].format(**fmt))


def verdict_chip(langs: list) -> str:
    return ('<span class="pr-verdict" data-state="none">'
            f'<span class="chip ok pv ok">{label(langs, "correct")}</span>'
            f'<span class="chip ng pv ng">{label(langs, "wrong")}</span>'
            '</span>')


def explain_block(key: str, ans: int | None, details: dict, langs: list,
                  script: str = "") -> str:
    """The 解説 button and its (hidden) panel for one question.

    A key this page cannot resolve gets no reveal at all rather than a box
    arguing for option 1 — an item with no key is a Markdown bug the sheet
    builder already warns about loudly, and inventing one here would hide it.

    An item with no 詳細解説 entry gets 「解説はまだ用意されていません」, NOT the
    booklet's own 解説 column. That column is where `模範解答.html` falls back to
    (`explanation_box_html`'s `raw_kaisetsu`), and it is fine there because that
    page is built only after authoring is frozen — but this page is written by
    `make sheet`, so it exists all through the pipeline, and the 解説 column is
    authoring prose: it cites `moji-goi.md`, `matrix_helper.py` and 「×4」 shapes
    at a reader who is trying to learn a word. exam-model-answer prohibits
    exactly that leak in learner-facing explanations, so this page passes an
    empty fallback and says plainly that the explanation is not written yet.
    """
    if ans not in (1, 2, 3, 4):
        return ""
    choukai = not key.isdigit()
    script_html = ""
    if choukai and script:
        script_html = ('<div class="pr-script"><span class="pr-script-label">'
                       + label(langs, "script_title") + '</span>'
                       + ma.apply_furigana(script) + '</div>')
    if (details.get("ja") or {}).get(key):
        box = ma.explanation_box_html(details, key, ans, "", langs,
                                      choukai=choukai)
    else:
        box = pane(langs, lambda lg:
                   f'<div class="explanation-box">'
                   f'<div class="exp-heading">{ma.UI[lg]["exp_heading"]}</div>'
                   f'<div class="exp-content">{UI[lg]["pending"]}</div></div>')
    ans_line = ('<div class="pr-ans">'
                + pane(langs, lambda lg: ma.UI[lg]["ans_badge"])
                + str(ans) + '</div>')
    return collapse(
        f'<div class="pr" data-q="{key}">'
        f'<button type="button" class="pr-btn" aria-expanded="false" '
        f'onclick="toggleExp(this)">'
        f'<span class="pr-lbl show">{label(langs, "show")}</span>'
        f'<span class="pr-lbl hide">{label(langs, "hide")}</span>'
        f'</button>{verdict_chip(langs)}'
        f'<div class="pr-panel" hidden>{ans_line}{script_html}{box}</div>'
        f'</div>')


def load_details(d: Path) -> dict:
    """{lang: 詳細解説 data} for whichever sets exist, exactly as
    build_model_answer loads them — `ja` owns the exam wording, every other
    language carries prose only."""
    out = {}
    for lg in ma.LANGS:
        f = d / ("詳細解説.json" if lg == "ja" else f"詳細解説.{lg}.json")
        if not f.is_file():
            continue
        try:
            out[lg] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"  ! {f.name} did not parse; its pane falls back to the "
                  f"booklet 解説: {exc}")
    return out


def build(d: Path, out_dir: Path | None = None, storage: str = "server") -> Path:
    """Write one test's 練習.html. Returns the path written.

    `storage` picks nothing about answers — practice keeps no record — only
    where 「テスト一覧」 points, which differs between `make serve` and the Pages
    build exactly as it does for the sheet (build_interactive.LIST_HREF).
    """
    gengo_src, choukai_src = d / "言語知識・読解.md", d / "聴解.md"
    if not gengo_src.is_file() or not choukai_src.is_file():
        sys.exit(f"Missing source markdowns in {d}")
    if storage not in bi.LIST_HREF:
        raise ValueError(f"unknown deployment: {storage}")

    graw = gengo_src.read_text(encoding="utf-8")
    craw = choukai_src.read_text(encoding="utf-8")

    gkeys = ga.parse_gengo_keys(gengo_src)
    ckeys = ga.parse_choukai_keys(choukai_src)
    answers = {str(k): v for k, v in gkeys.items()}
    answers.update(ckeys)

    details = load_details(d)
    langs = [lg for lg in ma.LANGS if lg in details] or ["ja"]

    scripts = bi.parse_choukai_scripts(d / "聴解スクリプト.txt")

    def script_for(key: str) -> str:
        # 詳細解説.json owns the wording where it has it; the .txt is the
        # fallback, and the same precedence 模範解答.html uses.
        stored = (details.get("ja") or {}).get(key) or {}
        return stored.get("script") or scripts.get(key, "")

    def after(key: str) -> str:
        return explain_block(key, answers.get(key), details, langs,
                             script_for(key))

    gmd, gids = bi.inject_gengo(bi.strip_key(graw, gengo_src), after=after)
    cmd, cused = bi.inject_choukai(bi.strip_key(craw, choukai_src),
                                   list(ckeys.keys()), bi.example_premarks(craw),
                                   after=after)
    gengo_body, choukai_body = bi.render_bodies(gmd, cmd)

    dest = out_dir if out_dir is not None else d
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / OUT_NAME
    n_all = len(gids) + len(cused)
    player = bi.player_html(d)

    list_href = bi.LIST_HREF[storage]
    lang_switch = ""
    if len(langs) > 1:
        lang_switch = '<span class="lang-switch">' + "".join(
            f'<button class="lang-btn" data-lang="{lg}" '
            f'onclick="setLang(\'{lg}\')">{ma.LANG_NAME[lg]}</button>'
            for lg in langs) + '</span>'

    bar = (f'<div id="bar">'
           f'<a class="back" href="{list_href}">{label(langs, "back")}</a>'
           f'<b id="bar-title">{label(langs, "bar_title", test_id=d.name)}</b>'
           f'<span class="sub" id="where"></span>'
           f'<span class="grow"></span>'
           f'<span id="bar-controls">'
           f'{lang_switch}'
           f'<span class="sub">{label(langs, "answered")} '
           f'<b id="done">0 / {n_all}</b></span> '
           f'<button type="button" aria-expanded="false" onclick="toggleAll(this)">'
           f'<span class="pr-lbl show">{label(langs, "open_all")}</span>'
           f'<span class="pr-lbl hide">{label(langs, "close_all")}</span></button> '
           f'<button type="button" onclick="location.href=\'解答.html\'">'
           f'{label(langs, "exam_mode")}</button>'
           f'</span></div>')

    note = (f'<div class="pr-note">{label(langs, "note", n_all=n_all)}'
            f'<div class="pr-note-links">'
            f'<a class="ui-btn" href="模範解答.html">'
            f'{label(langs, "model_answer")}</a></div></div>')

    body = (f'<div id="screen-exam">{note}'
            f'<h1 class="section-title">JLPT N2 言語知識（文字・語彙・文法）・読解</h1>'
            f'{gengo_body}'
            f'<hr class="section-divider">'
            f'<h1 class="section-title">JLPT N2 聴解</h1>'
            f'{player}{choukai_body}</div>')

    js = (PRACTICE_JS % {"answers": json.dumps(answers, ensure_ascii=False),
                         "langs": json.dumps(langs),
                         "total": n_all}
          + ma.LANG_SWITCH_JS + bi.CHROME_JS + (bi.PLAYER_JS if player else ""))

    out.write_text(
        f'<!DOCTYPE html><html lang="{UI[langs[0]]["html_lang"]}">'
        f'<head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'{bi.booklet.FONT_TAGS}'
        f'<title>{UI[langs[0]]["doc_title"].format(test_id=d.name)}</title>'
        # Same staleness stamps as 解答.html, plus the two explanation sets this
        # page renders: an explanation rewritten after the page was built is
        # exactly the drift `make check` (check_artifact_freshness) must catch.
        f'{bi.booklet.src_sha_comments([gengo_src, choukai_src, d / "聴解スクリプト.txt", d / "聴解_チャプター.json", d / "詳細解説.json", d / "詳細解説.vi.json"])}'
        f'<style>{bi.booklet.CSS}{bi.booklet.SCREEN_CSS}{bi.app_style.APP_CSS}'
        f'{bi.EXTRA_CSS}{ma.EXPLANATION_CSS}{PRACTICE_CSS}</style></head>'
        f'<body data-lang="{langs[0]}">{bar}{body}'
        f'<script>{js}</script></body></html>',
        encoding="utf-8")

    pending = [k for k in gids + cused if not (details.get("ja") or {}).get(k)]
    if pending:
        print(f"  ! {len(pending)} question(s) have no 詳細解説 entry yet and "
              f"reveal 「解説はまだ用意されていません」: {pending[:6]} — author the "
              f"explanations (exam-model-answer), then `make practice {d.name}`")

    missing = [k for k in gids + cused if answers.get(k) not in (1, 2, 3, 4)]
    if missing:
        print(f"  ! {len(missing)} question(s) got no 解説 reveal (no key in the "
              f"Markdown): {missing[:6]} — fix the key table, not this page")
    print(f"  {out}  ({n_all} items, {len(langs)} language(s): "
          f"{', '.join(langs)}; no clock, no grading, no record)")
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Build 練習.html (練習モード) for one test: the whole paper on "
                    "one page, no clock, no grading, one model answer per "
                    "question behind a button.")
    ap.add_argument("test_dir", help="tests/<test_id>")
    ap.add_argument("--storage", choices=sorted(bi.LIST_HREF), default="server",
                    help="which deployment's 「テスト一覧」 link to write: "
                         "'server' for make serve (default), 'local' for the "
                         "GitHub Pages build. Answers are never stored either way")
    ap.add_argument("--out", type=Path, default=None,
                    help="write the page here instead of into the test folder")
    args = ap.parse_args()

    d = Path(args.test_dir)
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")
    build(d, out_dir=args.out, storage=args.storage)


if __name__ == "__main__":
    main()
