#!/usr/bin/env python3
"""Bank the hand-transcribed Shin Kanzen / Soumatome 聴解 items.

`build_choukai_bank.py` owns the official half of `logs/choukai_bank.json` —
290 items cut out of the ten imported sittings. This owns the TEXTBOOK half:
one record per item declared in
`.agents/choukai-audio/references/textbook_items.json`, resolved to a CD track,
measured, duration-checked, and handed back for that file to append.

Why textbook items are slot-free
--------------------------------
An official item speaks its own 「N番。」 and is therefore locked to the slot it
occupied in its source paper. A textbook track speaks no number call at all, so
these records are banked BODY-ONLY, carry `needs_number_call: True`, and may
fill ANY slot of their 大問; the composer prepends a harvested official call
(`tools/harvest_number_calls.py`) plus the 2.7 s pause that follows one in
official audio.

Spoken options vs printed options
---------------------------------
問題3 and 問題4 SPEAK their four (three) options, so those arrive inside
`script_lines` as `^[1-4]、` lines and are harvested out of them. 問題1 and
問題2 PRINT theirs: the booklet shows the list and the audio never says it. A
declaration for those two sections therefore carries a separate
`printed_options` array, and putting them in `script_lines` instead is a defect
this file refuses — `spoken_shape` counts every character there as SPOKEN, so
four printed options would inflate an item's transcribed length against the
audio it actually has and the CHAR_RATE guard would refuse every 問題1/2 item
for a speech rate that looks about half what it is.

The body span is measured, not declared
---------------------------------------
Neither book's track is only the item. Both wrap it:

* **Soumatome** — a ~0.2 s marker blip, the item, a ~5.2 s built-in answer
  pause, then a 669 Hz end tone (measured identical across tracks).
* **Shin Kanzen** — a two-part spoken track id (a fixed ~0.90 s word then the
  track number, 0.3–0.7 s), the item, then a trailing answer pause to EOF.

`body_span` strips both ends structurally: it drops a LEADING run only when the
run is short AND a real pause follows it, and a TRAILING run only when the run
is short AND a 3 s+ pause precedes it (the built-in answer pause is the only
thing an end tone can sit behind). Everything between is the item, and the
composer lays the pacing table's own answer pause after it.

The guard against a mis-read track number
-----------------------------------------
A wrong track number is the failure mode this file exists to catch: the data
file is hand-typed off a scan, and a track that is off by one still produces
plausible-looking audio. Two checks, and an item that fails either is REFUSED
rather than banked:

1. the measured body span must sit inside its 大問's `TYPE_BANDS`, and
2. the span the transcript implies must agree with the span measured — expressed
   as an implied speech rate that has to land inside `CHAR_RATE`.

Both bands separate CLASSES from each other; they are not calibration figures
(the calibrated numbers live in `choukai-audio/SKILL.md`'s pacing table, and
`choukai_segment.expected_gaps` is what applies them here).

Usage
-----
    python3 tools/build_textbook_bank.py            # measure and report
    python3 tools/build_textbook_bank.py --json     # print the records
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from choukai_segment import (  # noqa: E402
    EXT_BELOW_LUFS, EXT_CAP_DBFS, FRAME_MS, expected_gaps, measure)

ITEMS_PATH = (ROOT / ".agents" / "choukai-audio" / "references"
              / "textbook_items.json")

BOOKS = {
    "soumatome": {
        "label": "日本語総まとめ N2 聴解",
        "cd_dir": {
            1: "refs/Soumatome/Nihongo Sou Matome N2 - Choukai-CD/"
               "日本語総まとめＮ2-ＣＤ1",
            2: "refs/Soumatome/Nihongo Sou Matome N2 - Choukai-CD/"
               "日本語総まとめＮ2-ＣＤ2",
        },
        "track_file": "{track:02d}.mp3",
        # A ~0.2 s marker blip opens the track; nothing spoken before the item.
        "max_header_runs": 1,
    },
    "shinkanzen": {
        "label": "新完全マスター N2 聴解",
        "cd_dir": {
            1: "refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai-CD/"
               "Shin_Kanzen_Masuta_N2-Choukai-AudioCD1",
            2: "refs/Shinkanzen/Shin_Kanzen_Masuta_N2-Choukai-CD/"
               "Shin_Kanzen_Masuta_N2-Choukai-AudioCD2",
        },
        "track_file": "Track{track:02d}.mp3",
        # A spoken track id in two parts: a fixed ~0.90 s word, then the track
        # NUMBER (0.30 s for 「に」 up to 0.72 s for 「じゅうに」 — measured across
        # tracks 65–76, which is how it was identified as an id and not a
        # 「N番。」: an item's own number would not be constant at 0.90 s.)
        "max_header_runs": 2,
    },
}

# --- body-span extraction ----------------------------------------------------
RUN_FLOOR_S = 0.10       # ignore sub-frame clicks
RUN_MERGE_S = 0.50       # a shorter dip is within-speech, not a boundary
HEADER_RUN_MAX = 1.30    # a header part is never longer than this
HEADER_ZONE_S = 6.00     # ...and never starts later than this
HEADER_GAP_MIN = 0.80    # ...and is always followed by a real pause
TONE_RUN_MAX = 1.00      # the end tone measures ~0.8 s
TONE_GAP_MIN = 3.00      # ...and always sits behind the built-in answer pause

# --- refusal bands -----------------------------------------------------------
# Body-span bands per 大問. Wide on purpose: they separate item TYPES from one
# another (a 問題1 track mis-labelled 問題4 is a 3x error), and the official
# spans they are drawn from are `logs/choukai_bank.json`'s own — 問題4 20.3–31.9,
# 問題3 43.7–115.0, 問題1 52.5–114.4, 問題2 75.9–142.1, 問題5 138.7–226.7 —
# widened downward because a textbook body carries no 「N番。」 and no pause after
# one, and outward for the two books' shorter internal gaps.
TYPE_BANDS = {
    "問題1": (40.0, 140.0),
    "問題2": (60.0, 175.0),
    "問題3": (33.0, 135.0),
    "問題4": (11.0, 40.0),
    "問題5": (105.0, 250.0),
}

# Implied seconds per spoken character once `expected_gaps` is removed. Same
# status as TYPE_BANDS: a refusal band, not a calibration. It catches a track
# that is the right TYPE but the wrong ITEM, which the duration band cannot.
CHAR_RATE = (0.060, 0.200)

SPOKEN_CHOICE_RE = re.compile(r"^([1-4])、(.*)$")
SPEAKER_LABEL_RE = re.compile(r"^[^:：]{1,6}[:：]")

# The 大問 whose options the booklet PRINTS and the audio never speaks
# (`jlpt-exam-structure`'s "Printed in booklet" column owns the fact). Items in
# these sections declare `printed_options` instead of carrying 「N、…」 lines in
# `script_lines`; `derive_text` refuses either mistake in either direction.
PRINTED_OPTION_SECTIONS = ("問題1", "問題2")

# How many options each 大問 takes. 問題4 is the odd one at three.
EXPECTED_OPTIONS = {"問題1": 4, "問題2": 4, "問題3": 4, "問題4": 3, "問題5": 4}


class Refused(Exception):
    """An item did not survive the guards, so it is not banked."""


def track_path(book: str, cd: int, track: int) -> Path:
    spec = BOOKS[book]
    if cd not in spec["cd_dir"]:
        raise Refused(f"{book}: no CD {cd}")
    return ROOT / spec["cd_dir"][cd] / spec["track_file"].format(track=track)


def speech_runs(path: Path) -> tuple[list[list[float]], float]:
    """Merged speech runs and total duration, from the cached envelope."""
    envelope, lufs = measure(path)
    frame_s = FRAME_MS / 1000.0
    extended = min(EXT_CAP_DBFS, lufs - EXT_BELOW_LUFS)
    loud = envelope >= extended
    edges = np.flatnonzero(np.diff(loud.astype(np.int8)))
    bounds = np.concatenate(([0], edges + 1, [loud.size]))
    raw: list[list[float]] = []
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        if loud[lo] and (hi - lo) * frame_s >= RUN_FLOOR_S:
            raw.append([lo * frame_s, hi * frame_s])
    merged: list[list[float]] = []
    for start, end in raw:
        if merged and start - merged[-1][1] < RUN_MERGE_S:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged, envelope.size * frame_s


def body_span(path: Path, max_header_runs: int
              ) -> tuple[float, float, float, int, int]:
    """(start, end, file duration, header runs dropped, tail runs dropped)."""
    runs, duration = speech_runs(path)
    if not runs:
        raise Refused(f"{path.name}: no speech above the extended threshold")

    first = 0
    while first < len(runs) and first < max_header_runs:
        start, end = runs[first]
        if start > HEADER_ZONE_S or (end - start) > HEADER_RUN_MAX:
            break
        following = runs[first + 1][0] if first + 1 < len(runs) else duration
        if following - end < HEADER_GAP_MIN:
            break
        first += 1

    last = len(runs) - 1
    while last > first:
        start, end = runs[last]
        if (end - start) <= TONE_RUN_MAX and start - runs[last - 1][1] >= TONE_GAP_MIN:
            last -= 1
        else:
            break

    return (runs[first][0], runs[last][1], duration,
            first, len(runs) - 1 - last)


def derive_text(script_lines: list[str], section: str,
                printed_options: list[str] | None = None
                ) -> tuple[str, list[str], str]:
    """(stem, options, script body) from the transcript lines.

    Two shapes, because the exam has two (`jlpt-exam-structure`'s "Printed in
    booklet" column):

    * **問題3 / 問題4 — options SPOKEN.** They are `^[1-4]、` lines inside
      `script_lines` and are harvested out of them, leaving the dialogue.
    * **問題1 / 問題2 — options PRINTED.** The audio never says them, so they
      arrive in `printed_options` and `script_lines` must contain no choice
      line at all. The stem is the FIRST line only (marker + situation +
      question, which is what the announcer reads up front) and the repeated
      closing question stays in the script — the same split the official
      問題1/問題2 records carry.
    """
    printed = section in PRINTED_OPTION_SECTIONS
    options: list[str] = []
    plain: list[str] = []
    for line in script_lines:
        choice = SPOKEN_CHOICE_RE.match(line)
        if choice:
            options.append(choice.group(2).strip())
        else:
            plain.append(line)
    if not plain:
        raise Refused("script_lines carry no non-choice line")

    if printed:
        if options:
            raise Refused(
                f"{section} PRINTS its options, so script_lines must carry no "
                f"「N、…」 choice line — found {len(options)}. Move them to "
                f"printed_options; left in the script they are counted as "
                f"spoken characters and the CHAR_RATE guard refuses the item")
        if not printed_options:
            raise Refused(
                f"{section} PRINTS its options and none are declared — add a "
                f"`printed_options` array read off the 問題冊子 page")
        # 問題1/2: the announcer reads situation+question, then the talk, then
        # the question again. Only the first line is the stem.
        return plain[0], list(printed_options), "\n".join(script_lines[1:])

    if printed_options:
        raise Refused(
            f"{section} SPEAKS its options, so they belong in script_lines as "
            f"「N、…」 lines, not in printed_options")
    # The stem is the situation line plus, when the item announces one, the
    # question read after the talk — the same two-part shape the official
    # records carry. A speaker-tagged line is dialogue, never the question.
    stem = plain[0]
    if len(plain) > 1 and not SPEAKER_LABEL_RE.match(plain[-1]):
        stem += plain[-1]
    return stem, options, "\n".join(script_lines)


def spoken_shape(script_lines: list[str]) -> tuple[int, int, int]:
    """(spoken chars, lines, spoken-choice lines) — `hint_from_script`'s shape.

    It takes `script_lines` and NOTHING else on purpose: every character it
    counts is a character the audio says. A 問題1/2 item's printed options live
    in their own field and never reach here, which is what keeps the CHAR_RATE
    guard comparing spoken text against spoken audio.
    """
    spoken = [SPEAKER_LABEL_RE.sub("", line).strip() for line in script_lines]
    choices = sum(1 for line in script_lines if SPOKEN_CHOICE_RE.match(line))
    return sum(len(s) for s in spoken), len(spoken), choices


def build_one(spec: dict) -> dict:
    """Measure and validate one declared item; return its bank record."""
    book, cd, track = spec["book"], spec["cd"], spec["track"]
    section = spec["section"]
    if book not in BOOKS:
        raise Refused(f"{spec['id']}: unknown book {book!r}")
    if section not in TYPE_BANDS:
        raise Refused(f"{spec['id']}: unknown section {section!r}")

    audio = track_path(book, cd, track)
    if not audio.is_file():
        raise Refused(
            f"{spec['id']}: missing {audio.relative_to(ROOT)}. The textbook CDs "
            f"are release assets, not git objects (AGENTS.md §3) — restore with:"
            f"\n  gh release download refs --pattern "
            f"'{'Soumatome' if book == 'soumatome' else 'Shinkanzen'}.zip' "
            f"--dir /tmp && unzip -n /tmp/*.zip -d refs/")

    start, end, duration, n_head, n_tail = body_span(
        audio, BOOKS[book]["max_header_runs"])
    span = end - start

    lo, hi = TYPE_BANDS[section]
    if not lo <= span <= hi:
        raise Refused(
            f"{spec['id']}: body span {span:.1f}s is outside {section}'s "
            f"{lo:.0f}–{hi:.0f}s band — the track number is probably wrong "
            f"({audio.name} runs {duration:.1f}s in total). Re-check "
            f"{spec.get('source_page', 'the page')}")

    chars, lines, choices = spoken_shape(spec["script_lines"])
    gaps = expected_gaps(section, 1, lines, choices)
    rate = (span - gaps) / max(chars, 1)
    if not CHAR_RATE[0] <= rate <= CHAR_RATE[1]:
        raise Refused(
            f"{spec['id']}: {span:.1f}s of audio against {chars} transcribed "
            f"characters implies {rate:.3f} s/char, outside the plausible "
            f"{CHAR_RATE[0]}–{CHAR_RATE[1]} band — this track is the right "
            f"length for a {section} item but does not say what the transcript "
            f"says. Re-check {spec.get('source_page', 'the page')}")

    stem, options, script = derive_text(
        spec["script_lines"], section, spec.get("printed_options"))
    expected_options = EXPECTED_OPTIONS[section]
    if len(options) != expected_options:
        source = ("printed_options" if section in PRINTED_OPTION_SECTIONS
                  else "spoken choice line(s)")
        raise Refused(
            f"{spec['id']}: {len(options)} {source}, "
            f"{section} takes {expected_options}")
    if len(set(options)) != len(options):
        raise Refused(f"{spec['id']}: two options are identical")
    answer = spec["answer"]
    if not 1 <= answer <= expected_options:
        raise Refused(
            f"{spec['id']}: answer {answer} is outside 1–{expected_options}")

    payload = dict(spec["explanation"])
    payload.update({"stem": stem, "options": options, "script": script})
    vi = dict(spec["explanation_vi"])
    if len(vi.get("options_analysis") or []) != len(options):
        raise Refused(
            f"{spec['id']}: the Vietnamese pane analyses "
            f"{len(vi.get('options_analysis') or [])} options, not {len(options)}")

    return {
        "id": spec["id"],
        "source": book,
        "source_page": spec.get("source_page", ""),
        "kind": "item",
        "section": section,
        # Slot-free: a textbook item speaks no number, so the composer may put
        # it anywhere in its 大問. 0 is "no slot", which is also what the
        # preamble records use.
        "slot": 0,
        "needs_number_call": True,
        "audio": {
            "path": str(audio.relative_to(ROOT)),
            "start": round(start, 3),
            "end": round(end, 3),
            # The book's OWN built-in answer pause, reported and then discarded:
            # the composer lays the pacing table's value instead.
            "answer_pause": round(duration - end, 3),
        },
        "script_lines": list(spec["script_lines"]),
        "answer": answer,
        "explanation_payload": payload,
        "explanation_vi_payload": vi,
        "kaisetsu_cell_text": spec.get("kaisetsu_cell", ""),
        "measured": {"span": round(span, 3), "chars": chars, "lines": lines,
                     "rate": round(rate, 4),
                     "dropped_head_runs": n_head, "dropped_tail_runs": n_tail},
    }


def build_records(verbose: bool = False) -> tuple[list[dict], list[str]]:
    """(records, refusals) over every item the data file declares."""
    if not ITEMS_PATH.is_file():
        return [], [f"no textbook item file at {ITEMS_PATH.relative_to(ROOT)}"]
    data = json.loads(ITEMS_PATH.read_text(encoding="utf-8"))
    records, refusals = [], []
    seen: set[str] = set()
    for spec in data["items"]:
        if spec["id"] in seen:
            refusals.append(f"{spec['id']}: declared twice")
            continue
        seen.add(spec["id"])
        try:
            record = build_one(spec)
        except Refused as exc:
            refusals.append(str(exc))
            continue
        records.append(record)
        if verbose:
            m = record["measured"]
            print(f"ok    {record['id']:<22} {record['section']}  "
                  f"{m['span']:6.1f}s  {m['chars']:4d} chars  "
                  f"{m['rate']:.3f} s/char  key {record['answer']}")
    return records, refusals


# The margin below which an item is reported as sitting ON a band edge. Not a
# refusal: an item this close to an edge is evidence about the BAND, not about
# the item, and the two readings (a band about to refuse a correct declaration,
# a band no longer separating types) both need a human.
BAND_EDGE_MARGIN = 0.10


def band_headroom(records: list[dict]) -> tuple[list[str], list[str]]:
    """(per-section span/rate report, items sitting on a band edge).

    `TYPE_BANDS` and `CHAR_RATE` were written when only 問題3 and 問題4 were
    banked, so three of the five bands had never refused or admitted anything;
    問題1 and 問題2 started drawing 2026-09-09. This is the pass that exercises
    them: it prints, per 大問, the band, how many items are inside it and where
    the extremes actually sit, and it names any item within
    `BAND_EDGE_MARGIN` of a band edge — the case where the next correct
    declaration gets refused, or where the band has stopped separating one item
    type from another.
    """
    from collections import defaultdict
    by_section: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        by_section[rec["section"]].append(rec)

    report, edges = [], []
    for section in TYPE_BANDS:
        lo, hi = TYPE_BANDS[section]
        group = by_section.get(section, [])
        if not group:
            report.append(f"  {section}  band {lo:5.0f}–{hi:5.0f}s   "
                          f"(no items banked)")
            continue
        spans = [r["measured"]["span"] for r in group]
        rates = [r["measured"]["rate"] for r in group]
        report.append(
            f"  {section}  band {lo:5.0f}–{hi:5.0f}s   n={len(group):2d}  "
            f"spans {min(spans):6.1f}–{max(spans):6.1f}s  "
            f"rates {min(rates):.3f}–{max(rates):.3f} s/char")
        width = hi - lo
        for rec in group:
            span = rec["measured"]["span"]
            if span - lo < width * BAND_EDGE_MARGIN:
                edges.append(f"{rec['id']} span {span:.1f}s is within "
                             f"{BAND_EDGE_MARGIN:.0%} of {section}'s {lo:.0f}s "
                             f"floor")
            if hi - span < width * BAND_EDGE_MARGIN:
                edges.append(f"{rec['id']} span {span:.1f}s is within "
                             f"{BAND_EDGE_MARGIN:.0%} of {section}'s {hi:.0f}s "
                             f"ceiling")
            rate = rec["measured"]["rate"]
            rwidth = CHAR_RATE[1] - CHAR_RATE[0]
            if rate - CHAR_RATE[0] < rwidth * BAND_EDGE_MARGIN:
                edges.append(f"{rec['id']} rate {rate:.3f} is within "
                             f"{BAND_EDGE_MARGIN:.0%} of CHAR_RATE's floor")
            if CHAR_RATE[1] - rate < rwidth * BAND_EDGE_MARGIN:
                edges.append(f"{rec['id']} rate {rate:.3f} is within "
                             f"{BAND_EDGE_MARGIN:.0%} of CHAR_RATE's ceiling")
    return report, edges


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true",
                    help="print the records instead of the report")
    args = ap.parse_args(argv)

    records, refusals = build_records(verbose=not args.json)
    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=1))
        return 1 if refusals else 0

    from collections import Counter
    by_section = Counter(r["section"] for r in records)
    by_book = Counter(r["source"] for r in records)
    print(f"\n{len(records)} textbook item(s): "
          + ", ".join(f"{k} {v}" for k, v in sorted(by_section.items()))
          + "  |  " + ", ".join(f"{k} {v}" for k, v in sorted(by_book.items())))
    report, edges = band_headroom(records)
    print("\nTYPE_BANDS / CHAR_RATE headroom")
    for line in report:
        print(line)
    for line in edges:
        print(f"EDGE     {line}")
    for line in refusals:
        print(f"REFUSED  {line}")
    return 1 if refusals else 0


if __name__ == "__main__":
    raise SystemExit(main())
