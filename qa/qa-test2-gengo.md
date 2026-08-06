# TEST 2 GENGO/DOKKAI: FAIL (28 findings, 11 automatic)

Reviewer: fresh-eyes QA, authored nothing in this paper. Skills read in full before
any other tool call: `.agents/exam-qa-review/SKILL.md`, `.agents/question-authoring/SKILL.md`.
Scope: the 71 items of `tests/2/言語知識・読解.md` only. No file was edited.

**Entry-condition note (M15):** `exam-qa-review` requires `make check` green before QA
starts. It is **RED** — `FAILED — 43 problem(s)`, `15 warning(s)`, of which 9 FAILs and
1 WARN are on test 2. QA was run anyway per instruction; the verdict below assumes the
pre-filed gate list is being repaired in parallel.

---

## 1. Blind-solve diff

Solved items 1–71 from the body only (lines 1–492, key section at line 493 unread), then
diffed against the key tables.

**Mismatches: ZERO. 71/71 agreement.**

That is not a pass signal, it is finding **F-DOKKAI-EASY (A10)** below: a hostile reader
who has never seen the paper should not go 71/71, and on the 読解 half I did not need the
passages. The only item where I could not derive an answer from the printed material at
all was **12**, where I picked 4 by elimination of the impossible rather than by reading
the stem (see A1) — the key agrees, which proves the item was keyed to a stem that is not
on the page.

Two items I answered with reservations, both filed rather than resolved as reviewer error:

| Item | My answer | Key | Resolution |
|---|---|---|---|
| 12 | 4 (guessed from the ledger-visible intent 怖がる) | 4 | **Not reviewer error** — the stem prints no word for the affix to attach to. Filed as A1. |
| 13 | 1 | 1 | **Not reviewer error** — 2「全」 is equally defensible. Filed as A2. |

---

## 2. Findings table

Automatic-fail rows are marked **A**; the rest are moderate/minor (**M**).

| # | Item | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| **A1** | 問題3-12 | unanswerable item / broken Japanese | Stem: 「妹は子供のころ、暗い場所を極端に(　)性格だった。」 All four options (ぶった／づいた／ばんだ／がった) are **bound suffixes**; the stem prints no host word. Key 4 assembles to 「暗い場所を極端に**がった**性格だった」. `logs/ledger.json` test 2 `word_formation` names the target as 「〜がる(怖がる)」 — the host 怖 was dropped in drafting. | Restore the host: 「暗い場所を極端に**怖**(　)性格だった」→ がった. Then re-verify ぶった／づいた／ばんだ each attach to 怖 and fail on collocation. |
| **A2** | 問題3-13 | second defensible answer | Stem 「今年度の(　)人口に関する統計データが公表された」; key 1 総. Option 2 全 gives 全人口, which is standard statistical register — 総務省統計局『人口推計』: 「人口推計の範囲は，我が国に常住している**全人口**（外国人を含む。）である」. Both fit the frame and the register. | Replace 全 with a prefix that cannot take 人口 (e.g. 過／副／被), or move the item to a stem where 全 is blocked. |
| **A3** | 問題8-45 | broken Japanese (問題8 glue) | Assembled: 「…信頼できる経験豊富な仲間との十分な協力でなければ到底**どんな大きな困難を乗り越えることはできない**。」 `どんな+N` under negation requires も/でも (どんな大きな困難**も**…できない). The break is at the join between option 4 and the stem's fixed tail — exactly the glue-check class. | Change the fixed tail to 「困難**も**乗り越えることはできない」, then re-splice all four options end to end. |
| **A4** | 問題13-67 | broken Japanese in a stem | Stem: 「嗅覚による記憶の**呼び起され方**について」. Correct okurigana is 呼び起こされ方 — and the passage itself writes it correctly 20 lines earlier: 「匂いによって**呼び起こされる**記憶は」. Two spellings of one lemma in one paper. | 「呼び起こされ方」. |
| **A5** | 問題2-6 ↔ 問題8-46 | cross-section answer leak | Item 6 keys おさめた→**収めた** against 納/治/修. 問題8-46's stem prints the answer in kanji: 「彼はまだ初心者である…見事な成果を**収めた**。」 An examinee who reaches 問題8 can back-solve item 6 without knowing the compound. | Rewrite 46's tail (e.g. 「見事な結果を出した」) or re-carrier item 6. No tested 表記/漢字 string may appear elsewhere in the booklet body. |
| **A6** | 問題10(1) ↔ 問題13 | topic repeated inside the paper | 問題10(1): 「意識的に通知を切る時間を持つことが、現代人にとって真の休息につながる」. 問題13 closes: 「画面の明るさや通知音に注意を奪われ…たまには目を閉じ…意識を向けてみてはどうだろうか」. Same subject (screen/notification overload → deliberate disconnection) and the same proposition is keyed twice (52 key 2, 69 key 2). | Re-topic 問題10(1) from a surface not already in the paper; the 問題13 essay is the longer investment. |
| **A7** | 問題11 （注1）×3 | apparatus carried over from another test | Test 2's three orphan 問題11 notes are the **same three terms in the same 問題11 slots** as test 1's, lightly reworded: t1 `（注1）格段に：はっきりと大きく` → t2 `（注1）格段：程度がはっきり大きいこと`; t1 `（注1）精神論：気持ちや心がけだけで何とかしようとする考え方` → t2 `（注1）精神論：気持ちだけで解決しようとする考え方`; t1 `（注1）屋上緑化：建物の屋上に植物を植えて緑を増やすこと` → t2 `（注1）屋上緑化：建物の屋上に植物を植えること`. The rewording is why the byte-identical gate check is silent. (The *orphan* half is pre-filed; the **provenance** half is this finding.) | Delete all three; author notes from test 2's own passages. |
| **A8** | 問題6-27, -28, -30 | distractor dies on sight (step 2b) | 27-2 「長い間の努力が実を結び、ついに試験に**反発**することができた」 and 27-3 「新しい機械の操作方法を**反発**して、業務の効率を高めた」 are outside 反発's domain entirely (the slots want 合格/習得) — domain violations, not collocation traps. 28-4 「彼女は約束の時間に**おろそか**に現れて、みんなを驚かせた」 is word salad. 30-1 「服装はいつも**大まか**で、非常に**細かい**デザインにこだわっている」 and 30-3 「到着時刻は**大まか**に決められており、**1秒の狂いもなく正確**だ」 are self-contradictory inside one sentence — eliminable by logic without knowing 大まか. | Apply question-authoring's three-step procedure (write a correct sentence → break exactly one thing inside the word's own domain → search the result). |
| **A9** | 問題1-2, 問題1-3 | distractor not a real word / unrelated kanji | Item 2 (抑える=おさえる): たかえる **is not a Japanese word**; かかえる and つかえる are readings of 抱/使・仕, which share nothing with 抑. Item 3 (講じる=こうじる): **めじる** and **ろうじる** are not words (only ほうじる=焙じる/報じる is). Both violate 「Every option must be a real Japanese word」 and the same-kanji rule. | Item 2: build from 抑/押 readings + real ～える verbs of the same class. Item 3: 報じる／論じる／command real ～じる verbs on visually adjacent 講/構/購/溝. |
| **A10** | 問題10–14 (all 20) | keys findable without the passage | Re-solved the 読解 half from the option sets alone: the key reproduces on **15 of 20** items (52,53,55,57,58,59,60,61,62,63,64,66,67,68,69) because 2–3 distractors per item are absurd absolutes. Samples: 62-1「在宅勤務を**完全に廃止**して…全社員出社体制に戻す」/62-3「業務の**すべて**をオンライン化し、オフィス自体を解約」/62-4「社員の希望を**無視**して…一方的に固定」; 67-3「感情は**一切**伴わない」/67-4「子供時代**しか**体験できない」; 69-1「情報収集を**すべて**やめるべきだ」; 59-2「工房の見学を**一切**行わず」/59-4「職人が観光客の**自宅を訪問**して手芸指導」; 61-2「通勤にかかる時間と費用が**増大**」(under telework). | Rewrite the distractors as statements the passage *addresses and denies*, not as positions nobody holds. Ban the absolute-quantifier tell (すべて/一切/必ず/完全に/しか) from 読解 distractors unless the passage uses it. |
| **A11** | 問題9 48–51 | blank-category collision + no passage-level blank | 49「食欲がわか(ないのも無理はない)」, 50「変えるのは(一筋縄ではいかない)」, 51「味が(欠かせないだろう)」 are all sentence-final predicate slots; 48 is the only connective. **No blank requires tracking the whole passage's argument** — each is decidable from its own sentence (50 from the next sentence, 51 from the following one). Distinct from the pre-filed "tags absent" gate FAIL, which only checks that tags are *written*. | Re-cast one blank as a true `[内容推論]` full-predicate slot whose four options are only separable by the article's overall stance (the 「目新しいものとして騒ぐのではなく」 conclusion is the natural anchor). |
| M1 | 問題7-41 | key not idiomatic in its frame | 「本日の午後5時(限り)、今年度の助成金申請の受付をすべて終了いたします」. The attested deadline forms are 「本日午後5時**をもって**」 or 「本日**限りで**」; bare 「五時限り、」 as an adverbial is not standard. 「〜を限りに」 is on the TOO_HARD list, so the frame the author built only fits an N1 form. | Rewrite the carrier so 「限り」 lands in its N2 sense (「お一人様一点限り」/「本日限りの受付です」). |
| M2 | 問題7-33 vs -42 | one function tested twice | 33「新商品の発売(にあたって)、関係者を集めた発表会が…開催された」 and 42「新しい店舗のオープン(に先立って)、…内覧会と説明会が行われた」 are the same carrier shape and each key fits the other's stem perfectly. Neither key is fixed by meaning, only by which distractors were offered. | Re-carrier 33 to a non-event use (手続き・審査にあたって) or replace one key. |
| M3 | 問題8-44, -45, -47 | tested point below the N2 band | Ledger targets: 「〜たびに」(44), 「〜でなければ」(45), 「状況限定(〜状況において…)」(47). 〜たびに is taught as N3 (multiple standard teaching inventories head it there); 〜でなければ is a basic conditional; 〜において is N3. The paper's 問題8 keys on grammar the examinee cleared two levels ago. | Re-sample `grammar_p8`; add たびに / でなければ / において to `level_band_grammar.txt` `## TOO_EASY` (safe substrings — てからでなければ is already on ALLOW). |
| M4 | 問題2-8 | 2×2 matrix violated | 繋統／計統／**系統**／係統 — only the first character ever varies; 統 is fixed across all four. question-authoring: 「Do not vary only one character position while holding the other fixed」. | Add a second-position swap (系**統**/系**続**) to make the matrix 2×2. |
| M5 | 問題2-9 | tested item too easy | 「ちょきん」→**貯金** is N4 vocabulary, and the distractors 貯全／丁金／待金 are transparent non-words. | Replace with an N2 compound whose components genuinely compete. |
| M6 | 問題4-15, -17 | functional-category grab-bag | 15: 検討／成立／遭遇／辞退 = deliberation / establishment / encounter / declining — four categories, and only 検討 collocates with 「を重ねる」 at all. 17: かろうじて／着々と／相次いで／まんまと = barely / steadily / successively / as-schemed; the 解説 itself names four different usage types, which is the proof it fails 「one label ×4」. | Rebuild 15 from サ変 nouns that all take 「を重ねる」 (検討/協議/議論/審議); rebuild 17 from degree-of-narrowness adverbs (かろうじて/ぎりぎり/どうにか/なんとか). |
| M7 | 問1–6 (all 30) | mandatory artifact absent | The `## 文字・語彙` notes (line 507) are running prose. **Not one** `24: 程度副詞 ×4 (…)` functional-category line exists, and **no** 問題1 distractor-source line (`いたわる=労わる, …`). question-authoring §0 makes both required output; their absence is why A8/A9/M6 shipped. | Add one category line per item 1–30 and one source line per 問題1 item; if a line cannot be written with `×4`, the item is not shippable. |
| M8 | 問題11-62, 11-60, 12-65 | 解説 does not quote the deciding line | **62**: the 解説 quotes 第3段落「テレワーク経験者の約7割が出社と在宅の併用（ハイブリッドワーク）を希望している」, which does not decide the item; the deciding line is 第4段落「両者の強みを融合させたフレキシブルな職場環境をデザインすることが求められている」. **60**: the 解説's 「体験料による直接的な収入増加に加え、ファンが定着すること」 is the **option text**, not the passage — the passage reads 「…に加え、ものづくりの背景にあるストーリーに共感した「ファン」が定着し」. **65**: 「健康管理アプリの普及に伴い…**歩数に励む**人が多い」 misquotes B, which says 「**ウォーキングに**励む人が多い」. | Re-paste all three from the passage. |
| M9 | 問題10(1) | note block inside the passage | Line 233 puts 「（注1）デジタルデトックス：…」 **between** the first and second body paragraphs; the note block belongs after the passage, before the question. | Move the definition line below the passage. |
| M10 | 問題13 注3/注4/注5 | wrong-band and circular glosses | 注3「質感：**ここでは**、感じ方の細かい様子」 and 注4「扉：**ここでは**、思い出へつながるきっかけ」 open with the pattern question-authoring bans as trivial/circular. 注5 marks **バランス**, which is a headword in `openjlpt/vocab-n2.json` — standard N2, must not be glossed at all. (The gate is silent on all three: see R-GATE-3/R-GATE-4.) | Delete the 注5 marker on バランス rather than writing it a definition; drop 注3; keep 注4 only if reworded as a metaphor gloss without 「ここでは」. |
| M11 | 問題5-23 | stem coordination error | 「夜間の外出時には、**スリや防犯**に用心してください」 coordinates a threat (スリ) with a countermeasure (防犯). 用心する takes the danger. | 「スリや**ひったくり**に用心してください」. |
| M12 | 問題8-47 ↔ 読解 | tested form in the paper's own prose | 47 tests 〜(の中)において; the paper then prints 「真のコミュニケーション**において**、沈黙は…」 (問題10(4)) and stem 53 「言語獲得**において**重要だと…」. | Reword the two prose instances. |
| M13 | 問題14-71 | banned stem shape / single-cell lookup | 71 is written as 「このお知らせの内容と合っているものはどれか。」 — the exact shape question-authoring bans at 71 — and key 1 is decidable from one cell (「出演者には『まなびポイント（200ポイント）』を付与します（先着100組）」). The gate filed only the 解説-quote half of this. | Rewrite 71 as a second applicant whose plan fails exactly one condition, and quote both cells. |
| M14 | 問題3-11 | two distractors die on morphology | まみれ／だらけ are **noun** suffixes (泥まみれ/傷だらけ) and cannot attach to the verb stem つけ at all; the item is effectively a 2-way choice between っぱなし and がち. | Replace with verb-stem suffixes that compete (〜がち／〜っぱなし／〜きり／〜通し). |
| M15 | whole test | process | `make check` is RED (43 problems / 15 warnings; 9 FAILs + 1 WARN on test 2). QA's entry condition was not met. | Repair the gate list, then re-review. |
| M16 | ledger | rotation accounting | `logs/ledger.json` test 2 records **5** `word_formation` items for a **3**-item 問題 (gate FAIL). 「〜立て(採れたて)」 and 「当〜(当劇場)」 appear nowhere in the paper but are now burned for future draws. | Trim the two untested items from the test-2 history entry. |

---

## 3. Root-cause table (step 6.5)

Grouped: rows sharing one cause are one skill defect.

| ID | Findings | Code | Tests on disk showing the class | Owning file | Concrete edit |
|---|---|---|---|---|---|
| R-1 | **A1** | `GATE-BLIND` | 1/4 (test 2 only) | `tools/check_consistency.py` + `.agents/question-authoring/SKILL.md` 問題3 | Gate: add `check_word_formation_host()` — for each 問題3 stem, assert a non-particle content token sits immediately adjacent to `(　)`, and that `<host><keyed affix>` is a printed Japanese word. Skill: add the construction step 「まず完成形を書く(怖がる)→接辞だけを切り出して空欄にする→残った語幹が本文に印刷されていることを確認する」. |
| R-2 | **A2**, A8, A9, M6, M14 | `RULE-IGNORED` + `GATE-BLIND` | 4/4 (skill names t1 28, t2 27+28, t3 26/28/29/30, t4 26) | `.agents/question-authoring/SKILL.md` §0 artifact index; `tools/check_consistency.py` | The functional-category line (M7) is the rule that would have caught all five, and it is not written anywhere in this paper (see R-3). Additionally: `check_note`-style FAIL when a 問題6 wrong sentence's collocation is attested is not mechanizable — state that in the skill and keep it human — but the **self-contradiction** half (A8: 大まか＋非常に細かい, 大まか＋1秒の狂いもなく) is decidable: FAIL a 問題6 option containing the keyed word and one of its listed antonyms in the same sentence. |
| R-3 | **M7** (hence A8, A9, M6) | `GATE-BLIND` | 4/4 — no paper on disk carries a `N: label ×4 (…)` line | `tools/check_consistency.py` | Add `check_category_lines()`: FAIL when the `## 文字・語彙` notes block does not contain, for each of items 1–30, one line matching `^\s*(\d+):\s*\S+\s*×4\s*\(.+/.+/.+/.+\)`; for items 1–5 additionally require a `=`-joined distractor-source list. question-authoring §0 already declares the shape — the gate reading it is what makes the artifact non-skippable. |
| R-4 | **A3** | `RULE-IGNORED` | 2/4 (t2 45, t4 three items) | none — process failure | The 問題8 glue rule is explicit ("Read the fixed lead-in, then all four options in key order, then the fixed tail, as one unbroken sentence"). Report per AGENTS.md §0; no skill change. |
| R-5 | **A4** | `GATE-BLIND` | 1/4 | `tools/check_consistency.py` | Add `check_okurigana_consistency()`: collect all `漢字+かな` verb/adjective spans in the booklet body, group by kanji prefix, FAIL when one prefix appears with two different okurigana tails (呼び起こされ / 呼び起され). Cheap, string-decidable, and generalizes past this one typo. |
| R-6 | **A5**, M12 | `RULE-MISSING` + `GATE-BLIND` | 2/4 (t2 収めた; t4 「時代に即した」 vs 問題7-38) | `.agents/question-authoring/SKILL.md` "Item integrity"; `tools/check_consistency.py` | Skill: extend 「One grammar point may be the KEY only once per paper」 to 「**no tested string may appear anywhere else in the booklet body** — a 問題1/2 answer in kanji, or a 問題7–9 keyed form in running prose, hands the item away」. Gate: after parsing keys, FAIL when a keyed 問題2 orthography string, or a 問題7/8/9 keyed form, occurs in the body outside its own option row. |
| R-7 | **A6** | `RULE-UNENFORCEABLE` | ≥2/4 (t4 shipped two 聴解 items on one errand) | `.agents/jlpt-test-generation/SKILL.md` §"One topic, one surface" | The whole-paper topic table is prose with no artifact, so a skipped pass and a done pass look identical. Require the table as a committed section (`tests/<id>/logs` or a `<!-- topic-table -->` block in the .md) with one row per surface and a one-word subject tag, and have the gate FAIL on a repeated tag. Until then it stays a reviewer judgment — say so rather than assuming the gate has it. |
| R-8 | **A7** | `GATE-WRONG` | 2/4 (t1↔t2) — and the gate's existing check reports **clean** | `tools/check_consistency.py` | The current check compares `（注N）` **definition lines** byte-for-byte across tests. Test 2 reworded all three and passed. Fix: compare the **glossed term set** per 問題 slot across generated tests and FAIL on any term reused in the same 問題 slot; re-verify every test that passed on the old check. |
| R-9 | **A10** | `RULE-MISSING` | 4/4 (I re-solved t2 15/20 options-only; the class is the one exam-qa-review §2b names for 問1/4/5/6 but never extends to 読解) | `.agents/question-authoring/SKILL.md` 問題10-14; `.agents/exam-qa-review/SKILL.md` §2b | Skill: add 「**読解 distractors must be positions the passage addresses**: each wrong option restates something the passage says and then denies, qualifies, or reverses. A distractor stating an absolute nobody argues (すべて/一切/必ず/完全に/しか) is noise — official July 2025 ships none.」 Add the construction procedure: harvest all four options from passage sentences, then break the key's three competitors on scope, agent, or direction. §2b gains a 読解 bullet with this paper's 62/67/69 as the shipped example. |
| R-10 | **A11** | `GATE-WRONG` (partial) | 4/4 (skill records t1 48/51, t2 49/50/51, t3 48/50, t4 48/51) | `tools/check_consistency.py` | The gate checks that four **tags** are written and distinct — it cannot see that the tags describe the blanks. That half stays human. But one decidable proxy is missing and would have caught t2: FAIL when ≥3 of the four 問題9 blanks are **sentence-final** (the blank is the last token before 。), which is exactly what 49/50/51 are. |
| R-11 | **M8** | `GATE-WRONG` ×2 | 4/4 papers cleared this check; t3 is the only one it ever fired on | `tools/check_consistency.py:990,1726` | (a) Line 1726 passes `gt[:gcut.start()]` — the **whole body including option rows** — as `source`, so a 解説 that quotes its own option (item 60) matches and is never flagged. Strip stem lines (`^\*\*\d+\*\*`) and option lines (`^\s[1-4]\.`) before matching. (b) Line 1010's `len(p) >= 14` skips both halves of item 65's ellipsis quote (13 and 9 chars). Lower to 8 for ellipsis parts. Re-verify all four papers after the fix. |
| R-12 | **M10** | `GATE-WRONG` | 4/4 (skill names t1 鑑賞/評価制度, t2 質感/バランス, t3 ×7, t4 準備) | `tools/check_consistency.py:826-849` | question-authoring documents the WARN as firing on 「definition body repeating the glossed term **or opening ここでは**」. `check_note_band()` implements only the first half, and only when the term has ≥2 kanji all present in the definition — so 「質感：ここでは…」 and 「扉：ここでは…」 pass silently, as does every katakana term (デジタルデトックス：デジタル機器…). Add: FAIL/WARN when a definition starts with `ここでは` or ends `〜のこと` with no other content, and treat katakana terms by substring rather than by kanji. |
| R-13 | **M3** | `GATE-WRONG` (incomplete data file) | 2/4 (t3's 〜ば〜ほど fired; t2's たびに/でなければ/において did not) | `.agents/exam-qa-review/references/level_band_grammar.txt` | The `## TOO_EASY` list is 18 entries and misses the `grammar_p8` pool's sub-N2 rows. Add `たびに`, `でなければ`, `において` (ALLOW already shields てからでなければ). Then re-sample or prune `pools.json` `grammar_p8` — the pool handed the author these, exactly as it handed test 3 〜ば〜ほど. |
| R-14 | **M13** | `GATE-BLIND` | 3/4 (skill records t2/t3/t4 all putting the content-match shape on 71) | `tools/check_consistency.py` | The banned-stem-shape check runs on 問題11 only. Extend it to item **71**: FAIL when 71's stem matches 「(お知らせ|案内|内容)と合っているもの」. The rule text already exists in question-authoring 問題14. |
| R-15 | **M1**, M2, M4, M5, M9, M11 | `RULE-IGNORED` | mixed | none — process failures | Each has a specific rule already on the page (2×2 matrix; N2 band both sides; note block placement; "the correct sentence must be flawless"; one function per paper). No skill change; report as skipped checks. |
| R-16 | **M16** | `PIPELINE-GAP` | 3/5 ledger entries (4-removed, 2, 4) | `.agents/item-pool-sampling/SKILL.md` + gate (already FAILs) | The sampler recorded a 5-item `word_formation` draw against a 3-item 問題. The gate catches it; the fix belongs in `sample_items.DRAW` alignment and in trimming the historical rows, not in cooldown expiry. |
| R-17 | **M15** | `RULE-IGNORED` | — | none — process failure | QA was entered on a red gate. |

**Blocking note:** R-1, R-3, R-5, R-6, R-7, R-8, R-9, R-10, R-11, R-12, R-13, R-14 are
`RULE-MISSING` / `RULE-UNENFORCEABLE` / `GATE-BLIND` / `GATE-WRONG` / `PIPELINE-GAP` and
therefore **block the next generation run** until applied or explicitly rejected
(exam-qa-review §6.5). R-8, R-11 and R-12 are `GATE-WRONG`: every test that passed those
checks must be re-verified after the fix.

---

## 4. Coverage statement

**Blind solve.** Items 1–71 answered from `tests/2/言語知識・読解.md` lines 1–492 only;
key section (line 493+) read afterwards. 71/71 agreement, 0 mismatches.

**Step 1 — key-by-key proof, all 71.** Deciding fact recorded for each:

- 問題1 (1–5): 更新=こうしん / 抑=おさ / 講=こう / 免=まぬが / 潤=うるお. All five keys correct.
- 問題2 (6–10): 成功を**収**める collocation / 継続 / 系統 / 貯金 / 削減. All correct.
- 問題3 (11–13): っぱなし on V-masu / **A1 — no host printed** / 総人口 (**A2 — 全人口 equally valid**).
- 問題4 (14–20): 流れに逆らう / 検討を重ねる / Nに貢献する (無生物主語可) / かろうじて間に合う / 拝借 (謙譲) / まして (a fortiori) / 捜索が難航する. All correct.
- 問題5 (21–25): swap-in tested on all five — 「にぎやかだ」「だいたい終了した」「注意してください」「急速な変化」「取り乱していては」 all survive the frame. Keys correct; stem defect at 23 (M11).
- 問題6 (26–30): keys 1/4/1/3/2 — each keyed sentence is itself flawless. Option-sentence length avg **30.2 JP chars** (official ~27) ✓ in band.
- 問題7 (31–42): all twelve keys are the N2 form the frame demands; 41 is the exception (M1).
- 問題8 (43–47): every item spliced end to end in 解説 order — 43 「つまり今の彼には/自分の自由な時間/というものを/ほとんど持てていない」✓; 44 「知らない町を訪れる/たびに必ず/予想もしない新しい/発見が何度もあり」✓ (必ず＋何度も is redundant but grammatical); 45 ✗ (**A3**); 46 「わりにうまく/本番での強い緊張を/乗り越えて高いパフォーマンスを/しっかり発揮し」✓ (うまく sits far from 乗り越えて — awkward, not broken); 47 「状況のなかに/おいては/激しい価格競争が/続く限りは常に」✓ (heavy but grammatical). No word occurs twice in any splice. **Second-ordering hunt run on all five: no item has a second natural ★ position** — every floating element is bound inside its own chunk (たびに必ず, わりにうまく, 続く限りは常に).
- 問題9 (48–51): 48 additive→しかも ✓; 49 「わかないのも無理はない」 ✓; 50 「一筋縄ではいかない」 ✓ (the only option that takes an abstract 行為 subject); 51 「欠かせないだろう」 ✓, confirmed by the next sentence 「味が伴わなければ続く食事にはならない」.
- 読解 (52–71): deciding line located in the passage for all 20. Three 解説 cells do not quote it (M8). Scripted verbatim scan of every `「…」` span in the 読解 key table **against passage prose only** (options and stems excluded) returned exactly two non-verbatim spans: item 60 and item 65.

**Step 2 — two-answer hunt, all 71.** One impossibility reason written per wrong option.
Second defensible answer found in **one** item: **13** (全人口, A2). Near-misses checked and
cleared with a stated reason: 4 のがれた=逃れた (different kanji, both real — 免れる is not
read のがれる); 16 尽力 (requires an animate agent; the subject is 「彼の提案」); 19 一段と
(no a-fortiori reading); 24 急速な vs 緩やかな/複雑な/微妙な (only 急速 carries suddenness);
33/42 (each key blocked from the other item's option list — but see M2); 50 二の足を踏む
(requires a human subject).

**Step 2b — weak distractors.** Functional category written out for every option of
問1/問4/問5/問6 (30 items). Fails: 問題1-2, 問題1-3 (A9); 問題4-15, 問題4-17 (M6); 問題6-27,
-28, -30 (A8). Passing sets, with their single label: 14 「『流れに』を受ける自動詞 ×4」;
19 「程度・進行副詞 ×4」; 21/22/23/24/25 (な形容詞・副詞・動詞 each ×4); 26/29 「時間副詞 /
分業動詞 ×4」; 問題1-4 「〜れた形の離脱動詞 ×4」; 問題1-5 「〜って形の実在動詞 ×4」;
問題1-1, 問題1-3 (on-reading phonetic minimal pairs — the official pattern, accepted for 1).
Borderline, reported not filed: 問題4-16 (反映 is a weaker competitor), 問題4-18, 問題4-20.

**Step 2.5 — level band.** All twelve 問題7 keys checked against
`.agents/exam-qa-review/references/level_band_grammar.txt`: none appears under `## TOO_HARD`
or `## TOO_EASY`; にほかならない, ないことには, にもかかわらず are on `## ALLOW`. Judgment
calls the file cannot decide: **41「限り」** (M1) and the five **問題8** targets (M3 —
たびに N3, でなければ N4, において N3). 問1–6 spot-check: **問題2-9 貯金 is N4** (M5);
問題5-21 活気がある→にぎやかだ is N3-easy (reported, not filed); the remaining 28 sit in band.

**Step 3 — mechanical reads (all run).**

| Measure | Test 2 | Bar | Verdict |
|---|---|---|---|
| 問題7 stem JP chars | 41,44,39,33,32,37,36,42,54,39,52,37 — **avg 40.5**, min 32 | each ≥30, avg ≥40 | **PASS** |
| 問題7 dialogue/setting stems | **2** (39 「（窓口で）」+職員 turn; 41 「（市のホームページで）」) | ≥2 | **PASS** |
| 問題8 assembled sentences | all ≥45 JP chars, options 4–12 chars | not three-word drills | PASS |
| 問題9 cloze body | **538 JP chars** | 500–700 | **PASS** |
| 問題9 blank categories | 論理接続 ×1, 文末/慣用 predicate ×3, `[内容推論]` ×0 | four distinct, one 内容推論 | **FAIL (A11)** |
| in-body `（注N）` markers, 読解 | **6** (問題10(1) デジタルデトックス; 問題13 嗅覚/大脳辺縁系/質感/扉/バランス) vs **8** definition lines | ≥15; July 2025 = 30 | **FAIL** (pre-filed) + orphans both directions (pre-filed) |
| `（中略）` | 1, under the 問題11 instruction line, inside no passage | ≥1 inside a passage | **FAIL** (pre-filed) |
| 読解 section JP chars | 問題10 1035 / 問題11 1860 / 問題12 506 / 問題13 872 / 問題14 530 (gate's own count) | 1150/2250/510/900/560 | **FAIL, all five** (pre-filed) |
| per-passage | 問題10: 216/191/176/180/172; 問題11: 424/487/494/**284** | 200 / 400 | **FAIL** (pre-filed) |
| 問題11 structure | 4 passages × 2, instruction 「(1)から(4)」 | ✓ | PASS (stem shapes pre-filed FAIL) |
| 問題2 2×2 matrix | 6 ✓ homophone set, 7 ✓, **8 ✗** (M4), 9 ✓ weak, 10 ✓ | 2×2 | 1 fail |
| 問題3 affixes productive on THIS stem | 11 ✗ (M14), 12 ✗ (A1), 13 ✓ | all four plausible | 2 fails |
| 問題5 swap-in survival | 5/5 survive | must survive | PASS |
| 問題6 option length | avg 30.2 | ~27 | PASS |
| 問題14 constraint count | 70 = app cell + 出演者ポイント cell (2, marginal); **71 = 1 cell** | ≥2 each | **FAIL (M13)** |
| 問題14 invented detail | 「留学生」 is decorative but not contradicted by the flyer | none | pass, noted |
| item counts per 問題 | 5/5/3/7/5/5/12/5/4/5/8/2/3/2 — **identical to `imported-n2-2025-07`** | official | PASS |
| `<ruby>` furigana | none | none | PASS |
| Latin script | `Web`, `SNS` only — both in the gate's `LATIN_OK` (`WEB`, `SNS`) | allowlist only | PASS |
| numbered passage markers | ①② occur only as time-slot labels inside the 問題14 flyer (「①11:00〜12:30 ②14:00〜15:30」), not as bolded passage spans | 1-to-1 with stems | **PASS — gate-adjacent false positive**, reported for clarity |
| every sentence is Japanese | **1 break: item 67's 「呼び起され方」 (A4)**; 1 broken assembly: 45 (A3); 1 unassemblable stem: 12 (A1); 1 coordination error: 23 (M11) | zero | **FAIL** |

**Copy check (scripted).** Every line of test 2's body with ≥12 JP chars was matched
against `tests/1`, `tests/3`, `tests/4` and `tests/imported-n2-2025-07`. **44 hits, all of
them 問題 instruction boilerplate** (「## 問題10 次の(1)から(5)の文章を読んで…」 etc.), which
is official wording every paper must share, plus one generic stem line 「**54** このお知らせ
の内容と合っているものはどれか。」 shared with test 1. **No passage, option, flyer or note
definition is byte-identical to another test's or to the official paper's.** The 問題11
note carry-over (A7) is *near*-verbatim, which is precisely why the scripted check is
clean — see R-8.

**Step 6 (gengo part).** `logs/test_spec.json` on disk is **test 3's**
(`"test_id": "3", "seed": 20260806, "harvest_sha": "dc34edede771"`), so it is not test 2's
blueprint. Audit run against `logs/ledger.json` history entry
`{"test_id": "2", "seed": 20260804, "harvest_sha": "harvest_20260804"}` instead:

| Category | Ledger draw | Paper | Verdict |
|---|---|---|---|
| kanji_reading | 更新/抑える/講じる/免れる/潤う | items 1–5 | **5/5 match** |
| orthography | 収める(成功を)/継続/系統/貯金/削減 | items 6–10 | **5/5 match** |
| word_formation | 〜っぱなし/〜がる(怖がる)/総〜/〜立て/当〜 | items 11–13 | 3 of 5 used; **〜がる's host word missing (A1)**; 〜立て・当〜 untested but recorded (M16) |
| context_words | 逆らう/検討/貢献/かろうじて/拝借/まして/難航 | items 14–20 | **7/7 match** |
| paraphrase | 活気がある/おおかた/用心する/急激だ/じたばたする | items 21–25 | **5/5 match** |
| usage | あらかじめ/反発/おろそか/分担/大まか | items 26–30 | **5/5 match** |
| grammar_p7 | 12 forms, in order | items 31–42 | **12/12 match, in slot order** |
| grammar_p8 | 換言要約/〜たびに/〜でなければ/〜わりに/状況限定 | items 43–47 | **5/5 match** (level: M3) |

**No silent target substitution in 問1–8.** Answer-position compliance could **not** be
audited — `answer_positions` on disk belongs to test 3; see Skips.

**`make check` output, test 2 lines, with resolution:**

- 9 FAILs — （注N） 1-to-1 pairing; both length-floor checks; （中略） placement; 問題11
  retrieval stem shapes; 問題11 考え/主張 coverage; 問題14 two-cell quotes; 問題9 category
  tags; plus two 聴解-side FAILs (問題5 2番 lead-in, stale MP3) outside my scope. All
  pre-filed by the task; **confirmed valid, none is a false positive**, not re-filed here.
- 1 WARN — 「読解 has substantial （注N） glosses … got 6」: **valid**, pre-filed.
- 1 WARN (repo-wide) — 「built HTML records its source sha … 5 stamp(s) missing」: valid,
  build-side, outside my scope.
- **Absent warnings that should have fired** — three silent-gate findings, all evidenced
  above: no 解説-quote WARN despite items 60 and 65 (R-11); no note-band WARN despite
  質感/バランス/ここでは (R-12); no cross-test note-copy FAIL despite A7 (R-8).
- Ledger FAIL 「test 2/word_formation: 5 recorded, DRAW says 3」 — valid (M16).

**Web/URL work:** two searches run to convert judgment into evidence —
`総務省統計局『人口推計』` confirming 全人口 as standard statistical register (A2), and the
JLPT-level classification of 〜たびに / 〜わりに (M3). No harvest-URL spot-check was run
(cross-test provenance is another reviewer's step — see Skips).

**Within-paper topic table** (built, not claimed; cross-test columns deliberately omitted):

| Surface | Subject | Collision |
|---|---|---|
| 問題9 | 昆虫食 — 環境負荷が小さい / 受容と価格の壁 | echoes 問題11(1) |
| 問題10(1) | デジタルデトックス — 通知を切る休息 | **A6 with 問題13** |
| 問題10(2) | 言語獲得と脳科学 — 対話の重要性 | — |
| 問題10(3) | ごみ分別改定のお知らせ | — |
| 問題10(4) | 会話の沈黙 | — |
| 問題10(5) | 夜間オープン講座の案内 | mild echo of 問題14 (市民向け学習機会) |
| 問題11(1) | 脱プラスチック — 環境メリット / コストの壁 | 環境 register ×2 with (4); argument shape shared with 問題9 |
| 問題11(2) | クラフトツーリズム — 地域活性化・若い世代 | 地域活性化＋若年層 ×2 with (4) |
| 問題11(3) | ハイブリッドワーク | — |
| 問題11(4) | グリーンパートナー制度 — 緑地管理・高齢化・若年層 | see (1) and (2) |
| 問題12 | ウォーキングの目標歩数 | — |
| 問題13 | 匂いと記憶 — 視覚偏重の現代 | **A6 with 問題10(1)** |
| 問題14 | 生涯学習フェスタ | — |

One automatic collision (A6). Three softer echoes — 問題9↔問題11(1) (同じ「環境に良いが
コスト/受容が壁」構造), 問題11(1)↔(4) (環境), 問題11(2)↔(4) (地域活性化＋若年層参加) —
reported as one grouped moderate concern rather than four findings; they share A6's root
cause R-7.

---

## 5. Skips

1. **聴解 (問題1–5, 30 items)** — assigned to another reviewer. Not read, not audited.
2. **Cross-test topic table and step 6.3–6.5 provenance/blend audit** (web-fact
   consistency, blend ratios, domain caps, harvest URL spot-checks) — assigned to the
   cross-test/provenance reviewer. Within-paper repetition only is covered above.
3. **Answer-position compliance (step 6.2)** — **cannot be run**: `logs/test_spec.json`
   on disk is test 3's blueprint (`"test_id": "3"`), and `logs/ledger.json` records the
   item draw but **no `answer_positions`** for test 2. Test 2's prescribed key positions
   are not recoverable from any artifact on disk. This is itself a pipeline gap worth
   filing if it is not already: the spec is a single mutable file, so every test's
   blueprint is destroyed by the next test's `merge_seeds.py` run. Recommend
   `logs/test_spec.<test_id>.json` (or a copy into `tests/<id>/`) so past papers stay
   auditable.
4. **Shin Kanzen N2 PDF cross-check (step 2.5 procedure 3)** — not run. The
   `level_band_grammar.txt` inventory was used instead, plus two web searches. No 問題7 key
   sat close enough to the N1 boundary to need the TOC; the level findings raised (M1, M3,
   M5) are on the too-**easy** side, which the PDFs would not have decided either way.
5. **Attestation search for every 問題6 wrong collocation** — searched the two that
   looked possibly real (反発 with 試験/操作方法: neither is attested, both are domain
   violations = A8). The remaining wrong sentences fail on domain or self-contradiction
   before the collocation question arises.
6. **`解答.html` / built HTML** — not inspected; the Markdown is the single source of
   truth and the build stamps are a separate WARN already filed.
