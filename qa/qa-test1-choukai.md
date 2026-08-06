# TEST 1 CHOUKAI: FAIL (13 findings, 4 automatic)

Scope: the 30 聴解 answers (問題1–問題5) of `tests/1` plus all four 例. Reviewer
authored nothing in this paper. Read in full before any other tool call:
`.agents/exam-qa-review/SKILL.md`, `.agents/choukai-script-writing/SKILL.md`,
`.agents/jlpt-exam-structure/SKILL.md`, plus `SPEAKER_MAP` in
`.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py`.

**Entry condition violated.** `python3 tools/check_consistency.py` currently
**FAILS** (43 problems, 15 warnings). Five failure rows name test 1, three of
them 聴解 (例 byte-identity, 問題5 2番 lead-in, `script_sha: None`). Per
`exam-qa-review` "do not start QA on a failing gate" this review should not have
begun; it was run anyway on explicit instruction, and the four already-filed
classes are excluded from the count above.

---

## 1. Blind-solve diff (30/30, no key read until after)

Answers derived from `聴解スクリプト.txt` + the printed options in `聴解.md`
(lines 1–163 only), before opening the key table at line 200.

| Item | Reviewer | Key | Match |
|---|---|---|---|
| 問1-1..5 | 2, 3, 2, 1, 4 | 2, 3, 2, 1, 4 | ✓✓✓✓✓ |
| 問2-1..6 | 3, 4, 2, 2, 4, 4 | 3, 4, 2, 2, 4, 4 | ✓✓✓✓✓✓ |
| 問3-1..5 | 2, 3, 3, 2, 2 | 2, 3, 3, 2, 2 | ✓✓✓✓✓ |
| 問4-1..11 | 1,2,3,1,1,1,2,1,2,1,2 | 1,2,3,1,1,1,2,1,2,1,2 | ✓ ×11 |
| 問5-1 / 2-質問1 / 2-質問2 | 2 / 1 / 4 | 2 / 1 / 4 | ✓✓✓ |

**Zero mismatches.** No mis-key, no second defensible answer found on any of the
30 items. The four 例 also blind-solved to the announced numbers (問題1→2,
問題2→2, 問題3→2, 問題4→1) and the マークシート pre-marks agree
(`1 **(2)** 3 4` / `1 **(2)** 3 4` / `1 **(2)** 3 4` / `**(1)** 2 3`).

The findings below are therefore all *construction* defects, not key defects —
which is exactly the shape `exam-qa-review` §2b warns about: items that solve
correctly but for the wrong reason.

---

## 2. Findings

Severity `AUTO` = automatic-fail class per `exam-qa-review` "Ground rules".

| # | Item | Class | Evidence | Proposed fix |
|---|---|---|---|---|
| **F1** | 問題2-1番, options 2 and 4 | **AUTO** — 聴解 distractor not grounded in anything said | Script 73–80 contains no 寝坊 and no 最寄り駅を間違え. The 解説 itself confesses: `「4の最寄り駅間違いは音声にない」` (`聴解.md:214`). Option 2「朝寝坊してしまったから」 is likewise absent. Only option 1 is denied (「電車、止まってたの?」「いや、電車は普通に動いてたんですけど」). | In the script, have 女 raise and the man kill both: e.g. 女「寝坊でもしたの?」男「いえ、家はいつも通りに出たんですけど」 and 男「駅に着いてから…気づいて」→ add 女「駅、間違えたのかと思った」男「駅は合ってたんです」. Then re-harvest the options out of the script and write the three grounding lines into the 解説 cell in the mandated shape `2 ✗「…」→ 明確に否定`. |
| **F2** | 問題1 例 + 問題2 例, **booklet side** (`聴解.md:17–20`, `58–62`) | **AUTO** — content copied verbatim from an `imported-*` paper | All 8 printed 例 option lines are byte-identical to `tests/imported-n2-2025-07/聴解.md`: ` 1. 作文を書く / 2. 教科書の問題をやる / 3. ノートを買う / 4. プリントを作る` and ` 1. 仕事が忙しかったから / 2. 夜遅くまで映画を見ていたから / 3. 朝早く起きたから / 4. なかなか眠れなかったから`. The gate's copy check only reads `聴解スクリプト.txt`, so the booklet half is unreported. (Recurrence: test 2's 問題1 例 options are identical too — 2 of 4 papers.) | The already-filed script-side fix (author fresh 例 dialogues) must regenerate the **printed option sets in `聴解.md`** in the same edit, or the copy survives the fix. |
| **F3** | `tests/1/聴解.html`, `tests/1/解答.html` | **AUTO** — artifact older than the source it is built from | mtimes: `聴解.md` = 2026-08-05 (epoch 1785977815) but `聴解.html` = 2026-08-04 (1785923766) and `解答.html` = 1785923767 — both ~15 h **older** than the Markdown they render. `grep -c src_sha` = **0** in both files, so nothing records what they were built from. (Distinct from the already-filed `script_sha: None` MP3 staleness, which covers only the audio.) | `make booklet 1 && make sheet 1` after the script/Markdown fixes, in the same pass as `make mp3 1`. |
| **F4** | 問題4-4番 | **AUTO** — off-level KEY (step 2.5, TOO_EASY side) | Stem 「田中さん、次の部署の会議、来週の金曜だっけ?」, key 「うん、そのはずだよ」. The whole discrimination is 「〜だっけ」(confirmation) + 「〜はず」 — both N3 inventory items. Every other 即時応答 in the paper tests an N2 idiom/keigo point (目を通す, に決まっている, のあまり, 〜がい, 席を外しております, 〜ようがない, 〜ばいいのに, 敬語の方向, お言葉に甘えて, てっきり). Of the 24 `quick_response` items in the ledger's `legacy` row, every one is an N2 idiom/keigo formula; this stem matches none of them. | Replace the item with an unused pool idiom (`大目に見る`, `差し支えなければ`, `めどが立つ`, `顔が広い`, `気が利く`, `口が堅い` are all unused in tests 1–4) and keep answer position 1. |
| F5 | 問題1-1番 opt 4; 問題1-4番 opt 3 | minor — weak grounding (noun-level only) | 「保証期間を調べる」: the script says only 「保証期間内でしたら交換できますが」 — the noun occurs, but no line proposes, reassigns or kills *checking* it. 「一週間後にまた来る」: 「まず一週間飲んでみてください」 supplies 一週間; a follow-up visit is never mentioned (the follow-up in the script is 大学病院の紹介). | Add a killing line each: 店員「保証期間はこちらで確認済みですので」; 医者「一週間後にまた来ていただかなくても、電話でご様子を伺います」 — or swap the options for candidates the dialogue already raises. |
| F6 | 問題5-1番 (`店員`+`妻`), 問題5-2番 (`教室の人`+`妻`) | minor — two labels, one voice | `SPEAKER_MAP`: 店員 = FEMALE +6%, 妻 = FEMALE +4% (2% apart); 教室の人 = FEMALE +0%, 妻 = FEMALE +4% (4% apart). Both are three-party items, so the gate's WARN (two-party only) never sees them — the already-filed WARN lists only 問題1-1番/1-3番/問題2-2番. | Recast: 問題5-1番's 店員 → a male-mapped label (e.g. `店長` MALE +0%) so 店員/夫/妻 are three distinct voices; 問題5-2番's `教室の人` → `講師`… (also FEMALE) is no help — give it a MALE mapping or use `係員`/rename. Narration states no gender for either label, so recasting is free. |
| F7 | 問題3-5番 (stem), 問題3-2番, 問題3-4番 (stems) | minor — 問題→question-type mapping | 問題3 is 概要理解 and the on-disk official reference uses one stem shape, 6/6: 「〜は何について話していますか」 (`imported-n2-2025-07`, 例+1–5番). Test 1 deviates on three of six: 5番 「女の人は何のために電話しましたか」 (a purpose-retrieval question, the ポイント理解 shape), 2番/4番 「…が一番言いたいことは何ですか」. Tests 2, 3 and 4 use 何について exclusively, so this is test 1 alone. | Rewrite 5番's question as 「女の人は何について話していますか」 with the options re-anchored on gist (the current option set already works as a gist set); 2番/4番 may keep 一番言いたいこと only if the fixing pass can cite an official paper using it — otherwise normalise. |
| F8 | 問題1-3番, 問題1-4番 (stems) | minor — 課題理解 stem shape | Both ask 「〜はこのあとどうしますか」. Official 問題1 is 5/5 「この後(まず)何をしますか」; `choukai-script-writing` §"The 問題 decides the QUESTION TYPE" gives 「〜は、このあとまず何をしますか」 as the shape. The items themselves are genuine 課題理解 (an action is chosen), so this is fidelity, not solvability. (Recurrence: test 3's 問題1-1番 「今夜寝る時にどうすることにしましたか」 — 2 of 4 papers.) | Reword to 「女の人はこのあとまず何をしますか」/「男の人はこのあとまず何をしますか」. Booklet has no stem text for 問題1, so the edit is script-only + MP3 rebuild. |
| F9 | 問題3-5番 (script line 161) | minor — unnatural Japanese | 「もし落とし物として預かっていらっしゃいませんか。」 — 「もし」 opens a conditional that never lands (no 〜たら/〜なら consequent), and 預かる+ていらっしゃる reads as strained honorific for a lost-property enquiry. Same line: 「連絡先はメッセージに残した番号までお願いします。」 is self-referential (she is *in* the message). | 「落とし物として届いておりませんでしょうか。」 and 「ご連絡は、このメッセージに残しました番号までお願いいたします。」 |
| F10 | 問題4-4番 (script line 198) | minor — unidiomatic/ambiguous | 「次の部署の会議」 parses two ways ("the next department's meeting" / "the department's next meeting"); native usage is 「次の部会」「部内の会議」. | Superseded if F4 replaces the item; otherwise 「今度の部内の会議」. |
| F11 | 問題5-1番 (script line 257) | minor — announcer wording fidelity | Test 1 speaks 「質問。夫婦はどのソファを買いますか。」. In `imported-n2-2025-07` the 問題5 1番 question carries **no** 「質問。」 marker (「問題に対応するために、何をすることにしましたか。」); only 2番 uses 質問1。/質問2。, which test 1 does correctly. | Drop the 「質問。」 prefix on 問題5-1番. |
| F12 | 問題5-2番 (script lines 263–264) | minor — block convention | The block's first line is the lead-in, not the situation: `2番。まず話を聞いてください。…` with 「料理教室の説明を聞いて、夫婦が話しています。」 pushed to line 2. `choukai-script-writing` requires marker + situation on the same line, and the official model is exactly `2番。ラジオを聞いて男の人と女の人が話しています。`. Same root as the already-filed spoken-lead-in defect. | One edit: `2番。料理教室の説明を聞いて、夫婦が話しています。` — deleting the lead-in fixes both. |
| F13 | 問題4, all 12 blocks | minor — block convention | Marker lines are bare (`1番。`) with the stimulus on line 2 behind a `女:`/`男:` label. Convention and the official model put the stimulus on the marker line (`1番。昨日は腹痛でおかゆすら食べられなかったんだ。`). Harmless to the parser (`validate_script()` passes: 3 option lines present) and it buys a voice contrast against the narrator-read options, but it is an undocumented divergence and adds a 1.3 s gap the official has not. | Either normalise to the official shape, or add the exception to `choukai-script-writing` §"Block conventions" explicitly. |

### Already filed by `make check` — not re-counted
Confirmed present, no additional instances beyond F2/F3/F6 above:
問題1 例 script block identical to test 2 **and** to official July 2025; 問題2 例
script block identical to official July 2025 (verified by exact block match, and
no other block in test 1 exceeds 0.55 similarity to any block in tests 2/3/4 or
the official paper — the 33 item blocks are otherwise original); 問題5 2番
lead-in spoken; `聴解_チャプター.json` `script_sha: null` while
`sha1(聴解スクリプト.txt)[:12] = dab82a49b64c`; three two-party one-voice items.

---

## 3. Root causes (step 6.5) — grouped

| ID | Findings | Code | Tests showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|---|
| RC-1 | F1, F5 | `GATE-BLIND` (the rule exists and is specific — `choukai-script-writing` §"The keyed option must be quotable" even names test 1 問題2-1番 — so the paper side is `RULE-IGNORED`, carried forward unrepaired; what is missing is enforcement) | 4 of 4 per that section; verified here for test 1 | `tools/check_consistency.py` | Add `check_choukai_option_grounding()`: for every 問題1–3 item, require the 解説 cell to contain exactly (options−1) lines matching `^\d ✗「(.+)」→ .+$`, and require each captured quote to appear **verbatim** in `聴解スクリプト.txt` within that item's block. This is fully string-decidable (unlike the token-overlap WARN, which the skill correctly says can never be promoted) because it checks the *author-supplied* quote, not semantic similarity. Fail, not warn. Test 1's 問題1–3 解説 cells today carry prose, not the mandated per-option lines, so the check would have caught F1 and F5 at once. |
| RC-2 | F2 | `GATE-WRONG` (a copy check exists but measures only one of the two files the 例 lives in) | 2 of 4 (tests 1, 2) | `tools/check_consistency.py` | Extend the existing "no 例。block is byte-identical to another test's" check to the booklet: parse the `**例**` option list out of each `tests/*/聴解.md` 問題1/問題2 block and fail on an exact list match against another test **or** against any `imported-*` paper. Same exemption for imported papers as the script-side check. |
| RC-3 | F3 | `PIPELINE-GAP` + `GATE-WRONG` (staleness is a hard failure for the MP3 but only a WARN for HTML, and the WARN fires on a *missing stamp*, never on mtime) | 5 of 5 tests warn; test 1 additionally has HTML older than its Markdown | `tools/check_consistency.py` + `.agents/jlpt-test-generation/SKILL.md` | (a) Promote "built HTML records its source sha" from WARN to FAIL once every test has been rebuilt once. (b) Add a cheap pre-check that fails when `mtime(聴解.html) < mtime(聴解.md)` or `mtime(解答.html) < mtime(any source .md)` — mtime catches the case where the stamp is simply absent. (c) In `jlpt-test-generation`'s workflow, make step "regenerate artifacts" a single ordered command block `make mp3 <id> && make booklet <id> && make sheet <id> && make check` so a script fix cannot ship with stale HTML. |
| RC-4 | F4 | `RULE-UNENFORCEABLE` — `exam-qa-review` §2.5 says 即時応答 idioms must sit in the N2 band, but `references/level_band_grammar.txt` is scoped to 問題7–9 keys, so there is no list a 問題4 item can be checked against | 1 of 4 verified in scope (聴解 only) | `.agents/exam-qa-review/references/level_band_grammar.txt` + `.agents/question-authoring/SKILL.md` + gate | Add a `## TOO_EASY_QR` block to the band file containing bare-confirmation and N3 core forms (`っけ`, `だっけ`, `はずだ` as sole point, `てもいい`, `なきゃ`) and have `check_consistency.py` match every 問題4 stem+key in `聴解スクリプト.txt` against it. In `question-authoring`, state as a construction rule (not a review check): **every 即時応答 stem must instantiate one sampled `quick_response` pool item**, named in the 解説 cell — which also makes the spec audit mechanical. |
| RC-5 | F6 | `GATE-WRONG` — the casting check is scoped to two-party items, so any third speaker hides a duplicate voice | 3 two-party instances already flagged in test 1; 2 three-party instances invisible in test 1, unmeasured elsewhere | `tools/check_consistency.py` + `.agents/choukai-mp3-generation/SKILL.md` §Casting | Change the check from "items with exactly 2 labels" to "any item block": WARN when two distinct labels in one block resolve to the same `voice` **and** their `rate` differs by <6 percentage points. Add to `choukai-mp3-generation` §Casting: "three-party items need three distinguishable voices; 女/妻/店員/教室の人/先生/医者/専門家/レポーター/職員/係員/担当者/講師/アナウンス(ー) are all one female voice — at most one per item." |
| RC-6 | F7, F8, F11, F12, F13 | `RULE-UNENFORCEABLE` — `jlpt-exam-structure` gives question *shapes* in prose and the block conventions in prose, so nothing decides whether a stem or a block matches | F8: 2 of 4; F7: 1 of 4; F12: 4 of 4 (same root as the already-filed lead-in defect) | `.agents/jlpt-exam-structure/SKILL.md` + `tools/check_consistency.py` | Add a canonical **stem template table** next to the existing instruction-line table, transcribed from `imported-n2-2025-07`: 問題1 → `…は(この後|このあと)(まず)?何をしますか。` / `…しなければなりませんか。`; 問題2 → `どうして…か。` / `…一番…は何ですか。` / `どのように…か。`; 問題3 → `…は何について話していますか。`; 問題5-1番 → question line with **no** 「質問。」 prefix; 問題5-2番 → `質問1。`/`質問2。`. Then a gate check that every item block's last question line matches its 問題's regex set. Also state explicitly that 問題4 stimulus and 問題5-2番 situation go on the marker line (F12/F13). |
| RC-7 | F9, F10 | `RULE-MISSING`, and **it must stay human judgment** | not machine-countable | — | Naturalness of Japanese cannot be mechanized here; the honest fix is that the read-aloud pass stays a reviewer duty (`exam-qa-review` §3 "Every sentence is Japanese"). No skill edit proposed. Recording it so the next reviewer does not assume the gate covers it. |

---

## 4. Coverage — grounding table, all 問題1–3 distractors

Every wrong option → the script line that raises it, or `NOT IN SCRIPT`.
(K) marks the key.

**問題1**

| Item | Opt | Grounding |
|---|---|---|
| 1番 | 1 交換の書類に記入する | 「レシートの確認や書類への記入は、本体がそろってからで大丈夫です」→ 後回し |
| | 2 (K) 車から商品を取ってくる | 「では、まず車から商品を取ってきていただけますか」 |
| | 3 レシートを見せる | 「今はレシートだけ持ってきていて」＋「レシートの確認…は、本体がそろってから」→ 後回し |
| | 4 保証期間を調べる | 「保証期間内でしたら交換できますが」— 名詞のみ。誰も「調べる」と言わない → **F5** |
| 2番 | 1 質問を増やす | 「質問の数は十分です」→ 否定 |
| | 2 対象者を変える | 「対象者の選び方も問題ありません」→ 否定 |
| | 3 (K) グラフにする | 「まずは結果を見やすくすることを優先してください」＋「グラフにした方がいい…?」「ええ」 |
| | 4 参考文献を追加 | 「それは発表の後でも間に合うから」→ 後回し |
| 3番 | 1 ネットで申請し直す | 「オンライン申請の本日分の受け付けはすでに終了しております」→ 否定 |
| | 2 (K) 窓口に取りに行く | 「窓口でしたら、本日の午後五時まで発行できます」→「じゃあ、窓口に取りに行きます」 |
| | 3 家族に取ってもらう | 「代理の方がお受け取りになる場合でも、ご本人の委任状と代理人の身分証が必要です」→ 実質不可 |
| | 4 郵送 | 「郵送ですと到着まで数日かかります」＋「それだと間に合いませんね」→ 否定 |
| 4番 | 1 (K) 薬を飲んで様子を見る | 「まず一週間飲んでみてください」／「まずは薬で様子を見ましょう」 |
| | 2 大学病院で検査 | 「その場合は…大学病院を紹介します」→ 条件付き・後 |
| | 3 一週間後にまた来る | 「まず一週間飲んでみてください」— 再診の言及なし → **F5** |
| | 4 運動を始める | 「軽い運動も効果的ですが、無理はしないでくださいね」→ 副次的 |
| 5番 | 1 ポスターを印刷 | 「ポスターはもう業者に頼んであるから大丈夫」→ 否定 |
| | 2 飾り付け | 「会場の飾り付けは私と山田さんでやるし」→ 他者に割り当て |
| | 3 名簿を作る | 「それお願いしたいんだけど、その前に…」→ 後回し |
| | 4 (K) マイクの音を確認 | 「マイクがちゃんと使えるか見てもらえる?」→「先にそっちを確認してから」 |

**問題2**

| Item | Opt | Grounding |
|---|---|---|
| 1番 | 1 電車が事故で止まった | 「電車、止まってたの?」「いや、電車は普通に動いてたんですけど」→ 否定 |
| | 2 朝寝坊 | **NOT IN SCRIPT** → **F1 (AUTO)** |
| | 3 (K) 忘れ物を取りに帰った | 「会議で使うUSBメモリを家に忘れたことに気づいて」「それで取りに戻ったの?」「はい」 |
| | 4 最寄り駅を間違えた | **NOT IN SCRIPT**（解説も自認）→ **F1 (AUTO)** |
| 2番 | 1 値段が高い | 「お家賃は予算内だし」→ 否定 |
| | 2 駅から遠い | 「歩くのは好きなので、それは問題ないんです」→ 否定 |
| | 3 部屋が狭い | 「お部屋の広さもちょうどいいと思います」→ 否定 |
| | 4 (K) 周りがうるさい | 「すぐ隣が幹線道路ですよね。夜も車の音、結構するんじゃないかと」「静かな環境じゃないと集中できない」 |
| 3番 | 1 値段が安い | 「よく『値段が安いから』と言われるんですが、実は特別安いわけではないんです」→ 否定 |
| | 2 (K) 野菜が新鮮 | 「毎朝、契約している農家から直接野菜を仕入れています。とにかくこれに尽きますね」 |
| | 3 店の雰囲気 | 「店内も落ち着いた雰囲気で素敵ですね」＋「内装やサービスにも気を配ってはいますが、やはり一番の売りは素材」→ 従属化 |
| | 4 店員のサービス | 同上「サービスにも気を配ってはいますが」→ 従属化 |
| 4番 | 1 給料が安かった | 「給料も悪くなかったし」→ 否定 |
| | 2 (K) 自分の店を持ちたかった | 「自分の店で自分の考えたパンを売りたいという夢がありました」「思い切って退職しました」 |
| | 3 体を壊した | 「そうではなくて、健康にはまったく問題ありませんでした」→ 否定 |
| | 4 家族の近くに住みたかった | 「それが理由で辞めたわけではありません」→ 明確に否定 |
| 5番 | 1 部品が届かなかった | 「心配してた時期もあったんですけど、それは何とか間に合って」→ 否定 |
| | 2 工場で事故 | 「いえ、事故は一度も起きていません」→ 否定 |
| | 3 デザイン変更 | 「おかげでデザインは変えずに済みましたし」→ 否定 |
| | 4 (K) 検査で問題 | 「発売前の最終検査で、長時間使うとモーターが熱くなりすぎることがわかったんです」 |
| 6番 | 1 毎日少しずつ続ける | 「毎日の練習も大事ですが、間違いを恐れて黙っていたら…話せるようにはなりません」→ 従属化 |
| | 2 いい教科書 | 「『どの教科書がいいですか』…もちろん、いい教材や話す相手がいれば理想的です。でも…そこではない」→ 否定 |
| | 3 ネイティブの友達 | 同上「『ネイティブの友達を作るべきですか』」→ 否定 |
| | 4 (K) 間違いを恐れない | 「上達する人は、間違えることを怖がりません」「この繰り返しができる人が、結局一番伸びるんです」 |

**問題3** (概要理解 — distractors are competing topic labels; official practice
grounds each on a noun from the talk, which all 15 here do)

| Item | Opt | Grounding |
|---|---|---|
| 1番 | 1 睡眠不足が原因の病気 | 「毎日の睡眠不足が借金のように積み重なって」（病気は未言及・話題の外延） |
| | 2 (K) 週末の寝だめの問題点 | 「週末の寝だめで完全に解消することはできません」「悪循環に陥ります」 |
| | 3 早起きの方法 | 「同じ時間に寝て、同じ時間に起きることです」 |
| | 4 体内時計の仕組み | 「体内時計が乱れ」 |
| 2番 | 1 試験的な運用 | 「まず一部の部署で試験的に運用しました」→ 経緯の一部 |
| | 2 対応時間の短縮 | 「クレーム対応にかかる時間を減らすための制度だ」→「それだけが狙いではない」で否定 |
| | 3 (K) 解決の質で評価 | 「それより大きいのは、対応件数の多さではなく、どれだけ丁寧に問題を解決できたかで一人ひとりを評価できるようになることです」 |
| | 4 残業を減らす | 「残業が減るのも助かる点です」→ 従属化 |
| 3番 | 1 正しい育て方 | 「世話といっても、水やりと、ときどき葉のほこりを拭くくらいです」 |
| | 2 掃除を楽にする方法 | 「葉のほこりを拭く」「部屋の空気が変わり」 |
| | 3 (K) 植物を育てることのよさ | 「気持ちに余裕が生まれるんです」「机の上に小さな鉢を一つ置いてみてはいかがでしょうか」 |
| | 4 忙しい毎日の時間の使い方 | 「忙しい日は、一日があっという間に過ぎてしまいますが」 |
| 4番 | 1 ネットを使うな | 「インターネットで調べ物をしますね。とても便利です」→ 否定 |
| | 2 (K) 正しいか確かめる | 「必ず複数の情報源を比べること」「情報を集める力よりも、情報を疑う力」 |
| | 3 本や論文だけ | 「できれば本や論文など…で確認すること」→ 「だけ」への誇張 |
| | 4 専門家は必ず正しい | 「専門家が書いたものもあれば、間違った情報を…写しただけのものもあります」→ 否定 |
| 5番 | 1 本を借りる手続き | 「中央図書館の二階の閲覧席で勉強していた」（借用は未言及） |
| | 2 (K) 落とし物の確認 | 「青い折りたたみ傘を置き忘れたようです。もし落とし物として預かっていらっしゃいませんか」 |
| | 3 開館時間を聞く | 「本日の午後三時ごろ、もう一度図書館に伺えますので」 |
| | 4 勉強席を予約 | 「二階の閲覧席で勉強していたのですが」 |

### Other checks run

- **問題4 keigo/rank direction (all 11 + 例).** 1番 女→課長 「お送りした…目を通していただけましたか」 → 課長 downward 「ざっと読みましたよ」 ✓; 6番 「席を外しております」 → 「後ほどかけ直します」 ✓ (option 3 mis-reads a temporary absence as 出張 — a real trap); 9番 「教えていただけませんか」 → 「今お見せしますね」 ✓ with option 1 「教えていただきました」 the reversed-direction trap the 解説 names. No item keys a superior speaking humble keigo downward. Idiom band: 目を通す / に決まっている / のあまり / 〜がい / 席を外す / 〜ようがない / 〜ばいいのに / 敬語方向 / お言葉に甘えて / てっきり are all N2; **4番 alone is below band (F4)**.
- **例 answerability (all four).** Each 例's announced number is the option its dialogue supports, and each matches the マークシート pre-mark (§1). 問題3/問題4 例 options are spoken, not printed, per the printed/spoken table ✓.
- **問題5 structure.** 1番 options spoken (`1、12万円の最新モデル。`…), booklet prints only `1 ・ 2 ・ 3 ・ 4` ✓. 2番 options printed (体験/基礎/集中/オンライン), never spoken ✓. 質問1 and 質問2 sit in the same block ✓. 3 answers from 2 blocks ✓.
- **Booklet ↔ script sync.** All five 問題N instructions in `聴解.md` are character-for-character the canonical texts in `jlpt-exam-structure` §"問題N instruction lines" (including 問題2's 「問題用紙を見てください」 — test 1 does **not** carry the 「せんたくしを読んで」 drift the skill warns about), and the script repeats them with 「では、練習しましょう。」 appended ✓. 問題5 1番 lead-in verbatim ✓; 2番 lead-in spoken (already filed, F12). Every printed option in 問題1/2/5-2番 matches the item it belongs to; no printed option is spoken and no spoken choice is printed.
- **Narration ↔ `SPEAKER_MAP` gender.** All 18 narration lines checked. No 「〈label〉の男/女の人」 contradicts its casting: the only gendered narrations are 女の人/男の人 on `女`/`男` themselves, and every role label (店員, 職員, 医者, 先生, 専門家, レポーター, 店長, 部長, 教室の人) is narrated without a gender claim. Zero mismatches — test 3's defect class is absent here. Duplicate-voice pairs: 5 (3 filed, 2 new — F6).
- **Structural validation.** `validate_script()` → `script OK: 46 blocks, items 問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2`; no answer-reveal line outside the four 例 confirmations; no `（※…）` annotations; no ASCII `,`/`.`; every speaker label is in `SPEAKER_MAP`; file ends with 「これで、聴解試験を終わります。」.
- **Verbatim-copy sweep, both directions.** Every one of test 1's 33 item blocks compared against every item block of tests 2, 3, 4 and `imported-n2-2025-07` (`difflib` ratio, threshold 0.55): exactly three hits, all already-filed 例 copies (問題1 例 = test 2 = official; 問題2 例 = official). No numbered-item dialogue, and no option line outside the two 例 sets, is shared with any other paper — **except** the booklet 例 option lists (F2), which the script-level sweep cannot see.
- **Artifacts.** `sha1(聴解スクリプト.txt)[:12] = dab82a49b64c`; `聴解_チャプター.json` records `script_sha: null` (already filed) and its 38 chapters (5 sections + 33 items) were written 2026-08-04, ~16.6 h before the current script — **the shipped MP3 can be speaking superseded text and must be rebuilt**. `聴解.html`/`解答.html` likewise predate `聴解.md` with no `src_sha` stamp (F3).

---

## 5. Skips (explicit)

1. **Spec/blueprint audit of 問題1/2/4 target items — SKIPPED.**
   `logs/test_spec.json` describes **test 3** (`"test_id": "3", "seed": 20260806`),
   and `logs/ledger.json` has no history row for test 1 — only `legacy`
   (`test_id: "legacy", seed: null`), an unattributed aggregate of 24
   `quick_response` items covering more than one test. There is no governing
   blueprint for test 1 on disk, so target-item and answer-position compliance
   cannot be verified. Partial evidence recorded instead: of test 1's 11 問題4
   items, only 「席を外しております」(6番) and 「お言葉に甘えて」(10番, in the
   keyed reply) appear in the `legacy` pool row; the other nine are unattributable.
   None of the 11 recurs in tests 2/3/4, so 即時応答 rotation is at least clean.
2. **Audio not listened to.** MP3 staleness judged from mtime + `script_sha`
   only; pacing/loudness are `official-audio-analysis`'s domain and were not
   re-measured.
3. **言語知識・読解 (問1–71) not reviewed** — another reviewer's scope.
4. **Cross-test topic table (step 5) not built** — another reviewer's scope. The
   only cross-test work done here is item-level: the verbatim-copy sweep and the
   即時応答 rotation check above.
5. **Harvest URL verification (step 6.5) not run** — `logs/seeds.json` belongs to
   test 3's harvest and no seed provenance exists for test 1.
6. **Skill files not edited.** `exam-qa-review` permits the reviewer to add a
   newly-found defect class to its own file; every class found here is already
   listed there, so no edit was needed. Per the assignment, no file in the repo
   was modified.
