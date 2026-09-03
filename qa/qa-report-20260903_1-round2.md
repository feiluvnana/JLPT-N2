# QA report — 20260903_1 (adversarial pass, ROUND 2 — delta audit)

**Reviewed revision** (sha1 over raw bytes):

| file | round 1 reviewed | round 2 reviewed (this pass) | moved? |
|---|---|---|---|
| `tests/20260903_1/言語知識・読解.md` | `cbc0ee7f1fa3` | **`0e20cefe83bc`** | yes |
| `tests/20260903_1/聴解.md` | `86f3bc731ff5` | **`2aa0fb60e2cd`** → `5d39eb6ce59d` after my own mechanical repair (F1) | yes |
| `tests/20260903_1/聴解スクリプト.txt` | `8d5d0e5b7ecb` | **`9aff35a19e01`** — unmoved by me | yes |
| `tests/20260903_1/聴解.mp3` | sha256 `9531179d2368f8ca…` | sha256 **`0953a2cdc407bde9…`**, 32,630,157 bytes | yes |
| `tests/20260903_1/聴解_チャプター.json` | — | `script_sha` = `9aff35a19e01` | in sync |

All four sources moved since round 1, so this is a strictly later revision on every
file. The script sha is the `9aff35a19e01` the hand-off named, and the MP3 is the
32,630,157 bytes it named.

**Timestamp:** 2026-09-03. **Reviewer:** fresh-eyes context; authored nothing in this
paper and repaired nothing in it before this pass.
**Round 1 verdict** (header glanced only after my own solve, as §"Ground rules"
permits): `QA: FAIL (4 findings, 0 automatic)`.
**Entry condition:** `make check` exit 0 — 0 FAIL / 238 WARN / 103 skipped, and **no
WARN line has this test as its subject**.
**Loop position:** round 2 of a maximum of two fresh-eyes rounds.

---

## 1. Verdict

**QA: PASS**

One new finding was raised in this pass (**F1**, the 問題1 構成表 `決め手の位置`
column) and it is **closed inside this pass** by a mechanical repair I applied and
re-gated — see §4 and the loud notice in §7. Zero findings remain open against the
paper. Four skill/gate findings (§5, `S1`–`S4`) are open and, per
§6.5 "Effect on the loop", **block the next generation run**, not this paper.

All five repairs verified correct and **no repair introduced a new defect** — which was
the specific risk this round existed to test, since round 1's own F2 was created by a
repair.

---

## 2. Blind-solve diff

**Solved from:** `qa/20260903_1/keyless.md`, rebuilt at the start of this pass and
carrying source shas `0e20cefe83bc` / `2aa0fb60e2cd` / `9aff35a19e01` — i.e. the
revision under review. I wrote my answers down before opening any keyed file.

Scope solved: the 11 items the five repairs touched, plus 聴解問題5's three keyed
slots (whose `topics.json` record I was asked to re-verify).

| item | my blind answer | key as shipped | result |
|---|---|---|---|
| 問題6-29 | 3 | 3 | match |
| 問題11-57 | 1 | 1 | match |
| 問題11-58 | 2 | 2 | match |
| 問題12-65 | 1 | 1 | match |
| 問題12-66 | 4 | 4 | match |
| 聴解問題1-例 | 3 | 3 (announced 3番) | match |
| 聴解問題1-1番 | 4 | 4 | match |
| 聴解問題1-2番 | 4 | 4 | match |
| 聴解問題1-3番 | 1 | 1 | match |
| 聴解問題1-4番 | 2 | 2 | match |
| 聴解問題1-5番 | 2 | 2 | match |
| 聴解問題5-1番 | 1 | 1 | match |
| 聴解問題5-2番 質問1 | 3 | 3 | match |
| 聴解問題5-2番 質問2 | 2 | 2 | match |

**14 / 14, zero mismatches, zero mis-keys.** Every one also matches
`test_spec.json["answer_positions"]`: 聴解_問題1 `[4,4,1,2,2]` ✓, 聴解_問題5 `[1,3,2]` ✓,
問題12 `[1,4]` ✓, 問題11 slots 1–2 `[1,2]` ✓, 問題6_語彙 slot 4 `3` ✓.

### Blind STRATEGY passes (§0, required in every report)

Measured over the shipped 読解 options, JP-char class only:

| pass | 問題10–13 (18 items) | 問題10–14 (20 items) | official | fail line |
|---|---|---|---|---|
| 1 — most character bigrams shared with own passage | **33.3 %** (6/18) | 30.0 % | 32.8 % | >45 % |
| 2 — second-longest option | **27.8 %** (5/18) | 35.0 % | 24.6 % | >45 % |

Both inside the band and essentially on the official figure. Related rates, all inside
their caps: (tied-)longest-key **27.8 %** (cap 35 %, official 30 %); **uniquely**
longest-key **22.2 %** (cap 30 %, official 20 %); worst per-item option-length ratio
**1.38** at 問題12-66 (WARN >1.65, FAIL >2.50 — read from `dokkai.md`, the owner, per
this skill's 2026-09-03 correction; the withdrawn 1.30 clamp is *not* applied).

Note on the two repaired items: strategy 1 happens to land on the key at both 65 and
66, but on margins of 1 and 2 bigrams out of totals of 3–9 (65: `[9,8,8,3]`; 66:
`[4,5,4,7]`) — 問題12's two short passages give thin overlap counts, so this is noise,
not a signal. The section total is 33.3 %, one half-point above official.

---

## 3. Per-item walkthrough — the items in scope

`OK` rows carry the deciding quote, as §7 requires. **This is a delta walkthrough, not
a 101-item walkthrough** — see the coverage statement in §6 for exactly what I did and
did not re-derive.

### Repair 1 & 2 — 問題12(A) rewording, and 問題66's re-synced 解説

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題12-65 | 1 | `OK` | A「制服のある学校でも、かばんや上着の選び方に生徒の好みは表れる」＋B「制服も自分に合う形をさがして選び取れるものだと思うようになりました」→ 選択肢1。2はAの「流行によってかえって似通ってくる」と反対、3はAが「なくすという話へ進むのは早すぎる」と否定、4はAが「買いそろえる負担は決して軽くない」と否定 | — |
| 問題12-66 | 4 | `OK` | Aは「制服が個性を失わせるとの指摘は当たらない」で反論、Bは「娘の様子を見ていて」「思うようになりました」で経験。1はA/Bが入れ替わり、2はAが反論側、3はAが「見直しが進んでいるのはうなずける」と是認しており批判していない | — |

**Verification of repair 1** (「見直しが進んでいるのも当然だろう」→「〜のはうなずける」):

- **The banned frame is gone paper-wide.** `のも当然だろう` occurs exactly twice in
  `言語知識・読解.md`: line 201 (問題9-51's own option) and line 497 (its 解説). **Zero
  occurrences in the 問題10–14 prose region**, glosses included. The 問題9-51 ×
  問題12(A) 文末-frame collision round 1 filed is fully cleared.
- **The whole keyed-form grep re-run, as §3 now demands after ANY 読解 prose edit.** I
  re-grepped all 21 問題7/8/9 keyed forms (にしてみれば・にかかわりなく・ないではいられ・
  ことか・上は・といっても・にしては・がたい・もので・わけにもいかない・というと・あげく・
  たうえで・につれて・に限らず・とはいえ・をはじめ・割に合わない・そこで・大きく外れない・
  のも当然だろう) over the 10,132-char 問題10→問題14 region: **all zero.** The single
  `ことか` hit is the substring inside option 58-4's 「気づかないことから」 — a different
  form, and in an option, not prose.
- **The assigned closing move is intact.** 問題12(A) still ends
  「制服が個性を失わせるとの指摘は当たらない。服装が自由な学校をいくつか訪ねてみると、
  生徒の服は流行によってかえって似通ってくるからである。」 — 反論応答, template
  「〜との指摘は当たらない。〜からである。」, untouched. The repair landed on the passage's
  4th sentence, not its closing.
- **Claim and register unchanged.** The たしかに／ただし concession frame around the edited
  sentence is preserved (「たしかに、…見直しが進んでいるのはうなずける。ただし、そこから
  制服そのものをなくすという話へ進むのは早すぎる。」). 「うなずける」 is attested editorial
  register and sits at N2. 問題12's measured length is **564** JP chars (band 510–600),
  so the −1-char edit did not move it out of band.
- **Repair 2 verified mechanically, not by eye.** Every quoted string in items 65 and 66
  is an **exact substring** of the passage as it now stands — 3/3 at 65 and **4/4 at
  66, including the re-synced 「見直しが進んでいるのはうなずける」**. I also checked 57/58
  (5/5 and 2/2 exact) since the same file was edited. The only non-matching bracketed
  string in scope is 29's 「同じ行いを長く続ける」, which is an authored definition of the
  target word — 問題6 has no passage, so no source-quote rule applies to it.

### Repair 3 — 問題11(1)'s （注3） gloss

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題11-57 | 1 | `OK` | 「使いはじめた世代は変わったことに気づかず、上の世代は耳につく」「この差が、乱れという一語で語られやすい」→ 1。2は「読者からの手紙をよく読む」と矛盾、3は「三十年ほどかけて静かに進む」と矛盾、4は「どちらが規範にかなうかを決めることではない」と矛盾 | — |
| 問題11-58 | 2 | `OK` | 「新しい使い方が広まる速さは、百年前と大きく変わっていない」＋「二つの形が併存している時期を、そのまま書き残すことだ」→ 2。1・3は筆者が判定を避ける立場と矛盾、4は気づかない側を上の世代と取り違えた反転 | — |

Gloss as shipped: **「変遷：年月がたつうちに、しだいに別の姿になること」**

- **No tested 問題7/8/9 form appears in it.** The previous repair had planted
  問題8-44's keyed 「〜につれて…ていく」 inside this line; `につれて` now occurs **only** at
  line 168 (問題8-44's own option) and line 490 (its 解説) — **zero in prose**. The new
  wording's own grammar (`〜うちに`, `しだいに`) is keyed nowhere in this paper: neither
  appears in any 問題7/8/9 key or distractor.
- **Byte-unique against every （注N） line in every test on disk.** I parsed all
  `（注N）term：definition` lines across every `tests/*/言語知識・読解.md`. The only other
  変遷 gloss on disk is `20260814_1`'s 「時とともに移り変わっていくこと」 — different text.
  The four duplicate (term, definition) pairs the scan found are all *between
  `imported-*` official papers* (一切：全く, 費やす：使う, 本心：本当の気持ち,
  把握する：しっかりと理解する) — no generated paper is involved.
- **It still glosses 変遷 correctly at N2 level.** 「年月がたつうちに、しだいに別の姿になる
  こと」 is an accurate reading of 変遷; every word in the definition is N3-or-below
  (年月/たつ/しだいに/別/姿); it is not circular (it reuses neither 変 nor 遷 nor
  移り変わる); and 変遷 is a formal Sino-Japanese term, so it is legitimately glossable —
  it is not on `dokkai.md`'s banned basic-word list.
- **It leaks no answer to 57 or 58.** 57 keys on the two-generations-coexisting
  sentence, 58 on the unchanged-speed + don't-rush-judgement pair. Neither key nor any
  distractor restates the gloss, and none of 57/58's seven 解説 quotes is drawn from it.
- **Marker/definition pairing is still 1-to-1.** Per-passage, markers and definition
  numbers match exactly, in every 問題10–14 block: 問題11(1) `[1,2,3,4,5]` ↔ `[1..5]`,
  and the same for 11(2)/11(3)/11(4) and 問題13 `[1..8]`. **28 in-body markers, 28
  definition lines** paper-wide (gate floor 25) — zero orphans, zero unpaired markers,
  every headword present in its own passage body. `（中略）` count 4 (non-zero), `<ruby>`
  count 0.

### Repair 4 — 問題6-29's per-option 解説

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題6-29 | 3 | `OK` | 正：「祖父は退職してからも十年間、毎朝の散歩を継続している」＝同じ行いを長く続ける対象。解説の各理由が実際にその選択肢を排除する理由と一致する（下記） | — |

The blanket clause 「いずれも『継』の字に引かれた誤用」 is gone, and each replacement
reason is **the reason that actually excludes that option** — I derived the exclusions
independently before reading the 解説, and they agree three for three:

| option | shipped reason | my independent exclusion | agrees? |
|---|---|---|---|
| 1 この道を…まっすぐ継続すると | 「道を先へ行くのは『進む』で、『道が続く』の『続』に引かれた誤用」 | needs 進む; 継続 cannot denote spatial progression — the pull is 続 via 道が続く | yes |
| 2 兄が家の土地を継続する | 「土地を受け継ぐのは『相続する』で、三つのうちこれだけが『跡を継ぐ』の『継』に引かれた誤用」 | needs 相続する／継ぐ — the pull is 継 | yes |
| 4 カメラとパソコンを継続した | 「機器をつなぐのは『接続する』で、『継続』と『続』を共有する語への取り違え」 | needs 接続する — the pull is 続 | yes |

The 1-and-4-by-続 / 2-by-継 split is correct, and 「三つのうちこれだけが」 correctly
isolates option 2. **Stem, options and key did not move**: key 3 matches
`答案_positions` 問題6_語彙 slot 4, and the option set is the one in the keyless render.

### Repair 5 — 聴解問題1-3番 and 問題1-4番, re-authored (full item review)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 聴解問題1-例 | 3 | `OK` | 「出張の申請、システムに入れるのが今日の五時までなんだ」＋「すぐやります」。announced 「最もよいものは3番です」 and the pre-marked grid cell 「1 2 **(3)** 4」 both equal 3 | — |
| 聴解問題1-1番 | 4 | `OK` | 「届いた分の数が納品書と合ってるか、先に見てくれる」。1=「下げるのは閉店してからでいいよ」(後回し)、2=「そっちは急がないから」(後回し)、3=「はこは田中くんが…運んでくれることになってるんだ」(別の人に割り当て) | — |
| 聴解問題1-2番 | 4 | `OK` | 「一人が続けて使える時間の上限を書き入れといて」。1=「ますが細かいと…今のままでいい」、2=「先に埋めちゃうと、あとから替えられないから、それは無理だね」、3=「分けなくても、名字が入ってればわかるから」 | — |
| **聴解問題1-3番** | 1 | `OK` | 再作項目。「それで、一つお願いなんだけど、業者さんの連絡先だけ、田中さんに聞いといてもらえる」＋女「今日のうちに聞いてみます」。**誤答3件すべて台本の引用可能な一行で死ぬ**：2=「あっちは古いままだから、見なくてかまわないよ」（＋「動画を撮ってくれてるから、それを見といてね」の二行掛かり）、3=「あさっての朝は、いつもの時間で平気だよ。早めに来なくても、間に合うから」、4=「発注に使うパスワードのほうは、田中さんからもうメールで届いてると思う」＋女「はい、届いてます」 | — |
| **聴解問題1-4番** | 2 | `OK`（注記1件） | 再作項目。「ご本人が書いた委任状と、窓口にいらっしゃる方の身分証明書、この二点が必要です」＋「身分証明書は、代わりにいらっしゃるご自分のものをお持ちください」（「自分の」を決めるのは後者）。1=「印鑑は、現在いただかない決まりになっております」、3=「申請書は…書いてお持ちいただくことはできません」、4=「お子さまの健康保険証は、こちらではお使いになれません」 | 注記のみ、修正不要 — §4 N2 |
| 聴解問題1-5番 | 2 | `OK` | 「駅のコインロッカーに入れといて、夜、取ってから来られたらどうでしょう」＋女「それがよさそうですね。そうします」。1=「あしたの朝出される便だと、間に合わないかもしれません」、3=「日にちの変更はお受けできない決まりなんです」、4=「今はお聞きにならなくて平気です」 | — |

**Keys land exactly where `answer_positions` says**: 聴解_問題1 `[4,4,1,2,2]`, and the
問題1 marksheet grid pre-marks the 例 at 3, matching the announced number. **Every
distractor in all six rows dies on a quotable script line** — 18 of 18, with the line
quoted above.

**4番's stimulus has an addressee who can act on it.** The narration is
「男の人が、市役所の電話の自動音声案内を聞いています」: there is a listener, he is the
代わりの方 the guidance addresses, and he is the one going to the counter. This is not
the 火災報知器 defect (a prompt with no defined responder), which in any case is a
即時応答/問題4 rule; the 問題1 non-dialogue requirement is an addressee who can act, and
it is met.

**The 問題1 構成表 read as COLUMNS, verified against the script rather than trusted:**

| column | declared | my measurement from `聴解スクリプト.txt` | quota | verdict |
|---|---|---|---|---|
| 正解 | 6 different actions | 出張申請／納品書照合／上限記入／連絡先を聞く／委任状＋身分証／ロッカー預け — all different | no repeat | ✓ |
| 質問型 | まず2・どう直す1・何をしますか1・物・提出1・その他1 | verified off the six question lines: 例「この後まず何を」/1番「この後まず何を」/2番「どう直しますか」/3番「この後何をしなければ」/4番「あした何を持って行かなければ」/5番「このあとどうしますか」 | ≤3 of 6 on one frame; ≥1 modify/method; ≥1 condition-match | ✓ (まず 2/6) |
| 消去方法 | 既に完了2・別の人に割り当て2・後回し2・不要2・実行不可2・明確に否定2・規則で不可2・条件不足1・順番待ち0 | row-counts reproduce exactly; 18 tokens total reconcile | ≤2 **rows** per token | ✓ |
| 決め手の位置 | 冒頭2／中盤3／終盤1 | **two labels were wrong — see F1.** Corrected to 冒頭2（2番・4番）／中盤3（1番・3番・5番）／終盤1（例）. Bucket tally **unchanged at 2/3/1** | ≤3 of 6 in any one third | ✓ after F1 |
| 提案消去回数 | 例1／1番1／2番1／3番0／4番0／5番0 | I re-ran the gate's own predicate (`CHOUKAI.PROBE_RE` + the ましょうか/ますか suffix list) over the spoken turns: **1/1/1/0/0/0, identical** | ≤2 items with ≥3 | ✓ (0 items ≥3) |
| 決め手の種類 | 時刻・日程／在庫・数量／設備・故障／連絡・情報の不足／規則・制度／場所・経路 | all six verified against the deciding line (例=五時までの期限／1番=納品書との数合わせ／2番=熱がたまるので冷やす必要／3番=店長が連絡先を持っていない／4番=必要書類の決まり／5番=改札外のロッカー) | ≤2 rows per token | ✓ **6/6 distinct** |
| counter-scene cap | サービスカウンター型1（5番） | `COUNTER_RE` hits 1番's 「衣料品の店で」 only; either count is 1 | ≤2 | ✓ |
| assigning-work floor | 4（例・1番・2番・3番） | verified: 部長→部下／店長→アルバイト／先生→学生／店長→アルバイト | ≥3 | ✓ (note §4 N4) |
| establishment-type uniqueness | 会社／衣料品店／大学研究室／電話のアルバイト先／市役所／ホテル | `SETTING_CLASSES` hits 4番=役所 and 5番=宿泊施設, one row each | one per 大問 | ✓ (note §4 N4) |
| non-dialogue presence | 4番 (自動音声案内, single speaker) | confirmed: one speaker, no interlocutor | ≥1 per paper | ✓ |

The `決め手の種類` column — the one the skill flags hardest, because
`20260819_1` put two items on *a diner who cannot eat something* while differing on
every other column — is **six distinct tokens over six rows** here. Clean.

**Non-dialogue medium/slot rotation, the reason 5 was re-authored:** the gate now
carries `check_choukai_nondialogue_medium_rotation`, and this paper reads
`ok 20260903_1: 問題1 non-dialogue medium and slot both rotate off 20260828_2's
(immediately previous)`. Medium moved 留守番電話／音声メッセージ → 自動音声メニュー and
slot moved 3番 → 4番, against `20260828_2` 問題1-3番 (小学校事務室の留守電) and
`20260828_1` 問題1-2番 (待ち合わせ変更の留守電). `choukai-items.md`'s grandfather table
records that `20260903_1` **left `CHOUKAI_NONDIALOGUE_ROTATION_GRANDFATHERED` by being
repaired, which is the only way out** — confirmed: the five WARNs on that check name
`20260810_1`/`20260818_1`/`20260819_1`/`20260827_1`/`20260828_2`, not this test.

### 聴解問題5 — solved for the record audit

| 項目 | 鍵 | 判定 | 決め手 |
|---|---|---|---|
| 聴解問題5-1番 | 1 | `OK` | 男2「その消して回るところだけ、警備の方にお願いできないですかね。…うちの人手は増やさなくて済みます」＋男1「あ、それなら毎日続きますね」＋女「それでいきましょう」。2=「去年やってみたのよね…一週間でやめちゃったの」、3=「今年度は予算が取れなくて」、4=男1「今の人数だと、たぶん二週間で誰もやらなくなります」 |
| 聴解問題5-2番 質問1 | 3 | `OK` | 女「太陽の観察会、二人で行こうよ」＋男「いいね」＝はじめに二人で行こうと考えた会 |
| 聴解問題5-2番 質問2 | 2 | `OK` | 男「じゃあ、星座の解説会にするよ」。4=「三脚、うちにないよね」「ないよ」、1=「今月の分はもう終わってるって」、3=男が女に譲った（「じゃあ、君が行けばいいよ」） |

質問1 and 質問2 print the four candidates in the **same order** (月／星座／太陽／写真),
matching the enumeration order, and **no deciding attribute is printed beside any
option name** — both `jlpt-exam-structure` §問題5-2番 requirements met.

---

## 4. Findings

| id | item / artifact | class | evidence | disposition |
|---|---|---|---|---|
| **F1** | `tests/20260903_1/聴解.md` 問題1 構成表, `決め手の位置` column (was lines 248/253/259) | `要修正` — false record in an audit artifact. **Not** an item defect, **not** a quota breach | Declared 例=「中盤（7行目／全10行）」 and 5番=「終盤（10行目／全18行）」. Measured from the script: 例 has **9** spoken lines with the decider at 7 (7/9 = 0.78 → **終盤**); 5番 has **17** with the decider at 10 (10/17 = 0.59 → **中盤**). Both labels are wrong under every denominator I tried, including the author's own inflated ones (7/10 = 0.70 is still the last third; 10/18 = 0.56 is still the middle). The supporting note also enumerated only **5 of 6** rows, omitting 5番 — and 5番 in fact has *more* post-decider content than most rows (女's acceptance, the かぎ deferral, the 日にち rule) | **CLOSED in this pass.** I applied the mechanical correction (§7) and re-gated. The two errors cancelled, so the bucket tally was **2/3/1 before and after** and the ≤3-per-third quota was never actually breached — which is why this is not disqualifying |

**No other finding.** In particular, none of the five repairs introduced a defect:

- repair 1 removed the frame without touching the closing move, the claim, the register
  or the length band, and items 65/66 still key correctly;
- repair 2's re-synced quotes are exact, 4/4;
- repair 3 removed the planted 〜につれて frame and did not plant a new one — its own
  grammar is keyed nowhere, it is byte-unique on disk, it glosses correctly, it leaks
  nothing, and pairing stayed 1-to-1;
- repair 4's three per-option reasons are each the true exclusion, and the item did not
  move;
- repair 5's two re-authored items solve cleanly, key to spec, ground all 18
  distractors on quotable lines, give 4番 an addressee who can act, and hold every
  問題1 構成表 quota as a column.

### Notes for the next paper — not findings, no repair asked

| id | observation | why it is not a finding |
|---|---|---|
| N1 | 聴解問題1-4番's question adds 「あした」 (「男の人は、**あした**何を持って行かなければなりませんか」) but the automated guidance never mentions a date, so the framing is ungrounded | Harmless to solvability: all four options and all four deciding lines are date-independent, so no option is created or killed by it. There is no 聴解 rule against ungrounded question framing (the "scenario detail the source never describes" automatic fail is scoped to 問題14). A tighter stem would be 「窓口に何を持って行かなければなりませんか」 |
| N2 | 問題1 has two rows on the same 主導 pair, 店長→アルバイト (1番 and 3番), both after 3番 was re-authored into a shop-manager phone call | No rule caps 主導 repetition inside a 大問, and the establishment rule is about 場面: 1番 is 衣料品店の売り場, 3番's shop is never named. Errands (入れ替え作業 vs 引き継ぎ連絡), media (対面 vs 電話) and decider axes (在庫・数量 vs 連絡・情報の不足) all differ, so the two items are not the same errand. Folded into `S3` |
| N3 | 20260828_2 — the immediately previous paper — set 聴解問題5-2番 at a 市役所, and this paper's re-authored 4番 is also 市役所 | Different errand (オンライン申請の操作案内相談 vs 住民票の写しの代理請求), different 大問, different slot, different theme (デジタル化 vs 行政・手続き), and 4番 is not a headline surface. The establishment-uniqueness rule is intra-大問. `行政・手続き` appears exactly **once** in the whole paper |
| N4 | 問題1's closings rhyme mildly: 2番/3番/5番 all end on the subordinate-or-customer accepting (「なるほど、わかりました」/「はい、じゃあいつもの時間に行きます」/「わかりました。じゃあ、そのままにしておきます」) | Not identical, so the gate's >4-char identical-closer rule is not engaged; openings are well varied (4 distinct types over 6 items) and the 構成表 documents a per-row 決め手 cue. Worth deliberate variation next paper |
| N5 | 説明-vs-意外な観察 is a coin-flip on 問題10(3) | Under one labelling 説明 would reach 3 and breach the ≤2 cap; under the other the paper is 7 shapes × ≤2. Resolved in this paper's favour on evidence — see §6 and `S4` |

---

## 5. Root cause

Per §6.5, each finding gets exactly one code, with the recurrence test applied by
reading the papers on disk, and a concrete proposed edit. `F1` yields `S1`; `S2`–`S4`
are classes this pass surfaced independently of any paper finding.

| id | from | code | tests showing the class | owning file | concrete proposed edit |
|---|---|---|---|---|---|
| **S1** | F1 | `RULE-UNENFORCEABLE` | The rule text has never stated the formula, so every paper carrying the column is exposed; `20260903_1` is the first where the label was actually re-derived | `question-authoring/references/choukai-items.md` §"Read it as columns" | The line reads 「**決め手の位置** — 冒頭 / 中盤 / 終盤 (no more than 3 of 6 rows in any one third)」 and never says a third *of what*. Append the formula: 「位置は *決め手の発話の行番号 ÷ その項目の総発話行数* を三等分して決める（≤1/3=冒頭、≤2/3=中盤、それ以外=終盤）。非対話項目は発話行の代わりに文を数える。構成表には *n行目／全m行* を必ず併記し、m は台本の発話行だけを数える（質問行・場面説明行は含めない）」. Without a stated denominator the author counted the closing question line in two rows and not in the other four, which is how both labels went wrong |
| **S2** | F1 (gate half) | `GATE-BLIND` | same as S1 | `tools/check_consistency.py` `check_choukai_decider_position` | The check reads the **declared** label out of the 構成表 and tallies buckets — it never opens the script, so a mislabelled row passes and a correct tally can sit on top of two wrong labels (exactly this paper). With S1's formula stated, this becomes string-decidable: parse the 「n行目／全m行」 the column already prints, recompute the bucket from `n/m`, and FAIL when the recomputed bucket differs from the printed label. That predicate, run against its founding case, flags 例 (7/9 → 終盤, labelled 中盤) and 5番 (10/17 → 中盤, labelled 終盤) and also catches the two wrong `m` values, since 9≠10 and 17≠18 are checkable against the script |
| **S3** | N2 | `RULE-MISSING` | 2 of the papers on disk put two 問題1 rows on one 主導 pair (this paper: 例/1番/2番/3番 include 店長→アルバイト twice; `20260828_1` runs 駅の窓口/病院受付/家電量販店 as three staff-to-customer rows) — **two or more papers = systemic by definition** | `question-authoring/references/choukai-items.md` §場面 | The `場面` rule caps the establishment type and the `assigning-work` quota is a floor only, so nothing caps the **主導 pair**. Add: 「**主導** — 同じ主導の組（部長→部下・店長→アルバイト・先生→学生・係員→客…）は1大問に2行まで。仕事を割り当てる型の下限（≥3）を満たすために同じ組を繰り返してはならない——場面・用件・決め手の軸が違っても、受験者は同じ力関係の指示を二度聞かされる」. This is string-decidable off the 主導 column, so mirror it as a ≤2-rows-per-pair tally in `check_consistency.py` beside the existing 消去方法 tally |
| **S4** | N5 | `RULE-UNENFORCEABLE` | `20260813_1` split two independent QA passes on 主張-vs-条件提示 before that call was made mechanical; the same gap is now live one shape over | `question-authoring/references/dokkai.md` §"Thirteen surfaces" | The file made 主張-vs-条件提示 mechanical ("if a closing explicitly REJECTS a stated single-factor view … classify it as 主張") but left 説明-vs-意外な観察 to taste, and 問題10(3) 「使う額が熱心さと合わないのは、…手立てになっているからだ」 sits on the line: under 説明 the paper has three 説明 and breaches the ≤2 cap; under 意外な観察 it has 7 shapes × ≤2 and complies. Add the same kind of override: 「前件が予想と食い違う事実（意外・ずれ・合わない・にもかかわらず）を提示し、後件がその**原因**を述べる形は、字面に「意外にも」が無くても **意外な観察**。**説明** は予想との食い違いを提示しない機構・区別の記述に限る」. Under that rule 問題10(1) and 問題10(3) are both 意外な観察 and 問題9/問題11(2) are both 説明 — the reading this pass adopted |

**A note on the `shipped_surface` disagreement, filed here rather than as a paper
finding.** This skill's own §"Ground rules" tells the author to add **three** fields —
`shipped_theme`, `shipped_surface`, `note` — and asserts that
`check_theme_record_agreement()` "reads exactly this". It does not: the check's
docstring and predicate require `shipped_theme` + `note` only, and the sole paper on
disk carrying `shipped_surface` is `20260821_1`, the paper the rule was written from.
`20260903_1`'s 市役所 entry carries `shipped_theme` + `note` and passes. Per AGENTS.md
("when two statements disagree the owner wins, and the disagreement is a defect to
fix") this is a doc-vs-gate drift, not a defect in this paper — and since **this file
is the one file the reviewer may edit directly**, I flag it for the next pass over it
rather than silently conforming: either drop `shipped_surface` from the three-field
list, or add it to the check. The same sentence also requires the note to quote the
deciding line; this paper's note describes rather than quotes, and nothing reads that
requirement either.

---

## 6. Rulings on the corrected records

I audited these rather than trusting them, as instructed — round 1's own F3 was this
exact class (聴解問題5-2番's two speakers recorded inverted while the keys and `notes`
were correct).

| record | ruling | evidence |
|---|---|---|
| `logs/topics.json` 聴解問題1-3番 `claim` | **TRUE as re-derived.** The 在庫表 claim is gone | Now 「紙のマニュアルは見なくてよくパスワードはもう届いていて早出も要らないので、業者の連絡先を田中さんに聞く」 — all three distractor deaths named, and 紙のマニュアル is the script's own word (「紙のマニュアルのほうは、どうしましょう」/「あっちは古いままだから、見なくてかまわないよ」) |
| `logs/topics.json` 聴解問題1-4番 `claim` | **TRUE as re-derived.** The 委任状の代筆 claim is gone | Now 「印鑑も申請書の持参も息子の保険証も認められないので、委任状と自分の身分証を持って行く」. The distractor really is 息子が書いた申請書, and it really dies on 「申請書は…書いてお持ちいただくことはできません」 |
| `logs/topics.json` 聴解問題5-2番 `surfaces` + `claim` (round 1's F3) | **TRUE — the inversion is genuinely fixed**, verified against the script and not against the narrative of the defect | Record: 「女は太陽の観察会・男は星座の解説会」 / 「太陽の観察会は女が、席を譲った男は別の条件で星座の解説会を選ぶ」. Script: 女「私が太陽の観察会に申し込むね」, 男「じゃあ、星座の解説会にするよ」, and 男「じゃあ、君が行けばいいよ」 is the man giving up the seat. Actors now the right way round |
| `logs/topics.json` 聴解問題5-1番 `surfaces` + `claim` + `shapes` | **TRUE** | Correctly identifies the reviver as a **third** speaker (男2 proposes moving the doer to the night security round) and 男1 as the denier who then switches — matches 男1「あ、それなら毎日続きますね」 |
| `logs/topics.json` `shapes` (newly written, 33 entries) | **COMPLETE and structurally sound**; contents spot-verified where I had solved the item | 33 entries, exactly one per 聴解 surface, keys align 1-to-1 with `surfaces` (zero missing, zero extra), no two entries are the same string, section split 問題1:6 / 問題2:7 / 問題3:6 / 問題4:12 / 問題5:2 = 33. I verified the 問題1 (6) and 問題5 (2) entries against the script line by line; the 問題2/3/4 entries (25) I did **not** re-derive — stated as a skip in §8. `ok test 20260903_1: logs/topics.json records a shapes entry for each of its 33 聴解 surfaces` |
| `test_spec.json` ↔ `logs/ledger.json` byte-identity | **TRUE** — the two `items` blocks are byte-identical under canonical JSON | Compared field for field; zero diffs across all 11 categories |
| The corrected 市役所 clause in both files | **TRUE** | Now 「a single-speaker automated phone guidance, the paper's 問題1 non-dialogue item」 — the stale "counter transaction" wording is gone, and it correctly leaves `scenario`/`theme` at the drawn values (`recency_map` keys on the string) while recording `shipped_theme: 行政・手続き` + `note`. See §5 on the missing third field |

### Paper-wide invariants re-derived in this pass

**Closing-move / final-sentence column — all 13 axis-2 closings, re-read, not trusted.**
`dokkai.md`'s denominator table makes this 13 rows (問題9 + 問題10×5 + 問題11×4 +
問題12(A) + 問題12(B) + 問題13; 問題14 outside the taxonomy):

| # | surface | final sentence (abbrev.) | shape |
|---|---|---|---|
| 1 | 問題9 | 「…価格に織り込まれていくことによる。」 | 説明 |
| 2 | 問題10(1) | 「意外にも…原因は…にある。」 | 意外な観察 |
| 3 | 問題10(2) | 「ご不便をおかけしますが、ご理解をお願いいたします。」 | 実用文・分類外 |
| 4 | 問題10(3) | 「使う額が熱心さと合わないのは…手立てになっているからだ。」 | 意外な観察 (S4) |
| 5 | 問題10(4) | 「…教えていただけますでしょうか。」 | 実用文・分類外 |
| 6 | 問題10(5) | 「受け取っているのは…安心なのかもしれません。」 | 随筆 |
| 7 | 問題11(1) | 「…という批判もあるが、実際には…変わっていない。」 | 反論応答 |
| 8 | 問題11(2) | 「ちがいは…という点にあります。」 | 説明 |
| 9 | 問題11(3) | 「…だけでは足りない…こそが要る。」 | 主張 |
| 10 | 問題11(4) | 「…期間を置いた自治体では…割合が低くなっています。」 | 条件提示 |
| 11 | **問題12(A)** | **「制服が個性を失わせるとの指摘は当たらない。…からである。」** | **反論応答 — assigned move INTACT** |
| 12 | 問題12(B) | 「けれども娘の様子を見ていて…思うようになりました。」 | 随筆 (genre carve-out) |
| 13 | 問題13 | 「水をどこに預けるかを、住民といっしょに決められるかどうかが問われている。」 | 主張 |

**7 shapes over 13 closings: 説明 2, 意外な観察 2, 実用文・分類外 2, 随筆 2, 反論応答 2,
主張 2, 条件提示 1 — none over the ≤2 cap.** This reproduces round 1's independent
count ("13 finals over 7 shapes, none over the cap"), and the repair changed nothing in
the column: it landed on 問題12(A)'s 4th sentence. The two 反論応答 rows also differ at
the **sentence-template** level (「批判もあるが、実際には」 vs
「指摘は当たらない。…からである」), as do the two 主張, the two 随筆 and the two 説明, so no
named `FINAL_SENTENCE_TEMPLATES` skeleton appears more than twice. Marker-family total
is 3 — below the 5–9 official range, which `dokkai.md` states (2026-09-03, RC-D) is
**not** a defect, since only the upper side is enforced and variety is proved by the
per-shape cap.

**読解 measured bands**, by the gate's own documented method (JP-char class, passage
region, `（注N）` definition lines kept — the method must be named beside the number):

| 大問 | measured | floor | ceiling |
|---|---|---|---|
| 問題10 | 1315 | 1100 | 1330 |
| 問題11 | 2518 | 2250 | 2700 |
| **問題12** | **564** | 510 | 600 |
| 問題13 | 920 | 800 | 1070 |
| 問題14 | 571 | 450 | 640 |

All five inside the window; 問題12 stayed in band across the repair. *(A methodological
caution worth recording: counting only indented paragraph lines gives 問題13 = 713,
which looks like a floor breach. It is not — the gloss definition lines are part of
`passage_prose` by design. Quote the method with the number.)*

**聴解 register / voice / length**, from `make choukai-profile`: 196 turns, 7,214
spoken chars, reactions 18.4 %, openers 28.6 %, fillers 54.1/10k, 縮約形 79.0/10k, 問題1
まず-rate **20 %** (the lowest on disk alongside `20260821_1`, against official 36.8 % —
the 「この後まず何を」 monoculture is genuinely broken here), 問題3 median talk length
**263** (official median 268, range 158–397, target 220–300). Gate-side: narration
gender matches `SPEAKER_MAP`, same-gender pitch separation holds, item speaker pairs
cast distinguishable voices, 問題4 register 4 casual / 2 keigo, voice balance worst
section 問題5 at 54 %.

**Audio chain — all four artifacts agree, and the MP3 needed no rebuild.**

- `聴解_チャプター.json` carries `script_sha` = `9aff35a19e01` = the current script sha,
  so the chapters were cut from the shipped script, not a superseded one; duration
  2,719.11 s; 問題1 chapters present for all six items (例 31.69 / 1番 113.44 / 2番
  184.09 / 3番 279.76 / 4番 368.02 / 5番 457.16) — the re-authored 3番 (88 s) and 4番
  (89 s) have real audio.
- MP3 on disk: **32,630,157 bytes**, sha256 `0953a2cdc407bde9…`. `logs/upload_manifest.json`
  records `audio/20260903_1.mp3` at **size 32630157, sha256 `0953a2cdc407bde9…`** — the
  uploaded asset is these exact bytes. Gate: `ok 28 exam MP3(s) are on the audio
  release`, `ok 聴解.mp3 was built from today's 聴解スクリプト.txt (script_sha
  9aff35a19e01)`, `ok …built with today's pacing (pacing_sha 4d623645a38d)`.
- My repair touched `聴解.md` only. **Script sha unmoved at `9aff35a19e01`**, so no
  re-synthesis and no re-upload.

**Topic table (delta rows only) — this paper against the two before it:**

| surface | 20260828_1 | 20260828_2 | 20260903_1 | verdict |
|---|---|---|---|---|
| 聴解問題1-3番 | 留守番電話 (待ち合わせ変更) | 小学校の留守電 (出欠) | **アルバイト先の店長からの引き継ぎの電話** | medium and errand both fresh |
| 聴解問題1-4番 | マンション管理事務室 (チラシ原稿) | 工場見学の集合場所 | **市役所の電話の自動音声案内** (住民票の代理請求) | fresh; establishment recurs from 28_2's 問題5-2番 but errand/theme/大問/slot all differ (N3) |
| 問題1 non-dialogue medium | 留守番電話 @2番 | 留守番電話 @3番 | **自動音声メニュー @4番** | medium **and** slot both rotated |
| headline theme set | — | メディア・情報／人間関係／地域活性化／子育て・家族／デジタル化 | 消費・経済／防災／医療・福祉／環境／科学・技術 | **zero intersection** (rule 4 allows ≤1 two papers back, 0 immediately previous) |

読解 theme axis: 14 surfaces / **13 theme rows, all distinct** (問題12(A) and (B) are one
theme row on 教育, per `dokkai.md`'s denominator table). `行政・手続き` occurs once in the
paper. Per-slot 聴解 theme rotation clean over the previous two papers.

### `make check` WARN resolution

Final gate state after my repair: **exit 0, 0 FAIL, 238 WARN, 103 skipped** — byte-for-byte
the state I entered on, so the repair moved no gate line.

- **Zero WARN lines have `20260903_1` as their subject.** Every check naming this test
  reads `ok`. This is the strongest form of the §"Entry condition" requirement and it
  needs no per-line justification.
- **The five `問題1 non-dialogue medium and slot` WARNs** name `20260810_1`,
  `20260818_1`, `20260819_1`, `20260827_1`, `20260828_2` as subjects; `20260903_1`
  appears in them only as the citation `qa-report-20260903_1 RC-C`, i.e. as the source
  of the rule. Resolution: these are the grandfathered pre-rule papers. **Not this
  paper's WARNs**; this paper's own line is `ok`.
- **The three `shapes` WARNs** name `20260827_2`, `20260828_1`, `20260828_2` — the rows
  still missing the field, named in `TOPICS_SHAPES_DRIFT_GRANDFATHERED`. These are the
  three new WARNs the hand-off predicted. `20260903_1`'s row is filled and reads `ok`.
  Resolution: correct as designed — a hole in three older records, and per §6.5 they
  are `PIPELINE-GAP` work items that should be filled before the next paper, since the
  errand-archetype rule has no other data to read.
- **The `pools_sha` WARN** lists 14 older ids whose recorded sha no longer matches
  `pools.json`. `20260903_1` is **not** among them — its recorded `pools_sha` is
  `37704aadda35`, the current value. It appears only in the trailing "stamped on a
  REROLL" note, which the check's own text calls "a record, not a defect". Resolution:
  false positive with respect to this paper.
- **Two skips belong to this test's `詳細解説.json`**, which Stage 5 has deliberately
  not created yet. Correct: `模範解答.html` must not be built until this paper passes.
  It may now be built.

---

## 7. LOUD NOTICE — the one repair I applied

I edited **`tests/20260903_1/聴解.md` and nothing else**, confined to the 問題1 構成表's
`決め手の位置` column (F1). Three replacements:

1. 例 row: `中盤（7行目／全10行）` → **`終盤（7行目／全9行）`**
2. 5番 row: `終盤（10行目／全18行）` → **`中盤（10行目／全17行）`**
3. the `**決め手の位置**` paragraph: buckets restated as
   `冒頭2（2番・4番）／中盤3（1番・3番・5番）／終盤1（例）`; the formula I measured with
   written down inline (per-row `n/m`); and the post-decider-content enumeration
   extended from 5 rows to all **6**, adding 5番's own follow-up content.

**I did NOT touch `聴解スクリプト.txt`** — its sha is unmoved at `9aff35a19e01`, so **the
MP3 does not need rebuilding and does not need re-uploading**. I rebuilt the two
derived HTML artifacts so nothing predates its source (`make booklet 20260903_1`,
`make sheet 20260903_1`; 聴解.md 18:38:11 → 聴解.html / 解答.html 18:38:21) and re-ran
`make check`: identical 0 FAIL / 238 WARN / 103 skipped, with
`ok 20260903_1: 問題1 決め手の位置 spread (6 rows)` still green on the corrected labels
(tally 2/3/1 either way).

**Caveat on my own edit, stated rather than hidden:** the two *line counts* are pure
arithmetic with one right answer. The two *labels* follow from those counts only under
the positional-thirds reading of 「一つのバケツに3行まで」, and the owner has never written
the formula down — which is precisely finding `S1`. If the owner adopts a different
denominator, my labels should be re-derived under it. What is not in doubt either way:
the declared values were wrong, and the quota was never breached.

---

## 8. Coverage and skips (AGENTS.md §0.7)

**Read in full before any other tool call:** `AGENTS.md`, `.agents/exam-qa-review/SKILL.md`.
**Read as routed, in the sections the deltas touched:**
`question-authoring/references/dokkai.md` §"Thirteen surfaces, thirteen different
essays" (denominators, six shapes, template table, genre carve-out);
`question-authoring/references/choukai-items.md` §"Read it as columns", §場面,
§grandfather table; `tools/check_consistency.py` (`DOKKAI_FLOOR`/`CEILING`,
`passage_prose`, `check_dokkai_lengths`, `check_dokkai_rhetorical_monotony`,
`check_choukai_decider_position`, `check_choukai_probe_carousel`,
`check_theme_record_agreement`, `check_topics_shapes_field`).

**Ran, on all items in scope:** step 0 blind solve from `qa/20260903_1/keyless.md`
(14 items) + both blind-strategy passes over all 20 読解 items; step 1 key-by-key proof
(14); step 2 / 2b distractor elimination (14 items = 44 wrong options, each with the
line that kills it); step 3 mechanical reads on the touched artifacts (`（注N）`
pairing and gloss uniqueness paper-wide, 読解 length bands paper-wide, option-length
and longest-key rates paper-wide, keyed-form grep paper-wide, 解説-quote substring check
across 162 bracketed strings in 聴解.md and the 5 in-scope 解説 rows in
言語知識・読解.md); step 4 聴解 structure — the full 問題1 構成表 read as **columns**
against the script, plus 問題5's printing rules; step 5 the closing-move column (all 13)
and the delta rows of the cross-test topic table incl. the headline-theme set
intersection; step 6 provenance (spec↔ledger byte-identity, `answer_positions`
compliance for every in-scope key, the corrected 市役所 clause); step 6.5 root cause.

**Deliberately NOT re-derived — this was a scoped delta audit, by instruction**
("you are not re-deriving that whole pass, you are auditing the deltas and their blast
radius"):

1. **The 87 items outside the delta were not re-solved.** Round 1 blind-solved 101/101
   with zero mis-keys against sources that have since changed only in the five places
   audited here. I re-solved 14 items and verified paper-wide that no other item's text
   moved in a way that could touch a key (the keyed-form grep, the gloss pairing scan,
   the length bands and the option-length/longest-key rates are all paper-wide, and all
   are inside band).
2. **`logs/topics.json`'s 25 `shapes` entries for 問題2/3/4 were not re-derived** — only
   the 8 for 問題1 and 問題5, which is what I was asked to verify. Their structural
   completeness (33/33, 1-to-1, no duplicates) *was* checked.
3. **No archive measurement was blocked** — `make choukai-profile`, `make check`'s
   archive checks and the `refs/` `*.md` extracts all ran; nothing was substituted from
   memory, and no `refs/` binary was needed.
4. **`make model-answer` was not run** and `詳細解説.json` / `詳細解説.vi.json` do not
   exist. Correct for this point in the pipeline: Stage 5 runs only after this pass, and
   it is now unblocked.
5. **`make qa-eval` / `make lint-draft` / `make repair-plan` were not run.** The gate is
   0 FAIL with no WARN naming this test, and the blind solve was done by hand from the
   keyless render as §0 requires; these tools would have added no evidence this report
   lacks.

**Source stillness.** mtimes were checked at the start (all sources quiet since 18:14)
and again before writing. The only movement is my own repair to `聴解.md`, disclosed in
§7; `言語知識・読解.md` (`0e20cefe83bc`) and `聴解スクリプト.txt` (`9aff35a19e01`) are
byte-for-byte what I solved from.

---

## 9. Verdict, restated

**QA: PASS**

The paper ships. All five repairs are correct and none introduced a defect. All four
corrected records are true of the shipped paper, including the two `claim` fields and
the 聴解問題5-2番 actor ordering that round 1 filed as F3. The one new finding (F1) was
a false record in the 問題1 構成表 whose enforced quota was never actually breached; I
closed it mechanically in-pass, disclosed the edit, and re-gated to the identical
result. No script byte changed, so **no MP3 rebuild and no re-upload are required.**

Open work that does **not** block this paper but **does** block the next generation run
(§6.5): `S1` and `S2` (the 決め手の位置 formula and the gate that should recompute it),
`S3` (no cap on 主導 repetition), `S4` (説明-vs-意外な観察 left to taste), the
`shipped_surface` doc-vs-gate drift in this skill, and the three `shapes` rows still
empty on `20260827_2`/`20260828_1`/`20260828_2`.

`make model-answer 20260903_1` is now unblocked.
