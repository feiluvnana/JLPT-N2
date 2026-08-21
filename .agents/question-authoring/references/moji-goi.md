# 文字・語彙 (問題1–6) — construction rules

Section reference for the `question-authoring` skill. Read the core `SKILL.md`
alongside this file — it carries the N2-band rule, the sniff test, the mandatory
functional-category line, and item integrity (問題1 option-form and
conjugation-lock are Item integrity #13–14). This file owns the stem contract,
the per-section composition quotas, and the 問題1 two-branch distractor rule.

**Every number here is printed by `python3 tools/goi_profile.py --baseline`** —
one parser, both corpora, 954 of 964 archive items (98.9 %). Do not retype a
number from memory: refresh it from the script, which is also what the gate
imports (`tools/check_consistency.py`). "official" = all 31 sittings, "cur" =
the 7 current-era sittings (12/2022–12/2025) the repo models; where the two
disagree the current-era figure is the tighter one and the one a quota uses.

---

# Part 0 — rules that bind every 大問

## The stem: one clause, one actor, and a person in it

問題1/2/5 test a reading, a spelling and a synonym. **Every character of context
beyond what disambiguates the target is reading load charged to a vocabulary
item** — and a candidate who cannot parse 「市は来年度の予算を見直し、」 then loses a
文字・語彙 mark for a 読解 reason. Measured 2026-08-21: our fourteen papers ran a
median 29-char 問題1/2/5 stem where every official sitting runs 15–21.5, and 7 %
comma-free where official runs 73 %. The section had turned into a passage.

| Rule (per paper) | official | cur | ours, 2026-08-21 | author to |
|---|---|---|---|---|
| median 問題1/2/5 stem, JP chars | 15–21.5 (med 18) | 15–17.5 | **21–32 (med 29)** | **17** |
| 問題1/2/5 stems with no 「、」 (of 15) | 47–93 % (med 73) | 60–93 % | **0–60 % (med 7 %)** | **≥9 (60 %)** |
| 問題1–5 stems carrying です・ます (of 25) | 2–11 (med 6) | 4–8 | **0–4 (med 1)** | **7** |
| …first-person stems (私/僕/自分…) | 0–4 | 1–4 | **0–2 (med 0)** | **≥1** |
| …stems whose ACTOR is an institution | 0–7 (med 2) | 0–3 | **0–9 (med 3)** | **≤2** |
| median 問題4 stem / longest single one | 19–37 / 47 | 26–34 / 44 | **24–64 / 75** | **30 / ≤44** |

Official, for the shape: 「この家の柱はしっかりしている。」「なかなか討論が終わらない。」
「この野菜はビタミンが豊富です。」「暑いので、日陰ですずんだ。」 Ours, before the rule:
「開会式では、会長が今年の目標について短い**演説**をした。」

All five rows are ONE authoring habit, so fix them in one rewrite:

1. **An institutional actor drags the other rows with it** — 「市は…決めた」 needs a
   modifier clause to be specific (hence the comma) and does not take です・ます;
   「私の娘は音に敏感で」 needs neither. Workplace *scenes* are fine (仕事/会社/会議
   lexis runs at official's own rate); what drifted is the institution as the
   sentence's **subject**. Same finding as `official_calibration.md` §13 for 問題8.
2. **です・ます costs no length** — 「この野菜はビタミンが豊富です。」 is 15 chars. It
   needs a person in the sentence, not another clause.
3. **問題4 is officially the long section** (one comma, a scene) — exempt from the
   問題1/2/5 band, not from its ceiling. Its own rule (§"A time/date/quantity key")
   says the stem must fix every axis that excludes a distractor; do that **in the
   fewest clauses that do so**. Trading the axis-fixing clause away to hit the
   band swaps a measured defect for an unmeasured one, which is worse.

Gate: `check_moji_stem_shape`, `check_moji_stem_register`, `check_moji4_stem_band`
(FAIL outside the archive's whole range, WARN outside the current era's; all
fourteen papers on disk are grandfathered by name — the sets are a queue).

## N options, N different words — in EVERY 大問

一つの大問の中で、同じ語を二つの項目の選択肢に出さない。**Measured: 0 repeats in
31 of 31 official sittings, in every 大問.** With 12–20 printed slots a repeat
tells the candidate the repeated word is not the key of at least one item it
appears in — elimination information from the paper, not from the language
(21を確信した受験者に23の消去情報を、言語ではなく紙のほうから与えてしまう).

Incidents: 「わずかに」 keyed at 問題5-21 and printed as a distractor at 問題5-23
(`20260819_1`, `qa-report-20260819_1-round3` R3-S4); four papers repeat a 問題3
affix — 「半」 twice over (`20260810_1`/`20260810_2`), 「総」, 「各」, 「性」 — which a
問題5-only rule and its 問題5-only check could not see (REPORT-GOI §F6).

**The repair is the DISTRACTOR, never the key**: the key is half of a drawn pool
entry, so moving it silently un-tests the drawn item. Replace with another word of
the same functional category (the shipped fix was 問題5-23 「わずかに」→「多少」).
Gate: `check_moji_option_reuse` over 問題1–6.

## The KEY must be N2 — and no gate checks that for vocabulary

The band gate reads `level_band_grammar.txt`, which covers 問題7–9 grammar only.
Check every 問題1–6 key against Shinkanzen N2-Goi/N2-Kanji and Soumatome N2
語彙/漢字 — a headline N3-or-below word absent from either N2 volume is too easy
(avoid 賢い/かしこい). No vendored word list exists anymore to query; this is a
judgment call, and a re-drawn key's band goes into the QA report by name with the
book and page that confirmed it.

---

# Part 1 — 問題1 (漢字読み)

Test N2-band words: 交渉, 慌てる, 妨げる, 潔い, 措置, 傾向, 効率, 険しい. Build
distractors from REAL confusions — reading traps (措置(そち) vs しょち/そうち),
homophone kanji sets (納める/収める/治める/修める, 敗れる/破れる), same-radical fakes
(険/検/剣/験).

## Underline the WHOLE word, okurigana included

The underline is the bold span: `**収まった**`, never `**収**まった` or a bolded
particle (`**生じる**`, never `**に**生じる`). Official July 2025 marks `**才能**`,
`**辛い**`, `**収まった**` — the inflectional tail sits inside the mark, and 問題2
does the same with kana spans (`**しめって**`). Corroborated archive-wide
(`official_calibration.md` §5).

**The defect is splitting a word, not the character count.** Forbidden:
`**爆**ぜる`, asking for a bare character's reading. Legitimate: a whole word that
happens to be one kanji — official draws them (腕, 柱, 針). A single-kanji *word*
is a normal target; a single-kanji *fragment* of a longer word is not.

**Okurigana exposure is a RELATION between the printed span and the option field,
not a property of the options.** Whatever kana tail the bold span prints, all four
options must carry it: `**生じる**` → every option ends 〜じる; `**常に**` →
すでに/ただちに/しだいに/つねに (`20260819_1`, compliant). `20260813_2` 問題1-5 printed
`**頻繁に**` against ひんはん/びんぱん/びんはん/ひんぱん — the item asks for the reading
of 頻繁に and **every available answer reads 頻繁**, so a candidate who reasons
correctly finds no correct option (REPORT-GOI §F9; 24 of our 25 okurigana targets
comply). Gate: `check_moji1_okurigana_exposure`, no exemptions.

## 1–2 of the 5 問題1 targets are 訓読み — a band, not a cap

A 訓読み target is one whose okurigana is printed, or a single-kanji 和語 word.

**Evidence base, stated exactly** (this is the one 文字・語彙 number no script can
re-derive): the archive's underline does not survive the text-layer extract, so
`goi_profile.py` reports `target=None` for every official 問題1 item. The band
rests on **five sittings, hand-classified 2026-08-19** (7/2023–12/2025: 2/2/1/2/2
of 5) plus the calibration table below (12 訓読み of 35 current-era items, 34 %).
Shin Kanzen's two typeset 語彙 模擬試験 are what would settle it.

**Both bounds, one reason.** Above 2, the 2×2 on-reading grid (清濁/長短) official
runs in 3–4 of 5 slots stops being exercised and 問題1 measures word recognition
instead (`20260819_1`: 4 of 5 訓読み, grid in ONE item, `qa-report-20260819_1` F3).
At 0, word recognition stops being tested at all (`20260817_3`: five on-reading
compounds, a shape the window never shows). Author to 2.

Enforced at draw time by `sample_kun_capped()` in `sample_items.py` (both bounds,
including on the `--reroll-one` path) and re-checked by
`check_mondai1_reading_type_mix()`; both read the same classifier,
`sample_items.is_kun_target()`. **Repair with `sample_items.py --reroll-one
kanji_reading:<index>` and a fresh RNG seed** — never a hand substitution
(§"Build the set BEFORE you accept the target"), and never by re-balancing the
option field, which cannot change what kind of reading the printed target has.

## 2-kanji on-reading compounds: the 2×2 Cartesian product matrix

For 2-kanji 音読み targets (矛盾, 縮小, 概要, 効率, 措置), official tests each kanji's
reading independently: kanji 1 reading A (correct) vs B (confused —
清濁/長短/同音/同類漢字), kanji 2 reading C vs D → four options `{AC, AD, BC, BD}`.

- **矛盾(むじゅん):** A=む,B=ぶ; C=じゅん,D=じゅう → {むじゅん,むじゅう,ぶじゅん,ぶじゅう}. *Defect:* `むじん` (an arbitrary 3rd ending breaks the 2×2).
- **概要(がいよう):** A=がい,B=かい; C=よう,D=ゆ → {がいよう,がいゆ,かいよう,かいゆ}.

## The two-branch rule — same kanji OR same semantic field (the ONLY statement)

Every distractor shares the target's word form/conjugation class (Item integrity
#13–14; a real word per the RESOLVE procedure below) AND is either:

- **(a) 同漢字** — a reading of the target's own kanji or of a same-radical/
  visual-component kanji (措置: そち/しょち/そうち), OR
- **(b) 同分野** — a real N2 word in the SAME semantic field (official 7/2025
  辛い→あまい/にがい/しぶい; 収まった→さだまった/しずまった/やすまった — often sharing no
  kanji with the target).

Both branches are legal; forbidden is a grab-bag satisfying neither (いたわる's
distractors must not be ことわる/さわる/かわる). When branch (a) is empty for a drawn
target, the fix is never inventing non-words. **Scope: branch (b) is the 訓読み
branch.** For a 音読み compound target (才能, 起床, 概要), official distractors are
清濁/長短 derivations of the key's own on-reading and are NOT words — step 6 of the
RESOLVE procedure below.

## A spelling with TWO 訓読み: key the LOWER-graded one; never print the other

Some headwords are graded twice — `潜る(くぐる)` at N1 beside `潜る(もぐる)` at N2
(~110 pool entries). (1) **Key the reading the corpus grades lower** — keying the
harder member asks "which reading did the examiner mean". (2) **The other reading
may not appear in the option set at all** — it is a second correct pronunciation
of the printed string, not a distractor. Measured: 0 of the 35 current-era items
does (decisive case 7/2025-2, 辛い carries both からい and つらい; official offered
あまい/にがい/しぶい).

Record both readings and levels on the source line —
`くぐる=潜る[N1] / もぐる=潜る[N2] → key もぐる` — after checking Shin Kanzen
N2-Goi/N2-Kanji and Soumatome. A pool entry naming the harder reading is a
**pool** defect (send it to `exam-blueprint`'s kanji_reading validity rule).
**No gate since 2026-08-11**, when `check_mondai1_key_band()` went with
`openjlpt`; Shin Kanzen 漢字 別冊1's 訓読みが二つ以上ある漢字 is the list it is about.

## Build the set BEFORE you accept the target — reject the target, never the rule

The three constraints (conjugation lock + real word + one of the two branches)
intersect to nothing for some pool entries — then the target is undrawable, not
negotiable. In order: (1) write the target's okurigana and locked word class;
(2) list same-kanji/look-alike readings → branch (a); (3) if fewer than three,
list same-field real N2 words → branch (b); (4) **if (a)+(b) still yield fewer
than three real words, STOP** — report undrawable and ask `exam-blueprint` to
re-draw. Do not invent a word or widen the field. Worked empty case: 「労わる」 — 労
reads only ロウ/いたわ(る)/ねぎら(う), no look-alike gives a ～わる verb (a={}), and
every real ～わる verb is an unrelated field (b={}).

**"Re-draw" means `sample_items.py --reroll <category>` — never hand-pick a
replacement, even a real N2 word.** `20260817_1` found `居酒屋(いざかや)` undrawable
and hand-swapped in `潔い(いさぎよい)`, shipping a repeat drawn 7 tests earlier and
deep inside `kanji_reading`'s cooldown: a hand substitution never touches the
ledger `--reroll` updates (`exam-blueprint` "Rotation model").

## All four readings must RESOLVE — check them against the books, don't judge them

**2026-08-11: this ran as a scripted `openjlpt` lookup; that corpus is deleted**,
and both books are scanned images with no text layer — so it is now author
diligence: read the page via the Read tool's `pages` support, or use trained
vocabulary knowledge cross-checked against these books (for a miss, the archive's
OCR'd `booklet.md`/`key.md`). The rules didn't change, only the mechanism.

Official treats the two target types differently (all 35 current-era items,
`official_calibration.md` §5):

| Target | n | What the distractors are |
|---|---|---|
| **訓読み** (okurigana printed, or single-kanji) | 12 | **real words, every option, no exception** — same class/conjugation as the key, usually same field; frequently not sharing the target's kanji. |
| **音読み compound** | 23 | predominantly non-words — 清濁 (さいのう→ざいのう), 長短 (きしょう→きしょ), ん⇄う (のうやく→のんやく) derivations of the key's own reading. ~5 of 23 mix in real homophones (握手→拍手); one set is four real compounds (分析→分解/分節/分割). |

Both blanket rules are wrong ("every option a dictionary word" fails 23/35;
"音読み distractors must be non-words" fails ~6). The invariant is directional:
**a 訓読み set may never contain a non-word; a 音読み set may, but only as a
derivation of the key's own reading.**

Procedure: (1) reduce each option to dictionary form (さだまった→さだまる); (2) check
all four against Shinkanzen/Soumatome pages, per option; (3) a HIT is evidence —
write the confirmed headword + branch label into the source line
(`さだまる=定まる[N1, Shinkanzen p.NNN]`), citing whichever source you checked; (4) a
MISS is a debt — confirm via 常用漢字表 音訓 or the archive, record
`やすまる=休まる[常用音訓]`; (5) if no spelling confirms anywhere, the reading is
invented — delete the option (がいり/そうじる/うんじる have no confirmable spelling);
(6) for 音読み targets, every option is EITHER a real word OR a derivation
(清濁/長短/ん⇄う of the target's own reading) — nothing else; (7) a 解説 etymology
must quote the headword actually confirmed in step 3.

`make check` has never WARNed on a non-listed reading — **the written
source-and-branch line IS the check, the author's, not the gate's.** A distractor
with no writable branch label must be replaced; inventing spellings (弄わる/招わる)
is a severe defect.

## The target's spelling must match its headword in Shinkanzen/Soumatome

問題1 tests a reading off a printed spelling — printing 「労わる」 where the textbook
headword is 「労る」 changes the item (the extra 「わ」 locks the option class). Fix
`pools.json`, then re-sample; re-spelling the stem alone leaves the pool to
re-draw the defect next test.

---

# Part 2 — 問題2 (表記)

## Composition first: ≥1 和語 target, ≤3 bare compounds — then build the grids

**Measured, 31 of 31 sittings: 1–3 of the 5 items are 和語 targets with printed
okurigana (median 2), and 1–3 are bare 2-kanji compounds (median 3, current era
2–3).** Our papers ran 0–2 和語 (six papers at 0) and 2–5 bare compounds (eleven at
4 or 5): 問題2 had become one puzzle repeated five times (REPORT-GOI §F3).

| per paper | official | cur | author to |
|---|---|---|---|
| 和語 items (any option carries okurigana/kana) | **1–3, every sitting** | 1–3 | **2** |
| items whose four options are all bare 2-kanji | 1–3 | 2–3 | **≤3** |

The branches test different things, which is why official runs both every
sitting: a grid item asks 「which of two lookalike kanji spells this on-reading」, a
和語 item 「which kanji writes this native word, given its okurigana」. Official
12/2025 ran three inflected 和語 of five (りゃくして/すずんだ/すくわれました) with options
2–6 characters long; our option lengths never left 2–4.

**The 2×2 grid is a device, not the format** — official completes it in 80 % of its
compound items (cur 89 %), ours in 100 % of 55, which is what five compound items a
paper forces. That pressure is also where the `orthography` repeats come from
(REPORT-GOI §F8): 249 entries cannot supply five clean grids a paper forever.
Enforced at draw time by `sample_wago_floor()` (`exam-blueprint`) and re-checked by
`check_moji2_composition`.

## The 2×2 component matrix, when the item IS a compound

Swap EACH kanji of a correct 2-kanji compound independently for a
lookalike/homophone → `{A,B}×{C,D}→{AC,AD,BC,BD}`. Pseudo-compounds and non-words
are standard and expected — they need not be dictionary headwords (official ships
`支接/施接/支設`, `液って/温って/汗って`).

- **げひん(下品):** A=下,B=不; C=品,D=晶 → {下品,下晶,不品,不晶}. *Defect:* mixing in `等`, omitting B+D.
- **うんが(運河):** A=運,B=雲; C=河,D=賀 — 運=ウン, 雲=ウン, 河=ガ, 賀=ガ, so all four parse as the printed うんが. **Do NOT use D=海:** {運海,雲海} read うんかい, so two options die on reading alone and the item collapses to 運 vs 雲 (`20260817_3` 問題2-9 shipped exactly that — and this file taught it as the model set until 2026-08-19). **A complete component grid is NOT the check; the kana skeleton is.**
- **げた(下駄):** {下,不}×{駄,太}. **かいこう(開港):** {開,回}×{港,向}. **のうこう(濃厚):** {濃,農}×{厚,高}.

**Single-kanji stems with okurigana** (けわしい→険しい): all four share the exact
okurigana and come from the same phonetic-radical/visual set
(`{険しい,験しい,検しい,剣しい}`). **Native compound items** (やぬし→家主): every
option is legitimate standard kanji (`{家主,宅主,宿主,店主}`) — banned: absurd
combinations (`守柱`).

**The stem's kana is the key's reading.** Write the stem kana from the key
option's reading, then verify every non-key option parses as the same kana
skeleton (かいこう → 開港/開向/回港/回向). A stem kana no option reads is an
automatic-fail class.

**Procedure — write the reading of each COMPONENT before you accept the grid.**
Two columns, one line per component: `A=運(ウン) B=雲(ウン)` / `C=河(ガ) D=賀(ガ)`.
Every column must be readings-identical; if any component's on-reading differs
from its partner's, the grid is dead however good the lookalike is. Then read the
four products back against the stem kana. Doing this on paper is the check — "the
grid is complete" is not, and neither is "the kanji look alike". (`make matrix`
validates only: both generators are hard-disabled until a real 音訓 table exists.)

## Every printed glyph must be 常用 — `references/joyo_kanji.txt` decides it

**Every constituent kanji glyph must be a legitimate, standard 常用/N2 kanji** —
banned: obscure/alien glyphs (`惰楪`'s `楪`). **The authority is
`references/joyo_kanji.txt`**, the 2136 characters of the 2010 常用漢字表, the way
`level_band_grammar.txt` is the authority for 問題7–9's band. Check the key and
all three distractors character by character before the item is written.
`check_moji2_option_glyphs()` reads the same file and FAILs any 問題2 option — and
any 問題1 **printed target** — carrying a glyph outside it.

The file settles a judgement the prose kept losing: `20260817_3` shipped 問題2-8
keyed 「飢饉」 through **three** QA rounds (「饉」 is not 常用; 「飢」 occurs zero times in
31 sittings), caught only by a fresh reviewer checking the inventory by hand.
`20260811_1` is exempt **by name** (`MOJI_GLYPH_GRANDFATHERED`, 問題2-9
「曳帰す」/「曳返す」) — read the set in `tools/check_consistency.py`, not this
sentence.

**A 表外 glyph is a POOL defect only in `orthography`**, the one item type with no
kana escape: such an entry is undrawable — delete it and
`sample_items.py --reroll orthography`, never hand-substitute a target.
**Everywhere else the repair is kana, not deletion** —
`check_pool_glyph_inventory()`'s ~14 WARNed entries (蕎麦, 凌ぐ, 繋がる, 卑怯 …) are
legitimate N2 **words** whose *kanji spelling* is off-band, and 問題4/5/6 print
them in kana as official does. A standing list, not a deletion list.

---

# Part 3 — 問題3 (語形成)

諸〜, 〜化, 準〜, 〜済み, 〜制, 未〜, 〜性, and the four real negation prefixes
非〜/無〜/未〜/不〜 — there is no fifth; 迷〜 is not real and is banned
(`references/banned_collocations.txt`). Distractors must be real N2 affixes of the
same functional family. Not required that all four attach plausibly to the stem
(official 教育→則/理/論/規, only 教育観 attaches) — but every affix must be a real,
standard morpheme, and the twelve printed affixes are **twelve different words**
(Part 0; 「半」 alone was printed in six of our fourteen papers).

---

# Part 4 — 問題4 (文脈規定)

N2 nouns/adverbs: 難航, 発足 (distractor: 成立), かろうじて, うんざり, てきぱき, 需要.
Distractors share the semantic field AND functional category (core sniff-test
rule). Stem band: Part 0's last row (median 30, no stem past 44).

**The stem is a BLANK, never the answer** — every stem carries （　）and never
prints the answer word elsewhere (a printed answer is an automatic-fail class).

**Never key a near-synonym of the answer** — a distractor the stem also accepts
(コンクール vs コンテスト in the same sentence) makes the item double-answerable. If
the stem accepts two options, change the target or stem — never defend the item.

## A time/date/quantity key: the stem must FIX every axis the distractors can vary

**Construction step, before the options are written.** When the key is a time,
date, or quantity word, list the axes a reader could silently choose differently —
the month, the year, the direction, the unit, whose calendar — and make the stem
state each one, in as few clauses as state them. Every wrong option must then be
excluded by the printed text ALONE, never by the reader's default reading.

`20260818_1` 問題4-14 shipped 「請求書は毎月（　）に発送しますので、五日ごろにはお手元に
届きます。」 keyed 初旬, excluding 月末/下旬 as 「五日に届く発送日にならない」 — which holds
only if the arrival is in the SAME month, so two distractors survive a reading the
stem never ruled out (`qa-report-20260818_1` F7). The repair is one clause in the
stem, not a new distractor set: 「…ので、**同じ月の**五日ごろには…」. The 解説 must then
say which axis the stem fixed, so the next reader can check the exclusion instead
of re-deriving it.

---

# Part 5 — 問題5 (言い換え類義)

The stem contains the HARD word (あいにく, 妥当, ありふれた, くたくた, 重宝); options
are simpler, never the reverse (Item integrity #12). Twenty options, twenty
different words (Part 0).

**Each option must be idiomatic ON ITS OWN, not merely survivable in the stem.**
The swap test only asks whether the sentence parses; read each option as a bare
phrase with the stem covered and ask whether a native writer would produce it
unprompted. **When the target IS the natural collocate of the frame, change the
frame instead of substituting into it** — `20260817_3` 問題5-21 keyed 器用だ and
shipped 「手先が上手だ」, because 手先が**器用** is unusable (it is the target), so
「手先が〜」 could only yield marked wordings. The fix was 「細かい作業が得意だ」.

**Key length.** The uniquely-longest option is the key in 19 % of official
length-varying items (問題5 22/116, 問題6 29/151; per paper 0–50 % all-era, 11–22 %
current era — six sittings run 0 %, so there is **no floor**: a paper keying no
long option is an ordinary official shape). `check_moji_longest_key_rate` caps the
paper at 30 %, which is the current era's envelope, not the archive's. In 問題5 a
breach is usually a PHRASE key against bare single-word distractors — give all
four the same grain.

**Katakana headwords are rare on purpose** — the archive draws one in 3/35
current-era 問題5 items (`official_calibration.md` §12); `sample_items.py` draws at
that measured rate instead of the pool's raw ~30 %. A paper with zero katakana
targets in 問題5/6 is the archive's usual shape, not a thin draw.

---

# Part 6 — 問題6 (用法)

1 correct sentence + 3 grammatical-but-wrong-usage sentences (妥協, 発揮, 解消,
募集, あふれる). Wrong sentences must be **tempting, not absurd**, and must not be a
second REAL collocation (「契約を解消」 is attested, so it is a second correct
answer, not a distractor). Per wrong sentence: (1) write it correct; (2) break
exactly ONE thing, and break it the way **a learner would plausibly get it
wrong**; (3) search the result — if attested, it is a second correct answer, back
to step 2.

| Sentence (解消) | Verdict |
|---|---|
| ✅『長年の誤解が解消した』 | correct option |
| ✓『渋滞を解消に導いた』 | right domain, wrong collocation — the hardest discrimination, so prefer it |
| ✓『部屋の電気を解消した』 | a domain shift, and legal — but the weak kind: 解消 is invited by the kanji 消 alone, so it reads absurd rather than tempting |
| ✗『契約を解消した』 | attested — banned (second correct answer) |

**Length, re-measured 2026-08-21.** Official option sentences: current era **mean
26.0, median 25, range 18–39 (n=136)**; all 31 sittings mean 26.3, median 26, range
**13–39** (n=608). *History:* the row read 「mean 25.0, median 25, range 9–35
(n=136)」 until 2026-08-21, with the advice 「a 9-char option is official, so short
alone isn't a defect」 — no parse reproduces the 9 (shortest of 608 is 13), so
**that advice is withdrawn**: under 18 chars is outside the current era entirely.
Give each sentence a who/when/what. Our papers run mean 26.6, median 27, range
14–40 — the same distribution, i.e. this was a doc defect, not a paper defect.

## "Never leave the word's own domain" was WRONG — refuted, not carried (R2-F9)

Until 2026-08-19 step (2) read "break exactly ONE thing INSIDE the word's own
domain — never leave the domain", with 「部屋の電気を解消した」 listed as *banned*.
**Official does the opposite**, and 12/2024 settles it — every one of these is a
printed wrong option (`refs/JLPT_N2_NEW/15. N2 12-2024/booklet.md` L96–120):
26 薄める 「コースのレベルを薄めた」「テレビの音量を薄めた」 (all three leave the domain) ·
27 充実 「空には雲が充実している」 · 29 ふもと 「駅のふもとで池田さんと会う」 · 30 定年
「犬の定年は…10歳から15歳」. As written the rule fails that sitting and our own
`20260818_1` 問題6-26/30, which two fresh-eyes rounds read as sound. **A rule that
fails the corpus it is calibrated against is the defect.** (Route history, so
nobody re-files it: round 1 filed it against `exam-qa-review` §2b, the restating
file, and was declined for process; round 2 re-filed it here and it is refuted
here.)

**What actually fails a wrong sentence:**

1. **A sentence no learner would produce** — absurd instead of tempting. That is
   what the old rule was reaching for and mis-stated: three 消す-domain sentences
   for 解消 is a bad set not because they leave the domain but because nobody
   reaches for 解消 to mean 消す three times in a row.
2. **A second ATTESTED collocation** (「契約を解消」) — two correct answers.
3. **A form tell** — an option not sharing the printed word form the other three
   use (below).

A domain shift is official's main device. Use it where the shift is one a learner
actually makes (素質 for a machine's 性能, 占める for an absolute quantity), and
reach for a same-domain wrong collocation when both are available, because it is
the harder item.

## A word's OTHER attested sense is still that word — check it too

Step 3's search covers EVERY sense the word carries, not just the KEY sentence's.
`20260811_1` shipped 落ち着く keyed on "person calms down" with a wrong option
reading 「試験の点数が落ち着いてきた」 — but 落ち着く also has an attested "fluctuating
VALUE settles" sense (相場が落ち着く), and a test score is a fluctuating value, so
that "wrong" sentence is a live second answer. Name EACH sense before writing
distractors (the list is Shin Kanzen 語彙's 意味がたくさんある言葉, three 課, and
Soumatome 第7週).

## All four options share the SAME word-form of the headword

If the headword is a suru-verb (宣伝する), every option bolds a conjugated verb form
— never a bare-noun option against three verb-form ones (`20260811_1` 問題6-26).
The same binds bare-noun headwords: if the headword is a plain noun (民間), every
option uses that identical printed word or a bare inflection — never let one option
alone derive a 〜的/〜化/〜性 form while the others stay bare (`20260817_2` 問題6-28
shipped 民間**的な**選挙 against three bare-民間 options). Official ships exactly one
option in a different form at 13 % of items, the same rate as ours, so the rule is
about the TELL, not about uniformity.
