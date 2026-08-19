# QA report — テスト `20260818_1` — ROUND 3 (final independent fresh-eyes pass)

Reviewer context: fresh — authored/fixed nothing on this paper, had never seen its
key table when Section 0 below was written.
Timestamp (start): 2026-08-19 18:36 JST (`date` at first tool call)

Reviewed revision (sha1 over raw bytes, as rendered into the keyless build):

| file | sha1 | sha1[:12] |
|---|---|---|
| `tests/20260818_1/言語知識・読解.md` | `02a0e5c6a45817d11c1baf318daaf7e1a125e6e1` | `02a0e5c6a458` |
| `tests/20260818_1/聴解.md` | `fa8048345c4d17b7511d083fcb3ce1d29ec20679` | `fa8048345c4d` |
| `tests/20260818_1/聴解スクリプト.txt` | `fa4e9dbb44bf7b30f8e8b0ee7c1596c810156718` | `fa4e9dbb44bf` |
| `tests/20260818_1/test_spec.json` | `3439adb9b4936077c724941905a8790b3d2990c2` | `3439adb9b493` |

`聴解スクリプト.txt` sha1[:12] = `fa4e9dbb44bf` — matches the `script_sha` the
hand-off said the rebuilt MP3 should carry.

---

## 0. Blind solve — written BEFORE any key table was opened

**Solved from:** `qa/20260818_1/keyless.md` only (1072 lines, built by
`make keyless 20260818_1` from the three shas above). 聴解 solved from the
embedded verbatim `聴解スクリプト.txt`; the MP3 was not played (see §7 Skips).

Disclosure, for honesty about what "blind" means here: my task brief quoted
three keys in passing (問題8-45 = 1, 聴解問題5-2番 質問1 = 2 / 質問2 = 1). I
derived all three independently from the keyless render before checking
anything, and their derivations are written out in the walkthrough, but those
three items were not blind in the strict sense. All other 98 items were.

### 言語知識（文字・語彙・文法）1–51

| # | ans | # | ans | # | ans | # | ans |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 14 | 1 | 27 | 3 | 40 | 2 |
| 2 | 4 | 15 | 1 | 28 | 3 | 41 | 1 |
| 3 | 1 | 16 | 4 | 29 | 3 | 42 | 3 |
| 4 | 3 | 17 | 1 | 30 | 2 | 43 | 4 |
| 5 | 4 | 18 | 3 | 31 | 1 | 44 | 4 |
| 6 | 4 | 19 | 2 | 32 | 3 | 45 | 1 |
| 7 | 4 | 20 | 4 | 33 | 2 | 46 | 1 |
| 8 | 1 | 21 | 2 | 34 | 4 | 47 | 2 |
| 9 | 2 | 22 | 1 | 35 | 4 | 48 | 4 |
| 10 | 2 | 23 | 1 | 36 | 1 | 49 | 2 |
| 11 | 1 | 24 | 2 | 37 | 3 | 50 | 2 |
| 12 | 4 | 25 | 2 | 38 | 1 | 51 | 3 |
| 13 | 4 | 26 | 2 | 39 | 2 | | |

Flat list 1–51:
`1,4,1,3,4,4,4,1,2,2,1,4,4,1,1,4,1,3,2,4,2,1,1,2,2,2,3,3,3,2,1,3,2,4,4,1,3,1,2,2,1,3,4,4,1,1,2,4,2,2,3`

Item 36 was the only 文法 item I was not confident on at solve time (both
`解けっこない` and `解けようがない` read as candidate negations of possibility);
I committed to **1** and recorded the doubt here before opening the key.

### 読解 52–71

| # | ans | # | ans |
|---|---|---|---|
| 52 | 3 | 62 | 4 |
| 53 | 1 | 63 | 3 |
| 54 | 4 | 64 | 4 |
| 55 | 3 | 65 | 4 |
| 56 | 3 | 66 | 4 |
| 57 | 3 | 67 | 1 |
| 58 | 2 | 68 | 3 |
| 59 | 4 | 69 | 2 |
| 60 | 4 | 70 | 4 |
| 61 | 2 | 71 | 2 |

Flat list 52–71: `3,1,4,3,3,3,2,4,4,2,4,3,4,4,4,1,3,2,4,2`

### 聴解

| 問題 | items | answers |
|---|---|---|
| 問題1 | 1–5番 | 1, 3, 3, 3, 2 |
| 問題2 | 1–6番 | 3, 1, 2, 2, 1, 2 |
| 問題3 | 1–5番 | 4, 4, 3, 1, 3 |
| 問題4 | 1–11番 | 2, 3, 1, 1, 2, 1, 3, 1, 2, 3, 3 |
| 問題5 | 1番 | 3 |
| 問題5 | 2番 質問1 / 質問2 | 2 / 1 |

**End of blind solve. Everything below was written after opening the keys.**

---

## 1. Verdict

**`QA: PASS`** — round 3, fresh eyes, all of steps 0–6 run on all 101 items.

- Blind solve: **101/101 agreement** with the shipped keys (third consecutive
  round at 101/101 — no key has ever been wrong on this paper).
- **0 automatic-fail findings. 0 blocking findings.**
- 5 non-blocking findings recorded in §4 (one draw-freshness judgment I accept
  with archive evidence, three next-blueprint notes, one gate-message defect).
  Per `exam-qa-review` §6.5 "Effect on the loop", F1's **gate fix blocks the
  next generation run**, not this paper.
- `make check`: **All checks passed (26 skipped), 123 warning(s)** — exactly
  **one** warning names this paper; resolved in §6.
- `make lint-draft 20260818_1`: `✓ ALL CHECKS CLEAN`.
- `make verify-scramble 20260818_1`: 5/5 items `ARTIFACT: ok`, all five
  `UNDECIDED` (by design), no illegal exclusion leg. Uniqueness re-derived by
  hand below, not taken from the tool.

## 2. Blind-solve diff

**Solved from:** `qa/20260818_1/keyless.md` (built by `make keyless 20260818_1`
from the three shas in the header) and nothing else. 聴解 solved from the
verbatim `聴解スクリプト.txt` embedded in that render. `聴解.mp3` was **not
played** (see §7).

```
python3 tools/qa_eval.py tests/20260818_1 --answers "[...101 answers from §0...]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches**, so there is no reviewer-error-vs-mis-key adjudication to
do. The one item I recorded doubt on before opening the key (問題7-36) is
argued out in the walkthrough; my committed answer `1` was the key.

Sources were still at the end of the pass: `言語知識・読解.md` `02a0e5c6a458`,
`聴解.md` `fa8048345c4d`, `聴解スクリプト.txt` `fa4e9dbb44bf` — unchanged from
the render (re-verified after writing; see §6).

## 3. Per-question walkthrough — all 101 items

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 1 だいり | OK | 「私が**代理**で出席した」— 代=ダイ・理=リ。2×2 {だい,たい}×{り,じ}; たいり=音読み派生(非語, 音読み枝で合法), だいじ=大事, たいじ=退治 | — |
| 問題1-2 | 4 とかい | OK | 「人の多い**都会**へ移り住む」— 都=ト・会=カイ。{と,ど}×{かい,がい} 全て同一漢字の清濁派生 | — |
| 問題1-3 | 1 ひがん | OK | 「**彼岸**には…墓参りをする」— 彼=ヒ・岸=ガン。ひかん=悲観/びがん=美顔/びかん=美観（実在語・同音枝） | — |
| 問題1-4 | 3 しんけい | OK | 「小さな物音にも**神経**を使っていた」— {しん,じん}×{けい,きょう}、神=ジン(神社)・経=キョウ(経典) の別音を試す格子 | — |
| 問題1-5 | 4 みにくい | OK | 「文字の色が薄く…**見にくい**」— 訓読み＋送り仮名型。四択とも実在語（読み/気づき/分かり/見にくい）で 訓読みセットに非語なし = moji-goi §問題1 の (b)同分野枝 | — |
| 問題2-6 | 4 基礎 | OK | 「文法の**きそ**をもう一度確認して」— {基,規}×{礎,祖}、A=基(キ)B=規(キ)/C=礎(ソ)D=祖(ソ) で四択とも「きそ」と読める | — |
| 問題2-7 | 4 量る | OK | 「粉の**重さ**を一グラム単位で」— 重さ/容積は「量る」。測る=長さ・高さ・速さ、計る=時間・数、図る=計画 | — |
| 問題2-8 | 1 支援 | OK | 「被害を受けた地域への**しえん**」— {支,枝}×{援,演}、四択とも「しえん」 | — |
| 問題2-9 | 2 休業 | OK | 「改装のため…三日間**きゅうぎょう**」— {休,求}×{業,行}、四択とも「きゅうぎょう」 | — |
| 問題2-10 | 2 促進 | OK | 「移住を**そくしん**するための補助金」— {促,側}×{進,信}、四択とも「そくしん」 | — |
| 問題3-11 | 1 再 | OK | 「一度は承認された計画だが、予算が足りず（再）検討」— 初/続/新は「初検討・続検討・新検討」が語として不成立 | — |
| 問題3-12 | 4 深 | OK | 「光がほとんど届かない（深）海」— 高海/低海/重海は不成立 | — |
| 問題3-13 | 4 量 | OK | 「交通（量）が多く、渋滞が絶えない」— 率は「高い」と結ぶ、費は運賃の額、交通数は非語 | — |
| 問題4-14 | 1 初旬 | OK | 「**同じ月の**五日ごろにはお手元に届きます」が着日の月を固定 → 発送は同月5日より前 = 初旬のみ | — |
| 問題4-15 | 1 超一流 | OK | 「世界中のホールから招かれる」「だれもが認める」— 一人前/駆け出し/半人前はいずれも下位水準 | — |
| 問題4-16 | 4 上げた | OK | 「腕を**上げた**」= 上達。「入社したころは失敗ばかり」との対比。腕を伸ばす=腕そのもの、広げる=商売、高める=技術/意識 | — |
| 問題4-17 | 1 当分 | OK | 「医者から（当分）激しい運動は控えるように」— たちまち=一瞬、いまだに=継続中の状態、のちほど=直後 | — |
| 問題4-18 | 3 食う | OK | 「車体が大きいので、ガソリンをよく（食う）」— 消費の慣用は食うのみ（時間を食う/電気を食う） | — |
| 問題4-19 | 2 間もなく | OK | 「（間もなく）二番線に電車が到着いたします」— 駅の定型。今にも＋そうだ要求、たった今=完了、いつしか=気づかぬ変化 | — |
| 問題4-20 | 4 付き合って | OK | 「一人では決められないので…友人が（付き合って）くれた」— 立ち会う=第三者、掛け合う=交渉、向き合う=取り組む | — |
| 問題5-21 | 2 一羽もいなくなった | OK | 「百年ほど前に**絶滅した**」— 数が減った/島の外へ移った/めったに見られない はいずれも残存 | — |
| 問題5-22 | 1 怖くて | OK | 「大きな熊に出会い、**恐ろしくて**足が動かなかった」— 悔しい/情けない/苦しい は足がすくむ理由にならない | — |
| 問題5-23 | 1 落ち着いた | OK | 「いつも**穏やかな**口調で指示を出す」— 事務的=冷たい、遠回し=言い方、よそよそしい=親しみのなさ | — |
| 問題5-24 | 2 危なくなった | OK | 「資金が集まらず…実現は**危うくなった**」— 遅れた=時期のみ、取りやめ=決定済み、決まった=反対 | — |
| 問題5-25 | 2 少しずつ | OK | 「肩の痛みは**徐々に**やわらいでいった」— すっかり=結果、ときどき=断続、またたく間=一瞬。公式12/2024 問題5-23 も 徐々に を出題（帯内、選択肢セットは非重複） | — |
| 問題6-26 | 2 | OK | 「音楽家としての**素質**があると言われてきた」= 生まれつきの伸びる力。1=機械の性能、3=努力で身につけた（素質は生得）、4=土地の条件 | — |
| 問題6-27 | 3 | OK | 「泥棒が家に**侵入した**」= 許可なく外から中へ。1=入場、2=参入、4=流出（向きが逆） | — |
| 問題6-28 | 3 | OK | 「赤字続きだった経営は…黒字に**転じた**」= 状態の変化。1=変更、2=曲がっている、4=転用 | — |
| 問題6-29 | 3 | OK | 「県内で採れた果物のジュースを**生産している**」= 商品を量産。1=発表、2=生まれた、4=作って | — |
| 問題6-30 | 2 | OK | 「アジア向けが全体の約六割を**占めて**いる」= 全体に対する割合。1=獲得、3=絶対量、4=集めた | — |

Applied to 問題6 the **owner's** rule (`moji-goi.md` §問題6), not the refuted
domain rule: each wrong sentence is a learner-plausible break, none is a second
attested collocation (searched 土地の素質 / 市場に侵入 / 道が転じる / 支持を占める
— none is standard), and all four options in each item carry the identical printed
word form.

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 というか | OK | 「素朴というか（物足りないというか）」— 並列の二つ目。3 というより は前を退ける言い直しで並列を受けられない | — |
| 問題7-32 | 3 ないものだろうか | OK | 「**なんとか**もう少し短くでき（ないものだろうか）」— なんとか が願望を固定 | — |
| 問題7-33 | 2 に際して | OK | （図書館の掲示で）「ご利用に際して」— に応じて は変数不在、に沿って/に基づいて は指針・根拠名詞を要求 | — |
| 問題7-34 | 4 ものか | OK | 「この雨で（試合ができるものか）。グラウンドは池のようになっている」— 反語。3 わけか は可能性を認めてしまう | — |
| 問題7-35 | 4 につれて | OK | 「標高が上がるにつれて、木の背は目に見えて低く」— に沿って/にわたって/に先立って は名詞接続 | — |
| 問題7-36 | 1 解けっこない | OK（本紙で最も細い弁別） | 「僕に（解けっこない）よ」— 〜っこない は ます形接続で可能形にも付く（勝てっこない/できっこない）。2 解けようがない は 〜ようがない が本来 ます形（解き）に付き、可能形＋に格の経験者主語と噛み合わない。3 かねない=可能性あり（真逆）、4 きれない=完遂の否定 | 直す必要なし。ただし将来 2 を「解きようがない」に差し替えれば二答リスクは構造的にゼロになる（現状でも一答） |
| 問題7-37 | 3 おそれがあります | OK | （気象情報で）「水があふれる（おそれがあります）。早めの避難を」— ようがない/ほかありません/どころではありません は危険の予告にならない | — |
| 問題7-38 | 1 にもかかわらず | OK | 「当日は朝から晴れ、（平日にもかかわらず）…入りきれないほどの人」— だけあって は平日と混雑が結び付かない | — |
| 問題7-39 | 2 上に | OK | 「（値段が安い上に）、店員の対応**も**気持ちがいいからだ」— 後半の も と呼応する添加 | — |
| 問題7-40 | 2 風邪気味 | OK | 「少し（風邪気味）だ」— 加減/具合/気配 は の を要求、接尾語として直接付かない | — |
| 問題7-41 | 1 のみならず | OK | 「（駅舎の設備のみならず）、周辺の歩道の段差の解消に**まで及ぶ**」と呼応 | — |
| 問題7-42 | 3 ところだった | OK | 「**もう少しで**（乗り過ごすところだった）。隣の人が起こしてくれて」— 未実現の直前 | — |
| 問題8-43 | 4 | OK | 地元の人に(1)→限らず(2)→**観光客にも(4)**→人気がある(3)。私の再導出: 「限らず」は裸の「に」を直前に要求 → [1→2] が塊。「そうだ」の直前に立てるのは述語の(3)のみ。残るのは [1→2] と (4) の前後だけで、「も」が前提とする基底命題（地元の人にも人気がある）が未提示のまま広げ先だけを先出しする並びは対応の向きが逆で不成立 | — |
| 問題8-44 | 4 | OK | 和食をはじめ(1)→タイ料理やインド料理まで(2)→**作れるように(4)**→なったと(3)。「自慢している」が引用の「と」を要求 → (3) が最終。「なったと」の直前は「〜ように」で終わる(4)のみ。残る二枚は「AをはじめBまで」で順序固定（到達点の後に代表例を挙げ直す並びは作れない） | — |
| 問題8-45 | 1 | OK（再カット後、私の独立検証で一意） | 祖母が(2)→近くに住んでいてくれる(3)→**おかげで(1)**→慌てずに済んでいる(4)。24通りを手で走査: 文末に立てるのは終止形の(3)(4)のみ、「おかげで」は連体形を直前に要求（印刷済み「〜ときも」は連体形でないので文頭にも立てない）。競合は (3)→(1)→(2)→(4) の一つだけで、そこでは文末述語の主語が祖母になり、「〜てくれる」が受益者を私たち側に固定し主題も「共働きの私たちは」である文と矛盾する。ラウンド2が見つけた二文法並びは解消済み | — |
| 問題8-46 | 1 | OK（純構文的に一意） | 持ち主の高齢化に(2)→伴って(3)→**住宅街へと姿を変え(1)**→つつある(4)。「つつある」はます形要求→(1)のみ、「伴って」は に句要求→(2)のみ、「らしい。」に接続できるのは(4)のみ。塊が二つできて順序が確定 | — |
| 問題8-47 | 2 | OK | 電子申請の利用が(3)→増えたとはいえ(1)→**紙で出したがる(2)**→高齢の利用者が今も多い(4)。「〜たがる」は人主語限定なので (3) の後ろに置けない。(2)を最後に置くと「今も多い」が連体修飾になり「電子申請/紙に高齢者が多い」という趣旨と正反対の文になる | — |
| 問題9-48 | 4 言い換えれば | OK | [論理接続] 前文の観察を「文字に見えているか／機器が文字として扱っているかは別」と言い直す。たとえば=例が来ない、それどころか=打ち消しでない、しかも=新情報なし | — |
| 問題9-49 | 2 言うまでもない | OK | [慣用・形式名詞] 直前で「中身は一枚の絵になる」と説明済み → 「ぼやけ、語を探せない**ことは**（言うまでもない）」 | — |
| 問題9-50 | 2 のも当然だ | OK | [文末モーダル] 掲示板／手元の機器の二例の直後。とは限らない/わけがない は二例と矛盾、どころではない は結びにならない | — |
| 問題9-51 | 3 今後の分を文字で残せばよい | OK | [内容推論] 「一から打ち直すのは簡単ではない**が**、（　）」の逆接。2 は前半が退けた方法そのもの、4 は「大きくすると形がぼやけ」と逆、1 は渡し方の一方のみ | — |

問題9 の四空欄はカテゴリ4種（論理接続／慣用・形式名詞／文末モーダル／内容推論）で重複なし、
選択肢は最長14字（上限16）で読解型の要約選択肢はない。cloze 本文は 567 JP字（目標500–700）。

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 3 | OK | 「初めて会った人と数時間も過ごせるのは、遊びの規則が先に決まっているからだという」＋「何を話すかを考えなくても、順番が回れば手が動き、言葉が出てくる」 | — |
| 問題10-53 | 1 | OK | 「ベンチに所在なげに腰を下ろしていられることは、この街にいてよいと言われるのに近い」 | — |
| 問題10-54 | 4 | OK | 「話し合う形を先に試した三つの部署では、深刻になる前の軽い相談が、その後の一年で二倍近くに増えています」 | — |
| 問題10-55 | 3 | OK | 三条件の合成: 「会員登録をされている方です」＋「午前七時から九時まで」＋「お届け予定日の前日正午まで承ります」 | — |
| 問題10-56 | 3 | OK | 「比べる相手を昨日までの自分に置き換えたとき、比較はようやく自分の役に立ち始める」 | — |
| 問題11-57 | 3 | OK | 「どれも、敬体の選び方や指示語の使い方が絡み、相手との関係によって言い方を変えなければならない」。1は「困りごとは、語の数の不足ではない」で明示的に否定 | — |
| 問題11-58 | 2 | OK | 「作業の手順書を平易な日本語に書き直したうえで、聞き返してよいという合図を先に決めていた」 | — |
| 問題11-59 | 4 | OK | 「あらかじめ日時と会場を印刷し、①来られない場合だけ連絡を求める形に改めた」＝日時会場を先に決めて知らせ、都合の悪い人が断る | — |
| 問題11-60 | 4 | OK | 「封筒を開けてから申し込みが終わるまでの手数が減ったことが、そのまま受診率の差になっていた」。3は「精密検査に進む割合も上がった」で反証 | — |
| 問題11-61 | 2 | OK | 直後の例示「祖母の家からなら通える学校がある」 | — |
| 問題11-62 | 4 | OK | 「聞くことと決めることを分けて考えれば…決定の責任が子どもに移ることはない」 | — |
| 問題11-63 | 3 | OK | 「運筆を数え切れないほど重ねた手が、覚えた形の隙間に、勝手に自分の癖を置いていったのだと思う」 | — |
| 問題11-64 | 4 | OK | 「まねている最中に、まねていない部分が生まれる」 | — |
| 問題12-65 | 4 | OK | A「電車の中で先に手をつけたほうが、頭が余計な準備運動を要らなくなる」＋B「電車の中で今日の段取りを立てておけば、午前の仕事の立ち上がりは速くなる」。2はAのみ（Bは車内作業の可否に触れない） | — |
| 問題12-66 | 4 | OK | A「往復の一時間を仕込みに使えるかどうかで、その日の仕事の質は変わってくる」／B「通勤の時間を仕事に明け渡さないことが、長く働き続けるための備えになる」 | — |
| 問題13-67 | 1 | OK | 直後「建物の骨組みと配管は改修で持たせ、内側の壁は取り払って一部屋を広く取る」。4は「駐車場のまま置くのではなく…広場として貸し出された」で逆 | — |
| 問題13-68 | 3 | OK | 「差が出ていたのは、住民が自分たちで使い方を決められる場所が、建物の中に残されていたかどうかである」。1は「家賃の安さではなかった」で否定 | — |
| 問題13-69 | 2 | OK | 「動かせるのは、住む人が手を入れてよい範囲をどこまで開くかである」＋結び「住民が手を加えられる余白を残したという共通点がある」 | — |
| 問題14-70 | 4 | OK | 表の「印鑑登録証明書…窓口のみ」＋「受け取りには申請時の受付番号が必要です」の二セル合成。3は「申請の翌日以降に」で否定 | — |
| 問題14-71 | 2 | OK | 「ご本人か同じ世帯の方」＋「十五歳未満の方の証明書は、オンラインでは申請できません」の二条件合成（十四歳）。1は送料100円で不足 | — |

読解の機械読み（自分で再測定＋ゲート）: （注N）in-body 31（下限25、目標27–61帯内）／
（中略）3か所すべて 問題11・13 の本文内／問題13 は 800字下限クリア／全20問 max÷min ≤ 1.30／
uniquely-longest key 4/20 = 20%（公式20%、上限30%）／tied-longest 6/20 = 30%（上限35%）／
`<ruby>` 0件／マークスパン ①×5 は本文と設問文で文字列完全一致・7〜15字のポインタ長・（注N）は太字外／
問題11 は (1)から(4)・考え主張設問 3件（公式1–4）・各ペア 事実把握 先行。
注は 雑居ビル/渇き/所在なげ/風通し/見劣り/在留資格/技能実習/敬体/指示語/定着率/がん検診/受診勧奨/
オプトアウト方式/精密検査/行動経済学/意見表明権/児童相談所/一時保護/聴取/代弁/臨書/楷書/朱/師範/運筆/
高経年団地/空室率/分譲/用途変更/共益費/住み継ぐ の31語で、N3–N5 基本語や標準N2語の注はゼロ。

### 聴解 (問題1–5、例を含む)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 4 | OK | 「車にまだ試作品の箱が残ってるから、先に運んできてくれる?」＝アナウンスの「最もよいものは4番です」とマークシートの **(4)** が一致 | — |
| 問題1-1番 | 1 | OK | 「Aの棚の箱、一つずつ数えてくれる?」／2=「台車が修理に出ちゃってて、今日は運べない」実行不可、3=「数が合わないと、部長がはんこを押してくれない」条件不足、4=「そのままで平気だよ」不要 | — |
| 問題1-2番 | 3 | OK | 「昨日届いた写真、お店ごとのフォルダに分けといてくれる?」／1=「写真がそろってから、まとめて回りたいの」順番待ち、2=「会長が知り合いの会社にお願いしてくれてる」別の人、4=「市の観光課で型が決まってて」規則で不可 | — |
| 問題1-3番 | 3 | OK | 「今から順番に電話してみてくれる?」／1=「表の直しは、人が決まってからでいいよ」後回し、2=「名札はもう印刷して封筒に入れてある」既に完了、4=「コピーは増やさなくて平気だよ」明確に否定 | — |
| 問題1-4番 | 3 | OK | 「伺いたいことを先にメールでいただけますか」→「今日中にお送りします」／1=記事の中身が決まってから、2=「今週いっぱい改装で閉めちゃってる」、3以外の4=「細かい数字が手元になくて、お答えできない」 | — |
| 問題1-5番 | 2 | OK | 「かかりつけの医院で…そちらにお電話で空きを伺ってみてください」／1=「コピーは…要りませんよ」、3=「用紙は、医院の枠が取れた方にお渡しする決まり」、4=「診断書のようなものは、うちでは求めておりません」 | — |
| 問題2-例 | 4 | OK | 「二週間、コーヒーをやめてみます」＝announced 4、マークシート **(4)** 一致 | — |
| 問題2-1番 | 3 | OK | 「二十歳以上の方でしたら、どなたでも大丈夫」→「それなら父に頼んでみます。前の日なら来られる」→「四日の午後でお取りしておきますね」／1=希望日は満杯、2=本人は前日まだ海外、4=「管理人さんにお願いすることはできない決まり」 | — |
| 問題2-2番 | 1 | OK | 「自分の手で形にできる回数が、東の方がずっと多いんです。そこが決め手で」／2=「四十分くらい長くなっちゃう」、3=「四年分で計算したら、ほとんど同じ」、4=「テニス部はどっちにもある」 | — |
| 問題2-3番 | 2 | OK（言い換えがやや緩い→F2） | 「子ども、次の日の朝から授業があるので」で水曜を、「金曜は私が会社を出られなくて」で金曜を外し日曜昼を選ぶ。1=「後ろでも構いません」、3=安さは選ばれず、4=「妻は日曜も仕事」 | 鍵を「子どもの翌日の授業にさしつかえないこと」に締めれば言い換えの幅が消える（現状でも他3択が明示否定されており一答） |
| 問題2-4番 | 2 | OK | 「病院に通いたいというお声をたくさんいただきまして、そちらを通す形になりました」／1=「去年より少し増えてる」、3=「工事は去年で終わっております」、4=「人手は、今のところ足りております」 | — |
| 問題2-5番 | 1 | OK | 「地下鉄で振替輸送を行っております」＋「追加のお支払いはございません」／2=一時間待つと三時に間に合わない、3=「特急券をお持ちの方にご案内している相乗り」、4=「バスは振替の対象になっておりません」 | — |
| 問題2-6番 | 2 | OK | 「四十年ずっと、朝五時に起きて川沿いを歩いてた…それだけは」＋結び「朝のことさえ変わらなければ」／1=「距離は気にしてない」、3=「相部屋でも本人は平気」、4=「食べ物にこだわりはない」 | — |
| 問題3-例 | 2 | OK | 温湿度管理・手を触れない・飲み物・鉛筆＝「作品を守るためのお願い」。announced 2、マークシート **(2)** 一致 | — |
| 問題3-1番 | 4 | OK | 「三十ページで合わないと感じたら、そこでやめていい」＋「途中でやめることを自分に許した人ほど、次の一冊に手を伸ばすのが早い」。誤答は本文に出てこない（問題3 は自分の誤答に言及しないのが正しい） | — |
| 問題3-2番 | 4 | OK（再スロット後の整合を確認） | 「踏むまでの時間は、腕ではなく、目で決まります」＋「すでに足がブレーキの上にあります」。読み上げ選択肢の4番目＝正解で `answer_positions["聴解_問題3"][1]=4` と一致、解説行も 2番→4 | — |
| 問題3-3番 | 3 | OK | 「環境のための出費は…値段の変化に耐える体をつくる話なんです」 | — |
| 問題3-4番 | 1 | OK（再スロット後の整合を確認） | 「頭の中に入れるときではなく、取り出すときに強くなる」。読み上げ選択肢の1番目＝正解で `answer_positions[...][3]=1` と一致、解説行も 4番→1。番号入れ替えによる解説ずれなし | — |
| 問題3-5番 | 3 | OK | 「まず、正面の建物にお寄りいただき」…「積むときから分けておいていただきますと」＝持ち込み手順 | — |
| 問題4-例 | 2 | OK | 「五階まで運んでいただけませんか」→「二人で持てば、すぐ運べますよ」。announced 2、マークシート **(2)** 一致 | — |
| 問題4-1番 | 2 | OK | 部下の離席報告→課長が納得して用件を伝える（敬語の向き正しい）。1=課長本人に伝えると言う立場逆転、3=「席が足りない」語義取り違え | — |
| 問題4-2番 | 3 | OK（鍵は妥当。抽選の新鮮さのみ F1） | 記名依頼→「携帯の番号でもよろしいですか」で条件を確かめ返す。1=点検日時の依頼で論点ずれ、2=受け側の発話（立場逆転） | 鍵は直す必要なし。F1（同一 errand の連続出題）を直すなら `--reroll-one quick_response:1` で引き直して本項目を書き直す |
| 問題4-3番 | 1 | OK | 「お先に失礼します」→「お疲れさま。気をつけて帰ってね」。2=訪問客側の挨拶、3=「失礼」の語義取り違え | — |
| 問題4-4番 | 1 | OK | 提案の勧め→「まだ形になってないんですけど」（遠慮）。2=会議終了の誤り、3=佐藤さん本人に「佐藤さんにも伝える」立場逆転 | — |
| 問題4-5番 | 2 | OK | 集合時間の確認→「始発に乗れば、十分間に合うよ」。1=気温の話（論点ずれ）、3=昨日の話 | — |
| 問題4-6番 | 1 | OK | 返却場所の案内→「この箱に入れるんじゃないんですね」（思い違いに気づく）。2=紛失者への案内、3=施設側が返す立場逆転 | — |
| 問題4-7番 | 3 | OK | 「到着予定は三日後です。それでもよろしいですか」→「週末までに間に合うなら、それでけっこうです」。1=「三日前」時制の誤り、2=出ていない前提 | — |
| 問題4-8番 | 1 | OK | 進捗確認→「それが、数字がまだ届かなくて」。2=日程の空き（論点ずれ）、3=「プレゼント」語義取り違え | — |
| 問題4-9番 | 2 | OK（差し替え後の鍵を独立検証） | 屋外中止の案内→「雨でも、中の展示は見られますか」。1=案内を出す側（立場逆転）、3=去年の話（時制ずれ）。受付＝話し相手が定義済みで「宛先のないアナウンス」ではない | — |
| 問題4-10番 | 3 | OK | 品切れ→「次に入るのは、いつごろでしょうか」。1=「切らす／切る」語義取り違え、2=先週の話 | — |
| 問題4-11番 | 3 | OK（薬剤師の修正が全ファイルで一致） | 「薬の説明は、薬剤師からお聞きください」→「その窓口は、会計の隣でしょうか」。1=注射の話、2=説明を次回に回す。`調剤師` は pools/spec/ledger/script/解説 のいずれにも0件、`薬剤師` で一致 | — |
| 問題5-1番 | 3 | OK | 冒頭案「あそこを休けい所にして、順番に回っていただく道を作れないか」→男1・男2が別々の理由で賛成→当番三人の条件が「三人なら出せるって」で満たされ「じゃあ、それでいこう」。1=「レジが止まっちゃって大変だった」、2=「問題を考える時間がないな」、4=「住所を書いていただくことになるので、そこはちょっと」 | — |
| 問題5-2番 質問1 | 2 | OK（全面再執筆分を独立検証） | 「じゃあ、五分のを、パンを食べながら見るか」→「それがいいわ」。1=「朝は、下の子がうるさくて、聞こえないと思う」、3=「下の子の試合で家にいないから無理ね」、4=「去年もためこんで、結局消してた」 | — |
| 問題5-2番 質問2 | 1 | OK | 「電車の中じゃ、画面は開けないだろ」→「だから、さっきの、耳だけでいいのにする。歩きながらでも聞けるって」＝音声配信。同一候補が家では不可・移動中は最適という設計で、質問1と質問2が別解になる | — |

聴解の構造読み（構成表を列で読み、台本と突き合わせ）: 問題1 は 消去方法9トークンが各2行以内・
6件の正解行動すべて相違・決め手は全件が最終発話でない・合図語も 悪いんだけど/なし/それで/なし/実は と分散。
問題2 は どうして2・どのように2・「一番」2（上限2）で quota 内、正解内容6件すべて相違、
鍵は全6件が台本の決め手語の言い換え（ゲートの verbatim 判定 0/6）。問題3 は 施設案内2（例・5番、上限2）・
人物の主張4（下限3）、選択肢はすべて「〜について」なしの裸の名詞句、どの話も自分の誤答に言及しない。
問題4 は 誤答22件の型が最多5件（23%、上限40%）で、型の組み合わせが一致する対はない。
問題5 は 3話者・3話者で、質問1と質問2の選択肢順は読み上げ列挙順（音声配信/朝のまとめ/週末の特集/録画）と同一、
決め手の属性は選択肢名に印刷されていない（「音声配信」まで）。
同一大問内で 正解の内容が重複する項目はゼロ（問題3 の 1番・4番 は同じ番号4だが内容は別物で、
ゲートの照合対象も選択肢テキスト）。

## 4. Findings

Severity key: **AUTO** = automatic fail (blocks the paper) · **BLOCK** = blocking
finding · **MINOR** = real but non-blocking, repair optional for this paper ·
**NEXT** = next-blueprint observation · **GATE** = tooling defect, no paper impact.

**AUTO: none. BLOCK: none.**

| id | 項目 | class | severity | evidence | repair (appliable as written) |
|---|---|---|---|---|---|
| **F1** | 聴解問題4-2番 (+ 4-8番, 4-10番) | drawn-item freshness: same **errand key** as a recent paper, invisible to the gate | **MINOR** | `pools.json` `quick_response_keys` assigns 「窓口:記名依頼」 to BOTH this paper's 「お客様、恐れ入りますが、こちらにお名前とご連絡先をご記入いただけますでしょうか。」 and `20260817_3`'s 「恐れ入りますが、こちらの書類にご署名をお願いできますでしょうか。」 (its 問題4-4番) — the **immediately previous** paper, inside `quick_response`'s own 16-draw cooldown. The reply shape coincides too: 20260817_3's 解説 reads 「署名を求められ、印鑑でもよいかを確かめ返す1が正解（応じる意思を前提にした間接的な返答）」, this paper's 「…携帯の番号でよいかを確かめ返す3が正解（応じる意思を前提にした間接的な返答）」. Same class, 2 more: 「職場:進捗確認」 vs `20260817_2`, 「店:在庫照会」 vs `20260810_1`. Also `20260813_2`'s 問題4-10番 stimulus 「担当者:恐れ入りますが、こちらの用紙にお名前とご連絡先をご記入いただけますか。」 is 0.864 difflib-similar to this paper's line with the same reply type (「この欄でいいですか」/「携帯の番号でもよろしいですか」) | Optional for this paper: `python3 .agents/exam-blueprint/scripts/sample_items.py 20260818_1 --reroll-one quick_response:1` (index 1 = the 記名依頼 entry), re-author 聴解問題4-2番 from the new stimulus, update `test_spec.json`/`logs/ledger.json` (the reroll writes both) and `logs/topics.json`'s five fields for that row, then `make mp3 20260818_1 && make booklet 20260818_1 && make sheet 20260818_1 && make check`. **Mandatory before the next paper: the gate scope fix in §5/R1.** |
| **F2** | 聴解問題2-3番 | key paraphrases its deciding line loosely | **MINOR** | Script: 「安いのはうれしいんですけどね。子ども、次の日の朝から授業があるので。」 Key: 「子どもが学校を休まずにすむこと」. Going to a Wednesday **evening** show would not literally require an absence; the printed key overstates 「翌朝の授業にさしつかえる」 as 「学校を休む」. The item is still one-answer: 1 is waived on air (「後ろでも構いません」), 3 is declined (「安いのはうれしいんですけどね」+ the 授業 reason), 4 is false (「妻は日曜も仕事」) | In `tests/20260818_1/聴解.md` replace 「子どもが学校を休まずにすむこと」 with 「子どもの翌日の授業にさしつかえないこと」 in the **three** places it occurs — L67 (printed option 2 of 問題2-3番), L263 (構成表 正解 cell), and L198's 解説 sentence 「台本の『次の日の朝から授業がある』を『学校を休まずにすむ』と言い換えている」 → 「…『翌日の授業にさしつかえない』と言い換えている」 (the 構成表 鍵の言い換え cell on L263 carries the same sentence). The string occurs **0** times in `聴解スクリプト.txt`, so no script edit and no MP3 rebuild; `make booklet 20260818_1 && make sheet 20260818_1 && make check` only. Leaving it as shipped is defensible — this is a tightening, not a correction |
| **F3** | 問題12 | commuting appears one paper apart, this time as a headline surface | **NEXT** | This paper's 問題12 = 通勤の一時間の使い方 (theme 交通, headline). `20260817_3`'s 問題10(3) = 自転車通勤の危険度を決めるのは距離と経路の組み合わせ (theme 交通, non-headline). Rule 4 binds headline-vs-headline only, and 交通 is not in `20260817_3`'s headline set, so **no rule is breached**; the shared setting (the commute) is nevertheless one paper old | Next blueprint: when the 問題12 draw lands on a theme the previous paper spent on ANY 読解 surface, check the SUBJECT before authoring (`exam-blueprint` rule 4b already prescribes exactly this for the cloze — extend the same 5–15-char subject check to 問題12/13/14) |
| **F4** | 聴解問題5-1番 | 2-back cross-register subject overlap | **NEXT** | 空き店舗の活用: this paper's 聴解問題5-1番 = 空き店舗3軒を休けい所にしてスタンプラリーの道を作る; `20260817_2`'s 問題10(5) = 空き店舗を活用した若手店主による多世代交流拠点づくり. Two papers back, different register, different errand (rest stops on a walking route vs a multi-generation hub). Same class as the 夫婦-in-問題5-2番 note (standing item 4) | Record in `logs/topics.json` notes for the next blueprint; no repair to this paper |
| **F5** | tooling | `check_spec_errand_rotation`'s green line asserts more than it measured | **GATE** | It prints 「20260818_1: no drawn errand repeats inside its own cooldown window」 with no count. I re-ran its predicate myself: **0 of this paper's 33 themed draws carry an errand `key`**, so for the two categories the check actually loops over it compared nothing. This paper is the only one of the 13 with zero keyed themed draws (others: 1–4). The precedent for this failure shape is in `exam-qa-review`'s own automatic list ("the gate prints '0 prescribed' and passes, verifying nothing") | In `tools/check_consistency.py::check_spec_errand_rotation`, print the comparison count in the check name, e.g. `f"{d.name}: no drawn errand repeats inside its own cooldown window ({keyed} keyed draw(s) compared, {len(qr)} quick_response)"`, and make `keyed == 0` print as a `skip(...)` rather than an `ok(...)` for the categories that contributed nothing |

Everything else I looked for and did **not** find, so it is on record as checked:
no mis-key, no second defensible answer, no unanswerable item or 例, no
off-level key, no non-word option, no ungrounded 聴解 distractor, no 解説 quote
absent from its source (97 聴解 + 57 読解 quotes all matched verbatim after
stripping （注N）), no 「言及なし」/「未言及」 confession in a 問題1–2 解説, no
（注N） orphan, no `<ruby>`, no verbatim or near-verbatim passage/dialogue reuse
from another test or from `refs/`/`imported-*` (733 sentences × 7,712 compared;
every ≥0.9 hit is official fixed rubric), no spec↔ledger mismatch, no
spec↔topics theme disagreement, no artifact older than its source, no headline
theme repeat, no in-paper subject repeat, no 問題14/聴解 shared decisive number.

## 5. Root-cause table (step 6.5)

Recurrence measured by reading the papers on disk, not estimated.

| id | root cause | tests showing the class | owning file | proposed edit (concrete) |
|---|---|---|---|---|
| **R1** ← F1, F5 | `GATE-BLIND` (+ the silence half of `GATE-WRONG`) | **2 of 13** — `20260818_1` (3 repeats) and `20260817_2` (1: 「窓口:担当者不在」 vs `20260813_1`). ≥2 ⇒ systemic by definition | `tools/check_consistency.py` (`check_spec_errand_rotation`), with a data note for `.agents/exam-blueprint/references/pools.json` | Change the category loop from `for cat in ("listening_scenarios", "reading_topics")` to `for cat in ("listening_scenarios", "reading_topics", "quick_response")`. `sample.errand_key()` already resolves `quick_response` strings (`build_key_index` folds `quick_response_keys` into `_KEY_BY_TEXT`), so no other code changes. **Predicate already run against its founding case and every paper on disk** (this review, §4 F1): it fires on `20260818_1` (3) and `20260817_2` (1) and on nobody else — so committing it requires either grandfathering `20260817_2` by name in `ERRAND_ROTATION_GRANDFATHERED` (it shipped before the map existed) or accepting one new WARN there. Also print the compared count so a zero-coverage run reads as `skip`, not `ok` (F5). Data note: 「席を外しております」 (keyed 窓口:担当者不在) and this paper's 「課長、来客の応対で少々席を外しておりました。」 (unkeyed) are deliberately NOT clustered — the speech acts differ (informing a customer vs self-reporting to one's boss); leave them unkeyed, but say so in the map's comment so the next editor does not "fix" it |
| **R2** ← F3, F4 | `RULE-UNENFORCEABLE` — rule 4b's subject check is written for the cloze only, so 問題12/13/14 and 聴解問題5 land on a 1–2-paper-old SUBJECT while every theme rule stays green | 2 of 13 for this exact shape (`20260818_1` 問題12; `20260817_3`'s cloze vs `20260817_2`'s 問題10(4), already recorded in `exam-blueprint` rule 4b) | `.agents/exam-blueprint/SKILL.md` §"The four theme rules", rule 4b | Widen rule 4b from 「問題9 は…」 to: 「**headline surfaces (問題9/12/13/14/聴解問題5-1番/5-2番) each get a 5–15 JP-char SUBJECT written at blueprint time, and each is diffed against the previous paper's THIRTEEN 読解 subjects AND its 21 聴解 subjects in `logs/topics.json` `surfaces` — headline or not. Same setting + different issue is allowed and must be written down as such in `notes`; same setting + same issue is a redraw.」 Not mechanizable beyond that (subject identity is judgment), so it belongs in the blueprint procedure, not the gate |
| **R3** ← F2 | `RULE-MISSING` — nothing requires a 聴解問題2 key to be a paraphrase that stays inside what the deciding line actually asserts. The existing rules push the other way: `make check` fails a key that is a **verbatim** token match, so authors paraphrase, and nothing bounds how far | 1 of 13 (this paper) — below the systemic threshold, filed as a rule gap rather than a pattern | `.agents/question-authoring/references/choukai-items.md` §問題2 (key paraphrase) | Add: 「言い換えた鍵は、決め手の一行が**主張していること**を超えてはならない。台本が『次の日の朝から授業がある』と言うとき、鍵は『翌日の授業にさしつかえない』までで、『学校を休まずにすむ』（欠席の話）は台本が言っていない事態を持ち込んでいる。QA 手順: 鍵の文を台本の決め手の一行と並べ、鍵にしかない名詞（欠席・休む・遅刻…）を一つずつ指さして、その語が台本のどの語に対応するか言えるかを確かめる。」 Not string-decidable; keep it as an authoring+QA procedure |

`RULE-IGNORED`: none — every rule I checked that has a specific written form was
followed, including the ones the last two rounds installed (問題7 stem
distribution, marked-span identity, 問題3 解説 wording, the 問題6 owner rule).

## 6. Coverage — the slot × paper topic table (step 5)

Built from the SHIPPED content (I re-read every passage and script block and
re-tagged it myself); `logs/topics.json` agreed with my re-tag on all 47 rows,
and agreed with `test_spec.json` on all 33 themed surfaces (the spec-vs-topics
theme disagreement class is clear).

| slot | 20260818_1 (this) | theme | 20260817_3 | 20260817_2 |
|---|---|---|---|---|
| 問題9 | 知らせを文字として残すか画像として残すかの違い | デジタル化 | 値上げと内容量削減のどちらが買う人の信頼を損なうか | 自動販売機の技術進化と防災インフラ化 |
| 問題10(1) | 一人客が初対面の相手と長く同席できるボードゲームカフェ | スポーツ・余暇 | 社外での就業を届出制と許可制に分ける社内規程の改定メ… | 旧耐震基準建物の耐震改修の必要性 |
| 問題10(2) | 用がなくてもいてよいと伝える公園のベンチ | 地域活性化 | 加工食品の賞味期限表示を年月日から年月へ変えるお知ら… | 睡眠の質が翌日の作業効率を左右する仕組み |
| 問題10(3) | ハラスメント防止研修を動画視聴から部署ごとの話し合いに改める社内メー… | 働き方 | 自転車通勤の危険度を決めるのは距離と経路の組み合わせ | 認知症患者でも音楽で記憶がよみがえる現象 |
| 問題10(4) | 宅配の時間帯指定を朝夜だけ一時間刻みに改めるお知らせ | 消費・経済 | 手書きが生む書き出す前に考える時間 | マイナンバーカードによる証明書発行の一元化 |
| 問題10(5) | 比べる相手を昨日までの自分に置き換える | 人間関係 | 習い事をやめる時期を子ども自身に決めさせる | 空き店舗を活用した若手店主による多世代交流拠点づくり |
| 問題11(1) | 生活の日本語と仕事の日本語を分ける相手と目的 | 教育 | 農泊で持ち帰るのは名所より家の日常 | 特定空き家指定制度と固定資産税軽減措置の打ち切り |
| 問題11(2) | 案内文と手続きの形だけを変えて上がったがん検診受診率 | 医療・福祉 | 挨拶の多い集合住宅ほど共用部の傷みと修繕費が少ない | 円安による生活費上昇が非正規・年金生活者に偏る構造 |
| 問題11(3) | 子どもに聞く手順と決める責任を分ける意見表明権 | 子育て・家族 | デジタルタトゥーの中心が本人の書き込みから他人の記録… | 夫の両親との多世代同居で重ねる価値観のすり合わせ |
| 問題11(4) | 臨書を重ねた手に現れた教わっていない線 | 文化・伝統 | 疑うことと出所をたどって確かめることの違い | 日本の譲り合い文化の背景にある同調圧力 |
| 問題12(A) | 通勤の一時間をその日の仕事の仕込みに使う | 交通 | 失われる自然を近くに作り直して埋め合わせる開発論 | 観光地の入場者数上限設定を支持する意見 |
| 問題12(B) | 通勤の一時間を勤務の外に置いて長く働き続ける | 交通 | 代えのきかない場所を計画段階で開発対象から外す保全論 | 予約・料金による需要調整を重視する意見 |
| 問題13 | 住民が手を加えられる余白を残した高経年団地の再生 | 住まい | 遠隔診療が引き受けられる情報の範囲と通院負担による普… | AI普及による雇用構造の変化と学び直し支援の必要性 |
| 問題14 | ひばり市の証明書オンライン申請のご案内 | 行政・手続き | みどり市民スポーツ大会の参加募集要項 | 大学奨学金3類（学業奨励・家計急変・家計基準）の申請… |
| 聴解問題1-例 | 見本市のブース設営で車から試作品の箱を運ぶ | 働き方 | 写真教室の撮影会で変更された集合場所の下見 | サークル部室での歓迎会案内メール送付準備 |
| 聴解問題1-1番 | 倉庫の棚卸しで帳簿と合わない棚の箱を数え直す | 働き方 | 新製品発表会に向けた開発部からの試作品借用 | 来客対応引き継ぎでの資料印刷 |
| 聴解問題1-2番 | グルメマップ編集で増えた写真を店ごとに分ける | 地域活性化 | 研究室で桁の違う測定値を実験ノートと照合 | 引っ越し見積もりのための荷物リスト作成 |
| 聴解問題1-3番 | 講演会の受付の欠員を埋めるため学生に電話する | 働き方 | 専門学校の資料請求200件を地域ごとに仕分ける発送準… | クレーム対応での出荷事実確認 |
| 聴解問題1-4番 | 社長不在の取材先へ質問を先にメールで送る | メディア・情報 | 郵便局窓口で不在連絡票がなく荷物を受け取れない | イベント会場準備の椅子並べ |
| 聴解問題1-5番 | 集団接種の枠が埋まりかかりつけの医院に電話する | 医療・福祉 | ハローワークで応募の前に必要な求職登録 | 塾体験授業前のレベルチェックテスト受験 |
| 聴解問題2-例 | 薬より先に寝る前の過ごし方を見直す薬局の助言 | 睡眠・健康 | 会議が一日増えたための航空券の翌日便への振り替え | 社内食堂メニューリニューアルで一番多い要望 |
| 聴解問題2-1番 | 一年ぶりに帰国する人が止めていたガスの開栓を父親に立ち会ってもらう | 住まい | エレベーターのない四階への引っ越しで見積もりが上がっ… | テレワーク機器配布方法変更の理由 |
| 聴解問題2-2番 | 献立を自分の手で形にできる回数で志望校を変える | 教育 | クリーニングの仕上がりが来週になる理由 | 学習法講演で一番おすすめの勉強法 |
| 聴解問題2-3番 | 子どもの翌朝の授業を優先して選ぶ公演の日 | 文化・伝統 | 傷んだ毛先を避けた根元だけのカラー | ベビー用品レンタルの返却方法 |
| 聴解問題2-4番 | 総合病院の前を回すことになったバス路線の変更 | 交通 | 部屋探しで最優先する夜間の楽器演奏可 | 携帯電話料金プラン変更の理由 |
| 聴解問題2-5番 | 追加料金なしの地下鉄振替輸送で目的の駅へ向かう | 交通 | 鍵を箱に入れるだけのホステルのチェックアウト | コンサート入場時に見せるもの |
| 聴解問題2-6番 | 四十年続けた朝の散歩を続けられる介護施設 | 医療・福祉 | 振り替え制度を決め手にしたカルチャー教室選び | プール利用で一番気をつけてほしいこと |
| 聴解問題3-例 | 作品を守るための美術館からのお願い | 文化・伝統 | 図書館の自習席予約方法の変更 | 健康診断受診方法変更のお知らせ |
| 聴解問題3-1番 | 途中でやめてもよいという読み方 | 教育 | 服を繊維の原料に戻して作り直す技術 | 産地分散栽培という農家の工夫 |
| 聴解問題3-2番 | 危ないと予想しながら走ること | 教育 | 入居前の暮らし方をそのまま続ける介護施設の方針 | 数が増えても品質にこだわる弁当店の姿勢 |
| 聴解問題3-3番 | 環境への取り組みと会社の力 | 環境 | 契約を急がせない初回相談に変えたエステサロン | てまえどり運動をきっかけとした客の意識の変化 |
| 聴解問題3-4番 | 思い出す練習と記憶の関係 | 科学・技術 | 点検で運転の癖を伝える整備担当の考え | 信頼に基づく働き方への転換 |
| 聴解問題3-5番 | 大きなごみを持ち込むときの手順 | 環境 | 温泉で安全に入浴するための過ごし方 | カーシェア返却方式の変更 |
| 聴解問題4-例 | 荷物を五階まで運ぶ依頼への応対 | 人間関係 | 資料のコピー依頼への即応 | 資料確認依頼への即応 |
| 聴解問題4-1番 | 離席の理由の報告への応対（会社） | 働き方 | 申請書の書き方を教えてほしいという依頼への応対 | 業務進捗確認への回答 |
| 聴解問題4-2番 | 名前と連絡先の記入依頼への応対（自宅での点検作業の記録票） | 住まい | 資料作成を手伝ってもらった礼への応対 | 待機案内への応対 |
| 聴解問題4-3番 | 先に帰る同僚のあいさつへの応対（会社） | 働き方 | 数字を大きくという助言への応対 | 障害報告の申し出への応対 |
| 聴解問題4-4番 | 企画会議で出してはという勧めへの応対（会社） | 働き方 | 書類への署名依頼への応対 | 荷物預かり申し出への応対 |
| 聴解問題4-5番 | 明日の集合時間の確認への応対（建設現場） | 働き方 | 時間をもらった礼への応対 | 体調を気遣う声かけへの応答 |
| 聴解問題4-6番 | 鍵の返却場所の案内への応対（貸し会議室） | 働き方 | 撮影を控えるよう求める案内への応対 | 完売案内への応対 |
| 聴解問題4-7番 | 取り寄せレンズの到着予定の確認への応対（眼鏡店） | 消費・経済 | 議事録の確認依頼への応対 | 担当者不在案内への応対 |
| 聴解問題4-8番 | プレゼン資料の進み具合の問いへの応対（会社） | 働き方 | 事業計画書の説明の申し出への応対 | キャンセル料発生確認への応対 |
| 聴解問題4-9番 | 雨天による屋外イベント中止の案内への応対（科学館の受付） | 科学・技術 | 「願ってもない」と言われたことへの応対 | 助言を気に留めていない件への応対 |
| 聴解問題4-10番 | 品切れの案内への応対（花屋） | 消費・経済 | 印刷を明日の会議に間に合わせてほしいという依頼への応… | 講演後の質問申し出への応対 |
| 聴解問題4-11番 | 薬の説明を薬剤師から聞くよう促す案内への応対（病院の会計・院内薬局あ… | 医療・福祉 | 懇親会に顔を出せないかという誘いへの応対 | 面会時間案内への応対 |
| 聴解問題5-1番 | 空き店舗を休けい所にして順番に回る道を作るスタンプラリー | 地域活性化 | 町内会の世代間交流イベントを公園での炊事に決めた話し… | 居酒屋宴会コースの3人での検討 |
| 聴解問題5-2番 | テレビの専門家が挙げたニュースとの付き合い方四つから、夫婦がうちで一… | メディア・情報 | 地域防災訓練の四プログラムを互いの助言で選び直す二人 | 家庭支援センターで夫婦が相談方法を段階的に絞り込んで… |

### 6.1 `make check` — every WARN that names this paper, resolved

`make check` → **All checks passed (26 skipped), 123 warning(s)**. Of the 123,
**exactly one** names `20260818_1` (line 2190 of the run; also printed inline at
line 401). One `skip` also names it. Everything else belongs to older papers.

| line | WARN / skip | resolution |
|---|---|---|
| 401 / 2190 | `no 聴解 slot repeats its own theme in the previous 2 papers (2 slot(s)) — 聴解問題2-2番=教育 (also 20260817_2); 聴解問題2-1番=住まい (also 20260817_3)` | **Both resolved as acceptable, with reasons, not by re-tagging** (re-tagging to dodge a WARN is forbidden — `exam-blueprint` rule 4c). **住まい (問題2-1番):** the drawn errand is 「ガス会社:開栓の予約」 — a returning-from-abroad customer arranging who will be present for the gas turn-on. 住まい is the honest tag for a service call to a home; `20260817_3`'s same-slot 住まい item was 「引越し:見積もり」 (a moving quote). Different institution, different errand, no shared decisive detail, and the author had already **re-angled this item off a house-move setting**, which is the substantive repair the WARN asks for. I agree with round 2. **教育 (問題2-2番):** this paper's item is 塾:進路面談 — a student switching first-choice universities because one gives her more chances to build her own menu ideas; `20260817_2`'s same-slot 教育 item was 塾:体験授業. I note more than the theme matches: both are set in a 塾. Two papers apart, the errands (career counselling vs a trial lesson), the decision structure and the discriminating axis all differ, and 教育 carries 3 of this paper's 21 listening slots against a cap of 5. Acceptable — but this is the row I would spend the next paper's re-angle on, because *institution* identity in one slot is a stronger tell than a theme tag, and no check measures it across papers (within a paper, `check` does: "no two 聴解 items of one 大問 share an establishment type"). |
| 2133 | `skip 詳細解説.json options match the booklet — no 詳細解説.json (run make scaffold-explanations)` | Correct and expected: `make model-answer` is the **final** step, run only after QA passes (`AGENTS.md` §5). Nothing to resolve; it becomes live when 模範解答.html is built. No stale-option risk exists yet because no `詳細解説.json` exists. |

Warn-class lines I additionally re-derived by hand because they are the ones a
regex cannot settle, and which this paper passes rather than merely not tripping:
問題7 stem distribution (gate: mean **42.0** inside 36–52, **3** stems under 34,
spread **35** ≥ 25 — my own remeasure of the bare stems: 22/28/29/29/34/35/35/37/
38/41/46/55, i.e. 4 under 30, against official 7/2025's ~21% under 30 and the
twelve older papers' **zero**); 読解 uniquely-longest key 20% and tied-longest
30%; 聴解 uniquely-longest 14% and median key ÷ distractor-mean 1.04;
（注N） 31 in-body.

### 6.2 The five standing items I was asked to rule on

1. **The slot × theme WARN (問題2-2番=教育, 問題2-1番=住まい).** Ruled above in
   §6.1. **Agree with round 2 on both**, with one addition round 2 did not state:
   the 教育 row is also an *institution* repeat (塾 → 塾) in the same slot two
   papers apart. Still not a defect — but it is where the next re-angle should go.
2. **R6 (問題6 "never leave the word's own domain") — the refutation HOLDS.** I
   verified the counterexamples in the archive myself rather than trusting the
   citation: `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md` L100 「うるさいと言われた
   ので、テレビの音量を薄めた。」, L102 「今日の午後は雨の予報で、空には雲が充実して
   いる。」, L112 「明日、駅のふもとで池田さんと会う約束をした。」, L120 「犬の定年は
   一般的に 10 歳から 15 歳の間だといわれている。」 — all four are printed **wrong
   options** in a real sitting, and all four leave the target's domain. The rule as
   written would fail that sitting and would fail this paper's 問題6-26 (掃除機/土地)
   and 問題6-30 (賞金/十キロ). The owner file (`moji-goi.md` §問題6) now states the
   three things that actually fail a wrong sentence (no learner would produce it /
   a second attested collocation / a form tell), and I applied **those** in §3. The
   refutation is filed at the owner with evidence and route history, which is the
   right place; nothing to re-open.
3. **`pools_sha` "INERT" labelling — honest.** The gate line reads
   `every stamped spec's pools_sha matches pools.json (d24928db9883) [1 stamped of
   13; INERT on the 12 unstamped: …]`, naming every id it verifies nothing about.
   That is the opposite of the failure it is guarding against. For the one stamped
   spec (this paper) the check is live and green: the stamp equals the current
   `pools.json` sha1[:12] (`d24928db9883`, recomputed independently). Backfilling
   the other 12 is correctly refused — nobody can recover the pool bytes a past
   draw saw, so a hand-written stamp would be a fabrication. One thing I can only
   *corroborate*, not prove: that this paper's stamp is machine-written. It is
   consistent with the tool having written it — `pools.json` mtime 17:35:31 <
   `test_spec.json` = `logs/ledger.json` = **18:08:00 to the same second**, which
   is what one `sample_items.py` reroll run looks like and not what two hand edits
   look like — and `sample_items.py` stamps at lines 1078/1089, 1161/1170 and
   1215/1221 on exactly the `--reroll`/`--reroll-one` paths this seed records. I
   cannot rule out a hand refresh, and say so rather than implying I verified it.
4. **`20260817_2`'s 問題5-2番 was also a 夫婦 item (2 papers back).** Agree with
   round 2's successor: **minor note, not a finding.** Subject (家庭支援センターで
   の相談方法の絞り込み vs テレビの専門家が挙げたニュースの追い方), theme
   (子育て・家族 vs メディア・情報) and decision structure (段階的絞り込み vs
   共同決定＋用途別の第二選択) all differ. What repeats is the CAST. Recorded as
   F4's sibling; if anything is worth adding to `choukai-items.md` it is a cast
   rotation line for 問題5 (夫婦/同僚/親子/店員と客), not a subject rule.
5. **The `ERRAND_ROTATION_GRANDFATHERED` entry for this paper was removed — I
   verified the breach is gone, not just the exemption.** Independently
   recomputed: the old 聴解問題5-2番 entry 「陶芸教室:初心者コースの説明」 carries
   `key` 「カルチャースクール:受講申し込み」 in `pools.json`, and so do
   `20260817_1`'s 「カルチャースクールの受講手続き」 and `20260817_3`'s
   「カルチャー教室:コース選び」 — three inside an 11-draw window, which is the
   breach that earned the exemption. The shipped entry is 「テレビ:専門家の解説」,
   which carries no `key` and appears in no prior ledger entry; intersecting this
   paper's 21 listening + 12 reading draws against each category's own cooldown
   window (11 and 22 draws) by display string, folded through `head()`, gives
   **zero** repeats in all 11 categories. So the grandfather was removed because
   the breach was removed. **Caveat, which is F5:** for the two categories that
   check loops over, this paper now has 0 keyed entries, so its green line is not
   independent evidence — my by-hand recomputation above is.

### 6.3 Provenance (step 6), re-verified independently

- **Spec ↔ ledger:** identical field for field. Same 11 categories, same item
  strings in the same order (5/5/3/7/5/5/12/5/11/12/21 = 96 draws), same themes on
  all 33 themed entries, same `seed`, same `generated_at`, same `pools_sha`. No
  `harvest_sha` field exists on either side (so no date-shaped fabrication).
- **Seed expression** records the recovery history the brief describes, in full:
  `9670904` + 2 `--reroll(listening_scenarios)` + 1 `--reroll-one(quick_response:8)`
  + **5** `--reroll-one(listening_scenarios:16)` (seeds 70517349, 92056458,
  94620437, 69634010, 74989867). That matches the 聴解.md audit note's account of
  the 問題5-2番 redraw (three rejected on theme rule 4, one rejected for colliding
  with this paper's own 問題10(1) ボードゲームカフェ, the fifth accepted) — and the
  rejection of a ボードゲームカフェ scenario **because this paper's 問題10(1) already
  uses it** is process evidence I could not have got from the paper alone.
- **Replay:** I did not attempt a seed replay. `pools.json` has been edited since
  the draw (the 調剤師→薬剤師 repair), so a replay cannot reproduce the draw
  item-for-item by construction — which is exactly what `pools_sha` exists to
  record. Round 1 replayed 6/11 categories and round 2 got 4/11 for the same
  reason; a third partial replay would add nothing that the stamp does not.
- **Target item match (問題1–8, 聴解問題4):** all 21 vocab/kanji/grammar targets and
  all 11 即時応答 stimuli are the exact spec strings (gate: `問題1/2/4 test the
  items test_spec.json drew (21 targets)`, `問題8 items realize their drawn
  grammar_p8 targets (5 drawn)`, `every recorded draw resolves to a pools.json
  entry (22 items)`), and I spot-verified the repaired one end to end: `薬剤師`
  appears in `pools.json`, `test_spec.json`, `logs/ledger.json`,
  `聴解スクリプト.txt` and the 解説; `調剤師` appears in **none** of them.
- **listening_scenarios → surfaces:** I mapped all 21 drawn scenarios onto the 21
  authored 聴解 settings (問題1 例+5, 問題2 例+6, 問題3 例+5, 問題5 ×2). Every drawn
  entry is used exactly once and every authored item resolves to one drawn entry —
  no unrecorded substitution, no unused draw. Same for the 12 `reading_topics` →
  the 12 pool-origin 読解 surfaces; the 13th surface (問題9 cloze) legitimately has
  no pool entry, no draw and no cooldown.
- **Answer positions:** all 101 keys equal `answer_positions` slot for slot
  (verified by diffing my own §0 answer list, which equals the shipped keys,
  against the spec arrays).
- **Copyright non-reproduction:** invented specifics are N2-rounded and
  non-citational (約4割 → 「全体の約六割」, 「前年の一・四倍」, 「二倍近く」,
  250/300/350円, 送料100円); no passage, dialogue, 例, stem or option matches
  `refs/` or an `imported-*` paper (similarity scan in §4).

### 6.4 Answer-position distribution (the item I was asked to judge as shipped)

Whole paper: **1×26 / 2×26 / 3×26 / 4×23**. 言語知識・読解 (71): 17/18/15/21.
聴解 (30): 9/8/11/2 — but 11 of those items are the 3-option 問題4, so the
four-option listening pool is 19 items with position 4 keyed **twice** (10.5%),
and **問題1 and 問題2 key no 4 at all**.

I measured the archive rather than guessing at a ceiling (31 sittings,
`refs/JLPT_N2_NEW/*/key.md`):

- Official 問題1 keys no 4 in **10 of 31** sittings; 問題2 in **4 of 31**;
  **both** empty in **2 of 31** — `8. N2 7-2017` (問題1 `[1,2,2,3,2]`, 問題2
  `[3,3,3,1,2,3]`) and `14. N2 7-2023` (問題1 `[3,2,2,2,3]`, 問題2
  `[2,3,1,3,1,3]`). This paper's shape (問題1 `[1,3,3,3,2]`, 問題2
  `[3,1,2,2,1,2]`) is therefore **attested official practice**, including the
  three-of-one-number run in 問題1 (cf. `6. N2 7-2015` 問題1 `[3,3,2,3,3]`).
- 問題11's 4×4-of-8 with no 1 is likewise inside the archive: official 問題11 has
  a 4-of-one-position in 5 sittings and a 5-of-one in 1, and **2 sittings key
  only three of the four positions** — including `16. N2 7-2025`, whose 問題11
  keys `[1×2, 2×4, 3×2]` and no 4 at all.

**Ruling: the shipped per-section distribution is acceptable as it stands.** The
whole-paper balance (26/26/26/23) is tighter than most official sittings, and the
two thin sections have direct official precedent. Re-keying now would mean
rewriting correct items for a pattern the archive contains, which is a worse
trade than shipping it.

## 7. Skips and limits — stated, not implied

1. **`聴解.mp3` is UNLISTENED.** I have no audio playback in this environment. I
   verified everything about it that is verifiable without hearing it — it was
   built from the current script (`script_sha fa4e9dbb44bf`, equal to the file's
   own sha1[:12]), with the current pacing (`pacing_sha d241e428f28f`), and its
   mtime (18:29) is later than `聴解スクリプト.txt` (18:27) while
   `聴解_チャプター.json` (18:29) matches, so no artifact predates its source. What
   nobody has checked in three rounds: whether the synthesis actually *sounds*
   right — voice/gender assignment as heard, pause lengths at the answer gaps,
   mis-read numbers or 漢字 readings (e.g. 「彼岸」-class words do not occur in the
   script, but 「四日」「二十歳」「一羽」 do), clipping, and the 例 announcements. **This
   is the paper's largest unverified surface**, and it is unverified by the same
   limitation in all three rounds, not by choice.
2. **The scanned N2 volumes were not page-read.** `Shin Kanzen N2-Goi/Kanji` and
   `日本語総まとめ N2 語彙/漢字` are image-only PDFs with no index, so I corroborated
   the 30 問題1–6 keys two other ways instead: every target resolves to
   `pools.json` (whose vocabulary/kanji slices come only from those four volumes),
   and the register matches the archive — official 12/2024 問題1 tests
   優秀/迷った/背骨/実践/衣装 and 問題2 tests けいび/ひなん/うやまう/じゅこう/
   あつかましい, which brackets 代理/都会/彼岸/神経/見にくい and 基礎/量る/支援/休業/
   促進; official 12/2024 問題5-23 keys **徐々に** itself. The one target I could
   not corroborate from either direction is **彼岸** (culturally specific); it is
   pool-resolved and its 2×2 grid is official-shaped, so I did not fail it, but I
   did not page-verify it either.
3. **No seed replay** (§6.3, with the reason).
4. **`模範解答.html` / `詳細解説.json` do not exist yet**, so the
   模範解答↔問題冊子 option-sync surface could not be reviewed. It is correctly
   the next step after this report, and every option must be re-synced if F2 is
   applied.
5. Nothing else was skipped: steps 0, 1, 2, 2b, 2.5, 3, 4, 5, 6 and 6.5 ran on all
   101 items plus the four 例, on `言語知識・読解.md` `02a0e5c6a458`, `聴解.md`
   `fa8048345c4d`, `聴解スクリプト.txt` `fa4e9dbb44bf`, `test_spec.json`
   `3439adb9b493`, `logs/ledger.json` and `logs/topics.json`. Source shas were
   re-read after the walkthrough was written and had **not** moved, so no fixing
   pass edited underneath this review.

---

`QA: PASS`
