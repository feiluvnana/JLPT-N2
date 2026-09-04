# QA report — 20260904_2, ROUND 2 (fresh eyes, authored nothing, did not run round 1)

Reviewed revision (sha1, raw bytes; re-verified unchanged after the review — the
sources were still throughout, mtimes 22:16–22:32 on 2026-09-04):

- `tests/20260904_2/言語知識・読解.md` = `d6b09c416db06ccdd811bab5e47ec4adb2490aa1`
- `tests/20260904_2/聴解.md`           = `ce48991551fa924356d6f9ce2a072cb47cd87d88`
- `tests/20260904_2/聴解スクリプト.txt` = `61fa39b5d131d6f5f00d66c63a9d05a6cfeec5b9`

Blind-solve render: `qa/20260904_2/keyless.md` = `47fdfbe9de97bf7777d0a848a48d48755156fbf1`
(rebuilt at the start of this pass; its header carries the three shas above, and
they had not moved when the review finished).

Timestamp: 2026-09-04, after the round-1 fix pass.

---

## 1. Verdict

```
QA: FAIL (2 findings, 0 automatic)
```

**Read this line with its content.** Both findings are in EXPLANATORY / AUDIT
artifacts — one misquoted script line in a 構成表 commentary paragraph, one false
premise inside a 問題8 解説's structural proof. **Neither touches a key, an
option, a stem, a passage, a script line, the MP3, the answer sheet or any file
an examinee sees.** All 101 keys are proven, all 101 blind-solved correctly, and
every automatic-fail class in `exam-qa-review` was checked and came back clean.

Per `jlpt-test-generation`'s stage-4 loop rule, **a FAIL round with ≤3 findings
may be fixed directly without a third review**, so this verdict does not force a
disclosed skip — 2 ≤ 3, and the direct-fix path is the sanctioned one. Both
repairs are single-string edits, written out below so they can be applied without
re-deriving anything.

Per the round-2 brief, each finding is labelled explicitly:

| Finding | Blocker on the paper? | Verdict |
|---|---|---|
| R2-F1 — 聴解.md:349 commentary misquotes a script line | **No.** Audit prose only; the paper is correct. | True finding, must be fixed before commit; not a content defect |
| R2-F2 — 問題8-47 解説's 構造 leg is factually false | **No.** The item still has exactly one defensible answer (proof in §3). | True finding, must be fixed before commit; not a two-answer item |

Everything the brief asked me to re-adjudicate independently came back
**verified**: the hand edit to `answer_positions.聴解_問題5` is legal on all four
measures, the 13-final closing column is correct on both the labels and the
skeletons, the 問題7/8/9 keyed-form exposure grep is at **zero** hits in every
frame, the 問題3 key-exclusive-token count is **0** under five extraction
patterns, the 問題5-2番 rewrite genuinely removes the opening-turns shortcut, the
新 WARN on 問題2's 理由 count is inside its own quota, and the MP3 is built from
the shipped script.

---

## 2. Blind-solve diff

**Solved from `qa/20260904_2/keyless.md` and nothing else** — the whole
101-question paper plus the verbatim `聴解スクリプト.txt`, with every key, key
table, marked grid and 解説 column stripped by `strip_key()`. The answer list was
written down in full before any sourced Markdown was opened, then evaluated with
`tools/qa_eval.py`.

```
python3 tools/qa_eval.py tests/20260904_2 --answers "[...101 answers...]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches.** Nothing to resolve as reviewer error, nothing to file as a
second defensible answer or a mis-key. The reviewer's list, in paper order:

```
問1-6   1 3 2 2 4 | 4 1 4 3 2 | 3 4 1 | 1 3 4 4 2 1 2 | 4 1 3 2 3 | 2 4 1 2 4
問7-9   4 1 1 3 4 3 2 1 3 3 4 2 | 1 3 4 3 4 | 4 1 3 2
問10-14 3 1 4 4 2 | 1 4 1 3 2 1 2 2 | 2 4 | 1 3 4 | 3 3
聴解1-5 1 1 2 1 2 | 3 4 3 4 3 1 | 4 2 3 2 3 | 3 2 2 3 3 1 2 1 3 1 2 | 3 1 2
```

### The two mandatory blind-strategy passes (問題10–13, 18 items)

Run before any reasoning about meaning, using `tools/dokkai_profile.py`'s own
`calc_overlap()` / `_opt_len()` so the numbers are the gate's own measurement:

| Strategy | Score | Bar | Official |
|---|---|---|---|
| 1 — pick the option sharing the most character bigrams with its own passage | **4/18 = 22.2 %** | FAIL above 45 % | 32.8 % |
| 2 — pick the second-longest option | **7/18 = 38.9 %** | FAIL above 45 % | 24.6 % |

Both are below chance-plus-noise on strategy 1 and inside the bar on strategy 2.
Supporting numbers, all measured here rather than taken from the gate line:

- **median key−distractor overlap margin = −0.124** (must be ≤ 0; a negative
  margin means the keys share LESS passage surface than the distractors, which is
  the direction the rule wants).
- **(tied-)longest key rate 5/18 = 27.8 %** (target ≤35 %, official 30 %);
  **uniquely longest 4/18 = 22.2 %** (target ≤30 %, official 20 %). The
  uniquely-longest figure is the one nine of eleven shipped papers failed by
  hand; this paper is inside it.
- **Option-length ratio per item, 問題10–13 only** (問題14 exempt — the number is
  `dokkai.md`'s, WARN above 1.65 / FAIL above 2.50, read from the owner as
  required): worst is item 55 at **1.39**, then 68 at 1.35 and 60 at 1.25. Every
  item inside WARN.
- **Key paraphrase, longest common substring key↔passage (items 52–69):** max
  **10 chars** (item 59), median 4.5. The rule fails at LCS ≥20, or ≥15 with the
  LCS covering ≥50 % of the option. Nothing is close. Item **64**, the F6
  re-authored item, sits at LCS 4 / 33 chars — genuinely paraphrased, not a lift.

---

## 3. Per-question walkthrough — all 101 items

`OK` rows carry the deciding quote. Paper order.

### 文字・語彙 (1–30)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 1 しょくにん | OK | 職=ショクのみ、人=ニン/ジン。2×2 {しょく,じょく}×{にん,じん}。3 しょくじん が最強競合（人をジンと読む語が多い）。`職人` は Shin Kanzen N2 漢字表の見出し | — |
| 問題1-2 | 3 こうえん | OK | {こう,ごう}×{えん,いん}。1 こういん=工員/行員、4 ごういん=強引 の実在同音語を混ぜる官製の型。`講演` は goi_reference に2件 | — |
| 問題1-3 | 2 へいかい | OK | {へい,べい}×{かい,がい}。1 へいがい=弊害 が実在語。`閉会` は kanji_tables/Soumatome 双方に出現 | — |
| 問題1-4 | 2 たに | OK | 訓読み目標。さか(坂)/たに(谷)/みね(峰)/おか(丘) は全て常用音訓を持つ同語類の実在語で、非語ゼロ。**`refs/Shinkanzen/kanji_tables.md` L4968「711 谷 / コク / たに：」— N2 漢字巻の見出し項目そのもの**なので TOO_EASY ではない | — |
| 問題1-5 | 4 とうしょ | OK | {とう,どう}×{しょ,じょ}。3 どうしょ=同所 が実在語 | — |
| 問題2-6 | 4 回答 | OK | {回,会}×{答,当}、四字とも常用、`matrix_helper.py --reading かいとう` が Cartesian＋仮名骨格ともに PASS | — |
| 問題2-7 | 1 課程 | OK | {課,科}×{程,定}、仮名骨格 PASS。`課程` は goi_reference に3件 | — |
| 問題2-8 | 4 採用 | OK | {採,彩}×{用,要}、音符「采」共有の視覚類似字。仮名骨格 PASS | — |
| 問題2-9 | 3 収めた | OK | 同訓異字。四字とも常用音訓に「おさ-める」。1 納/2 治/4 修 は対象がそれぞれ 金品・乱れ・学業 で「成功」を取れない | — |
| 問題2-10 | 2 険しい | OK | 音符「僉」系列 {険,検,剣,験}。検・剣・験に訓「けわ」なし。`moji-goi.md` §問題2 が模範として挙げる集合そのもの | — |
| 問題3-11 | 3 同 | OK | 「私と（　）世代」＝比較の相手を要求。各=既出集合の各員、全=全体、両=対の二つ、いずれも「私と」を取れない | — |
| 問題3-12 | 4 率 | OK | 「上がった」が全体に対する比の変化。費（出席に費用は生じない）／差（比較対象が不在）／量（人はかさで測れない） | — |
| 問題3-13 | 1 界 | OK | 「入りました」＝職業世界への加入。場=建物・区画、域=土地・領分、圏=中心を要する範囲 | — |
| 問題4-14 | 1 上旬 | OK | 「三日から五日までの三日間」が固定軸。月末/中旬(11–20)/下旬(21–末) は三日〜五日を含まない。※§7 に難易度の所見 | — |
| 問題4-15 | 3 かかわる | OK | 「多くの人の生活に」が影響の及ぶ先。したがう=規則に従う行為者、まじわる=交差・交際、あてはまる=条件の一致で、いずれも影響関係を表さない。`かかわる` は官製 12/2019・7/2022・7/2023 に出現 | — |
| 問題4-16 | 4 親類 | OK | 「父方の」＝家系のどちら側か、血縁でしか切れない。仲間=行動、近所=場所、知人=面識 | — |
| 問題4-17 | 4 退屈して | OK | 「長い説明が続いたので」が原因を単調さと長さに固定。緊張=失敗不安、遠慮=自分の抑制、感心=内容の質への評価。`退屈` は官製 12/2021・7/2021・12/2022 に出現 | — |
| 問題4-18 | 2 枯れて | OK | 「水をやり忘れて」が失われたものを水分に固定。汚れる=外からの付着、折れる=外力、崩れる=構造物 | — |
| 問題4-19 | 1 手ごろな | OK | 「学生によく売れている」が買い手を固定。派手=見た目、貴重=希少さ、高価=結果と矛盾。`手ごろ` は官製 7/2012・7/2014 に出現 | — |
| 問題4-20 | 2 返品 | OK | 「届いた商品にきずがあったので」が戻す対象を購入品に固定。返信=連絡、返却=借用物、返済=借金。返-接頭の4語で組んだ良い集合 | — |
| 問題5-21 | 4 やめる | OK | 置換「その選手は今年でやめるそうだ。」成立。復帰=向きが逆、休養=復帰前提、転職=継続前提 | — |
| 問題5-22 | 1 偶然 | OK | 置換「駅で偶然昔の友人に会いました。」成立。しばしば=頻度、わざわざ=意図、ようやく=時間。`偶然` は Shinkanzen 漢字表・Soumatome 語彙 双方に出現 | — |
| 問題5-23 | 3 重要な | OK | 置換「その件は重要な問題ではない。」成立。複雑=込み入り方、新しい=時間、個人的=範囲。いずれも程度の軸ではない | — |
| 問題5-24 | 2 すばらしい | OK | 置換「舞台で見たおどりは実にすばらしい。」成立。めずらしい=希少、はげしい=勢い、なつかしい=見る人の思い出 | — |
| 問題5-25 | 3 自分勝手な | OK | 置換「弟は昔から自分勝手なところがある。」成立。大げさ=表現、のんき=心配の少なさ、消極的=積極性の軸 | — |
| 問題6-26 | 2 甚だしい被害 | OK | 甚だしい＝望ましくない程度が度を越す。1 おいしさ＝望ましい性質、3 数の多さ＝「おびただしい」、4 坂の傾き＝「険しい/急な」。いずれも非攻撃的な学習者エラーで、実在コロケーションではない | — |
| 問題6-27 | 4 父を説得して | OK | 1=納得、2=説明、3=向きが逆（説得されて）。目的語が人に限られる点が軸 | — |
| 問題6-28 | 1 失敗するリスク | OK | 2=コスト/費用、3=ストレス、4=チャンス。4 は「〜と考えて、思い切って…した」が行為の理由を要求するのに対し、リスクは避けたい可能性なので理由になれない（§7 に所見） | — |
| 問題6-29 | 2 産地にこだわって | OK | 1=主語は選ぶ人、味そのものは主語にならない、3=「心に引っかかる」、4=自動詞なので「を」を取れない | — |
| 問題6-30 | 4 チケット代を払い戻して | OK | 1=返却、2=払い込む、3=返す。払い戻すは受け取った側が代金を返す向きの語 | — |

**問題6 の集合検査**（`moji-goi.md` Part 6）：どの誤答文も (a) 学習者が実際に犯す
一点破壊であり、(b) 第二の実在コロケーションではなく（甚だしいおいしさ／リスクが
かかる／リスクがたまる／味がこだわる／本を払い戻す、いずれも不成立）、(c) 語形の
tell なし（26 は連体3・終止1 で官製の13%と同率、鍵を選ばせない）。gate 実測 mean
27.9 / median 28 / range 23–32 / 30字超3件 — 目標 mean 23–29・最長≥29・30字超≥2 を
すべて満たす。

### 文法 (31–51)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 4 とは驚いた | OK | 前文が「ばったり会った」と既定事実。1 はずがない＝事実と矛盾、2 ことだろう＝既起の出来事を受けられない、3 ところだった＝未実現 | — |
| 問題7-32 | 1 おかげで | OK | 後件「すぐ慣れた」が良い結果。2 せいで＝悪い結果、3 くせに＝非難対象なし、4 ところで＝無駄という結論を導く | — |
| 問題7-33 | 1 としたら | OK | 「決まる」を仮定して見通しを述べる。2 からといって＝後件に打ち消し必要、3 どころか＝前件否定、4 ものの＝逆接だが食い違いなし | — |
| 問題7-34 | 3 に即して | OK | 「実情」は状態。1 をこめて＝気持ち名詞、2 をきっかけに＝出来事、4 をよそに＝前半と正反対 | — |
| 問題7-35 | 4 だけに | OK | 経験の長さ→当然の帰結。1 わりに＝ずれ不在、2 ばかりか＝別事実の付加、3 とはいえ＝逆接の食い違い不在 | — |
| 問題7-36 | 3 お越しになる | OK | 山田様の動作を高める尊敬語。1 参られる＝謙譲＋尊敬助動詞の誤用、2 お目にかかる＝「会う」の謙譲、4 お越しする＝自分側の謙譲 | — |
| 問題7-37 | 2 に先立って | OK | 展示会の前段階。1 をもとに＝材料、3 のもとで＝影響下、4 にわたって＝期間の長さを要する | — |
| 問題7-38 | 1 つつも | OK | 「知り」＋逆接。2 つつあり＝進行、3 次第＝一回きりの後件、4 がてら＝意図的行動を要求 | — |
| 問題7-39 | 3 に相違ない | OK | 「湯飲みがまだ温かい」が根拠。1 どころではない＝た形に接続不可、2 とは限らない＝例外の指摘、4 わけがない＝根拠と正反対 | — |
| 問題7-40 | 3 と同時に | OK | 二つの効果の並立。1 かたわら＝人の活動、2 あまり＝過度の悪結果、4 うえで＝必要条件 | — |
| 問題7-41 | 4 からして | OK | 人数を手がかりに待ち時間を推す。1 にしては＝ずれ不在、2 をめぐって＝争点、3 にかけては＝能力の分野 | — |
| 問題7-42 | 2 やらあいさつ回りやら | OK | 並立して大変さを示す。1 といい〜といい＝評価述語を要求、3 なり〜なり＝選択、4 につけ〜につけ＝対語を要求 | — |
| 問題8-43 | 1 うれしいことは | OK | 語順 名前を呼んでもらえた(2)→ときほど(4)→**うれしいことは(1)**→なかった(3)。終止形は「なかった」のみ。逆順「うれしいことは…ときほどなかった」は程度比較の読みを強いるが「なかった」は存在の否定なので不成立 — 解説がこの唯一の対抗語順を名指しして排除している。`verify_scramble` FREE UNITS **0** | — |
| 問題8-44 | 3 たまらない様子の | OK | 「たまらない」は「〜てたまらない」の束縛形式で「心配で」と不可分、「たまらない様子の」は連体の「の」なので直後に名詞＝「妹に」のみ。「試験の結果が」は関係節内部の主語で、外の述語「言った」の主語は「母は」なので束縛先がない。FREE UNITS 1 | — |
| 問題8-45 | 4 もっと続けようという | OK | 引用「と」→思考動詞で［3→1］、連体「という」→名詞で［4→2］の二塊。終止形は「意欲が湧いてくる」のみなので［3→1］［4→2］の順に確定。FREE UNITS 1。抽選目標「心理変化(〜意欲が湧いてくる)」を印字通りに実現 | — |
| 問題8-46 | 3 基づいて | OK | 「基づいて」は「〜に基づいて」の束縛形式、「利用者アンケートの」は連体「の」、リード「昨年秋に行った」も連体述語 → ［4→1→3→2］の一本鎖。FREE UNITS 1 | — |
| 問題8-47 | 4 違いに気づかないことなど | **要修正** | **鍵は正しい**（下の証明参照）が、解説の構造欄が「名詞で始まるカードは「父である以上」だけである」と書いている。**「違いに気づかないことなど」も名詞（違い）で始まる**ので、この前提は事実として偽。`tests/20260904_2/言語知識・読解.md` L528 | 当該一文を「名詞で始まるカードは「父である以上」と「違いに気づかないことなど」の二つだが、後者を選ぶと(3)(4)(1)(2)＝「…三十年も聞いてきた違いに気づかないことなど、父である以上、あろうはずがない」となり、理由節「父である以上」が無修飾のまま残って「父であること」が気づける根拠にならない。鍵の語順だけが「三十年も聞いてきた父」という修飾関係を作り、理由節を成立させる」に差し替える |
| 問題9-48 | 4 言いかえれば | OK | [論理接続] 直前三文（市役所と商店会→給水所→案内役）の段階的記述を、後文が一つにまとめ直す。1 しかも＝新事実の付加、2 なぜなら＝「〜からだ」を要求、3 とはいえ＝対立不在 | — |
| 問題9-49 | 1 悩まされずにすむ | OK | [文末モーダル] 「流れができれば」が条件、後件は望ましい結果。2 ほかない＝我慢、3 にすぎない＝過去の評価、4 てばかりいる＝継続で矛盾 | — |
| 問題9-50 | 3 おそれがある | OK | [慣用・形式名詞] 好ましくない可能性。1 きらいがある＝人や物の傾向で事態を受けられない、2 かぎりである＝感情語を要求、3 しだいである＝可能性を述べない | — |
| 問題9-51 | 2 参加者の中に生まれている | OK | [内容推論] 「前の年にコースの脇で名前を呼ばれ、拍手を受けた人が、今度は自分が呼ぶ側に回りたいと思うのである」。1 名簿・登録は本文になし、3 賞品は第三段落と正面から矛盾、4 「呼びかけても、人はなかなか動かない」と逆 | — |

**問題9 の4欄検査**：[論理接続] / [文末モーダル] / [慣用・形式名詞] / [内容推論] の
四カテゴリで重複なし（gate も4種＋内容推論を確認）。cloze 本文 **693 JP字**（目標
500–700 の内側）。選択肢は全て16字以下（官製 current-era 最大14）。

**問題7 の三数**（`bunpou.md` §問題7、片側だけでなく両側）：mean **41.9**（帯
36–52）／34字未満の stem **3本**（必要2本以上）／max−min **39**（必要25以上）。
対話・場面ラベル付き stem も 33・36・41 の3本ある。

### 読解 (52–71)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 3 | OK | 「景色の細かさではなく、そのとき自分がどれだけ心細かったか…という気分のほうであった」＋「場面の細かさを欠いたまま気分だけを連れてくる」。1 は写真側の結果と入れ替え、2 も写真側、4 は「途中の中継の場所を経ないで」と正反対 | — |
| 問題10-53 | 1 | OK | 「一人ずつの申し込みでよいのかどうかを、今週中にお教えいただけないでしょうか」。2 当番の組み直しは尋ねていない、3 配り方は不出、4 「希望する者が何人かおります」と逆 | — |
| 問題10-54 | 4 | OK | 「省かれた手間の中にあったものを数え直さないかぎり、この代償の差し引きは合わないままである」。1 迷う時間は「いっしょに消えている」、2 は「値札の外に置かれたまま」、3 は不出 | — |
| 問題10-55 | 4 | OK | 「作った電気は売らずに…自家消費の形に切りかえます」＋「…六月十日までに配布の用紙で組合までお知らせください」。1 板の撤去は不出、2 各世帯集金は不出、3 発電はやめない | — |
| 問題10-56 | 2 | OK | 「そこには性質の違う二つの手当てが混ざっています」＋「前者は用事の呼びかけを断つ手当てであり、後者は目の反射を断つ手当てです」。1 は前者を後者の目的にすり替え、3 は「気持ちを引きはがします」と逆、4 は「目が自分でそちらを向いてしまいます」と逆 | — |
| 問題11-57 | 1 | OK | 「手元に残るのは食い違う二人の話と、路面の制動痕くらいのもので、どちらがどこで何を見ていたのかは、最後まで分からない」。2 速さは不出、3 作りかえられないのは装置側、4 「むしろ増えている」と逆 | — |
| 問題11-58 | 4 | OK | 「だれの落ち度かを言いあてる材料は、むしろ増えている」＋「問いは前へ動いたのであって、消えたわけではない」。1・4 が正面対立で 4 が本文、2 は「書きとめに残っていても」、3 は過失が問われなくなったとは不出 | — |
| 問題11-59 | 1 | OK | 「差がついていたのは、家族以外の手が最初に入った時期である」。2・3 は「病気の重さでも、同じ家に住む人の数でもなかった」で明示的に除外、4 は疲れの量ではなく時期 | — |
| 問題11-60 | 3 | OK | 「レスパイトの制度は、休むためというより先に、次の潮時を自分で選ぶ余裕を手元に残すためにあると私は思っている」。1 は「選べる先は空いている所にかぎられ」と逆、2 は余裕のあるうちを勧めており逆、4 は「重い」を無くせるとは不出 | — |
| 問題11-61 | 2 | OK | 「来るのは一度きりの人ばかりで」＋「その食堂には、同じ顔が何度も戻ってきていたのです」。1 は「たしかに増えていました」と逆、3 店主は「うちは何も変わっていません」、4 は「道は分かりにくく」と逆 | — |
| 問題11-62 | 1 | OK | 「めずらしさは一度で使い切られるのに対し、店先の立ち話は次に来る理由として残ります」。2 は滝の客が一度きり、3 は分かりにくさが立ち話を生んだので逆、4 は掲載回数と常連の関係は不出 | — |
| 問題11-63 | 2 | OK | 「実家も近く、夫も休みを取ってくれていましたから、こういう所は身寄りの遠い人が使うものだと、私は勝手に決めていたのです」。1・3・4 はいずれも本文にない用途 | — |
| 問題11-64 | 2 | OK | **F6 の再作項目。** 指示語「そのような見守り方」＝直前の「直そうとせずに「その持ち方で大丈夫ですよ」とだけ言って、そのまま黙って見ていてくれました」。鍵の後半は「帰ってからも、直されて手が止まりそうになると、あの朝の光と食器の音が先に浮かびます」。1 は「手が止まりそうになる」と逆、3 は「直そうとせずに」と逆、4 は沐浴を自分でしており逆。**LCS(鍵,本文)=4字/33字**で純粋な抜き出しではない。無標の指示語 stem は官製にも実在（12/2023「そのような状態とあるが」、7/2023「そのようなときとはどのようなときか」ほか） | — |
| 問題12-65 | 2 | OK | A「会議の記録には残らない種類の中身が、そこを通って動いているわけである」／B「立ち話から生まれる仕事の知恵は、会議の場ではまず出てきません」。1 は B のみ、3 は A の一面のみ、4 はどちらも述べていない | — |
| 問題12-66 | 4 | OK | A「話の行き来を早める道具でもあり、その場にいない人を置いていく仕掛けでもある」（両面）／B「席の配置をいじって話の量をふやす前に、話の外に置かれる人がだれかを数えておきたい」（順序）。1 A は席配置を勧めていない、2 どちらも減らせと言わない、3 どちらも職場の中の話 | — |
| 問題13-67 | 1 | OK | 「火事や選挙のような大きな出来事なら、その場に居合わせた何人かが書きこみ、うちの朝刊より早く町中に伝わる」。2・3・4 は「消えたのは、だれも読みたいと言わなかった記事のほうである」に続く消えた側の例 | — |
| 問題13-68 | 3 | OK | ①の直前「どれも、出した日に読まれた覚えがない」＋末尾「なぜうちが後なのかと聞かれても、答えられる人はもういない」。1 書き手の力量は不出、2 選ぶ難しさの話ではない、4 記憶から消えるとは不出 | — |
| 問題13-69 | 4 | OK | 「売っていたのは、だれかがその部屋に常駐していたという事実のほうだった」＋「その持ち場が、紙といっしょになくなった」。1 は「書く人がいなくなったのではない」、2 は不出、3 は「数の上では…むしろ増えたように見える」と逆 | — |
| 問題14-70 | 3 | OK | **2条件以上**：①=「九月三十日までに市のホームページからお申し込みください」＋「市のホームページでお申し込みいただけるのは、①と④に限ります」、③=「②と③は、前もってのお申し込みは要りません。当日、始まる十五分前までに受付へお越しください」。対象条件「市外にお住まいの十八歳以上の方」も高木さん（市外・二十歳）に照合。1 は①が当日不可、2 は③がHP不可、4 は「お電話と窓口では受け付けておりません」 | — |
| 問題14-71 | 3 | OK | **2条件以上**：②千円＋③二千円＝三千円。対象条件（③「中学生以上の方」に中学二年生が該当、②「どなたでも」）も要る。4 は①の三千円を足した額だが、森さんは市内在住で①の対象外なので「①にお申し込みの方は、③に参加費なしで」の適用も受けない — 誘い込みが効いている | — |

**読解の機構検査**：`<ruby>` **0件**（N2 漢字に振り仮名なし）／（注N）**30件**（gate
帯 27–61、床 25）で orphan なし・in-body と定義行が1対1／（中略）**4件**（すべて
問題11–13 の中）／※記号 0件／絶対量化詞・全否定マーカー 0件／マーク①は 68 の
stem と1対1で、太字スパンは指示サイズ。注の見出し語 30 件はいずれも N1・専門・
制度名・慣用（嗅覚／制動痕／逸脱／猶予／過失／予見／ケアマネジャー／疲弊／訪問介護
／レスパイト／潮時／棚田／渡し場／秘境／身寄り／沐浴／助産師／悪気／引け目／廃刊／
審議会／縦覧／老朽／輪番／議事録／常駐／試行／代償／自家消費／視野）で、`dokkai.md`
の禁止リスト（選択・信号・技術・文化・質・準備・手順・設計・現象・経由・偏り・維持・
継続・前提・細部・バランス）に当たるものは一つもない。最も甘いのは **視野** だが、
本文は「視野の端に入る動き」という光学的な語義で使っており、その語義の注記は妥当。

### 聴解 (30 items + 4 例)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 2 | OK | 台本告知「最もよいものは2番です」＝マークシート「1 **(2)** 3 4」。対話も支持：「申請の用紙に、いくつ要るか書いてくれる」→「今から書きます」 | — |
| 問題1-1番 | 1 | OK | 「エプロンとふきんだけは、ご自分のをお持ちください」→「二つとも持っていきます」。2 不要「包丁とまな板は、教室のをお使いいただきます」／3 不要「材料はこちらでそろえますので」／4 別の人に割り当て「持ち帰りの入れ物も、こちらで包んでお渡ししてます」— 三つとも台本に接地 | — |
| 問題1-2番 | 1 | OK | 非対話（留守番電話）。「月曜に間に合うかどうかだけ、今日中にメールでお返事をいただけますか」。2「写真は…送っていただかなくて大丈夫」／3「もう反映して印刷に回してあります」／4「まだ考えていただかなくてけっこうです」 | — |
| 問題1-3番 | 2 | OK | 「木曜は、二時までに帰ってこられれば」→「工事は三時からですから、それなら大丈夫」→「じゃあ、木曜でお願いします」。1「火曜は、朝から出かける用があった」／3「土曜は…もういっぱい」／4「工事が長引いたときだけ」 | — |
| 問題1-4番 | 1 | OK | 「来週、直接持っていくんです。じゃあ、外側に貼ってください」。2「内側だと、渡すときに分かりませんもんね」／3「リボンは…お付けできない」／4「紙袋は、お会計のときにもうお入れしてあります」 | — |
| 問題1-5番 | 2 | OK | 「班のみんなに、当日出られるかどうか、一人ずつ聞いてもらえるかな」→「今日中に回ってみます」。1「消防署への連絡は…分かってからでいい」／3「道具は、署のほうで決めることになってて」／4「一か月前にならないと区の窓口が受け付けてくれない」 | — |
| 問題2-例 | 4 | OK | 告知「最もよいものは4番です」＝マークシート「1 2 3 **(4)**」。「来月の十日に、地図を新しくしたものが出るんです」＋「今回はやめて、来月まで待ちます」 | — |
| 問題2-1番 | 3 | OK | 非対話（駅アナウンス）。「ただいま、部品の取り替えを行っております」＋「運転を再開できますのは、午前十一時ごろ」＝昼前。1「上りも下りも運転を見合わせております」／2 調べる作業は完了だが取り替えはこれから／4「振り替えのバスは…本日は出ておりません」だが電車は再開する | — |
| 問題2-2番 | 4 | OK | 「今回いただくのは、銀行にお届けになっているほうなんです」＋「銀行のは、家に置いてきちゃった」。1「保険証券は…お持ちでなくても大丈夫」／2「通帳は持ってきました」／3「郵送でも受け付けております」＝郵便だけ、を否定 | — |
| 問題2-3番 | 3 | OK | 「途中で、次にどこを押せばいいのか書いてなくて。そこで毎回止まっちゃう」＋「あの紙、機種が変わったのに、絵だけ前のままなんです」。1「電話はすぐつながって、丁寧に教えてもらえました」／2「日本語のところもちゃんとありましたし」／4「それは工事のときに引いてもらいました」 | — |
| 問題2-4番 | 4 | OK | **F4 の再角度づけ項目。** 「そのままにしておきますと、警察が自転車を調べたときに、前の方のところへ連絡が行ってしまうんです」。1「前の方にしていただくことは、何もありません」／2「持ち主が変わったときは、必ず入れ直しです」／3「いえ、前のはそのままで、新しいものを別のところに貼らせていただきます」— 三つとも提示され明示的に否定される。質問型は「何と言っていますか」＝内容・発言で、2番の「どうして」と別（§4に再判定） | — |
| 問題2-5番 | 3 | OK | 「日曜と月曜は休みをいただいてまして、そのあとですと火曜になります」＋「火曜なら、仕事の帰りに寄れます」＋「火曜の六時ごろまでに」。1「かかとだけでしたら、あさっての夕方」＝底の張り替えが加わり不成立／2「土曜は、午後から店を閉めて」／4「じゃあ、早いほうがいいので、火曜にします」で本人が否定 | — |
| 問題2-6番 | 1 | OK | 「三十分ほどで終わりますよ」＋「よかった。今日の午後は、仕事に戻れないと思ってました」。2 うんざりではなく覚悟が外れた／3「はい、それは大丈夫です」＝期限は心配なし／4「去年の分は、会社がお出しになっていますから」 | — |
| 問題3-例 | 3 | OK | 告知3番＝マークシート「1 2 **(3)** 4」。「まず三分、だれとも相談せずに、自分の考えを紙に書いてください」 | — |
| 問題3-1番 | 4 | OK | **F3 の鍵書き換え項目**（「…時こくだけを書く理由」→「…時こくだけにした理由」）。「何を食べたかではなく、何時に食べたかだけを書いてもらいました」／独話は誤答を一つも口にしていない（問題3の設計どおり） | — |
| 問題3-2番 | 2 | OK | 「一つは、いつ書かれたかです」「もう一つは、まちがっていたとき、だれかが直せる場所に置かれているかどうかです」＋「中身を読むのは、そのあとでいいんです」 | — |
| 問題3-3番 | 3 | OK | 「それで、今年から決まりの数を減らしました。二十四あったものを、六つにしました」 | — |
| 問題3-4番 | 2 | OK | **F3 の鍵書き換え項目**（「…勧めるやり方」→「値段を最後に伝える勧め方」）。「最後に、お代はこれだけ下がりますと申し上げる」＋「今も、値段の話は最後にしています」 | — |
| 問題3-5番 | 3 | OK | 「それからは、金額より先に、直しを何回まで受けるかというところをさがすようになりました」 | — |
| 問題4-例 | 1 | OK | 告知1番＝マークシート「**(1)** 2 3」。「明日の集まり、駅の前でいいかな」→「うん、そこにしよう」 | — |
| 問題4-1番 | 3 | OK | 「先方のご都合が悪くなりまして」→「来週の空いている日を聞いてみます」（間接的な返答）。1 立場の逆転、2 時制の誤り | — |
| 問題4-2番 | 2 | OK | 「資料は何部ご用意いたしましょうか」→「来る人が増えたから、十二部お願い」。部長→部下の平体で敬語の向きも正しい。1 立場の逆転、3 既に完了 | — |
| 問題4-3番 | 2 | OK | 「レシートの発行は必要ですか」→「経費で落とすので、いただけますか」。1 対象の取り違え、3 立場の逆転 | — |
| 問題4-4番 | 3 | OK | 「ペットの飼育は規約で禁止されています」→「金魚も、飼ってはいけないんでしょうか」。1 誤った前提、2 対象の取り違え | — |
| 問題4-5番 | 3 | OK | 「皆さんのおかげで無事に終えることができました」→「こちらこそ、いい経験をさせていただきました」。1 時制の誤り、2 誤った前提 | — |
| 問題4-6番 | 1 | OK | 「食事の時間、変更は可能ですか」→「六時か七時でしたら、お選びいただけます」。2 論点のずれ、3 既に完了 | — |
| 問題4-7番 | 2 | OK | keigo 刺激「遠慮なくお申し付けください」→「ありがとうございます。休むところはありますか」。1 立場の逆転、3 論点のずれ | — |
| 問題4-8番 | 1 | OK | 「少し遅れて参加してもよろしいでしょうか」→社長「かまわないよ。先に始めているから」。敬語の向き（社員→社長／社長→社員の平体）正しい。2 誤った前提、3 立場の逆転 | — |
| 問題4-9番 | 3 | OK | casual 刺激「この資料、会議までに目を通しておいてくれるかな」→「うん、昼までには読んでおくよ」。1 は「目を通す」の語義取り違え、2 論点のずれ | — |
| 問題4-10番 | 1 | OK | casual 刺激「作りがいがないよね」→「あとで来るって、みんな言ってたよ」（間接的な返答）。2 論点のずれ、3 誤った前提 | — |
| 問題4-11番 | 2 | OK | **F5 の差し替え項目。** keigo 刺激「社長、本日の業界誌に弊社の記事が掲載されております」→「どのあたりに出ている。持ってきてくれるか」。誤答3も台本に合わせて「業界誌なら、毎月、家に届いているよ」に整合済み。**台本全体で「新聞」は0件**なので、問題13（地方紙の廃刊）との語の重なりも消えている | — |
| 問題5-1番 | 3 | OK | 「発表ごとに取っている質疑の時間を、最後にまとめて一回だけにしませんか」に難点が出るが「質問を紙に書いて出してもらいましょう」で解消され「質疑は最後にまとめる形で進めましょう」。1「二十分は話したいとおっしゃっている」で撤回／2「大きい部屋が一つしか借りられなかったの」／4「夕方は、懇親会の準備で会場が使えないの」 | — |
| 問題5-2番-質問1 | 1 ストレッチ | OK | **F1/F2 の再作項目。** 「そっか。じゃあ、僕はストレッチにしとくよ。土曜の朝なら空いてるし、着替えも道具もいらないっていうのが、いちばん楽でいい」。2「バスに乗ってまで行くとなると、続かなくてさ」／3「うち、七時に上がれる日なんてないよ」／4「それだと、僕が行く意味はないなあ」 | — |
| 問題5-2番-質問2 | 2 プール | OK | 「私はバスでも行くよ。水の中を歩くなら、ひざが痛くても続けられるって言ってたし」＋「先生にも、まず体を動かしなさいって言われてるから、私はプールにする」。1「休みも火曜と木曜だけだから、土曜の朝も無理」／3「私は夜、店を閉めるのが遅いんだ」／4 本人が取り下げ | — |

---

## 4. The seven landing sites, re-verified independently

A repair is not verified by the check it cleared. Every number below was
re-measured in this pass.

### 4.1 F1+F2 — the hand edit to `answer_positions.聴解_問題5` ([3,1,1] → [3,1,2])

The brief flagged this as unverified by any gate. I re-measured all four legality
conditions against `sample_items.py`'s own constants:

| Condition | Constant | Measured | Verdict |
|---|---|---|---|
| Section mode count | `MAX_SECTION_MODE["聴解_問題5"]` = 2 | **1** (3/1/2 all distinct) | inside |
| Mode count is a shape official produces | `SECTION_MODE_DIST["聴解_問題5"]` = `{1: 5, 2: 6}` | mode **1** occurs in 5 of 11 era-matched sittings | **realisable** — not merely under a ceiling |
| Whole-paper 4-choice totals | `POSITION_BAND` = (19, 27) over the 90-item deck | **1:22 / 2:21 / 3:24 / 4:23** (was 23/20/24/23) | inside, and spread narrowed 4→3 |
| Longest same-position run | `MAX_POSITION_RUN` = 3 | **3**, unchanged by the edit | at the cap, legal |
| 聴解問題4 (width-3) untouched | `POSITION_BAND_3` = (2,6), run cap 2 | 3/4/4, run 2 | unchanged |

`section_mode_breaches()` returns **[]** on the shipped plan.

**The premise behind the edit also checks out.** I re-derived it from
`refs/JLPT_N2_NEW/answer_keys.json` rather than accepting the claim: across all
**31** sittings, 聴解問題5's last two keys (質問1/質問2) are **never** equal —
0/31, spanning 7/2010 through 12/2025. The pre-fix `[3,1,1]` reserved a shape
the archive does not contain, so F2 was a real automatic fail and this is the
right repair.

**Recorded in all three files?** Yes, and I read each:
`test_spec.json`'s `spec_notes` narrates the edit with its own re-measurement;
`logs/ledger.json`'s 20260904_2 entry repeats it with the two new deciding lines
quoted verbatim from the shipped script; `logs/topics.json`'s 聴解問題5-2番 row
carries `surfaces`, `themes`, `claim` and `shapes`, all four re-read against the
script below.

### 4.2 F1+F2 — does the 問題5-2番 rewrite actually remove the round-1 defect?

The requirement is that a candidate who hears only the opening turns can answer
**neither** question. Re-read from the script:

- 男's first statement of preference: 「僕は筋力体操かなあ。」 → option **3**.
  Key for 質問1 is **1** (ストレッチ). Wrong.
- 女's first statement of preference: 「私は眠りの講座がいいな。」 → option **4**.
  Key for 質問2 is **2** (プール). Wrong.

Both opening preferences are explicitly withdrawn later, by the speakers
themselves, on stated grounds. A candidate who stops listening after the first
two turns scores **0 of 2**. Defect removed.

Printing rules (`jlpt-exam-structure` §問題5-2番) also re-checked: 問題5 prints no
options at all (both items are spoken); the four course names are read in the
**same order** for 質問1 and 質問2 (ストレッチ/プール/筋力体操/眠り = the
男性職員's own enumeration order); **no deciding attribute is printed beside a
name** (「ストレッチの教室」, not 「ストレッチの教室（土曜の朝）」); the decision is
by name, never by ordinal; and 「質問1。」/「質問2。」 are both spoken, which is what
`make_choukai_mp3.py`'s `GAP_AFTER_SHITSUMON1` keys its 10-second pause off.

### 4.3 F3 — 問題3 key-exclusive tokens, re-measured

I did not accept the 構成表's tally. I re-extracted all **24** spoken 問題3
options from the shipped script and ran the token scan with **five** patterns —
the gate's three (`[一-鿿]{2,}`, `[ァ-ヶー]{2,}`, `[ぁ-ゖ]{4,}`) plus the two the
round-1 report proposed (`[一-鿿][ぁ-ゖ]{1,3}`, `[ぁ-ゖ]{1,3}[一-鿿]`, which are what
catch 「やり方」 and 「書く」):

```
tokens appearing in >=2 KEYS and 0 distractors: 0
```

**Zero.** The six keys now read 話し合う前に一人で書く時間の役わり / 食事の記録を
時こくだけにした理由 / 中身以外で正しさを見分けるやり方 / 決まりの数を六つに減らした
わけ / 値段を最後に伝える勧め方 / 契約書で金額より先に見るところ — 「やり方」 is now
in one key only, 「書く」 in one key only.

**And the repair took the route the rule requires.** I confirmed the reading the
fix pass cited: `choukai-items.md` §問題3 says *"Repair by RE-ANGLING one item's
key, never by giving the word to a distractor"*, and `exam-qa-review` §4 repeats
it. The two changed strings are option texts; **the monologues are unchanged**,
and both re-worded keys still name the talk's actual subject (1番 「何を食べたか
ではなく、何時に食べたかだけを書いてもらいました」; 4番 「今も、値段の話は最後に
しています」). Declining my predecessor's push-it-into-a-distractor suggestion was
correct.

Option lengths are 11–18 chars (24 options), slightly above official's 10–15 band
because the distractors were lengthened rather than the keys trimmed — again the
direction the owner prescribes. 聴解 key-length predictability is measured green:
uniquely-longest **4/30 = 13 %** (target ≤35 %, official 28 %), median
key ÷ distractor-mean **0.97** (official 1.00).

### 4.4 F4 — the re-angle, and the WARN it created

**Re-adjudicated from the owner, not from the fix report.**
`question-authoring/references/choukai-items.md` §"Section item mix" row for
問題2 reads, verbatim:

> `| 2 | 一番/優先 ≤2 **and** 理由 ≤3 of 6 | 5.5% 一番 / 32.6% 理由 | FAIL at >4 on one type |`

It is an **upper bound with no floor**, and the two FAIL conditions on the
section are *>4 on one type* and *0 content items*. The shipped section is
内容・発言 2 / 理由 1 / 一番・優先 1 / その他(いつ) 1 / 気持ち 1 — no type above 2,
content items 2 (the `≥2 of 6` quota, satisfied explicitly by 1番 and 4番 rather
than by a machine classification of 6番), and one 気持ち item (its own `≥1`
quota). **The WARN is a judgment-call line and the judgment is defensible: the
section now spans five question types across six items, which is more varied
than official, not less.** Counting the 例 (どうして), 理由 is 2 of 7 = 29 %, near
official's 37 %.

**Did the re-angle actually separate 4番 from 2番?** Three axes, checked against
the script rather than the table:

| axis | 2番 | 4番 (shipped) | separated? |
|---|---|---|---|
| 質問型 | どうして (「どうして今日は手続きができないのですか」) | 内容・発言 (「前の持ち主の登録について何と言っていますか」) | **yes, unambiguously** |
| 用件の形 | 手続きが前提不足で止まる（はんこ違い） | 手続きはその場で完了し、店員が**放置した場合の帰結**を説明する | **yes, unambiguously** |
| 決め手の種類 | 規則・制度 | 連絡・情報の不足 | **defensible, but the soft half** — 4番's decider could also be read 規則・制度 (「人にゆずるたびに、入れ直していただくことになっています」) |

Even under the stricter reading of the third axis the cap is not breached
(規則・制度 would be 2 rows of 7, ceiling 2), and the listener is genuinely doing
two different jobs: 2番 asks *what blocks her today*, 4番 asks *what the clerk
says happens if you skip it*. **The repair is effective.** The 決め手の種類 label
is recorded as the weaker leg in §7, not filed as a finding.

決め手の種類 tally re-counted over all 7 rows (例 included, cap 2/token):
時刻・日程 2 / 連絡・情報の不足 2 / 規則・制度 1 / 設備・故障 1 / 人手・担当 1. Both
pairs at the cap carry **different** 質問型, so the 「決め手の種類と質問型が同時に
重なる」 shape F4 named exists nowhere in the table.

### 4.5 F5 — 日経新聞 → 業界誌, carried through every file

Verified by grep rather than by reading the note:

- `.agents/exam-blueprint/references/pools.json` L3890 = 「社長、本日の業界誌に
  弊社の記事が掲載されております。」 — **「日経新聞」 occurs nowhere in pools.json.**
- `tests/20260904_2/test_spec.json` `items.quick_response` carries the corrected
  string (the file's only other 「日経新聞」 hits are inside `spec_notes`, narrating
  the change — correct).
- `logs/ledger.json`'s 20260904_2 entry carries the same corrected string, plus a
  note. `check_draw_provenance()` resolves (gate: "every recorded draw resolves to
  a pools.json entry (22 items)").
- `聴解スクリプト.txt` speaks 業界誌 in both the stimulus and distractor 3, and
  **「新聞」 occurs 0 times in the whole script**, so the 問題4-11番 ↔ 問題13
  (地方紙の廃刊) lexical echo the round-1 report recorded beside F5 is gone too.
- The 20260904_2 `topics.json` row's 聴解問題4-11番 `surfaces`/`claim`/`shapes`
  all say 業界誌.

### 4.6 F6 — item 64, and the keyed-form exposure grep re-run over the new prose

**This is the check the brief singled out, and it is the one that caught
`20260903_1`.** I re-ran it by hand over the SHIPPED 問題10–14 prose *including
（注N） definition lines*, excluding stems and option strings per the rule's three
written exclusions, for all **17** keyed 問題7/8/9 forms — using the exact forms
the spec drew, not loose substrings:

| keyed form (spec) | occurrences in 問題10–14 prose |
|---|---|
| 〜とは(驚いた) / 〜おかげで / 〜としたら / 〜に即して / 〜だけに / 敬語:お越しになる / 〜に先立って / 〜つつも / 〜に相違ない / 〜と同時に / 〜からして / 〜やら〜やら | **0 each** |
| 〜ほど〜はない / 〜てたまらない / 〜意欲が湧いてくる / 〜に基づいて / 〜などあろうはずがない | **0 each** |
| 言いかえれば / 〜ずにすむ / 〜おそれがある | **0 each** |

**Zero hits, in any frame, for every keyed form.** The three near-misses a loose
substring scan throws up, and why none is a hit:

1. **「お越し」 ×3** in the 問題14 flyer — all 「お越しください」, the
   お＋連用形＋ください request form, not the 尊敬語 お越しに**なる** the item keys.
   And it is excluded twice over: exclusion #2 (a form carried by two or more of
   the item's own options carries no discriminating information) applies exactly —
   **options 3 and 4 both print 「お越し」**, so the flyer cannot push a reader
   toward either. The discrimination is 〜になる vs 〜する.
2. **「ほど」 ×4** — 「二十年ほど」「十分ほど」「一年ほど」 (approximation) and
   問題12(B)'s proportional 「量がふえるほど…開いていきます」. None is the keyed
   超越比較 「〜ほど…はない」; none carries the negation the form requires.
3. **「はず」 ×1**, in 問題11(1)'s （注4）「気をつけていれば避けられた**はず**の、
   あやまち」 — a 連体 use against a 文末-keyed 「〜あろうはずがない」, which the
   rule names explicitly as *not* a hit (its own worked example is nearly
   identical). 1 occurrence ≤ 1 anyway.

「という」 turns up 12 times, but 問題8-45's drawn target is
**「心理変化(〜意欲が湧いてくる)」**, not 「という」 — the 「もっと続けようという」 card
is a connective card in the scramble, not the tested point. None of the 12 is
even the 意向形＋という shape.

**Item 64's own new prose is inside this scan** (問題11(4) is in
`dokkai_closing_scopes()`'s enumeration), so the F6 repair planted nothing. Its
length effect also holds: 問題11 totals **2668** JP chars against the 2700 ceiling
and the 2250 floor — gate confirms both.

### 4.7 F7 — the 13-final closing column, re-derived from the sentences

I built the column myself from `dokkai_closing_scopes()` (the 13-closing
enumeration, 問題12 split into A and B), read each surface's last two prose
sentences, and assigned a label from the closed catalogue using `dokkai.md`'s two
**mechanical overrides** (主張-vs-条件提示; 説明-vs-意外な観察) rather than by feel.

| # | surface | final sentence (last one) | shape | sentence skeleton |
|---|---|---|---|---|
| 1 | 問題9 | 来年その大会が開かれるかどうかは、…自分から申し出た人がいたかどうかで、おおよそ見当がつく。 | 条件提示 | 「AかどうかはBかどうかで見当がつく」 |
| 2 | 問題10(1) | においで呼び出される記憶が、場面の細かさを欠いたまま気分だけを連れてくるのは、この道すじの短さによる。 | 意外な観察 | 「〜のは…による」（動詞終止） |
| 3 | 問題10(2) | 一人ずつの申し込みでよいのかどうかを、今週中にお教えいただけないでしょうか。 | 実用文・分類外 | 依頼疑問 |
| 4 | 問題10(3) | 省かれた手間の中にあったものを数え直さないかぎり、この代償の差し引きは合わないままである。 | 主張 | 「〜ないかぎり…ままである」 |
| 5 | 問題10(4) | …六月十日までに配布の用紙で組合までお知らせください。 | 実用文・分類外 | 命令依頼 |
| 6 | 問題10(5) | 前者は用事の呼びかけを断つ手当てであり、後者は目の反射を断つ手当てです。 | 説明 | 「S1はN1であり、S2はN2です」（二主語の区別） |
| 7 | 問題11(1) | 問いは前へ動いたのであって、消えたわけではない。 | 反論応答 | 「〜のであって…わけではない」 |
| 8 | 問題11(2) | ただ、私が受け持った家のうち、初めの半年のうちに家族以外の手を入れた世帯では、途中で入院に切りかえた例が目立って少ない。 | 条件提示 | 相関「[V-た+集団]では+数量の増減」 |
| 9 | 問題11(3) | めずらしさは一度で使い切られるのに対し、店先の立ち話は次に来る理由として残ります。 | 意外な観察 | 「AのにたいしB」（並列対比） |
| 10 | 問題11(4) | 人に手を借りた日のことは、してもらった中身が薄れたあとも、その日の光や音の形になって残るものらしいのです。 | 随筆 | 「Xのことは…らしいのです」 |
| 11 | 問題12(A) | 雑談は、話の行き来を早める道具でもあり、その場にいない人を置いていく仕掛けでもある。 | 説明 | 「Sは、N1でもあり、N2でもある」（一主語の両面） |
| 12 | 問題12(B) | 席の配置をいじって話の量をふやす前に、話の外に置かれる人がだれかを数えておきたいと思います。 | 主張 | 「Xする前にYしたいと思います」 |
| 13 | 問題13 | だれも読みたいと言わなかった記事が消えたあとで、町は初めてそれを探しはじめる。 | 反論応答 | 「Xが消えたあとで、初めて…はじめる」 |

**Shape tally: 条件提示 2 / 意外な観察 2 / 主張 2 / 説明 2 / 反論応答 2 / 随筆 1 /
実用文・分類外 2 = 13.** Every label is from the closed catalogue (F7's whole
point — the pre-fix row invented 対比整理・留保つき提示・両面提示), every shape is
at or under the cap of 2, and I reached each label independently. The two
overrides were applied and both are load-bearing:

- **問題10(1)** is 意外な観察, not 説明: the passage states a mismatch with
  expectation in its own words (「ところが、においをかがされた人が語ったのは、景色の
  細かさではなく…気分のほうであった」) and the closing gives its **cause**. Under 説明
  the paper would sit at 説明 ×3 and breach the cap.
- **問題10(3)** is 主張, not 条件提示: the closing explicitly rejects the
  single-factor view (「たしかに一日は長く使える。だが、その一日の中からは…消えている」)
  before its conclusion, and it addresses the reader. Under 条件提示 the paper
  would sit at 条件提示 ×3.

**Two labels I could have read differently, and neither flips compliance** — I
checked, because a shape label two readers split on is a coin flip, not a cap:
問題11(3) could be 随筆 (first-person, generalises without prescribing) → 随筆 2 /
意外な観察 1, still compliant; 問題13 could be 随筆 → same. The paper does not
depend on my label choice.

**Read down the SKELETON column, separately, as the rule requires** —
`FINAL_SENTENCE_TEMPLATES` run over the 13 finals:

```
A わけではない                      1   (問題11(1))
A では/ほど B が多い（相関）         1   (問題11(2))
every other named template          0
分裂文 「〜のは、…だ」               0
not-A-but-B reframe (REFRAME_CLOSING) 0 of 13
```

**No template appears more than once.** The `20260904_1` F2 defect — five of
thirteen finals on the 分裂文 skeleton behind a compliant label spread — is **not
reproduced**: the count here is **0** by the named regex, and the only cleft-ish
final (問題10(1) 「〜のは、…による」) closes on a verb, not a copula, and is alone.
The 後知れ 「〜ていた のだ」 skeleton, which carries its own tighter cap of 1, is at 0.

**Round-2's repair-collateral rule, applied.** F7 was a whole-column re-derivation,
so every one of the 13 is a landing site. I read each shared pair's two skeletons
side by side:

- **条件提示 (問題9 / 問題11(2))** — the one pair `dokkai.md` warns collides *by
  construction*. 問題11(2) IS the named correlation skeleton; 問題9 is 「〜かどうかは
  …かどうかで見当がつく」 with no では/ほど and no quantity. **Deliberately varied.**
- **意外な観察 (問題10(1) / 問題11(3))** — cleft-plus-cause vs parallel contrast.
  Distinct.
- **主張 (問題10(3) / 問題12(B))** — conditional-plus-ままである vs
  「〜する前に…たいと思います」. Distinct, and only the second is prescriptive in form.
- **反論応答 (問題11(1) / 問題13)** — 「〜のであって…わけではない」 vs a temporal
  「Xが消えたあとで初めて…」. Distinct.
- **実用文・分類外 (問題10(2) / 問題10(4))** — request question vs imperative.
- **説明 (問題10(5) / 問題12(A))** — **the closest pair on the column, and I read
  it twice.** Both close on coordinated copular nominals. They are separated by
  three things: 問題10(5) has **two subjects** in an either/or distinction
  (前者は…／後者は…), 問題12(A) has **one subject** with the both-and frame
  「〜でもあり…でもある」; the registers differ (です / である); and the rhetorical
  operations differ (separating two things vs asserting one thing is two things at
  once). I judge them template-distinct. **Recorded in §7 as the pair to watch**,
  because they are the nearest miss on this paper's column.

### 4.8 Artifact freshness — nothing is older than its source

| artifact | stamp | source | verdict |
|---|---|---|---|
| `聴解.mp3` | `script_sha 61fa39b5d131` | `聴解スクリプト.txt` sha1 = `61fa39b5d131…` | **matches** — the audio speaks the shipped script |
| `聴解.mp3` | `pacing_sha 4d623645a38d` | current pacing | matches |
| `聴解_チャプター.json` | same two shas, duration 2813.36 s | — | matches |
| `聴解.html` / `言語知識・読解.html` / `解答.html` | source sha stamped | the two .md | gate: "built HTML matches the Markdown it stamps" |

mtimes are consistent with the dependency order: script 22:16 → mp3 + chapters
22:25 → booklets/sheet 22:32. The 22:32 edits are 構成表/解説 prose in `聴解.md`,
which the MP3 does not depend on; the script itself has not moved since 22:16.

---

## 5. Findings

| id | item / file | class | evidence | fix |
|---|---|---|---|---|
| **R2-F1** | `tests/20260904_2/聴解.md` **L349** (問題5 構成表 下の解説文) | **要修正** — a quote attributed to the script that the script does not contain | The paragraph writes 「…女の委員長がその場で**「それがいちばん早いわね。じゃあ、その方向で」**と…いったん合意してしまい」. The script (`聴解スクリプト.txt` **L344**) reads 「女:そうですね。**それがいちばん早いですね。**じゃあ、その方向で。」 — 「わね」 for 「ですね」. The substantive claim (the chair agreed on the spot, then the agreement was retracted by new information) is TRUE and verifiable; only the quoted string is wrong, and it also mis-states the chair's register (casual 女性語 vs the polite です・ます she actually speaks). | Replace the quoted string with the script's own line: 「それがいちばん早いですね。じゃあ、その方向で」. One-character-class edit; no other file changes. |
| **R2-F2** | `tests/20260904_2/言語知識・読解.md` **L528** (問題8-47 解説, 構造欄) | **要修正** — a false premise inside the per-card proof | The 解説 asserts 「「三十年も聞いてきた」は普通形で終わる述語なので直後に名詞が必要で、**名詞で始まるカードは「父である以上」だけである**」. **「違いに気づかないことなど」 also begins with a noun (違い)**, so the stated premise is false as written. The item is nevertheless safe: the alternative it fails to exclude, (3)(4)(1)(2) = 「同じ機械の音を三十年も聞いてきた違いに気づかないことなど、父である以上、あろうはずがない」, requires reading 「三十年も聞いてきた違い」 as a gapless relative AND leaves 「父である以上」 unmodified, so the reason clause ("since he is a father") no longer grounds the noticing — only the keyed order builds 「三十年も聞いてきた父」. `verify_scramble` reports FREE UNITS **1** and ARTIFACT ok, and the last-slot proof is sound; the defect is confined to this one structural leg. | Replace the sentence with: 「名詞で始まるカードは「父である以上」と「違いに気づかないことなど」の二つだが、後者を先に置くと理由節「父である以上」が無修飾のまま残り、「父であること」が違いに気づける根拠にならない。「三十年も聞いてきた父である以上」という修飾関係を作れるのは鍵の語順だけである。」 |

**Nothing else was filed.** Every automatic-fail class in `exam-qa-review` was
checked on all 101 items and came back clean. In particular, and stated because
the brief asked for it explicitly:

- second defensible answer: **none** (blind solve 101/101; every distractor has a
  named impossibility in §3, not a "the key fits better")
- keyed option the source does not state: **none** (171 読解/文法/語彙 解説 quotes
  and 222 聴解 解説/構成表 quotes machine-traced; the 45 + 38 non-matches are all
  rule names, grammar-form citations, 問題5 置換確認 sentences, elided 「…」 quotes,
  option strings, and deliberately-recorded superseded history — each was read
  individually, and exactly one, R2-F1, was a real misquote)
- off-level key: **none** (問題1–6 checked by hand against Shin Kanzen / Soumatome
  and the 31-sitting archive; 谷(たに) is Shin Kanzen N2 漢字 entry **711**)
- option that is not a real Japanese word: **none** (the non-words are confined to
  問題1/2, where 音読み/表記 pseudo-compounds are the official design)
- 聴解 distractor not grounded in the script: **none** (every 問題1–3 wrong option
  carries a quoted script line in its 解説, and all quotes trace)
- 問題9 blanks sharing a category: **no** (four distinct tags)
- 問題7 stem with no （　）: **none**; 問題4 stem printing its own answer: **none**
- 読解 distractor eliminable by an absolute quantifier: **0 candidates**
- 読解 blind-strategy score above 45 %: **no** (22.2 % / 38.9 %)
- 即時応答 prompt with no defined responder: **none** (all 11 + 例 address a
  specific present interlocutor; 0 `アナウンス` speaker labels in 問題4)
- orphaned （注N）: **none** (30 markers, 30 definitions, 1-to-1 per passage)
- 問題14 generic truth-check shape / single-constraint item / invented detail:
  **none** (both items combine ≥2 constraints — see §3)
- artifact older than its source: **none** (§4.8)
- apparatus reused verbatim or near-verbatim from another test: **none** — I ran a
  full-corpus scan of every ≥18-JP-char non-boilerplate sentence in this paper
  against all 31 official booklets + scripts, every `tests/imported-*`, and all
  21 other generated tests. **5 hits, all benign:** two are official's own
  repeated question frames (「このメールで問い合わせていることは何か」 in **6** of the
  31 sittings, 「男の人は、この後まず何をしなければなりませんか」 in **5**), and two
  are `quick_response` pool sentences legitimately redrawn (20260812_2 is **16**
  draws back and 20260813_2 is **14**, against `cooldown_for('quick_response')` =
  **12**)
- item redrawn inside its rotation cooldown: **none** (checked directly against
  `cooldown_for()`, not just the gate line)
- theme record disagreement between `test_spec.json` and `logs/topics.json`:
  **none** — 20 rows joined, all agree, so the three-field divergence record does
  not apply to this paper
- headline theme repeating the previous test's in any slot: **none** (§6)
- `logs/ledger.json` disagreeing with `test_spec.json`: **none**; no hand-written
  date-shaped `harvest_sha`
- 問題1–2 解説 containing 「言及なし」/「未言及」: **0 occurrences**

---

## 6. Root-cause table

| id | root cause | recurrence (measured, by reading the papers) | owning file | proposed edit |
|---|---|---|---|---|
| **R2-F1** | `GATE-BLIND` | **7 of 22 papers on disk.** I ran the predicate across every `tests/*/聴解.md`: 20260810_1 (1), 20260817_3 (3), 20260821_1 (3), 20260827_2 (3), 20260903_1 (2), 20260904_1 (1), 20260904_2 (2, of which 1 is a deliberately-recorded superseded string). **Systemic by definition.** | `tools/check_consistency.py` (+ a one-line convention in `choukai-items.md`) | `check_section_table_quotes()` stops at the 構成表 table rows *by design* — but the free-text paragraphs UNDER those tables quote the script too, and nothing reads them, which is exactly why R2-F1 shipped. Widen it: scan `「…」` spans in the non-table lines of the 構成表 section as well, skipping any span containing `…`/`〜` (elision/pattern) and any span on a line marked as history. To make the second exclusion machine-decidable, add to `choukai-items.md` §構成表: **"a quoted string that is no longer in the script must be introduced by 「出荷時は」/「〜だった」/[SUPERSEDED] on the same line"** — the convention this paper already follows for 「日経新聞」 and 「新聞なら、毎朝、家で読んでいるよ」. **Founding measurement, run before proposing:** the predicate fires on `20260904_2` L349 (the founding case) and on the 6 other ids above; with the history exclusion in place it does **not** fire on this paper's 「日経新聞」 line. |
| **R2-F2** | `RULE-UNENFORCEABLE` | **14 items across 4 papers** carry the phrasing 「名詞で始まるカードは「X」だけである」 (20260827_1 ×4, 20260827_2 ×2, 20260904_1 ×4, 20260904_2 ×4), and a noun-initial test contradicts the uniqueness claim in **every one**. In 13 of the 14 the leg is decorative — another leg already forces the order. **問題8-47 of this paper is the one where it is load-bearing:** the を-object leg fixes slot 1, the last-slot proof fixes slot 4, and this claim is the only thing choosing between 「父である以上」 and 「違いに気づかないことなど」 for slot 2. | `question-authoring/references/bunpou.md` §問題8 (+ `verify_scramble.py`) | `bunpou.md` tells the author to write a per-card proof but never says what makes a leg SOUND, so "only card X begins with a noun" became a formula rather than a claim. Add, as a construction procedure rather than a post-hoc check: **"Before writing 「…だけである」 in a 構造 leg, list every card the claim ranges over and show the leg on each. A card beginning with a noun-plus-particle (「試験の結果が」「違いに気づかないことなど」) is noun-initial for the purpose of a 連体修飾 host, so a uniqueness claim about noun-initial cards is almost always false — exclude the rival on the SEMANTIC ground (what the resulting clause would have to mean) instead."** Mechanisable half for `verify_scramble.py`: parse `名詞で始まるカードは「(.+?)」だけ` out of the 解説 and print every other card whose first morpheme is a noun, as a WARN beside `FREE UNITS` — it cannot judge the semantics, but it can stop the false universal. **Founding measurement:** the predicate flags 問題8-47 of `20260904_2` (「父である以上」 claimed unique; 「違いに気づかないことなど」 also noun-initial) and the 13 other items above. |

**Effect on the loop** (`exam-qa-review` §6.5). Both root causes are open and
`GATE-BLIND`/`RULE-UNENFORCEABLE`, so **each must be applied or explicitly
rejected with a reason before the next test is authored** — they will otherwise
reproduce, and the measurements above show they already have, seven times and
four times respectively.

**No `GATE-WRONG` was found on any check that this paper passed.** I checked the
two most load-bearing ones by re-implementing them: the 13-closing enumeration
(`dokkai_closing_scopes()` returns exactly 13 with 問題12 split — matches
`dokkai.md`'s denominator table) and `FINAL_SENTENCE_TEMPLATES` (its 分裂文 row
correctly returns 0 on this paper; I verified by reading all 13 finals that there
is genuinely no cleft pile-up, i.e. the silence is real and not a mis-scope).

One **pre-existing WARN-class false positive**, not filed as a finding because it
is a linter noise issue with no effect on the paper: `make lint-draft 20260904_2`
reports 「Marker ②/③/④ appears in passage but is not referenced in question stems」.
All three are **問題14 flyer course numbers** (①田んぼの学校 … ④空き家の片づけ手伝い),
not 読解 passage markers. `lint_draft.py`'s `DOKKAI-MARKER` rule should exempt the
問題14 section, the same way `dokkai.md`'s option-length rule already exempts it.

---

## 7. Coverage statement

### Steps run, on which files

| step | scope | files |
|---|---|---|
| 0 — blind solve | **all 101 items**, from the keyless render alone, evaluated with `qa_eval.py`; then both mandatory blind-strategy passes over 問題10–13 | `qa/20260904_2/keyless.md` |
| 1 — key-by-key proof | **all 101**, deciding line located for each (§3) | 言語知識・読解.md, 聴解.md, 聴解スクリプト.txt |
| 2 — distractor elimination | **all 101**, one impossibility per wrong option | as above |
| 2b — plausibility (too weak) | every 問題1–6 option set (functional-category / tone read, incl. the 3:1-valence tell), every 聴解問題1–3 wrong option traced to its raising line | as above |
| 2.5 — level band | 問題1–6 keys by hand against `refs/Shinkanzen/kanji_tables.md`, `goi_reference.md`, `refs/Soumatome/goi_reference.md` and the 31-sitting archive; 問題7–9 keys against `bunpou.md`'s band | refs/ |
| 3 — mechanical reads | 文字・語彙 two stem counts, 問題7 three-number distribution, 問題8 splice + rival-ordering by hand + `make verify-scramble`, 問題9 categories and cloze length, 読解 apparatus/length/paraphrase/predictability (LCS computed here), the keyed-form frame grep re-run from the drawn forms, 171 + 222 解説 quotes machine-traced | all |
| 4 — 聴解 structure | the 構成表 read as COLUMNS for all five sections, all 24 問題3 spoken options re-scanned for key-exclusive tokens under 5 patterns, all four 例 verified answerable and equal to their announced numbers and to the marked grid, keigo direction on all 11 即時応答 | 聴解.md, 聴解スクリプト.txt |
| 5 — whole-paper & cross-test | 13-final closing column re-derived twice (labels + skeletons), theme table built from SHIPPED content, headline sets intersected against both previous papers, full-corpus verbatim scan | logs/topics.json, tests/*, refs/* |
| 6 — provenance | spec ↔ ledger ↔ topics.json ↔ pools.json for all 22 drawn items; `answer_positions` vs all 101 keys; the hand edit re-measured | test_spec.json, logs/ |
| 6.5 — root cause | §6, both predicates run over every paper on disk | — |

### Topic table (built from the SHIPPED text, not the spec tags)

**13 読解 theme rows, 13 distinct themes** (問題12 A+B = one row, per `dokkai.md`'s
denominator table):

| surface | theme (re-tagged from what shipped) | subject |
|---|---|---|
| 問題9 | スポーツ・余暇 | 市民マラソンが続く条件 |
| 問題10(1) | 科学・技術 | におい／写真と記憶の呼び出し |
| 問題10(2) | 働き方 | 週四日勤務の試行と当番 |
| 問題10(3) | 消費・経済 | 翌日配送の代償 |
| 問題10(4) | 環境 | 集会所の太陽光を自家消費へ |
| 問題10(5) | 教育 | 集中できる机の二つの手当て |
| 問題11(1) | 交通 | 自動運転と責任の所在 |
| 問題11(2) | 医療・福祉 | 在宅介護と外の手を入れる時期 |
| 問題11(3) | 旅行・観光 | 秘境の滝と途中の食堂 |
| 問題11(4) | 子育て・家族 | 産後ケアと見守られた記憶 |
| 問題12(A)+(B) | 人間関係 | 職場の雑談の両面 |
| 問題13 | メディア・情報 | 地方紙の廃刊と持ち場 |
| 問題14 | 地域活性化 | まちの担い手体験プログラム |

No subject appears twice. **21 drawn 聴解 scenarios**, per-theme max **4**
(消費・経済), well inside rule 3's ≤5.

**Cross-test, rule 4, computed rather than accepted:**

| slot | 20260904_2 | 20260904_1 (1-back) | 20260903_1 (2-back) |
|---|---|---|---|
| 問題9 | スポーツ・余暇 | 旅行・観光 | 消費・経済 |
| 問題12 | 人間関係 | 住まい | 教育 |
| 問題13 | メディア・情報 | 行政・手続き | 防災 |
| 問題14 | 地域活性化 | 食 | 医療・福祉 |
| 聴解問題5-1番 | 教育 | 文化・伝統 | 環境 |
| 聴解問題5-2番 | 睡眠・健康 | 働き方 | 科学・技術 |

- **1-back intersection = ∅** (rule 4 allows zero). This is what F1 existed to
  fix — the pre-fix 聴解問題5-2番 was 旅館:食事場所の希望確認 (食) against
  20260904_1's 問題14 食.
- **2-back intersection = {教育}, exactly 1** (rule 4 allows at most one).
- 問題12's theme differs from both previous papers' 問題12 specifically.
- Rule 2 (lenient reading, the one `check_topics_themes()` encodes): the four
  読解 headline themes each appear exactly once in the 読解 half. 聴解問題5-1番's
  教育 also tags 問題10(5), which the lenient reading permits explicitly.
- 問題14 shares no decisive number with any 聴解 item (gate, re-read: the flyer's
  numbers are 千/二千/三千円, 九月三十日, 十月十一日/十二日, 定員 12/8/20/6 — none
  recurs as a 聴解 decider).

### Every `make check` line naming this test, with its resolution

`python3 tools/check_consistency.py` → **1 FAIL, 5 WARN** touching 20260904_2.

| line | resolution |
|---|---|
| **FAIL** `32 exam MP3(s) are on the 'audio' release — ['20260904_2'] differ…` | **Expected, orchestrator's, not a paper defect.** The MP3 is built and correct; it has not been pushed because `make upload-files` is deliberately out of this pass's scope (and out of mine). Resolves the moment Stage 5 uploads. |
| **WARN** `errand-rotation check compares most of the draw (3/44 = 7% keyed)` | **Systemic, every paper trips it** (measured: 20260819_1 5 %, 20260821_1 2 %, 20260827_1 5 %, 20260827_2 2 %, 20260828_1 5 %, 20260903_1 2 %, 20260904_1 5 %). It says the errand-key check is *silent* about 41 unkeyed draws, not that anything repeats. The repair is pool growth, which is not this paper's. **Not a paper defect.** |
| **WARN** `no 聴解 slot repeats its own theme in the previous 2 papers (2 slot(s)) — 聴解問題3-5番=働き方 (also 20260903_1); 聴解問題2-6番=行政・手続き (also 20260904_1)` | **Pre-existing, dispositioned in round 1 §4, re-checked here.** These are non-headline 聴解 slots; rule 4's zero-tolerance clause binds the **headline** set, which is clean (∅ against the 1-back). Slot-level theme reuse in 問題2/問題3 is a WARN precisely because it is not decidable by count. Both errands differ (2-6番 税務署の確定申告 vs 20260904_1's row; 3-5番 契約書の読み方 vs 20260903_1's). **Not a paper defect.** |
| **WARN** `every stamped spec's pools_sha matches pools.json (12b54f88ee78) [21 of 22]` | **Repo-wide and expected.** The F5 pool repair legitimately changed `pools.json`, so every previously-stamped spec now records an older sha — including this paper's own `3a0b702a1277`. This is the intended record of "the pool moved", not drift. **Not a paper defect.** |
| **WARN** `聴解 section mix (judgment calls) — 問題2: 1 理由 (どうして) item(s)` | **NEW, created by the F4 repair. Re-adjudicated independently in §4.4 and accepted.** The owner's row is an upper bound (`理由 ≤3 of 6`) with **no floor**; the section's two FAIL conditions (>4 on one type, 0 content items) are both far off; 内容・発言 sits at 2, satisfying its own `≥2` quota explicitly; 気持ち at 1 satisfies its `≥1`. Counting the 例, 理由 is 2 of 7 = 29 % against official's 37 %. **Resolved — see §8 for the note this leaves the next paper.** |
| **WARN** `問題1/2 options share vocabulary with their script block (2/47 = 4%) — 問題2-例-4; 問題2-6番-1` | **Not disclosed in the round-2 brief; adjudicated here from scratch.** Both flagged options are **KEYS** (問題2's 例 is announced 4番, and `answer_positions.聴解_問題2[5]` = 1), and the WARN's own text says the question is whether an option "truly has no basis in the script". Both do: 例-4 restates 「来月の十日に、地図を新しくしたものが出るんです」＋「今回はやめて、来月まで待ちます」; 6番-1 restates 「三十分ほどで終わりますよ」＋「よかった。今日の午後は、仕事に戻れないと思ってました」. Zero **distractors** are ungrounded — which is the failure mode the check exists for. **False positive for this paper; resolved.** |
| `skip` `詳細解説.json` ×2, `問題8 form-family (0 of 5 tagged)` | Expected. The model answer is Stage 5 and has not run; the 問題8 family map is hand-maintained and this draw carries no tag. Neither is evidence of anything. |

### Numbers the skill requires printed rather than assumed

- **問題1/2/5 stems with no 「、」: 14 of 15 (93 %)** — author target ≥9, official
  runs 47–93 % comma-free. Per-paper median stem length **17** JP chars (archive
  max 21.5; fourteen earlier papers shipped 29).
- **問題1–5 stems in です・ます: 7 of 25 (28 %)** — author target exactly 7,
  official 2–11. First-person stems 3, institution-actor stems 0.
- **問題7 stems:** mean **41.9** (band 36–52) / **3** stems under 34 (need ≥2) /
  spread **39** (need ≥25). Dialogue or setting-label stems present (33, 36, 41).
- **問題6 option sentences:** mean 27.9, median 28, range 23–32, **3** over 30
  chars (targets: mean 23–29, longest ≥29, ≥2 over 30).
- **問題9 cloze body: 693 JP chars** (target ~500–700); options all ≤16 chars.
- **問題13: 1070-char ceiling / 800 floor** — inside; **問題11 total 2668 / 2700**.
- **読解 register:** kanji density **30.9 %** (band 22–34, gate WARN band 24–32),
  first-person essays **9 of 12** (floor 4), です・ます passages **4** (floor 3),
  median sentence **36.0** chars (target 33–43), short-sentence share 23.6 %
  (band 12–30).
- **聴解:** 縮約形 47.2/10k, hesitation 43 tokens (band 9–48), reaction turns
  20.5 %, 問題3 talk lengths 269–298 (band 220–300, all six inside), voice balance
  worst section 57 %.
- **Re-drawn keys this pass:** the only tier-C re-draw was
  `--reroll-one listening_scenarios:6` (F1), which draws a **scenario**, not a
  vocabulary key — so no 問題1–6 key changed and there is no new band check to
  report. All 22 drawn items are the ones the spec and ledger record.

---

## 8. Notes for the NEXT paper (recorded, deliberately not filed as findings)

Per the round-2 brief, each of these is explicitly **not a blocker** on
20260904_2. They are things a reviewer would want on the record.

1. **問題2's 理由 count at 1 of 6 is the floor-less edge of a quota.** The F4
   repair was correct and the WARN is inside the rule, but official's largest
   問題2 class is 理由 at 33–37 %, and a paper at 1 of 6 sits well under it. If a
   second paper also lands at 1, the class becomes systemic. Pre-emptive edit for
   `choukai-items.md` §"Section item mix": give the 問題2 理由 row a soft floor
   (**target 2 of 6**, WARN below), so the next author re-angles a *different*
   item when they need to break a 決め手×質問型 collision.
2. **問題10(5) is tagged 教育 for a passage that never mentions study.** The
   passage ("集中できる机") is about attention and workspace; 教育 is the closest
   value in the closed vocabulary but is a stretch. `test_spec.json` and
   `topics.json` agree, so this is **not** the theme-record-divergence class and
   nothing needs the three-field note — but the tag is what keeps "no theme on two
   読解 surfaces" green (re-tagging to 働き方 would collide with 問題10(2)). Worth
   knowing that the 13-distinct-themes line has one soft row.
3. **A setting echo no gate compares: 問題10(4) and 聴解問題1-5番 are both a
   町内会 集会所 with a 班 and an administrative deadline.** Different subjects
   (太陽光の自家消費 vs 防災訓練の準備), different themes (環境 vs 防災), different
   errands — so no rule is breached, and the 構成表's own same-establishment check
   is 聴解-internal. But to a reader taking the paper straight through, the same
   civic furniture appears twice. `check_consistency.py` compares 読解 settings to
   聴解 settings nowhere.
4. **問題4's vocabulary set runs a shade easier than the current-era official
   band.** Nothing meets the TOO_EASY definition (no headline N3-or-lower item
   outside both N2 volumes; no option set of four N4–N5 words), and 退屈/手ごろ/
   返品/かかわる/枯れる all appear in official N2 booklets. But compare the keys
   side by side: ours are 上旬・かかわる・親類・退屈・枯れる・手ごろ・返品 against
   7/2025's 誓った・一時的に・関与・べたべた・反則・追い払った・スタイル and
   12/2024's 完了・衰えて・省略・思い込んで・口調・役目・ずうずうしい. **問題4-14
   (上旬 vs 月末/中旬/下旬) is the softest item on the paper** — the stem prints
   「三日から五日まで」, so it resolves by arithmetic once the three 旬 terms are
   known. Not a defect; a drift direction to watch.
5. **The closest pair on the closing column is 説明 (問題10(5) / 問題12(A)).** I
   judged them template-distinct in §4.7 (two subjects in an either/or distinction
   vs one subject in a both-and duality; です vs である), and the named-template
   counter agrees at 0 for both. But they are the two finals on this paper that
   read most alike down the column, and `20260904_1`'s F2/F3 history is that a
   pair which survives one round wearing different clothes is exactly what the
   next round finds. If 説明 is drawn twice again, vary one away from a coordinated
   copular nominal entirely.
6. **`lint_draft.py`'s `DOKKAI-MARKER` rule fires on 問題14 course numbers.** Three
   WARNs (②③④) on this paper, all false. Filed as a tool scope note in §6.

---

## 9. Skips

Stated explicitly, per `AGENTS.md` §0.7.

1. **`make upload-files` was NOT run**, so the one `make check` FAIL
   (`exam MP3(s) are on the 'audio' release`) is still open. The brief forbade it
   and it is the orchestrator's step. The MP3 exists, is built from the shipped
   script, and is correct — it is simply not pushed.
2. **`make model-answer` was NOT run**, per the brief and per `AGENTS.md` §5
   (Stage 5 runs after QA passes). Consequently `詳細解説.json` /
   `詳細解説.vi.json` do not exist, and the two gate lines that read them
   (`詳細解説 prose contracts`, `詳細解説.json options match the booklet`) `skip`.
   **Neither the model answer nor its two language panes was reviewed** — that is
   out of scope for this pass and must be QA'd on its own terms after Stage 5.
3. **No file was edited.** I reviewed; I did not repair. Both findings in §5 carry
   the exact replacement text so they can be applied without re-deriving anything.
4. **No `git add` / `git commit`** was run.
5. **Archive binaries were available** — `refs/JLPT_N2_NEW/*/booklet.md`,
   `script.md` and `answer_keys.json` are all present and were read directly, so
   nothing in this review rests on a remembered number. The `refs/Shinkanzen/*`
   and `refs/Soumatome/*` extracts were read as OCR (secondary evidence, per
   `AGENTS.md` §3); **no PDF page was opened**, because every band this pass
   needed was decidable from the tracked `*.md` extracts plus the 31-sitting
   archive. The one lookup that mattered — 谷(たに) as an N2 漢字 headword — was
   confirmed at `refs/Shinkanzen/kanji_tables.md` L4968 rather than asserted.
6. **`make check`'s full output was read line by line** (6557 lines), not grepped
   for FAIL. All 6 lines naming this test are dispositioned in §7.

---

## 10. Verdict, restated

```
QA: FAIL (2 findings, 0 automatic)
```

Both findings are in explanatory artifacts; the examinable paper is clean on
every check this skill defines. 2 ≤ 3, so `jlpt-test-generation`'s stage-4 rule
permits **direct repair without a third review** — apply the two replacement
strings in §5, re-run `make check` (neither edit touches the script, so no MP3
rebuild is needed; `聴解.md` and `言語知識・読解.md` must be re-rendered with
`make booklet` + `make sheet`), sanity-read the two diffs, and Stage 5 can start.

The two root causes in §6 are open and block the **next** generation run until
applied or explicitly rejected.
