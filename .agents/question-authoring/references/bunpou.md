# 文法 (問題7–9) — construction rules

Section reference for the `question-authoring` skill. Read the core
`SKILL.md` alongside this file — it carries the N2-band rule, distractor
discipline, and item integrity (問題8 assembly/★-position/glue/uniqueness
link-table rules are Item integrity #4–8 there). This file adds the
問題7–9-specific rules and benchmark lengths, measured on
`refs/JLPT_N2_NEW/` (per-sitting figures: `official_calibration.md` §7).

## Inventory — N2-list items only

Only Shin Kanzen N2 文法 headed forms: 〜かねない, 〜ざるを得ない,
〜わけにはいかない, 〜に先立って, 〜を契機に, 〜つつも, 〜ようがない,
〜に限って, 〜ものの, 〜ばかりに, 〜たところ, humble/honorific traps (伺う;
include one FAKE form like 参られます as a distractor). Pool draws come from
`exam-blueprint` — never invent a form outside that inventory.

- **BANNED too easy (N3–N5):** 〜によると, 〜ば〜ほど, 〜がち alone,
  お〜ください, 〜てください, 〜ほうがいい, 〜ことができる, 〜たいです,
  〜前に/〜後で as the sole point — full list:
  `references/level_band_grammar.txt` `## TOO_EASY`.
- **BANNED too hard (N1):** 〜にあって, 〜をもって, 〜ともなると, 〜までもなく
  (except the set phrase 言うまでもなく as running text, not a productive
  key), 〜を皮切りに, 〜がてら/〜かたわら as keys, 〜ずにはおかない,
  〜余儀なくされる as the tested form — `## TOO_HARD` in the same file.
- **One grammar point may be the KEY only once per paper**, and a tested
  form stays out of the reading passages — core Item integrity #15.

## 問題7 — stem length is a DISTRIBUTION, not a floor

Official stems average **~43 JP chars** (median ~41; interquartile ~33–54),
and — the part that matters — they are **spread**: 7/2025 runs 26…74
(mean 40.8, range 48), 12/2025 opens 23…65. About 21% of official stems sit
under 30 chars (`official_calibration.md` §9). A set written to one length
reads as one authorial voice, however idiomatic each sentence is.

**Three binding numbers, all measured over the 12 stems, JP chars only:**

| | bar |
|---|---|
| 12-stem mean | inside **36–52** |
| stems under **34** JP chars | **at least 2** |
| max − min | **at least 25** |

Until 2026-08-19 this rule was written in the low direction only ("average
≥40, each stem ≥30"), so twelve papers optimised the floor and **every one
of the 12 on disk shipped ZERO stems under 30 chars** (means 47.7–57.4);
`20260817_3` shipped mean 52.8, min 46, range 12 — twelve two-clause
narrative sentences, one template. Nothing pushed back because nothing was
written in the high direction.

**Construction instruction — write the two SHORT stems FIRST.** Before any
of the other ten: pick two grammar points whose form is testable with no
scene at all, and write those stems at **25–34 chars, no background clause**
(official: 「今度の旅行、費用は一人三万円(　)。」). Then write the long ones
around them. A rule you can only verify after writing all twelve gets
skipped — this one is verifiable when two sentences exist.

Repairing a set that came out flat means **compressing** stems (drop the
background clause), never lengthening the rest: lengthening moves the mean
the wrong way and leaves the range unchanged.

### One form, one item — the fourth binding number

**No grammar form may appear in more than ONE item's option set across
問題7.** Measured over the six current-era sittings (7/2023–12/2025), no
5-kana grammar n-gram occurs in two 問題7 option lines. A form printed three
times as a wrong option is eliminable on sight by its third appearance: the
examinee stops reading the stem and starts reading the paper's habits.

`20260819_1` printed 「どころではない」 as a wrong option in **3 of 12** items
(問33, 問38, 問41) and never as a key (F2). Recurrence over the 14 papers on
disk: **11 exceed the official maximum of 1**, three exceed 2
(`20260814_1` 「わけではない」×4, `20260810_1` 「にひきかえ」×3, `20260819_1`×3).

`check_mondai7_option_form_reuse()` enforces it, and it enforces it in two
steps on purpose: it ships at **more than 2** — the count that fires on
exactly the three worst papers — and **tightens to more than 1**, the
official maximum, once those are repaired. Both numbers are constants at the
top of that check; read them there, not here. Repair by replacing the surplus
distractors with real N2 forms that are impossible for a nameable reason, and
rewriting the 解説 cells that argue them — never by shortening the form so
the n-gram stops matching.

Build length with scene-setting (職場・電話・掲示・インタビュー), a
subordinate clause, or a short dialogue lead-in — never by padding the
tested form. Official items often open with `(会社で)`/`(電話で)`/a named
role. Lengthen the *situation*: 「このまま働きすぎると、体を壊し(　)よ。」
fails the band even with the correct key かねない; rewrite toward
「最近残業が続き休日もほとんど取れない。このまま働きすぎると、体を壊し(　)よ。」
(scene + consequence). Same rule for 問題8 frames and 問題9 cloze prose.

**Shape:** every official paper includes several 問題7 items with dialogue
turns or a setting label (`（会社で）`/`（電話で）`/`（インタビューで）`/
homepage notice). Include at least 2 (prefer 2–4) of the 12 (`make check`
WARNs on a set with none).

**Dialogue/setting Markdown layout** — do NOT crush the stem onto one line.
Official booklets put the place label first, then each speaker on its own line:

```
**40** （会社で）
A「どうしたの。」
B「経験がないのに引き受けた(　)、大変な目にあってしまったよ。」
 1. どころか  2. ばかりに  3. ながらに  4. おきに
```

Rules: (1) `（会社で）` alone on the stem's first line after `**N**`; (2)
each speaker turn on its own following line; (3) the option row still on
ONE line under the turns. Collapsing to `**40** （会社で）A「…」B「…」` is
forbidden — reads as a drill line. The sheet builder keeps its question
context across those stem lines, so radios still attach — don't "fix" a
sheet by flattening the dialogue (`exam-app`).

## 問題8 (文の組み立て) — length is mostly in the OPTIONS

Measured on `refs/JLPT_N2_NEW/` + the official 2018 sample + July 2025:

- **Sum of the four options**: typically 16–29 JP chars.
- **Per option:** a mix is fine (a particle next to a clause), but ≥2
  options ≥5 JP chars and the longest usually ≥7 — four 2–4 char scraps
  read as drill chunks, not N2 scramble chunks.
- **Assembled sentence** (stem frame + four options) ≥45 JP chars, prefer
  ~50–75. Fund the length with stem context when the options alone can't.
- Prefer nested/phrase chunks (複文フレーム) over isolated particles when
  the grammar point allows.

**Treat all of the above as authoring targets, not rejection grounds.**
`official_calibration.md` §9 measured the gate's three 問題8 constants
against the archive and they reject 20%/38%/34% of official items
(`P8_OPT_SUM_MIN` 16 vs an official band of 9–41; `P8_LONG_OPTS_MIN` 2 vs
0–4; `P8_ASSEMBLED_MIN` 45 vs 30–78) — 51% of official options are under 5
chars, and a bare adverb/particle on a card is official practice. Chunk-size
intuitions don't survive contact with the archive — **the invariant is
★-uniqueness** (Item integrity #8, the link table); length is calibration only.

### At most ONE card may be a FREELY-ORDERABLE PRE-PREDICATE UNIT

This is a CONSTRUCTION rule, checked before any proof is written — it decides
whether the item can be made unique at all.

**A pre-predicate unit is free when nothing structural fixes where it sits.**
Japanese does not order the material in front of a predicate: 「〜を〜に基づいて
決める」 and 「〜に基づいて〜を決める」 are both ordinary, SOV and OSV are both
ordinary, and — the half the old wording missed — **an adjunct CLAUSE scrambles
against an object exactly as freely as a second argument would.** So if two
cards (or two card BLOCKS) both sit in front of the final predicate and neither
is pinned by one of the four sources below, the item has TWO ★ answers whatever
the 解説 says. That is an item defect, not a proof defect.

**The rule, as it must be counted:**

> 最終述語の前に来るカード（塊）のうち、位置が構造的に固定されていないものは1つまで。
> 共項か付加詞かは問わない——条件節・時の節・理由節など、述語に係る従属節も
> 「自由な単位」に数える。位置を固定できる源は (1) 連体修飾の主要部、(2) 引用の
> 「と」、(3) 下位範疇化された助詞（形式名詞の連体修飾スロットを含む）、(4) 半分ずつを
> 語彙的に順序づける呼応テンプレート の四つだけであり、「重い前置きが三つ並ぶと崩れる」
> のような処理負荷・自然さの議論は根拠にならない。自由な単位が二つ残るなら、片方を
> 下線の前の文中へ移すか、主要部が隣接を強制するカードに差し替えて切り直す。

**Why the rename — the worked example this wording exists for.** From
2026-08-19 to 2026-08-20 this section read *"at most ONE card may be a free
**co-argument** of the final predicate"*, and it measured the wrong quantity.
`20260819_1` 問題8-45 shipped as `申請書に不備が / あった場合は / 受け付けを /
断らねばならない`: exactly ONE free co-argument (「受け付けを」), so the rule
passed it — while 「申請書に不備があった場合は」, a は-marked conditional ADJUNCT
clause, was a second freely-orderable unit sitting in front of the same
predicate. The rival `受け付けを → 申請書に不備が → あった場合は →
断らねばならない` is grammatical and keys ★=2 instead of ★=4, and the shipped
解説 excluded it only with a heaviness/topic-position argument — *「前置きの句が
三つ並ぶと崩れる」* — which is precisely the kind of reason the block above
refuses. **This is the same structural shape round 2 declared fatal for 43 and
47 and then exempted for 45 ad hoc** (`qa-report-20260819_1-round3` R3-S1). The
item was re-cut on 2026-08-20; see the repair paragraph below.

**Legal adjacency comes from four sources, and never from transitivity:**

1. a **連体修飾 head** — the modifying clause's own arguments cannot leave it
   (`20260819_1` 問題8-44: 「あの技術を→受け継ぐ人が」);
2. a **quotative 「と」** — 「〜と+言う/思う/自慢している」;
3. a **subcategorised particle** — 「に→基づいて」, 「に→限らず」, a 形式名詞's
   連体修飾 slot (「体を壊した→ときほど」);
4. a **fixed 呼応 template that lexically orders its two halves** —
   「AだけでなくBも」, 「AほどBはない」, 「〜のは…からだ」. Both halves are
   positionally fixed BY the template, so neither counts as free.

**The repair when two free units exist: RE-CUT the item.** Move one unit into
the stem (before the first blank), or replace the card with one whose host
forces adjacency by 1–4 above, or fuse the loose unit into the predicate card
so it is no longer separately orderable. Do NOT reroll the drawn form — the
`grammar_p8` target is the contract; the cards are yours.
`20260819_1` 問題8-43 and 問題8-47 both shipped as
*[adjunct block] + [free を-object] + [predicate]* and both admitted a second
★; each was repaired by moving the を-object into the stem, leaving the four
cards as two lexically-chained blocks
(`qa-report-20260819_1-round2` R2-F1/R2-F2). `20260819_1` 問題8-45 was re-cut
the same day the rule was re-scoped: the adjunct clause and the を-object were
replaced by ONE chained unit (`申請書の → 不備が → 見つかった場合は`), with the
object folded into the predicate card (`課長に報告せねばならない`), so the
sentence now has a single pre-predicate unit and one ordering. The class
recurs: `20260810_2` 問題8-45 has the same shape.

**The audit is per item, all five, every time you touch one.** Write the final
predicate down, list every card or block sitting in front of it — arguments AND
adjunct clauses — and name the source (1–4) that fixes each one's position. A
unit you cannot assign a source to is the free one, and there may be at most
one. `tools/verify_scramble.py`'s `free_unit_count()` prints the same number
(`FREE UNITS: n`) off the 解説's word-order line and FAILs at n ≥ 2, so the
audit is recorded rather than remembered — but the tool merges cards by a
string rule and the WRITTEN audit is still the rule.

### The uniqueness proof is a TWO-PART procedure, and three structural legs are illegal

Item integrity #8 requires the 解説's uniqueness note to prove, per card, why
that card cannot be the FINAL card before the fixed tail. Write it in this order,
because the order is what makes it checkable:

1. **Compute the forced blocks first.** For each card, name the card that must
   immediately precede or follow it, and why (a connective's subcategorisation:
   「限らず」 wants a bare 「に」 before it; 「〜つつある」 wants a ます形; 「おかげで」
   wants a 連体形; 「自慢している」 wants a quotative 「と」). Write the blocks out —
   ［A→B］ — before excluding anything.
2. **Then enumerate ONLY the orderings the blocks permit**, and exclude each
   survivor. A survivor that is ungrammatical is excluded structurally; a
   survivor that PARSES is excluded by naming the reading it produces and the
   contradiction that reading creates. Never by "it connects to nothing".

**Three legs are false by construction and `make verify-scramble` now FAILs on
all three** (`illegal_legs()`; run it after every 問題8 edit):

- **"placing X last leaves Y in the middle, where it connects to neither
  neighbour / loses its receiver"**, applied to a card that can sit
  mid-sentence. Two shapes always can: **(a) a card ending in a plain-form
  predicate** is a 連体修飾句 of whatever noun follows it, and **(b) a card that is
  a bare adverbial phrase (に/にも/でも/は/も/まで/から…) whose receiving predicate is
  printed AFTER the blanks** can be fronted over any number of clauses, so it
  never needs an adjacent receiver. **If such an adverbial card exists and the
  other three form one contiguous block, the item has TWO ★ answers and must be
  re-cut** — that is not a proof defect, it is an item defect.
- **"that ordering stacks two particles, so it is impossible."** Only stacked
  CASE particles are impossible (を+が). 「観光客にも地元の人に…」 is everyday
  Japanese (「私にも彼に似たところがある」).
- **「『X〈助詞〉』は述語（動詞）を要求するので［X→その述語］は連続した塊になる」** —
  **false for EVERY case and topic particle**, not only 「を」/他動詞. **A particle
  constrains ORDER, never ADJACENCY**: it licenses a predicate *somewhere later in
  the clause*, and Japanese scrambles pre-predicate material freely. (The one
  particle that genuinely demands an immediately following element is 連体 「の」,
  which wants a noun 直後 — that is source 1, not this leg.)

  **How to tell this leg from a legal one — DIRECTION.** A **bound element
  pointing BACKWARD at its own host** is legal, and adjacency really does follow:
  「そうだ」/「からだ」 wanting a 普通形 **直前**, 「ときほど」 wanting a 連体修飾述語
  **直前**, 「基づいて」 wanting a bare 「に」 **直前**. A **card ending in a
  case/topic particle pointing FORWARD** at "whichever of the four cards is a
  predicate" is this leg, whatever the particle is.

  **Worked example — 「は」, `20260819_1` 問題8-46** (2026-08-20). Cards
  `心細いものは / 体を壊した / ときほど / ない`, key ★=1 on
  「体を壊したときほど心細いものはない」. The 解説 excluded its one rival
  `1→2→3→4`（★=3、「心細いものは体を壊したときほどない」）with
  「『心細いものは』の『は』は述語を要求し、四枚のうち述語は『ない』だけなので、
  ［心細いものは→ない］も塊になる」. In that rival 「ない」 **is** later — just not
  adjacent — so the leg excludes nothing. Item, cards and key were sound; only the
  reason was not, and the valid exclusion was source 4, already named in the same
  解説's opening line: 「AほどBはない」 orders both halves lexically, and the reversed
  「BはAほどない」 forces a gradable-comparative reading that the bare existential
  「ない」 cannot carry.

  The leg proves nothing even when its conclusion happens to hold: at
  `20260819_1` 問題8-44 the two cards really are adjacent, but because
  「あの技術を」 sits INSIDE the 連体修飾 clause headed by 「受け継ぐ人」, which is
  source 1 above — restate the proof from the real source, do not keep the
  leg. Where the leg is load-bearing (`20260819_1` 問題8-43 and 問題8-47) the
  item itself has two ★ answers and must be re-cut per the construction rule
  above. It shipped in **4 of that paper's 5** 解説 as 「を」 (round 2) and in the
  **5th** as 「は」 (round-3 verification) — one paper, all five items.
  `verify_scramble.illegal_legs()` was widened from the 「他動詞」 anchor to the
  particle-general form on 2026-08-20 (`PREDICATE_DEMAND_LEG` + `CASE_TOPIC_END`,
  with a 直前 guard for the backward-looking legal legs) and fires on all five;
  the 70 問題8 items on the 14 papers on disk produce zero findings.

Structural legs stay legal for cards that genuinely cannot attach — a bare
particle tail before the printed tail (nothing to predicate), a テ形 or ます形 with
no host, a 連用 form the tail cannot receive, a card that is not the form the
printed tail demands.

The class has now shipped **three times in one paper's five items**, which is why
the procedure above replaced the old one-paragraph rule:

- `20260818_1` 問題8-47 argued 「『紙で出したがる』を最後に置くと『高齢の利用者が今も
  多い』が途中に入って前後のどのカードとも結べない」. It can: 4→3→1→2 reads
  「高齢の利用者が今も多い電子申請の利用が増えたとはいえ、紙で出したがるそうだ」 and keys
  ★=1. The key still stood — the rival makes elderly users numerous *inside*
  e-application, contradicting the sentence's own point — but that is a SEMANTIC
  argument the 解説 never made (`qa-report-20260818_1` F9). Repaired at that item,
  and **the other four proofs were not re-read**, which is the process half of
  the finding.
- Round 2 then found 問題8-45 with the same leg 「『おかげで』を最後に置くと『子どもの
  急な熱にも』が受け手を失う」 — false, because 「子どもの急な熱にも」's receiver
  「慌てずに済んでいる」 was printed AFTER the blanks. Here the rival WAS grammatical
  and natural (「子どもの急な熱にも祖母が近くに住んでいてくれるおかげで慌てずに済んでいる」),
  so the item had two ★ answers and was re-cut: the adverbial moved into the stem
  and the predicate became the fourth card, leaving no frontable card at all
  (`qa-report-20260818_1-round2` R2-F1).
- The same re-read then found 問題8-44 leaning on the identical leg and 問題8-43
  on the particle-stacking one. Both proofs were rewritten; both items were
  already unique on other grounds.

**An invalid leg in one proof implies nothing about the other four — re-read all
five against this section whenever you repair one.**

**Blanks may end the sentence.** When a re-cut needs the printed tail gone,
`＿＿ ＿＿ ★ ＿＿。` is official practice (12/2025 問題8-44 「そんなに ★ 。」 and
問題8-46 「…初対面とは思えない ★ 。」, `refs/JLPT_N2_NEW/17.N2 12-2025/booklet.md`),
and it removes leg (b)'s whole precondition: with no predicate after the blanks,
no card can be fronted over one.

### Register mix across the 5 items — the archive varies SCENE, not grammar band

A paper whose 問題8 items are all correctly N2-band grammar but all set in
the same dense formal register still reads as uniformly hard — a
register/scene effect, invisible to `level_band_grammar.txt`. Measured over
35 current-era items (`official_calibration.md` §13):

| register | share |
|---|---|
| personal/casual (family, friends, first-person daily life, casual dialogue) | **63%** |
| neutral/factual (trivia, weather, plain description) | 23% |
| formal/institutional (workplace policy, business, admin notice, technical) | **14%** |

Personal/casual is the majority in every one of the 7 sittings; two
sittings (12/2024, 12/2025) ship ZERO formal/institutional items — no
sitting exceeds 2 of 5. Three generated papers checked before this rule
existed skewed the opposite way (73% corporate/formal, one paper 5/5 — a
shape that never occurs in the archive).

**Binding target: at most 2 of the 5 問題8 items may be
formal/institutional; at least 2 should be personal/casual** (family, a
friend, first-person daily life, a casual `A「…」`/`B「…」` dialogue — same
layout as 問題7). Independent of which grammar point was drawn — a
formal-sounding form can still carry a personal-register sentence (`〜わりに`
about a family dinner, not a quarterly budget), and the reverse. Don't let
every item default to office/business setting just because 問題7's seeds or
the test's web topics lean corporate — 問題8's register is a separate
authoring decision.

## 問題9 (cloze)

- Official cloze passages run ~500–700 JP chars (title+body, excluding the
  option lists) — never a 150–200 char mini-paragraph (N3 drill length).
  Four blanks; the prose should read like a short magazine/column piece.
- **Every option stays grammar/phrase scale — never 読解-length
  paraphrases.** Across 7 current-era sittings (112 options), official
  問題9 options run 1–14 JP chars (median 6, mean 6.1). Author to ≤14;
  `make check` FAILs any option >16. A blank whose four choices look like
  問題10–13 主張/内容 options (「〜ことにある」 mini-summaries, 20–40 char
  paraphrases) is off-format even tagged `[内容推論]` — shipped in every
  generated paper until the length gate existed.
- **The four blanks must test four DIFFERENT categories** — assign each a
  distinct type BEFORE writing, then check no type repeats:
  - **(a) 論理接続表現** — sentence-initial discourse connective
    (しかし/そのうえ/つまり…).
  - **(b) 文末モーダル表現** — a modal/inference family on the previous
    clause (わけだ/わけがない/わけではない/わけにはいかない, はずだ/はずがない,
    のも無理はない…) — ONE such family per paper, never two blanks on the same family.
  - **(c) 内容推論** — the choice requires tracking the whole passage's
    argument, not just the local sentence (at least one blank must be
    this). Options stay short grammar/phrase forms like (a)(b)(d)
    (conjugations, short predicates, particles, demonstratives, ≤14 chars).
    **Do not** write four mini-要約 of the thesis — that's 読解 問題10–13,
    not 文章の文法.
  - **(d) 慣用/形式名詞** — a set phrase or formal noun (つもり, 元も子もない,
    願ってもない…). 四字熟語 used as a sentence-final evaluative predicate
    (本末転倒だ, 言語道断だ) count as set phrases and belong here; what (d)
    excludes is a content noun standing in for the thesis.

  Category collision shipped in 4/4 papers with this rule already written,
  because a blank's category was recorded nowhere.
- **The category tag is mandatory OUTPUT** (core §Answer keys): each of the
  four 問題9 rows in the `## 文法` key table must OPEN its 解説 cell with
  the tag in brackets — `[論理接続]` `[文末モーダル]` `[内容推論]`
  `[慣用・形式名詞]`, verbatim. `make check` FAILs unless the four cells
  carry four distinct tags including **exactly one `[内容推論]`**. Example:
  `[文末モーダル] 前の文の「…はずだった」を受け、…`. Assign tags *before*
  writing the blanks — tagging afterward is how earlier papers ended up
  with two modal blanks.

### 問題9's sixteen options have NO pool — measure them by hand or repeat them

問題9 is the only scored surface `sample_items.py` does not draw. Its four
blanks have no pool entry, no ledger row, no cooldown, and no gate: **nothing
has ever compared a paper's 問題9 options against any other paper's.** So the
author reaches for whatever set phrase comes to mind — which is the same
short list every time, and often this file's own worked examples.

`20260817_3` shipped three collisions from that single gap in one run:
元も子もない and やむを得ない both recycled from `20260817_2`'s 問題9-51 — same
item number, one paper apart — and 願ってもない printed as a 問題9 option while
the paper's own drawn `quick_response` list gave it to 聴解問題4-9番 as the
stimulus idiom. All three are examples written into this file above.

**Mandatory, before the key table is written — a WRITTEN measurement, not a
recollection.** Put all sixteen option strings in one column and check them
against two sources:

1. **The previous two papers' 問題9 — every blank, not just the matching
   slot.** `grep -A4 '^\*\*4[89]\*\*\|^\*\*5[01]\*\*' tests/<prev>/言語知識・読解.md`,
   or read the 問題9 block of each. Zero exact repeats, and no repeat of a
   distinctive set phrase (慣用句・四字熟語・modal family) in any position.
   Ordinary connectives (しかし, つまり) and bare formal nouns recur in the
   archive too and are exempt.
2. **This paper's own `test_spec.json`** — the drawn `quick_response`
   phrases, `bunpou` targets and `listening_scenarios`. A 問題9 option that
   is also a drawn item is an in-paper echo the ledger cannot see, because
   the option was never an item.

Record the comparison in the build notes (`logs/topics.json` `notes`) so the
next paper's author has the last set to diff against. If a collision turns up,
change the option — 問題9 has no `--reroll`.

`check_mondai9_option_reuse()` now covers the two halves a regex can decide:
**≤2 of a blank's four options may recur in the SAME blank of either of the
previous 2 papers** (it reads their 問題9 option lists straight out of
`tests/<id>/言語知識・読解.md` — there is no new ledger or `logs/` field to
maintain), and **no 問題9 option may equal a `quick_response`/`grammar_p7`/
`grammar_p8` string this paper drew.** The hand measurement above is still the
rule: the gate compares slot against matching slot, so a distinctive set phrase
moved from 51 to 49 clears it, and only the column catches that.

## Counting

Count Japanese characters only (hiragana/katakana/kanji/JP punctuation);
ignore spaces and the `(　)`/`＿＿`/`★` markers when eyeballing, but don't
strip scene-setting just to hit a number.
