---
name: exam-model-answer
description: Single owner of generating the model answer and comprehensive explanation deliverable (模範解答.html). Generates a complete, interactive, concise explanation document for every question in an exam (71 Language Knowledge & Reading questions + 30-31 Listening questions), in Japanese AND Vietnamese behind an in-page segmented control — the two sets independently written, never translated from one another. Explains why the correct answer is right (with evidence, grammar rules, dictionary definitions, passage quotes, listening script evidence) and why each distractor option is incorrect. Use whenever generating 模範解答.html for a test, updating question explanations, reviewing model answers, or explaining exam solutions.
---

# Exam Model Answer & Explanation (模範解答・詳細解説)

This skill owns generating `tests/<test_id>/模範解答.html` — the model
answer and in-depth explanation deliverable — and the two explanation sets it
renders: `詳細解説.json` (Japanese) and `詳細解説.vi.json` (Vietnamese).

## Two languages, two rewrites

**The page ships the explanations in TWO languages behind one segmented
control** (2026-08-25): Japanese in `詳細解説.json`, Vietnamese in
`詳細解説.vi.json`. Every label the page prints outside the exam's own wording
lives once per language in `build_model_answer.UI`.

**The two sets are WRITTEN, not translated. This is the rule, not a preference.**
A sentence-for-sentence translation of the Japanese pane is a defect, and the
cheapest one to commit, so name it: 「代理」の代は「ダイ」、理は「リ」です reads
to a Japanese-literate learner as a fact being confirmed, and to a Vietnamese
learner as an unexplained assertion about a system (音読み/訓読み) the sentence
never introduced. Translated, it stays unexplained — the reader gets the
Japanese pane's *framing* in words they can read, which is worth less than the
effort of reading it. Written for that reader, the same item says *代 đọc âm On
là「ダイ」* and the framing comes with it.

So: solve the item, then write the explanation for the reader in front of you.
Do not open the other language's file to "check" — that is how a rewrite becomes
a translation one sentence at a time.

What is NOT rewritten, in either pane: **the exam's own wording.** The stem,
the options, the reading passage and the listening script are stored ONCE, in
`詳細解説.json`, and both panes print them identically above the explanation —
the reader always sees the original question first, in Japanese, whichever
language they are reading the explanation in. `詳細解説.vi.json` therefore
carries **only** `why_correct`, `options_analysis` and `points`; a `stem`,
`options`, `passage` or `script` key in it is a second copy of text that already
has an owner, and the gate FAILs it.

The page falls back cleanly: with no `詳細解説.vi.json` on disk it renders
exactly the single-language page it always did, segmented control and all
suppressed.

## Length: the terseness bands

Explanations had been growing without a bound. Measured across all 20 papers on
2026-08-25: `why_correct` averaged **101** characters — 139, 148 and 173 in the
three most recent papers — each option analysis **50**, each point **34** across
**4.0** points, for **42,500 authored characters per paper**. The cost lands
twice: authoring is the slowest stage in the whole pipeline, and a learner does
not find out why option 2 is wrong any better from 170 characters than from 50.

Furigana `《…》` and the `[正解]`/`[不正解]` tag are stripped before counting, so
ruby markup can never push a line over.

| Field | Japanese | Vietnamese |
| ----- | -------- | ---------- |
| **whole item** (`why_correct` + all options + all points) | ≤ 210 | ≤ 380 |
| `why_correct` | ≤ 90 | ≤ 160 |
| each `options_analysis` entry | ≤ 50 | ≤ 90 |
| each `points` entry | ≤ 45 | ≤ 80 |
| number of `points` | 2–4 | 2–4 |

**The item budget is the row that matters.** The per-field caps are a ceiling,
and a ceiling on its own shortens nothing: the fleet mean was already 50 for an
option analysis and 34 for a point, so those caps trim the tail and leave the
average where it was. The budget is half the measured 421 characters an item was
costing, and it is what a paper is actually held to. The caps exist so one field
cannot eat the whole of it.

A well-spent budget is not tight. One sentence of evidence, one clause of reason
per option, two glosses comes to roughly **140** characters — comfortably inside
210, with room for the item that genuinely needs more.

**Aim at ~170 and leave the top of the band empty.** The cap is a ceiling, not a
target, and an entry written flush against it is one edit away from breaching.
That is not hypothetical: on 2026-08-25 three papers were rewritten with per-item
maxima of exactly 210, and a concurrent 読解 repair pass — re-syncing 解説 quotes
to repaired passage wording, which is ordinary downstream work — pushed **38
items** back over the budget the same afternoon. Every one of them had been
sitting at 203–210. A 解説 quote grows whenever the line it quotes is edited, so
the headroom is not slack; it is what lets the paper survive its own maintenance.

`check_consistency.py`'s `KAISETSU_BANDS` and `KAISETSU_ITEM_BUDGET` **own these
numbers** and the gate asserts this table against them — change one and the other
fails, so edit the constant and refresh the table from it. Vietnamese runs longer
than Japanese for the same content (words where Japanese writes kanji), so both
its caps and its budget are the Japanese ones ×1.8; that factor is a design
allowance, not a measurement, and is due a re-measure once several papers are
authored in it.

### The one defect the gate cannot see: prose that outlived its item

When an item's options are rewritten, `詳細解説.json`'s `options` array gets
re-synced — `check_model_answer_option_sync` FAILs if it does not — but the
`options_analysis` prose beside it does not, and **nothing checks that the prose
describes the options it sits next to.** The result reads perfectly and argues
about a question the paper no longer asks. It has shipped four times:
20260818_1 item 54 and 20260819_1 items 53/54 (found 2026-08-25), and
20260817_1 items 49 and 37, caught mid-rewrite the same day while a concurrent
読解 pass was replacing their options.

Two symptoms of it ARE decidable and are now gated by
`check_kaisetsu_tag_keys`: a `[正解]` tag on the wrong index, and a
「Nが正解」 ordinal in `why_correct` that disagrees with the key. Both mean the
entry predates the item's current options, so **re-solve the item and rewrite
the whole entry — never just move the number.**

The general case is not string-decidable, and that was measured rather than
assumed. Requiring every 「…」 span in the prose to trace to the item's own
passage flags **2700** spans fleet-wide, virtually all of them legitimate:
a vocabulary item's explanation quotes usage examples (「悲しみに暮れる」,
「措置を講じる」) that correctly appear nowhere in the paper. Narrowing to
clauses of 14+ characters absent from the entire paper still flags 1209;
narrowing to clauses belonging to a *different* item flags 36, mostly
coincidental common phrases (「よろしくお願いします」). No threshold separates
the defect from ordinary teaching prose.

So this one is yours to catch by reading: **whenever you touch an item, read its
`options_analysis` against the options actually printed.** It is also
`exam-qa-review`'s to catch — a green gate is the entry condition for that pass,
not a substitute for it (`AGENTS.md` §0.5).

**Cut, do not hollow out.** The band is met by deleting the restatement, the
second example and the throat-clearing — never by replacing a concrete reason
with 「文脈に合いません」. A generic line is a *different* defect and is
separately prohibited below. Two sentences of real evidence beat five of
padding, and that is the whole point of the cap.

## Purpose & Pedagogical Quality

While `解答.html` is for taking the test and grading, `模範解答.html` is for
**deep post-exam study (復習・学習)**. For every question (all 101 items:
71 Gengo/Dokkai + 30-31 Choukai), it provides:

1. **Question Stem & Choices**: full context, options, correct-answer badge.
2. **Reading Passages & Audio Transcripts**: 読解 — full passage text with
   numbered markers (`①`, `②`, `（注1）`); 聴解 — full spoken transcript with
   speaker labels.
3. **Concise Explanation** — every field inside the terseness bands above:
   - **Solve the item before you explain it.** Derive the answer from the
     passage/script FIRST, then compare with the answer key, then write. An
     explanation composed backwards from the key reads just as convincing when
     the key is wrong, so this pass is the last cheap chance to catch a
     mis-key — in a generated paper it is the author's own mis-key, in an
     import a mis-transcribed line. A disagreement is never resolved by
     softening the explanation: fix the key (generated) or follow the source
     and report it (`external-test-import` step 3 owns the import tie-break).
     Never let `why_correct` argue for one option while the key names another
     — `check_choukai_kaisetsu_keys()` fails that contradiction for 聴解, and
     nothing but you checks it for 言語知識・読解.
   - **Why the correct answer is selected**: the deciding quote from the
     passage/audio, or the grammar rule or kanji reading that settles it —
     then the conclusion. That is the whole field: one piece of evidence and
     what it proves, typically two short sentences.
   - **Full option-by-option analysis**: a concrete, SPECIFIC reason for EVERY
     choice — contrary to the text, unmentioned, wrong collocation / particle
     / verb form, wrong moment in the audio. One clause of reason is enough;
     the band leaves room for exactly that and no restatement of the option.
     Exactly ONE option tagged `[正解]`/`[Đúng]` matching the official key,
     all others `[不正解]`/`[Sai]` — never all wrong, never a mismatched key
     (the tag is re-applied by index at render, so the two panes cannot
     disagree about which option is right). Generic placeholders
     ("選択肢1は文脈・文法制約に合致しません", "Không phù hợp với ngữ cảnh") are
     prohibited — in BOTH languages, and shortening is never a licence to
     produce one.
   - **Zero internal metadata leaks** — never `[kanji-n2.json]`, `[同分野]`,
     `[N1]`, `〜れる一段動詞×4`, or similar pipeline artifacts; explanations
     are strictly learner-facing.
   - **Mandatory furigana** (`｜漢字《かんじ》` or `<ruby>`) on all target
     kanji, difficult vocabulary, stems, and explanations — throughout the
     Japanese set.
     In the Vietnamese set it is required in **`points`** and nowhere else.
     That is where a word is being handed to the reader to learn, so a
     Vietnamese speaker needs its reading; elsewhere the Japanese is a quote
     pointing back at a passage they can see above the explanation, and ruby
     on it is noise. Scoped 2026-08-25 after the first four Vietnamese sets
     were measured: the wider rule this replaces ("every Japanese word quoted
     in the Vietnamese pane") was met by NONE of them — 0 ruby spans outside
     `points` across all four — and a rule nothing meets is not a rule. The
     narrow one is checked; see `check_kaisetsu_vi_points_furigana`.
     **pykakasi is a first draft, never the answer** — `詳細解説.json`
     furigana is hand-authored (`apply_furigana()` only converts existing
     `《…》` markup into `<ruby>`, it computes nothing). Check pykakasi
     output reading-by-reading before typing it in; known failure modes: a
     bare `人` reads `にん` (should be `ひと` — genuine `にん` compounds are
     always long enough that kakasi merges them into one token); `方` right
     after hiragana reads `ほう` (should be `かた` — genuine `ほう` compounds
     glue `方` to a preceding kanji, not hiragana); `小さい`/its conjugations
     get a stray chouon (`ちーさい` for `ちいさい`, a dictionary bug). A
     separate hand-authoring failure (found across a 2026-08 sweep, 216
     instances in one file): a compound split across a kanji-hiragana-kanji
     boundary (取り組み, 受け取る) sometimes gets the whole preceding
     reading re-prepended onto the second kanji's ruby (`取《と》り組
     《とりく》み` instead of `取《と》り組《く》み`) — each `《…》` must hold
     only that kanji's own reading. Treat unverified furigana as a defect;
     a word's reading must also stay internally consistent within one file.
   - **Important Vocabulary & Grammar** — **2–4** entries, each inside the
     band: the tested word/pattern (reading, core meaning, and the one nuance
     that decides this item), or the grammar form needed to parse the
     sentence, or the single piece of vocabulary a learner most likely does
     not know. Reading and listening items still carry something worth
     surfacing when the "point" is comprehension rather than one word — a
     question-type cue, an elimination signal. Pick the 2–4 that earn their
     place; an exhaustive gloss of every hard word in the passage is what the
     band exists to stop.
   - **Plain language, in whichever language the pane is** —
     `why_correct`/`options_analysis`/`points` are written FOR N2 learners:
     short sentences, common vocabulary; keep (and furigana) an unavoidable
     technical term rather than inventing a vaguer paraphrase. In the
     Vietnamese pane, Japanese appears only as quoted material — the item's
     words in 「」 and readings in furigana — never as a run of untranslated
     prose; the gate flags a long unquoted kana/kanji run as what a pasted
     translation looks like. None of this applies to
     `stem`/`options`/`passage`/`script` — the exam's actual wording,
     furigana'd only, never reworded and never translated.
   - **Emoji-free** — clean, professional typography throughout.

## Authoring — scaffold directly, never type passages from scratch

```bash
make scaffold-explanations <id>            # -> 詳細解説.json, stems/options/passages pre-populated
make scaffold-explanations <id> LANG=vi    # -> 詳細解説.vi.json, an EMPTY skeleton
```

**Count the items the scaffold gives you before you write into it.** A
generated N2 paper is 101 entries and an import is 101 (or 75 + 聴解 for a
四-question sitting); `check_kaisetsu_item_coverage` now FAILs a short file,
because every OTHER 詳細解説 line in the gate measures the entries that are
present and is therefore blind to a missing one. The scaffold shipped a
100-item file for two papers: `derive_choukai_raw` split a two-question 問題5
only on literal 「質問1。」/「質問2。」 markers, which official sittings and imports
carry and this repo's generated scripts (20260828_2 onward) do not, so 問5-2
came back as ONE entry holding 質問1's four options with `[正解]` on option 1.
`20260903_1` shipped that way — 100 items, plus a spurious empty `問5-2` card in
`模範解答.html`, because `build_model_answer`'s `all_choukai_keys` unions the
derived keys with the markdown ones. Fixed 2026-09-04 in
`verify_fidelity._split_spoken_block`, which now recovers an unmarked 質問
positionally (the narration line directly before each option group).

Then complete `why_correct`, `options_analysis` and `points` per item, inside
the terseness bands. Validate each parses
(`python3 -c "import json,sys; json.load(open(sys.argv[1]))" tests/<id>/詳細解説.json`),
run `make check` (it enforces the bands, the parity between the two sets, and
the option sync against the booklet), then `make model-answer <id>`.

**Order matters, and so does isolation.** Author `詳細解説.json` first — it owns
the item keys and the booklet wording the Vietnamese scaffold is generated
against, so `LANG=vi` refuses to run without it. Then author the Vietnamese set
**in a context that is not holding the Japanese one**. That is the same reason
QA runs with fresh eyes (`AGENTS.md` §5): a context that has just written 101
Japanese explanations will produce Vietnamese ones shaped like them, sentence
for sentence, without ever deciding to translate. Two subagents, one per
language, reading the paper — not each other — is the shape that survives.

The Vietnamese skeleton is deliberately empty and carries no exam wording. Read
the item out of `詳細解説.json` or the booklet, solve it, and write.

**Do not write a per-test "compiler" script** (a one-off Python file
building a literal `details = {...}` dict). Four such files accumulated in
`scripts/` before this rule existed — each 100–400KB, unreferenced by any
Makefile target, not re-runnable without clobbering hand-edits.
`詳細解説.json` is the artifact; a script that produced it once is not.

Instead use the shared fidelity tool:

```bash
python3 .agents/exam-model-answer/scripts/verify_fidelity.py tests/<id>
```

It re-derives `stem`/`options`/`passage`/`script` straight from
`言語知識・読解.md`, `聴解.md`, and `聴解スクリプト.txt` and reports every
place `詳細解説.json`'s wording has drifted (furigana differences ignored;
only wording compared). Run it before editing (to see existing drift) and
again when done (to confirm you introduced none) — report-only; read its
docstring for the expected mismatch shapes (問6/問9 stems keep their
instruction-line context; 聴解 `script` excludes the trailing restated
question). Every other reported mismatch is a real defect — most commonly
a passage left empty on a 2nd+ question sharing it, or wording that no
longer matches the booklet/script it was copied from.

## Deliverable Specification

| Deliverable | File Name | Description / Source |
| ----------- | --------- | -------------------- |
| Model Answer & Detailed Explanation | `模範解答.html` | Generated by `build_model_answer.py` from `言語知識・読解.md`, `聴解.md`, `聴解スクリプト.txt`, and `test_spec.json` |
| Japanese explanations | `詳細解説.json` | Hand-authored. Owns the exam wording (`stem`/`options`/`passage`/`script`) for BOTH panes |
| Vietnamese explanations | `詳細解説.vi.json` | Hand-authored, independently of the Japanese set. Prose only — no exam wording |

## Execution & Mandatory Final Step Rule

> **CRITICAL INVARIANT**: Generating `模範解答.html` **MUST ALWAYS BE THE
> ABSOLUTE FINAL STEP** in both the generation and import pipelines.
>
> - **Generation**: run `make model-answer <id>` ONLY AFTER Stage 4 QA
>   returns `QA: PASS` and all question/option/script edits are frozen —
>   earlier is prohibited because subsequent QA fixes desynchronize the
>   explanations from the exam.
> - **Import**: run `make model-answer imported-<slug>` ONLY AFTER all 101
>   keys are verified against the official answer key and `make check` is
>   completely green.

```bash
python3 .agents/exam-model-answer/scripts/build_model_answer.py tests/<id>
make model-answer <id>          # or: make explanation <id>
```

## Structure & Architecture

- **Script**: `.agents/exam-model-answer/scripts/build_model_answer.py`
- **Output**: `tests/<test_id>/模範解答.html`
- **UI Features**: Noto Serif/Sans CJK JP typography; section tabs
  (すべて/文字・語彙/文法/読解/聴解); a 1–71 + 聴解 1–30 quick-nav grid; a
  search/filter box; an embedded 聴解 audio player with chapter timestamps;
  print-friendly (`@media print`) and mobile-responsive layout.
