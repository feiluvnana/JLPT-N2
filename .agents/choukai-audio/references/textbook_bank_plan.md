# Mixed-pool 聴解 — the slot-free half of the clip bank

Status: **built and shipping for 問題1, 問題2, 問題3 and 問題4** (2026-09-10).
問題5 is the only 大問 still official-only, for the source reasons in §6.

Four sources. Shin Kanzen and Soumatome are the textbook half (§2, §3);
『新しい「日本語能力試験」問題例集』(2009) is a third, added 2026-09-09 — free
official JEES audio from jlpt.jp, one item per 大問, banked the same way (§7);
**『完全模試 N2』(Jリサーチ) is a fourth**, added 2026-09-10 — three mock papers
pressed to exam timing, and the first source that clears all five acceptance
checks on its own (§8).
Three more books arrived 2026-09-10 and were run through the five-point check
(§9): 耳から覚える is **the second source in the repo that lays a real 20 s
option-reading pause**, ドリル&ドリル lays only 15.2 s, and 試験に出る lays none.
**77 items are banked and 17 are `excluded`** with the measurement that refused
each: 問題1 ×15, 問題2 ×10, 問題3 ×16, 問題4 ×36, by source soumatome 37,
shinkanzen 21, kanzenmoshi 11, mondaireishuu 4, mimikara 4.

Both books have now been read end to end — every page of both 別冊 and every
one of Soumatome's 116 CD tracks and Shin Kanzen's 163 measured.

The pool is **not** exhausted, and it is worth being exact about why it stopped
where it did. Roughly six more Soumatome 課題理解 items and two or three more
概要理解 items are readable and of the right type (cd1/54, cd2/12, cd2/15,
cd2/19, cd2/21, cd2/22, cd2/23 for 問題1; cd1/32, cd2/40 for 問題3). None of
them would change anything, because **depth only matters at the step where it
buys another slot**, and the next step in each 大問 is still out of reach even
after the 問題例集 items: at 3 slots, 問題1 and 問題3 each need 18 items to stay
under the wear ceiling (they hold 15 and 14), 問題2 needs 12 for even a second
slot and holds 10 (§6.1), and 問題4 needs 24 for a fourth and holds 23 — which
would project **exactly 4.00** against a 4.0 ceiling, over it on the next paper
composed. At 8 slots the four pools sit at 2.30–3.29 uses per clip, down from
2.56–3.54 before the 問題例集 items. Transcribing more without a slot to spend
it on buys nothing a reader would hear. §6 lists what is genuinely blocked, and
every entry carries a number.

What is true on disk now:

- **exactly ONE paper is composed from official recordings only** —
  `20260807_1`, named in `compose_choukai.OFFICIAL_ONLY_TESTS`. It is the
  control: the reference a listener can compare the mixed papers against;
- **every other paper draws from a MIXED pool** — the ten imported official
  sittings plus **62 slot-free items** (問題1 ×15, 問題2 ×10, 問題3 ×14,
  問題4 ×23), with `TEXTBOOK_SLOTS = {問題1: 2, 問題2: 1, 問題3: 2, 問題4: 3}`
  taking **8 of a paper's 29 slots** from the slot-free side. Each paper's mix is
  recorded in `logs/choukai_draws.json` under `sources`;
- **the slot counts are a measurement, not a preference.**
  `tools/choukai_wear.py` (`make choukai-wear`) divides `slots × mixed papers`
  by pool depth and exits non-zero above `WEAR_CEILING` = 4.0 uses per clip
  across the suite. At the current depths: 問題1 3.07, 問題2 2.30, 問題3 3.29,
  問題4 3.00, against 1.5–2.4 for an official clip. It is also what showed the
  pre-2026-09-09 numbers were already over — 問題3 projected **5.75** and 問題4
  **4.18** — which is why 問題4 went from 4 slots to 3 while three other 大問
  went up. **The slot counts did not move when the 問題例集 items landed**, and
  that is the tool being used as intended rather than a disappointment: four
  more clips buy depth (every 大問's wear fell) and no 大問 reached its next
  threshold, so nothing was raised on a hope.

Everything below was measured, not assumed. Where something is still unknown it
says so.

---

## 1. The blocker: textbook clips carry no 「N番。」 — solved by harvesting one

An official item's audio opens with the announcer saying 「3番。」 and the bank
keeps official items in their original slot for exactly that reason
(`choukai-audio` Part 0). Textbook tracks have no number call at all, so a
textbook clip dropped into slot 3 would leave the examinee with no idea which
item is playing.

**Measured, and this is the finding that makes the mixed pool work:** every
official item has a **clean, long pause right after its number call** — median
0.90 s of speech then a **2.68 s** pause. Over the 290 banked official items,
163 expose it at a 0.15 s detection floor with the acceptance bands
`harvest_number_calls.py` applies (0.6–1.2 s of speech, ≥1.2 s pause); a looser
first pass counted 188. The ones that do not are dominated by each section's
slot-1 item, whose clip start is snapped by the preamble logic rather than by an
answer pause.

Availability per number, counting only clean candidates:

| 番 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| candidates | 4 | 26 | 28 | 28 | 28 | 14 | 7 | 7 | 7 | 7 | 7 |

All eleven are harvestable, and better than that: **three sittings cover 1–11 on
their own** (2022-12, 2023-07, 2025-07), because numbers 7–11 exist only in
問題4 and those sittings expose all five cleanly. `harvest_number_calls.py`
prefers a single sitting, so a composed paper's eleven prepended calls are
**one announcer** — it picked `imported-n2-2022-12`, all eleven spans 1.02–1.04 s
of contiguous speech with no internal silence above 0.12 s.

So:

- official items stay exactly as they are — slot-preserved, carrying their own
  call, no re-cut, no re-verification of phase 1;
- textbook items are banked BODY-ONLY and the composer prepends the harvested
  「N番。」 plus `AFTER_NUMBER_CALL` = 2.7 s, the measured median above. Having no
  baked-in number, they are slot-free and fill any position.

Do **not** re-cut the official bank to split every number call. It is
unnecessary and most of 問題1/2/3/5's slot-1 items have no clean cut point.

**Verified on a composed paper** (`20260810_1`, 問題4-3番, a Soumatome clip):
0.96 s of speech, 2.72 s pause, then the body — the same shape an official item
has natively.

---

## 2. Soumatome — the better-documented of the two sources

`refs/Soumatome/nihongo-soumatome-n2-choukai-kaitou-script.pdf` (54 pp, 55 MB).
No text layer, but a clean scan that reads reliably page by page, and under the
100 MB read cap so it opens directly with the Read tool's `pages` parameter.

Every item is a table row carrying, in one place: a **「こたえ」 column** (the
answer key), the **full script**, a **CD track icon** (`cd1/25`, `cd2/4`), and —
for 概要理解, ポイント理解 and 統合理解 — **the printed options as well**.
課題理解's options are the exception: they live only in the main 問題冊子.

### Track mapping

`cd1/N` → `refs/Soumatome/Nihongo Sou Matome N2 - Choukai-CD/日本語総まとめＮ2-ＣＤ1/NN.mp3`
(64 tracks), `cd2/N` → `…/日本語総まとめＮ2-ＣＤ2/NN.mp3` (52 tracks).

The mapping was verified against durations across five item types (課題理解
71–74 s, ポイント理解 92 s, 概要理解 110 s, 統合理解 112–145 s, 即時応答 25–34 s),
and that agreement is what makes it trustworthy. `build_textbook_bank.py` now
enforces the same idea per item, so a mis-read track number is refused rather
than banked (§5).

### Track anatomy — what has to be cut off each end

Measured across cd1/39–43 and cd2/43–49, and identical in every one:

```
~0.5 s silence │ ~0.2 s marker blip │ ~1.5 s │ THE ITEM │ 5.1–5.2 s │ ~0.8 s tone │ ~1.0 s
```

The trailing 0.8 s is a **669 Hz tone** — peak frequency 669–670 Hz on all five
tracks checked, high |correlation| between them. It is the book's end-of-item
marker, not speech. The 5.2 s before it is the book's own answer pause, which
the composer discards and replaces with the pacing table's value.

### The first track of a section run is NOT only the item

`cd1/39` (問題I 1番) and `cd2/43` (問題IV 1番) both measure 6–9 s longer than
their siblings — 24.9 s and 29.5 s against 14.6–18.3 s — and their implied
speech rate comes out at 0.36 s/char against the siblings' 0.13–0.17. Two
tracks, both their section's **1番**: the section instruction is bound into the
first track. Both are listed under `excluded` in
`.agents/choukai-audio/references/textbook_items.json` with the measurement, and
both were found by the CHAR_RATE guard rather than by reading — which is the
guard working as designed.

**Two more instances turned up in 2026-09-09's sweep, so this is a rule.**
`cd2/34` (第5章 問題II 1番) lays its 20.3 s option pause at **31 s** into the
track where every other 問題2 track lays it at 8–14 s, and comes out at
0.26 s/char; `cd2/39` (第5章 問題III 1番) comes out at 0.225 s/char, the ~15 s
its transcript cannot explain being 問題III's own instruction. Four instances,
all of them a section's 1番: **expect the FIRST track of any Soumatome section
run to be refused, and read the refusal as the guard working.**

### The 20 s option-reading pause is the gate on 問題2, and it identifies the type

A 問題2 item's option-reading pause sits INSIDE the clip and the composer never
re-times it, so it has to be measured per track before anything is banked.
Sweeping every Soumatome track for one found exactly **15**: cd1/29, cd1/30,
cd1/46, cd1/47, cd2/4, cd2/5, cd2/6, cd2/25, cd2/26, cd2/27, cd2/34, cd2/35,
cd2/36, cd2/37, cd2/38 — all at **20.1–20.3 s**, against official's 20.22 s
[20.19–20.81]. Nine are banked and six are `excluded` with their numbers.

That measurement also settled a mis-identification. 第5章 問題III (cd2/39–42)
had been taken for the ポイント理解 set; it lays only a **2.6 s** gap, so it is
概要理解, and the real 問題2 set is 問題II — cd2/34–38. Reading the 問題冊子 page
confirms it from the other side: 問題III's instruction is 「話の前に質問はありま
せん。まず話を聞いてください。それから質問と選択肢を聞いて」 and the page prints
no options at all, only the ① ② ③ ④ bubbles, exactly like this repo's 問題3.

---

## 3. Shin Kanzen — usable only via the book, never via the extract

**`refs/Shinkanzen/choukai_script.md` is unusable as a transcript.** Its OCR
renders 男 as 第/勤/顎/舅, 女 as 袋/愛/髪, 質問 as 資簡/資間, and mangles the option
digits. It remains fine for what `AGENTS.md` §3 says it is — corroborating
register and family — and must never be used for a key or a quoted line.

The **PDF itself is clean typeset**. `Shin_Kanzen_Masuta_N2-Choukai.pdf` is
193 MB over 161 pages, above the read cap, so slice it with pypdf first. The
別冊「解答とスクリプト」 begins at PDF p.116 and the **模擬試験 runs PDF pp.150–161**
(別冊 pp.35–46), printing 「答え N」 and a CD track icon per item.

### Track mapping — verified two ways

Read off the book and independently confirmed by CD2 durations:

| CD2 tracks | duration shape | section |
|---|---|---|
| 46–50 | 61.8–94.5 s | 問題1 ×5 |
| 52–57 | 87.0–102.6 s | 問題2 ×6 |
| 59–63 | 74.3–94.5 s | 問題3 ×5 |
| 65–76 | 23.4–29.0 s | 問題4 ×12 (no 例) |
| 78–80 | 119.2–171.6 s | 問題5 |

Tracks 45, 51, 58, 64, 77 are the short section instructions between them.

### Track anatomy — a spoken track id, not a number call

Every ITEM track opens with two short spoken runs before the item:

```
0.24 s │ 0.88–0.90 s │ 1.7 s │ 0.30–0.72 s │ 1.1–1.2 s │ THE ITEM │ trailing pause to EOF
```

The first run is **constant at 0.88–0.90 s across every item track** — 問題1
through 問題5, 1番 through 12番 — so it is not the item's own number. The second
run tracks the NUMBER: 0.38 s for 2番, 0.44 s for 10番, **0.72 s for both 11番 and
12番**, exactly the mora counts of 「に」/「じゅう」/「じゅういち」/「じゅうに」. It is a
track id, and both runs are dropped. (The instruction tracks differ — their
first run measures 1.18–1.20 s — which is a second, independent confirmation
that the 0.90 s run is keyed to track TYPE and not to the item.)

There is no end tone; the file simply ends after the book's answer pause.

### The practice chapters are drills, not items — with four exceptions

`実力養成編` I–VI (CD1 all, CD2 1–44) is mostly two-option a/b discrimination
drills and fill-in-the-blank exercises whose 答え is free text
(「本棚を買う、コーヒーを買う」), not one of four printed options. Only each
chapter's **確認問題** is exam-format. What that yields:

- **II 即時応答 確認問題** — four items, all inside ONE track (CD1/25). Not
  banked; see §6.3 for the measurement that refused the split.
- **III 課題理解 確認問題** — three items, one per track (CD1/44–46). cd1/45 and
  cd1/46 are banked; cd1/44 is a picture-legend item and is `excluded`.
- **IV ポイント理解 確認問題** — CD1/67–69, unusable for the pause reason below.
- **V/VI 概要理解・統合理解 確認問題** — not read: 問題3's pool is already at 13
  and 問題5 is blocked on §6.2 regardless, so neither would change a slot count.

### No Shin Kanzen track lays an option-reading pause, anywhere in the book

**Measured over all 163 tracks on both CDs**, sweeping for any internal pause of
8 s or more. The longest option-reading pause in the entire book is **10.1 s**:

| where | pause |
|---|---|
| 模擬試験 問題2 (CD2 52–57), all six | 10.1 s |
| IV ポイント理解 確認問題 (CD1 67–69) | 10.0–10.1 s |
| IV ポイント理解 練習 (CD1 57–65) | 8.0–8.1 s |
| official | **20.22 s [20.19–20.81]** |

So the caveat this file used to carry about one track (Track52) is a property of
the recordings, not a quirk of the mock paper, and **Shin Kanzen contributes no
問題2 item at all**. The book itself states the exam's figure — 問題用紙 p.47:
「実際の試験では、質問の後、話が始まるまで20秒ぐらい時間があります」 — so its own
recordings are abridged relative to what it documents. Soumatome lays the full
20.1–20.3 s and covers 問題2 on its own.

### Keys

All read off the page, never from the OCR extract:

- 問題1 = 3, 2, 2, **1**, 3 — 1番/2番 別冊 p.35, 3番/4番 p.36, 5番 p.37, all
  re-read 2026-09-09. **Two corrections to this file's earlier revision**: 3番
  was recorded as unread and is 2; 4番 was recorded as 2 and is **1**, which is
  also what its script supports — the woman corrects 「フロントに荷物預けて」 to
  「駅で預けたら？」 and the man answers 「じゃ、そうしよう」, so the answer is
  駅で荷物を預けて、バスに乗る. (3番 is moot in either case: it and 1番 are
  picture-legend items, §4.)
- 問題2 = 4, 3, 2, 2, 3, 4 — 1番 別冊 p.37, 2番/3番 p.38, 4番–6番 p.39, all read
  2026-09-09. The 1番–3番 row that was carried over unverified from an earlier
  revision (4, 3, 2) is now **confirmed**. None of the six is bankable — the
  pause reason above.
- 問題3 = 4, 4, 4, 2, 1
- 問題4 = 3, 3, 3, 2, 1, 3, 2, 3, 2, 1, 1, 3
- 問題5 1番 = 3; 2番 質問1 = 1, 質問2 = 2

`textbook_items.json` carries the ones that are banked, each with the page it
came from in `source_page`.

**問題3 2番 (B60) is deliberately NOT banked.** The book files it under 概要理解,
but it is a two-speaker dialogue asking 「先生はどうして生徒に声をかけましたか」 —
a ポイント理解 question in a 概要理解 slot. `jlpt-exam-structure` says 問題3 is a
monologue for gist, so it would ship an off-type item into 問題3.

---

## 4. What each section cost, and what it bought

| section | options are | what it needed | banked |
|---|---|---|---|
| 問題4 即時応答 | spoken | script + key only | **34 items** (Soumatome 10, Shin Kanzen 12, 完全模試 11, 問題例集 1) |
| 問題3 概要理解 | spoken by BOTH books (and printed in Soumatome's answer booklet too) | script + key + option text | **14 items** (Shin Kanzen 4, Soumatome 9, 問題例集 1) |
| 問題1 課題理解 | printed | script PDF **+ the main 問題冊子** for the option lists | **15 items** (Soumatome 9, Shin Kanzen 5, 問題例集 1) |
| 問題2 ポイント理解 | printed | same, **plus a measured 20 s option-reading pause inside the clip** | **10 items** (Soumatome 9, 問題例集 1 — see §3) |
| 問題5 統合理解 | Shin Kanzen PRINTS 1番's four choices instead of speaking them | see §6 | 0 |

問題3 and 問題4 were the cheap two and were done first: they are 16 of a
paper's 29 slots and the two 大問 whose options the audio speaks, so nothing
about them needed a page of the 問題冊子.

問題1 and 問題2 cost a 問題冊子 page per item and, for 問題2, one measurement per
track. Two extra classes of exclusion turned up there and only there:

- **picture-legend items.** `render_booklet` prints a flat 1–4 list, so an item
  whose options are letter combinations over illustrations (`1 ア イ ウ エ`) or
  which is answerable only against a printed form is unusable however good the
  audio is. Four items went out this way: shinkanzen 模擬試験 問題1's 1番 and
  3番, shinkanzen cd1/44, soumatome cd1/59.
- **items short of the type.** `TYPE_BANDS` is deliberately wide, so it is not
  the whole test: soumatome cd1/48 clears its 33 s floor at 38.0 s but its talk
  is ~105 spoken characters against `check_consistency.P3_TALK_FLOOR` = 175 and
  an official 概要理解 range of 158–397.

## 5. What exists now

| File | Owns |
|---|---|
| `tools/harvest_number_calls.py` | `logs/choukai_number_calls.json` — one clean 「N番。」 span per number 1–11, from one sitting. `make number-calls [CHECK=1]` |
| `.agents/choukai-audio/references/textbook_items.json` | The hand transcriptions: script lines, key, page, and both explanation panes. Also an `excluded` list with the measurement that refused each entry |
| `tools/build_textbook_bank.py` | Resolving each item to audio — a `(cd, track)` for a textbook pressing, a `window` into one shared file for 問題例集 (§7) — measuring the body span, and REFUSING an item that fails a guard. `make textbook-bank` reports; it never writes |
| `tools/build_choukai_bank.py` | Still the single writer of `logs/choukai_bank.json`, now `BANK_VERSION = 2` with both halves. `make choukai-bank` |
| `tools/compose_choukai.py` | The source policy (`OFFICIAL_ONLY_TESTS`, `TEXTBOOK_SLOTS`), the number-call prepend, and `resolve()` — the one place a slot-free textbook record becomes a `問N-M`-keyed item |
| `tools/choukai_wear.py` | Measured and projected wear per 大問 and per source — the number `TEXTBOOK_SLOTS` is set from, and it exits non-zero above `WEAR_CEILING`. `make choukai-wear` |

### Bank schema v2

Every record carries `source` (`official` | `soumatome` | `shinkanzen`). Official
records also carry `needs_number_call: false` and keep their `slot`; textbook
records carry `needs_number_call: true`, `slot: 0`, an `audio.path` into `refs/`
instead of a `source_test`, `script_lines` (body-only, no 「N番。」), a single
`answer`, and unkeyed `explanation_payload` / `explanation_vi_payload` /
`kaisetsu_cell_text` — unkeyed because the `問N-M` id is not known until the draw
places the clip.

### The two guards, and why they are the important part

A wrong CD track number is the failure mode this whole path invites: the data
file is hand-typed off a scan, and a track that is off by one still yields
plausible audio. `build_textbook_bank.py` refuses an item unless

1. its measured body span sits inside its 大問's `TYPE_BANDS`, and
2. the span the transcript implies matches the span measured — expressed as an
   implied speech rate inside its source's rate band: `CHAR_RATE`
   (0.060–0.200 s/char) for a textbook pressing, `CHAR_RATE_OFFICIAL`
   (0.080–0.360) for a clip cut from an official recording. **One band could not
   do both**, and the measurement that says so is in §7.

Both are **type-separation bands, not calibration figures** — the calibrated
numbers live in `SKILL.md`'s pacing table. The second guard is the one that
matters: it caught both anomalous tracks in §2, neither of which the duration
band alone would have rejected. A refusal fails `make choukai-bank`; the repair
is to fix the declaration or move the item to `excluded` **with the measurement
that justifies it**.

Admitted items measure 0.111–0.191 s/char and the refusals sit at 0.202, 0.224,
0.225, 0.26 and 0.36 — the ceiling has real work to do and the nearest admitted
item is 0.009 below it.

### The band edges are populated on BOTH sides, which is the healthy reading

`band_headroom()` names any admitted item within 10% of an edge, and
`check_choukai_textbook_bands` WARNs on the list. At 58 items it names seven:
soumatome cd1/45 (47.7 s) and cd1/60 (44.8 s) near 問題1's 40 s floor,
cd1/47 (65.4 s) and cd2/5 (66.7 s) near 問題2's 60 s floor, and cd2/32 (0.190),
cd1/30 (0.189) and shinkanzen cd2/63 (0.191) near CHAR_RATE's 0.200 ceiling.

**That WARN is not a signal to widen anything, and here is the test that says
so:** every edge it names has admitted items just inside it AND refused items
just outside it — 54.2 s and 55.0 s below 問題2's floor, 0.202/0.224/0.225/0.26
above the rate ceiling. A band with traffic on both sides is separating classes,
which is its whole job. The WARN would be worth acting on in the other case: an
edge with admitted items pressed against it and nothing ever refused past it,
which means the edge is about to reject a correct declaration for no reason.
Re-read the list that way rather than by counting entries.

| 大問 | floor | admitted min | admitted max | ceiling |
|---|---|---|---|---|
| 問題1 | 40 | 44.8 | 84.4 | 140 |
| 問題2 | 60 | 65.4 | 101.2 | 175 |
| 問題3 | 33 | 51.0 | 96.8 | 135 |
| 問題4 | 11 | 14.6 | 21.6 | 40 |

---

## 6. What remains, and the exact blocker for each

Both books are read. Nothing below is waiting on someone to open a page — each
entry is waiting on a measurement, an ear, or a source outside these two books.

### 6.1 問題2 cannot grow past 10, and Shin Kanzen cannot help

Soumatome's 15 tracks with a 20 s option-reading pause are fully mined: 9
banked, 6 `excluded` with numbers (cd2/6 at 54.2 s and cd2/26 at 55.0 s under
問題2's 60 s floor and ~18 s under the shortest official ポイント理解 item;
cd2/4 at 0.224 s/char and cd2/25 at 0.202 s/char against a 0.200 ceiling;
cd2/34 with its section instruction bound in; cd2/27 on a source disagreement
between 別冊 p.42's footnote and 問題冊子 p.62's printed option list). Shin
Kanzen adds nothing: **not one of its 163 tracks lays more than 10.1 s** (§3).
The 問題例集 contributes exactly one (§7), which lays 20.19 s at 11.9 s into the
clip. So the pool is 10 against the 12 a second slot needs, and 問題2 stays at
1 slot per paper (2.30 uses per clip, down from 2.56).

### 6.2 問題5 — measured in detail 2026-09-09, and there is a path

**What the books do and do not speak.** Measured on soumatome cd2/52 (別冊 p.54,
質問1=3, 質問2=1, a genuine two-question 2番, body 127.7 s):

- the **two 質問 questions ARE spoken** — 「質問1」+question at 115.1–121.0 s,
  「質問2」+question at 124.3–130.0 s;
- the **four options are NOT spoken at all.** The body ends at 130.0 s, right
  after 質問2's question; the book prints the options in the 問題冊子 instead;
- the gap between the two questions is **3.28 s**, where official lays
  `GAP_AFTER_SHITSUMON1` = **10 s** [7.8–12.4].

Both of this section's blockers therefore reduce to the same missing piece: the
option read-back. Official reads the four choices after 質問1, leaves 10 s, then
reads them again after 質問2, and neither book records any of that.

**One item now exists that speaks its options, and it is still not enough.**
`mondaireishuu:問5-1` (§7) is the only 問題5 item in any of the three sources
whose four choices are SPOKEN, which is exactly the piece both books are missing.
It is nevertheless in `excluded`: measured body span **86.2 s** against 問題5's
105–250 s band, because it is the OLD 統合理解 shape — one 家族三人 discussion,
ONE question, the choices read once — where a current 問題5 slot runs
138.7–226.7 s in the official bank. It is evidence that the read-back problem is
soluble from a source outside the two books, not an item.

**The path, and it is one piece of work rather than two.** If the composer
supplies the read-backs itself — cut the clip at the end of 質問1's question,
lay four synthesized choice lines with `GAP_BETWEEN_SPOKEN_CHOICES`, lay
`GAP_AFTER_SHITSUMON1`, then the book's own 質問2 question, then the four lines
again — then the 10 s pause is laid by construction and the printed-options
blocker is gone with it. What it costs:

- **re-introducing Edge-TTS into the composed path**, which Part 0 retired on
  2026-09-08. The precedent for splicing is the harvested 「N番。」, but that is
  a REAL official announcer; this would put a synthetic voice inside a real
  item, and Part 3's own rule is one engine end to end because mixed voices
  break every 「男の人は」 question. It is an ear-only judgment and no gate hears
  it — someone has to listen and decide it is acceptable;
- **pool depth, which is the harder constraint.** 問題5 has 2 slots, so one
  textbook slot needs **6+ bankable items** to stay under the 4.0 ceiling
  (1 slot × 23 papers ÷ 6 = 3.83). Candidates: soumatome cd1/38, cd1/50,
  cd1/51, cd2/50, cd2/51, cd2/52 plus Shin Kanzen 模擬試験 CD2 78–80 and
  chapter VI. Enough exists, but every one needs a transcript, a key off the
  page, printed options off the 問題冊子, both explanation panes, and
  verification on the RENDERED MP3;
- **`check_mondai5_prints_nothing()` and the 問題5 house rule.** This repo
  prints nothing under 問題5 by design (`jlpt-exam-structure` owns why), so the
  synthesized read-back is what keeps that rule intact — printing the options
  instead would be the other design, and it is a spec change, not a composer
  change.

Not attempted in 2026-09-09's session: it is a stage of its own, and shipping
it half-done would put a clip with no option read-back into a live paper.

### 6.3 One bundled 即時応答 track, and it needs an ear

Shin Kanzen CD1/25 holds all four items of 実力養成編II's 確認問題 (keys 3, 3,
1, 2 off 別冊 p.7). It is the last unmined 即時応答 material in either book —
Soumatome's two sets and Shin Kanzen's 模擬試験 12 are all banked, and every
other 練習 in chapter II is a two-option drill.

A splitter was written for it and **refused it**, correctly. The body carries
**four** pauses of 2.5 s+ (3.20 s @34.9, 3.08 s @61.2, 3.30 s @84.8, 2.96 s
@107.6) where three would split it into four, and two interleaved series run
through it that no measurement here explains: 0.16 s blips each preceded by
exactly 2.28 s (@22.9, @43.6, @71.1), and 0.90 s runs each preceded by ~3.1 s
(@34.9, @61.2, @84.8, @107.6 — the last with only 1.6 s of file after it, and
0.90 s is also the length of the fixed Shin Kanzen track-id word). Finishing it
needs someone to LISTEN to the track and say where the four items start; a
wrong boundary ships a clip that begins mid-sentence into every paper that
draws it and no gate hears anything. The splitter was deleted rather than left
in the tree unused; the measurement is in `textbook_items.json`'s `excluded`.

**The fourth 問題4 slot is no longer waiting on this track** — `refs/KanzenMoshi/`
supplied 11 items on 2026-09-10 and the slot went back to 4 at 2.82 projected
uses (§8). Splitting CD1/25 is still worth doing: at 38 items a **fifth** slot
projects 3.16, inside the ceiling.

### 6.4 The remaining source of novelty is outside all three

`refs/JLPT_N2_NEW/` holds 21 official sittings that are not imported. They
carry **exact** `booklet.md` (printed options) and `key.md` plus audio, and
would take the official pool from 10 to 31 candidates per slot with zero
transcription of options or keys — which fixes novelty for 問題5 too, from the
side no textbook can reach.

**Two of the 21 just got much cheaper.** `refs/External/` now holds the
『日本語能力試験公式問題集』 第一集 and 第二集, whose N2 listening sets are re-releases
of **7-2011** and **12-2016** — both already in the archive, so they add no clip
(measured: 37.9 % and 40.7 % script-window overlap against a ~2 % background;
`refs/External/README.md` §1). What they add is an EXACT text layer for two
sittings the archive holds only as 1-bit stencil scans: a born-digital script for
both, and for 12-2016 the printed 問題1/問題2 option lists and the full 正答表 as
well. The paragraph below is about the OCR cost; for those two it is zero.

**The cost is not zero and it is not the OCR.** Each sitting has to become a
whole `tests/imported-<slug>/` paper before `build_choukai_bank.py` can read it
(§5): it needs a complete `聴解スクリプト.txt`, and the 30 choukai entries of
BOTH `詳細解説.json` and `詳細解説.vi.json`, hand-authored, before one clip is
bankable — the 71 言語知識・読解 items on top of that. The dialogue transcript
exists as Vision OCR at ~98% character accuracy in 28 of the 31 folders, which
is enough for `hint_from_script`'s lengths but not for the 「」 quotes the
詳細解説 is built on, so every quoted line needs checking against a page that is
a 1-bit stencil bitmap. One sitting is a full pipeline run; 21 is not a session.
Judged against Stages C–E in 2026-09-09's session and **declined in favour of
finishing both books**, which was self-contained and doubled the mixed slot
count. It remains the right next move, one sitting at a time.

---

## 7. 『新しい「日本語能力試験」問題例集』(2009) — a third source, and how it differs

Added 2026-09-09. `refs/External/mondaireishuu_2009/` — free from
<https://www.jlpt.jp/samples/sample09.html>, no account and no purchase.
`refs/External/README.md` owns the provenance; this section owns what it
contributes to the bank.

### Why it is here and not with the official half

These are official JEES recordings, but they are **not a sitting**: five items,
no 例, no `tests/imported-*` folder for `build_choukai_bank.py` to reconcile
audio against text. They are hand-declared — transcript, key, printed options,
both explanation panes — which is this file's shape, not that one's. Banking
them body-only also makes them **slot-FREE**, where an official record is locked
to the slot it occupied; all five sit in slot 1 of their 大問, so keeping the
slot would have wasted four of them.

### One MP3, five items — so a declaration names a WINDOW, not a track

`N2Sample.mp3` is 554 s and carries the whole sample sitting: opening, five 問題
instructions, one item per 大問. (The script and booklet PDFs print TWO items per
大問; the audio has the first of each. jlpt.jp says so on the page, and the file
confirms it — five answer pauses, five 「N番。」 calls, every second accounted for.)

So `build_textbook_bank.py` grew a second way to resolve audio: a `window`
bracketing the item between the structural silences either side of it. The span
is still **measured**, by snapping to the speech runs the window contains, and a
window whose edge falls inside a speech run is REFUSED — that is the guard that
replaces the track-number guard, and it is the one that matters here, because the
file lays 14–19 s of section instruction beside every item.

Structure, measured (`choukai_segment.measure`, extended threshold):

| | instruction | 「1番。」 | item body | pause after |
|---|---|---|---|---|
| 問題1 | 0.0–29.4 | 32.60–33.54 | **36.16–94.38** | 12.20 s |
| 問題2 | 106.6–137.7 | 137.66–138.60 | **141.22–237.18** | 12.18 s |
| 問題3 | 249.4–277.9 | 277.86–278.82 | **281.54–352.14** | 5.22 s |
| 問題4 | 357.4–384.7 | 384.72–385.68 | **388.40–410.96** | 5.44 s |
| 問題5 | 416.4–454.0 | 454.02–454.98 | **457.70–543.90** | 5.50 s |

The 5.2–5.5 s pauses are the sample's own, shorter than the exam's 8 s; the
composer discards them and lays the pacing table's value, exactly as it does for
a textbook clip.

**問題2 carries its 20 s option-reading pause, and it was verified inside the cut
clip**: 20.19 s at 11.90 s in, against official's 20.22 s [20.19–20.81] and the
8–14 s position every good Soumatome track lays it at (§2). That is the
measurement 問題2 is bottlenecked on and the one Shin Kanzen cannot supply at all.

### What is banked, and what is not

| item | section | span | rate | key | status |
|---|---|---|---|---|---|
| 問1-1 | 問題1 | 58.2 s | 0.162 | 3 | banked |
| 問2-1 | 問題2 | 96.0 s | 0.177 | 2 | banked |
| 問3-1 | 問題3 | 70.6 s | 0.197 | 4 | banked |
| 問4-1 | 問題4 | 22.6 s | 0.235 | 3 | banked |
| 問5-1 | 問題5 | 86.2 s | — | 4 | `excluded` — under the 105 s floor; old one-question 統合理解 shape (§6.2) |
| 問1-2 … 問4-2 | — | — | — | — | `excluded` — no audio; 問1-2 is a picture-legend item besides |

Keys read off `N2-seikai.pdf` p.155, printed options off `N2-mondai.pdf`
pp.51–56, scripts off `N2-script.pdf` pp.156–160. All five PDFs are scans with
no text layer, so every field was read from the page, never from an extract.

### `CHAR_RATE` could not judge these, and the measurement says why

`mondaireishuu:問4-1` was refused on the first build at **0.235 s/char** against
`CHAR_RATE`'s 0.200 ceiling. The window was right and the transcript was right.
Re-measuring the OFFICIAL bank with the same formula settled it:

| | 問題1 | 問題2 | 問題3 | 問題4 | 問題5 |
|---|---|---|---|---|---|
| official median | 0.197 | 0.200 | 0.215 | **0.231** | 0.211 |
| official range | 0.165–0.239 | 0.165–0.255 | 0.083–0.258 | 0.181–0.323 | 0.158–0.354 |
| over CHAR_RATE's 0.200 | 22/50 | 30/60 | 43/50 | **94/110** | 14/20 |

**94 of the official bank's own 110 問題4 items sit above the ceiling**, and our
item at 0.235 is the official 問題4 MEDIAN. So `CHAR_RATE` is a fact about how
Shin Kanzen and Soumatome press their CDs — tighter than the exam — not about
Japanese speech. What official lays and `expected_gaps` does not model is the
~1.1 s pause after each spoken 「N、」 (`choukai-audio` Part 3, deviation 3): the
repo speaks a choice as one utterance, so the function never needed it.

The repair was a **second band for a second recording style**, not a wider one:
`CHAR_RATE_OFFICIAL` = (0.080, 0.360), the official envelope above rounded
outward, selected per source by `rate_band_for()` — which
`check_choukai_textbook_bands` imports rather than restating, so the gate and the
builder cannot disagree about which band applies. It is wide, and it still guards
what this guard is for: a window off by one structural silence swallows 14–19 s
of instruction and lands far outside even this.

### The one code-level side effect worth knowing

問2-1's two speakers are a mother and her daughter, so the item needs a female
PAIR. `SPEAKER_MAP` had `男1`/`男2` but no `女1`/`女2` — even though
`choukai-audio` Part 2 has always documented 「女1/女2 + 男」 as a supported cast.
The labels were added (±20 Hz on the 210 Hz female base, 3.3 semitones apart,
pitch only). This is not about synthesis, which is retired:
`check_choukai_reaction_rate`, `check_choukai_volume` and
`check_mondai5_speakers` all parse turns by `label in SPEAKER_MAP`, so every turn
of a two-female item would have been invisible to the register gates rather than
wrong in the audio.


---

## 8. 『完全模試 N2』(Jリサーチ, 2013) — the first source that clears all five checks

Added 2026-09-10. `refs/KanzenMoshi/` — ISBN 978-4-86392-129-0, 3 audio CDs
(43 tracks each, one CD per mock paper), `…-Mock Tests.pdf` (128 pp, the 問題冊子)
and `…-Taisaku.pdf` (114 pp, 解答・解説). Both PDFs are scans with no text layer
and both are over the 100 MB read cap, so slice with pypdf before reading.
Purchased, like Shin Kanzen and Soumatome.

### The five-point check (`SKILL.md` §"Adding a NEW SOURCE"), measured

| # | Check | Result |
|---|---|---|
| 1 | audio | 3 CDs, paper-specific (no two tracks byte-identical across discs) |
| 2 | full script | ✅ printed per item in `Taisaku.pdf`, **with the CD track number as a badge** — transcript and track map on the same line, which no other source gives |
| 3 | key | ✅ 正答 per item, plus 他の選択肢 notes and a 言葉と表現 gloss usable for both explanation panes |
| 4 | 問題1/2 options | ✅ **text lists, not picture legends** (問題冊子 pp.34, 36) |
| 5 | exam timing | ✅ **all 18 問題2 items lay 19.3–20.1 s** of option-reading pause (official 20.22 [20.19–20.81], Soumatome 20.1–20.3, Shin Kanzen max 10.1) |

Point 5's 19.3 s floor sits **0.9 s under official's band** and the composer never
re-times it. Admitted as a knowing deviation: it is 4% short where Shin Kanzen's
is 50% short, and the number is recorded here so the next reader judges it rather
than rediscovers it.

### Track map — identical on all three CDs

| tracks | what |
|---|---|
| 01 / 02 / 09 / 17 / 25 / 38 / 41 | opening and the 問題1–5 instructions (41 is 問題5's 3番 lead-in) |
| 03 / 10 / 19 / 26 | the 問題1/2/3/4 例 |
| **04–08** | 問題1 ×5 |
| **11–16** | 問題2 ×6 (each carrying its own 19.3–20.1 s option pause) |
| **20–24** | 問題3 ×5 |
| **27–37** | 問題4 ×11 |
| **39 / 40 / 42** | 問題5: two single-question items with **SPOKEN** options, then the 質問1/質問2 item whose options the 問題冊子 prints |
| 43 | closing |

Item counts confirmed against the book's own 配点表 (解答・解説 p.87): 5/6/5/11/4,
55 点 — so this paper scores **31** listening answers where a current official
sitting scores 30, its 問題5 running three item blocks instead of two.

**One track per paper is still unexplained**: Track18 (54.4 s), between 問題3's
instruction and its 例. It touches no item — the 解説 badges make 例 = 19 and the
items 20–24 — so it is a note, not a blocker. Resolve it by ear when 問題3 is
transcribed.

### Every item track speaks its own 「N番。」

~1.0 s of speech then a 2.7–2.9 s pause, the shape §1 measured on official items.
`max_header_runs: 1` drops it, so these clips are banked **body-only and
slot-free** like every other hand-declared source, and the composer prepends a
harvested official call.

### `official_pacing: True`, and the measurement that decided it

Declared against `CHAR_RATE` (0.060–0.200) first, as §5 prescribes, and **nine of
the eleven correct declarations were refused** at 0.200–0.238 s/char. The spans
were right (17.9–25.1 s inside 問題4's 11–40 s band, against official's 20.3–31.9),
so the rate band was wrong for this source, exactly as it was for
`mondaireishuu:問4-1`: 第1回's eleven items measure **0.190–0.238 s/char** against
official 問題4's 0.181–0.323 (median 0.231) and Soumatome / Shin Kanzen 問題4's
0.111–0.196. The repair is the flag, not a wider band — this CD is pressed to exam
timing, and four independent measurements say so (the 20 s pause, the spoken
「N番。」, ~3 s spoken-choice gaps, 7.2–7.4 s answer pauses against official's 8).

### What is banked, and what remains

**第1回 問題4 ×11 (CD1 tracks 27–37)**, keys off 解答・解説 pp.33–34. Pool 23 → 34,
which bought back the fourth 問題4 slot (`TEXTBOOK_SLOTS` 問題4: 3 → 4, projected
2.82 uses against the 4.0 ceiling).

Untranscribed, in the order they pay off:

| what | items | buys |
|---|---|---|
| 問題2 ×18 | the bottleneck §6.1 called unfixable — 10 → 28 | slots 1 → 4 |
| 問題3 ×15 | 14 → 29 | slots 2 → 4 |
| 問題1 ×15 | 15 → 30 | slots 2 → 4 |
| 問題4 ×22 (第2回/第3回) | 34 → 56 | a 5th–9th slot |
| 問題5 ×6 spoken-option items | 0 → 6, but only **3** measure inside the 105–250 s band (bodies ≈85, 84, 100, 125, 133, 158 s) | a first 問題5 slot needs 6 in band, so still short — the same short-統合理解 shape §6.2 measured on `mondaireishuu:問5-1` |
| 問題5 ×3 質問1/質問2 items | options are PRINTED | blocked exactly as §6.2 describes |

Nothing here is blocked on a source any more; it is blocked on transcription time,
one 大問 at a time.


---

## 9. Three more books (2026-09-10) — one accepted, two accepted with limits

Run through `SKILL.md` §"Adding a NEW SOURCE" before any transcription. All
three print scripts, keys and text options, and all three PDFs are scans with a
watermark from a redistribution site rather than a publisher's own file — same
handling as every other book here, but the provenance is recorded rather than
described as a purchase.

| | 耳から覚える 聴解トレーニング N2 (`mimikara`) | ドリル&ドリル N2 聴解・読解 | 試験に出る N1/N2 聴解 |
|---|---|---|---|
| folder | `refs/MimikaraOboeru/` | `refs/DrillAndDrill/` | `refs/ShikenNiDeru/` |
| tracks | 93 (2 CDs) | 156 (3 CDs) | 187 (3 CDs) |
| script / key / text options | ✅ ✅ ✅ | ✅ ✅ ✅ | ✅ ✅ ✅ |
| **option-reading pause** | **20.3–20.5 s ×10** | **15.1–15.3 s ×30** | **none, 0 of 187** |
| bundled tracks (many items behind one track) | 12 | 0 | 0 |
| verdict | **accepted**, and it is the 問題2 source | accepted for 問題1/3/4; **問題2 REFUSED** | accepted for 問題1/3/4; **no 問題2**. N1 and N2 sections are separate — take only N2 |

### The 20 s measurement is the whole story again

`耳から覚える` lays **20.3–20.5 s** against official's 20.22 [20.19–20.81] — the
first source since Soumatome to sit inside the band, and its ten tracks are
exactly the two 実践問題 sets' ポイント理解 items (CD2 07–10, 35–38) plus the
ポイント理解 chapter's まとめの問題 pair (CD1 16–17). That is **10 more 問題2
items**, against a pool of 10 that has been stuck at one slot since 2026-09-09
(§6.1). Their printed option lists are not in the script section, so locating
them is the first job of the next session.

`ドリル&ドリル`'s 15.2 s is the interesting rejection: it is not abridged the way
Shin Kanzen's 10.1 s is, but it is still **25 % under** the pause the composer
never re-times, and there is now a source that lays the full one. Refused for
問題2, kept for the other three 大問.

`試験に出る` lays no option pause at all in any of its 187 tracks. Its 応用練習
items and its two 模擬試験 (one N1, one N2) are still usable for 問題1/3/4 —
**and its N1 half must never be drawn**, since nothing downstream re-checks
level.

### What is banked from it so far

Four items from 実践問題 第1回 — 問題3 ×2 (CD2-14, CD2-15) and 問題4 ×2 (CD2-17,
CD2-19) — keys off 別冊 p.15, whose answer table also cross-checks the three
問題4 scripts read off p.103 (2, 1, 3 — all three agree). 問題3 goes 14 → 16
(wear 3.43 → 3.00), 問題4 34 → 36 (2.67). No slot count moves: 問題3's third slot
still needs 18.

`mimikara:cd2-18` is `excluded` with its numbers — a **verified** declaration
refused at 0.246 s/char where its four siblings sit at 0.145–0.199, because the
line enumerates ("会議の書類作り、荷物の発送、机の片づけと") and the reader pauses
between the listed items, which `expected_gaps` does not model. The band stays
as it is; it separates types correctly for every other item in this book.

### Only the 実践問題 sets are declarable

The 練習 tracks bundle several items behind 10.3 s pauses (12 tracks), which is
the §6.3 problem: splitting one needs an ear, and a wrong boundary ships a clip
that starts mid-sentence. The exam-format material is the two 実践問題 sets —
per set 課題理解 4, ポイント理解 4, 概要理解 4, 即時応答 8, 統合理解 3 — plus each
chapter's まとめの問題 pair.
