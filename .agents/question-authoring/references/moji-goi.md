# 文字・語彙 (問題1–6) — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — it carries the N2-band rule, the sniff test, the
mandatory functional-category line, and item integrity (the 問題1 option-form
and conjugation-lock rules are Item integrity #13–14 there). This file owns the
問題1 two-branch distractor rule and every 問題1–6-specific construction rule.

## 問題1 (漢字読み)

Test N2-band words: 交渉, 慌てる, 妨げる, 潔い, 措置, 傾向, 効率, 険しい.
Build distractors from REAL confusions — reading traps (措置(そち) vs
しょち/そうち), homophone kanji sets (納める/収める/治める/修める, 敗れる/破れる),
same-radical fakes (険/検/剣/験).

### Underline the WHOLE word, okurigana included

In the Markdown the underline is the bold span: write `**収まった**`, never
`**収**まった`. Official July 2025 (`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`,
問1) marks `**才能**`, `**辛い**`, `**刑事**`, `**起床**`, `**収まった**` — the
inflectional tail sits *inside* the mark in both okurigana items, and 問題2 does
the same with kana spans (`**しめって**`). Corroborated across the archive
(`references/official_calibration.md` §5, with its §0 caveat that the archive is
a Word-typeset reproduction, consistent across sittings).

**The defect is splitting a word, not the character count.** Forbidden: marking
part of a word and leaving the rest outside — test 4 shipped `**爆**ぜる`, which
asks for a bare character's reading and lets ばく/はつ compete with はぜる.
Legitimate: a whole word that happens to be one kanji — official draws them
(腕 12/2023-1, 柱 12/2025-1, 針 12/2012; 柱's set ゆか/かべ/たな is an ordinary
訓読み semantic-field set). A single-kanji *word* is a normal target; a
single-kanji *fragment* of a longer word is not.

### The two-branch rule — same kanji OR same semantic field (the ONLY statement)

Every distractor must share the target's word form and conjugation class (core
Item integrity #13–14; each option a real word per the RESOLVE procedure below)
AND be either:

- **(a) 同漢字** — a reading of the target's OWN kanji or of a same-radical /
  visual-component kanji (措置: そち/しょち/そうち; 険しい: けんしい/けんみしい/
  かんしい/けわしい), OR
- **(b) 同分野** — a real N2 word in the SAME semantic field (official 7/2025
  問1-2 辛い → あまい/にがい/しぶい; 問1-5 収まった → さだまった/しずまった/
  やすまった — such distractors frequently do NOT share the target's kanji).

Both branches are legal. Forbidden is the grab-bag that satisfies neither:
いたわる's distractors must not be ことわる/さわる/かわる (readings of
断る/触る/代わる — kanji sharing nothing with 労, fields sharing nothing with
"care for"; test 4 shipped exactly that). A one-branch reading of this rule is
what produced it: when the "same kanji" branch is empty for a drawn target, the
next step is inventing non-words, never widening to unrelated words.
**Scope:** branch (b) is the 訓読み branch. For a 音読み compound target (才能,
起床, 概要 — no okurigana printed), official distractors are 清濁/長短
derivations of the key's own on-reading and are *not* words; that branch and its
verification are step 6 of the RESOLVE procedure below.

### A spelling with TWO 訓読み: key the LOWER-graded one; never print the other

Some headwords are graded twice under one spelling — `潜る(くぐる)` at N1 beside
`潜る(もぐる)` at N2, and ~110 other entries across the slices. Two binding
consequences:

1. **The key must be the reading the corpus grades lower.** Keying the harder
   member turns the item into "which reading did the examiner mean" — an N1
   discrimination wearing an N2 target.
2. **The other reading may not appear in the option set at all** — it looks like
   a branch-(a) distractor but is a second correct pronunciation of the printed
   string, so the examinee is asked to guess intent, not to read.

Measured: all 35 current-era 問題1 items (12/2022–12/2025, 14 訓読み) — ZERO put
a target's alternative reading in its own option set. Decisive case: 7/2025-2,
辛い carries からい and つらい and official offered あまい/にがい/しぶい.
**Procedure:** look the spelling up in the openjlpt vocab slices before writing
options, and record BOTH readings and levels on the 問題1 source line:
`くぐる=潜る[N1] / もぐる=潜る[N2] → key もぐる`. A pool entry naming the harder
reading is a **pool** defect: send it back to `exam-blueprint` (kanji_reading
validity rule) rather than repairing the option set. Shipped counter-example:
tests/2 問題1-4 prints 潜る, keys くぐる, offers もぐる — its key note documented
the trap as if it were a feature. `check_mondai1_key_band()` fails both halves.

### Build the set BEFORE you accept the target — reject the target, never the rule

The three constraints (conjugation lock + real word + one of the two branches)
intersect to nothing for some pool entries; then the target is undrawable, not
negotiable. In order: (1) write the target's okurigana and the word class it
locks; (2) list the target kanji's other readings and same-radical look-alikes
in that class → branch (a) candidates; (3) if fewer than three, list real N2
words of the same class in the target's semantic field → branch (b) candidates;
(4) **if (a)+(b) still yield fewer than three real words, STOP — report the
target as undrawable and ask `exam-blueprint` to re-draw it.** Do not invent a
word, do not widen the field to "any ～わる verb", do not ship near-misses plus
filler. Worked empty case — test 4's 「労わる」: okurigana locks ～わる; 労 reads
only ロウ/いたわ(る)/ねぎら(う) and no look-alike gives a ～わる verb, so (a)={};
every real ～わる verb (ことわる・かわる・くわわる・まじわる・さわる…) is in an
unrelated field, so (b)={}. The paper shipped invented non-words, and a previous
fix round had already shipped the unrelated-kanji set — two failures on one
undrawable target.

### All four readings must RESOLVE — look them up, do not judge them

「実在語のみ」 was already a rule and test 4 still shipped がいり/そうじる/
うんじる, because nothing said WHERE to look. It is a lookup with two branches,
because official papers treat 音読み and 訓読み targets differently — measured
over all 35 current-era 問題1 items (`references/official_calibration.md` §5):

| Target | n | What the distractors are |
|---|---|---|
| **訓読み** (okurigana printed, or a single-kanji word) | 12 | **real words, every option, no exception** — same word class and conjugation as the key (争って → four 五段 ～って), usually the same semantic field; frequently not sharing the target's kanji. |
| **音読み compound** | 23 | **predominantly non-words** — 清濁 (さいのう→ざいのう), 長短 (きしょう→きしょ), ん⇄う (のうやく→のんやく) derivations of the key's own on-reading. But ~5 of 23 mix in real homophone words (握手→拍手, 討論→議論, 実践→実験, 刑事→検事/幹事, 衣装→以上), and one set is four real compounds (7/2024-2 分析 → 分解/分節/分割). |

Both blanket rules are wrong ("every option a dictionary word" fails 23/35;
"音読み distractors must be non-words" fails ~6). The invariant is directional:

> **A 訓読み set may never contain a non-word. A 音読み set may — but only as a
> derivation of the key's own reading (清濁 / 長短 / ん⇄う).**

The operational procedure:

1. **Reduce each option to dictionary form** (さだまった → さだまる; the
   conjugation lock has already forced all four into one class).
2. **Run all four through the openjlpt indices** — vocab `word`/`reading` fields
   plus kanji `kunyomi` (dots and leading `-` stripped). From the workspace root:

   ```bash
   python3 -c "
   import json,sys;B='.agents/exam-blueprint/references/openjlpt';V={};K={}
   for lv in ('n1','n2','n3'):
    for e in json.load(open(f'{B}/vocab-{lv}.json')):
     for k in (e['word'],e['reading']):
      if k: V.setdefault(k,set()).add(e['word']+'['+e['level']+']')
    for e in json.load(open(f'{B}/kanji-{lv}.json')):
     for r in e['kunyomi']: K.setdefault(r.replace('.','').lstrip('-'),set()).add(e['character']+'['+e['level']+']')
   for a in sys.argv[1:]: print(a, sorted(V.get(a,())) or sorted(K.get(a,())) or 'MISS')
   " さだまる しずまる おさまる やすまる
   ```
3. **A HIT is the evidence**: write the returned headword into the 問題1 source
   line — `さだまる=定まる[N1]`, `あまい=甘[N2 kunyomi]` — plus the branch label
   each option satisfies (`[同漢字]` or `[同分野]`). The source is whatever the
   lookup returned — run it; never write the spelling from memory.
4. **A MISS is not a verdict, it is a debt.** The slices hold 7,040 vocab
   entries (~790 with an empty `reading`) and the kanji lists stop at N3, so
   real words miss (やすまる=休まる — an official distractor — and こうじる=講じる
   both MISS). On a miss, write the option's kanji spelling, confirm the reading
   in a second source (`refs/Shinkanzen/` or the 常用漢字表 音訓), record it as
   `やすまる=休まる[SK]`.
5. **If no spelling can be written, the reading is invented — delete the
   option.** がいり/そうじる/うんじる all MISS and have no spelling: 概 reads
   ガイ/おおむ.ね, 要 reads ヨウ, 損 reads ソン, so none is a reading of its
   target nor a derivation of the key. (そうじる is the one defensible member —
   ん→う is a real manipulation; the set still shipped two fabrications.)
6. **音読み targets: every option is EITHER a real word OR a derivation.** A
   real homophone compound is official practice — record its headword like any
   HIT. A non-word is legal only as a derivation of the key's own reading; write
   the derivation next to it on the same line: 清音⇄濁音 (`さいのう→ざいのう`),
   長音⇄短音 (`きしょう→きしょ`), ん⇄う (`のうやく→のんやく`), or another real
   on-reading of the target's own kanji / same-radical look-alike. An option
   with neither a headword nor a derivation is fabricated — replace it. (In a
   訓読み set this branch does not exist: every option is a real word, full stop.)
7. **If the 解説 gives an etymology or names the trap** (「労う＝ねぎらう」), it
   must quote the headword the lookup returned, not a form assembled while
   writing the cell.

**NO GATE CHECKS THIS.** An earlier version claimed `make check` WARNs on a
non-listed reading; it does not — the gate touches `openjlpt/kanji-n2.json` only
to assert the file exists. Three invented non-words shipped in test 4 without a
warning. Until the QA work-list item `GATE-BLIND` lands, the written
source-and-branch line **is** the check — the author's, not the gate's. A
distractor with no writable branch label must be replaced; a distractor that is
not a real word must never be written at all — test 4's "repair" of the 労わる
set was もてあそわる/まねわる/ひるがえわる with invented spellings
(弄わる/招わる/翻わる), a worse failure than the set it replaced.

### The target's spelling must match its openjlpt headword

問題1 tests a reading off a printed spelling, so non-standard okurigana changes
the item: test 4 printed 「労わる」 (from `pools.json`) where `vocab-n1.json`
heads it 「労る」 — and the extra 「わ」 is what locked the option class. On a
mismatch, fix `pools.json`, then re-sample; re-spelling the stem alone leaves
the pool to re-draw the defect next test.

### The KEY must be N2 — and no gate checks that for vocabulary

The band gate reads `references/level_band_grammar.txt`, which covers 問題7–9
grammar only. Before shipping any 問題1–6 item, look the key up in the openjlpt
vocab slices: a key that is an N3 headword and absent from the N2 list is too
easy — test 4 keyed 賢い/かしこい (N3). Treat the lookup as a question, not a
ruling: that corpus labels ordinary N2 words (把握・転換・審査・じっくり) "N1",
so confirm the verdict against `refs/Shinkanzen/` before replacing anything.

## 問題2 (表記)

Official items use a **2×2 component matrix**: take the correct 2-kanji
compound and swap EACH kanji independently for a visually/structurally similar
wrong one, so all four options share the same two-character skeleton
(かいこう → 開港/開向/回港/回向; のうこう → 濃厚/農厚/濃高/農高; かくじゅう →
拡張/拡充/各充/各張). Do not vary only one position while holding the other
fixed. **Non-words and pseudo-compounds are normal and expected in 表記
distractors** (official July 2025 ships 液って/温って/汗って and 支接/施接/支設)
— they need not be dictionary headwords, but must test orthographic component
precision. ⚠ Worked examples in this file are patterns — never ship an
example's target word or option set.

**The stem's kana is the key's reading.** The 音/訓 reading printed in the 問題2
stem must equal the reading of the keyed kanji option (しひん 下品 would miskey:
下品 reads げひん). Write the stem kana from the key option's reading, then
verify every non-key option parses as the same kana skeleton (かいこう →
開港/開向/回港/回向). A stem kana no option reads is a gate-level automatic-fail
class (shipped in 20260807_2 item 6: しひん ≠ 下品).

## 問題3 (語形成)

諸〜, 〜化, 準〜, 〜済み, 〜制, 未〜, 〜性, and the four real negation prefixes
非〜/無〜/未〜/不〜 — there is no fifth; 迷〜 is not a real negation prefix and is
listed in `references/banned_collocations.txt`. Distractors must be real N2
affixes of the same functional family. It is NOT required that all four attach
plausibly to the stem (official 7/2025 問3-11: 教育 → 則/理/論/規, where only
教育観 attaches) — but every affix must be a real, standard morpheme, never an
invented one like 迷〜.

## 問題4 (context)

N2 nouns/adverbs: 難航, 発足 (distractor: 成立), かろうじて, うんざり, てきぱき,
需要. Distractors share the semantic field — and the functional category, per
the core sniff-test rule and category line.

**The stem is a BLANK, never the answer.** Every 問題4 stem must carry （　）
in the slot and must not print the answer word anywhere in the sentence
(official booklets ship every stem with （　）). A stem that prints the answer
is a gate-level automatic-fail class (shipped in 20260807_2, items 14–20). The
（　） is the printed sentence's only gap — the instruction line reads
「（　）に入れるのに最もよいものを…」.

**Never key a near-synonym of the answer.** Context words are N2 nouns/adverbs
chosen so exactly one option fits the sentence; a distractor that is a
near-synonym the stem also accepts (コンクール vs コンテスト in the same
sentence) makes the item double-answerable (shipped in 20260807_2 item 14). If
the stem accepts two options, the target or the stem must change — reject the
item, never the rule.

## 問題5 (paraphrase)

The stem contains the HARD word (あいにく, 妥当, ありふれた, くたくた, 重宝);
options are simpler. Never the reverse. Substitutability check: core Item
integrity #12.

## 問題6 (用法)

1 correct sentence + 3 that are grammatical but misuse the word's
collocation/domain (妥協, 発揮, 解消, 募集, あふれる). "Wrong sentences must be
tempting, not absurd" was a prohibition-with-examples and 4/4 papers reproduced
the defect anyway (t1 28 解消 — three 消す-domain sentences; t2 27/28; t3 26,
28, 29, 30; t4 26 解消, plus the mirror failure — 「契約を解消」, a REAL
collocation and therefore a second correct sentence). The procedure, per wrong
sentence, in this order:

1. Write a sentence in which the KEY word is *correct*.
2. Break exactly **one** thing **inside the word's own domain** — swap the
   object for another the domain contains but the word does not take, or shift
   register. Never leave the domain: an out-of-domain sentence is eliminable
   without knowing the word.
3. **Search the result.** If the collocation is attested, it is a second correct
   sentence, not a distractor — back to step 2.

Worked example for 解消, spanning both failure edges and the target:

| Sentence | Verdict |
|---|---|
| ✅『長年の誤解が解消した』 | the correct option |
| ✗『部屋の電気を解消した』 | **domain violation — banned** (消す's domain; dies on sight) |
| ✗『契約を解消した』 | **attested — banned** (a second correct answer) |
| ✓『渋滞を解消に導いた』 | **the target band: right domain, wrong collocation** |

**Length:** official option sentences measure mean 25.0, median 25, range 9–35
JP chars (current era, n=136; `official_calibration.md` §7 — the old 「~27」 was
a mild over-estimate). Tests 1–4 averaged ~19, so the gap is real, but the mean
is not the rule and a 9-char option sentence is official: one short line among
four is fine, four short lines is the drill. Give each sentence a who/when/what
unless brevity is doing work — a telegram-length misuse line leaves no room for
the situation that makes a wrong collocation tempting.
