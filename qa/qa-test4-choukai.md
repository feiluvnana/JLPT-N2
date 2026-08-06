# TEST 4 CHOUKAI: FAIL (22 findings, 11 automatic)

Reviewer: fresh-eyes QA subagent. Authored nothing in this test. **No file in the repo was edited.**
Read in full before any other tool call: `.agents/exam-qa-review/SKILL.md`, `.agents/choukai-script-writing/SKILL.md`, `.agents/jlpt-exam-structure/SKILL.md`, plus `SPEAKER_MAP` in `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py`.

**Entry-condition violation (reported, not waived):** `exam-qa-review` requires `make check` green before QA starts. It is **not** green — `make check` exits 1 with **43 problems + 15 warnings**, six of them on test 4 (four 読解, two 聴解). QA was run anyway per the task instruction; the 聴解 half is reviewed below.

---

## 1. Blind-solve diff

Solved from `tests/4/聴解スクリプト.txt` + the printed options in `tests/4/聴解.md` lines 1–143, **before** reading the key tables (lines 144–263).

| 問題 | reviewer | key | diff |
|---|---|---|---|
| 問題1 1–5番 | 4, 1, 1, 2, 3 | 4, 1, 1, 2, 3 | — |
| 問題2 1–6番 | 1, 2, 3, 1, 4, 2 | 1, 2, 3, 1, 4, 2 | — |
| 問題3 1–5番 | 1, 3, 1, 2, 4 | 1, 3, 1, 2, 4 | — |
| 問題4 1–11番 | 1, 3, 3, 1, 2, 1, 3, 2, 2, 1, 2 | 1, 3, 3, 1, 2, 1, 3, 2, 2, 1, 2 | — |
| 問題5 1番 / 2-質問1 / 2-質問2 | 1, 4, 2 | 1, 4, 2 | — |
| 例 (問題1/2/3/4) | 2, 4, 2, 1 | announced 2, 4, 2, 1; marksheet pre-marks 2, 4, 2, 1 | — |

**30/30 + 4/4 例 agree. Zero mismatches.** No mis-key was found — the mis-keys the earlier review reported (問題1-5番 点検作業員, 問題2-4番 measure-not-cause) are genuinely repaired. Note that agreement is a *low* bar here: findings C5, C6, C13 below are items I answered correctly *without* the dialogue mattering.

**解説 quote audit (step 1):** 74 quoted spans in the key section; 7 do not match literally. All 7 are false positives, verified by splitting: 4 are ellipsis-elided quotes (`窓口へお越しいただく方法もございますが…あまりおすすめできません` etc.) whose **both halves are present verbatim**, 3 are dictionary glosses, not quotes (`知っています`, `板につく`, `願う`). **No invented quote remains** — the "five 解説 quotes the audio never speaks" defect is fixed.

---

## 2. Findings table

Class key: **AUTO** = automatic fail per `exam-qa-review` "Ground rules"; **MAJ** = major; **MIN** = minor.

| # | Item | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| C1 | 問題2 例, option 2 | **AUTO** ungrounded distractor | Printed `2. 色が気に入ったから`. `色` occurs **once in the whole script**, in the 問題3 例 (靴: 「デザインや色も大切ですが」) — never in the バッグ dialogue. | Replace with an option the bag dialogue raises and kills, e.g. `革の質感がよかったから` (「革の質感がいいね」— said by 女, never given as 男's reason). |
| C2 | 問題1 例, option 4 | **AUTO** ungrounded distractor | Printed `4. 日程を全員に知らせる`. Nothing in the 忘年会 dialogue raises notifying anyone; 「金曜日だから混むかもしれないし」 mentions the day only. | Replace with `参加費を集める` **and add the line that kills it**, or use `人数をまとめる` (already reassigned: 「人数は僕がまとめておくから」) — note option 1 already occupies that slot, so a new line is needed. |
| C3 | 問題4 例 | **AUTO** verbatim copy from an imported paper | `tests/4`: 「例。今日、ちょっと残業できる？」 vs `tests/imported-n2-2025-07`: 「例。今日、ちょっと残業できる?」 — identical but for the question-mark width. Tests 1/2/3 authored their own 問題4 例; only test 4 copied. | Author a fresh 例 stimulus. The ledger's 12th `quick_response` draw is unused and available. |
| C4 | 問題2-5番, 問題1-4番, 問題2-3番 | **AUTO** topic repeats the previous test | vs `tests/3`: 問題2-2番「ラジオで…**自転車シェアリング**サービスについて…好評な一番の理由」 ↔ t4 問題2-5番「…**自転車シェアリング**について…何に不満」 (same subject, same 問題, mirrored question). t3 問題1-5番「市役所で…**使い捨て傘**削減事業」 ↔ t4 問題1-4番 傘シェアリング＋「売店では**使い捨て**ビニール傘も」 (same 問題). t3 問題1-1番「夏の**熱中症**対策…今夜寝る時に」 ↔ t4 問題2-3番「**熱中症**予防…**夜間のエアコン**」 (same decisive content). | Re-author these three items on unused drawn scenarios. Chronology note: t4 was drawn 08-04, t3 regenerated 08-05, so the collision was introduced by the t3 regeneration — but the two papers cannot both ship as-is. |
| C5 | 問題1-3番 ↔ 問題1-4番 | **AUTO** subject twice in this paper | 3番:「参ったな、**急に雨が降ってきた**よ」→ key 「スマホで配車アプリをダウンロードする」. 4番:「**急に雨が降ってきた**んですが」→ key 「スマホのアプリで会員登録をする」. Adjacent items, same trigger, same key shape. | Re-author 4番 on a different trigger and a non-app action. |
| C6 | 問題1-4番 ↔ 問題2-5番 | **AUTO** subject twice in this paper | Both are app-registered share services with 「ポート」 and a return step: 4番「ポートの二次元コードを読み取って傘を借りられます…どの駅のポートへでも返却できます」; 問題2-5番「返却しようとした**ポート**が満車で」. 「ポート」 is decisive in the 問題2 item. | Re-author one of the two. |
| C7 | 問題3-5番 ↔ 問題14 flyer; 問題1-5番 ↔ 問題10 | **AUTO** cross-surface repeat | 問題14 = 「さくらコイン」: buy at 地元商店街 → get points via 専用スマートフォンアプリ. 問題3-5番 = 「加盟店舗で買い物…スタンプ…抽選」 in a 商店街. Step 5 forbids the 問題14 flyer sharing a decisive detail with a listening item. Also 設備点検 twice: 読解 問題10「設備点検および蔵書点検のため…全館休館」 ↔ 聴解 問題1-5番「エレベーターおよび駐車場の**設備点検**」. | Move one of each pair off the shared subject. |
| C8 | 問題5-2番 / closing | **AUTO** item unanswerable in real time | `聴解スクリプト.txt` has **no blank line before line 278**, so 「これで、聴解試験を終わります。」 sits **inside** the 2番 block. `pause_after()` fires on the block's first line, so 質問2 is followed by `GAP_BETWEEN_LINES` = **1.3 s**, then the exam-end announcement, then the 10 s `ANSWER_PAUSE`. 質問2 has effectively no answer time. Official (`imported-n2-2025-07`) keeps the closing as its own 1-line block. | Insert a blank line before the closing; rebuild the MP3. |
| C9 | 問題3-5番 | **AUTO** broken Japanese (agent/benefactive error) | 「加盟店舗で買い物をしたお客様に**スタンプを押していただき**、一定数が集まったら…」 — 「お客様に…押していただく」 makes the *customer* the stamper. In a stamp rally the shop stamps the customer's card. | 「加盟店舗で買い物をしたお客様のカードにスタンプを押していただき」 (agent = 加盟店舗) or 「…お客様にスタンプをお渡しし」. |
| C10 | 問題4-5番 | **AUTO** keigo error in the stimulus + off-register key | Stimulus: 「木村さん、いつも細やかな**お心遣いをいただき**、本当に**気が利きます**ね。」 — the speaker humbles himself (いただき) and then evaluates the addressee with 気が利く, an appraisal made downward. Key: 「いえいえ、**滅相もありません**」 — the idiomatic denial of praise is 「とんでもございません」; 滅相もない denies an outrageous imputation, and 「滅相も**あり**ません」 is the non-standard form of 滅相もない／ございません. It is also above the N2 band (step 2.5). | Rewrite the stimulus as a downward compliment (「木村さんはいつも細やかで、本当に気が利きますね。」) and key 「いえいえ、とんでもございません。」 The spec item is `気が利く`, which the stimulus already carries. |
| C11 | 問題4-1番 | **AUTO** second defensible answer | Stimulus 「このプロジェクト、君が中心になって進めて**くれないか**。」 Key 1 「はい、喜んで引き受けさせていただきます」; option 3 「恐れ入りますが、お断りいたします」 is a well-formed, register-appropriate business refusal. Nothing in the stimulus forces acceptance, so both are valid replies to a request. | Break option 3's form, not its stance — e.g. 「はい、お断りいたします」 or 「恐れ入りますが、お断りになります」 (respectful form on one's own act). |
| C12 | 問題5-1番 | MAJ wrong item type for 統合理解 | 7-line block, one voice, answer stated verbatim: 「中でも情報処理研究室は…迷っている人にはまず見学を**おすすめします**」. Official 問題5-1番 (`imported-n2-2025-07`) is an **18-line, 3-speaker** deliberation whose key (会場を変更する) is never stated. It also duplicates 2番's frame (a male official enumerates four numbered options, then one is picked). | Re-author as a 3-speaker discussion where the decision is inferred from the last turns; keep 統合理解's requirement to combine information. |
| C13 | 問題5-2番 | MAJ solvable without integrating | The script labels the choices 「**1番**のアパート」…「**4番**のアパート」 in the same order as the printed options, and both keys' option numbers equal the spoken ordinals (質問1→4, 質問2→2). Number-matching solves both without processing either student's conditions. Official names its four options (夕日通り／西が丘／さくら公園／東山). | Give the four apartments names (or shuffle the printed order against the spoken order). |
| C14 | 問題5-2番 | MAJ casting — one voice, two people | Narration 「係の**男の人**と留学生2人」; labels used are `男` (MALE +0%), `学生` (MALE +6%), `女` (FEMALE +4%). The two men are the same voice 6% apart in a 3-party item, and 質問2 asks specifically about 「男の留学生」. Additional instance of the class `make check` already WARNs on for 問題2-1番 (教授/学生). | Recast the 係 as `係員` (FEMALE) or `男2` (MALE −8%). |
| C15 | 問題3 全items + 問題5-1番 | MIN script format | 28 of 64 spoken choice lines end without 「。」 (`1、靴のデザインのトレンド`). `choukai-script-writing` mandates `1、…。`; `imported-n2-2025-07` has **0** such lines (`1、新しい洗剤の特徴。`). Affects edge-tts final prosody and choice-gap timing. | Add 「。」 to every 問題3/問題5-1番 choice line; rebuild the MP3. |
| C16 | 問題1-1番 | MIN Latin in a spoken script | 「公式**Web**サイト」「**Web**サイトからだと」 ×4 spoken, plus printed option 4 「Webサイトから再配達を申請する」. `Web` and `N` are the only Latin in the file; edge-tts pronunciation of bare Latin is unpredictable, and the official scripts contain none. | Use 「ホームページ」 in both the script and the printed option. |
| C17 | 問題5 header block | MIN block convention | Block 40 is 3 lines: `問題5。` + instruction + the 1番 lead-in. `choukai-script-writing` requires the 1番 lead-in to be **its own block** between the instruction and `1番。`; merging it drops one 3 s `PAUSE_AFTER_INSTRUCTION` beat. (The 問題1–4 header+instruction merge is **not** a defect — `imported-n2-2025-07` does the same.) | Split the lead-in into its own block. |
| C18 | 聴解 provenance | MIN/MAJ off-spec scenarios | vs `logs/ledger.json` test 4 (seed 20260805): **not drawn** — 問題1-4番 傘シェアリング, 問題2-2番 昇降式デスク, 問題2-5番 自転車シェアリング, 問題3-4番 路上喫煙禁止区域; 問題2-3番 drifted 「ラジオ:睡眠の話」→熱中症. **Drawn but unused** — 会社:会議の準備／不動産屋:部屋探し／ラジオ:睡眠の話／引っ越し業者との調整／地域の防災訓練のスケジュール／人事部からの健康診断のお知らせ／テレビ:専門家の解説. 4 of 18 scored items are off-list. | Re-author the four items onto unused drawn scenarios (which also resolves C4/C5/C6), or record the substitution in the ledger. |
| C19 | all 聴解 解説 | MIN mandated format ignored | `choukai-script-writing` mandates one line per wrong option in the shape ``1 ✗「script line」→ 別の人に割り当て``. **No** 解説 cell uses it. 問題3 1番/3番/5番 carry **zero** quotes and no distractor treatment at all (e.g. 1番: 「初級クラスの受講生に合わせた教材選定のポイントと…について解説している。」). | Rewrite the 30 解説 cells in the mandated shape. |
| C20 | various | MIN Japanese/naturalness | 問題1-1番 「担当が別の配達中の場合」 (→「担当の者が別の配達に出ている場合」); the same clause 「画面上で空き状況を確認しながら…ご指定いただけます」 repeated in two consecutive 担当者 turns; 問題1-4番 set at 「駅」 then 「**地下鉄**のどの駅のポートへでも」; 問題1-5番 「行**な**います」 (official uses 行います); 問題2-2番 「座る時間も**混ぜ**ないと」 (→取らないと／挟まないと); 問題2-6番 「希望日の**3日前ではなく**、1週間前までに」 — a contrast with something nobody proposed and no option states; 問題2-4番 bus route named 「山の手線」, colliding with JR 山手線; 問題2-3番 「搬送されるケース」 without 救急/熱中症で; 問題5-2番 「**閑静**な住宅街にあり…非常に**静か**な環境」. | Line edits as noted. |
| C21 | 問題2-3番/4番, 問題3-4番 | MIN casting/label | 3番 and 4番 are adjacent monologues both labelled `アナウンサー` (FEMALE +4%) — two different "people", one voice, back to back; 4番's narration says 「案内**アナウンス**」 while the label is `アナウンサー` (`アナウンス` exists in `SPEAKER_MAP`). 問題3-4番's narration says 「市の**職員**」 but the closing question says 「**男の人**は」 (label `男`, to avoid the FEMALE-mapped `職員`). | Use `アナウンス` for 問題2-4番; make 問題3-4番's narration 「市の男の職員が」. |
| C22 | 問題1-2番 opts 3/4 | MIN weak grounding | Options 「出張先のホテルを**変更**する」/「上司に日程変更の**許可**をもらう」 — the script raises 連絡 only: 「上司の部長と、宿泊先のホテルには私から**連絡**しておきましょうか」. The topics are reassigned; the actions in the options are never spoken. | Reword to 「上司と宿泊先のホテルに連絡する」 so the reassignment is exact. |

### Answer-position note (not a finding — unverifiable, see §6)
Across the 19 four-option 聴解 items the keys fall 1×7 / 2×5 / 3×3 / 4×4 — a visible skew toward 1 that cannot be checked against `answer_positions` because the on-disk spec is test 3's.

---

## 3. Root-cause table (step 6.5)

Grouped by shared cause. "on disk" = how many of tests 1/2/3/4 show the class (checked by reading their sources, not from memory).

| Findings | Root cause | On disk | Owning file | Concrete proposed edit |
|---|---|---|---|---|
| C1, C2 | `GATE-BLIND` (rule exists, is specific, and is unenforced for 例 items) | 4/4 (skill names test 1 問題2-1番, test 2 ×5, test 3 ~14, test 4 問題2 例) | `tools/check_consistency.py` (+ `choukai-script-writing` "keyed option must be quotable") | The existing 解説-quote check is per-**key**; extend it to the **例**: for 問題1/2 例 blocks, require each printed 例 option to share ≥1 content bigram with the 例 dialogue, and FAIL (not WARN) when an option's every content word is absent from the block. The 例 is the one item `make check` currently never inspects for grounding, and it is the first thing the examinee hears. |
| C3 | `GATE-WRONG` (a check exists and mis-measures) | 3/4 (t1, t2 問題1 例 vs official; t4 問題4 例 stimulus) | `tools/check_consistency.py` | `no 例。block is byte-identical to another test's` compares whole **blocks** and exact **bytes**. It missed t4 because (a) only the stimulus line was copied, options rewritten, and (b) `？` vs `?`. Change to: NFKC-normalise, then compare the 例's **first line** (and each dialogue line) across all tests **including `imported-*`**; flag any line ≥10 JP chars appearing in two papers. Then re-verify every test that passed on the old check. |
| C4, C5, C6, C7 | `RULE-UNENFORCEABLE` + `GATE-BLIND` — "One topic, one surface" is prose the author verifies *after* writing, and nothing measures it | 4/4 (t4 had 部屋探し in 問題1-4番 and 問題5-3番 before; the repair introduced a new pair) | `jlpt-test-generation` §"One topic, one surface" + `tools/check_consistency.py` | (1) Authoring-time construction rule: `merge_seeds.py` must emit **one scenario per 聴解 slot** (21 slots) and the author may use only the scenario in the slot — no free choice. (2) Gate: build a keyword set per 聴解 item (narration nouns) and per 読解 passage, and FAIL when any two surfaces in one paper, or any surface and the **previous test's** same-numbered surface, share ≥2 content nouns. The three t3↔t4 collisions (自転車シェアリング, 使い捨て傘, 熱中症/夜間エアコン) are all detectable this way. |
| C8, C17 | `GATE-BLIND` (block-shape rules that `validate_script()` half-enforces) | C8: 1/4 (t4 only — t1/t2/t3 and official keep the closing separate); C17: needs per-test check | `tools/check_consistency.py` + `choukai-mp3-generation/scripts/make_choukai_mp3.py` `validate_script()` | Add two structural assertions to `validate_script()`, next to the existing 質問1/質問2 check: (a) `CLOSING` must be the **entire** last block — fail if `これで、聴解試験を終わります。` appears in a block that also matches `ITEM_RE`; (b) the 問題5 1番 lead-in must be its own block — fail if 「問題用紙に何も印刷されていません。まず話を聞いて」 shares a block with 「問題5では、」. Both are string-decidable and both silently corrupt pacing. |
| C9, C10, C20 | `RULE-UNENFORCEABLE` — "Every sentence is Japanese / read it aloud" is a review-time judgment with no construction procedure | 4/4 (skill records six broken sentences in t4's 読解 half alone) | `question-authoring` + `choukai-script-writing` | Cannot be mechanised; keep as human judgment but make it a **construction** step, not a review step: `choukai-script-writing` should require the author to state, per dialogue, the **agent of every benefactive** (〜ていただく/〜てもらう/〜てあげる) and the **rank direction** of every 敬語 turn before the block is considered done. C9 and C10 are both agent/direction errors that a written agent-list would have caught at authoring time. |
| C11 | `RULE-MISSING` — no skill says a 即時応答 distractor may not be a pragmatically valid alternative stance | 2/4 (t2 keyed a 社長 speaking humble keigo downward; t4 C11) | `question-authoring` 即時応答 section (+ `choukai-script-writing`) | Add: "A 問題4 distractor must be wrong in **form** — tense, keigo direction, self/other reference, or a literal reading of the idiom — never merely a different but well-formed stance. A polite refusal, a polite acceptance, and a polite deferral are all valid replies to a request; if two options differ only in stance, the item has two answers." |
| C12, C13 | `RULE-MISSING` — no skill states what makes 問題5 統合理解 *integrated* | needs a t1/t2/t3 sweep; t4 fails both items | `jlpt-exam-structure` 問題5 row + `choukai-script-writing` | Add to `jlpt-exam-structure` §問題5: "1番 is a **≥3-speaker deliberation of ≥12 turns** whose key is *never stated* — it is inferred from the last agreement (official July 2025 1番 = 18 lines, 3 speakers, key 会場を変更する). A monologue that names its own answer is 問題2/3 material, not 問題5. 2番's four candidates are given **names**, not ordinals, and the printed option order must not mirror the spoken order — otherwise the item is solvable by number-matching." |
| C14, C21 | `GATE-WRONG` — the one-voice check WARNs and only covers **two-party** items | 4/4 (skill: t1 three pairs, t2 one, t3 three gender contradictions, t4 教授/学生) | `tools/check_consistency.py` + `choukai-mp3-generation` §Casting | The check pairs exactly two labels per block, so t4's 3-party 問題5-2番 (`男`+`学生`+`女`) is invisible. Change to: for every item block, group **all** labels by resolved (voice, rate) and warn on any group of ≥2 whose rates differ by <10%; **promote to FAIL** when the item's questions distinguish the speakers (「男の学生は」/「女の学生は」/「男の留学生は」), because the examinee then cannot tell them apart. |
| C15, C16 | `GATE-BLIND` — the ASCII-punctuation check exists; the sibling rules do not | C15: t4 (28 lines) vs official 0; C16: t4 only | `tools/check_consistency.py` | Beside the existing ASCII `,`/`.` rejection add: (a) every `^[1-4]、` line must end in `。`/`?`/`？`; (b) no Latin `[A-Za-z]{2,}` in a spoken line except the leading `N2聴解`. Both are one-line regex checks on a file the gate already parses. |
| C18 | `GATE-BLIND` — the target-item audit covers 問題1–8 + 即時応答 but **not** `listening_scenarios` | 2/4 (gate already catches t3's `quick_response` substitution; nothing checks scenarios in any test) | `tools/check_consistency.py` + `exam-qa-review` §6.1 | Extend the "問題1/2/4 test the items `test_spec.json` drew" check to `listening_scenarios`: every 聴解 item's narration must contain ≥1 content noun from its assigned drawn scenario, and every drawn scenario must be consumed. **Blocked prerequisite:** `logs/test_spec.json` currently holds **test 3's** spec, so no per-test spec history exists — add `logs/spec_<test_id>.json` (or a `test_id` key + archive) so a finished paper can still be audited against the spec it was authored from. |
| C19 | `RULE-IGNORED` — the format is specific, mandated, and was simply not used | 4/4 | none (process failure, AGENTS.md §0) | No skill change. Report as a process failure. Optional gate assist: WARN when a 聴解 解説 cell contains no `「…」` at all (問題3 1番/3番/5番 would fire). |
| — | `PIPELINE-GAP` — stale MP3 (already filed by `make check`) | 4/4 (all four tests record `script_sha: None`) | `jlpt-test-generation` workflow | Not re-filed. See the evidence note in §5. |

---

## 4. Coverage statement

### 4a. Steps run

| Step | Ran on | Result |
|---|---|---|
| Blind-solve | script + booklet options, keys hidden | 30/30 + 4 例 agree (§1) |
| 1. Key-by-key proof | all 30 items + 4 例 | every key restates a quoted script line (§4b); 理由 items 問題2-4番/6番 keyed to the **cause** |
| 2 / 2b. Distractor grounding | every wrong option in 問題1/2/3 (24 items × 3 = 72 options) | §4b table; 2 ungrounded (C1, C2), 2 weak (C22) |
| 3. 聴解 structure | 問題→type map, 例 mechanics, printed-vs-spoken, block shape, instruction sync | C8, C12, C13, C15, C17 |
| Narration ↔ SPEAKER_MAP | all 21 blocks | C14, C21; no gender contradiction found |
| Booklet ↔ script sync | 問題1/2 printed options, 問題5-2番 printed options, 5 instruction lines | clean (see 4c) |
| Read aloud | every line of the script | C9, C10, C20 |
| Verbatim-copy | vs `imported-n2-2025-07`, `tests/1|2|3`, both directions | C3 (§4d) |
| 5. Topic table | this paper + t2 + t3 + the 読解 half | C4, C5, C6, C7 (§4e) |
| 6. Spec/provenance | `logs/ledger.json` test 4 entry (spec on disk is t3's) | C18 (§4f) |
| Artifact staleness | mtimes + `script_sha` + git | §5 |

### 4b. Grounding table — every 問題1/2/3 distractor (key marked ✅)

**問題1 例** (key 2): 1 「参加者の人数も確認しておきますね」→「人数は僕がまとめておくから」= reassigned ✓ | ✅2 「君は店の予約をお願いできるかな」「すぐ電話します」 | 3 「駅前の居酒屋にしようと思ってるんですけど」= venue effectively chosen ✓(weak) | 4 **NOT IN SCRIPT** ✗ **C2**
**問題1-1番** (key 4): 1 「窓口へお越しいただく方法もございますが…あまりおすすめできません」✓ | 2 「自動音声でのお申し込みも承っておりますが…細かい時間帯の指定が難しく」✓ | 3 「配達員へ直接ご連絡いただいても…対応いたしかねます」✓ | ✅4 「専用フォームから伝票番号を入力してご申請ください」
**問題1-2番** (key 1): ✅1 「何よりも先に訪問先の担当者様に連絡を入れて」 | 2 「指定席を予約していた列車が運休…次の列車に乗るしかない」✓(superseded) | 3 「宿泊先のホテルには私から連絡しておきましょうか」△ topic reassigned, **変更** never said — C22 | 4 「上司の部長と…私から連絡しておきましょうか」△ **許可** never said — C22
**問題1-3番** (key 1): ✅1 「さっそくスマホでそのアプリを入れてみるよ」 | 2 「タクシー会社の電話がかなり混み合っていて、なかなかつながらない」✓ | 3 「大通りでもタクシーを拾うのは難しいわよ」✓ | 4 「駅の乗り場まで歩くか、配車アプリを使ってみたら？」✓(not chosen)
**問題1-4番** (key 2): 1 「現金の支払いは窓口では受け付けておりません」✓ | ✅2 「まずはスマホのアプリで無料の会員登録を」「今ここで登録します」 | 3 「返却ボックスの場所は、登録のあとにアプリで確認すればいいですか」✓(ordering) | 4 「使い捨て傘は買いたくないので」✓
**問題1-5番** (key 3): 1 「点検終了後に管理会社が回収いたしますので、皆様が剥がす必要はございません」✓ | 2 「当日ご自宅にいらっしゃる必要はございません」✓ | ✅3 「事前に管理事務所へご連絡の上、一時的な車移動の手続きを」 | 4 「点検の時間は何時ごろになりますか」→ already answered in-dialogue ✓
**問題2 例** (key 4): 1 「デザインも気に入ったんだけど」✓(not the reason) | 2 **NOT IN SCRIPT** ✗ **C1** | 3 「値段は少し高かったんだけど」✓ | ✅4 「使いやすそうだったから思い切って決めたよ」
**問題2-1番** (key 1): ✅1 「引用している文献の表記方法が、指定のルールに従っていません」 | 2 「指定された文字数も満たしています」✓ | 3 「締め切り時間にきちんと間に合っています」✓ | 4 「グラフやデータの使い方も適切です」✓
**問題2-2番** (key 2): 1 「購入費用は総務が予算内でうまく調整…困るようなことは特になかった」✓ | ✅2 「慣れるまではずっと立って作業していると足や腰に疲労がたまる」 | 3 「通路の広さは前と変わらないよ」✓ | 4 「配線工事は特に必要なかったんだ」✓
**問題2-3番** (key 3): 1 「タイマーで途中で切るのではなく」✓ | 2 「扇風機を併用して」✓(denies だけ) | ✅3 「設定温度を高めにして朝までつけっぱなしにしておくことが推奨されます」 | 4 「冷たい水を一気にたくさん飲むと…原因になる」✓
**問題2-4番** (key 1 = the CAUSE): ✅1 「運転手不足が深刻化しており、現在の運行便数を維持することが困難」 | 2 「道路工事に伴う迂回…はございません」✓ | 3 「新しい駅へのルートの追加はございません」✓ | 4 「増便をお望みの声も多く…当面は難しい」✓ — the measure (夜間の便数削減) is **not** keyed. Earlier defect fixed.
**問題2-5番** (key 4): 1 「借りたポートと違う場所にも返せるから便利」✓ | 2 「会員登録もアプリで簡単だったよ」✓ | 3 「駅のすぐそばにポートがある」✓ | ✅4 「返却先が満車なのが一番困るよ」
**問題2-6番** (key 2): 1 「代わりに出られる人もこちらで探せる」✓ | ✅2 「期限を過ぎた申し出は認められない決まりでね」 | 3 「その日に休みを希望している人も他にいない」✓ | 4 「伝え方は口頭でかまわないんだ」✓ — no second true statement remains. Earlier defect fixed.
**問題3 例** (key 2): 1 「デザインや色も大切ですが」✓ | ✅2 「自分の足の形に合った靴を選ぶことが健康への第一歩」 | 3 歩き方 not said △ | 4 お手入れ not said △
**問題3-1番** (key 1): ✅1 「教材選びの際は、ぜひイラストや図表のわかりやすさに着目して」 | 2 「文法解説の詳しさだけで選んでしまいがち」✓ | 3 「イラストや写真が豊富に使われているテキスト」✓ | 4 「受講生」✓ / 採点 not said △
**問題3-2番** (key 3): 1 「会場」✓ / 交通手段 not said △ | 2 「出展社」✓ / 新製品 not said △ | ✅3 「名札を係の者にお見せください。お名前とご連絡先が出展社に送られ」 | 4 飲食店 **not said** △
**問題3-3番** (key 1): ✅1 「その数値データをグラフにして、冒頭で強調した方が」 | 2 「デザインについてのスライドは完成しました」✓ | 3 「競合他社の製品との差別化ポイント」✓ / 価格調査 not said △ | 4 「新製品発表会」✓ / 会場手配 not said △
**問題3-4番** (key 2): 1 「指定された喫煙所」✓ / 増設工事 not said △ | ✅2 「駅周辺の路上喫煙禁止区域における注意点をご説明します」 | 3 「電子たばこも同様に禁止の対象」✓ | 4 「罰則は現時点では科しておりません」✓
**問題3-5番** (key 4): 1 「地域の特産品が当たる抽選」✓ | 2 「若い世代やファミリー層を呼び込む」✓ | 3 「加盟店舗」✓ / 営業時間 not said △ | ✅4 「スタンプラリー企画を提案したい…ご協力いただける加盟店を募集」

△ = topic-level 概要理解 distractor whose head noun is in the script but whose modifier is not. Not filed individually: measured on `imported-n2-2025-07`, official 問題3 distractors behave the same way (「固い汚れの落とし方。」「家具を長く使う方法。」), so a strict reading of the grounding rule would fail the official paper — a check that fails the reference bar is a wrong check. Filed instead as a note that the rule's 問題3 clause needs the same softening the token-overlap WARN already has.

### 4c. Booklet ↔ script sync
- 5 instruction lines: `聴解.md` and `聴解スクリプト.txt` are **character-identical**, and all five also match `jlpt-exam-structure` §"問題N instruction lines" verbatim (including 問題2's 「問題用紙を見てください」 and 問題5's 「問題用紙にメモを」, the two places the skill records other tests drifting). The 問題5 1番/2番 booklet lead-ins match the canonical text.
- Spoken-choice accounting: 64 `^[1-4]、` lines = 問題3 (6×4) + 問題4 (12×3) + 問題5-1番 (4). **No choice line appears in any 問題1/2 or 問題5-2番 block** — the printed/spoken split is correct.
- 問題5-2番's four printed options correspond 1-to-1, in order, to the four apartments described (閑静／大学徒歩5分・5万円／築浅セキュリティ／駅・商店街) — see C13 for why that ordering is itself the problem.
- Marksheet 例 pre-marks (2/4/2/1) equal the announced numbers (2/4/2/1).
- Item counts: 問題1 例+5, 問題2 例+6, 問題3 例+5, 問題4 例+11, 問題5 2 blocks/3 answers = **30 answers** ✓. 43 blocks total (within the 43–46 range on disk).

### 4d. Verbatim-copy check (both directions)
| vs | shared non-instruction lines | shared blocks >60 chars | verdict |
|---|---|---|---|
| tests/1 | 3 | 3 | all canonical announcer/question lines (「女の人は何について話していますか。」, 例 confirmations) |
| tests/2 | 4 | 3 | same |
| tests/3 | 1 | 8 | same + shared 問題4/問題5 header blocks |
| imported-n2-2025-07 | 1 | 2 | 例 confirmations only at block level — **but** the 問題4 例 **stimulus line** is a copy (C3), invisible to a block-level comparison |
No dialogue turn, monologue, or option is shared with any other paper. Test 4's 問題1 例 (忘年会) is original — the 学校で先生が学生に copy is tests 1 and 2, not this one.

### 4e. Topic table (聴解 items + the collisions that matter)
| Slot | test 4 | test 3 | test 2 | collision |
|---|---|---|---|---|
| 問1 例 | 忘年会の店予約 | 出張の準備 | 学校の宿題 (copied from official) | — |
| 問1-1 | 郵便局:再配達 | 家庭:熱中症対策 | 美術館 | — |
| 問1-2 | 出張の遅延連絡 | 学習塾 | 薬局 | — |
| 問1-3 | タクシー配車アプリ | スーパー:食品ロス | ボランティア事務所 | **C5** (with 問1-4) |
| 問1-4 | 駅:傘シェアリング | 銀行窓口 | 会社 | **C4** (t3 問1-5 使い捨て傘), **C5**, **C6** |
| 問1-5 | マンション設備点検 | 市役所:使い捨て傘削減 | 会社 | **C7** (読解 問題10 設備点検) |
| 問2 例 | バッグ選び | パーティ欠席 | 体に力が入らない | — |
| 問2-1 | 大学:レポート指導 | 職場:腰痛予防 | 睡眠の質 | 大学/教授 also 問5-1 |
| 問2-2 | 昇降式デスク | ラジオ:自転車シェアリング | 防災訓練 | — |
| 問2-3 | ラジオ:夜間エアコン/熱中症 | コンサート入場 | 社内食堂 | **C4** (t3 問1-1 熱中症・寝るとき) |
| 問2-4 | バス:ダイヤ変更 | 大学就職課 | イベント役割 | — |
| 問2-5 | 自転車シェアリング | テレビ:天気予報 | マンション騒音 | **C4** (t3 問2-2), **C6** |
| 問2-6 | バイト:シフト変更 | アパート電気工事 | ラジオ:アップサイクル | — |
| 問3-1..5 | 日本語教材／見本市名札／プレゼン資料／路上喫煙／商店街スタンプラリー | 開発部／ラジオ専門家／保険窓口／ニュース／講演会医師 | テレビ／メンバー／物流／窓口／講師 | **C7** (スタンプラリー ↔ 問題14 さくらコイン商店街); 二次元コード also in 問1-4 |
| 問5-1 | 大学:研究室配属 | 観光案内所 | 会社 | 大学/教授 twice |
| 問5-2 | 留学生センター:アパート | (2番) | (2番) | 大学 three times |
Also cross-cutting: **スマホアプリでの登録・決済** is decisive or near-decisive in 問1-3, 問1-4, 問2-5 **and** 問題14 — four surfaces, one motif.

### 4f. Spec / provenance
- `logs/test_spec.json` on disk describes **test 3** (its `<!-- seed -->` and content do not match test 4's `seed: 20260805`). Per the task instruction the audit used `logs/ledger.json`, which **does** carry a `test 4` entry (seed 20260805, harvest `harvest_20260805`, generated 2026-08-04 14:55) **and** a separate `test 4-removed` entry (seed 20260803, `legacy0803sh`) — the removed first attempt. The `4-removed` entry is stale history and is what `make check` flags for over-recorded draw counts, alongside `test 4` itself.
- **問題4 即時応答 target items: 11 of 11 scored items match the ledger draw.** 1番/2番/4番/6番/7番/11番 are character-identical; 3番 (存じております), 5番 (気が利く), 8番 (板につく), 10番 (願ってもない) realise their idiom items correctly; 9番 drifted 「新しいシステム、慣れるまで…」→「新しい**社内**システム、慣れるまで…」 (same item, trivial). The 12th recorded item 「皆さんのおかげで無事に終えることができました。」 is **unused** — but `make check` independently reports the ledger over-records `quick_response` (12 recorded, `DRAW` says 11), so this is a ledger accounting bug, **not** an authoring substitution. Verdict: **target-item audit PASSES.**
- `listening_scenarios`: 4 scored items off-list, 7 drawn scenarios unused → **C18**.
- **Answer-position compliance: SKIPPED** (see §6).

---

## 5. `make check` output — every line, with resolution

`make check` **FAILS** (exit 1): 43 problems, 15 warnings. Test 4's rows:

| Line | Half | Resolution |
|---|---|---|
| `4: 問題5 2番 lead-in is booklet-only` | 聴解 | Pre-filed. Confirmed present (script line 270) and shared with tests 1/2/3 — the 2番 lead-in is the only 2番 line common to all four papers, which is the systemic signature the skill describes. Not re-filed. |
| `4: 聴解.mp3 … script_sha bb73a9c3cfa4 … records None` | 聴解 | Pre-filed. **Additional evidence:** `sha1(聴解スクリプト.txt)[:12]` = `bb73a9c3cfa4`; `聴解_チャプター.json` records `null`. mtimes: script/md 2026-08-06 09:56, mp3/chapters 2026-08-05 **17:07**. Commit `4df5631` (08-05 **19:00**) rewrote all five 問題 instructions in the script *after* the MP3 was built, so the shipped audio still says 「最もよいものを一つ**選びなさい**」 in all five sections, 「質問と**選択肢**を」 in 問題3, the old 問題4 instruction missing 「まず…それから」, and 問題5 missing 「**問題用紙に**メモを」. The examinee **hears** text that contradicts every instruction printed in the booklet. Not re-filed, but this is the concrete impact. |
| `4: 聴解 two-party items … 1番。大学で教授 ['教授','学生']` (WARN) | 聴解 | Pre-filed. Confirmed: both MALE, 12% apart. **C14 is an additional instance the check cannot see** (3-party 問題5-2番). |
| `4: built HTML records its source sha: 5 stamp(s) missing` (WARN) | both | Real. Independently verified that `聴解.html`'s body **does** match the current `聴解.md` line for line (0 divergent lines after stripping `<rt>`), so the HTML is stale in *stamp* only, not content — but the stamp is what makes that checkable, and without it the mtime skew (HTML 08-05 19:00 vs md 08-06 09:56) is undecidable without this manual diff. Fix: `make booklet 4 && make sheet 4`. |
| `4: （注N） markers…`, `読解 length floors`, `（中略）`, `問題11 retrieval stem`, `問題11 opinion question`, `読解 key length 66`, `問題14 解説 quotes`, `問題9 解説 tags`, `読解 gloss count 5` | 読解 | Out of scope for this review (聴解 half only). All nine remain open and independently fail test 4. |
| `ledger draw counts … test 4/word_formation 5 vs 3, quick_response 12 vs 11, listening_scenarios 20 vs 21, reading_topics 11 vs 12` | inputs | Real; explains the unused 12th 即時応答 item (§4f). |
| `logs/seeds.json … reused 1 URL` | inputs | Real, affects the shared harvest. Out of scope. |

WARNs I judged **false positives**: none in the 聴解 half. The 7 unmatched 解説 quotes flagged by my own quote scan are false positives of *my* matcher (ellipsis elision + dictionary glosses), verified half-by-half — the gate's own quote check does not report them for test 4.

---

## 6. Verdict on each earlier-review claim

| Claim | Verdict | Evidence |
|---|---|---|
| 問題1↔問題2 question types swapped | **FIXED** | The 夜間エアコン monologue now sits in 問題2 with 「どのように説明していますか」; all five 問題1 items ask 「このあとまず何をしますか」/「点検当日までに何をしなければなりませんか」 (the latter is an attested official 課題理解 shape — cf. the official 例 「学生は今日、家で何をしなければなりませんか」). Type map clean. |
| 問題1 例 printed options for a different question, announcer declared one correct | **FIXED** | Options 1–4 all answer 「このあとまず何をしますか」; announced 2番 = 「店に電話して予約する」, supported by 「君は店の予約をお願いできるかな」「すぐ電話します」. (Option 4 is separately ungrounded — **C2**, a different defect.) |
| Key naming 点検作業員 where the script says 管理事務所 | **FIXED** | 問題1-5番 key is now 「管理事務所に車の移動を申し出る」, matching 「事前に管理事務所へご連絡の上」. |
| Five 解説 quotes the audio never speaks | **FIXED** | 74 quotes checked; all 7 non-literal matches resolve to ellipsis elisions or dictionary glosses (§1). |
| 問題2-4番 keyed the measure instead of the cause | **FIXED** | Key 1 = 「運転手が不足し、今の便数を維持できないため」 = 「運転手不足が深刻化しており、現在の運行便数を維持することが困難」. The measure (夜間の便数削減) is now in the 解説 as the *result*. |
| 問題1 1番 and 問題2 1番 each carrying one fabricated option | **FIXED** for both scored items | 問題1-1番: all three distractors are raised and denied. 問題2-1番: option 4 (グラフのタイトル) is grounded by 「グラフやデータの使い方も適切です」. **BUT the class survives in the 例 items** — 問題2 例 option 2 (**C1**) and 問題1 例 option 4 (**C2**), which no gate inspects. |
| 問題1-4番 and 問題5-3番 both apartment-hunting | **FIXED, but the repair created a new pair** | 問題1-4番 is now 傘シェアリング; 問題5 has only 1番/2番 (2番 = apartments). The repair moved the item onto an off-spec scenario that now duplicates 問題1-3番 (**C5**) and 問題2-5番 (**C6**), and collides with test 3 (**C4**). |

---

## 7. Skips (explicit)

1. **Answer-position compliance (step 6.2) — SKIPPED.** `logs/test_spec.json` on disk is test 3's; `logs/ledger.json`'s test 4 entry records drawn *items* but no `answer_positions`. There is no artefact on disk recording the positions test 4 was authored against. Reported instead: the observed distribution (1×7 / 2×5 / 3×3 / 4×4 over the 19 four-option items) and the pipeline gap (§3, C18 row).
2. **Web-blend / harvest-URL verification (step 6.3–6.5) — SKIPPED.** Same cause: the spec is test 3's, so no `origin`/URL provenance exists for test 4's 聴解 scenarios. `make check` separately reports one duplicated seed URL in `logs/seeds.json`; no URL was fetched (no network use attempted).
3. **Audio verification — NOT PERFORMED.** `聴解.mp3` was not decoded or listened to. Staleness is established from `script_sha`, mtimes, and the commit diff (§5), which is conclusive for the instruction text; per-item timing claims in C8/C15/C17 are derived from `gap_before_line()`/`pause_after()` semantics read from the source, not measured on the audio.
4. **読解 half — OUT OF SCOPE** by assignment. Its nine open `make check` failures are listed in §5 but not reviewed; note that C7 required reading 問題10 and 問題14, and both cross-surface collisions were found there.
5. **`refs/` PDFs not opened.** Official calibration was taken from `tests/imported-n2-2025-07/聴解スクリプト.txt`, which is the transcription of `refs/JLPT/16. N2 07-2025 (script).pdf` and is the bar the gate itself measures against. Its 問題5-2番 block ends at the dialogue (質問1/質問2 absent from the transcription), so it was not used as the model for that one shape.
6. **No file was edited**, including `exam-qa-review/SKILL.md`. The skill permits the reviewer to add newly-found defect classes to it directly; the classes behind C11, C12/C13, C15/C16 and the 問題3-distractor calibration note are new to that file, but this review is under a read-only instruction, so they are filed as proposed edits in §3 instead.
