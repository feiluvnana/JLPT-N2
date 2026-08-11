---
name: exam-blueprint
description: Single owner of WHAT each exam tests — RANDOM, non-repeating pool sampling of grammar points, vocabulary, kanji, listening scenarios, and reading topics, and answer-position balance. Use BEFORE authoring any questions, whenever generating a new test, whenever the user asks for "another test", "random questions", "different questions", or says tests repeat, feel stale, or feel textbook-bound. Never let the language model choose items from memory — model choices are heavily biased toward the same famous items and are NOT random; selection must come from scripts/sample_items.py.
---

# Exam Blueprint — pool sampling

## Why this skill exists, and the invariant it owns

A model asked to "pick 12 N2 grammar points" picks nearly the same 12 every time, reuses
the same scenarios, and biases keys toward positions 2-3 — determinism wearing a
randomness costume. Hence four mechanisms: **explicit pools**
(`references/pools.json`), **seeded RNG sampling** (`scripts/sample_items.py` — code,
not vibes), an **LRU coverage ledger** (`logs/ledger.json`), and **answer-position
balancing**.

**Tested linguistic items are always the pool's, topics are always yours to write.**
Grammar, vocabulary, kanji, idioms/keigo ALWAYS come from `pools.json`, calibrated
against the Shin Kanzen Master inventories; the assigned `reading_topics`/
`listening_scenarios` entry sets the scene and content, and the author writes the
passage/dialogue from it directly at N2 level (Part II below) — no external source, no
harvest, no blend ratio to hit. Where this sits in the generation workflow is owned by
`jlpt-test-generation` (pass table).

---

# Part I — The pool and the draw

## Pool entries stay inside the N2 band

Do not add N1-only forms or N3–N5 drills to `references/pools.json` — the banned lists
live in `question-authoring/references/level_band_grammar.txt`. `make check` fails papers
whose 問題7–9 keys hit that list **and checks the pool itself**: a `TOO_EASY` form
(`〜ば〜ほど`) sat in `grammar_p8` because the paper check only matches the
keyed *option string*. A banned pool form is a defect when committed, not when drawn.

**A `kanji_reading` entry must come with a writable distractor set, or it is not a pool
entry.** The 問題1 two-branch distractor rule is owned by `question-authoring`; for some
entries its intersection is **empty**, and an author who has already drawn the target
invents non-words instead of rejecting it (e.g., 「労わる」). Before adding or keeping
an entry, write its three distractors with their source kanji; if you cannot, it is out.

**A pool spelling must match its headword in Shin Kanzen Master N2-Goi/N2-Kanji or
日本語総まとめ N2 語彙/漢字** (`refs/Shinkanzen/`, `refs/Soumatome/`). 問題1 tests a
reading off a printed spelling, so okurigana is part of the item (`労わる` vs the
dictionary's `労る`). Fix the pool, never just the paper.

### The `kanji_reading` validity rule (audited 2026-08-06)

Unanswerable 問題1 items (such as `領(えり)`, `線(すじ)`, `爆(は.ぜる)`) ship
when nothing checks that the printed kanji actually *has* the keyed reading. Every entry
must satisfy all four:

1. **Shape.** `語(よみ)`: `語` contains a kanji; `よみ` is hiragana, **no `.` and no
   katakana** (a dot is a raw KANJIDIC kunyomi with okurigana detached; katakana is a
   bound-morpheme on-reading dump — neither is a printable word).
2. **Attested.** `(語, よみ)` appears as a headword + reading in Shin Kanzen Master
   N2-Goi/N2-Kanji or 日本語総まとめ N2 語彙/漢字 — decisive for **single-kanji** entries,
   which have no fallback (`針(はり)` is a headword and legitimate; `領(えり)` is not).
2b. **One 語, two 訓読み → keep the LOWER-graded reading.** `潜る(くぐる)` is attested —
   at N1, beside N2 `潜る(もぐる)`; the harder member turns the item into "which reading
   did the examiner mean". Keep the lowest-graded entry, delete the others; rank by
   whether the reading is the one carried in the Shinkanzen/Soumatome N2 volume (present
   there → N2; recognizably harder and absent from the N2 volume → N1 by trained
   Japanese-vocabulary knowledge) or by which reading the official archive
   (`refs/JLPT_N2_NEW/`'s `booklet.md`/`key.md`) actually keys. `question-authoring`
   carries the paper-side half, but the pool entry is the defect — repair it here.
3. **In band, if the reference misses it.** A **multi-character** word not found on the
   author-checked pages of the Shinkanzen/Soumatome N2 volumes stays only when its
   reading is the ordinary dictionary reading on 常用 音訓 *and* the word is corroborated
   by the official archive under `refs/JLPT_N2_NEW/`. A reference-book miss is often a
   gap (概要, 潜む); zero hits in **both** sources is the removal signal.
4. **Drawable.** Three distractors writable (see `question-authoring`).

**Verify against Shin Kanzen Master N2-Goi/N2-Kanji and Soumatome N2 語彙/漢字 — never a
bare kanji dictionary.** A KANJIDIC-style raw readings list carries 表外 readings (the
source of the previously-shipped `領: えり` defect) and can refute an okurigana shape but
never *confirm* an entry; the same trap applies to any future word/reading index, so
never stand one up as a shortcut. Both the Shinkanzen and Soumatome N2 PDFs are scanned
images with **no text layer** (confirmed via `pdftotext` — zero lines extracted from
either the Soumatome Goi PDF or the Shinkanzen Goi PDF), so there is no grep-able
replacement for a corpus lookup: verify a candidate by reading the relevant PDF pages
(the Read tool's PDF vision support) or by trained Japanese-vocabulary knowledge
cross-checked against these books; for a reference-book miss, corroborate against the
official archive's already-OCR'd `booklet.md`/`key.md` under `refs/JLPT_N2_NEW/` —
calibration only, never copy an official item.

The 2026-08-06 audit removed **103** of 218 entries and repaired `免れる(まぬがれる)` →
`免れる(まぬかれる)`; 112 remain, 22× headroom over `DRAW` of 5. **`kanji_reading` is the
only category whose parenthetical is a reading** — `納める(税金)` is context,
`詫びる(謝る)` a synonym, `諸〜(諸問題)` an example; the rule does not apply to them.

**2026-08-11: grown to 200 via `vocab-n1/n2/n3.json`, never `kanji-n2.json`.** The
(now-deleted) `expand_pools.py`'s `expand_kanji()` sourced `kanji_reading` candidates from
`vocab-n1/n2/n3.json` word+reading pairs rather than `kanji-n2.json` (KANJIDIC) — exactly
the banned authority above, and exactly how `領(えり)`/`爆(は.ぜる)` shipped before the
2026-08-06 audit had to remove them. That construction made Shape and Attested (rules 1–2)
hold by construction, and additionally enforced rule 2b (keep only the lower-graded
reading of a two-訓読み word, via `word_reading_levels()`) at build time instead of
leaving it to a later audit. Rule 4 (drawable distractors) was never pre-verified per
entry — see `question-authoring/references/moji-goi.md` §"Build the set BEFORE you accept
the target" for the authoring-time re-draw path when an entry turns out undrawable; that
has always been how the pool handles it, not a gap this pass introduced.

**2026-08-11 (later still): `openjlpt` fully removed.** The `references/openjlpt/` data
directory and its four consuming scripts (`classify_level.py`, `expand_pools.py`,
`suggest_pool_additions.py`, `fetch_openjlpt.py`) are gone from the repo — only
`promote_adjunct.py` remains archived, since it never touched `openjlpt` (see "Archived
growth tooling" below). Any further `kanji_reading` growth is manual from here: read the
Shinkanzen/Soumatome N2 volumes (or corroborate a reference-book miss against the official
archive) and hand-verify all four rules above before adding an entry — there is no script
left to source or pre-check candidates. The two automated `make check` gates that
depended on `openjlpt` in `tools/check_consistency.py` — `check_mondai1_key_band()`
(enforced rule 2b above; the exact rule that caught the previously-shipped `免れる`
reading defect) and `check_moji2_stem_kana()` (問題2 stem-kana-matches-key check) — have
likewise been deleted already, by parallel work on this same removal. Both rules are now
enforced by manual review only (`exam-qa-review`, `question-authoring`), not by
`make check`; a green gate no longer proves either one held, so read those skills'
relevant sections with the same rigor `make check` used to substitute for.

## One grammar point, one pool entry (no spelling variants)

The sampler's cross-category `taken` guard compares **raw strings**, so two spellings of
one point are two items to the code: `grammar_p7` carried `〜気味` + `〜ぎみだ` resulting in
keying one point twice in one 問題7.

- **One spelling per point.** Not kanji *and* kana (`〜に伴って` / `〜にともなって`), not
  with *and* without an optional tail (`〜つつも` / `〜つつ(も)`), not two conjugations of
  one verb (`〜に沿って` / `〜に沿う`).
- **Cross-category overlap must be spelled identically** — overlap is legal, and `taken`
  keeps an item to one 問題 per test, but only byte-identical entries count
  (`〜わりに(は)` beside `〜わりに` defeated it).
- **A parenthetical is a disambiguating gloss, never a variant.** `〜次第だ` (depends on)
  in `grammar_p7`, bare `〜次第` (as soon as) in `grammar_p8`.

`make check` fails a grammar entry hitting `TOO_HARD`/`TOO_EASY` without an `ALLOW`, and
two same-category entries whose skeletons match after stripping `〜`/`～` and
parentheticals. **The skeleton rule is a floor** — it misses `〜がち`/`〜がちだ` and
`〜気味`/`〜ぎみだ`, the pairs that shipped; read new entries against the rules above.

Known residue, left deliberately (audited 2026-08-06): five `grammar_p7` × `grammar_p8`
pairs where p8's labelled pattern contains p7's bare form — do not add more, and
`--reroll grammar_p8` if a drawn 問題8 pattern repeats a 問題7 point; `taken` is
raw-string (`head()` is recency-only), so `交渉(こうしょう)` and `交渉` can both land in
one paper — the fix belongs in `sample_items.py`, still open;
`〜ずくめ(黒ずくめ)` matches `TOO_HARD` `ずくめ` but is a 問題3 affix — the band check
stays scoped to the grammar categories (elsewhere it produces false hits).

**2026-08-11: `grammar_p7`/`grammar_p8` audited against the Shin Kanzen N2 Bunpou
TOC + 索引 (all 26 lessons, ~211 forms) and found roughly half the book's discrete
forms missing** — two whole lessons (13課's topic-framing cluster `〜とは`/`〜といえば`/
`〜というと`; 21課's emphasis cluster) had zero coverage, and a dozen more lessons were
missing 2-5 forms each. Added 60 N2-band forms to `grammar_p7` (172 total; `grammar_p8`
unchanged at 42), each checked against `references/level_band_grammar.txt`'s bans and
against the skeleton-dup check before landing (`〜上(に)`/`〜限り(は)` were rewritten to
`〜上に`/`〜限りは` — the parenthetical form collided on skeleton with an existing entry).
The previously-malformed `〜に過言ではない` was fixed in place to
`〜と言っても過言ではない`, the form the trap example above actually names.

## `paraphrase`/`usage` katakana rate is capped, not left to the pool's composition

`references/pools.json`'s `paraphrase` pool is 27.1% katakana-containing (38/140) and
`usage` is 32.7% (49/150) — legacy 2級-era loanword entries (バケツ, ダム, ハンドル,
マラソン…) inflate both. The official archive draws a katakana HEADWORD in only 3/35
問題5 items and 1/35 問題6 items (`question-authoring/references/official_calibration.md`
§12) — a plain `rng.sample()` reproduces the pool's ~30% share per draw instead of the
archive's ~5-9% per-item rate, and three generated papers measured before the fix drew 3,
3 and 6 combined katakana headwords against an official average of 0.57.

`sample_items.py`'s `draw()` routes `paraphrase`/`usage` through
`sample_katakana_capped()` instead of `rng.sample()`: it runs `n` independent
Bernoulli(`KATAKANA_TARGET_RATE[name]`) trials to decide how many katakana slots the draw
gets (capped at `KATAKANA_CAP[name]`, never observed above 1 in one section of one paper),
then fills those slots from the pool's katakana subset and the rest from the non-katakana
subset. **Do not derive the target rate from the pool's own katakana share** — that is
the composition being corrected for, not the target; re-derive `KATAKANA_TARGET_RATE` only
by re-measuring the archive (§12), never by recomputing `len(katakana)/len(pool)`.

This does not fix the pool's katakana entries that are themselves too easy for N2 (§12's
second finding) — that is a `kanji_reading`-style band audit still to be done, following
"Pool entries stay inside the N2 band" above.

**2026-08-11: grown the non-katakana side instead of removing the katakana side.**
`expand_pools.py`'s `expand_vocab_cat()` now skips any candidate containing a katakana
character. `vocab-n2.json` had only **1** unused katakana word left (128 of 129 katakana
N2 entries were already in the pool) against **1339** unused non-katakana N2 words — the
pool's ratio came from exhausting the katakana side of the source file while the
non-katakana majority sat untouched, not from a deliberate mix. Growing `paraphrase` to
200 (+60) and `usage` to 210 (+60) from that non-katakana majority dropped the pool ratio
to 19.0% and 23.3% respectively — real progress, but still above the archive's ~5–9%
per-item rate, which is why the sampler cap above still does the actual enforcement; this
expansion is dilution, not the mechanism.

**2026-08-11 (later same day): `usage` audited and its legacy dump removed instead of
diluted further.** Of the pool's 210 entries, only the first 67 were curated for 問題6's
shape (妥協/発揮/解消-style: abstract, collocation-rich, one right domain + three tempting
wrong ones). The remaining 143 were a raw legacy-corpus tail — 49 basic 2級-era katakana
loanwords (ピストル, ビタミン, ピンク…) plus 94 non-katakana entries that `openjlpt`
tags "N2" but are really concrete single-referent nouns with no exploitable domain
(算盤, 座布団, 三日月, へそ…) or otherwise below band — neither shape supports a 問題6
item at all. Removed the 143, added 54 curated replacements (30 abstract nouns/adjectives,
19 collocation-rich verbs, 5 katakana) mined from `vocab-n2.json` and checked against
this doc and `question-authoring/references/moji-goi.md` for domain richness, then
grandfathered back the 6 removed words two already-shipped tests had actually drawn
(`logs/ledger.json`/`test_spec.json` entries must resolve to a live pool string —
`check_draw_provenance()`; removing a historically-drawn entry breaks that, and
re-sampling an already-authored test is forbidden elsewhere in this doc, so the correct
repair here is to keep the word, not to re-draw the test). Net: 210 → 127, katakana share
23.3% → 4.7% (6/127) — close to the archive's ~5–9% rate by composition alone, though the
sampler cap remains the actual enforcement mechanism, not pool composition.

**2026-08-11 (after `openjlpt` removal): `paraphrase` and `usage` grown from
Shinkanzen/Soumatome instead of `vocab-n2.json`.** With `openjlpt` gone, growth is manual:
sampled ~370 pages combined across `refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Goi.pdf` and
`refs/Soumatome/nihongo-soumatome-n2-goi.pdf` (`nihongo-soumatome-n2-kanji.pdf` wasn't part
of this vocabulary pass — it's the kanji volume), harvested candidate words matching each
pool's shape (paraphrase: a hard word with a simpler common synonym; usage: an abstract,
collocation-rich verb/noun/adjective that supports one correct + three
tempting-wrong-domain sentences), then filtered against `pools.json`. Two independent
passes ran concurrently (this repo's own removal-plus-expansion effort) and each missed
some of the other's collisions — a reconciliation pass caught them by normalizing every
candidate's trailing な/だ/に/する/の before comparing (a harvested `衛生的な` against an
existing bare `衛生的`, or `見事な` against a same-pass addition `見事だ`, read as the SAME
headword) and dropped 13 paraphrase near-duplicates and 1 usage near-duplicate
(`普及する` against the pool's existing bare `普及`) that plain string comparison missed.
Net: `paraphrase` 200 → 118 (the legacy-dump audit two entries above) → 156 (+38 from the
concurrent pass) → 143 (−13 reconciled dupes); `usage` 127 → 189 (+62 curated) → 218 (+29
from the concurrent pass) → 217 (−1 reconciled dupe, `普及する` against the pool's existing
bare `普及`). Cross-pool suffix-variant
overlap (a bare `context_words` headword and a conjugated `paraphrase`/`usage` entry of
the same word) was left in deliberately per "Pools may legitimately overlap... what
matters is depth" above — only BYTE-IDENTICAL entries are guaranteed kept apart by the
sampler's `taken` set (see "One grammar point, one pool entry"), so a future audit could
still tighten this, but it is not the defect class that rule targets.

## Topic themes — the closed vocabulary (this skill owns it)

`reading_topics` and `listening_scenarios` entries are **objects, not bare strings** —
`{"topic": "在宅勤務と切り替え", "theme": "働き方"}` — and `theme` comes from a **CLOSED**
list of twenty values, defined once in `scripts/level_data.py` as `THEMES`:

| | | | |
|---|---|---|---|
| 睡眠・健康 | 医療・福祉 | 食 | 環境 |
| 防災 | 交通 | 住まい | 働き方 |
| 教育 | 子育て・家族 | 地域活性化 | デジタル化 |
| 消費・経済 | 文化・伝統 | スポーツ・余暇 | 人間関係 |
| 行政・手続き | メディア・情報 | 旅行・観光 | 科学・技術 |

**Never widen the list to make an entry or seed fit** — a stretched label looks like
agreement and is worse than a wrong one. Pick the nearest value, or say the entry does not
belong. Adding a value is a deliberate taxonomy edit: change `THEMES`, retag every entry
the new value should own, report it. The tags exist because string checks compare
*wording*: 「交替制勤務と睡眠の質」 and 「就寝前の刺激と生活習慣」 pass as two subjects
and the paper tests sleep twice — under the tags both
read `睡眠・健康`, a lookup instead of a judgement.

**What the sampler enforces.** `check_pool_themes()` **fails** on any themed entry that is
a bare string, lacks a `theme`, or carries an off-list value. After the draw,
`check_theme_spread()` **warns** when one theme exceeds `THEME_CAP` (reading **1**,
listening 5) — a re-draw/re-blend decision, not noise. `THEME_CAP` and rule 3 below are one
decision in two places: change either, change the other in the same pass. Reading is the
half that must come out all-distinct, so the draw meets it directly
(`sample_distinct_theme()`) and the WARN is only the backstop for a hand-edited or blended
spec. Listening keeps the WARN-vs-defect **asymmetry deliberately** — the sampler cannot
see which scenario maps to which 問題; do not harden that WARN or soften the prose.

### The four theme rules

**Do the arithmetic first.** A paper authors 12 reading + 21 listening = 33 themed
surfaces against a 20-value vocabulary, so "one surface per theme" is *impossible* and
must never be written as a rule; uniqueness applies to the headline surfaces, the rest
get caps.

> **The headline set** = `問題9` cloze, `問題12` A/B (**one** surface), `問題13` 長文,
> `問題14` flyer, `聴解問題5` 統合理解. Five surfaces.
>
> 1. **Five headline surfaces, five DIFFERENT themes.**
> 2. **A headline theme appears nowhere else in the 読解 half** (e.g., shipping
>    デジタルデトックス as both 問題9 and 問題10(1)). Listening is governed by rule 3 only.
> 3. **Reading: ONE surface per theme — all thirteen 読解 surfaces differ.** Listening
>    caps at ≤5 scenarios per theme (`THEME_CAP`). The reading side is a distinctness
>    rule, not a cap: 13 surfaces against the 19 themes that carry reading entries leaves
>    6 spare, so "no repeat" is arithmetically reachable and a repeat is always a
>    re-angle or a re-draw, never a pool limit. `sample_distinct_theme()` meets it inside
>    the draw; the cloze and every web seat are yours to keep distinct.
> 4. **Cross-test: no theme headlines two consecutive papers, and across the previous two
>    papers together at most ONE headline theme may repeat** (only against the
>    paper-before-last, only once in the set).

**These rules bind pool-origin and web-origin surfaces alike** — scope by surface, never
by origin; an offline all-pool paper is not exempt. The pools are lopsided (`働き方` holds
44 of 240 listening scenarios, `科学・技術` only 2 — hence the listening cap of 5): when a
cap keeps breaching, grow the thin themes in the pool or move a surface's subject; never
stretch a label or raise `THEME_CAP`.

**Previous papers' headline themes** come from the two most recent **generated** papers
still on disk (`imported-*` excluded — an official paper is what others copy; a removed
test's `logs/topics.json` rows are history, not budget). One paper on disk → compare
against it; none → rule 4 is vacuous — **say so in your report either way**. Papers
predating the tagging carry no `theme`: tag their five headline subjects by hand from
their `logs/topics.json` rows.

**How to comply:** after the blend report, write down every surface's theme (pool entries
carry theirs; an `"origin": "web"` entry inherits the theme of the surface it displaced,
or the nearest existing tag); check the five headline themes against each other, then the
読解 list, then the per-theme totals; apply rule 4 and record the prior themes and repeat
count in your final report. A theme tag is a floor exactly as token overlap is: it catches
the renamed subject, not a *shape* repeat or a stretched label — the whole-paper topic
table pass (`jlpt-test-generation` §"One topic, one surface") stays mandatory.

**The four rules bind the SHIPPED surfaces, and only `logs/topics.json` records those.**
The spec-side `check_theme_spread()` WARN can never enforce them: it counts the *draw*, it
cannot see which entry became which 問題, and — the hole 20260810_1 fell through — it
counts nothing at all for the two surface kinds that carry no theme in a spec, the
`cloze_topic` and every `"origin": "web"` entry. That paper's draw held two `働き方`
reading topics, exactly at `THEME_CAP`; the shipped paper held **five**, because the
untagged web ワーケーション seed, the untagged 熱中症 cloze, and a 職場-framed passage
tagged `睡眠・健康` were invisible to every check. So:

- **Every web seed and the cloze inherit a theme, and the inherited value is written down**
  — into the spec entry when you blend (`"theme"` beside `"origin": "web"`), and into
  `logs/topics.json` when you build. An entry with no theme is not "untagged", it is
  uncounted, which reads as compliant.
- **A tag must describe the passage as authored, not the topic as drawn.** Re-tag at build
  time if drafting moved the subject: a 「メンタルヘルスと職場」 essay written entirely
  about corporate systems is `働き方`, whatever the pool row says. Re-tagging is the honest
  repair; the defect is authoring away from the tag and leaving the tag behind.
- `check_topics_themes()` in `tools/check_consistency.py` reads the recorded themes and
  FAILs the four rules on the 読解 half. Papers whose rows predate the field WARN.

## Rotation model (ledger v2 — LRU, not reset)

`logs/ledger.json` is `{"version": 2, "history": [ {test_id, seed, generated_at,
items{...}}, … ]}` — one entry per draw, newest last. A v1 flat ledger migrates
automatically into one synthetic oldest draw.

- **Cooldown, not exhaustion.** An item used within the last `COOLDOWN` (=2) draws is
  ineligible (`ago(x) >= cool`; `apply_adjunct` uses the same test). A pool that cannot
  fill a draw relaxes the cooldown one step at a time, says so, and **the level it
  settled on is written into the spec** — clearing a category's whole history instead
  causes a draw to repeat multiple items from earlier papers.
- **One item, one 問題 per test** — categories draw against a shared `taken` set; a
  post-draw assertion aborts on any collision.
- **Cooldown is by WORD, across categories** — recency tracks both raw string and
  `head()` identity.
- **Attribution** — pass `--test-id <id>` so each draw records its consumer.
- **What gets RECORDED is the pool entry-string — never the paper's surface form, never a
  substitute.** `recency_map()` keys on the raw string and `head()`; neither strips a
  leading `〜` nor undoes an inflection, so a ledger/spec row that does not equal a pool
  string **cools nothing** — an inflected realization (「行かずじまい」 left `〜ずじまい`
  permanently un-cooled) or an off-pool substitute (`キャンセル` for `テニスコート`),
  which can never rotate. Repair by **re-sampling**, never by editing either file to
  match the paper. `check_draw_provenance()` fails any recorded item resolving to neither
  a `pools.json` entry (raw, tilde-stripped, or `head()`-folded) nor an adjunct row with
  `item` + `level: N2` + `evidence`; `origin: web` rows are traced by
  `check_harvest_provenance()` instead.

Every `tests/<test_id>/test_spec.json` therefore carries
`"rotation": {"recency_source": "ledger", "history_len": 2, "cooldown": 2}` —
`recency_source` is always `"ledger"` (a spec without the key predates rotation);
`history_len` is how many **other tests'** draws the recency map covered (`0` means the
draw proves nothing); `cooldown` is the **weakest** level actually applied to any category
(`COOLDOWN` normally, lower under relaxation, `0` when exhausted), read as "no item here
appears in the last `cooldown` ledger entries".

`assert_rotation()` re-checks that claim against the ledger before the spec is written, on
both raw string and `head()`. **A red line there means `draw()` is broken — never lower
`COOLDOWN` to make it green.** Keep every pool ≥ 2.5× the per-test draw; inspect with
`sample_items.py --check-depth`.

**A draw count that disagrees with `DRAW` is a ledger defect, not history.** A recorded
item burns cooldown whether or not the paper asked about it; entries written under
superseded `DRAW` values over-record items no question used. **Trim over-recorded items;
do not let them expire through cooldown.** Shortfalls are not trimmable: record what the
paper actually used. `make check` asserts every history entry except `legacy` matches
`sample_items.DRAW`; a red line means repair the ledger, never widen the check. (Ledger
repair is paper-repair work, not pool work.)

## Answer positions are balanced across sections, not only inside them

Per-section `[(i % width) + 1 …]` filling is even *within* a section but hands every
`count % 4` remainder to the lowest positions — a structural +15/+7/+4/+0 on positions
1/2/3/4 over the 18 four-choice sections (e.g. an unmanaged distribution yielding 31 keys on position 1).
`balanced_position_plan()` keeps the per-section floor allocation and gives each remainder
to whichever positions are furthest behind **paper-wide** (realised 22/23/23/22). Never 3+
identical positions in a row; 即時応答 keys are uniform over 1-3.

`POSITION_BAND = (19, 27)` — each of positions 1-4, over the 90 four-choice items. **The
band is PROVISIONAL** (90/4 = 22.5 ± a working tolerance). If measurement of the official
archive disagrees, **change the two numbers** — never reinterpret the band to fit a draw.
The sampler exits rather than emit a plan outside it. 聴解 問題4 (3-choice) is balanced
section-locally and is not part of the 90.

## Adjunct one-shots (non-pool items — staging stays live)

Nothing enters a test without N2 evidence. `sample_items.py` may replace up to **20%** of
each category's draw with `status=ready` rows from `logs/adjunct_staging.json`
(`--no-adjunct` for pure pool). Adjunct records in `test_spec.json` look like
`{"item": "…", "origin": "adjunct", "level": "N2", "evidence": [...]}`; author them like
pool items — `make check` enforces the cap and provenance. **The staging file is live; the
growth tooling is archived** (below). Never inline an unclassified string into a test,
`pools.json`, or the staging file.

## Archived growth tooling

`archive/` now holds only `promote_adjunct.py` — it grows `references/pools.json` by
promoting approved `logs/adjunct_staging.json` rows, and never touched `openjlpt`. Pool
growth is paused; it has **no Makefile target** and must be moved back into `scripts/` to
run (it imports `level_data.py` as a sibling) — see `archive/README.md`. Restore it if the
sampler starts reporting exhausted categories.

**2026-08-11: `classify_level.py`, `expand_pools.py`, `suggest_pool_additions.py`, and
`fetch_openjlpt.py` were deleted, not archived.** All four existed solely to
classify/fetch/expand `pools.json` against the vendored OpenJLPT N1–N3 JSON slices
(`references/openjlpt/`), which is itself deleted — the pool authority is now Shin Kanzen
Master (`refs/Shinkanzen/`) and 日本語総まとめ N2 (`refs/Soumatome/`) exclusively (see
"Pool entries stay inside the N2 band" above). Both are scanned PDFs with no text layer,
so there is no scripted equivalent of the old classify/expand pipeline — growing a pool
now means an author reading the relevant Shinkanzen/Soumatome pages (or the official
archive) and hand-adding entries, the same way `promote_adjunct.py`'s staging rows are
already authored by hand before promotion. See `archive/README.md` for the full account.

## `scripts/sample_items.py` — usage

**The seed must be an RNG output, never a number the agent writes down.**
Agents left to "pick" a seed produce date-shaped, memorable values that collide
across separate sessions, which is exactly the collision the seed exists to prevent.
Generate it by running a command and use the printed value verbatim:

```bash
python3 -c "import secrets; print(secrets.randbelow(10**8))"   # any platform
# PowerShell equivalent: Get-Random -Maximum 100000000
```

```bash
SEED=$(python3 -c "import secrets; print(secrets.randbelow(10**8))")
python .agents/exam-blueprint/scripts/sample_items.py --seed "$SEED" --test-id <id>
python .agents/exam-blueprint/scripts/sample_items.py --check-depth
python .agents/exam-blueprint/scripts/sample_items.py --reroll listening_scenarios --seed "$SEED"
```

`tests/<test_id>/test_spec.json` is the authoring contract: per section, the exact items
to test, the scenario/topic lists, and the answer-position sequence per 問題. **It belongs
to ONE test and may predate the current `DRAW`.** Do not "reconcile" an already-authored
test by re-sampling — that rewrites the contract its 101 keys were placed against.
Re-sample when you start the NEXT test, and read the printed draw counts then.

Binding rules for the authoring step: author questions ONLY for the sampled items — if one
is genuinely unusable, `--reroll <category>`, never substitute from memory; when the
sampler warns that sampled `listening_scenarios` share a domain prefix and they run the
same errand, `--reroll listening_scenarios` before writing anything; place each correct
answer at the position the spec dictates and design distractors around it, not the other
way; record the seed in the exam's source file header (comment); new items learned from
reference books go through staging via the archived tooling, never inlined ad hoc.

`pools.json` categories: kanji_reading, orthography, word_formation, context_words,
paraphrase, usage, grammar_p7, grammar_p8, quick_response, listening_scenarios,
reading_topics. Pools may legitimately overlap (the sampler keeps overlaps apart within a
test); what matters is depth.

---

# Part II — Author the passage yourself

`sample_items.py`'s draw assigns one `reading_topics` entry to every 読解
surface (問題9-13, cloze included) and one `listening_scenarios` entry to
every 聴解 setting (問題1/2/3/5), each carrying its theme tag ("Topic themes"
above). Compose every passage, dialogue, flyer, notice, or 即時応答 setting
yourself, in original prose, directly from that assigned `topic`/`scenario`
string. No external source, no fetch, no citation.

Apply this N2 gate to your own draft:

- **Expressibility.** Draft one sentence introducing the topic using only
  N2-and-below vocabulary; if it needs N1 jargon, generalize it
  (生成AIの著作権問題 → 新しい技術と仕事の変化).
- **Neutrality.** JLPT content stays deliberately unremarkable. Avoid
  politics/elections, religion, war/crime/accidents with victims,
  discrimination debates, celebrity gossip, or anything distressing. Prefer
  daily life, work customs, technology in daily use, food, travel, education,
  environment, community, non-medical health habits.
- **Invented specifics.** A survey figure or flyer detail you write
  (「ある調査によると、約4割が…」) is your own invention, rounded to an
  N2-friendly form (approximate, not a decimal percentage) — never phrase it
  as a citation or attribute it to a real organization or study.
- **Original composition.** Write the passage/dialogue from the topic string
  outward. Never copy from `refs/` (calibration only — `jlpt-test-generation`
  §Invariants).

## Freshness — creative recombination

Force novelty combinatorially, rolled with the RNG seed from
`tests/<test_id>/test_spec.json` (never by model preference): scenario =
random(place) × random(complication) × random(constraint), e.g. 市役所 ×
必要書類が足りない × 締め切りは今日中. Reach for this whenever a bare
topic/scenario string does not yet suggest a concrete scene.

## What still governs a self-authored surface

- **`sample_items.py`'s pool rotation and theme rules are unchanged** — read
  "Topic themes" and "The four theme rules" above; they bind every surface
  regardless of how it is written.
- **The whole-paper topic pass stays mandatory** (`jlpt-test-generation`
  §"One topic, one surface") — the guard against a subject repeating within
  the paper or against the previous two tests in a renamed form (「屋上緑化」
  vs 「グリーンパートナー制度」).
- The TESTED item (grammar point, vocabulary, kanji reading, idiom/keigo) is
  always the pool-sampled item from `test_spec.json["items"]` — the assigned
  topic sets scene and content only, exactly as before.

**`logs/topics.json` — the whole-paper topic table, as a file.** One row per test, written
by the **build pass** from the finished sources (`jlpt-test-generation` stage 3) — what the
paper *actually* tests. Each row carries `surfaces` (every 読解 passage, 問題9, 問題14, and
every 聴解 item incl. the 例 — the shipped subject as one noun phrase), `themes` (the same
keys → a `THEMES` value, every surface included; this is what makes the four theme rules
checkable at all) and `shapes` (each 聴解 item's errand shape, e.g. "reschedule call" — two
subjects can run the identical errand). No subject or shape may repeat within the paper or
against the previous two rows.

**The honest limit.** 「屋上緑化」 vs 「グリーンパートナー制度」 are one subject with zero
shared tokens, and no mechanized check catches that. **Subject identity cannot be
mechanized** — the human whole-paper topic table pass stays mandatory; a green topic check
is not evidence the paper is new.
