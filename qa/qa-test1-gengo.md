# TEST 1 GENGO/DOKKAI: FAIL (26 findings, 7 automatic)

Scope: the 71 言語知識・読解 items (問1–問14) of `tests/1` only. Reviewer authored nothing
in this paper. No file in the repo was edited.

**Entry-condition violation (report first):** `exam-qa-review` requires a green
`make check` before QA starts. `make check` is currently **RED — 43 problems**, 8 of
them on test 1. I proceeded anyway because the task assigned the review, but the
verdict below is not "QA on a green gate".

---

## 2. Blind-solve diff

I answered all 71 items from lines 1–454 only (the key section begins at line 455 and
was not opened until every answer was written down).

**Mismatches: ZERO.** All 71 blind answers equal the keys:

```
1:1  2:2  3:3  4:4  5:3  6:1  7:2  8:2  9:3 10:1 11:1 12:3 13:2 14:1 15:2
16:2 17:1 18:3 19:1 20:3 21:1 22:1 23:2 24:3 25:3 26:1 27:2 28:3 29:1 30:1
31:2 32:3 33:2 34:3 35:2 36:1 37:4 38:1 39:3 40:2 41:3 42:3 43:1 44:3 45:3
46:3 47:4 48:2 49:1 50:3 51:4 52:2 53:2 54:4 55:2 56:3 57:3 58:1 59:2 60:2
61:3 62:4 63:3 64:2 65:2 66:1 67:1 68:2 69:3 70:4 71:2
```

No mis-key exists in this paper. But a 71/71 blind solve is **itself a signal, not a
clean bill**: I solved 問題12 item 66 and several 読解 items without needing the
passage (G21, G22), and two 問題8 items admit a *second* natural ordering whose ★ is a
different option (G2, G3) — my blind answer matched the key there by choosing the
ordering the author intended, not because the other is excluded. Those are filed below.

---

## 3. Findings table

Automatic-fail classes are marked **AUTO**. Pre-filed `make check` findings (読解 length
floors, 問題11 retrieval stems, 問題9 tags absent, 問題14 解説 quotes, 9 glosses, 鑑賞)
are NOT repeated here; where I found an *additional* instance the gate missed it is
filed (G18), and where I judged a rule a false positive it is in §5.

| # | Item | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| **G1** | 問5 **24** | **AUTO** — 問題5 option not substitutable | Stem `この製品のデザインは**ありふれて**いる。` — bold span ends in て, the four options are `珍しい / 古い / どこにでもある / 流行している`. Swapping the key gives 「デザインは**どこにでもある**いる」. Same break for all four. Official bar `imported-n2-2025-07` 問24 is `中山さんは**帰省して**います。` with all four options in て-form (`ふるさとに戻って`…) | Extend the bold to `**ありふれている**` and keep the plain-form options (or keep the span and rewrite all four as て-forms) |
| **G2** | 問8 **43** | **AUTO** — second defensible ★ | Key order `2→4→1→3` = 「このチーズケーキは値段の安さのわりに濃厚な味で、とても喜ばれた」 (★=1). Order `2→3→4→1` = 「このチーズケーキは濃厚な味で、値段の安さのわりにとても喜ばれた」 is equally grammatical and idiomatic — わりに attaches to 喜ばれた just as readily — and puts ★ on option **4** | Option 3「濃厚な味で」 is a floating て-form clause: replace with a chunk bound to わりに (e.g. 「濃厚な味がして」→ bind it, or make option 3 the noun phrase the わりに-clause must precede) |
| **G3** | 問8 **47** | **AUTO** — second defensible ★ | Units are `[1+2] ご年齢やご予算に細かく応じた`, `[4] 料金帯の異なる`, `[3] プランをいくつか`. Both pre-nominal modifiers attach to プラン and commute: key `1→2→4→3` (★=4) and `4→1→2→3` = 「料金帯の異なるご年齢やご予算に細かく応じたプランをいくつかご提案いたします」 (★=2). Nothing in the stem orders them | Bind one modifier to the other (e.g. 「料金帯の異なるプランを」 as one option) so only one order parses |
| **G4** | 問12 **65** opt 4 | **AUTO** — broken Japanese | ` 4. 作品は一度しか見ていけないという点` — しか requires ない; 「見ていけない」 is not a form. Intended 「見てはいけない」 | Rewrite as 「作品は一度しか見てはいけないという点」 (or replace the distractor) |
| **G5** | 問13 passage | **AUTO** — broken Japanese in a passage | 「話を聞きながら、私は自分の**勘知識**に気づいた。」 — 勘知識 is not a Japanese word | 「自分の**思い違い**に気づいた」 |
| **G6** | 問6 **28** 解消 | **AUTO** — distractors eliminable for one reason unrelated to the tested point | All three wrong sentences break the same way (解消 used for 消す/捨てる): 「冷蔵庫に残っていた牛乳を解消した」/「部屋の電気を解消した」/「書き間違えた文字をきれいに解消した」. `question-authoring` names 『部屋の電気を解消した』 verbatim as the banned domain-violation example. A learner who knows 解消 ≠ 消す kills all three at once → 1-way item. Contrast the official set 潰す (`imported-n2-2025-07` 問26), whose three wrong sentences break differently (割る / 畳む / 破る) | Keep at most one 消-domain misuse; add two in-domain wrong collocations per the skill's worked example (e.g. 「渋滞を解消に導いた」-type: right domain, wrong collocation) |
| **G7** | 問9 **48**/**51** | **AUTO** — two blanks in one category, and no whole-passage blank | 48 keys `だけ` (副助詞/限定), 51 keys `つもり` (形式名詞/認識) — one category by `question-authoring`'s taxonomy (`[慣用・形式名詞]`). 49 `慣れてしまい` is an aspectual て-form, none of the four listed types. **None** of the four requires tracking the whole passage: 48/49/51 are decided by their own clause, 50 by the adjacent sentence pair | Rewrite one of 48/51 as an `[内容推論]` full-predicate blank (four clause options, decidable only from the whole column's argument) and one as `[文末モーダル]`; then write the four tags (the tags themselves are the pre-filed gate FAIL) |
| G8 | 問7 **41** | tested form recurs in the paper | 問7-41 keys 〜たところ; 問題11(4) passage reads 「屋上を社員が野菜を育てる菜園に**したところ**、部署の違う社員同士の会話が増えた」 in the same 結果 sense — and the 63 解説 quotes that exact sentence | Reword the passage to 「菜園にしたら」/「菜園にした結果」 |
| G9 | 問9 **48** | key primed inside its own passage | Blank 48 keys だけ in 「かざす【48】で支払いが済む」; the same passage's last line reads 「支出を見直す**だけでも**、使いすぎには早めに気づけるはずだ」 | Reword the closing sentence (「見直せば」) |
| G10 | 問7 **31**/**37** | option sets 75% identical | 31 = `がたい/かねない/きれない/ぬけない`; 37 = `かねない/きれない/がたい/ようがない` — three shared options across two items of the same 問題 | Rebuild 37's distractors from a different family |
| G11 | all 71 | realized answer-position imbalance | Distribution 1:19 2:22 3:23 **4:7** (9.9%). 文字・語彙 keys option 4 **once in 30** (item 4); 問題2/4/5/6 never key 4; 問題8 keys 3 three times in five | Re-order options so each 問題 spreads positions; the drawn spec (unavailable, see §6) prescribes ~4 distinct positions per 5-item block |
| G12 | 問4 **19** | 2b — no shared functional category | かろうじて (辛うじて達成) / たいして (否定呼応の程度) / かえって (逆接評価) / いっそ (選択). Cannot be written as one label ×4; たいして dies on the affirmative 「間に合った」 without knowing かろうじて. Same shape as the banned わりに + 案の定/とっくに/一段と set | Replace with 達成度副詞 ×4 (やっと/ようやく/どうにか as competitors) |
| G13 | 問4 **17** | 2b — mixed part of speech | 需要 (数量名詞) / 重要 (な形容詞) / 必要 (な形容詞) / 応募 (スル名詞). Only 需要 can be the subject of 伸びている; the frame kills 重要/必要 on form | Use quantity nouns ×4 (需要/消費…— but note 消費 would create a second answer; prefer 供給/出荷/売上-type competitors) |
| G14 | 問4 **15** | 2b — four unrelated mimetic domains | ぎっしり (密度) / うんざり (心理) / がっしり (体格) / じっくり (態度). Only うんざり and がっしり even take 〜してきた. Official 問17 (べたべた/かさかさ/じめじめ/ちくちく) keeps all four in one domain (触感) | Replace with psychological-state mimetics ×4 (うんざり/いらいら/くよくよ/そわそわ) |
| G15 | 問5 **23** | 2b — POS mix | 意外な / 適切な / 複雑な / **厳しい** — three な-adjectives and one い-adjective under the bold span 「**妥当な**」 | Use 妥当な→適切な/穏当な/厳格な-type な-adjectives ×4 |
| G16 | 問6 26–30 | wrong-sentence length under band | Per-item averages 18.8 / 18.2 / 18.2 / 21.0 / 21.0, section average **19.4** JP chars against `question-authoring`'s official ~27 | Give each of the four sentences a who/when/what |
| G17 | 問1–6 key notes | mandatory artifact absent | `## 文字・語彙` carries four free-text notes only (items 5, 7, 8, 20). **Zero** of the 30 items has the required functional-category line `N: 〈label〉 ×4 (…/…/…/…)`, and no 問題1 item has the distractor-source line (`いたわる=労わる, …`). `question-authoring` §0: "An absent artifact makes the item unshippable" | Write all 30 category lines and 5 source lines; G12–G15 are exactly what writing them would have surfaced |
| G18 | 問12/問13 notes | wrong-band gloss — **additional instances the gate missed** | `（注6）評価制度：成績や成果を測る仕組み` — a transparent compound of 評価 + 制度, both standard; and `（注5）慰め：相手を元気づけようとする言葉や態度` — **慰める is present in `openjlpt/vocab-n2.json`**, but the gate matches the marker string 慰め exactly, so only 鑑賞 was reported | Drop both glosses; spend the budget on the N1/rare terms the paper is short of |
| G19 | 問13 notes | note numbering does not restart per passage | 問題12 uses （注1）（注2）; 問題13 then opens at **（注3）** and runs to （注6）. Every passage in `imported-n2-2025-07` restarts at （注1） (verified: 問題11 (1) 注1–2, (2) 注1–4, 問題13 注1–7) | Renumber 問題13 as 注1–注4 |
| G20 | 問10 **54** | non-verbatim 「」 quote in 解説 | 解説 says 「前後する場合がある」; the notice reads 「終了時刻が前後する場合があ**ります**」 | Re-paste the source span |
| G21 | 問12 **66** | 読解 item answerable without the passage | Options 2「AもBも、映画館だけが正しいと考えている」/3「Aは家での鑑賞を支持し、Bは映画館だけを支持している」/4「AもBも、映画を見る必要はないと考えている」 — 4 is absurd on its face and 2/3 are self-cancelling; option 1 is the only coherent statement | Rebuild as a 相違点 question with three partially-true readings of A and B |
| G22 | 問10–14 | key is the longest option in 15 of 19 vertical items | Key/distractor-mean ratios: 53 1.35, 55 1.47, 59 1.41, 61 1.36, 63 1.29, 64 1.30, 66 1.41, 68 1.25, 69 1.27, 71 1.62 — key strictly longest in 11, joint-longest in 4. Gate silent because its rule needs ≥50 chars **and** ≥1.7× | Pad the distractors or trim the keys so the four options sit within ±40% |
| G23 | 問7 | 12-stem average under the authoring target | Counts 45/31/30/33/39/36/34/38/38/64/46/40 → **avg 39.5**, min 30, 4 under 35. `question-authoring`: "paper average ≥40", official ~43. (Clears `exam-qa-review`'s ≥35 fail line) | Add a clause of scene-setting to 32, 33, 34, 37 |
| G24 | 問7 **41** | setting label collapsed onto the stem line | `**41** （駅の案内所で）電車が止まっている理由を駅員に聞いた(　)、…` — `question-authoring` requires the label alone on the first line after `**N**` | Break the line after （駅の案内所で） |
| G25 | provenance | test 1's draw is in no ledger entry, and three of its tested items recur in test 3 | `logs/ledger.json` has 5 history entries (`legacy`, `4-removed`, `2`, `4`, `3`); none has `test_id: "1"`. The unattributed `legacy` entry contains **none** of 問1's five items, **none** of 問2's five, **none** of 問3's three, and only 2 of 問7's 12 forms. Consequence, verifiable on disk: `あふれる` is t1 問6-30 key **and** t3 問6-29 key; `〜たところ` is t1 問7-41 key **and** t3 問7-33 key; `伺う` is t1 問7-42 key **and** t3 問7-37 key | Reconstruct a `test_id: "1"` history entry from the paper before the next draw, or re-sample the three collided items |
| G26 | 問2 **6** | option set duplicates an official item's | Test 1: けいこう → `傾向/頃向/傾好/携向`. `imported-n2-2025-07` 問7: けいこう → `傾向/頃向/傾高/頃高` — same target word, two of four options byte-identical in the same slots. Root: this exact set is `question-authoring`'s own worked example, copied from the official paper | Change the target compound (e.g. のうこう/かくじゅう were also lifted — pick a fresh one) |

---

## 4. Root-cause table (step 6.5)

Grouped; a row covers every finding listed in it. "Tests showing the class" was measured
by reading the other papers/spec on disk where stated, not from memory.

| # | Findings | Code | Tests w/ class | Owning file | Concrete proposed edit |
|---|---|---|---|---|---|
| R1 | G12, G13, G14, G15, G17, G6 | **GATE-BLIND** (the rule exists and its artifact is mandated; nothing reads the artifact) | 4/4 per the skill's own record | `tools/check_consistency.py` | Add `check_category_lines(name, key_gengo)`: for every item 1–30 require a line in `## 文字・語彙` matching `^\s*(\d+):\s*(\S+)\s*×4\s*\(([^/]+/){3}[^)]+\)` whose four listed options equal the item's four options in order, and for items 1–5 additionally a line containing `=` four times. **FAIL** on any missing item. This is the one edit that would have caught G6 and G12–G15 at authoring time, because the author cannot write `程度副詞 ×4` over かろうじて/たいして/かえって/いっそ. |
| R2 | G1 | **GATE-BLIND** (string-decidable) | t1; t4 shipped the same class (「値段の比較的美味しい」) | `tools/check_consistency.py` | Add to the 問題5 checks: extract the bold span and the characters that follow it up to 。; if the span ends in `て/で` (or the trailing text starts with `いる/います/いた`), FAIL unless all four options end in `て/で`. |
| R3 | G2, G3 | **RULE-UNENFORCEABLE** (the permutation hunt is required but leaves no artifact, so a skipped hunt and a passed hunt look identical) | 4/4 — the skill records one such item in each of t2, t3, t4 | `question-authoring` (問題8 section) + `tools/check_consistency.py` | Make the hunt an artifact like the 問題9 tags: **each 問題8 解説 cell must append the rejected orderings it tested**, e.g. `他順: 2-3-4-1 →「…わりにとても喜ばれた」は成立するため不可`. Gate: FAIL a 問題8 解説 with no `他順:` segment. An author who must write the alternative down discovers G2 while writing it. |
| R4 | G4, G5 | **RULE-IGNORED** for G5 (「read the whole paper aloud once」 exists and was skipped) + **GATE-BLIND** for the decidable half | 4/4 (t4 shipped six broken sentences) | `tools/check_consistency.py` | Cheap, near-zero-false-positive check that catches G4 exactly: FAIL any stem/option/passage sentence containing `しか` with no `ない/ぬ/ません/まい` before the next 。. G5's class (a coined compound like 勘知識) can only be a WARN — propose: WARN on any 2+ kanji token in a passage that appears in none of the vendored `openjlpt/vocab-n*.json` slices. State plainly in `exam-qa-review` that full broken-Japanese detection stays human judgment. |
| R5 | G8, G9, G10 | **GATE-BLIND** (string-decidable, no check exists) | t4 shipped the class (〜にともなって keyed twice; 「時代に即した」 in a passage while 問7 tested に即して) | `tools/check_consistency.py` | Add `check_tested_form_reuse()`: collect the 問題7/8/9 keyed forms from the 文法 key table, strip the leading 〜, and FAIL when a form occurs literally in 読解 passage prose or in the 問題9 cloze body; and FAIL when two items in the same 問題 share ≥3 of their 4 options. |
| R6 | G11, G25 | **PIPELINE-GAP** (a paper can exist on disk with no ledger attribution, so its items are never excluded from later draws) + GATE-BLIND for the position spread | 1 test (t1) unattributed; the collision it caused is visible in t3 | `jlpt-test-generation` workflow §sampling + `tools/check_consistency.py` | Gate: FAIL when `tests/<id>/` exists (non-`imported-`) and `logs/ledger.json` has no history entry with that `test_id`. WARN when any answer number is keyed on fewer than 15% of a paper's 71 gengo keys. Workflow: state that `sample_items.py` must be called with `--test-id <id>` (the `make sample` default has no way to pass it — `AGENTS.md` §4 already flags this, so make the gate enforce it). |
| R7 | G16, G23, G24 | **RULE-UNENFORCEABLE** (numbers exist in prose; only 読解 lengths are gated) | 4/4 for 問題7 length (t1–t4 avg 20–34) | `tools/check_consistency.py` | Extend the length gate that already owns 読解: FAIL 問題7 when the 12-stem average < 40 or any stem < 30 JP chars; FAIL 問題6 when the 20 option sentences average < 24; FAIL a 問題7 stem whose line contains `（…で）` followed by more than the label. |
| R8 | G18 | **GATE-WRONG** (the check exists and mis-measures, so green was not evidence) | t1 (慰め, 評価制度); the skill records t2 質感/バランス, t4 準備 under the same blindness | `tools/check_consistency.py` | Two fixes to the vocab-band WARN: (1) normalize the glossed term before lookup — try the term, term+`る`, term+`する`, term+`い`, and the term with a restored okurigana tail (慰め→慰める); (2) add a compound rule — for a 4-kanji gloss term, WARN when it splits into two 2-kanji halves that are both headwords in `vocab-n2.json` or absent-but-basic (評価/制度). Then **re-verify every test that passed on it** (t2, t3, t4 glosses). |
| R9 | G19 | **RULE-MISSING** (no skill says note numbering restarts per passage; the gate only checks 1-to-1 pairing) | t1 confirmed; unchecked in t2–t4 | `question-authoring` (問題10-14 → 「Vocabulary Explanations」) + `tools/check_consistency.py` | Add the sentence: 「（注N）の番号は**各パッセージごとに（注1）から振り直す**。問題12のAとBは一つのパッセージとして通し番号でよい（official July 2025）」. Gate: FAIL when any passage's in-body markers do not start at 1 and run contiguously. |
| R10 | G20 | **GATE-BLIND at the margin** (the check exists but only fires at ≥14 chars — `check_explanation_quotes`, line 1008) | 3/4 per the skill's record (13 condensed 「」 spans in t3 alone) | `tools/check_consistency.py` | In `check_explanation_quotes`, add a second pass: for a 「」 span of 6–13 chars that is not in the source, WARN when an edit-distance-≤2 variant **is** in the source. A near-miss is the condensed-quote signature and has almost no false positives; absence alone at that length does not. |
| R11 | G21, G22 | **RULE-MISSING** (the 2b plausibility rule enumerates 問1/問4–6 and 聴解問題1–3; 読解 options are not covered anywhere) | t1 (66); the "key findable without the passage" class shipped in t3 and t4 in its length form | `exam-qa-review` §2b + `question-authoring` (読解 section) | Add a 読解 bullet to §2b: 「読解: for every wrong option, name the line in the passage that raises it and the line that denies it. An option contradicted by nothing in the passage (or self-evidently false without it) is noise — the item then tests nothing.」 Gate (WARN): flag a 読解 item whose key is the longest of the four in more than 60% of items 52–71. |
| R12 | G26 | **RULE-WRONG** (the skill's worked example is a verbatim official item, so a compliant author reproduces it) | t1 confirmed; check t2–t4's 問題2 against the same example | `question-authoring` (問題2 表記) | Replace the three worked examples — `けいこう → 傾向/頃向/傾高/頃高` is `imported-n2-2025-07` 問7 exactly. Substitute invented compounds and add: 「Worked examples in this file are patterns, not items — never ship an example's option set.」 Gate: extend the existing "no （注N） definition byte-identical across tests" check to 問題1–3 option **sets** vs `imported-*` papers. |

**Boundary note:** per `exam-qa-review` §6.5 I did not apply any of these edits. The one
file the reviewer may edit is `exam-qa-review/SKILL.md` itself; I did not edit it either,
because R11 (the only genuinely absent class) is proposed above and the review is being
returned to an orchestrator that owns the fix pass. Flagging that explicitly so it is
not silently dropped: **R11's §2b edit still needs to be made.**

---

## 5. False positives — rules I checked test 1 against and cleared, with evidence

The bar is `imported-n2-2025-07`: a rule that paper fails is a wrong rule. Three
findings I would otherwise have filed are withdrawn, and each is a `GATE-WRONG`-class
defect in the *rule*, not in test 1:

| Rule | Test 1 item | Why it is a false positive |
|---|---|---|
| 問題1 「every distractor must be a reading of the target's OWN kanji, or of a kanji sharing a radical/visual component」 (`question-authoring` 問題1, `exam-qa-review` §2b) | Items 2 慌てて (すてて=捨/あてて=当/たてて=立), 3 妨げて (和/広/掲), 4 潔く (快/素早/著) | The official paper does exactly this: 問1-**2** 辛い → あまい/にがい/しぶい (甘い/苦い/渋い — nothing shared with 辛), 問1-**5** 収まった → さだまった/しずまった/やすまった (定/静/休). The official pattern is *same word form + same conjugation class + same semantic field*. Test 1's three items satisfy all of it, and every option is a real word with the conjugation lock intact (the ～てて/～れて leak the skill records for test 1's item 2 has already been repaired). **Proposed edit:** restate the rule as 「same conjugation class AND (same kanji/radical **or** same semantic field)」 in both files. |
| 問題3 「affixes that could plausibly attach to THIS stem」 | Item 11 諸/複/類/群 on 問題 | Official 問3-**11** is 教育 → 則/理/論/規: 教育則/教育理/教育規 do not attach either. Official 問題3 distractors are real morphemes that fail the specific collocation, which is what test 1 has. |
| 問題1/2 「every option must be a real Japanese word」 applied to 表記 | Item 8 `負れて` | Official 問2-**6** offers 液って/温って/汗って and 問2-**10** offers 支接/施接/支設 — non-words are the norm in 表記, where the options are candidate spellings, not words. |

**Level band (§2.5), all 問題7–9 keys + spot-checks:** かねない / ざるを得ない /
わけにはいかない / に先立って / を契機に / つつも / ようがない / に限って / ものの /
ばかりに / たところ / 伺う / わりに / ように / つつある / 応じた / だけ / てしまい /
しかし / つもり. All are Shin-Kanzen N2 headed forms; `references/level_band_grammar.txt`
lists かねない・ざるを得ない・わけにはいかない・つつも・ようがない・に限って・つつある・
だけ under `ALLOW` and none under `TOO_HARD`. One near-miss checked and cleared: the file
lists **つもりです** under `TOO_EASY` (the N4 volitional). 問9-51 keys the N2 self-perception
sense 「節約している**つもり**だったのに」, a different point, so it is in band — but an
author working from the list could not tell, so `level_band_grammar.txt` should read
`つもりです（意志）— ただし「〜ているつもりだ（認識）」はN2`.

---

## 6. Coverage statement

**Read in full before any other tool call:** `.agents/exam-qa-review/SKILL.md` (462 lines),
`.agents/question-authoring/SKILL.md` (745 lines).
**Read for the review:** `tests/1/言語知識・読解.md` (518 lines — lines 1–454 first, keys
at 455–519 only afterwards), `logs/test_spec.json`, `logs/ledger.json`,
`tests/imported-n2-2025-07/言語知識・読解.md` (問題1–6 and the 読解 apparatus, as the bar),
`tests/2|3|4/言語知識・読解.md` (copy-check + t3 item collision),
`.agents/exam-qa-review/references/level_band_grammar.txt`,
`.agents/item-pool-sampling/references/openjlpt/vocab-n2.json`,
`tools/check_consistency.py` (the quote and gloss checkers, lines 885–1015).

| Step | Items covered | Result |
|---|---|---|
| Blind solve | 71 / 71 | 0 mismatches (§2) |
| 1 — key-by-key proof | 71 / 71 | Every key traces to a deciding line. One 解説 quote non-verbatim (G20); the other 8 flagged by my matcher are grammar-form citations (「〜ざるを得ない」) or blank-filled reconstructions (48, 51) and are legitimate |
| 2 — two-answer hunt | 71 / 71 | 2 items with a second defensible answer (G2, G3). Checked and cleared the known near-synonym traps: 20 発足/成立 (sanctioned pair), 14 難航 with no 停滞 present, 17 需要 with no 消費 present, 29 妥協 (「妥協を続けている」 is attested but the sentence is semantically self-contradicting, so it is not a second key) |
| 2b — weak distractors | 30 / 30 (問1–6), category written out for each | 4 fails (G12–G15), 1 one-reason set (G6); 問1 all five sets pass ×4 (音読み×4 for 1/5, 一段動詞て形×4 for 2, 〜げる動詞て形×4 for 3, 形容詞連用形×4 for 4); 問5 21/22/25 pass (〜ことに副詞句×4, 状態述語×4, て形述語×4); 問4 14/18/20 pass |
| 2.5 — level band | 問題7–9 keys (21) + spot-checks on 問1–6 | All in band; see §5 |
| 3 — mechanical reads | all | Counts below |
| 6 — provenance (gengo part) | 問1–8 targets, 71 key positions | **SKIPPED against the spec — reason in §7**; substituted a ledger audit, which produced G25 and G11 |

**Counts measured (not claimed):**

- **問題7 stems (JP chars):** 45, 31, 30, 33, 39, 36, 34, 38, 38, 64, 46, 40 → **avg 39.5**,
  median 38, min 30, 0 under 30, 4 under 35. Dialogue/setting-label stems: **3** (40, 41,
  42) — the ≥2 rule is met; 41's layout is G24.
- **問題8:** option sums 23 / 23 / 29 / 22 / 29 (band 16–29 ✓); ≥2 options ≥5 chars in all
  five ✓; longest option 9/8/10/7/8 (≥7 ✓); assembled sentences 49 / 52 / 58 / 45 / 59
  (≥45 ✓). Splice test: every item assembles to one grammatical sentence with no word
  twice ✓. Second-ordering hunt: 43 and 47 fail (G2, G3); 46 has two natural orderings
  (`ここ数年→世界各国で` and the reverse) but **★ is option 3 in both**, so the key stays
  unique — noted, not filed. 44 and 45 are order-locked.
- **問題9:** body ≈ **495** JP chars excluding the instruction line (541 with it) — at the
  bottom edge of the official 500–700 band. Blank categories: 48 副助詞/限定, 49 アスペクト
  て形, 50 論理接続, 51 形式名詞 → 48 and 51 collide, none is 内容推論 (G7).
- **読解 lengths** (gate's own measurement, authoritative): 問題10 894 (floor 1150) with
  passages 229/139/180/178/169 (floor 200 → four short); 問題11 1832 (floor 2250) with
  passages 409/381/449/525 (floor 400 → (2) short); 問題12 377 (floor 510); 問題13 **951
  (floor 900 — the one section in band)**; 問題14 243 (floor 560). All pre-filed.
- **読解 apparatus:** in-body （注N） markers **9**, definition lines **9**, pairing 1-to-1
  per passage, **no orphans in either direction** ✓ (this is the one apparatus rule tests
  2/3/4 failed and test 1 passes). （中略） **×4**, all inside 問題11(1), 問題11(2),
  問題11(4), 問題13 ✓. Numbering restart: **fails** (G19). No `<ruby>` anywhere ✓.
  Numbered markers ①/② pair 1-to-1 with stems in every passage ✓ (問題11(1) ①→57,
  (3) ①→61, (4) ①→63 ②→64, 問題13 ①→67 ②→68; no orphans).
- **問題14:** item 70 combines 曜日・時間帯 + 対象(初心者) → B and E ✓ two constraints;
  item 71 combines 申込期限 + 受付方法(電話不可) + 支払方法(振込・当日不可) ✓ three
  constraints, and is a person-scenario, not 「内容と合っているもの」 — test 1 is the
  compliant example the skill cites, confirmed. Every referenced detail (28歳, E's start
  month) is describable from the flyer ✓. The missing 解説 cell quotes are pre-filed.
- **読解 key/distractor lengths:** no key ≥50 chars, so the gate's rule cannot fire; but
  the key is the longest option in 11 of 19 and joint-longest in 4 more (G22). Max ratio
  1.62 (item 71).
- **Copy check** (all ≥12-JP-char sentences of test 1 vs `imported-n2-2025-07` and tests
  2/3/4): **no passage, stem, or option sentence is shared.** The 14/14/11/5 overlaps are
  the official 問題 instruction lines (which must be identical), the header, and two
  generic stems — 「筆者の考えに合うのはどれか」 (shared with the official paper, an
  official stem shape, and used here in 問題10 where it is not banned) and
  「このお知らせの内容と合っているものはどれか」 (shared with test 2, in 問題10 where the
  ban does not apply). The one real overlap is the 問題2 option set, filed as G26.
- **Latin script:** only `A-102` / `A-105` (品番, inside a business email — official papers
  print product codes), the `A`/`B` speaker labels in 問7-40, and `N2` in the title. No
  unfinished English words ✓.
- **`make check` WARNs on test 1, with resolution:** `鑑賞` gloss → pre-filed, real
  (confirmed: 鑑賞 is a headword in `vocab-n2.json`). `9 in-body glosses vs official 30` →
  pre-filed, real (I measured 9 independently). `built HTML records its source sha — 5
  stamps missing` → out of my scope (build pass), left open. `聴解 two-party voices` and
  `test 4` WARN → out of scope. **No 解説-quote WARN was emitted for test 1, and that is a
  gate gap, not evidence** — item 54's quote is non-verbatim but 9 chars long, under the
  checker's 14-char floor (G20/R10).

---

## 7. Skips

1. **Step 6 answer-position and target-item audit against `logs/test_spec.json` — SKIPPED.**
   The on-disk spec is `test_id: 3`, `seed: 20260806`, and its `items` are test 3's
   (軍/尋ねる/副/改/縮小 for 漢字読み against test 1's 交渉/慌てる/妨げる/潔い/措置). Test 1's
   blueprint no longer exists on disk, so neither the target-item match nor the 71-position
   compliance can be checked. **Substituted:** a `logs/ledger.json` audit, which showed test 1
   has no history entry at all and produced G25, plus a distribution audit of the realized
   keys (G11). Attribution for test 1 is unavailable — stated per the task instruction.
2. **Steps 4, 5, and the web/harvest half of step 6 — out of scope by assignment**
   (聴解 structure, the cross-test topic table, harvest URL fetches, blend balance).
   Another reviewer covers them. Note for whoever does: `logs/test_spec.json` cannot serve
   test 1 there either, for the same reason.
3. **Shin-Kanzen PDF cross-check of the hard side (§2.5 step 3)** — not run. Every 問題7–9
   key is on `question-authoring`'s own N2 inventory list and `level_band_grammar.txt`
   classifies the ones it covers as ALLOW, so rasterizing the N2 文法 TOC would not have
   changed a verdict. Stated rather than implied.
4. **The pre-filed `make check` classes** (読解 length floors and per-passage minima,
   問題11 (1)(3)(4) retrieval-only, 問題9 tags absent, 問題14 解説 quotes, 9 glosses, 鑑賞)
   were verified as real but not re-filed, per the task instruction. One *additional*
   instance of the gloss class was found and is filed as G18.
5. **No file was edited**, including `exam-qa-review/SKILL.md`, which §6.5 would permit —
   see the boundary note under §4.
