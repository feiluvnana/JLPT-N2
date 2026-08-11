# 読解 (問題10–14) — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — it carries the N2-band rule, distractor discipline, item
integrity, and the key-cell artifacts. This file adds the 問題10–14-specific
rules and owns the repo's single copy of the 読解 length-band table.

## What a 読解 section is

Difficulty lives in the QUESTIONS, not the vocabulary: ask
筆者の考え/一番言いたいこと/どういうことか, never mere fact lookup. Passage
inventory per paper: opinions with a turn (しかし/ところが), one business
email, one notice with 3 false options contradicted by ※ fine print, one A/B
pair (agree on one point, differ on conclusion), one flyer with two-condition
matching where one tempting option fails exactly one condition.

**NO FURIGANA in 読解:** passages (問題9–14) and question stems/options carry
no `<ruby>` — test-takers read N2 kanji unaided. Over-the-level, rare, or
domain words are glossed ONLY via `（注N）` (below).

## Thirteen surfaces, thirteen different essays — subject AND closing move

The 読解 half is 13 surfaces (問題9 cloze + 問題10×5 + 問題11×4 + 問題12 + 問題13 +
問題14). They must differ on **two** axes, and a paper can pass the first while
failing the second badly. 20260810_1 shipped both failures through a green gate.

**Axis 1 — subject/theme. All thirteen carry DIFFERENT themes**, per
`exam-blueprint` §"The four theme rules" rule 3. Not "at most two per theme" —
one each. 19 of the 20 themes carry reading entries, so 13 distinct is always
reachable and a repeat is a re-angle, never a pool limit.

**Count the SHIPPED surfaces, not the spec draw.** 20260810_1's spec drew only
two `働き方` reading topics, but the two web seeds carried no `theme` at all and
the 問題9 cloze was never counted, so the paper shipped **five**
workplace-institution surfaces (問題9 職場の熱中症対策 / 問題10(4) 育休メール /
問題11(1) 職場のメンタルヘルス / 問題11(4) 転職と定着 / 問題12 ワーケーション)
while every gate stayed green. The recording rule that closes this hole is
`exam-blueprint` §"`logs/topics.json`" — every surface, web ones included,
records a theme, and `check_topics_themes()` reads them.

**Axis 2 — the closing move, which no theme tag can see.** Two passages on
completely different subjects are still *the same essay* when both end
「制度／技術／箱を整えるだけでは足りない。人の姿勢こそが要る」. 20260810_1 ran
that one move in **nine of its ten essay-type passages**; a reader meets the
same argument thirteen times and the paper reads as one author with one idea.

MEASURED over the 問題10–14 region of the 31-sitting archive, counting the
marker family 「〜だけで(は)」「こそ」「〜て初めて」「求められ(ている)／欠かせない」
「〜ではないだろうか／のではないか」:

| | official (7 current-era sittings) | generated |
|---|---|---|
| markers per 読解 half | **5–9, median 6** | 23 / 29 / **33** |

Official uses the move — it just does not use it *twice in a row*.
`check_dokkai_rhetorical_monotony()` in `tools/check_consistency.py` **WARNs
above 12** (official max 9 + headroom, so no real paper trips it) and prints the
per-marker split. A WARN here is a rewrite instruction, not noise.

**How to comply while drafting** — write the closing move of each passage in one
line beside its theme, and require the list to be varied. The shapes official
actually ships, so no more than **two** passages share one:

- 主張 — 「AだけではB、Cこそが」 (the move above; ≤2 per paper, not 9)
- 説明 — the passage explains a mechanism or a distinction and stops there
- 意外な観察 — an unexpected fact, then its cause (「意外にも〜。理由は〜」)
- 反論応答 — 「〜という批判もあるが、実際には〜」
- 随筆 — a personal observation that generalises without prescribing
- 条件提示 — a concrete, checkable condition (「〜した自治体ほど〜」), no exhortation

**The answerability consequence, which is the real damage.** When nine
passages close the same way, their keys close the same way too: 20260810_1's
52/54/56/58/60/62/64/69 were all the "human/attitude" option beside three
「Xさえすれば十分」 strawmen — a test-taker keys eight items by picking the
soft-sounding option **without reading a single passage**. Distractor sets must
therefore vary in kind across the section (see the core `SKILL.md` distractor
rules); a section whose wrong options are uniformly overstatements is
strategy-solvable however well each item reads on its own.

## Length bands — the single copy in this repo

These numbers once lived in three files at once, hand-synced, and 4/4 generated
papers shipped 問題11 and 問題14 under band while every gate stayed green. They
are stated **here and nowhere else** — `jlpt-exam-structure` points at this
table — and `check_dokkai_lengths()` in `tools/check_consistency.py` enforces
the floors.

| Section | official min | official median | gate floor |
|---|---|---|---|
| 問題10 短文 (5 passages) | 1143 | 1225 | **≥1100** |
| 問題11 中文 (4 passages) | 2449 | 2556 | **≥2250** |
| 問題12 A/B | 532 | 551 | **≥510** |
| 問題13 長文 | 814 | 904 | **≥800** |
| 問題14 情報検索 | 489 | 604 | **≥450** |

(The gate floors are `DOKKAI_FLOOR` in `tools/check_consistency.py`, and the
code is the authority if this table ever drifts — they were re-calibrated
against the 31-sitting archive to sit *below* every official paper, so a
check an official paper fails is a wrong check.)

Per-passage floors on top of the section totals: **each 問題10 passage ≥150 JP
chars, each 問題11 passage ≥400** (`DOKKAI_PASSAGE_FLOOR`). Current-era
per-passage measurements: 問題10 157/241/334 (min/median/max, n=35), 問題11
507/655/763 (n=28) — author 問題10 passages to ~240 and 問題11 to ~650. An
official 短文 is *allowed* to be short; a generated one that is short is
usually thin rather than deliberate.

**The counting method, stated once** (three different figures for one paper
were in the repo at the same time): **JP characters only** — hiragana,
katakana, kanji and JP punctuation, the same character class
`check_dokkai_lengths()` uses — over **passage prose only** (instruction lines,
question stems and option rows removed; `（注N）` definition lines kept).
Digits, Latin and spaces are excluded. Never quote a length without naming this
method — a number quoted without it is not comparable.

**Author to the medians, not the floors.** Every floor sits below the official
minimum by design (the gate must never fail a real paper), so a paper that
merely clears the gate is still under-length against the band — a paper at the
medians clears both. Do not hit a floor by padding the note block
or the question stems: the gate measures the passage region (問題14's flyer
table and conditions do count). **問題14 is the one section where JP-char
counting misleads**: the flyer is dates, prices and times, so counted all-char
(JEES-style) it measures 676–793, median 707 — right on the published
700字程度 while looking ~25% short in JP chars.

**Calibrate to the era, not to a paper:** 問題11 became 4 passages × 2 items at
12/2022 and its length jumped with it, so the window is the 7 sittings
12/2022–12/2025 — never "the last five papers", which mixes eras. Band and
per-sitting figures: `references/official_calibration.md` §2.

## （中略）

Use `（中略）` when a quoted source would otherwise run long: official ships
**2–5 per paper in the current era, median 3, never zero**
(`official_calibration.md` §3); avoid shipping papers with zero `（中略）`. Cut at least one
passage across 問題11–13, and every `（中略）` must sit inside a 問題11–13
passage body — never floating under an instruction line (the gate checks
placement).

## 問題11 stems

All figures from `official_calibration.md` §4 — current era, n = 7 sittings,
28 pairs, 56 stems; where it disagrees with July 2025 alone, the archive wins.

- **Anchoring:** every stem is anchored either on **筆者** or on a **marked
  span** (「①…とあるが」/「〜とは何を指すか」). 82% name 筆者; **18% do not**
  and anchor on a span instead (0–3 per paper). Stem shapes must avoid unanchored
  pure-retrieval shapes.
- **Banned — the four pure-retrieval shapes:** 「本文で述べられている〜はどれか」
  「〜として正しいものはどれか」「〜の主な目的は何か」「〜の内容と合っているもの
  はどれか」. Corroborated at n = 15 sittings: **0 occurrences**, and not in
  問題10/12/13/14 either. `make check` FAILs on them.
- **Paper level: 問題11 carries at LEAST ONE 考え/主張 stem** — the official
  spread is 1–4 of the 8 (12/2023 and 12/2024 ship exactly 1; 7/2025 ships 4).
  Zero is the defect and the gate FAILs it. Author **2–3 among the eight** (the
  archive median), at most one per pair.
- **Pair level: the 事実把握 stem comes FIRST** — 26 of 28 official pairs (the
  two exceptions are the two 考え/考え pairs). The gate WARNs on an inverted
  pair — a style regularity, not an answerability defect.

**The old pairing rule is NOT a rule.** "One 事実把握 + one 考え/主張 per 問題11
pair" (and its earlier "exactly one of each" sharpening) is **not supported by
the official corpus**: over the 28 current-era pairs the split is **13
one-of-each, 13 two-事実, 2 two-考え**, and July 2025 is the ONLY sitting in the
entire 31-paper archive where all four pairs come out one-of-each — the rule
was calibrated to that outlier, and as a per-pair requirement it rejects 6 of
the 7 current official papers. It is not a requirement, and this file is where
that statement lives. (**問題13 is the regular one**: its item 69 is a
考え/主張 stem in **7 of 7** papers — treat that slot as mandatory.)

Classify each stem as you write it, by its SHAPE, not its intent — span
anchoring is tested FIRST, because
「売れた理由とあるが、筆者はなぜ売れたと考えているか」 is 事実把握 despite
containing 考えて:

- **事実把握** — anchored to a *specific* span, term, or sub-topic and
  answerable from the sentences around it: 「①…とあるが、どういうことか」/
  「…とあるが、筆者はなぜ…と考えているか」/「〜について、筆者はどのように述べて
  いるか」/「筆者によると、…とはどういうことか」.
- **考え/主張** — unanchored, answerable only from the passage as a whole:
  「筆者の考えに合うのはどれか」/「筆者が最も言いたいことは何か」/「〜について、
  筆者はどう考えているか」/「筆者が…として大切にしていることは何か」.

Write the eight labels down while drafting and count the 考え/主張 ones. If the
count is zero, rewrite the SECOND stem of one pair as an unanchored 考え
question — never re-label a stem to make the tally look right. The gate reads
*shape* only; a 筆者-anchored stem whose key is still a paraphrase of one
sentence needs a reader (`exam-qa-review` step 3).

## （注N） glosses

- **Pairing is 1-to-1 per passage, both directions:** every `（注N）` definition
  line annotates a word actually in that passage's body, and every in-body
  marker has a definition line. An orphan either way is an automatic QA fail,
  not a stylistic slip (e.g., unmarked glosses, orphan definition lines, or missing 注 definition lines).
- **Count in-body markers** — one per glossed term, in the passage region — not
  raw `（注N）` occurrences, which double-count because each gloss also has a
  definition line. (Count actual in-body markers, not definition lines.)
- **The two numbers:** the gate **WARNs below 25** in-body glosses
  (`GLOSS_MARKER_MIN` — a floor *below* every current official paper, which is
  what a floor should be). **Author to the official band, not the floor**:
  July 2025 = 30, current-era band 27–61 per paper, median 39 — target ~30–40.
  Additionally **≥3 in every 中文/長文 passage** (each of the four 問題11
  passages, and 問題13). A paper at exactly 25 markers stays green and is
  still below every current official paper.
- **Where the count is earned** — never write a per-問題 floor that touches
  問題12 or 問題14, which get **zero** glosses in every current-era paper:

  | | 問題10 | 問題11 | 問題12 | 問題13 | 問題14 |
  |---|---|---|---|---|---|
  | current-era range | 3–13 | 17–36 | **0** | 0–12 | **0** |
  | median | 6 | 24 | **0** | 7 | **0** |

  Per 問題11 passage: min 2, median 5.5, max 13 (26 of 28 carry ≥3). Plan ~5
  per 中文 and ~7 for the 長文 and the paper total takes care of itself; do not
  spread a quota across 問題10 to reach a number.
- **The count rule and the band rule are ONE rule — choose the notes while
  drafting the passage.** Avoid glossing basic or in-band N2 words just to increase the gloss count.
  Reaching the count with basic-word glosses (such as 割引・洗髪・契機・規制・革新・省力化・増幅) is worse
  than shipping a low count, because it degrades the passage. A 中文 on a
  specialized subject (ゾウの進化, 医療の個別性, 起業 — July 2025's own)
  naturally carries five domain terms; a passage written entirely in general
  vocabulary carries none and cannot be rescued by annotation afterwards. If a
  drafted passage yields fewer than 3 glossable terms under ✅ TARGETS, its
  subject is too plain for 中文 — deepen the subject, never gloss down to the
  floor.
- **STRICT vocabulary band for notes (non-negotiable):**
  - 🚫 **BANNED:** glossing N3–N5 words or standard N2 vocabulary (選択, 信号,
    技術, 文化, 質, 準備, 手順, 設計, 現象, 経由, 偏り, 維持, 継続, 前提, 細部,
    バランス) with trivial/circular definitions (`〜のこと`). The enumerated
    list is examples, not the boundary — no enumeration can close the class
    (it never covered 割引, 洗髪, 契機, 鑑賞, 評価制度, 省力化, and 4/4 papers
    shipped wrong-band glosses under it).
  - 🚫 **The operational test, not the list:** a term is glossable only if
    (1) it is genuinely above the N2 band — checked against Shin Kanzen Master
    N2-Goi/N2-Kanji and 日本語総まとめ N2 語彙/漢字 (`refs/Shinkanzen/`,
    `refs/Soumatome/`): if either book carries it as a headline N2 word, do not
    gloss it — and (2) the definition introduces words the term itself does
    not contain (「洗髪：髪の毛を洗うこと」 and 「割引：…金額を引くこと」 fail；
    「大脳辺縁系：…」 passes). **2026-08-11: the automated half of this check
    (an `openjlpt`-based band lookup) was removed along with `openjlpt`** —
    `make check` now WARNs on condition (2) only (the circular-definition
    half, which needs no corpus); condition (1) is a manual band judgment call
    for the author/reviewer, same as every other 問題1–6 vocabulary-band
    decision in this repo (`exam-qa-review` §2.5). **Both conditions are
    necessary, neither is sufficient** on its own — a term absent from
    Shinkanzen/Soumatome is not automatically over-level (準備, 技術, 選択 are
    plausibly absent from any one textbook's index and are still banned). A
    glossable term must ALSO fall in ✅ TARGETS, which is the positive
    requirement that decides.
  - ✅ **TARGETS** — `（注N）` glosses are strictly reserved for: N1-level or
    rare/literary words (委ねる, 雄弁, 死守する, 顧みる, 飼いならす, 抑圧,
    その場しのぎ); onomatopoeic/colloquial expressions (むきむきの);
    specialized/domain jargon (大脳辺縁系, 起業, 機動性); contextual/figurative
    metaphors (余白のあるメディア, 思い出の扉).
  - **Cross-check against this SAME paper's 問題1–6.** `20260811_1` glossed
    健やかさ in 問題11(4)'s （注3） while 健やか was, in the same paper,
    the correct-answer key of a 問題6 usage item — the paper itself proves the
    word is ordinary, testable N2 vocabulary, contradicting the gloss's own
    implicit claim that it needs explaining. Before finalizing any （注N）
    target, check it against every 問題1–6 stem/option/key already drawn for
    this test; a word tested elsewhere in the same paper as plain N2
    vocabulary can never also be a （注N） target here.
- **「ここでは」 is not the defect.** Official uses it freely in definition
  lines (July 2025 glosses 像を結ぶ as 「ここでは、姿がわかる」) — the ban is
  about glossing a *basic* word circularly, not about the phrase. A
  `make check` 「ここでは」 WARN on an over-level term is a false positive to
  state as such in your report, never a defect to edit away.
- Annotate in text strictly as `（注1）`, `（注2）`… (never `<ruby>`).
  Immediately after the passage (before its questions), the note block:
  `（注1）語彙：簡潔で自然な日本語の意味の説明` — one line per note.

## 問題14 (情報検索)

**70 and 71 are BOTH person-scenario items** — 7 of 7 current papers
(`official_calibration.md` §6). The correct answer always requires combining
**at least two** constraints from the table (topic + date/time, or a category +
a footnote exception; commonly 3: 7/2025-71 = 受付期間終了 + 開始3日前まで +
電話のみ; 12/2024-70 = room type + bath + 朝食付きプラン + Sunday rate). Never a
single-field lookup.

- **71 may never be 「このお知らせの内容と合っているものはどれか」** — a
  content-match question collapses to a one-cell lookup; the defect shipped in
  exactly that shape in t2/t3/t4, and not one official paper uses it. Write 71
  as a second applicant whose plan fails exactly one condition.
- The two official shapes to copy: a named person with 2–3 requirements → which
  option/course/room; a named person on a given date → what they must do to
  book, with a footnote exception deciding it.
- **The 解説 cells for 70 and 71 must each quote the TWO flyer cells the key
  combines** (`「カテゴリーB：…」＋「※…の場合は…」`) — one quote means one
  constraint. `make check` FAILs a 問題14 解説 cell with fewer than two
  distinct `「…」` spans that occur in the flyer text.
- Every constraint the QUESTION references (a role, category, condition) must
  be describable from the flyer/table text as printed — t3 asked how someone
  applies as 「補助スタッフ」 when the flyer described no staff/volunteer role
  at all.
- **Every WRONG option must contain at least one clause that is factually
  FALSE against the flyer** — not merely incomplete. `20260811_1` shipped a
  wrong option combining two clauses that were BOTH true (a photo count that
  really was sufficient, plus a document that really was required) — true-but-
  incomplete is a second defensible answer, since nothing in the option can be
  disproven. Build a wrong option by taking a true combination and changing
  ONE fact to something the flyer contradicts (a wrong photo count, a document
  the flyer does not require for this row, a fee/deadline that does not match),
  never by just leaving a requirement out.

## 読解 keys — paraphrase, and keep the four lengths close

**Paraphrase every 読解 key to option length (~25–40 JP chars) and keep the
four options close in length**, or the key is findable by string length alone —
without reading the passage (t3 shipped items 67/68/69 as consecutive keys of
91/101/61 chars, lifted verbatim, beside ~31–34 char distractors; t4 item 66 at
55 vs 31). "Within ±40% of each other" is a target, not an invariant: over 140
current-era items, 95% satisfy **max/min ≤ 1.8** — author to that — but
official ships 2.10 (12/2025-66) and 2.09 (12/2023-65). Two consequences the
older wording got wrong: an item at 1.9 is not automatically a defect, and the
key being the longest of the four is not either (29% of official keys are).
**The defect is a key that is long AND a verbatim span of the passage** — that
turns 主張理解 into string matching. `make check` FAILs a keyed 読解 option
(52–71) that is ≥50 JP chars, present verbatim in the passage, **and** ≥1.7×
the mean of the other three — against 138 official keyed options the longest is
61 chars and the highest ratio 1.55, so no official item trips the pair. That
gate constant survives the archive; keep it.
