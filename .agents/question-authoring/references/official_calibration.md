# Official N2 calibration — measured across the `refs/JLPT_N2_NEW/` archive

**What this is.** Every number below was measured, not remembered, from the
**31 official N2 sittings 7/2010–12/2025** in `refs/JLPT_N2_NEW/` plus the
official answer-key PDF in the same folder. It exists because the repo's
calibration constants were all derived from **one** paper (July 2025), and a
sample of one cannot tell a rule from a coincidence. Six of the seven constants
audited in §9 turn out to fail at least one other official paper.

**Calibrate against the BAND, not against one paper.** Where a band is given,
authoring targets the median and the gate floors sit below the observed minimum.

**Copyright.** `refs/` is calibration input only. This file records counts,
lengths, and stem *shapes*. It quotes only the short recurring frames that are
format facts (「筆者の考えに合うのはどれか」), never passage or option content.

---

## 0. Method, and what is NOT measurable

Extraction: `.agents/external-test-import/scripts/extract_pdf_text.py` on all
62 booklet/script PDFs, into a scratchpad (never into the repo). All 31
**booklets** carry a real text layer (11.5k–13.3k JP chars each — consistent, so
complete). The measurement scripts were `measure.py` (prose/apparatus) and
`parse_answers.py` (keys); both read the extracts plus each sitting's real
per-大問 item counts, so no era's numbering is assumed.

Character counting: unless a row says otherwise, **JP chars only**
(hiragana/katakana/kanji/JP punctuation) — the same class
`tools/check_consistency.py` uses, so the numbers here are directly comparable
to its constants. JEES's own 字 figures count digits and Latin too; §1 gives
both, because for 問題14 the difference is ~25%.

Reliability: a section's number is used only when the parser recovered exactly
as many stems as the official key has items for that 大問 (and, for 問題10, five
passages). Cells failing that test are excluded, not guessed.

### Unavailable / unreliable — do not invent numbers for these

| Measurement | Why |
|---|---|
| **聴解 script text for 28 of 31 sittings** | only 12/2023, 7/2024 and 12/2024 script PDFs have a text layer (~7.2–7.5k JP chars). The other 28 are image scans that extract to ~1.0–2.0k chars: 問題 instructions, the 1番/2番 setup lines and the 問い only, no dialogue. Turn-count, spoken-option length and dialogue pacing are therefore **not** measured here — use `official-audio-analysis` on the MP3s instead. |
| **例 (practice item) conventions** | **no 例 appears anywhere** — not in any of the 31 booklets, not in the three full scripts, not in the official 2009 問題例集 script (`jlpt.jp/samples/pdf/N2-script.pdf`, rasterised and read). The only evidence the 例 exists is 問題5's instruction 「この問題には練習はありません」, which implies 問題1–4 have one. Content conventions for 例 are **unmeasurable from this corpus**; `jlpt-exam-structure` must not cite this file for them. |
| **問題1 underline rendering as JEES prints it** | the archive is a Vietnamese-market reproduction typeset in Word, not a JEES booklet scan. §5's underline finding is consistent across sittings but is the reproducer's typography. |
| **問題10/11 per-passage split, 6 pre-2018 sittings** | 12/2015, 7/2016, 7/2017 and 12/2017 lose a 問題11 passage marker in extraction; 7/2014 and 12/2019 lose a 問題10 marker. Section totals for those cells are still reliable; per-passage numbers are excluded. |
| **問題8 for 12/2022 and 7/2023** | only 3 of 5 and 1 of 5 items recovered (multi-line option rows). §7's 問題8 band is over 64 of 75 items in the last 15 sittings (85%). |
| **7/2023 問題14 item numbers** | the source PDF misprints them as 68/69 where the official key says 70/71. Measured with a ±4 slack; flagged, not corrected in the repo. |
| **7/2025 問題11 instruction line** | prints 「(1)から(3)」 but the paper actually carries four passages and eight items. Instruction lines are unreliable across this archive — **count passage markers, never trust the instruction**. |

---

## 1. Format drift: the exam has three eras, and the repo models the newest

Derived from the official answer-key PDF (`ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf`),
which parses cleanly for **all 31 sittings, 100% of items**.

| Era | sittings | 言語知識・読解 items | 大問 1–14 counts | 聴解 items | 聴解 1–5 counts |
|---|---|---|---|---|---|
| 7/2010 – 7/2018 | 17 | **75** | 5/5/5/7/5/5/12/5/5/5/9/2/3/2 | **32** | 5/6/5/12/4 |
| 12/2018 – 7/2021 | 6 | 72–73 | 問3→3, 問4 wobbles, 問9→4, 問11 9↔8 | 30 | 5/5–6/5/11/3–4 |
| **12/2021 – 12/2025** | **9** | **71** | **5/5/3/7/5/5/12/5/4/5/8/2/3/2** | **30** | **5/6/5/11/3** |

- The 2009 guidebook's published 小問数 目安
  (`jlpt.jp/reference/pdf/guidebook1e.pdf`, p.21) is **exactly** the 2010–2018
  column: 75 + 32 = 107. The current 大問のねらい PDF
  (`jlpt.jp/guideline/pdf/n2.pdf`) has **dropped the 小問数 column entirely** —
  consistent with the counts having drifted below the 目安.
- **The repo's 71 + 30 = 101 contract is correct, and is the 12/2021-onward
  format.** So is 聴解問題4 = 11 (not the guidebook's 12) and 問題5 = 2 items /
  3 answers (not 3 items / 4 answers).
- **One further break inside the current era**: 問題11 was **3 passages** (3/2/3
  or 3/3/2 items) through 7/2022 and became **4 passages × 2 items** from
  **12/2022**. Its length jumped with it (§2). **The right calibration window
  for 読解 is therefore the 7 sittings 12/2022 – 12/2025**, not "the last five
  papers" and not `refs/JLPT/`'s five (which mixes 7/2023 in with nothing older
  and misses 7/2024 entirely).

---

## 2. 読解 section lengths — the band

JP chars of passage prose (instruction, stems and option rows removed;
（注N） definition lines kept, as `check_dokkai_lengths()` does).

### Current format (12/2022 – 12/2025, n = 7)

| 大問 | min | median | max | all-char median (JEES 字) | JEES 字程度 spec |
|---|---|---|---|---|---|
| 問題10 短文 (5 passages) | **1143** | 1225 | 1329 | 1328 | 200字 × 5 |
| 問題11 中文 (4 passages) | **2449** | 2556 | 2685 | 2712 | 500字 × n |
| 問題12 統合 A/B | **532** | 551 | 592 | 551 | 合計600字 |
| 問題13 長文 | **814** | 904 | 1061 | 961 | 900字 |
| 問題14 情報検索 | **489** | 604 | 638 | **707** | 700字 |

Per sitting:

| sitting | 問10 | 問11 | 問12 | 問13 | 問14 |
|---|---|---|---|---|---|
| 12/2022 | 1169 | 2609 | 537 | **814** | 611 |
| 7/2023 | 1190 | 2556 | 581 | 1005 | 621 |
| 12/2023 | **1143** | 2542 | 551 | 904 | 638 |
| 7/2024 | 1329 | 2685 | 592 | **817** | 566 |
| 12/2024 | 1258 | 2667 | 532 | 1061 | **504** |
| 7/2025 | 1249 | 2451 | 572 | 989 | 604 |
| 12/2025 | 1225 | 2449 | 543 | 882 | **489** |

### Wider windows (for context only — do not author to these)

| 大問 | last 15 sittings (7/2018–) | all 31 |
|---|---|---|
| 問題10 | 1140–1444 (med 1213) | 1061–1444 (med 1225) |
| 問題11 | 1778–2685 (med 2179) | 1205–2685 (med 2007) |
| 問題12 | 495–596 (med 569) | 451–726 (med 570) |
| 問題13 | 814–1136 (med 989) | 814–1136 (med 989) |
| 問題14 | 437–638 (med 566) | 423–759 (med 575) |

**問題14 is the one section where JP-char counting is misleading**: the flyer is
full of dates, prices and times. All-char (JEES-style) it measures 676–793,
median 707 — right on the published 700字程度. In JP chars it looks 25% short.

### Per passage

| | min | median | max | n |
|---|---|---|---|---|
| 問題10 短文, each passage (current) | **157** | 241 | 334 | 35 |
| 問題11 中文, each passage (current) | **507** | 655 | 763 | 28 |

The 問題11 per-passage median of 655 runs ~30% **above** JEES's own 500字程度
spec. The 問題10 minimum of 157 (12/2023, passage 5) sits **below** the 200字
spec — official 短文 passages are allowed to be short.

---

## 3. （注N） glosses and （中略）

In-body markers only (a line that is a `（注N）用語：定義` definition line is not
counted; every gloss otherwise double-counts).

| sitting | 問10 | 問11 | 問12 | 問13 | 問14 | total 10–14 | （中略）/paper |
|---|---|---|---|---|---|---|---|
| 12/2022 | 5 | 22 | 0 | **0** | 0 | 27 | 5 |
| 7/2023 | 5 | 20 | 0 | 7 | 0 | 32 | 3 |
| 12/2023 | 6 | 24 | 0 | 9 | 0 | 39 | 2 |
| 7/2024 | 13 | 36 | 0 | 12 | 0 | **61** | 4 |
| 12/2024 | 12 | 33 | 0 | 9 | 0 | 54 | 4 |
| 7/2025 | 3 | 17 | 0 | 7 | 0 | 27 | 3 |
| 12/2025 | 10 | 26 | 0 | 6 | 0 | 42 | 3 |

- **Current-era band: 27–61 in-body markers per paper, median 39.** Last 15
  sittings: 17–61, median 32. All 31: 14–61, median 28.
- **問題12 gets 0 and 問題14 gets 0, in every current-era paper.** The count is
  earned in 問題11 and 問題13. Do not spread a quota across 問題10.
- Per 問題11 passage: **min 2, median 5.5, max 13** (n=28). 26 of 28 carry ≥3;
  two carry 2. 問題13: 0–12, median 7 — **12/2022 shipped a 長文 with zero
  glosses**.
- **（中略）: 2–5 per paper in the current era (median 3); never 0.** Over the
  last 15 sittings, 0–5 (12/2017, 7/2011, 12/2011, 7/2019 shipped none).
- Definition-line style: official uses 「ここでは、…」 freely, e.g. July 2025
  問題10(1) glosses 像を結ぶ as 「ここでは、姿がわかる」. The repo bans 「ここでは」
  as a *circular* definition marker — that ban is about glossing a basic word,
  not about the phrase, and should not be read as a prohibition on the phrase
  itself.

---

## 4. 問題11 question pairing — "exactly one 事実把握 + one 考え/主張" is a July-2025 artifact

Classified by stem shape (考え/主張 = 考えに合う / 言いたいこと / どう考えて /
大切にしていること / 述べていることに合う; everything span- or 筆者によると-anchored
= 事実把握). Current era, 4 passages × 2 stems:

| sitting | pair 1 | pair 2 | pair 3 | pair 4 |
|---|---|---|---|---|
| 12/2022 | 事/事 | 事/考 | 事/事 | 事/考 |
| 7/2023 | 事/事 | **考/考** | 事/事 | 事/事 |
| 12/2023 | 事/事 | 事/事 | 事/考 | 事/事 |
| 7/2024 | 事/考 | 事/考 | 事/考 | 事/事 |
| 12/2024 | 事/考 | 事/事 | 事/事 | 事/事 |
| **7/2025** | 事/考 | 事/考 | 事/考 | 事/考 |
| 12/2025 | 事/考 | 事/事 | 事/考 | **考/考** |

**28 pairs: 13 one-of-each, 13 two-事実, 2 two-考え.** July 2025 is the **only**
sitting in the whole archive where all four pairs are one-of-each. A gate that
FAILs a pair with no 考え/主張 stem would fail **6 of the 7** current official
papers.

What *does* hold across all 7:

- **Every paper carries at least one 考え/主張 stem in 問題11** — 1 to 4 of the 8
  (12/2023 and 12/2024 have exactly 1; 7/2025 has 4).
- **The 事実把握 stem comes first in the pair** in 26 of 28 pairs (the two
  exceptions are the two-考え pairs).
- **The four banned retrieval shapes** (「本文で述べられている〜はどれか」
  「〜として正しいものはどれか」「〜の主な目的は何か」「〜の内容と合っているものは
  どれか」) appear **0 times** — not in 問題11, and not in 問題10, 12, 13 or 14
  either, across the last 15 sittings. **The ban is fully corroborated.**
- **「筆者」 is NOT in every stem.** 10 of 56 current-era 問題11 stems (18%) omit
  it; 37 of 125 (30%) over the last 15 sittings. Per sitting the count of
  筆者-less stems is 0/2/3/2/3/0/0. A stem without 筆者 is anchored to a marked
  span instead (「①…とあるが」/「それとは何を指すか」).

問題13 (3 items) is far more regular than 問題11: items 67/68 are span- or
筆者によると-anchored and item **69 is a 考え/主張 stem in 7 of 7** current papers.

---

## 5. 問題1 — underline and distractors

Underline (rasterised page 1 of 7/2025 and 12/2025, read visually): **the mark
covers the whole word including okurigana and the inflected tail** —
辛い / 収まった / 争って are underlined complete, never 収まった with only 収 marked.
**Corroborates** `question-authoring`'s rule. Two caveats: the typography is the
reproducer's (§0), and **single-kanji whole words are drawn officially** (腕
12/2023-1, 柱 12/2025-1) — those are not "undrawable single-kanji pool entries",
they are words that happen to be spelled with one kanji.

Distractors, all 35 current-era items classified:

| target type | n | what the distractors are |
|---|---|---|
| **訓読み** (okurigana printed, or single-kanji word) | 12 | **real words, every option, no exception.** Same word class and conjugation as the key (争って → all four are 五段 ～って), and usually the same semantic field (柱 → ゆか/かべ/たな; 幼い → するどい/かしこい/しつこい; 外れて → みだれて/やぶれて/つぶれて). Distractors frequently do **not** share the target's kanji. |
| **音読み compound** | 23 | predominantly **non-words**: 清濁 (さいのう→ざいのう), 長短 (きしょう→きしょ), ん⇄う (のうやく→のんやく) manipulations of the key's own on-reading. |

**The other pass's July-2025 conclusion is CORROBORATED, with one refinement**:
roughly 5 of 23 音読み sets deliberately mix in **real homophone words** —
握手 → 拍手, 討論 → 議論, 実践 → 実験, 刑事 → 検事/幹事, 衣装 → 以上 — and one set
(7/2024-2 分析 → 分解/分節/分割) is **four real compounds**. So "音読み distractors
must be non-words" would be as wrong as "all four options must be dictionary
words". The invariant is directional: **a 訓読み set may never contain a
non-word; a 音読み set may, but only as a derivation of the key's own reading.**

---

## 6. 問題12 / 問題14 — stem formulas

**問題12 (A/B, 2 items) is near-formulaic** across all 7 current papers:
item 65 asks what A and B have **in common** (「A と B が共通して述べていること」)
or how each 述べている; item 66 asks how the two **differ** in advice or stance
(「A と B はどのようなアドバイスをしているか」/「どのように述べているか」).

**問題14: 70 and 71 are BOTH person-scenario items in 7 of 7 papers.** Not one
uses 「このお知らせの内容と合っているものはどれか」. **Fully corroborates** the
repo's rule. Observed constraint counts for the key: always ≥2 cells, commonly
3 (7/2025-71 combines 受付期間終了 + 開始3日前まで + 電話のみ; 12/2024-70 combines
room type + bath + 朝食付きプラン + Sunday rate). Typical shapes: a named person
with 2–3 requirements → which option/course/room; and a named person on a given
date → what they must do to book, where a footnote exception decides.

---

## 7. 文法 — 問題7 / 問題8 / 問題9

**問題7 stems (JP chars), last 15 sittings, n = 180:**
mean **43.1**, median **39**, min **17**, max **103**.
Deciles: 25 / 29 / 32 / 35 / 39 / 44 / 50 / 58 / 67.
**38 of 180 stems (21%) are under 30 chars; 17 (9%) under 25; 3 under 20.**
Per-paper averages in the current era: 36 / 48 / 39 / 51 / 43 / 38 / 43 — min 36.

**問題8, 64 of 75 items over the last 15 sittings (85% coverage):**

| measure | official band | median |
|---|---|---|
| sum of the four options | **9 – 41** | 20 |
| options ≥5 JP chars, per item | **0 – 4** | 2 |
| longest option | 3 – 13 | 7 |
| assembled (stem + 4 options) | **30 – 78** | 47 |

Per-option: **51% of official 問題8 options are under 5 JP chars** (median option
length 4). **Bare adverbs/particles on a card are official practice**, not a
defect: 12/2023-47 「一度」, 12/2024-43 「もう」, 7/2025-43 「もちろん」,
7/2025-44 「珍しく」, plus bare particles/verbs (12/2024-44 「だけ」「する」「して」).
4 of 29 current-era items (14%) carry one.

**問題9 cloze body (title + prose, options excluded), last 15: 393 – 695, median
597.** Current era: 498 / 597 / 695 / 672 / 577 / 674 / 689 — min 498. The 393
outlier is 7/2021. Four blanks in every sitting since 12/2020.

**問題6 用法 option sentences: mean 25.0 JP chars, median 25, range 9 – 35**
(current era, n=136; last 15 gives mean 25.3). `question-authoring`'s stated
「~27」 is a mild over-estimate, and the real news is the floor: a 9-char option
sentence is official, so a short one is not by itself a defect.

---

## 8. Answer-key positions — the 19–27 band is exactly the modern envelope

From the official key PDF. Counting the **90 four-choice items** (all 101 minus
聴解問題4's 11 three-choice items):

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

- **All 9 modern sittings satisfy 19–27 per position, and the observed range is
  exactly 19–27** — the band is the empirical envelope with zero margin.
  **Corroborated; keep it.**
- Pooled modern share: **23.4% / 25.5% / 26.7% / 24.3%.** Position 3 is the
  modal key and position 1 the rarest — official is *not* uniform, so a sampler
  forcing 22/23/22/23 would be less official than the band.
- Over all 31 sittings the envelope widens to 19–29 and 4 sittings (7/2010,
  7/2012, 7/2015, 7/2016) fall outside 19–27 — all pre-2017.
- 聴解問題4 (11 three-choice items) is near-uniform, 2–7 per position, typically
  4/4/3.

---

## 9. Constants in `tools/check_consistency.py` that do NOT survive the archive

Each row: the current constant, what the official papers actually do, and a
recommended value. **This pass did not edit `check_consistency.py`** — another
pass owns it.

| Constant | now | five-/seven-paper reality | verdict | recommend |
|---|---|---|---|---|
| `DOKKAI_FLOOR[10]` | 1150 | current-era min **1143** (12/2023) | **FAILS** an official paper by 7 chars | **1100** |
| `DOKKAI_FLOOR[11]` | 2250 | current-era min 2449 | survives (era-specific: pre-12/2022 ran 1778–2179) | keep **2250**, note it is only valid for the 4-passage format |
| `DOKKAI_FLOOR[12]` | 510 | current-era min 532 (last 15 min 495) | survives current era | keep **510** |
| `DOKKAI_FLOOR[13]` | 900 | current-era min **814** (12/2022), **817** (7/2024) | **FAILS 2 of 7** | **800** |
| `DOKKAI_FLOOR[14]` | 560 | current-era min **489** (12/2025), **504** (12/2024) | **FAILS 2 of 7** | **450** in JP chars — or switch this one section to all-char counting and floor at **620** (all-char band 676–793) |
| `DOKKAI_PASSAGE_FLOOR[10]` | 200 | current-era min **157** (12/2023 p5); 171/187/191 in 7/2021, 12/2021, 12/2020 | **FAILS** | **150** |
| `DOKKAI_PASSAGE_FLOOR[11]` | 400 | current-era min 507 | survives | keep **400** (raise to 450 only if the 4-passage format persists) |
| gloss WARN floor (`notes >= 15`) | 15 | current-era band **27–61**, median 39; 30 of 31 sittings ≥17 | far too low — every under-glossed paper passes | **25**, matching `question-authoring`'s new target |
| `P7_STEM_MIN` | 30 | **21% of 180 official stems are under 30**; min 17 | **FAILS heavily** — 12/2022 alone has 5 stems under 30 | drop the per-stem FAIL to a WARN, or lower to **20**; the paper-level rule is the real one |
| `P7_PAPER_AVG_MIN` | 35 | current-era averages 36–51, last-15 mean 43.1 | survives (12/2022 at 36 is 1 above) | keep **35**; author to **43** |
| `P9_PASSAGE_MIN` | 450 | last-15 min **393** (7/2021); current-era min 498 | survives the current era, fails 7/2021 | keep **450** (author to ~600) |
| `P8_OPT_SUM_MIN` | 16 | official band **9–41**, median 20; **13 of 64** measured items are under 16 | **FAILS 20% of official items** | **9**, or drop the per-item FAIL and gate the paper median at ~18 |
| `P8_LONG_OPTS_MIN` | 2 | official band **0–4**, median 2; **24 of 64** items have fewer than 2 | **FAILS 38% of official items** | **0** (i.e. retire), or WARN only |
| `P8_ASSEMBLED_MIN` | 45 | official band **30–78**, median 47; **10 of 29** current-era items under 45 | **FAILS 34%** | **30** |
| `LONG_KEY_MIN` = 50, `LONG_KEY_RATIO` = 1.7 | | 138 keyed 読解 options measured: longest key **61** chars, highest key/mean ratio **1.55**; **0 official items trip the pair** | **survives — no false positive on 7 official papers** | keep |

### Two more repo facts the archive contradicts

- **`question-authoring`'s 読解 length table and `check_consistency.py`'s
  docstring give different numbers for the same paper.** The table says July
  2025 = 1328/2569/617/1055/702; the gate's docstring says 1274/2503/572/1005/622;
  this pass measures 1249/2451/572/989/604 (JP) and 1348/2604/572/1042/793
  (all-char). Three numbers for one paper means at least two measurement
  methods are undocumented. Fix by naming the method next to the number.
- **「keep all four 読解 options within ±40% of each other」** — 133 of 140
  current-era items (95%) satisfy max/min ≤ 1.8, so the rule is *mostly* right,
  but official ships items at 2.10 (12/2025-66) and 2.09 (12/2023-65), and 29%
  of official keys are the longest of their four options. State it as a target
  with the measured 95th percentile, not an invariant.
- **「問題1 の 4 択はすべて実在語」 / 「音読みは非語」** — neither is universal; see §5.
- **「no bare adverb on a 問題8 card」** — contradicted; see §7. The real
  invariant is single-solution uniqueness, which a bare adverb endangers but
  does not by itself violate.
- **「問題11 の各パッセージは事実把握1+考え1」** — contradicted by 6 of 7 current
  papers; see §4.

---

## 10. Web cross-check (official sources)

| Fact | Official source | Archive agrees? |
|---|---|---|
| N2 = 言語知識(文字・語彙・文法)・読解 105 min + 聴解 50 min | [jlpt.jp/e/guideline/testsections.html](https://www.jlpt.jp/e/guideline/testsections.html) | n/a (not measurable from PDFs) |
| 3 scoring sections 0–60 each, total 0–180, sectional cutoff **19**, overall pass **90** | [jlpt.jp/e/guideline/results.html](https://www.jlpt.jp/e/guideline/results.html) | matches `exam-answer-grading` exactly |
| 大問 names and ねらい; 問題10 = 200字程度, 問題11 = 500字程度, 問題12 = 合計600字程度, 問題13 = 900字程度, 問題14 = 700字程度 | [jlpt.jp/guideline/pdf/n2.pdf](https://www.jlpt.jp/guideline/pdf/n2.pdf) (current revision — **no 小問数 column**) | 問題12/13/14 match; 問題11 passages run ~30% long; 問題10 passages sometimes short |
| 2009 小問数 目安: 5/5/5/7/5/5/12/5/5/5/9/2/3/2 + 聴解 5/6/5/12/4, with the footnote that it is a 目安 「変更される場合があります」 | [jlpt.jp/reference/pdf/guidebook1e.pdf](https://www.jlpt.jp/reference/pdf/guidebook1e.pdf) p.21 | matches 2010–2018 exactly; current papers are 5 items lighter |
| Official N2 sample listening script: 問題1 speaks the 問い **before** the dialogue and **repeats it after**; speakers labelled M/F | [jlpt.jp/samples/pdf/N2-script.pdf](https://www.jlpt.jp/samples/pdf/N2-script.pdf) (image PDF, rasterised) | matches the three full archive scripts |

**No contradiction was found between jlpt.jp and the archive.** The one apparent
conflict — published 小問数 vs. actual item counts — is resolved by JEES's own
footnote calling the counts a 目安, and by the current PDF having dropped them.
Non-official sites were not used for any number in this file.

---

## 11. `AGENTS.md` §3 describes the archive (`refs/JLPT_N2_NEW/`)

`AGENTS.md` §3 describes `refs/JLPT_N2_NEW/` holding **31 sittings**, and `make check` asserts those paths exist:

> - **Official Past Exam Archive (`refs/JLPT_N2_NEW/`) — 31 sittings, 7/2010 – 12/2025.**
>   One directory per sitting, named `<n>. N2 <month>-<year>/`, each holding the
>   booklet PDF, the listening script PDF, and the listening MP3. The official
>   answer keys for **all 31 sittings** are in
>   `refs/JLPT_N2_NEW/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf`.
>   **Calibrate against the band measured in
>   `.agents/reference-book-reading/references/official_calibration.md`, not
>   against a single paper.** The current exam format (71 + 30 items, 問題11 in
>   four passages) dates from **12/2022**; earlier sittings are a different
>   blueprint and must not be averaged in for 読解 lengths.

---

## 12. 問題5/問題6 katakana-headword rate — the pool over-draws it 5–7×

Measured by reading every 問題5 (言い換え類義) and 問題6 (用法) item's TESTED
HEADWORD across the current-era archive (n = 35 items each; 12/2022, 7/2023,
12/2023, 7/2024, 12/2024, 7/2025, 12/2025), classifying the headword itself as
katakana or kanji/wago (a katakana word appearing only among the four options,
never as the tested word, is recorded separately — it is a register choice on
the distractor set, not a pool draw).

| 問題 | katakana HEADWORD | all-options-katakana (headword is wago) | zero katakana anywhere |
|---|---|---|---|
| 5 (n=35) | **3 (8.6%)** — 12/2022-21 テクニック, 7/2023-22 テンポ, 12/2024-21 ガイド | 2 (5.7%) — 7/2024-22 行儀→アイディア/サービス/マナー/イメージ, 12/2025-22 題→デザイン/アイデア/ストーリー/タイトル | 30 (85.7%) |
| 6 (n=35) | **1 (2.9%)** — 12/2022-29 ベテラン | n/a (問題6 options are sentences, not a word list) | 34 (97.1%) |

- **Combined headword rate: 4/70 (5.7%).** Only 12/2022 drew a katakana
  headword in BOTH sections of the same paper; 6 of the 7 sittings drew **zero**
  katakana headwords across 問題5+問題6 combined.
- **`references/pools.json`'s `paraphrase` pool is 27.1% katakana-containing
  (38/140) and `usage` is 32.7% (49/150)** — 3–6× the measured official rate.
  `sample_items.py`'s `draw()` is a plain `rng.sample()` with no
  script-awareness, so an unweighted 5-item draw from either pool has an
  ~27–33% expected katakana share per item — close to **5 combined katakana
  headwords per paper in expectation**, against an official average of 0.57.
  Three generated papers checked (`tests/20260807_1`, `20260810_1`,
  `20260810_2`) drew 3, 3 and 6 combined katakana headwords respectively —
  averaging 4/paper, ~7× the official rate, and never once resembling the
  official "usually zero" shape.
- **Root cause is the draw, not the writing.** The pool's katakana share was
  never capped against measured official behavior; a uniform random sample
  reproduces the pool's composition, and the pool's composition does not match
  the archive.
- **A second, separate finding while reading the pool**: several `paraphrase`
  and `usage` katakana entries (バケツ, ダム, ハンドル, ピストル, ビタミン,
  マラソン, モーター, ロビー, ボーナス, ランチ, ランニング…) are concrete,
  everyday loanwords that read as N3/N4 vocabulary under the golden rule
  ("would this appear in an N3 book?") — `references/openjlpt` labels them
  `N2`, but that corpus is a legacy 2級 word list and mislabels in both
  directions (`question-authoring/references/moji-goi.md` §"KEY must be N2"
  already warns of the opposite mislabel, N2 words tagged N1). This pass did
  not purge the pool — it only measured the ratio and fixed the draw (§ below,
  `exam-blueprint/scripts/sample_items.py`'s `KATAKANA_CAP`) — a follow-up pass
  should re-run the openjlpt/Shin-Kanzen band check on every katakana pool
  entry the same way `kanji_reading` was audited (exam-blueprint §"Pool
  entries stay inside the N2 band").

## 13. 問題8 register mix — official skews personal/casual, generated skews corporate/formal

Classified every current-era 問題8 stem's setting/register (n = 35; same 7
sittings as §12) into **personal/casual** (family, friends, first-person daily
life, casual dialogue quotes), **neutral/factual** (trivia, weather, plain
description, no institutional actor), or **formal/institutional** (workplace
policy, business, administrative notice, scientific/technical exposition):

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

- **Personal/casual is the majority register in every sitting, and two of the
  seven sittings (12/2024, 12/2025) ship ZERO formal/institutional 問題8
  items** — the format tolerates an all-personal paper but not an
  all-institutional one; no sitting exceeds 2 of 5 formal/institutional items.
- The same 3 generated papers checked in §12 skew the other way: **11 of 15
  items (73%) are corporate/formal** (契約書 negotiation, system procurement,
  personal-data policy, price negotiation, workplace manuals, project
  outcomes), **2 (13%) personal/casual**, **2 (13%) neutral**. One paper
  (`20260807_1`) is 5/5 formal/institutional — a shape that never occurs in the
  7-sitting archive.
- **This is a register/scene variance finding, not a grammar-band finding** —
  every generated item's grammar point is still correctly N2 (per
  `level_band_grammar.txt`); the reported "問題8 feels uniformly hard" comes
  from every item sharing one dense, abstract, institutional register, where
  official papers mix in plain first-person narrative and casual dialogue that
  reads easier at equal grammatical difficulty. The fix is a register-mix rule
  in `question-authoring/references/bunpou.md` §問題8, not a change to which
  grammar forms are drawn.
