# QA Report — 20260817_3 (round 2, fresh-eyes)

Reviewed revision:
- `言語知識・読解.md` sha1 `09abaea058359743a618aef853fe97bc3b5d5ce1` (mtime 2026-08-18 18:42:23)
- `聴解.md` sha1 `3df152b5d618790c515ac1847e245cb9500a4b4a` (mtime 2026-08-18 18:37:13)
- `聴解スクリプト.txt` sha1 `55361ffa7c57658f5a34765d0db72be30548ccb7` (mtime 2026-08-18 18:22:53)
- Report started 2026-08-19. Reviewer: fresh-eyes Stage 4, round 2 — authored nothing in this paper, wrote none of round 1's report, received no summary of author intent.

## Verdict

**QA: FAIL (4 findings, 0 automatic)** — findings N2, N3, N5, N6, all Minor or Trivial. 14 of round 1's 15 findings verified closed; blind solve 101/101. Full reasoning in Section 9.

Artifact ordering (staleness check): `聴解スクリプト.txt` 18:22:53 → `聴解.mp3` / `聴解_チャプター.json` 18:28:55 → `聴解.md` 18:37:13 → all HTML 18:42:23. No artifact predates its source. OK.

Solved from: `qa/20260817_3/keyless.md` (built by `make keyless 20260817_3`, 1069 lines).

---

## Section 0 — Blind solve (written BEFORE opening any key)

### 言語知識・読解 (1–71), answered from keyless.md only

| # | ans | # | ans | # | ans | # | ans |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 19 | 1 | 37 | 4 | 55 | 2 |
| 2 | 4 | 20 | 4 | 38 | 1 | 56 | 2 |
| 3 | 1 | 21 | 2 | 39 | 2 | 57 | 2 |
| 4 | 4 | 22 | 4 | 40 | 1 | 58 | 1 |
| 5 | 1 | 23 | 1 | 41 | 4 | 59 | 3 |
| 6 | 3 | 24 | 1 | 42 | 3 | 60 | 3 |
| 7 | 4 | 25 | 3 | 43 | 4 | 61 | 1 |
| 8 | 3 | 26 | 1 | 44 | 3 | 62 | 4 |
| 9 | 1 | 27 | 2 | 45 | 1 | 63 | 2 |
| 10 | 4 | 28 | 4 | 46 | 1 | 64 | 2 |
| 11 | 3 | 29 | 2 | 47 | 4 | 65 | 3 |
| 12 | 3 | 30 | 4 | 48 | 3 | 66 | 3 |
| 13 | 2 | 31 | 1 | 49 | 2 | 67 | 1 |
| 14 | 1 | 32 | 3 | 50 | 3 | 68 | 4 |
| 15 | 1 | 33 | 2 | 51 | 4 | 69 | 4 |
| 16 | 4 | 34 | 1 | 52 | 4 | 70 | 2 |
| 17 | 3 | 35 | 2 | 53 | 3 | 71 | 2 |
| 18 | 2 | 36 | 2 | 54 | 4 |  |  |

Flat list 1–71:
`3,4,1,4,1,3,4,3,1,4,3,3,2,1,1,4,3,2,1,4,2,4,1,1,3,1,2,4,2,4,1,3,2,1,2,2,4,1,2,1,4,3,4,3,1,1,4,3,2,3,4,4,3,4,2,2,2,1,3,3,1,4,2,2,3,3,1,4,4,2,2`

(聴解 answers appended below after solving from the embedded script.)

### 聴解 (30 items), answered from the embedded `聴解スクリプト.txt` in keyless.md

問題1: 例=1 / 1番=2, 2番=3, 3番=2, 4番=1, 5番=3
問題2: 例=2 / 1番=4, 2番=2, 3番=3, 4番=2, 5番=1, 6番=4
問題3: 例=2 / 1番=3, 2番=3, 3番=3, 4番=1, 5番=4
問題4: 例=2 / 1番=2, 2番=3, 3番=2, 4番=1, 5番=2, 6番=3, 7番=2, 8番=2, 9番=3, 10番=3, 11番=1
問題5: 1番=1 / 2番 質問1=2, 質問2=4

Flat 聴解 list (問1 1-5, 問2 1-6, 問3 1-5, 問4 1-11, 問5 1番/質問1/質問2):
`2,3,2,1,3, 4,2,3,2,1,4, 3,3,3,1,4, 2,3,2,1,2,3,2,2,3,3,1, 1,2,4`

Blind solve complete and recorded. Only now opening the sourced Markdown.

### Blind-solve diff

Evaluated with `python3 tools/qa_eval.py tests/20260817_3 --answers "[...]"` and re-verified by parsing the 正解 columns out of `言語知識・読解.md` (71 rows) and `聴解.md` (30 rows) directly.

**Result: 101 / 101 agreement. Zero mismatches, zero findings from step 0.**

(`qa_eval.py` reported "106 scored items / 5 discrepancies"; items 102–106 are the parser mis-reading five non-key numbers (306/325/337/318/295 — not in 1–4, so not options) out of the 聴解 tail. That is a `qa_eval.py` defect, filed as F-N4 below, not a paper defect.)

A 101/101 blind solve is a strong signal but **not** a pass: it proves each key is *findable*, not that it is *unique*. Steps 1–2 below carry that burden.

---

## Section 1 — Round-1 F1–F15 closure, verified against the artifact

Method: for each finding I re-derived the defect from the shipped files, not from any claim that a fix was made. `logs/topics.json` notes and the `セクション構成表` were treated as claims to be checked, not evidence.

| # | Round-1 defect | Status | Evidence from the shipped artifact |
|---|---|---|---|
| **F1** | 問題8-44 had a second grammatical ordering (★ could be 4) | **CLOSED** | Card 1 is now 「部屋を見るだけでなく」 (was 「実際に部屋を見て」). Only 1-2-3-4 survives: 「部屋を見るだけでなく」 cannot precede 「うえで」 (だけでなく takes no 〜うえで), cannot sit last before 「決めようと思う」, and 「周りの環境**も**」 needs it as antecedent. I enumerated the alternatives that round 1 named — 2-3-4-1 now reads 「周りの環境も自分の足で確かめたうえで部屋を見るだけでなく決めようと思う」, ungrammatical. ★ = slot 3 = card 3 = key **3**, as shipped. The 解説 (line 527) now states the last-slot bar explicitly. |
| **F2** | 問題4-16 key + set were N3–N4 (姿/跡/光/影) | **CLOSED** | Whole 問題4 re-drawn via `+reroll(context_words,79773993)` (recorded in `test_spec.json` seed). New set 引き分け/手数料/研修/読書家/しぼむ/道徳/いきなり. 影 deleted from `pools.json` `context_words` (`git diff` shows exactly that one deletion). Level: 棄権・勝ち越し・逆転勝ち, 保証金, 見習い, 努力家/愛好家/専門家, ほどける/しぼむ, 道徳/礼儀/権利, 徐々に/あらかじめ/たびたび are all N2-band; no set is four N3–N5 words. Keys sit at spec positions [1,1,4,3,2,1,4] ✓. See N1 below for the one residual level note (いきなり). |
| **F3** | Five 読解 closings on one 「A そのものではなく B」 skeleton | **CLOSED** | `そのものではなく` now occurs **0** times in the whole 読解 half; `ではなく` occurs twice and both are **mid-passage** (問題11(3)「本人が書いたものではなく、他人が…」, 問題13「代わりに置かれるものではなく…」), never in a final sentence. I re-read all 13 finals: 問題9=理由提示(〜ためだ) / 10(1)=事務的締め / 10(2)=注記 / 10(3)=問いの再定義(つまるところ〜という問いである) / 10(4)=定義の置き換え(私が今そう呼びたいのは〜である) / 10(5)=帰結提示(〜持てる) / 11(1)=情景回帰(手はまだ覚えている) / 11(2)=留保つき再確認(それでも〜保たれている) / 11(3)=情景回帰(指を置く) / 11(4)=A だけではない。B こそが / 12A=主張再提示(〜が現実的である) / 12B=主張再提示(〜条件になる) / 13=対比例示(A では…になり、B では…になる). Sentence-final predicates spread である×3, 〜ている×2, 〜になる×2, plain 〜る×3, 〜と言える×1. Gate's `REFRAME_CLOSING` proxy: **1 matched** (cap 2). |
| **F4** | 聴解問題1 消去方法 device over cap (別の人に割り当て ×4) | **CLOSED (one residual, see N2)** | Re-verified by reading the script, not the table. Tokens across all 6 rows: 既に完了 2, 実行不可 2, 順番待ち 2, 不要 2, 条件不足 2, 後回し 2, 別の人に割り当て 2, 規則で不可 2, 明確に否定 1. No token above 2. 「別の人に割り当て」 now only 2番(林くん)/3番(川口さん) — 例's camera moved to 実行不可 (「貸し出し用のカメラ、今ぜんぶ点検に出ちゃってて、当日は使えないの」) and 5番's copy/interview moved to 不要/明確に否定. The 構成表 also adopted a closed token vocabulary, which was round 1's own proposed fix. |
| **F5** | 問題1 closing turns rhymed; last line named the key's keyword | **CLOSED** | Last spoken line per item: 例「それは、あとで一緒に書き込もう。」/ 1番「練習は明日でいいよ。」/ 2番「はい、わかりました。」/ 3番「じゃあ、さっそく取りかかります。」/ 4番「お手数をおかけしますが、よろしくお願いいたします。」/ 5番「はい、お待ちしております。」— six different skeletons, 「はい、〜ます」 once. Keyword leak: no last line contains a ≥2-char kanji/katakana token occurring in exactly one printed option (ノート/はがき/家に取りに戻る all gone). 1番's last line contains 練習, which points at a **wrong** option (opt 3, printed as れんしゅう in kana anyway). |
| **F6** | 聴解問題2-1番 repeated 20260817_2's moving-quote errand | **CLOSED by re-angle — accepted, with the pool defect still live** | Reviewed on its merits per instruction. Shipped item: 「会社の休憩室で、女の人と男の人が話しています。女の人は、どうして引っ越しの見積もりが思ったより高くなったと言っていますか。」 The changed axes are real and all four move together: speakers (colleagues, no vendor present), register (くだけた, not 敬語), question class (理由型 ポイント理解, not 課題理解), and tense (post-quote explanation, not pre-quote task). Nothing in the dialogue is a transaction. The gate's own errand check `no 聴解1/2/3/5 errand repeats 20260817_2's` is **ok**. What remains is the **noun** 「引っ越しの見積もり」 recurring one paper apart — real but thin. I accept the re-angle. What I do **not** accept as closed is the root cause: `pools.json` still carries `引越し:見積もり`, `引っ越し業者との見積もり調整` and `引っ越し業者との調整` as three separate entries, so the cooldown will hand out the same errand again (see RC-2). |
| **F7** | 問題9 repeated 20260817_2's 行政・手続き 読解 subject | **CLOSED** | 問題9 rewritten to 「値段と量」 (実質値上げ／内容量削減). `logs/topics.json` 問題9 theme updated 行政・手続き → 消費・経済, and `surfaces` updated to match the shipped passage. No 窓口/申請書/記入 content survives: the words 申請書・窓口・記入 appear **0** times in the 読解 half. |
| **F8** | 問題9 thesis echoed 聴解問題4-1番 (申請書の書き方) and 聴解問題2-5番 (用紙を廃止) | **CLOSED** | Same rewrite. 問題9 is now about price vs. quantity; 聴解問題4-1番's 申請書 stimulus and 聴解問題2-5番's abolished sign-out sheet no longer share a subject with any 読解 surface. |
| **F9** | 問題2-9 grid {運,雲}×{河,海} — 運海/雲海 read うんかい, two free eliminations | **CLOSED** | Shipped set is 運河/運賀/雲河/雲賀, grid {運,雲}×{河,賀}. 運=ウン, 雲=ウン, 河=ガ, 賀=ガ — all four parse as the stem kana うんが. 解説 (line 488) states the kana-skeleton claim explicitly. |
| **F10** | 問題9-51 keyed 「そうとは限らない」 while 問題11(4) printed 「〜とは限らない」; 問題9-48 keyed ところが, used 3× in 読解 prose | **CLOSED** | 問題9 keys are now その反面 / はずだ / 損なわれやすくなる / 本末転倒だ. In the whole 読解 half: 「その反面」 0 hits, 「本末転倒」 0, 「はず」 **1** (問題12A 「姿を消したはずの種が」 — 連体 frame, not the 文末 frame the item keys). 「とは限らない」 survives once in 問題11(4) but is no longer any key. 問題7/8/9 keys do not collide with each other. |
| **F11** | 聴解問題2-2番 key reused the script's own verb 回す | **CLOSED** | Script rewritten: 「よそ」「業者」「あずけ」「回す」 all occur **0** times in `聴解スクリプト.txt`. Deciding lines are now 「しみ抜き専門の工場に一度出すことになるんです」 + 「店の中だけでは仕上げられない品なので」; key is 「よその業者にあずけるから」 — two independent substitutions (工場→業者, 出す→あずける). `logs/topics.json` note (c), which says 「よそ」 still shares with the script, is **stale** (see N3). |
| **F12** | 聴解問題4-5番 key carried an unstated premise (伺いたいことがありました) | **CLOSED** | Key is now 「とんでもないです。ちょうどお待ちしていました。」 — presupposes nothing beyond the prompt (a caller was expected). Distractors 1 (asks how long the busy period lasts) and 3 (offers to reschedule) still fail on their own grounds. |
| **F13** | 問題5-21 option 2 was the marked 「手先が上手だ」 | **CLOSED** | Option 2 is 「細かい作業が得意だ」 — exactly round 1's proposed wording, an idiomatic phrase on its own. Key position 2 preserved. |
| **F14** | 構成表 inaccurate: (a) 問題1 消去方法 undercount, (b) 問題3 talk lengths (311–353) did not reproduce | **CLOSED** | (a) The tally now enumerates all nine tokens with their row ids, and I reproduced it from the script. (b) The table now prints **both** measures per talk (gate measure `p3_talk_chars` 295–337, punctuation-stripped 274–313) and explicitly retracts the old 311–353 figure as having wrongly included the question line. The table also added a quotation convention marking pre-fix strings with 〈旧〉. This is a genuinely better artifact than round 1's. |
| **F15** | 問題4 already-done distractor shape at 3 by intent (もう/もう/先ほど); fix assigned to the rule | **OPEN (skill), paper acceptable** | Verified: the rule text was **not** changed — `choukai-items.md:364` still reads `≤2 items may carry an already-done (もう/すでに/さっき + 〜た) distractor`, and `git log -- .agents/` shows no commit after round 1. The paper still ships 3 items of that shape (1番「その申請書はもう受け付けました」, 3番「数字はもう全部消しときました」, 4番「その書類は先ほど郵便で送りました」) and the 構成表 counts 2, correctly under the rule as written. **Paper verdict: acceptable.** 3 of 24 distractors cannot make the shape scoreable (the rule's own incident band is 8/11 and 9/11), and the gate's own official band is "median 1, max 3". **Skill verdict: still open** — it blocks the next generation run per exam-qa-review §6.5, not this paper. |

**Closure score: 14 of 15 closed at the paper level; F15 remains open as a skill defect only.** No fix introduced a new defect that I could find, with the two small exceptions logged as N2 and N3 below.

---

## Section 2 — Rulings on the two escalated judgement calls

### Ruling A — 問題9-51's 四字熟語 options under the `[慣用・形式名詞]` tag: **NOT a category error. The item stands.**

`bunpou.md` (lines 144–145) defines the category as:

> **(d) 慣用/形式名詞** — a set phrase or formal noun (つもり, 元も子もない, 願ってもない…).

The category is explicitly a **disjunction**: *set phrase* OR *formal noun*. Two of the three worked examples the owning file gives — 元も子もない and 願ってもない — are lexical idioms, not formal nouns, and both occupy exactly the slot 51 occupies: a fixed evaluative predicate closing a 〜のでは / 〜では clause. 一石二鳥だ / 一長一短だ / 二者択一だ / 本末転倒だ are 四字熟語, which is a *kind* of 慣用句. They therefore sit inside (d) as the owning file writes it, and the tag is correct rather than a relabel of convenience.

Three supporting checks, all of which the item passes:

1. **Format scale.** All four options are 5 JP chars. `bunpou.md`'s bar is ≤14 (official max), gate FAILs above 16. The failure mode the rule guards against — options that read like 読解 主張 summaries — is absent.
2. **No category collision.** The four tags are `[論理接続]` 48 / `[文末モーダル]` 49 / `[内容推論]` 50 / `[慣用・形式名詞]` 51 — four distinct, exactly one 内容推論. Gate green, and I re-derived it.
3. **Discrimination is on the tested point, not on vocabulary trivia.** The stem 「客に買い続けてもらうための**売り上げ**なのに、その売り上げを守ろうとして中身を削るのでは、（　）」 states an ends/means inversion in the sentence itself; 本末転倒 names exactly that. 一石二鳥 is positively valued and collides with 第4段落's 「二か月後に一割以上落ち込んだ」; 一長一短 asserts a mixed property, which the passage never grants the tactic; 二者択一 describes the *choice* stage the passage located back in 第2段落 (「作り手には二つの道がある」), not the consequence. One defensible answer.

The one thing I would flag to the skill rather than to the paper: (d) as written invites this question every time, because "set phrase" is not enumerated. **Proposed edit** to `bunpou.md` §(d): add the sentence *"四字熟語 used as a sentence-final evaluative predicate (本末転倒だ, 言語道断だ) count as set phrases and belong here; what (d) excludes is a content noun standing in for the thesis."* Filed as RC-5.

### Ruling B — 問題7 stem length and dispersion: **YES, this is a finding.** Filed as **N5 (Minor)**.

Measured on the shipped file, JP chars only:

| | this paper | official 7/2025 (measured by the same function) | official 12/2025, first 6 stems |
|---|---|---|---|
| 12-stem mean | **52.8** | 40.8 | — |
| min | **46** | 26 | 23 |
| max | 58 | 74 | 65 |
| range | **12** | 48 | 42 |
| stems <30 chars | **0 (0 %)** | 1 (8 %) | 1 of 6 |
| stems >54 chars | 4 | 2 | 2 |

The `make check` floor is a *floor* (mean ≥35, fail if several sit under 30), and `exam-qa-review` §3 states the rule only in the low direction. Both are silent here, which is why this has been visible since the first build and never blocked anything.

Two separate problems, and the second is the real one:

1. **Central tendency.** 52.8 is above every official per-paper mean I can measure and is at the very top of the skill's own per-*item* band (~33–54). Marginal on its own.
2. **Dispersion — the finding.** Official 問題7 always mixes a few very short stems (23, 26, 30) with a few long ones (65, 74). This paper's twelve stems occupy a 12-character window with a hard floor at 46. **Every stem is a two-clause narrative sentence with a background clause.** That is the same defect class as F3's closing-move repeat: not one bad item, but twelve items written to one template, which reads as a single authorial voice rather than as an official set. It also costs the section its natural difficulty spread — official's short stems are the ones that test the form with no context to lean on.

Severity **Minor, not automatic**: no key is affected, no item is unanswerable, and every stem is idiomatic Japanese. But it is a genuine finding, not a false positive, and it should be fixed by compressing 3–4 stems to the 25–35 char range (31, 37, 42 are the easiest — drop the background clause), not by lengthening anything.

### View on the standing WARN — `（注N） definitions introduce words the term does not contain` (7 candidates)

**I agree with both previous stages: false positive on all seven. Not a `GATE-WRONG` finding.**

The check's own criterion, printed in the message, is *"flag only if the definition's sole content is the headword's own kanji restated with no added predicate/mechanism."* Reading each:

| 注 | Definition | Added beyond the headword's own kanji |
|---|---|---|
| 農泊 | 農家に泊まり、その土地の暮らしや仕事に触れる旅行の形 | the whole second clause — what the traveller does, and the genus (旅行の形) |
| 管理組合 | 分譲された集合住宅の所有者全員でつくり、建物の維持管理を行う組織 | 分譲, 所有者全員, 組織 — the legal constitution, none of it in 管理+組合 |
| 離島 | 本土から遠く離れ、船や飛行機でしか行き来できない島 | the access criterion, which is load-bearing for 問題13-69's key (通院の負担) |
| 血糖 | 血液の中に含まれるぶどう糖 | ぶどう糖 — glucose specifically, not "sugar", which 糖 alone would give |
| 触診 | 体に手を触れて状態を確かめる診察の方法 | 状態を確かめる, 診察の方法 — the purpose and the genus |
| 初診 | その病気について、その医療機関で最初に受ける診察 | per-institution and per-illness scoping — exactly what 問題13's 「初診については対面を原則」 turns on |
| 菜っ葉 | 食用にする葉物の野菜 | 食用にする + the genus 野菜 — **the weakest of the seven** |

All seven headwords are also correctly *chosen*: 農泊 is a recent coinage, 管理組合/触診/初診/血糖 are institutional or medical terms, 離島 carries a specific criterion the passage argues from, and 菜っ葉 is colloquial rather than standard N2. None is on `dokkai.md`'s banned list of basic/standard words.

The check is behaving as designed — it lists candidates and instructs the reader to judge, and it says so in the message. What it cannot avoid is that a *good* Japanese definition of a 漢語 naturally unpacks that 漢語's own kanji, so it will fire on every well-glossed technical passage forever. I am not filing that as a defect (a candidate-lister with a hand-judgement instruction is not a mis-measurement), but I do note one paper-level nit: **菜っ葉's gloss is close to circular** (菜+葉 → 葉物の野菜). Filed as N6 (Trivial) with a suggested rewording.

---

## Section 3 — Per-question walkthrough (all 101 items)

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 3 | OK | 相続=そうぞく。2×2 {そう,ぞう}×{そく,ぞく} complete; all four are 清濁 derivations of the target's own reading, okurigana none, bold covers the whole word | — |
| 問題1-2 | 4 | OK | 命令=めいれい。2×2 {めい,めん}×{れい,れん}; 長音⇄撥音 derivations, same word form | — |
| 問題1-3 | 1 | OK | 論じる=ろんじる。All four (論/感/応/信じる) are real N2 漢語+じる verbs — moji-goi branch (b). 「じる」 shared by all four, so okurigana leaks nothing | — |
| 問題1-4 | 4 | OK | 星座=せいざ。2×2 {せい,ぜい}×{さ,ざ} | — |
| 問題1-5 | 1 | OK | 実際に=じっさいに。2×2 {じっ,じつ}×{さいに,ざいに}; 促音化 is the tested point, all four carry the printed 「に」. Note: the bold includes the adverbial に, but since all four options carry it there is no leak | — |
| 問題2-6 | 3 | OK | こうせい→構成。Grid {構,講}×{成,製}; all four parse as こうせい | — |
| 問題2-7 | 4 | OK | ほうふ→豊富。{豊,報}×{富,婦}; all four parse as ほうふ | — |
| 問題2-8 | 3 | OK | ききん→飢饉。{飢,基}×{饉,金}; 基金 is real but killed by 「冷害で作物が実らず」 | — |
| 問題2-9 | 1 | OK **(F9 closed)** | うんが→運河。{運,雲}×{河,賀}; 運=ウン, 雲=ウン, 河=ガ, 賀=ガ — all four parse as the printed うんが. The round-1 うんかい defect is gone | — |
| 問題2-10 | 4 | OK | いど→井戸。{井,居}×{戸,度}; all four parse as いど | — |
| 問題3-11 | 3 | OK | 建物内。「持ち出しが禁止されているため」 confines 閲覧 to inside; 外 contradicts it, 側=立場, 間=二点間. All four real productive suffixes | — |
| 問題3-12 | 3 | OK | 仮契約。「正式な契約は来月だが」 is the licensing contrast. 準/略/半 are real prefixes forming no word with 契約 | — |
| 問題3-13 | 2 | OK | 旧市街。「古い建物が今も残っている」. 前/現/元 attach to 役職, not 市街 | — |
| 問題4-14 | 1 | OK **(F2 redraw)** | 「両者とも決め手を欠いたまま持ち時間を使い切り」 forces a no-result outcome → 引き分け. 棄権 dies on 「持ち時間を使い切り」 (they played to the end); 逆転勝ち presupposes a winner; 勝ち越し needs a series. Four match-outcome nouns, one category | — |
| 問題4-15 | 1 | OK | 「ほかの銀行の口座に振り込む場合は、二百二十円の（　）」 — a charge for a procedure. 送料=goods shipping, 代金=the price of the thing itself, 保証金=refundable deposit. Four payment nouns | — |
| 問題4-16 | 4 | OK | 「まず一か月間の（　）を受け、そのあとそれぞれの部署に配属される」 — post-hire training. 面接 precedes hiring; 講演 is not received for a month; 見習い is a status, not something one 受ける | — |
| 問題4-17 | 3 | OK | 「家の壁は一面が本棚になっている」 licenses 読書家. 努力家 unconnected to books; 愛好家/専門家 both require a preceding domain noun | — |
| 問題4-18 | 2 | OK | 「空気が少しずつ抜けて」 forces deflation. ふくらむ is the opposite; ほどける applies to knots; こぼれる to liquids. Four 自動詞 of form-change | — |
| 問題4-19 | 1 | OK | 「法律の問題ではなく（　）の問題だ」 — the paired term must be outside codified rules, so 規則 is denied by the contrast itself; 礼儀=manners; 権利=entitlement | — |
| 問題4-20 | 4 | OK (see N1) | 「思わず持っていた荷物を落としてしまった」 = surprise, only いきなり supplies it. 徐々に is gradual, あらかじめ contradicts 思わず, たびたび gives no shock. Four time-manner adverbs | see N1 |
| 問題5-21 | 2 | OK **(F13 closed)** | 器用だ→細かい作業が得意だ, licensed by 「セーターくらいなら一日で編んでしまう」. Option is now idiomatic on its own (was 「手先が上手だ」). 計算/力仕事/記憶力 are other ability axes | — |
| 問題5-22 | 4 | OK | 印象的だった→心に残った。分かりやすい/意外/短い are other evaluation axes, none containing "stayed with me" | — |
| 問題5-23 | 1 | OK | 几帳面な→きちんとしている, licensed by 「机の上の物の位置がいつも同じだ」. Swap test survives: 「祖父はきちんとしている人で」 | — |
| 問題5-24 | 1 | OK | くどい→しつこい, licensed by 「聞いているうちに疲れてしまう」. そっけない is the opposite pole; 厳しい/冷たい are other negative axes | — |
| 問題5-25 | 3 | OK | おのずと→自然に, licensed by 「無理に暗記しようとしなくても」. わざと is the exact opposite; 一気に clashes with 「毎日使っているうちに」 | — |
| 問題6-26 | 1 | OK | 「持ち合わせがない同僚の昼食代を、私が立て替えておいた」 = paying on someone's behalf. 2 needs 建て替える, 3 組み替える, 4 買い替える — all four stay inside the 〜替える substitution domain, no domain violation | — |
| 問題6-27 | 2 | OK | 「思い通りにならないとすぐ物に当たるとは、幼稚な態度だ」. 1 needs 単純 and clashes with the positive 「迷わずに扱える」; 3 needs 簡単; 4 needs 幼い. All four inside the immature/simple domain | — |
| 問題6-28 | 4 | OK | 「営業部の山田さんあてにかかってきた電話を、私が取り次いだ」 — the intermediary relation. 1=報告, 2=引き継ぐ, 3=教える; all four are transmission verbs | — |
| 問題6-29 | 2 | OK | 「事故のあと、この町にもようやく平穏な日々が戻ってきた」 — 平穏 predicates 日々/状況. 1 needs 穏やか (水面), 3 平然 (表情), 4 和らぐ (痛み). All four inside the calm domain | — |
| 問題6-30 | 4 | OK | 「この電子辞書には、専用の充電器が付属している」. 1=所属 (person), 2=添付 (document), 3=取り付ける (fitting a part). All four attach/belong verbs | — |

### 文法 (問題7–9)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 | OK | 「細かい点はさておき、まずは発売の時期を決めないと」 — priority switch. はもとより *adds* rather than defers; といえども needs same-topic 逆接; をよそに needs a third party's concern being ignored | — |
| 問題7-32 | 3 | OK | 「人は自分でやってはじめて…分かるものだ」. てからでないと and たところで both require a negative 後件; the 後件 is the affirmative 「分かるものだ」 | — |
| 問題7-33 | 2 | OK | 「好調だという事前の予想に反して…前年を大きく下回り」. に沿って/に応じて would make prediction and outcome agree; をもとに needs a deliberate act as 後件 | — |
| 問題7-34 | 1 | OK | 「今度こそ天気予報を確かめずに山へ入るまいと決めている」 — negative volition, licensed by 「痛い目にあったので」. までだ inverts the sense; ことか needs a degree adverb | — |
| 問題7-35 | 2 | OK | 「創業百年を超える老舗だけあって、料理も接客も申し分なく」 — expectation met. のわりに/とはいえ both require a gap between expectation and fact | — |
| 問題7-36 | 2 | OK | 「あの人が理由もなく遅れるわけがない。何か事情があったんですよ」 — the following line is the defence, so only a categorical denial fits. しかない would concede the lateness | — |
| 問題7-37 | 4 | OK | 「飲み物抜きで注文…その場合は二百円お安くなります」 — the discount fixes exclusion; 込みで/付きで both include | — |
| 問題7-38 | 1 | OK | 「社内で進めるにしろ、外部に任せるにしろ」 — the paired form must repeat verbatim; からには/とすれば/につけ all break the correlative | — |
| 問題7-39 | 2 | OK | 「まず本人の話を聞くべきだ」 — 当為. きり cannot attach to 辞書形; ばかり would mean "only listens" | — |
| 問題7-40 | 1 | OK | 「初心者向けの絵本」, licensed by 「海外の子どもに配る目的で作られ」. 頼み/込み/次第 cannot name an intended readership | — |
| 問題7-41 | 4 | OK | 「道具がほこりだらけで」. ずくめ needs a uniform desirable/colour set; がち needs an animate tendency; っぱなし needs ます形, not the noun ほこり | — |
| 問題7-42 | 3 | OK | 「長年住んでいた家を売ってまで資金を用意した」 — extreme means. たきり/たあげく/たところで all clash with the achieved, affirmative 後件 | — |
| 問題7 (set) | — | **要修正 (N5)** | 12-stem mean **52.8** JP chars, min **46**, max 58, range 12; official 7/2025 measures mean 40.8, min 26, range 48. **Zero stems under 30** (official 8–17 %). Every stem is a two-clause narrative sentence — one template across the whole 大問. Gate is silent because its rule is a floor only | Compress 3–4 stems into the 25–35 char band by dropping the background clause; 31, 37, 42 are the easiest. Do not lengthen anything |
| 問題8-43 | 4 | OK | 兄は休日も(1)→朝早くから出かける(2)→**一方(4)**→弟は昼過ぎまで(3). 一方 must follow a 連体形 clause, and only card 2 is one; card 3 cannot take card 2 (「弟は昼過ぎまで朝早くから出かける」 is contradictory); only card 3 attaches to 「布団から出てこない」. Unique. No bare adverb | — |
| 問題8-44 | 3 | OK **(F1 closed)** | 部屋を見るだけでなく(1)→周りの環境も(2)→**自分の足で確かめた(3)**→うえで(4). Round 1's rival 2-3-4-1 is now ungrammatical: 「…確かめたうえで部屋を見るだけでなく決めようと思う」 leaves だけでなく without its second conjunct. Card 1 also cannot precede うえで nor sit last. Unique | — |
| 問題8-45 | 1 | OK | 渋滞に巻き込まれて(2)→遅刻する(3)→**ことがない(1)**→ように(4). ことがない needs 連体形 遅刻する; ように must close before 「毎朝三十分も早く家を出ている」; テ形 can only lead. Unique | — |
| 問題8-46 | 1 | OK | 弟は(2)→もうぐっすり眠って(3)→**しまった(1)**→にちがいない(4). にちがいない takes 普通形 and closes the quoted 「と思い」; しまった requires the テ形. Unique | — |
| 問題8-47 | 4 | OK | ご本人から(1)→書面による(2)→**申し出が(4)**→ない限りは(3). 「書面によるご本人」 is meaningless so 1-2 is fixed; ない限りは takes the ガ格 申し出が and is the only card that can meet the comma. Unique | — |
| 問題8 (set) | — | OK | All five 解説 cells now carry an explicit **last-slot** proof (round 1's proposed rule), not just a middle-order proof. No option is a bare adverb. Each set has exactly one grammatical ordering of 24, verified by hand | — |
| 問題9-48 | 3 | OK **(F10 closed)** | `[論理接続]` 前段「誰でもその場で気づく」 vs 後段「買う人はその日、何も感じないまま店を出る」 — two opposed faces of the same ¥20. そのうえ adds in the same direction; たとえば would need an instance; ようするに would need a restatement | — |
| 問題9-49 | 2 | OK | `[文末モーダル]` 「客はこれまでどおり買い続けてくれるはずだ」, fixed by the next line 「少なくとも、売る側はそう考えてきた」. にすぎない devalues; どころではない inverts; ものではない preaches | — |
| 問題9-50 | 3 | OK | `[内容推論]` requires the whole passage: 第3段落 「売る側からそれを告げられる機会は、ついに一度もない」 plus 第4段落's measured 一割以上 drop. 高まっていく/問題にならない contradict the drop; 変わらないだろう *is* the premise 第3段落 opens by questioning | — |
| 問題9-51 | 4 | OK **(Ruling A)** | `[慣用・形式名詞]` 「客に買い続けてもらうための売り上げなのに、その売り上げを守ろうとして中身を削るのでは、本末転倒だ」 — the stem states the ends/means inversion. 一石二鳥 is positively valued and collides with the 一割以上 drop; 一長一短 asserts a benefit the passage never grants; 二者択一 belongs to 第2段落's choice stage. Four 五-char 四字熟語, one functional class. Category ruling: inside (d) | — |
| 問題9 (passage) | — | OK (one note) | Body **738** JP chars against bunpou.md's ~500–700 — 5 % over the top of the stated band, not a defect (the rule guards against 150–200 char stubs). Four distinct category tags, exactly one 内容推論. All 16 options 4–9 chars (official max 14) | Optional: trim ~40 chars from 第2段落 |

### 読解 (問題10–14)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 4 | OK | 「新しい規程では、この扱いを二つに分けます」+「本業と競合しない業種で、月の就業時間が二十時間を超えない場合は…届出書」/「同業他社での就業や、月二十時間を超える就業は、従来どおり申請と許可」. 1 drops the 業種 axis; 2 is false (permission already existed); 3 inverts 「開始前に」 | — |
| 問題10-53 | 3 | OK | 「対象は、賞味期限までの期間が九十日以上ある商品に限ります」 → 三か月以上. 1 over-generalises past 「一部について」; 2 denied by 「消費期限の表示がある商品は、これまでどおり日付まで」; 4 denied by 「八月三十一日までの入荷分は…従来の表示で」 | — |
| 問題10-54 | 4 | OK | 「片道十キロを超え、大型車の多い幹線道路を通る経路では負傷事故の割合が高いが、五キロ以内で自転車道の整備された道を行く経路では、その割合は徒歩通勤の場合と変わらない」 — distance × road type. 1's 車道/歩道 axis, 2's severity claim and 3's short-distance-on-a-trunk-road case are all absent from the text | — |
| 問題10-55 | 2 | OK | 「一度書いた行は消えない。だから書き出す前に、相手の顔を思い浮かべ、何をどの順で伝えるかをひとしきり考えることになる」. 1 is the screen's property, stated in reverse; 3 is the belief the essay retracts; 4 contradicts 「手が思考の速さについていかない」 | — |
| 問題10-56 | 2 | OK | 「なぜ始めたのか、何が面白くなくなったのかを本人に言葉にさせ、やめる時期を自分で決めさせること」. 1 is the position 「無理がある」 rejects; 3 inverts the agency; 4 contradicts the whole essay | — |
| 問題11-57 | 2 | OK | 「二晩のあいだに見たのは、畑と台所と、縁側から見える山の稜線くらいのものである」. 1 (取材の忙しさ), 3 (地元の人しか知らない場所) and 4 (夜が早い) are not in the text | — |
| 問題11-58 | 1 | OK | 「旅先で私たちが持ち帰るのは、名所の写真よりも、そこで誰かが繰り返している日常のほうなのかもしれない」. 2 is denied by 「集落には空いた民宿が何軒もある」; 3 by 「手伝ってほしいと言われたのではない」; 4 is never evaluated | — |
| 問題11-59 | 3 | OK | 「ところが一度でも言葉を交わした相手であれば、その人が通る場所として意識されるようになる」. 1/2/4 are named in the passage but never as the origin of the feeling | — |
| 問題11-60 | 3 | OK | 「挨拶を交わす、と答えた住民の割合が高い建物ほど、共用部の破損や放置物が少なく、修繕にかかる費用も低く抑えられていた」. 1 denied by 「共用部を保つのは定期的な点検や清掃の契約であり」; 2 denied by 「世帯数や築年数が近い建物どうしで比べても、この傾向は変わらなかった」; 4 is not a comparison the text makes | — |
| 問題11-61 | 1 | OK | 「事件や事故の当事者として名前が出た人、勤め先の不祥事とともに写真が流れた人が、何年たっても検索結果の上位に自分の名前と当時の見出しを見つけてしまう」. 2 (法律), 3 (放置), 4 (後からの注目) are absent | — |
| 問題11-62 | 4 | OK | 「目立つのは、本人が書いたものではなく、他人が本人について書いたもののほうだという」. 1 is the *original* assumption, explicitly dated 「この言葉が使われ始めたころ」; 2 denied by 「転載先をたどりきることは難しい」; 3 absent | — |
| 問題11-63 | 2 | OK | 「疑いは…都合の悪い情報を遠ざける口実にもなる」 + 「確かめるとは、その情報が最初にどこから出てきたのかをたどり…見に行く作業である」. 1/3/4 add acquisition routes and expertise claims the passage never makes | — |
| 問題11-64 | 2 | OK | 「判断をいったん保留したまま出所をたどる、その地味な手間を惜しまない態度こそが、見分ける力の中身なのだと言える」. 1 denied by 「そのぶん正確に判断できるようになるとは限らない」; 3 over-reads 一次情報; 4 is not claimed | — |
| 問題12-65 | 3 | OK | A「それらを作るのをやめてしまうという選択は現実的ではない」/ B「道路や施設を作るのをやめてしまうことはできない、という点に異論はない」. 1 is A only and even A hedges; 2 and 4 appear in neither | — |
| 問題12-66 | 3 | OK | A「失われる分を数え、同じだけの環境を近くに用意していく仕組みが現実的である」/ B「計画の段階で、代えのきかない場所を開発の対象から外しておくことである」. 1/2/4 match neither position | — |
| 問題13-67 | 1 | OK | 「一つは、すでに診断がつき、同じ薬を続けている患者の定期的な受診である」+「もう一つは、初めての症状について診断を求める受診である」. 2 takes a detail of the first layer as an axis; 3 is a user-attribute split; 4 is the regulatory split, discussed a paragraph later | — |
| 問題13-68 | 4 | OK | 「対面が担ってきた仕事のうち、情報の量が限られていても成り立つ部分を引き受ける仕組みである」. 1 denied by 「対面診療の代わりに置かれるものではなく」; 2 inverted (初診 is where remote is *weakest*); 3 mistakes a first-layer detail for the relation | — |
| 問題13-69 | 4 | OK | The two threads the essay ends on: 「どこまでを画面で扱えるかという線の引き直しである」 + 「同じ画面越しの診察が、通院に半日かかる島では暮らしを支える手段になり、駅前の医院に五分で歩ける町では余分な手続きになる」. 1 substitutes 通信環境 for 通院の負担; 2 denied by 「この層では対面の診察に及ばない」; 3 is a recommendation never made | — |
| 問題14-70 | 2 | OK | Three constraints combined: 卓球「高校生以上の方」→ a 中学2年生 cannot enter; 5キロマラソン「中学生以上の方」→ can; 「中学生以下の方が参加する種目は、保護者の同意書…の提出が必要です」. 1 denied by 「当日、会場での現金のお支払いはできません」; 3 by 「郵送では受け付けません」; 4 by the マラソン row | — |
| 問題14-71 | 2 | OK | Two constraints combined: 親子ペアリレー「申込締切 9月26日」 vs the stated 10月1日; ウォーキング大会「当日受付」. 1 denied by 「1組1,500円」; 3 by 「ウォーキング大会はこの数に含みません」; 4 by both deadline cells. Every referenced detail is on the printed flyer | — |

**読解 mechanical reads (measured on the shipped file, not taken from the gate)**

| Check | Bar | This paper | 判定 |
|---|---|---|---|
| In-body `（注N）` markers, 問題10–13 | ≥25, target 30–40 | **31 markers / 31 definition lines, 1-to-1** | OK |
| Orphaned glosses / unmarked definitions | 0 | 0 | OK |
| Gloss level (no basic N3–N5 / standard N2 words) | 0 violations | 0; 7 gate candidates all judged (see Section 2), 菜っ葉 is the only weak one | OK (N6 trivial) |
| `（中略）` in 中文/長文 | ≥1 | 3 | OK |
| `<ruby>` in 言語知識・読解.md | 0 | 0 | OK |
| Marked spans ①–⑤ | 1-to-1 with stems, pointer-sized, `（注N）` outside bold | 6 spans, 6 stems, all exact-string identical, lengths 11–22 chars | OK |
| Option length ratio max/min | ≤1.30 | max **1.26** (問63 / 問71) | OK |
| (Tied-)longest key rate | ≤35 % (official 30 %) | **25 %** (5/20) | OK |
| **Uniquely** longest key rate | ≤30 % (official 20 %) | **20 %** (4/20) | OK |
| Key length rank spread | varied | rank1×5 / rank2×6 / rank3×5 / rank4×4 | OK |
| Absolute quantifier / categorical denial | 0 free eliminations | 0 candidates (gate agrees) | OK |
| Key paraphrasing 52–69 (no verbatim lift) | no LCS ≥15 & ≥50 %; none ≥20 | gate green; hand-checked 54, 60, 64, 68 — longest surviving run 11 chars | OK |
| Section lengths | 10≥1100 / 11≥2250 / 12≥510 / 13≥800 / 14≥450 | all pass (gate) | OK |
| Closing-move variety | ≤2 per shape, differing at sentence-template level | 13 finals, no skeleton repeated more than twice, `そのものではなく` **0** | OK **(F3 closed)** |

### 聴解 (30 items)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 1 | OK | 「これから下見に行って、みんなが待てる場所があるか見てきてくれる?」. Announced 「最もよいものは1番です」 = printed pre-mark **(1)** = what the dialogue supports | — |
| 問題1-1番 | 2 | OK | 「開発部から試作品、借りてきてくれる?」+「数に限りがあるらしいから、早い方がいいんだ」. 1 不要「もともと天井に付いてるから、予約は要らないよ」/3 後回し「練習は明日でいいよ」/4 条件不足「価格はまだ役員会で決まってないから、今は入れられない」 | — |
| 問題1-2番 | 3 | OK **(F5 closed)** | 「実験ノートの元の数字と一つずつ照らし合わせてみてくれる?」. 1「林くんがやってくれることになってる」/2「装置が来月まで別の班に貸し出されてる」/4「来週の打ち合わせまでに直せばいい」. Closing is now the bare 「はい、わかりました。」 — no keyword leak | — |
| 問題1-3番 | 2 | OK **(F5 closed)** | 「今のうちに、請求はがきを地域ごとに分けといてくれる?」, motivated by 「地域ごとに分けてないと割引が使えないの」 and by the mid-dialogue new information 「新しいパンフレットの到着が明後日にずれ込む」. 1「そのあとでね」/3「事務の川口さんが重さを量ってから貼ってくれる」/4「もう百部ずつ束ねて棚に置いてある」. Closing 「じゃあ、さっそく取りかかります。」 names nothing | — |
| 問題1-4番 | 1 | OK **(F5 closed)** | 「一度お戻りになって、あの票を持ってきていただけますか」. 2「そこが空欄ですと受け付けられない」/3「あちらも番号を押していただく形」/4「お荷物がこちらにある間はできない決まり」. Closing is now 「お手数をおかけしますが、よろしくお願いいたします。」. Note: all three distractors die on the same missing number — realistic and each separately denied, but it is the section's least discriminating item | — |
| 問題1-5番 | 3 | OK | 「先に求職の申し込みの登録を済ませていただく必要があるんです」. 1 不要「求人票のコピーは、紹介状といっしょにこちらでお付けします」/2 規則「こちらの求人はハローワークを通してのお問い合わせに」/4 明確な否定「面接の日程を今日決めていただくことはありません」 | — |
| 問題1 section | — | OK **(F4/F5 closed; N2 residual)** | 5 distinct keyed actions ✓. 場面: 4 work-assignment / 2 counter ✓. 質問型 all この後まず ✓. 消去方法 tokens re-counted from the script: no token above 2 of 6 rows ✓. Closing turns: 6 different skeletons ✓. See N2 for the one cell I classify differently | N2 |
| 問題2-例 | 2 | OK | 「明日の会議が急に一日増えちゃって」. 電車 denied by the guest, 観光/買い物 withdrawn. Announced 2 = pre-mark **(2)** | — |
| 問題2-1番 | 4 | OK **(F6 re-angle accepted)** | 「新しい部屋、四階なんだけどエレベーターがなくて。あと二名つけないと手が足りない」+「四階まで持って上がるとなると全然違うんだって」. 1「荷物、前の家より減らしたくらい」/2「うちは四月の半ばなの。混む時期はわざと外した」/3「距離はむしろ前より近いくらい」 — each explicitly denied by the speaker. Key paraphrases twice (エレベーターなし→階段, 二名つける→人手がよぶん); 階段/運ぶ/人手/よぶん all absent from the script | — |
| 問題2-2番 | 2 | OK **(F11 closed)** | 「しみ抜き専門の工場に一度出すことになるんです」+「店の中だけでは仕上げられない品なので」. 1「今週はむしろ空いているくらい」/3「機械は先月入れ替えたばかり」/4「配送は毎日あります」. Key 「よその業者にあずける」: よそ/業者/あずけ occur **0** times in the script | — |
| 問題2-3番 | 3 | OK | 「なので今日は、根元だけを染めて、毛先は次に来ていただくときに」→「確かに。じゃあ、それでお願いします」. 1「切らなきゃいけない状態になりかねなくて」/2 the 店長 talks her back out of it/4「それでも毛先に薬をのせることになるので、傷みは同じ」. 根元 ↔ 「前に染めたところが伸びてきちゃって」 licenses 「のびた部分」 | — |
| 問題2-4番 | 2 | OK | 「夜にギターを弾くので、音が出せるかどうかが一番でして」+「とにかく、夜に音が出せるところを見せてください」. 1「家賃は多少上でも構わない」/3「自転車があるので、20分でも平気」/4「一人なので、狭くても気にしません」 | — |
| 問題2-5番 | 1 | OK | 「部屋の鍵をこの箱に入れといていただければ、それでおしまいです」+「ほかの手続きは要りません」 (two turns merged into one option). 2「今は先にお支払いが済んでるので、なくしました」/3「それは特にお願いしてないですね」/4「お部屋の方は、そのままで大丈夫」 | — |
| 問題2-6番 | 4 | OK | 「同じ月のうちでしたら、あいているクラスに振り替えていただけますよ」→「振り替えができるなら、今度こそ続けられそうです」. 1「料金はどこも似たようなものかなと」/2「場所は、正直そんなに気にしてないんです」/3「先生がどんな方かは、始めてみないと分かりませんしね」 | — |
| 問題2 section | — | OK | 6 distinct keys ✓. Quotas: どうして ×2 (≥2) ✓; どのように ×2 (≥1) ✓; 一番/優先 ×2 (≤2) ✓. Key-marking devices deliberately varied (contrast / proposal accepted / summarising line) ✓. No bare 「〜ではありません」 sweep | — |
| 問題3-例 | 2 | OK | 自習席の取り方の変更. Announced 2 = pre-mark **(2)**. Lead-in names setting + speaker only, not the topic | — |
| 問題3-1番 | 3 | OK | 「繊維になる前の原料の状態まで戻す技術が実用化されてきました」+「服が何度でも服に生まれ変わる」. 1 熱の利用 never mentioned; 2 生地の丈夫さ absent; 4 古着の値段 absent. Talk 306 chars (gate measure) | — |
| 問題3-2番 | 3 | OK | 「施設の決まりに合わせていただくのではなく、その方のこれまでの暮らし方を、できる限りそのまま続けていただくことを大事にしています」. 1 費用 / 2 資格 / 4 面会 all absent. 325 chars | — |
| 問題3-3番 | 3 | OK | 「初回のご相談は九十分に延ばして、その日は契約のお話を一切しないことにしました」+「押し切られたという気持ちで帰るお客様がいなくなったのが、私は一番うれしい」. 1 肌の手入れ / 2 料金の仕組み / 4 移転 absent. 337 chars | — |
| 問題3-4番 | 1 | OK | 「故障を見つけるのが点検だと思われがちですが、私たちにとっては、運転の癖をお返しする場なんです」. 2 部品交換 mentioned only as 「そう多くありません」; 3 燃料 / 4 買いかえ absent. 318 chars | — |
| 問題3-5番 | 4 | OK | 「湯船に入られる前に、かけ湯をしていただき」+「お風呂に入る前と上がった後には、必ずお水かお茶をお飲みください」. 1 成分・効能 / 2 混雑 / 3 休憩室 absent. 295 chars | — |
| 問題3 section | — | OK **(F14(b) closed)** | Quotas: institutional announcements 2 (例/5番, ≤2) ✓; person's 主張・意図・経験 4 (≥3) ✓. Talks 295–337 (gate measure) / 274–313 (JP-char measure) — both in band, and the 構成表 now prints both and retracts the wrong 311–353. Options are bare noun phrases, no 「〜について」. No monologue names or denies its own distractors (gate confirms) | — |
| 問題4-例 | 2 | OK | 「承知しました、今日中にやっておきます」. Announced 2 = pre-mark **(2)** | — |
| 問題4-1番 | 2 | OK | 「こちらの記入例を見ながら書いてみてください」. 1 presupposes it is already submitted, contradicting 「書き方がよく分からない」; 3 answers the *next* step | — |
| 問題4-2番 | 3 | OK | 「困ったら、また声をかけてください」 — deflect thanks. 1 has the tense wrong (already helped); 2 inverts the roles (the thanked party thanking back) | — |
| 問題4-3番 | 2 | OK | 「そうですね、印刷する前に直しておきます」. 1 overshoots (deleted the figures); 3 reverses the polarity (smaller) | — |
| 問題4-4番 | 1 | OK | 「印鑑でも構いませんか」 — indirect acceptance via a condition; the paper's one question-key (official band 0–15 %). 2 inverts the role; 3 asserts a false premise | — |
| 問題4-5番 | 2 | OK **(F12 closed)** | 「とんでもないです。ちょうどお待ちしていました。」 — presupposes nothing beyond the prompt. 1 asks how long the busy spell lasts (not a reply to thanks); 3 misreads the thanks as a fresh request | — |
| 問題4-6番 | 3 | OK | 「あ、失礼しました。すぐにしまいます。」 — the paper's only 「あ、」-opening key (cap ≤2). 1 contradicts the notice; 2 inverts the role | — |
| 問題4-7番 | 2 | OK | 「助かった。夕方までに見て返すよ。」 — 課長 replies casually to a ます-form subordinate ✓. 1 has the tense wrong; 3 contradicts 「作成いたしました」 | — |
| 問題4-8番 | 2 | OK | 「ちょうど気になっていたところだ。」 — 社長 casual to a subordinate ✓. 1 contradicts 「まとまりました」; 2… 3 misidentifies the period | — |
| 問題4-9番 | 3 | OK | 願ってもない = 望んでも得られないほどありがたい → 「そう言っていただけると、こちらも助かります」. 1 reads it as regret; 2 reads it as dissatisfaction | — |
| 問題4-10番 | 3 | OK | 間に合わせる = 期限までに何とか用意する → 「うちのプリンターで刷れば間に合います」. 1 misreads 「今日中は無理」 as a closure; 2 puts it in the past | — |
| 問題4-11番 | 1 | OK | 顔を出す = 短時間でも姿を見せる → 「三十分なら寄れると思う」. 2 takes 顔 literally; 3 answers a different question | — |
| 問題4 section | — | OK (F15 open at rule level) | Keys opening はい/いいえ/では: **0** ✓ (gate: 0 % of 36). 「あ、」 keys: 1 ✓. Question-keys: 1 ✓. Already-done shape: 2 under the rule as written, **3** by intent (1番/3番 もう+た, 4番 先ほど+た) — 3 of 24 distractors, inside the gate's own official band (median 1, max 3) and far from the 8/11–9/11 rate the cap exists for. Paper acceptable; the rule still needs widening | see F15 / RC-4 |
| 問題5-1番 | 1 | OK | 3 speakers (女の人・男1・男2) ✓. 「公園で、みんなでお昼を作って食べるっていうのはどう?」→「それなら座ってできるし、子どもも野菜を切る係で入れるね」→「火を使う許可は、去年の夏祭りのときに取ってる」→「じゃあ、それでいこう」. 2「公民館、十月いっぱい耐震の工事に入っちゃう」/3「八十代の方が途中で座り込んじゃって」/4「学校の行事と重なる時期なんです」 — three different grounds ✓ | — |
| 問題5-2番 質問1 | 2 | OK | 「そうだな。消火器はこの前の秋にもやったし、同じことの繰り返しになりそうだ。救命講習にするよ。」 1 withdrawn by himself; 3「炊き出しは、僕が入っても鍋を見てるだけになりそう」; 4「僕は腰を痛めてるから、重い物を運ぶ方は無理」 | — |
| 問題5-2番 質問2 | 4 | OK | 「あ、確かに。名簿って、避難所で使うものだもんね。」→「じゃあ、避難所づくりにする。」 1「消火器は、重くて持ち上げられなかったし」; 2「私は去年受けて修了証をもらってるから、今年はあなたが行った方がいいよ」; 3「うん、去年やった」 | — |
| 問題5 section | — | OK | 1番 = 意見整理型 with 3 speakers; 2番 = 列挙→評価型 where the enumerating 講師 decides nothing ✓. Labels bare and phonetically distinct (消火器訓練/救命講習/炊き出し体験/避難所づくり), no deciding attribute printed beside a name, and 質問1/質問2 read the same four labels in the **same** order ✓. 質問 pair 男の人は／女の人は, rotated off the 最初／結局 pair ✓. Decision structure (mutual-advice swap) differs from both previous papers | — |

**聴解 mechanical reads**

| Check | Bar | This paper | 判定 |
|---|---|---|---|
| Whole-section uniquely-longest key rate | ≤35 % (official 28 %) | **15 %** (4/27) | OK |
| Median key ÷ distractor mean | ≤1.15 (official 1.00) | **1.03** | OK |
| Narration ↔ voice ↔ `SPEAKER_MAP` | no contradiction | gate green on all items; I re-read each label against its narration | OK |
| 例 announced number ↔ pre-mark ↔ dialogue | must agree | [1, 2, 2, 2] on all three, and each dialogue supports its announced number (hand-checked) | OK |
| No two items in a section share a key | — | gate: 16 keys compared, ok | OK |
| No two items end on the same turn | — | gate ok; I read all six 問題1 closings as a column | OK |
| Reaction turns / fillers / contractions | 18 % / 9–48 / 22.4–67.4 per 10k | 22 % / 34 / 57.1 | OK |
| Answer reveal in a scored item | forbidden | 「最もよいものは◯番です」 occurs only in the four 例 blocks | OK |
| MP3 / chapter freshness | artifacts newer than sources | `script_sha` = `55361ffa7c57` = shipped script; MP3 18:28:55 > script 18:22:53 | OK |

---

## Section 4 — Whole-paper and cross-test topic table (step 5), provenance (step 6)

### Headline theme set, built from the SHIPPED surfaces

| Slot | 20260817_1 | 20260817_2 | **20260817_3 (this paper)** |
|---|---|---|---|
| 問題9 | 文化・伝統 (方言) | 科学・技術 (自動販売機) | **消費・経済 (値段と量 — 実質値上げ)** |
| 問題12 | 地域活性化 (地方移住) | 旅行・観光 (入場者数上限) | **環境 (開発と代償措置)** |
| 問題13 | メディア・情報 (フィルターバブル) | 働き方 (AIと学び直し) | **医療・福祉 (遠隔診療)** |
| 問題14 | 環境 (リサイクル自転車) | 教育 (奨学金) | **スポーツ・余暇 (市民スポーツ大会)** |
| 聴解問題5-1番 | 住まい (宅配ボックス) | 食 (宴会コース) | **人間関係 (世代間交流イベント)** |
| 聴解問題5-2番 | 睡眠・健康 (仮眠カフェ) | 子育て・家族 (家庭支援センター) | **防災 (防災訓練)** |

- **Rule 1** — six headline surfaces, six different themes: **PASS**.
- **Rule 2** — no headline theme reused on another 読解 surface: **PASS** (13 読解 surfaces, 13 distinct themes; 問題12A/12B share 環境 by design as one surface).
- **Rule 3** — 13 読解 surfaces, 13 distinct themes: **PASS**. Listening theme cap ≤5: max is 教育 at 4 of 21: **PASS**.
- **Rule 4** — intersection with 20260817_2 (immediately previous) = **∅**: **PASS**. Intersection with 20260817_1 (two back) = **{環境}**, exactly one, inside the allowance: **PASS**.
- **問題12's own cross-test column** — 人間関係 → 地域活性化 → 旅行・観光 → **環境**: no repeat: **PASS**.
- **`test_spec.json` theme ↔ `logs/topics.json` theme**, surface by surface: agree on every themed surface. No relabel-to-dodge.
- **`logs/topics.json` `surfaces` / `themes` / `shapes` / `closing_moves` all reflect the SHIPPED (post-fix) paper**, not the discarded draws — I checked all four fields against the artifact. The `notes` field is the exception (see N3).

### Non-headline cross-test checks

| Check | Result |
|---|---|
| 問題9's subject vs 20260817_2's 読解 surfaces | 消費・経済 label matches 20260817_2 問題11(2) (円安と生活費の偏り), but that surface is **not headline**, and the subjects do not overlap: macro exchange-rate incidence across household types vs. a firm's choice between raising price and cutting contents, and the consumer's ability to notice. No shared fact, example, or argumentative move. **Not a repeat.** (This is the case `logs/topics.json` note (b) escalated; I rule it clean.) |
| 聴解 errand repeat vs 20260817_2 | Gate check `no 聴解1/2/3/5 errand repeats 20260817_2's` — **ok**. The one adjacency (引っ越しの見積もり) is F6, ruled accepted above. |
| Two 聴解 items running the same errand within this paper | 問題1-3番 (bulk-mail prep at a school office) and 問題1-4番 (collecting a parcel at a post office) both touch the postal system but are different errands, different roles, different tasks. 問題2-例 (延泊) and 問題2-5番 (チェックアウト) are both lodging-reception scenes in one section — see **N7**. |
| 問題14 flyer vs any 聴解 item | The flyer's decisive cells (高校生以上 / 中学生以上 / 同意書 / 9月26日 / 10月3日 / 当日受付 / 振込 / 2種目 / 雨天延期 / 30分前) appear nowhere in the script. No shared decisive detail. |
| Any subject twice in this paper | None. I listed all 47 surfaces and compared pairwise. |

### Closing-move column (13 essay surfaces, read from the last two sentences)

| Surface | Move | Final-sentence template |
|---|---|---|
| 問題9 | 理由提示 | 〜と感じてしまう**ためだ** |
| 問題10(1) | 事務連絡 | ご不明な点はご相談ください (no move) |
| 問題10(2) | 条件提示 | ※〜従来の表示で販売します (no move) |
| 問題10(3) | 問いの再定義 | 〜という問いは、つまるところ、〜という問いである |
| 問題10(4) | 随筆・定義の置き換え | 私が今そう呼びたいのは、〜数分間である |
| 問題10(5) | 帰結提示 | この過程を経た子どもは、〜手ごたえを持てる |
| 問題11(1) | 随筆・情景回帰 | 〜籠の重さを、私の手はまだ覚えている |
| 問題11(2) | 留保つき再確認 | もっとも〜ではない。それでも、〜保たれている |
| 問題11(3) | 情景回帰 | 相談者は〜と指を置く |
| 問題11(4) | 主張 | A **だけではない**。B **こそが**〜と言える |
| 問題12(A) | 主張再提示 | 〜には、〜仕組みが現実的である |
| 問題12(B) | 主張再提示 | 〜先に決めておくことが、〜条件になる |
| 問題13 | 対比例示 | 同じ〜が、A では P になり、B では Q になる |

No template appears more than twice. `そのものではなく` = **0** occurrences; the two surviving `ではなく` are both mid-passage. **F3 closed** and, unlike round 1, the two surfaces that do share a move (問題12A/12B; 問題10(4)/11(1) as 随筆) differ at the sentence-template level.

### Provenance & spec blueprint audit (step 6)

| Check | Result |
|---|---|
| Target item match, 問題1–8 + 聴解 | All 58 語彙/文法/quick_response targets, 21 `listening_scenarios` and 12 `reading_topics` resolve to `pools.json` (gate: 22 items + 21 listening targets, ok). Every shipped item matches its drawn target; the 問題4 redraw is recorded in the seed as `+reroll(context_words,79773993)`. **No unrecorded substitution.** |
| `logs/ledger.json` ↔ `test_spec.json` | `seed` and `items` compare **equal field for field** (verified by object comparison, not by eye). No `harvest_sha` field exists in this ledger's schema, so no fabricated date-shaped sha is possible. |
| Rotation cooldown | Intersection of this paper's draws with 20260817_1 and 20260817_2, after folding parenthetical readings: **zero in every category**. Gate's own per-category cooldown check over the full 6-test window: ok. |
| `answer_positions` | Present and non-empty for all 19 slots, **101 prescribed**, and the flat vector equals both the shipped keys and my blind-solve vector. Distribution 1×24 / 2×27 / 3×27 / 4×23. |
| Copyright non-reproduction | **22-char** JP-only overlap scan (stricter than round 1's 25) of the whole paper against all 62 files under `refs/JLPT_N2_NEW/*/{booklet,script}.md` and `tests/imported-*/*.{md,txt}`: **385 distinct overlaps, every one of them official instruction boilerplate or the mandated 問題1 narration formula** (「…で男の人と女の人が話しています。…はこの後まず何をしますか」). Zero passage, dialogue, 例, stem or option overlap. Proper nouns (山田/佐藤/川村/田中/川口/林/みどり市) share no set with any imported paper. |
| Invented flavour detail | Numbers are author-invented and N2-simplified: 二百二十円, 九十日以上, 二百件, 一割, 二か月後, 二十時間. None is a decimal, none cites a real source ("ある食品会社が" / "ある調査では" / "各地の事故統計"). |

---

## Section 5 — Findings

**Zero automatic-fail findings.** No second defensible answer, no keyed option the source does not state, no unanswerable item or 例, no 解説 quote absent from the source, no repeated topic, no broken Japanese, no narration/voice contradiction, no spec/paper provenance mismatch, no off-level key, no non-word option, no ungrounded 聴解 distractor, no 問題9 category collision, no free elimination, no stale artifact, no verbatim reuse.

| # | Item(s) | Class | Severity | Evidence | Fix |
|---|---|---|---|---|---|
| **N1** | 問題4-20 | Level, easy end of band | **Observation — not filed as a finding** | Key いきなり sits at the N3/N2 boundary. But `exam-qa-review` §2.5 binds the **option set**: 徐々に and あらかじめ are solidly N2 and the discrimination is a real one, so the set clears the TOO_EASY bar that failed round 1's 姿/跡/光/影. | None. Recorded so the next reviewer does not re-derive it. |
| **N2** | 聴解.md `セクション構成表`, 問題1 例 row | 構成表 cell not supported by the script | **Minor** | The table records the 例's third elimination as `順番待ち（名簿は場所確定後）`. The script line is 「それは、あとで一緒に書き込もう。」 — nothing in the dialogue makes the roster wait on the location; that reads as **後回し**. Round 1's version of this line was 「場所が決まってからでいいよ」, an explicit dependency; the F4 fix rewrote the line but not the label. Reclassified, 後回し reaches **3 of 6 rows** (例 / 1番 / 2番) against the ≤2 cap — though only **2 of the 5 scored rows**. | Either restore an explicit dependency in the 例's line (e.g. 「場所が決まってから、一緒に書き込もう。」) so the `順番待ち` label is true, or relabel the cell 後回し and move 1番's or 2番's deferral to another token. Prefer the first — it is a one-line script edit and the 例 is not scored. |
| **N3** | `logs/topics.json` → 20260817_3 → `notes` | Stale hand-off note | **Minor** | Note (a) says 「願ってもない is a printed distractor at 問題9-51」 — 願ってもない occurs **0** times in `言語知識・読解.md`; 問題9-51's options are the four 四字熟語. Note (c) says 聴解問題2-2番's key 「still shares 「よそ」 with the script's 「よそにお願いする」」 — 「よそ」 occurs **0** times in the shipped script. Both describe pre-fix artifacts. This field is the hand-off the next paper's blueprint stage reads; a stale note there costs a real draw decision. | Delete notes (a) and (c); keep (b) and (d), which are still true (and (d) is now finding N5). |
| **N4** | `tools/qa_eval.py` | Evaluator mis-parses the key table | **Minor (tooling, not the paper)** | Run against this paper it reports `Total Scored Items : 106` and five discrepancies at items 102–106 with "keys" 306 / 325 / 337 / 318 / 295. Those five numbers are the **問題3 per-talk character counts printed in the `セクション構成表`**, which the parser reads as key rows. Values outside 1–4 can never be options, so the parser is provably wrong here. The blind solve is the one thing standing between a mis-key and shipping; its evaluator returning phantom discrepancies teaches reviewers to discount its output. | In `qa_eval.py`, stop parsing after the key tables (or reject any parsed key not in 1–4, and any item index >101). |
| **N5** | 問題7 (all 12 stems) | Stem length and dispersion | **Minor** | 12-stem mean **52.8** JP chars (official 7/2025: 40.8), min **46** (official 26; 12/2025 has a 23), range **12** (official 48), **0 %** under 30 chars (official 8–17 %). Every stem is a two-clause narrative sentence with a background clause — one template across the 大問. Gate and `exam-qa-review` §3 both state the rule as a floor only, which is why this has been green since the first build. Full measurement in Section 2, Ruling B. | Compress 3–4 stems to 25–35 JP chars by dropping the background clause (31, 37, 42 are the easiest). Do not lengthen anything, and do not change any keyed form or `answer_positions`. |
| **N6** | 問題11(1) `（注3）菜っ葉` | Near-circular gloss | **Trivial** | 「菜っ葉：食用にする葉物の野菜」 — 菜 + 葉 restated as 葉物の野菜, with 食用にする the only added content. The other six gate candidates all add a real predicate or mechanism (Section 2). | Reword, e.g. 「菜っ葉：ほうれん草や小松菜など、葉の部分を food として食べる野菜」 → in Japanese: 「菜っ葉：ほうれん草や小松菜など、葉の部分を食べる野菜」. |
| **N7** | 聴解問題2-例 / 問題2-5番 | Two lodging-reception scenes in one section | **Observation — not filed as a finding** | 例 = 「ビジネスホテルのフロントで、係員と男の人が話しています」 (extending a stay); 5番 = 「ホステルの受付で、男の人と女の人が話しています」 (checkout procedure). Both are drawn scenarios (`ビジネスホテル:延泊`, `ホステル:チェックアウト`), both 旅行・観光, both a lodging front desk, in the same 大問. The errands differ, so this is not the §5 "same errand" fail — but the setting repeats inside one section and the 例 is heard immediately before. | No rule is breached — `exam-qa-review` §5's bar is the same *errand*, and these are different errands. Recorded so a second occurrence is recognisable. For the next draw, add lodging-reception to the same-section adjacency the sampler avoids, or move one of the two to 問題1. |
| **F15** (carried) | 聴解問題4 | Already-done distractor shape at 3 by intent | **Open — skill, not paper** | See Section 1. Rule unchanged, paper compliant as written, 3/24 distractors is inside the gate's own official band. | Widen `choukai-items.md:364`'s token list; see RC-4. |

**Filed findings: N2, N3, N5, N6 — four, all Minor or Trivial.** N1 and N7 are observations against no rule; F15 is a carried skill finding. None of the seven is an automatic fail, none affects a key, and none makes an item unanswerable or two-answered.

---

## Section 6 — Root-cause table (step 6.5)

Recurrence test applied first, by measuring the papers on disk — not by judgement.

| Finding | Code | Tests showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|
| **N5** (問題7 stem dispersion) | `GATE-BLIND` + `RULE-UNENFORCEABLE` | **12 of 12** papers on disk. Measured 問題7 stem means: 48.8 / 51.6 / 55.8 / 48.5 / 57.4 / 47.7 / 48.6 / 56.9 / 55.9 / 54.3 / 54.3 / **52.8**. **Every paper has ZERO stems under 30 JP chars**; official 7/2025 has one at 26 and 12/2025 one at 23. Systemic by definition. | `tools/check_consistency.py` + `.agents/exam-qa-review/SKILL.md` §3 + `question-authoring/references/bunpou.md` | The rule is written one-directionally ("fail if the average is under ~35, or several sit under ~30"), so twelve papers have optimised the floor and nothing has ever pushed back. Replace with a two-sided **distribution** requirement and gate it: `check_p7_stem_distribution()` — FAIL when the 12-stem mean is outside **36–52**, when **fewer than 2** stems sit under 34 JP chars, or when max−min is under **25**. All three are string-decidable. Mirror the same three numbers into `bunpou.md` §問題7 as a construction instruction ("write two short stems FIRST — 25–34 chars, no background clause — then the ten long ones"), because a rule verifiable only after writing gets skipped. |
| **N4** (`qa_eval.py` phantom items) | `GATE-WRONG` | Affects every paper whose `聴解.md` carries a `セクション構成表` containing numbers — i.e. every paper since that rule landed. The symptom is silence-plus-noise: it reports discrepancies that cannot exist. | `tools/qa_eval.py` | Two lines: (1) truncate the 聴解 source at the `## セクション構成表` heading before parsing keys; (2) reject any parsed `(item, key)` pair where `key not in {1,2,3,4}` or `item > 101`, and hard-error rather than reporting it as a discrepancy. A blind-solve evaluator that emits false discrepancies is worse than none — it trains reviewers to discount the one automated support the blind solve has. |
| **N2** (構成表 label survived its own line's rewrite) | `GATE-BLIND` (count) + `RULE-MISSING` (re-derivation) | 2 occurrences in this test alone: round-1 **F14(a)** (tally under-counted), now **N2** (label no longer matches the rewritten line). Same class, one fix round apart. | `tools/check_consistency.py` + `.agents/question-authoring/references/choukai-items.md` §"Write the SECTION TABLE" | Round 1 already proposed the gate half and it was **not implemented**: now that this paper has demonstrated a working closed vocabulary `{既に完了, 別の人に割り当て, 順番待ち, 後回し, 実行不可, 規則で不可, 条件不足, 不要, 明確に否定}`, promote it into `choukai-items.md` as mandatory and add `check_choukai_elimination_tokens()`: parse the 構成表's 消去方法 column, FAIL on any token outside the closed set, and FAIL when any token appears in more than 2 rows of one 問題 (例 counted). Then add the sentence the gate cannot check: *"When a fix rewrites a script line, re-derive that row's 消去方法 token from the NEW line. A label that survives the rewrite of the line it describes is the defect, not the fix."* |
| **N3** (stale `logs/topics.json` notes) | `RULE-MISSING` | 2 papers: `20260817_1` shipped a stale `shapes` field (already recorded in `exam-qa-review`'s ground rules); this paper ships a stale `notes` field. Same class — a hand-off field describing a discarded draft. | `.agents/exam-qa-review/SKILL.md` ground rules | The existing rule enumerates exactly four fields (`surfaces`, `themes`, `shapes`, `closing_moves`) and `notes` is outside the list, so it is the one field nobody re-reads. Extend it to five and add the verifiability clause: *"Every claim in `notes` that quotes a paper string must quote a string that is still in the paper. A note naming an artifact the fix removed (願ってもない at 問題9-51; 「よそ」 in the script) is worse than no note — the next blueprint stage plans around it."* |
| **N6** (near-circular gloss) | `RULE-UNENFORCEABLE` | 1 paper at this severity; the gate's candidate list fires on 3 papers (20260817_1/2/3), all previously judged false positives. | `.agents/question-authoring/references/dokkai.md` §（注N） | "Fail trivial circular definitions" is a judgement with no procedure, so it is decided ad hoc every time. Add the authoring-time test: *"Write the gloss, then delete from it every character that also appears in the headword. What remains must still identify the term. 「菜っ葉：食用にする葉物の野菜」 leaves 「食用にする物の野菜」 — insufficient. 「触診：体に手を触れて状態を確かめる診察の方法」 leaves 「体に手を触れて状態を確かめるの方法」 — sufficient."* This is the same test the gate approximates, moved to where it can be acted on. |
| **N7** (two lodging-reception scenes in one section) | `RULE-MISSING` | 1 paper. Not systemic yet; filed so the second occurrence is recognisable. | `.agents/exam-blueprint/SKILL.md` + `sample_items.py` | The sampler enforces theme caps and cross-test cooldown but has no notion of *setting adjacency within one section*. Add a `setting` field to `listening_scenarios` entries (`宿泊受付`, `郵便窓口`, `教室`, …) and make `sample_items.py` refuse to place two entries with the same `setting` in the same 大問, 例 included. |
| **F15** (carried) | `RULE-UNENFORCEABLE` | 2+ papers (the cap exists because 9/11 and 8/11 shipped; 20260810_2 still shows 8/11 in the gate output). | `.agents/question-authoring/references/choukai-items.md:364` | Unchanged since round 1. Widen the token list to `(もう / すでに / さっき / 先ほど / 今しがた / たった今 + 〜た)`, and restate the neighbouring cap as a concentration bound (round 1 showed the ≤2-per-shape form is arithmetically unsatisfiable: 22 distractors, 5 named shapes, max 20 slots). |

### The round-1 skill and gate edits were NOT applied

`git log -- .agents/ tools/` shows no commit after `c18e6fd` (which predates round 1), and `git status` shows exactly one working-tree change under `.agents/`: the deletion of 影 from `pools.json`. **Every one of round 1's 13 root-cause edits is still open**, including the two `RULE-CONFLICT` rows inside `exam-qa-review/SKILL.md` itself. The ones this review saw fire again or would still fire:

| Round-1 RC | Still open? | Evidence from this round |
|---|---|---|
| F1 → `verify_scramble.py` returns the same `RESULT: WARNING` for every item | **Open** | Still uninformative; F1 was fixed by hand-reasoning, not by the tool. |
| F2 → add a `src` provenance field to vocab pool entries | **Open** | Only 影 was deleted. The next `context_words` draw has the same blind spot. |
| F3 → final-sentence template check | **Open** | The paper was fixed by rewriting; the gate proxy that missed it is unchanged. |
| F4 → closed-vocabulary 消去方法 gate check | **Open** | The *paper* adopted the closed vocabulary voluntarily. The gate still cannot read it — which is how N2 got through. |
| F5 → `check_choukai_closing_turn_shape()` + last-line keyword check | **Open** | The paper was fixed and its 構成表 documents a hand-run of exactly the check that was proposed. No code. |
| F6 → de-duplicate the 引っ越し / カルチャー pool entries, add a `key` field | **Open** | `pools.json` still carries all three 引っ越し strings. This will re-fire. |
| F7/F8 → bind the cloze's theme, list quick_response phrases in the topic table | **Open** | Fixed by rewriting 問題9; nothing prevents the next paper. |
| F9 → fix moji-goi's own うんが example, which breaks its own rule | **Open** | `moji-goi.md` still teaches the うんかい-broken set as a model. **This is the highest-value single edit on the list** — a reference file that demonstrates the violation it forbids. |
| F10 → make "one grammar point, one key" a number | **Open** | I applied it by hand at 1 occurrence; the clause is still unactionable prose. |
| F11 → extend `check_choukai_key_paraphrase` to the key's final predicate | **Open** | Gate still reports only `0/4 are verbatim token-matches` — 4 of 27 keys examined. |
| F13 → moji-goi 問題5 "each option idiomatic on its own" | **Open** | — |
| F14(b) → have `make check` print measured per-talk char counts | **Open** | The 構成表 author had to measure by hand and document two measures. |
| 2 × `RULE-CONFLICT` in `exam-qa-review/SKILL.md` (問題3 affix rule; 「言及なし」 in 問題3 解説) | **Open** | Both still stand. This paper's five 問題3 解説 cells read 「〜は出てこない」/「触れていない」, which under this skill's literal ground-rule text is an automatic fail on 5 items and under `choukai-items.md` (the owner) is required. I applied the owner's rule, per AGENTS.md. |

Per `exam-qa-review` §6.5, none of this blocks **this paper** — a paper reaches PASS when the paper is fixed. All 18 open items (13 carried + 5 new) **block the next generation run**, and must be applied or explicitly rejected with a reason before a new test is authored.

---

## Section 7 — Coverage statement

| Step | Ran on | Result |
|---|---|---|
| 0 — Blind solve | `qa/20260817_3/keyless.md` only (1069 lines), rebuilt by `make keyless 20260817_3` at the start of this session; then `tools/qa_eval.py`, then a direct parse of both key tables | **101 / 101, zero mismatches** |
| 1 — Key-by-key proof | all 101 items across `言語知識・読解.md`, `聴解.md`, `聴解スクリプト.txt` | Every row in Section 3 carries its deciding line, quoted from the source |
| 2 — Distractor elimination | all 101 items, one reason per wrong option | No second defensible answer found. 問題8's five sets enumerated by hand for uniqueness |
| 2b — Distractor plausibility | 問題1–6 functional-category line per set; 問題1's two-branch rule; 問題2's kana-skeleton rule; 聴解問題1–3 grounding traced to a script line for every wrong option | No option dies for a reason unrelated to the tested point; no non-word option; no fabricated 聴解 distractor |
| 2.5 — Level band | 問題1–9 keys + 即時応答 idioms, calibrated against `refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md` and `17.N2 12-2025/booklet.md` 問題4–7 read directly; 問題7–9 also covered by `level_band_grammar.txt` | No TOO_HARD, no TOO_EASY. One easy-end observation (N1) |
| 3 — Mechanical reads | measured on the shipped files with my own scripts, not read off the gate: 注N counts, marker pairing, ruby, 中略, marked spans, option length ratio, both longest-key rates, rank spread, quantifier scan, 問題7 stem distribution, 問題9 body length and option lengths, 聴解 length metrics | N5 |
| 4 — 聴解 structure | `セクション構成表` read as columns and **re-derived from the script**, not trusted; all quotas; 例 announced number vs pre-mark vs dialogue; first and last spoken line of every 問題1/2 item read as a column; narration ↔ label ↔ `SPEAKER_MAP` | N2 |
| 5 — Topic table | this paper + the two before, re-tagged from the shipped surfaces; headline set intersections; closing-move column re-read from the final sentences; 47 surfaces compared pairwise | N7 (observation) |
| 6 — Provenance & spec audit | `test_spec.json` ↔ `logs/ledger.json` ↔ shipped items ↔ `pools.json`; `answer_positions` (101 prescribed); cooldown intersection; 22-char copyright scan over 62 reference/imported files | Clean. N3 is a `logs/topics.json` documentation defect, not a provenance mismatch |
| 6.5 — Root cause | Section 6, with the recurrence test measured across all 12 papers for N5 | 6 rows + the carried round-1 list |

### `make check` — exit 0, 62 warnings, exactly ONE on this paper

| WARN | Resolution |
|---|---|
| `20260817_3: （注N） definitions introduce words the term does not contain: 農泊 / 菜っ葉 / 管理組合 / 離島 / 血糖 / 触診 / 初診` | **False positive on all seven**, under the check's own printed criterion — each definition adds a predicate, mechanism, or scoping criterion the headword's kanji do not carry, and all seven headwords are correctly chosen (recent coinage, institutional, medical, or colloquial). Full reasoning and the per-gloss table in Section 2. Not a `GATE-WRONG` finding: the check lists candidates and instructs the reader to judge, which is what it did. One residual nit — 菜っ葉's gloss is near-circular — filed as **N6**. |
| The other 61 | All on other tests (20260807_1 … 20260817_2). Out of scope for this review. |

Also run and read: `make keyless 20260817_3` (clean build, keys stripped), `python3 tools/qa_eval.py` (see N4), `git log -- .agents/ tools/` and `git diff .agents/exam-blueprint/references/pools.json` (to establish which round-1 root-cause edits landed — one did).

### Source stillness

`shasum` re-run at the end of the review:

- `言語知識・読解.md` = `09abaea058359743a618aef853fe97bc3b5d5ce1` — unchanged
- `聴解.md` = `3df152b5d618790c515ac1847e245cb9500a4b4a` — unchanged
- `聴解スクリプト.txt` = `55361ffa7c57658f5a34765d0db72be30548ccb7` — unchanged

No fixing pass ran underneath this review; every byte offset claimed above still holds.

---

## Section 8 — Skips, stated explicitly

1. **`聴解.mp3` was never listened to — by me or by anyone, at any point in this paper's life.** I have no audio playback in this context. **Prosody, pitch accent, speaker attribution as actually voiced, the naturalness of Edge-TTS on 「飢饉」「六畳／八畳」「不在連絡票」「一石二鳥」, whether the four re-synthesised items sound like their neighbours, and whether the answer pauses land where the chapter marks say — are ALL UNVERIFIED.** What I verified mechanically instead: `聴解_チャプター.json`'s `script_sha` = `55361ffa7c57` = the shipped script's sha (gate confirms); MP3 mtime 18:28:55 postdates the script's 18:22:53; the pacing sha matches; every speaker label resolves in `SPEAKER_MAP` with a voice gender consistent with its narration; no scored item contains an answer reveal. **A human must listen to this MP3 end to end before the paper is served.** This is the single largest unverified surface in the paper and it has now survived two QA rounds.
2. **Shin Kanzen / Soumatome page lookups were not performed for the 問題1–6 keys.** Both are scanned images with no text layer. I calibrated the band against the official archive's own 問題1–6/問題7 items in `refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md` and `17.N2 12-2025/booklet.md`, read directly, plus pool provenance. A page-level confirmation of いきなり (N1) against the two N2 volumes would settle the one observation I accepted.
3. **`make model-answer` was not run** and `詳細解説.json` does not exist, so `check_model_answer_option_sync` has nothing to compare — the 模範解答 ↔ 問題冊子 sync check in `exam-qa-review` §3 is **not applicable yet**. Per `AGENTS.md` §5 the model answer is the final step, after QA passes.
4. **No fixes were applied**, to the paper or to any skill — including the two `RULE-CONFLICT` rows inside `exam-qa-review/SKILL.md` that round 1 identified and that I re-confirmed are still open. I left them so the whole work list moves together and so this report records what the rules said when the paper was reviewed.
5. **I did not re-litigate F6's re-angle-vs-reroll decision**, per instruction; I reviewed the shipped re-angle on its merits and accepted it, while recording that the underlying pool duplication that caused it is unfixed.
6. **The other 11 papers' 問題7 stem distributions were measured but not reviewed.** N5's recurrence test shows all 12 papers carry the class; whether the other 11 should be repaired is a coordinator decision, not this review's scope.

---

## Section 9 — Verdict

Steps 0–6 all ran, on all 101 items, with no sampling. The blind solve matched the key on every item. Fourteen of round 1's fifteen findings are closed at the paper level, verified against the artifact rather than against a claim; the fifteenth (F15) is a skill defect that the paper does not breach as the rule is written. There are **no automatic-fail findings** — this paper has one defensible answer per item, every key supported by a quoted source line, every 聴解 distractor grounded and denied, a clean provenance chain, and zero reproduction from the reference archive.

Four Minor/Trivial findings remain open against the paper: **N2** (a `セクション構成表` label that survived the rewrite of the line it describes), **N3** (two stale claims in `logs/topics.json`'s hand-off note), **N5** (問題7's twelve stems written to one long template, with no short stem at all), and **N6** (a near-circular gloss). `exam-qa-review` §7 permits PASS only with zero findings open, and the reviewer does not negotiate the bar.

Repair notes for the fix round: **N3** and **N6** are text-only edits touching no item. **N2** is a one-line change to the 問題1 例 script and therefore requires `make mp3` and a rebuild. **N5** touches 3–4 問題7 stems, which sends those items and the whole of 問題7 back through steps 1–4. If the coordinator judges N5 out of scope for this paper — it is a 12-of-12 systemic class better repaired as a pipeline change than one paper at a time — the remaining three fall inside `jlpt-test-generation`'s stage-4 ≤3-findings exception and may be fixed directly without a round 3. That is the coordinator's call to make explicitly, not mine to assume.

**QA: FAIL (4 findings, 0 automatic)**
