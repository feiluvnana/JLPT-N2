# 20260914_1 — stage-2 author hand-offs (verbatim, for stage 3)

These are the three authors' OWN reported tables, recorded here because
`jlpt-test-generation` §"Stage 3" needs them and an orchestrator's paraphrase is
the documented mis-key mechanism. **Everything below is a CLAIM by the context
that wrote the fragment. Stage 3 must re-derive from the files on disk anything
it acts on** — these rows say where to look, not what is true.

## 文法 author — keyed forms and frames, for the cross-half re-grep

`jlpt-test-generation` §"Stage 3": after ANY edit to 問題10–14 prose, re-grep
every 問題7/8/9 keyed form across the whole 読解 half and record the counts AND
the frames. The author could not do this itself (the 読解 half was being written
in parallel, in another context), so this is stage 3's to run.

| Q | keyed form | frame | as printed |
|---|---|---|---|
| 31 | 〜ものか | 文末 | するものか |
| 32 | 〜ことはない | 文末 | 落ち込むことはない |
| 33 | 〜一方だ | 文末 | 減る一方だ |
| 34 | 〜上で | 連用 | お読みになった上で、ご記入ください |
| 35 | 〜に限って | 連用 | 置いてきた日に限って雨になる |
| 36 | 〜もかまわず | 連用 | ぬれるのもかまわず、… |
| 37 | 〜ながらも | 連用 | 弱りながらも、… |
| 38 | 〜ずにはいられない | 文末 | みずにはいられなかった |
| 39 | 〜にもかかわらず | 連用 | 冷たい雨にもかかわらず、… |
| 40 | 〜次第だ | 文末 | 天気次第です |
| 41 | 〜わけにはいかない | 文末 | 休むわけにはいかない（＋終助詞よ） |
| 42 | 〜というものではない | 文末 | なるというものではない |
| 43 | 心理変化「〜意欲が湧いてくる」 | 文末（★card は連体） | 意欲が湧いてくる |
| 44 | 〜おかげで →「〜おかげだと」 | 連用・引用節内 | おかげだと今でも思っている |
| 45 | 〜をきっかけに | 連用（★card は連体/辞書形） | 〜のをきっかけに |
| 46 | 〜に沿って…進める | 連用 | 日程に沿って進めてまいります |
| 47 | 〜ほど〜はない | 文末（★card は連体） | 〜ときほど…時間はない |
| 48 | したがって | 接続詞・文頭 | したがって |
| 49 | 〜ないことには | 連用・従属節 | 開いてみないことには |
| **50** | **〜ずに済む** | **文末 — the ONLY 問題9 文末モーダル key** | **せずに済む** |
| 51 | （内容推論・名詞句） | 連体修飾＋名詞 | 人が覚えておく仕事 |

> "**The one string stage 3 must grep as a 文末モーダル across the merged paper is
> 「せずに済む」/「〜ずに済む」 (問題9-50).** 51's key is a noun phrase, not a
> modal. All 12 問題7 keys and the 5 問題8 targets above must also not recur as
> keys or in 読解 prose."

The author also flagged, unprompted, the one thing it wanted a fresh read on:
> "`せざるを得ない` also appears as a distractor at 問題7-41; cross-大問 distractor
> reuse is neither gated nor forbidden, but it is the one thing in this fragment
> I'd flag for a fresh-eyes read."

And, for `logs/topics.json`'s `notes` (bunpou.md requires the sixteen-option
comparison be recorded there; the author could not write that file):
> "**Stage 3 should paste the four option rows above into that row.**"
The four 問題9 option rows are in `tests/20260914_1/_sections/問7-9_文法.md` —
read them from there, do not retype them.

## 読解 author — the thirteen-row column as SHIPPED

Reproduced in `qa/allocation-20260914_1.md` as PLANNED; the author's shipped
column matched it row for row, with one stated interpretation:

> "One allocation row needed interpretation, stated rather than re-labelled:
> 10(2)'s prescribed final 「…ためだという。」 is written in です・ます as
> 「…ためだといいます。」 (same skeleton, same hearsay-cause close) because the
> row's assigned voice is です・ます."

Author-reported tallies to VERIFY, not to trust: no closing shape >2, no
template >2, not-A-but-B family exactly 2 (問題10(4), 問題11(2)), 〈想定→実は〉
exactly 2 (問題10(2), 問題13), です・ます 5 of 12 passages, （注N） 32 markers,
指示語 stem at 問62, span-anchored stem at 問68, **zero** absolute-quantifier
options kept, key rank 30/25/25/20 %.

Two length bands the author says are near their ceilings and named as the first
things to re-check if stage 3's counter disagrees:
> "問題11 sits at 2676 against the 2700 ceiling and 問題10 at 1319 against 1330 —
> if stage 3's counter differs from mine by more than ~10 chars, those two are
> the ones to re-check first."

## 文字・語彙 author — the rerolled item

問題3-13 was re-authored after the orchestrator's `--reroll-one word_formation:2`
(see `qa/stage3-report-20260914_1.md` for the defect and the root cause). The
author re-ran the gate's own `goi_profile.option_reuse` afterwards and reports it
empty, with 問題3's three keys now 圏 / 別 / 版.
