# Stage 3 (build + gate) — `20260910_1`

Finished 2026-09-10 by the resuming context (the run was paused mid-stage-3 at
17:41; `qa/PAUSED-20260910_1.md` is the state file it left). **Stages 4 and 5
have not run.** Nothing is committed.

## What was read, in full, from disk

`qa/PAUSED-20260910_1.md` · `AGENTS.md` · `.agents/jlpt-test-generation/SKILL.md`
· `.agents/exam-blueprint/SKILL.md` (§"Topic themes", §"The four theme rules",
§"logs/topics.json", the `key`/errand section) · `.agents/choukai-audio/SKILL.md`
(all of it, Part 0 first) · `.agents/exam-qa-review/SKILL.md` §4 (the composed-paper
replacement checks). Plus, as evidence: `tools/compose_choukai.py`
(`previous_slot_clips`, `freshest`, `key_spread`), `tools/check_consistency.py`
(`check_exam_audio_hosting`, `check_note_band_reuse`, `check_topics_*`), this
paper's `言語知識・読解.md` / `聴解スクリプト.txt` / `聴解.md` in full,
`logs/choukai_draws.json`, `logs/topics.json` rows for `20260909_1` and
`20260907_1`, `logs/upload_manifest.json`, `logs/ledger.json`, and
`refs/JLPT_N2_NEW/answer_keys.json` (the 31-sitting key set — tracked, no binary
needed).

## Commands run, in order, with outcomes

| # | command | outcome |
|---|---|---|
| 1 | `make check` (baseline) | exit 2 — **1 FAIL, 157 WARN**. Reproduces the state file's claim exactly. |
| 2 | `shasum -a 256 tests/20260910_1/聴解.mp3` vs manifest | matched (`7d13348a…`) — claim reproduced by real hash, not the gate's mtime cache |
| 3 | `gh release view audio` | `20260910_1.mp3` present, 40,891,053 B — the uploaded asset was the audio on disk |
| 4 | (edit) `tools/compose_choukai.py::freshest()` + 3 SKILL.md docs | root fix for the cross-slot clip repeat found by the topic pass (below) |
| 5 | `make mp3 20260910_1 SEED=10323372` | re-composed. 44.4 min, 34 chapters. **No starvation note.** |
| 6 | `make booklet 20260910_1` | both HTML rebuilt |
| 7 | `make sheet 20260910_1` | `解答.html` + `練習.html`; expected notice that 71 言語知識・読解 items have no 詳細解説 yet (Stage 5) |
| 8 | `make upload-files TARGET=tests TEST=20260910_1` | 1 asset uploaded (42.6 MB); manifest updated |
| 9 | `make check` | exit 2 — **1 FAIL, 157 WARN**; diff against run 1 is three `ok` lines whose counts moved with the new draw, nothing else |
| 10 | (write) `logs/topics.json` row | appended |
| 11 | `make check` | exit 2 — **2 FAIL**: the new one was `check_topics_notes_quotes` on two 「…」 spans in my own `notes` that are not in the paper |
| 12 | (edit) those two spans → backticks | the rule is 「」 means "this string is in the paper" |
| 13 | `make check` (final) | exit 2 — **1 FAIL, 157 WARN**. Baseline restored. |

No `make sample`, no edit to any other test's folder, no Stage 4, no Stage 5,
no commit.

## The state file's claims — which reproduced

| claim | verdict |
|---|---|
| seed 96722689, ledger at 26 draws, no rerolls | **reproduced** (`logs/ledger.json` last entry: `20260910_1`, seed `96722689`, 2026-09-10 16:22:57; 26 entries) |
| `言語知識・読解.md` sha `179d0566…` | **reproduced** — that is the **sha256**; the repo's own stamp is sha1-12 `a12f0077186e`. Same bytes, unchanged since 17:30 |
| `previous_slot_clips()` fixed at the root (greatest id below this paper's) | **reproduced** — read the code; the fix is correct and is what makes the same-slot bar real |
| same-slot repeats vs `20260909_1` = 0 | **reproduced** on the 17:38 draw, and still 0 after the re-compose |
| source mix official 18 / kanzenmoshi 5 / mondaireishuu 2 / soumatome 2 / mimikara 1 / shinkanzen 1 | **reproduced** for the 17:38 draw. **Superseded** by the re-compose (new mix below) |
| on-disk MP3 sha256 = manifest's | **reproduced** (then re-established after the re-compose) |
| `make check` = 1 FAIL / 157 WARN, the FAIL being Stage 5's `詳細解説.json` | **reproduced**, and still true at the end |
| every artifact's stamped source sha matches its input | **reproduced** at both the start and the end (table at the bottom) |

One thing the state file does not record: **every file in `tests/20260910_1/`
except `聴解.mp3` had mtime *and* ctime 19:00:49**, i.e. after the pause. The
bytes are the ones the state file measured (the sha256 above matches), so this
is a metadata-only touch — most likely the unrelated `練習.html` rebuild pass
that landed at that time. No content moved; I verified by hash rather than by
timestamp.

## Whole-paper pass: one topic, one surface

Themes are filled from the **shipped** surface, not the spec draw. `20260909_1`
and `20260907_1` columns are looked up in `logs/topics.json`.

### 読解 (13 surfaces + 問題14)

| surface | theme | subject shipped | closing move | rhetorical MOVE | 20260909_1 (same slot) | 20260907_1 (same slot) |
|---|---|---|---|---|---|---|
| 問題9 cloze | 医療・福祉 | 補聴器を数か月でしまいこむ人／静かな部屋から順に慣らす | 意外な観察 (`〜からである` 理由節閉じ) | **A** 道具は入れただけでは働かない | 地域活性化・案内図の向き | 食・繊維の切る向き |
| 問題10(1) | メディア・情報 | 字幕を出したまま見る視聴者が増え、制作側の前提が入れかわった | 反論応答 | 前提の更新 | デジタル化・「大きくする」の呼び分け | デジタル化・家族アルバムの取りこみ |
| 問題10(2) | 食 | 弁当のおかずを冷ましてから詰める理由が、作る側になって分かった | 随筆 | 経験による回収 | 科学・技術・科学館メール | 子育て・家族・上ばきを買う役目 |
| 問題10(3) | 行政・手続き | 市民課の呼び出しが名前から番号札の番号だけになる通知 | 実用文・分類外 | — (通知) | 子育て・家族・予定表の書き写し | 地域活性化・物産展の区画変更メール |
| 問題10(4) | 地域活性化 | 募集に持ち場と時間を並べたら手伝いの申し出が三倍になった | 主張 | **B** 原因の付け替え（意識→提示の仕方） | 文化・伝統・銭湯の湯温の札 | 防災・町内会が集会所を早く開ける |
| 問題10(5) | 住まい | 換気扇の異音の点検を留守中に頼む、鍵の渡し方の問い合わせメール | 実用文・分類外 | — (メール) | 医療・福祉・貸し出し受け取り場所 | スポーツ・余暇・道に迷った体験談 |
| 問題11(1) | スポーツ・余暇 | 卓球開放日に通い続けるかは腕前でなく初日に名前を呼び合えたか | 条件提示 | **B** 原因の付け替え | 人間関係・断れる小さな頼み | 環境・雨水タンクの補助 |
| 問題11(2) | 交通 | 動く階段の片側空けは、乗り口の列で失う数分のほうが大きい | 反論応答 | 部分最適の反転 | 睡眠・健康・靴下と足の熱 | 交通・便数と待ち時間 |
| 問題11(3) | 文化・伝統 | 風呂敷の平包みと真結びは、渡したあと何が起きるかで選び分ける | 説明 | 二項の並置 | 教育・「わかりましたか」の問い方 | メディア・情報・広報紙のはがき |
| 問題11(4) | 旅行・観光 | 記念の置き物より、日々使う麻の布巾が旅の記憶を連れて戻る | 随筆 | 常識の反転（値打ち→使用） | 防災・帰宅と腰を下ろせる場所 | 人間関係・会えた回数と親しさ |
| 問題12(A) | デジタル化 | 申し込みが止まるのは慣れでなく画面の外の用事、書きかけを預かれ | 主張 | **B** 原因の付け替え | 交通・踏切と歩道橋 | 住まい・家具を買う順番 |
| 問題12(B) | デジタル化 | 入れてみたら伸びたのは慣れない人でなく若い世帯だった | 意外な観察 | 予想外の受益者 | 交通・同上 | 住まい・同上 |
| 問題13 | 環境 | 給水機が使われ続けるのは置き場所でなく足元を整える手がある建物 | 条件提示 | **A** 道具は入れただけでは働かない | メディア・情報・調査の出どころの一行 | 働き方・応援の受け入れ準備 |
| 問題14 | 子育て・家族 | かえで市子育て送迎サポートの案内（四区分の時間・料金・初回の顔合わせ） | — (案内) | — | スポーツ・余暇・運動広場の夜間開放 | 旅行・観光・旅の道具の貸し出し |

Closing-move tally: 実用文・分類外 2 / 随筆 2 / 主張 2 / 反論応答 2 / 意外な観察 2
/ 条件提示 2 / 説明 1 — **no shape over 2**, and every one of the thirteen
assignments the authors were handed holds on the shipped prose (checked
sentence by sentence, not from the brief).

### 聴解 — 29 items (draw audit; every 問題4 row included)

| slot | clip | subject shipped | theme | 20260909_1 same slot | 20260907_1 same slot |
|---|---|---|---|---|---|
| 1-1 | `soumatome:cd2-32` | 図書館の案内板の前で、明日は休館日なので土曜に来ると決まる | 教育 | 音楽教室のクラス変更 | 断水の知らせ |
| 1-2 | `2025-07:問題1-2` | 科学館の講演会準備、後回しの資料の印刷にすぐ取りかかる | 働き方 | カフェの調理の手伝い | 休講の知らせの入れ方 |
| 1-3 | `2025-07:問題1-3` | 文房具会社、開発メンバーの担当割りを決めておく | 働き方 | 宿題は掲示で自分で確かめる | 読む本を二さつ選ぶ |
| 1-4 | `2023-07:問題1-4` | 建築設計事務所、照明器具の素材をガラスから和紙へ | 働き方 | 未提供のピザとコーヒー | 二人組の巡回表を作る |
| 1-5 | `shinkanzen:cd2-47` | 市民サッカークラブ、今日のメールに駐車場がないことを書く | スポーツ・余暇 | 自転車の預かり場所を調べる | お茶にとろみをつける依頼 |
| 2-1 | `2023-07:問題2-1` | 林業イベントで一番の楽しみは基本作業の体験 | 環境 | 荷物の到着日と時間 | 行事の知らせに参加資格を入れる |
| 2-2 | `kanzenmoshi:cd1-13` | 今日眼鏡なのは使い捨てコンタクトを切らしたから | 睡眠・健康 | 前髪を切りすぎた | 帰る日を一日おそくする理由 |
| 2-3 | `2021-07:問題2-3` | 大学建設の住民アンケート、どちらとも言えないが約三分の一 | 地域活性化 | マラソン引退の理由 | 書類の出し方は順番制 |
| 2-4 | `2025-07:問題2-4` | 公園ボランティアを始めたきっかけは花を育てたい望み | 地域活性化 | 鉛筆画で気に入っている点 | 古紙は台車で取りに回る |
| 2-5 | `2025-12:問題2-5` | ピザ屋の売り上げは言い切る広告で伸びた | 消費・経済 | 五千メートルの勝因 | 峠は鎖なしで通れる（意外） |
| 2-6 | `2023-07:問題2-6` | 共同研究で一番難しかったのは各国からの協力 | 科学・技術 | 勉強会の開始時間 | 給湯機の取りかえ時期 |
| 3-1 | `2023-12:問題3-1` | 動物病院の先生、犬の健康に必要なこと | 医療・福祉 | 小さな宿が予約で埋まる理由 | 会議そのものが変わった |
| 3-2 | `2021-07:問題3-2` | 留守番電話、傘があるかの確認依頼 | 人間関係 | 南村の移住支援 | 隣の人が三十分話す形 |
| 3-3 | `mimikara:cd2-14` | 電子書籍を利用する理由の調査 | デジタル化 | **通信販売を利用する理由の調査** | 森の二つのお願い |
| 3-4 | `2025-12:問題3-4` | 固形石けんのいいところ | 消費・経済 | 地下鉄が深くてこわい | 手ぬぐいのはしをぬわない理由 |
| 3-5 | `kanzenmoshi:cd1-21` | レジは客と直接接するので気を使って大変 | 働き方 | 設備より社員全員の節電 | タブレットで学校に分かること |
| 4-1 | `2025-07:問題4-1` | おかゆすら食べられなかった→何も食べられなかったのか | 睡眠・健康 | 本屋ついでの食事 | 先方の社長の到着 |
| 4-2 | `2021-07:問題4-2` | けがは大したことない→そりゃ、よかった | 人間関係 | 映画がいまいち | 体の具合 |
| 4-3 | `2021-07:問題4-3` | ご迷惑をおかけしました→とんでもない | 人間関係 | 社長が呼んでいる | メールの確認 |
| 4-4 | `kanzenmoshi:cd1-37` | しまった場所が分からない→また忘れたのか | 人間関係 | 去年の優勝校だから負ける | 中心になって進めて |
| 4-5 | `2021-07:問題4-5` | 代表に選ばれたからには→精一杯やる | 教育 | 今日は休みか | 面会時間 |
| 4-6 | `2021-07:問題4-6` | **森君が遅刻なんて、ありえない→いつも時間守るのに** | 人間関係 | 電車事故で歩いて帰った | マスクの着用 |
| 4-7 | `2025-12:問題4-7` | 卒論の締め切り→とにかく間に合わせる | 教育 | **森さんに限って遅刻はない** | 新人が気が利く |
| 4-8 | `kanzenmoshi:cd1-30` | 取っといてもいい→もう使わない | 住まい | 出張の急な代役 | 手の空いたときの手伝い |
| 4-9 | `kanzenmoshi:cd1-33` | 連絡したほうがいい→とってみます | 働き方 | 年齢を問わず参加できる | 新システムの慣れにくさ |
| 4-10 | `2021-07:問題4-10` | レストラン行ったことある→あそこまぁまぁ | 食 | 荷物を夕方まで預かって | お茶と菓子を辞退 |
| 4-11 | `2024-07:問題4-11` | 迷った挙句→いろいろ悩んだんだね | 教育 | 発送作業を手伝ってもらう | サンプルの置き場所 |
| 5-1 | `2022-07:問題5-1` | 演劇部の衣装のペンキを飾りを縫い付けて隠す | 教育 | パン屋、パンを小さくする | 市役所、見本の机を移す |
| 5-2 | `2021-12:問題5-2` | 防災フェア、先着のヘリコプター→応急手当 | 防災 | 語学研修の宿を一つずつ選ぶ | 文化センターの四教室 |

### Reading the table

- **Each surface against its OWN draw.** The 12 `reading_topics` entries are
  `{theme, origin:"authored", avoid:[…]}` — there is **no drawn subject
  string** for a 読解 surface any more, so the read is: does the shipped subject
  sit inside its assigned theme, and is it absent from that theme's `avoid`
  list? **All 12 assigned themes are shipped on the surface they were assigned
  to** (子育て・家族→問題14, 行政・手続き→10(3), スポーツ・余暇→11(1),
  メディア・情報→10(1), デジタル化→12, 旅行・観光→11(4), 文化・伝統→11(3),
  環境→13, 住まい→10(5), 交通→11(2), 食→10(2), 地域活性化→10(4)), and the
  問題9 cloze composes the 13th theme 医療・福祉, distinct from all of them. **No
  surface moved off its draw; no `origin: "reauthored"` stamp is needed.** I
  grepped every `avoid` list for the shipped subject's own tokens: the three
  nearest entries are 15, 5 and 6 papers back (`20260821_1` 問題10(1) 家の煮物,
  `20260904_1` 聴解4-10番 修繕の立ち入り, `20260904_3` 問題11(3) 軽い運動の会),
  all different situations and all far outside the two-paper window.
- **Theme rules 1–4 (exam-blueprint).** Headline set = 問題9 医療・福祉 / 問題12
  デジタル化 / 問題13 環境 / 問題14 子育て・家族 / 聴解問題5 教育 + 防災 — five
  different themes (rule 1 ✓). None of the four 読解 headline themes appears on
  another 読解 surface (rule 2 ✓). All thirteen 読解 themes distinct (rule 3 ✓).
  Against `20260909_1` {地域活性化, 交通, メディア・情報, スポーツ・余暇,
  消費・経済, 住まい}: no overlap; against `20260907_1` {食, 住まい, 働き方,
  旅行・観光, 行政・手続き, 文化・伝統}: no overlap (rule 4 ✓, and the budget of
  one repeat two papers back is unspent). `check_topics_themes` re-derives all
  four from the row I wrote and passes. Shipped 聴解 theme tally (a draw audit,
  not a cap): 働き方 5, 教育 5, 人間関係 5, 地域活性化 2, 睡眠・健康 2,
  消費・経済 2, and 1 each of スポーツ・余暇/環境/科学・技術/医療・福祉/
  デジタル化/住まい/食/防災 — max 5, well under the 8–11 the skill measured
  across the corpus.
- **Rule 4b (headline SUBJECTS against the whole previous paper).** The cloze
  (補聴器) and 問題12/13/14 were each diffed against all 14 読解 and 29 聴解
  subjects of `20260909_1`: no match. Same setting, different issue, recorded as
  the rule requires: 問題12 (役所の申し込み画面) sits in the same 窓口・デジタル化
  territory as `20260909_1` 問題10(1) (「大きくする」の呼び分け) — the issue is
  書きかけの保存 vs 語の呼び分け.
- **No topic twice inside this paper.** Checked 読解×読解, 読解×聴解 and the
  cloze against all eleven 問題4 stimuli specifically. The only shared domain is
  読解問題11(1) (市の体育館の卓球開放日) × 聴解1-5番 (市民サッカークラブ) — a
  domain, which a composed paper is allowed to share, with no shared decisive
  detail (名前を呼び合う相手 vs 駐車場がないこと). `make check` independently
  confirms 問題14 shares no decisive number with any 聴解 item.
- **Rhetorical MOVE, read across both halves (cap 2).** Two moves are carried by
  more than one surface:
  - **A — 「道具は据えただけでは働かない、周りの手当てが要る」**: 問題9 (補聴器)
    and 問題13 (給水機). **Two, at the cap.** Both are headline surfaces and the
    echo is closer than the cap contemplates, but their closings differ
    (意外な観察 / 条件提示) and their subjects and themes are unrelated. Recorded,
    not repaired.
  - **B — 「原因を本人の資質（関心・腕前・慣れ）から提示の仕方・仕組みへ付け替える」**:
    問題10(4), 問題11(1) and 問題12(A). **Three — one over the cap.** See the
    findings below.
  No 聴解 talk carries either move: the nearest, 聴解2-6番 (難しかったのは技術より
  各国の協力), ranks difficulties inside one project rather than reattributing a
  cause, so the cross-half half of the rule is clean.
- **問題12's own cross-test column**: デジタル化 (this paper) / 交通 (`20260909_1`)
  / 住まい (`20260907_1`) — one topic per paper ✓.
- **Errand identity across three papers** (the `shapes` column, since no
  draw-time check survives for authored/composed scenarios): read down all 29
  rows against both previous papers. One coincidence, at 聴解3-3番 — see
  findings.

## Findings this pass produced

### F1 — REPAIRED: the previous paper's slot-free clips came back a slot over

`20260910_1` as composed at 17:38 carried **two of `20260909_1`'s own
recordings**: `mondaireishuu:問2-1` (its 問題2-2 → our 問題2-1) and
`mondaireishuu:問3-1` (its 問題3-3 → our 問題3-1). A candidate who sat both papers
would have heard the same two items again one paper later.

Root cause: `previous_slot_clips()` bars the previous paper's clip **per slot**,
which is exact for an official draw (slot-preserving: item *k* of 問題N is only
ever drawn from item *k* of 問題N) and **blind to a hand-declared one**, which is
banked `slot: 0` and placed wherever the 大問's textbook slots fall. Least-used-
first makes it worse by construction: a freshly banked clip has 0 uses, so the
next paper reaches for it, and it is *still* among the least-used the day after —
both offenders were 問題例集 items banked 2026-09-09. Measured over all 25
consecutive transitions on record: **14 of them repeat at least one clip in a
different slot**, every one of them slot-free. Same class as
qa-report-20260909_1 F4, one layer further out.

Repair, at the root: `compose_choukai.freshest()` now takes the previous paper's
**whole draw** as an additional bar for the slot-free half (the per-slot bar is
unchanged, and for official clips the new set adds nothing). Docs updated in the
three places that state the rule: `choukai-audio` Part 0 rule 2,
`jlpt-test-generation` §"One topic, one surface", `exam-qa-review` §4 check 1.

Re-composed at the **same seed** (`10323372`) — **16 of 29 item slots moved**,
plus 4 of the 5 section preambles. After it: 0 same-slot repeats and **0
any-slot repeats against `20260909_1` and against `20260907_1`**, 0 duplicates
inside the paper, no starvation note. New source mix: official 18, kanzenmoshi 7,
soumatome 2, mimikara 1, shinkanzen 1 = 29 (問題例集 fell to 0 because both its
drawn items were the barred ones). A side effect worth recording: the 17:38 draw
also had 聴解2-4番 (公園ボランティアを始めた理由) beside 聴解5-1番 (東公園のゴミ
対策をボランティアが提案) — two 公園ボランティア items in one paper, invisible to
`name_clash` because they share no person name. The re-draw removed it.

### F2 — OPEN, for Stage 4: the rhetorical-MOVE cap is exceeded by one

「原因を本人の資質から提示の仕方・仕組みへ付け替える」 is the move of 問題10(4)
(「人が集まらないのは関心が薄いからだ、という見方には無理がある」→書き方を変えれば
手は挙がる), 問題11(1) (腕前ではなく、こちらが名前を呼ぶ場面を用意したか) and
問題12(A) (「機械に慣れていないからだと片づけられがちである」→止まる理由は画面の
外). Cap is two surfaces across both halves. Not string-decidable, so no check
sees it; the gate's `not-A-but-B` nets read 2 and 0 because all three write the
reframe without the marker family.

Not repaired here: this is authored 読解 prose, Stage 3 does not author, and any
edit to 問題10–14 prose obliges the full re-grep protocol plus a fresh-eyes
re-read of the edited passage. **Cheapest repair if Stage 4 agrees:** re-angle
問題10(4) — it is a 問題10 短文, the smallest surface carrying the move, and its
theme (地域活性化) and closing shape (主張, currently 2 of a cap of 2) both have
room to move.

### F3 — OPEN, for Stage 4: 聴解4-6番 repeats the previous paper's 森/遅刻 item

This paper's 問題4-6番 is 「森君が遅刻なんて、ありえないよね」 → 「森君、いつも時間
守るのにね。」 `20260909_1` shipped 問題4-7番 on `森さんに限って、まさか試合に遅刻
することはない`. **Different clips from different sittings, near-identical
content, one paper apart** — and `choukai-audio` names this exact pair as the
case the within-大問 name-clash penalty was written for. Nothing catches the
cross-paper version: the clip-id bar sees two different ids, and
`compose_choukai.name_clash()` only scores names inside one paper.

Not repaired here, deliberately. The repo already records that cross-clip
content similarity is **not string-decidable** (raw similarity pairs below the
officials' own within-大問 maximum, and a hard name ban fires on a real sitting),
so the only mechanical lever is extending `name_clash` to the previous paper's
names — which would fire on 山田/田中/鈴木-class names that official sittings
reuse constantly, and must be measured against the archive before it lands. A
second re-draw at Stage 3 to chase a content near-duplicate is also how a paper
enters re-draw-forever, which `jlpt-test-generation` tells us to report instead.
**Recommendation to Stage 4:** decide between accepting it with the reason
recorded, and a measured `name_clash` widening.

### F4 — OPEN (observation): 聴解3-3番 repeats the previous paper's item SHAPE in the same slot

Ours: an announcer reports a survey and the key is 「電子書籍を利用する理由」.
`20260909_1` 問題3-3番: an announcer reports a survey and the key is 「通信販売を
利用する理由」. Same slot, same 話の型, one paper apart; different subject,
different recording, different theme tag (デジタル化 vs 消費・経済), so
`check_slot_theme_repeat()` cannot see it. On a composed paper there is nothing
to re-angle — this is the draw audit, and the honest disposition is to report it.
Candidate root-cause row: bank records carry no 話の型 tag, so the composer
cannot bar a shape repeat in the same slot the way it now bars a clip repeat.

## 聴解 draw audit (final draw)

- **Same-slot repeats vs `20260909_1`: 0. Any-slot repeats: 0.** Same against
  `20260907_1`: 0 and 0. No clip appears twice inside the paper.
- **Source mix** (`logs/choukai_draws.json`): official 18, kanzenmoshi 7,
  soumatome 2, mimikara 1, shinkanzen 1 = 29. Drew from 8 sittings
  (2021-07 ×4, 2021-12 ×1, 2022-07 ×1, 2023-07 ×3, 2023-12 ×1, 2024-07 ×1,
  2025-07 ×4, 2025-12 ×3).
- **Starvation: none.** The composer printed no starvation note, and the
  zero-repeat result above shows no slot had to drop a bar. It did print the
  standing note that 2 figure items (`2021-12:問題1-5`, `2022-12:問題1-2`) are
  excluded from the draw as uncomposable.
- **Per-section key tally** (`exam-qa-review` §4 check 5): 問題1 max 3, 問題2
  max 2, 問題3 max 3, 問題5 max 2 — **every four-option 大問 at or under the
  ceiling of 3**. 問題4 (three options, eleven items) keys option 1 five times.
  Check 5's ceiling of 3 is derived from four-option sections and is
  arithmetically unreachable in 問題4 (11 items over 3 options force a mode of
  ≥4), so I measured the real band off `refs/JLPT_N2_NEW/answer_keys.json`, all
  31 sittings: **問題4's modal key runs 4–7, median 5** (4 ×13, 5 ×14, 6 ×3,
  7 ×1); 問題1 2–4, 問題2 2–4, 問題3 2–4, 問題5 1–3. This paper's 5 is the
  archive's own median. (The pre-re-compose draw was at 6 — inside the band but
  at its 87th percentile; the re-draw improved it.)
- The audio round-trip (`choukai_segment.py`) and the two by-ear spot checks are
  `exam-qa-review` §4 checks 2–3 and belong to Stage 4; they are **not** run
  here. Stage 4 must re-run checks 1–5 in full, because the half was re-composed
  after the state file was written.

## `make check` — every line naming `20260910_1`, with its disposition

Final run: **exit 2, 1 FAIL, 157 WARN**, identical to the entry baseline.

| line | disposition |
|---|---|
| **FAIL** `詳細解説.json explains every keyed item (30 entries for 101 keys)` | **Expected at this stage.** The 30 聴解 entries are written by `make mp3`; the 71 言語知識・読解 entries are Stage 5's. Clears when Stage 5 runs. Not mine to fix. |
| **WARN** `the errand-rotation check compares most of the draw (1/44 = 2% keyed)` | **Systemic, not this paper.** The repair named in the message is in `pools.json` (give every new entry an errand `key`), not in the test. Carried forward; it names the same ratio on every recent paper. |
| **WARN** `the 問題8 form-family check compares most of the draw (1/5 = 20% family-tagged)` | **Systemic, not this paper.** Same shape: the repair is the hand-maintained `grammar_form_families` map in `pools.json`. Carried forward. |
| `skip` `no 聴解1/2/3/5 errand repeats 20260909_1's` | Not a pass, by the check's own words — it defers to the `shapes` column. **Read**: see the 聴解 table and F3/F4 above. |
| `skip` ×6 (セクション構成表 quotes / validate_script / 問題5 質問1・質問2 markers / 問題5 prints no options / 問題5 enumeration order / 聴解 authoring-register-pacing family) | All are the composed-paper exemptions `choukai-audio` Part 0 and `exam-qa-review` §4 declare. Correct for this paper. |
| `skip` `詳細解説 carries no scaffold placeholder — no 模範解答.html` | Correct: Stage 5 has not run. |
| `skip` `聴解.mp3 was built with today's pacing` | Correct: a composed timeline has no synthesis constants, hence no `pacing_sha`. |
| every other line naming this test (≈110 `ok`) | pass |

Lines worth quoting because they are the ones a repair would have broken:
`no （注N） headword is reused as plain text in 問題1-9 or the 聴解 script` **ok**
(this is `check_note_band_reuse`, and it is the answer to outstanding item 4 —
see below); `no 問題7/8/9 keyed form appears more than 1× in the 問題10-14 prose,
or even once in the same 文末/連用/連体 frame as its stem` **ok**; `聴解.mp3 was
built from today's 聴解スクリプト.txt (script_sha 17a65b38bee0)` **ok**;
`36 exam MP3(s) are on the 'audio' release` **ok**.

### `check_note_band_reuse`, re-run with every section present

Green. The 読解 author wrote 28 （注N） glosses without being able to see 問題1–9
or the 聴解 script (parallel authoring); the check compares every headword
against both, and now that the merged `言語知識・読解.md` and the composed
`聴解スクリプト.txt` are on disk it has actually run over them. It also ran again
after the re-compose, i.e. against the **new** listening script — worth saying,
because a re-drawn 聴解 half is new text for this check to search. 28 glosses,
0 reuses. (`読解 has substantial （注N） glosses … got 28` is inside the official
current-era band 27–61.)

### No 読解 prose was edited

The rule "a repair made to clear one gate check is not verified by that check
passing / re-grep every 問題7/8/9 keyed form after ANY edit to 問題10–14 prose"
did not trigger: **I changed no character of `言語知識・読解.md`** (sha unchanged
at `a12f0077186e` from 17:30 through now). The keyed-form check is green on the
same bytes the authors shipped.

## The `logs/topics.json` row

Appended, with all eight fields: `surfaces` (43 keys — 14 読解 + 29 聴解, no 例
because a composed script has none), `themes` (43), `shapes` (29, one per 聴解
item, derived from the shipped script and 解説, not from the drawn scenarios),
`closing_moves` (13 読解 surfaces), `voices` (14), `persona` (14, max 2 per token:
解説者 2, 職業人 2, 生活者 2, and one each of 市（通知）/世話役/住人（依頼）/調査者/
観察者/実務者/研究者/市（案内）), `claim` (43), `notes`.

`notes` records, as asked: the 問題9 row (theme 医療・福祉, closing move 意外な観察,
final-sentence template 分類外「〜からである」理由節閉じ) and its **sixteen option
strings**; both `make mp3` runs and why; the 16-slot diff; the key tally with the
31-sitting measurement behind it; F2/F3/F4 as open findings; the same-setting-
different-issue notes; the unspent listening draws; and the per-test invariant
for the gate ("the only lines naming this paper are 2 pool-coverage WARNs and the
Stage 5 FAIL") rather than a repo-wide total.

`check_topics_notes_quotes` FAILed my first draft on two 「…」 spans that quote
nothing in the paper — the convention is that 「」 in a row asserts "this string
is on the paper". Both are backticks now, and the check reads 9 spans and passes.

## Also on the tree, and NOT this paper's work

An unrelated `exam-app` feature (a 読解-translation toggle in 練習モード) landed
during the pause: `build_practice.py`, `build_model_answer.py`,
`check_consistency.py` (two new checks), two SKILL.md files, and all 35 tracked
`練習.html`. Left exactly as found.

Riding on this run and needing its own line at commit time:
`tools/compose_choukai.py` — **two** root fixes now, `previous_slot_clips()`
(previous context) and `freshest()` (this one). Both change the draw for every
future paper. `logs/choukai_bank.json` also carries the previous context's
one-line 解説 quote fix in `.agents/choukai-audio/references/textbook_items.json`.

## Artifact shas at hand-off

| file | sha1-12 | stamped in |
|---|---|---|
| `言語知識・読解.md` | `a12f0077186e` | `言語知識・読解.html`, `解答.html`, `練習.html` |
| `聴解.md` | `6f3326aa0281` | `聴解.html`, `解答.html`, `練習.html` |
| `聴解スクリプト.txt` | `17a65b38bee0` | `解答.html`, `練習.html`, and `聴解_チャプター.json`'s `script_sha` |
| `聴解_チャプター.json` | `91d240a629e2` | `解答.html`, `練習.html` |
| `詳細解説.json` | `ca7a4e017efb` | `練習.html` |
| `詳細解説.vi.json` | `32d16f632c63` | `練習.html` |
| `聴解.mp3` | sha256 `f90a02333c1854986023…` | `logs/upload_manifest.json`, and uploaded to release `audio` |

Duration 44.4 min, 34 chapters.

## What Stage 4 inherits

1. F2 (MOVE cap, 読解, repairable), F3 (森/遅刻, 聴解, judgment), F4 (問題3-3 shape
   echo, 聴解, observation).
2. `exam-qa-review` §4 checks 1–5 **must be re-run in full** — the listening half
   was re-composed after the last verification.
3. Two root-cause candidates for its table: bank records carry no 話の型 tag
   (F4); `name_clash` has no cross-paper axis (F3). A third, milder one: a
   composed paper still burns 21 `listening_scenarios` + 11 `quick_response`
   draws in `logs/ledger.json` that never reach the paper, which is also what
   makes the errand-rotation WARN unavoidable.
