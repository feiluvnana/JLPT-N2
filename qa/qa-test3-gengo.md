# TEST 3 GENGO/DOKKAI: FAIL (31 findings, 22 automatic)

Reviewer: fresh-eyes QA, `exam-qa-review` steps 1, 2, 2b, 2.5, 3, 6 (gengo part).
Scope: the 71 items of `tests/3/言語知識・読解.md` only.
Skills read in full before the first tool call: `.agents/exam-qa-review/SKILL.md`,
`.agents/question-authoring/SKILL.md`.

---

## 2. Blind-solve diff

I answered all 71 items from `tests/3/言語知識・読解.md` lines 1–537 (the document
truncated immediately before `# 解答(言語知識・読解)` at line 538), then read the key
tables. **67 / 71 matched.** Four mismatches:

| Item | Mine | Key | Resolution |
|---|---|---|---|
| 18 | 1 トナー | 4 インキ | **FINDING F8.** Not reviewer error. `大型印刷機の(　)が切れてしまったため、新しいボトルを交換した。` — トナー切れ and トナーボトル are the standard collocations for a large office printer/copier; インキ切れ is the standard one for a press. The stem's own word 「ボトル」 points at トナーボトル at least as strongly. Two defensible answers. |
| 36 | 3 に先立って | 2 とともに | **FINDING F6.** Not reviewer error. A's turn fixes the expansion in the future (「いよいよ来月からですね」), so 「事業の拡大に先立って、新たな専門人材の確保が急務となっています」 is natural and arguably better motivated than 「拡大とともに」. 〜に先立って is an N2 headed form (`question-authoring` 問題7-9 list), i.e. a same-band competitor that must be impossible and is not. |
| 44 | 1 周辺地域の | 2 交通網を麻痺させた | **FINDING F3.** Reviewer's first ordering (3-4-1-2) is indeed bad — 「麻痺させた経済活動全般」 misparses. But 1-2-3-4 is fully natural: 「今度の台風は、周辺地域の交通網を麻痺させた激しい風雨をもたらしたばかりか、経済活動全般にも大きな打撃を与えた。」 ★ = option **3**. Two ★ answers, not one. |
| 46 | 3 実際に使われる | 1 触れるほど | **FINDING F4.** Key order 3-2-1-4 yields 「実際に使われる多くの文章に触れれば触れるほど…」; order 2-1-3-4 yields 「多くの文章に触れれば触れるほど、実際に使われる表現の幅が広がり…」 — grammatical, natural, and the commoner collocation (実際に使われる**表現** ≫ 実際に使われる**文章**). Two ★ answers. |

The blind solve also surfaced items where I hit the key but only by guessing (20:
all four garments fit; 30, 42, 17: the key and a distractor both work). Those are
filed below.

`make check`'s 解説-quote WARN, adjudicated: **the QUOTE is wrong, the ITEM is
right.** 解説 66 writes 「過去の情熱や初心を思い起こさせ…」; passage A line 432
says 「忘れていた**当時の**情熱や初心を思い起こさせ…」. Key 2 is correct on the
passage as written; the 「」 span is a paraphrase and must be re-pasted (F24).

---

## 3. Findings table

`AUTO` = on the `exam-qa-review` automatic-fail list; any one fails the paper.

| # | Item(s) | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| F1 | 31 | **AUTO** unanswerable / broken Japanese | Stem: 「どうも風邪(　)**だから**今日は…」 with options `がちだ / っぽい / 気味だ / 勝ちだ`. Key 3 splices to 「風邪気味**だだ**から」. Options 1 and 4 do the same; option 2 gives 「風邪っぽい**だ**から」. **No option produces a grammatical sentence.** | Cut the stem's だ (「風邪(　)から」) or strip だ from options 1/3/4. Keep key on slot 3. |
| F2 | 20 | **AUTO** ≥2 defensible answers | 「夏らしい爽やかな素材で作られた青い(　)を着て現れた。」 vs `スーツ/ブラウス/ワンピース/ジャケット`. All four are summer-weight blue garments one 着る. Nothing in the stem discriminates — this is a **4-way** ambiguity. | Add a discriminator that only ワンピース satisfies (e.g. 「上下がつながった」 / a hem-length or 一枚で着られる cue). |
| F3 | 44 | **AUTO** two ★ answers | See diff above: 1-2-3-4 ★=3 vs key 3-4-2-1 ★=2, both natural. | Lock the order: make 周辺地域の bind to 交通網 only (e.g. replace 「激しい風雨をもたらした」 with a te-form 「激しい風雨をもたらし」 so it cannot head a relative clause). |
| F4 | 46 | **AUTO** two ★ answers | See diff above: 2-1-3-4 ★=3 vs key 3-2-1-4 ★=1. | 「実際に使われる」 is the floating modifier — bind it (「実際に使われている表現に」 inside option 4) or replace it. |
| F5 | 66 | **AUTO** broken Japanese inside the KEYED option | Line 451, option 2 (the key): 「Aは過去の曲から**活力得る**ことを肯定し…」 — particle を missing. | 「活力**を**得ること」. |
| F6 | 36 | **AUTO** ≥2 defensible answers | See diff. とともに (key) and に先立って both fit the dialogue. | Rewrite the B turn so the personnel need is *concurrent with* growth, not prior to it (e.g. 「事業の拡大(　)、社員数も年々増えています」), which kills に先立って. |
| F7 | 42 | **AUTO** ≥2 defensible answers | 「疲れからか仕事の効率が下がり(　)。」 — 下がり**ぎみだ** (key) and 下がり**がちだ** are both natural, both ALLOW-band (`level_band_grammar.txt` lines 119–120). | Replace distractor 4 がちだ with a form the 連用形 frame rejects. (Also see F19 — がちだ cannot stay anyway.) |
| F8 | 18 | **AUTO** ≥2 defensible answers + **AUTO** 2b | See diff. Additionally `ペンキ`/`ニス` are **paint-domain** nouns beside two printing-consumable nouns — they die on sight, so the item is a 2-way coin flip between the two real competitors. | Name the machine unambiguously (「輪転印刷機」/「オフセット印刷機」 → インキ) and replace ペンキ/ニス with printing consumables (`トナー`, `インクリボン`, `感光ドラム`). |
| F9 | 17 | **AUTO** ≥2 defensible answers | 「その国は今まさに経済発展の(　)にあり」 — 途上 (key) and 過程 are both standard (`発展の過程にある` is ordinary Japanese); 途中 is defensible too. | Move the key onto its locked collocation (「発展(　)国への支援」) or replace 過程/途中. Note 過程 is also the 問題2-7 key — see F29. |
| F10 | 30 | **AUTO** two correct sentences | Option 3 「彼は**性格がふわふわしている**ので…」 uses an **attested** collocation (ふわふわした性格 = flighty). Only the consequence clause is odd, not the word use — so the item has two usable sentences. This is the 「契約を解消」 class named in `question-authoring` 問題6. | Rewrite option 3 to break the collocation, not the logic (e.g. put ふわふわ on a hard/solid object). |
| F11 | 1 | **AUTO** off-level / invalid key (step 2.5) | Key 軍 = **いくさ**. 常用漢字表 gives 軍 the reading **グン only** — いくさ is a 表外訓 (the joyo spelling of いくさ is 戦). JLPT never keys a 表外読み. The stem 「大きな軍があった」 is itself archaic for 「大きな戦があった」. | Replace the whole item; the pool entry `軍(いくさ)` should be pulled from `pools.json.kanji_reading`. |
| F12 | 1, 2, 4 | **AUTO** 2b — distractors from unrelated kanji | 1: いさお=功/勲, いのち=命, いかり=怒り — nothing shares a component with 軍. 2: たまわる=賜る, たたえる=称える — nothing shares 尋. 4: たしかめる=確かめる, とがめる=咎める, とどめる=留める — nothing shares 改. This is exactly the いたわる/ことわる/さわる/かわる shape §2b names. | Rebuild each distractor as a reading of the target kanji or a same-radical kanji, and write the source line (F25). |
| F13 | 2 | **AUTO** 2b — okurigana giveaway | Printed form 尋**ねる**. Only たず**ねる** and たば**ねる** fit 〜ねる; たまわる and たたえる are ruled out by the visible okurigana without reading the kanji. The item is a 2-way choice. | Give all four options the 〜ねる class, or use the dictionary form of a verb whose okurigana does not select. |
| F14 | 16, 19 | **AUTO** 2b — no shared functional category | 16: ようやく(完了副詞)/いきなり(突発副詞)/あいにく(残念副詞)/おおかた(推量副詞) — four categories; あいにく is the exact 「まして vs あいにく/徐々に/たまたま」 example already printed in `question-authoring`. 19: **かげむ is not a Japanese word** (陰る=かげる); たたむ is in an unrelated domain. Only はずむ competes. | 16: four 突発・即時副詞 (いきなり/突然/にわかに/だしぬけに). 19: four intransitive 意欲/勢い verbs (しぼむ/そがれる/衰える/失せる). |
| F15 | 26, 27, 29 | **AUTO** 2b — domain-violation distractors | 26: 「ベテラン**な挨拶**」「ベテラン**な味**」「今日の天気は**ベテラン**で」 — all three leave the person-noun domain entirely and die on sight; the item tests nothing. 27: 「不具合を普及する」(repair domain), 「元の状態に普及させる」(restoration domain). 29: 「運動を**あふれる**ことで」 uses an intransitive verb transitively (word salad); 「シュレッダーにかけることで**あふれさせた**」 is nonsense. | Apply the `question-authoring` 解消 procedure: write a sentence where the word is correct, then break exactly one thing **inside its own domain**. 26 needs three sentences about experienced people/skills. |
| F16 | 11, 12, 13 | **AUTO** 2b — non-productive affixes | 12: 〜難い attaches to verb 連用形, never to 人 (人難い); 人迷い is not a formation at all — both die on morphology, leaving only 避け. 13: 違〜 and 標〜 are not productive prefixes; only 別〜 competes with 異〜. 11: 食べ好き is not a formation. `question-authoring` 問題3: options must be affixes that could plausibly attach to **this** stem. | Replace with real competitors: 12 → 人**見知り**/人**慣れ**/人**嫌い**/人**任せ**-type suffix set; 13 → 異/別/他/各 (all real noun prefixes). |
| F17 | 48, 50 | **AUTO** 問題9 category collision | 48 (「非常に(　)手段」) and 50 (a whole clause) are **both 内容推論** — neither is decidable from its local sentence alone. 49 is 論理接続, 51 is 文末モーダル; **no 慣用・形式名詞 blank exists**. `question-authoring` names this exact pair: 「t3 48/50」. Distinct from the already-filed missing tags — the collision survives even after tags are added. | Rewrite 48 as a 慣用/形式名詞 blank (つもり, 元も子もない, 〜わけ…) and tag all four. |
| F18 | 問題10(1), 11(2), 11(3), 11(4), 12, 13 | **AUTO** topic repeated inside the paper (step 5) | **マイボトル twice**: 問題11(3) 「マイボトル持参キャンペーン」 (専用給水機 + 「1杯につき50円の割引」) and 問題13 「マイボトルの持参」 (「給水スポット」 + 「ドリンク代金の割引サービス」) — same subject, same two decisive details, in one paper. **食品ロス twice**: 問題10(1) 食品ロス削減 and 問題11(4) フードバンク連携による食品ロス削減. **記憶 twice**: 問題11(2) 味覚が記憶を呼び覚ます and 問題12 音楽が記憶を呼び覚ます (both cite the emotion/memory brain link). | Replace 問題11(3) and one of 問題11(2)/問題12. Root cause is upstream — see RC7. |
| F19 | 31 + 42 | **AUTO** one grammar point keyed twice | 31 keys 「気味だ」, 42 keys 「ぎみだ」 — the same point in two spellings. `logs/test_spec.json` `grammar_p7` itself lists both (`"〜気味"` and `"〜ぎみだ"`), and `logs/ledger.json` recorded the same draw, so this originated in the sampler, not in authoring. | Re-roll one of the two 問題7 slots; fix `sample_items.py` (RC8). |
| F20 | 40 + 5/問題9/問題10(4); 27 + 40 | **AUTO** tested form modeled elsewhere in the paper | Item 40 keys 〜に伴って, while **〜に伴い** appears unglossed three times in the same booklet: item 5's own stem (「景気の急激な悪化に伴い」, l.25), the 問題9 cloze passage (「高齢化に伴い」, l.211) and 問題10(4) (「デジタルツールの普及に伴い」, l.286). Likewise 普及 is the 問題6-27 **tested word** and item 40's stem prints 「インターネットの急速な普及」 — nearly item 27's correct sentence (「スマートフォンが急速に普及した」), so 27 is answerable from 40's stem. `question-authoring`: 「keep a tested form out of the reading passages too」. | Swap the running-text instances to 〜につれて/〜とともに and rewrite item 40's carrier off 普及. |
| F21 | 57, 59, 63 | **AUTO** banned pure-retrieval 問題11 stem — **gate missed these** | 57 「スマート農業の導入によって得られる利点として、**文章で述べられているものはどれか**」, 63 (identical shape), 59 「**文章で説明されているものはどれか**」. `tools/check_consistency.py:855` `P11_BANNED_STEM = re.compile(r"本文で述べられて|…")` anchors on **本文**; this paper writes **文章**, so three of the four banned-shape stems slipped past. None of the three names 筆者 (筆者-less stems: 5 of 8, matching the figure `question-authoring` records for t3). | Rewrite as 筆者-anchored stems; fix the regex (RC6). |
| F22 | 71 | **AUTO** 問題14 single-constraint item / wrong item shape | 「このキャンペーンの条件について、**説明と合っているものはどれか**」, key 1 = 「市外在住者の利用も還元対象」 — one cell, no scenario. `question-authoring`: 「70 and 71 are **both** person-scenario items; 71 may never be a content-match question」, and it names t3's 71 as the shipped example. The gate only counts 解説 quotes, so the stem shape is unchecked. | Rewrite 71 as a second applicant whose plan fails exactly one condition (e.g. a 市外在住者 buying at a mall chain store, or a shared-cycle 月額 contract). |
| F23 | 29 | minor — kanji misuse in the KEYED sentence | Option 2 (key): 「堤防を**超えて**あふれ出した」. Water passing over an embankment is 越える; 超える is for exceeding a quantity. `question-authoring`: 「the correct sentence must be flawless」. | 「堤防を**越えて**」. |
| F24 | 66, 52 | minor — 解説 quotes not verbatim | 66: 「過去の情熱や初心を…」 vs passage 「忘れていた**当時の**情熱や初心を…」 (this is the `make check` WARN; item is right, quote is wrong). 52: 「使いきれる分だけを買うことを徹底し」 and 「古いものから順に消費する習慣」 drop the passage's inner 「」 (「『使いきれる分だけを買う』ことを徹底し」). | Re-paste both spans from the passage. |
| F25 | all of 1–30 | minor (blocking artifact) — mandatory key-note lines absent | `## 文字・語彙` (lines 540–551) contains the answer grid **and nothing else**. `question-authoring` §0 requires, for **every** 問1–6 item, a functional-category line (`24: 程度副詞 ×4 (…)`) and, for 問1, the distractor-source line (`いたわる=労わる, …`). 30 required lines, 0 present. Writing them is what would have exposed F12/F14/F15/F16 at authoring time. | Add all 30 lines; gate their presence (RC5). |
| F26 | 問題10(3),(4), 11(1),(3), 13 | minor — wrong-band / circular glosses **beyond** the ones the gate flagged | Additional to 便箋/割引/蘇る/責務/洗髪: **規制**(「ルールを設けて行動を制限すること」), **増幅**, **革新**(「古い仕組みを改めて**新**しくすること」), **省力化**(「手間や**労力**を減らすこと」), **再評価**(「**価値**を改めて見直すこと」), **環境負荷**(「**環境**に与える悪影響や負担」 — the definition repeats the term), **継承者**(「事業や技術を受け**継ぐ**人」), **風土**, **途絶**(「**途**中で**途**切れて…」), **契機**(「きっかけ。」). All ten are absent from `vocab-n2.json`, so the gate's WARN cannot see them — but absence is not proof of over-level (`question-authoring`: 「Both conditions are necessary, neither is sufficient」). **契機 additionally contradicts the paper itself**: it is glossed as over-level in 問題13 yet printed bare as a 問題7-36 option (「を契機に」). Same for 割引: glossed in 問題11(3), bare in 問題13 and in item 68's option. | Delete these ten glosses. The in-body marker count then drops from 29 to ~19 — still above the 15 floor. |
| F27 | 43, 45, 47 | minor — second natural ordering (★ unaffected) | 43: 1-2-3-4 and 2-1-3-4 both read naturally (聴衆に対して is a floating adjunct). 45: 1-2-4-3 and 2-1-4-3 both natural (将来にわたって floats). 47: 2-1-4-3 is a weaker but available alternative. In all three the alternative keeps ★ on the same option, so no key ambiguity — but `question-authoring` 問題8 requires exactly ONE natural ordering. | Position-lock the floating adjunct in each (bind it with a particle to a fixed neighbour). |
| F28 | 48, 50, 51 | minor — cloze options separable by polarity alone | 48: key 現実的な vs 無理な/抽象的な/一時的な (all negative). 50: key is the only affirming clause among three warnings. 51: key に違いない vs にすぎない/わけがない/はずがない (all negative). Three of four blanks are solvable by sign-matching the surrounding sentence, without tracking the argument. | Give at least two blanks a same-polarity distractor set. |
| F29 | 9, 24, 28; 17/7 | minor — level spot-checks (step 2.5) | 下車 (問題2-9) and まあまあ (問題6-28) are N4/N3-band vocabulary; わずかに (問題5-24) is low N2 and 問題5 is supposed to carry the HARD word in the stem. Separately, 過程 is the key of 問題2-7 and reappears as a 問題4-17 option — the paper prints the word as correct, then requires rejecting it. | Re-roll 9 and 28 toward N2; move 過程 off the 17 option list. |
| F30 | spec | minor — spec ↔ pool drift | `test_spec.items.grammar_p8` contains `"相対比較(〜ば〜ほど)"` and `grammar_p7` contains `"〜気味"`; **neither string exists in `pools.json`** for that category today (〜気味 lives in `word_formation`; there is no ば〜ほど entry at all). The ledger shows the same draw, so the sampler emitted them. ば〜ほど is on the TOO_EASY list — the already-filed 問題8-46 level failure originates here, not in authoring. | Assert spec ⊆ pool in the gate (RC14). |
| F31 | 問題11(3) | minor — wrong genre for 中文 | 問題11(3) is 「【社内連絡】マイボトル持参キャンペーンの開始について … 環境推進委員会」 — a notice, not signed opinion prose. That is *why* its two stems (61, 62) can only ask retrieval (the already-filed defect): a notice has no 筆者 to ask about. It also duplicates the register of 問題10(1) 「【社内通知】… 総務部環境推進課」, so the paper prints two internal announcements from an environment committee. | Replace the passage with an essay; the fix for the filed 61/62 finding is a new passage, not reworded stems. |

**Already-filed by `make check`, not re-filed here** (checked as present, no false
positives found): 読解 length floors 問題11/問題14; the two pure-retrieval stems 61/62;
問題11(3) retrieval-only pair; the 67/68/69 length-findable keys; 問題14 解説 quoting
one cell; the missing 問題9 category tags; 問題8 〜ば〜ほど TOO_EASY; glossed-but-standard
便箋/割引/蘇る; circular 責務/洗髪.

**Resolved, previously shipped, verified gone:** the 問題14 「補助スタッフ」 invented
role (the flyer is now a 地域電子通貨 campaign; every detail items 70/71 reference —
大手チェーン店, コンビニ, 月額定額プラン, 市外在住者, 有効期限 — is printed in the
flyer). Also gone: the 問題9 Latin-script 「contrast」 (no Latin run ≥2 chars anywhere
in the file); the 問題8 stem/option word duplication (all five assembled sentences
splice clean, no word twice); the 問題11 orphaned glosses (注 markers and definitions
pair 1-to-1 in every passage, both directions).

---

## 4. Root-cause table (step 6.5)

Grouped: rows sharing one cause are one skill defect.

| RC | Findings | Code | Tests on disk showing the class | Owning file | Concrete edit |
|---|---|---|---|---|---|
| RC1 | F6, F7, F8, F9, F10, F2 | `RULE-UNENFORCEABLE` | 4/4 (t1 難航/停滞, t2 超満員, t3 問題9-52, t4 に即して/未記入/おろそか) | `question-authoring` + `tools/check_consistency.py` | The 「name the reason each distractor is IMPOSSIBLE」 rule has **no artifact** outside 問1–6. Extend §0's artifact table: every **問題4, 問題5, 問題7** row's 解説 cell must carry three `N ✗ …理由` clauses, one per wrong option. Add `check_distractor_reasons()`: FAIL when a 問題4/5/7 解説 cell contains fewer than three `✗` clauses. A written reason for 「3 に先立って」 on item 36 could not have been produced. |
| RC2 | F3, F4, F27 | `RULE-UNENFORCEABLE` | 3/4 (t2, t3, t4 each shipped one two-★ item) | `question-authoring` 問題8 | 「actively try to permute every option into every other slot」 is a thought with no output. Require a second 解説 line per 問題8 row: `別順序不可：(1)(2)入替→「…」不自然` naming the rejected permutation. Gate: FAIL a 問題8 解説 cell with no `別順序不可` line. |
| RC3 | F1 | `GATE-BLIND` | 1/4 (new class) | `tools/check_consistency.py` | Nothing ever splices a 問題7 stem with its keyed option. Add `check_mondai7_splice()`: substitute the keyed option into `(　)` and FAIL on `だだ`, `だで`, い-adjective + `だ`, or a doubled particle at the join. String-decidable, and it catches exactly the printed 「風邪気味だだから」. |
| RC4 | F5, F23 | `RULE-IGNORED` + `GATE-BLIND` | 2/4 (t4 shipped six broken sentences, several inside correct options) | process; partially `tools/check_consistency.py` | The 「read the whole paper aloud」 pass demonstrably did not run on the key tables' own options. Particle omission is not mechanizable, but two narrow checks are: (a) WARN on a 読解 option containing a 2+-kanji noun immediately followed by a verb with no particle where the same noun+を/が appears elsewhere in the paper; (b) FAIL on 「堤防を超え/ハードルを超え」-class 越/超 confusions from a small confusion list. Otherwise state it as human judgment and make the authoring pass report per-section read-aloud confirmation. |
| RC5 | F25 → F12, F13, F14, F15, F16 | `GATE-BLIND` | 4/4 (the category-line rule was written *because* t1–t4 all skipped it) | `tools/check_consistency.py` | **Highest-value single edit.** The artifact is mandated by `question-authoring` §0 and nothing verifies it exists. Add `check_goi_category_lines()`: FAIL when `## 文字・語彙` lacks a line matching `^\s*(\d+):\s*\S+\s*×4\s*\(` for each of items 1–30, and for 問1 items additionally `\w+=\S+`. Five separate 2b failures in this paper (F12/F13/F14/F15/F16) are all downstream of that one unwritten line. |
| RC6 | F21 | `GATE-WRONG` | ≥1 here; **re-verify t1, t2, t4** | `tools/check_consistency.py:855` | `P11_BANNED_STEM = re.compile(r"本文で述べられて\|として正しいもの\|主な目的は\|内容と合っている")` matches only 本文. Change to `r"(?:本文|文章|この文章)で(?:述べられて|説明されて)\|として正しいもの\|主な目的は\|(?:内容|説明)と合っている"`. Green was never evidence for stems written with 文章 — this is the classic GATE-WRONG shape. |
| RC7 | F18, and the spec half of it | `GATE-WRONG` | 4/4 for cross-surface repetition | `tools/check_consistency.py` + `merge_seeds.py` (`web-topic-research`) | The blend contract's 「every surface gets a distinct topic」 compares **exact strings**, so `logs/test_spec.json` shipped 「社内でのマイボトル持参キャンペーン告知」 (#8) beside 「マイボトル持参による使い捨て容器の削減」 (#11), 「家庭での食べきり…」 (#1) beside 「…フードバンク連携による食品ロス削減」 (#9), and 「スマート農業におけるロボット農機の導入」 (#6) beside 「スマート農業と担い手」 (#12) — 12 topics for 11 surfaces, so pool topic #12 was **starved** and the paper duly wrote each duplicate twice. Fix: compare topics on shared distinctive tokens (≥3-char kanji/katakana runs, stop-listing 地域/社会/日本…) and FAIL on any shared token across two topics; make `merge_seeds.py` reject a harvest that produces one. |
| RC8 | F19 | `GATE-BLIND` / `PIPELINE-GAP` | 2/4 (t4-removed's draw also carried 〜気味 in `grammar_p7`) | `item-pool-sampling/scripts/sample_items.py` + `tools/check_consistency.py` | The gate folds spellings **inside `pools.json` per category** but never inside a single draw, and 〜気味 reaches `grammar_p7` from a different pool category than 〜ぎみだ, so the fold never compares them. Fix: apply the existing normalizer (kanji tail → kana, drop trailing だ) across the **whole `items` block** of a draw and reject/re-roll on collision; add the same assertion over `logs/test_spec.json` in the gate. |
| RC9 | F20 | `GATE-BLIND` | ≥2/4 (t4 shipped 〜にともなって twice and 「時代に即した」 beside the に即して key) | `tools/check_consistency.py` | Fully string-decidable and unchecked. Add `check_tested_form_leakage()`: for each 問題7/8/9 keyed form (kana-folded, particle-stripped) and each 問題6 target word, search all passage/stem prose outside its own item; FAIL on a hit. Would have caught 〜に伴い ×3 and 普及 ×4 in seconds. |
| RC10 | F26 | `GATE-WRONG` | 4/4 (t1 鑑賞/評価制度, t2 質感/バランス, t3 these ten, t4 準備) | `question-authoring` + `tools/check_consistency.py` | The WARN tests membership in a 1793-entry slice, which by `question-authoring`'s own text cannot decide the class — so it reports 3 of 15 wrong-band glosses and trains the reader to shrug. Convert the judgment into an artifact, exactly as the 問題9 tags were: **every 注 definition line must open with a category tag** — `[N1・稀語]` `[専門語]` `[比喩]` `[口語]` — and `make check` FAILs on an untagged gloss. An author who has to type `[専門語]` in front of 「割引：決められた価格から一定の金額を引くこと」 will not write the gloss. |
| RC11 | F22 | `GATE-BLIND` | 3/4 (t2, t3, t4 all put a content-match question on 71) | `tools/check_consistency.py` | `check_mondai14_quotes()` counts 解説 quotes but never reads the stem, so a reworded content-match stem (「説明と合っているものはどれか」 instead of 「このお知らせの内容と合っているものはどれか」) passes. Add: FAIL when the 問題14 stem for **71** matches `(内容|説明|条件)と?合っている|条件について` or does not name a person/plan (`さん(は|が)`). |
| RC12 | F17 | `RULE-UNENFORCEABLE` (already partly gated) | 4/4 | `question-authoring` (no change) + gate | The four-tag FAIL is already specified; once tags land, extend the same check to assert the four tags are **distinct** *and* that the four blanks' option shapes differ (one full-clause blank, one sentence-initial connective, one sentence-final modal, one set phrase). Tag distinctness alone would not have caught 48/50, since 48 could be tagged 慣用 dishonestly. |
| RC13 | F31 | `RULE-MISSING` | 2/4 (t3 here; t2's 問題11(2)) | `question-authoring` 問題11 section | Nothing states what a 中文 passage *is*. Add one sentence: 「問題11の4本はすべて署名のある論説・エッセイ体で書く。掲示・社内連絡・メール・チラシは問題10か問題14にのみ置く」, plus gate: FAIL a 問題11 passage containing 【社内連絡】/【お知らせ】/【件名】/全社員の皆様へ. This is upstream of the filed 「(3) asks only retrieval」 finding — a notice cannot be given a 筆者 stem. |
| RC14 | F30 | `PIPELINE-GAP` | ≥2/4 | `tools/check_consistency.py` | Add: every non-`adjunct` entry of `logs/test_spec.json["items"][cat]` must be present in `pools.json[cat]`, else FAIL. Off-pool items (here `相対比較(〜ば〜ほど)`, a TOO_EASY form) currently reach the author with pool authority. |
| RC15 | F11, F29 | `GATE-BLIND` | 1–2/4 | `tools/check_consistency.py` + `pools.json` | Nothing checks a `kanji_reading` pool entry's reading against the joyo table. Add a check of each `kanji_reading` entry against `openjlpt/kanji-n2.json` readings (or the joyo list) and FAIL on a 表外訓 such as `軍(いくさ)`; remove that entry from the pool. |

**Blocking note (`exam-qa-review` §6.5).** RC1–RC3, RC5–RC11, RC13–RC15 are
`RULE-MISSING` / `RULE-UNENFORCEABLE` / `GATE-BLIND` / `GATE-WRONG` / `PIPELINE-GAP`
and therefore **block the next generation run** until applied or explicitly rejected.
RC6 additionally requires re-verifying tests 1, 2 and 4, whose 問題11 stems were
cleared by the mis-anchored regex.

---

## 5. Coverage statement

Files read: `tests/3/言語知識・読解.md` (all 602 lines — body 1–537 first, keys 538–602
only afterwards), `logs/test_spec.json`, `logs/ledger.json`,
`.agents/item-pool-sampling/references/pools.json`,
`.agents/item-pool-sampling/references/openjlpt/vocab-n2.json`,
`.agents/exam-qa-review/references/level_band_grammar.txt`,
`tools/check_consistency.py` (問題11/問題14 checks), and — for the copy check —
`tests/imported-n2-2025-07/`, `tests/1/`, `tests/2/`, `tests/4/言語知識・読解.md`.

**Steps run on all 71 items:** 1 (key-by-key proof), 2 (two-answer hunt, one
impossibility statement per wrong option), 2b (functional category per option for
問1/3/4/5/6), 2.5 (level band on every 問題7–9 key + spot-checks on 問1–6), 3 (all
mechanical reads), 6 gengo part (target items + answer positions).

**Measurements (JP chars, kana/kanji/JP punctuation only):**

- **問題7 stems** (12): 40, 36, 43, 44, 39, **60**, **59**, 44, 39, 44, **69**, 36 —
  **average 46.1**, minimum 36, none under 30. Official band ~43 avg / 33–54 IQR: **pass**.
  Dialogue-or-setting stems: **3** (36 （会社で）, 37 （電話で）, 41 （オフィスで）), all
  in the multi-line layout `question-authoring` prescribes. Requirement ≥2: **pass**.
- **問題8**: option-sum 24 / 29 / 28 / 30 / 34 (band 16–29, three slightly over — fine);
  assembled sentence 49 / 53 / 63 / 56 / 62, all ≥45: **pass**. ≥2 options ≥5 chars and
  longest ≥7 in every item: **pass**. No word appears twice in any spliced sentence: **pass**.
- **問題9 cloze body**: **721** JP chars (band ~500–700; marginally over, not a defect).
  Blank categories as authored: 48 内容推論 / 49 論理接続 / 50 内容推論 / 51 文末モーダル →
  **collision, see F17**; at least one whole-passage blank exists (50): pass.
- **読解 passage prose** (excluding 注 definition lines, stems and options — a stricter
  metric than the gate's, which is why my numbers sit below the gate's):
  問題10 **1282** (per passage 292 / 237 / 214 / 232 / 261, all ≥200 ✓);
  問題11 **1780** (537 / 416 / 389 / 392 — (3) and (4) sit below the 400 per-passage floor
  on this metric; the section total is already filed as short);
  問題12 **555** (A 258 / B 252); 問題13 **1130**; 問題14 flyer **568**.
- **`（注N）` apparatus**: 58 total occurrences = **29 in-body markers + 29 definition
  lines**. In-body count 29 vs the ≥15 bar: **pass on count**, but see F26 — ten of the 29
  are wrong-band, i.e. the count was reached the way `question-authoring` explicitly warns
  against. Pairing is 1-to-1 in **every** passage in both directions (no orphan marker, no
  orphan definition). `（中略）` present **once**, inside 問題11(1)'s passage body: **pass**.
- **Formatting**: zero `<ruby>`; zero `①/②` numbered markers (so no orphan-marker risk);
  zero Latin runs ≥2 characters anywhere in the file.
- **Spec conformance (step 6)**: all **71** answer positions match
  `test_spec.answer_positions` exactly (問題1 `[1,1,2,4,3]` … 問題14 `[2,1]`). All 問1–8
  target items match `test_spec.items` exactly — 軍(いくさ)/尋ねる/副/改/縮小, 解答/過程/
  就職/下車/為替, 〜放題/〜嫌い/異〜, ジャーナリスト/アクセント/いきなり/途上/インキ/
  しぼむ/ワンピース(adjunct), 愚かだ/ゼミ/テンポ/わずかに/どっと, ベテラン/普及/まあまあ/
  あふれる/ふわふわ, the twelve 問題7 forms, the five 問題8 frames. **No author
  substitution.** The defects at items 1, 20, 42 and 46 originate in the *spec*
  (F11, F19, F30), not in a swap.
- **Copy check**: longest shared content n-gram with `imported-n2-2025-07` and with tests
  1/2/4, after stripping headings and instruction lines, is the file-header boilerplate
  (「時間: 105分 問題数: 71問…」, shared by all generated tests) plus one shared stem
  template 「…について、文章の内容と合っているものはどれか」 (item 55, also in test 4).
  **No passage, stem, option or 例 is copied** from the official paper or from another test.

**`make check` WARNs, adjudicated:** the one WARN I was asked to resolve — the 解説 quote
「過去の情熱や初心を思い起こさせ…」 — is a **true positive**: the quote is a paraphrase
(passage says 「忘れていた当時の…」) and the key is nonetheless correct (F24). I found no
false positive among the pre-filed gate findings; I did find that the gate **under**-reports
three classes (RC6 問題11 stems, RC10 glosses, RC11 問題14 stem shape).

---

## 6. Skips

- **聴解 (30 items, `聴解.md` / `聴解スクリプト.txt` / MP3 / chapters)** — out of scope by
  assignment; another reviewer covers it. Two cross-half observations handed over rather
  than adjudicated: (a) `test_spec.listening_scenarios` contains 「駅での傘シェアリング
  サービスの拡大」, 「自転車シェアリングのポート間貸出・返却」 and 「シェアサイクル利用時の
  ヘルメット着用促進」 while the 問題14 flyer's category C prints 「市内シェアサイクル、
  駅前傘シェアサービス」 and item 70's option 3 turns on the シェアサイクル 月額定額プラン —
  `exam-qa-review` step 5 forbids the flyer sharing a decisive detail with a listening item;
  (b) three listening seeds are shared-mobility topics, which the listening reviewer should
  check against its own repetition rule.
- **Cross-test topic table and provenance/harvest audit (step 5 across tests, step 6.3–6.5)**
  — assigned to another reviewer. I checked repetition **within** this paper only (F18) and
  reported the spec-level duplication that produced it (RC7) because it is a gate defect, not
  a topic verdict. No `logs/seeds.json` URL was fetched.
- **`refs/Shinkanzen/*.pdf` TOC cross-check for step 2.5's hard side** — not opened; every
  問題7–9 key resolved against `references/level_band_grammar.txt` (all twelve 問題7 keys are
  ALLOW-band or unlisted-N2; 気味/ぎみ and がち are explicitly ALLOW, so F19 is a duplication
  defect, not a band defect). The one band failure I raise (F11, 軍=いくさ) is decided by the
  常用漢字表 reading set, not by Shin Kanzen.
- **No file was edited.** This is a review; every fix above is a proposal for the fixing pass.
