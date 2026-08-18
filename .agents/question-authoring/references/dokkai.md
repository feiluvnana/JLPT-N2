# 読解 (問題10–14) — construction rules

Section reference for the `question-authoring` skill. Read the core
`SKILL.md` alongside this file — it carries the N2-band rule, distractor
discipline, item integrity, and key-cell artifacts. This file adds the
問題10–14-specific rules and owns the repo's single copy of the 読解
length-band table.

## What a 読解 section is

Difficulty lives in the QUESTIONS, not the vocabulary: ask 筆者の考え/
一番言いたいこと/どういうことか, never mere fact lookup. Passage inventory
per paper: opinions with a turn (しかし/ところが), one business email, one
notice with 3 false options contradicted by ※ fine print, one A/B pair
(agree on one point, differ on conclusion), one flyer with two-condition
matching where one tempting option fails exactly one condition.

**NO FURIGANA in 読解** — passages (問題9–14), stems, and options carry no
`<ruby>`; over-level/rare/domain words are glossed only via `（注N）` (below).

## Thirteen surfaces, thirteen different essays — subject AND closing move

The 読解 half is 13 surfaces (問題9 cloze + 問題10×5 + 問題11×4 + 問題12 +
問題13 + 問題14). They must differ on **two** axes — a paper can pass the
first while failing the second badly (`20260810_1` shipped both through a
green gate).

**Axis 1 — subject/theme. All thirteen carry DIFFERENT themes**
(`exam-blueprint` §"The four theme rules" rule 3) — not "at most two per
theme", one each; 19 of 20 themes carry reading entries, so 13 distinct is
always reachable. **Count the SHIPPED surfaces, not the spec draw** — a
sampler draw of two `働き方` topics can still ship five workplace surfaces
once untracked web seeds and the cloze are counted (`20260810_1`'s
precedent). The recording rule that closes this hole is `exam-blueprint`
§"`logs/topics.json`" — every surface, web ones included, records a theme.

**Axis 2 — the closing move, which no theme tag can see.** Two passages on
different subjects are still the same essay if both end 「制度／技術／箱を
整えるだけでは足りない。人の姿勢こそが要る」 — `20260810_1` ran that move in
nine of ten essay-type passages. Measured over the 問題10–14 region of the
archive (marker family 「〜だけで(は)」「こそ」「〜て初めて」「求められている／
欠かせない」「〜ではないだろうか」): official runs **5–9 per 読解 half,
median 6**; generated papers without this rule ran 23–33.
`check_dokkai_rhetorical_monotony()` WARNs above 12 (official max 9 +
headroom) and prints the per-marker split — a WARN here is a rewrite
instruction, not noise.

**How to comply while drafting** — write each passage's closing move beside
its theme, and vary the list. No more than **two** passages may share one
shape:

- 主張 — 「AだけではB、Cこそが」 (the move above; ≤2 per paper, not 9)
- 説明 — explains a mechanism/distinction and stops there
- 意外な観察 — an unexpected fact, then its cause (「意外にも〜。理由は〜」)
- 反論応答 — 「〜という批判もあるが、実際には〜」
- 随筆 — a personal observation that generalises without prescribing
- 条件提示 — a concrete, checkable condition (「〜した自治体ほど〜」), no exhortation

**The ≤2-per-shape cap is not enough alone — the two sharing a shape must
also differ at the SENTENCE-TEMPLATE level**, not swap content words into
the same skeleton. `20260817_2` shipped three such pairs (same closing
sentence pattern, different content) that passed both the shape cap and the
marker scan, since both classify by CATEGORY, not literal skeleton — if two
passages assigned the same shape share a template, rewrite one to a
structurally different pattern for that shape before finalizing.

If a closing explicitly REJECTS a stated single-factor view
(「〜という見方には無理がある」, 「〜だけでは…」) before its conclusion,
classify it as 主張 regardless of whether it uses the literal marker
「こそが」 — 条件提示 never opens with an explicit rejection, only reports a
correlation. This makes the 主張-vs-条件提示 call mechanical rather than a
coin flip between reviewers (two independent QA passes on `20260813_1` split
on exactly this before the rule existed).

**Genre carve-out** (`20260817_1` QA finding): the override above does not
apply when the rejection targets the AUTHOR'S OWN prior self-understanding
inside a first-person, non-argumentative essay — a memoir realising "this
was never just X, it's part of who I am" is 随筆 (personal reframe), not 主張
(a societal claim aimed at the reader), even sharing the same 「…ではなく…だ」
grammar. Check whether the passage's other paragraphs argue FOR a course of
action addressed to the reader (主張) or simply narrate a realisation with
no prescription (随筆) — the override fires only on the former.

**Thirteen surfaces do not force thirteen instances of the six shapes.** 6
shapes × cap 2 = 12 < 13, so at least one surface must sit OUTSIDE this
taxonomy rather than forcing a 3rd instance into any shape. 問題14 is
normally that surface — a flyer has no authorial voice or argument, and no
closing move in this narrative sense; treat it as outside the taxonomy by
default and reserve the six shapes for the twelve essay-type surfaces (問9,
問10×5, 問11×4, 問12, 問13), each capped at exactly 2.

**The answerability consequence, which is the real damage.** When nine
passages close the same way, their keys close the same way too —
`20260810_1`'s 52/54/56/58/60/62/64/69 were all the "human/attitude" option
beside three 「Xさえすれば十分」 strawmen, so a test-taker keys eight items by
picking the soft-sounding option without reading a single passage.
Distractor sets must vary in kind across the section; a section whose wrong
options are uniformly overstatements is strategy-solvable regardless of how
well each item reads alone.

## 読解 distractors — no free eliminations

A 読解 distractor must be eliminable only by checking it against the
passage's actual content — never on sight, passage closed, by spotting an
absolute quantifier or categorical denial (`exam-qa-review`'s ground rules
already treat this as automatic fail: すべて/まったく/のみ/だけで十分/
無関係/存在しない). `check_consistency.py` WARNs a candidate for human
judgment, since it can't tell an on-sight-eliminable use from a
content-dependent one that merely contains the token (「戸籍謄本も**すべて**
オンライン提出できる」 is fine — still requires checking the passage).
Shipped in all 8 prior generated papers before `20260813_2`'s QA caught it.

- **Don't:** 「〜すれば、同居の問題は**すべて**解決するということ」 — rejected
  without opening the passage.
- **Do:** 「〜が同居の理想的な解決策だということ」 — plausible until checked
  against what the passage actually argues, so eliminating it requires
  reading.

## Length bands — the single copy in this repo

These numbers once lived in three files at once, hand-synced, and 4/4
generated papers shipped 問題11/問題14 under band while every gate stayed
green. Stated **here and nowhere else** — `jlpt-exam-structure` points at
this table, and `check_dokkai_lengths()` enforces the floors.

| Section | official min | official median | gate floor |
|---|---|---|---|
| 問題10 短文 (5 passages) | 1143 | 1225 | **≥1100** |
| 問題11 中文 (4 passages) | 2449 | 2556 | **≥2250** |
| 問題12 A/B | 532 | 551 | **≥510** |
| 問題13 長文 | 814 | 904 | **≥800** |
| 問題14 情報検索 | 489 | 604 | **≥450** |

(`DOKKAI_FLOOR` in `tools/check_consistency.py` — re-calibrated against the
31-sitting archive to sit below every official paper; a check an official
paper fails is a wrong check, so the code is authoritative if this table drifts.)

Per-passage floors: each 問題10 passage ≥150 JP chars, each 問題11 passage
≥400 (`DOKKAI_PASSAGE_FLOOR`). Current-era per-passage measurements: 問題10
157/241/334 (min/med/max, n=35), 問題11 507/655/763 (n=28) — author 問題10 to
~240, 問題11 to ~650. An official 短文 is *allowed* to be short; a generated
one that's short is usually thin, not deliberate.

**Counting method, stated once**: JP characters only (hiragana/katakana/
kanji/JP punctuation, same class `check_dokkai_lengths()` uses) over
**passage prose only** (instructions/stems/options removed; `（注N）`
definitions kept). Digits/Latin/spaces excluded. Never quote a length
without naming this method.

**Author to the medians, not the floors** — every floor sits below the
official minimum by design, so clearing the gate alone still leaves a paper
under-length against the band. Don't pad the note block or stems to hit a
floor — the gate measures the passage region (問題14's table/conditions
count). **問題14 misleads in JP chars**: counted all-char it measures
676–793, median 707 — right on 700字程度 while looking ~25% short in JP chars.

**Calibrate to the era, not a paper**: 問題11 became 4×2 at 12/2022 and its
length jumped with it — the window is 12/2022–12/2025 (7 sittings), never
"the last five papers," which mixes eras. Per-sitting figures:
`official_calibration.md` §2.

## （中略）

Official ships **2–5 per paper in the current era, median 3, never zero**
(`official_calibration.md` §3) — avoid shipping zero. Cut at least one
passage across 問題11–13, and every `（中略）` must sit inside a 問題11–13
passage body, never floating under an instruction line.

## Marked-span quoting — bold every span a question anchors on

**Rule (every 問題10–14 stem):** whenever a stem anchors on a specific span
via `「…」とあるが` — a quoted clause, sentence, or defined term — that EXACT
span must be marked in the passage body with a circled-number marker AND
bolded, `①**span**`, and the stem must reference it identically,
`①**span**とあるが`. Never leave either side as a bare `「quoted text」とあるが`
with no marker/bold — `check_dokkai_numbered_markers` only asserts passage
and question markers match as SETS, so a paper with zero markers anywhere
passes it trivially. `check_dokkai_span_anchor_bold` FAILs the bare-quote
shape directly (WARNs on a marker present without the bold — the milder
half, since a marker at least gives the set-match check something to pair).

Every paper in the repo follows this except `20260817_1`, which shipped
three span-anchored stems as plain bare quotes. The rule applies equally to
a defined vocabulary term (`①**重ね合わせ**`) and to a full clause/sentence
span — a definitional gloss on a bolded term goes OUTSIDE the bold
(`①**重ね合わせ**（注2）`, never `①**重ね合わせ（注2）**`).

A passage with multiple span-anchored questions numbers them ①②③… in
reading order; one question still uses ①, never a bare quote. An unanchored
stem (筆者の考えに合うのはどれか) needs no marker — this rule only fires on
the `「…」とあるが` shape.

## 問題11 stems

All figures from `official_calibration.md` §4 — current era, n=7 sittings,
28 pairs, 56 stems; where it disagrees with July 2025 alone, the archive wins.

- **Anchoring:** every stem is anchored on **筆者** or a **marked span**
  (「①…とあるが」/「〜とは何を指すか」). 82% name 筆者; 18% don't and anchor on
  a span instead (0–3 per paper). Avoid unanchored pure-retrieval shapes.
- **Banned — four pure-retrieval shapes:** 「本文で述べられている〜はどれか」
  「〜として正しいものはどれか」「〜の主な目的は何か」「〜の内容と合っているもの
  はどれか」 — 0 occurrences across 15 sittings, in any 問題. `make check`
  FAILs on them.
- **Paper level: 問題11 carries at LEAST ONE 考え/主張 stem** — official
  spread is 1–4 of 8. Zero is the defect and the gate FAILs it. Author 2–3
  of the eight (archive median), at most one per pair.
- **Pair level: the 事実把握 stem comes FIRST** — 26 of 28 official pairs
  (exceptions are the two 考え/考え pairs). The gate WARNs on an inverted
  pair — a style regularity, not an answerability defect.

**The old "one 事実把握 + one 考え/主張 per pair" rule is NOT a rule** — over
28 current-era pairs the split is 13 one-of-each, 13 two-事実, 2 two-考え, and
July 2025 is the ONLY sitting where all four pairs come out one-of-each. As a
per-pair requirement it rejects 6 of 7 current official papers — it is not a
requirement, and this file is where that statement lives. (**問題13 IS
regular**: item 69 is a 考え/主張 stem in 7 of 7 papers — treat that slot as
mandatory.)

Classify each stem by SHAPE, not intent — span anchoring is tested FIRST,
since 「売れた理由とあるが、筆者はなぜ売れたと考えているか」 is 事実把握 despite
containing 考えて:

- **事実把握** — anchored to a specific span/term/sub-topic, answerable from
  the sentences around it: 「①…とあるが、どういうことか」/「〜について、筆者は
  どのように述べているか」/「筆者によると、…とはどういうことか」.
- **考え/主張** — unanchored, answerable only from the passage as a whole:
  「筆者の考えに合うのはどれか」/「筆者が最も言いたいことは何か」.

Write the eight labels down while drafting and count the 考え/主張 ones. If
zero, rewrite the SECOND stem of one pair as an unanchored 考え question —
never re-label a stem to make the tally look right.

## （注N） glosses

- **Pairing is 1-to-1 per passage, both directions** — every definition line
  annotates a word actually in that passage's body, and every in-body marker
  has a definition line. An orphan either way is an automatic QA fail.
- **Count in-body markers**, not raw occurrences (each gloss also has a
  definition line, so occurrence-counting nearly doubles the figure).
- **The two numbers:** the gate WARNs below 25 in-body glosses
  (`GLOSS_MARKER_MIN` — a floor below every current official paper). **Author
  to the band, not the floor**: current-era band 27–61/paper, median 39,
  target ~30–40, plus ≥3 in every 中文/長文 passage.
- **Where the count is earned** — never a per-問題 floor touching 問題12/14
  (zero glosses in every current-era paper):

  | | 問題10 | 問題11 | 問題12 | 問題13 | 問題14 |
  |---|---|---|---|---|---|
  | current-era range | 3–13 | 17–36 | **0** | 0–12 | **0** |
  | median | 6 | 24 | **0** | 7 | **0** |

  Per 問題11 passage: min 2, median 5.5, max 13 (26 of 28 ≥3). Plan ~5 per
  中文, ~7 for the 長文; do not spread a quota across 問題10 to reach a number.
- **The count rule and the band rule are ONE rule.** Reaching the count with
  basic-word glosses (割引・洗髪・契機・規制・革新・省力化・増幅) is worse than a
  low count — it degrades the passage. A specialized subject naturally
  carries five domain terms; a plain-vocabulary passage carries none and
  can't be rescued by annotation afterward. If a draft yields fewer than 3
  glossable terms, its subject is too plain for 中文 — deepen the subject,
  never gloss down to the floor.
- **STRICT vocabulary band for notes:**
  - 🚫 **BANNED**: glossing N3–N5 or standard N2 vocabulary (選択, 信号, 技術,
    文化, 質, 準備, 手順, 設計, 現象, 経由, 偏り, 維持, 継続, 前提, 細部,
    バランス — examples, not the boundary) with trivial/circular definitions.
  - 🚫 **The operational test**: (1) genuinely above N2 band — check against
    Shin Kanzen N2-Goi/N2-Kanji and Soumatome N2 語彙/漢字: if either carries
    it as a headline N2 word, don't gloss it; AND (2) the definition
    introduces words the term itself does not contain (「洗髪：髪の毛を洗う
    こと」 fails; 「大脳辺縁系：…」 passes). `make check` WARNs on condition
    (2) only (no corpus needed since `openjlpt`'s removal); condition (1) is
    a manual band judgment (`exam-qa-review` §2.5). **Both conditions are
    necessary, neither sufficient** — a term absent from Shinkanzen/Soumatome
    isn't automatically over-level (準備, 技術, 選択 plausibly are too, and
    are still banned).
  - ✅ **TARGETS**: N1-level/rare/literary words (委ねる, 雄弁, 死守する,
    顧みる, 飼いならす, 抑圧, その場しのぎ); onomatopoeic/colloquial
    (むきむきの); specialized/domain jargon (大脳辺縁系, 起業, 機動性);
    contextual/figurative metaphors (余白のあるメディア, 思い出の扉).
  - **Cross-check against this SAME paper's 問題1–6.** `20260811_1` glossed
    健やかさ in 問題11(4) while 健やか was, in the same paper, a 問題6 key —
    proving the word is ordinary N2 vocabulary. `check_note_band_reuse()`
    FAILs a same-paper match mechanically (plain string search) — found the
    same defect independently in 3 more papers by 2026-08-17. A DIFFERENT
    shape (a passage's own specialized subject noun repeating unglossed many
    times within its own passage, e.g. 仮眠, フィルターバブル) is NOT the same
    defect — that's the passage's actual topic recurring, not a leaked
    band-reuse; treat repetition as a prompt to look twice, not a rule.
  - **The band call is still mostly manual** — a 2026-08-17 audit found
    roughly a THIRD of all glosses across ten papers (18–52% per paper, no
    paper clean) targeted ordinary N2-or-easier vocabulary (クレーム, 議会,
    アーカイブ, 懸念, 検証, 遠慮, 対話, 委ねる, 沈黙, 示唆, 発酵食品, こつ,
    相談役, 培養, 水素, 実感, 化学物質, 摩擦, 妥当, 助成, 共生, 栞, 衰退, 端末,
    安否, 代替, 郷土料理, 解明する, 惣菜, 厄介, 障壁 — worked examples, not a
    closed list). The test is always the two conditions, not list membership.
  - **A note can leak the answer even when band and circularity are both
    fine** — if a gloss's definition states the fact/cause/comparison the
    item tests, the reader answers from the glossary without engaging the
    passage. Confirmed: `20260817_1`'s 重ね合わせ note IS item 57's answer;
    `20260814_1`'s 物理的環境 note states the passage's whole thesis before
    the reader gets there. Before finalizing a gloss, check whether it
    already answers its anchored item — if so, generalize the definition
    (meaning only, never why it matters) or gloss a different word. No
    mechanical check catches this; QA must (`exam-qa-review`'s two-answer hunt).
- Annotate strictly as `（注1）`, `（注2）`… (never `<ruby>`), one line per
  note immediately after the passage.

## 問題14 (情報検索)

**70 and 71 are BOTH person-scenario items** — 7 of 7 papers
(`official_calibration.md` §6). The answer always combines **≥2**
constraints from the table (topic+date/time, or category+footnote
exception; commonly 3). Never a single-field lookup.

- **71 may never be** 「このお知らせの内容と合っているものはどれか」 — a
  content-match question collapses to a one-cell lookup (shipped in
  t2/t3/t4; no official paper uses it). Write 71 as a second applicant whose
  plan fails exactly one condition.
- Two official shapes: a named person with 2–3 requirements → which option;
  a named person on a given date → what to do to book, decided by a footnote.
- **The 解説 cells for 70/71 must each quote the TWO flyer cells the key
  combines** — one quote means one constraint. `make check` FAILs a cell
  with fewer than two distinct quoted spans occurring in the flyer text.
- Every constraint the QUESTION references must be describable from the
  flyer text as printed — never invent a role/category the source doesn't
  describe.
- **Every WRONG option must contain at least one clause factually FALSE
  against the flyer** — not merely incomplete. `20260811_1` shipped a wrong
  option combining two BOTH-true clauses (true-but-incomplete is a second
  defensible answer). Build a wrong option from a true combination with ONE
  fact changed to something the flyer contradicts, never by omission alone.

## 読解 keys — unpredictable option lengths and strict paraphrasing

### 1. Option length balance and unpredictable key length (longest answer rate ~20–35%)

**BINDING: key length must be unpredictable, all four options within ~30%
of each other (max/min ≤ 1.30).**

1. Every keyed item (問題10–14, 52–71): four options' JP-char lengths satisfy
   max/min ≤1.30 — `make check` FAILs (`check_dokkai_option_length_balance`).
2. The key must NOT be predictably the longest option. **Two rates, not one**
   — measured over 219 official items in 31 sittings:

   | measure | official | FAIL above |
   |---|---|---|
   | key is (tied-)longest | 30 % | 35 % |
   | key is the UNIQUELY longest | **20 %** | **30 %** |

   Both are gated (`check_dokkai_longest_key_rate`). The pair exists because
   the tied rate alone is gameable, and was gamed: nine of the eleven papers
   on disk sat at exactly 6/20 = 30 % tied — authored straight at the top of
   the old "20–35 %" target — but reached it with the key the UNIQUELY longest
   every time, where official reaches the same 30 % partly through ties
   (2026-08-18, user report). Since rule 1 clusters all four options into a
   ±30 % band, "a hair longer than all three" is a reliable tiebreak inside
   it: `20260810_2` keyed 37 vs [31,31,32], 41 vs [33,33,34], 38 vs [31,31,32]
   and three more like them, every item inside every per-item rule.
   **Author to 20 % uniquely-longest, not to the ceiling.**
3. Vary key length rank across items (~4–6 each of rank 1/2/3/4) by
   lengthening distractors with genuine, passage-groundable clauses
   (conditions, consequences, qualifications — never filler). Letting the key
   TIE the longest distractor is a legitimate repair — official does it — and
   a one-character trim is usually all a tie needs. Do not shorten a key to
   fix rank: 問題10–13 keys carry the paraphrase load (§2 below), and
   shortening is how a paraphrase collapses back into the passage's wording.
4. The same tell is gated in 聴解, where it was far worse (39–79 % per paper):
   `question-authoring/references/choukai-items.md` §"Key length carries no
   information".

### 2. Strict key paraphrasing — keys must NEVER be verbatim text lifts

**BINDING: every key in 問題10–13 (52–69) must be genuinely paraphrased.**

1. No verbatim lifts: an LCS against the passage ≥15 JP chars AND ≥50% of
   the key length is a FAIL (`check_verbatim_keys`); ≥20 chars is an
   automatic FAIL; ≥85% verbatim on a short key is an automatic FAIL. (問題14
   items 70–71 are excluded — flyer lookup tests exact printed conditions.)
2. Rephrase the author's logic with synonyms, abstract summaries, or
   grammatical restructuring. Test: can a test-taker find the answer by
   searching for identical character sequences in the passage? If yes, rewrite.

### 3. Stems quoting marked spans

A key must never be answerable purely from the stem's own quoted span. When
a stem anchors on `①**quoted clause**とあるが`, the key must require
synthesizing something OUTSIDE that clause (its cause, consequence, or a
term it defines) — never restate the clause with a synonym swapped in. Draft
the key from the passage's surrounding reasoning, then check: does the
option depend on anything the stem didn't already show the reader? If not,
rewrite it.
