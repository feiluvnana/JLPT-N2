# 読解 audit — 14 generated papers vs 31 official sittings vs Shin Kanzen N2 読解

Date: 2026-08-20. Read-only analysis; nothing on disk was changed.

**Status, 2026-08-25 — the remediation plan is consumed on the authoring side.**
All 14 generated papers have had their reading half repaired (commits
`d19fb20`…`2f3c48a`). Every 読解 axis `tools/check_consistency.py` measures is
now inside its band on every paper: kanji density, median sentence length and
short-sentence share, polite and first-person voice, span-anchored and 指示語
stem counts, section and per-passage lengths, 問題10 apparatus INTENT stems and
考え share, overlap direction (key − best distractor), key rank spread,
longest-key share, closing-move variety, （注N） counts, 問題6 option and 問題7 stem
bands, 問題9 option-set reuse, and keyed-form exposure in the passage prose. Two
gate defects were found and fixed while doing it, both recorded in
`check_consistency.py`'s own docstrings: `passage_prose` counted the 大問
instruction line as prose (making KEY_EXPOSURE_MAX unsatisfiable for any paper
keying 「として」), and a missing 「## 読解」 heading made `dokkai_profile` default
every 読解 key to 1 and report overlap/key-rank numbers against answers it had
never read (`check_dokkai_key_table_parses` now FAILs on that).

**Still open** (tracked in `logs/dokkai_remediation_state.json`): the P5Q
fresh-eyes blind solves — `exam-qa-review` is owed on every repaired paper and
must run in a context that authored nothing; P6; P7.4; and the draw-level
warnings a prose edit cannot reach (a 問題7↔問題8 grammar form inside its cooldown
on eight papers, 20260814_1's two repeated headline themes, and its 問題14 sharing
its decisive number with a 聴解 item — those need `--reroll` or a 聴解 rewrite).

**Corpora actually opened**

| Corpus | What was read | n |
|---|---|---|
| Generated | `tests/*/言語知識・読解.md`, 問題10–14 region (passages, prefaces, （注N）, stems, options, `## 読解` key table) | 14 papers, 182 surfaces, 280 keyed items |
| Official | `refs/JLPT_N2_NEW/*/booklet.md` (text-layer extracts) + `answer_keys.json` | 31 sittings; **7 current-era** (12/2022–12/2025) carry every format-dependent number: 138 keyed items, 126 four-option 問題10–13 items |
| Shin Kanzen | `Shin_Kanzen_Masuta_N2-Dokkai.pdf` — 目次, 「本書をお使いになる方へ」, 第1部 pp.2–3, and the **模擬試験 (p.181+)**, a complete typeset N2 読解 paper | 1 book, 238 pages |
| Repo rules | `AGENTS.md`, `question-authoring/SKILL.md` + `references/dokkai.md` + `references/official_calibration.md`, `jlpt-exam-structure`, `exam-qa-review`, the 読解 half of `tools/check_consistency.py` | — |

**Three corpus facts worth recording before the findings**

1. **`Shin_Kanzen_Masuta_N2-Dokkai.pdf` is cited nowhere in this repo.** `AGENTS.md` §3 lists it; a grep for `Dokkai` across `.agents/`, `tools/` and `AGENTS.md` returns only the app's score-section identifier and the Goi/Kanji volumes that `dokkai.md` §（注N） cites for the gloss band. So every 読解 authoring rule was derived from the official archive alone — and the one N2 reading textbook in `refs/` carries exactly the taxonomy the findings below say has drifted (§F11).
2. **The file is 109 MB, over the 100 MB PDF read cap**, so it cannot be opened with the pages parameter directly. Split it first (`pypdf` → ≤10-page chunks in the scratchpad) and read the chunk; the scan is clean and fully legible that way. Same class of mechanic as the choukai 別冊 discovery — record it or the next agent concludes the book is unreadable.
3. **The official `booklet.md` extracts carry inline furigana as separate lines** (「…映す 鏡 / かがみ / 」といいます」). My parser drops a short all-hiragana line that follows a kanji-final line. Counts below are sound; individual character strings from the official side are illustrations, never quotable wording (`reading-reference-pdfs.md`).

`make check` is currently **RED — 1 FAIL, 139 WARN** (the FAIL is `20260819_1`'s 詳細解説.json option drift, a 聴解 item, unrelated to this audit). Every finding below except parts of F2, F5 and F10 is invisible to it.

---

## Summary — the shortcomings, ranked

| # | Finding | Measured | Gated today? |
|---|---|---|---|
| F1 | **Surface overlap points at the key**: an examinee who cannot read Japanese and picks the option sharing the most character bigrams with the passage scores **60.3%** | official 32.8%, chance 25%; the key out-overlaps its best distractor in **9 of 14** papers and in **0 of 7** official ones | no |
| F2 | **The key is the SECOND-longest option in half our items** | 48.8% vs official 29.5%; 6 papers beyond the archive's worst single paper — and the `≤1.30` clamp that caused it is a FAIL that **40.5% of official items breach** | gated backwards |
| F3 | **The passages have no essay voice** | です・ます share in essay passages: median **0.0%** vs official 32.1% (10 of 14 papers zero); first-person 37% vs 80%; kanji density 35.5–41.7% vs official 25.1–29.8% — **no overlap** | no |
| F4 | **問題14 asks a generic truth-check where official asks a computed value or an action** | 19 of 28 items 「〜について、正しいものはどれか」 vs **0 of 12** official | no |
| F5 | **The four banned retrieval shapes are gated in 問題11 only** — three are live on disk in 問題10/問題13 | `20260807_1` 問10-53, `20260814_1` 問10-56 + 問13-68; the whole truth-check family is **28 of 280** items vs **0 of 138** | scope bug |
| F6 | **Span over-anchoring**: 「とあるが」 5–7 per paper against a current-era official median of **0** | ours median 5.5, official cur 0.86/paper (4 of 7 sittings zero) | hygiene only, never the rate |
| F7 | **One-sided length bands**: 問題10 runs 17% over the official ceiling | ours median 1434, official band 1143–1329; 9 of 14 papers above official max; per passage 278 vs 232 | floors only |
| F8 | **Sentence rhythm is uncalibrated and swings** | per-paper median sentence 28–73 JP chars vs official's tight 35–42 | no |
| F9 | **問題10's dominant official shape is a fifth of ours**, and the notice/email items ask content instead of intent | 筆者の考え-family 46% official vs 33% ours; intent-shape apparatus stems **10 of 11** vs **4 of 23** | no |
| F10 | **The ※-exception notice is a house style** | ※ 5–16 per paper vs official 0–3; absolute-quantifier options 5.0% vs 1.6% | WARN (quantifiers only) |
| F11 | Shin Kanzen's 読解 taxonomy, 模擬試験 and 別冊 are unused and undocumented | see above | — |

---

## F1 — surface overlap points at the key, and that is the whole section

**The measurement.** For every four-option 問題10–13 item I ran five strategies that require no Japanese at all, against the item's OWN passage. Chance is 25%.

| blind strategy | official (n=122) | generated (n=252) |
|---|---|---|
| pick the longest option | 26.2% | 21.8% |
| pick the **second**-longest option | 24.6% | **49.2%** |
| pick the shortest option | 23.0% | 16.3% |
| pick the option with the longest common substring with the passage | 27.0% | **46.4%** |
| **pick the option sharing the most character bigrams with the passage** | **32.8%** | **60.3%** |

Strictly (ties excluded — "the key's overlap is strictly higher than every distractor's"): official 30.3%, ours **59.5%**.

**The direction is the point, and it is a bright line.** Per paper, the median of
(key overlap − best distractor's overlap):

| official sitting | strict top-overlap share | median margin |
|---|---|---|
| N2 7/2025 | 11% | **−0.100** |
| N2 12/2025 | 17% | −0.082 |
| N2 12/2022 | 28% | −0.056 |
| N2 12/2023 | 38% | −0.055 |
| N2 7/2023 | 38% | −0.074 |
| N2 12/2024 | 39% | −0.052 |
| N2 7/2024 | 44% | −0.021 |

| generated paper | strict top-overlap share | median margin |
|---|---|---|
| `20260810_1` | 78% | **+0.156** |
| `20260814_1` | 83% | +0.142 |
| `20260812_2` | 61% | +0.116 |
| `20260817_2` | 78% | +0.102 |
| `20260811_1` | 67% | +0.087 |
| `20260817_1` | 72% | +0.087 |
| `20260810_2` | 83% | +0.078 |
| `20260817_3` | 61% | +0.061 |
| `20260812_1` | 50% | +0.007 |
| `20260813_2` | 44% | −0.005 |
| `20260813_1` | 44% | −0.027 |
| `20260818_1` | 39% | −0.031 |
| `20260819_1` | 44% | −0.041 |
| `20260807_1` | 28% | −0.067 |

**Every official paper is negative; nine of fourteen generated papers are positive.**
Pooled, official −0.079 against generated +0.053.

Official keys share **less** surface with the passage than their strongest distractor. That is not an accident of style: it is what happens when distractors are built out of passage material (so they are attractive) and the key is written as a paraphrase (so it is not findable by matching). Our papers do the opposite — the key is paraphrased *from the sentence it answers*, so it keeps that sentence's vocabulary, while distractors are invented from outside the passage and share less.

Five papers are already on the right side of zero — `20260807_1` (the oldest),
`20260813_1`, `20260813_2`, `20260818_1`, `20260819_1` — and the worst are in the
middle of the corpus. So this is not a drift with a direction; it is an axis nobody
measures, wandering. Two of the three most recent papers are negative, which is the
strongest argument that the fix is reachable by authoring discipline alone.

**Why it matters.** `dokkai.md` §2 already forbids verbatim lifts and gates them (LCS ≥15 chars and ≥50% of the key, or ≥20 chars). That check measures **one contiguous span**. Overlap does not need to be contiguous to be visible: 「支援策を増やす前に、申請に要する手間の多さを見直す」 shares 支援策/申請/手間/見直 with its passage without a single 15-character run. The rule is satisfied, and the tell survives.

**Fix.** Owner: `question-authoring/references/dokkai.md` §"読解 keys". The rule to add is directional and countable: **a paper's median (key − best distractor) overlap margin must be ≤ 0 — the line every official paper clears — and distractors must be built FROM passage material** (a true clause with one fact changed, official's own construction — the same move `dokkai.md` §問題14 already demands for the flyer, generalised to 問題10–13). Gate line: a paper-level `check_dokkai_overlap_direction` (§Phase 3), because this is a distribution, not an item defect.

---

## F2 — the key is the second-longest option, because the rule said "not the longest"

**Measurement**, four-option 問題10–13 items, key rank by JP-char length (rank 1 = strictly longest):

| key rank | official (n=126) | generated (n=252) |
|---|---|---|
| 1 (strictly longest) | 28.7% | 24.6% |
| **2** | 29.5% | **48.8%** |
| 3 | 27.0% | 14.7% |
| 4 | 14.8% | 11.9% |

The uniquely-longest rate itself is fine — ours 19.0%, official 23.0%, both inside `dokkai.md`'s 20%/30% band. The *rest* of the distribution moved: ranks 3 and 4 emptied into rank 2.

**Per paper, and this is where a threshold has to be set carefully.** The largest share
any one rank takes, over each paper's 18 four-option items: official 33/39/**56**/39/44/33/44%
— its worst paper (7/2023) puts 10 of 18 keys at rank 2 all by itself. Generated:
`20260813_2` **78%**, `20260810_1` **72%**, `20260812_1` **72%**, `20260811_1` **67%**,
`20260807_1` **61%**, `20260814_1` **61%**, `20260812_2` 56%, `20260810_2` 50%, then
`20260813_1`/`20260819_1` 39% and four papers at 33%. So **six papers sit beyond the
archive's worst single paper**, and any per-paper gate must sit above 56% or it fails
an official one — the corpus-level 48.8% vs 29.5% is the finding, the per-paper line is
where the gate goes.

**Where it came from is written in the gate's own comment.** `check_dokkai_option_length_balance`'s docstring records the 2026-08-17 audit: the key was the longest in 73.5% of items (58.5% strictly), so the repo added "a hard per-item cap at max/min ≤1.3, FAIL not WARN … stricter than the official archive on this one axis, on purpose." It worked on the axis it measured. Inside a ±30% band, "a hair shorter than exactly one distractor" is the next available tiebreak, and that is where the keys went.

**And the cap itself does not survive the archive.** Same parse, both sides:

| max/min over the four options | official cur | generated |
|---|---|---|
| median | 1.26 | 1.18 |
| p90 | 1.61 | 1.27 |
| max | 4.29 | 1.32 |
| **share above 1.30 (the FAIL line)** | **40.5%** | 0.4% |
| mean option length (JP chars) | 26.3 | 32.7 |

`official_calibration.md` §9 audits fifteen gate constants against the archive and **this one is not among them** — it was set from a generated-paper audit, never checked against an official paper. A gate line that fails two of every five official items is the shape `AGENTS.md` §0 calls a defect: "a floor that rejects an official paper is a wrong floor," and the same logic applies to a ceiling.

**Fix.** Owner: `dokkai.md` §"読解 keys — unpredictable option lengths". Replace the per-item clamp with the archive's envelope plus a paper-level rank spread:

- per item: max/min **WARN above 1.65** (official p90 1.61), FAIL only above the archive max;
- per paper: **no key rank may take more than 40% of the items** (official worst 29.5%), and the uniquely-longest band stays as it is;
- the repair direction stays "lengthen a distractor with a passage-groundable clause," never "trim the key" (§F1 — trimming a key is how a paraphrase collapses back onto the passage's wording).

---

## F3 — the passages have no essay voice

Official 読解 passages are excerpts from published essays and books: first-person, half of them addressed to the reader in です・ます, with quoted speech. Ours are impersonal policy prose.

**Measurement, essay-type passages only** — the 問題10 notice/email items and 問題14 are excluded, so the comparison is essay-to-essay (n=64 official, 142 generated):

| | official cur | generated |
|---|---|---|
| です・ます share of sentence endings, median | **32.1%** (22.4–46.3%) | **0.0%** (0.0–11.3%) |
| papers with zero polite sentences in any essay | 0 of 7 | **10 of 14** |
| passages containing 私/僕/自分 | **80%** | 37% |
| kanji share of JP chars (問題10–13) | 25.1–29.8%, med 28.1% | 35.5–41.7%, med **37.3%** |
| institutional lexis per 10k chars (市/自治体/制度/窓口/社員/研修…) | 7–17, med 10 | 20–107, med **42** |
| personal lexis per 10k (私/母/友人/子ども/思い出…) | 4–51, med 33 | 6–44, med 13 |
| quoted speech 「…」 per 10k | 21–51, med 25 | 2–32, med 8.5 |
| rhetorical 〜だろうか/〜ではないか per 10k | 1–7, med 5 | 0–4, med 0.5 |
| colloquial んです/でしょう/ですね per 10k | 0–13, med 10 | 0–1, med 0 |

**The kanji band does not overlap.** Not one generated paper is inside the official range, and not one official paper is inside ours. That single number is most of the "読解 feels harder than the real thing" complaint: a 37% kanji density is the density of a 白書, not of the essays JEES excerpts.

**Corroboration from the third corpus.** Shin Kanzen's 模擬試験 passages are attributed excerpts (香山リカ『若者の法則』岩波書店, 脇明子『読む力は生きる力』岩波書店). The B half of its A/B pair runs entirely in です・ます (「シリーズものというのは、だれにとっても誘惑的な存在です」); its 長文 is first-person with quoted dialogue. The textbook's 第1部 is titled 評論・**解説・エッセイ**など — three registers, and we write one.

**Topic tagging agrees, weakly.** Keyword-tagging the 196 reading surfaces recorded in `logs/topics.json`: 自治体/行政/制度 22%, 職場/企業 9%, 個人/生活/随筆 **3%** (5 surfaces in 14 papers). 41% of labels did not tag, so treat this as corroboration of the register measurement above, not as its own evidence.

**Why it matters.** Register is not decoration. Official 問題10 keys on 「筆者はどのように考えているか」 for essays written in the first person, where the reader has to separate the author's stance from what the author reports. A third-person policy paragraph has no stance to separate — which is exactly why our 問題10 drifted to content questions (§F9) and our keys drifted onto the passage's own words (§F1). One register produces one question type produces one key shape.

**Fix.** Owner: `dokkai.md` §"What a 読解 section is" (the passage inventory) and `exam-blueprint` Part II (which assigns the topic). Add a **voice quota** to the thirteen-surface table, countable with the regexes above:

- **≥4 of the 12 essay-type surfaces are first-person** (私/僕), and **≥3 carry です・ます throughout** — official 80% and 32%; ours 37% and 0%.
- **kanji density per paper in 24–32%** — the archive's band with headroom, measured over 問題10–13 passage prose.
- ≥1 passage carrying quoted speech; ≥1 carrying a 疑問提示文 (Shin Kanzen 第1部 device 4, §F11).

---

## F4 — 問題14 asks a generic truth-check; official asks for a value or an action

**Measurement**, all 問題14 stems, classified by what the stem asks for:

| what the stem asks | official (n=12) | generated (n=28) |
|---|---|---|
| a **value** (料金はいくらになるか / 何を用意すべきか / どの書類か) | 42% | 4% |
| an **action** (どうしなければならないか / 予約のしかた / どのように申し込むか) | 42% | 4% |
| a **choice** among printed options (どの講座か / 誰か) | 17% | 25% |
| **generic truth-check** (「〜について、正しいものはどれか」/「適切なのはどれか」) | **0%** | **68%** |

Official, for contrast: 「中村さんたちの運賃はいくらになるか」「ニコラスさんはどのように申し込まなければならないか」「入会時に支払うものは何か」. Ours, from the last eight papers: 「田中さんについて、正しいものはどれか」 — twelve of sixteen items.

**Both rules the repo wrote are satisfied.** `dokkai.md` §問題14 requires 70 and 71 to be person-scenario items (28 of 28 are) and bans the literal 「このお知らせの内容と合っているものはどれか」 for item 71 (no paper does that in 問題14). Naming a person in front of a truth-check satisfies both while asking the generic question anyway — and `check_mondai14_quotes` reads the 解説's two quoted cells, not the stem, so the gate confirms two constraints were *used* and never notices that the question was "which of these four sentences is true."

**Why it matters.** 情報検索 tests locating and combining printed conditions to produce an answer. "Which statement is true" turns that into four independent verification passes over the whole flyer — more work, less skill, and it is the one shape the archive avoids in 7 of 7 papers.

**Fix.** Owner: `dokkai.md` §問題14. State the target as **what the answer IS**: a value, an action, or one named option from the flyer — not a proposition to verify. Gate line `check_dokkai_q14_stem_target`: FAIL when both items are the truth-check shape, WARN on one.

---

## F5 — the banned retrieval shapes are gated in 問題11 only, and three are on disk

`official_calibration.md` §4 records that four stem shapes appear **0 times in 15 sittings, in any 問題**: 「本文で述べられている〜はどれか」「〜として正しいものはどれか」「〜の主な目的は何か」「〜の内容と合っているものはどれか」. `dokkai.md` calls them banned. `check_mondai11_stems` FAILs them — reading only 問題11's stems (`P11_BANNED_STEM` is applied inside that function and nowhere else).

Live on disk today:

| paper | item | stem |
|---|---|---|
| `20260807_1` | 問題10-53 | 「このお知らせの**内容と合っているものはどれか**。」 |
| `20260814_1` | 問題10-56 | 「…支援活動の傾向**として正しいものはどれか**。」 |
| `20260814_1` | 問題13-68 | 「…物理的手法の特徴として、**本文で述べられているものはどれか**。」 |

All three are the literal banned strings, in 問題10 and 問題13, with the gate green on that line for both papers. Across the whole corpus the truth-check family (including the 問題14 shape of §F4) is
**28 of 280 items (10.0%) against 0 of 138 official** — `20260813_2` and `20260814_1`
five each, `20260817_1` three, seven papers two each.

**Fix.** One-line scope change plus one addition: run the banned-shape check over **問題10–14**, and add the bare 「正しいものはどれか」/「適切なのはどれか」 to the family — the family exists because it names the shape, and 「として」 is not what makes it retrieval.

---

## F6 — span over-anchoring: five to seven per paper against an official median of zero

**Measurement.** 「とあるが」 per paper (the archive's own marker for a span-anchored stem; it prints the span underlined with a ①-marker and re-quotes it bare in the stem):

| corpus | median | range | papers at 0 |
|---|---|---|---|
| official, all 31 sittings | 1 | 0–5 | 6 of 31 |
| **official, current era (7)** | **0** | 0–3 | **4 of 7** |
| generated (14) | **5.5** | 0–7 | 1 of 14 |

And the buckets it displaced, same classifier both sides (priority: apparatus → span → 考え/主張 → によると → どのように述べ → truth-check → 理由):

| 問題11 stem bucket | official cur (n=56) | generated (n=112) |
|---|---|---|
| span-anchored | 26.8% | **46.4%** |
| 「筆者によると、…」 retrieval | 25.0% | **3.6%** |
| 考え/主張 | 25.0% | 26.8% |

| 問題13 stem bucket | official cur (n=21) | generated (n=42) |
|---|---|---|
| span-anchored | 28.6% | **47.6%** |
| 「筆者によると、…」 | 28.6% | **2.4%** |

**指示語 items went with it.** Shin Kanzen 第1部-2 lists 指示語を問う as question type #1 (「それは何を指しているか」), and the archive uses it steadily — official current era **1.57 per paper** (6 of 7 papers carry one: 「それとあるが、どういうことか」「このような工夫とはどのようなことか」「②これとは何か」). Ours: **0.64 per paper, and 8 of 14 papers have none**. Our span anchors are content noun phrases instead, which is the easier object: a demonstrative forces the reader to search backwards, a quoted noun phrase is already the answer's neighbourhood.

**What the repo built instead.** Three gate checks (`check_dokkai_numbered_markers`, `check_dokkai_span_anchor_bold`, `check_dokkai_span_anchor_identity`), a length band (median 8, WARN >25, FAIL >35), a fixed repair direction, and a gloss-outside-the-bold rule — an apparatus for a shape the current-era archive uses less than once per paper. Every one of those checks is *correct*; none of them asks how many spans a paper should have. And the band behind them mixes eras: the 55 measured spans come from all 31 sittings, where pre-2018 papers ran 4–5 per paper, so the p95 that governs today's authoring was set mostly by a format that no longer ships.

**Fix.** Owner: `dokkai.md` §"Marked-span quoting" (rate) + `jlpt-exam-structure` (the question-form inventory, which today owns instruction lines but not question lines). **≤2 span-anchored stems per paper** (current-era max is 3, all-era median 1), **≥1 指示語 item**, and restore 「筆者によると、〜は何か」 as the default retrieval shape — it is a quarter of official's 問題11 and 問題13 and 3% of ours. Re-derive the span-length band on the current era alone (§D1).

---

## F7 — every length rule is a floor, and 問題10 sits above the official ceiling

Generated numbers measured with the gate's own `passage_prose()` + JP-char class; official numbers from `official_calibration.md` §2, which used the same function. Apples to apples.

| 大問 | official cur (min–max, median) | generated (min–max, median) | papers above the official MAX |
|---|---|---|---|
| 問題10 | 1143–1329, **1225** | 1180–1658, **1434** | **9 of 14** |
| 問題11 | 2449–2685, 2556 | 2331–2703, 2530 | 1 |
| 問題12 | 532–592, 551 | 526–664, 580 | **7 of 14** |
| 問題13 | 814–1061, 904 | 881–1154, 950 | 2 |
| 問題14 | 489–638, 604 | 462–710, 581 | 4 (and 1 below the min) |

Per passage (my parse, both sides): 問題10 official 158/232/326 (min/med/max, n=30) vs generated 178/**278**/385 (n=70) — our median sits above official's p75 (257) and our longest 短文 is 18% past the archive's longest. `dokkai.md` says "author 問題10 to ~240"; the corpus is at 278 and nothing reports it, because `DOKKAI_FLOOR`/`DOKKAI_PASSAGE_FLOOR` are floors.

Options and stems run long too: options 32.7 vs 26.3 JP chars (**+24%**), stems 29 vs 25. Summed across 20 items and five sections, a generated 読解 half is a materially longer read than the paper it is calibrated against — in a section whose real constraint is 105 minutes.

**Fix.** Owner: `dokkai.md` §"Length bands". Make every row two-sided — the table already has "official min / official median / gate floor", so add **gate ceiling** = archive max with headroom, and a per-passage ceiling for 問題10 (≥350 is outside the archive). Extend `check_dokkai_lengths` to FAIL above the ceiling, and add an option-length band (mean per paper 24–30 JP chars).

---

## F8 — sentence rhythm is uncalibrated, and it swings paper to paper

Sentence = span ending 。 inside 問題10–13 passage prose, （注N） definition lines removed, JP chars.

| | per-paper median sentence | range of per-paper medians | share of sentences <25 chars |
|---|---|---|---|
| official cur | 35–42, **median of medians 38.0** | **7-point spread** | 14–27% |
| generated | 28–73, median of medians 43.8 | **45-point spread** | 0–39% |

Per paper: `20260817_1` **73.0**, `20260817_2` 65.5, `20260814_1` 57.0, `20260810_2` 53.0 … `20260818_1` 33.0, `20260819_1` **28.0**. Two papers ship essays whose sentences average nearly twice official's; the newest paper ships essays a quarter shorter, with 39% of its sentences under 25 characters against official's 14–27%.

Both tails are real damage in opposite directions. A 73-character median means one sentence per idea per clause-chain, which is where 「どういうことか」 items become parsing exercises. A 28-character median is the choppy declarative style visible in `20260819_1` 問題10(1) (「刈られた土手は歩きやすく、見通しもよい。」) — each sentence carries one fact, so the passage becomes a list and the question becomes a lookup. Official's stability (35–42 across 7 sittings, seven years) is not an accident; it is the register of published essay prose.

**Fix.** Owner: `dokkai.md` §"Length bands" (same section, since it is the same authoring pass). **Median sentence length per paper 33–43 JP chars, and share of sentences under 25 chars in 12–30%.** Gate as WARN outside, FAIL outside 28–50 — the archive's whole range with headroom. It is one regex and it makes both tails visible while drafting.

---

## F9 — 問題10's dominant official shape is a fifth of ours, and the apparatus items ask the wrong thing

**問題10 stem buckets**, same classifier as §F6:

| bucket | official cur (n=35) | generated (n=70) |
|---|---|---|
| 考え/主張 (筆者の考えに合う / 言いたいこと) | 28.6% | 11.4% |
| どのように述べ/考え | 17.1% | 21.4% |
| **the two together — "what does the author think"** | **45.7%** | **32.9%** |
| — of which the apparatus stems asking **intent** | 10 of 11 | **4 of 23** |
| apparatus (この お知らせ/メール/文書 …) | 28.6% | 32.9% |
| によると retrieval | 5.7% | 11.4% |
| truth-check | 0% | 2.9% |

**The apparatus items are the sharper half.** Official's notice/email items ask for the document's *intent* — 「このお知らせで伝えたいことは何か」「このメールで問い合わせていることは何か」「このメールの用件は何か」: **10 of its 11** apparatus stems (the eleventh asks an action; none asks content). Ours ask for its *content* — 「このお知らせによると、…は何か」「このお知らせから分かることは何か」「このお知らせによると、…正しいものはどれか」: 4 of 23 use the intent shape. Intent requires reading the whole notice and deciding what it is FOR; content is a lookup, and a lookup on a notice is where the ※-exception trap (§F10) comes from.

**Fix.** Owner: `jlpt-exam-structure` gains a §"問題10–13 question-form inventory" (it owns instruction lines today and no question lines at all — the same gap the choukai audit found for 問題1), with the archive's shares; `dokkai.md` §"What a 読解 section is" gains the quota: **≥2 of 5 問題10 items on the 筆者の考え family, and every notice/email item asks intent, not content.**

---

## F10 — the ※-exception notice is a house style, not an official one

| | official cur | generated |
|---|---|---|
| ※ characters in 問題10–14 | 0–3 per paper (0 in 3 of 7 sittings) | **5–16, median 9** |
| options carrying an absolute quantifier / categorical denial (すべて・のみ・まったく・必ず・一切…) | 9 of 552 (**1.6%**) | 56 of 1120 (**5.0%**) |

`dokkai.md`'s passage inventory *prescribes* "one notice with 3 false options contradicted by ※ fine print", and 問題14 adds a footnote-decided item on top, so a compliant paper ships two ※-trap surfaces minimum; the corpus ships four to eight. The archive's notices carry their exceptions in prose.

The quantifier line is more nearly fixed than it looks: the three newest papers (`20260817_3`, `20260818_1`, `20260819_1`) are at **zero**, against 9–11 in `20260813_1` and `20260817_1`. The WARN worked. The ※ count has no rule at all.

**Fix.** Owner: `dokkai.md` §"What a 読解 section is". Cap ※ at **≤3 per paper** (the archive's max) and rewrite the passage-inventory line: a notice's exceptions may be prose, and the "3 false options contradicted by ※" recipe is one option among several, not the shape of the item. Keep the quantifier WARN as is — it is working.

---

## F11 — Shin Kanzen's 読解 taxonomy, 模擬試験 and 別冊 are unused

The book in `refs/Shinkanzen/` carries, in clean typeset Japanese:

- **第1部-1 「文章のしくみを理解する」 — five discourse devices**: 1) 対比 2) 言い換え 3) 比喩 4) **疑問提示文** 5) 主張表現. This is the standard taxonomy for how an N2 passage is built, and it is what a passage-authoring brief needs. `dokkai.md` instead uses a home-made "six closing moves" list (主張/説明/意外な観察/反論応答/随筆/条件提示) with a ≤2-per-shape cap and two gate checks behind it. The home-made list is defensible — but it classifies **endings**, and the textbook classifies **structure**, which is what the questions key on. My measurements say we over-run 主張表現 (こそ/だけでは present in every paper) and barely use 疑問提示文 (§F3: 0–4 per 10k vs official 1–7).
- **第1部-2 「問いを解く技術」 — five question types**: 指示語 / だれが・何が・何を / 下線部の意味 / 理由 / 例. Our corpus has 0.64 指示語 items per paper (§F6) and 0.14 例 items; the archive has 2.10 and 0.16 across 31 sittings.
- **第2部 — 情報検索 by source type**: 広告 / お知らせ / 説明書き / 表・リスト. Our 問題14 is a table in 14 of 14 papers; the textbook and the archive spread across four source types.
- **模擬試験 (p.181+)** — a complete N2 読解 section with a 問題9 A/B pair, a 長文, marked spans, and attributed real-prose passages. A second reference paper, non-OCR, that no skill file points at.
- **別冊「解答と解説」** — keys and per-item explanations, the same shape as `詳細解説.json`.
- One caveat to record with it: the book's own 問題紹介 states 内容理解(中文) as 「9問(500字程度の中文に3問×3題)」 — the **pre-12/2022 format**, with its own footnote 「ただし、問題数は変更される場合があります」. It is a register and question-type source, **never** a format or length source; the 7-sitting current-era window owns those.

**Fix.** `tools/extract_shinkanzen_dokkai.py` (reusing the Vision OCR path in `tools/vision_ocr.swift` that `extract_jlpt_n2_new.py` uses) → `refs/Shinkanzen/dokkai_reference.md`, a `make extract-shinkanzen-dokkai` target in `AGENTS.md` §4, and three pointers: `AGENTS.md` §3's Shinkanzen bullet, `dokkai.md`'s opening (the five devices and five question types, marked **secondary evidence**), and `official_calibration.md` §0's corpus list.

---

## What is healthy — measured, not assumed

- **Answer positions are clean.** 読解 keys (items 52–71) land 22/27/25/26% across options 1–4 (n=280) against official's 21/23/28/28% (n=138). Every paper is inside the envelope.
- **問題11's pair mix matches the archive.** Ours: 30 事/考 pairs, 26 事/事 (n=56). Official current era: 11 事/考, 12 事/事, 1 考/考 (n=28, plus the two irregular sittings). Every paper carries ≥1 考え/主張 stem, which is the rule that actually holds across 7 of 7 official papers — and the repo correctly retired the "one of each per pair" rule that would have failed 6 of them.
- **問題13 closes on 考え/主張 in 14 of 14**, and 問題12's item 65 asks the common point in 14 of 14 — both the official regularities, both honoured.
- **問題14 items are person-scenario in 28 of 28** — official's 7-of-7 invariant, and the shape our stems then squander (§F4).
- **Length floors are met by every paper**, and 問題11's per-passage lengths sit inside the archive (ours 489–777, median 630; official 507–763, median 655).
- **問題12 A/B halves are balanced** (|A−B| ≤ 17% of the longer, same as official's 0–15%).
- **The gloss apparatus is honest where it is counted**: 問題12 and 問題14 carry zero glosses in 12 of 14 papers, matching the archive's 0-in-every-paper; the count is earned in 問題11 (13–20 markers). The remaining gap is the total — 12–43 against the official 27–61, which is exactly what the existing WARN says on 7 papers.
- **The span apparatus itself is clean.** Marker/stem pairing, character-identical spans, gloss-outside-the-bold and the length band are all green across 14 papers — the 19 over-band spans found in 2026-08-18 were re-cut and stayed re-cut. The defect is the *rate* (§F6), not the hygiene.
- **The newest three papers are visibly better** on the things that were counted: absolute-quantifier options 0 (against 9–11 two months ago), ratio-median 1.10–1.11, uniquely-longest 17–28%.

The pattern across F1, F2, F4, F5 and F7 is the one the choukai audit named in its own words: **a counted tell gets fixed and an uncounted one grows in its place.** Every finding here is either a distribution the rules specify one-sidedly (a floor with no ceiling, a ban with no rate) or a rule whose scope stops one 大問 short of the defect.

---

## Recommended order of work

1. **Settle the two measurement conflicts first** (§D1): the `≤1.30` clamp against official's 40.5% breach rate, and the span band's era mixing. A quota built on an unreproducible or era-mixed number moves papers away from official — F2 is that failure already shipped.
2. **Fix the two scope bugs** (F5's 問題11-only ban, F4's stem-blind 問題14 check). Cheapest lines in this report, and three live breaches disappear.
3. **Add the overlap-direction rule and its gate line** (F1) — the single highest-impact change, because it is the axis on which our 読解 is solvable without Japanese.
4. **Make the length and rhythm bands two-sided** (F7, F8): both are one regex each and both are currently invisible.
5. **Add the voice quota** (F3) — the most expensive to comply with and the one that makes F9's question mix reachable at all.
6. **Cap the span rate and restore 筆者によると / 指示語** (F6).
7. **Extract the Shin Kanzen 読解 reference** (F11) and point the skills at it.

---

## Method, and what I did not do

- **Parsers.** One record type from both sides (`{section, passage, stem, options[4], key}`). Official: `booklet.md` split on `^#*\s*問題\s*(\d+)`, passages on `^\(\d\)$`/`^A|B$`, stems on `^(\d{2})\s+` filtered by that sitting's own `answer_keys.json` 大問 map (no era's numbering assumed), options on `^[1-4]\s` in sequence with wrapped lines folded into the previous option, inline-furigana lines dropped as described above. Generated: `### (n)` passages, `^\*\*(\d{2})\*\*` stems, `^\s+[1-4][.、]` options, keys from the `## 読解` table.
- **Lengths** are quoted two ways, each named: the gate's own `passage_prose()` + JP-char class for generated papers (so the numbers are the gate's), and `official_calibration.md` §2 for official papers (same function, already committed). Per-passage and per-sentence figures are my parse on both sides.
- **Overlap** = share of an option's character bigrams (kanji/kana only) occurring anywhere in its own passage. **LCS** figures use kanji/kana-only normalisation, which is deliberately more permissive than `check_verbatim_keys`'s (that one breaks a match at punctuation) — my LCS numbers are comparable across corpora but **not** comparable to the gate's ≥15/≥20 thresholds, and I make no claim about gate-invisible verbatim lifts.
- **Stem classification** is one priority-ordered bucket list, stated in the report and applied identically to both corpora. It replaced a first attempt whose 「とは何」 pattern silently matched 「ことは何か」 — every stem-shape number here is from the corrected pass.
- **Not done:** I did not re-derive the official gloss/（中略）/length tables; where I needed them I quote `official_calibration.md` and say so. My own 中略 parse under-counted (passage-region only), so the committed 2–5/median 3 band stands.
- **Not done:** no per-item difficulty or answerability review. This audit measures *distributions*; whether a specific item has two defensible answers is `exam-qa-review`'s job and is not in scope here.
- **Not done:** I did not run any authoring or repair, and changed nothing on disk. `make check` was run once, to state what the gate currently sees (1 FAIL, 139 WARN).
- **Not done:** the six pre-`20260814_1` papers' 問題12 A/B halves parse under a different marker (`### A` vs `**A**`), so the symmetry number covers 8 of 14 papers.

---

# Remediation plan

Ordered so that nothing is authored against a number that later moves, and so the
expensive step — rebuilding a paper's model answer and its translation — happens
exactly once per paper. Each item names the **owner file** the rule belongs to, the
**gate line** that makes it observable, and the **acceptance test** that says it is
done.

Conventions this plan follows, from `AGENTS.md` §4 and `dokkai.md`:

- A rule has **one owner file**; every other file points at it.
- The **authoring target is tighter than the gate**. The gate FAILs only outside the
  archive's whole range; the target is the archive's median.
- A new gate line that existing papers breach ships with a **named grandfather set**,
  and the set is named **in the owner doc too**.
- **The dokkai rebuild chain is the expensive leg.** Any edit to a stem, an option or
  a passage in `言語知識・読解.md` makes three downstream artifacts stale:
  `詳細解説.json` (the gate already FAILs option drift — that is today's single red
  line), every `詳細解説.<lang>.json` (13 of 14 papers ship `vi`), and
  `模範解答.html`. So one touched item costs
  `make booklet` + `make sheet` + a `詳細解説` entry edit + a re-translated entry +
  `make model-answer` + `make pages`. **Batch every edit to one paper into one pass**,
  exactly as the choukai plan batches MP3 rebuilds.

### Autonomy contract — the agent runs this without asking

Every "decision" below is a **decision rule with a bright line**, not a question to
escalate: D1 and D2 are settled by measurement, D3 is a policy with thresholds, and
§5.0's tier is derived from the artifact a repair touches. An agent that reaches a
fork not covered by a rule extends the rule in the owner file and says so in its final
report — it does not stop.

**Decides for itself, and never asks:** which findings exist and at what tier; which
papers get tier A/B/C work; the replacement numbers D1/D2 produce; what to write in
every repaired stem, option and passage; when to batch a paper's rebuild; which ids
enter or leave a grandfather set (an id leaves only when that paper is actually
repaired); and **committing each completed step**.

**Out of scope, so not questions either:** pushing to a remote; editing anything in
`refs/` (it is the measuring stick); and removing a check — this plan only adds them,
and a check that proves wrong is re-thresholded with the reason recorded.

**One sequencing rule that replaces an escalation:** a repair that moves a shipped
paper's KEY — re-keying an item, or rewriting options such that the key's option
number changes — requires an `exam-qa-review` blind solve of that section. **It is its
OWN step, never the tail of the authoring step**, because `AGENTS.md` §5's
non-negotiable rule is that QA runs in a context that authored nothing: a blind solve
appended to the context that just wrote the options is not blind. The authoring step
therefore ends by queuing `P5Q-<id>-<section>` with `deps: [the authoring step]`, and
the next runner — a later cron firing, or a subagent spawned for it — performs it with
the paper's text as its only input. A re-key with no *independent* blind solve behind
it is a defect class this repo has shipped more than once.

**Reports, per `AGENTS.md` §0.7:** skills read, phases run, papers touched, papers
still queued and where they sit in D3's order, every grandfather id added or removed,
and the `make check` output read line by line — written to
`qa/dokkai-remediation-report.md`. A `declined` status is reserved for a step the
measurement showed was a false positive, with the measurement recorded; it is never
"we chose not to fix this paper".

---

## Phase R — running this unattended

Identical in shape to the choukai plan's Phase R, and it shares its state file's
design so the two can run in either order (never simultaneously — see the lease).

- **State file** `logs/dokkai_remediation_state.json`, tracked, same schema:
  `{plan_source, plan_sha, max_steps_per_run, steps:[{id, deps, status, artifact,
  tier, test_id, needs_rebuild}], runs:[…], runner:{lease, at}}`.
  `status ∈ todo | doing | done | blocked | declined | stale` — where `declined` means
  "re-measured and not a real finding", never "skipped".
- **Step granularity: one paper, one tier, one artifact.** Never larger.

| Step shape | Example id | Ends with |
|---|---|---|
| one tool/doc change | `P1-profile`, `P2.2-quotas` | `make check` green |
| one paper's tier A | `P5A-20260814_1-stems` | booklet + sheet + 詳細解説 + translation + model-answer for that id |
| one paper's tier B | `P5B-20260817_1-register` | same, plus every item's evidence re-verified |
| one surface re-author | `P5C-20260810_2-mondai10` | same, plus `logs/topics.json` updated |

- **No rebuild is deferrable here.** Unlike the choukai plan, there is no shared
  rebuild batch: the expensive artifacts are per paper, so the batch boundary IS the
  paper. A step that edits a paper and stops before `make model-answer` leaves the
  gate red on that id, so the step is not done until the chain is complete. Record
  `gate_expected` if a step must be interrupted mid-chain.
- **Every run starts by reconciling, not trusting:** `git status`; `make check` read
  line by line; compare failures against `state.gate_expected`; re-derive any stale
  `doing` step by *measuring* the paper, never by trusting the flag; a twice-failed
  step becomes `blocked` with its error text and the run moves on.
- **Restart:** a cron routine every 4–6 h with a fixed, stateless prompt (all state is
  on disk), or self-paced `/loop` for an interactive burst. Never both — the state
  file carries a `runner` lease and a runner finding a fresh foreign lease exits.
  The routine deletes itself when no `todo`/`doing` remains.
- **One commit per completed step**, message naming the step id
  (`dokkai(P5A-20260814_1): retire two banned retrieval stems`).

### R.8 What still needs a human — three things, and none of them is a decision

The plan is written to run without a person in the loop, and the 読解 half is easier to
automate than 聴解 was: **every finding in this report is text-measurable**, so there is
no analogue of the choukai plan's D2, where the margin dispute could only be settled by
listening to an MP3. An agent can measure, decide, author, verify and commit every step
below. What it cannot do:

1. **Start it, and pre-authorise it.** Someone types the first prompt and gives the
   harness standing permission to run `make`, edit `tests/`, and `git commit` — in a
   permission-gated session every one of those prompts a human, which is a harness
   setting, not a question the plan asks. Arming the cron routine is itself an agent
   action, but the routine only fires while the machine is awake.
2. **Publish.** Pushing to a remote and deploying `_site/` are out of scope by design
   (§Autonomy contract). Every step's value lands locally, in `make check` and in the
   papers; making it public is a separate instruction.
3. **Judge two things no gate can.** The gates measure distributions; they cannot say
   whether a rewritten passage reads like natural published Japanese, or whether a
   `詳細解説.vi.json` entry is a good Vietnamese explanation — the only check on the
   latter today is that its quoted option text matches the printed paper. Neither
   blocks the plan, and neither is a decision the agent should stop for. Both are places
   where a native reader adds signal the plan cannot generate, so the final report names
   the papers whose prose was rewritten and the entries that were re-translated, as a
   review list rather than a request.

**The one structural requirement.** "Fresh eyes" is a *context* requirement, not a
human requirement (`AGENTS.md` §5), so the runner needs one of: subagents available, or
step granularity fine enough that authoring and blind-solving land in different cron
firings. §R.3's one-paper-one-tier-one-artifact rule plus the queued `P5Q-*` QA steps
give the second for free — which is why a QA step must never be folded into the step
that authored the text it reviews.

---

## Phase 0 — three decisions the plan makes by rule

### D1. One parse owns each measured number

**Problem.** Three numbers in the 読解 rules cannot be reproduced as stated:

1. `check_dokkai_option_length_balance`'s `≤1.30` FAIL — **40.5% of official
   current-era items breach it** (§F2), and `official_calibration.md` §9, which audits
   fifteen constants against the archive, does not list this one. It was derived from
   a generated-paper audit only.
2. `dokkai.md` §"Length band — the span is a pointer": 55 spans, median 8, p95 23,
   measured across all 31 sittings — an **era mix**, since pre-2018 papers ran 4–5
   spans and the current era runs 0–3 (§F6). The *rate* was never measured at all.
3. `dokkai.md`'s per-passage 問題10 guidance ("author to ~240") against a corpus at
   278 median — not a conflict, but unobservable, because the constant it is written
   beside is a floor (§F7).

**Decision.** The measurement stops being prose and becomes a committed script
(Phase 1). Then re-derive the option-length envelope, the span rate and band
(current era only), and the length ceilings with it, and update whichever document is
wrong. Print the parse rule beside every row, as `official_calibration.md` §0 already
does for its own numbers.

### D2. The key-length rule becomes a distribution, not a per-item clamp

**Problem** (§F2): the per-item clamp is stricter than the archive on purpose, and it
manufactured a worse tell (48.8% of keys at rank 2 vs official 29.5%). Tightening it
further cannot help: the tell lives in the *ranking*, which a clamp cannot see.

**Decision, by measurement rather than taste.** Adopt the archive's envelope per item
and gate the *paper* on spread:

| level | rule | official evidence |
|---|---|---|
| item | max/min WARN above **1.65**, FAIL above **2.5** | official median 1.26, p90 1.61, max 4.29 |
| paper | no key rank may exceed **60%** of items (WARN above 45%) | official per-paper worst **56%**, median 39% |
| paper | uniquely-longest 20–30% (unchanged) | official 23.0% |
| paper | **overlap direction: the median (key − best distractor) overlap margin must be ≤ 0** | **7 of 7** official papers negative (−0.021…−0.100); 9 of 14 generated positive |
| paper | overlap share: key strictly top in **≤50%** of items (WARN above 44%) | official 11–44%, median 38% |

The last row is F1's gate line and the reason D2 is one decision, not two: length and
overlap are the two axes on which a key is findable without reading, and clamping one
in isolation is what pushed the corpus onto the other.

The margin row is the primary line and the share row the secondary one: the margin has
a natural zero that every official paper clears and 9 of 14 generated papers fail, so it
needs no arbitrary threshold at all. **Both thresholds were set after checking they fail
no official paper** — the first draft of this plan proposed 40%/55% on the share, which
would have failed 7/2024 (44%) and put three more official papers on WARN. That check is
the rule, not a courtesy: a gate line an official paper trips is a wrong line
(`AGENTS.md` §0).

### D3. Repair scope — all fourteen papers, ordered rather than filtered

**The scope is the whole corpus.** Both halves of the ask are in scope: the pipeline
(Phases 1–3, 7) and **every paper on disk** (Phase 5). So D3 is not a filter that
decides *whether* a paper is repaired — it is the **ordering rule** that decides in
what order, because the corpus cannot be repaired in one run and an interrupted run
must always have finished the most damaging work first.

**Order, highest priority first.** A finding on a paper is repaired before another
when it is:

1. **exam-breaking** — a mis-key, a second defensible answer, or an item answerable
   without reading its passage;
2. a **literal breach of a stated rule** — the banned retrieval shapes (F5), the
   問題14 truth-check shape (F4);
3. **outside the archive's whole range** — a gate FAIL for a non-grandfathered id
   (kanji density, sentence rhythm, length ceilings, overlap margin, key rank);
4. **off the archive's median but inside its range** — the WARN class (span rate,
   ※ count, gloss count, question-form mix);

and, within one priority class, the **three most recent papers first**, since those are
what the next author copies.

**Grandfather sets exist, but only as temporary bookkeeping.** A Phase-3 check that
lands before its papers are repaired names the breaching ids so the gate stays
readable; **every such id has exactly one removal condition — that paper's repair —
and the plan is not done until every set is empty.** That is the repo's own rule
(`dokkai.md` §場面-style sets: "an id leaves the set the moment that paper's section is
repaired"), applied without exception here. No paper is written off as "forward-only".

**What that costs, stated honestly.** The distributional findings do not spare a single
paper: kanji density is outside the official band in **14 of 14**, the voice quota in
**14 of 14**, the span cap in **12 of 14**. So full-corpus repair means a prose pass
over most of the 読解 half of every paper, plus the per-paper rebuild chain (Phase 4)
including the Vietnamese explanation entries. §5.4's matrix is the actual work list;
the total is roughly **14 item-level passes + 12 prose passes + ~40 surface
re-authorings**, and at one paper per session it is a multi-week plan, which is exactly
why Phase R makes it resumable and why the ordering above matters more than the
totals.

## Phase 1 — `tools/dokkai_profile.py`: one measurement, two consumers

**Why first.** Every conflict in D1 has the same cause: the numbers live in prose, the
gate re-implements them, and nothing forces the two to agree. `official_calibration.md`
§0 documents its parse rules and its scratchpad `measure.py` was never committed.

**Build it.** New file, repo-level (it measures `refs/` and `tests/`, so it is not a
skill script — same class as `tools/check_consistency.py`):

```
tools/dokkai_profile.py [--official] [--tests <id>…] [--era cur|all] [--json] [--baseline]
```

- **One parser, two front-ends**, producing the same record type from
  `refs/JLPT_N2_NEW/*/booklet.md` and `tests/*/言語知識・読解.md`:
  `{section, passage_idx, preface, passage, stem, options[4], key, glosses[]}`.
  Official 大問 membership comes from that sitting's own `answer_keys.json`, never from
  an assumed numbering; inline-furigana lines are dropped by the documented rule.
- **Emit every number this report used**, per paper and pooled: section and per-passage
  lengths, sentence-length distribution, kanji density, です・ます share, first-person
  passage share, institutional/personal lexis rates, stem-bucket histograms per 大問,
  span rate and span lengths, 指示語/例 item counts, apparatus-stem shapes, 問題14 stem
  target, option-length distribution and key rank, overlap direction and margin,
  absolute-quantifier and ※ rates, gloss counts per 大問, （中略）.
- **`--baseline`** prints the official table in the exact Markdown `dokkai.md` and
  `official_calibration.md` carry, so refreshing a doc is a paste, not a retype.
- **`check_consistency.py` imports it** instead of re-implementing counts. The gate
  keeps owning the **thresholds**; the script owns the **measurement**.
- **Reuse, do not duplicate:** `passage_prose()`, `dokkai_section()` and the JP-char
  class already live in `check_consistency.py` and are the committed definition of
  every length in the repo. The profile script imports them rather than re-deriving,
  or the repo gains a fourth way to count a character.

**Acceptance test:** `python3 tools/dokkai_profile.py --official --baseline`
reproduces every official figure in `official_calibration.md` §§2–6 and `dokkai.md`'s
length/span tables, or the doc is edited to what it prints, with the parse rule named
on the row. Then `make check` is green and its 読解 numbers are byte-identical to the
script's.

**Effort:** the largest single item in this plan (~400–600 lines), and it pays for
itself the first time a quota is questioned. Much of it exists already as the audit
scripts behind this report.

---

## Phase 2 — rule changes, by owner file

### 2.1 `jlpt-exam-structure` — the 読解 question-form inventory (F4, F6, F9)

This file owns instruction lines and owns no question lines, which is why nothing told
an author that 「〜について、正しいものはどれか」 is a shape the archive never uses. Add
§"問題10–14 question forms" with the archive's inventory (re-derived per D1):

| 大問 | Frame | Official share |
|---|---|---|
| 10 | 筆者の考えに合うのはどれか / 筆者はどのように考えているか | ~29% |
| 10 | 筆者はどのように述べているか / 筆者の説明に合うのはどれか | ~17% |
| 10 | apparatus **intent**: この お知らせ/メール で伝えたいことは何か・問い合わせていることは何か・用件は何か | ~23% (8 of 10 apparatus items) |
| 10 | 筆者によると、…は何か | ~6% |
| 11/13 | 筆者によると、…は何か / どうすればいいか | **25–29%** |
| 11/13 | span- or 指示語-anchored: 「…」とあるが、どういうことか / それは何を指すか | 27–29% (≤3 per paper) |
| 11/13 | 筆者の考えに合うのはどれか / 言いたいことは何か | 24–25% |
| 12 | 65 = A と B が共通して述べていること; 66 = どのようなアドバイス/どうしたらいい | 7 of 7 |
| 14 | a **value**, an **action**, or one named **option** — never a proposition to verify | 12 of 12 |

Note beside it the two facts a generator needs: the banned four retrieval shapes occur
**0 times in any 大問** across 15 sittings, and 「筆者」 is absent from 18% of 問題11
stems (never gate on 筆者 alone).

### 2.2 `question-authoring/references/dokkai.md` — the quotas

| # | Rule to add | Official | (gate) |
|---|---|---|---|
| F1 | The paper's median (key − best distractor) passage-overlap margin is **≤ 0**, and the key is strictly top in ≤50% of items; distractors are built FROM passage material with one fact changed | margin negative in 7 of 7; share 11–44% | yes |
| F2 | Per item max/min WARN >1.65, FAIL >2.5; per paper no key rank above 60% (WARN >45%) | median 1.26; per-paper worst rank share 56% | yes, replaces the 1.30 clamp |
| F3 | ≥4 of the 12 essay surfaces first-person; ≥3 in です・ます throughout; kanji density per paper **24–32%** | 80%, 32%, 25.1–29.8% | yes (kanji band), WARN (voice) |
| F4 | 問題14 items ask a value, an action or a named option — not 「正しいものはどれか」 | 12 of 12 | yes |
| F5 | The banned-retrieval-shape family covers **問題10–14**, and includes bare 「正しいもの/適切なもの はどれか」 | 0 of 138 | yes |
| F6 | ≤2 span-anchored stems per paper; ≥1 指示語 item; 「筆者によると」 retrieval is the default anchored shape | 0–3 spans, 1.57 指示語 | yes (cap), WARN (指示語) |
| F7 | Every length row gains a **ceiling**: 問題10 ≤1330 (passage ≤350), 問題11 ≤2700, 問題12 ≤600, 問題13 ≤1070, 問題14 ≤640; mean option length 24–30 | archive maxima | yes |
| F8 | Median sentence length per paper **33–43** JP chars (FAIL outside 28–50); share under 25 chars 12–30% | 35–42, 14–27% | yes |
| F9 | ≥2 of 5 問題10 items on the 筆者の考え family; every notice/email item asks **intent** | 46%, 8 of 10 | yes (first), WARN (second) |
| F10 | ※ ≤3 per paper; the "3 false options contradicted by ※" recipe is one option, not the shape | 0–3 | yes |

Also correct two statements in that file: the passage inventory ("one notice with 3
false options contradicted by ※ fine print") overstates a rare official shape, and the
span-length band must be re-derived on the current era (D1) with the **rate** stated
next to it — a band with no rate is what produced F6.

### 2.3 `exam-blueprint` — the voice axis on the theme table (F3)

The thirteen-surface rules govern **subject** (axis 1) and **closing move** (axis 2).
Add axis 3, **voice**: each surface records `一人称随筆 / 評論 / 解説 / 通知` and the
paper's tally must reach F3's quota. `logs/topics.json` already records one label per
surface; extend the record rather than adding a file, exactly as the rotation history
does.

### 2.4 `exam-qa-review` — two lines the gate cannot decide

- The blind-solve pass gains a **strategy check**: before reading anything, answer the
  20 読解 items by "most passage overlap" and by "second-longest option" and record
  both scores. Above 45% on either, the section is returned to authoring. This is
  cheap (the keyless render already exists, `make keyless`) and it is the only way a
  human-facing pass sees F1/F2 on a single paper.
- The 「〜について、正しいものはどれか」 shape becomes a named automatic finding for
  問題14, as the 「内容と合っている」 shape already is for 問題11.

---

## Phase 3 — gate lines, so none of this can regress silently

New checks in `tools/check_consistency.py`, each importing its measurement from
Phase 1. House style: the docstring carries the incident, the failure message carries
the repair, the threshold sits outside the archive's whole range, and every breaching
paper is named in a grandfather set the owner doc also names.

| Check | Measures | FAIL / WARN | Grandfathered |
|---|---|---|---|
| `check_dokkai_overlap_direction` | median (key − best distractor) passage bigram-overlap margin, and the strict top-overlap share | FAIL when the margin > 0 or the share > 50%; WARN above 44% | the 9 papers with a positive margin until repaired |
| `check_dokkai_key_rank_spread` | key-rank histogram per paper | FAIL when one rank >60%, WARN >45% | `20260813_2` 78%, `20260810_1` 72%, `20260812_1` 72%, `20260811_1` 67%, `20260807_1` 61%, `20260814_1` 61% |
| `check_dokkai_option_length_band` | replaces the ≤1.30 clamp | FAIL >2.5 per item; WARN >1.65 | none — it loosens |
| `check_dokkai_banned_stems` | the banned family over **問題10–14**, incl. bare 正しいもの/適切なもの | FAIL | `20260807_1`, `20260814_1` until repaired |
| `check_dokkai_q14_stem_target` | 問題14 stem asks value / action / named option | FAIL when both items are truth-check; WARN on one | 12 papers, listed |
| `check_dokkai_span_rate` | span-anchored stems per paper; 指示語 items per paper | FAIL >4 spans; WARN >2 or 0 指示語 | the 8 papers at ≥5 |
| `check_dokkai_register` | です・ます share, first-person share, kanji density | FAIL kanji outside 22–34%; WARN on the voice quotas | all 14 on voice; `20260814_1` on kanji |
| `check_dokkai_sentence_rhythm` | median sentence length, share <25 chars | FAIL outside 28–50; WARN outside 33–43 | `20260817_1`, `20260817_2`, `20260814_1`, `20260810_2`, `20260819_1` |
| `check_dokkai_lengths` (extend) | the existing floors gain ceilings | FAIL above the archive max | the 9 papers above the 問題10 ceiling |
| `check_dokkai_q10_form_mix` | 問題10 stem-bucket histogram; apparatus stems asking intent | FAIL at 0 考え/主張 items; WARN below 2 or on a content-shaped apparatus stem | most papers — measure first, then name |
| `check_dokkai_asterisk_rate` | ※ per paper in 問題10–14 | WARN >3 | 11 papers |

Two scope notes so the checks do not over-promise:

- **`check_dokkai_overlap_direction` needs each item's OWN passage**, not the
  concatenated 読解 region — `check_verbatim_keys` uses the concatenation, which is
  right for a verbatim-lift hunt and wrong here (an option overlapping a *different*
  passage is not a tell). The profile script's record type already carries the pairing.
- **Every new check declares its repair artifact** in the `FINDING_REPAIR` table the
  choukai plan introduces (`§5.0`), so the tier is derived rather than decided, and the
  meta-check that FAILs an undeclared finding covers these slugs too.

---

## Phase 4 — the per-paper rebuild chain

There is no shared batch here; the unit is the paper. For each repaired id, in order:

```
make booklet <id>          # 言語知識・読解.html from the edited Markdown
make sheet <id>            # 解答.html — embeds the printed options
# edit 詳細解説.json for every touched item (stem, options, 解説 prose quoting them)
make scaffold-translation <id> TLANG=vi TLABEL="Tiếng Việt"   # only the touched entries
make merge-translation <id> TLANG=vi
make model-answer <id>     # 模範解答.html, carrying both languages
make pages                 # once, after the last paper of the run
make check                 # read every line
```

Two costs to write into the step rather than discover:

- **The translation leg is the expensive one.** 13 of 14 papers ship `詳細解説.vi.json`;
  a touched item needs its `vi` entry re-translated, not just re-merged. Scope each
  step to the items it actually touches — `scaffold_translation.py` packets are
  per-item for exactly this reason.
- **`20260819_1` has no `模範解答.html` yet** and is today's single gate FAIL (its
  `詳細解説.json` carries a 聴解 option the paper no longer prints). Repair that
  drift and build its model answer as step **P4.0**, before any dokkai edit lands on
  that id, or the red line hides the next one.

---

## Phase 5 — the 14 papers on disk

Tiered by **what a repair touches**, derived mechanically (never decided per session):

| Tier | Touches | Also needs | Marginal cost |
|---|---|---|---|
| **A** | a stem, an option, or a key-table cell | the Phase 4 chain for that id | ~30 min/paper + translation of touched entries |
| **B** | passage prose, subject unchanged (register, length, rhythm) | Phase 4 chain **plus** re-verification of every item anchored on that passage: span identity, 解説 quotes, overlap direction, key rank | ~2 h/paper |
| **C** | a new surface (subject or voice changed) | all of B **plus** `logs/topics.json` and the blueprint's theme record | real authoring, one surface at a time |

`tier = {"stem/option/key-cell": "A", "passage prose": "B", "<surface re-author>": "C"}[artifact]`,
declared once per finding slug beside the check. **Escalation is allowed,
de-escalation is not**: a tier-A repair that turns out to need the passage rewritten is
recorded as escalating to B with the reason; a tier-B finding may never be quietly
settled by a stem edit.

### Tier A — item-level, and it clears every literal breach

1. **`20260807_1` 問10-53** — 「このお知らせの内容と合っているものはどれか」 → the
   archive's intent shape (「このお知らせで伝えたいことは何か」). Re-check the four
   options still discriminate on intent; the notice itself does not change.
2. **`20260814_1` 問10-56 and 問13-68** — both literal banned shapes. 56 → a
   筆者の考え/述べ shape; 68 → a span- or 筆者によると-anchored shape (its 問題13
   partner 67 already carries one, so check the pair does not double up).
3. **The 19 問題14 truth-check items** across `20260811_1`, `20260812_1`, `20260812_2`,
   `20260813_1`, `20260813_2`, `20260814_1`, `20260817_1`, `20260817_2`, `20260817_3`,
   `20260818_1`, `20260819_1`. Rewrite each to ask a value, an action or a named
   option. The scenario prose stays; the question and usually the four options change,
   so the 解説's two flyer quotes must be re-checked against the new question
   (`check_mondai14_quotes` still applies).
4. **Overlap and rank repairs, worst-first by margin**: `20260810_1` (+0.156),
   `20260814_1` (+0.142), `20260812_2` (+0.116), `20260817_2` (+0.102), `20260811_1`
   and `20260817_1` (+0.087), `20260810_2` (+0.078), `20260817_3` (+0.061),
   `20260812_1` (+0.007); rank-only on `20260813_2` (78% at rank 2) and `20260807_1`
   (61%). The move is always the same and never touches the passage: **rebuild each
   distractor from a true passage clause with one fact changed** (which raises its
   overlap and its plausibility together), and lengthen distractors rather than
   trimming the key. Acceptance per paper: median overlap margin ≤ 0, strict top-overlap
   share ≤44%, no key rank above 45%.
5. **The ※ trim** where a ※ line sits in a notice whose item is already being
   repaired — `20260819_1` (8), `20260818_1` (7), `20260812_2` (6), `20260813_1` (6),
   `20260817_3` (6).

### Tier B — passage prose, subject unchanged

6. **Length trims to the ceiling** (F7): `20260810_1` 1658→≤1330, `20260814_1` 1604,
   `20260812_1` 1588, `20260817_2` 1587, `20260810_2` 1566, `20260807_1` 1546. Cut
   sentences, never compress them — compression raises kanji density (F3) and
   sentence length (F8) at the same time. Re-verify each item's evidence survives the
   cut, and re-run the span-identity check.
7. **Rhythm repairs** (F8): `20260817_1` (median 73 → ≤50), `20260817_2` (65.5),
   `20260814_1` (57), `20260810_2` (53). Splitting a 70-character sentence at its
   subordinate boundary usually fixes both this and the length overshoot in one edit,
   which is why 6 and 7 are one step per paper, not two.
8. **Kanji-density repair** on `20260814_1` (41.7% → ≤34%), by replacing 漢語
   compounds with the everyday phrasing official uses — this is the same edit as the
   register work and should be done with it.

### Tier C — surfaces that need re-authoring, in D3's order (all 14 papers)

9. **Voice pass on the three most recent papers** (`20260817_3`, `20260818_1`,
   `20260819_1`): convert ≥4 essay surfaces per paper to first-person and ≥3 to
   です・ます, which in practice means re-authoring those surfaces rather than editing
   them. This is the worked example the next author copies — it is worth more here than
   anywhere else in the corpus.
10. **Span-rate reduction** on `20260811_1`, `20260812_1`, `20260812_2`, `20260813_2`
    (7 spans each → ≤2), converting the surplus into 「筆者によると」 retrieval and one
    指示語 item per paper. Each converted stem needs a new key and three new options,
    so this is authoring, not editing; a blind solve follows per the autonomy contract.
11. **Then the remaining eleven papers, in D3 order** — the same voice pass and span
    conversion, plus the 問題10 form mix (≥2 筆者の考え items, apparatus stems asking
    intent). This is the long tail of the plan and the reason it is written to be
    resumable: eleven papers × two or three surfaces each, one paper per session, each
    ending green and committed. A paper is not skipped here — it is queued, and its
    grandfather entry is what marks the queue.

**What "done" means for Phase 5.** F1, F3, F8 and F9 are distributions across a
section, so a paper is either re-authored on that axis or it keeps its shape — there is
no partial credit and no patch. Phase 5 is complete when, for **all fourteen papers**:
every literal ban breach is gone; every section is inside the F7 ceilings and floors;
kanji density is inside 24–32% and median sentence length inside 33–43; the overlap
margin is ≤0 and no key rank exceeds 45%; the span cap and 指示語 floor hold; and every
Phase-3 grandfather set is **empty**. Until then the state file's remaining `todo`
steps and the non-empty sets are the same list, read two ways.

---

### 5.4 Per-paper work matrix — what each of the fourteen papers needs

Every cell is measured (Phase 1 regenerates the table). `TC` = truth-check-shaped items
(F4/F5), `mgn` = median overlap margin (F1, must reach ≤0), `rank` = largest key-rank
share (F2, must reach ≤45%), `spans` = span-anchored stems (F6, cap 2), `指` = 指示語
items (F6, floor 1), `漢` = kanji density (F3, band 24–32%), `文` = median sentence
length (F8, band 33–43), `len` = sections above the F7 ceiling, `注` = gloss markers
(floor 25, band 27–61), `※` = F10 (cap 3).

| paper | TC | mgn | rank | spans | 指 | 漢 | 文 | len over ceiling | 注 | ※ |
|---|---|---|---|---|---|---|---|---|---|---|
| `20260807_1` | 1 | −0.067 | 61% | 3 | **0** | 36.9% | 36.5 | 問10 1546, 問12 664 | 12 | 6 |
| `20260810_1` | 0 | **+0.156** | 72% | 4 | 1 | 37.4% | 45.0 | 問10 1658, 問12 617; 問14 **462 under** | 24 | 9 |
| `20260810_2` | 0 | +0.078 | 50% | 6 | 1 | 39.0% | 53.0 | 問10 1566 | 22 | 8 |
| `20260811_1` | 1 | +0.087 | 67% | 7 | 1 | 36.1% | 52.5 | 問13 1154, 問14 661 | 20 | 9 |
| `20260812_1` | 2 | +0.007 | 72% | 7 | **0** | 36.6% | 41.0 | 問10 1588, 問12 659 | 25 | 11 |
| `20260812_2` | 2 | +0.116 | 56% | 7 | **0** | 36.9% | 39.0 | 問10 1502, 問14 643 | 21 | 16 |
| `20260813_1` | 1 | −0.027 | 39% | 8 | **0** | 38.4% | 42.5 | 問14 644 | 19 | 11 |
| `20260813_2` | **5** | −0.005 | **78%** | 7 | 1 | 39.6% | 50.0 | — | 23 | 14 |
| `20260814_1` | **5** | **+0.142** | 61% | 2 | **0** | **41.7%** | 57.0 | 問10 1604, 問12 648, 問14 710 | 42 | 5 |
| `20260817_1` | 3 | +0.087 | 33% | 3 | **0** | 39.5% | **73.0** | 問13 1110 | 20 | 0 |
| `20260817_2` | 2 | +0.102 | 33% | 3 | 1 | 37.8% | **65.5** | 問10 1587, 問12 629 | 26 | 5 |
| `20260817_3` | 2 | +0.061 | 33% | 6 | 1 | 35.5% | 36.0 | — | 31 | 9 |
| `20260818_1` | 2 | −0.031 | 33% | 5 | 1 | 35.6% | 33.0 | — | 31 | 11 |
| `20260819_1` | 2 | −0.041 | 39% | 5 | 2 | 37.3% | **28.0** | — | 43 | 13 |
| **needs work** | **12 papers** | 9 | 8 | 12 | 6 | **14** | 8 | 9 | 7 | 11 |

Read the bottom row as the plan's size: **no paper is clean**, the cheapest paper
(`20260818_1`) needs an item pass plus a prose pass, and the two register columns
(漢 and the voice quota behind F3) are the only ones that touch all fourteen.

Suggested per-paper session shape, one paper per session, in the D3 order:

1. tier A item pass — TC stems, 問14 targets, overlap/rank repairs, ※ trim;
2. tier B prose pass — kanji density, sentence rhythm, length ceilings, gloss top-up
   (the four interact, so they are one edit);
3. tier C surfaces — voice conversion (≥4 first-person, ≥3 です・ます) and span
   conversion to 筆者によると/指示語, which is where the new items get written;
4. Phase 4 rebuild chain, `make check` read line by line, commit;
5. `exam-qa-review` blind solve of 読解 if any key moved, plus the two strategy scores.

---

## Phase 6 — the next paper is the real acceptance test

Run the normal 4-stage pipeline (`jlpt-test-generation`) with these additions to the
読解 authoring stage's brief:

1. **Voice** — ≥4 of the 12 essay surfaces first-person, ≥3 in です・ます throughout,
   kanji density 24–32%, ≥1 passage with quoted speech, ≥1 with a 疑問提示文.
2. **問題10** — ≥2 items on the 筆者の考え family; every notice/email item asks intent;
   section ≤1330 JP chars and no passage above 350.
3. **問題11/13** — ≤2 span-anchored stems in the whole paper, ≥1 指示語 item,
   「筆者によると」 as the default retrieval shape, ≥1 考え/主張 stem in 問題11 and
   item 69 in 問題13.
4. **問題14** — both items ask a value, an action or a named option; ≥2 flyer cells
   each; ※ ≤3 paper-wide.
5. **Keys** — distractors built from passage clauses with one fact changed; median
   overlap margin ≤ 0 and strict top-overlap share ≤44%; no key rank above 45%;
   sentence median 33–43.
6. **The artifact QA reads**: the thirteen-surface table gains a **voice** column and a
   **question-form** column, and is read down as columns before the section is called
   finished — the same discipline the closing-move column already has.

Then: `make check` green with **no new grandfather entries**, `make lint-draft`,
`make qa-eval`, `make keyless` + the two blind strategy scores under 45%, and a
fresh-eyes `exam-qa-review`. If any quota needs a grandfather entry for a paper
written *after* Phase 2, the quota is wrong — fix the quota, not the paper.

---

## Phase 7 — the Shin Kanzen 読解 corpus (F11)

1. **Extractor** `tools/extract_shinkanzen_dokkai.py`, reusing the Vision OCR path in
   `tools/vision_ocr.swift` that `extract_jlpt_n2_new.py` already drives. Emit
   `refs/Shinkanzen/dokkai_reference.md` in the same fenced `[OCR ▼]…[OCR ▲]` shape
   with the same "OCR, not quotable as exact wording" header. Note the 109 MB split
   requirement in the script's docstring.
2. **Make target** `make extract-shinkanzen-dokkai`, listed in `AGENTS.md` §4 beside
   `extract-archive`, owned by §3.
3. **Point the skills at it**: `AGENTS.md` §3's Shinkanzen bullet, `dokkai.md`'s
   opening (the five discourse devices and five question types), and
   `official_calibration.md` §0's corpus list. Mark it **secondary evidence** — a
   textbook, not the exam, and one whose 問題紹介 still describes the pre-12/2022
   format, so it corroborates register and question type and never sets a length or
   count.
4. **Then feed it to Phase 1's script** as a third front-end, so the register
   inventory can quote a non-OCR-of-a-stencil source for once.

---

## Sequencing, dependencies, and cost

```
D1 ─┬─> Phase 1 (dokkai_profile.py) ──> Phase 2 (docs) ─┐
    ├─> re-derive F2's envelope, F6's band, F7's ceilings │
    └─> D2 (key rules become distributional) ─────────────┼─> Phase 3 (gate lines)
                                                          │        ▲
D3 ─┬─> grandfather sets ─────────────────────────────────┘        │
    └─> Phase 5 tier A (item-level: F4, F5, F1/F2 repairs) ────────┘
            │  (each id: booklet -> sheet -> 詳細解説 -> vi -> model-answer)
            ▼
        Phase 5 tier B (length, rhythm, kanji) — per paper, same chain
            ▼
        Phase 5 tier C (voice pass, span conversion) — all 14, D3-ordered
                                                     ──> Phase 6: the next paper
Phase 7 (Shinkanzen extract) — independent, any time
P4.0 (20260819_1: fix today's FAIL, build its model answer) — before anything
                                            touches that id
```

| Step | Size | Forces a per-paper rebuild? | Blocks |
|---|---|---|---|
| Phase R (state file + cron) | small, once | no | **everything** — it is what survives interruption |
| P4.0 (`20260819_1` FAIL + model answer) | small | yes, that id | any edit to that id |
| D1/D2/D3 | small | no | Phases 2, 3, 5 |
| Phase 1 script | large (400–600 lines) | no | Phases 2, 3 |
| Phase 2 docs | medium, 4 files | no | Phase 3 |
| Phase 3 gate | medium, ~11 checks | no | Phase 6 |
| Phase 5 tier A | ~50 items over 14 papers | **yes, per paper** | — |
| Phase 5 tier B | 14 papers (kanji band alone hits all of them) | yes, per paper | — |
| Phase 5 tier C | ~40 surfaces over 14 papers | yes, per paper | Phase 5's completion |
| Phase 6 | one full paper | its own | — |
| Phase 7 | medium | no | nothing |

**Default execution order, if the run is cut short.** Each phase leaves the repo green,
so an agent should prioritise rather than ask which to drop: (1) P4.0, because a red
gate hides everything behind it; (2) F5's scope fix plus the three banned stems — one
line of code and three stems, and a stated ban stops being violated on disk; (3) F4's
問題14 stem rule and gate line, the largest single-shape divergence in the section;
(4) Phase 1, because without it the next quota is built on an unreproducible number,
which is how F2 happened; (5) D2's replacement of the ≤1.30 clamp, because the clamp is
actively pushing new papers toward the rank-2 tell.

**Split by what improves what:** Phases 1–3 and 7 improve the *pipeline* — they make
the next paper better and stop the regressions recurring, but change nothing a learner
sees today. Phase 5 is the only phase that improves the fourteen papers a learner can
take right now, and it covers all fourteen (§5.4). Its tier A is where the ratio of
learner-visible improvement to cost is highest — three stems and ~50 options remove
every literal rule breach in the corpus — and its tier B/C tail is the bulk of the
calendar time, one paper per session, which is what Phase R exists for.

## Risks to watch

- **Phase 1 re-measurement will move numbers the current papers were built to** (F2's
  clamp certainly, F6's span band probably). That is the point, but it means Phase 3's
  grandfather sets must be computed *after* Phase 1, not guessed now.
- **The overlap metric is normalisation-dependent.** Bigram overlap on kanji/kana-only
  text is stable enough to gate a distribution, but it is not a linguistic measure of
  paraphrase quality. Ship it with the margin fallback (D2) and re-check the threshold
  against the archive whenever the normalisation changes.
- **F3's voice quota fights F7's length ceiling.** です・ます prose runs longer in
  characters than だ・である for the same content. Author both together, and treat a
  paper that hits the ceiling only by reverting to plain style as failing F3, not
  passing F7.
- **Translation drift is the real cost of tier A.** Thirty repaired items across twelve
  papers is thirty `vi` entries to re-translate; a step that edits the Japanese and
  skips the translation ships a model answer that explains wording the paper does not
  contain — which is exactly today's single FAIL.
- **Grandfathering fatigue**: eleven new checks with eleven exemption sets makes green
  weaker, not stronger, and here the sets start large — some cover all fourteen papers.
  They are a queue, not an amnesty: each set's id-removal condition is written next to
  it, the state file's `todo` list mirrors it, and Phase 5 is not done until every set
  is empty. If a set is still non-empty when the plan is declared finished, the plan
  was not finished.
- **The 構成表 analogue does not exist for 読解.** The choukai plan can gate on a table
  the author fills; 読解's equivalent artifacts are the thirteen-surface column and the
  key-notes lines, and only the former is written down today. Phase 2.4's voice and
  question-form columns are what make F3/F9 auditable by a human at all — add them
  before the checks that read them.
