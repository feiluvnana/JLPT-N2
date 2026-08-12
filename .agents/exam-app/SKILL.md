---
name: exam-app
description: Single owner of rendering and running the exam. Owns the whole app surface — Markdown sources → booklet HTML with A4 print geometry and furigana helpers (NO PDF, ever), the MERGED problem+answer sheet 解答.html with radio bubbles, an embedded 聴解 audio player and in-page 180-point grading, the ONE local server and test list, the static GitHub Pages build that keeps answers in localStorage, and CLI grading (scaled 0–180 scores, pass/fail evaluation, 採点結果.json) via grade_answers.py. Use whenever generating/regenerating/fixing exam booklets or formatting (answers squashed on one line, cramped spacing, furigana misaligned, tables splitting across pages); whenever the user wants to take/answer/solve a test on screen, mentions the answer sheet, マークシート, 解答用紙, the test list, playing the listening audio while answering, or publishing/hosting the exam on GitHub Pages; and whenever the user asks to grade, score, check answers, 採点, 答え合わせ, or analyze exam results.
---

# Exam App (冊子レンダリング・解答用紙・サーバー・採点)

One skill owns the whole app — booklet rendering, the merged problem+answer
sheet, the server, the static Pages twin, and grading — all in
`.agents/exam-app/scripts/`:

| Script | Job |
| - | - |
| `build_booklet.py` | Markdown → booklet HTML (`言語知識・読解.html`, `聴解.html`); owns the shared CSS and ruby/furigana helpers |
| `build_interactive.py` | Markdown → `解答.html`, the merged sheet with in-page grading; also the `--keyless` QA render |
| `serve_sheet.py` | the ONE local server: test list, exam, results, saved into `tests/<id>/` |
| `build_pages.py` | the static GitHub Pages build into `_site/` |
| `grade_answers.py` | CLI grading twin: scaled scores, pass/fail, `採点結果.json` |
| `app_style.py`, `index_view.py`, `local_store.py` | shared modules — see "Shared modules" below |

## Shared modules — one copy of everything, now all siblings

- `app_style.py` holds `APP_CSS`, the app chrome; **both** builders import it
  (`index_view.py` for screen 1, `build_interactive.py` for screens 2–3). Add
  chrome there, never in either script — two copies of "the same" CSS is how
  designs drift, and no gate can see a drifted colour. `APP_CSS` must stay free
  of bare element selectors: 解答.html loads it on top of the booklet stylesheet.
- `index_view.py` — screen 1's CSS, cards and actions, fed the same test objects
  by `/api/tests` (server) or a baked manifest + localStorage (Pages).
  `make check` fails if `INDEX_CSS` is defined anywhere else.
- `local_store.py` — `window.JLPTStore`, the localStorage backend, the ONLY
  place the key schema is written down; keys spell out the files they stand in
  for.
- `build_interactive.py` imports `build_booklet.py`'s `CSS`, `SCREEN_CSS`,
  `widen()`, `fit_ruby()` and `mark_furigana_blocks()` so the sheet and the
  booklet render identically — **sibling imports now**, both files live in this
  skill's `scripts/`; changing any of them changes both, rebuild both.
  `add_choukai_furigana()` is NOT shared: `build_booklet.py` applies it only to
  聴解-named files, so `聴解.html` carries auto-furigana the 聴解 half of
  `解答.html` lacks — a known rendering difference, not an import bug.
- `build_pages.py` calls `build_interactive.build()` rather than copying
  `tests/<id>/解答.html`, which would ship a sheet POSTing to an API that does
  not exist on Pages.

## Execution

```bash
# Booklets: Markdown (source of truth) → python-markdown → styled HTML. No PDF.
python3 .agents/exam-app/scripts/build_booklet.py tests/<id>/言語知識・読解.md tests/<id>/聴解.md
# or: make booklet <id>
# The merged problem+answer sheet:
python3 .agents/exam-app/scripts/build_interactive.py tests/<id>
# or: make sheet <id>     (--storage local / --out DIR are the Pages build's)
# Serve every test — list, exam, results — saving directly into tests/<id>/:
python3 .agents/exam-app/scripts/serve_sheet.py
# or: make serve          (options: --port 8765, --no-open; takes NO test id)
# The static twin for GitHub Pages — same screens, answers in localStorage:
python3 .agents/exam-app/scripts/build_pages.py
# or: make pages          (then: make preview-pages)
# The QA blind-solve render — the same paper, no keys, no sheet:
python3 .agents/exam-app/scripts/build_interactive.py tests/<id> --keyless
# or: make keyless <id>   (→ qa/<id>/keyless.md)
# CLI grading (the in-page grader is the normal path — this is its twin):
python3 .agents/exam-app/scripts/grade_answers.py --test-dir tests/<id>
# or: make grade <id>     (inline: --answers-gengo "1:4,…" --answers-choukai "問1-1:2,…")
```

Re-run the booklet build AND the sheet build after ANY edit to the `.md`
sources: they are the single source of truth and are never deleted — the grader
parses answer keys out of them and the sheet builder parses questions out of
them. Editing HTML by hand is always wrong.

## Booklet rendering (`build_booklet.py`)

`tests/<id>/言語知識・読解.md` + `tests/<id>/聴解.md` → `言語知識・読解.html` +
`聴解.html` in the same folder. That is the whole pipeline. **No PDF.**

### Why no PDF — this rule lives here now

`@page { size: A4 }` and the page-break rules stay in the CSS, so **Cmd-P from
the browser gives the same A4 booklet**. Removing the PDF step removed a real
defect class: WeasyPrint and wkhtmltopdf laid the absolute-positioned `<rt>`
out differently, so whichever happened to be on PATH silently changed the
furigana output. The browser is now the only renderer. **Never reintroduce
weasyprint/wkhtmltopdf** (or poppler — no PDF toolchain at all).

### Non-negotiables baked into the script (know WHY they exist)

1. **`nl2br` extension is mandatory.** Markdown joins consecutive lines into one
   paragraph; without nl2br every vertically-stacked option list collapses onto
   a single unreadable line. (This was a real user complaint.)
2. **CJK fonts**: body = Noto Serif CJK JP (real booklets are serif/明朝),
   headings/bold = Noto Sans CJK JP. Verify: `fc-list | grep -i "noto.*cjk"`.
3. **Option widening**: lines holding 3+ options (`1. ◯ 2. ◯ 3. ◯ 4. ◯`) get
   three IDEOGRAPHIC spaces (U+3000) inserted between options — HTML collapses
   ASCII spaces but preserves U+3000. Regular double-spaces are NOT enough.
4. **Table styling**: `table { width: 100%; border-collapse: collapse;
   page-break-inside: avoid; }` for full-width exam tables.
5. **Page-break control**: `page-break-inside: avoid` on tables/blockquotes,
   `page-break-after: avoid` on headings. line-height ≥ 1.9 for Japanese.
6. Layout follows `jlpt-exam-structure`: horizontal options for
   文字・語彙・文法, vertical for 聴解 and 問題6.
7. **Ruby furigana**: `<ruby>漢字<rt>かんじ</rt></ruby>` passes through
   python-markdown into styled HTML. The stack is done by hand, not with
   `ruby-position` (the old PDF renderers ignored it and dropped the base
   below the reading — the original misalignment bug), and is kept because it
   renders identically everywhere and `fit_ruby()` depends on it: `ruby` is an
   `inline-block` (`position: relative; line-height: 1` — anything taller
   floats the reading away from the kanji), `rt` is `position: absolute;
   bottom: calc(100% + 0.1em)`, `left/right: -0.6em`. Two Python passes
   support it: `fit_ruby()` gives ruby a `min-width` when the reading is wider
   than its base, and `mark_furigana_blocks()` adds `class="furi"`
   (line-height 2.1) only to blocks containing ruby.
8. **Vocabulary notes** (`（注1）…`) use `.vocab-notes` styling (9pt,
   line-height 1.6, top dashed border) to replicate the official Dokkai layout.
9. **`add_choukai_furigana()`'s pykakasi output is not trustworthy as-is** —
   a 2026-08 audit of shipped `聴解.html` found real, wrong readings in it:
   a bare `人` token came back `にん` instead of `ひと` (every genuine `にん`
   compound like 三人/本人/友人 is long enough that kakasi already merges it
   into one token, so a standalone `人` is always "hito"); a `方` token right
   after hiragana (伝わり方, 使い方, …) came back `ほう` instead of `かた`
   (genuine `ほう` compounds like 一方/先方 have `方` glued to a preceding
   *kanji*, so this never fires on those); and `小さい`/`小さく`/`小さかった`
   came back with a bogus chouon (`ちーさい`) — a `kks.convert()` dictionary
   bug. All three are now corrected by `fix_hira()` inside
   `add_choukai_furigana()`. If you touch that function again, or add a new
   choukai test and spot another wrong reading, add the fix there (not a
   one-off patch on the generated HTML) and rebuild every test's `聴解.html`
   with `make booklet <id>` so the fix isn't test-specific.

`SCREEN_CSS` is the screen-only shell: a centered 60 em column (an unbounded
full-width line is unreadable on a monitor) plus a `--gutter` variable the
sheet's sticky bar and audio player pull out to — entirely inside
`@media screen`, so the `@page` A4 geometry is untouched.

### verify() — automatic, aborts the build

`build_booklet.py` runs `verify()` on every build and **aborts** on: mojibake
(any `�`); an `<ol>` in the output (a stem used `N.` list syntax, which
restarts numbering at 1 per section — stems must be bold `**6**`, `**11**`);
or a missing bold stem for any of questions 1–71 in `言語知識・読解.html`
(how a dropped or mis-numbered question gets caught). Still check by eye that
the key/explanation tables render at the end of both files and that furigana
sits over its base; Cmd-P to preview the A4 pagination.

## The three screens

The exam merges the problem booklet and radio bubbles into one deliverable
(`解答.html`): you answer **inside the booklet**, press 「採点する」, and the
complete 180-point result appears immediately. One server covers every test
(`make serve` takes no test id); the same three screens also ship as a static
site for GitHub Pages — only where the answers are kept differs.

| # | Screen | Where it lives | What it does |
| - | ------ | -------------- | ------------ |
| 1 | テスト一覧 | `GET /` — `serve_sheet.py` | Every test in `tests/`, with answered count (of 101), last score, and an **origin badge** (`imported` if the folder starts with `imported-`, else `generated`). Links to screen 2, or straight to screen 3 for a graded test |
| 2 | 受験 | `GET /tests/<id>/解答.html` — `build_interactive.py` | The exam. Each click autosaves; 「← 一覧」 returns to screen 1 |
| 3 | 採点結果 | same page, `#screen-result` | Rendered from the result object on 「採点する」, or fetched from `採点結果.json` when the URL carries `?screen=result`. Its buttons sit at the END of the page — the bar already carries the way out |

A graded test is never locked: 「解答に戻ってやり直す」 (or 「もう一度解く」 on
the list) reopens screen 2 with the saved answers still selected, and
re-grading overwrites `採点結果.json`. `解答.html` is the deliverable you solve
on; it is NOT the booklets `言語知識・読解.html` / `聴解.html`, which
`build_booklet.py` overwrites on every build, and there are no per-section
`*_解答.html` files.

## Grading — press 「採点する」 (in-page: the normal path)

Pressing the button: (1) grades all 101 questions against embedded keys,
(2) evaluates section cutoffs (≥19/60) and total threshold (≥90/180),
(3) switches to screen 3 and renders the result, (4) **saves to whichever store
this build uses** (`採点結果.json` and `ユーザー解答.json`): into `tests/<id>/`
under `make serve`, into localStorage on a Pages build, and — with no server
and no store, e.g. bare `file://` — as browser downloads of the same two JSON
files. If anything is unanswered the button asks for confirmation; unanswered
items appear as 「未解答」 chips, not as wrong.

**全設問解答チェック表 expands as one list.** 「すべての設問詳細を展開」builds
detail blocks for all 101 items at once, cloning each item's problem text from
the still-in-DOM `#screen-exam` plus あなたの答え / 正解; extraction is
display-only (`extractQuestionHtml` / `buildAllDetailsHtml`).

### One source of truth for the grading data

The in-page grader is the normal path; **`grade_answers.py` is its CLI twin**
(offline/batch runs, re-grading a saved `ユーザー解答.json`), and the gate's
parity check keeps them honest: `computeResult()` returns the **same document
`grade_answers.py` writes**, stays free of DOM and `Date`, and `make check`
executes it under node and compares with the Python grader **field for field**.
There is no Markdown report — the result is data, read back by the result
screen and the test list; do not add a report back.

`ANSWER_KEY`, `TAXONOMY`, `ADVICE` and the section definitions are **serialized
out of `grade_answers.py` at build time** (`GENGO_QUESTION_TAXONOMY`,
`CHOUKAI_QUESTION_TAXONOMY`, `ADVICE_FOR`). Never hand-write those tables into
the JS — a second copy is exactly how the grader's 大問 ranges drifted from
`jlpt-exam-structure` once already. Keep those structures serializable, and
re-run `build_interactive.py` after changing any of them. Listening keys come
from `grade_answers.parse_choukai_keys()` itself, so the emitted JSON can never
drift from what grading expects.

## The answer key must never be VISIBLE — one truncation, three build modes

The key is embedded as JS data so grading works offline — but it must never be
_rendered_. **`strip_key()` truncates everything from the key heading
(`KEY_HEADING`, the `# 解答…` / `# 【正解…` regex) onward out of the document
body, and the builder exits with an error if it cannot find that heading** —
never "fix" that by loosening the check. The trade-off is deliberate: the key
is reachable via devtools, which is acceptable for a self-study mock (it is in
`聴解.md` next door anyway); what matters is that it is not on screen while you
solve. Everything the script emits goes through the same `strip_key()`, so
there is one place to get it right and one place that aborts.

| Mode | Command | Writes | Keys |
| - | - | - | - |
| server sheet (default) | `make sheet <id>` | `tests/<id>/解答.html` | embedded as JS data, never rendered |
| Pages sheet | `make pages` → `build_pages.py` calls `build(storage='local')` | `_site/tests/<id>/解答.html` | same |
| **keyless render** | `make keyless <id>` (`--keyless`) | `qa/<id>/keyless.md` | **none, anywhere in the file** |

### `--keyless` — the QA blind-solve render

`exam-qa-review`'s first ground rule is "blind-solve before reading the keys",
and it was not executable: the keys live at the END of the same two Markdown
files the paper lives in, so every earlier QA pass was half-blind (test-4 root
cause **R20**). `--keyless` emits the whole paper and nothing else: both
booklets through `strip_key()`, plus `聴解スクリプト.txt` verbatim so 聴解 is
solvable without the audio. It embeds no key data at all — no JS, no key
object — and re-scans its own output with `KEY_HEADING`, refusing to write a
render that still carries a key heading. The header carries the `sha1[:12]` of
each source — exactly what `exam-qa-review`'s report header must name; solve,
rebuild when done, check the shas have not moved. **It is not a deliverable**:
`tests/<id>/` has a fixed file contract (`AGENTS.md` §2), so the render lands
in `qa/<id>/keyless.md` (gitignored), beside the QA report that consumes it.

## Audio player (聴解 only)

- `<audio src="聴解.mp3">` is referenced **relatively**, never embedded (a
  ~30 MB MP3 as base64 would be ~40 MB of HTML). Controls: play/scrub, ±10 s,
  playback speed (0.75–1.5), chapter dropdown.
- **Chapter marks** come from `聴解_チャプター.json`, written during MP3
  synthesis (exact assembler offsets, not silence-detection guesses). If
  absent, the dropdown hides itself and everything else works — the builder
  prints a note to re-run the generator.
- Some browsers block `file://` media subresources: a 「MP3を選ぶ」 file picker
  is always present as fallback, and the player turns red with an instruction
  if `<audio>` errors. Never require a web server.

## Serving (`serve_sheet.py`) — five things it must keep doing

1. **One server, every test.** Started with no arguments, serves the whole
   `tests/` tree; routes: `/` (list), `/api/tests` (same list as JSON),
   `/tests/<id>/…` (static, range-aware), `POST /api/tests/<id>/answers`,
   `POST /api/tests/<id>/submit`, `POST /api/tests/<id>/clear` (deletes
   `採点結果.json` + `ユーザー解答.json` from the list's 「結果を削除」). Only
   paths under `tests/` are reachable.
2. **Screen 1 reads the disk, never a cache.** Progress comes from
   `ユーザー解答.json` / `採点結果.json` in each test dir; the page is the
   shared shell from `index_view.py` and the live read is `GET /api/tests`,
   which carries `Cache-Control: no-store` — a stale list is worse than none.
   Cards share one fixed height; the sticky `#bar` is the same fixed height on
   all three screens.
3. **Range requests.** `聴解.mp3` is ~30 MB and `<audio>` re-requests it with
   `Range:` on every seek; `SimpleHTTPRequestHandler` ignores Range, which made
   seeking slow. The handler answers `Range:` itself with `206 Partial Content`
   (`416` when unsatisfiable) and advertises `Accept-Ranges: bytes` on GETs.
4. **Client disconnects are not errors.** Every abort (a seek, a closed tab)
   kills the socket mid-`copyfile`; `handle()` and `finish()` swallow
   `BrokenPipeError`/`ConnectionResetError`. Do not re-raise a broken pipe;
   the request is simply over.
5. **Threaded.** `ThreadingHTTPServer`, because a single-threaded server queues
   the 採点する submit behind whatever MP3 stream is in flight.

## Two deployments, one app — `make serve` and GitHub Pages

The exam runs in two places, and they are **the same three screens with two
storage backends**, never two apps:

| | `make serve` (local) | GitHub Pages (`make pages`) |
| - | - | - |
| Screen 1 | `serve_sheet.py` renders the shell, `GET /api/tests` reads the disk | `_site/index.html`, same shell, progress read from localStorage |
| Screens 2–3 | `tests/<id>/解答.html`, `--storage server` | `_site/tests/<id>/解答.html`, `--storage local` |
| Answers | `tests/<id>/ユーザー解答.json` via `POST /api/…` | `localStorage[jlpt-mock/v1/<id>/ユーザー解答.json]` |
| Result | `tests/<id>/採点結果.json` via `POST /api/…` | `localStorage[…/採点結果.json]` |
| 「← テスト一覧」 | `/` | `../../index.html` (Pages serves from `/<repo>/`) |

```bash
make pages            # every test → _site/   (make pages 1 for one test)
make preview-pages    # python3 -m http.server -d _site 8766
```

`.github/workflows/pages.yml` runs exactly that on push and deploys the
artifact. `_site/` is **gitignored**: CI rebuilds it from `tests/`, so the site
is never committed and `tests/` stays the single source. The MP3s are copied in
beside each sheet (~30 MB per test) — the slow part; `--no-audio` skips them.
Pages' CDN answers `Range:` so seeking is cheap there; `make preview-pages`
uses `python3 -m http.server`, which does not — a preview limitation only.

**One store per build — the rule that has not changed.** Exactly one storage
backend is live per build, chosen at BUILD time
(`build_interactive.py --storage server|local`), **never sniffed at runtime**,
and only the live one is emitted into the page: a server sheet does not even
contain the localStorage code. Two live stores is the failure this rule exists
to prevent — the list counting one set of answers while the sheet shows
another. `make check` asserts every `tests/<id>/解答.html` is always the
**server** build and carries no store prefix; the local build belongs in
`_site/` only.

**What Pages cannot do, and what stands in for it.** No disk: nothing lands in
`tests/<id>/` and `grade_answers.py` has nothing to read. Local builds
therefore grow a 「採点結果を保存（JSON）」 button (screen 3) and
「バックアップを保存」/「バックアップを読み込む」 (screen 1) — one JSON holding
every test's two documents, also how answers move between browsers. Say so on
the page (the Pages lede does): clearing site data loses the lot.

## On-screen layout — one design across three screens

Screens 2–3 keep the booklets' centered **60em** measure (`SCREEN_CSS`), moved
off `<body>` onto `#screen-exam` / `#screen-result` so the bar spans the window
like screen 1. Screen 1's `<main>` is wider (**80em**) for the test cards; do
not widen the exam/result columns to match, and do not "simplify" to
`width:100vw` — it includes the scrollbar and shoved 「採点する」 off-screen
(`#bar`'s generous horizontal padding exists for the same reason). All inside
`@media screen`, so Cmd-P still prints the A4 booklet. The bar names where you
are: `initSpy()`/`updateSpy()` track the nearest heading above the bar and show
「聴解 ｜ 問題2」 — the exam is one very long page. `fitPlayer()` measures the
bar and sets the player's sticky offset from it; never hard-code that offset.

## Answer capture

**Every radio click** writes progress to the one place this build uses: under
`make serve`, `tests/<id>/ユーザー解答.json` via `POST /api/tests/<id>/answers`
(debounced ~250 ms), read back on reload; on a Pages build, the matching
localStorage key and nothing else. Screen 1 counts that same one place, and
everything between the radio and the store goes through `STORE`, so nothing in
the page knows which backend it talks to. 「採点する」 writes `採点結果.json`
plus the same `ユーザー解答.json` shape `grade_answers.py` reads:
`{"言語知識_読解": {"33": 2, …}, "聴解": {"問1-1": 2, …}}`.

## Parser contract (why the Markdown conventions are load-bearing)

The builders locate questions in the Markdown, so the formatting conventions
are the renderer's contract; content and format authoring rules live with
`question-authoring` and `jlpt-exam-structure`. What the parsers require:

- 言語知識: `**33** stem` then indented ` 1. … 2. …` option lines, OR 問題6's
  `**28 募集**`, OR 問題9's all-on-one-line `**50** 1. こと  2. だけ …`.
  **問題7 dialogue stems may span lines** after `**N**` (setting `（会社で）`,
  then `A「…」` turns) before the option row: `inject_gengo` must keep `cur`
  across those stem lines — flushing on every non-option line used to drop
  radios for Q32/39/40/41/42.
- 聴解: `**1番**` + indented options (問題1/2 only — the two sections that print
  their choices), OR a bare bubble row `**1番** 1 ・ 2 ・ 3 ・ 4` for the
  問題3/4/5 items that print nothing. **All of 問題5 takes the bubble-row form,
  `**質問1**`/`**質問2**` included** — this repo prints no options for either of
  its items (`jlpt-exam-structure` §聴解), so 質問N is a bubble row, not a
  `**質問1**` heading over an option list.
- `**例**` rows get a STATIC row with the answer already filled in, never
  radios — the 例 is a demonstration, not a scored item. The number comes from
  the `解答用紙` grid's `**(n)**` cell (`example_premarks()`), read BEFORE
  `strip_key` truncates that grid away; `jlpt-exam-structure` requires the
  pre-mark, and `make check` asserts it equals the announced number.
- **The builder warns loudly** when a question gets no radio group
  (`no radio group for …`) or a group has no key. Treat either warning as a
  bug in the Markdown, never as noise — a silently missing group means that
  question can never be answered or scored.

## CLI grading (`grade_answers.py`)

Parses the keys from the two Markdown sources, reads examinee responses, and
writes `tests/<id>/採点結果.json`. **User answers are auto-discovered**:
`ユーザー解答*.json` in the test dir and cwd (several matching files merge);
inline `--answers-gengo` / `--answers-choukai` override.

- **Scaled 0–180 scoring**: raw section counts → 0–60 per section —
  言語知識 (51 items), 読解 (20 items), 聴解 (30 answers; 問題5の2番 yields
  two).
- **The scale is proportional, an approximation — and say so.** The real exam
  equates scores across sittings (得点等化), which needs item statistics we do
  not have. Proportional scaling is the honest stand-in for a mock; never
  describe its output as a real JLPT score, and never "improve" it with
  invented difficulty weights.
- **Pass/fail (published JLPT N2 criteria)**: total ≥ 90/180 AND every section
  ≥ 19/60 (基準点). Failing any single sectional cutoff is 不合格 regardless
  of total — always enforce it.
- **Taxonomy**: the 大問 → question ranges are owned by `jlpt-exam-structure`;
  the code owner is `GENGO_QUESTION_TAXONOMY` in `grade_answers.py`, which
  asserts at import that its ranges tile 1–71 with no gap or overlap. No copy
  of the table lives in this doc.
- **Advice integrity**: weak-area advice must map to the corresponding
  _Shin Kanzen Masuta N2_ study area (`refs/Shinkanzen/`).

## Result document (`採点結果.json`) — the schema is a contract

The result is **data, not prose**. `解答.html` and the test list read this file
back; `result_payload()` in `grade_answers.py` is its only Python definition,
`computeResult()` builds the identical structure, and `make check` compares the
two field for field:

```jsonc
{
  "test_id": "1",
  "graded_at": "2026-08-05T09:12:33+00:00",   // the ONLY field allowed to differ between graders
  "summary": {
    "passed": false,                           // overall >=90 AND every section >=19
    "total_scaled_score": 118, "max_scaled_score": 180,
    "cutoff_passed": true, "overall_threshold_passed": true,
    "sections": {                              // keyed by section name
      "言語知識（文字・語彙・文法）": {"raw_correct": 33, "raw_total": 51,
                                     "scaled_score": 39, "cutoff": 19, "passed_cutoff": true},
      "読解":   {"raw_correct": 14, "raw_total": 20, "scaled_score": 42, "cutoff": 19, "passed_cutoff": true},
      "聴解":   {"raw_correct": 20, "raw_total": 30, "scaled_score": 40, "cutoff": 19, "passed_cutoff": true}
    }
  },
  "taxonomy_stats": {                          // per 大問; empty 大問 are omitted
    "問1": {"name": "漢字読み (Kanji Reading)", "section": "言語知識",
            "correct": 3, "total": 5, "percentage": 60.0}
  },
  "weak_areas": [                              // percentage < 60, with the study advice
    {"code": "問3", "name": "…", "section": "言語知識", "percentage": 33.3, "advice": "…"}
  ],
  "detail_gengo":  {"1": {"correct": 4, "user": 2, "is_correct": false}},   // all 71
  "detail_choukai": {"問1-1": {"correct": 2, "user": null, "is_correct": false}}
}
```

The result screen renders it into 総合判定, 得点サマリー, 大問別詳細分析,
全設問解答チェック表. Its 大問 ratings are the labels both graders agree on:
`優 (Strong)` (≥80%), `良 (Fair)` (60–79%), `要強化 (Weak)` (<60%) — plain
text, no emoji. **These bands are a repo-internal study diagnostic, not the
official 参考情報**: the real 合否結果通知書 reports A (≥67%) / B / C (<34%),
only for 文字・語彙 and 文法, and is 合否判定の対象外; ours rates every 大問
on 80/60 because the point is "what to revise next". Keep the distinction;
aligning the two means changing both graders plus the `make check` parity test.

## Verification

```bash
make check            # the real gate — asserts everything below, every test on disk
```

On the booklets: `verify()` runs on every build (above). On the sheet: **101
radio groups**, every expected key present, no group name shared by two
questions, 4 options per gengo question and 3 for 問題4 (393 inputs total), no
emoji in report labels, and the in-page grader and `grade_answers.py` producing
an **identical `採点結果.json`** (every field but the timestamp) on the same
simulated answers. On the two deployments: both screen-1 renderers go through
`index_view` and nobody else defines `INDEX_CSS`; the localStorage prefix lives
in exactly one module; every `tests/*/解答.html` is the server build with no
store prefix; `_site/` is gitignored with `.nojekyll` written; `make pages` /
`make preview-pages` exist and are documented here.

Two option-counting bugs the sheet checks were written to prevent (both
shipped and made the exam partly unanswerable): **one bubble per horizontal
question** — 問題1–8 print all four choices on one line and the group got
`width=1`; `option_run()` counts a consecutive `1..k` run on the line (a
consecutive run only, so `1. 価格が3.5倍…` is not miscounted) — and **問題5's
質問1/質問2 colliding with 1番**, which made two items unanswerable; 質問N
always belongs to 2番 whenever the section is 問題5. That second rule holds in
BOTH parser paths — the `**質問1**`-heading path and the bubble-row path — and
the bubble-row path is the one every current test takes.

Manual spot-check after a parser change:
`python3 .agents/exam-app/scripts/build_interactive.py tests/1` — expect
exactly 101 items (71 Gengo/Dokkai, 30 Choukai), zero warnings. After ANY
change to the scoring JS, the parity check must run — in practice: run
`make check` (it extracts the last `<script>` block, stubs the DOM, calls
`computeResult()` under node, and compares with `grade_answers.result_payload()`).

## Environment

`python3 -m pip install markdown pykakasi` plus the Noto CJK JP fonts. **No PDF toolchain** — no weasyprint, no wkhtmltopdf, no poppler.
