# Mixed-pool 聴解 — Shin Kanzen and Soumatome in the clip bank

Status: **built and shipping for 問題3 and 問題4** (2026-09-08). 問題1, 問題2 and
問題5 are still official-only, for source reasons named in §6 — not because
nobody got to them.

What is true on disk now:

- **exactly ONE paper is composed from official recordings only** —
  `20260807_1`, named in `compose_choukai.OFFICIAL_ONLY_TESTS`. It is the
  control: the reference a listener can compare the mixed papers against;
- **every other paper draws from a MIXED pool** — the ten imported official
  sittings plus 26 textbook items, `TEXTBOOK_SLOTS` of each 大問's slots taken
  from the textbook side. Each paper's mix is recorded in
  `logs/choukai_draws.json` under `sources`.

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

### Keys

All read off the page, never from the OCR extract:

- 問題1 = 3, 2, **?**, 2, 3 — 1番/2番 別冊 p.35, 4番/5番 p.39; **3番 (別冊 p.38) has not been read**
- 問題2 4番–6番 = 2, 3, 4 (別冊 p.39, read here). **1番–3番 = 4, 3, 2 is carried
  over from this file's earlier revision and was NOT re-read** — treat it as
  unverified until someone opens 別冊 p.38
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
| 問題4 即時応答 | spoken | script + key only | **22 items** (Soumatome 10, Shin Kanzen 12) |
| 問題3 概要理解 | spoken by BOTH books (and printed in the answer booklet too) | script + key + option text | **4 items** (Shin Kanzen) |
| 問題5 統合理解 | Shin Kanzen PRINTS 1番's four choices instead of speaking them | see §6 | 0 |
| 問題1 課題理解 | printed | script PDF **+ the main 問題冊子** for the option lists | 0 |
| 問題2 ポイント理解 | printed | same, and Shin Kanzen's option pause is half official's | 0 |

問題3 and 問題4 together are 16 of a paper's 29 slots, and the two 大問 whose
options the audio speaks — which is exactly why they were cheap. Nothing about
them needed a page of the 問題冊子.

---

## 5. What exists now

| File | Owns |
|---|---|
| `tools/harvest_number_calls.py` | `logs/choukai_number_calls.json` — one clean 「N番。」 span per number 1–11, from one sitting. `make number-calls [CHECK=1]` |
| `.agents/choukai-audio/references/textbook_items.json` | The hand transcriptions: script lines, key, page, and both explanation panes. Also an `excluded` list with the measurement that refused each entry |
| `tools/build_textbook_bank.py` | Resolving each (book, cd, track) to audio, measuring the body span, and REFUSING an item that fails a guard. `make textbook-bank` reports; it never writes |
| `tools/build_choukai_bank.py` | Still the single writer of `logs/choukai_bank.json`, now `BANK_VERSION = 2` with both halves. `make choukai-bank` |
| `tools/compose_choukai.py` | The source policy (`OFFICIAL_ONLY_TESTS`, `TEXTBOOK_SLOTS`), the number-call prepend, and `resolve()` — the one place a slot-free textbook record becomes a `問N-M`-keyed item |

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
   implied speech rate inside `CHAR_RATE` (0.060–0.200 s/char).

Both are **type-separation bands, not calibration figures** — the calibrated
numbers live in `SKILL.md`'s pacing table. The second guard is the one that
matters: it caught both anomalous tracks in §2, neither of which the duration
band alone would have rejected. A refusal fails `make choukai-bank`; the repair
is to fix the declaration or move the item to `excluded` **with the measurement
that justifies it**.

Admitted items measure 0.111–0.191 s/char, so the band has real headroom on both
sides and the two refusals sat at 0.36.

---

## 6. What remains, and the exact blocker for each

1. **問題1 and 問題2** — their options are PRINTED, and neither answer booklet
   prints 課題理解's or (for Shin Kanzen) ポイント理解's. The lists are in the main
   問題冊子: `refs/Soumatome/nihongo-soumatome-n2-choukai.pdf` (99 MB, under the
   read cap) and the front half of the Shin Kanzen PDF (over it — slice first).
   Soumatome's answer booklet DOES print ポイント理解's options (別冊 pp.49–50,
   cd2/39–42), so **four Soumatome 問題2 items are cheap and are the obvious next
   step.**
   One caveat that must not be skipped: a **Shin Kanzen 問題2 track lays only a
   10.1 s option-reading pause** (measured on Track52) where official lays 20.2 s
   and `choukai_segment.GAP_OPTION_READING` expects it. Banking one would give
   the examinee half the reading time, inside a clip nothing re-times. Soumatome
   lays 20.2 s (cd1/29) and has no such problem.
2. **問題5** — two independent blockers. Shin Kanzen PRINTS 1番's four choices
   where official and this repo's 問題5-1番 speak them, so a lifted 1番 leaves the
   examinee with bubbles and no options. And neither book lays the **10 s 質問1
   answer pause** that sits INSIDE an official 2番 between the two read-backs
   (`SKILL.md` §「質問1。/質問2。 are not labels, they are the answer pause」).
   Both need composer work — splitting a clip at its own 質問1 boundary and
   inserting `GAP_AFTER_SHITSUMON1` — not just a transcript.
3. **More 即時応答 and 概要理解.** Both books have exercise-chapter items beyond
   the mock papers that were not read (Soumatome 第2章/第3章/第4章; Shin Kanzen's
   practice chapters, CD1 and CD2 tracks 1–44). Every one is a straight extension
   of `textbook_items.json` with no tooling change. Growing the pool is what
   lets `TEXTBOOK_SLOTS` go up without re-mining the same 26 clips.
4. **The cheaper win that is still NOT a substitute:** the 21 official sittings
   in `refs/JLPT_N2_NEW/` that are not yet imported have **exact** `booklet.md`
   (printed options) and `key.md` (keys) plus audio, and would take the official
   pool from 10 to 31 candidates per slot with zero transcription. Their dialogue
   transcript is OCR in 28 of 31 cases, which costs the 詳細解説 its quoted script
   evidence but nothing else — and `hint_from_script` only needs approximate
   LENGTHS, which OCR preserves even when it mangles characters.
