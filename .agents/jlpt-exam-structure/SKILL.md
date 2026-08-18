---
name: jlpt-exam-structure
description: Single owner of official JLPT exam format facts — section layout, question counts, timing, booklet printing conventions, and announcer/例 (practice example) mechanics. Consult whenever writing, checking, or discussing the structure of a JLPT exam or any of its sections (問題1〜問題14 for N2), including questions like "how many questions in N2 choukai" or "what is printed in the booklet". Other skills MUST defer to this file for format facts.
---

# JLPT Exam Structure (N2 reference)

## Deliverable File Mapping (`tests/<test_id>/`)

All section layouts, counts, and item specs here are benchmarked against the
official past exams in `refs/JLPT_N2_NEW/`.

The 2009 概要版 guidebook lists 小問数 as a pre-launch 目安 (「実際の試験での
出題数は多少異なることがあります」); actual recent papers use the counts
below — prefer them always. This isn't a formality: guidebook numbers have
twice been copied in as if measured. Where it disagrees with reality:
語形成 5 (real **3**), 文章の文法 5 (**4**), 内容理解（中文） 9 (**8**, 4
passages × 2), 即時応答 12 (**11**), 統合理解 4 (**3** answers from 2 items),
totals 75+32 (**71+30**). The 聴解 counts are checkable without a script —
official audio's answer-pause histogram is 12×12s (問1+2), 17×8s
(問3+4+問5-1番), 7×20s (問2 option-reading) — see `choukai-audio`.

**The counts below are the CURRENT era's — the exam has three.** Measured
over all 31 sittings 7/2010–12/2025 (`official_calibration.md` §1):

| Era | sittings | 言語知識・読解 | 聴解 |
|---|---|---|---|
| 7/2010 – 7/2018 | 17 | **75** (5/5/5/7/5/5/12/5/5/5/9/2/3/2) | **32** (5/6/5/12/4) |
| 12/2018 – 7/2021 | 6 | 72–73 (問3→3, 問9→4, 問11 9↔8) | 30 |
| **12/2021 – 12/2025** | **9** | **71** (5/5/3/7/5/5/12/5/4/5/8/2/3/2) | **30** (5/6/5/11/3) |

The repo's **71+30=101 contract dates from 12/2021**, and 問題11's 4×2 shape
from **12/2022** (below) — a pre-2022 paper looks different because it IS
different. **Never average a 読解 length or stem-shape frequency across
eras** — the measurement window is the 7 sittings 12/2022–12/2025.

Deliverable file names and sources: **AGENTS.md §2** (single copy).

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
| 10 | 短文 (5 short passages × 1Q; incl. one business email, one notice/掲示) | 5 | 52-56 |
| 11 | 中文 (4 passages × 2Q each) | 8 | 57-64 |
| 12 | 統合理解 (A/B compared texts, 2Q) | 2 | 65-66 |
| 13 | 主張理解 (1 long essay, 3Q) | 3 | 67-69 |
| 14 | 情報検索 (flyer/table + 2 condition-matching Q) | 2 | 70-71 |

Question numbering is continuous 1-71 across the whole paper.

**Character counts are deliberately NOT in this table** — length bands live
in exactly one place, `question-authoring`'s 読解 length-band table
(問題10–14) and Benchmark section (問題7/8/9), enforced by
`check_dokkai_lengths()`. A second copy of a number is a second thing to
drift — three copies once hand-synced out of step and 問題11/14 shipped
under band while `make check` stayed green. This file states the *shape*
facts only.

**読解 apparatus** (baseline: `refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`): a
real paper glosses freely across 問題10–13 and uses `（中略）` inside
中文/長文. Gloss count/metric/band and the 問題13 length floor are owned by
`question-authoring`.

**問題11 shape:** every current-era paper is **4 passages × 2 questions**
(Q57–64) — younger than the item counts: 問題11 ran 3 passages through
7/2022, became 4×2 at **12/2022**, length jumping from 1778–2179 to
2449–2685 JP chars (`official_calibration.md` §1–2). The instruction
sometimes still says `(1)から(3)` — **count passage markers, never trust the
instruction**. Generated mocks author 4×2 and print `(1)から(4)`. The
sampler draws `reading_topics: 12` (5 short + 4 medium + 1 A/B + 1 long + 1
info); a spec with only 11 is one 中文 topic short.

**問題11 stem shape (measured, `official_calibration.md` §4, n=7/56 stems):**
**筆者 is not obligatory** — 82% of stems name 筆者, 18% anchor on a marked
span instead (0–3/paper); no official stem anchors on neither. **"At least
one 考え/主張" is paper-level, not pair-level** — pairs split 13 one-of-each/
13 two-事実/2 two-考え, so a per-pair requirement rejects 6 of 7 current
papers. The format fact: the paper carries at least one 考え/主張 stem in
問題11 (spread 1–4 of 8), the 事実把握 stem comes first in 26 of 28 pairs,
and 問題13's item 69 is 考え/主張 in 7 of 7. The four banned retrieval shapes
(「本文で述べられている〜はどれか」「〜として正しいものはどれか」「〜の主な目的は
何か」「〜の内容と合っているものはどれか」) are corroborated at n=15 sittings
— zero occurrences, in any 問題.

### 時間配分の目安 (105分)

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

(Sums to 105 min incl. a 2-min final review.)

## 聴解 — ~50 min, 30 answers

| 問題 | Type | Count | Printed in booklet | Spoken 例? |
|---|---|---|---|---|
| 1 | 課題理解 (what to do first/next) | 5 | 4 options per item + 例 | yes + confirmation |
| 2 | ポイント理解 (why/what point) | 6 | 4 options per item + 例; has option-READING time | yes + confirmation |
| 3 | 概要理解 (gist of monologue) | 5 | NOTHING (memo space only) | yes + confirmation |
| 4 | 即時応答 (quick response, 3 choices) | 11 | NOTHING | yes + confirmation |
| 5 | 統合理解 (long integrated) | 3 answers | **NOTHING — both items** | NO practice (この問題には練習はありません) |

問題5 shape: **2 item blocks, 3 answers** — `1番` + `2番` (二つの質問), **all
choices spoken**. Keys are `問5-1`, `問5-2-1`, `問5-2-2`.

### Printed options are kana-LEANING — the booklet is not a reading test

Official 問題1/2 options are deliberately light on kanji:

```
1 ページがぬけていないか かくにんする      1 食品かんれんの仕事をする
2 本のデータをとうろくする                2 大学院に進む
3 本にカバーをつける                     3 研究の仕事をする
4 イベントで使う本を選ぶ                  4 しゅっぱんしゃで働く
```

確認→かくにん, 登録→とうろく, 印刷→いんさつ, 出版社→しゅっぱんしゃ — while
本/選ぶ/進む/広く stay kanji, and it's editorial (the same option can mix
both). Measured over 297 official options: mean kanji ratio **0.298**, only
32% exceed 0.35. Our eight papers ran 0.472 across 416 options, 73% above
0.35 — denser than any official sitting that parses.

**Why a format fact, not style**: 問題2 gives 20s (`GAP_OPTION_READING`) to
read four options before the talk starts — kanji there is decoding time
stolen from listening, converting a 聴解 item into a 漢字 item. Target
**≤0.35 kanji**, kana on the tested content word rather than grammar.
**Not gated** — only 2–6 of 31 `booklet.md` extracts expose their 問題1/2
option blocks to a parser, so no per-sitting distribution exists to
threshold against; the pooled figure is sound, the per-sitting range isn't.

### 問題5 prints nothing — a deliberate divergence from official

**This repo prints NO options anywhere in 問題5**, 1番 and 2番 alike — the
booklet carries the instruction, a メモ area, and a bare bubble row per
answer; every choice is read aloud. **This is a house rule, not a format
fact.**

**What official actually does:** all 31 sittings print 2番's four options —
names only, and 質問1/質問2 print the SAME four in the SAME order. July 2025:

```
 1. 夕日通り
 2. にしがおか
 3. さくら公園
 4. 東山
```

Dec 2025 prints `1 1番の自転車 / 2 2番の自転車 / …` — the same list emptied
of information; the house rule is the next step along that line. Cost: our
問題5 is harder than the real one (no re-readable list). Do not "restore"
the printed list on the grounds official has it — removed knowingly; raise
it only if QA finds the difficulty wrong.

Mechanically, 問題5 is now shaped exactly like 問題3 (nothing printed,
choices spoken, 3s between them). Three rules follow:

- **No decisive attribute attached to a name** — no 家賃/立地/条件/時間帯/定員
  riding along in the read-back list (`1、夕日通り、海沿いで駅から5分。` is
  forbidden). Restating the deciding attribute in the choice IS the answer.
  Speak the bare name; the deciding detail belongs in the dialogue only.
- **質問1 and 質問2 read the same four choices, in one order** — two
  different lists (or a re-ordering) desynchronizes the two questions.
- **The choice-list order IS the audio's introduction order, and the
  deciding line names a candidate — never an ordinal.** Both measured across
  the archive: July 2025 speaks 1つ目/2つ目/3つ目/最後 and prints the same
  order; the resolving line always names an attribute (「鳥が見られる所？」),
  never a `Nつ目` back-reference, in 31 sittings.

  **Consequence**: a mis-keyed 問題5-2番 is fixed by re-enumerating candidates
  so the dialogue introduces them in the read-back order, then `make mp3
  <test_id>` — **never by re-ordering the choice list alone**, which
  silently re-keys the item against a dialogue still saying 「3つ目の方法が
  ぴったりですね」 (exactly what one repair pass did to `tests/3`).
  `check_mondai5_enumeration()` fails both halves wherever the script uses
  ordinal labels; `check_mondai5_prints_nothing()` fails a booklet printing
  options under 問題5.

## Announcer / 例 mechanics (script + booklet must both honor these)

- Opens (spoken): 「Nに聴解。これから、Nにの聴解試験を始めます。問題用紙にメモを
  とってもかまいません。」 — spell the level `Nに`, never `N2`, so TTS doesn't
  read the digit as English "two" (`choukai-audio` owns TTS spelling). Printed titles may still say `N2`.
- Each of 問題1-4: instruction → 「では、練習しましょう。」 → 例 item →
  「最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。
  最もよいものは◯番ですから、答えはこのように書きます。では、始めます。」
- 問題1/2 questions are spoken TWICE: before and after the conversation.
- 問題3/4/5: choices SPOKEN (「1、…。2、…。」), not printed — all of 問題5
  including 2番's two questions (official prints 2番's). **Spoken ≠ same
  pacing**: 問題3/5 leave ~3.0s between choices; 問題4's three are read
  continuously (1.0–2.0s, ordinary dialogue spacing) — `GAP_BETWEEN_SPOKEN_CHOICES`
  applies to 問題3/5 only, not an oversight.
- 問題5-2番 options are spoken TWICE — after 質問1 and again after 質問2, with
  the 10s answer pause between the two runs.
- Closes: 「これで、聴解試験を終わります。」

## 問題N instruction lines (canonical — transcribed from `refs/JLPT_N2_NEW/`)

Paste these into BOTH `聴解.md` and `聴解スクリプト.txt`; copy from here, never
from a previous test — `make check` only proves booklet and script agree with
EACH OTHER, so both drifting the same way passes green. Transcribed from
July 2025.

| Where | Text |
|---|---|
| 問題1 | 問題1では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。 |
| 問題2 | 問題2では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。 |
| 問題3 | 問題3では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問とせんたくしを聞いて、1から4の中から、最もよいものを一つ選んでください。 |
| 問題4 | 問題4では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、それに対する返事を聞いて、1から3の中から、最もよいものを一つ選んでください。 |
| 問題5 | 問題5では、長めの話を聞きます。この問題には練習はありません。問題用紙にメモをとってもかまいません。 |
| 問題5 1番 | 問題用紙に何も印刷されていません。まず話を聞いてください。それから、質問とせんたくしを聞いて、1から4の中から、最もよいものを一つ選んでください。 |
| 問題5 2番 | 問題用紙に何も印刷されていません。まず話を聞いてください。それから、二つの質問とせんたくしを聞いて、それぞれ1から4の中から、最もよいものを一つ選んでください。 |

- 問題1〜4: the SCRIPT appends 「では、練習しましょう。」, then the 例, then the
  confirmation ending 「では、始めます。」. The BOOKLET prints the instruction only.
- 問題5: both lead-ins are spoken, each its own block BEFORE its `N番。`
  marker — 1番's adds 「では、始めます。」, 2番's doesn't (already running).
  The 2番 line is a house adaptation, since nothing is printed: 「問題用紙に
  何も印刷されていません」 replaces 「問題用紙の」. No combined 「1番、2番。…」 line.
- The official scan renders some words in kana (いんさつ, えらんで); this repo
  writes 印刷/選んで, and `make check`'s typo guard expects 印刷 — either is
  fine as long as booklet and script match.

## 認定の目安 (official level descriptor — what N2 is allowed to test)

> 日常的な場面で使われる日本語の理解に加え、より幅広い場面で使われる日本語を
> ある程度理解することができる
>
> **読む** ・幅広い話題について書かれた新聞や雑誌の記事・解説、平易な評論など、
> **論旨が明快な**文章を読んで文章の内容を理解することができる。・**一般的な話題**
> に関する読み物を読んで、話の流れや表現意図を理解することができる。
>
> **聞く** ・日常的な場面に加えて幅広い場面で、**自然に近いスピード**の、
> まとまりのある会話やニュースを聞いて、話の流れや内容、登場人物の関係を理解
> したり、要旨を把握したりすることができる。

Two consequences: 読解 passages are 新聞・雑誌の記事/解説/平易な評論 with a
**clear line of argument** (N1's descriptor says 論理的にやや複雑/抽象度の
高い文章 — a dense 問題13 is off-level even at the right length); 聴解
dialogue is **自然に近い** speed, not N1's 自然な speed (check `choukai-audio`
before touching `SPEAKER_MAP` rate). The 例 column's pre-marked answer must
equal the announcer's declared number — `make check` compares them.

## Booklet layout conventions

- **Heading structure**: a `#` banner (`# 【文字・語彙】`, `# 【読解】`)
  wrapping `## 問題N` headers. Never make `問題N` an `h1` — the answer-key
  parser (`parse_choukai_keys()`) only recognizes `## 問題N`.
- **Numbering**: bold numbers (`**1**`…`**71**`; `**例**`, `**1番**`) —
  never `1.`/`6.` list syntax (resets HTML `<ol>` numbering).
- 文字・語彙・文法: short options run HORIZONTALLY (` 1. ◯◯  2. ◯◯ …`).
  Reading questions and 問題6 sentences are vertical.
- 聴解 booklet: options stacked VERTICALLY, one per line, in 問題1/2 ONLY
  (the two sections that print any). 問題3/4/5 print a bare bubble row
  (`**1番** 1 ・ 2 ・ 3 ・ 4`) and nothing else.
- Stems bold the tested word (**地域**) or show blanks as (　)/＿＿. The bold
  span covers the whole word, okurigana included — never a bare kanji with
  its tail outside.
- 問題8 uses ＿＿ ＿＿ ★ ＿＿, answer = whichever option lands on ★.
- **読解 vocabulary notes**: 問題9–14 passages carry NO furigana; over-level
  terms are annotated inline only via `（注1）`, `（注2）`…, with structured
  note blocks below the passage before its questions.
- **Passage numbered markers (1-to-1)**: every `①**...**`/`②**...**` in a
  passage must match a question stem — no orphaned markers.

## Answer Key & Explanation Table Structure

The single copy of the answer-key table format — `question-authoring` points
here rather than restating it.

Both booklets conclude with table-formatted keys, opened by a heading
starting `解答` or `正解` (`^#+\s*(解答|【?正解)`) — the marker
`build_interactive.py` truncates from; it aborts if absent. Keep 解答/正解
out of any heading in the question body, or the body gets truncated too:

- `言語知識・読解.md`: key heading (e.g. `# 解答と解説`), containing
  `## 文字・語彙` (multi-column key table), `## 文法` (3-col, Q31–51),
  `## 読解` (3-col, Q52–71).
- `聴解.md`: `# 解答用紙(マークシート)` (bubble sheets 問題1〜5), then
  `# 【正解・解説】※解き終わってから見てください` (section tables per 問題 +
  `## 得点の目安`) — key sub-headers must be `## 問題N`
  (`parse_choukai_keys()` keys off `##`). 問題5's table carries 3 rows for 2
  items, labelled 質問1/質問2.
