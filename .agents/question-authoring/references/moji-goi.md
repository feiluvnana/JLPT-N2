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

### Underline the WHOLE word, okurigana included (no particle, no okurigana split, no okurigana leak)

In the Markdown the underline is the bold span: write `**収まった**`, never
`**収**まった`, and never bold a surrounding particle like `**に**生じる` (write
`**生じる**`). Official July 2025 (`refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`,
問1) marks `**才能**`, `**辛い**`, `**刑事**`, `**起床**`, `**収まった**` — the
inflectional tail sits *inside* the mark in both okurigana items, and 問題2 does
the same with kana spans (`**しめって**`). Corroborated across the archive
(`references/official_calibration.md` §5, with its §0 caveat that the archive is
a Word-typeset reproduction, consistent across sittings).

**The defect is splitting a word, not the character count.** Forbidden: marking
part of a word and leaving the rest outside — e.g. `**爆**ぜる`, which
asks for a bare character's reading and lets ばく/はつ compete with はぜる.
Legitimate: a whole word that happens to be one kanji — official draws them
(腕 12/2023-1, 柱 12/2025-1, 針 12/2012; 柱's set ゆか/かべ/たな is an ordinary
訓読み semantic-field set). A single-kanji *word* is a normal target; a
single-kanji *fragment* of a longer word is not.

**Okurigana non-exposure:** When the target has okurigana (e.g. 生じる, 慌てる,
逃す, 潜る), the hiragana tail is visibly printed in the stem. Therefore:
1. **All four options MUST share the exact same okurigana as printed in the stem** —
   `生じる` options must all end in `〜じる` (`1. せいじる  2. しょうじる  3. そうじる  4. しょじる`).
2. **Never vary the okurigana in the options** — offering `しょうする` or `せいする`
   beside `生じる` is a broken item: examinees see `じる` printed in hiragana right
   in the stem sentence, which immediately eliminates `〜する` options on sight.

### 2-kanji on-reading compounds: the 2×2 Cartesian product matrix ({A, B} × {C, D} → {AC, AD, BC, BD})

For 2-kanji 音読み compound targets (e.g. 矛盾, 縮小, 概要, 効率, 措置, 交渉):
Official items test each kanji's reading independently using a complete **2×2
Cartesian product matrix**:
- **Kanji 1 on-reading:** A (correct reading) vs B (confused on-reading / 清濁・長短・同音/同類漢字 reading).
- **Kanji 2 on-reading:** C (correct reading) vs D (confused on-reading / 清濁・長短・同音/同類漢字 reading).
- **Four options:** {AC, AD, BC, BD} (permuted into the prescribed key slot).

**Worked examples:**
- **矛盾 (むじゅん):** A=む, B=ぶ; C=じゅん, D=じゅう → {1. むじゅん, 2. むじゅう, 3. ぶじゅん, 4. ぶじゅう}.
  *Defect:* options like `むじん` introduce an arbitrary 3rd ending and break the 2×2 symmetry.
- **縮小 (しゅくしょう):** A=しゅく, B=じゅく; C=しょう, D=しょ (or じょう) → {1. しゅくしょう, 2. しゅくしょ, 3. じゅくしょう, 4. じゅくしょ}.
  *Defect:* mixing `しゅくじょう` with `しゅくしょ` without forming a complete 2×2 grid.
- **概要 (がいよう):** A=がい, B=かい; C=よう, D=ゆ → {1. がいよう, 2. がいゆ, 3. かいよう, 4. かいゆ}.

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
"care for"). A one-branch reading of this rule is
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
validity rule) rather than repairing the option set. Avoid documenting
the trap as if it were a feature when stem prints 潜る, keys くぐる, and offers もぐる. `check_mondai1_key_band()` fails both halves.

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
filler. Worked empty case — e.g. 「労わる」: okurigana locks ～わる; 労 reads
only ロウ/いたわ(る)/ねぎら(う) and no look-alike gives a ～わる verb, so (a)={};
every real ～わる verb (ことわる・かわる・くわわる・まじわる・さわる…) is in an
unrelated field, so (b)={}. Avoid shipping invented non-words or unrelated-kanji sets on an undrawable target.

### All four readings must RESOLVE — look them up, do not judge them

Every option must be a real word (avoid non-words like がいり/そうじる/うんじる),
by performing a lookup with two branches,
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
4. **A MISS is a debt.** The slices hold 7,040 vocab
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

An earlier version claimed `make check` WARNs on a
non-listed reading; it does not — the gate touches `openjlpt/kanji-n2.json` only
to assert the file exists. Invented non-words must never be written without a
warning or check. Until the QA work-list item `GATE-BLIND` lands, the written
source-and-branch line **is** the check — the author's, not the gate's. A
distractor with no writable branch label must be replaced; a distractor that is
not a real word must never be written at all — repairing an item like 労わる
by writing もてあそわる/まねわる/ひるがえわる with invented spellings
(弄わる/招わる/翻わる) is a severe defect.

### The target's spelling must match its openjlpt headword

問題1 tests a reading off a printed spelling, so non-standard okurigana changes
the item: printing 「労わる」 (from `pools.json`) where `vocab-n1.json`
heads it 「労る」 — and the extra 「わ」 is what locked the option class. On a
mismatch, fix `pools.json`, then re-sample; re-spelling the stem alone leaves
the pool to re-draw the defect next test.

### The KEY must be N2 — and no gate checks that for vocabulary

The band gate reads `references/level_band_grammar.txt`, which covers 問題7–9
grammar only. Before shipping any 問題1–6 item, look the key up in the openjlpt
vocab slices: a key that is an N3 headword and absent from the N2 list is too
easy — avoid keying N3 words like 賢い/かしこい. Treat the lookup as a question, not a
ruling: that corpus labels ordinary N2 words (把握・転換・審査・じっくり) "N1",
so confirm the verdict against `refs/Shinkanzen/` before replacing anything.

## 問題2 (表記)

Official items use a **2×2 component matrix**: take the correct 2-kanji
compound and swap EACH kanji independently for a visually/structurally/phonetically
similar wrong one, so all four options form the complete Cartesian product
`{A, B} × {C, D} → {AC, AD, BC, BD}`.

### The 2×2 component matrix: {A, B} × {C, D} → {AC, AD, BC, BD}

- **Position 1 kanji:** A (correct kanji) vs B (confused / lookalike / homophone kanji).
- **Position 2 kanji:** C (correct kanji) vs D (confused / lookalike / homophone kanji).
- **Four options:** {AC, AD, BC, BD} (permuted into the prescribed key slot).
- **Pseudo-compounds and non-words are standard and expected in 表記:**
  They need not be dictionary headwords; their purpose is testing character-level
  orthographic precision (official July 2025 ships `支接/施接/支設` and `液って/温って/汗って`).

**Worked examples (patterns — do not ship exact examples):**
- **げひん (下品):** A=下, B=不; C=品, D=晶 (or 等) → {1. 下品, 2. 下晶, 3. 不品, 4. 不晶}.
  *Defect:* options like `下等, 下晶, 不品, 下品` fail the 2×2 symmetry by mixing `等` and `晶` and omitting B+D (`不晶` or `不等`).
- **うんが (運河):** A=運, B=雲; C=河, D=海 → {1. 運河, 2. 運海, 3. 雲河, 4. 雲海}.
  *Defect:* options like `雲海, 運河, 転海, 雲河` inject an arbitrary 3rd kanji `転` instead of completing the {運, 雲} × {河, 海} grid.
- **げた (下駄):** A=下, B=不; C=駄, D=太 → {1. 下駄, 2. 下太, 3. 不駄, 4. 不太}.
  *Defect:* options like `下太, 惰楪, 下駄, 不駄` break the 2×2 grid and use an alien, non-standard glyph `楪`.
- **かいこう (開港):** A=開, B=回; C=港, D=向 → {開港, 開向, 回港, 回向}.
- **のうこう (濃厚):** A=濃, B=農; C=厚, D=高 → {濃厚, 農厚, 濃高, 農高}.

### Constituent kanji legitimacy: real 常用/N2 kanji only (no alien or bizarre glyphs)

Even though pseudo-compounds are standard in the 2×2 matrix, **every single
constituent kanji glyph MUST be a legitimate, standard 常用 / N2 kanji**:
- **Banned:** Fabricating or using obscure, non-standard, or alien kanji (such as
  `惰楪`'s `楪`). Examinees are tested on standard Japanese orthography, not rare
  CJK dictionary curiosities.

### Single-kanji stem + okurigana items & Native compound items

1. **Single-kanji stems with okurigana (e.g. けわしい → 険しい, あやうい → 危うい, たくましい → 逞しい):**
   - All four options share the **exact same okurigana** (e.g. `〜しい`).
   - The four kanji options must be **legitimate standard kanji** from the same
     phonetic radical / visual confusion set: `{1. 験しい, 2. 険しい, 3. 検しい, 4. 剣しい}`
     (all four share the ケン reading and radical/component elements).
2. **Native kun-yomi / compound items (e.g. やぬし → 家主, ほのお → 炎, けはい → 気配):**
   - Every constituent kanji and distractor option must be **legitimate, standard, and plausible**:
     for `やぬし` (家主), use standard kanji ({家主, 宅主, 宿主, 店主} or {家, 宅} × {主, 守}).
   - **Banned:** Absurd, nonsensical combinations like `守柱` or `家柱` (random pillar compounds).

### The stem's kana is the key's reading

The 音/訓 reading printed in the 問題2 stem must equal the reading of the keyed
kanji option (しひん 下品 would miskey: 下品 reads げひん). Write the stem kana
from the key option's reading, then verify every non-key option parses as the
same kana skeleton (かいこう → 開港/開向/回港/回向). A stem kana no option reads
is a gate-level automatic-fail class (e.g. stem しひん paired with key 下品 which reads げひん).

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
is a gate-level automatic-fail class. The
（　） is the printed sentence's only gap — the instruction line reads
「（　）に入れるのに最もよいものを…」.

**Never key a near-synonym of the answer.** Context words are N2 nouns/adverbs
chosen so exactly one option fits the sentence; a distractor that is a
near-synonym the stem also accepts (e.g. コンクール vs コンテスト in the same
sentence) makes the item double-answerable. If
the stem accepts two options, the target or the stem must change — reject the
item, never the rule.

## 問題5 (paraphrase)

The stem contains the HARD word (あいにく, 妥当, ありふれた, くたくた, 重宝);
options are simpler. Never the reverse. Substitutability check: core Item
integrity #12.

**Katakana headwords are rare on purpose — do not add more for "variety."** The
archive draws a katakana target in only 3/35 current-era 問題5 items
(`references/official_calibration.md` §12); `exam-blueprint`'s
`sample_items.py` now draws `paraphrase`/`usage` at that measured rate instead
of the pool's raw ~30% katakana share. If a draw hands you a paper with zero
katakana targets in 問題5/6, that is the archive's usual shape, not a thin
draw to compensate for.

## 問題6 (用法)

1 correct sentence + 3 that are grammatical but misuse the word's
collocation/domain (妥協, 発揮, 解消, 募集, あふれる). "Wrong sentences must be
tempting, not absurd" is the rule (avoid three 消す-domain sentences for 解消,
plus the mirror failure — 「契約を解消」, a REAL
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
a mild over-estimate). Avoid short stems averaging ~19; target standard stem lengths.
Give each sentence a who/when/what
unless brevity is doing work — a telegram-length misuse line leaves no room for
the situation that makes a wrong collocation tempting.
