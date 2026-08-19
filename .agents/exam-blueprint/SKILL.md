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

**2026-08-11: `grammar_p7`/`grammar_p8` audited against Shin Kanzen's full
TOC (~211 forms)** — roughly half the book's forms were missing, including
two whole lessons with zero coverage. Added 60 N2-band forms to `grammar_p7`
(172 total; `grammar_p8` unchanged at 42), each checked against the band-ban
list and the skeleton-dup check.

## `paraphrase`/`usage` katakana rate is capped, not left to the pool's composition

The official archive draws a katakana HEADWORD in only 3/35 問題5 items and
1/35 問題6 items (`official_calibration.md` §12) — far below what a plain
`rng.sample()` would reproduce from the pool's own katakana share. `draw()`
routes `paraphrase`/`usage` through `sample_katakana_capped()` instead:
`n` independent Bernoulli(`KATAKANA_TARGET_RATE[name]`) trials decide how many
katakana slots the draw gets (capped at `KATAKANA_CAP[name]`), filled from
the katakana subset, the rest from non-katakana. **Do not derive the target
rate from the pool's own katakana share** — that's the composition being
corrected for; re-derive only by re-measuring the archive (§12).

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
genuinely distinct and needs none. Currently 40 entries carry one, in 19
clusters.

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

**And never delete a duplicate to solve it.** Four shipped tests name those
strings in `logs/ledger.json`, and `check_draw_provenance()` requires every
recorded draw to resolve to a pool entry — deleting a duplicate FAILs the gate
on papers that are already out. Add the `key`; a shared `key` is correct data,
never a defect.

**What the gate does with it.** `check_pool_errand_keys()` FAILs a blank or
non-string `key` (drop the field rather than leave it empty — a blank key is an
identity shared with every other blank one) and WARNs the **effective depth**
the clusters cost: 19 clusters currently cost 21 entries, so `cooldown_for()`'s
headroom is optimistic by that many. Resolve that by **growing** the pool, never
by unsharing a key. `check_spec_errand_rotation()` FAILs a draw whose errand a
paper inside its own cooldown window already drew; the nine papers that already
breached it are exempted by name and print the same measurement as a WARN.
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
- **Attribution** — pass `--test-id <id>` so each draw records its consumer.
- **What gets RECORDED is the pool entry-string, never the paper's surface
  form or a substitute.** `recency_map()` keys on the raw string and
  `head()` — an inflected realization or an off-pool substitute cools
  nothing and can never rotate. Repair by re-sampling, never by editing
  either file to match the paper.

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
key distribution within each mondai predictable. `balanced_position_plan()`
generates a globally balanced sequence of the 90 four-choice items (22/23/23/22,
within `POSITION_BAND = (19, 27)`), shuffles with no run longer than
`MAX_POSITION_RUN` anywhere in the deck, and slices into sections in order.
Individual sections naturally repeat positions (e.g. `[2, 4, 2, 1]` or
`[3, 3]`), matching official papers. 聴解 問題4 (3-choice) is balanced
section-locally and is not part of the 90.

```
MAX_POSITION_RUN = 3   # longest same-position run allowed in the 90-item deck
POSITION_BAND_3 = (2, 6)   # per-position count band, 聴解 問題4 (11 items)
```

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
3/5/3 split. `balanced_positions()` now draws each position independently
and rejects until counts sit inside `POSITION_BAND_3` with no run of 3 — a
genuine per-draw distribution. This only affects the NEXT draw;
already-authored tests keep their shipped positions.

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
```

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
