# 聴解 items — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — sniff test, item integrity (the 解説 verbatim-quote rule
and the 即時応答 keigo-direction rule are #19–20 there). Script FILE format and
audio pacing are owned by `choukai-audio`; booklet printing conventions
(問題5-2番 labels, instruction wording, 例 mechanics) by `jlpt-exam-structure`.

## Every wrong option is MENTIONED, then ELIMINATED

For 問題1, 問題2, and 問題4/5, every wrong option must correspond to a real
task/statement/fact from the audio that is **reassigned, superseded, denied, or
reinterpreted** (already done / rejected / 「それが理由ではありません」) — never
invented from nothing. An option nobody says is not a distractor, it is
fabricated noise, and it lets the item be solved without tracking the
conversation. For **問題3 (概要理解) only**, official distractors are
topic-level summaries or general statements with key modifiers missing/altered.

**An option that is raised and left TRUE is a second answer**, even if it is
"only a contributing factor": test 1's 遅刻理由 item affirmed 道が混んでいた in
the audio while keying USB忘れ. A どうして item's wrong causes must be denied,
not merely outweighed.

課題理解 (問題1) hides the correct FIRST action behind 「その前に」「それが先」.

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
and **4/4** papers shipped ungrounded options (t1 問題2-1番 options 2 and 4 —
the 解説 itself admits it; t2 five options across 4 items; t3 ~14 options, with
問題2-2番's three wrong options all fabricated; t4 問題2 例 option 2).
`make check` WARNs when a 問題1/2 option shares no ≥2-char kanji/katakana token
with its item's script block — WARN only, because that heuristic flags 5/44 on
the *official* paper (official distractors are often paraphrased). The
mechanical check cannot tell "reassigned" from "never said"; the written
grounding line is what does.

## Spoken choice pacing

Options spoken in 聴解 must follow official lengths: **~10–15 chars per choice
in 問題3/問題4**.

## 問題5-2番 printed options

Official papers print **bare labels** for the four choices (「夕日通り /
にしがおか / さくら公園 / 東山」-style) — never full sentences and never the
deciding attributes (`東山（商店街の近くで便利）` is forbidden): the item exists
to test matching the attributes *heard* in the audio to the labels. The printed
format spec (same four labels, same order, for 質問1 and 質問2) is owned by
`jlpt-exam-structure` — defer to it.

## 即時応答 (問題4)

Tests idioms and keigo: 目を通す, お言葉に甘えて, 〜かと思いきや, 〜ようがない,
席を外しております, 在庫を切らしております. When the spec carries
`qr_situation_seeds`, the seed flavors only the SETTING of the utterance; the
tested keigo/idiom stays the sampled one. The keyed reply must fit the
speaker's rank and keigo direction — core Item integrity #20.
