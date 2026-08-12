---
name: jlpt-exam-structure
description: Single owner of official JLPT exam format facts — section layout, question counts, timing, booklet printing conventions, and announcer/例 (practice example) mechanics. Consult whenever writing, checking, or discussing the structure of a JLPT exam or any of its sections (問題1〜問題14 for N2), including questions like "how many questions in N2 choukai" or "what is printed in the booklet". Other skills MUST defer to this file for format facts.
---

# JLPT Exam Structure (N2 reference)

## Deliverable File Mapping (`tests/<test_id>/`)

All section layouts, question counts, and item specifications in this document are benchmarked against and aligned with the official JLPT past exams in `refs/JLPT_N2_NEW/` (e.g. 07/2023, 12/2023, 12/2024, 07/2025, 12/2025).

The 2009 概要版 guidebook lists 小問数 as a pre-launch 目安 (「実際の試験での出題数は多少異なることがあります」); **actual recent papers** (every exam in `refs/JLPT_N2_NEW/`) use the counts below. Prefer the past-exam counts over the guidebook table — always.

That is not a formality: guidebook numbers have twice been copied into this repo
as if measured. The rows where it disagrees with reality, so nobody "fixes" them
back: 語形成 5 (real: **3**), 文章の文法 5 (**4**), 内容理解（中文） 9 (**8**,
i.e. 4 passages × 2), 即時応答 12 (**11**), 聴解 統合理解 4 (**3** answers from
2 items), totals 75+32 (**71+30**). The 聴解 counts are checkable without
reading a script: the official audio puts an answer pause after scored items
only, so its histogram is 12 × 12 s (問題1+2), 17 × 8 s (問題3+4+問題5 1番),
7 × 20 s (問題2 option-reading) — see `choukai-audio`.

**The counts below are the CURRENT era's, and the exam has three.** Measured
over all 31 sittings 7/2010–12/2025
(`question-authoring/references/official_calibration.md` §1):

| Era | sittings | 言語知識・読解 | 聴解 |
|---|---|---|---|
| 7/2010 – 7/2018 | 17 | **75** (5/5/5/7/5/5/12/5/5/5/9/2/3/2) | **32** (5/6/5/12/4) |
| 12/2018 – 7/2021 | 6 | 72–73 (問3→3, 問9→4, 問11 9↔8) | 30 |
| **12/2021 – 12/2025** | **9** | **71** (5/5/3/7/5/5/12/5/4/5/8/2/3/2) | **30** (5/6/5/11/3) |

So the repo's **71 + 30 = 101 contract dates from 12/2021**, and 問題11's 4×2
shape from **12/2022** (§"問題11 shape" below) — a pre-2022 paper looks different
because it *is* different, not because it was misread. The 2009 guidebook's 目安
is exactly the 2010–2018 column, which is why it keeps looking authoritative;
the current 大問のねらい PDF has dropped the 小問数 column entirely. **Never
average a 読解 length or a stem-shape frequency across eras** — for anything
measured, the window is the 7 sittings 12/2022–12/2025.

The deliverable file names and their sources live in **AGENTS.md §2**
(Deliverables Naming Convention) — the single copy; this file no longer
restates the table.

## 言語知識(文字・語彙・文法)・読解 — 105 min, 71 questions


| 問題 | Type | Count | Q# |
|---|---|---|---|
| 1 | 漢字読み (kanji reading) | 5 | 1-5 |
| 2 | 表記 (orthography: kana→kanji) | 5 | 6-10 |
| 3 | 語形成 (prefix/suffix: 未/化/性/済み/制…) | 3 | 11-13 |
| 4 | 文脈規定 (word in context) | 7 | 14-20 |
| 5 | 言い換え類義 (paraphrase) | 5 | 21-25 |
| 6 | 用法 (correct usage among 4 sentences) | 5 | 26-30 |
| 7 | 文の文法1・文法形式の判断 (grammar fill-in) | 12 | 31-42 |
| 8 | 文の文法2・文の組み立て (scramble, ★ position) | 5 | 43-47 |
| 9 | 文章の文法 (cloze passage, 4 blanks) | 4 | 48-51 |
| 10 | 短文 (5 short passages × 1Q; include one business email and one notice/掲示) | 5 | 52-56 |
| 11 | 中文 (4 passages × 2Q each) | 8 | 57-64 |
| 12 | 統合理解 (A/B compared texts, 2Q) | 2 | 65-66 |
| 13 | 主張理解 (1 long essay, 3Q) | 3 | 67-69 |
| 14 | 情報検索 (flyer/table + 2 condition-matching Q) | 2 | 70-71 |

Question numbering is continuous 1-71 across the whole paper.

**Character counts are deliberately NOT in this table.** Passage and carrier
length bands live in exactly one place — `question-authoring`'s 読解 length-band
table (問題10–14) and its Benchmark section (問題7/8/9) — and
`tools/check_consistency.py`'s `check_dokkai_lengths()` is what enforces them.
They used to be restated here, in `question-authoring`, and in the gate at once,
hand-synced; only one of the three numbers was gated, and all four generated
papers shipped 問題11 and 問題14 under band while `make check` stayed green.
A second copy of a number is a second thing to drift, so this file states the
*shape* facts (how many passages, how many questions, what is printed) and
nothing measured in characters.

**読解 apparatus (official baseline — measured on July 2025,
`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`; the in-tree `imported-n2-2025-07`
this used to cite was deleted):** a real paper glosses freely across 問題10–13 and uses `（中略）`
inside 中文/長文. The gloss count, its metric (in-body markers), the vocabulary
band a gloss may target, and the 問題13 length floor are all owned by
`question-authoring`. Avoid shipping low gloss counts or omitting `（中略）` entirely.

**問題11 shape:** every paper in the current era is **4 passages × 2 questions**
(Q57–64) — but that shape is **younger than the item counts**: 問題11 ran **3
passages** (3/2/3 or 3/3/2 items) through 7/2022 and became 4×2 at **12/2022**,
with its length jumping from 1778–2179 to 2449–2685 JP chars
(`question-authoring/references/official_calibration.md` §1–2). The
instruction line sometimes still says `(1)から(3)`; **count passage markers, never
trust the instruction** — instruction lines are unreliable across the archive.
Generated mocks must author **4×2**
and print `(1)から(4)` in the instruction. The sampler matches this: it draws
`reading_topics: 12  # 5 short + 4 medium + 1 A/B + 1 long + 1 info`. A spec
carrying only 11 reading topics was drawn before that fix and is one 中文 topic
short.

**問題11 stem shape (format fact, measured):** in July 2025
(`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`), **all 8** 問題11 stems name 筆者 (57「筆者はどのように述べているか」 … 64「筆者が医者と
して大切にしていること」); **none** is a bare retrieval stem. Generated tests
1/2/3/4 shipped **4/6/5/6** stems out of 8 that do not name 筆者. So the format
requires: every stem names 筆者 (or is 「①…とあるが、どういうことか」 on a marked
span), at least one of each passage's two stems is a 考え/主張 question, and the
four pure-retrieval shapes 「本文で述べられている〜はどれか」「〜として正しいもの
はどれか」「〜の主な目的は何か」「〜の内容と合っているものはどれか」 do not appear
in 問題11 at all. Authoring procedure and the gate check: `question-authoring`
問題11 stems / `tools/check_consistency.py`.

**Correction — measured across the archive (12/2022–12/2025, n = 7 sittings /
56 stems; `.agents/question-authoring/references/official_calibration.md`
§4).** The paragraph above was derived from July 2025 alone and two of its
claims do not survive:

- **筆者 is not obligatory.** 82% of current-era 問題11 stems name 筆者; **18% do
  not**, anchoring on a marked span instead (0–3 per paper). What no official
  stem does is anchor on *neither* — avoid stems that anchor on neither.
- **"At least one 考え/主張 per passage" is a paper-level rule, not a pair-level
  one.** Official pairs split 13 one-of-each / 13 two-事実 / 2 two-考え, so a
  per-pair requirement rejects **6 of the 7** current papers. The format fact is:
  the paper carries **at least one** 考え/主張 stem in 問題11 (spread 1–4 of the
  8), the 事実把握 stem comes first in 26 of 28 pairs, and 問題13's item 69 is a
  考え/主張 stem in 7 of 7.

The four banned retrieval shapes are **corroborated at n = 15 sittings** — zero
occurrences, and not in 問題10/12/13/14 either.

### 時間配分の目安 (105分)

Per-part time budget (sums to the 105-min limit including a 2-min final
review):

| Part | 問題 | 目安 |
|---|---|---|
| 文字・語彙 | 問題1-6 | 15分 |
| 文法 | 問題7-9 | 15分 |
| 読解・短文 | 問題10 | 15分 |
| 読解・中文 | 問題11 | 25分 |
| 読解・統合理解 | 問題12 | 9分 |
| 読解・主張理解 | 問題13 | 15分 |
| 読解・情報検索 | 問題14 | 9分 |
| 見直し | whole paper | 2分 |

## 聴解 — ~50 min, 30 answers

| 問題 | Type | Count | Printed in booklet | Spoken 例? |
|---|---|---|---|---|
| 1 | 課題理解 (what to do first/next) | 5 | 4 options per item + 例 options | yes + confirmation |
| 2 | ポイント理解 (why/what point) | 6 | 4 options per item + 例 options; has option-READING time | yes + confirmation |
| 3 | 概要理解 (gist of monologue) | 5 | NOTHING (memo space only) | yes + confirmation |
| 4 | 即時応答 (quick response, 3 choices) | 11 | NOTHING | yes + confirmation |
| 5 | 統合理解 (long integrated) | 3 answers | **NOTHING — both items** (memo space + bubble rows only) | NO practice (この問題には練習はありません) |

問題5 shape: **2 item blocks, 3 answers** — `1番` + `2番` (二つの質問), **all choices spoken**. Keys are `問5-1`, `問5-2-1`, `問5-2-2`.

### 問題5 prints nothing — a deliberate divergence from official

**This repo prints NO options anywhere in 問題5**, for 1番 and 2番 alike. The
booklet carries the instruction, a メモ area, and a bare bubble row per answer
(`**質問1** 1 ・ 2 ・ 3 ・ 4`); every choice is read aloud. **This is a house
rule, not a format fact** — flagged here in full because everything else in this
file is measured, and a reader must not mistake this for the archive.

**What official actually does, for calibration:** all 31 sittings print 2番's
four options. They are **names only**, and 質問1 and 質問2 print the **same four
in the same order**. July 2025 (`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`, the
exact text layer of the PDF) carries exactly this, twice — once under `**質問1**`,
once under `**質問2**`:

```
 1. 夕日通り
 2. にしがおか
 3. さくら公園
 4. 東山
```

Dec 2025 prints `1 1番の自転車 / 2 2番の自転車 / …` — the same list emptied of
information. **The house rule is the next step along that line**: with nothing
printed, all four candidates must be held from the audio, and no printed word
can leak a deciding attribute. The cost is that a candidate loses the option
list they could re-read while the audio ran, so our 問題5 is harder than the real
one. Do not "restore" the printed list on the grounds that official has it — it
was removed knowingly. Do raise it if the difficulty proves wrong in QA.

Mechanically, 問題5 is now shaped exactly like 問題3: nothing printed, choices
spoken, 3 s between them. Three rules follow, the first two inherited from the
official page and re-pointed at the spoken list:

- **No decisive attribute attached to a name** — no 家賃, 立地, 条件, 時間帯,
  定員 riding along with the candidate in the read-back list
  (`1、夕日通り、海沿いで駅から5分。`). 統合理解 measures holding four candidates'
  attributes from the audio and matching them against two questions; restating
  the deciding attribute in the choice IS the answer, and the item stops
  measuring anything. Speak the bare name — the sea-front detail that decides
  質問1 belongs in the dialogue only. (Under the old printed list this same rule
  read "no parenthesised attribute beside a name"; a generated paper broke it.)
- **質問1 and 質問2 read the same four choices, in one order.** Two different
  lists, or the same four re-ordered, turn one memory task into two and
  desynchronise the two questions from each other and from the key.
- **The choice-list order IS the order the audio introduces the candidates, and the
  deciding line names a candidate — never an ordinal.** Both halves are
  format facts, measured across the archive:
  - **Order.** July 2025 speaks 1つ目 夕日通り / 2つ目 西が丘 / 3つ目 さくら公園 /
    最後 東山 and prints `1 夕日通り / 2 にしがおか / 3 さくら公園 / 4 東山`.
    Dec 2014 (four 方法, 1〜4つ目) and July 2019 (four 校舎, まず/2つ目/それから/
    4つ目) do the same, and Dec 2025 enumerates by the printed number itself
    (「1番の自転車は…」) — the same rule with the labels made explicit.
  - **Decider.** The resolving line always names an ATTRIBUTE:
    「鳥が見られる所？」「お寺の近くっていう所」 (7/2025),
    「折りたためる自転車なら」「1番安定性が高いのにする」 (12/2025). In 31
    sittings no 問題5 candidate item speaks a `Nつ目` back-reference after its
    enumeration.

  **Consequence, and it is the whole reason this is written down:** a mis-keyed
  問題5 2番 is fixed by re-enumerating the candidates so the dialogue introduces
  them in the read-back order, then `make mp3 <test_id>` — **never by re-ordering
  the choice list alone.** A list re-ordered under an audio that still says
  「3つ目の方法がぴったりですね」 silently re-keys the item: the ordinal points at a
  numbered SLOT, so the paper then has two defensible answers, the ordinal's and
  the key's. That is exactly what one repair pass did to `tests/3` (spoken
  個別面談/模擬面接/AI/座談会, listed AI/模擬面接/個別面談/座談会, deciding line
  「3つ目」, key on slot 1). Both halves now live in `聴解スクリプト.txt`, which
  removes the two-file desync but **not** the defect — an ordinal decider still
  re-keys the item when the enumeration is re-ordered, and now one file edit is
  enough to do it. `tools/check_consistency.py` fails both halves —
  `check_mondai5_enumeration()` — wherever the script uses ordinal labels at
  all; a paper that enumerates by name resolves nothing there and is left to
  `exam-qa-review` step 4. `check_mondai5_prints_nothing()` fails a booklet that
  prints an option list under 問題5.

## Announcer / 例 mechanics (script + booklet must both honor these)

- Exam opens (spoken / `聴解スクリプト.txt`): 「Nに聴解。これから、Nにの聴解試験を始めます。問題用紙にメモをとってもかまいません。」
  — spell the level as **`Nに`**, never `N2`, so TTS does not read the digit
  as English "two" (`choukai-audio` owns the TTS spelling rule). Printed
  booklet titles may still say `N2`.
- Each of 問題1-4: instruction → 「では、練習しましょう。」 → 例 item →
  「最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。
  最もよいものは◯番ですから、答えはこのように書きます。では、始めます。」
- 問題1/2 questions are spoken TWICE: before and after the conversation.
- 問題3/4/5: choices are SPOKEN (「1、…。2、…。」), not printed — **all of 問題5,
  2番's two questions included** (§"問題5 prints nothing" above; official prints
  2番's).
  **Spoken ≠ same pacing**: measured on the official Dec 2025 audio, 問題3 and
  問題5 leave ~3.0 s between choices, while 問題4's three choices are read
  continuously (1.0–2.0 s apart, i.e. ordinary dialogue spacing). That is why
  `GAP_BETWEEN_SPOKEN_CHOICES` in `choukai-audio` applies to 問題3/問題5
  only — not an oversight; do not "fix" it.
- 問題5 2番 options are SPOKEN, twice — the four choices are read after 質問1 and
  again after 質問2, with the 10 s answer pause between the two runs (official
  prints them and reads none; see the divergence note above).
- Exam closes: 「これで、聴解試験を終わります。」

## 問題N instruction lines (canonical — transcribed from `refs/JLPT_N2_NEW/`)

These are the texts `choukai-audio` tells you to paste into BOTH
`聴解.md` and `聴解スクリプト.txt`. Copy from here, never from a previous test:
`make check` only proves the booklet and the script agree with **each other**, so
a paper where both drift the same way passes green, and the tests on disk do
drift. Transcribed from the July 2025 booklet (`refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf`).

| Where | Text |
|---|---|
| 問題1 | 問題1では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。 |
| 問題2 | 問題2では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。 |
| 問題3 | 問題3では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問とせんたくしを聞いて、1から4の中から、最もよいものを一つ選んでください。 |
| 問題4 | 問題4では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、それに対する返事を聞いて、1から3の中から、最もよいものを一つ選んでください。 |
| 問題5 | 問題5では、長めの話を聞きます。この問題には練習はありません。問題用紙にメモをとってもかまいません。 |
| 問題5 1番 | 問題用紙に何も印刷されていません。まず話を聞いてください。それから、質問とせんたくしを聞いて、1から4の中から、最もよいものを一つ選んでください。 |
| 問題5 2番 | 問題用紙に何も印刷されていません。まず話を聞いてください。それから、二つの質問とせんたくしを聞いて、それぞれ1から4の中から、最もよいものを一つ選んでください。 |

- 問題1〜4: the SCRIPT appends 「では、練習しましょう。」 to the instruction, then
  the 例, then the confirmation line ending 「では、始めます。」. The BOOKLET
  prints the instruction only.
- 問題5: **both** lead-ins are spoken and appear in both files, each as its own
  block BEFORE its `N番。` marker — the 1番 one adds 「では、始めます。」, the 2番
  one does not (the section is already running). The 2番 line is a house
  adaptation of the official one, since nothing is printed: 「問題用紙に何も印刷
  されていません」 replaces 「問題用紙の」 and 「せんたくし」 joins the two 質問.
  Official's 2番 line is booklet-only, because official prints 2番's options.
  There is still no combined 「1番、2番。…」 line.
- The official scan renders some words in kana (いんさつ, えらんで); this repo
  writes 印刷 / 選んで, and `make check`'s typo guard expects 印刷. Either is
  acceptable as long as the booklet and the script match — do not "fix" one file
  alone.

## 認定の目安 (official level descriptor — what N2 is allowed to test)

The published 認定の目安 for N2 (「読む」「聞く」 language behaviours) bounds
passage genre and listening pace, so it belongs here rather than in an
authoring skill's head:

> 日常的な場面で使われる日本語の理解に加え、より幅広い場面で使われる日本語をある程度理解することができる
>
> **読む** ・幅広い話題について書かれた新聞や雑誌の記事・解説、平易な評論など、**論旨が明快な**文章を読んで文章の内容を理解することができる。・**一般的な話題**に関する読み物を読んで、話の流れや表現意図を理解することができる。
>
> **聞く** ・日常的な場面に加えて幅広い場面で、**自然に近いスピード**の、まとまりのある会話やニュースを聞いて、話の流れや内容、登場人物の関係を理解したり、要旨を把握したりすることができる。

Two consequences the pipeline actually uses:

- 読解 passages are 新聞・雑誌の記事/解説/平易な評論 with a **clear line of
  argument** — N1's descriptor is the one that says 論理的にやや複雑 /
  抽象度の高い文章. A 問題13 that reads as dense abstraction is off-level even at
  the right character count.
- 聴解 dialogue is **自然に近い** speed, not N1's 自然な speed — see
  `choukai-audio`'s audio-analysis step before touching any `SPEAKER_MAP` rate.
- Answer grids include an 例 column with the sample answer pre-marked — and the
  pre-marked number MUST equal the number the announcer declares
  (「最もよいものは◯番です」): the grid and the announcement are one
  demonstration, seen and heard together. `make check` compares them; three of
  the four shipped tests had at least one grid pre-marking a different number.

## Booklet layout conventions

- **Heading structure (both booklets)**: a `#` banner section (`# 【文字・語彙】`,
  `# 【文法】`, `# 【読解】`, `# 【問題】`) wrapping `## 問題N` section headers.
  Never make `問題N` an `h1`. Parsers are level-agnostic where it counts
  (`build_interactive.py` matches `^#+\s*問題([1-5])`) but the answer-key parser
  is NOT — `parse_choukai_keys()` only recognizes `## 問題N` — so `##` is the
  safe, uniform choice everywhere.
- **Markdown Question Numbering**: Always use bold numbers (`**1**` ... `**71**` for file 1; `**例**`, `**1番**` for file 2). Never use `1.` or `6.` list syntax to prevent HTML `<ol>` list resets.
- 文字・語彙・文法: short options run HORIZONTALLY on one line
  (` 1. ◯◯  2. ◯◯  3. ◯◯  4. ◯◯`). Reading questions and 問題6 usage sentences are vertical.
- 聴解 booklet: options stacked VERTICALLY, one per line with a leading space —
  in **問題1 and 問題2 only**, the two sections that print any. 問題3/4/5 print a
  bare bubble row per item (`**1番** 1 ・ 2 ・ 3 ・ 4`, `**質問1** 1 ・ 2 ・ 3 ・ 4`)
  and nothing else.
- Question stems bold the tested word: **地域**, or show blanks as (　) / ＿＿.
  The bold span is the booklet's underline, so it covers the **whole word,
  okurigana included** (July 2025 問1 marks `**収まった**`, `**辛い**`) — never a
  bare kanji with its tail outside the mark. Authoring rule and the shipped
  counter-example: `question-authoring` 問題1.
- 問題8 uses ＿＿ ＿＿ ★ ＿＿ with the answer = whichever option lands on ★.
- **Dokkai Vocabulary Notes (No Furigana)**: Reading passages (問題9-14) containing uncommon vocabulary, domain-specific terminology, or rare kanji contain **NO FURIGANA** (`<ruby>`). Test-takers are expected to read N2 kanji without furigana. Over-the-level or rare terms must ONLY be annotated inline using `（注1）`, `（注2）`... with structured note blocks `（注1） 語彙：説明` sitting below the passage before questions.
- **Passage Numbered Markers (1-to-1)**: Every numbered marker (`①**...**`, `②**...**`) in a reading passage MUST match 1-to-1 with a question stem. Do not place unused/orphaned markers in passages.

## Answer Key & Explanation Table Structure

This section is the **single copy** of the answer-key table format —
`question-authoring` points here rather than restating it.

Both booklets must conclude with structured table-formatted answer keys and
explanations, opened by a **heading whose text starts with `解答` or `正解`**
(`^#+\s*(解答|【?正解)`) — the marker `build_interactive.py` truncates from, and
it aborts if absent. Any wording qualifies; keep 解答/正解 out of the start of
any heading in the question body, or the body gets truncated too:
- `言語知識・読解.md`:
  - the key heading (e.g. `# 解答(言語知識・読解)` or `# 解答と解説`), containing:
  - `## 文字・語彙`: Multi-column key table (`| 問 | 答 | ...`)
  - `## 文法`: 3-column table (`| 問 | 答 | 解説 |`) for Q31–51
  - `## 読解`: 3-column table (`| 問 | 答 | 解説 |`) for Q52–71
- `聴解.md`:
  - `# 解答用紙(マークシート)`: Bubble sheets for 問題1〜問題5
  - `# 【正解・解説】※解き終わってから見てください`: Section-by-section tables (`| 番号 | 正解 | 解説 |`) for 問題1〜問題5 + `## 得点の目安`
  - key sub-headers must be `## 問題N` — `parse_choukai_keys()` keys section state off `##`, so `# 問題N` in the key section parses as nothing
  - 問題5's table carries **3 rows for 2 items**, the 2番 rows labelled with 質問1/質問2 (see question-authoring for the accepted label styles)
