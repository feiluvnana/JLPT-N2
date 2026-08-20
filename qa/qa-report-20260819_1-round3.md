# QA report — テスト 20260819_1 (round 3, fresh eyes — final round the pipeline allows)

Reviewed revision (sha1[:12] over raw bytes; re-verified unmoved after the pass):

- `言語知識・読解.md` = `8aac663cf0ff`  (mtime 2026-08-20 16:05:56)
- `聴解.md` = `0ccc5b80910c`  (mtime 2026-08-20 15:57:58)
- `聴解スクリプト.txt` = `b856e2fc0de8`  (mtime 2026-08-20 11:19:47 — **unchanged since round 1**)
- `聴解.mp3` (mtime 11:22:19) / `聴解_チャプター.json` `script_sha` = `b856e2fc0de8` (matches), `pacing_sha` = `d241e428f28f`
- `qa/20260819_1/keyless.md` = `6bd5508b3e9b` — rebuilt after the pass, **byte-identical**, so no fixing pass edited underneath this review.

Reviewed 2026-08-20. The reviewer authored nothing in this paper, read
`exam-qa-review/SKILL.md` in full from disk before its first other tool call,
and solved all 101 items blind from `qa/20260819_1/keyless.md` before opening
any key table, any 解説, or either previous round's report. **Nothing is
inherited from round 1 or round 2** — every claim those rounds and the two fix
passes make was re-derived here from disk, including all five 問題8 items over
all 24 permutations each, and both new gate detectors re-run against their own
founding cases.

Entry condition: `make check` **exit 0**, "All checks passed (30 skipped), 138
warning(s)". **No WARN or FAIL line names `20260819_1` as its subject** (its own
per-test block: 96 `ok`, 4 `skip`). Three WARN lines *mention* the id inside
citations to `qa-report-20260819_1`; their subjects are other papers.

---

## 1. Verdict

**QA: PASS**

Zero paper findings remain open. All 101 items and the four 例 were solved
blind at **101/101**, every key was proved against its deciding line, every 問題8
item was derived unique over all 24 orderings independently of the 解説, and
every one of the four pipeline repairs round 2 demanded was re-run here against
the incident that motivated it — including reconstructing the pre-fix strings
and executing the predicates on them.

**Three claims relayed to this round were found to be wrong, and are corrected
in §6:** `聴解.md` is *not* unchanged since round 1 (its sha moved; the change is
the authorised observation-2 fix and touches no item); the new
`verify_scramble` detector does *not* fire on 問題8-44 in the shipped paper
(the fix pass removed the offending wording, so it fires on zero items on disk
— it fires correctly on all five reconstructed founding cases); and
`check_key_grammar_exposure` reads the form via `grammar_form_parts()`, not
`grammar_form_tokens()`. None of the three changes the verdict.

**Four skill/gate findings are open (§5).** None blocks this paper; per §6.5
each blocks the NEXT generation run until applied or explicitly rejected. The
largest is that `bunpou.md`'s new 問題8 construction rule — written by the
round-2 fix pass — is **under-scoped**: it counts free *co-arguments* of the
final predicate and therefore cannot see the argument-vs-adjunct-clause case,
which is what 問題8-45 actually is. 45 survives, but it survives on a judgment
argument the rule does not license, and the next 45-shaped item will not.

**Nothing here is "safe to ship as recorded" in the sense of a suppressed
defect** — the eight items in §7 are calibration observations against rules
that do not exist yet, not breaches of rules that do. The reviewer does not
invent a bar mid-review (`exam-qa-review` §"The reviewer does not negotiate the
bar"), so they are filed as proposed rules with the measurements attached.

---

## 2. Blind-solve diff

**Solved from `qa/20260819_1/keyless.md`** (built by `make keyless 20260819_1`;
1088 lines; keys, key tables, marked answer grid and 解説 column stripped by
`strip_key()`). 聴解 solved from the embedded verbatim `聴解スクリプト.txt`.
All 101 answers were written down before any other file was opened, then
scored with:

```
python3 tools/qa_eval.py tests/20260819_1 --answers "[3,1,1,2,4, 2,4,1,2,3, 2,3,4, 2,1,4,3,4,3,1, 4,2,3,1,2,
 2,1,3,2,4, 1,3,1,1,2,1,3,4,2,2,4,4, 2,4,4,1,2, 1,3,2,4, 3,4,2,3,1, 1,3,4,4,3,2,2,1, 4,1, 2,4,2, 4,2,
 1,1,2,2,2, 4,3,3,1,4,2, 1,4,3,2,3, 1,2,3,3,1,2,2,3,3,1,2, 2,3,1]"
```

```
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches — nothing to resolve or file.** The reviewer's list was then
diffed by hand against `test_spec.json["answer_positions"]` group by group
(問題1 `[3,1,1,2,4]` … 聴解_問題5 `[2,3,1]`): all 19 groups identical, so step
6.2 is satisfied by the same artifact.

This is the third consecutive round at 100 %, by three contexts that authored
nothing. That is evidence about answerability, not about variety or level —
which is what steps 2b, 2.5 and 5 below are for.

---

## 3. Per-question walkthrough — all 101 items + 4 例

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 3 えんぜつ | OK | 「演**説**」の説は連濁してゼツ。2×2 {えんせ,えんぜ}×{つ,い} で四択が同じ語形、送り仮名なし＝非露出。えんせつ/えんぜい/えんせい はいずれも演・説自身の音読み派生（枝1） | — |
| 問題1-2 | 1 ほうがく | OK | {ほう,ぼう}×{がく,かく}。角は連濁してガク。ぼう は方の濁音化派生＝`exam-qa-review` §3 が認める清濁派生 | — |
| 問題1-3 | 1 なさけ | OK | 訓読み型（2×2非適用）。四択とも送り仮名「け」共通で非露出、たすけ/しつけ/いいつけ はすべて実在語・同分野（枝2） | — |
| 問題1-4 | 2 しゅっか | OK | 出は無声音の前で促音化。しゅうか は実在同音語「集荷」で最強の妨害肢。四択とも送り仮名なし | — |
| 問題1-5 | 4 つねに | OK | 四択とも「〜に」型副詞・送り仮名「に」共通。すでに/ただちに/しだいに は実在語（枝2） | — |
| 問題1 全体 | — | OK | 訓読み 2/5（情け・常に）＝ cap 2。gate `問題1 訓読み mix (2 of 5, cap 2)` ok。印刷漢字はすべて常用 | — |
| 問題2-6 | 2 漢和 | OK | {漢,緩}×{和,話}。漢=カン/緩=カン、和=ワ/話=ワ で四択とも「かんわ」と読める。緩和のみ実在語だが辞典の種類は表さない | — |
| 問題2-7 | 4 回転 | OK | {回,開}×{転,店}、四択とも「かいてん」。開店は実在語だが「軸を中心に」と結ばない | — |
| 問題2-8 | 1 削減 | OK | {削,作}×{減,限}、四択とも「さくげん」。他三つは疑似熟語（moji-goi §問題2 が明示的に許容） | — |
| 問題2-9 | 2 形容動詞 | OK | {形,型}×{容,要}、「動詞」は四択共通の固定部分。四択とも「けいようどうし」と読める | — |
| 問題2-10 | 3 意義 | OK | {意,異}×{義,議}、四択とも「いぎ」。異議は実在語だが「見いだす」と結ばない | — |
| 問題2 全体 | — | OK | 5/5 が {A,B}×{C,D} 格子、どの設問も仮名が四択すべての読みと一致（＝印刷どおりで解答可能）。gate `every 問題1/2 printed kanji is 常用` ok | — |
| 問題3-11 | 2 不 | OK | 「不十分」。未/無/非 は実在の否定接頭語で同一機能族、未十分・無十分・非十分 は不成立 | — |
| 問題3-12 | 3 沿い | OK | 「線路沿いに一キロほど続いている」。向き/寄り/越し はすべて実在の位置接尾語 | — |
| 問題3-13 | 4 まみれ | OK | 「ほこりまみれ」。ずくめ/がち/ぎみ はすべて実在の状態接尾語。全四択が同一機能族＝moji-goi §問題3（全部が付く必要はない） | — |
| 問題4-14 | 2 恐らく | OK | 文末「だろう」と呼応する陳述副詞。まさか＝打ち消し推量、いかにも＝〜らしい、案の定＝的中済み。四択とも陳述副詞 | — |
| 問題4-15 | 1 自営業 | OK | 「会社を辞め」＋「受け継いだ技術を生かして」。副業/兼業は本業の存在を要求、分業は複数人。四択とも働き方の名詞 | — |
| 問題4-16 | 4 煮る | OK | 「だし汁で」「やわらかくなるまで」が液中加熱を指定。焼く＝直火、蒸す＝湯気、炒める＝油。四択とも加熱調理の他動詞 | — （§7-1 に難易度の観察を記載。規則違反ではない） |
| 問題4-17 | 3 身が入らなかった | OK | 「休みの予定ばかり考えてしまい」が理由。気が済む＝満足、歯が立たない＝難しすぎる、目が届かない＝広範囲への注意。四択とも身体語慣用句の否定形 | — |
| 問題4-18 | 4 不足している | OK | 「必要な実務経験が半年ほど」＝必要量への未達。減少/低下/消耗はいずれも「以前より減る」型。（`不足している` は総まとめN2語彙 p.28 の見出し語「人手が不足している」で確認） | — |
| 問題4-19 | 3 開発 | OK | 「技術の〜に成功した」。開拓＝未開分野、発掘＝埋もれたものを見つける、製造＝設計どおり作る | — |
| 問題4-20 | 1 固い | OK | 「固い約束」＝破られない。厚い/濃い/重い はすべてイ形容詞・連体で、約束の破られなさは表さない | — |
| 問題5-21 | 4 わずかに | OK | 「うっすら」＝ごく薄く。置換確認「庭の草にわずかに雪が積もっていた」が成立。すっかり/たっぷり/厚く はいずれも量が多い側 | — （§7-2 に問題5内での再使用の観察） |
| 問題5-22 | 2 ぼんやりした | OK | 「うつろな目」＝何も映していない目つき。思いつめた/けわしい/落ち着きのない はいずれも別種の目つき。四択とも目つきの連体修飾 | — |
| 問題5-23 | 3 さらに | OK | 「いっそう」＝前より程度が増す。わずかに＝逆、一時的に＝一時だけ、思ったより＝予想との比較 | — |
| 問題5-24 | 1 強い驚きを与える | OK | 「衝撃的な」。心を温かくする/思わず笑ってしまう/少しも珍しくない はいずれも別の印象。四択とも印象を述べる述語 | — |
| 問題5-25 | 2 遅い | OK | 「押してから記録されるまで」が時間の長さを話題にしている。弱い＝強さ、短い＝逆、大きい＝程度 | — |
| 問題6-26 | 2 特定 | OK | 「汚染を引き起こした工場が特定された」＝候補から一つに絞る正用。1＝決定、3＝把握、4＝保つ | — |
| 問題6-27 | 1 切れる | OK | 「しょうゆが切れてしまい」＝在庫が尽きる正用。2「話が切れて」は途切れる の誤用（慣用は 話が途切れる）、3＝割れた、4＝枯れて | — （§7-3） |
| 問題6-28 | 3 分解 | OK | 「古いラジオを分解して、故障の原因を調べた」＝部品にばらす正用。1＝分担、2＝決裂、4＝分割 | — |
| 問題6-29 | 2 吟味 | OK | 「市場で吟味した魚だけを客に出す」＝品質を評価して選び取る正用。1＝確認、3＝修復、4＝見直した | — （§7-3） |
| 問題6-30 | 4 重なる | OK | 「法事と入学式が同じ日に重なって」＝同時同所の正用。1＝増えて、2＝かかった、3＝膨らんで | — |
| 問題6 全体 | — | OK | 15 の誤用文を moji-goi §問題6 の現行規則（「学習者が作りそうな壊し方か」「第二の実在コロケーションでないか」、2026-08-19 の domain 規則撤回後）で読み直した。第二の実在コロケーションは 0 件。gate `contains no banned collocations` ok | — |

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 気になってならない | OK | 「〜つもりでいたが、やはり」＝抑えられない感情の告白。2は余裕がない意で「やはり」と逆、3は禁止、4は一般的性質の否定 | — |
| 問題7-32 | 3 道も空いていることだし | OK | 「思い切って〜ことにした」を後押しする軽い理由列挙。1は悪い結果を要求、2は対比要素が後続しない、4は同一主体への非難 | — |
| 問題7-33 | 1 待つよりほかない | OK | 「原因が分からない以上」を受ける唯一手段。2は待てない事情を要求（前提が逆）、3は他人の推量、4は助言 | — |
| 問題7-34 | 1 駅ビルの完成とともに | OK | 完成と人の流れの移動が並行。2は対応させる変数がない、3は時間関係が逆、4は「完成」を材料にできない | — |
| 問題7-35 | 2 静かなものの | OK | 静か（長所）と吸引力が及ばない（短所）の逆接。1わりに は「静か→吸引力が強い」期待を作れず「及ばない」と結べない、3は原因結果、4は同方向の添加 | — |
| 問題7-36 | 1 吐くことだ | OK | 震えを訴えるAへの助言。2は推量、3は話し手自身の決定、4は一般的道理 | — |
| 問題7-37 | 3 長く続けていく上で | OK | 辞書形＋上で＝判断の場面、後半「大切なのは〜だ」を導く。1は変化を表し不変の評価と噛み合わない、2は二つ目の事柄が来ない、4はた形接続 | — |
| 問題7-38 | 4 に越したことはない | OK | 後続「もっとも、読み通すには時間がかかる」という但し書きと自然に接続。1は価値を下げる、2は打ち消す主体が文中にない、3は一般論の主語がない | — |
| 問題7-39 | 2 ができて以来 | OK | 開店を境に現在まで続く減少。1は後にこれからの行動が必要、3は境目を表せない、4は条件 | — |
| 問題7-40 | 2 のことだから | OK | 「用心深い彼女」の性格を根拠に「〜はずですよ」と推測。1は観察事実を要求、3は確認済みの納得、4は実際に起きた事の理由 | — |
| 問題7-41 | 4 慌てることはない | OK | 「まだ二週間ある」が根拠の「その必要はない」。1は「そんなに」を受けられない、2は逆方向、3は手段の不在 | — |
| 問題7-42 | 4 調べてからでないと | OK | 後半の否定「何とも申し上げられません」と呼応。1は当然の帰結を作り矛盾、2は肯定的結果、3はその機会の行動を要求 | — |
| 問題7 全体 | — | OK | **三数値すべて実測**: 平均 **41.2** JP字（帯 36–52）、34字未満 **3** 本（下限2）、最大−最小 **42**（下限25）。会話・場面ラベル付き stem あり（33 (会社で)、40 (電話で)、36 A/B）。同一形が3項目以上の選択肢に出る事例なし（5仮名窓で最大2＝shipped `P7_FORM_REUSE_MAX`） | — |
| 問題8-43 | 2 決めている | OK | **24通りを独立に走査**。［長年の経験に→基づいて］は「基づいて」が直前の に 名詞句を要求し該当が一枚のみ、［決めている→そうだ］は伝聞そうだが直前の普通形を要求し該当が一枚のみ。2塊の順は B-A が文末を そうだ 以外にしてしまうため不可 → 1通り。カード側の自由共項 **0**（を目的語は stem 内） | — |
| 問題8-44 | 4 受け継ぐ人が | OK | 24通り走査。「あの技術を」は「受け継ぐ人」を主要部とする連体修飾節の**内側**なので離脱不可（隣接の根拠は連体修飾＝規則が認める源）。「つまり」は前文を言い換える接続表現で空欄先頭のみ。印刷済み「という」が普通形を要求し最終は「身内にいなかった」 → 1通り。自由共項 **1** | — |
| 問題8-45 | 4 受け付けを | OK | 24通り走査。［申請書に不備が→あった場合は］は が が存在述語を要求して固定。対抗順 `(4)→(1)→(2)→(3)`「窓口の担当者は、受け付けを申請書に不備があった場合は断らねばならない」を実際に読み、**却下**：裸の を 目的語を は 標示の条件節の左へ出す操作は、43/47 を壊した節内 NP-NP スクランブリングとは別物で、(i) 「〜場合は」は は により枠設定機能を持ち節頭を強く要求する、(ii) 句読点なしで連結される問題8の印刷形では「受け付けを申請書に」が誤導的な二重格連続を作る。**文法的だが idiomatic ではない**ので「文法的・慣用的・意味等価」の三条件を満たさない | 項目は維持。ただし **45 は規則ではなく判断で生き残っている** — §5 R3-S1 参照 |
| 問題8-46 | 1 心細いものは | OK | 24通り走査。「ときほど」は形式名詞 とき を含み連体修飾述語を要求（該当は「体を壊した」のみ）。「心細いものは」の は は述語を要求（該当は「ない」のみ）。「AほどBはない」が2塊の順も語彙的に固定 → 1通り | — |
| 問題8-47 | 2 変えている | OK | 24通り走査。「AだけでなくBも」が［味だけでなく→皿の色や明るさも］を語彙的に順序づけ（逆順は も が付加相手を失う）。「から」が直前の普通形を要求し［変えている→からだ］固定。冒頭「〜のは」が理由の言い切りを要求し最終は「からだ」 → 1通り。を目的語は stem 内 | — |
| 問題8 全体 | — | OK | 裸の副詞カード 0（gate ok）。5項目とも抽選された `grammar_p8` を実現（gate ok）。`make verify-scramble 20260819_1` = ARTIFACT ok ×5、**PROOF LEG INVALID 0 件**、RESULT UNDECIDED ×5（仕様どおり——一意性はこの表の手読みが根拠） | — |
| 問題9-48 | 1 それでいて | OK | 前文「家族の命を守るために玄関に置かれている」と後文「一度も背負われないまま」＝一つの物の相反する二面。そのうえ＝同方向、なぜなら＝理由でない、そこで＝行動でない。[論理接続表現] | — |
| 問題9-49 | 3 役に立たないわけだ | OK | 直前二文が「運べない」事情を説明済み → 当然の帰結。1は全否定で段落と逆、2は意志的行為用、4は部分否定で段落を打ち消す。[文末モーダル] | — |
| 問題9-50 | 2 そもそも無理がある | OK | 「持ち出す量と家に置く量を同じにしようとするところに」を受け発想自体の欠陥を指摘。1は「ところに」を受けない、3は比較相手がない、4は段落と矛盾。[慣用・形式名詞] | — |
| 問題9-51 | 4 持ち出す分と残す分に分ける | OK | 第3段落「備えを二つに分ける考え方」＝全体の趣旨。1は残りを家に置く説明を落とす、2は説明と正反対、3は最終段落の結果の一つ。[内容推論] | — |
| 問題9 全体 | — | OK | 4つのカテゴリが全て相異なり [内容推論] を1件含む（gate ok）。本文 **689** JP字（帯 500–700）。選択肢最長16字（gate ok、公式現行最大14の近傍） | — |

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | 決め手の行 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 3 | OK | 「丈の高い植生（注1）が、川と林とをつなぐ回廊（注2）になっているためである」＋「刈り取れば道筋は分断され、数年たっても戻らない」。1は「刈られた土手は歩きやすく」と逆、2は費用の記述なし、4は最後の観察結果で目的ではない | — |
| 問題10-53 | 4 | OK | 「立ち上げ（注1）の遅れが最も短かったのは、操作に最も慣れた班ではありませんでした」＋「伝票の余白に気づいたことを書き残す習慣のあった班です」。1はこれに反する、2は書式の記述なし、3は今後の話 | — |
| 問題10-54 | 2 | OK | 「食べ物と飲み物は、手作りかどうかにかかわらずお売りになれません」。1は「市外の方はお申し込みになれません」に反する、3は「前もってのお振り込みはできません」に反する、4は「五月十日に延期します」 | — |
| 問題10-55 | 3 | OK | 「まずこの感じ取る力が落ちる」＋「実際に働く汗腺の割合が減る」＋「この二つが同じ時期に進む」。2は「汗腺（注2）の数は変わらない」に反する | — |
| 問題10-56 | 1 | OK | 「支援策の数を数える前に、必要な人が何か所を回らされているかを数えるべきである」。3は窓口分割を問題視しているので逆 | — |
| 問題11-57 | 1 | OK | 「その空いた時間に流れ込んだのは、真偽（注3）の確かめられていない書き込みだった」＋「何も出さない時間帯を、人は黙って待ってはくれない」。2は逆、3は費用の記述なし、4は裏取りの速さに触れない | — |
| 問題11-58 | 3 | OK | 「この三つを言い分けて数字を出しておけば…理解は崩れない」＋末尾「誤りに気づいてから直し終えるまでを短くする段取りである」。2は試した結果が逆 | — |
| 問題11-59 | 4 | OK | 「分かれ目は、代わりのバスの経路をいつ引き始めたかにあった」。3は「過疎（注3）の進み方も、高齢者の割合も、両者でほとんど変わらない」に反する | — |
| 問題11-60 | 4 | OK | 「廃止の議論が続いているあいだに、通学と通院の時刻を住民から集め」「経路を先に引いていた」。3は「駅を起点（注5）にするのをやめて」と逆 | — |
| 問題11-61 | 3 | OK | 「自分が消えたあとに残る困りごとを、一つずつ数えていたのだ」＋鍵の予備・地主の名前・猫の餌・鉢の返し先。1は「預金や保険の欄はほとんど空白のまま」に反する | — |
| 問題11-62 | 2 | OK | 「書き留められていたのは、片づけようのない結び目（注5）のほうだった」＋「誰かに返すもの、誰かに頼むこと、誰かが困ること」 | — |
| 問題11-63 | 2 | OK | 直後「交流を売り物にした家では、一年以内に退去（注3）する人の割合が、そうでない家の二倍近くに上っていた」 | — |
| 問題11-64 | 1 | OK | 「洗濯を待つ数分のあいだに言葉を交わす」＋「話したくない日は、そのまま部屋へ戻る」。2は「共用の居間は狭く」と逆 | — |
| 問題12-65 | 4 | OK | A「座っている時間を集めても、その日に何が前へ進んだかは一行も分からない」／B「席に着いている時間を数えても仕事の中身は見えないという点も、そのとおりだと思う」。3はBの立場でAは成果測定自体を否定していない | — |
| 問題12-66 | 1 | OK | A「週の初めに今週終える仕事を三つまで書き出し…確かめる手順」／B「見えにくい仕事を評価の表に書き入れておかないかぎり」。2はAが「私はこの方向に反対である」 | — |
| 問題13-67 | 2 | OK | 「単語も文末の言い方も共通語になっているのに、声の高さの動きだけはその土地のものが残っていることが多い」。1は残る/変わるが入れ替わり | — |
| 問題13-68 | 4 | OK | 「前者は資料を増やし、後者は機会を増やす」＋末尾「記録は、言葉を資料に変える作業である。継承は、言葉を口に出せる場面を増やす作業である」 | — |
| 問題13-69 | 2 | OK | 「だが、要るものが違う」＋末尾「二つを同じ名前で呼んできたあいだに…」。4は「抑揚（注1）が最後まで残る」と逆。**obs.5 の書き換え後の鍵**（「一つの言葉でまとめて呼ぶことはできない」）を本文と突き合わせ済み——依然として本文の主張であり、逐語引用でもない | — |
| 問題14-70 | 4 | OK | 「市立美術館の特別展は共通券の対象外です」＋「別に800円が必要です」＋学生券の使える期間欄「買った日と翌日」の**2セル以上**を結合。1は期間欄に反する、2は「ほかの割引とを合わせてお使いになることはできません」、3は郷土博物館の共通券欄が「一回」 | — |
| 問題14-71 | 2 | OK | 「中学生以下のお子様は、どの施設も入館無料ですので、券は必要ありません」＋郷土博物館・市立美術館の休館日欄「月曜日」の**2セル結合**。3は使える期間欄「買った日と翌日」、4は「十名以上の団体…三日前までに」 | — |
| 読解 全体 | — | OK | 20項目すべて max/min ≤1.30。**唯一最長率 5/20 = 25 %**（公式20、目標≤30）、**同着含む最長率 6/20 = 30 %**（目標≤35）。逐語持ち上げ 0（gate ok）。絶対量化子・全否定による一目消去 0 件 | — |
| 読解 装置 | — | OK | 本文中 （注N） **32**（問題10=6／問題11=20／問題13=6）、定義行も 32 で 1対1、孤立定義 0。目標帯 30–40 内、下限25超。注の見出し語は 植生/回廊/立ち上げ/放熱/汗腺/申請主義/第一報/裏取り/真偽/錯綜/風評/存廃/輸送人員/過疎/乗り合い/起点/簞笥/エンディングノート/罫線/終活/結び目/所帯/呼び水/退去/設え/土間/抑揚/話者/継承/方言札/土着/規範 — **禁止リスト（選択・信号・技術・文化・質・準備・手順・設計・現象・経由・偏り・維持・継続・前提・細部・バランス）に該当ゼロ**、循環定義ゼロ。`<ruby>` **0 件**。（中略）**4 箇所**（問題11×3・問題13×1、すべて中文/長文の内側）。長さ: 問題13 = 1049 JP字（下限800）、各節の下限も gate ok | — |
| 読解 marked span | — | OK | ①は 5 件（57/59/61/63/67）。各設問の引用文字列と本文の太字が**完全一致**（「空白は情報の不在ではない」12字／「同じ人口減少の下でこの差が出る」14字／「残しておいたのは手続きではなかった」16字／「看板を高く掲げた家ほど短命だった」15字／「単語から先に置き換わる」11字）。すべてポインタ長で、推論を丸ごと含む長さではない。（注N）が太字の内側に入る例なし | — |

### 聴解 (例 + 30項目)

| 項目 | 鍵 | 判定 | 決め手 / 誤答の根拠行 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 3 | OK | 「参加する人の名前、先にまとめてくれる?」。**アナウンスの3番＝マークシートの (3)** で一致し、会話も3を支持。1「人数は、名前がそろってからでいいよ」2「バスは会計の中村さんが取ってくれてるって」4「しおりなら、去年のを直してもう作ってあるの」 | — |
| 問題1-1番 | 1 | OK | 「配る資料が足りなくなっちゃって。悪いんだけど、追加でコピーしといてくれる?」。2「いすは明日の朝、みんなでやろう」3「先生、今日は外の講習に行っててつかまらないんだ」4「名札は、受講が決まった方にしかお出しできない決まりでね」——3誤答すべて台本行あり | — |
| 問題1-2番 | 1 | OK | 「分け終わった袋を、あそこの軽トラックまで運んでくれる?」。2「道具はね、数がそろわないと渡せなくて」3「名前は、書いてもらわなくていいの」4「駐車の場所は、今年は作らないことにしたの」 | — |
| 問題1-3番 | 2 | OK | 「今回のいすは、その金額を超えちゃうから、悪いけど、二社にお願いしてくれるかな」。1「型番なら、去年の注文書に書いてある」3「サインは、来週の会議でまとめてもらうから、今はいいよ」4「数は、各部署から出してもらわないと分からないんだ」 | — |
| 問題1-4番 | 2 | OK | 「下の階の方に、天井にしみが出ていないか、声をかけていただけますか」。1「写真は、業者が伺ったときに撮りますので、けっこうです」3「修理の業者は、こちらから今日中に手配しておきます」4「管理人が今週、けがで休んでおりまして」 | — |
| 問題1-5番 | 2 | OK | 「かばんから出して、お手元にお持ちください」。1「重さは、出していただいてから、こちらで量りますので」3「あのシールは、係の者しか貼れないことになっておりまして」4「あちらは、生き物をお預けになる方の窓口です」 | — |
| 問題2-例 | 1 | OK | 「土曜は、朝のうちに三十人分しかご用意できないんです」＋「五十人はもう確定してます」。アナウンス1番＝マークシート (1) 一致 | — |
| 問題2-1番 | 4 | OK | 「その方の分だけ卵を外してお作りできます」→「じゃあ、そうしてください」。1「みんな仕事で無理なんです」2「土曜は六名様のお席がもう埋まっておりまして」3「個室はそのままお取りしております」 | — （§5 R3-S3 に問題2内の決め手軸の重複を記載） |
| 問題2-2番 | 3 | OK | 「この数字が、一日のうちのいつ高くなっているのか」＋「それがまだ分からないんです」。1「いえ、少し上です」2「お父様のことは、今回の数字とは結びつきませんよ」4「今回は出しません」 | — |
| 問題2-3番 | 3 | OK | 「注文を一人ずつ変えられるお店にしたいの」＋「みんなが食べられる方がいいと思う」。1「駅から少し歩くけど、注文を変えられるところにするか」2「三つとも、ほとんど同じ」4「今年はどこも個室が取れるから、そこは心配ないの」 | — （同上） |
| 問題2-4番 | 1 | OK | 「風呂の入れる回が決まってるなら、そっちに合わせます」。2「電車は予定どおり着いた」3「お部屋は、もうご用意ができております」4「お祭りは、先週で終わってしまいまして」 | — |
| 問題2-5番 | 4 | OK | 「うちには、そのゴムを置いてなくて」。1「ええ、電池はございます」2「交換はいつも私がしております。今日もおりますよ」3「この時計の部品は、今も作られております」 | — |
| 問題2-6番 | 2 | OK | 「駅の裏の駐車場でもお返しいただけますよ」＋「かぎは、駐車場の隣にあるお店にお持ちください」。1「空港は、今、工事をしておりまして、お預かりを止めております」3「こちらまで戻していただかなくても大丈夫です」4「あちらは、船に車を乗せるお客様だけのお預かりでして」 | — |
| 問題3-例 | 2 | OK | 「大きな水そうの前でお聞きいただきたいこと」＋三つの見方。アナウンス2番＝マークシート (2) 一致 | — |
| 問題3-1番 | 1 | OK | 「思い切って席を三十に減らしました」＋「今は、席が少ないのに、一年の売り上げは当時より上です」。**問題3は誤答に言及しない設計**（choukai-items §問題3）で、gate `問題3 monologues do not name their own distractors` ok | — |
| 問題3-2番 | 4 | OK | 「そのお客様が、その品物を何年、どんなふうに使うのかを先に聞くことだよ」＋「暮らしの話から始めれば、答えはお客様の方から出てくるんだ」 | — |
| 問題3-3番 | 3 | OK | 「返す日を延ばすことができるのは、次にお待ちの方がいらっしゃらない本に限ります」＋「延ばせるのは一度きりで」 | — |
| 問題3-4番 | 2 | OK | 「あの数字は、強さを表したものではないんです」＋「百回集めたとき、そのうち六十回は、一ミリ以上の雨が降りました、という意味なんですね」 | — |
| 問題3-5番 | 3 | OK | 「私がいちばん見ていただきたいのは、その本が、学ぶ人に自分のことを話させる作りになっているかどうか」＋「本を手に取るときは、そこを見てください」 | — |
| 問題3 全体 | — | OK | 話の長さ（`p3_talk_chars`）実測 **1番=306／2番=334／3番=311／4番=333／5番=337**、`聴解.md` 構成表の記載と**完全一致**（obs.2 の修正を再検証）。下限175・目標220+・公式中央値305 の帯内。5件とも 何について 型 | — |
| 問題4-例 | 3 | OK | 「あと少しなので、昼までには。」。アナウンス3番＝マークシート (3) 一致 | — |
| 問題4-1番 | 1 | OK | 「あちらでご記入をお願いします」に対し記入内容を確かめ返す。2は案内する側の言い方（立場逆転）、3は既に済ませたとして今後の記入と噛み合わない。敬語方向: 客→係員の丁寧体で一致 | — |
| 問題4-2番 | 2 | OK | 「代わりに出席していただけませんか」に翌日の空きを示して受ける。1は出席者に後で聞く側（立場逆転）、3は資料の話にすり替え | — |
| 問題4-3番 | 3 | OK | 「保険証の有効期限が切れております」に事情を述べる。1は話に出ていない前提、2は既に渡したとして今の指摘に答えない | — |
| 問題4-4番 | 3 | OK | 「騒音に関する苦情が入っております」に夜の作業をやめると答える。1は取り次ぐ側（立場逆転）、2は住人の立場（誤った前提） | — |
| 問題4-5番 | 1 | OK | 「勝つに決まってるよ」を過去の事実で打ち消す。2は「決まってる」の語義取り違え、3は時制の誤り | — |
| 問題4-6番 | 2 | OK | 「確認していただけますか」に変更の範囲を聞き返す。1は自分が送った側、3は「スケジュール」を予定表の意に取り違え | — |
| 問題4-7番 | 2 | OK | 「口が堅いから、相談しても大丈夫だよ」に応じる。1は「口が堅い」を食べ物の固さに取り違え、3は話と反対の前提 | — |
| 問題4-8番 | 3 | OK | 「手を焼いてるんです」にいつか終わると答える。1は論点のずれ、2は聞き分けがいいと逆に受け取る | — |
| 問題4-9番 | 3 | OK | 「締め切りを一日だけ延ばしていただけないでしょうか」に条件付きで受ける。1は自分が謝る側、2は時制の誤り | — |
| 問題4-10番 | 1 | OK | 「明日十時に弊社へお越しいただくことになっております」に部屋の空きを確かめる。2は話と反対、3は昨日の話 | — |
| 問題4-11番 | 2 | OK | 「指定席と自由席、どちらをご希望ですか」に属性で答える。1は「指定」の語義取り違え、3は案内する側 | — |
| 問題4 全体 | — | OK | 11項目の刺激文はすべて `test_spec.json` の `quick_response` 抽選文字列を実現（5番「〜に決まってる」→「勝つに決まってるよ」、8番「手を焼く」→「手を焼いてるんです」、10番の 10時→十時 は TTS 用の数詞表記。**未使用の抽選 0 件・未記録の差し替え 0 件**）。返事が はい/いいえ/では で始まる率 0%（gate ok）。敬語方向は11件とも成立 | — |
| 問題5-1番 | 2 | OK | 「中身を三種類だけにしておけば、そんなにかかりませんよ」→「あ、それならできそう」「じゃあ、それでいきましょう」。1は提案者自身が「開けたばかりの時期に、それは続けられないと思う」と撤回、3「火を使う口が一つしかないの」、4「箱代が思ったよりかかるのよ」 | — |
| 問題5-2番 質問1 | 3 | OK | 男「実は先週、相談の方を申し込んどいたんだ」「一時からで取っちゃってるから、授業とちょうど重なるんだよ」＋「学部を変えた人の話が聞きたくてさ」。1は時間重複、2「今から行っても、置いてあるのを見るだけだ」、4「名前がもういっぱいで」 | — |
| 問題5-2番 質問2 | 1 | OK | 女「私はもう決めてる。模擬授業。」で即決し最後まで不動。3は「私、申し込んでない」＋「当日のお申し込みは受け付けておりません」 | — |
| 問題5 印刷規約 | — | OK | 両項目とも選択肢を印刷せず読み上げのみ（gate `問題5 prints no options`）。2番は**属性で決まり、序数ではない**（gate ok）。質問1と質問2の読み上げ順が同一（模擬授業／研究室／相談/図書館）で、決め手の属性を選択肢名の横に印刷していない | — |

---

## 4. Findings table

**Paper findings: 0 open, 0 automatic.**

| # | 項目 | Class | Evidence | Status |
|---|---|---|---|---|
| — | — | — | No item was found mis-keyed, two-answered, unanswerable, off-band, ungrounded, or copied. | — |

Round-2's five findings were each re-verified as genuinely closed, from the
shipped bytes rather than from the fix pass's claims:

| round-2 finding | re-verified how | verdict |
|---|---|---|
| **R2-F1** 問題8-43 second ★ | Re-derived all 24 orderings from the shipped cards `1.そうだ/2.決めている/3.長年の経験に/4.基づいて`; two lexically-forced blocks, one legal concatenation, ★=2. The old rival is impossible because the を-object is no longer a card | **CLOSED** |
| **R2-F2** 問題8-47 second ★ | Same procedure on `1.からだ/2.変えている/3.皿の色や明るさも/4.味だけでなく`; 「AだけでなくBも」 orders one block, 「から」+普通形 the other, 「〜のは」 forces からだ last. ★=2 | **CLOSED** |
| **R2-F3** illegal 「を→他動詞→隣接」 leg | `grep 他動詞を要求` over the shipped 解説 = **0 hits**. 43/44/45/47 carry new legs; **each was judged on its own merits** — 43 伝聞そうだ接続 ✓ valid, 44 連体修飾節の内側 ✓ valid (and explicitly disclaims transitivity), 45 主題「〜は」の位置 ✓ valid *as an argument* though not as a rule (§5 R3-S1), 47 「AだけでなくBも」+「から＋普通形」 ✓ valid. No wrong-but-different argument found | **CLOSED** |
| **R2-F4** `check_key_grammar_exposure` label bug | Re-ran the extraction over **all 70** `grammar_p8` draws in `logs/ledger.json`: 46 are label-wrapped, and **0 now yield an unusable form** (`理由説明(〜のは…からだ)`→`['のは','からだ']`, `〜ほど〜はない`→`['ほど','はない']`, `対比表現(〜一方…だ)`→`['一方']`). Re-ran over all 14 papers: **`20260810_1` is the only id that gains a line** (`問題8 target「一方」×3`) and it is already in `KEY_EXPOSURE_GRANDFATHERED`. The 46-of-70 silent class is **genuinely closed** | **CLOSED** |
| **R2-F5** cleft-reason frame ×2 | Rebuilt the skeleton `のは[^。]{0,25}?からだ` under copula normalisation and ran it on (a) the reconstructed pre-fix sentences → **2 hits**, (b) the shipped 問題10–14 prose → **0 hits**. Independently, **every** 問題7/9 keyed form was grepped across the shipped 問題10–14 region: **0 occurrences of all 15**, against a ceiling of 1 | **CLOSED** |

---

## 5. Root-cause table (§6.5) — four OPEN skill/gate findings

None blocks this paper. Each blocks the **next** generation run until applied or
explicitly rejected.

| # | Finding | Root cause | Recurrence | Owning file | Concrete proposed edit |
|---|---|---|---|---|---|
| **R3-S1** | `bunpou.md`'s new 問題8 rule is **under-scoped**: it caps *free co-arguments of the final predicate* at one, so it cannot see the argument-vs-**adjunct-clause** case. 問題8-45 is exactly that shape — `[申請書に不備が→あった場合は]` (a は-marked conditional clause, an ADJUNCT, not a co-argument) and `[受け付けを]` (the one free co-argument) are both freely-orderable pre-predicate units. The rule counts 1 and passes; the actual uniqueness rests on the 解説's heaviness/topic-position argument, which no rule licenses. **This is the same structural shape round 2 declared fatal for 43 and 47** ("*[adjunct chunk] + [を-object] + [predicate]*, and Japanese does not fix the order of an adjunct against an object of the same verb") and then exempted for 45 ad hoc | `RULE-UNENFORCEABLE` — the rule exists, is specific, and is measurable, but measures the wrong quantity, so a compliant item can still be non-unique | **≥2 of 14 — systemic.** Scanned every paper's 問題8 for `[case-marked adjunct or adjunct CLAUSE] + [free を-object] + [predicate]`: `20260819_1` 問題8-45; `20260810_2` 問題8-45 (already on round 2's list). Official 7/2025 + 12/2025's ten 問題8 items contain **zero** instances — all are single modification/quotative chains | `.agents/question-authoring/references/bunpou.md` §"At most ONE card may be a free co-argument of the final predicate" | **Rename and re-scope the rule to what it must count: "At most ONE card may be a FREELY-ORDERABLE PRE-PREDICATE UNIT."** Replace the sentence "at most ONE card may be a free co-argument of the final predicate" with: **「最終述語の前に来るカード（塊）のうち、位置が構造的に固定されていないものは1つまで。共項か付加詞かは問わない——条件節・時の節・理由節など、述語に係る従属節も『自由な単位』に数える。位置を固定できる源は (1) 連体修飾の主要部、(2) 引用の「と」、(3) 下位範疇化された助詞、(4) 半分ずつを語彙的に順序づける呼応テンプレート の四つだけであり、"重い前置きが三つ並ぶと崩れる" のような処理負荷・自然さの議論は根拠にならない。自由な単位が二つ残るなら、片方を下線の前の文中へ移すか、主要部が隣接を強制するカードに差し替えて切り直す。」** Then add 45 by name as the worked example of the case the previous wording missed. **Founding-case check before commit:** applied to `20260819_1` 問題8-45 the new wording must FAIL the item as constructed (2 free units) where the old wording passed it (1 free co-argument); applied to 43/44/46/47 it must still pass (0/1/0/1 free units). |
| **R3-S2** | The 問題8 uniqueness proof is **not machine-decidable and is not required to be human-audited either.** `verify_scramble` returns `RESULT: UNDECIDED` on all five items by design and says so; `make check` reads none of it. So the only thing standing between a 問題8 item and two ★ answers is a reviewer voluntarily walking 24 permutations — which is exactly what round 1 did not do (it passed 43 and 47) | `GATE-BLIND` for the auditable half: nothing records that the 24-permutation walk happened, or its result | 3 of 14 papers shipped a non-unique 問題8 item (`20260810_2`-45, `20260819_1`-43 and -47 pre-fix) | `tools/verify_scramble.py` + `.agents/exam-qa-review/SKILL.md` §3 問題8 | **Make the tool emit the free-unit count, which IS string-decidable from the cards.** Add `free_unit_count(item)`: for each card, decide whether its position is fixed by one of the four licensed sources (`RENTAI_HEAD_CARD`, `QUOTATIVE_CARD`, a subcategorising particle tail matched against the partner card's head, or a 呼応 pair both of whose halves are named in the 解説); print `FREE UNITS: n` and **FAIL at n ≥ 2**. Run before commit over all 14 papers and name every id that moves; expected FAILs are `20260810_2`-45 and (pre-fix) `20260819_1`-43/-47. This does not decide uniqueness — it decides the one property that has caused every non-unique item on disk. |
| **R3-S3** | **Two items in one 聴解 section decide on the same axis.** 問題2-1番's deciding fact is 「実は、一人、卵が食べられない者がいまして」 and 問題2-3番's is 「今年入った人の中に、辛いものが食べられない人と、魚が苦手な人がいて」 — both turn on *a diner who cannot eat something*, three items apart, and 2-3番's keyed option prints the same lexical frame (「食べられない物がある人もたのめること」). The `構成表` cannot see it (different 場面, different 正解, different 質問型), the theme tags actively hide it (食 vs 働き方), and the drawn scenarios do not cause it — `レストランでの予約変更とアレルギー対応` was drawn with the allergy in it, but `職場:歓迎会の店選び` carries no dietary constraint at all; the author added one | `RULE-MISSING` — no rule constrains the *deciding axis*. `exam-qa-review` §5 fails "the same errand" and "the same subject"; these are neither. `choukai-items.md`'s 問題2 quotas count 質問型 and 消去方法, never the discriminating fact | 2 of 14 by a scan of the 構成表 決め手 columns (`20260819_1` 問題2-1番/2-3番; `20260817_2` 問題1 where 「割り当て」 carried 4 rows) — the shape recurs whenever a quota table counts labels rather than facts | `.agents/question-authoring/references/choukai-items.md` §問題2 構成表 + `.agents/exam-qa-review/SKILL.md` §4 | **Add a `決め手の種類` column to the 問題2/問題1 構成表 and cap it at 2 rows per section**, with the vocabulary written as a closed list the way 消去方法 already is (e.g. `在庫・数量 / 時刻・日程 / 費用 / 規則・制度 / 身体・飲食の制約 / 場所・経路 / 人手`). Then add to `exam-qa-review` §4's bullet list: **「同じ大問の二項目が同じ決め手の種類で決まっていないか——場面・正解・質問型が違っても、決め手が同種なら受験者は同じ聞き取りを二度させられている。構成表の決め手列を縦に読むこと。」** Not gate-checkable (the taxonomy is a judgment), so it must be an authoring-time column, not a post-hoc check. |
| **R3-S4** | **No rule caps option-word reuse inside one 問題5**, and this paper keys 「わずかに」 at 問題5-21 while printing it as a distractor at 問題5-23. Round 2 rejected the observation on the correct ground that no rule exists. Measured against the archive: **0 of 5 official 問題5 sections (80 options) repeat an option word within the section** | `RULE-MISSING` + `GATE-BLIND` (string-decidable, trivially) | 1 of 14 by a scan of every paper's 問題5 option sets; low frequency, but zero-tolerance in the archive | `.agents/question-authoring/references/moji-goi.md` §問題5 + `tools/check_consistency.py` | **moji-goi.md §問題5:** 「一つの問題5の中で、同じ語を二つの項目の選択肢に出さない。公式5回分80選択肢での重複は0件。鍵として出した語を別項目の妨害肢に再利用すると、21を確信した受験者に23の消去情報を与えてしまう。」 **Gate:** `check_mondai5_option_reuse()` — collect the 20 options of 問題5, FAIL on any word appearing twice. **Founding-case measurement to paste into the docstring:** `20260819_1: 「わずかに」×2 (問21 key, 問23 distractor)`; re-run over all 14 papers and name every id that gains a line before committing, so the new rule cannot quietly re-classify shipped work. |

---

## 6. Claims relayed to this round — verified, one by one

| Claim | Verdict | Evidence |
|---|---|---|
| 問題8-43 order `3→4→2→1`, ★=2, **0** free co-arguments | **TRUE**, independently derived over 24 orderings | §3 |
| 問題8-44 unchanged, **1** free co-argument | **TRUE** | 「受け継ぐ人が」 is いなかった's が-subject; 「あの技術を」 is inside the 連体修飾 clause |
| 問題8-45 unchanged, **1** free co-argument | **TRUE as counted, MISLEADING as a safety argument** | The count is right; it is the wrong quantity — the conditional clause is a second free *unit*. See R3-S1. The item still stands |
| 問題8-46 unchanged, **0** free co-arguments | **TRUE under the fix pass's definition** ("free" = not fixed by a structural source). 「心細いものは」 *is* ない's only co-argument but is fixed to it by the は-predicate requirement, and 「ときほど」 by the 呼応 template | — |
| 問題8-47 order `4→3→2→1`, ★=2, **1** free co-argument | **TRUE** | — |
| The illegal 「を→他動詞→隣接」 leg was removed from 43/44/45/47 and each replaced with a leg valid *for that item* | **TRUE**, and each replacement was judged on its merits, not on the fix pass's word | `grep 他動詞を要求` = 0 hits. No wrong-but-different argument found. 44's replacement explicitly disclaims transitivity in its own text |
| `illegal_legs()`'s third detector is anchored on 「他動詞」 rather than a window, because the proposed window form false-fired on 45's が-existence and 46's は-predicate legs | **TRUE and sound engineering, not fitting to founding cases.** Executed the shipped predicate on both shipped legs: **0 fires each**, as claimed. Executed it on the three reconstructed pre-fix legs: **fires on all three**, with the differentiated 連体修飾 message on 44 | The anchor is the one token that distinguishes an invalid transitivity claim from the legal 「〜を要求し…塊になる」 wording that が-existence, は-predicate and 形式名詞 legs all share. It is a principled anchor |
| "It fires on 44 with a differentiated message rather than exempting 連体修飾" | **FALSE for the shipped paper.** `make verify-scramble 20260819_1` reports `ARTIFACT: ok ×5` and **zero** leg fires: the fix pass removed the 「他動詞を要求」 wording from 44 as well, so the detector fires on **no item on disk**. The differentiated branch is real code and does fire — on the reconstructed 44 pre-fix leg (verified) | Not a defect: the detector's founding cases are the pre-fix strings, and §6.5's requirement is that it be *run* against them, which this round did |
| It cannot fire on `20260810_2` 問題8-45 because that 解説 prints no proof at all | **TRUE, and correctly documented rather than papered over.** `make verify-scramble 20260810_2` → `ARTIFACT: MISSING` on all five items, so `missing_proof()` already fails it. The module docstring states this in full | The engineering is sound; the *construction* half of that class remains human, which is R3-S1/R3-S2 |
| `check_key_grammar_exposure` reads the form via `sample_items.grammar_form_tokens()` | **FALSE in detail, TRUE in substance.** It uses `grammar_form_parts()` — the ordered chunks, matched as one discontinuous skeleton inside a single sentence — because the token set cannot express a *frame* (`理由説明(〜のは…からだ)` is 「のは…からだ」, not the token 「からだ」). The docstring says so | Substantively correct; the relayed name was wrong |
| Copula normalisation (`からだ`≡`からである`) | **TRUE**, one `replace("である","だ")` covering all three named equivalences | Verified: without it the pre-fix pair scores 0, with it 2 |
| Pre-fix revision FAILs; shipped reads ok; `20260810_1` is the only id that gains a line | **ALL TRUE** | Pre-fix reconstruction → 2 hits (> `KEY_EXPOSURE_MAX` 1). Shipped → `ok`. 14-paper re-run: only `20260810_1` gains `問題8 target「一方」×3`, already grandfathered |
| The 46-of-70 silent-draw class is genuinely closed | **TRUE** | All 41 distinct `grammar_p8` entries in the ledger now yield ≥1 usable chunk; **0** yield nothing. Residual risk is over-firing (`〜ながら…する` etc. end in the very common 「する」), which is the opposite failure and currently produces no spurious line on any paper |
| R2-F5: both cleft-reason sentences re-worded, count 2 → 0 | **TRUE**, and stronger than reported: **all 15** 問題7/9 keyed forms occur **0 times** in the shipped 問題10–14 prose | — |
| The `dokkai.md` thirteen-final-sentence column and closing-move shapes still hold after the rewrite | **TRUE, verified by re-reading the closings, not by `make check`.** Neither re-worded sentence is its passage's final sentence — 問題10(1) still closes 「見た目の乱れを指摘する声は今も届くが、…三倍に上る。」 (反論応答: 「〜という批判もあるが、実際には〜」 — the template *exactly*), 問題11(3) still closes 「…母が誰に向けて書いたのかは、今なら分かる気がする。」 (随筆). Independently re-labelled all **11 essay surfaces** from the shipped last two sentences: 条件提示 2 (問9, 問11(2)) / 反論応答 2 (問10(1), 問11(1)) / 意外な観察 2 (問10(2), 問11(4)) / 説明 2 (問10(4), 問13) / 主張 2 (問10(5), 問12) / 随筆 1 (問11(3)) = 11, **≤2 everywhere**. Normalised each final to its template and read the column: no template appears more than twice (the 「A ではなく B」 family is 問11(1) 「…技術より、…段取りである」 and 問12A 「…話ではない。…話である」 = 2, at the cap) | 問題12 A/B counted as ONE surface, which is `dokkai.md`'s own accounting ("問9, 問10×5, 問11×4, 問12, 問13") |
| Observation 7 ruled 意外な観察, keeping 説明 at 2 | **RULING ACCEPTED — and it is a definitional argument, not label-shopping.** `dokkai.md` defines 意外な観察 as "an unexpected fact, then its cause". 問題11(4) marks the unexpected fact with a 逆接 and a quantified surprise (「**ところが**、①看板を高く掲げた家ほど短命だった」…「二倍近くに上っていた」) and the closing supplies the cause (「行事として約束された親しさは、参加しない自由を住人から取り上げてしまう」). It is structurally the same move as 問題10(2), the other 意外な観察. 説明's two (問10(4), 問13) both explain a mechanism with **no** unexpected-fact frame. The distinction survives inspection | — |
| Observations 1, 2, 5 applied | **ALL TRUE.** (1) `notes` now says eleven and reports the reframe family as a hand count of 2 with the proxy 0 disclaimed. (2) 構成表 問題3 now prints 306/334/311/333/337 = `p3_talk_chars` exactly. (5) 「無理がある」 now occurs **1×** in the whole booklet body (問題9-50's key only); 問題13-69's key reads 「一つの言葉でまとめて呼ぶことはできない」, still the passage's thesis, still a paraphrase, option lengths 32/33/29/29 → max/min 1.14 | — |
| Observations 3, 4, 6, 8 rejected | **3 — rejection CORRECT as to the rule, but the archive says otherwise; re-filed as R3-S4** with the measurement (0 of 5 official sections repeat). **4 — rejection ACCEPTED**: 「に越したことはない」(38) and 「ことはない」(41) are two distinct Shin Kanzen headwords sharing a tail, the shipped constant is `P7_FORM_REUSE_MAX = 2`, and `bunpou.md` forbids repairing this by shortening the n-gram; 「ばかりに」(32,35) and 「うちに」(37,39) are distractor-only. **6 — rejection ACCEPTED**: 「話が切れる」 is not attested (the idiom is 話が途切れる), so it is a learner-plausible break, not a second correct answer; the key 「しょうゆが切れて」 is canonical. **8 — rejection ACCEPTED**: neither 問題1-4 nor 問題8-43 is a topic-table surface, and 食 runs 4 listening surfaces against a cap of 5 | — |
| `聴解.md` / `聴解スクリプト.txt` / `聴解.mp3` untouched since round 1 | **FALSE for `聴解.md`, TRUE for the other two.** `聴解.md` = `81f1b7846a31` in rounds 1 and 2, **`0ccc5b80910c` now** (mtime 15:57:58, after round 2's 13:40 report) — the observation-2 構成表 fix, which round 2's own §8.6 records and which this round re-derived from `p3_talk_chars`. **No item, option, 例, key or 解説 in `聴解.md` moved**: all 30 keys ≡ `answer_positions`, all 4 例 announced numbers ≡ the marksheet, and the whole booklet-vs-script grounding was re-read here from scratch. `聴解スクリプト.txt` = `b856e2fc0de8` (unchanged since round 1, and `聴解_チャプター.json`'s `script_sha` matches), `聴解.mp3` mtime 11:22:19 > script 11:19:47 | The relayed claim was stale, not the paper |

---

## 7. Observations (calibration; no rule breached, nothing to repair on this paper)

1. **問題4-16 is the paper's easiest item.** Key 煮る against 焼く/蒸す/炒める: 蒸す
   and 炒める are N2-band, but 焼く is N5 and 煮る is N3/N4-band, and the item is
   decided by だし汁 — world knowledge, not vocabulary level. It does **not** meet
   `exam-qa-review` §2.5's stated TOO_EASY test (the set is not four basic
   N4–N5 items, and 煮る is a `pools.json` entry, i.e. harvested from the N2
   volumes; 日本語総まとめ N2 語彙 does headline everyday verbs of exactly this
   register — ける, 甘える, 高くつく, 召し上がる at pp. 26–28, and 「人手が不足
   している」 at p. 28, which independently confirms 問題4-18's key). Recorded so
   the next blueprint prefers a set whose four members are all N2.
2. **「わずかに」 is the key at 問題5-21 and a distractor at 問題5-23** — re-filed as
   R3-S4 with the archive measurement rather than left as a bare note.
3. **Two of the fifteen 問題6 wrong sentences sit closer to the boundary than the
   other thirteen**: 27-2 「そこで話が切れてしまった」 and 29-4 「持っていた地図を
   何度も吟味した」. Neither is a second attested collocation (話が途切れる is the
   idiom; 吟味 requires evaluating quality/merit, not reading a map for
   information while lost), and both keys are canonical, so both items stand.
   Recorded for calibration only, as round 2 asked for 27-2.
4. **The 問題4 例 stimulus template recurs across papers in the same slot.**
   `20260813_1` 「このデータ、明日の朝までにまとめておいてもらえる?」,
   `20260817_3` 「この資料、明日の朝までにコピーしといてくれる?」, this paper
   「この資料、会議までに間に合いそう?」 — one skeleton 「この＋[事務用名詞]、[期限]
   まで(に)…?」 three times. Measured similarity is **0.31–0.45**, i.e. a shared
   template, **not** near-verbatim (the automatic-fail bar is a few edited
   characters, ~0.9+), and the speech acts differ (request / request / status
   query). `topics.json` already records the 2-back half of this. No rule caps
   例 template reuse across tests; proposing one is out of proportion to a
   non-scored 例.
5. **問題2-9's target 形容動詞 is a 4-kanji metalinguistic term**, with the 2×2
   applied to 形容 and 動詞 held fixed. `moji-goi.md` §問題2 states the grid over
   "each kanji of a correct 2-kanji compound", so a fixed tail is an extension of
   the letter of the rule, not a breach of it; all four options read けいようどうし
   and all six glyphs are 常用 (gate ok). Official 問題2 targets are everyday words;
   this one is not. Recorded.
6. **問題4-1番's stimulus opens in announcement register** (「診察券をお持ちで
   ない方は、初めての方窓口へ。」) but is saved by the deictic 「**あちら**でご記入を
   お願いします」, which puts a specific addressee in front of the speaker. It is
   therefore not the automatic-fail shape (「a 即時応答 prompt with no defined
   responder」 — the 火災報知器 case). It is the drawn `quick_response` string
   verbatim, so any repair belongs in the pool, not the paper.
7. **問題9 and 問題11(1) are both disaster-domain** (非常持ち出し袋 / 災害の第一報).
   Different subjects, no shared fact, number or condition; `topics.json`
   already flags the adjacency. Confirmed by reading both passages.
8. **The 「A ではなく B」 reframe family sits exactly at `dokkai.md`'s cap of 2**
   (問題11(1), 問題12A). The gate's marker-family proxy prints 0 for it, which
   settles nothing — this is a hand count, and one more instance would breach.

---

## 8. Coverage statement

| Step | Ran on | Result |
|---|---|---|
| 0 Blind solve | `qa/20260819_1/keyless.md` (1088 lines), all 101 items + 4 例, before any key was opened | 101/101, 0 discrepancies |
| 1 Key-by-key proof | all 101 items, `言語知識・読解.md` + `聴解.md` + `聴解スクリプト.txt` | every key restates a quoted deciding line (§3) |
| 2 Distractor elimination | all 101 items × 3 (or 2) wrong options | no "the key fits slightly better" case; the two closest are §7-3 |
| 2b Plausibility | 問題1–6 functional-category columns; every 聴解問題1–3 distractor traced to its script line | all 問題4/5/6 sets share one functional category; **every** 聴解1–3 distractor has a raising line (§3) |
| 2.5 Level band | all 問題1–6 keys against Shin Kanzen / 総まとめ N2 (incl. a direct read of `refs/Soumatome/nihongo-soumatome-n2-goi.pdf` pp. 4–9, 26–28); 問題7–9 against `level_band_grammar.txt` via the gate | 0 TOO_HARD, 0 TOO_EASY; 問題4-16 noted (§7-1) |
| 3 Mechanical reads | 問題7 三数値 (41.2 / 3 / 42), 問題8 5 items × 24 orderings **by hand**, 問題9 categories + 689 chars, 注N 32 1-to-1, 中略 4, ruby 0, marked spans 5, 読解 length/predictability rates, 問題5 substitution, 問題2 2×2 ×5, 問題1 2×2 + okurigana, 問題3 affixes, keyed-form exposure 0/15 | all pass |
| 4 聴解 structure | セクション構成表 read as **columns** and re-derived from the script (消去方法 9 tokens × 2 rows; 質問型 どうして3/どのように2/一番1; 問題3 種別 2+4; talk chars re-measured); first and last spoken line of every item; 例 announced-number ↔ marksheet ↔ dialogue; keigo direction ×11 | table is accurate; R3-S3 is the one thing the table cannot see |
| 5 Topic table | all 13 読解 + all 31 聴解 surfaces, from the **shipped** text, vs `20260818_1` and `20260817_3`; themes re-tagged from the passages; closing moves re-labelled from the last two sentences | headline sets: ∩`20260818_1` = **∅**; ∩`20260817_3` = **{防災}** = 1 (rule 4's single allowance). 13 読解 surfaces, 13 distinct themes. Listening max 食 = 4 (cap 5). No subject twice. 問題14 shares no number/condition with any 聴解 item |
| 6 Provenance | `test_spec.json` ↔ `logs/ledger.json` field-for-field; all 22 draws → `pools.json`; all 11 `quick_response` → script; all 21 `listening_scenarios` → an authored item (0 unused, 0 unrecorded substitutions); `answer_positions` ↔ 101 keys; spec themes ↔ `topics.json` themes | identical. Seed records round 1's four `--reroll-one` calls and nothing since (round 2 ran no reroll, as claimed). `pools_sha` `aadf23081392` is a real sha, not date-shaped. Ledger `items` == spec `items` (deep equality) |
| 6.5 Root cause | 4 findings (§5), each with a founding-case measurement and a concrete edit | — |
| `notes` verification | all 25 quoted strings in `logs/topics.json`'s `20260819_1` `notes` grepped against the paper | **0 claims quote a string that is not there.** 15 non-matches are all correct: meta/template text, ellipsis-elided quotes that resolve (「…技術より、…段取りである」 ✓, 「…話ではない。…話である」 ✓, 「それでも市は刈り残しを続けている。…ためである。」 ✓, 「開く前は、…のだろうと身構えた。」 ✓), and strings the note asserts are **absent** and which are absent (みどり市民ホール, 同じ名前で呼んできたことに無理がある, 確認します, both pre-fix cleft sentences). All five fields (`surfaces`/`themes`/`shapes`/`closing_moves`/`notes`) present and mutually consistent |
| Cross-test apparatus | 例 blocks compared by **similarity** against all 13 other papers; longest common run against all 31 official booklets and every `imported-*` | max 例 similarity **0.45** (§7-4). All ≥20-char runs shared with `refs/` are the format-fixed 問題 instruction headings, which `jlpt-exam-structure` requires to be identical. **No passage, dialogue, 例, stem or option is shared** |
| Artifact freshness | mtimes + stamped shas | `聴解.mp3` 11:22:19 > `聴解スクリプト.txt` 11:19:47 ✓; `聴解_チャプター.json` `script_sha` = `b856e2fc0de8` = the script ✓; all three HTML 16:08 > their Markdown 15:57 / 16:05 ✓; gate `built HTML matches the Markdown it stamps` ok |
| Sources still | shas + mtimes read before the pass and again before writing this file | unmoved; `keyless.md` rebuilt after the pass and byte-identical |

### `make check` WARN resolution

`make check` exit 0, "All checks passed (30 skipped), 138 warning(s)" — the same
total as rounds 1 and 2, so no verdict moved anywhere on disk. **No WARN or FAIL
line has `20260819_1` as its subject.** Three WARN lines mention the id:

| WARN line | Resolution |
|---|---|
| `every stamped spec's pools_sha matches pools.json` | The actual mismatch is `20260818_1`'s stamp (`d24928db9883` vs current `aadf23081392`). The line names `20260819_1` only to record that its sha was stamped on a REROLL, so it certifies that redraw's pool. The check's own docstring names this as expected after any pool repair. **Not a defect.** |
| `20260807_1` / `20260810_1` / `20260817_2`: 問題1 訓読み mix | Cites `qa-report-20260819_1 F3` as the source of the rule. Subjects are three grandfathered papers; this paper measures **2 of 5, cap 2 — ok**. |
| `20260810_1` / `20260814_1`: no 問題7 form printed in more than 2 items' options | Cites `qa-report-20260819_1 F2`. Subjects are other papers; this paper is **ok**. |

This paper's own block: **96 `ok`, 4 `skip`, 0 WARN, 0 FAIL.** The four skips:

| skip | Resolution |
|---|---|
| `詳細解説.json options match the booklet` | Correct ordering — `make model-answer` is the post-QA step (`AGENTS.md` §5). Not a defect. |
| `詳細解説.<lang>.json translations` | Same. |
| `no two drawn surfaces share one errand key` (0 keyed draws) | No drawn entry in this spec carries an errand key, so there is nothing to compare — the check's own docstring says so. Verified independently: I intersected this paper's draws against `20260818_1`'s and `20260817_3`'s in **all eight** item categories after folding okurigana/kana tails and 類型 wrappers → **zero overlap in every category**. |
| `no drawn errand repeats inside its own cooldown window` (0 keyed draws) | Same, same verification. |

### Topic table (this paper vs the two before)

| surface | 20260819_1 | 20260818_1 | 20260817_3 | verdict |
|---|---|---|---|---|
| 問題9 (headline) | 防災 — 非常持ち出し袋の重さ | デジタル化 | 消費・経済 | — |
| 問題12 (headline) | 働き方 — 在宅勤務の評価 | 交通 | 環境 | — |
| 問題13 (headline) | 文化・伝統 — 方言の記録と継承 | 住まい | 医療・福祉 | — |
| 問題14 (headline) | 旅行・観光 — 共通観覧券 | 行政・手続き | スポーツ・余暇 | — |
| 聴解問題5-1番 (headline) | 食 — カフェの品書き | 地域活性化 | 人間関係 | — |
| 聴解問題5-2番 (headline) | 教育 — 見学会の催し選び | メディア・情報 | **防災** | the one allowed 2-back repeat |
| **headline set ∩** | — | **∅** (rule 4 zero-tolerance ✓) | **{防災} = 1** (cap 1 ✓) | pass |
| 読解 13 surfaces | 防災/環境/科学・技術/消費・経済/睡眠・健康/子育て・家族/メディア・情報/交通/医療・福祉/住まい/働き方/文化・伝統/旅行・観光 | — | — | **13 distinct ✓** |
| 聴解 theme max | 食 4 (問2-例, 問2-1番, 問3-1番, 問5-1番) | — | — | cap 5 ✓ |
| in-paper subject repeat | none. Closest: 問題9 / 問題11(1) both disaster-domain (§7-7); 問題2-1番 / 問題2-3番 share a deciding **axis**, not a subject (R3-S3) | — | — | pass |
| 問題14 ↔ 聴解 | 800/1,200/600円, 月・火・水の休館日, 十名以上・三日前, 特別展の別途800円 — **none appears in the script**; 問題14 names no aquarium (聴解問題3-例) and no reserved seat (問題4-11番) | — | — | pass |
| 読解 closing moves | 条件提示 2 / 反論応答 2 / 意外な観察 2 / 説明 2 / 主張 2 / 随筆 1 = 11 essay surfaces | — | — | ≤2 each ✓; no template >2 ✓ |
| keys inheriting the closing | no "human/attitude vs strawman" cluster: the 20 読解 keys split across mechanism (55, 68), datum (52, 63), reframe (58, 62, 69), procedure (60, 66), and information retrieval (54, 70, 71) | — | — | pass |

---

## 9. Skips, stated explicitly

- **`聴解.mp3` was NOT listened to.** This reviewer has no audio playback
  capability. Everything the audio can carry was verified from the text and the
  stamps instead: `聴解_チャプター.json`'s `script_sha` = `b856e2fc0de8` = the
  shipped `聴解スクリプト.txt` (so the MP3 speaks the shipped text, not a
  superseded one), `pacing_sha` = `d241e428f28f`, mtime 11:22:19 > the script's
  11:19:47, and the gate's `聴解 narration gender matches SPEAKER_MAP's voice`
  and `聴解 item speaker pairs cast distinguishable voices` are both ok. **What
  remains unverified is only what an ear can hear** — actual voice quality,
  mispronunciation of a rare reading, pause length. Rounds 1 and 2 report the
  same limitation, so **no round has listened to this MP3**.
- **No page-by-page read of the Shin Kanzen scans.** `refs/Soumatome/
  nihongo-soumatome-n2-goi.pdf` was read directly (pp. 4–9 TOC/format, 26–28
  第1週問題4 + 第2週1日目) to calibrate the register question in §7-1 and to
  confirm 問題4-18's key; the Shin Kanzen volumes were consulted only through
  `pools.json` provenance and the gate. The scans have no text layer, so an
  exhaustive per-key lookup is not feasible in one pass; §2.5's verdicts are
  judgment calls made against that partial evidence, and are stated as such.
- **No fix was applied.** The reviewer proposes; §5's four edits are for
  whoever touches the skills next, and none of them changes this paper.
- **`make model-answer` was not run and must not be** until this PASS is
  recorded — it is the post-QA final step (`AGENTS.md` §5). `詳細解説.json` does
  not exist yet, which is why two gate lines skip.

---

## 10. What this verdict means for the loop

`QA: PASS`. Steps 0–6 ran on all 101 items and the four 例; zero paper findings
remain open. The paper may be committed and served, and `make model-answer
20260819_1` is now the correct next command.

The four §5 findings are **skill/gate findings and block the next generation
run**, not this paper (`exam-qa-review` §6.5, "Effect on the loop"). R3-S1 is
the one that matters most: the rule the round-2 fix pass wrote to stop 43 and 47
from recurring counts the wrong quantity, and 問題8-45 — an item that ships
sound — is the proof, because it satisfies the rule while still having two
freely-orderable pre-predicate units. The next 45-shaped item will not be as
lucky, and the rule as written will pass it.

---

## 11. Root-cause disposition (appended 2026-08-20 by the disposition pass)

Written by a context that authored none of this paper and none of round 3.
Everything above this heading is untouched. `exam-qa-review` §6.5 "Effect on
the loop" requires each §5 finding to be **applied or explicitly rejected with a
reason** before the next generation run; all four are **applied**, two of them
with a stated partial scope.

**One of the four changed this paper's shipped content: R3-S1** (問題8-45
re-cut). R3-S4 changed one printed distractor. R3-S2 and R3-S3 changed no
printed content. `聴解スクリプト.txt` and `聴解.mp3` were not touched and
`make mp3` was **not** re-run.

| # | Disposition | What was done, and why |
|---|---|---|
| **R3-S1** | **APPLIED — and it found a real paper defect** | `bunpou.md`'s §"At most ONE card may be a free co-argument of the final predicate" is renamed and re-scoped to §"At most ONE card may be a **FREELY-ORDERABLE PRE-PREDICATE UNIT**", carrying the report's Japanese wording verbatim (共項か付加詞かは問わない; the four licensed sources; 「重い前置きが三つ並ぶと崩れる」 is explicitly not a reason). 問題8-45 is written in as the worked example. **The founding-case check the report asked for was run and it fails 45 as constructed**, exactly as predicted — see the two rows below. |
| **R3-S2** | **APPLIED, with the threshold enforced only from the rule's own date** | `free_unit_count()` added to `tools/verify_scramble.py`: it reads the word order off the 解説's own `カード(n)→…` line, merges each adjacent pair whose adjacency is forced by one of `bunpou.md`'s four sources (plus bound tails and subordinate-clause absorption), prints `FREE UNITS: n`, and FAILs at n ≥ 2. Run over all 14 papers; measurements and the grandfather list are below. |
| **R3-S3** | **APPLIED for 問題1 and 問題2; this paper NOT changed, deliberately** | `choukai-items.md` gains §決め手の種類 — a closed nine-token list and a ≤2-rows-per-問題 cap, written the way §消去方法 already is — and `exam-qa-review` §4 gains the 「決め手列を縦に読むこと」 bullet verbatim from the report. The column was filled in on this paper's 問題1/問題2 構成表 with its tallies. |
| **R3-S4** | **APPLIED, and this paper repaired** | `moji-goi.md` §問題5 gains the rule; `check_mondai5_option_reuse()` added to `tools/check_consistency.py`. 問題5-23's distractor 「わずかに」 → 「多少」. |

### R3-S1 — the founding-case check, and the decision it forced

Applied to the paper's five 問題8 items, the re-scoped wording measures:

| item | pre-predicate blocks | free units | old rule (co-arguments) | verdict |
|---|---|---|---|---|
| 43 | `[長年の経験に＋基づいて]` ｜ `[決めている＋そうだ]` | **1** | 0 | passes |
| 44 | `[つまり]` ｜ `[あの技術を＋受け継ぐ人が]` ｜ `[身内にいなかった]` | **1** (つまり is fixed clause-initial) | 1 | passes |
| **45 (as shipped through round 3)** | `[申請書に不備が＋あった場合は]` ｜ `[受け付けを]` ｜ `[断らねばならない]` | **2** | 1 | **FAILS** |
| 46 | `[体を壊した＋ときほど＋心細いものは＋ない]` | **0** | 0 | passes |
| 47 | `[味だけでなく＋皿の色や明るさも]` ｜ `[変えている＋からだ]` | **1** | 1 | passes |

The report predicted `0/1/-/0/1`; 43 measures **1**, not 0, and the difference
is definitional rather than a disagreement: `[長年の経験に基づいて]` is not a
co-argument (the を-object is in the stem) but it *is* a pre-predicate unit. With
one unit there is nothing to permute it against, so 1 and 0 are the same verdict
— which is why the rule's bar is 2, not 1.

**45 was ruled a PAPER DEFECT and re-cut.** The honest reading the report asked
for: the rival `受け付けを → 申請書に不備が → あった場合は → 断らねばならない`
is grammatical — round 3 itself concedes 「文法的だが idiomatic ではない」 — and
it keys ★=2 against the key's ★=4. Long-distance scrambling of a matrix object
over a は-marked conditional clause is ordinary Japanese; the only thing standing
between the two readings was the 解説's heaviness/topic-position argument, and
that is precisely the class of argument the re-scoped rule refuses. Weakening the
rule to fit the item was the one repair not available, and calling it a
proof-only defect would have required accepting the heaviness argument as a
licensing source. **So round 3's PASS was granted on an item that does not hold
under the rule round 3 itself proposed** — stated loudly, as asked.

The repair is `bunpou.md`'s own ("cards only — the drawn form is the contract"):

```
was:  **45** 窓口の担当者は、＿＿ ＿＿ ★ ＿＿。
       1. 申請書に不備が  2. あった場合は  3. 断らねばならない  4. 受け付けを
       申請書に不備が(1)→あった場合は(2)→**受け付けを(4)**→断らねばならない(3)

is:   **45** 窓口の担当者は、＿＿ ＿＿ ★ ＿＿。
       1. 不備が  2. 課長に報告せねばならない  3. 申請書の  4. 見つかった場合は
       申請書の(3)→不備が(1)→**見つかった場合は(4)**→課長に報告せねばならない(2)
```

窓口の担当者は、申請書の不備が見つかった場合は課長に報告せねばならない。
The を-object is folded into the predicate card, and the three remaining cards
form ONE chained unit: 「申請書の」's の demands an immediately following noun,
and 「不備が」 is the subject of 「見つかった」 *inside* the 場合 clause, so it
cannot leave it. **FREE UNITS: 1.** The 24-permutation walk was redone by hand:
only 「課長に報告せねばならない」 can close the sentence (の-止まり／が-止まり／
「〜場合は」 cannot), which leaves six orderings, and the five rivals die on two
nameable facts — 「申請書の課長」 has no referent, and 報告する takes an animate
agent so 「不備が」 cannot be its subject. Drawn form `義務当然(〜ねばならない)`
unchanged, key still 4, `answer_positions` untouched, **no reroll**. Option sum
27 JP chars, assembled 36 — both inside the gate. `register`: still the paper's
single formal/institutional 問題8 item.

### R3-S2 — the measurement over all 14 papers, and why 13 are grandfathered

Founding cases, all executed before the check was accepted (its docstring names
them): shipped-45 → **2** (FAIL); `20260810_2`-45 → **2** (FAIL); the
reconstructed pre-round-2 `20260819_1`-43 and -47, with 「畑に出る日を」/
「客の感じ方を」 still on cards → **2** each (FAIL); re-cut 45 → **1**.

The 14-paper run then found the class far commoner than round 3's scan reported:
**33 of the 65 items on the 13 earlier papers read n ≥ 2**, against round 3's
estimate of one. The gap is real and is not tuned away — round 3 scanned only for
*[adjunct clause] + [free を-object]*, while the rule it proposed covers **any**
two free units, so two bare co-argument NPs (`20260813_1` 問題8-44:
「自分の言動には」/「常に責任を」) are the same defect and were never counted.

| id | items at n ≥ 2 |
|---|---|
| 20260807_1 | none |
| 20260810_1 | 44, 46, 47 |
| 20260810_2 | 43, **45**, 46, 47 |
| 20260811_1 | 43, 44, 45, 47 |
| 20260812_1 | 47 |
| 20260812_2 | 44, 46, 47 |
| 20260813_1 | 43, 44, 45, 46, 47 |
| 20260813_2 | 43, 47 |
| 20260814_1 | 43, 45, 46 |
| 20260817_1 | 43, 46, 47 |
| 20260817_2 | 43, 44, 45 |
| 20260817_3 | none |
| 20260818_1 | 43, 47 |
| **20260819_1** | **none** (45 was 2 before the re-cut) |

All 13 earlier ids are in `FREE_UNIT_GRANDFATHERED` — **by name and by date**,
because the rule did not exist when they were authored (it landed 2026-08-19 in
its co-argument form and was re-scoped 2026-08-20). They print their measurement
and do not affect the exit code, exactly as `SETTING_ADJACENCY_GRANDFATHERED` and
`MOJI_GLYPH_GRANDFATHERED` do; an id leaves the set the moment its 問題8 is
re-cut. `20260810_2` still exits non-zero on `missing_proof()`, unchanged.

**Stated limitation, in the docstring and here:** the merger works on adjacent
pairs of the KEYED order, so a swap blocked by a NON-adjacent lexical requirement
(`20260818_1`-43: 「限らず」 wants a bare 「に」, which kills the rival that fronts
「観光客にも」) still reads n=2. That is not a mis-measurement of the *rule* —
`bunpou.md` counts units whose position is fixed by one of four sources, and
nothing fixes 「観光客にも」 — but it does mean n ≥ 2 is a construction-rule
breach, not a proof that two ★ answers exist. n ≤ 1 is likewise not proof of
uniqueness: the tool still returns `UNDECIDED` and the 24-permutation walk is
still the reviewer's.

### R3-S3 — applied as a rule; this paper's 聴解 deliberately NOT changed

The `決め手の種類` column and its ≤2-row cap are in `choukai-items.md`, the QA
bullet is in `exam-qa-review` §4, and the column is filled in on this paper's
問題1/問題2 構成表. **Filled in, this paper measures:**

- 問題1 (6 rows): 連絡・情報の不足1 / 在庫・数量1 / 場所・経路1 / 費用・金額1 /
  設備・故障1 / 規則・制度1 — six rows, six tokens.
- 問題2 (7 rows): 在庫・数量2 (例, 5番) / **身体・飲食の制約2 (1番, 3番)** /
  時刻・日程2 (2番, 4番) / 場所・経路1 (6番).

**The call, made deliberately rather than by default: 問題2-1番 and 2-3番 are
NOT differentiated, and `make mp3` was not re-run.** The pair sits exactly ON
the cap the report itself proposed (2 rows, the same cap §消去方法 has always
used), and it is not alone there — 在庫・数量 and 時刻・日程 also sit at 2. A
tighter bound would have to be a cap of 1, which no measurement in the report
supports and which 7 rows against 9 tokens make nearly unsatisfiable. Rewriting a
deciding line to clear a bound the rule does not set would mean re-synthesising
the MP3 for a rule breach that does not exist. What the disposition does instead
is make it **visible and bounded**: the column now records the collision in the
paper's own 構成表, with the note that the next paper must treat
身体・飲食の制約 as spent for that 大問.

The report proposed the column for 問題1 **and** 問題2. It is added to both, but
note the asymmetry honestly: the 問題1 half of the finding (`20260817_2` 問題1,
「割り当て」×4) is an *elimination-device* over-cap and is already a FAIL under
`check_choukai_elimination_tokens()`'s closed vocabulary and `ELIMINATION_ROW_CAP`.
The new column adds the deciding-FACT axis there, which nothing measured before.

### R3-S4 — rule added, and this paper repaired

`moji-goi.md` §問題5 now states the rule with the archive measurement (0 repeats
in 80 official options), and `check_mondai5_option_reuse()` enforces it.
**Founding-case run before it was accepted:** on the pre-fix option sets it
prints `「わずかに」×2 (問21, 問23)` and FAILs; on the shipped sets it is `ok`.
Re-run over all 14 papers: **every other id is already clean at 20 distinct
options**, so no id is grandfathered and the new rule re-classifies no shipped
work.

**This paper WAS repaired**, because the repair costs one distractor and the
archive is zero-tolerance: 問題5-23 option 1 「わずかに」 → 「多少」, which sits in
the same slot (a small-degree adverb against the key 「さらに」 = 前より程度が増す)
and the same functional category (`23: 程度の変化を表す副詞句 ×4`). **The key was
not touched** — 「わずかに」 at 問題5-21 is half of the drawn `paraphrase` entry
`うっすら(わずかに)`, so moving it would have un-tested the drawn item, and no
reroll was needed because a 問題5 distractor is authored, not drawn. 「多少」
occurs nowhere else in the paper.

### Verification run after every edit

`make autofix 20260819_1` (clean) → `make lint-draft 20260819_1`
(**ALL CHECKS CLEAN**) → `make booklet` + `make sheet` (both rebuilt from the
edited Markdown in the same change) → `make verify-scramble 20260819_1`
(**ARTIFACT ok ×5, PROOF LEG INVALID 0, FREE UNITS 1/1/1/0/1, exit 0**) →
`make check` (**exit 0, "All checks passed (30 skipped), 138 warning(s)"** — the
same warning total as rounds 1, 2 and 3, and **no WARN or FAIL line has
`20260819_1` as its subject**; the new `check_mondai5_option_reuse` prints `ok`
on all 14 papers). `make sample`, `make model-answer`,
`make scaffold-explanations` and every translation target were **not** run —
Stage 5 runs after this pass.

---

## 12. Post-round-3 verification finding — 問題8-46's uniqueness proof (2026-08-20)

An independent verification of the re-cut 問題8 items found a **proof-quality
defect at 問題8-46**, in exactly the class rounds 2 and 3 had just banned. Item,
cards, order and key are unaffected (★=1, matching `answer_positions`); only the
written proof was wrong.

### The defect

The 解説 excluded 46's one rival ordering — `1→2→3→4`, ★=3,
「心細いものは体を壊したときほどない」 — with

> 「心細いものは」の「は」は述語を要求し、四枚のうち述語は「ない」だけなので、
> ［心細いものは→ない］も塊になる

which is the R2-F3 leg with **は** in place of **を**. In that rival 「ない」 *is*
later in the clause, merely not adjacent, so the premise licenses the ordering it
was written to exclude. `illegal_legs()` could not see it: its third arm was
anchored on the token 「他動詞」, a choice its own comment justified by pointing at
a が-existence leg it called legal — **that leg was an instance of the class, not
an exception to it.**

### The repair — 解説 only

問題8-46's second 連結の制約 leg is replaced by the 呼応 template, a legal
adjacency source (bunpou.md source 4) that the 解説's own opening line already
named without deploying: 「AほどBはない」 orders both halves lexically, and the
reversed 「BはAほどない」 forces a gradable-comparative reading of 「ない」 that the
bare existential 「〜はない」 cannot carry, contradicting the sentence's superlative
sense. The last-slot proof's closing sentence now derives the single ordering from
that template instead of from the deleted 塊. **No particle-requires-an-adjacent-
predicate argument is printed anywhere on the paper.**

**Every other 解説 on the paper was scanned for the generalized leg** — the shape
「『X〈助詞〉』は…を要求し、…なので［X→Y］は塊になる」 for ANY particle, across 問題7–9,
読解 and 聴解. Six 「〜を要求」 legs remain and all six are legal, each a BOUND
element pointing backward at its own host or a 呼応 template: 43「基づいて」直前に
「に」名詞句 / 43「そうだ」直前に普通形 / 44「という」直前に普通形 / 45「の」直後に名詞 /
46「ときほど」直前に連体修飾述語 / 47「からだ」直前に普通形 + 47「だけでなく」→「も」.
**46 was the only instance.**

### Root cause, and the detector widening

| root cause | fix |
|---|---|
| `bunpou.md` stated the banned leg for 「を」/transitivity only, so it read as a fact about transitive verbs rather than about particles | The third illegal leg is restated for **any case or topic particle**, with 46 as the worked example, an explicit *"a particle constrains ORDER, never ADJACENCY"*, the 「の」 exception, and a **direction test** for telling this leg from a legal one (a bound element demanding a host 直前 is legal; a particle-final card demanding "whichever card is a predicate" is this leg) |
| `illegal_legs()`'s 他動詞 anchor is blind to every particle but 「を」 | **Widened and shipped.** New `PREDICATE_DEMAND_LEG` (`述語/動詞/用言/述部を要求…`) fires when the last-named card **ends in a case/topic particle**, the window does **not** say 直前, and an adjacency conclusion (塊/連続/隣接…) follows within 80 chars. The 他動詞 arm is kept verbatim so its four founding cases stay covered; overlapping matches report once |

**Founding-case run before the widening was accepted** (required by R2-F3's own
terms). It fires on **all five**: 問題8-46's pre-fix 「は」 leg, and the pre-fix
「を」 legs of 43, 44, 45 and 47 (44 still gets the softened *"conclusion holds,
reason does not"* message, per R2-F3).

**False-positive measurement, stated honestly.** Across **70 問題8 items on all 14
papers on disk, zero findings** — but that is a thin negative sample for the new
arm: the whole corpus contains only **4** 述語/動詞を要求 legs, all on this paper,
all legal, and all three that sit within `LEG_WINDOW` are rejected at the first
gate (their requiring card ends in だ/ほど, not in a case particle). The 直前 guard
is therefore untested by the corpus, so it was tested against **4 synthetic legal
legs** of the risky shapes — a 形式名詞 clause-closer ending in 「は」
(「見つかった場合は」…直前に連体修飾する述語を要求し…塊になる), 伝聞「そうだ」, the 呼応
「だけでなく」→「も」, and 「の」は直後に名詞を要求 — **all four stay clean.** The arm is
precise on everything measurable today; if a legal leg is ever written as a
particle-final card demanding a predicate 直後, it will fire, and the message says
to restate the proof from the real source rather than to re-cut.

### Verification run

`make booklet 20260819_1 && make sheet 20260819_1` (rebuilt in the same change as
the `.md` edit) → `make lint-draft 20260819_1` (**ALL CHECKS CLEAN**) →
`make verify-scramble 20260819_1` (**ARTIFACT ok ×5, PROOF LEG INVALID 0, FREE
UNITS 1/1/1/0/1, exit 0**) → `make check` (**exit 0, "All checks passed (30
skipped), 138 warning(s)"** — the same total as rounds 1–3, and no WARN or FAIL
line has `20260819_1` as its subject; its only non-`ok` lines are the two
`詳細解説.json` skips, which Stage 5 fills). `make sample`, `make mp3`,
`make model-answer`, `make scaffold-explanations` and every translation target
were **not** run.
