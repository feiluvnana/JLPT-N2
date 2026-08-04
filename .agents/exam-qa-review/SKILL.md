---
name: exam-qa-review
description: Single owner of the adversarial QA pass that every generated test must survive BEFORE it is served or committed. Use after `make check` is green on a new or repaired test, whenever the user asks to review/audit/QA a test, and whenever another agent (any harness, any model) reports a test as done. A green gate is the entry condition for this skill, not a substitute for it — every defect class listed here shipped through a green gate at least once.
---

# Exam QA Review (adversarial pass)

## Why this skill exists

Tests 2, 3, and 4 all shipped with `make check` green. The generator model
optimizes what is checked; everything unchecked drifts. The drift has a shape —
the same three failure modes every time:

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

QA therefore has one job: **read the paper the way a hostile examinee would**,
with the sources side by side, and refuse to pass anything it cannot prove.

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
  contradicting the mapped voice; a spec/paper provenance mismatch.
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

### 3. Mechanical reads

- **問題5 言い換え:** swap the option into the stem; the sentence must survive
  (test 4: 「値段の比較的美味しい」 did not).
- **問題8:** splice stem + options in 解説 order; read end to end; no word twice.
  Then hunt the SECOND ordering: try each option in each other slot — a floating
  adverb/adjunct (ほとんど, 直接, 一度…) that reads naturally in two slots is
  two ★ answers. One such item shipped in each of tests 2, 3, and 4.
- **問題9 cloze:** read stem + option aloud as one sentence, all four options.
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

### 6. Provenance audit

`logs/test_spec.json` against the paper: every surface's topic is the spec's
topic with the spec's origin; no duplicate entries; web share within 30–60% per
surface. Then spot-check the harvest itself: pick 2–3 `logs/seeds.json` URLs
and fetch them. Sequential or unresolvable URLs mean the "harvest" was invented,
which silently breaks the no-two-tests-share-a-harvest rotation guarantee —
report it even if the topics themselves are usable.

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
4. **Coverage statement:** which steps ran on which files, the topic table
   itself (not a claim that you built it), the URLs fetched in step 6 and what
   they returned, and every WARN from `make check` with its resolution.
5. **Skips:** anything not done, stated explicitly, with why. An unstated skip
   is how defects ship (AGENTS.md §0.7).

Only after a PASS report may the test be committed or served. A FAIL report
goes back to the author (or the fixing pass) with the findings table as the
work list.

## Relationship to the other gates

`make check` proves the mechanical contract (keys parse, positions match,
options distinct, script shape). This skill proves the CONTENT: one defensible
answer, sources that support their keys, a paper that does not repeat itself.
Neither substitutes for the other; the orchestrator runs them as steps 9 and
9.5. When QA finds a defect class this file does not list, add it here AND, if
it is string-decidable, to `tools/check_consistency.py` — rules only count when
they execute or get read.
