# TEST 2 CHOUKAI: FAIL (22 findings, 8 automatic)

Reviewer: fresh-eyes QA, 聴解 half only (問題1–問題5, 30 scored answers + 4 例).
Read in full before any other tool call: `.agents/exam-qa-review/SKILL.md`,
`.agents/choukai-script-writing/SKILL.md`, `.agents/jlpt-exam-structure/SKILL.md`,
plus `SPEAKER_MAP` in `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py`.

**Entry condition not met.** `exam-qa-review` requires `make check` green before QA.
`python3 tools/check_consistency.py` currently exits FAILED with 43 problems, 10 of
them on `tests/2` (ledger draw counts, 読解 length floors, （注N） pairing, 問題11
stems, the four already-filed 聴解 items). I proceeded because the task assigned it;
recorded here as a process deviation per AGENTS.md §0.7.

---

## 1. Blind-solve diff (script + booklet options only, answer tables unread)

| 問題 | My answers | Key | Diff |
|---|---|---|---|
| 問題1 (例,1–5) | 例2 / 1,3,1,2,4 | 例2 / 1,3,1,2,4 | none |
| 問題2 (例,1–6) | 例2 / 2,1,1,2,3,4 | 例2 / 2,1,1,2,3,4 | none |
| 問題3 (例,1–5) | 例1 / 1,4,3,1,2 | 例1 / 1,4,3,1,2 | none |
| 問題4 (例,1–11) | 例1 / 1,2,3,2,3,2,3,1,1,3,1 | 例1 / 1,2,3,2,3,2,3,1,1,3,1 | none |
| 問題5 | 3 / 質問1=4 / 質問2=2 | 3 / 4 / 2 | none |

**0 mismatches on 30 items + 4 例.** That is not a pass signal: three items
(問題1-1番, 問題2-1番, 問題2-5番) I solved *without needing the audio*, because their
wrong options are not in the script at all — see F1–F3. 問題2-2番 I solved by
eliminating the three denied options, not by recognising the key — see F5.
問題3-例/3番/5番 were solvable from the narration line alone — see F13.

Marksheet 例 pre-marks match the announcer in all four 問題 (問題1 (2)=2番,
問題2 (2)=2番, 問題3 (1)=1番, 問題4 (1)=1番), and every 例 is answerable from its
printed/spoken options with the announced number supported by the dialogue.

---

## 2. Findings

**Already filed by `make check` — NOT re-filed:** 問題1 例 byte-identical to test 1's
and to `imported-n2-2025-07`'s; 問題5 2番 lead-in spoken; `script_sha: None` (stale
MP3); 問題2-6番 casting アナウンサー+専門家 on one voice.

| # | Item | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| **F1** | 問題1-1番 opt 3 | **AUTOMATIC** — 聴解 distractor not grounded in the dialogue | 「ボランティアガイドツアーの受付に並ぶ」. The script mentions only 音声ガイド, 「カウンターで専用端末を借りる方法」, 「本日窓口が大変混み合っておりまして」. No ボランティアガイドツアー exists anywhere in `聴解スクリプト.txt`. | Replace with an option the dialogue raises and kills, e.g. 「カウンターに並んで専用端末を借りる」 is already opt 4 — instead add a line 女:「解説パンフレットを先にお渡ししましょうか」 男:「いえ、結構です」 and key an option to it. |
| **F2** | 問題2-1番 opt 3 | **AUTOMATIC** — ungrounded distractor | 「就寝直前までスマホで動画を見てリラックスしたこと」. Script's only スマホ line is 「睡眠トラッキングアプリをスマホに入れてね」; no video-watching, no relaxation claim. | Ground it: add 男:「寝る前に動画を見るのはやめたけど、それは大して変わらなかったな」, or replace with 「アプリの通知で就寝時刻を早めたこと」 tied to a real line. |
| **F3** | 問題2-5番 opts 1 **and** 4 | **AUTOMATIC** — two of three distractors ungrounded; the item is answerable without listening | 「隣の部屋からの話し声が聞こえること」 and 「エレベーターの動作音が部屋まで届くこと」. Script names exactly three noises: 「外の車の音とか?」→「道路側は静かなんだけど」, 「階段を歩く足音やドアの開閉音…それは許容範囲かな」, 「上の階の部屋から聞こえる深夜のドタバタという足音」. Neither 隣室の話し声 nor エレベーター is said. | Rewrite opts 1/4 onto the two lines already in the script: 「道路側の車の音」(denied: 静か) and split 「階段の足音」/「ドアの開閉音」 into two options (both 許容範囲). |
| **F4** | 問題2 例 opts 1 and 3 | **AUTOMATIC** — ungrounded (and see F7) | Printed 「1. 仕事が忙しかったから」「3. 友達と電話でおしゃべりをしていたから」. The 例 dialogue says only 「熱も出なかったし」「前日の夜に遅くまで映画を見ちゃって、睡眠不足だった」. Neither work nor a phone call is mentioned. | Author a fresh 例 (see F7) whose four options all trace to its own lines. |
| **F5** | 問題2-2番 key (opt 1) | **AUTOMATIC** — keyed option the source does not state | Question: 「今回の防災訓練で特に改善すべき点として二人が合意したものはどれですか」. Key: 「**以前の**訓練で非常階段の避難ルート**確認**が不十分だったこと」. What the script actually agrees on: 男「次回は避難ルートの誘導手順を一番に改善しましょう」/女「ルートの周知徹底を優先しましょう」/女「ルートの事前周知が不十分でした」. The key names the *previous* training, and uses 確認 — the noun the script attaches to what was **fine** (「消火器の位置確認や避難場所への到着時間は問題なかった」). Solvable only by elimination. | Rewrite opt 1 by copy-paste from the deciding line: 「避難ルートの事前周知と誘導手順が不十分だったこと」. |
| **F6** | Whole 聴解 half | **AUTOMATIC** — a subject twice in the paper in any register | (a) **Cafeteria improvement twice**: 問題2-3番 「社内食堂のリニューアルで、最も強く要望されている変更は何ですか」 (options: ヘルシーメニュー / 値下げ / **営業時間の延長** / ドリンクバー) and 問題5-2番 「学食の改善案」 (options: テラス席 / **学食の夜間営業の延長** / 自販機 / キッチンカー) — same errand, overlapping option. (b) **役割分担 three times**: 問題1-3番 (フードドライブ準備の分担), 問題2-4番 (地域交流フェスタの担当分け), 問題3-2番 key 「合宿準備における役割分担とスケジュール共有の大切さ」. (c) **睡眠 twice, adjacent**: 問題2 例 (睡眠不足) then 問題2-1番 (睡眠の質). (d) **Cross-surface into 言語知識**: 問題6 #29 分担 keyed sentence 「イベントの準備作業をチームのメンバーで分担して進めた」 is 問題2-4番's scenario; 問題6 #26 あらかじめ is spoken verbatim in 問題4-5番 both in the prompt (「あらかじめ釘を刺しておいた」) and in the keyed reply (「そうですね、あらかじめ注意しておいた方がいいですね」). | Re-topic one of each pair from the unused `logs/ledger.json` scenarios for test 2 (「図書館:電子書籍サービスの説明」「プール:利用証の更新」「保育園:送迎時間の相談」「レンタカー:返却場所の確認」 are all undrawn-on-paper). Keep 学食 in 問題5 only. |
| **F7** | 問題2 例 (script + booklet) | **AUTOMATIC** — content copied from an `imported-*` official paper | Booklet options 「1. 仕事が忙しかったから」「2. 夜遅くまで映画を見ていたから」 are **byte-identical** to `tests/imported-n2-2025-07/聴解.md`'s 問題2 例 options (and to test 1's). The dialogue is the same item lightly reworded: official 「久しぶりに映画を見始めたら止まらなくなっちゃって。気がついたら朝の3時だったんだ」→ test 2 「前日の夜に遅くまで映画を見ちゃって、睡眠不足だったんだよね」. Same cause, same key text. Additionally 問題4 例 clones the official frame: official 「今日、ちょっと残業できる?」 with 1 accept / 2 negated verb / 3 past-tense verb → test 2 「今日、ちょっと付き合ってくれない?」 with 「いいよ、どこに行くの?」/「うん、付き合わないよ」/「そう、付き合ったんだ」. | Author fresh 例 dialogues for 問題2 and 問題4 from the item pool, not from the official paper. (問題1 例 already filed by the gate; the fix must cover all three.) |
| **F8** | Script + options, 3 places | **AUTOMATIC** — broken/unnatural Japanese | (a) 問題1-4番 opt 1 「相手の**留守電メッセージ**を残さずに切る」 — ungrammatical; needs 「相手の留守電**に**メッセージを残さずに切る」. (b) Script 問題2-4番: 女「**男の人に**お願いしたいのは、当日の来場者受付と…なの」 — she is addressing him to his face; no Japanese speaker calls the present interlocutor 男の人. (c) Script 問題1-4番: 男「社名と**お名前**を伝えて…」 — 尊敬 prefix on his own name; must be 「社名と名前を伝えて」. | (a) insert に; (b) 「田中さんにお願いしたいのは」; (c) drop お. |
| F9 | 問題5-2番 block (script line 283) | Major structural — pacing corruption | 「これで、聴解試験を終わります。」 has **no blank line before it**, so it lives inside the `2番。` item block (block 43 = 12 lines). `gap_before_line()` gives it the ordinary 1.3 s gap and `pause_after()` fires the 問題5 10 s answer pause **after** the closing announcement. Examinees get 1.3 s to answer 質問2 and then hear that the exam is over. | Insert a blank line before the closing so it is its own block. |
| F10 | 問題5 header block (script lines 253–255) | Structural — parser contract | `問題5。` + the section instruction + the 1番 lead-in 「問題用紙に何も印刷されていません。…では、始めます。」 are all ONE block. `choukai-script-writing` §"Required structure" requires the 1番 lead-in to be **its own block between the instruction and `1番。`**, and §"Block conventions" requires `問題N。` and the instruction to be separate blocks. All five 問題N headers share a block with their instruction (blocks 2,10,19,27,41). | Split into three blocks for 問題5 and two for 問題1–4. |
| F11 | 問題1-5番 opts 1, 3 | Distractor plausibility (step 2b) — eliminable for a reason unrelated to the tested point | 「航空券の手配をキャンセルする」/「宿泊先をビジネスホテルに変更する」 both presuppose an existing booking, which the dialogue explicitly denies: 男「ホテルや飛行機の手配が**先だと思っていました**」 — nothing has been booked, so nothing can be cancelled or changed. ビジネスホテル is never said. | Reword to raised-then-superseded actions: 「宿泊先のホテルを予約する」/「飛行機の手配をする」 (both raised, both superseded by 「まず社内の専用申請書を出して承認を得る必要があるの」). |
| F12 | 問題5-2番 casting | Voice/narration | Labels 先生 (FEMALE, +0%) and 女 (FEMALE, +4%) both appear in a three-party item, and 質問2 asks about 「女の学生」. The examinee must separate the female student from the female teacher by 4% speech-rate alone. `make check`'s one-voice warning is scoped to **two-party** items, so it does not see this. | Recast 先生 as a male-mapped label (e.g. 教授, MALE −6%) or give the item 男1/男2+女. |
| F13 | 問題3 例, 3番, 5番 narration | 概要理解 answer leak | 例: 「女の人が**部屋の模様替えについて**話しています」 → key 「部屋の模様替えの工夫」 — the demonstration item is answered by its own narration. 3番: 「アナウンサーが**物流の取り組みについて**話しています」; 5番: 「講師が**新しい店舗形態について**話しています」 → in 5番 opts 3 (スマホ操作教室) and 4 (センサーの販売価格) die on the narration alone. Official practice avoids this: `imported-n2-2025-07` 例 says 「街頭で女の人が**ある商品について**話しています」. | Narrate setting + speaker only: 「女の人が話しています」/「アナウンサーが話しています」/「講師が話しています」. |
| F14 | 問題2-6番 | 理由 question keyed to a description, not the stated reason | Question: 「アップサイクルファッションが注目されている一番の理由」. The script's stated reason is 「特に若者の間で、環境負荷を減らしつつ自分だけの個性を表現できることが高く評価されています」 — **no option offers it**. The key (opt 4 「回収した服を新しいデザインのバッグや小物へ再利用すること」) is the *definition* of upcycling, resting on 「古着を新しいデザインの製品へ再利用することが一番の魅力です」. | Either make opt 4 「環境負荷を減らしながら個性を表現できること」 (the stated reason) or delete the 高く評価されています line so only one reason stands. |
| F15 | 問題2-1番 key (opt 2) | Key bundles a non-cause | Key: 「睡眠アプリで**呼吸を計測し**毎朝の起床時間を揃えたこと」. The script's stated cause is only the second half: 「『毎朝起きる時間を休日も平日も揃える』ようにしたんだ。これが一番効果的だったよ」. 呼吸の計測 is the vehicle, never the reason. | Trim to 「毎朝の起床時間を休日も平日も揃えたこと」. |
| F16 | 問題3-5番 key (opt 2) | Key names a thing the script never says | Key: 「**AI決済ロボット**導入による店舗業務の効率化と利便性」. Script: 「レジを通さずに買いものができる『無人決済店舗』や**AI接客ロボット**の導入」 — two different things fused into a third that is spoken nowhere. | 「無人決済店舗やAI接客ロボットの導入による店舗業務の効率化と利便性」. |
| F17 | 問題2-4番 | 問題-to-question-type mapping | Stem: 「男の人は当日、どの役割を担当しますか」. `choukai-script-writing` §"The 問題 decides the QUESTION TYPE" lists 問題2 shapes as 「どうして〜か / 何が一番〜か / どのように説明していますか」; a "what will you do" stem belongs to 問題1's 課題理解 family. The dialogue is also a task-assignment conversation (設営→学生, 資料/弁当→事務局, 受付+誘導→男). | Either re-shape to a ポイント理解 stem (「女の人は男の人に何を一番期待していますか」) or move the item to 問題1 and re-order options to the prescribed answer position. |
| F18 | 問題5-1番 opt 4 | Ungrounded option (問題5) | 「経理部の窓口へ直接領収書を持ち込む」. The script never mentions 経理部 or a counter; the only paper-receipt line is 「紙の領収書は部署ごとにまとめて毎月保管するらしい」. | Reword to 「紙の領収書を部署ごとにまとめて経理に提出する」 (raised, but not the申請方法) or add a denial line. |
| F19 | 問題4-6番 key (opt 2) | Keyed reply presupposes an impossible action | Prompt: 「議事録、**作成いたしましたが**、ご確認いただけますか」 (submitted just now). Key: 「**確認したよ**。要点がよく整理されているね」 — a completed check of a document handed over in the same breath. Opt 1 is the keigo trap, opt 3 contradicts 作成済み, so the item is solvable by elimination while the key itself is unnatural. | Key a forward-looking reply: 「ああ、ありがとう。あとで目を通しておくよ」. |
| F20 | 問題4-7番 opt 1 | Weak second reading | 「いえ、全員揃ってから始めます」 functions as an implicit refusal of 「少し遅れて参加してもよろしいでしょうか」, so it is arguably answerable; it survives only because 「全員揃ってから始めます」 in fact accommodates a late arrival. | Replace with a clearly impossible reply, e.g. 「はい、懇親会は昨日でしたね」. |
| F21 | 問題4-2番 / 問題4-1番 wording; 問題4-10番 level | Minor naturalness / band | (a) 「明日の野外イベントの件ですが、あいにく天候が**悪化して**見合わせることになりました」 — tomorrow's weather stated as accomplished fact; 「悪化する見込みで」. (b) 「採算が取れるか二の足を踏んでしまうよ」 — 二の足を踏む takes a に-marked action; an embedded question needs 心配で/不安で between them. (c) 10番 「お先に失礼いたします」→「お疲れ様でした。お気をつけて」 is an N4-band exchange; 1 of 11 即時応答 items below the N2 band (`exam-qa-review` step 2.5). | (a)/(b) reword; (c) swap in the unused ledger item 「明日の打ち合わせ、オンラインでの参加でもよろしいでしょうか。」 — see F22. |
| F22 | Spec / ledger provenance | Draw–paper mismatch | `logs/test_spec.json` on disk describes **test 3**, so the check ran against `logs/ledger.json` history entry `test_id: "2"` (seed 20260804, harvest_sha `harvest_20260804`). `quick_response` records **12** items for 11 slots: 11 are used (with two elaborations — 「課長、この件は私の力不足でした。申し訳ございません。」 shipped as 「今回のシステム障害の件…大変申し訳ございません」, 「先方のご要望に沿えるよう、もう一度検討してみます。」 gained チームで), item 12 「明日の打ち合わせ、オンラインでの参加でもよろしいでしょうか。」 is **unused**, and the 例 is off-pool. `listening_scenarios` records 20 (gate says DRAW is 21) and 7 authored 聴解 items match none of them: 薬局ののど薬 (問題1-2番), ワーケーション申請 (問題1-5番), 睡眠アプリ (問題2-1番), アップサイクル (問題2-6番), 地域商品券 (問題3-1番), 置き配 (問題3-3番), 無人決済店舗 (問題3-5番). 「博物館:展示解説の音声ガイド」 shipped as 美術館. `make check` independently FAILs test 2 on the same ledger counts. | Re-sample or record the substitutions; do not hand-edit the ledger to match the paper. |

**Keigo-direction check requested explicitly:** the previously reported "社長 speaking
humble keigo downward" is **no longer keyed**. 問題4-4番's key is 「分かりました。では、
会議室で聞かせてください」 (neutral-polite, correct downward) and 問題4-7番's key is
「ええ、仕事が落ち着き次第、お越しください」 (尊敬語, acceptable downward). The humble-
downward form now appears only as 問題4-6番's **distractor** 1 「かしこまりました。すぐに
拝見いたします」, correctly explained in the 解説. Defect resolved; F19 is a different
defect in the same item.

Minor, recorded but not counted as a finding: 解説 for 問題4-10番 quotes 「お先に失礼
します」 where the script says 「お先に失礼**いたします**」 (8 JP chars, below
`check_explanation_quotes`'s 14-char threshold, so the gate is right not to see it);
問題2-4番 opt 4 adds 「懇親会の」/「お茶」 to a line that says only 「お弁当の手配」;
問題1-1番 opt 2 adds 「企画展の特別」 to 「入場チケットの購入」.

---

## 3. Root-cause table (step 6.5)

| Findings | Code | Tests on disk showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|
| F1, F2, F3, F4, F11, F18 (ungrounded / on-sight-eliminable 聴解 options) | `RULE-UNENFORCEABLE` + `GATE-BLIND` | 4/4 (the skill itself records t1 問題2-1番, t2 ×5, t3 ~14, t4 問題2 例) | `.agents/choukai-script-writing/SKILL.md` §"The keyed option must be quotable"; `tools/check_consistency.py` | The skill already prescribes the grounding format `1 ✗「script line」→ 別の人に割り当て`, and **test 2 uses it in zero of its 16 問題1–3 解説 cells** — prose narration passed instead. Make it a contract, not a suggestion: (1) in the skill, state "a 問題1/2/3 解説 cell that is not exactly three `N ✗「…」→ 理由` lines is not shippable"; (2) add `check_choukai_option_grounding()` to the gate — for every 問題1–3 item, require exactly 3 lines matching `^\s*([1-4]) ✗「(.+?)」`, that the three digits are the non-key positions, and that each quoted span occurs in `聴解スクリプト.txt`. This is decidable against a file we author, so it FAILs (unlike the token-overlap WARN, which is calibrated on paraphrase and must stay a warning). |
| F5, F15, F16 (key does not restate the deciding line) | `RULE-IGNORED` + `GATE-BLIND` | 4/4 (t4 問題1-5番 点検作業員/管理事務所 is the same shape) | `.agents/choukai-script-writing/SKILL.md` §"Quotable"; `tools/check_consistency.py` | Rule exists and was skipped, so no skill text is missing — but add the mechanical half: for 問題1–3, compute the best character-overlap between the keyed option and any single script line in that item's block; WARN under 50% (measured on `imported-n2-2025-07` before setting the threshold). That flags F5/F15/F16 without touching legitimate paraphrase. |
| F6 (within-paper topic repetition, incl. cross-surface into 問題6) | `RULE-UNENFORCEABLE` + `GATE-BLIND` | 4/4 (t4 apartment-hunting in 問題1-4番 and 問題5-3番) | `.agents/jlpt-test-generation/SKILL.md` §"One topic, one surface"; `tools/check_consistency.py` | The whole-paper table is a manual pass with no artifact, so it is skipped invisibly. (1) Require the table to be **written to `logs/topic_table_<test_id>.md`** with one row per 聴解 item + one per 読解 surface + one per 問題6 usage key — a pass with no file is a skipped pass. (2) Add a gate check: extract content nouns from each 聴解 item's narration line and each 問題6 keyed sentence; FAIL when two rows share ≥2 content nouns (食堂/学食, 分担/役割, 睡眠). |
| F7 (copying `imported-*` / official material) | `GATE-WRONG` (under-scoped) | 3/4 (t1 and t2 問題1 例; t1 問題2 例 vs official) | `tools/check_consistency.py` | The existing check compares `例。` blocks **byte-identically** only, so a light rewrite and a copied *option list* both pass. Extend it: (a) `difflib.SequenceMatcher` ratio ≥0.60 between any two tests' 例 blocks FAILs; (b) compare `聴解.md` option lines across all tests incl. `imported-*` — a byte-identical option line of ≥6 JP chars FAILs. Both would have caught F7. Re-verify every test that passed the byte-identical version. |
| F8 (broken Japanese in a script line and an option) | `RULE-IGNORED` | 2/4 (t4 shipped six broken sentences) | none — `exam-qa-review` step 3 already says "read the whole paper aloud once" | Not mechanizable; it stays a human read. Worth naming in `choukai-script-writing`: "no line may refer to a speaker present in the conversation as 男の人/女の人 — use their name or drop the phrase", which *is* string-decidable and could be a WARN (`(男|女)の人に(お願い|頼み)` inside a dialogue line). |
| F9, F10 (block contract: closing line inside an item block; lead-in and 問題N headers merged) | `GATE-BLIND` | 1/4 for F9 (test 2 only — checked t1/t3/t4 block lists); 4/4 for merged 問題N headers | `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py` `validate_script()` | All three are string-decidable and none is checked. Add: (1) the last block must be exactly `これで、聴解試験を終わります。` on one line (today the CLOSING test is a substring search over the whole text, which is why the line hides inside 問題5-2番 and eats its answer pause); (2) `^問題[1-5]。$` must be a **single-line** block; (3) for 問題5, a block whose first line starts 「問題用紙に何も印刷されていません」 must exist between the instruction block and `1番。`. |
| F12 (same-voice pair in a ≥3-party item) | `GATE-WRONG` (scope) | 2/4 (t1 three two-party pairs, t4 問題1-4番) | `tools/check_consistency.py` + `.agents/choukai-mp3-generation/SKILL.md` §Casting | Today's WARN only inspects **two-party** items. Change it to: for every item block, group its labels by resolved `(voice, rate)` and WARN when any group has ≥2 labels and the rates are within 6% — regardless of how many parties the item has. |
| F13 (問題3 narration names the topic) | `RULE-MISSING` | 4/4 (checked t1/t3/t4 問題3 narrations — all name the topic in ≥2 items) | `.agents/choukai-script-writing/SKILL.md` §"The 問題 decides the QUESTION TYPE" | Add a row/sentence: "問題3 (概要理解) narration states **setting + speaker only**. Official: 「テレビで男の人が話しています」/「街頭で女の人が**ある商品**について話しています」. If the narration must name a subject, use an indefinite (ある商品/あることについて). No content word in the narration may reappear in any option." Gate half: WARN when a 問題3 narration content word ≥2 JP chars appears in the keyed option. |
| F14 (理由 keyed to a description while the stated reason is unoffered) | `RULE-UNENFORCEABLE` | 2/4 (t4 問題2-4番 keyed the measure, not the cause) | `.agents/choukai-script-writing/SKILL.md` §"A 理由 question must be keyed to the CAUSE" | The rule covers cause-vs-measure but not cause-vs-definition. Extend it: "If the script contains a sentence of the form 〜が(高く)評価されています/〜が理由です/〜からです, **that sentence must be the key**. A key resting on 〜が一番の魅力です while an explicit evaluative reason goes unoffered is a mis-key." |
| F17 (問題2 carrying a 課題理解 stem) | `RULE-UNENFORCEABLE` | 2/4 (t4 shipped 問題1↔問題2 swapped) | `.agents/choukai-script-writing/SKILL.md` question-type table; `tools/check_consistency.py` | The table lists allowed shapes but no closed list to check against. Make it closed and gate it: 問題1 stems must end 「何をしますか/何をしなければなりませんか」; 問題2 stems must match 「どうして」「何が一番」「どのように」「何だと言っていますか」「何が…と言っていますか」; 問題3 stems must be 「何について話していますか/説明していますか」. FAIL on any 問題1–3 stem outside its section's list — 「どの役割を担当しますか」 is then caught at build time. |
| F19, F20, F21 (即時応答 reply logic / band) | `RULE-MISSING` | not surveyed across tests (聴解-only scope) | `.agents/question-authoring/SKILL.md` 即時応答 section | Add a construction rule: "the keyed reply must be performable **at the moment of speaking** — no reply may assert a completed action the prompt just introduced (「作成いたしました」→「確認したよ」)", and "each of the two wrong replies must be impossible, not merely unlikely; a reply that could be read as an implicit yes/no to the prompt is a second answer." |
| F22 (draw–paper mismatch; unused drawn item) | `GATE-WRONG` / `PIPELINE-GAP`, already failing | 3/4 (gate FAILs t2, t4, t4-removed on draw counts; t3 on a substituted 即時応答 item) | `tools/check_consistency.py` + `.agents/item-pool-sampling/SKILL.md` | The gate compares ledger counts to `DRAW` but nothing checks that every drawn 聴解 item **appears in the paper**, and for test 2 the spec-vs-paper target check cannot run at all because `logs/test_spec.json` holds only the newest test. Propose: persist per-test specs as `logs/test_spec_<test_id>.json` (keeping `logs/test_spec.json` as a symlink/copy of the current one) so the 問題1/2/4 target audit is runnable for **every** test on disk, not just the last one authored. |

---

## 4. Coverage — 問題1–3 distractor grounding (every wrong option)

`✓` = line quoted from `tests/2/聴解スクリプト.txt`; `✗` = NOT IN SCRIPT.

**問題1** (key in brackets)
| Item | Opt | Grounding |
|---|---|---|
| 例 [2] | 1 | ✓「作文は来週でいいですよ」 |
| | 3 | ✓「先生、答えはノートに書きますか」 |
| | 4 | ✓「今からプリントを配りますから」 |
| 1番 [1] | 2 | ✓「入場チケットの購入、ありがとうございました」(already done; 「企画展の特別」 invented) |
| | 3 | **✗ NOT IN SCRIPT** (F1) |
| | 4 | ✓「カウンターで専用端末を借りる方法」+「端末のレンタルは500円」「貸出まで少々お時間をいただいております」 |
| 2番 [3] | 1 | ✓「そのあとで、成分が重ならないのど薬をお選びします」 |
| | 2 | ✓「急がれるなら後でも大丈夫です」 |
| | 4 | ✓「相談カウンターでの詳細説明は、薬が決まってからにしましょう」 |
| 3番 [1] | 2 | ✓「届け出はもう先週済ませてあります」 |
| | 3 | ✓「店長さんとの約束が来週なので、まだ動けません」 |
| | 4 | ✓「集まった食品を数えて記録するのは、当日の作業にしましょう」 |
| 4番 [2] | 1 | ✓ negation of 「留守電かメッセージを入れておきましょうか」/「それが一番確実ですね」 (ungrammatical — F8a) |
| | 3 | ✓「携帯の電波が不安定な場所にいらっしゃるみたいでしたよ」 |
| | 4 | ✓「メールは後で大丈夫です」 |
| 5番 [4] | 1 | **✗** presupposes a booking denied by 「ホテルや飛行機の手配が先だと思っていました」 (F11) |
| | 2 | ✓「現地のコワーキングスペースや宿泊先のホテルは自分で予約するんですよね」→ superseded |
| | 3 | **✗** ビジネスホテル never said; no booking to change (F11) |

**問題2**
| Item | Opt | Grounding |
|---|---|---|
| 例 [2] | 1 | **✗ NOT IN SCRIPT** (F4) |
| | 3 | **✗ NOT IN SCRIPT** (F4) |
| | 4 | ✓「熱も出なかったし」 |
| 1番 [2] | 1 | ✓「高いまくらでも買った?」/「いや、まくらは変えてないんだ」 |
| | 3 | **✗ NOT IN SCRIPT** (F2) |
| | 4 | ✓「就寝前の筋トレは逆に目が冴えちゃって良くなかったけど」 |
| 2番 [1, defective — F5] | 2 | ✓「ヘルメットの配布や安否確認はスムーズでしたね」(quantity never addressed) |
| | 3 | ✓「消火器の位置確認…問題なかった」 |
| | 4 | ✓「避難場所への到着時間は問題なかった」 |
| 3番 [1] | 2 | ✓「価格についての意見はそれほど多くありませんでした」 |
| | 3 | ✓「営業時間の延長…を求める声もありましたが」 |
| | 4 | ✓「ドリンクバーの設置を求める声もありましたが」 |
| 4番 [2] | 1 | ✓「設営はボランティアの学生さんたちがやってくれることになったの」 |
| | 3 | ✓「資料やお弁当の手配は事務局で済ませてあるわ」 |
| | 4 | ✓ same line (「懇親会の」「お茶」 invented) |
| 5番 [3] | 1 | **✗ NOT IN SCRIPT** (F3) |
| | 2 | ✓「階段を歩く足音やドアの開閉音も時々聞こえるけど、それは許容範囲かな」 |
| | 4 | **✗ NOT IN SCRIPT** (F3) |
| 6番 [4] | 1 | ✓「海外からの輸入古着やリサイクルも一般的ですが」 |
| | 2 | ✓「単に中古品として再販売したり、処分したりするのではなく」 |
| | 3 | ~ only generic 「リサイクル」; 「化学繊維の原料に分解」 invented |

**問題3** (spoken options; official style raises each topic word in passing)
| Item | Opt | Grounding |
|---|---|---|
| 例 [1] | 2 | ✓「高価な家具を買わなくても」 |
| | 3 | ~「窓の近くにデスクを移動させると」(掃除 invented) |
| | 4 | ~「クッションやカーテンを選ぶと」(洗濯 invented) |
| 1番 [1] | 2 | ✓「大型ショッピングモールとの競争が激しい中」 |
| | 3 | ✓「スマートフォンで利用できる電子商品券も導入し」 |
| | 4 | ~「商店街」(閉店対策 invented) |
| 2番 [4] | 1 | ~「会計、部屋割り、食事手配」(値下げ交渉 invented) |
| | 2 | ~ same line (予約変更 invented) |
| | 3 | **✗** サークル/募集 never said |
| 3番 [3] | 1 | ~「ネット通販の拡大に伴い」(価格高騰 invented) |
| | 2 | ✓「ドライバー不足が課題となっています」 |
| | 4 | ✓「宅配ボックスの利用が標準化されつつあります」(補助制度 invented) |
| 4番 [1] | 2 | ✓「マイナンバーカードをお持ちであれば」 |
| | 3 | ~「病院や薬局の領収書」(診察券 invented) |
| | 4 | ~ same line (割引 invented) |
| 5番 [2] | 1 | ✓ inverted from 「人手不足や人件費の高騰に対応するため」 |
| | 3 | ✓「高齢のお客様への操作サポート」 |
| | 4 | ✓「天井のカメラやセンサーで商品を識別し」(販売価格 invented) |

**Other checks run and their result**

- **Booklet ↔ script instruction sync (verbatim):** 問題1/2/3/4/5 and the 問題5 1番 lead-in are character-for-character identical between `聴解.md` and `聴解スクリプト.txt`, and all six match `jlpt-exam-structure` §"問題N instruction lines" canonically (the three drifts previously recorded for test 2 — 「どのような内容か」, 「文章がやや長くなります」, 問題4 missing 「まず…それから」 — are all gone). 問題5 2番's line is booklet text spoken aloud — already filed.
- **Printed vs spoken choices:** no `^[1-4]、` line in 問題1/問題2 (correct); present in 問題3, 問題4, 問題5 1番 (correct); absent in 問題5 2番 (correct).
- **Structure counts:** 44 blocks; item blocks 問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2 = 33 ✓. Every 問題1–4 has one 例 and one full confirmation line ✓. No bare 最もよいものは◯番です after a scored item ✓. No `（※…）` annotations ✓. No ASCII `,`/`.` ✓. Every item's dialogue sits in its marker's own block ✓ (the historic 問題2 20 s option-reading bug is not present).
- **Narration ↔ SPEAKER_MAP:** all 33 items checked. No 「〈label〉の男/女の人」 contradiction. Female-mapped labels used with female narration (店員/専門家/アナウンサー/担当者/講師/先生/女), male-mapped with male (男/学生). Same-voice pairs: 問題2-6番 (アナウンサー+専門家 — already filed) and 問題5-2番 (先生+女 — F12).
- **Verbatim-copy diff** (item blocks, `difflib` ratio >0.55, both directions, vs `tests/1`, `tests/3`, `tests/4`, `tests/imported-n2-2025-07`): exactly one full-block match — 問題1 例 vs test 1 and vs the official paper (already filed). Booklet option lines diffed the same way: 問題1 例 (4 lines) and 問題2 例 (2 lines) identical to test 1 **and** to the official paper → F7. All other 30 items and their options are original.
- **Artifact staleness:** `sha1(聴解スクリプト.txt)[:12] = b00c46d5b7af`; `聴解_チャプター.json` carries **no `script_sha` key at all** (only `duration` + 38 chapters). Git corroborates real staleness: script and `聴解.md` last committed 2026-08-05 19:00:28 (the commit that rewrote the 問題 instructions), MP3 and chapter JSON at 2026-08-05 17:47:51 — the shipped audio speaks the **pre-update** instructions. Already filed; evidence added. `聴解.html`/`解答.html` are in the same commit as `聴解.md` and their rendered text matches it (checked after stripping `<rt>`/tags: 「エレベーターの動作音」「隣の部屋からの話し声」「問題2では、まず質問を…」 each present once), so the HTML is *not* content-stale despite the inverted mtimes; no `src_sha` stamp exists to prove it either way (gate WARN, valid).
- **Level band (即時応答):** 二の足を踏む, 見合わせる, 釘を刺す, 力不足, ご説明させていただきます, ご確認いただけますか, お任せいただけますでしょうか — all N2-band. One item below band (10番, F21c). None N1.
- **make check WARNs touching 聴解 test 2:** exactly one — 「6番。ラジオでア ['アナウンサー', '専門家'] — both labels resolve to one voice」. Already filed; confirmed true, not a false positive (both are FEMALE, +4% vs +0%).

---

## 5. Skips (explicit)

1. **言語知識・読解 items (Q1–71)** — assigned to another reviewer. I opened
   `tests/2/言語知識・読解.md` only to check cross-surface leakage for F6 (問題6 #26
   あらかじめ, #29 分担) and read nothing else there.
2. **Cross-test topic table** — assigned to another reviewer. I built only the
   within-paper 聴解 table (F6) and ran the text-level copy diff against tests 1/3/4
   and `imported-n2-2025-07`.
3. **`logs/test_spec.json` target audit** — the on-disk spec describes **test 3**, so
   per instructions I used `logs/ledger.json`'s `test_id: "2"` history entry instead
   (F22). The 101-position `answer_positions` audit is therefore **not possible** for
   test 2 and is skipped for that reason.
4. **Harvest URL spot-check (step 6.5)** — outside 聴解 scope; note that
   `make check` FAILs `logs/seeds.json` on a reused URL
   (`https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf`).
5. **Audio listening** — I did not play `聴解.mp3`. All pacing claims (F9) are derived
   from the block structure applied to `gap_before_line()`/`pause_after()`/
   `ANSWER_PAUSE` in `make_choukai_mp3.py`, not from measurement.
6. **No file was edited.** Review only, per assignment — including
   `.agents/exam-qa-review/SKILL.md`, which this skill would normally allow the
   reviewer to extend (F13's 問題3-narration-leak class is absent from its
   automatic-fail list and should be added by whoever applies these findings).
