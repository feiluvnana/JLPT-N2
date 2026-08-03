---
name: jlpt-exam-structure
description: Single owner of official JLPT exam format facts — section layout, question counts, timing, booklet printing conventions, and announcer/例 (practice example) mechanics. Consult whenever writing, checking, or discussing the structure of a JLPT exam or any of its sections (問題1〜問題14 for N2), including questions like "how many questions in N2 choukai" or "what is printed in the booklet". Other skills MUST defer to this file for format facts.
---

# JLPT Exam Structure (N2 reference)

## Deliverable File Mapping (`tests/<test_id>/`)

- **言語知識・読解**: Source `tests/<test_id>/言語知識・読解.md` → Output PDF `tests/<test_id>/言語知識・読解.pdf`
- **聴解 (Booklet)**: Source `tests/<test_id>/聴解.md` → Output PDF `tests/<test_id>/聴解.pdf`
- **聴解 (TTS Script)**: `tests/<test_id>/聴解スクリプト.txt` (or `script.txt`) → Output MP3 `tests/<test_id>/聴解.mp3`

## 言語知識(文字・語彙・文法)・読解 — 105 min, 75 questions


| 問題 | Type | Count | Q# |
|---|---|---|---|
| 1 | 漢字読み (kanji reading) | 5 | 1-5 |
| 2 | 表記 (orthography: kana→kanji) | 5 | 6-10 |
| 3 | 語形成 (prefix/suffix: 未/化/性/済み/制…) | 5 | 11-15 |
| 4 | 文脈規定 (word in context) | 7 | 16-22 |
| 5 | 言い換え類義 (paraphrase) | 5 | 23-27 |
| 6 | 用法 (correct usage among 4 sentences) | 5 | 28-32 |
| 7 | 文法形式判断 (grammar fill-in) | 12 | 33-44 |
| 8 | 文の組み立て (scramble, ★ position) | 5 | 45-49 |
| 9 | 文章の文法 (cloze passage, 5 blanks) | 5 | 50-54 |
| 10 | 短文 (5 short passages × 1Q; include one business email and one notice/掲示) | 5 | 55-59 |
| 11 | 中文 (3 passages × 3Q, ~400-500 chars each) | 9 | 60-68 |
| 12 | 統合理解 (A/B compared texts, 2Q) | 2 | 69-70 |
| 13 | 主張理解 (1 long essay ~700 chars, 3Q) | 3 | 71-73 |
| 14 | 情報検索 (flyer/table + 2 condition-matching Q) | 2 | 74-75 |

Question numbering is continuous 1-75 across the whole paper.

## 聴解 — ~50 min, 32 questions

| 問題 | Type | Count | Printed in booklet | Spoken 例? |
|---|---|---|---|---|
| 1 | 課題理解 (what to do first/next) | 5 | 4 options per item + 例 options | yes + confirmation |
| 2 | ポイント理解 (why/what point) | 6 | 4 options per item + 例 options; has option-READING time | yes + confirmation |
| 3 | 概要理解 (gist of monologue) | 5 | NOTHING (memo space only) | yes + confirmation |
| 4 | 即時応答 (quick response, 3 choices) | 12 | NOTHING | yes + confirmation |
| 5 | 統合理解 (long integrated) | 4 answers | nothing for 1番/2番; printed options for the final two-question item | NO practice (この問題には練習はありません) |

## Announcer / 例 mechanics (script + booklet must both honor these)

- Exam opens: 「N2聴解。これから、N2の聴解試験を始めます。問題用紙にメモをとってもかまいません。」
- Each of 問題1-4: instruction → 「では、練習しましょう。」 → 例 item →
  「最もよいものは◯番です。解答用紙の問題◯の例のところを見てください。
  最もよいものは◯番ですから、答えはこのように書きます。では、始めます。」
- 問題1/2 questions are spoken TWICE: before and after the conversation.
- 問題3/4/5(1番・2番): choices are SPOKEN (「1、…。2、…。」), not printed.
- Exam closes: 「これで、聴解試験を終わります。」
- Answer grids include an 例 column with the sample answer pre-marked.

## Booklet layout conventions

- **Markdown Question Numbering**: Always use bold numbers (`**1**` ... `**75**` for file 1; `**例**`, `**1番**` for file 2). Never use `1.` or `6.` list syntax to prevent HTML `<ol>` list resets.
- 文字・語彙・文法: short options run HORIZONTALLY on one line
  (` 1. ◯◯  2. ◯◯  3. ◯◯  4. ◯◯`). Reading questions and 問題6 usage sentences are vertical.
- 聴解 booklet: options stacked VERTICALLY, one per line with a leading space.
- Question stems bold the tested word: **地域**, or show blanks as (　) / ＿＿.
- 問題8 uses ＿＿ ＿＿ ★ ＿＿ with the answer = whichever option lands on ★.
- **Dokkai Vocabulary Notes & Furigana**: Reading passages (問題9-14) containing uncommon vocabulary, domain-specific terminology, or rare kanji annotate inline terms using `（注1）`, `（注2）`... or `<ruby>漢字<rt>かんじ</rt></ruby>`. Structured note blocks `（注1） 語彙：説明` sit below the passage before questions.

## Answer Key & Explanation Table Structure

Both booklets must conclude with structured table-formatted answer keys and explanations:
- `言語知識・読解.md`:
  - `## 文字・語彙`: Multi-column key table (`| 問 | 答 | ...`)
  - `## 文法`: 3-column table (`| 問 | 答 | 解説 |`) for Q33–54
  - `## 読解`: 3-column table (`| 問 | 答 | 解説 |`) for Q55–75
- `聴解.md`:
  - `# 解答用紙(マークシート)`: Bubble sheets for 問題1〜問題5
  - `# 【正解・解説】※解き終わってから見てください`: Section-by-section tables (`| 番号 | 正解 | 解説 |`) for 問題1〜問題5 + `## 得点の目安`

