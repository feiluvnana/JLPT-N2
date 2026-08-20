---
name: exam-app
description: Single owner of rendering and running the exam. Owns the whole app surface — Markdown sources → booklet HTML with A4 print geometry and furigana helpers (NO PDF, ever), the MERGED problem+answer sheet 解答.html with radio bubbles, an embedded 聴解 audio player and in-page 180-point grading, the ONE local server and test list, the static GitHub Pages build that keeps answers in localStorage, and CLI grading (scaled 0–180 scores, pass/fail evaluation, 採点結果.json) via grade_answers.py. Use whenever generating/regenerating/fixing exam booklets or formatting (answers squashed on one line, cramped spacing, furigana misaligned, tables splitting across pages); whenever the user wants to take/answer/solve a test on screen, mentions the answer sheet, マークシート, 解答用紙, the test list, playing the listening audio while answering, or publishing/hosting the exam on GitHub Pages; and whenever the user asks to grade, score, check answers, 採点, 答え合わせ, or analyze exam results.
---

# Exam App (冊子レンダリング・解答用紙・サーバー・採点)

One skill owns booklet rendering, the merged problem+answer sheet, the
server, the static Pages twin, and grading — all in `.agents/exam-app/scripts/`:

| Script | Job |
| - | - |
| `build_booklet.py` | Markdown → booklet HTML (`言語知識・読解.html`, `聴解.html`); shared CSS and ruby/furigana helpers |
| `build_interactive.py` | Markdown → `解答.html`, the merged sheet with in-page grading; also the `--keyless` QA render |
| `serve_sheet.py` | the ONE local server: test list, exam, results, saved into `tests/<id>/` |
| `build_pages.py` | the static GitHub Pages build into `_site/` |
| `grade_answers.py` | CLI grading twin: scaled scores, pass/fail, `採点結果.json` |
| `app_style.py`, `index_view.py`, `local_store.py` | shared modules |

## Shared modules — one copy of everything

- `app_style.py` holds `APP_CSS`; both builders import it. Add chrome there,
  never in either script — two copies drift, and no gate sees a drifted
  colour. Must stay free of bare element selectors (loads on top of the
  booklet stylesheet).
- `index_view.py` — screen 1's CSS/cards/actions, fed the same test objects
  by `/api/tests` or a baked manifest. `make check` fails if `INDEX_CSS` is
  defined anywhere else.
- `local_store.py` — `window.JLPTStore`, the ONLY place the localStorage key
  schema is written.
- `build_interactive.py` imports `build_booklet.py`'s `CSS`, `SCREEN_CSS`,
  `widen()`, `fit_ruby()`, `mark_furigana_blocks()` so sheet and booklet
  render identically — sibling imports, both live in this skill's `scripts/`.
  `add_choukai_furigana()` is NOT shared: applied only to 聴解-named files,
  so `聴解.html` carries auto-furigana the 聴解 half of `解答.html` lacks — a
  known difference, not a bug.
- `build_pages.py` calls `build_interactive.build()` rather than copying
  `解答.html`, which would ship a sheet POSTing to a nonexistent API.

## Execution

```bash
python3 .agents/exam-app/scripts/build_booklet.py tests/<id>/言語知識・読解.md tests/<id>/聴解.md   # make booklet <id>
python3 .agents/exam-app/scripts/build_interactive.py tests/<id>                                    # make sheet <id>
python3 .agents/exam-app/scripts/serve_sheet.py                                                      # make serve (--port 8765, --no-open; NO test id)
python3 .agents/exam-app/scripts/build_pages.py                                                       # make pages (then make preview-pages)
python3 .agents/exam-app/scripts/build_interactive.py tests/<id> --keyless                           # make keyless <id> -> qa/<id>/keyless.md
python3 .agents/exam-app/scripts/grade_answers.py --test-dir tests/<id>                              # make grade <id>
```

Re-run the booklet AND sheet build after ANY edit to the `.md` sources — they
are the single source of truth; the grader parses keys out of them and the
sheet builder parses questions out of them. Editing HTML by hand is always wrong.

## Booklet rendering (`build_booklet.py`)

`言語知識・読解.md` + `聴解.md` → their HTML twins in the same folder. That is
the whole pipeline. **No PDF.**

### Why no PDF — this rule lives here now

`@page { size: A4 }` and page-break rules stay in the CSS, so Cmd-P from the
browser gives the same A4 booklet. Removing the PDF step removed a real
defect: WeasyPrint and wkhtmltopdf laid absolute-positioned `<rt>` out
differently, so whichever was on PATH silently changed the furigana output.
**Never reintroduce weasyprint/wkhtmltopdf/poppler** — no PDF toolchain at all.

### Non-negotiables baked into the script (know WHY they exist)

1. **`nl2br` is mandatory** — without it every vertically-stacked option
   list collapses onto one unreadable line.
2. **CJK fonts**: body = YuMincho (real booklets are 明朝 — confirmed via
   `pdffonts` on every `refs/JLPT_N2_NEW/` booklet), headings/bold =
   YuGothic. Ship as system fonts on macOS/Windows 8.1+; fallback chain adds
   Hiragino Mincho ProN/Hiragino Sans and Google-Fonts Noto Serif/Sans JP.
   Never put a sans-serif font ahead of YuMincho in the body chain — regressed
   once already (commit `116cc88` silently rendered a whole booklet
   sans-serif). Verify: `fc-list | grep -iE "yumincho|yugothic"`.
3. **Option widening**: lines with 3+ options get three IDEOGRAPHIC spaces
   (U+3000) between them — HTML collapses ASCII spaces but keeps U+3000.
4. **Tables**: `width:100%; border-collapse:collapse; page-break-inside:avoid`.
5. **Page-break control**: avoid inside tables/blockquotes, avoid after
   headings; line-height ≥1.9 for Japanese.
6. Layout per `jlpt-exam-structure`: horizontal options for 文字・語彙・文法,
   vertical for 聴解 and 問題6.
7. **Ruby furigana**: `<ruby>漢字<rt>かんじ</rt></ruby>`, stacked by hand
   (not `ruby-position` — old PDF renderers ignored it and dropped the base
   below the reading). `ruby` is `inline-block; position:relative;
   line-height:1`; `rt` is `position:absolute; bottom:calc(100% + 0.1em);
   left/right:-0.6em`. `fit_ruby()` gives ruby a `min-width` when the reading
   is wider than its base; `mark_furigana_blocks()` adds `class="furi"`
   (line-height 2.1) only to blocks containing ruby.
8. **Vocabulary notes** (`（注1）…`): `.vocab-notes` styling (9pt, line-height
   1.6, top dashed border) replicates the official Dokkai layout.
9. **Passage boxes are not optional decoration** — official booklets print
   every 問題9–14 passage/notice inside a ruled box, separate from the
   questions below it (`.passage-box`, produced by `box_passages()`).
   **14 boxes per paper**: 問題9 ×1, 問題10 ×5, 問題11 ×4, 問題12 ×2 (A and B
   box separately), 問題13 ×1, 問題14 ×1 — `make check`
   (`check_passage_boxes`) FAILs any other count, in the Markdown AND in both
   built HTML files. The box comes from pattern-matching the source, so an
   authoring dialect the boxer misses prints an unboxed passage with no error:
   both the `## 問題N` + inline instruction and the bare-heading + instruction-
   paragraph forms are matched, and 問題12's texts may be labelled `### A` or
   `**A**`. A dialect that ships boxless is a `box_passages()` bug — teach the
   boxer, never hand-edit HTML (2026-08-20: three papers rendered 0 boxes and
   three more merged 問題12's A and B into one, all green).
10. **`add_choukai_furigana()`'s pykakasi output needs a fixup pass** — a
   2026-08 audit found real wrong readings: bare `人` came back `にん` instead
   of `ひと` (genuine `にん` compounds like 三人/本人 are long enough that
   kakasi already merges them, so a standalone `人` is always "hito"); `方`
   right after hiragana came back `ほう` instead of `かた`; `小さい`/`小さく`
   came back with a bogus chouon. All three are corrected by `fix_hira()`
   inside `add_choukai_furigana()` — if you touch that function again or
   spot another wrong reading, fix it there (not the generated HTML) and
   rebuild every test's `聴解.html`.

`SCREEN_CSS` is the screen-only shell: a centered 60em column plus a
`--gutter` variable the sheet's sticky bar/audio player use — entirely inside
`@media screen`, so `@page` A4 geometry is untouched.

### `verify()` — automatic, aborts the build

Runs on every build; aborts on mojibake, an `<ol>` in the output (stems must
be bold `**6**`, never `N.` list syntax which restarts numbering), or a
missing bold stem for any of questions 1–71. Still check by eye that key/
explanation tables render at the end of both files and furigana sits over
its base; Cmd-P to preview pagination.

## The three screens

`解答.html` merges the problem booklet and radio bubbles into one
deliverable: answer **inside the booklet**, press 「採点する」, the 180-point
result appears immediately. `make serve` (no test id) covers every test; the
same screens ship as a static Pages site — only where answers are kept differs.

| # | Screen | Where it lives | What it does |
| - | ------ | -------------- | ------------ |
| 1 | テスト一覧 | `GET /` — `serve_sheet.py` | every test in `tests/`, answered count, last score, origin badge (`imported`/`generated`) |
| 2 | 受験 | `GET /tests/<id>/解答.html` | the exam; each click autosaves |
| 3 | 採点結果 | same page, `#screen-result` | rendered on 「採点する」 or fetched from `採点結果.json` |

A graded test is never locked — 「解答に戻ってやり直す」 reopens screen 2 with
saved answers, re-grading overwrites `採点結果.json`. `解答.html` is NOT the
booklets, which `build_booklet.py` overwrites on every build; there are no
per-section `*_解答.html` files.

**`make mp3` obliges `make sheet`.** The player embeds `聴解_チャプター.json`
verbatim, so every chapter offset comes from the MP3 build that wrote that
file. Rebuild audio and the sheet seeks to the previous build's offsets while
the Markdown stays byte-identical — the chapter JSON is stamped as a
**fourth source** of `解答.html`, and `make check` fails a sheet older than
its chapters.

## Grading — press 「採点する」 (in-page: the normal path)

Grades all 101 questions against embedded keys, evaluates section cutoffs
(≥19/60) and total (≥90/180), switches to screen 3, and saves to whichever
store this build uses (`採点結果.json`/`ユーザー解答.json`): into `tests/<id>/`
under `make serve`, into localStorage on Pages, or as browser downloads with
no server/store. Unanswered items appear as 「未解答」 chips, not wrong.

**全設問解答チェック表 expands as one list** — 「すべての設問詳細を展開」builds
detail blocks for all 101 items from the still-in-DOM exam screen plus
あなたの答え/正解 (display-only).

### One source of truth for the grading data

`grade_answers.py` is the in-page grader's CLI twin. `computeResult()`
returns the **same document** `grade_answers.py` writes, stays free of DOM
and `Date`, and `make check` runs it under node and compares field for field
against the Python grader. There is no Markdown report — the result is data.

`ANSWER_KEY`, `TAXONOMY`, `ADVICE`, and section definitions are **serialized
out of `grade_answers.py` at build time** — never hand-write those tables
into JS (a second copy is exactly how the grader's 大問 ranges once drifted
from `jlpt-exam-structure`). Re-run `build_interactive.py` after changing any
of them.

## The answer key must never be VISIBLE — one truncation, three build modes

The key is embedded as JS data so grading works offline, but never
_rendered_. `strip_key()` truncates everything from the key heading onward,
and the builder errors if it can't find that heading — never loosen the
check. Every emitted document goes through the same `strip_key()`.

| Mode | Command | Writes | Keys |
| - | - | - | - |
| server sheet (default) | `make sheet <id>` | `tests/<id>/解答.html` | embedded JS, never rendered |
| Pages sheet | `make pages` | `_site/tests/<id>/解答.html` | same |
| **keyless render** | `make keyless <id>` | `qa/<id>/keyless.md` | **none, anywhere** |

### `--keyless` — the QA blind-solve render

`exam-qa-review`'s first ground rule is blind-solve before reading the keys
— unexecutable before this existed, since the keys live at the END of the
same two Markdown files the paper lives in. `--keyless` emits the whole paper
through `strip_key()` plus `聴解スクリプト.txt` verbatim, embeds no key data
at all, and re-scans its own output with `KEY_HEADING`, refusing to write a
render that still carries one. Header carries each source's `sha1[:12]` —
what the QA report header must name. Not a deliverable: lands in
`qa/<id>/keyless.md` (gitignored), beside the QA report.

## Audio player (聴解 only)

- `<audio src="聴解.mp3">` is referenced relatively, never embedded (a ~30MB
  base64 blob would be ~40MB of HTML). Controls: play/scrub, ±10s, speed
  0.75–1.5, chapter dropdown.
- **Chapter marks** come from `聴解_チャプター.json` (exact assembler offsets,
  not silence-detection guesses) — absent, the dropdown just hides itself.
- Some browsers block `file://` media: a 「MP3を選ぶ」 picker is always
  present as fallback. Never require a web server.

## Serving (`serve_sheet.py`) — five things it must keep doing

1. **One server, every test** — no arguments, serves the whole `tests/`
   tree; routes `/`, `/api/tests`, `/tests/<id>/…`, `POST /api/tests/<id>/
   {answers,submit,clear}`. Only paths under `tests/` are reachable.
2. **Screen 1 reads the disk, never a cache** — `GET /api/tests` carries
   `Cache-Control: no-store`.
3. **Range requests** — `聴解.mp3` is ~30MB and `<audio>` re-requests with
   `Range:` on every seek; the handler answers `206 Partial Content` itself
   and advertises `Accept-Ranges: bytes`.
4. **Client disconnects are not errors** — swallow `BrokenPipeError`/
   `ConnectionResetError`, never re-raise.
5. **Threaded** (`ThreadingHTTPServer`) — a single-threaded server would
   queue 採点する behind an in-flight MP3 stream.

## Two deployments, one app — `make serve` and GitHub Pages

Same three screens, two storage backends, never two apps:

| | `make serve` (local) | GitHub Pages (`make pages`) |
| - | - | - |
| Screen 1 | `serve_sheet.py`, `GET /api/tests` reads disk | `_site/index.html`, progress from localStorage |
| Screens 2–3 | `解答.html`, `--storage server` | `_site/.../解答.html`, `--storage local` |
| Answers | `ユーザー解答.json` via `POST /api/…` | `localStorage[jlpt-mock/v1/<id>/…]` |
| Result | `採点結果.json` via `POST /api/…` | `localStorage[…]` |

```bash
make pages            # every test → _site/   (make pages 1 for one test)
make preview-pages    # python3 -m http.server -d _site 8766
```

`.github/workflows/pages.yml` runs this on push. `_site/` is **gitignored** —
CI rebuilds from `tests/`; MP3s (~30MB/test) are copied in, `--no-audio`
skips them. Pages' CDN answers `Range:`; `make preview-pages`'s
`http.server` does not (a preview-only limitation).

**One store per build.** Exactly one backend is live per build, chosen at
BUILD time (`--storage server|local`), never sniffed at runtime — a server
sheet contains no localStorage code at all. `make check` asserts every
`解答.html` is always the server build with no store prefix.

**What Pages cannot do:** no disk, so local builds grow a 「採点結果を保存
（JSON）」 button and a 「バックアップを保存/読み込む」 pair — one JSON per
test's two documents, and how answers move between browsers. Say so on the
page: clearing site data loses the lot.

## On-screen layout — one design across three screens

Screens 2–3 keep the booklets' centered 60em measure, moved onto
`#screen-exam`/`#screen-result` so the bar spans the window like screen 1.
Screen 1's `<main>` is wider (80em) for cards — don't widen the exam/result
columns to match, and don't use `width:100vw` (includes the scrollbar,
shoves 採点する off-screen). All inside `@media screen`. `initSpy()`/
`updateSpy()` track the nearest heading above the bar (「聴解 ｜ 問題2」);
`fitPlayer()` measures the bar and sets the player's sticky offset — never
hard-code it.

## Answer capture

Every radio click writes to the one place this build uses:
`ユーザー解答.json` via `POST /api/tests/<id>/answers` (debounced ~250ms)
under `make serve`, or the matching localStorage key on Pages — nothing in
the page knows which backend it talks to. 採点する writes `採点結果.json`
plus the same shape: `{"言語知識_読解": {"33": 2, …}, "聴解": {"問1-1": 2, …}}`.

## Parser contract (why the Markdown conventions are load-bearing)

- 言語知識: `**33** stem` then indented ` 1. … 2. …`, OR 問題6's `**28 募集**`,
  OR 問題9's all-on-one-line form. **問題7 dialogue stems may span lines**
  after `**N**` — `inject_gengo` must keep `cur` across those lines
  (flushing on every non-option line once dropped radios for Q32/39–42).
- 聴解: `**1番**` + indented options (問題1/2 only), OR a bare bubble row
  `**1番** 1・2・3・4` for 問題3/4/5. **All of 問題5 takes the bubble-row
  form, including `質問1`/`質問2`** — this repo prints no options for either
  item, so 質問N is a bubble row, not a heading over an option list.
- `**例**` rows get a STATIC row with the answer pre-filled, never radios —
  the number comes from the 解答用紙 grid's `**(n)**` cell, read before
  `strip_key` truncates it; `make check` asserts it equals the announced number.
- **The builder warns loudly** on a question with no radio group or a group
  with no key — always a Markdown bug, never noise.

## CLI grading (`grade_answers.py`)

Parses keys from the two Markdown sources, reads responses, writes
`採点結果.json`. **User answers are auto-discovered**: `ユーザー解答*.json` in
the test dir and cwd; inline `--answers-gengo`/`--answers-choukai` override.

- **Scaled 0–180 scoring**: raw section counts → 0–60 per section —
  言語知識 (51 items), 読解 (20 items), 聴解 (30 answers; 問題5-2番 yields two).
- **The scale is proportional, an approximation — say so.** The real exam
  equates scores across sittings (得点等化), which needs statistics this repo
  doesn't have. Never describe the output as a real JLPT score or "improve"
  it with invented difficulty weights.
- **Pass/fail (published N2 criteria)**: total ≥90/180 AND every section
  ≥19/60 — failing any one sectional cutoff is 不合格 regardless of total.
- **Taxonomy**: 大問→question ranges owned by `jlpt-exam-structure`;
  `GENGO_QUESTION_TAXONOMY` asserts at import that its ranges tile 1–71 with
  no gap/overlap. No copy of the table lives in this doc.
- **Advice integrity**: weak-area advice maps to the matching Shin Kanzen
  Masuta N2 study area.

## Result document (`採点結果.json`) — the schema is a contract

Data, not prose. `解答.html` and the test list read it back;
`result_payload()` in `grade_answers.py` is its only Python definition,
`computeResult()` builds the identical structure, `make check` compares both
field for field:

```jsonc
{
  "test_id": "1",
  "graded_at": "2026-08-05T09:12:33+00:00",   // the ONLY field allowed to differ between graders
  "summary": {
    "passed": false, "total_scaled_score": 118, "max_scaled_score": 180,
    "cutoff_passed": true, "overall_threshold_passed": true,
    "sections": {
      "言語知識（文字・語彙・文法）": {"raw_correct": 33, "raw_total": 51, "scaled_score": 39, "cutoff": 19, "passed_cutoff": true},
      "読解":   {"raw_correct": 14, "raw_total": 20, "scaled_score": 42, "cutoff": 19, "passed_cutoff": true},
      "聴解":   {"raw_correct": 20, "raw_total": 30, "scaled_score": 40, "cutoff": 19, "passed_cutoff": true}
    }
  },
  "taxonomy_stats": { "問1": {"name": "漢字読み (Kanji Reading)", "section": "言語知識", "correct": 3, "total": 5, "percentage": 60.0} },
  "weak_areas": [ {"code": "問3", "name": "…", "section": "言語知識", "percentage": 33.3, "advice": "…"} ],
  "detail_gengo":  {"1": {"correct": 4, "user": 2, "is_correct": false}},
  "detail_choukai": {"問1-1": {"correct": 2, "user": null, "is_correct": false}}
}
```

The result screen renders 総合判定, 得点サマリー, 大問別詳細分析,
全設問解答チェック表. 大問 ratings: `優` (≥80%), `良` (60–79%), `要強化`
(<60%) — plain text, no emoji. **These bands are a repo-internal study
diagnostic, not the official 参考情報** (the real 合否結果通知書 reports A/B/C
only for 文字・語彙/文法, 合否判定の対象外) — keep the distinction; aligning
the two means changing both graders plus the parity test.

## Verification

```bash
make check            # the real gate — asserts everything below, every test on disk
```

Booklets: `verify()` on every build. Sheet: 101 radio groups, every expected
key present, no shared group name, 4 options per gengo question and 3 for
問題4 (393 inputs total), no emoji in report labels, and the in-page grader
matching `grade_answers.py`'s `採点結果.json` field for field. Deployments:
both screen-1 renderers go through `index_view`; the localStorage prefix
lives in exactly one module; every `解答.html` is the server build; `_site/`
is gitignored with `.nojekyll`.

Two option-counting bugs the sheet checks were written to prevent (both
shipped and made the exam partly unanswerable): **one bubble per horizontal
question** (`option_run()` counts a consecutive `1..k` run only, so
`1. 価格が3.5倍…` isn't miscounted), and **問題5's 質問1/質問2 colliding with
1番** — 質問N always belongs to 2番 whenever the section is 問題5, in both
parser paths.

Manual spot-check after a parser change:
`python3 .agents/exam-app/scripts/build_interactive.py tests/1` — expect
exactly 101 items, zero warnings. After any scoring JS change, `make check`
runs the parity check (extracts the last `<script>`, stubs the DOM, calls
`computeResult()` under node, compares with `grade_answers.result_payload()`).

## Environment

`python3 -m pip install markdown pykakasi` plus Noto CJK JP fonts. **No PDF
toolchain** — no weasyprint, no wkhtmltopdf, no poppler.
