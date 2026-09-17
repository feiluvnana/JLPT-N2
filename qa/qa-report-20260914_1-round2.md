# QA report — 20260914_1 (round 2, stage 4 re-review)

Reviewed 2026-09-17, in a context that authored nothing and repaired nothing in
this paper. Round 1 (`qa/qa-report-20260914_1.md`) returned `QA: FAIL` with 6
findings; this round re-reviews the six repairs, their whole 大問, and the
collateral each repair could have moved.

Reviewed revision (sha1 over raw bytes, re-verified after the review — unmoved):

| file | sha1 | round 1's sha1 | moved? |
|---|---|---|---|
| `tests/20260914_1/言語知識・読解.md` | `da9cf3b0d8d320bf7517d02325acd271ec082f19` | `5a72de2f3ee6…` | **yes** (F1/F2/F3/F5) |
| `tests/20260914_1/聴解.md` | `c49a45173973bfabf438e9575e0a1b3e46d2c876` | `c49a45173973…` | no |
| `tests/20260914_1/聴解スクリプト.txt` | `7b5b31fe2832ee910eac8b15acfb04d699b76767` | `707c88cf0f82…` | **yes** (F4, one character) |

Upstream sources also read: `tests/imported-n2-2022-07/聴解スクリプト.txt`,
`logs/choukai_bank.json`, `logs/choukai_draws.json`, `logs/ledger.json`,
`logs/topics.json`, `.agents/exam-blueprint/references/pools.json`
(`pools_sha 96db386fa22b`, re-computed here, matching spec **and** ledger).

Provenance re-derived from `tests/20260914_1/test_spec.json` (counted, not
retyped): blueprint base seed `48895101`, plus **34** `--reroll-one`
invocations — `reading_topics:9` ×30, `paraphrase:0` ×2, `word_formation:2` ×1,
`kanji_reading:4` ×1. 聴解 composition seed **`91888352`** (unchanged).
`logs/ledger.json` is field-for-field identical to the spec.

---

## 1. Verdict

**QA: FAIL (2 findings, 0 automatic)**

**All six round-1 repairs are verified sound.** Every one of the five touched
items and all four of their 大問 were blind-solved from a freshly rebuilt keyless
render and then proved against the sources; the three escalated judgement calls
are all ruled in the repair context's favour, with measurements below. No new
content defect exists in the paper.

The two findings are both **record/process defects created BY the repair pass**,
which is the collateral class this round exists to catch:

- **NEW-1** — the provenance note was corrected to "31 rerolls" and the repairs
  then moved the spec to **34** across four categories. Round 1's F6, reopened by
  its own fix.
- **NEW-2** — F4's repair was applied upstream and to this paper but its third
  prescribed step was not executed: `20260817_1` and `20260818_1` still ship the
  superseded line, so two papers now disagree with `logs/choukai_bank.json`.

Neither is in this paper's content. Both are ≤3 findings, so
`jlpt-test-generation`'s stage-4 exception applies: they may be fixed directly
without a round 3.

## 2. Blind-solve diff

**Solved from `qa/20260914_1/keyless.md`, rebuilt first** (`make keyless
20260914_1`; 905 lines; its header carries `da9cf3b0d8d3` / `c49a45173973` /
`7b5b31fe2832`, i.e. the post-repair revision). The stale pre-repair render that
was on disk was **not** solved from.

Scope solved blind, per §"Fix, regenerate, re-check, RE-REVIEW" (changed items
AND their whole 問題): **問題1 (1–5), 問題5 (21–25), 問題8 (43–47),
聴解問題2 (1番–6番)** = 21 items, answered from that file alone before any key,
解説, `test_spec.json` or repair note was opened.

| 項目 | reviewer | key | |
|---|---|---|---|
| 問題1-1…5 | 2, 4, 1, 3, 4 | 2, 4, 1, 3, 4 | ✅ |
| 問題5-21…25 | 4, 3, 2, 4, 3 | 4, 3, 2, 4, 3 | ✅ |
| 問題8-43…47 | 3, 2, 4, 2, 4 | 3, 2, 4, 2, 4 | ✅ |
| 聴解問題2-1番…6番 | 3, 2, 2, 1, 2, 3 | 3, 2, 2, 1, 2, 3 | ✅ |

**21 of 21, zero mismatches.** No mis-key, no second defensible answer.

**Contamination disclosed:** this reviewer was required to read round 1 in full,
which prints the keys of the 80 untouched items. Those 80 were therefore NOT
re-solved blind and are carried forward from round 1 (§8.1). The 21 items above
are uncontaminated for the three re-authored ones (問題1-2's option field,
問題1-5 whole, 問題5-21 whole — none of which existed when round 1 recorded its
keys) and contaminated-but-unchanged for 問題8/聴解問題2, where the artifact under
review is the **解説 proof**, not the key.

**Blind strategy passes (F1/F2)** were not re-run: no 読解 byte moved. Verified
independently rather than assumed — `tools/dokkai_profile.py` reproduces round
1's paper exactly (total 6149 JP, kanji 30.3 %, sentence median 33.0, bigram
margin **−0.095**, top-rank 30.0 %, spans 1, ※ 0), and the gate reprints
（注N）=32, uniquely-longest-key 4/20, ratio ≤1.65, LCS clean. Round 1's
27.8 % / 16.7 % stand.

## 3. Per-question walkthrough — the re-reviewed scope (21 items)

### 問題1 (漢字読み) — F2 (item 5 re-drawn), F3 (item 2 option field rebuilt)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 2 | OK | `**巨額**` 全語ボールド、{きょ,ぎょ}×{かく,がく} 完備。四択とも仮名骨格一致。未変更、round 1 の判定を再確認 | — |
| 問題1-2 | 4 | **OK（修理検証済み）** | `**伸ばす**`／ころばす・とばす・けとばす・のばす。四択とも実在の五段他動詞、送り仮名「ばす」統一（gate `every 問題1 option carries the printed okurigana` ok）。field=「物や体に力を加えて動かす」は四択すべてに当てはまる（転ばす＝倒して動かす／飛ばす＝飛んで行かせる／蹴飛ばす＝蹴って動かす／伸ばす＝引いて長くする）。round 1 F3 の「喜ばす＝感情の分野」は解消 | — |
| 問題1-3 | 1 | OK | `**性格**`、{せい,しょう}×{かく,がく}。未変更 | — |
| 問題1-4 | 3 | OK | `**神経症**`、{しん,じん}×{しょう,じょう}、中間「けい」固定。未変更 | — |
| 問題1-5 | 4 | **OK（修理検証済み）** | `**投手**`／としゅ・とうじゅ・とじゅ・とうしゅ。音読み複合語ターゲットなので `moji-goi.md` §RESOLVE 手順6（「実在語 **または** キー自身の音読みの派生形」）が適用され、三つの誤答は 長短(投=トウ／ト)×清濁(手=シュ／ジュ) の完全な2×2。**公式 7/2025 問題1-4 起床→きしょう/ぎしょう/きしょ/ぎしょ と構造が同一**。キーに拗音「しゅ」あり＝reading trap 保持。stem「兄は野球部で投手を務めている。」15字、常体、「投手を務める」は実在連語 | — |
| 問題1 全体 | — | OK | 訓読み **1/5**（伸ばす のみ）＝band 1–2（gate `問題1 訓読み mix (1 of 5, band 1-2)` ok）。round 1 は 2/5（慌てる＋伸ばす）だったので、再抽選で band の下端へ移動したが逸脱していない | — |

### 問題5 (言い換え類義) — F1 (item 21 re-drawn)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題5-21 | 4 | **OK（修理検証済み）** | 「駅から近いのに、この町の家賃は**案外**安い。」→思ったより。四択とも「N＋より」の比較基準句＝**一つの機能カテゴリ**（2b 充足、3:1 のトーン分割なし）。置換テスト: 四択とも文として成立し、選別は意味のみ。✗理由は三つとも別軸（1 別の場所／2 別の時点／3 全体をならした数値）。stem の「のに」は 案外 が反する期待を立てる節で、公式 7/2025 問題5-23「教室がやかましくて、勉強に集中できない。」と同型 | — |
| 問題5-22 | 3 | OK | わびた→謝った。未変更 | — |
| 問題5-23 | 2 | OK | 混雑して→込んで。未変更 | — |
| 問題5-24 | 4 | OK | つねに→絶えず。未変更 | — |
| 問題5-25 | 3 | OK | とっくに→もう。未変更 | — |
| 問題5 全体 | — | OK | ハード語の帯: **案外 は N2**（§4 F-none の証拠表を参照）。問題1/2/5 stem 読点なし率が 100 %→**93 %** に移動（下記 §5）。唯一最長キー 0/5 | — |

### 問題8 (文の組み立て) — F5 (43 と 47 の解説を書き直し)

四枚の語尾を列に書き出して「…だけ」型の主張を全項目で検算した
（`exam-qa-review` §3 の 2026-09-14 追加行）:

| 項目 | 四枚の語尾 | 解説の主張 | 検算 |
|---|---|---|---|
| 43 | と / 辞書形 / という / 辞書形 | 「辞書形は**二枚**あり、形だけでは決まらない」 | **真**（2枚）— 偽の「だけ」節は削除済み |
| 44 | た形 / と / を / ている | 引用の「と」で終わるのは おかげだと のみ | **真**（1枚） |
| 45 | まで / に / た / 辞書形 | 「辞書形で終わるのは『足をのばす』だけ」 | **真**（1枚） |
| 46 | に / て / で / ます | 「に」で終わるのは お示しした日程に のみ | **真**（1枚） |
| 47 | ほど / ない / 連体形 / 連体形 | 「連体形は**二枚**あり、形では決まらない」 | **真**（2枚） |

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題8-43 | 3 | **OK（修理検証済み）** | 2→1→**3**→4＝「一か所でも弾けるようになると、もっと練習したいという意欲が湧いてくるから不思議だ。」 round 1 が偽と判定した「辞書形で終わるのは『一か所でも弾ける』だけ」は**削除され**、解説は今「辞書形は二枚あり形だけでは決まらない」と自認したうえで、(a)「ようになると」は条件の「と」止まりで「から不思議だ」の直前に立てない、(b)「という」は同格で直後に「意欲」を呼ぶ、(c) 残る「一か所でも弾ける」を末尾に置くと〜ようになる の共起制約と「やめようかと思っていたのに…不思議だ」が指す反転に反する、の三段で末尾を決めている。`verify_scramble`: FREE UNITS 1、ARTIFACT ok、RESULT UNDECIDED（機械は一意性を決めない、と自ら述べる） | — |
| 問題8-44 | 2 | OK | 3→1→**2**→4。「と」止まりは おかげだと の一枚のみ＝引用連鎖が全体を固定。未変更 | — |
| 問題8-45 | 4 | OK | 2→1→**4**→3。「だけ」主張は真（上表）。未変更 | — |
| 問題8-46 | 2 | OK | 3→1→**2**→4。rival を明示して意味側で排除済み。未変更 | — |
| 問題8-47 | 4 | **OK（修理検証済み）** | 3→1→**4**→2＝「帰って子どもの寝顔を見るときほど心のほどける時間はない。」 解説は連体形が二枚あることを認めたうえで、**入替（4→1→3→2, ★=3）を文字列で引用して**排除する: 「心のほどけるときほど帰って子どもの寝顔を見る時間はない」は「AほどBはない」の比較軸が立たず、かつ「嫌なことが続いた日でも」が求める救いではなく不満になる。round 1 が要求した一文が入っている。裸の が／は 止まりカードなし＝zero-anaphora 二重束縛の余地なし | — |
| 問題8 全体 | — | OK | 5項目とも FREE UNITS 1 / ARTIFACT ok。解説長 379–604字（他27紙の 問題8 解説は n=185, 中央154, 範囲41–1002）＝帯外れなし。`.md` の解説欄に terseness band は無く（band は `詳細解説.json` のもの）、gate の `詳細解説.json inside the terseness bands` は ok | — |

### 聴解問題2 (composed) — F4 (6番の末尾設問文)

| 項目 | 鍵 | 判定 | 決め手 |
|---|---|---|---|
| 聴解問題2-1番 | 3 | OK | 男「学校や絵画教室でも指導経験がない人はちょっとね」「経験の有無は譲れないよ」 |
| 聴解問題2-2番 | 2 | OK | 女2「自分でやったら切りすぎちゃって…こんなんじゃ、みんなに笑われちゃうよ」（けんかは「きのうの夜、電話で仲直りした」で消去、試験は「ちゃんと勉強したんだから」で消去） |
| 聴解問題2-3番 | 2 | OK | 男「この前の健康診断で筋肉を増やしたほうがいいって言われたんだ」（ダイエットは「というか」で否定、景色・寄り道は「まあ、それに」の付け足し） |
| 聴解問題2-4番 | 1 | OK | 「自分が卒業した高校のサッカー部…そこで、コーチの仕事をする機会を得ました」（プロは「大学までは」＝過去） |
| 聴解問題2-5番 | 2 | OK | 「私自身は流れてきた木の枝を拾って、テーブルや椅子なんかを作っています」（アクセサリーは「作る人が多い」＝他人、貝の研究は「私の友人」） |
| 聴解問題2-6番 | 3 | **OK（修理検証済み）** | 冒頭・末尾とも「講師は防災グッズに関して一番大切な**こと**は何だと言っていますか。」で**一致**。鍵は「災害の際にちゃんと使うことができて、初めて意味がある」。印刷選択肢は四つとも「〜こと」で終わり、設問の「こと」を**第四の証人**として裏づける |

## 4. The three escalated judgement calls

### 1. `投手` — zero hits across five corpora. **RULED: accepted, in band, not off-shape.**

The reasoning the repair context gave is right, and here is the measurement that
settles it rather than the argument:

**The attestation proxy is refuted by official's own targets.** Grepping each
word against `refs/Hajimete/vocab_reference.md`, `refs/Shinkanzen/goi_reference.md`,
`refs/Soumatome/goi_reference.md` and all 31 `refs/JLPT_N2_NEW/*/booklet.md`:

| word | Hajimete | ShinKanzen 語彙 | Soumatome 語彙 | official | what it is |
|---|---|---|---|---|---|
| **刑事** | 0 | 0 | 0 | 1 | **official 7/2025 問題1-3's own TARGET** |
| **視察** | 0 | 0 | 0 | 3 | official 7/2025 問題2-8's own target |
| 湿る | 0 | 0 | 0 | 0 | official 7/2025 問題2-6's own target |
| **投手** | 0 | 0 | 0 | 0 | this paper's 問題1-5 |
| 起床 | 6 | 0 | 0 | 1 | official 7/2025 問題1-4 |

A rule that reads "0/0/0/0 ⇒ off-band" fails **three of ten** current-era 問題1/2
official targets, including the occupation noun 「私の友人は刑事です。」 —
15 chars, です・ます, everyday word, 2×2 grid け/か × いじ/んじ. The proxy is
refuted, exactly as `moji-goi.md` §"The KEY must be N2" already says
(*"absence is not evidence of absence, and by exactly the same token presence is
not evidence of presence"*).

**The positive evidence, with the hit lines read** (the §2.5 requirement):

- `refs/Shinkanzen/kanji_tables.md` L3617–3621, entry **#475**:
  「投　トウ　…　なげる　投げる（他）　第23回」 — 投 is a **Shin Kanzen N2-漢字
  headword** with the reading トウ, taught in 第23回. Not a fragment, not OCR
  noise: it sits in a numbered column between #474 当 and #476 島.
- 投 in the archive: 投票 ×5, 投函 ×2 — the トウ reading is attested in official ink.
- **The one POSITIVE band test the skill names returns nothing against it.** 投手
  has 0 archive occurrences, so there is no 「（注N）投手：…」 anywhere — unlike
  自ずから, where the おのず family occurred 4 times and was glossed 4/4, which is
  what made round 1's F1 decidable. Absence of the gloss signal is not proof, but
  the signal that condemned 自ずから is simply not present here.
- **Shape precedent is exact**: official 7/2025 問題1-4 keys 起床 against
  きしょう/ぎしょう/きしょ/ぎしょ — 長短 on kanji 1 × 清濁 on kanji 2, three
  non-word derivations of the key's own reading. 投手 → としゅ/とうじゅ/とじゅ/とうしゅ
  is the same grid on the same two axes. `moji-goi.md` §RESOLVE step 6 permits
  exactly this for a 音読み compound.

Not TOO_EASY either: the tested discrimination is トウ-not-ト plus シュ-not-ジュ,
the same order of difficulty as けいじ-not-けんじ. It is not an N3-or-below headline
word of the 賢い/治す/スカート class the skill names.

### 2. `とばす` ⊂ `けとばす`. **RULED: accepted.**

No rule in `moji-goi.md`, `exam-qa-review` or `check_consistency.py` forbids a
substring relation inside one option set (grepped; the only adjacent rule,
§"N options, N different words", is scoped to *two different items of one 大問*
and the gate reads it that way — `no word appears twice in one 大問's options` ok).

**The cited precedent is weaker than claimed, and a stronger one exists.**
7/2023 問題1-2 is 乱れて → くずれて/**あれて**/**あばれて**/みだれて; あれて is a
*subsequence* of あばれて, not a contiguous substring, so it does not carry the
claim on its own. Measured instead over every all-kana 4-option set in the 31
booklets (n=310): **25 sets (8.1 %) contain a proper substring pair.** Most are
the 2×2 grid's own arithmetic (きしょ⊂きしょう, さいど⊂さいどう…), but official
7/2012 問題4 prints 「だいて / いだいて / かかえて / だきしめて」 — two distinct
real words in one set where one is a contiguous substring of the other, and one
fact (抱く reads だく and いだく) touches both.

**And the objection does not cash out here.** 問題1 is solved positively: the
candidate must know 伸＝の. Elimination via 飛ばす removes options 2 and 3 and
leaves **ころばす vs のばす**, a 2-way choice — the shared knowledge does not
deliver the key. Applying the skill's own on-sight test (cover the kanji, keep
the okurigana: 「私は毎晩足を◻ばす体操をします。」) at least two options still fit
(のばす, けとばす), so nothing is uniquely selected by the printed form.

### 3. The semantic-field labels. **RULED: both labels hold; on the ✗ reasons, one yes and one qualified.**

**問題1-2, `field=物や体に力を加えて動かす`** — holds for all four: 転ばす (knock
over → move), 飛ばす (send flying), 蹴飛ばす (kick away), 伸ばす (pull out
longer). All four are transitive 五段 verbs in 〜ばす sharing the printed
okurigana. This is the branch-(b) shape official uses (7/2025 収まった →
さだまった/しずまった/やすまった, field = 落ち着く). Round 1's F3 objection
(喜ばす sits in the emotion field) is resolved.

**On "is each ✗ reason genuinely distinct": in 問題1 it cannot be, and the rule
does not ask for it.** Every 漢字読み distractor dies for one reason — it is not
the reading of the printed kanji. The three-different-deaths rule lives in
`moji-goi.md` Part 4 (問題4 文脈規定), not Part 1. What Part 1 requires is a
per-option **source-and-branch line**, and all three carry one, each naming a
different confirmed headword and its attestation:
`転ばす〔常用音訓 転(ころ-ぶ)〕/ 飛ばす〔飛(と-ばす)〕/ 蹴飛ばす〔蹴(け-る)＋飛(と-ばす)〕`.
Checked against the 常用漢字表 音訓: **と-ばす is listed for 飛** and **け-る for 蹴**,
both correct; and the 転ばす line honestly cites ころ-ぶ rather than claiming
ころ-ばす is a 常用音訓 — which it is not. The 解説 is accurate about what it claims.

**問題5-21, `比較の基準を表す「〜より」句`** — holds for all four (都会より /
去年より / 平均より / 思ったより), and here the three ✗ reasons **are** genuinely
distinct, on three different axes: 別の場所 (1), 別の時点 (2), 全体をならした数値 (3).
No 3:1 tone split, no one-clause triple kill (gate `no 問題4–6 解説 eliminates all
three distractors in one clause` ok).

## 5. Repair collateral — what was checked because the repairs could have moved it

| collateral risk | measured | verdict |
|---|---|---|
| an option string now duplicated elsewhere in 問題1–6 | `goi_profile.py`: *repeated option inside one 大問: none*; gate `no word appears twice in one 大問's options` ok | ok |
| **the new KEY string printed elsewhere in the paper** | 「思ったより」 occurs **twice**: 問題5-21 option 4 (the key) and 問題6-30 option 1's sentence 「…思ったより早く終わった。」 | **not a finding** — the rule and the gate are scoped per-大問, these are different 大問, and 問題6-30's sentence does not contain 案外, so it hands a solver nothing. Recorded as S1 below because the reroll had no check for it |
| 問題1/2/5 stem 読点なし率 (round 1 S1: 100 %, above official max 93 %) | **independently recounted, 14/15 = 93.3 %** — 問題5-21's new stem is the only one carrying 「、」. `goi_profile.py --baseline`: official 47–93 % (n=31), current era **60–93 %** (n=7) | **S1 resolved** — inside the band, at its exact ceiling |
| 問題1/2/5 stem median / longest | median **16** (official 15–21.5, current 15–17.5); the new 問題5-21 stem is the longest at 20 chars (official 問題5 stems run 9–31, current 10–23) | ok |
| 問題1–5 register | 8 polite of 25 (current era 16–32 %; this paper 32 %), 1 first-person, 2 institution-actor | ok, at the polite ceiling |
| 問題1 訓読み band | 2/5 → **1/5**; band is 1–2 | ok |
| 問題8 解説 over-running a terseness band | 43=591, 47=604 chars; the other 27 papers' 問題8 解説 run n=185, median 154, range 41–1002. `.md` 解説 cells carry no band; `詳細解説.json inside the terseness bands` ok | ok |
| a 解説 quote that no longer traces | `make findings` → `logs/findings.json` carries **exactly one** record for this test (`kaisetsu_length`, the stage-5 FAIL). No quote-trace record. The unattributed 「解説 quotes trace」 WARN lines in `make check` belong to other tests | ok |
| the false 「辞書形で終わるのは…だけ」 claim surviving anywhere | grepped `.md` and all four HTML: 0 occurrences. The only surviving 「だけ」 claim is 45's, which is true | ok |
| 71 answer positions after two rerolls | re-flattened `answer_positions` in 問題1…問題14 order and diffed against the shipped key table: **71/71, zero mismatches** | ok |
| ledger ↔ spec after the rerolls | seed string, `pools_sha` and all 11 item categories byte-identical | ok |
| `pools.json` after the F1 pool-defect deletion | recomputed sha1[:12] = **`96db386fa22b`** = spec = ledger. 「自ずから(自然と)」 **absent** from `paraphrase` (142 entries). 案外 present. 投手 present in `kanji_reading` (1526 entries) | ok |
| rotation cooldown on the two new draws | 投手 and 案外 appear in none of the previous four papers' `kanji_reading`/`paraphrase`. Gate `rotation claim holds` ok | ok |
| stale strings anywhere in the test folder | 自ずから / 慌てる / 喜ばす: **0** in `.md`, all four HTML, `詳細解説.*`, `test_spec.json` | ok |
| built HTML regenerated from the repaired Markdown | 投手 / けとばす / 案外 present in `言語知識・読解.html`, `解答.html`, `練習.html`; gate `built HTML matches the Markdown it stamps` + `records its source sha` ok | ok |
| 読解 untouched by the repairs | `dokkai_profile.py` reproduces round 1 exactly (6149 JP, 30.3 % kanji, 33.0 median, margin −0.095, top-rank 30.0 %); gate reprints （注N）=32, uniquely-longest 4/20, ratio ≤1.65 | ok |
| `logs/topics.json` notes still quoting live strings | both round-1 quotes re-grepped and present (「出し直しの速さのほうが先に動いていた」 ×2, 「直す手がかりが紙に書いてある場合にだけ」 ×1). All 8 required fields present | ok |

## 6. 聴解 — the six composed-paper checks, re-run in full

The listening half **was** re-composed since round 1, so `exam-qa-review` §4's
"checks 1–6 must be re-run in full" applies. All six were re-run.

1. **No clip repeats the previous paper.** `logs/choukai_draws.json`: 29 item
   clips, **0** shared with `20260911_1` in the same slot **and 0 shared in any
   slot** (the slot-free textbook half included); the 5 section preambles share
   none either. No starvation note. Source mix: official ×18, kanzenmoshi ×6,
   shinkanzen ×2, mimikara ×1, mondaireishuu ×1, soumatome ×1.
2. **Audio round-trip.** `python3 tools/choukai_segment.py tests/20260914_1/聴解.mp3`
   → `ok  20260914_1  44.3 min  LUFS -15.76  問題1:5 問題2:6 問題3:5 問題4:11 問題5:2`
   — **5/6/5/11/2 recovered**, identical to round 1.
3. **Printed options ↔ audio.** 聴解.md is byte-identical to round 1, so the
   printed field did not move. 問題2's six items were re-read line by line against
   the script; every option's content word traces (指導経験→「経験があること」,
   前髪→かみがた, 筋肉を増やす→筋肉をつける, コーチの仕事→高校でサッカーのコーチ,
   テーブルや椅子→家具, 実際に使ってみよう→使ってみること). No 「演技力」-class break.
4. **Keys come from the bank, not from a hand edit.** Verified at the byte level:
   `git diff logs/choukai_bank.json` is **two lines**, both the same こと fix on
   `2022-07:問題2-6`; `git diff tests/imported-n2-2022-07/聴解スクリプト.txt` is
   **one line**, the same fix. `聴解.md` did not move at all.
5. **Key balance.** 問題1 mode 3 (band 2–4) / 問題2 mode 3 (2–4) / 問題3 mode 2
   (2–4) / 問題4 mode 4 (4–7, the arithmetic floor for 11 three-option items) /
   問題5 [2,2,1] mode 2 (1–3) — **all inside the 31-sitting band**.
6. **Every clip read as Japanese.** The opening announcement reads
   「N2聴解。これから、N2の聴解試験を始めます。問題用紙にメモをとってもかまいません。」
   — the 37-paper 「Nに聴解」 typo is absent (0 hits) and the only Latin run in the
   whole script is `N2` ×2. 問題2 and 問題3 were re-read in full from the keyless
   render; the remaining clips are covered by round 1, and the two-line bank diff
   **proves** no other clip's text moved.

**F4 itself is verified, and independently.** The fix is not merely "someone
typed こと": `refs/JLPT_N2_NEW/13. N2 7-2022/script.md` L188 — the item's own
first read — already prints 「一番大切な**こと**は」, and the sole もの is L197, the
解説欄's 「問い …？（正解:３）」 line, which is a 解説 restatement rather than a
transcription of the second read. A **fourth** witness that nobody has cited:
all four printed options end in 「〜こと」 (関心を持つこと / 買いそろえること /
使ってみること / 定期的に見直すこと), so 「一番大切なもの」 would not have matched
its own option field. 詳細解説.json / 練習.html / 解答.html all now print こと and
carry zero もの.

## 7. Findings

| id | 項目 | class | 証拠 | 判定 | 修理 |
|---|---|---|---|---|---|
| **NEW-1** | provenance record | 要修正（記録）— round 1 F6 re-opened by its own fix | `qa/RESUME-20260914_1.md` L33-38 reads 「plus **31** `--reroll-one` invocations — `word_formation:2` ×1 and `reading_topics:9` ×30 … (counted from `test_spec.json`, 2026-09-17)」. `test_spec.json`'s seed string, counted here, holds **34**: `reading_topics:9` ×30, **`paraphrase:0` ×2**, `word_formation:2` ×1, **`kanji_reading:4` ×1`**. The F1/F2 repairs added three invocations after the note was corrected, and the note's own dated "counted from test_spec.json" claim is now false | 未修理（QA は生成物を触らない） | Rewrite that bullet to 「**34** `--reroll-one` invocations — `reading_topics:9` ×30, `paraphrase:0` ×2, `word_formation:2` ×1, `kanji_reading:4` ×1 (問題12 の三度の再執筆と、round 1 F1/F2 の再抽選)」. **Spec and ledger are correct and must not be touched.** Re-derive the count from the spec at the moment of writing, never from this report |
| **NEW-2** | F4 repair completeness (repo-level; **not** a defect of this paper) | 要修正 — bank ↔ paper desync | `exam-qa-review` §4 check 6 prescribes 「upstream → `make choukai-bank` → **re-compose every paper holding that clip**」 and round 1 F4's repair column repeats it. Steps 1–2 were done and `20260914_1` was re-composed; **`20260817_1` and `20260818_1` also draw `2022-07:問題2-6`** and still print 「一番大切な**もの**は何だと言っていますか。」 in `tests/<id>/聴解スクリプト.txt`. Their own gate lines stay green because each MP3 was built from its own stale script. The line ships to candidates through `練習.html`/`模範解答.html` | 未修理 | **CORRECTED 2026-09-17** — this column originally read 「`make mp3 20260817_1 SEED=<its recorded seed>` and the same for `20260818_1`, at the seeds their `logs/choukai_draws.json` entries record」. **That command is destructive and was not run.** A recorded seed does not reproduce a past paper's draw: `usage_counts()` and `previous_slot_clips()` move as later papers are composed, so `make mp3` at the old seed composes a DIFFERENT paper. Measured 2026-09-17 against the tree of that date: `20260817_1` at `19054272` moves **15 of 29 slots and 3 of 5 preambles**, `20260818_1` at `60629400` **17 of 29 and 2 of 5**. The correct repair is `python3 tools/compose_choukai.py <id> --replay --no-audio` for each paper (reuses the recorded draw by construction, keeps the MP3, so no re-upload and no round-trip re-verification are needed). Rule now written in `choukai-audio` Part 0 §"A recorded seed does NOT reproduce a past paper's draw", and `exam-qa-review` §4 check 6's repair line corrected to match. If the re-render is judged too expensive for two shipped papers, reject it explicitly with a reason — do not leave it silent |

**Nothing was repaired by this reviewer**, and `make sample`,
`make model-answer`, `make scaffold-explanations` and `make upload-files` were
not run, per the review brief.

## 8. Root-cause table (§6.5)

| finding | code | 同クラスを示す紙の数 | 所有ファイル | 具体的な提案 |
|---|---|---|---|---|
| **NEW-1** | `PIPELINE-GAP` (not `RULE-IGNORED`) | **3 instances on this one paper**: the original 「four」, round 1 F6's correction to 「31」, and now 「31」-vs-34. ≥2 ⇒ systemic by definition | `.agents/jlpt-test-generation/SKILL.md` (stage ordering) ＋ `tools/check_consistency.py` | Round 1 filed this as `RULE-IGNORED` ("nothing to change"). **That classification is refuted by its own recurrence**: a hand-typed count next to a machine-generated seed string goes stale every time a later stage rerolls, which is exactly what a repair pass does. Two edits: (1) `jlpt-test-generation` — a note may **name** the spec field, never restate a count derived from it; replace the RESUME template's reroll bullet with 「reroll 数は `test_spec.json` の seed 文字列から数えること（この note は数を持たない）」. (2) A gate check, string-decidable: `check_resume_reroll_count()` — parse `reroll-one\(` occurrences in `tests/<id>/test_spec.json`'s seed and compare against any `**N** --reroll-one` figure in `qa/RESUME-<id>.md`; FAIL on disagreement. **Run against its founding case**: on today's tree it fires on `20260914_1` (note 31, spec 34) and on no other id (no other RESUME file states a count in that form) |
| **NEW-2** | `GATE-BLIND` | 2 papers (`20260817_1`, `20260818_1`); the class — a bank repair that stops at the bank — is new, but §4's own repair instruction has named the third step since 2026-09-11 | `tools/check_consistency.py` | Add `check_choukai_script_matches_bank()`: for every composed paper, each clip id in `logs/choukai_draws.json` must have its `logs/choukai_bank.json` `script` body present verbatim in `tests/<id>/聴解スクリプト.txt`. **Already written and run against its founding case during this review** — over all 28 composed papers and 425 bank records it reports **exactly 2 mismatches, `20260817_1 問題2-6` and `20260818_1 問題2-6`, and zero false positives.** This is the only thing standing between "the bank was repaired" and "the papers were repaired"; `check_choukai_mp3_script_sha` compares a paper to its own script and therefore certifies a stale pair as consistent |
| **S1** (record only, no defect) | `GATE-BLIND` | 1 paper | `tools/check_consistency.py` ＋ `.agents/question-authoring/references/moji-goi.md` §"N options, N different words" | 問題5-21's re-drawn key 「思ったより」 is also printed inside 問題6-30's option sentence. The rule and `check_moji_option_reuse` are both scoped **per 大問**, so nothing looked, and on the merits nothing leaks (問題6-30's sentence does not contain 案外). But a reroll lands a key string into a paper that already exists, and no step asks whether the new string is already in print. Cheap addition: extend `check_moji_option_reuse` to WARN (never FAIL) when a 問題1–6 **key** string also occurs anywhere else in 問題1–6, so a reviewer is told to judge it. Measured on this paper it fires once, on this pair |
| **S2** (round-1 S1, now resolved) | — | — | — | Round 1's S1 proposed making the comma-free stem rule two-sided (「archive 全域 47–93 % の外で FAIL、現行 60–93 % の外で WARN」) because four papers sat at 100 %. **This paper moved to 93.3 % as a side effect of the F1 reroll, i.e. it now sits at the ceiling rather than above it**, so the proposal is no longer needed *for this paper* — but it is still unapplied and still blocks the next run under §6.5, and the other three papers (`20260817_1`, `20260827_1`, `20260904_3`) are unchanged at 100 % |

Round 1's F1–F5 root causes (the `check_pool_gloss_band()` proposal, the
branch-(b) field-label procedure, `check_choukai_question_repeat()`, the
`verify_scramble --audit-claims` proposal) are **still unapplied** and still
block the next generation run under §6.5. Two of them are now better motivated,
not worse: the field-label procedure is exactly what the F2/F3 repair had to
invent by hand (`field=…` is written into the 解説 source line for 問題1-2 but
not for 問題1-5, because a 音読み target has no branch-(b) field — that
asymmetry belongs in the rule), and `check_choukai_question_repeat()` would have
found NEW-2's two papers as well as this one.

## 9. Coverage statement

| step | ran on | scope |
|---|---|---|
| 0 blind solve | `qa/20260914_1/keyless.md` (**rebuilt first**) | 問題1, 問題5, 問題8, 聴解問題2 = 21 items, 21/21 agreement |
| 0 strategy passes | — | not re-run; 読解 unchanged, re-verified by `dokkai_profile.py` |
| 1 key-by-key proof | `言語知識・読解.md`, `聴解.md`, `聴解スクリプト.txt` | the same 21 items |
| 2 / 2b distractor hunt | same | the same 21 items → the three rulings in §4 |
| 2.5 level band | `refs/Shinkanzen/kanji_tables.md`, `goi_reference.md`, `refs/Soumatome/goi_reference.md`, `refs/Hajimete/vocab_reference.md`, 31 × `booklet.md` | 投手, 案外, and the five official control words in §4's table — **hit lines opened and quoted**, not grep totals |
| 3 mechanical reads | `goi_profile.py`, `goi_profile.py --baseline`, `dokkai_profile.py`, `lint_draft.py`, `verify_scramble.py`, `choukai_segment.py`, `check_consistency.py`, `check_consistency.py --json` | §5's table |
| 4 聴解 (composed, 6 checks) | all six re-run — §6 | |
| 5 topic table | not rebuilt — no theme moved (§10.2) | |
| 6 provenance | `test_spec.json`, `logs/ledger.json`, `logs/topics.json`, `pools.json` | → NEW-1 |
| 6.5 root cause | §8 | |

**`make check`**: **1 FAIL, 3 WARN, 5 skip** for this test.

- **FAIL** `20260914_1: 詳細解説.json explains every keyed item (30 entries for
  101 keys)` — **expected and correct at this stage.** The 30 present entries are
  the 聴解 ones `make mp3` wrote; the 71 言語知識・読解 entries are stage 5's work,
  which must not run before QA passes (AGENTS.md §5). Not a finding.
- **WARN 1** `errand-rotation compares 1/44 = 2 % keyed` — same disposition as
  round 1: a true coverage warning about `pools.json` metadata, not a defect of
  this paper, and unrepairable from here. Not a false positive.
- **WARN 2** `問題8 form-family compares 1/5 = 20 % tagged` — same class.
  Compensated by hand: the 17 keyed 問題7/8/9 forms are all distinct and the
  gate's `問題7 <-> 問題8 cooldown` compares all 17 tokens, ok.
- **WARN 3** `聴解問題5 repeats a headline theme of 20260911_1 (スポーツ・余暇)` —
  accepted, composed branch of rule 4, unchanged from round 1. The surface is
  `2022-07:問題5-1`, lifted from a real sitting; nobody chose its subject, and the
  only lever is seed-shopping, which `exam-blueprint` rule 4 forbids.
- The repo-wide `every stamped spec's pools_sha matches pools.json` WARN now
  lists `20260911_1` among the superseded ids, which is the expected consequence
  of the F1 pool deletion; `20260914_1`'s own stamp (`96db386fa22b`) is current.
- **skips** — `問題7 form family (0 of 12 tagged)`, `聴解 errand vs 20260911_1`,
  `セクション構成表 cell quotes` (composed paper has none, correctly), `validate_script`,
  `問題5 printing` ×3, `聴解 authoring/register/pacing` (composed), `詳細解説
  scaffold placeholder` (no `模範解答.html` yet). Each is the documented composed/
  imported exemption or a pool-metadata gap; the two that a skip does not clear
  (`問題7 form family`, `聴解 errand`) were covered by hand — 17 distinct keyed
  forms, and the `shapes` column of `logs/topics.json` read against the previous
  paper's.

**`make lint-draft`**: no blocking errors. One WARN,
`[DOKKAI-ABS-QUANT] 「点の数だけで足りる」` in 問題12-66 option 3 — **pre-existing,
judged by hand and not a finding**: the option asserts what B says and cannot be
eliminated without reading B, which is the content-dependent use `dokkai.md`
explicitly permits. The gate's own scan of the same family reports 0 candidates.

## 10. Skips — what this round did NOT do, and why

1. **The 80 untouched items were not re-solved blind.** The review brief required
   reading round 1 in full, which prints their keys, so a second blind solve of
   them would be theatre. Their round-1 rows stand, and I re-verified everything
   about them that a repair could have moved: 71/71 answer positions, the 読解
   profile, the （注N） count, the option-length and longest-key rates, the
   topics.json quotes, the ledger/spec agreement, and the absence of every
   discarded string. Stated here rather than implied (AGENTS.md §0.7).
2. **The whole-paper topic table (§5) was not rebuilt.** No theme moved: 問題1-5
   and 問題5-21 are pool vocabulary items, which carry no `theme`; 問題8's repairs
   touched only 解説 prose; the 聴解 repair changed one word inside one clip's
   tail question. `logs/topics.json`'s rows are unchanged and the gate's five
   theme checks (`themes come from the closed vocabulary`, `no theme on two 読解
   surfaces`, `headline surfaces take five different themes`, `no headline theme
   repeats 20260911_1's`, `at most one repeats 20260910_1's`) are all ok. Round
   1 §6's table stands.
3. **I did not listen to `refs/JLPT_N2_NEW/13. N2 7-2022/13. Nghe N2 T7-2022.mp3`.**
   Round 1 §8.1 named this as the one decisive test for F4 and this environment
   still has no playback or ASR, so I did not run it and I do not claim to know
   what the audio says. What I can state is documentary and is stronger than
   round 1 had: the script PDF's own item line (L188) reads こと, the 解説欄 line
   (L197) is the only もの, and all four printed options end in こと. If a later
   context does listen and the audio says もの, the repair reverses cleanly —
   one line upstream, `make choukai-bank`, re-compose the three papers.
4. **`make choukai-wear` not run.** Known pre-existing non-zero exit (問題3
   textbook half at 4.26 uses/clip against a 4.0 ceiling); it is not a state this
   paper's draw created and the prescribed repair is the
   `archive_bank_expansion.md` queue. No bearing on this verdict.
5. **No repairs applied, and `make sample` / `make model-answer` /
   `make scaffold-explanations` / `make upload-files` not run**, per the brief.
   `make keyless`, `make check`, `make findings`, `make lint-draft`,
   `make verify-scramble` and the three profilers are all read-only or write only
   under `qa/` and `logs/findings.json`.

---

**次の担当者へ**: both findings are one-line record fixes plus one re-compose;
under `jlpt-test-generation`'s stage-4 rule (≤3 findings) they may be applied
directly without a round 3. NEW-1 must be re-derived from `test_spec.json` **at
the moment of writing**, not copied from this report — that is the exact mistake
the finding records, three times over now. NEW-2 touches two other shipped
papers, not this one; if it is deferred, defer it explicitly with a reason. Once
both are closed the paper is ready for stage 5 (`make model-answer 20260914_1`),
whose `詳細解説.json` must carry the **corrected** 問題8-43/47 proofs, not the
superseded ones.

**QA: FAIL (2 findings, 0 automatic)**
