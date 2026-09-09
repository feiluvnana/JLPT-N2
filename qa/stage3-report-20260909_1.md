# Stage 3 (build + gate) — 20260909_1

Written 2026-09-09 by the stage-3 context. Sole writer on `tests/20260909_1/`
for the duration.

Source shas at hand-off (what stage 4 must re-read and compare):

| file | sha1[:12] |
|---|---|
| `tests/20260909_1/言語知識・読解.md` | `cada56c17af5` |
| `tests/20260909_1/聴解スクリプト.txt` | `f24673424c0a` (also `聴解_チャプター.json.script_sha`) |
| `聴解.mp3` | 46.4 min / 2783.6 s, 34 chapters, `bank_version` 2, uploaded to the `audio` release |

---

## 1. What I read, in full, from disk

1. `AGENTS.md` (via `CLAUDE.md`)
2. `.agents/exam-app/SKILL.md`
3. `.agents/choukai-audio/SKILL.md` — whole file, Part 0 first
4. `.agents/jlpt-test-generation/SKILL.md` — whole file; §"Stage 3 — build + gate"
   and §"One topic, one surface" are the contract this report answers
5. `.agents/exam-blueprint/SKILL.md` §"The four theme rules", §"Rotation model",
   §"`logs/topics.json`" (row format, `shapes`/`claim`/`persona`/`voices`, the
   「」-means-verbatim rule)
6. `.agents/question-authoring/references/dokkai.md` §"Thirteen surfaces" and
   §"The denominator" — to label `closing_moves` from the shipped finals rather
   than from memory
7. The three stage-2 fragments, `test_spec.json`, `logs/topics.json` rows for
   20260907_1 and 20260904_3, `logs/choukai_draws.json`
8. The docstrings of `check_key_grammar_exposure`, `check_p14_choukai_shared_decider`,
   `check_topics_themes`, `check_theme_repeat_cross_test`, `check_topics_shapes_field`,
   `check_slot_theme_repeat` in `tools/check_consistency.py` — each check's own
   documentation, read before acting on its output

## 2. The merge

`tests/20260909_1/言語知識・読解.md` was assembled mechanically from
`_sections/問1-6_文字語彙.md`, `_sections/問7-9_文法.md`, `_sections/問10-14_読解.md`:
bodies in booklet order 問題1…問題14, then ONE `# 解答(言語知識・読解)` heading, then
the `## 文字・語彙` / `## 文法` / `## 読解` key tables in the same order. Each fragment
was asserted to contain exactly one `<!-- KEY -->` marker and **no** key heading of
its own before merging (`^#+\s*(解答|【?正解)` regex, matching `strip_key()`).
No item was re-authored while merging.

## 3. Commands run, in order, and their results

| # | command | result |
|---|---|---|
| 1 | (merge script) | wrote `言語知識・読解.md`, 37,564 chars |
| 2 | grep of the 文法 author's cross-section list (pre-build) | **FAIL** predicted: 問題8 target `ように…する` ×2 — repaired, see §4 |
| 3 | `make autofix 20260909_1` | ALL CHECKS CLEAN |
| 4 | `make lint-draft 20260909_1` | ALL CHECKS CLEAN |
| 5 | `make verify-scramble 20260909_1` | exit 0; all five 問題8 items: keyed ★ survives the junction filter, ARTIFACT ok (per-card last-slot proof present), FREE UNITS 1 each (FAIL is at 2). RESULT `UNDECIDED` on all five — the tool's normal outcome; it does not decide uniqueness |
| 6 | `make mp3 20260909_1 SEED=65083608` | 46.4 min, 34 chapters; mix mondaireishuu ×4 / official ×21 / shinkanzen ×3 / soumatome ×1; 8 sittings |
| 7 | `make booklet 20260909_1` | both HTML built, `verify()` clean |
| 8 | `make sheet 20260909_1` | 101 items (71 + 30), player + chapters, storage=server, zero warnings |
| 9 | `make check` (run 1) | 3 FAILs naming this test — see §4 |
| 10 | `make choukai-bank` | 402 records; 10 sittings + 62 textbook items |
| 11 | `make mp3 20260909_1 SEED=65083608` (re-run) | byte-identical draw (verified clip-by-clip) |
| 12 | `make booklet` + `make sheet` (rebuild) | clean |
| 13 | `make upload-files TARGET=tests TEST=20260909_1` | 44.5 MB pushed to release `audio`; `logs/upload_manifest.json` updated (40 assets) |
| 14 | `make check` (run 2) | 1 FAIL naming this test (詳細解説, stage 5) |
| 15 | (append `logs/topics.json` row) | 43 surfaces, 29 of them 聴解 |
| 16 | `make check` (run 3, final) | **2 FAILs, 2 WARNs** naming this test — §6 |

`make mp3` ran before `make booklet` on both passes, as required — it writes the
whole 聴解 half (`聴解スクリプト.txt`, `聴解.md`, `聴解.mp3`, `聴解_チャプター.json`
and the 30 choukai `詳細解説` entries in both panes) and `make booklet` renders the
`聴解.md` it produced.

## 4. Hand-offs closed, and the four repairs they forced

### 4.1 The 文法 author's cross-section grep list — **closed, one repair**

Measured on the assembled 読解 prose exactly as `check_key_grammar_exposure` does
(`passage_prose()` over 問題10–14, instruction lines stripped, whitespace squeezed,
（注N） glosses INCLUDED because the check counts them).

**Every 問題7/問題9 keyed option string occurs ZERO times in the 問題10–14 prose.**

| Q | keyed string | stem frame | occurrences in 問題10–14 prose |
|---|---|---|---|
| 31 | とともに | 連用 | 0 |
| 32 | べきだ | (no frame class — bare modal) | 0 |
| 33 | をもとに | 連体 | 0 |
| 34 | にすぎない | 文末 | 0 |
| 35 | 向けだ | 文末 | 0 |
| 36 | といえば | 連用 | 0 |
| 37 | というわけではない | 文末 | 0 |
| 38 | ことだし | 連用 | 0 |
| 39 | 際 | (no frame class — 1-char 形式名詞) | 0 |
| 40 | に越したことはない | 文末 | 0 |
| 41 | て以来 | 連用 | 0 |
| 42 | くせに | 連用 | 0 |
| 48 | その結果 | 連用 | 0 |
| 49 | せざるを得ない | 文末 | 0 |
| 50 | 案内しているつもりでも | 連用 | 0 |
| 51 | 次の一歩を決める手がかり | 文末 | 0 |

The 問題8 drawn frames (`grammar_p8`, both copula spellings normalised by
`_copula_norm`): 目的表現(〜ように…する), 〜でなければ, 補足追加(〜なお…),
同時進行(〜ながら…する), 義務当然(〜ねばならない).

**`目的表現(〜ように…する)` FAILed at ×2** and, once reduced to ×1, the
same-sentence branch (`reproduced whole in one 読解 sentence`) would still have
fired — so **both** occurrences were removed, not one:

- 問題11(3): `…こちらが見えるようにするための問いで…` →
  「答えをうながす（注3）ためではなく、こちらが見るための問いで、手ごたえ（注4）はすぐにありました。」
- 問題13: `それで最後まで読まれるようになった例…` →
  「それで最後まで読まれる文章に変わった例をいくつも見てきた経験があるから、短くすること自体に反対するつもりはない。」

Neither is a closing sentence; I re-read both passages' closings after the edit and
neither closing move moved (問題11(3) 反論応答, 問題13 主張). All five 問題8 frames now
score 0 on both branches. The gate line is green **on merit**, not grandfathered.

### 4.2 `check_note_band_reuse` — **re-run now, green**

Could only run half at stage 2 (it compares gloss headwords against 問題1–9 **and**
`聴解スクリプト.txt`, which did not exist then). Re-run against the composed script:
`ok 20260909_1: no （注N） headword is reused as plain text in 問題1-9 or the 聴解 script`.
The neighbouring gloss lines are also green: 29 glosses (official current-era band
27–61, median 39), 0 orphans, all pair 1-to-1, all survive the subtraction test.

### 4.3 `make verify-scramble` — **run for real**, row 5 of the table above.

### 4.4 Two further repairs the gate forced, and one root-caused out of the test

- **`check_p14_choukai_shared_decider` FAILed on `一週間`**, shared between the 問題14
  flyer (`通訳が必要な方は、一週間前までに…`) and 聴解問題1-4番
  (「動画は申請書の締め切り後、一週間以内の提出だったんだ」). The 聴解 side is a lifted
  official clip, so the **flyer's** number moved, as the check instructs:
  「・通訳が必要な方は、十日前までにくらし相談課へお申し出ください。」 問70's option 2 and
  its 解説 were re-derived with it. **Neither key changed** — 問70=3 and 問71=4 turn on
  the 「前日までに電話」 cell and the 第二土曜 row, not on that interval. Re-checked: the
  flyer's decisive tokens are now {十日前, 三か月} and share nothing with the script.
- **問52's 解説 quoted a sentence the passage does not contain**
  (`どちらも「大きくする」と呼ばれているので、同じものだと思っている人が多い`). Replaced with
  the shipped wording 「どちらも「大きくする」と呼ばれるため、同じものだと思われやすい」.
  This is a quote-fidelity correction, not a re-authoring: the key (4) and the
  reasoning are untouched.
- **The one 聴解 quote WARN was root-caused OUT of this paper.** 聴解問題3-3番's 解説
  cell is composed verbatim from `.agents/choukai-audio/references/textbook_items.json`
  (`mondaireishuu:問3-1`), whose `kaisetsu_cell` abbreviated the script's
  「ゆっくりと買い物ができる」 to `ゆっくり買い物ができる`. Fixed in the declaration —
  the owner file — then `make choukai-bank` and `make mp3` re-run with the SAME seed.
  The draw is byte-identical (`usage_counts()` excludes the paper's own prior draw),
  verified clip-by-clip across all 29 slots.

## 5. The whole-paper topic table

Columns: this paper | 20260907_1 | 20260904_3. Themes are filled from the SHIPPED
surface. 「」 marks strings that are in the paper; everything else is description.

### 5.1 読解 (13 surfaces + 問題14)

| surface | theme | drawn theme → shipped? | closing move | rhetorical MOVE | 20260907_1 | 20260904_3 |
|---|---|---|---|---|---|---|
| 問題9 (cloze) | 地域活性化 | no draw (13th surface) — subject: a town's information boards and what changes when the map faces the way the reader walks | 主張 | *the cheap fix is the orientation, not the content* | 食 (包丁の向きと味) | 環境 |
| 問題10(1) | デジタル化 | drawn デジタル化 → yes | 説明 | *two things with one name do different jobs* | デジタル化 (アルバムの取りこみ) | 交通 |
| 問題10(2) | 科学・技術 | drawn 科学・技術 → yes (science-museum lecture logistics) | 実用文・分類外 | — (email) | 子育て・家族 | 旅行・観光 |
| 問題10(3) | 子育て・家族 | drawn 子育て・家族 → yes | 条件提示 | *acting on the day the information arrives* | 地域活性化 | 地域活性化 |
| 問題10(4) | 文化・伝統 | drawn 文化・伝統 → yes | 随筆 | *a custom has a fixed part and an adjusted part* | 防災 | 睡眠・健康 |
| 問題10(5) | 医療・福祉 | drawn 医療・福祉 → yes | 実用文・分類外 | — (notice) | スポーツ・余暇 | 文化・伝統 |
| 問題11(1) | 人間関係 | drawn 人間関係 → yes | 随筆 | *the small imposition is the signal, not the burden* | 環境 | メディア・情報 |
| 問題11(2) | 睡眠・健康 | drawn 睡眠・健康 → yes | 意外な観察 | *what tires you is not the amount but the sameness* | 交通 | 食 |
| 問題11(3) | 教育 | drawn 教育 → yes | 反論応答 | *two questions return different kinds of thing* | メディア・情報 | スポーツ・余暇 |
| 問題11(4) | 防災 | drawn 防災 → yes | 条件提示 | **the thing everyone stocks is not the thing that decides it** | 人間関係 | 教育 |
| 問題12(A/B) | **住まい** | drawn 住まい → yes | 意外な観察 / 反論応答 | **the thing everyone buys is not the thing that decides it** | **住まい** | 科学・技術 |
| 問題13 | メディア・情報 | drawn メディア・情報 → yes | 主張 | *cutting the reader's work must not cut the reader's check* | 働き方 | 医療・福祉 |
| 問題14 | **働き方** | drawn 働き方 → yes | (outside axis 2) | — (flyer) | 旅行・観光 | 防災 |

**Every 読解 surface was read against its OWN draw first.** All twelve drawn
`reading_topics` themes map 1:1 onto the twelve non-cloze surfaces as an exact
multiset; no surface wandered off its draw, so no `"origin": "reauthored"` stamp is
warranted and none was added. The cloze is the author-composed thirteenth.

### 5.2 聴解 (29 composed surfaces) — a DRAW audit, not a topic audit

| slot | subject (shipped) | theme | clip | prev paper same slot | 2 back same slot |
|---|---|---|---|---|---|
| 問1-1 | 休んだときの宿題は研究室前の掲示で確かめる | 教育 | mondaireishuu:問1-1 | soumatome:cd2-3 | 2022-07:問題1-1 |
| 問1-2 | 生花サークルのポスター、写真の位置を中央へ | 文化・伝統 | 2022-12:問題1-2 | soumatome:cd1-60 | shinkanzen:cd2-47 |
| 問1-3 | レッスンのプログラム訂正を貼り紙で告知 | 働き方 | soumatome:cd2-2 | 2022-07:問題1-3 | 2024-07:問題1-3 |
| 問1-4 | 市民文化祭への応募、まず申請書を提出 | 文化・伝統 | 2023-12:問題1-4 | 2024-07:問題1-4 | 2025-12:問題1-4 |
| 問1-5 | ホテル秋のフェア、ロビーのイベント企画案3つ | 働き方 | 2024-12:問題1-5 | 2023-12:問題1-5 | soumatome:cd2-16 |
| 問2-1 | 前髪を切りすぎて学校に行きたくない | 子育て・家族 | mondaireishuu:問2-1 | soumatome:cd1-29 | 2022-12:問題2-1 |
| 問2-2 | 実験の参加条件は一日六時間以上の睡眠 | 睡眠・健康 | 2022-12:問題2-2 | 2023-12:問題2-2 | 2023-12:問題2-2 |
| 問2-3 | マラソン選手の引退理由は指導の機会 | スポーツ・余暇 | 2025-12:問題2-3 | 2024-07:問題2-3 | 2021-12:問題2-3 |
| 問2-4 | 鉛筆画の魅力は何度でも消してやり直せること | スポーツ・余暇 | 2023-12:問題2-4 | 2024-12:問題2-4 | 2021-12:問題2-4 |
| 問2-5 | 実習生への指導、目の高さを合わせて話す | 教育 | 2022-12:問題2-5 | 2023-12:問題2-5 | 2025-12:問題2-5 |
| 問2-6 | 勉強会の反省点は開始時間の余裕のなさ | 教育 | 2024-12:問題2-6 | 2022-12:問題2-6 | soumatome:cd2-35 |
| 問3-1 | 片付けの効果 | 住まい | 2025-12:問題3-1 | shinkanzen:cd2-62 | soumatome:cd2-28 |
| 問3-2 | 写真は何を伝えたいかを意識して撮る | スポーツ・余暇 | 2024-07:問題3-2 | 2021-07:問題3-2 | 2025-07:問題3-2 |
| 問3-3 | 通信販売を利用する理由の調査 | 消費・経済 | mondaireishuu:問3-1 | 2021-12:問題3-3 | 2021-07:問題3-3 |
| 問3-4 | 仲間言葉としての方言 | 文化・伝統 | shinkanzen:cd2-59 | soumatome:cd2-41 | 2025-12:問題3-4 |
| 問3-5 | 設備より先に社員一人一人の節電 | 環境 | 2024-12:問題3-5 | 2022-12:問題3-5 | soumatome:cd2-8 |
| 問4-1 | 本屋のついでの食事の誘い → 店を知っている | 人間関係 | 2025-12:問題4-1 | 2023-12:問題4-1 | 2025-07:問題4-1 |
| 問4-2 | 今日休みかの確認 → 午後からの出勤 | 働き方 | mondaireishuu:問4-1 | soumatome:cd1-43 | shinkanzen:cd2-67 |
| 問4-3 | 部活を休みがちな理由 → バイトが忙しい | スポーツ・余暇 | 2024-12:問題4-3 | 2024-07:問題4-3 | 2025-12:問題4-3 |
| 問4-4 | 研修が物足りなかった → 自分はあれでよかった | 教育 | 2023-12:問題4-4 | 2023-07:問題4-4 | 2022-07:問題4-4 |
| 問4-5 | 電気の消し忘れの指摘 → 認めて謝る | 働き方 | 2023-12:問題4-5 | 2024-12:問題4-5 | 2022-12:問題4-5 |
| 問4-6 | チケット当選の報告 → 運がいいね | 人間関係 | **2023-12:問題4-6** | **2023-12:問題4-6** | 2022-12:問題4-6 |
| 問4-7 | 引き受けなきゃよかった → 今はよかったのだろう | 人間関係 | shinkanzen:cd2-66 | 2022-07:問題4-7 | 2021-12:問題4-7 |
| 問4-8 | 出張の代役依頼 → 本人の事情を尋ね返す | 働き方 | 2021-12:問題4-8 | shinkanzen:cd2-68 | shinkanzen:cd2-65 |
| 問4-9 | 年齢を問わず参加 → 何歳でもいいのか | スポーツ・余暇 | 2025-12:問題4-9 | 2025-07:問題4-9 | shinkanzen:cd2-69 |
| 問4-10 | やらせてほしい → 任せる | 働き方 | shinkanzen:cd2-72 | 2023-07:問題4-10 | 2024-07:問題4-10 |
| 問4-11 | 予想に反して各年代に受けている → 意外だ | 消費・経済 | 2025-12:問題4-11 | shinkanzen:cd2-67 | 2023-07:問題4-11 |
| 問5-1 | 和菓子の新商品、費用と手間をかけない店内の貼り紙 | 消費・経済 | 2021-07:問題5-1 | 2025-07:問題5-1 | **2021-07:問題5-1** |
| 問5-2 | 団体旅行、午前は作家の家めぐり／午後は筆作り体験 | 旅行・観光 | 2022-07:問題5-2 | 2022-12:問題5-2 | 2022-12:問題5-2 |

Preambles: 問題1 `2024-07`, 問題2 `2023-07`, 問題3 `2023-12`, 問題4 `2024-07`,
問題5 `2024-07`.

**Draw audit result.** ONE clip repeats the immediately previous paper in the same
slot: **問題4-6 = `2023-12:問題4-6`**, also 20260907_1's 問題4-6. It is **not**
exhaustion — that slot has 15 banked candidates and ten of them stood at one prior
use when this paper drew — it is the **mandated seed**: `compose_choukai.py` spends
least-used clips first and breaks ties from the seed, and it exposes no per-slot
exclusion, so the only way to move that one slot is to re-draw all 29 with a
different seed. The seed was fixed by the orchestrator and used verbatim, so the
repeat is **reported rather than re-drawn**, per `jlpt-test-generation`
§"One topic, one surface". 問題4 is the cheapest slot for a repeat: a single-turn
stimulus with no scenario, no printed options and no 場面.
One clip repeats the two-papers-back column in the same slot
(`2021-07:問題5-1` at 問題5-1) — a minor finding, noted. No other clip id appears in
either previous paper's draw at all, in any slot.

### 5.3 The 11 drawn `quick_response` phrases — a spec-vs-shipped divergence, not a topic row

The brief asked for a row per drawn `quick_response` phrase "with the setting
invented for it". **No setting was invented for any of them, and none of them is in
this paper.** Since 2026-09-08 the whole 聴解 half is composed from banked
recordings (`choukai-audio` Part 0), so the eleven drawn phrases —
`ご家族の方ですね。こちらへどうぞ。` / `山田さん、資料の作成、手伝ってくれて本当にありがとう。`
/ `気を遣う` / `今日は定時で上がらせていただいてもよろしいでしょうか。` / `間に合わせる`
/ `課長、来週の出張ですが、宿泊先を変更してもよろしいでしょうか。` / `願ってもない` /
`この度の障害について、取り急ぎ状況をご報告いたします。` / `都合をつける` /
`先日の打ち合わせの件、その後進展はございましたでしょうか。` /
`火災報知器が作動しました。避難してください。` — were drawn, recorded in the ledger,
and **spent by nothing**. The same is true of the 21 `listening_scenarios` themes.
The 問題4 rows in §5.2 are the eleven items the paper actually ships, and they are
lifted official/textbook stimuli. Checked against 問題9's subject specifically
(the other unpooled surface): the cloze is about the orientation of town maps, and
no 問題4 stimulus, drawn or shipped, touches signage, maps or wayfinding.
**Recommendation to the orchestrator:** stage 1 should stop drawing
`quick_response` and `listening_scenarios` for composed papers, or the spec should
mark them historical — a draw that spends a cooldown on nothing makes the ledger
lie to the next paper.

### 5.4 How the table reads

- **Rule 3** (all thirteen 読解 surfaces take different themes): satisfied — 13
  distinct themes; gate line green.
- **Rule 1** (five headline surfaces, five different themes): satisfied — 地域活性化
  / 住まい / メディア・情報 / 働き方 / 消費・経済 + 旅行・観光, and no 聴解問題5 theme
  touches a 読解 headline; gate line green.
- **Rule 2** (lenient reading): no 読解 headline theme appears on another 読解 surface.
- **Rule 4b** (the cloze's SUBJECT against all thirteen 読解 and all 聴解 subjects of
  20260907_1): no match — 20260907_1 ships no wayfinding, signage or map surface.
- **Rule 4, two papers back**: exactly ONE headline theme shared with 20260904_3
  (消費・経済), inside the budget of one; gate line green.
- **Rule 4, one paper back**: **BREACHED THREE WAYS — see §6.1.**
- **読解 rows and 聴解 rows read as ONE list**: the nearest cross-half pair is 問題12
  (where the light in a room falls) against 聴解問題3-1番 (what tidying a room
  changes) — both indoors, no shared decisive detail, and a shared domain is
  explicitly allowed now that nobody chose the 聴解 item's domain. 問題13
  (what a rewrite deletes from a public notice) against 問題10(5) and 問題14, which
  are notices themselves: they assert nothing about how notices are written.
  No decisive number or condition is shared between 問題14 and any 聴解 item
  (gate line green after the `一週間` repair).
- **Rhetorical MOVE column, read across both halves (cap 2)**: the move
  *the thing everyone reaches for is not the thing that decides it* runs on
  **three** surfaces — 問題11(4) (kit vs a place to stop), 問題12 (bulb brightness vs
  where the light is) and 聴解問題3-2番 (technique vs what you want to express).
  One over the cap. Per the rule the 読解 side is the one re-angled, because
  聴解問題3-2番 is a lifted clip. **Recorded for stage 4, not repaired at stage 3** —
  re-angling 問題11(4) or 問題12 is authoring, and both surfaces are already inside
  the §6.1 repair, so whichever surface that repair moves should be chosen to clear
  this row at the same time. Two further pairs were read and cleared: 問題10(3) and
  問題11(4) share a shape but differ in move (one reports a correlation, the other
  names a second kind of preparation); 問題11(3) and 問題13 both concern what a text
  hands its receiver, but 11(3) draws a distinction between two question types and
  13 makes a claim about what may be cut.
- **Errand identity across three papers** (`shapes` column): no two 聴解 items of
  this paper run the same errand shape, and none matches an entry in either
  previous row. The 問題4 shapes are the closest cluster (eleven single-turn
  responses) and they differ in speech act: 誘い / 確認 / 理由 / 同意の求め / 指摘 /
  報告 / 含み / 依頼 / 情報 / 願い出 / 意外な結果.
- **聴解 theme spread**: 働き方 6 and スポーツ・余暇 5 across the 29 composed
  surfaces, above the authored-pool cap of 5. Recorded because it is measured, not
  because it is actionable — a composed paper draws from the bank and no re-angle
  exists.

## 6. Every FAIL and WARN naming 20260909_1, with its disposition

`make check` final run: **2 FAILs, 2 WARNs** name this test. 128 of the 148 lines
mentioning it are `ok`; the rest are `skip`s that state their own reason
(composed-聴解 exemptions, unkeyed authored draws, no 模範解答.html yet).

### 6.1 FAIL — `no headline theme repeats 20260907_1's (immediately previous, rule 4)`: `['住まい', '働き方', '旅行・観光']`

**BLOCKING, and NOT repairable at stage 3.** 20260907_1's headline set is
食 / 住まい / 働き方 / 旅行・観光 / 行政・手続き / 文化・伝統. This paper's 問題12 is
住まい (20260907_1's 問題12 was also 住まい), its 問題14 is 働き方 (20260907_1's 問題13
was 働き方), and its 聴解問題5-2番 is 旅行・観光 (20260907_1's 問題14 was 旅行・観光).
The id is not grandfathered.

The tags are not negotiable and were not shopped: a city flyer whose four desks are
wages, workplace injury, workplace relationships and changing jobs is 働き方, and an
A/B pair about where to put the lamps in a room is 住まい. `exam-blueprint` rule 4c
forbids re-tagging to make an overlap disappear, and rule 4c's usual release valve
does not reach this one — the valve is the cloze, and the cloze carries neither
repeated theme (it is 地域活性化, free against both previous papers).

**Root cause, two stages back and in two places.**
(a) **Stage 1** drew 住まい and 働き方 among the twelve `reading_topics` themes one
paper after 20260907_1 headlined both, and *nothing at draw time compares the draw
against the previous paper's headline set* — `check_theme_spread()` counts the draw
against `THEME_CAP` only, and rule 4 is enforced post hoc on `logs/topics.json`,
i.e. after both surfaces have already been written.
(b) **Stage 2's 読解 author** then placed those two themes on 問題12 and 問題14, the
two headline surfaces, with nothing in its brief naming which surfaces are
headline-constrained. The author had freedom here — several of the twelve drawn
themes suit an A/B pair or a flyer — so this was avoidable at stage 2 with one line
of guidance.

**Repairs available, for the orchestrator to choose before stage 4:** re-author
問題12 and/or 問題14 onto two of the themes now sitting on non-headline surfaces (a
stage-2 job: an A/B pair and a flyer, plus their four keys and 解説), stamping the
moved surfaces `"origin": "reauthored"` in spec AND ledger per `exam-qa-review`
§"A fix that changes WHAT a surface tests". Choosing 問題12 also clears the
rhetorical-move breach in §5.4.

**The 聴解問題5-2番 third of the breach is not repairable in any case**, and it is a
rule/machinery disagreement the 2026-09-08 composition rework introduced rather than
a defect in this paper: rule 4 counts 聴解問題5 in the headline set on the assumption
that it was authored against a drawn theme, and for a composed paper it never is
(`jlpt-test-generation` §"One topic, one surface": "nothing in the paper can be
re-angled to fix them"). **Proposed change, raised not routed around** (AGENTS.md
§0): either exclude 聴解問題5 from `headline_theme_set()` for a paper whose
`choukai_origin` is `composed` — the same carve-out the slot-theme family and the
register/pacing bands already get — or state in `exam-blueprint` rule 4 that a
composed paper's 聴解問題5 theme is recorded but not counted. I did **not** implement
either: changing a gate to make my own paper green is exactly the move the repo's
own rules forbid.

### 6.2 FAIL — `詳細解説.json explains every keyed item (30 entries for 101 keys)`

**Structural at stage 3; not a defect in the paper.** `make mp3` writes the 30 聴解
entries into both `詳細解説` panes; the 71 言語知識・読解 entries belong to **stage 5**,
which is prohibited before QA passes (AGENTS.md §5, and my brief). The three other
`詳細解説` gate lines already `skip` for the same reason
(`no 模範解答.html — the paper has not reached the model-answer stage`), and the two
that do run are green (`names the official key in tag and prose`,
`inside the terseness bands`; the `.vi` pane likewise). This FAIL closes when stage 5
runs and cannot close before it. I did not run `make model-answer` and authored no
`詳細解説` entry.

### 6.3 WARN — `the 問題8 form-family check compares most of the draw (1/5 = 20% family-tagged)`

**The known live WARN from stage 1. Resolved by hand, not deferred.** It is a
coverage statement about `grammar_form_families` in `pools.json`, not a finding
against this paper: the map is hand-maintained and four of the five drawn 問題8
entries carry no tag, so the collision line below it is silent about them. Read by
hand, the five drawn frames are 目的表現(〜ように…する), 〜でなければ, 補足追加(〜なお…),
同時進行(〜ながら…する) and 義務当然(〜ねばならない) — five different grammar points
with no shared form core and no shared function-word tail, so **there is no
duplicate for the tag to have caught**. The 問題7 ↔ 問題8 cross-pool cooldown line is
green for this paper on merit. The repair is in `pools.json` and belongs to whoever
next grows the family map; the threshold must not be lowered
(qa-report-20260904_1-round2 S6).

### 6.4 WARN — `no 聴解 slot repeats its own theme in the previous 2 papers`: 聴解問題3-4番=文化・伝統

**Deferred to QA, with the reason.** Not actionable and not a repeat of content: the
three clips are different recordings from three different sources
(`shinkanzen:cd2-59` here, `soumatome:cd2-41` in 20260907_1, `2025-12:問題3-4` in
20260904_3), and a composed paper cannot re-angle a lifted item. The tag itself is
not negotiable — a 概要理解 talk about 方言 is 文化・伝統 — and re-tagging to clear the
line is the dodge `exam-blueprint` rule 4c names. One further reason the line is
weak evidence here: **20260907_1's own row records its 聴解 entries as HISTORICAL**
(its listening half was recomposed on 2026-09-08 and its row was never re-derived
from the new draw), so half of what this WARN compares against is a tag for an item
that paper no longer carries. That stale row is itself worth a QA finding against
20260907_1.

### 6.5 One FAIL that named this test in run 1 and is now closed

`35 exam MP3(s) are on the audio release — ['20260909_1'] differ from what was
uploaded`. Closed by `make upload-files TARGET=tests TEST=20260909_1` (44.5 MB to
release `audio`); `logs/upload_manifest.json` is updated and must be committed with
the test.

## 7. `logs/topics.json` row

Appended for `20260909_1`: `surfaces` (43 keys — 14 読解 + 29 聴解), `themes` (43),
`shapes` (29, one per 聴解 surface), `closing_moves` (13 — 問題14 is outside axis 2),
`voices` (14), `persona` (14), `claim` (43), `notes`.
Gate lines confirming the row: `records a claim per surface`,
`records a shapes entry for each of its 29 聴解 surfaces`,
`themes come from the closed THEMES vocabulary`,
`closing_moves come from the closed CLOSING_MOVES vocabulary`,
`every 読解 surface carries a theme`, `no theme on two 読解 surfaces`,
`headline surfaces take five different themes`,
`every logs/topics.json 「…」 span occurs in its own paper (7 spans read)` — all green.

The row carries what the 文法 author asked for: 問題9's theme `地域活性化`, its
invented subject, its closing move `主張`, and the sixteen-option measurement
(one option shared with 20260907_1, `そのうえ`; one with 20260904_3, `たとえば`; both
in the 論理接続 blank 48; blanks 49/50/51 share nothing with either paper). No
repo-wide warning total is pinned anywhere in the row — the invariants are stated
per test.

**Closing-move tally (13 closings, cap 2):** 主張 2 (問題9, 問題13) / 説明 1 (問題10(1))
/ 実用文・分類外 2 (問題10(2), 問題10(5)) / 条件提示 2 (問題10(3), 問題11(4)) /
随筆 2 (問題10(4), 問題11(1)) / 意外な観察 2 (問題11(2), 問題12(A)) /
反論応答 2 (問題11(3), 問題12(B)). Two calls were made by `dokkai.md`'s mechanical
overrides rather than by taste: 問題12(A) is 意外な観察 (the passage states the
mismatch — the room's total light is unchanged — and the closing gives the cause),
and 問題11(1) is 随筆 under the genre carve-out (the rejection targets the narrator's
own prior belief inside a first-person essay that prescribes nothing to the reader).

**Persona tally (cap 2):** 観察者 2 / 職業人 2 / 生活者 2 / 調査者 2 / 実務者 2 /
主催者（依頼） 1 / 親 1 / 福祉センター（通知） 1 / 市（案内） 1.

**Gate-measured 読解 quotas:** first-person passages 6 of 12, です・ます passages 3,
kanji density 27.5 %, novel vocabulary 15.7 % of 306 kanji-words, unglossed novel
7.2 / 1k chars, median sentence 35.0 JP chars, all section lengths inside the
official floor/ceiling — every one green.

## 8. What I did not do, and why

- **No `make model-answer`, no hand-authored `詳細解説`** — stage 5 owns both and
  they are prohibited before QA passes.
- **No `make sample`** — this test's QA is open.
- **No 読解 re-authoring** for the rule-4 breach (§6.1) or the three-way
  rhetorical-move repeat (§5.4). Both need a stage-2 context; stage 3 does not
  author. The four edits I did make are listed in §4 and are all mechanical
  (a form removed, a number moved, two quotes corrected to the shipped bytes).
- **No gate loosened, no theme re-tagged, no grandfather set widened.**
- **No 聴解 re-draw.** The seed was used verbatim as instructed; the single
  same-slot repeat is reported in §5.2.
- Nothing was blocked on a missing `refs/` binary: no archive file was needed.
