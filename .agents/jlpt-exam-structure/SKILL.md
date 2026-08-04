---
name: jlpt-exam-structure
description: Single owner of official JLPT exam format facts — section layout, question counts, timing, booklet printing conventions, and announcer/例 (practice example) mechanics. Consult whenever writing, checking, or discussing the structure of a JLPT exam or any of its sections (問題1〜問題14 for N2), including questions like "how many questions in N2 choukai" or "what is printed in the booklet". Other skills MUST defer to this file for format facts.
---

# JLPT Exam Structure (N2 reference)

## Deliverable File Mapping (`tests/<test_id>/`)

All section layouts, question counts, and item specifications in this document are benchmarked against and aligned with the 5 official JLPT past exams in `refs/JLPT/` (07/2023, 12/2023, 12/2024, 07/2025, 12/2025).

The official JLPT guidebook lists slightly higher 小問数 as 目安; **actual recent papers** (every exam in `refs/JLPT/`) use the counts below. Prefer the past-exam counts over the guidebook table when they disagree.

- **言語知識・読解**: Source `tests/<test_id>/言語知識・読解.md` → Booklet `tests/<test_id>/言語知識・読解.html`
- **聴解 (Booklet)**: Source `tests/<test_id>/聴解.md` → Booklet `tests/<test_id>/聴解.html`
- **聴解 (TTS Script)**: `tests/<test_id>/聴解スクリプト.txt` → Output MP3 `tests/<test_id>/聴解.mp3`
- **Answer sheet**: both Markdown sources → the ONE merged `tests/<test_id>/解答.html` (there are no per-section `*_解答.html` files)

## 言語知識(文字・語彙・文法)・読解 — 105 min, 71 questions


| 問題 | Type | Count | Q# |
|---|---|---|---|
| 1 | 漢字読み (kanji reading) | 5 | 1-5 |
| 2 | 表記 (orthography: kana→kanji) | 5 | 6-10 |
| 3 | 語形成 (prefix/suffix: 未/化/性/済み/制…) | 3 | 11-13 |
| 4 | 文脈規定 (word in context) | 7 | 14-20 |
| 5 | 言い換え類義 (paraphrase) | 5 | 21-25 |
| 6 | 用法 (correct usage among 4 sentences) | 5 | 26-30 |
| 7 | 文法形式判断 (grammar fill-in) | 12 | 31-42 |
| 8 | 文の組み立て (scramble, ★ position) | 5 | 43-47 |
| 9 | 文章の文法 (cloze passage, 4 blanks) | 4 | 48-51 |
| 10 | 短文 (5 short passages × 1Q; include one business email and one notice/掲示) | 5 | 52-56 |
| 11 | 中文 (3 passages, 8Q total — typically 2+2+4; ~400-500 chars each) | 8 | 57-64 |
| 12 | 統合理解 (A/B compared texts, 2Q) | 2 | 65-66 |
| 13 | 主張理解 (1 long essay ~700-900 chars, 3Q) | 3 | 67-69 |
| 14 | 情報検索 (flyer/table + 2 condition-matching Q) | 2 | 70-71 |

Question numbering is continuous 1-71 across the whole paper.

## 聴解 — ~50 min, 30 answers

| 問題 | Type | Count | Printed in booklet | Spoken 例? |
|---|---|---|---|---|
| 1 | 課題理解 (what to do first/next) | 5 | 4 options per item + 例 options | yes + confirmation |
| 2 | ポイント理解 (why/what point) | 6 | 4 options per item + 例 options; has option-READING time | yes + confirmation |
| 3 | 概要理解 (gist of monologue) | 5 | NOTHING (memo space only) | yes + confirmation |
| 4 | 即時応答 (quick response, 3 choices) | 11 | NOTHING | yes + confirmation |
| 5 | 統合理解 (long integrated) | 3 answers | nothing for 1番; printed options for 2番's two questions | NO practice (この問題には練習はありません) |

問題5 shape (recent official papers): **2 item blocks, 3 answers** — `1番` (spoken choices) + `2番` (二つの質問, options printed). Keys are `問5-1`, `問5-2-1`, `問5-2-2`.

## Announcer / 例 mechanics (script + booklet must both honor these)

- Exam opens: 「N2聴解。これから、N2の聴解試験を始めます。問題用紙にメモをとってもかまいません。」
- Each of 問題1-4: instruction → 「では、練習しましょう。」 → 例 item →
  「最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。
  最もよいものは◯番ですから、答えはこのように書きます。では、始めます。」
- 問題1/2 questions are spoken TWICE: before and after the conversation.
- 問題3/4/5(1番): choices are SPOKEN (「1、…。2、…。」), not printed.
  **Spoken ≠ same pacing**: measured on the official Dec 2025 audio, 問題3 and
  問題5 leave ~3.0 s between choices, while 問題4's three choices are read
  continuously (1.0–2.0 s apart, i.e. ordinary dialogue spacing). That is why
  `GAP_BETWEEN_SPOKEN_CHOICES` in `choukai-mp3-generation` applies to 問題3/問題5
  only — not an oversight; do not "fix" it.
- 問題5 2番 options are printed only — do not speak them.
- Exam closes: 「これで、聴解試験を終わります。」
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
- 聴解 booklet: options stacked VERTICALLY, one per line with a leading space.
- Question stems bold the tested word: **地域**, or show blanks as (　) / ＿＿.
- 問題8 uses ＿＿ ＿＿ ★ ＿＿ with the answer = whichever option lands on ★.
- **Dokkai Vocabulary Notes & Furigana**: Reading passages (問題9-14) containing uncommon vocabulary, domain-specific terminology, or rare kanji annotate inline terms using `（注1）`, `（注2）`... or `<ruby>漢字<rt>かんじ</rt></ruby>`. Structured note blocks `（注1） 語彙：説明` sit below the passage before questions.

## Answer Key & Explanation Table Structure

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
