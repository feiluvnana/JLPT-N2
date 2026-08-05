---
name: interactive-answer-sheet
description: Single owner of the MERGED problem+answer sheet — the complete exam booklet (言語知識・読解 and 聴解) rendered into a single HTML file (解答.html) with radio bubbles beside every choice and an embedded audio player for 聴解 — and of the one server that lists every test, runs them, and shows their results. Use whenever the user wants to take/answer/solve a test on screen, mentions the answer sheet, マークシート, 解答用紙, selecting answers, the test list, or playing the listening audio while answering. Grades the full 180-point exam in-page on button press and saves 採点結果.json and ユーザー解答.json directly.
---

# Interactive Answer Sheet (問題用紙＝解答用紙)

## Why this skill exists

The exam merges the problem booklet and interactive radio bubbles into a single unified deliverable (`解答.html`). You answer **inside the booklet**, press 「採点する」, and the complete 180-point JLPT result appears immediately and is saved as `採点結果.json`.

## The three screens

One server (`serve_sheet.py`) covers every test in `tests/`. There is no
per-test server: `make serve` takes no test id.

| # | Screen | Where it lives | What it does |
| - | ------ | -------------- | ------------ |
| 1 | テスト一覧 | `GET /` — built by `serve_sheet.py` | Every test in `tests/`, each with its answered count (out of 101) and last score. Links to screen 2, or straight to screen 3 for a graded test |
| 2 | 受験 | `GET /tests/<id>/解答.html` — built by `build_interactive.py` | The exam. Each click autosaves; 「← 一覧」 returns to screen 1 |
| 3 | 採点結果 | in the same page, `#screen-result` | Rendered from the result object on 「採点する」, or fetched from `採点結果.json` when the URL carries `?screen=result`. Its buttons (「← テスト一覧へ戻る」/「解答に戻ってやり直す」) sit at the END of the page — the bar already carries the way out, so a second nav row above the report only pushes the report down |

A graded test is never locked: 「解答に戻ってやり直す」 (or 「もう一度解く」 on the
list) reopens screen 2 with the saved answers still selected, and re-grading
overwrites `採点結果.json`.

## Execution

```bash
python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/<test_id>
# or: make sheet <test_id>

# Serve every test — list, exam, and results — with direct saving into tests/<id>/:
python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py
# or: make serve            (options: --port 8765, --no-open)
```

Outputs into `tests/<test_id>/`:

| File        | Contents                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------- |
| `解答.html` | Full exam (71 Gengo/Dokkai questions + 30 Choukai items + Audio player, in-page 180pt grading) |

Re-run after ANY edit to `言語知識・読解.md` / `聴解.md` — the Markdown stays
the single source of truth, exactly as for the booklet HTML.

## Grading & Direct Saving — press 「採点する」

Pressing the button:

1. grades the full 101 questions immediately against embedded keys (Language Knowledge, Reading, Listening),
2. evaluates section cutoffs ($\ge 19/60$) and total threshold ($\ge 90/180$),
3. **switches to screen 3** and renders the result there, and
4. **saves directly to `tests/<test_id>/`** (`採点結果.json` and `ユーザー解答.json`) if served via `make serve`, or downloads both JSON files if opened standalone.

If anything is unanswered the button asks for confirmation first, and
unanswered items appear as 「未解答」 chips in the check grid rather than as wrong.

### The result is data, not prose

`computeResult()` returns the **same document `grade_answers.py` writes** — the
`採点結果.json` shape (`summary`, `taxonomy_stats`, `weak_areas`,
`detail_gengo`, `detail_choukai`). Nothing else in the page scores anything, and
`resultHtml()` only formats what `computeResult()` returned. Keep
`computeResult()` free of DOM and `Date`: `make check` executes that exact
function under node and compares its output with the Python grader **field for
field**, not just on totals, because both screens and the test list read the
same file. There is no Markdown report any more — do not add one back.

### One source of truth for the grading data

`ANSWER_KEY`, `TAXONOMY`, `ADVICE` and the section definitions are **serialized
out of `grade_answers.py` at build time** (`GENGO_QUESTION_TAXONOMY`,
`CHOUKAI_QUESTION_TAXONOMY`, `ADVICE_FOR`). Never hand-write those tables into
the JS — a second copy is exactly how the grader's 大問 ranges drifted from
`jlpt-exam-structure` in the first place.

## The answer key must never be VISIBLE

The key is embedded as JS data so grading can happen offline with no server —
but it must never be _rendered_. The builder truncates everything from the key
heading (`# 解答…` / `# 【正解…`) onward out of the document body, and **exits
with an error if it cannot find that heading**. Never "fix" that by loosening
the check. The trade-off is deliberate: the key is reachable via devtools by
someone who goes looking, which is acceptable for a self-study mock (the key
is in `聴解.md` next door anyway); what matters is that it is not on screen
while you solve.

`解答.html` is the deliverable you solve on, and it is NOT the same file as the
booklets `言語知識・読解.html` / `聴解.html`, which `build_booklet.py` overwrites
on every booklet build. There are no per-section `*_解答.html` files — one
merged sheet covers the whole exam.

## Audio player (聴解 only)

- `<audio src="聴解.mp3">` is referenced **relatively**, never embedded — a
  ~30 MB MP3 inlined as base64 would be ~40 MB of HTML.
- Controls: play/scrub, ±10 s, playback speed (0.75–1.5), and a chapter
  dropdown.
- **Chapter marks** come from `聴解_チャプター.json`, written by
  `choukai-mp3-generation` during synthesis (exact offsets from the
  assembler, not silence-detection guesses). If the file is absent the
  dropdown hides itself and everything else still works — the builder prints
  a note telling you to re-run the MP3 generator.
- Some browsers block `file://` media subresources. A **「MP3を選ぶ」** file
  picker is always present as a fallback, and the player turns red with an
  instruction if the `<audio>` element errors. Never require a web server.

## Serving (`serve_sheet.py`) — five things it must keep doing

1. **One server, every test.** It is started with no arguments and serves the
   whole `tests/` tree; the routes are `/` (list), `/api/tests` (the same list
   as JSON), `/tests/<id>/…` (static, range-aware),
   `POST /api/tests/<id>/answers` and `POST /api/tests/<id>/submit`. Only paths
   under `tests/` are reachable, so the repo is not on the web.
2. **Screen 1 reads the disk, never a cache.** Progress comes from
   `ユーザー解答.json` and `採点結果.json` in each test dir, and the index is
   sent `Cache-Control: no-store` — a stale list is worse than no list.
3. **Range requests.** `聴解.mp3` is ~30 MB and the `<audio>` element re-requests
   it with `Range:` on every seek. `SimpleHTTPRequestHandler` ignores Range and
   restreams the whole file, so the browser cancelled each previous transfer:
   seeking was slow and the console filled with aborted downloads. The handler
   answers `Range:` itself with `206 Partial Content` (`416` for an
   unsatisfiable range) and advertises `Accept-Ranges: bytes` on GETs.
4. **Client disconnects are not errors.** Every abort — a seek, closing the tab,
   a paused buffer — kills the socket mid-`copyfile` and used to print a
   `BrokenPipeError` traceback per abort. `handle()` and `finish()` swallow
   `BrokenPipeError`/`ConnectionResetError`. Do not "fix" a broken pipe by
   re-raising it; the request is simply over.
5. **Threaded.** `ThreadingHTTPServer`, because a single-threaded server queues
   the 採点する submit behind whatever MP3 stream is in flight — the submit
   appeared to hang while the audio buffered.

## On-screen layout — one design across three screens

`app_style.py` holds `APP_CSS`, the shared chrome, and **both** builders import
it: `serve_sheet.py` for screen 1, `build_interactive.py` for screens 2 and 3.
Two scripts producing "the same" design from two copies of the CSS is exactly
how they drift, and no gate can see a drifted colour. Add chrome there, not in
either script. `APP_CSS` must stay free of bare element selectors — 解答.html
loads it on top of the booklet stylesheet.

The sheet also imports `SCREEN_CSS` from `build_booklet.py` so the exam text
keeps the booklets' centered 60 em measure (unreadable line lengths otherwise on
a wide monitor). But the measure is moved off `<body>` onto `#screen-exam` /
`#screen-result`, because **the bar must span the window exactly as it does on
screen 1** and a bar inside a centered body cannot. Do not "simplify" that back
to `width:100vw`: `100vw` includes the scrollbar, so the bar overflowed and
「採点する」 fell off the right edge. `#bar` also carries generous horizontal
padding for the same reason — the scrollbar sits on its right edge.

It is all inside `@media screen` — the A4 `@page` geometry is untouched, so
Cmd-P still prints the booklet.

The bar names where you are: `initSpy()`/`updateSpy()` track the nearest heading
above the bar and show 「聴解 ｜ 問題2」. The exam is one very long page, so
without it there is no way to tell which 大問 you are in but to scroll back.
`fitPlayer()` measures the bar and sets the player's sticky offset from it —
never hard-code that offset, it depends on the font and on whether the bar wraps.

## Answer capture

- **Every radio click** writes progress to one place: `tests/<test_id>/ユーザー解答.json`
  via `POST /api/tests/<id>/answers` when served with `make serve` (debounced
  ~250 ms so rapid clicks do not thrash the disk). On reload the sheet loads that
  same file with `fetch('ユーザー解答.json')` — no `localStorage`, no second
  copy. Screen 1 counts that file too, which is why there must not be a second
  copy: two stores would give the list and the sheet different answers.
- 「採点する」 grades in-page and `POST /api/tests/<id>/submit` writes
  `採点結果.json` plus the same `ユーザー解答.json` shape `grade_answers.py`
  reads: `{"言語知識_読解": {"33": 2, …}, "聴解": {"問1-1": 2, …}}`. Over
  `file://` (no server) radio clicks cannot persist; grading falls back to
  browser downloads for the two JSON files.

## Parser contract (why the Markdown conventions are load-bearing)

The builder locates questions in the Markdown, so `question-authoring`'s
formatting rules are not cosmetic:

- 言語知識: `**33** stem` then indented ` 1. … 2. …` option lines, OR 問題6's
  `**28 募集**`, OR 問題9's all-on-one-line `**50** 1. こと  2. だけ …`.
- 聴解: `**1番**` + indented options, OR a bare bubble row
  `**1番** 1 ・ 2 ・ 3 ・ 4` for the 問題3/4/5 items that print nothing.
- `**例**` rows get a STATIC row with the answer already filled in, never radios
  — the 例 is a demonstration, not a scored item. The number comes from the
  `解答用紙` grid's `**(n)**` cell (`example_premarks()`), read from the source
  BEFORE `strip_key` truncates that grid away. `jlpt-exam-structure` requires it:
  the announcer says 「解答用紙の問題◯の例のところを見てください。最もよいものは
  ◯番ですから、答えはこのように書きます」, so a blank 例 row points at nothing.
  `make check` already asserts the grid mark equals the announced number.
- Listening keys come from `grade_answers.parse_choukai_keys()` itself, so the
  emitted JSON can never drift from what grading expects.

**The builder warns loudly** when a question gets no radio group
(`no radio group for …`) or when a group has no answer key. Treat either
warning as a bug in the Markdown formatting, not as noise — a silently
missing group means that question can never be answered or scored.

## Verification

```bash
make check            # asserts everything below, for every test on disk
```

`make check` (`tools/check_consistency.py`) is the real gate. On the answer
sheet it asserts: **101 radio groups**, one per scored question; every expected
key present; no group name shared by two questions; 4 options for each of the
71 gengo questions; 3 for 問題4's 即時応答 items (393 inputs total); no emoji in
the report labels; and that the in-page grader and `grade_answers.py` produce an
**identical `採点結果.json` document** (every field but the timestamp) on the
same simulated answers.

Two option-counting bugs it was written to prevent, both of which shipped in
every earlier version of the sheet and made the exam partly unanswerable:

- **one bubble per horizontal question.** 問題1-8 print all four choices on a
  single line; the option regex reports only the FIRST number on a line, so the
  group got `width=1` and you could only ever answer 1. Many horizontal-layout
  questions in test 1 were affected. `option_run()` now counts a consecutive `1..k` run on
  the line (a consecutive run only, so `1. 価格が3.5倍…` is not miscounted).
- **問題5's 質問1/質問2 colliding with 1番.** Routing them to `問5-2-N`
  requires 2番 to be identifiable; if 質問1/質問2 fall through to `問5-1`,
  two items become unanswerable and two answers clobber each other.
  質問N now always belongs to 2番 whenever the section is 問題5.

Manual spot-check if you change the parser:

```bash
python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/1
# expect exactly: 101 items (71 Gengo/Dokkai, 30 Choukai), zero warnings
```

To check the in-page grader against the Python one, extract the last `<script>`
block, stub the DOM, call `computeResult()` with simulated answers under `node`,
and compare its object with `grade_answers.result_payload()` on the same input.
Do this after ANY change to the scoring JS — `make check` already does exactly
this, so in practice: run `make check`.
