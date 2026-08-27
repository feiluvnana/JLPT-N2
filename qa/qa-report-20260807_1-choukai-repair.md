# QA Report — `tests/20260807_1/` — 聴解 repair pass (`P5C2-20260807_1`)

**Scope:** targeted, 聴解-only review of the full section re-author recorded in
`logs/choukai_remediation_state.json` step `P5C2-20260807_1` (+ its `-reroll` predecessor).
文字語彙/文法/読解 are untouched and out of scope. Reviewer read nothing of this test before
this pass and authored none of it.

**Reviewed revision (sha1, full):**
- `聴解.md` — `d5d430ee77ccbe39b850cc3d7ebd1b528df67680`
- `聴解スクリプト.txt` — `b4b250e61495c9d3535f0177094e09dd05321ab9`
- `言語知識・読解.md` — `f49851e4becf04273ce58c75588d95facaaca2b7` (out of scope, recorded only
  per the header requirement)
- Source mtimes at start of review: `聴解.md` 2026-08-27 12:34:57, `聴解スクリプト.txt`
  2026-08-27 12:32:10, `言語知識・読解.md` 2026-08-25 15:50:55. Re-checked after writing this
  report — unchanged. Review is not void.

**Files read in full before reviewing:** `.agents/exam-qa-review/SKILL.md`,
`.agents/question-authoring/references/choukai-items.md`, `.agents/choukai-audio/SKILL.md`,
`tests/20260807_1/聴解.md`, `tests/20260807_1/聴解スクリプト.txt`,
`logs/choukai_remediation_state.json` (the `P5C2-20260807_1` and `-reroll` step notes, read as a
claim to verify, not trusted), `make check` full output.

---

## Verdict

**QA: PASS** (0 automatic-class findings; 1 minor audit-table-accuracy finding, non-binding; the
rest are pre-existing WARN-class items already adjudicated as acceptable in
`logs/choukai_remediation_state.json` and re-independently confirmed here).

All 30 scored items (+4 例) have one clean, well-grounded, correctly-keyed answer. The blind
solve, done directly from `聴解スクリプト.txt` before opening `聴解.md`'s key table, matched the
printed key on all 34 rows — zero mis-keys, zero double-answers, zero fabricated/ungrounded
distractors, zero quota breaches against any FAIL-class threshold. `make check` reports **zero
聴解-content FAILs** for this test (the repo's one FAIL is the explicitly out-of-scope,
already-deferred `詳細解説.json` desync — see Coverage statement).

The only thing this pass required correcting is a labeling error in the audit table itself
(F1 below) — the table's own `決め手の位置` claim for 問題1-2番 does not match where the
deciding line actually sits in the script. It does not change the section's compliance with the
quota it exists to enforce (recomputed below), so it is filed as non-binding per this task's
explicit PASS/FAIL framing ("PASS … or only stylistic/non-binding").

---

## Blind-solve diff

Solved directly from `聴解スクリプト.txt` (per this task's explicit instruction — no
`qa/20260807_1/keyless.md` render exists or was built for this scoped pass): every item's
dialogue/monologue and repeated/echoed question were read and answered independently; only then
was the option-number mapping (printed for 問題1/2 in `聴解.md`, spoken for 問題3/4/5 in the
script) consulted, followed by `聴解.md`'s printed key.

**Result: 34/34 match.** No mismatches between my independently-derived answer and the printed
key on any item (問題1 例+1–5番, 問題2 例+1–6番, 問題3 例+1–5番, 問題4 例+1–11番, 問題5 1番 +
2番 質問1/質問2). Full reasoning is in the per-question walkthrough below; every OK row carries
the deciding quote.

---

## Per-question walkthrough (all 30 scored items + 4 例)

| 項目 | 鍵 | 判定 | どこが問題か / deciding quote | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 3 | OK | 女「先に、そっちの予定を確認してもらえますか」→ male's own schedule check is the first action asked of him | — |
| 問題1-1番 | 3 | OK | 女性係員「でしたら、先に利用申込書をご提出いただくことになってます」→男「はい、では窓口に行ってきますね」 | — |
| 問題1-2番 | 3 | OK | 男性担当者「それでしたら、伝票は印刷できなくても大丈夫ですよ…ただ、それは箱に商品を詰め終わってからで構いません」→女「そうですね。じゃあ、先に箱に入れときますね」 | — |
| 問題1-3番 | 1 | OK | 部長「宿を押さえるには、研修の日程表を総務に送って、泊まる人数と日にちを固めてもらう必要があるんだ。それが先だね」→女「分かりました。じゃあ、それを先にやっときます」 | — |
| 問題1-4番 | 2 | OK | 先生「東門に行く前に、先にこの受付で見学バッジを受け取っておく必要があるんだ。バッジがないと、門を通してもらえないから」→学生「あ、先にバッジなんですね」 | — |
| 問題1-5番 | 4 | OK | アナウンス「確定申告のご相談をご希望の方は、まず一階の受付で整理券をお取りください」 | — |
| 問題2-例 | 3 | OK | 男「それより一番いいのは、あと何分で来るか分かることかな…やっぱり、あと何分か分かるのが一番助かるよ」 | — |
| 問題2-1番 | 3 | OK | 女性係員「まず、こちらから上の階に注意の文書をお届けしますね」 | — |
| 問題2-2番 | 3 | OK | 店長「子ども服の売り場が仮設スペースに移るんだ。そこが一番のポイントだから」 | — |
| 問題2-3番 | 4 | OK | 係員「あくまで、何度もいらっしゃる方の負担を軽くするためのものなので」 | — |
| 問題2-4番 | 2 | OK | 係員「地震の揺れが建物にどう伝わっていくかを見ていただく模型なんです…揺れが伝わっていく様子を、目で追ってみてください」 | — |
| 問題2-5番 | 1 | OK | 教授「まず縦軸の目盛りを確認してください…軸の目盛りをまず見る。これが一番大事なポイントです」 | — |
| 問題2-6番 | 1 | OK | 男「正直、ここまで戻ってくるとは思ってなくて、ちょっとほっとしてるんだ」「驚きっていうよりは安心の方が大きいかな」 | — |
| 問題3-例 | 2 | OK | 「同じ番組に、二つの入り口から人が来てるわけです…たどり着き方が枝分かれしてきた」; no wrong-option topic mentioned | — |
| 問題3-1番 | 2 | OK | 「付けているお宅は八割台の半ばまで来てるそうなんです…条例で決められた…満たしているお宅は、七割を切る」; no wrong-option topic mentioned | — |
| 問題3-2番 | 1 | OK | 「児童クラブに登録している子は、全国でおよそ百五十七万人…受け入れの枠はかなり広がってきた」; no wrong-option topic mentioned | — |
| 問題3-3番 | 3 | OK | 「大人の一日の歩数は…どちらも少しずつ下がってきてる」; no wrong-option topic mentioned | — |
| 問題3-4番 | 2 | OK | 「備蓄を始めた方が一気に増えるのは最初の一年、二年くらいまでで、そこから先、数字があまり伸びなくなる…この足踏みしてるところ」; no wrong-option topic mentioned | — |
| 問題3-5番 | 4 | OK | 「こうした働きを持つ緑を、道路や広場の整備の中にきちんと組み込むことにしました」; no wrong-option topic mentioned | — |
| 問題4-例 | 2 | OK | 男「お先に失礼します」→標準的な返し「お疲れさまでした」 | — |
| 問題4-1番 | 3 | OK | 「ここに置いたはずの傘、知らない?」→「ごめん、心当たりがないなあ」(間接的な「知らない」の言い方) | — |
| 問題4-2番 | 3 | OK | 部下「折り入ってご相談したいことが…お時間よろしいでしょうか」→上司「うん、いいよ。そこに座って」 | — |
| 問題4-3番 | 2 | OK | 「無事に終えることができました」→「お疲れさまでした。私も楽しかったです」 | — |
| 問題4-4番 | 1 | OK | 「写真撮影はご遠慮ください」→「あ、すみません、気づきませんでした」 | — |
| 問題4-5番 | 1 | OK | 「板についてきたね」(褒め)→謙遜「恐縮です、まだまだですけど」 | — |
| 問題4-6番 | 2 | OK | 「この書類、今日中に英訳してもらえる?」→「分かりました、今すぐ取りかかります」 | — |
| 問題4-7番 | 2 | OK | 「うちのチーム勝てるかな」→「そんなの、勝つに決まってるじゃん」 | — |
| 問題4-8番 | 1 | OK | 「今度の飲み会、行くでしょ?」→間接的な断り「うーん、正直あんまり気が進まないんだよね」 | — |
| 問題4-9番 | 1 | OK | 「数字を大きくしたほうが見やすいんじゃない?」→「あ、確かに。今から直しますね」 | — |
| 問題4-10番 | 2 | OK | 「いつ終わりそう?」→見通しを答える「来月には終わるめどが立ちました」 | — |
| 問題4-11番 | 3 | OK | 「荷物、少しの間、預かっていただけますか」→「かしこまりました。少々お待ちください」 | — |
| 問題5-1番 | 3 | OK | 女「今、修理材料の確保について、調査をしっかりして、作り手を支援していく方向で検討が進んでるんです」…男2「結局、最初に聞いた調査と支援の方向で、そのまま進むってことか」女「はい…そこに落ち着いた」 — the other three proposals (海外輸入/種類削減/修理縮小＋記録化) are each explicitly denied | — |
| 問題5-2番 質問1 | 2 | OK | 夫「いつでも行けて、しかも泳げるのがいいな」→妻「二十四時間使えてプールもあるコースね」＝かえで | — |
| 問題5-2番 質問2 | 4 | OK | 妻「あおぞら…お昼のコースって水曜は開講してないみたい」→「結局、私が通えるのは夜しかないから、夜だけのコースにするわ。料金も真ん中くらいだし」＝ほしぞら | — |

---

## Findings table

| # | Item(s) | Class | Evidence | Fix |
|---|---|---|---|---|
| **F1** | 問題1 構成表, row 2番 (`決め手の位置`) | Minor (audit-table accuracy) | The table claims 2番's decider sits in 中盤 (middle third). Counting the item's 8 dialogue lines (女/男性担当者 alternating), the actual deciding line — 男性担当者「それでしたら、伝票は印刷できなくても大丈夫ですよ…ただ、それは箱に商品を詰め終わってからで構いません」 — is line 6 of 8 (position 0.75), inside the LAST third (終盤), not the middle. Recomputed for all 6 rows: 例≈0.43 (mid), 1番≈0.22 (冒頭), **2番≈0.75 (終盤, not 中盤 as claimed)**, 3番≈0.625 (中盤), 4番≈0.67 (border, defensibly 終盤 as claimed), 5番≈0.4 (defensibly 冒頭 as a single-turn announcement). Even with 2番 reclassified, the distribution stays inside the ≤3-per-third quota (e.g. 冒頭2/中盤2/終盤2), so this is a labeling error, not a quota breach | Correct the `決め手の位置` cell for 2番 from `中盤` to `終盤` and update the summary prose (「決め手の位置は冒頭3・中盤2・終盤1」→ the corrected split, e.g. 冒頭2・中盤2・終盤2), re-verifying the ≤3-per-third quota still holds (it does) |
| F2 | 問題1-2番 構成表 (`決め手の種類`) | Minor (soft judgment call, not a rule violation) | Tagged `連絡・情報の不足` (lack of contact/information). The decider is actually a SEQUENCING fact (box before calling the convenience store), closer to a procedural-order fact than "missing information." Does not create a hidden repeat with any other row (regardless of tag, 2番's underlying decider — packing-before-calling — is distinct from every other 問題1/2 item), and the closed 9-token list has no clean "sequencing" token, so this is the same vocabulary-gap class already on record for other papers (see root-cause) | No change required to ship; if the closed-vocabulary list is ever extended, a `手順・順序` token would fit this row better than any of the nine current options |
| F3 | 聴解 register (whole section, `make check` WARN) | Minor, pre-acknowledged | Short reaction-turn rate measures 9% of 121 turns (official 18%; the register rule's own stated floor for "the conversation lets the other speaker land" is ~12%). `logs/choukai_remediation_state.json`'s own `P5C2-20260807_1` note records this residual and explicitly leaves it WARN-class, not fixed further. Independently confirmed present and unchanged | Optional future pass: add 3–5 more short acknowledgement turns (「うん。」「そうですか。」) distributed across 問題1/2, re-run `make mp3` |
| F4 | 問題1-5番 (closing-turn leak, `make check` WARN) | Minor, structural, pre-acknowledged | 「一階」「受付」「整理券」 all surface in what the parser reads as the item's one and only turn (a single continuous `アナウンス:` line — this is the section's sole non-dialogue item, required by the ≥1-non-dialogue-item target). Because there is only one turn, the deciding phrase is unavoidably inside "the last line" by construction. `logs/choukai_remediation_state.json` records this as an accepted structural tradeoff for the non-dialogue item shape, not solvable without removing the non-dialogue item itself (which is required elsewhere in the quotas) | No fix recommended — converting to a leak-free shape would require a second speaker turn, undermining the deliberate non-dialogue design; leave as documented |
| F5 | 問題2 構成表 (`理由` count) | Minor, pre-acknowledged, documented tradeoff | Only 1 of 6 問題2 items is 理由-framed (official median ~37%). `聴解.md`'s own prose already states this was traded off to fit a required `気持ち` item (6番) while staying at 理由=1/一番=2 (both within their ≤3/≤2 ceilings). `make check`'s own WARN line for this test names exactly this tradeoff. Independently re-verified: the two hard ceilings (`≤2 一番`, `≤3 理由`) are met, and `≥1 気持ち` is met | No fix required — this is a target-vs-gate softness already disclosed in the paper's own audit table, not a rule violation |
| F6 | `logs/topics.json` `voices` map | Pre-existing, out of scope | `make check`: 14 papers including 20260807_1 record no per-surface `voices` map. Shared defect across the whole corpus, not introduced or touched by this repair | Out of scope for a per-test content repair; tracked separately |

---

## Root-cause table (§6.5)

| Finding | Root-cause code | Tests showing this class | Owning file | Proposed edit |
|---|---|---|---|---|
| F1 | `RULE-IGNORED`-adjacent — the `決め手の位置` rule is specific (choukai-items.md §Section item mix, 問題1 row: "no more than 3 of 6 rows may share a position bucket"), and the table's own cell is simply miscounted for one row. Not a rule gap: the author had the rule and the method, and mis-derived one entry | This paper only, checked in this pass; the general failure mode (a self-reported audit cell not re-derived from the actual script) is the same class already named in choukai-items.md for other papers' 消去方法 relabeling incidents, so ≥2 papers show the broader "self-reported table not re-verified" pattern | (no skill change — the rule and method are already specific) | Apply exam-qa-review's own existing instruction: "verify the table against the script, not on trust" before trusting any 構成表's self-reported position/type columns |
| F2 | `RULE-UNENFORCEABLE` — the nine-token `決め手の種類` closed list (choukai-items.md §決め手の種類) has no token for "procedural sequencing" (do A before B), so an item whose true decider is ordering gets mapped onto the nearest available wrong-ish token by construction | This paper's 問題1-2番 only, checked in this pass; `qa-report-20260810_2-choukai-repair.md` F5 documents the same category gap ("no token for procedural next step or personal circumstance") on a different paper — 2 papers now show this class | `question-authoring/references/choukai-items.md` §決め手の種類 | Add a tenth token, e.g. `手順・順序` (procedure/sequencing), or instruct: "if no token fits cleanly, write a short gloss instead of forcing the nearest token" |
| F3, F4, F5 | `RULE-UNENFORCEABLE`/target-vs-gate softness, all three already tracked as residuals in `logs/choukai_remediation_state.json`'s own `P5C2-20260807_1` step note — no new root cause to file; independently re-confirmed present and non-blocking | This paper only for F4 (structural, item-specific); F3/F5 are the same "target vs gate" class the skill already documents generally (choukai-items.md §"Target vs gate") | (no skill change needed — already documented) | n/a |
| F6 | `PIPELINE-GAP`, pre-existing across 14 papers, untouched by this repair by design | 14 papers | `logs/topics.json` / whichever script writes it | Out of scope for this pass; a separate cross-paper fix |

---

## Coverage statement

- **Blind solve**: all 30 scored items + 4 例, from `聴解スクリプト.txt` directly. 34/34 matched
  the printed key.
- **Step 1 (key-by-key proof)**: done for all 34 rows — every OK row above carries the deciding
  quote copied from the script.
- **Step 2 (distractor elimination)**: done for all 30 scored items — every wrong option in
  問題1/2/4/5 was traced to a script line that raises then reassigns/defers/refuses/denies it
  (cross-checked against both the script text and `聴解.md`'s 解説/ポイント cells); 問題3
  distractors are correctly topic-level with zero self-mentions in any of the 6 talks, exempted
  per rule.
- **Step 2.5 (level band)**: 問題4 idioms/expressions (心当たりがない, 折り入って, 板につく,
  〜に決まってる, 気が進まない, めどが立つ, かしこまりました) sit at ordinary N2-conversational
  level; no N1 or sub-N3 flags.
- **Step 3 (mechanical reads, 聴解-relevant only)**: `まず` density inside 問題1 dialogue content
  (excluding instruction lines and the repeated question, which legitimately carry the word)
  checked by direct grep — exactly ONE occurrence in scored dialogue content (問題1-5番's
  announcement), matching `聴解.md`'s own claim precisely. Item-count structure (33 item blocks,
  2 problem-5 lead-ins, closing line) and `script_sha`/`pacing_sha` freshness verified via
  `make check` — no FAILs.
- **Step 4 (聴解 structure)**: `セクション構成表` present and read as columns for all 5 問題.
  正解 uniqueness (no repeated action/object within a 問題): confirmed for all 5 大問. 消去方法
  closed-vocabulary cap (≤2 rows/token, 問題1 only per current scope): confirmed compliant
  (all nine tokens used, none over 2 rows). 決め手の種類 cap (≤2 rows/token, 問題1+2): confirmed
  compliant for both tables. 決め手の位置 spread (≤3/6 in one third): compliant even after F1's
  correction. 質問型 mix: 問題1 まず = 1 of 5 scored (well under the ≤3/6 cap, and the section
  gained the required ≥1 non-dialogue item, 5番); 問題2 一番=2/理由=1/内容・発言=2/気持ち=1, all
  within their respective bounds (F5). 問題3 institutional/person mix (scored items only, 例
  excluded per the paper's own established convention): 2 institutional (3番,5番) / 3 person
  (1番,2番,4番) — meets the ≤2/≥3 target exactly. Probe-carousel (≥3 proposal-deny turns): 0 of 6
  問題1 items. 問題4 register: casual=5/12 (above the 2–4 target band but inside the archive's
  observed max of 6, not gated), keigo=3/12 (within ≤4), already-done distractors=0
  (well under the ≤2 target/≤3 ceiling), あ、-opening keys=2 (at the ≤2 cap, not over). 問題5:
  1番 has 3 distinguishable speaker roles (男1/男2/女) per the required ≥3-speaker structure;
  2番 decides by candidate NAME, never ordinal; the four choices are read in the same
  enumeration order after both 質問1 and 質問2 (confirmed directly in the script).
- **Step 6.5 (root-cause)**: done, table above.
- **`make check`**: run in full. Repo-wide: **1 FAIL** (`詳細解説.json options match the
  booklet`, 46/99 stored options differ from the rewritten booklet) — this is the **expected,
  explicitly out-of-scope** consequence of this repair (the task instructed not to touch
  `詳細解説.json`/`詳細解説.vi.json`/`模範解答.html`; `logs/choukai_remediation_state.json`
  records this as deferred to a future `exam-model-answer` pass, step `P5D-c1-c2-tail`). It does
  not affect the correctness of `聴解.md`/`聴解スクリプト.txt` reviewed here. **All 聴解-relevant
  WARNs for 20260807_1**, adjudicated:
  - short reaction-turn rate 9% (F3) — agree, real but WARN-only and already tracked as a
    residual; not blocking.
  - 問題1/2 closing-turn leaks (3, all 問題1-5番) (F4) — agree, structural consequence of the
    required non-dialogue item, not fixable without removing that item; not blocking.
  - 問題2 理由 count (1 of 6) (F5) — agree, documented tradeoff for the required `気持ち` item,
    both hard ceilings (一番≤2, 理由≤3) met; not blocking.
  - missing `voices` map in `logs/topics.json` (F6) — pre-existing across 14 papers, untouched by
    this repair, out of scope.
  - rotation-cooldown collisions naming 20260807_1's own draws (税務署:確定申告 vs 20260817_1;
    grammar_p7 「〜に基づいて」/「〜に沿って」 vs 20260811_1/20260812_2/20260813_1; grammar_p8
    「〜ばかりに」 vs 20260813_2) — these are findings AGAINST the LATER papers for re-drawing
    inside 20260807_1's cooldown window, not against 20260807_1 itself; confirmed out of scope
    for this review and not actioned.
  - 20260810_1 headline-theme repeat with 20260807_1 (働き方/科学・技術) and 20260810_1's
    聴解問題2-3番 theme repeat (スポーツ・余暇) — both are findings against 20260810_1 (the later
    paper), and the shared themes trace to 20260807_1's untouched 読解 surfaces, not to the
    rewritten 聴解 section; confirmed out of scope.
- **Narration↔voice↔SPEAKER_MAP**: checked every item's gender narration (男の人/女の人/男性係員/
  女性係員/男性担当者/女性店員/etc.) against its script label; no contradictions found. 問題5-1番
  uses 男1:/男2:/女: (3-speaker pitch-split format) per the required structure; 問題5-2番 uses
  男性係員:/夫:/妻:, and `logs/choukai_remediation_state.json`'s `P5C2-20260807_1-reroll`/`D2`
  history records this pairing's margin as 2.94 st (compliant, ≥1.9 st target) — not
  re-measured from raw audio in this pass (see Skips).
- **例 answerability**: all four 例s (問題1=3, 問題2=3, 問題3=2, 問題4=2) checked against both the
  spoken dialogue and the marksheet's pre-marked answer — all match and are answerable from the
  printed/spoken options.

## Skips

- Did not build/read a `qa/20260807_1/keyless.md` render — no `make keyless` target invocation
  was made because this is an explicitly scoped 聴解-only pass and the full-paper keyless render
  would include the out-of-scope 71 Language Knowledge/Reading items; the script text itself
  served the same blind-solve function for the 30 in-scope items + 4 例 (stated per
  exam-qa-review's "state which file you solved from").
- Did not review 文字語彙/文法/読解 (問題1–14 of Language Knowledge & Reading) — explicitly out
  of scope per the task.
- Did not review `詳細解説.json`/`詳細解説.vi.json`/`模範解答.html` — explicitly out of scope per
  the task; the one repo-wide `make check` FAIL belongs to that artifact and is expected/deferred
  to a separate `exam-model-answer` pass per the remediation plan.
- Did not re-listen to the rendered `聴解.mp3` audio or re-measure pitch-separation semitones from
  raw audio (no audio playback tool available in this environment); freshness/pacing/voice-balance
  were taken from `make check`'s own audio-based gates (all `ok`/non-WARN for this test) plus the
  remediation log's own recorded semitone measurement for 問題5-2番's casting, not independently
  re-measured here.
- Did not action the cross-test rotation-cooldown / headline-theme findings that name
  20260807_1 as the EARLIER paper in a collision (see Coverage statement) — those are findings
  against the later papers (20260810_1, 20260811_1, 20260812_2, 20260813_1, 20260813_2,
  20260817_1), not against this test, and are explicitly out of scope for a review of
  20260807_1's own listening rewrite.
- Did not action F6 (missing `voices` map) — pre-existing across 14 papers, a cross-paper
  bookkeeping gap, not a defect introduced or fixable by this test's own content.
