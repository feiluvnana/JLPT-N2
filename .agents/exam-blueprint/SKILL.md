---
name: exam-blueprint
description: Single owner of WHAT each exam tests — RANDOM, non-repeating pool sampling of grammar points, vocabulary, kanji, listening scenarios, and reading topics, and answer-position balance. Use BEFORE authoring any questions, whenever generating a new test, whenever the user asks for "another test", "random questions", "different questions", or says tests repeat, feel stale, or feel textbook-bound. Never let the language model choose items from memory — model choices are heavily biased toward the same famous items and are NOT random; selection must come from scripts/sample_items.py.
---

# Exam Blueprint — pool sampling

## Why this skill exists, and the invariant it owns

A model asked to "pick 12 N2 grammar points" picks nearly the same 12 every
time, reuses scenarios, and biases keys toward positions 2-3 — determinism
wearing a randomness costume. Hence four mechanisms: **explicit pools**
(`references/pools.json`), **seeded RNG sampling** (`scripts/sample_items.py`
— code, not vibes), an **LRU coverage ledger** (`logs/ledger.json`), and
**answer-position balancing**.

**Tested linguistic items are always the pool's, topics are always yours to
write.** Grammar, vocabulary, kanji, idioms/keigo ALWAYS come from
`pools.json`, calibrated against Shin Kanzen Master; the assigned
`reading_topics`/`listening_scenarios` entry sets scene and content, and the
author writes the passage/dialogue from it directly at N2 level (Part II) —
no external source, no harvest, no blend ratio. Workflow placement:
`jlpt-test-generation` (pass table).

---

# Part I — The pool and the draw

## Pool entries stay inside the N2 band

Do not add N1-only forms or N3–N5 drills to `references/pools.json` — banned
lists live in `question-authoring/references/level_band_grammar.txt`.
`make check` fails papers whose 問題7–9 keys hit that list, **and checks the
pool itself** — a banned form sitting uncommitted in a pool is a defect the
moment it's committed, not only when drawn.

**A `kanji_reading` entry must come with a writable distractor set, or it is
not a pool entry.** The 問題1 two-branch distractor rule is `question-
authoring`'s; some entries have an empty intersection, and an author who's
already drawn the target invents non-words instead of rejecting it. Write the
three distractors before adding or keeping an entry; if you can't, it's out.

**A pool spelling must match its headword in Shin Kanzen Master N2-Goi/
N2-Kanji or 日本語総まとめ N2 語彙/漢字.** 問題1 tests a reading off a printed
spelling, so okurigana is part of the item (`労わる` vs the dictionary's
`労る`). Fix the pool, never just the paper.

**An `orthography` entry containing a 表外漢字 is a pool defect — delete it and
re-draw (`sample_items.py --reroll orthography`), never patch the sentence.**
問題2 prints all four options, so every glyph in the grid must be standard
常用/N2 kanji (`question-authoring/references/moji-goi.md` §問題2 owns the
option-set rule); an entry whose own headword is outside 常用 cannot produce
one. `飢饉` shipped from this pool and survived three QA rounds: 饉 is not a
常用漢字, and 飢 occurs **zero times** across all 31 official sittings in
`refs/JLPT_N2_NEW/`. Same shape as 問題1's 表外音訓 rule below — the defect is
the entry, and re-spelling the stem leaves the pool to re-draw it next test.

**A `quick_response` entry is a SENTENCE, so a defective one is corrected in
place — it is not the same repair as an undrawable entry.** The 飢饉 rule above
says *delete and `--reroll`*, and the reason is specific: an `orthography` entry
whose own headword needs a 表外 glyph is **undrawable** — no compliant item
exists, so there is nothing to fix on the entry. A `quick_response` entry that
is merely ungrammatical is a different case: the tested errand and register are
sound and the sentence itself is the defect, so the repair is to **fix the entry
and print the corrected entry in the paper**, leaving pool, spec, ledger and
script all naming the same string. `20260818_1` drew
「薬の説明は、調剤師から伺ってください。」 — 謙譲語 aimed at the listener (F5) — and it
was corrected in `pools.json`, with that paper's `test_spec.json` and
`logs/ledger.json` rows following the corrected entry so
`check_draw_provenance()` still resolves.

**Correct the WHOLE sentence, not the reported defect (R2-F5).** That first
repair changed 伺ってください→お聞きください and left the sentence's subject noun
alone — 「調剤師」, which is not a Japanese professional title (the licensed one is
**薬剤師**; 調剤 is the act) and occurs nowhere in the 31-sitting archive. So one
pool sentence produced two defects in two QA rounds, the second one printed and
SPOKEN. The entry now reads 「薬の説明は、薬剤師からお聞きください。」. When you touch a
pool sentence, re-read every noun in it against the world, and note the
paper-side cost: the fix re-synthesises the MP3 and re-labels the invented scene
(`20260818_1`'s section table said 動物病院の会計, which has no dispensing window).
`check_pool_nonexistent_titles()` now FAILs a pool string naming a title that
does not exist (調剤師, 看護士, 診療師 …) — a deny-list, so it catches the near
misses that have shipped, not every possible invention. That is NOT "patch the sentence instead
of the pool", which is what the rule forbids: the pool IS the thing that changed,
and no paper prints a string the pool does not carry. The precedent is the
`内〜(国内)` → `〜内(国内)` correction (R3-2), where the machinery was adjusted so
the corrected string did not orphan a recorded draw — same principle, and the
reason a pool fix must never be allowed to "punish the fix".

`check_pool_keigo_direction()` FAILs any `quick_response` entry putting a 謙譲語
verb on a 〜てください aimed at the listener (`question-authoring` Item integrity
#20 covers the keyed REPLY; nothing had ever read the drawn STIMULUS).

### The `kanji_reading` validity rule (audited 2026-08-06)

Unanswerable 問題1 items (`領(えり)`, `線(すじ)`, `爆(は.ぜる)`) ship when
nothing checks the printed kanji actually *has* the keyed reading. Every
entry must satisfy all four:

1. **Shape.** `語(よみ)`: `語` contains a kanji; `よみ` is hiragana, no `.`
   and no katakana (a dot is a raw KANJIDIC kunyomi with okurigana detached;
   katakana is a bound-morpheme on-reading dump — neither is a printable word).
2. **Attested.** `(語, よみ)` appears as a headword+reading in Shin Kanzen
   N2-Goi/N2-Kanji or Soumatome N2 — decisive for single-kanji entries, which
   have no fallback.
3. **One 語, two 訓読み → keep the LOWER-graded reading.** Rank by whether
   the reading is the one carried in the N2 volume, or by which reading the
   official archive keys.
4. **In band, if the reference misses it.** A multi-character word absent
   from Shinkanzen/Soumatome stays only when its reading is the ordinary
   dictionary reading on 常用音訓 AND the word is corroborated by the
   official archive — zero hits in both sources is the removal signal.
5. **Drawable.** Three distractors writable.

**Verify against Shin Kanzen Master and Soumatome — never a bare kanji
dictionary** (a KANJIDIC-style list carries 表外 readings, the source of the
previously-shipped `領: えり` defect, and can refute but never confirm an
entry). Both PDFs are scanned images with no text layer — read the relevant
pages or corroborate against the official archive's OCR'd `booklet.md`/`key.md`.

The 2026-08-06 audit removed 103 of 218 entries; 112 remain, 22× headroom
over `DRAW` of 5. `kanji_reading` is the only category whose parenthetical is
a reading (`納める(税金)` is context, `詫びる(謝る)` a synonym).

**Growth history, briefly** (2026-08-11): grown to 200 sourcing candidates
from `vocab-n1/n2/n3.json` (never the banned `kanji-n2.json`/KANJIDIC path),
which enforces Shape/Attested/rule-3 by construction. `openjlpt` (the
vendored classify/expand corpus) was fully removed the same day — its four
consuming scripts are deleted, `promote_adjunct.py` remains archived. Any
further `kanji_reading` growth is now manual: read Shinkanzen/Soumatome (or
corroborate against the archive) and hand-verify all four rules — no script
sources or pre-checks candidates anymore. Two `make check` gates that
depended on `openjlpt` (`check_mondai1_key_band()`, `check_moji2_stem_kana()`)
were deleted alongside it; both rules are now manual-review only
(`exam-qa-review`, `question-authoring`) — a green gate no longer proves
either held.

## One grammar point, one pool entry (no spelling variants)

The sampler's cross-category `taken` guard compares **raw strings** — two
spellings of one point are two items to the code (`grammar_p7` once carried
both `〜気味` and `〜ぎみだ`, keying one point twice in one 問題7).

- **One spelling per point** — not kanji *and* kana, not with *and* without
  an optional tail, not two conjugations of one verb.
- **Cross-category overlap must be spelled identically** — `taken` keeps an
  item to one 問題 per test, but only byte-identical entries count.
- **A parenthetical is a disambiguating gloss, never a variant** — `〜次第だ`
  (depends on) in `grammar_p7`, bare `〜次第` (as soon as) in `grammar_p8`.

`make check` fails a grammar entry hitting `TOO_HARD`/`TOO_EASY` without an
`ALLOW`, and two same-category entries whose skeletons match after stripping
`〜`/parentheticals — **the skeleton rule is a floor**, it misses pairs like
`〜がち`/`〜がちだ`; read new entries against the rules above by hand too.

Known residue (audited 2026-08-06, left deliberately): five `grammar_p7`×
`grammar_p8` pairs where p8's pattern contains p7's bare form — don't add
more; `--reroll grammar_p8` if a drawn 問題8 pattern repeats a 問題7 point.

**`grammar_p7` and `grammar_p8` are ONE rotation space** (F1, 2026-08-20).
**15** forms are listed in both pools (`つつある/てたまらない/として/としても/
ないことには/につれて/に基づいて/に沿って/に限らず/のみならず/ばかりか/ばかりに/
わりに/をきっかけに/をはじめ`) and the per-category cooldown window could not
see across them: `head()` splits a p8 entry on its first paren, so
`限定表現(〜のみならず…も)`'s identity was the LABEL 「限定表現」, not the form.
`20260819_1` drew that entry and `変化推移(〜につれて…ていく)` into 問題8 after
`20260818_1` — the paper immediately before it — had KEYED both forms in its
問題7, with every gate green; **9 of the 14 papers on disk leak this way.**
`grammar_form_tokens()` now folds the FORM into `identity_tokens()` (cross-
paper cooldown) and `taken_tokens()` (one point, one 問題 per paper), and
`check_grammar_cross_category_rotation()` is the backstop. Repair a hit with
`--reroll-one grammar_p8:<index>` and a fresh RNG seed, then re-author that
item — never a hand substitution.

**2026-08-11: `grammar_p7`/`grammar_p8` audited against Shin Kanzen's full
TOC (~211 forms)** — roughly half the book's forms were missing, including
two whole lessons with zero coverage. Added 60 N2-band forms to `grammar_p7`
(172 total; `grammar_p8` unchanged at 42), each checked against the band-ban
list and the skeleton-dup check.

## A `paraphrase` parenthetical is a NON-BINDING gloss — and a bad one is a POOL defect

`納める(税金)` is context, `詫びる(謝る)` a synonym, `半ば(なかば)` a reading:
the parenthetical means something different per category and nothing had ever
said what a `paraphrase` one obliges. It names **the intended simpler synonym**,
and it is a gloss, not the key — an author may key a different word, and when
one does, **the reason goes into the stage handoff** so the deviation is
reportable instead of silent. `check_spec_target_items()` reads 問題1/2/4 only;
no gate reads a `paraphrase` parenthetical, and none can.

**A gloss that is not idiomatic in the drawn word's own frame is a defect in
`pools.json`, to be fixed there — never worked around item by item.** The entry
read `うっすら(かすかに)`; 「かすかに」 modifies faint *perception* (音・光・におい),
not quantity, so 「庭の草にかすかに雪が積もっていた」 is not idiomatic while
「わずかに雪が積もっていた」 is. `20260819_1`'s author keyed 「わずかに」 and
recorded the deviation — the right call — but the pool would have handed the
same bad gloss to the next paper that drew うっすら (F5,
qa-report-20260819_1). It now reads `うっすら(わずかに)`; 「かすかに」 remains a
valid standalone `paraphrase` entry. Follow the `調剤師` precedent when you
touch one: correct the entry, and carry the corrected string into every
`test_spec.json`/`logs/ledger.json` row that recorded it, so
`check_draw_provenance()` still resolves.

## Composition is drawn, not authored — three shapes `draw()` enforces

**Most 文字・語彙 quotas are properties of the DRAW, not writing choices.** The
和語 share of 問題2, the 訓読み count of 問題1 and the katakana rate of 問題5/6 are
all decided before an author writes a word, so each is enforced inside `draw()`
and re-checked by the gate — never left to the pool's own composition, which is
the thing being corrected for. **Never re-derive a target from
`len(subset)/len(pool)`; re-measure the archive** (`official_calibration.md`
§12/§14, `tools/goi_profile.py --baseline`).

| category | helper | rule | archive |
|---|---|---|---|
| `paraphrase`, `usage` | `sample_katakana_capped()` | `n` Bernoulli(`KATAKANA_TARGET_RATE`) trials pick the katakana slots, capped at `KATAKANA_CAP` | katakana headword in 3/35 問題5 and 1/35 問題6 items |
| `kanji_reading` | `sample_kun_capped()` | 訓読み count inside `KUN_FLOOR`–`KUN_CAP` = **1–2 of 5**, both bounds, `--reroll-one` included | five hand-classified sittings run 2/2/1/2/2 |
| `orthography` | `sample_wago_floor()` | 和語 count drawn from the archive's own histogram `WAGO_DIST` (floor `WAGO_FLOOR`), bare 2-kanji compounds ≤ `COMPOUND_CAP` = 3 | 和語 1–3 and compounds 1–3 in **31 of 31** sittings |

Two things the 2026-08-21 additions record, because both were shipped defects:

- **A one-sided rule produces the opposite monoculture.** `KUN_CAP` alone let a
  paper draw ZERO 訓読み (`20260817_3`) with the gate printing `ok`, so the cap
  became a band. Every per-paper composition rule here is now two-ended
  (REPORT-GOI §F5/§D2).
- **A fixed quota reproduces a shape the archive varies.** `sample_wago_floor()`
  samples the 和語 count from the archive's histogram (1:1, 2:23, 3:7 sittings)
  rather than always drawing the median 2 — the same reasoning that made the
  katakana cap Bernoulli rather than a fixed one-per-paper.

`is_kun_target()`, `is_wago_orthography()` and `is_bare_compound()` are the
classifiers, and `tools/check_consistency.py` imports them, so the sampler and
the gate can never disagree about what a branch is.

**Growth history, briefly:** both pools were grown and re-curated across
several 2026-08-11 passes — legacy 2級-era katakana dumps and off-domain
concrete nouns were removed, replacements mined from Shinkanzen/Soumatome
after `openjlpt`'s removal, with a reconciliation pass catching near-duplicate
harvests across concurrent editing sessions (normalizing trailing な/だ/に/
する/の before comparing). Current state: `paraphrase` 143 entries, `usage`
217, katakana share dropped from ~30% to single digits — real dilution, but
the sampler cap above remains the actual enforcement mechanism, not pool
composition. Cross-pool suffix-variant overlap (a bare `context_words`
headword vs a conjugated `paraphrase`/`usage` entry of the same word) is left
in deliberately — only byte-identical entries are guaranteed kept apart.

## Topic themes — the closed vocabulary (this skill owns it)

`reading_topics`/`listening_scenarios` entries are **objects, not bare
strings** — `{"topic": "在宅勤務と切り替え", "theme": "働き方"}` — and `theme`
comes from a **CLOSED** list of twenty values, defined once in
`scripts/level_data.py` as `THEMES`:

| | | | |
|---|---|---|---|
| 睡眠・健康 | 医療・福祉 | 食 | 環境 |
| 防災 | 交通 | 住まい | 働き方 |
| 教育 | 子育て・家族 | 地域活性化 | デジタル化 |
| 消費・経済 | 文化・伝統 | スポーツ・余暇 | 人間関係 |
| 行政・手続き | メディア・情報 | 旅行・観光 | 科学・技術 |

**Never widen the list to make an entry fit** — a stretched label looks like
agreement and is worse than a wrong one; pick the nearest value or say the
entry doesn't belong. The tags exist because string checks compare *wording*:
two differently-worded sleep-related entries both read `睡眠・健康` under the
tags, a lookup instead of a judgement.

**What the sampler enforces.** `check_pool_themes()` FAILs a themed entry
that's a bare string, lacks a `theme`, or carries an off-list value. After
the draw, `check_theme_spread()` WARNs when one theme exceeds `THEME_CAP`
(reading 1, listening 5) — a re-draw/re-blend decision. Reading must come out
all-distinct, so the draw meets it directly (`sample_distinct_theme()`); the
WARN is only a backstop for a hand-edited spec. Listening keeps the WARN-vs-
defect asymmetry deliberately — the sampler can't see which scenario maps to
which 問題.

### `key` — the errand identity, and the rule for near-duplicate entries

A themed entry is `{"topic"|"scenario": …, "theme": …}` plus an **optional
`"key"`**: the entry's errand identity, written `institution:errand`
(`引っ越し業者:見積もり`, `カルチャースクール:受講申し込み`). Two entries whose
display strings differ but whose errand is the same carry the **same** `key`,
and `sample_items.py` resolves rotation through `errand_key()` before it
compares display strings, so one errand cools down once however many ways the
pool spells it. An entry with no `key` is its own key — most of the pool is
genuinely distinct and needs none. Currently 41 themed entries carry one in 19
clusters, plus 9 `quick_response` phrases in 4 (§"`quick_response` has keys
too") — 23 clusters in all, which is the number `check_pool_errand_keys()`
prints; re-read it there rather than trusting this sentence.

**The incident (2026-08-19, R14):** the cooldown compared display strings, so
`引越し:見積もり` / `引っ越し業者との見積もり調整` / `引っ越し業者との調整` were
three separate items to it and two of them went out in consecutive papers with
every gate green (`qa-report-20260817_3` F6). Re-measured across the whole
ledger once the keys landed: **nine of the twelve papers on disk** had drawn an
errand a recent predecessor drew, every one of them invisible to the string
comparison.

**The authoring rule — key it, never re-spell it.** A new `listening_scenarios`
/`reading_topics` entry naming an errand an existing entry already names must
carry **that entry's `key`, verbatim**, not a new string and not a new
paraphrase of the errand. Adding the near-duplicate unkeyed re-opens the hole
by construction: the pool grows, the cooldown does not.

**`quick_response` has keys too, in a separate map (F4, 2026-08-19.)** Its
entries are bare strings, so a `key` cannot sit on the entry: making them
objects would orphan every recorded draw, which `check_draw_provenance()`
resolves by string. The keys live in a top-level
`"quick_response_keys": {"<phrase>": "<institution:errand>"}` map instead, and
`build_key_index()` folds it into the same index, so `errand_key()`,
`recency_map()` and `draw()`'s in-test `taken` set all see it with no signature
change. Clustering covered `listening_scenarios`/`reading_topics` ONLY until
this landed, and `quick_response` had been drawn 11-at-a-time in all 13 papers
with no errand identity at all: `20260818_1` drew both
「…こちらにお名前とご連絡先をご記入いただけますでしょうか」 and
「キャンセル待ちの方は、こちらに名前をお書きください」 — 問題4-2番 and 4-9番, two
items running one errand, which `exam-qa-review` counts as an AUTOMATIC fail.
Four clusters exist today (`窓口:記名依頼`, `店:在庫照会`, `窓口:担当者不在`,
`職場:進捗確認`); add a key whenever you add a phrase whose errand the pool
already carries. `check_spec_quick_response_errand_pair()` FAILs a paper drawing
two phrases from one cluster.

**`quick_response` is also inside the CROSS-paper cooldown now (F1,
2026-08-19).** The pair check above is in-paper only, and
`check_spec_errand_rotation()` — the cross-paper half — looped
`listening_scenarios`/`reading_topics` and nothing else, so for 13 papers a
16-draw `quick_response` cooldown was enforced by no gate at all: `20260818_1`
drew 窓口:記名依頼 one paper after `20260817_3` did, plus 職場:進捗確認 and
店:在庫照会 inside their windows, with every line green. The check now loops all
three keyed categories (`ERRAND_ROTATION_CATEGORIES` in
`tools/check_consistency.py`), prints how many keyed draws it compared, and
`skip`s a paper whose draws carry no key — `20260818_1` had **zero** keyed
themed draws, so its old green line had compared nothing (F5). Repair a
`quick_response` hit with `--reroll-one quick_response:<index>`, which costs one
問題4 item instead of eleven.

**And never delete a duplicate to solve it.** Four shipped tests name those
strings in `logs/ledger.json`, and `check_draw_provenance()` requires every
recorded draw to resolve to a pool entry — deleting a duplicate FAILs the gate
on papers that are already out. Add the `key`; a shared `key` is correct data,
never a defect.

**What the gate does with it.** `check_pool_errand_keys()` FAILs a blank or
non-string `key` (drop the field rather than leave it empty — a blank key is an
identity shared with every other blank one) and WARNs the **effective depth**
the clusters cost, currently 23 clusters over 27 entries, so `cooldown_for()`'s
headroom is optimistic by that many. Resolve that by **growing** the pool, never
by unsharing a key. `check_spec_errand_rotation()` FAILs a draw whose errand a
paper inside its own cooldown window already drew, across all three keyed
categories; the papers that already breached it are exempted by name and print
the same measurement as a WARN — **read the set in
`tools/check_consistency.py`** (`ERRAND_ROTATION_GRANDFATHERED`) for who and how
many, and note that each id carries the date of the key that put it in breach,
which is a different date for `quick_response` than for the two themed
categories.
Repair a hit with `sample_items.py --reroll <category>`, never a hand
substitution (§"Rotation model").

### The four theme rules

A paper authors 12 reading + 21 listening = 33 themed surfaces against a
20-value vocabulary, so "one surface per theme" is impossible — uniqueness
binds only the **headline set** = 問題9 cloze, 問題12 A/B (one surface),
問題13 長文, 問題14 flyer, 聴解問題5. Five surfaces:

1. **Five headline surfaces, five DIFFERENT themes.**
2. **A headline theme appears nowhere else in the 読解 half.** Listening is
   governed by rule 3 only.
3. **Reading: ONE surface per theme — all thirteen 読解 surfaces differ.**
   Listening caps at ≤5 scenarios per theme. 13 surfaces against 19 themes
   that carry reading entries leaves 6 spare — "no repeat" is arithmetically
   reachable, so a repeat is always a re-angle or re-draw, never a pool limit.
4. **Cross-test: no theme headlines two consecutive papers, and across the
   previous two papers together at most ONE headline theme may repeat**
   (only against the paper-before-last, only once).

**Rule 5 — VOICE is the third axis, and it is a per-paper quota.** Subject
(rules 1–4) and closing move (`dokkai.md`) govern *what* a surface is about and
*how it ends*; neither says what register it is written in, and the corpus
answered that question with one register in fourteen papers: **です・ます in 0%
of essay surfaces against official's 30–45%, first-person in 37% against 60–100%,
kanji density 35.5–41.7% against 25.5–30.1% — a band with no overlap at all**
(REPORT-DOKKAI.md §F3). Official 読解 passages are excerpts from published
essays; ours read as policy prose, and that single fact is most of the
"読解 feels harder than the real thing" complaint.

So each of the thirteen surfaces records a **voice** alongside its subject and
closing move — `一人称随筆` / `評論` / `解説` / `通知` — and the paper's tally must
reach, over the 12 essay-type surfaces (問題14 excluded):

| quota | official | gate |
|---|---|---|
| ≥4 surfaces in the **first person** (私/僕/自分) | 60–100%, median 78% | WARN |
| ≥3 surfaces in **です・ます throughout** | 30.5–45.2% of endings, median 35% | WARN |
| kanji density per paper **24–32%** | 25.5–30.1%, median 28.4% | FAIL outside 22–34% |
| ≥1 surface carrying quoted speech 「…」; ≥1 carrying a 疑問提示文 | 21–51 / 10k, 1–7 / 10k | QA reads it |

Record it in `logs/topics.json` beside the subjects, as a **`voices` map keyed
by the same surface keys** — `{"問題10(1)": "一人称随筆", "問題11(2)": "評論", …}`.
That extends the record instead of adding a file (the same argument the rotation
history makes), and `surfaces` keeps its existing shape so every reader of it
still works. `make check` WARNs on a paper whose entry has no `voices` map; all
fourteen papers on disk are in that state, and each leaves it when its surfaces
are re-authored under this rule. A paper that reaches the length ceiling only by reverting
to plain style **fails this rule rather than passing the length one**: です・ます
prose runs longer for the same content, so author both together
(`dokkai.md` §"Length bands", §"Axis 3").

**Rule 4b — the cloze's SUBJECT, not its theme, is bound against the whole
previous paper.** 問題9 is the one scored surface with no pool entry, no draw
and no cooldown, so rules 1–4 reach it only through its headline THEME tag —
and a theme tag is too coarse to stop the actual repeat. `20260817_3`'s cloze
(申請書を書かせない窓口) carried a headline theme that cleared rule 4 while
repeating the SUBJECT of `20260817_2`'s 問題10(4) (窓口ごとに住所氏名を書き直す
負担) — a non-headline surface, one paper back.

Procedure, at blueprint time: (1) write the cloze's subject as a concrete
noun phrase, 5–15 JP chars (`書かない窓口`, `内容量を減らす値上げ`), not a theme
label; (2) list the previous paper's **thirteen** 読解 subjects from its
`logs/topics.json` `surfaces` field, headline and non-headline alike; (3) no
match — same institution plus same issue is a match even under different theme
tags. A hit means re-subject the cloze before authoring, not re-label it.

Bind the SUBJECT, never the theme: two consecutive papers each spend 13
distinct themes out of a 20-value vocabulary, so theme overlap between them is
forced by arithmetic and "no 読解 theme may match the previous paper's" is
unsatisfiable — proposed after round 1 of `20260817_3` QA and rejected on
those grounds, 2026-08-19.

**The subject check is for EVERY headline surface, not just the cloze (R2,
2026-08-19).** Written for 問題9 alone, it left 問題12/13/14 and 聴解問題5 landing
on a one- or two-paper-old SUBJECT with every theme rule green: `20260818_1`'s
問題12 headlined 通勤の一時間の使い方 (交通) one paper after `20260817_3` spent
自転車通勤の危険度 (交通) on a NON-headline 問題10 surface, and its 聴解問題5-1番
ran 空き店舗の活用 two papers after `20260817_2`'s 問題10(5) did
(`qa-report-20260818_1-round3` F3/F4). Rule 4 could not see either, because it
compares headline against headline. So: **every headline surface (問題9, 問題12,
問題13, 問題14, 聴解問題5-1番, 聴解問題5-2番) gets a 5–15 JP-char SUBJECT written
at blueprint time, and each is diffed against the previous paper's THIRTEEN 読解
subjects AND its 21 聴解 subjects in `logs/topics.json` `surfaces` — headline or
not.** Same setting + a different issue is allowed and must be written into
`notes` as such; same setting + same issue is a redraw (or, for the cloze,
re-subject it — rule 4c). Subject identity is judgment, so this stays a blueprint
procedure and no gate measures it.

**Rule 4c — the cloze is the designated release valve for a rule-4 collision.**
When the headline set breaches rule 4, 問題9 is the ONE headline surface with no
pool entry, no draw and no cooldown, so re-subjecting it is the only repair that
needs no reroll and touches no other surface. Reach for it FIRST, and never
resolve a rule-4 breach by re-tagging: a theme the reviewer's own independent
re-tag agrees with is not negotiable, and a relabel that dodges the rule hides
the collision instead of clearing it (`exam-qa-review` Ground rules; the
`20260813_1` 問題13 precedent). `20260818_1` shipped with TWO headline themes
repeating the paper two back where rule 4 allows one (科学・技術 at 問題9, 教育 at
聴解問題5-2番), recorded the judgment in `logs/topics.json` and left it — the
honest fix was available the whole time and was taken in the round-1 fix pass:
the cloze moved 科学・技術 (部屋の響き) → デジタル化 (文字として残すか画像として残すか).
A re-subjected cloze must still satisfy everything its original brief did — its
assigned closing-move shape, the final-sentence template cap, the 問題9 category
tags and option-length limits, and 「the cloze's SUBJECT against the whole
previous paper」 (rule 4b) — and note that a candidate theme is only free if it
headlines NEITHER of the previous two papers (防災 looked free for `20260818_1`
and was not: it headlined `20260817_3`'s 聴解問題5-2番).

**These rules bind pool-origin and web-origin surfaces alike** — an offline
all-pool paper is not exempt. The pools are lopsided (`働き方` holds 44 of
240 listening scenarios, `科学・技術` only 2 — hence the listening cap of 5):
when a cap keeps breaching, grow the thin themes or move a surface's
subject; never stretch a label or raise `THEME_CAP`.

**Previous papers' headline themes** come from the two most recent
**generated** papers on disk (`imported-*` excluded). None on disk → rule 4
is vacuous, **say so in your report**. Pre-tagging papers: tag their five
headline subjects by hand from their `logs/topics.json` rows.

**How to comply:** after the blend report, write down every surface's theme
(a web/cloze entry inherits the theme of the surface it displaced or the
nearest tag); check the five headline themes against each other, then the
読解 list, then per-theme totals; apply rule 4 and record prior themes/repeat
count in your report. A theme tag is a floor, same as token overlap — it
catches the renamed subject, not a shape repeat; the whole-paper topic table
pass stays mandatory regardless.

**The four rules bind the SHIPPED surfaces — only `logs/topics.json` records
those.** The spec-side `check_theme_spread()` WARN can't enforce them: it
counts the draw, not which entry became which 問題, and it counts nothing at
all for `cloze_topic`/`"origin": "web"` entries (the hole `20260810_1` fell
through — its shipped paper held five `働き方` reading surfaces against a cap
of 2, all invisible to every check). So:

- **Every web seed and the cloze inherit a theme, written down** — into the
  spec entry when blending, into `logs/topics.json` when building. No theme
  is not "untagged", it's uncounted, which reads as compliant.
- **A tag must describe the passage as authored, not the topic as drawn** —
  re-tag at build time if drafting moved the subject.
- **Voice & Register quota across 読解 surfaces**:
  - ≥4 of the 12 essay surfaces written in first-person (`私`, `僕`, `自分`).
  - ≥3 passages carry `です・ます` polite style throughout.
  - Kanji density across reading prose 24–32%.
- `check_topics_themes()` reads recorded themes and FAILs the four rules on
  the 読解 half. Rows predating the field WARN.

## Rotation model (ledger v2 — LRU, not reset)

`logs/ledger.json` is `{"version": 2, "history": [ {test_id, seed,
generated_at, items{...}}, … ]}` — one entry per draw, newest last. A v1
flat ledger migrates automatically.

- **Cooldown, not exhaustion — and PER-CATEGORY, not a flat constant.** An
  item used within the last `cooldown_for(cat, pool_size)` draws is
  ineligible. A flat `COOLDOWN=2` once applied the same window regardless of
  pool depth, and two items proved it by repeating within 4-5 tests.
  `cooldown_for()` scales the window to each pool's OWN depth
  (`pool_size // draws_per_test`, minus a margin); a pool that can't fill a
  draw at its own ceiling relaxes one step at a time, says so, and **the
  level it settled on is written into the spec**.
- **Weighted by recency too, not just filtered** — `weighted_sample_no_replacement()`
  favors items that have gone longest since use (weight `ago(x)+1`), so a
  just-cooled item doesn't cluster right at the cooldown boundary.
- **One item, one 問題 per test** — categories draw against a shared `taken`
  set; a post-draw assertion aborts on collision.
- **Cooldown is by WORD, across categories** — recency tracks both raw
  string and `head()` identity, **plus a themed entry's `key`** when it has
  one, so near-duplicate errands cool down as one item (§"`key` — the errand
  identity", which owns the field and the rule for adding entries).
- **A reroll only re-verifies the category it touched** — every OTHER
  category in the spec was drawn at some earlier point against a different
  "now" window, so re-verifying them against the current window is wrong the
  moment a test is rerolled after later tests already exist. Fixed by
  scoping the post-draw check to `{cat: picked}` on the reroll path.
  `--reroll-one` scopes it one level further, to the single new entry, for the
  same reason: the kept entries of that category are older draws.
- **Attribution** — pass `--test-id <id>` so each draw records its consumer.
- **What gets RECORDED is the pool entry-string, never the paper's surface
  form or a substitute.** `recency_map()` keys on the raw string and
  `head()` — an inflected realization or an off-pool substitute cools
  nothing and can never rotate. Repair by re-sampling, never by editing
  either file to match the paper.
- **The legacy exemption is a QUEUE, and the queue is PRINTED.** The nine specs
  marked `{"legacy": true}` were drawn before each category was checked against
  its own `cooldown_for()` window, and re-sampling an already-authored paper is
  banned — so they keep their skip. What is not allowed is the skip being where
  the list stops existing: `check_legacy_item_repeats()` WARNs one line per live
  repeat, by item and by paper pair, and the list only shrinks when a paper is
  actually re-drawn. As of 2026-08-21 it holds **eleven items over nine paper
  pairs, 3–5 draws apart against windows of 26–47** (`orthography` 歌謡/果実/
  努める/系統/育児, `usage` 持参/大まか/宣伝する, `paraphrase` あらかじめ/どなる,
  `context_words` ええと) — 「宣伝する」 keys 問題6 in two papers a learner may take
  back to back, which is what a hidden queue costs (REPORT-GOI §F8).

### A `grammar_p8` draw whose form is a general-purpose sentence pattern obliges a prose grep

**Some `grammar_p8` entries are not N2 headwords at all** — `理由説明(〜のは…からだ)`,
`換言要約(〜つまり…ということだ)`, `対比表現(〜一方…だ)`, `例示指示(〜例えば…)` name
frames that any expository writer uses without thinking. 400 lines of 問題10–14
prose cannot be kept clear of one by luck, and `question-authoring` Item
integrity #15 ("a tested form stays out of the reading passages") binds them
exactly as it binds 〜かねない.

**So the draw carries an authoring obligation, and it is a STEP in the stage-3
handoff, not a hope:** when a drawn `grammar_p8` entry is a general-purpose
pattern, grep the drafted 読解 passages for its frame — **both copula spellings**
(`からだ`/`からである`, `のだ`/`のである`) — and re-word every hit but at most one,
which must not be in the tested syntactic frame. Re-wording is cheap and never
touches the item; re-keying is the fallback.

`20260819_1` drew `理由説明(〜のは…からだ)` for 問題8-47 and shipped 問題10(1) and
問題11(3) both closing a sentence with 「…のは、…からである。」 — the exact 文末
cleft-reason frame the item tests, twice, invisible to every gate for two
independent reasons (`qa-report-20260819_1-round2` R2-F5). The mechanical half
is now real: `check_key_grammar_exposure()` reads the FORM through
`grammar_form_tokens`/`grammar_form_parts` instead of the 類型 LABEL and folds
`である`→`だ`, so the ≥2-occurrence COUNT is measured. The judgement half is not
mechanisable — a cleft-reason sentence is not distinguishable from ordinary
prose by regex in every frame — so the gate ships the count and the author owns
the reading.

**A recorded seed is replayable only against the pool it was drawn from — so
every spec records `pools_sha` (R7, 2026-08-19).** `draw()` consumes a fixed
number of RNG values per category, so deleting one entry changes WHICH items a
category picks **without shifting the stream**: the later, unaffected categories
replay bit-exactly and the earlier ones silently do not. `20260818_1`'s QA hit
exactly that — its recorded seed reproduced 6 of 11 categories after
`pools.json` changed four hours after the draw, and the reviewer had to infer
the intermediate pool state from commit timestamps. `sample_items.py` now stamps
the first 12 hex of sha1 over `pools.json` into both `test_spec.json` and the
ledger entry (a reroll re-stamps, since it re-draws against the current pool).
`check_pools_sha_replayability()` **reports** a mismatch and never fails it: a
legitimate pool repair invalidates every earlier stamp, and failing on that
would punish the fix. Never re-sample an authored test to add a stamp — the 13
papers predating the field are a documented skip, not a defect.

Every spec carries `"rotation": {"recency_source": "ledger", "history_len":
2, "cooldown": 6}` — `cooldown` is the WEAKEST level actually applied to any
category that draw (usually set by the thinnest pool, e.g. `grammar_p8`).
`assert_rotation()` re-checks the claim against the ledger; a red line means
`draw()` is broken — never lower a cooldown to make it green. Keep every pool
≥2.5× the per-test draw; inspect with `sample_items.py --check-depth`.

**2026-08-17: both `assert_rotation()` and `check_spec_rotation()` checked
every category against ONE spec-wide scalar** — a real bug: anything with a
deeper pool than the draw's thinnest category was never actually
re-verified (`kanji_reading`'s 303-draw window collapsed to a 6-draw check).
Found alongside a separate process violation: `20260817_1`'s QA found the
drawn 問題1 target `居酒屋(いざかや)` undrawable and swapped in a hand-picked
substitute instead of `--reroll kanji_reading` — the single-scalar bug meant
even a re-run wouldn't have caught the resulting repeat. Fixed both functions
to verify per category via `cooldown_for(cat, len(pools[cat]))` — the same
ceiling `draw()` itself enforces. The 9 tests shipped before the fix carry
unverifiable rotation claims and are marked `"rotation": {"legacy": true}`
(never re-sample an already-authored test to clear a legacy skip). **The
standing rule was never the gap: an undrawable target still means `--reroll
<category>`, never a hand-picked substitute** — only the after-the-fact
enforcement was missing.

**A draw count that disagrees with `DRAW` is a ledger defect, not history.**
A recorded item burns cooldown regardless of whether the paper used it;
entries under a superseded `DRAW` over-record. Trim over-recorded items;
never let them expire through cooldown. Shortfalls are not trimmable — record
what the paper actually used.

## Answer positions are balanced globally across the paper, unpredictable inside sections

Do not force each mondai to carry equal quotas of positions 1..4 — that makes
key distribution within each mondai predictable. Two bars instead, and
`balanced_position_plan()` satisfies both at once:

1. **Whole-paper balance.** Each position takes 19–27 of the 90 four-choice
   items (`POSITION_BAND`), and no position runs more than `MAX_POSITION_RUN`
   times anywhere in the paper, **section seams included**.
2. **Per-大問 shape drawn from the archive.** Each section's row is built by
   `section_row()`: its mode COUNT is drawn from `SECTION_MODE_DIST` — the
   measured per-大問 distribution over the era-matched sittings — and realised by
   rejection sampling over i.i.d. rows. Conditioning on the mode count leaves
   WHICH position clusters uniform, so the shape is calibrated and the identity
   of the clustered option stays unpredictable.

Individual sections therefore repeat positions the way official papers do
(`[2, 4, 2, 1]`, `[3, 3]`), at official's own rate. 聴解 問題4 (3-choice) gets
the same treatment against its own distribution and is not part of the 90.

```
MAX_POSITION_RUN = 3   # longest same-position run allowed anywhere in the deck
POSITION_BAND_3 = (2, 6)   # per-position count band, 聴解 問題4 (11 items)
MAX_SECTION_MODE = {...}   # per-大問 CEILING on the most-frequent position
SECTION_MODE_DIST = {...}  # per-大問 TARGET distribution of that mode count
```

The two mode tables are one measurement read two ways — the ceiling is
`max(SECTION_MODE_DIST[section])` — and `sample_items.py` asserts that at import
so they cannot drift apart under a hand edit.

### `MAX_SECTION_MODE` — the ceiling the balance contract was missing

Global balance and a run cap do **not** bound how many of one section's keys
land on one option: a run cap only constrains ADJACENT items. `20260818_1`
drew 問題7 = `[1,1,2,4,4,1,1,1,2,1,1,1]` — **eight of twelve keys on option 1**
— and 問題4_語彙 = `[1,1,4,1,3,1,4]`, four of seven, with every gate green
(`qa-report-20260818_1` F1). The 2026-08-18 audit above examined only the
too-SMOOTH tail; nothing had ever looked at the other end, and no ceiling
existed in the code or in this file.

`MAX_SECTION_MODE` in `sample_items.py` is the **maximum mode count observed
per 大問 over the 31 sittings** in `refs/JLPT_N2_NEW/answer_keys.json`, measured
only on the sittings whose item count for that 大問 equals today's — 問題3 5→3,
問題9 5→4, 問題11 9→8, 聴解問題4 12→11 and 聴解問題5 4→3 all changed at 12/2022,
and mixing eras inflates the ceiling (聴解問題4 reads 7 across all 31 but **5**
over the 18 current-shape sittings). Re-derive by re-measuring the archive,
never by reading a paper:

| | 問1 | 問2 | 問3 | 問4 | 問5 | 問6 | 問7 | 問8 | 問9 | 問10 | 問11 | 問12 | 問13 | 問14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ceiling | 3 | 3 | 2 | 3 | 3 | 3 | **5** | 3 | 2 | 3 | 4 | 2 | 2 | 2 |

聴解: 問題1 4, 問題2 4, 問題3 4, 問題4 **5**, 問題5 2.

`balanced_position_plan()` re-draws a plan that breaches the table, and
`check_answer_position_section_clustering()` FAILs a spec that does. It holds by
construction now — every mode count the target distribution can draw is a count
the archive shows — so a breach at the gate means the two tables have drifted.

**It is a CEILING, not a target** — and a ceiling alone was the wrong
instrument, which is `SECTION_MODE_DIST`'s whole reason for existing.

### `SECTION_MODE_DIST` — the target the ceiling could not express (R2-F8)

問題7's own official distribution is mode 3 in 14 sittings, 4 in 16 and 5 in
exactly **one**, so a generator that lands on 5 every paper reproduces a shape
official does not have — the same failure `bunpou.md` §問題7 documents for stem
length. Measured 2026-08-19, the ceiling-only sampler was doing exactly that in
**eight sections at once**, because slicing one globally balanced deck makes each
section's mode multinomial while official balances *within* each 大問:

| 大問 | official (era-matched) | sampler, ceiling only | sampler, with `SECTION_MODE_DIST` |
|---|---|---|---|
| 問題3 | 1:92 % 2:8 % | 1:39 % 2:61 % | 1:93 % 2:7 % |
| 問題4_語彙 | 2:80 % 3:20 % | 2:24 % 3:76 % (**inverted**) | 2:80 % 3:20 % |
| 問題7 | 3:45 % 4:52 % 5:3 % | 3:5 % 4:56 % 5:40 % | 3:48 % 4:48 % 5:4 % |
| 問題9 | 1:64 % 2:36 % | 1:10 % 2:90 % | 1:64 % 2:36 % |
| 問題1/2/5/6/8 | 2:94–97 % | 2:62–68 % | 2:91–98 % |
| 聴解問題4 | 4:61 % 5:39 % | 4:40 % 5:60 % | 4:61 % 5:39 % |

(400 simulated plans per column, era-matched against
`refs/JLPT_N2_NEW/answer_keys.json`; every other section matches within noise
too.) **Do not "fix" the skew by lowering the ceiling below 5** — that would
reject a real official sitting. The fix is the distribution, and mode 5 stays
reachable at its official 1-in-31 rate. This changed the RNG consumption of
`balanced_position_plan()`, so a seed recorded before 2026-08-19 no longer
replays its own `answer_positions`; the 13 papers on disk keep the positions
they shipped (never re-sample an authored test) and no gate line moves, because
the ceiling predicate is unchanged.

**Repairing an already-authored paper.** Do not hand-edit a drawn position to
taste. Permute the printed option ORDER of the affected items so the key lands
on a compliant slot — item content, stems and distractor sets survive
unchanged — and keep the paper's global totals inside `POSITION_BAND` by
SWAPPING with an item elsewhere that gives up the position the moved key takes.
Then re-sync `answer_positions`, both key tables, every 解説 that names an
option number (`check_mondai7_option_refs` reads 問題7's) and the 問1–6
functional-category line, which lists the options in printed order. Worked
example: `20260818_1` moved 4 of 問題7's eight `1`s and 1 of 問題4's four, in
five swaps with 問題1-1/問題2-8/問題3-11/問題5-22/問題5-23, leaving the totals at
22/23/22/23 exactly.

### The algorithm is calibrated; 8 shipped papers still all landed maximally smooth

Measured 2026-08-18 against a user report that 聴解 keys "arrange very
evenly" within a mondai. Official itself clusters hard — over all 31
sittings' 問題1/問題2 key rows, the most-frequent position within one section
repeats 3–4 times in 29%/48% of sections respectively (e.g. `4. N2 7-2013`
問1 keys `2,2,3,3,3`). Every one of the 8 shipped papers instead had its
most-frequent position appear at most twice — never matching official's
clustering. Simulating `balanced_position_plan()` over 3,000 seeds at the
real deck offsets reproduces official's distribution almost exactly — **the
algorithm is not the defect**; 8 real draws all landing smooth is a
low-probability coincidence (~0.01% joint), not proof of a bug, but not
something to wave away twice either. Fixed the run-length cap the same pass
(originally banned ANY run of 3, stricter than official's own observed max
run of 3 — now `MAX_POSITION_RUN = 3`, i.e. no run of 4+). **Do not
"fix" this by hand-editing a drawn position to look more clustered** — that
manufactures the exact predictable pattern the report complains about. A
naturally-clustered draw is not a defect to smooth out; only **every** 聴解
4-choice section of **several consecutive papers** landing at max-count ≤2
would be the actual signal worth re-auditing.

### 聴解_問題4 (3-choice, 11 items) WAS the real bug — fixed 2026-08-18

Unlike the sections above, 問題4's old `balanced_positions()` built its base
list as `[(i % width) + 1 for i in range(count)]` and only ever *reshuffled*
it — the per-position COUNTS were never randomized, so `count=11, width=3`
produced exactly 4/4/3 on every single draw, forever (checked: all 5 shipped
papers with a real key table are 4/4/3). Official varies — July 2025 keys a
3/5/3 split. That was fixed 2026-08-18 by drawing each position independently
and rejecting until the counts sat inside `POSITION_BAND_3` with no run of 3;
`balanced_positions()` was then folded into `section_row()` (2026-08-19, R2-F8),
which keeps both of those constraints and additionally matches 問題4's measured
mode distribution {4:61 %, 5:39 %} instead of drifting to {4:40 %, 5:60 %}. Both
changes affect only the NEXT draw; already-authored tests keep their shipped
positions.

## Adjunct one-shots (non-pool items — staging stays live)

Nothing enters a test without N2 evidence. `sample_items.py` may replace up
to **20%** of each category's draw with `status=ready` rows from
`logs/adjunct_staging.json` (`--no-adjunct` for pure pool). Records look like
`{"item": "…", "origin": "adjunct", "level": "N2", "evidence": [...]}`;
author them like pool items — `make check` enforces the cap and provenance.

**Adjunct evidence must cite a currently-valid source.** `20260811_1`
shipped a row citing `openjlpt` 32 minutes after that corpus was deleted from
the repo — never cite `openjlpt` in new evidence, and never copy a prior
test's adjunct row verbatim; re-derive fresh against Shin Kanzen/Soumatome or
the official archive each time. `check_draw_provenance()` FAILs any adjunct
row citing `openjlpt`. The item itself must still clear the N2 band on its
own merits — a stale citation and an off-level word are different defects.

## Archived growth tooling

`archive/` holds only `promote_adjunct.py` (grows `pools.json` from approved
staging rows) — no Makefile target, must be moved back into `scripts/` to run.
`classify_level.py`/`expand_pools.py`/`suggest_pool_additions.py`/
`fetch_openjlpt.py` were **deleted, not archived** (2026-08-11) — all four
existed solely to work against the now-deleted `openjlpt` corpus. Growing a
pool now means an author reading Shinkanzen/Soumatome (or the archive) and
hand-adding entries — see `archive/README.md`.

## `scripts/sample_items.py` — usage

**The seed must be an RNG output, never a number the agent writes down** —
agent-picked seeds are date-shaped and collide across sessions:

```bash
python3 -c "import secrets; print(secrets.randbelow(10**8))"   # any platform
SEED=$(python3 -c "import secrets; print(secrets.randbelow(10**8))")
python .agents/exam-blueprint/scripts/sample_items.py --seed "$SEED" --test-id <id>
python .agents/exam-blueprint/scripts/sample_items.py --check-depth
python .agents/exam-blueprint/scripts/sample_items.py --reroll listening_scenarios --seed "$SEED"
python .agents/exam-blueprint/scripts/sample_items.py --reroll-one quick_response:8 --seed "$SEED"
```

**`--reroll-one <category>:<index>` redraws ONE drawn entry** (R2-F2,
2026-08-19), under exactly the same exclusions as a full reroll: this paper's
other picks in every category — including the same category's KEPT entries — plus
that category's own cooldown window. It records itself in the seed expression as
`+reroll-one(cat:idx,seed)`, re-stamps `pools_sha`, and writes the updated list
to both the spec and this test's ledger entry, so `check_draw_provenance()` still
resolves. Use it when ONE drawn entry is the defect: `--reroll quick_response`
replaces all **eleven** stimuli and forces a whole-問題4 re-author plus an MP3
rebuild to repair one of them, and that cost is what invited the cheaper wrong
repair — `20260818_1` drew two 「窓口:記名依頼」 stimuli and the first fix pass
re-angled one item's invented SETTING instead of redrawing the errand, which is
not what the rule measures (`qa-report-20260818_1-round2` R2-F2). The sanctioned
repair now costs one item. **It is still a redraw, not a hand substitution** — the
index selects WHICH entry leaves, never which entry arrives.

`tests/<test_id>/test_spec.json` is the authoring contract — per section,
the exact items to test, scenario/topic lists, and the answer-position
sequence. **It belongs to ONE test and may predate the current `DRAW`.** Do
not "reconcile" an already-authored test by re-sampling; re-sample for the
NEXT test.

Author questions ONLY for the sampled items — if one is genuinely unusable,
`--reroll <category>`, never substitute from memory; when the sampler warns
that sampled `listening_scenarios` share a domain prefix and run the same
errand, `--reroll` before writing anything; place each correct answer at the
spec's position and design distractors around it; record the seed in the
source file header; new items go through staging, never inlined ad hoc.

`pools.json` categories: kanji_reading, orthography, word_formation,
context_words, paraphrase, usage, grammar_p7, grammar_p8, quick_response,
listening_scenarios, reading_topics. Pools may legitimately overlap; what
matters is depth.

---

# Part II — Author the passage yourself

`sample_items.py`'s draw assigns one `reading_topics` entry to every 読解
surface of 問題10–14 (12 = 5 short + 4 medium + 1 A/B + 1 long + 1 info — 問題9
cloze has no pool seat: its author composes the topic, keeping it distinct
under the four theme rules, and the build pass records what shipped as a
13th `reading_topics` entry with `origin: "reauthored"` + note) and one
`listening_scenarios` entry to every 聴解 setting (問題1/2/3/5). Compose every
passage/dialogue/flyer/notice/即時応答 setting yourself, in original prose,
directly from that assigned string. No external source, no fetch, no citation.

Apply this N2 gate to your own draft:

- **Expressibility.** Draft one sentence using only N2-and-below vocabulary;
  generalize anything needing N1 jargon (生成AIの著作権問題 → 新しい技術と
  仕事の変化).
- **Neutrality.** Avoid politics/elections, religion, war/crime/accidents
  with victims, discrimination debates, celebrity gossip, anything
  distressing. Prefer daily life, work customs, technology in daily use,
  food, travel, education, environment, community, non-medical health habits.
- **Invented specifics.** A survey figure or flyer detail you write is your
  own invention, N2-rounded (approximate, not a decimal) — never phrased as
  a citation of a real source.
- **Original composition.** Write from the topic string outward. Never copy
  from `refs/` (calibration only).

## Freshness — creative recombination

Force novelty combinatorially, rolled with the spec's RNG seed (never model
preference): scenario = random(place) × random(complication) × random(constraint),
e.g. 市役所 × 必要書類が足りない × 締め切りは今日中. Reach for this whenever a
bare topic/scenario string doesn't yet suggest a concrete scene.

## What still governs a self-authored surface

- **`sample_items.py`'s pool rotation and theme rules are unchanged** —
  they bind every surface regardless of how it's written.
- **The whole-paper topic pass stays mandatory** (`jlpt-test-generation`
  §"One topic, one surface") — the guard against a subject repeating within
  the paper or the previous two tests in a renamed form.
- The TESTED item is always the pool-sampled item from `test_spec.json`;
  the assigned topic sets scene and content only.
- **A drawn `listening_scenarios` string names both a SETTING and an
  ERRAND** (`空港:搭乗手続きの案内` = airport SETTING, boarding-procedure
  ERRAND) — the authored dialogue must match both. If the errand genuinely
  doesn't fit, `--reroll listening_scenarios`, not a free rewrite of the
  label's second half.

**`logs/topics.json`** — the whole-paper topic table, one row per test,
written by the build pass. Each row carries `surfaces` (every 読解 passage,
問題9, 問題14, every 聴解 item incl. 例, one noun phrase each), `themes` (same
keys → a `THEMES` value), `shapes` (each 聴解 item's errand shape). No
subject or shape may repeat within the paper or against the previous two rows.

**The honest limit.** 「屋上緑化」 vs 「グリーンパートナー制度」 are one
subject with zero shared tokens, and no mechanized check catches that —
**subject identity cannot be mechanized**; the human whole-paper topic table
pass stays mandatory, and a green topic check is not evidence the paper is new.
