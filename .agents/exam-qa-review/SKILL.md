---
name: exam-qa-review
description: Single owner of the adversarial QA pass that every generated test must survive BEFORE it is served or committed. Use after `make check` is green on a new or repaired test, whenever the user asks to review/audit/QA a test, and whenever another agent (any harness, any model) reports a test as done. A green gate is the entry condition for this skill, not a substitute for it — every defect class listed here shipped through a green gate at least once.
---

# Exam QA Review (adversarial pass)

## Why this skill exists

`make check` can be green while the paper is still broken. The generator model
optimizes what is checked; everything unchecked drifts, in four recurring
failure modes:

1. **No self-reconciliation** — options written before the dialogue/passage
   settled, never reconciled after (a 聴解 key naming 点検作業員 where the
   script says 管理事務所; a 解説 quoting lines the audio never speaks).
2. **Fluency beats discrimination** — four plausible-*looking* words are not
   four discriminating options (すなわち as a distractor for the synonym
   つまり); an item ends with two defensible answers.
3. **Late-file degradation** — defects cluster in whatever was generated last
   (often the listening half); weight the end of the paper as heavily as the
   start.
4. **The skills themselves are defective** — reviews have found recurring
   classes (ungrounded 聴解 distractors, low `（注N）` counts, 問題6 domain-
   violation distractors, single-field 問題14 lookups, under-band passages).
   QA's output is **two** work lists: the paper's findings, and the skill
   defects behind them (step 6.5).

QA's one job: **read the paper the way a hostile examinee would**, sources
side by side, refuse to pass anything unproven — then name what let each
defect through.

## Ground rules (strict by construction)

- **Default verdict is FAIL.** Doubt resolves AGAINST the item — if you have
  to argue for a key, the item fails.
- **Fresh eyes, mandatory — no same-session fallback.** The reviewer must not
  be a context that authored any part of the test. Run in a subagent or a new
  session that has read nothing but this file and the test's files
  (`AGENTS.md` §5) — a context re-reading its own writing is still the author
  auditing its own intent.
- **Blind-solve before reading the keys — from the keyless render, step 0.**
  A key you've seen cannot be un-seen. Executable procedure:
  1. `make keyless <test_id>` → `qa/<test_id>/keyless.md`: the whole
     101-question paper plus `聴解スクリプト.txt`, key heading/tables/解答用紙
     marks/解説 column truncated by `strip_key()` (`exam-app` §"The answer key
     must never be VISIBLE"). Build aborts rather than emit a render still
     carrying a key.
  2. **Read that file and nothing else.** Answer all 101 items; write the
     list into your report draft. 聴解 is solvable from the embedded script.
  3. Only then open the sourced Markdown and diff your list against the keys.

  Every mismatch is a finding — reviewer error (say why, with the deciding
  quote) or a second defensible answer / mis-key. Copy the render's source
  `sha1`s into the report header; rebuild the render when you finish — if the
  shas moved, a fixing pass edited underneath you and the review is void.
  **State which file you solved from.**
- **Entry condition:** `make check` green, its WARN lines resolved or
  individually justified. Do not start QA on a failing gate.
- **Evidence or it didn't pass** — a quoted line, a spliced sentence, a
  table, never "looks fine".
- **No sampling. All 101 items, every check.** A spot-check is a skipped step.
- **Any single automatic-fail finding fails the WHOLE test** until fixed and
  re-reviewed. Automatic fails:
  - a second defensible answer; a keyed option the source does not state; an
    unanswerable item or 例; a 解説 quote not in the source; a topic repeated
    within the paper or from the previous test; broken Japanese anywhere;
    narration contradicting the mapped voice; a spec/paper provenance
    mismatch;
  - **an off-level KEY** (N1-hard or N3/N4/N5-easy — `level_band_grammar.txt`
    covers 問題7–9 grammar only, so every 問題1–6 vocab key is the reviewer's:
    check against Shin Kanzen Master N2-Goi/N2-Kanji and 日本語総まとめ N2
    語彙/漢字, not a vendored corpus — `openjlpt` was removed 2026-08-11);
  - **an option that is not a real Japanese word**; **a drawn target for
    which no rule-compliant option set exists** — file it against the draw
    (step 2b);
  - **a paper whose `test_spec.json` carries no `answer_positions`** — the
    gate prints "0 prescribed" and passes, verifying nothing;
  - **a distractor eliminable on sight for a reason unrelated to the tested
    point** — wrong part of speech, domain, tone, or an unrelated functional
    category (step 2b);
  - **a 聴解 distractor not grounded in anything said in the dialogue**;
  - **a 問題9 blank testing the same grammatical/functional category as
    another blank in the same passage**;
  - **a 問題7 stem with no `（　）` at all**, which prints its own keyed answer;
  - **a 問題1 option set that is not the printed target's word form, or a
    問題2 set that is not the stem's inflected form** — printed okurigana then
    selects the key on sight;
  - **a 読解 distractor eliminable by an absolute quantifier or categorical
    denial** (すべて/まったく/のみ/だけで十分/無関係/存在しない);
  - **a 読解 section whose blind-solve strategy score exceeds 45%** (e.g. key is predictable via highest surface/bigram overlap with the passage, or key is consistently the uniquely longest option; paper median overlap margin >0);
  - **a 即時応答 prompt with no defined responder** — an announcement has no
    addressee-reply (e.g. a 火災報知器 prompt);
  - **an orphaned `（注N）` gloss whose term never appears in the passage
    body, or an in-body marker with no definition line**;
  - **a 問題14 item using a generic truth-check shape** (「〜として正しいものはどれか」「〜の内容と合っているものはどれか」) instead of asking a value, action, or named option;
  - **a 問題14 item answerable from a single constraint, or referencing a
    scenario detail the source text never describes**;
  - **an artifact older than the source it is built from** — `聴解.mp3`/
    `聴解_チャプター.json` predating `聴解スクリプト.txt`, or HTML predating its
    Markdown — the audio then speaks superseded text and no other gate sees it;
  - **apparatus carried over verbatim OR near-verbatim from another test** —
    compare by similarity, not equality (byte identity is the gate's test; a
    few edited characters evade it), and compare the surrounding sentences too;
  - **a 読解 key identifiable without reading the passage** — a verbatim
    60–110 char lift beside ~25-char distractors;
  - **any passage, dialogue, 例, stem, or option copied verbatim from `refs/`
    or from an `imported-*` paper** (`jlpt-test-generation` §Invariants:
    reference material is calibration only) — check against imported papers
    directly, not just test-against-test;
  - **a surface's `theme` in `test_spec.json` disagreeing with the same
    surface's `theme` in `logs/topics.json` WHERE `topics.json` relieves a
    quota or headline collision that the spec value creates** — a relabel in
    one file that dodges a collision without re-authoring or updating the other
    hides the collision instead of resolving it (`20260813_1`'s 問題13
    precedent). Decide it by counting, not by spotting the disagreement: tally
    the themes under each file's values and see whether the `topics.json`
    tagging is what brings a per-theme count inside its cap or takes a surface
    out of the headline set. If both tallies comply, the disagreement is a
    **`要修正` bookkeeping desync**, not an automatic fail — §5 *instructs* you
    to distrust the spec's theme and re-tag from the shipped text, so a paper
    that follows §5 honestly will routinely disagree with a stale pool tag
    (`20260821_1`'s 聴解問題2-3番/2-6番 precedent: neither relabel moved any
    count, both files were simply out of sync with a wrong `pools.json` tag).
    Then record the divergence — do NOT reconcile it by moving a `theme` value
    and do NOT edit `pools.json`. On the spec entry **and** the byte-identical
    ledger entry, keep the drawn `scenario`/`topic` string untouched
    (`recency_map()` keys on it) and keep `theme` at the value the sampler drew
    (the ledger is a record of the DRAW), then add three fields:
    `"shipped_theme"`, `"shipped_surface"` and a `"note"` saying, with the
    deciding line quoted, why the pool tag does not describe the authored
    surface. One paper's surface drifting off a tag is a record-keeping fact
    about that paper, not a pool defect. **`check_theme_record_agreement()`
    reads ONE of the three** — it joins each spec/ledger row to its
    `topics.json` surface, FAILs on a disagreement with no `"note"`, and goes
    silent once the note is there. `shipped_theme`, `shipped_surface`, and the
    requirement that the note QUOTE the deciding line rather than describe it,
    are read by this pass and by nothing else: check them off the row by hand.
    This paragraph said "reads exactly this" until 2026-09-04, i.e. it asserted
    a three-field contract the predicate never had, and the drift was found the
    only way it could be — by a reviewer reading the check
    (`qa-report-20260903_1-round2.md` §5, the trailing note). `20260821_1` is
    the sole paper on disk carrying `shipped_surface`; `20260903_1`'s 市役所 row
    carries `shipped_theme` + a note that describes rather than quotes, and
    passes. **Do not "resolve" this by dropping a field** — the three-field
    record is the authoring requirement, and the gap is in what the gate can
    see. Gating the other two is a live proposal, not a done deal: it would
    newly WARN every paper on disk that recorded a divergence under the
    one-field predicate, so it is taken as a deliberate widening (§6.5's
    re-run-and-state rule), not as a silent tightening. That check exists because this bullet
    previously ended in a prose sync instruction that nothing read: round 1 of
    `20260821_1` filed the desync, the rule was rewritten, and round 2 measured
    that not one byte had moved in either file (NF-4). Prose no check reads is
    prose that does not run;
  - **a headline theme (問題9/12/13/14/聴解問題5-1番/聴解問題5-2番) repeating the
    immediately-previous test's headline theme in ANY slot** —
    `exam-blueprint` rule 4's zero-tolerance clause, unchecked by any script.
    Build the 6-slot set yourself from the SHIPPED content and diff against
    the previous test's recorded set.
- **An option SET reused from an official paper**, even with no byte-identical
  line — compare the *sets* of proper nouns per 問題 against `tests/imported-*`.
- **問題5-2番 printing the deciding attribute beside an option name, or a
  different order for 質問1 vs 質問2** — printing facts are
  `jlpt-exam-structure` §問題5-2番; check against that, don't restate it.
- **A 問題8 item whose keyed order is ungrammatical, or whose set contains a
  bare adverbial standing alone** — the construction rule is the fix: no
  option may be an adverb alone, exactly one of 24 orderings may be
  grammatical.
- **A 解説 cell that itself declares a distractor ungrounded** — any
  「言及なし」/「未言及」 in a **問題1–2** 解説 is a confession, not an
  explanation. **問題3 (概要理解) is exempt, by design:** its distractors are
  topic-level summaries and the monologue must NOT mention its own wrong
  options (`question-authoring/references/choukai-items.md` §問題3, the owner;
  `make check` FAILs a 問題3 talk that mentions 2+ of them). 「〜の話は出てこない」
  is the correct 問題3 解説. This rule spanned 問題1–3 until 2026-08-19, which
  made every compliant 問題3 解説 an automatic fail on paper.
- **`logs/ledger.json` disagreeing with `test_spec.json`, or a hand-written
  `harvest_sha`** — compare field for field; a date-shaped sha is fabricated.
- **An item redrawn from a test inside the rotation cooldown** — `sample_items.py`
  has the cooldown data but no gate compares draws across tests; intersect the
  ledger's last two entries with this test's, after folding okurigana/kana
  tails, before trusting the draw.
- **Fix, regenerate, re-check, RE-REVIEW.** Repair sources, regenerate
  booklet/`解答.html`(+MP3 if the script changed), re-run `make check`. Changed
  items AND their whole 問題 go back through steps 1–4; step 5's table rebuilds
  if any topic moved. **Exception** (`jlpt-test-generation`'s stage-4 loop
  rule): a FAIL round with ≤3 findings may be fixed directly, skipping
  re-review — same rigor as any fix (root-cause, verify `make check`,
  sanity-read the diff). Fixes introduce defects at the same rate as
  authoring — a fix-and-approve in the same breath is a rubber stamp, not a
  review. A closing-move-shape fix (`dokkai.md` §"Thirteen surfaces, thirteen
  different essays") is verified by re-reading the new closing against the six
  named shapes, never by `make check` alone — `20260812_1`'s round-1 "fix"
  passed the mechanized marker check while shipping an identical 主張 shape,
  caught only by round-2 re-reading (`qa-report-20260812_1.md` F2→F3).
- **A fix that changes WHAT a surface tests must also update
  `test_spec.json["items"]["reading_topics"/"listening_scenarios"]` and
  `logs/ledger.json`'s mirrored entry**, marked `"origin": "reauthored"` with
  a `"note"` (`check_draw_provenance()` requires this). `20260811_1` re-themed
  five surfaces across two fix rounds and left the spec/ledger pointing at the
  original draws through a whole QA pass — a mismatch a same-file re-review
  cannot see, because it's BETWEEN files.
- **The same fix must also update every relevant field in that surface's OWN
  `logs/topics.json` entry** — the row's keys, which are
  **`surfaces`, `themes`, `closing_moves`, `voices`, `claim`, `persona`,
  `shapes`, `notes`** (read them off the row).
  **Correction, 2026-09-03:** this bullet briefly claimed "no row on disk has
  ever had a `shapes` key". That measurement was wrong — `shapes` (each 聴解
  item's errand shape, 33 entries) was present on **16 of the 20 rows**, on
  every paper through `20260827_1`; four papers had dropped it, silently,
  because no gate check read it. Deleting it from this
  list would have ratified that drift instead of catching it, so it is restored:
  `exam-blueprint` §"`logs/topics.json`" and `jlpt-test-generation` §stage 3
  both still require the field, and the errand-archetype rule ("two 聴解 items
  may not run the same errand, and archetypes must not repeat within the last
  two tests") has no other data to read. `20260903_1`'s row was then filled in
  from its shipped 聴解 (17 of 20), and `check_topics_shapes_field()` now reads
  the field, so the drift cannot recur silently: the three rows still empty are
  named in `TOPICS_SHAPES_DRIFT_GRANDFATHERED` and WARN, any other id FAILs.
  Verify a field's presence by grepping
  the rows, never from a claim about them — including this one.
  `20260817_1` updated
  `surfaces`/`themes` and left the closing-shape field describing the discarded
  pre-fix draw; no check compares it against `surfaces`. Update all of them
  together.
  **`surfaces` and `claim` are verifiable against the item, and must be
  verified — not only `notes`.** Both are one-line prose retellings of what
  shipped, and a retelling can invert the item while every gate stays green:
  `20260903_1` recorded 聴解問題5-2番 as 「男は太陽の観察会・女は星座の解説会」 and
  「太陽の観察会は男が、席を譲った女は…星座の解説会を選ぶ」 when the script has the
  woman take 太陽 (「私が太陽の観察会に申し込むね」) and the man take 星座 (「じゃあ、
  星座の解説会にするよ」) — the two people swapped, in the file the next paper's
  blueprint reads, with the KEYS correct and `notes` correct. Re-read each
  `surfaces`/`claim` line against the item's own deciding lines, naming who did
  what; a row whose actors are reversed is a false record even when no count
  moves.
  **`notes` is verifiable, and must be verified: every claim in `notes` that
  quotes a paper string must quote a string that is still in the paper.** The
  four-field list above stood until 2026-08-19, so `notes` was the one field
  nobody re-read — `20260817_3` shipped a note saying 「願ってもない is a printed
  distractor at 問題9-51」 (0 occurrences after the fix) and another saying the
  聴解問題2-2番 key still shared 「よそ」 with the script (0 occurrences).
  `notes` is the hand-off the NEXT paper's blueprint stage plans around; a note
  naming an artifact the fix removed is worse than no note. `grep` each quoted
  string before you leave it there.
- **The reviewer does not negotiate the bar** — no waiving a rule because the
  test is "mostly fine" or the deadline is close. Propose a change in the
  report if a rule seems wrong; apply it as written to this test.
- **Imported tests (`tests/imported-*`)**: do NOT update `logs/ledger.json`.
  Skip step 5 (topic table vs past generated tests) and step 6 (provenance).
  Focus QA on transcription fidelity, booklet-script sync, and solvability.

## The pass, in order

### 0. Blind solve, from `qa/<test_id>/keyless.md`

```bash
make keyless <test_id>      # → qa/<test_id>/keyless.md — the paper, no keys
python3 tools/qa_eval.py tests/<test_id> --answers "[1, 3, 1, 2, ...]"  # instantly diffs & validates
```

Read that file only, answer all 101 items, evaluate with `qa_eval.py`, then
open the sourced Markdown and diff. Full procedure in "Ground rules" above;
the diff is §7 item 2 of the report. Steps 1–6 all read the keys, so none can
run first.

**Then run the two BLIND STRATEGY passes over the 20 読解 items, and record both
scores in the report** (REPORT-DOKKAI.md §F1/§F2, §2.4). Before reasoning about
meaning, answer each 問題10–13 item twice mechanically:

1. pick the option sharing the most character bigrams with its own passage;
2. pick the second-longest option.

Chance is 25%. Official papers score 32.8% and 24.6% on these; a shipped paper
of ours scored **60.3%** and **49.2%**, which means an examinee who reads no
Japanese outscores one who reads badly. **Above 45% on either, the section goes
back to authoring** — and the repair is to rebuild distractors from passage
clauses with one fact changed, never to trim the key (trimming is how a
paraphrase collapses back onto the passage's wording). These two numbers are the
only way a single paper's F1/F2 exposure is visible to a human pass; the gate
sees the distribution, not the solvability.

### 1. Key-by-key proof (all 101 items)

For each item, find the line that DECIDES it and confirm the keyed option
restates that line — not a paraphrase of what the author probably meant.
Copy the deciding line into the 解説 cell if absent (paste, never from
memory). A 理由 question must be keyed to the CAUSE the source states, not
the measure taken about it.

### 2. Distractor elimination (the two-answer hunt)

For every item, write one line per wrong option naming why it is IMPOSSIBLE —
a fact: a collocation that doesn't exist, a source line that denies it, a
grammatical clash. If the best you can write is "the key fits slightly
better", the item has two answers — replace the distractor, don't defend the
key.

Highest-risk shapes (all shipped): near-synonym connectives (すなわち/つまり),
competing particles on one noun (に沿って/に即して on ニーズ), negative
prefixes that both attach (無記入/未記入), adverbs sharing a frame
(いいかげん/おろそか on 〜にする), formal-vs-plain movement/weather-verb pairs
(接近する/近づく on a mere degree adverb like 大きく — both take "Nに〜, 上陸する
おそれ" equally well in weather-bulletin register; disambiguate with a mundane/
non-technical subject where the Sino-Japanese verb reads as overreaching, not
with a degree adverb alone — `qa-report-20260828_2.md` F2), and 問題6 "wrong"
sentences that are actually real collocations (品質に妥協する, 考慮に値する —
search before trusting).

### 2b. Distractor plausibility (the opposite failure — too WEAK, not too strong)

Catches a distractor eliminable on sight for a reason unrelated to the tested
point, collapsing a 4-way discrimination into "spot the one option that isn't
nonsense." For every wrong option: *is this the SAME part of speech/
functional category/domain/tone as the key, competing on the tested point —
or does it die for an unrelated reason first?*

- **Vocab-in-context/paraphrase/usage (問4-6):** write each option's
  functional category (degree adverb, regret adverb…); if the four don't
  share one, FAIL (わりに with 案の定/とっくに/一段と — none a comparison
  competitor; 切実 with 痛快 in the set — tonally opposite).
  **The worked case, and the tell to look for (`20260904_1` F1, 2026-09-04):
  if the four options split 3:1 on TONE and the 解説 kills the three wrong ones
  in a single clause, the item is not a 4-choice — it is a 2-choice on
  valence.** 問題4-18 keyed 殺し合う against 助け合う / 話し合う / 支え合う and
  wrote 「1 ✗ 助け合う 3 ✗ 話し合う 4 ✗ 支え合う＝いずれも肯定的な相互行為で、
  子どもに向かない理由にならない」 — one sentence, one axis, three options gone,
  and all four stems N4/N5 under one 〜合う so no N2 vocabulary was tested
  either. Read the 解説 as the author's own confession here: three ✗ in one
  sentence is a claim that three options die for one reason.
  `check_goi_option_set_valence()` now reports that shape, and the register
  half is measured in `moji-goi.md` §"The REGISTER floor" — but the gate only
  sees the sentence, so the option set is still yours to judge. The repair is
  a re-draw (`--reroll-one <cat>:<index>`); accepting a re-written 解説 over
  the same four options is the move to refuse. **問題6's wrong
  sentences are `question-authoring/references/moji-goi.md` §問題6's rule — read
  it there, do not judge them from this file.** This bullet used to restate the
  rule as "each wrong sentence must stay inside the word's own domain", which is
  **refuted**: official 12/2024's 問題6 leaves the target's domain in 5 of its 5
  items (「テレビの音量を薄めた」「空には雲が充実している」「駅のふもとで」「犬の定年」…,
  all verbatim in `refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md`), so applying it
  fails a real sitting. What fails a wrong sentence is that no learner would
  produce it, or that it is a second attested collocation — the owner carries the
  evidence table and the route history (round 1 R6 → round 2 R2-F9, refuted
  2026-08-19). Restating an owner's rule here is what let the two files disagree
  for a whole generation cycle.
- **問1 漢字読み — the TWO-branch distractor rule, every option a REAL word.**
  Each distractor satisfies one of two branches (a reading of the target's
  own/same-component kanji, OR a real N2 word in the same field and form); a
  grab-bag fails both, a non-word is never a distractor. Rule text and shipped
  examples: `question-authoring/references/moji-goi.md`. **When no
  rule-compliant set exists, the TARGET is the defect** — fail the item, send
  it back to `exam-blueprint` to redraw.
- **問1 — the `(漢字, 読み)` PAIR must exist**, underline covering the whole
  word incl. okurigana. Check against Shin Kanzen Master N2-Goi/N2-Kanji and
  日本語総まとめ N2 語彙/漢字 (no JSON index exists — read the page or
  corroborate against the archive); a pair with no headword (表外音訓 like
  `領(えり)`) is a **pool** defect — delete and re-draw, never patch the sentence.
- **聴解問題1-3:** for every wrong option, find the script line that raises
  it — no line means fabricated, FAIL (same check as step 4, worth repeating
  here as a plausibility defect too).

### 2.5. Level band (N2 only — not N1, not N3–N5)

Tested items (問題1–9 keys, 問題5's hard word, 聴解 即時応答 idioms) must sit
inside the N2 band. TOO_HARD (N1) → replace with N2, keeping
`answer_positions`; TOO_EASY (N3–N5) → replace with a real N2 discrimination.
`level_band_grammar.txt` (TOO_HARD/TOO_EASY/ALLOW) covers the string-decidable
half; this step owns the judgment calls (vocab keys, 問題5 hard words, 読解
questions that only test N5 fact-lookup).

Per 問題7–9 key (spot-check 問題1–6/即時応答): (1) name the form actually
tested; (2) ask both directions — would Shin Kanzen N1 claim this? Would an
N3-or-easier book headline it? Either yes fails it; (3) cross-check the hard
side against `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-*.pdf`'s TOC/index; (4)
distractors may show off-level forms only when morphologically/
collocationally impossible in the stem; (5) passive N1 exposure in 読解/聴解
prose is fine when glossed — it must not be what the question keys on.

**The vocab half is entirely yours** — no gate has ever checked a 問題1–6 key,
and no vendored corpus exists to script one against (`openjlpt` deleted
2026-08-11). Check every key against Shin Kanzen/Soumatome and write the
result in the report: a headline N3-or-lower textbook item not in either N2
volume is **TOO_EASY** (賢い/かしこい; also basic verbs like 治す/なおす,
katakana sets like スカート/ジャケット/セーター — `20260811_1` shipped all
three shapes in one paper). This binds the OPTION SET as a whole too — four
basic N4–N5 adverbs (めったに/なかなか/とても/ちっとも) is TOO_EASY even if the
key alone might survive a lookup. **This is a judgment call, not a lookup
verdict** — `openjlpt` mislabeled ordinary N2 vocabulary (把握, 審査, 依頼…)
as "N1"/"N3", so a single source's label was never sufficient.

### 3. Mechanical reads

- **文字・語彙 stems — two counts, thirty seconds, and no gate can see them on
  one paper.** Before solving, count (a) how many of the fifteen 問題1/2/5 stems
  carry no 「、」 and (b) how many of the twenty-five 問題1–5 stems are in
  です・ます, and compare against `moji-goi.md` Part 0 §"The stem" (author: ≥9 and
  7; official runs 47–93 % comma-free and 2–11 polite). Fourteen papers shipped a
  問題1/2/5 stem median of 29 chars against an archive maximum of 21.5, and six
  shipped no comma-free stem at all, through four fresh-eyes QA rounds — because
  nobody counted. Print both counts in the report.
- **A re-drawn key's BAND is a named QA question, not the author's silent
  judgment.** Every tier-C repair (`--reroll`/`--reroll-one`) lands in the report
  as 「key X drawn, band checked against <book, page>」, and this pass reads that
  line. No gate checks vocabulary band (`moji-goi.md` Part 0 §"The KEY must be
  N2"), so an unstated band check did not happen.
- **問題7 stems — measure the DISTRIBUTION, both directions.** The three
  binding numbers are `question-authoring/references/bunpou.md` §問題7's (mean
  inside 36–52 JP chars, ≥2 stems under 34, max−min ≥25); compute all three
  and print them in the report, never just the mean. This bullet stated the
  rule as a floor only until 2026-08-19, and all 12 papers on disk answered by
  optimising the floor: means 47.7–57.4 and **zero** stems under 30, against
  official 7/2025's 26 and 12/2025's 23. Repair by compressing stems, not
  lengthening them. Also fail zero dialogue/setting-label stems in the set
  (official always has a few).
- **問題8/9 length:** 問題8 shouldn't read as three-word drills; 問題9 cloze
  body should land ~500–700 JP chars, not a 150–200 char stub.
- **読解 apparatus & formatting** (bar: `refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`):
  gate WARNs below **25** in-body `（注N）` across 問題10–13 (floor; target
  ~30–40, `dokkai.md`). 問題13's gate floor is **≥800** JP chars (dokkai.md).
  Fail zero `（中略）` anywhere in 中文/長文. Count **in-body markers**, not raw
  occurrences (each gloss also has a definition line — occurrence-counting
  nearly doubles the figure; a gloss count exceeding in-body count means
  orphaned definitions). **Fail glossing basic N3–N5 or standard N2 words**
  (選択, 信号, 技術, 文化, 質, 準備, 手順, 設計, 現象, 経由, 偏り, 維持, 継続,
  前提, 細部, バランス) or trivial circular definitions — notes target
  N1+/rare/literary/specialized terms or contextual metaphors only. **Fail
  any `<ruby>` in `言語知識・読解.md`** — N2 kanji get no furigana; over-level
  terms use `（注N）` only. **Fail mismatched passage markers** (`①`/`②`) — every
  marker must match 1-to-1 with a question stem in that block, and the span
  it bolds must be the same characters as the stem's quote, pointer-sized,
  with any `（注N）` outside the bold (`dokkai.md` §"Marked-span quoting";
  gated, but read the span against the key too — a bold long enough to cover
  the reasoning has already answered the item).
- **問題11:** 4 passages × 2 questions, instruction `(1)から(4)`. No per-pair
  事実/考え pairing requirement (the archive doesn't support one — stem-shape
  rules and the paper-level 考え/主張 floor live in `dokkai.md`). Every
  `（注N）` term must occur in that passage's body.
- **問題2 表記:** confirm the 2×2 shape `{A,B}×{C,D}→{AC,AD,BC,BD}` (e.g.
  {下,不}×{品,晶}→下品/下晶/不品/不晶). Pseudo-compounds are valid; fail an
  arbitrary 3rd kanji breaking the grid or a non-standard glyph. For
  single-kanji-with-okurigana stems, all 4 options share the okurigana and
  use real radical/homophone sets. Fail any stem whose kana matches none of
  the options' readings (unanswerable as printed).
- **問題3 語形成:** every option must be a real, standard, productive affix of
  the same functional family. Fail a nonsense affix (迷〜; the real four
  negations are 非/無/未/不). **Official does NOT require all four to attach to
  the stem** — official's 教育 item offers 則/理/論/規 beside the key, and only
  教育観 attaches (`question-authoring/references/moji-goi.md` §問題3, the
  owner, which carries the rule and this example). Until
  2026-08-19 this bullet demanded plausible attachment to THIS stem, directly
  contradicting the owner; a paper cannot satisfy both.
- **問題4 文脈規定:** every stem must carry a （　）blank. A key word printed
  in the stem itself is trivially answerable — fail it.
- **読解 length/predictability:** the per-item option-length ratio is
  `dokkai.md` §"Option length balance"'s, and **this file must not restate the
  number** — it is WARN above 1.65 / FAIL above 2.50, measured on **printed**
  length over **問題10–13 only, 問題14 exempt**. This bullet read "all 20 items
  (52–71) satisfy `max/min ≤ 1.30` JP chars" until 2026-09-03, i.e. it kept the
  clamp the owner had **withdrawn on 2026-08-21 for failing 34.3 % of official
  current-era items** — wrong threshold, wrong metric, wrong scope, in the file
  the reviewer reads. `20260903_1` (ratios 1.06–1.36, worst 1.36) would have
  been failed on items 64/66/69 by a rule official itself fails. Read the number
  from the owner every time. **Two longest-key rates, both gated** — (tied-)longest
  ≤35 % (official 30 %) AND **uniquely** longest ≤30 % (official 20 %); rank
  varied across items. Check the uniquely-longest one by hand: a paper can sit
  inside the tied target while every key is the sole longest option, which is
  what nine of eleven shipped papers did (dokkai.md §'読解 keys' rule 2).
  **読解 paraphrasing:** every key in 52–69 must be genuinely paraphrased (no
  LCS ≥15 chars and ≥50% of option; no LCS ≥20 chars; no pure lifts).
- **聴解 length/predictability:** the key must not be findable by length in ANY
  section — whole-section uniquely-longest rate ≤35 % (official 28 %), median
  key ÷ distractor-mean ≤1.15 (official 1.00). Both gated
  (`check_choukai_longest_key_rate`). Read the option sets for the shape that
  caused it: short topic labels against one full-proposition key
  (choukai-items.md §'Key length carries no information').
- **模範解答 ↔ 問題冊子:** `詳細解説.json` stores its own copy of every option and
  `build_model_answer.py` PREFERS it over the booklet, so a rewritten option
  leaves the model answer explaining wording the paper does not contain — 722
  options were stale at once (`check_model_answer_option_sync`). Whenever an
  option changes, re-sync the `options` array AND any 解説 prose quoting it.
- **問題14:** the answer must combine **≥2** constraints (never single-field);
  every scenario detail the question references must be describable from the
  source as printed — fail an invented detail (a role the flyer never names).
- **問題5 言い換え:** swap the option into the stem; the sentence must survive.
- **問題8:** splice stem+options in 解説 order, read end to end, no word
  twice. Then try each option in each other slot — a floating adverb that
  reads naturally in two slots is two ★ answers.
- **問題8 — a subject/topic-marker card (裸の「が」/「は」止まり) can double-bind
  by zero-anaphora; `verify_scramble.py`'s `free_unit_count()` cannot see this.**
  When the 解説 excludes a rival ordering by asserting "card X's only possible
  predicate is the verb inside card Y", write down EVERY card that contains a
  verb/predicate X could bind to — including the FINAL card — before accepting
  that claim. Japanese zero-anaphora lets a が/は-marked subject serve as the
  covert subject of a LATER clause too, not only the nearest one: `20260827_2`
  問題8-47 keyed 彼のような→温厚な人が→感情的になったとしても→声を荒げるなど
  あろうはずがない (★=2) on the claim that 「温厚な人が」's only predicate is
  「なった」 inside the としても-card — false, because 「温厚な人が」 equally binds
  to 「あろうはずがない」 in the final card, making 感情的になったとしても→彼のような
  →温厚な人が→…あろうはずがない (★=3) an equally grammatical, equally natural
  rival (concessive としても-clauses routinely precede their own subject via
  zero-anaphora, e.g. 「疲れたとしても、彼は休まない」). This is the
  TWO-FREE-PRE-PREDICATE-UNITS defect (`bunpou.md` §"At most ONE card may be a
  FREELY-ORDERABLE PRE-PREDICATE UNIT") in a form `free_unit_count()`'s
  string-merging cannot catch, because it folded the subject block and the
  concessive card into one chain on the strength of the same now-refuted claim
  (`FREE UNITS: 1` was printed; the true count is 2). A 解説's per-card proof is
  only sound if it tested the final card as a candidate host too, not just the
  nearest one (`qa-report-20260827_2.md` F1).
- **問題9 cloze:** read stem+option aloud as one sentence, all four options.
  Name each blank's category (論理接続表現/文末モーダル表現/内容推論/慣用・
  形式名詞); fail if two+ blanks share a category, or if none requires
  tracking the whole passage. **Fail any option reading like a 読解 paraphrase**
  (20+ chars, thesis summaries) — official options max 14 chars.
- **問題1 漢字読み:** bold span covers the entire word incl. okurigana, never
  bolding surrounding particles. All four options share the exact printed
  okurigana (never leaking the answer by varying it). Confirm the 2×2
  on-reading matrix (矛盾 {む,ぶ}×{じゅん,じゅう}); fail arbitrary 3rd
  endings. All four options are the target's word form, each a real word or
  valid 清濁/長短 derivation, and none uniquely selected by conjugation/
  okurigana (cover the kanji, keep okurigana visible — if only one option
  still fits, fail it).
- **One grammar point, one KEY per paper — as a count, not as "exposure".**
  No form may be keyed twice across 問題7/8/9. Then, for each 問題7/8/9 keyed
  connective or modal, `grep` it across 問題10–14: **at most ONE occurrence in
  the 読解 prose, and never in the same syntactic frame as the stem.**
  `20260817_3` keyed 「そうとは限らない」 at 問題9-51 while 問題11(4) printed
  「〜とは限らない」 in the identical 文末 frame, and keyed 「ところが」 at
  問題9-48 while the prose used it 3×. Until 2026-08-19 this bullet said only
  "check the keys against the running text", with no statement of what a hit
  was — so it was unactionable and got skipped. A 連体 use of a form keyed in a
  文末 frame (「姿を消したはずの種が」 against a keyed 「〜はずだ」) is not a hit.
  **Count （注N） gloss DEFINITION lines as 読解 prose, and re-run this grep after
  every prose repair, however mechanical.** `20260903_1` cleared a
  byte-identical-gloss FAIL by rewording 問題11(1)'s （注3）変遷 to 「時代が進む
  につれて、少しずつ変わっていくこと」 — which planted 問題8-44's keyed
  「〜につれて…ていく」 in its own frame (Nが V-るにつれて → gradual change → ていく),
  in a line printed in the booklet, at a stage that re-ran `make check` (blind to
  frames, it prints 1 ≤ 1 and passes) but not this read. A repair whose whole
  point was one gate check is exactly the repair nobody re-reads against the
  other rules: after ANY edit to 問題10–14 prose, glosses included, re-grep all
  問題7/8/9 keyed forms.
  **Three exclusions, written down 2026-09-04 (`qa-report-20260904_1` S4)
  because the rule's scope phrase — "keyed connective or modal" — did not
  decide them, and an undecided clause is one a reviewer settles differently
  every time:**
  1. **Scope is connectives and 文末 modals. 授受・使役・受身 auxiliaries are
     out of scope.** 〜てくれる/〜てもらう, 〜させる, 〜れる/られる are the grammar
     every Japanese paragraph is built from; counting their occurrences
     measures prose volume, not a leak.
  2. **A form carried by TWO OR MORE of the item's own options carries no
     discriminating information, so its exposure is not counted.** 問題9-51
     keyed 「もう一つ用意してくれる」 while its own distractors 1 and 3 read
     「決めてくれるだろう」 and 「一つに絞ってくれる」 — three of four options on one
     form, so nothing in the prose can push a reader toward the key.
  3. **The scan covers passage PROSE and （注N） definition lines only — never
     another 大問's option strings.** 問題9-49's 「はずだ」 turning up inside a
     問題10/問題11 OPTION is a distractor sentence written for a different item;
     it does not help anyone read the passage this item hangs on.

  All three were re-verified against `20260904_1` on 2026-09-04 and **none of
  them flips its verdict**: over `dokkai_closing_scopes()`'s passage prose plus
  the （注N） lines, 〜てくれる occurs **once** outside 問題9's own passage
  (問題10(1) 「…知らせてくれる。」) and 「はず」 **zero** times, so 問題9-51 and
  問題9-49 sit at ≤1 with the exclusions and without them. An exclusion that
  DID flip a verdict would have to be argued on the merits before adoption —
  these are written down because they were already true, not to buy a pass.
- **Grep each 問題9 keyed 文末 modal across 問題10–13 prose too, not just the
  connectives.** `20260903_1` keyed 「のも当然だろう」 at 問題9-51 while 問題12(A)
  printed 「見直しが進んでいるのも当然だろう」 — same 文末 frame, same 問題9 slot as
  the `20260817_3` 「〜とは限らない」 incident, and the paper even carries
  「とは限らない」 as 問題9-51's own distractor. Two papers on one class: the shape
  is a 文末 modal, and 問題9's 文末モーダル blank is where it recurs.
- **Every sentence is Japanese** — read the whole paper aloud once, watching
  for broken constructions (especially inside CORRECT options).

### 4. 聴解 structure

- **Read the セクション構成表 in `聴解.md` as COLUMNS, before any item** — the
  table and its per-section quotas are `question-authoring/references/choukai-items.md`'s.
  Fail on: the same 正解 twice in a section; one 消去方法 more than twice; one
  主導 pair on more than two rows (§場面 — and read synonymous pairs together,
  which the gate's string tally cannot); any quota breached. **A missing table is itself a fail.** Verify the table
  against the script, not on trust — an author who filled it in wrongly is
  exactly the author whose section repeats.
- **Three columns the gate reads as counts, so read them the same way**
  (added 2026-08-21, REPORT-CHOUKAI.md §F1/§F2): `質問型` — no more than 3 of 6
  on one frame, and at least one modify/method and one condition-match item;
  `決め手の位置` — no more than 3 of 6 rows in any one third (冒頭/中盤/終盤),
  and each cell must print the 「n行目／全m行」 the label is derived from, which
  the gate now recomputes and re-counts against the script
  (`choukai-items.md` §決め手の位置 owns the formula — `20260903_1` shipped two
  labels wrong under every denominator, behind a compliant tally);
  `提案消去回数` — at most 2 items carrying ≥3 proposal-and-deny turns. All
  three shipped as monocultures behind a green gate: 70 of 70 問題1 items asked
  「この後まず何を…」, and the newest three papers put 14 of 15 deciders in the
  first third *because* the rule against "always last" had no other side.
  A paper also needs **one non-dialogue item** somewhere (announcement,
  留守番電話, automated menu — 16% of official 問題1) and **≥1 casual 問題4
  stimulus**, ideally 5 of 12.
- **同じ大問の二項目が同じ決め手の種類で決まっていないか——場面・正解・質問型が
  違っても、決め手が同種なら受験者は同じ聞き取りを二度させられている。構成表の
  決め手列を縦に読むこと。** The 問題1/問題2 構成表 carries a `決め手の種類`
  column drawn from a closed nine-token list, capped at 2 rows per 問題, 例
  counted (`choukai-items.md` §決め手の種類). No gate can re-derive it — the
  column is the artifact, and a section without it is as unshippable as one
  without the table. `20260819_1` 問題2-1番 and 問題2-3番 both decided on *a
  diner who cannot eat something* while differing in 場面, 正解, 質問型 and
  theme tag (食 vs 働き方), which is why no other column and no check saw it.
- **問題3: read the twenty-odd SPOKEN options as one column and look for a word
  only the keys carry.** A content token that occurs in two or more of a 大問's
  read-aloud options and is the key EVERY time is a lexical signature — the
  candidate who spots it answers both items without understanding either talk.
  `20260904_1` spoke 「そのまま」 in exactly two of 問題3's 24 options, 3-1番's
  option 3 and 3-5番's option 1, both keys, zero distractors, and both talks ran
  the same arc (「以前は加工していた → そのまま通した → そのほうが効いた」). Repair by
  RE-ANGLING one item's key, never by giving the word to a distractor, and move
  the `logs/topics.json` surface record with it (§"A fix that changes WHAT a
  surface tests"). `check_choukai_key_exclusive_token()` reports this for 問題3;
  it is deliberately not run over 問題4, where the same predicate flags official
  7/2022's reply formulas. Rule and measurements:
  `question-authoring/references/choukai-items.md` §問題3.
- **The セクション構成表's own 引用規約 binds its CELLS, and now something reads
  them.** `check_section_table_quotes()` matches every 「…」 in a 構成表 table row
  against the current script — the key-table quote scan stops at the 構成表
  heading by design, so until 2026-09-04 the audit table was the one artifact
  quoting the script that nothing verified, and `20260904_1` shipped
  問題2-4番's 決め手 cell missing the script's 「なんですよね」
  (`qa-report-20260904_1` F7/S3). The free-text paragraphs UNDER the tables are
  out of scope on purpose (they quote rule names and quotas); reading those is
  still yours.
- **Read the first and last spoken line of each item in a column too** — if
  openings/closings rhyme, the section is a template (`choukai-audio`
  §"Banned formulas"); the gate only catches *identical* closers >4 chars.
- Question type matches the 問題: 何をしますか in 問題1, どうして/何が一番 in
  問題2, 何について in 問題3.
- **Every 問題1-3 wrong option must be grounded in the script** — find the
  line that raises each distractor (mentioned then reassigned/superseded/
  denied). An option nobody says is fabricated noise — fail it.
- **Every 例 is answerable from its printed options, AND the announced number
  is what the dialogue supports** (`choukai-audio` owns the full rule) — the
  marksheet's pre-marked 例 must equal the announced number; `make check`
  compares them, the dialogue-supports-it half is yours.
- 即時応答 keyed replies must match the speakers' keigo direction
  (`question-authoring`).
- **Narration ↔ voice ↔ `SPEAKER_MAP`:** 「女の学生」 must not be spoken by a
  male-mapped label (`choukai-audio`). Wrong options must each be raised and
  DENIED — a second true statement is a second answer.

### 5. Whole-paper and cross-test topic table

Build the table from `jlpt-test-generation` §"One topic, one surface" — one
row per surface incl. each 聴解 item, one column per test (this + two
before). Fail on: any subject twice in this paper (any register); any
subject repeating the previous test; two 聴解 items running the same errand;
the 問題14 flyer sharing a decisive detail with a listening item; check
問題12's A/B theme against the previous tests' 問題12 specifically.

**Also compare the headline-theme SET as a whole, not just 問題12** — build
this test's 5-surface set (問題9/12/13/14, 聴解問題5's both items) and the
paper-before-last's, intersect them. `exam-blueprint` rule 4 allows **at most
one** repeat across the whole set — checking only 問題12 missed a second
repeat elsewhere in `20260811_1` (問題12 and paper-before-last's 聴解問題5-2番
both landed on 食, on top of an already-permitted 問題13 repeat).

Two columns only a human can judge, both shipped green in `20260810_1`:
- **Theme column, from the SHIPPED passage** — re-tag every 読解 surface from
  what it's actually about, then apply `exam-blueprint` §"The four theme
  rules". Don't trust `test_spec.json` — web seeds/cloze carry no theme, and
  a drafted passage can wander off its pool tag.
- **Closing-move column** — `dokkai.md` §"Thirteen surfaces, thirteen
  different essays". Read each passage's last two sentences, label the move;
  more than two sharing one closing is a finding. Then check whether the
  **keys inherit it** — 6+ keyed options being the same "human/attitude"
  choice beside strawmen is a major finding. **Read the column twice: once
  down the shape labels and once down the SENTENCE SKELETONS.** The cleft
  「〜のは、…だ」 crosses every label, so a paper can show ≤2 per shape and still
  end five of thirteen surfaces on one pattern (`20260904_1` F2; the skeleton
  is now `FINAL_SENTENCE_TEMPLATES`'s 分裂文 row).
- **When a round-1 finding names a PAIR of surfaces sharing a skeleton, round 2
  re-derives the pair on the NEW skeleton AND the NEW shape label — clearing
  the named template is not clearing the pair.** A repair aimed at one template
  moves the writing off that template and lands it somewhere; if both halves of
  the pair land in the same place, the pair survives the repair wearing
  different clothes, and every automated line still reads compliant.
  `20260904_1` round 1 F2 ordered 問題12(B)/問題13 split off 「〜のは…のほうだ」;
  the repair moved BOTH onto 「〜ていた＋のだ／のです」 and left BOTH labelled
  意外な観察 — one pair, re-clothed, two surfaces apart. Neither reading was
  visible to any check: the shared cap is 2 and both sat at exactly 2, which is
  why the 後知れ skeleton now carries a cap of 1 of its own
  (`FINAL_TEMPLATE_CAPS`). **Verification here is by re-reading, not by `make
  check`** — name the two surfaces, quote both new closings, and say which
  skeleton and which label each now carries. This is the third paper on record
  to show the repair-collateral class (`20260812_1` F2→F3, `20260903_1` F2,
  `20260904_1` round-2 F2/F3), so treat every round-1 repair's landing site as
  in scope for round 2, not just the defect it named.

**A refuted candidate metric, recorded so it is not re-derived
(`qa-report-20260904_1` S5, 2026-09-04).** The obvious way to mechanise "the
keys inherit the closing" is to score the strategy *pick the 読解 option
carrying a contrast marker* (〜ではなく / 〜より / だけでなく / こそ / というより /
わけではない). **It is not gateable, for two independent reasons, both measured
over all 29 papers on disk:**

1. **It fails official sittings.** The reviewer's run had `20260904_1` worst
   among generated at 4 of 5 marked options keyed (80 %), against official
   7/2025 at **1/1 = 100 %** and 12/2024 at 2/5 = 40 %. A rule that fails a
   real sitting is refuted, not evidence about ours — the same verdict §2b's
   問題6-leaves-its-domain rule got.
2. **It is not reproducible across two honest definitions of "marker", which
   is worse.** Re-run 2026-09-04 during the root-cause pass with a marker
   family taken from `FINAL_SENTENCE_TEMPLATES` and a scope of items 52–69,
   the SAME papers come out differently: `20260904_1` 2/8 = 25 %, official
   7/2025 1/3 = 33 %, 12/2024 0/4 = 0 %, while generated 20260828_2 reads
   5/6 = 83 % and 20260807_1 2/2 = 100 %. Per-paper n is 1–12 options, so the
   percentage moves by tens of points on one reclassified option and the
   ranking of papers inverts between the two runs.

Do not file `20260904_1`'s nine "obvious X, not Y" keys as a defect on this
basis. The finding that survived measurement was the repeated SKELETON (F2),
which is decidable on a fixed 13-final denominator; the marker rate is not.

### 6. Provenance & Spec Blueprint Audit

1. **Target Item Match Audit (問題1–8 & 聴解問題4):** verify every tested item
   matches the EXACT target in `test_spec.json["items"]` — an unrecorded
   substitution corrupts the rotation ledger. Confirm each entry resolves to
   `pools.json` (or `origin: adjunct` + evidence) AND matches
   `logs/ledger.json`'s history entry — editing the spec to match an authored
   substitution makes the gate green over an item never actually drawn.
   Extend this to `listening_scenarios` — map every 聴解 item's narration to a
   drawn scenario; an authored item matching no drawn entry (while another
   drawn entry went unused) is an unrecorded substitution.
2. **Answer Positions Compliance:** all 101 positions match `answer_positions`
   exactly.
3. **Topic Match & Copyright Non-Reproduction:** every 読解 passage/聴解
   scenario written from its OWN assigned entry, not a substituted one; any
   invented flavor detail reads as the author's own N2-simplified invention
   (約4割, never a decimal, never phrased as citing a real source); no
   passage/dialogue copied from `refs/` or an `imported-*` paper.

### 6.5. Root-cause every finding against the skills

**The paper is not the defect; it is the symptom** — every item was written
per `.agents/*/SKILL.md`, sampled by a script, cleared by `check_consistency.py`.
After the findings table closes, ask per finding: *what would have had to be
different in the skills or gate for this to be impossible?*

**Apply the recurrence test first, not as a judgment call.** Count how many
tests on disk show the finding's class, by reading their sources. **Two or
more papers = systemic by definition** — stop calling it an authoring slip.

Assign each finding exactly one root cause:

| Code | Meaning | Fix goes to |
|---|---|---|
| `RULE-MISSING` | No skill forbids it; the author had no way to know | the owning skill |
| `RULE-UNENFORCEABLE` | A rule exists but as unverifiable prose ("keep passages long enough") | the owning skill — convert to a number/procedure |
| `RULE-IGNORED` | The rule exists, is specific, and was skipped | nothing to change; report as process failure (AGENTS.md §0) |
| `GATE-BLIND` | String-decidable, no check exists | `tools/check_consistency.py` |
| `GATE-WRONG` | A check exists and mis-measures, so green was never evidence | the gate, plus re-verify every test that passed on it |
| `PIPELINE-GAP` | Sources right; an artifact wasn't regenerated, or ordering permits staleness | `jlpt-test-generation` + the gate |

`GATE-WRONG` is the most dangerous and easiest to miss — the symptom is
silence. Two live examples: the `（注N）` counter matched both the in-body
marker AND its definition line (9 real glosses reported as 18); the 解説
quote matcher didn't strip inline `（注N）` (five real quotes reported
missing). A miscalibrated check is worse than none — it converts an open
question into false proof.

**Who owns what**:

| Symptom | Owning skill |
|---|---|
| 問題1–6 stems/options/distractors, 問題9 blank categories, 読解 apparatus, 問題14 constraint count | `question-authoring` (+ its `references/*.md`) |
| Which item is tested, answer-position balance, rotation/ledger | `exam-blueprint` |
| 問題-to-question-type mapping, 例 mechanics, printed vs spoken, section counts | `jlpt-exam-structure` |
| Script block shape, narration labels, `SPEAKER_MAP`, pacing | `choukai-audio` |
| Topic freshness, cross-test repetition, pool rotation | `exam-blueprint` |
| Pass ordering, regeneration steps, artifact staleness | `jlpt-test-generation` |
| Booklet/sheet rendering, stem layout, furigana | `exam-app` |
| Anything string-decidable, any row above | also `tools/check_consistency.py` |

**A root cause without a proposed edit is not a root cause** — name the file,
section, and actual sentence/number/check to add. Prefer, in order: (1) a
number/template replacing a judgment call, (2) a construction procedure at
authoring time (a rule verifiable only *after* writing gets skipped), (3) a
gate check when string-decidable. State plainly when a rule can't be
mechanized and must stay human judgment.

**A new gate check must be RUN against the incident that motivated it before
it is committed — a check that would not have caught its own founding case is
not evidence.** Print the founding paper's measurement and paste it into the
root-cause row; if the incident predates the paper on disk, reconstruct the
offending string and run the predicate on it directly. This is not
belt-and-braces: three checks written in the 2026-08-19 root-cause pass shipped
mis-scoped in exactly this way, all from one cause — each was written from the
incident NARRATIVE and never re-read against the rule text it cites.
`check_key_grammar_exposure` claimed 問題7/8/9 and looped over 問題7/9 (R3-7);
`check_dokkai_final_sentence_templates` read 12 finals where `dokkai.md` counts
13 essay surfaces, so 問題12A's closing was never measured (R3-8); and
`check_mondai9_option_reuse` cited a **two**-shared-option incident under a
threshold that fires at three, i.e. it could not have caught the case it was
written for (R3-9). A fourth, `check_note_band`, ran for three papers on a
predicate whose entire history was ten false positives, under a warn name that
stated the *passing* condition (R3-10). The same rule binds a check whose
threshold or scope you CHANGE: re-run it over every paper on disk and state
which ids move, so a widened rule cannot quietly re-classify shipped work.

**Boundaries.** The reviewer *proposes* skill edits, never applies them to
generation skills mid-review. The one file the reviewer may edit directly is
**this one** — when a defect class is absent from this skill, add it
immediately, with the shipped example named.

**Effect on the loop.** A paper may reach `QA: PASS` with skill findings still
open — the paper is fixed, which is what PASS means. But an open
`RULE-MISSING`/`RULE-UNENFORCEABLE`/`GATE-BLIND`/`GATE-WRONG`/`PIPELINE-GAP`
finding **blocks the next generation run** — it will reproduce it. Each must
be applied, or explicitly rejected with a reason, before a new test is authored.

### 7. Report (required format)

Without the report the review didn't happen. In this order:

1. **Verdict line:** `QA: PASS` or `QA: FAIL (<n> findings, <m> automatic)` —
   PASS only writable when steps 0–6 all ran on all items and zero findings
   remain open.
2. **Blind-solve diff:** which file you solved from, then reviewer's answer
   vs key for every mismatch, resolved as reviewer error (with the deciding
   quote) or filed as a finding.
3. **Per-question walkthrough — all 101 items, one row each, no exceptions**
   — this is what *proves* the review happened, not the findings table.
   Paper order (1–71, then 聴解 例/1番…, 問題5 質問1/質問2):

   | Column | What goes in it |
   |---|---|
   | 項目 | item number and 大問 (`問題7-38`, `聴解問題2-4番`) |
   | 鍵 | the key as shipped |
   | 判定 | `OK` / `要修正` / `自動不合格` |
   | どこが問題か | non-OK: file+line and the exact wrong string. OK: the deciding quote |
   | どう直すか | the concrete repair, appliable without re-deriving it |

   `OK` rows without a quote mean the item wasn't actually checked. Write the
   walkthrough BEFORE the findings table — findings are extracted from it.
4. **Findings table:** item, class, evidence quote, fix applied or reason left open.
5. **Root-cause table (6.5):** finding id, root-cause code, how many tests
   show the class, owning file, concrete proposed edit — group rows sharing
   one root cause (ten items on one missing rule is ONE skill defect).
6. **Coverage statement:** which steps ran on which files, the topic table
   itself, every `make check` WARN with its resolution (including any
   determined a false positive — that's a `GATE-WRONG` finding).
7. **Skips:** anything not done, stated explicitly, with why (AGENTS.md §0.7).

**Where the report goes:** `qa/qa-report-<test_id>.md`, one per test,
overwritten on each re-review, with the reviewed revision's `sha1`s
(言語知識・読解.md, 聴解.md, 聴解スクリプト.txt) and timestamp at the top.

**The sources must be still** — check mtimes before starting and again
before writing; abort if they moved (another context is mid-repair, and every
row is a claim about a byte offset).

Only after PASS may the test be committed or served. A FAIL report goes back
to the author with the findings table as the work list, and the root-cause
table to whoever touches the skills next.

## Relationship to the other gates

`make check` proves the mechanical contract (keys parse, positions match,
options distinct, script shape). This skill proves the CONTENT: one
defensible answer, sources supporting their keys, a paper that doesn't repeat
itself. Neither substitutes for the other (stages 3 and 4 of
`jlpt-test-generation`).

**A green "keys match test_spec.json answer_positions" line is ZERO evidence
about which option is actually correct** — it only compares the digit in the
正解 column with the digit the sampler reserved for that slot, so a key
written to satisfy the spec rather than the passage goes green on a mis-key
BY CONSTRUCTION (`tests/3`'s 聴解問題1-1番 keyed 4 while its own 解説 tagged
option 3 as 正解, and the position check passed). Nothing in the gate reads a
問題1–6 vocabulary key's level either. Step 1's key-by-key proof and step 0's
blind solve are the only things that establish a key at all.

The gate has **one** thing to say about correctness: `check_choukai_kaisetsu_keys()`
fails a 聴解問題1–3 row whose 解説 marks a different option `○`/（正解） than
the 正解 column names. It's silent wherever grounding lines weren't written —
its silence proves nothing, but when it speaks, start there.

It also proves the **generator**, via step 6.5 — the only pass that reads a
finished paper against every rule that produced it. When QA finds a defect
class this file doesn't list, add it here AND, if string-decidable, to
`tools/check_consistency.py`; when it finds the cause elsewhere, file it in
the root-cause table with the concrete edit. A check that mis-measures counts
for less than none — it makes green look like proof.
