---
name: question-authoring
description: Single owner of how to WRITE JLPT exam items at the correct difficulty — vocabulary, kanji, grammar, reading passages, and listening dialogues, including distractor design and answer-key format. Use whenever creating or revising any exam question, whenever the user says questions "seem easy/hard", or when checking difficulty alignment. Difficulty bugs are the #1 revision cause — consult this before writing a single item.
---

# Question Authoring (N2 calibration)

## File Output & Location (Japanese File Names)

Questions are written to Markdown source files inside `tests/<test_id>/`:
- Language Knowledge & Reading: `tests/<test_id>/言語知識・読解.md`
- Listening Booklet: `tests/<test_id>/聴解.md`

## The golden rule — stay inside the N2 band

Draft an item, then ask **both** sides before keeping it:

1. **"Would this appear as a headed item in an N3 (or N4/N5) book?"** If yes, discard — too easy.
2. **"Would Shin Kanzen N1 / a standard N1 list claim this as an N1 form?"** If yes, and it is **not** in Shin Kanzen N2's inventory, discard — too hard.

The tested point (kanji, word, grammar, idiom) must be something an N2 mock
is allowed to key on. Passive exposure to harder wording in a 読解 passage is
fine when glossed with `（注N）`; it must not be the answer discrimination. Off-level
KEYS are an automatic QA fail — see `exam-qa-review` §2.5 and
`exam-qa-review/references/level_band_grammar.txt`.

Verify every tested word/grammar point against `refs/Shinkanzen/` (N2
inventory) and benchmark sentence structure, distractor density, and passage
length against the official past exam sets in `refs/JLPT_N2_NEW/` (see
`reference-book-reading`). Items drawn with `"origin": "adjunct"` in
`tests/<test_id>/test_spec.json` passed `classify_level.py` — treat them like pool items;
do not swap them for memory picks.

## Benchmark against Official Exams (`refs/JLPT_N2_NEW/`)

Maintain high consistency with the official exams in `refs/JLPT_N2_NEW/` (e.g. 07/2023, 12/2023, 12/2024, 07/2025, 12/2025):
- **Dokkai character counts**: stated ONCE, in the 読解 length-band table under
  「問題10-14 (reading)」 below — that table is the single copy in this repo, and
  `tools/check_consistency.py`'s `check_dokkai_lengths()` is what enforces it.
  Do not restate a band here, in `jlpt-exam-structure`, or in a test's notes:
  three hand-synced copies is why all four papers shipped short 問題11 and
  問題14 while every gate stayed green (G8).
- **Grammar stem lengths (問題7–9) — measured on papers in `refs/JLPT_N2_NEW/`**:
  - **問題7**: official stems average **~43 JP chars** (median ~41; interquartile ~33–54). A paper whose 12 stems average under ~35, or that ships many under ~30, reads as textbook-drill short, not exam-length. Target: **each stem ≥30 JP chars**, **paper average ≥40**, with most items in the **35–55** band. Build length with scene-setting (職場・電話・掲示・インタビュー), a subordinate clause, or a short dialogue lead-in — not by padding the tested form. Official items often open with `(会社で)` / `(電話で)` / a named role before the blank.
  - **問題8 (文の組み立て) — length is mostly in the OPTIONS**: measured on
    `refs/JLPT_N2_NEW/` papers + the official 2018 sample (`jlpt.jp` N2G.pdf) and the
    clean import `imported-n2-2025-07`:
    - **Sum of the four options** typically **16–29 JP chars** (July 2025 items
      sit ~16–29; sample 2018 has chunks like「山を下りて何日かすると」「二度と
      したくないと」).
    - **Per option**: mix is fine (a 2–3 char particle next to an 8–12 char
      clause), but **≥2 options must be ≥5 JP chars**, and the longest should
      usually be **≥7**. Four scraps of 2–4 chars (`わりに/ケーキは/とても/値段の`
      — test 1) read as textbook drills, not N2 scramble chunks.
    - **Assembled sentence** (stem frame + four options) **≥45 JP chars**;
      prefer ~50–75. Stem context before/after the blank run is required when
      options alone cannot fund that length.
    - Prefer **nested/phrase chunks** (thinka/N2 guides: 複文フレーム) over
      isolated particles when the grammar point allows.
  - **問題9**: official cloze passages run **~500–700 JP chars** (title + body, excluding the four option lists). Do not ship a 150–200 char mini-paragraph — that is N3 drill length. Four blanks still; the prose around them must feel like a short magazine/column piece.
  - **問題9 — the four blanks must test four DIFFERENT categories.** Before
    writing the four blanks, assign each one a distinct type from this list
    (or an equivalent), then check no type repeats: (a) **論理接続表現** —
    sentence-initial discourse connective (しかし/そのうえ/つまり…); (b)
    **文末モーダル表現** — a modal/inference family attached to the previous
    clause (わけだ/わけがない/わけではない/わけにはいかない, はずだ/はずがない,
    のも無理はない…) — pick ONE such family per paper, not two different
    blanks drawing on the same family; (c) **内容推論** — a full predicate
    that requires tracking the whole passage's argument, not just the local
    sentence, to choose (this is where the "passage-level trap" lives — at
    least one of the four blanks must be this type); (d) **慣用/形式名詞** — a
    set phrase or formal noun (つもり, 元も子もない, 願ってもない…). Test 4
    shipped two connective blanks and two content-inference blanks (four
    slots, two categories); test 2 and test 3 each repeated one pair. Four
    slots, four categories — no exceptions.
  - **問題9 — write each blank's category down; it is required output, not a
    thought.** Category collision shipped in **4 / 4** papers (t1 48/51 both
    副助詞・形式名詞; t2 49/50/51 all sentence-final predicate slots; t3 48/50;
    t4 48/51 both 文末モーダル) *with the four-category rule above already on
    this page*, because a blank's category was written down nowhere — so
    neither author nor reviewer could check it without re-deriving all four.
    Therefore: **each of the four 問題9 rows in the `## 文法` key table must open
    its 解説 cell with the category tag in brackets** — `[論理接続]`
    `[文末モーダル]` `[内容推論]` `[慣用・形式名詞]` — **and exactly one row must
    carry `[内容推論]`.** Use these four strings verbatim: `make check` matches
    them literally and FAILs when the four 問題9 解説 cells do not carry four
    distinct tags including exactly one `[内容推論]`. Example cell:
    `[文末モーダル] 前の文の「…はずだった」を受け、…`. Assign the four tags
    *before* writing the blanks and write each blank to its tag; tagging
    afterwards, to whatever you happened to write, is how t1/t2/t4 ended up
    with two modal blanks. The `[内容推論]` blank is the one whose four options
    are full predicates/clauses and cannot be chosen from the local sentence
    alone (t3's blank 50 is the one shipped example that qualifies).
  - Count Japanese characters only (hiragana/katakana/kanji/JP punctuation); ignore spaces and the `(　)` / `＿＿` / `★` markers themselves when eyeballing, but do not strip scene-setting just to hit a number.
- **Distractor Design**: Distractor options must replicate official confusion logic (e.g. 近義語 nuances, 誤用 collocations, condition disqualifications). See "Distractor plausibility" below — this is not optional polish.
- **Listening Spoken Choice Pacing**: Options spoken in 聴解 must follow official lengths (~10-15 chars per choice in 問題3/問題4).

## Distractor plausibility — the sniff-test rule (governs every section below)

`exam-qa-review`'s two-answer hunt (§2) catches a distractor that is too STRONG
(a second defensible answer). This rule catches the opposite failure, which is
just as real and was never checked anywhere: a distractor that is too WEAK —
eliminable on sight, for a reason that has nothing to do with the point being
tested. Four tests shipped this pattern across 問1, 問4, 問5, 問6, and 聴解問題1
〜3 simultaneously: distractors from an unrelated semantic/tonal/domain
category, discarded by a sniff test rather than by knowing the tested word.

**The test, for every distractor before you ship it:** *"Would a well-prepared
N2 examinee, moving quickly, seriously weigh this option before ruling it out
— for the SPECIFIC reason the item is supposed to test — or does it die on
sight for some unrelated reason (wrong part of speech, wrong domain, wrong
tone, wrong register, not even a competitor in the same functional category)?"*
If it dies on sight, it is not a distractor, it is noise, and the item
effectively becomes a 2-way or 1-way choice. Replace it with a real competitor
in the SAME category as the key:

- **Vocabulary-in-context / paraphrase / usage (問4-6):** every distractor must
  be the same part of speech AND the same functional category as the key —
  e.g. if the key is a comparative/concessive adverb (わりに), every distractor
  must also be a degree/comparison adverb, not a grab-bag of regret (あいにく),
  gradualness (徐々に), and coincidence (たまたま) that share nothing with the
  tested function. If the key is tonally neutral, no distractor may be
  jarringly upbeat or negative (痛快 next to 切実/深刻 is discarded on tone
  alone before the reader engages the meaning). For 問題6, every wrong sentence
  must describe a plausible situation for THAT WORD'S domain — a wrong
  collocation or register, never a domain the word doesn't apply to at all
  (解消 applied to physically discarding a computer, 把握 personified onto a
  medicine, are sniff-test fails, not misuse traps).
- **Kanji reading (問1):** see the existing 問題1 rules in "Item integrity"
  below (same word form, conjugation lock) and the two-branch
  「Same-kanji OR same semantic field rule」 in 「問題1 (漢字読み)」 below, which
  is the single statement of this rule. This bullet adds nothing to it and must
  not be read as narrower: a distractor may be a reading of the same/same-radical
  kanji **or** a real N2 word in the same semantic field. What is forbidden is
  the grab-bag that satisfies neither — いたわる's distractors must not be
  ことわる/さわる/かわる (readings of 断る/触る/代わる: kanji sharing nothing with
  労, fields sharing nothing with "care for"). This bullet said "never readings
  of an entirely unrelated kanji" and so contradicted the section below, whose
  own official examples (辛い → あまい/にがい/しぶい) are exactly that; an author
  reading only this line is left with one branch, and when that branch is empty
  for the drawn target the next step is inventing non-words. Test 4 took it.
- **聴解 dialogues (問題1-3):** "every wrong option must be MENTIONED then
  eliminated" (below) is the plausibility rule for listening — an option
  nobody says in the dialogue is not a distractor, it is fabricated noise, and
  it lets the item be solved without tracking the conversation at all. Every
  wrong option must correspond to a real task/statement/fact from the audio
  that is reassigned, superseded, denied, or reinterpreted — never invented
  from nothing. **The procedure and the required artifact are in 「聴解
  dialogues」 below** (dialogue first, options harvested from it, one
  `N ✗「line」→ reason` line per wrong option in the 解説 cell) — that is how
  this bullet is complied with; re-reading the prohibition is not.

### The functional-category line is mandatory OUTPUT, not a thought

The rule above shipped in **4 / 4** papers anyway, because it asks the author to
*ask themselves* a question: there is no artifact, so a skipped check and a
passed check look identical on disk. The proof: the option set 問5-24 shipped in
test 4 — key わりに against 案の定/とっくに/一段と — was **already named as a bad
example in the skills** (`exam-qa-review` §2b, alongside this file's
まして/あいにく/徐々に/たまたま twin) when test 4 shipped it again. A prohibition
with an example is not enough. So the check becomes a line of text that either
exists or does not:

- **For every 問1–6 item, the `## 文字・語彙` key notes must print the category
  of all four options on one line**, in this shape:

  ```
  24: 程度副詞 ×4 (比較的/非常に/たいして/一段と)
  ```

  One category label, `×4`, then the four options. **If you cannot write `×4`
  after a single label — i.e. the four labels are not identical — the item is
  not shippable**: replace the odd options with real competitors in the key's
  category and rewrite the line. Do not invent a label broad enough to cover a
  grab-bag (「副詞」 over 案の定/とっくに/一段と is such a label; the honest ones
  are 予想副詞/時間副詞/程度副詞, which is three categories and a failed item).
- **For 問題1, print the source of every distractor reading on the same line** —
  `いたわる=労る[N1], ねぎらう=労[N3 kunyomi], ...`, and mark which branch each one
  satisfies (`[同漢字]` or `[同分野]`). **The source is whatever the openjlpt
  lookup returned** — run it, do not write the spelling from memory; the
  procedure, the command, and the 音読み branch (where a non-word option is legal
  if it is a 清濁/長短 derivation) are under 「All four readings must RESOLVE」 in
  「問題1 (漢字読み)」 below. Test 4's set was
  `ことわる=断る, さわる=触る, かわる=代わる`: writing the sources out makes it
  visible in one glance that none of those kanji shares anything with 労 **and**
  that no branch label can be written for any of them. **A distractor with no
  writable branch label must be replaced; a distractor that is not a real word
  must never be written at all** — test 4's "repair" of that set was
  もてあそわる/まねわる/ひるがえわる with invented spellings (弄わる/招わる/翻わる),
  which is a worse failure than the set it replaced.
  **NO GATE CHECKS THIS.** An earlier version of this bullet claimed
  「`make check` WARNs when a distractor reading is not a listed reading of the
  target kanji…」; it does not — `tools/check_consistency.py` touches
  `openjlpt/kanji-n2.json` only to assert the file exists (and in one comment).
  Three invented non-words shipped in test 4 without a single warning. Until that
  check exists (it is on the QA work list as `GATE-BLIND`), the written
  source-and-branch line **is** the check, and it is the author's, not the gate's.

This is a construction-time discipline, not a post-hoc filter: when drafting
four options, draft the key, then draft three competitors from the SAME
category first, and only then check they're each impossible for a specific,
nameable reason (the existing "name the reason each distractor is IMPOSSIBLE"
rule). A distractor that fails the plausibility test and a distractor that
creates a second answer are two ends of the same axis — aim for the narrow
band between them.

## Using web seeds from `tests/<test_id>/test_spec.json` (when present)

If `merge_seeds.py` ran, the spec carries web provenance — honor it in every
section, under these caps (full rules: web-topic-research):

- **Provenance is binding**: entries marked `"origin": "web"` are written
  around that seed; `"origin": "pool"` entries stay pool-topic-based. Never
  swap origins to taste — the 30-60% web / ≥40% pool blend is the point.
- **Tested item ≠ web item**: the kanji/word/grammar/idiom being tested is
  ALWAYS the sampled pool item (Shin-Kanzen-calibrated). Web seeds only set
  the topic, scene, or facts around it.
- **問題1-8 carrier sentences**: at most 1 in 3 stems per 問題 may draw on
  `spec.carrier_seeds`; the rest use neutral settings. Same N2 bar: if the
  seed needs N1 vocabulary to mention, don't use it in that stem.
- **問題4 即時応答**: `spec.qr_situation_seeds` may flavor the setting of an
  utterance; the tested keigo/idiom stays the sampled one.
- **問題9**: follow `spec.cloze_topic` (web or pool as rolled).
- **問題14**: if `spec.info_retrieval_texture` exists, weave its (already
  simplified) numbers into the flyer's conditions.
- **Facts**: max one borrowed fact per passage/dialogue, in simplified form
  (約4割, not 38.6%); never reproduce source sentences or article structure.

## Per-section rules

**問題1 (漢字読み)** — test N2-band words: 交渉, 慌てる, 妨げる, 潔い, 措置,
傾向, 効率, 険しい. Build distractors from REAL confusions:
- reading traps: 措置(そち) vs しょち/そうち; homophone kanji sets:
  納める/収める/治める/修める, 敗れる/破れる; same-radical fakes: 険/検/剣/験.
- **The underline covers the WHOLE word, okurigana included.** In the Markdown
  the underline is the bold span, so write `**収まった**`, not `**収**まった`.
  Official July 2025 (`tests/imported-n2-2025-07/言語知識・読解.md`, 問1) marks
  `**才能**`, `**辛い**`, `**刑事**`, `**起床**`, `**収まった**` — the inflectional
  tail is *inside* the mark in both okurigana items, and 問題2 does the same with
  the kana span (`**しめって**`). Corroborated across the archive
  (`reference-book-reading/references/official_calibration.md` §5, rasterised
  7/2025 and 12/2025 read visually — with §0's caveat that the archive is a
  Word-typeset reproduction, so this is the reproducer's typography, consistent
  across sittings).

  **The defect is splitting a word, not the character count.** Forbidden:
  marking part of a word and leaving the rest outside — test 4 shipped
  `**爆**ぜる`, which asks for the reading of a bare character rather than of a
  word and lets `ばく`/`はつ` compete with `はぜる`. **Legitimate: a whole word
  that happens to be one kanji.** Official draws them — 腕 (12/2023-1), 柱
  (12/2025-1), 針 (12/2012) — and 柱's option set ゆか/かべ/たな is an ordinary
  訓読み semantic-field set. A single-kanji *word* is a normal target; a
  single-kanji *fragment* of a longer word is not.
- **Conjugation lock (読み):** when the stem shows conjugated okurigana, every
  option must fit that conjugation — not a different verb class whose ending
  the print already rules out. Each option must also be a real word. See Item
  integrity below (test 1's 慌てて).
- **Same-kanji OR same semantic field rule:** Every distractor must share the same word form and conjugation class AND be either (a) a reading of the target's OWN kanji or a same-radical/visual-component kanji (e.g. 措置: そち/しょち/そうち, 険しい: けんしい/けんみしい/かんしい/けわしい), OR (b) a real N2 word in the SAME semantic field (e.g. official July 2025 問1-2 辛い → あまい/にがい/しぶい; 問1-5 収まった → さだまった/しずまった/やすまった). A grab-bag of unrelated words across different semantic fields is forbidden. This is the **only** statement of the rule; the 「Kanji reading (問1)」 bullet under "Distractor plausibility" defers to it. **Scope: branch (b) is the 訓読み branch.** For a 音読み compound target (才能, 起床, 概要 — no okurigana printed) official distractors are 清濁/長短 derivations of the key's own on-reading and are *not* words; that branch and its verification are step 6 of 「All four readings must RESOLVE」 below.
- **Build the set BEFORE you accept the target — and reject the target, never the
  rule.** The three constraints (conjugation lock + real word + one of the two
  branches) intersect to nothing for some pool entries, and when they do, the
  target is undrawable, not negotiable. Procedure, in this order: (1) write the
  target's okurigana and the word class it locks; (2) list the target kanji's
  other readings and its same-radical look-alikes in that class → branch (a)
  candidates; (3) if fewer than three, list real N2 words of the same class in
  the target's semantic field → branch (b) candidates; (4) **if (a)+(b) still
  yields fewer than three real words, STOP: report the target as undrawable and
  ask `item-pool-sampling` to re-draw it.** Do not invent a word, do not widen
  the field to "any ～わる verb", and do not ship three near-misses plus filler.
  Worked example of the empty case — test 4's 「労わる」: okurigana locks ～わる;
  労 reads only ロウ/いたわ(る)/ねぎら(う) and no look-alike (栄・営・学・券・努)
  gives a ～わる verb, so (a) = {}; every real ～わる verb (ことわる・かわる・
  くわわる・まじわる・さわる・たまわる・おわる・そなわる・おそわる) belongs to an
  unrelated field, so (b) = {}. The paper shipped invented non-words instead, and
  a *previous* fix round had already shipped the unrelated-kanji set — two
  failures on one undrawable target.
- **All four readings must RESOLVE — look them up, do not judge them.** 「実在語
  のみ」 was already written above and test 4 still shipped `がいり`, `そうじる`,
  `うんじる` (items 1 and 2), because nothing said **where to look**. It is a
  lookup, and it has two branches, because official papers treat 音読み and
  訓読み targets differently. Measured over **all 35 current-era 問題1 items
  (12/2022–12/2025, n = 7 sittings)** —
  `.agents/reference-book-reading/references/official_calibration.md` §5, which
  corroborates the split first read off July 2025 and refines it:

  | Target | n | What the distractors are |
  |---|---|---|
  | **訓読み** (okurigana printed, **or a single-kanji word**) | 12 | **real words, every option, no exception.** Same word class and conjugation as the key (争って → four 五段 ～って), usually the same semantic field (柱 → ゆか/かべ/たな; 幼い → するどい/かしこい/しつこい; 7/2025 辛い → あまい/にがい/しぶい). They frequently do **not** share the target's kanji. |
  | **音読み compound** | 23 | **predominantly non-words** — 清濁 (さいのう→ざいのう), 長短 (きしょう→きしょ), ん⇄う (のうやく→のんやく) derivations of the key's own on-reading. **But ~5 of the 23 mix in real homophone words** (握手→拍手, 討論→議論, 実践→実験, 刑事→検事/幹事, 衣装→以上), and one set is four real compounds (7/2024-2 分析 → 分解/分節/分割). |

  So **both** blanket rules are wrong: "every option must be a dictionary word"
  fails 23 of 35 items, and "音読み distractors must be non-words" fails ~6. The
  invariant is **directional**:

  > **A 訓読み set may never contain a non-word. A 音読み set may — but only as a
  > derivation of the key's own reading (清濁 / 長短 / ん⇄う).**

  Everything else in a 音読み set has to be a real word. The rule that operationalises
  it:

  1. **Reduce each option to dictionary form** (さだまった → さだまる; the
     conjugation lock has already forced all four into one class).
  2. **Run all four through the openjlpt indices** — the vocab files' `word` and
     `reading` fields plus the kanji files' `kunyomi` (dots and leading `-`
     stripped). One command, from the workspace root:

     ```bash
     python3 -c "
     import json,sys;B='.agents/item-pool-sampling/references/openjlpt';V={};K={}
     for lv in ('n1','n2','n3'):
      for e in json.load(open(f'{B}/vocab-{lv}.json')):
       for k in (e['word'],e['reading']):
        if k: V.setdefault(k,set()).add(e['word']+'['+e['level']+']')
      for e in json.load(open(f'{B}/kanji-{lv}.json')):
       for r in e['kunyomi']: K.setdefault(r.replace('.','').lstrip('-'),set()).add(e['character']+'['+e['level']+']')
     for a in sys.argv[1:]: print(a, sorted(V.get(a,())) or sorted(K.get(a,())) or 'MISS')
     " さだまる しずまる おさまる やすまる
     ```
  3. **A HIT is the evidence**: write the headword it returned into the 問題1
     source line (§0) — `さだまる=定まる[N1]`, `あまい=甘[N2 kunyomi]`.
  4. **A MISS is not a verdict, it is a debt.** The slices hold 7,040 vocabulary
     entries (3463 N1 + 1793 N2 + 1784 N3, ~790 of them with an empty
     `reading`) and their kanji lists stop at N3, so real words miss: `やすまる`
     (休まる — an *official* July 2025 distractor) and `こうじる` (講じる) both
     return MISS. On a miss the author must write the option's **kanji spelling**
     and confirm the reading in a second source — `refs/Shinkanzen/` or the
     常用漢字表 音訓 — then record it as `やすまる=休まる[SK]`.
  5. **If no spelling can be written, the reading is invented — delete the
     option.** `がいり`, `そうじる`, `うんじる` all return MISS **and** have no
     spelling: 概 reads ガイ/おおむ.ね and 要 reads ヨウ, so 「がいり」 is neither a
     reading of the target nor a 清濁/長短 manipulation of がいよう; 損 reads ソン,
     so 「うんじる」 is derivable from nothing. (`そうじる` is the one defensible
     member of that set — ん→う is a real manipulation — and `こうじる`=講じる is a
     real word; the set was still shipped with two fabrications in it.)
  6. **音読み targets: every option is EITHER a real word OR a derivation.** A
     real homophone/near-homophone compound is official practice (握手→拍手,
     討論→議論, 実践→実験, 刑事→検事) — record its headword like any other HIT. A
     non-word is legal only as a derivation of the key's own reading; write the
     derivation next to it on the same line: 清音⇄濁音 (`さいのう→ざいのう`),
     長音⇄短音 (`きしょう→きしょ`), ん⇄う (`のうやく→のんやく`), or another real
     on-reading of the target's own kanji / a same-radical look-alike. **An option
     with neither a headword nor a derivation is fabricated** — replace it. (In a
     **訓読み** set this branch does not exist: every option is a real word, full
     stop.)
  7. **If the 解説 gives an etymology or names the trap** (「労う＝ねぎらう」), it
     must quote the headword the lookup returned, not a form assembled while
     writing the cell.

- **The target's spelling must match its `openjlpt` headword.** 問題1 tests a
  reading off a printed spelling, so a non-standard okurigana changes the item.
  Test 4 printed 「労わる」 (from `pools.json`) where
  `references/openjlpt/vocab-n1.json` heads it as 「労る」 — and the extra 「わ」 is
  what locked the option class in the first place. On a mismatch, fix
  `pools.json`, then re-sample; re-spelling the stem alone leaves the pool to
  re-draw the defect next test.
- **The KEY must be N2, and no gate checks that for vocabulary.** The band gate
  reads `references/level_band_grammar.txt`, which covers 問題7–9 grammar only.
  Before shipping any 問題1–6 item, look the key up in
  `references/openjlpt/vocab-n1|n2|n3.json`: a key that is an N3 headword and
  absent from the N2 list is too easy — test 4 keyed 賢い/かしこい (N3). Treat the
  lookup as a question, not a ruling: that corpus labels ordinary N2 words such
  as 把握・転換・審査・じっくり "N1", so confirm the verdict against
  `refs/Shinkanzen/` before replacing anything.

**問題2 (表記)** — official items use a **2×2 component matrix**: take the
correct 2-kanji compound and swap EACH kanji independently for a
visually/structurally similar wrong one, so all four options share the same
two-character skeleton (かいこう → 開港/開向/回港/回向; のうこう → 濃厚/農厚/
濃高/農高; かくじゅう → 拡張/拡充/各充/各張). Do not vary only one character
position while holding the other fixed. **Non-words and pseudo-compounds are
normal and expected in 表記 distractors** (e.g., official July 2025 ships
液って/温って/汗って and 支接/施接/支設). Distractors do NOT need to be real
dictionary headwords, but must test orthographic component precision.
⚠ **Worked examples in this file are patterns, never ship an example's target word or option set.**

**問題3 (語形成)** — 諸〜, 〜化, 準〜, 〜済み, 〜制, 未〜, 〜性, and the four
real negation prefixes 非〜/無〜/未〜/不〜 (there is no fifth — 迷〜 is not a
real negation prefix and is listed in `references/banned_collocations.txt`).
Distractors must be real N2 affixes of the same functional family. It is
**not** required that all four distractors plausibly attach to the stem (official
July 2025 問3-11 uses 教育 → 則/理/論/規, where only the key 教育観 attaches).
However, all four affixes must be real, standard affixes—never invented
morphemes like 迷〜.

**問題4 (context)** — N2 nouns/adverbs: 難航, 発足(distractor: 成立),
かろうじて, うんざり, てきぱき, 需要. Distractors share the semantic field.

**問題5 (paraphrase)** — stem contains the HARD word (あいにく, 妥当,
ありふれた, くたくた, 重宝); options are simpler. Never the reverse.

**問題6 (usage)** — 1 correct + 3 sentences that are grammatical but misuse
the word's collocation/domain (妥協, 発揮, 解消, 募集, あふれる).

"Wrong sentences must be tempting, not absurd" was on this page as a
prohibition-with-examples, and **4 / 4** papers reproduced the defect anyway
(t1 28 解消 — three 消す-domain sentences; t2 27 反発 + 28 おろそか; t3 26, 28,
29, 30; t4 26 解消, plus the mirror failure — a distractor,「契約を解消」, that
is a *real* collocation and therefore a second correct sentence). A prohibition
does not tell you how to produce a compliant wrong sentence. This does.

**Procedure for each of the three wrong sentences (do it in this order):**

1. Write a sentence in which the KEY word is *correct*.
2. Break exactly **one** thing **inside the word's own domain** — swap the
   object for another the domain contains but the word does not take, or shift
   register. Do not leave the domain: a sentence from a different domain is
   eliminable without knowing the word.
3. **Search the result.** If the collocation is attested, you have written a
   second correct sentence, not a distractor — go back to step 2.

Worked example for **解消**, spanning both failure edges and the target:

| Sentence | Verdict |
|---|---|
| ✅『長年の誤解が解消した』 | the correct option |
| ✗『部屋の電気を解消した』 | **domain violation — banned** (消す's domain, not 解消's; dies on sight) |
| ✗『契約を解消した』 | **attested — banned** (a second correct answer) |
| ✓『渋滞を解消に導いた』 | **the target band: right domain, wrong collocation** |

**Length:** official option sentences measure **mean 25.0, median 25, range
9–35 JP chars** (current era, n=136; `official_calibration.md` §7 — the 「~27」
this file used to state was a mild over-estimate). Tests 1–4 averaged **~19**
(t1: 24/16/17/18 …), so the gap is real, but **the mean is not the rule and a
9-char option sentence is official**: a single short line among four is fine,
four short lines is the drill. Write each of the four with a who/when/what
unless brevity is doing work — a telegram-length misuse line leaves no room for
the situation that makes a wrong collocation tempting.

**問題7-9 (grammar)** — only N2-list items (Shin Kanzen N2 文法 headed forms):
〜かねない, 〜ざるを得ない, 〜わけにはいかない, 〜に先立って, 〜を契機に,
〜つつも, 〜ようがない, 〜に限って, 〜ものの, 〜ばかりに, 〜たところ,
humble/honorific traps (伺う; include one FAKE form like 参られます as a
distractor). Pool draws come from `item-pool-sampling` — do not invent a form
outside that inventory.
BANNED too easy (N3–N5): 〜によると, 〜ば〜ほど, 〜がち alone, お〜ください,
〜てください, 〜ほうがいい, 〜ことができる, 〜たいです, 〜前に/〜後で as the
sole point — full list in `exam-qa-review/references/level_band_grammar.txt`
`## TOO_EASY`.
BANNED too hard (N1): 〜にあって, 〜をもって, 〜ともなると, 〜までもなく
(except the set phrase 言うまでもなく as running text, not a productive key),
〜を皮切りに, 〜がてら/〜かたわら as keys, 〜ずにはおかない, 〜余儀なくされる
as the tested form — full list under `## TOO_HARD` in the same file. Tests 2–4
shipped several of these as 問題7 keys through a green gate.
**Length is part of the N2 bar** (see Benchmark above): tests 1–4 shipped
問題7 stems averaging 20–34 JP chars against an official ~43 average — the
grammar point was right, the carrier was too short. Lengthen the *situation*,
not the grammar tag. A one-clause stem like
「このまま働きすぎると、体を壊し(　)よ。」 fails the official length band even
when かねない is the correct key; rewrite toward
「最近残業が続き休日もほとんど取れない。このまま働きすぎると、体を壊し(　)よ。」
(scene + consequence). Same rule for 問題8 frames and 問題9 cloze prose.
**Also match official stem *shape*:** every paper in `refs/JLPT_N2_NEW/` includes
several 問題7 items with dialogue turns or a setting label
`（会社で）` / `（電話で）` / `（インタビューで）` / homepage notice. Generated
tests 1–4 shipped zero dialogue stems — include **at least 2** (prefer 2–4)
per paper among the 12.

**問題7 dialogue / setting layout (Markdown):** do **not** crush the stem onto
one line. Official booklets put the place label first, then each speaker on
its own line (see July 2025 問41 司会／医者 in the booklet extract). Write:

```
**40** （会社で）
A「どうしたの。」
B「経験がないのに引き受けた(　)、大変な目にあってしまったよ。」
 1. どころか  2. ばかりに  3. ながらに  4. おきに
```

Rules: (1) `（会社で）` / `（電話で）` / `（窓口で）` etc. alone on the stem’s first
line after `**N**`; (2) each speaker turn (`A「…」` / `山田「…」`) on its own
following line; (3) the horizontal option row still on one line under the
turns. Collapsing to
`**40** （会社で）A「…」B「…」` is forbidden — it reads as a drill line, not a
booklet stem. `build_interactive.py` keeps `cur` across those stem lines, so
radios still attach; do not “fix” a sheet by flattening the dialogue.

**問題10-14 (reading)** — difficulty lives in the QUESTIONS, not vocabulary:
ask 筆者の考え/一番言いたいこと/どういうことか, never mere fact lookup.
Passages: opinions with a turn (しかし/ところが), one business email, one
notice with 3 false options contradicted by ※ fine print, one A/B pair
(agree on one point, differ on conclusion), one flyer with two-condition
matching where one tempting option fails exactly one condition.
- **Length bands — the single copy in this repo, and the gate enforces them.**
  For three rounds these numbers lived in `question-authoring`,
  `jlpt-exam-structure`, and `check_consistency.py` at once, hand-synced, with
  only one of them (問題13) actually gated and only as a WARN. An author cannot
  verify a band without measuring, so nobody did: **4 / 4** papers shipped
  問題11 and 問題14 under band. So the bands are stated **here and nowhere
  else** — `jlpt-exam-structure` now points at this table — and
  `tools/check_consistency.py`'s `check_dokkai_lengths()` is the enforcer.

  **What these numbers count, stated once because three different figures for
  one paper were in the repo at the same time** (this table said July 2025 =
  1328/2569/617/1055/702, the gate docstring said 1274/2503/572/1005/622, the
  archive measures 1249/2451/572/989/604): **JP characters only** — hiragana,
  katakana, kanji and JP punctuation, the same character class
  `check_dokkai_lengths()` uses — counting **passage prose only** (instruction
  lines, question stems and option rows removed; `（注N）` definition lines kept).
  Digits, Latin and spaces are **excluded**. Any number quoted without that
  method is not comparable — say the method when you quote one.

  **Calibrate to the era, not to a paper.** 問題11 became 4 passages × 2 items at
  **12/2022**, and its length jumped with it, so the window is the **7 sittings
  12/2022–12/2025** — not "the last five papers", which mixes eras. Band and
  per-sitting figures: `reference-book-reading/references/official_calibration.md`
  §2. Columns below: the current-era **min / median** (JP chars), the gate floor,
  and what tests 1–4 shipped.

  | Section | official min | official median | gate floor | t1 | t2 | t3 | t4 |
  |---|---|---|---|---|---|---|---|
  | 問題10 短文 (5 passages) | 1143 | 1225 | **≥1200** | 941 | 1084 | 1486 | 1092 |
  | 問題11 中文 (4 passages) | 2449 | 2556 | **≥2200** | 1881 | 1912 | 2110 | 1371 |
  | 問題12 A/B | 532 | 551 | **≥600** | 422 | 551 | 647 | 487 |
  | 問題13 長文 | 814 | 904 | **≥900** | 1051 | 920 | 1260 | 881 |
  | 問題14 情報検索 | 489 | 604 | **≥650** | 309 | 605 | 625 | 583 |

  **Three gate floors now sit ABOVE the official minimum** — 問題12 (≥600 vs an
  official 532), 問題13 (≥900 vs 814, failed by 12/2022 and 7/2024) and 問題14
  (≥650 vs 489, failed by 12/2024 and 12/2025); 問題10's ≥1200 also clears
  12/2023's 1143. A floor that rejects an official paper is a wrong floor
  (`official_calibration.md` §9 recommends 1100 / 2250 / 510 / 800 / 450), and
  `tools/` is another pass's file. **Author to the medians** — a paper at the
  median clears both the real band and the current over-tight gate. **問題14 is
  the one section where JP-char counting misleads**: the flyer is dates, prices
  and times, so all-char (JEES-style) it measures 676–793, median 707, right on
  the published 700字程度 while looking 25% short in JP chars.

  Per-passage floors on top of the section totals: **each** 問題10 passage
  ≥200 JP chars, **each** 問題11 passage ≥400 — the gate's numbers. The
  current-era measurements are 問題10 **157 / 241 / 334** (min/median/max, n=35)
  and 問題11 **507 / 655 / 763** (n=28), so the 問題10 floor is again above the
  official minimum (12/2023's fifth 短文 is 157) while the 問題11 floor has
  100+ chars of headroom. Author 問題10 passages to ~240 and 問題11 to ~650; an
  official 短文 is *allowed* to be short, but a generated one that is short is
  usually thin rather than deliberate. Count JP chars only, and count the
  passage body — the flyer's table and conditions count for 問題14. Do not hit a
  floor by padding the note block or the question stems; the gate measures the
  passage region. Use `（中略）` when a quoted source would otherwise run long:
  official ships **2–5 per paper in the current era, median 3, never zero**
  (`official_calibration.md` §3) — tests 1–4 shipped none.
- **問題11 stems — anchored, and at least one 考え/主張 per PAPER.** The oldest
  rule here said each passage's two questions must be "ONE factual-comprehension
  question plus ONE main-point/opinion question"; it was then sharpened to
  "exactly one of each per pair". **Both are wrong, and the second one was
  measured off a single sitting.** All numbers below come from
  `.agents/reference-book-reading/references/official_calibration.md` §4 —
  the current-era archive, **12/2022–12/2025, n = 7 sittings, 28 pairs, 56
  stems** — and where it disagrees with July 2025, the archive wins.

  > **Anchoring.** Every stem is anchored either on **筆者** or on a **marked
  > span** (「①…とあるが」/「〜とは何を指すか」). 82% of current-era stems name 筆者;
  > **18% do not** and anchor on a span instead (0–3 per paper). A stem that
  > names neither is the retrieval shape below — generated tests 1/2/3/4 shipped
  > 4/6/5/6 of those out of 8.
  > **Paper level: 問題11 carries at LEAST ONE 考え/主張 stem** — the official
  > spread is **1–4 of the 8** (12/2023 and 12/2024 ship exactly 1; 7/2025 ships
  > 4). Zero is the defect; two per pair is not.
  > **Pair level: the 事実把握 stem comes FIRST** — 26 of 28 official pairs (the
  > two exceptions are the two 考え/考え pairs).
  > **Banned in 問題11** — the four pure-retrieval shapes
  > 「本文で述べられている〜はどれか」「〜として正しいものはどれか」「〜の主な目的
  > は何か」「〜の内容と合っているものはどれか」. **Corroborated at n = 15
  > sittings: 0 occurrences, and not in 問題10/12/13/14 either.**

  **Why "one 事実把握 + one 考え/主張 per pair" is NOT the rule.** July 2025 is the
  only sitting in the whole 31-paper archive where all four pairs come out one of
  each — the rule was calibrated to the outlier. The current era's 28 pairs:

  | sitting | pair 1 | pair 2 | pair 3 | pair 4 |
  |---|---|---|---|---|
  | 12/2022 | 事/事 | 事/考 | 事/事 | 事/考 |
  | 7/2023 | 事/事 | **考/考** | 事/事 | 事/事 |
  | 12/2023 | 事/事 | 事/事 | 事/考 | 事/事 |
  | 7/2024 | 事/考 | 事/考 | 事/考 | 事/事 |
  | 12/2024 | 事/考 | 事/事 | 事/事 | 事/事 |
  | 7/2025 | 事/考 | 事/考 | 事/考 | 事/考 |
  | 12/2025 | 事/考 | 事/事 | 事/考 | **考/考** |

  **13 one-of-each, 13 two-事実, 2 two-考え.** A per-pair rule rejects **6 of the
  7** official papers, so it cannot be the bar. **What to author:** 2–3 考え/主張
  stems among the eight (the archive median), at most one per pair, never zero,
  and the 事実把握 stem first in every pair. **問題13 is the regular one — its item
  69 is a 考え/主張 stem in 7 of 7 papers**; treat that slot as mandatory.

  Classify each stem as you write it, by its shape, not by its intent — span
  anchoring is tested FIRST, because 「売れた理由とあるが、筆者はなぜ売れたと考えて
  いるか」 is 事実把握 despite containing 考えて:

  - **事実把握** — anchored to a *specific* span, term, or sub-topic and answerable
    from the sentences around it: 「①…とあるが、どういうことか」/「…とあるが、筆者は
    なぜ…と考えているか」/「〜について、筆者はどのように述べているか」/「筆者に
    よると、…はどうすればいいか」/「筆者によると、…とはどういうことか」.
  - **考え/主張** — unanchored, answerable only from the passage as a whole:
    「筆者の考えに合うのはどれか」/「筆者が最も言いたいことは何か」/「〜について、
    筆者はどう考えているか」/「筆者が…として大切にしていることは何か」.

  Write the eight labels down while drafting and count the 考え/主張 ones. If the
  count is zero, rewrite the SECOND stem of one pair as an unanchored 考え
  question — do not re-label a stem to make the tally look right.

  **Two gate checks currently over-enforce this section** (`tools/` is another
  pass's file, this is a pointer not a permission): `check_mondai11_stems()`
  FAILs any pair that is not one-of-each — that is the July-2025 rule, and it
  rejects 6 of 7 official papers — and it classifies a 筆者-less span-anchored
  stem as 未分類 when 18% of official stems are exactly that. Both need rescoping
  to the paper-level rule above. The banned-shape half of that function is
  corroborated and should stay a FAIL. And the honest limit is unchanged: the
  gate reads *shape*; a 筆者-anchored stem whose key is still a paraphrase of one
  sentence needs a reader (`exam-qa-review` step 3).
- **問題11 glosses:** every `（注N）` must annotate a word that actually appears
  in that passage's body, and every in-body marker must have a definition
  line — the pairing is 1-to-1 per passage, both directions. An orphaned note
  is a shipped defect (test 3 shipped unmarked glosses across all four 問題11
  passages; test 2 shipped 4 orphans; test 4 shipped a 問題13
  「準備（注5）」 with no 注5 line), not a stylistic slip.
- **問題14 — 70 and 71 are BOTH person-scenario items.** The correct answer must
  always require combining **at least two** constraints from the table (topic +
  date/time, or a category + a footnote exception) — never a single-field
  lookup. The defect has a fixed shape: it is always **item 71**, always written
  as 「このお知らせの内容と合っているものはどれか」, and it shipped that way in
  t2 (71 = 先着100組, one cell), t3 (71 = 市外在住者も対象, one cell) and t4
  (71 = 事前予約不要, one cell). t1 is the compliant example (70 = 時間帯 +
  初心者; 71 = 期限 + 受付方法 + 支払方法). So:

  > 70 and 71 are **both** person-scenario items. 71 may never be
  > 「このお知らせの内容と合っているものはどれか」 — a content-match question
  > collapses to a one-cell lookup (tests 2, 3, 4 all shipped it there). Write
  > 71 as a second applicant whose plan fails exactly one condition. **The 解説
  > cell for each of 70 and 71 must quote the TWO source cells the key combines**
  > (`「カテゴリーB：…」＋「※…の場合は…」`); one quote means one constraint.

  **Corroborated across the archive** (`official_calibration.md` §6): 70 and 71
  are both person-scenario items in **7 of 7** current papers, and **not one**
  uses 「このお知らせの内容と合っているものはどれか」. The key always combines **≥2
  cells and commonly 3** (7/2025-71 = 受付期間終了 + 開始3日前まで + 電話のみ;
  12/2024-70 = room type + bath + 朝食付きプラン + Sunday rate). The two official
  shapes to copy: a named person with 2–3 requirements → which option/course/room,
  and a named person on a given date → what they must do to book, with a footnote
  exception deciding it.

  `make check` FAILs when a 問題14 解説 cell contains fewer than two distinct
  `「…」` spans that occur in the flyer text. Every constraint the QUESTION
  references (a role, category, or condition) must also be describable from the
  flyer/table text as printed — do not invent a scenario detail (test 3 asked
  how someone applies as "補助スタッフ" when the source flyer never described a
  staff/volunteer role at all).
- **読解 keys must be paraphrased to option length.** **Paraphrase every 読解 key
  to option length (~25–40 JP chars) and keep the four options close in length**,
  or the key is findable by string length alone — without reading the passage.
  Test 3 shipped items 67, 68, 69 as three consecutive keys of 91/101/61 chars,
  lifted verbatim from the passage, beside ~31–34 char distractors; test 4
  shipped item 66 at 55 vs 31.

  **"Within ±40% of each other" is a target, not an invariant** — measured over
  140 current-era items (`official_calibration.md` §9), **95% satisfy
  max/min ≤ 1.8**, so that is the number to author to, but official ships items
  at **2.10** (12/2025-66) and **2.09** (12/2023-65). Two things follow that the
  older wording got wrong: an item at 1.9 is not automatically a defect, and
  **the key being the longest of the four is not a defect either — 29% of
  official keys are.** What is a defect is a key that is long **and** a verbatim
  span of the passage: that is doubly wrong, because it turns 主張理解 into string
  matching. `make check` FAILs a keyed 読解 option (52–71) that is ≥50 JP chars,
  present verbatim in the passage, **and** ≥1.7× the mean of the other three —
  measured against 138 official keyed options, the longest official key is 61
  chars and the highest ratio 1.55, so **no official item trips the pair**. That
  gate constant survives the archive; keep it.
- **Vocabulary Explanations for Dokkai (NO FURIGANA / MANDATORY)**:
  - **NO FURIGANA IN DOKKAI**: Reading passages (問題9–14) and question stems/options in 言語知識・読解 contain **NO FURIGANA** (`<ruby>`). Test-takers are expected to read N2 kanji without furigana. Over-the-level, rare, or domain-specific words must ONLY be glossed using `（注1）`, `（注2）` notes at the bottom of the passage.
  - **How many, and how they are counted.** Official papers gloss freely:
    measured as **in-body markers** (one per glossed term, in the passage
    region — not raw `（注N）` occurrences, which double-count because each gloss
    also has a definition line), and tests 1/2/3/4 carry **9 / 6 / 29 / 15**.
    (July 2025 measures **27** in the archive's PDF extract and **30** in this
    repo's `imported-n2-2025-07` markdown — a 3-marker extraction difference, not
    a disagreement about the rule. Quote the archive's number.)

    **The bar is ≥25 in-body markers across 問題10–13, and ≥3 in every 中文/長文
    passage** (each of the four 問題11 passages, and 問題13). A floor of 15 was
    "half of official" and let all four papers ship under-glossed; 25 is the
    number to author to. `tools/check_consistency.py` currently WARNs below 15 —
    that gate is the backstop, not the target, and a paper at 16 markers is off
    -calibration even though it stays green.

    **Corroborated by the archive** (`official_calibration.md` §3, current era
    12/2022–12/2025, n=7): the per-paper band is **27–61 in-body markers, median
    39** — so ≥25 is a floor *below* every current official paper, which is what
    a floor should be. Per section, and this is the part a blanket per-問題 rule
    would get wrong:

    | | 問題10 | 問題11 | 問題12 | 問題13 | 問題14 | total |
    |---|---|---|---|---|---|---|
    | current-era range | 3–13 | 17–36 | **0** | 0–12 | **0** | 27–61 |
    | median | 6 | 24 | **0** | 7 | **0** | 39 |
    | July 2025 (one sitting) | 3 | 17 | 0 | 7 | 0 | 27 |

    **問題12 and 問題14 get zero glosses in every current-era paper** — never
    write a per-問題 floor that touches them. The count is earned in **問題11**
    (per passage: min 2, median 5.5, max 13, n=28; 26 of 28 carry ≥3) and
    **問題13** (0–12, median 7 — 12/2022 shipped a 長文 with none). Plan ~5 per
    中文 and ~7 for the 長文 and the paper total takes care of itself; do not
    spread a quota across 問題10 to reach a number.

    One archive finding that touches the band rule below: official uses
    「ここでは、…」 freely in definition lines (July 2025 glosses 像を結ぶ as
    「ここでは、姿がわかる」), so **the repo's 「ここでは」 ban is about glossing a
    basic word circularly, not about the phrase**. Do not rewrite a legitimate
    gloss to avoid the string — `make check` WARNs on it, and a 「ここでは」 gloss
    on an over-level term is a false positive to state as such in your report
    (§0.5), not a defect to edit away.
  - **The count rule and the band rule below are one rule; do not trade them
    against each other.** Test 3 is the warning: it is the only paper in band on
    the count (29 markers) and it got there by glossing 割引・洗髪・契機・規制・
    革新・省力化・増幅 — banned-band words. Reaching the count with basic-word
    glosses is worse than shipping 5, because it also degrades the passage.
    The two rules only conflict when the passages are written first and glossed
    afterwards — there are then only so many hard words on the page, and the
    author starts glossing 準備. Reverse the order: **choose the notes while
    drafting the passage.** A 中文 on a specialized subject (ゾウの進化,
    医療の個別性, 起業 — July 2025's own) naturally carries five domain terms; a
    passage written entirely in general vocabulary carries none and cannot be
    rescued by annotation afterwards. If a drafted passage yields fewer than 3
    glossable terms under the ✅ TARGETS list, its subject is too plain for 中文 —
    deepen the subject, never gloss down to the floor.
  - **STRICT VOCABULARY BAND FOR NOTES (NON-NEGOTIABLE)**:
    - 🚫 **STRICTLY BANNED**: Glossing N3–N5 words or standard N2 vocabulary (e.g., 選択, 信号, 技術, 文化, 質, 準備, 手順, 設計, 現象, 経由, 偏り, 維持, 継続, 前提, 細部, バランス) with trivial/circular definitions (`ここでは…`, `〜のこと`). Glossing basic words degrades test quality and is a QA failure.
    - 🚫 **The operational test, not the list:** a term is glossable only if
      (1) it does **not** appear in
      `.agents/item-pool-sampling/references/openjlpt/vocab-n2.json` (if it is in
      the N2 vocabulary file it is standard N2 — do not gloss it), and (2) the
      definition introduces words the term itself does not contain (「洗髪：髪の毛を
      洗うこと」 and 「割引：…金額を引くこと」 fail this; 「大脳辺縁系：…」 passes).
      The enumerated list below is examples, not the boundary. It has to be a
      test rather than a list because the banned class is "any standard N2 or
      below word", which no enumeration can close: the 21-word list here could
      never have caught 割引, 洗髪, 契機, 鑑賞, 評価制度, or 省力化, and **4 / 4**
      papers shipped wrong-band glosses under it (t1 鑑賞/評価制度, t2 質感/
      バランス, t3 the seven above, t4 準備).
      Check it in one line:
      `python3 -c "import json,sys;w={e['word'] for e in json.load(open('.agents/item-pool-sampling/references/openjlpt/vocab-n2.json'))};print([x for x in sys.argv[1:] if x in w])" 鑑賞 割引 バランス`
      `make check` WARNs on both halves (glossed term present in
      `vocab-n2.json`; definition body repeating the glossed term or opening
      `ここでは`).
      **Both conditions are necessary, neither is sufficient**: that file is a
      1793-entry N2 slice, so absence is not proof a word is over-level (準備,
      技術, 選択 are all absent from it and all banned). A glossable term must
      ALSO fall in one of the ✅ TARGETS categories below — that is the positive
      requirement, and it is the one that decides.
    - ✅ **TARGETS**: `（注N）` glosses are strictly reserved for:
      - N1-level or rare/literary words (e.g., 委ねる, 雄弁, 死守する, 顧みる, 飼いならす, 抑圧, その場しのぎ)
      - Onomatopoeic / colloquial expressions (e.g., むきむきの)
      - Specialized / domain jargon (e.g., 大脳辺縁系, 起業, 機動性)
      - Contextual / figurative metaphors (e.g., 余白のあるメディア, 思い出の扉)
  - Annotate in text strictly as `（注1）`, `（注2）`… (never `<ruby>`).
  - Immediately following the passage (before question items), provide the
    note block `（注1）語彙：簡潔で自然な日本語の意味の説明` (one line per note).
  - Use `（中略）` at least once across 問題11–13 when cutting a longer
    exposition — official papers do; generated tests 1–4 never did.

**聴解 dialogues** — for 問題1, 問題2, and 問題4/5, every wrong option must be MENTIONED then eliminated (already done / rejected / explicitly denied: 「それが理由ではありません」). For **問題3 (概要理解)** only, official distractors are topic-level summaries or general statements with key modifiers missing/altered, matching official paper structure.

**Construction order is binding: write the dialogue FIRST, then harvest the
options from it.** Never draft an option set before the script line exists.
Then record the grounding in the 解説 cell of `聴解.md`, one line per wrong
option, in this shape:

```
1 ✗「script line as spoken」→ 別の人に割り当て
2 ✗「…」→ 後回しにされた
4 ✗「…」→ 明確に否定
```

**聴解 問題5-2番 (printed options)** — Official papers print bare labels for the four choices in 問題5-2番 (e.g., 「夕日通り / にしがおか / さくら公園 / 東山」 or 「共用の大型ボックス / 各戸専用の小型ボックス / 冷蔵機能付きボックス / 管理人室」). DO NOT print full sentences or include the deciding attributes (e.g., 「東山（商店街の近くで便利）」 or 「東山を利用する」). The item exists to test whether the examinee can remember and match the attributes heard in the audio to the labels.


An option with no quotable line is fabricated noise: delete it and take one
from the script. This cell is what QA reads; if it is absent, the item is
not shippable.

Why this is an order and an artifact rather than the rule it replaces: "every
wrong option must be MENTIONED then eliminated" was already stated **three
times** across this file and `choukai-script-writing`, always as a property to
verify *after* both files exist — i.e. the last thing an author does, in the
last file authored, which is exactly where long-run degradation lands. Nothing
recorded whether the check ran, so skipping it was invisible, and **4 / 4**
papers shipped ungrounded options (t1 問題2-1番 options 2 and 4 — the 解説
itself admits it; t2 5 options across 4 items; t3 ~14 options, with 問題2-2番's
three wrong options all fabricated; t4 問題2 例 option 2). The grounding cell
makes a skip visible on disk. `make check` WARNs when a 問題1/2 option shares no
≥2-char kanji/katakana token with its item's script block — WARN only, because
that heuristic flags 5/44 on the *official* paper (official distractors are
often paraphrased). The mechanical check cannot tell "reassigned" from "never
said"; the written grounding line is what does.
An option that is raised and left TRUE is a second answer even if it is "only
a contributing factor": test 1's 遅刻理由 item affirmed 道が混んでいた in the
audio while keying USB忘れ — a どうして item's wrong causes must be denied,
not merely outweighed.
課題理解 hides the correct first action behind 「その前に」「それが先」.
即時応答 tests idioms and keigo: 目を通す, お言葉に甘えて, 〜かと思いきや,
〜ようがない, 席を外しております, 在庫を切らしております.

## Item integrity (every rule here shipped broken at least once)

`make check` enforces the mechanical half of this list per test; the rest is on
you. Run it before calling any authoring work done.

- **Passage Numbered Markers Must Match Questions Exactly (1-to-1)**: Every numbered marker (`①**...**`, `②**...**`) placed in a reading passage MUST be referenced by a question stem in that passage's question set. Never leave orphaned/unused numbered markers in a passage (e.g. marking both ① and ② in a passage when questions only ask about ①).
- **Four DIFFERENT options.** Never let the same string appear twice in one
  option set — that is a second correct answer. Test 2 shipped
  `1. 削減  2. 削減` and `1. ぶった … 3. ぶった`. When building near-miss kanji
  distractors, read the four back to yourself before moving on.
- **The key goes where `answer_positions` says — and if the spec has none, STOP.**
  `tests/<test_id>/test_spec.json` prescribes the correct-option number for all 101 items so
  no number is over-used. Write the item, then *order the options* so the correct
  one lands on the prescribed slot. Do not write the key you feel like and do not
  "fix" the imbalance later — `make check` compares all 101 against the spec.
  **The failure mode is the spec being silent, not wrong.** `make check` prints
  `keys match tests/<test_id>/test_spec.json answer_positions (0 prescribed)` and passes
  when the field is absent, so an author who never looked cannot tell. All four
  papers on disk were authored that way — none of their `test_spec.json` files has
  the field, `tests/<test_id>/test_spec.json` is missing entirely, and the keys came out
  38–53% on option 1 (test 2: 53/25/11/13 of 101). `sample_items.py` does emit
  `answer_positions`, so a spec without it was not produced by the sampler: re-run
  `sample_items.py --seed <n> --test-id <id>` and author against its output rather
  than starting from a spec that prescribes nothing.
- **問題8: the answer is the option on ★, which is the 3rd of 4 blanks.**
  Assemble the full sentence first, confirm it is grammatical, number the
  positions, and only then read off which option sits third. Test 2 shipped
  three of five keys naming the 2nd or 4th blank instead. Write the 解説 as the
  word order with option numbers in parentheses, correct one bolded:
  `状況に(2)→おいて(4)→**価格競争が(1)**→続く限り(3)`. `make check` parses that
  sequence and asserts its 3rd entry equals the key, so it must be a real
  permutation of 1-4 that matches the stem's options.
- **問題8: the stem must be MISSING exactly what the options supply.** Write the
  finished sentence, cut the four-part span out of it, and let the blanks stand
  where the span was — do not leave the words in the stem as well. Test 3
  shipped all five items with the sentence written out in full *and* chopped
  into options, so 45 assembled to
  「兄が外で活発に遊ぶのを外で遊ぶのを好むのに対して…」 and 49 said
  パニックになって twice. Every other 問題8 gate passed, because none of them
  read the stem's own words. The test: splice stem + options in 解説 order and
  read the result end to end. If any word occurs twice, the stem is wrong, not
  the key.
- **Every scramble must form ONE grammatical sentence.** Two options that cannot
  coexist make the item unanswerable no matter the key: test 2 offered both
  「まったく」 and 「ほとんど持てていない」 in one set, and both 「わりに」 and
  「にもかかわらず」 in another. One contrast marker, one degree adverb.
- **問題8: check the GLUE at both ends, not just among the four options.**
  The four options must chain into each other correctly (above), but they
  must ALSO glue grammatically onto the stem's fixed text immediately before
  the first blank and immediately after the last one — test 4 shipped three
  items where the option chain was internally fine but stacked an
  incompatible verb or a duplicate conditional/particle against the FIXED
  trailing text outside the blank span (`…ご連絡を` + fixed tail
  `お問い合わせください`; `…立ち返らねば` + fixed tail `なければならない`,
  double-stacking the conditional). Read the fixed lead-in, then all four
  options in key order, then the fixed tail, as one unbroken sentence — the
  join points are exactly as much a failure surface as the internal order.
- **問題8: exactly ONE of the 24 orderings may be grammatical — build for it,
  then count it.** A floating adverb or adjunct (ほとんど, 直接, 一度, 年々,
  世界中で…) that reads equally well in two slots gives the item two defensible ★
  answers — QA failed one such item in each of tests 2, 3, and 4
  (「ほとんど自分の時間を/自分の時間をほとんど」, 「窓口に直接/直接窓口に」,
  「一度原点に/原点に一度」), and test 4's current version ships **four** items
  with two valid ★ answers. The old rule here said "actively try to permute every
  option into every other slot" — a review-time judgement with no artifact, which
  is why it kept passing. It is now two construction rules and one count.

  **The invariant is uniqueness — nothing else.** An earlier version of this
  bullet banned bare adverbs outright (`着実に`, `お気軽に`, `ほとんど`, `直接`,
  `年々`). **The archive contradicts that ban**
  (`.agents/reference-book-reading/references/official_calibration.md` §7,
  64 of 75 items over the last 15 sittings): a bare adverb or particle on a card
  is **official practice** — 12/2023-47 「一度」, 12/2024-43 「もう」,
  7/2025-43 「もちろん」, 7/2025-44 「珍しく」, plus bare particles and verbs
  (12/2024-44 「だけ」「する」「して」). 4 of 29 current-era items (14%) carry one,
  and **51% of all official options are under 5 JP chars**. So:

  **Risk flag 1 — a bare adverb card makes the uniqueness check mandatory and
  explicit.** An adverb constrains neither its left nor its right neighbour, so
  it is the single commonest way to end up with two valid ★ answers (tests 2, 3
  and 4 each failed QA on exactly that: ほとんど自分の時間を / 直接窓口に /
  一度原点に). It is allowed — but if any card is one, you must run the link table
  below and write its result down; you may not eyeball the item. If the table
  yields more than one path, the fix is to attach the adverb to what it modifies
  on the SAME card (`着実に成果を上げて`) or move it into the stem's fixed text.

  **Risk flag 2 — an under-glued card.** A card that ends in something naming
  what follows — a particle (`を`/`に`/`が`/`と`/`の`), a 接続形 (て形・連用中止・
  条件形), or a 連体形 demanding a noun — can sit in only one slot, and a set
  built that way usually has a unique ordering by construction. This is a way to
  *reach* uniqueness, not a requirement in itself: official ships plenty of cards
  that are glued at neither end.

  **Add no further numeric limits here.** §9 of the calibration file measures
  three of the gate's own 問題8 constants against the archive and they reject
  **20% / 38% / 34%** of official items (`P8_OPT_SUM_MIN` 16 vs an official band
  of 9–41; `P8_LONG_OPTS_MIN` 2 vs a band of 0–4; `P8_ASSEMBLED_MIN` 45 vs
  30–78). Chunk-size intuitions do not survive contact with the archive —
  uniqueness does.

  **The count, written out.** 4! = 24 orderings; do not read 24 sentences, build
  the link table instead:

  1. Write the fixed lead-in **L** (stem text before the first blank) and the
     fixed tail **T** (stem text after the last blank).
  2. Fill a 4×4 table of ordered pairs: mark `○` in cell (i, j) only if option i's
     ending can be immediately followed by option j's opening in grammatical
     Japanese. 12 interior cells (the diagonal is unused).
  3. Mark the 8 boundary cells the same way: `L→i` for each option, `i→T` for each
     option — this is the both-ends glue check already required above.
  4. **Count the complete paths `L→…→T` that visit all four cards.** Exactly one
     may exist. Two or more = two defensible ★ answers, replace the floating card.
     Zero = the item is unanswerable as printed.
  5. Record the result in the same 解説 cell as the word order, appended after it:
     `状況に(2)→おいて(4)→**価格競争が(1)**→続く限り(3)｜一意性: 24通り中1通り、裸の副詞なし`.
     **Write no parenthesised single digit in that suffix** — `make check` reads
     every `(1)`–`(4)` in the cell as the word order and will fail on a fifth.
- **A cloze blank must not repeat what the stem already says.** `…からでも
  ( 54 )はいかがだろうか` with option `試してみてはいかがだろうか` ends the
  sentence twice. Read stem-plus-option aloud as one sentence for all four.
- **Exactly ONE option may be defensible.** Three wrong answers, not three
  weaker answers. The failure looks like a well-written item, so it survives
  every gate: test 3's 問題9 (52) offered 無理もないだろう / 自然なことだ /
  珍しいことではない / 仕方がない for 「増えているのも( )」 — four ways of saying
  the same thing, with the key arguably the third-best of them. 問題4 (19) keyed
  切実 while 深刻 sat in the option list and fits 「〜な問題だ」 just as well.
  For every distractor, name the reason it is *wrong* — not merely less apt. If
  the reason is "the key is slightly more natural", rewrite the stem until the
  distractor is impossible (切実 → put it on 願い, where 深刻 cannot go).
- **Name the reason each distractor is IMPOSSIBLE — in writing.** This is the
  single rule that catches the two-defensible-answer family before it ships,
  and test 4 shipped six of them at once: 問題9 (51) offered すなわち against
  the key つまり (the same word), (52) したがって against そう考えると (both
  fit); 問題7 (38) keyed に即して with に沿って in the list, and
  「ニーズに沿ったサービス」 is if anything the commoner collocation; 問題3 (14)
  keyed 未記入 with 無記入 available (both are words); 問題4 (19) keyed おろそか
  with いいかげん beside it, and 健康管理をいいかげんにする is ordinary
  Japanese. Every one reads as a well-made item. Write the reason in the 解説
  cell (「1『に沿って』は…」) — a distractor you cannot explain away is a second
  key, and the fix is to REPLACE THE DISTRACTOR, not to defend the key.
  Near-synonyms are the whole risk: two connectives that both summarize, two
  negative prefixes that both attach, two adverbs that both take 〜にする.
  The same class then failed QA in every earlier test too: 停滞 beside the key
  難航 on 交渉が(　)している (交渉が停滞する is attested), 大満員 beside 超満員,
  消費 beside 需要 on 〜が伸びている, こと beside だけ in a cloze, and a 問題6
  distractor using 把握 in ordinary reportage phrasing. **The test is a search,
  not a feeling**: for every distractor, check whether distractor+frame is an
  attested collocation (search 「<word> 例文」 if unsure); if it exists, the
  item has two keys — replace the distractor.
- **問題5 言い換え: the option must be substitutable.** Read the stem with the
  option swapped in and confirm it is still a grammatical sentence. Test 4
  underlined わりに in 「値段の**わりに**美味しい」 and keyed 比較的, which
  yields 「値段の比較的美味しい」 — the item cannot be answered as printed. A
  meaning match is not enough; the frame around the word has to accept it.
- **問題1 漢字読み: all four options must be the same word form.** Test 4 gave
  the dictionary form 労わる four options of which three were て-forms
  (やしなって・なぐさめて・あがめて), so the answer was identifiable without
  reading the kanji at all. Distractors are READINGS of the same written form —
  ideally a genuine trap the kanji supports (労う = ねぎらう for 労わる = いたわる).
- **問題1 漢字読み: conjugation must not give the answer away.** Test 1 keyed
  慌てて with `1. あきれて  2. あわてて  3. あふれて  4. あばれて`. The stem's
  okurigana is ～てて (～てる class); three distractors are ～れて (～れる
  class: あきれる・あふれる・あばれる). Only the key fits the printed
  conjugation, so the item is solvable without reading the kanji. Mora count
  need not match — the leak is the conjugation class clash. The same defect
  appears whenever okurigana already selects one option's ending and rules out
  the others (～てて vs ～れて, ～って vs ～いて, ～んで vs ～いで, …). **Every
  option must be a real Japanese word** (a genuine reading of some real verb/
  adjective/noun), not a made-up near-miss string. **The test before shipping:**
  cover the kanji, keep okurigana visible — if exactly one option still fits
  the conjugation, rewrite. Fixes, in order of preference: (1) put the target
  in dictionary form so okurigana does not advertise the class (慌てる → real
  ～る readings that could confuse); (2) keep the conjugated stem but give every
  distractor the same conjugation class and a real-word reading; (3) pick a
  different carrier whose written form does not leak. Never mix ～れる-class
  readings under a ～てる-class stem just because the words "look related."
- **One grammar point may be the KEY only once per paper.** Not just one item
  per 問題: test 4 keyed 〜にともなって in 問題7 (33) and again as the 問題9
  blank (53). Cross-check the 問題7/8/9 key list against itself, and keep a
  tested form out of the reading passages too (問題9's passage said
  「時代に即した」 while 問題7 (38) was testing 〜に即して).
- **問題6 用法: the correct sentence must be flawless, the wrong ones merely
  wrong.** Test 4's 妥協 key read 「互いの条件を歩み寄り」 (歩み寄る is
  intransitive) — the one sentence that must be beyond doubt was ungrammatical.
  And a distractor has to be a MISUSE, not a rarer valid use: the same item
  offered 「品質の向上に妥協した」 and the 考慮 item offered 「考慮に値する」,
  both real collocations, so both items had two correct sentences. Before
  keeping a wrong sentence, search the collocation; if it exists, rewrite it.
- **Japanese only — no Latin script in the prose.** A stray English word means
  the sentence was drafted and never finished: test 3's 問題9 read 「単なる無音の
  contrast ではない」. Loan words go in katakana. `make check` allows only the
  initialisms real papers print (SNS, AI, CD…).
- **Distractors must be grammatical Japanese that is merely WRONG.** 用法
  (問題6) distractors are sentences a learner could believe — a wrong
  collocation or domain, never word salad. 「整備がおろそかに完璧だった」 is not
  a distractor, it is a bug: nobody can be tempted by it, so the item tests
  nothing.
- **Explanations must quote the real text.** The 解説 cell for a 読解 or 聴解
  item has to quote the passage or script line that decides it — copy-paste,
  do not paraphrase from memory. Test 2's 聴解 key quoted four lines of dialogue
  that were nowhere in `聴解スクリプト.txt`, which hid a keyed answer that the
  script did not actually support. If you cannot find the quote, the item is
  broken, not the explanation.
  **A paraphrase inside 「」 is a defect even when the key is right** — QA found
  the condensed-quote class in every one of tests 1–3 (13 non-verbatim 「」
  spans in test 3 alone, two of which misstated the audio). Write every 解説
  quote by selecting and pasting the source line at authoring time, then treat
  each `make check` 解説-quote WARN as a diff list to re-paste, never as noise
  to justify.
- **即時応答: the keyed reply must fit the speaker's rank and direction.**
  Keigo has a direction: test 2 keyed a 社長 answering a subordinate with
  「かしこまりました。会議室でお伺いします」 (humble, wrong way up), which made
  a register-appropriate distractor equally defensible, and had a 課長 say
  「拝見しました」 about a subordinate's 議事録. When the prompt names roles,
  check every option's honorific direction against them.

## Markdown formatting contract (CRITICAL to prevent HTML numbering bugs)

- **Question stems MUST use bold numbers, NOT Markdown list syntax**:
  - Write `**1** 労働組合は...`, `**6** 最近...`, `**71** ...` (for `言語知識・読解.md`).
  - Write `**例**`, `**1番**`, `**2番**` (for `聴解.md`).
  - **NEVER** write `1. 労働組合...` or `6. 最近...` — Markdown converts `N.` lines into HTML `<ol>` lists, which resets the question number back to 1 at every section header and indents sub-options as nested lists.
- **Horizontal Options Layout (問題1–5, 問題7, 問題8)**:
  - Options must run on a SINGLE line with leading space and double spaces between choices:
    ` 1. こうしょう  2. こうちょう  3. きょうしょう  4. こうしゅう`
  - The booklet builder detects 3+ options on a line and converts spaces into wide ideographic spaces (`\u3000\u3000\u3000`).
  - **例外ではない — 問題7 dialogue stems:** setting + speaker turns are multi-line
    (see above); only the `1. … 2. … 3. … 4. …` row stays horizontal on one line.
- **Vertical Options Layout (問題6, 問題10–14, 聴解)**:
  - Options must be on separate lines with a leading space:
    ` 1. 資料をコピーする`
    ` 2. 会議室の予約を変更する`

## Answer keys & Explanations (MANDATORY TABLE FORMAT)

Answer keys and explanations MUST be formatted as Markdown tables at the end of `言語知識・読解.md` and `聴解.md`. Single grid summary tables without explanations are STRICTLY FORBIDDEN.

**Both files MUST open their key section with a heading whose text starts with
`解答` or `正解`/`【正解`** (regex `^#+\s*(解答|【?正解)`). Any wording qualifies —
existing tests use `# 解答(言語知識・読解)` and `# 解答と解説` for
`言語知識・読解.md`, and `# 解答用紙(マークシート)` for `聴解.md`. This is not
cosmetic: `build_interactive.py` truncates the document from the FIRST such
heading onward so the key never renders on the answer sheet, and it **exits
with an error** if there is none. Two consequences:

- a key section introduced only by `##` sub-headers fails the build;
- never put `解答`/`正解` at the START of a heading in the question body — the
  whole document from there down would be truncated out of the answer sheet.
  (`# 問題用紙・解答用紙` is safe: it starts with 問.)

### 0. Required artifacts inside the key tables (index)

Six rules in this file are complied with by **writing a specific line into a
key cell**, not by thinking something. Each replaces a prose rule that four
papers read and reproduced the defect anyway. They are indexed here because the
key tables are where they land; the rule and its shipped evidence are at the
linked section.

| Artifact | Where it goes | Shape | Rule |
|---|---|---|---|
| Functional-category line | `## 文字・語彙` key notes, every 問1–6 item | `24: 程度副詞 ×4 (比較的/非常に/たいして/一段と)` | 「The functional-category line is mandatory OUTPUT」 |
| 問題1 distractor sources | same line as above, 問1 items | `いたわる=労る[N1][同漢字], …` — every option's resolved headword AND its branch label, plus `[SK]` or a 清濁/長短 derivation where the lookup MISSes | same + 「All four readings must RESOLVE」 |
| 問題8 uniqueness note | `## 文法`, rows 43–47, after the word order | `｜一意性: 24通り中1通り、裸の副詞なし` (no parenthesised single digit) | 「exactly ONE of the 24 orderings」 |
| 問題9 category tag | `## 文法`, the four 問題9 rows, cell opening | `[論理接続]` `[文末モーダル]` `[内容推論]` `[慣用・形式名詞]`, exactly one `[内容推論]` | 問題9 rule under Benchmark |
| 問題14 two-cell quotes | `## 読解`, rows 70 and 71 | two distinct `「…」` spans present in the flyer | 問題14 rule under 問題10-14 |
| 聴解 option grounding | `聴解.md` 問題1/2/3 解説 cells | `1 ✗「script line as spoken」→ 別の人に割り当て`, one line per wrong option | 「聴解 dialogues」 |

An absent artifact makes the item unshippable — that is the point of writing it
down rather than checking it. `make check` reads the 問題9 tags and the 問題14
quote pairs and FAILs on them; the other four are read by `exam-qa-review`.

### 1. `言語知識・読解.md` Answer Key Format
Under the key heading (see above), must contain three distinct section headers:
- `## 文字・語彙`: Multi-column table (`| 問 | 答 | | 問 | 答 | | 問 | 答 | | 問 | 答 |`) for Q1–30, plus key notes for notable kanji/words — **including the mandatory functional-category line for every 問1–6 item** (§0).
- `## 文法`: 3-column table (`| 問 | 答 | 解説 |`) for Q31–51 with exact grammar point explanations and scramble sequence breakdowns for Q43–47 — **each Q43–47 cell closing with the uniqueness note** (§0). **The four 問題9 rows (48–51) each open their 解説 with a bracketed category tag** (§0).
- `## 読解`: 3-column table (`| 問 | 答 | 解説 |`) for Q52–71 quoting key passage text and rationale. **Rows 70 and 71 each quote the TWO flyer cells the key combines** (§0).

### 2. `聴解.md` Answer Key Format
Must contain two main parts:
- `# 解答用紙(マークシート)`: Standard bubble-sheet tables for 問題1〜問題5 with sample item (例) pre-marked (e.g. `1 **(2)** 3 4`).
- `# 【正解・解説】※解き終わってから見てください`:
  - `## 問題1 課題理解`: 3-column table (`| 番号 | 正解 | 解説 |`) for 1番–5番 quoting deciding phrase, **plus the option-grounding lines** (§0).
  - `## 問題2 ポイント理解`: 3-column table (`| 番号 | 正解 | 解説 |`) for 1番–6番, **plus the option-grounding lines** (§0).
  - `## 問題3 概要理解`: 3-column table (`| 番号 | 正解 | 解説 |`) for 1番–5番, **plus the option-grounding lines** (§0).
  - `## 問題4 即時応答`: 3-column table (`| 番号 | 正解 | ポイント |`) for 1番–11番 detailing honorifics/idiom points. **Eleven**, not twelve — 12 is the 2009 guidebook's 目安; every paper in `refs/JLPT_N2_NEW/` speaks 11 items (measurable in the official audio as 11 × 8 s answer pauses), and `expected_choukai` / `answer_positions` both require 11.
  - `## 問題5 統合理解`: 3-column table (`| 番号 | 正解 | 解説 |`) with **3 rows** — 問題5 has 2 items but 3 answers. The 番号 cell must let `parse_choukai_keys()` reach `問5-1`, `問5-2-1`, `問5-2-2`; it accepts either label style — `**1番**` / `**2番 質問1**` / `**2番 質問2**` (preferred) or `1` / `2-質問1` / `2-質問2`. The 2番 rows MUST carry `質問1`/`質問2`; the 1番 row must NOT.
  - `## 得点の目安`: Score range guidelines.



