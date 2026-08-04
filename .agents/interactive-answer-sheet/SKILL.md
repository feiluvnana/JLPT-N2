---
name: interactive-answer-sheet
description: Single owner of the MERGED problem+answer sheet — the complete exam booklet (言語知識・読解 and 聴解) rendered into a single HTML file (解答.html) with radio bubbles beside every choice and an embedded audio player for 聴解. Use whenever the user wants to take/answer/solve a test on screen, mentions the answer sheet, マークシート, 解答用紙, selecting answers, or playing the listening audio while answering. Grades the full 180-point exam in-page on button press and saves 採点結果.md and user_answers.json directly.
---

# Interactive Answer Sheet (問題用紙＝解答用紙)

## Why this skill exists

The exam merges the problem booklet and interactive radio bubbles into a single unified deliverable (`解答.html`). You answer **inside the booklet**, press 「採点する」, and the complete 180-point JLPT grading report (`採点結果.md`) appears immediately.

## Execution

```bash
python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/<test_id>
# or: make sheet <test_id>

# To serve in browser with automatic direct file saving into tests/<test_id>/:
python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py tests/<test_id>
# or: make serve <test_id>
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
3. **renders the full 180-point report on screen** and scrolls to it, and
4. **saves directly to `tests/<test_id>/`** (`採点結果.md` and `user_answers.json`) if served via `make serve` or local HTTP server, or downloads them if opened standalone.

If anything is unanswered the button asks for confirmation first, and
unanswered items appear as 「— 未解答」 in the check table rather than as wrong.

### One source of truth for the grading data

`ANSWER_KEY`, `TAXONOMY`, `ADVICE` and the section definitions are **serialized
out of `grade_answers.py` at build time** (`GENGO_QUESTION_TAXONOMY`,
`CHOUKAI_QUESTION_TAXONOMY`, `ADVICE_FOR`). Never hand-write those tables into
the JS — a second copy is exactly how the grader's 大問 ranges drifted from
`jlpt-exam-structure` in the first place. `make check` proves the two agree by
running the sheet's own JS under node and comparing raw scores with
`grade_answers.py` on identical simulated answers (36/51 + 14/20 + 21/30 for
test 1 at the time of writing).

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

## Serving (`serve_sheet.py`) — three things it must keep doing

1. **Range requests.** `聴解.mp3` is ~30 MB and the `<audio>` element re-requests
   it with `Range:` on every seek. `SimpleHTTPRequestHandler` ignores Range and
   restreams the whole file, so the browser cancelled each previous transfer:
   seeking was slow and the console filled with aborted downloads. The handler
   answers `Range:` itself with `206 Partial Content` (`416` for an
   unsatisfiable range) and advertises `Accept-Ranges: bytes` on GETs.
2. **Client disconnects are not errors.** Every abort — a seek, closing the tab,
   a paused buffer — kills the socket mid-`copyfile` and used to print a
   `BrokenPipeError` traceback per abort. `handle()` and `finish()` swallow
   `BrokenPipeError`/`ConnectionResetError`. Do not "fix" a broken pipe by
   re-raising it; the request is simply over.
3. **Threaded.** `ThreadingHTTPServer`, because a single-threaded server queues
   the 採点する `POST /api/submit` behind whatever MP3 stream is in flight — the
   submit appeared to hang while the audio buffered.

## On-screen layout

The sheet imports `SCREEN_CSS` from `build_booklet.py`, so it uses the same
centered 60 em measure as the booklets instead of stretching to the window
width (unreadable line lengths on a wide monitor). `SCREEN_CSS` exposes
`--gutter`; the sticky `#bar` and `#player` pull out to it with negative
margins so they still read as full-width chrome over the text column. It is all
inside `@media screen` — the A4 `@page` geometry is untouched, so Cmd-P still
prints the booklet.

## Answer capture

- **Every radio click** writes progress to one place: `tests/<test_id>/user_answers.json`
  via `POST /api/save-answers` when served with `make serve` (debounced ~250 ms so
  rapid clicks do not thrash the disk). On reload the sheet loads that same file
  with `fetch('user_answers.json')` — no `localStorage`, no second copy.
- 「採点する」 grades in-page and writes `採点結果.md` plus the same
  `user_answers.json` shape `grade_answers.py` reads:
  `{"言語知識_読解": {"33": 2, …}, "聴解": {"問1-1": 2, …}}`. Over `file://`
  (no server) radio clicks cannot persist; grading falls back to browser
  downloads for the two files.

## Parser contract (why the Markdown conventions are load-bearing)

The builder locates questions in the Markdown, so `question-authoring`'s
formatting rules are not cosmetic:

- 言語知識: `**33** stem` then indented ` 1. … 2. …` option lines, OR 問題6's
  `**28 募集**`, OR 問題9's all-on-one-line `**50** 1. こと  2. だけ …`.
- 聴解: `**1番**` + indented options, OR a bare bubble row
  `**1番** 1 ・ 2 ・ 3 ・ 4` for the 問題3/4/5 items that print nothing.
  `**例**` rows are rendered as plain text — the 例 is not scored.
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
the report labels; and that the in-page grader and `grade_answers.py` return
identical raw scores on the same simulated answers.

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
block, drop the DOM-bound functions, call `buildReport()` with simulated
answers under `node`, and compare raw counts with `grade_answers.py` on the
same input. Do this after ANY change to the scoring JS.
