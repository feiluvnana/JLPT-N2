# Mixed-pool 聴解 — adding Shin Kanzen and Soumatome to the clip bank

Status: **designed and de-risked, not implemented.** Phase 1 (official-only
composition) shipped 2026-09-08 and every generated paper now draws from the
ten imported sittings. The target state the user asked for is different:

- **exactly ONE test** composed from official recordings only;
- **every other test** composed from a MIXED pool — official + Shin Kanzen +
  Soumatome.

This file records what was verified while scoping that, so the next run starts
from evidence instead of re-deriving it. Everything below was measured, not
assumed; where something is still unknown it says so.

---

## 1. The blocker phase 1 did not have: textbook clips carry no 「N番。」

An official item's audio opens with the announcer saying 「3番。」 and the bank
keeps items in their original slot for exactly that reason (`choukai-audio`
Part 0). Textbook tracks have no number call at all, so a textbook clip dropped
into slot 3 would leave the examinee with no idea which item is playing.

**Measured (2026-09-08), and this is the finding that makes the mixed pool
work:** every official item has a **clean, long pause right after its number
call** — median 1.15 s into the item, median duration 2.68 s. Over the 290
banked items, 188 expose it at a 0.15 s detection floor. The 102 that do not
are dominated by each section's slot-1 item, whose clip start is snapped by the
preamble logic rather than by an answer pause.

Availability per number, counting only clean candidates:

| 番 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| candidates | 15 | 37 | 28 | 29 | 28 | 15 | 7 | 8 | 7 | 7 | 7 |

So all eleven numbers are harvestable. **The design follows from this:**

- official items stay exactly as they are — slot-preserved, carrying their own
  call, no re-cut, no re-verification of phase 1;
- textbook items are banked BODY-ONLY and the composer prepends a harvested
  「N番。」 clip plus a ~2.7 s pause. Having no baked-in number, they are
  slot-free and can fill any position.

Do **not** re-cut the official bank to split every number call. It is
unnecessary (official items already have theirs) and 102 of 290 have no clean
cut point anyway.

---

## 2. Soumatome — the better of the two sources

`refs/Soumatome/nihongo-soumatome-n2-choukai-kaitou-script.pdf` (54 pp, 55 MB,
added by the user 2026-09-08). No text layer, but it is a **clean scan** and
reads reliably page by page — unlike the Shin Kanzen OCR (below). Under the
100 MB read cap, so it opens directly.

Every item is a table row carrying, in one place:

- a **「こたえ」 column** — the answer key;
- the **full script**;
- a **CD track icon** (`cd1/25`, `cd2/4`) — the audio mapping, printed;
- for 概要理解 and 統合理解, **the four printed options as well**.

### Track mapping — verified against audio durations

`cd1/N` → `refs/Soumatome/Nihongo Sou Matome N2 - Choukai-CD/日本語総まとめＮ2-ＣＤ1/NN.mp3`
(64 tracks), `cd2/N` → `…/日本語総まとめＮ2-ＣＤ2/NN.mp3` (52 tracks).

Spot-checked, and the durations match the item type the book claims:

| track | book says | duration | consistent with |
|---|---|---|---|
| cd1/25, 26 | 課題理解 (問題1) | 71.4 s, 74.4 s | 問題1 items run 33–110 s |
| cd1/29 | ポイント理解 (問題2) | 91.7 s | 問題2 |
| cd1/32 | 概要理解 (問題3) | 109.5 s | 問題3 |
| cd1/35, 38 | 統合理解 (問題5) | 112.2 s, 144.5 s | 問題5 |
| cd1/39–43 | 即時応答 (問題4) | 24.8–33.7 s | 問題4 items run 14–31 s |

That agreement across five different item types is what makes the mapping
trustworthy; do not bank a track whose duration contradicts its claimed type.

### Structure located so far

- 第1章 準備しよう — pronunciation/grammar drills. **Not exam-shaped, skip.**
- 第2章 問題のパターンに慣れよう — one section per exam type:
  課題理解 (p.10), ポイント理解 (p.11), 概要理解 (p.12), 統合理解① (p.13),
  統合理解② (p.15), then まとめ問題 with 問題I–V (pp.16–21).
  **問題I of まとめ問題 is a run of five 即時応答 items** (cd1/39–43).
- 第3章 いろいろなタイプの話を聞こう — 指示や説明 (p.22), 会話 (p.23),
  電話・メッセージ (p.25), 意見や感想 (p.27), まとめ問題 (pp.29–31 onward).
- Pages 32–54 not yet read. Expect the remaining chapters plus a 模擬試験.

---

## 3. Shin Kanzen — usable only via the book, never via the extract

**`refs/Shinkanzen/choukai_script.md` is unusable as a transcript.** Its OCR
renders 男 as 第/勤/顎/舅, 女 as 袋/愛/髪, 質問 as 資簡/資間, and mangles the
option digits. It remains fine for what `AGENTS.md` §3 says it is — corroborating
register and family — and must never be used for a key or a quoted line.

The **PDF itself is clean typeset**. `Shin_Kanzen_Masuta_N2-Choukai.pdf` is
193 MB, over the read cap, so slice it first (pypdf; the 別冊 begins at PDF
p.116 and its own TOC puts 模擬試験 at 別冊 p.35 ≈ PDF p.150).

The 模擬試験 is the high-value slice: a complete 問題1–5 paper in the same
5/6/5/11/2 shape as official, printing 「答え N」 and a CD track icon per item.

### Track mapping — verified two ways

Read off the book (B46–B50 = 問題1 1番–5番, B52–B54 = 問題2 1番–3番) and
independently confirmed by CD2 durations:

| CD2 tracks | duration shape | section |
|---|---|---|
| 46–50 | 61.8–94.5 s | 問題1 ×5 |
| 52–57 | 87.0–102.6 s | 問題2 ×6 |
| 59–63 | 74.3–94.5 s | 問題3 ×5 |
| 65–76 | 23.4–29.0 s | 問題4 ×12 (例 + 11) |
| 78–80 | 119.2–171.6 s | 問題5 |

Tracks 45, 51, 58, 64, 77 are the short section instructions between them.

Keys already read from the 別冊: 問題1 = 3, 2, 2, 1, 3; 問題2 1番–3番 = 4, 3, 2.
**Everything else still needs reading off the page.**

---

## 4. What each section costs

The gating question per section is where its printed options live.

| section | options | needs | cost |
|---|---|---|---|
| 問題3 概要理解 | printed | script PDF alone — options are in the answer booklet | **cheap** |
| 問題4 即時応答 | spoken | script + key only | **cheapest, and 11 of 29 slots** |
| 問題5 統合理解 | printed | script PDF alone | **cheap** |
| 問題1 課題理解 | printed | script PDF **+ the main 問題冊子** for the option lists | medium |
| 問題2 ポイント理解 | printed | same | medium |

Recommended order: 問題4 first (largest section, smallest items, one-digit
keys, nothing to print), then 問題3 and 問題5, then 問題1/2 once the 問題冊子
pages are transcribed.

---

## 5. Remaining implementation

1. `tools/harvest_number_calls.py` → bank one clean 「N番。」 span per number
   1–11, choosing among the candidates in §1 and verifying each is 0.6–1.2 s of
   speech followed by a ≥1.2 s pause.
2. Extend the bank schema with `"source": "official" | "soumatome" | "shinkanzen"`
   and, for textbook records, `"needs_number_call": true`. Bump `BANK_VERSION`.
3. `tools/build_textbook_bank.py` — hand-transcribed items keyed by
   `(book, cd, track)`, resolved to audio paths, duration-checked against the
   §2/§3 tables before being admitted.
4. `tools/compose_choukai.py`: prepend the number call for textbook items, and
   add a source policy — one test official-only, the rest mixed with a target
   share per section.
5. Re-draw the 22 mixed papers, rebuild, `make check`, `make upload-files`,
   commit.

**A cheaper win that is NOT a substitute but should be considered alongside:**
the 21 official sittings in `refs/JLPT_N2_NEW/` that are not yet imported have
**exact** `booklet.md` (printed options) and `key.md` (keys) plus audio, and
would take the pool from 10 to 31 candidates per slot with zero transcription.
Their dialogue transcript is OCR in 28 of 31 cases, which costs the 詳細解説
its quoted script evidence but nothing else — and `hint_from_script` only needs
approximate LENGTHS, which OCR preserves even when it mangles characters.
