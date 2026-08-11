# 文法 (問題7–9) — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — it carries the N2-band rule, distractor discipline, and
item integrity (the 問題8 assembly, ★-position, glue, and uniqueness link-table
rules are Item integrity #4–#8 there). This file adds the 問題7–9-specific
rules and benchmark lengths, measured on `refs/JLPT_N2_NEW/` (per-sitting
figures: `references/official_calibration.md` §7).

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
  (except the set phrase 言うまでもなく as running text, not a productive key),
  〜を皮切りに, 〜がてら/〜かたわら as keys, 〜ずにはおかない, 〜余儀なくされる
  as the tested form — `## TOO_HARD` in the same file. Avoid shipping
  these as 問題7 keys.
- **One grammar point may be the KEY only once per paper**, and a tested form
  stays out of the reading passages — core Item integrity #15.

## 問題7 — stem length and shape

Official stems average **~43 JP chars** (median ~41; interquartile ~33–54). A
paper whose 12 stems average under ~35, or that ships many under ~30, reads as
textbook-drill short. Target: **each stem ≥30 JP chars, paper average ≥40**,
most items in the **35–55** band. (Note the band's honesty check: 21% of
official 問題7 stems are themselves under 30 — the floor is an authoring
target, not an official per-item invariant; `official_calibration.md` §9.)

Build length with scene-setting (職場・電話・掲示・インタビュー), a subordinate
clause, or a short dialogue lead-in — never by padding the tested form.
Official items often open with `(会社で)` / `(電話で)` / a named role. Avoid short
20–34 char stem averages with the right grammar points where the carrier is too short.
Lengthen the *situation*:
「このまま働きすぎると、体を壊し(　)よ。」 fails the band even when かねない is
the correct key; rewrite toward
「最近残業が続き休日もほとんど取れない。このまま働きすぎると、体を壊し(　)よ。」
(scene + consequence). Same rule for 問題8 frames and 問題9 cloze prose.

**Shape:** every official paper includes several 問題7 items with dialogue
turns or a setting label (`（会社で）`/`（電話で）`/`（インタビューで）`/homepage
notice). Include **at least 2** (prefer 2–4) per paper among the 12 (`make check` WARNs on a set with none).

**Dialogue / setting Markdown layout** — do NOT crush the stem onto one line.
Official booklets put the place label first, then each speaker on its own line:

```
**40** （会社で）
A「どうしたの。」
B「経験がないのに引き受けた(　)、大変な目にあってしまったよ。」
 1. どころか  2. ばかりに  3. ながらに  4. おきに
```

Rules: (1) `（会社で）` etc. alone on the stem's first line after `**N**`;
(2) each speaker turn (`A「…」` / `山田「…」`) on its own following line;
(3) the horizontal option row still on ONE line under the turns. Collapsing to
`**40** （会社で）A「…」B「…」` is forbidden — it reads as a drill line. The
sheet builder keeps its question context across those stem lines, so radios
still attach; do not "fix" a sheet by flattening the dialogue (rendering:
`exam-app`).

## 問題8 (文の組み立て) — length is mostly in the OPTIONS

Measured on `refs/JLPT_N2_NEW/` papers + the official 2018 sample (jlpt.jp
N2G.pdf) and the July 2025 booklet
(`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`):

- **Sum of the four options** typically **16–29 JP chars** (2018 sample has
  chunks like 「山を下りて何日かすると」「二度としたくないと」).
- **Per option:** a mix is fine (a 2–3 char particle next to an 8–12 char
  clause), but **≥2 options ≥5 JP chars** and the longest usually **≥7**. Four
  scraps of 2–4 chars (e.g. `わりに/ケーキは/とても/値段の`) read as drill
  chunks, not N2 scramble chunks.
- **Assembled sentence** (stem frame + four options) **≥45 JP chars**; prefer
  ~50–75. Stem context before/after the blank run is required when the options
  alone cannot fund that length.
- Prefer **nested/phrase chunks** (複文フレーム) over isolated particles when
  the grammar point allows.

**Treat all of the above as authoring targets, not rejection grounds.** §9 of
`official_calibration.md` measured the gate's three 問題8 constants against the
archive and they reject **20% / 38% / 34%** of official items (`P8_OPT_SUM_MIN`
16 vs an official band of 9–41; `P8_LONG_OPTS_MIN` 2 vs 0–4; `P8_ASSEMBLED_MIN`
45 vs 30–78); 51% of all official options are under 5 chars, and a bare adverb
or particle on a card is official practice. Chunk-size intuitions do not
survive contact with the archive — **the invariant is ★-uniqueness** (core Item
integrity #8, the link table), and length is calibration.

### Register mix across the 5 items — the archive varies SCENE, not grammar band

A paper whose 問題8 items are all correctly N2-band grammar but all set in the
same dense, formal register still reads as uniformly hard — because "hard"
here is a register/scene effect, not a grammar-band one, and it is invisible
to `level_band_grammar.txt`. Measured over the same 35 current-era items
(`official_calibration.md` §13), classifying each stem's setting:

| register | share |
|---|---|
| personal/casual (family, friends, first-person daily life, casual dialogue) | **63%** |
| neutral/factual (trivia, weather, plain description) | 23% |
| formal/institutional (workplace policy, business, administrative notice, technical) | **14%** |

**Personal/casual is the majority register in every one of the 7 sittings, and
two sittings (12/2024, 12/2025) ship ZERO formal/institutional items** — an
all-personal paper is normal; no sitting exceeds 2 of 5 formal/institutional
items. Three generated papers checked before this rule existed skewed the
opposite way — 11/15 items (73%) corporate/formal (契約書 negotiation, system
procurement, price negotiation, workplace manuals), one paper 5/5 formal — a
shape that never occurs in the archive.

**Binding target: at most 2 of the 5 問題8 items may be
formal/institutional; at least 2 should be personal/casual** (family, a
friend, first-person daily life, a casual dialogue quote — `A「…」`/`B「…」`
same layout as 問題7). This is independent of which grammar point was drawn —
a formal-sounding grammar form can still carry a personal-register sentence
(`〜わりに` about a family dinner, not a quarterly budget), and the reverse.
Do not let every item default to the same office/business setting just
because 問題7's carrier seeds or the test's web topics lean corporate; 問題8's
register is a separate authoring decision from 問題7's.

## 問題9 (cloze)

- Official cloze passages run **~500–700 JP chars** (title + body, excluding
  the four option lists). Never a 150–200 char mini-paragraph — that is N3
  drill length. Four blanks; the prose must feel like a short magazine/column
  piece.
- **The four blanks must test four DIFFERENT categories** — assign each blank a
  distinct type BEFORE writing, then check no type repeats:
  - **(a) 論理接続表現** — sentence-initial discourse connective
    (しかし/そのうえ/つまり…);
  - **(b) 文末モーダル表現** — a modal/inference family attached to the previous
    clause (わけだ/わけがない/わけではない/わけにはいかない, はずだ/はずがない,
    のも無理はない…) — ONE such family per paper, never two blanks drawing on
    the same family;
  - **(c) 内容推論** — a full predicate requiring the whole passage's argument,
    not just the local sentence (the passage-level trap — at least one blank
    must be this type);
  - **(d) 慣用/形式名詞** — a set phrase or formal noun (つもり, 元も子もない,
    願ってもない…).

  Category collision shipped in **4/4** papers with this rule already written
  (t1 48/51; t2 49/50/51; t3 48/50; t4 48/51), because a blank's category was
  recorded nowhere.
- **The category tag is mandatory OUTPUT** (core §Answer keys): each of the
  four 問題9 rows in the `## 文法` key table must OPEN its 解説 cell with the
  tag in brackets — `[論理接続]` `[文末モーダル]` `[内容推論]`
  `[慣用・形式名詞]`, these four strings verbatim. `make check` matches them
  literally and FAILs unless the four cells carry four distinct tags including
  **exactly one `[内容推論]`**. Example cell:
  `[文末モーダル] 前の文の「…はずだった」を受け、…`. Assign the tags *before*
  writing the blanks and write each blank to its tag — tagging afterwards, to
  whatever you happened to write, is how t1/t2/t4 ended up with two modal
  blanks. The `[内容推論]` blank is the one whose four options are full
  predicates/clauses and cannot be chosen from the local sentence alone (t3's
  blank 50 is the shipped example that qualifies).

## Counting

Count Japanese characters only (hiragana/katakana/kanji/JP punctuation); ignore
spaces and the `(　)` / `＿＿` / `★` markers themselves when eyeballing, but do
not strip scene-setting just to hit a number.
