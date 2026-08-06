---
name: exam-qa-review
description: Single owner of the adversarial QA pass that every generated test must survive BEFORE it is served or committed. Use after `make check` is green on a new or repaired test, whenever the user asks to review/audit/QA a test, and whenever another agent (any harness, any model) reports a test as done. A green gate is the entry condition for this skill, not a substitute for it — every defect class listed here shipped through a green gate at least once.
---

# Exam QA Review (adversarial pass)

## Why this skill exists

Tests 2, 3, and 4 all shipped with `make check` green. The generator model
optimizes what is checked; everything unchecked drifts. The drift has a shape —
the same four failure modes every time:

1. **No self-reconciliation.** The generator never re-reads its output against
   its own source. Test 4 keyed a 聴解 option naming 点検作業員 where the script
   says 管理事務所, and its 解説 quoted five lines the audio never speaks —
   options written before the dialogue settled, never reconciled after.
2. **Fluency beats discrimination.** Four plausible words *look* like an option
   set, so すなわち shipped as a distractor for つまり — the same word. Test 4
   had seven items with two defensible answers.
3. **Late-file degradation.** Defects cluster in whatever was generated last
   (test 4: the listening half). Long single-pass generation degrades; the
   review must weight the end of the paper at least as heavily as the start.
4. **The skills themselves are defective.** Every paper is an output of the
   skills in `.agents/`. A full review of tests 1–4 found seven defect classes
   in **all four papers at once** — 問題11 passages with two factual questions
   and no opinion question; 聴解 distractors nobody says; 5–29 `（注N）` glosses
   against the official ~35; no 問題9 blank requiring whole-passage tracking;
   問題6 domain-violation distractors; item 71 as a single-field lookup;
   passages under band. Four independent authoring runs do not make the same
   seven mistakes by coincidence. Repairing the four papers and stopping there
   guarantees test 5 ships them again — so QA's output is **two** work lists:
   the paper's findings, and the skill defects behind them (step 6.5).

QA therefore has one job: **read the paper the way a hostile examinee would**,
with the sources side by side, and refuse to pass anything it cannot prove —
then name what let each defect through.

## Ground rules (strict by construction)

- **The default verdict is FAIL.** A test is broken until every check below has
  produced its evidence. The reviewer's job is to break the paper; "I found
  nothing" is only a pass if the evidence trail shows where you looked. Doubt
  resolves AGAINST the item: if you have to argue for a key, the item fails.
- **Fresh eyes, mandatory — no same-session fallback.** The reviewer must not
  be a context that authored anything in the test. Run this skill in a subagent
  or a NEW session that has read nothing but this file and the test's files.
  AGENTS.md §6 makes authoring-vs-QA the one non-negotiable split even in the
  worst fallback; a context that wrote any part of the paper re-reading it from
  disk is still the author auditing its own intent — the setup every defective
  test shipped through. (This also keeps authoring contexts small: author, then
  hand off; don't interleave.)
- **Blind-solve before reading the keys.** Take the paper first: answer every
  文字・語彙/文法/読解 item and, from the script, every 聴解 item, WITHOUT
  looking at the answer tables. Then diff against the keys. Every mismatch is a
  finding — either the reviewer is wrong (fine, say why) or the item has a
  second defensible answer or a mis-key. This one procedure would have caught
  most of test 4's shipped defects on its own; do it before anything else so
  the keys cannot anchor your reading.
- **Entry condition:** `make check` green, and its WARN lines either resolved
  or individually justified. Do not start QA on a failing gate.
- **Evidence or it didn't pass.** Every verdict below is backed by a quoted
  line, a spliced sentence, or a table — never "looks fine". If you cannot
  produce the evidence, the item fails.
- **No sampling. All 101 items, every check.** "Spot-checked and it looked
  good" is a skipped step, not a pass. The only sampling allowed is the harvest
  URL fetch in step 6 (2–3 URLs), because the rest of that step is exhaustive.
- **Any single automatic-fail finding fails the WHOLE test** until fixed and
  re-reviewed. Automatic fails: a second defensible answer; a keyed option the
  source does not state; an unanswerable item or 例; a 解説 quote not in the
  source; a topic repeated within the paper or from the previous test; broken
  Japanese anywhere in stems, options, passages, or script; narration
  contradicting the mapped voice; a spec/paper provenance mismatch; **an
  off-level KEY** (N1-hard or N3/N4/N5-easy — see step 2.5 /
  `references/level_band_grammar.txt`, which covers 問題7–9 GRAMMAR only, so
  every 問題1–6 vocab key is on the reviewer: test 4 keyed 賢い/かしこい, an N3
  headword in `openjlpt/vocab-n3.json`, and no gate looked); **an option that is
  not a real Japanese word** (test 4's 問題1 もてあそわる/まねわる/ひるがえわる);
  **a drawn target for which no rule-compliant option set exists** — file it
  against the draw, not the options (test 4's 労わる, step 2b); **a paper whose
  `tests/<test_id>/test_spec.json` carries no `answer_positions`** — the gate prints
  "0 prescribed" and passes, so nothing verifies the 101 keys and all four papers
  on disk came out answer-1-heavy (38–53% on option 1); **a distractor eliminable on sight for
  a reason unrelated to the tested point** — wrong part of speech, wrong
  domain, wrong tone, or an unrelated functional category (see step 2b); **a
  聴解 distractor not grounded in anything said in the dialogue**; **a 問題9
  blank testing the same grammatical/functional category as another blank in
  the same passage**; **an orphaned `（注N）` gloss whose term never appears in
  the passage body, or an in-body `（注N）` marker with no definition line**
  (test 4 shipped 「準備（注5）」 with no 注5 at all); **a 問題14 item answerable
  from a single constraint, or referencing a scenario detail (a role, category)
  the source text never describes**; **an artifact older than the source it is
  built from** — `聴解.mp3`/`聴解_チャプター.json` predating
  `聴解スクリプト.txt`, or the HTML predating its Markdown; the audio then
  speaks superseded text and no other gate can see it (tests 2 and 4 both
  shipped this from one commit that rewrote the 問題 instructions); **apparatus
  carried over verbatim from another test** — test 2's 問題11 `（注N）` notes were
  a character-for-character copy of test 1's, in the same passage slots, and
  three were orphaned because the passages around them had changed; **a 読解 key
  identifiable without reading the passage**, because it is a verbatim 60–110
  character lift of a passage sentence beside ~25 character distractors (test 3
  shipped three in a row); **any passage, dialogue, 例, stem, or option copied
  verbatim from `refs/` or from an `imported-*` paper** — AGENTS.md §5 allows
  reference material for calibration only, and tests 1 and 2 shipped three 例
  dialogues (236, 228 and 236 characters) byte-identical to the official July
  2025 exam's. Check this against the imported papers directly, not just
  test-against-test: the round that found it had filed the defect as test 2
  copying test 1, and missed that BOTH had copied the official paper.
- **Fix, regenerate, re-check, RE-REVIEW.** Findings are repaired in the
  Markdown/script sources, then booklet HTML + `解答.html` (+ MP3 if the script
  changed) are regenerated and `make check` re-run. Then the changed items AND
  their whole 問題 go back through steps 1–4, and step 5's table is rebuilt if
  any topic moved. Fixes introduce defects at the same rate as authoring —
  test 4's repairs were themselves re-reviewed and one had to be redone. A
  fix-and-approve in the same breath is a rubber stamp, not a review.
- **The reviewer does not negotiate the bar.** No waiving a rule because the
  test is "mostly fine", the deadline is close, or the author already ran the
  gate. If a rule here seems wrong, propose the change in the report; apply the
  rule as written to this test.
- **Imported Tests (`tests/imported-*`) Rule:** Do NOT update `logs/ledger.json` or `logs/seeds.json` for an imported test. Imported tests do not sample from the item pool or web seeds. For imported tests, skip Step 5 (topic table against past generated tests) and Step 6 (provenance audit). Focus QA strictly on transcription fidelity against source PDFs/audio, booklet-script option sync, and solvability.


## The pass, in order

### 1. Key-by-key proof (all 101 items)

For each item, find the line in the passage/script that DECIDES it, and confirm
the keyed option restates that line — not a paraphrase of what the author
probably meant. Copy the deciding line into the 解説 cell if it is not already
there (paste, never from memory; `make check` WARNs on quotes it cannot find,
and that warning found five invented quotes in test 4).

While there: a 理由 question must be keyed to the CAUSE the source states, not
to the measure taken about it (test 4 問題2-4番 keyed "cut night buses" when
the script gave 運転手不足 as the reason — and another option said so).

### 2. Distractor elimination (the two-answer hunt)

For every item, write one line per wrong option naming why it is IMPOSSIBLE —
not "less natural". The reason must be a fact: a collocation that does not
exist, a line in the source that denies it, a grammatical clash. If the best
you can write is "the key fits slightly better", the item has two answers;
**replace the distractor**, do not defend the key.

Highest-risk shapes (all shipped): near-synonym connectives (すなわち/つまり),
competing particles on the same noun (に沿って/に即して on ニーズ), negative
prefixes that both attach (無記入/未記入), adverbs sharing the frame
(いいかげん/おろそか on 〜にする), and 問題6 "wrong" sentences that are actually
real collocations (品質に妥協する, 考慮に値する — search before trusting).

### 2b. Distractor plausibility (the opposite failure — too WEAK, not too strong)

Step 2 catches a distractor that creates a second answer. This step catches
the mirror failure, which passed a green gate in tests 1–4 across 問1, 問4,
問5, 問6, and 聴解問題1–3 at once: a distractor eliminable on sight, for a
reason that has nothing to do with the tested point, so the item collapses
from a 4-way discrimination into "spot the one option that isn't nonsense."

For every item, ask of each wrong option: *"Is this the SAME part of
speech/functional category/domain/tone as the key, competing on the specific
point being tested — or does it die for an unrelated reason before the reader
ever engages that point?"* Evidence, not a feeling:

- **Vocab-in-context/paraphrase/usage (問4-6):** write the functional category
  each option belongs to (degree adverb, regret adverb, coincidence adverb,
  …). If the four options don't share one category, FAIL — e.g. わりに (key)
  with 案の定/とっくに/一段と (as-expected / already / increasingly — none is a
  comparison/degree competitor); まして (key) with あいにく/徐々に/たまたま
  (regret / gradualness / coincidence — none is a comparative-adverb
  competitor); 切実 (key) with 痛快 in the set (tonally opposite, discarded
  without reading). For 問題6, confirm each wrong sentence describes a
  situation inside the word's own domain, merely misusing it — 解消 applied to
  physically discarding a computer, or 把握 personified onto a medicine, are
  domain violations, not collocation traps, and FAIL this step even though
  they are grammatically well-formed.
- **問1 漢字読み — TWO branches, and this file used to state only one.** A
  distractor passes if it satisfies **either**: **(a)** it is a reading of the
  target's own kanji or of a same-radical/visual-component kanji (措置: そち/
  しょち/そうち; 険しい: けわしい/けんしい/かんしい), **or (b)** it is a real N2
  word in the SAME semantic field and the same word form (official July 2025
  問1-2 辛い → あまい/にがい/しぶい; 問1-5 収まった → さだまった/しずまった/
  やすまった). What fails is a grab-bag across unrelated fields: いたわる with
  ことわる/さわる/かわる (readings of 断る/触る/代わる — unrelated kanji AND
  unrelated fields) satisfies neither branch, and a reader eliminates all three
  without ever considering 労. This is `question-authoring`'s 問題1 「Same-kanji
  OR same semantic field rule」 restated; if the two files ever disagree again,
  `question-authoring` owns authoring and this bullet is the copy to fix.
- **問1 — every option must be a REAL WORD, and if no compliant set exists the
  TARGET is the defect.** Non-words are never distractors. Test 4 shipped
  「労わる」 with もてあそわる/まねわる/ひるがえわる and a 解説 that invented
  spellings for them (弄わる/招わる/翻わる) — a "repair" of the earlier
  ことわる/さわる/かわる set, i.e. the item failed this rule twice in two
  different directions. It was not fixable at the option level: the printed
  okurigana locks the class to ～わる, 労 reads only ロウ/いたわ(る)/ねぎら(う),
  no look-alike kanji yields a ～わる verb, and every real ～わる verb is an
  unrelated kanji in an unrelated field — **both branches empty.** When that
  happens, do not invent options and do not argue the set down: fail the item,
  and send the TARGET back to `item-pool-sampling` to be re-drawn. Check the
  same way round too — a target whose printed okurigana disagrees with its
  `openjlpt` headword spelling (test 4's 労わる vs the corpus's 労る) is a pool
  defect, not a typo to patch in the paper.
- **聴解問題1-3:** for every wrong option, find the line in the script that
  raises it. If no line raises it, it is fabricated, not a distractor — FAIL.
  (This is the listening form of the same check; do it here as well as in
  step 4, since it is a plausibility defect, not only a structural one.)

If you cannot point to the shared category, the reason it's the SAME kind of
option as the key, the item fails this step — replace the distractor with a
real competitor, do not argue the current one is "close enough."

### 2.5. Level band (N2 only — not N1, not N3–N5)

The paper's **tested** items (問題1–9 keys, 問題5's hard word, 聴解 即時応答
idioms) must sit inside the N2 band. Drifting either way is a fail:

| Drift | Symptom | Action |
|-------|---------|--------|
| **Too hard (N1)** | Keyed grammar/vocab that Shin Kanzen N2 does not head, and common N1 lists do (にあって, をもって, ともなると, までもなく as productive grammar, を皮切りに, 余儀なくされる as a tested form, …) | Replace the KEY with an N2 form; keep `answer_positions` |
| **Too easy (N3–N5)** | Keyed form a lower-level textbook would drill (によると, ば〜ほど, てください, ほうがいい, ことができる, たいです, 前に/後で as the sole point, がち alone, …) | Replace with a real N2 discrimination |

Procedure for every 問題7–9 key (and spot-check 問題1–6 / 即時応答):

1. Name the form the item actually tests (from the keyed option + 解説 gloss).
2. Ask both sides, not one: *"Would Shin Kanzen N1 / a Tettei-N1 list claim this?"* AND *"Would this appear as a headed item in an N3 (or easier) book?"* If either is yes, the item fails — rewrite, do not argue "examinees should know it anyway".
3. Cross-check the hard side against `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-*.pdf` TOC / inventory (rasterize when there is no text layer — see `reference-book-reading`). Forms absent from N2 Shin Kanzen and present in N1 lists are TOO_HARD.
4. Distractors may show off-level forms **only when they are morphologically or collocationally impossible in the stem** so an N2 examinee can eliminate them without knowing the N1/N3 item. Prefer N2-band distractors.
5. Passive exposure to N1 wording inside 読解/聴解 prose is allowed when glossed (`（注N）`) or simplified; it must not be what the question keys on.

`make check` enforces the string-decidable half via
`references/level_band_grammar.txt` (TOO_HARD / TOO_EASY / ALLOW). This step
still owns the judgment calls the gate cannot see (vocab keys, 問題5 hard
words, "がちだ" vs bare "がち", 読解 questions that only test N5 fact-lookup).

**The vocab half is entirely yours — do it as a lookup, not a feeling.** The
band file holds grammar; no gate has ever checked a 問題1–6 key. So look every
tested key up in `references/openjlpt/vocab-n1|n2|n3.json` and write the result
into the report. A key that is an **N3 headword and absent from the N2 list is
TOO_EASY** — that is how 賢い/かしこい shipped as a 問題1 key in test 4.

**But the labels are a lookup, not a verdict — read this before filing.** That
corpus is an aggregate word list: it labels 把握・転換・審査・じっくり・前もって・
逃す・省みる as "N1" and 依頼・実施・克服・考慮・偶然・徐々に as "N3", and every
one of those is ordinary N2 exam vocabulary that is correctly keyable. Use the
lookup to *raise the question*, then answer it with step 2.5's two questions
against Shin Kanzen N2 (`refs/Shinkanzen/`). Filing 把握 as off-level because a
list said "N1" is the same mis-measurement this skill codes `GATE-WRONG`, and it
sends the fixing pass off to break working items.

### 3. Mechanical reads

- **問題7 stem length:** count JP chars on every stem. Official papers average
  ~43 (band ~33–54). Fail the paper if the 12-stem average is under ~35, or if
  more than a couple of stems sit under ~30 — that is the short-carrier defect
  tests 1–4 shipped (avg 20–34) while the grammar keys looked fine. Fix by
  rewriting the situation, not by changing the keyed form. Also fail a paper
  whose 問題7 set has **zero** dialogue/setting-label stems (`「…」` turns or
  `（会社で）` etc.) — official papers always include a few.
- **問題8 / 問題9 length:** 問題8 assembled sentences should not read as
  three-word drills; 問題9 cloze body should land ~500–700 JP chars (official),
  not a 150–200 char stub.
- **読解 apparatus & formatting:** using `imported-n2-2025-07` (July 2025) as
  the bar — fail (or hard-warn) a generated paper with fewer than ~15 `（注N）`
  across 問題10–13, with **no** `（中略）` anywhere in 中文/長文, or with 問題13
  under ~850 JP chars. Count **in-body markers** (one per glossed term, in the
  passage region), not raw `（注N）` occurrences: each gloss also has a
  definition line and 解説 may back-reference it, so occurrence counting nearly
  doubles the figure — that is precisely the `GATE-WRONG` bug that let tests 1–4
  ship 5–9 glosses against a nominal 15 bar. Measured with the in-body metric,
  July 2025 has **30** and tests 1/2/3/4 have 9/6/29/5. A gloss count that
  exceeds the in-body count means orphaned definitions (test 2: 8 definitions,
  6 markers) — check both directions.
  **Fail any paper that glosses basic N3–N5 or standard N2 words** (such as 選択, 信号, 技術, 文化, 質, 準備, 手順, 設計, 現象, 経由, 偏り, 維持, 継続, 前提, 細部, バランス) or uses trivial circular definitions. Notes must strictly target N1+/rare/literary/specialized terms or contextual metaphors.
  **Fail any paper containing `<ruby>` (furigana) in `言語知識・読解.md`** — test-takers read N2 kanji without furigana; over-the-level terms must use only `（注N）` notes.
  **Fail any paper with mismatched passage numbered markers (`①**...**`, `②**...**`)** — every numbered marker in a passage must match 1-to-1 with a question stem in that question block (no orphaned/unused markers).
- **問題11:** must be 4 passages × 2 questions with instruction `(1)から(4)`.
  Each passage's two questions must split ONE factual-comprehension question
  + ONE main-point/opinion question — fail a passage with two factual
  questions and no opinion question (test 4 shipped one). For every `（注N）`
  in each passage, confirm the glossed term actually occurs in that passage's
  body — an orphaned gloss (test 3 shipped this across all 4 passages) fails
  the paper.
- **問題2 表記:** confirm the 2×2 component-matrix shape — each of the 4
  options should share the compound's two-character skeleton with only one
  or both characters swapped for a visually/structurally similar wrong one.
  Fail a set where a "distractor" is a real, unrelated word (test 4's 展開
  next to 傾向), or where only one character position ever varies across all
  four options.
- **問題3 語形成:** confirm every option is a real, productive affix that
  could plausibly attach to the SPECIFIC stem — not just a plausible affix in
  the abstract. Fail a nonsense affix (test 4's 迷〜, not a real negation
  prefix — the real four are 非/無/未/不) or an option that doesn't suffix
  onto the stem at all (伴い/同行/組み合わせ on 家族).
- **問題14:** confirm the correct answer requires combining **at least two**
  constraints from the table/flyer (never a single-field lookup), and that
  every scenario detail the question references (a role, category, condition)
  is actually describable from the source text as printed — fail a question
  that invents a detail the flyer never mentions (test 3 asked about a
  "補助スタッフ" role the source never described).
- **問題5 言い換え:** swap the option into the stem; the sentence must survive
  (test 4: 「値段の比較的美味しい」 did not).
- **問題8:** splice stem + options in 解説 order; read end to end; no word twice.
  Then hunt the SECOND ordering: try each option in each other slot — a floating
  adverb/adjunct (ほとんど, 直接, 一度…) that reads naturally in two slots is
  two ★ answers. One such item shipped in each of tests 2, 3, and 4.
- **問題9 cloze:** read stem + option aloud as one sentence, all four options.
  Then name each blank's category (論理接続表現 / 文末モーダル表現 / 内容推論 /
  慣用・形式名詞 — see `question-authoring`'s 問題9 rule). Fail the passage if
  two or more blanks share a category (test 4 shipped two connective blanks
  and two content-inference blanks; test 2 and test 3 each repeated one
  pair) or if NONE of the four blanks requires tracking the whole passage's
  argument rather than just the local sentence.
- **問題1 漢字読み:** all four options the same word form as the target; each
  a real word; and none uniquely selected by the stem's conjugation/okurigana.
  Cover the kanji, keep okurigana visible — if only one option still fits the
  conjugation class, fail it (test 1: 慌てて with three ～れて vs one ～てて).
  Same mora count is not required.
- **One grammar point, one KEY per paper** — check 問題7/8/9 keys against each
  other AND against the reading passages' running text.
- **Every sentence is Japanese.** Read the whole paper aloud once. Test 4 had
  six broken sentences (「契約の契約書を解消」, 「互いの条件を歩み寄り」,
  「借りましたCD」, 「代わりに代診」…), several inside CORRECT options.

### 4. 聴解 structure

- The question type matches the 問題: 何をしますか lives in 問題1, どうして/
  何が一番 in 問題2, 何について in 問題3. Test 4 shipped 問題1↔問題2 swapped.
- **Every 問題1-3 wrong option must be grounded in the script.** For each
  distractor, find the line that raises it (a task/statement mentioned then
  reassigned, superseded, or denied). An option nobody says is fabricated
  noise, not a distractor, and it lets the item be solved without tracking the
  conversation — fail it and demand a real one (test 4's 問題1 1番 and 問題2
  1番 each shipped one fabricated option; test 1's 問題3 2番 had 3 of 4 options
  never mentioned at all).
- Every 例 is answerable from its printed options AND the announced number is
  the option the dialogue supports (test 4's 問題1 例 printed options for a
  different question, and the announcer declared one of them correct; test 3's
  問題1 例 kept the announcement while its option set was mangled so the true
  first action was not printed at all). The marksheet's pre-marked 例 must equal
  the announced number — `make check` now compares them (it caught mismatches
  in three of the four shipped tests), but the dialogue-supports-it half is
  yours.
- 即時応答 keyed replies must match the speakers' rank (keigo direction — see
  question-authoring; test 2 keyed a 社長 speaking humble keigo downward).
- Narration ↔ voice ↔ `SPEAKER_MAP`: 「女の学生」 must not be spoken by a
  male-mapped label. Wrong options must each be raised and DENIED in the audio;
  a second true statement is a second answer.

### 5. Whole-paper and cross-test topic table

Build the table from `jlpt-test-generation` §"One topic, one surface" — one row
per surface **including each 聴解 item**, one column per test (this test, the
two before it). Fail on: any subject twice in this paper in any register; any
subject repeating the previous test; two 聴解 items running the same errand
(test 4: apartment-hunting in 問題1-4番 and 問題5-3番); the 問題14 flyer sharing
a decisive detail with a listening item; and check 問題12's A/B theme against
the previous tests' 問題12 specifically (three papers in a row argued 働き方).

### 6. Provenance & Spec Blueprint Audit

Verify `tests/<test_id>/test_spec.json` against the authored paper end to end:

1. **Target Item Match Audit (問題1–8 & 聴解 問題4):**
   - Verify every item tested in `漢字読み` (問1), `表記` (問2), `語形成` (問3), `文脈規定` (問4), `言い換え類義` (問5), `用法` (問6), `文法問題7` (問7), `文法問題8` (問8), and `即時応答` (聴解 問4) matches the EXACT target item specified in `test_spec.json["items"]`.
   - Fail any paper where an author substituted a different target item during drafting — unrecorded substitutions corrupt the rotation ledger.
2. **Answer Positions Compliance Audit:**
   - Verify all 101 answer key positions (71 Gengo + 30 Choukai) match `test_spec.json["answer_positions"]` exactly.
3. **Web Fact Consistency & Copyright Non-Reproduction:**
   - For every web-derived surface (`origin: "web"` in `reading_topics`, `listening_scenarios`, `info_retrieval_texture`, `qr_situation_seeds`, `carrier_seeds`), verify the passage/dialogue incorporates the simplified fact in `test_spec.json` accurately without contradicting it.
   - Verify copyright invariants: max 1 simplified fact per passage/dialogue, original phrasing, no reproduction of source article structure or verbatim sentences.
4. **Web Blend Balance & Carrier Cap:**
   - Verify web share sits within 30–60% per surface with pool ≥40%, and no single domain supplies >2 topic seeds.
   - Verify carrier sentences in 問題1–8 use web texture on at most 1 in 3 stems per 問題.
5. **Harvest URL Verification:**
   - Spot-check 2–3 `logs/seeds.json` URLs by fetching them. Sequential or unresolvable URLs mean the harvest was invented — report it immediately.

### 6.5. Root-cause every finding against the skills

**The paper is not the defect; it is the symptom.** Every item in it was written
by an agent following `.agents/*/SKILL.md`, sampled by a script, and cleared by
`tools/check_consistency.py`. So after the findings table is closed, walk it
once more and answer, per finding: *what would have had to be different in the
skills or the gate for this to be impossible?* Fixing only the paper leaves the
generator that produced it unchanged.

**The recurrence test — apply it first, it is not a judgment call.** Count how
many of the tests on disk show the finding's class. A class present in **two or
more papers is systemic by definition**: stop calling it an authoring slip and
root-cause it. Do this by reading the other tests' sources, not from memory. The
review of tests 1–4 turned up, among others: two-factual 問題11 in all four
papers; ungrounded 聴解 distractors in all four; the `問題14` single-field lookup
landing on item 71 in three; the 問題5 2番 lead-in spoken aloud in all four
though official papers keep it booklet-only; `SPEAKER_MAP` gender mismatches in
two; a stale MP3 in two (same commit); and test 2's 問題11 notes being a
verbatim copy of test 1's, in the same passage slots.

Assign each finding exactly one root cause:

| Code | Meaning | Fix goes to |
|---|---|---|
| `RULE-MISSING` | No skill forbids it. The author had no way to know. | the owning skill |
| `RULE-UNENFORCEABLE` | A rule exists but as prose with no number, template, or procedure ("keep passages long enough"), so it cannot be complied with or verified | the owning skill — convert to a number or a construction procedure |
| `RULE-IGNORED` | The rule exists, is specific, and was skipped | nothing to change; report it as a process failure per AGENTS.md §0 |
| `GATE-BLIND` | String-decidable, and no check exists | `tools/check_consistency.py` |
| `GATE-WRONG` | A check exists and **mis-measures**, so green was never evidence | `tools/check_consistency.py`, **plus re-verify every test that passed on it** |
| `PIPELINE-GAP` | Sources are right; an artifact was not regenerated, or step ordering permits staleness | `jlpt-test-generation` workflow + the gate |

`GATE-WRONG` is the most dangerous code and the easiest to miss, because the
symptom is silence. Two live examples found this way: the `（注N）` counter
matched both the in-body marker **and** its gloss-definition line, so 9 real
glosses reported as 18 and every paper cleared a 15-gloss bar that was really
7.5; and the 解説 quote matcher did not strip inline `（注N）` from the source,
so five quotes that *are* in the passage were reported missing — burying the one
that genuinely was not. A miscalibrated check is worse than no check: it
converts an open question into false proof, and it trains the next reviewer to
discount the warning.

**Who owns what** — name the skill by file, not by area:

| Symptom | Owning skill |
|---|---|
| 問題1–6 stems, options, distractor sets, 問題9 blank categories, 読解 apparatus (`（注N）`, `（中略）`, lengths), 問題14 constraint count | `question-authoring` |
| Which item is tested, answer-position balance, rotation/ledger accounting | `item-pool-sampling` |
| 問題-to-question-type mapping, 例 mechanics, what is printed vs spoken, section counts | `jlpt-exam-structure` |
| Script block shape, spoken/booklet split, narration labels | `choukai-script-writing` |
| `SPEAKER_MAP`, voice↔narration agreement, pacing, pauses | `choukai-mp3-generation` |
| Topic freshness, cross-test/cross-surface repetition, blend caps, domain caps | `web-topic-research` + `merge_seeds.py` |
| Pass ordering, regeneration steps, artifact staleness | `jlpt-test-generation` |
| Booklet/sheet rendering, stem-line layout, furigana | `exam-booklet-generation`, `interactive-answer-sheet` |
| Anything string-decidable, in any row above | also `tools/check_consistency.py` |

**A root cause without a proposed edit is not a root cause.** For each one,
write the target file, the section, and the actual sentence, number, table row,
or check to add — enough that the fixing pass applies it without re-deriving it.
Prefer, in this order: (1) a number or a template that replaces a judgment call,
(2) a construction procedure at authoring time rather than a check at review
time — a rule the author can only verify *after* writing the passage gets
skipped,
(3) a check in the gate when the rule is string-decidable. State when a rule
genuinely cannot be mechanized and must stay a human judgment; that is a valid
answer, and saying so keeps the next reviewer from assuming the gate has it.

**Boundaries.** The reviewer *proposes* skill edits and does not apply them to
generation skills mid-review — an author-adjacent context rewriting the rules it
was just judged against is the same inversion this skill exists to prevent. The
one file the reviewer may edit directly is **this one**: when a defect class
found in the paper is absent from this skill, add it to the automatic-fail list
or the relevant step immediately, in the same session, with the shipped example
named. Rules only count when they execute or get read.

**Effect on the loop.** A paper may reach `QA: PASS` with skill findings still
open — the paper is fixed, and that is what PASS is about. But **an open
`RULE-MISSING`, `RULE-UNENFORCEABLE`, `GATE-BLIND`, `GATE-WRONG`, or
`PIPELINE-GAP` finding blocks the next generation run**, because the next test
will reproduce it. Each must be applied, or explicitly rejected with a reason,
before a new test is authored. Carrying one forward silently is how a defect
becomes all four papers.

### 7. Report (required format)

The report is the deliverable; without it the review did not happen. It must
contain, in this order:

1. **Verdict line:** `QA: PASS` or `QA: FAIL (<n> findings, <m> automatic)`.
   PASS is only writable when steps 1–6 all ran on all items and zero findings
   remain open.
2. **Blind-solve diff:** reviewer's answer vs key for every mismatch, each
   resolved as "reviewer error because …" (with the deciding quote) or filed
   as a finding.
3. **Findings table:** one row per finding — item, class (from the automatic-
   fail list or "minor"), evidence quote, fix applied or reason left open.
4. **Root-cause table (step 6.5):** one row per finding — finding id, root-cause
   code, how many tests on disk show the class, owning file, and the concrete
   proposed edit. Group the rows that share a root cause: ten items failing on
   one missing rule is **one** skill defect, and reporting it ten times hides
   that. Findings coded `RULE-IGNORED` still get a row, marked as needing no
   skill change.
5. **Coverage statement:** which steps ran on which files, the topic table
   itself (not a claim that you built it), the URLs fetched in step 6 and what
   they returned, and every WARN from `make check` with its resolution —
   including any WARN you determined to be a false positive, with the evidence,
   since that is a `GATE-WRONG` finding.
6. **Skips:** anything not done, stated explicitly, with why. An unstated skip
   is how defects ship (AGENTS.md §0.7).

Only after a PASS report may the test be committed or served. A FAIL report
goes back to the author (or the fixing pass) with the findings table as the
work list — and the root-cause table goes to whoever touches the skills next,
because the paper's fixes do not change the generator that produced it.

## Relationship to the other gates

`make check` proves the mechanical contract (keys parse, positions match,
options distinct, script shape). This skill proves the CONTENT: one defensible
answer, sources that support their keys, a paper that does not repeat itself.
Neither substitutes for the other; the orchestrator runs them as steps 9 and
9.5.

It also proves the **generator**, via step 6.5. QA is the only pass that reads a
finished paper against every rule that produced it, which makes it the only
place the skills get audited at all — and the audit is not optional, because a
defect class that survives here gets re-authored into the next test. So when QA
finds a defect class this file does not list, add it here AND, if it is
string-decidable, to `tools/check_consistency.py`; when it finds the *cause* in
another skill, file it in the root-cause table with the concrete edit. Rules only
count when they execute or get read — and a check that mis-measures counts for
less than none, because it makes green look like proof.
