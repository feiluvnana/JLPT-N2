---
name: question-authoring
description: Single owner of how to WRITE JLPT exam items at the correct difficulty — vocabulary, kanji, grammar, reading passages, and listening dialogues, including distractor design and answer-key format. Use whenever creating or revising any exam question, whenever the user says questions "seem easy/hard", or when checking difficulty alignment. Difficulty bugs are the #1 revision cause — consult this before writing a single item.
---

# Question Authoring (N2 calibration)

## File Output & Location (Japanese File Names)

Questions are written to Markdown source files inside `tests/<test_id>/`:
- Language Knowledge & Reading: `tests/<test_id>/言語知識・読解.md`
- Listening Booklet: `tests/<test_id>/聴解.md`

## The golden rule

Draft an item, then ask: "would this appear in an N3 book?" If yes, discard.
Verify every tested word/grammar point against reference books in `refs/Shinkanzen/` and benchmark sentence structure, distractor density, and passage length directly against the 5 official past exam sets in `refs/JLPT/` (see `reference-book-reading`).

## Benchmark against Official Exams (`refs/JLPT/`)

Maintain high consistency with the 5 recent official exams (07/2023, 12/2023, 12/2024, 07/2025, 12/2025):
- **Dokkai Character Counts**: Short (~150-200 chars), Medium (~400-500 chars), Long (~700 chars), Flyer (1 table + 2 matching scenarios).
- **Distractor Design**: Distractor options must replicate official confusion logic (e.g. 近義語 nuances, 誤用 collocations, condition disqualifications).
- **Listening Spoken Choice Pacing**: Options spoken in 聴解 must follow official lengths (~10-15 chars per choice in 問題3/問題4).

## Using web seeds from `logs/test_spec.json` (when present)

If `merge_seeds.py` ran, the spec carries web provenance — honor it in every
section, under these caps (full rules: web-topic-research):

- **Provenance is binding**: entries marked `"origin": "web"` are written
  around that seed; `"origin": "pool"` entries stay pool-topic-based. Never
  swap origins to taste — the 30-60% web / ≥40% pool blend is the point.
- **Tested item ≠ web item**: the kanji/word/grammar/idiom being tested is
  ALWAYS the sampled pool item (Shin-Kanzen-calibrated). Web seeds only set
  the topic, scene, or facts around it.
- **問題1-8 carrier sentences**: at most 1 in 3 stems per 問題 may draw on
  `spec.carrier_seeds`; the rest use neutral settings. Same N2 bar: if the
  seed needs N1 vocabulary to mention, don't use it in that stem.
- **問題4 即時応答**: `spec.qr_situation_seeds` may flavor the setting of an
  utterance; the tested keigo/idiom stays the sampled one.
- **問題9**: follow `spec.cloze_topic` (web or pool as rolled).
- **問題14**: if `spec.info_retrieval_texture` exists, weave its (already
  simplified) numbers into the flyer's conditions.
- **Facts**: max one borrowed fact per passage/dialogue, in simplified form
  (約4割, not 38.6%); never reproduce source sentences or article structure.

## Per-section rules

**問題1-2 (kanji)** — test N2-band words: 交渉, 慌てる, 妨げる, 潔い, 措置,
傾向, 効率, 険しい. Build distractors from REAL confusions:
- reading traps: 措置(そち) vs しょち/そうち; homophone kanji sets:
  納める/収める/治める/修める, 敗れる/破れる; same-radical fakes: 険/検/剣/験.

**問題3 (語形成)** — 諸〜, 〜化, 準〜, 〜済み, 〜制, 未〜, 〜性. All four
options must be real affixes; only one collocates.

**問題4 (context)** — N2 nouns/adverbs: 難航, 発足(distractor: 成立),
かろうじて, うんざり, てきぱき, 需要. Distractors share the semantic field.

**問題5 (paraphrase)** — stem contains the HARD word (あいにく, 妥当,
ありふれた, くたくた, 重宝); options are simpler. Never the reverse.

**問題6 (usage)** — 1 correct + 3 sentences that are grammatical but misuse
the word's collocation/domain (妥協, 発揮, 解消, 募集, あふれる). Wrong
sentences must be tempting, not absurd.

**問題7-9 (grammar)** — only N2-list items: 〜かねない, 〜ざるを得ない,
〜わけにはいかない, 〜に先立って, 〜を契機に, 〜つつも, 〜ようがない,
〜に限って, 〜ものの, 〜ばかりに, 〜たところ, humble/honorific traps
(伺う; include one FAKE form like 参られます as a distractor).
BANNED (too easy): 〜によると, 〜ば〜ほど, 〜がち alone, お〜ください.

**問題10-14 (reading)** — difficulty lives in the QUESTIONS, not vocabulary:
ask 筆者の考え/一番言いたいこと/どういうことか, never mere fact lookup.
Passages: opinions with a turn (しかし/ところが), one business email, one
notice with 3 false options contradicted by ※ fine print, one A/B pair
(agree on one point, differ on conclusion), one flyer with two-condition
matching where one tempting option fails exactly one condition.
- **Vocabulary Explanations & Furigana Rules for Dokkai (MANDATORY)**:
  - When authoring reading passages containing uncommon vocabulary, N1/specialized terms, or rare idioms, annotate them in text as `（注1）`, `（注2）`... or HTML ruby syntax `<ruby>難解漢字<rt>なんかいかんじ</rt></ruby>`.
  - Immediately following the passage (before question items), provide a structured vocabulary note block `（注1） 語彙：簡潔な意味の説明` wrapped in a `<div class="vocab-notes">` block or clean paragraph.
  - Furigana should be attached to non-standard readings, proper nouns, or rare kanji above N2 target level using `<ruby>漢字<rt>ルビ</rt></ruby>`.

**聴解 dialogues** — every wrong option must be MENTIONED then eliminated
(already done / rejected / explicitly denied: 「それが理由ではありません」).
課題理解 hides the correct first action behind 「その前に」「それが先」.
即時応答 tests idioms and keigo: 目を通す, お言葉に甘えて, 〜かと思いきや,
〜ようがない, 席を外しております, 在庫を切らしております.

## Markdown formatting contract (CRITICAL to prevent HTML numbering bugs)

- **Question stems MUST use bold numbers, NOT Markdown list syntax**:
  - Write `**1** 労働組合は...`, `**6** 最近...`, `**75** ...` (for `言語知識・読解.md`).
  - Write `**例**`, `**1番**`, `**2番**` (for `聴解.md`).
  - **NEVER** write `1. 労働組合...` or `6. 最近...` — Markdown converts `N.` lines into HTML `<ol>` lists, which resets the question number back to 1 at every section header and indents sub-options as nested lists.
- **Horizontal Options Layout (問題1–5, 問題7, 問題8)**:
  - Options must run on a SINGLE line with leading space and double spaces between choices:
    ` 1. こうしょう  2. こうちょう  3. きょうしょう  4. こうしゅう`
  - The booklet builder detects 3+ options on a line and converts spaces into wide ideographic spaces (`\u3000\u3000\u3000`).
- **Vertical Options Layout (問題6, 問題10–14, 聴解)**:
  - Options must be on separate lines with a leading space:
    ` 1. 資料をコピーする`
    ` 2. 会議室の予約を変更する`

## Answer keys & Explanations (MANDATORY TABLE FORMAT)

Answer keys and explanations MUST be formatted as Markdown tables at the end of `言語知識・読解.md` and `聴解.md`. Single grid summary tables without explanations are STRICTLY FORBIDDEN.

**Both files MUST open their key section with a top-level heading matching
`# 解答…` or `# 【正解…`** — `言語知識・読解.md` uses `# 解答と解説`, `聴解.md` uses
`# 解答用紙(マークシート)`. This is not cosmetic: `build_interactive.py` truncates
the document from that heading onward so the key never renders on the answer
sheet, and it **exits with an error** if the heading is missing. A key section
introduced only by `##` sub-headers will fail the build.

### 1. `言語知識・読解.md` Answer Key Format
Under `# 解答と解説`, must contain three distinct section headers:
- `## 文字・語彙`: Multi-column table (`| 問 | 答 | | 問 | 答 | | 問 | 答 | | 問 | 答 |`) for Q1–32, plus key notes for notable kanji/words.
- `## 文法`: 3-column table (`| 問 | 答 | 解説 |`) for Q33–54 with exact grammar point explanations and scramble sequence breakdowns for Q45–49.
- `## 読解`: 3-column table (`| 問 | 答 | 解説 |`) for Q55–75 quoting key passage text and rationale.

### 2. `聴解.md` Answer Key Format
Must contain two main parts:
- `# 解答用紙(マークシート)`: Standard bubble-sheet tables for 問題1〜問題5 with sample item (例) pre-marked (e.g. `1 **(2)** 3 4`).
- `# 【正解・解説】※解き終わってから見てください`:
  - `## 問題1 課題理解`: 3-column table (`| 番号 | 正解 | 解説 |`) for 1番–5番 quoting deciding phrase.
  - `## 問題2 ポイント理解`: 3-column table (`| 番号 | 正解 | 解説 |`) for 1番–6番.
  - `## 問題3 概要理解`: 3-column table (`| 番号 | 正解 | 解説 |`) for 1番–5番.
  - `## 問題4 即時応答`: 3-column table (`| 番号 | 正解 | ポイント |`) for 1番–12番 detailing honorifics/idiom points.
  - `## 問題5 統合理解`: 3-column table (`| 番号 | 正解 | 解説 |`) with **4 rows, not 3** — 問題5 has 3 items but 4 answers. Label them exactly `**1番**`, `**2番**`, `**3番 質問1**`, `**3番 質問2**`: `parse_choukai_keys()` maps those to the keys `問5-1`, `問5-2`, `問5-3-1`, `問5-3-2`, and a 3-row table silently loses one scored answer.
  - `## 得点の目安`: Score range guidelines.



