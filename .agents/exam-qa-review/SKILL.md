---
name: exam-qa-review
description: Single owner of the adversarial QA pass that every generated test must survive BEFORE it is served or committed. Use after `make check` is green on a new or repaired test, whenever the user asks to review/audit/QA a test, and whenever another agent (any harness, any model) reports a test as done. A green gate is the entry condition for this skill, not a substitute for it — every defect class listed here shipped through a green gate at least once.
---

# Exam QA Review (adversarial pass)

## Why this skill exists

Tests can ship with `make check` green if QA is skipped. The generator model
optimizes what is checked; everything unchecked drifts, in the same four
failure modes every time:

1. **No self-reconciliation.** An authoring run keyed a 聴解 option naming 点検作業員
   where the script says 管理事務所, and its 解説 quoted five lines the audio
   never speaks — options written before the dialogue settled, never
   reconciled after.
2. **Fluency beats discrimination.** Four plausible words *look* like an option
   set, so すなわち shipped as a distractor for つまり — the same word. An item can end up
   with two defensible answers if distractors are not properly discriminated.
3. **Late-file degradation.** Defects cluster in whatever was generated last
   (e.g., the listening half); weight the end of the paper at least as
   heavily as the start.
4. **The skills themselves are defective.** Reviews of generated papers have found
   several defect classes present across papers — ungrounded
   聴解 distractors, low `（注N）` gloss counts against official baselines, 問題6
   domain-violation distractors, single-field lookups in info-retrieval, passages
   under band, among others. QA's output is **two** work lists: the paper's
   findings, and the skill defects behind them (step 6.5).

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
  AGENTS.md §5 makes authoring-vs-QA the one non-negotiable split even in the
  worst fallback; a context that wrote any part of the paper re-reading it from
  disk is still the author auditing its own intent — the setup every defective
  test shipped through.
- **Blind-solve before reading the keys — from the keyless render, step 0.**
  Do this before opening any file under `tests/<id>/` — a key you have seen
  cannot be un-seen, and it anchors every judgment after it. The procedure is
  executable; run it exactly:

  1. `make keyless <test_id>` → `qa/<test_id>/keyless.md`: the whole
     101-question paper plus `聴解スクリプト.txt`, with the key heading, key
     tables, 解答用紙 grid and 解説 column truncated away by the same
     `strip_key()` that protects `解答.html` (see `exam-app` §"The answer key
     must never be VISIBLE"). The build aborts rather than emit a render that
     still carries a key heading.
  2. **Read that file and nothing else** — not `言語知識・読解.md`, not
     `聴解.md`. Answer all 101 items from it and write the answer list into
     your report draft. 聴解 is solvable from the embedded script; `聴解.mp3`
     carries no keys either.
  3. Only then open the sourced Markdown and diff your list against the keys.

  Every mismatch is a finding — either the reviewer is wrong (fine, say why,
  with the deciding quote) or the item has a second defensible answer or a
  mis-key. Copy the source `sha1`s from the render's header into the report
  header, and rebuild the render when you finish: if the shas moved, a fixing
  pass was editing underneath you and the review is void (see "The sources
  must be still"). **Report which file you solved from** — solving from
  anything else is a skipped step under AGENTS.md §0.7, not a style choice.
- **Entry condition:** `make check` green, and its WARN lines either resolved
  or individually justified. Do not start QA on a failing gate.
- **Evidence or it didn't pass.** Every verdict below is backed by a quoted
  line, a spliced sentence, or a table — never "looks fine". If you cannot
  produce the evidence, the item fails.
- **No sampling. All 101 items, every check.** "Spot-checked and it looked
  good" is a skipped step, not a pass.
- **Any single automatic-fail finding fails the WHOLE test** until fixed and
  re-reviewed. Automatic fails: a second defensible answer; a keyed option the
  source does not state; an unanswerable item or 例; a 解説 quote not in the
  source; a topic repeated within the paper or from the previous test; broken
  Japanese anywhere in stems, options, passages, or script; narration
  contradicting the mapped voice; a spec/paper provenance mismatch; **an
  off-level KEY** (N1-hard or N3/N4/N5-easy — see step 2.5 /
  `question-authoring/references/level_band_grammar.txt`, which covers 問題7–9
  GRAMMAR only, so every 問題1–6 vocab key is on the reviewer: avoid keying
  賢い/かしこい, an N3 headword — check Shin Kanzen Master N2-Goi/N2-Kanji and
  日本語総まとめ N2 語彙/漢字 (`refs/Shinkanzen/`, `refs/Soumatome/`), not a
  vendored corpus (`openjlpt` was removed 2026-08-11); **an option that is not a real Japanese word** (e.g.
  もてあそわる/まねわる/ひるがえわる); **a drawn target for which no
  rule-compliant option set exists** — file it against the draw, not the
  options (e.g., 労わる, step 2b); **a paper whose
  `tests/<test_id>/test_spec.json` carries no `answer_positions`** — the gate
  prints "0 prescribed" and passes, so nothing verifies the 101 keys;
  **a distractor
  eliminable on sight for a reason unrelated to the tested point** — wrong
  part of speech, wrong domain, wrong tone, or an unrelated functional
  category (see step 2b); **a 聴解 distractor not grounded in anything said in
  the dialogue**; **a 問題9 blank testing the same grammatical/functional
  category as another blank in the same passage**; **a 問題7 stem with no
  `（　）` at all, which prints its own keyed answer** (e.g. including
  「社内規定に即して」 or 「入学式にあたって」 in the stem);
  **a 問題1 option set that is not the printed target's word form, or a 問題2
  set that is not the stem's inflected form** — the printed okurigana then
  selects the key on sight (e.g. 効く with せき/こう/さく, or
  こころよく with four ～い options none of which substitutes into the stem);
  **a 読解 distractor eliminable by an absolute quantifier or categorical
  denial** (すべて/まったく/のみ/だけで十分/無関係/存在しない);
  **a 即時応答 prompt with
  no defined responder** — an announcement has no addressee-reply, so the keyed
  "response" is just another announcement (e.g., a 火災報知器 prompt);
  **an orphaned `（注N）` gloss whose term never appears in the passage body,
  or an in-body `（注N）` marker with no definition line** (e.g.,
  「準備（注5）」 with no 注5 at all); **a 問題14 item answerable from a single
  constraint, or referencing a scenario detail (a role, category) the source
  text never describes**; **an artifact older than the source it is built
  from** — `聴解.mp3`/`聴解_チャプター.json` predating `聴解スクリプト.txt`, or
  the HTML predating its Markdown; the audio then speaks superseded text and
  no other gate can see it;
  **apparatus carried over verbatim OR near-verbatim from another test** —
  byte identity is the gate's test, and a few edited characters evade it.
  Compare by similarity, not equality, and compare the passage sentences
  around the gloss too;
  **a 読解 key identifiable without reading the
  passage**, because it is a verbatim 60–110 character lift of a passage
  sentence beside ~25 character distractors;
  **any passage, dialogue, 例, stem, or option copied verbatim from `refs/` or
  from an `imported-*` paper** — `jlpt-test-generation` §Invariants allows reference material for
  calibration only. Check this
  against the imported papers directly, not just test-against-test;
  **a surface's `theme` in `tests/<test_id>/test_spec.json` disagreeing with
  that same surface's `theme` in `logs/topics.json`** — a Stage-3 fix that
  relabels a theme in one file to dodge a same-paper headline collision
  without re-authoring the passage or updating the other file's mirrored
  entry hides the collision instead of resolving it (`20260813_1`'s 問題13 was
  relabeled 医療・福祉 in `logs/topics.json` to avoid a headline clash with
  聴解問題5-2番, while `test_spec.json` still recorded the original
  スポーツ・余暇 for the identical topic string, and the shipped passage's own
  content — スタジアム観戦のバリアフリー化, with zero medical/welfare content —
  never stopped being スポーツ・余暇; the collision the relabel was meant to
  avoid was real and stayed real). No check compares these two files' `theme`
  fields against each other — confirm this yourself before trusting either;
  **a headline theme (問題9/12/13/14/聴解問題5-1番/聴解問題5-2番) repeating the
  immediately-previous generated test's headline theme in ANY slot** —
  `exam-blueprint` rule 4's zero-tolerance clause, which no script checks (the
  only automated cross-test 聴解 check compares SUBJECT strings, not themes;
  confirmed absent from `tools/check_consistency.py` by direct search). Build
  the 6-slot headline theme set yourself from the SHIPPED content (not the
  recorded tags) and diff it against the previous test's own recorded set.
- **An option SET reused from an official paper, even when no line is
  byte-identical.** Compare the *sets* of proper nouns per 問題, against
  `tests/imported-*`, not just the sentences.
- **問題5-2番 printing the deciding attribute beside each option name, or
  printing the four options in a different order for 質問1 and 質問2.** The printing facts (bare names only, one
  shared order, audio-introduction order) are `jlpt-exam-structure`'s
  §問題5 2番 — check against that, do not restate it.
- **A 問題8 item whose keyed order is ungrammatical, or whose option set contains
  a bare adverbial.** (e.g., keying 4→3→1→2 to produce
  「新たな目標を掲げて**きっかけに**」 — a non-sentence). The
  construction rule is the fix, not a review heuristic: no option may be an
  adverb standing alone, and exactly one of the 24 orderings may be grammatical.
- **A 解説 cell that itself declares a distractor ungrounded** — any 「言及なし」/「未言及」/「今回の話ではない」 in
  a 問題1–3 解説 is a confession, not an explanation.
- **`logs/ledger.json` disagreeing with `tests/<test_id>/test_spec.json`, or a
  hand-written `harvest_sha`.**
  Compare the two files field for field, and treat a date-shaped sha as
  fabricated.
- **An item redrawn from a test inside the rotation cooldown.** `sample_items.py`
  keeps `COOLDOWN = 2` and the ledger has the data, but no gate compares draws
  across tests. Intersect the ledger's last two entries
  with this test's, after folding okurigana/kana tails, before trusting the draw.
- **Fix, regenerate, re-check, RE-REVIEW.** Findings are repaired in the
  Markdown/script sources, then booklet HTML + `解答.html` (+ MP3 if the script
  changed) are regenerated and `make check` re-run. Then the changed items AND
  their whole 問題 go back through steps 1–4, and step 5's table is rebuilt if
  any topic moved. **Exception (owned by `jlpt-test-generation/SKILL.md`'s
  stage-4 loop rule): a FAIL round with 3 or fewer findings total may be fixed
  directly, skipping this step's re-review** — the orchestrator applies the
  same rigor as any other fix (root-cause each finding, verify `make check`,
  sanity-read the diff) instead of spawning steps 1–4 again. Fixes introduce
  defects at the same rate as authoring —
  a prior round of repairs was itself re-reviewed and one had to be redone.
  A fix-and-approve in the same breath is a rubber stamp, not a review.
  **A closing-move-shape fix (dokkai.md §"Thirteen surfaces, thirteen
  different essays") is verified by RE-READING the new closing against the
  six named shapes and writing which one it now is — never by `make check`
  turning green alone.** `20260812_1`'s round 1 "fixed" 問題11(4) by swapping
  `ではなく` for `である前に`, which satisfied the mechanized marker check
  (`check_dokkai_closing_reframe()`, itself only a proxy) while shipping the
  identical 主張 shape as two other passages — caught only because round 2 QA
  re-read the closing itself instead of trusting the gate (qa-report-20260812_1.md
  F2→F3). The same standard already applies to distractor fixes; it applies
  here too.
- **A fix that changes WHAT a surface tests (its topic/scenario, not just its
  wording) must also update `test_spec.json["items"]["reading_topics"]`/
  `["listening_scenarios"]` and `logs/ledger.json`'s mirrored entry** — mark
  the changed entry `"origin": "reauthored"` with a `"note"` explaining why
  (`tools/check_consistency.py`'s `check_draw_provenance()` requires this, the
  same evidentiary bar as an `adjunct` row). `20260811_1` re-themed five
  surfaces across two fix rounds to resolve theme-collision findings and left
  the spec/ledger pointing at the original, orphaned draws through an entire
  QA pass — an automatic-fail spec/paper provenance mismatch that a same-file
  re-review cannot see, because the mismatch is BETWEEN files. Check this
  explicitly whenever a fix round changes a topic/scenario, not just when a
  paper first ships.
- **The reviewer does not negotiate the bar.** No waiving a rule because the
  test is "mostly fine", the deadline is close, or the author already ran the
  gate. If a rule here seems wrong, propose the change in the report; apply the
  rule as written to this test.
- **Imported Tests (`tests/imported-*`) Rule:** Do NOT update `logs/ledger.json` for an imported test. Imported tests do not sample from the item pool. For imported tests, skip Step 5 (topic table against past generated tests) and Step 6 (provenance audit). Focus QA strictly on transcription fidelity against source PDFs/audio, booklet-script option sync, and solvability.


## The pass, in order

### 0. Blind solve, from `qa/<test_id>/keyless.md`

Before any other step and before opening any file under `tests/<test_id>/`:

```bash
make keyless <test_id>      # → qa/<test_id>/keyless.md — the paper, no keys
python3 tools/qa_eval.py tests/<test_id> --answers "[1, 3, 1, 2, ...]"  # -> instantly diffs & validates (saves ~70% tokens)
```

Read that file only, answer all 101 items, evaluate answers with `tools/qa_eval.py`. Then open the
sourced Markdown and diff. Full procedure and reporting obligations in
"Ground rules" → blind-solve; the diff is §7 item 2 of the report. Steps 1–6
below all read the keys, so none of them can run first.

### 1. Key-by-key proof (all 101 items)

For each item, find the line in the passage/script that DECIDES it, and confirm
the keyed option restates that line — not a paraphrase of what the author
probably meant. Copy the deciding line into the 解説 cell if it is not already
there (paste, never from memory; `make check` WARNs on quotes it cannot find).

While there: a 理由 question must be keyed to the CAUSE the source states, not
to the measure taken about it (e.g., keying "cut night buses" when
the script gave 運転手不足 as the reason — while another option stated the reason).

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
the mirror failure: a distractor eliminable on sight, for a
reason that has nothing to do with the tested point, so the item collapses
from a 4-way discrimination into "spot the one option that isn't nonsense."

For every item, ask of each wrong option: *"Is this the SAME part of
speech/functional category/domain/tone as the key, competing on the specific
point being tested — or does it die for an unrelated reason before the reader
ever engages that point?"* Evidence, not a feeling:

- **Vocab-in-context/paraphrase/usage (問4-6):** write the functional category
  each option belongs to (degree adverb, regret adverb, coincidence adverb,
  …). If the four options don't share one category, FAIL — e.g. わりに (key)
  with 案の定/とっくに/一段と (none a comparison/degree competitor); まして
  (key) with あいにく/徐々に/たまたま (none a comparative-adverb competitor);
  切実 (key) with 痛快 in the set (tonally opposite, discarded without
  reading). For 問題6, confirm each wrong sentence describes a situation
  inside the word's own domain, merely misusing it — 解消 applied to
  physically discarding a computer, or 把握 personified onto a medicine, are
  domain violations, not collocation traps, and FAIL this step even though
  they are grammatically well-formed.
- **問1 漢字読み — the TWO-branch distractor rule, and every option a REAL
  word.** Each distractor must satisfy one of the two branches (a reading of
  the target's own or a same-component kanji, OR a real N2 word in the same
  semantic field and word form); a grab-bag across unrelated fields fails both
  branches, and a non-word is never a distractor. Full rule text and the
  shipped example strings live in `question-authoring/references/moji-goi.md`,
  which owns the rule. **When no rule-compliant option set exists, the TARGET
  is the defect**: do not invent options and do not argue the set down — fail
  the item and send the target back to `exam-blueprint` to be re-drawn.
- **問1 — the `(漢字, 読み)` PAIR must exist, and the underline must cover the
  whole word, okurigana included.** Check every 問題1 target against Shin
  Kanzen Master N2-Goi/N2-Kanji and 日本語総まとめ N2 語彙/漢字
  (`refs/Shinkanzen/`, `refs/Soumatome/` — `openjlpt` was removed 2026-08-11,
  so there is no JSON index to query; read the relevant page or corroborate
  against the official archive); a pair with no headword (a 表外音訓 like
  `領(えり)` or `線(すじ)`) is a **pool** defect —
  delete the entry and re-draw, never patch the sentence. The underline/bold
  layout rule and its shipped counter-example live in
  `question-authoring/references/moji-goi.md`.
- **聴解問題1-3:** for every wrong option, find the line in the script that
  raises it. If no line raises it, it is fabricated, not a distractor — FAIL.
  (This is the listening form of the same check; do it here as well as in
  step 4, since it is a plausibility defect, not only a structural one.)

If you cannot point to the shared category, the reason it's the SAME kind of
option as the key, the item fails this step — replace the distractor with a
real competitor, do not argue the current one is "close enough."

### 2.5. Level band (N2 only — not N1, not N3–N5)

The paper's **tested** items (問題1–9 keys, 問題5's hard word, 聴解 即時応答
idioms) must sit inside the N2 band; drifting either way is a fail. A TOO_HARD
(N1) key is replaced with an N2 form, keeping `answer_positions`; a TOO_EASY
(N3–N5) key is replaced with a real N2 discrimination. The example lists of
too-hard and too-easy forms live in
`question-authoring/references/level_band_grammar.txt` (TOO_HARD / TOO_EASY /
ALLOW), which `make check` enforces for the string-decidable half. This step
owns the judgment calls the gate cannot see (vocab keys, 問題5 hard words,
"がちだ" vs bare "がち", 読解 questions that only test N5 fact-lookup).

Procedure for every 問題7–9 key (and spot-check 問題1–6 / 即時応答):

1. Name the form the item actually tests (from the keyed option + 解説 gloss).
2. Ask both sides, not one: *"Would Shin Kanzen N1 / a Tettei-N1 list claim
   this?"* AND *"Would this appear as a headed item in an N3 (or easier)
   book?"* If either is yes, the item fails — rewrite, do not argue "examinees
   should know it anyway".
3. Cross-check the hard side against `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-*.pdf`
   TOC / inventory (rasterize when there is no text layer — see
   `question-authoring`). Absent from N2 Shin Kanzen + present in N1 lists =
   TOO_HARD.
4. Distractors may show off-level forms **only when they are morphologically or
   collocationally impossible in the stem** so an N2 examinee can eliminate
   them without knowing the N1/N3 item. Prefer N2-band distractors.
5. Passive exposure to N1 wording inside 読解/聴解 prose is allowed when
   glossed (`（注N）`) or simplified; it must not be what the question keys on.

**The vocab half is entirely yours — check it against the books, not a
feeling.** The band file holds grammar; no gate has ever checked a 問題1–6
key, and (2026-08-11) there is no vendored corpus to script one against either
— `openjlpt` is deleted, and exam-blueprint's pool authority is now Shin Kanzen
Master N2-Goi/N2-Kanji and 日本語総まとめ N2 語彙/漢字 exclusively. Check every
tested key against those two textbooks (`refs/Shinkanzen/`, `refs/Soumatome/`)
and write the result into the report: a word that is a headline N3-or-lower
textbook item and does not appear as N2 in either volume is **TOO_EASY** (e.g.
keying 賢い/かしこい — and just as much an absolute-beginner verb/set-phrase
like 治す/なおす or お金をためる, or a basic katakana loanword set like
スカート/ジャケット/セーター/ワンピース: `20260811_1` shipped all three shapes
in one paper, so do not assume those categories are exempt from this check just
because they are common daily words rather than a single hard vocabulary item).
The check also binds the OPTION SET as a whole, not just the key: a 問題4/問題6
item whose four options are all basic N4–N5 frequency/degree adverbs
(めったに/なかなか/とても/ちっとも — `20260811_1` 問題4-17, QA round 3 F3) has
no N2 discrimination point anywhere in it and is TOO_EASY even if the keyed
word alone might survive a lookup; rebuild the whole set from N2-band adverbs
(あくまで/一概に/まんべんなく/ろくに…).
**This is a judgment call, not a lookup verdict** — when
`openjlpt` existed it mislabeled ordinary, correctly keyable N2 exam vocabulary
(把握, 審査, じっくり, 依頼, 徐々に, …) as "N1" or "N3", so a single source's
label was never sufficient even when a script could produce one. Answer with
step 2's two questions against Shin Kanzen N2 (`refs/Shinkanzen/`), cross-check
Soumatome and the official archive when a call is close. Filing 把握 as
off-level because one source said "N1" is the mis-measurement this skill codes
`GATE-WRONG`, and it sends the fixing pass off to break working items.

### 3. Mechanical reads

- **問題7 stem length:** count JP chars on every stem. Official papers average
  ~43 (band ~33–54). Fail the paper if the 12-stem average is under ~35, or if
  more than a couple of stems sit under ~30 — avoid short stem averages (e.g. under ~35 JP chars). Fix by
  rewriting the situation, not by changing the keyed form. Also fail a paper
  whose 問題7 set has **zero** dialogue/setting-label stems (`「…」` turns or
  `（会社で）` etc.) — official papers always include a few.
- **問題8 / 問題9 length:** 問題8 assembled sentences should not read as
  three-word drills; 問題9 cloze body should land ~500–700 JP chars (official),
  not a 150–200 char stub.
- **読解 apparatus & formatting:** using July 2025 as the bar — read it from
  `refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`, the exact PDF text layer. The
  gate WARNs below **25** in-body `（注N）` across 問題10–13 (the floor);
  authoring targets the official band, ~30–40 — bands and rationale in
  `question-authoring/references/dokkai.md`. 問題13's gate floor is **≥800**
  JP chars (all section floors: dokkai.md). Fail a generated paper with
  **no** `（中略）` anywhere in 中文/長文. Count **in-body markers** (one per
  glossed term, in the passage region), not raw `（注N）` occurrences — each
  gloss also has a definition line, so occurrence counting nearly doubles the
  figure. A gloss count exceeding the in-body count means orphaned
  definitions — check both directions.
  **Fail any paper that glosses basic N3–N5 or standard N2 words** (such as 選択, 信号, 技術, 文化, 質, 準備, 手順, 設計, 現象, 経由, 偏り, 維持, 継続, 前提, 細部, バランス) or uses trivial circular definitions. Notes must strictly target N1+/rare/literary/specialized terms or contextual metaphors.
  **Fail any paper containing `<ruby>` (furigana) in `言語知識・読解.md`** — test-takers read N2 kanji without furigana; over-the-level terms must use only `（注N）` notes.
  **Fail any paper with mismatched passage numbered markers (`①**...**`, `②**...**`)** — every numbered marker in a passage must match 1-to-1 with a question stem in that question block (no orphaned/unused markers).
- **問題11:** must be 4 passages × 2 questions with instruction `(1)から(4)`.
  There is **no per-pair 事実/考え pairing requirement** — the official corpus
  does not support one; stem-shape rules and the paper-level 考え/主張 floor
  live in `question-authoring/references/dokkai.md`. For every `（注N）` in
  each passage, confirm the glossed term actually occurs in that passage's
  body — an orphaned gloss fails
  the paper.
- **問題2 表記:** confirm the 2×2 component-matrix shape `{A, B} × {C, D} → {AC, AD, BC, BD}`
  — each of the 4 options should share the compound's two-character skeleton with
  each character position varied independently across the 4 options ({下, 不} × {品, 晶}
  → 下品, 下晶, 不品, 不晶; {運, 雲} × {河, 海} → 運河, 運海, 雲河, 雲海; {下, 不} × {駄, 太}
  → 下駄, 下太, 不駄, 不太). Pseudo-compounds (非語) are standard and valid.
  Fail a set where an arbitrary 3rd kanji breaks the 2×2 grid (e.g. 転海 in 運河's set),
  or where a non-standard / alien glyph appears (banned: `惰楪`'s `楪`).
  For single-kanji stems with okurigana (けわしい → 険しい), confirm all 4 options share
  the okurigana and use real radical/homophone sets ({険しい, 験しい, 検しい, 剣しい}).
  For native compound items (やぬし → 家主), confirm all options use plausible standard kanji
  (家主, 宅主, 宿主, 店主), not nonsensical gibberish like `守柱`.
  Also confirm the stem kana matches the keyed option's reading: e.g. if the stem
  reads しひん but its key 下品 reads げひん, no option reads the stem's kana, so the item
  is unanswerable as printed. Fail any 問題2 stem whose kana matches none of the options' readings.
- **問題3 語形成:** confirm every option is a real, productive affix that
  could plausibly attach to the SPECIFIC stem — not just a plausible affix in
  the abstract. Fail a nonsense affix (e.g. 迷〜, not a real negation
  prefix — the real four are 非/無/未/不) or an option that doesn't suffix
  onto the stem at all (伴い/同行/組み合わせ on 家族).
- **問題4 文脈規定:** every stem must carry a （　）blank for the options to
  fill. Print the answer word in the stem and the item is trivially answerable
  — fail it. If a paper ships 問題4 stems with the key word in the sentence
  (e.g. 「才能ある若手が集まり、**コンクール**で世界一を目指す。」with コンクール = option 2),
  this directly contradicts the paper's own instruction 「（　）に入れるのに最もよいもの」and official sittings, which blank every 問題4 stem.
- **問題14:** confirm the correct answer requires combining **at least two**
  constraints from the table/flyer (never a single-field lookup), and that
  every scenario detail the question references (a role, category, condition)
  is actually describable from the source text as printed — fail a question
  that invents a detail the flyer never mentions (e.g., asking about a
  "補助スタッフ" role the source never described).
- **問題5 言い換え:** swap the option into the stem; the sentence must survive
  (e.g., 「値段の比較的美味しい」 does not).
- **問題8:** splice stem + options in 解説 order; read end to end; no word twice.
  Then hunt the SECOND ordering: try each option in each other slot — a floating
  adverb/adjunct (ほとんど, 直接, 一度…) that reads naturally in two slots is
  two ★ answers.
- **問題9 cloze:** read stem + option aloud as one sentence, all four options.
  Then name each blank's category (論理接続表現 / 文末モーダル表現 / 内容推論 /
  慣用・形式名詞 — see `question-authoring`'s 問題9 rule). Fail the passage if
  two or more blanks share a category (e.g., shipping two connective blanks
  and two content-inference blanks — a repeated pairing that has shipped
  before) or if NONE of the four blanks requires tracking the whole passage's
  argument rather than just the local sentence. **Also fail any option that
  reads like a 読解 paraphrase** (20+ JP chars, 「〜ことにある」 thesis
  summaries, mini-要約 of the passage) — official options max at 14 chars;
  `[内容推論]` changes *what decides the blank*, not option length.
- **問題1 漢字読み:**
  - **Stem underline formatting:** bold span covers the entire word including
    okurigana (`**生じる**`, `**潜る**`, `**逃す**`, `**慌てる**`), never bolding
    surrounding particles (`**に**生じる`) and never leaving okurigana unbolded
    outside (`**生**じる`).
  - **Okurigana consistency & non-exposure:** all four options MUST share the exact
    same printed okurigana (e.g. `生じる` → all options end in `〜じる`, never `〜する`).
    Fail any item where options vary okurigana that is already visibly printed in
    the stem (which leaks the answer on sight).
  - **2×2 Cartesian product matrix for 2-kanji on-reading compounds:** confirm
    {A, B} × {C, D} → {AC, AD, BC, BD} (e.g. 矛盾 {む, ぶ} × {じゅん, じゅう};
    縮小 {しゅく, じゅく} × {しょう, しょ}). Fail arbitrary 3rd endings like `むじん`.
  - All four options are the same word form as the target; each a real word (or valid
    清濁/長短 on-reading derivation); and none uniquely selected by the stem's
    conjugation/okurigana (cover the kanji, keep okurigana visible — if only one
    option still fits, fail it). Same mora count is not required.
- **One grammar point, one KEY per paper** — check 問題7/8/9 keys against each
  other AND against the reading passages' running text.
- **Every sentence is Japanese.** Read the whole paper aloud once. Avoid broken
  sentences (such as 「契約の契約書を解消」, 「互いの条件を歩み寄り」,
  「借りましたCD」, 「代わりに代診」), especially inside CORRECT options.

### 4. 聴解 structure

- **Read the セクション構成表 in `聴解.md` as COLUMNS, before any item.** The table
  (one row per item: 場面 / 主導 / 正解 / 消去方法 / 質問型) and the per-section
  quotas it is checked against are defined in
  `question-authoring/references/choukai-items.md`. Fail on: the same 正解 twice
  in a section; one 消去方法 more than twice; any quota breached
  (問題1 counter items, 問題2 「一番/優先」 keys, 問題3 announcements, 問題4
  already-done distractors, 問題5's two types). **A missing table is itself a
  fail** — every defect this step catches shipped past a green gate AND a
  fresh-eyes QA that read the items one at a time, including `20260813_2`'s
  問題1, which keyed 「本人確認書類を提示する」 in both 1番 and 2番.
  Verify the table against the script rather than trusting it: an author who
  filled it in wrongly is exactly the author whose section repeats.
- **Read the first and last spoken line of each item in a column too.** If the
  openings or closings rhyme, the section is a template
  (`choukai-audio` §"Banned formulas"); the gate only catches *identical*
  closers longer than 4 chars.
- The question type matches the 問題: 何をしますか lives in 問題1, どうして/
  何が一番 in 問題2, 何について in 問題3. Ensure question types match section definitions.
- **Every 問題1-3 wrong option must be grounded in the script.** For each
  distractor, find the line that raises it (a task/statement mentioned then
  reassigned, superseded, or denied). An option nobody says is fabricated
  noise, not a distractor — fail it and demand a real one. The per-option grounding artifact this
  reads (the 解説 lines) is defined in
  `question-authoring/references/choukai-items.md`.
- **Every 例 is answerable from its printed options, AND the announced number
  is the option the dialogue supports** — the full 例-answerability rule text
  lives in `choukai-audio`. The marksheet's pre-marked 例 must equal the
  announced number: `make check` compares them, but the dialogue-supports-it half is yours.
- 即時応答 keyed replies must match the speakers' rank (keigo direction — see
  question-authoring).
- **Narration ↔ voice ↔ `SPEAKER_MAP`:** 「女の学生」 must not be spoken by a
  male-mapped label — the casting/gender-voice rule text lives in
  `choukai-audio`. Wrong options must each be raised and DENIED in the audio;
  a second true statement is a second answer.

### 5. Whole-paper and cross-test topic table

Build the table from `jlpt-test-generation` §"One topic, one surface" — one row
per surface **including each 聴解 item**, one column per test (this test, the
two before it). Fail on: any subject twice in this paper in any register; any
subject repeating the previous test; two 聴解 items running the same errand
(e.g., apartment-hunting in both 問題1-4番 and 問題5-3番); the 問題14 flyer sharing
a decisive detail with a listening item; and check 問題12's A/B theme against
the previous tests' 問題12 specifically.

**Also compare the headline-theme SET as a whole, not just 問題12.** Build this
test's 5-surface headline set (問題9, 問題12, 問題13, 問題14, 聴解問題5 — both
its items) and the paper-before-last's own headline set, then intersect them.
`exam-blueprint` rule 4 allows **at most one** repeat across the whole set;
checking only 問題12 in isolation missed a second repeat elsewhere in
`20260811_1` (問題12 and paper-before-last's 聴解問題5-2番 both landed on 食,
on top of the one already-recorded, already-permitted 問題13 repeat) — two
repeats total, one over budget, and neither in-flight `test_spec.json` note
mentioned the second.

Two columns of that table are yours to judge, because no string check decides
either — both shipped green in 20260810_1:

- **Theme column, from the SHIPPED passage.** Re-tag every 読解 surface yourself
  from what the passage is *about*, then apply `exam-blueprint` §"The four theme
  rules". Do not trust `test_spec.json`: web seeds and the cloze carry no theme,
  and a drafted passage can wander off its pool tag (a 「メンタルヘルスと職場」
  entry tagged `睡眠・健康` was authored as a corporate-systems essay). That paper
  shipped five `働き方` reading surfaces against a cap of 2 with every gate green.
- **Closing-move column** — `question-authoring/references/dokkai.md` §"Thirteen
  surfaces, thirteen different essays". Read each passage's last two sentences
  and label the move. More than two passages closing 「〜だけでは足りない、〜こそ
  が要る」 is a finding; nine of ten is what shipped. Then check whether the
  **keys inherit it**: if 6+ keyed 読解 options are the "human/attitude" choice
  beside 「Xさえすれば十分」 strawmen, the section is solvable without reading and
  that is a major finding, not a style note.

### 6. Provenance & Spec Blueprint Audit

Verify `tests/<test_id>/test_spec.json` against the authored paper end to end:

1. **Target Item Match Audit (問題1–8 & 聴解 問題4):**
   - Verify every item tested in `漢字読み` (問1), `表記` (問2), `語形成` (問3), `文脈規定` (問4), `言い換え類義` (問5), `用法` (問6), `文法問題7` (問7), `文法問題8` (問8), and `即時応答` (聴解 問4) matches the EXACT target item specified in `test_spec.json["items"]`.
   - Fail any paper where an author substituted a different target item during drafting — unrecorded substitutions corrupt the rotation ledger.
   - **Check the spec against the ledger and the pool, not only against the paper.** `tools/check_consistency.py` compares paper↔spec, so editing `test_spec.json` to match an authored substitution makes the gate green even when the substituted item was never drawn — a paper has shipped testing an item that `logs/ledger.json` and `pools.json` recorded as a different item, one not even in the pool. For every `items` entry, confirm it appears in `pools.json` (or carries `origin: adjunct` with evidence) AND matches the same test's `logs/ledger.json` history entry.
   - **Extend the audit to `listening_scenarios`.** Map every 聴解 item's narration to a drawn scenario. An item with no matching scenario alongside a drawn scenario that went unused is a substitution — this has shipped as an authored item (e.g. a 家電量販店/冷蔵庫の配送 dialogue) matching no drawn entry while other drawn scenarios went unauthored.
2. **Answer Positions Compliance Audit:**
   - Verify all 101 answer key positions (71 Gengo + 30 Choukai) match `test_spec.json["answer_positions"]` exactly.
3. **Topic Match & Copyright Non-Reproduction:**
   - For every 読解 passage and 聴解 scenario, confirm it was written from its OWN assigned `reading_topics`/`listening_scenarios` entry, not a substituted or borrowed one (see item 1's substitution check, extended to topics).
   - Verify any invented flavor detail (a survey figure, a flyer deadline) reads as the author's own invention, N2-simplified (約4割, not a decimal), never phrased as a citation of a real source.
   - Verify no passage/dialogue is copied from `refs/` or from an `imported-*` paper (`jlpt-test-generation` §Invariants).

### 6.5. Root-cause every finding against the skills

**The paper is not the defect; it is the symptom.** Every item in it was
written by an agent following `.agents/*/SKILL.md`, sampled by a script, and
cleared by `tools/check_consistency.py`. After the findings table is closed,
walk it once more and answer, per finding: *what would have had to be different
in the skills or the gate for this to be impossible?* Fixing only the paper
leaves the generator that produced it unchanged.

**The recurrence test — apply it first, it is not a judgment call.** Count how
many of the tests on disk show the finding's class, by reading the other tests'
sources, not from memory. A class present in **two or more papers is systemic
by definition**: stop calling it an authoring slip and root-cause it.
Examples of systemic findings from QA include: ungrounded 聴解 distractors in
multiple papers; the 問題14 single-field lookup landing on item 71; the
問題5 2番 lead-in spoken aloud though official papers keep it
booklet-only; `SPEAKER_MAP` gender mismatches; a stale MP3; or passage gloss notes being a verbatim copy of another test's notes in the same passage slots.

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
symptom is silence. Two live examples: the `（注N）` counter matched both the
in-body marker **and** its gloss-definition line, so 9 real glosses reported as
18 and every paper cleared a 15-gloss bar that was really 7.5; and the 解説
quote matcher did not strip inline `（注N）` from the source, so five quotes
that *are* in the passage were reported missing — burying the one that
genuinely was not. A miscalibrated check is worse than no check: it converts an
open question into false proof, and it trains the next reviewer to discount
the warning.

**Who owns what** — name the skill by file, not by area:

| Symptom | Owning skill |
|---|---|
| 問題1–6 stems, options, distractor sets, 問題9 blank categories, 読解 apparatus (`（注N）`, `（中略）`, lengths), 問題14 constraint count | `question-authoring` (incl. its per-section `references/*.md`) |
| Which item is tested, answer-position balance, rotation/ledger accounting | `exam-blueprint` |
| 問題-to-question-type mapping, 例 mechanics, what is printed vs spoken, section counts | `jlpt-exam-structure` |
| Script block shape, spoken/booklet split, narration labels, `SPEAKER_MAP`, voice↔narration agreement, pacing, pauses | `choukai-audio` |
| Topic freshness, cross-test/cross-surface repetition, pool rotation | `exam-blueprint` |
| Pass ordering, regeneration steps, artifact staleness | `jlpt-test-generation` |
| Booklet/sheet rendering, stem-line layout, furigana | `exam-app` |
| Anything string-decidable, in any row above | also `tools/check_consistency.py` |

**A root cause without a proposed edit is not a root cause.** For each one,
write the target file, the section, and the actual sentence, number, table row,
or check to add — enough that the fixing pass applies it without re-deriving
it. Prefer, in this order: (1) a number or a template that replaces a judgment
call, (2) a construction procedure at authoring time rather than a check at
review time — a rule the author can only verify *after* writing the passage
gets skipped, (3) a check in the gate when the rule is string-decidable. State
when a rule genuinely cannot be mechanized and must stay a human judgment;
that is a valid answer, and it keeps the next reviewer from assuming the gate
has it.

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
   PASS is only writable when steps 0–6 all ran on all items and zero findings
   remain open.
2. **Blind-solve diff:** name the file you solved from — `qa/<test_id>/keyless.md`
   unless you state otherwise and why — then reviewer's answer vs key for every
   mismatch, each resolved as "reviewer error because …" (with the deciding
   quote) or filed as a finding.
3. **Per-question walkthrough — all 101 items, one row each, no exceptions.**
   The findings table below summarises; this section *proves* the review
   happened, because it is the only artefact that shows an item was looked at
   and cleared. A report that jumps from the verdict to a findings table is
   indistinguishable from a spot-check, and a spot-check is a skipped step
   (§"No sampling"). One row per item, in paper order (1–71, then 聴解
   例/1番…, 問題5 質問1/質問2), each carrying:

   | Column | What goes in it |
   |---|---|
   | 項目 | item number and 大問 (`問題7-38`, `聴解問題2-4番`) |
   | 鍵 | the key as shipped |
   | 判定 | `OK` / `要修正` / `自動不合格` |
   | **どこが問題か** | for a non-OK row: **file and line** (`言語知識・読解.md:149`) plus the exact string that is wrong — never "the key is off". For an `OK` row: the deciding line from the passage/script that proves the key, quoted |
   | **どう直すか** | the concrete repair — the replacement option, the reordered slots, the sentence to rewrite, the target to send back for re-draw. A repair a fixing pass can apply without re-deriving it |

   `OK` rows are not filler: the quoted deciding line is step 1's evidence for
   that item, and an `OK` row with no quote means the item was not actually
   checked. Write the walkthrough **before** the findings table — findings are
   then extracted from it, so nothing can be summarised away.
4. **Findings table:** one row per finding — item, class (from the automatic-
   fail list or "minor"), evidence quote, fix applied or reason left open.
5. **Root-cause table (step 6.5):** one row per finding — finding id, root-cause
   code, how many tests on disk show the class, owning file, and the concrete
   proposed edit. Group the rows that share a root cause: ten items failing on
   one missing rule is **one** skill defect, and reporting it ten times hides
   that. Findings coded `RULE-IGNORED` still get a row, marked as needing no
   skill change.
6. **Coverage statement:** which steps ran on which files, the topic table
   itself (not a claim that you built it), the URLs fetched in step 6 and what
   they returned, and every WARN from `make check` with its resolution —
   including any WARN you determined to be a false positive, with the evidence,
   since that is a `GATE-WRONG` finding.
7. **Skips:** anything not done, stated explicitly, with why. An unstated skip
   is how defects ship (AGENTS.md §0.7).

**Where the report goes.** Write it to `qa/qa-report-<test_id>.md` (create `qa/`
if it does not exist), one file per test, overwritten on each re-review. Name
the reviewed revision at the top — `sha1` of `言語知識・読解.md`,
`聴解.md`, and `聴解スクリプト.txt`, plus the timestamp — because a report
without it cannot be told apart from a report on the *previous* revision.

**The sources must be still.** Do not review a test another context is
mid-repair on: check the mtimes of the three sources before you start and again
before you write the report, and abort if they moved. Every row of the
walkthrough is a claim about a byte offset in a file; if the file is being
rewritten underneath, the report is wrong on arrival, and the fixing pass will
chase items that no longer exist.

Only after a PASS report may the test be committed or served. A FAIL report
goes back to the author (or the fixing pass) with the findings table as the
work list — and the root-cause table goes to whoever touches the skills next,
because the paper's fixes do not change the generator that produced it.

## Relationship to the other gates

`make check` proves the mechanical contract (keys parse, positions match,
options distinct, script shape). This skill proves the CONTENT: one defensible
answer, sources that support their keys, a paper that does not repeat itself.
Neither substitutes for the other; the orchestrator runs them as stages 3 and
4 (`jlpt-test-generation`).

**A green `keys match test_spec.json answer_positions` line is ZERO evidence
about which option is actually correct.** Its label now ends `(slot agreement
only — content correctness is exam-qa-review step 1)`, and that is the whole of
what it claims: it compares the digit in the 正解 column with the digit
`sample_items.py` reserved for that slot, so a key written to satisfy the spec
rather than the passage goes green on a mis-key **by construction** — `tests/3`'s
聴解 問題1-1番 keyed 4 while its own 解説 tagged option 3 「発券機に行こう」→
決定された行動（正解）, and every position check passed. Nothing in the gate
reads a 問題1–6 vocabulary key's level either (`level_band_grammar.txt` covers
問題7–9 grammar only), and its one string-decidable corner — a 問題1 target
whose spelling carries two graded readings — is `check_mondai1_key_band()`, not
a general answer check. Step 1's key-by-key proof and step 0's blind solve are
the only things that establish a key at all; do not let a green positions line
shorten either of them.

The gate does have **one** thing to say about correctness, and it is worth
reading before step 1: `check_choukai_kaisetsu_keys()` fails a 聴解 問題1–3 row
whose 解説 marks a different option `○`/（正解） than the 正解 column names. It
is silent wherever the author did not write the per-option grounding lines, so
its silence proves nothing — but when it speaks, the paper has stated two
different answers for one item and step 1 should start there.

It also proves the **generator**, via step 6.5. QA is the only pass that reads a
finished paper against every rule that produced it, which makes it the only
place the skills get audited at all. When QA finds a defect class this file does
not list, add it here AND, if it is string-decidable, to
`tools/check_consistency.py`; when it finds the *cause* in another skill, file
it in the root-cause table with the concrete edit. Rules only count when they
execute or get read — and a check that mis-measures counts for less than none,
because it makes green look like proof.
