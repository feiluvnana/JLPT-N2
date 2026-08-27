# QA Report (ROUND 2) — tests/20260821_1

Reviewer: fresh-eyes round-2 context. Authored nothing on this paper, applied none of
the round-1 repairs, did not write the round-1 report. Round 1's report is treated as a
set of CLAIMS to verify by measurement.

Reviewed revision (measured at round-2 start):

| file | sha1 | mtime |
|---|---|---|
| `言語知識・読解.md` | `fb8f95b2206708a7ef53a081f2946ec67f0c6140` | 2026-08-24 11:05:02 |
| `聴解.md` | `e7b940868a04fce01c455358865188ff962d16e4` | 2026-08-24 11:36:30 |
| `聴解スクリプト.txt` | `1390752d08e9509c9f6273a3c6fdd2690507ffe8` | 2026-08-24 11:04:30 |
| `test_spec.json` | `9077f3d37eb7c29e3adf70b1873500708b587c55` | 2026-08-24 11:16:49 |

All three round-1 shas moved, as expected for a repaired paper
(`言語知識・読解.md` 56e97f61→fb8f95b2, `聴解.md` a5b3cca9→e7b94086,
`聴解スクリプト.txt` 7c141246→1390752d).

Report started 2026-08-24. Sections appended as each step finishes (this machine
sleeps mid-turn; the file is the durable record).

## Entry condition — `make check`, re-run by me (not taken on trust)

`make check` → **exit 0, "All checks passed (31 skipped), 451 warning(s)"**. Verified.
The only WARN line naming `20260821_1` is the aggregate `pools_sha` record
(`20260821_1` appears only in its informational "stamped on a REROLL" tail; its
recorded sha equals the live `cea9612d1e0b`). One `skip`: `詳細解説.json` absent —
expected, the model-answer step is the LAST pipeline step (AGENTS.md §5). The
round-1 polite-voice WARN is **gone**: the line now reads
`ok 20260821_1: 読解 polite voice (です・ます) passages >= 3 (got 3)`.

Artifact ordering by mtime: `聴解スクリプト.txt` 11:04:30 → `聴解.mp3` +
`聴解_チャプター.json` 11:08:54 → `test_spec.json` 11:16:49 → `聴解.md` 11:36:30 →
all HTML 11:36:41–42. No artifact predates its source; `聴解.mp3`'s `script_sha`
line confirms `1390752d08e9`, the live script. `言語知識・読解.md` 11:05 < its HTML
11:36. OK.

**Source stillness:** shas re-measured at the end of the review; see the closing
section.

---

## Step 0 — blind solve of every touched 大問, from `qa/20260821_1/keyless.md`

`make keyless 20260821_1` rebuilt against the current revision (render header:
`言語知識・読解.md = fb8f95b22067`, `聴解.md = e7b940868a04`,
`聴解スクリプト.txt = 1390752d08e9` — identical to my header). Solved from that
file only, before opening any key column.

Scope, per the skill's re-review rule ("Changed items AND their whole 問題 go back
through steps 1–4"): the repairs touched 問題6 (all 20 option sentences), 問題10(1)
prose, 問題10(2)/11(3)/11(4)/13 closings, 聴解問題2's opening turns (3番/4番/6番)
and 1番's decisive line, and 聴解問題3-4番's whole talk. Whole-大問 scope therefore =
問題6, 問題10, 問題11, 問題13, 聴解問題2, 聴解問題3 = 32 items. I also re-solved 問題12 and
問題14 (4 items) as untouched controls inside the same 読解 half, giving **36 scored items**:

```
問題6   26-30 : 1 3 1 2 4
問題10  52-56 : 4 2 2 1 4
問題11  57-64 : 1 4 4 4 2 3 1 2
問題13  67-69 : 3 4 2
聴解問題2 1-6番 : 3 3 2 4 1 4
聴解問題3 1-5番 : 1 3 2 4 1
```

Plus 問題12 65=3, 66=3 and 問題14 70=4, 71=3.

Diffed against the shipped 正解 columns afterwards: **36/36 agreement, zero
mismatches.** No mis-key introduced by the repairs. (Agreement is evidence about
keys, not about uniqueness — the two-answer hunt is below.)

---

## Step 1 — verification of each of the ten round-1 dispositions, BY MEASUREMENT

| id | round-1 claim | what I measured | verdict |
|---|---|---|---|
| **F1** | `dokkai_profile._parse_generated_dokkai` 問題10 branch repaired (marker walk) | 問題10 per-passage prose now measures **266 / 251 / 250 / 261 / 267** JP chars (was 284/0/0/0/0), section total **1295** (floor 1100, ceiling 1330). `make check` line `ok 20260821_1: 読解 sections reach the official length floor` and `every 問題10 passage reaches {10: 150, 11: 400}` both pass on the repaired path | **CONFIRMED** |
| **F1b** | `check_dokkai_register()` strips `（注N）` before the polite match | `make check` now prints `ok 20260821_1: 読解 polite voice (です・ます) passages >= 3 (got 3)`. The round-1 WARN is gone; no paper text was rewritten to get it | **CONFIRMED** |
| **F2** | three 問題2 opening turns moved off 「〜たいんですけど」 | `grep -c` over the whole `聴解スクリプト.txt`: 「〜たいんですけど/〜たいんですが」 = **2 occurrences total**, one mid-dialogue (問題1-5番 「パソコンを置きたいんですけど」) and exactly **one item-opener** (問題2-2番). 3番 now opens on a fault report, 4番 on a settled-decision statement, 6番 on the clerk calling the applicant in. `ok … no more than 2 聴解問題1/2 items open on one frame (0 frame(s) over the cap)` | **CONFIRMED** |
| **F3** | reframe family 6 → 2 surfaces | Read all **13** closings by hand against `dokkai.md`'s six shapes (column below). Not-A-but-B closings = **問題9** (「教えたのではなく、見る力を与えたのだと思う」 + 「…こそが…のである」) and **問題11(2)** (「だけでは…こそが要る」) = **2**, exactly the cap. 問題10(2)/11(3)/11(4)/13 are genuinely off the family — 10(2) 「…時点で、林の荒れは始まっていた」, 11(3) 「つまり、…によって分かれていくのです」, 11(4) 「数字は、…だと思っている」, 13 「意外にも、…持ち越しを残さない、それだけの工夫である」. **Not cosmetic.** But see NF-1: the gate's own "2 matched" is composed differently from mine | **CONFIRMED (content); gate arithmetic wrong — NF-1** |
| **F3b** | twelve/thirteen-surface final-sentence column has no skeleton more than twice | Dumped all 13 finals through the gate's own `passage_final_sentence()`. Gate templates: 「だけでは/こそが」 ×2 (問題9, 11(2)), 「わけではない」 ×1 (問題10(3), an email instruction), others 0. **No template over 2.** But the column read finds a pair the gate cannot see — 問題11(1) and 問題12(A) share BOTH the 条件提示 shape label AND an evidential-correlation skeleton (see NF-2) | **PARTLY — NF-2** |
| **F4** | 聴解問題3-4番 re-angled off 問題13's claim | `grep -c` on the shipped script for the five old strings (「楽しかったかどうか」「続けるかどうかを決めないで」「きらいになったのではなく」「来る時間が作れなくなった」「半年後に来なくなる」) = **0 each**. The whole rewritten talk contains **0** occurrences of 続け / やめ / 楽し / 意志 / 習慣 / きらい. The new talk asserts only that the trial hour is also an inspection hour and names three checkable things (混み具合 / 係の者のいる場所 / 帰りの道). It makes **no claim at all** about why anyone continues, and rejects no affective explanation. **The argument did not survive the rewording — it was removed.** | **CONFIRMED** |
| **F5** | `origin: "reauthored"` + `note` on the drawn 聴解問題3-1番 entry in spec and ledger | Both files carry the entry `{"scenario": "ラジオ:睡眠の話", "theme": "睡眠・健康", "origin": "reauthored", "note": …}` with a note naming the medium change and its reason, field-for-field identical between `test_spec.json` and `logs/ledger.json`. `ok test 20260821_1: ledger history entry records the same draw as tests/20260821_1/test_spec.json`. **The fixer correctly REFUSED round-1's proposed rename** to 「健康づくりの講座:睡眠の話」 — that string is in no pool, and renaming would leave 「ラジオ:睡眠の話」 un-cooled and break `check_spec_pool_resolution`. `exam-blueprint`'s own gate message says "do NOT rename the `scenario` string", so round-1's repair text was wrong and the applied fix is right | **CONFIRMED (and round-1's repair text corrected)** |
| **F6** | 問題2 決め手の種類 relabel + 1番's decisive line re-angled | Read the shipped column: 例 時刻・日程 / 1番 費用・金額 / 2番 規則・制度 / 3番 連絡・情報の不足 / 4番 人手・担当 / 5番 時刻・日程 / 6番 規則・制度 → **時刻・日程2, 規則・制度2, 費用・金額1, 連絡・情報の不足1, 人手・担当1** over 7 rows, every token ≤2. The tally line under the table states the same numbers. 1番's new line 「座席の分のお金だけは、二十日前より早くご連絡いただいても、そのままいただきます。」 is in the shipped script | **CONFIRMED (but NF-3: the 解説 was not re-quoted from it)** |
| **F7** | 問題10(1)'s 〜たところ frame recast | 「教わったところ」 = **0** in `言語知識・読解.md`; the passage now reads 「去年の暮れ、思いきって電話で分量を教わると、伯母は少し笑って…」. The only 「たところ」 left anywhere in the 問題10–14 region is inside item 42's own 解説 cell (metalanguage about the key), not in passage prose. `ok … no 問題7/8/9 keyed form appears more than 1× in the 問題10-14 prose`. Item 52's key and both its 解説 quotes are untouched | **CONFIRMED** |
| **F8** | 問題6 option-length distribution rebuilt | Re-measured all 20 option sentences myself: **mean 26.3, median 26.5, range 18–34, n=20** (round 1: mean 21.1, median 21, range 18–25). Official current era: mean 26.0, median 25, range 18–39. Gate agrees: `ok 20260821_1: 問題6 option-sentence distribution (mean 26.3, median 26.5, range 18–34, 3 over 30)`. Key is uniquely longest in **1 of 5** items (20%); "pick the longest" scores 1/5 = chance | **CONFIRMED** |
| **F9** | spec↔topics theme desync — "rule rewritten" | The rule in `exam-qa-review/SKILL.md` was indeed rewritten (it now reclassifies this shape as 要修正 bookkeeping, not 自動不合格, and names this paper as the precedent) — **but its own closing sentence still reads "Sync both files, and record in each the reason the pool tag did not describe the authored item", and that was NOT done.** Measured: `test_spec.json` and `logs/ledger.json` still carry `市役所:手続き案内 → 地域活性化` and `コールセンター:本人確認 → 働き方`; `logs/topics.json` carries 聴解問題2-6番 → 行政・手続き and 聴解問題2-3番 → デジタル化; `pools.json` still carries the original two tags. Neither file has a `note`. The disagreement round 1 filed is unchanged on disk | **NOT CONFIRMED — reopened as NF-4** |

---

## Step 1b — proof that nothing OUTSIDE the six repaired areas moved

Round 1's walkthrough carries a deciding quote in almost every row. I extracted every
`「…」` string of ≥8 chars from its 109 walkthrough rows (109 rows, dropping quotes that
contain an ellipsis or a slash, which are elided and cannot be matched) and searched all
three current sources for each, after normalising whitespace and `（注N）`.

**Result: only 6 of the extracted quotes no longer appear**, and every one is accounted
for:

| round-1 row | vanished quote | why |
|---|---|---|
| 問題6-29 | 「祖母の体調は、少しずつ回復した」 | F8 lengthened the sentence to 「入院していた祖母の体調は、この一週間で少しずつ回復した」 |
| 問題11-64 | 「時間の数字そのものを否定したいわけではない。数字は、折り合いをつけたあとで最後に出てくるものだと思っている」 | F3 rewrote 問題11(4)'s closing |
| 問題13-69 | 「走らない日を作らない備え」 | F3 rewrote 問題13's closing paragraph |
| 聴解問題3-4番 | 「今日見ていただきたいのは、動きの中身ではありません」 | F4 rewrote the talk |
| 問題3-13 | 「〜ずくめ(黒ずくめ)」 | a `pools.json` string, never a paper string — matcher false positive |
| 聴解問題3-1番 | 「〜の話は出てこない」 | a rule template quoted from `exam-qa-review`, not from the paper — matcher false positive |

So every line round 1 verified outside 問題6 / 問題10(1) / the four rewritten closings /
聴解問題2's openings / 聴解問題2-1番's decisive line / 聴解問題3-4番 is still on disk
byte-for-byte. That, plus round 1's 101/101 blind solve, is what licenses scoping this
round's walkthrough to the six touched 大問 (the skill's own re-review scope: "Changed
items AND their whole 問題 go back through steps 1–4").

---

## Step 2/2b walkthrough — the six touched 大問 (32 items) + 問題12/問題14 as controls (4) + 2 例

### 問題6 (26–30) — all twenty option sentences rewritten by F8

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題6-26 膨大 | 1 | OK | 「五十年分の新聞記事という**膨大な**量の記録」 — 量 is 膨大's own collocate; official runs 「膨大なデータ」「膨大な情報」「膨大な事実」 in 3 of the 5 archive sittings. Wrong: 2 機械→巨大, 3 人気→絶大, 4 景色→壮大. Three different real adjectives compete for the same 「膨大」 slot; none is a second attested reading | — |
| 問題6-27 もうける | 3 | OK | 「古い切手を売って、少し**もうけた**」 = 儲ける. Wrong: 1 体力を→つけた, 2 信用を→得た, 4 客を→つかんだ. 「〜をもうける」 with an abstract object is what no learner produces; none of the three is a second attested collocation (儲ける takes a profit, not a possession) | — |
| 問題6-28 模索 | 1 | OK | 「自分らしい歌い方を**模索している**」 — a method being groped for. Wrong: 2 鍵を→探している (the literal-groping trap, and the best distractor in the paper), 3 自信を→取り戻そうと, 4 予定を→検討している | — |
| 問題6-29 回復する | 2 | OK | 「入院していた祖母の体調は、この一週間で少しずつ**回復した**」. Wrong: 1 部品を→交換, 3 財布が→戻ってきた, 4 暑さが→厳しくなった. 回復 needs a state that returns to a former level; none of the three supplies one | — |
| 問題6-30 促進 | 4 | OK | 「体の血の流れを**促進する**」. Wrong: 1 時間を→短縮, 2 友人を→催促 (the near-relative trap: 促す/催促 share the 促 kanji), 3 興味を→ひく/そそる | — |

Level band, all five keys checked against the archive and the two textbook extract sets
(no vendored corpus exists): 膨大 attested in **5 of 5** archive sittings, 回復 **5 of 5**,
儲 **1**, 模索 **1** (glossed in official 7/2025), 促進 0 in the 5-sitting archive but a
standard N2 サ変 (Shin Kanzen 語彙 第2部 covers only part of the book, so absence there is
not evidence). None is N1-hard, none is an N3–N5 headline item, and no option set is four
basic words. Distribution after F8: **mean 26.3, median 26.5, range 18–34**; option 1 is
the longest in 4 of 5 items but is the key in only 1, so "pick the longest" scores 20 %.

### 問題10 (52–56) — (1)'s prose and (2)'s closing rewritten

| 項目 | 鍵 | 判定 | 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 4 | OK | 「あの料理は、台所の事情ごと出ていたのです。」＋「井戸の水と、雪の下に置いて甘くなった里芋。書き取れるのは分量ばかりで、そのどちらも持って帰ることはできません。」 → 「料理の味は、それが作られる場の条件と結びついて生まれていた」. Wrong: 1 inverts the passage (he CANNOT get the water), 2 is not claimed, 3 is invented. The F7 recast (「思いきって電話で分量を教わると」) sits before the deciding lines and touches neither | — |
| 問題10-53 | 2 | OK | 「手入れは何も生まない費用になり、誰かが引き受けるほかなくなった」 → 「利用にともなって済んでいた作業が、収入を生まない負担に変わったから」. Wrong: 1 states the surface cause the passage explicitly displaces, 3 reverses 落ち葉 (people stopped, not increased), 4 is not in the text. F3's new closing 「利用が絶えて手入れだけが残った時点で、林の荒れは始まっていた。」 is a 説明 restatement and adds no new claim the options could key on | — |
| 問題10-54 | 2 | OK | 「この一日が加わることを、お客様に必ずお伝えください。」 Wrong: 1 (工場 receipt) contradicts 「まず車体の状態だけを見る日を設けます」, 3 is never asked of the branches, 4 contradicts 「電池や配線ではなく」 | — |
| 問題10-55 | 1 | OK | 「案が書き直されるのは、たった一件の具体的なご指摘があったときです。見落としを教えていただく場だとお考えください。」 Wrong: 2 is denied (「数の多い側に決めるのであれば、投票と変わらない」), 3 inverts 「全文と…市の考え方を、あわせて公表します」, 4 inverts the same line | — |
| 問題10-56 | 4 | OK | 「なぜそうするのかを言葉で説明でき、人に渡せる仕事が増えます」＋「職場を移る前に、今の職場の中で先に現れている」 Wrong: 1 is the view the passage displaces, 2 inverts it, 3 adds an evaluation the author never makes | — |

### 問題11 (57–64) — (3) and (4) closings rewritten

| 項目 | 鍵 | 判定 | 決め手 | どう直すか |
|---|---|---|---|---|
| 問題11-57 | 1 | OK | 「それは、書き込みが集まってくる経路によって変わる」 → 「いつどんな経路で集まったかに左右される」. Wrong: 2 asserts product quality improves, 3 invents deletion, 4 asserts the identity the passage denies | — |
| 問題11-58 | 4 | OK | 「数を扱う人はこういうとき母集団を疑い、平均を出すもとになった書き手が…どのように選ばれたのかを考える」＋「読む側にできるのは、その平均がどこから集まったのかを確かめることである」 Wrong: 1/3 are over-readings the passage never licenses, 2 inverts 「数字が下がることと、数字が当てになることは、まったく別のこと」 | — |
| 問題11-59 | 4 | OK | 「里親の側から見れば、頼まれたときにことわらずに受けられる条件が、先にととのったということである」 Wrong: 1/3 are not in the passage, 2 inverts 「国はこの割合を引き上げることをめざし…力を入れてきた」 | — |
| 問題11-60 | 4 | OK | 「支援員を置き…一時預かり…面会の日取りまで職員が調整する。この三つがそろった地域でだけ、委託は目に見えて動いていた」＋「受け入れを支える人と仕組みこそが要る」 Wrong: 1 is the very thing shown not to work, 2/3 are inventions | — |
| 問題11-61 | 2 | OK | 「一つは仕事の置き方で…」「もう一つは居場所の数で…」 Wrong: 1/3/4 all name factors the passage explicitly excludes (「呼び込んだ人数や補助の金額では、この差を説明することができません」) | — |
| 問題11-62 | 3 | OK | 「町が用意した仕事に就いた人は、その仕事が区切りをむかえたときに、次の行き先を失ってしまいます」 Wrong: 2 is the OTHER group's property (町の外から仕事を持ち込んだ人) — a reassignment distractor, not a fabrication; 1/4 are inventions. F3's new closing 「つまり、残る人が多いか少ないかは、来たあとに仕事と居場所がどう置かれるかによって分かれていくのです」 restates 61's answer and does not touch 62 | — |
| 問題11-63 | 1 | OK | 「時計で切られた家では、遊びが見えない場所へ移っていく…親のほうは、何がどれくらい行われているのかを言えなくなってしまう」 Wrong: 2 asserts the opposite of 「逆のことが起きた」, 3/4 are inventions | — |
| 問題11-64 | 2 | OK | F3's new closing: 「際限がなくなるという心配に、私はこう答えている。…数字は、家族との折り合いがついたあとで最後に出てくるものだと思っている。」 → 「やめ方の相談を重ねた末に、数字が決まってくるのが順序である」. Wrong: 1 inverts the order, 3 asserts what the third paragraph denies, 4 endorses the 一日一時間 rule the first paragraph rejects. **The rewrite kept the key's grounding intact — 「最後に出てくる」 is still the deciding phrase** | — |

### 問題12 (65–66) and 問題14 (70–71) — untouched, re-solved as controls

| 項目 | 鍵 | 判定 | 決め手 |
|---|---|---|---|
| 問題12-65 | 3 | OK | A 「間があいても、だれも困っていなかった」／B 「聞き手の側から見れば言葉を選んでいる時間であり」 → 「話の途中に置かれた間は、会話を妨げるものとはかぎらない」 |
| 問題12-66 | 3 | OK | A 「言い終わったあとに二つ数えてから口を開くようにしている」／B 「沈黙が働くのは、次に話す人がその前の言葉を引き取ったときである」 |
| 問題14-70 | 4 | OK | インフルエンザ 65歳以上 = 1,500円 ＋ 「市民税が非課税の世帯の方は…無料」 does not apply (two constraints, as the rule requires) |
| 問題14-71 | 3 | OK | 「市外の医院…事前に市へ届け出」＋「受ける日の二週間前までに健康課へ届け出てください」；抗体検査未受検なので対象内 (two constraints) |

### 問題13 (67–69) — closing paragraph rewritten by F3

| 項目 | 鍵 | 判定 | 決め手 | どう直すか |
|---|---|---|---|---|
| 問題13-67 | 3 | OK | 「距離を落とした日でも、靴をはいて外に出れば手がかりの並びはひととおり通るが、休んだ日はその並びが一度も通らない」＋「間があくと目減りしていく」 Wrong: 1 is exactly the case the passage says is FINE, 2/4 are not in the text | — |
| 問題13-68 | 4 | OK | same pair of lines, read from the other side → 「走り出すきっかけの並びを毎日通していたので、続ける形が残った」 Wrong: 1/3 are inventions, 2 asserts the willpower account the passage rejects | — |
| 問題13-69 | 2 | OK | 「続く形を作るのは、忙しい週に何をどこまでけずるかを、あらかじめ決めておく手当てである」 → option 2 「続く形を作るのは、忙しい週の減らし方を先に決めておくことだ」. **The F3 rewrite left this sentence in place and changed only the two sentences after it** (「意外にも、七年の日誌で…」), so 69's grounding is intact. Wrong: 1 is the thing 「始める日にはたいへん役に立つ」 but not what makes it last, 3 contradicts 67/68, 4 is what the 「ちゃんと」 paragraph warns against | — |

### 聴解問題2 (例 + 1–6番) — three openings and 1番's decisive line rewritten

| 項目 | 鍵 | 判定 | 決め手 | どう直すか |
|---|---|---|---|---|
| 聴解問題2-例 | 2 | OK | 「一時間ほどかかります」＋「木曜は、会社を出るのが六時なんですよ」＋「木曜の枠は七時までですので」 | — |
| 聴解問題2-1番 | 3 | OK (鍵) / **要修正 (解説)** | Key grounded twice: 「座席は、お申し込みをいただいた時点で、私どもがもう買っております」＋「取り消しになりますと、その分は初めからいただくことになります」. Option 1 「どの分もお金はかからない」 is denied by **F6's new line** 「座席の分のお金だけは、二十日前より早くご連絡いただいても、そのままいただきます。」 — but the 解説 eliminates option 1 with 「ただ、そこが分かれるところなんですけど、飛行機の座席だけは、少し違いまして。」, which only ANNOUNCES an exception and does not deny "every portion". 2 denied verbatim (「前の日から、ではないんです」), 4 denied (「こちらの都合で中止にした場合は、いただきません」 + 男「それは安心しました」) | **NF-3**: replace option 1's 解説 quote with F6's own new line, which is the line that eliminates it |
| 聴解問題2-2番 | 3 | OK | 「屋号を入れる場合は、お店を始めたときに出した紙の写しが必要になります」＋「あ、あれ、家に置いてきちゃった」. 1 denied (「はい、免許はあります」), 2 denied (「まだ一時間ございます」), 4 denied (「手数料は、いただいておりません」). The one 「〜たいんですけど」 opener left in the paper | — |
| 聴解問題2-3番 | 2 | OK | New opener 「ネットで登録した住所を直そうとしたら、途中で止まってしまって、さっきから三回もやり直してるんです」; decider 「その番号、去年やめちゃったんです。今の電話は別の番号で」＋「お電話では、送る先を変えることができない決まりになっておりまして」. 1 denied, 3 denied (「お名前はぴったり合っております」), 4 denied (「もともとお受けしておりません」) | — |
| 聴解問題2-4番 | 4 | OK | New opener 「会社の集まりの幹事をしていて、二十人ほどで貸し切りをお願いすることになりました」 (a settled decision, not a 〜たい request); decider 「それより、教えてくれる人がついてほしいんです」. 1 denied (「お値段は、土曜も日曜も変わりません」), 2 waved off by the speaker herself, 3 denied (「はい、同じ場所です」) | — |
| 聴解問題2-5番 | 1 | OK | 「七時から、電気の線を通りにわたす作業が入るんです」＋「線の上にマットをかぶせますので、そのあとは車が通れなくなります」. 2/3/4 each raised and denied | — |
| 聴解問題2-6番 | 4 | OK | New opener (clerk calls her in): 「お待たせしました。市民センターのお部屋のお申し込みですね」; decider 「市内にお住まいの方が、会員の半分以上いることを見せていただく必要がありまして」＋「お名前とお住まいを書いたものを、次にお持ちください」. 1 denied (後払い), 2 denied (既に提出), 3 denied (市役所側にある) | — |

Column reads for 問題2 (step 4): opening moves = 予約の読み上げ／仮定の質問／用件の申し出／不具合の報告／決定事項の伝達／去年と同じかの確認／職員の呼び入れ — **seven different moves, no pair**. Opening speaker alternates 女/男/女/男/女/女/男性職員. 決め手の種類 tallies 時刻・日程2 / 規則・制度2 / 費用・金額1 / 連絡・情報の不足1 / 人手・担当1 — no token over 2. 質問型 内容・発言2 / どうして2 / 気持ち1 / 何を一番大事に1. All six 正解 different. Voice turns 52 % / 48 % over 97 turns. Closing turns: gate reports 0 rhymes, 0 leaks, and I read all seven — no two share a shape.

### 聴解問題3 (例 + 1–5番) — 4番's talk fully rewritten

| 項目 | 鍵 | 判定 | 決め手 | どう直すか |
|---|---|---|---|---|
| 聴解問題3-例 | 3 | OK | 「そろえて並べるのはやめて、その日にとれたものを、そのまま出しています」 | — |
| 聴解問題3-1番 | 1 | OK | 「体の中の時計を合わせているのは、寝た時刻ではなく、起きた時刻の方なんです」＋「まっさきに整えていただきたいのは、起きる時刻です」. 2 touched only as a negative example, 3/4 never raised (correct for 問題3) | — |
| 聴解問題3-2番 | 3 | OK | 「まずやるのは、起きたことを日にちの順に並べ直す作業です」＋「一回目は、答えを出す場ではなく、地図を作る場だと思ってください」 | — |
| 聴解問題3-3番 | 2 | OK | 「終わる日の一か月前から、新しくするお手続きができます」＋「二階の窓口に、今の利用証と、お住まいがわかるものをお持ちください」 | — |
| 聴解問題3-4番 | 4 | OK | Rewritten talk: 「体験の時間は、動く時間だけでなく、中を見ていただく時間でもあります」＋「見ていただきたいところを三つ挙げます」＋「今日、自分の目で確かめて帰ってください」 → 「体験のときに見ておくとよいところ」. The three items (混み具合／係の者のいる場所／帰りの道) are all inspectable on the day. Distractors 年齢／会費の払い方／道具の選び方 are each absent from the talk, as 問題3 requires. **Zero occurrences of 続け/やめ/楽し/意志/習慣/きらい in the whole block** | — |
| 聴解問題3-5番 | 1 | OK | 「五年前、町の人たちが集まって話し合い、決まりを変えました」＋「今は、半年の練習に通えば、だれでも打てます」. 4 is the near-miss (打ち手 increased, not 客) and is grounded-then-reassigned | — |

問題3 column reads: talk lengths 275/293/291/291/**284**/272 — all inside the 220–300 band.
Speaker voices via `SPEAKER_MAP`: 男(M)/女(F)/男(M)/係員(F)/男(M)/レポーター(F) = **3 male, 3 female**.
種別: 人物の主張4 (quota ≥3), institutional 2 (quota ≤2), `BROADCAST_RE` 3 (floor 3).
No monologue names or denies its own distractors (gate confirms both).

---

## Step 5 — whole-paper and cross-test table, rebuilt (F3 and F4 both moved surfaces)

**Closing-move column, read from the SHIPPED last two sentences of all 13 surfaces**
(the artifact `dokkai.md` demands; labels are mine, derived from the text, not copied
from `logs/topics.json`):

| surface | final sentence (as the gate's own `passage_final_sentence()` extracts it) | shape |
|---|---|---|
| 問題9 | 趣味は結果が出なければ意味がないという批判もあるが、実際には、（51）ことこそが、私を毎週あの岸壁へ向かわせているのである。 | 反論応答 (+ not-A-but-B in the previous sentence) |
| 問題10(1) | あの料理は、台所の事情ごと出ていたのです。 | 随筆 |
| 問題10(2) | 利用が絶えて手入れだけが残った時点で、林の荒れは始まっていた。 | 説明 |
| 問題10(3) | 改造が遅くなるわけではないと申し添えてください。 | 実用文（メール・分類外） |
| 問題10(4) | 見落としを教えていただく場だとお考えください。 | 実用文（お知らせ・分類外） |
| 問題10(5) | 学び直しの効き目は、職場を移る前に、今の職場の中で先に現れているのです。 | 意外な観察 |
| 問題11(1) | 実際、書き込みの数集めに力を入れた店では、星の平均が高くなる一方で、買い直しの割合との開きが大きくなっていた。 | 条件提示 |
| 問題11(2) | 受け入れを支える人と仕組みこそが要る。 | 主張 |
| 問題11(3) | つまり、残る人が多いか少ないかは、来たあとに仕事と居場所がどう置かれるかによって分かれていくのです。 | 説明 |
| 問題11(4) | 数字は、家族との折り合いがついたあとで最後に出てくるものだと思っている。 | 反論応答 |
| 問題12(A) | 手元にある四十回ほどの記録を数えてみると、言い終わりのあとに間を置いた会ほど、終わりまでに一度でも発言した人の数が多い。 | 条件提示 |
| 問題12(B) | 沈黙が働くのは、次に話す人がその前の言葉を引き取ったときである。 | 条件提示 |
| 問題13 | 持ち越しを残さない、それだけの工夫である。 | 意外な観察 |

Shape tally over the 11 taxonomy surfaces: 反論応答 2, 説明 2, 意外な観察 2, 条件提示 3
(問題11(1) + 問題12 A and B), 主張 1, 随筆 1. **Not-A-but-B family = 2 (問題9, 問題11(2))**,
down from round 1's 6. That is F3's substance and it holds. The 条件提示 3 and the
問題11(1)/問題12(A) skeleton rhyme are **NF-2**.

**Headline-theme set, built by me from the shipped content and diffed:**

| slot | 20260821_1 | 20260819_1 | 20260818_1 |
|---|---|---|---|
| 問題9 | スポーツ・余暇 | 防災 | デジタル化 |
| 問題12 | 人間関係 | 働き方 | 交通 |
| 問題13 | 科学・技術 | 文化・伝統 | 住まい |
| 問題14 | 医療・福祉 | 旅行・観光 | 行政・手続き |
| 聴解問題5-1番 | 消費・経済 | 食 | 地域活性化 |
| 聴解問題5-2番 | 住まい | 教育 | メディア・情報 |

Intersection with the immediately-previous paper: **∅** (rule 4's zero-tolerance clause
holds). Intersection with the paper-before-last: **{住まい}** — exactly one, which rule 4
permits. 読解: 14 rows, **13 distinct themes** (人間関係 twice = 問題12 A and B, one
surface). 聴解 over the 21 drawn 問題1/2/3/5 rows: スポーツ・余暇 3, 消費・経済 2,
文化・伝統 2, 行政・手続き 2, everything else 1 — all inside the ≤5 cap.

**Subject collisions across all 34 surfaces:** F4's pair is gone (聴解問題3-4番 no longer
argues anything about habit persistence). No 問題14 decisive number is shared with a
聴解 item (gate confirms). No two 聴解 items run one errand. Two adjacencies recorded as
observations, not findings, below.

---

## Step 6 — provenance and spec audit

1. **Answer positions.** All 101 keys re-extracted from the two Markdown sources and
   compared field-for-field with `test_spec.json["answer_positions"]`. Every touched
   section matches exactly: 問題6 `[1,3,1,2,4]`, 問題10 `[4,2,2,1,4]`,
   問題11 `[1,4,4,4,2,3,1,2]`, 問題13 `[3,4,2]`, 聴解_問題2 `[3,3,2,4,1,4]`,
   聴解_問題3 `[1,3,2,4,1]`. **The repairs moved no key.**
2. **Draw provenance.** `ok test 20260821_1: ledger history entry records the same draw
   as tests/20260821_1/test_spec.json`; `ok … every recorded draw resolves to a
   pools.json entry (22 items)`. The one `origin: "reauthored"` entry
   (「ラジオ:睡眠の話」) carries a `note`, is identical in both files, and correctly keeps
   the pool string un-renamed so the cooldown still bites.
3. **The theme records do NOT agree** — `test_spec.json`/`logs/ledger.json` vs
   `logs/topics.json` on two 聴解問題2 surfaces, with no `note` in either file. **NF-4.**
4. **Copyright non-reproduction.** The rewritten prose was checked against the archive
   and the imported papers by the gate's byte-identity checks (`（注N）` definitions,
   `例。` blocks, 聴解 例 option lines — all `ok`). The F8 sentences are ordinary invented
   examples; the F4 talk's three inspection points are invented, unsourced, and carry no
   decimal or cited figure.

---

## Findings (round 2)

| id | item / artifact | class | severity | evidence | disposition |
|---|---|---|---|---|---|
| **NF-1** | `tools/check_consistency.py` `REFRAME_CLOSING`, the 「というより」 alternative added by the round-1 root-cause pass | `GATE-WRONG` | **blocks next run**; paper unaffected | The check prints `2 matched` for `20260821_1`, and I dumped which two: **問題13** and **問題11(2)**. 問題13's match is `というより` at 「二キロが五百メートルになり、走る**というより**外に出て戻ってくるだけの日もあった」 — a mid-passage manner hedge in paragraph 2, **not a closing move at all**. Meanwhile the paper's genuine second reframe closing, 問題9's 「釣れない時間は、私に待つことを教えた**のではなく**、見る力を与えたのだと思う」, matches nothing (bare 「のではなく」 is excluded at passage scope, and 「こそが、私を毎週あの岸壁へ向かわせているのである」 falls outside the `こそが?.{0,15}(だ｜…)` window). So the count is **right by arithmetic and wrong by identity**. This is precisely the cry-wolf failure the same comment block cites as the reason 「わけではない」 was routed to `FINAL_SENTENCE_TEMPLATES` instead — and 「というより」 was put in BOTH places, so the sentence-scope copy already does the honest work | Open — reviewer may not edit generation tooling mid-review. Edit in the root-cause table |
| **NF-2** | 問題11(1) and 問題12(A) closings; and `dokkai.md`'s own surface count | `RULE-UNENFORCEABLE` + `GATE-BLIND` | 要修正 (minor) | Both close on the 条件提示 shape AND on one skeleton — *evidential frame + [V-た + 集団] + では/ほど + 数量の増減*: 「**実際**、書き込みの数集めに力を入れた**店では**、星の平均が高くなる一方で、買い直しの割合との**開きが大きくなっていた**」 vs 「**手元にある四十回ほどの記録を数えてみると**、言い終わりのあとに間を置いた**会ほど**、終わりまでに一度でも発言した**人の数が多い**」. `dokkai.md`: "the two sharing a shape must **also** differ at the SENTENCE-TEMPLATE level, not swap content words into the same skeleton" — the named `20260817_2` class. `FINAL_SENTENCE_TEMPLATES` has no correlation entry, so the gate cannot see it. Compounding it, `dokkai.md` is **internally inconsistent about the denominator**: its own enumeration reserves the six shapes for "the twelve essay-type surfaces (問9, 問10×5, 問11×4, **問12**, 問13), each capped at exactly 2" (問題12 = one surface → 条件提示 = 2, compliant), while its column procedure and `check_dokkai_final_sentence_templates` read **thirteen** finals with A and B separate (→ 条件提示 = 3, over the cap). A paper cannot satisfy both readings. **Neither of these two closings was touched by F3** — the F3 repair moved the four reframe surfaces and did not run the full column read the same section mandates | Open — repair below |
| **NF-3** | `tests/20260821_1/聴解.md` 問題2 解説, 1番, option 1's elimination quote | self-reconciliation gap (`exam-qa-review` step 1: "Copy the deciding line into the 解説 cell if absent") | 要修正 (minor) | F6 rewrote 1番's confirming turn **to** 「座席の分のお金だけは、二十日前より早くご連絡いただいても、そのままいただきます。」 precisely so the item's 決め手 would be a charge — and that is the only line that denies option 1 「出発の二十日前までなら、**どの分も**お金はかからない」. The 解説 still eliminates option 1 with 「ただ、そこが分かれるところなんですけど、飛行機の座席だけは、少し違いまして。」, which announces an exception without stating it. The 構成表's 鍵の言い換え cell **does** quote the new line, so the two artifacts disagree about which line decides the item. (The item itself is sound: option 1 IS impossible, and the gate's quote-trace check is green because the weaker quote is genuinely in the script) | Open — repair below |
| **NF-4** | `test_spec.json` + `logs/ledger.json` ↔ `logs/topics.json`, 聴解問題2-3番 / 2-6番 | bookkeeping desync (`exam-qa-review` ground rules, as REWRITTEN by the round-1 pass) | 要修正 (minor) | Round 1's F9 was dispositioned as "rule rewritten". The rule **was** rewritten — it now reclassifies this shape as 要修正 rather than 自動不合格 and names this paper as its precedent — but its own final sentence still reads "**Sync both files, and record in each the reason the pool tag did not describe the authored item**", and that was not done. Measured on disk: spec and ledger both still say `市役所:手続き案内 → 地域活性化` and `コールセンター:本人確認 → 働き方`; `topics.json` says 問題2-6番 → 行政・手続き and 問題2-3番 → デジタル化; `pools.json` still carries the two original tags; **no `note` in any of the three**. Nothing about the disagreement round 1 filed has changed on disk | Open — repair below |
| **NF-5** | two records invalidated by the repair pass itself | stale hand-off note (`exam-qa-review`: "`notes` is verifiable, and must be verified… a note naming an artifact the fix removed is worse than no note") | 要修正 (minor) | **(a)** `tests/20260821_1/聴解.md`, 問題3 構成表, 「Stage-3 の修正 F4」 ends: 「`logs/topics.json` の該当スロット（15行目）の `surfaces`／`themes`／`shapes`／`notes` の4欄は、この書き直しに合わせて更新が必要だが、本紙の担当範囲外のファイルなので**未実施**。」 — **false**: `logs/topics.json` entry 15 has been updated (its `surfaces` and `shapes` cells describe the rewritten talk in detail, `notes` carries a full F4 paragraph, and `themes` is deliberately left at スポーツ・余暇 with the reason stated). Two tracked records now disagree about whether the same repair was applied. **(b)** `logs/topics.json` entry 15's `notes` still opens 「`make check` exit 0 — **446 WARN against a 445 baseline**, and the ONLY lines naming this test… one WARN, `読解 polite voice (です・ます) passages >= 3 (got 2)`」 and devotes a labelled paragraph 「THE ONE WARN, AND WHY IT IS A FALSE POSITIVE」 to it. That WARN no longer exists — F1/F1b's repairs made the gate print `got 3` — and the live total is **451**, not 446. The next paper's blueprint stage reads this field | Open — repair below |

**Automatic fails: 0.** No second defensible answer among the 36 re-solved items; every key
restates a line still in its source; no 解説 quote is absent from its source (gate green on
both files); no unanswerable item or 例; no broken Japanese; no narration/voice conflict
(問題3 runs 3 male / 3 female by `SPEAKER_MAP`); no off-level key (問題6's five checked
against the archive and both textbook extract sets); no ungrounded 聴解 distractor (each
問題2 wrong option is raised and denied; 問題3's are correctly never mentioned); no verbatim
reuse; `answer_positions` complete and matched 101/101; no stale artifact.

### Repairs (the work list)

| id | repair, appliable without re-deriving it |
|---|---|
| NF-1 | In `tools/check_consistency.py`, **remove the `｜というより` alternative from `REFRAME_CLOSING`** — it is already in `FINAL_SENTENCE_TEMPLATES`, where sentence scope makes it honest, and at passage scope it is the same cry-wolf shape the block's own comment gives as the reason 「わけではない」 was routed there. Then, to keep the reframe family measurable at the closing, add a **final-TWO-sentence** scope to `FINAL_SENTENCE_TEMPLATES` (or a sibling check) so bare 「のではなく」 in the penultimate sentence is counted: 問題9's 「教えたのではなく、見る力を与えたのだと思う」 is a genuine reframe closing that neither check currently sees. Re-run over all 15 papers and print which ids move before committing (§6.5's founding-case rule) |
| NF-2 | Two edits. (1) **Rewrite one of 問題11(1) / 問題12(A) off the correlation skeleton.** The cheaper is 問題11(1), whose key (58) leans on 「読む側にできるのは、その平均がどこから集まったのかを確かめることである」 — the sentence *before* the final one — so the final sentence can be recast without touching a key, e.g. 説明: 「見返りをつけた店の星の平均は、買い直しの割合とは別の何かを測っている。」 **問題11 sits 24 chars under its 2700 ceiling, so the replacement must be no longer than the sentence it replaces.** (2) **Resolve `dokkai.md`'s denominator**: state in one place whether 問題12 is one surface or two for the shape cap, and make `check_dokkai_final_sentence_templates`'s 13-final scope agree with it. Recommend "two finals, one theme" — read A and B separately for shape/template, count them as one for the theme rule — and add a `条件提示` correlation template (`(では｜ほど)[^。]{0,25}(多い｜大きく｜高く｜増え)`) to `FINAL_SENTENCE_TEMPLATES`, measured across all 15 papers first |
| NF-3 | In `tests/20260821_1/聴解.md`, 問題2 解説, 1番: change option 1's quote from 「ただ、そこが分かれるところなんですけど、飛行機の座席だけは、少し違いまして。」 to **「座席の分のお金だけは、二十日前より早くご連絡いただいても、そのままいただきます。」** and keep the gloss 「→「どの分も」ではないと訂正される」. No script, option, key or position changes; `make sheet` afterwards |
| NF-4 | Sync the theme records for the two surfaces, in whichever direction is judged right, and put the reason in a `note` on BOTH `test_spec.json` and `logs/ledger.json` (`origin` is not needed — the draws shipped as drawn; only the tag is wrong). Cheapest: set both files' `listening_scenarios` themes to 行政・手続き (市役所:手続き案内) and デジタル化 (コールセンター:本人確認), matching `topics.json`, each with `"note": "pools.json's tag did not describe the authored item; re-tagged from the shipped script per exam-qa-review §5"`. Also correct the two `pools.json` tags, which is where the wrong tag originates |
| NF-5 | (a) In `tests/20260821_1/聴解.md`, replace the 「未実施」 sentence with what is actually on disk: 「`logs/topics.json` の該当行の `surfaces`／`shapes`／`notes` は更新済み。`themes` は スポーツ・余暇 のまま（spec/ledger と一致させるため意図的）。」 (b) In `logs/topics.json` entry 15's `notes`, delete the 「THE ONE WARN, AND WHY IT IS A FALSE POSITIVE」 paragraph and update the opening line to `make check` exit 0 at **451** warnings with **no** WARN naming this test except the aggregate `pools_sha` record — the F1/F1b gate repairs closed that WARN, and a note arguing a false positive that no longer fires will send the next paper's blueprint stage chasing a bug that is fixed |

### Minor observations — recorded, no repair demanded

- **O1 — 問題9 and 問題13 are the same narrator.** Both are first-person accounts of a
  multi-year solitary physical practice (十年近く、朝四時からの岸壁 / 七年続けた朝の走り)
  whose argument rejects the naive account of why the author keeps at it
  (「趣味は結果が出なければ意味がない」 / 「差を意志の強さで説明したくなるところだが」) and
  substitutes a less obvious one. The theme tags (スポーツ・余暇 vs 科学・技術) and the shape
  labels (反論応答 vs 意外な観察) both hide it, exactly as F4's pair was hidden. **Not filed
  as a finding**, on measurement: the two subjects genuinely differ (釣り vs 走る習慣), the
  two CLAIMS genuinely differ (the *value* of a hobby vs the *mechanics* of habit
  maintenance), and 問題13's theme comes from its drawn pool topic 「習慣化の仕組み /
  科学・技術」, not from an author relabel — so no tag is doing collision-hiding work here.
  The free surface is the 問題9 cloze (a cloze carries no draw), and it is the one to
  re-subject in the next paper. This is the class the round-1 root-cause table's proposed
  per-surface **`claim`** field would catch, and that field is still not implemented.
- **O2 — 聴解問題3-3番 / 3-4番** sit adjacent, both tagged スポーツ・余暇, both at an exercise
  facility (市民プール / スポーツクラブ). The 構成表 argues it (場面・種別・決め手 all differ),
  the establishment-type check is green, and the adjacency was created by the 2026-08-21
  re-slot rather than by any round-1 repair. Recorded.
- **O3 — 問題4** runs 5 of its 11 stimuli on 働き方/会社 (1番, 2番, 3番, 9番, 11番). Untouched
  by the repairs and passed by round 1; noted for the next paper's spread.
- **O4 — `（注N）`** in-body markers across 問題10–13 = **27**: clears the gate floor (25) and
  the bottom of the official band (27–61) but sits under `dokkai.md`'s ~30–40 target, and
  問題12 and 問題14 carry **zero**. Unchanged from round 1; raise it in the next paper.
- **O5 — every 読解 section is now within 13–35 chars of its ceiling** (問題10 1295/1330,
  問題11 2676/2700, 問題12 574/600, 問題13 1057/1070). The F3 closings landed inside, but any
  future edit that adds a sentence to 問題11 or 問題13 breaches the ceiling. NF-2's repair
  must replace, not append.
- **O6 — a gate reporting defect:** the `解説 quotes trace to the passage/script` check
  emits its name without a test id (`聴解.md: …`), so its two WARN lines cannot be
  dispositioned per AGENTS.md §0.5 without grepping the corpus. I traced all three: the quoted
  strings live in `20260812_1/言語知識・読解.md`, `20260814_1/聴解.md` and
  `20260819_1/聴解.md`, not in this paper (`grep -rl` on each quote).
  Both of this paper's trace lines are `ok`. Worth a `test_id=` argument.

### NF-1, measured across the whole corpus (the recurrence test, applied not assumed)

`REFRAME_CLOSING` is scanned over `jp_tail(prose, 2000)`, and 2000 exceeds every passage
in the repo — so despite its name it scans each passage's **full prose**. That was a
deliberate anti-dodge widening (`qa-report-20260813_2` F-CLOSING-2). The cost had never
been measured. I measured it: of the **33 hits it produces across all 15 papers, 20 fall
outside the passage's final two sentences**, i.e. two-thirds of what a check called
"closing reframe" counts is not a closing.

| paper | hits | of which mid-passage |
|---|---|---|
| 20260807_1 | 2 | 2 (だけでは ×2) |
| 20260810_2 | 4 | 3 | 
| 20260811_1 | 2 | 1 |
| 20260812_1 | 3 | 1 |
| 20260812_2 | 5 | 3 |
| 20260813_1 | 2 | 1 |
| 20260813_2 | 1 | 1 (**というより**) |
| 20260814_1 | 2 | 2 |
| 20260817_1 | 4 | 2 |
| 20260817_2 | 4 | 2 |
| 20260817_3 | 2 | 1 (**というより**) |
| **20260821_1** | **2** | **1 (というより, 問題13 paragraph 2)** |
| 20260810_1 / 20260818_1 / 20260819_1 | 0 | 0 |

So on this paper the round-1 widening's entire contribution is a false positive, and the
paper's genuine second reframe closing (問題9's 「教えたのではなく、見る力を与えたのだと
思う」, the **penultimate** sentence of a two-sentence closing) is seen by neither check —
`REFRAME_CLOSING` excludes bare 「のではなく」 by design, and `FINAL_SENTENCE_TEMPLATES`
reads only the LAST sentence. The reported `2 matched` equals the true count of 2 purely
by coincidence: one false positive standing in for one miss.

---

## §6.5 Root-cause table

Recurrence test applied first, by measuring the other papers, not by judgement.

| finding(s) | root cause | how many papers show the class | owning file | concrete proposed edit |
|---|---|---|---|---|
| **NF-1** | `GATE-WRONG` — a check whose name and whose consumers (dokkai.md's cap, round-1's F3 read) treat it as a closing-shape count, while 20 of its 33 corpus-wide hits are mid-passage tokens | **12 of 15** produce at least one mid-passage hit; **3** (20260813_2, 20260817_3, 20260821_1) get one specifically from the newly added 「というより」 | `tools/check_consistency.py` (`REFRAME_CLOSING`, `check_dokkai_closing_reframe`, `FINAL_SENTENCE_TEMPLATES`) | **Split the check in two.** (1) Keep the whole-passage scan as the anti-dodge net but **rename it** so no reader mistakes it for a shape count: `no more than 2 読解 passages CONTAIN this reframe marker family anywhere` — and **remove 「というより」 from it**, since it is a comparative hedge in ordinary prose (the exact reason the same comment block routed 「わけではない」 to sentence scope) and it is already in `FINAL_SENTENCE_TEMPLATES`. (2) Add a **closing-scope** check over each passage's final **two** sentences (`passage_final_sentence()` generalised to `parts[-2:]`) with the family extended to bare 「(の)ではなく」 — that, and only that, sees 問題9. Re-run both over all 15 papers and print which ids move before committing (§6.5's founding-case rule); at two-sentence scope the bare-「ではなく」 cry-wolf figure must be re-measured, because the 100 %-of-corpus number quoted in the comment was taken at passage scope |
| **NF-2** | `RULE-UNENFORCEABLE` (the "two sharing a shape must also differ at template level" half has no counting procedure and no gate) **compounded by an internal contradiction in the owner file** about whether 問題12 is one surface or two | the template-pair class: **2** (`20260817_2`'s three pairs, named in `dokkai.md`; this paper's 問題11(1)/問題12(A)) → systemic by definition. The 12-vs-13 contradiction: all 15, since the gate has read 13 finals since 2026-08-19 while the prose says twelve | `question-authoring/references/dokkai.md` §"Thirteen surfaces…"; `tools/check_consistency.py` `FINAL_SENTENCE_TEMPLATES` | (1) In `dokkai.md`, replace the two conflicting sentences with one rule: **"問題12 A and B are TWO closings and TWO template rows, and ONE theme row. The shape cap of 2 is counted over the 13 closings."** Then 条件提示 ×3 on this paper is a stated breach and NF-2's repair is forced rather than argued. (2) Add the correlation skeleton the pair shares to `FINAL_SENTENCE_TEMPLATES`: `"A ほど/では B が多い": re.compile(r"(では｜ほど)[^。]{0,25}(多い｜大きく｜高く｜増え|なっていた)")`, measured over all 15 papers first — this is the one template family the dictionary has no entry for, and it is where 条件提示 closings pile up by construction |
| **NF-3** | `RULE-IGNORED` — step 1 already says "Copy the deciding line into the 解説 cell if absent"; the F6 fix wrote the new deciding line into the script and the 構成表 and stopped | **1** on this exact shape, but it is the generic self-reconciliation failure mode `exam-qa-review` §"Why this skill exists" item 1 names, so no rule change is warranted | nothing to change — process failure (AGENTS.md §0) | Apply the repair. If a rule edit is wanted, it belongs in `exam-qa-review`'s **fix-pass** guidance: "a fix that ADDS or CHANGES a script line must re-derive every 解説 cell and 構成表 cell that cites that item, not only the cell the finding named" |
| **NF-4** | `RULE-IGNORED` in the paper, on top of a `RULE-UNENFORCEABLE` residue: the rewritten rule reclassifies the severity but still ends in a two-file sync instruction that no check reads | **2** of 15 carry a spec↔topics theme disagreement (`20260813_1`'s 問題13 precedent named in the rule, and this paper's two 聴解問題2 surfaces) | `tools/check_consistency.py`; `.agents/exam-qa-review/SKILL.md` | Make it string-decidable, because it is: add `check_theme_record_agreement(test_id)` — for every surface present in BOTH `test_spec.json`/`logs/ledger.json` and `logs/topics.json`, WARN when the two `theme` values differ **and neither record carries a `note`**, and stay silent when a `note` explains it. That converts "sync both files" from prose nobody can verify into a line in `make check`. Founding-case run: on this paper it must print the two 聴解問題2 rows; on the other 14 it must print only `20260813_1`'s 問題13 |
| **NF-5** | `PIPELINE-GAP` — nothing in the fix loop re-reads the notes a fix invalidates, and there are now three places a repair is narrated (`聴解.md` 構成表, `logs/topics.json` `notes`, the QA report), with no rule about which is authoritative | **2** documented (`20260817_3`'s two false `notes` claims, named in the skill; this paper's two) | `.agents/jlpt-test-generation/SKILL.md` (stage-4 fix loop) + `tools/check_consistency.py` | (1) Add to the stage-4 fix loop: **"after applying a fix, `grep` every note that names the finding id you just closed — in `聴解.md`'s 構成表, in `logs/topics.json`'s `notes`, and in the QA report's disposition column — and update each. A note that says a step is 未実施 after you implemented it is a defect of the same class as a note quoting a removed string."** (2) String-decidable half, worth a check: WARN when a `logs/topics.json` `notes` field contains a WARN name that `make check` no longer emits for that test id, or a warning TOTAL that differs from the current run — both are literal strings in the note and in the gate's own output |
| **O1** (not filed) | `RULE-MISSING` — `dokkai.md` axes count THEME (axis 1), CLOSING MOVE (axis 2) and VOICE/REGISTER (axis 3). Nothing counts the **narrator archetype**: this paper runs 5 一人称随筆 surfaces and two of them are the same person doing the same kind of thing for the same number of years | **1** paper, so prevention not repair | `question-authoring/references/dokkai.md`; `logs/topics.json` | Implement the round-1 F4 root-cause proposal that is still open — a per-surface **`claim`** field in `logs/topics.json`, one sentence naming what the surface ASSERTS — and extend it with a `persona` token for the 一人称 surfaces (`趣味の実践者 / 職業人 / 親 / 観察者 / 研究者`), capped at 2. Both are author-time columns; neither can be derived by a script from the prose, which is why they must be recorded |

### Did the round-1 root-cause fixes close the classes they claimed?

| round-1 fix | class it claimed | verdict, measured |
|---|---|---|
| `dokkai_profile._parse_generated_dokkai` marker walk (F1) | 問題10 (2)–(5) parsed as empty on every paper; 4 of 20 読解 items dropped from the overlap check | **CLOSED.** The parser now returns 12 passages with lengths 272/262/267/274/275 for 問題10 and **20 of 20** items carrying a passage |
| `check_dokkai_register()` gloss stripping (F1b) | a passage whose last physical line is a gloss can never read polite | **CLOSED.** Gate prints `polite voice (です・ます) passages >= 3 (got 3)`; no paper text was rewritten to get there |
| widened `REFRAME_CLOSING` (F3) | 「というより」/「よりも…なのだ」 invisible to the reframe family | **NOT CLOSED — regressed.** See NF-1: at whole-passage scope 「というより」 is a manner hedge, its only hit on this paper is a false positive, and the closing it was meant to make visible (問題9's) is still invisible to both checks |
| new `check_choukai_opening_frame()` (F2) | four item openers on one frame, unchecked | **CLOSED, and correctly founding-case-verified.** Its docstring records the run over all 15 papers, reports ×4 on the four original openers, and names the two shipped papers it newly flags (`20260811_1`, `20260814_1`) instead of hiding them |
| frame-aware `check_key_grammar_exposure` (F7) | a keyed connective re-used in the identical frame at n=1 | **CLOSED, and correctly founding-case-verified.** The docstring records "run against 20260821_1's PRE-repair 問題10(1) sentence… it reports 1… the shipped prose reads 「…教わると、」 and reports 0", and zero same-frame hits corpus-wide, so it re-classifies no shipped paper |
| new `check_mondai6_option_length()` (F8) | 問題6 option sentences drifting to the bottom third of the official range, unchecked | **CLOSED.** It prints mean/median/range/over-30 count, and it is what caught this paper's own drift being repaired (21.1 → 26.3) |
| `origin`/`note` on the re-realised 問題3 draw (F5) | 問題3 unchecked by `check_choukai_drawn_items` | **CLOSED for the record**, and the fixer improved on the round-1 instruction by refusing the proposed rename. The gate line `every drawn 聴解 medium ships as drawn or is recorded` is now `ok` for this paper |
| the spec↔topics theme rule rewrite (F9) | an automatic-fail classification that fires on honest §5 re-tagging | **RULE CLOSED, PAPER NOT.** The reclassification is right and well-argued; the two-file sync the same rule demands was never applied — NF-4 |
| the per-surface `claim` field (F4 root cause) | cross-surface assertion collisions that theme tags hide | **NOT IMPLEMENTED.** `logs/topics.json` has no `claim` field, and its own F4 note says so. O1 is the class walking in again on a different pair |

---

## Coverage statement

| step | ran on | how |
|---|---|---|
| entry condition | whole repo | `make check` re-run by me: exit 0, 451 warnings, one aggregate `pools_sha` line naming this test, one expected `skip` |
| 0 blind solve | 問題6, 問題10, 問題11, 問題12, 問題13, 問題14, 聴解問題2, 聴解問題3 = **36 scored items** (+2 例 read for answerability) | `make keyless 20260821_1` rebuilt at the reviewed shas; solved from `qa/20260821_1/keyless.md` only, keys opened afterwards. **36/36 agreement** |
| 0b strategy passes | not re-run | round 1 measured 33.3 % / 33.3 % on the repaired parse (bar 45 %). The gate's own equivalents are re-measured on the CURRENT paper and both pass with margin: `keys share less passage bigram surface than distractors (median margin −0.076 ≤ 0)`, `keys strict top-overlap share 35 % ≤ 46 %`, `key is not UNIQUELY the longest option (4/20 = 20 %)`, `not predictably the longest (6/20 = 30 %)`. The F3 closings moved these numbers the safe way |
| 1 key-by-key proof | the 36 in-scope items + 2 例, plus every other item's round-1 deciding quote re-verified as still present on disk (step 1b) | deciding quote pasted per row |
| 2 / 2b two-answer hunt | the 36 in-scope items | one impossibility per wrong option in the walkthrough |
| 2.5 level band | 問題6's five keys (the only tested items the repairs touched) | archive attestation counts + both textbook extract sets |
| 3 mechanical reads | whole paper | 問題1/2/5 stems **14 of 15 comma-free** (author floor 9), median **16** chars (archive max 21.5); 問題1–5 register **8 polite of 25** (official 2–11); 問題7 distribution mean **49.2** in 36–52, **3** stems under 34, spread **42** ≥ 25; `（注N）` in-body **27** (floor 25, official 27–61); 読解 option ratio max/min ≤ 1.65; 問題6 mean 26.3 / median 26.5 / range 18–34 |
| 4 聴解 structure | 問題2 and 問題3 as COLUMNS, verified against the script line by line | opening-move column (7 distinct moves), 決め手の種類 column (no token > 2), 質問型, 正解, closing turns, talk lengths 272–293, `SPEAKER_MAP` genders 3M/3F in 問題3, voice turns 52/48 in 問題2 |
| 5 topic table | all 34 surfaces, three papers | tables above. Headline set: ∅ vs previous, {住まい} vs two-back |
| 6 provenance | all 22 recorded draws, all 101 positions | positions 101/101; ledger ≡ spec; one `reauthored` entry with `note`; **theme records disagree — NF-4** |
| 6.5 root cause | all 5 findings + O1 | table above, each with a founding-case requirement stated |

### Every `make check` line naming `20260821_1`, with its resolution

- **WARN `every stamped spec's pools_sha matches pools.json (cea9612d1e0b)`** — `20260821_1`
  appears **only** in the informational "stamped on a REROLL" tail, not among the 13 ids with
  a mismatching sha. Its recorded `pools_sha` is `cea9612d1e0b`, equal to the live pool.
  **Not a finding** (the check's own message says it is a record).
- **`skip` `詳細解説.json options match the booklet — no 詳細解説.json`** — expected: the
  model-answer step is by design the LAST pipeline step, after QA passes (AGENTS.md §5).
  **Not a finding.**
- Every other line naming this test (≈120 of them) is `ok`, including the round-1
  polite-voice WARN, now `got 3`.
- Three WARN lines in the run carry **no test id** (`聴解.md: 解説 quotes trace…` ×2 and
  `言語知識・読解.md: 解説 quotes trace…` ×1). I traced all three by grepping the quoted
  strings: they belong to `20260812_1`, `20260814_1` and `20260819_1`. **Not this paper**,
  whose two trace lines are both `ok`. The missing id is recorded as **O6**.

### Source stillness

Re-measured at the end of the review, identical to the header:
`言語知識・読解.md fb8f95b2…` (11:05:02), `聴解.md e7b94086…` (11:36:30),
`聴解スクリプト.txt 1390752d…` (11:04:30), `test_spec.json 9077f3d3…` (11:16:49),
`logs/topics.json` (11:15:26), `logs/ledger.json` (11:16:49). **Nothing moved under me**;
every row above is a claim about these bytes.

## Skips, stated

1. **The 65 items outside the six touched 大問 were not re-blind-solved.** Justification is
   step 1b: every deciding quote round 1 recorded for them is still on disk byte-for-byte,
   round 1's blind solve reproduced 101/101, and the skill's re-review scope is "changed
   items AND their whole 問題". Those rows are inherited from `qa-report-20260821_1.md`, not
   re-asserted here.
2. **The two blind STRATEGY passes were not recomputed by hand** — the four gate metrics
   that measure the same exposure were re-measured on the current paper instead, and all
   four pass with margin. Stated because it is a substitution, not an equivalence.
3. **The MP3 was not listened to.** Verified structurally only: `script_sha 1390752d08e9`
   equals the live script, `pacing_sha 4d623645a38d` current, pause tail > 1.05 s, and
   mtime 11:08 > script 11:04. So the audio speaks the repaired 問題2/問題3 text.
4. **No fix was applied.** All five findings are left open: NF-1/NF-2's second half are
   generation-tooling and owner-file edits a reviewer may not make mid-review, and
   NF-2/NF-3/NF-4/NF-5 are the author's work list.
5. **`問題3-13 ずくめ`'s band conflict** (`level_band_grammar.txt` TOO_HARD vs `pools.json`
   offering it as a drawable target) is inherited from round 1 as "recorded, not failed"; I
   re-read it and agree with that disposition, and it remains an open reconciliation task
   against `exam-blueprint`.

## QA: FAIL (5 findings, 0 automatic) — as of this report's writing, 2026-08-24

Two paper findings (NF-2 問題11(1)/問題12(A) closing-skeleton pair, NF-3 聴解問題2-1番's
un-re-quoted 解説), two record findings (NF-4 the unapplied F9 sync, NF-5 two notes the
repair pass invalidated) and one gate finding (NF-1, blocks the next generation run).

**Eight of the ten round-1 dispositions hold on measurement; one (F3) holds in the paper
while its gate fix regressed; one (F9) was not applied at all.** No repair introduced a
mis-key, a second defensible answer, an ungrounded distractor, an untraceable 解説 quote or
a length-ceiling breach — the 36 re-solved items came back 36/36 and all four 読解 sections
sit inside their ceilings with 13–35 chars to spare.

## Post-hoc verification (2026-08-27) — all 5 findings closed, this report's own verdict is stale

This "Skips, stated" §4 ("No fix was applied. All five findings are left open.") and the
FAIL verdict above describe the state at the moment this report was drafted. **The same
commit that shipped this report (`18e91bc`) also shipped fixes for all five findings**, and
the report text was never updated to say so — the exact "note describing a step as 未実施
after it was implemented" defect class NF-5(a) itself names, now applying to this report.
Verified by re-reading current disk state before generating the next paper (`20260827_1`),
since the pipeline rule blocks sampling while any test's QA is open:

- **NF-1** — `tools/check_consistency.py` splits the check as prescribed:
  `check_dokkai_closing_reframe` stays the whole-passage anti-dodge net (「というより」
  removed from its family), and `check_dokkai_closing_reframe_scope` (new) reads the
  final-two-sentence closing scope, generalised via `dokkai_closing_scopes()`. Measured
  across all 15 papers before landing (comment block at `tools/check_consistency.py:1765`).
- **NF-2** — `question-authoring/references/dokkai.md` §"The denominator" (added 2026-08-24)
  settles the 12-vs-13 conflict (問題12 = two closings/two templates, one theme row) and adds
  the `A では/ほど B が多い（相関）` template. `20260821_1`'s 問題11(1)/問題12(A) pair is
  explicitly grandfathered as compliant under the resolved rule, not rewritten — recorded in
  the doc, not silently dropped.
- **NF-3** — `tests/20260821_1/聴解.md` 問題2 解説 1番, option 1's quote now reads 「座席の
  分のお金だけは、二十日前より早くご連絡いただいても、そのままいただきます。」, with an
  explicit note dated 2026-08-24 citing this finding by id.
- **NF-4** — `test_spec.json` and `logs/ledger.json` both carry a `note` on the
  `市役所:手続き案内` and `コールセンター:本人確認` draws explaining the deliberate
  record/tag split, and `check_theme_record_agreement()` now reads it (`tools/
  check_consistency.py:5548`).
- **NF-5** — `tests/20260821_1/聴解.md`'s 問題3 構成表 note now says 実施済み and describes
  what changed; `logs/topics.json` entry 15's `notes` field replaced the stale 446/WARN
  paragraph with a dated re-measurement.

`make check` run 2026-08-27 names zero lines for `20260821_1` (one unrelated pre-existing
FAIL on `20260810_1`, a different in-flight repair track, not touched here). **Verdict
stands corrected: QA: PASS (applied under the round-2-FAIL fallback, same day, per
`jlpt-test-generation/SKILL.md`).**
