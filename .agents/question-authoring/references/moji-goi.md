# 文字・語彙 (問題1–6) — construction rules

Section reference for the `question-authoring` skill. Read the core
`SKILL.md` alongside this file — it carries the N2-band rule, the sniff
test, the mandatory functional-category line, and item integrity (問題1
option-form and conjugation-lock are Item integrity #13–14). This file owns
the 問題1 two-branch distractor rule and every 問題1–6-specific rule.

## 問題1 (漢字読み)

Test N2-band words: 交渉, 慌てる, 妨げる, 潔い, 措置, 傾向, 効率, 険しい.
Build distractors from REAL confusions — reading traps (措置(そち) vs
しょち/そうち), homophone kanji sets (納める/収める/治める/修める,
敗れる/破れる), same-radical fakes (険/検/剣/験).

### Underline the WHOLE word, okurigana included

The underline is the bold span: `**収まった**`, never `**収**まった` or a
bolded particle (`**生じる**`, never `**に**生じる`). Official July 2025
marks `**才能**`, `**辛い**`, `**刑事**`, `**起床**`, `**収まった**` — the
inflectional tail sits inside the mark, and 問題2 does the same with kana
spans (`**しめって**`). Corroborated archive-wide (`official_calibration.md`
§5).

**The defect is splitting a word, not the character count.** Forbidden:
`**爆**ぜる`, asking for a bare character's reading. Legitimate: a whole
word that happens to be one kanji — official draws them (腕, 柱, 針; 柱's
set ゆか/かべ/たな is an ordinary 訓読み field set). A single-kanji *word* is
a normal target; a single-kanji *fragment* of a longer word is not.

**Okurigana non-exposure:** when the target has okurigana (生じる, 慌てる,
逃す, 潜る), the tail is visibly printed in the stem, so **all four options
MUST share that exact okurigana** (`生じる` options all end `〜じる`) —
offering `しょうする`/`せいする` beside a printed `じる` tail eliminates them
on sight.

### 2-kanji on-reading compounds: the 2×2 Cartesian product matrix

For 2-kanji 音読み targets (矛盾, 縮小, 概要, 効率, 措置, 交渉), official
tests each kanji's reading independently: kanji 1 reading A (correct) vs B
(confused — 清濁/長短/同音/同類漢字), kanji 2 reading C vs D → four options
`{AC, AD, BC, BD}`.

- **矛盾(むじゅん):** A=む,B=ぶ; C=じゅん,D=じゅう → {むじゅん,むじゅう,ぶじゅん,ぶじゅう}. *Defect:* `むじん` (arbitrary 3rd ending breaks 2×2).
- **縮小(しゅくしょう):** A=しゅく,B=じゅく; C=しょう,D=しょ/じょう → complete grid, never mix without forming it.
- **概要(がいよう):** A=がい,B=かい; C=よう,D=ゆ → {がいよう,がいゆ,かいよう,かいゆ}.

### The two-branch rule — same kanji OR same semantic field (the ONLY statement)

Every distractor shares the target's word form/conjugation class (Item
integrity #13–14; a real word per the RESOLVE procedure below) AND is either:

- **(a) 同漢字** — a reading of the target's own kanji or a same-radical/
  visual-component kanji (措置: そち/しょち/そうち), OR
- **(b) 同分野** — a real N2 word in the SAME semantic field (official 7/2025
  辛い→あまい/にがい/しぶい; 収まった→さだまった/しずまった/やすまった — often
  sharing no kanji with the target).

Both branches are legal; forbidden is a grab-bag satisfying neither
(いたわる's distractors must not be ことわる/さわる/かわる — unrelated kanji,
unrelated field). When branch (a) is empty for a drawn target, the fix is
never inventing non-words. **Scope: branch (b) is the 訓読み branch.** For a
音読み compound target (才能, 起床, 概要), official distractors are
清濁/長短 derivations of the key's own on-reading and are NOT words — that
branch is step 6 of the RESOLVE procedure below.

### A spelling with TWO 訓読み: key the LOWER-graded one; never print the other

Some headwords are graded twice — `潜る(くぐる)` at N1 beside `潜る(もぐる)`
at N2 (~110 entries across the pool slices).

1. **The key must be the reading the corpus grades lower** — keying the
   harder member turns the item into "which reading did the examiner mean".
2. **The other reading may not appear in the option set at all** — it's a
   second correct pronunciation of the printed string, not a distractor.

Measured: all 35 current-era 問題1 items (14 訓読み) — ZERO put a target's
alternative reading in its own option set (decisive case: 7/2025-2, 辛い
carries both からい and つらい; official offered あまい/にがい/しぶい).
**Procedure:** check the spelling against Shin Kanzen N2-Goi/N2-Kanji and
Soumatome N2 語彙/漢字 before writing options, and record both readings and
levels on the source line: `くぐる=潜る[N1] / もぐる=潜る[N2] → key もぐる`. A
pool entry naming the harder reading is a **pool** defect — send it to
`exam-blueprint` (kanji_reading validity rule), don't repair the option set.
**2026-08-11: no automated gate for this anymore** (`check_mondai1_key_band()`
was deleted with `openjlpt`) — verified by author/QA reading the textbook
pages directly.

### Build the set BEFORE you accept the target — reject the target, never the rule

The three constraints (conjugation lock + real word + one of the two
branches) intersect to nothing for some pool entries — then the target is
undrawable, not negotiable. In order: (1) write the target's okurigana and
locked word class; (2) list same-kanji/look-alike readings → branch (a)
candidates; (3) if fewer than three, list same-field real N2 words →
branch (b) candidates; (4) **if (a)+(b) still yield fewer than three real
words, STOP** — report undrawable and ask `exam-blueprint` to re-draw. Do
not invent a word or widen the field. Worked empty case: 「労わる」 — 労 reads
only ロウ/いたわ(る)/ねぎら(う), no look-alike gives a ～わる verb (a={}); every
real ～わる verb is an unrelated field (b={}).

**"Ask exam-blueprint to re-draw it" means run `sample_items.py --reroll
<category>` — never hand-pick a replacement, even a real N2 word.**
`20260817_1` found `居酒屋(いざかや)` undrawable this way and hand-swapped in
`潔い(いさぎよい)` instead of rerolling — shipped a repeat drawn only 7 tests
earlier, deep inside `kanji_reading`'s real cooldown, because a hand
substitution never touches the ledger `--reroll` updates
(`exam-blueprint` "Rotation model"). A hand-picked word is unverifiable
against rotation no matter how sound its distractor set is.

### All four readings must RESOLVE — check them against the books, do not judge them

**2026-08-11: this ran as a scripted `openjlpt` lookup; that corpus is
deleted.** Both Shinkanzen and Soumatome are scanned images with no text
layer (confirmed via `pdftotext`) — no grep-able index exists. This is now
an author-diligence procedure: read the relevant page via the Read tool's
`pages` support, or use trained vocabulary knowledge cross-checked against
these books (or, for a miss, the archive's OCR'd `booklet.md`/`key.md`). The
rules didn't change — only the verification mechanism did.

Every option must be a real word, verified with two branches, because
official treats 音読み and 訓読み targets differently (all 35 current-era
問題1 items, `official_calibration.md` §5):

| Target | n | What the distractors are |
|---|---|---|
| **訓読み** (okurigana printed, or single-kanji) | 12 | **real words, every option, no exception** — same class/conjugation as the key, usually same field; frequently not sharing the target's kanji. |
| **音読み compound** | 23 | predominantly non-words — 清濁 (さいのう→ざいのう), 長短 (きしょう→きしょ), ん⇄う (のうやく→のんやく) derivations of the key's own reading. ~5 of 23 mix in real homophones (握手→拍手, 討論→議論); one set is four real compounds (分析→分解/分節/分割). |

Both blanket rules are wrong ("every option a dictionary word" fails 23/35;
"音読み distractors must be non-words" fails ~6). The invariant is
directional: **a 訓読み set may never contain a non-word; a 音読み set may,
but only as a derivation of the key's own reading.**

Procedure: (1) reduce each option to dictionary form (さだまった→さだまる);
(2) check all four against Shinkanzen/Soumatome pages, per option; (3) a
HIT is evidence — write the confirmed headword + branch label into the
source line (`さだまる=定まる[N1, Shinkanzen p.NNN]`), citing whichever
source you actually checked; (4) a MISS is a debt — confirm via 常用漢字表
音訓 or the archive, record `やすまる=休まる[常用音訓]`; (5) if no spelling
confirms anywhere, the reading is invented — delete the option (がいり/
そうじる/うんじる have no confirmable spelling); (6) for 音読み targets, every
option is EITHER a real word OR a derivation (清濁/長短/ん⇄う of the target's
own reading) — nothing else; (7) a 解説 etymology must quote the headword
actually confirmed in step 3.

`make check` has never WARNed on a non-listed reading, and even the old
`openjlpt`-existence check is gone — the written source-and-branch line IS
the check, the author's, not the gate's. A distractor with no writable
branch label must be replaced; inventing spellings (弄わる/招わる/翻わる) is a
severe defect.

### The target's spelling must match its headword in Shinkanzen/Soumatome

問題1 tests a reading off a printed spelling — printing 「労わる」 where the
textbook headword is 「労る」 changes the item (the extra 「わ」 locks the
option class). Fix `pools.json`, then re-sample; re-spelling the stem alone
leaves the pool to re-draw the defect next test.

### The KEY must be N2 — and no gate checks that for vocabulary

The band gate reads `level_band_grammar.txt`, which covers 問題7–9 grammar
only. Check every 問題1–6 key against Shinkanzen N2-Goi/N2-Kanji and
Soumatome N2 語彙/漢字 — a headline N3-or-below word absent from either N2
volume is too easy (avoid 賢い/かしこい). No vendored word list exists
anymore to query — this is a judgment call.

## 問題2 (表記)

Official uses a **2×2 component matrix**: swap EACH kanji of a correct
2-kanji compound independently for a lookalike/homophone → `{A,B}×{C,D}→
{AC,AD,BC,BD}`. Pseudo-compounds and non-words are standard and expected —
they need not be dictionary headwords (official ships `支接/施接/支設`,
`液って/温って/汗って`).

- **げひん(下品):** A=下,B=不; C=品,D=晶 → {下品,下晶,不品,不晶}. *Defect:* mixing in `等`, omitting B+D.
- **うんが(運河):** A=運,B=雲; C=河,D=賀 → {運河,運賀,雲河,雲賀} — 運=ウン, 雲=ウン, 河=ガ, 賀=ガ, so all four parse as the printed うんが. *Defect:* an arbitrary 3rd kanji like `転`. **Do NOT use D=海:** {運海,雲海} read うんかい, not うんが, so two options die on reading alone and the item collapses to 運 vs 雲 (`20260817_3` 問題2-9 shipped exactly that — and this file taught it as the model set until 2026-08-19). A complete component grid is NOT the check; the kana skeleton is.
- **げた(下駄):** A=下,B=不; C=駄,D=太 → {下駄,下太,不駄,不太}. *Defect:* a non-standard glyph like `楪`.
- **かいこう(開港):** {開,回}×{港,向}. **のうこう(濃厚):** {濃,農}×{厚,高}.

### Every printed glyph must be 常用 — `references/joyo_kanji.txt` decides it

**Every constituent kanji glyph must be a legitimate, standard 常用/N2
kanji** — banned: obscure/alien glyphs (`惰楪`'s `楪`). **The authority is
`references/joyo_kanji.txt`**, the 2136 characters of the 2010 常用漢字表, the
way `level_band_grammar.txt` is the authority for 問題7–9's band. Check the key
and all three distractors against it, character by character, before the item
is written. `check_moji2_option_glyphs()` reads the same file and FAILs any
問題2 option — and any 問題1 **printed target** — carrying a glyph outside it.

The file settles a question judgement kept getting wrong: `20260817_3` shipped
問題2-8 keyed 「飢饉」 through **three** QA rounds under the prose rule above, and
it was caught only when a fresh reviewer checked the glyph inventory by hand
(round 3, R3-1). 「饉」 is not 常用, and 「飢」 occurs zero times across all 31
official sittings. `20260811_1` is exempted **by name**
(`MOJI_GLYPH_GRANDFATHERED`) for 問題2-9's 「曳帰す」/「曳返す」 — invented
non-words on 表外 「曳」, shipped the day before the rule existed — and prints the
same measurement as a WARN; repairing it means re-drawing and re-authoring that
item. Read the set in `tools/check_consistency.py` for who is currently exempt,
not this sentence.

**A 表外 glyph is a POOL defect only in `orthography`.** 問題2 is the one item
type that must print its options in kanji, so there is no kana escape: an
`orthography` entry whose spelling needs a 表外 character is undrawable — delete
it and `sample_items.py --reroll orthography`, never hand-substitute a target
(`exam-blueprint` §pool hygiene). **Everywhere else, the repair is kana, not
deletion.** `check_pool_glyph_inventory()` currently WARNs 14 pool entries
(蕎麦, 凌ぐ, 汲む, 繋がる, 呑気, 卑怯, 儲ける, 揃える, 詫びる, 几帳面だ …) — those
are legitimate N2 **words** whose *kanji spelling* is off-band, and in 問題4/5/6
you print them in kana, as official does. That WARN is a standing list, not a
deletion list: judge it per category.

**Single-kanji stems with okurigana** (けわしい→険しい): all four share the
exact okurigana, and the kanji options come from the same phonetic
radical/visual set (`{険しい,験しい,検しい,剣しい}`). **Native compound
items** (やぬし→家主): every option must be legitimate standard kanji
(`{家主,宅主,宿主,店主}`) — banned: absurd combinations (`守柱`).

**The stem's kana is the key's reading** — write the stem kana from the key
option's reading, verify every non-key option parses as the same kana
skeleton (かいこう → 開港/開向/回港/回向). A stem kana no option reads is an
automatic-fail class.

**Procedure — write the reading of each COMPONENT before you accept the
grid.** Two columns, one line per component: `A=運(ウン) B=雲(ウン)` /
`C=河(ガ) D=賀(ガ)`. Every column must be readings-identical; if any
component's on-reading differs from its partner's, the grid is dead
regardless of how good the lookalike is. Then read the four products back
against the stem kana. Doing this on paper is the check — "the grid is
complete" is not, and neither is "the kanji look alike."

## 問題3 (語形成)

諸〜, 〜化, 準〜, 〜済み, 〜制, 未〜, 〜性, and the four real negation
prefixes 非〜/無〜/未〜/不〜 — there is no fifth; 迷〜 is not real and is
banned (`references/banned_collocations.txt`). Distractors must be real N2
affixes of the same functional family. Not required that all four attach
plausibly to the stem (official 教育→則/理/論/規, only 教育観 attaches) — but
every affix must be a real, standard morpheme.

## 問題4 (context)

N2 nouns/adverbs: 難航, 発足 (distractor: 成立), かろうじて, うんざり,
てきぱき, 需要. Distractors share the semantic field AND functional category
(core sniff-test rule).

**The stem is a BLANK, never the answer** — every stem carries （　）and
never prints the answer word elsewhere (a printed answer is an
automatic-fail class).

**Never key a near-synonym of the answer** — a distractor the stem also
accepts (コンクール vs コンテスト in the same sentence) makes the item
double-answerable. If the stem accepts two options, change the target or
stem — never defend the item.

## 問題5 (paraphrase)

The stem contains the HARD word (あいにく, 妥当, ありふれた, くたくた, 重宝);
options are simpler, never the reverse (Item integrity #12).

**Each option must be idiomatic ON ITS OWN, not merely survivable in the
stem.** The swap test only asks whether the sentence still parses; read each
of the four options as a bare phrase with the stem covered and ask whether a
native writer would produce it unprompted. **When the target IS the natural
collocate of the frame, do not build options by substituting into that
frame — change the frame.** `20260817_3` 問題5-21 keyed 器用だ and shipped
「手先が上手だ」: the idiomatic phrase is 手先が**器用**, which is unusable
because it is the target, so substituting into 「手先が〜」 can only produce
marked wordings. The fix was a different frame — 「細かい作業が得意だ」.

**Katakana headwords are rare on purpose** — the archive draws one in only
3/35 current-era 問題5 items (`official_calibration.md` §12);
`sample_items.py` now draws at that measured rate instead of the pool's raw
~30% share. A paper with zero katakana targets in 問題5/6 is the archive's
usual shape, not a thin draw.

## 問題6 (用法)

1 correct sentence + 3 grammatical-but-wrong-collocation/domain misuses
(妥協, 発揮, 解消, 募集, あふれる). Wrong sentences must be tempting, not
absurd (avoid three 消す-domain sentences for 解消) — and must not be a
second REAL collocation (「契約を解消」 is attested, so it's a second correct
answer, not a distractor). Per wrong sentence: (1) write it correct; (2)
break exactly ONE thing INSIDE the word's own domain — never leave the
domain; (3) search the result — if attested, it's a second correct answer,
back to step 2.

| Sentence (解消) | Verdict |
|---|---|
| ✅『長年の誤解が解消した』 | correct option |
| ✗『部屋の電気を解消した』 | domain violation — banned (消す's domain) |
| ✗『契約を解消した』 | attested — banned (second correct answer) |
| ✓『渋滞を解消に導いた』 | the target band: right domain, wrong collocation |

**Length:** mean 25.0, median 25, range 9–35 JP chars (n=136,
`official_calibration.md` §7) — a 9-char option is official, so short alone
isn't a defect. Give each sentence a who/when/what unless brevity is doing work.

### A word's OTHER attested sense is still that word — check it too

Step 3's search must cover EVERY sense the word carries, not just the one
the KEY sentence uses. `20260811_1` shipped 落ち着く keyed on "person calms
down" with a wrong option reading 「試験の点数が落ち着いてきた」 — but 落ち着く
also has an attested "fluctuating VALUE settles" sense (相場が落ち着く), and a
test score is a fluctuating value, so the "wrong" sentence is a live
second-answer risk. For any multi-sense verb/adjective, name EACH sense
before writing distractors and check step 3 against all of them.

### All four options share the SAME word-form of the headword

If the headword is a suru-verb (宣伝する), every option bolds a conjugated
verb form — never mix a bare-noun option against three verb-form ones
(`20260811_1`'s 問題6-26 shipped exactly this). The same binds bare-noun
headwords: if the headword is a plain noun (民間), every option uses that
identical printed word or a bare inflection — never let one option alone
derive a 〜的/〜化/〜性 form while the others stay bare (`20260817_2`'s
問題6-28 shipped 民間**的な**選挙 against three bare-民間 options — the same
shape-tell on a noun instead of a verb).
