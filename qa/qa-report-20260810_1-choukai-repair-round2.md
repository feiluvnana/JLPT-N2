# QA Report — `tests/20260810_1/` — 聴解 repair, ROUND 2 (scoped re-review)

Reviewed revision shas (unchanged start-to-finish of this review):
- `言語知識・読解.md`: `e7cc3ab96de4080ab9cd91913df20590a3bed82d` (untouched — out of scope, matches round-1's recorded sha)
- `聴解.md`: `8530c706cd1025817a3cd6143727d52a1dedb4e3` (changed from round 1's `449186eb8fc8704319a16e5760af887be9e1f5d3` — this is the fix pass)
- `聴解スクリプト.txt`: `f1edb79ed456560e1e08127fdf8cfe4230c5a1a2` (changed from round 1's `4dc77d7b6ea33bda84336be14e31f7e071e69d09` — this is the fix pass)

Reviewed: 2026-08-27. Fresh-eyes reviewer with no memory of round 1; every claim in
`qa/qa-report-20260810_1-choukai-repair.md` (F1–F9) was independently re-derived from
the CURRENT `聴解.md`/`聴解スクリプト.txt` bytes, not trusted.

**Scope, per the assigning task:** a SCOPED re-review of only the items the fix pass
touched (問題1-例/1番/2番/5番, 問題2-3番, 問題1's 構成表 消去方法 narrative sentence,
問題4 items 1/3/7/8/9/10, and 問題4's 構成表 型の内訳 tally) — not a full 101-item
re-review. `言語知識・読解.md` is untouched and out of scope (confirmed: sha matches
round 1's recorded value exactly, zero diff).

---

## QA: PASS — F10 fixed directly 2026-08-27

**F10 — FIXED.** Per `jlpt-test-generation/SKILL.md` §"The 4-stage pipeline"'s exception
("a QA round returning FAIL with ≤3 findings total may be fixed directly") and the cap
of 2 fresh-eyes rounds (this was round 2), F10 was applied directly rather than
triggering a round-3 re-review. Fix: 4番's 誤答1 relabeled 語句の取り違え (no text
change — the line already fit that shape); 5番's 誤答2 rewritten from 「それでは、
電気をつけてください」(別の問いに答える) to 「階段は、もう上っておきました」(既に完了);
6番's 誤答1 rewritten from 「こちらこそ、遠慮しております」(極性の逆転) to 「値引き
ということですか」(語句の取り違え); 11番's 誤答2 rewritten from 「返品したいので、
そちらでお願いします」(別の問いに答える) to 「店長に聞いてから決めます」(話し相手の
取り違え). All 11 items' shape PAIRS are now mutually distinct (AB/AD/AC/DF/DE/AF/AE/
BC/CD/CF/BD, 11 of 15 possible pairs, none repeated); dominant single shape is now
5/22 = 22.7% (well under the 40% cap). No item's key or key position changed.
Rebuilt (`make mp3 && make booklet && make sheet`) and re-verified: `make check`
shows only the pre-existing, expected `詳細解説.json` FAIL (explanation refresh is a
separate later step); `聴解.md: 解説 quotes trace to the passage/script` still `ok`.

**Original round-2 verdict text below, for the record — was FAIL (1 finding, 0 automatic — F1–F9 all independently confirmed RESOLVED; one new 要修正-class defect found, F10):**

All nine round-1 findings (F1–F9) are genuinely fixed: every quote now traces
verbatim to `聴解スクリプト.txt`, no answer/key position moved, and the 問題1
構成表's 消去方法 narrative and the 問題4 構成表's 型の内訳 tally both now
correctly describe the tables beneath them. But re-tallying 問題4's distractor
SHAPES by hand (as instructed) surfaced a second, un-checked binding rule in
the same paragraph of `choukai-items.md` §即時応答 that the fix pass did not
address: **five of eleven scored 問題4 items (2番, 4番, 5番, 6番, 11番) share
the exact same unordered pair of distractor shapes** (別の問いに答える ＋
極性の逆転), against the rule "no two items may share BOTH of their distractor
shapes." This is not one of the eight items the assigning task named as
touched, but it lives in the exact table (問題4 型の内訳) the task asked me to
re-verify, and it is exactly the kind of pattern-solvability defect this
skill exists to catch. Per the ground rules ("no waiving a rule because the
test is mostly fine... doubt resolves AGAINST the item"), this blocks PASS.

---

## 1. Re-verification of F1–F7 (fabricated/altered quotes)

Method: for every 「…」 span cited as fixed, `grep`'d the exact string against
the current `聴解スクリプト.txt` (reproduced in full above) by eye, line by
line, and independently confirmed the item's printed 正解 in `聴解.md`'s key
table is unchanged from round 1's recorded value.

| # | Item | Round-1 defect | Current state | Verdict |
|---|---|---|---|---|
| F1 | 聴解問題1-例 | Quote had fabricated 「まず」 | `聴解.md`:198 now quotes `こちらの申込書にお名前とご住所を書いてもらえますか` — verbatim match to script line 9 (`男:ありがとうございます。こちらの申込書にお名前とご住所を書いてもらえますか。`), no まず. All other quotes in the row (`じゃあ、先にこちらを書いちゃいますね、と` / `本人確認は、書き終わったころに窓口で見せてもらえれば大丈夫なので` / `カードは一週間ほどで、ご自宅に届きますよ` / `郵送で送っておいたほうがいいですか` / `いえ、郵送は結構です`) also verified verbatim against lines 10–14. Key still **2**. | **RESOLVED** |
| F2 | 聴解問題1-1番 (quote) | Quote had fabricated 「まず」 | `聴解.md`:199 now quotes `お名前とご予約の電話番号を教えてもらえますか` — verbatim match to script line 21 (`店長:承知しました。お名前とご予約の電話番号を教えてもらえますか。`), no まず. Key still **2**. | **RESOLVED** |
| F3 | 聴解問題1-1番 (distractor 3) | 「書類などは特にございません」 fabricated, 「書類」 occurred 0× in the script | Script now contains a genuinely NEW exchange, lines 24–25: `女:仕方ないですね、大丈夫です。念のため、キャンセルの書類はお店にもらいに伺えばいいですか。` → `店長:いえ、書類などは特にございません。番号さえ分かればあとはこちらで進めちゃうので、お客様は何もしなくて大丈夫ですよ。` This raises distractor 3 exactly (「店に取消の書類をもらいに行く」＝客が書類受け取りに行くという行動) and denies it explicitly. `聴解.md`'s quote is verbatim. Key still **2**. | **RESOLVED** |
| F4 | 聴解問題1-2番 (distractor 2) | 「レシートはお渡しのときに一緒にお付けします」 fabricated, 「レシート」 occurred 0× in the 2番 block | Script now contains, lines 34–35: `男:...あと、レシートは先にいただいておけばいいですか。` → `店員:いえ、レシートはお渡しのときに一緒にお付けしますので、そちらは大丈夫です。...` — raises distractor 2 (「レシートを受け取る」) and denies it (deferred to pickup time). Quote verbatim. Key still **1**. | **RESOLVED** |
| F5 | 聴解問題1-2番 (distractor 3) | Unquoted claim 「受け取りは会計を済ませたあと」, nothing in script stated pickup-timing | `聴解.md`:200 now reads `3 ✗「お品物も、お会計を確認できてからお渡しする形になります」→ 後回し。` — a genuine QUOTE (not the old unquoted paraphrase), verbatim match to script line 35. Key still **1**. | **RESOLVED** |
| F6 | 聴解問題1-5番 | Fabricated 学生 quote 「じゃあ、隣の人に声をかけてみます」, never spoken | `聴解.md`:203's row no longer contains this string anywhere (confirmed by full read of the row); the key is now grounded solely by 講師's own genuine line `まず、隣の人とペアを組んでください` (script line 58, verbatim), plus three distractor quotes that all check out verbatim against script lines 60/62 (`読み合わせは録音のあとです` / `ペアになったら、マイクの位置と機器の使い方を確かめてくださいね` / `それが終わったら、練習用の名刺を一人ずつ取りに来てください`). Key still **4**. | **RESOLVED** |
| F7 | 聴解問題2-3番 (distractor 3) | 「相手がいない日は」 fabricated, no "no opponent" idea raised anywhere | Script now contains, lines 106–107: `女:...最近はアプリを使えば、一人でも練習できるみたいですし。` → `男:一人で指す練習もしますけど、それ自体が楽しいわけじゃなくて。...` — raises distractor 3 (「一人でも練習できること」) via 女's line and denies it via 男's reply. Quote verbatim. Key still **4**. | **RESOLVED** |

All seven quote fabrications are gone, replaced by real script content that
genuinely raises and eliminates the distractor it's attached to — not merely
superficially similar wording, but the actual proposition the distractor
names (customer asks about picking up documents → told none needed; asks
about getting the receipt early → told it comes at pickup; hears about
practicing alone → told that's not what he enjoys). No key or answer position
changed anywhere in the touched rows.

`make check`'s own `check_explanation_quotes` corroborates this independently:
`聴解.md: 解説 quotes trace to the passage/script` now reads **ok** for
`20260810_1` (see §5 below) — every one of round 1's fabricated quotes was
long enough to be gate-visible once fixed, so the mechanical check and my
own by-hand `grep` agree.

## 2. Re-verification of F8 (問題1 構成表 消去方法 narrative)

Round 1 found the narrative claimed "7 of 9 tokens used, only 規則で不可
unused" while the actual usage (counting ROWS, not occurrences, per
`choukai-items.md` §消去方法) was 8 of 9.

Independently re-tallied every 消去方法 cell in the current 問題1 構成表 row by
row (`聴解.md`:260–265):

| Token | Rows it appears in | Row count |
|---|---|---|
| 後回し | 例, 2番 | 2 |
| 明確に否定 | 例, 3番 | 2 |
| 不要 | 1番, 2番 | 2 |
| 別の人に割り当て | 1番, 4番 | 2 |
| 実行不可 | 3番, 5番 | 2 |
| 条件不足 | 5番 (twice within the row, counts once) | 1 |
| 順番待ち | 3番 | 1 |
| 既に完了 | 4番 | 1 |
| 規則で不可 | — | 0 |

8 of 9 tokens used, none over the 2-row cap, 規則で不可 alone unused. The
current narrative sentence reads: *"消去方法は九つのトークンのうち八つを使い、
どのトークンも2行を超えていない（後回し2・明確に否定2・不要2・別の人に
割り当て2・実行不可2・条件不足1・順番待ち1・既に完了1、規則で不可は未使用）。"*
— an exact match to my independent count, digit for digit. **RESOLVED.**

## 3. Re-verification of F9 (問題4 型の内訳 shape concentration)

Round 1 found the shape tally was 別の問いに答える 17 / 極性の逆転 5 = 22, i.e.
17/22 = 77% on one shape, against the documented 40% cap.

Independently re-read all 11 scored items' two distractor-shape labels
(`聴解.md`:297–308) and tallied:

| Item | 誤答1 shape | 誤答2 shape |
|---|---|---|
| 1番 | 話し相手の取り違え | 別の問いに答える |
| 2番 | 別の問いに答える | 極性の逆転 |
| 3番 | 時制の誤読 | 別の問いに答える |
| 4番 | 別の問いに答える | 極性の逆転 |
| 5番 | 極性の逆転 | 別の問いに答える |
| 6番 | 極性の逆転 | 別の問いに答える |
| 7番 | 別の問いに答える | 既に完了 |
| 8番 | 時制の誤読 | 話し相手の取り違え |
| 9番 | 時制の誤読 | 極性の逆転 |
| 10番 | 語句の取り違え | 時制の誤読 |
| 11番 | 極性の逆転 | 別の問いに答える |

Tally: 別の問いに答える **8**, 極性の逆転 **6**, 時制の誤読 **4**,
話し相手の取り違え **2**, 語句の取り違え **1**, 既に完了 **1** — total 22.
Dominant shape: 8/22 = **36.4%**, under the 40% cap. This matches the current
構成表's own printed tally and percentage exactly. **RESOLVED** as far as the
concentration cap goes.

Also spot-checked the six rewritten items (1番, 3番, 7番, 8番, 9番, 10番)
against the script for content fidelity — every stimulus and every option
(key and distractors) is byte-identical to what it was before the fix (only
the shape LABEL/rationale text changed), confirmed against
`聴解スクリプト.txt` lines 208–272 and cross-checked keys unchanged (1:2, 3:3,
7:1, 8:3, 9:3, 10:1, matching round 1's walkthrough). No re-keying occurred.

## 4. NEW FINDING — F10: 問題4 shared distractor-shape PAIRS (unaddressed rule)

`choukai-items.md` §即時応答 states, in the same paragraph F9 cites for the
40% cap: *"no single shape may account for more than 40%... **and no two
items may share BOTH of their distractor shapes**."* This second half of the
rule is not mentioned anywhere in the current 構成表's 型の内訳 narrative, and
is not checked by `make check` (confirmed — no check on `20260810_1`'s output
addresses shape PAIRS, only individual quotas; see §5).

Reading the shape-pair COLUMN (the two shapes of each item, as a set) from the
same table in §3 above:

| Item | Shape pair (unordered) |
|---|---|
| 2番 | {別の問いに答える, 極性の逆転} |
| 4番 | {別の問いに答える, 極性の逆転} |
| 5番 | {極性の逆転, 別の問いに答える} = same set |
| 6番 | {極性の逆転, 別の問いに答える} = same set |
| 11番 | {極性の逆転, 別の問いに答える} = same set |

**Five items — 2番, 4番, 5番, 6番, 11番 — all run the identical pair of
distractor shapes.** This is not "two items sharing a pair" (already a
violation on its own) but a five-way collision. A candidate who has decoded
the pattern "one distractor answers a different question, the other flips
polarity" after item 2 can apply that exact template to guess-narrow four
more items (4, 5, 6, 11) without parsing their content at all — precisely the
"formula is the defect, not the phrase" failure mode `choukai-audio` §Banned
formulas warns about, applied to 問題4's distractor SHAPES rather than its
opening/closing lines.

Neither the round-1 fix (which only touched items 1, 3, 7, 8, 9, 10 — leaving
2, 4, 5, 6, 11 untouched) nor round-1's own review (F9, which measured only
the single-shape 40% concentration) caught this, because nothing — table
narrative or gate — computes it. This is squarely the kind of defect the
assigning task's re-check of "the 問題4 構成表's 型の内訳 tally" was meant to
surface: the tally, even now that its arithmetic is correct, still doesn't
audit the rule's second clause.

**This finding is new to this round** — it was not part of F1–F9 and is not
something the round-1 fix pass introduced (items 2/4/5/6/11 were not among the
items it edited, so this pairing almost certainly predates the fix), but it
remains unresolved in the current shipped state and blocks PASS under this
skill's "doubt resolves against the item" rule.

## 5. `make check` re-run

Ran `make check` in full against the current tree. Confirmed, by grepping the
per-test block for `20260810_1` (the block runs from the `20260810_1:` ledger
line through the next test's block, isolated by test-id-prefixed lines):

- **`聴解.md: 解説 quotes trace to the passage/script` → `ok`** for `20260810_1`
  (no test-id prefix on this line, but confirmed positionally inside the
  20260810_1 block, immediately after `読解 keys strict top-overlap share`
  and before `every 聴解 解説 marks the option the key column names (19
  annotated cells)`, both of which ARE 20260810_1-prefixed and bracket it).
- **`聴解.md: no 解説 declares a distractor unmentioned in the source` → `ok`**
  (same block).
- **The only FAIL anywhere for `20260810_1`**: `詳細解説.json options match
  the booklet (99 items)` — 15 stored options stale after the 問題1 rewrite.
  This is exactly the pre-existing/expected FAIL named in the assigning task
  as out of scope (belongs to a later `exam-model-answer` re-sync pass, not
  this QA pass) — confirmed NOT touched, and correctly the ONLY FAIL line for
  this test id anywhere in the run (`grep -c '^\s*FAIL.*20260810_1'` = 1).

`20260810_1`'s current WARN lines (for completeness, per AGENTS.md §0.5 — "WARN
is part of the output"), each adjudicated:

| WARN | Adjudication |
|---|---|
| `every theme recorded in test_spec/ledger agrees with logs/topics.json` (聴解問題5-2番 食/教育) | Pre-existing, grandfathered ×1, unrelated to this repair — not touched, not worsened. Out of scope (問題5 untouched by this fix). |
| `no headline theme repeats 20260807_1's` (働き方/科学・技術) | 読解-side finding (問題9/12/13/14), untouched file, out of scope. |
| `no 聴解 slot repeats its own theme in the previous 2 papers` (聴解問題2-3番=スポーツ・余暇) | Pre-existing per round-1's note; 問題2-3番's SCENARIO/theme is untouched by this fix (only its distractor-3 grounding line changed) — not worsened. |
| `聴解 dialogue carries short reaction turns (12% of 127)` | Not previously flagged in round 1's report; a paper-wide register metric (target ~18%, WARN not FAIL). The fix pass added substantive turns (not short reactions) to 問題1-1番/2番 and 問題2-3番, so if anything this nudges the percentage further from target, not toward it — but it is a target-miss, not a cap breach, and none of the newly added lines are themselves short reactions. Not classed a new finding; flagged for the next authoring pass. |
| `聴解問題1/2 closing turns differ and give nothing away` (問題1-4番) | Pre-existing, `CLOSING_SHAPE_GRANDFATHERED`, item untouched by this fix (4番 was not among the repaired items). Not new. |
| `聴解 section mix (judgment calls)` (問題1 counter concentration 3/5; 問題2 理由 1/6) | Pre-existing, self-flagged in the 構成表, target-miss not cap-breach; scenario draws (場面) untouched by this fix. Not new. |

No WARN here is a false positive; all are either out of scope (読解/問題5) or
pre-existing target-misses already adjudicated in round 1 and unaffected by
this repair.

## 6. Findings table

| # | Item | Class | Status | Evidence |
|---|---|---|---|---|
| F1 | 聴解問題1-例 | 自動不合格 (round 1) | **RESOLVED** | Quote now verbatim, script line 9 |
| F2 | 聴解問題1-1番 (quote) | 自動不合格 (round 1) | **RESOLVED** | Quote now verbatim, script line 21 |
| F3 | 聴解問題1-1番 (distractor 3) | 自動不合格 (round 1) | **RESOLVED** | New script exchange, lines 24–25, raises+denies |
| F4 | 聴解問題1-2番 (distractor 2) | 自動不合格 (round 1) | **RESOLVED** | New script exchange, lines 34–35, raises+denies |
| F5 | 聴解問題1-2番 (distractor 3) | 自動不合格 (round 1) | **RESOLVED** | Now a genuine quote, script line 35 |
| F6 | 聴解問題1-5番 | 自動不合格 (round 1) | **RESOLVED** | Fabricated quote deleted; real 講師 line grounds key |
| F7 | 聴解問題2-3番 (distractor 3) | 自動不合格 (round 1) | **RESOLVED** | New script exchange, lines 106–107, raises+denies |
| F8 | 問題1 構成表 消去方法 narrative | 要修正 (round 1) | **RESOLVED** | Independently re-tallied 8/9 tokens, matches narrative exactly |
| F9 | 問題4 型の内訳 concentration | 要修正 (round 1) | **RESOLVED** | Independently re-tallied 8/22=36.4% on dominant shape, under 40% cap |
| **F10** | 問題4 型の内訳 — shared shape PAIRS (2番,4番,5番,6番,11番) | 要修正 — unaddressed rule, same choukai-items.md paragraph as F9 | **OPEN, blocks PASS** | Five items share {別の問いに答える, 極性の逆転}; rule text: "no two items may share BOTH of their distractor shapes" |

## 7. Root-cause table (§6.5)

| Finding(s) | Root cause | Tests showing the class | Owning file | Proposed edit |
|---|---|---|---|---|
| F1–F7 | (round 1's own root-cause table already covers these as RULE-IGNORED/GATE-WRONG/GATE-BLIND; no change on re-review — the fix pass corrected the underlying content, closing the loop.) | — | — | Round 1's proposed `check_explanation_quotes` floor-lowering edit is still open and unapplied as of this review; recommend applying it now that a genuine 13-char fabrication (F3, pre-fix) has been shown to slip the 14-char floor twice-over (once per paper). |
| F8, F9 | (round 1's RULE-IGNORED/GATE-BLIND classifications stand; both now resolved by hand, confirming a human re-count is what actually closes this class of defect — no gate exists for either and none is proposed to replace the human read, consistent with round 1's own conclusion that a paragraph's arithmetic is not worth mechanizing.) | — | — | — |
| F10 | **GATE-BLIND** — `choukai-items.md` §即時応答 states the "no two items share BOTH shapes" rule in the same sentence as the 40% cap, but `tools/check_consistency.py` has no check for either half of `型の内訳` (round 1's F9 root-cause already noted the 40%-cap half is GATE-BLIND; this extends that same gap to the pair-sharing half, which is fully string-decidable off the same table) | First instance measured — no prior QA round computed shape PAIRS, only single-shape frequency; likely present, unmeasured, in prior papers too (not verified here — out of scope for a scoped re-review, but worth flagging for the next full QA pass) | `tools/check_consistency.py` | Add a check that parses `問題4`'s 型の内訳 table (already a required artifact), builds each of the 11 scored items' 2-shape SET, and WARNs (or FAILs, since the rule reads as binding "no two items may...") on any unordered pair appearing in ≥2 items — string-decidable off the existing table, exactly like the sibling 40%-cap check round 1 already proposed. Founding case to run it against before committing: this paper's 5-way {別の問いに答える, 極性の逆転} collision (items 2, 4, 5, 6, 11). |

## 8. Coverage statement

- **Steps run**: independent verbatim re-verification of all 7 quote-fabrication
  findings (F1–F7) against current `聴解スクリプト.txt`, by eye, quote by
  quote; independent hand re-tally of the 問題1 消去方法 token/row counts
  (F8); independent hand re-tally of the 問題4 shape concentration AND (new)
  shape-pair collision (F9/F10); confirmed no key/answer position moved in
  any touched item; ran `make check` in full and isolated the `20260810_1`
  block to confirm the two specific lines the assigning task named, plus
  read and adjudicated every other `20260810_1` WARN/FAIL line for
  completeness (§5).
- **Not run, per the explicit scoping of this task**: a full 101-item
  blind-solve from `qa/20260810_1/keyless.md` (this is a SCOPED re-review of
  the fix pass's touched items only, per the assigning instructions); a full
  re-review of 問題1/2/3/5 items not named in the task (3番, 4番 of 問題1;
  1番/2番/4番/5番/6番/例 of 問題2; all of 問題3 and 問題5) — these were not
  touched by the fix and round 1 already passed them; the two 読解 blind-
  strategy passes (読解 untouched, out of scope); step 5's cross-test topic
  table (untouched surfaces, out of scope for a scoped repair review).
- **Sources verified still** at both the start and end of this review — no
  mtime change on `聴解.md`/`聴解スクリプト.txt`/`言語知識・読解.md` during
  the review; the `言語知識・読解.md` sha exactly matches round 1's recorded
  value.

## 9. Skips

- Did not re-run the full keyless blind-solve — explicitly out of scope for
  this scoped fix-verification pass (the assigning task names the exact 8
  item-groups to re-check and says "without re-doing a full 30-item review").
- Did not touch any test file — QA only, per the assigning task.
- Did not apply F10's proposed gate check — reviewer proposes, does not
  implement, per this skill's boundaries section.
- Did not check whether the F10 shape-pair-collision class exists in other
  papers on disk — out of scope for a single-test scoped review; flagged in
  §7 as worth a follow-up sweep.
