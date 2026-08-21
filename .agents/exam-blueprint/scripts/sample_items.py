#!/usr/bin/env python3
"""
Sample a randomized test blueprint from the N2 item pools.

Usage:
    python sample_items.py --test-id 4 --seed 20260803
    python sample_items.py --test-id 4 --reroll grammar_p7 --seed 99999
    python sample_items.py --test-id 4 --reroll-one quick_response:8 --seed 99999

Outputs tests/<test_id>/test_spec.json (the authoring contract) and updates
ledger.json (v2 LRU cooldown: an item drawn within the last N draws is
ineligible, where N is PER-CATEGORY — long relative to how deep that
category's own pool is, see `cooldown_for()` — not a single flat constant;
when a pool cannot fill a draw the cooldown relaxes one step at a time and
says so — history is never reset). Once the cooldown window has excluded the
recently-used items, the pick among what remains is WEIGHTED by recency too
(`weighted_sample_no_replacement()`), not uniform — an item that cleared the
cooldown a moment ago is still less likely to be drawn than one unused for
much longer, so a draw does not cluster right at the cooldown boundary.
"""

import argparse
import hashlib
import itertools
import json
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOLS = HERE.parent / "references" / "pools.json"
ROOT = HERE.parents[2]
LOGS_DIR = ROOT / "logs"
LEDGER = LOGS_DIR / "ledger.json"
STAGING = LOGS_DIR / "adjunct_staging.json"

sys.path.insert(0, str(HERE))
from level_data import (  # noqa: E402
    THEMED_CATS, THEMES, entry_text as item_text, entry_key, entry_theme,
)

ADJUNCT_CAP = 0.20  # max share of each category draw filled from staging

# R13: how many entries of one theme a single draw may hold before the mix is
# too narrow to give every 問題 its own subject. Warn, don't fail: the author
# maps scenarios to 問題, so only they can see whether two same-theme entries
# actually collide.
#
# The LISTENING cap is set ABOVE the expected count so the warning means
# "unusually concentrated", not "the pool is uneven": 働き方 holds 44/240
# listening entries -> 3.9 expected in a 21-draw, so a cap of 3 would fire on
# nearly every seed and be ignored within two tests. Re-derive it if the pool
# balance changes.
#
# READING is 1, and it is a floor the draw itself now meets rather than a
# warning the author is left to act on: every 読解 surface must sit on its own
# theme (`exam-blueprint` rule 3, `question-authoring/references/dokkai.md`
# §"Thirteen surfaces, thirteen different essays"). 20260810_1 shipped five
# workplace-institution reading surfaces under the old cap of 2 — the cap held
# on the draw and the paper still read as one essay repeated, because the cloze
# and the web seeds were never counted. The arithmetic works: 19 of the 20
# themes carry reading entries (行政・手続き carries none) against a 12-topic
# draw, so distinctness leaves 7 themes spare.
THEME_CAP = {"reading_topics": 1, "listening_scenarios": 5}

# Categories whose draw must hold at most one entry per theme, enforced during
# the draw by `sample_distinct_theme()` rather than warned about afterwards.
DISTINCT_THEME_CATS = {"reading_topics"}

# Target per-ITEM probability that a 問題5/6 draw slot is a katakana
# headword, enforced during the draw by `sample_katakana_capped()`.
# Measured against the 7 current-era sittings
# (`question-authoring/references/official_calibration.md` §12): the archive
# draws a katakana HEADWORD in only 3/35 (問題5, 8.6%) and 1/35 (問題6, 2.9%)
# items — never more than one per section in the same paper. `pools.json`'s
# `paraphrase` is 27.1% katakana-containing and `usage` is 32.7%; a plain
# `rng.sample()` reproduces that composition (~1.4 and ~1.6 expected katakana
# items per 5-draw) instead of the archive's near-zero norm. Three generated
# papers checked before this existed drew 3, 3 and 6 combined katakana
# headwords per paper against an official average of 0.57. These are the
# measured item-level rates, not the pool's native share — do not replace them
# with `len(katakana)/len(pool)` if the pool composition changes; re-measure
# the archive instead.
KATAKANA_TARGET_RATE = {"paraphrase": 3 / 35, "usage": 1 / 35}
KATAKANA_CAP = {"paraphrase": 1, "usage": 1}  # never observed 2 in one section

# Target per-ITEM probability that a 問題1 draw slot is a 訓読み target, and the
# hard per-paper ceiling, enforced during the draw by `sample_kun_capped()`
# (qa-report-20260819_1 F3).
# `question-authoring/references/moji-goi.md` §問題1 measured 12 訓読み of the 35
# current-era 問題1 items (34%), and per sitting official runs 2/2/1/2/2 of 5 —
# never more than TWO. Nothing enforced that: `20260819_1` drew 4 of 5 訓読み
# (半ば/情け/湯/常に), `20260807_1` drew 4, `20260810_1` and `20260817_2` drew 3.
# The consequence is not cosmetic — the 2×2 on-reading grid (清濁/長短
# discrimination) that official exercises in 3–4 of the 5 slots is what 問題1
# actually discriminates on, and a 訓読み-heavy paper measures word recognition
# instead. The rate is the archive's, not the pool's own 31% 訓読み share; do not
# re-derive it from `pools.json`.
KUN_TARGET_RATE = {"kanji_reading": 12 / 35}
KUN_CAP = {"kanji_reading": 2}
# ...and the FLOOR, added 2026-08-21 (REPORT-GOI.md §F5). A one-sided rule
# produces the opposite monoculture: with only a ceiling, `20260817_3` drew 0 of
# 5 訓読み and the gate printed `ok`. Five hand-classified sittings run 2/2/1/2/2,
# minimum ONE — a paper testing five on-reading compounds stops testing word
# recognition, which is the other half of what 問題1 measures. Both bounds are
# enforced by `sample_kun_capped()` and re-checked by
# `check_mondai1_reading_type_mix()`.
KUN_FLOOR = {"kanji_reading": 1}

# 問題2 composition, enforced during the draw by `sample_wago_floor()`
# (REPORT-GOI.md §F3). Measured over 31 of 31 sittings: 1–3 of the five 問題2
# items are 和語 targets with printed okurigana (median 2) and 1–3 are bare
# 2-kanji compounds (median 3). Ours ran 0–2 和語 (six papers at ZERO) and 2–5
# compounds (eleven at 4 or 5), because `moji-goi.md` taught the 2×2 component
# grid in detail and never put a count on it — so 問題2 became one puzzle
# repeated five times. This is a DRAW property, not a writing choice: the
# `orthography` entry decides it. Drawn and printed counts agree on all 14
# papers on disk, so the gate may read either.
WAGO_FLOOR = {"orthography": 1}          # author to 2
COMPOUND_CAP = {"orthography": 3}        # the archive's own ceiling, 31 of 31
# The archive's OWN histogram of 和語 items per sitting (31 sittings: one paper
# with 1, twenty-three with 2, seven with 3). The draw samples this instead of
# fixing the count at the median, because a fixed quota reproduces a shape the
# archive varies — the same reason `sample_katakana_capped()` runs Bernoulli
# trials rather than forcing exactly one katakana headword.
WAGO_DIST = {"orthography": {1: 1, 2: 23, 3: 7}}


def is_katakana_headword(entry) -> bool:
    """True if the pool entry's headword (gloss stripped) is a katakana word.

    `head()` already strips the disambiguating `(...)`/`（...）` gloss —
    `怠る(サボる/なまける)`'s headword is `怠る`, not katakana, even though the
    gloss names a katakana synonym. Matches on any katakana character, same
    test used to measure the archive rate in official_calibration.md §12.
    """
    return bool(re.search(r"[゠-ヿ]", head(item_text(entry))))


# --- 訓読み / 音読み classification of a `kanji_reading` entry (F3) ----------
# A `kanji_reading` entry is `語(よみ)`. Official treats the two target types
# differently (moji-goi.md §問題1's distractor table), and only the 音読み
# compound carries the 2×2 清濁/長短 grid, so the mix is a calibration number,
# not a taste. Nothing could count it before this: the shape of a reading is the
# only signal on disk — there is no 音訓 column in `pools.json` and no
# grep-able dictionary in the repo (`joyo_kanji.txt` is a bare character set).
_KUN_KANA = re.compile(r"[ぁ-んァ-ヶーゝゞ々]")
_KUN_KANJI = re.compile(r"[一-鿕]")
_KUN_SMALL = "ゃゅょ"
# The morae an ON-reading may take as its SECOND mora (漢音/呉音 shapes:
# こう/かい/せん/しき/かつ/ぎょう…). A native 訓読み almost never lands here
# (なか, なさ, つね, さかい, わざ …) — that asymmetry is the whole test.
_ON_TAIL = set("うくきつちんいーっ")
_SURU_TAILS = ("じる", "ずる", "する")


def _morae(s: str) -> list[str]:
    out: list[str] = []
    for ch in s:
        if ch in _KUN_SMALL and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def _on_shaped_chunk(ms: list[str]) -> bool:
    return len(ms) == 1 or (len(ms) == 2 and ms[1] in _ON_TAIL)


def on_segmentable(reading: str, k: int) -> bool:
    """Can `reading` be cut into exactly `k` ON-reading-shaped chunks?

    こうしょう → こう|しょう (2 kanji) yes; かたみち → no cut of かたみち into two
    on-shaped chunks exists, so 片道 is a 訓読み compound even though it prints
    no okurigana.
    """
    ms = _morae(reading)
    if not ms or k <= 0:
        return False

    def rec(i: int, left: int) -> bool:
        if left == 0:
            return i == len(ms)
        return any(i + L <= len(ms) and _on_shaped_chunk(ms[i:i + L])
                   and rec(i + L, left - 1) for L in (1, 2))

    return rec(0, k)


def split_reading_entry(entry) -> tuple[str, str]:
    """`半ば(なかば)` -> (`半ば`, `なかば`); an entry with no gloss -> (entry, '')."""
    m = re.match(r"^(.+?)[(（](.+?)[)）]\s*$", item_text(entry))
    return (m.group(1).strip(), m.group(2).strip()) if m \
        else (item_text(entry).strip(), "")


def is_kun_target(entry) -> bool:
    """True when a `kanji_reading` entry's target is a 訓読み word.

    KNOWN LIMIT, stated rather than hidden: this decides 音 vs 訓 from the SHAPE
    of the recorded reading, so a single-kanji 訓読み word whose reading happens
    to be on-shaped (灰(はい), 恋(こい), 奥(おく), 筒(つつ), 乳(ちち) — 5 of the
    pool's 74 single-kanji entries) reads as 音読み here. It errs toward
    UNDER-counting 訓読み, i.e. toward letting a draw through, never toward
    failing a compliant one. The four founding cases it must reproduce are
    `20260807_1` (4), `20260819_1` (4), `20260810_1` (3), `20260817_2` (3);
    `check_mondai1_reading_type_mix()` in `tools/check_consistency.py` imports
    THIS function so the gate and the sampler can never disagree.
    """
    t, r = split_reading_entry(entry)
    t = t.replace("〜", "").replace("～", "").replace("~", "")
    if not _KUN_KANJI.search(t):
        return True                       # kana headword: not an on-compound
    m = re.search(r"([ぁ-ん]+)$", t)
    tail = m.group(1) if m else ""
    core = t[:len(t) - len(tail)] if tail else t
    if _KUN_KANA.search(core):
        return True                       # internal okurigana: 折り曲げる, 取り扱う
    ks = _KUN_KANJI.findall(core)
    if not ks:
        return True
    if not r:
        return not tail
    if tail:
        if not r.endswith(tail):
            return True                   # reading and spelling disagree: judge kun
        stem = r[:-len(tail)]
    else:
        stem = r
    if len(ks) == 1:
        # 演じる/生じる/害する are 音読み stems wearing okurigana; 見にくい,
        # 閉じる, 恥じる are not — the stem has to be an on-shaped 2+-mora
        # reading before the okurigana can be discounted.
        if tail and tail not in _SURU_TAILS:
            return True
        return not (len(_morae(stem)) >= 2 and on_segmentable(stem, 1))
    return not on_segmentable(stem, len(ks))


# --- 和語 / bare-compound classification of an `orthography` entry (F3) -----
# One regex each on the entry's headword, shared by the sampler and the gate the
# way `is_kun_target()` is: 問題2 prints the target in KANA and the options in
# kanji, so what decides the branch is whether the WORD carries okurigana
# (努める, 険しい, 計る → 和語) or is a bare 2-kanji compound (果実, 系統 → grid).
_HIRAGANA = re.compile(r"[ぁ-ゟ]")


def is_wago_orthography(entry) -> bool:
    """True if an `orthography` headword carries okurigana/kana (a 和語 target)."""
    return bool(_HIRAGANA.search(head(item_text(entry))))


def is_bare_compound(entry) -> bool:
    """True if an `orthography` headword is exactly two kanji and no kana."""
    h = head(item_text(entry))
    return len(h) == 2 and len(_KUN_KANJI.findall(h)) == 2


def weighted_sample_no_replacement(rng: random.Random, items: list,
                                   weights: list[float], n: int) -> list:
    """Weighted sample of `n` items from `items`, no replacement.

    Efraimidis-Spirakis A-Res: give each item a key `u ** (1/w)` for
    `u ~ Uniform(0,1)`, keep the top-`n` keys. This is what lets `draw()`
    do more than exclude the cooldown window and then pick uniformly among
    what is left — heavier weight (a larger `ago`, i.e. longer since last
    use, or never used) makes an item more likely to win, so a draw does not
    cluster right at the cooldown boundary the instant an item clears it.
    `n` may equal `len(items)` — this then returns every item, weighted-shuffled
    (`sample_distinct_theme` relies on exactly that to order its greedy pass).
    """
    keyed = sorted(
        ((rng.random() ** (1.0 / w), it) for it, w in zip(items, weights)),
        key=lambda kv: kv[0], reverse=True,
    )
    return [it for _, it in keyed[:n]]


def sample_katakana_capped(rng: random.Random, eligible: list, n: int,
                           target_rate: float, cap: int, name: str,
                           weight_fn=None) -> list:
    """`n` entries whose katakana-headword count matches the archive's rate.

    §12's archive rate is near-zero per paper (0 in most sittings, 1 in a
    minority, never 2+ in one section) — a fixed quota that forces exactly
    `cap` katakana items every draw, or that only trims the pool's native ~30%
    share down to `cap` without lowering how OFTEN a katakana item appears at
    all, both reproduce a shape the archive doesn't have. So: run `n`
    independent Bernoulli(target_rate) trials to decide how many katakana
    slots this draw gets (capped at `cap`), then fill that many from the
    katakana subset and the rest from the non-katakana subset.

    `weight_fn`, when given, picks each subset by recency weight (see
    `weighted_sample_no_replacement`) instead of uniformly.
    """
    kata = [e for e in eligible if is_katakana_headword(e)]
    plain = [e for e in eligible if not is_katakana_headword(e)]
    k = min(cap, len(kata), sum(rng.random() < target_rate for _ in range(n)))

    def pick(pool: list, count: int) -> list:
        if count <= 0:
            return []
        if weight_fn:
            return weighted_sample_no_replacement(
                rng, pool, [weight_fn(e) for e in pool], count)
        return rng.sample(pool, count)

    if len(plain) < n - k:
        print(f"  warning: pool '{name}' has too few non-katakana entries "
              f"({len(plain)}) to fill {n - k} of {n} slots — falling back "
              f"to an uncapped draw; grow the non-katakana side of this pool")
        return pick(eligible, n)
    picked = pick(plain, n - k) + pick(kata, k)
    rng.shuffle(picked)
    return picked


def sample_kun_capped(rng: random.Random, eligible: list, n: int,
                      target_rate: float, cap: int, name: str,
                      already: int = 0, weight_fn=None,
                      floor: int = 0) -> list:
    """`n` entries whose 訓読み count sits inside the archive's BAND.

    Same shape as `sample_katakana_capped()`, and for the same reason: the
    pool's own 訓読み share (31%) is close to the archive's (34%), so an
    unbounded draw is usually fine and occasionally lands 3 or 4 of 5 — which
    four papers did, with no gate able to see it (qa-report-20260819_1 F3) — or
    ZERO, which `20260817_3` did under the ceiling-only rule (REPORT-GOI §F5).
    `already` is how many 訓読み entries of this category the draw is KEEPING
    (nonzero only on the `--reroll-one` path), so a one-entry redraw can neither
    push the paper over the ceiling nor leave it under the floor the full draw
    respects.
    """
    budget = max(0, cap - already)
    kun = [e for e in eligible if is_kun_target(e)]
    plain = [e for e in eligible if not is_kun_target(e)]
    k = min(budget, len(kun), sum(rng.random() < target_rate for _ in range(n)))
    k = max(k, min(budget, len(kun), max(0, floor - already)))

    def pick(pool: list, count: int) -> list:
        if count <= 0:
            return []
        if weight_fn:
            return weighted_sample_no_replacement(
                rng, pool, [weight_fn(e) for e in pool], count)
        return rng.sample(pool, count)

    if len(plain) < n - k:
        print(f"  warning: pool '{name}' has too few 音読み entries "
              f"({len(plain)}) to fill {n - k} of {n} slots — falling back "
              f"to an uncapped draw; grow the 音読み side of this pool")
        return pick(eligible, n)
    picked = pick(plain, n - k) + pick(kun, k)
    rng.shuffle(picked)
    return picked


def sample_wago_floor(rng: random.Random, eligible: list, n: int, floor: int,
                      compound_cap: int, name: str, kept: list | tuple = (),
                      weight_fn=None, dist: dict | None = None) -> list:
    """`n` `orthography` entries with at least `floor` 和語 targets and at most
    `compound_cap` bare 2-kanji compounds (F3).

    Unlike the katakana and 訓読み caps this is not a per-item rate — the archive
    runs BOTH branches in every one of 31 sittings (和語 1–3, compounds 1–3) — so
    the 和語 count is drawn from the archive's own histogram (`WAGO_DIST`) and the
    compounds fill the rest up to their ceiling. `kept` is what a `--reroll-one`
    is keeping, counted against both bounds.
    """
    wago = [e for e in eligible if is_wago_orthography(e)]
    comp = [e for e in eligible if is_bare_compound(e)]
    other = [e for e in eligible if e not in wago and e not in comp]
    have_w = sum(1 for x in kept if is_wago_orthography(x))
    have_c = sum(1 for x in kept if is_bare_compound(x))

    def pick(pool: list, count: int) -> list:
        if count <= 0 or not pool:
            return []
        count = min(count, len(pool))
        if weight_fn:
            return weighted_sample_no_replacement(
                rng, pool, [weight_fn(e) for e in pool], count)
        return rng.sample(pool, count)

    hist = dist or {2: 1}
    target = rng.choices(list(hist), weights=list(hist.values()))[0]
    want_w = max(0, max(floor, target) - have_w)
    if len(wago) < want_w:
        print(f"  warning: pool '{name}' has too few 和語 entries "
              f"({len(wago)}) to fill {want_w} of {n} slots — grow the "
              f"okurigana side of this pool (moji-goi.md §問題2 composition)")
        want_w = len(wago)
    picked = pick(wago, want_w)
    room_c = max(0, compound_cap - have_c)
    rest = n - len(picked)
    take_c = min(room_c, rest, len(comp))
    picked += pick(comp, take_c)
    rest = n - len(picked)
    if rest > 0:
        spare = [e for e in other + wago + comp if e not in picked]
        # Never break the compound ceiling to fill the draw: prefer anything
        # that is not a bare compound, and only then fall back.
        first = [e for e in spare if not is_bare_compound(e)]
        picked += pick(first, min(rest, len(first)))
        rest = n - len(picked)
        if rest > 0:
            picked += pick([e for e in spare if e not in picked], rest)
    rng.shuffle(picked)
    return picked

# category -> items drawn per test (N2)
DRAW = {
    "kanji_reading": 5,
    "orthography": 5,
    "word_formation": 3,
    "context_words": 7,
    "paraphrase": 5,
    "usage": 5,
    "grammar_p7": 12,
    "grammar_p8": 5,
    "quick_response": 11,
    # 5+6+5 scored items + 例×3 + 統合2 = 21. This was 19 (and 20 before that):
    # the 統合 term was in the comment but never in the value, so 問題5's two
    # items got no sampled scenario and the author had to invent one.
    "listening_scenarios": 21,   # 5+6+5 items + 例×3 + 統合2 (author maps them)
    "reading_topics": 12,        # 5 short + 4 medium + 1 A/B + 1 long + 1 info
}

# answer-position plans: (section, count, positions)
ANSWER_SECTIONS = [
    ("問題1_語彙", 5, 4), ("問題2_語彙", 5, 4), ("問題3_語彙", 3, 4),
    ("問題4_語彙", 7, 4), ("問題5_語彙", 5, 4), ("問題6_語彙", 5, 4),
    ("問題7", 12, 4), ("問題8", 5, 4), ("問題9", 4, 4),
    ("問題10", 5, 4), ("問題11", 8, 4), ("問題12", 2, 4),
    ("問題13", 3, 4), ("問題14", 2, 4),
    ("聴解_問題1", 5, 4), ("聴解_問題2", 6, 4), ("聴解_問題3", 5, 4),
    ("聴解_問題4", 11, 3), ("聴解_問題5", 3, 4),
]


# R17: key arrangement must be unpredictable across sections.
# Do NOT force each individual section/mondai to have floor(count/4) of each
# position 1..4 (which made small sections completely predictable, e.g. every 4-item
# section having {1,2,3,4} and every 2-item section having distinct numbers).
# Instead, the 90 four-choice items are globally balanced across the whole paper
# (each position 1..4 receives 19-27 items, POSITION_BAND) with no 4 identical
# answers in a row anywhere, seams included. Until 2026-08-19 that balance was
# produced by shuffling ONE 90-item deck and slicing it in order; the slices are
# now built per section against SECTION_MODE_DIST and checked for the global band
# afterwards (R2-F8, below) — the whole-paper contract in this note is unchanged,
# only the direction the plan is built in.
#
# 2026-08-18: the shuffle cap was a run of 3 (no 1-1-1) until this line, which
# turned out to over-correct the R17 fix above for the four SMALL 聴解 slices
# specifically (5/6/5/3 items) — even a properly balanced global deck reads as
# suspiciously even once cut into a window that small. Measured against the
# official archive's own key.md answer keys (refs/JLPT_N2_NEW/16. N2 7-2025 and
# 17.N2 12-2025's 聴解問題1, 5 items each): 7/2025 keys 2,3,3,3,2 — a real run of
# THREE, and only 2 of the 4 positions used at all; 12/2025 keys 2,2,3,1,1 —
# again only 3 of 4 positions. Every one of this repo's first 11 tests'
# 聴解問題1 sections used all 4 positions with no repeats beyond one pair,
# and 聴解問題5 (3 answers) landed on 3 DISTINCT positions in all 8 tests
# checked — both artifacts of the pre-R17 per-section-quota algorithm those
# tests were drawn under (see the "legacy_position_quota" marker below), but
# the leftover run-of-3 ban in THIS algorithm was independently pushing new
# draws toward the same suspiciously-even shape the R17 fix was supposed to
# remove. A run of 3 is real official behavior; a run of 4 has not been
# observed anywhere in the 31-sitting archive, so that is the cap now, not 3.
#
# PROVISIONAL BAND — retune, don't reinterpret. 90 four-choice items / 4 = 22.5,
# and ±4 is the working tolerance until the measured spread of the official
# papers (refs/JLPT_N2_NEW answer keys) replaces it. If that measurement
# disagrees, change these two numbers; the algorithm does not care what they are.
POSITION_BAND = (19, 27)
MAX_POSITION_RUN = 3   # longest same-position run allowed anywhere in the deck;
                       # see the note above — 3 is observed in the archive, 4 is not.

# --- Per-section MODE ceiling (F1, qa-report-20260818_1) -------------------
# The 2026-08-18 audit above examined only the too-SMOOTH tail: it asked whether
# our sections cluster as hard as official's, found they never did, and relaxed
# the run cap. Nothing ever looked at the other end, and there was no ceiling at
# all — so `20260818_1` drew 問題7 = [1,1,2,4,4,1,1,1,2,1,1,1], EIGHT of twelve
# keys on option 1, plus 問題4_語彙 with four of seven, and every gate stayed
# green. A globally balanced deck sliced in order does not bound a single
# slice's mode: the run cap only forbids ADJACENT repeats.
#
# The ceiling below is the MAXIMUM mode count observed per 大問 over all 31
# sittings in `refs/JLPT_N2_NEW/answer_keys.json`, measured only on the sittings
# whose item count for that 大問 equals today's (問題3 5→3, 問題9 5→4, 問題11
# 9→8, 聴解問題4 12→11 and 聴解問題5 4→3 all changed at 12/2022, and mixing eras
# inflates the ceiling — 聴解問題4 reads 7 across all 31 but 5 over the 18
# current-shape sittings). Re-derive it by re-measuring the archive, never by
# reading a paper. Measured 2026-08-19:
#
#   問1 3/5  問2 3/5  問3 2/3  問4 3/7  問5 3/5  問6 3/5  問7 5/12  問8 3/5
#   問9 2/4  問10 3/5  問11 4/8  問12 2/2  問13 2/3  問14 2/2
#   聴解問1 4/5  聴解問2 4/6  聴解問3 4/5  聴解問4 5/11  聴解問5 2/3
#
# This is a CEILING, not a target: 問題7's own distribution is mode 3 in 14
# sittings, 4 in 16 and 5 in exactly ONE, so a generator that authors to 5 every
# paper reproduces a shape official does not have (bunpou.md §問題7 documents the
# same failure on stem length). `balanced_position_plan()` rejects and reshuffles
# a plan that breaches it; `check_answer_position_section_clustering()` in
# tools/check_consistency.py fails a spec that does.
MAX_SECTION_MODE = {
    "問題1_語彙": 3, "問題2_語彙": 3, "問題3_語彙": 2, "問題4_語彙": 3,
    "問題5_語彙": 3, "問題6_語彙": 3, "問題7": 5, "問題8": 3, "問題9": 2,
    "問題10": 3, "問題11": 4, "問題12": 2, "問題13": 2, "問題14": 2,
    "聴解_問題1": 4, "聴解_問題2": 4, "聴解_問題3": 4, "聴解_問題4": 5,
    "聴解_問題5": 2,
}

# --- Per-section MODE DISTRIBUTION (R2-F8, qa-report-20260818_1-round2) -----
# The ceiling above is the right VALUE and the wrong INSTRUMENT on its own. It
# bounds the worst case and says nothing about the shape, and the shape was
# wrong in eight sections at once: slicing ONE globally balanced 90-item deck
# makes each section's mode multinomial, while official examiners balance
# WITHIN each 大問. Measured over 400 simulated plans against the era-matched
# archive, the old generator ran
#
#   問題3   official {1:92%, 2: 8%}          -> sampler {1:39%, 2:61%}
#   問題4   official {2:80%, 3:20%}          -> sampler {2:24%, 3:76%}  (inverted)
#   問題7   official {3:45%, 4:52%, 5: 3%}   -> sampler {3: 5%, 4:56%, 5:40%}
#   問題9   official {1:64%, 2:36%}          -> sampler {1:10%, 2:90%}
#   問題1/2/5/6/8 official {2:94-97%}        -> sampler {2:62-68%}
#   聴解問題4 official {4:61%, 5:39%}         -> sampler {4:40%, 5:60%}
#
# i.e. our slices were MORE clustered than any official sitting's distribution,
# while still (after the ceiling landed) never breaching the ceiling. Authoring
# to a ceiling reproduces a shape official does not have — the identical failure
# `bunpou.md` §問題7 documents for stem length.
#
# So the target is a DISTRIBUTION, applied by rejection sampling: each section's
# mode COUNT is drawn from the table below, then a random row is redrawn until it
# realises that count (`section_row()`), and the whole plan is redrawn until the
# global totals still sit inside `POSITION_BAND` and the deck still respects
# `MAX_POSITION_RUN` across section seams. Mode 5 in 問題7 stays reachable at its
# official 1-in-31 rate, which is the point of not lowering the ceiling.
#
# VALUES ARE SITTING COUNTS, not percentages — the measurement itself, so it can
# be re-derived and diffed. Measured 2026-08-19 from
# `refs/JLPT_N2_NEW/answer_keys.json`, era-matched exactly as MAX_SECTION_MODE
# is: only the sittings whose item count for that 大問 equals today's (hence
# n=31 for the unchanged sections and n=10..18 for the five that changed shape
# at 12/2022). Re-derive by re-measuring the archive, never by reading a paper.
SECTION_MODE_DIST = {
    "問題1_語彙": {2: 30, 3: 1},            # n=31
    "問題2_語彙": {2: 30, 3: 1},            # n=31
    "問題3_語彙": {1: 12, 2: 1},            # n=13
    "問題4_語彙": {2: 24, 3: 6},            # n=30
    "問題5_語彙": {2: 29, 3: 2},            # n=31
    "問題6_語彙": {2: 30, 3: 1},            # n=31
    "問題7": {3: 14, 4: 16, 5: 1},          # n=31
    "問題8": {2: 29, 3: 2},                 # n=31
    "問題9": {1: 7, 2: 4},                  # n=11
    "問題10": {2: 24, 3: 7},                # n=31
    "問題11": {2: 1, 3: 8, 4: 1},           # n=10
    "問題12": {1: 27, 2: 4},                # n=31
    "問題13": {1: 21, 2: 10},               # n=31
    "問題14": {1: 22, 2: 9},                # n=31
    "聴解_問題1": {2: 22, 3: 8, 4: 1},      # n=31
    "聴解_問題2": {2: 11, 3: 11, 4: 4},     # n=26
    "聴解_問題3": {2: 25, 3: 4, 4: 1},      # n=30
    "聴解_問題4": {4: 11, 5: 7},            # n=18
    "聴解_問題5": {1: 5, 2: 6},             # n=11
}

# The two tables are one measurement read two ways, so they cannot be allowed to
# drift: the ceiling IS the largest mode count the archive shows for that 大問.
# A mismatch means one of them was hand-edited instead of re-measured.
_MODE_TABLE_MISMATCH = {
    name: (MAX_SECTION_MODE.get(name), max(dist))
    for name, dist in SECTION_MODE_DIST.items()
    if MAX_SECTION_MODE.get(name) != max(dist)
}
assert not _MODE_TABLE_MISMATCH, (
    "MAX_SECTION_MODE disagrees with max(SECTION_MODE_DIST) for "
    f"{_MODE_TABLE_MISMATCH} — both are the same era-matched measurement of "
    "refs/JLPT_N2_NEW/answer_keys.json; re-measure, do not hand-edit either")
assert set(SECTION_MODE_DIST) == {n for n, _, _ in ANSWER_SECTIONS}, (
    "SECTION_MODE_DIST must cover exactly the sections in ANSWER_SECTIONS")


def shuffle_no_triple(rng: random.Random, base: list[int], name: str,
                      max_run: int = 2) -> list[int]:
    """Shuffle `base` until no position repeats more than `max_run` times running.

    `max_run` defaults to 2 (no 3-in-a-row), which is what the width-3 section
    (聴解問題4) uses. 4-choice sections pass `max_run=MAX_POSITION_RUN` (3) — see
    the note above `POSITION_BAND` for why a run of 3 is correct there and a run
    of 2 was not. Callers: `section_row()`, per section; the cross-seam run cap
    is `balanced_position_plan()`'s, on the assembled deck.
    """
    base = list(base)
    window = max_run + 1
    if len(set(base)) < 2 and len(base) >= window:
        # No arrangement can satisfy the run-length cap; fail loudly rather
        # than spin forever in the shuffle loop.
        sys.exit(f"shuffle_no_triple: impossible constraint for {name} "
                 f"({len(base)} items over {len(set(base))} position(s))")
    for _ in range(10_000):
        rng.shuffle(base)
        if all(len(set(base[i:i + window])) > 1
               for i in range(len(base) - window + 1)):
            return base
    sys.exit(f"shuffle_no_triple: no valid arrangement after 10000 shuffles "
             f"for {name} ({len(base)} items)")


POSITION_BAND_3 = (2, 6)   # per-position count band for width-3 draws (聴解
                           # 問題4, 11 items). Official's own count split is
                           # not an even quota — 7/2025 keys 3/5/3 over 11
                           # items, 12/2025 keys 4/4/3 — so a fixed
                           # floor(count/width) split, reshuffled or not,
                           # always reproduces the SAME per-position counts
                           # every draw (found 2026-08-18: every one of this
                           # repo's shipped 問題4 sections ran exactly 4/4/3,
                           # because the old `[(i % width) + 1 ...]` base list
                           # only ever gets reordered, never re-counted).


def section_max_run(width: int) -> int:
    """Longest same-position run allowed inside one section's own row.

    4-choice sections take `MAX_POSITION_RUN` (3, observed in the archive — see
    the note above `POSITION_BAND`). The width-3 section (聴解問題4) keeps the
    stricter cap of 2 it has always had: with only three positions a run of 3 is
    a much larger share of an 11-item row, and nothing in the archive shows one.
    """
    return 2 if width == 3 else MAX_POSITION_RUN


def sample_mode_target(rng: random.Random, name: str) -> int:
    """One section's mode COUNT, drawn from the official distribution (R2-F8)."""
    dist = SECTION_MODE_DIST[name]
    counts = sorted(dist)
    return rng.choices(counts, weights=[dist[c] for c in counts], k=1)[0]


def section_row(rng: random.Random, name: str, count: int,
                width: int) -> list[int]:
    """One section's answer positions, mode-matched to the archive (R2-F8).

    Draw the target mode count from `SECTION_MODE_DIST[name]`, then REJECTION
    SAMPLE independent rows until one realises exactly that count, then order it
    under the section's own run cap. Conditioning an i.i.d. row on its mode count
    is what keeps WHICH position is the mode uniform — the shape is calibrated,
    the identity of the clustered option stays unpredictable, which is the
    invariant §"Answer positions are balanced globally" owns.

    The rejection loop is cheap except where the target is the least likely
    row shape (問題7's mode 3 = a perfectly even 3/3/3/3 split, ~2 % of rows), so
    the bound is generous rather than tight.
    """
    target = sample_mode_target(rng, name)
    lo3, hi3 = POSITION_BAND_3
    for _ in range(50_000):
        row = [rng.randrange(1, width + 1) for _ in range(count)]
        if section_mode(row)[1] != target:
            continue
        if width == 3 and not all(lo3 <= row.count(p) <= hi3
                                  for p in range(1, width + 1)):
            continue
        return shuffle_no_triple(rng, row, f"{name} ({count}x{width})",
                                 max_run=section_max_run(width))
    sys.exit(f"section_row: no {count}x{width} row for {name} with mode count "
             f"{target} after 50000 draws — SECTION_MODE_DIST[{name}] offers a "
             f"count this section size cannot realise; re-measure the archive")


def section_mode(row: list[int]) -> tuple[int, int]:
    """(most-frequent position, how many times it occurs) in one section's row."""
    if not row:
        return (0, 0)
    counts = {p: row.count(p) for p in set(row)}
    pos = max(sorted(counts), key=lambda p: counts[p])
    return (pos, counts[pos])


def section_mode_breaches(plan: dict[str, list[int]]) -> list[str]:
    """Sections whose most-frequent position beats the archive ceiling (F1)."""
    out = []
    for name, row in plan.items():
        cap = MAX_SECTION_MODE.get(name)
        if cap is None:
            continue
        pos, cnt = section_mode(row)
        if cnt > cap:
            out.append(f"{name} {pos}x{cnt} of {len(row)} (official max {cap})")
    return out


def balanced_position_plan(rng: random.Random,
                           sections: list[tuple[str, int, int]]
                           ) -> tuple[dict[str, list[int]], dict[int, int]]:
    """Answer positions for every section: per-大問 shape, whole-paper balance.

    Two bars, and they pull in opposite directions:

    * **Globally balanced** — each position takes 19–27 of the 90 four-choice
      items (`POSITION_BAND`), and no position runs more than
      `MAX_POSITION_RUN` times anywhere in the paper, seams included. Never a
      per-section QUOTA: forcing every 4-item section to hold {1,2,3,4} is what
      made small sections predictable (R17).
    * **Per-section SHAPE drawn from the archive** — each section's row is built
      by `section_row()`, whose mode count comes from `SECTION_MODE_DIST` and is
      realised by rejection sampling. Until 2026-08-19 the rows were slices of
      one shuffled global deck, which made every section's mode multinomial and
      left eight sections measurably MORE clustered than any official
      distribution (R2-F8) — the ceiling below caught only the extreme tail
      (`20260818_1`'s 問題7 = 8 of 12 on option 1, F1).

    Rows are built first, the paper is checked second, and the whole plan is
    redrawn if the global band or the cross-seam run cap fails. `MAX_SECTION_MODE`
    is re-verified at the end as a belt: it holds by construction now (every
    drawable target is a count the archive actually shows), and a breach here
    would mean the two tables have drifted apart.
    """
    lo, hi = POSITION_BAND

    for _ in range(2000):
        plan = {name: section_row(rng, name, count, width)
                for name, count, width in sections}
        deck = [p for name, _, width in sections if width == 4
                for p in plan[name]]
        running = {p: deck.count(p) for p in (1, 2, 3, 4)}
        if not all(lo <= running[p] <= hi for p in running):
            continue
        # The run cap is a property of the PAPER, not of a section: a row that
        # ends 4,4 followed by a row that opens 4,4 is a run of four nobody
        # measured while the deck was shuffled as one list.
        window = MAX_POSITION_RUN + 1
        if any(len(set(deck[i:i + window])) == 1
               for i in range(len(deck) - window + 1)):
            continue
        if section_mode_breaches(plan):
            continue
        return plan, running

    sys.exit("balanced_position_plan: no plan satisfying SECTION_MODE_DIST, "
             f"{POSITION_BAND} and MAX_POSITION_RUN after 2000 attempts — "
             "re-measure both tables against refs/JLPT_N2_NEW/answer_keys.json "
             "rather than widening a band")


# --- Ledger (v2): draw history, newest last ------------------------------
# v1 was a flat {category: [used items]} with an all-or-nothing reset — when a
# pool ran out, the ENTIRE history cleared, so an item from the immediately
# previous test could reappear in the very next one. v2 keeps per-draw history
# so rotation is LRU (least-recently-used) and degrades smoothly instead of
# resetting, and so each item can be attributed to the test that used it.

COOLDOWN_FLOOR = 2   # minimum cooldown even for the thinnest pool
COOLDOWN_MARGIN = 2  # draws of headroom left below full pool exhaustion, so
                     # the existing "relax one step when tight" path below
                     # still has room to degrade smoothly instead of jumping
                     # straight from a long cooldown to 0


def cooldown_for(cat: str, pool_size: int) -> int:
    """How many previous draws make an item in `cat` ineligible.

    A single flat COOLDOWN=2 protected every category as weakly as the
    thinnest one: word_formation's 85-entry pool (3 drawn/test, ~28 tests to
    exhaust) rotated no better than grammar_p8's 42-entry pool (5/test, ~8
    tests to exhaust) — proven when `〜好き(猫好き)` and `〜化(簡素化)` each
    repeated within 4-5 tests despite a pool deep enough to go ~28 tests
    without a repeat. Scale the window to each pool's OWN depth instead of a
    constant: a rich pool remembers for a long time, a tight one for less,
    and COOLDOWN_MARGIN keeps every pool's window a little short of full
    exhaustion so it can still relax gracefully (see `draw()`) rather than
    jump straight to cool=0 the moment the pool grows by a handful of items.
    """
    n = DRAW[cat]
    depth = pool_size // n if n else 0
    return max(COOLDOWN_FLOOR, depth - COOLDOWN_MARGIN)


def carry_legacy(old: dict | None, new_items: list, fresh: dict) -> dict:
    """Rebuild a spec's `rotation` block across a reroll WITHOUT losing what it
    already proved, or claiming what it never did.

    Both reroll paths used to replace this block wholesale, which silently
    dropped `legacy`/`legacy_note` — and a legacy spec's marker is the only
    record that its OTHER categories were drawn before the gate checked each
    category against its own `cooldown_for()` window. Dropping it made the spec
    claim a rotation proof it does not have, and `check_spec_rotation` then
    correctly FAILed on pre-existing legacy repeats in categories the reroll
    never touched (found across 13 papers during the 2026-08-21 文字・語彙 pass).

    The other half is the honest converse: the ENTRIES just drawn ARE proved,
    against the current window, by `assert_rotation()` at draw time — so they
    join `verified_items` and the gate checks exactly those. The unit is the
    entry, not the category: on the `--reroll-one` path the category's KEPT
    entries are still older draws against an older window, which is the same
    reason this file scopes its own post-draw check to `{cat: picked}`. A legacy
    exemption is therefore a queue that shrinks one drawn item at a time, not an
    amnesty for the whole paper.
    """
    out = dict(fresh)
    old = old or {}
    if old.get("legacy"):
        out["legacy"] = True
        if old.get("legacy_note"):
            out["legacy_note"] = old["legacy_note"]
    verified = list(old.get("verified_items") or [])
    for x in new_items:
        t = item_text(x)
        if t not in verified:
            verified.append(t)
    out["verified_items"] = sorted(verified)
    return out


def load_staging_ready() -> dict[str, list[dict]]:
    """category -> staging rows with status=ready and level=N2."""
    if not STAGING.is_file():
        return {}
    data = json.loads(STAGING.read_text(encoding="utf-8"))
    by_cat: dict[str, list[dict]] = {}
    for e in data.get("entries", []):
        if e.get("status") != "ready" or e.get("level") != "N2":
            continue
        cat = e.get("category")
        if cat:
            by_cat.setdefault(cat, []).append(e)
    return by_cat


def apply_adjunct(rng: random.Random, cat: str, picked: list,
                  staging_by_cat: dict[str, list[dict]], taken: set,
                  recency: dict, cool_max: int) -> list:
    """Replace up to ADJUNCT_CAP of pool draws with staged N2 adjunct items."""
    n = len(picked)
    cap = int(n * ADJUNCT_CAP)
    if cap < 1:
        return picked
    pool = staging_by_cat.get(cat, [])
    if not pool:
        return picked

    inf = 10 ** 9

    def ago(x: str) -> int:
        return min(recency.get(x, inf), recency.get(head(x), inf))

    eligible = []
    for e in pool:
        it = e.get("item", "")
        if not it or it in taken or head(it) in {head(t) for t in taken}:
            continue
        if ago(it) < cool_max:      # used within this category's cooldown
            continue
        eligible.append(e)
    if not eligible:
        return picked

    rng.shuffle(eligible)
    replace_n = min(cap, len(eligible))
    result = list(picked[: n - replace_n])
    for e in eligible[:replace_n]:
        result.append({
            "item": e["item"],
            "origin": "adjunct",
            "level": "N2",
            "evidence": e.get("evidence", []),
        })
        taken.add(e["item"])
    print(f"  note: {cat} used {replace_n} adjunct item(s) from staging")
    return result


def pools_sha() -> str:
    """First 12 hex digits of sha1 over `pools.json`'s raw bytes (R7).

    A recorded SEED is only replayable against the pool it was drawn from.
    `draw()` consumes a fixed number of RNG values per category, so removing one
    entry changes WHICH items are picked without shifting the stream — the later
    categories realign perfectly and the earlier ones silently do not. That is
    exactly what happened to `20260818_1`: its recorded seed reproduced 6 of 11
    categories after `pools.json` changed four hours later, and the reviewer had
    to infer the intermediate pool state from commit timestamps
    (qa-report-20260818_1 §6.1, R7). Stamping the pool revision makes
    "is this spec genuine?" answerable by replay instead of by inference.

    Same 12-hex convention as `script_sha`/`pacing_sha` (`choukai-audio`).
    Specs written before 2026-08-19 carry no stamp; the gate reports that as a
    skip, never a failure — an unstamped spec is old, not wrong.
    """
    return hashlib.sha1(POOLS.read_bytes()).hexdigest()[:12]


def load_ledger() -> dict:
    if not LEDGER.exists():
        return {"version": 2, "history": []}
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    if data.get("version") == 2:
        return data
    # migrate v1 flat lists -> one synthetic oldest draw
    legacy = {k: v for k, v in data.items() if isinstance(v, list)}
    print("  note: migrating ledger v1 -> v2 (history-based LRU rotation)")
    return {"version": 2,
            "history": [{"test_id": "legacy", "seed": None,
                         "generated_at": None, "items": legacy}] if legacy else []}


def head(item: str) -> str:
    """Normalized identity of a pool entry, ignoring the disambiguating gloss.

    Pools spell the same word differently per category — 「あらかじめ」 in
    context_words, 「あらかじめ(前もって)」 in paraphrase — so a raw string
    comparison misses cross-category repeats.
    """
    return str(item).split("(")[0].split("（")[0].strip()


# --- errand identity (R14, 2026-08-19) -----------------------------------
# The cooldown used to compare DISPLAY STRINGS, so three pool entries spelling
# one errand three ways (`引越し:見積もり` / `引っ越し業者との見積もり調整` /
# `引っ越し業者との調整`) were three separate items to it, and two of them went
# out in consecutive papers with every gate green (qa-report-20260817_3 F6).
# `pools.json` now carries an optional `key` on those entries — the institution
# and errand — and everything that decides "have we used this recently" resolves
# it through `errand_key()` first. The duplicate ENTRIES stay: four shipped
# tests name them in logs/ledger.json and check_draw_provenance() requires every
# recorded draw to resolve to a pool entry, so deleting them would break the
# gate on papers that are already out.
#
# Key tokens live in their own namespace so a key can never be confused with a
# pool string in the recency/taken maps.
KEY_NS = "key»"
_KEY_BY_TEXT: dict[str, str] = {}


def build_key_index(pools: dict) -> dict[str, str]:
    """display string -> errand key, for every pool entry that carries one.

    `quick_response` entries are bare strings, so their keys live in a separate
    top-level `quick_response_keys` map instead of on the entry (F4,
    qa-report-20260818_1): making them objects would orphan every recorded draw
    in `logs/ledger.json`, which `check_draw_provenance()` resolves by string.
    Clustering was `listening_scenarios`/`reading_topics`-only until 2026-08-19,
    so `20260818_1` drew BOTH 「…お名前とご連絡先をご記入いただけますでしょうか」
    and 「キャンセル待ちの方は、こちらに名前をお書きください」 — two 問題4 items
    running one errand (write your name at a counter), an automatic QA fail that
    nothing upstream could see. With the map in place `draw()`'s cross-key
    `taken` exclusion prevents the pair by construction.
    """
    idx: dict[str, str] = {}
    for cat in THEMED_CATS:
        for e in pools.get(cat, []):
            k = entry_key(e)
            if k:
                idx[item_text(e)] = k
    for text, k in (pools.get("quick_response_keys") or {}).items():
        if isinstance(k, str) and k.strip():
            idx[str(text)] = k
    return idx


def errand_key(entry) -> str | None:
    """The entry's errand key, from the entry itself or from the pool index.

    Ledger and spec rows record `{"scenario": …, "theme": …}` with no `key`, so
    recorded history has to be resolved through the index built off the current
    pool — that is what makes the rule retroactive over the draws already made.
    """
    return entry_key(entry) or _KEY_BY_TEXT.get(item_text(entry))


def affix_marker_free(t: str) -> str:
    """`内〜(国内)` and `〜内(国内)` are one item under two notations, or ''.

    Only for the `word_formation` shape — an affix marker OUTSIDE a
    parenthetical gloss. `pools.json` corrected 「内〜(国内)」 to 「〜内(国内)」
    (qa-report-20260817_3-round3 R3-2) and without this the corrected string
    would look like an item nothing has ever drawn, so its cooldown would
    restart. Grammar entries whose 〜 sits inside the gloss (`相対比較(〜ば〜ほど)`)
    are excluded: folding those would collide short kana tails across the pool.
    """
    if "(" not in t and "（" not in t:
        return ""
    if not re.search(r"[〜～]", re.split(r"[(（]", t)[0]):
        return ""
    return t.replace("〜", "").replace("～", "")


# --- grammar FORM identity: 問題7 and 問題8 are ONE rotation space (F1, 2026-08-20)
# `grammar_p7` spells a point bare (`〜のみならず`) and `grammar_p8` spells the
# same point as a 類型-labelled pattern (`限定表現(〜のみならず…も)`). Neither the
# raw string nor `head()` folds those together — `head()` splits on the first
# paren, so the p8 entry's identity is the LABEL 「限定表現」 — so the two
# categories rotated independently and 13 forms listed in both pools could go out
# one paper apart with every gate green.
#
# THE INCIDENT: `20260819_1` drew `限定表現(〜のみならず…も)` and
# `変化推移(〜につれて…ていく)` into 問題8 after `20260818_1` — the IMMEDIATELY
# previous paper — had KEYED 〜のみならず and 〜につれて in its 問題7
# (qa-report-20260819_1 F1). Measured over the whole ledger the day this landed:
# **9 of 14 papers** leak p7↔p8 inside the drawing category's own cooldown window.
#
# The token is the FORM, not the entry: strip the 類型 wrapper when it holds the
# 〜-marked pattern, then cut on 「…」/「・」/「〜」 and keep the chunks of
# GRAMMAR_FORM_MIN+ characters. Short tails (〜上, 〜がち, 〜きり) produce no token
# and keep their ordinary string cooldown — form tokens only ever ADD identity.
GRAMMAR_FORM_CATS = ("grammar_p7", "grammar_p8")
GRAMMAR_FORM_NS = "form»"
GRAMMAR_FORM_MIN = 3        # 「わりに」 is the shortest dual-listed form; 2 would
                            # collide kana tails across unrelated points
_GRAMMAR_FORM_ENTRY = re.compile(r"^(?P<label>[^(（]*)[(（](?P<inner>.+)[)）]\s*$")


def grammar_form_parts(entry) -> list[str]:
    """The entry's FORM, label stripped, cut into its chunks IN ORDER.

    `限定表現(〜のみならず…も)` -> `['のみならず', 'も']`; `〜に基づいて` ->
    `['に基づいて']`; `理由説明(〜のは…からだ)` -> `['のは', 'からだ']`; a word
    entry with no 〜 marker -> `[]`.

    Order is kept because a discontinuous pattern is only that pattern when its
    chunks occur in order — `check_key_grammar_exposure()` matches the whole
    skeleton (「のは…からだ」), not one chunk of it, and a set could not express
    that. `grammar_form_tokens()` below is this list filtered and namespaced, so
    the two can never disagree about what the FORM of an entry is.
    """
    t = item_text(entry)
    if not re.search(r"[〜～]", t):
        return []           # the 〜 marker IS the grammar/affix entry signature;
                            # without it this is a word, and head() already folds
                            # words across categories
    m = _GRAMMAR_FORM_ENTRY.match(t)
    inner = (m.group("inner") if m and re.search(r"[〜～]", m.group("inner"))
             else re.split(r"[(（]", t)[0])
    return [p for p in (q.strip(" 　、。") for q in re.split(r"[…・〜～~]", inner))
            if p]


def grammar_form_tokens(entry) -> set[str]:
    """The grammar FORMS an entry tests, namespaced, for cross-category recency.

    `限定表現(〜のみならず…も)` -> {`form»のみならず`}; `〜のみならず` -> the same
    token, which is the whole point. `〜しかない・よりほかない` -> both halves.
    `〜上(で)` -> {} (the gloss carries no 〜, and 「上」 is one character).
    """
    return {GRAMMAR_FORM_NS + p for p in grammar_form_parts(entry)
            if len(p) >= GRAMMAR_FORM_MIN}


def identity_tokens(entry) -> set[str]:
    """Every token that makes this entry 'the same item' for RECENCY."""
    t = item_text(entry)
    toks = {t, head(t)} - {""}
    flat = affix_marker_free(t)
    if flat:
        toks |= {flat, head(flat)}
    k = errand_key(entry)
    if k:
        toks.add(KEY_NS + k)
    toks |= grammar_form_tokens(entry)
    return toks


def taken_tokens(entry) -> set[str]:
    """The in-test exclusion tokens: the display string, the errand key, the form.

    Deliberately NOT head() — cross-category head folding is recency's job
    (`recency_map`), and widening the in-test set would change draws that have
    nothing to do with the errand-key defect this was added for.

    The grammar FORM token is the exception, and it is here for the same reason
    it is in `identity_tokens()`: 問題7 and 問題8 draw from two pools that list 15
    forms in common, so without it one paper could key 〜のみならず at 問題7 and
    build its 問題8 frame on 限定表現(〜のみならず…も) — 「one grammar point may be
    the KEY only once per paper」 (question-authoring Item integrity #15) with
    nothing able to see it (F1).
    """
    t = item_text(entry)
    k = errand_key(entry)
    return (({t} if t else set()) | ({KEY_NS + k} if k else set())
            | grammar_form_tokens(entry))


def recency_map(history: list) -> dict:
    """item -> how many draws ago it was last used (0 = most recent draw).

    Recency is tracked BY WORD, ACROSS CATEGORIES, not per category. Pools
    overlap on purpose (41 words are both context_words and usage items), and
    a category-local map let 「あらかじめ」 be tested in one paper's 問題4 and
    again in the next paper's 問題5 — consecutive papers testing the same word,
    with every gate green. `taken` stops that inside one test; this stops it
    across tests.
    Keys are the raw string, its head(), and — for a themed entry whose pool row
    carries one — its `KEY_NS`-prefixed errand key, so an errand that the pool
    spells three ways cools down once (see `errand_key`).
    """
    rec: dict = {}
    for ago, entry in enumerate(reversed(history)):
        for items in entry.get("items", {}).values():
            for item in items:
                for tok in identity_tokens(item):
                    rec.setdefault(tok, ago)
    return rec


def sample_distinct_theme(rng: random.Random, eligible: list, n: int,
                          name: str, weight_fn=None) -> list | None:
    """`n` entries, no two sharing a theme. None when the pool cannot.

    Greedy over a shuffle, which is uniform enough for this purpose and, unlike
    rejection sampling over `rng.sample`, terminates: the caller only needs SOME
    theme-distinct draw, not a uniformly-random one among all such draws.
    Untagged entries are treated as one shared theme so a category that lost its
    tags degrades to "one untagged entry", never to "distinctness is vacuous".

    `weight_fn`, when given, orders the shuffle by recency weight (see
    `weighted_sample_no_replacement`) so the greedy pass still favors
    longer-unused entries, not just a plain shuffle.
    """
    if weight_fn:
        shuffled = weighted_sample_no_replacement(
            rng, eligible, [weight_fn(e) for e in eligible], len(eligible))
    else:
        shuffled = list(eligible)
        rng.shuffle(shuffled)
    picked, used = [], set()
    for e in shuffled:
        th = entry_theme(e) or ""
        if th in used:
            continue
        picked.append(e)
        used.add(th)
        if len(picked) == n:
            return picked
    print(f"  warning: pool '{name}' cannot fill {n} distinct themes "
          f"({len(picked)} available) — falling back to a themed draw; grow "
          f"the thin themes rather than relaxing the rule")
    return None


def draw(rng: random.Random, pool: list, recency: dict, n: int,
         name: str, taken: set, cool_max: int,
         kept: list | tuple = ()) -> tuple[list, int]:
    """LRU draw. Returns (picked, cooldown_actually_applied).

    `cool_max` is this category's own cooldown ceiling (`cooldown_for()`) —
    a number of PREVIOUS DRAWS: at cool=cool_max nothing used in the last
    cool_max ledger entries can be drawn (ago 0 .. cool_max-1 excluded),
    which is what the docstring, the SKILL and `rotation.cooldown` all promise.
    The old test was `ago(x) > cool`, i.e. one draw stricter than documented —
    harmless in itself, but it meant the number written into the spec was not
    the number enforced, and a gate cannot check a promise nobody records.

    Relaxation is not silent any more either. cool=0 is the old "last resort"
    (no recency filter at all) and it is a value the caller RETURNS and records,
    so a paper drawn without rotation says so in its own spec instead of only
    in a console line nobody kept.

    `kept` is the entries of this same category the caller is KEEPING (nonzero
    only on the `--reroll-one` path). Nothing but the mix caps read it: a
    one-entry redraw must not be able to push the paper past a per-paper ceiling
    the full draw respects.
    """
    if len(pool) < 2.5 * n:
        print(f"  warning: pool '{name}' is thin ({len(pool)} for draws of {n}) "
              f"— consider adding items from the reference books")
    inf = 10 ** 9

    def ago(x) -> int:
        # Every identity token, not just the display string: an entry whose
        # errand key was drawn recently is as recently used as the entry that
        # drew it, however differently the pool spells the two (R14).
        return min((recency.get(tok, inf) for tok in identity_tokens(x)),
                   default=inf)

    def weight(x) -> float:
        # +1 so an item sitting right at the cooldown boundary (ago == cool,
        # the minimum eligible) never gets a zero/negative weight; everything
        # past that is weighted by how much LONGER it's gone unused, so a
        # draw does not cluster right at the boundary the moment it clears.
        return float(ago(x)) + 1.0

    for cool in range(cool_max, -1, -1):
        eligible = [x for x in pool
                    if not (taken_tokens(x) & taken) and ago(x) >= cool]
        if len(eligible) >= n:
            if cool == 0:
                print(f"  WARNING: pool '{name}' exhausted its rotation — "
                      f"drawing with NO cooldown. Grow this pool.")
            elif cool < cool_max:
                print(f"  note: pool '{name}' is tight — cooldown relaxed to "
                      f"{cool} draw(s) (of {cool_max}); consider growing the pool")
            if name in DISTINCT_THEME_CATS:
                picked = sample_distinct_theme(rng, eligible, n, name,
                                               weight_fn=weight)
                if picked is not None:
                    return picked, cool
            if name in KATAKANA_CAP:
                return sample_katakana_capped(
                    rng, eligible, n, KATAKANA_TARGET_RATE[name],
                    KATAKANA_CAP[name], name, weight_fn=weight), cool
            if name in KUN_CAP:
                return sample_kun_capped(
                    rng, eligible, n, KUN_TARGET_RATE[name], KUN_CAP[name],
                    name, already=sum(1 for x in kept if is_kun_target(x)),
                    weight_fn=weight, floor=KUN_FLOOR.get(name, 0)), cool
            if name in WAGO_FLOOR:
                return sample_wago_floor(
                    rng, eligible, n, WAGO_FLOOR[name], COMPOUND_CAP[name],
                    name, kept=kept, weight_fn=weight,
                    dist=WAGO_DIST.get(name)), cool
            return weighted_sample_no_replacement(
                rng, eligible, [weight(x) for x in eligible], n), cool
    remaining = len([x for x in pool if item_text(x) not in taken])
    sys.exit(f"pool '{name}' cannot supply {n} distinct items "
             f"({remaining} available after cross-category exclusion)")


COMMON_DOMAINS = [
    "会社", "大学", "病院", "不動産", "旅行", "市役所", "区役所", "図書館",
    "引っ越し", "ホテル", "アルバイト", "ジム", "駅", "美術館", "学校", "スーパー",
    "レストラン", "カフェ", "公園", "警察", "消防", "郵便局", "銀行", "防災",
]


def extract_domain(text: str) -> str:
    """Extract domain prefix or key entity from a scenario/topic string."""
    t = item_text(text)
    if ":" in t:
        return t.split(":")[0].strip()
    if "：" in t:
        return t.split("：")[0].strip()
    for d in COMMON_DOMAINS:
        if d in t:
            return d
    return ""


def check_domain_collisions(scenarios: list) -> list[str]:
    """Find pairs of scenarios sharing the same domain prefix/entity."""
    warnings = []
    seen: dict[str, list[str]] = {}
    for item in scenarios:
        d = extract_domain(item)
        if d:
            seen.setdefault(d, []).append(item_text(item))
    for dom, items in seen.items():
        if len(items) > 1:
            warnings.append(f"domain '{dom}': {items}")
    return warnings


def check_pool_themes(pools: dict) -> None:
    """R13: every themed pool entry carries a theme from the CLOSED vocabulary.

    Hard failure, not a warning. `expand_pools.py` and `promote_adjunct.py`
    still append bare strings to these categories, so without this the theme
    coverage silently rots the first time either runs, and the cross-test theme
    comparison the tags exist for goes quiet instead of red.
    """
    bad = []
    for cat, key in THEMED_CATS.items():
        for e in pools.get(cat, []):
            if not isinstance(e, dict) or not e.get(key):
                bad.append(f"{cat}: {e!r} is not {{'{key}': …, 'theme': …}}")
            elif e.get("theme") not in THEMES:
                bad.append(f"{cat}: 「{e[key]}」 theme={e.get('theme')!r}")
    if bad:
        sys.exit("pools.json themed entries are broken:\n  " +
                 "\n  ".join(bad) +
                 f"\n  valid themes: {', '.join(THEMES)}"
                 "\n  (exam-blueprint/SKILL.md §'Topic themes' — tag the "
                 "entry, never widen the vocabulary to fit it)")


def report_key_clusters(pools: dict) -> None:
    """Print the errand-key clusters so pool depth is not read off len(pool).

    A cluster of 3 entries sharing one `key` is ONE drawable errand, not three:
    after this change the cooldown treats them as one, so `cooldown_for()`'s
    headroom arithmetic is optimistic by (cluster size − 1) per cluster. Not a
    failure — the clusters are deliberate, and merging them away is what
    `check_draw_provenance()` forbids (see `errand_key`) — but it must be
    visible at draw time.
    """
    clusters: dict[str, list[str]] = {}
    for cat in THEMED_CATS:
        for e in pools.get(cat, []):
            k = entry_key(e)
            if k:
                clusters.setdefault(f"{cat}/{k}", []).append(item_text(e))
    for text, k in (pools.get("quick_response_keys") or {}).items():
        clusters.setdefault(f"quick_response/{k}", []).append(str(text))
    dupes = {k: v for k, v in clusters.items() if len(v) > 1}
    if not dupes:
        return
    extra = sum(len(v) - 1 for v in dupes.values())
    print(f"  note: {len(dupes)} errand-key cluster(s) cover {extra} duplicate "
          f"pool entr(ies) — they cool down as ONE item each (R14). "
          f"Effective depth is len(pool) − {extra}.")


def check_theme_spread(picked: list, cat: str) -> list[str]:
    """Warn when one theme takes too much of a themed draw.

    Surface strings cannot see that 「交替制勤務と睡眠の質」 and 「就寝前の刺激と
    生活習慣」 are one subject; the tags can. The sampler does not know which
    entry the author will map to which 問題, so this warns rather than rerolls.
    """
    cap = THEME_CAP.get(cat)
    if not cap:
        return []
    counts: dict[str, list[str]] = {}
    for e in picked:
        th = entry_theme(e)
        if th:
            counts.setdefault(th, []).append(item_text(e))
    return [f"theme '{th}' x{len(xs)} (cap {cap}): {xs}"
            for th, xs in counts.items() if len(xs) > cap]


def assert_rotation(spec_items: dict, history: list, pools: dict) -> None:
    """R10 proof: nothing drawn may appear inside ITS OWN category's cooldown
    window (`cooldown_for(cat, len(pools[cat]))`) — never a single spec-wide
    scalar. `spec["rotation"]["cooldown"]` records only the WEAKEST cooldown
    any category relaxed to (documented as such), so checking every category
    against that one number under-checks every category deeper than the
    thinnest one: a thin category relaxing to 2 made this check accept a
    kanji_reading item (real window ~300 draws, 305x headroom) repeating only
    7 draws back. `20260817_1` shipped exactly that — a hand-substitution
    during QA that never went through `--reroll`, so this check never even
    ran on it, and would have passed it anyway under the old single-scalar
    form. Fixed 2026-08-17 (see exam-blueprint SKILL.md 'Rotation model').
    """
    if not history:
        return
    clashes = []
    for cat, xs in spec_items.items():
        cool = cooldown_for(cat, len(pools.get(cat, [])))
        if cool <= 0:
            continue
        recent: dict[str, str] = {}
        for entry in history[-cool:]:
            tid = str(entry.get("test_id"))
            for cat_items in entry.get("items", {}).values():
                for x in cat_items:
                    for tok in identity_tokens(x):
                        recent.setdefault(tok, tid)
        for x in xs:
            t = item_text(x)
            tid = next((recent[tok] for tok in identity_tokens(x)
                        if tok in recent), None)
            if tid:
                clashes.append(f"{cat}:「{t}」 (test {tid}, needs its own "
                                f"{cool}-draw cooldown)")
    if clashes:
        sys.exit(f"rotation broken: {len(clashes)} item(s) drawn inside their "
                 f"own category's cooldown window: {'; '.join(clashes)} — "
                 f"this is a bug in draw(), not a reason to lower "
                 f"cooldown_for()")


def check_pool_depths(pools: dict) -> None:
    """Report pool sizes and headroom multipliers against draw requirements."""
    print("Pool Depth Health Check:")
    for cat, n in DRAW.items():
        size = len(pools.get(cat, []))
        ratio = size / n if n > 0 else 0
        status = "OK" if ratio >= 2.5 else "THIN"
        print(f"  [{status:4s}] {cat:20s}: {size:4d} items / {n:2d} draw ({ratio:5.1f}x headroom)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--reroll", default=None,
                    help="resample only this category, keep the rest")
    ap.add_argument("--reroll-one", default=None, metavar="CAT:INDEX",
                    help="resample ONE entry of a category, keep the other "
                         "entries and every other category "
                         "(e.g. --reroll-one quick_response:8)")
    ap.add_argument("--test-id", required=True,
                    help="test id; writes tests/<test_id>/test_spec.json and "
                         "records ledger attribution")
    ap.add_argument("--no-adjunct", action="store_true",
                    help="pure pool draw; ignore logs/adjunct_staging.json")
    ap.add_argument("--check-depth", action="store_true",
                    help="check pool sizes and headroom multipliers without sampling")
    args = ap.parse_args()

    pools = json.loads(POOLS.read_text(encoding="utf-8"))
    check_pool_themes(pools)
    # Built once, read by errand_key() everywhere below (R14). It has to exist
    # before the first recency_map() call, or history resolves without keys.
    global _KEY_BY_TEXT
    _KEY_BY_TEXT = build_key_index(pools)
    report_key_clusters(pools)

    if args.check_depth:
        check_pool_depths(pools)
        return

    if args.reroll and args.reroll_one:
        sys.exit("--reroll and --reroll-one are alternatives: the first redraws "
                 "a whole category, the second one entry of one")

    seed = args.seed if args.seed is not None else int(time.time())
    rng = random.Random(seed)
    spec_path = ROOT / "tests" / str(args.test_id) / "test_spec.json"

    ledger = load_ledger()
    history = ledger["history"]
    staging_by_cat = {} if args.no_adjunct else load_staging_ready()
    recency = recency_map(history)

    if args.reroll:
        cat = args.reroll
        if cat not in DRAW:
            sys.exit(f"unknown category '{cat}'. Valid: {', '.join(DRAW)}")
        if cat not in pools:
            sys.exit(f"category '{cat}' is in DRAW but missing from pools.json")
        if not spec_path.is_file():
            sys.exit(f"--reroll needs an existing {spec_path.relative_to(ROOT)}")
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        # Find THIS test's ledger entry by id — it is not necessarily the newest
        # one. An earlier test has been rerolled after a later test already
        # existed, and writing to history[-1] put the earlier test's picks into
        # the later test's entry, which then failed assert_rotation against
        # them. Drop this category from the entry so its own picks are not
        # counted against the redraw, and exclude everything the other
        # categories already hold.
        own_entry = None
        for e in reversed(history):
            if (str(e.get("test_id")) == str(spec.get("test_id")) or
                    str(e.get("seed")) == str(spec.get("seed"))):
                own_entry = e
                break
        if own_entry is not None:
            own_entry.setdefault("items", {}).pop(cat, None)
        taken_text = {tok for c, xs in spec["items"].items()
                      if c != cat for x in xs for tok in taken_tokens(x)}
        # THIS TEST'S OWN ENTRY LEAVES THE HISTORY, not just its rerolled
        # category (F1 fix pass, 2026-08-20). Popping the category alone left
        # the entry occupying a slot, so every `ago` draw() measured was one
        # SHALLOWER than the window `assert_rotation()` then proved against
        # (it drops the whole entry via `prior_history`). A reroll could
        # therefore pick an item exactly `cool` draws back, draw() would
        # accept it and assert_rotation() would abort on it — which is what
        # `--reroll-one grammar_p8:0` did on the first attempt at this repair
        # (「目的結果(〜ために…なった)」, drawn by 20260813_2 six draws back).
        # The kept entries stay excluded through `taken_text` below, which is
        # an in-test collision guard, not cooldown history.
        updated_recency = recency_map([h for h in history
                                       if h is not own_entry])
        cool_max = cooldown_for(cat, len(pools[cat]))
        picked, cool = draw(rng, pools[cat], updated_recency,
                            DRAW[cat], cat, taken_text, cool_max)
        if staging_by_cat:
            picked = apply_adjunct(rng, cat, picked, staging_by_cat,
                                   taken_text, updated_recency, cool_max)
        spec["items"][cat] = picked
        spec["seed"] = f"{spec.get('seed')}+reroll({cat},{seed})"
        # R7: a reroll re-draws against the CURRENT pool, so the stamp moves
        # with it — the spec records the revision the newest draw used.
        spec["pools_sha"] = pools_sha()
        spec["rotation"] = carry_legacy(spec.get("rotation"), picked, {
            "recency_source": "ledger",
            "history_len": 0,          # filled in below, once this test's own
                                       # entry can be told from the others
            # a reroll can only make the paper's weakest cooldown weaker
            "cooldown": min(cool, spec.get("rotation", {}).get("cooldown", cool)),
        })
        if own_entry is not None:
            own_entry.setdefault("items", {})[cat] = picked
            own_entry["seed"] = spec["seed"]
            own_entry["pools_sha"] = spec["pools_sha"]
        for w in check_theme_spread(picked, cat):
            print(f"  WARNING: {cat} draw is theme-heavy — {w}")
        # Only THIS category was freshly drawn — against "now" (the full
        # ledger's current end, via updated_recency above). Every other
        # category in spec["items"] is untouched, drawn at some earlier point
        # against whatever window existed then. Re-verifying the WHOLE spec
        # here compares old, already-valid picks against a "last cooldown
        # entries of right now" window that has nothing to do with when they
        # were drawn — for a test rerolled after later tests already exist,
        # that window is the tail of the ENTIRE ledger, not the entries that
        # preceded this test, and spuriously fails on categories the reroll
        # never touched (reproduces even at the old flat COOLDOWN=2). Verify
        # only what actually changed.
        rotation_check_items = {cat: picked}
    elif args.reroll_one:
        # --- single-entry reroll (R2-F2, 2026-08-19) ------------------------
        # `--reroll <cat>` was the only redraw available, and for `quick_response`
        # it replaces all ELEVEN stimuli — a whole-問題4 re-author plus an MP3
        # rebuild — to repair one drawn entry. That cost is what invited the
        # cheaper wrong repair: `20260818_1` drew two 「窓口:記名依頼」 stimuli
        # (問題4-2番 + 4-9番, an automatic QA fail) and the fix pass re-angled one
        # item's invented SETTING instead of redrawing the errand, which is not
        # what the rule measures (qa-report-20260818_1-round2 R2-F2). One entry
        # out, one entry in, under exactly the same exclusions as a full reroll:
        # this test's other picks (all categories, INCLUDING this category's kept
        # entries) via `taken`, and the category's own cooldown window via
        # `recency`. Recorded in the seed expression the way the other rerolls
        # are, so the draw stays replayable and check_draw_provenance() resolves.
        spec_of = args.reroll_one.rsplit(":", 1)
        if len(spec_of) != 2 or not spec_of[1].lstrip("-").isdigit():
            sys.exit(f"--reroll-one takes <category>:<index>, got "
                     f"'{args.reroll_one}' (e.g. quick_response:8)")
        cat, idx = spec_of[0], int(spec_of[1])
        if cat not in DRAW:
            sys.exit(f"unknown category '{cat}'. Valid: {', '.join(DRAW)}")
        if cat not in pools:
            sys.exit(f"category '{cat}' is in DRAW but missing from pools.json")
        if not spec_path.is_file():
            sys.exit(f"--reroll-one needs an existing {spec_path.relative_to(ROOT)}")
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        current = (spec.get("items") or {}).get(cat) or []
        if not -len(current) <= idx < len(current):
            sys.exit(f"--reroll-one {cat}:{idx} is out of range — "
                     f"{cat} holds {len(current)} entr(ies) in "
                     f"{spec_path.relative_to(ROOT)}")
        own_entry = None
        for e in reversed(history):
            if (str(e.get("test_id")) == str(spec.get("test_id")) or
                    str(e.get("seed")) == str(spec.get("seed"))):
                own_entry = e
                break
        # Same reason as the full-reroll path: this paper's own recorded picks
        # must not count as "recently used" against its own redraw. The KEPT
        # entries come back through `taken` immediately below, so they are still
        # excluded — just as in-test collisions, not as cooldown history.
        if own_entry is not None:
            own_entry.setdefault("items", {}).pop(cat, None)
        idx %= len(current)              # normalise a negative index once
        replaced = current[idx]
        kept = [x for i, x in enumerate(current) if i != idx]
        taken_text = {tok for c, xs in spec["items"].items() if c != cat
                      for x in xs for tok in taken_tokens(x)}
        taken_text |= {tok for x in kept for tok in taken_tokens(x)}
        # THIS TEST'S OWN ENTRY LEAVES THE HISTORY, not just its rerolled
        # category (F1 fix pass, 2026-08-20). Popping the category alone left
        # the entry occupying a slot, so every `ago` draw() measured was one
        # SHALLOWER than the window `assert_rotation()` then proved against
        # (it drops the whole entry via `prior_history`). A reroll could
        # therefore pick an item exactly `cool` draws back, draw() would
        # accept it and assert_rotation() would abort on it — which is what
        # `--reroll-one grammar_p8:0` did on the first attempt at this repair
        # (「目的結果(〜ために…なった)」, drawn by 20260813_2 six draws back).
        # The kept entries stay excluded through `taken_text` below, which is
        # an in-test collision guard, not cooldown history.
        updated_recency = recency_map([h for h in history
                                       if h is not own_entry])
        cool_max = cooldown_for(cat, len(pools[cat]))
        picked, cool = draw(rng, pools[cat], updated_recency, 1, cat,
                            taken_text, cool_max, kept=kept)
        # No adjunct pass: ADJUNCT_CAP of a 1-item draw is 0 by construction
        # (`int(1 * 0.20)`), so apply_adjunct() would return the pick unchanged.
        spec["items"][cat][idx] = picked[0]
        spec["seed"] = f"{spec.get('seed')}+reroll-one({cat}:{idx},{seed})"
        spec["pools_sha"] = pools_sha()   # R7, same as --reroll
        spec["rotation"] = carry_legacy(spec.get("rotation"), picked, {
            "recency_source": "ledger",
            "history_len": 0,          # filled in below
            "cooldown": min(cool, spec.get("rotation", {}).get("cooldown", cool)),
        })
        if own_entry is not None:
            own_entry.setdefault("items", {})[cat] = spec["items"][cat]
            own_entry["seed"] = spec["seed"]
            own_entry["pools_sha"] = spec["pools_sha"]
        for w in check_theme_spread(spec["items"][cat], cat):
            print(f"  WARNING: {cat} draw is theme-heavy — {w}")
        print(f"  reroll-one {cat}[{idx}]:\n"
              f"    out: 「{item_text(replaced)}」\n"
              f"    in : 「{item_text(picked[0])}」"
              + (f"  (errand key 「{errand_key(picked[0])}」)"
                 if errand_key(picked[0]) else ""))
        # Only the ONE new entry was drawn against "now"; the kept entries were
        # drawn earlier against a different window (see the full-reroll note
        # above), so verifying the whole category would be the same false
        # positive one level down.
        rotation_check_items = {cat: picked}
    else:
        items = {}
        taken: set = set()          # cross-category: one item, one 問題 per test
        theme_warns: list[str] = []
        effective_cool = None
        for cat, n in DRAW.items():
            if cat not in pools:
                sys.exit(f"category '{cat}' is in DRAW but missing from pools.json")
            cool_max = cooldown_for(cat, len(pools[cat]))
            picked, cool = draw(rng, pools[cat], recency, n, cat, taken, cool_max)
            effective_cool = cool if effective_cool is None else min(effective_cool, cool)
            if staging_by_cat:
                picked = apply_adjunct(rng, cat, picked, staging_by_cat,
                                       taken, recency, cool_max)
            items[cat] = picked
            taken.update(tok for x in picked for tok in taken_tokens(x))
            theme_warns += [f"{cat}: {w}" for w in check_theme_spread(picked, cat)]
        positions, pos_totals = balanced_position_plan(rng, ANSWER_SECTIONS)
        spec = {
            "seed": seed,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_id": args.test_id,
            # R10: the rotation this draw actually enforced, so a gate can check
            # the paper against logs/ledger.json instead of trusting a constant.
            # cooldown is the WEAKEST level applied to any category (COOLDOWN
            # unless a thin pool forced relaxation; 0 = no rotation at all).
            "rotation": {
                "recency_source": "ledger",
                "history_len": len(history),
                "cooldown": effective_cool,
            },
            # R7: the pool revision this seed is replayable against.
            "pools_sha": pools_sha(),
            "items": items,
            "answer_positions": positions,
        }
        history.append({"test_id": args.test_id, "seed": seed,
                        "generated_at": spec["generated_at"],
                        "pools_sha": spec["pools_sha"], "items": items,
                        "draw": dict(DRAW)})
        print(f"  answer positions over the {sum(pos_totals.values())} "
              f"four-choice items: " +
              ", ".join(f"{p}x{pos_totals[p]}" for p in (1, 2, 3, 4)) +
              f"  (band {POSITION_BAND[0]}-{POSITION_BAND[1]})")
        for w in theme_warns:
            print(f"  WARNING: theme-heavy draw — {w}")
        # A fresh draw's entry sits at the true end of `history` (just
        # appended above), so every category in it was drawn against the same
        # "now" window — the whole spec is fair to re-verify at once.
        rotation_check_items = spec["items"]

    # Invariant: no item may be tested by two different 問題 in the same paper.
    collisions = {}
    for a, b in itertools.combinations(spec["items"], 2):
        both = {item_text(x) for x in spec["items"][a]} & {item_text(x) for x in spec["items"][b]}
        if both:
            collisions[f"{a} x {b}"] = sorted(both)
    if collisions:
        sys.exit(f"same-test collision (a bug in draw()): {collisions}")

    # R10: prove EVERY category's OWN cooldown_for() window against the
    # ledger — everything recorded under a DIFFERENT test id. Do not reach
    # for history[-1] here: on the reroll path this test's entry can sit
    # anywhere in the list.
    prior_history = [h for h in history
                     if str(h.get("test_id")) != str(args.test_id)]
    spec["rotation"]["history_len"] = len(prior_history)
    assert_rotation(rotation_check_items, prior_history, pools)

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"seed={spec['seed']} -> {spec_path.relative_to(ROOT)} written, "
          f"ledger updated at {LEDGER.relative_to(ROOT)} "
          f"({len(history)} draw(s) recorded)")
    for cat, xs in spec["items"].items():
        rec = recency_map(history[:-1]) if history else {}
        reused = sum(1 for x in xs if item_text(x) in rec)
        print(f"  {cat}: {len(xs)} items ({len(xs) - reused} never used before)")

    # Same-domain scenario collision check
    scen_warns = check_domain_collisions(spec["items"].get("listening_scenarios", []))
    if scen_warns:
        print("\n  WARNING: listening_scenarios contains same-domain pair(s):")
        for w in scen_warns:
            print(f"    - {w}")
        print("  Consider --reroll listening_scenarios if two items share the same errand shape.")


if __name__ == "__main__":
    main()

