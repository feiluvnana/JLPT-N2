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
An option that is raised and left TRUE is a second answer even if it is "only
a contributing factor": test 1's 遅刻理由 item affirmed 道が混んでいた in the
audio while keying USB忘れ — a どうして item's wrong causes must be denied,
not merely outweighed.
課題理解 hides the correct first action behind 「その前に」「それが先」.
即時応答 tests idioms and keigo: 目を通す, お言葉に甘えて, 〜かと思いきや,
〜ようがない, 席を外しております, 在庫を切らしております.

## Item integrity (every rule here shipped broken at least once)

`make check` enforces the mechanical half of this list per test; the rest is on
you. Run it before calling any authoring work done.

- **Four DIFFERENT options.** Never let the same string appear twice in one
  option set — that is a second correct answer. Test 2 shipped
  `1. 削減  2. 削減` and `1. ぶった … 3. ぶった`. When building near-miss kanji
  distractors, read the four back to yourself before moving on.
- **The key goes where `answer_positions` says.** `logs/test_spec.json`
  prescribes the correct-option number for all 107 items so no number is
  over-used. Write the item, then *order the options* so the correct one lands
  on the prescribed slot. Do not write the key you feel like and do not
  "fix" the imbalance later — `make check` compares all 107 against the spec.
- **問題8: the answer is the option on ★, which is the 3rd of 4 blanks.**
  Assemble the full sentence first, confirm it is grammatical, number the
  positions, and only then read off which option sits third. Test 2 shipped
  three of five keys naming the 2nd or 4th blank instead. Write the 解説 as the
  word order with option numbers in parentheses, correct one bolded:
  `状況に(2)→おいて(4)→**価格競争が(1)**→続く限り(3)`. `make check` parses that
  sequence and asserts its 3rd entry equals the key, so it must be a real
  permutation of 1-4 that matches the stem's options.
- **問題8: the stem must be MISSING exactly what the options supply.** Write the
  finished sentence, cut the four-part span out of it, and let the blanks stand
  where the span was — do not leave the words in the stem as well. Test 3
  shipped all five items with the sentence written out in full *and* chopped
  into options, so 45 assembled to
  「兄が外で活発に遊ぶのを外で遊ぶのを好むのに対して…」 and 49 said
  パニックになって twice. Every other 問題8 gate passed, because none of them
  read the stem's own words. The test: splice stem + options in 解説 order and
  read the result end to end. If any word occurs twice, the stem is wrong, not
  the key.
- **Every scramble must form ONE grammatical sentence.** Two options that cannot
  coexist make the item unanswerable no matter the key: test 2 offered both
  「まったく」 and 「ほとんど持てていない」 in one set, and both 「わりに」 and
  「にもかかわらず」 in another. One contrast marker, one degree adverb.
- **問題8: exactly ONE ordering may be natural.** A floating adverb or adjunct
  (ほとんど, 直接, 一度, 年々, 世界中で…) that reads equally well in two slots
  gives the item two defensible ★ answers — QA failed one such item in each of
  tests 2, 3, and 4 (「ほとんど自分の時間を/自分の時間をほとんど」,
  「窓口に直接/直接窓口に」, 「一度原点に/原点に一度」). After assembling the
  sentence, actively try to permute every option into every other slot; if any
  alternative order is grammatical and natural, replace the floating word with
  one that is position-locked (an object with its particle, a conjugation-bound
  form) before shipping the item.
- **A cloze blank must not repeat what the stem already says.** `…からでも
  ( 54 )はいかがだろうか` with option `試してみてはいかがだろうか` ends the
  sentence twice. Read stem-plus-option aloud as one sentence for all four.
- **Exactly ONE option may be defensible.** Three wrong answers, not three
  weaker answers. The failure looks like a well-written item, so it survives
  every gate: test 3's 問題9 (52) offered 無理もないだろう / 自然なことだ /
  珍しいことではない / 仕方がない for 「増えているのも( )」 — four ways of saying
  the same thing, with the key arguably the third-best of them. 問題4 (19) keyed
  切実 while 深刻 sat in the option list and fits 「〜な問題だ」 just as well.
  For every distractor, name the reason it is *wrong* — not merely less apt. If
  the reason is "the key is slightly more natural", rewrite the stem until the
  distractor is impossible (切実 → put it on 願い, where 深刻 cannot go).
- **Name the reason each distractor is IMPOSSIBLE — in writing.** This is the
  single rule that catches the two-defensible-answer family before it ships,
  and test 4 shipped six of them at once: 問題9 (51) offered すなわち against
  the key つまり (the same word), (52) したがって against そう考えると (both
  fit); 問題7 (38) keyed に即して with に沿って in the list, and
  「ニーズに沿ったサービス」 is if anything the commoner collocation; 問題3 (14)
  keyed 未記入 with 無記入 available (both are words); 問題4 (19) keyed おろそか
  with いいかげん beside it, and 健康管理をいいかげんにする is ordinary
  Japanese. Every one reads as a well-made item. Write the reason in the 解説
  cell (「1『に沿って』は…」) — a distractor you cannot explain away is a second
  key, and the fix is to REPLACE THE DISTRACTOR, not to defend the key.
  Near-synonyms are the whole risk: two connectives that both summarize, two
  negative prefixes that both attach, two adverbs that both take 〜にする.
  The same class then failed QA in every earlier test too: 停滞 beside the key
  難航 on 交渉が(　)している (交渉が停滞する is attested), 大満員 beside 超満員,
  消費 beside 需要 on 〜が伸びている, こと beside だけ in a cloze, and a 問題6
  distractor using 把握 in ordinary reportage phrasing. **The test is a search,
  not a feeling**: for every distractor, check whether distractor+frame is an
  attested collocation (search 「<word> 例文」 if unsure); if it exists, the
  item has two keys — replace the distractor.
- **問題5 言い換え: the option must be substitutable.** Read the stem with the
  option swapped in and confirm it is still a grammatical sentence. Test 4
  underlined わりに in 「値段の**わりに**美味しい」 and keyed 比較的, which
  yields 「値段の比較的美味しい」 — the item cannot be answered as printed. A
  meaning match is not enough; the frame around the word has to accept it.
- **問題1 漢字読み: all four options must be the same word form.** Test 4 gave
  the dictionary form 労わる four options of which three were て-forms
  (やしなって・なぐさめて・あがめて), so the answer was identifiable without
  reading the kanji at all. Distractors are READINGS of the same written form —
  ideally a genuine trap the kanji supports (労う = ねぎらう for 労わる = いたわる).
- **One grammar point may be the KEY only once per paper.** Not just one item
  per 問題: test 4 keyed 〜にともなって in 問題7 (33) and again as the 問題9
  blank (53). Cross-check the 問題7/8/9 key list against itself, and keep a
  tested form out of the reading passages too (問題9's passage said
  「時代に即した」 while 問題7 (38) was testing 〜に即して).
- **問題6 用法: the correct sentence must be flawless, the wrong ones merely
  wrong.** Test 4's 妥協 key read 「互いの条件を歩み寄り」 (歩み寄る is
  intransitive) — the one sentence that must be beyond doubt was ungrammatical.
  And a distractor has to be a MISUSE, not a rarer valid use: the same item
  offered 「品質の向上に妥協した」 and the 考慮 item offered 「考慮に値する」,
  both real collocations, so both items had two correct sentences. Before
  keeping a wrong sentence, search the collocation; if it exists, rewrite it.
- **Japanese only — no Latin script in the prose.** A stray English word means
  the sentence was drafted and never finished: test 3's 問題9 read 「単なる無音の
  contrast ではない」. Loan words go in katakana. `make check` allows only the
  initialisms real papers print (SNS, AI, CD…).
- **Distractors must be grammatical Japanese that is merely WRONG.** 用法
  (問題6) distractors are sentences a learner could believe — a wrong
  collocation or domain, never word salad. 「整備がおろそかに完璧だった」 is not
  a distractor, it is a bug: nobody can be tempted by it, so the item tests
  nothing.
- **One grammar point, one item.** Do not test 〜にほかならない in 問題7 and
  again as a 問題9 blank. Check the 問題7/8/9 sets against each other.
- **Explanations must quote the real text.** The 解説 cell for a 読解 or 聴解
  item has to quote the passage or script line that decides it — copy-paste,
  do not paraphrase from memory. Test 2's 聴解 key quoted four lines of dialogue
  that were nowhere in `聴解スクリプト.txt`, which hid a keyed answer that the
  script did not actually support. If you cannot find the quote, the item is
  broken, not the explanation.
  **A paraphrase inside 「」 is a defect even when the key is right** — QA found
  the condensed-quote class in every one of tests 1–3 (13 non-verbatim 「」
  spans in test 3 alone, two of which misstated the audio). Write every 解説
  quote by selecting and pasting the source line at authoring time, then treat
  each `make check` 解説-quote WARN as a diff list to re-paste, never as noise
  to justify.
- **即時応答: the keyed reply must fit the speaker's rank and direction.**
  Keigo has a direction: test 2 keyed a 社長 answering a subordinate with
  「かしこまりました。会議室でお伺いします」 (humble, wrong way up), which made
  a register-appropriate distractor equally defensible, and had a 課長 say
  「拝見しました」 about a subordinate's 議事録. When the prompt names roles,
  check every option's honorific direction against them.

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

**Both files MUST open their key section with a heading whose text starts with
`解答` or `正解`/`【正解`** (regex `^#+\s*(解答|【?正解)`). Any wording qualifies —
existing tests use `# 解答(言語知識・読解)` and `# 解答と解説` for
`言語知識・読解.md`, and `# 解答用紙(マークシート)` for `聴解.md`. This is not
cosmetic: `build_interactive.py` truncates the document from the FIRST such
heading onward so the key never renders on the answer sheet, and it **exits
with an error** if there is none. Two consequences:

- a key section introduced only by `##` sub-headers fails the build;
- never put `解答`/`正解` at the START of a heading in the question body — the
  whole document from there down would be truncated out of the answer sheet.
  (`# 問題用紙・解答用紙` is safe: it starts with 問.)

### 1. `言語知識・読解.md` Answer Key Format
Under the key heading (see above), must contain three distinct section headers:
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
  - `## 問題5 統合理解`: 3-column table (`| 番号 | 正解 | 解説 |`) with **4 rows, not 3** — 問題5 has 3 items but 4 answers, so a 3-row table silently loses one scored answer. The 番号 cell must let `parse_choukai_keys()` reach `問5-1`, `問5-2`, `問5-3-1`, `問5-3-2`; it accepts either label style used so far — `**1番**` / `**2番**` / `**3番 質問1**` / `**3番 質問2**` (preferred for new tests; used by the first, since-removed test 4 — removed in 9a794d5, last at b9b90de; the current `tests/4/` is a different test) or `1` / `2` / `3-質問1` / `3-質問2` (test 1, still on disk). The 3番 rows MUST carry `質問1`/`質問2`; the 1番/2番 rows must NOT.
  - `## 得点の目安`: Score range guidelines.



