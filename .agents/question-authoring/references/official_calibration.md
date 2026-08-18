# Official N2 calibration — measured across the `refs/JLPT_N2_NEW/` archive

**What this is.** Every number below was measured, not remembered, from the
**31 official N2 sittings 7/2010–12/2025** in `refs/JLPT_N2_NEW/` plus the
official answer-key PDF in the same folder — because the repo's earlier
calibration constants were derived from **one** paper (July 2025), and a
sample of one cannot tell a rule from a coincidence. Six of the seven
constants audited in §9 fail at least one other official paper.

**Calibrate against the BAND, not against one paper.** Where a band is
given, authoring targets the median and the gate floors sit below the
observed minimum.

**Copyright.** `refs/` is calibration input only. This file records counts,
lengths, and stem *shapes* — it quotes only short recurring format frames
(「筆者の考えに合うのはどれか」), never passage or option content.

---

## 0. Method, and what is NOT measurable

Extraction: `.agents/external-test-import/scripts/extract_pdf_text.py` on
all 62 booklet/script PDFs, into a scratchpad (never the repo). All 31
**booklets** carry a real text layer (11.5k–13.3k JP chars each). Measured
with `measure.py` (prose/apparatus) and `parse_answers.py` (keys), both
reading each sitting's real per-大問 item counts (no era's numbering assumed).

Character counting: unless stated otherwise, **JP chars only**
(hiragana/katakana/kanji/JP punctuation) — the same class
`tools/check_consistency.py` uses. JEES's own 字 figures count digits/Latin
too; §1 gives both since for 問題14 the difference is ~25%.

A section's number is used only when the parser recovered exactly as many
stems as the official key has items for that 大問 (and, for 問題10, five
passages) — cells failing that test are excluded, not guessed.

### Unavailable / unreliable — do not invent numbers for these

| Measurement | Why |
|---|---|
| **聴解 script text for 28 of 31 sittings** | only 12/2023, 7/2024, 12/2024 have a text layer (~7.2–7.5k chars); the rest extract to ~1.0–2.0k chars (instructions/setup lines only, no dialogue). Turn-count/pacing are measured from the MP3s instead. |
| **例 (practice item) conventions** | no 例 appears anywhere in the 31 booklets or three full scripts, or the official 2009 sample script. `jlpt-exam-structure` must not cite this file for 例 content conventions. |
| **問題1 underline rendering as JEES prints it** | the archive is a Vietnamese-market reproduction typeset in Word, not a JEES scan — §5's finding is consistent but is the reproducer's typography. |
| **問題10/11 per-passage split, 6 pre-2018 sittings** | a passage marker is lost in extraction for those 6; section totals stay reliable, per-passage numbers are excluded. |
| **問題8 for 12/2022 and 7/2023** | only 3/5 and 1/5 items recovered (multi-line option rows). |
| **7/2023 問題14 item numbers** | misprinted 68/69 where the key says 70/71 — measured with ±4 slack, flagged not corrected. |
| **7/2025 問題11 instruction line** | prints 「(1)から(3)」 but the paper has four passages/eight items — count passage markers, never trust the instruction. |

---

## 1. Format drift: the exam has three eras, and the repo models the newest

From the official answer-key PDF, which parses cleanly for all 31 sittings.

| Era | sittings | 言語知識・読解 items | 大問 1–14 counts | 聴解 items | 聴解 1–5 counts |
|---|---|---|---|---|---|
| 7/2010 – 7/2018 | 17 | **75** | 5/5/5/7/5/5/12/5/5/5/9/2/3/2 | **32** | 5/6/5/12/4 |
| 12/2018 – 7/2021 | 6 | 72–73 | 問3→3, 問4 wobbles, 問9→4, 問11 9↔8 | 30 | 5/5–6/5/11/3–4 |
| **12/2021 – 12/2025** | **9** | **71** | **5/5/3/7/5/5/12/5/4/5/8/2/3/2** | **30** | **5/6/5/11/3** |

- The 2009 guidebook's 小問数目安 matches the 2010–2018 column (75+32=107)
  exactly; the current 大問のねらい PDF has dropped that column entirely —
  consistent with counts having drifted below it.
- **The repo's 71+30=101 contract is correct — the 12/2021-onward format**,
  including 聴解問題4=11 (not 12) and 問題5=2 items/3 answers (not 3/4).
- **One further break inside the current era**: 問題11 was 3 passages
  through 7/2022, became **4 passages × 2 items from 12/2022**, and its
  length jumped with it (§2). **The right 読解 calibration window is the 7
  sittings 12/2022–12/2025**, not "the last five papers."

---

## 2. 読解 section lengths — the band

JP chars of passage prose (instruction/stems/options removed; （注N）
definitions kept, as `check_dokkai_lengths()` does).

### Current format (12/2022 – 12/2025, n = 7)

| 大問 | min | median | max | all-char median (JEES 字) | JEES spec |
|---|---|---|---|---|---|
| 問題10 短文 (5 passages) | **1143** | 1225 | 1329 | 1328 | 200字 × 5 |
| 問題11 中文 (4 passages) | **2449** | 2556 | 2685 | 2712 | 500字 × n |
| 問題12 統合 A/B | **532** | 551 | 592 | 551 | 合計600字 |
| 問題13 長文 | **814** | 904 | 1061 | 961 | 900字 |
| 問題14 情報検索 | **489** | 604 | 638 | **707** | 700字 |

Per sitting (問10/問11/問12/問13/問14): 12/2022 1169/2609/537/814/611 · 7/2023
1190/2556/581/1005/621 · 12/2023 1143/2542/551/904/638 · 7/2024
1329/2685/592/817/566 · 12/2024 1258/2667/532/1061/504 · 7/2025
1249/2451/572/989/604 · 12/2025 1225/2449/543/882/489.

Wider windows, for context only (do not author to these): last 15 sittings
問10 1140–1444 (med 1213), 問11 1778–2685 (med 2179), 問12 495–596 (med 569),
問13 814–1136 (med 989), 問14 437–638 (med 566); all 31 give similar or wider
bands.

**問題14 is the one section where JP-char counting misleads**: the flyer is
full of dates/prices/times. All-char it measures 676–793, median 707 — right
on the published 700字程度; in JP chars alone it looks 25% short.

### Per passage

| | min | median | max | n |
|---|---|---|---|---|
| 問題10 短文, each passage (current) | **157** | 241 | 334 | 35 |
| 問題11 中文, each passage (current) | **507** | 655 | 763 | 28 |

問題11's per-passage median (655) runs ~30% above JEES's own 500字程度 spec;
問題10's minimum (157, 12/2023 passage 5) sits below the 200字 spec — official
短文 passages are allowed to be short.

---

## 3. （注N） glosses and （中略）

In-body markers only (a `（注N）用語：定義` definition line is not counted).

| sitting | 問10 | 問11 | 問12 | 問13 | 問14 | total 10–14 | （中略）/paper |
|---|---|---|---|---|---|---|---|
| 12/2022 | 5 | 22 | 0 | **0** | 0 | 27 | 5 |
| 7/2023 | 5 | 20 | 0 | 7 | 0 | 32 | 3 |
| 12/2023 | 6 | 24 | 0 | 9 | 0 | 39 | 2 |
| 7/2024 | 13 | 36 | 0 | 12 | 0 | **61** | 4 |
| 12/2024 | 12 | 33 | 0 | 9 | 0 | 54 | 4 |
| 7/2025 | 3 | 17 | 0 | 7 | 0 | 27 | 3 |
| 12/2025 | 10 | 26 | 0 | 6 | 0 | 42 | 3 |

- **Current-era band: 27–61 markers/paper, median 39.** Last 15: 17–61, med
  32. All 31: 14–61, med 28.
- **問題12 and 問題14 get 0 in every current-era paper** — the count is
  earned in 問題11/問題13; never spread a quota across 問題10.
- Per 問題11 passage: min 2, median 5.5, max 13 (n=28; 26 of 28 carry ≥3).
  問題13: 0–12, median 7 (12/2022 shipped zero).
- **（中略）: 2–5 per paper in the current era (median 3), never 0.** Last 15:
  0–5 (a few sittings shipped none).
- Official uses 「ここでは、…」 freely in definitions (e.g. 像を結ぶ →
  「ここでは、姿がわかる」) — the repo's ban targets *circular* definitions of
  basic words, not the phrase itself.

---

## 4. 問題11 question pairing — "exactly one 事実把握 + one 考え/主張" is a July-2025 artifact

Classified by stem shape (考え/主張 = 考えに合う/言いたいこと/どう考えて/
大切にしていること/述べていることに合う; everything span- or 筆者によると-
anchored = 事実把握). Current era, 4 passages × 2 stems:

| sitting | pair 1 | pair 2 | pair 3 | pair 4 |
|---|---|---|---|---|
| 12/2022 | 事/事 | 事/考 | 事/事 | 事/考 |
| 7/2023 | 事/事 | **考/考** | 事/事 | 事/事 |
| 12/2023 | 事/事 | 事/事 | 事/考 | 事/事 |
| 7/2024 | 事/考 | 事/考 | 事/考 | 事/事 |
| 12/2024 | 事/考 | 事/事 | 事/事 | 事/事 |
| **7/2025** | 事/考 | 事/考 | 事/考 | 事/考 |
| 12/2025 | 事/考 | 事/事 | 事/考 | **考/考** |

**28 pairs: 13 one-of-each, 13 two-事実, 2 two-考え.** July 2025 is the ONLY
sitting where all four pairs are one-of-each — a gate FAILing any other shape
would fail 6 of the 7 current official papers.

What DOES hold across all 7: every paper carries at least one 考え/主張 stem
in 問題11 (1–4 of the 8); the 事実把握 stem comes first in 26 of 28 pairs
(exceptions are the two-考え pairs); the four banned retrieval shapes
(「本文で述べられている〜」「〜として正しいものはどれか」「〜の主な目的は何か」
「〜の内容と合っているものはどれか」) appear **0 times**, in any 問題10–14, in
15 sittings — fully corroborated. **「筆者」 is NOT in every stem** — 10 of
56 current-era 問題11 stems (18%) omit it, anchoring on a marked span instead.

問題13 (3 items) is far more regular: items 67/68 are span/筆者-anchored and
item **69 is a 考え/主張 stem in 7 of 7** current papers.

---

## 5. 問題1 — underline and distractors

Underline (rasterised 7/2025 and 12/2025 page 1): the mark covers the whole
word incl. okurigana/inflected tail (辛い/収まった/争って underlined
complete, never partial) — corroborates `question-authoring`'s rule.
**Single-kanji whole words are drawn officially** (腕, 柱) — not
"undrawable", just one-kanji-spelled words.

Distractors, all 35 current-era items classified:

| target type | n | what the distractors are |
|---|---|---|
| **訓読み** (okurigana printed, or single-kanji) | 12 | **real words, every option, no exception** — same word class/conjugation as the key, usually the same semantic field; frequently don't share the target's kanji. |
| **音読み compound** | 23 | predominantly non-words: 清濁/長短/ん⇄う manipulations of the key's own on-reading. |

**Refinement**: ~5 of 23 音読み sets deliberately mix in real homophone words
(握手→拍手, 討論→議論), and one set is four real compounds — so "音読み
distractors must be non-words" is as wrong as "all four must be dictionary
words". The invariant is directional: **a 訓読み set may never contain a
non-word; a 音読み set may, but only as a derivation of the key's own reading.**

---

## 6. 問題12 / 問題14 — stem formulas

**問題12 is near-formulaic** across all 7 papers: item 65 asks what A and B
have **in common**; item 66 asks how they **differ** in advice/stance.

**問題14: 70 and 71 are BOTH person-scenario items in 7 of 7 papers** — never
「このお知らせの内容と合っているものはどれか」. Key constraint counts: always
≥2 cells, commonly 3. Typical shapes: a named person with 2–3 requirements →
which option; a named person on a given date → what to do to book, decided
by a footnote exception.

---

## 7. 文法 — 問題7 / 問題8 / 問題9

**問題7 stems (JP chars), last 15 sittings, n=180:** mean **43.1**, median
**39**, min **17**, max **103**. 21% of stems are under 30 chars; 9% under
25. Per-paper current-era averages: 36/48/39/51/43/38/43 — min 36.

**問題8, 64 of 75 items over last 15 (85% coverage):**

| measure | official band | median |
|---|---|---|
| sum of the four options | **9–41** | 20 |
| options ≥5 JP chars, per item | **0–4** | 2 |
| longest option | 3–13 | 7 |
| assembled (stem+4 options) | **30–78** | 47 |

51% of official 問題8 options are under 5 JP chars. **Bare adverbs/particles
on a card are official practice, not a defect** (「一度」「もう」「もちろん」
「珍しく」, bare particles like 「だけ」「する」「して」) — 14% of current-era
items carry one.

**問題9 cloze body, last 15: 393–695, median 597.** Current era:
498/597/695/672/577/674/689 — min 498 (7/2021 outlier: 393). Four blanks
every sitting since 12/2020.

**問題9 options (current era, 112 = 7×4×4):** mean 6.1, median 6, range
1–14. Zero options exceed 14 JP chars — a 20–40 char 読解-style paraphrase on
a `[内容推論]` blank is off-format; cap every option at ≤16 (author to ≤14).

**問題6 用法 option sentences: mean 25.0, median 25, range 9–35** (n=136) —
a 9-char option is official, so short alone is not a defect.

---

## 8. Answer-key positions — the 19–27 band is exactly the modern envelope

Counting the 90 four-choice items (all 101 minus 聴解問題4's 11 three-choice
items), from the official key PDF:

| sitting | pos 1 | 2 | 3 | 4 | 19–27? |
|---|---|---|---|---|---|
| 12/2021 | 20 | 27 | 22 | 21 | PASS |
| 7/2022 | 22 | 21 | 23 | 24 | PASS |
| 12/2022 | 21 | 23 | 24 | 22 | PASS |
| 7/2023 | 20 | 23 | 25 | 22 | PASS |
| 12/2023 | 21 | 20 | 25 | 24 | PASS |
| 7/2024 | 22 | 24 | 25 | 19 | PASS |
| 12/2024 | 23 | 22 | 23 | 22 | PASS |
| 7/2025 | 21 | 22 | 26 | 21 | PASS |
| 12/2025 | 19 | 26 | 23 | 22 | PASS |

**All 9 modern sittings satisfy 19–27, and the observed range IS exactly
19–27** — the band is the empirical envelope with zero margin. Pooled modern
share: 23.4/25.5/26.7/24.3% — position 3 is modal, position 1 rarest, so a
sampler forcing 22/23/22/23 would be LESS official than the band. Over all
31 sittings the envelope widens to 19–29 (4 pre-2017 sittings fall outside
19–27). 聴解問題4 (3-choice) is near-uniform, 2–7 per position, typically 4/4/3.

---

## 9. Constants in `tools/check_consistency.py` that do NOT survive the archive

This pass did not edit `check_consistency.py` — another pass owns it.

| Constant | now | reality | verdict | recommend |
|---|---|---|---|---|
| `DOKKAI_FLOOR[10]` | 1150 | current-era min 1143 | FAILS by 7 chars | **1100** |
| `DOKKAI_FLOOR[11]` | 2250 | current-era min 2449 (pre-2022 ran 1778–2179) | survives, era-specific | keep 2250 |
| `DOKKAI_FLOOR[12]` | 510 | current-era min 532 | survives | keep 510 |
| `DOKKAI_FLOOR[13]` | 900 | current-era min 814/817 | FAILS 2 of 7 | **800** |
| `DOKKAI_FLOOR[14]` | 560 | current-era min 489/504 | FAILS 2 of 7 | **450** JP chars, or switch to all-char and floor 620 |
| `DOKKAI_PASSAGE_FLOOR[10]` | 200 | current-era min 157 | FAILS | **150** |
| `DOKKAI_PASSAGE_FLOOR[11]` | 400 | current-era min 507 | survives | keep 400 |
| gloss WARN floor | 15 | current-era band 27–61, med 39 | far too low | **25** |
| `P7_STEM_MIN` | 30 | 21% of 180 official stems under 30 | FAILS heavily | WARN, or lower to 20 — paper-level rule is the real one |
| `P7_PAPER_AVG_MIN` | 35 | current-era averages 36–51 | survives | keep 35; author to 43 |
| `P9_PASSAGE_MIN` | 450 | last-15 min 393 (7/2021), current-era min 498 | survives current era | keep 450; author to ~600 |
| `P8_OPT_SUM_MIN` | 16 | official band 9–41, med 20; 13/64 under 16 | FAILS 20% | **9**, or gate paper median at ~18 |
| `P8_LONG_OPTS_MIN` | 2 | official band 0–4; 24/64 under 2 | FAILS 38% | **0** (retire), or WARN only |
| `P8_ASSEMBLED_MIN` | 45 | official band 30–78; 10/29 under 45 | FAILS 34% | **30** |
| `LONG_KEY_MIN`=50, `LONG_KEY_RATIO`=1.7 | | 138 keys: longest 61, highest ratio 1.55, 0 official trips | survives | keep |

### Two more repo facts the archive contradicts

- **`question-authoring`'s length table and the gate's docstring once gave
  different numbers for the same paper** — three numbers for one paper means
  at least two measurement methods were undocumented; name the method next
  to every number quoted.
- **Official baseline: ~29% of keys are the longest option, evenly spread
  across ranks.** This repo enforces max/min ≤1.30 per item and a 20–35%
  paper-level longest-key rate, against the artificial tell of the key being
  longest in 75%+ of items. Keys in 問題10–13 must be genuinely paraphrased,
  never verbatim lifts.
- **「問題1's 4 options are all real words」/「音読み distractors are
  non-words」** — neither is universal; see §5. **「no bare adverb on a 問題8
  card」** — contradicted, see §7 (the real invariant is single-solution
  uniqueness). **「問題11 pairs are 事実把握1+考え1」** — contradicted by 6 of
  7 current papers; see §4.

---

## 10. Web cross-check (official sources)

| Fact | Source | Archive agrees? |
|---|---|---|
| N2 = 言語知識・読解 105min + 聴解 50min | jlpt.jp/e/guideline/testsections.html | n/a (not PDF-measurable) |
| 3 sections 0–60 each, total 0–180, cutoff 19, pass 90 | jlpt.jp/e/guideline/results.html | matches exactly |
| 問題10=200字, 問題11=500字, 問題12=600字, 問題13=900字, 問題14=700字 | jlpt.jp/guideline/pdf/n2.pdf (no 小問数 column) | 12/13/14 match; 問題11 runs ~30% long, 問題10 sometimes short |
| 2009 小問数目安: 5/5/5/7/5/5/12/5/5/5/9/2/3/2 + 聴解 5/6/5/12/4 (目安, may change) | jlpt.jp/reference/pdf/guidebook1e.pdf p.21 | matches 2010–2018 exactly; current papers are 5 items lighter |
| Sample script: 問題1 speaks the 問い before AND after the dialogue; speakers M/F | jlpt.jp/samples/pdf/N2-script.pdf | matches the three full archive scripts |

No contradiction found between jlpt.jp and the archive — the apparent
小問数-vs-actual-counts conflict is resolved by JEES's own 目安 footnote and
the current PDF dropping the column. Non-official sites were not used for
any number here.

---

## 11. `AGENTS.md` §3 describes the archive (`refs/JLPT_N2_NEW/`)

31 sittings 7/2010–12/2025, one directory per sitting (booklet PDF + script
PDF + MP3); answer keys for all 31 in one PDF. **Calibrate against the band
in this file, not a single paper.** The current format (71+30 items, 問題11
in four passages) dates from 12/2022 — earlier sittings are a different
blueprint and must not be averaged in for 読解 lengths.

---

## 12. 問題5/問題6 katakana-headword rate — the pool over-draws it 5–7×

Measured by reading every 問題5/問題6 item's TESTED HEADWORD across the
current-era archive (n=35 each):

| 問題 | katakana HEADWORD | all-options-katakana (wago headword) | zero katakana anywhere |
|---|---|---|---|
| 5 (n=35) | **3 (8.6%)** | 2 (5.7%) | 30 (85.7%) |
| 6 (n=35) | **1 (2.9%)** | n/a | 34 (97.1%) |

**Combined headword rate: 4/70 (5.7%)**; 6 of 7 sittings drew zero katakana
headwords across both sections. Against this, the pool's `paraphrase`/`usage`
katakana share (27.1%/32.7% at measurement time — 3–6× the official rate)
with a plain `rng.sample()` produced ~4 combined katakana headwords per
paper in expectation; three checked generated papers drew 3/3/6, ~7× the
official rate. **Root cause was the draw, not the writing** — the pool's
katakana share was never capped against measured behavior. The fix
(`sample_katakana_capped()`, `exam-blueprint/SKILL.md`'s katakana section)
is what enforces the rate now, not pool composition — do not re-derive
`KATAKANA_TARGET_RATE` from a fresh `len(katakana)/len(pool)` count.

**Separate finding**: several katakana pool entries (バケツ, ダム, ハンドル,
ピストル, ビタミン, マラソン, モーター, ロビー, ボーナス, ランチ, ランニング…)
read as N3/N4 vocabulary under the golden rule, despite a legacy corpus
labelling them N2 — not purged by this pass; a follow-up band audit (like
`kanji_reading`'s) is still open.

## 13. 問題8 register mix — official skews personal/casual, generated skews corporate/formal

Classified every current-era 問題8 stem's register (n=35) into
personal/casual, neutral/factual, or formal/institutional:

| sitting | personal/casual | neutral/factual | formal/institutional |
|---|---|---|---|
| 12/2022 | 2 | 1 | 2 |
| 7/2023 | 2 | 3 | 0 |
| 12/2023 | 2 | 1 | 2 |
| 7/2024 | 3 | 2 | 0 |
| 12/2024 | **5** | 0 | **0** |
| 7/2025 | 3 | 1 | 1 |
| 12/2025 | **5** | 0 | **0** |
| **total (35)** | **22 (63%)** | **8 (23%)** | **5 (14%)** |

Personal/casual is the majority register in every sitting; two sittings ship
ZERO formal/institutional items, and no sitting exceeds 2 of 5. Three
checked generated papers skewed the other way (73% corporate/formal, one
paper 5/5). **This is a register/scene variance finding, not a grammar-band
finding** — every item's grammar point is still correctly N2; the "問題8
feels uniformly hard" complaint comes from every item sharing one dense
institutional register where official mixes in plain first-person/casual
dialogue. The fix is a register-mix rule in `bunpou.md` §問題8, not a change
to which grammar forms are drawn.
