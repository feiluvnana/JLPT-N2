# 聴解 predictability audit — `tests/20260810_2`, item by item

Date: 2026-08-26. Read-only analysis; nothing under `tests/` was changed.
Scope: one paper, chosen because it is the one currently open in this session
(`詳細解説.json`/`詳細解説.vi.json` are mid-edit) and because it is already a
named, unrepaired entry in `logs/choukai_remediation_state.json`
(`P5C2-20260810_2`, tier C, status `todo`). This report is the item-level
evidence behind that ledger entry, answering one question per line: **can
this item's key be inferred without following the Japanese?**

**Method.** Every one of the 33 item blocks in
`tests/20260810_2/聴解スクリプト.txt` was read against its own key and 解説
cell in `聴解.md`, then checked against the rules already written in
`.agents/choukai-audio/SKILL.md` (register rules, banned-formula table,
決め手の位置 rule) and the cross-paper measurements in the 2026-08-20 audit
(`git show HEAD:REPORT-CHOUKAI.md`, uncommitted-deleted but still readable
from history) plus `tools/choukai_profile.py --tests 20260810_2 --json`. No
audio was listened to — findings below are about the **script text**, not
casting/pacing (問題5's casting is a separate, already-tracked axis, noted at
the end but not re-measured here).

**Headline verdict.** Confirmed: this paper is more solvable-by-pattern than
official. Two of its five sections (問題2, 問題4) carry a **one-way tell** —
a marker that is either always the answer or always wrong, present in most
of the section's items — on top of the already-documented 問題1
last-line/まず monoculture. 問題3 and 問題5 are comparatively clean.

---

## Ranked findings

### 1 — 問題2: every item's last line names the answer with the same rhetorical marker (SEVERE)

Six of the section's seven blocks (例, 1, 2, 3, 5, 6) close with a variant of
the identical device — the authority figure states the winning point using an
emphatic "this is it" phrase, delivered as (or immediately followed by) the
**last line before the repeated question**:

| # | Closing line | Marker family |
|---|---|---|
| 例 | 「ええ、そこが土台です。」 | そこが〜です |
| 1番 | 「ええ、そこが本当の分かれ目です。」 | そこが〜です |
| 2番 | 「ここだけは絶対。」…「とにかく、お名前。」 | 絶対／とにかく |
| 3番 | 「とにかく、二回分をまとめて、これだけは。」 | とにかく／これだけは |
| 5番 | 「はい、そこが目玉です。」 | そこが〜です |
| 6番 | 「ええ、それだけで伝わり方が変わりますよ。」 | それだけで |

A solver who has learned this ONE template ("listen for そこが／これだけは／
とにかく／絶対 near the end, pick the option it names") answers 6 of 7 items
correctly without tracking the rest of the dialogue — a stronger shortcut
than 問題1's last-line pattern below, because it is a **repeated lexical
marker**, not just a structural position. Only **4番** (the 何によって決めたか
item) breaks the template — it has no 一番/emphatic-marker framing at all,
which is also why it is the one item whose question form differs (see #4).

### 2 — 問題4: an "already done" distractor is a one-way tell in 6 of 11 items (SEVERE)

A distractor that claims the requested action **has already been completed**
appears in 6 of the 11 scored items, and in every one of the 6 it is the
**wrong** answer — never once the key:

| # | Stimulus (what's asked/requested) | "Already done" distractor | Correct instead |
|---|---|---|---|
| 3番 | 山田さん、書類を今日中に英訳してもらえる？ | 2「その書類は、もう英訳しておきました」 | 1（すぐ取りかかります） |
| 4番 | そろそろお引き取りください | 2「お会計は、さっき済ませましたが」 | 3（すぐ出ます） |
| 7番 | 社長、間もなくご到着 | 1「社長は、もう到着されているんですね」 | 3（会議室に案内してくれ） |
| 8番 | 試着室、こちらをご利用ください | 2「試着室は、もう使い終わりました」 | 1（着てみますね） |
| 9番 | 戻られたら伝言をお伝えいただけますか | 2「鈴木は、もう出社しております」 | 1（承知しました） |
| 10番 | 割り勘にしようよ | 2「会計は、もう店の人に伝えてあるよ」 | 3（そうだね） |

(`choukai_profile.py`'s automated counter reads 8/11 on a looser regex; the
6 above are the ones a human read confirms fit the pattern exactly — either
count is far past `choukai-audio` §Register rule 5's "rotate the device"
instruction, which exists precisely so no single kill-device becomes
learnable.) A test-taker who has never heard of this paper but has taken
enough JLPT mocks to notice "the もう-option is always the trap" starts 問題4
with a real, exploitable edge in most of the section — a shortcut official
audio does not offer at this rate (REPORT-CHOUKAI.md's own November-2025-era
measurement capped a healthy paper at "archive median 1, max 3" for this
exact device).

### 3 — 問題1: 100% まず framing, and the decider sits in the item's last 1–2 lines every time (HIGH, already tracked)

Confirmed independently in the previous turn of this session and repeated
here for completeness — see the per-item table below. All 6 blocks (incl.
例) ask 「この後まず何をしますか」 (`q1_mazu_share` = 1.0), and in every one the
correct action is the speaker's final line, or is restated there after being
set up 1–2 turns earlier. Two items (例, 1番) pivot on the identical word
それより. This is exactly the failure `choukai-audio` §Register rule 6 was
written to ban (2026-08-18) — this paper predates the rule (generated
2026-08-10).

### 4 — 問題2 question-type monoculture: 5 of 6 scored items are 一番-framed (HIGH, matches known F3)

`q2_forms` for this paper: 一番・優先 4, 理由 1, 内容・発言 1 — but reading the
actual question lines, **1番 also carries 一番** ("一番の理由"), so 5 of 6
scored items (1, 2, 3, 5, 6) use a 一番/最も-superlative frame. The prior
cross-paper audit (REPORT-CHOUKAI.md §F3) measured official's 一番・優先 share
at 6%; this single paper runs it at over 80% of its own section. This is the
same root cause as Finding #1 — a 一番-framed question all but requires the
dialogue to contain an explicit "this is the most important one" line, which
is exactly the marker Finding #1 documents.

### 5 — 問題3: 100% institutional speaker, 100% one voice (MEDIUM — register, not a key-guessing shortcut)

All 6 blocks (incl. 例) are an institutional/expert monologue (市の担当者,
アナウンサー ×2, 専門家, レポーター ×2), and `voice_balance` shows 問題3 resolves
to 0 male / 6 female turns — every talk is read by the same voice as the
announcer. This does not hand a solver the key the way #1–#4 do (概要理解
still requires matching the one paraphrased option against the talk's
topic), but it flattens the section into one register and removes any
signal a listener could get from speaker type or voice, which is a
documented cross-paper drift (REPORT-CHOUKAI.md §F5/F7) rather than a new
finding.

### 6 — 問題5: clean on the predictability axis

1番's elimination sequence (4 candidates, each killed by one distinct
reason — cost, staffing, a competitor already there — before the survivor is
adopted) is the expected shape for a single 3+-speaker discussion item, and
with only one such item in the paper there is no cross-item monoculture to
measure. 2番 enumerates candidates in the same order they're read back,
decides by named attribute (駅から近い→さくら町, 公園そば・静か→川辺) rather than
by ordinal, and answers the two questions with two different rooms — all
compliant with `choukai-audio`'s 問題5 rules. The remediation ledger's open
item for this test, "問題5-2番 casting", is a **pitch/voice-separation**
concern (an audio-casting question this report did not re-measure, since it
requires listening or a pitch-margin script pass, not a script-text read) —
unrelated to key-inference and not double-counted here.

---

## Every item, in order

Position column: where the deciding line sits relative to the block
(early / mid / **last** = final substantive line before the repeated
question or, for 問題4, before the reply options).

### 問題1 課題理解 (question form: 100% この後まず何をしますか)

| # | 場面 | 正解 | Decider position | Tell |
|---|---|---|---|---|
| 例 | 図書館 | 3 | **last** | それより pivot; distractors killed by "later/already answered" |
| 1番 | 家具店（電話） | 1 | **last** | それより pivot; distractor killed by "後回し" (deferral) |
| 2番 | 会社（仕様変更） | 2 | **last** (restates a mid-turn instruction) | deferral ("保留", "後回し") |
| 3番 | 交番 | 3 | **last** (restates an early instruction) | deferral ("後で", "交番が引き受け") |
| 4番 | 体育館受付 | 3 | **last** (restates a mid-turn instruction) | deferral ("当日でよい", "記入が先") |
| 5番 | 信用金庫 | 4 | **last**, adjacent to the decider one line earlier | deferral ("受け取ってもらえない", "後", "その後の段階") |

Every wrong option across all 6 items is killed by the same device: it names
something that happens **later**, not something untrue. `choukai-items.md`'s
消去方法 rotation (reassign / defer / refuse / already-done) is present only
in its "defer" form here — a second monoculture layered on top of Finding #3.

### 問題2 ポイント理解 (see Findings #1, #4 for the cross-item pattern)

| # | 場面 | 正解 | Decider position | Marker |
|---|---|---|---|---|
| 例 | ラジオ：給食アレルギー対策 | 2 | **last** | 「そこが土台です」 |
| 1番 | 保険窓口 | 2 | **last** | 「そこが本当の分かれ目です」 |
| 2番 | 会社：セミナー受付 | 3 | mid, restated **last** | 「ここだけは絶対」／「とにかく、お名前」 |
| 3番 | 薬局 | 1 | mid, restated **last** | 「とにかく…これだけは」 |
| 4番 | 会社：海外会議の時間 | 4 | distributed, resolved at 「結局〜に落ち着きました」 | none — the one item without the marker |
| 5番 | 銀行 | 1 | **last** | 「そこが目玉です」 |
| 6番 | 社内研修 | 2 | **last** | 「それだけで伝わり方が変わりますよ」 |

### 問題3 概要理解 (all institutional, all one voice — Finding #5)

| # | 場面 | 正解 | Speaker type |
|---|---|---|---|
| 例 | ニュース：自動運転バス実証運行 | 3 | レポーター (institutional) |
| 1番 | 地域ニュース：見守り機器設置費補助 | 3 | 市の担当者 (institutional) |
| 2番 | ニュース：孤独・孤立の調査 | 3 | アナウンサー (institutional) |
| 3番 | ラジオ：定期購入の解約トラブル | 1 | 専門家 (institutional) |
| 4番 | 地域情報番組：祭りの担い手不足 | 4 | レポーター (institutional) |
| 5番 | ニュース：オンライン診療の法整備 | 2 | アナウンサー (institutional) |

Distractor pattern here is healthy — each wrong option is a topic simply
never mentioned in the talk, not a paraphrase trap, which matches official's
概要理解 shape and is not being flagged as a defect.

### 問題4 即時応答 (Finding #2 for the one-way もう-tell)

| # | Stimulus role | 正解 | もう/already-done distractor? |
|---|---|---|---|
| 例 | 男（席） | 1 | no |
| 1番 | 係員（案内） | 1 | no |
| 2番 | 店員（案内） | 2 | no (opt1 declines, not "already done") |
| 3番 | 男（依頼） | 1 | **yes — opt2, wrong** |
| 4番 | 店員（退店案内） | 3 | **yes — opt2, wrong** |
| 5番 | 妻（報告） | 2 | no |
| 6番 | 担当者（確認） | 2 | no |
| 7番 | 部長（報告） | 3 | **yes — opt1, wrong** |
| 8番 | 店員（案内） | 1 | **yes — opt2, wrong** |
| 9番 | 女（伝言依頼） | 1 | **yes — opt2, wrong** |
| 10番 | 男（提案） | 3 | **yes — opt2, wrong** |
| 11番 | 部長（褒め言葉） | 2 | no |

### 問題5 統合理解 (Finding #6 — clean)

| # | 場面 | 正解 | Notes |
|---|---|---|---|
| 1番 | 企画会議（3話者） | 2 | 4-candidate sequential elimination, expected shape for this item type |
| 2番 質問1 | 不動産屋（兄） | 1 | decided by named attribute (駅から近い), not ordinal |
| 2番 質問2 | 不動産屋（妹） | 3 | decided by named attribute (静か・公園そば), not ordinal |

---

## Where this belongs

- Root cause and existing rules: `.agents/choukai-audio/SKILL.md` §Register
  rules 5 (kill-device rotation) and 6 (decider position), and the
  banned-formula table — this paper predates several of them.
- 問題2's 一番 monoculture: owner is
  `.agents/question-authoring/references/choukai-items.md` §Section item
  mix (the quota table REPORT-CHOUKAI.md §F3 already flagged as needing a
  content/reported-statement quota).
- This paper's repair is already queued: `logs/choukai_remediation_state.json`
  → `P5C2-20260810_2` (tier C, `<section re-author>`, status `todo`). This
  report supplies the item-level "why" for that entry; it does not change
  its status or perform the rewrite.
