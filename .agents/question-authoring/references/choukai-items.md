# 聴解 items — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — sniff test, item integrity (the 解説 verbatim-quote rule
and the 即時応答 keigo-direction rule are #19–20 there). Script FILE format and
audio pacing are owned by `choukai-audio`; booklet printing conventions
(問題5-2番 labels, instruction wording, 例 mechanics) by `jlpt-exam-structure`.

## Write the SECTION TABLE, then read its COLUMNS — required artifact

Every 聴解 defect that cleared a green gate AND a fresh-eyes QA was a
**section-level repeat**, invisible item by item (`20260813_2` keyed the same
action in both 問題1-1番 and 2番 via the same interrupting line — two clean
items, one duplicate answer). A section is not finished when its items are
written. Append to `聴解.md`, **after the answer-key heading** (so
`strip_key()` keeps it out of `解答.html`), one table per 問題:

```
## セクション構成表（作問監査用）
### 問題1
| 項目 | 場面 | 主導 | 正解 | 消去方法 | 質問型 | 決め手の位置 | 提案消去回数 | 決め手の種類 |
|---|---|---|---|---|---|---|---|---|
| 1番 | スーパーのレジ | 店員→客 | 本人確認書類を提示 | 順番待ち（先に会員登録）／不要／実行不可 | どう直す・方法 | 冒頭（3行目／全11行） | 1 | 規則・制度 |
| 2番 | 会社の朝会 | 部長→部下 | 見積書を送る | 別の人に割り当て／既に完了／条件不足 | この後まず | 中盤（6行目／全12行） | 0 | 人手・担当 |
```

Then read it **as columns, not as rows**:

- **正解** — no two rows may name the same action or object.
- **消去方法** — no device more than twice (§"Eliminated ≠ contradicted").
- **場面 / 主導 / 質問型** — against the quotas below (≤3/6 まず, ≥1 modify, ≥1 condition).
- **決め手の位置** — 冒頭 / 中盤 / 終盤 (no more than 3 of 6 rows in any one third).
  位置は *決め手の発話の行番号 ÷ その項目の総発話行数* を三等分して決める
  （≤1/3=冒頭、≤2/3=中盤、それ以外=終盤）。非対話項目は発話行の代わりに文を数える。
  構成表には *n行目／全m行* を必ず併記し、m は台本の発話行だけを数える
  （質問行・場面説明行は含めない）。See §"決め手の位置 — the formula, and the
  denominator it is measured over" below.
- **提案消去回数** — turns with proposals (≤2 items with ≥3 proposals).
- **決め手の種類** — no token more than twice per section (§"決め手の種類").

If a column repeats, rewrite the ITEM, not the table. QA reads this table first
(`exam-qa-review` §4 聴解); a section with no table is not shippable.

### 場面 — one establishment type per 大問

**No two items of one 問題 may sit at the same KIND of counter**, 例 counted.
`20260817_3` 問題2 opened its 例 at 「ビジネスホテルのフロント」 and set 5番 at
「ホステルの受付」: a listener hears the same errand twice in one section, and
every automated gate was green — both entries are tagged 旅行 (theme caps pass),
their errand keys differ (cooldown passes), and `sample_items.py`'s
domain-collision WARN compares the literal prefix, for which 「ホテル」 and
「ホステル」 are two domains. Nothing upstream can catch it: the sampler draws all
21 `listening_scenarios` without knowing which 大問 each will land in — **you do
that mapping, so it is yours to check.** Synonyms count as one type
(ホテル/旅館/ホステル/民宿, 病院/クリニック, 美容院/理髪店, レストラン/カフェ/食堂,
市役所/区役所 …); different establishments of a broad domain do not
(大学の研究室 vs 専門学校の事務室 is fine, and so is 郵便局の窓口 vs
ハローワークの窓口 inside 問題1's ≤2 サービスカウンター quota).

Fix a collision by **placing the two scenes in different 大問, or re-angling one
onto another establishment** — never with `--reroll listening_scenarios`, which
re-draws all 21 entries to repair one placement you control.

`check_choukai_setting_adjacency()` reads this column and FAILs a repeat —
**except for the papers named in its `SETTING_ADJACENCY_GRANDFATHERED` set,
which print the same measurement as a WARN.** That set holds the papers that
already breached the rule the day the check landed (2026-08-19); clearing one
means re-writing a 場面 and re-synthesising its MP3, i.e. a decision about that
paper, and an id leaves the set the moment that paper's 聴解 is repaired.
**Read the set in `tools/check_consistency.py`, not this sentence, for who is
currently exempt** — as of 2026-08-19 it is `20260817_3` alone (問題2 例
ビジネスホテルのフロント / 5番 ホステルの受付, the incident above), pending the
re-angle of its 例.

This paragraph exists because the rule and the gate disagreed for one day: §場面
said the check "fails on a repeat" while the only paper that repeats was
exempted by name, so the section read as enforced and measured as advisory
(round 3, R3-4). **A doc that says "fails" beside a gate that warns is worse
than either — it is the shape where green stops being evidence.** Any exemption
the gate carries is named here, the way §消去方法 names its four.

**主導 — 同じ主導の組は1大問に2行まで。** 同じ主導の組（部長→部下・店長→アルバイト・
先生→学生・係員→客…）は1大問に2行まで。仕事を割り当てる型の下限（≥3）を満たすために
同じ組を繰り返してはならない——場面・用件・決め手の軸が違っても、受験者は同じ力関係の
指示を二度聞かされる。

The 場面 rule above caps the establishment and the 「≥3 must be someone
assigning work」 quota (§"Section item mix") is a **floor only**, so until this
paragraph existed nothing capped the pair itself, and two papers answered the
floor by repeating one pair: `20260903_1` 問題1 runs 店長→アルバイト in both 1番
and 3番 (1番 衣料品店の売り場, 3番 an unnamed shop by phone — different errand,
medium and 決め手 axis, which is exactly why no other column saw it), and
`20260828_1` runs 客→職員 / 職員→患者 / 職員→住民（理事） as three staff-to-customer
問題1 rows that only synonymy separates, with 客→店員 printed twice outright in
its 問題2. Two papers is systemic by definition
(`qa-report-20260903_1-round2.md` N2/S3).

Fix a third row by re-casting who drives it (a peer, a subordinate asking up, a
non-dialogue medium), never by re-labelling the same pair with a synonym —
店長→店員 and 店長→アルバイト are one pair to a listener.
`check_choukai_leader_pairs()` mirrors this as a ≤2-rows-per-pair tally over the
問題1 表, beside the §消去方法 tally, and counts **normalised cell strings**: a
synonym pair reads as two different pairs to the gate and stays QA's to read as
a column (`exam-qa-review` §4).

### 消去方法 uses a CLOSED vocabulary — mandatory

Free text in this column is how a device count comes out wrong: `20260817_3`
wrote 「順番待ち／順序が逆」, 「登録後に係員」 and 「第三者に割り当て」 in one
問題1, and its own tally then read four reassignments as two — the over-cap
shipped and QA found it, not the author. **Every 消去方法 cell is one token per
distractor, in the item's option order, each token EXACTLY one of these nine,
verbatim:**

`既に完了` · `別の人に割り当て` · `順番待ち` · `後回し` · `実行不可` ·
`規則で不可` · `条件不足` · `不要` · `明確に否定`

**Separator: 「／」.** Each token may carry a parenthetical quoting the script
line that earns it (`順番待ち（「分け終わった順番どおりに出したいから、そのあとでね」）`)
— strongly preferred, since the quote is what makes the row re-derivable — and
that evidence usually contains 「、」, which is why the slash is the boundary
mark. 「、」 is accepted too, so no existing table needs rewriting; the token
itself is what is not flexible.

No token may appear in more than **2 rows of one 問題**, 例 included, and the cap
counts ROWS, not occurrences — a row that kills two distractors the same way
still counts once. Counting is then `grep`, not judgement. If a distractor's
elimination fits none of the nine, the distractor is not eliminated by a device
official uses: rewrite the line, don't invent a tenth label.

**Scope today: 問題1.** `check_choukai_elimination_tokens()` reads the 問題1 表
only — that is where the incident happened and where a paper has demonstrated
the vocabulary working. 問題2's 消去方法 column is still free text in all 12
papers on disk and stays QA's to read as prose (`exam-qa-review` §4); write it
in the closed vocabulary when you can, and expect 問題2 to adopt the rule once a
paper has shipped a compliant 問題2 表. Four papers with a pre-vocabulary 構成表
(`20260813_2`, `20260814_1`, `20260817_1`, `20260817_2`) are grandfathered by
name and print the measurement as a WARN; any other id FAILs.

**When a fix rewrites a script line, RE-DERIVE that row's 消去方法 token from the
NEW line.** A label that survives the rewrite of the line it describes is the
defect, not the fix. `20260817_3` fixed its over-cap by rewriting the 例's line
from 「場所が決まってからでいいよ」 (a real dependency → `順番待ち`) to
「それは、あとで一緒に書き込もう」 (no dependency → `後回し`) and left the cell
reading `順番待ち` — the second QA round found the table describing a line the
paper no longer contains. Re-derive from the script every time; the table is
evidence, and evidence is re-read, not carried forward.

### 決め手の種類 — the column that counts FACTS, not labels

Every other column of the 構成表 counts a label: 場面, 正解, 消去方法, 質問型. Two
items can differ in all four and still make the candidate do **the same listening
twice**, because what an item is *decided by* has no column at all.

`20260819_1` 問題2-1番 turns on 「実は、一人、卵が食べられない者がいまして」 and
問題2-3番, three items later, on 「今年入った人の中に、辛いものが食べられない人と、
魚が苦手な人がいて」 — one axis, *a diner who cannot eat something*, twice; 3番's
keyed option even prints the same lexical frame (「食べられない物がある人も
たのめること」). Nothing could see it: different 場面, different 正解, different
質問型, and the theme tags actively hide it (食 vs 働き方). The drawn scenarios did
not cause it either — `職場:歓迎会の店選び` carries no dietary constraint at all;
the author added one (`qa-report-20260819_1-round3` R3-S3).

**Add a `決め手の種類` column to the 問題1 and 問題2 構成表.** One token per row,
from this closed list — the same discipline §消去方法 already runs, for the same
reason (free text makes a repeat uncountable):

`在庫・数量` · `時刻・日程` · `費用・金額` · `規則・制度` · `身体・飲食の制約` ·
`場所・経路` · `人手・担当` · `設備・故障` · `連絡・情報の不足`

**No token in more than 2 rows of one 問題, 例 counted** — rows, not occurrences,
exactly as §消去方法 counts. Then read the column DOWN, not across. If a token
would take a third row, re-angle the item's deciding line onto another axis; the
scenario draw does not decide this, the author does.

**Not gate-checkable, on purpose.** Which fact decides an item is a judgment the
author makes while writing the deciding line, and a regex cannot re-derive it
from the script. The column is the artifact; QA reads it as a column
(`exam-qa-review` §4). `20260819_1`'s own measurement, filled in after the rule
existed: 問題1 = six distinct tokens; 問題2 = 在庫・数量2 / 身体・飲食の制約2 /
時刻・日程2 / 場所・経路1 — three tokens sitting exactly ON the cap, which is what
the finding above looks like once it is visible.

**THE CAP IS CONDITIONAL: two rows sharing a 決め手の種類 token must differ in
質問型** (added 2026-09-05, qa-report-20260904_2 F4). The cap of 2 bounds the
DECIDER and says nothing about what the candidate is asked to do with it — so
two items can sit exactly ON the cap, share a question frame, run the same
errand shape, and read compliant in every column. `20260904_2` 問題2 shipped
2番 and 4番 both **規則・制度 + どうして**, both a counter transaction stopped by
a prerequisite the customer must go fetch, with mirrored distractors
(2-2-1「保険の証券を持ってきていない」 ↔ 2-4-3「ゆずりますと書いた紙を、持ってきて
いない」; 2-2-3「郵便でしか受け付けられない」 ↔ 2-4-2「ネットからでないと、申しこめ
ない」). If they share both columns the candidate does the same listening twice
however different the 場面 and the 正解 look — **re-angle one item's deciding
line onto another axis and its question onto another frame.**

Unlike the cap above, **this half IS gate-checked**: both columns are closed
vocabularies, so the pair is decidable by string matching from the 構成表 alone.
`check_choukai_decider_question_type_pair` FAILs a 問題1/2 whose 構成表 has two
rows agreeing on both, counting 例 (the same denominator the cap uses); the
papers breaching the day it was written are named in
`DECIDER_QTYPE_PAIR_GRANDFATHERED` and WARN with the same measurement. Read the
set in `tools/check_consistency.py`, not this sentence, for who is exempt today.

**Re-angling a どうして row is usually the cheap side.** 問題2's 理由 quota is a
CAP of 3 with no floor, and its 内容・発言 quota is a FLOOR of 2 — so moving one
どうして row to 内容・発言 clears the pair and helps the other quota at the same
time, which is exactly the repair `20260904_2` took (4番 went 規則・制度 +
どうして → 連絡・情報の不足 + 内容・発言, and the transaction now completes rather
than being blocked). Relabelling the cell is NOT the repair: that is the
`choukai_decider_formula` defect, a false record in an audit artifact.

**AND THE 気持ち ROW HAS A CROSS-PAPER RULE OF ITS OWN** (added 2026-09-05,
qa-report-20260904_3 F3/R4). Every column above is read WITHIN one paper.
`20260904_2` and `20260904_3`, one paper apart, both put a 質問型=**気持ち** item
in 問題2-**6番**, both keyed the valence **安心**, both in key position 1, and
both on the same trigger shape: a service provider volunteers an accommodating
fact that dissolves a stated worry, and the customer opens 「よかった。」＋
「〜と思ってた(んです)」. `check_slot_theme_repeat` compares THEMES (食 vs
行政・手続き) and saw nothing.

- **The 気持ち item may not sit in the same numbered slot as either of the
  previous two papers'**, and **its keyed valence may not repeat inside that
  window** (安心 / 納得 / 心配 / 残念 / 不満 / 意外 / 感謝 / 期待 / あきらめ /
  迷い / 満足 / 困惑 / 驚き). `check_choukai_kimochi_repeat()` WARNs on both,
  which is where R4 put the call — a human's.
- Measured 2026-09-05 over all 23 papers, ten of which carry a 気持ち row: the
  SLOT line names four (`20260828_1` 1番, `20260828_2` 5番, `20260903_1` 5番,
  `20260904_3` 4番) and the VALENCE line one (`20260904_1` 心配 against
  `20260903_1` 心配). `20260904_3`'s hit is **repair collateral** — round 1's
  F3 fix swapped 問題2-4番↔6番 to get the 気持ち item off `20260904_2`'s slot 6
  and landed it on `20260904_1`'s slot 4, which is the shape
  `exam-qa-review` §repair collateral names.
- **The valence line reads the 正解 cell, so write the emotion IN it.** The
  same measurement found four of the ten rows unclassifiable — 「ほっとしている」,
  「ありがたく感じている」, and `20260904_3`'s own 「希望した場所ではないが、この席で
  よいと思っている」 — and an unclassifiable row is not compared at all (the
  gate's line says which). Name the valence with one of the words above and the
  row joins the measurement; the rest of the cell can say whatever it needs to.
- **Re-slotting is the weaker repair and re-angling the emotion is the stronger
  one**, in that order — moving the item leaves the same feeling keyed one
  paper later, which is what the valence line exists to catch.

### 決め手の位置 — the formula, and the denominator it is measured over

The column above capped 「3 of 6 rows in any one third」 from the day it was
added and **never said a third OF WHAT**, which made every label in it an
opinion. `20260903_1` is the first paper whose labels were actually re-derived
from the script, and two of six were wrong: the 例 was declared
「中盤（7行目／全10行）」 against a script with **9** spoken lines (7/9 = 0.78 →
終盤) and 5番 「終盤（10行目／全18行）」 against **17** (10/17 = 0.59 → 中盤). The
author had counted the closing question line into `m` in two rows and not in
the other four — an inconsistency no reader could catch, because the
denominator was nowhere written down (`qa-report-20260903_1-round2.md` F1/S1).

**The formula, binding:**

```
位置 = 決め手の発話の行番号 n ÷ その項目の総発話行数 m
  n/m ≤ 1/3        → 冒頭
  1/3 < n/m ≤ 2/3  → 中盤
  2/3 < n/m        → 終盤
```

- `m` counts **spoken script lines only** — the item's 場面説明 line and the
  closing question line are NOT lines of the dialogue and are never counted.
- **Non-dialogue items count SENTENCES instead of lines** (an announcement or
  automated menu has one speaker and no turns): write 「n文目／全m文」.
- **The 構成表 cell must print the count beside the label**, as
  `冒頭（3行目／全11行）` / `中盤（案内3文目／全9文）`. A bare 「中盤」 is a claim with
  no evidence, and it is what the two wrong labels above hid behind.

`check_choukai_decider_position()` reads both halves: it tallies the buckets
from the label prefix, and where the cell prints `n行目／全m行` it recomputes the
bucket from `n/m` and **FAILs on a label that disagrees with its own numbers**.
Papers whose 構成表 predates this format print the missing-denominator half as a
WARN and are named in `CHOUKAI_DECIDER_FORMULA_GRANDFATHERED` in
`tools/check_consistency.py` — **read the set in the code, not this sentence**;
an id leaves it by re-deriving its own column, never by widening the rule.

## Section item mix — quotas measured against the 31-sitting archive

A section that runs one item shape six times is solvable by pattern even when
every item is individually clean — and it has shipped, repeatedly, while
`make check` stayed green. Evidence and method:
`choukai-audio/references/official_register.md` §7.3. The left column below is
binding; write it into the 構成表 and check it there.

| 問題 | Quota | Official | Gate threshold |
|---|---|---|---|
| 1 | ≤3 of 6 items on the まず frame; ≥1 modify/method (どう直す・どのように); ≥1 condition-match (どの〜) or object frame | 36.8% まず / 5.8% modify / 1.9% condition | FAIL at ≥5 on one frame |
| 1 | ≥1 non-dialogue item per paper (announcement / message / automated menu) | 16% of 問題1 (25/155) | WARN |
| 1 | ≤2 of 6 items with ≥3 proposal-and-deny turns ("the probe carousel") | 2 items in 155; per-item median 0 | FAIL at >2 items |
| 1 | Decider position must not share a bucket (first/mid/last third) in >3 of 6 rows | spread ⅓ each | FAIL at >3 rows sharing |
| 1 | ≤2 of 6 items at a service counter; **≥3 must be someone assigning work** (「〜してくれる？」) | 6% at a counter (9/153) | WARN |
| 2 | **≥2 of 6 content/reported-statement questions** (何・どんな・〜と言っていますか) | 37.6% 内容・発言, plus 20.4% その他 | FAIL at 0 content items |
| 2 | 一番/優先 ≤2 **and** 理由 ≤3 of 6 | 5.5% 一番 / 32.6% 理由 | FAIL at >4 on one type |
| 2 | ≥1 item keyed to a speaker's 気持ち (Shin Kanzen: 「理由や目的、話し手の気持ち」) | 2–5% | target / QA |
| 3 | ≤2 of 6 institutional announcements; **≥3 must be an ordinary person's 主張・意図・経験** | 33.8% institutional / 39.0% person | FAIL at 5 of 6 institutional |
| 3 | Talk length: target **220–300 spoken chars** (band, not floor) | per item median 243 [p10 202, p90 320]; current era 158–397 | FAIL outside [150, 400] |
| 4 | **2–4 of 12 stimuli clearly casual**; ≤2 keigo counter prompts; no class-addressed stimulus (「〜の方は、…窓口へ」) | 20.7% casual (median **1** per sitting, max 6) / 9.1% keigo (median 0, max 2), rest neutral | FAIL at 0 casual; WARN below 2 casual or above 4 keigo |
| 4 | ≤2 of 12 items may carry an already-done distractor (**target**; archive ceiling 3, gate FAILs at >3 — §即時応答); ≤2 may key a reply opening 「あ、」 | median 1, max 3 | FAIL at >3 done |
| 5 | 1番 ≥3 speakers cast on distinguishable voices (≥1.9 st margin); 2番 the OTHER official type; no shared template | 31/31 sittings ≥3 spk | FAIL at 0 items with ≥3 spk |

**The non-dialogue item's MEDIUM rotates** (added 2026-09-03, `RC-C`). The
row-2 quota above is a floor with no rotation clause, and three consecutive
papers answered it with a recorded one-way voice message, twice in the same
slot (`20260828_1` 問題1-2番 留守電, `20260828_2` 問題1-3番 留守電, and
`20260903_1` **as first drafted** 問題1-3番 音声メッセージ —
`qa-report-20260903_1.md` handed item #5; the run of three is the evidence, and
the two adjacent-pair breaches inside it were `20260828_2` and `20260903_1`).
`20260903_1` has since been repaired and no longer reads that way on disk (see
the grandfather note below); the draft is quoted here because it is what the
rule was written against. So:

- **The three media are** 館内・車内アナウンス, 留守番電話／音声メッセージ, and
  自動音声メニュー. 留守番電話 and 音声メッセージ are **ONE class** — a recorded
  one-way message is one medium however it was delivered (answering machine,
  phone voicemail, a message file on a smartphone); relabelling the delivery
  does not rotate the medium, which is exactly what `20260903_1`'s draft did.
- **No medium may serve two consecutive papers**, and **the item may not sit in
  the same 問題1 slot number as the previous paper's**.

Both halves are decidable from the item's own lead-in line, so
`check_choukai_nondialogue_medium_rotation()` in `tools/check_consistency.py`
enforces them; that constant's comment carries the per-paper measurement and
the `CHOUKAI_NONDIALOGUE_ROTATION_GRANDFATHERED` set of the pre-rule papers
that breach it — **five today**, `20260810_1`, `20260818_1`, `20260819_1`,
`20260827_1`, `20260828_2`. An id leaves that set when its 問題1 non-dialogue
item is re-authored onto a different medium — never by widening the rule.

**`20260903_1` is the one id that has left, and it left the only way an id
may.** It was the founding case and it was still unshipped when the rule
landed, so it was repaired rather than exempted: its non-dialogue item is now
問題1-**4番**, a 市役所の電話の自動音声案内 (自動音声メニュー — a medium neither
`20260828_2` nor `20260828_1` used), and the 「アルバイトの引き継ぎ」 errand that
had carried the 音声メッセージ is voiced as a two-person phone call in 3番, with
the MP3 re-synthesised. It passes on merit, as a `check` and not a `warn`.
Read the set in the code, not this paragraph, for who is exempt today.

**Target vs gate.** These quotas are what you author to; `make check` (§G16)
FAILs only *beyond the archive's whole range* — a green gate means "no
official sitting looks this bad," not "this section is official-shaped." The
genre/counter/「あ、」 quotas can't be decided by regex; they print as a WARN
and QA settles them off the 構成表.

**Every "Official" cell above is printed by
`make choukai-profile BASELINE=1`** (`tools/choukai_profile.py`, §§2–7) over
the same 31 sittings, with the parse rule for each row printed under it.
Refresh a cell by pasting that output — three of these numbers (18% どのように,
問題3 median 305, 49% casual) were retyped from a one-shot analysis nobody could
reproduce, and papers were then authored to them (REPORT-CHOUKAI.md §F3, §F7).

**Which papers each of these gates exempts today.** The rules above landed
2026-08-21 against 14 finished papers, so every one of them ships with a named
grandfather set in `tools/check_consistency.py`, and **an id leaves its set the
moment that paper's 聴解 is repaired** — never by widening a threshold:

| Gate | Set | Ids exempted today |
|---|---|---|
| 問題1 質問型 mix | `CHOUKAI_Q1_FORMS_GRANDFATHERED` | all 14 — every paper runs one frame |
| 問題1 決め手の位置 (bucket spread) | `CHOUKAI_DECIDER_GRANDFATHERED` | all 14 (7 of them have no 構成表 column yet, so they skip) |
| 問題1 決め手の位置 label vs its own n/m (added 2026-09-04) | `CHOUKAI_DECIDER_FORMULA_GRANDFATHERED` | the 11 papers whose cells print no 「n行目／全m行」 — `20260807_1`, `20260810_1`, `20260810_2`, `20260817_3`, `20260818_1`, `20260819_1`, `20260821_1`, `20260827_1`, `20260827_2`, `20260828_1`, `20260828_2`. `20260903_1` prints all six and passes on merit |
| 問題1 主導 row cap (added 2026-09-04) | `LEADER_PAIR_GRANDFATHERED` | **none** — measured over every paper on disk, no 問題1 表 puts one 主導 string on more than 2 rows |
| 問題1 probe carousel | `CHOUKAI_PROBE_GRANDFATHERED` | `20260807_1`, `20260810_2`, `20260817_3`, `20260818_1`, `20260819_1` |
| 問題2 質問型 mix | `CHOUKAI_Q2_MIX_GRANDFATHERED` | all but `20260813_2` |
| 問題3 talk band | `CHOUKAI_TALK_BAND_GRANDFATHERED` | `20260807_1`, `20260810_1`, `20260810_2`, `20260811_1` |
| 問題4 stimulus register | `CHOUKAI_Q4_REGISTER_GRANDFATHERED` | all 14 — 0 casual stimuli anywhere |
| 聴解 voice balance | `CHOUKAI_VOICE_BALANCE_GRANDFATHERED` | all 14 |
| 聴解.mp3 pacing freshness | `PACING_SHA_GRANDFATHERED` | 13 — the Phase 4.2 jitter rebuild is still pending; **this set is not a policy, it is a to-do** |
| 問題1 non-dialogue medium/slot rotation (added 2026-09-03) | `CHOUKAI_NONDIALOGUE_ROTATION_GRANDFATHERED` | `20260810_1`, `20260818_1`, `20260819_1`, `20260827_1`, `20260828_2` — five; `20260903_1` **left the set by being repaired** (2026-09-03), which is the only way out |

**問題4's register is fixed by the DRAW, not by the writing.** `quick_response`
holds two kinds of entry: bare idioms and patterns (目を通す, 〜に決まってる),
where you invent the setting and therefore choose the register, and complete
service-counter sentences (「保険証の有効期限が切れております」), where the
register arrives with the draw. 80 of the pool's 200 entries are the second
kind, so an unconstrained draw of 11 landed ~4.4 keigo stimuli in every paper —
against an archive median of 0 and a maximum of 2. `sample_items.py`'s
`sample_keigo_capped()` now caps the drawn keigo sentences at the archive's
maximum (`KEIGO_CAP`), so the casual/neutral target is reachable by writing.
A paper drawn before 2026-08-25 carries the old, keigo-heavy draw; repairing its
問題4 means `--reroll quick_response`, not re-wording a stimulus whose tested
phrase is the keigo (core Item integrity #20 keeps the sampled expression).

**問題1's default is not a customer at a counter.** Official 問題1 is
overwhelmingly a superior, teacher or colleague handing out work (7/2025: 図書館
staff→staff, 課長→開発リーダー, 市役所職員→アルバイト, 部長→学生— zero counter
items). The counter shape is easy to solve: customer asks, staff refuse twice,
staff name the answer. Vary who drives (`choukai-audio` §"Banned formulas").

## Every wrong option is MENTIONED, then ELIMINATED

For 問題1, 問題2, and 問題4/5, every wrong option must be a real
task/statement/fact from the audio that is **reassigned, superseded, denied,
or reinterpreted** — never invented from nothing. An option nobody says is
fabricated noise: it lets the item be solved without tracking the
conversation. **問題3 (概要理解) only**: distractors are topic-level summaries
or general statements with a modifier missing/altered.

**An option raised and left TRUE is a second answer**, even as "only a
contributing factor" — a どうして item's wrong causes must be denied, not
merely outweighed. 課題理解 (問題1) hides the correct FIRST action behind
「その前に」「それが先」.

### 問題1: the deciding line's POSITION is part of the item, not just its content

Found 2026-08-18: a shipped test's 問題1 killed all three distractors in
**every one of its 6 items**, then pivoted on the identical word 「それより」
straight into the correct action — solvable by ignoring the dialogue and
taking whatever follows それより. `choukai-audio/SKILL.md` §Register rule 6
owns the evidence (official items where the deciding line sits first or
mid-turn, with a real later-due or already-claimed task trailing it) and rule
7 (a stated plan revised by new information mid-call). Binding:

- **Do not make the deciding line the section's last substantive clause in
  every item.** Place it first or mid-dialogue in at least half a section's
  items, and let the conversation continue with a real trailing task
  (later-due, or already assigned to the OTHER speaker) — never dead filler.
- **Do not signal the answer with the same pivot word every time** — count
  the pivot word per item the same way §"Eliminated ≠ contradicted" counts
  elimination devices.
- **Reach for a plan-revised-by-new-information shape** in one or two 問題1/2
  items per test (a booking, an order, an email already sent) — it moves the
  deciding line off the last position because the dialogue has to work out
  what changed, and it's official's own construction (`choukai-audio` rule 7).
- **When the deciding line does land last for its own reasons**, the option
  must not be a verbatim substring of that final clause — restate it, per
  §"The 解説 QUOTES the script; the OPTION restates it" below.

### Eliminated ≠ contradicted — rotate the DEVICE, and count it

Official kills a candidate by **reassigning** it to a named third party,
**deferring** it (その前に / 先に / 後回しになってました), **refusing** it
(難しい / 無理 / 見送), or noting it is **already done** (もう〜てある). Flat
「〜ではありません」 is its last resort: **0.4 per 10k chars**, against **17.1**
in papers written without this rule (archive: `official_register.md` §2.3).

- **No two items in a section may reuse the same elimination device for their
  key.** List device-per-item in one column; if it reads the same word four
  times, rewrite.
- **The elimination-device tally being perfectly flat is itself a signature.** Official
  does not distribute devices evenly across all nine tokens; it prefers reassign/defer
  and reaches for the others rarely. The nine tokens are a *ceiling* per row (≤2 rows each),
  not a checklist to fill evenly.
- Reassignment/deferral both satisfy the quotable-grounding rule below —
  naming WHO makes a better 解説 quote than a flat denial.
- 「一番大切なのは〜」 as the answer-marker in every 問題2 item is the same
  failure one level up: official runs 2.1 per 10k chars, generated papers ten
  times that. Mark the answer by **contrast** (「〜も大事ですけど、やっぱり…」)
  or **concede-then-correct**, and vary it item to item.

## Key length carries no information — the option a guesser picks must be wrong

**BINDING, every 聴解 section.** Found 2026-08-18 from a user report ("it tends
to make the longer key the correct answer"). Measured over the 11 papers then
on disk, the key was the **uniquely longest** of its options in:

| 問題 | Ours (before) | Official | Official key ÷ distractor mean |
|---|---|---|---|
| 1 (printed, 4 opts) | 52 % | 19 % (n=26) | 0.99 |
| 2 (printed, 4 opts) | 72 % | 25 % (n=71) | 1.00 |
| 3 (spoken, 4 opts) | 60 % | 27 % (n=130) | 1.02 |
| 4 (spoken, 3 opts) | 50 % | 29 % (n=241) | 1.00 |
| 5 (spoken, 4 opts) | 45 % | — | — |
| **whole 聴解** | **39–79 % per paper** | **28 %** (n=460, 31 sittings; per-sitting 13–29 %) | **1.00** |

A candidate who understood nothing, read the printed 問題1/2 list and marked the
longest line scored better than one who understood half the audio. That is the
whole defect: **the paper answered itself.**

**The bug is not that options vary in length — official varies MORE than we do**
(median max/min 2.55 in 問題1, against the 読解 rule's 1.30). Official option
sets are wildly uneven and the key sits anywhere in the order; 7/2025 問題3-3番
keys the SHORTEST of its four (「店をやる喜び」, 6 chars, against 13 and 15).
So **never equalise the four options** — that is a different, equally readable
tell, and it flattens the specificity that makes a distractor tempting.

**The cause is a length that varies WITH correctness**, and it comes from the
rule one section down: the key carries the paraphrase load, so it got written as
a full proposition while its distractors were left as bare topic labels.
`20260812_2` 問題2-2番 keyed 「雨の日は車がなかなかつかまらないこと」 (18 JP
chars) against 「料金の見方」(5) / 「クーポンの使い方」(8) /
「支払い方法の登録」(8) — three labels and one sentence, and only one of those
four shapes can be the answer.

**Repair, and the authoring rule: raise the DISTRACTORS, never trim the key.**

1. **All four options take the same grammatical shape and the same grade of
   specificity.** If the key is 「〜が〜で〜こと」, every distractor is too. If
   the key names a condition, the distractors name conditions. Official 7/2025
   問題2-1番: 食品かんれんの仕事をする / 大学院に進む / 研究の仕事をする /
   しゅっぱんしゃで働く — four of one shape, 7–12 chars, key 10.
2. **Grow a distractor with content the script actually gives it.** Every wrong
   option is already MENTIONED then ELIMINATED (§ above) and its 解説 cell
   already quotes the line that kills it — that quote is the material. Expand
   the label into the proposition the script states, then keep the 解説 cell
   pointed at the same line. Never pad with filler (「〜など」「しっかり」) and
   never invent a fact: a longer option that says nothing new is the same defect
   wearing the opposite sign.
3. **Vary the key's length RANK across a section** — roughly a quarter of items
   at each rank. One section whose keys are all rank 2 is still a pattern.
4. **Trimming the key is the last resort, not the first**, in 問題2 and
   問題5-1番: the key there must stay a genuine paraphrase (§"The 解説 QUOTES
   the script; the OPTION restates it"), and shortening is how a paraphrase
   collapses back into the script's own words. Fix the distractors instead.

`make check` (`check_choukai_longest_key_rate`, G16) FAILs a paper above **35 %**
uniquely-longest across the whole 聴解 section, and WARNs when the median key ÷
distractor-mean exceeds 1.15 — a paper can slip under the rate while every key
is still habitually the second-longest, which the ratio catches and the rate
does not. Both are measured over the whole section, not per 問題: five or six
items cannot separate a bias from noise. **Author to the official 28 %, not to
the 35 % ceiling.**

## Construction order is binding: dialogue FIRST, then harvest the options

Never draft an option set before the script line exists. Write the dialogue,
harvest the options from it, then record the grounding in the 解説 cell of
`聴解.md`, one line per wrong option — **this file is the single definition of
the artifact**:

```
1 ✗「script line as spoken」→ 別の人に割り当て
2 ✗「…」→ 後回しにされた
4 ✗「…」→ 明確に否定
```

An option with no quotable line is fabricated noise: delete it and take one
from the script. This cell is what QA reads; its absence means the item is
not shippable. `make check` (`check_choukai_option_grounding`, added
2026-08-27 per qa-report-20260810_1-choukai-repair.md F5 — this line
described the WARN for a long time before any function implemented it) WARNs
(not FAILs — 5/44 official options also miss a token match, since official
distractors are often paraphrased) when a 問題1/2 option shares no ≥2-char
kanji/katakana token with its script block; the mechanical check can't tell
"reassigned" from "never said" — the written grounding line is what does.

## The 解説 QUOTES the script; the OPTION restates it

These are two different jobs. Collapsing them is why **40 of 53 keyed 問題1/2
options (75 %) once contained no content word absent from their own script** —
answerable by catching one noun, nothing tracked or held.

Shin Kanzen teaches the opposite (実力養成編 IV-2, p.52): 「選択肢では、話の中の
長い説明を、**別の言い方で簡単に短くまとめている**ことがあります。また、
**2人の話を1つにしている**場合もあります。」 Official example — 7/2025 問題2-1番
says 「そこに入りたいんだ」 and keys 「しゅっぱんしゃで**働く**」: 入りたい→働く
*is* the item.

**Scope: 問題2 and 問題5-1番's action options** — not 問題1 (there the
discrimination is WHO/WHEN, not vocabulary; official reuses its own words,
e.g. 7/2025 keys 「本のデータをとうろくする」 against 「…登録してくれる？」), and
not 問題5-2番's labels (those must MATCH the dialogue's naming by design — see
below). For 問題2/問題5-1番:

- **Test the option's CORE word — its final verb or head noun — against the
  script, not the whole string.** A real paraphrase changes what carries the
  meaning: 溜まっちゃう→滞留する (process→result), 入りたい→働く (official),
  準備運動→ウォーミングアップ (register swap of the HEAD noun).
- **A whole-string kana-respelling is NOT a paraphrase.** Found 2026-08-18,
  `20260817_2` 問題2-2番: key 「学んだことを人にせつめいしてみる」 against script
  「学んだ内容を誰かに説明してみることなんです」 — only 内容→こと and 誰か→人
  changed; 説明する itself survives as its own kana spelling (せつめい). Same
  paper, 問題2-5番: key 「スマートフォンの画面を見せる」 against script's own
  「スマホの画面を…見せる方法」 — only スマホ→スマートフォン changed, 見せる
  unchanged. Both pass a naive "does some word differ" check while reusing the
  one word that actually decides the item.
- **`make check`'s mechanical WARN (`check_choukai_key_paraphrase`) cannot see
  either example above.** It only tokenizes 2+-char kanji runs and 3+-char
  katakana runs; a key written mostly in hiragana (せつめいしてみる) yields zero
  tokens and is silently exempted. A clean `make check` on this point proves
  nothing — judge the core word by eye, every time, for every 問題2/5-1番 key.
- **Reach for 「2人の話を1つにする」** — merge what A proposes with what B
  accepts into one option; the cheapest way to make an option unmatchable to
  any single line.
- The 解説 still quotes the script verbatim (§"Construction order" above);
  quotable ≠ copyable — the quote proves the option is grounded, the
  paraphrase is what makes it an item. Distractors keep sharing vocabulary
  with the script (that's what makes them tempting) — **only the KEY carries
  the paraphrase load.**

Not gated as a FAIL: official listening options are kana-leaning
(`jlpt-exam-structure` §"Printed options are kana-LEANING"), so token-matching
against a kanji script understates official overlap. `make check` reports our
own verbatim share as a WARN against a design threshold, not a measured band.

### The verbatim gate runs in ONE direction — the other end is the 構成表's arrow

`check_choukai_key_paraphrase` measures how CLOSE a key sits to the deciding
line, so everything above pushes keys away from the script's words. Nothing
measures a key that has drifted too FAR, and 13 of 13 papers are therefore
measured in one direction only. `20260818_1` 問題2-2番 scored 0/6 verbatim —
green — while keying 「作ったものを試せる機会が多いから」 against a decider of
「自分の手で**形にできる**回数が、東の方がずっと多いんです。そこが決め手で」: 形にする
is not 試す, so the key names a proposition the script never states. The item
still had one answer (all three distractors were explicitly denied), which is
exactly why it survived — a paper can be keyed by elimination and still be
mis-keyed as a paraphrase (`qa-report-20260818_1` F13).

**The rule, and it cannot be mechanized:** the 構成表's 鍵の言い換え column already
forces the author to write `decider → key`. **Read that arrow as an EQUATION.**
If the two sides are not the same proposition, the key is wrong even when every
distractor is denied — repair the KEY, not the distractors. Both directions in
one sentence: the key must restate the decider in different words, and it must
restate *that* decider, not a neighbouring idea the same scene would support.
Verbatim distance is gated; propositional identity is human judgment, so it is
QA's step-1 read (`exam-qa-review`) and the author's own arrow, and a clean
`make check` proves only the near half.

**A paraphrased key may not assert MORE than its deciding line does** (R3,
`qa-report-20260818_1-round3` F2 — the same one-directional hole, one notch
milder). `20260818_1` 問題2-3番 keyed 「子どもが学校を休まずにすむこと」 off
「子ども、次の日の朝から授業があるので」: going to a Wednesday **evening**
performance would not require an absence, so 欠席 is a state of affairs the script
never puts on the table. The key was tightened to
「子どもの翌日の授業にさしつかえないこと」. The item still had one answer (all three
distractors are explicitly denied on air), which is why it shipped — being keyed
by elimination hides an overstated paraphrase exactly as it hides a mis-keyed one.
**QA/authoring procedure, not gatable:** set the key beside the decider and point
at every noun that exists only in the key (欠席・休む・遅刻・無料 …); for each one,
name the script word it corresponds to. If you cannot, the key has added a
proposition — trim the key to what the line asserts, or move the deciding line so
it asserts what the key says.

## 問題3 (概要理解): the narration names the SETTING, never the topic

Official 問題3 item lines are setting plus speaker only — 「1番 ラジオで女の人が
話しています。」 — **never** what the talk is about, in every item of every
sitting; the question 「何について話していますか」 is the whole task, so naming
the subject in the lead-in answers it. Write `N番。<場所>で、<話者>が
話しています。` and stop. `make check` fails a lead-in carrying 「〜について」/
「〜の話」.

**The monologue must NOT mention its own wrong options.** No 問題3 monologue
in 31 sittings refers to its distractors — the four options are topic-level
summaries of one talk with a modifier moved or scope widened. The closing
"denial sweep" (「Xの話ではありませんし、Yについて論じているのでもありません」)
is **forbidden** (0 occurrences in the archive, shipped in every item of a
generated 問題3 before this rule) — it hands the answer to anyone who hears
three negations, and no human speaks that way. `make check` fails the formula
outright and also fails a talk mentioning two or more of its own options.

**Options are bare noun phrases, never suffixed 「〜について」** (一人旅をするよさ,
not 一人旅について) — 8 of 685 archive options end that way (1 %), against all
24 of a five-paper generated sample.

**No content word may appear in two or more of 問題3's read-aloud options and
be the KEY every time.** 問題3's options are spoken, so the only thing a
candidate can carry across the section is their vocabulary: a word that turns
up in two of the ~24 options, both of them keys, and in none of the ~18
distractors is a lexical signature the answer wears. Whoever notices it
answers two items without understanding either talk. This is the 聴解 form of
the 読解 rule against a key identifiable without reading the passage.

`20260904_1` shipped exactly that: 「そのまま」 in 3-1番's option 3 and 3-5番's
option 1, both keys, zero distractors — and both talks even ran one arc
(以前は加工していた → そのまま通した → そのほうが効いた), which is what made the token
a real handle rather than a coincidence (`qa-report-20260904_1` F4).

- **The repair is to RE-ANGLE one of the two items** so its key states the
  claim in its own vocabulary, then take the word out of the option. Re-keying
  a 問題3 item changes WHAT the surface tests, so update `logs/topics.json`'s
  `surfaces`/`claim`/`shapes` and stamp the spec/ledger row `"origin":
  "reauthored"` with a note QUOTING the new deciding line.
- **Handing the word to a distractor is NOT the repair.** It removes the
  measurement while leaving two keys on one narrative arc.
- `check_choukai_key_exclusive_token()` reports this, over 問題3 only. That
  scope is measured, not cautious: the same predicate run over 問題4 flags the
  reply formulas 即時応答 is made of (「わかりました」「じゃあ」「お願いします」) in
  eight generated papers **and in official 7/2022** (「だよね」 ×2, both keys),
  so it is refuted for that 大問; 問題1/2 print their options, where a shared
  word is on the page for everyone. Over 問題3 alone, none of the eight
  official sittings on disk flags.
- **The column is read over VERB AND ADJECTIVE LEMMAS, not only 2+-kanji
  tokens.** `20260904_3`'s own 構成表 asserted 「0件」 from a re-run that used
  three kanji/katakana/kana patterns, and 「変え」 was sitting in 2 of its 24
  options — 2番's key 「今年から**変える**、健康診断の日の決め方」 and 3番's key
  「会場を作る人の分け方を**変えた**こと」, both keys, zero distractors
  (`qa-report-20260904_3` F4/F8a). One kanji plus okurigana is not a
  2-kanji token, and two inflections of one verb are not the same string, so
  the predicate could not represent the case at all. `check_choukai_key_exclusive_token()`
  now folds 漢字1字＋送りがな to `lemma:<漢字>`, **excluding a trailing kana that
  is a case particle** (はがをにでともへやかのねよ — without the guard
  「契約書**で**」 reads as the verb 書く). When you re-run the audit by hand,
  run the fold too, and say so: an audit table that certifies a measurement is
  worth exactly the measurement.

**The six talks of one 問題3 must run six DIFFERENT ARCS.** The lexical rule
above is about WORDS; this one is about how the monologue MOVES, and it is the
defect a word-level scan cannot see. `20260904_3` ran 「以前／想定と違った →
変えた → 効いた」 in FOUR of its six talks (例・1番・3番・5番), and 1番 and 5番
were additionally the same food-retail owner speaking at a 講演会/講座 whose
crux was the same 受け渡しの時刻 — two of five scored items were one listening
(`qa-report-20260904_3-round2` F2; `20260904_1` had shipped the same class one
paper earlier).

Measured against the archive: official **7/2025** runs 一人旅のよさ
〈自分の好みとその理由の説明〉/ 木の家具 〈物の魅力の説明〉/ 菓子屋
〈仕事の喜びの語り〉/ 良い睡眠 〈通説の訂正と条件の提示〉/ 米作りロボット
〈問題→技術の導入→効果〉 — five arcs, **one row each**, and exactly one of the
five on a problem→solution arc. Official **12/2025**: 片付けの効果
〈効用の列挙〉/ 研修の評価 〈体験の評価〉/ 子への注意 〈助言〉/ 固形石けん
〈自分の選択とその良さの説明〉/ 農業体験会 〈取り組みの目的の説明〉 — five arcs,
one row each. Neither sitting repeats an arc.

- **The 問題3 構成表 carries a 「話の型（アーク）×決め手の領域」 column**, one cell
  per row, both halves from the vocabulary below. It is a declared column and
  not a derived one on purpose: an arc is a claim about a 300-character
  monologue, no regex decides it, and a guessing predicate would either miss
  this defect or fail a real sitting.
- **No two rows may share BOTH tokens** (`check_topics_p3_archetype_repeat()`
  FAILs), and **no arc may fill more than 2 of the rows** (WARN — official runs
  1). A paper whose 構成表 has no such column is *unmeasured*, and the gate says
  `skip`; a skip is not a pass.
- **The arc vocabulary**, as it stands from the papers and sittings measured
  above: 自分の方針とその理由の説明 / 自分の好みとその理由の説明 /
  自分の選択とその良さの説明 / 条件の提示 / 範囲の説明 / 以前のやり方→変更→効果 /
  問題→技術の導入→効果 / 注意事項の案内 / これから始める人への助言 / 助言 /
  物の魅力の説明 / 仕事の喜びの語り / 通説の訂正と条件の提示 / 効用の列挙 /
  体験の評価 / 取り組みの目的の説明. A new arc is authoring, not a defect — add
  it here **and** to `P3_TALK_ARCS` in `tools/check_consistency.py` in the same
  edit, because an arc spelled two ways cannot collide with itself.
- **The repair is to re-angle the ARC, not to move the draw**: keep the drawn
  `listening_scenarios` entry and its theme tag, change what the talk does with
  it. Re-keying it changes WHAT the surface tests, so the `origin: reauthored`
  stamp and the `surfaces`/`claim`/`shapes` update apply as above.

**The talk must be long enough to have a gist.** Official 問題3 talks run a
median of **305 spoken chars** (p10 251, minimum 177 over 149 items,
`official_register.md` §7.4); a four-sentence talk has no structure to
summarize, so a 概要 question degenerates into 沿って聞く. **Target: 220+
spoken chars** — make the point twice in different words. `make check` FAILs
below 175 (the archive minimum); clearing the gate is not the same as hitting
the target.

## Spoken choice pacing

Options spoken in 聴解 follow official lengths: **~10–15 chars per choice** in
問題3/問題4.

## 統合理解 (問題5): two items, two DIFFERENT types

Shinkanzen's 問題紹介 defines two shapes, one of each every sitting:

- **1番 — 2人以上の話し手の意見を整理しながら聞き取る.** A three-party discussion;
  the four options are ACTIONS harvested from the argument. **3 speakers in
  every sitting since 2020** — nobody reads a list, candidates surface as
  proposals and two are killed by the other participants. Must have ≥3
  speakers and no menu (`choukai-audio` Part 2 owns casting/pitch margins).
- **2番 — ある話を聞いた後で、それについての意見や評価を聞いて判断する.** A third
  voice enumerates four candidates, **then** two listeners weigh them;
  質問1/質問2 separate the two picks. Must keep the heard-then-evaluated
  shape — the enumerating voice is not one of the two deciders.

Five generated papers running made both items the same shape (two speakers,
four labelled candidates, eliminated one at a time) — that's 問題1's task
twice at double length, spending both 統合理解 slots on 課題理解.

**Rotate the 質問 pair across tests.** 「最初どう思っていたか／最終的にどうする
ことにしたか」 ran four consecutive papers; official also rotates
男の人は／女の人は, 1日目/2日目, 最初/結局.

**BINDING: 質問1 and 質問2 must key DIFFERENT options.** They are two scored
items sharing one dialogue, and the shape only earns its two marks if they
track two different resolutions. Key both to the same option and they collapse
into one: whatever answers the first answers the second. MEASURED 2026-09-05 —
**0 of 31** official sittings key 質問1 = 質問2 (`refs/JLPT_N2_NEW/*/key.md`)
and **0 of 32** papers under `tests/` do. `20260904_2` was the first and only
one ever to ship it, both keyed 「1 お部屋」 off a dialogue whose man opens
「僕は部屋で食べたいな」 and closes 「じゃあ、部屋にしよう」 — a candidate who
heard only the opening turn banked 2/2 (qa-report-20260904_2 F2, an automatic
QA fail). `check_mondai5_2_distinct_keys` FAILs it.

Two things the gate cannot see and you must still do: **neither question may be
answerable from the opening turn**, and the fix is a re-authored item, not a
swapped digit. The repaired `20260904_2` is the model — the man opens on
筋力体操 (option 3) and the woman on 眠りの講座 (option 4), both openers are
killed by their own quoted lines, and the keys land on 1 and 2. Note that
`MAX_SECTION_MODE["聴解_問題5"] = 2` lets two of the section's three answers
share a position and cannot know that entries 2 and 3 ARE 質問1 and 質問2, so a
drawn plan can RESERVE this collision: check the pair against the plan before
authoring, and re-measure `answer_positions` by hand after any repair.

### The 構成表 must state BOTH items' decision structure, against the last three papers

Each 問題5 item's task shape is FIXED (1番 a multi-person meeting choosing among
proposals, 2番 a two-person pick-one-from-a-list), so the only thing that can
vary between papers is the **decision structure** — who proposes, the order
candidates die in, and whether the adopted one is a late arrival, an opening
proposal held pending a condition, or a plan someone reverses.

**Write that structure into the 問題5 構成表 for 1番 AND 2番, naming the previous
three papers' structures.** This existed as prose for 2番 only, and it worked:
all four papers carrying a 構成表 varied 2番 deliberately and documented it. All
four said nothing about 1番, and `20260818_1` then shipped a 問題5-1番 with
`20260817_3`'s exact archetype — a three-person local-association meeting that
rejects three proposals on three grounds and adopts a NEW idea raised late — same
slot, consecutive papers (`qa-report-20260818_1` F3). The rule named the wrong
slot, so the paper complied with it and repeated anyway. Structures seen so far,
so the next paper can diff against them:

| paper | 1番 | 2番 |
|---|---|---|
| 20260817_1 | — | 単独逐次消去 (one person kills candidates by their own constraints) |
| 20260817_2 | — | 共同逐次消去 (a couple kills together, then splits the last two) |
| 20260817_3 | 逐次消去＋後出し採用 (three rejected on three grounds, a late new idea adopted) | 入れ替わり型 (mutual advice moves both off their first pick) |
| 20260818_1 | 冒頭提案＋条件保留 (the adopted plan opens the talk, two back it for DIFFERENT reasons, a condition holds it, the alternatives are explored as fallbacks and die, the condition is then met) | 共同決定＋用途別の第二選択 (the two settle ONE candidate for shared use, then one of them takes a DIFFERENT one for a second, individual purpose — and the candidate that was impossible in the first context is the key in the second; official 7/2014 and 7/2015 問題5-3番 both run it). Its first draft was 別人のための選択 (each choosing for a different beneficiary) and was replaced when the scenario was redrawn for R2-F3 — the row records what the paper SHIPS |

No script gates this — the table is the artifact, and QA reads it as a column
(`exam-qa-review` §4).

## 問題5-2番 choices — spoken, not printed

This repo prints nothing in 問題5; 2番's four choices are read aloud after
質問1 and again after 質問2 (divergence from official, owned by
`jlpt-exam-structure` §"問題5 prints nothing"; `choukai-audio` owns where they
sit in the script block). Authoring musts:

- **Bare labels** (「夕日通り / にしがおか / さくら公園 / 東山」), never full
  sentences and never the deciding attribute riding along
  (`4、東山、商店街の近くで便利です。` is forbidden) — a choice that restates the
  heard attribute answers itself.
- **Short and phonetically distinct** — spoken-once labels can't be re-read;
  four names differing by one mora is an accidental discrimination item, not
  統合理解.
- **Announce each question as 「質問1。…」/「質問2。…」** — the marker is what the
  synthesizer keys 質問1's 10 s answer pause off, so a bare question line ships
  an item nobody has time to answer. Rule and incident:
  `choukai-audio` §"質問1。/質問2。 are not labels, they are the answer pause".
- **ONE set of four labels, read identically after both questions** —
  `20260812_2` read short labels after 質問1 and ~20-char compound sentences
  after 質問2, so the two questions stopped sharing a candidate list. Write
  the four once, read that block twice.
- The 10–15-char band above is for 問題3/問題4 sentence options; 問題5-2番's
  labels are names — shorter is correct.

## 即時応答 (問題4)

**The stimulus must be spoken TO a specific person, never broadcast.** Never
label a 問題4 stimulus `アナウンス:`/`アナウンサー:` (those are 問題3-monologue
labels with no expected reply, per `SPEAKER_MAP`) — a facility-wide PA prompt
has no addressee to answer as. If a drawn `quick_response` phrase reads as a
broadcast, recast it as a specific staff member speaking to the specific
customer in front of them (same tested phrase/register, now addressed).

**The answer is often INDIRECT — 間接的な答え方** (Shin Kanzen 実力養成編 II-2-B,
p.29): 男「一緒に行きませんか。」's real answer is 「ちょっと、熱があるんです。」 —
a fact implying 断り, not a direct 受け/断り. Official's 973 replies run 13 %
as questions and only ~15% open with an explicit acceptance marker (はい/
わかりました/承知); write some keys as inferences (state the obstacle/
consequence and let it imply the reply), and let a reply BE a question
(official median ~4/paper, band 0–15 — not gated, since 0 alone is inside the
archive; only a reader can tell "none" from "none, and every key is a direct
acceptance").

**The three replies must not open はい/いいえ/では.** Official: 94 % open with
content, only 1.3 % on those three combined. Write the three as **stances**
on the prompt (take-and-act / misread tense-or-aspect / invert polarity), not
yes/no signals — official 4番 pattern (7/2025, OCR): prompt 「この量は食べきれ
ないよ。」 → `1 私、ちょっと食べてあげようか？` `2 他のも注文する？`
`3 量、ちょうどいいんだ。`, none announcing yes/no. Reply length stays ~15 chars
median. `make check` WARNs above the official opener rate.

**No reply SHAPE may be the key** (the already-done trap): when almost every
「もう〜た」 option is wrong, もう **is** the key and the item scores without
Japanese (archive averages 1.0 such item in 11.4; shipped papers have run
9/11 and 8/11 before this rule). Bounds for a paper's 問題4 (12 items incl. 例):

- **Already-done distractors: author to ≤2, three is the archive's ceiling,
  four fails.** The archive runs a **median of 1** such item in 11.4 and a
  **maximum of 3**, so the three numbers are: write 1–2; a third is inside what
  official ships and is allowed only when the 構成表 names the three rows and
  says why each needs the shape; a fourth is beyond anything official ships and
  `make check` FAILs it. This is §"Target vs gate" applied — the quota table's
  「≤2 of 12」 is the authoring target, the archive's range is the bar — and it
  is written out here because the flat 「≤2」 read as a hard cap and left
  `20260817_3` sitting at 3, in the gap between two numbers **in this same
  file** (round 3, R3-5). Do not read the ceiling as the target: the median is
  1, and a generator that writes to the maximum every paper reproduces the
  distribution official does not have (see `bunpou.md` §問題7 for the same
  failure on a different number).
- **Count the SHAPE, not the word: もう / すでに / さっき / 先ほど / 今しがた /
  たった今 + 〜た**, and any other wording that says the task is finished.
  `20260817_3` shipped three (「もう受け付けました」「もう全部消しときました」
  「先ほど郵便で送りました」) and counted two, correctly under the old token list,
  because 先ほど was outside it. `make check`'s regex now carries all six words
  as a **lower bound** on the count — it is the reading aid, not the rule; a
  finished-task reply worded around all six still counts.
- **Concentration bound on the other shapes**: no single shape may account for
  more than **40 %** of the distractor SLOTS, and **no two items may share BOTH
  of their distractor shapes**. This replaces the ">2 items per shape" form,
  which was arithmetically unsatisfiable and so was ignored rather than obeyed:
  22 distractors over 5 named shapes at ≤2 items × 2 distractors = 20 slots < 22
  (`20260817_3` QA, round 1).
  - **The shape is one token from a CLOSED vocabulary**, written in the 構成表's
    「誤答の型」 column, two per row: **時制の誤り / 論点のずれ / 語義の取り違え /
    誤った前提 / 立場の逆転 / 対象の取り違え / 既に完了**. Free text is what makes
    both caps uncountable — four papers (`20260813_2`, `20260814_1`,
    `20260817_1`, `20260817_2`) wrote 「すり替え」「的外れ」「事実に反する」 and their
    columns cannot be compared with anything, which is the same failure 消去方法
    had before its vocabulary landed. `check_choukai_p4_distractor_shapes()`
    reads the column; those four are exempt by name and any other paper FAILs.
  - **The 40 % denominator is the DISTRACTOR SLOTS (2 per row, 24 in a 12-row
    大問), not the rows.** Measured 2026-09-05 over all 16 papers carrying the
    column, the corpus maximum is **7/24 = 29 %** (`20260817_3`, 論点のずれ and
    語義の取り違え) and no paper trips 40 %; read against ROWS instead, 15 of 16
    would trip it, which is how a cap gets quietly abandoned.
  - **例 counts**, like every other 構成表 cap (消去方法, 主導, 決め手×質問型): its
    distractors are heard and its key is announced. Measured that way, seven
    papers ship one duplicated pair each — `20260817_2` 既に完了+的外れ (例+1番),
    `20260817_3` 誤った前提+論点のずれ (例+7番) **and** 語義の取り違え (3番+9番, the
    only scored-row pair on disk), `20260819_1` 時制の誤り+論点のずれ (例+9番),
    `20260827_1` and `20260827_2` 対象の取り違え+論点のずれ, `20260828_2`
    誤った前提+論点のずれ (例+9番), `20260903_1` 時制の誤り+論点のずれ (例+7番) —
    all exempt by name; `20260904_1`/`_2`/`_3` are clean on merit.
- the KEYED reply may open with 「あ、」 in ≤2 items.

List the 12 keys in one column and the 24 distractors in another, **writing
each distractor's shape beside it** — if either sorts by form, the section is
broken (same read the 構成表 demands above). The shape column is what makes
both caps above countable instead of impressionistic.

Tests idioms/keigo (目を通す, お言葉に甘えて, 〜かと思いきや, 〜ようがない,
席を外しております, 在庫を切らしております): invent the SETTING yourself, keep
the sampled keigo/idiom, and match the keyed reply to the speaker's rank and
keigo direction (core Item integrity #20).

**The keyed reply introduces no unstated premise.** A key that presupposes a
fact the prompt never states (an appointment, a prior arrangement) lets a
plain reply that answers the prompt AS STATED compete with it — a
double-answer fail. When the key needs such a premise, put it in the prompt;
otherwise pick a key the prompt grounds.
