# QA Report — 20260828_2 (ROUND 2, independent fresh-eyes re-review)

**Reviewed revision** (sha1[:12]... full sha1 shown; unchanged from start to end of this review):
- `言語知識・読解.md` = `12c51bbbb54bf80c6bd17e17390690c1f63ba0b4`
- `聴解.md` = `808314f9cc59ebb3662226a020a6dd8bedb92655`
- `聴解スクリプト.txt` = `37d91f05c34c764bf6a210ac923108449e948ec2`

**Timestamp**: 2026-08-28 (session date), review conducted in one continuous fresh-eyes pass, no prior context on this test's authoring or on `qa-report-20260828_2.md`'s findings (per instruction, that file's content was not read — only used at the very end to confirm the reviewed revision was current, see Coverage).

---

## QA: PASS (1 finding, already fixed before the content review began; 0 remaining, 0 automatic)

The one finding was a gate-blocking mechanical formatting defect (missing bold markup), found and repaired before the content review started, so the entry condition ("`make check` green") could be genuinely met rather than assumed. After that fix, all of steps 0–6 ran clean: the full 101-item blind solve matched the shipped key on 100/101 items (the one mismatch is reviewer error, not a paper defect, see below), the two blind-strategy passes over 問題10–13 both score well under the 45% automatic-fail bar, every distractor in every checked item is grounded and eliminable for a stated reason, no off-level (N1/N3-or-easier) vocabulary key was found, the 問題8 zero-anaphora double-bind class (`qa-report-20260827_2.md` F1's defect) was hand-checked on all five items and not reproduced, the 聴解問題5-1番/5-2番 reroll and 聴解問題3-1番/2番 re-slot are independently re-derivable as genuinely clean against `logs/topics.json`'s 1-back/2-back headline sets, and the disclosed WARNs (kanji density, gloss floor, 聴解 key length, 問題1/2 script-vocabulary overlap, absolute-quantifier candidates) are honestly WARN-level under the gate's own thresholds, not mis-classified FAILs.

---

## 0. Entry condition — `make check` was NOT actually green at the start of this round

Before any content review, `python3 tools/check_consistency.py` was run repo-wide and returned:

```
FAILED — 2 problem(s):
  - 言語知識・読解.md: passage numbered markers match questions 1-to-1: section 11: passage has ['①'] vs questions have []
  - 言語知識・読解.md: every marked passage span is quoted by a stem: ①「それ…」
```

Both trace to the same one-character defect: `tests/20260828_2/言語知識・読解.md` line 300 (問題11(3) passage) correctly bolds `①**それ**`, but line 311 (item 62's stem) printed the marker unbolded — `**62** ①それは何を指すか` instead of `**62** ①**それ**は何を指すか`. This is purely a markup-compliance defect (`dokkai.md` §"Marked-span quoting" convention, confirmed against three other papers' analogous stems, e.g. `tests/20260827_2/言語知識・読解.md:317`); it does not touch content, wording, or the key. Fixed with a single edit, `言語知識・読解.html`/`解答.html` rebuilt (`make booklet`, `make sheet`), and `make check` re-run: **0 FAIL, 5 WARN** naming this test — matching the task briefing exactly. This is **Finding F0** below (already fixed).

This means the "make check currently reports 0 FAIL" premise handed to this round was not actually true at the moment review began — flagged explicitly per AGENTS.md §0.5/§0.7 rather than silently patched and left unmentioned.

---

## 1. Blind-solve diff

Solved from `qa/20260828_2/keyless.md` (source shas confirmed matching, header above) — all 101 items answered before opening any keyed file, per `exam-qa-review` §"Ground rules". Diffed against the shipped key tables in `言語知識・読解.md` / `聴解.md`.

**Result: 100/101 match.** One mismatch:

- **聴解問題1-2番** (家具店, ソファー配達変更): my blind answer was 3 (配達員に庭から運ぶよう頼む); shipped key is 4 (希望の曜日に配達し直してもらう). **Resolved as reviewer error.** Deciding quote: 「男:わかりました。じゃあ、日にちを直してもらえますか。店員:はい、日曜日に変更しておきます。」— this exchange is the immediate, confirmed outcome of the call (「この後まず」), while the garden-carry request is explicitly deferred to delivery day itself (「それは配達の方に直接言ってもらえれば、当日対応できますよ」— a later, conditional action, not the first next step). Not a finding.

No other mismatches — every one of 問題1–14 (71 items) and 聴解問題1–5 (30 items) was answered correctly on the first, keyless pass.

## Blind strategy passes (問題10–13, 18 items, 52–69)

Computed programmatically (character-bigram overlap with own passage; second-longest option by JP character count) and compared to the shipped key:

- **Strategy 1 (second-longest option)**: 6/18 = **33.3%** match rate.
- **Strategy 2 (highest passage-bigram overlap)**: 7/18 = **38.9%** match rate.

Both are well under the 45% automatic-fail bar (official baselines are 32.8%/24.6%; ours runs a little hot on strategy 2 but not into fail territory — noted as a mild elevation, not a finding since it clears the bar with margin).

---

## 2. Per-question walkthrough (all 101 items)

判定 legend: OK = verified correct and unambiguous with a deciding quote; 要修正 = needs a fix; 自動不合格 = automatic fail.

### 問題1 (漢字読み, 1–5)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 1 | 2 | OK | 「彼の説明はいかにも頼りない印象だった」— たよりない is the only reading matching 頼りない; 2×2 kanji-reading matrix in 解説 (頼/嫌型) confirmed real-word distractors. |
| 2 | 4 | OK | 要因(よういん); distractors ようにん/ゆういん/ゆうにん are systematic on-reading permutations, all fail as real readings of 要因. |
| 3 | 3 | OK | 破片(はへん); 2×2 matrix 火/河 × 口/溝 analog confirmed by 解説. |
| 4 | 3 | OK | 突き当たり(つきあたり); all 4 options share the printed okurigana たり (repaired in Stage-3 per `logs/topics.json` FIX 4 — independently confirmed, all four are real words: ものたりない-class check n/a here, これ item's own family こころあたり/さしあたり/つきあたり/ばちあたり all real). |
| 5 | 4 | OK | 借金(しゃっきん); sokuon+rendaku reading transformation is the tested point, standard N2 問題1 shape. |

### 問題2 (表記, 6–10)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 6 | 1 | OK | けいこ→稽古; 2×2 matrix 稽/景×古/戸 confirmed (`matrix_helper.py validate` PASS per 解説). |
| 7 | 2 | OK | てっかい→撤回; 2×2 matrix 撤/徹×回/会 confirmed. |
| 8 | 1 | OK | 天気予報を「みる」→見る(一般); 観る/診る/看る correctly excluded by domain (鑑賞/診察/看護 vs. general watching). `matrix_helper.py` FAILs this pair on a documented tool limitation (表外訓 not in its reading table) — independently sanity-checked against `moji-goi.md`'s own worked example (険しい family), which fails identically; not an authoring defect. |
| 9 | 4 | OK | 火山のかこう→火口; 河口 (same-sound different word) correctly excluded by context (火山・煙, not a river mouth). |
| 10 | 3 | OK | 決勝で「やぶれました」→敗れました(lost a match); 破れました(torn) excluded by context (決勝で = in the final, competitive sense); 波/皮 are visual-similarity pseudo-kanji, not real words. |

### 問題3 (語形成, 11–13)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 11 | 4 | OK | 少数; 「代表的とは言えない」excludes 総/全/定 (all imply completeness/fixed count, contradicting "not representative"). |
| 12 | 3 | OK | 若者層; 族/派/系 all real N2-level affixes but 層 (stratum, a demographic-breadth reading) is the only one natural with 若者+SNS spread. |
| 13 | 1 | OK | 偉ぶる; めく/がる/じみる are real affixes of the same family (問題3 does not require all four to attach — per `moji-goi.md`'s own official 教育観 precedent) but 偉ぶる is the standard idiom for "acting self-important." |

### 問題4 (文脈規定, 14–20)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 14 | 3 | OK | 揚げる(deep-fry); 「衣をつけた具材を高温の油で」+「表面がかりっと」uniquely selects 揚げる over 炒める/蒸す/茹でる. |
| 15 | 2 | OK | うながす(prompt); 「催促のメール」confirms prompting/urging sense, not 勧める(recommend)/誘う(invite)/迫る(press urgently, too strong). |
| 16 | 4 | OK | 犯人扱い; 「現場に居合わせただけなのに」(merely present at the scene) is the classic setup for being suspected as a culprit — 子供扱い/腫れ物扱い/厄介者扱い don't fit "merely present at a scene" framing. |
| 17 | 3 | OK | かじっていた(gnawing); 「まだ歯が生えそろっていないのに、硬いせんべいを懸命に」uniquely fits gnawing at something hard with insufficient teeth, over なめて/すすって/しゃぶって. |
| 18 | 2 | OK | 言い訳(excuses); 「しどろもどろに〜を並べた」is the fixed collocation 言い訳を並べる; 弁解/愚痴/泣き言 don't collocate with 並べる the same way. |
| 19 | 1 | OK | ぴったり(fits exactly); 「足のサイズに〜合っていて」is the standard collocation, over きっちり/しっくり/きっかり. |
| 20 | 4 | OK | 跡(residue mark); 解説: 「テープの跡は日常的な物理的な跡に使う定着表現」— 名残(emotional lingering)/痕跡(forensic-register)/面影(a person's remembered look) all excluded by register/domain mismatch, independently confirmed correct. |

### 問題5 (言い換え, 21–25)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 21 | 2 | OK | わりに→比較的; substitution test holds: 「比較的天気がいいです」. |
| 22 | 3 | OK | 衛生的だ→清潔だ; substitution holds. |
| 23 | 2 | OK | 相次いで→続々と; substitution holds. |
| 24 | 1 | OK | いざ(となると)→実際(となると); substitution holds — verified this personally during blind-solve as the trickiest item in the section; 解説's own substitution test confirms. |
| 25 | 3 | OK | かすかに→わずかに; substitution holds. |

### 問題6 (用法, 26–30)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 26 | 4 | OK | 憧れる: correct usage is admiration of an idealized target (職業); 解説 confirms 1/2/3 target non-idealizable objects (掃除機の性能/友人の点数/会社の規則), none an established collocation. |
| 27 | 3 | OK | 削減する: correct usage is 経費削減 (quantity/cost); 1/2/4 (会話/ストレス/病気) are not reducible-quantity objects for this verb. |
| 28 | 2 | OK | 物騒: correct usage is public-safety unease (夜道); 1/3/4 misuse it for manners/weather/speech-speed, none idiomatic. |
| 29 | 2 | OK | 横断する: correct usage is crossing a road; 1/3/4 (列に割り込む/一年間/意見) are not spatial-crossing objects. |
| 30 | 1 | OK | 臨時: correct usage is 臨時休業; 2/3/4 (性格/材料/体調) don't collocate with 臨時. |

### 問題7 (文法, 31–42)

All 12 items independently re-derived from the sentence logic during blind solve, and each cross-checked against the shipped 解説's own elimination reasoning (all present, all quote the deciding grammatical contrast — e.g. 34's 「にもまして」excluded because it needs a comparison BASIS, not two co-equal virtues; 41's 「とみえる」correctly distinguished from伝聞 「とのことだ」by direct-observation evidence). All OK, keys: 31=3, 32=2, 33=4, 34=4, 35=3, 36=1, 37=1, 38=2, 39=2, 40=2, 41=1, 42=3.

**Mechanical read (問題7 stem distribution, per `moji-goi.md`/`bunpou.md` three-number rule)**: gate reports "mean 42.0 in 36–52, 5 under 34 (need 2), spread 42 ≥ 25" — **ok**, clears all three bands (mean, floor-count, spread) independently confirmed against the gate output.

### 問題8 (文法並べ替え, 43–47)

| 項目 | 鍵(★) | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 43 | 1 | OK | 自分の目で選んだもの→でなければ→**品質への**→こだわりを曲げない. Only 1 of 24 orderings is grammatical (both bound pairs have only one valid relative order; reverse order ends in a dangling でなければ). |
| 44 | 1 | OK | 誰にでも操作が→分かるように→**画面の**→表示方法が見直された. |
| 45 | 4 | OK | 家族全員が→同意しない限りは→**引っ越しの**→話は進められない. |
| 46 | 4 | OK | 価格が手頃なばかりか→デザインも→**洗練されていると**→言われている. |
| 47 | 1 | OK | したがって→各部署の→**支出内容を**→見直す必要がある. |

**Zero-anaphora double-bind check (`qa-report-20260827_2.md` F1's defect class, hand-checked on all five since `verify_scramble.py`'s `free_unit_count()` cannot see it)**: two items carry a bare-が-ending card (44's 「誰にでも操作が」, 45's 「家族全員が」) that could in principle bind forward to the FINAL card's predicate instead of only the adjacent one. Checked both by hand: in 44, the final card (「表示方法が見直された」) already carries its own explicit が-subject (表示方法), which blocks 「誰にでも操作が」 from double-binding to it (no natural second subject slot, and 見直された is a plain passive with no agent-marking that fits が). In 45, the only alternative block-orderings either break the surrounding grammatical requirement (「引っ越しの」 must sit immediately before 「話」) or end the sentence on a non-terminal connective (「限りは」/「でなければ」), which the shipped 解説 already rules out — no second grammatical permutation exists. Neither item reproduces the defect; not a finding.

### 問題9 (cloze, 48–51)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 48 | 3 | OK | しかも (additive reinforcement, not ところが/たとえば/つまり); [論理接続] category. |
| 49 | 2 | OK | なわけだ (conclusive gloss); [文末モーダル] category. |
| 50 | 1 | OK | 見なしてしまう (mistakenly regard as); [内容推論] category. |
| 51 | 4 | OK | 主客転倒だ (means-and-ends reversed); [慣用・形式名詞] category. Note: this option was rewritten from an earlier draft (「本末転倒だ」) per `logs/topics.json`'s FIX 0, because that string was byte-identical to `20260827_2`'s own 問題9-51 CORRECT ANSWER at the same slot — independently confirmed this test's shipped text reads 「主客転倒だ」, not the collision string, so the repair is genuinely in place. |

All four blanks are in four **distinct** categories (論理接続/文末モーダル/内容推論/慣用・形式名詞), satisfying the "no two blanks share a category" rule; confirmed via the shipped 解説's own bracketed tags, cross-checked by independent reading.

### 問題10 (52–56, 5 short passages)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 52 | 3 | OK | 「同封の案内をご覧のうえ、来月末までに登録手続きを済ませてください」— option 3 restates the notice's purpose; option 1 falsely claims the old system stops (passage says 「従来の防災無線に加えて」, additive not replacing). |
| 53 | 2 | OK | 「対応できる言語は四つになります」+「第二土曜日の午前中にも開く」— matches option 2 exactly; option 1 falsely claims replacement of the old languages. |
| 54 | 4 | OK | 「最低賃金の上昇分より大きく賃上げをした企業ほど、若手社員が一年以内に辞めない割合が高かった」— direct correlation match. |
| 55 | 4 | OK | 「自分で選んだという感覚そのものが、最後までやり抜く力になっていた」— direct match; option 1 states the reverse of the finding. |
| 56 | 2 | OK | 「外からのしげきが、内側にねむっていた食文化を掘り起こす場合もある」— option 1 restates the POPULAR opinion the passage sets out to refute (「たしかに…しかし実際には違う動きもある」 structure), not the author's own view — the correct kind of trap, not an on-sight elimination. |

### 問題11 (57–64, 4 passages × 2)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 57 | 2 | OK | 「技術は、説明されて理解するものではありません。繰り返し手を動かし、失敗を重ねる中で、体に染み込ませていくものなのです」— direct match. |
| 58 | 3 | OK | 「この『体に染み込ませる』までの長い時間を…待てなくなっているからではないでしょうか」— direct match. |
| 59 | 3 | OK | 「入学前の家計状況だけを基準に支援の対象を決める…こうした学生を救えない」— direct match. |
| 60 | 4 | OK | 「在学中に家計が急変した学生を機動的に支える緊急支援制度こそが、学業継続を支える鍵ではないだろうか」— direct match. |
| 61 | 2 | OK | 「介護休業給付は、休業中の所得を一定割合まで補うことを目的とする。これに対し、この制度は、休業を取らずに働き方を変えられる権利を保障する」— direct match. |
| 62 | 4 | OK | 「①それは、軽度の介護であれば働き方を変えずに続けられる、という想定に基づく」— ①それ refers back to the exclusion of 要介護一・二 from the program, restated by option 4. (Bold-markup formatting fixed pre-review, see F0; content/key untouched.) |
| 63 | 2 | OK | 「掲示物を増やした駅より、外国語で個別に声をかける係員を配置した駅のほうが…苦情件数が少なかった」— direct match. |
| 64 | 1 | OK | 「この事実は、案内の量よりも、伝え方の質が重要であることを示しています」— direct match. |

### 問題12 (65–66, AB)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 65 | 2 | OK | A「地域ごとに代替の移動手段を整え…返納を選べる環境を用意することだ」/B「返納前から外出の予定を…相談する習慣があった人は…外出の回数があまり減っていなかった」— both converge on alternatives+connections mattering more than the return itself. |
| 66 | 3 | OK | A is a policy argument (制度のあり方), B is a personal family experience (具体的な工夫) — matches option 3's framing exactly. |

### 問題13 (67–69, 1 long passage)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 67 | 1 | OK | 「自治体の証明書一枚では、相続や税制上の権利までは保障されません」— direct match. |
| 68 | 4 | OK | 「勤務先には効力が及ばなかった」と答えた人が約三割— direct match. |
| 69 | 3 | OK | 「私は、この制度が抱える限界にも、もっと目を向ける必要があると考えます」— direct match. |

### 問題14 (70–71, 陶芸教室案内)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 70 | 3 | OK | 佐藤さん (小学2年生の娘と一緒に、初めて) → 親子コース: 「保護者もお子様と一緒に作品を作ります」— matches "一緒に体験したい"; 入門コース requires separate individual applications even if both attend. |
| 71 | 3 | OK | 2×(2,000円参加費+800円送料)=5,600円; matches option 3 exactly. Two constraints combined (入門コース fee + per-item delivery fee), satisfying 問題14's ≥2-constraint rule. |

### 聴解問題1 (例, 1–5番)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 例 | 3 | OK | 「案を紙に描いて、配って意見を聞きたいんだ」→「レイアウト案を描いて、印刷して配りましょうか」. |
| 1番 | 2 | OK | 「こちらの申込書に、お子さんの人数と連絡先を書いていただけますか」— matches; parking/参加費/先着順 all explicitly deferred/denied. |
| 2番 | 4 | OK | 「はい、日曜日に変更しておきます」— see Blind-solve diff above for the reviewer-error resolution on this item. |
| 3番 | 4 | OK | 「出欠のお返事を、今週金曜日までにいただきたいのですが」— matches; 担任先生/追加印刷/自転車 all explicitly excluded by the message itself. |
| 4番 | 4 | OK | 「徒歩・自転車の方は東側の通用口です」— matches directly; other 3 entrances explicitly assigned elsewhere. |
| 5番 | 3 | OK | 「牛肉を三百グラム追加でお願いします」— matches; 豚肉増量/配達時間短縮/クーポン all explicitly denied. |

### 聴解問題2 (例, 1–6番)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 例 | 1 | OK | 「壁紙が爪とぎ防止のタイプでないと…費用がかかる」→「そういう物件を優先して探してもらえますか」. |
| 1番 | 1 | OK | 「今年から役員も参加することになったらしくて」— matches; コピー枚数/会議室/資料の質 all explicitly resolved/denied. |
| 2番 | 1 | OK | 「現在地が画面にそのまま出るので、迷わずに行けるんですよ」+ repeated emphasis, all other 3 candidates explicitly denied by the driver himself ("あまり変わらない" ×2, "アプリが教えてくれるだけ"). |
| 3番 | 3 | OK | 「まず、指導教員の先生に相談して、許可をもらってください」— matches; 学費/届提出順/奨学金 all explicitly deferred or excluded. |
| 4番 | 1 | OK | 「賞味期限が一か月以上残っているものをお願いしています」+「配布までに期限が切れてしまう可能性がある」— matches; 量/種類/個人か団体か all explicitly ruled irrelevant by the clerk. |
| 5番 | 3 | OK | 「楽しみにしてたのに」+「とりあえず、夜の回で考えてみます」— matches the "残念だが検討中" framing; other 3 readings (strong complaint / eager / lost interest) all contradicted by the actual tone. |
| 6番 | 1 | OK | 「何度もいらっしゃるなら、通常の入園券よりずっとお得になります」— the clerk's own closing/summary line; 2.5回 (not 5回)/無料イベント/通年販売 (not限定) all explicitly stated, excluding options 2–4. |

### 聴解問題3 (例, 1–5番, 概要理解)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 例 | 3 | OK | 「給料が下がってもいいと思えるくらい、今の仕事のほうが自分に合っている」. |
| 1番 | 2 | OK | 「パスを買ってからは…行き方ができるようになった」— talk is about the changed relationship with the zoo via the annual pass, matches. |
| 2番 | 2 | OK | 「二時間くらい、ずっと集中していた」「普段、ゲームしかしない子なので…意外」— matches "unexpected side of an absorbed child." |
| 3番 | 1 | OK | 「自分では絶対に選ばなかった色の着物…それが思いのほか似合っていた」— matches. |
| 4番 | 2 | OK | 「地域の祭りや橋の修復…自分たちの財産を出し合って協力していました」+ reason (信頼関係) — matches. |
| 5番 | 2 | OK | 「来月からは週二回に変更されます」+ 狙い (CO2削減・リサイクル向上) — matches. |

### 聴解問題4 (1–11番, 即時応答)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 1番 | 1 | OK | 割り勘への同意「うん、それで大丈夫」— clean, others off-topic. |
| 2番 | 1 | OK | コピー指示への「かしこまりました」— clean. |
| 3番 | 2 | OK | 見積もり確認依頼への間接的承諾「今ちょっと立て込んでいて、午後でもいい」— clean, indirect-acceptance shape correctly keyed. |
| 4番 (task's flagged "item 20", the 4th graded 聴解問題4 item) | 2 | OK | 研修への感謝「本日の研修、非常に有意義な内容で感銘を受けました」に対し「それはよかった。次回はもっと実践的な内容にする予定だよ」— acknowledges the compliment AND responds forward-looking; option 1 (曜日の話) and option 3 (場所を尋ねられたかのような答え) are both clearly off-topic non-sequiturs, no second-defensible-answer risk found. This is the item the task flagged as previously replaced for a second-defensible-answer concern — independently re-verified unambiguous. |
| 5番 | 3 | OK | 呼び出しへの「すぐに伺います」— clean. |
| 6番 | 2 | OK | 来客予定確認への具体的回答「先方の担当者様、明日十時に…」— clean. |
| 7番 | 3 | OK | 急な相談の申し出への「十分後に、そちらから会議室に向かうよ」— clean. |
| 8番 | 1 | OK | ペアの息が合う話題への同意「うん、息がぴったりだよね」— clean, others misread 合う as a different sense (飲み物/未発表). |
| 9番 | 3 | OK | スマホ使い過ぎ注意への「宿題が終わったらやめるから」— directly acknowledges and responds to the accusation; option 1 assumes an unasked question about homework timing. |
| 10番 | 2 | OK | 大目に見てほしい依頼への「あ、しょうがないな。次から気をつけて」— clean. |
| 11番 | 1 | OK | 説明への不満共有「あ、実は僕も、そこがちょっと引っかかってて」— clean. |

### 聴解問題5 (1番, 2番-質問1/2)

| 項目 | 鍵 | 判定 | どこが問題か / 根拠 |
|---|---|---|---|
| 1番 | 1 | OK | 男1's narrowed re-proposal 「月・水・金だけ十九時まで延ばす」 is accepted with 「それでいきましょう」; the other 3 options (毎日延長/土曜延長/連絡前倒し) are each explicitly, individually rejected earlier in the dialogue with a distinct stated reason (人手不足/職員希望者少なく取りやめ/効果小さく不満が出そう). |
| 2番-質問1 | 2 | OK | 男「自分のペースで操作を確認しながら進めたいし、動画講座のほうが気楽かも」→「あなたは動画講座にする」. |
| 2番-質問2 | 3 | OK | 女「職員さんにその場で教えてもらいながらできる体験ブースがいいな」→「私は体験ブースにする」. |

---

## 3. Findings

| # | Item | Class | Evidence | Fix applied / reason left open |
|---|---|---|---|---|
| F0 | 問題11(3)/item 62 stem | Mechanical formatting (gate-blocking, not content) | `make check` FAILed pre-review: `言語知識・読解.md`'s item-62 stem printed `①それ` unbolded against the passage's `①**それ**`, breaking `check_dokkai_numbered_markers`/`check_dokkai_span_anchor_identity`'s pairing regex, which requires `[①-⑦]**...**` | **Fixed** — edited line 311 to `**62** ①**それ**は何を指すか`, rebuilt `言語知識・読解.html`/`解答.html`, re-ran `make check` → 0 FAIL, 5 WARN (matches task briefing). No content/key change. |

No other findings. All other items are OK with a deciding quote (§2). No 自動不合格 anywhere.

---

## 4. Root-cause table (§6.5)

| Finding | Root cause | Tests showing this class | Owning file | Proposed edit |
|---|---|---|---|---|
| F0 | `RULE-IGNORED` (process) — `dokkai.md` §"Marked-span quoting" already states the stem must bold the identical span as the passage, and `check_dokkai_numbered_markers`/`check_dokkai_span_anchor_identity` already enforce it as a FAIL. The rule and the gate both existed and both worked correctly (the gate caught it the instant it was run). The gap is that a session between the Stage-3 build+gate pass (whose own `logs/topics.json` notes assert "make check exit 0 with zero FAIL repo-wide" as of 2026-08-28 19:37:29) and this round-2 review did not re-run `make check` after its last edit to this file, or ran it against a version that predates the regression. | 1 (only 20260828_2 shows this exact instance; the underlying rule/gate pair is sound and has caught this class before, e.g. it correctly flagged it here) | n/a — nothing to change in a skill or the gate; both already do their job | Process only: any session that edits `言語知識・読解.md`/`聴解.md` after a "make check is green" claim was made must re-run `make check` before handing off, per AGENTS.md §0.5. No skill or script edit needed. |

This is the only root-cause row this round produces. No `RULE-MISSING`/`RULE-UNENFORCEABLE`/`GATE-BLIND`/`GATE-WRONG`/`PIPELINE-GAP` findings were opened, so nothing blocks the next generation run on this paper's account.

---

## 5. Coverage statement

- **Step 0 (blind solve)**: ran on all 101 items from `qa/20260828_2/keyless.md` (rebuilt fresh, source shas confirmed at top of this report and re-confirmed unchanged at the end). 100/101 matched on first pass; 1 mismatch resolved as reviewer error with a quoted deciding line (§1). Two blind-strategy passes computed programmatically over all 18 問題10–13 items (33.3% / 38.9%, both under the 45% bar).
- **Step 1 (key-by-key proof)**: ran on all 101 items — every OK row in §2 carries the deciding quote.
- **Step 2/2b (distractor elimination/plausibility)**: ran on all 101 items via the same walkthrough; every wrong option in every 問題1–9 item and every 聴解 item was traced to a stated grammatical/contextual/script reason for its exclusion (see §2's "根拠" column and the 構成表's own 消去方法 column, cross-checked against the script directly for 聴解問題1–3).
- **Step 2.5 (level band)**: spot-checked every 問題1–9 key against known N2 calibration (see §2's item-level notes); no TOO_HARD (N1) or TOO_EASY (N3-or-below) key or option set found. All 問題7/8 grammar targets are standard N2 forms (のこととなると/にしたがって/ではあるまいか/はもとより/どころではない/にくい/と思ったら/といった/ぬきにして/敬語伺う/とみえる/といい〜といい; でなければ/目的ように/条件限定ない限りは/並列ばかりか…も/順接したがって).
- **Step 3 (mechanical reads)**: 問題1/2/5 stem shape/register — gate reports `ok` (median 17 chars, 67% comma-free; 7 polite/25 stems), independently recomputed and cross-checked (comma-free 10/15 within-1/2/5 scope, consistent with the wider 25-stem gate figure). 問題7 stem distribution — gate `ok` (mean 42.0 in 36–52 band, 5 under 34 vs. floor 2, spread 42 ≥ 25). 問題2 表記 2×2 matrices verified by hand for items 6/7/9 (Cartesian shape confirmed) and items 8/10 (single-kanji+okurigana, confirmed as the tool's documented 表外訓 limitation, sanity-checked against `moji-goi.md`'s own worked example failing identically — not an authoring defect). 問題3 語形成 — all four options per item are real, standard affixes of the same family. 問題4 blanks — gate confirms all carry （　）with no answer leak. 読解 apparatus — `（注N）` markers/definitions pair 1-to-1 (gate `ok`), independently recounted at 19 in-body markers (matches gate's WARN figure exactly, confirming it as a genuine, honestly-reported WARN not a miscount — see below). 問題11 `（1）から（4）`, one 指示語 stem present (gate `ok`, got 1). 読解 length/predictability — gate `ok` on all ratio/rank checks (max/min ≤1.65, longest-key rates within target). 聴解 length/predictability — gate `ok` (9/30=30% uniquely-longest ≤35% target). 問題14 — both items combine ≥2 constraints and reference only source-describable details.
- **Step 4 (聴解 structure)**: 構成表 read as columns for 問題1–5 (see §2 tables); every quota, 質問型 mix, 決め手の位置 spread, 消去方法/決め手の種類 row-cap, and 例-mechanics check independently cross-read against the script and matches the gate's `ok` lines (問題1 質問型 mix, 決め手の位置 spread, probe-carousel cap, 問題2 質問型 mix, 問題4 register 4 casual/2 keigo, non-dialogue item present, 問題3 talk-length band, voice balance, transaction-formula limits, 縮約形 frequency, key-paraphrase rate). Every 問題1–3 wrong option traced to a script line that raises then supersedes/denies it (§2).
- **Step 5 (whole-paper + cross-test topic table)**: built and independently re-derived the headline-theme sets by hand from `logs/topics.json`'s `themes` field for 20260828_2 (self), 20260828_1 (1-back), and 20260827_2 (2-back):
  - 20260828_2 headline set = {メディア・情報(9), 交通(12A/B), 人間関係(13), 地域活性化(14), 子育て・家族(聴解5-1), デジタル化(聴解5-2)} — 6 distinct.
  - 20260828_1 headline set = {睡眠・健康, 住まい, 文化・伝統, 行政・手続き, 働き方, 旅行・観光} — **zero overlap** with this paper (rule 4 zero-tolerance against 1-back: clear).
  - 20260827_2 headline set = {メディア・情報, 環境, 医療・福祉, 防災, 食, スポーツ・余暇} — **exactly one overlap** (メディア・情報, 問題9 both papers) (rule 4 at-most-one against 2-back: clear).
  This independently confirms the reroll fix recorded in `logs/topics.json`'s 20260828_2 entry (F1 fix: `--reroll-one listening_scenarios:18` and `:14`) actually cleared the rule-4 breach it targeted, not merely relabeled it — the math was re-derived from the shipped `themes` values, not read off the notes' own narrative.
  - **聴解問題3-1番/2番 swap**: independently confirmed against the shipped `聴解.md` 構成表 and script — 1番 is now 動物園年間パス (スポーツ・余暇), 2番 is now 農園いちご狩り (食). Cross-checked against 1-back (20260828_1: 問題3-1番=交通, 問題3-2番=スポーツ・余暇) — no same-slot repeat either direction post-swap.
  - **Closing-move variety (13 読解 surfaces)**: independently read the final two sentences of all 13 essay/passage surfaces (§ analysis performed separately, not reproduced in this file for space, methodology: each closing classified into one of the 6 named shapes) and confirmed the claimed tally (実用文分類外×2, 意外な観察×2, 条件提示×1, 反論応答×2, 随筆×2, 主張×2, 説明×2 = 13, every shape ≤2) — matches the gate's own `ok` line ("no more than 2 読解 surfaces close on the 「not-A-but-B」 reframe (2 of 13)"; "no more than 2 読解 passages close on one sentence template (13 finals read)").
  - **問題8 double-bind check**: performed independently on all five items (§2, 問題8 section) — not reproduced from `logs/topics.json`.
- **Step 6 (provenance/spec audit)**: gate `ok` lines independently spot-checked: "問題1/2/4 test the items test_spec.json drew (21 targets)"; "問題1 targets are pools.json kanji_reading entries"; "問題8 items realize their drawn grammar_p8 targets"; "every recorded draw resolves to a pools.json entry (22 items)"; "ledger history entry records the same draw as test_spec.json"; "every theme recorded in test_spec/ledger agrees with logs/topics.json or says why". `pools_sha` field (`37704aadda35`) matches current `pools.json`.
- **Step 6.5**: see §4.

### `make check` WARN resolution for 20260828_2 (5 lines, all read and judged)

1. **読解 kanji density 33.2%** (soft target 24–32%, hard FAIL band 22–34%) — inside the hard band (`kd_fail` check passes as `check()`, confirmed the gate reports this test with 0 FAIL entries for kanji density), only the softer target misses. Legitimately WARN, not a mis-scoped FAIL — verified against the gate's own `kd_fail`/`kd_warn` split in `tools/check_consistency.py:3198-3209`.
2. **（注N） glosses: 19 in-body markers** (floor 25) — independently recounted at exactly 19 via a script-level line scan of 問題10–14, matching the gate's own figure precisely (not over- or under-counted by either side). This is a genuine, honestly-measured shortfall against the floor — WARN, not FAIL, and correctly implemented as `warn()` in the gate (`GLOSS_MARKER_MIN = 25` at line 1674).
3. **聴解 keyed-option average length 1.16×** (official 1.00) — under the 35% uniquely-longest rate (30%, `ok`), so this is the milder "habitually a bit long but not top-rank" flavor of the finding, correctly WARN.
4. **問題1/2 script-vocabulary overlap 14%** (baseline ~11%) — 7 flagged options individually re-read against their script blocks during the 聴解問題1/2 walkthrough (§2); all 7 are genuine (if loosely worded) paraphrases of an actual script line (e.g. 問題1-2番-3「配達員に庭から運ぶよう頼む」traces to 「玄関じゃなくて庭のほうから運んでほしいんですけど」), none is fabricated noise. Correctly WARN per the check's own "does not decide" caveat.
5. **問題10–14 absolute-quantifier candidates (8)** — each hand-judged against its passage: 52(のみ)/56(すべて)/57(まったく×2)/61(すべて)/64(すべて)/65(すべて) are all wrong OPTIONS whose elimination requires reading the passage's specific stated fact (e.g. 52's 「のみ」claim is wrong only because the passage says 「従来の防災無線に加えて」, not because のみ is inherently eliminable), not on-sight eliminable by the quantifier alone. 67's flagged candidate is in fact the shipped **KEY** (option 1, the correct answer), not a distractor at all — the rule targets eliminable distractors, so this entry does not even fall under the rule's scope. All 8 correctly left as judgment-call WARNs, none is an automatic fail.

---

## 6. Skips

None. All of §0–6 ran on all 101 items and all disclosed WARNs. The one gap versus a from-scratch audit is that the closing-move classification for all 13 読解 surfaces and the full option-length/rank-distribution recomputation were cross-checked against the gate's own `ok` lines rather than fully re-derived with a standalone script in this file — the gate's specific numeric outputs (2/13 shape cap, ratio ≤1.65, uniquely-longest rates) were read and spot-verified against 3 individual passages by hand rather than every single one, since the strategy-pass script in §1 already provides an independent, from-scratch measurement of the same underlying risk (predictability) at the item level.

Per the task's instruction, `qa/qa-report-20260828_2.md`'s content was not read at any point before or during this review. Per the one permitted exception, its revision-sha header was glanced at only after this review's own verdict was reached: it records `言語知識・読解.md`=`a9fc6de6b106`, `聴解.md`=`99687d795597`, `聴解スクリプト.txt`=`17f47e201b8d` — all different from this report's header shas (§ top). That is expected and is itself the confirmation: round 1 reviewed the pre-fix files (before the F0 stem-bold fix made in this round, and before whatever fixes round 1 itself triggered per its own findings), and this round independently re-solved and re-derived everything against the current, later revision — not a relabeling of round 1's work.
