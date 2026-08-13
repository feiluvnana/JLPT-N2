# 聴解 items — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — sniff test, item integrity (the 解説 verbatim-quote rule
and the 即時応答 keigo-direction rule are #19–20 there). Script FILE format and
audio pacing are owned by `choukai-audio`; booklet printing conventions
(問題5-2番 labels, instruction wording, 例 mechanics) by `jlpt-exam-structure`.

## Write the SECTION TABLE, then read its COLUMNS — required artifact

Every 聴解 defect that has cleared both a green gate and a fresh-eyes QA was a
**section-level repeat**, invisible item by item. `20260813_2` 問題1 keyed
「本人確認書類を提示する」 in **both** 1番 and 2番, reached by the same interrupting
line 「あ、すみません、〜の前に…先に確認させていただけますか」 — two consecutive
items, one answer, one device, both individually clean. Nothing in the pipeline
had ever put two keys side by side.

A section is not finished when its items are written. Append to `聴解.md`,
**after the answer-key heading** (so `strip_key()` keeps it out of `解答.html`),
one table per 問題:

```
## セクション構成表（作問監査用）
### 問題1
| 項目 | 場面 | 主導 | 正解 | 消去方法 | 質問型 |
|---|---|---|---|---|---|
| 1番 | スーパーのレジ | 店員→客 | 本人確認書類を提示 | 割り込み「その前に」 | この後まず |
| 2番 | 会社の朝会 | 部長→部下 | 見積書を送る | 第三者に割り当て | この後まず |
```

Then read it **as columns, not as rows**:

- **正解** — no two rows may name the same action or object. The same key twice is
  a duplicate item, not a coincidence.
- **消去方法** — no device more than twice (§"Eliminated ≠ contradicted").
- **場面 / 主導 / 質問型** — against the quotas in the next section.

If a column repeats, rewrite the ITEM, not the table. QA reads this table first
(`exam-qa-review` §4 聴解); a section with no table is not shippable.

## Section item mix — quotas measured against the 31-sitting archive

A section that runs one item shape six times is solvable by pattern, which is a
content defect even when every item is individually clean — and it is what has
actually shipped, repeatedly, while `make check` stayed green. Evidence, method
and per-paper numbers: `choukai-audio/references/official_register.md` §7.3. The
left column is binding; write it into the 構成表 above and check it there.

| 問題 | Quota | Official | Papers written without this rule |
|---|---|---|---|
| 1 | ≤2 of 6 items at a service counter, and **≥3 must be someone assigning work** (「〜してくれる？」, 「〜しておいてもらえますか」) | **6 %** at a counter (9/153) | 42 % (17/40); **5/5** in `20260813_2` |
| 2 | ≤2 of 6 keyed by 「一番/優先」; **≥2 理由 (どうして)**; ≥1 どのように | 6 % / 37 % / 18 % | 52 % / 38 % / **2 %** |
| 3 | ≤2 of 6 institutional announcements; **≥3 must be a person's 主張・意図・経験** (ラジオ/テレビ/講演/インタビュー) | Shinkanzen 問題紹介: 「話全体の主題、話し手の意図、主張などを判断する」 | **6/6** announcements in each of the last two papers |
| 4 | ≤2 of 12 items may carry an already-done distractor; ≤2 may key a reply opening 「あ、」 | median 1, **max 3** of 11.4 | **9/11** (`20260813_2`), 8/11 (`20260810_2`) |
| 5 | 1番 ≥3 speakers; 2番 the OTHER official type; no shared template | one of each type, every sitting | last **5** papers: same template twice |

**Target vs gate.** The quotas above are what you author to; `make check`
(§G16 in `tools/check_consistency.py`) FAILs only *beyond the archive's whole
range* — 「について」 above 2, a talk under 175 chars, already-done above 3, zero
3-speaker 問題5 items, any split turn — so a green gate means "no official
sitting looks this bad", not "this section is official-shaped". The 問題1/問題2/
問題3-genre quotas and the keyed-「あ、」 cap cannot be decided by regex at all:
they print as one WARN per paper and QA settles them off the 構成表.

**問題1's default is not a customer at a counter.** Official 問題1 is
overwhelmingly a superior, teacher or colleague handing out work — 7/2025 runs
図書館 staff→staff, 課長→開発リーダー, 市役所職員→アルバイト, 部長→学生, and not
one counter item. The counter shape is easy to write and easy to solve: the
customer asks, staff refuse twice, staff name the answer. Vary who drives
(`choukai-audio` §"Banned formulas").

## Every wrong option is MENTIONED, then ELIMINATED

For 問題1, 問題2, and 問題4/5, every wrong option must correspond to a real
task/statement/fact from the audio that is **reassigned, superseded, denied, or
reinterpreted** (already done / rejected / 「それが理由ではありません」) — never
invented from nothing. An option nobody says is not a distractor, it is
fabricated noise, and it lets the item be solved without tracking the
conversation. For **問題3 (概要理解) only**, official distractors are
topic-level summaries or general statements with key modifiers missing/altered.

**An option that is raised and left TRUE is a second answer**, even if it is
"only a contributing factor": e.g., an item affirming 道が混んでいた in
a dialogue where that was just a minor factor. A どうして item's wrong causes must be denied,
not merely outweighed.

課題理解 (問題1) hides the correct FIRST action behind 「その前に」「それが先」.

### Eliminated ≠ contradicted — rotate the DEVICE, and count it

Measured over the 31-sitting archive against generated papers
(`choukai-audio/references/official_register.md` §2.3), official kills a
candidate by **reassigning** it to a named third party, **deferring** it
(その前に / 先に / 後回しになってました), **refusing** it (難しい / 無理 / 見送), or
noting it is **already done** (もう〜てある). Flat 「〜ではありません」 is its last
resort: **0.4 per 10 k chars, against 17.1 in papers written without this
rule**.

- **No two items in a section may use the same elimination device for their
  key.** Write the section, then list device-per-item in one column; if the
  column reads the same word four times, rewrite.
- Reassignment and deferral both satisfy the quotable-grounding rule below —
  「その資料は山下さんが引き受けてくれました」 is a better 解説 quote than
  「それは必要ありません」 precisely because the listener has to track who.
- 「一番大切なのは〜」 as the answer-marking phrase in every 問題2 item is the
  same failure one level up: official uses 一番 2.1 per 10 k chars, and generated
  papers have run ten times that.
  Let the speaker mark the answer by **contrast** (「〜も大事ですけど、やっぱり…」)
  or by **conceding then correcting**, and vary it item to item.

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
from the script. This cell is what QA reads; if it is absent, the item is not
shippable.

Why an order and an artifact rather than the prohibition they replace:
"mentioned then eliminated" was already stated three times across two skill
files, always as a property to verify *after* both files exist — the last thing
an author does, in the last file authored, exactly where long-run degradation
lands. Nothing recorded whether the check ran, so skipping it was invisible,
and **4/4** papers shipped ungrounded options — the 解説 itself admits it.
`make check` WARNs when a 問題1/2 option shares no ≥2-char kanji/katakana token
with its item's script block — WARN only, because that heuristic flags 5/44 on
the *official* paper (official distractors are often paraphrased). The
mechanical check cannot tell "reassigned" from "never said"; the written
grounding line is what does.

## 問題3 (概要理解): the narration names the SETTING, never the topic

Official 問題3 item lines are 「1番 ラジオで女の人が話しています。」/「2番 講演会で
家具を作る職人が話しています。」/「3番 テレビでアナウンサーの男の人がお菓子屋の人に
インタビューしています。」 — setting plus speaker, and **nothing about what the
talk is about**, in every item of every sitting. The question 「何について話して
いますか」 is the whole task, so naming the subject in the lead-in answers it.

Generated papers have written 「ラジオで、専門家が◯◯の注意点について話しています。」
over a keyed option naming that same ◯◯ — i.e. the answer was read out before the
talk began. Write `N番。<場所>で、<話者>が話しています。` and stop. `make check`
fails a 問題3 item line carrying 「〜について」/「〜の話」.

## 問題3 (概要理解): the monologue must NOT mention the wrong options

In 31 official sittings, **no 問題3 monologue refers to its distractors at all**.
The four options are topic-level summaries of the same talk with a modifier
moved or a scope widened (7/2025 1番: 一人旅のよさ vs 一人旅をする寂しさ /
一人旅とグループ旅の共通点 / 一人旅の注意点 — 寂しさ appears only as something
*other people say*, and the other two never appear). The item is hard because
all four options are *about* the talk.

So the closing "denial sweep" — 「Xの話ではありませんし、Yについて論じているので
もありません。Zを取り上げているわけでもありません」 — is **forbidden**. It appears
**0 times in the archive**, and it has shipped in every item of a generated
問題3. It destroys the item twice over: it hands the answer to anyone who hears
the three negations, and it is not language a human speaker would produce. Write
the monologue as a talk that is only ever about ONE thing, then harvest three
near-misses from its own content. `make check` fails the formula outright, and
also fails a talk that mentions two or more of its own four options.

### 問題3 options are bare noun phrases — never suffixed 「〜について」

Official 概要理解 options are noun phrases and nothing else: 一人旅をするよさ /
木の家具の魅力 / 店をやる喜び / 米作りでのロボットの活用. **8 of 685 archive
options end in 「〜について」 — 1 %**; four of the last five generated papers ended
**all 24** of theirs that way. Two costs: the four options become
grammatically identical, so the set reads as a menu of subject headings instead
of four competing readings of one talk; and the suffix pushes each option past
the 10–15-char band below. Write the noun phrase and stop.

### The talk must be long enough to have a gist

Measured with one rule on both sides (the item block minus its lead-in, its
spoken choices and its question — `official_register.md` §7.4): official 問題3
talks run a **median of 305 spoken chars**, p10 251, **minimum 177** over 149
items; the papers run a median of **179**, longest 258. **41 % shorter than
official, and 34 of 40 items sit below the official 10th percentile.**

A 概要理解 talk of four sentences has no structure to summarize: the gist is
simply its last sentence, so the item degenerates into 沿って聞く rather than
全体をつかむ. **Target: 220+ spoken chars** — make the point twice in different
words, the way a real speaker circles back, which is what lets a 概要 question
have a defensible answer. `make check` FAILs below **175** (the archive minimum,
per its threshold policy), so passing the gate is not the same as hitting the
target.

## Spoken choice pacing

Options spoken in 聴解 must follow official lengths: **~10–15 chars per choice
in 問題3/問題4**.

## 統合理解 (問題5): two items, two DIFFERENT types

Shinkanzen's 問題紹介 defines 統合理解 as two shapes, and the archive uses **one of
each, every sitting**:

- **1番 — 2人以上の話し手の意見を整理しながら聞き取る.** A three-party discussion of
  a problem; the four options are ACTIONS harvested from the argument
  (7/2025: 開催日を変更する / ポスターを貼る場所を増やす / 会場を変更する /
  選手の人数を減らす). **3 speakers in every sitting since 2020.** Nobody reads a
  list — the candidates surface as proposals, and two of them are killed by the
  other participants.
- **2番 — ある話を聞いた後で、それについての意見や評価を聞いて判断する.** A third
  voice (ラジオ/アナウンス/講師) enumerates four candidates, **then** two listeners
  weigh them, and 質問1/質問2 separate the two listeners' picks (or day 1 / day 2).

The last five generated papers made both items the same item: two speakers, four
labelled candidates read out by one of them, eliminated one at a time. That is
問題1's task twice at double length, and it spends the paper's only 統合理解 slots
on 課題理解.

- **1番 must have ≥3 speakers and no menu.** Under two ja-JP voices that means
  `男1`+`男2`+`女` or `女1`+`女2`+`男`; `choukai-audio` Part 2 owns the casting and
  the pitch margins.
- **2番 must keep the heard-then-evaluated shape** — the enumerating voice is not
  one of the two deciders.
- **Rotate the 質問 pair across tests.** 「最初どう思っていたか／最終的にどうする
  ことにしたか」 has been the pair in **four consecutive papers**. Official rotates
  between each person's pick (男の人は／女の人は), 1日目/2日目, and 最初/結局.

## 問題5-2番 choices — spoken, not printed

**This repo prints nothing anywhere in 問題5**; 2番's four choices are read aloud
after 質問1 and again after 質問2. Official prints them instead — the divergence,
and why it was accepted, is owned by `jlpt-exam-structure` §"問題5 prints
nothing". Defer to it for the format spec (same four labels, same order, both
questions) and to `choukai-audio` for where they sit in the script block.

What is yours to get right when authoring the item:

- **Bare labels** (「夕日通り / にしがおか / さくら公園 / 東山」-style) — never full
  sentences, and never the deciding attribute riding along
  (`4、東山、商店街の近くで便利です。` is forbidden, exactly as
  `東山（商店街の近くで便利）` was when the list was printed). The item exists to
  test matching attributes *heard* in the dialogue to the labels; a choice that
  restates the attribute answers itself.
- **Spoken now means the labels must survive being heard once.** A printed list
  could be re-read; this one cannot. Keep the four short and phonetically
  distinct — four place names differing in one mora
  (「中央町 / 中央通り / 中山町 / 中野通り」) is a listening-discrimination item by
  accident, not 統合理解.
- **ONE set of four labels, read identically after 質問1 and after 質問2.**
  Official prints the same four under both questions — 7/2025 夕日通り /
  にしがおか / さくら公園 / 東山; 12/2024 第一会場〜第四会場; 12/2025 1番の自転車〜
  4番の自転車. `20260812_2` read four short labels after 質問1 and four ~20-char
  compound sentences after 質問2: two different sets, so the two questions stop
  sharing a candidate list and the item stops being 統合理解. Write the four once,
  then read that same block twice.
- The ~10–15-char-per-choice band under "Spoken choice pacing" above is for
  問題3/問題4 sentence options. 問題5 2番's are names: shorter is correct.

## 即時応答 (問題4)

### The stimulus must be spoken TO a specific person, never broadcast

A 即時応答 item only works if there is someone for the test-taker to answer
*as*. `20260811_1` shipped a `quick_response` pool phrase
(「館内では携帯電話のご利用をお控えください」) scripted with the speaker label
`アナウンス:` — a facility-wide PA broadcast with no addressee — matching the
skill's own automatic-fail precedent (a 火災報知器 prompt with no
addressee-reply; `exam-qa-review/SKILL.md`'s automatic-fail list). This is now
a **second shipped occurrence** of the same defect class.

**Never label a 問題4 stimulus line `アナウンス:` or `アナウンサー:`** — those
labels are for 問題3-style monologues only (`choukai-audio/SKILL.md`'s
`SPEAKER_MAP`), where no reply is expected. If a drawn `quick_response` phrase
reads as a public announcement, recast it as a specific staff member speaking
directly to the specific customer in front of them before scripting it (e.g.
`係員:お客様、館内では携帯電話のご利用をお控えください。`) — same tested
phrase/register, but now addressed to someone who can answer.

### The three replies must not be はい / いいえ / では

Measured over 1 113 official replies: **94 % open with content**, and only
1.3 % open with はい, いいえ or では combined. Generated papers have run over half
their replies on those three openers, plus 「まだ〜ていません」 four times as often
as official. When almost every 「まだ〜ていません」 option is a wrong answer, the
*shape* is the key: the item becomes solvable without hearing the prompt.

Write the three replies as three **stances** on the prompt instead: take it and
act, misread its tense or aspect, invert its polarity. Official shape (7/2025
4番, OCR — pattern only): prompt 「見てて、この定食。この量は食べきれないよ。」 →
`1 私、ちょっと食べてあげようか？` `2 他のも注文する？` `3 量、ちょうどいいんだ。`
Nothing announces yes or no; each reply commits to a reading of 食べきれない.
Reply length stays official (median 15 chars). `make check` WARNs when a paper's
問題4 exceeds the official rate of these openers.

### No reply SHAPE may be the key — the already-done trap

Fixing the はい/いいえ/では openers moved the tell instead of removing it. In
`20260813_2` **9 of 11** items carry a wrong reply shaped 「もう〜た / 済ませました
/ さっき〜ました」; `20260810_2` has 8 of 11. The archive averages **1.0 such item
in 11.4**. When every option that says もう is wrong, もう **is** the key and the
section scores without Japanese — the identical defect to the 「まだ〜ていません」
one, mirrored. `20260813_2` also keys a reply opening 「あ、」 in 5 of its 11 items.

Caps for a paper's 問題4 (12 items incl. 例):

- ≤2 items may carry an already-done (もう/すでに/さっき + 〜た) distractor;
- no other single shape — misread tense, inverted polarity, wrong addressee,
  answering a different question — may be the wrong answer in more than 2 items;
- the KEYED reply may open with 「あ、」 in ≤2 items.

Write the three replies as three stances (above), then list the 12 keys in one
column and the 24 distractors in another. **If either column can be sorted by
form, the section is broken** — that is the same column read the 構成表 demands
at the top of this file.

Tests idioms and keigo: 目を通す, お言葉に甘えて, 〜かと思いきや, 〜ようがない,
席を外しております, 在庫を切らしております. Invent the utterance's SETTING
yourself (office, store, phone call…); the tested keigo/idiom stays the
sampled one regardless of setting. The keyed reply must fit the speaker's
rank and keigo direction — core Item integrity #20.

**The keyed reply introduces no unstated premise.** The reply that advances the
dialogue (a suggestion, a consolation, a judgment) may only rely on what the
prompt states or directly implies; a key that presupposes a fact the prompt never mentions (an appointment, a prior arrangement) lets a second option that
answers the prompt as stated compete with it. That is a double-answer fail
(e.g., if the key's 「予約」 premise was never in the prompt, a plain sympathetic reply is equally natural). When the key needs
such a premise, put it in the prompt; otherwise pick a key the prompt grounds.
