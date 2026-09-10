# QA Report — 20260909_1, ROUND 2 (adversarial pass, `exam-qa-review`)

**Reviewed revision** (sha1[:12] over raw bytes, `shasum -a 1`), verified at the START and again at the END of the pass:

| file | sha1[:12] at start | at end | moved? |
|---|---|---|---|
| `言語知識・読解.md` | `4ebe0605afaf` | `4ebe0605afaf` | no |
| `聴解.md` | `66eb855c8a3a` | `66eb855c8a3a` | no |
| `聴解スクリプト.txt` | `3efcc7f2675d` | `3efcc7f2675d` | no |
| `test_spec.json` (recorded, not required) | — | `0250fdf1904a` | — |

Reviewer: round-2 fresh-eyes context. Authored nothing, repaired nothing, is not round 1's
reviewer. Timestamp 2026-09-09. Sources were still throughout, so every byte-offset claim below
is about the revision named. `qa/20260909_1/keyless.md` records the same three shas.
`模範解答.html` is confirmed absent — stage 5 has not started.

Read in full from disk before any other tool call: `AGENTS.md`,
`.agents/exam-qa-review/SKILL.md`, `qa/qa-report-20260909_1.md` (round 1's RECORD — read, not
edited), `qa/root-cause-dispositions-20260909.md`.

---

## 1. Verdict

**QA: FAIL (3 findings, 1 automatic)**

- **R2-F1** `要修正` — `logs/topics.json`'s row records the SUPERSEDED listening half (24 of 29 聴解 rows)
- **R2-F2** `自動不合格` — a topic repeated within the paper: 問題11(4) ↔ 聴解問題4-7番
- **R2-F3** `要修正` — 聴解問題1 and 聴解問題3 each key the same option 4 times of 5

All five of round 1's findings (F1–F5) are independently verified CLOSED. Blind solve is
**101/101**. The three findings above are all downstream of one thing the dispositions got
wrong: the re-composition moved **25 of 29** listening slots, not one.

---

## 2. Blind-solve diff

Solved from **`qa/20260909_1/keyless.md`** only. Verified keyless before reading
(`grep -n "正解\|解説\|解答用紙"` → no output). 聴解 solved from the render's embedded
`聴解スクリプト.txt`. All 101 answers written down before any keyed source was opened.

```
python3 tools/qa_eval.py tests/20260909_1 --answers "[...]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
✓ 100% Blind-Solve Agreement across all 101 items.
```

**Agreement: 101/101 (100.0%). Zero mismatches, so no finding arises from step 0.** Round 1's
single mismatch (item 73, the unanswerable figure item) is gone: the slot now prints four real
options and I answered it correctly blind.

### 2.1 Blind STRATEGY passes over the 読解 items (both recorded, re-implemented from scratch)

問題10–13, 18 items, chance 25%, ceiling 45% on either. Computed with my own implementation
(bigram overlap normalised by each option's own bigram count) and run over the ten officials in
the same script, so the comparison is like-for-like.

| strategy | 20260909_1 | official range (my run, 10 sittings) | verdict |
|---|---|---|---|
| most character bigrams shared with own passage | **44.4 %** | 11.1 – 44.4 % | PASS (< 45 %) |
| second-longest option | **11.1 %** | 11.1 – 55.6 % | PASS (< 45 %) |
| median overlap margin (key − best distractor) | **−0.027** | −0.018 … −0.161 (all negative) | PASS (must not exceed 0) |

The bigram figure **exactly ties the official maximum** (imported-n2-2022-12, 44.4 %) and sits
0.6 points under the ceiling. It passes the rule and does not exceed any real sitting, so it is
not a finding — but it is the paper's closest-to-the-line number and the second run in a row to
say so. Round 1 measured 41.7 % with a different normalisation; both are inside.

### 2.2 My own key-paraphrase measurement (re-measured, not trusted)

`check_verbatim_keys` was inert on every paper before 2026-09-09, so I implemented the longest
common **contiguous** substring with my own DP and measured at both scopes — key vs its own
passage, and key vs the whole 問題10–14 prose half (6 456 chars).

| item | key len | LCS own | % | LCS whole half | % | longest run |
|---|---|---|---|---|---|---|
| 52 | 30 | 4 | 13 % | 4 | 13 % | は似てい |
| 53 | 22 | 5 | 23 % | 5 | 23 % | るかどうか |
| 54 | 31 | 4 | 13 % | 6 | 19 % | 決めておいた |
| 55 | 31 | 7 | 23 % | 7 | 23 % | 、その日ごとに |
| 56 | 36 | 7 | 19 % | 7 | 19 % | これまでどおり |
| 57 | 19 | 6 | 32 % | 6 | 32 % | 困ったときに |
| 58 | 35 | 5 | 14 % | 5 | 14 % | ではなく、 |
| 59 | 27 | 5 | 19 % | 5 | 19 % | た日の翌朝 |
| 60 | 28 | 3 | 11 % | 3 | 11 % | のまま |
| 61 | 26 | 7 | 27 % | 7 | 27 % | 、分かった状態 |
| 62 | 30 | 6 | 20 % | 6 | 20 % | いる途中の人 |
| 63 | 23 | 6 | 26 % | 6 | 26 % | 決めてあった |
| 64 | 30 | 5 | 17 % | 5 | 17 % | 降りられる |
| 65 | 27 | 5 | 19 % | 5 | 19 % | 橋ができて |
| 66 | 41 | 3 | 7 % | 3 | 7 % | は自分 |
| 67 | 19 | 6 | 32 % | 6 | 32 % | 人にたずねた |
| 68 | 26 | 3 | 12 % | 3 | 12 % | 、自分 |
| 69 | 32 | 6 | 19 % | 6 | 19 % | 自分で確かめ |
| 70 | 30 | 10 | 33 % | 10 | 33 % | 前の週の金曜日までに (問題14, lift-exempt) |
| 71 | 4 | 0 | 0 % | 1 | 25 % | 千 (問題14) |

**Worst run in 52–69 is 7 characters (23 %)**, against thresholds of LCS ≥ 15 & ≥ 50 %, or
LCS ≥ 20. **Zero violations, measured independently at the stricter scope.** This reproduces
round 1's numbers to the character, which is the point of re-measuring. Item 69 — the item whose
passage F3 re-closed — measures 6 chars (19 %) 「自分で確かめ」, unchanged in class.

The 10-char run at item 70 is the 問題14 flyer condition 「前の週の金曜日までに」, which 問題14 is
exempt from restating and which official does every sitting.

---

## 3. Per-question walkthrough — all 101 items

Paper order 1–71, then 聴解 問題1…問題5 (問題5-2番 質問1/質問2). `OK` rows carry the deciding
quote; non-OK rows carry file+string and the concrete repair. There is no 例 row: the marksheet
prints 「（出典の台本に練習問題「例」の行がないため、例の欄はありません。）」 — see §5.5, where the
predicate is refuted against all ten officials.

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 1. おどろく | OK | 驚く＝思いがけないことに出あってはっとする。おどろく/なげく/つぶやく/わめく の四つとも実在の同分野和語動詞、送り仮名「く」を四択が共有 | — |
| 問題1-2 | 3. あらそう | OK | 争う＝勝ち負けや順位をめぐって力をぶつけ合う。きそう/たたかう/あらそう/はりあう 四つとも実在語、送り仮名「う」共有 | — |
| 問題1-3 | 2. れいせい | OK | 冷静。2×2読み行列 {れい,ひや}×{せい,じょう} が完全に成立 | — |
| 問題1-4 | 3. じどうけんばいき | OK | 自動券売機。2×2 {はい,ばい}×{き,ぎ}、「売」の連濁が決め手 | — |
| 問題1-5 | 2. たいりょく | OK | 体力。2×2 {たい,てい}×{りょく,りき} | — |
| 問題2-6 | 3. 講義 | OK | {構,講}×{義,議}。構＝組み立てる字で、人に説き聞かせる「講」ではない | — |
| 問題2-7 | 1. 遠足 | OK | {遠,園}×{足,促}。園＝草木を植えた場所の字 | — |
| 問題2-8 | 1. 一通り | OK | {一,人}×{通,遠}、四択とも「り」共有。人通りは実在語だが読みは「ひとどおり」 | — |
| 問題2-9 | 2. 抑える | OK | {収,抑,治,納} すべて「おさ-」を持つ実在字、送り仮名「える」共有 | — |
| 問題2-10 | 3. 預ける | OK | {予,野,預,序} すべて予の部品を持つ、送り仮名「ける」共有 | — |
| 問題3-11 | 3. 嫌い | OK | 人嫌い＝人と付き合うのをわずらわしく思う性質。「大勢が集まる場所を避けている」が決め手 | — |
| 問題3-12 | 4. 浅 | OK | 浅学＝学問の身につけ方が十分でないこと。「述べさせていただきます」の謙譲文脈 | — |
| 問題3-13 | 2. 新 | **OK（F2 修理を確認）** | 幹は「四月から（　）体制になり、これまでなかった部署もできる。」— 鍵「新」の字は幹に出ていない。「これまでなかった部署もできる」が 旧/前 を殺し、現 は「〜になる」の変化先にならない | — |
| 問題4-14 | 1. 要領 | OK | 要領を得ない＝話の中心がはっきりしない（慣用句として固定） | — |
| 問題4-15 | 4. 発車 | OK | 「ドアが閉まり、電車はゆっくりと」＝止まっていた場所から動き出す。車 は四択すべてが担ぐので手がかりにならない | — |
| 問題4-16 | 3. 真っ黒 | OK | 「魚が（　）に焦げた」＝これ以上ないほど黒い | — |
| 問題4-17 | 2. 無邪気 | OK | 「三歳の娘は大人の事情など何も知らず、ただ（　）に笑っている」 | — |
| 問題4-18 | 2. ふさいで | OK | ふさぐ＝通り道や穴を物でうめて通れなくする。「人の通り道を」が決め手 | — |
| 問題4-19 | 1. 足が出て | OK | 足が出る＝かかった金が決めておいた額をこえる。「予算を決めておいたが、買いすぎて」 | — |
| 問題4-20 | 3. 響き | OK | 響き＝その言葉が耳に残す感じ。「古い言い方には、どこか懐かしい（　）がある」 | — |
| 問題5-21 | 2. つまり | OK | 要するに＝前に述べたことを短くまとめると | — |
| 問題5-22 | 4. がっかりして | OK | 落ち込む＝思うようにいかず気持ちが沈む。置換確認可 | — |
| 問題5-23 | 3. 役立てて | OK | 重宝する＝便利なものとしてたびたび使って役に立てる | — |
| 問題5-24 | 3. 話し合った | OK | 交渉する＝条件について相手と話し合って折り合いをつける | — |
| 問題5-25 | 2. どのように | OK | いかに＝どのような方法で。「解決するか」が方法を問う | — |
| 問題6-26 | 4. 無理な働き方を何年も続けて、父はすっかり健康を損なった。 | OK | 損なう＝保たれているよい状態をこわす。1 皿は「割る」、2 金は「損する」、3 待ち合わせは「すっぽかす」 | — |
| 問題6-27 | 4. 会社をやめると言い出した部下を、部長が何度も引き止めた。 | OK | 引き止める＝去ろうとする人を思いとどまらせる。1 は「停止させる」、2 は自分の行為で「見合わせる」、3 は物理力で「せき止める」— 三つとも別の正しい動詞、単一軸ではない | — |
| 問題6-28 | 1. 大人でも一人で運べない重さだから、まして子どもには無理だろう。 | OK | まして＝前の例より条件の悪い場合を重ねて示す。2 は「そのうえ」、3 は逆向き、4 は「結局」 | — |
| 問題6-29 | 3. 明日の発表の準備が終わらず、昨夜は徹夜で資料を作った。 | OK | 徹夜＝夜のあいだ一度も寝ないで通す。1 は機械を主語に取り、眠らないものに徹夜は使えない（「機械を徹夜で動かす」なら可）。2 は昼間、4 は時刻の語ではない | — |
| 問題6-30 | 3. この植物は、暖かい地方にしか育たない種類に属している。 | OK | 属する＝あるまとまりや区分の中に含まれる。1 は「付いている」、2 は「よる」、3 以外は所属関係でない | — |
| 問題7-31 | 4. とともに | OK | 「人口が減る（　）、空き家の数もふえていった」＝並行変化。にひきかえ は対比、どころか は否定強調、につけ は「〜につけ…につけ」 | — |
| 問題7-32 | 1. べきだ | OK | 「期日を約束した以上、今日中に出す（　）」＝当然の義務 | — |
| 問題7-33 | 3. をもとに | OK | 「祖母から聞いた話（　）書かれた」＝素材・典拠 | — |
| 問題7-34 | 2. にすぎない | OK | 「天候に助けられた一時のもの（　）」＝それ以上でない | — |
| 問題7-35 | 2. 向けだ | OK | 「文字を習い始めた子ども（　）。むずかしい漢字は一つも出てこない」＝対象指定 | — |
| 問題7-36 | 4. といえば | OK | 「連休（　）、去年は道が混んでいて」＝話題の取り上げ | — |
| 問題7-37 | 3. というわけではない | OK | 「高ければ必ず長く使える（　）」＝部分否定 | — |
| 問題7-38 | 1. ことだし | OK | 「雨もやんだ（　）、そろそろ買い物に出かけない」＝軽い理由の列挙 | — |
| 問題7-39 | 2. 際 | OK | 「お電話をなさる（　）は、一階のロビーへ」＝掲示の丁寧な場面指定 | — |
| 問題7-40 | 1. に越したことはない | OK | 「席の数には限りがあるのだから、早めに取っておく（　）」＝それが最善 | — |
| 問題7-41 | 3. て以来 | OK | 「引っ越し（　）、あの丘には一度も登っていない」＝起点からの継続 | — |
| 問題7-42 | 4. くせに | OK | 「詳しいと言っていた（　）、いつも同じ角で曲がりそこねる」＝非難含みの逆接 | — |
| 問題8-43 | 4. ように | OK | 家族を→起こさない→**ように**→新聞は玄関で読むらしい。らしい が文末固定、家族を は を格で二重束縛なし。★=4 一意 | — |
| 問題8-44 | 1. 味わえない | OK | 店を開けたばかりの時間→でなければ→**味わえない**→ものだと思う。でなければ は直前に名詞句を要求 | — |
| 問題8-45 | 2. 予想されますので | OK | なお→当日は受付の混雑が→**予想されますので**→早めにお越しください。が 格の唯一の述語は 予想されます（最終札は読者への命令で主語を取れない） | — |
| 問題8-46 | 2. 勉強する | OK | 音楽を→聞きながら→**勉強する**→くせが直らないらしい。らしい 文末固定。4→1→2→3 も ★=2 で同値、二答にならない | — |
| 問題8-47 | 4. 山を歩く人たちの | OK | 持っていかねばならない→というのが→**山を歩く人たちの**→間の決まりだ。`verify-scramble` は UNDECIDED（18/24 生存）なので手で全札を全スロットに入れて確認、最終札も宿主候補として検査。裸の が/は 札なし、FREE UNITS 1 が正しい。4→1→2→3 は 山を歩く人たちの を の格主語に消費して「間の決まりだ」が所有者を失い不成立 | — |
| 問題9-48 | 4. その結果 | OK | [論理接続] 前＝半回転が必要、後＝立ち止まり大通りを歩き出す。因果 | — |
| 問題9-49 | 4. せざるを得ない | OK | [文末モーダル] 「決まりを動かさないかぎり、読み手はこの半回転を（　）」＝避けられない | — |
| 問題9-50 | 2. 案内しているつもりでも | OK | [内容推論] 「町は（　）、初めて来た人はその場から動けない」＝意図と結果の逆接 | — |
| 問題9-51 | 2. 次の一歩を決める手がかり | OK | [慣用・形式名詞] 最終文「何を載せるかを考える前に」が 3「店の数や名前のくわしさ」を、第3段落の景色と絵の重なりが 1/4 を殺す。四つの空欄は四つの異なるカテゴリ | — |
| 問題10-52 | 4. 呼び名は似ているが、文章の形を組み直すか近づけて見るかが違う | OK | 「名前は似ていても、届く先が違う」＋「行の切れ目が引き直され」／「紙を目に近づける動き」 | — |
| 問題10-53 | 1. 当日に持ちこむ道具があるかどうかと、その中身 | OK | 「お持ちになる道具がありましたら、その大きさと、電源をお使いになるかどうかを…お知らせいただけないでしょうか」 | — |
| 問題10-54 | 4. 早いうちに休みを決めておいた家庭のほうが、行事に足を運べていた | OK | 「配られた日のうちに休む日を決めていた家ほど、行事に出られた回数は多かった」 | — |
| 問題10-55 | 2. 変えない決まりのそばには、その日ごとに手で加減される部分がある | OK | 「変えないと決めた部分と、その日ごとに加減する部分とが、はじめから組になっているのかもしれません」 | — |
| 問題10-56 | 4. 用具を受け取る場所だけが変わり、申し込みと返却はこれまでどおりであること | OK | 「十月からは地下一階の用具室でお渡しします」＋「お申し込みは、これまでどおり一階の受付です」＋「お返しになる場所も、これまでどおり一階の受付です」 | — |
| 問題11-57 | 1. 困ったときに助けを求める人も少なかった | OK | 「頼みごとがほとんど交わされない地区では、困ったときに声を上げる人も少なく」 | — |
| 問題11-58 | 4. 断ることのできる頼みは相手への負担ではなく、次の声かけを生む合図になる | OK | 「断れる頼みは、頼まれた側にとって荷物ではなく、あなたは頼ってよい相手だという知らせである」 | — |
| 問題11-59 | 1. 長く歩き回った日の翌朝のほうが、起きるのが楽だったこと | OK | 「いちばん意外だったのは、よく歩いた日の翌朝が軽かったことだ」 | — |
| 問題11-60 | 4. 同じ姿勢のまま長く過ごし、体の使い方がかたよるためである | OK | 「同じ形のまま固められていて、肩や腰がこわばる（注4）のは、使いすぎからも、使わなさすぎからも起きる」 | — |
| 問題11-61 | 1. 答える側に、分かった状態を思い描いたうえで判断させる | OK | 「答える側に判定の仕事をさせるという性質があります。分かったかどうかを自分で決めるには、分かった状態がどういうものかを知っていなければならず」 | — |
| 問題11-62 | 2. 学んでいる途中の人でも答えられ、どこで止まったかが伝わる問い | OK | 「返ってくるのは判定ではなく事実で、まだ分かっていない人にも答えられます」＋「その人がどこで止まっているかが見えます」 | — |
| 問題11-63 | 3. 途中で休める場所を前もって決めてあったかどうか | OK | 「分かれ目になっていたのは、途中で一度腰を下ろせる場所を、その日より前に決めておいたかどうかだった」 | — |
| 問題11-64 | 3. 歩き通すための品をそろえるほかに、途中で降りられる場所も要る | OK | 「それらはみな歩き続けるための備えであって、歩くのをやめてよい場所を先に決めておくのは、別の備えだ」 | — |
| 問題12-65 | 1. 橋ができても、人の多くはそれまでの通り方を変えていない | OK | A「橋を上る人はごく少なく、朝も夕方も、人が集まる場所は前と同じである」／B「橋を上った人は、そのまま待って通った人の五分の一ほどでした」 | — |
| 問題12-66 | 4. Aは自分が橋を使わずにすませる理由を、Bは使われ方の時間によるかたよりを | OK | A「私自身、急いでいる日でさえ、橋のほうへは足が向かない」／B「その間だけを取れば三倍になります」 | — |
| 問題13-67 | 2. だれがいつ何人にたずねたのかを示す一行 | OK | 「「市が昨年十月に、十八歳以上の千人にたずねたところ」。こういう一行である」 | — |
| 問題13-68 | 1. 示された結果を、自分の身の回りに当てはめて考えること | OK | 「千人ならうちの町にも当てはまりそうだ、昨年十月なら今年の値上がりは入っていない。そんなふうに、読んだ人が自分の側で先へ進める」 | — |
| 問題13-69 | 3. 短くする作業でも、読む人が自分で確かめに進める手がかりは残したい | **OK（F3 修理後に再検証）** | 「後者まで一緒に削ってしまうと、読み終わったところで道が途切れる」＋新しい最終文「削る順番のいちばん後ろに、数えた人と数えた時期を示す一行を置いてほしい」。1 は筆者が「短くすること自体に反対するつもりはない」と両立、2 は順序の話をしていない、4 は逆 | — |
| 問題14-70 | 3. 前の週の金曜日までに電話をし、ラケットとくつは自分で用意する | OK | 三条件の重ね：卓球=月・金／「テニスと卓球は…前の週の金曜日までに管理室へお電話ください」／「ラケットと球の貸し出しはしておりません」＋「運動ぐつにはきかえてから」 | — |
| 問題14-71 | 4. 千二百円 | OK | バスケ「一人 二百円」×2（水曜、中学生の息子は「おとなの方といっしょに」で可）＋テニス「一面 八百円」＝1200円。二条件以上 | — |
| 聴解問題1-1番 | 3. 木村先生に電話する | OK | 「空いているか確認しましょうか」→「あ、それは大丈夫だった」で 1 が消え、「先生に電話して確かめてもらえないかな」が最初の一手。連絡と名簿修正は「済んだら」の後 | — |
| 聴解問題1-2番 | 4. 特急・自由席 | **OK（F1 修理を確認）** | 「乗り換えはなしで」→特急、「禁煙車はいっぱい」「タバコは困ります」→「じゃあ、自由席になりますね」。印字選択肢は 新幹線・指定席／新幹線・自由席／特急・指定席／特急・自由席 の実文で、図版依存ではない | — |
| 聴解問題1-3番 | 3. 先輩にげんこうをたのむ | OK | 「吉田さん、先輩に依頼してくれる？先生の方は僕がやるよ」。写真は1年生、紹介文はパートリーダー、表紙は印刷会社から選ぶ | — |
| 聴解問題1-4番 | 3. 研究室の前のけいじを見る | OK | 「私の研究室の前の掲示を見て、宿題を確認してください。友達に聞いたりしないで」 | — |
| 聴解問題1-5番 | 3. 土曜日 | OK | 平日7時はバイト6時までで「ちょっときついな」、「土曜日も平日と同じだ」→「じゃ、土曜だな」。明日=月曜は「月曜日と祝日は、休館日でしょ」で消える | — |
| 聴解問題2-1番 | 2. かみがたが気に入らないから | OK | 「自分でやったら切りすぎちゃって…こんなんじゃ、みんなに笑われちゃうよ。ねぇ、今日学校休んじゃだめ？」。けんかは「電話で仲直りした」、試験は本人が否定 | — |
| 聴解問題2-2番 | 2. 一日に6時間以上寝ている人 | OK | 「一日に、少なくとも六時間は睡眠を取っている人のみ参加できます」。走らせない／過去の参加者も可 | — |
| 聴解問題2-3番 | 1. しどう者になる機会をもらったため | OK | 「大学の陸上部でコーチをしないかと誘っていただきました…早めにそちらの道に進もうと引退を決めました」。大学院は入学済み、成績は良かった側、体力は「まだ戦える」 | — |
| 聴解問題2-4番 | 4. 消しゴムで消して書き直せること | OK | 「自分が納得いくまで何度でも消してやり直せるっていうところが、特にいいと思ってるんだ」。費用は友達の勧めの理由 | — |
| 聴解問題2-5番 | 2. ご飯の量を少なくする | OK | 「健康のためには少し減らしてみましょうか」→「そうしましょう」。味は「これぐらいがちょうどいい」、サラダは「ちょうどいい」、おかずの種類は「これでいきましょう」 | — |
| 聴解問題2-6番 | 3. 開始時間が早かったこと | OK | 「始まる時間はもう少し余裕を持って参加できる設定にしたほうがよかった」。講師一人は「だからこそ」で良かった側、教室は「そんなことなかった」、資料なしは「負担もなくて」 | — |
| 聴解問題3-1番 | 4. 利用する理由 | OK | 「「忙しくて買いに行く時間がない」「お茶を飲みながらゆっくりと買い物ができる」…など多くの意見が出されました」＝利用理由の列挙 | — |
| 聴解問題3-2番 | 1. 日本人の食生活の変化 | OK | 「食事の中身だけでなく、食事のとり方も昔とは大きく異なっています。この講演会ではこのようなことをお話ししたい」 | — |
| 聴解問題3-3番 | 1. 高齢者をサポートする役割 | OK | 「高齢者の体調に変化がないか、確認している…自治体が高齢者一人一人の状況を知り、健康を守ることができる」 | — |
| 聴解問題3-4番 | 1. 植物の種の運ばれ方 | OK | 「植物は動物のように歩けないので、いろいろな方法で仲間を増やすんです」＋風・アリ・動物の体の三例。タンポポは最初の一例のみ | — |
| 聴解問題3-5番 | 1. 和紙を作る職人を目指したきっかけ | OK | 「和紙を通してみる光の柔らかさ、美しさに感動しました…和紙作りの技術を一から学びたいと思い立って」 | — |
| 聴解問題4-1番 | 2. そう？色も悪くないと思うけどね。 | OK | 「色はともかく使いやすいのよね」＝色は評価の外に置く含み。1 は「完璧」で含みを取り違え、3 は逆 | — |
| 聴解問題4-2番 | 2. 本当、期待してたのにね。 | OK | 「いまいちだったね」＝期待外れ。1 は逆評価、3 は含みの取り違え | — |
| 聴解問題4-3番 | 3. あ、午後からの出勤だそうです。 | OK | 「今日、お休みだったっけ？」＝今日の勤務の確認。1 は感想のずれ、2 は昨日にすり替え | — |
| 聴解問題4-4番 | 1. まだ戻られてないんですか？ | OK | 「昼ごはん食べに行ったきりですね」＝出たまま戻らない。2/3 は状態を逆に取る | — |
| 聴解問題4-5番 | 1. 間に合ってよかったですね。 | OK | 「乗り遅れるところでしたよ」＝結果的には乗れた。2 は乗れなかったと誤読、3 は無関係 | — |
| 聴解問題4-6番 | 3. 森君、いつも時間守るのにね。 | **OK（F4 修理後の新クリップ）** | 「森君が遅刻なんて、ありえないよね」＝普段は遅れない前提への同意。1 は逆、2 は事実の取り違え | — |
| 聴解問題4-7番 | 3. それはひどい目にあったね。 | **要修正（R2-F2 の一方）** | 鍵自体は妥当（「電車の事故で、昨日は会社から歩いて帰ったんだ」＝苦労話に同情）。問題は item ではなく **紙全体**：問題11(4) の中文一面が「電車が長く止まった日…勤め先から歩いて帰った」で同一題材（§6.3） | 聴解側は差し替え不能（実クリップ）。問題11(4) を別題材に再執筆するか、当スロットを再抽選する |
| 聴解問題4-8番 | 3. そういうことなら、仕方ないね。 | OK | 「先輩が休みだから私がやらざるを得なくなって…」＝やむを得ない事情。1 は逆、2 は感情の取り違え | — |
| 聴解問題4-9番 | 2. え、何歳でもいいんですか。 | OK | 「年齢を問わず参加できる」＝制限なし。1 は逆、3 は別の制限の読み込み | — |
| 聴解問題4-10番 | 1. えーっと、荷物が置いてありますけど…。 | OK | 「この席、空いていますか」＝空席の確認。2 は「閉める」との混同、3 は満員の店の言葉 | — |
| 聴解問題4-11番 | 1. 大人でもそんなに難しいの？ | OK | 「子供用の…半分も解ければいい方だよ」＝大人でも難しいという含み。2/3 は含みを逆に取る | — |
| 聴解問題5-1番 | 2. 飾りをつけて汚れを隠す。 | OK | 「やっぱり、ペンキが見えないように、なにか縫い付けるのがいいんじゃないですか」→「わかりました、そうします」。洗剤は「生地がダメになったら困ります」、青ドレスはセリフ変更不可、母のドレスは「申し訳ないよ」で消える | — |
| 聴解問題5-2番-質問1 | 2. 2番のコース | OK | 「湖のコースはハイキングに二時間近く歩く…ちょっと自信ないなぁ。作家の家とかを回るほうならいいけど」→「じゃあ午前中はそれにして」 | — |
| 聴解問題5-2番-質問2 | 4. 4番のコース | OK | 「主人公が書道の名人…筆とかの道具の話もよく出てくるんだ。だからすごく興味があって、午後はそれでいいなあ」＝四番の筆作り体験 | — |

**Walkthrough totals: 101 rows — 100 `OK`, 1 `要修正`, 0 `自動不合格` at ITEM level.** The
automatic fail (R2-F2) is a whole-paper property, not an item defect, and is filed against the
pair 問題11(4) ↔ 聴解問題4-7番.

---

## 4. Verification of round 1's five repairs — measured, not read off the disposition

### 4.1 First, a correction the rest of this section depends on

`qa/root-cause-dispositions-20260909.md` states of F1: **"Re-composed on the SAME seed; only
問題1-2 moved."** That is **false**. Measured:

- **25 of 29 slots carry a different clip** than the composition round 1 reviewed. Only
  問題2-1/2-2/2-3/2-4/2-6-class slots and 問題5-2 survived; I verified it two independent ways:
  - 16 of the 27 deciding quotes in round 1's own walkthrough are **absent** from the current
    `聴解スクリプト.txt` (e.g. 問題1-3's 「とりあえず、貼り紙とかして訂正の案内をしてください」,
    問題3-4's 「仲間言葉として使うという考え方」, 問題4-1's 「本屋行くついでにご飯でも食べない」,
    問題5-1's 「店内に…」), and several that ARE present have moved slot (round 1's 問題1-1 quote is
    now at 問題1-4; its 問題4-2 quote is now at 問題4-3);
  - the source mix moved from **shinkanzen 3 / soumatome 1** (round 1's reading) to
    **shinkanzen 1 / soumatome 3** (`logs/choukai_draws.json`, measured).
- The **cause is benign and visible in the code**: F4's repair puts the `avoid_slot` bar inside
  `freshest()` (`tools/compose_choukai.py` L300–320), which runs for **every** slot, so it
  changes rng consumption globally even at a fixed seed. Nothing is wrong with the composer.
- The **consequence is not benign**: round 1's §5 (all 30 option sets, all 29 script bodies, the
  22 official keys, the 8 blind-solved textbook keys, the 問題3 lexical-signature column, the
  問題5-2 printing read) is evidence about text that no longer exists, and **nothing re-ran the
  whole-paper topic pass** on the new listening half. That is how R2-F1 and R2-F2 shipped.

I therefore re-ran all four composed-paper checks from scratch, on all 30 items rather than
sampling.

### 4.2 F1 — figure-dependent clip. **VERIFIED CLOSED, at the root.**

- `logs/choukai_bank.json` carries `figure_dependent` on exactly **2 of 402** records:
  `2021-12:問題1-5` and `2022-12:問題1-2`.
- **Independently re-derived, not trusted:** I ran my own predicate over every record's declared
  `options` — "every option is bare digits, ≥3 options" — and it returns **exactly those two and
  nothing else**, both already flagged `True`. No unflagged figure item is hiding in the bank.
- `tools/compose_choukai.py` L275 `if rec.get("figure_dependent"): skipped_figure.append(...)`
  — a hard `continue`, with the exclusion **printed** rather than silent.
- Residual, stated: **62 item records carry no `figure_dependent` field at all** (問題1×15,
  問題2×10, 問題3×14, 問題4×23 — the textbook half). `rec.get()` treats absent as false, which is
  the safe default here because none of the 62 has a digits-only option set. But the field is
  written by `build_choukai_bank.py` and not by `build_textbook_bank.py`, so a future
  figure-bearing textbook declaration would be drawn without the flag ever being consulted.
  Recorded in the root-cause table, not filed as a paper finding.
- **In the paper:** shipped 問題1-2番 is `2021-07:問題1-2`, printing 「新幹線・指定席／新幹線・自由席
  ／特急・指定席／特急・自由席」. `grep -c '!\['` on `聴解.md` = 0 and no item needs an image. My
  blind solve answered it 4, matching the key.

### 4.3 F2 — key morpheme printed in its own stem. **VERIFIED CLOSED, and the fairness test holds.**

- Stem is now 「四月から（　）体制になり、これまでなかった部署もできる。」 Target `新〜(新体制)` is
  unchanged in `test_spec.json` and `logs/ledger.json` (no substitution).
- I re-implemented round 1's predicate — a **kanji** of the keyed option occurs in its own stem,
  is carried by **no other option**, proper nouns stripped — and ran it over 問題3–6 of this paper
  and of every corpus paper:

| paper | hits |
|---|---|
| **20260909_1** | **0** |
| all ten `tests/imported-*` | 0 each |
| 20260907_1, 20260904_3 | 0 |
| 20260904_2 | 1 (問題4-20 返品 / 商品) |
| 20260827_2 | 1 (問題4-19 腹が決まって / 決意) |

  So the predicate still fires on the two other papers round 1 named, fires on no official
  sitting, and now scores 0 here. **Note for whoever writes the gate check: the predicate must
  be restricted to kanji.** A character-level version fires on kana in **all ten officials**
  (2–3 hits each) and would be refuted on arrival.
- The new disqualifier works: 「これまでなかった部署もできる」 kills 旧 and 前 (a reversion cannot
  create a department that never existed); 現 still fails 「四月から〜になる」 as a change-destination.

### 4.4 F3 — two closings on one skeleton. **VERIFIED CLOSED, and the pair re-derived on the NEW skeleton AND the NEW label**, as round 2 must.

The 13 essay closings as shipped:

| surface | closing sentence | skeleton | label |
|---|---|---|---|
| **問題9** | …その一枚がどちらを向いて立つのかを決め**ておきたい**。 | 〜ておきたい（筆者の意志） | 主張 |
| 問題10(1) | 名前は似ていても、届く先が違う。 | 対句・体言止め | 説明 |
| 問題10(2) | 何もお持ちにならない場合も、その旨をお知らせください。 | 依頼（実用文） | 実用文・分類外 |
| 問題10(3) | …配られた日のうちに休む日を決めていた家ほど、行事に出られた回数は多かった。 | 相関（〜ほど…） | 条件提示 |
| 問題10(4) | しきたりというものは、…はじめから組になっているのかもしれません。 | 〜かもしれません | 随筆 |
| 問題10(5) | 地下の用具室に置いていかれますと記録が残らず、…続きます。 | 帰結（実用文） | 実用文・分類外 |
| 問題11(1) | 断る余地のない頼み**だけが**、人を遠ざける。 | 〜だけが… | 随筆 |
| 問題11(2) | 姿勢を変えた回数が、そのまま朝の軽さになっていた。 | 〜ていた（発見） | 意外な観察 |
| 問題11(3) | ただ、二つの問いは、返ってくるものが初めから違うのです。 | 〜のです（留保） | 反論応答 |
| 問題11(4) | …途中で寄れる一か所を先に決めてあった人**だけが**、…たどり着いていた。 | 〜だけが… | 条件提示 |
| 問題12(A) | 終わりの来る三分と自分で払う三分とを、頭より先に体が選び分けているのだと思う。 | 〜のだと思う | 意外な観察 |
| 問題12(B) | それでも、平均という一つの数字ではかると、…数の外に落ちます。 | それでも〜 | 反論応答 |
| **問題13** | 削る順番のいちばん後ろに、数えた人と数えた時期を示す一行を置い**てほしい**。 | 〜てほしい（読者への依頼） | 主張 |

- **〜ておきたい over the 13 finals: 1** (問題9 only). The token round 1 measured at 2 is at 1.
- **The pair did NOT survive re-clothed.** The two halves now carry **different skeletons**
  (筆者の意志 〜ておきたい vs 読者への依頼 〜てほしい) and **different moves** — 問題9 is a
  priority inversion (「何を載せるかを考える前に…決めておきたい」: settle the thing that actually
  decides before the obvious thing), 問題13 is concession-then-ranking (preceded by
  「削るなという話ではない。」: cut, but rank this one line last). They still share the **label**
  主張 at 2 of 13, which is exactly the shared cap and therefore compliant, not a finding.
- 〜てほしい occurs **3×** in the 問題10–14 prose, but it is keyed nowhere in 問題7/8/9, so the
  key-exposure rule does not reach it and the new closing plants nothing.
- Label tally re-derived from the table above: 主張 2 / 説明 1 / 実用文・分類外 2 / 条件提示 2 /
  随筆 2 / 意外な観察 2 / 反論応答 2 = 13, every shape at or under 2.
- 「〜だけが」 remains at 2 (問題11(1), 問題11(4)) — at the shared cap, so compliant. Recorded as an
  observation for the second round running, since all ten officials score 0 on it.

### 4.5 F4 — clip repeating the previous paper in the same slot. **VERIFIED CLOSED.**

Measured over all 29 item slots and all 5 preambles of `logs/choukai_draws.json`:

- **same-slot repeats vs `20260907_1`: 0.** (Round 1's offender 問題4-6 = `2023-12:問題4-6` is now
  `2021-07:問題4-6`.)
- preamble repeats vs the previous paper: 問題1 preamble `2024-12:問題1-preamble` is the same as
  20260907_1's. `previous_slot_clips()` returns `rows[-1]["clips"]` only — **preambles are not
  covered by the bar.** Not filed: `exam-qa-review` §4 check 1 is about clip ids in item slots,
  the preamble is announcer boilerplate, and round 1 recorded preamble collisions as clean under
  the same reading. Named in the root-cause table so the next person decides it deliberately.
- No clip and no preamble is used twice **within** the paper (0 duplicates).
- One two-back same-slot repeat: `2023-07:問題4-11` at 問題4-11, also in `20260904_3`. The rule
  covers the immediately-previous paper only, so this is inside the rule; stated because round 1
  reported a different two-back repeat and that one no longer exists.
- The composer's starvation carve-out printed nothing, so no slot needed the bar dropped.

### 4.6 F5 — `shipped_surface` on the re-authored records. **VERIFIED CLOSED, in both files.**

| file | entry | `theme` (drawn, untouched) | `shipped_theme` | `shipped_surface` | `note` |
|---|---|---|---|---|---|
| `test_spec.json` | `reading_topics[5]` | 住まい | 交通 | `問題12(A)` | present |
| `test_spec.json` | `reading_topics[10]` | 働き方 | スポーツ・余暇 | `問題14` | present |
| `logs/ledger.json` | `reading_topics[5]` | 住まい | 交通 | `問題12(A)` | present |
| `logs/ledger.json` | `reading_topics[10]` | 働き方 | スポーツ・余暇 | `問題14` | present |

All three required fields present in both files, drawn strings and drawn `theme` untouched, and
the `note` quotes the deciding lines. `make check`'s new
`check_reauthored_shipped_surface()` names **18** grandfathered pre-rule ids and does **not**
name `20260909_1` — it passes on merit. Spec ↔ ledger compared field for field: same `seed`
(70398536), same `pools_sha` (4119aed1e4b0), **all 11 item categories byte-identical**, no
`harvest_sha` in either file (so no date-shaped fabricated sha).

---

## 5. 聴解 — all four composed-paper checks, re-run on the new composition

`聴解_チャプター.json` declares `"source": "composed"`, `"bank_version": 2`,
`"script_sha": "3efcc7f2675d"` — the same sha this report is written against. Per §4 the
authoring/register/pacing family (場面 mix, 決め手 spread, 質問型 balance, distractor shape, key
length, closing turns, voice casting) is **out of scope** and no セクション構成表 exists or should.
Source mix as measured: **mondaireishuu 4 / official 21 / shinkanzen 1 / soumatome 3**, from
eight sittings.

**Check 1 — no clip repeats the previous paper in the same slot: PASS, 0 collisions.** §4.5.

**Check 2 — the audio round-trips.**

```
python3 tools/choukai_segment.py tests/20260909_1/聴解.mp3
ok  20260909_1   46.5 min  LUFS -15.48  問題1:5  問題2:6  問題3:5  問題4:11  問題5:2
```

**5/6/5/11/2 recovered exactly** against the composed script. Artifact ordering is clean:
`聴解スクリプト.txt` 18:48:51 → `聴解.mp3` 18:49:29 → `聴解_チャプター.json` 18:49:31; HTML 19:00:55
postdates both Markdown sources (18:48:51 / 18:59:10). `logs/upload_manifest.json` carries this
test's mp3, and the gate raises no release FAIL for it.

**Check 2b — chapter marks and the number-call seam, re-derived arithmetically.** I recomputed
every chapter offset from the bank's own audio spans (`end − start`, `answer_pause`, `guard_s`
0.25) and compared to `聴解_チャプター.json`'s 34 marks (5 section headers + 29 items):

- for every `needs_number_call: False` clip, the next mark lands within 0.3–1.0 s of the
  predicted offset (encode rounding);
- for every one of the 8 `needs_number_call: True` textbook clips, the next mark lands **3–7 s
  later** than predicted — the harvested 「N番。」 span prepended in front of the clip, exactly as
  designed;
- each section header → first item gap is a **constant +2.75 s** across all five sections;
- the eight number calls needed are 4番, 5番, 1番, 1番, 2番, 3番, 7番, 10番 — all ≤ 11, inside the 11
  harvested spans in `logs/choukai_number_calls.json`, and all eight appear correctly in the
  script text (「4番。授業で、男の先生が、話しています。」 etc.);
- duration 2788.32 s = 46.47 min, matching the segmenter's 46.5 min.

The **seam at the repaired slot** is clean: 問題1-1番 ends at 285.95, which is exactly where
問題1-2番 starts; 問題1-2番 is an official clip in its own slot, so its spoken 「2番。」 is the
source's own and needs no harvested call.

**Check 3 — a mis-drawn slot would print one sitting's options over another's audio. Verified for all 30 items, not two.**

- **Every one of the 29 drawn clips' script lines occurs verbatim in `聴解スクリプト.txt`** —
  29/29 clean, line by line, furigana-normalised.
- **Every printed option set matches its drawn clip's own option array**: 問題1/問題2/問題5-2's
  printed options (0 missing from `聴解.md`) and 問題3/問題4/問題5-1's spoken options (0 missing from
  `聴解スクリプト.txt`). No slot is mis-drawn.
- `詳細解説.json` and `詳細解説.vi.json` were rewritten by `make mp3` and are **in sync with the new
  composition**: 30 entries each, 0 options absent from the shipped sources, 0 stored `script`
  fields absent from the shipped script. I read a sample of `options_analysis` lines (問1-2, 問3-4,
  問4-7) — each names the fact that kills that option; none is scaffold-shaped.

**Check 4 — a 聴解 mis-key means the BANK is wrong.** All **30** keys (including 問5-2-1 and
問5-2-2) match the bank's `answers`/`answer` field exactly, and all 30 match my independent blind
solve. Unlike round 1's composition, **every drawn textbook clip now carries an `answer` in the
bank**, so no key rests on a reviewer's solve alone. No mis-key.

### 5.1 Answer positions

All **71** 言語知識・読解 positions match `test_spec.json["answer_positions"]` exactly — re-derived
field by field, **zero mismatches**. Overall 71-item spread 1:16 / 2:18 / 3:18 / 4:19.

The 30 聴解 positions are exempt by construction (`check_answer_positions` sets
`skip_choukai = ck_origin == "composed"`); the spec's reserved 聴解 arrays differ from the shipped
keys, correctly. But the balance the composer targets instead is where **R2-F3** lives — §5.2.

### 5.2 聴解 key balance — R2-F3

Shipped keys per section, and the same measurement over the ten officials:

| section | 20260909_1 | worst official section (10 sittings) |
|---|---|---|
| 問題1 (5 items, 4 options) | **3, 4, 3, 3, 3 → key 3 four times of five** | 3 of 5 (2025-07: 3,3,3) |
| 問題2 (6 items, 4 options) | 2, 2, 1, 4, 2, 3 → max 3 of 6 | 3 of 6 |
| 問題3 (5 items, 4 options) | **4, 1, 1, 1, 1 → key 1 four times of five** | 3 of 5 (2023-07, 2024-12) |
| 問題4 (11 items, 3 options) | 1×4, 2×3, 3×4 → max 4 of 11 | 4–5 of 11 |
| 問題5 (3 items) | 2, 2, 4 | 2025-12: 2,3,2 (same shape) |

**In 30 four-option official sections across ten sittings, the maximum is 3-of-5 / 3-of-6. Never
4.** This paper has **two** sections at 4-of-5. A candidate who marks 3 for all of 問題1 and 1 for
all of 問題3 scores 8/10 on those two sections without listening.

Corpus recurrence, measured by reading every paper's keys: **8 of 25** generated papers show a
section at ≥4 (`20260810_1`, `20260818_1`, `20260819_1`, `20260821_1`, `20260827_1`,
`20260904_1`, `20260904_3`, `20260909_1`), and **20260909_1 is the only one with two such
sections** — the worst instance on disk. All ten officials: max 3. Fairness test passes.

**Root cause, in the code:** `tools/compose_choukai.py::key_spread()` pools
`問題1 + 問題2 + 問題3 + 問題5` into **one 19-key bucket** and penalises only that bucket's
deviation. This paper's pooled distribution is 1:5 / 2:5 / 3:5 / 4:4 — near-perfect, penalty
≈0.16 — while two of its sections are monocultures. The objective is blind to per-section skew
**by construction**, and nothing downstream measures it: `check_answer_positions` skips 聴解
entirely for a composed paper.

### 5.3 聴解問題3 lexical-signature read (the `20260904_1` 「そのまま」 class)

Read the 20 spoken 問題3 options as one column. Every content token that occurs in ≥2 options
across different items also occurs in at least one **distractor**: `利用` = 3-1番 options 1 and 3
(distractors) + 3-1番 option 4 (key) + 3-3番 option 4 (distractor); `理由` = 3-1番 key + 3-4番
option 4 and 3-5番 option 3 (both distractors); `高齢者` = 3-3番 key + 3-3番 option 3 (distractor).
**No key-only signature.** The gate's `check_choukai_key_exclusive_token()` agrees (silent).

### 5.4 問題5-2番 printing

Both 質問1 and 質問2 print the same four options in the same order (「1番のコース」…「4番のコース」),
with no deciding attribute printed beside a name. Compliant with `jlpt-exam-structure` §問題5-2番.

### 5.5 例 — the predicate is REFUTED, and I state what it cost

There is no 例 block and the marksheet says why. I tested the obvious finding: the 問題1 preamble
clip's audio span is **174.0 s** while its banked `text` is only the two narration lines (~15 s),
so roughly 159 s of the MP3 is 例 dialogue the composed script does not transcribe and the booklet
prints no options for. Same shape at 問題3 (81.5 s) and 問題4 (146.9 s).

**Refuted:** all ten `tests/imported-*` officials carry the identical disclaimer
(「この回の出典には練習問題「例」の行がないため、例の欄はありません。」) for the identical reason, and
their MP3s carry the same untranscribed 例 audio. A predicate that fails ten real sittings is not
a finding. Recorded as an observation so a third round does not re-derive it.

---

## 6. Whole-paper and cross-test topic table

### 6.1 The record does not describe the paper — R2-F1

`logs/topics.json`'s `20260909_1` row carries all eight required keys (`surfaces`, `themes`,
`closing_moves`, `voices`, `claim`, `persona`, `shapes`, `notes`), each verified PRESENT by
reading the row. **But its 聴解 half records the SUPERSEDED composition.** Measured, clip by clip:

| slot | `surfaces` / `themes` record | what the paper actually ships |
|---|---|---|
| 聴解問題1-1番 | 大学の授業で休んだときの宿題は掲示で確かめる / 教育 | 音楽教室の事務室、木村先生に電話（`2021-12:問題1-1`） |
| 聴解問題1-2番 | 生花サークルの留守番電話…ポスターの写真の位置 / 文化・伝統 | 駅の窓口で特急の自由席を買う（`2021-07:問題1-2`） |
| 聴解問題1-3番 | 貼り紙で訂正の案内 / 働き方 | オーケストラのパンフレット、先輩に原稿を依頼（`2025-12:問題1-3`） |
| 聴解問題1-4番 | 市民文化祭のステージ演奏への応募 / 文化・伝統 | 授業を休んだときの宿題確認（`mondaireishuu:問1-1`） |
| 聴解問題1-5番 | ホテルの秋のフェアの企画案 / 働き方 | 図書館の開館時間、土曜に来る（`soumatome:cd2-32`） |
| 聴解問題2-5番 | 保育園の先生が実習生に…目の高さ / 教育 | 弁当のご飯の量を減らす（`2025-07:問題2-5`） |
| 聴解問題3-1番 | 片付けの効果 / 住まい | 通信販売を利用する理由（`mondaireishuu:問3-1`） |
| 聴解問題3-2番 | 鉄道の写真家の講演 / スポーツ・余暇 | 日本人の食生活の変化（`shinkanzen:cd2-63`） |
| 聴解問題3-3番 | 通信販売を利用する理由 / 消費・経済 | 移動スーパーの高齢者見守り（`2022-12:問題3-3`） |
| **聴解問題3-4番** | **仲間言葉としての方言 / 文化・伝統** | **植物の種の運ばれ方**（`2021-07:問題3-4`） |
| 聴解問題3-5番 | 社長の話、社員の節電 / 環境 | 和紙職人を目指したきっかけ（`2023-12:問題3-5`） |
| 聴解問題4-1〜4-8, 4-10, 4-11 | ten different one-liners | ten **different** one-liners |
| **聴解問題5-1番** | **和菓子の新商品セットの宣伝の貼り紙 / 消費・経済** | **高校演劇部の衣装、飾りで汚れを隠す** |

**24 of 29 聴解 rows in `surfaces`, `themes` AND `shapes` describe items the paper does not
contain.** Only 聴解問題2-1〜2-4, 2-6, 4-9 and 5-2番 are right.

The `notes` field's 聴解 draw audit states four things that are **false of the shipped draw**,
each measured against `logs/choukai_draws.json`:

| `notes` claim | measured |
|---|---|
| "Source mix … shinkanzen 3 / soumatome 1" | shinkanzen **1** / soumatome **3** |
| "問題4-6 is `2023-12:問題4-6`, which 20260907_1 also spent in 問題4-6" | 問題4-6 is `2021-07:問題4-6`; **0** same-slot repeats |
| "`compose_choukai.py` … offers no per-slot exclusion, so the only way to move that one slot is to re-draw all 29" | it now has one (L300–320); the whole half moved |
| "One clip repeats 20260904_3 in the same slot, `2021-07:問題5-1` at 問題5-1" | 問題5-1 is `2022-07:問題5-1`; the actual two-back repeat is `2023-07:問題4-11` at 問題4-11 |
| "聴解問題3-4番 … `shinkanzen:cd2-59` here" | 問題3-4 is `2021-07:問題3-4`; cd2-59 is not drawn at all |

Nothing in the row records that the 聴解 half was re-composed at all.

**Why this is `要修正` and not `自動不合格`, decided by counting as the skill instructs.** The
automatic-fail bullet is "a surface's `theme` in `test_spec.json` disagreeing with the same
surface's `theme` in `logs/topics.json` **where `topics.json` relieves a quota or headline
collision the spec value creates**." The spec's `listening_scenarios` are unspent (§7.2), so
there is no spec-vs-topics theme pair of that kind; and where the record differs from the shipped
tagging, the **record is the worse value, not the more permissive one** — recorded 働き方 6 vs
shipped ≈3, and recorded 聴解問題5-1番 = 消費・経済 vs shipped 教育, which if anything *creates* a
two-back overlap rather than relieving one. The record is not dodging a cap. So: a bookkeeping
desync, per the skill's own test.

**But it is not merely stale bookkeeping**, and four consequences are live:

1. **The gate's own `聴解問題3-4番=文化・伝統 (also 20260904_3, also 20260907_1)` WARN is a statement
   about a clip that is not in this paper.** Its disposition — "the tag itself is not negotiable —
   a 概要理解 talk about 方言 is 文化・伝統" — describes a 方言 talk the paper does not contain. The
   shipped 問題3-4番 is a children's-programme talk on how plant seeds travel (科学・技術), which
   collides with neither previous paper's tag. The WARN is an artifact of the record, not of the
   paper.
2. **`used_subjects_by_theme()` builds the NEXT draw's `avoid` list from this row** (skill §5,
   since 2026-09-07). The next paper will be told to avoid 25 subjects this paper never shipped,
   and will not be told to avoid the ones it did.
3. **`shapes` is the ONLY record of what errand each 聴解 item ran**, and the errand-archetype rule
   is read off that column and nothing else. 24 of 29 entries describe the wrong errand.
4. **The whole-paper topic pass (step 5) has never been run against the shipped listening half.**
   That is not an inference — R2-F2 is what it would have caught.

### 6.2 Headline theme set, re-tagged from the SHIPPED content

I re-tagged the two composed headline surfaces from what the shipped clips are actually about,
using `level_data.THEMES`'s closed 20-value vocabulary:

| slot | 20260904_3 (two back) | 20260907_1 (previous) | **20260909_1 as shipped** |
|---|---|---|---|
| 問題9 | 環境 | 食 | 地域活性化 |
| 問題12 (A/B) | 科学・技術 | 住まい | 交通 (re-authored) |
| 問題13 | 医療・福祉 | 働き方 | メディア・情報 |
| 問題14 | 防災 | 旅行・観光 | スポーツ・余暇 (re-authored) |
| 聴解問題5-1番 | 交通 | 行政・手続き | **教育** ← record says 消費・経済 |
| 聴解問題5-2番 | 消費・経済 | 文化・伝統 | 旅行・観光 |

- **Rule 1** (five headline surfaces, five different themes): satisfied — 地域活性化 / 交通 /
  メディア・情報 / スポーツ・余暇 / 教育 / 旅行・観光, all distinct. (A high-school drama club with a
  teacher and two students is 教育; 文化・伝統 would also be arguable, and I say so because it
  matters: under 文化・伝統 the rule-4 intersect against 20260907_1 becomes **two**, not one. 教育 is
  the reading I defend — the deciding voice is 女2, the teacher, and the errand is a school
  performance, not a cultural practice.)
- **Rule 2** (a 読解 headline theme appears nowhere else in the 読解 half): satisfied.
- **Rule 3** (all thirteen 読解 surfaces differ): satisfied — 13 distinct themes with 問題12 A/B
  counted once.
- **Rule 4, one paper back**: intersect = **{旅行・観光}**, carried only by the composed
  聴解問題5-2番. WARN, not FAIL, per the 2026-09-09 amendment; unrepairable without re-drawing the
  whole listening half. The gate prints exactly this.
- **Rule 4, two papers back**: intersect = **{交通}** only — 1 ≤ 1, within budget. Round 1's
  two-back {交通, 消費・経済} pair no longer exists once 聴解問題5-1番 is tagged from the shipped clip,
  and the gate has correspondingly **stopped printing the 消費・経済 note** (I grepped the whole
  `make check` output: absent). Still worth carrying forward: 問題12 was moved to 交通 to clear the
  previous-paper 住まい collision, and 交通 is 20260904_3's 聴解問題5-1番 headline, so the next paper
  has zero two-back headroom on 交通.

### 6.3 Cross-surface subject check — R2-F2 (automatic fail)

Built the table one row per surface including each 聴解 item. **One subject appears twice in the
paper:**

- **問題11(4)** — the whole 中文 passage: 「電車が長く止まった日のことを、あとから調べた。**勤め先から
  歩いて帰った**四十人ほどに、通った道すじと家に着いた時刻を書き出してもらった。」
  (`tests/20260909_1/言語知識・読解.md` L361)
- **聴解問題4-7番** — the stimulus: 「7番。電車の事故で、昨日は**会社から歩いて帰った**んだ。」
  (`tests/20260909_1/聴解スクリプト.txt` L196), key 3 「それはひどい目にあったね。」

Same subject — walking home from work because the trains stopped — in two registers, at
near-identical wording (勤め先から歩いて帰った / 会社から歩いて帰った). `exam-qa-review` §5: "Fail on:
any subject twice in this paper (any register)", and the automatic-fail list carries "**a topic
repeated within the paper** or from the previous test". This needs no fairness test: it is an
existing binding rule applied as written, not a new predicate.

It is also **not** a keyed leak — 聴解問題4-7番 is decidable from its own stimulus and 問題11(4)'s
four items turn on the stopping-place finding, not on the hardship. The defect is the repetition
itself, and it is **repair collateral from the re-composition**: the previous draw had
`shinkanzen`-sourced 「最初は引き受けなきゃよかったかなと思ったんだけど」 in this slot; the F1/F4 fix
moved 問題4-7 to `soumatome:cd1-42`, and no one re-read the paper against the 読解 half afterwards.

Everything else in the cross-surface read is clean, including the pairs I looked hardest at:

- 問題14's flyer shares **no decisive detail** with any listening item. Its deciders are 卓球 月・金 /
  前の週の金曜日までの電話 / ラケット持参 / 一人二百円 / 一面八百円; I checked each against every
  number and errand spoken in the 聴解 half by hand as well as relying on the gate's
  `問題14 shares no decisive number with any 聴解 item` line. (Note the old draw's 卓球部 clip at
  問題4-3 is gone, which would have been a second collision.)
- **No two 聴解 items run the same errand** (29 distinct errands read off the shipped scripts).

Three near-misses I measured and did **not** file, recorded so round 3 does not re-derive them:

1. 聴解問題2-5番 (弁当: ご飯の量・塩分・健康) ↔ 聴解問題3-2番 (日本人の食生活の変化: 米の消費量・油).
   Both touch rice quantity and health in Japanese meals, but the errands differ (a product
   decision vs a lecture's theme) and neither's deciding line is available to the other.
2. 聴解問題2-3番 (マラソン選手の引退) ↔ 聴解問題4-9番 (市民マラソン大会の年齢制限). A shared domain
   word, not a shared subject.
3. 問題11(3) (「わかりましたか」vs 事実をたずねる問い) ↔ 聴解問題1-4番 (休んだときの宿題確認の手順).
   Both classroom procedure; the subjects (question design vs absence procedure) are distinct.

### 6.4 Closing moves and the SENTENCE-SKELETON second read

Done in full at §4.4 — the 13 finals, their skeletons and their labels, with the F3 pair
re-derived on both. No shape and no skeleton exceeds 2; the only pair at 2 on one skeleton is
「〜だけが」 (問題11(1), 問題11(4)), which is the shared cap.

**Keys did not inherit the closings:** the 13 closings resolve to eleven distinct sentence
skeletons, and the 20 読解 keys spread 1:6 / 2:3 / 3:3 / 4:6 with a 33 % dominant rank — no
cluster of "human/attitude choice beside strawmen".

One stale narration, not filed: `notes` justifies 問題12(A) = 意外な観察 by "the passage states the
mismatch — **the room's total light is unchanged** — and the closing gives the cause", which
describes the **discarded 住まい draft**, not the shipped 交通 passage. A later paragraph in the same
field does record the re-author and asserts the label carried over. I checked the label against
the shipped text on its own merits and it holds (「これで待つ人は減るだろうと思っていた。ところが、
そうはならなかった。」 states the mismatch; the closing gives the cause).

---

## 7. Provenance & spec blueprint audit

### 7.1 Target item match (問題1–8)

Every tested item matches the EXACT target in `test_spec.json["items"]`, in order — 問題1
驚く/争う/冷静/自動券売機/体力; 問題2 講義/遠足/一通り/抑える/預ける; 問題3 〜嫌い(人嫌い)/浅〜(浅学)/
新〜(新体制); 問題4 要領/発車/真っ黒/無邪気/ふさぐ/足が出る/響き; 問題5 要するに/落ち込む/重宝する/
交渉する/いかに; 問題6 損なう/引き止める/まして/徹夜/属する; 問題7 all 12 forms in spec order; 問題8
目的表現(〜ように…する)/〜でなければ/補足追加(〜なお…)/同時進行(〜ながら…する)/義務当然(〜ねばならない)
at items 43–47. **No unrecorded substitution**, F2's stem rewrite included (the target did not
move).

### 7.2 `listening_scenarios` / `quick_response` — measured, feeding §9 disposition (b)

`test_spec.json` draws **21 `listening_scenarios` + 11 `quick_response` = 32 entries**, and
**zero** of their drawn strings occur anywhere in the shipped `聴解.md` or `聴解スクリプト.txt`. All
32 shipped nothing. Corpus-wide: **800** such entries across the 25 generated specs. This
confirms the deferred row's measurement exactly.

Extending §6.1 of the skill to `listening_scenarios` as instructed — "map every 聴解 item's
narration to a drawn scenario; an authored item matching no drawn entry (while another drawn entry
went unused) is an unrecorded substitution" — is **not applicable** to a composed paper: no 聴解
item is authored from any drawn entry, all 21 went unused, and that is the deferred defect itself
rather than a substitution. Stated rather than skipped.

### 7.3 Copyright non-reproduction — re-run on every 読解 surface, boilerplate stripped

The skill requires a re-authored surface's provenance scan to be re-run, because the scan that
cleared the pre-fix text is evidence about text that no longer exists. F3 changed 問題13's final
sentence, so 問題13 is in scope alongside 問題12 and 問題14. Longest shared **contiguous** run,
passage prose and flyer apparatus only, with the official 問題 instruction formulas stripped (they
are shared by construction and otherwise report as 37–58-char "hits"):

| surface | vs 24 previous generated | vs 10 imported officials | vs 31 `refs/*/booklet.md` |
|---|---|---|---|
| 問題9 | 9 | 9 | 9 |
| 問題10 | **16** 「いただき、ありがとうございます。」 | **16** (same) | **16** (same) |
| 問題11 | 13 「にどう思われるかを気にして」 | 10 | 11 |
| 問題12 (re-authored) | 12 「と思っていた。ところが、」 | 7 | 11 |
| **問題13 (F3-re-closed)** | **11** 「る。（中略）では、なぜ」 | **9** 「てほしい。（注1）」 | **9** (same) |
| 問題14 (re-authored) | 13 「ご自分でお持ちください。・」 | 10 | 10 |

**Maximum anywhere: 16 characters**, and that one is a fixed business-letter formula in
問題10(2)'s email. Threshold is 20. Nothing approaches an apparatus lift, and no option SET of
proper nouns is shared with any official 大問. Invented flavour details read as N2-simplified
inventions (「およそ二割」「五分の一ほど」「三倍」 — no decimals, no cited source).

---

## 8. Findings table

| id | item | class | tier | mechanical / authoring | evidence | status |
|---|---|---|---|---|---|---|
| **R2-F1** | `logs/topics.json` row `20260909_1` | the record describes a paper that was not shipped | **C (要修正)** | **mechanical** (record / pipeline) | 24 of 29 聴解 rows in `surfaces`, `themes` and `shapes` name clips the paper does not contain (§6.1 table): 聴解問題1-2番 still records the FIGURE item the F1 fix removed (「生花サークル…ポスターの生花の写真の位置」), 聴解問題3-4番 records 方言/文化・伝統 where the paper ships 植物の種の運ばれ方, 聴解問題5-1番 records 和菓子/消費・経済 where the paper ships 高校演劇部の衣装. `notes` asserts "Source mix … shinkanzen 3 / soumatome 1" (actual 1/3), "問題4-6 is `2023-12:問題4-6`" (actual `2021-07:問題4-6`), "`compose_choukai.py` … offers no per-slot exclusion" (it now does), and "`2021-07:問題5-1` at 問題5-1" repeats two back (actual `2022-07:問題5-1`; the real two-back repeat is 問題4-11). Nothing records that the 聴解 half was re-composed. Consequences: the gate's 聴解問題3-4番 WARN is about an absent clip; `used_subjects_by_theme()` seeds the next draw's avoid list from this row; `shapes` is the sole errand record. | OPEN |
| **R2-F2** | 問題11(4) + 聴解問題4-7番 | **a topic repeated within the paper** — automatic fail | **A (自動不合格)** | **mechanical** (composer draw) + whole-paper pass | 問題11(4) `言語知識・読解.md` L361: 「電車が長く止まった日のことを、あとから調べた。**勤め先から歩いて帰った**四十人ほどに…」 — the entire 中文 passage. 聴解問題4-7番 `聴解スクリプト.txt` L196: 「電車の事故で、昨日は**会社から歩いて帰った**んだ。」 Same subject, two registers, near-identical wording. `exam-qa-review` §5 "Fail on: any subject twice in this paper (any register)"; automatic-fail list, "a topic repeated within the paper". Collateral: the F1/F4 re-composition moved 問題4-7 from a `shinkanzen` clip to `soumatome:cd1-42`, and no whole-paper pass was re-run. | OPEN |
| **R2-F3** | 聴解問題1 + 聴解問題3 | per-section key monoculture — the key is findable without listening | **C (要修正)** | **mechanical** (composer objective) | Shipped keys: 問題1 = **3,4,3,3,3** and 問題3 = **4,1,1,1,1** — the same option four times of five, in two sections. Over 30 four-option sections in ten official sittings the maximum is **3** (never 4). 8 of 25 generated papers show a section at ≥4; this is the only one with two. Root cause: `tools/compose_choukai.py::key_spread()` pools 問題1+2+3+5 into one 19-key bucket (this paper's pooled spread is 5/5/5/4, penalty ≈0.16 — near-perfect), and `check_answer_positions` skips 聴解 entirely for a composed paper, so nothing measures per-section skew. | OPEN |

Nothing was repaired. This pass wrote no file under `tests/20260909_1/`, `logs/` or `tools/`, did
not edit round 1's report or the dispositions file, and ran no `make sample` / `mp3` /
`model-answer` / `booklet` / `sheet`. `模範解答.html` confirmed absent, so stage 5 has not started.

### 8.1 Candidates I MEASURED AND REFUTED (recorded so they are not re-derived)

1. **No 例 block / untranscribed 例 audio.** 問題1's preamble carries ~159 s of 例 dialogue the
   script does not transcribe and the booklet prints no options for. **Refuted:** all ten
   `tests/imported-*` officials carry the identical disclaimer and the identical untranscribed
   audio. §5.5.
2. **"A character of the key occurs in its own stem" as a general predicate.** Fires on kana in
   **all ten officials** (2–3 hits each: 案の定→やっぱり, さわがしい→うるさい, 概要→大体の内容 …).
   Only the **kanji-restricted** form scores 0/10 official. §4.3 — this matters for whoever
   implements round 1's F2 gate check.
3. **Preamble collision with the previous paper.** 問題1's preamble is `2024-12:問題1-preamble` in
   both this paper and `20260907_1`, because `previous_slot_clips()` returns `clips` only. Not
   filed: §4 check 1 is about item slots, the preamble is announcer boilerplate, and round 1 read
   it the same way. Named in §9 so the next person decides it deliberately rather than by
   omission.
4. **問題4–6 valence collapse (the `20260904_1` 3:1 tone split).** No 問題4–6 解説 kills three
   distractors in one clause — each writes one disqualifier per option, and 問題6-27's three are
   three *different* correct verbs (停止させる / 見合わせる / せき止める), so animacy is not a single
   axis. The gate's `check_goi_option_set_valence` is silent for this test. Not a finding.
5. **聴解 key-length / register / pacing bands** — out of scope for a composed paper by §4;
   running them would measure the yardstick against itself.
6. **問題6 wrong sentences leaving the target's domain** — refuted in the owner (`moji-goi.md`
   Part 6) against official 12/2024; not applied.
7. **問題13 length.** My scope measures 907 JP chars; round 1 measured 827 and the `notes` claim
   1009. All three are above the ≥800 floor, so the disagreement is scope definition, not a
   defect. Recorded because three numbers for one passage invite a fourth.

### 8.2 Other observations, not filed

- The **bigram-overlap strategy at 44.4 %** exactly ties the official maximum (2022-12) and sits
  0.6 points under the 45 % ceiling. Passes; second round running that this is the paper's
  closest-to-the-line number.
- **「〜だけが」 closings at 2 of 13** (問題11(1), 問題11(4)) — the shared cap, so compliant, but all
  ten officials score 0. Round 1 recorded the same; recording it again because a cap-hugging pair
  is what F3's class was.
- **`notes`' 問題12(A) label justification still describes the discarded 住まい draft** (§6.4). The
  label is right on the shipped text; the sentence explaining it is not.
- **問題10–13 in-body `（注N）` = 29** (問題10 2, 問題11 20, 問題13 7), definitions pairing 1-to-1 with
  markers (29/29, no orphans). Above the gate floor of 25, one below `dokkai.md`'s ~30–40 target.
- **Textbook clip wear is AT the ceiling**: `make choukai-wear` measures max 4 uses per clip
  against a ceiling of 4.0 in 問題1, 問題3 and 問題4. It exits zero, but there is no headroom left.
- **62 bank item records carry no `figure_dependent` field** — the textbook half. Safe today
  (none has a digits-only option set) but the flag is written by only one of the two bank builders.
- `（中略）` present (問題11 ×3, 問題13 ×1 = 4, non-zero ✓); zero `<ruby>` and zero `《》` in
  `言語知識・読解.md` ✓; zero doubled punctuation in either source ✓; marked span 問題13
  ①**だれがいつ数えたのか** matches item 68's stem quote character-for-character, pointer-sized,
  no `（注N）` inside the bold, 1-to-1 ✓.

---

## 9. Root-cause table (§6.5)

Recurrence counted by reading the sources, not by judgment. **Two or more papers = systemic by
definition.**

| id | root cause | papers showing the class | owning file | concrete proposed edit |
|---|---|---|---|---|
| **R2-F1** | **PIPELINE-GAP** (a re-composition rewrites `聴解.md`, `聴解スクリプト.txt`, `聴解.mp3`, the chapters and both `詳細解説` panes, but **not** `logs/topics.json` — and no stage owns re-deriving that row afterwards) + **GATE-BLIND** (nothing joins the row's 聴解 keys to `logs/choukai_draws.json`) | **≥2 papers on record**, i.e. systemic: `20260909_1` (measured here, 24 of 29 rows) and `20260907_1` (its own `notes` says so: "20260907_1's own row records its 聴解 entries as HISTORICAL (its listening half was recomposed on 2026-09-08 and its row was never re-derived from the new draw)"). Any paper re-composed after its topic pass is exposed. | `.agents/jlpt-test-generation/SKILL.md` + `tools/check_consistency.py` | (1) `jlpt-test-generation`, beside the one-writer-per-test-folder rule: **"`make mp3` invalidates the `logs/topics.json` 聴解 rows. Any re-run — same seed included — requires the 聴解 `surfaces`/`themes`/`shapes` and the draw-audit paragraph of `notes` to be re-derived from `logs/choukai_draws.json` before QA is re-entered. A composed paper's row is a record of the DRAW, so it can be rebuilt mechanically from the draws file plus the bank."** (2) New gate check `check_topics_choukai_draw_agreement()`: for a paper whose `聴解_チャプター.json` says `composed`, join each `logs/topics.json` 聴解 row to that slot's clip in `logs/choukai_draws.json` and FAIL when the row's `surfaces` text shares no content token with the clip's own banked `explanation.stem` / `script` opening line. **Founding-case run:** on the current bytes it fires on 24 of 29 rows here; run on 20260907_1 it fires too (that paper's own notes predict it); on the ten `imported-*` papers it does not apply (no `choukai_draws` row), and on a correctly-recorded paper it is silent — I verified the five surviving rows (2-1〜2-4, 2-6, 4-9, 5-2) pass the predicate. |
| **R2-F2** | **PIPELINE-GAP** — the same one. `exam-qa-review` §5's cross-surface subject table is the only thing that catches a 読解↔聴解 subject collision, and a re-composition after stage 3 replaces one side of that table with nothing re-reading it. **Not** `RULE-MISSING`: the rule is specific and binding ("any subject twice in this paper, any register") and it was simply never applied to the new draw. | **1 paper for this collision**, but the *class* — a re-composition landing a clip on a 読解 subject — is created by the same gap as R2-F1 and will recur on every re-composed paper. | `.agents/jlpt-test-generation/SKILL.md` §"One topic, one surface" (same edit as above) | Same edit (1). Add explicitly: **"a re-composition re-opens the cross-surface subject table, not only the 聴解 rows of it — re-read all 29 new 聴解 subjects against the thirteen 読解 surfaces before re-entering QA."** The repair for THIS paper is on the 読解 side (per `jlpt-test-generation`'s rule that the 聴解 item is the lifted one): re-author 問題11(4) onto a different subject, or re-draw 問題4-7. I do not recommend a gate check: subject identity is not string-decidable — 「勤め先から歩いて帰った」 vs 「会社から歩いて帰った」 happens to share 6 characters, but a paraphrased collision would not, and a shared-token predicate over 29×13 pairs would drown in false positives. **State it as human judgment.** |
| **R2-F3** | **GATE-WRONG**, in the composer's own objective — `key_spread()` measures the right thing at the wrong granularity, so a per-section monoculture scores as a near-perfect paper. The symptom is silence, which is the shape §6.5 calls the most dangerous. Plus **GATE-BLIND** downstream: `check_answer_positions` skips 聴解 wholesale for a composed paper, so no check reads the shipped 聴解 key balance at all. | **8 of 25** generated papers have a section at ≥4-of-5 (or 4-of-6): `20260810_1`, `20260818_1`, `20260819_1`, `20260821_1`, `20260827_1`, `20260904_1`, `20260904_3`, `20260909_1`. Systemic. All ten officials: max 3. | `tools/compose_choukai.py` (`key_spread`) + `tools/check_consistency.py` | (1) `key_spread()`: score each 大問 separately rather than pooling 問題1/2/3/5 — `for section in SECTIONS: counts over that section's keys; expect = n/ n_opts` — and add a hard term for any section whose modal key exceeds **3**, so the 400-attempt search treats it as near-disqualifying rather than as noise. (2) New gate check `check_choukai_shipped_key_balance()`, which is the line that exists for the 71 and not for the 30: **FAIL** any paper whose 聴解 section keys the same option more than 3 times, **for a composed paper as well as an authored one** — the composer chose the combination even though it did not write the items. **Founding-case run, over all 35 papers on disk:** fires on the 8 generated ids above (20260909_1 twice, in 問題1 and 問題3 — the worst on disk) and on **none** of the ten official sittings, whose maximum is 3. So it catches its own founding case and cannot fail a real sitting. Grandfather the 7 pre-rule ids by name; `20260909_1` should be repaired, not grandfathered, since it has not shipped. |

### 9.1 Skill findings with no paper finding attached

| id | root cause | evidence | proposed edit |
|---|---|---|---|
| **R2-S1** | **The dispositions file states a measurement it did not take.** "Re-composed on the SAME seed; only 問題1-2 moved" is false — 25 of 29 slots moved — and every downstream reader (including my own briefing) inherited it. The mechanism is visible: F4's `avoid_slot` bar sits inside `freshest()`, so it changes rng consumption for every slot at a fixed seed. | §4.1: 16 of 27 of round 1's own deciding quotes absent from the current script; source mix 3/1 → 1/3. | `.agents/choukai-audio/SKILL.md`, beside the seed rule: **"A fixed seed does not fix the draw across composer changes. `avoid_slot`, the figure exclusion and the wear counts all run inside the per-slot choice, so any change to them re-draws the whole half at the same seed. After ANY `make mp3` re-run, diff `logs/choukai_draws.json` against the previous row and report the number of slots that moved — never assert that one slot moved because only one was intended to."** And in `exam-qa-review` §4: **"If the listening half was re-composed since the last review, checks 1–4 must be re-run in full; a previous round's verification is evidence about clips that may no longer be drawn."** |
| **R2-S2** | **`exam-qa-review` §4's composed-paper carve-out does not say whether ANSWER-KEY BALANCE is in scope**, and the enumeration ("場面 mix, 決め手 spread, 質問型 balance, distractor shape, key length, closing turns, voice casting") reads as exhaustive. A reviewer applying it literally checks nothing about the 30 keys' positions, which is how R2-F3's class reached 8 papers. | 8 of 25 papers; two rounds on this paper before it was measured. | `.agents/exam-qa-review/SKILL.md` §4, in the composed-paper block, as a **fifth** replacement check: **"5. The shipped 聴解 key balance IS in scope, even though the items are not authored here — the composer picked the combination. Tally each section's keys: no section may key the same option more than 3 times (official maximum over 30 four-option sections in ten sittings is 3). This is the 聴解 counterpart of the 71-item `answer_positions` check, which `check_answer_positions` skips wholesale for a composed paper."** This is the one file the reviewer may edit directly; I have not edited it, because the caller's instruction was to file rather than fix. The sentence above is final text — whoever takes it needs to derive nothing. |
| **R2-S3** | **Round 1's S1 and S2 were written out verbatim and left unapplied**, and S1 in particular (§6.2's "all 101 positions" wording, which for a composed paper 30 cannot satisfy) is still live in `exam-qa-review`. I hit it this round and had to re-derive the same resolution. | `exam-qa-review` §6.2 unchanged; §4 check 1 still calls itself a verification of a guarantee the composer now genuinely makes (so S2's text needs updating again, not just applying). | Apply round 1's S1 as written. **Update S2 rather than applying it as written**: the composer now HAS a previous-paper exclusion, so §4 check 1 should read **"the composer bars the previous paper's clip per slot and prints a note if that would starve a slot; verify the bar held (it covers item slots only, not section preambles) and report any starvation note."** |

**Effect on the loop.** R2-F1, R2-F2 and R2-F3 are open. R2-F1 and R2-F3 carry
`PIPELINE-GAP` / `GATE-WRONG` / `GATE-BLIND` root causes and therefore **block the next
generation run** until applied or explicitly rejected with a reason (§6.5). R2-F3 most urgently
of the three as a *rule* change, because the composer will reproduce it on the next draw; R2-F1
most urgently as a *data* repair, because `used_subjects_by_theme()` reads that row to build the
next paper's avoid list.

---

## 9.2 Audit of the two dispositions I was asked to judge

### (a) S3 — "the ≤5 listening cap governs the DRAW, so the 23-of-25 shipped figure was measuring something the cap never governed." **I AGREE with the narrowing. No real defect was talked away — but its supporting numbers are not measurements of shipped content, and one of them is void.**

**What I verified independently.**

- The draw-level cap **holds on this paper**: `test_spec.json`'s 21 `listening_scenarios` tally
  教育 4 / 睡眠・健康 4 / 食 3 / 消費・経済 2 / 働き方 2 / six themes at 1 — **max 4**, as the
  disposition claims.
- It holds **everywhere**: I tallied the drawn `listening_scenarios` themes of all 25 generated
  specs and **no paper exceeds 5** at draw level (three early papers show 7–8 *untagged* entries,
  which is a missing-`theme` artifact, not a theme count). So the cap is real, enforced by the
  sampler and `check_spec_blend`, and unbroken on disk.
- A composed listening half authors **no surface** from any drawn scenario (§7.2: 0 of 32 drawn
  strings appear anywhere in the shipped 聴解), so there is nothing for the cap to bind on the
  shipped side. Correcting the rule's wording rather than the check is the right move — a correct
  check should not be edited to match a mis-stated rule, exactly as the disposition says.

**Where the disposition's evidence does not survive contact with this paper.** Its two empirical
claims about SHIPPED themes both come from `logs/topics.json`, which for this paper is R2-F1:

| disposition's claim | measured against the shipped paper |
|---|---|
| 働き方 is the offender here (round 1 measured 6) | **≈3.** Re-tagging the 29 shipped clips myself: 働き方 sits on 聴解問題4-3番 (佐藤さんは午後出勤), 4-4番 (課長が昼食から戻らない) and 4-8番 (プレゼンをやらざるを得ない). The recorded 6 counted clips the paper does not contain. |
| "聴解問題4's eleven items are workplace by format" | **3 of 11.** The shipped eleven are a plate's colour, a disappointing film, a colleague's shift, a manager at lunch, a bus and a missed flight, 森君's punctuality, walking home after a train accident, a presentation, a citizens' marathon, an occupied seat, and a children's riddle book. Only three are workplace exchanges. |
| "23 of 25 papers exceed the cap" (shipped) | Not reproducible as a statement about shipped content. It is computed over `logs/topics.json` rows, and **at least two of the 25 rows do not describe their papers** — this one (24 of 29 聴解 rows wrong) and `20260907_1`, whose own `notes` says its row "was never re-derived from the new draw". |

**Verdict.** Keep the rule change; it is correct on the merits and I would not reopen it. But the
"23 of 25 / 24 of 25 / 働き方 by format" figures should be **re-derived from `logs/choukai_draws.json`
plus the bank after R2-F1 is repaired**, and until then not quoted as evidence about shipped
papers. And the one concrete thing the disposition left standing on the strength of those figures —
the 聴解問題3-4番 slot-theme WARN, accepted as "composed, unrepairable, the tag is not negotiable" —
is a statement about a 方言 talk this paper does not contain (§10.3). That is not the cap rule being
wrong; it is the record being wrong, which is R2-F1.

### (b) The 32 unspent draws per composed paper — **DEFERRAL IS DEFENSIBLE for shipping this paper, and I agree it must land before the next `make sample`. I disagree that the harm is confined to bookkeeping.**

**What I verified independently.**

- **21 `listening_scenarios` + 11 `quick_response` = 32** entries drawn, and **zero** of their
  drawn strings occur anywhere in `聴解.md` or `聴解スクリプト.txt`. All 32 shipped nothing.
- Corpus-wide: **800** such entries across the 25 generated specs — matching the disposition's
  525 + 275 exactly.
- The "safe to defer" claim checks out on the part that matters most: the pools that decide what
  the paper **TESTS** are untouched. All 11 spec item categories are byte-identical between
  `test_spec.json` and `logs/ledger.json`; the 22 recorded draws resolve to `pools.json`; the 71
  authored items match their targets exactly (§7.1); and all 71 answer positions match (§5.1).
  Nothing an examinee sees is wrong because of this row.
- The "blast radius" claim also checks out: stopping the draw changes `test_spec.json`'s shape,
  which `check_spec_blend`, `check_draw_provenance`, `check_surface_subjects`, the errand-coverage
  skips and the theme-cap line all read. Doing that at the tail of a generation run, after the
  paper is built and reviewed, is exactly how a green gate stops meaning anything. Deferring is
  the more conservative choice, and it is the right one.

**Where I disagree.** "The harm is confined to bookkeeping for two categories that no longer feed
any authored surface" understates it in two specific ways:

1. **It burns two pools' rotation cooldowns on phantom content.** The gate's errand-rotation check
   compares drawn errand `key`s across papers inside a cooldown window and **FAILs** on a hit — it
   currently FAILs `20260904_3` on a `reading_topics` errand, so the mechanism is live, not
   theoretical. Thirty-two phantom draws per paper mean a future paper can be failed for
   "repeating" a listening errand that has never been spoken on any paper, and the report writer
   will have no shipped text to check the claim against. That is the same "green stops meaning
   anything" failure the disposition invokes to justify deferral, pointing the other way.
2. **The 800 entries already on disk need an explicit decision when the fix lands** — grandfather
   the consumed cooldowns, or recompute them as never-drawn. Silently changing the draw shape
   without deciding this re-classifies 25 papers' rotation history as a side effect.

**Verdict.** Defensible to defer past this paper; not defensible to land the fix without those two
points written into it. The disposition already blocks the next `make sample` on this row, which is
the correct gate — I would add the sentence: *"the repair must state whether the 800 already-drawn
`listening_scenarios`/`quick_response` entries keep or lose their cooldown, because the
errand-rotation check FAILs on them today."*

---

## 10. Coverage statement

| step | ran on | notes |
|---|---|---|
| 0. Blind solve | all 101, from `qa/20260909_1/keyless.md` only | **101/101**; verified keyless before reading |
| 0b. Two blind strategy passes | items 52–69 + all ten officials, my own implementation | 44.4 % / 11.1 %, median margin −0.027 |
| 1. Key-by-key proof | all 101 | walkthrough §3, every row carries its deciding quote |
| 2. Distractor elimination | all 101 | 問題6-27/6-29, 聴解問題4 全11 written up in §3 and §8.1(4) |
| 2b. Distractor plausibility | 問題1–6, 聴解問題1–3 | no valence 3:1 collapse; 問1 two-branch rule verified; every 聴解問題1–3 distractor traced to a script line |
| 2.5. Level band | 問題1–9 keys, 問題5 hard words, 即時応答 | §10.1 |
| 3. Mechanical reads | §10.2 | every owner number quoted from its owner |
| 4. 聴解 structure | composed-paper checks 1–4, **all re-run on the new composition**, plus the chapter/number-call arithmetic | §5; authoring family out of scope |
| 5. Whole-paper & cross-test topic table | §6, re-tagged from shipped content | R2-F1, R2-F2 |
| 6. Provenance & spec audit | §7, re-scan on 問題12/問題13/問題14 | max shared run 16 chars |
| 6.5. Root cause | §9 | recurrence measured, founding cases run over 35 papers |

### 10.1 Vocabulary level band (entirely the reviewer's — no gate has ever checked a 問題1–6 key)

The only 問題1–6 change since round 1 is 問題3-13's **stem**; the drawn target (`新〜(新体制)`) and all
twenty-five keys are unchanged, so round 1's band verdicts stand and I re-affirm them on my own
read: 問題1 驚く/争う are N3-ish as words but the tested point is the reading discrimination among
four real same-field verbs; 冷静/自動券売機/体力 are N2 音読み compounds on clean 2×2 matrices; 問題2
一通り and 抑える do the real work; 問題3 浅学 is the hardest and a genuine N2 humble-register item;
問題4 要領を得ない and 足が出る are idiom-level N2; 問題5 重宝する and いかに are the two N2
discriminations, and 落ち込む's option set keeps two same-valence competitors so it is not TOO_EASY
as a set; 問題6 損なう and まして are the hardest. No option set is four N4–N5 basics. 問題7–9 keys:
`level_band_grammar.txt` green, and read by hand 〜に越したことはない and 〜ことだし are the top of the
N2 band with no N1 class (〜んがため, 〜をものともせず) and no N3 (〜ながら as bare simultaneity).

**No tier-C re-draw (`--reroll` / `--reroll-one`) was performed in this paper** — F2 was repaired
by a stem rewrite around the same drawn target — so there is no "key X drawn, band checked against
<book, page>" line for this pass to read, and none is owed.

### 10.2 Mechanical reads — every number measured here, owner's bar quoted from the owner

**文字・語彙 stems** (`moji-goi.md` Part 0 §"The stem"), re-measured because 問題3-13's stem changed:

| measure | owner's bar | this paper | verdict |
|---|---|---|---|
| median 問題1/2/5 stem, JP chars | official 15–21.5; author to **17** | **17** (range 15–21) | on target |
| 問題1/2/5 stems with no 「、」 (of 15) | official 47–93 %; author to **≥9** | **13 / 15 = 87 %** | PASS |
| 問題1–5 stems in です・ます (of 25) | official 2–11 (med 6); author to **7** | **7 / 25** | exactly on target |
| first-person stems | official 0–4; author to **≥1** | **3** | PASS |
| median 問題4 stem / longest | author to **30 / ≤44** | **29 / 32** | PASS |

**問題7 stem DISTRIBUTION** — all three binding numbers (`bunpou.md` §問題7). Stems (JP chars):
`29, 68, 35, 30, 37, 72, 33, 45, 61, 46, 26, 62`.

| bar | required | measured | verdict |
|---|---|---|---|
| 12-stem mean | inside 36–52 | **45.3** | PASS |
| stems under 34 JP chars | ≥ 2 | **4** (29, 30, 33, 26) | PASS |
| max − min | ≥ 25 | **46** | PASS |
| dialogue/setting-label stems | official always has a few | **5** | PASS |

**読解 option length & key predictability** (`dokkai.md` §"Option length balance", read from the
owner; printed length, 問題10–13 only, 問題14 exempt):

- per-item max/min ratio: **max 1.39 (item 67), median 1.16** — WARN above 1.65, FAIL above 2.50. PASS.
- key rank spread `{1:6, 2:3, 3:3, 4:6}`, dominant **33 %** — FAIL > 60 %, WARN > 45 %. PASS.
- (tied-)longest key **5/18 = 28 %** (ceiling 35 %, official 30 %). PASS.
- **UNIQUELY** longest key, by hand as the skill demands: **5/18 = 28 %** (ceiling 30 %, official
  20 %, target band 20–30 %). PASS, at the top of the band. Over the gate's 20-item scope: 25 %.

**読解 apparatus:** in-body `（注N）` 問題10–13 = **29** markers (2 / 20 / 0 / 7), 29 definitions,
1-to-1, no orphans; `（中略）` = 4, non-zero; 問題13 passage **907** JP chars (floor ≥800); zero
`<ruby>` / `《》`; marked span 1-to-1 and pointer-sized; 問題9 cloze body ~700 JP chars with four
**distinct** category tags and longest option 12 chars (official max 14).

**One grammar point, one KEY — the exposure grep, re-run because 読解 prose was edited by F3.**
Extracted the 問題10–14 passage prose **plus every `（注N）` definition line** (6 510 chars, the
`check_key_grammar_exposure` scope), then grepped all 20 keyed 問題7/問題9 strings and the five
問題8 frames' components:

- **all 20 keyed 問題7/問題9 strings occur ZERO times**;
- 問題8's five frames score zero on every component (`ように` 0, `でなければ` 0, `ながら` 0,
  `ねばならない` 0, `なお` 0 in this scope);
- the only non-zero token is **「つもり」 ×1** — 問題13's 「短くすること自体に反対するつもりはない」 —
  at the ≤1 cap **and** in a different syntactic frame from 問題9-50's concessive 「〜つもりでも」
  (negated 〜つもりはない vs concessive 〜つもりでも). Compliant on both halves.
- **No form is keyed twice across 問題7/8/9.**
- F3's new closing introduces 〜てほしい (3× in the prose), which is keyed nowhere — no leak.

**問題8 — uniqueness read by hand** (`make verify-scramble 20260909_1` returns item 47
**UNDECIDED**: 18 of 24 orderings survive its 4-junction filter, rival ★ values [1,2,3]). I
spliced all five items and tested every card in every slot **including the FINAL card as a
candidate host** — the zero-anaphora trap. All five ★ values match the key and my blind solve got
all five independently; `FREE UNITS: 1` is correct on item 47 (the two chains are
[持っていかねばならない＋というのが] and [山を歩く人たちの＋間の決まりだ]; no bare が/は card sits in
front of two candidate predicates). Item 46's rival 4→1→2→3 yields the **same** ★=2, so it is not
a second answer. Detail in the §3 rows for 43–47.

### 10.3 `make check` — every line naming this test, with my own disposition

Current state: **1 FAIL, 3 WARN** name `20260909_1` (grep-verified: exactly 4 lines in the whole
output). The two-back `消費・経済` note the briefing listed as known is **no longer printed** —
consistent with §6.2's arithmetic.

| line | my disposition |
|---|---|
| **FAIL** `詳細解説.json explains every keyed item (30 entries for 101 keys)` | **Structural, not a paper defect. Accepted.** `詳細解説.json` carries exactly the 30 聴解 entries `make mp3` writes; the 71 言語知識・読解 entries belong to stage 5, prohibited before this verdict (AGENTS.md §5). `模範解答.html` is absent, so `check_kaisetsu_no_scaffold_placeholders` correctly skips. I additionally verified the 30 present entries are **not stale** against the new composition (§5, check 3) and are item-specific rather than scaffold prose. |
| **WARN** `問題8 form-family coverage 1/5 = 20% family-tagged` | **A `pools.json` map-coverage statement, not a fact about this draw. Accepted.** I read the five drawn 問題8 frames by hand — 目的表現(〜ように…する) / 〜でなければ / 補足追加(〜なお…) / 同時進行(〜ながら…する) / 義務当然(〜ねばならない) — and they share no form core with each other or with any of the twelve 問題7 forms; the gate's own cross-pool line (`no grammar form crosses 問題7 <-> 問題8 inside its cooldown`) is `ok`. Every generated paper carries this WARN at 20–40 %. Repair is in `pools.json`, not in this paper. |
| **WARN** `聴解問題5 repeats a headline theme of 20260907_1 — ['旅行・観光']` | **Correct and unrepairable. Accepted, and stated as rule 4 requires.** Re-derived from the shipped clip: 旅行・観光 sits on exactly one surface in the whole 44-surface tally, the composed 聴解問題5-2番 (`2022-07:問題5-2`, the group-tour free-day item). No 読解 surface carries it, so there is nothing to re-angle, and the only other lever is seed-shopping, which the repo forbids. |
| **WARN** `no 聴解 slot repeats its own theme in the previous 2 papers — 聴解問題3-4番=文化・伝統 (also 20260904_3, also 20260907_1)` | **NOT accepted as stated — this WARN is about a clip the paper does not contain, and that is R2-F1.** The tag comes from `logs/topics.json`, which still records the pre-recomposition `shinkanzen:cd2-59` 方言 talk. The shipped 問題3-4番 is `2021-07:問題3-4`, a children's-programme talk on how plant seeds travel — **科学・技術**, colliding with neither previous paper's 問題3-4 tag. Once the row is re-derived this line should disappear. **No `GATE-WRONG` filed against the check**: the check reads its input correctly; the input is wrong. |

No line was determined a false positive of the check itself, so no `GATE-WRONG` finding arises
from the gate's own logic. (R2-F3's `GATE-WRONG` is against `compose_choukai.py::key_spread`, not
against `check_consistency.py`.) `make check` overall still FAILs on the one 詳細解説 line; there
are no other FAILs naming this test anywhere in its output. The 18 grandfathered
`shipped_surface` lines name other ids, not this one.

---

## 11. Skips — stated explicitly (AGENTS.md §0.7)

1. **I did not listen to `聴解.mp3`.** §4 check 3 asks for two items spot-checked **by ear**; there
   is no audio playback in this environment. **Substituted, with wider coverage:**
   `tools/choukai_segment.py` round-trips the MP3 against the composed script and recovers
   5/6/5/11/2 exactly; I verified **all 30** printed/spoken option sets and **all 29** clip script
   bodies against `logs/choukai_bank.json`; and I re-derived **every chapter offset**
   arithmetically from the bank's audio spans, which independently confirms the eight harvested
   「N番。」 prepends and the section seams. What none of this can see is audio quality inside a
   correctly-placed clip (level jumps, clipped heads/tails); LUFS −15.48 over 46.5 min is the only
   evidence I have there.
2. **`refs/` binaries were not opened.** The archive is absent on this machine, so no PDF page and
   no source MP3 was read. Every textbook/archive claim above rests on the **tracked `*.md`
   extracts** and on `tests/imported-*` (exact for `booklet.md`/`key.md`). Per AGENTS.md §3 I
   substituted **no** number from memory: every count in this report is a measurement I ran on
   files present on disk. §10.1's band judgments rest on extract-level evidence plus the
   31-sitting `booklet.md` corpus, not on a page read — a stricter verdict on 浅学 or 重宝する needs
   `Shinkanzen.zip` / `Soumatome.zip` restored (~1 GB), which I did not download unasked.
3. **Stage 5 (`詳細解説` 言語知識・読解 authoring, `make model-answer`) not run and not reviewed** —
   prohibited before this verdict. The gate's one FAIL is that absence.
4. **No repair, no regeneration.** Nothing under `tests/20260909_1/`, `logs/` or `tools/` was
   edited; round 1's report and the dispositions file were read and left untouched; no
   `make sample` / `mp3` / `model-answer` / `booklet` / `sheet` was run.
   `.agents/exam-qa-review/SKILL.md` — the one file this skill permits the reviewer to edit —
   was **also left unedited**, because the caller's instruction was to file rather than fix.
   R2-S2 and R2-S3 are the edits I would otherwise have applied to it directly, and their text is
   written out verbatim in §9.1 so whoever takes them needs to derive nothing.
5. **セクション構成表 checks not run** — a composed paper has none and must not have one (§4).
6. **`make check` was run read-only and in full**; I did not run `make findings`,
   `make repair-plan`, `make goi-profile` / `dokkai-profile` / `choukai-profile` in `BASELINE`
   mode, because every owner number this pass needed was quoted from its owner file and measured
   directly. `make choukai-wear` was run (read-only) and is reported in §8.2.

---

QA: FAIL (3 findings, 1 automatic)
