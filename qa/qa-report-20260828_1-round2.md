# QA Report — 20260828_1 — ROUND 2 (fresh-eyes, capped)

Reviewed revision (sha1, raw bytes) — unchanged from round 1 and confirmed
unmoved (re-hashed) at the end of this pass:

- `言語知識・読解.md` = `af50b30ba4d396c87c50cfaf374b441d9002623d`
- `聴解.md` = `ffd4046c6a62758fcbbb2af136dedefddb006922`
- `聴解スクリプト.txt` = `075b55c7164badff07d63bca7bb646f0a47a5ad1`

Timestamp: 2026-08-28. Reviewer: fresh context, authored nothing in this
paper, did not carry forward round 1's answers into my own blind solve.
`make check` entry condition confirmed green (0 FAIL, 214 WARN repo-wide)
before starting. Round 1's report (`qa/qa-report-20260828_1.md`) was read
for context per the task brief, but every one of its six findings was
independently re-derived below from the shipped files, not trusted.

## QA: FAIL (1 finding, 0 automatic) — CAPPED, apply directly, no round 3

**Per AGENTS.md/exam-qa-review's rule: this is round 2 of a 2-round cap for
this paper. This report has 1 finding (0 automatic-fail), which is ≤3, so
the pipeline's exception applies: fix it directly (root-cause, verify
`make check`, sanity-read the diff) — do NOT spawn a third fresh-eyes
round.** All six of round 1's findings (F1–F6) were independently
re-verified and are CONFIRMED FIXED (detail in §1 and the six-item checklist
below). One new, narrower finding survived my own re-derivation of the
closing-move shape column, which round 1 did not build far enough to catch
(see F7).

---

## 1. Blind-solve diff

Solved from `qa/20260828_1/keyless.md` only (render's own sha1[:12]s, matching
the header above: `言語知識・読解.md`=`af50b30ba4d3`, `聴解.md`=`ffd4046c6a62`,
`聴解スクリプト.txt`=`075b55c7164b`). Answered all 101 items before opening
any keyed source file, then diffed against `言語知識・読解.md`/`聴解.md`.

**Mismatches: 0 of 101.** My independent blind pass matched the shipped key
on every single item, including the eleven 問題4 即時応答 items round 1 had
three near-misses on (聴解4-1番/3番/7番) — on this pass I read those three
correctly the first time using the same 誤った前提 (false-premise) pattern
round 1 identified as the paper's consistent distractor device for 問題4, and
independently confirmed items 43–47's ★ positions (43=1, 44=2, 45=4, 46=3,
47=2) by writing out the full sentence for each permutation before opening
the key.

**Blind strategy passes (20 読解 items, my own script, independent
methodology from round 1's — bigram sets computed against each item's own
passage, second-longest by stripped-punctuation character count):**
- Strategy 1 (max passage-bigram overlap, strict tie-break): **5/20 = 25.0%**
  (6/20 = 30.0% if ties are scored leniently)
- Strategy 2 (second-longest option): **6/20 = 30.0%**

Both are comfortably under the 45% automatic-fail ceiling (chance is 25%),
confirming round 1's F2 fix independently — my absolute numbers differ from
round 1's claimed post-fix 20%/25% because of methodology (tie-break rule,
whether option punctuation is stripped before counting length), but the
conclusion — well under 45%, close to chance — replicates under a second,
independently-written script. **Verification item 1: CONFIRMED.**

---

## 2. Per-question walkthrough (all 101 items)

Paper order. Rows matching round 1's key table are marked OK with my own
independently-derived deciding quote (not copied from round 1's report).

### 文字・語彙 (1–30) — all OK, independently confirmed

| 項目 | 鍵 | 判定 | どこが問題か |
|---|---|---|---|
| 問題1-1 | 3 | OK | 下記＝かき、実在語。がぎ/かぎ/がきは非語または別語 |
| 問題1-2 | 1 | OK | 人生＝じんせい |
| 問題1-3 | 4 | OK | 分割＝ぶんかつ |
| 問題1-4 | 2 | OK | 埋め立てる＝うめたてる |
| 問題1-5 | 4 | OK | 追う＝おう |
| 問題2-6 | 4 | OK | 重圧から「かいほう」された＝解放 |
| 問題2-7 | 2 | OK | 冬でも「おんしつ」で育てる＝温室 |
| 問題2-8 | 3 | OK | 銀行で「ひきだす」＝引き出す |
| 問題2-9 | 1 | OK | 薄い紙が「やぶれる」＝破れる |
| 問題2-10 | 1 | OK | 経済発展の「きばん」＝基盤 |
| 問題3-11 | 1 | OK | 0対0のまま迎えた＝後半 |
| 問題3-12 | 3 | OK | 他店より＝低価格（同価格は「より」と統語的に結合しない） |
| 問題3-13 | 2 | OK | そばにいると覚える＝安心感 |
| 問題4-14 | 1 | OK | 偶然出会った＝ばったり |
| 問題4-15 | 2 | OK | ゴロゴロしてばかり＝怠け者 |
| 問題4-16 | 2 | OK | 使い切ってしまう＝金遣いが荒い |
| 問題4-17 | 4 | OK | 騙し取っていた＝詐欺 |
| 問題4-18 | 4 | OK | 一万円当たる＝ついている |
| 問題4-19 | 2 | OK | チェスで＝負かして |
| 問題4-20 | 4 | OK | 続けるうち＝じょじょに |
| 問題5-21 | 3 | OK | じっくり＝よく考えて |
| 問題5-22 | 4 | OK | 単なる＝ただの |
| 問題5-23 | 4 | OK | 愚かだ＝馬鹿げている |
| 問題5-24 | 1 | OK | 情けない＝恥ずかしい |
| 問題5-25 | 2 | OK | しくじる＝失敗する |
| 問題6-26 | 4 | OK | 「新しい案を提案した」が用法として正 |
| 問題6-27 | 4 | OK | 「学費を援助することにした」が正 |
| 問題6-28 | 1 | OK | 「自分のペースで走り続けた」が正 |
| 問題6-29 | 3 | OK | 「海外の農法を取り入れて」が正 |
| 問題6-30 | 3 | OK | 「返済を催促した」が正 |

### 文法 (31–51) — all OK, independently confirmed

| 項目 | 鍵 | 判定 | どこが問題か |
|---|---|---|---|
| 問題7-31 | 1 | OK | 慎重な彼女への強い否定推量＝はずがない |
| 問題7-32 | 2 | OK | 謙譲語「会う」＝お目にかかり |
| 問題7-33 | 4 | OK | 将棋の腕＝にかけては |
| 問題7-34 | 2 | OK | 謙譲語「受ける」＝承りました |
| 問題7-35 | 4 | OK | 義務・不可避＝断らないわけにはいかない |
| 問題7-36 | 2 | OK | 中立的結末＝末に |
| 問題7-37 | 2 | OK | 条件持続＝限り |
| 問題7-38 | 1 | OK | 情報範囲限定＝限りでは |
| 問題7-39 | 4 | OK | 部分否定＝わけではない |
| 問題7-40 | 4 | OK | 納得評価＝だけのことはある |
| 問題7-41 | 3 | OK | 経由・媒介＝を通じて |
| 問題7-42 | 3 | OK | 願望＝てほしいものだ |
| 問題8-43 | ★=1 | OK | 長年の(3)→親友からの忠告(2)→だった(1)→としても(4)。だ述語の後方拘束＋逆接末尾ロックで一意 |
| 問題8-44 | ★=2 | OK | 気軽に引き受けた(3)→仕事が(4)→予想以上に大変だった(2)→ばかりに(1)。主語衝突回避で一意 |
| 問題8-45 | ★=4 | OK | 資格を取った(3)→だけの人が(2)→優秀だ(4)→からといって(1)。連体修飾＋述語拘束で一意 |
| 問題8-46 | ★=3 | OK (re-verified, F3) | 後輩の指導に(2)→気を配るだけでなく(4)→自分の仕事も(3)→こなしながら(1)。「AだけでなくBも」は日本語の固定語順の相関表現で、B（も）がA（だけでなく）に先行することはできない（も に前方の対比対象が存在しない）。両順序を実際に書き出して検証済み — 逆順「自分の仕事もこなしながら、後輩の指導に気を配るだけでなく」は、だけでなく...も の相関ペアの語順を破壊しており、20260827_2 の主語ゼロ照応の事例（が/はは自由に前方参照できる）とは異なる、固定された語彙的相関構造 |
| 問題8-47 | ★=2 | OK (re-verified, F4) | 資源が限られている(3)→状況において(1)→それだけに効率的な運用が(2)→求められるため(4)。指示語「それ」は逆参照専用（カタフォラ不可）— こそあど体系でそれは既出情報にしか係れないという確立した文法事実で、これは 46 とは異なる、より強い制約 |
| 問題9-48 | 3 | OK | 対策を記録し始めた転換＝そこで |
| 問題9-49 | 2 | OK | 自問形＝ないだろうか |
| 問題9-50 | 1 | OK | 忘れていたことと対応＝後回しになる |
| 問題9-51 | 1 | OK | 大規模な問題に個人の努力が無力＝焼け石に水 |

### 読解 (52–71) — all OK, independently confirmed

| 項目 | 鍵 | 判定 | どこが問題か |
|---|---|---|---|
| 問題10-52 | 4 | OK | 「レベル別3クラス」「少人数制」「10日前までにお申し込み」の複合 |
| 問題10-53 | 3 | OK | 団体可否・空き状況・割引を尋ねている |
| 問題10-54 | 2 | OK | 「見えない粒へと姿を変えながら…残り続ける」 |
| 問題10-55 | 1 | OK | 「定年退職後の住民が…運営側に回る」 |
| 問題10-56 | 3 | OK | 「地盤の成り立ちの違いが…被害の出方を左右している」 |
| 問題11-57 | 3 | OK | 「正規の配信サービスに登録する視聴者が増えている」 |
| 問題11-58 | 2 | OK | 最終文「一律に敵視するだけでは…窓口を自ら閉ざしかねない」の言い換え |
| 問題11-59 | 1 | OK | 「行ってよいかどうかという問いは…等閑視されがち」 |
| 問題11-60 | 2 | OK | 最終文「実現可能性…だけでは足りず…倫理的な視点こそが…欠かせない」 |
| 問題11-61 | 4 | OK | 「義理の両親が…振る舞いに…細かなずれ」 |
| 問題11-62 | 3 | OK | 最終文「長い時間をかけて少しずつすり合わせていく」 |
| 問題11-63 | 4 | OK | 「歩き始める1歳半から2歳ごろを挙げる回答が多く」 |
| 問題11-64 | 4 | OK (F6 re-verified) | 解説の引用は本文と逐語一致（下記§4参照） |
| 問題12-65 | 2 | OK | A「便利な町」/B「歩いて済むようになり」＝移動が楽になる |
| 問題12-66 | 1 | OK | Aは政策論、Bは心情描写 |
| 問題13-67 | 2 | OK | 「距離が生まれ…打ち解けにくくなる」批判 |
| 問題13-68 | 1 | OK | 「敬語を保った組み合わせの方が…良好な関係が続いている割合が高かった」 |
| 問題13-69 | 4 | OK | 「知り合って間もない…丁寧な言葉遣いという型を保つこと自体が…知恵」 |
| 問題14-70 | 4 | OK | 戸籍謄本は本籍が当市の方のみ→伊藤さんは対象外→写しのみ、南部で可 |
| 問題14-71 | 2 | OK | マイナンバーは東部のみ・要予約 |

### 聴解 (例・1–30) — all OK, independently confirmed

| 項目 | 鍵 | 判定 | どこが問題か |
|---|---|---|---|
| 聴解問題1-れい | 2 | OK | 「先にこちらを書きますね」 |
| 聴解問題1-1番 | 3 | OK | 「もっと上、入力欄のすぐ下に置いてほしい」 |
| 聴解問題1-2番 | 3 | OK | 「十四時で大丈夫か…連絡をくれるかな」 |
| 聴解問題1-3番 | 4 | OK | 「朝食を抜いて…保険証も…忘れずに」 |
| 聴解問題1-4番 | 2 | OK | 「先に、そのチラシの原稿を作っていただけますか」 |
| 聴解問題1-5番 | 2 | OK | 「設置場所の幅と…通路の幅を測っておいて」 |
| 聴解問題2-れい | 4 | OK | 「配達のトラックが…通れなくなる」 |
| 聴解問題2-1番 | 1 | OK | 「雰囲気が変わらないなら、うれしいです」 |
| 聴解問題2-2番 | 2 | OK | 「水分をこまめに取ることの方が大事です」 |
| 聴解問題2-3番 | 3 | OK | 「大規模な改装工事をしていて…営業していない」 |
| 聴解問題2-4番 | 3 | OK | 「まだ出欠のはがきを出してない人には…早く出してほしい」 |
| 聴解問題2-5番 | 2 | OK | 「一人当たりの料金が上がったりしないか、それが一番心配」 |
| 聴解問題2-6番 | 4 | OK | 「屋根付きのエリアと…料金を分けることになった」 |
| 聴解問題3-れい | 1 | OK | 「受け取り開始を早める場合は事前手続きが必要」 |
| 聴解問題3-1番 | 3 | OK | 「深夜便は通常より本数を減らして運行」 |
| 聴解問題3-2番 | 2 | OK (F6 re-verified) | 引用は script と逐語一致（下記§4参照） |
| 聴解問題3-3番 | 2 | OK | 「中央値は…引っ張られにくく」 |
| 聴解問題3-4番 | 1 | OK | 「まず確認するのは、質問の内容を事前にもらえるかどうか」 |
| 聴解問題3-5番 | 3 | OK | 「間違いを恐れずに話せるかどうか」 |
| 聴解問題4-れい | 1 | OK | script-given |
| 聴解問題4-1番 | 3 | OK | サイズ交換は一度のみ→今回は諦める（誤った前提パターンで1を排除） |
| 聴解問題4-2番 | 1 | OK | 「指定席で、窓側の席をお願いします」が直接応答 |
| 聴解問題4-3番 | 1 | OK | 開始時刻を尋ねる＝間接的な承諾（誤った前提パターンで2を排除） |
| 聴解問題4-4番 | 2 | OK | 「水を差す」を正しく認識 |
| 聴解問題4-5番 | 2 | OK | 同じ時間に同意 |
| 聴解問題4-6番 | 3 | OK | 案内に礼を言う |
| 聴解問題4-7番 | 1 | OK | 印刷報告に礼を言う（誤った前提パターンで2を排除） |
| 聴解問題4-8番 | 3 | 検討済み・現状維持 | 自己同定型応答として機能（下記§4参照） |
| 聴解問題4-9番 | 2 | OK | 「僕も全然心当たりがないんだよ」 |
| 聴解問題4-10番 | 1 | OK | 「その件でしたら、存じております」 |
| 聴解問題4-11番 | 1 | OK | 「あいにくですが、その日は実家に帰る予定」 |
| 聴解問題5-1番 | 2 | OK | 「店舗で…撮影して、SNSで流す」に同意 |
| 聴解問題5-2番-質問1 | 3 | OK | 「観光地めぐりの方なら…僕は、そちらにします」 |
| 聴解問題5-2番-質問2 | 1 | OK | 「私は、最初のとおり、温泉ゆったりプランで」 |

---

## 3. Findings table

| # | Item(s) | Class | Evidence | Fix applied or left open |
|---|---|---|---|---|
| **F7** | 問題12(B) closing-move shape, `logs/topics.json`'s `closing_moves` bookkeeping | 要修正 — closing-move shape cap (≤2) actually breached by 1, masked by a mis-tag | The Stage-3 build's own `closing_moves` record (`logs/topics.json`, `20260828_1` entry) tags 問題9=随筆, 問題11(3)=随筆, and **問題12(B)=説明** — reporting only 2 of 13 surfaces on 随筆, inside cap. Re-reading 問題12(B)'s actual final two sentences against `dokkai.md`'s own shape definitions: 「便利さと引き換えに何かを失ったとは思わない。これまでとは違う種類の豊かさに、**今は出会えたと感じている**。」 is a first-person personal realization that generalises without prescribing anything to the reader — the textbook definition of **随筆**, not 説明 (説明 = "explains a mechanism/distinction and stops there", which fits 問題10(3)'s プラスチック分解 passage, not a house-move memoir with no mechanism explained). Worse: 問題12(B)'s closing template (「〜のだと、**今は**…と**感じている**」) is nearly IDENTICAL in skeleton to 問題11(3)'s closing (「〜ものなのだと、**今は**…と**思っている**」) — both are "X なのだと、今は〜(感じて／思って)いる" reflective-realization templates, which is exactly the sentence-template-level collision `dokkai.md` separately bans ("the two sharing a shape must also differ at the SENTENCE-TEMPLATE level"). Correctly re-tagged, 随筆 covers 3 of 13 surfaces (問題9, 問題11(3), 問題12(B)), one over the ≤2-per-shape cap — the exact defect class F5 (round 1) targeted, surviving the round-1 fix because round 1 checked only the narrower literal-marker reframe family (だけでは/こそ/ではなく), not the full 6-shape column the skill's own procedure requires ("write each passage's closing move beside its theme… No more than two passages may share one shape"). I independently re-derived all 13 closings from the shipped final sentences before consulting `logs/topics.json`'s self-report, and only two of my 13 labels disagreed with the author's own (問題10(4): I initially over-read it as 主張 via the だけでは-override rule, but on closer reading it opens on a contradicted assumption then explains why — textbook **意外な観察**, matching the author's own tag, so I retract that initial reading; 問題11(1) similarly is 反論応答 [批判もあるが実際には…], matching the author's tag, not 主張 — the だけでは-override in `dokkai.md` is scoped narrowly to the 主張-vs-条件提示 boundary and does not apply to passages that were never 条件提示 candidates). Only 問題12(B) survives as a genuine mis-tag. | **Left open** (this round's only finding; ≤3, apply directly per the pipeline exception — see verdict). Fix: re-tag 問題12(B)'s `closing_moves` entry from 説明 to 随筆 in `logs/topics.json` (bookkeeping only — the passage itself does not need rewriting to be truthfully re-tagged, since re-tagging alone would then correctly flag the cap breach); the SUBSTANTIVE fix is to rewrite ONE of {問題9, 問題11(3), 問題12(B)}'s closing to a different one of the six named shapes (or to a template clearly distinct from "Xなのだと、今は〜ている") — 問題12(B) is the cheapest to rewrite since its passage's own content (a house-move essay) does not require the "今は…と感じている" ending; e.g. close instead on a concrete comparison (「もっと早く決めればよかったと思う」 type is banned by the override rule's genre carve-out only if argumentative; a simple factual close about what changed avoids 随筆 entirely). Re-run the closing-move column and `make check`'s `check_dokkai_final_sentence_templates`/`check_dokkai_rhetorical_monotony` after. |

**No other findings.** F1 (headline-theme collision), F2 (blind-strategy
>45%), F3 (問題8-46 second ★), F4 (問題8-47 flagged), F6 (quote hygiene, 2 of
4 real quotes) are all independently CONFIRMED FIXED below (§ numbered
checklist). No new automatic-fail condition found anywhere in the 101-item
walkthrough, the two-answer hunt, distractor plausibility, level-band spot
checks, 問題1/2 real-word/reading-pair/okurigana rules, 問題14's ≥2-constraint
rule, 聴解 1–3 distractor grounding (every wrong option traced to a script
line), 聴解 narration/voice/SPEAKER_MAP consistency (text-level; MP3 not
re-listened, see Skips), 問題9 blank-category distinctness, grammar-point
single-key-per-paper, or 問題5-2番 printing/order rules.

---

## 4. The six numbered verification items — explicit status

1. **Blind mechanical strategies re-run independently (own script, not
   round 1's).** Strategy 1 = 5/20 (25.0%, 6/20=30.0% lenient); Strategy 2 =
   6/20 (30.0%). Both well under the 45% ceiling. **CONFIRMED.**
2. **問題8-46/47 rival orderings written out by hand.** For 46, the only
   candidate rival is the block-swap [3,1,2,4] (自分の仕事もこなしながら、
   後輩の指導に気を配るだけでなく、着実に成果を上げている). I initially
   suspected this was equally grammatical (the same zero-anaphora class as
   `20260827_2`'s precedent), but on writing out the full sentence and
   testing whether 「も」 in 「自分の仕事も」 has any established antecedent
   when placed first, it does not — 「AだけでなくBも」 is a FIXED bipartite
   Japanese correlative (unlike free subject zero-anaphora), and reversing
   it is a textbook ungrammatical/anomalous reordering, not merely a
   dispreferred one. For 47, the only rival is [2,4,3,1]-style reordering,
   which fails immediately because 「それだけに」's 「それ」 is a
   backward-reference-only demonstrative (こそあど system: それ cannot be
   used cataphorically) — placing that block first leaves 「それ」 with
   nothing to refer to. Both orders are now uniquely determined. **F3 and F4
   CONFIRMED fixed** — no second defensible ★ in either item.
3. **問題9 and 問題13 fresh content review.** Both blind-solved cleanly (no
   mismatch, §1). Distractors: 問題9's four blanks test four distinct
   categories (論理接続/文末モーダル/内容推論/慣用句), none eliminable on
   sight. 問題13's four options per item are genuine paraphrase competitors,
   none an absolute-quantifier freebie. Level band: vocabulary
   (焼け石に水, 等閑視 registered via注, 目算) sits inside N2–N2+ band, no
   N1-headline-only or N4/N5 giveaway. **CONFIRMED sound.**
4. **Headline-theme set vs. `20260827_2` and `20260827_1`**, rebuilt from
   `logs/topics.json` myself (not trusted from the gate's "ok" line alone):
   this test's set = {睡眠・健康, 住まい, 文化・伝統, 行政・手続き, 働き方,
   旅行・観光}; `20260827_2`'s = {メディア・情報, 環境, 医療・福祉, 防災, 食,
   スポーツ・余暇} — **zero intersection**. `20260827_1`'s = {環境, 防災,
   メディア・情報, デジタル化, 交通, 行政・手続き} — **exactly one**
   intersection (行政・手続き). **CONFIRMED**: zero-tolerance rule satisfied
   against the immediately-previous test, at-most-one rule satisfied against
   two-back.
5. **Closing-move shape distribution, re-derived from the 13 actual final
   sentences, not from `logs/topics.json`'s self-report.** Result: 主張×2
   (問題11(2), 問題12(A)), 条件提示×1 (問題10(5)), 意外な観察×2 (問題10(4),
   問題11(4)), 反論応答×2 (問題11(1), 問題13), 説明×1 (問題10(3)), 随筆×3
   (問題9, 問題11(3), **問題12(B)**), 実用文・分類外×3 (問題10(1),
   問題10(2), 問題14). **One cap breach found: 随筆 at 3 of 13, one over the
   limit — filed as F7.** This is narrower than what round 1 fixed (round 1
   only tracked the literal だけでは/こそ/ではなく reframe family, which is
   correctly down to 2/13) but the skill's full 6-shape procedure was never
   completed, and it catches this one.
6. **問題11-64 and 聴解問題3-2番 quotes spot-checked against source.** Item
   64's 解説 now reads 「当初は…出産直後の身体的負担を軽減することが最も求められる
   支援だろうと目算されていましたが、実際に家庭が切実に助けを必要としていたのは
   …動き回るようになった時期だった」 — every substring between the ellipses is a
   byte-exact match against `言語知識・読解.md` line 337 (previously
   truncated mid-word at 「目算さ…」; now complete and correct).
   聴解問題3-2番's 解説 now reads 「一人で黙々と通っていた会員ほど早くやめてしまう
   傾向がはっきりと出ています」, an exact match to `聴解スクリプト.txt` line 190
   (previously dropped 「てしまう」／「と」). **Both CONFIRMED fixed,
   verbatim.**

---

## 5. Side effects named in the fix reports — re-verified independently

- **Kanji density**: gate reports 34.0% (target 24–32%, hard band ≤34%) —
  confirmed at the boundary of the hard band, not breaching it; matches the
  claimed "34.3% → trimmed to 34.0%" narrative (WARN, not FAIL, not
  escalated — consistent with round 1).
- **Key-rank-dominant-share**: gate reports rank 3 = 50% of 20 items (WARN
  ceiling 45%, hard FAIL ceiling 60%, official's own observed max is 56%
  per the check's docstring). 50% sits inside official's own observed range
  and under the hard FAIL line. Not escalated, consistent with round 1's
  judgment that this is an acceptable byproduct of the F2 distractor
  lengthening.
- **Duplicate grammar-point / other side-effect fixes** mentioned in Stage-3's
  own notes (logs/topics.json) — verified against `make check`'s green
  9/9-clean grammar-exposure lines ("no 問題7/8/9 keyed form appears more
  than 1× in the 問題10-14 prose" = ok) — no residual collision found.

---

## 6. Root-cause table

| Finding | Root cause | Recurrence | Owning file | Proposed edit |
|---|---|---|---|---|
| F7 (随筆 shape at 3/13 via a mis-tagged 問題12(B)) | **RULE-IGNORED + GATE-BLIND.** `dokkai.md` §"Thirteen surfaces" explicitly instructs "write the thirteen FINAL SENTENCES out in one column before finalising and read them down the column… Normalise each final to its template" — this procedure was not completed for the F5 fix; only the literal reframe-marker family was re-measured. No check in `check_consistency.py` computes the SIX shapes at all (only the narrower literal reframe/template string families) — a shape assignment is currently unverifiable except by a human building the column, and the human (Stage-3, then round-1 QA) both stopped at the literal-marker layer. | 2nd occurrence of "the ≤2-per-shape cap survives on paper via `logs/topics.json`'s tags disagreeing with a hand re-read of the shipped final sentences" (1st: `20260817_3`, cited in `dokkai.md` itself — "labelled its thirteen surfaces across six shapes, ≤2 each, every label defensible, and still shipped five finals on one skeleton"). Systemic by the recurrence test. | `question-authoring/references/dokkai.md` (authoring procedure already exists but is skippable) + `tools/check_consistency.py` (no gate check exists for the 6-shape distribution at all, only for the literal reframe/template string families) | Add a `check_dokkai_closing_shape_cap()` to `check_consistency.py` that reads the SAME `closing_moves` dict already recorded in `logs/topics.json` and FAILs/WARNs if any of the six shape values appears >2 times among the 13 axis-2 rows (問題12 A/B split) — this at least catches a self-consistent OVER-cap even though it cannot verify the tag itself is truthful. Separately, since the tag's TRUTHFULNESS is exactly what broke here, `jlpt-test-generation`'s Stage-3 checklist should require the closing-move column to be built by re-reading the shipped final sentences AFTER all content fixes land (not before, and not carried over from an earlier draft), immediately before the `logs/topics.json` write — this is a process-ordering gap (`PIPELINE-GAP`) as much as a rule-ignored gap, since 問題12(B)'s content itself may have shifted during the F1/F2 fix passes without its `closing_moves` tag being re-read afterward. |
| (Confirms, no new root cause) F1–F4, F6 fixes | N/A — verified sound on independent re-derivation, nothing to add | — | — | — |

---

## 7. Coverage statement

- **Step 0 (blind solve):** ran on all 101 items from `qa/20260828_1/keyless.md`
  only, zero mismatches; two independent blind-strategy scripts run (§1).
- **Step 1 (key-by-key proof):** ran on all 101 items, every row carries an
  independently-derived deciding quote (§2).
- **Step 2/2b (distractor elimination & plausibility):** ran during blind
  solve and walkthrough; no eliminable-on-sight distractor and no
  unrelated-category distractor found on this pass, matching round 1.
- **Step 2.5 (level band):** spot-checked all 30 文字・語彙 keys plus 問題9's
  cloze vocabulary and 問題13's register against Shin Kanzen/Soumatome
  domain-fit judgment; no off-level key found.
- **Step 3 (mechanical reads):** all `make check` WARN lines for this test
  reproduced and read; F7 aside, none reclassified from round 1's
  resolutions (問題6 option-length, 問題1/2/5 stem shape,指示語 stems=0,
  first-person/polite-voice register, sentence-rhythm, 問題10-14
  absolute-quantifier candidates, option-length ratios, 問題1/2 script-overlap
  15% — all re-read by eye where a candidate existed, no finding beyond what
  round 1 already logged as noted-not-escalated).
- **Step 4 (聴解 structure):** セクション構成表 read as columns for all five
  大問; 決め手の種類 caps (6 rows/7 rows, each token ≤2) cross-checked against
  the actual script content — compliant. Every 問題1–3 wrong option traced
  to a script line during the walkthrough. 問題4-8番 addressee question
  re-examined independently (§ below) — judged functional, matching round
  1's conclusion.
- **Step 5 (whole-paper & cross-test topic table):** rebuilt independently
  from `logs/topics.json` for this test, `20260827_1`, `20260827_2` — zero
  collision against immediately-previous, exactly one against two-back
  (both confirmed, §4 item 4). No within-paper 読解 theme repeat (13
  distinct). Closing-move column rebuilt from the 13 actual final sentences
  — **F7 found** (随筆 at 3/13). No 聴解 item runs the same specific errand as
  another in this paper or the previous two (ledger-verified by the gate,
  spot-checked by eye for 聴解問題1-4番/1-5番 which share a broad 住まい tag
  but are unrelated errands — mailbox installation vs. appliance delivery).
- **Step 6 (provenance & spec audit):** `answer_positions` cross-checked
  against every keyed row in the walkthrough — 100% match. Gate's own
  provenance lines (`test_spec records the rotation it was drawn under`,
  `ledger history entry records the same draw`, `every theme recorded in
  test_spec/ledger agrees with logs/topics.json or says why`) all green;
  spot-read `logs/topics.json`'s Stage-3 `notes` field in full and confirmed
  every quoted claim in it against the shipped text (percentages, item
  numbers, the 聴解問題3-2番 rewrite claim) — all verifiable, none stale.
- **`問題4-8番` addressee (item 8 in round 1's numbering):** independently
  re-examined. Judged functional — a categorical service announcement
  ("診察券をお持ちでない方は、初めての方窓口へ") that a listener can plausibly
  self-identify into and answer in the first person, distinct from a
  no-reply broadcast (fire alarm, boarding announcement). Concur with round
  1's resolution.
- **`言語知識・読解.md` 解説-quote-not-found WARN for item 56** (`〜以外では
  起こることがない`): traced — this is the reviewer's/author's own bracketed
  paraphrase of option 4's text (「液状化は砂地を埋め立てた土地以外では起こらない
  ということ」), not a claimed passage citation; same GATE-WRONG class as
  round 1's F6(a)/(b) (the quote-verifier cannot distinguish an
  option-paraphrase gloss from a source citation). No item defect; already
  root-caused by round 1, not re-filed here.

---

## 8. Skips

- **Raw MP3 audio was not re-listened to.** Narration/voice/SPEAKER_MAP
  consistency checked against `聴解スクリプト.txt`/`聴解.md` text only. The
  gate's own `聴解.mp3 was built from today's 聴解スクリプト.txt` and `built
  with today's pacing` lines are green, and mtimes confirm the MP3
  postdates the script, so staleness is not suspected — but a wrong TTS
  voice assigned to a correctly-labeled speaker would not surface in a
  text-only pass. Flagging per AGENTS.md §0.7 rather than silently skipping.
- **F7 was NOT fixed by this reviewer** — per the round-2 cap rule, a report
  with ≤3 findings (this one has 1) is meant to be applied directly by
  whoever picks it up next, with the same rigor as any fix, not sent back
  for a third fresh-eyes round. I left it unfixed in the shipped files
  because fixing it crosses into authoring judgment (choosing a
  replacement closing shape for 問題12(B) or another surface) that this
  review pass should hand off explicitly rather than rush. Whoever applies
  it should re-run `make check` and re-read the new closing against all six
  named shapes before considering it done (no further fresh-eyes round
  required per the cap).
