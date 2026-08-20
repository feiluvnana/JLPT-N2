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
| 項目 | 場面 | 主導 | 正解 | 消去方法 | 質問型 |
|---|---|---|---|---|---|
| 1番 | スーパーのレジ | 店員→客 | 本人確認書類を提示 | 順番待ち（先に会員登録）／不要／実行不可 | この後まず |
| 2番 | 会社の朝会 | 部長→部下 | 見積書を送る | 別の人に割り当て／既に完了／条件不足 | この後まず |
```

Then read it **as columns, not as rows**:

- **正解** — no two rows may name the same action or object.
- **消去方法** — no device more than twice (§"Eliminated ≠ contradicted").
- **場面 / 主導 / 質問型** — against the quotas below.

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

## Section item mix — quotas measured against the 31-sitting archive

A section that runs one item shape six times is solvable by pattern even when
every item is individually clean — and it has shipped, repeatedly, while
`make check` stayed green. Evidence and method:
`choukai-audio/references/official_register.md` §7.3. The left column below is
binding; write it into the 構成表 and check it there.

| 問題 | Quota | Official | Papers written without this rule |
|---|---|---|---|
| 1 | ≤2 of 6 items at a service counter; **≥3 must be someone assigning work** (「〜してくれる？」) | 6 % at a counter (9/153) | 42 % (17/40); 5/5 in `20260813_2` |
| 2 | ≤2 of 6 keyed by 「一番/優先」; **≥2 理由 (どうして)**; ≥1 どのように | 6 % / 37 % / 18 % | 52 % / 38 % / 2 % |
| 3 | ≤2 of 6 institutional announcements; **≥3 must be a person's 主張・意図・経験** | Shinkanzen: 「話し手の意図、主張などを判断する」 | 6/6 announcements, last two papers |
| 4 | ≤2 of 12 items may carry an already-done distractor (**target**; the archive's ceiling is 3, the gate FAILs at 4 — §即時応答); ≤2 may key a reply opening 「あ、」 | median 1, max 3 of 11.4 | 9/11, 8/11 |
| 5 | 1番 ≥3 speakers; 2番 the OTHER official type; no shared template | one of each type, every sitting | last 5 papers: same template twice |

**Target vs gate.** These quotas are what you author to; `make check` (§G16)
FAILs only *beyond the archive's whole range* — a green gate means "no
official sitting looks this bad," not "this section is official-shaped." The
genre/counter/「あ、」 quotas can't be decided by regex; they print as a WARN
and QA settles them off the 構成表.

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
not shippable. `make check` WARNs (not FAILs — 5/44 official options also miss
a token match, since official distractors are often paraphrased) when a
問題1/2 option shares no ≥2-char kanji/katakana token with its script block;
the mechanical check can't tell "reassigned" from "never said" — the written
grounding line is what does.

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
- **Concentration bound on the other shapes** (misread tense, inverted
  polarity, wrong addressee, answering a different question): no single shape
  may account for more than **40 %** of the paper's 22 scored distractors, and
  **no two items may share BOTH of their distractor shapes**. This replaces
  the ">2 items per shape" form, which was arithmetically unsatisfiable and so
  was ignored rather than obeyed: 22 distractors over 5 named shapes at ≤2
  items × 2 distractors = 20 slots < 22 (`20260817_3` QA, round 1).
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
