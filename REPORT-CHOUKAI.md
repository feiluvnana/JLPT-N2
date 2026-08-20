# 聴解 script audit — 14 generated papers vs. 31 official sittings vs. Shin Kanzen N2 聴解

Date: 2026-08-20. Read-only analysis; nothing on disk was changed.

**Corpora actually opened**

| Corpus | What was read | n |
|---|---|---|
| Generated | `tests/*/聴解スクリプト.txt` + each paper's `聴解.md` (options, keys, 解説, 構成表) | 14 papers, 462 item blocks, 2,061 turns |
| Official | `refs/JLPT_N2_NEW/*/script.md` (the archive extracts) + `answer_keys.json` + one full MP3 (7/2025) | 31 sittings, ~2,000 turns |
| Shin Kanzen | `Shin_Kanzen_Masuta_N2-Choukai.pdf` — 問題紹介 pp.2–11, 実力養成編 III, and the **別冊「解答とスクリプト」, which is bound into the same PDF** (模擬試験 script, pp.35+) | 1 book |
| Shin Kanzen CD | `…-Choukai-AudioCD1/2` — durations, loudness, pause distribution | 163 tracks, 156 min |

**Two corpus facts worth recording before the findings**

1. **The Shin Kanzen CD folder contains no script.** The transcripts are the 別冊 pages inside `Shin_Kanzen_Masuta_N2-Choukai.pdf` (scanned, no text layer, but cleanly legible via the pages-parameter read). This includes a **complete 模擬試験 script** — a second, non-OCR, exactly-typeset N2 listening paper that no skill file currently points at. `choukai-audio` Part 4 says only "Shinkanzen CD tracks are weaker evidence" and nothing about the script existing. That is a documentation gap, not a defect (§F11).
2. **The CD is 163 per-item practice tracks** (median 55 s, no answer pauses, no continuous paper), so it is a register/pacing-of-speech source, not a paper-structure source. Its 模擬試験 tracks *are* usable for pause measurement, and I used them (§F8).

Everything below is measured with one parser per claim, applied identically to both sides. Where my parse disagrees with a number already written in the repo, I say so instead of picking a winner (§F3, §F7).

---

## Summary — the shortcomings, ranked

| # | Finding | Measured | Gated today? |
|---|---|---|---|
| F1 | 問題1 asks one question, 70/70 times | 100% 「この後まず何を…」 vs official 40% carrying まず at all | no |
| F2 | The deciding line moved from "always last" to "always first" | newest 3 papers: 14 of 15 items decide in the first third | no |
| F3 | 問題2's question mix is the inverse of official's | 一番 39% + 理由 39% (official 6% + 22%); 何/どれ 5% (official 33%) | partly (WARN, wrong direction) |
| F4 | The whole paper drifted into keigo service-counter Japanese | 問題4 stimuli 44% keigo vs official 13%; 問題1 counters 39% vs 13% | WARN only |
| F5 | Every service/expert role in `SPEAKER_MAP` is female | 問題3 is 80% female-voiced (official ≈ balanced); the announcer is female too | no |
| F6 | Same-voice pairs under the documented pitch margin | 17 items in 10 papers, incl. **2 Hz** apart in `20260807_1` 問題5-2番 | no (gate threshold is 10 Hz, doc says 20–25 Hz) |
| F7 | 問題3 speaker type and talk length both drifted | 84% institutional speakers vs 42%; newest talks 306–337 chars | length WARN only |
| F8 | The rendered audio's pause distribution is quantised | 60% of sub-2 s pauses sit in two spikes; 1% exceed 1.05 s vs 21–24% in both reference corpora | no |
| F9 | A shared keigo skeleton across papers | 「かしこまりました」 in 12/14 papers (24×) vs 4× in 31 sittings | no |
| F10 | Live breaches still on disk from grandfathered papers | 4 papers with 20/20 問題3 options ending 「〜について」; 3 papers with no ≥3-speaker 問題5; 7 papers with no 構成表 | grandfathered WARN |
| F11 | Shin Kanzen's script corpus is unused and undocumented | see above | — |

`make check` is currently **green (138 warnings, 0 failures)** at the time of the audit; **re-run 2026-08-20 after this report's plan update: green, 139 warnings, 0 failures** (the extra one is `20260819_1`'s missing `詳細解説.vi.json`, §5D). Every finding above except parts of F3/F4/F7/F10 is invisible to it.

---

## F1 — 問題1 asks the same question 70 times out of 70

**Measurement.** Every scored 問題1 item in all 14 papers ends on 「〜は、この後まず何をしますか」 (37, 53%) or 「〜は、この後まず何をしなければなりませんか」 (33, 47%). No other frame occurs, in any paper.

Official, over 129 readable 問い lines in the 問題1 spans of the 31 extracts:

| Official 問題1 question | share |
|---|---|
| contains まず / 最初 at all | **40%** |
| 「何をしますか/しなければなりませんか」 with no まず | 37% |
| 「どう直しますか」「どのように仕上げますか」 (modify / method) | 15 items |
| 「どの番号を押せばいいですか」「どの順番で押さなければなりませんか」「どの席を選びますか」 (condition match) | 6 items |
| 「何を持って行かなければなりませんか」「何を出しますか」 (bring / submit an object) | 5 items |
| 「いつ届くように送らなければなりませんか」「今ここでいくら払いますか」「どこでパソコンを使いますか」 | 4 items |

**Shin Kanzen says the same thing twice.** 問題紹介 p.3: 「質問で『これからまず何をしなければなりませんか』**のように**、最初にすることを聞いている**場合は**、いくつかのすることの中でもどれが優先されるのかを判断しなければなりません」 — the まず frame is presented as *one case*, not the default. And 実力養成編 III splits 課題理解 into **four** sub-skills (目次 pp.33/37/40/43):

1. するべきことを理解する
2. 最初にすることを考える ← the only one our papers ever write
3. 条件に合う情報を聞き取る (p.42's worked item is an automated phone menu: 「希望日の空き状況を知りたいとき、どの番号を押せばいいですか」 → 184 / 10808 / 20804 / 20808)
4. 条件を聞き取って整理する (問題紹介 例題1 keys a **set**: ア案内表示 イマイク ウ机 エいす オごみ箱 → 1 アイウ / 2 アウオ / 3 ウオ / 4 アウ)

**Related, same root.** Official 問題1 has **19 single-speaker items** (an announcement, a 留守番電話 message, a 課長からのメッセージ, an automated menu) out of 138 — 14%. Our papers have **0 of 70**: every 問題1 item is a two-person dialogue.

**Why it matters.** The question form decides what listening operation is tested. One frame for 15 papers means 課題理解 has been reduced to "spot the first-priority action in a two-person dialogue," and three of Shin Kanzen's four named sub-skills are never exercised. It also *causes* F2: if the question is always "what first", enumerate-then-defer is the only way to build the item.

**Fix.** Owner: `jlpt-exam-structure` (question-line inventory) + `question-authoring/references/choukai-items.md` §Section item mix. Add a 問題1 質問型 quota alongside the existing 場面/主導 quotas — e.g. ≤3 of 6 items on the まず frame, ≥1 modify/method (どう直す・どのように), ≥1 condition-match (どの〜), ≥1 non-dialogue item (announcement/message/automated menu). The 構成表's 質問型 column already exists and already reads 「この後まず」 six times per paper: it makes the defect visible and nothing reads it as a column.

---

## F2 — the deciding line inverted from "always last" to "always first"

Rule 6 in `choukai-audio` (added 2026-08-18 after `20260817_2` pivoted every item on 「それより」) says the deciding action must not be the final substantive clause in at least half a section's items. The papers complied — and produced the opposite monoculture.

**Measurement.** For each 問題1/2 item I took the deciding line quoted in that item's own 解説 cell, located it in the script block, and normalised its position (0 = first turn, 1 = last):

| paper | 問題1 decider positions |
|---|---|
| `20260813_2` (pre-rule) | 0.90, 0.50, 0.91, 0.50, 0.82 |
| `20260817_2` | 0.20, 0.00, 0.20, 0.40, 0.00 |
| `20260817_3` | 0.18, 0.17, 0.33, 0.28, 0.06 |
| `20260818_1` | 0.17, 0.14, 0.17, 0.31, 0.36 |
| `20260819_1` | 0.17, 0.33, 0.17, 0.23, 0.23 |

The newest three papers put the decider in the **first third of 14 of their 15 items** (the fifteenth at 0.36). `20260819_1`'s own 構成表 states it plainly — 決め手の位置 reads 冒頭・冒頭・冒頭・冒頭・中盤・中盤 — and reports it as compliance.

`20260812_2` 問題2 is the same failure with a different constant: all six items decide at position **0.64**.

**The item shape underneath it.** Counting proposal turns (turns ending 〜ましょうか/〜ますか/〜は。) per 問題1 item: official median **0**, one item in 154 with ≥3. Ours: median 1, and 11 of 70 items with ≥3 — concentrated in exactly the newest papers (`20260818_1`: 3,3,3,3,2; `20260819_1`: 3,4,2,1,1). The template is: driver assigns task → receiver proposes three alternatives → each is killed with a different closed-vocabulary device → receiver announces the original task. `20260819_1` 問題1 runs it in 6 of 6 items, with a perfectly balanced 消去方法 tally (nine tokens × exactly 2 rows) documenting it.

Also: the receiver announces the action in the final turn in **23% of our 問題1/2 items vs 9.5% official** (final turn contains 〜てきます/〜ときます/〜ますね and is >10 chars).

**Why it matters.** "Mark the first thing the other speaker is asked to do" scores this section without Japanese, exactly as "take whatever follows それより" did. The rule that fixed the last-position bias is satisfied to the letter by an equally readable first-position bias.

**Fix.** Owner: `choukai-audio` §Register rule 6 → make it two-sided (a distribution over positions, not a floor), and make the 構成表's 決め手の位置 column a *counted* column: no more than half a 大問's rows may share a position bucket. Cap the proposal-carousel shape at ≤2 items per 大問 (official: 1 in 154).

---

## F3 — 問題2's question mix is the inverse of official's

One parse, applied to official 問い lines and to our repeated question lines, priority 理由 → 一番/優先 → どのように → 何/どれ:

| | official (n=181) | generated (n=84) |
|---|---|---|
| 何・どれ・どんな (content of what was said) | **33%** | 5% |
| その他 (何をしたいと言っていますか etc.) | 38% | 0% |
| 理由 | 22% | **39%** |
| 一番・優先 | 6% | **39%** |
| どのように | 1% | 17% |

`20260810_1` keys five of its six 問題2 items with 一番; `20260812_1` keys five with 理由. Official's dominant frame is the reported-statement question — 「〜は何をしてはいけないと言っていますか」「〜は卒業したら何をしたいと言っていますか」「係の人はどんな人にボランティアに来てほしいと言っていますか」 — and 「〜と言っていますか」 appears in **45% of official 問題2 questions vs 30% of ours**. Shin Kanzen 問題紹介 p.4 names the target as 「出来事の理由や目的、**話し手の気持ち**など」; emotion-framed questions (どうして怒って/残念がって/心配して) are 5% of official and 2% of ours.

**A measurement conflict to settle, not to route around.** `choukai-items.md` §Section item mix cites official as 6% 一番 / **37% 理由** / **18% どのように** and therefore *requires* ≥2 理由 and ≥1 どのように per paper. Under my parse the same corpus reads 6% / 22% / 1%. The 理由 gap is explicable (my regex counts 理由・どうして・なぜ; theirs may bucket differently), but **どのように at 18% vs 1% cannot both be right**, and the quota built on 18% is pushing papers to 17% — sixteen times my measured official rate. Per `AGENTS.md` §0, that disagreement is the defect. Whoever re-measures should write the parse rule next to the number, as `official_register.md` §6 does.

**Fix.** Owner: `choukai-items.md` §Section item mix. Re-derive the 問題2 quota from one stated parse, and add the missing bucket: **≥2 of 6 items must be a content/reported-statement question** (何・どんな・と言っていますか). Today the quota table names only the three rare types, so a compliant paper is guaranteed to look nothing like official.

---

## F4 — the paper drifted into keigo service-counter Japanese

即時応答 is officially a casual-speech section. Ours is a workplace/counter section.

| | official | generated |
|---|---|---|
| 問題4 stimuli carrying keigo markers (ございます/いただ/ておりま/申し訳/伺) | 13% (42/320) | **44%** (67/154) |
| 問題4 stimuli clearly casual (だよ/だね/よね/んだ/かな/でしょ) | **49%** | 27% |
| 問題1 items at a service counter (lead-in keyword set) | 13% (20/154) | **39%** (27/70) |

Official 問題4 stimuli, for contrast: 「この間のキャンプ、一緒に来たらよかったのに。」「来るの遅いよ。もう時間ぎりぎりだよ。」「今日はどこもすごい人ごみだね。」 Ours, from `20260819_1`: 「診察券をお持ちでない方は、初めての方窓口へ。あちらでご記入をお願いします。」「明日の会議のことで、急なお願いで申し訳ありませんが、代わりに出席していただけませんか。」「お客様、保険証の有効期限が切れております。」 — four consecutive items (1–4) spoken by 係員 / 担当者 / 店員 / 職員.

The first of those is also close to the line `choukai-items.md` §即時応答 draws: 「〜方は、…窓口へ」 is addressed to a class of people, not to the person in front of the speaker, which is the shape the rule bans as having "no addressee to answer as."

**Why it matters.** 即時応答 tests 縮約形, intonation and 間接的な答え方 (Shin Kanzen II-2). A keigo counter prompt suppresses all three — you cannot contract 「ご記入をお願いします」 — and it interacts with F5: the service roles are the female-voiced labels.

**Fix.** Owner: `choukai-items.md` §即時応答. Add a stimulus-register quota mirroring the archive: ≥5 of 12 clearly casual, ≤2 keigo counter prompts. This is countable with the regexes above, so it can be a gate line rather than a judgment call.

---

## F5 — every service and expert role in `SPEAKER_MAP` is female

`SPEAKER_MAP` (`.agents/choukai-audio/scripts/make_choukai_mp3.py:76`) holds 23 labels: **9 male, 14 female**. Every institutional role is in the female half — 店員, 先生, 医者, 専門家, レポーター, 教室の人, 職員, 係員, 担当者, 講師, アナウンス, アナウンサー. The male half is 男/男1/男2/夫/学生/部長/店長/教授/FP.

Consequence, measured on resolved voices:

| 大問 | female share of turns (pooled, 14 papers) |
|---|---|
| 問題1 | 52% |
| 問題2 | 52% |
| 問題3 | **80%** |
| 問題4 | **65%** |
| 問題5 | 50% |

By item: **56 of 70 問題3 items are female-only, 14 male-only, 0 mixed.** Official 問題3, by speaker tag: 34 male-only, 40 female-only, 40 mixed/role, 35 untagged — no lean. And the narrator/announcer is also `NanamiNeural`, so most of our 概要理解 section is the announcer's voice at a pitch offset.

問題4 prompts: 7 of 11 items are role-labelled in `20260810_1`, `20260810_2` and `20260813_2`; 8 of 11 prompts resolve to the female voice in six papers.

**Fix.** Owner: `choukai-audio` Part 2. Either add male mappings for the service/expert roles (`職員2`, `係員2`, `担当者2`, `講師2`, `専門家2` with MALE voices) or — better, since a remap breaks every existing paper's audio — state the rule that role labels come in gendered pairs and the author picks per item, then add a gate line: no 大問 may exceed ~70% of turns on one voice.

---

## F6 — same-voice pairs below the documented pitch margin, and three numbers with no owner

`choukai-audio` Part 2 states the margin: same-gender labels are separated by pitch, "~25 Hz on a ~210 Hz female, ≤20 Hz on a ~120 Hz male", and names the failing case verbatim: 「職員(−14 Hz) beside 女(+0 Hz) is only 14 Hz, under margin」.

Papers on disk that ship pairs under that margin — 17 items across 10 papers:

| paper | item | pair | voice | gap |
|---|---|---|---|---|
| `20260807_1` | 問題5-2番 | 係員 / 妻 | F | **2 Hz** |
| `20260811_1` | 問題1-3番, 問題2-2番, 問題2-5番 | 女 / 職員 | F | 14 Hz (two-party items — both speakers one voice) |
| `20260811_1` | 問題1-5番 | 係員 / 女 | F | 18 Hz (two-party) |
| `20260812_2` | 問題1-5番, 問題5-1番 | 女 / 職員 | F | 14 Hz (two-party) |
| `20260812_2` | 問題1-3番, 問題2-6番 | 女 / 担当者 | F | 20 Hz (two-party) |
| `20260812_2` | 問題2-4番 | 係員 / 女 | F | 18 Hz (two-party) |
| `20260817_2` | 問題1-3番 | 男 / 部長 | M | 18 Hz (two-party) |
| `20260810_1`, `20260810_2`, `20260812_1`, `20260814_1`, `20260817_1`, `20260819_1` | 問題5-2番 | 係員/女, 女/担当者, 女/職員 | F | 14–20 Hz |

Nine of these are **two-party items where both speakers share one voice** — the case `choukai-audio` Part 2 calls "a defect", because in 問題1/2/5 *who* said the deciding line is the whole task.

**Three numbers disagree, and each one is written down somewhere:**

- `choukai-audio` Part 2: 25 Hz (female) / 20 Hz (male), with 14 Hz named as too tight.
- `tools/check_consistency.py:7050`: flags only `abs(p1-p2) < 10` Hz, and only when the item has exactly two labels — so the 2 Hz pair in `20260807_1` 問題5-2番 (a three-label item) can never be seen, and the 14 Hz pairs pass.
- `qa/qa-report-20260811_1.md` §6: adjudicated the 14–18 Hz pairs **GATE-WRONG false positive**, reasoning from "identity comes from pitch" — the half of the doc that has no number. That same report's §7 records that the MP3 was never listened to.

`make check` today prints `20260819_1: 聴解 item speaker pairs cast distinguishable voices — ok` for a paper whose 問題5-2番 casts 女(+0 Hz) against 職員(−14 Hz), and whose 構成表 documents the 14 Hz split as deliberate compliance.

**Fix.** Settle the margin once, and in the right unit — the table above measures against the doc's Hz numbers, and Hz is part of the problem: 18 Hz on a ~120 Hz male voice is 2.42 semitones and plainly audible, while 20 Hz on a ~210 Hz female voice is 1.57 and marginal, so the Hz rule flags the wrong rows. Re-state it in semitones (plan §D2, which clears `20260817_2` outright and leaves exactly one FAIL-class defect — `20260807_1` at 0.16 st), make the doc, the gate threshold and the QA precedent carry that one number, and extend the check to same-gender pairs inside 3-label items.

---

## F7 — 問題3 drifted in speaker type, and the newest papers overshot on length

**Speaker type.** Classifying 問題3 lead-ins as an institutional/expert speaker vs. an ordinary person: official **42% / 33%**, ours **84% / 11%**. Official's most common lead-ins are 「ラジオで女の人が話しています」(11), 「テレビでアナウンサーが話しています」(8), 「ラジオで男の人が話しています」(6); ours are 担当者 / 職員 / 係員 / 講師 / 専門家 explaining a service — 「市の防災講座で、担当者が話しています」「市の広報で、担当者が話しています」「地域のニュースで、町の担当者が話しています」. The quota (≤2 institutional, ≥3 a person's 主張・意図・経験) exists and is a WARN; `20260819_1` satisfies it by counting 「ラジオで、店長が」 and 「家電の売り場で、男の人が新人に」 as person-items, which is fair — but the pooled 84% shows the section-level habit is intact.

**Length overshoot.** Under my parser (item block minus lead-in, options and question line), official per-paper median talk length runs **133–281 chars**; our papers run 142–196 for the older half and **307, 318, 327, 333** for `20260817_2`, `20260817_3`, `20260818_1`, `20260819_1`. `20260819_1`'s own 構成表 reports 306–337 and cites the target as "公式の中央値305・p10 251" from `official_register.md` §7.4.

Both numbers cannot be the official median. §7.4's own note says an earlier "median 257" came from a different parse and was replaced by 305; my parse gives 226 with a maximum per-paper median of 281. The papers are being written to a target no parse I can run reproduces, and the gate FAILs only below 175, so the overshoot is unobservable. **This needs the same treatment as F3: one parse, stated next to the number.** Whichever wins, a talk that is 30–50% longer than the archive's longest costs runtime the section does not need (the newest papers' MP3s run 46–47 min against official's 36.6–52.1).

---

## F8 — the rendered audio's pause distribution is quantised

`official_pacing.md` measures pause *medians* and every constant sits inside its band. The *distribution* was never measured. One method (`silencedetect=noise=-35dB:d=0.30`, all silences under 2 s), three corpora:

| | median | p75 | p90 | max | share in the 0.5 s + 0.9 s spikes | share > 1.05 s |
|---|---|---|---|---|---|---|
| ours (`20260819_1` 聴解.mp3) | 0.51 s | 0.92 s | 0.93 s | 1.55 s | **60%** | **1%** |
| Shin Kanzen CD2, 17 tracks | 0.66 s | 1.04 s | 1.22 s | 1.73 s | 19% | 24% |
| official 7/2025 full MP3 | 0.69 s | 1.00 s | 1.41 s | 2.00 s | 20% | 21% |

Our sub-2 s pauses take essentially two values: `GAP_BETWEEN_LINES` = 0.9 s at every turn boundary, and ≤`GAP_WITHIN_TURN_MAX` = 0.5 s everywhere inside a turn, because `shape_pauses()` caps every internal pause and every turn gap is a constant. **The class of pause that is one in five in both reference corpora — the 1.1–1.4 s beat where a speaker thinks — does not exist in our audio at all.** Loudness is correct (−15.4 LUFS measured; Shin Kanzen runs −13.8 to −15.2, official −15.0 median).

For completeness, the Shin Kanzen mock's answer pause measures ~9.8 s where official 問題1 measures 12.2 s and we use 12 s — the textbook is tighter than the exam, so it is not a calibration target, only corroboration that our value is the exam's.

**Fix.** Owner: `choukai-audio` Part 3. Two options, both cheap: (a) allow a small deterministic jitter on `GAP_BETWEEN_LINES` (e.g. ±0.25 s keyed off a hash of the line, so builds stay reproducible), and (b) raise `GAP_WITHIN_TURN_MAX`'s cap for turns that end a thought, so a long beat can survive. Either way the claim to verify afterwards is the *distribution*, not the median — measured on the rendered MP3, per Part 3's own rule.

---

## F9 — a shared keigo skeleton across papers

Cross-paper reuse of dialogue 8-grams is only slightly above official (generated median 4.4% of a paper's 8-grams also occur in another paper; official 3.1%). What differs is *which* strings are shared. Official's most widely reused strings are human courtesy: ありがとうございます (28 sittings), はい、わかりました (17), よろしくお願いします (15). Ours are transaction formulas:

| phrase | our papers | official |
|---|---|---|
| かしこまりました | **12/14 papers, 24×** | 4× in 31 sittings |
| 〜ていただけますか | 12/14, 25× | 6× in 31 sittings |
| よろしいでしょうか | 10/14, 13× | 6× in 31 sittings |
| あ、そうなんですね | 8/14, 17× | 0.2/10k chars (21× our rate inverted) |
| 〜た方がいいですか | 8/14, 13× | **0 in 31 sittings** |
| 〜ておきましょうか | — | 12× our rate inverted |
| そうですね | 0.9/10k | 4.8/10k (we under-use it 5×) |

「〜た方がいいですか」 is on `choukai-audio`'s banned-formula list ("as every probe"). At 1–3 per paper it does not breach the letter of that ban, but it is a phrase the archive never uses and eight of our papers do, including both of the newest.

Turn shape is drifting too: our median turn is **27 chars over 2,061 turns against official's 38** while our turn *count* per paper is higher (107–198 vs 66–143). `official_register.md` §1 says turn length "is already right — median 36 vs 32"; under my parse (OCR wrap-lines rejoined on the official side) the gap is now 11 chars. The audible effect is ping-pong: more, shorter turns, each separated by the same 0.9 s (F8).

---

## F10 — breaches still on disk behind grandfather clauses

These are known and exempted by name, but they are what a learner actually gets today:

- **20/20 問題3 spoken options end in 「〜について」** in `20260811_1`, `20260812_1`, `20260812_2`, `20260813_1`. Official: 8 of 685 (1%). The gate FAILs above 2/paper for any non-grandfathered id.
- **No 問題5 item has ≥3 speakers** in `20260811_1`, `20260812_2`, `20260813_1` (max 2). `choukai-items.md` §統合理解 requires it of 1番; official has one every sitting since 2020.
- **No セクション構成表** in the 7 papers before `20260813_2` — the artifact QA reads first.
- **問題3 talks below the archive minimum**: `20260807_1` (168–170 chars), `20260810_1` (132–166).
- **`20260812_1` carries 50 filler tokens**, over the 48 archive ceiling.
- **`20260810_2` has an already-done distractor in 8 of 11 問題4 items** (archive median 1, max 3).
- One item-level observation on the newest paper that no check covers: `20260819_1` 問題2 例 (パン屋, move a 50-portion order to another day) and 1番 (レストラン, change a booking for an egg allergy) are two different establishment types — so `check_choukai_setting_adjacency()` passes — but the same **errand**: "modify a food order/booking by phone or counter", back to back at the head of the section. The 場面 rule is written on establishment type; the thing a listener notices is the errand.

---

## What is healthy — measured, not assumed

So the report is a fair audit rather than a list of complaints:

- **Answer positions are clean.** Our 4-option 聴解 items key 25/25/28/21% across 1–4 (n=191); official 20/28/31/21% (n=603). 問題4's 3-option items are likewise flat.
- **Key length no longer carries the answer.** `20260818_1` 14% uniquely-longest, `20260819_1` 25%, against official 28% and the 35% ceiling; key/distractor-mean ratio 1.00–1.04 against official 1.00. This was 39–79% before the rule.
- **縮約形 recovered.** The newest four papers measure 39.9 / 62.5 / 48.4 / 46.2 per 10k spoken chars against the archive's 22.4–67.4 band; the older half sits at 9.9–14.6. The rule worked.
- **問題3's denial sweep and topical lead-ins are gone** from every paper written after the rule, and the newest papers' monologues are real 主張 talks (`20260819_1` 1番, the restaurant that cut 50 seats to 30, is a good item).
- **The 例 mechanics, the 問題5 enumeration order rule, `script_sha`/`pacing_sha` stamping and the 消去方法 closed vocabulary all hold** on the papers that carry them, and `20260819_1`'s 構成表 is genuinely auditable — it is what let me measure F2 in an hour instead of a day.
- **Loudness and the answer-pause structure of the rendered audio match the archive** (−15.4 LUFS; 12 s/8 s/10 s/20 s pauses present and in the right places).

The pattern across F1–F3 and F7 is the one `official_register.md` §7 already named: a counted tell gets fixed and an uncounted one grows in its place. Every finding here is a *distribution* the rules specify one-sidedly — a floor with no ceiling, a target with no shape, a median with no spread.

---

## Recommended order of work

1. **Settle the two measurement conflicts before authoring anything** (F3's どのように rate, F7's 問題3 length target). A quota built on an unreproducible number moves papers away from official.
2. **Settle the pitch margin** (F6) — one listening session, three files to update, and it unblocks a real audio defect (2 Hz).
3. **Add the 問題1 質問型 quota** (F1) — highest impact per line of doc, since it also breaks F2's template. Include one non-dialogue item per paper.
4. **Make the position/shape columns counted, not decorative** (F2): 決め手の位置 and the proposal count belong in the same "read it as a column" discipline as 消去方法.
5. **Register quotas for 問題4 stimuli and 問題3 speakers** (F4, F7), both regex-countable.
6. **Gender-pair the role labels** (F5) and add a per-大問 voice-balance line.
7. **Jitter the turn gap** (F8), then verify the distribution on a rendered MP3.
8. **Point the skills at Shin Kanzen's 別冊 script** (F11) — a clean second reference paper, with the 音の変化・縮約形 chapter next to it.

**Then remake the papers against the strengthened rules.** Steps 1–8 fix the pipeline
and change nothing a learner would notice in the 14 papers on disk. The remediation
plan's Phase 5 is the other half and, per the 2026-08-20 decision, it is not scoped
down: 3 papers get targeted item rewrites (C1), 8 get their 聴解 section regenerated
wholesale (C2), 3 are grandfathered by id. Rules first is not optional — regenerating
a section against today's one-sided quotas rebuilds the same defect.

## Method, and what I did not do

- **Parsers.** Official: `script.md` split on `### 問題 N`, item lines `^\d+\s*番`, turns from `^(男|女|…)[：:]` with wrapped OCR lines rejoined into the preceding turn, `問い` lines and `（正解：N）` read separately. Generated: blocks split on blank lines, section on `^問題N。$`, turns on `^label[：:]`, spoken options on `^[1-4]、`. Decider position: last 「…」 quote in the item's 解説 cell, matched into the block by its first 12 chars. Pauses: `silencedetect=noise=-35dB:d=0.30`, silences <2 s only. Loudness: `loudnorm …print_format=summary` (never `volumedetect`).
- **OCR caveat.** Official dialogue in `refs/JLPT_N2_NEW/*/script.md` is ~98% accurate OCR. Every official quote above is an illustration of a pattern, not quotable official wording (`question-authoring/references/reading-reference-pdfs.md`). Counts are sound; individual characters are not.
- **Not done, and it matters for F5/F6/F8:** I did not listen to any MP3. The voice findings are from `SPEAKER_MAP` values and from silence/loudness measurement; the margin question in F6 is exactly the kind that only an ear settles.
- **Not done:** official 問題1/2 printed options are only exposed to a parser in a few `booklet.md` extracts, so the key-length and paraphrase claims here reuse the repo's existing measurements rather than re-deriving them.
- **Not done:** I did not re-run any authoring or repair. `make check` was run once (green, 138 warnings) purely to state what the gate currently does and does not see.

---

# Remediation plan

Ordered so that nothing is authored against a number that later moves, and so the
expensive step (rebuilding audio) happens exactly once. Each item names the **owner
file** the rule belongs to, the **gate line** that makes it observable, and the
**acceptance test** that says it is done. Where a change forces a rebuild or a
grandfather clause, that cost is written into the step rather than discovered later.

### Decision log

| Date | Decision | Where it lands |
|---|---|---|
| 2026-08-20 | **The plan strengthens the rules AND remakes the papers.** Phases 1–4 and 7 fix the pipeline; Phase 5 fixes what is on disk. Neither half is optional, and Phase 5 is no longer scoped down to whatever survives the rebuild window. | §D3, §Phase 5 |
| 2026-08-20 | **Section-level repair uses wholesale 聴解 regeneration for the papers that fail on 3+ axes**, not item-by-item retrofit. Patching a paper to the edge of each quota costs more than authoring one compliant by construction, and it cannot produce a section that reads unlike a template. | §5C (C1/C2) |
| 2026-08-20 | **Pool depth verified before committing to C2** — `--check-depth` run against the live pools, cooldown windows computed. C2 at 8 papers is feasible with no cooldown relaxation (§5C.3). | §5C.3 |

Conventions this plan follows, from `AGENTS.md` §4 and `choukai-items.md`
§"Target vs gate":

- A rule has **one owner file**; every other file points at it.
- The **authoring target is tighter than the gate**. The gate FAILs only outside
  the archive's whole range; the target is the archive's median.
- A new gate line that existing papers breach ships with a **named grandfather
  set**, and the set is named **in the owner doc too** — a doc that says "fails"
  beside a gate that warns is the shape where green stops being evidence.
- Any change to a `GAP_`/`PAUSE_`/`SHAPE_` constant or to `pause_after` /
  `gap_before_line` / `shape_pauses` moves `pacing_sha`, which makes **every**
  paper's `聴解.mp3` stale and `make check` red until it is rebuilt — and because
  `解答.html` embeds `聴解_チャプター.json` verbatim, each rebuild also needs
  `make sheet`.

### Autonomy contract — the agent runs this without asking

This plan is written to be executed end to end by an agent, deciding for itself. So
every "decision" below is a **decision rule with a bright line**, not a question to
escalate: D2 is settled by measurement rather than by taste, D3 is a policy with
thresholds, and §5.0's tier is derived from the artifact a repair touches. An agent
that reaches a fork not covered by a rule should extend the rule in the owner file
and say so in its final report — not stop.

**Decides for itself, and never asks:** which findings exist and at what tier; which
papers get tier A/B/C work (D3's rule); the margin number (D2's measurement); what to
write in every repaired line and every backfilled 構成表 cell; when to batch the
rebuild; which ids enter or leave a grandfather set (subject to the repo's standing
rule that an id leaves only when the paper is actually repaired); and **committing
each completed step** (Phase R.6 — the commit is what makes the work resumable, so it
is part of the mechanism, not a courtesy).

**Three things are simply out of scope**, so they are not questions either:

- **Pushing to a remote.** Every step's value lands locally, in `make check` and in
  the papers. Publishing is a separate instruction, not a step of this plan.
- **Deleting or rewriting anything in `refs/`.** The archive is the measuring stick;
  a plan that edits its own baseline cannot detect its own regressions.
- **Removing a check.** This plan only adds them. If a check proves wrong, the repair
  is to fix its threshold or its declaration and record why — `make check`'s own
  history is the audit trail, and a deleted line leaves none.

**One sequencing rule that replaces what would otherwise be an escalation:** a repair
that moves a shipped paper's KEY (re-keying an item, changing which option is correct)
must be followed in the same step by a fresh `exam-qa-review` blind solve of that
section. A re-key with no blind solve behind it is a defect class this repo has
shipped more than once. That is a step the runner performs, not a decision it defers.

**Reports, per `AGENTS.md` §0.7:** skills read, phases run, papers touched, tier-C
declines with their reason, every grandfather id added or removed, and the `make
check` output read line by line — written to `qa/choukai-remediation-report.md`
(Phase R.7), since there may be no human in the session to read a chat message.

---

## Phase R — running this unattended: checkpoint, interruption, restart

This plan is long enough that no single session finishes it. It must therefore be
**resumable by construction**, and that is a design property of the state file and the
step granularity — not something a runner can achieve by watching a fuel gauge.

### R.1 There is no quota gauge to read — so do not gate on one

Stated plainly, because a plan that assumes otherwise will stall: **no tool available
to an agent in this repo returns remaining usage.** Usage limits surface as a
harness-level message that *interrupts* the turn; they are not queryable in advance,
they are not in the filesystem, and `make check` knows nothing about them. (`/usage`
is a slash command a person types, not a tool call.)

Three consequences, and they shape everything below:

1. **Assume interruption at an arbitrary instruction**, not at a step boundary. Any
   design that needs a graceful shutdown hook is wrong.
2. **Make every step small and idempotent**, so an interrupted run loses at most one
   step's work and re-running it is a no-op.
3. **Detect the mess on wake, do not prevent it.** Every run starts by reconciling
   the repo (R.4), which is also exactly what a fresh context can do without trusting
   anything the previous run claimed.

### R.2 The state file

`logs/choukai_remediation_state.json` — tracked, because it is history the next run
depends on, the same argument `AGENTS.md` §2 makes for `logs/ledger.json`:

```json
{
  "plan_source": "REPORT.md#remediation-plan",
  "plan_sha": "b3f1c0a99e21",
  "created": "2026-08-20",
  "max_steps_per_run": 6,
  "steps": [
    {"id": "P1-profile",        "deps": [],              "status": "todo",
     "artifact": "tools/choukai_profile.py", "tier": null, "test_id": null},
    {"id": "P5A-20260810_1",    "deps": ["P1-profile"],  "status": "todo",
     "artifact": "聴解.md", "tier": "A", "test_id": "20260810_1"},
    {"id": "P5B-20260807_1-cast","deps": ["D2"],         "status": "todo",
     "artifact": "聴解スクリプト.txt", "tier": "B", "test_id": "20260807_1",
     "needs_rebuild": true},
    {"id": "P4-rebuild-batch",  "deps": ["P4.2-jitter", "…all tier B…"],
     "status": "todo", "artifact": "聴解.mp3", "test_id": "*"}
  ],
  "runs": [{"at": "…", "steps_done": ["P1-profile"], "ended": "completed|interrupted"}]
}
```

- **`plan_sha`** is sha1 of this plan section. If it changes, the runner does not
  silently re-plan: it appends the new steps, marks superseded ones `stale`, and says
  so in its report. Same reflex as `script_sha` — mechanical evidence that the work
  order on disk matches the plan on disk.
- **`status`** ∈ `todo | doing | done | blocked | declined | stale`. `declined` is
  D3's rule saying no, with the reason stored — that is how a grandfathered paper
  stops being re-considered every run.
- **`max_steps_per_run`** is the runaway guard. A run does that many steps and stops
  even if it has room; the next firing continues. Six is a starting value — two tier-B
  script edits, or one C2 paper's 大問, is a comfortable unit.

### R.3 Step granularity: one paper, one tier, one artifact

Never larger. Specifically:

| Step shape | Example id | Ends with |
|---|---|---|
| one tool/doc change | `P1-profile`, `P2.2-quotas` | `make check` green |
| one paper's tier A | `P5A-20260817_2-shoukyo` | `make booklet` + `make sheet` for that id, `make check` green |
| one paper's tier B edits | `P5B-20260817_1-cast` | script edited; **rebuild deferred to the batch step** |
| one C1 item rewrite | `P5C1-20260819_1-mondai1` | script + `聴解.md` edited; rebuild deferred |
| one C2 paper, one 大問 | `P5C2-20260810_1-mondai2` | script + `聴解.md` edited; rebuild deferred. **The `--reroll` is its own earlier step** (`P5C2-20260810_1-reroll`) so a re-drawn spec is committed before anything is authored against it |
| one paper's §5D tail | `P5D-20260810_1` | QA passed, `詳細解説.json` + `.vi.json` authored, `make model-answer` — in that order |
| a rebuild batch | `P4-rebuild-batch`, `P5-rebuild-batch` | `make mp3` + `make sheet` ×N, `make pages`, `make check` green |

Deferring every rebuild to one batch step is what makes tier B free (§5B) **and** what
makes interruption cheap: a script edit costs seconds to redo, a 47-minute MP3 does not.
The cost is that between the first tier-B edit and the batch step, those papers'
`script_sha` are stale and `make check` is **red on those lines**. That is intended and
must be recorded in the state file (`"gate_expected": "red: script_sha on <ids>"`), or
the next run will read red as damage and start repairing the wrong thing.

### R.4 Every run starts by reconciling, not by trusting

The first thing a fresh context does — before reading which step is next:

1. `git status` — an interrupted run may have left edits. Uncommitted edits belonging
   to a `doing` step are that step's work in progress: finish it, do not revert it.
2. **`make check`, read every line.** Compare the failures against
   `state.gate_expected`. Anything red that is *not* expected is the interrupted
   step's damage and is repaired before new work begins.
3. **Stale `doing`**: a step marked `doing` with a timestamp older than the restart
   interval was interrupted mid-flight. Re-derive its actual state by *measuring*
   (does the paper have a 構成表? does the script still contain the split turn?), never
   by trusting the flag. This is the same rule the 消去方法 incident taught: evidence
   is re-read, not carried forward.
4. **Twice-failed steps become `blocked`** with the error text, and the run moves on.
   No step is retried a third time without the plan being amended — that is how a
   loop turns into a runaway.

### R.5 Restart: schedule it, do not rely on the session surviving

Two mechanisms, both available in this harness. Use the first for unattended work.

**A. A cron routine (primary).** Arm it once, at the start of execution, with the
`schedule` skill (`CronCreate`). Fire every 4–6 hours — long enough that a
rolling-window usage limit has reset by the next firing, short enough that a stalled
plan is noticed the same day. The prompt is fixed and stateless, because all state is
on disk:

```
Resume the 聴解 remediation.
1. Read AGENTS.md §0 in full, then logs/choukai_remediation_state.json.
2. Run Phase R.4's reconcile (git status; make check; repair unexpected red).
3. Do up to max_steps_per_run unblocked steps, in dependency order.
4. Update the state file after EACH step, and commit that step.
5. Stop. Report steps done, steps blocked, and the gate's state.
Plan: REPORT.md, "Remediation plan". Do not re-plan; append if plan_sha changed.
```

Because the prompt carries no step numbers, an interrupted run and a scheduled run are
the same operation. The routine deletes itself (`CronDelete`) when the state file has
no `todo`/`doing` left — that is the plan's terminating condition, checked by the
runner rather than by a person.

**B. Self-paced `/loop` (when a session is already open).** `/loop` with no interval
lets the agent call `ScheduleWakeup` after each step and choose its own delay: a long
one (1200 s+) while waiting on nothing in particular, short only when it is genuinely
polling something. Use this to work a burst interactively; fall back to A for
overnight progress. Do not run both at once — two runners racing the same state file
is the one failure mode this design does not survive, so the state file carries a
`"runner"` lease field with a timestamp, and a runner that finds a fresh foreign lease
exits immediately.

**What happens when the quota does run out mid-step:** the turn dies with the state
file saying `doing` and the working tree holding a partial edit. Nothing needs to be
done at that moment. The next firing's R.4 reconcile finds the stale `doing`, measures
what actually landed, finishes or restarts that one step, and continues. That is the
whole quota story — not prediction, recovery.

### R.6 Commits are part of the mechanism, not a courtesy

One commit per completed step, message naming the step id
(`choukai(P5C2-20260810_1-mondai2): re-author 問題2 against the new 質問型 quota`). Three reasons this is load-bearing
rather than housekeeping: it makes `git status` a truthful signal for R.4's reconcile;
it bounds what an interrupted step can lose to one step; and it lets a bad step be
reverted precisely instead of by hand-unpicking a mixed working tree. Batch the LFS-heavy
rebuild into its own commit (`choukai(P4-rebuild-batch): …`), since it is ~460 MB of
objects and wants to be revertible on its own.

**Pushing is out of scope for the plan** — every step's value is realised locally, in
`make check` and in the papers, so nothing here needs a remote. If the work should be
published, that is a separate instruction.

### R.7 Termination and the final report

The plan is done when: the state file has no `todo` or `doing`, `make check` is green
with `gate_expected` empty, **both** rebuild batches have run, **every C1/C2 paper has
completed its §5D tail (QA passed, `詳細解説.json` + `詳細解説.vi.json` authored,
`模範解答.html` rebuilt last), the 構成表 grandfather set added in Phase 3 is empty**,
and one new paper (Phase 6) has passed `exam-qa-review` without a new grandfather
entry. The runner then writes
`qa/choukai-remediation-report.md` — phases run, papers touched, every `declined` step
with its D3 clause, every grandfather id added or removed, and the residual WARNs it
judged false positives — and deletes its cron routine. `AGENTS.md` §0.7 asks for that
report from whoever does the work; here, whoever does the work is the runner.

---

## Phase 0 — three decisions the plan makes by rule

Nothing in Phases 2–5 can be authored correctly until these are settled. Each is
resolved by a stated rule rather than by preference — the consequence of guessing is
that a quota gets built on the wrong number again (F3, F7).

### D1. One parse owns each measured number

**Problem** (F3, F7): `choukai-items.md` requires ≥1 どのように per 問題2 on a cited
official rate of 18%; my parse of the same 31 files gives 1%. `official_register.md`
§7.4 gives 問題3 talk median 305 (revised from an earlier 257); my parse gives 226.
Papers are being authored to targets that cannot be reproduced, and §6 of
`official_register.md` says outright that its numbers come from an uncommitted
one-shot analysis. **That is the root cause of both conflicts, and it will recur.**

**Decision to take:** the measurement stops being prose and becomes a committed
script (Phase 1). Then re-derive the 問題2 質問型 mix and the 問題3 length band with
it, and update whichever of the two documents is wrong.

**Output:** a single table of official baselines, generated by the script, pasted
into `official_register.md` with the parse rule printed beside each row.

### D2. The pitch margin — settle it by measurement, in semitones

**Problem** (F6): three numbers, all written down. `choukai-audio` Part 2 says
~25 Hz female / ~20 Hz male and names 職員(−14 Hz) beside 女(+0 Hz) as under margin.
`check_consistency.py:7050` flags only below **10 Hz**, and only for two-label
items. `qa/qa-report-20260811_1.md` §6 adjudicated the 14–18 Hz pairs a **GATE-WRONG
false positive**, from the half of the doc that carries no number, and its §7 records
that the MP3 was never played.

**Why a listen is the wrong instrument anyway.** The dispute is about audibility, and
audibility of a pitch difference is logarithmic — so Hz is the wrong unit, and the
doc's two numbers are not even equivalent to each other:

| pair | Δ in Hz | on a base of | Δ in semitones |
|---|---|---|---|
| Part 2's female margin (女 vs a role label) | 25 Hz | ~210 Hz | **1.95 st** |
| Part 2's male margin | 20 Hz | ~120 Hz | **2.67 st** |
| 女(+0) vs 職員(−14), 9 shipped items | 14 Hz | ~210 Hz | **1.12 st** |
| 係員(+18) vs 妻(+16), `20260807_1` 問題5-2番 | 2 Hz | ~210 Hz | **0.16 st** |
| 男(+0) vs 部長(−18), `20260817_2` 問題1-3番 | 18 Hz | ~120 Hz | **2.42 st** |

One semitone threshold replaces both Hz numbers and makes the gate gender-agnostic.
0.16 st is inaudible on any voice; 1.12 st is about the width of a sung whole tone
and is the case genuinely in dispute.

**And the reframe already decides three of the disputed items.** Under the fallback
thresholds below, `20260807_1`'s 0.16 st is a FAIL, the female 14–20 Hz pairs land in
the WARN band where QA settles them, and `20260817_2`'s 男/部長 pair — flagged as
"under margin" by the Hz rule (18 < 20) — **clears at 2.42 st**. That is the whole
argument for the unit change: the Hz rule was condemning the one pair that is
comfortably audible and passing the one that is not.

**The measurement, which an agent can run:**

1. Build the two disputed papers with `--keep-segments`, then estimate **median F0 per
   speaker per item** (autocorrelation or YIN on the 24 kHz mono segments — same
   detector both sides, as `official_pacing.md` §5 already insists for speech rate).
   Report Δ in semitones, not Hz.
2. Establish the reference from the archive: official 問題5-1番 has ≥3 speakers in
   31/31 sittings since 2020, so every sitting contains at least one **same-gender
   pair**. Measure their F0 separation the same way. That distribution — not a
   preference — is the band our pairs must reach.
3. Set the gate FAIL below the official band's lower edge and WARN between that and
   the authoring target. Write the number in **semitones** in all three places in the
   same change: Part 2's prose, the gate threshold, and a one-line note in
   `qa/qa-report-20260811_1.md` recording that its §6 adjudication was revisited with
   the margin sentence in hand.

**Fallback, if F0 extraction proves unreliable on TTS segments** (edge-tts pitch
shifts are synthetic and may quantise): adopt **≥1.9 st** as the authoring margin —
the semitone value Part 2's own female number already implies — FAIL below **1.0 st**,
WARN between. That catches `20260807_1`'s 0.16 st immediately, puts the nine 1.12 st
items in the WARN band where QA settles them, and invalidates nothing on a number
nobody has derived. Record it as decided by rule, and note that a listener may
overturn it later.

### D3. Repair scope for the 13 shipped papers

**The rule, applied per finding without asking.** Tier A and B are always repaired —
their cost is minutes, or zero inside the rebuild window. Tier C is repaired when any
of these is true, and grandfathered with a written reason when none is:

1. the finding is **exam-breaking** — a mis-key, a second defensible answer, an
   answer audible in the wrong place (this overrides tier and age: repair it now,
   then re-run `exam-qa-review`, per the autonomy contract's one hard stop);
2. the finding would be a **gate FAIL** for a non-grandfathered id — i.e. the paper
   sits outside the archive's whole range, not merely off its median;
3. the paper is one of the **three most recent** — those are what the next author
   copies, so a defect left there propagates.

Otherwise: grandfather by id, with the reason and the id-removal condition written
next to it. Ranked by priority when time is finite: exam-breaking → gate-FAIL class →
audible defect → distribution WARN.

Applying that rule to this report gives:

| Class | Papers | Action |
|---|---|---|
| Text-only artifacts (wrong 消去方法 tokens, stale 解説 quotes) | 1 + n | **repair** — Phase 5 tier A. No audio rebuild. The 7 missing 構成表 were also tier A until 2026-08-20; all 7 are C2 papers, so their tables now come from the regeneration instead (§5C.1). |
| Bounded script edits (F6 casting, F10's 問題3 options, split turns, filler/reaction counts) | 11 | **repair** — Phase 5 tier B, landed inside Phase 4's rebuild window, where the marginal cost is zero. |
| Section-level design (F1, F2, F3, F7) | 13 | **tier C by rule**, split by *method* per the 2026-08-20 decision: the three most recent papers get targeted item rewrites (**C1**); the eight papers whose 聴解 fails on three or more axes at once get the section **regenerated wholesale** against the Phase 2 rules (**C2**); three papers are grandfathered with the reason recorded. Every paper named by clause 2 or 3 lands in C1 or C2 — none is dropped. See §5C. |
| Pause distribution (F8) | all 14 | rebuilt as a side effect of Phase 4, at no extra cost. |

The split, and every id the rule grandfathers, goes in the final report — an
unstated skip is the thing that keeps shipping (`AGENTS.md` §0.7).

---

## Phase 1 — `tools/choukai_profile.py`: one measurement, two consumers

**Why this is first.** Every conflict in this report (F3, F7) and the two corrected
figures already recorded in `official_register.md` §7.1/§7.4 have the same cause:
the numbers live in prose, the gate re-implements them, and nothing forces the two
to agree. `official_register.md` §6 documents the five parse rules and then says
"not committed as a script."

**Build it.** New file, repo-level (it measures `refs/` and `tests/`, so it is not a
skill script — same class as `tools/check_consistency.py`):

```
tools/choukai_profile.py [--official] [--tests <id>…] [--json] [--baseline]
```

- **One parser, two front-ends.** Official: `refs/JLPT_N2_NEW/*/script.md`, split on
  `^#+\s*問題\s*[1-5１-５]`, item lines `^\d+\s*番`, turns from the speaker-tag regex
  with wrapped OCR lines rejoined into the preceding turn, `問い` lines and
  `（正解：N）` read separately. Generated: blocks on blank lines, sections on
  `^問題N。$`, turns on `^label[：:]`, spoken options on `^[1-4]、`. The two
  front-ends must produce the same record type: `{section, item, leadin, question,
  turns[], options[], key}`.
- **Emit every number this report used**, per paper and pooled: turn count and
  length distribution, short-reaction share, opener share, filler count, 縮約形 /10k,
  flat-denial /10k, さん /10k, 一番 /10k, まず-in-問題1, 問題1 質問型 histogram,
  問題1 single-speaker item count, proposal-turns-per-item, decider position (from
  the 解説 quote), 問題2 質問型 histogram, 問題3 speaker type + talk length + option
  suffixes, 問題4 stimulus register + reply shapes, 問題5 speaker counts, resolved
  voice balance per 大問, and same-voice pitch gaps.
- **`--baseline`** prints the official table in the exact Markdown that
  `official_register.md` carries, so refreshing the doc is a paste, not a retype.
- **`check_consistency.py` imports it** instead of re-implementing the counts. The
  gate keeps owning the *thresholds*; the script owns the *measurement*.

**Acceptance test:** `python3 tools/choukai_profile.py --official --baseline`
reproduces every official figure in `official_register.md` §§1–7, or the doc is
edited to what it prints — with the parse rule named on the row. Then `make check`
is green and its choukai numbers are byte-identical to the script's.

**Effort:** the largest single item in this plan (~400–600 lines), and it pays for
itself the first time a quota is questioned.

---

## Phase 2 — rule changes, by owner file

Each row is the rule to write. Numbers marked **(gate)** also become a check in
Phase 3; the rest are authoring targets that QA settles off the 構成表.

### 2.1 `jlpt-exam-structure` — the 問題1 question-line inventory (F1)

Today this file owns the instruction lines but not the *question* lines, so nothing
told an author that 「この後まず何をしますか」 is one frame among several. Add a
§"問題1 question forms" table with the archive's inventory (re-derived per D1):

| Frame | Official share | Example |
|---|---|---|
| この後/これから + まず + 何をしますか・しなければなりませんか | ~40% | 「女の職員はこの後まず何をしますか」 |
| 何をしますか・しなければなりませんか, no まず | ~37% | 「女の職員はこの後何をしますか」 |
| どう/どのように 〜ますか (modify a draft, a poster, a booking) | ~12% | 「学生はスピーチの原稿をどう直しますか」 |
| どの〜を選ぶ/押す/買う (condition match) | ~5% | 「どの番号を押せばいいですか」 |
| 何を持って行く/出す/書く (object) | ~4% | 「料理教室に何を持って行かなければなりませんか」 |
| いつ/いくら/どこ | ~3% | 「今ここでいくら払いますか」 |

Note the two facts a generator needs beside it: **課題理解 options may be a SET**
(Shin Kanzen 問題紹介 例題1 keys アウ against アイウ/アウオ/ウオ), and **~14% of
official 問題1 items are single-speaker** (announcement, 留守番電話, 課長からの
メッセージ, automated menu).

### 2.2 `question-authoring/references/choukai-items.md` — quotas (F1, F2, F3, F4, F7)

Extend §"Section item mix" — the existing quota table is the right home; it is
missing the question-shape and register dimensions entirely.

| 問題 | Rule to add | Official | **(gate)** |
|---|---|---|---|
| 1 | ≤3 of 6 items on the まず frame; ≥1 modify/method; ≥1 condition-match or object frame | 40% まず / 12% modify / 9% condition+object | yes, ≥5 of 6 on one frame FAILs |
| 1 | ≥1 non-dialogue item per paper (announcement / message / automated menu) — may be placed in 問題1 or 問題3 | 14% of 問題1 | WARN |
| 1 | ≤2 of 6 items may carry ≥3 proposal-and-deny turns ("the probe carousel") | 1 item in 154 | yes, >3 FAILs |
| 1 | The decider's position must not share a bucket (first/middle/last third) in more than 3 of 6 rows | — | yes |
| 2 | **≥2 of 6 must be a content/reported-statement question** (何・どんな・〜と言っていますか) | 33% + 38% | yes, 0 FAILs |
| 2 | 一番 ≤2 **and** 理由 ≤3 of 6 — the existing floor gets a ceiling | 6% / 22% | yes |
| 2 | ≥1 item keyed to a speaker's 気持ち (Shin Kanzen 問題紹介 p.4: 「理由や目的、話し手の気持ち」) | 5% | target only |
| 3 | ≤2 of 6 institutional/expert speakers — the existing rule, restated as the *speaker*, not the setting | 42% institutional, 33% ordinary person | WARN → FAIL at 5 of 6 |
| 3 | Talk length: a **band**, not a floor — target 220–300 spoken chars, gate FAIL below 175 and above the archive maximum (per D1) | median 226–305 depending on parse | yes, two-sided |
| 4 | ≥5 of 12 stimuli clearly casual; ≤2 keigo counter prompts | 49% casual / 13% keigo | yes, 0 casual FAILs |
| 4 | No stimulus addressed to a class of people (「〜の方は、…窓口へ」) — the existing "never broadcast" rule, with this wording added as the failing shape | — | WARN |

Also add, in §"Eliminated ≠ contradicted": **the elimination-device tally being
perfectly flat is itself a signature.** `20260819_1` 問題1 uses each of the nine
tokens in exactly 2 of 6 rows. Official does not distribute devices evenly; it
prefers reassign/defer and reaches for the others rarely. Rule: the nine tokens are
a *ceiling* per row, not a checklist to fill.

### 2.3 `choukai-audio/SKILL.md` — register, casting, pacing (F2, F5, F6, F8, F9)

- **Rule 6 becomes two-sided.** Current text bans "always last". Add: "…and it must
  not always arrive first. Across a 大問, decider positions must not all fall in one
  third of their items — `20260818_1` and `20260819_1` put 14 of 15 in the first
  third after this rule landed, which is the same defect with the sign flipped."
- **§Banned formulas** gains the current inventory, with counts (F9):
  「かしこまりました」12/14 papers, 24× vs 4× in 31 sittings; 「〜ていただけますか」
  25×; 「よろしいでしょうか」13×; 「あ、そうなんですね」17×; 「〜た方がいいですか」
  13× against **0 in the archive**. Rule: no service formula above the archive's
  per-paper rate, and 「〜た方がいいですか」 is not "banned as every probe" but
  simply a phrase the archive never uses.
- **§Register** gains the turn-shape row: our median turn is 27 chars over 2,061
  turns against official's 38, with more turns per paper. Correct §1's "turn LENGTH
  is already right" once D1's parser settles it.
- **Part 2 gains gendered role pairs** (F5): state that `SPEAKER_MAP`'s role labels
  are 14 female / 9 male and that every service and expert role is female, so a
  paper that uses role labels lands on one voice. Rule: **no 大問 may exceed 70% of
  its turns on one voice**; role labels come in pairs (Phase 4.1) and the author
  picks per item. Keep the existing "remapping an existing label is a last resort"
  warning — it is why Phase 4.1 *adds* labels instead.
- **Part 3 gains a distribution row** (F8): the pacing table measures medians; add
  the shape. Under one method (`silencedetect -35dB d=0.30`, silences <2 s), the
  official 7/2025 MP3 and the Shin Kanzen CD both put **21–24% of pauses above
  1.05 s**; our rendered audio puts **1%** there and 60% into two spikes at 0.5 s
  and 0.9 s. Rule: verify the *distribution* on the rendered MP3, not the median.

### 2.4 `choukai-audio/references/official_pacing.md` and `official_register.md`

Mirror Phase 1's output. Replace §6's "not committed as a script" with the command
that reproduces every number, and add the third corpus: the Shin Kanzen mock tracks
measure turn gaps median 0.66 s (p75 1.04, p90 1.22), answer pause ~9.8 s, loudness
−13.8 to −15.2 LUFS — corroboration that 0.9 s sits at the slow edge and that our
12 s answer pause is the exam's, not the textbook's.

---

## Phase 3 — gate lines, so none of this can regress silently

New checks in `tools/check_consistency.py`, §G16's block, each importing its
measurement from Phase 1. House style: the docstring carries the incident, the
failure message carries the repair, the threshold sits outside the archive's whole
range, and any existing paper that breaches it is named in a grandfather set that
the owner doc also names.

| Check | Measures | FAIL / WARN | Grandfathered |
|---|---|---|---|
| `check_choukai_q1_question_forms` | 問題1 質問型 histogram from the repeated question line | FAIL at ≥5 of 6 on one frame; WARN below the ≥1-modify/≥1-condition targets | all 13 (100% single-frame) |
| `check_choukai_decider_position` | position bucket of each item's decider, from the 構成表's 決め手の位置 column | FAIL when >3 of 6 rows share a bucket | `20260813_2`, `20260817_2`, `20260817_3`, `20260818_1`, `20260819_1` |
| `check_choukai_probe_carousel` | proposal turns per 問題1 item | FAIL at >3 items with ≥3 proposals | `20260818_1`, `20260819_1` |
| `check_choukai_q2_question_mix` | 問題2 質問型 histogram, priority-ordered | FAIL at 0 content/reported-statement items or >4 on one type | all papers except `20260813_2`, `20260814_1` |
| `check_choukai_q4_stimulus_register` | keigo vs casual markers on the 12 stimuli | FAIL at 0 clearly-casual; WARN above 4 keigo counter prompts | most papers — measure first, then name |
| `check_choukai_q3_talk_band` | replaces the one-sided length check with a band | FAIL below 175 or above the archive max | papers already WARNing on the floor |
| `check_choukai_voice_balance` | resolved voice share per 大問 | WARN above 70%, FAIL above 85% | 問題3 in ~10 papers |
| `check_voice_casting` (extend) | same-gender pitch gaps in items with **≥2** labels, not exactly 2 | FAIL below D2's number; WARN between it and the margin | the nine two-party pairs, pending D3 |
| `check_choukai_service_formulas` | per-paper rate of the §Banned-formulas inventory | WARN above the archive's per-paper max | — |
| `check_choukai_pause_distribution` | share of sub-2 s pauses above 1.05 s in the rendered MP3 | WARN below 10% | all 14 until Phase 4.2 lands |

Two notes on scope, so the checks do not over-promise:

- **Read the 構成表, do not re-derive.** `check_choukai_decider_position` reads the
  column the author already fills, exactly as `check_choukai_elimination_tokens`
  reads 消去方法. That keeps the artifact authoritative and the check cheap — and it
  means the 構成表 must gain the 決め手の位置 column for the papers that lack it, or
  the check skips them.
- **`check_choukai_pause_distribution` needs the MP3**, so it belongs behind the
  same `if origin == "generated"` guard as the sha checks and must skip cleanly when
  the audio is absent.

---

## Phase 4 — the audio work, in ONE rebuild

Both changes here move `pacing_sha` or `SPEAKER_MAP`, and each rebuild is ~33 MB of
new Git LFS object per paper (13 MP3s are committed today). **Batch them.** Do 4.1
and 4.2 in one commit, then rebuild once.

### 4.1 Gendered role labels (F5)

**Add**, never remap — a remap silently re-voices every existing paper, and
`script_sha` does not hash the map:

```
"職員2":  {"voice": MALE, "rate": "+0%",  "pitch": "-14Hz"},   # male counterpart of 職員
"係員2":  {"voice": MALE, "rate": "+0%",  "pitch": "+8Hz"},
"担当者2":{"voice": MALE, "rate": "+0%",  "pitch": "-20Hz"},
"講師2":  {"voice": MALE, "rate": "-6%",  "pitch": "-24Hz"},
"専門家2":{"voice": MALE, "rate": "-6%",  "pitch": "-10Hz"},
"店員2":  {"voice": MALE, "rate": "+4%",  "pitch": "+12Hz"},
"医者2":  {"voice": MALE, "rate": "+0%",  "pitch": "-8Hz"},
"アナウンサー2": {"voice": MALE, "rate": "+4%", "pitch": "+6Hz"},
```

Naming is a judgment call — `職員2` reads as "the second 職員 in one item", which is
not what these are. Prefer explicit gender: `男性職員` / `女性職員`, and keep the
bare label as an alias for the existing female mapping so no shipped script breaks.
Whichever is chosen, **`SPEAKER_MAP` is not hashed into `script_sha`, so adding
labels alone does not force a rebuild** — only 4.2 does.

### 4.2 Pause jitter (F8)

The constants are right; the *distribution* is degenerate because every turn gap is
exactly `GAP_BETWEEN_LINES` and every within-turn pause is capped at
`GAP_WITHIN_TURN_MAX`.

Design constraints, both from the existing code:

- **Deterministic.** `make_silences()` pre-creates every silence the plan needs and
  a warm cache must be byte-identical to a cold build. Derive the jitter from a
  stable hash of the line text, e.g. `ladder[sha1(line)[0] % len(ladder)]`.
- **Quantised.** Silence files are named `_sil_{s:g}.wav`, so a continuous jitter
  would create hundreds of tiny WAVs. Use a short ladder — e.g.
  `(0.65, 0.90, 0.90, 1.15, 1.40)` — which keeps the median near 0.9, restores a
  ~20% tail above 1.05 s, and adds three files to the cache.
- Weight the long values toward turn boundaries that follow a question or a short
  reaction, where both reference corpora put their long beats.
- Consider raising `SHAPE_PAUSE_FLOOR`/`GAP_WITHIN_TURN_MAX` handling so a
  sentence-final 。 inside a long turn can keep a ~0.7 s beat instead of being
  capped to 0.5 s. Measure before choosing; official's within-turn p90 is 0.72 s.

**Then, in this order:** `make mp3 <id>` and `make sheet <id>` for all 14 papers →
`make pages` → `make check`. Budget ~2 min per paper plus the LFS churn. The
acceptance test is not the constant: re-run
`check_choukai_pause_distribution` on two rebuilt MP3s and confirm the >1.05 s share
lands in 10–25%, and that the two spikes hold under 35% of pauses.

### 4.3 The one content repair (F6, per D3)

`20260807_1` 問題5-2番: recast 妻(+16 Hz) or 係員(+18 Hz) so the enumerating voice and
the two deciders are three distinguishable people — simplest is to move the
enumerator to a male label (`店長`, or 4.1's new `男性係員`), which also fixes the
item's all-female casting. Then `make mp3 20260807_1` + `make sheet 20260807_1`.
This one rides along in the Phase 4 batch, with the rest of Phase 5's tier B.

---

## Phase 5 — the 14 papers on disk

Phases 1–4 improve the *pipeline* and the *next* paper. They leave the papers a
learner can take today almost untouched. This phase is the other half, and it is
tiered by **what a repair costs**, not by how bad the defect is — because the cost
is dominated by one thing: whether the fix touches `聴解スクリプト.txt`.

The tier of any given repair is **derived mechanically** from the artifact it touches (§5.0) — it is never something a session decides.

| Tier | Touches | Rebuild needed | Marginal cost |
|---|---|---|---|
| **A** | `聴解.md` only (構成表, 解説 cells, printed 問題1/2 options) | `make booklet <id>` + `make sheet <id>` (+ `make pages`) — the `src_sha` stamps make this mandatory | minutes per paper, **no audio** |
| **B** | `聴解スクリプト.txt` (spoken lines, spoken options, speaker labels) | `make mp3 <id>` + `make sheet <id>` | **zero, if done inside the Phase 4 rebuild window** |
| **C1** | re-authoring some of a section's items | same as B | real authoring work, ~8 items over 3 papers |
| **C2** | `--reroll` + re-authoring a whole 聴解 section | same as B | real authoring work, ~30 items × 8 papers — **plus §5D's explanation, translation and QA tail, which is larger than the authoring** |

**The scheduling insight that makes Tier B affordable:** Phase 4 already rebuilds all
14 MP3s for the jitter change. Every script edit landed in the same window is free —
no extra rebuild, no extra LFS churn. Do the Tier B list *before* pressing the
rebuild, or it costs 33 MB per paper to redo later.

### 5.0 The tier is DERIVED from the artifact, so every session computes the same one

This is not about keeping judgment out of the loop — it is about keeping the *same*
judgment in it. A tier assigned ad hoc per repair drifts: the same defect gets called
A by one session and C by the next, and the batching in §5B — the thing that makes
~30 script edits free — silently breaks the first time something lands outside the
rebuild window. So the tier is derived rather than decided: it is a **pure function of
which artifact the repair touches**, and that is a static property of the *check that
found the defect*, declared once at the check:

```
tier = { "聴解.md": "A", "聴解スクリプト.txt": "B", "<section re-author>": "C" }[artifact]
```

**Where the declaration lives.** `tools/check_consistency.py` gains one table next to
§G16, keyed by a stable finding slug — not by the check's f-string title, which
changes whenever a message is reworded:

```python
# artifact a repair touches -> tier is derived; automation class is declared.
FINDING_REPAIR = {
    "choukai_section_table_missing":  ("聴解.md",             "assisted"),
    "choukai_elimination_tokens":     ("聴解.md",             "assisted"),
    "choukai_voice_margin":           ("聴解スクリプト.txt",  "deterministic"),
    "choukai_split_turns":            ("聴解スクリプト.txt",  "deterministic"),
    "choukai_contraction_rate":       ("聴解スクリプト.txt",  "deterministic"),
    "choukai_q3_option_suffix":       ("聴解スクリプト.txt",  "assisted"),
    "choukai_filler_band":            ("聴解スクリプト.txt",  "assisted"),
    "choukai_reaction_floor":         ("聴解スクリプト.txt",  "assisted"),
    "choukai_service_formula_rate":   ("聴解スクリプト.txt",  "assisted"),
    "choukai_q1_question_forms":      ("<section re-author>", "authoring"),
    "choukai_q2_question_mix":        ("<section re-author>", "authoring"),
    "choukai_decider_position":       ("<section re-author>", "authoring"),
    "choukai_probe_carousel":         ("<section re-author>", "authoring"),
    "choukai_q3_talk_band":           ("<section re-author>", "authoring"),
    "choukai_q5_speaker_count":       ("<section re-author>", "authoring"),
    "choukai_q4_done_concentration":  ("<section re-author>", "authoring"),
}
```

**Three rules that keep the mapping honest**, each of which exists because the
alternative is a silent under-scope:

1. **Declare the cheapest SUFFICIENT artifact.** A key-length problem could be
   patched by editing printed options (`聴解.md`, tier A) or by rewriting the
   deciding line (script, tier B). Declare the one that actually repairs the defect,
   not the one that hides it — for key length that is the script, because
   `choukai-items.md` says raise the distractors, never trim the key.
2. **Escalation is allowed, de-escalation is not.** A tier-B repair that turns out to
   need a re-authored item is recorded as escalating to C, with the reason. A tier-C
   finding may never be quietly settled by a text edit — that is how a 消去方法 label
   outlived the line it described (`choukai-items.md` §消去方法). **C1 vs C2 is not
   part of this derivation**: the artifact says "re-author", and the *paper's* axis
   count (§5C) then says whether that means some items or the whole section. A paper
   already in C2 absorbs any escalation for free — record it, but do not schedule it
   separately.
3. **A check with no declaration is a gate failure, not a default.** Add the
   meta-check `check_every_choukai_finding_declares_repair()`: if a §G16 check fires
   for a slug absent from `FINDING_REPAIR`, FAIL. The repo already asserts that docs
   match code this way; the same reflex applies here. Defaulting an unknown finding
   to tier C would be *safe* but would quietly grow tier C forever; failing makes
   somebody classify it once.

**Where the plan comes out.** `check_consistency.py` gains a `--json` mode emitting
one record per finding — `{slug, test_id, status, artifact, tier, automation, detail}`
— and a thin consumer turns it into the work order:

```
make findings                  # tools/check_consistency.py --json -> logs/findings.json
make repair-plan [<id>]        # tools/choukai_repair_plan.py -> qa/<id>/repair-plan.{json,md}
make repair-plan TIER=B        # just the batch that must land before the rebuild
```

`repair-plan.md` is the operator's page, and every field on it is derived:

- findings grouped **A / B / C**, each with the id, the item, the measurement, and
  the owner-doc section that states the rule;
- the **rebuild set** — the ids with ≥1 tier-B finding, i.e. exactly the papers that
  need `make mp3` + `make sheet` — printed as the command list, so batching is
  mechanical rather than remembered;
- the **deterministic subset**, printed as the single `make autofix <id>` invocation
  that applies it;
- what is *not* in the plan: tier-C findings for papers the operator declined, listed
  with their grandfather reason, so a decline is visible rather than absent.

**Thresholds stay in one place.** The gate owns thresholds, `choukai_profile.py`
(Phase 1) owns measurement, `FINDING_REPAIR` owns the artifact, and the tier is
derived from the artifact. The repair-plan tool computes nothing of its own — if it
did, it would be the fourth copy of a number, which is the defect this report opened
with (F3, F7).

**What the derivation does and does not settle.** It settles *which lane a repair is
in* — mechanically, so two sessions on the same corpus produce the same work order.
It does not settle two other things, and neither of them needs a question asked:

- **Whether a tier-C paper gets repaired** — D3's rule decides that, by clause, and
  the agent applies it and records the outcome.
- **What to write.** The `automation` column says how much of the fix the *tooling*
  produces, not whether a human is involved: `deterministic` (the tool rewrites the
  line), `assisted` (the tool localises the lines and measures the target, the author
  writes them), `authoring` (a re-written item). All three are the agent's work; only
  the first is free.

### 5.0.1 The deterministic subset — extend `make autofix`, don't build a second lane

`tools/lint_draft.py` already owns this lane (`autofix_script()`,
`autofix_gengo_md()`, `make autofix <id>`), and already nudges the 縮約形 rate with
`--fix`. Add the three findings that are genuinely mechanical:

| Finding | Deterministic rule | Verified afterwards by |
|---|---|---|
| `choukai_split_turns` | two consecutive lines with the same label → one line joined at 。 | `check_script_register`'s split-turn FAIL goes quiet; the reaction share is re-measured *without* the fake short turns |
| `choukai_voice_margin` | swap the offending label for the widest-margin same-role alternative in `SPEAKER_MAP` (Phase 4.1's gendered pairs make this always available) | the existing narration-gender check, which FAILs if the swap contradicts 「〜の男の人」 |
| `choukai_contraction_rate` | the existing `--fix` conversions (〜ている→〜てる etc.), announcer lines excluded | the contraction-rate WARN, and `make check`'s script/pacing sha lines forcing the rebuild |

Everything else stays `assisted` on purpose. Stripping 「〜について」 off a 問題3
option is *not* deterministic — 「一人旅について」 does not become a well-formed
option by deletion, it becomes 「一人旅をするよさ」, which is a writing decision. A
tool that pretended otherwise would ship 20 malformed options per paper and a green
gate.

### Tier A — text-only

> **Superseded in part, 2026-08-20.** Tier A's bulk item was backfilling the missing
> セクション構成表 in the 7 papers that have none — `20260807_1`, `20260810_1`,
> `20260810_2`, `20260811_1`, `20260812_1`, `20260812_2`, `20260813_1`. **All seven
> are C2 papers**, and a regenerated section writes its own table to the corrected
> column list, so backfilling them is work done twice. **Dropped** — with Phase 3's
> 構成表-reading checks carrying the 8 C2 ids as a grandfather set instead (§5C.1).
> Phase 1's proposed `--scaffold-table <id>` mode loses its main consumer with it;
> build it only if it earns its place elsewhere. If C2 is cancelled or stalls, this
> backfill comes back — see §Risks.

What remains in Tier A is the per-paper text repair below, plus the column-set fix,
which is now MORE load-bearing than before: C2 authors 8 tables from scratch against
whatever the list says at that moment.

**Note on the column set.** The 構成表 is accumulating columns — 場面, 主導, 正解,
消去方法, 質問型, and now `決め手の種類` (added for `20260819_1`'s
one-axis-twice defect). Phase 2 adds two more (`決め手の位置`, proposal count).
**Fix the column list once in `choukai-items.md` §"Write the SECTION TABLE" before
any C2 paper is authored**, so all 14 papers carry the same table, and state for each
column whether it is capped, read-down-only, or gate-read. This got MORE urgent when
the backfill was dropped, not less: C2 writes 8 tables from scratch, and eight tables
authored against a list that changes next week is the expensive way to do this.

Also in Tier A, per paper:

- `20260817_2` — 消去方法 cells carry 5 tokens outside the closed nine
  (「割り当て」×4, 「工程差し替え」) and 後回し in 4 rows against the 2-row cap. It is
  a WARN only because the id is grandfathered; the cells are wrong regardless, and
  re-deriving them is text-only.
- Every paper whose 解説 quotes a line the script no longer contains — that is
  exactly the failure `choukai-items.md` §消去方法 records ("a label that outlives the
  line it describes"). For C2 papers this is absorbed by the regeneration; check it
  on the non-C2 papers, and on any paper a Tier B script edit touches.

### Tier B — script edits to land inside the Phase 4 rebuild

Highest value first. Each is a bounded edit, not a re-authoring.

> **Scope narrowed, 2026-08-20 (§5C.1).** Rows below for `20260807_1`, `20260811_1`,
> `20260812_1`, `20260812_2`, `20260813_1` and `20260813_2` are **C2 papers whose
> scripts are about to be replaced** — skip them; the regeneration covers the same
> defects. Tier B is now the 6 non-C2 papers. **One exception, and it ships first:**
> `20260807_1` 問題5-2番 is the only FAIL-class casting defect on disk and it is one
> label — repair it now rather than waiting for that paper's regeneration.
>
> **Gap found while reconciling:** F6 lists 問題5-2番 casting pairs at 14–20 Hz in
> `20260812_1`, `20260814_1` and `20260817_1`, but only `20260817_1` and `20260814_1`
> survive outside C2 — **and neither has a Tier B row below.** Add one for each when
> D2 settles the margin, or two grandfathered papers keep a defect nothing tracks.

| Paper | Edit | Finding | Auto? |
|---|---|---|---|
| `20260807_1` | 問題5-2番: move the enumerator off 係員(+18 Hz) so it is not 2 Hz from 妻(+16 Hz) — one label per line | F6 — **0.16 st, the only FAIL-class casting defect** | deterministic |
| `20260811_1` | 問題1-3番, 問題1-5番, 問題2-2番, 問題2-5番: 4 two-party items on one voice, 1.12–1.42 st apart → swap one label to a male role | F6 — WARN band; fix while the script is open, since the rebuild is free | deterministic |
| `20260812_2` | 問題1-3番, 問題1-5番, 問題2-4番, 問題2-6番, 問題5-1番: same, 5 items, 1.12–1.57 st | F6 — WARN band | deterministic |
| `20260817_2` | 問題1-3番: **no edit** — 男/部長 is 2.42 st, above the margin; the Hz rule flagged it wrongly | F6 (resolved by D2) | n/a |
| `20260819_1` | 問題5-2番: 女/職員 at 1.12 st — and its 構成表 documents the 14 Hz split as compliance, so fix the table in the same pass | F6 — WARN band | deterministic |
| `20260811_1`, `20260812_1`, `20260812_2`, `20260813_1` | rewrite all 20 問題3 spoken options per paper from 「〜について」 to bare noun phrases (official: 1%) | F10 | assisted |
| `20260813_2` | split-turn repair: 9 pairs of consecutive same-speaker lines → one turn, one line (each currently buys a fake 0.9 s gap and inflates the reaction rate) | F10 | deterministic |
| `20260810_2`, `20260813_2` | 問題4: reduce already-done distractors from 8/11 and 9/11 to ≤2 items — re-word the distractor, not the key | F10 | authoring (escalates to C) |
| `20260812_1` | filler count 50 → inside the 9–48 band; the surplus is stalling, not acknowledging — convert some to the OTHER speaker's 「うん」 | F10 | assisted |
| `20260814_1` | short-reaction share 7.5% → ≥12%: add reaction turns from `official_register.md` §2.1's inventory | F10 | assisted |
| `20260817_3` | re-angle the 問題2 例 off 「ビジネスホテルのフロント」 so 5番's 「ホステルの受付」 is not the same errand twice — this clears the last id in `SETTING_ADJACENCY_GRANDFATHERED` | F10 | assisted |
| all 14 | while the script is open: trim the service formulas above the archive rate (「かしこまりました」 24×, 「〜た方がいいですか」 13× against 0 in 31 sittings) | F9 | assisted |

Two of these change spoken options (`20260811_1`, `20260812_1`, `20260812_2`,
`20260813_1`) or a key's grounding, so re-check `聴解.md`'s printed options and 解説
cells in the same edit, and re-run `make verify-scramble`-equivalent sanity — here,
`make check`'s 聴解 block plus a re-read of the 解説 quote against the new line.

### Tier C — section-level repair, by one of two methods

These are the section-level design defects (F1, F2, F3, F7). They cannot be patched —
the items have to be rewritten. **The 2026-08-20 decision is about *how*.**

Item-by-item retrofit is the expensive method, not the cheap one, once a paper fails
on several axes at once. Every edit lands in a section where another item also
breaches a quota, so each rewrite has to be re-checked against the whole section, and
the end state is a paper tuned to the edge of each number — which is exactly the
shape that produced F2: the fix for the last one-sided rule satisfied it to the letter
and grew a new monoculture underneath. Re-authoring the section from a fresh draw
costs the same per item, needs no cross-checking, and cannot inherit the template.

So Tier C splits by method, and the split is derived from a count, not chosen:

> **A paper enters C2 when its 聴解 breaches three or more independent axes**
> (question-frame monoculture, decider position, 問題3 length/speaker, 問題5 party
> count, casting margin, option form, missing 構成表). Two or fewer → C1.

#### C1 — targeted item rewrite (3 papers)

For papers where the rest of the section is sound. Bounded and enumerated.

| Paper | Section | Defect | Work |
|---|---|---|---|
| `20260817_3` | 問題1 | まず-frame monoculture; 例 shares 「ビジネスホテルのフロント」 with 5番 | rewrite 2 of 6 to the new 質問型 quota; re-angle the 例 (clears the last id in `SETTING_ADJACENCY_GRANDFATHERED`) |
| `20260818_1` | 問題1, 問題5-1番 | frame monoculture; 5-1番 repeats `20260817_3`'s archetype (its own QA report's F3) | rewrite 2 of 6 + 1 item |
| `20260819_1` | 問題1 | 6 of 6 on the まず frame, deciders 冒頭/中盤 throughout, 問題5-2番 at 1.12 st | rewrite 3 of 6 — **this is the worked example the next author copies**, so it gets the full mixed-frame treatment incl. one non-dialogue item |

#### C2 — regenerate the 聴解 section wholesale (8 papers)

Re-draw and re-author 問題1–5 against the Phase 2 rules rather than retrofitting.

| Paper | Independent axes failing today | n |
|---|---|---|
| `20260807_1` | 問題3 168–170 chars (under floor); FAIL-class casting (0.16 st); no 構成表 | 3 |
| `20260810_1` | 問題2 6/6 keyed 一番; 問題3 132–166; 問題5-2番 casting; no 構成表 | 4 |
| `20260810_2` | 問題3 144–166; 問題4 8/11 already-done distractors; 問題5-2番 casting; no 構成表 | 4 |
| `20260811_1` | 問題3 174–181; no ≥3-speaker 問題5; 4 same-voice items; 20/20 「〜について」 options; no 構成表 | 5 |
| `20260812_1` | 20/20 「〜について」 options; filler count 50 (band 9–48); 問題5-2番 casting; no 構成表 | 4 |
| `20260812_2` | 問題2 all six deciders at 0.64; no ≥3-speaker 問題5; 5 same-voice items; 20/20 「〜について」 options; no 構成表 | 5 |
| `20260813_1` | no ≥3-speaker 問題5; 20/20 「〜について」 options; no 構成表 | 3 |
| `20260813_2` | 問題1 5/5 service counter with late deciders; 9 split turns; 問題4 9/11 already-done | 3 |

**Grandfathered, with the reason recorded:** `20260814_1` (short-reaction share 7.5%
+ 問題5-2番 casting — 2 axes, both Tier B edits), `20260817_1` (問題5-2番 casting only
— **and note it has no Tier B row today; add one**), `20260817_2` (消去方法 tokens are
Tier A; its 18 Hz casting is cleared outright by D2). Each leaves the set the moment
its 聴解 is repaired.

#### 5C.1 What C2 does to Tier A and Tier B — reconcile BEFORE starting either

This is where the saving actually is, and where the double work hides.

- **All 7 papers missing a 構成表 are C2 papers.** Tier A's backfill of those seven
  tables is therefore *entirely redundant* if C2 proceeds — the regenerated section
  writes its own table, to the corrected column list. **Do not backfill them.** That
  removes Tier A's only bulk item and, with it, the `--scaffold-table` mode Phase 1
  was going to grow for this purpose (keep the mode only if it earns its place for
  future imports).
- **This breaks the Phase 3 dependency as written.** Tier A was scheduled before
  Phase 3 because the new checks read the 構成表 and would otherwise permanently
  `skip` half the corpus. With the backfill dropped, the fix is ordering, not
  scaffolding: **Phase 3's 構成表-reading checks land with a grandfather set of the
  8 C2 ids, and each id leaves the set as its C2 regeneration completes.** That is
  the same mechanism the repo already uses, and it is honest about coverage in a way
  a scaffolded-then-discarded table is not.
- **Roughly half the Tier B list is inside C2 papers** (`20260807_1`, `20260811_1`,
  `20260812_1`, `20260812_2`, `20260813_1`, `20260813_2`). Do not spend a casting
  swap, an option rewrite, or a split-turn repair on a script that is about to be
  replaced. Tier B shrinks to the non-C2 papers: `20260814_1`, `20260817_1`,
  `20260817_2`, `20260817_3`, `20260818_1`, `20260819_1`.
- **One exception, and it ships first:** `20260807_1` 問題5-2番 is the only FAIL-class
  casting defect on disk (0.16 st) and `20260807_1` is a C2 paper. Do not wait for
  its regeneration — it is one label, and a FAIL-class audio defect is shipping to
  learners today (§Default execution order).

#### 5C.2 C2 is a partial re-draw, and the mechanism already exists

A regenerated 聴解 section needs fresh pool entries, and hand-picking them is the
failure `exam-blueprint` §"What gets RECORDED" names outright — an off-pool
substitute cools nothing and can never rotate. The supported path:

```bash
SEED=$(python3 -c "import secrets; print(secrets.randbelow(10**8))")
python3 .agents/exam-blueprint/scripts/sample_items.py --reroll listening_scenarios --seed "$SEED" --test-id <id>
python3 .agents/exam-blueprint/scripts/sample_items.py --reroll quick_response      --seed "$SEED" --test-id <id>
```

Both re-stamp `pools_sha`, record `+reroll(cat,seed)` in the spec's seed expression,
and rewrite that test's ledger entry so `check_draw_provenance()` still resolves.
`--reroll` scopes its post-draw verification to the category it touched, which is
what makes rerolling an OLD paper legal at all now that newer papers exist
(`exam-blueprint` §"A reroll only re-verifies the category it touched").

#### 5C.3 Pool depth — checked, and C2 fits

Run against the live pools on 2026-08-20:

| Category | Pool | Drawn/paper | `cooldown_for()` window | Ineligible at the tightest point | Eligible for a draw of |
|---|---|---|---|---|---|
| `listening_scenarios` | 290 | 21 | `290//21 − 2` = **11 draws** | ≤231 | **≥59** for 21 → 2.8× |
| `quick_response` | 200 | 11 | `200//11 − 2` = **16 draws** | ≤176 | **≥24** for 11 → 2.2× |

**C2 at 8 papers is feasible with no cooldown relaxation** — the draw never has to
step down a level, so no regenerated paper records a weakened rotation guarantee in
its spec. `quick_response` is the tighter of the two; if C2 is ever widened past 8
papers, re-run `--check-depth` first, because that is the category that will relax.

Note what this costs elsewhere: 8 rerolls consume 168 `listening_scenarios` and 88
`quick_response` entries, so the pools stay near-saturated for the next several
papers. Pool growth is parked in `.agents/exam-blueprint/archive/` with no make
targets; if Phase 6 and its successors start hitting relaxation, that is the reason.

### What Phase 5 does and does not fix

**Scope of record, so it is not re-litigated per run:** Tier A shrinks to the
non-構成表 text repairs; Tier B covers the 6 non-C2 papers; C1 rewrites items in the
3 most recent papers; C2 regenerates the 聴解 section of the 8 oldest. 11 of 14
papers get section-level work; 3 are grandfathered by id with the reason and the
removal condition written next to them.

**Net effect when Phase 5 completes:** every paper is gate-measurable (each C2 id
leaves Phase 3's grandfather set as its regeneration lands), no paper ships a
FAIL-class casting defect, no 聴解 section sits outside the archive's range, and the
問題1 question-frame monoculture is gone from every paper a learner is likely to take
next.

**What it still does not fix.** The three grandfathered papers keep their shape —
`20260814_1`'s reaction share and `20260817_1`'s 問題5-2番 casting are Tier B edits,
but neither paper gets F1/F2 treatment. That is a decision, not an oversight:
"not repaired, forward-only" is legitimate, and an unstated skip is the thing that
keeps shipping (`AGENTS.md` §0.7). Both ids are named above with their removal
condition.

---

### 5D — the downstream artifacts a repair drags with it

**This was missing from the plan and is the largest single omission in it.** The tier
table prices a repair at `make mp3` + `make sheet`. That is the cost of changing a
*sound*. Changing an **item** — its script line, its options, or its key — invalidates
four more artifacts, and `AGENTS.md` §5 fixes the order they have to be rebuilt in.

Per paper touched by C1 or C2, after the script and 聴解.md are final:

| # | Artifact | Trigger | Command |
|---|---|---|---|
| 1 | `聴解.mp3`, `聴解_チャプター.json` | any script edit | `make mp3 <id>` |
| 2 | `聴解.html` | any 聴解.md edit (`src_sha`) | `make booklet <id>` |
| 3 | `解答.html` | 1 or 2 — it embeds the chapter JSON verbatim | `make sheet <id>` |
| 4 | **fresh-eyes `exam-qa-review`** | any item change | a context that authored nothing (`AGENTS.md` §5) |
| 5 | `詳細解説.json` | any item change — the explanation cites a line that no longer exists | `make scaffold-explanations <id>`, then author |
| 6 | `詳細解説.<lang>.json` | 5 — every language the paper ships with | `make scaffold-translation` → `make merge-translation` |
| 7 | `模範解答.html` | 5 or 6 — **always last**, after QA passes | `make model-answer <id>` |
| 8 | `_site/` | all of the above | `make pages` |

Steps 5–7 are not bookkeeping. `GENERATE.md` declares Vietnamese (`vi` /
`Tiếng Việt`) as a shipping language, and **13 of the 14 papers on disk already carry
`詳細解説.vi.json`** — including all 8 C2 papers. So a regenerated 聴解 section means
~30 Japanese explanations **and** ~30 Vietnamese ones, per paper. Across the 8 C2
papers that is on the order of 240 explanations and 240 translations — comparable to
the authoring of the sections themselves, and it was nowhere in the cost table.

**Also found while checking this:** `20260819_1` has `詳細解説.json` but **no
`詳細解説.vi.json`** — the only paper missing a language `GENERATE.md` declares.
`make check` already WARNs on it ("ships the Tiếng Việt (vi) model answer GENERATE.md
declares: no 詳細解説.vi.json"), so this is an open warning, not a discovery — it is
listed here because it lands in the same §5D tail. Close it in the pass that
regenerates that paper's explanations after C1, not before: authored now, the C1
rewrite invalidates it immediately.

**The one hard ordering rule:** `make model-answer` is the final step for every paper,
run only after QA has passed and the items are locked (`AGENTS.md` §5). Building it
earlier means building it twice.

**Two consequences for scheduling.**

- **C2 papers should be batched through steps 4–7 as a group**, not paper-by-paper —
  the QA context is the expensive part to spin up, and a reviewer holding the new
  quota table in context can audit several papers against it far cheaper than one.
- **Saved learner state goes stale.** A repaired paper's `ユーザー解答.json` and
  `採点結果.json` still refer to the *old* items, so any result already recorded
  against a C1/C2 paper becomes meaningless — the result screen and the test list
  both read `採点結果.json`. Decide per paper: delete the stale record, or keep it and
  accept that it scores a paper that no longer exists. **Recommendation: delete, and
  say which ids lost a record in the final report.** Note the browser also keeps
  answers in `localStorage` for the Pages build, which no repo-side deletion clears.

---

## Phase 6 — the next paper is the real acceptance test

Everything above is preparation. The proof is one newly generated paper that hits
the targets without a grandfather clause. Run the normal 4-stage pipeline
(`jlpt-test-generation`) with these additions to the 聴解 authoring stage's brief:

1. **問題1**: six items on ≥3 different question frames, including one
   modify/method item and one condition-match item; one non-dialogue item somewhere
   in the paper; ≤2 items with a proposal carousel; deciders spread across all three
   position buckets.
2. **問題2**: ≥2 content/reported-statement questions, ≤2 一番, ≤3 理由, ≥1
   気持ち item.
3. **問題3**: ≥3 ordinary-person speakers (「ラジオで男の人が話しています」), ≤2
   institutional; talks 220–300 chars.
4. **問題4**: ≥5 clearly casual stimuli, ≤2 keigo counter prompts, no
   class-addressed prompt.
5. **問題5**: 1番 with ≥3 speakers cast on ≥3 distinguishable voices, per D2's
   margin.
6. **構成表**: gains the 質問型 (問題1), 決め手の位置, and 提案消去回数 columns, and
   is read as columns before the section is called finished.

Then: `make check` green with **no new grandfather entries**, `make lint-draft`,
`make qa-eval`, and a fresh-eyes `exam-qa-review` pass whose §4 聴解 step reads the
new columns. If any quota needs a grandfather entry for a paper written *after*
Phase 2, the quota is wrong — fix the quota, not the paper.

---

## Phase 7 — the Shin Kanzen script corpus (F11)

A complete N2 聴解 paper plus ~40 exercise dialogues sit unused in
`Shin_Kanzen_Masuta_N2-Choukai.pdf`'s 別冊, in clean typeset Japanese, with the
音の変化・縮約形 and 間接的な答え方 chapters that the register rules already cite by
page number.

1. **Extractor:** `tools/extract_shinkanzen_choukai.py`, reusing the Vision OCR path
   already in `tools/extract_jlpt_n2_new.py` / `tools/vision_ocr.swift`. Emit
   `refs/Shinkanzen/choukai_script.md` in the same fenced `[OCR ▼]…[OCR ▲]` shape,
   with the same "OCR, ~98% accurate, not quotable as exact wording" header.
2. **Make target:** `make extract-shinkanzen`, listed in `AGENTS.md` §4 next to
   `extract-archive`, owned by §3.
3. **Point the skills at it:** `AGENTS.md` §3 (the Shinkanzen bullet), and
   `choukai-audio` Part 4's line about the CD — which today implies no script
   exists. Mark it clearly as **secondary evidence**: a textbook, not the exam, so
   it corroborates shape and register but never sets a target that the 31-sitting
   archive can set instead.
4. **Then feed it to Phase 1's script** as a third front-end, so the register
   inventory can quote a non-OCR-of-a-stencil source for once.

---

## Sequencing, dependencies, and cost

```
D1 ─┬─> Phase 1 (choukai_profile.py) ──> Phase 2 (docs) ──> Phase 3 (gate lines)
    └─> re-derive F3/F7 numbers                                       ▲
                                                                      │
D3 ──> grandfather sets, incl. the 8 C2 ids on the 構成表 checks ──────┘
       (C2 replaces Tier A's backfill: each id leaves the set as its
        regeneration lands — see §5C.1. Nothing blocks Phase 3 now.)

D2 ─┬─> Phase 4.1 casting labels ─┐
    │   [ship 20260807_1 5-2番 NOW — FAIL-class, one label]
    └─> Phase 5B casting repairs ─┤   (non-C2 papers only)
        Phase 4.2 pause jitter ───┼──> REBUILD #1: make mp3 + make sheet ×14
        Phase 5B script edits ────┘    (batch — 33 MB LFS per paper)

Phase 5C1 (3 papers, item rewrites) ─┐
Phase 5C2 (8 papers, --reroll +      ├─> REBUILD #2: mp3+sheet ×11
           full 聴解 re-author) ─────┘   then §5D steps 4–7 as ONE batch:
                                          QA -> 詳細解説 -> vi -> model-answer
Phase 7 (Shinkanzen extract) — independent, any time
                                                     ──> Phase 6: the next paper

Every box above is one or more Phase-R steps: reconcile -> pick next unblocked
step -> do it -> update state -> commit -> stop. A cron routine re-enters that
loop every 4-6 h, so an interrupted run (quota, crash, closed session) resumes
at the next firing with no instruction from anyone.
```

| Step | Size | Forces a rebuild? | Blocks |
|---|---|---|---|
| Phase R (state file + cron routine) | small, once | no | **everything** — it is what makes the rest survive interruption |
| D1 decision | small | no | Phases 2, 3 |
| D2 measurement (F0 in semitones) | small | no | 4.1, 4.3, gate threshold |
| D3 decision | small | no | every grandfather set |
| Phase 1 script | large (400–600 lines) | no | Phases 2, 3 |
| Phase 2 docs | medium, 4 files | no | Phase 3 |
| Phase 3 gate | medium, ~9 checks | no | Phase 6 |
| Phase 4 | small code, large compute | **yes, all 14** | Phase 6's audio claims |
| Phase 5 tier A | small — text repairs only; **the 7-table backfill is dropped** (§5C.1) | booklet+sheet only | — |
| Phase 5 tier B | ~15 bounded edits, non-C2 papers only | **rides rebuild #1 — free if batched** | — |
| Phase 5 tier C1 | 3 papers, ~8 items total | rides rebuild #2 | — |
| Phase 5 tier C2 | **8 papers × a full 聴解 section** (~30 items each) | rides rebuild #2 | — |
| §5D steps 4–7 | **8+3 papers × (QA + ~30 詳細解説 + ~30 vi + model-answer)** | no, but must follow QA | — |
| Phase 6 | one full paper | yes, its own | — |
| Phase 7 | medium | no | nothing |

**Where the cost actually sits.** C2's authoring is ~240 items; §5D's explanation and
translation work on the same papers is ~240 + ~240 more, plus 11 fresh-eyes QA passes.
The listening authoring is under half the total. Any decision to scale this down
should scale down the *number of C2 papers* — which drops all four costs together —
not the per-paper depth, because a partly-regenerated section is exactly the
edge-tuned artifact C2 exists to avoid.

**Default execution order, if the run is cut short.** Stop points are cheap here
because each phase leaves the repo green; an agent working through this should
prioritise in this order rather than asking which to drop: (1) D2 plus the
`20260807_1` 問題5-2番 repair — a FAIL-class audio defect is shipping today and it is
one label; (2) the 問題1 質問型 quota in 2.1/2.2 — the single highest-leverage rule
change, and it breaks F2's template as a side effect; (3) Phase 1 — without it the
next quota is built on an unreproducible number, which is how F3 happened; (4) C1 on
`20260819_1`, because it is the paper the next author copies; (5) C2, newest-first.

**If C2 has to be scaled down, cut papers, not depth** — take them off the C2 list
oldest-first and grandfather them by id with the reason. A half-regenerated section
is the edge-tuned artifact C2 exists to avoid.

**Split by what improves what:** Phases 1–4 and 7 improve the *pipeline* — they make
the next paper better and stop the regression recurring, but change almost nothing a
learner would notice in the papers already on disk. **Phase 5 is the only phase that
improves those papers**, and after the 2026-08-20 decision it is also the largest:
11 of 14 papers get section-level work, and §5D's QA/explanation/translation tail on
those 11 is bigger than the listening authoring itself. The plan is deliberately
both halves — strengthen the rules, then remake the papers against them — because
either alone leaves the corpus in the state this report measured.

## Risks to watch

- **Phase 1 re-measurement may move numbers the current papers were built to.**
  That is the point, but it means the grandfather sets in Phase 3 must be computed
  *after* Phase 1, not guessed now.
- **Phase 4.2 changes how every paper sounds.** The jitter ladder is a taste
  decision as much as a measurement; keep the median at 0.9 s so the change is
  additive (a tail appears) rather than a re-timing.
- **LFS growth**: one full rebuild is ~460 MB of new objects. Batch, and avoid
  rebuilding to test — measure the distribution on two papers first.
- **Grandfathering fatigue**: adding nine checks with nine exemption sets makes
  green weaker, not stronger. Every set added in Phase 3 needs the id-removal
  condition written next to it (`choukai-items.md` §場面 does this well: "an id
  leaves the set the moment that paper's 聴解 is repaired").
- **The 構成表 becomes load-bearing** for three new checks, and the 7 papers missing
  one are all C2 papers. The mitigation is no longer a backfill but a grandfather set
  of those 8 ids on the 構成表-reading checks, emptied as C2 lands (§5C.1). **The risk
  is that C2 stalls and the set becomes permanent** — which is the "grandfathering
  fatigue" failure one bullet up. If C2 is not going to finish, backfill the tables
  after all; do not leave 8 ids exempt indefinitely.
- **Two rebuilds, not one.** C2 cannot ride rebuild #1 (its scripts do not exist
  yet), so the plan now costs ~460 MB of LFS twice. Batch C1 and C2 into a single
  rebuild #2 — the moment they are split per paper, it is 11 rebuilds.
- **Pool saturation after C2.** 8 rerolls consume 168 `listening_scenarios` and 88
  `quick_response` entries. The draws fit today with no relaxation (§5C.3), but the
  pools sit near-saturated afterwards, so the *next* few papers are the ones that
  will hit a relaxed cooldown. Re-run `--check-depth` before Phase 6, and treat a
  relaxation warning as a signal to unpark the pool-growth tooling.
- **Stale learner records on repaired papers** — `ユーザー解答.json` / `採点結果.json`
  survive a repair and silently score items that no longer exist (§5D). `localStorage`
  copies in the Pages build cannot be cleared repo-side at all.
