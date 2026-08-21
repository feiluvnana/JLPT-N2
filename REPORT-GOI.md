# 文字・語彙 audit — 14 generated papers vs 31 official sittings vs Shin Kanzen N2 語彙/漢字 + 日本語総まとめ N2

Date: 2026-08-21 (measurements run 2026-08-20). Read-only analysis; nothing on disk was changed.

**Corpora actually opened**

| Corpus | What was read | n |
|---|---|---|
| Generated | `tests/*/言語知識・読解.md`, 問題1–6 region (stems, option rows, `## 文字・語彙` key table + 解説 cells) and every `test_spec.json` | 14 papers, **420 items, 1,680 options** |
| Official | `refs/JLPT_N2_NEW/*/booklet.md` 問題1–6 region + `answer_keys.json` | 31 sittings, **934 of 964 items parsed (96.9%)**, 922 after dropping 12 parse artifacts; the current era (12/2022–12/2025) is 7 sittings / 203 items |
| Shin Kanzen 語彙 | `Shin_Kanzen_Masuta_N2-Goi.pdf` — はじめに, 目次, 本書をお使いになる方へ (pp.1–7) and the tail (pp.225–240) | 1 book, 246 pp |
| Shin Kanzen 漢字 | `Shin_Kanzen_Masuta_N2-Kanji.pdf` — 表紙, はじめに, 目次 (pp.1–5, split out of a 264 MB file) | 1 book, 253 pp |
| Soumatome | `nihongo-soumatome-n2-goi.pdf` — はじめに, マーク凡例, 目次 (pp.1–6, split out of a 103 MB file) | 1 book, 156 pp |
| Repo rules | `AGENTS.md`, `question-authoring/SKILL.md` + `references/moji-goi.md` + `references/official_calibration.md`, `exam-blueprint/SKILL.md` + `scripts/sample_items.py` + `references/pools.json`, `exam-qa-review`, the 文字・語彙 half of `tools/check_consistency.py`, `logs/ledger.json` | — |

**Four corpus facts worth recording before the findings**

1. **The official 問題1/問題2/問題5 TARGET is not recoverable from the archive.** `booklet.md` is a text-layer extract and the underline does not survive it, so for 155 問題1 items I have the stem, the four readings and the key — and no way to say which word was underlined. Every finding below is therefore built on stems, option sets and keys, never on an inferred official target. This is also why the 訓読み cap cannot be re-derived from the archive (§F10.3) and why Shin Kanzen's two typeset 語彙 模擬試験 matter (§F11).
2. **Inline furigana arrives as separate lines** (「風邪 / かぜ / の（　）のために」), and in the current era it is dense — 8 to 53 ruby lines inside 問題1–6 per sitting, against 3–4 in the 2010–2016 sittings. My parser drops a short all-kana line that follows a kanji-final line. Whether that ruby is JEES's own or the Vietnamese reproducer's cannot be decided from `refs/` (`official_calibration.md` §0 makes the same caveat about the underline), so **I make no finding out of the fact that our papers carry zero ruby anywhere in `言語知識・読解.md`** — it is recorded here as an open question for whoever next reads a JEES original.
3. **Two option layouts break a naive parser and both are official.** 問題5 sometimes prints its four options in two columns, so they arrive in the order 1,3,2,4; and a ruby split can put markers 2/3/4 in the middle of a continuation line. Both are handled by slot-assignment rather than sequence; the 30 unparsed items are almost all 問題5 rows in three 2011–2012 sittings.
4. **`pools.json` has no provenance field.** The six 文字・語彙 categories are 3,673 bare strings (`kanji_reading` 1528, `context_words` 1381, `orthography` 249, `usage` 217, `paraphrase` 143, `word_formation` 85). A grep for `provenance|source|book|Shinkanzen|Soumatome` in that file returns nothing, so the rule "check every 問題1–6 key against Shin Kanzen N2-Goi/N2-Kanji and Soumatome N2 語彙/漢字" leaves no trace on disk and cannot be audited after the fact (§F11).

`make check` at the time of this audit: **green — 0 failures, 138 warnings** (run 2026-08-20 from a clean tree, and again on 2026-08-21 after this report was written: unchanged). Every finding below except parts of F5, F6 and F8 is invisible to it.

---

## Summary — the shortcomings, ranked

| # | Finding | Measured | Gated today? |
|---|---|---|---|
| F1 | **The 問題1/2/5 stem stopped being a sentence and became a passage** | per-paper median stem 21–32 JP chars vs official 15–22 (current era **15–17**); **14 of 14 papers above the current-era ceiling**; comma-free stems median **7%** vs official 73% (current era 80%), six papers at **0%** | no |
| F2 | **です・ます is gone from 文字・語彙** | polite marker in 問題1–5 stems: ours 0–16% (median 6%) vs official 8–41% (current era **16–32%**); 問題1 sentence-final polite **0 of 70** vs 34% official-cur; first person 1% vs 7% | no |
| F3 | **問題2 lost its 和語 branch and became a pseudo-compound grid** | okurigana-bearing option sets 16% vs official 44% (cur 40%); **six papers ship 0 of 5**, official ships 1–3 in every one of 31 sittings; all-2-kanji items **4–5 of 5 in eleven papers** where the archive never exceeds **3 of 5**; complete 2×2 grids 100% vs 80/89% | no |
| F4 | **問題4's stem outgrew the archive, and one paper left it far behind** | per-paper median 25–**66** vs official 17–35 (cur 24–32); 7 papers above the official ceiling; `20260811_1` median **66**, longest stem **76** against an archive maximum of 45 | no |
| F5 | **The 訓読み rule is a ceiling with no floor** | `20260817_3` ships **0 of 5** 訓読み and the gate prints `ok`; official runs 1–3 and never 0. Three papers are over the cap (4/3/3), grandfathered | half (cap only) |
| F6 | **問題3's twelve options are not required to be twelve different affixes** | 4 of 14 papers repeat an option inside 問題3 (`20260810_2` twice); official **0 of 31**. The identical rule is gated for 問題5 only | scope bug |
| F7 | **Institutional-actor register drift** | institution-only stems 4–36% (median 12%) vs official 0–16% (median 4%); four papers above the archive maximum; 問題2 alone 23% vs 6% | no |
| F8 | **Eleven live 文字・語彙 item repeats across nine paper pairs** | `orthography` 5, `usage` 3, `paraphrase` 2, `context_words` 1 — 3–5 draws apart against cooldowns of 26–47; learner-visible (「宣伝する」 keys 問題6 in two papers, 「果実」「系統」「育児」「歌謡」「努める」 key 問題2) | grandfathered skip |
| F9 | **One live item-level breach**: `20260813_2` 問題1-5 prints 「**頻繁に**」 and no option carries the printed 「に」 | 24 of 25 okurigana-bearing targets comply; this one does not | no |
| F10 | **Three owner-doc numbers are not reproducible** | 問題6 option length (doc 25.0 / 9–35 / n=136 vs measured 26.9 / 13–39 / n=540); 問題5/6 longest-key baseline (doc 15%/16% n=123/124 vs measured 19%/21% n=108/134); the 訓読み cap's window (5 sittings stated as archive-wide) | — |
| F11 | **The declared pool authority has never been read by the pipeline** | four scanned books, no extract, no make target, no per-entry citation — and their 別冊 carry the 音訓 tables that hard-disabled `make matrix`, plus two typeset 語彙 模擬試験 | — |

---

## F1 — the 問題1/2/5 stem stopped being a sentence and became a passage

**Measurement.** JP chars of the stem, bold markers stripped, one parser both sides.

| 大問 | official n | median | mean | range | official current era | generated n | median | mean | range |
|---|---|---|---|---|---|---|---|---|---|
| 問題1 | 155 | 18 | 18.1 | 9–31 | **16** | 70 | 27.5 | 27.3 | 16–40 |
| 問題2 | 155 | 19 | 19.6 | 10–35 | **18** | 70 | 30.0 | 29.5 | 21–41 |
| 問題3 | 129 | 23 | 23.8 | 11–37 | 22 | 42 | 31.5 | 32.3 | 24–45 |
| 問題5 | 141 | 16 | 17.0 | 9–31 | **15** | 70 | 27.0 | 26.9 | 15–42 |

Per paper, over the fifteen 問題1+2+5 stems:

| | min | median | max |
|---|---|---|---|
| official, 31 sittings | **15** | 18 | **22** |
| official, current era | 15 | 16 | **17** |
| generated, 14 papers | **21** | 29 | **32** |

**Every one of the fourteen papers sits above the current era's maximum, and thirteen sit above the maximum of all thirty-one sittings.** The single paper inside the wider band (`20260810_1`, 21) is still above every current-era sitting.

**And the shape, not just the length.** Share of 問題1/2/5 stems containing no 「、」 at all:

| | official all | official current era | generated |
|---|---|---|---|
| 問題1 | 75% | **83%** | **17%** |
| 問題2 | 70% | 74% | **7%** |
| 問題5 | 77% | **82%** | **7%** |
| per-paper share | 45–93% (med 73%) | 60–93% (med 80%) | **0–60% (med 7%)** |

Six papers — `20260807_1`, `20260810_2`, `20260813_2`, `20260814_1`, `20260818_1`, `20260819_1` — print **no comma-free 問題1/2/5 stem at all**. Thirteen of fourteen are below the archive's own minimum.

Official, for contrast: 「この家の柱はしっかりしている。」「なかなか討論が終わらない。」「暑いので、日陰ですずんだ。」「二人の意見は一致していた。」 Ours, from `20260819_1`: 「開会式では、会長が今年の目標について短い**演説**をした。」「市は来年度の予算を見直し、事業費を一割**さくげん**することを決めた。」

**Why it matters.** 問題1 tests a reading and 問題5 tests a synonym; every character of context beyond what disambiguates the target is reading load charged to a vocabulary item. The official stem is one clause with one actor. Ours is a two-clause sentence with a subordinate setup, and that is *systematic* — 83% comma-free became 17%. It also silently moves difficulty: a candidate who cannot parse 「市は来年度の予算を見直し、」 loses a 文字・語彙 mark for a 読解 reason.

**Fix.** Owner: `question-authoring/references/moji-goi.md`, one new subsection covering 問題1/2/5 stems (it currently specifies option sets in detail and says nothing about stems). Band: **per-paper median 15–22 JP chars, author to 17; at least 8 of the 15 stems comma-free**. Gate line: `check_moji_stem_shape` (§Phase 3).

---

## F2 — です・ます is gone from 文字・語彙

**Measurement.** Any polite marker (です/ます/ました/ません/でしょう/ください) anywhere in a 問題1–5 stem, and separately the sentence-final form:

| | official all | official current era | generated |
|---|---|---|---|
| 問題1 sentence-final polite | 27% | **34%** | **0 of 70** |
| 問題2 sentence-final polite | 26% | 29% | 4% |
| 問題4 sentence-final polite | 10% | 8% | 6% |
| 問題5 sentence-final polite | 21% | 17% | 4% |
| per-paper share, any polite marker, 問題1–5 | 8–41% (med 22%) | **16–32%** (med 28%) | **0–16%** (med 6%) |

Twelve of the fourteen papers are below the current era's minimum; six papers print **zero** polite stems across all twenty-five 問題1–5 items (`20260807_1` is at 4%, `20260812_2`/`20260813_2`/`20260814_1`/`20260817_1`/`20260817_2`/`20260819_1` at 0%).

Same axis, first person (私/僕/俺/わたし): official 5% of stems (7% current era), generated **1%** — three stems in 350.

**問題4 is the control.** Official 問題4 is only 8–10% polite, and ours is 6% — statistically the same. So this is not "official is polite"; it is that **問題1/2/5 carry a conversational register that our papers apply nowhere**, while 問題4 (the one section official writes in plain style) matches.

**Why it matters.** This is the 文字・語彙 half of the 読解 finding `REPORT-DOKKAI.md` §F3 records — the paper has one voice, and it is impersonal exposition. It costs the section its cheapest source of variety, and it interacts with F1: a です・ます stem tends to be a single clause about a person, which is exactly the shape F1 asks for.

**Fix.** Owner: `moji-goi.md`, same new stem subsection. Quota: **≥5 of the 25 問題1–5 stems in です・ます, ≥1 first-person stem**, floors taken from the current-era minimum (16%) rather than its median. Gate line: `check_moji_stem_register` (WARN class — it is a distribution).

---

## F3 — 問題2 lost its 和語 branch and became a pseudo-compound grid

`moji-goi.md` §問題2 opens with 「Official uses a **2×2 component matrix**」 and spends the section on grids: 下品, 運河, 下駄, 開港, 濃厚. Then it adds two paragraphs on 「Single-kanji stems with okurigana」 and 「Native compound items」. The paper-level consequence of that emphasis is measurable.

| | official all (n=155) | official current era (n=35) | generated (n=70) |
|---|---|---|---|
| items whose option set carries okurigana/kana (a 和語 verb or adjective target) | **44%** | **40%** | **16%** |
| items where all four options are bare 2-kanji compounds | 51% | 54% | **79%** |
| items where all four options are a single kanji | 3% | 6% | **0%** |
| complete 2×2 grid, among the 2-kanji sets | 80% | **89%** | **100%** (55 of 55) |
| mean option length (chars) | 2.5 | 2.5 | 2.2 |

Per paper, and this is the bright line:

| | 和語 items of 5 | all-2-kanji items of 5 |
|---|---|---|
| official, 31 sittings | **1–3, every sitting** (median 2) | **1–3, every sitting** (median 3) |
| official, current era | 1–3 (median 2) | 2–3 |
| generated | **0–2** (median 1); six papers at **0** | **2–5**; eleven papers at **4 or 5** |

Official 12/2025 問題2, for the shape: 「りゃくして」→縮して/省して/略して/簡して · 「すずんだ」→快んだ/冷んだ/清んだ/涼んだ · 「すくわれました」→嫌われました/敬われました/疑われました/救われました — three of the five items are inflected 和語, and the options run 2 to 6 characters. Ours never prints an option shorter than 2 or longer than 4 characters: the option-length histogram is official {1: 20, 2: 368, 3: 166, 4: 46, 5: 12, 6: 8} against generated {2: 232, 3: 40, 4: 8}.

**Why it matters.** The 和語 branch and the compound grid test different things. A grid item asks 「which of two lookalike kanji spells this on-reading」; a 和語 item asks 「which kanji writes this native word, given its okurigana」 — the discrimination official runs in two of five slots, every sitting, for fifteen years. Eleven of our papers run it at most once and six not at all, so 問題2 has become one puzzle repeated five times. That also explains why our grids are *always* complete: a paper with five compound items has to keep finding clean {A,B}×{C,D} products, and the pool's 249 `orthography` entries are then the binding constraint (which is where F8's repeats come from).

**Fix.** Owner: `moji-goi.md` §問題2 — add a **per-paper composition quota above the grid rules**: ≥1 (author to 2) of the 5 items is a 和語 target with printed okurigana, and **no more than 3 of the 5 may be bare 2-kanji compounds** (the archive's own ceiling in 31 of 31 sittings). Owner: `exam-blueprint` — the `orthography` draw needs the same mechanism `sample_katakana_capped()` already gives 問題5/6, because this is a draw-time property, not a writing choice. Gate line: `check_moji2_composition`.

---

## F4 — 問題4's stem outgrew the archive, and one paper left it far behind

問題4 is officially the *long* section of 文字・語彙 — one comma, a scene, 29.5 chars mean. So the finding is not that our stems are long; it is where they end up.

| | per-paper median | largest single stem |
|---|---|---|
| official, 31 sittings | 17–**35** | **45** |
| official, current era | 24–32 | 42 |
| generated | 25–**66** | **76** |

Seven papers sit above the archive's per-paper ceiling of 35: `20260811_1` **66**, `20260810_2` 43, `20260817_2` 40, `20260813_1` 38, `20260813_2` 37, `20260814_1` 37, `20260810_1` 36. `20260811_1` is not a near miss — its median 問題4 stem is 31 characters longer than the longest single 問題4 stem in thirty-one official sittings, and its longest is 76.

Comma-free 問題4 stems: official 13–16%, generated 3% — the same one-clause loss as F1, but from a lower baseline, so it is a much smaller effect here.

**Why it matters.** 問題4 is where 文脈規定 lives: the stem must fix exactly the axes that exclude the three distractors (`moji-goi.md` §"A time/date/quantity key" states this precisely, after `20260818_1` 問題4-14 shipped an unfixed axis). Length is how that rule fails in the other direction — every extra clause is another axis a reader can vary, and a 66-character stem is a small reading passage whose distractor exclusions no candidate can hold in working memory.

**Fix.** Owner: `moji-goi.md` §問題4 — band **per-paper median 24–35, no single stem above 45**, both from the archive; state next to it that the stem must fix the exclusion axes *in the fewest clauses that do so*, so the two rules point the same way. Gate line: extend `check_moji4_blank_stems`, which already parses this exact section for the （　） contract.

---

## F5 — the 訓読み rule is a ceiling with no floor

`check_mondai1_reading_type_mix()` caps 訓読み at 2 of 5 and its docstring is exemplary: the rule, the incident (`qa-report-20260819_1` F3), the repair, and the shared classifier. It has no lower bound.

Per paper, via `sample_items.is_kun_target()` — the gate's own classifier, imported, so these are the gate's numbers:

| paper | 訓読み of 5 | gate |
|---|---|---|
| `20260807_1` | **4** | WARN (grandfathered) |
| `20260810_1` | **3** | WARN (grandfathered) |
| `20260817_2` | **3** | WARN (grandfathered) |
| `20260810_2` `20260811_1` `20260812_1` `20260813_1` `20260813_2` `20260819_1` | 2 | ok |
| `20260812_2` `20260814_1` `20260817_1` `20260818_1` | 1 | ok |
| **`20260817_3`** | **0** | **ok** |

Pooled: 26 of 70 = 37%, against the 34% `moji-goi.md` records for the current era. So the *corpus* rate is right and the *paper* distribution is not bounded below: `20260817_3` tests five on-reading compounds and no native word, a shape the archive never ships (its own table gives 2/2/1/2/2 across 7/2023–12/2025, minimum 1).

**Why it matters.** Symmetry with F3, and the same reasoning the cap itself uses. The cap exists because a 訓読み-heavy paper stops exercising the 清濁/長短 grid; a paper with zero 訓読み stops exercising word recognition, which is the other half of what 問題1 measures. A one-sided rule reliably produces the opposite monoculture — this is precisely `REPORT-CHOUKAI.md` §F2's mechanism (a "not last" rule producing "always first") in another section.

**Fix.** Owner: `moji-goi.md` §"At most 2 of the 5 問題1 targets may be 訓読み" — becomes **1–2 of 5** (author to 2), the floor drawn from the archive minimum. `sample_kun_capped()` gains the floor at draw time exactly as it has the cap, including on the `--reroll-one` path, and `check_mondai1_reading_type_mix` prints both bounds. Grandfather: `20260817_3` (needs a `kanji_reading` re-draw, tier C).

---

## F6 — 問題3's twelve options are not required to be twelve different affixes

`check_mondai5_option_reuse()` exists because `20260819_1` keyed 「わずかに」 at 問題5-21 and printed it as a distractor at 問題5-23; the docstring records the official rate (0 of 80 options in 5 sittings) and the repair (replace the **distractor**, never the key). The rule is written for 問題5 and the check reads 問題5.

Same measurement, 問題3, whose current-era section is 3 items × 4 options = twelve printed affixes:

| paper | repeated option(s) inside 問題3 |
|---|---|
| `20260810_2` | 「総」 and 「半」 |
| `20260810_1` | 「半」 |
| `20260811_1` | 「各」 |
| `20260813_1` | 「性」 |

Official: **0 of 31 sittings** repeat an option inside 問題3 — and 0 of 31 in 問題2, 問題4, 問題5 or 問題6 either (one 2010s sitting repeats one 問題1 reading). Our other sections are clean too: 0 of 14 papers in 問題1, 2, 4, 5, 6. It is 問題3 alone, and 問題3 alone is ungated.

Related, at corpus scale: 「半」 is printed as a 問題3 option in **6 of the 14 papers** — the only option string that appears in six papers of the same 大問 anywhere in 文字・語彙.

**Why it matters.** With twelve slots, a repeat tells the candidate that the repeated affix is not the key of at least one of the two items it appears in — information from the paper, not from Japanese, which is the exact argument `moji-goi.md` §問題5 makes in Japanese ("21を確信した受験者に23の消去情報を、言語ではなく紙のほうから与えてしまう"). Cheapest finding in this report: one check, generalised from one that already exists.

**Fix.** Owner: `moji-goi.md` — move the "N options, N different words" rule out of §問題5 into a section-agnostic statement, with the official 0-of-31 rate beside it. Gate: rename/extend to `check_moji_option_reuse` over 問題1–6. Repair direction, unchanged from 問題5: replace the **distractor**, because the key is half of a drawn pool entry.

---

## F7 — institutional-actor register drift

Classified every 問題1–5 stem as *personal* (私/家族/友人/昨日/部屋 …), *institutional* (市/会社/課長/予算/事業/申請/制度 …), both, or neutral. Institution-only share:

| | min | median | max |
|---|---|---|---|
| official, 31 sittings | 0% | **4%** | **16%** |
| official, current era | 0% | 4% | 16% |
| generated | 4% | **12%** | **36%** |

Four papers are at or above the archive's maximum: `20260814_1` **36%**, `20260807_1` 28%, `20260810_2` 28%, `20260812_2` 20%. Per 大問, the drift is worst in 問題2 (generated 23% institutional vs official-cur 6%) and mildest in 問題5 (9% vs 6%).

**What it is not.** Workplace *scenes* are fine: stems containing 仕事/会社/会議/職場 lexis run 3–17% per paper (median 7%) against official 0–13% (median 6%). The drift is specifically toward **institutions as the sentence's actor** — 「市は…決めた」「担当者が…した」 rather than 「私の娘は音に敏感で」 — which is the same finding `official_calibration.md` §13 records for 問題8 (63% personal/casual official vs 73% corporate/formal generated), reproduced one section over.

**Why it matters.** It is what makes F1 and F2 hard to fix independently: an institutional actor needs a modifier clause to be specific (hence the comma), and it does not take です・ます naturally. All three findings are one authoring habit.

**Fix.** Owner: `moji-goi.md`, folded into the same stem subsection as F1/F2: **≤4 of 25 問題1–5 stems may have an institution as the actor** (archive maximum), ≥8 personal. This is countable with the two regex classes above, so it can be a WARN line rather than a judgment call.

---

## F8 — eleven live item repeats, all behind one grandfather clause

`cooldown_for()` scales each pool's window to its own depth: `orthography` 47 draws, `usage` 41, `paraphrase` 26, `word_formation` 26, `context_words` 195, `kanji_reading` 303. Against those windows, the fourteen shipped specs contain:

| category | item | papers | draws apart |
|---|---|---|---|
| `orthography` | 歌謡 | `20260807_1`, `20260811_1` | 3 |
| `orthography` | 果実 | `20260807_1`, `20260812_2` | 5 |
| `orthography` | 努める(努力) | `20260807_1`, `20260812_2` | 5 |
| `orthography` | 系統 | `20260810_1`, `20260813_1` | 5 |
| `orthography` | 育児 | `20260810_1`, `20260813_1` | 5 |
| `usage` | 持参 | `20260810_1`, `20260812_2` | 4 |
| `usage` | 大まか | `20260810_2`, `20260812_2` | 3 |
| `usage` | 宣伝する | `20260811_1`, `20260813_1` | 3 |
| `paraphrase` | あらかじめ(事前に) | `20260807_1`, `20260812_1` | 4 |
| `paraphrase` | どなる | `20260810_1`, `20260812_1` | 3 |
| `context_words` | ええと | `20260810_1`, `20260812_1` | 3 |

**Every one of them is inside the legacy window** (draws 1–7, the papers whose `test_spec.json` records `{"cooldown": 2, "legacy": true}`), and the gate says so by name: `skip 20260807_1: rotation claim holds … spec is grandfathered legacy — generated before this gate checked each category against its OWN cooldown_for() window`. Nothing is wrong with that skip: re-sampling an already-authored paper is explicitly banned. What is wrong is that **the skip is where the list stops existing** — no output anywhere names the eleven items, so nobody can see the queue, and a learner taking `20260811_1` then `20260813_1` meets 「宣伝する」 as a 問題6 headword twice.

Also measured, from the printed papers rather than the specs: eight target strings appear in two papers each (six in 問題2 — いくじ/かじつ/かよう/けいとう/つとめる/はかる, plus 問題4 「ええと」 and 問題5 「あらかじめ」), which is the same set seen through the booklet.

**Why it matters.** The repo's own §0 lists "a skipped harvest step that reused a previous seed and shipped a re-skin of an earlier paper with every automated gate green" as a founding defect. This is the softer version: the rotation model was fixed forward, correctly, and the seven papers drawn under the old model still carry its repeats with no visible ledger of what is owed. Two of the eleven (`orthography` 果実/努める in one pair, 系統/育児 in another) are *pairs* inside the same two papers, which is what makes them noticeable in a booklet rather than in a diff.

**Fix.** Owner: `exam-blueprint` "Rotation model" — the legacy exemption keeps its skip but gains a **named list**, printed by a new `check_legacy_item_repeats` as a standing WARN with one line per repeated item, removable only when that item's paper is re-drawn (tier C). This is the "grandfather sets are a queue, not an amnesty" rule the dokkai plan states, applied to the one exemption that currently hides its contents.

---

## F9 — one live item-level breach: 「頻繁に」

`20260813_2` 問題1-5 prints 「戸締まりを **頻繁に** 確かめる」 and offers ひんはん / びんぱん / びんはん / ひんぱん. The underlined span ends in 「に」; **no option does.**

`moji-goi.md` §問題1 is explicit twice over: the underline covers the whole word including its tail, and 「when the target has okurigana … **all four options MUST share that exact okurigana**」. The compliant version of exactly this shape is in the newest paper — `20260819_1` 問題1-5 prints 「**常に**」 against すでに / ただちに / しだいに / つねに.

Across all fourteen papers, 25 問題1 targets print a kana tail and **24 of 25 share it across all four options**. This is the one exception, and no gate reads the relation between the printed span and the option field.

**Why it matters.** It is not a difficulty question, it is a well-formedness one: the paper asks for the reading of 頻繁に and every available answer reads 頻繁. A candidate who reasons correctly finds no correct option.

**Fix.** Tier A repair on that item's option field (append 「に」 to all four, or reroll the target), plus a gate line `check_moji1_okurigana_exposure` comparing the printed bold span's kana tail against the four options — three lines, and it reads data both `check_moji2_option_glyphs` and `check_mondai1_reading_type_mix` already load.

---

## F10 — three numbers in the owner docs cannot be reproduced

Per `AGENTS.md` §0, a disagreement between a written number and the corpus is the defect. Three, in decreasing order of consequence:

**1. 問題6 option sentence length.** `official_calibration.md` §7 (quoted verbatim by `moji-goi.md` §問題6) says: 「mean 25.0, median 25, range 9–35 JP chars (n=136)」. Same corpus, my parse:

| parse | n | mean | median | range |
|---|---|---|---|---|
| every official option sentence | **540** | 26.9 | 27 | **13–39** |
| the key sentence only | 135 | 27.0 | 27 | 15–38 |
| per-item mean of the four | 135 | 26.9 | 27.2 | 14.8–36.5 |

No parse I can construct yields 25.0, a minimum of 9, or n=136. The consequence is written into `moji-goi.md`: 「**a 9-char option is official, so short alone isn't a defect**」 — advice resting on a minimum I cannot find, where the shortest of 540 official option sentences is 13. Our papers, for reference, measure mean 26.7 / median 27 / range 14–40, i.e. correct against my parse and 7% long against the doc's.

**2. The 問題5/6 longest-key baseline.** `check_moji_longest_key_rate`'s failure message says 「official is 15% (問題5, n=123) and 16% (問題6, n=124) over 31 sittings」. Same definition — uniquely-longest key, length-varying items only — my parse gives **19% (20/108)** and **21% (28/134)**. The threshold (≤30%) is unaffected and no paper's verdict changes, so this is a message-accuracy defect, not a gate defect. Worth fixing because it is the number an author calibrates to: our papers run 0–29%, and against 19/21% several of them are *under*-shooting rather than safely inside.

**3. The 訓読み cap's evidence window.** `moji-goi.md` §問題1 states, in adjacent sentences, 「Official's current era runs **2 / 2 / 1 / 2 / 2 of 5** (7/2023–12/2025) and never exceeds two」 (five sittings) and 「the calibration table … counts **12 訓読み among 35** current-era items (34 %)」 (seven sittings). 2+2+1+2+2 = 9 of 25, not 12 of 35, so the two lines measure different windows and only one of them is the window the cap is asserted over. And it **cannot be extended**: the archive loses the underline, so no official 問題1 target is recoverable from `booklet.md` (§corpus fact 1). The cap may well be right — it is not currently checkable, and the honest statement next to it is "five sittings, hand-classified", not "official never exceeds two".

**Fix.** Owner: `official_calibration.md` §7 and §12 plus the gate docstring. Every number gets its parse rule written beside it, the way §0 already promises and `choukai-audio/references/official_pacing.md` §6 actually does. Mechanism: §Phase 1's `tools/goi_profile.py --baseline` prints these tables so the docs are a paste, not a retype.

---

## F11 — the declared pool authority has never been read by the pipeline

`AGENTS.md` §3 is unambiguous: Shin Kanzen's 語彙/漢字 volumes together with both Soumatome volumes are 「exam-blueprint's **ONLY** vocabulary/kanji pool authority (`pools.json`'s `kanji_reading`, `context_words`, `paraphrase`, `usage`)」 since the vendored OpenJLPT corpus was deleted on 2026-08-11.

**What exists on disk:** four scanned PDFs with no text layer. No extract, no `make` target, no script under `tools/` or any skill, and no citation field in `pools.json` (§corpus fact 4). Since 2026-08-11 the repo has therefore had a pool authority that nothing can query and an authoring rule ("check all four options against the books") that leaves no evidence — `moji-goi.md` says so itself: 「the written source-and-branch line IS the check, the author's, not the gate's」. In practice those lines cite the book by name and never a page: `20260819_1`'s key rows read 「Shinkanzen N2漢字の見出し語」 thirty times with no page number, so they are unverifiable by a later reader.

**What is in the books** (read for this audit, from the front matter and 目次 of three of the four):

*Shin Kanzen マスター N2 語彙*, 246 pp, 2,283 headwords selected from the NTT『日本語の語彙特性』database:
- 実力養成編 第1部 話題別 (9章/21課): 人間 · 生活 · 趣味・娯楽 · 旅行 · 教育と仕事 · メディア · 社会 · 科学 · 抽象概念 — a topic taxonomy with 数量/時間・空間 sub-chapters.
- 実力養成編 第2部 性質別 (7章/16課): **意味がたくさんある言葉** (動詞①② · 形容詞・名詞) · **意味が似ている言葉** (副詞・形容詞 / 名詞・動詞) · **形が似ている言葉** · 副詞 (程度・時間・頻度 / 後ろに決まった表現が来る副詞 / まとめて覚えたい副詞) · オノマトペ · 慣用表現 (体の言葉①②) · **語形成** (二つの言葉をプラス / 単語の前に漢字 / 単語の後ろに漢字 / 形容詞から作る動詞と名詞).
- **模擬試験 第1回 (p.186) と 第2回 (p.188)** plus 別冊解答 — two complete, exactly typeset N2 語彙 papers, and it names the four item types the way the exam does (文脈規定 / 言い換え類義 / 用法 / 語形成).

*Shin Kanzen マスター N2 漢字*, 253 pp: ステップ1–3 (第1回〜第53回), 総合問題 ×2, 「広がる広げる漢字の知識」 = 接辞 · 読み方と意味 · 言葉の構成 · **音の変化**, with チャレンジ sets for each; **別冊1 漢字表 = 学習漢字リスト · 特別な読み方をする漢字の言葉 · 訓読みが二つ以上ある漢字 · 音読みが二つ以上ある漢字**; 別冊2 解答と解説. Its はじめに also records that it promoted **28 former 1級 kanji** into its N2 band — directly relevant to the band arguments this repo keeps re-litigating (「飢」, 「饉」).

*日本語総まとめ N2 語彙*, 156 pp, ~1,400 words, 8週×7日 with a 実戦問題 每週 and a 別冊解答・解説 carrying EN/ZH/KO glosses: 第4週 is a whole week of 副詞; 第5週 「やさしい漢字で書きますが…」 (物事 · 日中 · 年月 · 夜中 · 世間 · 作業 · 一生 · 用心 · 見事 · 土地 · 名字 · 発売 · 手品 · 合図 · 強気 · 本気 · 気楽 · 目安) is the 問題1/問題2 target band exactly; 第6週 カタカナで書く言葉①②③ + 似ている言葉①②③; 第7週 意味がたくさんある言葉①②③ + 言葉の前につく語 / 後ろにつく語; 第8週 組み合わせの言葉 + よく使われる表現.

**Four open problems whose data is sitting in those 別冊:**

| Open problem in this repo | What answers it |
|---|---|
| `make matrix`'s two generators are **hard-disabled** because 「they had no 音訓 table and emitted kana-skeleton-violating grids」 (`AGENTS.md` §4, qa-report-20260819_1 F4) | Shin Kanzen 漢字 別冊1: 音読みが二つ以上ある漢字 (and 音の変化 for 清濁/長短/促音) |
| The two-訓読み rule (「key the LOWER-graded one; never print the other」) lost its gate on 2026-08-11 and is now author diligence | Shin Kanzen 漢字 別冊1: **訓読みが二つ以上ある漢字** — the list the rule is about |
| 問題6's multi-sense trap (`20260811_1` 落ち着く: "person calms down" vs "value settles") is a per-item judgment with no list | 意味がたくさんある言葉 — three 課 in Shin Kanzen, three days in Soumatome |
| The two-branch distractor rule needs same-field and same-shape families and has no source for them | 意味が似ている言葉 / 形が似ている言葉 / 似ている言葉①②③ |

Plus the corpus gap F10.3 names: two typeset 語彙 模擬試験 are the only place in `refs/` where a **complete 問題1–6 paper with its targets marked** can be read at all.

**Fix.** §Phase 7: two extractors (`tools/extract_shinkanzen_goi.py`, `tools/extract_kanji_tables.py`) reusing the Vision-OCR path `extract_jlpt_n2_new.py` already drives, emitting `refs/Shinkanzen/goi_reference.md` and `refs/Shinkanzen/kanji_tables.md` (+ a Soumatome counterpart) in the same fenced `[OCR ▼]…[OCR ▲]` shape with the same "not quotable as exact wording" header; `make extract-shinkanzen-goi` / `make extract-kanji-tables` in `AGENTS.md` §4; then re-enable `matrix_helper.py`'s generators against the real 音訓 table, and add a `provenance` field to `pools.json` entries as they are confirmed.

---

## What is healthy — measured, not assumed

Everything below was measured on both corpora and shows **no defect**. Several are the axes I expected to fail.

- **Answer positions.** Per 大問, generated keys sit at 21–31% per position (問題1 27/24/23/26, 問題2 23/26/26/26, 問題4 29/23/22/26, 問題6 23/27/24/26); official runs 21–29% over 31 sittings. No clustering anywhere in 文字・語彙.
- **問題5/6 longest-key rate.** The gate reports 0–29% per paper; official is 19%/21% under my parse (15/16% under the docstring's). Inside either baseline in all 14 papers.
- **問題6 option sentence length.** Generated mean 26.7, median 27, range 14–40, 2% above 35; official mean 26.9, median 27, range 13–39, 4% above 35. The same distribution — and the reason F10.1 is a doc defect rather than a paper defect.
- **問題6 word-form consistency.** Exactly one option in a different word form: generated 13%, official current era 13% (11% over all 31). The two shipped breaches (`20260811_1` 問題6-26 bare noun vs three suru-forms, `20260817_2` 問題6-28 民間的な vs three bare) were real and were fixed; they are **not** a corpus-level pattern, and official ships the same shape at the same rate — 12/2025 問題6-28 「貢献」 prints three 「大きく貢献した/する」 against one 「貢献し、」. My classifier's resolution is coarse (it buckets 〜に/〜な/〜だ together), so the honest statement is "indistinguishable from official at this resolution".
- **問題1 option-set structure.** Derivation-type sets (all four readings within edit distance 2 — the 清濁/長短 grid) are 66% of our items against 74% current-era / 63% all-era official; normalised set tightness is 0.48 on both sides; shared kana suffix 67% vs 66/67%. The worry behind F5's cap — that our 問題1 stopped exercising the on-reading grid — **does not reproduce at corpus level**, only per paper.
- **Blind strategies.** Six strategies (longest, shortest, modal length, commonest-kanji, stem overlap, least-like-peers) × six 大問, chance 25%. 22 of the 36 cells are within 5 pp of official and most sit at chance. Where we differ we are usually *less* solvable: 問題1 "pick the longest reading" scores 32.6% on the current-era archive and **19.6%** on ours.
- **The one strategy above official**: 問題4 "pick the option built from the commonest kanji" scores **32.1%** on our papers against 23.1% all-era / 26.7% current-era official; per paper ours runs 14–55% (median 30%) against official 4–43% (median 25%). Two papers (`20260812_2` 55%, `20260817_3` 51%) are above the archive maximum. With seven items per paper this is a corpus-level signal only — worth one WARN line in Phase 3, not a repair.
- **Glyph inventory.** `check_moji2_option_glyphs` is green on 13 of 14 papers; `20260811_1` is the single by-name exemption. The 2026-08-19 rule works.
- **Within-paper option reuse** outside 問題3 (F6): 0 of 14 papers in 問題1, 2, 4, 5, 6.
- **問題4 option grain.** Any option carrying a particle 23% vs 20% current-era official; all-four-idiom sets 5% vs 4%; all-kana (adverb/mimetic) sets 18% vs 27% — the one mild gap, and inside the all-era band.
- **Katakana headwords.** 問題6 4% (3 of 70) vs official 3% current era / 1% all; 問題5 1% (1 of 70) vs the archive's 8.6%. `sample_katakana_capped()` is doing its job, and if anything 問題5 is now slightly under-drawn.
- **問題3 affix shape.** All-single-kanji affix sets 71% vs 76% current-era / 82% all-era official; mean affix length 1.35 vs 1.32; suffix-position items 64% vs 52%. Close enough to leave alone.
- **問題4 blank contract.** Every 問題4 stem prints （　） and no stem prints its key — `check_moji4_blank_stems` green on all 14.
- **Overlap between our items and the archive's.** Five of 67 generated 問題6 headwords (分解, 普及, 着々, 行方, 順調) also appear as official 問題6 headwords. That is shared N2 vocabulary, not copying: no option sentence resembles the archive's.

---

## Recommended order of work

1. **Fix F6 and F9 first.** One generalised check plus one item's option field, and both are literal breaches of rules already written. Cheapest learner-visible improvement in this report.
2. **Settle F10's three numbers** before any quota is authored against them (§D1). F10.1 is currently telling authors that a 9-character 問題6 option is official.
3. **Make F5's rule two-sided** and give F3 its per-paper quota — both are draw-time properties, so they belong in `sample_items.py` before they belong in a gate.
4. **Add the stem contract** (F1, F2, F4, F7 are one authoring habit and one new `moji-goi.md` subsection). This is the largest quality change and the most expensive to comply with.
5. **Publish F8's queue** — the eleven legacy repeats become a named list that shrinks, instead of a skip line.
6. **Extract the books** (F11) and re-enable `make matrix`'s generators against a real 音訓 table.

---

## Method, and what I did not do

- **Parsers.** One record type from both sides, `{corpus, paper, mondai, no, stem, options[4], key}`. Official: the 文字・語彙 region is located by the 問題1 instruction line and bounded by the 問題7 one (headings are unreliable — 12/2022 prints 「間題 4」 with no `###` and loses its 問題5 heading entirely), items are driven by each sitting's own `answer_keys.json` numbering rather than an assumed era, options are assigned to slots (not sequence) so the two-column 問題5 layout parses, full-width digits are normalised, and a short all-kana line following a kanji-final line is dropped as ruby. Generated: `^\*\*(\d+)\*\*` stems, `^\s*[1-4][.、]` options, keys from whichever of the three key-table shapes on disk that paper uses (`| 問題N | no | key |`, `| no | key |`, or the combined `# 解答(言語知識・読解)` table).
- **Coverage.** 934 of 964 official items (96.9%); 12 further records dropped where an option parsed longer than 45 characters (a swallowed continuation), leaving 922. The 30 unparsed items are almost all 問題5 rows in `2. N2 7-2011`, `2. N2 12-2011`, `3. N2 7-2012` and `14. N2 12-2023`. All 420 generated items parsed with all four options and a key.
- **Windows.** 文字・語彙 is far more era-stable than 読解 — only 問題3 changed count (5→3 items) — so most numbers are quoted over all 31 sittings **and** over the 7 current-era sittings, and the finding names which one it rests on. Where they disagree the current-era figure is the tighter one and the one a quota should use.
- **Classifiers, all stated and applied identically to both corpora:** 訓読み via `sample_items.is_kun_target()` (imported, so it is the gate's own classifier, and it reads spec entries — it cannot be run on official items, §F10.3); register by two regex classes printed in §F7; 和語 問題2 items by "any option contains hiragana"; grid completeness by {first char}×{second char} over 2-kanji options; option-set tightness by mean pairwise Levenshtein over mean length; glyph frequency from all 31 booklets' kanji counts.
- **Not done: no per-item answerability review.** Whether a specific 問題4 stem admits two options, or a 問題6 wrong sentence is secretly attested, is `exam-qa-review`'s job and is deliberately out of scope. This audit measures *distributions*.
- **Not done: no band judgment.** I did not decide whether any key is N2. That needs the books (§F11) and it is the one thing the deleted OpenJLPT corpus used to fake.
- **Not done: the ruby question.** Our papers carry no furigana in 言語知識・読解.md and the archive's 文字・語彙 region carries 3–53 ruby lines per sitting. I could not establish from `refs/` whether that ruby is JEES's or the reproducer's, so no finding was made either way; it is recorded in §corpus fact 2 as an open question.
- **Not done: no repair.** Nothing on disk was changed. `make check` was run once, to state what the gate currently sees (green, 138 warnings).

---

# Remediation plan

Ordered so that nothing is authored against a number that later moves, and so the
expensive step — rebuilding a paper's model answer and its translation — happens
exactly once per paper. Each item names the **owner file** the rule belongs to, the
**gate line** that makes it observable, and the **acceptance test** that says it is done.

Conventions this plan follows, from `AGENTS.md` §4 and the two sibling plans in
`REPORT-CHOUKAI.md` / `REPORT-DOKKAI.md`:

- A rule has **one owner file**; every other file points at it.
- The **authoring target is tighter than the gate**. The gate FAILs only outside the
  archive's whole range; the target is the archive's median.
- A new gate line that existing papers breach ships with a **named grandfather set**,
  and the set is named **in the owner doc too**. A set is a queue, not an amnesty
  (§F8 is what happens when it is neither).
- **文字・語彙 has one property the other two sections do not: most of its rules are
  draw-time properties, not writing choices.** 和語 share, 訓読み count, katakana rate
  and item rotation are decided by `sample_items.py` before an author writes a word.
  Where a finding can be enforced at draw time it is enforced there **and** re-checked
  by the gate — that is the shape `sample_kun_capped()` + `check_mondai1_reading_type_mix()`
  already has, and every new quota in Phase 2.3 copies it.
- **The rebuild chain is the expensive leg.** Any edit to a stem, an option or a key in
  `言語知識・読解.md` makes three downstream artifacts stale: `詳細解説.json` (the gate
  FAILs option drift), every `詳細解説.<lang>.json` (**all 14** papers ship `vi`), and
  `模範解答.html`. **Batch every edit to one paper into one pass.**

### Autonomy contract — the agent runs this without asking

Every "decision" below is a **decision rule with a bright line**, not a question to
escalate: D1 is settled by measurement, D2 by the archive's own envelope, D3 is a
policy with thresholds, and §5.0's tier is derived from the artifact a repair touches.
An agent that reaches a fork not covered by a rule extends the rule in the owner file
and says so in its final report — it does not stop.

**Decides for itself, and never asks:** which findings exist and at what tier; which
papers get tier A/B/C work; the replacement numbers D1 produces; what to write in every
repaired stem and option; which RNG seed a re-draw uses; when to batch a paper's
rebuild; which ids enter or leave a grandfather set (an id leaves only when that paper
is actually repaired); and **committing each completed step**.

**Out of scope, so not questions either:** pushing to a remote; editing anything under
`refs/` (it is the measuring stick); deleting a check (this plan only adds and
re-thresholds, with the reason recorded); and **hand-substituting a drawn item** — the
repair for any pool-origin defect is `sample_items.py --reroll <cat>` or
`--reroll-one <cat>:<index>` with a fresh seed, never a hand-picked word, however sound
(`exam-blueprint` "Rotation model"; the `居酒屋`→`潔い` incident is the founding case).

**One sequencing rule that replaces an escalation:** a repair that moves a paper's KEY —
a re-draw (tier C), or an option-field rewrite that changes the key's option number —
requires an `exam-qa-review` blind solve of 文字・語彙. **It is its OWN step, never the
tail of the authoring step**, because `AGENTS.md` §5's non-negotiable rule is that QA
runs in a context that authored nothing. The authoring step therefore ends by queuing
`P5Q-<id>-moji` with `deps: [the authoring step]`, and the next runner performs it with
the paper's text as its only input.

**Reports, per `AGENTS.md` §0.7:** skills read, phases run, papers touched, papers still
queued and where they sit in D3's order, every grandfather id added or removed, and the
`make check` output read line by line — written to `qa/goi-remediation-report.md`. A
`declined` status is reserved for a step the measurement showed was a false positive,
with the measurement recorded; it is never "we chose not to fix this paper".

---

## Phase R — running this unattended

Same shape as the choukai and dokkai plans, and it shares their state-file design so the
three can run in any order — **never simultaneously**, because all three edit the same
`言語知識・読解.md` files and the same `詳細解説.json`. The lease is what enforces that.

- **State file** `logs/goi_remediation_state.json`, tracked:
  `{plan_source, plan_sha, max_steps_per_run, steps:[{id, deps, status, artifact, tier,
  test_id, needs_rebuild, gate_expected}], runs:[…], runner:{lease, at}}`.
  `status ∈ todo | doing | done | blocked | declined | stale`.
- **Step granularity: one paper, one tier, one artifact.** Never larger.

| Step shape | Example id | Ends with |
|---|---|---|
| one tool/doc change | `P1-profile`, `P2.1-stems` | `make check` green |
| one paper's tier A | `P5A-20260813_2-mondai1-5` | booklet + sheet + 詳細解説 + vi + model-answer for that id |
| one paper's tier B | `P5B-20260814_1-stems` | same, plus every 解説 cell quoting a rewritten stem re-checked |
| one paper's tier C | `P5C-20260817_3-kanji_reading` | same, plus `test_spec.json` + `logs/ledger.json`, plus a queued `P5Q-*` blind solve |

- **The batch boundary IS the paper.** A step that edits a paper and stops before
  `make model-answer` leaves the gate red on that id; record `gate_expected` if a step
  must be interrupted mid-chain.
- **Every run starts by reconciling, not trusting:** `git status`; `make check` read line
  by line; compare failures against `state.gate_expected`; re-derive any stale `doing`
  step by *measuring* the paper (`tools/goi_profile.py --tests <id>`), never by trusting
  the flag; a twice-failed step becomes `blocked` with its error text and the run moves on.
- **Restart:** a cron routine every 4–6 h with a fixed, stateless prompt (all state is on
  disk), or self-paced `/loop` for an interactive burst — never both; a runner finding a
  fresh foreign lease exits. The routine deletes itself when no `todo`/`doing` remains.
- **One commit per completed step**, message naming the step id
  (`goi(P5A-20260813_2): give 問題1-5 options the printed 「に」`).

### R.8 What still needs a human — three things, and none of them is a decision

1. **Start it, and pre-authorise it.** Someone types the first prompt and gives the
   harness standing permission to run `make`, edit `tests/`, and `git commit`.
2. **Publish.** Pushing and deploying `_site/` are out of scope by design.
3. **Judge two things no gate can.** Whether a rewritten stem reads like natural
   Japanese, and whether a re-drawn key is genuinely N2. The second is the one place this
   plan is weaker than the dokkai plan: 読解 findings are all text-measurable, and
   **band judgment is not** — it needs the books, which is why Phase 7 is not optional
   here the way it is there. Until the extracts exist, a tier-C re-draw's band check is
   an author reading a scanned page, and the final report names every re-drawn key as a
   review list.

**The one structural requirement.** "Fresh eyes" is a *context* requirement, not a human
one (`AGENTS.md` §5): the runner needs either subagents, or step granularity fine enough
that authoring and blind-solving land in different firings. §R's one-paper-one-tier rule
plus the queued `P5Q-*` steps give the second for free.

---

## Phase 0 — three decisions the plan makes by rule

### D1. One parse owns each measured number

**Problem.** Three numbers the 文字・語彙 rules are built on cannot be reproduced as
stated (§F10): the 問題6 option-length band (25.0 / 9–35 / n=136 against a measured
26.9 / 13–39 / n=540), the 問題5/6 longest-key baseline (15%/16% against 19%/21%), and
the 訓読み cap's window (five sittings written as archive-wide, and unextendable because
the archive loses the underline).

**Decision, by rule.** Phase 1 builds one measurement script. Then, per number:

1. If the script reproduces the doc, the doc keeps its number and gains the parse rule
   beside it.
2. If it does not, **the doc is edited to what the script prints**, with the parse rule
   and the corpus window named on the row, and the old number recorded in a one-line
   history note (the house style `official_pacing.md` §6 already uses).
3. A number that *cannot* be measured from `refs/` at all — the 訓読み cap is the only
   one — is relabelled with its real evidence base ("five sittings, hand-classified,
   2026-08-19") and a pointer to what would settle it (Phase 7's 模擬試験 extract).
   **A cap whose evidence is five sittings stays a cap; it does not stay an assertion
   about the archive.**

No quota in Phase 2 may cite a number Phase 1 has not printed.

### D2. A one-sided rule becomes a band, always

Two findings in this report (F5's 訓読み cap, and F3's grid emphasis) and one in each
sibling report have the same shape: a rule with one bound produced a monoculture against
the other bound. So the plan adopts it as a rule about rules:

**Every 文字・語彙 composition rule ships as a band whose two ends both come from the
archive's per-paper distribution** — floor at the archive minimum, ceiling at the
archive maximum, author target at the median. Concretely, this converts:

| rule today | becomes |
|---|---|
| 訓読み ≤2 of 5 | **1–2 of 5** (archive 1–3, author to 2) |
| "問題2 uses a 2×2 grid" (no count) | **≤3 of 5 bare-compound items, ≥1 和語 item** (archive 1–3 and 1–3) |
| "keys must not be the longest" (≤30%) | keeps its ceiling, gains a **floor of 10%** (measured 19%/21% official) so a paper cannot key the shortest option every time |
| no stem rule at all | **median 15–22 chars, ≥8 of 15 comma-free, ≥5 of 25 polite, ≤4 of 25 institutional** |

Where a band's floor would fail an official paper, the floor is wrong (§AGENTS.md §0).
Where a band has only one archive-derived end, the other end is stated as "not measured"
rather than invented.

### D3. Repair scope — all fourteen papers, ordered rather than filtered

Every paper breaches at least four of the ten measured columns (§5.4), so a filter would
be a fiction. Order instead, by learner-visible cost:

1. **Literal breaches of a written rule**, wherever they are: `20260813_2` 問題1-5
   (§F9), the four 問題3 option repeats (§F6). Tier A, hours.
2. **`20260811_1`**, whose 問題4 stems (median 66) are outside every other paper's range
   as well as the archive's. One paper, tier B.
3. **The six 問題2 zero-和語 papers** and **`20260817_3`** (zero 訓読み) — tier C, because
   they need a draw, and they are the papers whose sections test one thing five times.
4. **The four institutional-register papers** (`20260814_1`, `20260807_1`, `20260810_2`,
   `20260812_2`) — tier B, and F1/F2/F4 come along in the same pass.
5. **The remaining papers' stem pass** — tier B, one paper per session.
6. **The seven legacy-repeat papers** — tier C, and last, because a re-draw of an
   already-authored item is the most expensive repair in the repo and the least visible
   to a single test-taker.

A paper is never partly repaired across a gate run: a step covers one tier of one paper
and ends with that paper green on the checks its tier owns.

---

## Phase 1 — `tools/goi_profile.py`: one measurement, two consumers

**Why first.** Every conflict in D1 has the same cause: the numbers live in prose, the
gate re-implements them, and nothing forces the two to agree.

**Build it.** New file, repo-level (it measures `refs/` and `tests/`, so it is not a
skill script — same class as `tools/check_consistency.py` and the sibling plans'
`choukai_profile.py` / `dokkai_profile.py`):

```
tools/goi_profile.py [--official] [--tests <id>…] [--era cur|all] [--json] [--baseline]
```

- **One parser, two front-ends**, producing the same record from
  `refs/JLPT_N2_NEW/*/booklet.md` and `tests/*/言語知識・読解.md`:
  `{section, no, stem, options[4], key, target?}`. Region located by the 問題1
  instruction line and bounded by the 問題7 one; item numbering from each sitting's own
  `answer_keys.json`; slot-assigned options (two-column 問題5 and ruby-split option rows
  both parse); full-width digits normalised; ruby lines dropped by the stated rule.
  **`target` is `None` for official 問題1/2/5** — the script must say so rather than
  guess, because that absence is F10.3.
- **Emit every number this report used**, per paper and pooled: stem length by 大問 and
  the 問題1/2/5 per-paper median; comma-free share; polite and first-person share;
  register classes; 問題2 和語 / bare-compound / grid-completeness / option-length
  histogram; 問題3 affix shape and option distinctness; 問題4 stem band, option grain,
  particle and katakana rates; 問題5 grain and phrase share; 問題6 sentence lengths, key
  rank and word-form classes; key positions per 大問; the six blind strategies; 訓読み
  counts via the imported `sample_items.is_kun_target`; and cross-paper item repeats
  read from `logs/ledger.json` against `cooldown_for()`.
- **`--baseline`** prints the official tables in the exact Markdown `moji-goi.md` and
  `official_calibration.md` carry, so refreshing a doc is a paste, not a retype.
- **`check_consistency.py` imports it** instead of re-implementing counts. The gate keeps
  owning the **thresholds**; the script owns the **measurement**.
- **Reuse, do not duplicate:** `jp_char_count()`, `gengo_option_sets()` and the section
  regexes already live in `check_consistency.py` and are the committed definition of
  every count in the repo; `sample_items.is_kun_target()` and `cooldown_for()` are the
  committed definitions of 訓読み and rotation. Import all five.

**Acceptance test:** `python3 tools/goi_profile.py --official --baseline` reproduces
every official figure in `official_calibration.md` §§5, 7, 12 and `moji-goi.md`'s tables,
**or the doc is edited to what it prints, with the parse rule named on the row** (D1).
Then `make check` is green and its 文字・語彙 numbers are byte-identical to the script's.

**Effort:** the largest single item in this plan (~400–600 lines); most of it exists
already as the audit scripts behind this report.

---

## Phase 2 — rule changes, by owner file

### 2.1 `moji-goi.md` — the stem contract (F1, F2, F4, F7)

The file specifies option sets in exhaustive detail and **says nothing about the stem**
except that 問題4 must carry （　） and must not print its answer. That gap is four of
this report's findings. Add one subsection, "The stem", above §問題1:

| Rule | Archive | Author target |
|---|---|---|
| 問題1/2/5 stem: one clause, one actor | per-paper median 15–22 chars (current era 15–17) | **17** |
| …at least 8 of the 15 comma-free | per-paper 45–93% (cur 60–93%) | **≥60%** |
| ≥5 of the 25 問題1–5 stems in です・ます; ≥1 first-person | 8–41% (cur 16–32%); 5–7% first person | **7 stems** |
| ≤4 of 25 stems with an institution as the actor | 0–16% (median 4%) | **≤2** |
| 問題4 stem: median 24–35, no single stem above 45 | 17–35, max 45 | **28** |

State the reason next to the 問題4 row, because the two rules there pull against each
other: the stem must fix every axis that excludes a distractor
(§"A time/date/quantity key") **in the fewest clauses that do so**.

### 2.2 `moji-goi.md` — section composition quotas (F3, F5, F6)

| # | Rule to add / change | Archive | Gate? |
|---|---|---|---|
| F3 | 問題2: **≥1 和語 target with printed okurigana** (author 2), **≤3 of 5 bare 2-kanji compounds** | 1–3 and 1–3 in **31 of 31** sittings | yes |
| F3 | State that the 2×2 grid is a **device, not the format** — the archive completes it in 80% (cur 89%) of its compound items, and 51% of its 問題2 items are not compound at all | 44% 和語 / 51% compound | WARN |
| F5 | 問題1 訓読み becomes **1–2 of 5** | 1–3, never 0 | yes (extend) |
| F6 | The "N options, N different words" rule moves out of §問題5 and becomes section-agnostic for 問題1–6 | 0 repeats in 31 sittings, any 大問 | yes (extend) |
| F9 | Restate the okurigana rule as a **relation between the printed span and the option field**, not a property of the options: the bold span's kana tail must appear in all four options | 24/25 compliant on our side | yes |
| — | 問題5/6 longest-key rate gains a **floor of 10%** (D2) | 19% / 21% measured | WARN |

### 2.3 `exam-blueprint` — the draw-time half (F3, F5, F8)

Four of this report's findings are properties of a draw, and the mechanism for enforcing
them already exists — `sample_katakana_capped()` puts 問題5/6 katakana headwords at the
measured 5.7% rate instead of the pool's raw 30%. Copy that shape:

- **`sample_wago_floor()`** for `orthography`: at least one drawn entry must be a 和語
  target with okurigana, at most three may be bare 2-kanji compounds. The classifier is
  one regex on the entry string and must be **shared with the gate**, as
  `is_kun_target()` is.
- **`sample_kun_capped()` gains the floor** (1–2 of 5), including on the `--reroll-one`
  path, so a single redraw cannot empty the 訓読み slot the way it cannot overfill it.
- **The legacy exemption gains a named list** (§F8): `logs/ledger.json` already holds
  every draw, so `check_legacy_item_repeats` needs no new data — only a printed queue.
- **`pools.json` gains an optional `provenance` field** per entry, filled as Phase 7's
  extracts confirm entries. Not a schema break: absent means unconfirmed, which is the
  honest current state of all 3,673 strings.

### 2.4 `official_calibration.md` — the three numbers (F10)

§7's 問題6 row, §12's neighbourhood, and the 問題5/6 longest-key baseline are rewritten
from `--baseline` output, each with its parse rule and corpus window on the row. §5's
問題1 distractor table gains the sentence that the underline is not in the extract, so
its 訓読み/音読み split is a hand classification of five sittings — the single most
load-bearing unmeasurable number in 文字・語彙.

### 2.5 `exam-qa-review` — two lines the gate cannot decide

- The blind-solve pass gains a **stem-shape read**: before solving, count the 問題1/2/5
  stems that carry a comma and the ones in です・ます, and compare against §2.1's bands.
  Two counts, thirty seconds, and it is the only way a human-facing pass sees F1/F2 on a
  single paper.
- **A re-drawn key's band is a named QA question**, not an author's silent judgment
  (R.8.3): every tier-C repair lands in the report as "key X drawn, band checked against
  <book, page>", and QA reads that line.

---

## Phase 3 — gate lines, so none of this can regress silently

New and extended checks in `tools/check_consistency.py`, each importing its measurement
from Phase 1. House style: the docstring carries the incident, the failure message
carries the repair, the threshold sits outside the archive's whole range, and every
breaching paper is named in a grandfather set the owner doc also names.

| Check | Measures | FAIL / WARN | Grandfathered |
|---|---|---|---|
| `check_moji_stem_shape` | per-paper median 問題1/2/5 stem; comma-free share | FAIL median >22 or comma-free <45%; WARN >18 or <60% | **all 14** (13 on each half) |
| `check_moji_stem_register` | polite share, first-person count, institution-actor count over 問題1–5 | FAIL polite <8% or institutions >4 of 25; WARN polite <16% | 8 papers on polite; `20260814_1`, `20260807_1`, `20260810_2`, `20260812_2` on register |
| `check_moji4_stem_band` (extends `check_moji4_blank_stems`) | 問題4 per-paper median and max | FAIL median >35 or any stem >45; WARN >32 | median: 7 papers; max: `20260810_1`, `20260810_2`, `20260811_1`, `20260813_2`, `20260817_2` |
| `check_moji2_composition` | 和語 items, bare-compound items, grid completeness | FAIL 和語 =0 or compounds >3; WARN compounds =3 with 和語 =1 | 和語: `20260810_1`, `20260810_2`, `20260813_1`, `20260817_1`, `20260817_2`, `20260819_1`; compounds: 11 papers |
| `check_mondai1_reading_type_mix` (extend) | 訓読み count, **both bounds** | FAIL outside 1–2 | over: `20260807_1`, `20260810_1`, `20260817_2` (already listed); under: `20260817_3` |
| `check_moji_option_reuse` (generalises `check_mondai5_option_reuse`) | repeated option string inside any 大問 | FAIL | `20260810_1`, `20260810_2`, `20260811_1`, `20260813_1` |
| `check_moji1_okurigana_exposure` | printed bold span's kana tail vs the four options | FAIL | none — `20260813_2` is repaired, not exempted (§D3.1) |
| `check_legacy_item_repeats` | every drawn item appearing twice inside its own `cooldown_for()` window, **printed by name** | WARN, one line per item | the 7 legacy papers, named item by item (the list IS the check) |
| `check_moji_longest_key_rate` (extend) | adds the 10% floor and the corrected baseline | WARN below 10% | `20260817_2`, `20260817_3`, `20260819_1` (0%) |
| `check_moji4_key_glyph_frequency` | share of 問題4 items whose key is the commonest-kanji option | WARN >45% | `20260812_2` (55%), `20260817_3` (51%) |

Two scope notes so the checks do not over-promise:

- **`check_moji_stem_register`'s classifiers are two regex lists**, printed in the
  docstring. They will mis-bucket edge cases; that is why the register half is WARN and
  the polite half — a closed set of six suffixes — is FAIL.
- **Every new check declares its repair artifact** in the `FINDING_REPAIR` table the
  choukai plan introduces, so §5.0's tier is derived rather than decided, and the
  meta-check that FAILs an undeclared finding covers these slugs too.

---

## Phase 4 — the per-paper rebuild chain

No shared batch; the unit is the paper. For each repaired id, in order:

```
# tier C only, first:
python3 .agents/exam-blueprint/scripts/sample_items.py --reroll-one <cat>:<index> --seed <fresh>
make check-tests             # spec/ledger agreement before a word is authored
# then, every tier:
make lint-draft <id>         # deterministic pre-lint
make booklet <id>            # 言語知識・読解.html
make sheet <id>              # 解答.html — embeds the printed options
# edit 詳細解説.json for every touched item (stem quote, option text, 解説 prose)
make scaffold-translation <id> TLANG=vi TLABEL="Tiếng Việt"   # only the touched entries
make merge-translation <id> TLANG=vi
make model-answer <id>       # 模範解答.html, carrying both languages
make pages                   # once, after the last paper of the run
make check                   # read every line
```

Three costs to write into the step rather than discover:

- **A stem rewrite (tier B) does not move the key, and still costs a translation.** Every
  `詳細解説` entry quotes its stem; all 14 papers ship `vi`. `scaffold_translation.py`
  chunks at 20 items (`--chunk-size`), not per item, so a step that touches three stems
  still pays for a chunk — which is the argument for batching a paper's whole tier into
  one step rather than shipping stems one at a time.
- **A re-draw (tier C) touches `test_spec.json` and `logs/ledger.json`**, and
  `check_draw_provenance` / `check_ledger_spec_agreement` read both. Re-draw *before*
  authoring, never after, or the ledger records an item the paper never asked.
- **`make matrix` is validate-only** (`AGENTS.md` §4): a re-drawn 問題2 target's grid is
  validated by the tool and **constructed by hand**, with the component readings written
  out per `moji-goi.md` §問題2's procedure. That stays true until Phase 7 lands a real
  音訓 table.

---

## Phase 5 — the 14 papers on disk

### 5.0 The tier is DERIVED from the artifact, not decided per session

| Tier | Touches | Also needs | Marginal cost |
|---|---|---|---|
| **A** | an option string, a key cell, a 解説 cell — the drawn target and the key both unchanged | the Phase 4 chain for that id | ~30 min/paper |
| **B** | a **stem**, same drawn target, same key | Phase 4 chain **plus** re-checking every 解説 cell that quotes the stem and every distractor exclusion the stem was carrying | ~2 h/paper |
| **C** | a **new drawn item** (re-draw): a different target, a new option set, possibly a new key position | all of B **plus** `test_spec.json` + `logs/ledger.json` + a queued independent blind solve (`P5Q-*`) + a band check against the books | real authoring, one item at a time |

`tier = {"option/key/解説 cell": "A", "stem": "B", "drawn item": "C"}[artifact]`, declared
once per finding slug beside its check. **Escalation is allowed, de-escalation is not:**
a tier-A repair that turns out to need the stem rewritten is recorded as escalating to B
with the reason; a tier-C finding may never be quietly settled by an option edit — which
is exactly what the `居酒屋`→`潔い` hand substitution was.

Finding → artifact → tier, fixed:

| Finding | Artifact | Tier |
|---|---|---|
| F6 問題3 repeated option | one distractor string | **A** |
| F9 「頻繁に」 option field | four option strings (or a re-draw, if 「に」 makes an option a non-word) | **A**, escalates to C |
| F10 doc numbers | `official_calibration.md`, gate docstrings | not a paper repair |
| F1 / F2 / F4 / F7 stems | stems | **B** |
| F3 和語 quota | drawn `orthography` entries | **C** |
| F5 訓読み floor | drawn `kanji_reading` entries | **C** |
| F8 legacy repeats | drawn entries in 5 categories | **C** |

### 5.4 Per-paper work matrix — what each of the fourteen papers needs

Every cell is measured; Phase 1 regenerates the table. `st` = median 問題1/2/5 stem
(band 15–22), `,–` = comma-free share of those stems (floor 45%), `丁` = polite share of
問題1–5 stems (floor 8%, target 16%), `和` = 問題2 和語 items (floor 1), `熟` = 問題2
bare-compound items (ceiling 3), `訓` = 問題1 訓読み (band 1–2), `問4` = 問題4 median/max
(ceiling 35/45), `官` = institution-actor share (ceiling 16%), `重` = repeated 問題3
option (must be 0), `旧` = live legacy item repeats (must reach 0).

| paper | st | ,– | 丁 | 和 | 熟 | 訓 | 問4 | 官 | 重 | 旧 |
|---|---|---|---|---|---|---|---|---|---|---|
| `20260807_1` | **25** | **0%** | **4%** | 1 | **4** | **4** | 30/34 | **28%** | 0 | **4** |
| `20260810_1` | 21 | 60% | **8%** | **0** | **5** | **3** | **36**/**49** | 12% | **1** | **5** |
| `20260810_2` | **32** | **0%** | **8%** | **0** | **5** | 2 | **43**/**63** | **28%** | **2** | **1** |
| `20260811_1` | **29** | **13%** | **4%** | 2 | 3 | 2 | **66**/**76** | 8% | **1** | **2** |
| `20260812_1` | **27** | **7%** | 16% | 1 | **4** | 2 | 34/45 | 8% | 0 | **3** |
| `20260812_2` | **26** | **13%** | **0%** | 1 | **4** | 1 | 25/31 | **20%** | 0 | **4** |
| `20260813_1` | **29** | **7%** | **8%** | **0** | **4** | 2 | **38**/41 | 16% | **1** | **3** |
| `20260813_2` | **30** | **0%** | **0%** | 2 | 2 | 2 | **37**/**51** | 12% | 0 | 0 + F9 |
| `20260814_1` | **31** | **0%** | **0%** | 1 | **4** | 1 | **37**/43 | **36%** | 0 | 0 |
| `20260817_1` | **29** | **7%** | **0%** | **0** | **5** | 1 | 32/35 | 12% | 0 | 0 |
| `20260817_2` | **24** | 33% | **0%** | **0** | **4** | **3** | **40**/**54** | 12% | 0 | 0 |
| `20260817_3` | **29** | **7%** | **8%** | 2 | 3 | **0** | 33/40 | 4% | 0 | 0 |
| `20260818_1` | **30** | **0%** | 16% | 1 | **4** | 1 | 34/37 | 12% | 0 | 0 |
| `20260819_1` | **29** | **0%** | **0%** | **0** | **4** | 2 | 30/36 | 12% | 0 | 0 |
| **needs work** | **13** | **13** | **12** | **6** | **11** | **4** | **7 / 5** | **4** | **4** | **7** |

Read the bottom row as the plan's size: **no paper is clean**, the cheapest papers
(`20260818_1`, `20260819_1`) still need a stem pass plus one draw, and the two stem
columns are the only ones that touch all fourteen.

Suggested per-paper session shape, one paper per session, in D3's order:

1. tier A pass — repeated 問題3 option, `20260813_2`'s 問題1-5 option field;
2. tier B pass — the stem contract (§2.1) across 問題1/2/5 and 問題4 in one edit, because
   length, clause count, politeness and actor are one rewrite;
3. tier C pass — 和語 / 訓読み / legacy re-draws (14 + 5 + 11 items, §Sequencing), one drawn item at a time, each with its
   spec + ledger update and its queued blind solve;
4. Phase 4 rebuild chain, `make check` read line by line, commit;
5. `exam-qa-review` blind solve of 文字・語彙 if any key moved, plus the two stem-shape
   counts from §2.5.

### What Phase 5 does and does not fix

- **Does:** every literal rule breach on disk (F6, F9); the stem monoculture (F1, F2, F4,
  F7) on all fourteen papers; the 問題2 and 問題1 composition floors (F3, F5) on the seven
  papers that breach them; and the legacy repeat queue (F8) as the re-draws land.
- **Does not:** make a re-drawn key verifiably N2 — that needs Phase 7 — and does not
  touch anything about difficulty *within* band, which is `exam-qa-review`'s to judge and
  no gate's.

---

## Phase 6 — the next paper is the real acceptance test

Run the normal 4-stage pipeline (`jlpt-test-generation`) with these additions to the
文字・語彙 authoring stage's brief:

1. **Stems** — 問題1/2/5 median 17 chars, ≥9 of 15 comma-free, ≥7 of 25 問題1–5 stems in
   です・ます, ≥1 first-person, ≤2 institution-actor stems, 問題4 median ≤28 and no stem
   above 45.
2. **問題2** — 2 和語 targets with printed okurigana, ≤3 bare 2-kanji compounds, every
   compound grid's component readings written out before the item is accepted.
3. **問題1** — 1–2 訓読み of 5, and the printed span's kana tail present in all four
   options.
4. **問題3** — twelve options, twelve different affixes.
5. **Draws** — every 文字・語彙 entry clear of its own `cooldown_for()` window (no legacy
   exemption applies to a new paper), and every key's band recorded with the book and page
   that confirmed it.
6. **The artifact QA reads**: the 文字・語彙 key table gains a **stem-shape line** per
   大問 (chars / commas / politeness) the way the 聴解 構成表 carries 決め手の位置, and it
   is read down as a column before the section is called finished.

Then: `make check` green with **no new grandfather entries**, `make lint-draft`,
`make qa-eval`, `make keyless` and a fresh-eyes `exam-qa-review`. If any quota needs a
grandfather entry for a paper written *after* Phase 2, the quota is wrong — fix the
quota, not the paper.

---

## Phase 7 — the four books (F11), and why it is not optional here

The sibling plans park their book extraction last because 読解 and 聴解 findings are all
measurable from the archive. **文字・語彙's are not**: the archive loses the underline, so
it cannot say what official tested (F10.3), and nothing in `refs/` can say whether a word
is N2 (R.8.3). Phase 7 is what closes both.

1. **`tools/extract_kanji_tables.py`** — Shin Kanzen N2-漢字 別冊1 → `refs/Shinkanzen/kanji_tables.md`:
   学習漢字リスト, 特別な読み方をする漢字の言葉, **訓読みが二つ以上ある漢字**,
   **音読みが二つ以上ある漢字**, plus 「広がる広げる漢字の知識」's 音の変化 pages. Reuse the
   Vision-OCR path in `tools/vision_ocr.swift` that `extract_jlpt_n2_new.py` drives; emit
   the same fenced `[OCR ▼]…[OCR ▲]` blocks with the same "OCR, not quotable as exact
   wording" header. **Note the 264 MB split requirement in the docstring** — the file is
   over the 100 MB PDF read cap and must be chunked first (Soumatome 漢字 173 MB and 語彙
   103 MB likewise; Shin Kanzen 語彙 at 40 MB reads directly).
2. **`tools/extract_shinkanzen_goi.py`** — Shin Kanzen N2-語彙 第2部 (意味がたくさんある言葉 /
   意味が似ている言葉 / 形が似ている言葉 / 副詞 / オノマトペ / 慣用表現 / 語形成) and the
   **模擬試験 第1回・第2回 (pp.186, 188) with 別冊解答** → `refs/Shinkanzen/goi_reference.md`.
   Add the Soumatome counterpart (第5週 やさしい漢字で書きますが…, 第6週 カタカナ/似ている言葉,
   第7週 意味がたくさんある言葉) as a second front-end of the same script.
3. **Make targets** `make extract-kanji-tables` and `make extract-shinkanzen-goi`, listed
   in `AGENTS.md` §4 beside `extract-archive`, owned by §3.
4. **Then the three things that were blocked become possible**, in this order:
   - **re-enable `matrix_helper.py`'s two generators** against a real 音訓 table — they
     were hard-disabled for its absence (qa-report-20260819_1 F4), and this is the one
     change in this plan that removes work from every future paper;
   - **restore a gate for the two-訓読み rule** (deleted 2026-08-11 with `openjlpt`) from
     訓読みが二つ以上ある漢字;
   - **feed the 模擬試験 to Phase 1 as a third front-end**, so 問題1's target-type mix can
     be measured on a typeset paper instead of asserted from five hand-classified
     sittings (D1.3).
5. **Mark everything secondary evidence** — a textbook, not the exam. It corroborates
   band, family and reading; it never sets a count or a length. The archive stays the
   measuring stick for those.

---

## Sequencing, dependencies, and cost

```
D1 ─┬─> Phase 1 (goi_profile.py) ──> Phase 2 (docs + sampler) ─┐
    ├─> re-derive F10's three numbers                          │
    └─> D2 (one-sided rules become bands) ─────────────────────┼─> Phase 3 (gate lines)
                                                               │        ▲
D3 ─┬─> grandfather sets ──────────────────────────────────────┘        │
    ├─> Phase 5 tier A (F6's four options, F9's one item) ──────────────┘
    ├─> Phase 5 tier B (the stem contract, 14 papers)
    └─> Phase 5 tier C (和語 / 訓読み / legacy re-draws)  ──> Phase 6: the next paper
Phase 7 (book extracts) — independent to start, BLOCKS tier C's band checks
                          and blocks re-enabling make matrix's generators
```

| Step | Size | Forces a per-paper rebuild? | Blocks |
|---|---|---|---|
| Phase R (state file + cron) | small, once | no | **everything** — it is what survives interruption |
| D1/D2/D3 | small | no | Phases 2, 3, 5 |
| Phase 1 script | large (400–600 lines) | no | Phases 2, 3 |
| Phase 2 docs + sampler | medium, 5 files | no | Phase 3, Phase 6 |
| Phase 3 gate | medium, ~10 checks | no | Phase 6 |
| Phase 5 tier A | 5 items over 5 papers | **yes, per paper** | — |
| Phase 5 tier B | 14 papers × ~20 stems | yes, per paper | — |
| Phase 5 tier C | **~30 drawn items over 13 papers** (14 for 問題2's composition quota, 5 for the 訓読み band, 11 legacy repeats — some coincide) | yes, per paper | Phase 5's completion |
| Phase 6 | one full paper | its own | — |
| Phase 7 | medium (2 extractors, 4 scans) | no | tier C band checks; `make matrix` |

**Default execution order, if the run is cut short.** Each phase leaves the repo green,
so an agent should prioritise rather than ask which to drop: (1) F6's generalised check
plus its four options and F9's one item — a stated rule stops being violated on disk for
the price of five strings; (2) F10.1, because `moji-goi.md` is currently telling authors
that a 9-character 問題6 option is official and no parse produces that number; (3) Phase 1,
because without it the next quota is built on an unreproducible number, which is how F10
happened; (4) F5's floor and F3's quota **in `sample_items.py`**, because a draw-time
rule stops the defect being authored at all; (5) the stem contract, which is the largest
quality change and the slowest.

**Split by what improves what:** Phases 1–3 and 7 improve the *pipeline* — they make the
next paper better and stop the regressions recurring, but change nothing a learner sees
today. Phase 5 is the only phase that improves the fourteen papers a learner can take
right now, and it covers all fourteen (§5.4). Its tier A is where the ratio of
learner-visible improvement to cost is highest; its tier B is the bulk of the calendar
time, one paper per session, which is what Phase R exists for.

## Risks to watch

- **Phase 1 will move numbers the current papers were built to** — F10's three certainly,
  and possibly the 問題5/6 longest-key band. That is the point, but it means Phase 3's
  grandfather sets must be computed *after* Phase 1, not guessed now.
- **The stem contract fights itself in 問題4.** A stem must fix every exclusion axis
  (`20260818_1` 問題4-14 shipped one unfixed) *and* stay under 35 characters. Author both
  together; a paper that hits the length band by dropping the axis-fixing clause has
  traded a measured defect for an unmeasured one, which is worse.
- **です・ます costs characters.** F2's quota and F1's length band pull in opposite
  directions for the same reason the dokkai plan's voice quota fights its length ceiling.
  A stem does not need to be long to be polite — 「この野菜はビタミンが豊富です。」 is 15
  characters — but it needs a person in it, which is F7's other half.
- **Tier C is a re-draw, and a re-draw is a new item.** Around thirty re-drawn items
  across thirteen papers is thirty new option sets, thirty 解説 cells, thirty `vi` entries
  and one blind solve per touched section. This is the single largest cost in the plan and the one most
  likely to be quietly downgraded to a hand substitution — which is the defect class
  `AGENTS.md` §0 opens with. **A tier-C step that ends without a ledger diff did not
  happen.**
- **Grandfathering fatigue**: ten checks with ten exemption sets makes green weaker, not
  stronger, and here two sets cover all fourteen papers. They are a queue, not an amnesty:
  each set's id-removal condition is written next to it, the state file's `todo` list
  mirrors it, and Phase 5 is not done until every set is empty. If a set is still
  non-empty when the plan is declared finished, the plan was not finished.
- **Band judgment stays unautomatable until Phase 7 lands, and possibly after.** An OCR of
  a scanned index is weaker evidence than a text layer; the extracts will corroborate a
  headword's presence and its readings, not settle every argument (「飢」 was 常用 and still
  N1-band). Ship them as secondary evidence and keep the human review list in the final
  report.
- **Three plans, one set of files.** This plan, `REPORT-CHOUKAI.md`'s and
  `REPORT-DOKKAI.md`'s all rewrite `tests/*/言語知識・読解.md` (two of them), every
  `詳細解説.json` and the same gate file. Run one at a time, honour the lease, and when two
  touch the same paper, do the **draw-time** work first (this plan's tier C), because a
  re-draw invalidates a stem the other plan may just have rewritten.
