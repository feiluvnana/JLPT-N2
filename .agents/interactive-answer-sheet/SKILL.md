---
name: interactive-answer-sheet
description: Single owner of the MERGED problem+answer sheet — the exam booklet rendered to HTML with a radio bubble beside every choice, plus an in-page audio player for 聴解 so the listening exam can be taken entirely in the browser. Use whenever the user wants to take/answer/solve a test on screen, mentions the answer sheet, マークシート, 解答用紙, selecting answers, or playing the listening audio while answering. Grades each half in-page on button press and emits 採点結果_*.md directly — no JSON handling. Runs AFTER the exam Markdown exists; exam-answer-grading is only needed for the combined 180-point judgement.
---

# Interactive Answer Sheet (問題用紙＝解答用紙)

## Why this skill exists

The exam used to ship as a booklet plus a separate `マークシート.pdf`, so
answering meant looking at two documents and
transcribing between them. This skill merges them: you answer **inside the
booklet**, press 採点する, and the report appears immediately. The old mark-sheet
layer (`マークシート.pdf` / `.html`, `--create-template`, `--user-pdf`) has
been removed — do not reintroduce it.

## Execution

```bash
python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/<test_id>
# or: make sheet <test_id>
```

Outputs into `tests/<test_id>/`:

| File | Contents |
|---|---|
| `言語知識・読解_解答.html` | 75 questions, radio bubble per choice, in-page grading |
| `聴解_解答.html` | 32 items + **audio player** for `聴解.mp3`, in-page grading |

Re-run after ANY edit to `言語知識・読解.md` / `聴解.md` — the Markdown stays
the single source of truth, exactly as for the booklet HTML.

## Grading happens in the page — press 「📊 採点する」

There is no JSON step. Pressing the button:

1. grades this half immediately against the embedded key,
2. **renders the report on screen** and scrolls to it, and
3. downloads `採点結果_言語知識・読解.md` / `採点結果_聴解.md`.

Each sheet grades **only its own half** (言語知識+読解, or 聴解), because that
is all it can see. The report says so explicitly: a 180-point 合否 needs both.
For the combined judgement, press 「解答JSONも保存」 in the result box and run
`exam-answer-grading` over both files.

If anything is unanswered the button asks for confirmation first, and
unanswered items appear as 「— 未解答」 in the check table rather than as wrong.

### One source of truth for the grading data

`ANSWER_KEY`, `TAXONOMY`, `ADVICE` and the section definitions are **serialized
out of `grade_answers.py` at build time** (`GENGO_QUESTION_TAXONOMY`,
`CHOUKAI_QUESTION_TAXONOMY`, `ADVICE_FOR`). Never hand-write those tables into
the JS — a second copy is exactly how the grader's 大問 ranges drifted from
`jlpt-exam-structure` in the first place. Verified equal: both graders return
46/54 + 18/21 + 27/32 on the same simulated answers.

## The answer key must never be VISIBLE

The key is embedded as JS data so grading can happen offline with no server —
but it must never be *rendered*. The builder truncates everything from the key
heading (`# 解答…` / `# 【正解…`) onward out of the document body, and **exits
with an error if it cannot find that heading**. Never "fix" that by loosening
the check. The trade-off is deliberate: the key is reachable via devtools by
someone who goes looking, which is acceptable for a self-study mock (the key
is in `聴解.md` next door anyway); what matters is that it is not on screen
while you solve.

`言語知識・読解_解答.html` is a deliverable and is NOT the same file as
`言語知識・読解.html`, which is a throwaway intermediate that `build_booklet.py`
overwrites on every booklet build.

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

## Answer capture

- Progress autosaves to `localStorage`, keyed `jlpt:<test_id>:<section>`, so a
  refresh or accidental close does not lose work.
- 「解答JSONも保存」 (in the result box) downloads `user_answers_gengo.json` /
  `user_answers_choukai.json` in exactly the shape `grade_answers.py` reads:
  `{"言語知識_読解": {"33": 2, …}, "聴解": {"問1-1": 2, …}}`. Only needed for the
  combined 180-point judgement — the per-section report needs no files.

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
python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/1
# expect exactly: 75 questions, 32 items, zero warnings
grep -c 'type="radio"' tests/1/言語知識・読解_解答.html   # 300 (75 x 4)
```

To check the in-page grader against the Python one, extract the last `<script>`
block, drop the DOM-bound functions, call `buildReport()` with simulated
answers under `node`, and compare raw counts with `grade_answers.py` on the
same input. Do this after ANY change to the scoring JS.
