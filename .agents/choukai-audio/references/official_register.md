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
| hesitation tokens per sitting — **corrected, see §7.1** | **median 27** (range 9–48), gate token list | 0–4 | ~0 |
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
| hesitation tokens per paper | 3–25 | **23–31** | median 27, min 9 (§7.1) | WARN < 9 **and > 48** |
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

---

## 7. Re-measurement 2026-08-13 — the register rules worked, and the tells moved

Re-run of §§1–3 over the same 31 `script.md` extracts, now against **8** shipped
papers (`tests/*/聴解スクリプト.txt`, 1 217 turns) instead of the original
baseline. Two things came out of it: one number in §1 was wrong, and every
measure §1 counts is now inside the band while **five measures it does not count
are outside it**. The pattern is the finding — a counted tell gets fixed and an
uncounted one grows in its place, so the rules below are written as
**distributions with caps**, not as phrase bans.

### 7.1 The hesitation figure was wrong (and its floor was above the archive)

§1 claimed "median 41 (range 13–70, present in 31/31)". It does not reproduce:

| Token list | Official median | Official range |
|---|---|---|
| the six §1 names (あのう/えー/えっと/うーん/まあ/ええと) | **10** | 1–28 |
| `check_consistency.py`'s `FILLERS` (adds あの、/あ、/ああ、/まあ、) | **27** | **9–48** |

Neither is 41, and the "never fewer than 13" half is false under both: 12/2024
and 7/2025 measure **9**, 12/2025 measures **11**. The gate's floor of 13 was
therefore set *above* three sittings — including both 2025 papers — which
contradicts this file's own stated policy ("thresholds sit at or below the
official minimum"). Floor corrected to **9**.

Caveat that applies to every filler count here: the official side is OCR, which
drops some 「あ、」. It is the same source the original figure came from, so the
comparison is sound; the absolute official value may run slightly low.

**A ceiling was missing, and the papers went through it.** Shipped papers now
measure **23–58** — `20260812_1` at 58 is above the official maximum of 48 and
`20260813_1` at 44 is above the official median. Composition is off in the same
direction: per paper, official carries `うん` **11.3** and `あ、` **12.9**;
the papers carry `うん` **4.2** and `あ、` **22.5**. They hesitate more than
official while *acknowledging* less. WARN band is two-sided: **9 ≤ fillers ≤ 48**.

### 7.2 What §1 counts is now fixed

| Measure | Official (pooled) | Papers (pooled) | Verdict |
|---|---|---|---|
| short reaction turns (≤12 ch) | 14.7 % (475/3 227) | 14.4 % (175/1 217) | inside |
| 問題4 replies opening はい/いいえ/では | 1.3 % | 0–11 % | inside |
| flat 「〜ではありません」 /10 k | 0.4 | median 0.55 | inside |
| turns opening with a filler/reaction | 44.4 % | 32.0 % | short, improving |

The 18 % / 35 % figures in §1 come from a different turn-splitting pass than the
§6 rule produces (§6 rejoins OCR wraps and drops 問い lines; that yields the
pooled 14.7 % / 44.4 % above on the same corpus). **The discrepancy is not
resolved** — do not treat either pair as authoritative until one parse owns the
number. The gate's 12 % floor sits below both, so nothing depends on it today.

### 7.3 Five uncounted tells, all outside the archive

Each row is now a rule with a cap; the rule text is owned by
`question-authoring/references/choukai-items.md` §"Section item mix".

| Measure | Official | Papers | Worst paper |
|---|---|---|---|
| 問題1 items set at a service counter | **6 %** (9/153) | 42 % (17/40) | `20260813_2` 5/5 |
| 問題2 items keyed by 「一番/優先」 | **6 %** (8/141) | 52 % (25/48) | `20260810_1`, `20260813_2` 5/6 |
| 問題2 items keyed by どのように | 18 % (25/141) | 2 % (1/48) | — |
| 問題4 items with a もう/済/さっき already-done distractor | median **1**, max **3**, of 11.4 | — | `20260813_2` 9/11, `20260810_2` 8/11 |
| 問題3 options ending 「〜について」 | **1 %** (8/685) | 60 % (116/192) | 24/24 in four papers |
| 問題3 talk length, spoken chars (§7.4 rule) | median **305**, p10 251, min **177**, max 709 (n=149) | median **179**, max 258 | 34 of 40 items below official p10 |
| 問題5 items with ≥3 speakers | 1番 3-party in **every** sitting since 2020 | 0 in the last 5 papers | — |
| consecutive same-speaker turn pairs | **0** (max 1, an OCR wrap) | 0 in 6 papers | **`20260813_2`: 9** |
| 「まず」 inside 問題1 dialogue /10 k | median **5.5** (0–19.1) | 4.1–36.3 | `20260807_1` 36.3 |
| 一番 token /10 k | median **1.8** | median 10.25 | `20260810_1` 21.2 |

Two of these need reading, not just counting:

- **The same-speaker split is a gamed metric, not a style slip.** All 9 pairs in
  `20260813_2` are a short turn placed immediately before a long turn *by the
  same speaker* (「職員:ありがとうございます。」 / 「職員:手数料の…」;
  「係員:承知しました。」 / 「係員:もちろんです。…」; also 「先生:なるほど。」, itself a
  banned formula). They lift that paper's short-reaction share to the 15 % its QA
  report credits as fixed — it is **12.2 %** without them. In the audio each one
  also buys a 0.9 s `GAP_BETWEEN_LINES` where official has a ≤0.5 s within-turn
  pause, so the metric was satisfied by an artifact the metric cannot see. Rule:
  one turn is one line (`choukai-audio` §"Block conventions").
- **問題5 lost the two-type structure**, which no token count would ever show.
  Shinkanzen's 問題紹介 defines 統合理解 as two shapes and the archive uses one of
  each per sitting; the last five papers used the enumerate-four-candidates shape
  for **both** items. Rule and evidence: `choukai-items.md` §統合理解.

### 7.6 The WRITING itself, measured 2026-08-14 (Shin Kanzen 実力養成編)

§§1–3 measured how often speakers react and how options get killed. This pass
measured the sentences — against the three 実力養成編 chapters that name what N2
listening actually tests. Same corpora (31 sittings / 8 papers), spoken text
only, speaker tags stripped.

**(a) 縮約形 — Shin Kanzen I-2, p.16.** The book opens 実力養成編 with a table of
contracted forms because parsing them is the skill. Per 10 k spoken chars:

| form | official | ours | ratio |
|---|---|---|---|
| 〜てる / 〜でる | 29.6 | 9.3 | 0.31× |
| 〜とく / 〜どく | 1.8 | 0.2 | 0.12× |
| 〜なきゃ / 〜なくちゃ | 2.3 | **0.0** | 0 |
| 〜ちゃう / 〜じゃう | 5.2 | 2.4 | 0.47× |
| って | 92.4 | 64.5 | 0.70× |
| 終助詞 よ / な / ね | 29.5 / 11.1 / 65.7 | 16.8 / 5.5 / 48.8 | 0.57× / 0.50× / 0.74× |

Combined (the six-form regex the gate uses): official **37.3 per sitting
[22.4–67.4], n=31**; ours 0.0 / 1.5 / 3.8 / 6.4 / 11.1 / 15.8 / 18.0 / 23.9 —
**seven of eight below the archive minimum**, one paper at zero.

The obvious explanation is wrong. Split by whether an item has a service-role
speaker (店員/職員/係員/担当者/…), where keigo would suppress contractions:

| | official | ours |
|---|---|---|
| items WITH a service-role speaker | 37.5 | **8.4** |
| items WITHOUT one | 45.5 | **13.2** |
| share of items with one | 10 of 378 (2.6 %) | 53 of 104 (51 %) |

Official keeps contracting at a counter; our casual items are still 3.4× below
official's casual items. It is a writing habit
(「〜ています」「〜ておきます」「〜なければなりません」), not a consequence of setting —
though the last row is independent corroboration of §7.3's 問題1 setting quota,
on a cleaner denominator.

**(b) 言い換え — Shin Kanzen IV-2, p.52.** 「選択肢では、話の中の長い説明を、別の
言い方で簡単に短くまとめている」「2人の話を1つにしている場合もあります」. Measured
within our corpus only: of 53 keyed 問題1/2 options, **40 (75 %) have every
2-char kanji/katakana token already present in their own script block**. Worked
official contrast, 7/2025 問題2-1番: 「そこに入りたいんだ」 → key 「しゅっぱんしゃで
働く」.

*No official percentage is given on purpose.* Official booklet options are
kana-leaning (see (d)), so matching their tokens against a kanji script
understates their overlap and would fabricate a flattering gap. Ours is an
absolute against a rule the book states.

**(c) 間接的な答え方 — Shin Kanzen II-2-B, p.29.** Replies that are questions:
official **13 %** of 973; ours **0 of 264**. Keyed replies opening with an
explicit acceptance marker: ours 15 %. Per sitting, official question-replies
range **0–15, median 4** — so the archive minimum is 0 and this cannot be gated
at the usual threshold; it stays a reading task.

**(d) Option orthography.** 297 official 問題1/2 options: mean kanji ratio
**0.298**, 32 % above 0.35. Our 416: **0.472**, 73 % above 0.35, every paper
denser than any official sitting that parses. Owner and reasoning:
`jlpt-exam-structure` §"Printed options are kana-LEANING". Per-sitting
distribution is NOT measured — only 2–6 of 31 `booklet.md` extracts expose their
listening option blocks to a parser, so no per-paper threshold is defensible
until `extract_jlpt_n2_new.py` reads those pages reliably.

### 7.4 Reproducing §7

Same five rules as §6, plus:

```
問題1 setting   CUST = 窓口|受付|フロント|レジ|店で|店に|店員|客|電話をかけ|問い合わせ|カウンター
問題2 q-type    over 問い lines (official) / each item's repeated question (ours),
                one per item: 理由 | 一番・優先 | どのように | 何・どれ
問題4 shape     per item, any NON-KEYED ^[1-3]、 matching もう|すでに|既に|さっき
問題3 options   ^[1-4]、(.+) inside the 問題3..問題4 span; suffix test on 「について」
問題3 talk      item block minus lead-in, minus ^[1-4]、 lines, minus the
                question line, minus speaker tags; count non-space chars
問題5 voices    distinct speaker labels per item block; a paper passes if ANY
                item has >=3 (31/31 sittings do)
same-speaker    two consecutive speaker-tagged lines with an identical label
まず            count in the 問題1 span with the question lines removed
```

Scored items only on both sides, throughout: official script PDFs usually omit
the 例, so counting ours with the 例 included overstates every per-section share
by a sixth. The earlier "問題3 median 257" figure in this file came from a
speaker-tag-only parse that silently dropped official monologues written without
a tag; the §7.4 rule above is parser-independent and gives 305.

### 7.5 What is gated, and what a green gate does not mean

`tools/check_consistency.py` §G16 gates the countable half at the archive's
outer edge, never at its median:

| Gate | FAILs at | Class |
|---|---|---|
| a section keying two items to the same thing | any | FAIL |
| 問題3 options suffixed 「〜について」 | > 2 per paper | FAIL |
| 問題3 talk length | any scored item < 175 | FAIL |
| 問題4 already-done distractors | > 3 items | FAIL |
| 問題5 items with ≥3 speakers | 0 | FAIL |
| two consecutive lines, one speaker label | any | FAIL |
| セクション構成表 covering every scored item | missing rows | FAIL |
| 問題1 counter share, 問題2 question mix, 問題3 genre, keyed 「あ、」, まず rate | the quotas | WARN — QA settles them |

The eight papers on disk on 2026-08-13 are exempt BY NAME
(`CHOUKAI_SECTION_GRANDFATHERED`) because all of them predate these rules and
every one lacks the 構成表; their breaches print as WARN lines carrying the same
measurement a FAIL would. Remove an id when its 聴解 is repaired. **A green G16
means no official sitting looks this bad — not that the section is
official-shaped**; the authoring targets are tighter and live in
`question-authoring/references/choukai-items.md` §"Section item mix".
