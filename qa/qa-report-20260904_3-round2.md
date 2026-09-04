# QA adversarial review — `20260904_3`, ROUND 2 (fresh eyes, final round)

Reviewed revision (sha1 over raw bytes, unchanged between start and end of this pass):

- `tests/20260904_3/言語知識・読解.md` = `9d6b5df9d918`
- `tests/20260904_3/聴解.md` = `2cf41b4a33e4`
- `tests/20260904_3/聴解スクリプト.txt` = `902a9288c0a5`

Reviewed 2026-09-05. Reviewer authored nothing in this test and did not perform
round 1 or the fix pass. Solved from `qa/20260904_3/keyless.md` (rebuilt at the
start of this pass from the shas above; re-hashed at the end — nothing moved).

---

## 1. Verdict

**QA: FAIL (3 findings, 2 automatic)**

Both automatic findings are **true blockers for THIS paper**, not notes for the
next one:

* **F1** puts an item on the paper that a candidate who has sat official
  7/2025 answers without reading it, and it reproduces that sitting's
  apparatus closely enough that it is a copyright/non-reproduction breach as
  well as a solvability one. It cannot ship.
* **F2** makes two of 問題3's five scored items the same listening. It is
  repairable by re-angling ONE item (5番), so it is narrower than F1, but it is
  a defect in the shipped paper, not a note.
* **F3** is a record defect in `logs/topics.json`, not in the paper. It does
  not block THIS paper from being correct, but it blocks the NEXT one, because
  the blueprint stage diffs against that row.

Both automatic findings are **new since round 1** and both are **landing sites
of round-1 repairs** — F1 is where the re-authored 問題14 landed, F2 is a pairing
that the 聴解問題3-2番 re-angle left unexamined. This is the third consecutive
paper to show the repair-collateral class the skill names in §5.

**Everything round 1 asked to be re-verified independently came back clean.**
The blind solve is 101/101 for a third time, the 21-form grep is 0 hits, the
13-final closing column re-derives exactly as recorded, the 問題2 構成表 is
correct against the swapped script line-for-line, both `reauthored` stamps are
present and accurate in both files, and `script_sha` matches. The two findings
below are in places nobody was asked to look.

---

## 2. Blind-solve diff

Solved from **`qa/20260904_3/keyless.md`** and nothing else, all 101 items,
answers written down before opening any keyed file.

```
python3 tools/qa_eval.py tests/20260904_3 --answers "[...101...]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches.** Three independent blind solves have now returned 101/101 on
this paper; no key is in doubt on solvability grounds.

### The two blind STRATEGY passes (items 52–69, 問題10–13, n=18)

| strategy | this paper | official | cap |
|---|---|---|---|
| 1 — pick the option sharing the most passage character bigrams | **6/18 = 33.3 %** | 32.8 % | 45 % |
| 2 — pick the second-longest option | **6/18 = 33.3 %** | 24.6 % | 45 % |

Both inside the cap and inside the archive's own behaviour. Supporting
length measurements, computed by hand rather than read off the gate:

* (tied-)longest key rate **4/18 = 22.2 %** (target ≤35 %, official 30 %)
* **uniquely** longest key rate **4/18 = 22.2 %** (target ≤30 %, official 20 %)
* worst per-item option-length ratio **1.41** (item 63) — under the 1.65 WARN
  line and far under the 2.50 FAIL line
* one distractor scores 1.00 bigram overlap (item 63 option 2, a deliberate
  verbatim lift used as a TRAP) — the key at 0.67 sits below it, which is the
  right direction

---

## 3. Per-question walkthrough — all 101 items

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 4 | OK | 専門家=せんもんか。2×2 {せん,ぜん}×{か,け}; 家 has real 音 カ/ケ so 3 and 1 are same-kanji derivations, 2 is 専's 清濁 derivation. All four end in the printed form | — |
| 問題1-2 | 3 | OK | 投資=とうし。{とう,どう}×{し,じ}; 当時/同志/同時 are all real homophone words — the official 握手→拍手 pattern | — |
| 問題1-3 | 1 | OK | 父親=ちちおや。訓読み target so all four are real words (親父/父母/母親) as the 訓 rule requires; 親父 is the strong competitor. Weakest band item on the paper (父親 is an N4-frequency WORD) but the READING discrimination is genuine and official runs comparable targets (柱/収まった) | — |
| 問題1-4 | 2 | OK | 祖先=そせん。{そ,そう}×{せん,ぜん}, long/short + 清濁 | — |
| 問題1-5 | 2 | OK | 名物=めいぶつ。{めい,みょう}×{ぶつ,もつ}; 名 has both 音, 物 has both — a true 2×2 | — |
| 問題2-6 | 4 | OK | しおからい=塩辛い。{塩,潮}×{辛,幸}, all four share 送り仮名「い」 | — |
| 問題2-7 | 3 | OK | あんい=安易。{安,案}×{易,以}; 案 contains 安 as a component | — |
| 問題2-8 | 1 | OK | てきせつ=適切。{適,敵}×{切,設}; 適/敵 share the 音符 啇 | — |
| 問題2-9 | 4 | OK | げた=下駄。{下,外}×{駄,太}; both 下 and 外 are real ゲ, both 駄 and 太 answer た | — |
| 問題2-10 | 1 | OK | みて=診て。「医師が…けがを」 selects 診る over 看る(nursing)/観る(spectating)/見る(generic); all four share 送り仮名「て」 | — |
| 問題3-11 | 4 | OK | 各分野。「一人ずつ」 requires enumerable individual fields; 両=two only, 総=whole, 別=separate | — |
| 問題3-12 | 1 | OK | 他人。All four attach to 人 (他人/外人/個人/当人) — a clean same-family set; 「自分の失敗を」 fixes the axis at 自分以外 | — |
| 問題3-13 | 3 | OK | 共同。一同/賛同/共同/異同 all real; 「兄たちは…店を開いた」 requires joint action | — |
| 問題4-14 | 1 | OK | 進化。「長い年月をかけて…環境に合うように」 is the definition of 進化; 消化/強化/老化 all real 〜化 nouns, same category | — |
| 問題4-15 | 3 | OK | 本来。「好む…生き物だ」 is a timeless property, not a time point; 今後/現在/従来 all anchor to a time | — |
| 問題4-16 | 2 | OK | つぶして。「ゆでたじゃがいも…バターと混ぜて」 selects crushing; こわす/けずる/やぶる are the wrong destruction manner | — |
| 問題4-17 | 3 | OK | にくらしくて。「一度もあやまらない彼の態度」 is other-directed irritation; はずかしい self-directed, なつかしい nostalgic, そうぞうしい auditory | — |
| 問題4-18 | 1 | OK | 手をつけ。「レポートにまだ…ていない」 = not yet started. All four are 手 idioms — the strongest option set on the paper | — |
| 問題4-19 | 4 | OK | 現に。「話は本当で、（　）昨日から半額の札が出ている」 — evidence for a claim just asserted; いまに/まさか/むしろ do not take evidence | — |
| 問題4-20 | 3 | OK | かつて。「あった場所だ」 = a past state no longer holding; さきほど is minutes ago, いよいよ/やがて point forward | — |
| 問題5-21 | 2 | OK | 粗末な→安っぽい。Substitution: 「兄はいつも安っぽい服を着ている。」 survives | — |
| 問題5-22 | 1 | OK | 悩んで→困って。「進路のことでずっと困っています。」 survives; あきれる/あせる/くやむ each add a component 悩む lacks | — |
| 問題5-23 | 4 | OK | 荒っぽい→らんぼうな。「らんぼうな運転をする。」 survives | — |
| 問題5-24 | 3 | OK | じたばたして→あわてて。「今さらあわてても結果は変わらない。」 survives; あきらめて inverts the meaning | — |
| 問題5-25 | 4 | OK | 慌ただしく→いそがしく。「年末はどこの店もいそがしくなります。」 survives; さわがしい is the near-miss (noise vs busyness), which is the tested discrimination. Options are ordinary words by design — the N2 item is the STEM's 慌ただしい | — |
| 問題6-26 | 4 | OK | 手際=仕事の運び方の巧みさ。「新しい店員は手際がよく、注文の品をすぐに出してくれた」。1 wants 手間, 2 wants 手順, 3 applies a person-word to a machine — three different learner errors, not one | — |
| 問題6-27 | 2 | OK | 消耗=使われて力や量が減る。「体力をすっかり消耗してしまった」。1 wants 消費, 3 wants 摩耗, 4 wants 使い切る | — |
| 問題6-28 | 2 | OK | 脱線=進んでいる筋道からそれる。「部長の話は途中で脱線して」。1 wants 逸脱, 3 wants あふれる, 4 is not a collocation at all | — |
| 問題6-29 | 1 | OK | 取り組む=課題に向かって努力する。「安全の問題に真剣に取り組んでいる」。2 wants 取り入れる, 3 wants 組み立てる, 4 wants 詰める | — |
| 問題6-30 | 4 | OK | 強化する=備えを強くする。「火事を防ぐための点検を強化する」。1 wants 強調, 2 wants 強まる, 3 wants 上達する | — |

**Two stem counts, printed as §3 requires:** 問題1/2/5 comma-free stems
**15/15 = 100 %** (author floor ≥9; official runs 47–93 %, so this is one stem
ABOVE the archive's observed ceiling — noted in §6, not filed); 問題1–5
です・ます stems **7/25**, exactly the author target, inside official's 2–11.
Stem lengths 15–19 JP chars, median 16, inside the archive's 15–21.5.

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 | OK | 〜抜きで=本来あるはずのものを省いて。「堅苦しいあいさつ抜きで気楽に始めよう」 | — |
| 問題7-32 | 3 | OK | 〜をめぐって=ある事柄を中心に争い/議論が起こる。「計画をめぐって、住民の間で意見が分かれ」 | — |
| 問題7-33 | 4 | OK | 〜かねる=丁寧な不可の断り。「ご本人の署名がないものは、お預かりいたしかねます」 | — |
| 問題7-34 | 3 | OK | 〜たとたん=その瞬間に。「外に出たとたん、大粒の雨が降ってきた」 | — |
| 問題7-35 | 4 | OK | 〜かねない=好ましくないことが起こりうる。「信頼関係まで一度に失いかねません」 | — |
| 問題7-36 | 2 | OK | 〜までして=極端な手段を取ってまで。「行列までして食べたい物ではない」 | — |
| 問題7-37 | 3 | OK | 〜だらけ=好ましくないものが一面に。「間違いだらけの答案」; まみれ needs a liquid/powder | — |
| 問題7-38 | 1 | OK | 〜と仮定すると=仮の場合を置く。「減り続けると仮定すると…計算になる」 — the 計算になる tail is what forces a hypothetical, not a discovery (かと思うと) | — |
| 問題7-39 | 1 | OK | 〜まい=打ち消しの推量。「あれだけ心配していたのだから、父も今さら怒るまい」 | — |
| 問題7-40 | 4 | OK | 〜限りは=その条件が満たされている間は。「働いている限りは、年齢や職種にかかわらず使うことができる」 | — |
| 問題7-41 | 2 | OK | 〜たきり=その後次の動作が起こらない。「去年の春に借りたきり、一度も開いていない」 | — |
| 問題7-42 | 2 | OK | 〜というものだ=当然の評価の言い切り。「いくらなんでも酷というものだ」 | — |
| 問題7 distribution | — | OK | Gate's own measure: **mean 45.5 (band 36–52), 2 stems under 34 (need ≥2), spread 37 (need ≥25)**. Four dialogue/setting-label stems (33,34,36,41) — official always carries some | — |
| 問題8-43 | 1 | OK | 3→2→**1**→4. 「のみならず」 needs a noun-clause left and 「にも」 right; 4「ことが…強みだ」 must be final and needs a 連体 form, which only 開かれている supplies. One grammatical order | — |
| 問題8-44 | 1 | OK | 2→3→**1**→4. 「かどうかを」 needs a clause left (音が出る) and a transitive right (確かめてみない); 4 must be final | — |
| 問題8-45 | 2 | OK | 1→3→**2**→4. 「多い一方で」 needs a が-subject, only card 1 supplies one; 4 ends in そうだ so it is final and needs a 連体, which only 出る supplies. **Zero-anaphora check (the 20260827_2 class): 「朝の客が」 is a bare が-card, so I tested every later predicate — 出る already has its own が-subject (売れ残りが) and 少なくない takes こと. It can only bind 多い. No second free pre-predicate unit** | — |
| 問題8-46 | 4 | OK | 2→1→**4**→3. 「地域の」 ends in の so a noun must follow (マラソン大会); 「ようになった」 must be final and needs 辞書形 (走る) | — |
| 問題8-47 | 2 | OK | 1→3→**2**→4. 「体によくないと」 is quotative and needs 分かり; 「くせだけは直らない」 must be final and needs a 連体 (食べる) | — |
| 問題9-48 | 4 | OK | [論理接続] 「これに対し」。Before: park leaves become soil. After: 「同じ並木でも…燃やすごみとして運ばれていく」 — a contrast, not addition/example/consequence | — |
| 問題9-49 | 2 | OK | [文末モーダル] 「土になるはずもなく」。Decider is the immediately preceding 「舗装の上には、その生き物がいない」 — no decomposers means no possibility, so only the strong negative fits. Note: two of the four options carry はず, so the form itself carries no discriminating information (the tested element is もない) | — |
| 問題9-50 | 2 | OK | [慣用・形式名詞] 「本末転倒」。「土に返そうとして…排水口を詰まらせるようでは」 — means defeating the end | — |
| 問題9-51 | 3 | OK | [内容推論] 「同じことが言える」。The whole essay says the outcome is set by what is underneath; the 根元に土を残す工事 paragraph is the same principle applied to 落ち葉の始末 | — |
| 問題9 categories | — | OK | Four distinct tags (論理接続 / 文末モーダル / 慣用・形式名詞 / 内容推論); no two blanks share one. Options max 16 JP chars. Cloze body ≈700 JP chars | — |

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 2 | OK | 「町の答えは、批判が見こんだ路線バスの代わりではなく、たたまれた路線の跡を細く埋めなおす乗り物として使う、ということである」 | — |
| 問題10-53 | 3 | OK | 「作り直しを協会にお願いできるのか、宿がそれぞれで用意してよいのか、お教えください」 — the email ASKS, so option 1 (「そのまま張り替えてよいか」) is a different question | — |
| 問題10-54 | 3 | OK | 「引っ越してきた世帯が、地区の中で名前を覚えてもらえる機会が、そこにしかなかったのである」; option 1 is denied by 「結びつきはなかった」, option 2 by 「効いていたのは道具ではなく」 | — |
| 問題10-55 | 1 | OK | 「組合が費用を病院へ直接お支払いする形に改めます」＋「窓口では残りの分だけをお支払いいただくことになり」 | — |
| 問題10-56 | 2 | OK | 「この十五年で変わったのはこちらの手のほうで、私が惜しんでいるのはその変わり方なのだと気がついた」; option 1 is explicitly refused by 「物を大事にしているのだと言われると、少し違う気がする」 | — |
| 問題11-57 | 1 | OK | 「「本当かどうかは分からなかった」と答える人が半分近くいた」＋「分からないまま回していたのである」 | — |
| 問題11-58 | 4 | OK | 「必要なのは、人を賢くする工夫よりも、押す手つきに数秒割りこむ仕掛けだと私は考えている」 | — |
| 問題11-59 | 3 | OK | 「問われるのは、一キロあたりの値段と、年間を通じて同じ量を出せるかどうか、その二つです」 | — |
| 問題11-60 | 2 | OK | 「この話は性質の違う二つに分かれます」＋「別の指標で測るべき事がらです」 | — |
| 問題11-61 | 3 | OK | 「紙の案内は、会があることと、いつ開くかは伝えます。けれども、そこが自分の入ってよい場所かどうかまでは伝えません」 | — |
| 問題11-62 | 3 | OK | 「体育館の奥をやめ、公民館の玄関わきの広間で開くことにしました」＋「その場で手ほどきを受け、一度投げてみます」 | — |
| 問題11-63 | 1 | OK | 「決まった時刻に教室へ出向かなくてよい。分からないところは何度でも巻き戻せる」 — the 値打ち the author FELT, before the reversal. Option 2 is a verbatim passage lift used as a trap (it is what actually worked, not what he valued) | — |
| 問題11-64 | 3 | OK | 「動かせない一点があると、その週の段取りはそこから組み立てられます」 | — |
| 問題12-65 | 3 | OK | A: 「大人がその同じものについて言いかえしているかどうか、という条件である」; B: 「子どもが何かをした直後にそれをことばで受け止める場面が入っていなければ、覚えは進みにくい」 | — |
| 問題12-66 | 2 | OK | A: 「量の多さは、この機会の数をふやしやすいという形で効いている」; B: 「数は、場面が生まれるための土台として要るのです」。Option 3's 「Bは量には関わりがない」 is exactly what B calls 行きすぎ | — |
| 問題13-67 | 3 | OK | 「それぞれに書類と面談があり、それぞれが娘の状態を最初から聞いてくる」＋「経管栄養の手順を、私は同じ言い方で八回説明した」; option 2 is denied by 「冊子の制度の多くは、たしかにこの町にもあった」 | — |
| 問題13-68 | 4 | OK | 「八つの窓口は、それぞれの所管の中できちんと働いていた。それでも、八つをつなぐ仕事だけが、どこの持ち場にも入っていなかった」 — which also kills option 2 | — |
| 問題13-69 | 2 | OK | 「私が同じ話をする回数は八回から一回に減り、制度は一つも増えていない」＋「そこは数を足しても埋まらない」 | — |
| 問題14-70 | 1 | **自動不合格** | Key sound in isolation and combines ≥2 constraints (Sat-afternoon/Sunday availability × 実習あり: ②Sat 13:30 実習, ⑤Sun 実習; ④ dies on 「実習はありません」, ①③ on Sat morning). **But the whole 大問 is a near-verbatim reproduction of official 7/2025's 問題14 — see F1.** Official's own 70 is 「前田さんは…午前中に行われる講座で、講義だけではなく実習もある講座がいい。前田さんの希望に合う講座はどれか。」 — the same two-constraint pair (time-of-day × 実習) on the same document, answered by the same two-circled-number option form | Re-author 問題14 onto a different document genre and a different decision mechanic — see F1 |
| 問題14-71 | 3 | **自動不合格** | Key sound in isolation and combines ≥2 constraints (受付期間 12/15–1/5 passed → late route 「開講の五日前」 = 1/13, × method 「先にお電話で空きをお確かめください」). **But the stem is official 7/2025's stem with the name, the circled number and the date swapped, and the option grid is official's {early date, late date} × {method A, method B}** — see F1. Measured longest shared run against `tests/imported-n2-2025-07`: **21 chars**, 「さんはどのように申し込まなければならないか」, against 10–13 for every other paper on disk | as F1 |
| 問題14 apparatus | — | **自動不合格** | 0 （注N） ✓ (verified by hand, as asked). But: five ①〜⑤ courses in a 4-column table (講座/内容/日時/受講料 vs official's タイトル/講座内容/日時/受講料), exactly one course with no 実習, 定員+抽選, a 受付期間 split into ①② / ③④⑤ at the same place, and a "past the deadline you may still apply until N days before 開講; phone to check" late route — official 7/2025 has every one of these | see F1 |

**読解 apparatus, counted by hand:** 32 in-body （注N） markers across 問題10–13
against 32 definition lines (**0 orphans**, floor 25, target 30–40); 問題12 and
問題14 carry ZERO, as official does; distribution 問題10 5 / 問題11 20 / 問題13 7.
**No gloss on a basic or standard word** — all 32 headwords are N1/rare/
specialized/metaphorical (過疎, 逐語訳, 魚粉, 呼び水, 経管栄養, 所管…); 転送 and
動機 are the two borderline entries and both are used in a technical sense.
**0 `<ruby>`**, **3 （中略）** all inside 問題11–13 passages, marked span ①
matches its stem 1-to-1 in 問題13.

### 聴解

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 3 | OK | 「部屋を何時から何時まで使えるか、公民館で確かめてきてくれる」→「わかりました。今から行ってきます」。Announced 例 number = 3, matches the pre-marked grid | — |
| 問題1-1番 | 4 | OK | 「その方をどの部屋にお通しするかが、まだ決まってなくて。課長に聞いておいてくれる」→「今日中にうかがいます」。1 ✗「先月まとめて注文してあるから、当分足りるよ」/2 ✗「毎朝、田口さんが開けて回ってくれてるんだ」/3 ✗「去年から使ってないんだよ」 | — |
| 問題1-2番 | 4 | OK | 「中くらいのを二つに分けて入れて、お代は大きいサイズの分だけいただこう」。1 ✗「量が半分近くになっちゃうから…出せないよ」/2 ✗「氷の量を変えるときの決まりだから、今はしなくていいよ」/3 ✗「中くらいのには合わないんだ。二重にはできないよ」 | — |
| 問題1-3番 | 1 | OK | 「お子さまの健康の記録を、必ずお持ちください」＋「来られた方ご自身の身分証も、お一人ずつ拝見しております」。2 ✗「今年からは要らなくなりました」/3 ✗「こちらで保管しております」/4 ✗「ご自宅でのご用意は要りません」。The paper's one non-dialogue item (自動音声案内), 16 % of official 問題1 | — |
| 問題1-4番 | 3 | OK | 「まず、その方が働き始める日を、はっきり決めてください」＋「そこが決まらないと、ほかは何も進みません」。1 ✗「日にちが決まってから、用紙といっしょにお渡しします」/2 ✗「まとめては出せないんですよ」/4 ✗「今はまだ大丈夫です」 | — |
| 問題1-5番 | 4 | OK | 「階段を下りた小ホールにお入りください」。1 ✗「早めにお申しこみになった二百名までで、もう埋まっております」(she applied しめ切りの二日前)/2 ✗「第三校舎は、今回は使っておりません」/3 ✗「二級の方はお入りになれません」 | — |
| 問題2-例 | 4 | OK | 「十枚で八千円なんです」＋「当日、券売機でもお求めになれますし」。Announced 例 number = 4, matches the grid | — |
| 問題2-1番 | 1 | OK | 「三日前までにお知らせいただければ、減らしたぶんのお代はちょうだいしません」。2 ✗「当日は増やせないんです」/3 ✗「一週間前ではなく、十日前までに」/4 ✗「この日はもう入っておりまして」 | — |
| 問題2-2番 | 2 | OK | 「四時に来られる人が何人いるか分からないと、いすを並べる係も…決められないんだ」＋「まず、四時に行ける人を数えなきゃだね」。1/4 ✗ assigned to others, 3 ✗「決まってるよ」 | — |
| 問題2-3番 | 2 | OK | 「少し間を空けてから見直したほうが、あとまで残る」＋「忘れかけたころに見るのが効くって」。1 ✗「説明する相手がいなくて」/3 ✗「朝はもともと勉強してるから、そこは変えなくていいかな」/4 ✗「今のままで困ってないし」 | — |
| 問題2-4番 | 1 | OK | The swapped 気持ち item. 「お部屋でのお夕食は、この時季はお受けしておりませんで」＋「そのお席は、五時半にお入りいただく回だけに」＋「部屋でゆっくり、というわけにはいきませんけど…かえってそのくらいがちょうどいいのかもしれませんね」。2 ✗「子どもが少しぐらい騒いでも平気ですね」/3 ✗ the same 「かえって…ちょうどいい」 line/4 ✗「日をずらさなくてもすみますし」. **Valence is 納得・割り切り, not 安心; the key carries neither 「安心」 nor the 「よかった。」＋「〜と思ってた」 opening that 20260904_2's 2-6番 used. Verified against both papers' scripts** | — |
| 問題2-5番 | 3 | OK | 「あそこは屋根の下で…雪の日でも車を出せます」＋「西側の置き場は屋根がなくて、朝、雪をおろしていただくことに」。1 ✗「どの置き場にお返しになってもけっこうです」/2 ✗「家からは西のほうが近いんですけど、そこは我慢します」/4 ✗「延長は、どちらの置き場でも、同じように」 | — |
| 問題2-6番 | 1 | OK | The swapped 在宅勤務 item. 「用紙を受け取ってから、実際に始められるまで、二週間ほどいただいております」＋「その順番待ちで」。2 ✗「週ごとに変えていただいてかまいません」/3 ✗「今はいただいておりません」/4 ✗「月に一度、まとめて出していただく形に」 | — |
| 問題2 構成表 | — | OK | **Re-derived independently against the script as it now reads.** 決め手の位置 fractions all correct, counting SPOKEN lines only: 例 9/13, 1番 4/15, 2番 9/12, 3番 3/13, **4番 7/11 = 0.636 ≤ 2/3 → 中盤 ✓**, 5番 6/12, 6番 3/14. Thirds 冒頭3/中盤2/終盤2, none over 3. 決め手の種類 ≤2 per token (時刻・日程 2 = 3番/4番, rest 1); the one pair at the cap differs on 質問型 (どうして / 気持ち). 質問型 内容・発言2 / どうして2 / 一番1 / 気持ち1, none over 3. Every 「…」 in the table traces to the current script (gate's `check_section_table_quotes` agrees) | — |
| 問題3-例 | 2 | OK | 「原因をうかがう前に…日にちを先に申し上げなさい」。Announced 例 = 2 ✓ | — |
| 問題3-1番 | 2 | **要修正** | Key correct: 「会議が何時に終わるか読めないから、届く時間がずれると困る」＋「次の月から、まとまった注文が二倍になりました」。Distractors all 周辺, none named by the talk. **But this item and 3-5番 run the same errand — see F2** | Leave 1番; re-angle 5番 (F2) |
| 問題3-2番 | 3 | OK | The re-angled item. 「血圧や血液の細かい数字に目を通すのは、産業医と保健師の二人だけです」＋「人事部に届くのは、だれが受けて、だれが受けていないか、その名前の一覧だけです」。Gist is now 結果の取り扱い, not 手続きの変更 — verified against the script, and no longer echoes 問題10(4)'s 「組織が手続きを改める」 move. 「変え」 now occurs in exactly one of 問題3's 24 spoken options (3番's key), re-counted by hand | — |
| 問題3-3番 | 4 | OK | 「昔は…仕事の中身で人を分けていました」＋「今は分け方を変えました。会場を、入り口から順に四つの区画に切って」 | — |
| 問題3-4番 | 1 | OK | 「お手持ちの券に書かれた番号と同じ入り口からお入りください」＋「明るさを上げておいていただけると助かります」 | — |
| 問題3-5番 | 3 | **要修正** | Key correct: 「始める前、いちばん心配していたのは、届ける人手でした」＋「ところが、困ったのは、そこではありませんでした」＋「届けている間に、温かいものは冷め…」. **Same errand as 3-1番 — see F2** | Re-angle this item's talk and key off "a food retailer discovers the real obstacle was delivery timing" — see F2 |
| 問題3 column read | — | OK | Spoken options read as one column: no content token occurs in ≥2 keys and 0 distractors. 「会場」 spans 3番's key and 4番's key but also 3番's options 2 and 3. 「届」 spans 5番's key and 5番's option 2. Talk lengths 272–297 chars, all inside the 220–300 target | — |
| 問題4-例 | 1 | OK | 「明日の練習、六時からだったよね」→ confirmation | — |
| 問題4-1番 | 2 | OK | 「耳が痛い」(idiom)→「私も、人のことは言えないよ」。1 takes the idiom literally, 3 drifts to wake-up time | — |
| 問題4-2番 | 2 | OK | 「領収書はこちらでよろしいでしょうか」→「日付が入ってるか、見てくれる」(superior, plain). 1 inverts the roles, 3 asserts completion | — |
| 問題4-3番 | 3 | OK | 「ご存知ですか」→「実は、まだ教わっていなくて」. 1 inverts the role, 2 drifts to collection day | — |
| 問題4-4番 | 1 | OK | 「心当たりはありますか」→「もしかして、かぎじゃないですか。見てみます」. 2 is the finder's line, 3 assumes a false premise | — |
| 問題4-5番 | 2 | OK | 「お言葉に甘えて」→「そうしなよ。無理して早く来ることないって」. 1 takes 甘えて as sweets, 3 changes the addressee | — |
| 問題4-6番 | 3 | OK | 「この先は工事中で、通れません」→「じゃあ、遠回りですね。どちらへ回れば」. 1 asserts a false premise, 2 inverts the role | — |
| 問題4-7番 | 1 | OK | 「少々お待ちいただけますでしょうか」→「どのくらい待ちますか。ほかに用があるもので」. 2 inverts the role, 3 is the wrong tense | — |
| 問題4-8番 | 1 | OK | Re-written key. 「新幹線のチケットを手配しておきましょうか」→「今回は車で回るので、切符はけっこうです」 — a reason-plus-decline, matching the offer's plain-polite register. 2 is the offerer's line, 3 drifts to speed | — |
| 問題4-9番 | 3 | OK | Re-written key. 「明日までにこちらのデータをご確認いただけますでしょうか」→「もとの資料もいただければ、確認できます」 — accepts conditionally. 1 is the wrong tense (来月), 2 drifts to how to write a request | — |
| 問題4-10番 | 1 | OK | 「思ったより反応がよくてびっくりしたよ」→「ほんとだね。第二弾も考えてみようか」. 2 inverts the premise, 3 drifts | — |
| 問題4-11番 | 1 | OK | Re-written key. 「もう一度検討してみます」→「うん、ただ、値段は動かさないでくれるかな」 — superior accepts and sets one limit; keigo direction correct (subordinate 謙譲 up, superior plain down). 2 mistakes the object, 3 is the wrong tense | — |
| 問題4 register | — | OK | 3 casual / 2 keigo prompts among the drawn 11; every prompt has a definable responder (no announcement-with-no-addressee); 0 replies open on はい/いいえ/では | — |
| 問題5-1番 | 2 | OK | 「ご予約のお電話をいただいたときに、こちらが持ち物を読み上げて、その場で言っていただくのはどうでしょう」→「予約の電話は、必ずご本人からかかってくるものね。それなら、全員に届くわ」「そうしましょう」。1 ✗「直せるのは来年の分から」/3 ✗「電話をかけられる人がいないの」/4 ✗「受付を通らずに、そのまま二階の教室へ」 — and all three also die on the stated criterion 「ご自分では読んでいない」 | — |
| 問題5-2番 質問1 | 4 | OK | 男: 「スマホはほとんど見ないんだよね。だから、いちばん安いシンプルでいいや」. 3 ✗「おまとめは、三回線以上からとなっておりまして」 | — |
| 問題5-2番 質問2 | 1 | OK | 女: 「そうだね。じゃあ、私はたっぷりにする」. 2 ✗「私、一日中うちにいるんだった。それじゃ意味ないね」/4 ✗「家で動画の教材、毎日流してるじゃない」 → 「量が足りなくなるね」. **Actors verified against the script in both directions** — the man takes シンプル, the woman takes たっぷり, and `logs/topics.json`'s `surfaces` and `claim` rows say the same (the 20260903_1 actor-swap class does not recur here). No deciding attribute is printed beside an option name; both questions enumerate in spoken order | — |

---

## 4. Findings

| id | item | class | evidence | status |
|---|---|---|---|---|
| **F1** | 問題14 (flyer + 70 + 71) | **自動不合格** — apparatus and both stems reproduced near-verbatim from an official sitting (`tests/imported-n2-2025-07` = `refs/JLPT_N2_NEW/16. N2 7-2025`); "reference material is calibration only" | Longest shared run **21 chars**: ours 「川上さんは、この案内を見て⑤の講座を受けたいと思った。今日は一月十一日である。川上**さんはどのように申し込まなければならないか**」 vs official 「ニコラスさんは公開講座の案内を見て、④の講座を受けたいと思った。今日は12月3日である。ニコラス**さんはどのように申し込まなければならないか**。」 — the same sentence with the name, the circled number and the date swapped. Every other paper on disk measures 10–13 against the same corpus. **The run understates it; the whole item is the clone:** ① a 5-course ①〜⑤ 公開講座 notice in a 4-column table (講座/内容/日時/受講料 vs official's タイトル/講座内容/日時/受講料); ② exactly one course with no 実習 (ours ④「実習はありません。」, official ②「②以外の講座では…実習も行います」); ③ 定員 + 抽選; ④ **a 受付期間 split into ①② and ③④⑤ at the same place** — a fingerprint, since nothing about a newly invented flyer requires a 2/3 split there; ⑤ the late route 「受付期間が過ぎても…開講の五日前まで受け付けます。この場合は、先にお電話で空きをお確かめください。」 vs official 「申し込み受付期間が過ぎている場合でも、定員に達していなければ講座開始の3日前までなら申し込み可能です。電話でご確認ください。」; ⑥ Q70 = time-of-day × 実習 → two circled numbers (official 「午前中に行われる講座で、講義だけではなく実習もある講座がいい」 / ours 「土曜日は昼まで別の用事があるが…実習のある講座を選びたい」); ⑦ Q71's option grid = {earlier date, later date} × {method A, method B} (official 12月5日/12月7日 × ホームページか電話/電話; ours 一月十三日/一月十五日 × 電話/窓口), key 4 there and 3 here | **FIXED** 2026-09-05 (round-2 direct-fix pass) — 問題14 re-authored onto a shelter-facility comparison table (`東野市防災課　指定避難所のご案内`), a document type and a decision mechanic official 7/2025 does not use: no 講座, no 受付期間, no 抽選, no late route, no application method. 70 is a choice item keyed on 段差 × ペット across two table cells; 71 is an action item keyed on 「避難所に着いたら受付でお申し出ください」 × 「一回三十分をめやすに、次の方と交代でお使いください」, both constraints load-bearing. 0 （注N）, keys 1/3 as `answer_positions` says. THREE-CORPUS SHARED-RUN SCAN of the replacement (same scanner, which reproduces this row's 21-char measurement on the pre-fix text exactly): **9** vs the 31 `refs/JLPT_N2_NEW/*/booklet.md` (「はどうすればよいか」), **7** vs the 10 `tests/imported-*` (「ではありません」), **12** vs the 22 other generated papers (「受付でお申し出ください。」, 20260813_1). |
| **F2** | 聴解問題3-1番 & 3-5番 | **自動不合格** — two 聴解 items running the same errand (§5) | Both are a small **food-retail owner** speaking at a **講演会/講座** who narrates *the constraint I worried about was not the real one; the real one was the timing of getting food to the customer*. 1番: 「味をよくすれば選んでいただけると思って、材料にばかりお金をかけていました。でも、注文は増えませんでした」→「届く時間がずれると困る」→「決めた時刻の三十分前から、そのあと三十分の間なら、いつでもお渡しできます」→ orders doubled. 5番: 「いちばん心配していたのは、届ける人手でした。ところが、困ったのは、そこではありませんでした」→「ご注文の多くが、夕方の同じ時間に集まる」＋「届けている間に、温かいものは冷め」→ on-board heater + cold boxes → 「店で買うのと変わらない」. Both tagged **食** in `logs/topics.json`, the only theme to appear twice in 問題3. **Widened**: 例 and 3番 run the SAME arc (「以前は原因を先に聞いていた→日にちを先に伝える→声が落ち着いた」; 「昔は仕事の中身で人を分けていた→区画で分けた→二時間早くなった」), so **4 of 6 問題3 talks are one template**. Measured against official 7/2025's 問題3: 一人旅のよさ / 木の家具の魅力 / 店をやる喜び / 良い睡眠の条件 / ロボットの活用 — **1 of 5** on a problem→solution arc, five distinct shapes. This is the class the skill records for 20260904_1 (「以前は加工していた→そのまま通した→そのほうが効いた」 twice) | **FIXED** 2026-09-05 (round-2 direct-fix pass) — three talks re-angled off the shared arc, drawn scenarios and key positions untouched: 例 → 〈自分の方針とその理由の説明〉 (key unchanged), 1番 → 〈条件の提示〉 re-keyed to 「会社からの注文を受ける店に要ること」 (option 2), 5番 → 〈これから始める人への助言〉 re-keyed to 「始める前にやめる目安を決めておくこと」 (option 3). 3番 keeps 以前→変更→効果 and is now the only talk on it. COUNTED BY HAND over all six talks: 方針の説明 / 条件の提示 / 範囲の説明 / 以前→変更→効果 / 注意の案内 / 助言 — **one row each**, i.e. at or below official 7/2025's 1-of-5. The arc is now a printed 問題3 構成表 column. Both re-keyed scenarios carry `"origin": "reauthored"` in spec AND ledger with the new deciding lines quoted. `make mp3` re-run (script_sha 17885d021b1d). A first draft of 5番's key contained 「やめ方を」 and tripped `check_choukai_key_exclusive_token` against 3番's 「分け方を」 (「方を」 ×2, both keys) — caught by the gate and re-keyed to 「やめる目安を」; the check now reads `ok`. |
| **F3** | `logs/topics.json` → `20260904_3.notes` | **要修正** — the row quotes strings the fix pass removed (`notes` verifiability rule; the 20260817_3 precedent) | The `notes` field is Stage 3's and was never updated by the fix pass. `grep -c` over the shipped sources returns **0** for every one of these strings it quotes as present: 「決めた会ほど、一年後まで残っている人が多いのです。」 (asserted to be 問題11(3)'s closing — the shipped closing is 「人の通り道に道具を出して開いた会ほど、初めて来た方がその日のうちに輪を投げてみた例が多いのです。」), 「うまくなった人」 (asserted repair of 問題11(3)), 「市内にご在住の方も」 (asserted repair of 問題14), 「市防災課」, 「みなと市」 (asserted to be this paper's invented place name — the shipped paper's only invented name is みどり市, in the 聴解 script). The headline audit likewise reads 「問題14 はみなと市の避難所運営訓練」; the shipped 問題14 is 東野防災学習センター's 公開講座. **The note's CONCLUSIONS still hold** (I re-derived the 21-form grep myself: 0 hits), but its EVIDENCE is a description of a paper that no longer exists, in the file the next paper's blueprint stage reads | **FIXED** 2026-09-05 (round-2 direct-fix pass) — the `notes` field is rewritten end to end against the shipped bytes, and the five quoted strings are gone from it as quotations (they are named in backticks as the strings the finding was about). The same predicate this row proposes was run locally over the row's `notes`, `surfaces`, `claim` and `shapes`: **0** 「…」 spans of ≥8 JP chars fail to occur in `言語知識・読解.md` or `聴解スクリプト.txt`. Two pre-existing spans of the same class were repaired with it — `claim/聴解問題5-2番` 「家にワイファイがない」 → 「ワイファイがないんだから、全部スマホの回線だよ」 and `shapes/聴解問題5-1番` 「本人が読んでいない」 → 「ご自分では読んでいない」. The proposed gate check itself was NOT implemented; the orchestrator owns it. |

### Things round 1 asked me to re-adjudicate, and things I re-derived rather than inherited — all clean

| asked | independently re-derived | verdict |
|---|---|---|
| Full 21-form keyed-grammar frame grep across the whole 読解 half | Scoped to 問題10–14 passage prose **plus （注N） definition lines plus the 問題14 table rows**; each form matched as its whole keyed string, per the rule's own frame semantics | **0 hits.** Two raw substrings exist and neither is a hit: (a) 「きっかけ」 ×1 in 問題11(4)'s 「（注3）動機：…気持ちのきっかけ」 — a bare predicate noun, not 問題8-46's 「Nをきっかけに」 frame, and 1 ≤ 1 anyway; (b) 「はず」 ×2 in 問題11(4) 「ありがたかったはずの講座」/「自由に選べるはずの形」 — both **連体**, while 問題9-49 keys the **文末** negative 「〜はずもない」, and the exclusion for a form carried by two of the item's own options applies as well (49's options 2 and 3 both carry はず). The fix pass reported "all 21 at 0"; the correct statement is 0 hits over 3 raw occurrences, all excluded on stated grounds |
| Re-derive the 13-final closing column BY SENTENCE, confirm the closed vocabulary and ≤2 per shape | Extracted the 13 closings with `dokkai_closing_scopes()` and labelled each from its own final two sentences against `dokkai.md`'s six shapes + the two mechanical overrides | **Matches the record exactly.** 説明 2 (問題9, 問題11(2)) / 反論応答 2 (問題10(1), 問題12(B)) / 実用文・分類外 2 (問題10(2), 問題10(4)) / 意外な観察 2 (問題10(3), 問題11(4)) / 主張 2 (問題11(1), 問題13) / 条件提示 2 (問題11(3), 問題12(A)) / 随筆 1 (問題10(5)). All seven values are in `CLOSING_MOVES`; nothing exceeds 2 |
| Confirm round 1's ruling that 問題12(A) is 条件提示, not the coin-flip 説明 (which would put 説明 at 3) | Re-read it cold. The passage frames its own content as a condition (「もう一つの条件が残る」「…という条件である」), the closing states the condition and its relation to quantity with **no exhortation**, which is 条件提示's definition; 説明 is "explains a mechanism/distinction and stops there" and the final sentence alone does read that way | **Confirmed 条件提示**, and the pair is safe for a second reason round 1 did not give: **the two 条件提示 closings do NOT share a sentence template.** 問題11(3)'s final instantiates `A では/ほど B が多い（相関）` (「…開いた会ほど…例が多いのです」); 問題12(A)'s final is 「量の多さは、…という形で効いている」 and matches no template. `dokkai.md`'s "the two sharing a shape must also differ at the SENTENCE-TEMPLATE level" is therefore satisfied, which is what makes the 条件提示 call safe regardless of how the coin lands |
| Read the 13-final column a second time down the SKELETONS (the `20260904_1` F2 class) | Ran `FINAL_SENTENCE_TEMPLATES` over the finals, then read the column by eye | `〜のは A ではなく B` ×1 (問題10(1)), `A では/ほど B が多い` ×1 (問題11(3)), everything else 0. By eye, **three** finals embed a のは/のが cleft (問題10(5), 問題11(1), 問題13) but none CLOSES on it — each continues into a different matrix predicate (「…と気がついた」/「…と私は考えている」/「…であって、そこは数を足しても埋まらない」), so the 分裂文 template does not fire. Deliberate variation, not a pile-up |
| Re-check every 解説 and 構成表 cell citing a changed item, incl. the 問題2 n行目／全m行 fractions | Counted spoken lines in every 問題2 block by hand against the swapped script | **All seven fractions exact** (例 9/13, 1番 4/15, 2番 9/12, 3番 3/13, 4番 7/11, 5番 6/12, 6番 3/14) and every label follows from its own fraction, including the boundary case 4番 at 0.636 ≤ 2/3 → 中盤. 決め手の種類 and 質問型 columns re-derived and correct; 6番's 設備・故障 leans on the CAUSE of the two-week wait (「貸し出しのパソコンに…設定をするんですが、その順番待ちで」) rather than the stated interval, which is defensible and is what keeps 時刻・日程 at 2 rather than 3 — flagged as a judgment call, not a finding |
| `script_sha` matches the script on disk | Gate line, re-read | `ok 20260904_3: 聴解.mp3 was built from today's 聴解スクリプト.txt (script_sha 902a9288c0a5)` = the sha I hashed myself. Artifact mtimes also order correctly: md 04:59/05:00 → html 05:02 → mp3+chapters 05:03 → sheet 05:03 |
| Both `reauthored` stamps present and accurate in spec AND ledger | Diffed all 11 categories field-for-field and read both notes against the script | **Byte-identical in all 11 categories.** Both stamps present in both files, on `listening_scenarios` 「人事部からの健康診断のお知らせ」 and 「旅館:食事場所の希望確認」. Every line each note quotes verbatim IS in the current script. **And the absence of any `reading_topics` stamp is correct, not an omission** — 問題11(3)'s re-angle moved it TOWARD its drawn topic 「高齢者向け軽スポーツの**普及**」, and the re-authored 問題14 lands squarely on its drawn topic 「避難所運営における多様性への配慮」 (theme 防災). Neither changed WHAT its surface tests |
| 問題14 longest shared run vs both previous papers (fix pass claimed 10) | Re-measured with LCS after stripping whitespace, markup and the mandated 大問 instruction | **Confirmed: 10 chars vs `20260904_2`** (「。【当日のご案内】・」) **and 10 vs `20260904_1`** (「）13:30〜15:」). Round-1 F2 is genuinely repaired. **But the fix pass compared against generated papers only** — extending the same measurement to `tests/imported-*` is what produced **F1** |
| 問題14 items combine ≥2 constraints; ZERO （注N） | Read both stems against the flyer | Both confirmed: 70 = availability window × 実習の有無; 71 = the expired 受付期間 → 開講五日前 deadline × the prescribed 電話 check. **0 （注N）** in the whole 問題14 block. These hold — F1 is about provenance, not about item construction |

---

## 5. Root-cause table

| id | code | how many tests show the class | owning file | proposed edit |
|---|---|---|---|---|
| **F1** | `PIPELINE-GAP` + `GATE-BLIND` | **1** by the recurrence test (only `20260904_3`; every other paper measures 10–13 against the archive). Not systemic — it is a **repair collateral**, the third consecutive paper to show that class (`20260812_1` F2→F3, `20260903_1` F2, `20260904_1` round-2 F2/F3, now this) | `tools/check_consistency.py` + `.agents/exam-qa-review/SKILL.md` (already amended, see §7) | Two edits. **(a) `PIPELINE-GAP`, the real cause:** round-1 F2 named a threshold ("≥20 chars **against the previous 2 papers**"), the fix pass met exactly that threshold, and nothing told it that re-authoring a surface re-opens the ARCHIVE scan too. Add to `jlpt-test-generation` §stage-4 fix loop: **"a repair that re-authors a whole surface must re-run the copyright/non-reproduction scan for that surface against `refs/` and `tests/imported-*`, not only against the previous generated papers — the scan that cleared the pre-fix text says nothing about the replacement."** **(b) `GATE-BLIND`, so it cannot recur silently:** implement round 1's proposed `check_q14_apparatus_reuse()` but give it **two corpora, not one** — the previous 2 generated papers AND every `tests/imported-*`. **Founding-case run, §6.5:** on this paper it prints `21 chars vs imported-n2-2025-07: 「さんはどのように申し込まなければならないか」`, i.e. it catches F1; run over the other 22 generated papers the maximum is 13 (`20260827_1`, 「料金はいくらになるか。1.」), so a 20-char threshold re-classifies **no** shipped paper. Note in the check's docstring that a stem SHAPE shared with official is legitimate (round-1 R3 established this) and that the 20-char line is a *trigger for a human read of the whole 大問*, not a verdict — F1's real evidence is the seven structural coincidences, none of which is string-decidable |
| **F2** | `GATE-BLIND` | **2** — `20260904_1` (「そのまま」 / the 加工→そのまま arc twice in 問題3) and `20260904_3`. **Systemic by the recurrence test** | `tools/check_consistency.py` + `.agents/question-authoring/references/choukai-items.md` §問題3 | The gate has `check_choukai_key_exclusive_token` (lexical) and `check_choukai_errand_repeat` (**cross-paper only**), and `check_choukai_errand_key_collision` **skips entirely** on this paper — its own line reads `skip … (0 of 44 draws keyed: listening_scenarios 0/21)`, because no `pools.json` entry carries an errand key. So the WITHIN-paper errand comparison has never run on any paper. Two edits: **(a)** make the 問題3 `shapes` value in `logs/topics.json` a **two-token pair from closed vocabularies** — `talk archetype × crux domain`, e.g. `想定外の制約発見×受け渡し時刻`, `制度の範囲説明×守秘` — mirroring round-1 R7's proposal for 問題4, and add `check_topics_p3_archetype_repeat()` FAILing when two rows of one paper share an archetype token, WARNing at 3+ rows on one archetype paper-wide. **Founding-case run:** on this paper 1番 and 5番 both take `想定外の制約発見`, and 例/3番 take it too → fires at 4/6; on `20260904_1` 3-1番 and 3-5番 both take it → fires; on official 7/2025 only 5番 does → does not fire, so the rule does not fail a real sitting (the test that refuted the contrast-marker metric in §5). **(b)** `choukai-items.md` §問題3 currently caps *lexical* signatures and 場面 duplication but says nothing about the talk's ARC; add the archetype list with the measurement above (official 7/2025 = 1 of 5 on the problem→solution arc; this paper = 4 of 6) |
| **F3** | `RULE-UNENFORCEABLE` | **2** — `20260817_3` (the founding case, two notes quoting removed strings) and `20260904_3`. **Systemic by the recurrence test** | `.agents/exam-qa-review/SKILL.md` §"A fix that changes WHAT a surface tests" + `tools/check_consistency.py` | The rule "every claim in `notes` that quotes a paper string must quote a string that is still in the paper" is real, is written down, and is enforced by nothing — so it is only ever caught by a reviewer who happens to grep, which is how it took eight days the first time. This one IS string-decidable: **add `check_topics_notes_quotes()`** — extract every 「…」 span of ≥8 JP chars from each history row's `notes`, `surfaces` and `claim`, and FAIL on any that does not occur in that test's `言語知識・読解.md` or `聴解スクリプト.txt`. This is the same predicate `check_kaisetsu_quotes` and `check_section_table_quotes` already apply to the 解説 column and the 構成表 cells; the `notes` column is the last quoting artifact nothing reads, exactly as the 構成表 was until 2026-09-04. **Founding-case run, §6.5:** on `20260904_3` it prints 5 unmatched spans (「決めた会ほど、一年後まで残っている人が多いのです」「うまくなった人」「市内にご在住の方も」…), i.e. it catches F3; state which other ids move before committing, and grandfather them by name rather than lowering the length floor |

**Effect on the loop.** F1's `PIPELINE-GAP` half, F2's `GATE-BLIND` and F3's
`RULE-UNENFORCEABLE` all **block the next generation run** until applied or
explicitly rejected with a reason — each will otherwise reproduce.

---

## 6. Coverage

| step | ran on | result |
|---|---|---|
| 0 — blind solve | `qa/20260904_3/keyless.md` only, all 101 | **101/101, 0 discrepancies** |
| 0 — blind strategy S1/S2 | items 52–69 | **33.3 % / 33.3 %**, both under the 45 % cap; official 32.8 % / 24.6 % |
| 1 — key-by-key proof | all 101 against the sourced Markdown and the script | every key traced to a deciding line; §3 carries the quote for each |
| 2 — distractor elimination | all 101 × every wrong option | no item with two defensible answers. 問題8 spliced end to end ×5, plus the zero-anaphora re-test on 45's bare が-card |
| 2b — plausibility | 問題1–6 option sets; 聴解問題1–3 grounding | every option set shares one functional category; every 聴解問題1/2 distractor has a script line that raises and then removes it (I traced all 48 by hand — see §3); no 解説 kills three distractors in one clause |
| 2.5 — level band | all 問題1–9 keys + 即時応答 idioms | inside N2. 12 問題7 forms and 5 問題8 targets all resolve to `pools.json` grammar categories (gate: 問題8 band ok). Vocabulary half judged by hand: **父親** (問題1-3) is the weakest — an N4-frequency word — but the tested READING discrimination (ちちおや vs 親父/父母/母親) is genuine and official runs comparable targets; **慌ただしい/粗末な/荒っぽい/じたばた** are all N2 stems with deliberately ordinary options, which is 問題5's official shape. No re-drawn vocabulary key this round (the paper's one tier-C repair is `grammar_p8:3` → 〜をきっかけに, from round 0), so the band-check-in-the-report rule bites on nothing new |
| 3 — mechanical reads | stems, 問題7 distribution, 読解 apparatus, length/predictability | 問題1/2/5 comma-free **15/15 = 100 %**, median 16; 問題1–5 です・ます **7/25**; 問題7 mean **45.5**, 2 under 34, spread 37; **32** in-body （注N） / 32 definitions / **0 orphans**; 問題14 （注N） **0**; **3 （中略）**; **0 `<ruby>`**; longest-key rates 22.2 % tied and 22.2 % uniquely; worst option ratio 1.41 |
| 4 — 聴解 structure | the whole セクション構成表 read as columns, against the script | see the 問題2 row in §3 and the re-derivation table in §4. 問題1 fractions spot-re-counted by hand (1番 3/16, 3番 8文/全11文 for the non-dialogue item) and exact. One non-dialogue item ✓, 3 casual 問題4 prompts ✓, keys distinct within each section ✓, no row shares 決め手の種類 AND 質問型 ✓ |
| 5 — topic table | all 47 surfaces × 3 papers | **F2** filed here. 13 読解 themes all distinct ✓. Headline set 環境/科学・技術/医療・福祉/防災/交通/消費・経済 — **∅ intersection with 20260904_2's and ∅ with 20260904_1's**, rule 4 clean in both windows, re-derived from `logs/topics.json` rather than from the notes. 問題12 themes distinct across the last four papers (科学・技術 / 人間関係 / 住まい / 教育). Closing-move column read twice, once down the labels and once down the skeletons (§4) |
| 6 — provenance | spec ↔ ledger ↔ pools ↔ topics | 11/11 categories byte-identical; both `reauthored` stamps parity-checked and accurate; `answer_positions` present and all 101 keys match; `surfaces`/`claim` re-read against the items for every changed surface incl. 聴解問題5-2番's actors (no swap) |
| 6 — copyright / non-reproduction | 627 sentences of this paper × a 1.59 MB corpus (all 31 archive `booklet.md`/`script.md` + all 10 `imported-*`) | 52 sentences carry a ≥16-char verbatim run. **51 are mandated boilerplate** — 大問 instructions, 聴解 narration formulas, and standard stems (「このメールで問い合わせていることは何か」「男の人は何について話していますか」「何を持って行かなければなりませんか」). **The 52nd is F1.** Zero passage or dialogue sentences overlap |
| 6.5 — root cause | 3 findings → 3 rows | §5; each carries a founding-case measurement |

### Every `make check` line naming this test, with its resolution

`grep -c 20260904_3` over the gate output returns 4 non-ok lines. All four:

| line | resolution |
|---|---|
| **FAIL** — `33 exam MP3(s) are on the audio release: ['20260904_3']` | **Expected, out of scope.** The orchestrator's `make upload-files` step, gated behind this verdict |
| **WARN** — `問題1/2 options share vocabulary with their script block (3/48 = 6 %)` | **False positive ×3, re-adjudicated by hand this round.** (a) 問題1-1番-1「来客用のお茶を、足りるかどうか見て買っておく」 is a near-verbatim lift of the speaker's own 「お茶は、足りるかどうか見て、多めに買っておいたほうがいいですか」 — the predicate has no 2-consecutive-kanji run to match on. (b) 問題1-2番-4「中くらいの入れ物二つに分けて入れる」 is the key, and the script's 「中くらいのを二つに分けて入れて」 contains **no two consecutive kanji at all** (中/二/分 are each single, 入れ物 is split by れ). (c) 問題2-例-4「一人分の代金が安くなり、その日に買えるから」 paraphrases 「十枚で八千円」→代金, 「当日、券売機でも」→その日に買える, by design. **All three are tokenizer artefacts; zero distractors are ungrounded.** 6 % is BELOW official's 11 % baseline, i.e. this paper paraphrases its options *less* than official does — the direction of the number is a compliment, not a warning |
| **WARN** — `no 聴解 slot repeats its own theme in the previous 2 papers: 聴解問題3-1番=食 (also 20260904_2)` | **Resolved as genuinely unrelated, on the cross-paper axis.** `20260904_2`'s 3-1番 is a radio talk on *why the speaker records only the TIME of meals, not what was eaten* — a personal record-keeping method. This paper's 3-1番 is a bento shop owner on *why corporate orders doubled when he offered a pickup window*. Same pool tag, no shared subject, no shared errand, no shared vocabulary of consequence. **The 食 tag on this slot is not the problem — see F2 for the problem the check does not look at, which is 食 twice WITHIN 問題3 (3-1番 and 3-5番) with a shared errand** |
| **WARN** — `the 問題8 form-family check compares most of the draw (1/5 = 20 % family-tagged)` | **Repo-level, not this paper's defect.** 4 of 5 drawn `grammar_p8` entries carry no `grammar_form_families` tag in `pools.json`; the repair is in the pool map, and the WARN correctly says the line below it is silent rather than green. Confirmed by hand that the 5 drawn 問題8 forms (のみならず / ないことには / 一方 / をきっかけに / つつ) collide with none of the 12 問題7 forms and with each other on neither form nor function |
| **WARN** — `every stamped spec's pools_sha matches pools.json` | **Inert record**, not a defect and not specific to this test — the check's own message says so. This paper is stamped on a reroll, so the sha certifies that redraw's pool |

---

## 7. Skips and edits

* **Nothing was skipped.** Steps 0–6.5 ran on all 101 items and on every artifact.
* **Not run, per the brief:** `git add`/`git commit`, `make upload-files`,
  `make model-answer`. Stage 5 is gated on this verdict and the verdict is FAIL,
  so it must not start. `詳細解説.json` does not exist yet, which is legal at
  this stage — the gate `skip`s its three explanation checks, and those skips
  are not passes.
* **The one file this pass may edit is this skill**, and one class was missing
  from it, so I have added it (`.agents/exam-qa-review/SKILL.md`, §"The pass, in
  order" → step 6.3's neighbourhood): **a re-authored surface's provenance scan
  must be re-run against `refs/` and `tests/imported-*`, because the scan that
  cleared the pre-fix text is evidence about text that no longer exists.**
  `20260904_3`'s 問題14 is named as the shipped example.
* **Sources were still** — the three shas at the top of this report are
  identical to the ones hashed before the first tool call and after the last.

---

## 8. The work list, ordered by cost

1. **F1 — re-author 問題14 again, off official 7/2025.** The subject
   (避難所運営における多様性への配慮) is the drawn one and does not have to move;
   the DOCUMENT and the MECHANIC must. Concretely: pick a document type official
   7/2025 does not use for a course notice (a 持ち物・当日の流れ案内, a
   会場別の実施日一覧, a 申込区分による窓口の振り分け), and build 71 on a decision
   that is not "the 受付期間 has passed, so use the late route and phone first."
   Then re-run the archive+imported scan on the replacement, not only against
   `_1`/`_2`.
2. **F2 — re-angle 聴解問題3-5番** (not 3-1番, whose key position and drawn
   scenario are load-bearing). The drawn scenario supports other gists; move it
   off *"the constraint I feared was not the real one, and the real one was
   delivery timing"*. Then re-run `make mp3` + `make sheet`, update the item's
   `surfaces` / `claim` / `shapes` rows, and re-read 例 and 3番's arcs against
   the new one so the repair does not land back on the template.
3. **F3 — rewrite `logs/topics.json`'s `notes` for this test** so every quoted
   string is one the shipped paper contains, and fold in what the fix pass did.
   Ten minutes, and it is what the next paper's blueprint stage reads.

Findings F1 and F2 are automatic, so **the paper does not ship as it stands.**
Because the loop caps fresh-eyes rounds at 2, these three will be applied
without a third independent pass; §8 states each repair concretely enough to be
applied without re-deriving it, and each carries the measurement that proves it
was needed.

**QA: FAIL (3 findings, 2 automatic)**


---

## 9. Disposition — round-2 direct-fix pass, 2026-09-05

Round 2 returned FAIL with **3** findings, which is inside the **≤3** that
`jlpt-test-generation` §"The 4-stage pipeline" allows to be **fixed directly**,
and the loop is capped at 2 fresh-eyes rounds. All three were therefore applied
with the same rigor (root-cause named, `make check` read line by line, diff
sanity-read) and **without a third independent review**. That is stated here and
in the fix pass's final report.

| id | disposition |
|---|---|
| F1 | FIXED — 問題14 re-authored; three-corpus shared-run scan 9 / 7 / 12 (see the row above) |
| F2 | FIXED — 例, 1番 and 5番 re-angled; six 問題3 arcs, one row each, counted by hand |
| F3 | FIXED — `logs/topics.json` `notes` rewritten; 0 unmatched 「…」 spans in the whole row |

**Not done, per the brief:** the round-2 root-cause table's proposed gate checks
(`check_q14_apparatus_reuse`, `check_topics_p3_archetype_repeat`,
`check_topics_notes_quotes`) were NOT implemented — the orchestrator owns those
after commit. `git add`/`git commit`, `make upload-files` and `make model-answer`
were not run.

**Gate after the fix:** the only FAIL naming this test is the standing
「exam MP3(s) are on the `audio` release」, which is the orchestrator's
`make upload-files` step. Three WARNs name it, all previously dispositioned in
§6 of this report and none moved by the fix: the 問題8 form-family coverage WARN
(repo-level, `pools.json`), `check_slot_theme_repeat` 聴解問題3-1番=食 (resolved on
the merits in §6; the arc that made it matter is gone), and the 問題1/2 option
grounding WARN at 3/48 = 6% (the same three tokenizer artefacts, below official's
own 11% baseline).
