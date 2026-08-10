# Official choukai REGISTER — the archive measured against generated papers

Companion to `official_pacing.md`. That file measures the **silence** between
words; this one measures the **words**. It exists because every generated paper
so far passed a green gate while sounding nothing like the official recording,
and the difference turned out to be countable.

Corpus: the 31 script extracts `refs/JLPT_N2_NEW/*/script.md` (321 558 chars,
3 215 dialogue turns) against the generated scripts in `tests/*/聴解スクリプト.txt`
(baseline: 27 020 chars, 321 turns, measured before this file existed). **The
official dialogue in those extracts is OCR**
(~98 % character-accurate): it is sound evidence for shape, rhythm, counts and
inventory, and it is **not** quotable as exact official wording
(`question-authoring/references/reading-reference-pdfs.md`). Every official
example below is an OCR-derived illustration of a *pattern*, never a phrase to
copy.

Turn = one speaker's uninterrupted speech, wrapped OCR lines rejoined.

---

## 1. The four countable gaps

| Measure | Official | Generated (baseline) | Ratio |
|---|---|---|---|
| turns that are short reactions (≤12 chars) | **18 %** (589/3215) | 6 % (19/321) | ⅓ |
| turns opening with a filler/reaction token | **35 %** (1131/3215) | 18 % (57/321) | ½ |
| hesitation tokens per sitting (あのう/えー/えっと/うーん/まあ/ええと) | **median 41** (range 13–70, present in 31/31) | 0–4 | ~0 |
| explicit denial 「〜ではありません」 per 10 k chars | **0.4** | 17.1 | **43×** |
| 問題3 "triple denial" close (Xの話ではありませんし…) | **0** in 31 sittings | 19.8/10 k — every item of a section | ∞ |
| 問題4 replies opening はい / いいえ / では | **1.3 %** combined | **57 %** | 44× |
| 問題4 「まだ〜ていません」-shaped distractors | 2 % | 8 % | 4× |

Turn LENGTH, by contrast, is already right — median 36 vs 32 chars, p90 94 vs
92, and unpunctuated runs median 9 / p99 32 on both sides. **The problem was
never sentence length; it is that the generated speakers never react, never
hesitate, and kill distractors by announcing that they are wrong.**

---

## 2. Inventories to draw from

### 2.1 Short reaction turns — official frequency

`はい。` 84 · `そうですか。` 33 · `わかりました。` 27 · `うん。` 19 ·
`はい、わかりました。` 11 · `そうなんだ。` 11 · `ありがとうございます。` 9 ·
`そうですね。` 8 · `あ、はい。` 7 · `そうだね。` 7 · `そうなんですか。` 7 ·
`わかった。` 6 · `そうか。` 6 · `なるほど。` 6 · `そう。` 5 ·
`よろしくお願いします。` 5

They are not filler in the wasteful sense: they are what makes the OTHER
speaker's turn land, and each one is a 0.9 s turn gap in the audio, which is
where the recording gets its breathing rhythm (see §4).

### 2.2 Turn-initial tokens — official counts (top 20 of 1131)

`はい` 268 · `うん` 223 · `ああ` 86 · `ええ` 85 · `あ、` 81 · `じゃ` 67 ·
`うーん` 61 · `あの` 48 · `へえ` 41 · `でも` 35 · `あのう` 34 · `えー` 24 ·
`いや` 24 · `まあ` 15 · `それが` 10 · `えっと` 9 · `ええと` 6 · `いえ` 5

Register split, from the same corpus: `うん / そうなんだ / だけど / 〜かな` are
casual (student, family, colleague); `はい / ええ / かしこまりました /
おっしゃる` are keigo (service counter, 部長, 医者). Mixing them inside one
speaker is the tell of a script written by a machine.

### 2.3 How official kills a wrong candidate — per 10 k chars

| Device | Official | Generated | Illustration (OCR, pattern only) |
|---|---|---|---|
| **deferred** — その前に / 先に / あとで / 後回し | 10.6 | 36.3 | 「資料の印刷、後回しになってました」 |
| **can't / won't** — 難しい / 無理 / 見送 / やめ | 3.5 | 6.6 | 「試合は難しいね。選手にもそんなことはお願いしてないから」 |
| **already done** — もう / すでに + 〜た | 1.9 | 1.3 | 「もうあんまり腫れてはいませんね」 |
| **reassigned to a named third party** | 0.4* | 0.0 | 「ホームページの更新は山下さんが引き受けてくれました」 |
| explicit 「必要ありません」/「しなくていい」 | 1.0 | 4.6 | — |
| explicit 「〜ではありません」 | 0.4 | 17.1 | — |
| 問題3 triple denial | 0 | 19.8 | — |

\* the regex only catches `〜さんが/に + 担当/引き受け/お願い`, so reassignment
is undercounted; read 7/2025 問題1-1番 and 2番 for how common it actually is.
The ORDER of the two columns is the finding: official prefers **reassign,
defer, refuse** — devices that leave the listener to work out that the option
is dead — and uses flat contradiction as a last resort. Generated papers invert
that.

### 2.4 問題4 replies — 1 113 official replies

- median 15 chars (generated: 15 — the one thing already right);
- **94 % start with content**, not with a yes/no/では token. Official openers:
  `あ` 3 % · `そう` 1 % · `うん` 0.6 % · `はい` 0.6 % · `いいえ`+`いえ` 0.5 %;
- the three replies of one item are usually three different *stances* on the
  prompt (agree-and-act, misread-the-tense, invert-the-polarity), not
  「はい」/「いいえ」/「では」;
- illustration of the official shape (7/2025 4番, OCR): prompt
  「見てて、この定食。この量は食べきれないよ。」 → `1 私、ちょっと食べてあげようか？`
  `2 他のも注文する？` `3 量、ちょうどいいんだ。` — no reply announces a
  yes/no; each one commits to a reading of 食べきれない.

A reply set of 「はい、〜」/「いいえ、まだ〜ていません」/「では、〜」 is
**solvable without hearing the prompt**: when almost every 「まだ〜ていません」
option is a wrong answer, the shape itself is the key. That is the defect this
inventory exists to prevent.

### 2.5 問題3 (概要理解) — official monologues never deny the other options

In 31 sittings, not one 問題3 monologue mentions the wrong options. The
distractors are topic-level summaries of the SAME talk with a modifier moved
(7/2025 1番: 一人旅のよさ vs 一人旅をする寂しさ / 一人旅とグループ旅の共通点 /
一人旅の注意点 — the talk mentions loneliness only as something *other people
say*, and never mentions the other two). What makes the item hard is that all
four options are *about* what was said; what made the generated items easy is a
closing sentence that names three of them and rejects each.

---

## 3. Banned formulas, with the count that banned them

| Formula | Official / 31 sittings | Generated (baseline) |
|---|---|---|
| 「Xの話ではありませんし、Yについて論じているのでもありません。Zを取り上げているわけでもありません。」 | 0 | every 問題3 item |
| 「〜た方がいいですか」 as the examinee's every turn | 0 | every 問題1 probe |
| 「かしこまりました」 as every service reply | 4 in 31 sittings | every service reply |
| 「わかりました。書きます。」 as an item's closing turn | 0 | reused across a section |
| 「なるほど、〜なんですね」 echo before the answer | rare | once per 問題2 item |
| 「一番」 in a 問題2 dialogue | 2.1/10 k | 24.1/10 k |

The per-formula ratios matter less than the shape of the failure: **a template
applied to every item in a section.** A shipped 問題1 ran
「すみません、〜んですが」 → 「かしこまりました。まず〜」 → two
「〜た方がいいですか」 probes, each refused → 「まずは〜をお願いします」 →
「わかりました。書きます。」 in every one of its items. A candidate who notices
that the last refused suggestion is never the answer scores the section without
Japanese.

---

## 4. Why this file is also an AUDIO file

`official_pacing.md` sets the gap between turns at 0.9 s. A section written
with official reaction density has ~40 % more turns per item, so the same
constant produces ~40 % more of those gaps — the "it just talks without
stopping" complaint is partly a *register* defect, not only a synthesis one.
Measured in a 7-minute dialogue window: official carries 86–100 within-turn
breath pauses (median 0.37–0.41 s), the generated baseline 69–70 (median
0.30 s). Half of that gap closes in the script, the other half in
`shape_pauses()`.

---

## 5. Where a rewritten paper should land

Scripts rewritten against §§1–3 and re-measured with the same rules. The gate
thresholds sit at or below the official minimum, so "inside the band" is the
target, not the official median:

| Measure | Baseline | Rewritten | Official | Gate |
|---|---|---|---|---|
| short reaction turns | 5–7 % | **12–14 %** | 18 % | WARN < 12 % |
| hesitation tokens per paper | 3–25 | **23–31** | median 41, min 13 | WARN < 13 |
| flat denials per 10 k chars | 10.5–16.0 | **2.3–3.1** | 1.4 | WARN > 6.0 |
| 問題4 replies opening はい/いいえ/では | 33–69 % | **0–11 %** | 1.3 % | WARN > 20 % |
| 問題3 denial sweeps | every item | **0** | 0 | FAIL |
| 問題3 lead-ins naming the topic | every item | **0** | 0 | FAIL |
| items sharing a closing turn | up to 3 in a section | **0** | 0 | FAIL |

Two rules came out of that rewrite and are now owned by
`question-authoring/references/choukai-items.md`:

- **問題3 lead-ins name the setting and the speaker, never the topic.** Generated
  papers wrote 「ラジオで、専門家が◯◯の注意点について話しています」 over a keyed
  option naming that same ◯◯ — the answer was spoken before the talk began.
  Official says 「ラジオで女の人が話しています。」 and stops.
- **A 問題3 talk must not name its own distractors.** A phrase blacklist is not
  enough: one paper wrote 「〜を主に論じているのではありません」 and passed it. The
  gate now counts how many of the item's four options the talk mentions and
  fails at two or more.

## 6. Reproducing this

```
turns       rejoin wrapped OCR lines between speaker tags; drop 問い/質問/★ lines
short turns len(turn) <= 12 chars
openers     turn.startswith(token) over the §2.2 token list
devices     regex per row of §2.3 over the joined turn text, per 10 k chars
問題4        replies = ^[1-3]\s*(.+)$ inside the 問題4..問題5 span
```

The measurement script is not committed (one-shot analysis over `refs/`), but
every number above is reproducible from those five rules in a few lines of
Python. Re-measure after adding sittings; do not re-derive from one paper.
