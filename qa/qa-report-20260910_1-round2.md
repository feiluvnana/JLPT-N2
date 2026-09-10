# QA report — `20260910_1` (Stage 4, adversarial pass, **round 2 — the capped round**)

| source | sha1[:12] | mtime |
|---|---|---|
| `tests/20260910_1/言語知識・読解.md` | **`fa043f11663b`** | 2026-09-10 21:56:38 |
| `tests/20260910_1/聴解.md` | `3498b31299b7` | 2026-09-10 21:16:26 |
| `tests/20260910_1/聴解スクリプト.txt` | `d79c542e341c` | 2026-09-10 21:16:26 |
| `tests/20260910_1/聴解_チャプター.json` | `2be9a93b7ccb` | 2026-09-10 21:17:05 |
| `tests/20260910_1/test_spec.json` | `997084f5e1a0` | 2026-09-10 19:00:49 |
| blind-solve render `qa/20260910_1/keyless.md` | `4ab819cda126` | rebuilt at the start of this pass |

Reviewed 2026-09-10, round 2. Reviewer authored no part of this paper and did not
review round 1. `言語知識・読解.md` was `fa043f11663b` when the render was built and
`fa043f11663b` when this report was written — the sources did not move under the pass.

Round 1's render (20:38) predated the 21:56 F2 repair, so it was stale; I rebuilt it
with `make keyless 20260910_1` before solving and solved from the rebuild.

---

## 1. Verdict

**QA: FAIL (3 findings, 2 automatic)**

| id | item | blocks shipping? |
|---|---|---|
| **F1** | 聴解問題4-8番 — the banked transcript of option 2 is not Japanese and is not what the audio says | **YES.** Automatic (broken Japanese anywhere). One string upstream; the key is unaffected. |
| **F2** | 問題4-15 — the key 初霜 is off-band (TOO_HARD), and it is a `pools.json` defect | **YES.** Automatic (an off-level KEY). One-item re-draw. |
| **F3** | 問題8-45 / 問題8-47 — a dialogue stem collapsed onto one line, which `bunpou.md` forbids | **Not on its own.** The items are solvable and correctly keyed. But **fix the gate before the paper** — the gate currently FAILs the mandated layout. |

Round 1's three findings (F2 読解 rhetorical monoculture, F3 聴解問題4-6番, F4 聴解問題3-3番)
are all **verified repaired** (§5). Round 1's skill finding **S1 is verified applied**, and
I reproduced its band independently from `answer_keys.json`. Two of round 1's root-cause
edits (F2-a, F2-b) were **never applied** — they do not block this paper but they block the
next generation run (§7).

Everything else on this paper is clean, and unusually so: 100/101 blind-solve agreement,
zero exposure leaks, zero provenance runs above 15 chars in any passage, every 読解
predictability metric inside the official band, all 71 answer positions matching, ledger ==
spec field for field, and every one of the 30 聴解 keys traced to its source recording.

---

## 2. Blind-solve diff

**Solved from `qa/20260910_1/keyless.md` (`4ab819cda126`) and nothing else**, all 101
items, before opening any keyed file. Evaluated with `python3 tools/qa_eval.py
tests/20260910_1 --answers "[…]"`:

```
Total Scored Items : 101
Agreement with Key : 100 / 101 (99.0%)
Discrepancies      : 1
  - Item 95: Blind-Solve=2 vs Key=3
```

**Item 95 = 聴解問題4-8番.** Resolved as **reviewer error, but it exposed F1.**
I picked 2 by reading 「だから持って言ったじゃない」 as a garbled 「だから持ってけって
言ったじゃない」 ("I told you to take one") — a natural 即時応答 reply. The source book's
printed key is **正答3** and the deciding logic is the official one: a single-line 即時応答
establishes no prior advice, so a reply presupposing advice is unwarranted; 「何だ、持って
ないの？」 is the mild-surprise confirmation of 「〜ばよかった」. My answer was wrong.
**But the reason I read it wrongly is that the string as shipped is not Japanese** — see F1.
No other item moved.

### Blind STRATEGY passes over 読解 (問題10–13, items 52–69, n=18)

| strategy | this paper | official | bar |
|---|---|---|---|
| 1. pick the option sharing the most character bigrams with its own passage | **33.3 %** (6/18) | 32.8 % | FAIL above 45 % |
| 2. pick the second-longest option | **5.6 %** (1/18) | 24.6 % | FAIL above 45 % |
| paper median overlap margin (key − best distractor) | **−0.0431** | — | must be ≤ 0 |

Both passes are at or below the official rate, and the median margin is negative — an
examinee who reads no Japanese does no better than chance here. No repair needed.

---

## 3. Per-question walkthrough — all 101 items

Paper order: 1–71, then 聴解 問題1 1番 … 問題5 2番-質問2. `どこが問題か` carries the deciding
quote for an `OK` row and the exact wrong string otherwise. 聴解 rows are annotated with the
drawn clip id in an HTML comment.

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 3 | OK | 街路や人の往来を表す「〜どおり」型の和語複合名詞 ×4 (おもてどおり/ひとどおり/おおどおり/うらどおり)。訓読み目標(送り仮名「り」が印字されている)なので、官製の型どおり四つとも実在語でそろえた(訓読み集合に非語を混ぜてはならない: moji-goi.m… | — |
| 問題1-2 | 2 | OK | 音読み複合語(音符の同音字・長短の混同) ×4 (ぜんりょう/ねんりょう/ねんりょ/ぜんりょ)。2×2読み行列 A=ねん(燃の常用音「ネン」、正) B=ぜん(燃の音符「然」の常用音「ゼン」。自然(しぜん)) / C=りょう(料の常用音「リョウ」、正) D=りょ… | — |
| 問題1-3 | 4 | OK | 人や物を遠ざけたり切り離したりすることを表す和語他動詞 ×4 (みすてる/おいたてる/きりすてる/へだてる)。訓読み目標(送り仮名「てる」が印字されている)なので四つとも実在語でそろえた(moji-goi.md §「All four readings must… | — |
| 問題1-4 | 4 | OK | 音読み複合語(同字別音・清濁の混同) ×4 (じゅうし/ちゅうじ/じゅうじ/ちゅうし)。2×2読み行列 A=ちゅう(中の常用音「チュウ」、正) B=じゅう(中のもう一つの常用音「ジュウ」。一日中(いちにちじゅう)) / C=し(止の常用音「シ」、正) D=じ(… | — |
| 問題1-5 | 2 | OK | 音読み複合語(清濁の二軸) ×4 (りょうしかん/りょうじかん/りょうじがん/りょうしがん)。2×2読み行列 A=りょうじ(領「リョウ」＋事「ジ」、正) B=りょうし(事を清音で読んだ派生。同音の実在語 漁師・猟師 あり) / C=かん(館の常用音「カン」、正… | — |
| 問題2-6 | 4 | OK | 「めずらしい」と書く単一漢字＋送り仮名「しい」の表記 ×4 (診しい/珠しい/現しい/珍しい)。単一漢字＋送り仮名の和語項目なので、四つとも同じ送り仮名「しい」を共有し、珍の視覚系列から取った(moji-goi.md §問題2「Single-kanji ste… | — |
| 問題2-7 | 3 | OK | 「ひとやすみ」と読み分解できる同訓表記 ×4 (人休み/一安み/一休み/人安み)。送り仮名「み」つきの和語複合名詞で、四つとも同じ送り仮名を共有する。2×2成分行列 A=一(ひと、常用訓「ひと、ひと-つ」) B=人(ひと、常用訓) / C=休(やす、常用訓「や… | — |
| 問題2-8 | 3 | OK | 「きょうよう」と読み分解できる同音表記 ×4 (協養/教様/教養/協様)。2×2成分行列 A=教(キョウ、常用音) B=協(キョウ、常用音の同音字) / C=養(ヨウ、常用音) D=様(ヨウ、常用音。養と同じ「羊」を含む視覚的類似字) → {教養,教様,協養,… | — |
| 問題2-9 | 2 | OK | 「かいてい」と読み分解できる同音表記 ×4 (開定/改定/改停/開停)。2×2成分行列 A=改(カイ、常用音) B=開(カイ、常用音の同音字) / C=定(テイ、常用音) D=停(テイ、常用音の同音字) → {改定,改停,開定,開停}。`matrix_help… | — |
| 問題2-10 | 1 | OK | 「ちかよる」と書く和語複合動詞の表記 ×4 (近寄る/近奇る/近夜る/近因る)。送り仮名「る」つきで、四つとも同じ送り仮名を共有する。第一成分は「ちか」と読める常用漢字が近のほかにないため2×2の成分行列は組めず、官製の単一系列型({険しい,験しい,検しい,剣… | — |
| 問題3-11 | 3 | OK | 時間の前後を表す接頭辞 ×4 (現/旧/前/翌)。前年度(ぜんねんど)＝いまの年度の一つ前の年度。「より来場者がずいぶん増えた」が、比べる相手がすでに終わって数の出そろった年度であることを表している。1 ✗ 現＝現段階・現政権のように、いま動いているものを指す… | — |
| 問題3-12 | 4 | OK | 組織や運用のしくみを表す接尾辞 ×4 (式/法/型/制)。会員制(かいいんせい)＝登録した会員だけが使えるというしくみ。「だれでも使えるわけではない」が、使える人を資格で限る決まりのことだと表している。1 ✗ 式＝日本式・自動式のように、やり方や様式を表す接尾… | — |
| 問題3-13 | 2 | OK | 動詞の連用形に付く接尾辞 ×4 (かけ/放題/ごたえ/がち)。飲み放題(のみほうだい)＝決められた時間の中で、いくらでも自由に飲めること。「二千円で二時間」が、料金と時間だけが決まっていて量に限りがない売り方であることを表している。1 ✗ かけ＝読みかけ・食べ… | — |
| 問題4-14 | 2 | OK | 「〜法」の形でやり方を表す漢語名詞 ×4 (治療法/予防法/使用法/解決法)。予防法＝病気にかからないようにするためのやり方。固定した軸は「かぜの」と「外から帰ったら必ず手を洗う」で、まだ病気になっていない段階の日々の行いであることを本文が印字している。1 ✗… | — |
| 問題4-15 | 4 | **自動不合格 (F2)** | 鍵「初霜」の 霜 は Shin Kanzen 漢字の N2 1,046字表（PDF p.191＝印刷 p.58 の ソウ/ゾウ 行 掃/窓/装/想/層/総…憎/蔵/贈/臓）に無く、Soumatome 語彙・Hajimete 2500 にも無く、31回の公式に実出現ゼロ（3件は 結→霜 の OCR ノイズ）。誤答 初雪/朝露/夕立 は全て帯内で、鍵だけが帯外。 | `pools.json` の `context_words` から 初霜 を削除し、`--reroll-one context_words:<index>` で引き直して 問題4-15 を書き直す。spec・ledger・topics.json に `"origin": "reauthored"` と note を入れる。 |
| 問題4-16 | 2 | OK | 程度や量を小さくすることを表す漢語サ変名詞 ×4 (削減/軽減/縮小/短縮)。軽減する＝苦しみや負担を軽くする。固定した軸は「薬が効いてきて」と「足の痛みが」で、小さくなったのが数量でも広がりでもなく、体に感じる苦しさであることを本文が印字している。1 ✗ 削… | — |
| 問題4-17 | 2 | OK | 住まいの種類を表す漢語名詞 ×4 (寮/別荘/下宿/社宅)。別荘(べっそう)＝ふだんの家とは別に、休みを過ごすために持つ家。固定した軸は「毎年夏になると」「湖のそばの」「一か月ほど過ごす」で、日常の住まいではなく季節ごとの滞在に使う家であることを本文が印字して… | — |
| 問題4-18 | 3 | OK | 「〜に」を取って人と対象との関わり方を表すい形容詞 ×4 (きびしい/したしい/くわしい/するどい)。くわしい＝ある分野のことを、細かいところまでよく知っている。固定した軸は「兄はパソコンに」と「故障するといつも直してくれる」で、兄が持っているのが積み重ねた知… | — |
| 問題4-19 | 4 | OK | 移動を表す和語動詞のて形 ×4 (登って/移って/進んで/乗って)。相談に乗る＝人の悩みを聞いて、いっしょに考えたり助言したりする。固定した軸は「困ったことがあれば」と「いつでも」で、話し手が相手の困りごとを引き受ける側であることを本文が印字している。1 ✗ … | — |
| 問題4-20 | 1 | OK | 二つのものの位置関係を表す動詞 ×4 (沿う/至る/交わる/面する)。沿う＝長く続くものから離れずに、並んで続く。固定した軸は「この遊歩道は川に」と「ゆるやかに続いている」で、道と川が長い区間にわたって並んでいることを本文が印字している。2 ✗ 至る＝進んだ先… | — |
| 問題5-21 | 4 | OK | 物事への向き合い方を表す動詞のて形 ×4 (あきて/なれて/とまどって/熱中して)。夢中になる＝ほかのことを忘れるほど、そのことに心を奪われる。置換確認：「弟は新しいゲームに熱中している。」＝成立、置換可能。1 ✗ あきて＝同じことが続いていやになることで、心… | — |
| 問題5-22 | 3 | OK | 出来事に対する話し手の評価を表す副詞 ×4 (幸いに/確かに/運悪く/やはり)。あいにく＝都合の悪いことに。置換確認：「運悪くその日は先約があります。」＝成立、置換可能。1 ✗ 幸いに＝望ましい結果になったことを表す副詞で、断りの理由を導く位置に置くと文の向き… | — |
| 問題5-23 | 1 | OK | 程度や差の大きさを表す副詞 ×4 (ずっと/わずかに/わりに/あまり)。はるかに＝比べたものとの差がとても大きいようす。置換確認：「今年の夏は去年よりずっと暑い。」＝成立、置換可能。2 ✗ わずかに＝差がごく小さいことを表す副詞で、大きな差を表すはるかにと正反… | — |
| 問題5-24 | 2 | OK | 数量に添えて見当を表す副詞 ×4 (ちょうど/だいたい/せいぜい/少なくとも)。およそ＝細かい数まではわからないが、その辺りだという見当。置換確認：「会場には、だいたい三百人が集まった。」＝成立、置換可能。1 ✗ ちょうど＝数がぴったり合うことを表す副詞で、大… | — |
| 問題5-25 | 3 | OK | 物の見え方を表す副詞 ×4 (はっきり/ちらりと/かすかに/きらきらと)。ぼんやり＝輪郭がはっきりせず、うすく見えるようす。置換確認：「遠くの山が霧の中にかすかに見えた。」＝成立、置換可能。1 ✗ はっきり＝輪郭が明らかであることを表す副詞で、正反対になる。2… | — |
| 問題6-26 | 2 | OK | 動詞「検討する」の用法 ×4(全選択肢が同一のサ変動詞の活用形)。正：新しい支店を出すかどうかという決めていない案を、会議でよく調べて考え直すという「案の良し悪しを、いろいろな面から調べて考える」用法。1 ✗ 体を調べて悪いところを見つけることは「検査する」で… | — |
| 問題6-27 | 4 | OK | 名詞「分担」の用法 ×4(全選択肢が同一のサ変名詞の活用形)。正：文化祭の準備という一つの仕事を、係を決めてクラスの全員で受け持ち合うという「一つの仕事を分けて、それぞれが受け持つ」用法。1 ✗ 一つの物を切って小さくすることは「分ける」で、分担が分けるのは受… | — |
| 問題6-28 | 2 | OK | 名詞「対策」の用法 ×4(全選択肢が同一の名詞形)。正：流行しているかぜという困った事態に対して、うがいや手洗いという手を打っている「起きて困ることに対して、前もってとる手だて」用法。1 ✗ 旅行のように望んで行うことの段取りを決めるのは「計画」で、対策が向き… | — |
| 問題6-29 | 4 | OK | 動詞「築く」の用法 ×4(全選択肢が同一の動詞の活用形)。正：店の主人が長い年月をかけて客との信頼関係を作り上げたという「時間をかけて、しっかりしたものを作り上げる」用法。1 ✗ 物を上へ重ねていくことは「積む」で、築くは土台から作り上げる大きなものや、年月を… | — |
| 問題6-30 | 1 | OK | 動詞「貢献する」の用法 ×4(全選択肢が同一のサ変動詞の活用形)。正：この研究が、病気の早期発見という広く役に立つ目標の前進に力を添えたという「あることのために力を尽くして、よい結果に役立つ」用法。2 ✗ 自分の家の庭仕事に一日打ちこむことは「精を出す」で、貢… | — |
| 問題7-31 | 1 | OK | 「〜だけあって」は、前件にふさわしい立派な結果が後件に現れることを表す。長く生地をねかせるという手間が、皮がかたくならないという良い結果を生んでいる。2「ものの」は逆接で、後件は前件から予想されることに反する内容でなければならないが、ここでは手間が良い結果の理… | — |
| 問題7-32 | 2 | OK | 「〜たところ」は、してみた結果こういうことが分かった、という発見を導く。窓口で尋ねるという行為の結果、住民票が不要だと判明したという流れ。1「とたん」は、その直後に思いがけない出来事が起こることを表す形で、後件は瞬間的な変化でなければならず、答えの内容は導けな… | — |
| 問題7-33 | 3 | OK | 「〜気味」は、はっきりとではないが少しその状態にある、という程度を表す接尾語。「風邪気味」は昨日から少しかぜの状態にあることを言う定型の言い方。1「続き」は「雨続き」のように同じことが何度も重なることを表す語で、昨日からの一回の状態には使えない。2「がち」は「… | — |
| 問題7-34 | 2 | OK | 「〜っこない」は、そんなことは絶対にありえないと親しい相手に強く打ち消す言い方。分厚い資料を一日で読み切るのは不可能だという主張に合う。1「ようがない」は「読みようがない」のように動詞のます形に付く形で、「できる」という辞書形には接続できない。3「どころではな… | — |
| 問題7-35 | 1 | OK | 「〜上に」は、同じ方向の事がらを重ねて付け加える。日当たりが悪いという不満に、壁がうすいという別の不満を重ねている。2「わりに」は前件から予想される程度と食い違う後件を導く形で、不満に不満を重ねる文には使えない。3「かわりに」は一方の不足を他方で埋め合わせる交… | — |
| 問題7-36 | 3 | OK | 「〜のことだから」は、その人の性格や日ごろの様子をよく知っているという前提から、確信をもって推量する言い方。慎重な部長ならすぐには返事をしない、という推量に合う。1「からには」は動詞や形容詞の普通形に付く形で、名詞「部長」には接続できない。2「にかけては」は「… | — |
| 問題7-37 | 4 | OK | 「〜ことから」は、ある事実を根拠として名前や判断が生まれたことを表す。水が緑に見えるという事実が「みどり池」という呼び名の由来になっている。1「をもとに」は名詞に付いて材料や土台を示す形で、「見える」という動詞の普通形には接続できない。2「につれて」は二つの変… | — |
| 問題7-38 | 3 | OK | 「〜てからでないと」は、前のことを済ませなければ後のことはできない、という必要条件を表す。検査を受けることが申し込みの前提になっている。1「るなり」は「〜するとすぐに」という意味で、後件は同じ人の直後の動作でなければならず、できないという規則は導けない。2「た… | — |
| 問題7-39 | 2 | OK | 「〜にしろ〜にしろ」は、二つのうちどちらの場合でも後件は変わらない、という並列の譲歩を表す。旅行でも家にいてもとにかく休みたい、という内容に合う。1「につけ家にいるにつけ」は、「うれしいにつけ悲しいにつけ」のように後件に感情や記憶が自然にわき起こることを述べる… | — |
| 問題7-40 | 1 | OK | 「〜おそれがある」は、好ましくないことが起こる可能性を表す。川の水があふれる危険を知らせ、近づかないよう求める文脈に合う。2「次第だ」は名詞に付いて「〜で決まる」を表すか、事情を説明して結ぶ形で、これから起こる危険の可能性は表せない。3「ことはない」はその必要… | — |
| 問題7-41 | 1 | OK | 「〜わけがない」は、そうである可能性はまったくないと強く否定する言い方。三年も働いてきたのだから知らないという可能性はない、という文脈に合う。2「はずだ」は根拠のある推量で、「知らないはずだ」では三年働いてきたという前提と正反対の推量になる。3「ものだ」は一般… | — |
| 問題7-42 | 3 | OK | 「〜よりほかない」は、ほかに方法がなくそうするしかない、という消極的な結論を表す。部品が遅れる以上、事情を説明して待ってもらう以外に手がない。1「までもない」はわざわざする必要がないほど当然だという意味で、対応が必要な場面と正反対になる。2「とは限らない」は断… | — |
| 問題8-43 | 4 | OK | 近所の子どもたちの(2)→書道の先生(3)→**として(4)**→この町で三十年を過ごしてきた(1)｜一意性: 24通り中1通り、裸の副詞なし。塊: 「近所の子どもたちの」は連体の「の」で終わり、直後に名詞を置くことを求めるので、名詞で始まる「書道の先生」の前… | — |
| 問題8-44 | 1 | OK | したがって(2)→会場までの道が(4)→**わかりにくい方は(1)**→早めにお出かけください(3)｜一意性: 24通り中1通り、裸の副詞は接続詞の「したがって」一枚のみで、文頭に固定。塊: 「わかりにくい」は「方」を主要部とする連体修飾節の述語であり、その主… | — |
| 問題8-45 | 4 | **要修正 (F3)** | `（家で）父「…」　母「…」` を一行に潰している。`bunpou.md` §"Dialogue/setting Markdown layout" は「Collapsing to `**40** （会社で）A「…」B「…」` is forbidden」。公式12/2024の問題8-44 は 娘「…」/母「…」 を別行に印字。同紙の問題7-33/39 は正しく分けており内部矛盾。 | 先に `check_consistency.py:1598` の問題8ステム正規表現を複数行対応にする（§5 の F3 行）。その後 `（家で）` / 父の行 / 母の行 に分ける。ゲートを直す前に紙だけ直すと FAIL する。 |
| 問題8-46 | 1 | OK | つまり(3)→今週中に資料を(4)→**仕上げなくてもよくなった(1)**→ということだ(2)｜一意性: 24通り中1通り、裸の副詞は接続詞の「つまり」一枚のみで、文頭に固定。塊: 「ということだ」は普通形の節を直前に取る形なので、四枚のうち普通形で終わる「仕… | — |
| 問題8-47 | 1 | **要修正 (F3)** | 問45と同じ。`（家で）姉「…」　母「…」` が一行。 | 問45と同じ。 |
| 問題9-48 | 3 | OK | [論理接続] 空欄の前は、補聴器は聞きたい声だけを選ばず、周りの音まで同じように拾って耳へ送る、という仕組みの説明。空欄の後は、そのために静かな所ではよく聞こえるのに人の多い店では声がうもれる、という帰結なので、「そのため」が入る。1「それにしても」は前の内容… | — |
| 問題9-49 | 4 | OK | [文末モーダル] 前の文で、音を選り分けるのは脳の働きであり、その働きが鈍っているあいだは音を大きくしても足りない、と述べている。この筋を受けて可能性を強く打ち消す「なるはずがない」が入る。1「ならないこともない」は打ち消しを弱めて可能性を認める形で、本文の主… | — |
| 問題9-50 | 1 | OK | [慣用・形式名詞] 早く楽になりたいという目的のために音量を上げ、その結果として補聴器そのものが使えなくなる、という筋なので、大事なことと小さなことを取り違えたという意味の「本末転倒である」が入る。2「一石二鳥である」は一つの行いで二つの利益を得ることで、ここ… | — |
| 問題9-51 | 2 | OK | [内容推論] 本文は、脳が音を選り分ける力を取りもどすまでには数週間から数か月かかり、静かな所から少しずつ慣らしていく必要がある、という筋で通っている。だから渡す側が最初に伝えるべきなのは、慣れるまでに時間がかかるという一言である。1「音は大きいほどよく聞こえ… | — |
| 問題10-52 | 4 | OK | 本文「音を出せない事情で出す人のほうが目立つ」「けれども、音を消したまま文字を追う見方は、もう制作側が先に考える前提になった」より、音を出せない場所で見る人を先に見こんで作る段階に入っている。1は「聞こえにくいから出す人より、音を出せない事情で出す人のほうが目… | — |
| 問題10-53 | 3 | OK | 本文「自分が作る側になって、ようやく分かりました」「同じ場所に立って初めて、そこで待つ理由が見えてきます」より、手順の意味は自分が同じ立場に立ったときに見えてくる。1は「ただの言い伝えだと思っていました」と、意味の分からないまま受け取っていた時期を振り返ってお… | — |
| 問題10-54 | 2 | OK | 本文「お名前をお呼びするのをやめ、番号札の番号だけでお呼び出しします」より、呼び出しが名前から番号に変わることを伝えている。1は読み上げる回数を減らすのではなく、名前を呼ぶこと自体をやめる。3は「受付で番号札をお取りになり」とあり、番号札は受付で受け取る。4は… | — |
| 問題10-55 | 3 | OK | 本文「何時から何時まで何をするのかを先に書き出せば、手は挙がる」「当日の持ち場と時間を並べた」より、募集の段階で一回ごとの受け持ちと時間を示すべきだと述べている。1は「配った先も部数も昨年と変えていない」とあり、同じ相手に配って申し出が三倍になったのだから、関… | — |
| 問題10-56 | 4 | OK | 本文「鍵をどうお渡しすればよいのかが分かりません」「お手数ですが、鍵のお渡しの仕方をご指示ください」より、鍵の渡し方をたずねている。1は費用については書かれていない。2は「こちらがいない間に入っていただいてかまいません」と、こちらから申し出ている。3は「羽根に… | — |
| 問題11-57 | 3 | OK | 本文「初日の点数と、その後の来館の回数との間には、これといったつながりが見えなかった」「まとめて買う券の有無も、住まいが近いかどうかも、同じである」より、打つ力や住まいの近さは来館と結びついていなかった。1と2は、いずれもつながりが見えなかったものである。4は… | — |
| 問題11-58 | 4 | OK | 本文「名前を覚えるかどうかは、こちらがしむけないかぎり、その日の運になってしまう」「名前を呼ぶ場面を一度作るための決まりである」より、呼び合う相手ができる場面をこちらから用意する必要がある。1は「ここでは対戦相手がその晩の顔ぶれしだいで組み替わる」とあり、同じ… | — |
| 問題11-59 | 1 | OK | 本文「片側を空けている間、段の半分はまばらなまま上がっていきます」「その間、立つ側には通勤客が並び、乗り口の手前が滞ります」より、段が空いたまま上がる一方で乗り口に列ができていた。2は「歩く人が絶え間なく来るわけではなく」とあり、逆である。3は「歩けないという… | — |
| 問題11-60 | 3 | OK | 本文「歩く人が縮める数十秒より、乗り口の列が長引く数分のほうが、駅の全体ではおおごとなのです」より、失われる時間のほうが大きいと考えている。1は駅の全体で見ると割に合わないとしており、逆である。2は時間帯を限る案は出てこない。4は階段の幅を広げる話は述べていな… | — |
| 問題11-61 | 1 | OK | 本文「結び目がないので、受け取った側は布を開くのに力が要らず、手つきも静かになります」より、力を入れずに開けるのが平包みの特徴である。2と4は「左右に引けば引くほど結び目は締まり」「両端を横に引き離すと、するりとほどけます」とあり、いずれも真結びのほうである。… | — |
| 問題11-62 | 4 | OK | 本文「渡したあとに何が起きるかが違うというだけのことです」「どちらを選ぶかは、包んだあとに布がどう扱われるかで決まります」より、そのあとの扱われ方によって選び分けるものだと述べている。1は布の値打ちや模様については触れていない。2は「どちらが優れているというも… | — |
| 問題11-63 | 1 | OK | 本文「押し入れの中の置き物たちは、買った瞬間にもう役目を終えていた」「買ったという出来事を残すための品だったからである」より、手に入れた時点で役目が終わっている品である。2は「結局いちばん高いものを買って」とあるが、作りについては述べていない。3は「押し入れの… | — |
| 問題11-64 | 3 | OK | 本文「使う品は違う。手に取るたびに、その日の空気が薄く塗り重ねられる」「布巾を絞るたびに、あの日の坂道のにおいが少しだけ戻ってくる」より、日々手に取る品のほうが旅の記憶をよびさますと考えている。1は「その土地でしか買えないものを探していた」ころの品が押し入れに… | — |
| 問題12-65 | 2 | OK | Aは「途中で止まる理由は、たいてい画面の外にある」と述べ、Bは「聞く相手の都合と、続けて座れる時間の長さが、人の手を止めていました」と述べており、どちらも慣れとは別の事情によるとしている。1はAが書き直しの多い記入欄に触れているだけで、Bは述べていない。3はB… | — |
| 問題12-66 | 3 | OK | Aは「書きかけを預かる仕組みを、まず入れてほしい」と仕組みがないことを問題にし、Bは「去年の秋から、申し込みの画面に書きかけを預かる仕組みを入れました」と入れたあとに分かったことを述べている。1はBに「ねらいは、機械に慣れていない方に最後まで進んでいただくこと… | — |
| 問題13-67 | 3 | OK | 本文「台の脇にかばんを置ける平らな面があること、こぼれた水をふく物が手の届くところに用意してあること、そして、その二つをまめに整える人が建物の中に決まっていることの三つである」より、三つがそろっていたことが共通点である。1は「玄関の脇にありながら、一年後には給… | — |
| 問題13-68 | 4 | OK | ①**この見当は外れた**の前に「人通りの多い入り口の脇に置けば使われるだろう、と考えた」とあり、あとには「廊下の突き当たりの、人の少ない場所にある台が、朝から晩まで使われていることもあった」とあるので、人通りの多さでは決まらなかったということである。1は建物… | — |
| 問題13-69 | 1 | OK | 本文「行き届いた足元があって初めて、機械は使われ続ける」「その二つをまめに整える人。この三つがそろっている建物では、給水機は五年たっても水を出し続けていた」より、足元を整える手があるかどうかで決まると述べている。2は「この見当は外れた」とある。3は数を増やすこ… | — |
| 問題14-70 | 2 | OK | 表の「夕方の迎え」の行の「九百円」と、【はじめてお使いになる方へ】の「きょうだいでご利用の場合、二人目からのお子さんは三百円引きになります」の二つを重ねる。一人目が九百円、二人目は三百円引きの六百円で、合わせて千五百円になる。よって2が正解。1は一人分だけの金… | — |
| 問題14-71 | 2 | OK | 【はじめてお使いになる方へ】の「はじめてご利用になる前に、サポートセンターでの顔合わせが必要です」と、「顔合わせは平日の午前十時から午後四時までで、一週間前までにお電話でご予約ください」の二つを重ねる。沢口さんは使うのが初めてなので、送りを申し込む前に顔合わせ… | — |
| 聴解問題1-1番 | 4 | OK | 先生「今回の授業は町の歴史などを各自図書館に行って、詳しく調べてみましょう」→町について調べる。次回はテーマ決め・商店街の人の話・クラスでの話し合いの回であり、今日はまだそこに至らない。 | — |  <!-- 2022-07:問題1-1 -->
| 聴解問題1-2番 | 3 | OK | 男「その間に、皆さんには私と一緒にそちらの倉庫から花の苗を運んでいただきます」→まず倉庫から苗を運ぶ。雑草抜きは「午前の方には雑草を抜いて、花壇の整備をしていただきました」と完了済み、目印を付けるのは職員の作業、苗を並べるのは「その後」。 | — |  <!-- 2021-12:問題1-2 -->
| 聴解問題1-3番 | 3 | OK | 1 ✗「開発メンバーを私が選んでみたんですけど」→課長が済ませた／2 ✗「来週の会議で私が紹介するから」→課長がやる／3 ○「メンバーを見て誰にどの仕事を任せるか決めておいてもらえますか？」→今やるべき作業／4 ✗「大まかなスケジュールは会議の資料の最後に載っていますから」→もうある。 | — |  <!-- 2025-07:問題1-3 -->
| 聴解問題1-4番 | 3 | OK | 男は「じゃ、土曜だな」と決め、そのあと「明日来るよ」と言い直したが、女「月曜日と祝日は、休館日でしょ」で否定され「じゃ、しかたない」と土曜に戻る。1 ✗ 2 ✗ 今日が日曜なので明日＝月曜は休館日。4 ✗ 祝日も休館日。 | — |  <!-- soumatome:cd2-32 -->
| 聴解問題1-5番 | 2 | OK | 男「今度の場所は駐車場がないんですよね。忘れてました」＝今日知らせるのはこれだけ。1 ✗「月曜日にメールしました」で済んでいる。3 ✗「開始時間はそのままだから、大丈夫ですよ」。4 ✗ 終わる時間も「それはもう月曜日のメールで」。 | — |  <!-- shinkanzen:cd2-47 -->
| 聴解問題2-1番 | 3 | OK | 「どちらとも言えないという人が、3分の1近くいます」＝約3分の1。1 ✗ 4 ✗「反対より賛成のほうが多い」。2 ✗ 賛成は「わずかに上回っている」程度で、3分の2には届かない。「半分以上」は回答した住民の割合。 | — |  <!-- soumatome:cd1-47 -->
| 聴解問題2-2番 | 2 | OK | 男「選手一人ひとりの体力の差が出ましたね」「チームグリーンは最後まで運動量が落ちませんでした」→アナウンサー「それが勝敗を分けたんですね」男「ええ、そういうわけです」＝選手の体力が上回っていた。1は「試合前はチームブルーに技術的に優れた選手が多くて楽な試合だろうと思われてた」＝負けた側の話、3・4は… | — |  <!-- 2021-07:問題2-2 -->
| 聴解問題2-3番 | 1 | OK | 「本音で話せた」「ここなら長く働けるかな」「ピンと来た」→働きやすそうだと感じたことが決め手。2 ✗「ほかの会社からも内定もらってた」→受かったのはここだけではない。3 ✗「元々はそっち(食品関係)の方に興味があった」→一番興味のある仕事ではない。4 ✗「事業内容とかにも関心はあった」→「も」で付け… | — |  <!-- kanzenmoshi:cd1-15 -->
| 聴解問題2-4番 | 1 | OK | 1 ○「庭がないんですが、花を育ててみたいとずっとずっと思ってたんですよ。それを友達に話したら、紹介してくれたんです」→始めたきっかけ。1が正解。／2 ✗「きれいになると町の人にも喜んでもらえて」→始めた後の感想／3 ✗「普段はあまり話す機会のない世代の方とも話せて、それも楽しみなんです」→後から加… | — |  <!-- 2025-07:問題2-4 -->
| 聴解問題2-5番 | 1 | OK | 「今日、木曜日の東京は雲一つない爽やかなお天気となっていますが、明日の午前中までとなりそうです」「東京は明日の午後から曇りとなり」→午前中は晴れるが、午後から曇る。雨は「明後日は朝から雨が降ったり止んだりの天気となる見込みで、夕方には大雨に変わるでしょう」＝明後日の話。 | — |  <!-- 2021-07:問題2-5 -->
| 聴解問題2-6番 | 3 | OK | 「さらに困難だったのはいくつもの国から協力してもらうこと」＝1番難しかったこと。計測器の開発も「非常に難しかった」がそれ以上、深海の温度測定は目的、データ分析は「時間もかかりますが」どまり。 | — |  <!-- 2023-07:問題2-6 -->
| 聴解問題3-1番 | 4 | OK | 1 ✗寂しさは「と言われることもありますが」と否定／2 ✗共通点ではなく「違って」と対比／3 ✗注意点の話はない／4 ○「旅先の一つ一つの経験をより深く味わえる」「穏やかな気分で過ごすことができる」→一人旅のよさ。4が正解。 | — |  <!-- 2025-07:問題3-1 -->
| 聴解問題3-2番 | 3 | OK | 「ちょっと見ておいていただけませんか」＝あるかどうかの確認の依頼。1 ✗ 持ってきてとは頼んでおらず、まず確認を頼んでいる。2 ✗「置き忘れたかもしれません」→あるかどうかは本人も知らない。4 ✗ 頼んでいるのは傘の有無の確認で、ソファーの状態ではない。 | — |  <!-- kanzenmoshi:cd1-20 -->
| 聴解問題3-3番 | 4 | OK | 「お客さんと直接接する…いろいろ気を使うことが多そうで」が女の学生の見方。1 ✗「立ちっぱなしだから？」→「それはいいんだけどね」と自分で否定。2 ✗「慣れたら大丈夫」は男の学生の発言。3 ✗「レジの方が時給はいい」→安いのは商品管理の方。 | — |  <!-- kanzenmoshi:cd1-21 -->
| 聴解問題3-4番 | 3 | OK | 1 ✗液体石けんが選ばれる理由の話ではなく、むしろ固形に変えた話／2 ✗人気のある種類の話ではない／3 ○「様々な形や色があって見た目も楽しめます」「準石けん分という成分が多く含まれていて、洗浄力が高いそうです」「プラスチックの容器がいらないので、環境にも優しい」→固形石けんのいいところ。／4 ✗目… | — |  <!-- 2025-12:問題3-4 -->
| 聴解問題3-5番 | 3 | OK | 「お勧めのプランのご紹介でお電話さしあげました」が用件そのもの。1 ✗ 注文の話は出ない。2 ✗「キャンペーン」は販促で、社会運動ではない。4 ✗ 発送の連絡も述べられていない。 | — |  <!-- soumatome:cd2-7 -->
| 聴解問題4-1番 | 2 | OK | 「おかゆすら食べられなかった」＝おかゆさえ食べられなかった→「何も食べられなかったの？」 | — |  <!-- 2025-07:問題4-1 -->
| 聴解問題4-2番 | 1 | OK | 「大したことない」＝軽いけが→安心する1。2 ✗ 心配は重いけがのときの反応。3 ✗「無理もない」は相手の言動に納得する表現で、けがの程度の話に合わない。 | — |  <!-- kanzenmoshi:cd1-36 -->
| 聴解問題4-3番 | 3 | OK | 「野菜が不足しがちなんだよね」＝足りていない→「気をつけて野菜も食べないとね」 | — |  <!-- 2023-07:問題4-3 -->
| 聴解問題4-4番 | 1 | OK | 「昼ごはん食べに行ったきりですね」＝出たまま戻っていない→「まだ戻られてないんですか？」 | — |  <!-- 2024-12:問題4-4 -->
| 聴解問題4-5番 | 1 | OK | 「乗り遅れるところでしたよ」＝結果的に間に合ったという報告を受けての反応→「間に合ってよかったですね。」 | — |  <!-- 2025-12:問題4-5 -->
| 聴解問題4-6番 | 2 | OK | 「取っといて」＝捨てずに残しておく提案→もう使わないと反対する2。1 ✗「取ってみよう」＝手に取る・応募するの意味にずれる。3 ✗ 提案に同意しており、会話が進まない同意の言い換え。 | — |  <!-- kanzenmoshi:cd1-30 -->
| 聴解問題4-7番 | 2 | OK | 「スタッフの分を含めて30個」＝合計が30個→「予約するお弁当は全部で30個ですね」 | — |  <!-- 2024-12:問題4-7 -->
| 聴解問題4-8番 | 3 | **自動不合格 (F1)** | 鍵3は本（完全模試 第1回 解答・解説 PDF p.35＝印刷 p.33、正答3）どおりで正しい。欠陥は選択肢2の文字起こし：本のインクは「だから**持つ**って言ったじゃない。」、リポジトリは「だから持って言ったじゃない。」＝ 持って＋言った で引用の って が落ちており日本語として成立しない。音… | `.agents/choukai-audio/references/textbook_items.json:2931` の当該行を「だから持つって言ったじゃない。」に直し、`make choukai-bank` → `make mp3 20260910_1 SEED=10323372`。再合成後 `logs/choukai_draws.json` が同一であることを確認する。あわせて 解説（「助言した側の言い方」）を、印字どおりの「相手が前に言った予定を持ち出して責める言い方」に書き替える。 |  <!-- kanzenmoshi:cd1-27 -->
| 聴解問題4-9番 | 2 | OK | 「〜たほうがいい」＝助言→これからする2。1 ✗「それで結構です」は相手の案を承認する言い方で、助言への返事にならない。3 ✗ 現在の状態を答えるだけで、助言に応じていない。 | — |  <!-- kanzenmoshi:cd1-33 -->
| 聴解問題4-10番 | 1 | OK | 「駅前にできたレストラン、行ったことある？」＝経験を尋ねている→行った上での感想「あぁ、あそこまぁまぁですね。」2・3は伝聞で、行ったかどうかの答えになっていない。 | — |  <!-- 2021-07:問題4-10 -->
| 聴解問題4-11番 | 3 | OK | 「お引き受けいたしかねます」＝引き受けられない→「あのう、どこが問題でしょうか」 | — |  <!-- 2023-12:問題4-11 -->
| 聴解問題5-1番 | 2 | OK | 花壇は「ゴミが多いのはベンチの周りだよね?あそこに花壇を作るのは難しいんじゃないかな」と退けられ、看板は「既にいくつか立ててあるから今以上に増やす必要ないんじゃないかな?」、見回りは「ボランティアの負担が大きくなるのはちょっとね」と保留。結論は「花壇を作る代わりにっていうアイディアが良さそうだね」＝… | — |  <!-- 2024-07:問題5-1 -->
| 聴解問題5-2番 質問1 | 1 | OK | 男の人は「時間がない時に会社でもできる運動を教えてもらおうかな」と言うが、続けて「まずは今どれくらい体力があるか測ってもらおう」と述べる。体力測定は「第1会場では体力測定を実施しております」。 | — |  <!-- 2024-12:問題5-2 -->
| 聴解問題5-2番 質問2 | 4 | OK | 女の人は「私はやっぱり毎日の献立かな？」と言うが、男の「最近ぐっすり眠れないって言ってなかった？お医者さんに相談してみたら」に「あ、そうだね。そっち先に行ってこよ」と答える。医師の個別相談は「第4会場では健康に関する悩みや相談に個別にお答えします。1時から4時まで医師がおります」。 | — |  <!-- 2024-12:問題5-2 -->

---

## 4. Findings

### F1 — 聴解問題4-8番: the banked transcript of option 2 is not Japanese, and is not what the MP3 says

**Class: automatic fail** (`exam-qa-review` §Ground rules — "broken Japanese anywhere").

The paper ships, in `tests/20260910_1/聴解スクリプト.txt` line 186 and in `聴解.md`'s
解説 cell for 問題4 8番 (line 201), and thence in `解答.html`, `練習.html` and
`詳細解説.json`:

```
2、だから持って言ったじゃない。
```

持って ＋ 言った with no quotative particle. It is not a sentence.

**What the source actually prints.** `refs/KanzenMoshi/JLPT_N2_Kanzen_Moshi-Taisaku.pdf`,
PDF page 35 = printed page 33 (第1回 解答・解説, left column, header 「1番　正答3」,
badge 27/CD1), rendered at 150/600/900 dpi:

```
M：あーあ、傘、持ってくればよかった。
F：1　じゃ、持っていこうか。
　　2　だから持つって言ったじゃない。
　　3　何だ、持ってないの？
```

At 900 dpi the glyph run after 持 is unambiguous: **full-size つ, then small っ, then て** —
持つ ＋ quotative って ＋ 言った. The repo dropped the full-size つ. The book's own line is
grammatical, so **the error is the repo's transcription, not the book's typography.**

**The audio corroborates the span.** `refs/KanzenMoshi/…/AudioCD1/Track27.mp3` (31.347 s).
`silencedetect=noise=-35dB:d=0.35` reproduces the bank's numbers to the centisecond: first
speech after the dropped 「1番。」 call at **4.1817 s** (bank `start 4.18`), last speech ends
**24.0977 s** (bank `end 24.08`), trailing silence **7.25 s** (bank `answer_pause 7.26`).
Option 2's run is 16.97–18.89 s = 1.92 s, the longest of the three, consistent with the
15-mora printed line and slightly long for the 14-mora repo string.

**The key is not affected.** The book prints 正答3; the bank says 3; the paper ships 3. The
item is answerable and correctly keyed either way. What is broken is the transcript a
learner reads and the explanation built on it.

**Second-order: the explanation glosses a line that is not there.** `詳細解説.json` (and the
booklet 解説 cell) say option 2 is 「助言したのに聞かなかった、と責める言い方。相手は助言を
受けていない。」 (VI: «đã bảo rồi mà», nhưng người kia chưa hề khuyên). That glosses a
「持ってけって言ったじゃない」-shaped line. The printed 「(傘を)持つって言ったじゃない」
reproaches the listener for **a prior statement of intent** ("you said you'd bring one"), not
for ignoring advice. The book gives no 解説 for this item at all — only a 言葉と表現 gloss on
the *correct* option (「何だ：「えっ、そうなの？」というような意味。予想や期待がはずれた軽い
驚き…」) — so the wrong-option rationale is the repo's own invention on top of a misreading.

**Systemic — two papers.** The bad string is hand-declared once, at
`.agents/choukai-audio/references/textbook_items.json:2931` (`kanzenmoshi:cd1-27`), and
flows into `logs/choukai_bank.json` and into **both** papers that have drawn the clip:

| paper | slot | artifacts carrying the string |
|---|---|---|
| `20260910_1` | 聴解問題4 **8番** | `聴解スクリプト.txt:186`, `聴解.md` 解説, `解答.html`, `練習.html`, `詳細解説.json` |
| `20260818_1` | 聴解問題4 **4番** | `聴解スクリプト.txt:172`, `解答.html`, `練習.html`, `詳細解説.json`, `模範解答.html` |

Two or more papers = systemic by the §6.5 recurrence test.

**Repair** (per §4 check 4 — *fix the bank's source and re-compose, never hand-edit `聴解.md`*):

1. `.agents/choukai-audio/references/textbook_items.json:2931` → `だから持つって言ったじゃない。`
2. Rewrite that item's `options_analysis[1]` and `kaisetsu_cell_text` in BOTH panes:
   「相手が前に『持つ』と言っていたことを持ち出して責める言い方。この一文だけでは、そう
   言った事実がないので話がかみ合わない。」 (VI likewise, **written**, not translated.)
3. `make choukai-bank` → `make mp3 20260910_1 SEED=10323372`, then **diff
   `logs/choukai_draws.json` and confirm the 29 clips are unchanged** (a one-character option
   edit must not move the draw; `freshest()` bars by id and the option-set constraint reads
   問題3 only, so it should not — but verify, do not assume).
4. Re-run `make sheet 20260910_1`, `make check`, and re-upload the MP3 if its bytes moved.
5. Do the same for `20260818_1`, which also needs `make model-answer` re-run.

### F2 — 問題4-15: the key 初霜 is off-band, and it is a pool defect

**Class: automatic fail** (`exam-qa-review` §Ground rules — "an off-level KEY … every
問題1–6 vocab key is the reviewer's").

```
**15** 今朝、庭に出てみると、草に今年の（　）がおりていた。
 1. 初雪  2. 朝露  3. 夕立  4. 初霜        [key 4]
```

Round 1 deferred this item (and eight others) as unsettleable because it was told the
`refs/` binaries were absent. They are present (4.6 GB). Settled against the pages:

| authority | result |
|---|---|
| Shin Kanzen N2-漢字, 別冊1 学習漢字リスト (1,046 kanji) | **霜 absent.** The ソウ/ゾウ run at PDF p.191 = printed p.58 is 掃/窓/装/想/層/総 … 憎/蔵/贈/臓. Checked visually. |
| Soumatome N2-語彙 | 霜 absent (0 occurrences) |
| はじめての N2単語 2500 | **absent.** Kana index p.305: はっこう → はっせい → はっそう → ばったり. No はつしも. |
| 31-sitting official archive | **zero real occurrences.** The 3 `霜` hits in `script.md` are 結→霜 OCR noise (「霜構語労した」= 結構苦労した; 「提宗された給料…霜高縮んだ柔」; 「和風のスカーフとか。霜の。」). |
| `refs/Shinkanzen/goi_reference.md`'s 13 `霜` hits | all the same OCR error: 「霜難袋」= 結婚式, 「霜論」= 結論, 「霜着」= 決着 |

Applying §2.5's two-direction test: would Shin Kanzen **N1** claim 霜? Yes — it is 常用 but
outside this repo's own N2 kanji list. Would an N3-or-easier book headline it? No.
**TOO_HARD.**

The shape is the one §2.5 names: **the key is harder than its own option set.** 初雪, 朝露 and
夕立 are all in-band; only the key is not. A candidate who does not know 霜 cannot reach the
item's actual discrimination (草に…おりる + 「今年の」初回性), which the 解説 states well.

**It is a pool defect, not an authoring slip.** `pools.json`'s `context_words` carries the bare
string 「初霜」 with no provenance field, and AGENTS.md §3 makes those four books the ONLY
authority for `context_words`. The word entered the pool from outside every authority.
`test_spec.json` and `logs/ledger.json` both record it faithfully, so nothing was substituted —
the draw itself is the defect, which is exactly the case `exam-qa-review` §2b routes to a
re-draw: *"When no rule-compliant set exists, the TARGET is the defect."*

**Repair:** delete 「初霜」 from `pools.json`'s `context_words`; `--reroll-one context_words:<index>`;
re-author 問題4-15 keeping `answer_positions`' 4; state the new key's band in the report as
「key X drawn, band checked against <book, page>」 (§3); mark the surface `"origin": "reauthored"`
with a `"note"` in `test_spec.json` AND `logs/ledger.json`; update `logs/topics.json`'s row.
Do **not** hand-substitute a word — that is the 2026-08-17 incident AGENTS.md §0 opens with.

### The other eight deferred items — all settled, all in band

| item | verdict | evidence |
|---|---|---|
| 問題1-1 大通り / おおどおり | **IN-BAND** | Shin Kanzen 漢字 PDF p.154 = printed p.21, #205 通: 「とおる ｜ 通る　**〜通り**　通り　一通り」 with とお ruby. Official 7/2015 問題4-19 prints 「A ホテルは**大通り**に（　）いて」 unfuriganaed. |
| 問題1-2 燃料 / ねんりょう | **IN-BAND** | Shin Kanzen 漢字 PDF p.195 = printed p.62, #916 燃「ネン」, 第44回; 料 also listed. Official 12/2023 問題8-44 option 「４ **燃料**として」, no furigana. |
| 問題1-3 隔てる / へだてる | **IN-BAND** | 隔 is *not* in Shin Kanzen's 1,046-kanji list (checked カク runs at printed pp. 22/26/46), but **official 7/2013 問題6-32 is 隔てる itself** — 「２ 大きな川が二つの市を隔てている。」 へだ‑てる is 常用訓, not 表外. |
| 問題1-5 領事館 / りょうじかん | **IN-BAND** | Shin Kanzen 漢字 PDF p.202 = printed p.69, #1032 領: 「リョウ ｜ 〜領　**領事**(りょうじ)　領収　要領」 — the pair printed with furigana; 館 in the same list. 領収書 was a 12/2017 問題2 key. |
| 問題2-9 改定 / かいてい | **IN-BAND** | Shin Kanzen 漢字 PDF p.162 = printed p.29, #322 改「カイ ｜ **改正**(かいせい)」. 改訂 is an option in official 12/2014 問題4 — the same-reading 改定/改訂 pair is precisely what 問題2 is built on. |
| 問題4-16 軽減 / けいげん | **IN-BAND** | Shin Kanzen 漢字 PDF p.164 = printed p.31: #356 軽「ケイ」, #366 減「ゲン ｜ 加減」. Official 7/2012 reading passage: 「女性社員の**負担を軽減する**と同時に」, no furigana. |
| 問題4-17 別荘 / べっそう | **IN-BAND (top of band)** | 荘 absent from all four extracts and from the ソウ run of the kanji list, **but** 別荘 appears unfuriganaed in official 12/2013 問題11 (「多田家の**別荘**の庭」) and 12/2011 問題14 (「政治家の**別荘**を別館として公開」). Known as reading vocabulary; as a 問題4 key it sits at the ceiling. |
| 問題6-27 分担 / ぶんたん | **IN-BAND, decisively** | Shin Kanzen 漢字 PDF p.192 = printed p.59, #853 担「タン ｜ **担当**(たんとう)　負担(ふたん)」, 第42回. And **official 7/2019 問題4-19 keys 分担 itself**: 「家事や育児は夫婦で（　）／１分別 ２区別 ３区分 ４**分担**」. |

**No 問題1 pool defect.** All four (漢字, 読み) pairs are 常用音訓 — no 表外音訓 like the
`領(えり)` case the skill names.

### F3 — 問題8-45 and 問題8-47 collapse a dialogue stem onto one line

**Class: 要修正.** The items are solvable and correctly keyed; this is a printing defect
that also exposes a gate that rewards the forbidden form.

```
SHIPPED  **45** （家で）父「最近、姉さん、帰りが遅いね。」　母「今の会社を辞めて、＿＿ ＿＿ ★ ＿＿らしいよ。」
SHIPPED  **47** （家で）姉「この子、小学生なのにもう百六十センチあるのよ。」　母「本当ね。＿＿ ＿＿ ★ ＿＿。」
```

`question-authoring/references/bunpou.md` §"Dialogue/setting Markdown layout" (lines 98–113):

> do NOT crush the stem onto one line … (1) `（会社で）` alone on the stem's first line after
> `**N**`; (2) each speaker turn on its own following line; (3) the option row still on ONE
> line under the turns. **Collapsing to `**40** （会社で）A「…」B「…」` is forbidden** — reads
> as a drill line.

**Official does not collapse.** `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md`, 問題8-44:

```
44 娘「今度のスピーチコンテスト、参加しようかなあ。でも、自信ないなあ。 」
  母「チャレンジ ★ ？いい経験になると思うよ。 」
```

Two lines, ★ on the second. And **this same paper's 問題7-33 and 問題7-39 are correctly
split** across lines, so the paper contradicts itself between 大問.

**Why it happened — the gate rewards the violation.** `tools/check_consistency.py:1598`:

```python
stems = {int(n): s for n, s in re.findall(r"^\*\*(\d+)\*\*\s*(.+)$", m8_text, re.M)}
```

First line only. Then `check("問題8 stems offer 4 blanks with ★ third", …)` requires the
`＿＿ ＿＿ ★ ＿＿` run inside that captured line. Founding-case run, required by §6.5 and done —
I ran the predicate on both layouts of item 45:

| layout | first-line stem captured | slots | stars | gate |
|---|---|---|---|---|
| `bunpou.md`-mandated, multi-line | `（家で）` | 0 | `[]` | **FAIL** |
| shipped, collapsed | `（家で）父「最近、姉さん…＿` | 4 | `[2]` | **PASS** |

So an author who follows the owner's rule fails the gate, and the only way to green is to
break the rule. **Fix the gate first; a paper-only fix will fail `make check`.**

**Recurrence — 8 papers on disk.** `20260904_2` (問題8-44), `20260910_1` (45, 47), and six
imports: `imported-n2-2021-07` (44, 45), `-2021-12` (45, 46), `-2023-12` (46), `-2024-07`
(43, 46), `-2024-12` (44, 46), `-2025-12` (44, 45). The imported ones are worse than a style
slip — they are **transcription-fidelity defects**, because the sittings they transcribe print
the turns on separate lines (12/2024 shown above). Same single cause.

**Repair:** widen the 問題8 stem capture to read from `**N**` up to the option row (the same
multi-line span `build_booklet.py` already renders as one question), re-run the check over
every paper on disk and state which ids move (§6.5's rule for a changed scope), then re-split
45 and 47 in this paper. The imports' fidelity should be re-checked against their pages in a
separate pass — not this paper's work.

---

## 5. Root causes (§6.5)

| id | root cause | recurrence | owning file | concrete proposed edit |
|---|---|---|---|---|
| **F1** | `GATE-BLIND` — a hand-declared textbook clip's TEXT is verified by nothing. `build_textbook_bank.py` guards **duration** and **char rate**; `check_choukai_*` compares the script against the composed MP3's *segmentation*, never against the source book. A transcription error is therefore invisible to every gate, and it propagates into the script, both 詳細解説 panes, the booklet 解説 cell and the model answer. | **2 papers** (`20260910_1`, `20260818_1`) from **1** bad declaration → systemic. | `tools/check_consistency.py` + `.agents/choukai-audio/SKILL.md` | (a) Add `check_textbook_script_grammaticality()`: over every `textbook_items.json` `script_lines` entry, flag a line matching `て\s*(言|い)っ` / `って?\s*言った` malformations — concretely, a `〜て` gerund immediately followed by 言っ with no `と`/`って` between. **Founding-case run, required before commit:** the predicate must fire on `kanzenmoshi:cd1-27`'s 「だから持って言ったじゃない。」 and on nothing else in the 425 banked records. (b) `choukai-audio` Part 0: add to the hand-declaration procedure — *"A declared `script_lines` block is a TRANSCRIPTION of ink. Read it back against the rendered page before banking it, and record the PDF page you read in `source_page`. The duration and rate guards do not read the text."* (c) `exam-qa-review` §4: add a sixth composed-paper check — *"6. Read every hand-declared (non-`official`) clip's `script_lines` aloud. The official half is machine-extracted from a sitting; the textbook half is typed by hand from a scan, and nothing checks it."* |
| **F2** | `RULE-UNENFORCEABLE` + `GATE-BLIND` — `pools.json`'s `context_words` entries are bare strings with **no provenance field**, so nothing can assert that a drawn word is attested in one of the four authorities AGENTS.md §3 names, and no gate has ever read a 問題1–6 key's band (the skill says so itself: *"no gate has ever checked a 問題1–6 key"*). | **1 confirmed off-band key here**; unmeasurable across the pool until provenance exists — which is the finding. | `.agents/exam-blueprint/references/pools.json` + `.agents/exam-blueprint/SKILL.md` + `tools/check_consistency.py` | (a) Give every `kanji_reading`/`context_words`/`paraphrase`/`usage` entry a `source` field naming the authority and page (`"shinkanzen-kanji p.62 #916"`, `"hajimete #472"`, `"official 7/2019 問題4-19"`). (b) Add `check_pool_vocab_provenance()`: WARN while coverage is below 100 %, listing untagged entries — **never lower the bar to make it green** (the pattern the two existing coverage WARNs already use). (c) Backfill by scanning the four extracts plus `refs/JLPT_N2_NEW/*/booklet.md`, and **delete every entry that resolves to none of them** — 初霜 is one; there are likely others, and finding them is the systemic half of this finding. |
| **F3** | `GATE-WRONG` — the check exists, mis-measures, and its silence was never evidence. Worse than blind: it actively rewards the layout its own owner forbids, so eight papers were shaped by it. | **8 papers** (2 generated, 6 imported) → systemic. | `tools/check_consistency.py:1598` (+ re-verify the 6 imports) | Replace the first-line capture with a span capture: `re.findall(r"^\*\*(\d+)\*\*[ \t]*(.*?)(?=^\s*1\.\s)", m8_text, re.M|re.S)` — the stem is everything between the item number and the option row, which is what the booklet renders as one question. Re-run over every paper on disk and **print which ids move**, per §6.5's rule for a changed scope. Then re-split `20260910_1`'s 45/47 and `20260904_2`'s 44. |
| **S1** | Round 1's **F2-a** (`RULE-UNENFORCEABLE`: the rhetorical-MOVE cap names no move vocabulary) was written out verbatim in round 1's report and **never applied**. `grep` of `.agents/jlpt-test-generation/SKILL.md` finds no SKELETON text; the file's only change today is the slot-free clip bar. | 3 papers ≥6 on the passage proxy per round 1. | `.agents/jlpt-test-generation/SKILL.md` §"One topic, one surface" | Apply round 1's F2-a text as written. It does not block this paper — the paper is repaired — but it blocks the next run, which has nothing to read. |
| **S2** | Round 1's **F2-b** (`GATE-BLIND`: `check_dokkai_belief_denial_monotony()`) was **never added** — `grep -n "belief_denial" tools/check_consistency.py` returns nothing. | same 3 papers. | `tools/check_consistency.py` | Apply round 1's F2-b text as written. I re-derived the predicate by hand over all 36 papers on disk in its absence (§6); the numbers reproduce round 1's founding-case run, so the check is ready to land as specified. |

**Effect on the loop.** F1 and F2 block this paper. F3 blocks it only after its gate is fixed
(and the gate fix must come first). S1 and S2 do not touch this paper and **must be applied or
explicitly rejected before the next test is authored** — they will reproduce.

*On S1/S2's status, checked rather than assumed:* `qa/root-cause-dispositions-20260910.md`
exists and records dispositions for an earlier round's rows (R2-S1/S2/S3, plus one paper-level
row rejected as a rider), but it **predates this paper's round 1** — its R2-S2 is the very
check-5 wording round 1's S1 then corrected — and it says nothing about F2-a or F2-b. So they
are not rejected-with-a-reason; they are simply unapplied. Either apply them or record a
disposition, but do not let them pass silently into the next run.

*Also carried forward and still open from that file:* the rejected-as-a-rider row — a composed
paper draws 21 `listening_scenarios` + 11 `quick_response` entries it never spends, and the
ledger burns their cooldown anyway. This paper does it too (`test_spec.json` draws 21 + 11; the
shipped 聴解 half is 29 banked clips using none of them). Not this paper's defect and not
repairable here, but it is the reason §6.2's cooldown intersect had to skip those two
categories.

---

## 6. Coverage

### Steps run

| step | on | result |
|---|---|---|
| 0 blind solve | `qa/20260910_1/keyless.md` (rebuilt), all 101 | 100/101; §2 |
| 0 blind strategy ×2 | 問題10–13, n=18 | 33.3 % / 5.6 %, margin −0.0431 |
| 1 key-by-key proof | all 101 | §3 walkthrough |
| 2 distractor elimination | all 101 | one line per wrong option read; §3 |
| 2b plausibility | 問題1–6 option sets, 聴解問題1–3 grounding | no 3:1 tone split, no single-clause-three-✗ 解説 |
| 2.5 level band | all 問題1–9 keys **against the actual pages** | **F2**; other 8 deferred items settled in-band |
| 3 mechanical reads | below | **F3**; rest clean |
| 4 聴解 (composed) | checks 1–5 **all re-run in full** | below |
| 5 topic table | this paper + `20260909_1` + `20260907_1` | below; clean |
| 6 provenance & spec | spec / ledger / positions / corpus scan | clean |
| 6.5 root cause | 5 rows | §5 |

### §3 — the counts this pass is required to print

| measurement | owner's band | this paper |
|---|---|---|
| 問題1/2/5 stems with no 「、」 | author ≥9 of 15; official 47–93 % | **13 of 15 (87 %)** ✓ |
| 問題1–5 stems in です・ます | author 7 of 25; official 2–11 | **5** ✓ (inside official) |
| 問題1/2/5 stem length | archive max 21.5 | median **16**, max **18** ✓ |
| 問題7 stem mean | 36–52 JP chars | **44.6** ✓ |
| 問題7 stems under 34 | ≥2 | **2** (問34=28, 問41=32) ✓ |
| 問題7 max−min | ≥25 | **35** (63−28) ✓ |
| 問題7 dialogue/setting-label stems | >0 | **4** (33, 38, 39, 40) ✓ |
| 問題8 option sum | typically 16–29 | 31 / 31 / 28 / 28 / 33 — three above the descriptive band, none a three-word drill |
| 問題9 cloze body | ~500–700 | **656** ✓ |
| 問題9 option max length | official max 14 | **14** ✓ (at the ceiling) |
| 問題9 blank categories | 4 distinct, ≥1 whole-passage | 48 [論理接続] / 49 [文末モーダル] / 50 [慣用・形式名詞] / 51 [内容推論] ✓ — 51 needs the last paragraph's time-lag |
| （注N） in-body markers | gate WARN below 25; target 30–40 | **28** ✓ (28 definitions, **0 orphans either way**) |
| （中略） | >0 | **3** ✓ |
| `<ruby>` in 言語知識・読解.md | 0 | **0** ✓ |
| 問題13 length | ≥800 JP chars | **937** ✓ |
| 読解 option-length ratio (問題10–13) | WARN >1.65, FAIL >2.50 | worst **1.43** ✓ |
| (tied-)longest key rate | ≤35 % (official 30 %) | **28 %** ✓ |
| **uniquely** longest key rate | ≤30 % (official 20 %) | **22 %** ✓ (items 56, 62, 66, 68) |
| 読解 key paraphrase | no LCS ≥15 & ≥50 %; no LCS ≥20; no lift | worst **12** chars (問58, 36.4 %) ✓ |
| （注N） basic-word glossing | fail any | **none** — all 28 headwords rare/literary/specialized |
| （注N） byte-identical reuse | fail any | **none** across every paper and every official booklet |

**One grammar point, one KEY per paper.** All 21 問題7/8/9 keys are distinct forms. I grepped
each keyed connective/modal across 問題10–14 passage prose **plus （注N） definition lines**,
excluding option strings (§3 exclusion 3): **every form scored 0 occurrences.** The single
non-zero was 〜として at 5 — all five inside the fixed 大問 instruction line 「後の問いに対する
答えとして最もよいものを…」, which is official boilerplate present in every sitting, not passage
prose. **Not a hit.** This matters because the F2 repair rewrote five surfaces, and the
`20260903_1` incident is precisely a repair planting a keyed form; it did not happen here.
(Observation, not a finding: 問題8-44 keys 順接接続 したがって and 問題9-48 keys そのため —
different FORMS, same functional family, in different tasks. The rule counts forms.)

**問題8, read by hand** (`make verify-scramble` returns UNDECIDED for all five by design):
each keyed order spliced end to end, then every option tried in every other slot, then the
zero-anaphora double-bind test on the が/は cards. 43: 2→3→4→1, chain welded by 〜の genitive
and として's noun host. 44: 2→4→1→3, したがって forced initial, ください forced final,
「会場までの道が」 can only be わかりにくい's subject. 45: 2→1→4→3, welded. 46: 3→4→1→2.
**47: 4→2→1→3** — 「伸び方が」 cannot bind to 「こえるだろう」 (a 伸び方 does not 背をこえる;
the covert subject there is 「この子」 from 姉's line), and 「今のような」 must sit adjacent-left
of 「伸び方」, so the pre-predicate chain is one unit, matching the tool's `FREE UNITS: 1`.
No option is a bare adverb; したがって and つまり are 接続詞, which official uses as cards.

### §4 — the five composed-paper checks, all five re-run in full

`聴解_チャプター.json` says `"source": "composed"`; the listening half was **re-drawn at 21:16**
after round 1, so a previous round's verification is evidence about clips no longer drawn.

**Check 1 — clip freshness, both bars.**

| | vs `20260909_1` | vs `20260907_1` |
|---|---|---|
| same-slot repeats | **0** | **0** |
| any-slot repeats (the slot-free bar) | **0** | **0** |

Within-paper duplicates 0. No starvation note in the composer output. Source mix
official 18 / kanzenmoshi 7 / soumatome 3 / shinkanzen 1 = 29. Round 1's F4 root-cause bar is
live in `compose_choukai.freshest()` and `MUTUALLY_EXCLUSIVE_CLIPS` carries the F3 pair.

**Check 2 — audio round-trip.** `python3 tools/choukai_segment.py tests/20260910_1/聴解.mp3` →
`ok  20260910_1  45.8 min  LUFS -16.09  問題1:5 問題2:6 問題3:5 問題4:11 問題5:2`. **5/6/5/11/2
recovered.** ✓

**Check 3 — do the printed options belong to the audio?** This environment cannot play audio,
so I replaced the by-ear spot check with a **measurement**, and extended it from 2 items to
all 29. (a) For six items spanning all four sources I extracted the composed segment at its
chapter mark and the source span at its banked offsets, downsampled both to 4 kHz mono and
cross-correlated the 10 ms log-energy envelopes:

| slot | clip | source file | best envelope corr | lag |
|---|---|---|---|---|
| 問題1-4 | soumatome:cd2-32 | 32.mp3 | 1.013 | 3.74 s |
| 問題1-5 | shinkanzen:cd2-47 | Track47.mp3 | 1.006 | 3.74 s |
| 問題2-4 | 2025-07:問題2-4 | imported 2025-07 聴解.mp3 | 0.955 | 0.00 s |
| 問題3-2 | kanzenmoshi:cd1-20 | Track20.mp3 | 0.986 | 3.74 s |
| 問題4-8 | kanzenmoshi:cd1-27 | Track27.mp3 | 1.059 | 3.72 s |
| 問題5-2 | 2024-12:問題5-2 | imported 2024-12 聴解.mp3 | 0.974 | 0.00 s |

Every lag is 0.00 s for an official clip (which carries its own 「N番。」) and 3.72–3.74 s for a
textbook clip (`needs_number_call: true`, the harvested call spliced in front) — the lags are
themselves a consistency check. (b) Deterministically, for **all 29 clips**: every banked
`script_lines`/`script` block occurs verbatim in `聴解スクリプト.txt` (0 misses), and every
printed option block in `聴解.md` matches its own clip's bank record (0 misses; 問題5-1番 has
no printed options by format, correctly). **No slot prints one sitting's options over
another's audio.** I did not listen — a human should still play two items before the commit.

**Check 4 — keys come from the source sittings.** All 30 shipped keys traced to
`logs/choukai_bank.json`: 17 official `answers` entries and 11 textbook `answer` fields plus
問題5-2's two — **0 mismatches**. The one blind-solve discrepancy (問題4-8番) traces to the
bank, and the bank's key is right; the bank's *text* is not (F1). Repaired at the bank, per
this check's own instruction.

**Check 5 — key balance vs the 31-sitting archive.** S1's corrected rule. I re-measured the
band from `refs/JLPT_N2_NEW/answer_keys.json` myself rather than trusting the row:

| 大問 | shipped keys | distribution | modal | archive band (re-measured, n=31) | |
|---|---|---|---|---|---|
| 問題1 | 4,3,3,3,2 | 2:1 3:3 4:1 | 3 | 2–4 (median 2) | ✓ |
| 問題2 | 3,2,1,1,1,3 | 1:3 2:1 3:2 | 3 | 2–4 (median 2) | ✓ |
| 問題3 | 4,3,4,3,3 | 3:3 4:2 | 3 | 2–4 (median 2) | ✓ |
| 問題4 | 2,1,3,1,1,2,2,2,3,1,3 | 1:4 2:4 3:3 | 4 | 4–7 (median 5) | ✓ at the arithmetic floor |
| 問題5 | 2,1,4 | all distinct | 1 | 1–3 (median 2) | ✓ |

**S1's band reproduces exactly** (問題1 2–4, 問題2 2–4, 問題3 2–4, 問題4 4–7 median 5,
問題5 1–3), and the corrected text is in `.agents/exam-qa-review/SKILL.md` line 620.
Round 1's S1 is verified applied and verified correct. Note the old wording really was
unsatisfiable: 問題4's 11 items over 3 options force a mode ≥4, and this paper sits at exactly 4.

### §5 — whole-paper and cross-test topic table

**Authored surfaces (14) — no subject twice, in any register.** 問題9 補聴器と脳の音の選り分け /
10(1) 字幕制作 / 10(2) 弁当のおかずを冷ます数分 / 10(3) 市民課の呼び出しの番号化 / 10(4) 手伝い
募集の紙の書き直し / 10(5) 換気扇の異音の点検依頼メール / 11(1) 卓球開放日の初日の五分 /
11(2) 動く階段の片側空け / 11(3) 風呂敷の平包みと真結び / 11(4) 旅の土産の置き物と布巾 /
12(A/B) 申し込み画面の書きかけ保存 / 13 給水機の足元 / 14 子育て送迎サポート案内. Thirteen
distinct subjects (12A/B share by format). No authored subject repeats `20260909_1` or
`20260907_1`.

**Headline-theme set (問題9/12/13/14/聴解問題5-1番/5-2番), built from the shipped content:**

| | this paper | `20260909_1` | `20260907_1` |
|---|---|---|---|
| 問題9 | 医療・福祉 | 地域活性化 | 食 |
| 問題12 | デジタル化 | 交通 | 住まい |
| 問題13 | 環境 | メディア・情報 | 働き方 |
| 問題14 | 子育て・家族 | スポーツ・余暇 | 旅行・観光 |
| 聴解問題5-1番 | **地域活性化** | 消費・経済 | 行政・手続き |
| 聴解問題5-2番 | 睡眠・健康 | 住まい | 文化・伝統 |

Intersection with the immediately-previous paper: **{地域活性化}, one slot** — and it falls
entirely on 聴解問題5-1番, a clip lifted from a real sitting. **The four AUTHORED headline
slots intersect `20260909_1` at zero.** `exam-blueprint` rule 4's zero-tolerance clause is
satisfied on everything anyone here chose. Intersection with the paper-before-last: **empty**
(rule 4 allows one). This is the WARN the gate raises and instructs be read as a draw audit;
I confirm that reading — there is no repair short of seed-shopping, which this repo forbids.

**Closing-move column, read twice.** Labels: 説明 2 (問題9, 11(3)) / 反論応答 2 (10(1), 11(2)) /
随筆 2 (10(2), 11(4)) / 実用文・分類外 2 (10(3), 10(5)) / 主張 2 (10(4), 12(A)) / 条件提示 2
(11(1), 13) / 意外な観察 1 (12(B)) = 13. **Every shape at or under the cap of 2.** Read again
down the SENTENCE SKELETONS: 分裂文 「〜のは、…だ」 appears **zero** times (the skeleton that
crossed every label in `20260904_1` F2); 「〜ていた のだ（後知れ）」 zero (`FINAL_TEMPLATE_CAPS`
≤1); the closest pair is plain past-progressive 「止めていました」(12(B)) and 「出し続けていた」(13),
two, inside the shared cap. No pile-up.

**Repair-collateral check on round 1's F2 — where did the five re-angled surfaces land?**
The skill requires this be verified by re-reading, never by `make check`:

| surface | new closing (last sentence) | new skeleton | label |
|---|---|---|---|
| 問題9 | 「この時間の差が、はじめのひと月に集まっている。」 | Xが〜に集まっている | 説明 (was 意外な観察) |
| 問題10(1) | 「けれども、音を消したまま文字を追う見方は、もう制作側が先に考える前提になった。」 | Xは…になった | 反論応答 |
| 問題10(4) | 「何時から何時まで何をするのかを先に書き出せば、手は挙がる。」 | 〜ば、… | 主張 |
| 問題11(1) | 「初日に名前を呼び合う相手ができた人ほど、三か月後も台に来ている割合が高かった。」 | 〜ほど…が高かった | 条件提示 |
| 問題11(2) | 「…歩く人を通した日の記録を、どの時間帯でも下回りました。」 | Xを下回りました | 反論応答 |

**Five distinct skeletons.** Two share the label 反論応答 — exactly at the cap of 2, and their
skeletons and personas differ (a subtitler's trade report vs a decade of platform counts).
The pair did not survive the repair wearing different clothes.

**The F2 proxy itself, re-derived by hand** (round 1's F2-b check was never added, so I ran
its predicate myself over all 36 papers on disk):

| corpus | range |
|---|---|
| official `imported-n2-*` (n=10) | **0–3** |
| other generated (n=25) | 0–4 |
| **`20260910_1`** | **3** — 問題12(A), 問題12(B), 問題13 |

Round 1 measured **6** before the repair. Counting 12(A)+(B) as one surface, as round 1's own
F2-a text prescribes, the paper is at **2** — exactly the cap. On the separate-surface scale it
is 3, at the top of the official band and below round 1's proposed WARN threshold of >3.
The `logs/topics.json` note's claim of 2 uses the A/B-as-one convention and is consistent.

**`logs/topics.json` row — all eight required keys present and verified.** `surfaces`, `themes`,
`closing_moves`, `voices`, `claim`, `persona`, `shapes`, `notes` all present (grepped, not
assumed). `themes` values all inside `level_data.THEMES`; `closing_moves` all inside the six
shapes plus 実用文・分類外 — **no invented label** (the `20260904_2` defect). I re-read every
`surfaces` and `claim` line against its item naming who did what — including 聴解問題5-2番,
the slot where `20260903_1` swapped its two speakers: the row says 「男の人はまず体力を測って
もらい、女の人は…眠れないことを医師に相談する」, and the script has the man say 「まずは今どれ
くらい体力があるか測ってもらおう」 and the woman 「そっち先に行ってこよ」 after being told
「お医者さんに相談してみたら」. **Correct, not swapped.** Every string quoted in `notes` still
occurs in the paper.

*Bookkeeping observation, not a finding:* `notes` is a chronological log and its Stage-3
paragraph still says 「問題9 … closing move 意外な観察」 and a pre-re-draw key tally
(問題1=3, 問題2=2, 問題3=3, 問題5=2, 問題4 最頻5) and source mix (soumatome 2 / mimikara 1).
Both are **explicitly superseded later in the same field** by the F3/F4 paragraph (which
states 問題1=3 問題2=3 問題3=3 問題4=4 問題5=1 and official 18 / kanzenmoshi 7 / soumatome 3 /
shinkanzen 1 — all of which I reproduced exactly) and by the F2 paragraph (which states the
問題9 move moved to 説明). The last word on every number is correct. Worth knowing when the
next blueprint reads this row.

### §6 — provenance and spec audit

1. **Target item match, all of 問題1–8.** Every tested item is the exact drawn target:
   `kanji_reading` 大通り/燃料/隔てる/中止/領事館 · `orthography` 珍しい/一休み/教養/改定/近寄る ·
   `word_formation` 前〜/〜制/〜放題 · `context_words` 予防法/初霜/軽減/別荘/くわしい/乗る/沿う ·
   `paraphrase` 夢中になる/あいにく/はるかに/およそ/ぼんやり · `usage` 検討する/分担/対策/築く/貢献する ·
   `grammar_p7` ×12 · `grammar_p8` ×5. **No unrecorded substitution.** (問題3-13 prints 飲み放題
   where the pool's illustrative example is 食べ放題 — the drawn target is the affix 〜放題, so the
   tested item is the drawn one.) `logs/ledger.json`'s entry matches `test_spec.json` **field for
   field** in all six vocabulary categories; `pools_sha` `4119aed1e4b0` matches `pools.json`;
   seed 96722689; **no `harvest_sha` field at all**, so nothing date-shaped was fabricated.
2. **Rotation cooldown.** Intersected this test's draws with the previous two ledger entries
   (`20260907_1`, `20260909_1`), folding okurigana/kana tails: **0 overlaps** in all eight item
   categories. (The apparent hits in `listening_scenarios`/`reading_topics` are whole pool-bucket
   objects, not drawn strings — and on a composed paper the drawn `listening_scenarios` are not
   used at all.)
3. **Answer positions.** All **71** 言語知識・読解 keys equal their prescribed
   `answer_positions` — 0 mismatches across all 14 blocks. The 30 聴解 positions differ from the
   spec, which is correct and expected: the composer sets them and `check_answer_positions`
   skips them for a composed paper. `test_spec.json` **does** carry `answer_positions` (19 blocks),
   so the "0 prescribed" automatic fail does not apply.
4. **Copyright non-reproduction — re-run on the re-authored surfaces**, because the scan that
   cleared the pre-fix text is evidence about text that no longer exists. Longest shared
   character run of each surface against 31 official `booklet.md` + every `imported-*` + every
   other generated paper:

   | surface | longest run | against |
   |---|---|---|
   | 問題9 **[re-authored]** | 9 (passage) / 58 = the fixed 大問 instruction line | 20260817_1 |
   | 問題10(1) **[re-authored]** | **9** 「のための備えという」 | 20260821_1 |
   | 問題10(4) **[re-authored]** | **10** 「る。人手が足りないと」 | 20260907_1 |
   | 問題11(1) **[re-authored]** | **10** 「ている割合が高かった」 | 20260828_1 |
   | 問題11(2) **[re-authored]** | **9** 「わけでもないのに、」 | 20260817_2 |
   | 問題10(2)/(3)/(5), 11(3)/(4), 13 | 9–15 | mixed |
   | 問題14 | 52 = the fixed instruction line only | — |

   Every real passage run is ≤15 characters. The 47–58 char runs are the 大問 instruction
   sentences every JLPT paper prints identically. `check_q14_apparatus_reuse()` (20+ char bar,
   three-corpus) is green, and my own scan agrees. No invented flavor detail cites a real
   source; the one number-shaped detail, 「申し出が三倍になった」, is the author's own
   N2-simplified invention with no decimal.

### The truncation incident — independent content verdict

**The reconstruction is faithful. Nothing was lost, paraphrased or truncated.** This is a
byte-level proof, not an inference.

The circular comparisons were unavailable — `qa/20260910_1/keyless.md` and all four HTML files
were regenerated from the current Markdown at 21:56 and after, so diffing them against the
Markdown proves nothing. The independent witnesses are `tests/20260910_1/_sections/`
(16:54–17:19, hours before both the F2 repair and the truncation) and round 1's report header,
which records the pre-repair revision as **`a12f0077186e` @ 19:00:49**.

Rebuilding a candidate from `_sections` and enumerating all 2^14 subsets of the 14 change
groups separating it from the shipped file yielded **exactly one mask reproducing
`a12f0077186e` byte-for-byte** (groups 0, 1, 2, 12). Therefore:

- the 19:00:49 pre-truncation file = `_sections` + four **pre-incident** authoring revisions;
- the shipped file (`fa043f11663b`) = that verified pre-truncation file **plus exactly groups
  3–11 and 13 and nothing else** — the ten hunks of the declared F2 repair (問題9, 10(1), 10(4),
  11(1), 11(2)) plus item 55's 解説;
- **every other byte** of the 102 KB file — 565 lines, all 14 大問, every stem, all 284 options,
  every （注N）, the 問題14 flyer table, all 71 key rows and 71 解説 cells — is identical to the
  pre-truncation bytes.

Corroborating integrity reads on the shipped file: 71 items, ids 1–71 complete, exactly 4
options each, none empty, none duplicated within an item; 71 key rows, 0 empty 解説; 28 in-body
（注N） against 28 definitions with **0 orphans in either direction**; the 問題14 table intact to
the last price and time (七百円/九百円/千三百円/千百円, all four time bands, all four deadlines,
plus 三百円引き and 一週間前までにお電話でご予約, which items 70/71 depend on); passage lengths
問題9 588, 10(1)–(5) 223–239, 11(1)–(4) 466–574, 12 530, 13 756, 14 346 JP chars — nothing thin.

Finally, every 「」- and backtick-quoted Japanese string in round 1's report and the stage-3
report was grepped against the shipped Markdown. **Every literal 読解/文法 string still
resolves except those belonging to the five deliberately re-angled surfaces** (e.g. 「そう思われ
やすいが、」, 「字幕は耳の聞こえない人のための備えだと長く言われてきた」, 「分けるのは腕前
だろうと思っていた。ところが、」), each confirmed to sit inside the pre-F2 text of a re-angled
surface and nowhere else. **Zero red flags.** The three `_sections`→shipped differences that are
not F2 (item 32's blank re-cut from 「尋ねてみた（　）」 to 「尋ね（　）」 with the options
absorbing てみた; items 45/47's collapsed dialogue; item 39's 解説 sharpened to quote the item's
own words) all predate the incident and are inside the verified 19:00 bytes. Items 45/47 are
nonetheless a real defect on their own merits — **F3**.

### `make check` — the full accounting

Run at the start of this pass: **1 FAIL, 165 WARN.**

**The FAIL** — `20260910_1: 詳細解説.json explains every keyed item (30 entries for 101 keys)`.
Stage 5 has not run; `詳細解説.json` currently holds only the 30 聴解 entries the composer
wrote. Expected, **not a finding**, and `make model-answer` must not run until F1 and F2 are
repaired and the keys are locked (AGENTS.md §5).

**Four WARNs name this paper — not two.** The brief's accounting under-counted by two:

| WARN | resolution |
|---|---|
| 聴解問題5 repeats a headline theme of `20260909_1` (`地域活性化`) | **Not a false positive; not repairable.** Composed slot, nobody here chose it, the 読解 half has nothing to re-angle. Draw audit; confirmed in §5, where the four authored headline slots intersect at zero. |
| no 聴解 slot repeats its own theme in the previous 2 papers — 聴解問題3-1番 = 旅行・観光 (also `20260909_1`) | **Not a false positive; not repairable.** Same class. The previous paper's item is an interview about a ten-room inn filling up; this is a first-person talk on the pleasures of solo travel. Tag shared, 決め手 not shared, different 質問型. |
| the errand-rotation check compares most of the draw (1/44 = 2 % keyed) | **Pool-metadata gap, not this paper's defect** — but it means the rotation check is *silent* here. I covered it by hand: the `shapes` column read plus the cooldown intersect (§6.2, 0 overlaps) is the errand read this WARN says is missing. |
| the 問題8 form-family check compares most of the draw (1/5 = 20 % tagged) | Same class, same silence. Covered by hand: `grammar_p8` = 〜として / 順接接続 / 目的達成 / 換言要約 / 仮定帰結 — five distinct families, and none collides with any of the twelve 問題7 forms. |

**Six WARNs are the grandfathered pre-rule papers** of round 1's new
`check_choukai_option_set_reuse()`: `20260811_1`, `20260814_1`, `20260821_1`, `20260828_1`,
`20260903_1`, `20260904_1` — confirmed six, all `[pre-rule paper]`, none this paper. The
remaining 155 WARNs name other tests and are outside this review's scope.

**Artifact freshness** — no artifact predates its source: 言語知識・読解.md 21:56:38 → .html
21:56:46; 聴解スクリプト.txt 21:16:26 → 聴解.mp3 21:17:04 → チャプター 21:17:05; 解答/練習.html
21:56:47. `聴解.mp3`'s sha256 `7ef3b9ea56ab…` equals `logs/upload_manifest.json`'s
`audio/20260910_1.mp3` entry, so the release asset is current.

---

## 7. Skips — stated explicitly

1. **I did not listen to the audio.** This environment cannot play sound. §4 check 3 was
   satisfied by measurement instead (envelope cross-correlation on six clips across all four
   sources, plus a deterministic all-29 script/option identity diff) — strictly stronger
   coverage than the two-item spot check the skill asks for, but not the same evidence as
   listening. **A human should play 問題1-4番 and 問題4-8番 before the commit.**
2. **`refs/` binaries were used.** All present (4.6 GB). The nine items round 1 deferred are
   settled against the actual pages (§4), using ~20 page renders of Shin Kanzen 漢字 (sliced,
   252 MB), the はじめての kana index, and the 完全模試 解答・解説 (sliced, over cap). No number
   in this report was substituted from memory or from another sitting.
3. **Round 1's F2-a and F2-b were verified NOT applied** and are re-filed as S1/S2. I did not
   apply them — the reviewer proposes skill edits and never applies them to generation skills
   mid-review.
4. **No file was edited.** Not the paper, not `logs/`, not `tools/`, not
   `.agents/exam-qa-review/SKILL.md` (my skill already carries S1's corrected text, verified at
   line 620, and I found no defect class missing from it this round). All scratch work is in
   `/tmp/qa2*`.
5. **Not run:** `make sample`, `make mp3`, `make model-answer`, `git commit`. No other test's
   folder was modified. The unrelated uncommitted work (練習モード translation toggle, today's
   composer fixes) was left alone.
6. **Not re-verified:** the six `imported-*` papers' 問題8 dialogue-layout fidelity (F3's
   recurrence set). I measured the recurrence and named the ids; checking each against its own
   scanned page is a separate import-fidelity pass, not this paper's work.

---

QA: FAIL (3 findings, 2 automatic)
