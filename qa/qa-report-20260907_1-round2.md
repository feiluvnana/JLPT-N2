# QA report — 20260907_1, ROUND 2 (adversarial pass, `exam-qa-review`)

Reviewed revision (sha1[:12] over raw bytes):

- `言語知識・読解.md` = `24fa4608e0b2` (round 1 read `8b2913e47172`)
- `聴解.md` = `40cc36e44e6a` (round 1 read `38168cfa331c`)
- `聴解スクリプト.txt` = `f458d9d2e216` (round 1 read `693c4fe9b322`)

All three sources moved since round 1 — the repair round landed. Reviewer:
fresh-eyes context, authored nothing, repaired nothing, is not the round-1
reviewer. Timestamp: 2026-09-08. Round 1's report (`qa-report-20260907_1.md`)
is treated as a RECORD and was not edited.

Entry condition when this pass began: `make check` per-test block **203 ok /
2 skip / 2 WARN**, plus one repo-wide FAIL (the un-uploaded `聴解.mp3`,
deferred to the coordinator by instruction). **That state did not hold:** a concurrent
session edited `言語知識・読解.md` twice during the pass, which put the per-test
block into a **FAIL** (built HTML predating its Markdown) for about three
minutes before the same session rebuilt it. As of my final gate run the block is
green again apart from the two descoped 聴解 WARNs. §4B has the account; §9 has
every WARN and FAIL with its resolution.

**Sources read.** The revision above (`24fa4608e0b2`) is what
`qa/20260907_1/keyless.md` was built from and what §3 and §6 were written
against. `言語知識・読解.md` subsequently became `acc50cca3281` (16:30) and then
`00d5c0ef1607` (16:43); **every load-bearing measurement in this report was
re-run against both and holds** (§4B). `聴解.md` and `聴解スクリプト.txt` never
moved.

> **This report is written incrementally**, section by section, as each
> measurement completes — a prior run of this pass was lost to a rate limit
> with the whole report unwritten.

---

## 1. Verdict

**QA: FAIL (3 findings, 0 automatic) — and the verdict does NOT turn on the
descoped 聴解 half.**

> **Scope, as instructed mid-pass:** 聴解 optimization is descoped — the choukai
> machinery is being reworked, so tuning it here is wasted work. Dropped and
> recorded in one line each in §4A: the pause-distribution WARN, the 問題2-1番
> key-paraphrase WARN, deferred items 2/3/4, and claim R-2. **Kept, as
> correctness rather than optimization:** the blind solve of all 30 聴解 items and
> every 聴解 key against `answer_positions` (clean — §2), any outright key leak
> (none — §4A), and the whole 読解 / 文法 / 文字・語彙 side unchanged.
>
> **All three findings below are on the KEPT half** (two 読解, one 文法), plus one
> gate defect. Descoping 聴解 does not move the verdict: if every 聴解 item were
> declared perfect today, this paper would still be a FAIL.

Round 1's F1 automatic fail is **genuinely closed** — verified by my own
measurement across three successive revisions of the file, not by reading the
repair's claim (§3 R-1). Eleven of round 1's twelve findings are closed, F11
included (it was closed by a concurrent session at 16:30 and I verified both its
band records against the tracked extracts). The tick-off table is §7.

| id | finding | tier | mechanical or authoring? |
|---|---|---|---|
| **R2-F1** | 問題10(5) and 問題11(4) closings landed on ONE skeleton (`〜ていない`) AND one label (意外な観察) — the only paper of 34 on disk at 2; **all ten official sittings at 0**. Repair collateral of round-1 F1 | 要修正 | **authoring decision** — which of the two is re-closed, and onto which shape |
| **R2-F5** | 問題10-55's key is a **22-char verbatim lift** of the notice's own sentence (79 % of the option); 問題11-57 trips the second prong at both boundaries (LCS 15, 50 %). Corpus maximum; **all ten official sittings measure 0** | 要修正 | **authoring** — re-paraphrase two options |
| **R2-F6** | 問題8-47's 解説 still says 「文頭に固定」 of a card standing at blank 1, not 文頭 — round 1 wrote this repair into its walkthrough and it was not applied | 要修正, minor | **mechanical** (one phrase) |
| ~~R2-F8~~ | **OBSERVED, THEN SELF-CLEARED — not counted.** For part of this pass `言語知識・読解.html`/`解答.html` (16:34:03) predated `言語知識・読解.md` (16:43:04) and `make check` FAILed on it — the skill's automatic-fail class *HTML predating its Markdown*. The concurrent session rebuilt at 16:46:41 and the gate now reports `ok: built HTML matches the Markdown it stamps`. **Struck from the count; the concurrency hazard behind it is filed as a root cause in §8** (§4B) | — | — |
| **S-1** | `check_verbatim_keys` is crippled by `SequenceMatcher`'s `autojunk` default and has been **inert on every paper on disk** — it reports LCS=3 where the true run is 22 | `GATE-WRONG` | gate fix, out of QA's scope to apply (`tools/`) |

**Nothing was repaired.** §11 says why: R2-F1 and R2-F5 need authoring
decisions, and R2-F6 is one phrase not worth a lone booklet rebuild while two
findings stay open.

Adjudicated and **NOT** findings, each with the measurement: the 読解 key
count↔process axis (§3 R-3) and two candidate closing skeletons that failed the
official-fairness test (§3 R-1b).

---

## 2. Blind-solve diff

**Solved from `qa/20260907_1/keyless.md`** (975 lines, rebuilt at 14:35 from the
three shas in the header above), and from nothing else. All 101 items answered
before any keyed source was opened; 聴解 solved from the embedded
`聴解スクリプト.txt`.

```
python3 tools/qa_eval.py tests/20260907_1 --answers "[101 answers]"
  Total Scored Items : 101
  Agreement with Key : 101 / 101 (100.0%)
  Discrepancies      : 0
```

**Zero mismatches**, independently of round 1's zero. The repairs moved five
読解 keys, two 問題7 stems and seven 聴解 items, and the paper still solves
cleanly: no mis-key, no unanswerable item, no 例 that fails to support its
announced number, no second answer a solver actually lands on.

This is evidence about correctness only. Every finding below is a
predictability or repetition defect — the class a 100 % blind solve cannot
rule out.

### The two mandatory blind STRATEGY passes (問題10–13, 18 items)

Both scores, and the owning script's figures, are in §9.

---

## 3. Independent verification of the three claims the repair round rests on

### R-1 — claim: the F1 predicate family is genuinely 0/13 in the SHIPPED finals

**VERIFIED, and stronger than claimed.** I re-measured from scratch rather
than re-running round 1's numbers: `dokkai_closing_scopes()`'s thirteen
surfaces, （注N） definition lines stripped, each surface's **final two
sentences**, two independent marker families.

Narrow family (round 1's stated regex):
`を?決めて(いる|います|いた|いました)｜を決め[てるた]｜分けて(いた|いる)｜を分けて｜作って(いた|いました)｜によって…(変わ｜入れかわ｜決ま)｜次第(で｜である)｜にかかって(いる)`

Widened family: the above **plus** `左右して｜決定づけ｜決め手｜によるところが大き｜を生んでいる｜生んでいた｜が…を?支えて｜で決まる｜で決まって`.

| paper | narrow | widened |
|---|---|---|
| **20260907_1 (this paper, post-repair)** | **0/13** | **0/13** |
| 20260907_1 (round 1's pre-repair reading) | 6/13 | 6/13 |
| 20260827_1 | 3/13 | 4/13 |
| 20260818_1 | 3/13 | 3/13 |
| 20260807_1, 20260813_2 | 2/13 | 2/13 |
| 20260812_1, 20260817_1, 20260819_1 | 1/13 | 2/13 |
| 20260810_1, 20260813_1, 20260827_2, 20260828_1 | 1/13 | 1/13 |
| 20260817_2, 20260904_1 | 0/13 | 1/13 |
| 11 other generated papers | 0/13 | 0/13 |
| **imported-n2-2024-07** | **1/13** (問題10(1)) | 1/13 |
| the other nine official sittings | 0/10–0/13 | 0/10–0/13 |

Two corrections to round 1's arithmetic, neither of which changes its verdict:
official is **not** 0/13 across all ten — `imported-n2-2024-07` 問題10(1)
carries one hit; and 20260827_1 measures 3/13 narrow on my scope, where round 1
recorded 2/13. Direction and magnitude hold: the paper went 6 → 0 and is now
the joint cleanest reading on disk.

Seven closings were rewritten, not six. Round 1's F1 table named six
(問題9, 11(2), 11(3), 11(4), 12(B), 13); its walkthrough row for item 56 named
問題10(5)'s 「時刻を決めるほうは、店では買えない。」 as a seventh. All seven strings
are at **0 occurrences** in the shipped `言語知識・読解.md`:

```
grep -c で その日の味の入り方を決めている      -> 0   (問題9)
grep -c 運行の間隔によって重さが入れかわる      -> 0   (問題11(2))
grep -c 読まれるかどうかを分けていた            -> 0   (問題11(3))
grep -c という言葉が二年を作っていた            -> 0   (問題11(4))
grep -c あの半年が、いまの置き場所を決めています -> 0   (問題12(B))
grep -c 三人分の助けになるかどうかを決めている   -> 0   (問題13)
grep -c 時刻を決めるほうは、店では買えない       -> 0   (問題10(5))
```

*(verification command output pasted in §6.)*

### R-1b — but have the seven rewritten closings converged on a NEW shared shape?

**PARTLY YES — this is R2-F1.** §5's repair-collateral rule says to treat every
round-1 repair's landing site as in scope, so I read the thirteen finals down
three columns: the shape LABELS, the gate's `FINAL_SENTENCE_TEMPLATES`, and my
own skeleton reading.

The thirteen final sentences as shipped:

| surface | label (`logs/topics.json`) | final sentence |
|---|---|---|
| 問題9 ★ | 説明 | 切り口をのぞけば、管が残っているか断たれているかは、目で見て確かめられる。 |
| 問題10(1) | 随筆 | すぐ見られる形に整理したつもりで、私は写真を見る時刻のほうを暮らしから消してしまっていた。 |
| 問題10(2) | 随筆 | …今年の春に気づいたのは、こちらの手順が一つずつ要らなくなっていくという成長のほうだった。 |
| 問題10(3) | 実用文・分類外 | ご返事をいただければ幸いです。 |
| 問題10(4) | 実用文・分類外 | 放送はいたしませんので、心配な方は明るいうちにお集まりください。 |
| 問題10(5) ★ | 意外な観察 | 引き返す時刻は、どの店にも置い**ていない**。 |
| 問題11(1) | 主張 | …そこを確かめずに配り続けても、庭のすみに置きものをふやしているだけになります。 |
| 問題11(2) ★ | 説明 | 時刻表を作る側は、この二つの路線に同じ物差しを当てることができない。 |
| 問題11(3) ★ | 条件提示 | 前の号の話に決着（注4）をつけた号ほど、読者からの返事は多くなっていました。 |
| 問題11(4) ★ | 意外な観察 | 気づけば二度目の春が来ていて、いちばん会いたい相手とはまだ会え**ていない**。 |
| 問題12(A) | 反論応答 | 買う順番を、生活の後ろに回すという話である。 |
| 問題12(B) ★ | 反論応答 | 半年おくれて置いた机は、十年たったいまも同じところにあります。 |
| 問題13 ★ | 主張 | それだけで、送った三人はようやく三人に近づく。 |

★ = rewritten by the F1 repair.

**Column 1, labels:** 説明2 / 随筆2 / 実用文・分類外2 / 意外な観察2 / 主張2 /
条件提示1 / 反論応答2 — all ≤2, closed vocabulary respected, and every label
re-read against its own closing (I judge 問題11(2)'s 説明 the weakest of the
thirteen — 「同じ物差しを当てることができない」 reads as a practitioner's 主張 —
but 説明 is defensible as the explanation's own conclusion, and moving it to
主張 would put 主張 at 3, so the label as recorded is the better of the two).

**Column 2, `FINAL_SENTENCE_TEMPLATES`:** one hit across thirteen finals
(問題10(2), 分裂文). Cap 2. Compliant.

**Column 3, skeletons — three candidate convergences, measured over all 24
generated papers and all 10 official sittings before filing any of them**, per
§5's refuted-metric discipline:

| candidate skeleton | 20260907_1 | generated max | **official max** | verdict |
|---|---|---|---|---|
| **A. final ends `〜ていない`** | **2/13** | **2/13 (this paper alone; next is 1)** | **0/13 — all ten sittings** | **SURVIVES → R2-F1** |
| B. final ends on a potential form (られる/できる/…) | 2/13 (問題9, 問題11(2)) | 2/13 (20260813_2) | **2/13** (12/2024 問題12(A)+(B)) | **REFUTED** — official reaches the same number, so it fails a real sitting |
| C. final ends on a negation of any form | 3/13 | 6/13 (20260811_1) | 2/13 (2023-07) | **REFUTED** — three papers tie at 3, and the three sentences share only polarity, not skeleton (negative existential / negative potential / negative perfect); n is 13, so one reclassification moves it by 8 points |

Candidate A is the one that survives all three fairness tests the skill demands:
reproducible, separates this paper from every other of the 34 on disk, and
fails no official sitting. Exact run, with the predicate anchored to the
sentence end (`てい(ない|ません)。?\s*$`):

```
20260907_1            2/13   問題10(5) + 問題11(4)     <-- the ONLY paper at 2
20260828_2            1/13   問題12(B)
20260903_1            1/13   問題11(1)
31 other papers       0
ALL TEN OFFICIAL      0/10 – 0/13
```

**A methodological note on my own first attempt, because it changed the answer.**
My first pass used `てい(ない|ません)|ておりません。?\s*$`, in which the `$` binds
only to the last alternative, so the first branch matched 〜ていない **anywhere**
in the final sentence. That inflated the corpus (nine generated papers and
`imported-n2-2024-07` appeared at 1) and would have put an official sitting on
the board. The anchored predicate is the one the finding rests on, and it is
also the one the proposed check must use. Recording the error rather than the
tidy number: an unanchored regex is exactly how `check_note_band` ran for three
papers on ten false positives (§6.5, R3-10).

It is filed as R2-F1 below.

### R-3 — claim: the 読解 keys no longer cluster on the count↔process axis

**VERIFIED on the substance, and here is the full 20-key column the build step
did not build** (it read at most 4 of 20 and offered judgement). Round 1's
proposed procedure: label each key with the AXIS it chooses on, finding above
8 of 20 on one axis.

First, **which key TEXTS actually moved.** No key DIGIT moved — all 20 answer
positions are identical to round 1's walkthrough, as `answer_positions` requires.
Five key option TEXTS were re-written, and they are exactly the five round-1 F1
named as restating a closing:

| item | round 1's key text | shipped key text |
|---|---|---|
| 60 | 運行の間隔によって…重さが変わってくる | 一時間に一本の路線では、遅れがそのまま待ち時間として残る |
| 62 | 伝えた事がらの行方まで伝えるかどうかで分かれる | 読者は知らせそのものより、その先の話を待っているということ |
| 64 | いつでも会えるという安心が、日程を決める動きを弱める | いつでも会える相手とは、次に会う日を約束しないまま別れてしまう |
| 65 | …過ごした時間が、置き場所を決めていく | その部屋でしばらく暮らしてから買った家具は、あとから置き直さずに済んだ |
| 69 | 受け入れる側の用意がなければ助けにはならない | 応援を受ける課は、来た人が最初にとりかかる仕事を先に書き出しておくべきである |

None of the five is a lift of its surface's NEW closing (measured in §3 R-1b's
neighbourhood; the closest is 69 at a 9-char run 「応援を受ける課は、」, which is
the passage's own subject noun, not its reasoning).

**The axis column, all 20 keys, re-derived from the shipped text:**

| item | key | axis it chooses on | direction |
|---|---|---|---|
| 52 | 見るための時間が暮らしから消えた | object/count ↔ **time** | process |
| 53 | 親のする手順が要らなくなる形でも表れる | measurement ↔ **process** | process |
| 54 | 区画を…通路の奥へ移してほしい | — (実用文 request) | — |
| 55 | 町内会の判断で早めに開ける | — (実用文 fact) | — |
| 56 | 引き返す時刻を決めていない人が多かった | object ↔ **time** | process |
| 57 | 減った家庭は、配布先の一部にとどまっていた | **count** ↔ process | **count (reverse)** |
| 58 | 配る前に水の使い道が決まっているかを確かめる | count ↔ **preparation** | process |
| 59 | 新しい時刻表を見て、発車の少し前に着くよう出かける | **mechanism** | process |
| 60 | 一時間に一本の路線では、遅れがそのまま待ち時間として残る | — (which-case contrast) | — |
| 61 | その後どうなったかを伝えた号 | **appearance ↔ substance** | (other axis) |
| 62 | 知らせそのものより、その先の話を待っている | **appearance ↔ substance** | (other axis) |
| 63 | 親しくない相手のほうが、会えた人数は多くなっていた | **count** ↔ process | **count (reverse)** |
| 64 | 次に会う日を約束しないまま別れてしまう | **mechanism** | process |
| 65 | しばらく暮らしてから買った家具は、置き直さずに済んだ | amount ↔ **order/time** | process |
| 66 | Aは買い直しの少なさ、Bは居場所が分かった経験 | — (two-text comparison) | — |
| 67 | 何をすればよいか分からないまま、立って過ごしていた | — (fact lookup) | — |
| 68 | 道具の置き場も次の手順も分からず、聞ける相手もいなかった | — (指示語 restatement) | — |
| 69 | 来た人が最初にとりかかる仕事を先に書き出しておくべき | count ↔ **preparation** | process |
| 70 | 折りたたみのいす | — (constraint match) | — |
| 71 | あすまでに電話…五百円を現金で払う | — (constraint match) | — |

**Count: 8 of 20 in the process direction** (52, 53, 56, 58, 59, 64, 65, 69),
**2 pointing the other way** (57, 63), 2 on appearance↔substance (61, 62 — and
those two are the SAME passage, where a 事実+考え pair is structurally required),
8 on no axis at all.

**Verdict: the cluster is NOT closed, but it is no longer decisive, and round 1's
own threshold is not breached.** Round 1 counted 10; I count 8 on the same axis
over nearly the same keys, and its proposed rule fires *above* 8. Two
observations that matter more than the tally:

1. **The strategy is no longer a free ride.** With 57 and 63 keyed the OTHER way,
   a candidate who blind-applies "prefer the process/time/preparation option"
   scores 8 right and 2 wrong on the 10 items where the axis exists — and must
   first correctly spot which items those are. Over all 20 items that is 40 %,
   below the 45 % bar, and the two mandatory mechanised strategies both pass
   (§6).
2. **Round 1's 8-of-20 threshold is not reproducible enough to be a gate**, and
   I say so rather than adopt it silently: the same 20 keys read 10 by one
   reviewer and 8 by another, on judgement calls about items 60, 62 and 68. Per
   §5's refuted-metric discipline that is a metric that moves by 2 on honest
   relabelling with n=20 — it belongs in this report as a human column, not in
   `check_consistency.py`. Recorded in the root-cause table (§5) as a
   **rejected** proposed edit, with the reason.

### R-4 — the 読解 key paraphrase rule, and the gate that never enforced it (R2-F5 + S-1)

Not asked for, found on the way: I hand-computed the longest common substring
between every key 52–69 and its own passage, because §3 states the rule
(*no LCS ≥15 chars and ≥50 % of option; no LCS ≥20 chars; no pure lifts*) and I
wanted the numbers rather than the gate's `ok`.

**Two items breach it, and one badly:**

- **問題10-55**, key 2 「市の知らせを待たず、町内会の判断で早めに開けるということ」
  against the notice's own 「そこで本年から、**市の知らせを待たず、町内会の判断で
  早めに開け**ます。」 — a **22-character verbatim run, 79 % of the option**.
  Both prongs of the rule trip. Its three distractors (待つ / 鍵を移す / 放送で
  知らせる) are all counterfactual rewrites, so the option whose wording is
  literally in the notice is the only one, and the surface-overlap strategy
  picks it: item 55 is one of my S1 hits (§6).
- **問題11-57**, key 3 「使用量が目に見えて減った家庭は、配布先の一部にとどまって
  いた」 — LCS **15 chars, exactly 50 %** 「使用量が目に見えて減った家庭は」. It
  trips the second prong at both boundaries simultaneously. Milder, but it is
  also an S1 hit.

**Fairness-tested before filing, as §5 requires.** Same predicate over all 24
generated papers and all 10 official sittings:

```
ALL TEN OFFICIAL SITTINGS        0 violations
23 of 24 generated papers        0 violations
20260827_1                       1  (item 67, LCS=22, 51%)
20260907_1                       2  (item 55 LCS=22/79%; item 57 LCS=15/50%)  <-- corpus maximum
```

The rule fails no real sitting, and this is the only paper on disk with more
than one breach. **R2-F5 stands.**

**S-1 — and the reason nobody saw it: the check is broken, not silent by luck.**
`check_verbatim_keys` computes the run with

```python
match = SequenceMatcher(None, flat_opt, flat).find_longest_match(...)
```

`difflib.SequenceMatcher` defaults to **`autojunk=True`**, which discards any
element occurring in more than 1 % of the second sequence. The 問題10–14 passage
corpus is ~6 000 characters, so the 25 commonest kana — `、` `。` `て` `し` `り`
`な` `か` `い` `の` `っ` `ら` `も` `す` `に` `と` `を` `は` `う` `が` `く` … — are all
classed as popular and excluded from matching. Measured on item 55's own strings:

```
autojunk=True  (as shipped):  LCS= 3  「町内会」
autojunk=False (correct)   :  LCS=22  「市の知らせを待たず、町内会の判断で早めに開け」
```

The check can only ever match runs of rare kanji, so **the 読解-key paraphrase
contract has never been enforced on any paper in this repo** — its green line
was never evidence. This is §6.5's `GATE-WRONG`, in its purest form: "the
symptom is silence." The one-token repair and its required corpus run are in
§5; applying it is out of this pass's scope (`tools/` is not QA's to edit).

---

## 4A. The descoped 聴解 items — recorded, not analysed

Per the mid-pass scope change, each of these is one line and no more. Every one
of them had already been measured before the change landed; I am **not** carrying
the analysis forward, and no 聴解 repair is proposed, designed or applied.

| dropped item | one-line record |
|---|---|
| `聴解 keys paraphrase the script` WARN (3/5) | **Real, and it is 問題2-1番** — that key's verbatim run off its own deciding line is 82 % of the option against 22–30 % for the section's other five. Not analysed further, no substitute wording designed. **Descoped.** |
| `聴解.mp3 pause distribution` WARN (6 % of 781, floor 7 %) | Not re-measured, not reasoned about. **Descoped.** |
| Deferred 2 — 聴解問題3-5番 vs `20260904_3` 問題3-2番 errand | Real: both are 組織としての案内 talks that draw a boundary around what an institution can and cannot see about you, and both 構成表 rows print the same arc token 「範囲の説明」. **Descoped, no repair.** |
| Deferred 3 — 自動車 at slot 2-5番 | **Not a finding** on the evidence I had gathered: all four axes round 1's F9 named (medium, 主導, 決め手の種類, apparatus) now differ; only the coarse 交通 tag, the slot and the presence of a car are shared. **Descoped.** |
| Deferred 4 — round-1 F7, 「染め」 on two surfaces | Half closed: the speaker is no longer introduced as a dyer, but 「染める」 survives in 問題3-4番's spoken distractor 1 beside 問題5-2番 質問2's key 「藍染め教室」. Not a solvability defect (the shared word sits on a distractor, so recognising it misleads). **Descoped.** |
| Claim R-2 — are F2's three subjects genuinely different? | Not carried forward as analysis. The one measurement already on record: the shared 7-char run 「をやめて、画面」 occurs **1×** now (was 2×), 「画面」 3× total, and 「紙」 zero times in that family. **Descoped.** |

### What I did KEEP on the 聴解 side, because it is correctness

- **All 30 scored 聴解 items blind-solved** from the embedded `聴解スクリプト.txt`
  and every key checked: **30/30 agreement**, inside the 101/101 of §2. No
  mis-key, no unanswerable item.
- **Every 聴解 key matches `test_spec.json`'s `answer_positions`** (gate `ok`,
  101 prescribed; and the digits agree with my independent solve, which is the
  half the position check cannot see).
- **All four 例 are answerable and their announced numbers match the marksheet**
  — `[3, 3, 2, 1]` vs `[3, 3, 2, 1]`, and I confirmed each dialogue actually
  supports its announced number (the half the gate cannot check).
- **No outright key leak or giveaway found**: `聴解問題1/2 closing turns differ
  and give nothing away` reports **0 rhymes, 0 leaks**, and I read the first and
  last spoken line of every item as a column myself — no closing turn names its
  own key. `問題3` has **0** key-exclusive content tokens across its 24 spoken
  options. `問題5-2番` prints no deciding attribute beside an option name and
  uses one order for both 質問.

Those are the only 聴解 claims this report makes.

---

## 4B. The sources moved underneath this review — what I did about it

This is not a content defect and it is not the repair round's: **a concurrent
session is editing this repo, and this paper, while I review it.** `exam-qa-review`
§7 says the sources must be still and to abort if they moved, so I am reporting
it rather than papering over it.

`言語知識・読解.md` took **three** distinct values during this pass:

| sha1[:12] | mtime | what I did with it |
|---|---|---|
| `24fa4608e0b2` | 13:38 | the revision `qa/20260907_1/keyless.md` was built from, and the one I blind-solved and wrote §3/§6 against |
| `acc50cca3281` | 16:30:59 | caught when I re-checked shas before writing; **round-1 F11's band records were added here** |
| `00d5c0ef1607` | 16:43:04 | current as of writing |

Alongside it the concurrent session modified `.gitignore`, added
`tools/choukai_segment.py`, and touched `言語知識・読解.md` / `詳細解説.json` /
`解答.html` / `模範解答.html` in seven other tests (`20260810_1`, `20260812_2`,
`20260814_1`, `20260817_2`, `20260827_2`, `20260828_1`, `20260828_2`).

**What I did about it, rather than trusting that nothing important moved:** I
re-ran every measurement this report rests on against each new revision. All of
them hold at `00d5c0ef1607`:

```
keys 1-71 identical to my blind solve      True   (all three revisions)
claim 1 — F1 predicate family              0/13   (all three revisions)
R2-F1  〜ていない finals                     2/13   問題10(5), 問題11(4)
R2-F5  verbatim key lifts                  55 (LCS=22, 79%), 57 (LCS=15, 50%)
R2-F6  「文頭に固定」 occurrences               1
```

So **no finding in this report is an artefact of a stale read**, and no key
moved. What the edits did change is option lengths: the (tied-)longest 読解 key
rate went 35 % → **30 %** and uniquely-longest 20 % → **10 %**, both improvements,
and the median overlap margin −0.016 → **−0.012**. §9's table carries the current
figures.

**The staleness FAIL it caused, and its self-clearing.** For roughly three
minutes this paper's own gate block carried a FAIL:

```
FAIL 20260907_1: built HTML matches the Markdown it stamps —
     言語知識・読解.html records 言語知識・読解.md=acc50cca3281, source is 00d5c0ef1607
```

The HTML had been built at 16:34:03 against `acc50cca3281`; the Markdown moved to
`00d5c0ef1607` at 16:43:04, so the booklet and answer sheet on disk rendered text
the source no longer contained. `exam-qa-review`'s automatic-fail list names
exactly this class: *an artifact older than the source it is built from … or HTML
predating its Markdown — no other gate sees it.*

**It has since cleared, and not by me:** the concurrent session rebuilt the HTML
at 16:46:41–42, and my final `make check` run reports

```
ok  20260907_1: built HTML matches the Markdown it stamps
ok  20260907_1: built HTML records its source sha
```

I deliberately did **not** run `make booklet`/`make sheet` myself while the file
was moving — rebuilding against a file another context is still editing just
produces a fourth revision and a fresh mismatch a minute later. I am recording
the episode rather than the finding: **it is struck from the finding count**, and
what survives is the root cause in §8, because nothing in the pipeline stops two
contexts writing to one test folder and the only symptom is a staleness FAIL that
reads like an author's mistake.

**One consequence the coordinator has to own, and I cannot close from here:**
every row of §6's walkthrough and every measurement in §3 is a claim about
`24fa4608e0b2`, re-verified at `00d5c0ef1607` for the load-bearing ones but not
re-read line by line at the newest bytes. The 文字・語彙 half in particular gained
three new 解説 cells (items 25/27/29) that I read and verified, but I cannot rule
out other prose edits I did not think to re-measure. **If the concurrent session
made substantive content changes beyond the band records and the option-length
balancing, the 読解/文法 half of this review needs re-running on the settled
file.** Diffing is not available to me: `tests/20260907_1/` is entirely untracked
(`?? tests/20260907_1/`), so there is no committed revision to compare against.

---

## 5. Round-1 F11 — closed during this pass, and verified rather than accepted

Round 1's F11 (no band record for 問題6's 「懸念」/「照会」, nor for the 陽気だ
re-draw) was **still open when I began** — I grepped for it and filed it as
R2-F7 (an id that consequently does **not** appear in §7's final finding
list). The concurrent session closed it at 16:30:59 by adding a `band記録` clause
to all three 解説 cells. Because `AGENTS.md` §3 forbids taking a band number on
trust, I checked each claim against the **tracked** extracts:

| claim in the new 解説 | my verification |
|---|---|
| 「陽気」は『はじめての日本語能力試験N2単語2500』見出し**929**(「今日は陽気がいい」「彼は本当に陽気な人だ」)に掲載 | **CONFIRMED** — `refs/Hajimete/vocab_reference.md` L13040 is 「929」 and L13080–13081 are those two example sentences verbatim |
| 「懸念」「照会」は四つのN2語彙権威に見出しなし、31回の `booklet.md` にも0件 | **CONFIRMED** — 懸念 0 and 照会 0 across `Hajimete/vocab_reference.md` + `Shinkanzen/goi_reference.md` + `Shinkanzen/kanji_tables.md` + `Soumatome/goi_reference.md`, and 0 across all `refs/JLPT_N2_NEW/*/booklet.md` |
| 「敏感」も四書0件だが本試験に出題されており、不掲載だけでは級外と決まらない | **CONFIRMED, and understated** — 敏感 is 0 in the four extracts but **5 hits** across the 31 `booklet.md` files, so the counter-example is stronger than the cell claims |

**Closed, and struck from the finding list.** The record now exists, it is honest about what it did and
did not establish ("掲載による積極的な裏づけは取れていない…判定ではなく記録として
残す"), and it cites the very counter-example round 1 raised against its own
zero. That is exactly what `exam-qa-review` §3 asks for — a stated band check,
not a manufactured verdict. I am recording the closure with my verification
because a band record nobody re-read is how REPORT-GOI.md §F10 happened.

---

## 6. Per-question walkthrough — all 101 items + 4 例

Every row's 決め手 was read against the source during the blind solve, then
re-read against the key table. `OK` rows carry the deciding quote, as the report
format requires.

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 3 | OK | 召し上がる＝めしあがる。四択とも実在の「〜上がる」複合動詞（起き上がる/出来上がる/召し上がる/盛り上がる）、印字送り仮名「がる」を共有 | — |
| 問題1-2 | 1 | OK | 粒＝つぶ。粒/粉/種/泡、一字和語の同一場（薬の形状）で四つとも実在語 | — |
| 問題1-3 | 2 | OK | 現象＝げんしょう。2×2 {げん,けん}×{しょう,ぞう} | — |
| 問題1-4 | 1 | OK | 打者＝だしゃ。2×2 {だ,た}×{しゃ,じゃ}、清濁派生のみ | — |
| 問題1-5 | 2 | OK | 学術＝がくじゅつ。2×2 {がく,かく}×{じゅつ,しゅつ} | — |
| 問題2-6 | 2 | OK | 幾分。2×2 {幾,育}×{分,文}、四字とも「いくぶん」に読み分解でき、成分行列は 解説 に明記 | — |
| 問題2-7 | 4 | OK | 依頼。2×2 {依,衣}×{頼,来}、衣は依の右側を含む視覚類似字 | — |
| 問題2-8 | 4 | OK | 下書き。2×2 {下,舌}×{書き,欠き}、した/した/か-く/か-く は四つとも常用音訓。`matrix_helper` のかな骨格 FAIL は 連濁 か→が を持たない工具側の限界で、解説 に手検証が記録されている | — |
| 問題2-9 | 2 | OK | 計る。「ストップウォッチで時間を」が対象を時間に固定し、異字同訓の官製指針が 時間→計る を明示。同訓異字は4×1なので `matrix_helper` FAIL は工具限界、解説 に記録あり | — |
| 問題2-10 | 3 | OK | 引力。2×2 {引,因}×{力,緑} | — |
| 問題3-11 | 2 | OK | 半永久。「この電池は（　）永久に使えるそうです」＝ほとんど永久といえるほど長く続く。準/微/超 はいずれも 永久 に前接しない | — |
| 問題3-12 | 4 | OK | 交通費。「毎月の交通（　）を自分で払っています」。代/料/賃 は 交通 と複合しない | — |
| 問題3-13 | 1 | OK | 異文化。「（　）文化の中で暮らすのは大変だ」。別/逆/反 は 文化 に前接しない | — |
| 問題4-14 | 3 | OK | 一般に。「ほかの地方のものより味が濃い」という一般的傾向の提示 | — |
| 問題4-15 | 2 | OK | 固まる。「冷蔵庫に入れておくと」＋ゼリーが形を保つ | — |
| 問題4-16 | 4 | OK | 合理的だ。「時間も費用もむだにしない」＝むだがなく理屈に合う | — |
| 問題4-17 | 3 | OK | 順応する。「南の海から来た魚」が湖の水温に自分を合わせる方向 | — |
| 問題4-18 | 4 | OK | 昇進する。「十年間まじめに働いた父は…課長に」＝上の役職へ上がる | — |
| 問題4-19 | 1 | OK | 発足する。「子どもの安全を見守る新しい会が」＝組織ができて活動を始める | — |
| 問題4-20 | 2 | OK | 飽きて。「買ったばかりのゲームに、たった三日で」＝十分だと感じ興味を失う | — |
| 問題5-21 | 3 | OK | そそっかしい→不注意な。「兄は不注意な性格で、忘れ物が多い。」で文が成立 | — |
| 問題5-22 | 4 | OK | 鋭い→敏感だ。「人の気持ちの変化に敏感だ。」。敏感 は官製 12/2025 の問題4選択肢にも出る現行語 | — |
| 問題5-23 | 1 | OK | 気が重い→気が進まない。「明日の発表を思うと気が進まない。」 | — |
| 問題5-24 | 3 | OK | 依然として→相変わらず。「駅前の工事は相変わらず終わらない。」 | — |
| 問題5-25 | 4 | OK | 陽気だ→明るい。「あの店の主人はとても明るい。」（陽気 は はじめて N2単語2500 に4回、帯は確認できる） | — |
| 問題6-26 | 2 | OK | 唱える＝自分の考えを主張として掲げる。「これまでの常識とは違う新しい説を唱えている」 | — |
| 問題6-27 | 3 | OK（pass 中に解消） | 懸念＝これから起こるかもしれない悪い結果への心配。「工事の遅れによる開店時期への懸念が、社内で広がっている」。**round-1 F11 の帯記録は 16:30 に追加され、私が tracked 抽出で検証した（§5）**——四書0件・31回0件を記録し、敏感の反例を挙げて「判定ではなく記録」と明言している | — |
| 問題6-28 | 1 | OK | 正式に＝決められた形式にのっとって。「両国の話し合いは、来月から正式に始まる」 | — |
| 問題6-29 | 3 | OK（pass 中に解消） | 照会＝情報を持つ相手に問い合わせて確かめること。「銀行に残高の照会をしたところ」。**同じく帯記録が追加され検証済み（§5）** | — |
| 問題6-30 | 1 | OK | 共感＝他人の気持ちや考えを自分もそのとおりだと感じること。「主人公の悩みに、多くの若い読者が共感を寄せている」 | — |

**問題6 の option set 判定（§2b）**：四文とも標的語の同一品詞・同一 register
で、`check_goi_option_set_valence` の 3:1 トーン分割も、三択を一文で消す 解説 も
無い（gate `ok`、私も5題を手で読んで確認）。誤答文はいずれも「学習者が実際に
産出しそうな誤用」型で、第二の成立コロケーションになっているものは無い。

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 3 | OK | 〜に応えて。「もう一度見たいという長年の声」＝要望にこたえて行動する | — |
| 問題7-32 | 3 | OK | 〜ずじまいだった。「せっかく地図まで用意したのに」＝結局しないまま終わった心残り | — |
| 問題7-33 | 1 | OK | 〜はさておき。値段の話を当面脇に置き、静かさを評価する | — |
| 問題7-34 | 4 | OK | 〜ないものだろうか。「一度書けば済むように…と、前から思っている」＝実現への願望 | — |
| 問題7-35 | 1 | OK | 〜あまり。緊張のしすぎが原因で原稿を飛ばした因果 | — |
| 問題7-36 | 4 | **OK（round-1 F12 解消）** | 「部長が出られない（　）、資料だけは全員分そろえておこう」。**単半の譲歩用法に切り直され、対の前半は印字されていない** | — |
| 問題7-37 | 4 | OK | 〜てはじめて。水道が止まって初めて分かったという気づき | — |
| 問題7-38 | 3 | **OK（round-1 F12 解消）** | 「気が長い（　）、そういうことに関心がないのだろう」。**「〜というか」の前半は印字されていない** | — |
| 問題7-39 | 2 | OK | 〜に限り。午前中の来店客だけを割引対象に限定 | — |
| 問題7-40 | 1 | OK | 〜に際して。改まった場面で、初回利用のそのときに | — |
| 問題7-41 | 4 | OK | 〜につけて。曲を聞くたびに記憶が自然に起こる | — |
| 問題7-42 | 1 | OK | 〜ところだった。教えられなければ危うくそうなりかけた | — |
| 問題8-43 | 2 | OK | お選びいただいた(3)→色の在庫が(1)→**そろい次第(2)**→すぐに発送いたします(4)。最終スロット証明が全カードを名指し、鍵以外の並びは「在庫が発送いたします」となり謙譲語の主語になれない | — |
| 問題8-44 | 1 | OK | 見上げる(2)→たびに(3)→**また背が伸びたと(1)**→思ったものだ(4)。連体形＋たびに、引用のと で二脚固定、FREE UNITS=0 | — |
| 問題8-45 | 2 | OK | 年齢の(1)→わりに(3)→**足が丈夫だと(2)**→言われることがある(4)。連体の＋わり、引用のと | — |
| 問題8-46 | 1 | OK | 東口が…混み合う(2)→のに対して(3)→**夜遅くまで学生の(1)**→話し声が絶えないのだ(4)。「AのにたいしてB」呼応 | — |
| 問題8-47 | 3 | 要修正（解説の一句のみ） | ★の一意性は健全。18/24 が接合フィルタを通るが、★を動かす唯一の自然な対抗 (2)→(3)→**(1)**→(4) は 解説 が正しく意味排除している——「「例えば」を述部の直前に置く並びは、例示の範囲が「思い出してみればいい」だけに縮み、リード文が予告した具体例が示されないことになるので取れない」。**私は独立に同じ排除に到達した。** ただし round 1 が指摘した 解説 の 「文頭に固定」 はまだ不正確：「例えば」は文頭ではなく、スクランブル span の1枚目（stem の「同じ話を」の後）に立つ | 「文頭に固定」→「**並びの先頭に固定**」。一句の置換で、鍵・選択肢・本文は動かない（R2-F6） |
| 問題9-48 | 4 | OK | [論理接続] 直前二文（沿えば管は残る／横から入れれば断たれる）を「中身が閉じるか、出入りの道が開くか」と言い直す言い換え接続 → つまり | — |
| 問題9-49 | 3 | OK | [文末モーダル] 「道が開いていれば水分が出やすく煮汁が入りやすい」から当然導かれる帰結 → 〜わけだ | — |
| 問題9-50 | 4 | OK | [慣用・形式名詞] 「水の通り道を開けるか閉じるかを選んでいるのだから」＝大げさではなく理にかなう → 道理にかなったことである | — |
| 問題9-51 | 1 | OK | [内容推論] 文章全体が、切る向きが味の入り方を左右するという筋。**round-1 F1 の 「その日の味の入り方を決めている」 は消えており、本文は 「選んでいる」 に書き替わっている** | — |

**問題9 の空欄カテゴリ**：論理接続 / 文末モーダル / 慣用・形式名詞 / 内容推論
——4つとも別（gate `ok`、[内容推論]1つを含む）。cloze 本体 688 JP字（帯 500–700）。

**「一文法点一鍵」の再走査（§3、prose 修理のあと必須）**：問題7/8/9 の keyed
form 全17件を 問題10–14 の passage prose と （注N） 定義行に grep し直した。
上限1回を超えるものは無く、同一 文末／連用／連体 frame の出現も無い（gate
`check_key_grammar_exposure` も `ok`）。7つの closing と5つの key text が
書き替わった直後なので、これは gate の green ではなく**再 grep で**確かめた。

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 1 | OK | 「すぐ見られる形に整理したつもりで、私は写真を見る時刻のほうを暮らしから消してしまっていた」 | — |
| 問題10-53 | 1 | OK | 「今年の春に気づいたのは、こちらの手順が一つずつ要らなくなっていくという成長のほうだった」 | — |
| 問題10-54 | 4 | OK | 「そこで本年は、通路の奥の、広場に近い区画へ移していただけないでしょうか」。**round-1 F3 解消**：差出人は「なかまち手づくりの会の大西」、宛先は「東通り商店会」で、次面の「桜坂町内会」と別団体になった | — |
| 問題10-55 | 2 | 要修正 | 決め手は「そこで本年から、市の知らせを待たず、町内会の判断で早めに開けます」。**R2-F5**：鍵はその一文の **14…22字を丸写し（選択肢の79%）**。§3 の言い換え規定（LCS ≥20字 で不可）に触れ、官製10回は0件 | 鍵を言い換える。例：「避難の知らせを待つのをやめ、町内会が自分で開ける時期を決めるということ」。解説 の引用は動かさない |
| 問題10-56 | 3 | OK | 「たいていの場合、迷った人は道具を持っていて、持っていなかったのは引き返す時刻のほうだった」 | — |
| 問題11-57 | 3 | 要修正 | 決め手は「使用量が目に見えて減った家庭は全体の三割ほどにとどまり」。**R2-F5（軽度）**：LCS 15字・選択肢の50%で、規定の第二項を両境界ちょうどで踏む | 「使用量が目に見えて減った家庭は」を「水道の使用量がはっきり下がった家庭は」等に言い換える |
| 問題11-58 | 4 | OK | 「ためた水をまく場所が置く前から決まっている家庭がどれだけあるか、そこを確かめずに配り続けても…」 | — |
| 問題11-59 | 2 | OK | 「乗る人が新しい時刻表を見て、また三分前に着くよう出かけてしまうからである」。理由を問う設問が、本文の述べる**原因**に鍵付けされている | — |
| 問題11-60 | 2 | OK | 「一時間に一本のほうでは、十分の遅れがそのまま十分の待ち時間になり、乗り継ぎの列車にも間に合わなくなる」。**鍵 text は F1 修理で書き替え済み**、新しい closing の写しではない | — |
| 問題11-61 | 2 | OK | 「色を増やした号も…数字はほとんど動きませんでした」＋「この「その後」を一つでも載せた号では、はがきの枚数が…およそ二倍だった」 | — |
| 問題11-62 | 3 | OK | 「「知らせだけが並ぶ紙は、こちらに用のない紙に見える」」＋「前の号の話に決着をつけた号ほど、読者からの返事は多くなっていました」。**書き替え済みの鍵** | — |
| 問題11-63 | 3 | OK | 「学生時代から続いている親しい友人とは、二人としか会えていない」対「年に一、二度しか話さない相手…とは、五人と会っている」 | — |
| 問題11-64 | 2 | OK | 「親しい友人とは、いつでも会えるという安心があるから、「近いうちに」で会話が終わり、手帳を開かないまま別れて」。**書き替え済みの鍵** | — |
| 問題12-65 | 1 | OK | A「順番を逆にした人のほうが、あとで買い直しをしていない」＋「そのうえで買った机や棚は、置き場所が動かない」／B「半年おくれて置いた机は、十年たったいまも同じところにあります」。**書き替え済みの鍵で、round 1 の 7字リフト「置き場所を決め」は消えている** | — |
| 問題12-66 | 4 | OK | A の「順番を逆にした人のほうが、あとで買い直しをしていない」と B の「自分がどこに長くいるかが分かりました」を対で拾う | — |
| 問題13-67 | 1 | OK | 「「立っている時間が長かった」」＋「行けといわれて行くのですが、行った先で何をすればいいのか、だれも教えてくれないんです」 | — |
| 問題13-68 | 3 | OK | ①の直前「置き場所がわからず、次に何をすればよいか質問しようにも」「相手は手がふさがっている」。marked span は stem の引用と同一文字列、（注N）は太字の外 | — |
| 問題13-69 | 4 | OK | 「応援を受ける課は、何人来るかを数える前に、来た人が最初の三十分で手をつけられる仕事を一つ書き出しておきたい」。**書き替え済みの鍵**、closing との共通run は 9字（「応援を受ける課は、」＝本文の主語名詞句） | — |
| 問題14-70 | 2 | OK | 折りたたみのいす だけが〈返す時刻 当日午後七時まで〉×〈返す場所 案内所・駅の窓口〉×〈当日その場で申込〉の三条件を同時に満たす。かさ・手押し車は五時まで、手押し車は案内所のみ、電動自転車は前日電話＋返却場所に駅の窓口が無い。**制約2つ以上を結合**、発明ディテール無し | — |
| 問題14-71 | 2 | OK | 「電動自転車は一回五百円です。お支払いは当日、現金でお願いします」＋「前日までにお電話」。カード払い(3)・その場申込(1)・無料(4)はいずれも案内が明示的に否定 | — |

### 聴解 (問題1–5)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 3 | OK | 「電気を使うお店がどこか、聞いて紙に書き出してくれる」→「わかりました。今から回ってきます」。**印字された例の番号3＝アナウンスの番号3＝対話が支持する番号** | — |
| 問題1-1番 | 1 | OK | 「飲むお水と、おてあらいに流すお水は、今晩のうちに、なべやバケツにためておいてください」。誤答3件はすべて放送内で否定／後回し。**非対話項目（館内放送）を1件持っている** | — |
| 問題1-2番 | 4 | OK | 「お名前はもう入れないで、授業の名前と、時間わりの番号を入れて」。**F2 修理後：画面は既存の背景で、errand は入れる「項目」の差し替えになっている** | — |
| 問題1-3番 | 1 | OK | 「図書室が金曜から本の整理で…読む本、今日のうちに二冊選んでおいてください」 | — |
| 問題1-4番 | 3 | OK | 「だから、試す人を二人ずつの組にして、回る順番を紙にしてくれる」 | — |
| 問題1-5番 | 2 | OK | 「その方の分だけ、お茶にとろみをつけてもらうように、台所に言ってきてくれる」。**round-1 F8 解消**：場所列挙型の errand（貸し出し先を消していく型）が消え、規則・資格・車両不在で消える指示型になった。20260904_3 2-5番… 1-5番 との共有軸は cast のみ | — |
| 問題2-例 | 3 | OK | 「三着以上お出しになりますと、一着千五百円になります」＋「そのほうが、一着分お得ですもんね」。例の番号3が一致 | — |
| 問題2-1番 | 4 | OK（鍵は正しい） | 決め手は「ですから、だれが参加できるのかを、必ず入れてください」で、鍵はこれを述べ直した命題。誤答3件はいずれも台本内で明示的に否定される。**言い換えの薄さは §4A で descope 済み** | — （descoped） |
| 問題2-2番 | 2 | OK | 「宿を五時半に出ていただくことに」→「五時半は、ちょっと」。誤答3件は宿・値段・祭りとして明示的に否定 | — |
| 問題2-3番 | 2 | OK | 「順番は決まっていて、課長が済ませるまでは、部長のところには回らないんです」。F2 の生き残り1件だが、単独なので paper 内の subject 重複ではない | — |
| 問題2-4番 | 3 | OK | 「当番が、そういうお宅の分だけ、台車で取りに回るようにしたんですよ」＋「運べないから出さない、という方が多かったんですよ」。gate の verbatim WARN はこの行を最終述部 branch で拾っているだけで、実 run は5字・26% | — |
| 問題2-5番 | 1 | OK | 「今年から、冬用のタイヤをはいていれば、鎖はなくても通れることになったんです」→「まさか、要らなくなってたなんて」。価は**意外**で、「安心」「納得」いずれの語も鍵に無い。**deferred 3 は §4 で不成立と判定** | — |
| 問題2-6番 | 3 | OK | 「この形のものは、直す部品を作るのが今年でおしまいなんです」＋「冬は二週間かかります。その間、お湯は出ません」。実 run 5字・22% | — |
| 問題3-例 | 2 | OK | 「頼まれた順ではなく、申しこみの締め切りが近いものから貼る、ということです」。**round-1 F6 解消**：問い合わせ電話を数える払いが消え、掲示板の紙の**選び方**の話に再アングルされた。例の番号2が一致 | — |
| 問題3-1番 | 4 | OK | 「ただ、いちばん変わったのは、会議そのもののほうです」 | — |
| 問題3-2番 | 4 | OK | 「三年前から、渡すのをやめました。かわりに、隣のお宅の方が三十分、お茶を飲みながら話す形にしたんです」。独話は自分の誤答を一つも名指ししない（問題3 の設計どおり） | — |
| 問題3-3番 | 1 | OK | 「中に入られる前に、二つお願いがございます」＋二点の列挙 | — |
| 問題3-4番 | 4 | OK（鍵は正しい） | 決め手は「ぬわないのには、わけが二つあります」＋かわきの早さ・手で裂けること。誤答3件はいずれも独話に出てこない周辺（問題3の設計どおり）。**「染め」の二面出現は §4A で descope 済み** | — （descoped） |
| 問題3-5番 | 3 | OK（鍵は正しい） | 決め手は「分かりますのは、開いた教材と、使った時間の合計、それに、宿題を出したかどうかです」＋「一方、お使いになった時こくや、調べものの中身までは、学校では分かりません」。**20260904_3 問題3-2番 との errand 一致は §4A で descope 済み** | — （descoped） |
| 問題4-例 | 1 | OK | 「うん、読み終わったら返してね」＝条件つき承知。番号1が一致 | — |
| 問題4-1番 | 1 | OK | 到着の知らせ→「じゃあ、下まで迎えに行ってくるよ」。誤答は既に完了／日程の決め直し | — |
| 問題4-2番 | 2 | OK | 「体は大丈夫？」→「うん、まあ、寝る時間だけは何とか」＝間接的な返答。敬語方向も同輩どうしで一致 | — |
| 問題4-3番 | 3 | OK | 「確認いただけましたでしょうか」→「すみません、今開いたところです」。1は立場の逆転 | — |
| 問題4-4番 | 1 | OK | 「君が中心になって進めてくれないか」→「私でよろしければ。いつから始めればいいですか」＝疑問文での返答。部長への返答として敬語方向が正しい | — |
| 問題4-5番 | 3 | OK | 「面会時間は午後二時から四時までです」→「そうですか。じゃあ、それまで下で待っています」 | — |
| 問題4-6番 | 1 | OK | 「マスクの着用にご協力ください」→「持っていないんですが、こちらで買えますか」。**応答者が定義された prompt**（係員→来訪者） | — |
| 問題4-7番 | 3 | OK | 「気が利くよね」→「うん。前の職場でも、そう言われてたって」。1は「利く」の語義取り違え | — |
| 問題4-8番 | 2 | OK | 「手が空いたら…手伝ってくれない？」→「三時には終わるけど、それでもいい？」 | — |
| 問題4-9番 | 2 | OK | 「慣れるまで少し時間がかかりそうですね」→「ええ、はじめの一週間は、二人ずつで見合いましょう」 | — |
| 問題4-10番 | 1 | OK | 「お茶をお入れしますね。お菓子もありますよ」→「どうぞ、お構いなく。すぐ失礼しますので」＝辞退 | — |
| 問題4-11番 | 2 | OK | 「サンプルが届きましたので、お持ちいたしました」→「ありがとう。そこの棚に置いといて」。課長→部下の敬語方向で一致 | — |
| 問題5-1番 | 4 | OK | 「番号を待っているというより、どこに何を書くか分からなくて、机の前で止まっている方が多いんです」→「書き方の見本を置いてある机…待っていただく場所のとなりに移しましょうよ」→「明日からできます」。他3案はすべて場内で否定 | — |
| 問題5-2番-質問1 | 4 | OK | 「町歩きの会は、当日でも申しこめるんだよね。残業のない日に行くよ」。そば打ち＝当番と重なる／庭木＝子どもの試合／藍染め＝平日で働いている、と本人が三つ取り下げる | — |
| 問題5-2番-質問2 | 2 | OK | 「車がないから、送り迎えのあるのがいちばんなのよ」＋「材料も用意してくれるみたいだし、父にはそれを勧めるわ」＝送り迎えのバスが出る藍染め教室。**決め手の属性は選択肢名の横に印字されておらず**（問題5は全て読み上げ）、質問1と質問2の選択肢順は同一 | — |

**行数**：文字・語彙30 ＋ 文法21 ＋ 読解20 ＝ 71、聴解 採点対象30 ＋ 例4 ＝ 34。
合計 **101 採点項目 + 4 例 = 105 行**。判定は `OK` **102**、`要修正` **3**
(問題8-47, 問題10-55, 問題11-57)、`自動不合格` **0**。

問題6-27 / 問題6-29 の行は、**この pass の途中で band 記録が追加されたため
`要修正` から `OK` に変わった**（§5 に検証を記録）。聴解の3行は §4A の descope に
より `OK（鍵は正しい）` に変えてある——鍵はいずれも健全で、落としたのは言い換えの
薄さと題材の重なりという最適化項目である。

R2-F1 は closing の対に対する **surface レベル**の finding なので、どの単一行も
それを担っていない（round 1 が F1/F2 を surface レベルで立てたのと同じ扱い）。
問題10(5)/問題11(4) 自身の item 行（56 / 64）は鍵として健全なので `OK` である。

---

## 7. Findings table

| id | item / surface | class | evidence | disposition | mechanical or authoring? |
|---|---|---|---|---|---|
| **R2-F1** | 問題10(5) + 問題11(4) closings | repair collateral: one skeleton + one label | 「引き返す時刻は、どの店にも置い**ていない**。」／「…いちばん会いたい相手とはまだ会え**ていない**。」 both labelled 意外な観察. **2/13 — the only paper of 34 on disk at 2**; next-highest generated is 1, and **all ten official sittings are 0** | OPEN — reported, not repaired | **authoring**: which of the two is re-closed, onto which of the six catalogued shapes |
| **R2-F5** | 問題10-55, 問題11-57 | 読解 key not genuinely paraphrased | 55: **22-char verbatim run = 79 %** of the option, lifted off the notice's own 「そこで本年から、市の知らせを待たず、町内会の判断で早めに開けます。」, with all three distractors counterfactual rewrites — so the one option whose wording is literally in the notice is the key, and it is an S1 hit. 57: LCS **15 / exactly 50 %**, tripping the second prong at both boundaries. **Corpus maximum; all 10 official sittings 0**, 23 of 24 generated papers 0 | OPEN | **authoring** (re-paraphrase; the 解説 quote need not move) |
| **R2-F6** | 問題8-47 解説 | 解説 prose inaccurate — round-1 note, unapplied | 「裸の副詞は接続の「例えば」一枚のみで**文頭に固定**」 — 「例えば」 stands at blank 1, after the stem's 「同じ話を」, not at 文頭. The cell's *substantive* exclusion is sound and I derived it independently (§9) | OPEN | **mechanical**: 「文頭に固定」→「並びの先頭に固定」 |
| ~~R2-F8~~ | `言語知識・読解.html`, `解答.html` | artifact older than its source — **transient** | `make check` FAILed at 16:43: 「built HTML … records …=acc50cca3281, source is 00d5c0ef1607」. The concurrent session rebuilt at 16:46:41; the gate now reports **`ok`** on both the sha-match and the source-sha lines | **CLEARED during the pass, not by me** — struck from the count. The hazard it exposed is a root cause (§8), not a paper finding | — |
| **S-1** | `tools/check_consistency.py` | `GATE-WRONG` | `check_verbatim_keys` calls `SequenceMatcher(None, a, b)` with the default `autojunk=True`; at a ~6 000-char passage corpus the 25 commonest kana become "popular" and unmatchable. On item 55's own strings: **reports LCS=3, true run 22** | OPEN — `tools/` is out of QA's scope to edit | gate fix (one keyword) |

**Round 1's twelve findings, ticked off one by one against the shipped files:**

| round-1 id | closed? | how I verified it |
|---|---|---|
| F1 (determinant-closing monoculture, AUTO) | **CLOSED** | 6/13 → **0/13** under both the narrow and widened family, re-measured at all three revisions of the file; all seven old closing strings at 0 occurrences (§3 R-1). Collateral: R2-F1 |
| F2 (three 聴解 items on 紙→画面, AUTO) | **CLOSED** on the one measurement kept | 「をやめて、画面」 1× (was 2×), 「画面」 3× total, 「紙」 0× in that family. Further analysis **descoped** (§4A) |
| F3 (one invented body on two surfaces) | **CLOSED** | three distinct bodies now (なかまち手づくりの会 / 東通り商店会 / 桜坂町内会), each on ONE surface, and 0 occurrences of any of them — or of 平川/大西 — in `20260904_2` or `20260904_3` |
| F4 (貸し出し errand in 問題14 and 聴解1-5番) | **CLOSED** | the only 貸し出し left in the 聴解 script is 「貸し出しのパソコン」 (incidental); 車いす/介護用品 at 0 |
| F5 (buses in 問題11(2) and 聴解2-5番) | **CLOSED** | 停留所 5× in 読解 問題11(2) only, **0× in the 聴解 script**; the two 「バス」 in 聴解 are incidental |
| F6 (問題2-1番 ≡ 問題3-例's insight) | **CLOSED** | 問題3-例 re-angled to noticeboard selection; 問い合わせ at 0 in that block. Its collateral is **descoped** (§4A) |
| F7 (染め ×2) | **HALF CLOSED — descoped** | §4A |
| F8 (聴解1-5番 ≡ 20260904_3 1-5番) | **CLOSED** | the place-elimination errand is gone; 1-5番 is now an instruction item |
| F9 (聴解2-5番 ≡ 20260904_3 2-5番) | **CLOSED — descoped** | §4A |
| F10 (two of three WARNs not handed forward) | **RESOLVED** | all three re-checked independently; two are false positives (§9), the third **descoped** |
| F11 (no band record for two 問題6 keys + the re-draw) | **CLOSED during this pass** | Added at 16:30:59 by a concurrent session; **I verified both claims against the tracked extracts** — 陽気 at 見出し929 with its two example sentences, and 懸念/照会 at 0 across four extracts and 31 sittings (§5) |
| F12 (two 問題7 stems print their key) | **CLOSED** | re-ran the predicate over all 12 問題7 items: **0 hits**; both stems re-cut onto the single-half use |

---

## 8. Root-cause table (§6.5)

Recurrence test applied first: a class shown by two or more papers is systemic by
definition. 聴解-side root causes are **not** filed, per the scope change.

| id | root cause | tests showing the class | owning file | concrete proposed edit |
|---|---|---|---|---|
| **S-1** | `GATE-WRONG` | **all 34 papers on disk** — the check has never worked | `tools/check_consistency.py` | In `check_verbatim_keys`, change `SequenceMatcher(None, flat_opt, flat)` to `SequenceMatcher(None, flat_opt, flat, autojunk=False)`. `difflib`'s autojunk drops any element in >1 % of the *second* sequence; at 6 040 characters that is the 25 commonest kana, so only rare-kanji runs could ever match. **Founding-case run, as §6.5 requires** — item 55's own strings: `autojunk=True` → LCS **3** (「町内会」); `autojunk=False` → LCS **22** (「市の知らせを待たず、町内会の判断で早めに開け」). **Corpus run at the fixed predicate, so a widened rule cannot quietly re-classify shipped work: exactly two ids move** — `20260907_1` (items 55, 57) and `20260827_1` (item 67, LCS 22 / 51 %). **All ten official sittings stay at 0**, so the contract the check was always meant to enforce fails no real sitting. `20260827_1` needs a grandfather entry by name or its own repair. This is the purest form of the row §6.5 calls most dangerous: the symptom was silence, and its green line was read as evidence by round 1 and by every prior pass |
| **R2-F5** | `GATE-WRONG` (downstream of S-1) | 2 | — | No separate edit; the paper defect exists because S-1 hid it |
| **R2-F1** | `GATE-BLIND` | 1 at 2/13, and it is the **fourth** paper to show the *repair-collateral* class (20260812_1 F2→F3, 20260903_1 F2, 20260904_1 round-2 F2/F3) | `tools/check_consistency.py` + `question-authoring/references/dokkai.md` | Add a `FINAL_SENTENCE_TEMPLATES` row **「〜ていない（不在の残り）」**: `re.compile(r"てい(ない|ません)。?\s*$")`, with `FINAL_TEMPLATE_CAPS = 1` — for the same reason 後知れ got one: it is a single pattern with a single rhetorical effect, so a second use is a rhyme, not a coincidence. **Founding-case run over all 34 papers at this check's final-sentence scope, predicate anchored: `20260907_1` = 2 (FIRES); `20260828_2` = 1 and `20260903_1` = 1 (silent at cap 1); the other 31 papers = 0; ALL TEN OFFICIAL SITTINGS = 0.** So it catches its own founding case, moves exactly ONE id — the paper it was written from — and fails no real sitting. Under the shared cap of 2 it would move zero ids and could not fire on the case it was written for, which is `check_mondai9_option_reuse`'s recorded mistake (R3-9). **Anchor the `$`**: the unanchored form matched 〜ていない mid-sentence and put nine generated papers and one official sitting on the board (§3 R-1b records the error) |
| **R2-F6** | `RULE-IGNORED` | 1 | nothing to change | Round 1 wrote the repair into its own walkthrough row and the fix round did not apply it — the same "flagged without repairing left it in the paper" pattern round 1's own claim-3 verdict criticised. Process failure (AGENTS.md §0) |
| **concurrency (the struck R2-F8)** | `PIPELINE-GAP` | 1 observed, but the class is structural | `jlpt-test-generation` + `tools/check_consistency.py` | The gate correctly FAILs a stale HTML, so the check is right; what is missing is an ordering rule for **concurrent sessions**. Nothing in the pipeline prevents a second context from editing `tests/<id>/*.md` while a QA pass or a build is in flight, and the only symptom is a staleness FAIL that looks like an author's mistake. Add to `jlpt-test-generation`: *a test folder has one writer at a time; a QA pass records the source shas it read, and a build or repair that finds them moved re-runs the pass rather than rebuilding on top of it.* This paper is the live case: `言語知識・読解.md` took three values inside one review (§4B) |
| **NEW-1** (note, no paper finding) | `RULE-MISSING` | 2 rounds noticed it, no rule covers it | `jlpt-test-generation` §"One topic, one surface" | **A rhetorical MOVE shared between a 読解 surface and a 聴解 item is uncovered by every rule in the repo.** 問題10(1) (digitising the album delivered instant access and deleted the viewing ritual) and 聴解問題3-1番 (the transcription tool did save typing, but the real change was the meetings) run one move — *the tool kept its promise; the real change was elsewhere* — both tagged デジタル化, neither re-authored, and round 1 noticed the echo inside F2's discussion without being able to file it. The 読解 closing-move cap is 読解-internal; the 聴解 errand rule is 聴解-internal; §5's subject clause compares SUBJECTS, and these differ (photo album vs meeting minutes). Add to the whole-paper pass: *label each 読解 surface and each 問題3 talk with its rhetorical move as well as its subject, and allow at most two surfaces on one move across the two halves.* Not string-decidable, so it is a skill edit and not a check. **Filed as a 読解-side note; no 聴解 repair is proposed.** |
| **NEW-2** (note) | `GATE-WRONG`, minor | 6 papers under-counted | `tools/check_consistency.py` | `FINAL_SENTENCE_TEMPLATES`'s correlation row `(では|ほど)[^。]{0,25}(多い|少ない|大きく|…|なっていた)` matches the plain past but **not the polite past**: 問題11(3)'s 「…号ほど、読者からの返事は**多くなっていました**。」 does not match, while the same sentence as 「多くなっていた。」 does. Since `dokkai.md` Axis 3 actively REQUIRES ≥3 です・ます passages per paper, the row goes blind on exactly the passages the style rule mandates. Widen the alternation to stems (`多|少な|大き|小さ|高|低|増え|減|開きが|なってい`). **Corpus effect measured before proposing:** `20260812_2` 0→2, `20260828_1` 0→2, `20260907_1` 0→1, six others +1; nothing reaches 3, so at the cap of 2 **zero ids move**. This paper is at 1 either way, so it is not a finding here |
| **round-1 F11, for the record (closed)** | closed, `RULE-UNENFORCEABLE` remains | all 24 generated papers | `exam-blueprint/references/pools.json` + `moji-goi.md` | The paper's record is now in place (§5), but the underlying cause is untouched: `pools.json`'s `usage`/`context_words`/`paraphrase` are bare string lists, so no band claim is checkable and every reviewer re-litigates the same two words. Convert each entry to `{"w": "照会", "src": "<book> p.<n>"}` (or `"src": "archive:<sitting>"`) and add `check_pool_band_source()` FAILing any drawn 問題1–6 item whose entry has no `src`. **This one is worth applying even though the paper defect closed** — the next paper reproduces the re-litigation otherwise |

**Effect on the loop.** S-1, R2-F1, the concurrency `PIPELINE-GAP`, NEW-1, NEW-2 and the F11 root cause
are `GATE-WRONG`/`GATE-BLIND`/`PIPELINE-GAP`/`RULE-MISSING`/`RULE-UNENFORCEABLE`
and therefore **block the next generation run** until applied or explicitly
rejected with a reason. **S-1 is the one to apply first**: it is a one-keyword
change, and until it lands, no paper's 読解-key paraphrase contract has ever
actually been checked.

---

## 9. Coverage statement

**Steps run, and on which files.** Step 0 (blind solve + both strategy passes) on
`qa/20260907_1/keyless.md` — rebuilt at the top of this pass from the three shas
in the header. **The 聴解 sources never moved** (`40cc36e44e6a` / `f458d9d2e216`,
mtimes 14:26 and 14:06). `言語知識・読解.md` moved twice under a concurrent
session and every load-bearing measurement was re-run against both new
revisions (§4B). Steps 1–3 on `言語知識・読解.md` — all 71
items, both key tables and every 解説 cell read. Step 4 on `聴解.md` (all four
構成表 read as COLUMNS, all five key tables) and `聴解スクリプト.txt` (all 51
blocks). Step 5 on `logs/topics.json` for this paper and the two before, plus the
shipped text. Step 6 on `test_spec.json` and `logs/ledger.json`. Step 6.5 in §8.

### The two mandatory blind STRATEGY passes (問題10–13, 18 items)

| strategy | my score | round 1's | bar |
|---|---|---|---|
| S1 — pick the option sharing the most character bigrams with its own passage | **7/18 = 38.9 %** (hits 54, 55, 57, 59, 60, 65, 67) | 6/18 = 33.3 % | fail above 45 % (official 32.8 %) |
| S2 — pick the second-longest option | **4/18 = 22.2 %** (hits 56, 59, 61, 65) | 3/18 = 16.7 % | fail above 45 % (official 24.6 %) |

Both pass. My S1 runs 5.6 points above round 1's because I normalised the
overlap by option bigram count rather than raw count; **the owning script settles
the metric that has an owner** — `tools/dokkai_profile.py` gives median overlap
margin (key − best distractor) = **−0.016** at the revision I solved and
**−0.012** at the current one, inside the ≤ 0.0 band both times, with strict
top-overlap key share 35.0 % against a band of ≤50 % (WARN >44 %). Note that
−0.012 is the thinnest margin of the last five papers (`20260904_2` −0.019,
`20260903_1` −0.177), and **two of my seven S1 hits are R2-F5's two items** —
the verbatim-lift finding and the overlap thinness are the same fact seen twice.

### Mechanical reads (§3), printed as the skill requires

| measure | value | band |
|---|---|---|
| 問題1/2/5 stems with no 「、」 | **14 / 15 (93 %)** | author ≥9; official 47–93 % |
| 問題1–5 stems in です・ます | **8 / 25** | author 7; official 2–11 |
| 問題1/2/5 stem median | 16 JP chars | current era 15–17.5 |
| 問題4 stem band | median 27, longest 30 | inside |
| 問題7 stem mean | **46.8** (was 45.5) | 36–52 |
| 問題7 stems under 34 chars | **2** (27, 29) | ≥2 |
| 問題7 stem spread (max−min) | **43** (70 − 27) | ≥25 |
| 問題7 options ≥3 chars printed in their own stem | **0 / 12** | round-1 F12 closed |
| 問題9 cloze body | 688 JP chars | 500–700 |
| 問題9 blank categories | 論理接続 / 文末モーダル / 慣用・形式名詞 / 内容推論 — 4 distinct, one [内容推論] | no two may share |
| 問題6 option set | mean 27.9, median 28, range 24–33, 2 over 30 | inside authoring target |
| 読解 in-body （注N） | **27** | floor 25, official 27–61 — **at the floor** |
| （中略） in 中文/長文 | 5 | ≥1 |
| `<ruby>` in 言語知識・読解.md | 0 | must be 0 |
| 読解 option-length ratio | all inside 1.65; none over 2.50 | WARN >1.65, FAIL >2.50 |
| (tied-)longest 読解 key | **6/20 = 30 %** (was 35 % at the revision I solved) | ≤35 % |
| uniquely-longest 読解 key | **2/20 = 10 %** (was 20 %) | ≤30 % (official 20 %) |
| 読解 lexical load | novel 15.3 % of 352 kanji-words, unglossed 7.4/1k | author ≤15.8 %, official cur 9.5–15.7 % — **at the edge** |
| 読解 kanji density / median sentence | 29.9 % / 35.0 chars | 24.5–31 % / 33–43 |

**聴解 mechanical reads are DESCOPED** (volume, register, talk length,
決め手の位置/種類, 質問型 mix, reaction ratio, longest-key rates). They were all
`ok` in the gate when the scope changed and I am not carrying the numbers
forward. The only two 聴解 lines I keep, because they are key-leak rather than
optimization, are:

| measure | value | band |
|---|---|---|
| 聴解問題1/2 closing turns give nothing away | **0 rhymes, 0 leaks** | must be 0 — no closing turn names its own key |
| 問題3 key-exclusive content tokens | **0** across the 24 spoken options | must be 0 — no word appears only in keys |

### Topic table (§5)

**Headline theme set** (問題9 / 問題12 / 問題13 / 問題14 / 聴解問題5-1番 / 5-2番),
re-derived from `logs/topics.json` and re-read against the shipped text:

| | 20260907_1 | 20260904_3 (1-back) | 20260904_2 (2-back) |
|---|---|---|---|
| 問題9 | 食 | 環境 | スポーツ・余暇 |
| 問題12 | 住まい | 科学・技術 | 人間関係 |
| 問題13 | 働き方 | 医療・福祉 | メディア・情報 |
| 問題14 | 旅行・観光 | 防災 | 地域活性化 |
| 聴解問題5-1番 | 行政・手続き | 交通 | 教育 |
| 聴解問題5-2番 | 文化・伝統 | 消費・経済 | 睡眠・健康 |

Intersection with 1-back: **∅**. With 2-back: **∅**. `exam-blueprint` rule 4's
zero-tolerance clause and the ≤1 allowance both satisfied. The repair round did
not disturb this.

**Within-paper subject repeats — the column that failed this paper in round 1,
re-derived:**

| round-1 repeat | status now |
|---|---|
| 紙→画面 ×3 | **×1** (問題2-3番 only) |
| 貸し出し ×2 | **×1** (問題14 only; the 聴解 half is now an incidental 「貸し出しのパソコン」) |
| バス/停留所 ×2 | **×1** as a subject (問題11(2)); 聴解's two 「バス」 are incidental attributes |
| 知らせの語順 ×2 | **×0** (問題3-例 re-angled to noticeboard selection) |
| 染め ×2 | **×2 — still present; DESCOPED (§4A)** |
| 北町町内会 ×2 | **×0** (three distinct bodies, one surface each) |

**Closing-move column** (13 surfaces): 説明2 / 随筆2 / 実用文・分類外2 /
意外な観察2 / 主張2 / 条件提示1 / 反論応答2 — all ≤2, closed vocabulary
respected, every label re-read against its own closing. Read again down
`FINAL_SENTENCE_TEMPLATES`: **1 hit** (問題10(2), 分裂文). Read a third time down
the PREDICATE FAMILY that failed round 1: **0 of 13**. Read a fourth time down
raw skeletons: **2 of 13 on 〜ていない — R2-F1.**

**`logs/topics.json` row — all eight required keys present, checked by grepping
the row rather than by any claim about it:** `surfaces` ✓, `themes` ✓,
`closing_moves` ✓, `voices` ✓, `claim` ✓, `persona` ✓, `shapes` ✓, `notes` ✓.
The row was re-derived from the shipped files by the build step and its
`closing_moves`/`themes` values are inside both closed vocabularies (gate `ok`).
Spot-read the two verifiable retellings against the items: 問題12(B)'s `claim`
correctly has the desk end up 「台所の入り口の柱のあたり」 and not 窓ぎわ (the
inverted-retelling defect `20260903_1` shipped), and 問題10(5)'s `surfaces` line
correctly quotes the *shipped* closing 「引き返す時刻は、どの店にも置いていない。」
rather than the discarded one. **Every string quoted in `notes` was grepped
against the paper; none is at 0 occurrences** — the `20260817_3` failure mode.

**A note not filed as a finding:** デジタル化 is the tag on **6 of 47 surfaces**
(問題10(1), 聴解1-2番, 2-3番, 3-1番, 3-5番, 4-9番) and 働き方 on 6. No rule caps a
tag across the whole paper — the theme rules bind 読解 surfaces (「no theme on two
読解 surfaces」, `ok`) and the six headline slots. The subjects behind the six
デジタル化 rows are now genuinely six subjects after the F2 repair, with the one
exception recorded as NEW-1 in §8.

### Provenance & spec audit (§6)

| check | result |
|---|---|
| `logs/ledger.json` ↔ `test_spec.json` | **field-for-field identical** on all 11 item categories (7/12/5/5/21/5/5/11/12/5/3 entries), seed `99970622+reroll-one(paraphrase:4,51963959)` and `pools_sha` `4119aed1e4b0` |
| `harvest_sha` | absent from both files, consistently — not a hand-written or date-shaped value |
| 問題1/2/4 target match | gate `ok` (21 targets); every recorded draw resolves to a `pools.json` entry (22 items) |
| `listening_scenarios` → shipped items | **21 drawn themes vs 21 shipped 聴解 slots, EXACT multiset match** (デジタル化4, メディア・情報2, 住まい2, 地域活性化2, 文化・伝統2, 環境2, and one each of 交通/医療・福祉/子育て・家族/旅行・観光/消費・経済/科学・技術/行政・手続き). Re-verified after the repair round moved seven 聴解 items: **no unrecorded substitution, no unused draw** |
| `reading_topics` → shipped surfaces | 12 drawn themes all shipped; the two extras in `topics.json` are expected — 食 is 問題9 (a cloze carries no drawn topic) and 住まい appears twice because 問題12(A)/(B) are two surfaces on one drawn topic |
| re-authored surfaces vs spec/ledger | **No `origin: "reauthored"` marker is required here, and I checked why rather than assuming.** Every `listening_scenarios` and `reading_topics` entry carries `origin: "authored"` with a `theme` and an `avoid` list — `exam-blueprint` authors these subjects rather than drawing them, so there is no drawn subject for a re-authored surface to contradict. No theme moved in the repair (聴解3-5番 is still デジタル化, 1-5番 still 医療・福祉, 2-5番 still 交通, 3-例 still メディア・情報), so the theme record in spec/ledger/`topics.json` still agrees three ways (gate: 「every theme recorded in test_spec/ledger agrees with logs/topics.json or says why (0 rows joined)」) |
| `answer_positions` | 101/101 match, and **no 読解 key digit moved in the repair** — the five key changes were option TEXT only. Note the gate's own caveat: slot agreement is zero evidence about content correctness, which step 0 and §6 supply |
| 問題14 apparatus vs 3 corpora | `check_q14_apparatus_reuse` `ok` (35 compared, no 20+ char shared run). Read by eye too: the 旅の道具貸し出し flyer shares no apparatus with official 7/2025's 公開講座 notice (no 定員/抽選, no 受付期間 split, no phone-to-check late route of that shape) or with `20260904_1/_2/_3` |
| copyright non-reproduction | Spot-grepped five distinctive shipped strings (「引き返す時刻は、どの店にも置いていない」「台所の入り口の柱のあたり」「手ぬぐいのはしをぬわない」「旅の道具の貸し出し」「応援を受ける課」) across all of `refs/` and every `tests/imported-*`: **0 hits each**. Gate `ok` on byte-identical （注N） lines, 例 blocks and 聴解 例 option lines. Invented figures read as the author's own N2-simplified inventions (三割ほど, 二千三百基, およそ二倍) — no decimals, no cited sources. **The seven re-authored surfaces' provenance scan was re-run here**, which is the clause the skill adds precisely because a pre-fix scan is evidence about text that no longer exists |

### 問題8 — all five items hand-verified for ★-uniqueness

`FREE UNITS` ≤1 on all five (44 is 0), `ARTIFACT: ok` on all five, no illegal
legs, and each 解説 carries a last-slot proof naming every card. Hand-checked the
forced junctions: 43 連体修飾 head + 形式名詞 次第 (and the one surviving rival
reads 「在庫が発送いたします」, a thing as the subject of a 謙譲語 — correctly
excluded); 44 連体形＋たびに and quotative と; 45 連体の＋わり and quotative と;
46 the 「AのにたいしてB」 呼応 template; 47 連体の + a floating 例えば.

**47 is the thinnest and I read it independently rather than accepting round 1's
verdict.** 18 of 24 orderings survive `verify_scramble`'s junction filter and
three rival ★ values (1, 2, 4) sit among the survivors. Only one of them is
grammatical *and* natural — (2)→(3)→**(1)**→(4), 「同じ話を二度聞かされたときの
自分の気持ちを、例えば思い出してみればいい」, ★=1 — and the 解説 excludes it on
scope: 「「例えば」を述部の直前に置く並びは、例示の範囲が「思い出してみればいい」だけに
縮み、リード文が予告した具体例が示されないことになるので取れない」. **I derived the
same exclusion before reading the cell**: 例えば must introduce the exemplifying
SITUATION (being told the same story twice), because the lead-in promises an
instance and no alternative actions are on offer for it to select among. The
exclusion is sound. The residual defect is the cell's other clause, 「文頭に固定」
— R2-F6. Also checked the zero-anaphora trap the skill names (`20260827_2` F1):
there is no 裸の「が」/「は」 card here, so no covert-subject rival to the final
card exists.

### `make check` — every line, with its resolution

Per-test block for this paper: **203 ok / 2 skip / 2 WARN.**

| line | resolution |
|---|---|
| ~~FAIL~~ `built HTML matches the Markdown it stamps` | **Fired at 16:43, now `ok`.** HTML built 16:34:03 against `acc50cca3281`; the Markdown moved to `00d5c0ef1607` at 16:43:04; the concurrent session rebuilt at 16:46:41. Verified green on my final gate run. Recorded because it was live for part of this review, not because it is open |
| WARN `聴解 keys paraphrase the script (3/5 verbatim token-matches)` | **DESCOPED** — recorded in one line in §4A (it is real, and it is 問題2-1番). Not analysed, no repair designed |
| WARN `聴解.mp3 pause distribution has a >1.05 s tail` | **DESCOPED** — not re-measured, not reasoned about (§4A) |
| skip `詳細解説.json options match the booklet` | Correct — stage 5 has not run and must not (instructed). `模範解答.html` absent, so `check_kaisetsu_no_scaffold_placeholders` is correctly inert |
| skip `詳細解説 prose contracts` | Same family |

Outside the per-test block:

| line | resolution |
|---|---|
| WARN `check_slot_theme_repeat`: 3 slots | **2-3番=デジタル化: FALSE POSITIVE** (a 20260904_2 電気店 whose air-con app stalls on an outdated instruction sheet, vs an internal stamp→screen approval order). **3-4番=文化・伝統: FALSE POSITIVE** (a 20260904_3 concert-venue entry announcement — itself a stretch of the tagger — vs a tenugui maker on unhemmed edges). **2-5番=交通: DESCOPED** (§4A; the four axes round 1 named had already been verified as differing). The two false positives above I re-checked against the other papers' own scripts rather than carrying round 1's verdict forward |
| WARN `every stamped spec's pools_sha matches pools.json` | Informational, as its own message states — expected after a pool repair; this paper's `4119aed1e4b0` **is** the current sha, so this paper is not among the 22 listed |
| skip ×2 (`errand key`, `問題8 form family`) | Structural: no drawn entry in the repo carries an errand key or a form-family tag, so there is nothing to compare. Pre-existing, not this paper's |
| **FAIL** `34 exam MP3(s) … ['20260907_1'] differ from what was uploaded` | **Not a paper defect, and out of scope by instruction** — this run was told not to run `make upload-files`. It must be run and `logs/upload_manifest.json` committed before the paper ships. Flagged, not resolved |

---

## 10. What was repaired, and what was rebuilt

**Nothing, by me.** No file under `tests/`, `logs/`, `tools/` or `.agents/` was
modified by this pass. `make keyless` was re-run once at the start (it writes
only to the gitignored `qa/20260907_1/`); `make check`, `make dokkai-profile` and
`make verify-scramble` are read-only. **`make mp3` was not run and will not be**
— per the scope change there is no 聴解 repair worth 44 minutes of synthesis in
this round. `make booklet`/`make sheet` were not run either (§4B).

**Something else did move**, and it was not this pass: a concurrent session
edited `言語知識・読解.md` twice (16:30:59, 16:43:04), `.gitignore`, seven other
tests' `.md`/`詳細解説.json`/`解答.html`/`模範解答.html`, and added
`tools/choukai_segment.py`. §4B has the full account, the three shas, and the
re-verification of every load-bearing measurement against the newest bytes.

`tests/20260907_1/` is entirely **untracked** in git (`?? tests/20260907_1/`), so
there is no committed revision to diff against — not the pre-repair files, and
not the pre-concurrent-edit ones. Every "before" figure in this report is
therefore quoted from round 1's report as a record, and every "after" figure is
my own measurement of the bytes on disk. I say so because it is the one place I
could not verify a claim two ways.

---

## 11. Skips, and why (AGENTS.md §0.7)

1. **No repairs applied.** Two of the four findings need an authoring decision
   (which of the two closings is re-cut in R2-F1; how the two 読解 keys are
   re-paraphrased in R2-F5). Making those choices in this context would make me
   author and auditor of the same fix, which `AGENTS.md` §5 says is never
   optional — and it matters *more* on the last fresh-eyes round, not less,
   because nothing downstream will re-read the fix. Of the two mechanical ones:
   **R2-F6** is one phrase in a 解説 cell and applying it alone would mean a
   booklet+sheet rebuild for it while two findings stayed open. It is named with
   the exact strings so it can be applied without re-derivation, and it should
   ride along with whichever rebuild applies R2-F5. **I also did not run the
   rebuild that the transient staleness FAIL called for** (§4B) — rebuilding
   against a file another context was still editing would only have produced a
   fresh mismatch; the concurrent session cleared it at 16:46 and the gate is
   green on it now.
2. **The whole 聴解 optimization half — descoped mid-pass by instruction.** The
   pause-distribution WARN, the 問題2-1番 key-paraphrase WARN, deferred items
   2/3/4 and claim R-2 are recorded in one line each in §4A and analysed no
   further; no substitute wording was designed and no repair proposed. What I
   kept there is correctness only: the 30-item blind solve, the key/position
   agreement, the four 例, and the two key-leak lines. **Stated explicitly
   because an unstated scope cut is indistinguishable from a skipped step**, and
   because the verdict must be readable as not depending on it (§12).
3. **`make mp3` not run, under any circumstances** (instructed).
4. **`.agents/` not edited.** `exam-qa-review` says the reviewer *may* edit its
   own SKILL.md directly and *should* when a defect class is missing — R2-F1's
   〜ていない skeleton, R2-F5's paraphrase rule (which the skill states but no
   working check has ever enforced), the one-writer-per-folder rule (§4B) and
   NEW-1's cross-half rhetorical move all qualify. **This run's instructions
   forbid touching `.agents/`**, and an explicit instruction from the caller
   overrides a skill's standing permission, so all four are filed as proposed
   edits in §8 instead. Flagging the conflict rather than routing around it —
   the same conflict round 1 flagged.
5. **`tools/check_consistency.py` not edited** (instructed). S-1 in particular
   is a one-keyword change whose founding-case run and full corpus run are
   already measured and printed in §8, ready to apply.
6. **`make upload-files` not run** (instructed). `make check` therefore still
   exits non-zero repo-wide on the un-uploaded MP3; this must be cleared before
   the paper ships.
7. **`make model-answer` / `詳細解説*.json` not touched** (stage 5, instructed).
   The two related gate lines correctly `skip`.
8. **`refs/` binaries never opened.** Every archive number here comes from the
   tracked `*.md` extracts and from `tests/imported-*`, both in git. This
   mattered once and I want it on the record: round-1 F11's new band records
   claim *absence* from four textbooks, and **absence from an OCR extract is not
   absence from the book**. I verified what the extracts can support (陽気 at
   見出し929 with both example sentences; 懸念/照会 at 0 across four extracts and
   31 sittings; 敏感's 5 archive hits) and I accepted the cells because they
   explicitly decline to turn that zero into a verdict — not because I opened a
   page. Nothing else was blocked on a missing binary.
9. **`tools/goi_profile.py` not run standalone** — `check_consistency.py` imports
   the same module and its per-test block prints the same numbers, quoted in §9.
   `dokkai_profile.py` I *did* run standalone, because the median-overlap-margin
   metric has a script owner and my own arithmetic disagreed with it (§9).
10. **The 20 読解 keys' axis column is a human judgment and is reported as one**
    (§3 R-3). I did not adopt round 1's proposed 8-of-20 threshold as a gate
    because it is not reproducible enough — the same keys read 10 by round 1 and
    8 by me. Rejecting a proposed edit with a reason rather than passing it on.
11. **The 読解/文法 half was not re-read line by line at the newest bytes.** The
    load-bearing measurements were (§4B), and the keys were confirmed identical
    across all three revisions, but §6's walkthrough rows are claims about
    `24fa4608e0b2`. If the concurrent session's edits went beyond the three band
    records and the option-length balancing I did detect, that half needs
    re-running on the settled file. I cannot rule it in or out without a diff,
    and the folder is untracked.

---

## 12. Verdict

**Does the verdict turn on the descoped 聴解 half? No.** All four findings are on
the kept side: R2-F1 and R2-F5 are 読解, R2-F6 is 文法, and S-1 is the gate check
behind R2-F5. **If every 聴解 item in this paper were declared perfect today, the
verdict would be unchanged.** The 聴解
items I did keep in scope came back clean: 30/30 blind-solve agreement, keys
matching `answer_positions`, all four 例 answerable and correctly announced, and
zero key leaks in the two lines that measure them.

The paper is materially better than round 1 read it. Both automatic fails are
closed, **eleven of round 1's twelve findings are closed** (F11 during this pass,
verified rather than accepted), the blind solve is clean at 101/101, and the
repair round's own collateral is far smaller than the defect it removed — the F1
predicate family went 6/13 → 0/13 and left one two-surface skeleton rhyme behind.

What blocks a PASS:

- **R2-F1 and R2-F5 are real 読解 defects** that no gate reported: R2-F5 because
  the check meant to catch it has never worked (S-1), and R2-F1 because the
  skeleton it lands on has no row in the template dictionary. Both are corpus
  maxima and both fail no official sitting, which is the standard this repo
  applies before believing a metric.
- **R2-F6** is round 1's own unapplied repair, which is the pattern round 1
  itself named.

Per `jlpt-test-generation`'s stage-4 loop rule, **a FAIL round with ≤3 findings
may be fixed directly, skipping re-review — and this round has exactly three,
none automatic, so the exception applies on its own terms.** That is the route I
would take, with the same rigour any fix gets: root-cause each, re-run
`make check`, sanity-read the diff. Recommended order:

1. **S-1** (one keyword in `tools/`) — until it lands, no paper's 読解-key
   paraphrase contract has ever been checked, and R2-F5 will keep shipping
   invisibly.
2. **R2-F5** — re-paraphrase 問題10-55's key off the notice's own sentence and
   soften 問題11-57's 15-char run. Both are single options.
3. **R2-F1** — re-close ONE of 問題10(5) / 問題11(4) onto another catalogued
   shape. This is the one I would argue hardest for despite its tier: it is the
   fourth paper on record to show repair collateral in the closing column, and
   leaving it makes this paper the founding case for a rule nobody applied to it.
4. **R2-F6** — one phrase, folded into the same edit.
5. **Rebuild last**: `make booklet 20260907_1 && make sheet 20260907_1` after
   steps 2–4 and after the concurrent session has stopped writing, then re-run
   `make check` and confirm the stamped shas match. The transient staleness FAIL
   of §4B is green as of my final run, but any edit above re-opens it.

One thing I cannot close and the coordinator must own: **whether the 読解/文法
half needs re-reading on the settled file** (§11.11). My findings survive all
three revisions, but a review of a moving target is not a review of the paper
that ships.

**QA: FAIL (3 findings, 0 automatic)**
