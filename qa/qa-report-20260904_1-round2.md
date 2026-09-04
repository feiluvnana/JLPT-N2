# QA report — 20260904_1 (adversarial pass, ROUND 2 — delta audit)

**Reviewed revision** (sha1[:12] over raw bytes):

| file | round 1 reviewed | round 2 reviewed (this pass) | moved? |
|---|---|---|---|
| `tests/20260904_1/言語知識・読解.md` | `7a0c60a0b6e3` | **`d963c3b152e1`** | yes |
| `tests/20260904_1/聴解.md` | `d1e35a786abe` | **`c61b7b069fdf`** | yes |
| `tests/20260904_1/聴解スクリプト.txt` | `9ee49e4307ea` | **`b3d6c423e293`** | yes |
| `tests/20260904_1/聴解.mp3` | duration 2779.17 s | sha256 `4bd812cb761adc21…`, 33,410,061 bytes, duration 2784.11 s, 38 chapters | yes |
| `tests/20260904_1/聴解_チャプター.json` | `script_sha 9ee49e4307ea` | `script_sha` **`b3d6c423e293`** = current script sha1[:12] | in sync |

All three text sources moved, so this is a strictly later revision on every file.
The MP3's sha256 equals `logs/upload_manifest.json`'s `audio/20260904_1.mp3`
fingerprint byte for byte (33,410,061 bytes), i.e. the audio on the `audio`
release is this revision's audio.

**Source mtimes checked at the start of the pass and again before writing:
unchanged** (12:57:58 / 12:43:51 / 12:37:06). No other context moved underneath
this review. **I edited nothing** — not the paper, not `.agents/`, not the gate.

**Timestamp:** 2026-09-04. **Reviewer:** fresh-eyes context. I authored nothing in
this paper, did not write round 1's report, and applied none of its repairs.
**Round 1 verdict:** `QA: FAIL (7 findings, 1 automatic)`.
**Entry condition:** `make check` exit 0 — 0 FAIL / 282 WARN / 120 skipped.
**Loop position:** round 2 of a maximum of two fresh-eyes rounds.

---

## 1. Verdict

**QA: FAIL (3 findings, 1 automatic)**

All seven round-1 repairs are verified correct on disk and none of them is a
re-label. Provenance, ledger, seed, audio freshness and the whole blast radius of
option/stem/解説/record edits check out. The three findings are:

| # | item | class | why it is open |
|---|---|---|---|
| **F1** | 問題5-24 | **自動不合格** | Off-level key (`いつも`, N5-core) on an option set whose three distractors are mutual synonyms — the live `check_goi_option_set_valence` WARN is a **true positive**, and it is the same defect class as round 1's F1, one 大問 later |
| **F2** | 問題12(B) / 問題13 closings | 要修正 | Round 1's F2 ordered this exact pair split. It cleared the 分裂文 skeleton but landed **both** on 「〜ていた＋のだ／のです」 **and** both on the shape label 意外な観察 — the pair is re-clothed, not split |
| **F3** | 問題11(3) （注3）便 | 要修正 | The F3 repair's new gloss hands item 61 six characters of its own key, on a stem anchored on the glossed word. Measured: the only such hit in 29 papers; 0 in 8 official sittings |

F2 and F3 are both **repair collateral** — defects that did not exist before the
round-1 fixes. That is precisely the failure mode round 2 exists to catch, and it
is the third paper on record to show it (`20260812_1` F2→F3, `20260903_1` F2, now
this).

Findings are ≤3, so per `jlpt-test-generation`'s stage-4 loop rule they may be
fixed directly. **Every finding below is written to be applied exactly as
stated.** Read §4's "Repairs, appliable as written" and the two verification
obligations attached to each — F2 in particular cannot be verified by `make
check` (§4).

---

## 2. Blind-solve scope and honesty statement

**Keyless render rebuilt at the end of this pass:** `qa/20260904_1/keyless.md`,
1031 lines, over the reviewed revision. It carries no key, no key table, no
marked grid, no 解説.

Round 1 blind-solved 101/101 from this render with zero discrepancies. This is a
delta audit, so I solved the delta rather than re-deriving the paper. **Being
exact about which items were blind:**

- **Solved from booklet text before opening any key table** (booklet region read
  first, key tables read afterwards): 問題4 (14–20), 問題5 (21–25),
  問題10 (52–56), 問題11 (57–64), 問題12 (65–66), 問題13 (67–69),
  問題14 (70–71), 聴解問題3 (例, 1–5番), 聴解問題5 (1番, 2番質問1/質問2).
  **All 36 match the shipped keys. Zero discrepancies, zero second defensible
  answers** — with the single exception recorded as F1, where the item is
  answerable without the tested knowledge rather than ambiguous.
- **NOT blind — verified as step-1 key proofs, not solves:** 問題8 (43–47) and
  the 聴解問題1/2 rows. I had read `test_spec.json` (which carries
  `answer_positions`) before reaching them. Stated per AGENTS.md §0.7; round 1's
  clean 101/101 blind solve stands as the blind evidence for these.

### Blind STRATEGY passes, re-run on the shipped revision (§0, required)

The 読解 prose, four options (58-2, 58-4, 64-4, 71-3) and one stem (67) all
moved since round 1, so these were recomputed, not carried over.

| strategy | round 1 | **round 2** | official | bar |
|---|---|---|---|---|
| second-longest option (問題10–13, 18 items) | 22.2 % | **22.2 % (4/18)** | 24.6 % | fail > 45 % |
| key is (tied-)longest | 22.2 % | **22.2 % (4/18)** | 30 % | ≤ 35 % |
| key is **uniquely** longest | 16.7 % | **16.7 % (3/18)** | 20 % | ≤ 30 % |
| median key−best-distractor bigram margin | −0.149 | **−0.158** (gate) | — | fail > 0 |
| strict top-overlap key share | — | **30 %** (gate) | 35 % | ≤ 50 %, WARN > 44 % |

All inside band, and the margin moved further into the safe direction. No
strategy pass regressed. Per-item option-length ratio: worst 1.36 at item 63,
inside `dokkai.md`'s WARN 1.65 / FAIL 2.50 (gate `ok` on both lines).

---

## 3. Per-repair walkthrough — the seven round-1 repairs, verified on disk

### F1 — 問題4-18, re-drawn on 乏しい ✅ CORRECT

`test_spec.json` `context_words[4]` = `乏しい`; seed string
`51231849+reroll-one(context_words:4,1788492579)+…`; `logs/ledger.json`'s
`items` dict compares `==` to the spec's, seed and `pools_sha eff0114aaa1a`
identical. **A sampler re-draw, not a hand substitution.**

Shipped item: 「山小屋に着いたときには手持ちの食料が（　）、翌朝の分しか残っていな
かった。」 / 浅く・**乏しく**・薄く・細く, key at the prescribed slot 2.
`殺` now occurs **0 times** in all three sources; `ふるまい` 0 times.

**Band, verified independently against the archive** (§3 requires a re-drawn key's
band be a named QA question): 乏しい is a 問題1 target in official **7/2015 item 5**
(「この世代の人たちはコンピュータの知識が乏しいように思います。」) and **12/2021 item 2**,
and occurs in 5 of the 31 booklets. N2 band confirmed. I did not open the Shin
Kanzen PDF the 解説 also cites (§7).

**Option set judged, not just the key:** the three distractors are *not* mutual
synonyms — 浅い(depth) / 薄い(thickness·concentration) / 細い(width) are three
different axes, each killed by its own sentence in the 解説, and 「食が細い」 makes
細く a designed trap rather than filler. This is the same one-semantic-field shape
official uses (12/2023 問題5: 上を向いて／横を向いて／下を向いて／後ろを向いて). **Not
the F1 class.** Contrast F1 below, where the three distractors mean the same thing.

### F5 — 問題8-46, re-drawn on 理由説明(〜のは…からだ) ✅ CORRECT

`grammar_p8[3]` = `理由説明(〜のは…からだ)`; seed carries
`+reroll-one(grammar_p8:3,1788492587)`. 問題8-46 ships
毎朝の(1) / かえって時間がかかる(2) / と気づいたからだ(3) / 電車通学をやめたのは(4).

Assembled: 「今年の春から一人で暮らし始めた妹が、毎朝の → 電車通学をやめたのは →
かえって時間がかかる → と気づいたからだ。」 ★ (3rd slot) = card **2**, the prescribed
position. Uniqueness proved per card, final card tested as a binding host
(`20260827_2` 問題8-47 precedent): 「毎朝の」 demands a noun and only card 4 starts
with one; 「と気づいたからだ」 demands a plain-form quotative and only card 2 supplies
one; 「〜のは」 is closed by 「からだ」 at the sentence end. One free pre-predicate
unit. No bare adverb card (gate `ok`).

The family collision is gone: the gate's new `check_p8_form_family` reports
`ok … (1 keyed entr(ies))` — one 「つつ」-family member remains, which is the
correct post-repair state.

### F2 — the five 分裂文 closings ⚠️ HALF-CORRECT → **finding F2**

Re-measured with the gate's own `dokkai_closing_scopes()` /
`passage_final_sentence()` over all 13 closings: the 分裂文 pattern
`(の|ん)は、?[^。]{2,60}(だ|である|…)$` now matches **0 of 13** (was 5). No
`FINAL_SENTENCE_TEMPLATES` row exceeds 1 hit (only 問題10(2) matches anything, on
「こそが」). That half is correct and was verified by reading, not by trusting the
note.

**But round 1's F2 repair instruction was 「最低限、問題12(B) と 問題13 の対を割る
こと」 and the pair is still one pair.** See finding F2 in §4.

### F3 — the seven padded （注N） glosses ✅ CORRECT (one leak, see F3 finding)

The seven struck words carry **no （注N） line** anywhere in the paper, and 抽選 /
一括 now appear as bare prose. Independently re-measured against
`refs/JLPT_N2_NEW/*/booklet.md` (definition lines dropped):

| struck word | official booklets printing it bare |
|---|---|
| 抽選 6 · 一括 3 · 視察 3 · ふるまい 2 · 当選 1 · 排除 1 · 当番 1 | reproduces round 1's F3 measurement exactly |

The **30 replacement/kept glosses measure 0 official bare uses**, with a single
exception: 便 (6 booklets contain a standalone 便, of which **2 are the
scheduled-service sense** — 「明日の飛行機は早期の便だから」 7/2023, 「飛行機の便を変える」
12/2013). That is *stricter* than official's own practice, which glosses
一切／そもそも／類／進化／概念 — words other sittings print bare 5, 7, 11, 5 and 2
times. The count is honest, not padded: **30 in-body markers / 30 definition lines
/ 0 orphans**, 問題13 lengthened rather than glosses cut (gate: floor 800 ✓,
ceiling 1070 ✓, all five section lengths inside band).

### F4 — 聴解問題3-5番 re-angled ✅ CORRECT

New talk (ラジオ), new key at the prescribed slot 1: 「質問を送る人が求めているもの」.
Deciding line, verbatim in the script: 「番組あてに書いてくださる方は、正しい答えが
ほしくて書いているとはかぎらないんですね。自分と同じことを考えている人がどこかにいる
と知りたくて、ペンを取ってくださるんです。」 解説 quotes both sentences verbatim.

**I read the 24 spoken options as a column by hand, not on the gate's word.**
「そのまま」 now occurs in **1** of 24 (3-1番's key). No content token of ≥2 chars
occurs in two or more options with every occurrence on a key: 問い合わせ (2, both
distractors), 使い方 (2, both distractors), わけ (2, both distractors), 言葉 (2,
one key one distractor), こと (4, mixed). Signature gone.

**The narrative-arc half also cleared.** 3-1番 is an instruction with an
illustrative example and no before/after on the speaker; 3-5番 is a dated
conversion narrative (去年の夏) with a measured outcome and a changed practice,
and its key is about what the *audience* wants, not about not-processing input.
Residual: 3-3番 and 3-5番 share the abstract moral "what the other party wants is
not the finished product", on unrelated domains with zero shared option lexis —
a family resemblance, **not** the F4 class, which needs a token shared by two
options that are both keys. Recorded, not filed.

Provenance recorded correctly: `listening_scenarios[12]` carries
`"origin": "reauthored"` **and** a `"note"` that **quotes** the deciding line and
names the new key — the three things §"A fix that changes WHAT a surface tests"
requires. `logs/topics.json`'s `surfaces` / `claim` / `shapes` for 3-5番 all match
the shipped script.

### F6 — 問題14-71 option 3 ✅ CORRECT

Options are now 四百円 / 五百円 / 千円 / 九百円 — four bare amounts, key 4. The
arithmetic holds on two constraints (①500円 + ②500円 at 二割引 = 400円 → 900円),
each distractor is a real mis-combination (vegetables only / fee only / no
discount), and the discount constraint is no longer leaked by an option.

### F7 — 聴解問題2-4番 構成表 cell ✅ CORRECT, and the gate that now reads it works

The cell reads 「走っても六時ちょうどなんですよね。毎日、間に合うかな」, byte-matching
`聴解スクリプト.txt` line 171. The 解説 cell for the same item was re-derived to the
same wording.

**I ran the new `check_section_table_quotes` against its own founding case**
(§6.5's requirement), by feeding the predicate the pre-repair cell string:

```
== PRE-REPAIR   WARN  … not found in the source: ['走っても六時ちょうど。毎日、間に合うかな']
== SHIPPED      ok    … セクション構成表 cell quotes trace to the passage/script
```

It catches the incident it was written for and is silent on the shipped text.

### The blast radius the fixes moved — all re-derived

| moved artifact | verdict |
|---|---|
| **58-2** 「棚が空になる日は、その日に運ばれてくる血液の量が減っているということ」 | OK. Killed by 「月ごとの合計が足りていても、その日の棚は空になってしまう」 + 「初めて針を刺す人の数は…以前とそれほど変わらない」: the author explicitly rejects the quantity framing this option grants. The weakest of the four, but eliminable on a stated fact, not on "the key fits better" |
| **58-4** 「決まりが厳しすぎるために、二度目に来る人が減ったということ」 | OK. Passage gives the reason as 「次にいつ来られるのかが分からない」, not strictness |
| **64-4** 「貸した相手が使いにくいと言うなら、その人の腕が足りていない」 | OK. Passage attributes the borrower's difficulty to the tool being fitted to its owner; 腕の不足 never appears |
| **67 stem** 「…手つづきが煩雑だったのはなぜか」 | OK, key 4. Deciding line 「施設ごとに申込書の形が違い、受け付けの始まる日も抽選の日もまちまちだったからである」. 煩雑 is a （注1） headword used in a stem — permitted (the gate's headword-reuse ban is scoped to 問題1–9) and the gloss 「こみいっていて、手間が多くわずらわしいこと」 does **not** state the reason, so no leak |
| **解説 64 / 65 / 69** | All three re-derived onto the NEW closings and every quote is present verbatim: 64 「台の当たり方が変われば面の仕上がりは変わる」; 65 「近所の方が感じていたわずらわしさは、私の見ていない時間に生まれていたのです」; 69 「いくつも押さえられるようになった団体が、先に動き方を変えていたのだ」. No 解説 quotes a superseded string |
| **`logs/topics.json` `notes`** (rewritten wholesale) | Every quoted paper string grepped. All present. `殺し合う`, `ふるまい`, the old 構成表 cell and the old 3-5番 key are correctly named as REMOVED, and all four measure 0 occurrences |
| **`claim` × 5 + `surfaces` × 1** | Re-read against the items, naming who did what (the `20260903_1` actor-swap class). 問題13's 団体 are the ones who changed behaviour ✓; 問題12(B)'s neighbour reports the darkness, the owner watched the weeds ✓; 聴解問題5-2番 「男の学生は当初の動画講座から…グループ練習会へ移る」 matches 「僕は動画講座かな」 → 「じゃあ、グループ練習会にするよ」, both questions asked about the male student ✓. **No inverted record found** |
| **`ledger.json`** | `items == spec["items"]`, seed byte-identical, `pools_sha` identical, no `harvest_sha` field at all |

**One wording defect in `notes`, not a paper defect.** The note asserts 「the pair
is split at skeleton level, not relabelled」 for 問題12(B)/問題13. Its own
`closing_moves` cell in the same row records both as 意外な観察, and the measurement
in F2 below shows both on one skeleton. The note claims a split the row's own data
denies. Fix it with F2.

### Keyed-form re-grep after every prose repair (§3, the `20260903_1` precedent)

Re-run from scratch over 問題10–14 passage prose + （注N） definition lines, for all
21 keyed 問題7/8/9 forms, because F2 rewrote five closings and F3 rewrote seven
glosses and lengthened 問題13:

- 19 of 21 forms: **0 occurrences**.
- 「〜てくれる」 (問題9-51): **1** — 問題10(1) 「…知らせてくれる。」 At the cap, and the
  S4 exclusions do not change the verdict (three of 51's four options carry the
  auxiliary).
- 「はずだ」 (問題9-49): **0** in prose; 2 in other 大問's OPTION strings, out of
  scope per S4(c).
- **問題8-46's new form 「のは…からだ」, which round 1 never had to check:** measured
  as the discontinuous skeleton within a single sentence, with copula
  normalisation (からである ≡ からだ) — **0 sentences carry both halves.** There are
  **5** sentence-final bare 「からだ／からである」 in 問題10–14 prose (問題11(4) ×2,
  問題12(A), 問題13, 問題11(3)), which is the highest of all 29 papers on disk
  (official 0–4, other generated 0–5); but the bare connective is not the keyed
  form, and the gate's own extraction comment says so explicitly. Recorded so the
  next reader need not re-derive it. Closest near-miss, also recorded: 問題12(A)
  puts 「実際に手が止まるのは、その手前の段階である。」 and 「持ち主が一人とはかぎらない
  からだ。」 in **adjacent** sentences — not the frame (the cleft's predicate is
  である; the からだ is an independent reason for the whole preceding assertion).
  **Concur with the carried-forward disposition on 問題9 ¶3's bare 「からだ。」**, and
  add that editing it alone would be inconsistent with these five.

---

## 4. Findings

| # | 項目 | class | evidence | status |
|---|---|---|---|---|
| **F1** | 問題5-24 | **自動不合格** — off-level key + three mutually-synonymous distractors | `言語知識・読解.md` L38, key row L476. Options たまに / まれに / **いつも** / ときどき on target 常に. 解説: 「1 ✗ たまに 2 ✗ まれに 4 ✗ ときどき＝**いずれも頻度が低いことを表す副詞で**、絶え間なさの逆になる。」 — one clause, one axis, three options. Live `check_goi_option_set_valence` WARN | **OPEN** |
| **F2** | 読解 問題12(B) + 問題13 closings | 要修正 — the pair round 1 ordered split is still one pair, on a new skeleton and one shape label | 12(B) 「近所の方が感じていたわずらわしさは、私の見ていない時間に**生まれていたのです**。」 / 13 「いくつも押さえられるようになった団体が、先に動き方を**変えていたのだ**。」 Both `〜てい(た)＋(のだ\|のです)`. `logs/topics.json` `closing_moves` labels **both** 意外な観察 | **OPEN** |
| **F3** | 問題11(3) （注3）便 | 要修正 — gloss leaks the key of a stem anchored on its own headword | Gloss 「便：**決まった道すじを、決まった時刻に**行き来する乗り物」; stem 61 「続いている**便**に共通しているのはどのような点か」; key 61-2 「予約がなくても**定まった時刻に**出し、待つ場所を屋根の下に置く点」. Shared content run 「まった時刻に」 = 6 chars | **OPEN** |

### F1 — the ruling you asked for, in full

**The WARN is a TRUE POSITIVE. It is a real defect and it is an automatic fail.**
Two independent grounds, either sufficient:

**(a) Three distractors, one reason.** たまに ≈ ときどき ≈ まれに all mean "not
often". A candidate who knows only that 常に is not "sometimes" eliminates three
options with one piece of knowledge, and cannot be asked to discriminate *among*
them. That is a 2-choice on frequency polarity with four options printed — the
`20260904_1` F1 shape one 大問 later. The 解説 states it in the author's own words.
**Measured against official practice:** I extracted all **25** parseable 問題5
option sets from the archive (12/2023, 7/2024, 12/2024, 7/2025, 12/2025) and read
each as a set. **Not one has three mutually-synonymous distractors.** The closest
official shape — 上を向いて／横を向いて／下を向いて／後ろを向いて (12/2023) — is a
paradigm of four *distinct* values, not three synonyms plus an antonym. And
official's own four-basic-adverbs set, いろいろ／まだ／やっぱり／かなり (7/2025-22),
carries four semantically **unrelated** adverbs; each dies for its own reason.

**(b) Off-level key and off-level option set.** The key is 「いつも」 — N5-core, the
first frequency adverb any learner meets. §2.5's named TOO_EASY example is
「four basic N4–N5 adverbs (めったに／なかなか／とても／ちっとも)」; たまに／まれに／
いつも／ときどき is that example with different words. The tested word 常に is
itself N3-register written Japanese, so the item tests nothing at N2. Every other
問題5 item on this paper is properly calibrated (やかましい, 用心する, だらしない,
妥当だ); 24 is the only one out of band, which is why it reads as a draw defect
rather than an authoring slip — and it is.

**The draw is the defect, and it is a single pool row.** `test_spec.json`
`paraphrase[3]` = **`つねに(いつも)`** — the pool entry prescribes both the target
*and* the key. Scanning all **143** `paraphrase` entries in
`.agents/exam-blueprint/references/pools.json`, this is the **only** entry whose
parenthesised key is an N5-core word. Delete or repair that one row and the class
cannot recur.

**Refusing the cheap fix, in the check's own words:** rewriting the 解説 as three
sentences leaves the same four options and buys nothing. The gate's failure text
says so; §2b says so; do not do it.

### Repairs, appliable as written

**F1 —**

```bash
python3 .agents/exam-blueprint/scripts/sample_items.py \
    --test-id 20260904_1 --reroll-one paraphrase:3
```

(`paraphrase:3` is 0-based and is the `つねに(いつも)` slot; verified against
`sample_items.py`'s `--reroll-one <CAT:INDEX>` handling and against the two
rerolls already in the seed string.) **No hand substitution.** Then:

1. Re-author 問題5-24 on the new target with the key at the prescribed position
   **3** (`answer_positions["問題5_語彙"] == [1,4,4,3,2]`).
2. Write the 解説 as **three separate sentences**, one per distractor, each naming
   a different axis. Re-run `make check` and confirm the
   `goi_option_set_valence` WARN is gone — not split, gone.
3. **Report the new key's band in the fix note as 「key X, band checked against
   <book, page or booklet+item>」** (§3). The archive route used for 乏しい above
   is the model.
4. Re-run steps 1–4 of this skill on all five 問題5 items, and re-check the
   問題1/2/5 stem counts (currently median 16 chars, 93 % comma-free — both at the
   top of the official band, so a longer replacement stem has little headroom).
5. Fix the pool row itself before the next generation run: see §5.

**F2 —** rewrite **問題12(B)'s final sentence only**. 問題13's closing must not be
touched: item 69's key (「心配された側ではなく、申し込みやすくなった側の動き方が変わっ
た」) hangs directly off it, and its 解説 was already re-derived once. Constraints
the replacement must satisfy, all of them:

- **Not** `〜てい(た)＋のだ／のです` (that is the defect), **not** 「〜のは…だ」
  (the skeleton round 1 removed), and **not** any `FINAL_SENTENCE_TEMPLATES` row
  already at its cap.
- **Not** any 「〜のだ／のです／のである」 ending at all. This paper already closes
  **5 of 13** surfaces on the のだ family against an official maximum of 4
  (measured over all 8 imported sittings); dropping 12(B) brings it to 4.
- Keep です・ます register — 12(B) is one of exactly 3 polite passages and the gate
  floor is 3.
- Keep the facts items 65 and 66 key on: the neighbour's concern was the night
  darkness rather than the weeds, and B reaches its problem *through the
  neighbour's words*.
- Plant no 問題7/8/9 keyed form (re-run the §3 grep afterwards — F3's gloss repair
  is why this is not optional).
- Keep 問題12 inside 510–600 JP chars (currently `ok` with margin).

A closing that satisfies all of these is a change of MOVE, not of wording: end on
the writer's own resolution or on a question rather than on a revelation, e.g.
「それからは、窓を開けに行くのを、日が落ちてからにしています。」 — 随筆-shaped (currently
1 of 13), no のだ, polite, and it leaves both keys untouched.

- **Then update `logs/topics.json`'s `20260904_1` row**: `closing_moves["問題12(B)"]`
  to the new move, `claim["問題12(B)"]` if the closing it retells changed, and the
  `notes` sentence asserting 「the pair is split at skeleton level」 — which is
  currently false.
- **Verification is by re-reading, not by `make check`.** The gate's cap is 2 and
  both readings of this pair sit at exactly 2, so it prints `ok` before and after
  (`20260812_1` F2→F3 precedent). Re-read the 13 finals as a column, twice: once
  down the shape labels and once down the sentence skeletons.

**F3 —** reword the gloss to drop the schedule wording:

```
（注3）便：決まった道すじを行き来する乗り物の、一回ごとの運行
```

Nothing else changes. Then verify: subtraction test still passes (no 便 character
in the definition), the marker/definition count stays 30/30 with 0 orphans, 問題11
stays inside 2250–2700 JP chars, and the §3 keyed-form grep is re-run over the
definition lines (the proposed wording contains none of the 21 forms).

---

## 5. Root-cause table (§6.5)

| # | code | recurrence (papers on disk showing the class) | owning file | concrete proposed edit |
|---|---|---|---|---|
| **F1** | `RULE-MISSING` | **1 pool row**, 1 of 143 `paraphrase` entries — but 2 items in this one paper (問題4-18 repaired, 問題5-24 shipped) | `.agents/exam-blueprint/references/pools.json` + `exam-blueprint/SKILL.md` | **Repair the row `つねに(いつも)`** — either drop it or re-key it to an N2 paraphrase (常に→絶えず／終始). Then add to `exam-blueprint` §pools: 「A `paraphrase` entry states the target AND the key. **Both** must sit in the N2 band. An entry whose parenthesised key is an N5-core word (いつも・とても・たくさん・すぐ・みんな) makes the item unfixable by authoring — it must be repaired in the pool.」 **Measured founding case:** scanning all 143 `paraphrase` entries, `つねに(いつも)` is the only row matching, so this edit repairs the corpus completely and re-classifies nothing else |
| **F1** | `RULE-UNENFORCEABLE` | same | `.agents/question-authoring/references/moji-goi.md` §問題5 | The register/valence rule is written for 問題4's context items; 問題5 is where the *synonym-cluster* form of the same collapse lives. Add: 「問題5 の4選択肢のうち、**二つ以上が互いに類義**であってはならない。三つが同一の軸の同じ側に並ぶと、受験者は一つの知識で三つを消せる——4択ではなく valence の2択になる。**官製の25問題5選択肢集合を実測した結果、互いに類義な誤答を3つ持つ集合は0件**（最も近い 上を向いて/横を向いて/下を向いて/後ろを向いて は4つの相異なる値）。」 |
| **F1** | *(not `GATE-BLIND`)* | — | — | `check_goi_option_set_valence` fired correctly, on the right item, with the right repair text. The gate did its job; the WARN was carried to QA rather than resolved. **No gate change proposed** — but see the process note below |
| **F2** | `GATE-BLIND` **with an honest caveat** | **1 paper at 2** (`20260904_1`); 6 generated at 1 (`20260813_2`, `20260817_1`, `20260818_1`, `20260819_1`, `20260821_1`, `20260827_1`); **8 official sittings at 0** | `tools/check_consistency.py` `FINAL_SENTENCE_TEMPLATES` | Add the row `"〜ていた のだ（後知れ）": re.compile(r'てい(た\|ました)(のだ\|のです\|のである\|のでした)。?\s*$')`. **Run over all 29 papers before committing — and read the result honestly: under the existing global `FINAL_TEMPLATE_CAP = 2` this row moves ZERO ids, i.e. it would NOT have caught its own founding case.** It is only evidence if it lands together with a per-template cap override (`FINAL_TEMPLATE_CAPS = {"〜ていた のだ（後知れ）": 1}`), which then moves **exactly one id, `20260904_1`**, and leaves all 8 official sittings and the other 20 generated papers untouched. Adding the row alone is the `check_mondai9_option_reuse` mistake (R3-9) repeated |
| **F2** | `RULE-UNENFORCEABLE` | **3 papers show the repair-collateral class** (`20260812_1` F2→F3, `20260903_1` F2, this) | `.agents/exam-qa-review/SKILL.md` §5, closing-move bullet | Add: 「**When a round-1 finding names a PAIR of surfaces sharing a skeleton, round 2 re-derives the pair on the NEW skeleton AND the NEW shape label — clearing the named template is not clearing the pair.** `20260904_1` round 1 F2 ordered 問題12(B)/問題13 split off 「〜のは…のほうだ」; the repair moved both onto 「〜ていた＋のだ／のです」 and left both labelled 意外な観察. Neither reading is visible to any check, because the cap is 2 and both sit at exactly 2.」 I am **proposing** this rather than applying it: it is a rule about round-2 conduct that belongs with the F2 gate row, so the two land together |
| **F3** | `GATE-BLIND` | **1 paper** (`20260904_1`); **0 of 8 official sittings** | `tools/check_consistency.py` + `dokkai.md` §（注N）「No answer leaks」 | The rule exists as prose and nothing reads it. Add `check_note_answer_leak()`: for every （注N） whose **headword occurs in a 問題10–14 stem**, WARN when the definition line and that item's **key** share a substring of **≥4 characters containing at least one kanji or katakana** (and not the headword itself). **FOUNDING-CASE MEASUREMENT, run over all 29 papers before proposing:** exactly **1** hit corpus-wide — `20260904_1` q61 「便」 ∩ 「まった時刻に」 — and **0** across the 8 official sittings. At a looser ≥3-char threshold the predicate produces 9 hits, 7 of them pure grammatical tails (「すること」「ってい」「ること」「一つの」「ている」), which is why the kanji/katakana condition is part of the rule and not a tuning knob |
| **process** | `RULE-IGNORED` | 1 | `AGENTS.md` §0.5 / §4, the stage-4 hand-off | `make check` was handed to round 2 as the entry condition with a WARN naming this paper **unresolved**. §0.5 and the Consistency-Gate section both say WARN is part of the output and must be resolved or individually justified *before* QA starts, and `exam-qa-review` §"Entry condition" repeats it. Deferring a live WARN to the reviewer is defensible **only when the hand-off says so in the report**, which it did not — the disposition lives in the orchestrator's prompt, not in `qa/`. Proposed edit to `jlpt-test-generation` §stage 3: 「A WARN naming the test under review is resolved, or the report records it as deferred-to-QA **with the reason**, before stage 4 is started. A WARN carried silently is indistinguishable from one nobody read.」 |

### Skill/gate findings with no paper defect

| # | code | evidence | proposed edit |
|---|---|---|---|
| **S1 (carried, still open)** | `GATE-WRONG` → **now fixed** | Round 1's S1 was applied: `check_errand_rotation` now WARNs with a coverage ratio (`2/44 = 5% keyed`) on **every** paper on disk instead of printing a confident `ok`. Verified in this run | **Closed as a gate change.** The underlying `pools.json` `key` gap is untouched — 42 of this paper's 44 draws still carry no errand key — so the WARN will fire on every paper until the pool is filled in. Keep it open against `exam-blueprint`, not against this paper |
| **S2 (carried)** | `GATE-WRONG` / `RULE-UNENFORCEABLE` | **DISPOSITION CONFIRMED, NOT DISPUTED.** 読解 kanji density is **31.6 %**. `official_calibration.md` L466–L497 now records: official current-era 25.5–30.1 %, all 21 generated papers 30.2–33.9 %, with the full sorted list and the two counterfactuals (WARN band → 25–30 flips **all 21**; `DOKKAI_KANJI_CEILING` 34 → 31 newly FAILs **17**). `20260904_1` at 31.6 is **7th lowest of 21**, below the generated median. This is pipeline drift, not this paper's defect, and the doc half was re-derived from `dokkai_profile.py` rather than retyped | **One residual defect in the applied half.** The gate still prints `20260904_1: 読解 kanji density in **target** 24–32% (got 31.6%)` — but 24–32 is now the *gate's WARN band*, and the *author target* is 25–30. An author reading that line concludes the paper hit a target it missed by 1.6 points. Rename the line to `読解 kanji density inside the gate WARN band 24–32% (author target 25–30%; got 31.6%)` at `check_consistency.py:3319`. Text only, no threshold moves, no id moves. **Also note the F3 repair pushed the number the wrong way** (31.3 → 31.6): lengthening 問題13 with 漢語 glosses (煩雑・周知・代行・重複・暫定) is density-raising, and the next repair of this class should be measured before it is applied |
| **S3** | *(round 1's S3 = F7)* | Applied. `check_section_table_quotes` exists, is scoped to 構成表 rows, and I ran it against its founding string — it fires (§3) | Closed |
| **S4** | `RULE-UNENFORCEABLE` → **applied** | The three exclusions are now written into `exam-qa-review` §3 as clauses 1–3 with the note that all three were re-verified against this paper and none flips a verdict. I re-derived clause (b) and (c) independently in §3 and reach the same result | Closed |
| **S5** | *(refutation record)* | The contrast-marker strategy is recorded in `exam-qa-review` §5 as refuted on two independent grounds, with the second run's numbers. I did not re-derive it | Closed as recorded. Do not re-derive |
| **S6 — NEW** | `GATE-WRONG` (coverage silence, the S1 class) | `check_p8_form_family` prints `ok … (1 keyed entr(ies))` — it compared **1 of this paper's 5** `grammar_p8` draws, because only the `つつ` and `ように` families are declared in `pools.json`. That is a confident `ok` over 20 % of the draw, which is exactly the shape S1 was raised about, in a check written **from** S1's own round | Two parts. (a) Apply S1's remedy here too: print the coverage ratio, and say in the line that it is silent about the unkeyed entries. (b) The family map is hand-maintained, so its completeness is unmeasured — add a one-off audit that clusters all `grammar_p7` + `grammar_p8` entries by `grammar_form_parts()` and lists any two entries sharing a form core but no `family` tag. Until that runs, the check's silence is not evidence |
| **S7 — NEW** | *(record only)* | `logs/topics.json`'s `notes` for this paper contains a self-contradiction of fact: 「NO MP3 REBUILD WAS NEEDED and none was run」 followed two sentences later by 「The rebuilt MP3 (sha256 4bd812cb761adc21…) WAS un-uploaded and is now on the `audio` release」. Both are true of different stages (an earlier fix context rebuilt; the re-merge stage did not), and every measurable claim checks out — but the sentence as written says the opposite of the next one | No gate change. Note for whoever next writes a Stage-3 note: attribute an artifact action to the stage that performed it. Recorded so a future reader does not read it as a staleness defect |

---

## 6. Coverage

**Steps run.** 0 (partial — keyless render rebuilt over the reviewed revision;
36 in-scope items solved from booklet text before any key; the two blind
STRATEGY passes re-computed on the shipped revision; §2 states exactly which
items were *not* blind and why). 1 (key proof for all 36 in-scope items plus the
5 問題8 orderings). 2 / 2b (distractor elimination for every in-scope item; the
問題4 and 問題5 option sets read as *sets* against the 25 official 問題5 sets).
2.5 (level band for 問題4/問題5's ten keys, and the band of both re-drawn keys
against the archive). 3 (mechanical reads: gloss counts, section lengths,
option-length ratios, longest-key rates, the keyed-form re-grep over all 21
forms, the 分裂文 and のだ-family closing measurements). 4 (問題3's 24 spoken
options read as a column by hand; the two changed 構成表 cells and the new
構成表-quote gate run against its founding case; 問題5's two questions and their
option order). 5 (closings column, both readings; the 問題13 / 聴解問題3-2番 and
問題12(B) / 聴解問題3-4番 adjacencies re-derived; headline sets confirmed via the
gate's four rotation checks). 6 (spec ↔ ledger field-for-field; 101 answer
positions; the `reauthored` provenance record on `listening_scenarios[12]`).
6.5 (root causes, each with a corpus run).

**Files read.** `tests/20260904_1/{言語知識・読解.md, 聴解.md, 聴解スクリプト.txt,
聴解_チャプター.json, test_spec.json}`; `qa/20260904_1/keyless.md`;
`qa/qa-report-20260904_1.md` (round 1, in full); `logs/{topics.json, ledger.json,
upload_manifest.json}`; `tools/check_consistency.py` (the six predicates named
above, read as source); `.agents/exam-qa-review/SKILL.md` (in full, from disk,
before any other tool call); `.agents/question-authoring/references/dokkai.md`
§（注N） + §問題14; `.agents/question-authoring/references/official_calibration.md`
§2; `.agents/exam-blueprint/references/pools.json`;
`.agents/exam-blueprint/scripts/sample_items.py` (CLI contract);
`refs/JLPT_N2_NEW/*/booklet.md` (31); `refs/Shinkanzen/goi_reference.md`;
`refs/Soumatome/goi_reference.md`; `tests/imported-n2-*/言語知識・読解.md` (8).

### The three adjudications you asked for

**1. `check_goi_option_set_valence` on 問題5-24 — TRUE POSITIVE.** Full reasoning
and the 25-set official measurement are in §4 F1. The check is correctly scoped
(問題4–6), correctly worded, and its repair instruction — fix the option set, never
the sentence — is the one to follow. **It is not a check to tune around.**

**2. The F3a rejection is SOUND, and I reproduced it independently.** At threshold
≥2 unglossed official uses, the founding words measure 抽選 6 / 一括 3 / 視察 3 /
ふるまい 2 / 当選 1 / 排除 1 / 当番 1 — and official sittings themselves gloss words
that other sittings print bare at higher rates (そもそも 7, 一切 5, 進化 5, 類 11,
概念 2, いわゆる 2; all six verified as actual （注N） lines in
`tests/imported-n2-2022-12`, `-2022-07`, `-2025-07`, `-2024-12`). A rule that
fails a real sitting is refuted; raising the threshold clears the archive only by
missing every founding word. **The rejection is correctly reasoned and correctly
recorded in `dokkai.md` §"（注N） — a refuted candidate check".**

Critically, **F3's paper-side repair does not depend on the refuted rule.** I
re-measured the 30 shipped glosses directly: 29 have **zero** unglossed official
uses, and the one exception (便, 2 official bare uses in the scheduled-service
sense) is still stricter than what official itself glosses. The count is honest —
30 markers / 30 definitions / 0 orphans, with 問題13 lengthened rather than
glosses cut. The repair stands. Its only defect is the leak filed as F3.

**3. S2's disposition is CONFIRMED, not disputed.** 31.6 % is 7th lowest of 21
generated papers, all 21 sit above official's 30.1 % maximum, and the doc half was
re-derived from the profiler with both counterfactuals and the full moving-id list
recorded. Tightening the gate would newly FAIL 17 shipped papers, which §6.5's
re-run-and-state rule correctly treats as a separate proposal, not a silent
tightening. Two riders, both in S2 above: the gate's WARN-line still calls 24–32
"target", and the F3 repair moved the number 0.3 points further from the
re-derived author target.

### Carried-forward dispositions, re-derived rather than accepted

- **問題9 ¶3's bare 「…からだ。」 — CONCUR.** Not 問題8-46's frame (the frame is the
  discontinuous pair within one sentence; this sentence has no 「のは」), outside the
  gate's 問題10–14 region, and the 読解 half already prints five ordinary bare
  「からだ／からである」 sentence-enders that nobody proposes to edit. Editing this one
  alone would be inconsistent as well as unnecessary.
- **問題4 printing 「細く」 (18) beside 「細やか」 (15) — CONCUR.** Different words,
  different readings, both distractors, both dying on their own axis; the gate's
  no-word-twice check passes on the correct reading.

### `make check` WARN resolution — every line naming this test

`make check` exits 0. **Four WARN lines have `20260904_1` as their subject or
name it:**

1. **`問題4–6 解説 eliminates all three distractors in one clause — 問題5-24`** —
   **NOT a false positive. Filed as F1, automatic fail.** See §4.
2. **`the errand-rotation check compares most of the draw (2/44 = 5% keyed)`** —
   correct and by design; it is round 1's own S1 remedy, and it fires identically
   on all 21 generated papers. Not this paper's defect; the repair is in
   `pools.json`.
3. **`every stamped spec's pools_sha matches pools.json`** — a multi-test record
   line that names every paper stamped on a reroll and says of itself that it is a
   record, not a defect. `20260904_1` stamped `eff0114aaa1a`, which is what its
   two rerolls were drawn from. Correct.
4. **`問題1/2 options share vocabulary with their script block (2/46 = 4%)`** —
   **false positive, and in the safe direction.** Both flagged options are the
   **keys** of their items (聴解問題2-1番-1 and 2-4番-4), and key paraphrase is what
   `choukai-items.md` asks for. Both are grounded in real script lines: 2-1番-1
   「かさが別の建物にうつされているから」 ← 「お預かりして三日たったものは、裏手の管理事務所
   のほうへまとめて移してるんです。あちらは、今日はお休みでして」 (script L120, and the
   「三日」 the 構成表 and `topics.json` both cite is verbatim there); 2-4番-4 ←
   「走っても六時ちょうどなんですよね。毎日、間に合うかな」 + 「少し気が楽になりました」
   (L171). **Zero distractors are flagged**, so there is no fabricated noise, and
   4 % deviates *below* the 11 % official baseline. The WARN's own text says it
   does not decide. **Not `GATE-WRONG`.**

Two `skip` lines name this test, both `詳細解説.json` absences that Stage 5
clears — correct ordering, not a gap. The remaining 278 WARNs name other tests
(chiefly the imported papers' Latin-script transcriptions and one quote line).

---

## 7. Skips (AGENTS.md §0.7)

- **No full 101-item blind solve.** This is a delta audit by instruction; round 1
  solved 101/101 from the same-shaped render with zero discrepancies. §2 names
  exactly which 36 items I solved blind and which 20 (問題8, 聴解問題1/2) I checked
  as key proofs only, having already read `answer_positions`. **If the fix round
  changes any item outside 問題5, that item and its 大問 need a fresh blind pass
  that this report does not supply.**
- **No full per-item walkthrough of the 65 items the repairs did not touch.**
  Round 1's §3 covers them and none of their sources moved in a way that reaches
  them. The keyed-form grep, the closing column, the topic table, the strategy
  passes and the gloss audit were all re-run paper-wide regardless, because those
  are the surfaces a local repair reaches.
- **`refs/` PDFs not opened.** Band decisions used the tracked `*.md` extracts and
  the 31 `booklet.md` files. The 乏しい band is established on the archive
  (7/2015 item 5, 12/2021 item 2) and does **not** rest on the 解説's additional
  Shin Kanzen page citation, which I did not verify — the PDF is 40 MB and
  readable, but the archive evidence is independent and decisive, so opening it
  would not change the verdict.
- **Audio not listened to.** Substituted: `script_sha` identity with the current
  script, duration, chapter count, the manifest sha256 match, and the gate's
  gender/pitch/pause checks.
- **`模範解答.html` / `詳細解説*.json` not inspected and `make model-answer` not
  run** — Stage 5 runs after PASS, by instruction. **Note for Stage 5: F1's repair
  will change 問題5-24's option strings again, on top of F1/F4/F6's round-1
  changes. Build `詳細解説.json`'s `options` arrays from the post-repair booklet,
  never from an earlier draft** (`check_model_answer_option_sync`).
- **No repairs applied, no `.agents/` file edited.** §6.5's Boundaries permit me to
  edit `exam-qa-review/SKILL.md` directly; I have not, because the two edits I
  propose there (F2's pair-re-derivation clause and F1's 問題5 synonym-cluster
  rule) belong with the gate rows they pair with, and the paper is FAIL regardless.
  Whoever applies the findings should apply them together.

---

## 8. Verdict, restated

**QA: FAIL (3 findings, 1 automatic).**

Seven of seven round-1 repairs are correct on disk, provenance is exact, and the
paper's measurable surfaces are among the strongest in the repository. All three
open findings sit where round 2 was supposed to look: one is a defect the fix
round surfaced and handed forward without resolving (F1), and two are collateral
the repairs themselves created (F2, F3). None requires re-deriving the paper; all
three are local, and each is written above so it can be applied exactly as stated.
