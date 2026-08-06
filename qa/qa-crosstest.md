# CROSS-TEST QA (exam-qa-review steps 5 & 6) — tests 1, 2, 3, 4

## 1. Verdict

**CROSS-TEST: FAIL (20 findings, 11 automatic)**

The single mechanical cause behind most of it: **test 3 and test 4 were blended from the
identical harvest.** `logs/test_spec.json` at commit `7638a2f` recorded
`{"test_id": "4", "seed": 20260805, "harvest_sha": "dc34edede771"}`; the spec on disk today
records `{"test_id": "3", "seed": 20260806, "harvest_sha": "dc34edede771"}`.
`sha1(logs/seeds.json)[:12]` = `dc34edede771`. Same harvest, twice. The gate cannot see it
because commit `4df5631` overwrote test 4's real `harvest_sha` in `logs/ledger.json` with the
placeholder string `harvest_20260805`.

### Chronology (from `logs/ledger.json` `generated_at`, not folder number)

`1` (legacy) → `4-removed` 08-03 17:36 → `2` 08-04 12:11 → `4` 08-04 14:55 → `3` 08-05 18:53

So "the previous test" pairs are **1→2, 2→4, 4→3** — *not* 3→4. Test 3 is the newest paper
and test 4 is the one immediately before it. Findings below use the real order.

---

## 2. The topic table

Columns are the four papers. Read repetition **left-to-right along 1 → 2 → 4 → 3**.
`[shape]` = the errand archetype, per `jlpt-test-generation` §"One topic, one surface".

### 読解 surfaces

| Surface | Test 1 | Test 2 | Test 4 | Test 3 |
|---|---|---|---|---|
| 問題9 cloze | キャッシュレス決済と使いすぎ | 昆虫食と食料不足 | 実店舗の体験価値への再定義 | **歴史的建造物の再生・宿泊施設化** |
| 問題10(1) | 取引先メール:部品の後継品切替 | デジタルデトックス | 方言と地域の暮らし | **食品ロス削減 社内通知** |
| 問題10(2) | 道草・遠回りの発見 | 言語獲得と対話 | 緑川市立図書館 休館案内 | 男性の育児休業の質 |
| 問題10(3) | マンション断水のお知らせ | 青葉市ごみ分別改定 | **手書き文字の再評価** | 観光公害とマナー |
| 問題10(4) | 挨拶＝安全の網 | 会話の沈黙 | **睡眠休養感** | **手書きの手紙の再評価** |
| 問題10(5) | 敬語＝距離の調節 | 社会人向け夜間講座 | **規格外野菜の加工品** | 伝統工芸の道具特注メール |
| 問題11(1) | 写真撮影と記憶 | 脱プラスチック代替素材 | 地域交流イベント スタッフ募集 | **スマート農業(自動走行・ドローン)** |
| 問題11(2) | 子どもの習い事のやめ方 | クラフトツーリズム | **スマート農業(自動草刈りロボット)** | 郷土料理と記憶 |
| 問題11(3) | 指差し確認 | ハイブリッドワーク | **古民家・歴史的建造物の改修活用** | マイボトル持参 社内連絡 |
| 問題11(4) | **屋上緑化** | **グリーンパートナー制度(住民の緑地管理)** | 伝統行事の担い手不足 | フードバンク連携 |
| 問題12 A/B | 映画館 vs 家での鑑賞 | ウォーキング目標歩数 | 模倣と独創 | 音楽と記憶 |
| 問題13 | 失敗を情報として扱う(陶芸家) | 匂いと記憶 | 時間の余白 | マイボトルと使い捨て容器 |
| 問題14 flyer | みどり市民スポーツセンター 教室案内 `[municipal course flyer + 申込期限]` | 港南市 生涯学習フェスタ／**まなびポイント** `[municipal event flyer + point scheme]` | **桜川市 電子地域通貨「さくらコイン」20%還元** `[municipal point-rebate flyer]` | **緑市 電子地域通貨「みどりコイン」20%還元** `[municipal point-rebate flyer]` |

### 聴解 surfaces (each item its own row)

| Item | Test 1 | Test 2 | Test 4 | Test 3 |
|---|---|---|---|---|
| 問1 例 | 学校の宿題 | 学校の宿題 | 会社 | 出張準備 (チケット/ホテル) |
| 問1-1番 | 家電売り場 ケトル交換 `[return/exchange]` | 美術館 音声ガイド `[download the app]` | 郵便 再配達申込 `[download/use the web form]` | 家庭 **熱中症・夜間エアコン** `[household decision]` |
| 問1-2番 | 大学 レポートをグラフ化 | 薬局 常用薬確認シート | 出張 電車遅延→訪問先へ電話 | 学習塾 体験授業→入塾手続き |
| 問1-3番 | 市役所 住民票の受取方法 | **フードドライブ 準備チラシ** | 街なか 急な雨→**配車アプリDL** `[sudden rain → app]` | スーパー **食品ロス 手前取りポスター** |
| 問1-4番 | 病院 頭痛の検査結果 | 取引先への折り返し電話 | 駅 急な雨→**傘シェアリング登録** `[sudden rain → app]` | 銀行 口座開設 |
| 問1-5番 | イベント準備 マイク確認 | ワーケーション申請書 | マンション **設備点検** 車の移動 | 市役所 **傘シェアリング導入** |
| 問2 例 | 眠い理由 | 体に力が入らない理由 | バッグを選んだ理由 | パーティ欠席の理由 |
| 問2-1番 | 遅刻理由(USB忘れ) | **睡眠の質改善(起床時間固定)** | レポート修正箇所 | **職場の腰痛・立ち作業** |
| 問2-2番 | **不動産屋 アパートの騒音** | 防災訓練の改善点 | **昇降式デスク 立ち仕事の課題** | **自転車シェアリング 好評理由** |
| 問2-3番 | レストラン人気の理由 | 社内食堂リニューアル | **熱中症・夜間エアコン** | コンサート 入場ゲート |
| 問2-4番 | 会社を辞めた理由 | イベント役割分担 `[event staffing]` | バスのダイヤ変更(運転手不足) | 就職課 面接の助言 |
| 問2-5番 | 新製品発売の遅れ | **マンションの騒音** | **自転車シェアリング 不満** | 週末の天気予報 |
| 問2-6番 | 外国語学習で大切なこと | 古着アップサイクル | バイトのシフト変更期限 | **マンション 電気設備点検 日程** |
| 問3 例 | テレビ | 部屋の模様替え | ラジオ | オンライン学習 |
| 問3-1番 | **睡眠負債・週末の寝だめ** | **地域商品券(10%プレミアム・電子商品券)** | 日本語教材の選定 | システム仕様変更と納期延期 |
| 問3-2番 | 評価基準の変更 | 夏合宿の役割分担 | 展示会 名札の二次元コード | **シェアサイクル ヘルメット着用** |
| 問3-3番 | 観葉植物を育てるよさ | 置き配と物流CO2 | プレゼン資料の構成 | 保険の契約内容見直し |
| 問3-4番 | ネット情報を疑う力 | 医療費控除 | 路上喫煙禁止区域 | **駅の傘シェアリング拡大** |
| 問3-5番 | 留守電 落とし物の確認 | 無人決済店舗・AI接客 | 商店街スタンプラリー | **睡眠の質と日中の作業効率** |
| 問4 (即時応答) | 9 items — 職場敬語・慣用句 | 9 items — 職場敬語・慣用句 (社長/課長) | 11 items — 職場敬語・慣用句 | 11 items — 職場敬語・慣用句 |
| 問5-1番 | 家具売り場 ソファ4種 `[pick 1 of 4]` | 経費精算のオンライン化 | 研究室4種 `[pick 1 of 4]` | 観光モデルコース4種 `[pick 1 of 4]` |
| 問5-2番 | 料理教室 4コース `[2 people pick]` | 学食改善案 `[2 people pick]` | **アパート4物件** `[2 people pick]` | 食品寄付イベント 担当エリア `[2 people pick]` |
| 問5-3番 | — (does not exist) | — | — (does not exist) | — |

Bold = participates in a repetition finding below. `問5-1番`/`問5-2番` shapes are
**format-mandated** by 統合理解 and are not filed as repeats.

---

## 3. Repetition findings

### 3.1 Within-paper (all automatic)

| # | Test | Finding | Evidence |
|---|---|---|---|
| **X1** | 3 | **食品ロス on four surfaces of one paper.** | 問題10(1)「食品ロスの削減に向けた家庭での取り組みについて」; 問題11(4)「売れ残った食品を地域の支援団体へ寄付する『フードバンク連携』」; 聴解問題1-3番「期限切れによる食品廃棄を減らすために、手前取りの呼びかけを強化したい」; 聴解問題5-2番「食品寄付受付イベントの担当エリア」 |
| **X2** | 3 | **マイボトル tested twice in 読解** (18 occurrences across two passages), plus a third unused spec allocation. | 問題11(3)「マイボトル持参キャンペーンの開始について…1杯につき50円の割引」 and 問題13「『マイボトルの持参』という生活習慣」+「マイボトルを持参した顧客に対してドリンク代金の割引サービス」. Both keyed on the same 割引 mechanic. `qr_situation_seeds[1]` = 「市民向けマイボトル給水の呼びかけ」 = a third slot on the same subject. |
| **X3** | 3 | **Shared-mobility on four 聴解 items + the 問題14 flyer.** Two umbrella-sharing, two bike-sharing. | 問題1-5番「傘シェアリングサービスの導入計画案」/ 問題3-4番「傘のシェアリングサービスが急速に拡大」— both even share the decisive detail 「駅…スポット設置」. 問題2-2番「自転車シェアリングサービス」/ 問題3-2番「シェアサイクル…ヘルメット着用」. |
| **X4** | 3 | **「感覚が記憶を呼び覚ます」 tested twice**, essay vs A/B. | 問題11(2)「味覚や嗅覚から得られた情報は、感情や記憶を司る大脳辺縁系（注2）に直接伝達される」 vs 問題12A「音楽は過去の記憶を呼び覚ます強力な触媒（注1）として作用する」. Same subject, different register — the rule's exact wording. |
| **X5** | 3 | Two environmental-campaign **社内通知 in the same register**, same 差出人 shape. | 問題10(1)「全社員の皆様へ／総務部環境推進課」 and 問題11(3)「全社員の皆様へ／環境推進委員会」. |
| **X6** | 4 | **Two adjacent 聴解 items run the identical errand.** | 問題1-3番「参ったな、急に雨が降ってきたよ」→ 「さっそくスマホでそのアプリを入れてみるよ」; 問題1-4番「急に雨が降ってきたんですが、駅の傘シェアリングを使いたいんです」→「今ここで登録します」. Same trigger sentence, same keyed action (install/register a phone app), consecutive item numbers. |
| **X10** | 3 | **問題14 flyer shares its subject with four listening items.** | Flyer row C: 「C：交通・シェアリング｜市内シェアサイクル、駅前傘シェアサービス｜月額定額プランの決済は対象外」 against 問題1-5番 / 問題2-2番 / 問題3-2番 / 問題3-4番. Shared *setting* would be tolerable; shared *subject on the graded flyer* is not. |

### 3.2 Cross-test (all automatic)

| # | Pair | Finding | Evidence |
|---|---|---|---|
| **X7** | **4 → 3** | **Ten surfaces repeat from the immediately previous paper.** | 1. 歴史的建造物 — T4 問題11(3)「古民家や歴史的建造物をリノベーション…宿泊施設や地域の交流スペースとして再生」 → T3 **問題9 cloze**「古民家や町家を改修して宿泊施設や交流拠点として再生」. 2. スマート農業 — T4 問題11(2) → T3 問題11(1). 3. 手書きの手紙 — T4 問題10(3) → T3 問題10(4). 4. 睡眠 — T4 問題10(4)「成人の約4割が1日の睡眠時間6時間未満」 → T3 聴解問題3-5番「成人の約4割が睡眠時間6時間未満」 (verbatim fact). 5. 熱中症・夜間エアコン — T4 聴解問題2-3番 → T3 聴解問題1-1番, both keyed on 「タイマーで途中で切るのではなく…朝までつけっぱなし」. 6. 自転車シェアリング — T4 聴解問題2-5番 → T3 聴解問題2-2番, **same 問題 slot**, both on 「借りたポートと異なる/違う場所にも返せる」. 7. 傘シェアリング — T4 聴解問題1-4番 → T3 聴解問題1-5番 + 問題3-4番. 8. 立ち作業と腰/足の疲労 — T4 聴解問題2-2番(昇降式デスク) → T3 聴解問題2-1番(腰痛予防), **same 問題 slot**. 9. マンション設備点検 — T4 聴解問題1-5番 → T3 聴解問題2-6番. 10. 電子地域通貨ポイント還元 flyer — T4 問題14 → T3 問題14, **same slot** (see X9). |
| **X8** | **1 → 2** | Three repeats into the next paper, one in the identical slot. | (a) 都市の緑 — T1 問題11(4)「屋上緑化」 → T2 問題11(4)「グリーンパートナー制度…街路樹や公園の草花を管理」, **same slot**; T2's passage still carries T1's leftover gloss 「（注1）屋上緑化：建物の屋上に植物を植えること」 though 屋上緑化 never appears in T2's body. (b) 睡眠 — T1 聴解問題3-1番「睡眠負債」 → T2 聴解問題2-1番「睡眠の質が改善した一番の理由」. (c) 住まいの騒音 — T1 聴解問題2-2番「すぐ隣が幹線道路…夜も車の音」 → T2 聴解問題2-5番「上の階の部屋から聞こえる深夜のドタバタ」. |
| **X9** | **2 → 4 → 3** | **Two archetypes ran three consecutive papers.** | (a) *Municipal digital-points scheme*: T2 聴解問題3-1番「プレミアム付きの地域商品券…10%のプレミアム…電子商品券」 + T2 問題14「まなびポイント（200ポイント）」 → T4 問題14「電子地域通貨『さくらコイン』…決済額の20%還元」 → T3 問題14「電子地域通貨『みどりコイン』…決済金額の20%分のポイントを還元」. T4 vs T3 match on: 20% rate, 「1回あたりの還元上限は2,000ポイント」/「1回の決済につき最大2,000ポイントまで還元」, expiry 2027年2月28日/翌年2月末日, 「※予算上限に達し次第終了」, 大型チェーン/コンビニ carve-out, and the invented-city + coin-name pattern (桜川市/さくらコイン ↔ 緑市/みどりコイン). This is the rename case `web-topic-research` documents as unmechanizable — and it shipped again after being documented. (b) *Community-event staffing*: T2 聴解問題2-4番「地域交流フェスタの担当分け…来場者受付と会場内での案内誘導」 → T4 問題11(1)「地域交流イベント…当日スタッフ…受付案内、会場設営の補助」 → T3 聴解問題5-2番「食品寄付受付イベントの担当エリア」. |

### 3.3 問題12 A/B compared across all four (as requested)

| Test | 問題12 theme |
|---|---|
| 1 | 映画館での鑑賞 vs 家での鑑賞 |
| 2 | ウォーキングの目標歩数 — 数値の可視化 vs 歩行の質 |
| 4 | 模倣と独創 |
| 3 | 昔の音楽との付き合い方 |

**The reported "three papers in a row argued 働き方" is NOT reproducible on the current files.**
`働き方 / テレワーク / リモートワーク / ハイブリッドワーク` occurs in exactly one generated
paper — test 2, 問題11(3) — and in no 問題12 at all. That defect was repaired. What *is* live
is X4: test 3's 問題12 (音楽と記憶) duplicates its own 問題11(2) (郷土料理と記憶).

### 3.4 Two reported defects I could not reproduce (report as fixed / mis-filed)

| Claim | Status |
|---|---|
| "test 4 has apartment-hunting in 問題1-4番 **and** 問題5-3番" | **Not reproducible.** T4 問題1-4番 is 駅の傘シェアリング; **no 問題5-3番 exists** in any of the four papers (問題5 = 1番 + 2番 in all of them). Apartment-hunting appears once in T4 (問題5-2番, 留学生センター, 4物件). The nearest live apartment repeat is T1 問題2-2番 (不動産屋) → T4 問題5-2番, three papers apart. |
| "test 2's フードドライブ listening key was spelled out in the 問題14 flyer's fine print" | **Not reproducible.** T2 問題14 is 港南市・生涯学習フェスタ (古本市・手話ワークショップ); no food content. Fixed. |

---

## 4. Provenance findings (step 6)

### 4.0 Which papers can be audited at all

`logs/test_spec.json` holds **one** spec: `"test_id": "3"`, `"seed": 20260806`,
`"generated_at": "2026-08-05 18:53:58"`, `"harvest_sha": "dc34edede771"`.

| Test | Spec on disk? | Ledger entry? | Auditable? |
|---|---|---|---|
| 1 | No — overwritten | **No** — folded into the `"legacy"` v1-migration aggregate (kanji_reading 10, orthography 10 … ≈ two draws in one row) | **No.** Not even its seed or its draw is recoverable. |
| 2 | No — overwritten at `1e7f44c` | Yes, seed 20260804, `harvest_sha: "harvest_20260804"` (placeholder, see X12) | **No spec** — target items, answer positions and blend provenance all unverifiable |
| 4 | No — overwritten at `4df5631` | Yes, seed 20260805, `harvest_sha: "harvest_20260805"` (placeholder; the spec that shipped it said `dc34edede771`) | **No spec** |
| 3 | **Yes** | Yes, seed 20260806, `harvest_sha: "dc34edede771"` | Yes — audited in full below |

**Three of the four shipped papers cannot be audited against a blueprint at all.** That is a
reportable provenance gap in its own right (X13), not a skip.

### 4.1 Findings table

| # | Test | Check | Result | Evidence |
|---|---|---|---|---|
| **X11** | 3 & 4 | No harvest may be reused | **FAIL (automatic)** | `git show 7638a2f:logs/test_spec.json` → `{"test_id":"4","seed":20260805,"harvest_sha":"dc34edede771"}`. Spec on disk → `{"test_id":"3","seed":20260806,"harvest_sha":"dc34edede771"}`. `sha1(logs/seeds.json)[:12] == dc34edede771`. `git log -- logs/seeds.json` shows the file has not been touched since `7638a2f` (08-04 18:55) — **test 3's regeneration on 08-05 re-ran the blend over test 4's untouched harvest.** This is X7's mechanism: a new `--seed` reshuffles which slot a subject lands in, not which subjects exist. |
| **X12** | 2, 4, 4-removed | `harvest_sha` must be the script's stamp, never hand-written | **FAIL** | `git diff 7638a2f HEAD -- logs/ledger.json`: `-"harvest_sha": "1f19b335917a"` / `+"harvest_sha": "harvest_20260804"`, and test 4's `+"harvest_sha": "harvest_20260805"` replacing the real `dc34edede771`. `legacy0803sh` on 4-removed. Commit `4df5631` also **deleted** the previous test-3 history entry and renamed the 08-03 entry to `4-removed`. The gate's "each test blended its own web harvest" check compares ledger values, so the hand-edit is exactly what made X11 invisible. AGENTS.md: "never by hand-writing a sha". |
| **X13** | 1, 2, 4 | Spec/paper provenance auditable | **FAIL (automatic)** | See 4.0. Target-item, answer-position and origin audits are impossible for three of four papers. |
| **X14** | 3 | Recorded provenance is re-derivable | **FAIL** | Running `merge_seeds.validate_harvest(logs/seeds.json)` today **aborts**: `3 seeds cite one URL https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf -> ['マイボトル持参による使い捨て容器の削減','市民向けマイボトル給水の呼びかけ','社内でのマイボトル持参キャンペーン告知']`. The spec's `harvest_sha` therefore points at a harvest the current pipeline refuses. (Count is **3**, not the 2 the gate reports.) |
| **X15** | 3 | Web fact used accurately, not contradicted | **FAIL (automatic)** | I fetched the source. It is real (18 pp., 環境省「リユース可能な飲料容器およびマイカップ・マイボトルの使用に係る環境負荷分析について」) and supports **one** of the six facts attributed to it (`繰り返し使えば…環境負荷を抑えられる` ← 「100 回使用した場合の１回使用あたりのCO2排出量は…低い」). It contains **0 occurrences of 給水** and **0 occurrences of 割引** in the entire document. Yet 「給水スポットや店舗での割引が普及の後押しになる」, 「カフェテリアでマイボトル割引を導入する企業がある」 and 「公共施設や店舗で給水できる場所が増えている」 are recorded as its facts and were then written into 問題13 (「無料の『給水スポット』が増加…ドリンク代金の割引サービス」) and 問題11(3) (「専用給水機を無料で…1杯につき50円の割引」). Invented facts, laundered through the spec into two graded 読解 surfaces. |
| **X16** | 3 | Every blended surface gets a **distinct** topic | **FAIL** | `items.reading_topics` (12) contains four near-duplicate pairs: 「マイボトル持参による使い捨て容器の削減」/「社内でのマイボトル持参キャンペーン告知」 (same URL, same subject); 「スマート農業におけるロボット農機の導入」/「スマート農業と担い手」; 「家庭での食べきりと食品の使いきり習慣」/「スーパーのフードバンク連携による食品ロス削減」; 「郷土料理と記憶」/「音楽と記憶」. The gate's distinctness check is exact-string, so all four pass. X1/X2/X4 are the paper-side consequence. |
| **X17** | 3 | Each seed feeds exactly one surface; blended surfaces stay ≥30% web | **FAIL** | `qr_situation_seeds` (3, all `origin: web`) and `carrier_seeds` (3, all web) are **entirely unused**: `grep` over `tests/3` finds 熱中症 0×, 地域通貨 0×, 規格外 0×, 図書館 0×, 電子書籍 0× in 問題1–8 and 聴解問題4. So 問題1–8 = **0% web** and 問題4 = **0% web**, both below the 30% floor. Worse, one idle seed (「地域の図書館での電子書籍と来館サービスの併用案内」) is the subject **test 4 already shipped** in its 問題10(2) (緑川市立図書館 休館・電子書籍) — further proof the harvest was never refreshed against the previous paper. |
| **X18** | all | `logs/topics.json` accumulates the topic record | **FAIL** | The file **does not exist**. `merge_seeds.check_topic_reuse()` prints `note: no topics.json history yet — cross-test topic check skipped` and returns. The build pass (`jlpt-test-generation` step 6) has never written it for any of the four tests, so the one automated cross-test topic guard has been a no-op on every run to date. |
| **X19** | 2, 4, 4-removed | Why the ledger "over-records" (parent's question) | **The ledger is correct; the gate is wrong.** | `DRAW` was retuned **after** those tests were sampled and no migration or grandfathering was done: `word_formation 5→3` and `quick_response 12→11` landed in `7638a2f` (08-04 18:55); `listening_scenarios 20→21` (and `reading_topics →12`) in `58a8c8b` (08-05 18:46). 4-removed was sampled 08-03 17:36, test 2 08-04 12:11, test 4 08-04 14:55 — all before. Only test 3 (08-05 18:53) matches the current table, and it matches exactly. So the four mismatches are historical draws measured against a table that changed under them, **not** corruption. |
| **X20** | all | Is `4-removed` vs `4` duplication corrupting rotation? | **Yes, mildly — and the bigger corruption is elsewhere.** | `COOLDOWN = 2`, LRU over `history`. (a) `4-removed` is a phantom draw no shipped paper uses, yet it occupies an LRU slot and permanently excludes its items — it overlaps test 4 on 3 grammar points (`〜にかけては`, `〜にわたって`, `〜にともなって`), i.e. the two entries double-book the same draw. (b) `legacy` compresses ≈2 real draws into one slot, so at test 3's sampling it sat at ago=3 and became redrawable: test 3 legitimately redrew **9 items last used by test 1's draw** — `尋ねる`, `愚かだ`, `普及`, `〜たとたん`, `〜まい`, `〜ぎみだ`, `顔が広い`, `大目に見る`, reading topic `キャッシュレスと金銭感覚` — plus 6 from `4-removed`. (c) Commit `4df5631` **deleted** a history entry outright (the original test 3), which rewrites the LRU window retroactively. (d) Separately, test 3's own `grammar_p7` draw contains **`〜気味` and `〜ぎみだ` together** — one grammar point under two spellings inside a single 問題7 — which the gate normalizes for `pools.json` but not for a draw. |

### 4.2 Blend balance — computed, not asserted (test 3, the only auditable paper)

| Surface | Total | Web | Pool | Verdict |
|---|---|---|---|---|
| `reading_topics` | 12 | 6 (**50%**) | 6 (50%) | PASS (30–60%, pool ≥40%) |
| `listening_scenarios` | 21 | 8 (**38%**) | 13 (62%) | PASS |
| `cloze_topic` | 1 | web | — | binary slot, PASS |
| `info_retrieval_texture` | 1 | web | — | binary slot, PASS |
| `qr_situation_seeds` → 問題4 | 3 allocated | **0 used → 0%** | 100% | **FAIL** (X17) |
| `carrier_seeds` → 問題1–8 | 3 allocated | **0 used → 0%** | 100% | **FAIL** on the floor; the 1-in-3 **cap** is trivially satisfied (0/47 stems) |

**Domain caps.** 16 topic-level web picks over 12 netlocs; **max 2 per domain**
(`caa.go.jp` 2, `bunka.go.jp` 2, `env.go.jp` 2, `mhlw.go.jp` 2) — the numeric cap holds.
But it is **defeated in substance**: `env.go.jp`'s two picks are the *same URL* and the *same
subject* (マイボトル), plus a third from that URL in the uncapped leftovers. A netloc counter
cannot see that one document was mined three times (X14/X16).

**Carrier cap (問題1–8, ≤1 in 3 stems per 問題).** Measured across all 47 stems of test 3's
問題1–8: **0 stems** carry web texture. Cap respected; floor missed.

**Copyright invariants.** Max-one-fact-per-passage holds where the fact is real. The failure is
upstream: test 3's 問題13 builds an entire paragraph on two facts (給水スポット increase,
店舗の割引サービス) attributed to a document containing neither (X15). No verbatim source-sentence
reproduction or source-structure mirroring was found in any of the four papers.

### 4.3 Rotation inputs — seeds and harvests

| Test | `--seed` | `harvest_sha` (ledger) | `harvest_sha` (spec, when it existed) | Notes |
|---|---|---|---|---|
| 1 | unrecorded | unrecorded | — | no entry at all; folded into `legacy` |
| 4-removed | 20260803 | `legacy0803sh` | — | placeholder; phantom draw |
| 2 | 20260804 | `harvest_20260804` | lost | placeholder; real value was `1f19b335917a` on the deleted test-3 row |
| 4 | 20260805 | `harvest_20260805` | **`dc34edede771`** | **ledger value falsified** |
| 3 | 20260806 | `dc34edede771` | `dc34edede771` | **same harvest as test 4** |

- Two tests sharing **both** seed and harvest: none (seeds are distinct).
- **Reused harvest: YES — `dc34edede771` served tests 4 and 3** (X11).
- **Missing/fabricated `harvest_sha`: 4 of 5 ledger rows** (X12).
- Per the parent's instruction I did not re-file the `make check` DRAW-count rows or the
  duplicate-URL row; X19 explains the DRAW mismatch's cause and X14 corrects the URL count to 3.

### 4.4 Harvest URL verification (WebFetch, 3 of 22)

| URL | Returned | Verdict |
|---|---|---|
| `https://www.maff.go.jp/j/kanbo/smart/index.html` | Live MAFF スマート農業 portal. Quoted back: 「ロボット技術やICTを活用して超省力・高品質生産を実現する新たな農業を実現」, plus 自動走行農機 and 農業用ドローン sections. | **Real; both seed facts supported verbatim in substance.** |
| `https://www.mhlw.go.jp/content/001305530.pdf` | Real 51-page MHLW 睡眠ガイド (6.1 MB). Text layer extracted locally: 睡眠休養感 ×61, and 「１日の平均睡眠時間が６時間未満の者の割合は、男性37.5％、女性40.6％…４割以上を占めていた」. | **Real; both seed facts supported** (and correctly rounded to 「約4割」 per the N2 simplification rule). |
| `https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf` | Real 18-page 環境省 report 「リユース可能な飲料容器およびマイカップ・マイボトルの使用に係る環境負荷分析について」 (377 KB). Local extraction: マイボトル ×8, **給水 ×0, 割引 ×0**. | **Real URL, fabricated facts** — 1 of the 6 facts attributed to it across 3 seeds is supported. See X15. |

**The harvest is not invented.** No sequential or templated IDs remain: the fabricated
`soumu.go.jp/main_content/000912345.pdf → …346 → …347` chain that `web-topic-research` documents
was removed at commit `7638a2f` (visible in `git diff 1e7f44c HEAD -- logs/seeds.json`) and the
current 22 seeds resolve to 14 real netlocs. The live defects are **reuse** (X11) and
**one document mined three times with invented facts** (X14/X15), not fabrication of URLs.

---

## 5. Root causes (step 6.5)

Grouped — findings sharing a cause get one row.

| ID | Findings | Code | Papers showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|---|
| **R1** | X11, X12 | `GATE-WRONG` | 4 of 4 (every ledger row carries an unverifiable `harvest_sha`) | `tools/check_consistency.py`, `.agents/item-pool-sampling/scripts/sample_items.py` | The harvest-reuse check reads `logs/ledger.json`, a file agents hand-edit. Make it **recompute**: in `check_harvest_hygiene()`, add `check("every ledger harvest_sha is a 12-hex sha1 stamp", all(re.fullmatch(r"[0-9a-f]{12}", e["harvest_sha"]) for e in hist if e.get("harvest_sha")), ...)` — this alone fails `harvest_20260804`, `harvest_20260805`, `legacy0803sh` today. Then add `check("the newest ledger harvest_sha equals sha1(logs/seeds.json)[:12]", hist[-1]["harvest_sha"] == sha1(seeds_path.read_bytes()).hexdigest()[:12], ...)`, so a spec blended over an untouched harvest cannot be relabelled. Finally make history **append-only**: `check("no ledger history entry was deleted or renamed", set(prev_ids) <= set(cur_ids))` against the committed HEAD~ copy. |
| **R2** | X7, X9, X10, X1, X2, X3, X4, X5, X6, X8 | `PIPELINE-GAP` | **4 of 4** | `.agents/jlpt-test-generation/SKILL.md` (step 6), `.agents/web-topic-research/SKILL.md` | `logs/topics.json` is specified in full and **has never been written** (X18), so the whole-paper table is rebuilt by eye each round and nothing accumulates — exactly the state the file was created to end. Fix as a **build-time artifact, not a review-time habit**: add `tools/write_topics.py <test_id>` that appends the `surfaces` + `shapes` row, make it a required line in `jlpt-test-generation` step 6 next to `make booklet`/`make sheet`, and add `check("every test on disk has a logs/topics.json row", ...)` to the gate so a missing row fails. Until a row exists per test, `check_topic_reuse()` is a no-op and every cross-test repeat above is invisible to automation. |
| **R3** | X7, X9 (the 桜川市/緑市 rename, 屋上緑化→グリーンパートナー) | `RULE-UNENFORCEABLE` | 4 of 4 | `.agents/web-topic-research/SKILL.md` §"The honest limit" | The skill correctly says subject identity cannot be mechanized, then leaves the human pass as prose. Convert it to a **procedure with an artifact**: add to `jlpt-test-generation` step 3.5 — "Before harvesting, paste the previous two `logs/topics.json` rows into your working notes and write one line per new seed: *same subject as row N? y/n, why*. A harvest may not be run until that list exists." A rule the author must produce output for gets done; a rule they must remember does not. Add the shipped example (さくらコイン ↔ みどりコイン: same 20%, same 2,000pt cap, same expiry month) to the skill's example list. |
| **R4** | X16 | `GATE-BLIND` | 3 of 4 (test 3 measurable; tests 2/4 show the paper-side symptom) | `tools/check_consistency.py` | The blend-contract distinctness check is exact-string. Add a **token-overlap** check over the spec's topic-level surfaces, reusing `merge_seeds.check_topic_reuse()`'s tokenizer: `check("no two blended spec surfaces share a >=2-char content token", ...)`. That catches マイボトル×2, スマート農業×2, 記憶×2 in the spec on disk right now — it would not have caught さくらコイン/みどりコイン (R3's job), but it costs nothing and fires today. |
| **R5** | X14, X15 | `GATE-BLIND` + `RULE-MISSING` | 1 of 4 measurable (only test 3 has a spec; tests 1/2/4 unverifiable) | `tools/check_consistency.py`, `.agents/web-topic-research/SKILL.md` §Step 1 | (a) `merge_seeds.validate_harvest()` aborts on the harvest on disk, yet the spec it produced sits there — the gate never runs the validator. Add to `check_harvest_hygiene()`: `try: merge_seeds.validate_harvest(seeds); except SystemExit as e: check(..., False, str(e))`, so a harvest the pipeline would refuse cannot stay on disk behind a green gate. (b) No rule says a seed's `facts` must be *findable in the cited document*. Add to `web-topic-research` Step 1: "Every entry in `facts` must be a paraphrase of a sentence you can point to on the fetched page. If you cannot point to it, the fact does not go in the harvest — a real URL with invented facts is worse than no seed, because it survives QA's URL fetch." Name the shipped example (給水/割引 attributed to `h23_lca_01.pdf`, which contains neither word). |
| **R6** | X17 | `RULE-UNENFORCEABLE` | 1 of 4 measurable | `tools/check_consistency.py`, `.agents/web-topic-research/SKILL.md` §Step 4 | The 30–60% band is enforced by `merge_seeds.py` on **allocation**; nothing checks **consumption**. Add a gate check for the two leftover surfaces: `check("every carrier_seed / qr_situation_seed in the spec appears in the paper", ...)` by searching each seed's ≥2-char content tokens in `言語知識・読解.md` 問題1–8 and 聴解問題4 — allocated-but-idle seeds mean the surface was authored off-contract at 0% web, and an idle seed is also free to collide with the next paper (it did: the 図書館電子書籍 seed was test 4's 問題10(2)). |
| **R7** | X19 | `GATE-WRONG` | 3 of 4 | `tools/check_consistency.py`, `.agents/item-pool-sampling/scripts/sample_items.py` | The gate compares historical ledger draws against the **current** `DRAW`, so retuning `DRAW` retroactively "corrupts" every past test and trains readers to ignore the message. Fix by stamping the contract into the record: have `sample_items.py` write `"draw": dict(DRAW)` into each new history entry, and change the gate to `check("each history entry records exactly its own recorded draw", ...)` , falling back to a **skip with an explicit note** for pre-stamp rows rather than a failure. Re-verify nothing else was hidden behind those four noisy rows. |
| **R8** | X20 | `PIPELINE-GAP` | 3 of 4 | `.agents/item-pool-sampling/SKILL.md`, `tools/check_consistency.py` | Three distinct ledger hygiene problems, one procedure missing: no documented way to retire a draw. Add to `item-pool-sampling`: "A test that is deleted from `tests/` is retired by setting `"retired": true` on its history entry — never by renaming it, and never by deleting the entry. Retired entries are skipped by `recency_map()` (so their items return to the pool) but keep their slot in the history so the LRU window is not resequenced." Then `recency_map()` skips `retired`, and the gate adds `check("no ledger entry was removed since HEAD~", ...)` (shared with R1). Separately, extend the existing pools-level "one grammar point, two spellings" normaliser to run over **a single draw** as well, which fails test 3's `〜気味` + `〜ぎみだ` today. |
| **R9** | X13 | `PIPELINE-GAP` | 3 of 4 | `.agents/jlpt-test-generation/SKILL.md`, `.agents/item-pool-sampling/scripts/sample_items.py` | `logs/test_spec.json` is a single mutable file, so generating test N destroys the only record of test N−1 and QA step 6 becomes unrunnable for every paper but the newest. Make the spec per-test: `sample_items.py` writes `tests/<test_id>/test_spec.json` **and** the working copy at `logs/test_spec.json`; the gate then checks `check("every test dir carries the spec it was authored from", ...)`. Without this, steps 6.1 (target-item match) and 6.2 (answer-position compliance) are permanently unauditable for tests 1, 2 and 4. |

**Blocking effect.** R1–R9 are all `GATE-WRONG` / `GATE-BLIND` / `RULE-UNENFORCEABLE` /
`RULE-MISSING` / `PIPELINE-GAP`. Per `exam-qa-review` §6.5 every one of them **blocks the next
generation run** until applied or explicitly rejected. R1 and R2 are the two that would have
prevented X7 (ten repeated surfaces) on their own.

---

## 6. Coverage statement

**Read in full before the first tool call:** `.agents/exam-qa-review/SKILL.md`,
`.agents/web-topic-research/SKILL.md`, `.agents/jlpt-test-generation/SKILL.md`.

**Step 5 (topic table).** Built from the sources on disk, not from the specs: all four
`言語知識・読解.md` 問題9–14 read in full, all four `聴解スクリプト.txt` read in full
(every 例, every 番). The table in §2 is the artifact — 13 読解 rows × 4 + 23 聴解 rows × 4.
Errand shapes recorded for the 聴解 rows and the 問題14 flyers.

**Step 6 (provenance).** `logs/test_spec.json`, `logs/seeds.json`, `logs/ledger.json`,
`logs/adjunct_staging.json` read in full; `merge_seeds.py` (`validate_harvest`,
`check_topic_reuse`, `MAX_PER_DOMAIN`, `harvest_sha`) and `sample_items.py` (`DRAW`,
`COOLDOWN`, `recency_map`) read for semantics; `tools/check_consistency.py`
`check_harvest_hygiene()` read. `validate_harvest()` and `check_topic_reuse()` executed
read-only against the on-disk harvest. Blend shares, domain histogram and the 47-stem carrier
count computed, not asserted. Git history used as evidence for X11/X12/X19
(`7638a2f`, `1e7f44c`, `a6276a8`, `4df5631`, `58a8c8b`).

**URLs fetched (3 of 22, the sampling this step allows):**
- `https://www.maff.go.jp/j/kanbo/smart/index.html` → live MAFF portal, quoted
  「ロボット技術やICTを活用して超省力・高品質生産を実現する新たな農業を実現」; seed facts supported.
- `https://www.mhlw.go.jp/content/001305530.pdf` → real 51-page MHLW sleep guide; 睡眠休養感 ×61
  and 「男性37.5％、女性40.6％…４割以上」; seed facts supported.
- `https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf` → real 18-page 環境省
  マイボトル LCA report; **給水 ×0, 割引 ×0**; 1 of 6 attributed facts supported → X15.

**`make check` WARN lines:** not re-run — the parent supplied the two results in scope
(DRAW-count mismatches, duplicate seed URL) and asked for causes rather than re-filing. Causes
delivered as X19 (ledger correct, gate compares against a retuned `DRAW`) and X14 (the count is
**3** seeds on that URL, not 2 — itself a `GATE-WRONG` under-report).

**No file in the repository was modified.** Report only, as instructed.

---

## 7. Skips, stated

1. **Item-level QA not performed** — keys, distractors, 解説 quotes, Japanese quality, level
   band, 問題7 stem lengths, `（注N）` apparatus, 聴解 option grounding. Four other reviewers own
   these; I read the papers for **subject and setting** only. Where an item-level defect was
   unavoidable evidence for a topic finding I quoted it (T2's orphaned 屋上緑化 / 精神論 glosses,
   T3's `〜気味`+`〜ぎみだ`) and flagged it for the item reviewers rather than adjudicating it.
2. **Step 6.1 (target-item match) and 6.2 (answer-position compliance) run for test 3 only** —
   and only partially, since they are the item reviewers' scope. For tests 1, 2 and 4 they are
   **impossible**, not skipped: no spec survives (X13/R9).
3. **19 of 22 harvest URLs not fetched** — the skill caps this step at 2–3; I fetched 3 and
   chose them to span three different domains and the one URL cited by three seeds.
4. **`tests/imported-n2-2025-07` excluded from the topic table** — `exam-qa-review`
   "Imported Tests Rule" exempts imported papers from steps 5 and 6. I did **not** verify
   whether any generated topic was lifted from it (that is the item reviewers' verbatim-copy
   check), and say so here so no one assumes it was covered.
5. **`4-removed`'s paper not inspected** — no `tests/4-removed/` directory exists; only its
   ledger draw could be analysed (X20).
