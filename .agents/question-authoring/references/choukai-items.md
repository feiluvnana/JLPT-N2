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

## Spoken choice pacing

Options spoken in 聴解 must follow official lengths: **~10–15 chars per choice
in 問題3/問題4**.

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
