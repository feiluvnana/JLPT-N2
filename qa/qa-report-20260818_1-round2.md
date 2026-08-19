# QA report — テスト 20260818_1 (ROUND 2, fresh context)

## Verdict

**QA: FAIL (9 findings, 2 automatic)** — reasoning in §8, findings in §3, root causes in §4.

Automatic: **R2-F1** 問題8-45 admits a second grammatical ordering (★=1 or ★=3); **R2-F2** 聴解問題4-2番 and 4-9番 still run the same drawn errand. Also open: R2-F3 (問題5-2番 errand inside its cooldown), R2-F4 (two 聴解 slot-domain repeats, deferred without authority), R2-F5 (調剤師), and R2-F6–F9 against the gate and the sampler, which block the next generation run. **The blind solve agreed with all 101 keys — nothing is mis-keyed.**

(Section 0 below is placed first because the coordinator required the 101 blind-solve answers to reach disk before any key table was opened; the required verdict line is here and repeated at the end.)

- Reviewer: fresh-eyes context. Authored nothing, fixed nothing, had never seen the key table when Section 0 below was written to disk.
- Timestamp (start): 2026-08-19
- Reviewed revision (sha1, raw bytes):
  - `tests/20260818_1/言語知識・読解.md` = `74377463d2e209a8fd555bddddf4152675e070ab`
  - `tests/20260818_1/聴解.md` = `402cb515898a7dbf8eda9d972bbb6ebe124798df`
  - `tests/20260818_1/聴解スクリプト.txt` = `2fbe5bf222dfd2e3e3d1bfef13801a51300e5f1b`
- mtimes at start: 言語知識・読解.md Aug 19 16:22:14, 聴解.md 16:10:59, 聴解スクリプト.txt 16:10:17, 聴解.mp3 16:27:07, 聴解_チャプター.json 16:27:07, 解答.html 16:28:53, test_spec.json 16:12:31
- Entry condition: `make check` → **All checks passed (27 skipped), 127 warning(s)** across all 13 papers. WARNs naming this paper are resolved in §6 below. (The `20260818_1` WARN text was deliberately NOT read until after Section 0 was on disk — several WARN messages in this repo print keyed option numbers.)

---

## Section 0 — BLIND SOLVE (written before any key was opened)

Solved from `qa/20260818_1/keyless.md` **only** (1068 lines: the 101 items plus the verbatim 聴解スクリプト). 聴解 solved from the embedded script; the MP3 was not played (no audio playback available in this environment — see §7 Skips).

### 言語知識・読解 (1–71)

| 問題 | items | my answers |
|---|---|---|
| 問題1 | 1–5 | 1, 4, 1, 3, 4 |
| 問題2 | 6–10 | 4, 4, 1, 2, 2 |
| 問題3 | 11–13 | 1, 4, 4 |
| 問題4 | 14–20 | 1, 1, 4, 1, 3, 2, 4 |
| 問題5 | 21–25 | 2, 1, 1, 2, 2 |
| 問題6 | 26–30 | 2, 3, 3, 3, 2 |
| 問題7 | 31–42 | 1, 3, 2, 4, 4, 1, 3, 1, 2, 2, 1, 3 |
| 問題8 | 43–47 | 4, 4, 1, 1, 2 |
| 問題9 | 48–51 | 4, 2, 2, 3 |
| 問題10 | 52–56 | 3, 1, 4, 3, 3 |
| 問題11 | 57–64 | 3, 2, 4, 4, 2, 4, 3, 4 |
| 問題12 | 65–66 | 4, 4 |
| 問題13 | 67–69 | 1, 3, 2 |
| 問題14 | 70–71 | 4, 2 |

Flat list, items 1→71:
`1,4,1,3,4, 4,4,1,2,2, 1,4,4, 1,1,4,1,3,2,4, 2,1,1,2,2, 2,3,3,3,2, 1,3,2,4,4,1,3,1,2,2,1,3, 4,4,1,1,2, 4,2,2,3, 3,1,4,3,3, 3,2,4,4,2,4,3,4, 4,4, 1,3,2, 4,2`

### 聴解 (30 items; 例 excluded)

| 問題 | items | my answers |
|---|---|---|
| 問題1 | 1–5番 | 1, 3, 3, 3, 2 |
| 問題2 | 1–6番 | 3, 1, 2, 2, 1, 2 |
| 問題3 | 1–5番 | 4, 4, 3, 1, 3 |
| 問題4 | 1–11番 | 2, 3, 1, 1, 2, 1, 3, 1, 2, 3, 3 |
| 問題5 | 1番 / 2番質問1 / 2番質問2 | 3 / 2 / 1 |

Flat list, 聴解 in paper order:
`1,3,3,3,2, 3,1,2,2,1,2, 4,4,3,1,3, 2,3,1,1,2,1,3,1,2,3,3, 3,2,1`

### Items I answered with reservation (recorded before the diff)

- **問7-36** (`僕に（　）よ`): chose **1 解けっこない**. `解けようがない` (option 2) is morphologically formable off 解ける's stem, so this needed a judgment call; `〜っこない` is the colloquial form that pairs with 「僕に」＋possibility, and B's register is casual. If the key is 2, this is a candidate two-answer item.
- **問2-7** (`重さを…はかる`): chose **4 量る**. `計る` (option 1) is the general-purpose はかる and is written for 重さ in ordinary non-official usage; the 常用漢字 付表 split (量る=重さ・容積 / 計る=時間・数) is what makes 4 uniquely right. Flagged for step 2.
- **問1-5** (`見にくい`): chose **4 みにくい** with no doubt about the answer, but the option SET (よみにくい／きづきにくい／わかりにくい) is not the target's own readings — filed as a step-2b question, not a solving doubt.
- **問7-31** (`素朴というか（　）`): chose **1 物足りないというか** on the 「AというかBというか」 frame.

---

## 1. Blind-solve diff

**File solved from:** `qa/20260818_1/keyless.md` (sha1s in the header above), plus the 聴解スクリプト embedded verbatim inside it. Nothing under `tests/20260818_1/` was opened until this section was written.

```
python3 tools/qa_eval.py tests/20260818_1 --answers "[...101 answers...]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches.** All four reserved items resolved in the key's favour:

- 問7-36 key = **1 解けっこない** — agrees. `解けようがない` is examined again in step 2 below (it is the one distractor in the paper closest to defensible).
- 問2-7 key = **4 量る** — agrees.
- 問1-5 key = **4 みにくい** — agrees; the option-set question is carried into step 2b.
- 問7-31 key = **1 物足りないというか** — agrees.

A 101/101 blind solve is evidence the keys are *findable*, not that each distractor is *impossible*; steps 2 and 2b carry that load.

---

## 2. Per-question walkthrough — all 101 items

Sources read side by side: `tests/20260818_1/言語知識・読解.md`, `聴解.md`, `聴解スクリプト.txt`, `test_spec.json`, `logs/ledger.json`, `logs/topics.json`, plus `refs/JLPT_N2_NEW/*` for calibration. Every non-OK row names the string and the repair.

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 1 だいり | OK | 2×2 {だい,たい}×{り,じ} all four printed; たいじ=退治, だいじ=大事 are real words, たいり a 清音 derivation. 代 has タイ (交代) so branch 1 holds | — |
| 問題1-2 | 4 とかい | OK | {と,ど}×{かい,がい}; どがい homophone of 度外. Okurigana absent, nothing selected on sight | — |
| 問題1-3 | 1 ひがん | OK | {ひ,び}×{がん,かん}; ひかん=悲観, びがん=美顔, びかん=美観 all real. Stem 「墓参りをする」 fixes 彼岸 | — |
| 問題1-4 | 3 しんけい | OK | {しん,じん}×{けい,きょう} — 神=ジン(神社), 経=キョウ(経典) both real alternate on-readings, so the grid is principled, not arbitrary | — |
| 問題1-5 | 4 みにくい | OK | Official prints this exact shape: 7/2025 問1-2 辛い→あまい/からい/にがい/しぶい and 問1-5 収まった→さだまった/しずまった/おさまった/やすまった (`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md` L4, L7). All four are real 〜にくい adjectives fitting 「案内板が…」; the printed 「にくい」 is shared so no option is selected by okurigana | — (round 1's clearance independently re-verified against the PDF-derived booklet) |
| 問題2-6 | 4 基礎 | OK | 2×2 {基,規}×{礎,祖}; 規礎/基祖/規祖 are non-words, all 4 glyphs 常用 | — |
| 問題2-7 | 4 量る | OK | 「粉の**重さ**を一グラム単位で」. 常用漢字 usage split: 量る=重さ・容積, 測る=長さ・速さ, 計る=時間・数, 図る=意図する. 計る is the only near-rival and its own domain is time/number, stated in the 解説 | — (judged, not waved: the disambiguator is 「重さ」 alone, which is how official homophone-verb items work) |
| 問題2-8 | 1 支援 | OK | {支,枝}×{援,演}; 枝援/支演/枝演 non-words | — |
| 問題2-9 | 2 休業 | OK | {休,求}×{業,行}; 求業/求行/休行 non-words | — |
| 問題2-10 | 2 促進 | OK | {促,側}×{進,信}; 側進/促信/側信 non-words. None of the 8 pseudo-compounds occurs anywhere in `refs/` (grepped) | — |
| 問題3-11 | 1 再 | OK | 「一度は承認された計画だが」 forces "again"; 初/続/新+検討 form no word | — |
| 問題3-12 | 4 深 | OK | 「光がほとんど届かない」→深海; 高海/低海/重海 are non-words. Official does NOT require all four to attach (moji-goi.md §問題3) | — |
| 問題3-13 | 4 量 | OK | 「渋滞が絶えない」→交通量; 率 collocates with 高い not 多い, 費 is a real word (交通費) but names a fare | — |
| 問題4-14 | 1 初旬 | OK | F7 closed: 「**同じ月の**五日ごろにはお手元に届きます」 now fixes the month, so 中旬/下旬/月末 are excluded by the printed text, not by a default reading | — |
| 問題4-15 | 1 超一流 | OK | 「世界中のホールから招かれる」「だれもが認める」; 一人前/駆け出し/半人前 all sit below that | — |
| 問題4-16 | 4 上げた | OK | 「入社したころは失敗ばかり」→腕を上げる. 腕を伸ばす = physically extend; 腕を高める is not a collocation | — |
| 問題4-17 | 1 当分 | OK | Forward-looking instruction 「控えるように」; いまだに is retrospective, のちほど is minutes-away, たちまち is instantaneous | — |
| 問題4-18 | 3 食う | OK | 燃料を食う (cf. 時間を食う/電気を食う); 吐く reverses the direction | — |
| 問題4-19 | 2 間もなく | OK | Station announcement immediately before arrival; たった今 is past, 今にも needs 〜そうだ | — |
| 問題4-20 | 4 付き合って | OK | 「一人では決められないので」→同行. 立ち会う is third-party attendance, 掛け合う is negotiation | — |
| 問題5-21 | 2 一羽もいなくなった | OK | 絶滅 = none left; 数が減った/めったに見られない leave survivors, 島の外へ移った keeps the species | — |
| 問題5-22 | 1 怖くて | OK | 熊+足が動かない = fear; 悔しい/情けない/苦しい name other emotions | — |
| 問題5-23 | 1 落ち着いた | OK | All four modify 口調 (same functional category); only 落ち着いた means 穏やか. 事務的 is cold, 遠回し is indirect, よそよそしい is distant | — |
| 問題5-24 | 2 危なくなった | OK | 危うい = at risk, not yet cancelled; 取りやめ is already decided, 遅れた keeps realisation | — |
| 問題5-25 | 2 少しずつ | OK | 「やわらいでいった」 = progressive; すっかり names a completed result, またたく間に the opposite rate | — |
| 問題6-26 | 2 素質 | OK | Key: 「幼いころから音楽家としての素質」 = innate. See the rule-conflict note below on options 1/4 | — (option 1 掃除機 / 4 土地 cross the word's domain, which `exam-qa-review` §2b and `moji-goi.md` §問題6 both forbid — but official does exactly this: 「空には雲が充実している」「コーヒーのにおいが充実している」「テレビの音量を薄めた」「駅のふもと」「犬の定年」, all five verified in `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md`. Filed as **R2-F9**, not against the paper) |
| 問題6-27 | 3 侵入する | OK | 「泥棒が…窓から家に侵入」. 1 観客が会場に (入場), 2 市場に (参入), 4 資料が外部に (流出) — all three stay inside the "enter" domain and break exactly one thing. Exemplary set | — |
| 問題6-28 | 3 転じる | OK | 「黒字に転じた」 = state change. 1 場所を (変更), 2 道が右に (曲がる), 4 倉庫を喫茶店に (転用) | — |
| 問題6-29 | 3 生産する | OK | 「工場で…ジュースを生産」. 1 エッセー, 2 案, 4 弁当 — all inside "make", wrong scale/register | — |
| 問題6-30 | 2 占める | OK | 「アジア向けが全体の約六割を占めて」 — needs a whole. 1 賞金 (獲得), 3 十キロ (absolute), 4 支持 (集める). Same domain note as 26 | — |

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 物足りないというか | OK | 「素朴というか」 is printed, so the frame 「AというかBというか」 wants its second half; というより retracts, どころか needs a contrast that never comes, くせに blames a person | — |
| 問題7-32 | 3 ないものだろうか | OK | 「なんとか」 fixes the wish reading; はず = inference, こと = 詠嘆 (needs なんと), わけ = 理由確認 | — |
| 問題7-33 | 2 ご利用に際して | OK | 掲示 register + a moment of action. に応じて needs a varying variable, に沿って/に基づいて need a 方針/根拠 noun | — |
| 問題7-34 | 4 試合ができるものか | OK | 「グラウンドは池のようになっている」 = rhetorical denial of A's claim; わけか concedes possibility | — |
| 問題7-35 | 4 標高が上がるにつれて | OK | Two co-varying changes; に沿って/にわたって/に先立って all need a noun, not a verb 連体形 | — |
| 問題7-36 | 1 解けっこない | OK | 「無理だよ」 sets a flat colloquial denial; 〜っこない attaches to the potential stem (できっこない). ようがない wants the plain ます-stem 解き and means "no means to"; かねない reverses polarity; きれない means "can't finish". I flagged this pre-diff as the item nearest to two answers and it holds | — |
| 問題7-37 | 3 おそれがあります | OK | Weather warning predicting an unwanted event; ほかありません = no choice, どころではありません = dismissal | — |
| 問題7-38 | 1 平日にもかかわらず | OK | 「ところが当日は朝から晴れ」+「入りきれないほどの人」 = counter-expectation; だけあって would make weekday a reason for crowds | — |
| 問題7-39 | 2 値段が安い上に | OK | 「店員の対応**も**」 demands additive 上に; ものの is adversative, かぎり conditional | — |
| 問題7-40 | 2 風邪気味 | OK | 〜気味 attaches bare to a noun; 加減/具合/気配 all need の (風邪の気配) or name adjustment | — |
| 問題7-41 | 1 駅舎の設備のみならず | OK | 「〜にまで及ぶ」 demands range extension; ばかりに restricts, どころか denies the first term which was in fact done | — |
| 問題7-42 | 3 乗り過ごすところだった | OK | 「もう少しで」+ avoided outcome; ばかりだった = one-way trend, とおりだった = as predicted | — |
| 問題8-43 | 4 観光客にも | OK | 1→2→**4**→3: 「地元の人に限らず観光客にも人気があるそうだ」. 限らず requires bare に, so 観光客に**も**限らず is impossible and 地元の人に is forced before it; 人気がある is the only card that can precede そうだ. Unique | — |
| 問題8-44 | 4 作れるように | OK | 1→2→**4**→3: 「なったと」 needs a quoting verb after it and 〜ように before it; をはじめ…まで is a fixed pair in that order. Unique | — |
| 問題8-45 | 1 おかげで | **自動不合格** | 「共働きの私たちは、＿＿ ＿＿ ★ ＿＿ 慌てずに済んでいる。」 The block [2 祖母が近くに → 3 住んでいてくれる → 1 おかげで] is forced contiguous, so card 4 「子どもの急な熱にも」 may sit **either side of it** and **both readings are grammatical**: key `2→3→1→4` (★=1) and rival `4→2→3→1` (★=3) = 「共働きの私たちは、子どもの急な熱にも祖母が近くに住んでいてくれるおかげで慌てずに済んでいる。」 A main-clause 〜にも adverbial fronted above a subordinate おかげで clause is ordinary Japanese (「彼は突然の雨にも傘を持っていたおかげで濡れずに済んだ」). `言語知識・読解.md` L528's 解説 excludes it with 「『おかげで』を最後に置くと『子どもの急な熱にも』が受け手を失う」 — **that leg is false**: 子どもの急な熱にも's receiver is 「慌てずに済んでいる」, which is printed AFTER the blanks. This is the identical invalid-leg class round 1 filed as F9 at 問題8-47; the fix pass repaired 47 and did not re-read the other four proofs against the corrected standard. `make verify-scramble` returns UNDECIDED with rival ★ values [1,3,4], so no tool contradicts this | Force the last slot from the printed tail. Concrete: move the adverbial into the stem — 「共働きの私たちは、子どもの急な熱にも＿＿ ＿＿ ★ ＿＿。」 with cards 1「祖母が」 2「近くに住んでいてくれる」 3「おかげで」 4「本当に助かっている」 → only ordering 1→2→3→4, ★=slot3=**3**; then re-sync `answer_positions` 問題8[3] (1→3) by swapping the position with an item elsewhere, and re-derive the 解説 |
| 問題8-46 | 1 住宅街へと姿を変え | OK | 2→3→**1**→4: つつある requires an immediately preceding ます-stem, which only 姿を変え is; 伴って requires a preceding に-phrase so it cannot open. Unique | — |
| 問題8-47 | 2 紙で出したがる | OK | 3→1→**2**→4. F9 closed: the 解説 now excludes the rival `4→3→1→2` **semantically** (「高齢の利用者が今も多い電子申請」 makes elderly users numerous *inside* e-application, contradicting the sentence, and leaves 「紙で出したがるそうだ」 subject-less) rather than by the invalid "connects to nothing" leg | — |
| 問題9-48 | 4 言い換えれば | OK | [論理接続] The following sentence restates the preceding observation in general terms; たとえば promises an example that never comes, しかも adds nothing new, それどころか needs a denial | — |
| 問題9-49 | 2 言うまでもない | OK | [慣用・形式名詞] The mechanism was just explained (「中身は一枚の絵になる」), so the consequence needs no argument; 思いもよらない/見当もつかない contradict the just-given explanation | — |
| 問題9-50 | 2 のも当然だ | OK | [文末モーダル] Two delivery examples immediately precede; とは限らない/わけがない would cancel them | — |
| 問題9-51 | 3 今後の分を文字で残せばよい | OK | [内容推論] F10's new blank. 「一から打ち直すのは簡単ではないが」 rules out option 2 by the printed 逆接; option 4 contradicts 「大きくすると形がぼやけ」; option 1 picks one delivery mode only. 14 JP chars, inside the ≤16 cap | — |
| — | — | — | Four distinct blank categories, one 内容推論 ✓ (gate). Cloze body = **551 JP chars** (target 500–700). Blank-51's option set shares nothing with either previous paper's 問題9-51 | — |

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 3 | OK | 「遊びの規則が先に決まっているからだ」+「何を話すかを考えなくても…言葉が出てくる」. 1 店が席を決めるとは書かれない, 2 「一人で来た客ばかり」に反, 4 は筆者の予想で観察と違う | — |
| 問題10-53 | 1 | OK | 「ベンチに所在なげに腰を下ろしていられることは、この街にいてよいと言われるのに近い」. 2 「互いに話しかける人はいない」, 3 取り外され人は減った, 4 背もたれの働きは未言及 | — |
| 問題10-54 | 4 | OK | 「話し合う形を先に試した三つの部署では…軽い相談が…二倍近くに増えています」. 2 は増加を減少に反転, 3 は意見の出所を取り違え (アンケート), 1 記録は未言及 | — |
| 問題10-55 | 3 | OK | Three cells combined: 会員限定 ×「一時間ごと」×「前日正午まで承ります」. 1 は「日中は二時間ごとのまま」, 2 は「登録のない方は…二時間ごと」, 4 は「九月三十日までに…これまでの区切り」 | — |
| 問題10-56 | 3 | OK | 「比べる相手を昨日までの自分に置き換えたとき、比較はようやく自分の役に立ち始める」. 1 は「比べること自体は止められない」に反 | — |
| 問題11-57 | 3 | OK | ①の直後「相手との関係によって言い方を変えなければならない」. 1 は「語の数の不足ではない」と明示的に否定 | — |
| 問題11-58 | 2 | OK | 「手順書を平易な日本語に書き直したうえで、聞き返してよいという合図を先に決めていた」 | — |
| 問題11-59 | 4 | OK | 「あらかじめ日時と会場を印刷し、来られない場合だけ連絡を求める形」. 1 は変更前, 3 は精密検査の話 | — |
| 問題11-60 | 4 | OK | 「手数が減ったことが、そのまま受診率の差になっていた」. 3 は「精密検査に進む割合も上がった」に反 | — |
| 問題11-61 | 2 | OK | ①の直後の列挙「祖母の家からなら通える学校がある、下の弟と離れたくない」. 3 は別段落の「難しい場面」の理由 | — |
| 問題11-62 | 4 | OK | 「聞くことと決めることを分けて考えれば…決定の責任が子どもに移ることはない」. 1 は冒頭で紹介された懸念で筆者の主張ではない | — |
| 問題11-63 | 3 | OK | 「覚えた形の隙間に、勝手に自分の癖を置いていったのだと思う」+「運筆を数え切れないほど重ねた手が」 | — |
| 問題11-64 | 4 | OK | 「まねている最中に、まねていない部分が生まれる」. 1/2/3 いずれも本文の否定側 | — |
| 問題12-65 | 4 | OK | A「電車の中で先に手をつけたほうが、頭が余計な準備運動を要らなくなる」/ B「たしかに、電車の中で今日の段取りを立てておけば、午前の仕事の立ち上がりは速くなる」 — both concede it. 2 is A-only (B never mentions 書類), so it is not 共通 | — |
| 問題12-66 | 4 | OK | A「往復の一時間を仕込みに使えるかどうかで…質は変わってくる」 vs B「通勤の時間を仕事に明け渡さないことが…備えになる」 | — |
| 問題13-67 | 1 | OK | ①の直後「建物の骨組みと配管は改修で持たせ、内側の壁は取り払って一部屋を広く取る」. 4 は「駐車場のまま置くのではなく」で逆 | — |
| 問題13-68 | 3 | OK | 「差が出ていたのは、住民が自分たちで使い方を決められる場所が、建物の中に残されていたかどうかである」. 1 は「家賃の安さではなかった」に反 | — |
| 問題13-69 | 2 | OK | 「動かせるのは、住む人が手を入れてよい範囲をどこまで開くかである」+ closing 「住民が手を加えられる余白を残したという共通点がある」. 4 は「割合が低かった」を「見られなくなった」に強めた誤り | — |
| 問題14-70 | 4 | OK | Two constraints: 印鑑登録証明書の受け取り方=「窓口のみ」 AND 「受け取りには申請時の受付番号が必要です」. F2's new condition kills option 3: 「※窓口で受け取る場合は、**申請の翌日以降に**…お越しください」 vs 「申請したその日のうちに」. 1 killed by 窓口のみ, 2 by 「ご本人のみ」. 来週の月曜 is describable from the flyer (翌日以降 is satisfiable) — no invented detail | — |
| 問題14-71 | 2 | OK | Two constraints: 「ご本人か同じ世帯の方」 (Sato qualifies) AND 「十五歳未満の方の証明書は、オンラインでは申請できません」 (the sister is 14). 1 killed by 「送料100円」, 3 by 「お届けまで一週間ほど」, 4 by the same 15-year rule. Both 70 and 71 re-derived cleanly against F2's changed condition — one defensible answer each | — |
| — | — | — | 20 読解 items: max/min ≤1.30 ✓; uniquely-longest key 4/20 = **20 %** (official 20 %, target ≤30 %) ✓; tied-longest 6/20 = **30 %** (official 30 %, target ≤35 %) ✓; no key is a verbatim lift; zero absolute-quantifier/categorical-denial free eliminations (gate: 0 candidates — I re-read all 80 options and agree) | — |

### 聴解 (30 scored items + 4 例)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 4 | OK | 「車にまだ試作品の箱が残ってるから、先に運んできてくれる?」; announced 4 = marksheet pre-mark 4 | — |
| 問題1-1番 | 1 | OK | 「Aの棚の箱、一つずつ数えてくれる?」 2✗台車が修理/3✗数が合わないとはんこ/4✗そのままで平気 — each grounded in a quoted line | — |
| 問題1-2番 | 3 | OK | 「昨日届いた写真、お店ごとのフォルダに分けといてくれる?」 1✗写真がそろってから/2✗会長が手配/3—/4✗市の型で選べない | — |
| 問題1-3番 | 3 | OK | 「今から順番に電話してみてくれる?」 1✗人が決まってから/2✗もう印刷して封筒に/4✗増やさなくて平気 | — |
| 問題1-4番 | 3 | OK | 「伺いたいことを先にメールでいただけますか」→「今日中にお送りします」 1✗記事の中身が決まってから/2✗改装で閉めている/4✗細かい数字が手元にない | — |
| 問題1-5番 | 2 | OK | 「そちらにお電話で空きを伺ってみてください」 1✗要りませんよ/3✗枠が取れた方にお渡しする決まり/4✗診断書は求めておりません | — |
| 問題2-例 | 4 | OK | 「二週間、コーヒーをやめてみます」; announced 4 = pre-mark 4 | — |
| 問題2-1番 | 3 | OK | 「二十歳以上の方でしたら…大丈夫」→「それなら父に頼んでみます。前の日なら来られる」→「四日の午後でお取りしておきますね」 1✗当日は満枠/2✗本人は前日行けない/4✗管理人は規則で不可 | — |
| 問題2-2番 | 1 | OK | F13 closed: key 「自分の案を実際に作る機会が多いから」 now restates 「自分の手で形にできる回数が、東の方がずっと多いんです。そこが決め手で」 (形にする→作る, 献立→案). 2✗四十分長い/3✗ほとんど同じ/4✗どっちにもある | — |
| 問題2-3番 | 2 | OK | 「子ども、次の日の朝から授業があるので」 rules out the cheap Wednesday; 1✗「後ろでも構いません」/3✗安さを退ける/4✗「妻は日曜も仕事」 | — |
| 問題2-4番 | 2 | OK | 「病院に通いたいというお声をたくさんいただきまして」 1✗「少し増えてるんです」/3✗「工事は去年で終わって」/4✗「人手は…足りております」 — all three denied outright | — |
| 問題2-5番 | 1 | OK | 「地下鉄で振替輸送」+「追加のお支払いはございません」 2✗一時間で三時に間に合わない/3✗相乗りは特急券の客/4✗バスは対象外 | — |
| 問題2-6番 | 2 | OK | 「四十年ずっと、朝五時に起きて川沿いを歩いてた…それだけは」+ closing 「朝のことさえ変わらなければ」 1✗距離は気にしてない/3✗相部屋で平気/4✗こだわりはない | — |
| 問題3-例 | 2 | OK | Museum requests; announced 2 = pre-mark 2 | — |
| 問題3-1番 | 4 | OK | 「三十ページで合わないと感じたら、そこでやめていい」. 問題3 is exempt from the grounding rule by design and this monologue names none of its own distractors (gate ✓) | — |
| 問題3-2番 | 4 | OK | 「頭の中に入れるときではなく、取り出すときに強くなる」 | — |
| 問題3-3番 | 3 | OK | 「環境のための出費は…値段の変化に耐える体をつくる話なんです」 | — |
| 問題3-4番 | 1 | OK (item) / see **R2-F4** (slot) | 「踏むまでの時間は、腕ではなく、目で決まります」. The item itself is sound; its DOMAIN repeats 20260817_3's 問題3-4番 (both driving) — a cross-test finding, not an item defect | — |
| 問題3-5番 | 3 | OK | 「まず、正面の建物にお寄りいただき」…「積むときから分けておいていただきますと」. Talk lengths 333/332/301/327/312 chars, all inside official p10 251–median 305+ | — |
| 問題4-例 | 2 | OK | 「二人で持てば、すぐ運べますよ」; announced 2 = pre-mark 2 | — |
| 問題4-1番 | 2 | OK | Subordinate reports 謙譲 「席を外しておりました」; the 課長 replies plainly and adds a message. 1 立場逆転, 3 「席」語義取り違え | — |
| 問題4-2番 | 3 | OK (item) / **自動不合格** (pairing, R2-F2) | Key 「携帯の番号でもよろしいですか」 answers the 連絡先 half. F4's re-angle to a home inspection visit actually *improved* distractor 1 (「点検は、明日の午前に…」 is now topic-adjacent yet still ignores the request). But the drawn stimulus is still 記名依頼 — see R2-F2 | Reroll one of the two 記名 stimuli (see R2-F2) |
| 問題4-3番 | 1 | OK | 「お先に失礼します」→「お疲れさま。気をつけて帰ってね。」 2 is the visitor's line, 3 misreads 失礼 as 無礼 | — |
| 問題4-4番 | 1 | OK | 「そんな、まだ形になってないんですけど」 = 遠慮; 3 tells 佐藤 that 佐藤 will be told | — |
| 問題4-5番 | 2 | OK | 「始発に乗れば、十分間に合うよ」; 1 answers about temperature, 3 switches to yesterday | — |
| 問題4-6番 | 1 | OK | 「あ、この箱に入れるんじゃないんですね」; 2 addresses someone who lost a key, 3 reverses roles | — |
| 問題4-7番 | 3 | OK | 「週末までに間に合うなら、それでけっこうです」; 1 says 三日**前**, 2 invents a prior order. F2 moved the 問題14 flyer off 三日後 so this side keeps its drawn string (gate: 問題14 shares no decisive number ✓) | — |
| 問題4-8番 | 1 | OK | 「それが、数字がまだ届かなくて」 = indirect "not going well"; 3 mishears プレゼン as プレゼント | — |
| 問題4-9番 | 2 | OK (item) / **自動不合格** (pairing, R2-F2) | 「どのくらい待てば入れそうですか」; 1 role-reverses, 3 recounts last week | See R2-F2 |
| 問題4-10番 | 3 | OK | 「次に入るのは、いつごろでしょうか」; 1 misreads 切らす as 切る | — |
| 問題4-11番 | 3 | OK (key) / **要修正** (wording, R2-F5) | F5 closed the keigo inversion: the stimulus now reads 「調剤師から**お聞き**ください」, and pool, spec, ledger and script all carry the corrected string (verified: the only `quick_response` diff vs HEAD is this one entry). Remaining defect: **調剤師** is not a Japanese professional title — the licensed one is 薬剤師 — and the scene the section table and `logs/topics.json` assign (動物病院の会計) has no dispensing counter at all | 調剤師 → 薬剤師 in `pools.json`, `聴解スクリプト.txt`, and relabel the scene (病院の会計 / 薬局併設の会計); rebuild the MP3 |
| 問題5-1番 | 3 | OK | F3's rewrite holds. Key 「空き店舗を回る道順を作る」: 「じゃあ、それでいこう」 after 「三人なら出せるって」 clears the one open condition. 1✗「レジが止まっちゃって大変だったよ」/2✗「問題を考える時間がないな」/4✗「住所を書いていただくことになるので、そこはちょっと」 — all three raised then killed. Decision structure (opening proposal → conditional hold → fallbacks die → condition met) differs from 20260817_3's sequential-elimination-then-late-adoption | — |
| 問題5-2番 質問1 | 2 週末集中 | OK | 「月に四回は、正直きついかも」 then 「大きいお皿も作ってみたいですし、二日間の方にします」 | — |
| 問題5-2番 質問2 | 1 一日体験 | OK | 「母には湯のみを作る方を勧めてみる」 + 「年に何回か出てくるだけ」「長い時間は座ってられなくて」「孫はまだ小さいから、絵付けの方は今度に」. Printed/spoken option order is the lecturer's enumeration order and identical for 質問1/質問2 (`jlpt-exam-structure` §問題5-2番); no deciding attribute is printed beside a course name (問題5 prints no options) | — (the errand behind this item is **R2-F3**) |

---

## 3. Findings

| # | item / target | class | evidence | status |
|---|---|---|---|---|
| **R2-F1** | 問題8-45 | **AUTOMATIC** — a second defensible answer | The forced block [2→3→1] leaves card 4 free on either side: key `2→3→1→4` (★=1) and `4→2→3→1` (★=3) are both grammatical (「共働きの私たちは、子どもの急な熱にも祖母が近くに住んでいてくれるおかげで慌てずに済んでいる。」). The 解説's exclusion 「『子どもの急な熱にも』が受け手を失う」 is false — its receiver 「慌てずに済んでいる」 is printed after the blanks. Same invalid-leg class as round 1's F9 (問題8-47), which was repaired at that item only | OPEN — blocking |
| **R2-F2** | 聴解問題4-2番 + 4-9番 | **AUTOMATIC** — same errand twice in one paper (round 1 F4, not cleared) | Both drawn stimuli are still 「こちらに（お）名前を…」 requests, and `pools.json`'s own new `quick_response_keys` assigns both the single errand 「窓口:記名依頼」. `exam-qa-review` Ground rules make "a topic repeated within the paper" automatic and §5 names "two 聴解 items running the same errand"; `exam-blueprint` §"`key` — the errand identity" prescribes `--reroll quick_response`, "however differently the pool spells it". F4's repair changed the **invented setting** (a home visit instead of a counter), which is not what either rule measures — the fix pass's own self-flag was correct | OPEN — blocking |
| **R2-F3** | 聴解問題5-2番 | drawn errand inside its own cooldown (round 1 F12, not cleared) | 「陶芸教室:初心者コースの説明」 now carries the errand key 「カルチャースクール:受講申し込み」, which **20260817_1** (「カルチャースクールの受講手続き」) and **20260817_3** (「カルチャー教室:コース選び」) both drew inside the 11-draw cooldown — I resolved all three through `build_key_index()` myself. Three papers, one errand, two of them consecutive | OPEN |
| **R2-F4** | 聴解問題2-1番, 聴解問題3-4番 | same slot + same domain as the immediately previous paper (round 1 F11, deferred without authority) | 2-1番: 20260817_3 「エレベーターのない四階への引っ越しで見積もりが上がった理由」 → 20260818_1 「ガス開栓の立ち会いを引っ越し前日に父親に頼む」 — both house-move errands, same slot, back to back. 3-4番: 20260817_3 「点検で運転の癖を伝える整備担当の考え」 → 20260818_1 「危ないと予想しながら走ること」 — both driving talks, same slot. **The deferral is not what round 1 asked for**: round 1 filed F11 with status OPEN and its re-review requirement reads "step 5's table rebuilds because F3/F10/**F11** move topics", i.e. it expected the paper to change. Nothing in `qa-report-20260818_1.md` defers the paper half | OPEN |
| **R2-F5** | 聴解問題4-11番 stimulus; `pools.json` | a printed/spoken term that is not a real Japanese title | 「薬の説明は、**調剤師**からお聞きください。」 The licensed profession is **薬剤師**; 調剤 is the act, and 調剤師 appears in no Japanese dictionary and nowhere in `refs/` (grepped all 62 archive extracts — neither 調剤師 nor 薬剤師 occurs). Compounding it, `聴解.md`'s section table and `logs/topics.json` place the scene at 動物病院の会計, where no dispensing window exists. F5 corrected this same sentence's keigo direction and left the noun | OPEN |
| **R2-F6** | `tools/check_consistency.py` `check_spec_errand_rotation` docstring | the check's own documentation now contradicts its own exemption set | The docstring still reads "**NINE** of the twelve papers on disk breach this the day it was written, so they are exempted BY NAME below". `ERRAND_ROTATION_GRANDFATHERED` now holds **ten** ids over **thirteen** papers. Per AGENTS.md §4 each check's docstring *is* its documentation, so this is the doc-says-one-thing/gate-says-another shape — introduced by the same edit that added `20260818_1` | OPEN |
| **R2-F7** | `tools/check_consistency.py` `check_slot_theme_repeat` | `GATE-WRONG` (scope) — measures the tagger at 問題1, and misses half its own founding case | (a) 16 of the 36 hits this check produces over the 13 papers on disk are at 聴解問題1 slots, where 働き方 is **forced** by `choukai-items.md`'s own 問題1 quota (問題1 must be work-assignment ≥3 of 5); 働き方 fills 15 of the ~65 問題1 scored slots. The docstring excludes 問題4 for exactly this reason and then includes 問題1. Three of this paper's five WARN rows are that false positive. (b) The check cannot see the 3-4番 half of the F11 incident it was written for, because the two tags differ (交通 vs 教育) — `logs/topics.json`'s own note admits it: "the tags 差 交通/教育, so check_slot_theme_repeat sees only the 問題2-1番 half". `exam-qa-review` §6.5: a check that would not have caught its own founding case is not evidence | OPEN |
| **R2-F8** | `.agents/exam-blueprint/scripts/sample_items.py` `balanced_position_plan()` | `GATE-WRONG`/`RULE-UNENFORCEABLE` — a ceiling was fitted where a distribution was needed | Measured, 1500 simulated plans vs the 31 sittings in `refs/JLPT_N2_NEW/answer_keys.json` (era-matched by item count). The sampler slices one globally balanced 90-item deck, which makes each section's mode multinomial and therefore **more** clustered than official in 8 sections at once: 問題3 official {1:92 %, 2:8 %} → sampler {1:40 %, 2:60 %}; 問題4_語彙 {2:80, 3:20} → {2:23, 3:77} (**inverted**); 問題7 {3:45, 4:52, 5:3} → {3:3, 4:54, 5:43}; 問題9 {1:64, 2:36} → {1:13, 2:87}; 問題1/2/5/6/8 (n=5) {2:94–97, 3:3–6} → {2:64–66, 3:34–36}; 聴解問題4 {4:61, 5:39} → {4:35, 5:65}. The fix pass documented only the 問題7 row and judged it unfixable because "lowering the ceiling below 5 would reject a real official sitting" — the ceiling is the wrong instrument, not the wrong value | OPEN |
| **R2-F9** | `question-authoring/references/moji-goi.md` §問題6 (owner) + `exam-qa-review` §2b | a binding rule contradicts the archive, and round 1's R6 named only the non-owning file | Both files say a 問題6 wrong sentence must "break exactly ONE thing INSIDE the word's own domain — never leave the domain" (`moji-goi.md` L302, with the 「部屋の電気を解消した」 = banned example). Official does the opposite: 「空には雲が充実している」, 「喫茶店の中は、コーヒーのにおいが充実している」, 「テレビの音量を薄めた」, 「明日、駅のふもとで池田さんと会う」, 「犬の定年は一般的に10歳から15歳の間だ」 — all five verified in `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md`. Applied as written, this paper's 問題6-26 (掃除機/土地) and 問題6-30 (賞金/十キロ) would be automatic fails, and so would that official sitting. Round 1 filed it as R6 against `exam-qa-review` §2b only; the OWNER per §6.5's table is `question-authoring`, so editing one file would create the two-statements-disagree defect AGENTS.md's preamble forbids | OPEN — must be decided, not carried, before the next paper |

### Checked and cleared this round (so it is not re-litigated)

| claim | verdict | evidence |
|---|---|---|
| 問題8 puts ★ in the 3rd blank in all five items — predictable? | **not a finding** | I suspected this and killed it with the source: official 7/2025 問題8 items 43–47 all print `＿＿ ＿＿ ★ ＿＿` with ★ third (read from `refs/JLPT_N2_NEW/16. N2 7-2025/16. N2 07-2025.pdf` p.9 — the `booklet.md` extract drops the underscores, so the PDF is the only witness). `jlpt-exam-structure` §274 and the gate line "問題8 stems offer 4 blanks with ★ third" both encode it correctly |
| F1's ten permuted items desynchronised a 解説, a functional-category line or `answer_positions` | **clean** | All ten (1, 8, 11, 19, 22, 23, 32, 37, 40, 42) re-derived from scratch. Every 解説 lists its options in the printed order (e.g. 19: 「時点を表す副詞 ×4 (今にも/間もなく/たった今/いつしか)」 matches print exactly), every 2×2 grid claim holds against the printed four, and `answer_positions` agrees with all 101 keys (gate, plus my 101/101 blind solve) |
| F6's gloss deletion left a marker/definition mismatch or a stale body reference in 問題13 | **clean** | 問題13 body carries （注1)–（注6) in order on 高経年団地/空室率/分譲/用途変更/共益費/住み継ぐ; the definition block lists exactly those six, same order, each headword present in the body. 改修 now appears bare in both 問題13 (「骨組みと配管は改修で持たせ」) and 問題7-41, consistently. Paper total: **31 in-body markers** (問10=5, 問11=20, 問12=0, 問13=6, 問14=0) — above the 25 floor, inside official 27–61, and 問題12/14 correctly carry zero |
| F10's new 問題9 subject collides with 問題14 (both digital paperwork) | **not a finding, but noted** | 問題9 is about whether a notice is stored as characters or as an image; 問題14 is a municipal online-application flyer (マイナンバーカード, 手数料, 受付番号). No fact, number, condition or decisive detail is shared, and neither item's key depends on anything in the other. It is the closest pair F10's re-subjecting created, and the next blueprint should know that デジタル化 now sits one surface from 行政・手続き |
| any passage, dialogue, 例, stem or option copied from `refs/` or another test | **clean** | Independent 20-char shingle sweep of all passages + script against 62 archive extracts and all 12 other tests. Every archive hit is prescribed boilerplate — the 問題N instructions, the mandated 問題1 narration frame 「〜で男の人と女の人が話しています。女の人は、この後まず何をしますか。」, and the 問題10 lead-in template 「以下は、ある会社が社員に送ったメールである。」 Zero content overlap. No `tests/imported-*` exists, so that half is vacuous — stated, not implied |
| 問題14's 田中さん/佐藤さん repeat the previous two papers' 問題14 names | **not a finding** | The two commonest Japanese surnames, used across the archive; `check_invented_proper_nouns` scopes to invented place/organisation names, correctly. 「ひばり市」 (F8's replacement) occurs in no other paper |
| closing-move variety | **not a finding** | 13 finals read by hand: 意外な観察 2 (10(1), 11(2)); 随筆 2 (10(2), 11(4)); 反論応答 2 (10(3), 11(3)); 説明 2 (問題9, 11(1)); 条件提示 2 (10(4), 13); 主張 2 (10(5), 問題12) — 問題12A and 12B both close on 主張, which the A/B format requires; counted separately that is 3, and the gate's own 13-final template check is green with no skeleton above 2. Keys do not inherit the closing: only 5 of the 20 読解 keys are the "stance" choice (56, 60, 62, 64, 69), under the 6+ threshold |
| 問題7 stem distribution | **pass, and the first paper on disk to pass it** | mean **42.3** (band 36–52) · **3** stems under 34 (need 2) · spread **35** (need ≥25) · shortest 27 (official min 26 in 7/2025). All twelve earlier papers have 0 stems under 34 |

---

## 4. Root-cause table (step 6.5)

Recurrence counted by reading the papers and the pool on disk, not judged.

| finding | code | how many papers / cases show the class | owning file | proposed edit |
|---|---|---|---|---|
| **R2-F1** | `RULE-UNENFORCEABLE` + process | The invalid-leg class is **2 of 5 items in this one paper** (47, caught by round 1; 45, missed) and `make verify-scramble` returns UNDECIDED on 問題8 items in **13 of 13** papers by construction, so the 解説's prose proof is the only evidence everywhere | `question-authoring/references/bunpou.md` §問題8 | Round 1's F9 edit made the *semantic* leg mandatory but left the invalid structural leg available. Replace the template with a two-part procedure: (1) **compute the forced blocks** — for each card, name the card that must immediately precede/follow it — then (2) **enumerate only the orderings the blocks permit** and exclude each survivor by contradiction, never by "connects to nothing". Add the numeric guard that catches this exact shape: *a card that modifies the predicate printed AFTER the blanks can be fronted, so it is never excluded by "loses its receiver"* — if such a card exists and the rest of the set forms one contiguous block, the item has two ★ answers and must be re-cut. This is string-decidable enough to gate: FAIL any 問題8 解説 whose last-slot proof uses a "受け手を失う/結べない" leg on a card whose particle is に/にも/でも/は/も and whose predicate lies outside the blanks. **Run against both founding cases before committing** — it must fire on 問題8-45's current 解説 and on 20260818_1's pre-fix 問題8-47 |
| **R2-F2** | `RULE-IGNORED` (process) + `RULE-MISSING` (tooling) | The errand pair occurs in **1 of 13** papers; but the *repair* gap is general — `--reroll <category>` is the only redraw available, and for `quick_response` it replaces all **11** stimuli and forces a whole-問題4 re-author plus an MP3 rebuild | `AGENTS.md` §0 (process); `.agents/exam-blueprint/scripts/sample_items.py` (tooling) | The rule was specific and available and the fix pass substituted a cheaper edit, which is `RULE-IGNORED` — nothing to change in the rule. What *invited* it is the tooling: add `--reroll-one <category>:<index>`, drawing a single replacement under the same `taken`/cooldown/cross-key exclusions and recording it in spec + ledger with `"origin": "rerolled"` and a note (the shape `check_draw_provenance()` already requires). That turns "re-author 11 items" into "re-author 1" and removes the incentive to re-angle a setting instead of redrawing an errand. Then the paper repair is one stimulus + three replies + MP3 |
| **R2-F3** | `PIPELINE-GAP` | **10 of 13** papers now sit in `ERRAND_ROTATION_GRANDFATHERED`, i.e. the class is the norm, not the exception; the errand 「カルチャースクール:受講申し込み」 alone was drawn by 3 papers inside one 11-draw window | `.agents/exam-blueprint/references/pools.json`; `exam-blueprint/SKILL.md` §"Rotation model" | Keying the pool retroactively is right and I verified it works. What is missing is the ordering rule: **key the whole cluster before the draw, never after it** — the pool WARN 「errand-key clusters cost 27 entries of effective pool depth (23 clusters)」 shows 23 clusters exist and only some are keyed, so the next paper can still draw an unkeyed third spelling. Add to `exam-blueprint`: a blueprint stage may not run while any `listening_scenarios`/`quick_response` cluster is unkeyed, and add a gate check that FAILs on two pool entries whose text shares ≥2 institution/errand tokens while only one carries a `key`. For this paper, `--reroll-one listening_scenarios:16` (per R2-F2's tooling) re-draws 問題5-2番's scenario without touching the other 20 |
| **R2-F4** | `RULE-IGNORED` (deferral not authorised) | Slot-domain repeats are visible in `logs/topics.json` across **20260817_2 → 3 → 20260818_1** in ≥3 slots | nothing to change in the rule text — `jlpt-test-generation` §"One topic, one surface" is explicit and round 1 converted it to a procedure | Repair the paper: re-angle 聴解問題2-1番 off the house move (the 引っ越し frame is the author's invention around the drawn 「ガス会社:開栓の予約」 — an 開栓 at a newly-built flat, a returning-from-abroad tenant, or a seasonal re-opening all keep the drawn errand) and re-angle 問題3-4番 off driving (its scenario 「自動車学校:学科」 is drawn, so re-slot it: swap 問題3-4番 with 問題3-2番's talk so the driving item does not land in 20260817_3's driving slot). Both are cheap; neither needs a redraw. Then update `logs/topics.json`'s `surfaces`/`themes`/`shapes`/`closing_moves`/`notes` together |
| **R2-F6** | `GATE-WRONG` (documentation) | 1 check, introduced by the 2026-08-19 fix pass | `tools/check_consistency.py` | Correct the count and, better, stop asserting the criterion in prose: have the check itself prove each exemption. Store the grandfather set as `{id: draw_timestamp_of_the_key}` and assert at run time that the paper's `generated_at` precedes the moment the breaching `key` entered `pools.json` (`git log -1 --format=%ad -S'"key": "…"'`, or a `keys_added_at` field in `pools.json`). An exemption that cannot prove its own criterion is an exemption by assertion. **My independent verification of the criterion for `20260818_1`, which the amendment should not have needed prose for:** `git show HEAD:.agents/exam-blueprint/references/pools.json` has 28 keyed `listening_scenarios` entries and 「陶芸教室:初心者コースの説明」 is **not** one of them; the worktree has 29 and it is; `pools.json` mtime 16:31:47 > the draw's `generated_at` 11:29:18. The claim is TRUE |
| **R2-F7** | `GATE-WRONG` (scope, both directions) | 16 of 36 hits over 13 papers are structurally-forced 問題1 false positives; the check catches 1 of the 2 halves of its own founding incident | `tools/check_consistency.py` `check_slot_theme_repeat` | (1) Narrow the slot pattern from `聴解問題[1235]-\d+番` to `聴解問題[235]-\d+番`, for the reason the docstring already gives for excluding 問題4: `choukai-items.md` §"Section item mix" makes 働き方 the mandated majority tag in 問題1, so a repeat there measures the quota, not the paper. Print the measurement when you change it: on the 13 papers the hit count moves 36 → 20 and this paper's 5 rows → 2. (2) Add the half it misses — compare each slot's **domain**, not only its tag, by intersecting the slot's `surfaces` string against the same slot two papers back on a content-word basis (運転/引っ越し/検診…), or state plainly in the docstring that the tag test cannot see a domain repeat across differing tags and that the reviewer owns that half. Right now the docstring claims the founding case and silently delivers half of it |
| **R2-F8** | `GATE-WRONG` (a ceiling standing in for a distribution) | 8 of 19 sections measurably skewed vs 31 official sittings; **13 of 13** papers were drawn under this plan generator | `.agents/exam-blueprint/scripts/sample_items.py`, `exam-blueprint/SKILL.md` §"Answer positions" | Keep `MAX_SECTION_MODE` as the hard ceiling (it correctly refuses to reject a real sitting) and add rejection sampling to the *target*: measure each section's official mode distribution once from `refs/JLPT_N2_NEW/answer_keys.json` (I have it: 問題1/2/6 {2:.97,3:.03}, 問題3 {1:.92,2:.08}, 問題4 {2:.80,3:.20}, 問題5/8 {2:.94,3:.06}, 問題7 {3:.45,4:.52,5:.03}, 問題9 {1:.64,2:.36}, 問題10 {2:.77,3:.23}, 問題11 {2:.10,3:.80,4:.10}, 問題12 {1:.87,2:.13}, 問題13 {1:.68,2:.32}, 問題14 {1:.71,2:.29}, 聴解1 {2:.71,3:.26,4:.03}, 聴解2 {2:.42,3:.42,4:.15}, 聴解3 {2:.83,3:.13,4:.03}, 聴解4 {4:.61,5:.39}, 聴解5 {1:.45,2:.55}) and accept a candidate plan with probability proportional to ∏ P(observed mode) — or, equivalently and more cheaply, draw each section's mode from that table first and shuffle a deck that realises it while keeping the global 22/23 band. This paper needs no change: its 問題7 mode is 4 (official's modal value) and every slice is inside the ceiling. **Run the new predicate over all 13 papers and state which ids move** before committing |
| **R2-F9** | `RULE-WRONG` | official 問題6 crosses the target's domain in ≥5 items of one sitting (12/2024), all quoted above; the paper's own 問題6 has 4 such options across items 26 and 30 | `question-authoring/references/moji-goi.md` §問題6 (**owner**), then `exam-qa-review` §2b as the restatement | Rewrite the owner's step (2) from "break exactly ONE thing INSIDE the word's own domain — never leave the domain" to: "the wrong sentence must be a **misuse a learner would plausibly commit**; a domain shift is official's main device (「テレビの音量を薄めた」), so what fails is a sentence no learner would produce, and what is still banned is a second ATTESTED collocation (「契約を解消」)". Keep the 解消/部屋の電気 row but relabel it from *banned* to *acceptable when the misuse is one a learner makes*. Then make `exam-qa-review` §2b point at the owner instead of restating it. The fix pass's refusal to weaken the rule unilaterally is right (see §5.6); what is not acceptable is leaving it open across another generation run, because §6.5 makes an open `RULE-*` finding a blocker |
| **R2-F5** | `RULE-MISSING` (pool content) | 1 of 200 `quick_response` entries; but the class — a pool sentence naming a non-existent institution/title — has now produced two defects on this one entry (F5's keigo direction, R2-F5's noun) | `.agents/exam-blueprint/references/pools.json`; `exam-blueprint/SKILL.md` §"A `quick_response` entry is a SENTENCE" | The in-place-correction path that F5 established is right and I verified it end to end. Add to it: **when a pool sentence is corrected, re-read the WHOLE sentence against the world, not only the reported defect** — F5 changed 伺ってください→お聞きください inside a sentence whose subject noun is not a real title. Gateable cheaply: keep a short deny-list of near-miss titles/institutions (調剤師→薬剤師, 診療師, 看護士→看護師) and FAIL any `quick_response`/scenario string containing one |

**Effect on the loop.** R2-F1 through R2-F5 block this paper. R2-F6 through R2-F9 block the **next** generation run under §6.5 — R2-F8 in particular, because every future paper's answer-position plan is drawn from the skewed generator, and R2-F9 because the next 問題6 author cannot satisfy both the owner's rule and the archive.

---

## 5. Rulings the coordinator asked for

### 5.1 Is F4 sufficient? (both stimuli still ask the listener to write their name)

**No.** The fix pass's own self-flag was correct. What the rules measure is the **errand**, not the setting: `exam-blueprint` §"`key` — the errand identity" says "one paper cannot run the same 即時応答 errand twice **however differently the pool spells it**", and `pools.json` — edited by that same fix pass — now assigns both drawn stimuli the single key 「窓口:記名依頼」. Re-angling 問題4-2番's invented scene onto a home visit changes nothing either rule reads; it is an improvement to the item (distractor 1 became topic-adjacent) and not a repair of the pairing. Filed as **R2-F2**, automatic. The honest obstacle is tooling, not judgment — `--reroll quick_response` replaces all 11 stimuli — so R2-F2's root-cause row proposes the single-entry reroll that makes the sanctioned repair affordable.

### 5.2 Is F1's documented residual (問題7 mode 3/4/5 at 3/55/42 % vs official 45/52/3 %) a finding?

**Yes — against `sample_items.py`, not against this paper**, and it is larger than documented. I reproduced the claim independently (1500 plans: 3.8 / 53.3 / 42.9 %) and then measured every section against all 31 sittings. Eight sections are skewed the same way, and 問題4_語彙 is worse than 問題7 — official {2:80 %, 3:20 %} against the sampler's {2:23 %, 3:77 %}, an inversion the fix pass did not report. The cause is structural: one globally balanced 90-item deck, shuffled and sliced, makes each section's mode **multinomial**, whereas official examiners balance *within* each 大問 (mode 2-of-5 in 97 % of sittings is exactly "as even as 5 items over 4 positions can be"). The 2026-08-19 change therefore over-corrected an earlier "too smooth per-section" complaint into "more clustered than official".

The fix pass's objection — "lowering the ceiling below 5 would reject a real official sitting" — is **correct and beside the point**: the ceiling should stay at 5. The missing instrument is a distribution, applied by rejection sampling, which leaves mode 5 reachable at its official 3 % rate. See **R2-F8** for the measured table. This paper is unaffected: its 問題7 mode is 4, official's modal value, and every slice is inside the ceiling.

### 5.3 Is the amendment to the F12 grandfather comment legitimate or self-serving?

**Legitimate in substance, defective in bookkeeping — and it should not have needed prose at all.**

The factual claim is true and I verified it without trusting the comment: at `HEAD` (327912e, 2026-08-19 15:18:21) `pools.json` carries 28 keyed `listening_scenarios` entries and 「陶芸教室:初心者コースの説明」 is not among them; the working tree carries 29 and it is; the file's mtime is 16:31:47 and the draw's `generated_at` is 11:29:18. So the key genuinely post-dates the draw, `draw()`'s cross-key exclusion genuinely could not have refused the pick, and the criterion the amendment states ("the draw predates the key") holds for `20260818_1` and for all nine ids already in the set (every one drawn before the `key` field existed — the earliest ledger entry after it is this paper's).

It also replaced a blanket prohibition with a **checkable** criterion, which is the better direction: "never add one to quiet a new paper" gives a later maintainer no way to decide a genuine retroactive breach.

What is wrong with it:
1. **The docstring above it still says "NINE of the twelve papers"** while the set holds ten of thirteen. Filed as **R2-F6**. A rule amendment that leaves its own check's documentation contradicting the code is the exact shape this repo keeps getting bitten by, and it was introduced by the amendment itself.
2. **The criterion is asserted in a comment rather than proven by the check.** That is what makes "legitimate vs self-serving" a matter of trust instead of measurement. R2-F6's proposed edit makes each exemption prove its own timestamp, so no future pass can add an id by writing a sentence.

So: not self-serving — but only because the fact happens to be true, which is not the same as the amendment being safe.

### 5.4 Is the F11 deferral what round 1 asked for?

**No.** `qa/qa-report-20260818_1.md` lists F11 with status **OPEN**, against two named items (聴解問題3-4番, 聴解問題2-1番), and its closing re-review requirement reads: *"step 5's table rebuilds because F3/F10/**F11** move topics."* Round 1 therefore expected the paper's topics to move. Its root-cause row proposes a rule + gate *in addition*, as every row does; nothing in the report defers the paper half, and §7's skip list — the place round 1 recorded what it was not doing — does not mention F11. Filed as **R2-F4**. The repair is cheap and needs no redraw (both scenarios can be re-angled or re-slotted, see R2-F4's row).

### 5.5 The three WARNs that name this paper

| WARN | ruling |
|---|---|
| `no drawn errand repeats inside its own cooldown window` — 「陶芸教室:初心者コースの説明」 = errand 「カルチャースクール:受講申し込み」 (20260817_1, 11-draw cooldown) | **Real, not a false positive.** I resolved the errand key through `build_key_index()` myself: **20260817_1** and **20260817_3** both drew this errand inside the window. The gate's by-name exemption is internally justified (§5.3) but a gate exemption cannot clear a QA finding — `exam-qa-review` ground rules make "an item redrawn from a test inside the rotation cooldown" a defect and prescribe the reroll. **R2-F3, open.** Note the WARN names only 20260817_1 (first match in the window) while the grandfather comment names only 20260817_3 — both are true, neither is complete |
| `no 聴解 slot repeats its own theme in the previous 2 papers (5 slots)` | **Split.** 3 of 5 are false positives: 聴解問題1-1番=働き方 (vs both papers) and 聴解問題1-3番=働き方 (vs 20260817_2) are forced by `choukai-items.md`'s 問題1 work-assignment quota, and the three subjects are genuinely unrelated (倉庫の棚卸し / 資料印刷 / 試作品借用 / 受付欠員の電話). 聴解問題2-2番=教育 vs 20260817_2's 学習法講演 is two papers apart with disjoint subjects (進路選択 vs 勉強法) and different question types — **accept**. 聴解問題2-1番=住まい vs 20260817_3's 引っ越し見積もり is **a real repeat**: consecutive papers, same slot, same life event. That row is **R2-F4**; the false-positive pattern is **R2-F7** |
| `no two drawn 問題4 stimuli run the same errand` — 「窓口:記名依頼」 ×2 | **Real. R2-F2, automatic.** See §5.1 |

Every other WARN in `make check`'s 127 lines names one of the twelve earlier papers and is outside this review's scope; two are pool-wide and I read them: `pools.json errand-key clusters cost 27 entries of effective pool depth (23 clusters)` — the direct consequence of the F4/F12 keying, and evidence for R2-F3's "key the whole cluster before the draw"; and `pools.json entries needing a 表外 glyph (14 across 5 categories)` — none of the 14 is drawn by this paper (gate: "every 問題1/2 printed kanji is 常用" ✓).

### 5.6 Was rejecting R6 legitimate?

**Yes, as a matter of process — and it must not stay rejected.**

Round 1 declined to edit `exam-qa-review` §2b itself for a stated reason (§7 skip 4: "it *weakens* an existing rule and a weakening should be read by a human before it lands"), and §6.5's Boundaries clause licenses the reviewer to *add* a defect class to that file, not to remove one. The fix pass's rejection therefore matches both round 1's own reasoning and the skill's boundary rule, and §6.5's requirement is satisfied by an explicit rejection with a reason. I agree.

Two things the rejection did not settle, which I am filing as **R2-F9**:
1. **It was filed against the wrong file.** The rule's owner is `question-authoring/references/moji-goi.md` §問題6, which carries the identical sentence and its own banned example. Editing only `exam-qa-review` §2b would leave the owner saying the opposite — the disagreement AGENTS.md's preamble calls "a defect to fix, not to route around".
2. **It cannot be carried indefinitely.** §6.5 makes an open `RULE-*` finding a blocker on the next generation run, and this one is live: applied as written it would fail this paper's 問題6-26 and 問題6-30, and it would fail official 12/2024. I verified all five of round 1's counterexamples directly in `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md`. Someone has to decide it before the next 問題6 is authored; until then I have marked those items OK against the archive and said so in the row.

---

## 6. Coverage

Steps 0–6 all ran, on all 101 items, no sampling. Files read in full: `tests/20260818_1/{言語知識・読解.md, 聴解.md, 聴解スクリプト.txt, test_spec.json, 聴解_チャプター.json}`, `qa/20260818_1/keyless.md`, `logs/{ledger.json, topics.json, adjunct_staging.json}`, `.agents/exam-qa-review/SKILL.md`, `AGENTS.md`/`CLAUDE.md`, plus the relevant sections of `check_consistency.py`, `sample_items.py`, `moji-goi.md`, `question-authoring/SKILL.md`, `exam-blueprint/SKILL.md`, `jlpt-exam-structure/SKILL.md`, `qa/qa-report-20260818_1.md` (round 1), and for calibration `refs/JLPT_N2_NEW/answer_keys.json`, all 62 `booklet.md`/`script.md` extracts, and pages 9 and 1–2 of the 7/2025 PDF.

### 6.1 Topic table (step 5) — re-tagged from the SHIPPED surfaces

Headline sets, built by me from the shipped content:

| slot | 20260818_1 | 20260817_3 (previous) | 20260817_2 (two back) |
|---|---|---|---|
| 問題9 | デジタル化 (文字か画像か) | 消費・経済 | 科学・技術 |
| 問題12 | 交通 (通勤時間の使い方) | 環境 | 旅行・観光 |
| 問題13 | 住まい (団地再生の余白) | 医療・福祉 | 働き方 |
| 問題14 | 行政・手続き (証明書オンライン申請) | スポーツ・余暇 | 教育 |
| 聴解問題5-1番 | 地域活性化 (スタンプラリー) | 人間関係 | 食 |
| 聴解問題5-2番 | 教育 (陶芸教室のコース選び) | 防災 | 子育て・家族 |

- vs the previous paper: intersection **∅** ✓ (rule 4's zero-tolerance clause).
- vs the paper two back: intersection **{教育}** = exactly **one** ✓ (rule 4's cap). This is where round 1's F10 landed and F10's re-subjecting of 問題9 (科学・技術 → デジタル化) closes it — verified from the shipped cloze, not from the label.
- 13 読解 surfaces carry **13 distinct themes** ✓; no 読解 subject occurs twice in the paper.
- 問題12's A/B theme (交通) differs from both predecessors' (環境, 旅行・観光) ✓.
- In-paper 聴解: **one repeat**, 問題4-2番/4-9番 (R2-F2). Two adjacent-but-distinct pairs cleared: 地域活性化 at 問題10(2)/聴解5-1番 and 教育 at 問題11(1)/聴解5-2番.
- 問題14 shares no decisive number, condition or rule with any 聴解 item ✓ (gate green after F2; I re-read 問70/71 against 聴解問題4-7番's 「三日後」 and the flyer's 「申請の翌日以降に」 — disjoint).
- Cross-test 聴解 slots: **two real repeats** (R2-F4) and three tag-only false positives (R2-F7).

### 6.2 Provenance (step 6) — what I could and could not establish

**Item match audit — clean, by content, item by item.** All 11 drawn categories map onto the printed paper with no substitution: `kanji_reading`→1–5, `orthography`→6–10, `word_formation`→11–13 (再〜/深〜/〜量), `context_words`→14–20, `paraphrase`→21–25, `usage`→26–30, `grammar_p7`→31–42 **in draw order**, `grammar_p8`→43–47, `quick_response`→問題4 1番–11番 **in draw order**, `listening_scenarios` 21 entries→the 21 聴解 slots (6+7+6+2), `reading_topics` 12 entries→the 12 読解 surfaces. `answer_positions` matches all 101 keys (gate, plus my 101/101 blind solve). The ledger row agrees with the spec field for field (gate ✓) and — checked against git — differs from the version committed at `HEAD` **only** in the F5-corrected `quick_response` string, so the ledger has not been hand-edited beyond the documented pool repair.

**Seed replay — I refute round 1's stronger claim, and confirm the weaker one.** I replayed the base seed `9670904` in process (no writes) against four reconstructions:

| reconstruction | categories reproduced |
|---|---|
| `HEAD` pools + the 12 prior ledger entries | **4 of 11** — kanji_reading, grammar_p7, grammar_p8, reading_topics |
| same, with `logs/adjunct_staging.json` applied | 4 of 11 |
| worktree pools + 12 prior entries | 3 of 11 |
| any variant with this paper's own ledger entry in the recency window | 0 of 11 |

Round 1 reported 6 of 11 at its own point in time; I get 4, and the difference is fully explained — `pools.json` has been edited **twice more since** (F5's `quick_response` string, F12's `listening_scenarios` key; I diffed HEAD against the worktree and those are the *only* two changes, in only those two categories). `draw()` consumes a state-dependent number of RNG values, so an edit in any earlier category desynchronises every later one. **So: the recovery is confirmed by content and refuted as a replay.** The spec on disk is the draw the ledger records and the paper prints; but nobody can reproduce it from the recorded seed today, and that is R7's founding defect, not a fault in the recovery.

`pools_sha` — **absent from all 13 specs and all 13 ledger entries**, this paper included. `check_pools_sha_replayability` therefore **skips**, correctly ("an unstamped spec is old, not wrong"), which means the R7 repair is inert on everything on disk and begins to bind only with the next paper. Stated rather than implied: the gate line that would have made this section a lookup instead of an investigation has never yet run on anything.

**One process note.** `logs/ledger.json`'s row for `20260818_1` is already **committed** at `HEAD` (in commit 327912e, "20260817_3: new N2 mock …"), while `tests/20260818_1/` is untracked. AGENTS.md §2 says to commit a new test and the updated ledger together; here the ledger row shipped one commit ahead of its test. Harmless as it stands, worth not repeating.

### 6.3 Artifact freshness

| artifact | source | verdict |
|---|---|---|
| `聴解.mp3` (16:27:07) | `聴解スクリプト.txt` (16:10:17) | newer ✓, and `聴解_チャプター.json` records `script_sha 2fbe5bf222df` = the shipped script's sha1[:12] (gate ✓) — the MP3 was rendered from the text I reviewed, after F3/F4/F5/F13 |
| `聴解.mp3` pacing | pacing config | `pacing_sha d241e428f28f` current ✓ |
| `言語知識・読解.html` (16:25:13) | `.md` (16:22:14) | newer ✓, built HTML matches the Markdown it stamps (gate ✓) |
| `聴解.html` (16:25:14) | `.md` (16:10:59) | newer ✓ |
| `解答.html` (16:28:53) | both `.md` | newer ✓, is the server build, carries no localStorage store (gate ✓) |
| `詳細解説.json` | — | absent; `check_model_answer_option_sync` **skips**. `make model-answer` has not run, which is correct — AGENTS.md §5 makes it the final step after QA passes |

Source mtimes and sha1s were re-checked at the end of the review and had **not** moved (`74377463d2e2` / `402cb515898a` / `2fbe5bf222df`), so no fixing pass edited underneath me and every row above is a claim about the bytes I read.

### 6.4 `make check`

`All checks passed (27 skipped), 127 warning(s)`, exit 0, full output read line by line (2284 lines). Three WARNs name this paper and each is ruled on in §5.5; two are pool-wide and ruled on there too. Of the 27 skips, the two that touch this paper are `詳細解説.json options match the booklet` (no such file yet, correct) and `recorded pools_sha matches pools.json` (no stamped spec exists, §6.2).

---

## 7. Skips and things I could not verify

1. **`聴解.mp3` is UNLISTENED.** I have no audio playback in this environment. Two QA rounds have now passed on this paper without anyone hearing it. What I verified is a different thing and does not substitute: the file post-dates the script, `聴解_チャプター.json`'s `script_sha` is byte-identical to the shipped `聴解スクリプト.txt`, its chapter marks are strictly increasing, and narration↔voice consistency is checked **from the script and `SPEAKER_MAP`** (gate: "聴解 narration gender matches SPEAKER_MAP's voice", "item speaker pairs cast distinguishable voices"). **Rendered pronunciation, actual voice assignment, pacing and answer-pause lengths are unverified by me and by round 1.** If R2-F5 is applied, the MP3 must be rebuilt anyway — that is the moment to have a person listen to it once end to end.
2. **The N2 vocabulary volumes were not opened.** `refs/Shinkanzen/*` and `refs/Soumatome/*` are scanned images with no text layer, and page-reading five volumes for ~30 headwords was not affordable here. I used the substitute `exam-qa-review` §2b permits — the 31-sitting archive — and judged every 問題1–6 key against it plus the 常用漢字 usage split for 問題2-7. The keys I consider least corroborated are **彼岸** (問題1-3, unattested either way in the archive; the stem 「墓参り」 is what fixes it) and **超一流** (問題4-15, a transparent 超+一流 formation rather than a headword). Neither is off-band in my judgment, and no key struck me as N1-hard or N3-easy; the option SETS are N2 discriminations throughout, not four N4 adverbs.
3. **Imported-paper comparison is vacuous.** No `tests/imported-*` directory exists, so "check against imported papers directly" had nothing to compare against. The `refs/` half ran in full (62 extracts, 20-char shingles).
4. **I applied no fix and edited no skill.** Per §6.5's boundary rule the reviewer proposes; and the one file a reviewer may edit is `exam-qa-review/SKILL.md`, where the only change I would make is R2-F9 — which *weakens* a rule, so like round 1 I have written it into the root-cause table instead of editing the file. No new defect class needed adding: R2-F1 is already covered by §3's 問題8 bullet ("try each option in each other slot") and R2-F2/F3/F4 by the ground rules and §5.
5. **R2-F8's proposed rejection sampler is specified but not implemented or benchmarked.** I measured the official distributions and the sampler's, and named the mechanism; I did not check how many reshuffles the acceptance test would need for the 問題11 row (official {2:10 %, 3:80 %, 4:10 %} is tight), so the 2000-attempt loop bound may need raising.
6. **`make check` ran in full and every line was read** (2284 lines, 127 WARNs). Nothing was skimmed. I deliberately did **not** read the WARN text naming this paper until Section 0 was on disk, because several WARN messages in this gate print keyed option numbers.
7. **Grammaticality judgment in R2-F1.** The finding rests on my reading that a fronted 「〜にも」 adverbial above a subordinate 「〜おかげで」 clause is natural Japanese. I give the parallel (「彼は突然の雨にも傘を持っていたおかげで濡れずに済んだ」) and note that `make verify-scramble` leaves ★∈{1,3,4} open rather than contradicting me, but no corpus check settles it and a native reader should confirm before the re-cut is applied. Per the ground rule that doubt resolves **against** the item, it is filed as automatic.

---

## 8. Verdict

Steps 0–6 ran on all 101 items. The key half is sound: **the blind solve agreed with all 101 keys**, every 解説 names the printed options in the printed order after F1's ten permutations, F2/F6/F7/F9/F13 close cleanly, and 問題7's stem distribution passes all three of `bunpou.md`'s numbers — the first paper on disk to do so. Nothing is mis-keyed.

What blocks it is one new item defect and three deferred cross-surface repeats:

- **R2-F1** (automatic) — 問題8-45 has two grammatical orderings; the 解説's exclusion leg is the same invalid one round 1 caught at 問題8-47 and the fix was applied to that item only.
- **R2-F2** (automatic) — 問題4-2番 and 4-9番 still run the drawn errand 「窓口:記名依頼」 twice; re-angling the invented setting is not what the rule measures.
- **R2-F3** — 聴解問題5-2番's errand was drawn by 20260817_1 and 20260817_3 inside its own cooldown.
- **R2-F4** — two 聴解 slot-domain repeats against the immediately previous paper, deferred without round 1 having asked for that.
- **R2-F5** — 調剤師 is not a real professional title.
- **R2-F6 – R2-F9** are generator/gate findings that block the **next** run, not this paper.

**QA: FAIL (9 findings, 2 automatic)**

---

## 9. Fix-pass disposition (appended by the round-2 fix pass, 2026-08-19)

Appended, not edited: every line above is the reviewer's and stays as written.
This section is the work list's closing record — what was APPLIED, what was
REJECTED/REFUTED and why, and what is still open with the reason. Under §6.5 an
open `RULE-*`/`GATE-*`/`PIPELINE-GAP` row blocks the next generation run until it
is applied or explicitly rejected; this is that record.

| finding | disposition | where |
|---|---|---|
| **R2-F1** 問題8-45 two orderings | **APPLIED (paper + owner + tool).** Re-cut so the item has no frontable card: the adverbial moved into the stem (「共働きの私たちは、子どもが急に熱を出したときも＿＿ ＿＿ ★ ＿＿。」) and the predicate became the fourth card; blanks now end the sentence, which is official practice (12/2025 問題8-44/46). Key stays option 1, so `answer_positions` did not move. **All five proofs re-read**: 44 and 43 were leaning on the same two invalid legs and were rewritten, 46 was upgraded to the block form, 47 keeps its round-1 semantic leg with the 連体修飾 target generalised | `tests/20260818_1/言語知識・読解.md`; `bunpou.md` §"The uniqueness proof is a TWO-PART procedure"; `tools/verify_scramble.py` `illegal_legs()` — FIRES on all four founding strings (45, pre-fix 47, pre-fix 44, pre-fix 43) and stays silent on 46's genuinely structural legs; re-run over all 13 papers, **no id moves** |
| **R2-F2** 問題4-2番/4-9番 one errand | **APPLIED (paper + tooling).** `--reroll-one <cat>:<index>` implemented; 問題4-9番's stimulus REDRAWN (seed 1514814): 「キャンセル待ちの方は、こちらに名前をお書きください。」 → 「雨天のため、屋外イベントは中止です。」 The item was re-authored (科学館の受付) keeping key position 2, the question-shaped key and its 立場の逆転／時制の誤り pair, so 問題4's shape counts and the 11-distinct-combination argument are unchanged. `20260818_1` is no longer grandfathered — `check_spec_quick_response_errand_pair` now passes it as a CHECK, and the exemption set is empty | `sample_items.py` `--reroll-one`; `exam-blueprint/SKILL.md`; `tests/20260818_1/{test_spec.json,聴解スクリプト.txt,聴解.md}`; `logs/{ledger.json,topics.json}`; MP3 rebuilt (`script_sha 8288a751e3c4`) |
| **R2-F3** 問題5-2番 errand inside its cooldown | **OPEN — paper half not applied, stated rather than implied.** The redraw is now affordable (`--reroll-one listening_scenarios:16`) but re-authoring 聴解問題5-2番 is a whole 統合理解 item — enumerating talk, two-person evaluation, four spoken labels, two keys, 構成表 structure note, MP3 — i.e. re-authoring beyond this finding's scope, so it was not opened. The gate exemption now PROVES its own criterion instead of asserting it (below), and the ordering rule is the generator half | exemption + proof: `tools/check_consistency.py` `ERRAND_ROTATION_GRANDFATHERED` / `prove_grandfather()` |
| **R2-F4** two slot-domain repeats | **APPLIED for 問題2-1番; OPEN for 問題3-4番.** 2-1番: the house-move frame is gone — same drawn errand (ガス会社:開栓の予約), but the caller is a tenant returning after a year abroad, the reason she cannot attend the day before is that she is still overseas, and the printed options dropped 引っ越し. Theme stays 住まい because that is what the errand is (re-tagging to dodge a WARN is forbidden), so the tag-level WARN remains and is now a genuine false positive: 帰国後の開栓立ち会い and 引っ越しの見積もり額 share no subject. 3-4番: its scenario 自動車学校:学科 is DRAWN, so the only repairs are a re-slot (swap with 問題3-2番, which permutes 聴解_問題3's positions) or a reroll; out of this pass's scope | `tests/20260818_1/{聴解スクリプト.txt,聴解.md}`, `logs/topics.json` |
| **R2-F5** 調剤師 | **APPLIED (pool + paper + gate).** 調剤師 → 薬剤師 in `pools.json`, with the spec, the ledger row and the script following the corrected entry; the invented scene moved from 動物病院の会計 to a hospital cashier with an in-house dispensary. New `check_pool_nonexistent_titles()` FAILs a pool string naming a title that does not exist — verified to fire on the pre-fix string and pass on the corrected one | `pools.json`; `exam-blueprint/SKILL.md` §"A `quick_response` entry is a SENTENCE"; `tools/check_consistency.py` |
| **R2-F6** grandfather docstring | **APPLIED.** The stale count is gone (the docstring no longer restates one — read the set), and the criterion is DATA plus a run-time assertion: each exempt id maps to when the key that breaches it entered `pools.json`, and `prove_grandfather()` asserts that the paper's own `generated_at` precedes it AND that it still breaches, so a stale exemption FAILs instead of sitting forever. Printed per id, e.g. `20260818_1: errand-rotation exemption proves its own criterion (drawn 2026-08-19 11:29:18 < keyed 2026-08-19 16:31:47, 1 breach(es) still measured)` | `tools/check_consistency.py` |
| **R2-F7** `check_slot_theme_repeat` scope | **APPLIED (both halves, one of them as a documented limit).** Slot pattern narrowed 問題1/2/3/5 → 問題2/3/5, for the reason the docstring already gave for excluding 問題4: `choukai-items.md`'s 問題1 quota mandates work-assignment in ≥3 of 6 items, so 働き方 there measures the rule. Measured over the 13 papers: hits **36 → 20**, `20260818_1` **5 → 2**, and two papers' WARN lines flip to ok (20260810_2, 20260817_3). The 問題3-4番 half it misses is now stated in the docstring as a limit the reviewer owns, with the reason a content-word intersection was rejected: the two founding surfaces share no token either, so it would have missed its own case while firing on unrelated pairs | `tools/check_consistency.py` |
| **R2-F8** ceiling vs distribution | **APPLIED (generator, next paper only).** `SECTION_MODE_DIST` added — the era-matched per-大問 mode-count distribution, stored as sitting COUNTS — and `section_row()` draws each section's mode from it, then rejection-samples i.i.d. rows until one realises it; the plan is redrawn until the global band and the cross-seam run cap still hold. Re-measured independently from `refs/JLPT_N2_NEW/answer_keys.json` (reproducing round 2's table exactly) and simulated over 400 seeds: all nineteen sections now match official within noise (問題4_語彙 24 %→80 % at mode 2; 問題7 3/4/5 = 48/48/4 vs official 45/52/3; 問題9 10 %→64 % at mode 1). The ceiling stays at 5. This paper's positions are untouched and no gate line moves | `sample_items.py`; `exam-blueprint/SKILL.md` §"Answer positions" |
| **R2-F9** (= round 1 **R6**) 問題6 domain rule | **REFUTED, and recorded as refuted so it stops blocking the next run and nobody re-files it.** The rule "each wrong 問題6 sentence must break exactly ONE thing INSIDE the word's own domain — never leave the domain" is wrong as written: official 12/2024's 問題6 leaves the target's domain in **all five items** — 26 薄める 「コースのレベルを薄めた」「エアコンをつけて温度を薄めた」「テレビの音量を薄めた」 (all three wrong options), 27 充実 「空には雲が充実している」「喫茶店の中は、コーヒーのにおいが充実している」, 29 ふもと 「駅のふもとで池田さんと会う」「ドアのふもとに猫がいて」, 30 定年 「犬の定年は…10歳から15歳」「この乗り物は…10歳が定年」 — every one re-verified verbatim in `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md` L96–120 by this pass, not taken from the report. Applied as written it fails that sitting and this paper's own 問題6-26/30. The OWNER now carries the refutation, the evidence table and the route history (R6 → R2-F9 → refuted), and `exam-qa-review` §2b points at the owner instead of restating it. What still fails a wrong sentence: a sentence no learner would produce, a second attested collocation, or a word-form tell | `question-authoring/references/moji-goi.md` §問題6; `exam-qa-review/SKILL.md` §2b |

**Gate after the pass:** `make check` → `All checks passed (26 skipped), 125
warning(s)`, exit 0 (was 27 skipped / 127 warnings: −2 from R2-F7's narrowing,
−1 from the 問題4 errand pair becoming a pass, +1 because `pools_sha` now RUNS on
one stamped spec instead of skipping on thirteen unstamped ones). Two WARNs name
this paper: the slot-theme rows ruled above, and the `pools_sha` record — the
stamp `4b8f99d5682c` was written by the reroll and the pool was corrected
afterwards for R2-F5, which is exactly the "a legitimate pool repair invalidates
the stamp" case that check reports and never fails.

**`pools_sha` was inert on everything** (absent from all 13 specs), so nothing was
back-filled — a stamp for a draw whose pool bytes nobody can recover would be a
fabrication. Instead the skip line now says INERT in those words, names the
unstamped ids, and the WARN says that a stamp written by a reroll certifies that
redraw's pool and not the whole spec's. `20260818_1` is stamped only because its
9番 stimulus was genuinely redrawn against the current pool.
