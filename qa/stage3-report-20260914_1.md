# 20260914_1 — stage 3 (build + gate) report

Written by the orchestrator. Provenance: blueprint seed
`48895101` (drawn by `python3 -c "import secrets; print(secrets.randbelow(10**8))"`,
verified unused in `logs/ledger.json` before the draw), plus one reroll-one —
final ledger seed string
`48895101+reroll-one(word_formation:2,57250112)`.

## Stage-2 repair: a sampler defect, caught by an author, repaired at the spec

The 文字・語彙 author reported that `word_formation` had drawn **both**
`〜別(男女別)` (問題3-12) and `別〜(別行動)` (問題3-13). Official prints 問題3
options as bare affixes (N2 7/2025 問題3: `1 則 2 理 3 論 4 規`), so both items
would have printed **`別`** as their key inside one 大問 —
`check_moji_option_reuse` FAIL, and unfixable from the distractor side because
the collision is key-vs-key.

Verified independently by the orchestrator against `test_spec.json`, then
repaired the way `exam-blueprint`/`question-authoring` prescribe — **reroll, never
a hand-substitution**:

```
python3 .agents/exam-blueprint/scripts/sample_items.py \
    --reroll-one word_formation:2 --seed 57250112 --test-id 20260914_1
```

Fresh seed `57250112` from `secrets.randbelow(10**8)`. `別〜(別行動)` out,
`〜版(決定版)` in. 問題3's three keys are now 圏 / 別 / 版.

### ROOT CAUSE — for QA's root-cause table, unfixed at stage 3

`check_spec_blend` fails a **repeated draw** — two identical pool entries. It
cannot see this case, because `〜別(男女別)` and `別〜(別行動)` are two distinct
pool entries whose PRINTED FORM is the same character. The affix position
(prefix vs suffix) is what makes them different entries and is exactly what 問題3
does not print. So the sampler may legally draw a 問題3 set that is guaranteed to
fail a downstream item-integrity check, and nothing at draw time says so.

This one was caught only because an author measured the option set with
`goi_profile.option_reuse` before shipping — i.e. by a human-equivalent read, not
by a gate. Candidate repair (NOT applied here; a gate change at the tail of a
generation run is the defect class `exam-qa-review` §6.5 names): a spec-time check
that strips the `〜`/`〜` affix markers from `word_formation` entries and fails a
paper whose 問題3 draw repeats a bare affix. Filed for QA to rule on.

---

# Stage 3 — build, gate, cross-half re-grep, whole-paper topic pass

Appended by the stage-3 context. Everything above this line was written by the
orchestrator before the build and is unchanged.

## 0. READ THIS FIRST — the 聴解 half of §§1–9 is SUPERSEDED; go to §11

**Every 聴解 number in §§1–9 describes the FIRST composition (seed `45256399`)
and no longer describes the paper.** The listening half was re-composed on
2026-09-14 at seed `91888352`, and two 読解 surfaces (問題12 A/B and 問題11(1))
were re-authored after §§1–9 were written. **§11, appended by the
`logs/topics.json` re-derivation context, carries the current facts** — the
final seed and source mix, the re-run draw audit, what the two repairs changed,
and what `make check` now says. Read §11 first and treat any 聴解 number in
§§1–9 as history.

The original banner said the clip bank would first be expanded from the 10
imported sittings to the full 31-sitting archive; the AMENDMENT in
`qa/replan-20260914_1.md` reversed that, and the re-composition draws from the
**existing 10-sitting bank**. `make mp3` was NOT re-run in the stage-3 context
and the bank was NOT rebuilt.

## 1. What was read, in full, from disk

`AGENTS.md`; `.agents/jlpt-test-generation/SKILL.md`;
`.agents/exam-app/SKILL.md`; `.agents/choukai-audio/SKILL.md` (all 1063 lines,
Part 0 included); `.agents/exam-blueprint/SKILL.md` §"The four theme rules",
§"`key` — the errand identity", §"logs/topics.json" and the authored-theme
section around it; `.agents/question-authoring/references/bunpou.md` §問題9 and
§"問題9's sixteen options have NO pool"; `qa/allocation-20260914_1.md`;
`qa/stage2-handoff-20260914_1.md`; `qa/stage3-report-20260914_1.md` (this file's
head); `qa/replan-20260914_1.md`.

## 2. Merge

`tests/20260914_1/言語知識・読解.md` was written by a mechanical merge of the
three `_sections/` fragments: bodies in booklet order (問1–6, 問7–9, 問10–14),
then ONE `# 解答(言語知識・読解)` heading, then the three key tables in the same
order. The merge script refuses a fragment whose body or key block carries its
own key heading. **Verified after merging**: exactly 1 heading matching
`build_interactive.KEY_HEADING`, 71 bold stems 1–71 with no gap and no
duplicate, 71 key rows 1–71.

## 3. Commands run, in order, with outcome

| # | command | outcome |
|---|---|---|
| 1 | merge script (scratchpad) | 578-line `言語知識・読解.md`, 1 key heading |
| 2 | `make autofix 20260914_1` | no blocking error; 1 WARN `[DOKKAI-ABS-QUANT] 'だけで足りる'` in 問題12-66 option 3 (a distractor that must read as an overstatement — left) |
| 3 | `make lint-draft 20260914_1` | same single WARN, nothing else |
| 4 | `make verify-scramble 20260914_1` | exit 0; all five 問題8 items: keyed ★ survives its junction filter, `ARTIFACT: ok` (per-card last-slot proof present), `FREE UNITS: 1` on each (FAIL is at 2). `RESULT: UNDECIDED` on all five is this tool's normal non-verdict, not a pass — 43 and 47 leave all 24 orderings standing, so their 解説 proofs are the only evidence and QA must read them |
| 5 | `SEED=$(python3 -c "import secrets; print(secrets.randbelow(10**8))")` | **45256399** |
| 6 | `make mp3 20260914_1 SEED=45256399` | 44.3 min, 34 chapters. **PROVISIONAL — see §0** |
| 7 | `make booklet 20260914_1` | both HTML rebuilt, `verify()` clean |
| 8 | `make sheet 20260914_1` | `解答.html` + `練習.html`, 101 items; expected notice that 71 言語知識・読解 items have no 詳細解説 yet (stage 5) |
| 9 | `make check` | 5 FAIL (first run) |
| 10 | `make upload-files TARGET=tests TEST=20260914_1` | `20260914_1.mp3` (42.6 MB) uploaded to release `audio`; `logs/upload_manifest.json` now 47 assets. This was the FIRST composition's MP3; the re-composed one **has since been uploaded too** — see §11.1, nothing is owed |
| 11 | five source repairs (§5) + `make booklet && make sheet` after each | — |
| 12 | `logs/topics.json` row appended | 43 surfaces / 43 themes / 43 claims / 29 shapes / 14 personas / 14 voices — **since re-derived**: 46/46/43/29/14/14 (§11) |
| 13 | `make check` (final) | **2 FAIL**, 217 WARN; 6 WARNs name this test — **superseded by §11.6** |

The mp3 seed came from `secrets.randbelow(10**8)` and is quoted verbatim.

## 4. 聴解 composition — PROVISIONAL (first composition)

- seed `45256399`; 44.3 min; 34 chapters.
- source mix: `official 18, kanzenmoshi 6, soumatome 2, mimikara 1,
  mondaireishuu 1, shinkanzen 1`; drew from 9 sittings (2021-07×5, 2021-12×2,
  2022-07×1, 2023-07×1, 2023-12×2, 2024-07×3, 2024-12×2, 2025-07×1, 2025-12×1).
- The composer printed two notes and **no starvation note for any slot**:
  2 figure items excluded as uncomposable (`2021-12:問題1-5`, `2022-12:問題1-2`),
  and 1 問題3 clip barred by `OPTION_SET_REUSE_MAX` (`mimikara:cd2-14`, 0.57
  against the previous paper's option set).

### Draw audit (first composition) — both bars held

Read from `logs/choukai_draws.json`, not re-derived from the bank:

| bar | result |
|---|---|
| no clip id repeats `20260911_1` **in the same slot** | **none** (0 of 29) |
| no slot-free (textbook) clip repeats `20260911_1` **in ANY slot** | **none** — this paper's 11 slot-free clips and the previous paper's 11 are disjoint |
| section preambles vs `20260911_1` | none repeated |

Two-papers-back (`20260910_1`, outside the bar by design) repeats **3** clips,
and one of them is in the same slot — a minor finding under
`jlpt-test-generation` §"A topic/domain match in the 2-tests-back column":

- `kanzenmoshi:cd1-20` — 問題3-2番 **here and there** (the 留守番電話 忘れ物確認 item)
- `soumatome:cd2-7` — 問題3-4番 here, 問題3-5番 there
- `kanzenmoshi:cd1-36` — 問題4-9番 here, 問題4-2番 there

### A within-大問 finding the composer cannot see (first composition)

**問題3-2番 and 問題3-4番 open on the identical situation line — both are
留守番電話のメッセージ**, two of five items in one 大問. `freshest()` bars clip
ids and `name_clash()` penalises shared personal names; neither looks at the
situation frame, so a 大問 can draw two items with the same opening frame with
every gate green. Root-cause row R1 below. (It may or may not survive the
re-composition; re-check it against the new draw.)

Within-大問 personal-name clash: **none**. 問題1 = 中村/山本/吉田, 問題4 =
佐藤/森/小田, 問題3 = 本田, 問題5 = none. (問題4-6番 is the
`森君が遅刻` clip named in `choukai-audio` Part 0 rule 4; the clip it must not
sit beside is not in this paper.)

## 5. Repairs made at stage 3 — all source edits, each with its rebuild

Every one is a 読解 prose or 解説 edit. **No key, option, answer position, item
or audio was touched.**

| # | where | from → to | why |
|---|---|---|---|
| R-a | 問題10(3) letterhead | `みどり町` → さざなみ町 | `check_invented_proper_nouns` near-name WARN against `20260910_1`'s `みどり市` — a one-character respelling of a recent paper's letterhead is the re-skin that line exists to stop |
| R-b | 問題11(1) first sentence | `私は市役所で` → 私は、市役所で | `check_invented_proper_nouns` **FAIL**: `place_name_candidates()` reads `私は市` as an invented municipality and `20260911_1` contains the same string. A false positive; one 読点 removes it without touching sense or voice. The systemic repair is `PLACE_STOP` — root-cause row R2 |
| R-c | 問題12(B) closing | `場合に限って` → 場合にだけ | **cross-half re-grep hit**: 問題7-35's key is 〜に限って in the 連用 frame, and the shipped 読解 closing used the same form in the same frame, in printed booklet text. 限定条件 skeleton, closing shape and template all unchanged |
| R-d | 問題9 ¶1 and ¶4 | `少し前までは、できあがった…` → 少し前まで、私たちは…；`…手が止まる、という人は少なくない。` → …手が止まる。私もその一人である。 | persona cap: 解説者 sat on 問題9, 問題10(4) and 問題11(4) — 3 against a cap of 2 (`check_topics_claim_field`). A narrator was given to the cloze rather than a tag being re-spelled; it also moves the paper toward the official first-person share |
| R-e | 問題9-50 and 9-51 解説 | leading 「…」 re-ordered so the KEY's form comes first | two **FAIL**s: `check_level_band_grammar` builds its haystack from the keyed option plus the 解説's leading 「…」 gloss, and both rows opened on a passage citation containing `が最後` (N1 ban) and `なければならない` (N3 ban). Category tags, keys and every distractor reason unchanged — root-cause row R3 |

## 6. Gate disposition — `make check`, final run

**2 FAIL, 217 WARN; six WARNs name `20260914_1`.**

### FAIL 1 — `詳細解説.json explains every keyed item (30 entries for 101 keys)`
**Expected and structural at this point in the pipeline.** The 30 聴解 entries
were written by `make mp3`; the 71 言語知識・読解 entries are stage 5's and
authoring them now is prohibited. `20260910_1` and `20260911_1` ended stage 3 in
exactly this state. Clears when stage 5 runs.

### FAIL 2 — `no headline theme repeats 20260911_1's (immediately previous, rule 4)` — **OPEN, escalated**
`['科学・技術']`: this paper's 問題12 (a headline surface) and `20260911_1`'s
問題14 carry it. Not repairable from where stage 3 stands — see §8, finding F1.

### The six WARNs naming this test

| WARN | disposition |
|---|---|
| errand-rotation coverage **1/44 = 2% keyed** | Pool-side gap, not this paper's. The two rotation lines under it are `ok` but silent about 43 draws. **The previous paper is NOT identical**: `20260911_1` prints 2/44 = 5%, `20260910_1` prints 1/44 = 2%. The repair is `key`s in `pools.json` (exam-blueprint §"`key` — the errand identity"), never lowering `ERRAND_COVERAGE_MIN`. Carried, unchanged, to QA |
| 問題8 **form-family tags 1/5 = 20%** | Same class, and here the previous paper *is* identical — `20260911_1` also prints 1/5 = 20%, as do 14 other papers. Hand-maintained map in `pools.json`; carried to QA |
| **読解 lexical load at the current-era ceiling** — novel 17.7% (official 9.5–15.7) | Real, and new: the kanji-word denominator is **271**, the smallest of the last three papers (`20260911_1` 312, `20260910_1` 306), which inflates the novel share. FAIL threshold is 19.3, so it is inside the gate but outside the official band. The stated repair is plainer subject matter — a 読解 re-authoring call, not a stage-3 edit. Handed to QA |
| **読解 lexical load above the current-era FLOOR** — unglossed **4.5/1k** (official 6.3–9.3) | The same measurement from the other side, and the lowest unglossed figure on record (next lowest is `20260911_1` at 6.4). 14 gloss headwords have moved words out of the unglossed column. The two WARNs must be repaired together — plainer subjects AND transparent unglossed compounds put back — which is why neither was attempted here. Handed to QA |
| 問題12: **no representative 「科学・技術」 word occurs in the shipped prose** | True positive on the tag, and the check names this exact shape ("a tag left un-moved because moving it would have exposed a rule-4 headline repeat"). **It cannot be cleared by re-tagging**: 環境 collides with 問題11(2) (rule 3) and 地域活性化 sits in `20260911_1`'s headline set (rule 4 again). Same root as FAIL 2 — see F1 |
| **4 聴解 slots repeat their own theme two papers back** — 3-2番=人間関係, 3-4番=消費・経済 (both `20260910_1`); 2-3番=教育, 2-6番=スポーツ・余暇 (both `20260911_1`) | **PROVISIONAL** (first composition). 2-3番/2-6番 are one paper back on the *theme tag only*, and their subjects are unrelated (地域の日本語教室の実用性 vs 図書館の貸し出し案; 飼い猫を選んだ理由 vs 映画の終わり方). 3-2番/3-4番 two papers back are the same *clips* — see the draw audit. Nothing here is authored, so there is nothing to re-angle; to be re-run against the new draw |

The `pools_sha` WARN lists `20260914_1` only in its "stamped on a REROLL" note —
correct, the spec carries `48895101+reroll-one(word_formation:2,57250112)`, and
its sha `5632b5631716` matches `pools.json` as it stands.

## 7. The cross-half re-grep — 問題7/8/9 keyed forms × the whole 読解 half

Re-derived from disk (keys + option lists parsed out of the merged file), not
from the hand-off table; the hand-off's form/frame column was confirmed row for
row. Scanned: the printed 問題10–14 half (passages, stems, options, （注N）
glosses) and, separately, the 読解 解説 column.

| key | form / frame | hits in printed 読解 | verdict |
|---|---|---|---|
| 31 | 〜ものか / 文末 | 1 — `どのようなものか` (問題59 stem) | interrogative noun + か, not the modal. **Not a hit** |
| 34 | 〜上で / 連用 | 2 — `上の階` (問題11(4)), `十名以上` (問題14) | noun 上 and 以上. **Not a hit** |
| 35 | 〜に限って / 連用 | **1, same frame** — 問題12(B)'s closing | **DEFECT — repaired (R-c)**; 0 after the repair |
| 50 | **〜ずに済む / 文末** | 1 — 問題11(2)-59 option 1, `切られずにすむように` | **連用**, not 文末. Different frame → not a hit under the rule; the gate's own `no 問題9 文末モーダル key is also a 文末モーダル in the 問題10-14 prose` is `ok` on this paper. Recorded rather than repaired because the string sits in a KEYED option and rewriting it would move option-length balance for a non-defect. **QA may overrule** |
| 32, 33, 36–49, 51 | — | 0 | clean |

Re-run after every repair; the table above is the post-repair state.

The 文法 author's own flag — "`せざるを得ない` also appears as a distractor at
問題7-41" — **does not hold on disk**: `せざるを得` occurs exactly once in the
paper, as 問題9-50's option 2. Nothing to act on.

Bonus pass (not required by the brief): the 問題9 cloze block was grepped for
every 問題7/8 keyed form — the only hits are inside 問題9's own option lists.

## 8. The whole-paper topic pass

One table, built from the SHIPPED surfaces. `logs/topics.json`'s new row IS that
table (43 surfaces × theme/claim + 29 shapes + 13 closing moves + 14 voices +
14 personas); this section records the READS and the counts.

### 8.1 Theme column, filled from the shipped surface

All 13 read surfaces ship inside the theme they were drawn with, in spec order
(問題10(1)–(5), 問題11(1)–(4), 問題12, 問題13, 問題14), and 問題9 ships on
デジタル化, the 13th theme the allocation assigned it. Per surface, "is the
shipped subject the one drawn?" — the draws are `{theme, origin: "authored"}`,
so the drawn string IS the theme and the subject was the author's to invent:
**13 of 13 on-theme, 0 stamped `reauthored`**, with ONE qualification —
問題12 ships a subject (住民が川の生き物を数えて送る取り組みと結果の返し方) that
uses no 科学・技術 vocabulary at all, which the gate flags and which §6 covers.

- rule 1 (five headline surfaces, five different themes): デジタル化 / 科学・技術 /
  人間関係 / 旅行・観光 / 消費・経済(聴5-1) / 教育(聴5-2) — **all distinct** ✔
- rule 2 (a 読解 headline theme appears nowhere else in the 読解 half): ✔
- rule 3 (all 13 読解 surfaces differ): **13 distinct themes** ✔.
  Listening is a draw audit, reported not capped (composed half).
- rule 4 one paper back: **BREACHED — 科学・技術** (F1).
  Two papers back: overlap with `20260910_1` is `{デジタル化}` — exactly the one
  repeat the budget allows ✔

### 8.2 The MOVE column, read down the SKELETON

〈通説／自分の想定した X → ところが・ではなかった → 実は Y〉, essay surfaces only,
問題12 A+B as ONE, three-beat rubric (attributed assumption + explicit denial +
実は Y):

- **conservative: 2 of 10** — 問題10(2) (「速さや語数だろうと思っておりました」→
  「返ってきたのは、立つ場所だという答えでした」) and 問題13
  (「長いあいだ、私もそう思っておりました」→「そうとは言えませんでした」). These are
  the two the allocation planned, and no other surface moved onto the skeleton.
- **BORDERLINE-inclusive: 6 of 10** — adding 問題9, 問題10(4), 問題11(1) (two
  candidate variables tested and dropped) and 問題11(3) (a worry the narrator
  held that was not borne out). None of the four attributes the assumption to
  anyone, which is what keeps them off the conservative count.
- Against the official band measured under the same rubric on 9 essay surfaces —
  3/9, 4/9, 4/9 conservative and 6/6/8 BORDERLINE-inclusive, owned by
  `qa-report-20260911_1` §"F3 の根拠" — this paper sits at or below official on
  both instruments. The plan was 2, the accept ceiling 3.
- The gate's own marker-bearing count prints **0 of 13**; that is a different
  instrument on a different denominator and is not the number above.
- Cross-half: no 聴解 item shares a move with a 読解 surface at the cap. The
  nearest is 聴解問題2 as a 大問, whose format IS "candidate raised → denied →
  real reason"; that is the 大問's shape, lifted from real sittings, not an
  authored move.

### 8.3 The TEMPLATE column, read down separately (twice, and again after each repair)

13 finals read. Every NAMED template is used exactly once —
`A だけではない。B こそが〜` (問題10(4)), `A わけではない` (問題11(2)),
`A では/ほど B が多い` (問題11(1)), `〜のは B だ` 分裂文 (問題11(3)) — and the
other nine are 分類外 and pairwise different (理由節「…からである。」/
体言＋「…気づいた。」/ 「…ためだといいます。」/ 依頼で閉じる / 案内文で閉じる /
順序の言い切り「…という順になる。」/ 事実の言い切り / 限定条件「…場合にだけ、成り立つ。」/
「…に応じて変わります。」). **Nothing above 1.** Re-read after R-c and R-d: R-c
kept 問題12(B) on 限定条件 and R-d did not touch 問題9's final sentence, so no
repair pushed a surface onto another surface's template.

not-A-but-B reframe family, counted over the PASSAGE prose (the allocation's
wider marker list, option lines excluded): **3 of 13** — 問題9
(「書類の数よりも、…のほうである」, and a second internal use), 問題10(4)
(「だけではない…こそが」), 問題11(2) (「わけではない」). The plan said 2; 問題9's
close was not counted when the plan was written. 3 of 13 is far under the 6-of-11
that made this a defect class (`20260821_1` F3). The gate's narrower net prints
1 (whole-passage) and 2 (closing).

### 8.4 Closing-shape column

説明 2 ・ 随筆 2 ・ 意外な観察 2 ・ 実用文・分類外 2 ・ 主張 1 ・ 条件提示 2 ・
反論応答 2 = 13, **none over 2**, exactly as planned. No surface carries the same
shape as the same surface of `20260911_1` (the allocation checked this row by
row and the shipped column matches the plan). Against `20260910_1` four slots
share a shape (問題9 説明, 問題10(3)/10(5) 実用文, 問題11(2) 反論応答); the two
実用文 slots are format-bound and no rule reaches two papers back on this axis.

### 8.5 persona and claim columns

`persona`, read down: 職業人 ×2, 解説者 ×2, and eleven singletons. It was
**解説者 ×3 before R-d** — 問題9, 問題10(4), 問題11(4) are all the same faceless
expositor — which is over `PERSONA_CAP`; the cloze was given a narrator rather
than the tag being re-spelled.

`claim`, read down, surfaced the finding the theme column cannot see — F2 below.

### 8.6 読解 × 聴解 read as ONE list

- **Shared decisive detail: none.** `check_surface_subjects`-style equality is
  not the test here; read by hand, no number or condition carries from a 読解
  surface to a 聴解 item. The gate's `問題14 shares no decisive number with any
  聴解 item` is `ok` independently.
- Domain adjacencies, all legitimate under "a 読解 passage may share a domain
  with a 聴解 item, because no one picked the 聴解 item's domain": 問題10(5)
  (値札の書き方) beside 聴解問題2-4番 (商品を値段の順に並べる) — both about making
  prices comparable, no shared detail; 問題14 (川下りの案内) beside 聴解問題1-5番
  (ホテルから美術館へ); 問題11(2) (植樹と手入れ) beside 聴解問題3-5番 (社員の節電).
- The 問題9 cloze against the shipped 聴解問題4 stimuli: no clash. (The drawn
  `quick_response` phrases are not shipped at all — the listening half is
  composed, so those 11 draws reach no surface. Worth knowing when reading the
  errand-coverage WARN.)
- 問題12 (A/B) cross-test column: 科学・技術 here, 働き方 on `20260911_1`,
  デジタル化 on `20260910_1` — one topic per paper, no subject repeat.

### 8.7 Findings

**F1 — rule 4 headline repeat, 科学・技術 (OPEN, gate FAIL, escalated).**
問題12 carries the theme `20260911_1` headlined at 問題14. It is not repairable
by re-tagging (§6) and not by rule 4c's release valve, because the breaching
theme sits on 問題12, not on the cloze. The only honest repair is **re-authoring
問題12 A and B onto a fresh theme**, which is stage-2 work and was not done here
(a build context that authors a surface then audits it breaks both
context-isolation rules). The constraint set for whoever does it:

- theme must be free of this paper's other twelve AND absent from both
  `20260911_1`'s and `20260910_1`'s headline sets → **教育 or 防災, and nothing
  else** (食/働き方/地域活性化/スポーツ・余暇 sit in `20260911_1`'s headline set;
  睡眠・健康 in `20260910_1`'s, whose budget デジタル化 has already spent);
- keep 問題12(A) 意外な観察 + 事実の言い切り and 問題12(B) 条件提示 + 限定条件,
  MOVE 数えたことの報告 counted once, voices 評論/評論, personas 観察者/研究者;
- `answer_positions.問題12 = [1, 2]`; section length 510–600 JP chars;
- the subject must be outside the new theme's `avoid` list;
- the draw must be replaced by `--reroll-one reading_topics:9`, not
  hand-substituted, and the spec + ledger stamped per `exam-blueprint`
  §"Replacing a shipped subject" — and note that a blind reroll has only a 2-in-7
  chance of landing on a non-colliding theme (root-cause row R4).

**F2 — 問題11(1) and 問題13 are one essay written twice (OPEN, no gate sees it).**
Both are a public counter worker of eight-to-ten years who read back their own
multi-year records, rejected the obvious explanation, and found that a short
piece of information handed over the counter before submission was the lever:

| | 問題11(1) | 問題13 |
|---|---|---|
| narrator | 市役所の補助の窓口、八年 | 町の助け合い窓口の取り次ぎ、十年 |
| evidence | 四年分の記録を並べ直した | 十年分の記録を読み返した |
| rejected | 紙の枚数／過去の提出回数 | 気兼ねの強さ |
| lever | 提出前に下書きを五分見せたか | 窓口が所要時間の見当を書き入れる |
| theme | 行政・手続き | 人間関係 |
| persona | 職業人 | 職業人 |

Themes differ, closing shapes differ (条件提示 / 反論応答), subjects differ as
strings — which is exactly the `20260821_1` F4/O1 shape the `claim` column was
added to catch, and it is what the claim column caught. The repair is a re-angle
of one of the two, and 問題11(1) is the cheaper side (問題13 is a headline
surface). Not done here for the same context-isolation reason as F1.

**F3 — 読解 lexical load out of band on both sides (OPEN).** §6; the two WARNs
must be repaired together or the second overshoots into the first.

**F4 — 聴解問題3-2番 and 問題3-4番 share a situation frame (PROVISIONAL).** §4.

## 9. Root-cause rows — for QA to rule on. None applied here

| # | where | what | proposed repair |
|---|---|---|---|
| R1 | `tools/compose_choukai.py` | `freshest()` bars clip IDS and `name_clash()` penalises shared personal names; **nothing looks at the situation frame**, so one 大問 can draw two items that open identically (問題3-2番/問題3-4番, both 留守番電話のメッセージ, this paper). A situation-frame clash is as solvable-by-pattern as a name clash and more visible to a candidate | a per-大問 penalty on a repeated situation-line frame, measured against the archive first (official sittings will show what frame repetition they actually allow inside one 大問) — the same MEASURE-then-choose discipline Part 0 rule 4 applies to the name ban |
| R2 | `tools/check_consistency.py` `PLACE_STOP` | `place_name_candidates()` reads `私は市` out of 「私は市役所で…」 as an invented municipality, and it FAILs whenever two papers both open a passage that way — `20260911_1` and this paper did. It is the same false-positive class every entry already in `PLACE_STOP` records | add `私は市`, `私は町`, `私は村` to `PLACE_STOP`. Cost of not doing it: the next paper that writes 「私は市役所で」 hits the same FAIL and the next agent buys a 読点 instead of fixing the net |
| R3 | `tools/check_consistency.py` `check_level_band_grammar` | the haystack is the keyed option plus **the 解説's leading 「…」 gloss**. `bunpou.md`'s own worked example for a 問題9 row is `[文末モーダル] 前の文の「…はずだった」を受け、…` — i.e. the documented shape opens on a PASSAGE citation, so a quoted passage line gets level-banded as if it were the key. Two FAILs on this paper, both false | for a 問題9 row, prefer the 「…」 span that contains the keyed option's own form; or restrict the haystack to the keyed option for rows whose 解説 opens with a bracket category tag. Do not widen `TOO_HARD`/`TOO_EASY` |
| R4 | `.agents/exam-blueprint/scripts/sample_items.py` `draw_authored_themes` | reading themes are drawn all-distinct and **index 9 always becomes 問題12**, a headline surface — but the draw has no cross-test headline constraint, so a rule-4 breach is drawable and nothing at spec time can see it (`check_theme_spread` "counts the draw, not which entry became which 問題"). This paper is the case: 科学・技術 at index 9, one paper after it headlined `20260911_1`'s 問題14. It also makes `--reroll-one reading_topics:9` a lottery — only 2 of the 7 free themes clear rule 4 here | teach the sampler the fixed surface mapping (indices 9/10/11 → 問題12/13/14, plus the cloze) and exclude, for those indices only, the themes in the previous paper's headline set — and at most one from the paper before that. It is the same `logs/topics.json` lookup `used_subjects_by_theme()` already does |
| R6 | `.agents/exam-blueprint/scripts/sample_items.py` — `main()`, BOTH reroll branches | **FIXED 2026-09-14, found while acting on R4.** `--reroll` and `--reroll-one` each called `draw(rng, pools[cat], …)` unconditionally, so an `AUTHORED_THEME_CATS` category was redrawn from the RETIRED pool — `pools.json` still carries those ~290 subject strings because `check_draw_provenance()` must resolve pre-2026-09-07 draws. `--reroll-one reading_topics:9` on this paper therefore wrote back a LEGACY entry, `{"topic": "教育格差とICT教育の導入効果", "theme": "教育"}`, beside eleven `{theme, origin: "authored", avoid: […]}` siblings: a PRESCRIBED subject with no `origin` and no `avoid`, handed to an author told to treat `origin` as binding and to invent a subject not in `avoid`. Invisible to the gate — `check_spec_blend()` sorts an entry carrying a `topic` into `drawn` (string-duplicate check only) and `check_theme_record_agreement()` joins by institution head, which an authored entry has none of. Latent since 2026-09-07; every reroll between then and now was a grammar/vocabulary category. Secondary: the same path self-redrew the rejected theme **2 of 40** fresh seeds — the authored twin of the 2026-08-19 `ago == 10**9` no-op | **APPLIED.** Both branches route through `draw_authored_themes()`, which gained `kept_themes` (the paper's other picks — `THEME_CAP`, reading 1 / listening 5) and `exclude_themes` (the rejected entry's own theme; self-redraw 2/40 → 0/40), and is handed `prior_history` so a later paper is never recency evidence. `weakest_cooldown()` leaves `rotation.cooldown` alone for a themed reroll (no pool entry, no cooldown), and `carry_legacy()` stops writing `""` into `verified_items`. Verified: full-draw `items`+`answer_positions` identical on 3 seeds, pool-category `--reroll-one` byte-identical on 5 categories × 3 seeds. Written up in `exam-blueprint/SKILL.md` §"`scripts/sample_items.py` — usage" |
| R4-bis | same as R4 — **R4 is now MEASURED, not predicted** | acting on R4 with the repaired sampler: of the **9** themes `THEME_CAP` left free for `reading_topics[9]`, exactly **one** (防災) clears rules 1, 3 and 4 — not the 2-of-7 this table estimated. The estimate counted only the two previous papers' 読解-headline themes; `headline_theme_set()` also carries their **聴解問題5** themes on the PREVIOUS-paper side, and rule 1 bars this paper's own 聴解問題5 themes (教育, 消費・経済) from a 読解 headline. That knocks out 教育 (rule 1, vs 聴解問題5-2番), 地域活性化 + スポーツ・余暇 (rule 4 one-back, `20260911_1`'s 聴解問題5) and 睡眠・健康 (rule 4 two-back WARN, `20260910_1`'s 聴解問題5 — the budget of one is already spent by 問題9/デジタル化). It took **22 fresh seeds** to land 防災, each appended to the spec's seed expression | R4's repair, unchanged — and derive a "free theme" list with `headline_theme_set()`, never by eye from the 読解 headline column. Not applied with R6: teaching the draw the headline constraint moves the FULL draw's RNG stream, which a reroll fix may not |
| R5 | pipeline shape | `check_kaisetsu_item_coverage` has no "stage 5 has not run" state, so **stage 3 can never hand stage 4 an exit-0 gate for a fresh generated paper**, while `exam-qa-review` names a green gate as its entry condition. Three consecutive stage-3 reports have had to write the same paragraph | either give the check a pre-model-answer skip keyed on the absence of `模範解答.html` (the sibling check already skips on exactly that), or write the "1 structural FAIL" exit condition into `jlpt-test-generation` §"Stage 3" so it stops being rediscovered |

## 10. What stage 3 did NOT do, and why

- **`make model-answer`, any `詳細解説*.json` authoring** — stage 5, prohibited
  before QA passes.
- **Re-running `make mp3`, rebuilding the clip bank** — steps 2–3 of
  `qa/replan-20260914_1.md`, another context's.
- **Re-authoring 問題12 (F1) or re-angling 問題11(1)/問題13 (F2)** — stage-2
  authoring; doing it here would make this context both author and auditor.
- **Any script or skill change** — the five root-cause rows above are filed
  instead (`exam-qa-review` §6.5).
- **`git commit`** — nothing was committed.
- **`make sample` for any other test id**, and no other test folder was touched.

---

# 11. Re-composition, repairs and the re-derived `logs/topics.json` row

Appended 2026-09-14 by the row re-derivation context and **re-derived a second
time the same day**, after three further repairs landed: 問題9 got its
first-person narrator (R-d, this time in the fragment), 問題12 A/B were authored
a **third** time onto 教育, and a lexical-load pass touched five surfaces. This
section is written from the SHIPPED bytes
(`tests/20260914_1/言語知識・読解.md`, `_sections/`, `聴解.md`,
`聴解スクリプト.txt`, `test_spec.json`, `logs/choukai_draws.json`) and supersedes
§§4, 6 and 8 wherever they disagree. §§11.1–11.2 describe the listening half,
which none of the three later repairs touched. Nothing here authored or edited
exam content; `make mp3`, `make sample`, `make model-answer` and the bank build
were NOT run.

## 11.1 The final 聴解 composition

| | value |
|---|---|
| command | `make mp3 20260914_1 SEED=91888352` |
| seed | **91888352** — `secrets.randbelow(10**8)`, used verbatim |
| superseded | seed `45256399`, the FIRST composition against the 10-sitting bank |
| source mix | official 18 / kanzenmoshi 6 / shinkanzen 2 / mimikara 1 / mondaireishuu 1 / soumatome 1 = **29 clips** |
| official sittings | **8** — 2021-07×2, 2021-12×2, 2022-07×3, 2022-12×2, 2023-07×1, 2023-12×3, 2024-12×2, 2025-12×3 |

**Re-derived, not quoted.** `compose_choukai.draw()` was re-run read-only in
process with the same seed, the same usage counts and the same `avoid_slot`;
its `clips` and `preambles` are byte-identical to the record in
`logs/choukai_draws.json`. The two composer notes come from that re-run:

1. `2 figure item(s) excluded from the draw (options are picture regions,
   uncomposable): 2021-12:問題1-5, 2022-12:問題1-2`
2. `1 問題3 clip(s) barred — spoken option set repeats the previous paper's
   above 0.30: mimikara:cd2-14 (0.57)`

**No starvation note was printed** — no slot ran out of candidates and had to
drop the previous-paper bar.

The MP3 on disk has already been uploaded: `logs/upload_manifest.json`'s
`audio/20260914_1.mp3` fingerprint (sha256 `bdcad790aaf7…`, 42,505,005 bytes)
matches the file, and `make check`'s `38 exam MP3(s) are on the audio release`
is `ok`. No further `make upload-files` is owed.

## 11.2 Draw audit, re-run against `logs/choukai_draws.json`

| bar | result |
|---|---|
| no clip id repeats `20260911_1` **in the same slot** | **none** (0 of 29) |
| no slot-free (textbook) clip repeats `20260911_1` **in ANY slot** | **none** — the 11 slot-free clips here and the 11 there are disjoint |
| (stronger, measured) any clip repeated at all vs `20260911_1` | **none** — the two papers share zero clip ids |
| section preambles vs `20260911_1` | none repeated (all five from different sittings) |

**Two papers back (`20260910_1`, outside the bar by design):** two textbook
clips recur, neither in the same slot — `kanzenmoshi:cd1-20` (問題3-3番 here,
問題3-2番 there) and `kanzenmoshi:cd1-36` (問題4-9番 here, 問題4-2番 there).
Recorded as the minor finding `jlpt-test-generation` §"A topic/domain match in
the 2-tests-back column" asks for. Note that the FIRST composition also spent
both of these, plus `soumatome:cd2-7`; the re-draw dropped one of the three and
moved both survivors off their two-back slots.

**Within-大問 personal-name clash: none.** 問題1 = 山田/吉田/中山, 問題2 =
中山(+母), 問題3 = no name the bank extracts (問題3-3番's 鈴木 is not picked up),
問題4 = 佐藤/森/小田, 問題5 = 山田(+母). No 大問 shares a name with the same
大問 of `20260911_1` either. **Two names do recur across 大問**: 中山
(問題1-5番 and 問題2-5番) and 山田 (問題1-1番 and 問題5-1番). The rule is
within-大問 only, so this is not a breach — recorded because a candidate hears
the same surname twice.

§4's finding F4 (問題3-2番 and 問題3-4番 both opening as 留守番電話のメッセージ)
**does not survive the re-draw**: this paper has exactly one 留守番電話 item
(問題3-3番). Root-cause row R1 stands on its own merits, but it no longer has a
live case in this paper.


## 11.3 The 読解 repairs, as shipped — 問題12 was authored THREE times

**Updated 2026-09-14 (second pass).** Three more repairs landed after §§11.1–11.2
were written; the row and this section were re-derived from the shipped bytes
again. The 聴解 half was NOT touched by any of them (`聴解.mp3` still carries
`script_sha 707c88cf0f82` and §§11.1–11.2 stand unchanged).

### 問題12 — 科学・技術 → 防災 → 教育

The history matters to the next paper's blueprint stage, so it is recorded whole:

| # | theme | why it was replaced |
|---|---|---|
| 1 | 科学・技術 | rule 4: `20260911_1` headlined it at 問題14 (stage 3's F1) |
| 2 | 防災 | **rule 1, created after the fact**: chosen against the FIRST composition's 聴解問題5 (消費・経済/教育), then the listening half was re-drawn at seed `91888352` and 聴解問題5-2番 became the 市民運動公園 防災フェア (`2021-12:問題5-2`) |
| 3 | **教育** (shipped) | freed by that same re-composition — the first composition's 聴解問題5-2番 had been 教育 |

The entry was re-drawn each time with `--reroll-one reading_topics:9`, never
hand-edited; `test_spec.json` now records **30** such seeds, the landing one
`91824944`. The shipped pair: a twice-weekly evening 学びの場 counting the days
to return written work — **A** three years of its own records (the speed of
re-submission moved half a year before the *number* of re-submitters did),
**B** six learning sites (returning fast changed nothing where only a score was
written; only where one line saying what to fix was added). Finals
`出し直しの速さのほうが先に動いていた。` and `…直す手がかりが紙に書いてある場合にだけ、
成り立つ。`. Closing shapes (意外な観察 / 条件提示), templates (事実の言い切り /
限定条件 — `場合にだけ`, R-c still held), voices (評論/評論), personas
(観察者/研究者) and MOVE (数えたことの報告, A+B as one) are all as the allocation
specified and unchanged from the 防災 version.

**The ordering lesson, which is the real finding and survives the fix:** a 読解
headline theme is chosen against `headline_theme_set()`, which takes this
paper's own 聴解問題5 themes as input — and the 聴解 half can be re-drawn
afterwards. `compose_choukai.py` knows nothing about themes and
`check_topics_themes` cannot measure anything until the topics row is written,
so nothing between those two points can see a theme that a re-composition has
just made illegal. Either fix the composition before choosing (re-choosing) a
読解 headline theme, or re-check the headline set after every re-composition.
This paper paid for the lesson with two extra authorings of 問題12.

### 問題9 — R-d is now on disk, in the FRAGMENT

§11.5's F6 is **closed**. The first-person repair was re-applied to
`tests/20260914_1/_sections/問7-9_文法.md`, so a re-merge cannot drop it again.
The passage carries `わたしの職場では`, `わたしたちは` and
`わたしも、直しを入れる前に`, and the row records what that makes true: voice
一人称随筆, persona 実務者. 解説者 now sits on 問題10(4) and 問題11(4) only —
`records a claim per surface` is `ok`.

Verified from the shipped text rather than taken on report: theme (デジタル化),
closing shape (説明), template (理由節 「…からである。」), MOVE (機構の説明) and
常体 are unchanged; the final sentence is byte-identical; **no denial-frame
marker was introduced** (と思っていた / ではなかった / ところが / 実は all absent
from 問題9), and the skeleton count is still `0 of 13`. The one `よりも` is the
pre-existing one in the final sentence.

**The root cause stays on the record even though the symptom is gone:**
`言語知識・読解.md` is a mechanical merge of `_sections/`, so a stage-3 repair
applied only to the merged file is lost at the next re-merge. Apply repairs to
the fragment.

### 問題11(1) — re-angled, and now also re-worded

Unchanged in substance since §11.3's first version: the 市役所 窓口 professional
became a 市民活動の連絡会 volunteer handling a survey of forty member groups, so
the F2 twin with 問題13 is gone (narrator 世話役/職業人, evidence a one-off survey
of forty other groups / ten years of the narrator's own records, lever role
tenure / a written time estimate). The lexical pass then reworded it (紙 → 書類,
`役が私に回ってきた` → `私が担当することになった`); the subject, claim, closing
shape, template and final sentence did not move. The row's 問題11(1)
`surfaces`/`claim` were re-worded to match the shipped 書類 vocabulary.

### The lexical-load pass (five surfaces + one kana change)

問題12(A), 問題12(B), 問題11(1), 問題13 and 問題11(4) were made plainer, and
問題11(3) took a kana change in the body only (`乾いた物` → 乾いたもの; option 2
still prints `乾いた物`). Re-derived against the row: subjects, claims, closing
shapes, templates, MOVEs, voices and personas all come out the same, and the
finals of 問題11(1), 問題13, 問題11(4) and 問題11(3) are byte-identical to what
the row already recorded.

**One thing did move: 問題11(4)'s （注N） set.** The glosses on 足場 and 下地 were
deleted and replaced one-for-one with glosses on 浮く and はがす. Nothing in the
row cites 問題11(4)'s notes, so no entry went stale — recorded because a reader
counting notes would otherwise be reading a changed passage. The gate is `ok` on
all six （注N） lines and the 読解 total is 32 (official band 27–61).

**Measured after the pass** (`tools/lexical_profile.py` + `make check`, not
carried forward): novel **15.21%** (official current era 9.5–15.7), unglossed
**6.87/1k** (band 6.3–9.3), gloss headwords **8**, kanji density **30.3%**,
median sentence **33.0** JP chars. All three 読解 WARNs §11.6 listed are gone.

### Cross-half re-grep, re-run over the changed prose

No 問題7/8/9 keyed form occurs in the new 問題12 prose, or in the re-worded
問題11(1), at all. Across the whole 読解 half there is still exactly one real
hit — `切られずにすむように` at 問題11(2)-59 option 1, 連用 against 問題9-50's 文末
key, which is not a breach — and the gate's own line is `ok`.

**§7's dismissal of the 文法 author's flag was wrong and is corrected here.**
〜ざるを得ない *does* appear twice as a printed distractor — 問題7-41 option 2
(`休まざるを得ない`) and 問題9-50 option 2 (`せざるを得ない`). §7 grepped
`せざるを得`, which cannot match `休まざるを得ない`. Not a breach: both are
distractors, neither is a key, the cross-half rule is about keyed forms in
問題10–14 prose, and `no 問題7 form printed in more than 2 items' options` is `ok`
at exactly 2. Handed to QA as a judgment call.

### Retired subjects — two retirements for one surface

`logs/topics.json` keeps five `差し替え前:` keys, themes only, no `claim`,
`persona`, `closing_moves` or `voices`, and none matching `READING_SURFACE`:

- `差し替え前:問題11(1)` — 行政・手続き (the 市役所 窓口 essay)
- `差し替え前:問題12(A)-科学・技術`, `差し替え前:問題12(B)-科学・技術`
- `差し替え前:問題12(A)-防災`, `差し替え前:問題12(B)-防災`

問題12 retired twice, so it carries two pairs. Neither is lost to
`used_subjects_by_theme()`, which is the whole point of the convention.

## 11.4 Whole-paper topic pass, re-read after the third round

Read as ONE list (13 読解 + 29 聴解), MOVE and TEMPLATE columns each read down
once, plus "is the shipped subject the one drawn?".

- **Every 読解 surface ships on its drawn theme**, 問題12 included — the gate's
  `問題12: the shipped prose uses a 「教育」 word` is `ok` (学習, 授業 in the prose).
- **Rule 1 — now satisfied.** Headline set: 問題9 デジタル化 / 問題12 教育 /
  問題13 人間関係 / 問題14 旅行・観光 / 聴解問題5-1番 スポーツ・余暇 + 5-2番 防災.
  No 読解 headline theme touches a 聴解問題5 theme.
- **Rule 3** — 13 読解 surfaces, 13 distinct themes: ✔
- **Rule 4** — one paper back `ok`, two papers back `ok`. What remains is the
  composed-half WARN: 聴解問題5-1番 (高校演劇部の衣装, スポーツ・余暇) repeats a
  headline theme of `20260911_1`. Nobody here chose that clip's subject.
- MOVE column: 数えたことの報告 ×2 (問題11(1); 問題12 A+B as one) — as planned.
  〈想定→実は〉 stays at the planned 2 (問題10(2), 問題13); the gate's skeleton
  count prints `0 of 13`.
- TEMPLATE column: 問題11(1) still closes on `A では/ほど B が多い（相関）`,
  問題12(B) still on 限定条件; nothing above one use; the gate's
  "no more than 2 読解 passages close on one sentence template" is `ok`.
- **読解 × 聴解 as one list.** No shared decisive detail. 問題12's move onto 教育
  puts it in the same theme as 聴解問題2-1番 (絵画教室の講師募集) and 聴解問題4-3番
  (漢字のテスト) — legitimate: the listening half is a draw audit, and rule 1
  measures only 読解-headline ∩ 聴解問題5. Also recorded, unchanged: 問題10(3)
  (メールの件名) beside 聴解問題3-5番 (大切な話にメールを使う理由).
- **One within-聴解 echo the composer cannot see** (unchanged): 聴解問題2-5番
  (ビーチコーミング) and 聴解問題3-2番 (海岸清掃) both put beach litter on the
  paper. No shared number or condition; composed half, nothing to re-angle.

### The volunteer-association residual — re-ruled: now TWO surfaces, still ACCEPT

The first version ruled on three surfaces (問題11(1) 市民活動の連絡会, 問題11(2)
木を植える会, 問題12 町内会). **問題12's move to a 学びの場 removes it from the
set**, so the residual is now two. The accept reasons hold unchanged for the
pair — different themes (行政・手続き / 環境), narrators (世話役 / 当事者),
closing shapes (条件提示 / 反論応答) and claims, with no shared decisive detail.

What still goes to QA is the narrower point, and it is the one that was always
the real one: **問題11(1) and 問題11(2) are adjacent surfaces in one 大問 and both
open on a first-person narrator naming the association they belong to** —
`私が担当することになった` and `私は町はずれの斜面` に木を植える会に加わっている.
(The first version quoted `役が私に回ってきた`; the lexical pass removed that
string, and the quote is replaced rather than left standing.) If QA wants it
closed, the repair is the angle of 問題11(1)'s opening sentence, not a re-tag.

## 11.5 Findings F5 and F6 — both CLOSED

- **F5 (rule 1, 防災 on two headline surfaces) — closed** by the third authoring
  of 問題12 onto 教育. The ordering root cause is unfixed and is written up in
  §11.3; it is a pipeline finding for QA, not a defect in this paper.
- **F6 (stage 3's R-d missing from disk) — closed** by re-applying the repair to
  `_sections/問7-9_文法.md`. The root cause (a repair applied to the merged file
  only is lost at the next re-merge) is unfixed and is written up in §11.3.

Nothing else this section opened is still open.

## 11.6 `make check` after the second re-derivation

**1 FAIL, and it is stage 5's.**

| # | line | disposition |
|---|---|---|
| 1 | `20260914_1: 詳細解説.json explains every keyed item (30 entries for 101 keys)` | Stage 5's — the 71 言語知識・読解 entries are not authored yet. Structural at this point; left alone |

Both FAILs the first version opened are gone
(`records a claim per surface` → `ok`, `headline surfaces take five different
themes` → `ok`), and so is stage 3's rule-4 科学・技術 FAIL.

**Three WARNs name this test** (this paper's invariant, not a repo-wide total):

1. errand-key coverage 1/44 = 2% — pool-side gap; `20260911_1` prints 2/44,
   `20260910_1` 1/44. Repair is `key`s in `pools.json`.
2. 問題8 form-family tags 1/5 = 20% — same class; the previous paper is identical.
3. 聴解問題5 repeats a headline theme of `20260911_1` (`スポーツ・余暇`) —
   composed branch of rule 4, WARN by design, nothing re-angleable.

**Five WARNs the first version listed are gone**: both 読解 lexical-load lines and
the median-sentence-length line (the lexical pass), 問題12's missing theme
vocabulary (the theme moved), and — already gone in the first version — the four
聴解 slots repeating a theme two papers back. The `pools_sha` WARN still names
this test only in its "stamped on a REROLL" note; sha `5632b5631716` matches
`pools.json`.

Artifacts are current: `built HTML matches the Markdown it stamps` and
`聴解.mp3 was built from today's 聴解スクリプト.txt (script_sha 707c88cf0f82)` are
both `ok`, so no `make booklet` / `make sheet` was owed or run.
