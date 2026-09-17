# Expanding the 聴解 clip bank to the 21 un-imported archive sittings

Status: **DESIGN ONLY — nothing here is built.** Written 2026-09-14 as the
research answer to "which route should future tests get
`refs/JLPT_N2_NEW/`'s 21 older sittings by?". It is the numbered follow-up to
`textbook_bank_plan.md` §6.4, which named the expansion as "the right next move,
one sitting at a time" and costed it in one paragraph. This file re-costs it
with measurements, and the conclusion is **not** the one §6.4 implies.

Every number below was produced by a read-only command that is printed beside
it. Nothing in `logs/` was written; no `make` target that composes, banks or
gates was run (a generation run for `20260914_1` was in flight).

---

## 0. The one-paragraph answer

**Take the hybrid, route C: a third hand-declared source
(`archive_items.json` + `tools/build_archive_bank.py`) that resolves audio
against `refs/JLPT_N2_NEW/` directly, takes its KEY from `key.md` and its
printed options from `booklet.md` (both exact), and requires every line of
learner-visible Japanese to be declared by hand the way
`textbook_items.json` already is.** Route A (21 full imports) buys the same
clips at roughly four times the cost and still needs the same code change;
route B (auto-build from `script.md`) is refused outright, because `script.md`
is OCR and the bank's text fields are printed to the candidate — measured
below at ~7 wrong characters per item and **14 % of spoken-option blocks in the
wrong order**.

---

## 1. What is actually on disk

```bash
ls refs/JLPT_N2_NEW/                 # 31 sitting folders + answer_keys.json
for d in refs/JLPT_N2_NEW/*/; do
  printf '%s mp3=%s md=%s\n' "$d" \
    "$(ls "$d" | grep -ci '\.mp3$')" \
    "$(for f in booklet.md script.md key.md audio_inspection.md; do [ -f "$d$f" ] && echo x; done | wc -l)"
done
```

All 31 folders carry the MP3, the booklet PDF, the script PDF and all four
`*.md` extracts. 10 are imported (`tests/imported-n2-2021-07` …
`imported-n2-2025-12`); **21 are not** — 2010-07 … 2020-12, i.e. every sitting
except the cancelled July 2020.

Bank today (`python3 -c` over `logs/choukai_bank.json`):

| | records |
|---|---|
| official items (10 sittings × 29 slots) | 290 |
| official preambles | 50 |
| hand-declared items (soumatome 37, shinkanzen 21, kanzenmoshi 19, mimikara 4, mondaireishuu 4) | 85 |
| **total** | **425** |

Two official records are `figure_dependent` and undrawable
(`2021-12:問題1-5`, `2022-12:問題1-2`).

---

## 2. The docstring is wrong: the 21 do NOT run 5/6/5/11/2

`tools/build_choukai_bank.py` (module docstring) and
`tools/choukai_segment.py:113` (`EXPECTED_SLOTS`) both assert "All 31 sittings
run the same 5/6/5/11/2 shape". **Measured against
`refs/JLPT_N2_NEW/answer_keys.json`, that is true of 11 sittings and false of
20.**

```bash
python3 - <<'EOF'
import json, collections
d = json.load(open('refs/JLPT_N2_NEW/answer_keys.json'))['exams']
for k, v in sorted(d.items(), key=lambda kv: (kv[1]['year'], kv[1]['month'])):
    ch = [i for i in v['items'] if i.get('part') == '聴解' or i.get('section') == '聴解']
    items = collections.defaultdict(set)
    for i in ch:
        items[i['mondai']].add(i['no'])
    print(f"{v['year']}-{v['month']:02d}", {m: len(s) for m, s in sorted(items.items())})
EOF
```

| era | 問題1 | 問題2 | 問題3 | 問題4 | 問題5 items (answers) |
|---|---|---|---|---|---|
| 2010-07, 2010-12 | 5 | 6 | 5 | **12** | **3 (4)** |
| 2011-07 … 2012-07 | 5 | 6 | 5 | 11 | **3 (4)** |
| **2012-12** | 5 | 6 | **4** | **12** | **3 (4)** |
| **2013-07** | 5 | **5** | 5 | **12** | **3 (4)** |
| 2013-12 … 2017-12 | 5 | 6 | 5 | **12** | **3 (4)** |
| 2018-07 … 2019-12 | 5 | **5** | 5 | 11 | **3 (4)** |
| **2020-12** | 5 | 6 | 5 | 11 | **2 (3)** |
| 2021-07 … 2025-12 (the 10 imported) | 5 | 6 | 5 | 11 | 2 (3) |

Three consequences, and they are the same on route A and on route B:

1. **`EXPECTED_SLOTS` must become era-aware.** It is read in four places —
   `choukai_segment.segment()` (the item list it fits, and `want2`, the
   option-reading anchor) and `build_choukai_bank.build_sitting()` (the
   pre-audio script-shape assertion and the preamble loop). A 2014-12 sitting
   raises `NotSegmented` today: `item_hint has 12 entries for 問題4, expected 11`.
   **Route A therefore does NOT get the 21 sittings "with no code change"** —
   an import of 2014-12 that faithfully transcribes 12 問題4 items and 3 問題5
   items is refused by the bank builder exactly as an archive-side build would be.
2. **問題5 changed shape in 2020-12 and the slot map is not identity.** Pre-2020
   官方 問題5 is 1番 (single question, spoken options), 2番 (single question,
   spoken options), 3番 (質問1/質問2, options PRINTED —
   `refs/JLPT_N2_NEW/5. N2 12-2014/booklet.md` lines 730-748). The current
   two-item shape is slot 1 = the single-question item, slot 2 = the
   two-question item. So an old 1番 maps to slot 1 unchanged; an old **2番 and
   3番 cannot be placed without cutting off their own 「2番。」/「3番。」 and
   prepending a harvested call**, because an official clip speaks its number and
   the booklet would disagree with the audio.
3. **2020-12 is the free one.** It is the only un-imported sitting already on
   the modern 5/6/5/11/2 shape, so it needs no era map at all. Start there.

### Candidates the 21 would add, per slot

```bash
# same script as above, projected onto the composer's SECTIONS
```

| 大問 | slot | now | +archive | total |
|---|---|---|---|---|
| 問題1 | 1–5 | 10 | +21 | **31** |
| 問題2 | 1–5 | 10 | +21 | **31** |
| 問題2 | 6 | 10 | +16 (5 sittings run 5 items) | **26** |
| 問題3 | 1–4 | 10 | +21 | **31** |
| 問題3 | 5 | 10 | +20 (2012-12 runs 4 items) | **30** |
| 問題4 | 1–11 | 10 | +21 | **31** |
| 問題5 | 1 | 10 | +21 | **31** |
| 問題5 | 2 | 10 | **+0** without a number-call re-cut (+21 with one) | 10 |

Old sittings' 問題4-12番 is simply never drawn (`compose_choukai.SECTIONS` caps
at 11) and `harvest_number_calls.py` has no 「12番。」 — banking it is harmless
and it is dead weight; do not bank it.

---

## 3. `script.md` is OCR, and the bank prints its text to the candidate

### 3.1 Which bank fields reach a learner-visible artifact

Traced through `tools/compose_choukai.py`, `build_interactive.py`,
`build_practice.py`, `build_model_answer.py`:

| bank field (official record) | written into | seen by the candidate? |
|---|---|---|
| `script` | `聴解スクリプト.txt` (`render_script`) | **YES** — `build_interactive.py:789/859` embeds it verbatim in `解答.html`'s result screen, `build_practice.py:498` prints it in `練習.html`, `build_model_answer.py:386/1304` prints it in `模範解答.html` |
| `explanation[問N-M]["options"]` | `聴解.md` option lists (`render_booklet`, 問題1/2 and 問5-2) → `聴解.html`, `解答.html` radio labels | **YES, and they are the answer choices** |
| `explanation[問N-M]` (`why_correct`, `options_analysis`, `points`, `stem`, `script`) | `詳細解説.json` | **YES** — `模範解答.html`, `練習.html` |
| `explanation_vi[…]` | `詳細解説.vi.json` | **YES** — the Vietnamese pane |
| `kaisetsu_cell[…]` | `聴解.md` 【正解・解説】 third column | **YES**, after submit |
| `answers` | the key tables and grading | YES (as a key) |
| `audio.start/end`, `audio.answer_pause` | the MP3 cut | audible only |
| `id`, `sitting`, `source_test`, `source`, `slot`, `figure_dependent`, `needs_number_call` | draw bookkeeping | internal |
| preamble `text`, `opening` | the section instruction in both the script and the booklet | **YES** |

**There is no internal-only text field.** Everything the bank stores as
Japanese is printed somewhere a candidate reads.

### 3.2 How bad the OCR is — measured against ground truth

The seven imported sittings whose script PDF is a stencil scan give a
ground-truth comparison: `refs/…/script.md`'s `[OCR ▼]` fences against the
hand-verified `tests/imported-n2-*/聴解スクリプト.txt` for the same paper.
(Scripts in `/tmp` scratch; reproduce by normalising both to bare
kanji/kana, blocking the OCR fences, and locally aligning each block with
`difflib.SequenceMatcher`.)

| measure | result |
|---|---|
| characters of each OCR block that appear, in order, in the exact text | median **0.973**, mean 0.956, min 0.306 (n=160 blocks) |
| OCR blocks matching the exact text at ≥0.99 | **32 of 160 (20 %)** |
| OCR blocks matching at ≥0.95 (two-sided ratio) | **0 of 160** |
| short substitutions in one sitting's global alignment (2021-07) | **219** over 5460 OCR characters |

A median 97.3 % character rate over a ~250-character item block is **about
seven wrong characters per banked item**, and they land on content words, not
on particles. Quoted verbatim from the extracts:

* `refs/JLPT_N2_NEW/12. N2 7-2021/script.md` vs the verified import:
  「新入生勧誘のための**指宗**」 for 掲示板, 「学生**譲**」 for 学生課,
  「**評高**」 for 許可, 「禁**強軍**」 for 禁煙車, 「**普発考**」 for 再発行.
* `refs/JLPT_N2_NEW/5. N2 12-2014/script.md` p.3: 「お弁当の**試作高**」
  (試作品), 「その線で**普検計**してみてくれる？」 (再検討),
  「肉が食べたい**ってという**声」 (っていう).
* `refs/JLPT_N2_NEW/9. N2 7-2018/script.md` p.2: 「**選業**体験」 (農業),
  「大学が**全確**してる」, 「**確業着**」 ×2 (作業着),
  「**憩像**以上に**浮**を掻く」 (想像/汗), 「**貴靴**」 (長靴),
  「**貧報**買わなきゃ」, 「**診前善**」 (診断書), 「打ち**答**わせ」 (打ち合わせ).
* `refs/JLPT_N2_NEW/1. N2 7-2010/script.md` p.1-2: 「**不動産産**に行く前に」,
  「**軽理**してみた」 (整理), 「この間の**通意**」 (地震),
  「かなり揺れて**稀**かった」 (怖かった), 「4桁の番号で**衝覚か**ください」
  (ご入力), 「富士**缶服**」.

A cross-sitting noise proxy (kanji in the OCR that occur nowhere in the verified
corpus of the ten imports plus all 31 exact `booklet.md`) runs a median of
**6.9 alien kanji per 1000** on the 21 un-imported sittings — a **lower bound**,
since the majority of the substitutions above (指宗, 軽理, 全確) land on common
kanji the proxy cannot see. The 21 are not measurably better than the 7
measurable ones; 2010-07's page-one sample alone carries six.

### 3.3 The defect this class already shipped

`qa/qa-report-20260911_1.md` F5. `2022-12:問題2-1` was banked as
「とても新人とは思えない**技力**だったよ」; 技力 is not a word, the page prints
演技力, and **the item's own printed option 4 reads 「主役の男の子の演技力」**.
It reached `聴解スクリプト.txt`, `詳細解説.json` and two rendered papers with
every gate green. The root cause recorded there is exactly the premise route B
would rest on — "the official half is machine-extracted, therefore safe" — and
`exam-qa-review/SKILL.md` §4 check 6 was rewritten on 2026-09-11 to say the
opposite in so many words: *"the official half is OCR off a SCANNED script PDF,
not a transcription of the audio"*.

**That defect survived a full, hand-checked import.** Route A is not immune to
this class either; it is only better instrumented against it.

### 3.4 The spoken-option order is scrambled in 14 % of blocks

This is the finding that ends route B on its own, and it is worse than a wrong
character because it silently re-keys an item.

`refs/JLPT_N2_NEW/5. N2 12-2014/script.md` 問題3-2番 prints its four spoken
options as:

```
2．気分転換をする方法
1． ゴルフの練習方法
4. 緊張感を持続させる方法
3． 同じミスを繰り返さないための方法
```

The script PDF lays them in two columns and the OCR reads them in visual order.
`key.md` gives 問3-2 → **3**, which is 同じミスを繰り返さないための方法 — correct
only if the DIGIT is read, never the position. Both
`build_textbook_bank.derive_text` and `compose_choukai.spoken_option_tokens`
harvest `^[1-4]、` lines **in file order**, so a naive archive parser would
publish `options = [気分転換, ゴルフ, 緊張感, 同じミス]` and key 3 would point at
緊張感を持続させる方法 — a mis-key, printed in `詳細解説`, with the audio saying
something else.

```bash
python3 - <<'EOF'
import re, unicodedata
from pathlib import Path
OPT = re.compile(r'^\s*([1-4１-４])\s*[.．、。]\s*\S')
tot = bad = 0
for d in sorted(Path('refs/JLPT_N2_NEW').glob('*/')):
    p = d / 'script.md'
    if not p.is_file():
        continue
    run = []
    for l in [unicodedata.normalize('NFKC', x).strip()
              for x in p.read_text(encoding='utf-8').splitlines()] + ['']:
        m = OPT.match(l)
        if m:
            run.append(int(m.group(1)))
        else:
            if len(run) in (3, 4):
                tot += 1
                bad += run != list(range(1, len(run) + 1))
            run = []
print(tot, bad)          # -> 316 44
EOF
```

**44 of 316 spoken-option blocks (13.9 %) are not in ascending digit order**,
concentrated in the older scans (2010-12, 2015-07, 2015-12, 2016-07: 5 each).

### 3.5 Does the alignment method even work on OCR text?

Yes — but only for the numbers, and only after real parser work.
`choukai_segment.segment()` needs `hint_from_script`'s `(spoken chars, lines,
choice lines)` per item, and tolerates `TAIL_FIT_MAX` = 0.30 mean relative error.
A prototype parser over `script.md` (join OCR line-wraps onto the preceding
speaker-labelled line, treat `^[1-4][.．、]` as a choice line) was compared
against the exact hint for all ten imported sittings:

* **characters**: within 2–10 % per item — well inside the fit tolerance;
* **turn counts**: usable for 問題1/2 (off by the one repeated-question line the
  extractor keeps outside the fence);
* **問題3 and 問題4 turn counts are wrong by construction** — the prototype
  reported 1–2 lines where the exact hint has 4 (問題4) and 7 (問題3), because
  the option digits OCR as `1．`/`1.`/`1、` interchangeably. With
  `choice_lines = 0`, `expected_gaps` under-predicts a 問題4 item by
  `GAP_BETWEEN_SPOKEN_RESPONSES × 3` ≈ 6.6 s on a ~25 s item — 26 %, at the
  edge of `TAIL_FIT_MAX`;
* item-boundary detection itself was fragile: the prototype found 4 問題3 items
  in 2021-12 and 2022-12 and 4 問題1 items in 2023-07.

So the **audio offsets are recoverable from OCR** (the hint is a length model,
and OCR preserves length), but only with a hardened, per-section parser that is
tested against the ten sittings whose exact hint is known. **The text is not
recoverable.** That asymmetry is the whole design.

### 3.6 The audio side is fine

```bash
python3 -c "
import sys; sys.path.insert(0,'tools')
from pathlib import Path
from choukai_segment import measure, find_pauses, OPTION_READING, ANSWER_12, ANSWER_8
d = Path('refs/JLPT_N2_NEW/5. N2 12-2014')
mp3 = [p for p in d.iterdir() if p.suffix=='.mp3'][0]
env, lufs = measure(mp3); ps = find_pauses(env, lufs)
print(len(ps), sum(1 for p in ps if OPTION_READING[0]<=p.duration<=OPTION_READING[1]))"
```

| sitting | duration | LUFS | ~20 s | ~12 s | ~8 s |
|---|---|---|---|---|---|
| 2010-07 | 50.2 min | −18.60 | 7 | 13 | 20 |
| 2012-12 | 36.6 min | −18.38 | 6 | 13 | 18 |
| 2014-12 | 41.4 min | −17.91 | 6 | 13 | 19 |
| 2018-07 | 43.1 min | −17.23 | 6 | 15 | 15 |
| 2020-12 | 38.2 min | −17.06 | 6 | 11 | 18 |
| 2025-07 (imported, control) | 42.2 min | −15.55 | 6 | 12 | 17 |

Every old sitting lays the same structural signature the segmenter anchors on.
`refs/…/audio_inspection.md` confirms 20.21–20.28 s option-reading pauses on
2014-12 — official's own band.

---

## 4. The cost of each route, honestly

### Route A — 21 full imports (`external-test-import`)

* **Per sitting**: `init_imported_test.py`, `言語知識・読解.md` (71 items, from
  the exact `booklet.md` — mostly mechanical, plus restored underlining, notes
  and 問題8 permutations), `聴解.md`, `聴解スクリプト.txt` (30 items, every
  fenced line reconciled against a 1-bit stencil page — §3.2's cost, one item at
  a time), a 101-key mechanical diff, then `詳細解説.json` **and**
  `詳細解説.vi.json` (101 entries each, in separate contexts) and
  `make model-answer`.
* **Still needs the code change of §2.** The era shapes refuse `make choukai-bank`
  whatever produced the folder.
* **Unit of work is one whole sitting** — 101 items — and 29 of the 101 are
  what the bank wants. There is no partial credit: `build_sitting()` raises
  `Reconciliation` unless the whole 聴解 half is present and every key and
  explanation resolves.
* **What it buys beyond clips**: 21 more playable past papers, the 読解 and
  文字・語彙 corpora for `goi_profile`/`dokkai_profile`, and the preamble clips.
  That is genuine value this design does not dismiss.
* **Estimate**: `textbook_bank_plan.md` §6.4's "one sitting is a full pipeline
  run" stands. Call it **1.5–2 sessions per sitting, 30–40 sessions for 21**.

### Route B — auto-build from `refs/JLPT_N2_NEW/` with no hand declaration

**Refused.** §3.2 and §3.4 are the refusal: it would publish ~7 wrong characters
per item into `聴解スクリプト.txt`, `詳細解説.json` and `詳細解説.vi.json`, and
mis-key roughly one 問題3/問題4 item in seven. There is no gate in the repo that
reads Japanese; `exam-qa-review` §4 check 6 is a human read, and it is the check
that would have to catch 630 items instead of the 29 a paper draws.

Cheap to build (a parser plus an era map, one session) and it is the one route
whose defects are invisible until a learner reads them. Do not take it.

### Route C — the archive as a third hand-declared source (**recommended**)

The insight is that the archive is **three different sources in one folder**,
and only one of them is bad:

| what | file | trust | cost |
|---|---|---|---|
| the recording | `*.mp3` | exact | free |
| the key | `key.md` | **exact**, colour-parsed and cross-checked 365/365 against the script PDFs' `（正解:N）` | free |
| the printed 問題1/2 and 問5 options | `booklet.md` | **exact** (full text layer on all 31) | free |
| the 問題N instruction | `booklet.md` | exact | free (and not needed — see below) |
| the dialogue | `script.md` | **OCR, ~97 %** | the whole cost |

So route C pays for the dialogue transcript and the two explanation panes, and
gets the key and the option lists for nothing. It reuses the shape
`textbook_items.json` already has, the guards `build_textbook_bank.py` already
applies, and the `window`-resolution path `mondaireishuu` already proved.

**Unit of work is ONE ITEM.** That is the decisive difference: the expansion can
be spent where `make choukai-wear` says it is needed (問題3 and 問題5 first),
one 大問 at a time, exactly as `refs/KanzenMoshi/` was on 2026-09-10.

**Estimate**: ~2.5× a textbook item, because the dialogue is longer than a drill
track and every fenced line needs the `external-test-import` §Step 2.4 ladder.
Against the 19 items 2026-09-10 banked from `KanzenMoshi` in one session, call it
**6–10 archive items per session**. 問題5 slot 1 (21 items, the single biggest
novelty win in the repo) is therefore **2–4 sessions**, not 30.

### Why C beats A

1. **A's extra 72 items per sitting buy no clip.** The bank reads 29.
2. **A is all-or-nothing per sitting; C is per item.** Wear is a per-大問
   problem, so per-item is the granularity the measurement actually asks for.
3. **Neither avoids the code change** (§2), so A's "no code change" advantage
   does not exist.
4. **A is not safer.** The one shipped defect of this class (§3.3) came through
   a completed import.
5. C does not preclude A. A sitting declared item-by-item can be promoted to a
   full import later; the transcript and the explanations are the same work,
   done once.

**What C gives up**: the 21 papers as papers, and the 読解/語彙 corpora. Say so
when recommending it. If the user wants past papers to SIT, route A is the right
route and the clips are a by-product — that is a product decision, not a
measurement.

---

## 5. Does this expansion even fix what is broken today?

Be honest about this, because the framing invites the wrong answer.

```bash
python3 -c "
import json; from collections import Counter
b=json.load(open('logs/choukai_bank.json')); d=json.load(open('logs/choukai_draws.json'))['history']
off=Counter(); tb=Counter()
for r in b['records']:
    if r['kind']!='item': continue
    (tb if r.get('needs_number_call') else off)[r['section'] if r.get('needs_number_call') else (r['section'],r['slot'])]+=1
print(tb, len(d))"
```

| 大問 | textbook slots | pool | projected textbook wear | official cand./slot | projected official wear |
|---|---|---|---|---|---|
| 問題1 | 2 | 15 | 3.60 | 10 | 1.72 |
| 問題2 | 2 | 15 | 3.60 | 10 | 1.90 |
| 問題3 | **3** | 19 | **4.26 — OVER 4.0** | 10 | 1.18 |
| 問題4 | 4 | 36 | 3.00 | 10 | 1.82 |
| 問題5 | 0 | — | — | 10 | **2.80** |

**`make choukai-wear`'s non-zero exit is a TEXTBOOK-pool problem and the archive
does not touch it directly.** It is fixable today by dropping
`TEXTBOOK_SLOTS["問題3"]` from 3 to 2 (2 × 27 ÷ 19 = **2.84**, inside the
ceiling), at the price of 問題3's official wear rising 1.18 → 1.72. That is the
correct immediate repair and it needs no new source.

What the archive buys is different and larger:

* **Novelty.** Official candidates per slot go 10 → 26–31 (§2), so official wear
  falls to **0.39–0.73** per clip. The pool stops being the scarce thing.
* **The official share of every paper.** With 31 candidates per slot,
  `TEXTBOOK_SLOTS` can be cut across the board without any 大問 going thin —
  the mixed pool becomes a seasoning rather than a crutch, and every paper moves
  toward the `20260807_1` control.
* **問題5, which no textbook can reach.** `textbook_bank_plan.md` §6.2 costs the
  問題5 textbook path at "re-introducing Edge-TTS into the composed path" plus
  6+ bankable items, and shelves it. The archive supplies **21 native 問題5
  slot-1 items with their own spoken read-backs and their own 10 s
  質問1 pause**, at no composer surgery whatsoever. 問題5 has the worst
  projected official wear (2.80) and is the only 大問 with no second source.
  **This is where the expansion should start.**

---

## 6. Implementation plan

Ordered so each step is independently shippable and independently gated.

### Step 1 — era-aware slot shapes (code only, no new clips)

*File*: `tools/choukai_segment.py`

* Replace the module-level `EXPECTED_SLOTS` constant with
  `slots_for(sitting) -> dict[str, int]`, driven by a table derived from
  `refs/JLPT_N2_NEW/answer_keys.json` rather than hard-coded (the table in §2 is
  the expected output, not the source of truth). **Keep `EXPECTED_SLOTS` as the
  modern default** so every existing caller keeps working unchanged.
* Give `segment()` an `expected: dict[str,int] | None = None` parameter used for
  the item list, for `want2`, and for the preamble loop; default to
  `EXPECTED_SLOTS`.
* **Fix the two docstrings that assert the false fact** (`choukai_segment.py`
  line 112 comment and `build_choukai_bank.py`'s "Slot-preserving draws"
  paragraph). Cite this file's §2.
* *Test*: `python3 tools/build_choukai_bank.py --check` must still reconcile all
  ten imports to the same 340 records. That is the regression bar.

### Step 2 — `tools/build_archive_bank.py` + `archive_items.json`

*New files*: `tools/build_archive_bank.py`,
`.agents/choukai-audio/references/archive_items.json`.

Model it on `tools/build_textbook_bank.py` — same `Refused` exception, same
`build_records() -> (records, refusals)` signature, so
`build_choukai_bank.main()` appends it the same way it appends the textbook half
(one writer for one file).

Declaration shape, per item:

```jsonc
{
  "id": "archive:2014-12:問題3-2",
  "sitting": "2014-12",
  "folder": "5. N2 12-2014",
  "section": "問題3",
  "slot": 2,                       // from the sitting's own numbering
  "target_slot": 2,                // where the composer may place it
  "window": [1234.5, 1310.2],      // bracket; the span is MEASURED inside it
  "answer": 3,                     // MUST equal key.md; the builder re-checks
  "source_page": "script.md p.7 / booklet.md p.21 (image-verified 2026-xx-xx)",
  "script_lines": ["…"],           // hand-verified, 「N番。」 INCLUDED
  "printed_options": ["…"],        // 問題1/2/問5-2 only, copied from booklet.md
  "explanation": { … }, "explanation_vi": { … }, "kaisetsu_cell": "…"
}
```

Resolution and guards — reuse, do not reimplement:

* audio by `window_span()` (import it from `build_textbook_bank`), which already
  **refuses a window edge that falls inside speech**. Do not add a second
  windowing implementation.
* `TYPE_BANDS` for the body span, `CHAR_RATE_OFFICIAL` for the implied rate
  (these ARE official recordings — `rate_band_for` must return the official band
  for `source == "archive"`, and `BOOKS`-equivalent metadata should carry
  `"official_pacing": True`).
* `EXPECTED_OPTIONS`, the duplicate-option refusal, the answer-range refusal, the
  Vietnamese `options_analysis` length check, `figure_dependent()` — all
  unchanged.
* **New guard, and it is the one this source specifically needs**: the declared
  `answer` must equal `refs/JLPT_N2_NEW/answer_keys.json`'s value for that
  `(sitting, 問題, item)`. It is free and exact, and it makes a mis-typed key
  impossible.
* **New guard #2**: for a 問題1/2 item, every declared `printed_option` must
  appear verbatim in that sitting's `booklet.md`. Free, exact, and it is the
  mechanical form of the 「演技力」 second-witness rule.

Records carry `source: "archive"`, `audio.path` pointing into
`refs/JLPT_N2_NEW/…`, and a `provenance` field (see §7 on why `source` alone is
a trap).

### Step 3 — number call and slot placement

Two sub-cases, and **only take the first one in the initial cut**:

* **`target_slot == slot`** (問題1/2/3/4 everywhere, 問題5-1番): bank the clip
  **with its own 「N番。」**, `needs_number_call: false`, slot-preserving, exactly
  like an imported official record. Nothing new is needed.
* **`target_slot != slot`** (問題5 old 2番 → slot 1, old 3番 → slot 2): the clip
  says the wrong number. Bank it body-only (`needs_number_call: true`,
  `slot: 0`) and let the composer prepend a harvested call. This is a second
  cut per item and a second verification, so **defer it**; it buys 21 extra
  問題5 slot-1 candidates and 21 問題5 slot-2 candidates and it is worth doing,
  after the first cut ships.

### Step 4 — do NOT bank archive preambles

`build_choukai_bank.build_sitting()` emits one preamble clip per section, whose
`text` is lifted from the import's `聴解スクリプト.txt`. The archive has no such
text (all 31 `script.md` begin at 問題1 — the opening and the 問題N instructions
are not printed in the script PDFs at all), and the pre-2020 問題5 preamble has a
different internal structure (one lead-in covering 1番 and 2番, a second before
3番). The bank already holds 50 preambles from 10 sittings, which is ample.
**Archive records are items only.** State it in the builder's docstring so the
next reader does not try.

### Step 5 — composer and policy

*File*: `tools/compose_choukai.py`

* `draw()` already indexes by `needs_number_call`, so a slot-preserving archive
  record lands in the `official` pool with no change. **That is the bug** —
  see §7.1. Add an explicit `provenance` filter so `OFFICIAL_ONLY_TESTS` papers
  draw only `imported` clips.
* `build_audio.source_for()`'s restore hint hard-codes a book→zip map defaulting
  to `Shinkanzen`; add `"archive": "JLPT_N2_NEW"`.
* After the first archive items land, **re-run `make choukai-wear` before
  touching `TEXTBOOK_SLOTS`** and lower the textbook slot counts rather than
  raising anything (`choukai-audio` Part 0: depth buys a slot only at the
  threshold).

### Step 6 — record and cross-reference

* Add §10 to `textbook_bank_plan.md` (or supersede §6.4 by pointing at this
  file) with the five-point result, the item list and every measurement.
* Update `choukai-audio/SKILL.md` Part 0's pool counts and the "Finite novelty"
  bullet, and the `AGENTS.md` §4 table if a `make archive-bank` target is added.
* `refs/JLPT_N2_NEW.zip` is **already on the `refs` release**, so no
  `make upload-files` is needed for the source — but note in Part 0 that
  composing now needs that 1.2 GB folder on disk, which it did not before.

---

## 7. Acceptance checks before an archive clip may enter a paper

Modelled on what `build_textbook_bank.py` already demands of a non-official
source, plus what this source specifically invites. A clip that fails any of
these is `excluded` **with the measurement that refused it**, never admitted by
widening a band.

| # | check | how | refuses |
|---|---|---|---|
| 1 | **key agrees with `answer_keys.json`** | exact lookup by (sitting, 問題, 番) | a mis-typed key — free and absolute |
| 2 | **printed options are verbatim `booklet.md`** (問題1/2/問5-2) | substring match against the sitting's own booklet extract | a hand-typing slip; also the machine half of the 「演技力」 rule |
| 3 | **body span inside `TYPE_BANDS`** | `window_span` + the existing band | a window bracketing the wrong item |
| 4 | **implied rate inside `CHAR_RATE_OFFICIAL`** (0.080–0.360) | `(span − expected_gaps) / spoken chars` | a clip that is the right length but does not say what the transcript says; and a window that swallowed a section instruction |
| 5 | **window edges fall in silence** | `window_span`'s straddle refusal | a cut inside speech |
| 6 | **spoken options are in DIGIT order, not file order** | the declaration stores `1、…` lines re-sorted by their own digit, and the builder asserts the digits read 1..N ascending | §3.4 — 14 % of archive option blocks are visually reordered; this is the new guard this source needs |
| 7 | **no bare-digit option set** | `figure_dependent()` | a picture-legend item that cannot be composed |
| 8 | **the 問題2 option-reading pause is inside the clip and measures 19–21 s** | `find_pauses` inside the declared window | a 問題2 window cut from the pause's end |
| 9 | **every line of `script_lines` is image-verified, and `source_page` says so** | `external-test-import` §Step 2.4 rung 3 — `pdftoppm -r 300` on the decisive lines, rung 1–2 elsewhere | §3.2; this is the expensive check and it is the point of route C |
| 10 | **option/script second-witness** | `check_choukai_option_grounding` (already exists, WARN, ~11 % official baseline) | the 「演技力」 class, on any paper that draws the clip |
| 11 | **loudness inside a declared band** | `choukai_segment.measure`'s LUFS per source file | see §8 — a new cross-source check this expansion requires |
| 12 | **`make choukai-wear` re-read before any `TEXTBOOK_SLOTS` change** | the existing tool | raising a slot on a hope |

Checks 1, 2 and 6 are new and all three are cheap, exact and specific to this
source. Check 9 is the human one and there is no substitute for it.

---

## 8. What could ship wrong

### 8.1 The control paper silently stops being official-only

`check_choukai_source_mix()` computes
`official_only = {t for t, s in by_source.items() if set(s) <= {"official"}}`
and FAILs unless it is exactly `OFFICIAL_ONLY_TESTS`. A slot-preserving archive
record has `needs_number_call: false`, so `draw()` files it in the `official`
index and **`20260807_1` would draw archive clips**. Tag them `source:
"official"` and the mix is unreadable in `logs/choukai_draws.json`; tag them
`source: "archive"` and the control paper's row stops being `<= {"official"}`
and the gate FAILs.

*Repair, decided up front*: keep `source: "official"` (they are the same JEES
recordings) and add `provenance: "imported" | "archive"`; teach `draw()` to
restrict `OFFICIAL_ONLY_TESTS` papers to `provenance == "imported"`, and
`compose_choukai`'s `sources` counter to record provenance too. The gate line
then keeps meaning what it says.

### 8.2 A mis-keyed 問題3/問題4 item from a reordered option block

§3.4. Caught by acceptance check 6 **only if the declaration stores the digit**.
A declaration that pastes the OCR block as-is passes every duration and rate
guard, ships a wrong option list into `詳細解説.json` and `模範解答.html`, and
hands the candidate a key that does not match the audio. This is the single
highest-severity thing route B or a careless route C can do.

*Gate*: check 6, plus `exam-qa-review` §4 check 6's read of all 29 drawn clips —
a human listening to the clip against the printed list is the last line.

### 8.3 OCR text reaching `聴解スクリプト.txt` and both `詳細解説` panes

§3.1 and §3.3. 「技力」 shipped this way. There is **no automated gate for it**:
the bank guards duration and char rate, the `check_choukai_*` family compares
the script against the composed MP3's segmentation, and none of them reads
Japanese.

*Gate*: acceptance check 9 (image verification at declaration time) is the
primary control; check 10 (`check_choukai_option_grounding`, WARN) is the only
machine detector and it only reaches 問題1/2; `exam-qa-review` §4 check 6 is the
backstop. **Do not resolve a suspected script defect by re-running the
extractor** — it reproduces the page faithfully, including the page's own typos.

### 8.4 An audible level and bandwidth step mid-paper

`build_audio` runs ONE `loudnorm` pass over the concatenated file, so relative
level differences between source clips survive.

```bash
for d in refs/JLPT_N2_NEW/*/; do
  grep -m1 '| mean volume |' "$d/audio_inspection.md"; done
```

| corpus | mean-volume spread | sample rates | bit rates |
|---|---|---|---|
| the 10 imported (today) | −17.4 … −21.7 dB (**4.3 dB**) | 44.1/48 kHz | 116–192 kb/s |
| all 31 (after expansion) | −15.3 (2015-07) … −23.3 (2019-12) (**8.0 dB**) | **32 kHz on 2010-12 and 2016-07**, else 44.1/48 | **65–82 kb/s on 14 of the 21** |

A 2019-12 clip beside a 2015-07 clip is an 8 dB step a listener hears as the
recording changing, and a 32 kHz/65 kb/s clip beside a 192 kb/s one is an audible
bandwidth change. Neither is a fidelity defect in the item; both break the
illusion of one sitting.

*Gate*: acceptance check 11 — measure integrated LUFS per source file with
`choukai_segment.measure` and either (a) refuse a sitting more than ~3 dB from
the pool median, or (b) apply a per-clip gain at cut time so every clip enters
the concat at the same integrated level. **(b) is the better engineering and is
a composer change, so it is not in the first cut** — do (a) first, and record
the excluded sittings in §9.

### 8.5 Era drift: 15-year-old items in a 2026 paper

The pacing table is unmoved in 15 years (`|r| ≤ 0.22` against sitting year —
`choukai-audio` Part 3), so the RHYTHM is safe. Content is not measured here:
a 2010 item can name a fax machine, a フィルムカメラ or a ガラケー. Nothing in the
repo checks topical currency.

*Gate*: none exists. Add it to the declaration review (`source_page` note) and
to `exam-qa-review` §4 check 6's read, and say so in Part 0. Consider a
`period_marked: true` flag for items to be excluded from the draw, following
`figure_dependent`'s precedent — **kept and flagged, never dropped**, so the
exclusion stays countable.

### 8.6 A shape assumption re-hard-coded somewhere else

`EXPECTED_SLOTS` is read in four places (§2). A fifth reader added later against
the modern shape reintroduces the bug silently.

*Gate*: after step 1, `make check` should assert that
`choukai_segment.slots_for()` reproduces `answer_keys.json`'s measured shape for
all 31 sittings — the table in §2 must be derived, never retyped
(`AGENTS.md` §4, "a measured number has one owner, and it is a script").

---

## 9. Sittings and items that must be EXCLUDED

Each with the measurement that disqualifies it. None of these is a judgment.

| what | measurement | verdict |
|---|---|---|
| **問題4-12番 of the 13 sittings that run 12 items** (2010-07, 2010-12, 2012-12, 2013-07, 2013-12 … 2017-12) | `compose_choukai.SECTIONS["問題4"] = 11`, and `logs/choukai_number_calls.json` harvests 1番–11番 only | **never bank** — no slot and no number call |
| **問題3-5番 of 2012-12** | that sitting runs 4 問題3 items (`answer_keys.json`) | slot 5 simply has no candidate there; 問題3 slot 5 gets 20 of 21 |
| **問題2-6番 of 2013-07, 2018-07, 2018-12, 2019-07, 2019-12** | those five run 5 問題2 items | 問題2 slot 6 gets 16 of 21 |
| **問題5 old 2番 and 3番, in the first cut** | their clips speak 「2番。」/「3番。」 and the composed booklet would number them 1番/2番 | **defer to step 3's second sub-case**, never place them with their own call |
| **2019-12 (−23.3 dB) and 2019-07 (−22.9 dB)** | 8.0 dB and 7.6 dB below 2015-07's −15.3 dB; the pool's own median is ≈ −19.9 dB | **hold until §8.4's per-clip gain exists**; they are the two extreme ends of the level spread |
| **2015-07 (−15.3 dB)** | the loud end of the same spread | same hold |
| **2010-12 and 2016-07** | MP3 sample rate **32 000 Hz** (`audio_inspection.md`), against 44.1/48 kHz everywhere else — an audible bandwidth step after the composer's 48 kHz resample | **hold**; admit only if a listen says the step is inaudible, and record that listen |
| **any item whose printed options are bare digits** | `figure_dependent()` | auto-excluded by the composer, kept in the bank so the exclusion stays countable (2 of 290 official records today) |
| **any item whose declared spoken options are not in ascending digit order after re-sorting** | acceptance check 6 | refused; re-read the page |

The two 32 kHz sittings and the three loudness outliers are **six of the 21**;
the remaining 15 are clean on every mechanical measure and are where the work
should go.

---

## 10. Where to start, concretely

1. **Step 1** (era-aware shapes, code only). Regression bar: `--check` still
   reconciles the ten imports to 340 records.
2. **2020-12** — the only un-imported sitting already on the modern shape, so it
   exercises steps 2 and 3 with zero era mapping. 29 declarable items.
3. **問題5 slot 1** across the 15 clean sittings. 15 items, the 大問 with the
   worst official wear (2.80) and no second source, and the one
   `textbook_bank_plan.md` §6.2 costs at "re-introduce Edge-TTS" from the
   textbook side. This is the highest value per hour in the whole expansion.
4. **問題3**, then **問題2** — the two 大問 whose textbook wear is at or over the
   ceiling, so each archive item there directly buys back an official slot.
5. Re-run `make choukai-wear`, LOWER `TEXTBOOK_SLOTS`, and re-read every line.
