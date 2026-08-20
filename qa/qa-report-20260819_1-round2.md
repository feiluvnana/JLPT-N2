# QA report — テスト 20260819_1 (round 2, fresh eyes)

Reviewed revision (sha1[:12] over raw bytes; re-verified unmoved after the pass):

- `言語知識・読解.md` = `b51b278b1573`  (mtime 2026-08-20 13:40:48)
- `聴解.md` = `81f1b7846a31`  (mtime 2026-08-20 11:20:14 — unchanged since round 1)
- `聴解スクリプト.txt` = `b856e2fc0de8`  (mtime 2026-08-20 11:19:47 — unchanged since round 1)
- `聴解.mp3` / `聴解_チャプター.json` `script_sha` = `b856e2fc0de8` (matches), `pacing_sha` = `d241e428f28f`
- `qa/20260819_1/keyless.md` = `2063e1f90232` — **rebuilt after the pass, byte-identical**, so no fixing pass edited underneath this review.

Reviewed 2026-08-20. The reviewer authored nothing in this paper, read
`exam-qa-review/SKILL.md` in full before its first other tool call, and solved
the paper blind before opening any key table or the round-1 report. Every claim
below was re-derived from disk; **nothing was inherited from round 1**, and the
round-1 report + its §8 disposition were read only *after* the blind solve was
scored.

---

## 1. Verdict

**QA: FAIL (5 findings, 2 automatic)**

The five round-1 findings are all genuinely closed, and all four pipeline
repairs (sampler, gate, `matrix_helper`, pool) do what §8 claims — each was
re-run against its own founding case here. Two of the four printed items the
fix pass **re-authored** are broken in a way round 1's items were not: 問題8-43
and 問題8-47 each admit a second grammatical ★ ordering, because both were cut
as *[adjunct chunk] + [を-object] + [predicate]*, and Japanese does not fix the
order of an adjunct against an object of the same verb. Both 解説 prove
uniqueness with a leg (`「を」は他動詞を要求する → よって隣接する`) that is false by
construction and that `bunpou.md`'s illegal-leg list does not yet name.

This is the failure mode the skill states outright: *fixes introduce defects at
the same rate as authoring.*

---

## 2. Blind-solve diff

**Solved from `qa/20260819_1/keyless.md`** (built by `make keyless 20260819_1`;
1088 lines; keys, key tables, marked answer grid and 解説 column stripped by
`strip_key()`). All 101 items plus the four 例 were answered from that file
alone — 聴解 from the embedded `聴解スクリプト.txt` — and written down before any
sourced Markdown, `test_spec.json`, or the round-1 report was opened.

```
python3 tools/qa_eval.py tests/20260819_1 --answers "[3,1,1,2,4, 2,4,1,2,3, 2,3,4, ...]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches.** No mis-key, no unanswerable item, no 例 whose announced
number the dialogue does not support. (One transcription slip in my first
`--answers` vector — item 26 typed as 1 where my worked answer said 2 — was my
own and is recorded here rather than hidden; the corrected vector is 101/101.)

100 % agreement is evidence about **which option the paper's own sources
support**, and is *zero* evidence about **second** defensible answers. The
two-answer hunt (step 2) and the 問題8 permutation read (step 3) ran separately
on all 101 items, and that is where this round's automatic fails come from —
at 問題8-43 and 問題8-47 my blind answer matched the key *and the item still has
two answers*, because the rival ordering keys a different ★ card.

---

## 3. Per-question walkthrough — all 101 items + 4 例

Sources read side by side: `tests/20260819_1/言語知識・読解.md`, `聴解.md`,
`聴解スクリプト.txt`, `test_spec.json`, `logs/ledger.json`, `logs/topics.json`,
`.agents/exam-blueprint/references/pools.json`, plus `refs/JLPT_N2_NEW/*` for
calibration. **The six items the fix pass changed carry a ⚑ and were re-derived
from scratch, tool output in their 解説 disregarded.**

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| ⚑問題1-1 | 3 えんぜつ | OK | Grid re-derived by hand: {えんせ,えんぜ}×{つ,い} → えんせつ/えんせい/えんぜつ/えんぜい = the four printed options exactly, no arbitrary 5th ending. 演=エン (sole on-reading); 説=セツ/ゼツ(連濁)/ゼイ(遊説=ゆうぜい) — every distractor is branch (a), a reading of the target's own kanji. Stem 「会長が今年の目標について短い**演説**をした」 fixes the word. No okurigana on any option (二字熟語), so nothing is selected on sight. `演説(えんぜつ)` is a `pools.json` `kanji_reading` entry and occurs in 1 archive booklet | — |
| 問題1-2 | 1 ほうがく | OK | {ほう,ぼう}×{がく,かく}; 方=ホウ/ボウ, 角=カク/ガク(連濁). 「進むべき**方角**さえ分からなく」 | — |
| 問題1-3 | 1 なさけ | OK | 「困っている人に**情け**をかける」. なさけ/たすけ/しつけ/いいつけ all real 和語 nouns, okurigana 「け」 shared by all four | — |
| ⚑問題1-4 | 2 しゅっか | OK | Grid re-derived: {しゅう,しゅっ}×{か,が} → しゅうか/しゅうが/しゅっか/しゅっが = the four printed, complete and closed. 出=シュツ→シュッ before the voiceless カ; 荷=カ. 「この村で採れた野菜は、翌朝のうちに都市へ**出荷**される」 fixes it. しゅうか is the strongest distractor (homophone of the real, same-field 集荷). Pool entry `出荷(しゅっか)` present | — |
| 問題1-5 | 4 つねに | OK | 「戸締まりを**常に**確かめる習慣」. All four are 〜に-type time/frequency adverbs, 「に」 shared | — |
| 問題1 全体 | — | OK | **訓読み 2 of 5** (情け, 常に) against the cap of 2 — `is_kun_target()` re-run over the whole ledger reproduces 20260807_1=4 / 20260810_1=3 / 20260817_2=3 / this paper=2. 2×2 on-reading grid now runs in **3 of 5** slots (1, 2, 4), against official's 3–4. F3 closed | — |
| 問題2-6 | 2 漢和 | OK | {漢,緩}×{和,話}; `matrix_helper validate --reading かんわ` = PASS with per-kanji segmentation printed. 「成り立ちや部首からも字を引ける」 fixes 漢和; 緩和 is real but names no dictionary | — |
| 問題2-7 | 4 回転 | OK | {回,開}×{転,店}; validate --reading かいてん = PASS. 「自らの軸を中心に」 excludes 開店 | — |
| 問題2-8 | 1 削減 | OK | {削,作}×{減,限}; validate PASS; 作減/作限/削限 pseudo-compounds (official practice) | — |
| 問題2-9 | 2 形容動詞 | OK | {形,型}×{容,要} + fixed 「動詞」; validate --reading けいようどうし = PASS (all four segment to けいようどうし). 「『静かだ』『便利だ』のように活用する語」 fixes the part-of-speech name | — |
| 問題2-10 | 3 意義 | OK | {意,異}×{義,議}; validate PASS. 「大きな**いぎ**を見いだしている」 — 異議 takes 唱える/申し立てる, never 見いだす | — |
| 問題3-11 | 2 不 | OK | 「説明が（　）十分だったため、質問が相次いだ」; 未/不/無/非 are the four real negating prefixes; 未十分・無十分・非十分 are non-words | — |
| 問題3-12 | 3 沿い | OK | 「線路（　）に一キロほど続いている」 — 向き/寄り/沿い/越し all real positional suffixes; only 沿い takes a long continuous path | — |
| 問題3-13 | 4 まみれ | OK | 「棚は、どれもほこり（　）だった」 — ずくめ/がち/ぎみ/まみれ all real state suffixes; only まみれ attaches to a substance | — |
| 問題4-14 | 2 恐らく | OK | 文末「だろう」 is the 呼応 partner; まさか wants 打ち消し推量, いかにも wants らしい/そうだ, 案の定 needs a confirmed outcome. All four are 陳述副詞 — one functional category | — |
| 問題4-15 | 1 自営業 | OK | 「会社を辞め」「父から受け継いだ技術を生かして」 — 副業/兼業 presuppose a surviving main job, 分業 needs several people. All four are work-form nouns | — |
| 問題4-16 | 4 煮る | OK | 「だし汁で」「やわらかくなるまで」 — 焼く uses no liquid, 蒸す uses steam not だし汁, 炒める uses oil. Four cooking transitives | — |
| 問題4-17 | 3 身が入らなかった | OK | 「休みの予定ばかり考えてしまい」 gives the cause; 気が済む needs 「〜するまで」, 歯が立たない is about difficulty, 目が届かない is about others/wide scope. Four body-part idioms in one form | — |
| 問題4-18 | 4 不足している | OK | 「必要な実務経験が半年ほど（　）」 — a shortfall against a requirement. 減少/低下/消耗 all describe going down from a prior level, which accumulated experience does not do | — |
| 問題4-19 | 3 開発 | OK | 「水をほとんど使わずに布を染める技術の（　）に成功した」 — 開拓 opens a field/land, 発掘 finds what is buried, 製造 makes goods to a fixed design. Four サ変 creation nouns | — |
| 問題4-20 | 1 固い | OK | 「いつかまたここで会おうと（　）約束」 — 厚い=layer/quantity, 濃い=density, 重い=burden; only 固い collocates with 約束 for unbreakability. Four イ形容詞 | — |
| 問題5-21 | 4 わずかに | OK | 「庭の草に**うっすら**雪が積もっていた」; substitution test: 「庭の草にわずかに雪が積もっていた」 survives. すっかり/たっぷり/厚く all denote quantity, not thinness. F5's pool repair (`うっすら(かすかに)`→`うっすら(わずかに)`) makes the paper and the pool agree; the item itself never moved | — (see obs. 3: わずかに is also a distractor at 23) |
| 問題5-22 | 2 ぼんやりした | OK | 「**うつろな**目で窓の外を見ていた」; 思いつめた=absorbed, けわしい=tense/angry, 落ち着きのない=darting — all four are gaze modifiers, none but ぼんやり means "nothing registering" | — |
| 問題5-23 | 3 さらに | OK | 「値上げが続き、家計のやりくりは**いっそう**厳しくなった」; わずかに reverses the degree, 一時的に conflicts with 「続き」, 思ったより compares to expectation not to before | — |
| 問題5-24 | 1 強い驚きを与える | OK | 「事故を伝える映像は…**衝撃的な**ものだった」; the other three are warm / comic / unremarkable — same functional slot (impression on the viewer), opposite content | — |
| 問題5-25 | 2 遅い | OK | 「シャッターを押してから記録されるまでの反応が**鈍い**」 — the stem's own 「〜から〜まで」 makes it a duration; 弱い=strength, 短い=reverses, 大きい=magnitude | — |
| 問題6-26 | 2 | OK | 「調査の結果、…汚染を引き起こした工場が**特定された**」 = narrowing to one from evidence. 1 wants 決定する, 3 wants 把握する, 4 wants 保つ | — |
| 問題6-27 | 1 | OK | 「しょうゆが**切れて**しまい、近所の店まで走った」 = stock ran out, canonical. 2 wants 途切れて, 3 wants 割れた, 4 wants 枯れて | — (obs. 6: opt 2 is the weakest of the paper's 15 wrong 問題6 sentences) |
| 問題6-28 | 3 | OK | 「動かなくなった古いラジオを**分解して**、故障の原因を調べた」. 1 wants 分担して, 2 wants 決裂した, 4 wants 分割する | — |
| 問題6-29 | 2 | OK | 「その日の朝に市場で**吟味した**魚だけを客に出す」 = inspecting to select quality. 1 wants 確認して, 3 wants 修復して, 4 wants 見直した | — |
| 問題6-30 | 4 | OK | 「祖母の法事と息子の入学式が同じ日に**重なって**しまった」. 1 wants 増えて, 2 wants かかった, 3 wants 膨らんで | — |

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 気になってならない | OK | 「気にしないつもりでいたが、やはり」 — an admission that the feeling won't be suppressed. 2 「していられない」 = no spare capacity, opposite of 「やはり」; 3 is 禁止; 4 denies as a general property what the speaker is currently feeling | — |
| 問題7-32 | 3 道も空いていることだし | OK | 「ことだし」 offers one supporting reason for 「思い切って〜ことにした」. ばかりに needs a bad outcome; どころか needs the contrasted element after it; くせに blames one subject and cannot bridge 道 → 私 | — |
| ⚑問題7-33 | 1 待つよりほかない | OK | 「原因が分からない以上、業者の到着を（　）ですね」 answering 「いつになりそうですか」. **New option 2 「待つわけにはいかない」 re-derived: eliminable.** 〜以上 licenses the conclusion the premise forces; "cause unknown" is the reason *to* wait (nobody on site can fix it), never a reason it is impermissible — and "we can't wait" answers no when-question. 3 「に違いない」 is 3rd-person conjecture, not a plan; 4 「べきではない」 is advice against waiting, which the premise cannot yield. 「どころではない」 now appears in **1** 問題7 item only (問41) — grep-verified, 2 occurrences in the file and both are 問41 (option line + its own 解説) | — |
| 問題7-34 | 1 駅ビルの完成とともに | OK | 「新しい（　）、人の流れが…移ってしまったのだ」 — parallel change. に応じて needs a scaling variable; に先立って reverses the time order against 「終わってから」; をもとに needs material for a judgement | — |
| 問題7-35 | 2 静かなものの | OK | 「音が（　）、吸い込む力は前のものに及ばない」 — plain concession. わりに needs the premise to *raise* an expectation the outcome undercuts, and quietness raises no expectation of suction; ばかりに needs quietness to *cause* the weakness; うえに adds same-direction items | — |
| 問題7-36 | 1 吐くことだ | OK | B advises A who is shaking: 「そういうときは、まず息を長く（　）」. ことだろう is conjecture, ことにする is the speaker's own decision, ものだ states a general truth not personal advice | — |
| 問題7-37 | 3 長く続けていく上で | OK | 「〜上で」 on 辞書形 = "in the course of", licensing 「大切なのは〜だ」. うちに needs a change during the interval; 上に adds a second item that never comes; 末に takes た形 (考えた末に) | — |
| ⚑問題7-38 | 4 に越したことはない | OK | 「契約の前に細かい条件まで確認しておく（　）。もっとも、読み通すには時間がかかる」 — 「もっとも」 is a qualifier on a recommendation, which only 「に越したことはない」 provides. **New option 2 「はずがない」 re-derived: eliminable.** 「保険は」 is the topic, i.e. the thing checked, not a subject capable of checking; 「確認しておくはずがない」 has no one to deny, and flatly contradicts the 「もっとも」 rider. 1 にすぎない devalues; 3 とは限らない needs a generalisation to except | — |
| 問題7-39 | 2 ができて以来 | OK | 「〜て以来」 = a boundary event whose state persists — 「めっきり減ってしまった」. しだい needs a future action; うちに cannot mark a boundary; ないかぎり contradicts the store existing | — |
| 問題7-40 | 2 のことだから | OK | 「用心深い彼女（　）、…はずですよ」 — 呼応 with はずだ from a known character trait. にしては needs an observed fact; だけあって needs a confirmed result; とあって needs an actual event | — |
| 問題7-41 | 4 慌てることはない | OK | 「まだ締め切りまで二週間ある。そんなに（　）よ」 — reassurance. 1 どころではない cannot take the degree adverb 「そんなに」; 2 ずにはいられない reverses; 3 ようがない means no means exists | — |
| 問題7-42 | 4 調べてからでないと | OK | 呼応 with the negative 「何とも申し上げられません」. からには forces "of course we will"; からこそ leads to a positive; にあたって needs the action taken on the occasion | — |
| 問題7 全体 | — | OK | Stem distribution measured, all three `bunpou.md` numbers: JP chars `[25,24,51,55,43,45,35,43,38,64,22,50]` → **mean 41.2** (band 36–52 ✓), **3 stems under 34** (need ≥2 ✓), **max−min = 42** (need ≥25 ✓). Dialogue/setting-label stems present (33, 36, 40). 5-kana form reuse re-measured by hand: max **2** — 「いられない」(31,41) and 「ことはない」(38,41). Shipped gate threshold is >2 | — (see §5 ruling and obs. 4) |
| ⚑問題8-43 | 2 畑に出る日を | **自動不合格 (R2-F1)** | Keyed order 「長年の経験に→基づいて→**畑に出る日を**→決めているそうだ」. Rival `(2)→(4)→(1)→(3)` = 「祖父は…**畑に出る日を長年の経験に基づいて決めているそうだ**。」 — fully idiomatic, identical meaning, ★ = **1**. 「〜を〜に基づいて決める」 and 「〜に基づいて〜を決める」 are both ordinary Japanese; nothing in the item forces one. The 解説's proof leg 「『畑に出る日を』の『を』は他動詞を要求し…［畑に出る日を→決めているそうだ］も連続した塊になる」 is **false**: a case-marked argument requires a licensing predicate *somewhere later*, never an adjacent one. `verify_scramble` lists the rival among its 12 survivors and returns `RESULT: UNDECIDED` (by design) | Re-cut the item so no two cards are free co-arguments of one verb. Cheapest route: fold 「長年の経験に」 into the stem (「祖父は…今も、長年の経験に」) and make the fourth card a chained modifier, or replace 「畑に出る日を」 with a card that must be adjacent to its host (a 連体修飾 chain, as official 12/2025-47 and 7/2025-45 do) |
| 問題8-44 | 4 受け継ぐ人が | OK | 「つまり→あの技術を→**受け継ぐ人が**→身内にいなかった ということだろう」. Unique: 「あの技術を」 sits *inside* the relative clause headed by 受け継ぐ人, so nothing may intervene; 「つまり」 rephrases the preceding sentence and can only be blank-initial; the printed tail 「という」 demands a 普通形 predicate, which only 「身内にいなかった」 is | — (the 解説's *reason* for the を-block is the invalid transitivity leg; the conclusion is right for the relative-clause reason instead — see R2-F3) |
| 問題8-45 | 4 受け付けを | OK | 「申請書に不備が→あった場合は→**受け付けを**→断らねばならない」. The rival `(4)→(1)→(2)→(3)` 「窓口の担当者は、受け付けを、申請書に不備があった場合は断らねばならない」 was tried and is degraded, not merely dispreferred: 「窓口の担当者は」 already occupies the topic slot, and stranding a bare を-object between it and a second は-marked conditional gives three fronted phrases before any predicate. Item stands | Rewrite the proof: the leg 「『受け付けを』の『を』は他動詞を要求し…塊になる」 is invalid (R2-F3). Replace it with the topic/は-stacking argument above |
| 問題8-46 | 1 心細いものは | OK | 「体を壊した→ときほど→**心細いものは**→ない」. 「ときほど」 is a 形式名詞 needing a 連体修飾 predicate, and only 「体を壊した」 is one; 「〜ほど〜はない」 is a fixed superlative template whose ほど-phrase precedes the ものは-phrase — the reverse (「心細いものは体を壊したときほどない」) breaks the template. Unique | — |
| ⚑問題8-47 | 2 客の感じ方を | **自動不合格 (R2-F2)** | Keyed order 「味だけでなく→皿の色や明るさも→**客の感じ方を**→変えているからだ」. Rival `(2)→(4)→(1)→(3)` = 「…感じられるのは、**客の感じ方を、味だけでなく皿の色や明るさも変えているからだ**。」 — grammatical OSV scrambling, identical meaning, and it puts the 「だけでなく…も」 focus phrase immediately before its verb, which is the canonical focus position. ★ = **1**. No semantic discriminator exists to exclude it; the 解説 excludes it with the same invalid 「を→他動詞→隣接」 leg as 43 | Re-cut. Move 「客の感じ方を」 into the stem (「…おいしく感じられるのは、客の感じ方を」) so the four cards form one chain, or replace it with a card that must be adjacent to its host |
| 問題8 全体 | — | 要修正 | Register mix (bunpou.md): formal/institutional = 1 (45), personal/casual = 2 (43, 46) — inside the 「≤2 formal, ≥2 personal」 target. No bare adverb card (gate ok). Both re-authored items realize their drawn `grammar_p8` targets (`〜に基づいて`, `理由説明(〜のは…からだ)`) — gate ok, spec-verified | — |
| 問題9-48 | 1 それでいて | OK | [論理接続] 「家族の命を守るために玄関に置かれている。（48）、一度も背負われないまま何年も過ぎていく」 — one object's two contrary faces. そのうえ adds same-direction; なぜなら needs a reason; そこで needs an action taken | — |
| 問題9-49 | 3 役に立たないわけだ | OK | [文末モーダル] the two preceding sentences establish that the bag cannot be carried in the dark with a child in tow — 「わけだ」 states the consequence that follows. わけがない negates absolutely; わけにはいかない needs a volitional act; わけではない is a partial denial that undoes the paragraph | — |
| 問題9-50 | 2 そもそも無理がある | OK | [慣用・形式名詞] 「持ち出す量と家に置く量を同じにしようとするところに、（50）」 — 「〜ところに」 takes a defect predicate. きりがない does not take 〜ところに; 変わりはない needs a comparand; 差し支えない contradicts the paragraph | — (see obs. 5: the same phrase is printed inside the KEY at 問題13-69) |
| 問題9-51 | 4 持ち出す分と残す分に分ける | OK | [内容推論] the third paragraph's whole proposal (最初の一日分だけ袋に、残りは家や車に). 1 drops the "keep the rest at home" half; 2 is what the text calls the cause of the weight; 3 is a downstream result, not what lightening *is*. Four distinct categories, no two blanks sharing one; all options ≤16 JP chars | — |

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 3 | OK | 「丈の高い植生（注1）が、川と林とをつなぐ回廊（注2）になっているからである」＋「刈り取れば道筋は分断され、数年たっても戻らない」. 1 reverses 「刈られた土手は歩きやすく」; 2 cost is never mentioned; 4 the insect count is a result, not the purpose | — |
| 問題10-53 | 4 | OK | 「立ち上げの遅れが最も短かったのは、操作に最も慣れた班ではありませんでした」＋「伝票の余白に気づいたことを書き残す習慣のあった班です」. 1 is the denied claim; 2 no re-formatting is described; 3 is the *future* plan, not the record | — |
| 問題10-54 | 2 | OK | 「食べ物と飲み物は、手作りかどうかにかかわらずお売りになれません」. 1 vs 「市外の方はお申し込みになれません」; 3 vs 「前もってのお振り込みはできません」; 4 vs 「雨天の場合は五月十日に延期します」 | — |
| 問題10-55 | 3 | OK | 「まずこの感じ取る力が落ちる」＋「実際に働く汗腺の割合が減る」＋「この二つが同じ時期に進む」. 2 vs 「汗腺の数は変わらない」; 1 and 4 assert what the passage does not | — |
| 問題10-56 | 1 | OK | 「支援策の数を数える前に、必要な人が何か所を回らされているかを数えるべきである」. 3 is the stated problem, i.e. the reverse; 2 and 4 are absent | — |
| 問題11-57 | 1 | OK | ①**空白は情報の不在ではない** → 「その空いた時間に流れ込んだのは、真偽の確かめられていない書き込みだった」＋「人は黙って待ってはくれない」. 2 reverses; 3 cost absent; 4 speed of verification absent | — |
| 問題11-58 | 3 | OK | 「この三つを言い分けて数字を出しておけば…理解は崩れない」＋closing 「誤りに気づいてから直し終えるまでを短くする段取りである」. 2 is the tried-and-failed policy; 1 and 4 are not the thesis | — |
| 問題11-59 | 4 | OK | 「分かれ目は、代わりのバスの経路をいつ引き始めたかにあった」. 3 vs 「過疎の進み方も、高齢者の割合も、両者でほとんど変わらない」; 1, 2 absent | — |
| 問題11-60 | 4 | OK | 「廃止の議論が続いているあいだに、通学と通院の時刻を住民から集め…経路を先に引いていた」. 3 vs 「駅を起点にするのをやめて」; 1, 2 absent | — |
| 問題11-61 | 3 | OK | ①**残しておいたのは手続きではなかった** → 「自分が消えたあとに残る困りごとを、一つずつ数えていたのだ」 + the enumerated 鍵の予備/地主の名前/猫の餌/鉢の返し先. 1 vs 「預金や保険の欄はほとんど空白のまま」; 2, 4 absent | — |
| 問題11-62 | 2 | OK | 「書き留められていたのは、片づけようのない結び目（注5）のほうだった」＋「誰かに返すもの、誰かに頼むこと、誰かが困ること」 | — |
| 問題11-63 | 2 | OK | ①**看板を高く掲げた家ほど短命だった** → 「交流を売り物にした家では、一年以内に退去する人の割合が、そうでない家の二倍近くに上っていた」 | — |
| 問題11-64 | 1 | OK | 「洗濯を待つ数分のあいだに言葉を交わす」＋「話したくない日は、そのまま部屋へ戻る」. 2 vs 「共用の居間は狭く」; 3, 4 absent | — |
| 問題12-65 | 4 | OK | A 「座っている時間を集めても、その日に何が前へ進んだかは一行も分からない」 / B 「席に着いている時間を数えても仕事の中身は見えないという点も、そのとおりだと思う」 — the one proposition both state. 3 is B only (A does not reject outcome-measurement) | — |
| 問題12-66 | 1 | OK | A 「週の初めに今週終える仕事を三つまで書き出し、金曜にその三つを並べて確かめる手順」 / B 「見えにくい仕事を評価の表に書き入れておかないかぎり」. 2 vs A's 「私はこの方向に反対である」 | — |
| 問題13-67 | 2 | OK | 「単語も文末の言い方も共通語になっているのに、声の高さの動きだけはその土地のものが残っている」. 1 swaps what stays; 3 vs 「次に文の形が変わり」; 4 adds 文の形 | — |
| 問題13-68 | 4 | OK | 「前者は資料を増やし、後者は機会を増やす」＋「記録は、言葉を資料に変える作業である。継承は、言葉を口に出せる場面を増やす作業である」 | — |
| 問題13-69 | 2 | OK | 「だが、要るものが違う」＋closing 「二つを同じ名前で呼んできたあいだに…同時に進んでいた」. 4 vs 「抑揚が最後まで残る」 | — (obs. 5) |
| 問題14-70 | 4 | OK | Combines **two** flyer cells: 「学生券をお求めの方は、学生証を窓口でお見せください」 (学生券 usable) and 「市立美術館の特別展は共通券の対象外です」「別に800円が必要です」. 1 vs 学生券's 使える期間 = 買った日と翌日; 2 vs 「ほかの割引とを合わせてお使いになることはできません」; 3 vs 郷土博物館's 共通券での利用 = 一回 | — |
| 問題14-71 | 2 | OK | Combines **two** cells: 「中学生以下のお子様は…券は必要ありません」 and 郷土博物館/市立美術館 休館日 = 月曜日. 1 vs the same closures; 3 vs 二日券 = 買った日と翌日; 4 vs 「十名以上の団体…三日前までに」 | — |
| 読解 全体 | — | OK | 32 in-body `（注N）` markers with 32 matching definition lines (1-to-1; ≥25 floor, inside the 27–61 official band); 4 `（中略）`, all inside 問題11–13; **zero `<ruby>`**; marked spans ①/② match their stems 1-to-1 and stay pointer-sized; uniquely-longest key rate **4/20 = 20 %** (target ≤30 %), tied-longest **6/20 = 30 %** (target ≤35 %); all 20 items within max/min ≤1.30; no verbatim lift | — |

### 聴解 (30 scored + 4 例)

The セクション構成表 was read as **columns before any item**, then re-derived
against the script rather than trusted (every 消去方法 cell's quotation was
grepped in `聴解スクリプト.txt`; all present verbatim).

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 聴解問題1-例 | 3 | OK | 「参加する人の名前、先にまとめてくれる?」; the other three each denied (人数=名前がそろってから／バス=中村さん／しおり=もう作ってある). Announced 「3番」 = marksheet pre-mark | — |
| 聴解問題1-1番 | 1 | OK | 「追加でコピーしといてくれる?」→closing 「機械が空いてるうちに行ってきます」. 2後回し／3実行不可／4規則で不可, each with its script line | — |
| 聴解問題1-2番 | 1 | OK | 「分け終わった袋を、あそこの軽トラックまで運んでくれる?」. 2条件不足／3不要／4明確に否定 | — |
| 聴解問題1-3番 | 2 | OK | 「今回のいすは、その金額を超えちゃうから…二社にお願いしてくれるかな」. 1既に完了／3後回し／4条件不足 | — |
| 聴解問題1-4番 | 2 | OK | 「下の階の方に、天井にしみが出ていないか、声をかけていただけますか」. 1不要／3別の人に割り当て／4実行不可 | — |
| 聴解問題1-5番 | 2 | OK | 「かばんから出して、お手元にお持ちください」. 1順番待ち／3規則で不可／4明確に否定 | — |
| 聴解問題1 全体 | — | OK | Keys [1,1,2,2,2]: two distinct digits, but all six keyed **actions** differ, and 6 of 31 official sittings do the same. Nine 消去方法 tokens at exactly 2 rows each (cap 2), re-counted from the 解説 cells not the table. Question type 「この後まず何をしますか」 ×6 ✓. Closing turns: 0 rhymes, 0 leaks | — |
| 聴解問題2-例 | 1 | OK | 「土曜は、朝のうちに三十人分しかご用意できないんです」＋「五十人はもう確定してます」. Announced 1番 | — |
| 聴解問題2-1番 | 4 | OK | 「その方の分だけ卵を外してお作りできます」＋「じゃあ、そうしてください」. 1金曜=みんな仕事で無理／2他コース=満席／3個室=そのまま | — |
| 聴解問題2-2番 | 3 | OK | 「この数字が、一日のうちのいつ高くなっているのか」＋「それがまだ分からないんです」. 1「いえ、少し上です」／2「お父様のことは…結びつきませんよ」／4「今回は出しません」 | — |
| 聴解問題2-3番 | 3 | OK | 「注文を一人ずつ変えられるお店にしたいの」＋「みんなが食べられる方がいい」. 1「駅から少し歩くけど」／2「三つとも、ほとんど同じ」／4「今年はどこも個室が取れる」 | — |
| 聴解問題2-4番 | 1 | OK | 「風呂の入れる回が決まってるなら、そっちに合わせます」. 2「電車は予定どおり着いた」／3「もうご用意ができております」／4「先週で終わってしまいまして」 | — |
| 聴解問題2-5番 | 4 | OK | 「ゴムを入れ替えないと、水が入る」＋「うちには、そのゴムを置いてなくて」. 1「電池はございます」／2「交換はいつも私がしております」／3「部品は、今も作られております」 | — |
| 聴解問題2-6番 | 2 | OK | 「駅の裏の駐車場でもお返しいただけますよ」＋「かぎは、駐車場の隣にあるお店にお持ちください」. 1「工事をしておりまして、お預かりを止めております」／3「戻していただかなくても大丈夫」／4「船に車を乗せるお客様だけ」 | — |
| 聴解問題2 全体 | — | OK | Question types: どうして 3 (2,4,5) / どのように 2 (1,6) / 何を一番 1 (3) — inside the quotas. All six keys are paraphrases or two-utterance merges, never a lifted line | — |
| 聴解問題3-例 | 2 | OK | 大きな水そうの楽しみ方 (三歩下がって／五分立ち止まって／上の階から). Announced 2番 | — |
| 聴解問題3-1番 | 1 | OK | 「思い切って席を三十に減らしました」＋「今は、席が少ないのに、一年の売り上げは当時より上です」. Talk mentions none of its three wrong options — correct for 概要理解 | — |
| 聴解問題3-2番 | 4 | OK | 「そのお客様が、その品物を何年、どんなふうに使うのかを先に聞くことだよ」 | — |
| 聴解問題3-3番 | 3 | OK | 「返す日を延ばすことができるのは、次にお待ちの方がいらっしゃらない本に限ります」 | — |
| 聴解問題3-4番 | 2 | OK | 「あの数字は、強さを表したものではないんです」＋「百回集めたとき、そのうち六十回は」 | — |
| 聴解問題3-5番 | 3 | OK | 「私がいちばん見ていただきたいのは、その本が、学ぶ人に自分のことを話させる作りになっているかどうか」 | — |
| 聴解問題3 全体 | — | OK | Question type 「何について話していますか」 ×6 ✓. Talk lengths (gate's own `p3_talk_chars`) 306/334/311/333/337, all above the 220 target and inside the official band. Broadcast/lecture/interview = 3 of 5 (1番ラジオ, 4番テレビ, 5番講演会), floor 3 ✓ | — (obs. 2: the 構成表 prints 2番=337 / 5番=334, transposed against the gate's measurement) |
| 聴解問題4-例 | 3 | OK | 「あと少しなので、昼までには」 answers 「間に合いそう?」. Announced 3番 | — |
| 聴解問題4-1番 | 1 | OK | 係員 directs the card-less patient to write at the first-visit window; 1 asks what to write. 2 is the staff's own line (立場の逆転); 3 claims it is already done before reaching the window | — |
| 聴解問題4-2番 | 2 | OK | Asked to attend in his place; 2 offers his free afternoon. 1 would ask the attendee afterwards (逆転); 3 switches to documents (ずれ) | — |
| 聴解問題4-3番 | 3 | OK | Told the insurance card has expired; 3 explains why the new one has not arrived. 1 invents a free-visit premise; 2 refers to a copy already handed over | — |
| 聴解問題4-4番 | 3 | OK | Told of a noise complaint; 3 undertakes to stop night work. 1 relays it upward (逆転); 2 sides with the residents (前提) | — |
| 聴解問題4-5番 | 1 | OK | 「勝つに決まってるよ」 → 「そう言って、前も負けたじゃない」. 2 takes 決まってる as "be selected"; 3 puts practice in the future | — |
| 聴解問題4-6番 | 2 | OK | Asked to check a schedule change; 2 asks the scope. 1 reverses who sent it; 3 takes スケジュール as the wall chart | — |
| 聴解問題4-7番 | 2 | OK | 「口が堅いから、相談しても大丈夫」 → 「思い切って話してみようかな」. 1 takes 口が堅い as food hardness; 3 inverts the premise | — |
| 聴解問題4-8番 | 3 | OK | 「手を焼いてるんです」 → 「そういう時期は、いつか終わりますから」. 1 changes subject; 2 hears 聞き分けがいい | — |
| 聴解問題4-9番 | 3 | OK | Asked for one more day; 3 grants it against the printing date. 1 apologises as the requester (逆転); 2 puts the deadline last week | — |
| 聴解問題4-10番 | 1 | OK | Told of a 10:00 visit tomorrow; 1 checks the meeting room. 2 reverses the direction; 3 talks about yesterday | — |
| 聴解問題4-11番 | 2 | OK | 「指定席と自由席、どちらを」 → 「二人で並んで座れる方で」. 1 takes 指定 as a designated place; 3 is the clerk's own line | — |
| 聴解問題4 全体 | — | OK | Keigo direction consistent in every pair (customer↔counter staff, junior↔senior). No 「はい／いいえ／いえ／では」 opener among 36 replies. 「もう/先ほど＋〜た」 shape in 2 items (1番, 3番), cap 2 ✓. All 11 drawn `quick_response` strings appear verbatim in the script | — |
| 聴解問題5-1番 | 2 | OK | 「中身をお客様に選んでいただく形にすれば」＋「中身を三種類だけにしておけば」→「あ、それならできそう」「じゃあ、それでいきましょう」. 1 withdrawn by its own proposer (仕入れ＋朝五時)／3 火口が一つ／4 箱代 | — |
| 聴解問題5-2番 質問1 | 3 | OK | 「実は先週、相談の方を申し込んどいたんだ」＋「一時からで取っちゃってるから、授業とちょうど重なる」. 4 定員／2 午前だけ／1 時間が重なる | — |
| 聴解問題5-2番 質問2 | 1 | OK | 「私はもう決めてる。模擬授業。」, never revised. 3「私、申し込んでない」／2「それじゃ、意味ないね」／4 定員 | — |
| 聴解問題5 全体 | — | OK | Nothing printed for either item (house rule, `jlpt-exam-structure`); 質問1/質問2 read the **same four names in the same order**, which is also the order the 職員 introduces them (一つ目〜四つ目); no deciding attribute is spoken beside any name; the resolving lines name attributes (申し込み済み／午前だけ／定員), never an ordinal | — |
| 聴解 全体 | — | OK | Narration ↔ label ↔ `SPEAKER_MAP` checked for every item: 学生=MALE +14Hz against 女=FEMALE +0Hz for 「男の学生と女の学生」; 職員/係員/担当者/医者/店員 are FEMALE and none is gendered by its narration; 店長=MALE for 「店長が話しています」. Whole-section uniquely-longest key rate 7/28 = 25 % (target ≤35 %). Section table present and, apart from obs. 2, correct | — |

---

## 4. Findings

| # | 項目 | Class | Evidence | Status |
|---|---|---|---|---|
| **R2-F1** | 問題8-43 | **自動不合格** — a second defensible ★ answer | Cards `1.基づいて / 2.畑に出る日を / 3.決めているそうだ / 4.長年の経験に`. Keyed `4→1→2→3` (★=2). Rival `2→4→1→3` = 「祖父は、周りの農家が新しい道具に頼るようになった今も、**畑に出る日を長年の経験に基づいて決めているそうだ**。」 — grammatical, idiomatic, and semantically identical to the key, with ★=**1**. The two chunks `[長年の経験に→基づいて]` (adjunct) and `[畑に出る日を]` (object) are co-dependents of one verb and Japanese does not order them. `verify_scramble` lists the rival among 12 survivors and returns `RESULT: UNDECIDED` — the tool never claimed uniqueness; the 解説 did | **OPEN** |
| **R2-F2** | 問題8-47 | **自動不合格** — a second defensible ★ answer | Cards `1.皿の色や明るさも / 2.客の感じ方を / 3.変えているからだ / 4.味だけでなく`. Keyed `4→1→2→3` (★=2). Rival `2→4→1→3` = 「同じ料理でも店で食べるとおいしく感じられるのは、**客の感じ方を、味だけでなく皿の色や明るさも変えているからだ**。」 — OSV scrambling, identical meaning, and it seats the 「だけでなく…も」 focus phrase in its canonical pre-verbal slot; ★=**1**. No semantic discriminator exists to exclude it | **OPEN** |
| **R2-F3** | 問題8-43/44/45/47 (4 of 5 解説) | 要修正 — a third illegal uniqueness leg, not in `bunpou.md`'s list | All four 解説 argue 「『Xを』の『を』は他動詞を要求し、四枚のうち他動詞を含むのは『Y』だけなので、［Xを→Y］は連続した塊になる」. The premise licenses only "Y appears somewhere after X", never adjacency. `bunpou.md` §問題8 names exactly two illegal legs (the lost-receiver leg and the stacked-particle leg) and `verify_scramble.illegal_legs()` detects exactly those two — both items returned `ARTIFACT: ok`. In 43 and 47 the leg is load-bearing (the item really is non-unique); in 44 it reaches the right conclusion for the wrong reason (adjacency there comes from the relative clause, not from transitivity); in 45 the item survives on an argument the 解説 does not make | **OPEN** |
| **R2-F4** | `tools/check_consistency.py::check_key_grammar_exposure` | 要修正 — `GATE-WRONG`, the 問題8 branch measures the LABEL, not the form | The branch does `re.sub(r"[（(].*?[）)]", "", pool_entry_text(e))`, which on a 類型-labelled entry deletes the FORM and keeps the LABEL. Run on this paper's five draws: `理由説明(〜のは…からだ)` → `"理由説明"`; `換言要約(〜つまり…ということだ)` → `"換言要約"`; `義務当然(〜ねばならない)` → `"義務当然"`; `〜ほど〜はない` → `"ほどはない"` (a string that cannot occur). Only `〜に基づいて` is measured correctly. Across the whole ledger, **46 of 70** recorded `grammar_p8` draws (66 %) are label-wrapped, so the 問題8 third of the rule has been inert on two-thirds of every 問題8 draw since it landed. The docstring says the 問題8 loop was *added* after R3-7 — it was added with the extraction inverted, which is exactly the "written from the incident narrative, never re-read against the rule text" failure §6.5 names | **OPEN** |
| **R2-F5** | 問題8-47 / 問題10(1) / 問題11(3) | 要修正 — a keyed 問題8 form is ordinary running text twice in the same paper's own 読解 prose, in the identical frame | 問題8-47's drawn point is `理由説明(〜のは…からだ)`. The 問題10–14 prose contains 「それでも刈り残しを続けた**のは**、丈の高い植生が、川と林とをつなぐ回廊になっている**からである**。」 (問題10(1) closing) and 「開く前に身構えた**のは**、財産の話が並んでいるだろうと思った**からである**。」 (問題11(3)) — **2 occurrences, both the 文末 cleft-reason frame the item tests**, against `exam-qa-review` §3's 「at most ONE occurrence, and never in the same syntactic frame」. Invisible to the gate for two independent reasons: R2-F4's label bug, and the prose writing 「からである」 where the pool entry writes 「からだ」 | **OPEN** |

### Round-1 findings — re-verified closed, not inherited

| # | Round-1 finding | Re-verification performed here | Verdict |
|---|---|---|---|
| F1 | 問題8-43/47 drawn from forms 20260818_1 keyed in 問題7 | Ledger re-read: `〜に基づいて` last drawn in **any** grammar category at `20260813_1` (7 draws back) and last in `grammar_p7` at `20260807_1` (13 back); `理由説明(〜のは…からだ)` last at `20260810_2` (11 back), never in `grammar_p7`. `cooldown_for('grammar_p8', 42) = 6`, so both clear their own window **and** the merged form-token window. `grammar_form_tokens()` re-read; `check_grammar_cross_category_rotation` prints `ok … (19 form tokens compared)` for this id and WARNs on the 8 grandfathered ids, each of which I confirmed against the ledger by hand | **CLOSED** (the *draw* is clean; the two items are broken for a different reason — R2-F1/F2) |
| F2 | 「どころではない」 in 3 of 12 問題7 items | `grep -c どころではない` = 2 occurrences in the file, both at 問41 (its option line and its own 解説). Re-ran the gate's own predicate (`P7_FORM_MIN_KANA = 5`) over the paper: max reuse now **2**, at 「いられない」(31,41) and 「ことはない」(38,41) | **CLOSED** |
| F3 | 問題1 訓読み 4 of 5 | `is_kun_target()` re-run over all 14 ledger entries: 20260807_1=4, 20260810_1=3, 20260817_2=3, **20260819_1=2** — reproduces the founding measurement exactly and matches `MONDAI1_KUN_GRANDFATHERED` = {20260807_1, 20260810_1, 20260817_2}. Both new grids re-derived by hand (see walkthrough) | **CLOSED** |
| F4 | `matrix_helper.py` generators + blind `validate` | Re-run: `validate --reading かいてん 回転 回体 同転 同体` → **FAIL, exit 1**, naming 回体/同転/同体; `--reading うんが 運河 運海 雲河 雲海` → FAIL on the 運海/雲海 pair (the 20260817_3 founding case); the real grid `開転 開店 回店 回転` → PASS with per-kanji readings printed; the same kanji grid **without** `--reading` → refused, exit 1; both generators exit 1 with the routing message. All five 問題2 grids re-validated with `--reading` → PASS; all three 問題1 kana grids return the Cartesian-shape-only string, which is what those 解説 cells now claim | **CLOSED** |
| F5 | `pools.json` `うっすら(かすかに)` | `pools.json` `paraphrase` now holds `うっすら(わずかに)` and a separate standalone `かすかに`; `test_spec.json` and `logs/ledger.json` carry the corrected string and agree field-for-field; `pools_sha` `aadf23081392` matches in spec, ledger and the live pool | **CLOSED** |

### Pipeline repairs — judged as a reviewer

| Change | Verified how | Verdict |
|---|---|---|
| `sample_items.py` 訓読み classifier + `KUN_CAP` + `kept=` | Imported `is_kun_target` and ran it over the ledger (table above). `KUN_CAP = {"kanji_reading": 2}` is wired into `draw()` at the `sample_kun_capped` branch, which receives `already=sum(1 for x in kept if is_kun_target(x))`, so a one-slot redraw counts the entries the paper keeps. `check_mondai1_reading_type_mix` **imports the same function**, so gate and sampler cannot disagree. The stated classifier limit (on-shaped single-kanji 訓 words read as 音) errs toward under-counting, i.e. toward passing — stated, not hidden | **SOUND** |
| `grammar_form_tokens()` merging `grammar_p7`/`grammar_p8` | Read the function; token = form with the 類型 wrapper stripped, cut on 「…・〜」, chunks ≥3 chars, namespaced. Verified on this paper's own entries. `GRAMMAR_FORM_MIN = 3` correctly drops 〜上/〜がち so short tails keep their ordinary string cooldown | **SOUND** — and see R2-F4: **the gate has a second, older copy of this extraction that is wrong, and was not switched over to this one** |
| Reroll off-by-one (own ledger entry dropped from recency) | Read both reroll paths: each finds `own_entry` and builds `updated_recency` from `[h for h in history if h is not own_entry]`, matching `prior_history` in `assert_rotation()`. The two are now measured against the same window; the kept picks stay excluded through `taken_text`, which is an in-test collision guard, not history. The reported abort (`目的結果(〜ために…なった)`, 20260813_2, 6 draws back against `cool=6`) is exactly the boundary case an off-by-one produces | **SOUND** |
| Three new gate checks + grandfather sets | Ran `make check`: exit 0, "All checks passed (30 skipped), **138** warning(s)". Warning delta from round 1's 124 accounted for exactly: 8 (`check_grammar_cross_category_rotation`) + 3 (`check_mondai1_reading_type_mix`) + 2 (`check_mondai7_option_form_reuse`) + 1 (`pools_sha` replayability, caused by F5's legitimate pool repair) = 14. No verdict moved. **Grandfather sets audited and honest**: each names its ids with the specific leak/measurement, each was confirmed against `logs/ledger.json`, and `20260819_1` is deliberately absent from all three, so no set hides a live defect on this paper | **SOUND** |
| `matrix_helper.py` | See F4 row | **SOUND** |
| `pools.json` + doc edits | See F5 row; `AGENTS.md` §4 `make matrix` row marked `validate only`, `bunpou.md` §問題7 carries the fourth binding number, `moji-goi.md` §問題1 carries the 訓読み cap | **SOUND** |

### The two reuses the fix pass deliberately left — rulings requested

- **「いられない」 ×2 (問31-2 「気にしていられない」, 問41-2 「慌てずにはいられない」): correctly left.** Both are **distractors**, and they are two different grammar points (〜てはいられない / 〜ずにはいられない) that merely share a 5-kana tail — the n-gram is a proxy for the form, not the form. Seeing the tail twice tells an examinee nothing, because neither sighting is a key. No repair.
- **「ことはない」 ×2 (問38-4 「に越したことはない」, 問41-4 「慌てることはない」): correctly left under the rule in force, but this is the pair to remove first.** Again two distinct Shin Kanzen headwords, so it is not a double-keyed form. But unlike the pair above, **both sightings are KEYS, and both sit at option position 4** — which is the shape 「the examinee learns the paper's habits」 actually describes. It is legal at the shipped `P7_FORM_REUSE_MAX = 2`; when the constant tightens to the official `1`, this is the pair that must go, and the tightening should not be done by shortening the n-gram. Recorded, no repair demanded this round.

### Minor observations (recorded, no repair demanded)

1. **`topics.json` `notes` arithmetic.** The row says 「twelve essay surfaces sit at exactly 2 per shape … with 随筆 1」 — 5×2+1 = **eleven**, not twelve (the 13 surfaces are 11 essays + 2 実用文). It also reports the 「A ではなく B」 reframe family as 「matched 0 passages」, which is the gate's marker-family **proxy** number presented as if it settled the question; a hand read finds two finals sharing the not-A-but-B skeleton (問題11(1) 「…技術より、…段取りである」, 問題12A 「…話ではない。…話である」) — at `dokkai.md`'s cap of 2, not over it. Every *quoted paper string* in `notes` was grepped and is still live (あおば市民ホール ✓, 800/1,200/600円 ✓, 十名以上 ✓, 三日前 ✓, 非常持ち出し袋 ✓, 二社に ✓, 水族館 ✓, 指定席と自由席 ✓, みどり市民ホール correctly absent ✓), and all five fields are present.
2. **`聴解.md` 構成表 問題3 talk lengths transposed.** The table prints 「2番=337／5番=334」; `make check`'s own `p3_talk_chars` prints `2番=334, 5番=337`. Both are in band, so nothing substantive follows, but the table is meant to be verifiable and this cell is not derived from the current script.
3. **「わずかに」 is the key at 問題5-21 and a distractor at 問題5-23.** Legal (no rule caps 問題5 option reuse) but a mild within-大問 tell. Unchanged from round 1.
4. **問題7 form reuse at the 5-kana window is 2, not 1** (ruling above). At shorter windows 「ばかりに」(32,35) and 「うちに」(37,39) also appear twice; both pairs are distractor-only and below the gate's 5-kana window.
5. **「無理がある」 is the keyed phrase at 問題9-50 and is printed inside the keyed option at 問題13-69** (「同じ名前で呼んできたことに無理がある」). The `check_key_grammar_exposure` rule counts prose, not options, and 「無理がある」 is a lexical phrase rather than a connective/modal — so no rule is broken. Still, the exact string that is the answer at 50 is inside the answer at 69; worth a different word at one of them.
6. **問題6-27 option 2 「そこで話が切れてしまった」** is the weakest of the paper's 15 wrong 問題6 sentences — 「話が途切れる」 is the idiom and 「話を切る」 is attested transitively, so 「話が切れる」 sits closer to the boundary than the other fourteen. The key (「しょうゆが切れて」) is unambiguous, so there is no two-answer risk; recorded for calibration only.
7. **問題11(4)'s closing move is label-sensitive.** Read as 意外な観察 the shape counts are 2/2/2/2/2/1 (compliant); read as 説明 — which its last two sentences arguably are, since the surprising finding lands mid-passage and the closing explains the mechanism — 説明 goes to **3**, over `dokkai.md`'s cap of 2. The passage was not touched by the fix pass; flagged so the next author re-reads it rather than inheriting round 1's label.
8. **Two newly-authored items share the agricultural register** — 問題1-4 「この村で採れた野菜は、翌朝のうちに都市へ出荷される」 and 問題8-43 「祖父は、周りの農家が…」. Neither is a topic-table surface, so no rule applies; noted because both are new this round and the fix pass's own note lists the words it avoided without listing this overlap. Likewise 問題8-47 adds a fourth food/restaurant surface (beside 聴解問題2-1番, 問題3-1番, 問題5-1番), all on different subjects.

---

## 5. Root-cause table (step 6.5)

| Finding(s) | Code | Tests showing the class | Owning file | Proposed edit (concrete) |
|---|---|---|---|---|
| **R2-F1, R2-F2, R2-F3** (one root cause — group) | `RULE-MISSING` + `GATE-BLIND` | **≥2 of 14 — systemic by the recurrence test.** Scanned every paper's 問題8 for the shape *[case-marked adjunct chunk] + [free を-object] + [single final predicate]*: `20260810_2` 問題8-45 (「契約書の細部にも／目を通しておくべきだ／説明を／しっかりと理解したうえで」 — rival 「契約書の細部にも、説明をしっかりと理解したうえで目を通しておくべきだ」 is grammatical and re-keys ★) and `20260819_1` 問題8-43 **and** 問題8-47. Official never does this: 7/2025 and 12/2025's ten 問題8 items are all single modification/quotative chains (「原料の小麦粉はもちろん水にまでこだわって」, 「自分の国にいては出会えない様々な文化や価値観を持つ人と交流したことで」) — no official item leaves two co-arguments of one verb free | `.agents/question-authoring/references/bunpou.md` §問題8 "The uniqueness proof is a TWO-PART procedure, and two structural legs are illegal" + `tools/verify_scramble.py::illegal_legs()` | **(1) `bunpou.md` — add the third illegal leg, verbatim:** "**「Xを」は他動詞を要求するので［Xを→その動詞］は連続した塊になる**" — **false.** A case particle licenses a predicate *somewhere later in the clause*, never an adjacent one; Japanese scrambles co-arguments freely. **The construction rule that follows: at most ONE card may be a free co-argument of the final predicate.** If two cards are both dependents of the same verb and neither is inside a 連体修飾 or 引用 chain, the item has two ★ answers whatever the 解説 says — re-cut it (move one into the stem, or replace it with a card whose host forces adjacency). Legal adjacency comes from a 連体修飾 head (問題8-44's 「あの技術を→受け継ぐ人が」), a quotative 「と」, or a subcategorised particle (「に→基づいて」) — never from transitivity alone. **(2) `verify_scramble.py::illegal_legs()` — add a third detector** matching `を」?は?他動詞を要求` / `を.{0,6}要求し.{0,20}連続した塊` within `LEG_WINDOW` of a named card, and FAIL unless that card's partner is a 連体修飾 head or a quotative. **Founding-case run required before commit:** on `20260819_1` it must fire on 問題8-43, 44, 45 and 47 (all four print the leg) and on `20260810_2` 問題8-45; state those ids in the docstring so the widened rule cannot quietly re-classify shipped work. |
| **R2-F4** | `GATE-WRONG` | The check is silent on **46 of 70** recorded `grammar_p8` draws across all 14 papers (66 %), and on 4 of this paper's 5. Silence, not a wrong number, is the symptom — exactly the class §6.5 calls the most dangerous | `tools/check_consistency.py::check_key_grammar_exposure` | **Delete the local regex and call the extraction that already exists.** The check currently does `form = re.sub(r"[（(].*?[）)]", "", pool_entry_text(e))`, which keeps the LABEL. `sample_items.grammar_form_tokens()` — written by this same fix pass, one day earlier, for this exact job — strips the 類型 wrapper, cuts on 「…・〜」 and keeps chunks ≥3 chars. `check_mondai1_reading_type_mix` already sets the precedent of importing from `sample_items` so gate and sampler cannot disagree; do the same here: `for tok in sample.grammar_form_tokens(e): form = tok.removeprefix(GRAMMAR_FORM_NS)`. **Also normalise the copula tail before counting** (`からだ`≡`からである`, `のだ`≡`のである`, `だ`≡`である`) — without it R2-F5 stays invisible even after the extraction is fixed. **Founding-case measurement to paste into the docstring:** on `20260819_1` the repaired check must print `問題8 target「のは…からだ」×2 (問題10(1), 問題11(3))`; re-run it over all 14 papers and name every id that gains a line. |
| **R2-F5** | `GATE-BLIND` (consequence of R2-F4) + a blueprint gap | 1 observed on this paper; unmeasurable elsewhere until R2-F4 lands, which is the point | `tools/check_consistency.py` (via R2-F4) + `.agents/exam-blueprint/SKILL.md` §"Rotation model" | The gate repair above is the mechanical half. The authoring half: **`exam-blueprint/SKILL.md` — a `grammar_p8` entry whose form is a general-purpose sentence pattern rather than an N2 headword (`理由説明(〜のは…からだ)`, `換言要約(〜つまり…ということだ)`) cannot be kept out of 400 lines of expository 読解 prose, so drawing one obliges the authoring stage to grep the drafted passages for the frame and re-word the hits.** State it as a step in the stage-3 handoff, not as a hope. This one resists full mechanisation — a cleft-reason sentence is not a "form" a regex can distinguish from ordinary prose in every frame — but the ≥2-occurrence count *is* mechanical once R2-F4 is fixed, so ship the count and leave the judgement to the author. |

**Effect on the loop.** R2-F1/F2/F3 block this paper. R2-F3's `RULE-MISSING`
half and R2-F4's `GATE-WRONG` **block the next generation run** — R2-F3 is the
rule that would have stopped the fix pass from writing these two items in the
first place, and R2-F4 means every 問題8 exposure result on every paper on disk
is currently unevidenced. Both must be applied, or explicitly rejected with a
reason, before a new test is authored.

**Note on scope.** This round found **3 paper findings** (R2-F1, R2-F2, R2-F3;
R2-F4 is tooling and R2-F5 is a consequence of it). That is at the boundary of
`jlpt-test-generation`'s stage-4 loop rule, which permits a direct fix without
re-review at ≤3 findings. **I recommend against taking it here**: the last pass
that re-authored two 問題8 items under that allowance is what produced R2-F1 and
R2-F2, and the repair for both is a re-cut of the item's card structure — the
same operation that failed. Re-review 問題8 in full after the fix.

---

## 6. Coverage statement

| Step | Ran on | Result |
|---|---|---|
| 0 Blind solve | `qa/20260819_1/keyless.md` (101 items + 4 例), before any key or the round-1 report | 101/101, 0 discrepancies |
| 1 Key-by-key proof | all 101, from `言語知識・読解.md` + `聴解.md` + `聴解スクリプト.txt` | deciding line quoted per item in §3 |
| 2 Distractor elimination | all 101 × 3 wrong options (2 for 聴解問題4) | an impossibility named per wrong option; the six changed items re-derived from scratch |
| 2b Plausibility | 問題1–6 option sets (functional category written per set), 聴解問題1/2/5 grounding (every 消去方法 quote grepped in the script) | all grounded; no fabricated 聴解 distractor |
| 2.5 Level band | 問題1–6 keys vs `pools.json` provenance + the 31-sitting archive; 問題7–9 vs `level_band_grammar.txt` (gate ok) | 演説 (1 archive booklet) and 出荷 both sit mid-N2; nothing TOO_HARD or TOO_EASY; the 訓/音 mix is now 2/3 |
| 3 Mechanical reads | 問題7 stem distribution (all three numbers computed), 問題8 permutation read (all 5 items × 24 orderings), 問題9 categories, 注N counts, 中略, ruby, marked spans, key-length rates | R2-F1/F2/F3 found here |
| 4 聴解 structure | 構成表 read as columns first, then re-derived against the script; first/last spoken line per item; question types; 例 ×4; `SPEAKER_MAP` per label | correct apart from obs. 2 |
| 5 Topic table | 13 読解 surfaces + 29 聴解 rows, this test vs 20260818_1 vs 20260817_3 | below |
| 6 Provenance | `test_spec.json` ↔ `logs/ledger.json` ↔ `pools.json` ↔ `logs/topics.json`; 101 answer positions; verbatim sweeps | clean |
| 6.5 Root cause | 5 findings, grouped to 3 causes | §5 |

**Topic table — headline set, rebuilt from the SHIPPED content and diffed:**

| slot | 20260819_1 (from the shipped text) | 20260818_1 | 20260817_3 |
|---|---|---|---|
| 問題9 | 非常持ち出し袋を持ち出す分と残す分に分ける — **防災** | デジタル化 | 消費・経済 |
| 問題12 A/B | 在宅勤務の成果をどう測るか — **働き方** | 交通 | 環境 |
| 問題13 | 方言の記録と継承は別の作業 — **文化・伝統** | 住まい | 医療・福祉 |
| 問題14 | みなと市まちなか共通観覧券 — **旅行・観光** | 行政・手続き | スポーツ・余暇 |
| 聴解問題5-1番 | 開店カフェの品書き（サンドイッチに決定） — **食** | 地域活性化 | 人間関係 |
| 聴解問題5-2番 | 大学見学会で午後の催しを別々に選ぶ — **教育** | メディア・情報 | 防災 |

Intersection with the immediately previous paper: **∅** (rule 4's zero-tolerance
clause). Intersection with the paper-before-last: **{防災}, exactly one** — the
maximum rule 4 allows; the subjects share nothing (何をどれだけ背負えるか vs
訓練でどのプログラムに出るか). Each theme was re-tagged from the shipped passage,
not read off `test_spec.json`, and every tag matched.

**In-paper repeats: none.** The closest adjacency is 問題9 (非常持ち出し袋)
beside 問題11(1) (災害の第一報) — the same domain, no shared fact, number or
condition. 問題10(3) (フリマ) and 問題14 (共通券) are both lookup surfaces with
fully disjoint conditions. No two 聴解 items run the same errand. 問題14's
decisive tokens (800/1,200/600円, 月火水の休館日, 十名以上, 三日前, 別に800円)
appear nowhere in `聴解スクリプト.txt`; the only shared token is 「火曜」, which
decides nothing on either side.

**Closing-move column (13 essay surfaces, read against `dokkai.md`'s six
shapes, from the last two sentences of each):** 反論応答 2 (問題10(1), 問題11(1))
／ 意外な観察 1–2 (問題10(2), and 問題11(4) depending on the read) ／ 説明 2–3
(問題10(4), 問題13, and 問題11(4)) ／ 主張 2 (問題10(5), 問題12A) ／ 条件提示 2
(問題11(2), 問題12B) ／ 随筆 1 (問題11(3)); 問題10(3) and 問題14 are 実用文,
outside the taxonomy. Compliant on the 意外な観察 reading, one over the cap on
the 説明 reading — see obs. 7. Sentence templates: two finals share the
not-A-but-B skeleton, at the cap. **The keys do not inherit the closing** — the
20 読解 keys split across mechanism / fact-retrieval / rule-lookup / method /
thesis, with no human-attitude-beside-strawmen monoculture.

**Provenance.** `test_spec.json` and `logs/ledger.json` agree **field for field**
across all 11 item categories, `seed` (`66485076` + 1 category reroll + 13
`--reroll-one`s, including the four this round was asked to verify) and
`pools_sha` (`aadf23081392`, matching the live pool). No `harvest_sha`. All 101
`answer_positions` match the printed keys. Every 問題1/2/4/8 target and every
聴解 scenario resolves to a `pools.json` entry (gate: 22 items). Artifact
freshness: `聴解スクリプト.txt` 11:19:47 → `聴解.mp3`/`聴解_チャプター.json`
11:22:19 (`script_sha` = `b856e2fc0de8` = current) → `言語知識・読解.md` 13:40:48
→ all three HTML 13:41:10. Nothing built from superseded text. 20-character
n-gram sweep of the six changed strings against all 31 archive booklets/scripts
and all 13 other tests: **0 hits**.

**`make check`:** exit 0, "All checks passed (30 skipped), **138** warning(s)".
**No WARN names `20260819_1`** — grep-verified over the full 2617-line output;
the only line mentioning this id is `pools_sha replayability`, whose actual
mismatch is `20260818_1`'s stamp going stale from F5's legitimate pool repair,
which that check's own docstring names as expected and never fails. The paper's
own section carries 98 `ok` and 2 `skip`: `詳細解説.json` and its translations do
not exist yet, which is correct ordering (`make model-answer` is the post-QA
step). The earlier round's two errand-rotation skips are gone; the 138 − 124
delta is fully accounted for above and no verdict changed. Every remaining WARN
belongs to a pre-rule grandfathered id or to the two `pools.json` health WARNs
(errand-key clusters, 表外 glyphs), neither of which touches this paper's draw.

---

## 7. Skips

- **`tests/imported-*` comparison** (option-set and verbatim reuse against
  imported papers): no `tests/imported-*` directory exists in this repository —
  verified, not assumed. The 31-sitting archive was swept instead, at
  20-character granularity, over both booklet and script.
- **`模範解答.html` / `詳細解説.json` ↔ 問題冊子 option sync:** neither file
  exists; `make model-answer` is the post-QA step (`AGENTS.md` §5) and the gate
  skips the sync check for the same reason. **This is now load-bearing:** R2-F1
  and R2-F2 will change 問題8-43 and 問題8-47's options, so the model answer must
  be generated only after the round-3 re-review.
- **Shin Kanzen / Soumatome page images for the two new 問題1 keys:** I did not
  open the scanned PDFs for 演説 and 出荷. Both are `pools.json` `kanji_reading`
  entries, and per `AGENTS.md` §3 those two textbook sets are that pool's *only*
  authority, so pool membership **is** the textbook attestation; 演説 is
  additionally attested in one archive booklet. I used that branch plus the
  archive, not the page-image branch — stated per `moji-goi.md`'s
  author-diligence procedure.
- **Whether `20260810_2` 問題8-45 (the second instance of R2-F1's class) should
  be repaired:** out of scope for this test's review. It is named in the
  recurrence count and in the proposed `illegal_legs()` founding-case run, and
  it is a decision about that paper.
- **Nothing was fixed.** Per this skill's boundary rule the reviewer proposes;
  §4 is the work list and §5 goes to whoever touches the skills next.

---

**QA: FAIL (5 findings, 2 automatic)** — 問題8-43 and 問題8-47 must be re-cut,
the 「を→他動詞→隣接」 leg removed from all four 解説 that print it, and the whole
of 問題8 re-reviewed afterwards. `聴解` is genuinely untouched (both shas match
round 1's byte for byte) and needs no re-read beyond what §3 records.

---

## 8. Fix-pass disposition (2026-08-20, round-2 findings applied)

Written by the fix pass, not the reviewer. Everything above this heading is
unchanged. Read in full before the first other tool call:
`AGENTS.md`, `jlpt-test-generation/SKILL.md`, `question-authoring/SKILL.md` +
`references/bunpou.md`, `exam-blueprint/SKILL.md`, `tools/verify_scramble.py`,
this report, `tests/20260819_1/_sections/RESUME.md`, and (for R2-F5)
`references/dokkai.md` §"Thirteen surfaces, thirteen different essays".

### 8.1 Findings

| # | Verdict | What was done |
|---|---|---|
| **R2-F1** 問題8-43 | **APPLIED — re-cut** | The を-object 「畑に出る日を」 moved into the STEM; the four cards are now two lexically-chained blocks. Stem: 「祖父は、周りの農家が新しい道具に頼るようになった今も、畑に出る日を＿＿ ＿＿ ★ ＿＿。」 Cards `1.そうだ / 2.決めている / 3.長年の経験に / 4.基づいて`; word order `3→4→**2**→1`, ★=**2** = `answer_positions`. The drawn form `〜に基づいて` is untouched — **no reroll**, per the brief. |
| **R2-F2** 問題8-47 | **APPLIED — re-cut** | The を-object 「客の感じ方を」 moved into the STEM; the predicate split at a forced junction. Stem: 「同じ料理でも店で食べるとおいしく感じられるのは、客の感じ方を＿＿ ＿＿ ★ ＿＿。」 Cards `1.からだ / 2.変えている / 3.皿の色や明るさも / 4.味だけでなく`; word order `4→3→**2**→1`, ★=**2** = `answer_positions`. Drawn form `理由説明(〜のは…からだ)` untouched — no reroll. |
| **R2-F3** 4 of 5 解説 | **APPLIED — all four, plus both root-cause repairs** | The leg 「『Xを』の『を』は他動詞を要求し…連続した塊になる」 is gone from 43/44/45/47 (43 and 47 have wholly new proofs; 44 and 45 keep their word order and get a valid leg — see §8.3). `bunpou.md` §問題8 gained the third illegal leg verbatim **and** a new preceding section, "At most ONE card may be a free co-argument of the final predicate". `verify_scramble.py::illegal_legs()` gained the third detector. |
| **R2-F4** `check_key_grammar_exposure` | **APPLIED** | The local `re.sub(r"[（(].*?[）)]", …)` is deleted. The check now imports `sample_items` at module scope (`SAMPLE_ITEMS`) and reads the form through the sampler's own extraction, plus a copula normaliser. See §8.4 for the founding-case measurement and the 14-paper re-run. |
| **R2-F5** 問題10(1)/問題11(3) | **APPLIED — both re-worded, blueprint half applied** | Neither cleft-reason sentence survives, so the count is **0**, not 1. `exam-blueprint/SKILL.md` gained §"A `grammar_p8` draw whose form is a general-purpose sentence pattern obliges a prose grep". |

Nothing was rejected among the five findings, and every row of §5's root-cause
table was applied.

### 8.2 問題8 re-read IN FULL — the new construction rule, per item

The rule authored into `bunpou.md`: **at most ONE card may be a free
co-argument of the final predicate**; a card's position is *not* free when it
is fixed by (1) a 連体修飾 head, (2) a quotative 「と」, (3) a subcategorised
particle, or (4) a fixed 呼応 template that lexically orders its halves. All
five items were audited against it, not only the two that were broken.

| item | final predicate | cards that are its dependents | what fixes each | free co-arguments | verdict |
|---|---|---|---|---|---|
| **43** (re-cut) | 決めている | 「長年の経験に」 (via 基づいて) | source 3: 「に→基づいて」 subcategorises the bare 「に」; 「そうだ」 subcategorises a 普通形, so ［決めている→そうだ］ is forced; the を-object is in the STEM | **0** | unique — two blocks, and the block ending in テ形 cannot be final |
| **44** | 身内にいなかった | 「受け継ぐ人が」 (subject) | source 1: 「あの技術を」 is the object INSIDE the 連体修飾 clause headed by 「受け継ぐ人」, so it cannot leave it; 「つまり」 is a connective, blank-initial only; the printed 「という」 demands a 普通形 | **1** (受け継ぐ人が) | unique, unchanged |
| **45** | 断らねばならない | 「受け付けを」 (object) | 「申請書に不備が」 is bound inside the 「〜場合は」 conditional clause (existence predicate あった); 「受け付けを」 is the single free co-argument | **1** (受け付けを) | unique, unchanged — see §8.3 for the replacement leg |
| **46** | ない | 「ときほど」, 「心細いものは」 | source 4: 「AほどBはない」 orders BOTH halves lexically; source 3 (形式名詞 「とき」's 連体修飾 slot) fixes ［体を壊した→ときほど］ | **0** (both halves template-fixed) | unique, unchanged |
| **47** (re-cut) | 変えている | 「味だけでなく…皿の色や明るさも」 (one focus block) | source 4: 「AだけでなくBも」 orders the block; 「から」 subcategorises a 普通形, so ［変えている→からだ］ is forced; the を-object is in the STEM | **1** (the focus block) | unique — the reverse order strands 「も」 |

Register mix is unchanged by the re-cuts (formal/institutional 1 = 45;
personal/casual 2 = 43, 46), no bare-adverb card was introduced, and both
re-cut items still realise their drawn `grammar_p8` targets — `make check`
prints `問題8 items realize their drawn grammar_p8 targets (5 drawn) ok`.
Calibration after the re-cut: 43 option sum 18 (each 3/5/6/4), assembled 52;
47 option sum 22 (each 3/5/8/6), assembled 53 — both inside `bunpou.md`'s
16–29 / ≥2 options ≥5 / ≥45 bands. 43's longest card is 6 rather than the soft
「usually ≥7」 target; that is a calibration preference, and
`official_calibration.md` §9 records that 51 % of official options are under 5
chars.

### 8.3 The legs that replaced the illegal one

- **44** — 「『受け継ぐ人が』は連体修飾を受ける名詞「人」を含み、その修飾節の動詞
  「受け継ぐ」の目的語は節の内部にしか置けない…（隣接の根拠は連体修飾節の内側という
  位置であって、他動詞であること自体ではない）」. The conclusion the old leg
  reached was right; the reason now matches the structure.
- **45** — the topic/は-stacking argument the reviewer supplied: 「窓口の担当者は」
  already occupies the topic slot, so fronting a bare を-object before a second
  は-marked conditional puts three pre-verbal phrases in a row.
- **43 / 47** — wholly new proofs (伝聞「そうだ」の接続要求／「から」の普通形要求 and
  「AだけでなくBも」の語順), each of which also records that the を-object was moved
  into the stem *because* two free co-arguments do not order.

### 8.4 R2-F4 — the repaired check, measured

`tools/check_consistency.py`:

- module scope now loads the sampler once as `SAMPLE_ITEMS` (the
  `check_mondai1_reading_type_mix` precedent, which took it as an argument —
  `check_key_grammar_exposure` has no such seam), and `check_specs`' local
  `sample = load(…)` reuses that same object;
- `sample_items.py` gained **`grammar_form_parts(entry)`** — the ordered,
  label-stripped chunks — and `grammar_form_tokens()` is now that list filtered
  to `≥GRAMMAR_FORM_MIN` and namespaced, so the sampler's own behaviour is
  bit-identical and the two extractions cannot diverge;
- the 問題8 branch matches the **ordered skeleton inside one sentence**
  (`[^。]{0,80}`), not a bare chunk. This is load-bearing: counting tokens would
  make `〜ほど〜はない` fire on every 「〜ではない。」 and `例示指示(〜例えば…)` on every
  「例えば」. The report's own expected string, 「のは…からだ」, IS the skeleton;
- `_copula_norm()` folds `である`→`だ`, giving からだ≡からである and のだ≡のである.

**Founding case, run against the PRE-FIX revision of this paper** (the file was
copied aside before any edit, the repaired check run on it, then restored — sha
verified identical afterwards):

```
FAIL  20260819_1: no 問題7/8/9 keyed form appears more than 1× in the 問題10-14
      prose — 問題8 target「のは…からだ」×2 (pool entry: 理由説明(〜のは…からだ))
```

and on the shipped revision the same line reads `ok`.

**Re-run over all 14 papers.** Ids whose 問題8 branch produces a line at all:

| id | line | status |
|---|---|---|
| 20260810_1 | `問題8 target「一方」×3 (pool entry: 対比表現(〜一方…だ))` | **GAINS a line** — the label bug measured it as 「対比表現」 |
| 20260807_1 | `問題8 target「からといって」×2` | unchanged (entry carries no 類型 label) |
| 20260813_2 | `問題8 target「として」×10` | unchanged (same reason) |
| the other 11 | — | no 問題8 line |

`20260810_1` is the only id that gains a line and it is **already** in
`KEY_EXPOSURE_GRANDFATHERED`, so the repair adds no grandfathered id and
re-classifies no shipped paper. The measurement and this table are pasted into
the check's own docstring.

**Founding-case run for the `illegal_legs()` detector**, before it was accepted:

- pre-fix `20260819_1`: fires on **43, 44, 45 and 47**, and NOT on 46 — whose
  legs (「『が』は存在を表す述語を要求し…」/「『は』は述語を要求し…」) are legal and use
  the same 「〜を要求し…塊になる」 wording. That is why the pattern is anchored on
  「他動詞」 rather than on the report's proposed
  `を.{0,6}要求し.{0,20}連続した塊` window, which would have false-fired on 45's
  and 46's valid が/は legs.
- **44 fires with a different message, not an exemption.** §5 proposed "FAIL
  unless that card's partner is a 連体修飾 head or a quotative" *and* required
  the run to fire on 44, whose partner 「受け継ぐ人が」 IS a 連体修飾 head. The two
  cannot both hold as suppression, so the exemption is expressed as the
  MESSAGE ("the CONCLUSION holds — restate the adjacency from the 連体修飾
  head"), and the item still FAILs. A proof rewritten onto the real source no
  longer matches the regex at all, which is the intended way out.
- `20260810_2` 問題8-45 — **the detector cannot fire and this is stated, not
  hidden**: that item's 解説 is a bare word-order line printing no uniqueness
  proof at all, so there is no leg text to match. `missing_proof()` already
  FAILs it (`ARTIFACT: MISSING — no last-slot proof … cards never named`),
  verified by running the tool on that paper. It carries the ITEM class (two
  free co-arguments), which is now a written construction rule in `bunpou.md`;
  the structural half is not string-decidable and no detector claims it.
  Repairing `20260810_2` remains out of scope, as §7 says.
- after the re-cut, `make verify-scramble 20260819_1` prints **zero**
  `PROOF LEG INVALID` lines and exits 0; sweeping the detector over all 14
  papers on disk produces zero hits, so no shipped paper is re-classified.

### 8.5 R2-F5 — the two re-wordings

| where | was | is |
|---|---|---|
| 問題10(1) | 「それでも刈り残しを続けた**のは**、丈の高い植生（注1）が、川と林とをつなぐ回廊（注2）になっている**からである**。」 | 「それでも市は刈り残しを続けている。丈の高い植生（注1）が、川と林とをつなぐ回廊（注2）になっている**ためである**。」 |
| 問題11(3) | 「開く前に身構えた**のは**、財産の話が並んでいるだろうと思った**からである**。」 | 「開く前は、財産の話が並んでいるのだろうと身構えた。」 |

Occurrences of the tested frame in the 読解 prose: **2 → 0** (one survivor
would have been legal; zero is what the re-wording produced, and neither
survivor is in the cleft-reason frame because neither survives).

`dokkai.md`'s thirteen-final-sentence rule was re-read before the rewrite and
is untouched by it: **neither sentence is its passage's final sentence.**
問題10(1) still ends 「見た目の乱れを指摘する声は今も届くが、…三倍に上る。」 and
問題11(3) still ends 「…母が誰に向けて書いたのかは、今なら分かる気がする。」 — so no
template's count moved, no shape assignment moved (問題10(1) stays 反論応答,
問題11(3) stays 随筆), and the thirteen-final-sentence column is byte-identical.
Item 52's key (3) still reads off the same two facts and its 解説 quote was
re-pasted to the new wording (Item integrity #19); items 61 and 62 never
depended on the 問題11(3) sentence.

### 8.6 Minor observations — ruled

| # | Ruling | Reason / what changed |
|---|---|---|
| 1 `topics.json` notes arithmetic | **APPLIED** | 「twelve essay surfaces」 → **eleven** (13 surfaces − 問題10(3) お知らせ − 問題14 チラシ; 問題12 A/B are one surface), which is what 5×2+1 says. The 「A ではなく B」 sentence now reports the **hand** count of 2 (問題11(1), 問題12A — at `dokkai.md`'s cap, not over it) and says explicitly that the gate's marker-family proxy 0 settles nothing. |
| 2 構成表 問題3 talk lengths | **APPLIED** | `聴解.md` now prints 「1番=306／2番=334／3番=311／4番=333／5番=337」, matching `make check`'s own `p3_talk_chars`. Booklet + sheet rebuilt. `聴解スクリプト.txt` and `聴解.mp3` are untouched, so no MP3 rebuild is due and both shas still match. |
| 3 「わずかに」 key at 21 / distractor at 23 | **REJECTED** | No rule caps 問題5 option reuse, and the two sightings are in different items with different targets. The only same-category replacements at 23 (多少/やや) are N3-band degree adverbs, so the swap would trade a documented-legal reuse for a weaker distractor — the sniff test (`question-authoring`) is the binding rule here and 「わずかに」 passes it. Recorded, unchanged. |
| 4 問題7 5-kana form reuse = 2 | **REJECTED (reviewer's own ruling adopted)** | Both pairs are two distinct Shin Kanzen headwords sharing a tail, the shipped constant is `P7_FORM_REUSE_MAX = 2`, and `bunpou.md` forbids repairing this by shortening the n-gram. The 「ことはない」 pair is recorded as the one to remove first when the constant tightens to 1. |
| 5 「無理がある」 keyed at 50 and inside the key at 69 | **APPLIED** | 問題13-69 option 2 (the key): 「…同じ名前で呼んできたことに無理がある」 → 「…一つの言葉でまとめて呼ぶことはできない」. Still the passage's thesis (「だが、要るものが違う」 + the closing), still a paraphrase rather than a lift (it now shares LESS text with the passage than the old wording), option lengths 32/33/29/29 → max/min 1.14, inside the ≤1.30 band. 問題9-50 is untouched. |
| 6 問題6-27 option 2 | **REJECTED** | 「話が切れる」 is a misuse, not a rarer valid use (the idiom is 話が途切れる), so Item integrity #16 is satisfied; the key 「しょうゆが切れて」 is unambiguous and the reviewer found no two-answer risk. Recorded for calibration, as the reviewer asked. |
| 7 問題11(4) closing-move label | **APPLIED — ruled and recorded** | The label is **意外な観察**, decided by `dokkai.md`'s own definition rather than by feel: 意外な観察 *is* 「an unexpected fact, then its cause」, and the passage marks the unexpected fact (ところが、①看板を高く掲げた家ほど短命だった) before explaining it. 説明 is the shape that explains a mechanism with no unexpected-fact frame. So 説明 stays at 2 (問題10(4), 問題13) and 意外な観察 at 2 — the cap holds on the only defensible reading, and the ruling is now written into `logs/topics.json` `notes` so the next reader does not re-open it. |
| 8 agricultural register / fourth food surface | **REJECTED (recorded)** | No rule applies — neither 問題1-4 nor 問題8-43 is a topic-table surface, and the four food/restaurant 聴解 surfaces are on different subjects (the theme cap for listening is 5). 問題8-43's stem is unchanged by the re-cut, so the observation neither grew nor shrank. Noted here so it is not re-discovered as new. |

### 8.7 Commands run, in order

```
make autofix 20260819_1        # ALL CHECKS CLEAN
make lint-draft 20260819_1     # ALL CHECKS CLEAN
make verify-scramble 20260819_1 # ARTIFACT: ok ×5, 0 PROOF LEG INVALID, exit 0
make booklet 20260819_1        # both HTML rebuilt
make sheet 20260819_1          # 101 items
make check                     # exit 0 — "All checks passed (30 skipped), 138 warning(s)"
```

`make check` was read line by line. **Zero FAIL.** The warning total is
**138 — identical to round 1 and round 2**, i.e. no verdict moved anywhere on
disk, and **no WARN or FAIL names `20260819_1`** (its own section: 96 `ok`,
4 `skip`). The four skips are the two `詳細解説.json` ones (correct ordering —
`make model-answer` is post-QA) and the two errand-rotation ones (`0 keyed
draw(s)`); the latter two were verified to be **unchanged by this pass** by
re-running the pre-edit code path, so they are not a regression from the
`SAMPLE_ITEMS` refactor. `pools_sha` replayability remains the only WARN line
mentioning this id, and its actual mismatch is `20260818_1`'s stamp, which the
check's own docstring names as expected.

### 8.8 Files written

- `tests/20260819_1/言語知識・読解.md` — 問題8-43/47 re-cut, four 解説 rewritten,
  問題10(1)/問題11(3) prose, 問題13-69 option 2, 問題10-52 解説 quote.
- `tests/20260819_1/聴解.md` — 構成表 問題3 talk lengths (obs. 2).
- `tests/20260819_1/{言語知識・読解,聴解,解答}.html` — rebuilt from those sources.
- `.agents/question-authoring/references/bunpou.md` — new §"At most ONE card may
  be a free co-argument of the final predicate"; third illegal leg; "two legs" →
  "three legs".
- `.agents/exam-blueprint/SKILL.md` — new §"A `grammar_p8` draw whose form is a
  general-purpose sentence pattern obliges a prose grep".
- `.agents/exam-blueprint/scripts/sample_items.py` — `grammar_form_parts()`;
  `grammar_form_tokens()` rebuilt on it (output unchanged).
- `tools/verify_scramble.py` — third `illegal_legs()` detector + founding cases.
- `tools/check_consistency.py` — `SAMPLE_ITEMS`, `KEY_EXPOSURE_GAP`,
  `_copula_norm()`, repaired 問題8 branch, docstring measurement.
- `logs/topics.json` — `20260819_1` `notes` (obs. 1, obs. 7, round-2 record).
- `qa/qa-report-20260819_1-round2.md` — this section only.
- `tests/20260819_1/_sections/RESUME.md` — resume point.

### 8.9 Skipped, and why

- **No `make sample` / `--reroll` / `--reroll-one` was run.** Both automatic
  fails were item-construction defects, and the brief (and `bunpou.md`'s new
  rule) require the drawn form to stay: the cards are the author's, the form is
  the contract. `test_spec.json` and `logs/ledger.json` are therefore untouched
  and the seed expression is unchanged.
- **`make mp3` not run** — `聴解スクリプト.txt` is unchanged; only the post-key
  構成表 line inside `聴解.md` moved, so `script_sha`/`pacing_sha` still match.
- **`make model-answer` / `make scaffold-explanations` / translations not run** —
  Stage 5 is post-`QA: PASS`, and 問題8-43/47's options and 問題13-69's key text
  moved in this pass, which is exactly the desync §7 warns about.
- **`20260810_2` 問題8-45 not repaired** — out of scope per §7; it is named in
  `bunpou.md`'s new rule and in the detector's docstring instead.
- **The paper was not re-blind-solved by this pass**, and must not be: §5's
  scope note recommends against the ≤3-finding direct-fix allowance here, so
  **問題8 needs a round-3 fresh-eyes re-review in full** — a context that
  authored nothing, including nothing in this section.
