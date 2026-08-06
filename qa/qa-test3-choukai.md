# TEST 3 CHOUKAI — adversarial QA (fresh eyes, reviewer did not author)

## 1. Verdict

**TEST 3 CHOUKAI: FAIL (31 findings, 19 automatic)**

Entry-condition note: `make check` is **not green** for test 3 (7 FAIL lines + 3 WARN
lines). `exam-qa-review` §Ground rules says "Do not start QA on a failing gate." I ran
the review anyway because the task explicitly scoped it and pre-filed the 聴解 gate
failures; this deviation is recorded here rather than silently.

---

## 2. Blind-solve diff

Procedure: I read `tests/3/聴解スクリプト.txt` end to end and `tests/3/聴解.md`'s
**question body only**, answered all 30 items, then opened the マークシート and the
【正解・解説】 tables.

| 問題 | reviewer's answers | key | diff |
|---|---|---|---|
| 問題1 (5) | 4, 1, 3, 1, 2 | 4, 1, 3, 1, 2 | none |
| 問題2 (6) | 4, 2, 2, 3, 1, 1 | 4, 2, 2, 3, 1, 1 | none |
| 問題3 (5) | 2, 4, 3, 1, 1 | 2, 4, 3, 1, 1 | none |
| 問題4 (11) | 3, 2, 1, 3, 1, 2, 1, 3, 1, 2, 2 | 3, 2, 1, 3, 1, 2, 1, 3, 1, 2, 2 | none |
| 問題5 (3) | 3, 1, 2 | 3, 1, 2 | none |

**30/30 agreement, zero mis-keys.** That is not a pass signal — it is a *difficulty*
signal. I solved 11 of the 18 scored items in one pass without needing to track the
conversation, because the wrong options are not competitors (see §5: 12 options across
6 items are raised by **no line in the script at all**). An item you can answer by
discarding nonsense is not testing listening.

Two items where my answer matched the key but the item is still filed:

- **問題4 例** — I marked 1, which is the announced number, but 3
  「いいえ、結構です」 is an equally natural reply to 「お菓子、いかがですか。」. Second
  defensible answer → F-07.
- **問題4 2番** — I marked 2 (the key), but 1 「じゃあ、後で部屋まで持ってきてくれる?」
  is a normal thing for a 課長 to say. I cannot write a fact that makes it impossible,
  only that the key fits better → per §2 of the skill, that is a two-answer item → F-25.

All 30 answer positions match `logs/test_spec.json["answer_positions"]`
(聴解_問題1 `[4,1,3,1,2]`, 問題2 `[4,2,2,3,1,1]`, 問題3 `[2,4,3,1,1]`,
問題4 `[3,2,1,3,1,2,1,3,1,2,2]`, 問題5 `[3,1,2]`). ✅

例 pre-marks vs announced numbers: 問題1 例=(2)/「2番です」, 問題2 例=(4)/「4番です」,
問題3 例=(2)/「2番です」, 問題4 例=(1)/「1番です」 — all four agree. ✅

**The known 問題1 例 defect is FIXED.** The task flagged that test 3 shipped a mangled
問題1 例 whose true first action was not printed. It now is: the dialogue ends
「じゃあ、先にホテルへ電話しておきますね。」 and printed option 2 is
「ホテルに確認の電話をする」, matching the announced 2番. Verified in `聴解.md`,
`聴解.html` (rendered) and `解答.html`. ✅ (Its option 4 is still ungrounded — F-20.)

---

## 3. Findings table

Class key: **AUTO** = on `exam-qa-review`'s automatic-fail list (or the task's
"broken Japanese / unnatural collocation / keigo error" rule). **min** = minor.

| # | Item | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| F-01 | 問題5-2番 | AUTO — broken Japanese | Script line 245: `職員:わかりました。では男1さんは北口広場、男2さんは南口コミュニティセンターですね。東町公民館は私が行きますので、残る西駅前広場は女さんにお願いできますか。` | `男1さん`/`男2さん`/`女さん` are `SPEAKER_MAP` labels used as personal names. edge-tts will speak 「おとこいちさん」. Give the four speakers in-world names (田中さん/佐藤さん/…) and use those in the dialogue; the labels stay in the `名:` prefix only. Re-synthesize. |
| F-02 | 問題5-2番 | AUTO — authoring annotation in narration | Script 247–248: `質問1。経験豊富な男の市民（男1）は、…` / `質問2。初めて参加する男の市民（男2）は、…` | `choukai-script-writing` §"No authoring annotations either" bans parentheticals outright — edge-tts reads them aloud. Delete both; once F-01's real names exist the questions become 「田中さんは、どこを担当することにしましたか」. |
| F-03 | 問題5-2番 | AUTO — narration contradicting the mapped voice / unlistenable casting | 4 speakers on 2 voices: `職員` F +0% and `女` F +4% (4 pts apart); `男1` M +4% and `男2` M −8%. Official 2番 (`imported-n2-2025-07`) has **two** speakers: 「2番。ラジオを聞いて男の人と女の人が話しています。」 | The examinee must separate two male citizens by speaking rate alone — the parentheses in F-02 exist *because* the audio cannot do it. Cut to ≤3 speakers with contrasting voices, or cast 男2 on a third distinct male voice. `make check`'s one-voice WARN never fired because it only inspects two-party items. |
| F-04 | 問題1-4番 | AUTO — keigo error | Script 44: `確認書類のご提示は番号がお呼びできた際にお願いいたします。` (also quoted verbatim into the 解説 cell of `聴解.md`) | `お呼びできる` is the speaker's 謙譲 potential; it cannot take `番号が` as subject. Rewrite 「番号をお呼びした際にお願いいたします」 and update the 解説 quote. |
| F-05 | 問題2-1番 | AUTO — unnatural collocation | Script 70: `山田さん、長時間の立ち作業でお腰の具合はいかがですか。` | `お腰` is not a modern polite form for the body part (it reads as 腰巻). Use 「腰の具合はいかがですか」. |
| F-06 | 問題3-1番 | AUTO — broken Japanese | Script 121: `…来月10日の納品スケジュールを2週間延期し、24日変更といたします。` | Missing particle. 「来月24日に変更いたします」. (Also prefer 「納品を2週間延期し」 over 「納品スケジュールを…延期し」.) |
| F-07 | 問題4 **例** | AUTO — second defensible answer, in the demonstration item | `例。お菓子、いかがですか。` / `1、ほう、おいしそうですね。` `3、いいえ、結構です。` — announced 1番 | 「結構です」 is the standard polite refusal of an offer; both 1 and 3 are valid. Compare official (`imported-n2-2025-07`): 「今日、ちょっと残業できる?」 / 「2、いいえ、残業はありません。」 — refusal-*shaped* but semantically wrong. Replace option 3 with a refusal-shaped non-answer (e.g. 「いいえ、お菓子は売り切れです。」). |
| F-08 | 問題1-1番 | AUTO — fabricated distractor | Option 1 「エアコンを使わずに扇風機をつける」 — **扇風機 appears nowhere in the script** | Replace with a candidate the dialogue raises and kills, e.g. 「冷えすぎを防ぐためタイマーを2時間で切る」 (夫's superseded habit). |
| F-09 | 問題2-1番 | AUTO — fabricated distractor | Option 1 「重い荷物を一人で持たないようにしたこと」 — **荷物 appears nowhere** | Replace with 「軽いストレッチを取り入れたこと」 (raised at line 73, and *not* the one called 一番効果的). |
| F-10 | 問題2-2番 | AUTO — **all three** wrong options fabricated | Options 1 「自転車の購入費用が割引されること」, 3 「電動自転車が必ず無料で借りられること」, 4 「保険の加入手続きが不要であること」 — 購入費用/電動自転車/保険 are **not in the monologue**. The script offers exactly two other candidates: 「アプリで簡単に解錠できる手軽さ」 and 「料金の安さ」 | Rebuild the option set out of the script: 1 手軽な解錠, 3 料金の安さ, 4 設置ポート数の多さ — all raised and all explicitly ranked below 「一番の理由は…返却できる点」. This is the item `choukai-script-writing` §"keyed option must be quotable" already names as test 3's worst; it is still there. |
| F-11 | 問題2-4番 | AUTO — fabricated distractors ×2 | Options 2 「難しい専門用語をたくさん盛り込むこと」 and 4 「抑揚をつけずに大きな声だけで話し続けること」 — neither 専門用語 nor 声/抑揚 is in the script | Replace with 「志望動機を整理しておくこと」 (raised: 「志望動機はしっかり整理できていますね」 — praised but not ranked first) and 「回答の内容を充実させること」 (raised: 「回答の内容も大切ですが」 — explicitly outranked). Both also fail step 2b: they are obviously bad advice and die on sight. |
| F-12 | 問題2-5番 | AUTO — fabricated distractor | Option 4 「暴風警報が発表される」 — no 警報/暴風 in the script | Replace with 「気温が下がって肌寒くなる」 (denied by 「日中の気温も上がり」). |
| F-13 | 問題2-6番 | AUTO — fabricated distractors ×2 | Options 2 「工事費用が来週の土曜日だけ割引になるから」 and 4 「マンション全体の停電が来週土曜日に予定されているから」 — 割引/停電 never mentioned | Replace with 「今週の土曜日は予約が埋まっていたから」 (raised, and a *partial* truth so it competes) and 「業者が来週しか対応できないから」 (denied by 「今週の平日はご都合がいかがでしょうか」). |
| F-14 | 問題1-5番 ≡ 問題3-4番 | AUTO — topic repeated inside the paper | 問題1-5番: 「使い捨てビニール傘の廃棄削減に向けて、傘シェアリングサービスの導入計画案」／「アプリ登録で借りて最寄りスポットへ返却」／「駅…へのスポット設置」. 問題3-4番: 「傘のシェアリングサービスが急速に拡大」／「アプリを使って…目的地の最寄り駅で返却」／「使い捨てビニール傘の削減」／「全駅へのスポット設置」 | Same service, same mechanism, same decisive fact, in two 問題. Drop one and author it from an unused spec scenario (`文房具:法人契約`, `研修会でのグループワーク`, `税務署:確定申告` are all still unused). |
| F-15 | 問題2-2番 ≡ 問題3-2番 | AUTO — topic repeated inside the paper | 問題2-2番 「自転車シェアリングサービス…ポートへ自由に返却」; 問題3-2番 「都市部で急速に普及したシェアサイクル」 | Same service in two registers. Combined with F-14, **4 of the 18 scored 聴解 items (22%) run the same "sharing service with return spots" mechanism**. |
| F-16 | 問題3-5番 | AUTO — subject repeats the previous test | test 3 問題3-5番: 「睡眠の質、すなわち起きた時の休養感が非常に重要です」. **tests/2 問題2-1番**: 「男の人は、睡眠の質が改善した一番の理由は何だと言っていますか。」 | 睡眠の質 is the head subject of a scored 聴解 item in both papers. Re-author from a fresh seed. |
| F-17 | 問題1-1番 | AUTO — question type belongs to another 問題 | 「二人は、今夜寝る時にどうすることにしましたか。」 Official 問題1 stems (`imported-n2-2025-07`) are uniformly 「この後まず何をしますか」/「何をしなければなりませんか」 (all 6 items). Official 問題**2** has exactly this shape: 「2人は試作の弁当をどのように変えて売ることにしましたか。」 | This is a ポイント理解 item sitting in 課題理解, and it asks about 二人 rather than one actor. Either move it into 問題2 (re-ordering options for the new `answer_positions` slot) or rewrite the question as a first-action question for one speaker. |
| F-18 | 問題2-3番 | AUTO — question type belongs to another 問題 | 「電子チケットを持っている来場者は、どこから入場しなければなりませんか。」 — `〜しなければなりませんか` is the official **問題1 例** shape (「学生は今日、家で何をしなければなりませんか。」) | With F-17 the paper has a clean 問題1↔問題2 inversion — the same defect class test 4 shipped. It is also a pure single-fact retrieval: the announcement lists four gates and the four options are those four gates, in order. |
| F-19 | 問題5 (whole section) | AUTO — the section does not test 統合理解 | **1番**: 係員 lists 「1番の歴史散策コース…2番の自然満喫コース…3番のグルメ食べ歩きコース…4番の温泉リフレッシュコース」; the question says 「地元の美味しい名物料理やスイーツを楽しみたい人は」 and the script says 「3番の…コースは、地元の新鮮な名物料理やスイーツの店舗を巡る」. The monologue's own item numbers are **identical to the option numbers**. **2番**: 質問1 is answered by 男1's own single line 「私が北口広場を引き受けますよ」, 質問2 by 男2's own line, and 職員 then repeats both | Compare official 1番: three speakers propose 日程変更, 締め切り延長, 少人数化, 試合形式; two are explicitly killed before 会場変更 survives. Rewrite per RC-7: the answer must require eliminating ≥2 listed options against constraints raised later, and the monologue must never number its items 1〜4 (official uses 1つ目/2つ目 or names). For 2番, neither 質問 may be answerable from one sentence by that speaker. |
| F-20 | 問題1 例 | min — ungrounded option | Option 4 「男の人に資料を渡す」 — the 例 dialogue never mentions handing anything over | Replace with 「新幹線のチケットを受け取りに行く」-adjacent grounded content, or 「出張の資料をもう一度確認する」. |
| F-21 | 問題1-2番 | min — ungrounded option | Option 4 「体験授業の感想を書く」 — 体験授業 is mentioned, **感想を書く is not** | Replace with 「受付で面談を受ける」 or ground it (「アンケートにご記入ください」 in the staff's turn). |
| F-22 | 問題1-5番 | min — ungrounded option | Option 3 「アプリの登録方法をマニュアル化する」 — 「アプリ登録で借りて」 is said, マニュアル化 is not | Replace with 「公共施設との設置交渉を先に進める」 (raised at line 51 and deprioritised at 52). |
| F-23 | 問題2-6番 | min — narration contradicts the dialogue | Narration: 「電話で**アパート**の住民の女の人と…」; the woman says 「**マンション**の定期電気設備点検の…」 and option 4 says 「マンション全体の停電」 | Make all three マンション. |
| F-24 | 聴解.md 得点の目安 | min — impossible scale | The booklet header says 「問題数: 30問」; the 得点の目安 block says 「**35問以上**正解: 合格ライン」／「**45問以上**正解: 高得点合格」 | Both thresholds exceed the number of questions. Use tests 1/2 and `imported-n2-2025-07`'s wording (27〜30 / 18〜24 / 17以下). (test 4's 26〜32点 is broken the same way — out of scope, flagged for the record.) |
| F-25 | 問題4-2番 | min — possible second answer | 「課長、新商品のサンプルが届きましたので、お持ちいたしました。」 / option 1 「じゃあ、後で部屋まで持ってきてくれる?」 | I cannot state a fact making option 1 impossible — a busy 課長 redirecting delivery to his room is ordinary. Replace with a functionally wrong reply, e.g. 「じゃあ、届いたら知らせてくれる?」 (already delivered → impossible). |
| F-26 | 聴解.md 解説 (all 18 items) | min — mandated grounding lines absent | `grep -c ✗ tests/3/聴解.md` → **0**. `choukai-script-writing` §"The keyed option must be quotable" mandates one `N ✗「script line」→ 理由` line per wrong option in the 解説 cell | This is the missing artefact that let F-08…F-13 ship: the cells justify only the key. Add the ✗ lines for every 問題1/2/3 wrong option. (tests 1, 2 and 4 all score 0 too — see RC-1.) |
| F-27 | 問題2 (section) | min — genre calibration | 3 of 6 問題2 items are monologues (2番 ラジオ, 3番 会場アナウンス, 5番 天気予報). Official July 2025 has **1** monologue in 6 | With 問題3's 5 monologues the paper runs 8 monologues in 11 items across 問題2+3, blurring ポイント理解 into 概要理解. Convert 2 of the 3 to conversations. |
| F-28 | 問題2-1番, 問題2-4番 | min — the key is restated by the partner | 2-1番 closes `女:なるほど。作業台の高さ調整が腰への負担軽減につながったんですね。`; 2-4番 closes `男:なるほど。相手の質問をよく聞いて、それに直接答えることが一番大事なんですね。` — each is a near-verbatim reading of the keyed option | Official 問題2 items end on the questioned speaker's own line, never on a partner's summary. Delete both confirmation turns. |
| F-29 | 問題4 3番 / 10番 / 11番 | min — below the N2 band | 3番 「15分ほどかかりますが、よろしいでしょうか」→「それくらいなら歩けます」; 10番 「カードと現金、どちらがよろしいですか」→「クレジットカードでお願いします」; 11番 「3日後です。それでもよろしいですか」→「急ぎませんので構いませんよ」 — none turns on an idiom, a keigo direction, or an indirect refusal | These three came **verbatim from the pool** (`test_spec.json["items"]["quick_response"]`), so the fix is in `pools.json`, not the paper (RC-9c). By contrast 6番 顔が広い, 7番 大目に見る, 4番 お手数をおかけします are correctly N2. |
| F-30 | 問題3-3番 | min — Latin in a spoken line | Script 140: `2、新しく発売された損害保険のPRについて。` | The gate rejects ASCII punctuation but not Latin words in the script. Write 「宣伝」 and let the gate check for it (RC-11). |
| F-31 | tests/3/聴解.html | min — md→html fidelity gap | `聴解.md` prints 19 answer-grid lines for 問題3/問題4/問題5-1番 (`**例** 1 ・ 2 ・ 3 ・ 4` …), i.e. 57 `・`. The rendered `聴解.html` contains **4** `・` in total — every grid line is dropped | Either render them or drop them from the md; a source line that silently disappears is how the two files diverge. (`解答.html` is unaffected — it builds its own radio groups, and `make check` confirms 101 correctly-sized groups.) |

### Already filed by `make check` — NOT re-filed, no additional instances found

| Pre-filed | My check |
|---|---|
| 問題5 2番 lead-in spoken | Confirmed at script line 239; **one** instance only. Booklet-side text at `聴解.md:143` is correct and must stay. |
| `script_sha: None` (stale MP3) | Confirmed: `聴解_チャプター.json` has only `duration`/`chapters`, no `script_sha`. **Independent corroboration:** `聴解.mp3` and `聴解_チャプター.json` are stamped Aug 5 18:59, `聴解スクリプト.txt` Aug 6 09:56 — the audio predates the script it is supposed to speak. The 38 chapter labels still match the current 33-item structure, so the drift is in line content, not item count. |
| 3 narration/`SPEAKER_MAP` gender mismatches (係員, アナウンサー, 職員) | Confirmed exactly 3: 問題2-3番 「係員の男の人」, 問題3-4番 「アナウンサーの男の人」, 問題5-2番 「職員の男の人」 — all three labels are FEMALE in `SPEAKER_MAP`. I audited the other 15 narrations: 問題1-2番 女/男, 問題1-3番 店長(M)/女の店員(F), 問題1-4番 女/男, 問題1-5番 「女の職員」 on FEMALE 職員 ✅, 問題2-1/4/5/6番, 問題3-1/2/3/5番, 問題5-1番 (no gender stated) — **no further mismatches**. |
| quick_response substitution 「こちらこそ、いつもお世話になっております。」 | Confirmed the paper's 8番 is 「本日は遠方からお越しいただき、ありがとうございました。」 with key 3 「こちらこそ、温かくお迎えいただき感謝申し上げます」. **No further substitutions** — see §6. Root cause added as RC-10: the sampled item is itself a *reply*, not a stimulus, so no author could have used it as a 問題4 prompt. |

---

## 4. Root-cause table (§6.5)

Recurrence counted by reading the other tests' sources on disk, not from memory.

| RC | Findings | Code | Tests showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|---|
| **RC-1** | F-08…F-13, F-20, F-21, F-22, F-26 | `GATE-BLIND` + `RULE-UNENFORCEABLE` | **4/4** — `grep -c ✗ tests/{1,2,3,4}/聴解.md` = 0, 0, 0, 0; `choukai-script-writing` already documents fabricated options in all four | `tools/check_consistency.py` + `.agents/choukai-script-writing/SKILL.md` | Add `check_choukai_distractor_grounding()`: for every 問題1/2/3 item, the 解説 cell must contain one line per wrong option matching `^([1-4]) ✗「(.+)」→`, and each quoted string must occur **verbatim** in `聴解スクリプト.txt`. **FAIL, not WARN** — the existing token-overlap check is a WARN by design and cannot decide this. This one check catches 12 of this paper's 19 automatic findings. In the SKILL, move the ✗ template from prose into a numbered authoring step ("write the 解説 ✗ lines *before* the option text; an option with no ✗ line does not exist yet"). |
| **RC-2** | F-01, F-02, F-03 | `GATE-BLIND` (F-01/F-02 string-decidable) + `RULE-MISSING` (F-03) | F-03 class: 4/4 (one-voice pairs in every paper — `make check` WARNs on tests 1, 2). F-01/F-02: 1/4 (test 3 only) | `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py` (`validate_script`), `tools/check_consistency.py`, `.agents/choukai-script-writing/SKILL.md` | (a) `validate_script()` — reject any spoken line matching `(男[12]\|女[12]?\|学生\|職員\|係員)さん` or containing `（男[12]）`/`（女[12]?）`: a `SPEAKER_MAP` label may never appear inside spoken text. (b) Promote the one-voice check from WARN to FAIL **and** run it on items with **any** number of labels, not just two — 問題5-2番's 職員/女 pair (both FEMALE, 4% apart) escaped it purely because the item has four labels. (c) SKILL §"One voice per person": add "問題5-2番 has at most three speakers — official July 2025's 2番 has two. Two same-gender participants must be given in-world surnames spoken in the dialogue; the label is a voice selector, never a name." |
| **RC-3** | F-04, F-05, F-06 | `RULE-UNENFORCEABLE` (mostly human judgment) | not audited across papers (out of scope); test 4 shipped 6 broken sentences per `exam-qa-review` §3 | `.agents/choukai-script-writing/SKILL.md` §Validation | Add a named "read-aloud honorific checklist" listing the three shipped patterns as banned: `お＋身体部位` (お腰/お足/お頭), `〜がお〜できた際` (謙譲 potential with a `が` subject), and `名詞＋変更といたします` (missing に). Add the string-decidable subset to the gate as a **WARN**: `お腰|お足|お頭`, `が\s*お[ぁ-ん一-龥]+できた`, `\d+日変更`. State explicitly in the SKILL that the rest cannot be mechanized and must be read aloud by a human/fresh context — so the next reviewer does not assume the gate has it. |
| **RC-4** | F-07 | `RULE-UNENFORCEABLE` | 1/4 confirmed here; test 4 shipped an unanswerable 問題1 例; test 3's own 問題1 例 was the previously-filed one | `.agents/choukai-script-writing/SKILL.md` §"The 例 must be answerable" | Extend: "…and every other 例 option must be **functionally impossible**, not merely less polite. Model on `imported-n2-2025-07` 問題4 例 (「今日、ちょっと残業できる?」／「2、いいえ、残業はありません。」 — refusal-shaped, semantically wrong). A generic polite refusal (結構です / 大丈夫です / いいえ、いりません) is never a valid distractor to an offer, because it is a correct answer." |
| **RC-5** | F-14, F-15, F-16 | `GATE-BLIND` + `PIPELINE-GAP` | 2/4 minimum: test 4 re-uses test 3's 熱中症・夜間エアコン (問題2-3番) and 自転車シェアリング (問題2-5番) | `.agents/web-topic-research/scripts/merge_seeds.py` + `tools/check_consistency.py` | The spec **itself** carries the duplicate pairs: `listening_scenarios` #5 「使い捨て傘ゼロに向けたシェアリング普及」 vs #15 「駅での傘シェアリングサービスの拡大」, and #7 「自転車シェアリングのポート間貸出・返却」 vs #13 「シェアサイクル利用時のヘルメット着用促進」. `make check` already FAILs on `logs/seeds.json` reusing one URL (`h23_lca_01.pdf` ×2), which is the same harvest defect one layer up. (a) `merge_seeds.py`: reject a harvest where two scenarios share a ≥4-char head noun after katakana/kanji normalization (シェアリング, シェアサイクル). (b) Gate: `check_listening_topic_distinctness()` — no two scenarios *assigned in one paper* may share a ≥3-char content noun, and no scenario head noun may equal one used by the immediately previous test (`睡眠` → test 2 問題2-1番). Both are string-decidable off `test_spec.json` + the ledger. |
| **RC-6** | F-17, F-18 | `GATE-BLIND` | **2/4** — test 4 shipped 問題1↔問題2 swapped (documented in `choukai-script-writing` §"The 問題 decides the QUESTION TYPE") | `tools/check_consistency.py` + `.agents/jlpt-exam-structure/SKILL.md` | Add `check_choukai_question_shapes()` off the script's item blocks: every 問題1 marker line must end `この(後\|あと)まず?(何をしますか\|何をしなければなりませんか)`; **no** 問題2 marker line may match `しなければなりませんか` or `まず何をしますか`; every 問題3 item block must contain `何について話していますか`. Fully string-decidable — the 例 lines and all 33 item blocks already carry the question on their first (問題1/2) or last (問題3) line. Also add the official stem inventory (transcribed above from `imported-n2-2025-07`) to `jlpt-exam-structure` §聴解 so the author copies shapes instead of inventing them. |
| **RC-7** | F-19 | `RULE-MISSING` | **2/4** — test 4's 問題5-1番 is the identical defect (教授 lists 4 labs 1つ目〜4つ目, says 「中でも情報処理研究室は…おすすめします」, question asks 「どの研究室を特に勧めていますか」, options = the 4 lab names in order). tests 1 and 2 are clean | `.agents/jlpt-exam-structure/SKILL.md` §問題5 + `.agents/choukai-script-writing/SKILL.md` | Add a construction rule (a rule the author applies *while writing*, not a check afterwards): "**問題5-1番**: the keyed option must survive the ELIMINATION of at least two other listed options against constraints raised *after* the list (official July 2025 kills 日程変更 — 「既に申し込んでる方や選手の都合もありますしね」 — and 試合形式 — 「今回は初心者も参加できるイベント」 — before 会場変更 survives). A monologue that lists four items and then names one as matching the question is a 問題2 item. **Never number the listed items 1〜4 in the monologue** — official uses 1つ目/2つ目 or names, precisely so the option index cannot be read off the list order. **問題5-2番**: neither 質問 may be answerable from a single sentence spoken by the person it asks about; the answer must combine a list description with a preference stated elsewhere (official: 「鳥が見られる所」 → さくら公園)." |
| **RC-8** | F-24 | `GATE-BLIND` | **2/4** — test 4's 聴解 scale reads 26〜32点 out of 30 | `tools/check_consistency.py` | One-line check: every integer preceding `問` or `点` inside a `## 得点の目安` block must be ≤30 in `聴解.md` and ≤71 in `言語知識・読解.md`. |
| **RC-9** | F-27, F-28, F-29 | `RULE-MISSING` (F-27, F-28); `PIPELINE-GAP` in the pool (F-29) | F-27/F-28 not previously named anywhere | `.agents/choukai-script-writing/SKILL.md`; `.agents/item-pool-sampling/…/pools.json` | (a) SKILL: "at most **2** of 問題2's 6 items may be monologues — official July 2025 has 1." (b) SKILL: "a 問題1/2 item's last dialogue turn must not restate the keyed option; official items end on the questioned speaker's own line, never on a partner's 「なるほど、〜ということですね」 summary." (c) `pools.json`: every `quick_response` entry must carry an idiom, a keigo direction, or an indirect refusal. Delete the three plain-comprehension prompts this paper inherited: 「お会計、カードと現金、どちらがよろしいですか。」「会場までは駅から歩いて15分ほどかかりますが、よろしいでしょうか。」「到着予定は3日後です。それでもよろしいですか。」 |
| **RC-10** | (pre-filed quick_response substitution) | `PIPELINE-GAP` | 1/4 observed | `.agents/item-pool-sampling/…/pools.json` + SKILL | The drawn item 「こちらこそ、いつもお世話になっております。」 is a **reply**, not a stimulus — it cannot be a 問題4 prompt, so the substitution was forced, not sloppy. Split the 即時応答 pool so entries are prompts only (replies belong in the option set), and add a gate check that no `quick_response` pool entry begins with `こちらこそ`/`はい、`/`いいえ、`. Without this the same substitution recurs on the next draw. |
| **RC-11** | F-30 | `GATE-BLIND` | 1/4 observed | `tools/check_consistency.py` | Extend the existing ASCII-punctuation script check: WARN on `[A-Za-z]{2,}` in a spoken line (`PR`), allowing single capitals used as labels (`Aゲート`, `Bゲート`), since edge-tts pronunciation of multi-letter Latin is unspecified. |
| **RC-12** | F-31 | `GATE-BLIND` | not audited across papers | `.agents/exam-booklet-generation/SKILL.md` + gate | Either render `**例** 1 ・ 2 ・ 3 ・ 4` lines or state in the SKILL that they are answer-sheet-only and remove them from the question-body markdown. A source line that renders to nothing is a silent divergence between the two files QA reads side by side. |
| **RC-13** | F-23 | `RULE-MISSING` | 1/4 observed | `.agents/choukai-script-writing/SKILL.md` | Add a self-reconciliation line to the authoring checklist: "after the dialogue is final, re-read the narration line against it — every noun the narration asserts (place type, role, count of speakers) must appear in the dialogue with the same value (test 3: narration アパート, dialogue マンション)." Not mechanizable in general; stated as human judgment on purpose. |

**Blocking effect (§6.5):** RC-1, RC-2, RC-5, RC-6, RC-7, RC-8, RC-9, RC-10, RC-11
are `RULE-MISSING`/`GATE-BLIND`/`PIPELINE-GAP` and therefore **block the next
generation run** until applied or explicitly rejected. RC-1 and RC-7 are the two with
confirmed multi-paper recurrence and the highest yield.

---

## 5. Coverage statement

### 5a. Steps run, on which files

| Step | Ran on | Result |
|---|---|---|
| Blind-solve, all 30 items + 5 例 | `聴解スクリプト.txt` + `聴解.md` question body | §2 — 30/30, 2 items still filed |
| Step 1 key-by-key proof | all 30 | every key restates a quotable script line; the two 理由 items (問題2-6番, 問題2 例) are keyed to the CAUSE, not the measure — 2-6番 key 「平日は仕事で立ち会えず、今週土曜の予約が埋まっていたから」 restates 「平日は仕事で帰宅が遅くなるため立ち会いができません」+「今週の土曜日はすでに予約が埋まっております」 ✅ |
| Steps 2 + 2b distractor audit | 問題1 (6 items × 3), 問題2 (7 × 3), 問題3 (6 × 3) = **57 wrong options** | table 5b |
| Step 3 (聴解 side) — 問題↔type mapping | all 18 scored items + 5 例, against `imported-n2-2025-07`'s 33 item lines | F-17, F-18 |
| Step 3 — 例 answerability + announced number | all 5 例 (問題1–4 have one each; 問題5 correctly has none) | F-07; 問題1 例 defect confirmed FIXED |
| Step 3 — 即時応答 rank/keigo + idiom band | all 11 | direction correct in all 11 (2番 課長 replies downward plain ✅, 8番 visitor↔host ✅, 9番 拝見いたします ✅); band: F-29 |
| Step 3 — 問題5 structure | 1番 spoken options / 2番 printed options | split correct: spoken choice lines per section = 問題3:24, 問題4:36, 問題5:4, 問題1/2:**0** ✅ — 問題5-2番's options are printed only ✅. Content: F-19 |
| Narration ↔ `SPEAKER_MAP` | all 18 narrations | 3 mismatches, all pre-filed; no further ones (§3) |
| Booklet ↔ script sync | 問題1/2/5-2番 printed options vs script; all 5 問題 instructions + the 問題5-1番 lead-in | printed options match the dialogue in all cases; **all six instruction texts are character-for-character identical between `聴解.md` and `聴解スクリプト.txt` AND identical to `jlpt-exam-structure`'s canonical table** — including 問題2 (no 「せんたくしを読んで」 drift) and 問題5 (「問題用紙にメモをとっても」 present). ✅ |
| Read every line aloud | all 45 script blocks | F-04, F-05, F-06, F-01, F-02 (+ minor: 問題1-2番 「本日体験授業を受けていただきましたが」 wants は) |
| Verbatim-copy check, both directions | test 3 vs `imported-n2-2025-07` and vs tests 1/2/4, at line and block level | **Clean.** The only shared blocks are mandated boilerplate (opening line, the five 問題N instructions, the four 例 confirmation lines, the 問題5 header, the 問題5-1番 lead-in, the closing line) plus the 問題5-2番 lead-in, which is shared *because* all four papers speak the line they shouldn't (pre-filed). Zero shared dialogue, monologue, 例 or option text. `make check`'s 例-uniqueness check also passes for test 3 (it FAILs for tests 1 and 2, which copied the official 問題1 例 byte-for-byte). ✅ |
| Structure validation | `validate_script()` | `script OK: 45 blocks, items 問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2` ✅ — no stray blank line inside any item block, all labels in `SPEAKER_MAP`, no answer reveal after a scored item |
| Step 6 spec audit | `logs/test_spec.json` | §6 |

### 5b. Grounding table — every 問題1–3 wrong option

Legend: ✅ = a script line raises it (reassigned / superseded / denied); ⚠ = only a
neighbouring word is raised, the option's own content is not; **✗ NOT IN SCRIPT** =
fabricated.

**問題1** (key marked ★)

| Item | Opt | Text | Grounding |
|---|---|---|---|
| 例 | 1 | 出張の資料を印刷する | ✅ 「はい、印刷は終わりました」 (already done) |
| | 2★ | ホテルに確認の電話をする | key — 「じゃあ、先にホテルへ電話しておきますね」 |
| | 3 | 新幹線のチケットを受け取りに行く | ✅ 「チケットなら僕が昼休みに行ってきたよ」 (reassigned) |
| | 4 | 男の人に資料を渡す | **✗ NOT IN SCRIPT** → F-20 |
| 1番 | 1 | エアコンを使わずに扇風機をつける | **✗ NOT IN SCRIPT** (no 扇風機) → F-08 |
| | 2 | 2時間のタイマーを設定してエアコンをつける | ⚠ タイマー raised (「タイマーを設定していたけど」), 「2時間」 invented |
| | 3 | 設定温度を下げてタイマーをつける | ✅ denied by 「設定温度を少し高めにして」 |
| | 4★ | 設定温度を高めにして朝までエアコンをつけ続ける | key — line 20/21 |
| 2番 | 1★ | 申込用紙に記入する | key — 「まずはこちらの申込用紙にご記入ください」 |
| | 2 | 受付で面談の日程を調整する | ✅ 「その後、受付で面談の日程を調整していただきます」 (later step) |
| | 3 | 初回授業の受講料を支払う | ✅ 「受講料のお支払いは初回授業の日で構いません」 (later) |
| | 4 | 体験授業の感想を書く | ⚠ 体験授業 raised, 感想を書く not → F-21 |
| 3番 | 1 | レジ前にポップを設置する | ✅ 「そのあと、レジ前のポップ作成をお願いするよ」 (later) |
| | 2 | 期限切れの食品を棚から回収する | ⚠ 「期限切れによる食品廃棄を減らす」 raised; 回収 not |
| | 3★ | 棚に専用のポスターを掲示する | key — 「まずは棚へのポスター掲示から始めて」 |
| | 4 | 手前取りを呼びかけるチラシを作成する | ⚠ 「手前取りの呼びかけ」 raised; チラシ not (ポスター/ポップ) |
| 4番 | 1★ | 開設申込書に記入する | key — 「まずこちらの開設申込書に…ご記入いただけますか」 |
| | 2 | 番号札を取って待つ | ✅ 「ご記入後に番号札をお取りになって少々お待ちください」 (later) |
| | 3 | 運転免許証を窓口に見せる | ✅ 「確認書類のご提示は番号がお呼びできた際に」 (later) |
| | 4 | 印鑑を押す | ✅ 「運転免許証と印鑑を持っています」 (raised, not asked for) |
| 5番 | 1 | 市民向けの利用案内パンフレットを作成する | ✅ 「パンフレット作成はその結果を見てからにしよう」 (postponed) |
| | 2★ | 駅の管理事務所に電話をして打診する | key — 「駅の管理事務所に連絡をとって打診してみてくれ」 |
| | 3 | アプリの登録方法をマニュアル化する | ⚠ 「アプリ登録で借りて」 raised; マニュアル化 not → F-22 |
| | 4 | 公共施設に傘のスポットを設置する | ✅ 「駅や公共施設へのスポット設置交渉」 (the negotiation is first) |

**問題2**

| Item | Opt | Text | Grounding |
|---|---|---|---|
| 例 | 1 | 体調が悪かったから | ✅ 「体調でも悪かったの?」→「いや」 |
| | 2 | 仕事が入ったから | ✅ 「仕事が入ったわけじゃないんだけどね」 |
| | 3 | 実家の用事で帰省したから | ✅ 「急に実家から両親が上京してきて」 (direction reversed) |
| | 4★ | 両親が上京してきたから | key |
| 1番 | 1 | 重い荷物を一人で持たないようにしたこと | **✗ NOT IN SCRIPT** (no 荷物) → F-09 |
| | 2 | 立ち作業をやめてすべて座り作業に変更したこと | ✅ 「小休止の際に椅子の併用」 (併用, not 全面変更) |
| | 3 | 休憩時間を2倍に増やしたこと | ⚠ 小休止 raised; 「2倍」 invented |
| | 4★ | 作業台の高さを自分の身長に合わせて調整したこと | key — 「特に作業台の高さを…一番効果的でした」 |
| 2番 | 1 | 自転車の購入費用が割引されること | **✗ NOT IN SCRIPT** → F-10 |
| | 2★ | 借りたポートと異なるポートへ返却できること | key |
| | 3 | 電動自転車が必ず無料で借りられること | **✗ NOT IN SCRIPT** → F-10 |
| | 4 | 保険の加入手続きが不要であること | **✗ NOT IN SCRIPT** → F-10 |
| 3番 | 1 | 中央のAゲート | ✅ 「紙のチケットをお持ちのお客様は中央のAゲートより」 |
| | 2★ | 西側のBゲート | key |
| | 3 | 東側の当日券窓口 | ✅ 「当日券の購入や…東側の当日券窓口に」 |
| | 4 | 南側の優先ゲート | ✅ 「車椅子をご利用のお客様は南側の優先ゲート」 |
| 4番 | 1 | 暗記した志望動機を完璧に素早く話すこと | ✅ 「用意してきた原稿をそのまま話そうとすると…」 (denied) |
| | 2 | 難しい専門用語をたくさん盛り込むこと | **✗ NOT IN SCRIPT** → F-11 |
| | 3★ | 相手の質問を正確に聞いて直接簡潔に答えること | key |
| | 4 | 抑揚をつけずに大きな声だけで話し続けること | **✗ NOT IN SCRIPT** → F-11 |
| 5番 | 1★ | 急速に天気が回復して晴れる | key |
| | 2 | 一日中激しい雨が降り続く | ✅ 「土曜日の朝にかけては…激しい雨」 (superseded) |
| | 3 | 雲が広がり夕方から雪になる | ✅ 「日曜日は…雲が広がりやすく、夕方から再び雨」 (day+雨→雪 swap) |
| | 4 | 暴風警報が発表される | **✗ NOT IN SCRIPT** → F-12 |
| 6番 | 1★ | 平日は仕事で立ち会えず、今週土曜の予約が埋まっていたから | key |
| | 2 | 工事費用が来週の土曜日だけ割引になるから | **✗ NOT IN SCRIPT** → F-13 |
| | 3 | 電気工事会社の都合で平日しか作業できないから | ✅ denied by 「来週の土曜日でしたら午前も午後も空いております」 |
| | 4 | マンション全体の停電が来週土曜日に予定されているから | **✗ NOT IN SCRIPT** → F-13 |

**問題3** (spoken options; 概要理解 distractors are word-echoes of the talk — that is
the official shape, so ⚠ here means "echo present, content absent", which is acceptable
for this 問題 type)

| Item | Opt | Echo in the talk |
|---|---|---|
| 例 | 1 通信教育の受講費用 | ⚠ 「講座」 echoed; 費用 absent |
| | 3 語学スクールの選び方 | ✅ 「語学やプログラミング」 |
| | 4 社会人の残業時間 | ✅ 「仕事で忙しい社会人」 |
| 1番 | 1 販売価格の値下げ | ✅ 「新システム」 |
| | 3 クライアントとの契約解除 | ✅ 「クライアントからの強い要望」 |
| | 4 開発部の新規採用計画 | ✅ 「開発部の男の人」 (narration) |
| 2番 | 1 料金改定の歴史 | ✅ 「料金割引キャンペーン」 |
| | 2 自転車の盗難防止対策 | ✅ 「自転車利用時のヘルメット着用」 |
| | 3 都市部の道路工事の計画 | ✅ 「都市部で急速に普及」+「改正道路交通法」 |
| 3番 | 1 保険金の給付手続きの迅速化 | ✅ 「生命保険や医療保険」 |
| | 2 損害保険のPR | ✅ 保険 echoed (but see F-30) |
| | 4 保険会社の社員研修 | ✅ 「保険会社の窓口」 (narration) |
| 4番 | 2 地下鉄の運賃改定 | ✅ 「地下鉄の主要駅」 |
| | 3 ビニール傘の製造コスト | ✅ 「使い捨てビニール傘」 |
| | 4 雨の日の電車の遅延対策 | ✅ 「突然の雨の際に」 |
| 5番 | 2 成人の平均通勤時間の変化 | ✅ 「成人の約4割が睡眠時間6時間未満」 |
| | 3 スマートフォンの最新機能 | ✅ 「就寝前のスマートフォン使用を控え」 |
| | 4 夜間のシフト勤務のメリット | ⚠ neither 夜間 nor 勤務 is in the talk |

**Totals: 57 wrong options audited — 12 fabricated (✗), 7 weak (⚠ in 問題1/2), 38 sound.**

### 5c. 聴解 topic table (step 5, listening rows only)

| Slot | Subject | Spec scenario | Repeat? |
|---|---|---|---|
| 問1-1 | 夜間エアコン・熱中症 | #1 web | — (test 4 later reuses it) |
| 問1-2 | 学習塾の入塾手続き | #2 pool | — |
| 問1-3 | スーパーの手前取り・食品ロス | #3 web | ≈ 問5-2 (食品の再分配) |
| 問1-4 | 銀行の口座開設 | #4 pool | — |
| 問1-5 | 傘シェアリング導入 | #5 web | **≡ 問3-4 → F-14** |
| 問2-1 | 職場の腰痛予防 | #6 web | — |
| 問2-2 | 自転車シェアリング | #7 web | **≡ 問3-2 → F-15** |
| 問2-3 | コンサート入場ゲート | #8 pool | — |
| 問2-4 | 面接の助言 | #9 pool | — |
| 問2-5 | 週末の天気予報 | #10 pool | — |
| 問2-6 | 電気設備点検の日程 | #11 pool | — |
| 問3-1 | システム仕様変更・納期延期 | #12 pool | — |
| 問3-2 | シェアサイクルのヘルメット | #13 web | **≡ 問2-2** |
| 問3-3 | 保険の見直し | #14 pool | — |
| 問3-4 | 駅の傘シェアリング拡大 | #15 web | **≡ 問1-5** |
| 問3-5 | 睡眠の質 | #16 web | **≡ tests/2 問2-1番 → F-16** |
| 問5-1 | 観光モデルコース | #17 pool | — |
| 問5-2 | 食品寄付イベント | #19 pool | ≈ 問1-3 |

Unused spec scenarios available for the repairs: #18 文房具:法人契約, #20 研修会での
グループワーク, #21 税務署:確定申告.

### 5d. `make check` output for test 3 — every line, with resolution

| Line | Scope | Resolution |
|---|---|---|
| FAIL 問題8 target grammar TOO_EASY (ばほど) | 言語知識 | out of scope (Gengo/Dokkai reviewer) |
| WARN （注N） above N2 band (便箋/割引/蘇る) | 読解 | out of scope |
| WARN （注N） circular definitions | 読解 | out of scope |
| FAIL 読解 length floors / 問題11 retrieval stems / 問題11 opinion Q / 読解 key length / 問題14 解説 / 問題9 tags | 読解 | out of scope |
| WARN 言語知識・読解.md 解説 quote not found | 読解 | out of scope |
| **FAIL 問題5 2番 lead-in is booklet-only** | 聴解 | pre-filed; confirmed, single instance (script:239) |
| **FAIL 聴解 narration gender vs SPEAKER_MAP ×3** | 聴解 | pre-filed; confirmed exactly 3, no further ones |
| **FAIL 問題1/2/4 test the sampled items — quick_response substitution** | 聴解 | pre-filed; confirmed the only substitution (§6). Root cause RC-10 added |
| **FAIL 聴解.mp3 script_sha None** | 聴解 | pre-filed; corroborated by mtimes (mp3 Aug 5 18:59 < script Aug 6 09:56) |
| **WARN built HTML records its source sha — 5 stamps missing** | both | **True positive on the stamp, but the artifacts are content-current**: I diffed `聴解.html` and `解答.html` against `聴解.md` by rendering both and comparing every 例/1番–6番 option list, the マークシート and the 解説 tables — all identical to the current markdown, including the repaired 問題1 例. So the missing stamp is a *provability* gap, not stale content, for the two 聴解 artifacts. Not filed as a content finding; the stamp should still be added. |
| (no WARN) 聴解 two-party one-voice | 聴解 | **This silence is itself a defect** — 問題5-2番 casts 職員(F+0%) and 女(F+4%) on the same voice, and 男1/男2 on the same voice, but the check only inspects items with exactly two labels. `GATE-WRONG`-adjacent, folded into RC-2(b). |

### 5e. Step 6 — spec audit (聴解 portion)

- **問題4 / `quick_response` (11 targets):** 10 of 11 match the paper exactly, in order.
  The single substitution is the pre-filed 「こちらこそ、いつもお世話になっております。」
  (paper 8番 = 「本日は遠方からお越しいただき、ありがとうございました。」). **No further
  substitution.**
- **問題1 / 問題2 / 問題3 / 問題5 scenarios (18 slots):** all 18 map 1-to-1 onto
  `listening_scenarios` #1–#17 and #19, **in spec order**, with no substitution. The
  three unused entries are #18, #20, #21 — a surplus, which the sampler allows.
- **Web-fact fidelity:** each `origin: web` scenario's `facts` are reproduced simplified
  and non-contradicted — e.g. #1's 「タイマーで途中切断せず朝まで適温で使い続けるのが
  望ましい」 → 妻's line 19; #7's 「借りたポートと異なるポートへ返却できる」 → line 78.
  One simplified fact per dialogue; no source sentence reproduced. ✅
- **Answer positions:** 30/30 match (§2). ✅
- Harvest URL spot-check **skipped** — see §6.

---

## 6. Skips (explicit)

1. **Harvest URL fetch (step 6.5 of the skill's provenance audit).** Not performed — no
   network use was authorized for this review and it is the one sampling step the skill
   permits. Note that `make check` independently FAILs `logs/seeds.json` for citing
   `https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf` twice, which is a
   harvest-integrity signal in the same family.
2. **言語知識・読解 (問1–71).** Out of scope by assignment; its `make check` FAILs are
   listed in 5d unresolved and belong to the Gengo/Dokkai reviewer.
3. **MP3 audio inspection.** I did not decode `聴解.mp3` to confirm which script version
   it speaks. The `script_sha: None` failure is pre-filed and the mtime ordering
   corroborates staleness; decoding would not change the required action (`make mp3 3`).
4. **Cross-test topic table for 読解/文字語彙 rows** (step 5's non-listening rows) — out
   of scope. The listening rows are in 5c.
5. **Level-band cross-check against `refs/Shinkanzen/*.pdf`** for F-29's three
   即時応答 items. I judged them off-band from their own content (no idiom, no keigo
   discrimination, no indirect refusal) rather than from the Shin Kanzen inventory; a
   PDF cross-check would strengthen but not change the call.
6. **I edited nothing.** Per the assignment I am a reviewer only; every fix above is a
   proposal for the fixing pass. Per `exam-qa-review` §Boundaries the reviewer may edit
   `exam-qa-review/SKILL.md` itself to record a new defect class — I did **not**, because
   the instruction to edit no file in the repo overrides. The classes worth adding there
   are: *a `SPEAKER_MAP` label spoken as a personal name*; *a 問題5 item whose answer
   requires no elimination*; and *a 得点の目安 threshold exceeding the question count*.
