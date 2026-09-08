#!/usr/bin/env python3
"""Harvest one clean 「N番。」 announcer call per number 1–11.

Why this exists
---------------
Official items open with the announcer saying 「3番。」 and the clip bank keeps
them slot-preserved for that reason (`choukai-audio` Part 0). Textbook tracks
(Shin Kanzen, Soumatome) carry **no number call at all**, so a textbook clip
dropped into slot 3 would leave the examinee with no idea which item is
playing. The mixed pool therefore banks textbook items BODY-ONLY and the
composer prepends a real official 「N番。」 to each.

The measurement that makes it work
----------------------------------
Every official item has a clean, long pause right after its number call —
median 0.90 s of speech then a 2.68 s pause, over the 290 banked items
(`references/textbook_bank_plan.md` §1). So the call can be cut out of an
existing bank item without touching the official bank itself: the span is
[speech onset, start of the first pause], and the duration bands below are what
prove the span is the NUMBER and not the number plus the situation line — a
span that ran on into the situation would measure well over `SPEECH_MAX`.

One announcer for all eleven
----------------------------
Numbers 7–11 exist only in 問題4, so a sitting supplies at most one candidate
for each and must have all five clean. Three of the ten do (2022-12, 2023-07,
2025-07), so the harvest prefers a **single sitting covering 1–11** and only
falls back to mixing sittings if none does. Eleven calls in one voice keep a
composed paper's textbook items sounding like one exam.

Offsets, not audio
------------------
Like the clip bank, this writes spans and nothing else — the composer cuts them
from the source MP3 at compose time (`build_choukai_bank.py` §"Offsets, not
audio").

Usage
-----
    python3 tools/harvest_number_calls.py            # -> logs/choukai_number_calls.json
    python3 tools/harvest_number_calls.py --check    # verify only, no write
    python3 tools/harvest_number_calls.py --report    # print every candidate
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from choukai_segment import (  # noqa: E402
    EXT_BELOW_LUFS, EXT_CAP_DBFS, FRAME_MS, find_pauses, measure)

BANK_PATH = ROOT / "logs" / "choukai_bank.json"
CALLS_PATH = ROOT / "logs" / "choukai_number_calls.json"
CALLS_VERSION = 1

NUMBERS = range(1, 12)          # 問題4 is the only 11-item 大問; nothing needs 12

# Acceptance bands. Every one of these is a REJECTION criterion, not a
# calibration figure: a span outside them is not a bare number call.
SPEECH_MIN = 0.6                # 「N番。」 measures 0.90 s median over the bank
SPEECH_MAX = 1.2                # above this the span has run into the situation
PAUSE_MIN = 1.2                 # the pause after it measures 2.68 s median
DETECT_FLOOR = 0.15             # pause-detection floor for this search only
ONSET_WINDOW = 4.0             # speech must start within this of the clip start
MIN_GAP_FROM_ONSET = 0.2        # a sub-0.2 s dip is a 促音 closure, not a pause

# Cut margins. The lead keeps a plosive first mora off the edge; the tail keeps
# the final 。 from being clipped by a frame-quantised pause start.
LEAD_S = 0.08
TAIL_S = 0.06


class NoCall(Exception):
    """No clean number call could be harvested for some number."""


# ---------------------------------------------------------------- measurement

def candidates(bank: dict, report: bool = False) -> dict[int, list[dict]]:
    """{number: [candidate span, …]} over every official item in the bank.

    A candidate is one bank item whose clip opens with speech in `SPEECH_MIN`..
    `SPEECH_MAX` followed by a pause of at least `PAUSE_MIN`.
    """
    items = [r for r in bank["records"]
             if r["kind"] == "item" and r.get("source", "official") == "official"]
    by_source: dict[str, list[dict]] = defaultdict(list)
    for rec in items:
        by_source[rec["source_test"]].append(rec)

    frame_s = FRAME_MS / 1000.0
    out: dict[int, list[dict]] = defaultdict(list)
    for source_test, recs in sorted(by_source.items()):
        audio = ROOT / "tests" / source_test / "聴解.mp3"
        if not audio.is_file():
            raise NoCall(
                f"missing source audio {audio.relative_to(ROOT)}. The exam "
                f"MP3s are release assets, not git objects (AGENTS.md §3) — "
                f"restore with:\n  gh release download audio --pattern "
                f"'{source_test}.mp3' --dir tests/{source_test}/")
        envelope, lufs = measure(audio)
        extended = min(EXT_CAP_DBFS, lufs - EXT_BELOW_LUFS)
        pauses = find_pauses(envelope, lufs, min_duration=DETECT_FLOOR)

        for rec in recs:
            clip_start = rec["audio"]["start"]
            first = int(clip_start / frame_s)
            window = envelope[first:first + int(ONSET_WINDOW / frame_s)]
            loud = np.flatnonzero(window >= extended)
            if loud.size == 0:
                continue
            onset = (first + int(loud[0])) * frame_s
            after = [p for p in pauses if p.start > onset + MIN_GAP_FROM_ONSET]
            if not after:
                continue
            pause = after[0]
            speech = pause.start - onset
            if not (SPEECH_MIN <= speech <= SPEECH_MAX):
                continue
            if pause.duration < PAUSE_MIN:
                continue
            out[rec["slot"]].append({
                "number": rec["slot"],
                "from_item": rec["id"],
                "source_test": source_test,
                "sitting": rec["sitting"],
                "start": round(max(0.0, onset - LEAD_S), 3),
                "end": round(pause.start + TAIL_S, 3),
                "speech": round(speech, 3),
                "pause_after": round(pause.duration, 3),
            })
    if report:
        for number in sorted(out):
            print(f"{number:2d}番  {len(out[number]):2d} candidates")
            for cand in out[number]:
                print(f"      {cand['from_item']:<28} "
                      f"{cand['start']:9.3f}→{cand['end']:9.3f}  "
                      f"speech {cand['speech']:.2f}s  "
                      f"pause {cand['pause_after']:.2f}s")
    return dict(out)


def pick(pool: dict[int, list[dict]]) -> tuple[dict[int, dict], str | None]:
    """Choose one candidate per number, preferring a single-sitting sweep.

    Quality inside a sitting is not a free choice — every candidate already
    passed the bands — so the tie-break is only there to be deterministic:
    the candidate whose speech length is closest to the pool median, then the
    longest following pause, then the id.
    """
    missing = [n for n in NUMBERS if not pool.get(n)]
    if missing:
        raise NoCall(
            "no clean 「N番。」 candidate for "
            + ", ".join(f"{n}番" for n in missing)
            + " — every candidate must be "
            f"{SPEECH_MIN}–{SPEECH_MAX}s of speech followed by a "
            f"{PAUSE_MIN}s+ pause")

    median = statistics.median(
        c["speech"] for n in NUMBERS for c in pool[n])

    def rank(cand: dict) -> tuple:
        return (abs(cand["speech"] - median), -cand["pause_after"],
                cand["from_item"])

    sweepers = sorted(
        {c["source_test"] for c in pool[1]}.intersection(
            *({c["source_test"] for c in pool[n]} for n in NUMBERS)))
    if sweepers:
        best_sitting = min(
            sweepers,
            key=lambda s: (sum(min(rank(c)[0] for c in pool[n]
                                   if c["source_test"] == s)
                               for n in NUMBERS), s))
        return ({n: min((c for c in pool[n]
                         if c["source_test"] == best_sitting), key=rank)
                 for n in NUMBERS}, best_sitting)

    return ({n: min(pool[n], key=rank) for n in NUMBERS}, None)


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-harvest and compare against the file on disk, "
                         "writing nothing")
    ap.add_argument("--report", action="store_true",
                    help="print every candidate span that passed the bands")
    args = ap.parse_args(argv)

    if not BANK_PATH.is_file():
        sys.exit(f"no clip bank at {BANK_PATH.relative_to(ROOT)} — "
                 f"run `make choukai-bank` first")
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))

    try:
        pool = candidates(bank, report=args.report)
        chosen, sweep = pick(pool)
    except NoCall as exc:
        print(f"FAIL  {exc}")
        return 1

    payload = {
        "version": CALLS_VERSION,
        "bands": {"speech_min": SPEECH_MIN, "speech_max": SPEECH_MAX,
                  "pause_min": PAUSE_MIN, "lead_s": LEAD_S, "tail_s": TAIL_S},
        "one_sitting": sweep,
        "calls": {str(n): chosen[n] for n in NUMBERS},
    }

    for number in NUMBERS:
        cand = chosen[number]
        print(f"{number:2d}番  {cand['source_test']}  "
              f"{cand['start']:9.3f}→{cand['end']:9.3f}  "
              f"speech {cand['speech']:.2f}s  pause {cand['pause_after']:.2f}s  "
              f"({len(pool[number])} candidates)")
    print("one announcer for all eleven: "
          + (sweep if sweep else "NO — mixed sittings (no single sitting "
                                 "covers 1–11)"))

    if args.check:
        if not CALLS_PATH.is_file():
            print(f"FAIL  {CALLS_PATH.relative_to(ROOT)} does not exist")
            return 1
        on_disk = json.loads(CALLS_PATH.read_text(encoding="utf-8"))
        if on_disk != payload:
            print(f"FAIL  {CALLS_PATH.relative_to(ROOT)} disagrees with a "
                  f"fresh harvest — re-run without --check")
            return 1
        print("--check: matches the file on disk")
        return 0

    CALLS_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print(f"\nwrote {CALLS_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
