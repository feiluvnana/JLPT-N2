# TEST 4 GENGO/DOKKAI: FAIL (28 findings, 9 automatic)

Reviewer: fresh-eyes QA, `tests/4/言語知識・読解.md` (71 items, 問1–問14). Read in
full before any other tool call: `.agents/exam-qa-review/SKILL.md`,
`.agents/question-authoring/SKILL.md`. Blind-solve ran on lines 1–451 (the file's
key section begins at line 452 and was not opened until all 71 answers were
recorded).

Findings already filed by `make check` for test 4 are NOT re-filed here (読解
length floors, 注1/注5 pairing, （中略） placement, stem 58, 問題11(1)(2)
retrieval-only, item 66 length, 問題14 解説 quotes, 問題9 tags, 5 in-body
glosses). Where I found *additional instances the gate missed*, they are filed
below and marked `[gate missed]`.

---

## 1. Blind-solve diff

**Zero mismatches.** My independent answers for all 71 items equal the printed
keys:

```
 1:1  2:1  3:4  4:3  5:2 |  6:4  7:1  8:1  9:2 10:3 | 11:1 12:1 13:2
14:2 15:3 16:2 17:3 18:1 19:4 20:1 | 21:3 22:1 23:2 24:4 25:1
26:1 27:4 28:1 29:3 30:2 | 31:4 32:1 33:4 34:2 35:2 36:4 37:3 38:1 39:1 40:3 41:3 42:2
43:1 44:2 45:3 46:4 47:1 | 48:1 49:4 50:2 51:3
52:1 53:1 54:3 55:2 56:4 | 57:3 58:2 59:1 60:4 61:4 62:2 63:3 64:1
65:1 66:2 | 67:3 68:1 69:2 | 70:2 71:1
```

Zero mismatches is **not** evidence of health here. Three items I "got right"
only by picking the author's intent over the printed sentence, and they are the
worst findings in the paper:

- **41** — I marked 3 because it is the only option in the semantic
  neighbourhood, then found the spliced sentence is a double negative that says
  the opposite of B's meaning (F2).
- **42** — I marked 2 because をめぐって is the *more idiomatic* of two options
  that both work; 「に関して」 is fully grammatical and natural in the same frame
  (F1).
- **26** — I marked 1 because it is the canonical usage, while option 3
  「一方的に契約を解消した」 is an attested collocation and therefore a second
  correct sentence (F3).

A blind-solve that lands on the key is only a pass when the other three options
are impossible. In these three they are not.

---

## 2. Findings table

`A` = automatic fail per `exam-qa-review` "Ground rules". Item = question number.

| # | Item | Class | Evidence (quoted) | Proposed fix |
|---|---|---|---|---|
| **F1** | 42 | **A** second defensible answer | Stem 「新しい公共施設の建設場所（　）、住民の間で賛否両論の議論が続いている。」 with options `1. に関して 2. をめぐって`. Key 2. 「建設場所に関して、住民の間で賛否両論の議論が続いている」 is ordinary Japanese. 解説 cell gives a gloss of をめぐって only and **no reason at all** for に関して. | Replace distractor 1 with a form the frame rejects (e.g. `に応じて`), or move the blank onto a frame only をめぐって takes (「建設場所（　）の対立が深まる」). Then write the impossibility reason for all three distractors into the 解説. |
| **F2** | 41 | **A** broken Japanese / unanswerable | Stem tail is 「今は旅行（　）状況ではないよ。」 Splicing the key: 「今は旅行**どころではない**状況ではないよ」 — どころではない is a predicate ending, and negating the noun clause again inverts the sense to "it is *not* a situation in which travel is out of the question", i.e. B can travel, contradicting 「書類作成に追われており」. No option produces a well-formed sentence. | Rewrite the tail: 「今は旅行（　）よ。」 with key どころではない, or 「今は旅行（　）の状況ではないよ。」 with key どころ. Re-check all four options against the *fixed text after the blank*, not only before it. |
| **F3** | 26 | **A** two correct sentences | Option 3 「取引先の度重なる納期遅延に業を煮やし、当社は一方的に契約を解消した。」 `question-authoring` 問題6 worked table lists ✗『契約を解消した』 as **"attested — banned (a second correct answer)"** verbatim. The 解説's defence ("合意に基づく解消でないから解除を使う") is a 解除/解消 legal nicety far above the N2 band, and the sentence reads as correct Japanese to any N2 examinee. | Replace option 3 with a right-domain / wrong-collocation sentence per the worked table's target band (e.g.『渋滞を解消に導いた』-shape). Do not defend the key. |
| **F4** | 28 | **A** two correct sentences | Option 4 「体調が悪いときは、無理をせずに妥協することが大切だ。」 妥協する in absolute use ("settle for less rather than push on") is standard Japanese; the sentence is idiomatic, not a misuse. No 解説 note exists for item 28 at all. | Break the collocation instead of the situation — keep the counterpart/standard that 妥協 requires and misuse it. Search the rewritten sentence before keeping it (問題6 procedure step 3). |
| **F5** | 10(4) + 13 | **A** topic repeated inside the paper | 問題10(4): 「質の高い眠りを確保することが、**日中のパフォーマンス**改善につながる。」 問題13: 「心と頭を休ませることこそが、結果として**日中のパフォーマンス**や人生の質を高めることになる。」 Two 読解 passages arguing the same thesis (rest quality → daytime performance) and sharing an 8-char phrase. | Re-topic 問題10(4) (the shorter passage) onto a subject no other surface uses. Rebuild the whole-paper topic table afterwards. |
| **F6** | 57 | **A** 読解 key findable without reading `[gate missed]` | Key option 3 is 38 JP chars of which **36 are a verbatim contiguous lift** of the passage's closing sentence: 「参加者にとって地域の魅力を新たな視点で発見できる貴重な機会になると考えて」. No other option contains any passage language. The gate's rule fires only at ≥50 chars AND ≥1.7× mean; this is 39 chars at 1.36×, so it passed. | Paraphrase the key to ~25–30 chars ("地域を新しい目で見直す機会になる"). See F6 root cause for the gate metric that misses it. |
| **F7** | 24 | **A** distractor eliminable on sight (wrong functional category) | Options `案の定 / とっくに / 一段と / 比較的` (key 4). Categories: 予想副詞 / 時間副詞 / 程度副詞 / 程度副詞 — not `×4`. **This exact set is already named as a fail example in `exam-qa-review` §2b** ("わりに (key) with 案の定/とっくに/一段と"). The stem was repaired since the previous round (「値段のわりに」→「わりに簡単に終わった」, swap-in now survives: 「この作業は比較的簡単に終わった」 ✓) but the option set was left untouched. | Replace 案の定 and とっくに with degree adverbs (`思ったより`, `かなり`, `わりあい`-class competitors) and write the `24: 程度副詞 ×4 (…)` line. |
| **F8** | 2, 5 | **A** distractor eliminable on sight (問1 same-kanji rule) | **2** 賢い: `かしこい / すごい / きびしい / たくましい` = 賢/凄/厳/逞 — none of 凄・厳・逞 shares a radical or component with 賢. Worse, the stem itself prints 「厳しい状況の中でも」 in kanji, so きびしい is dead on sight. **5** 逃す: `のがす / もどす / はがす / はずす` = 逃/戻/剥/外 — no shared component; the item's own in-kanji trap にがす (逃がす) is not offered. (Item **1** 労わる is now compliant: 労/労/栄/営 share the ⺌+冖 crown. Item **4** 省みる is marginal — 試/鑑/惟 are unrelated kanji but all four are 〜みる reflection verbs.) | 2: build from 賢/堅/緊 or use readings of 賢 itself. 5: use にがす/のがれる-family and same-radical 逸. Print the `いたわる=労わる, ねぎらう=労う, …` source line for every 問1 item. |
| **F9** | 48–51 | **A** 問題9 blank category collision + no whole-passage blank | With the category tags absent (gate FAIL, filed) I classified the four blanks myself: 48 `のも無理はない/わけにはいかない/わけがない/べきではない` = 文末モーダル選択; 49 = 論理接続; 50 = 慣用句; 51 `〜とは言い切れない/〜おそれがある/〜に違いない/〜どころではない` = 文末モーダル選択 again. 48 and 51 collide. Separately, **no blank requires tracking the whole passage**: 48 is decided by the preceding sentence, 49 by the preceding examples, 50 by the same clause (「好機を逃し、…」), 51 by the immediately following 「だが…」. | Rebuild 51 as the `[内容推論]` blank (a full predicate that only the article's overall argument — オンラインとオフラインの融合 — selects), then write all four tags. Assign tags *before* writing the blanks. |
| **F10** | 31, 32, 36 | High (key leaked into the reading passages) | 問題11(4) line 337: 「少子高齢化**に伴う**担い手不足により、縮小や中断を**せざるを得ない**状況になっている」 — the keys of items 31 (〜にともなって) and 32 (〜ざるを得ない). 問題11(1) line 278: 「経験の有無**を問わず**誰でも参加できる」 — the key of item 36, in nearly the same frame as its own stem 「年齢や職業（を問わず）、…誰でも受講することができる」. | Rewrite the three passage sentences (「担い手不足で縮小や中断が相次いでいる」, 「経験の有無に関係なく」). This is string-decidable — see root cause R4. |
| F11 | 1–30 (all) | Missing mandatory artifact | The `## 文字・語彙` notes contain only one ※ line covering items 26/27/30. **Not one** `N: <category> ×4 (opt/opt/opt/opt)` line exists for the 30 items, and no 問1 distractor-source line. `question-authoring` §0 lists both as required output whose absence makes the item "not shippable". F7 and F8 are exactly what those lines exist to expose. | Write the 30 category lines and the 5 問1 source lines; any item that cannot take a single `×4` label gets its options replaced first. |
| F12 | 44 | Unnatural assembled sentence | Splice: 「地球温暖化への**対策**として、当地域では、省エネ**対策**などをはじめとする各種環境保全の総合的な実現を急いで目指している。」 「各種環境保全の総合的な実現」 is not a collocation; 「実現を急いで目指している」 stacks two aspectual verbs; 対策 occurs in both the fixed lead-in and option 3. (★=2 is nonetheless the only possible order — I permuted all 24.) | Rewrite option 2 to 「環境保全の総合的な**対策の**」 → drop 対策 from the stem, or change the fixed tail to 「…実現を目指している」 and put 急いで inside another option. |
| F13 | 45 | Marginal collocation in the assembled sentence | 「乱れていた生活習慣を見直したのを**ちょうどきっかけに**思い切って…」 — the collocation is 「〜をきっかけに」 or 「ちょうどよい機会に」; bare 「ちょうどきっかけに」 is off. (Order is unique; ★=3 correct.) | Move ちょうど: 「見直したのを**ちょうどよい**きっかけに」 (and re-count option chars). |
| F14 | 61, 62 | Two items, one deciding sentence | Both keys reduce to the same clause 「建物の歴史的価値を活かしながら…観光客や地域住民を呼び込み、地域経済の活性化につなげる試みが成果を上げている」. Key 61-4 「建物の歴史的価値を活かしつつ地域を活性化し…」 and key 62-2 「地域資源を活かして観光客や住民を呼び込み、地域経済の活性化に…」 are paraphrases of each other, so solving one hands over the other. | Re-aim 62 at the 筆者's evaluation of the *risk* side (維持管理費の高騰・所有者の高齢化) or lengthen the passage (it is 231 JP chars against a 400 floor — already filed) and give the second question new ground. |
| F15 | 60, 63 | Pure-retrieval 問題11 stems `[gate missed]` | Stem 60 「…今後の可能性について、文章では**どのように述べられているか**」 and stem 63 「…課題として、**本文で挙げられているもの**はどれか」 are the banned retrieval shape in wording the gate's four literal strings (`本文で述べられて` / `として正しいもの` / `主な目的は` / `内容と合っている`) do not match. Stem 61 「…プロジェクトの**目的は何か**」 likewise dodges `〜の主な目的は`. Measured: **6 of 8** 問題11 stems do not name 筆者 (official July 2025 = 0). | Re-cast 60/61/63 as 筆者-anchored 考え/主張 stems. Gate fix in R7. |
| F16 | 11(1) | Wrong genre for 中文 | 問題11(1) is a 募集案内 (「募集人数は15名程度で、活動日は…」), not an essay — there is no 筆者 to ask about, which is *why* stems 57/58 cannot name one. It also duplicates the notice register of 問題10(2) (図書館休館のお知らせ) and 問題14 (flyer): three of the paper's reading surfaces are administrative notices. | Replace passage (1) with an opinion column carrying a turn (しかし/ところが), per `question-authoring` 問題10–14. |
| F17 | 11(1)–(4) | Monotone 問題11 theme set | (1) 地域交流イベントのスタッフ募集 / (2) 農業の高齢化・人手不足→ロボット / (3) 古民家改修による地域活性化 / (4) 伝統行事の担い手不足→若者ボランティア. Every passage is 地域の担い手不足・地域活性化; (2) and (4) both open on 高齢化に伴う担い手不足. 問題10(5) 規格外野菜 also overlaps (2)'s agriculture. | Re-topic at least two of the four from unrelated domains before rebuilding the topic table. |
| F18 | 29 | Three distractors fail for one unrelated reason | 「1 図書館で古い文献を模索して」「2 迷子になった子供の居場所を模索している」「4 暗い部屋の中で失くした鍵を手で模索した」 — all three are *concrete physical searching*, so the item collapses to "pick the abstract one" without knowing 模索 vs 捜索/探索. | Keep one concrete misuse; make the other two abstract-but-wrong (模索 where 検討/模倣 belongs). |
| F19 | 12 | Two of four affixes cannot attach to the stem | 「（　）自動で乾燥まで行なってくれる」 with `全 / 半 / 準 / 超`. 全自動 ✓ and 半自動 ✓ are real words; **準自動・超自動 are not**, so only two options genuinely compete. | Swap 準/超 for 完/未 (完全自動 / 未…) or move the stem to a noun all four prefixes take. |
| F20 | 15 | Distractor dies on the verb, not the tested point | 「新たな事業（　）を**設立**した」 with 始点/基準/拠点/地点. 基準 is ruled out by 設立 (you do not 設立 a 基準), not by the 事業拠点 semantics the item tests. | Replace 基準 with a location-class noun (本部/据点-adjacent) so all four compete on the same axis. |
| F21 | 27 | Distractors with no written impossibility reason; one near-attested | ※ note explains only option 2 (「測定した」が適切). Option 1 「荷物の重さを手で把握してから」 is unexplained, and 「重さを把握する」 is itself attested — only the inserted 「手で」 makes it wrong, which is a fine line to leave unstated. | Write the reason for options 1 and 3; strengthen 1 by removing the attested core (e.g. put 把握 on a purely physical grip). |
| F22 | 57 | 解説 elimination reason is incoherent | 解説: 「1は**展示内容の紹介ではなく団体自身の考えを問う設問のため不適合**」. Option 1 is 「経験者だけが参加すべきイベントだと考えている」; nothing in it concerns 展示内容. The line that actually denies it — 「応募条件は18歳以上であることのみで、活動経験は問いません」 — is never quoted. | Replace the cell with the denying quote. |
| F23 | 68, 69 | 解説 paragraph references wrong | 68 says 「第2段落の…」 but 「情報を遮断し、思考を休ませることで初めて…」 is in the **third** paragraph (after （中略）). 69 says 「第3段落の…」 but 「意識的にスケジュールの余白を作り出し…」 is in the **fourth**. (Both quotes themselves are verbatim-present; `make check` reports no missing quote for this file.) | Renumber, counting （中略） as a paragraph break. |
| F24 | 71 | Single-constraint 問題14 item, banned shape re-worded | Key 1 turns on one flyer cell, 「（平日10:00〜16:00、**事前予約不要**）」. The stem 「リンさんの行動に関する説明として適切なものはどれか」 is 「内容と合っているものはどれか」 rewritten — `question-authoring` requires 71 to be "a second applicant whose plan fails exactly one condition". (Only the 解説-quote proxy was gate-filed.) Also リンさん's stated 60歳 is never a condition anywhere in the flyer — decorative scenario detail. | Rewrite 71 as a person-scenario combining 還元率 + 付与上限 or 対象外 + 有効期限, and quote both cells. |
| F25 | 47 | Drawn point realized one level down | Ledger drew `義務当然(〜ねばならない)`; the paper's fixed tail is 「なければならない」, which is on `level_band_grammar.txt` `## TOO_EASY`. The 解説 states the substitution was deliberate ("「ねば」と「なければ」の二重条件表現を避けている"), which fixes last round's double-conditional but leaves the drawn N2 form untested. | Keep the drawn form once: 「…立ち返ら（ねばならない）」 as the fixed tail with 立ち返ら inside an option, or re-draw the point. |
| F26 | 31/42, 37/40 | Same form spelled two ways / key doubles as a distractor | Item 31 offers 「にそって」 in kana, items 40 and 42 offer 「に沿って」 in kanji — one form, two spellings, one paper. Item 37 offers 「を通して」 as a distractor while item 40 **keys** it. | Normalize the spelling; keep a keyed form out of other items' option lists. |
| F27 | 1–71 | Answer-position imbalance (unverifiable against the blueprint) | Distribution of the 71 keys: **1×25, 2×18, 3×15, 4×13**; 文字・語彙 alone is 1×12 / 2×7 / 3×6 / 4×5. Items 1–2 are both 1. `logs/test_spec.json` on disk describes **test 3**, and test 4's `logs/ledger.json` entry records `items` only — no `answer_positions` — so the prescribed positions cannot be recovered. | Re-derive test 4's spec (seed 20260805 + its harvest) and re-check, or record `answer_positions` in the ledger entry so the audit is possible after the spec rolls over. |
| F28 | 3 (問題3) | Ledger burned two undrawn-into-paper items | Ledger `test 4/word_formation` records 5 items — `〜連れ, 全〜, 無〜, 未〜(未記入), 〜がち(遅刻がち)` — but `DRAW` is 3 and the paper authors only the first three. 未記入 and 遅刻がち are marked used without ever being tested. (Gate FAILs this line already; noted here because it is the *paper-side* half: the three authored items are correct, the ledger is what is wrong.) Note that had 〜がち been authored it would have been an off-level key — bare がち is banned by `question-authoring`. | Trim the two over-recorded rows from `logs/ledger.json` (gate message says the same). |

**Verified NOT present** (previous round's defects, independently re-checked):
`迷〜` as a 問題3 negation prefix — gone, item 13 offers the four real prefixes
非/無/未/不. 展開 next to 傾向 in 問題2 — gone; all five 問題2 sets are clean 2×2
component matrices (転/展×換/館, 依/異×頼/来, 審/深×査/差, 支/志×援/園). 問題5
swap-in failure — item 24 now survives the swap. Broken Japanese inside correct
options 「契約の契約書を解消」「互いの条件を歩み寄り」「借りましたCD」「代わりに代診」
— all gone; item 28's key now reads 「互いに少しずつ歩み寄り、双方が納得する形で
妥協した」 (grammatical). 把握 personified onto a medicine — gone. 解消 applied to
discarding a computer — gone (though F3 replaced it with the opposite failure).
問題7 short carriers — fixed: average 40.2 JP chars, minimum 34, versus the
20–34 averages of tests 1–4. 問題8 glue defects (`ご連絡を`+`お問い合わせ
ください`, `立ち返らねば`+`なければならない`) — both fixed. `〜にともなって` keyed
twice (問題7 and 問題9) — fixed; each of the 33 keyed grammar points is keyed once.

---

## 3. Root causes (step 6.5)

Recurrence counted by reading tests/1, 2, 3 and imported-n2-2025-07 on disk, not
from memory.

| R | Findings | Code | Tests showing the class | Owning file | Concrete edit |
|---|---|---|---|---|---|
| **R1** | F1, F4, F21 | `RULE-IGNORED` + `GATE-BLIND` | 2, 3, 4 (systemic) | `question-authoring` "Name the reason each distractor is IMPOSSIBLE — in writing"; `tools/check_consistency.py` | The rule is specific and was skipped: 7 of the 12 問題7 解説 cells (31, 33, 37, 38, 40, 41, 42) name **no** distractor at all, and 問題6 items 28/29 have no note. Make it decidable: add `check_distractor_reasons()` — FAIL when a 問題7/9 解説 cell does not mention all three distractor numbers (`1「…」`/`2「…」`/`4「…」` pattern), and when a 問題6 item has no ※ line naming its three wrong sentences. A cell that must list three reasons cannot be written without noticing 「に関して」 has none. |
| **R2** | F2 | `RULE-MISSING` for 問題7 (the rule exists only for 問題8) | 4 (1 paper) | `question-authoring` 問題7 section | 問題8 already has "check the GLUE at both ends, not just among the four options". 問題7 has no equivalent, and F2 is the same defect one section earlier. Add after the 問題7 length rule: *"Splice the key into the blank and read the stem's fixed text **after** the blank as one sentence. A predicate-final form (〜どころではない, 〜ようがない, 〜ざるを得ない, 〜かねない) cannot be followed by a noun + だ/ではない tail; 「旅行どころではない状況ではない」 double-negates and inverts the speaker's meaning (test 4 item 41)."* Gate half: WARN when a keyed 問題7 option ends in ない and the stem text after the blank also contains ない before the sentence end. |
| **R3** | F3, F4, F18 | `RULE-IGNORED` + `GATE-BLIND` | 1, 2, 3, 4 (systemic) | `question-authoring` 問題6 procedure; `tools/check_consistency.py` | 『契約を解消した』 is printed **in the skill's own worked table** as banned-because-attested, and shipped anyway — step 3 of the procedure ("Search the result") was not run. Since the paper cannot search, encode what is already known: add `references/banned_collocations.txt` (seeded with 契約を解消, 品質に妥協, 考慮に値する, 妥協する[absolute], 重さを把握) and a gate check that FAILs a 問題6 **wrong** option containing any listed collocation. Also add to the 問題6 procedure: *"a wrong sentence with no object/counterpart for the word (absolute use) is usually correct Japanese — give every wrong sentence an explicit object."* |
| **R4** | F10 | `RULE-UNENFORCEABLE` → `GATE-BLIND` | 3 (「時代に即した」 vs 問題7-38), 4 (three instances) | `tools/check_consistency.py` | The rule ("keep a tested form out of the reading passages too") is prose with no procedure, and it is **fully string-decidable**. Add `check_key_form_leak()`: for every 問題7/8/9 keyed form, fold kanji tails to kana (に伴って/にともなって/に伴う) and search the 読解 passage regions and `聴解スクリプト.txt`; FAIL on a hit. This one check would have caught all three test-4 instances and test 3's. |
| **R5** | F5, F17, F16 | `RULE-UNENFORCEABLE` | 4 (this paper); the cross-test half is another reviewer's scope | `jlpt-test-generation` §"One topic, one surface"; `tools/check_consistency.py` | The topic table is a manual whole-paper pass with no artifact, so a skip is invisible. Cheap decidable floor: WARN when two 読解 passage regions share a content phrase of ≥6 JP chars that is not a function word (「日中のパフォーマンス」 would have fired), and WARN when ≥2 of the four 問題11 passages contain the same ≥4-char domain token (高齢化/担い手/活性化 all repeat here). The genre rule (F16) belongs in `question-authoring` 問題10–14 as a sentence: *"問題11 passages are essays or columns. A 案内/募集/お知らせ has no 筆者 and cannot carry a 考え stem — put notices in 問題10 or 問題14."* |
| **R6** | F6 | `GATE-WRONG` | 3 (3 items, caught), 4 (item 66 caught, item 57 **missed**) | `tools/check_consistency.py` | The check requires `≥50 JP chars AND ≥1.7× the distractor mean`, so it measures *length*, not *lifting*. Item 57 is a 36-of-38-character verbatim lift and passes at 39 chars / 1.36×. Replace the second condition with a lift metric: FAIL when the longest common substring between a keyed 読解 option and its own passage region is **≥20 JP chars and ≥60% of the option**, independent of absolute length; keep the existing length rule as an OR. **Then re-verify tests 1–3 on the corrected metric** — a green result on the old metric was never evidence. |
| **R7** | F15 | `GATE-WRONG` | 2, 3, 4 (each has a stem that dodges the literal list) | `tools/check_consistency.py` + `question-authoring` 問題11 | The ban is implemented as four literal strings, so synonyms walk straight through (`文章ではどのように述べられているか`, `本文で挙げられているもの`, `目的は何か` without 主な). Replace with the positive test the skill already states and which official papers satisfy 8/8: **FAIL any 問題11 stem that does not contain 筆者 and is not 「①…とあるが、どういうことか」**. That is one rule instead of a growing blacklist, and it cannot be dodged by rewording. Current measurement: test 4 = 6/8 non-compliant. |
| **R8** | F7, F8, F11, F19, F20 | `RULE-IGNORED` → `GATE-BLIND` | 1, 2, 3, 4 (systemic) | `question-authoring` §0 artifact table; `tools/check_consistency.py` | The `×4` category line and the 問1 source line are declared mandatory output, and **zero** of the 30 required lines exist in test 4. They exist precisely to make F7/F8 visible in one glance, and the gate does not read them (it reads only the 問題9 tags and 問題14 quotes). Add `check_vocab_category_lines()`: FAIL when the `## 文字・語彙` notes lack one `^\d+: .+ ×4 \(.+/.+/.+/.+\)$` line per item 1–30, and one `reading=word` source list per item 1–5. String-decidable, and it forces the author to confront a set like 案の定/とっくに/一段と that cannot take a single label. |
| **R9** | F9 | `RULE-IGNORED` (tags) + human judgment (collision) | 1, 2, 3, 4 (systemic — the skill itself records 4/4) | `question-authoring` 問題9 | The tag artifact is already mandatory and already gated; test 4 simply has none (gate FAIL, filed). Note the honest limit for the fixing pass: once tags exist, the gate can only check that four distinct strings are present — an author who tags a 文末モーダル blank `[内容推論]` still passes. The "one blank must require the whole passage" property stays a reviewer judgment; say so in the skill so the next reviewer does not assume the gate covers it. |
| **R10** | F12, F13 | `RULE-UNENFORCEABLE` | 2, 3, 4 | `question-authoring` 問題8 | "Splice … and read the result end to end" produces no artifact, so an awkward-but-grammatical result (F12) is never caught. Require the spliced sentence to be **written into the 解説 cell in full** after the option-order line — a sentence you must type out is a sentence you read. (The order line alone, which is what the gate parses, does not surface 「各種環境保全の総合的な実現を急いで目指している」.) |
| **R11** | F24 | `GATE-WRONG` | 2, 3, 4 (item 71 in all three) | `tools/check_consistency.py` + `question-authoring` 問題14 | The gate checks the **解説** for two flyer quotes, which is a proxy: an author can quote two cells for a key that turns on one. Add the stem-side half the skill states: FAIL a 問題14 stem matching `内容と合っている|説明として適切なもの|正しいものはどれか`, and require both 70 and 71 stems to name a person plus at least two of {金額, 日付/期間, カテゴリー, 条件}. |
| **R12** | F27, F28, F25 | `PIPELINE-GAP` | 2, 4 (both flagged by the gate's ledger-count check) | `jlpt-test-generation` workflow + `item-pool-sampling` | `logs/test_spec.json` is a single mutable file, so the blueprint that governed test 4 was overwritten by test 3's run and the 71 answer positions are now unauditable (F27). Fix the workflow: **snapshot the spec to `tests/<id>/test_spec.json` at the end of step 3**, and have `check_consistency.py` prefer the per-test copy. Same snapshot fixes attribution for F25/F28. |
| — | F14, F22, F23, F26, F21 | `RULE-IGNORED` | — | none | Process failures under AGENTS.md §0 (write the deciding quote, count the paragraphs, do not re-use a keyed form). No skill change proposed. |

---

## 4. Coverage statement

Steps run, on `tests/4/言語知識・読解.md` unless noted. All 71 items, no sampling.

**Blind-solve** — lines 1–451 only, all 71 answers recorded before line 452 was
opened. Diff in §1.

**Step 1 (key-by-key proof, 71/71)** — every key traced to a deciding line.
問1–30 traced to the ledger's drawn item plus the collocation; 問31–47 to the
grammar point and the spliced sentence; 問48–51 to the neighbouring sentence;
問52–71 to a passage line. `make check` reports **no** unlocatable 解説 quote for
this file (the one quote WARN in the run belongs to test 3). Two 解説 cells
mislabel the paragraph (F23) and one gives an incoherent reason (F22).

**Step 2 (two-answer hunt, 71/71)** — one impossibility line written per wrong
option. Three items could not be closed: F1 (42 / に関して), F3 (26 / 契約を解消),
F4 (28 / 妥協). Two more are thin but survive: item 18 (実施 vs 実行 — 「調査を
実行する」 is marked, 実施 is the collocation) and item 27 option 1 (「重さを手で
把握」 — the attested core is 「重さを把握」, and only 「手で」 breaks it; filed as
F21 for the missing written reason rather than as a second answer).

**Step 2b (weak distractors)** — functional category written out for every option
of 問1/問4/問5/問6:

| Item | Categories | Verdict |
|---|---|---|
| 1 労わる | 労/労/栄/営 — ⺌冖 crown shared | pass |
| 2 賢い | 賢/凄/厳/逞 | **F8** |
| 3 却下 | phonetic variants of 却下 | pass |
| 4 省みる | 省/試/鑑/惟 — all 〜みる 内省動詞 | marginal |
| 5 逃す | 逃/戻/剥/外 | **F8** |
| 14 | 漢語サ変 ×4 (text handling) | pass |
| 15 | 始点/基準/拠点/地点 — 基準 off-axis | **F20** |
| 16 | オノマトペ副詞 ×4 | pass |
| 17 | な形容詞＋にする ×4 | pass |
| 18 | 実〜サ変 ×4 | pass |
| 19 | 実感副詞/情感副詞/明瞭副詞/実感副詞 | fail (mixed; つくづく also near-synonymous with the key) |
| 20 | 漢語サ変 ×4 | pass |
| 21 | 時間/頻度/様態/様態 | marginal |
| 22, 23 | 様態副詞 ×4 | pass |
| 24 | 予想/時間/程度/程度 | **F7** |
| 25 | 時間副詞 ×3 + 目的副詞 | marginal |
| 26–30 | 用法 — see F3, F4, F18, F21 | 3 fails |

**Step 2.5 (level band)** — all 12 問題7 keys checked against
`references/level_band_grammar.txt`: にともなって / ざるを得ない(ALLOW) /
にわたって / 次第 / だからといって / を問わず / にかけては / ようがない(ALLOW) /
ことだ(ALLOW) / を通して / どころではない / をめぐって — **no TOO_HARD hit, no
TOO_EASY hit**. 問題8 drawn points: 補足追加(なお), をはじめ, をきっかけに,
のみならず, ねばならない — the last is realized as なければならない, TOO_EASY (F25).
問題9 keys: のも無理はない / つまり / 元も子もなくなる / さらに高まっていくに違いない
— in band (に違いない is low-N2 but is not the discrimination; polarity is).
問1–6 spot-checks: 却下・省みる・逃す・抜粋・拠点・克服・模索・把握・妥協・考慮 all
sit in the N2 band; かんがみる/おもんみる appear as N1 *distractors* only, which
the skill permits when eliminable.

**Step 3 (mechanical reads)** — every sub-check run:

- **問題7 stem lengths (JP chars):** 31:42, 32:42, 33:35, 34:53, 35:35, 36:38,
  37:39, 38:36, 39:34, 40:38, 41:56, 42:34 → **average 40.2**, median 38,
  minimum 34, none under 30. Official average ~43; the paper clears the ≥40
  average and the ≥30 floor. **Dialogue/setting stems: 2** (34 `（会場アナウンス）`,
  41 `（同僚に）` + A/B turns), meeting the ≥2 requirement — tests 1–4 previously
  shipped zero.
- **問題8:** option-character sums 43:29, 44:31, 45:43, 46:28, 47:32 (band
  16–29; 45 runs long, not a fail). Assembled sentences all ≥45 JP chars. All
  five spliced end-to-end; ★ = 3rd blank in all five and matches the key. Second-
  ordering hunt: all 24 permutations tried per item — **each item has exactly one
  natural order** (the floating adverbs 思い切って/本格的に/広く/大きく/いったん/
  もう一度 are each bound inside an option, not free-standing). No word occurs
  twice inside an option chain; 対策 repeats between stem and option in 44 (F12).
- **問題9:** cloze prose **557 JP chars** (official band 500–700 ✓). Four blanks;
  stem+option read aloud for all sixteen combinations — no blank repeats what
  the stem already says. Categories and the missing 内容推論 blank: F9.
- **問題1:** all four options share the target's word form in every item (all
  dictionary-form after last round's て-form fix); no conjugation/okurigana
  giveaway in any of the five; every option is a real word. Same-kanji rule:
  F8.
- **問題2:** 2×2 component matrix confirmed for all five — 転/展×換/館,
  務/努/勤(+求), 依/異×頼/来, 審/深×査/差, 支/志×援/園. No real unrelated word in
  any set. This section is clean.
- **問題3:** three items (matches `DRAW`=3). Affixes: 連れ/ぐるみ/付き/揃い (all
  real, productive), 全/半/準/超 (F19), 非/無/未/不 (the four real negation
  prefixes ✓). No nonsense affix.
- **問題5:** swap-in survival tested on all five keys — 「偶然出会った」/「少しずつ
  和やかに」/「すぐに片付けて」/「比較的簡単に終わった」/「前もって確認して」 all
  grammatical ✓.
- **問題6:** option-sentence lengths 26:[26,28,34,37] 27:[25,32,21,29]
  28:[26,27,21,26] 29:[24,20,28,20] 30:[23,27,23,36] → **average 26.6 JP chars**
  against official ~27 and tests 1–4's ~19. Length is fixed. Domain/collocation:
  F3, F4, F18, F21.
- **読解 apparatus:** in-body `（注N）` markers = **5** (定義行 5, occurrences 10);
  bar is ≥15, official July 2025 = 30 — gate WARN, filed. Marker/definition
  pairing broken in two places (filed). No `<ruby>` anywhere ✓. No Latin-script
  prose ✓ (gate). Numbered passage markers ①② : none used, none orphaned ✓.
  Section lengths **問題10 1043 / 問題11 1325 / 問題12 442 / 問題13 833 /
  問題14 502** against floors 1150/2250/510/900/560 — all five short (filed).
  Per-passage: 問題10 (1) 227, (2) 208, (3) 205, (4) **178**, (5) 225 (floor 200);
  問題11 (1) 420, (2) **304**, (3) **231**, (4) **370** (floor 400) — filed.
- **読解 key vs distractor lengths** (key chars / distractor mean / ratio): 52
  23/26.3, 53 31/31.3, 54 29/27.3, 55 28/25.7, 56 32/28.7, 57 **39/28.7 (1.36,
  36-char verbatim lift — F6)**, 58 22/14.3, 59 34/32.0, 60 40/29.7 (19-char
  lift), 61 34/28.0, 62 46/30.3 (1.52), 63 33/22.7, 64 37/33.0 (22-char lift),
  65 27/29.3, 66 **55/31.3 (1.76 — gate-filed)**, 67 32/28.3, 68 31/32.0, 69
  31/30.7, 70 4/4.0, 71 37/33.3.
- **問題14:** item 70 combines two constraints (20% 一般店舗 + 5% 大型店;
  800+500=1,300 ✓, and the ¥2,000-per-transaction cap does not bind) — compliant.
  Item 71: F24. Every scenario detail except リンさん's age is describable from
  the flyer. Internal date arithmetic is consistent (11/1 火 → 11/30 水 ✓;
  問題11(1) 11/5 水 + 11/15 土 ✓; 問題10(2) 10/10 月 → 10/15 土 ✓).
- **Every sentence is Japanese:** read end to end. One broken construction found
  (F2, item 41) and two awkward-but-grammatical assemblies (F12, F13). No broken
  Japanese inside any *correct* option — last round's four are all repaired.
- **Copy check:** every ≥20-JP-char sentence of test 4 (267 of them) and every
  ≥12-char option (139) searched against `tests/1`, `tests/2`, `tests/3` and
  `tests/imported-n2-2025-07`. **Zero content matches**; the only 9 hits are the
  official 問題11/12/13 instruction lines, which are boilerplate and must be
  identical. No apparatus (`（注N）` definition lines) is shared either.

**Step 6, gengo part (target-item audit)** — `logs/test_spec.json` on disk
describes **test 3** (`test_id: 3`, seed 20260806), so it is not test 4's
blueprint. `logs/ledger.json` holds two relevant entries: **`test 4`** (seed
20260805, harvest `harvest_20260805`, generated 2026-08-04 14:55) and
**`test 4-removed`** (seed 20260803, harvest `legacy0803sh`, generated
2026-08-03 17:36) — a superseded draw whose items (募る/占める/粘る…, 〜制/準〜/
〜風…, 円滑/衰退/柔軟…) appear nowhere in the shipped paper, so the shipped test 4
is the `test 4` entry. Audited against it:

| Category | Drawn | In paper | Verdict |
|---|---|---|---|
| kanji_reading | 労わる, 賢い, 却下, 省みる, 逃す | items 1–5, same order | **5/5 ✓** |
| orthography | 転換, 務める(役職を), 依頼, 審査, 支援 | items 6–10 | **5/5 ✓** |
| word_formation | 〜連れ, 全〜, 無〜, 未〜, 〜がち | items 11–13 = 連れ/全/無 | 3/3 authored ✓; 2 recorded-unused (F28) |
| context_words | 抜粋, 拠点, じっくり, おろそか, 実施, しみじみ, 克服 | items 14–20, same order | **7/7 ✓** |
| paraphrase | たまたま, 徐々に, さっさと, わりに, あらかじめ | items 21–25 | **5/5 ✓** |
| usage | 解消, 把握, 妥協, 模索, 考慮 | items 26–30 | **5/5 ✓** |
| grammar_p7 | にともなって, ざるを得ない, にわたって, 次第, だからといって, を問わず, にかけては, ようがない, ことだ, を通して, どころではない, をめぐって | items 31–42, same order | **12/12 ✓** |
| grammar_p8 | 補足追加(なお), 〜をはじめ, 〜をきっかけに, 限定表現(のみならず), 義務当然(ねばならない) | items 43–47 | 5/5 ✓ (47 realized as なければならない — F25) |

**No silent target substitution** in 問1–8. Answer-position compliance could not
be audited (F27, and see Skips).

**`make check` WARN lines for test 4, each resolved:**

| WARN | Resolution |
|---|---|
| `読解 has substantial （注N） glosses … got 5` | **Real.** Filed by the gate; confirmed by my own in-body count of 5 markers / 5 definitions. |
| `聴解 two-party items cast two distinguishable voices — 1番。大学で教授 ['教授','学生']` | Out of my scope (聴解 reviewer). Not evaluated. |
| `built HTML records its source sha — 5 stamp(s) missing` | **Real, and it applies to every test on disk including the imported one**, so it is a repo-wide un-stamped state rather than a test-4 regression. It still means the shipped `解答.html` cannot be proven to match the Markdown I reviewed — my findings are against the `.md`, which is the single source of truth. Rebuild before serving. |

No WARN was found to be a false positive on this file.

---

## 5. Skips (each with its reason)

1. **Answer-position compliance for the 71 keys (step 6.2).** Skipped — no
   blueprint on disk. `logs/test_spec.json` holds test 3 (`test_id: 3`, seed
   20260806) and test 4's ledger entry records `items` only, with no
   `answer_positions` key. I report the observed distribution instead
   (1×25 / 2×18 / 3×15 / 4×13; F27) and propose the per-test spec snapshot in
   R12.
2. **Web fact consistency, blend balance, carrier cap, harvest URL fetch
   (step 6.3–6.5).** Skipped — explicitly assigned to the cross-test
   topic/provenance reviewer in my task scope. I did not fetch any URL.
3. **Cross-test topic table (step 5).** Skipped for the cross-test axis (same
   reason). The *within-paper* half is done and produced F5, F16, F17.
4. **聴解 (step 4, and the 聴解 half of steps 1–2).** Out of scope by assignment.
5. **Shin Kanzen N2 PDF cross-check for the hard side of step 2.5.** Not run —
   I used `references/level_band_grammar.txt` plus judgment. No key fell near
   the N1 boundary (the hardest are にかけては and どころではない, both squarely
   Shin Kanzen N2), so rasterizing the TOC would not have changed a verdict.
   Stating it so the next reviewer does not assume the inventory was consulted.
6. **Live collocation searches** for F3 / F4 / item 18 / item 27. No web fetch
   was performed. F3 rests on `question-authoring`'s own worked table, which
   names 『契約を解消した』 as attested and banned — authoritative within the repo.
   F4 and item 27's option 1 rest on my judgment of attestation and are flagged
   as such; a fixing pass with web access should search them before rewriting.
7. **No file in the repo was modified.** Reviewer role: report only.
