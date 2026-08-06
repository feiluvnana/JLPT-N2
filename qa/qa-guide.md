# QA guide — what these reports are, and the order to fix them

Nine fresh-eyes reviewers audited tests 1–4 on 2026-08-06 under
`.agents/exam-qa-review/SKILL.md`. None of them authored any part of the papers;
none of them edited any file. Every report is a work list, not a change.

**All four papers are `QA: FAIL`.** Totals below exclude the 43 `make check`
failures, which the reviewers were told not to re-file.

| Report | Scope | Verdict | Findings (automatic) |
|---|---|---|---|
| `qa-test1-gengo.md` | tests/1 問1–14, 71 items | FAIL | 26 (7) |
| `qa-test1-choukai.md` | tests/1 問題1–5, 30 items + 例 | FAIL | 13 (4) |
| `qa-test2-gengo.md` | tests/2 問1–14 | FAIL | 28 (11) |
| `qa-test2-choukai.md` | tests/2 問題1–5 | FAIL | 22 (8) |
| `qa-test3-gengo.md` | tests/3 問1–14 | FAIL | 31 (22) |
| `qa-test3-choukai.md` | tests/3 問題1–5 | FAIL | 31 (19) |
| `qa-test4-gengo.md` | tests/4 問1–14 | FAIL | 28 (9) |
| `qa-test4-choukai.md` | tests/4 問題1–5 | FAIL | 22 (11) |
| `qa-crosstest.md` | steps 5 + 6 across all four | FAIL | 20 (11) |
| | | **total** | **221 (102)** |

Per test: t1 39/11 · t2 50/19 · t3 **62/41** · t4 50/20 · cross-test 20/11.

---

## 0. Three facts that change how you read every report

1. **`make check` is RED — 43 failures, 15 warnings.** The QA entry condition
   ("do not start on a failing gate") was deliberately waived on the user's
   instruction. Those 43 rows are a *pre-filed work list*; reviewers filed only
   what the gate missed. Read `make check` output alongside these reports.
   Cause: commit `8a6943c` added 740 lines of new checks today, so papers
   authored against the old gate now fail the new one. The failures are real.
2. **Folder order is not chronological.** Real authoring order is
   **1 → 4-removed → 2 → 4 → 3**. Test 3 is the *newest* paper; test 4 precedes
   it. Every "repeats the previous test" finding uses that order — do not
   re-derive it from folder numbers.
3. **`logs/test_spec.json` holds one spec, test 3's.** Tests 1, 2 and 4 have no
   blueprint on disk, so their target-item and answer-position audits are
   **impossible, not skipped**. Test 1 has no ledger entry at all.

---

## 1. The order, and why it is this order

Do not start at Phase 4. Each phase exists because the phase after it produces
wrong work without it.

```
Phase 1  Fix the instruments        ─ the gate lies today; every later "verified"
   │                                  claim rests on it
Phase 2  Fix the wrong rules        ─ three rules the OFFICIAL paper fails;
   │                                  authoring against them damages the papers
Phase 3  Fix the inputs             ─ spec/ledger/harvest/pools; re-topicking
   │                                  cannot start until the harvest is fresh
Phase 4  Repair the papers          ─ 1 → 2 → 4 → 3, and within each paper
   │                                  topics → passages → items → apparatus → build
Phase 5  Fresh-eyes re-review       ─ changed items AND their whole 問題
```

### Phase 1 — Fix the instruments first (`GATE-WRONG`)

A miscalibrated check is worse than no check: it turns an open question into
false proof. Ten were found. Each fix carries a **re-verification** duty for
every paper that passed on the broken version.

| Broken check | Symptom | Source |
|---|---|---|
| 問題11 banned-stem regex anchors on `本文` | test 3 writes `文章で述べられているもの` — 3 stems slipped past | t3-gengo RC6 |
| 解説-quote matcher passes option rows as "source", and floors at ≥14 chars | a 解説 quoting its own option validates; short/elided quotes invisible | t2-gengo R11, t1-gengo R10 |
| `（注N）` band WARN tests a vocab slice that cannot decide the class | reported 3 of 15 wrong-band glosses; term not normalised (慰め→慰める) | t3-gengo RC10, t1-gengo R8 |
| 例-copy check is byte-identical, block-level, script-only | misses booklet option lists, rewritten stimuli, `？` vs `?` | t1-choukai RC2, t4-choukai C3 |
| one-voice casting check inspects only 2-label items | 3-party items hide duplicate voices | t1-choukai RC5, t4-choukai C14 |
| key-findability needs ≥50 chars **and** ≥1.7× | a 36-char verbatim lift at 1.36× passes | t4-gengo R6 |
| ledger DRAW-count check compares old draws to today's `DRAW` | 4 noisy false failures that train readers to ignore the row | crosstest X19/R7 |
| `harvest_sha` read from the hand-editable ledger | **the whole test-3/test-4 harvest reuse was invisible** | crosstest R1 |
| blend "distinct topic per surface" is exact-string | マイボトル×2, スマート農業×2, 記憶×2 all pass | crosstest R4, t3-gengo RC7 |
| `validate_script()` tests the closing line as a substring | the closing sits *inside* 問題5-2番 and corrupts pacing | t2-choukai F9, t4-choukai C8 |

### Phase 2 — Fix the wrong rules before authoring against them

`tests/imported-n2-2025-07` is the bar. **A rule the official paper fails is a
wrong rule**, and "fixing" a paper against one makes it worse. Test 1's reviewer
withdrew three of its own findings on this basis:

- **問題1 「every distractor must share the target's kanji/radical」** — official
  問1-2 offers 辛い → あまい/にがい/しぶい and 問1-5 収まった → さだまった/しずまった/
  やすまった. Restate as *same conjugation class AND (same kanji/radical **or**
  same semantic field)*.
- **「every option must be a real word」 applied to 表記** — official 問題2 ships
  液って/温って/汗って and 支接/施接/支設. Non-words are the norm there.
- **問題3 「the affix must plausibly attach to THIS stem」** — official 問3-11 is
  教育 → 則/理/論/規, none of which attaches either.
- **聴解問題3 distractor grounding** — official 概要理解 distractors are
  topic-level with the modifier absent, exactly like test 4's. Soften the rule
  for 問題3 only (t4-choukai §4a).

⚠ **Re-adjudicate before fixing:** `qa-test3-gengo.md` F12 and
`qa-test4-gengo.md` F8 were filed under the *old* 問題1 rule. Apply the
corrected rule to them first; part of each may not be a defect. Their okurigana
findings (t3 F13) are a separate, valid rule and stand.

Also in this phase, because a compliant author reproduces them:

- `question-authoring`'s 問題2 worked example **is** an official item — test 1's
  item 6 option set is 75% identical to official 問7 as a result (t1-gengo R12).
  Replace the worked examples; add "examples are patterns, never ship one".
- `question-authoring` prints 『契約を解消した』 as banned-because-attested, and
  test 4 shipped it anyway (t4-gengo F3). Move these to a
  `references/banned_collocations.txt` the gate can enforce.
- `level_band_grammar.txt` lists `つもりです` as TOO_EASY without distinguishing
  the N2 認識 sense 「〜ているつもりだった」 (t1-gengo §5).

### Phase 3 — Fix the inputs (nothing downstream is auditable without them)

1. **Per-test spec snapshot.** `logs/test_spec.json` is a single mutable file, so
   generating test N destroys test N−1's blueprint. Write
   `tests/<id>/test_spec.json` at sampling time. Until this exists, three of four
   papers can never be audited. (crosstest R9, t2/t4-gengo)
2. **Ledger hygiene.** Stop hand-writing `harvest_sha` (`harvest_20260804`,
   `legacy_0803sh` are placeholders that replaced real stamps); make history
   append-only; add a `retired: true` flag instead of renaming (`4-removed` is a
   phantom draw double-booking test 4's items); reconstruct a `test 1` entry.
   ⚠ **Do NOT "trim the over-recorded items"** as `make check` advises — see the
   conflict in §3.
3. **Re-harvest `logs/seeds.json`.** It was reused across tests 4 and 3, one
   document is mined by three seeds, and that document contains **zero**
   occurrences of 給水 and 割引 though both are recorded as its facts and written
   into two graded passages. **All re-topicking in Phase 4 blocks on this.**
4. **Write `logs/topics.json`.** It has never been written for any test, so
   `merge_seeds.check_topic_reuse()` has been a silent no-op on every run — which
   is why ten surfaces repeated from test 4 into test 3 undetected.
5. **`pools.json` corrections:** pull `軍(いくさ)` (a 表外訓 — JLPT never keys
   one), pull `ば〜ほど` (TOO_EASY), fold `〜気味`/`〜ぎみだ` across the whole draw
   rather than per category, and remove the three sub-N2 即時応答 prompts.

### Phase 4 — Repair the papers: **1 → 2 → 4 → 3**

That order is dependency-driven, and conveniently runs cheapest to hardest:

- **1 and 2 are a pair** — test 2's 問題11 `（注N）` notes are test 1's, reworded,
  in the same passage slots, and both papers' 例 are the official paper's. Fix
  them together or you will fix the same copy twice. Neither depends on the
  harvest, so they can start immediately after Phase 2.
- **4 and 3 are a pair** — they share a harvest and collide on ten surfaces.
  Deciding *which paper keeps which subject* is one decision; it cannot be split
  across two agents. Both block on Phase 3.3.

Within one paper, work in this order — each step invalidates the ones above it
if done later:

1. **Topics and subjects** (they cascade into everything).
2. **Passage-level rewrites** — genre fixes (問題11 must be signed opinion prose,
   not 社内連絡), then length floors. Do not lengthen a passage you are about to
   replace.
3. **Item-level** — keys, distractors, splices, broken Japanese.
4. **Apparatus** — `（注N）` pairing and band, `（中略）`, 解説 quotes re-pasted by
   copy-paste, and the three mandatory artifacts that are missing from **all four
   papers**: 問1–6 category lines (`24: 程度副詞 ×4 (…)`), 問題8 alternative-order
   lines, 聴解 `N ✗「script line」→ 理由` grounding lines. Writing these is what
   surfaces the defects; they are not paperwork.
5. **Rebuild, in this order:** `make mp3 <id>` → `make booklet <id>` →
   `make sheet <id>` → `make check`. Every test currently ships an MP3 built from
   a superseded script (`script_sha: None`), so **the audio contradicts every
   printed 問題 instruction**.

### Phase 5 — Re-review with fresh eyes

Per `exam-qa-review`: fixes introduce defects at the same rate as authoring. The
changed items **and their whole 問題** go back through steps 1–4 in a context
that did not make the fix. Rebuild the cross-test topic table if any topic moved.
`QA: PASS` closes a paper; the root-cause tables stay open until applied or
explicitly rejected, and an open one **blocks the next generation run**.

---

## 2. Do-not-fix list

Reviewers verified these as already repaired or not reproducible. Fixing them
wastes a pass or re-introduces a defect.

| Claim | Status |
|---|---|
| "three papers in a row argued 働き方" in 問題12 | Not reproducible — 働き方 appears in one passage, in no 問題12 |
| test 4's 問題1-4番 and 問題5-3番 both apartment-hunting | **No paper has a 問題5-3番**; 問題5 is 1番+2番 everywhere |
| test 2's フードドライブ key spelled out in the 問題14 flyer | Not reproducible — that flyer is 生涯学習フェスタ |
| test 4's five invented 聴解 解説 quotes | Fixed; 74 quotes re-checked, the 7 non-literal ones are elisions/glosses |
| test 4's mis-keys (点検作業員, cause-vs-measure), 問題1↔2 swap, 迷〜, 展開/傾向, 問題5 swap-in, four broken correct options | All verified **gone** |
| test 3's 問題14 「補助スタッフ」 invented role, 問題1 例 mangled options, Latin 「contrast」, orphaned 問題11 glosses | All verified **gone** |
| test 2's 社長 speaking humble keigo downward | Fixed |

---

## 3. One conflict between reports — adjudicated

`make check` says: *"trim the over-recorded items from `logs/ledger.json`"*, and
`qa-test2-gengo.md` R16 / `qa-test4-gengo.md` F28 repeat that advice.

**Do not trim.** `qa-crosstest.md` X19 traces it: `DRAW` was retuned *after*
those tests were sampled (`word_formation 5→3`, `quick_response 12→11` in
`7638a2f`; `listening_scenarios 20→21` in `58a8c8b`), and no migration was done.
The ledger records what was actually drawn — it is correct. Trimming it would
delete real rotation history to satisfy a check that measures historical draws
against a table that changed under them. Fix the **check** (stamp each history
entry with its own `draw` dict), not the record.

---

## 4. Parallel-safety rules for fixing agents

- **One agent per (test, half).** Never two agents in the same `.md`. The
  topic-collision work for tests 3+4 is one agent, not two.
- **A gate/skill agent must not also author a paper.** An author-adjacent context
  rewriting the rules it was judged against is the inversion QA exists to prevent.
- **Reviewers may not apply their own root causes.** These reports propose; a
  separate pass applies.
- **Touching `聴解スクリプト.txt` obliges an MP3 rebuild**; touching any `.md`
  obliges booklet + sheet. A stale artifact is an automatic fail.
- **Re-run `make check` after every phase** and read every line, WARN included.
  Green is the floor, not the goal — it cannot see a second defensible answer.
