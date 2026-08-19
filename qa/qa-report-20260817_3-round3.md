# QA Report — `20260817_3` — Round 3 (final)

- Date: 2026-08-19
- Reviewer: fresh-eyes Stage-4 QA context (authored nothing; wrote neither prior report)
- Reviewed revision sha1:
  - `言語知識・読解.md` = `cc08ccb1087efb667f5c34b87364b6890688959e`
  - `聴解.md` = `c9d70682b6d285d434a371eae2a35f8702fa0534`
  - `聴解スクリプト.txt` = `61333cbd3e880207a86b629dbaa9962a8a5912ce`
- Blind solve source: `qa/20260817_3/keyless.md` (regenerated at start of this round)

Sections are appended as they are completed.

## 0. Blind solve (written BEFORE opening any keyed source)

Solved from `qa/20260817_3/keyless.md` only (regenerated this round; render sha1[:12] match the header above). No keyed file, no prior QA report, and no `test_spec.json` was opened before this list was committed to disk.

**言語知識・読解 (1–71)**

| # | 答 | # | 答 | # | 答 | # | 答 |
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
| 18 | 2 | 36 | 2 | 54 | 4 | | |

**聴解 (30 items)**

- 問題1 1–5番: 2, 3, 2, 1, 3
- 問題2 1–6番: 4, 2, 3, 2, 1, 4
- 問題3 1–5番: 3, 3, 3, 1, 4
- 問題4 1–11番: 2, 3, 2, 1, 2, 3, 2, 2, 3, 3, 1
- 問題5 1番: 1 / 2番 質問1: 2, 質問2: 4

### Blind-solve diff

`python3 tools/qa_eval.py tests/20260817_3 --answers "[…]"` →

```
Total Scored Items : 101
Agreement with Key : 101 / 101 (100.0%)
Discrepancies      : 0
```

**101/101, zero mismatches.** Every key is the answer an unaided N2-competent
solver reaches from the paper alone, so no mis-key and no "second answer that
beat the key" exists at the level a blind solve can detect. (This does **not**
clear two-defensible-answer items where the key is *also* right — that is
step 2's job, below.)

## Entry condition — `make check`

`make check` → **exit 0**, `All checks passed (26 skipped), 111 warning(s)`.

Exactly **two** of the 111 warnings land on `20260817_3` (plus one repo-level
pool warning that names no test). Both are addressed in §Coverage below.

### IMPORTANT — the gate moved *during* this review

I ran `make check` twice, ~5 minutes apart.

| | run 1 (≈11:27) | run 2 (11:32) |
|---|---|---|
| exit | **0** | **2 (FAIL)** |
| warnings | 111 | 112 |
| WARNs on `20260817_3` | 2 | **3** |

Two things changed underneath me, neither of them in `20260817_3`:

1. **`tools/check_consistency.py` was edited at 11:28:20**, adding a **12th**
   new check, `check_choukai_setting_adjacency()`. It produced no output at all
   in run 1 and fires on every test in run 2. So the root-cause pass I was asked
   to audit was **still in flight** when this round started; "11 new or upgraded
   gate checks" is now 12.
2. **`tests/20260818_1/test_spec.json` was written at 11:31:38**, together with
   `logs/ledger.json`. That is `make sample` for the **next** paper. It is the
   sole cause of the new FAIL:
   `FAIL both Markdown sources present — missing ['言語知識・読解.md', '聴解.md']`
   — a blueprint-only folder that has no booklets yet.

**Source stillness for the paper under review: intact.** The three sha1s in the
header are byte-identical at the start and at the end of this round
(`cc08ccb1…`, `c9d70682…`, `61333cbd…`), mtimes 10:43–11:16, all *before* my
first tool call. The review is not void. But two process facts are on the record:

- The QA entry condition (`make check` green) is **currently red**, for a reason
  outside this paper.
- `exam-qa-review` §6.5: open root-cause findings **block the next generation
  run**. A next generation run (`20260818_1`) was started before this final QA
  round returned a verdict. Filed below as **R3-6**.

## 1. Round-2 findings N2 / N3 / N5 / N6 — closure verified against the artifacts

Method: each re-derived from the shipped bytes. No claim of a fix was accepted
as evidence.

| # | Round-2 defect | Status | Evidence from the artifact |
|---|---|---|---|
| **N2** | 問題1 例 row labelled `順番待ち` while the script line 「それは、あとで一緒に書き込もう。」 carried no dependency | **CLOSED** | The script now reads (`聴解スクリプト.txt`, 例) 「名簿は、**待ち合わせの場所が決まってから**書き込むから、まだいいよ。」 — an explicit dependency, so `順番待ち` is earned. The fix did **not** take round 2's suggested wording, and the 構成表 says why: that wording would have returned 「場所」 to the last spoken line, where it appears in printed option 1 only, re-creating F5. Instead the roster exchange moved mid-dialogue and the 例 now closes on 「それは先週のうちにみんなに伝えてあるよ。」 (既に完了). I re-derived all 18 cells from the current script: 既に完了 2 (例/3番), 実行不可 2 (例/2番), 順番待ち 2 (例/3番), 不要 2 (1番/5番), 条件不足 2 (1番/4番), 後回し 2 (1番/2番), 別の人に割り当て 2 (2番/3番), 規則で不可 2 (4番/5番), 明確に否定 1 (5番). **No token over the 2-row cap.** Gate agrees: `ok … 問題1 消去方法 uses the closed vocabulary (6 rows)` — and `20260817_3` is *not* in `ELIMINATION_VOCAB_GRANDFATHERED`, so that is a real pass, not an exemption. |
| **N3** | `logs/topics.json` `notes` carried two claims about strings the fix had removed | **CLOSED** | `notes` is fully rewritten and dated `VERIFIED AGAINST THE SHIPPED FILES 2026-08-19`. I grepped every string it quotes: 「値段と量」 present; 「願ってもない」 **0** occurrences in `言語知識・読解.md` and the note no longer claims it; 「よそ」 **0** in the script and the note no longer claims it. The one string quoted that is *not* in the paper — 「書かない窓口」 — is explicitly framed as what 問題9 was rewritten **from**, i.e. a history statement, not a claim about the shipped paper. All five fields (`surfaces`/`themes`/`shapes`/`closing_moves`/`notes`) are mutually consistent and match the shipped surfaces. |
| **N5** | 問題7: 12-stem mean 52.8, min 46, spread 12, zero stems under 30 | **CLOSED, on merit** | Measured now: `[29, 29, 32, 39, 49, 50, 51, 52, 53, 56, 57, 58]`, **mean 46.2**, **3 stems under 34**, **spread 29**. All three of `bunpou.md`'s numbers are met (36–52 / ≥2 / ≥25). Compression was done by *shortening* (31, 37 became two-line dialogue stems; 41 「物置の道具はほこり（　）で、使えそうなものは一つもなかった。」), not by lengthening. 問題7 also now carries **3** dialogue/setting-label stems (31 会議で, 36 職場で, 37 店で) against the "fail zero" clause. **Caveat filed as R3-3:** `20260817_3` is still listed in `P7_DISTRIBUTION_GRANDFATHERED`, so a future regression here would print WARN, not FAIL. |
| **N6** | `（注3）菜っ葉：食用にする葉物の野菜` — near-circular | **CLOSED** | Line 288 now reads `（注3）菜っ葉：ほうれん草や小松菜など、葉の部分を食べる野菜`. Apply `dokkai.md`'s new subtraction test (delete every character the headword contains): 「ほうれん草や小松菜など、の部分を食べる野」 — two concrete exemplars plus a predicate survive. Sufficient. |

**Round-2 closure score: 4 of 4 closed.** No fix introduced a new defect that I
could find; the one residual is the grandfather entry noted above.

## 2. Round-1 F1–F15 — regression spot-check

Three rebuild cycles and a fix round have run since round 2 confirmed these.
I re-derived each from the current bytes.

| # | Round-1 defect | Still closed? | Evidence now |
|---|---|---|---|
| F1 | 問題8-44 second grammatical ordering | **YES** | Card 1 is still 「部屋を見るだけでなく」; 解説 line 527 still spells the last-slot proof. I re-enumerated: only 1-2-3-4 survives, ★=slot 3=card 3=key **3**. |
| F2 | 問題4 set N3–N4 (姿/跡/光/影) | **YES** | Set is 引き分け/手数料/研修/読書家/しぼむ/道徳/いきなり. New gate `check_moji4_option_set_level` reports `0 candidate(s)`. 影 still absent from `pools.json`. |
| F3 | Five 読解 closings on one skeleton | **YES** | 「そのものではなく」 **0** occurrences in the whole file. New gate `check_dokkai_final_sentence_templates` reads 12 finals, no template over the cap of 2. |
| F4 | 問題1 消去方法 over cap | **YES** | Re-derived above (N2 row): no token over 2 rows. |
| F5 | 問題1 closing turns rhymed / leaked the key | **YES** | Gate: `聴解問題1/2 closing turns differ and give nothing away (0 rhyme(s), 0 leak(s))` — and this test is not in `CLOSING_SHAPE_GRANDFATHERED`, so it is a genuine pass. |
| F6 | 聴解問題2-1番 repeated the previous paper's moving-quote errand | **Re-angle stands; pool defect now gated** | Reviewed on its merits below (§4). Gate: `no 聴解1/2/3/5 errand repeats 20260817_2's` = ok. The pool `key` field now exists and makes the residual visible as a named WARN. |
| F7 | 問題9 repeated 20260817_2's 行政・手続き subject | **YES** | 問題9 is 「値段と量」. In the whole 読解 half: 申請書 **0**, 記入 **0**. (窓口 occurs 5×, all in 問題11(3)'s 相談窓口 and 問題14's 申込窓口 — unrelated subjects.) |
| F8 | 問題9 thesis echoed two 聴解 items | **YES** | Same rewrite; no 読解 surface now shares a subject with 聴解問題4-1番 or 2-5番. |
| F9 | 問題2-9 grid {運,雲}×{河,海} | **YES** | Shipped 運河/運賀/雲河/雲賀; every option reads うんが. |
| F10 | keyed forms recurring in the 読解 prose | **YES** | Now gated: `no 問題7/9 keyed form appears more than 1× in the 問題10-14 prose` = ok, un-grandfathered. Hand check: 「その反面」 0 in prose (the 1 hit is the printed option itself), 「本末転倒」 0, 「はずだ」 1 (問題12A 「姿を消したはずの種が」, a 連体 use — exempt by rule). |
| F11 | 聴解問題2-2番 key reused the script's own verb | **YES** | よそ **0**, 業者 **0**, あずけ **0**, 回す **0** in `聴解スクリプト.txt`. |
| F12 | 聴解問題4-5番 key carried an unstated premise | **YES** | Key is 「とんでもないです。ちょうどお待ちしていました。」 |
| F13 | 問題5-21 option 2 was the marked 「手先が上手だ」 | **YES** | Line 72: `2. 細かい作業が得意だ`. |
| F14 | 構成表 inaccurate (undercount, wrong talk lengths) | **YES** | Tally enumerates all nine tokens with row ids and I reproduced it; the table prints both talk measures and the gate prints its own (`299/306/325/337/318/295`). |
| F15 | 問題4 already-done distractor shape at 3 by intent | **Paper acceptable; skill still open** | Unchanged since round 2. |

**No round-1 regression found.** Every F closed at round 2 is still closed.

## 3. Per-question walkthrough — all 101 items

### 文字・語彙 (問題1–6)

| 項目 | 鍵 | 判定 | どこが問題か / 決め手 | どう直すか |
|---|---|---|---|---|
| 問題1-1 | 3 そうぞく | OK | 相=ソウ・続=ゾク。2×2 {そう,ぞう}×{そく,ぞく}; 1/2/4 are 清濁 derivations, none a word. Okurigana not exposed. | — |
| 問題1-2 | 4 めいれい | OK | 命=メイ・令=レイ。2×2 {めい,めん}×{れい,れん}, 長音⇄撥音 axis; 1/2/3 non-words. Easy end of band but the discrimination is real. | — |
| 問題1-3 | 1 ろんじる | OK | 論=ロン, no alternative reading. Branch (b) set: 感じる/応じる/信じる are all real 漢語+じる verbs of the same 思考・言語行為 field; all four share 「じる」, so okurigana selects nothing. | — |
| 問題1-4 | 4 せいざ | OK | 星=セイ・座=ザ。2×2 {せい,ぜい}×{さ,ざ}. 1 (せいさ) is the 清音 derivation; 精査 exists but is a different field, so it is not selectable from 「冬の…がはっきり見えた」. | — |
| 問題1-5 | 1 じっさいに | OK | 実=ジツ→促音化ジッ, 際=サイ。2×2 {じっ,じつ}×{さいに,ざいに}; all four share the 「に」 tail. | — |
| 問題2-6 | 3 構成 | OK | {構,講}×{成,製}, all four read こうせい; 講/製 are real 常用 glyphs with the wrong sense. | — |
| 問題2-7 | 4 豊富 | OK | {豊,報}×{富,婦}, all read ほうふ. | — |
| 問題2-8 | 3 飢饉 | **自動不合格** | `言語知識・読解.md:27` — `饉` is **not a 常用漢字** and not in the N2 kanji scope; it appears in **0 of the 31 official sittings** in `refs/JLPT_N2_NEW/`. `moji-goi.md` §問題2 states the bar as *"Every constituent kanji glyph must be a legitimate, standard 常用/N2 kanji"*. The paper's own 解説 is the tell: rows 6/7/9/10 all end 「四字とも常用漢字」 and row 8 conspicuously does not. Off-level key (`exam-qa-review` automatic-fail list). | The defect is the **pool entry**, not the sentence — `pools.json:1742` `"飢饉"`. Delete it from `orthography` and `sample_items.py --reroll orthography`; never hand-substitute a target. Then add a 常用漢字 whitelist check for 問題2 options (see R3-1). |
| 問題2-9 | 1 運河 | OK | {運,雲}×{河,賀}; 運=ウン, 雲=ウン, 河=ガ, 賀=ガ — all four parse as the stem kana うんが. (F9 fix holds.) | — |
| 問題2-10 | 4 井戸 | OK | {井,居}×{戸,度}; 居戸/井度/居度 are pseudo-compounds; all four glyphs 常用. | — |
| 問題3-11 | 3 内 | 要修正 (軽微) | Key and item are sound — 「持ち出しが禁止されている」 decides 内, and 外 contradicts it, 側 marks a standpoint (会社側), 間 needs two points. **But** the drawn target is `pools.json` `"内〜(国内)"`, notated as a **prefix**, while the item tests the **suffix** 〜内 (建物内) — and the pool entry's own example 国内 is itself a suffix use. The pool string is internally contradictory. | Fix the pool entry to `"〜内(国内)"`. No paper edit needed — the item matches the example, which is the half that is right. Filed as R3-2. |
| 問題3-12 | 3 仮 | OK | 「正式な契約は来月だが」 pairs with 仮契約. 準/略/半 are real 接頭語 of the same family; 準契約・略契約・半契約 are not words. | — |
| 問題3-13 | 2 旧 | OK | 「古い建物が今も残っている」 decides 旧市街. 前/現/元 all attach to *offices* (前会長/現社長/元首相), not to 市街 — same functional family, so this is `moji-goi.md`'s permitted "not all four attach" shape, not a free elimination. | — |
| 問題4-14 | 1 引き分け | OK | 「両者とも決め手を欠いたまま持ち時間を使い切り」 — 棄権 is killed by 持ち時間を使い切り, 逆転勝ち/勝ち越し by 決め手を欠いた. All four are 勝負の結果 nouns. | — |
| 問題4-15 | 1 手数料 | OK | 「ほかの銀行の口座に振り込む」 — a procedure fee. 送料 needs a shipped object, 代金 a purchased one, 保証金 a returnable deposit. All four are 金銭 nouns. | — |
| 問題4-16 | 4 研修 | OK | 「一か月間の（　）を受け、そのあと…配属される」 — 見習い is a status not a thing one 受ける, 面接 precedes hiring, 講演 is not month-long. | — |
| 問題4-17 | 3 読書家 | OK | 「家の壁は一面が本棚」. 愛好家/専門家 require a preceding domain noun; 努力家 is unrelated to books. All four are 〜家 person nouns. | — |
| 問題4-18 | 2 しぼんで | OK | 「空気が少しずつ抜けて」. ふくらむ is the reverse, ほどける needs a knot, こぼれる a liquid. All four are テ形 自動詞 of form change. | — |
| 問題4-19 | 1 道徳 | OK | 「法律の問題ではなく（　）の問題だ」 requires a norm *outside* codified rules — 規則 is inside it, 礼儀 is etiquette, 権利 is an entitlement. | — |
| 問題4-20 | 4 いきなり | OK | 「思わず持っていた荷物を落として」 = unforewarned. 徐々に is gradual, あらかじめ is the opposite, たびたび is repetition. All four are time-manner adverbs. Easy end of the band (round-2 N1); the set holds. | — |
| 問題5-21 | 2 細かい作業が得意だ | OK | 「セーターくらいなら一日で編んでしまう」. Options are four ability predicates; calculation/strength/memory are none of them. Swap test passes. | — |
| 問題5-22 | 4 心に残った | OK | 印象的＝strongly remembered. 分かりやすい/意外/短い are three other evaluation axes. | — |
| 問題5-23 | 1 きちんとしている | OK | 「机の上の物の位置がいつも同じだ」. のんびり/落ち着いている/遠慮している are all 〜している character predicates but none is orderliness. | — |
| 問題5-24 | 1 しつこい | OK | 「聞いているうちに疲れてしまう」＋くどい＝repetitive. そっけない is the opposite pole, 厳しい/冷たい are other negative axes. | — |
| 問題5-25 | 3 自然に | OK | 「無理に暗記しようとしなくても」. わざと is the polar opposite, むやみに is heedless *deliberate* action, 一気に clashes with 「毎日使っているうちに」. | — |
| 問題6-26 | 1 | OK | 「持ち合わせがない同僚の昼食代を…立て替えておいた」 = pay on someone's behalf. 2 is 建て替える (different orthography), 3 組み替える, 4 買い替える — all inside the 〜替える family, none a domain jump. | — |
| 問題6-27 | 2 | OK | 「思い通りにならないとすぐ物に当たる」＋幼稚=immature (always pejorative). 1 needs 単純, 3 簡単, 4 幼い. | — |
| 問題6-28 | 4 | OK | 「営業部の山田さんあてにかかってきた電話を…取り次いだ」 = relay between two parties. 1 報告, 2 引き継ぐ, 3 教える — each lacks the go-between relation. | — |
| 問題6-29 | 2 | OK | 「事故のあと…平穏な日々が戻ってきた」. 1 needs 穏やか (water), 3 平然 (expression), 4 和らぐ (pain). All four stay inside the "calm" domain — a collocation trap, not a domain violation. | — |
| 問題6-30 | 4 | OK | 「専用の充電器が付属している」 = comes with the main object. 1 所属, 2 添付, 3 取り付ける. | — |

**問題1–6 level pass:** every key checked by hand against the N2 band. One
automatic fail (問題2-8). 命令/星座/実際に sit at the easy end but each option set
carries a real 清濁/長短/促音 discrimination, and official 7/2025's own 問題1
contains 辛い(からい), so they are inside the band as official uses it.

### 文法 (問題7–9)

問題7 stem lengths, all three numbers (`bunpou.md` §問題7): measured
`[29, 29, 32, 39, 49, 50, 51, 52, 53, 56, 57, 58]` → **mean 46.2** (band 36–52 ✓),
**3 stems under 34** (need ≥2 ✓), **max−min = 29** (need ≥25 ✓).
Dialogue/setting-label stems: **3** (31/36/37), against the "fail zero" clause.

| 項目 | 鍵 | 判定 | 決め手 / 問題点 | どう直すか |
|---|---|---|---|---|
| 問題7-31 | 1 はさておき | OK | 「名前はさておき、まず発売の時期を決めましょう」 — priority switch. はもとより adds rather than defers; といえども needs the same topic in the 後件; をよそに needs a third party's concern being ignored. | — |
| 問題7-32 | 3 てはじめて | OK | 「人は自分でやってはじめて…分かるものだ」. てからでないと demands a negative 後件; たとたん demands a one-off event; たところで demands a futile 後件. | — |
| 問題7-33 | 2 に反して | OK | 「予想…、売れ行きは前年を大きく下回り」. をもとに needs a deliberate act; に沿って means *as* predicted, contradicting 下回り; に応じて needs a varying quantity. | — |
| 問題7-34 | 1 まい | OK | 「今度こそ…山へ入るまいと決めている」 — negative volition. までだ inverts the meaning; わけだ cannot be the content of 決めている; ことか needs a degree adverb. | — |
| 問題7-35 | 2 だけあって | OK | 「老舗だけあって、料理も接客も申し分なく」. のわりに/とはいえ/どころか all require the 後件 to *defeat* the 前件; it confirms it. | — |
| 問題7-36 | 2 わけがない | OK | 「あの人が理由もなく遅れるわけがない。何か事情が…」. しかない would concede the lateness; ものではない judges propriety; ものがある cannot attach to 遅れる. | — |
| 問題7-37 | 4 抜きで | OK | B's 「二百円安くなります」 forces exclusion. 込みで/付きで both include; 次第で makes it conditional. | — |
| 問題7-38 | 1 にしろ | OK | The 前件 already prints 「進めるにしろ」; the paired form must repeat. からには/とすれば/につけ all break the 並立 frame. | — |
| 問題7-39 | 2 べき | OK | 「まず本人の話を聞くべきだと私は考えている」. きり needs タ形; ため needs a preceding reason question; ばかり means "only listens". | — |
| 問題7-40 | 1 向け | OK | 「海外の子どもに配る目的で作られ…初心者向けの絵本」. 頼み/込み/次第 cannot mark an intended audience. | — |
| 問題7-41 | 4 だらけ | OK | 「ほこりだらけで、使えそうなものは一つもなかった」. ずくめ needs a desirable/colour uniformity; がち needs an animate tendency; っぱなし needs a ます-stem. | — |
| 問題7-42 | 3 てまで | OK | 「住んでいた家を売ってまで資金を用意した」 — extreme means. たきり/たあげく/たところで each demand a different 後件 shape. | — |
| 問題8-43 | 4 一方 | OK | 兄は休日も(1)→朝早くから出かける(2)→**一方(4)**→弟は昼過ぎまで(3). Only 「弟は昼過ぎまで」 can precede 「布団から出てこない」; 一方 needs a 連体形 before it and a contrast clause after. 1 of 24. No bare adverb. | — |
| 問題8-44 | 3 自分の足で確かめた | OK | (1)(2)(3)(4) as printed; only 「うえで」 can precede 「決めようと思う」, and it requires the タ形 「確かめた」. F1 fix holds. | — |
| 問題8-45 | 1 ことがない | OK | 渋滞に巻き込まれて(2)→遅刻する(3)→**ことがない(1)**→ように(4). Only 「ように」 can precede 「毎朝…家を出ている」. | — |
| 問題8-46 | 1 しまった | OK | 弟は(2)→もうぐっすり眠って(3)→**しまった(1)**→にちがいない(4); only にちがいない closes a quoted clause before 「と思い」. | — |
| 問題8-47 | 4 申し出が | OK | ご本人から(1)→書面による(2)→**申し出が(4)**→ない限りは(3). Only 「ない限りは」 can precede the 読点+「登録内容を…」. Even under the marginal 2-1-4-3 reading, ★ (slot 3) is still 申し出が, so no second ★ answer exists. | — |
| 問題9-48 | 3 その反面 | OK | `[論理接続]` — 前段 = noticed at once; 後段 = 「何も感じないまま店を出る」. そのうえ adds same-direction; たとえば needs an example; ようするに needs a restatement. | — |
| 問題9-49 | 2 はずだ | OK | `[文末モーダル]` — 「少なくとも、売る側はそう考えてきた」 marks it as the seller's expectation. にすぎない devalues; どころではない reverses; ものではない moralises. | — |
| 問題9-50 | 3 損なわれやすくなる | OK | `[内容推論]` — 「気づかれずに済ませようとするほど」＋第4段落's 一割以上落ち込んだ. 高まっていく/変わらないだろう/問題にならない all contradict that result. | — |
| 問題9-51 | 4 本末転倒だ | OK | `[慣用・形式名詞]` — 「客に買い続けてもらうための売り上げなのに、その売り上げを守ろうとして中身を削る」 = ends and means inverted. 一石二鳥 is positive; 一長一短 needs one thing with two sides; 二者択一 describes 第2段落's stage, already past. Four distinct blank categories ✓; all options ≤ 8 JP chars (official max 14) ✓. | — |

**問題9 cloze body:** 738 JP chars (target ~500–700; gate floor 450). Slightly
long but inside the spirit of the rule; no finding.
**One grammar point, one key:** no form is keyed twice across 問題7/8/9, and no
keyed form occurs more than once in the 問題10–14 prose (gate ok, un-grandfathered;
hand-verified for 「その反面」0 / 「本末転倒」0 / 「はずだ」1-連体).

### 読解 (問題10–14)

Apparatus, measured: **31** in-body `（注N）` markers (official band 27–61, median
39) ✓; markers and definitions pair 1-to-1 per passage ✓; **3** `（中略）`, all
inside 問題11–13 ✓; **0** `<ruby>` ✓; 問題13 body over the 800-char floor ✓;
six marked spans (①②③④⑤ per block), each identical to its stem's quote and
pointer-sized (13–21 JP chars), none bolding the reasoning ✓.
Key predictability: `max/min ≤ 1.30` on all 20 items ✓; **uniquely** longest key
**4/20 = 20 %** (official 20 %, target ≤30 %) ✓; tied-longest **5/20 = 25 %**
(target ≤35 %) ✓; no key is a verbatim lift ✓.

| 項目 | 鍵 | 判定 | 決め手 (source line) | どう直すか |
|---|---|---|---|---|
| 問題10-52 | 4 | OK | 「新しい規程では、この扱いを二つに分けます」＋「同業他社での就業や、月二十時間を超える就業は、従来どおり申請と許可が必要です」— business type AND hours. 1 says "regardless of type" (denied), 2 says outside work is newly permitted (denied by 「従来は…許可が必要でした」), 3 says "after starting" vs 「開始前に届出書を」. | — |
| 問題10-53 | 3 | OK | 「対象は、賞味期限までの期間が九十日以上ある商品に限ります」= 三か月以上. 1 denied by 「加工食品の一部」, 2 by 「消費期限の表示がある商品は、これまでどおり日付まで」, 4 by 「八月三十一日までの入荷分は…従来の表示で販売」. | — |
| 問題10-54 | 4 | OK | 「片道十キロを超え、大型車の多い幹線道路を通る経路では負傷事故の割合が高いが、五キロ以内で自転車道の整備された道を行く経路では…変わらない」— distance × road type. 1 (車道/歩道) is not the passage's axis; 2 compares severity, not rate; 3 inverts the pairing. | — |
| 問題10-55 | 2 | OK | 「一度書いた行は消えない。だから書き出す前に、相手の顔を思い浮かべ…考えることになる」. 1 is the *screen*'s property; 3 is the belief the writer discards; 4 contradicts 「手が思考の速さについていかない」. | — |
| 問題10-56 | 2 | OK | 「なぜ始めたのか、何が面白くなくなったのかを本人に言葉にさせ、やめる時期を自分で決めさせること」. 1 denied by 「やめさせないことが忍耐力を育てる…には、無理がある」; 3 puts the adult back in charge; 4 refuses the question the passage answers. | — |
| 問題11-57 | 2 | OK | 「二晩のあいだに見たのは、畑と台所と、縁側から見える山の稜線くらいのもの」. 1/3/4 name reasons the passage never gives (取材の忙しさ / 案内された場所 / 夜が早い). | — |
| 問題11-58 | 1 | OK | 「旅先で私たちが持ち帰るのは、名所の写真よりも、そこで誰かが繰り返している日常のほうなのかもしれない」. 2 contradicts 「空いた民宿が何軒もある」; 3 contradicts 「手伝ってほしいと言われたのではない」; 4 is an evaluation the text does not make. | — |
| 問題11-59 | 3 | OK | 「ところが一度でも言葉を交わした相手であれば、その人が通る場所として意識されるようになる」. 1/2/4 are each present in the passage as *other* content (contracts, the survey record, 世帯数/築年数), so none is fabricated — each is raised then not connected to this feeling. | — |
| 問題11-60 | 3 | OK | 「挨拶を交わす、と答えた住民の割合が高い建物ほど、共用部の破損や放置物が少なく、修繕にかかる費用も低く抑えられていた」. 1 denied by 「共用部を保つのは定期的な点検や清掃の契約であり」; 2 denied by 「世帯数や築年数が近い建物どうしで比べても、この傾向は変わらなかった」; 4 swaps the dependent variable. | — |
| 問題11-61 | 1 | OK | 「事件や事故の当事者として名前が出た人、勤め先の不祥事とともに写真が流れた人が、何年たっても検索結果の上位に…見つけてしまう」. 2 invents a legal mechanism; 3 inverts the cause; 4 is not claimed. | — |
| 問題11-62 | 4 | OK | 「目立つのは、本人が書いたものではなく、他人が本人について書いたもののほうだという」. 1 is the *original* assumption («この言葉が使われ始めたころ»); 2 denied by 「転載先をたどりきることは難しい」; 3 not claimed. | — |
| 問題11-63 | 2 | OK | 「疑いは…都合の悪い情報を遠ざける口実にもなる」＋「確かめるとは、その情報が最初にどこから出てきたのかをたどり…」. 1/3/4 each add a claim about *how each is learned* that the text never makes. | — |
| 問題11-64 | 2 | OK | 「判断をいったん保留したまま出所をたどる、その地味な手間を惜しまない態度こそが、見分ける力の中身なのだと言える」. 1 denied by 「そのぶん正確に判断できるようになるとは限らない」; 3 overreaches 「たいてい見出しよりも慎重」; 4 not claimed. | — |
| 問題12-65 | 3 | OK | A「それらを作るのをやめてしまうという選択は現実的ではない」/ B「道路や施設を作るのをやめてしまうことはできない、という点に異論はない」. 1 is A-only and B qualifies it; 2/4 appear in neither. | — |
| 問題12-66 | 3 | OK | A「失われる分を数え、同じだけの環境を近くに用意していく仕組みが現実的である」/ B「計画の段階で、代えのきかない場所を開発の対象から外しておくこと」. 1/2/4 misattribute both sides. | — |
| 問題13-67 | 1 | OK | 「一つは、すでに診断がつき、同じ薬を続けている患者の定期的な受診である」/「もう一つは、初めての症状について診断を求める受診である」. 2 is a sub-detail of the first layer; 3 is a demographic split; 4 is the regulatory split, named separately. | — |
| 問題13-68 | 4 | OK | 「対面が担ってきた仕事のうち、情報の量が限られていても成り立つ部分を引き受ける仕組みである」. 1 denied by 「代わりに置かれるものではなく」; 2 inverts 「初診については対面を原則」; 3 is a first-layer detail. | — |
| 問題13-69 | 4 | OK | Combines 「情報の量が限られていても成り立つ部分」 with 「遠隔診療を便利だと感じるのは、通院の負担が重い人である」. 1 names 通信環境 where the text names 通院の負担; 2 denied by 「この層では対面の診察に及ばない」; 3 is a recommendation the text does not make. | — |
| 問題14-70 | 2 | OK | Two cells: 卓球「高校生以上の方」 (excludes a 中学2年生) AND ※「中学生以下の方が参加する種目は、保護者の同意書…の提出が必要です」. 1 denied by ※「当日、会場での現金のお支払いはできません」; 3 by ※「郵送では受け付けません」; 4 by マラソン「中学生以上の方」. **≥2 constraints ✓**, every referenced detail printed. | — |
| 問題14-71 | 2 | OK | Two cells: 親子ペアリレー 申込締切「9月26日」 vs 10月1日 AND ウォーキング大会 申込締切「当日受付」. 1 denied by 「1組1,500円」; 3 by ※「ウォーキング大会はこの数に含みません」; 4 by both 締切 cells. **≥2 constraints ✓**. | — |

### 聴解 (30 items)

`セクション構成表` read as columns first, then verified against the script (not
on trust). 正解 column: no two rows of any section name the same action or
object ✓. 消去方法: re-derived all 18 問題1 cells from the current script; no
token over the 2-row cap ✓ (table above, §1/N2). 質問型: 何をしますか only in
問題1, どうして/一番 in 問題2, 何について in 問題3 ✓. First/last spoken lines read
as a column: 0 rhymes, 0 key leaks ✓.

| 項目 | 鍵 | 判定 | 決め手 / 誤答の根拠となる台本行 | どう直すか |
|---|---|---|---|---|
| 問題1-例 | 1 | OK | 「これから下見に行って、みんなが待てる場所があるか見てきてくれる?」— announced 1番 = what the dialogue supports. Others: 順番待ち(名簿)/実行不可(カメラ点検中)/既に完了(持ち物). | — |
| 問題1-1番 | 2 | OK | 「開発部から試作品、借りてきてくれる?」＋「数に限りがあるらしいから、早い方がいいんだ」. 1 不要「予約は要らないよ」/3 後回し「練習は明日でいいよ」/4 条件不足「価格はまだ役員会で決まってない」. | — |
| 問題1-2番 | 3 | OK | 「実験ノートの元の数字と一つずつ照らし合わせてみてくれる?」. 1「グラフは、林くんが…」/2「装置が来月まで別の班に貸し出されてる」/4「来週の打ち合わせまでに直せばいい」. | — |
| 問題1-3番 | 2 | OK | 「今のうちに、請求はがきを地域ごとに分けといてくれる?」. 1「分け終わった順番どおりに…そのあとでね」/3「事務の川口さんが…貼ってくれる」/4「願書はもう百部ずつ束ねて棚に置いてある」. | — |
| 問題1-4番 | 1 | OK | 「一度お戻りになって、あの票を持ってきていただけますか」. 2「そこが空欄ですと受け付けられない」/3「あちらも番号を押していただく」/4「お荷物がこちらにある間はできない決まり」. | — |
| 問題1-5番 | 3 | OK | 「先に求職の申し込みの登録を済ませていただく必要があるんです」. 1「お取りいただかなくて大丈夫」/2「ハローワークを通してのお問い合わせと決まっている」/4「面接の日程を今日決めていただくことはありません」. | — |
| 問題2-例 | 2 | OK | 「明日の会議が急に一日増えちゃって」; announced 2番 matches. | — |
| 問題2-1番 | 4 | OK | 「四階なんだけどエレベーターがなくて。あと二名つけないと手が足りない」＋「四階まで持って上がるとなると全然違う」. 1「荷物、前の家より減らしたくらい」/2「うちは四月の半ばなの。混む時期はわざと外した」/3「距離はむしろ前より近いくらい」— each explicitly denied. Key requires the エレベーターなし→階段 inference; no key word appears in the script. | — |
| 問題2-2番 | 2 | OK | 「しみ抜き専門の工場に一度出すことになる」＋「店の中だけでは仕上げられない品」. 1「今週はむしろ空いている」/3「機械は先月入れ替えたばかり」/4「配送は毎日あります」. よそ/業者/あずける: 0 occurrences in the script (F11). | — |
| 問題2-3番 | 3 | OK | 「なので今日は、根元だけを染めて、毛先は次に…」→女「確かに。じゃあ、それでお願いします」. 1「今日また薬をのせると、切らなきゃいけない状態に」/2 withdrawn by 女 after 店長's push-back/4「それでも毛先に薬をのせることになるので、傷みは同じ」. 「のびた」 is earned by 女's own 「前に染めたところが伸びてきちゃって」. | — |
| 問題2-4番 | 2 | OK | 「音が出せるかどうかが一番でして」＋「夜しか時間が取れなくて」. 1「家賃は多少上でも構わない」/3「20分でも平気です」/4「狭くても気にしません」. | — |
| 問題2-5番 | 1 | OK | 「部屋の鍵をこの箱に入れといていただければ、それでおしまいです」＋「ほかの手続きは要りません」. 2「今は…なくしました」/3「それは特にお願いしてない」/4「お部屋の方は、そのままで大丈夫」. | — |
| 問題2-6番 | 4 | OK | 「あいているクラスに振り替えていただけますよ」→「振り替えができるなら、今度こそ続けられそうです」. 1「料金はどこも似たようなもの」/2「場所は、正直そんなに気にしてない」/3「先生がどんな方かは、始めてみないと分かりません」. | — |
| 問題3-例 | 2 | OK | 「来月からは、前の日の夜までにインターネットでお申し込みいただく形に改めます」; announced 2番. | — |
| 問題3-1番 | 3 | OK | 「繊維になる前の原料の状態まで戻す技術が実用化されてきました」＋「服が何度でも服に生まれ変わる」. 概要理解: the talk correctly does NOT mention its own distractors (`choukai-items.md` §問題3); gate confirms 0 named distractors. | — |
| 問題3-2番 | 3 | OK | 「施設の決まりに合わせていただくのではなく、その方のこれまでの暮らし方を…続けていただくことを大事にしています」. | — |
| 問題3-3番 | 3 | OK | 「初回のご相談は九十分に延ばして、その日は契約のお話を一切しないことにしました」. | — |
| 問題3-4番 | 1 | OK | 「故障を見つけるのが点検だと思われがちですが、私たちにとっては、運転の癖をお返しする場なんです」. | — |
| 問題3-5番 | 4 | OK | 「かけ湯をしていただき…」＋「お風呂に入る前と上がった後には、必ずお水かお茶を」. | — |
| 問題4-例 | 2 | OK | Request → acceptance with a deadline; announced 2番. | — |
| 問題4-1番 | 2 | OK | 「書き方がよく分からない…教えていただけませんか」→「こちらの記入例を見ながら書いてみてください」. 1 presupposes it is already filed; 3 answers a later step. Responder = counter staff, defined. | — |
| 問題4-2番 | 3 | OK | Thanks → 「困ったら、また声をかけてください」 from the helper. 2 reverses who thanks whom; 1 is a future-tense mismatch. | — |
| 問題4-3番 | 2 | OK | Suggestion → 「そうですね、印刷する前に直しておきます」. 1 over-reacts (deletes them); 3 goes the opposite way. | — |
| 問題4-4番 | 1 | OK | 「ご署名をお願いできますでしょうか」→「印鑑でも構いませんか。」 (indirect acceptance with a condition). 2 puts the clerk's job in the customer's mouth; 3 is a false premise. Keigo direction: 係員→客, reply plain-polite ✓. | — |
| 問題4-5番 | 2 | OK | 「とんでもないです。ちょうどお待ちしていました。」— presupposes only that a caller was expected (F12 fix holds). 1 asks a new question; 3 offers to reschedule. | — |
| 問題4-6番 | 3 | OK | 「写真撮影はご遠慮ください」→「あ、失礼しました。すぐにしまいます。」 1 contradicts the notice; 2 casts the customer as staff. Prompt has a defined addressee (お客様) — not an announcement. | — |
| 問題4-7番 | 2 | OK | 女(部下)→課長; 「助かった。夕方までに見て返すよ。」 plain form from the superior ✓. 1/3 are false premises. | — |
| 問題4-8番 | 2 | OK | 男→社長; 「ちょうど気になっていたところだ。」 ✓. 1 denies the report just made; 3 mistakes the period. | — |
| 問題4-9番 | 3 | OK | 「願ってもない」＝more than one could hope for; 「そう言っていただけると、こちらも助かります。」 1 reads it as regret, 2 as dissatisfaction — both are the standard misparse. Drawn idiom realized ✓. | — |
| 問題4-10番 | 3 | OK | 「間に合わせてほしいんだ」→「うちのプリンターで刷れば間に合います。」 1 misreads the fact; 2 puts it in the past. | — |
| 問題4-11番 | 1 | OK | 「顔を出せない?」→「三十分なら寄れると思う。」 2 takes 顔 literally; 3 answers a different question. | — |
| 問題5-1番 | 1 | OK | 「公園で、みんなでお昼を作って食べるっていうのはどう?」→「じゃあ、それでいこう」＋「公園を押さえておきますね」. 2「公民館、十月いっぱい耐震の工事」/3「八十代の方が途中で座り込んじゃって」/4「学校の行事と重なる時期」. | — |
| 問題5-2番 質問1 | 2 | OK | 「そうだな。消火器はこの前の秋にもやったし…救命講習にするよ。」 1 withdrawn by himself; 3「僕が入っても鍋を見てるだけになりそう」; 4「腰を痛めてるから、重い物を運ぶ方は無理」. | — |
| 問題5-2番 質問2 | 4 | OK | 「あ、確かに。名簿って、避難所で使うものだもんね。」→「じゃあ、避難所づくりにする。」 3 withdrawn (「去年やった」); 1「消火器は、重くて持ち上げられなかった」; 2「私は去年受けて修了証をもらってる」. Option order identical for 質問1/質問2 and equal to the spoken enumeration (消火器→救命→炊き出し→避難所) ✓; no deciding attribute printed beside an option name (nothing is printed at all — `jlpt-exam-structure` §"問題5 prints nothing"). | — |

**Narration ↔ voice:** every 聴解 speaker label resolves in `SPEAKER_MAP` with a
gender consistent with its narration (gate `聴解 narration gender matches
SPEAKER_MAP's voice`, `聴解 item speaker pairs cast distinguishable voices`).
「女の学生」/「女の講師」/「男の学生」 are all correctly cast. **This is a check of the
mapping table, not of the audio — see §Skips.**

## 4. Whole-paper & cross-test topic pass (step 5) and provenance (step 6)

### Headline theme set, built from the SHIPPED surfaces

| slot | 20260817_1 | 20260817_2 | **20260817_3** |
|---|---|---|---|
| 問題9 | 文化・伝統 | 科学・技術 | **消費・経済** |
| 問題12 | 地域活性化 | 旅行・観光 | **環境** |
| 問題13 | メディア・情報 | 働き方 | **医療・福祉** |
| 問題14 | 環境 | 教育 | **スポーツ・余暇** |
| 聴解問題5-1番 | 住まい | 食 | **人間関係** |
| 聴解問題5-2番 | 睡眠・健康 | 子育て・家族 | **防災** |

- vs `20260817_2` (immediately previous): intersection **∅** — rule 4's
  zero-tolerance clause satisfied.
- vs `20260817_1` (two papers back): intersection **{環境}**, exactly one —
  rule 4's at-most-one clause satisfied.

### Non-headline cross-test and in-paper checks

- **13 読解 surfaces, 13 distinct themes** (gate `no theme on two 読解 surfaces` ok).
- **No 読解 subject repeats `20260817_2`.** The closest pair is
  20260817_3 問題9 (実質値上げ／内容量削減) against 20260817_2 問題11(2)
  (円安による生活費上昇). Same theme tag, different subject and different
  mechanism; no rule binds a cloze's theme against a previous paper's
  non-headline surface. Recorded, not filed.
- **No two 聴解 items run the same errand** (gate `no two drawn surfaces share
  one errand key` ok, and I re-derived all 21 mappings by hand — every drawn
  scenario is used exactly once, none unused, no substitution).
- **問題14's flyer shares no decisive detail with any listening item** — its
  deciding cells are 申込締切 / 参加資格 / 同意書; nothing in 聴解 involves event
  registration.
- **Two clusters recorded, neither breaching a rule as written:**
  (a) three lodging surfaces paper-wide — 問題11(1) 農泊, 聴解問題2-例
  ビジネスホテル, 聴解問題2-5番 ホステル. The last two are inside one 大問 and are
  finding **R3-4**; 問題11(1) makes it a paper-level pattern.
  (b) three body/relaxation-service 聴解 scenes — 問題2-3番 美容院,
  問題3-3番 エステサロン, 問題3-5番 温泉施設 (all tagged スポーツ・余暇). Different
  errands, different 大問, so no rule fires; the tag is doing a lot of work.

### Closing-move column, read from each passage's last two sentences

問題9 意外な観察 / 10(1) 説明 / 10(2) 条件提示 / 10(3) 反論応答 / 10(4) 随筆 /
10(5) 主張 / 11(1) 随筆 / 11(2) 条件提示 / 11(3) 意外な観察 / 11(4) 主張 /
12 反論応答 / 13 説明 / 14 案内(掲示物).

**Six shapes at exactly 2 each over the 12 essay surfaces — none over the cap.**
I re-read all 13 and concur with the labels, with one honest note: 10(4)
(「私が今そう呼びたいのは…である」), 11(1) (「私の手はまだ覚えている」) and 11(3)
(「…と指を置く」) all end on a first-person or concrete-image gesture. The
*moves* differ (定義の置き換え / 感覚回帰 / 並置の観察) and the gate's three
sentence templates find no repeat, so this is at the boundary, not over it.
Recorded so a fourth occurrence is recognisable.

**Do the keys inherit a closing?** Four keys (55, 56, 58, 64) are the
"human/attitude" option against a technical alternative. The skill's bar is
**6+**; four is under it and each is independently forced by a quoted line.

### Provenance & spec audit (step 6)

1. **Target item match:** every 問題1–8 tested item and every 聴解問題4 stimulus
   resolves to its exact `test_spec.json` entry, and every entry resolves to
   `pools.json` (gate: `every recorded draw resolves to a pools.json entry
   (22 items)`, `問題1/2/4 test the items test_spec.json drew (21 targets)`).
   **One notation mismatch:** 問題3-11 realises `"内〜(国内)"` as the suffix 〜内
   — see R3-2. `listening_scenarios`: all **21** drawn entries mapped 1-to-1 to
   an authored item (問題1 ×6, 問題2 ×7, 問題3 ×6, 問題5 ×2), none unused, no
   substitution. `reading_topics`: all **12** mapped; 問題9 carries no drawn
   topic because the cloze is authored, which the spec and notes both state.
2. **Answer positions:** **101/101** match `answer_positions` exactly
   (`qa_eval.py` + gate). `answer_positions` is present and non-empty.
3. **Ledger ↔ spec:** identical field for field (seed, `generated_at`, all 11
   draw counts). No `harvest_sha` field exists, so no fabricated one.
4. **Copyright:** no imported paper exists on disk (`tests/imported-*` = none),
   so the imported-comparison half is vacuous — stated as a skip. Against
   `refs/`: 遠隔診療 / デジタルタトゥー / 農泊 / 本末転倒 each occur in **0** of
   the 31 archive `booklet.md` extracts; no passage, dialogue, 例, stem or
   option is a lift. Invented flavour detail is N2-simplified and unsourced
   (「二百二十円の手数料」, 「二か月後に一割以上落ち込んだ」, 「200件」) — no
   decimals, no citation of a real body.

## 5. Audit of the root-cause pass (nobody had reviewed it)

### 5a. Do the new gate checks test what their docstrings claim?

Twelve new/upgraded check functions, read line by line against their docstrings
and against the doc that owns each rule.

| Check | Verdict | Notes |
|---|---|---|
| `check_p7_stem_distribution` | **Sound** | Constants `(36,52) / 34 / 2 / 25` are byte-identical to `bunpou.md` §問題7's table. Measures exactly the three stated numbers. |
| `check_grammar_stem_lengths` (upgraded) | **Sound** | Extracts the 12 stems and feeds the distribution check; per-stem floor correctly demoted to WARN with the stated reason (a gate that fails an official paper is a wrong gate). |
| `check_dokkai_final_sentence_templates` | **Sound, under-scoped** | Three templates as documented, cap 2 as `dokkai.md` says. **But it reads 12 finals where `dokkai.md` counts 13 essay surfaces** — `passage_scopes(sec, 12)` returns 問題12 as ONE scope, so **問題12A's final sentence is never measured**. R3-8. |
| `check_mondai9_option_reuse` | **Sound; founding incident below its own threshold** | Half (b) (option = a drawn item of this paper) is exact. Half (a) uses `P9_SET_REUSE_MAX = 2`, i.e. it fires at **3+** shared options — but the docstring's own incident is *"recycled **two** options from the previous paper's 問題9-51"*, which the check would **not** catch. R3-9. On the coordination point I was asked about: it reads option strings from the previous papers' **booklets** (`p9_history`), not from any `logs/topics.json` schema. That is the right design — `topics.json` has no option field to read — and no doc claims otherwise. **No contradiction.** |
| `check_key_grammar_exposure` | **Sound; docstring overclaims** | The 連体 exemption is implemented correctly by matching the whole keyed string. **But the docstring's first line says "A form keyed in 問題7/8/9"** while the loop is `range(31,43) + P9_BLANKS` — **問題8 keys are not checked**. `exam-qa-review` §3 states the rule over 問題7/8/9. The printed check *name* says 問題7/9, so the gate output is honest and only the docstring and the skill are out of step. R3-7. |
| `check_pool_errand_keys` | **Sound** | Fails only a malformed `key`; the depth cost is a WARN, correctly framed as expected data rather than a defect. Matches `exam-blueprint` §`key` and `level_data.entry_key()`. |
| `check_spec_errand_rotation` | **Sound** | Resolves rotation through `errand_key()` before display strings, exactly as `exam-blueprint` R14 documents. `20260817_3` grandfathered — the knowingly-accepted decision; not re-litigated. |
| `check_moji4_option_set_level` | **Sound, deliberately narrow** | WARN-only, fires on four bare single-kanji nouns. The docstring says exactly that and does not claim to check level generally. |
| `check_choukai_elimination_tokens` | **Sound** | On the coordination point I was asked about: **the doc and the code agree exactly.** `choukai-items.md` §消去方法 says *"Scope today: 問題1. `check_choukai_elimination_tokens()` reads the 問題1 表 only"*, names the same nine tokens, the same 2-**row** cap, and the same four grandfathered ids as `ELIMINATION_VOCAB_GRANDFATHERED`. Separator handling (`／`, `、` accepted, parentheticals stripped first) matches too. **No contradiction.** |
| `check_choukai_setting_adjacency` | **Sound code, doc overstates enforcement** | Landed at **11:28 today, mid-review** — it is a 12th check, not one of the 11 I was told about. `choukai-items.md` §場面 ends *"`check_choukai_setting_adjacency()` reads this column and fails on a repeat"* with **no exemption clause**, while `SETTING_ADJACENCY_GRANDFATHERED = {"20260817_3"}` exempts the only paper that repeats. Compare §消去方法, which names its grandfathered ids in the doc. R3-4. |
| `check_choukai_closing_turn_shape` | **Sound** | Both halves measured on the last spoken line as documented; distractor-pointing tokens correctly reported without deciding. |
| `check_note_band` (upgraded context) | **Mis-named, and now behind its own doc** | The predicate (all of the term's kanji occur in the definition) is a defensible circularity heuristic. **But the WARN's name states the *passing* condition as if it were the failure** — 「（注N） definitions introduce words the term does not contain」 prints identically whether it passes or flags, so every reader has had to re-derive the criterion from the detail line. And `dokkai.md` §（注N） now carries a **strictly better, fully string-decidable** test (delete every character the headword contains; what remains must still identify the term) which the gate does not implement. Ten candidates over three papers; **ten judged false positives** by three independent reviewers. R3-10. |

### 5b. Do the skill-doc edits contradict the code?

Checked the coordination-sensitive pairs directly. **No contradiction found in
the two you named**, and none elsewhere except the two overstatements above:

| Doc | Code | Agree? |
|---|---|---|
| `bunpou.md` §問題7 table (36–52 / ≥2 under 34 / ≥25) | `P7_MEAN_BAND`, `P7_SHORT_MAX`, `P7_SHORT_MIN_COUNT`, `P7_SPREAD_MIN` | **exact** |
| `choukai-items.md` §消去方法 (9 tokens, 2-row cap, 問題1 only, 4 grandfathered ids) | `ELIMINATION_TOKENS`, `ELIMINATION_ROW_CAP`, scope, `ELIMINATION_VOCAB_GRANDFATHERED` | **exact** |
| `exam-blueprint` §`key` / R14 | `level_data.entry_key()`, `check_pool_errand_keys`, `check_spec_errand_rotation` | **exact** |
| `exam-qa-review` ground rules — five `topics.json` fields incl. `notes`, with the verifiability clause | (human rule, no code) — and the paper's `notes` complies | **consistent** |
| `moji-goi.md` §問題2 うんが example | the shipped 問題2-9 set 運河/運賀/雲河/雲賀 | **fixed; the file no longer teaches the うんかい-broken set** |
| `choukai-items.md` §場面 "fails on a repeat" | `SETTING_ADJACENCY_GRANDFATHERED = {20260817_3}` | **doc overstates** (R3-4) |
| `dokkai.md` §（注N） subtraction test | `check_note_band`'s all-kanji-present heuristic | **doc ahead of code** (R3-10) |

### 5c. Anything documented but not in fact implemented?

Round 2 filed seven root causes. I verified each landed:

| Round-2 RC | Implemented? | Evidence |
|---|---|---|
| N5 → `check_p7_stem_distribution` + `bunpou.md` numbers | **Yes** | Both, with matching constants. |
| N4 → `qa_eval.py` stops parsing at the 構成表 / rejects keys outside 1–4 | **Yes** | `tools/qa_eval.py` +113 lines; it now reports `Total Scored Items : 101`, not the phantom 106. |
| N2 → closed-vocabulary gate + "re-derive from the NEW line" sentence | **Yes** | Both. |
| N3 → five-field rule incl. `notes` verifiability | **Yes** | `exam-qa-review/SKILL.md` ground rules, with this paper's two stale notes named as the incident. |
| N6 → `dokkai.md` subtraction test | **Yes (doc)** — not gated | R3-10. |
| N7 → `setting` adjacency | **Yes, but as a 構成表 check, not a sampler field** | The implementation is *better* than proposed (the 大問 assignment only exists in the 構成表, which the docstring explains) — but the paper was then exempted from it. R3-4. |
| F15 → widen the already-done token list; concentration bound | **Yes — and the widened rule now fails this paper** | `choukai-items.md` line 428 now lists もう/すでに/さっき/先ほど/今しがた/たった今 and states 「`20260817_3` shipped three」. The cap is still ≤2. **R3-5.** |

Round-1 RCs also verified as landed: `verify_scramble.py` rewritten (+105),
`moji-goi.md`'s うんが example corrected, "one grammar point one key" converted
to a number and gated, `check_choukai_key_paraphrase` context extended.

**One thing is documented that is not implemented, and it matters:** nothing
anywhere validates 問題2's option glyphs against 常用漢字, although
`moji-goi.md` §問題2 states the requirement in bold. That is how R3-1 shipped
through three rounds.

## 6. Findings

### Paper findings

| # | Item | Class | Severity | Evidence | Fix |
|---|---|---|---|---|---|
| **R3-1** | 問題2-8 | Off-level key / banned glyph | **自動不合格** | `言語知識・読解.md:27` — options `基金 / 飢金 / 飢饉 / 基饉`, key `飢饉`. **`饉` is not a 常用漢字** and is outside the N2 kanji scope; `飢` is itself N1-band. `飢` occurs **0 times in every extract of all 31 official sittings** in `refs/JLPT_N2_NEW/` (booklet.md, script.md and key.md alike — `grep -rc 飢 refs/JLPT_N2_NEW/*/*.md` returns no non-zero line). `moji-goi.md` §問題2 is explicit: *"Every constituent kanji glyph must be a legitimate, standard 常用/N2 kanji"*. The paper's own 解説 is the confession: rows 6, 7, 9 and 10 each end 「四字とも常用漢字」; row 8 alone omits it. | The defect is the **pool entry**, not the sentence. Delete `"飢饉"` from `pools.json` `orthography` (line 1742) and re-draw with `sample_items.py --reroll orthography` — never hand-substitute a target (`exam-blueprint` rotation model). Then rebuild 問題2, `make check`, re-review 問題2 in full. |
| **R3-2** | 問題3-11 / `pools.json` | Spec ↔ pool notation mismatch | Minor | Drawn target is `"内〜(国内)"` — notated as a **prefix**, but its own example `国内` is a **suffix** use, and the item tests the suffix (`建物内`; the 解説 calls it 「接尾語」). The item is right and the pool string is self-contradictory. No gate reads 問題3 word-formation targets at all. | Change the pool entry to `"〜内(国内)"`. No paper edit. Optionally add a check that a `word_formation` entry's `〜` position matches its example. |
| **R3-4** | 聴解問題2 例 / 5番 | Repeated establishment type in one 大問 | Minor | 例 = 「ビジネスホテルのフロント」, 5番 = 「ホステルの受付」 — one 宿泊施設 twice in six items, the 例 heard immediately before. `choukai-items.md` §場面 now **forbids this in prose** and says the check *"fails on a repeat"*, but `SETTING_ADJACENCY_GRANDFATHERED = {"20260817_3"}` exempts precisely this paper, so the gate WARNs. Paper-wide this is the third lodging surface (問題11(1) 農泊). Round 2 recorded it as an observation because no rule existed; **a rule now exists.** | Re-angle **one** of the two — the 例 is unscored and cheapest to move (e.g. a 空港カウンター or a レンタカー営業所 for the extra-night reason), or move 5番's checkout to a different establishment. `--reroll listening_scenarios` is the wrong instrument (it re-draws all 21). Script + MP3 regeneration required. If instead the decision is to accept it, the honest form is to **say so in `choukai-items.md`**, not to carry a by-name exemption in the gate while the doc says it fails. |
| **R3-5** | 聴解問題4 1番/3番/4番 | Already-done distractor shape over cap | Minor | Three of eleven scored items carry it: 1番「その申請書は**もう**受け付けました」, 3番「数字は**もう**全部消しときました」, 4番「その書類は**先ほど**郵便で送りました」. `choukai-items.md` line 428 (rewritten in this very fix round, as round 2's F15 asked) now defines the shape by **shape**, lists 先ほど explicitly, states 「`20260817_3` shipped three」, and holds the cap at **≤2**. The paper therefore now breaches a binding rule in the owning reference. I re-checked the two *new* bounds and both pass: no distractor shape exceeds 40 % of the 22 scored distractors (max ≈4), and no two items share both of their distractor shapes. | Rewrite ONE of the three distractors onto a different shape — 3番 opt 1 is the cheapest (「数字はもう全部消しときました」 → e.g. 「印刷は先週の分で終わっています」 is still already-done; use instead an inverted-polarity or wrong-addressee reply). Script + MP3 regeneration required. **Alternative, equally legitimate:** amend the cap to ≤3 with a written reason — `choukai-items.md`'s own archive column records the official band as *median 1, max 3 of 11.4*, so 3 is inside what official ships. **I am not authorised to make that call and am not making it**; as the rule reads today, this is a finding. |

### Root-cause-pass / process findings (do not concern the paper's content)

| # | Class | Severity | Evidence | Fix |
|---|---|---|---|---|
| **R3-3** | Stale grandfather entry | Minor | `20260817_3` is still listed in `P7_DISTRIBUTION_GRANDFATHERED` although its 問題7 now passes on merit (mean 46.2, 3 under 34, spread 29). A future regression in this paper's 問題7 would print WARN, not FAIL. | Delete `"20260817_3"` from `P7_DISTRIBUTION_GRANDFATHERED` — the comment beside the set already prescribes exactly this ("Delete an id when that paper's 問題7 is recompressed"). |
| **R3-6** | Process — next run started before QA closed | **Moderate** | `tests/20260818_1/test_spec.json` + `logs/ledger.json` written at **11:31:38**, i.e. `make sample` for the next paper, **during** this round and before any verdict. `exam-qa-review` §6.5: open root-cause findings **block the next generation run**. It also broke the gate: `make check` now exits 2 on `FAIL both Markdown sources present`. | Hold `20260818_1` until this report's findings are applied or explicitly rejected. Add to `jlpt-test-generation`: *"`make sample <next>` may not run while any test's QA is open — the ledger it writes is the same file the open review is auditing."* Also consider making `check_test_contracts` `skip` rather than `FAIL` a blueprint-only folder, so an in-flight sample cannot red the gate for every other paper. |
| **R3-7** | Docstring overclaims scope | Minor | `check_key_grammar_exposure`'s docstring headline says 問題**7/8/9**; the loop covers 問題7 + 問題9 only. `exam-qa-review` §3 states the rule over 問題7/8/9. | Either extend the loop with the 問題8 keyed cards, or correct the docstring **and** add the exclusion to `exam-qa-review` §3 so QA knows 問題8 is still hand-work. Prefer the former. |
| **R3-8** | Check under-scoped vs its own rule | Minor | `check_dokkai_final_sentence_templates` reads **12** finals; `dokkai.md` counts **13** essay surfaces. 問題12 is one scope, so **問題12A's closing sentence is never measured** — and 問題12 is exactly where two closings sit side by side. | Split 問題12 into A and B scopes (`^\*\*A\*\*` / `^\*\*B\*\*`) before taking the final sentence; the cap and templates need no change. |
| **R3-9** | Founding incident below the check's own threshold | Minor | `check_mondai9_option_reuse`'s docstring cites *"recycled **two** options from the previous paper's 問題9-51"*, but `P9_SET_REUSE_MAX = 2` fires only at 3+. The check as built would not have caught the incident it was written for. | Either lower the threshold to 1 shared option for **non-connective** blanks (the docstring already argues 論理接続 is a small class and must stay loose), or correct the docstring to cite the incidents the check actually catches (20260814_1's 4/4, 20260817_2's 3/4). |
| **R3-10** | `GATE-WRONG`: mis-named warn + doc ahead of code | Minor | `check_note_band`'s warn name — 「（注N） definitions introduce words the term does not contain」 — states the **passing** condition and prints identically on pass and on flag. Ten candidates across `20260817_1/2/3`; **ten** judged false positives by three independent reviewers. Meanwhile `dokkai.md` §（注N） now carries a fully string-decidable subtraction test the gate does not run. | Rename to 「（注N） definition is not the headword's own kanji restated」, and replace the predicate with `dokkai.md`'s test: strip from the definition every character occurring in the headword; **FAIL when what remains carries no predicate** (no 用言) — that is decidable and would have flagged the old 菜っ葉 gloss while clearing all ten current candidates. |

**Findings: 8 open (4 on the paper, 4 on the gate/process), of which 1 is an
automatic fail.** R3-3 and R3-6 are counted in the process half.

## 7. Root-cause table (step 6.5)

Recurrence measured from the papers on disk, not judged.

| Finding | Code | Tests showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|
| **R3-1** (問題2 non-常用 glyph) | `GATE-BLIND` (+ pool data defect) | **1 of 12** at this severity, but the *class* — no gate has ever read a 問題1–6 key's level or a 問題2 option's glyph inventory — covers **12 of 12**. `exam-qa-review` §2.5 says so in as many words: *"no gate has ever checked a 問題1–6 key"*. | `tools/check_consistency.py` + `.agents/exam-blueprint/references/pools.json` | Add `check_moji2_option_glyphs()`: every kanji in every 問題2 option must be in the 常用漢字表. The list is 2136 characters, ships as a data file, needs no corpus and no judgement — this is precisely the *string-decidable* case §6.5 says to gate. Extend the same list to 問題1's printed targets. Then delete `"飢饉"` from `pools.json` `orthography`, and add to `exam-blueprint` §pool hygiene: *"an `orthography` entry containing a 表外漢字 is a pool defect — delete and re-draw, never patch the sentence"* (the rule already exists for 問題1's 表外音訓; extend it one line). |
| **R3-2** (`内〜` notation) | `GATE-BLIND` | 1 of 12 verified; I did not sweep the other 11's `word_formation` draws. | `pools.json` + `tools/check_consistency.py` | Fix the entry to `"〜内(国内)"`. Add a one-line check: for each `word_formation` entry `X〜(例)` the example must **start** with X, and for `〜X(例)` it must **end** with X. |
| **R3-4** (lodging twice in 問題2) | `RULE-IGNORED` at the paper level; `GATE-WRONG` at the exemption level | 1 of 12 (the check clears the other 11). | `.agents/question-authoring/references/choukai-items.md` §場面 | The rule and the code disagree about whether this paper is bound. Pick one and write it down: either repair the paper and delete the grandfather entry, or add to §場面 the same by-name exemption paragraph §消去方法 already carries. **A doc that says "fails" beside a gate that warns is the shape `exam-qa-review` §6.5 calls the most dangerous — green stops being evidence.** |
| **R3-5** (already-done ×3) | `RULE-UNENFORCEABLE` → now `GATE-BLIND` | The rule's own incident band is 9/11 and 8/11 on earlier papers; this paper is at 3/11. Systemic by the recurrence test. | `.agents/question-authoring/references/choukai-items.md` + `tools/check_consistency.py` | The cap was just rewritten as a *shape* count precisely because a token list under-counts — which makes it un-greppable again. Gate the token list as a **lower bound** (`もう/すでに/さっき/先ほど/今しがた/たった今 + 〜た` in a 問題4 distractor, count items, FAIL over the cap) and keep the shape column as the human half. Also reconcile the cap with the archive column in the same file (≤2 vs *max 3 of 11.4*) — one of the two numbers is wrong, and the paper is sitting in the gap between them. |
| **R3-6** (next run started mid-QA) | `PIPELINE-GAP` | 1 observed, and it is the first round where a fix pass and a QA pass have overlapped in one working tree. | `.agents/jlpt-test-generation/SKILL.md` + `tools/check_consistency.py` | Stage rule: no `make sample` for test *n+1* while test *n*'s QA is open. Gate: `skip`, not `FAIL`, a test folder that has `test_spec.json` and no Markdown — that state is a legitimate mid-pipeline moment and should not red the gate for eleven finished papers. |
| **R3-7 / R3-8 / R3-9** | `GATE-WRONG` (three instances, one cause) | All three landed in the same 2026-08-19 pass. | `tools/check_consistency.py` | One cause: **each check was written from the incident narrative and never re-read against the rule text it cites.** Add to `exam-qa-review` §6.5: *"A new gate check must be run against the incident that motivated it before it is committed — a check that would not have caught its own founding case is not evidence."* Then apply the three specific edits in §6. |
| **R3-10** (`check_note_band`) | `GATE-WRONG` | 3 of 12 papers produce candidates; **10 of 10 candidates were false positives**. | `tools/check_consistency.py` + `.agents/question-authoring/references/dokkai.md` | Rename the warn to state the failure, and implement `dokkai.md`'s subtraction test in place of the all-kanji-present heuristic. A warn whose entire history is false positives trains reviewers to skip warns — which is the failure mode `AGENTS.md` §0.5 exists to prevent. |
| **R3-3** | `GATE-WRONG` (self-inflicted) | 1. | `tools/check_consistency.py` | Delete `"20260817_3"` from `P7_DISTRIBUTION_GRANDFATHERED`, per the set's own comment. |

**Effect on the loop:** R3-1 blocks this paper. R3-2/4/5 must be applied or
explicitly rejected before it ships. R3-3/6/7/8/9/10 do not block the paper but
**block the next generation run** (`exam-qa-review` §6.5) — and one of them,
R3-6, is that a next generation run has already begun.

## 8. Coverage statement

| Step | Ran on | Result |
|---|---|---|
| 0 Blind solve | `qa/20260817_3/keyless.md` (rebuilt at round start) | **101/101**, 0 discrepancies |
| 1 Key-by-key proof | all 101 | every row in §3 carries the deciding line |
| 2 Distractor elimination | all 101 | one impossibility statement per wrong option; no "the key fits slightly better" |
| 2b Distractor plausibility | 問題1–6, 聴解問題1–3 | option sets share one functional category throughout; no free elimination |
| 2.5 Level band | 問題1–9 keys by hand, 問題7–9 also by gate | **one failure: 問題2-8 (R3-1)** |
| 3 Mechanical reads | 問題7 distribution, 問題8/9 length, 読解 apparatus & key predictability, 問題2 2×2 grids, 問題3 affixes, 問題4 blanks, 問題5 swap test, 問題8 splice, 問題9 categories, one-key-one-point | all measured, numbers printed above |
| 4 聴解 structure | 構成表 as columns, verified against the script; first/last lines as a column; grounding of every 問題1–3 distractor; 例 answerability; keigo direction; SPEAKER_MAP | **one failure: R3-5**; **one rule-vs-gate conflict: R3-4** |
| 5 Topic table | 47 surfaces × 3 tests | headline set clean vs both predecessors; 2 clusters recorded |
| 6 Provenance | spec ↔ pools ↔ ledger ↔ paper, 101 answer positions | clean except R3-2's notation mismatch |
| 6.5 Root cause | 8 findings + the audit of the root-cause pass itself | §5, §7 |

### Artifact freshness

`聴解.mp3` (11:17) and `聴解_チャプター.json` (11:17) postdate
`聴解スクリプト.txt` (10:43); the chapter file's `script_sha` `61333cbd3e88`
equals the shipped script's sha1 prefix; `pacing_sha` matches. Both HTML
booklets (11:16) postdate their Markdown (10:45 / 11:16) and the gate confirms
`built HTML matches the Markdown it stamps`. **No stale artifact.**

### Source stillness

Start-of-round and end-of-round sha1s are identical for all three sources
(`cc08ccb1…` / `c9d70682…` / `61333cbd…`). The review is valid. *Other* files in
the tree did move — see the "gate moved during this review" box and R3-6.

### Every `make check` WARN, resolved

Run 2 (11:32) reports 112 warnings; **three** name `20260817_3`, plus one
repo-level pool warning that names no test.

| WARN | Resolution |
|---|---|
| `no drawn errand repeats inside its own cooldown window` — 引っ越し業者:見積もり / カルチャースクール:受講申し込み / クリーニング店:仕上がり日 | **Real, and knowingly accepted** by the user, who was shown the re-draw-all-21 trade-off. Reviewed the re-angle on its merits: 聴解問題2-1番 moves speaker relation (colleagues in a break room, no vendor present), register (くだけた), question class (理由型 ポイント理解 vs 課題理解) and tense (post-quote explanation) — four independent axes, and the deciding content (four floors, no lift, two extra crew) shares nothing with a moving quote's usual material. **The re-angle is sound.** Not re-litigated. `logs/topics.json` `notes` records the debt for the next blueprint stage, correctly. |
| `（注N） definitions introduce words the term does not contain` — 7 candidates | **False positives, all seven** — derived independently with `dokkai.md`'s subtraction test: 農泊→「家にまり、その土地の暮らしや仕事に触れる旅行の形」; 菜っ葉→「ほうれん草や小松菜など、の部分を食べる野」; 管理組合→「分譲された集合住宅の所有者全員でつくり、建物の維持を行う織」; 離島→「本土から遠くれ、船や飛行機でしか行き来できない」; 血糖→「液の中に含まれるぶどう」; 触診→「体に手をれて状態を確かめるの方法」; 初診→「その病気について、その医療機関で最初に受ける察」. Every one leaves a predicate and a mechanism. Concurring with rounds 1 and 2, reached independently. **Because the check has now produced ten candidates and ten false positives, this is filed as `GATE-WRONG` R3-10.** |
| `no two 聴解 items of one 大問 share an establishment type` | **Real.** Filed as **R3-4**. |
| `pools.json errand-key clusters cost 21 entries of effective pool depth` (repo-level) | Expected by design — the check's own text says a shared `key` is correct data and the duplicates cannot be deleted because shipped ledger entries name them. Resolve by growing the pool. Not a defect of this paper. |

### Gate FAIL

`make check` exits **2**, on one line: `FAIL both Markdown sources present —
missing ['言語知識・読解.md', '聴解.md']` for `tests/20260818_1`. **Not this
paper.** Filed as R3-6.

## 9. Skips — stated explicitly

1. **`聴解.mp3` has never been listened to — by me or by anyone, across all
   three rounds.** I have no audio playback in this context. **Prosody, pitch
   accent, intonation, whether Edge-TTS renders 「飢饉」「六畳／八畳」「不在連絡票」
   「本末転倒」「稜線」 correctly, whether the voiced speaker attribution matches
   the narration by ear, whether the re-synthesised 例 block sounds like its
   neighbours, and whether the answer pauses land where `聴解_チャプター.json`
   says — are ALL UNVERIFIED.** What I verified is mechanical only: `script_sha`
   `61333cbd3e88` = the shipped script's sha, `pacing_sha` matches, MP3 mtime
   11:17 postdates the script's 10:43, duration 2752.95 s (45.9 min), every
   speaker label resolves in `SPEAKER_MAP` with a gender consistent with its
   narration, and no scored item contains an answer reveal. **A human must
   listen end to end before this paper is served.** This is the single largest
   unverified surface in the paper and it has now survived three QA rounds.
2. **`refs/Shinkanzen/*.pdf` and `refs/Soumatome/*.pdf` were not read.** Both
   are scanned images with no text layer; locating 飢饉 would mean rendering
   ~200 pages by eye. R3-1 therefore rests on three other grounds — 饉 is not a
   常用漢字, `飢` appears in **0 of 31** official sittings, and `moji-goi.md`'s
   bold glyph rule — not on a textbook lookup. If a Shinkanzen/Soumatome N2
   volume does headline 飢饉, that is an argument about the *pool*, and it
   should be recorded in the pool entry, not left for a fourth reviewer to
   re-derive.
3. **`tests/imported-*` comparison is vacuous** — no imported paper exists on
   disk. The `refs/` half of the copyright check ran.
4. **I did not sweep the other 11 papers' `word_formation` draws** for the R3-2
   notation defect; the recurrence count for that row is "1 verified", not
   "1 total".
5. **`make model-answer` was not run and `詳細解説.json` does not exist** — by
   instruction, and correctly: the model answer is the final step after PASS,
   and the gate `skip`s that check accordingly.
6. **I did not re-run `make lint-draft` / `make verify-scramble` / `make irt`.**
   `make check` covers the contracts they feed; 問題8 uniqueness was proved by
   hand enumeration in §3 rather than by `verify_scramble.py`, whose round-1
   defect (uniform `RESULT: WARNING`) I did not re-test.
7. **I did not fix anything.** No source file, skill, gate or pool was edited by
   this review.

## 10. Verdict

`QA: FAIL (8 findings, 1 automatic)`

- **Automatic:** R3-1 — 問題2-8's key and one distractor are built on `饉`, a
  非常用 glyph outside the N2 kanji scope, against `moji-goi.md`'s explicit
  bold rule and with zero precedent in 31 official sittings.
- **Paper, non-automatic:** R3-2 (pool notation), R3-4 (two lodging counters in
  one 大問, now forbidden by the doc and exempted by the gate), R3-5 (three
  already-done 問題4 distractors against the cap the fix round itself just
  rewrote).
- **Gate / process:** R3-3, R3-6, R3-7, R3-8, R3-9, R3-10 — none blocks the
  paper; all block the next generation run, and one of them is that the next
  generation run has already started.

The blind solve was **101/101** and every key is provably the single defensible
answer. Round 2's N2/N3/N5/N6 are **all four closed**, and round 1's F1–F15 show
**no regression**. This paper is much closer than the verdict line suggests —
but three of the four paper findings exist *because the fix round tightened the
rules and did not then re-measure this paper against them*, and the fourth has
been sitting in the pool since before round 1.

