# 読解 (問題10–14) — construction rules

Section reference for the `question-authoring` skill. Read the core
`SKILL.md` alongside this file — it carries the N2-band rule, distractor
discipline, item integrity, and key-cell artifacts. This file adds the
問題10–14-specific rules and owns the repo's single copy of the 読解
length-band table.

## What a 読解 section is

Difficulty lives in the QUESTIONS, not the vocabulary: ask 筆者の考え/
一番言いたいこと/どういうことか, never mere fact lookup.

**Reference Authority**:
- Primary measuring stick: the 31-sitting official past exam archive in `refs/JLPT_N2_NEW/` (specifically the 7 current-era sittings 12/2022–12/2025 for all counts, lengths, and bands).
- Secondary structural/discourse authority: `refs/Shinkanzen/dokkai_reference.md` (`Shin_Kanzen_Masuta_N2-Dokkai.pdf`).
  - **Five discourse devices (第1部-1 文章のしくみを理解する)**: 1) 対比 2) 言い換え 3) 比喩 4) 疑問提示文 5) 主張表現.
  - **Five question types (第1部-2 問いを解く技術を身につける)**: 1) 指示語 2) だれが・何が・何を 3) 下線部の意味 4) 理由 5) 例.
  - **Four 情報検索 source types (第2部)**: 広告 / お知らせ / 説明書き / 表・リスト.
  *(Secondary evidence: corroborates register, structure, and question taxonomy; never sets length or counts.)*

Passage inventory per paper:
- Diverse essay types (opinions with a turn, explanatory essays, reflective memoirs),
- One business email,
- One notice/announcement (exceptions in natural prose, ※ symbol capped at ≤3 per paper),
- One A/B pair (agree on one common observation, differ on conclusion/advice),
- One flyer/table with condition matching where distractor options fail specific conditions.

**NO FURIGANA in 読解** — passages (問題9–14), stems, and options carry no
`<ruby>`; over-level/rare/domain words are glossed only via `（注N）` (below).

## Thirteen surfaces, thirteen different essays — subject, closing move, AND voice

The 読解 half is 13 surfaces (問題9 cloze + 問題10×5 + 問題11×4 + 問題12 +
問題13 + 問題14). They must differ on **four** axes: subject/theme, closing
move, voice/register, and — added 2026-08-24 — the claim and the narrator.

### The denominator — settled here, stated nowhere else

**Three axes, three different denominators.** They are not the same number,
and this table is the single copy. The 2026-08-19 gate change split 問題12 for
the closing axis and nobody updated this file, so for five days the prose
reserved the shapes for "the twelve essay-type surfaces … each capped at
exactly 2" while `check_dokkai_final_sentence_templates` measured **thirteen**
closings with A and B separate — a paper could satisfy one reading or the
other, never both, and 20260821_1 shipped 条件提示 ×3 that was compliant under
the prose and a breach under the gate (qa-report-20260821_1-round2 NF-2).

| axis | denominator | rows | 問題12 | 問題14 |
|---|---|---|---|---|
| 1 — subject/theme | **13 theme rows** | 問題9 + 問題10×5 + 問題11×4 + 問題12 + 問題13 + 問題14 | **ONE** row — A and B are one passage pair on one subject | counted |
| 2 — closing move AND final-sentence template | **13 closings** | 問題9 + 問題10×5 + 問題11×4 + 問題12(A) + 問題12(B) + 問題13 | **TWO** rows — two essays, two closings, printed side by side, which is the one place a shape is most likely to rhyme | **outside** the taxonomy — a flyer has no authorial closing move |
| 3 — voice & register quotas | **12 passages** | 問9, 問10×5, 問11×4, 問12, 問13 | **ONE** passage (one （注N） scope) | outside |

**問題12 A and B are TWO closings and TWO template rows, and ONE theme row.
The ≤2-per-shape cap and the ≤2-per-template cap are counted over the
THIRTEEN closings of axis 2.** `dokkai_closing_scopes()` in
`check_consistency.py` is that enumeration in code, and every closing-scope
check reads it, so the number cannot drift apart from this table again.
(`check_dokkai_closing_reframe`, the whole-passage anti-dodge net, still
enumerates the 12 （注N） scopes with 問題12 joint — deliberately: "does this
passage CONTAIN the marker anywhere" is a passage-level question, not a
closing count. Its own docstring says so.)

**Arithmetic consequence, which replaces the old 問題14 carve-out:** 6 shapes ×
cap 2 = 12 < 13, so **at least one of the thirteen closings must sit OUTSIDE
the taxonomy** rather than force a third instance into any shape. 問題14 can no
longer be that surface — it is already outside axis 2. The carve-out surfaces
are 問題10's 実用文 members: a business email, a notice or an 案内 ends on an
instruction to the reader, not on an authorial move, so label it
**実用文・分類外** and do not spend a shape slot on it. 20260821_1 runs two
(問題10(3) email, 問題10(4) notice), leaving 11 taxonomy closings for 12 slots.

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

**Only the UPPER side of 5–9 is enforced, and that is deliberate** (stated
2026-09-03, `RC-D`). The 5–9 figure is the official *range*; the gate has one
threshold, `RHETORIC_CEILING = 12`, and no floor, because the failure mode this
axis exists to catch is **one closing family swallowing the paper** — the
generated 23–33 above, `20260810_1`'s nine-of-ten. **A total below 5 is not a
defect.** Variety is verified by the per-shape cap below — no more than 2 of
the 13 surfaces sharing one closing move — not by the marker total: a paper can
reach 13 distinct closings while using few of this family's markers at all,
and a paper can sit inside 5–9 with six surfaces on one shape. The case that
exposed the gap: `20260903_1` measured **3** and read as out-of-band with
nothing to say whether that mattered, while its independent per-shape read was
13 finals over 7 shapes, none over the cap
(`qa-report-20260903_1.md` handed item #7(b)). If you are at 3, check the shape
column, not the marker count.

**How to comply while drafting** — write each passage's closing move beside
its theme, and vary the list. No more than **two** passages may share one
shape:

- 主張 — 「AだけではB、Cこそが」 (the move above; ≤2 per paper, not 9)
- 説明 — explains a mechanism/distinction and stops there
- 意外な観察 — an unexpected fact, then its cause (「意外にも〜。理由は〜」)
- 反論応答 — 「〜という批判もあるが、実際には〜」
- 随筆 — a personal observation that generalises without prescribing
- 条件提示 — a concrete, checkable condition (「〜した自治体ほど〜」), no exhortation.
  **This shape has ONE natural skeleton and it collides with itself**: an
  evidential frame + a [V-た + group/period] では／ほど + a quantity going up or
  down (`A では/ほど B が多い（相関）`). Two 条件提示 closings will land on it
  unless you deliberately vary one — see the template list below.

**The ≤2-per-shape cap is not enough alone — the two sharing a shape must
also differ at the SENTENCE-TEMPLATE level**, not swap content words into
the same skeleton. `20260817_2` shipped three such pairs (same closing
sentence pattern, different content) that passed both the shape cap and the
marker scan, since both classify by CATEGORY, not literal skeleton — if two
passages assigned the same shape share a template, rewrite one to a
structurally different pattern for that shape before finalizing.

**Do it as a column, not as a judgement: write the thirteen FINAL SENTENCES
out in one column before finalising and read them down the column.** The
shape label is not the check — the sentence is. `20260817_3` labelled its
thirteen surfaces across six shapes, ≤2 each, every label defensible, and
still shipped **five** finals on one skeleton (「〜のは、A そのものではなく B
だ」 — 問題9, 問題10(3), 問題10(4), 問題11(1), 問題13), three of them on the
same 「〜そのもの…ではなく」 sub-skeleton, because nobody put the sentences side
by side. Normalise each final to its template as you write it down, and
rewrite until **no template appears more than twice** — regardless of what
the shape labels say. Keep the column; it is the artifact QA re-reads.

The named templates, which are exactly what `FINAL_SENTENCE_TEMPLATES` counts
(`check_dokkai_final_sentence_templates`) — a template with no name here is a
class QA cannot report and a fix cannot be asked for:

| template | skeleton |
|---|---|
| `〜のは、A ではなく B だ` | 「（では｜じゃ）なく」 |
| `A より B のほうが〜` | 「より（も｜は）…ほう／方が」 |
| `A だけではない。B こそが〜` | 「だけで（は｜も）ない／なく」・「こそが」 |
| `A というより B` | 「というより」 |
| `A わけではない` | 「わけでは（ない｜ありません）」 |
| `A では/ほど B が多い（相関）` | evidential frame + [V-た + 集団/期間] では／ほど + 数量の増減 |

The last row was added 2026-08-24 (qa-report-20260821_1-round2 NF-2): it is
where 条件提示 closings pile up by construction, it had no name, and so a paper
shipped 問題11(1) 「…力を入れた**店では**、星の平均が**高くなる**一方で、…**開きが
大きくなっていた**」 beside 問題12(A) 「…間を置いた**会ほど**、…発言した**人の数が
多い**」 — same skeleton, different content words, both labelled 条件提示, and
both invisible to every check and to the reviewer's own vocabulary.

**Build the column BEFORE writing the passages, not after** (`20260821_1` F3,
2026-08-24). That paper shipped **6 of 11** essay surfaces on the not-A-but-B
reframe — 問題9「のではなく…こそが」, 問題10(2)「というより」, 問題11(2)「だけでは
…こそが要る」, 問題11(3)「よりも…なのです」, 問題11(4)「わけではない」,
問題13「というより」 — while `check_dokkai_closing_reframe` reported **1
matched**, because its marker family had no 「というより」/「よりも」/「わけでは
ない」 alternative at all. The tokens are now counted (`REFRAME_CLOSING`,
`FINAL_SENTENCE_TEMPLATES`), but the gate is still only a proxy: the
authoring-time procedure is to write all thirteen rows — **surface | theme |
shape label | final-sentence template** — as the FIRST 読解 step, before any
passage prose exists, and to reject any plan where one shape label or one
template appears three times. Every not-A-but-B family member counts as one
shape: 「AではなくB」「AというよりB」「AよりもB」「AだけではなくB」
「Aわけではない」 are the same move in five surfaces of grammar.

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

**Thirteen closings do not force thirteen instances of the six shapes.** 6
shapes × cap 2 = 12 < 13, so at least one closing must sit OUTSIDE this
taxonomy rather than forcing a 3rd instance into any shape. See §"The
denominator" above for which: 問題14 is outside axis 2 already (a flyer has no
authorial voice, argument, or closing move in this narrative sense), so the
carve-out is taken by 問題10's 実用文 members (email / notice / 案内 —
label them 実用文・分類外). The six shapes are then spent on the remaining
essay-type closings among the thirteen of axis 2, each capped at exactly 2.

**The answerability consequence, which is the real damage.** When nine
passages close the same way, their keys close the same way too —
`20260810_1`'s 52/54/56/58/60/62/64/69 were all the "human/attitude" option
beside three 「Xさえすれば十分」 strawmen, so a test-taker keys eight items by
picking the soft-sounding option without reading a single passage.
Distractor sets must vary in kind across the section; a section whose wrong
options are uniformly overstatements is strategy-solvable regardless of how
well each item reads alone.

**Axis 3 — Voice & Register (the voice quota).**
Official 読解 passages are excerpts from published essays and books (first-person, half addressed to the reader in です・ます, with quoted speech and rhetorical devices). A compliant paper must avoid uniform impersonal policy prose:
- **First-person quota**: ≥4 of the 12 essay-type surfaces (問9, 問10×5, 問11×4, 問12, 問13) are written in the first person (containing 私/僕/自分).
- **Polite voice quota**: ≥3 passages carry です・ます sentence endings throughout.
- **Kanji density**: 24–32% JP chars across the paper's reading prose (FAIL outside 22–34%).
- **Rhetorical & discourse devices**:
  - ≥1 passage carrying quoted dialogue/speech 「…」
  - ≥1 passage carrying a 疑問提示文 (Shin Kanzen discourse device 4: 「〜のだろうか」「〜だろう」)
- **※ (asterisk) symbol count**: ≤3 in the entire paper across 問題10–14 (archive 0–3, median 0).

**Axis 4 — the CLAIM and the NARRATOR, recorded not measured** (added
2026-08-24). Axes 1–3 count what a surface is about, how it closes, and in
what register. None of them can see **what it asserts** or **who is
asserting it**, and that is where the collisions now land: `20260821_1` ran
問題9 and 問題13 as the same narrator — first-person, multi-year, solitary
physical practice, rejecting the naive explanation of why the author keeps at
it — with different themes (スポーツ・余暇 / 科学・技術) and different shape labels
(反論応答 / 意外な観察) hiding it in every column that existed. Record, in
`logs/topics.json` (see `exam-blueprint` §"`logs/topics.json`"), a **`claim`**
sentence per surface and a **`persona`** token per 読解 surface
(趣味の実践者 / 職業人 / 親 / 観察者 / 研究者 …), **capped at 2** like the closing
shapes, and read the claim column down before finalising.
`check_topics_claim_field()` enforces presence and the cap from the first
paper generated after adoption; it cannot judge whether two claims are the
same move, which is the read you still owe.

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

## Length bands & Sentence rhythm — the single copy in this repo

These numbers once lived in three files at once, hand-synced, and 4/4
generated papers shipped 問題11/問題14 under band while every gate stayed
green. Stated **here and nowhere else** — `jlpt-exam-structure` points at
this table, and `check_dokkai_lengths()` enforces the two-sided bounds.

| Section | official min | official median | official max | gate floor | gate ceiling |
|---|---|---|---|---|---|
| 問題10 短文 (5 passages) | 1143 | 1225 | 1329 | **≥1100** | **≤1330** |
| 問題11 中文 (4 passages) | 2449 | 2556 | 2685 | **≥2250** | **≤2700** |
| 問題12 A/B | 532 | 551 | 592 | **≥510** | **≤600** |
| 問題13 長文 | 814 | 904 | 1061 | **≥800** | **≤1070** |
| 問題14 情報検索 | 489 | 604 | 638 | **≥450** | **≤640** |

Per-passage bounds: each 問題10 passage 150–350 JP chars (ceiling 350; archive max 334), each 問題11 passage
≥400 (`DOKKAI_PASSAGE_FLOOR`). Current-era per-passage measurements: 問題10
157/241/334 (min/med/max, n=35), 問題11 507/655/763 (n=28) — author 問題10 to
~240, 問題11 to ~650. An official 短文 is *allowed* to be short; a generated
one that's short is usually thin, not deliberate.

**Option length band**: mean option length per paper **24–30** JP chars across all 20 items (official current era 26.3 JP chars).

### Sentence rhythm

Sentence rhythm in N2 essays is remarkably stable across official sittings:
- **Median sentence length per paper**: **33–43** JP chars (FAIL outside 28–50).
- **Share of sentences under 25 chars**: **12–30%** (official current-era band 14–27%, median 20.5%).

**Counting method, stated once**: JP characters only (hiragana/katakana/
kanji/JP punctuation, same class `check_dokkai_lengths()` uses) over
**passage prose only** (instructions/stems/options removed; `（注N）`
definitions kept). Digits/Latin/spaces excluded. Never quote a length
without naming this method.

**Author to the medians, not the floors or ceilings** — every floor sits below the
official minimum and every ceiling sits above the official maximum by design.
Don't pad the note block or stems to hit a floor — the gate measures the passage region
(問題14's table/conditions count). **問題14 misleads in JP chars**: counted all-char it measures
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

## Marked-span quoting & retrieval shapes

- **Span rate**: **≤2 span-anchored stems per paper** across 問題10–13 (current-era official median is 0, range 0–3; 4 of 7 sittings have 0). Do not over-anchor.
- **指示語 floor**: **≥1 指示語 item per paper** (Shin Kanzen 第1部-2 question type 1; official current era 1.57/paper, e.g. 「それ/これとは何を指すか」「どういうことか」).
- **Default retrieval shape**: **「筆者によると、〜は何か」** is the primary anchored retrieval frame (~25–29% of official 問題11/13 stems).

**Rule (every span-anchored stem):** whenever a stem anchors on a specific span
via `「…」とあるが` — a quoted clause, sentence, or defined term — that EXACT
span must be marked in the passage body with a circled-number marker AND
bolded, `①**span**`, and the stem must reference it identically,
`①**span**とあるが`. Never leave either side as a bare `「quoted text」とあるが`
with no marker/bold. `check_dokkai_span_anchor_bold` FAILs the bare-quote shape.

### The two sides must be the SAME characters

**BINDING: the bolded span in the passage and the span quoted in the stem
are character-identical.** Not "the same idea", not "the stem's span inside
the passage's span" — the same string.
`check_dokkai_span_anchor_identity` FAILs a mismatch.

**Repair direction is fixed: shorten the PASSAGE bold to the stem's span,
never lengthen the stem to the passage's.**

**A （注N） gloss never sits inside the bold**, wherever the glossed word
falls in the span — `①**重ね合わせ**（注2）`, never `①**重ね合わせ（注2）**`.
`check_dokkai_span_anchor_identity` FAILs a gloss inside bold.

### Length band — the span is a pointer, not a highlighter

Measured over official sittings:
- Median **8** JP chars (current-era band).
- **WARN above 25** JP chars.
- **FAIL above 35** JP chars.

**Author to the median, ~8–15 chars** — a phrase, not a sentence.

## 問題10 stems & apparatus

問題10 comprises 5 short passages (52–56), including one business email and one notice/document:
- **考え/主張 mix**: **≥2 of the 5 items** belong to the 筆者の考え family (「筆者の考えに合うのはどれか」「筆者はどのように考えているか」; official share ~46%).
- **Apparatus stems ask INTENT, not content**: for notices, emails, and announcements, stems must ask what the document is FOR (「このお知らせで伝えたいことは何か」「このメールで問い合わせていることは何か」「このメールの用件は何か」; 8 of 10 official apparatus items). Asking mere content lookup turns notices into lookup traps.

## 問題11 stems & Banned retrieval shapes

All figures from `official_calibration.md` §4 — current era, n=7 sittings,
28 pairs, 56 stems:

- **Anchoring:** every stem is anchored on **筆者**, a **marked span** (「①…とあるが」), or a **demonstrative/topic** (「筆者によると」). 82% name 筆者; 18% anchor on a span instead.
- **Banned across 問題10–14 — four pure-retrieval shapes + bare truth-checks:**
  1. 「本文で述べられている〜はどれか」
  2. 「〜として正しいものはどれか」
  3. 「〜の主な目的は何か」
  4. 「〜の内容と合っているものはどれか」
  5. Bare 「正しいものはどれか」「適切なものはどれか」
  *(0 occurrences across 15 sittings in any 大問; `check_dokkai_banned_stems` FAILs them).*
- **Paper level: 問題11 carries at LEAST ONE 考え/主張 stem** — official spread 1–4 of 8. Author 2–3 of the eight.
- **Pair level: the 事実把握 stem comes FIRST** — 26 of 28 official pairs.
- **問題13 IS regular**: item 69 is a 考え/主張 stem in 7 of 7 papers.

## （注N） glosses

- **Pairing is 1-to-1 per passage, both directions** — every definition line annotates a word actually in that passage's body, and every in-body marker has a definition line.
- **Count in-body markers**: gate WARNs below 25 in-body glosses (`GLOSS_MARKER_MIN`). **Author to the band**: current-era band 27–61/paper, median 39, target ~30–40.
- **Where the count is earned**: 問題11 (~5 per passage) and 問題13 (~7). **問題12 and 問題14 get 0** in every current-era paper.
- **STRICT vocabulary band**:
  - 🚫 **BANNED**: glossing standard N2 or easier vocabulary (選択, 信号, 技術, 準備, 手順, 維持, 継続, 前提, バランス…) with circular definitions.
  - 🚫 **Operational subtraction test**: delete from the definition every character that appears in the headword; what remains must still explain the concept.
  - ✅ **TARGETS**: N1-level/rare words, specialized domain jargon, contextual metaphors.
  - **No answer leaks**: a gloss must not give away the answer to a question anchored on it.

## 問題14 (情報検索)

**70 and 71 are BOTH person-scenario items** — 7 of 7 papers (`official_calibration.md` §6). The answer always combines **≥2** constraints from the table.

- **Target shape**: stems must ask for a **value** (料金はいくらになるか / 何を用意
  すべきか / 何を持って行かなければならないか), an **action** (どのように申し込むか /
  どうしなければならないか / どうすれば参加できるか), or a **choice** among named
  options (どの講座か / 希望に合うコースはどれか). Measured over all 14 official
  current-era items: **5 value, 6 action, 3 choice, 0 truth-check** — the
  classifier behind that count is `dokkai_profile.classify_q14_target` and it now
  covers 14 of 14, so a stem it calls `other` is a shape the archive does not use.
- **🚫 BANNED**: stems asking generic truth checks (「〜について、正しいものはどれか」
  「〜について、適切なのはどれか」). `check_dokkai_q14_stem_target` **FAILs when both
  items are truth-check shaped** and WARNs on one; the papers still exempt are
  `20260812_1`, `20260812_2`, `20260813_2`, `20260814_1`, `20260817_1`,
  `20260817_2` (`DOKKAI_Q14_TARGET_GRANDFATHERED`), and an id leaves that set the
  moment its two stems ask a value, an action or a named option — as
  `20260817_3`, `20260818_1` and `20260819_1` did on 2026-08-21.
- **A worked pair, from the repair of `20260819_1`:** 「川口さんが払う金額は、全部で
  いくらになるか」 with options 六百円 / 八百円 / 千円 / 千四百円 — each distractor a
  real combination of flyer cells with one fact changed (the student rate alone,
  the one-day rate mistaken for it, the museum's own admission added on top of a
  ticket that already covers it) — and 「日曜日にどの施設を回っておかなければならな
  いか」, keyed on the two 休館日 cells that read 月曜日. Neither asks whether a
  sentence is true; both make the candidate compute something.
- **The 解説 cells for 70/71 must each quote the TWO flyer cells the key combines**.
- **Every WRONG option must contain at least one clause factually FALSE against the flyer** — not merely incomplete. Build wrong options from true combinations with ONE fact changed to something the flyer contradicts.

## 読解 keys — unpredictable option lengths, rank spread, and strict paraphrasing

### 1. Option length balance & rank distribution

1. **Per-item length ratio**, 問題10–13 only — every number re-measured
   2026-08-21 with `make dokkai-profile BASELINE=1` §3 after repairing that
   script's option parser (it had been cutting option 4 at its first line and
   reading 「3,500円」 as one character, which manufactured ratios of 9–14 out of
   nothing):
   - **WARN if max/min > 1.65** — official 問題10–13 runs median 1.25, p90 1.55,
     **max 2.00** over 126 items.
   - **FAIL if max/min > 2.50** — outside that whole range, as a threshold must be.
   - **問題14 is exempt.** Its options are values and dates by design: official
     12/2023 問70 prints 「3,500円」 beside 「3,500円から200円と300円が割引された
     金額」 (4.17×), and 問題14's own range is 1.26–4.17. One threshold cannot
     serve both, and the old FAIL line was rejecting a shape the archive ships
     every sitting.
   - Length here is **printed length** (every non-space character), not JP-only —
     name the metric wherever this number is quoted.
   - The ≤1.30 clamp this replaced failed **34.3% of official current-era items**
     (the audit reported 40.5% from a parse whose truncations inflated it), and it
     is what pushed 48.8% of our keys onto rank 2 (§F2).
2. **Per-paper key rank spread**:
   - **No single key rank (1=longest, 2, 3, 4=shortest) may exceed 60% of items** (`check_dokkai_key_rank_spread` FAILs >60%, WARNs >45%). Official per-paper worst is 56%, median 39%.
   - **Uniquely longest rate**: key is uniquely longest in **20–30%** of items (official median 23.0%).
3. **Repair direction**: adjust ranks by **lengthening distractors with genuine, passage-groundable clauses** (conditions, consequences, qualifications). Do NOT shorten keys — shortening is how paraphrases collapse into verbatim lifts.

### 2. Overlap direction — keys must share LESS surface with the passage than distractors

Examinees must not be able to solve items by simple character matching:
1. **Overlap Margin**: the paper's median (key overlap − best distractor overlap) bigram margin must be **≤ 0.0** (negative in 7 of 7 official papers: −0.021 to −0.100).
2. **Top overlap share**: the key may be strictly top in passage bigram overlap
   in **≤50%** of items (WARN above **46%**; official range 10–45%, median 35%,
   re-measured 2026-08-21 — the WARN sat at 44% until one official sitting
   measured 45.0% under the repaired parser).
3. **Distractor construction**: build wrong options FROM passage material (a true clause with one fact altered) and write the key as an abstract paraphrase. This ensures distractors are attractive and share high surface overlap with the passage, while the key tests comprehension of the idea.

### 3. Strict key paraphrasing — keys must NEVER be verbatim text lifts

**BINDING: every key in 問題10–13 (52–69) must be genuinely paraphrased.**
1. No verbatim lifts: an LCS against the passage ≥15 JP chars AND ≥50% of the key length is a FAIL (`check_verbatim_keys`); ≥20 chars is an automatic FAIL; ≥85% verbatim on a short key is an automatic FAIL.
2. Rephrase the author's logic with synonyms, abstract summaries, or grammatical restructuring.

### 4. Stems quoting marked spans

A key must never be answerable purely from the stem's own quoted span. When
a stem anchors on `①**quoted clause**とあるが`, the key must require
synthesizing something OUTSIDE that clause — never restate the clause with a
synonym swapped in.
