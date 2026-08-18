---
name: question-authoring
description: Single owner of how to WRITE JLPT exam items at the correct difficulty — vocabulary, kanji, grammar, reading passages, and listening dialogues, including distractor design — and of difficulty calibration against the reference material. Use whenever creating or revising any exam question, whenever the user says questions "seem easy/hard", asks to "check against N2 material", verify difficulty level, calibrate exam content, compare with real JLPT booklets, or when the refs/ PDFs (Shin Kanzen textbooks, the official past-exam archive) need reading. Difficulty bugs are the #1 revision cause — consult this before writing a single item.
---

# Question Authoring (N2 calibration)

Questions are written to Markdown sources inside `tests/<test_id>/`:
`言語知識・読解.md` and `聴解.md`.

## Reading map — load this core + exactly ONE section file

This file is the core: N2 band, distractor discipline, item integrity,
formatting. Per-問題 construction rules live in `references/`; a
section-authoring agent reads this file plus the one row matching its job:

| Authoring… | Also read |
|---|---|
| 問題1–6 (文字・語彙) | `references/moji-goi.md` |
| 問題7–9 (文法) | `references/bunpou.md` |
| 問題10–14 (読解) | `references/dokkai.md` |
| 聴解 items (booklet options + script grounding) | `references/choukai-items.md` |
| any calibration number (lengths, counts, bands) | `references/official_calibration.md` |
| the `refs/` PDFs themselves | `references/reading-reference-pdfs.md` |

`references/level_band_grammar.txt` (問題7–9 band list) and
`references/banned_collocations.txt` are data files those documents cite.

## The golden rule — stay inside the N2 band

Draft an item, then ask **both** sides before keeping it:

1. **"Would this appear as a headed item in an N3 (or N4/N5) book?"** If
   yes, discard — too easy.
2. **"Would Shin Kanzen N1 / a standard N1 list claim this as an N1
   form?"** If yes, and it's **not** in Shin Kanzen N2's inventory, discard
   — too hard.

The tested point must be something an N2 mock may key on. Passive exposure
to harder wording in a 読解 passage is fine when glossed with `（注N）`; it
must not be the answer discrimination. Off-level KEYS are an automatic QA
fail — `exam-qa-review` §2.5 and `references/level_band_grammar.txt`
(grammar only; the vocabulary-key check is the manual Shinkanzen/Soumatome
verification in `references/moji-goi.md` — `openjlpt`, the scripted corpus
this used to read, was removed 2026-08-11). Verify every tested item against
`refs/Shinkanzen/`; benchmark structure, distractor density, and length
against `refs/JLPT_N2_NEW/`. Items drawn `"origin": "adjunct"` passed
`classify_level.py` — treat them like pool items; never swap for memory picks.

## Calibrate to the BAND, not to one paper

`references/official_calibration.md` is the measured evidence of record —
every 読解 length, （注N）/（中略） count, 問題7/8/9 length, 問題1 distractor
convention, 問題11 shape, and key-position distribution in it was measured
across the archive (31 sittings for keys, 15 for prose, the 7 current-format
sittings 12/2022–12/2025 for anything format-dependent). Read it before
quoting a number:

1. **The exam has eras.** The current blueprint (71+30 items, 問題11 as four
   2-question passages) dates from 12/2022; older papers are a different
   shape and must never be averaged into a band.
2. **One paper cannot tell a rule from a coincidence.** Several repo rules
   were derived from July 2025 alone and fail other official papers — §9
   lists each with a replacement. A floor that rejects an official paper is
   a wrong floor.
3. **Never report a number you could not compute**, and say what you could
   not measure (§0). Name the window honestly: "verified against the Shin
   Kanzen inventory and the 7 current-format sittings," not "5 past exams".
4. **`refs/` is calibration-only** — never copy questions, example
   sentences, or passages; all exam content must be original.

PDF mechanics — text-layer diagnosis, rasterizing scans, OCR trust rules for
the archive's `script.md` — are in `references/reading-reference-pdfs.md`.

## Distractor plausibility — the sniff-test rule (governs every section)

`exam-qa-review`'s two-answer hunt catches a distractor too STRONG (a second
defensible answer). This rule catches the opposite: a distractor too WEAK —
eliminable on sight for a reason unrelated to the tested point.

**The test, for every distractor:** *"Would a well-prepared N2 examinee,
moving quickly, seriously weigh this option before ruling it out — for the
SPECIFIC reason the item tests — or does it die on sight for an unrelated
reason (wrong part of speech, domain, tone, register)?"* On-sight death
makes it noise. Replace it with a real competitor in the key's category:

- **問4–6:** every distractor shares the key's part of speech AND
  functional category — a comparative adverb key gets degree/comparison
  adverbs, never a grab-bag of regret (あいにく)/gradualness (徐々に)/
  coincidence (たまたま), with no tonal clash (痛快 beside 切実/深刻 dies on
  tone alone). 問題6 wrong sentences stay inside THAT word's domain —
  wrong collocation or register, never an inapplicable domain.
- **問題1:** the two-branch rule — same/same-radical kanji OR a real N2
  word in the same field — is stated ONCE, in `moji-goi.md`, with the
  conjugation lock and lookup procedure. Both branches legal; a grab-bag
  satisfying neither is forbidden, and when both are empty the TARGET is
  undrawable — report for re-draw, never invent a word.
- **聴解 問題1–3:** an option nobody says in the dialogue is fabricated
  noise. Procedure and artifact (dialogue first, options harvested from it,
  one `N ✗「line」→ reason` line per wrong option): `choukai-items.md`.

Construction-time discipline: draft the key, then three competitors from the
SAME category, then check each is impossible for a specific, nameable
reason (Item integrity #11). Too-weak and second-answer are two ends of one
axis — aim for the narrow band between them.

### The functional-category line is mandatory OUTPUT, not a thought

This rule shipped broken in 4/4 papers because it had no artifact — a
skipped check and a passed check look identical on disk. So the check is a
line that exists or doesn't:

- **Every 問1–6 item's `## 文字・語彙` key notes print the category of all
  four options on one line**: `24: 程度副詞 ×4 (比較的/非常に/たいして/一段と)`.
  One label, `×4`. If the four honest labels aren't identical, the item is
  NOT shippable — replace the odd options. Never invent a label broad
  enough to cover a grab-bag (「副詞」 over three categories hides a failed item).
- **問題1 items additionally print each distractor's resolved source and
  branch label on the same line** — procedure in `moji-goi.md`. NO GATE
  checks 問題1 readings — the written line IS the check.

## Topics (from `test_spec.json`, written by you — no web fetch)

Ownership and the N2-authoring gate for topics: `exam-blueprint` Part II —
read before drafting. Binding: the TESTED item is always the sampled pool
item in `test_spec.json["items"]`; the assigned `reading_topics`/
`listening_scenarios` entry sets scene and content only. There is no
`origin: web` entry to honor anymore — 問題9 is authored from its own
assigned entry exactly like 問題10-13, and any invented flavor detail (a
number, a deadline, a survey figure) is your own invention, N2-simplified
(約4割, not 38.6%), never phrased as a citation.

## Item integrity (every rule here shipped broken at least once)

`make check` enforces the mechanical half per test; the rest is on you. Run
it before calling any authoring work done.

1. **Numbered markers pair 1-to-1 with stems.** Every `①**…**`/`②**…**` must
   be referenced by a question in that passage's set — no orphans. Just as
   binding, easier to skip: every stem anchoring on a quoted span
   (`「…」とあるが`) must point at a span that is ITSELF marked and bolded —
   never a bare quote with no `①**…**` on either side (`20260817_1` shipped
   three). `dokkai.md` §"Marked-span quoting" owns the rule; `make check`'s
   `check_dokkai_span_anchor_bold` FAILs the bare-quote shape.
2. **Four DIFFERENT options.** The same string twice is a second correct
   answer. Read the four back aloud.
3. **The key goes where `answer_positions` says — a SILENT spec means
   STOP.** The spec prescribes the key's option number for all 101 items;
   write the item, then order options so the key lands on its slot.
   `make check` passes with `(0 prescribed)` when the field is absent — a
   spec without it did not come from the sampler: re-run
   `sample_items.py --seed <n> --test-id <id>` and author against its output.
4. **問題8: the answer is the option on ★ = the 3rd of 4 blanks.** Assemble
   the sentence, confirm it grammatical, number positions, read off the
   3rd. Write the 解説 as the word order, key bolded:
   `状況に(2)→おいて(4)→**価格競争が(1)**→続く限り(3)` — `make check` parses
   it and asserts its 3rd entry equals the key.
5. **問題8: the stem must be MISSING exactly what the options supply.**
   Write the full sentence, cut the four-part span out — never leave the
   words in the stem too. Test: splice stem + options in 解説 order, read
   end to end — any word occurring twice means the stem is wrong.
6. **Every scramble forms ONE grammatical sentence.** Two options that
   cannot coexist make the item unanswerable regardless of key (「わりに」
   and 「にもかかわらず」 both offered). One contrast marker, one degree adverb.
7. **問題8: check the GLUE at both ends.** The chain must also join the
   stem's fixed text before the first blank and after the last. Read
   lead-in + four options in key order + tail as one unbroken sentence.
8. **問題8: exactly ONE of the 24 orderings may be grammatical — build for
   it, then COUNT it.** A bare adverb/particle on a card is official
   practice (`official_calibration.md` §7) — but it constrains neither
   neighbour, so **a bare-adverb card makes the link table mandatory**. An
   under-glued card (ending in を/に/が/と/の, a 接続形, or 連体形) sits in
   one slot — a way to reach uniqueness, not a requirement. The count:
   write lead-in **L** and tail **T**; fill the 4×4 table of ordered pairs
   (`○` where option i's ending can immediately precede option j's opening)
   plus the 8 boundary cells `L→i`/`i→T`; count complete paths `L→…→T`
   visiting all four cards. Exactly one may exist — two+ = two defensible
   ★ (attach the adverb to what it modifies on the SAME card, or move it
   into the stem); zero = unanswerable. Record it in the 解説 cell after the
   word order: `｜一意性: 24通り中1通り、裸の副詞なし` — with **no
   parenthesised single digit** in the suffix (`make check` reads every
   `(1)`–`(4)` as word order). Add no further numeric limits — chunk-size
   floors reject 20–38% of official items (`bunpou.md`).
9. **A cloze blank must not repeat what the stem already says.** Read
   stem-plus-option aloud as one sentence for all four.
10. **Exactly ONE option may be defensible — three WRONG answers, not three
    weaker ones.** If a distractor fails only because "the key is slightly
    more natural", rewrite the stem until the distractor is impossible
    (切実 → put it on 願い, where 深刻 cannot go).
11. **Name the reason each distractor is IMPOSSIBLE — in writing, in the
    解説 cell.** The test is a SEARCH, not a feeling: check whether
    distractor+frame is an attested collocation; if it exists the item has
    two keys — REPLACE THE DISTRACTOR, never defend the key. Near-synonyms
    are the whole risk: すなわち vs つまり, に沿って vs に即して, 無記入 vs
    未記入, いいかげん vs おろそか, 停滞 vs 難航, 超満員 vs 大満員, 消費 vs
    需要, こと vs だけ.
12. **問題5 言い換え: the option must be SUBSTITUTABLE.** Read the stem with
    the option swapped in (比較的 for 「値段の**わりに**」 →
    「値段の比較的美味しい」 is unanswerable as printed). A meaning match
    isn't enough; the frame must accept the word.
13. **問題1 & 問題2: 2×2 Cartesian product matrix ({A, B} × {C, D} → {AC,
    AD, BC, BD}).** Generate/validate deterministically with
    `python3 tools/matrix_helper.py` (zero token cost).
    - 問題1 on-reading compounds (矛盾, 縮小, 概要, 効率): options follow
      the 2×2 reading matrix — never break the grid with an arbitrary 3rd
      ending.
    - 問題2 2-kanji compounds (下品, 運河, 下駄, 開港): options follow the
      2×2 component matrix; pseudo-compounds (下晶, 不品) are normal and expected.
14. **問題1 & 問題2: okurigana non-exposure and kanji legitimacy.**
    - Underline covers the whole word (`**生じる**`, never `**に**生じる`
      or `**生**じる`).
    - Okurigana non-exposure (問題1): all four options share the exact
      printed okurigana (`生じる` → all four end `〜じる`, never `〜する`).
    - Kanji legitimacy (問題2): every constituent glyph is a real, legitimate
      常用/N2 kanji — no alien glyphs (banned: `惰楪`'s `楪`).
    - Single-kanji stems (けわしい→険しい): all four share the okurigana and
      use real radical/homophone sets.
    - Native compound items (やぬし→家主): plausible standard kanji only —
      never gibberish (`守柱`).
15. **One grammar point may be the KEY only once per paper** — not once per
    問題, and a tested form stays out of the reading passages.
16. **問題6: the correct sentence must be FLAWLESS, the wrong ones merely
    wrong.** A distractor must be a MISUSE, not a rarer valid use (「品質の
    向上に妥協した」, 「考慮に値する」 are real = second correct sentences).
    Search every wrong sentence's collocation; attested = rewrite.
17. **Japanese only — no Latin script in the prose.** A stray English word
    is a sentence never finished. Loan words in katakana; only real-paper
    initialisms (SNS, AI, CD…) pass the gate.
18. **Distractors are grammatical Japanese that is merely WRONG** — a wrong
    collocation or domain a learner could believe, never word salad
    (「整備がおろそかに完璧だった」 tempts nobody, tests nothing).
19. **解説 must quote the REAL text — copy-paste, never paraphrase from
    memory.** A paraphrase inside 「」 is a defect even when the key is
    right; no findable quote = the item is broken, not the explanation.
    Treat every 解説-quote WARN as a diff list to re-paste, never as noise.
20. **即時応答: the keyed reply must fit the speaker's rank and keigo
    DIRECTION.** When the prompt names roles, check every option's
    honorific direction against them.

## Markdown formatting contract (prevents HTML numbering bugs)

- **Stems use bold numbers, never Markdown list syntax**: `**1** 労働組合は...`,
  `**71** ...` (言語知識・読解.md) and `**例**`, `**1番**` (聴解.md). NEVER
  `1. 労働組合...` — `N.` lines become `<ol>`, which resets numbering at
  every header.
- **Horizontal options (問題1–5, 問題7, 問題8):** one line, leading space,
  double spaces between choices — the builder converts 3+ options on a line
  to ideographic spacing. 問題7 dialogue stems are multi-line
  (`bunpou.md`); only the option row stays on one line.
- **Vertical options (問題6, 問題10–14, 聴解):** one option per line, leading space.

## Answer keys — format pointers and the required artifacts

- **The answer-key TABLE format** (headings, table shapes, row counts) is
  owned by `jlpt-exam-structure` — its spec is the sole statement.
- **Key-heading truncation** (the sheet builder cuts at the first
  `解答`/`正解`-initial heading, errors without one) is owned by `exam-app`.
- **Six rules are complied with by writing a specific line into a key
  cell**, not by thinking something. An absent artifact makes the item unshippable:

| Artifact | Where it goes | Shape | Rule lives in |
|---|---|---|---|
| Functional-category line | `## 文字・語彙` key notes, every 問1–6 item | `24: 程度副詞 ×4 (比較的/…)` | this file (sniff test) |
| 問題1 distractor sources | same line, 問1 items | resolved headword + branch label per option | `moji-goi.md` |
| 問題8 uniqueness note | `## 文法` rows 43–47, after the word order | `｜一意性: 24通り中1通り、裸の副詞なし` | this file (#8) |
| 問題9 category tag | the four 問題9 rows, opening the 解説 cell | four distinct bracketed tags, exactly one `[内容推論]` | `bunpou.md` |
| 問題14 two-cell quotes | `## 読解` rows 70 and 71 | two distinct `「…」` spans present in the flyer | `dokkai.md` |
| 聴解 option grounding | `聴解.md` 問題1/2/3 解説 cells | `1 ✗「script line」→ 理由`, one per wrong option | `choukai-items.md` |
| Marked-span bold+marker | 問題10–14 passage AND its stem, wherever `「…」とあるが` | `①**span**とあるが` on both sides | `dokkai.md` §"Marked-span quoting" |

`make check` reads the 問題9 tags, 問題14 quote pairs, and marked-span
bold/marker pairing, and FAILs on them; the other three are read by `exam-qa-review`.

**読解 quality — three more rule clusters live in `dokkai.md`, not
duplicated here**: (1) a （注N） gloss must never leak the fact its own item
tests, and its headword must clear a same-paper reuse check
(`check_note_band_reuse()`); (2) a keyed 読解 option in 問題10–13 must be
genuinely paraphrased (no verbatim lifts), and never answerable purely from
the stem's own quoted span; (3) key length must be unpredictable — all 4
options within max/min ≤1.30, paper-level longest-key rate in the 20–35%
band. Read `dokkai.md` §"（注N） glosses" and §"読解 keys — unpredictable
option lengths and strict paraphrasing" in full before authoring or
reviewing 問題9–14 — do not rely on this summary while drafting.
