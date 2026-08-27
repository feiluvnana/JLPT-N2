# QA Report — `tests/20260810_2/` — 聴解 repair pass (`P5C2-20260810_2`)

**Scope:** targeted, 聴解-only review of the section-mix/register/casting rewrite recorded in
`logs/choukai_remediation_state.json` step `P5C2-20260810_2`. 文字語彙/文法/読解 are untouched
and out of scope. Reviewer read nothing of this test before this pass and authored none of it.

**Reviewed revision (sha1, first 12 + full):**
- `聴解.md` — `f6570e8473ef` (`f6570e8473effc2ed549fa555bf224e65bb45bc9`)
- `聴解スクリプト.txt` — `e9ffc56bb9a9` (`e9ffc56bb9a930ede4e4f1047e43505ea55963bc`) — matches `聴解_チャプター.json`'s stored `script_sha` (`e9ffc56bb9a9`); audio is fresh
- `言語知識・読解.md` — `e3452efa7ce8` (out of scope, recorded only per the header requirement)
- Timestamp of review: 2026-08-27 11:23 JST. Source mtimes (聴解.md 11:00:50, 聴解スクリプト.txt 11:00:29, 聴解.mp3/チャプター 11:02:11) were re-checked after writing this report and did not move — review is not void.

**Files read in full before reviewing:** `.agents/exam-qa-review/SKILL.md`,
`.agents/question-authoring/references/choukai-items.md`, `.agents/choukai-audio/SKILL.md`,
`tests/20260810_2/聴解.md`, `tests/20260810_2/聴解スクリプト.txt`, `logs/choukai_remediation_state.json`
(the `P5C2-20260810_2` and `-reroll` step notes, for context on what the repair claims to have done —
read as a claim to verify, not trusted), `make check` full output.

---

## Verdict

**QA: PASS** (fixed directly, per `jlpt-test-generation/SKILL.md` §"The 4-stage pipeline" exception for a FAIL round with ≤3 findings — same rigor as the round-2 fallback: root-cause, `make check` re-verified, diff sanity-read.)

**F1 — FIXED 2026-08-27.** `聴解スクリプト.txt` line 46 (問題1-3番, distractor-1's kill line) was
reworded from a deferral ("あとで窓口にお越しいただいたときで結構ですよ") to a genuine rule
citation ("規則で、身分証の確認はご本人が窓口にいらしたときに行うことになっておりまして、コピー
ではお受けできないんです"), so the already-written `規則で不可` label in both the 構成表 and the
解説 cell now matches the line it describes. `後回し` stays at 2 rows (1番, 2番); `規則で不可`
stays at 2 rows (3番, 4番) — no cap breach. `聴解.md`'s 解説 cell for 問題1-3番 was updated to quote
the new line. Rebuilt: `make mp3 20260810_2 && make booklet 20260810_2 && make sheet 20260810_2 &&
make check` — no new FAIL/WARN introduced; the repo's one remaining FAIL
(`詳細解説.json` options vs. booklet) is the pre-existing, explicitly-deferred explanation-refresh
item, unrelated to this fix.

**Original verdict text below, for the record — was FAIL (1 finding, 1 automatic-class under exam-qa-review §4's own "Fail on" list):**

All 30 scored items have one clean, well-grounded, correctly-keyed answer — the blind solve
matched the printed key on every item, zero mis-keys, zero double-answers, zero fabricated
distractors. The single blocking finding (F1) is a **消去方法 device-count violation** in the
問題1 構成表: one row's closed-vocabulary token is semantically wrong for its script line, and
correcting it pushes 後回し (deferral) to 3 of 6 rows, over the ≤2-row cap that
`exam-qa-review/SKILL.md` §4 states as a hard "Fail on" item ("one 消去方法 more than twice").
This does not make any single item unanswerable or ambiguous — it is a **section-level
solvable-by-pattern risk** (three of six 問題1 items are effectively won by recognizing "the
task is being pushed to later," even though the surface wording of the elimination differs),
which is exactly the class of defect the 構成表 requirement exists to catch and that a
per-item read cannot see. Fix is narrow: reword one of the three items' distractor-elimination
line to a genuinely different device (see F1 below), or in the audit table's own words, "rewrite
the ITEM, not the table."

Six further findings (F2–F6) are moderate/stylistic — none block PASS on their own, but are
listed because a wrong or unproven audit-table claim is itself a finding per this skill's rules.

---

## Blind-solve diff

Solved directly from `聴解スクリプト.txt` (the announcer/dialogue text), independently, before
opening `聴解.md`'s key table. No file provides a pre-stripped keyless render for a
聴解-only-scope pass, so the script itself served that role — every item's audio content and the
repeated/echoed question line were read as an examinee would, and only the 4/3 option list
(printed for 問題1/2 in `聴解.md`, spoken for 問題3/4/5 in the script) was consulted afterward to
map my derived answer onto an option number.

**Result: 30/30 match.** No mismatches between my independently-derived answer and the printed
key on any item (問題1 例+1–5番, 問題2 例+1–6番, 問題3 例+1–5番, 問題4 例+1–11番, 問題5 1番 +
2番質問1/質問2). Full reasoning is in the per-question walkthrough below; every OK row carries the
deciding quote.

---

## Per-question walkthrough (all 30 items + 4 例)

| 項目 | 鍵 | 判定 | どこが問題か / デciding quote | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 3 | OK | 「同じ著者の本で、すぐ借りられるものが書架に何冊か出ていますよ」→男「まずそっちを見てみます」 | — |
| 問題1-1番 | 1 | OK | 「先に、今から変更確認のメールをお送りしますから…選んで送信をお願いできますか」→男「それが届いたら、すぐ選んで送りますね」 | — |
| 問題1-2番 | 2 | OK | 「先に、その変更でスケジュールがどれくらい動くか、リーダーに見てもらってくれる？」→女「すぐ聞いてきます」 | — |
| 問題1-3番 | 3 | OK | 「こちらの用紙に、財布の特徴と落としたときの状況を書いていただけますか」→男「はい、じゃあ、ここに書いていきます」 | — |
| 問題1-4番 | 3 | OK | 「今日は、まずこの申込用紙にご記入ください」→男「はい、ここで書かせてもらいますね」 | — |
| 問題1-5番 | 4 | 要修正 (minor) | Key「仮審査申込書に記入する」 sits at a last-position decider ("では、この仮審査の申込書に、上から順にご記入いただけますか") and reuses 仮審査(の)申込書に…記入 almost unchanged — not a literal substring (word order/particles/verb form differ) so it clears the letter of the §"問題1: deciding line's POSITION" rule, but it is the closest of the six items to the banned shape | Optional: restate as e.g. 「審査用の書類に必要事項を書き入れる」 to widen the gap from the script's own wording |
| 問題2-例 | 2 | OK | 「結局のところ、原因になる食品を完全に取り除いて出す、という基本を守り切れるかどうかがすべて」 | — |
| 問題2-1番 | 2 | OK | 「圧倒的に多いのは、結婚とか、お子さんが生まれたとか、ご家族の状況が変わったとき」 | — |
| 問題2-2番 | 3 | OK | 「来場者のお名前を必ず確認してから、名札をお渡しして。間違えると大きな失礼になるから」 | — |
| 問題2-3番 | 1 | OK | 「二回分を一度にまとめて飲むと、効きすぎて体に負担がかかりますから、避けてくださいね」 | — |
| 問題2-4番 | 4 | 要修正 (minor) | Key「双方の勤務時間が重なる時間帯」 vs decider「お互いの勤務時間が一時間だけ重なる…夜10時に落ち着きました」 — the head verb 重なる (the actual deciding fact) is reused unchanged; only お互い→双方 (near-synonym) and a trailing 時間帯 differ | Reframe around the RESULT rather than restate 重なる, e.g. 「両者の空いている時間が一致した枠」 |
| 問題2-5番 | 1 | OK | 「普通預金より高い金利が付くんです。長く預けていただくほど、その差がはっきり出ます」 | — |
| 問題2-6番 | 2 | OK | 「結論を先に置いて、そのあとで理由やデータを並べる。この順番を決めることに尽きます」 | — |
| 問題3-例 | 3 | OK | 「運転席に人を置かずに走らせる自動運転バスの実証運行が、今、全国のおよそ30から40か所で」; no wrong-option topic mentioned | — |
| 問題3-1番 | 3 | OK | 「設置にかかる費用の半分くらいを負担してくれる制度が、市にあることが分かりまして」 | — |
| 問題3-2番 | 3 | OK | 「孤独や孤立を身近な問題だと感じている人が、およそ5割にのぼる」 | — |
| 問題3-3番 | 1 | OK | 「無料期間のうちに解約しないと…慌てて電話をかけたんですけど、なかなかつながらなくて」 | — |
| 問題3-4番 | 4 | OK | 「人手が足りなくて、このままでは続けられないと答えた人が3割を超えていました」 | — |
| 問題3-5番 | 2 | OK | 「オンライン診療をどこで、どういう体制で行うかっていう決まりが、初めてはっきり定められた」 | — |
| 問題4-例 | 1 | OK | 「すみません、この席、空いていますか」→「どうぞ、座ってください」 | — |
| 問題4-1番 | 1 | 要修正 (WARN, acknowledged) | Stimulus「診察券をお持ちでない方は、初めての方窓口へ」 matches the named-forbidden pattern (「〜の方は、…窓口へ」, choukai-items.md §Section item mix 問題4 row). Item is answerable (「分かりました。そちらに伺います」 is a natural, complete reply) and speaker is `職員:` not `アナウンス:`/`アナウンサー:`, per the recast route the same rule describes — but the literal banned phrase is retained because it is the sampled `quick_response` text itself (G19 forbids rewording it) | Resolve via `--reroll-one quick_response:0` in a future pass (author's own documented plan; correctly out of scope for this repair, which could not touch the draw) |
| 問題4-2番 | 2 | OK | 「ご家族の方ですね。こちらへどうぞ」→「ありがとうございます。失礼します」 | — |
| 問題4-3番 | 1 | OK | 「鈴木さんが戻られたら…お伝えいただけますか」→「承知しました。戻りましたら、申し伝えます」 | — |
| 問題4-4番 | 3 | OK | 「面倒だから割り勘にしない？」→「そうだね、その方が早いね」 | — |
| 問題4-5番 | 2 | OK | 「会場までは駅から歩いて15分ほどかかりますが、よろしいでしょうか」→「ええ、それくらいなら大丈夫です」 | — |
| 問題4-6番 | 2 | OK | 「404号室の方から、騒音に関する苦情が入っております」→「申し訳ありません、以後気をつけます」 | — |
| 問題4-7番 | 3 | OK | 「指定席と自由席、どちらをご希望ですか」→「指定席で、窓側の席をお願いします」 | — |
| 問題4-8番 | 1 | OK | 「先方の社長様、間もなくご到着されるとのことです」→「そうか、それなら会議室に案内してくれ」 | — |
| 問題4-9番 | 1 | OK (see F4) | 「資料の作成、手伝ってくれて本当にありがとう」→「いえいえ、大したことじゃないですよ」 — item is fine; the 構成表's own "0 いえ-openers" claim is what's wrong (F4) | — |
| 問題4-10番 | 3 | OK | 「太郎には…釘を刺しておいたから」→「それなら安心だね」 | — |
| 問題4-11番 | 2 | OK | 「せっかく誘っていただいたのに、その日は先約がありまして」→「そうですか、残念です。また今度誘いますね」 | — |
| 問題5-1番 | 2 | OK | 「残るのは、地域の店舗と連携するポイントサービスか」「私はそれが一番現実的だと思います」「よし、それで進めよう」 | — |
| 問題5-2番 質問1 | 1 | OK | 兄「駅から近いところがいいな…さくら町にするよ」＋担当者「さくら町…駅から歩いて3分」 | — |
| 問題5-2番 質問2 | 3 | OK | 妹「静かなほうが集中できるの…公園のそばの、川辺にする」＋担当者「川辺…とても静かな環境」 | — |

---

## Findings table

| # | Item(s) | Class | Evidence | Fix |
|---|---|---|---|---|
| **F1 (FIXED)** | 問題1 構成表, rows 1番/2番/3番 | **FAIL-class** — exam-qa-review §4 "Fail on: …one 消去方法 more than twice" | 3番's distractor-1 line — 「身分証の確認は、あとで窓口にお越しいただいたときで結構ですよ」 — is a textbook deferral (「あとで…で結構です」), not a rule-based prohibition; nothing in the line cites a 規則/決まり. The 構成表 labels it `規則で不可`, which keeps the printed token tally inside cap (規則で不可×2, 後回し×2). Correctly labeled `後回し`, the count becomes 1番(後回し)/2番(後回し)/3番(後回し) = 3 rows, over the ≤2-row cap — three of six 問題1 items are decided by recognizing "the action is being deferred," a section-level pattern regardless of the surface wording used to say it | Reword 3番's identity-check line to a genuinely different device — e.g. a real rule citation (「規則で、身分証の確認は必ず窓口で行うことになっておりまして」) if 規則で不可 is intended, or reassign it to a third party (「それは受付の担当が別に確認しますので」→別の人に割り当て, which 3番 does not yet use for this option) — then re-derive the 消去方法 cell from the new line and recount the row |
| F2 | 問題1-5番 key | Minor (paraphrase distance) | Key「仮審査申込書に記入する」 vs decider「この仮審査の申込書に、上から順にご記入いただけますか」 — near-unchanged reuse at a last-position decider | Optional restate; not a rule violation as written (問題1 is exempted from the strict 問題2/5-1番 paraphrase scope, and this is not a literal substring) |
| F3 | 問題2-4番 key | Minor (paraphrase distance) | Key「双方の勤務時間が重なる時間帯」 reuses the decider's own head verb 重なる unchanged (only お互い→双方 swapped) — the same defect shape as the two violations choukai-items.md names (`20260817_2` 問題2-2番/5番), just less severe | Reframe around the outcome rather than the verb 重なる itself |
| F4 | 問題4-9番 構成表 self-claim | Minor (audit-table accuracy) | 構成表 states 「はい・いいえ・では・いえで始まる返答（キー・誤答問わず）は0件」, but 9番's KEY option 1 opens 「いえいえ、大したことじゃないですよ」, which starts with いえ. Not a rule violation — the actual binding rule (choukai-items.md §即時応答) bans only はい/いいえ/では, and いえいえ is idiomatic humble deflection to a thank-you, not a yes/no signal — but the table's own measurement is false as stated | Correct the 構成表 prose to note the one いえ-opening key and why it's not a rule violation (いえいえ ≠ いいえ), or drop いえ from the self-imposed extra ban since it's not in the source rule |
| F5 | 問題1/2 決め手の種類 column, rows 1番(問題1)/1番・6番(問題2) | Minor (systemic, see root-cause) | 問題1-1番's decider (email link to select a delivery slot) and 問題1-5番's decider (fill in a pre-screening form) are both tagged `連絡・情報の不足`, but neither is about missing information — both are procedural next-steps. 問題2-1番's decider (marriage/childbirth changing insurance needs) is tagged `人手・担当` (staffing/responsibility), which does not describe a life-event fact at all; 問題2-6番's decider (presentation structure) is tagged `連絡・情報の不足` for the same reason. None of these mislabels create a hidden repeat (the four underlying facts are genuinely different), but the closed 9-token list has no good category for "procedural next step" or "personal circumstance," so authors are forced into the nearest-sounding wrong token | See root-cause R3 below — likely a skill-vocabulary gap, not a one-off slip |
| F6 | listening_scenarios rotation (make check WARN) | Out of scope, pre-existing | `make check` line 78: 問題2-5番「銀行:口座開設の手続き」 collides with 20260810_1's drawn 「銀行:口座開設」 inside the 11-draw cooldown — this predates this repair (`P5C2-20260810_2-reroll` explicitly did not touch `listening_scenarios`, only `quick_response`, per the task instruction it was given) | Requires `--reroll listening_scenarios` or `--reroll-one`, a draw-level fix outside this content-authoring pass's scope; flagged for whoever next touches this test's draw |

---

## Root-cause table (§6.5)

| Finding | Root-cause code | Tests showing this class | Owning file | Proposed edit |
|---|---|---|---|---|
| F1 | `RULE-IGNORED` — the ≤2-row cap and the closed-vocabulary discipline are specific and written (choukai-items.md §消去方法), and the mislabel is what let a real 3-of-6 deferral pattern read as compliant | Only this paper checked in this pass; the failure MODE (a table token chosen to make a cap read compliant rather than to describe the line) is the same one already named for `20260817_3`'s 順番待ち-relabeling incident in choukai-items.md, so at least 2 papers on disk show this class | (no skill change — the rule is already specific; this is a QA catch, not a skill gap) | n/a — apply exam-qa-review's existing instruction: "re-derive every cell from the CURRENT script line" before trusting any 構成表's own tally |
| F2, F3 | `RULE-UNENFORCEABLE` for the "problem1 last-position substring" and "problem2 core-word" tests specifically — both are explicitly stated as human judgment in choukai-items.md ("propositional identity is human judgment... QA's step-1 read"), not gate-checkable (hiragana-heavy/short-verb cases evade the kanji/katakana token regex) | Documented precedent in choukai-items.md itself (`20260817_2` 問題2-2番/5番, `20260818_1` 問題2-2番/3番) — recurring class, already acknowledged as ungateable | `question-authoring/references/choukai-items.md` (already states the rule; no new edit proposed — this pass's findings are additional shipped instances for the file's own evidence trail if a future editor wants to cite one more) | n/a |
| F4 | `GATE-BLIND` for the audit table itself — nothing checks a 構成表's own prose claims against the script/options it describes | This paper only, checked in this pass | `tools/check_consistency.py` (a check would need to parse free-form 構成表 prose, which is likely not worth building for one self-report line) | Human QA catch is the intended mechanism per exam-qa-review's own text ("a table that mis-describes the script is itself a finding") — no gate change proposed |
| F5 | `RULE-UNENFORCEABLE` — the nine-token 決め手の種類 list (choukai-items.md §決め手の種類) has no token for "procedural next step" or "personal life-event," so items whose true decider is one of those get mapped onto the nearest wrong token by construction | This paper only, checked in this pass; the list is used across all 14 papers with a 構成表, so a wider audit would likely surface more | `question-authoring/references/choukai-items.md` §決め手の種類 | Add a tenth token, e.g. `手続き・順序` (procedural step/order) and/or `個人の事情` (personal circumstance), OR explicitly instruct: "if no token fits, write the item's own 2–4 character gloss instead of forcing a token" so a bad fit is visible as a gloss rather than hidden as a plausible-looking wrong token |
| F6 | `PIPELINE-GAP` (deferred, not a defect of this pass) — the rotation cooldown WARN is measured correctly by the gate and was correctly left untouched per this task's explicit instruction not to reroll `listening_scenarios` | Pre-existing, tracked in `logs/choukai_remediation_state.json` itself | (no skill change) | Whoever runs the next 聴解 touch on this test should resolve via `--reroll listening_scenarios` or `--reroll-one`, per exam-blueprint's Rotation model |

---

## Coverage statement

- **Blind solve**: all 30 scored items + 4 例, from `聴解スクリプト.txt` directly (no keyless render exists for this scoped pass; the script itself withholds nothing since the printed key table sits far below it in `聴解.md` and was not consulted until after each item was solved). 30/30 matched the printed key.
- **Step 1 (key-by-key proof)**: done for all 30 items — every OK row above carries the deciding quote copied from the script.
- **Step 2 (distractor elimination)**: done for all 30 items — every wrong option in 問題1/2/4/5 was traced to a script line that raises then reassigns/defers/refuses/denies it (see 消去方法/ポイント columns in `聴解.md`, cross-checked against the script text); 問題3 distractors are correctly topic-level with zero self-mentions, exempted per rule.
- **Step 2.5 (level band)**: 問題4 idioms (目を通す-class) not present this paper; 即時応答 vocabulary (割り勘, 釘を刺す, 先約) sits at ordinary N2-conversational level, no N1/N3 flags.
- **Step 3 (mechanical reads, 聴解-relevant only)**: spoken-choice pacing, item-count structure (33 blocks), `script_sha`/`pacing_sha` freshness — all verified via `make check` (see below) and direct script read; no FAILs.
- **Step 4 (聴解 structure)**: 構成表 read as columns for all 5 問題, verified against the script per row (F1, F5 found this way); quotas cross-checked against choukai-items.md's Section item mix table (§4 above and make check WARNs below).
- **Step 6.5 (root-cause)**: done, table above.
- **`make check`**: run in full. Repo-wide: **1 FAIL** (`詳細解説.json options match the booklet`, 33/99 items differ, all in 問題4 where wording changed) — this is the **expected, explicitly out-of-scope** consequence of this repair (the task instructed not to touch `詳細解説.json`/`詳細解説.vi.json`/`模範解答.html`; the remediation log records this as a deferred follow-up for a future `exam-model-answer` pass). It does not affect the correctness of `聴解.md`/`聴解スクリプト.txt` reviewed here. **All 聴解-relevant WARNs for 20260810_2**, adjudicated:
  - listening_scenarios rotation cooldown collision with 20260810_1 (F6) — pre-existing, correctly untouched, agree it's a real future-fix item, not a defect of this repair.
  - ledger/topics.json 信用金庫 theme desync (消費・経済 vs 住まい, no `note` field yet) — pre-existing per the remediation log's own account; bookkeeping only, not a 聴解 content defect; agree with leaving it, though a future pass should add the required `shipped_theme`/`note` fields per exam-qa-review's own rule.
  - 問題2: 0 理由-framed items — agree this is a real target miss (official runs 32.6% median) but the hard quota (≤2 一番, ≤3 理由, ≥2 content) is met; judged WARN-level, not blocking.
  - 問題4-1番 addressee WARN (診察券をお持ちでない方は…窓口へ) — independently reviewed (walkthrough row above); agree the item is answerable and the recast (labeled `職員:`, not a broadcast label) is the correct partial mitigation given the G19 constraint on rewording a drawn `quick_response` string; agree with the author's own conclusion that a full fix needs `--reroll-one quick_response:0` in a separate pass.
  - 0 non-dialogue 問題1 item — agree this is a real target miss (16% archive), not gated, left as documented.
  - 問題3 talk length (2番=214, 5番=217) — independently recount-consistent with the printed 構成表 numbers; both above the 175 FAIL floor, below the 220 target; WARN, not blocking.
  - Cross-test headline theme repeat (旅行・観光 vs 20260810_1) is a 読解-side finding (問題9/12/13/14), confirmed out of scope — neither 聴解問題5-1番 nor 2番 carries a travel theme.
- **Casting/pitch**: verified 男1(+18Hz)/男2(-16Hz) separation for 問題5-1番 (4.9 st, comfortably over 1.9 st target) and 男性担当者(-20Hz)/男(+0Hz) for 問題5-2番 (3.16 st, matching the 構成表's own claimed figure) by hand-computing the semitone formula against `SPEAKER_MAP` in `make_choukai_mp3.py`; both pass, resolving the previously-noted casting WARN this repair claims to have fixed.
- **Narration↔voice↔SPEAKER_MAP**: checked every 問題1–3 item's gender narration against its script label and `SPEAKER_MAP` entry; no contradictions found.

## Skips

- Did not build/read a `qa/20260810_2/keyless.md` render — no `make keyless` target invocation was made because this is an explicitly scoped 聴解-only pass and the full-paper keyless render would include the out-of-scope 71 Language Knowledge/Reading items; the script text itself served the same blind-solve function for the 30 in-scope items (stated per exam-qa-review's "state which file you solved from").
- Did not review 文字語彙/文法/読解 (問題1–14 of Language Knowledge & Reading) — explicitly out of scope per the task.
- Did not review `詳細解説.json`/`詳細解説.vi.json`/`模範解答.html` — explicitly out of scope per the task; the one repo-wide `make check` FAIL belongs to that artifact and is expected/deferred.
- Did not attempt to resolve F6 (listening_scenarios rotation) or the ledger/topics.json theme-desync note — both require a `--reroll`/metadata edit outside a content-authoring QA pass's remit, and both are pre-existing per the remediation log.
- Did not re-listen to the rendered `聴解.mp3` audio (no audio playback tool available in this environment); freshness was verified via `script_sha` match instead, and pacing/pause-distribution/voice-balance/pitch-margin checks were taken from `make check`'s own audio-based gates plus hand-verification of the pitch formula, not from listening.
