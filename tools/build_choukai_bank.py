#!/usr/bin/env python3
"""Build the 聴解 clip bank from the imported official sittings.

`logs/choukai_bank.json` is the item bank `sample_items.py` draws from and
`compose_choukai_mp3.py` cuts against. One record per item SLOT per sitting,
carrying the audio offsets plus the exact wording that already exists on disk:
the script block from `聴解スクリプト.txt`, the stem/options/script/explanation
fields from `詳細解説.json` and `詳細解説.vi.json`, and the key parsed by
`exam-app`'s own `parse_choukai_keys`.

Offsets, not audio
------------------
The bank stores byte-free spans and nothing else. `refs/` binaries and
`tests/*/聴解.mp3` are both out of git on purpose (AGENTS.md §3), so a bank of
300 pre-cut MP3s would be 300 more untracked files that a fresh clone lacks and
that no reviewer can read. Clips are cut on demand at compose time from the
sitting's own MP3; the bank stays a reviewable text artifact.

Slot-preserving draws
---------------------
Every record is tagged with the slot it occupied in its source paper, and the
composer may only place it in that same slot. This is not a stylistic choice:
official reads 「N番。」 continuously into the situation line with no pause
between them, so renumbering an item would mean cutting inside speech. Keeping
the slot means every cut lands in a structural silence. All 31 sittings run the
same 5/6/5/11/2 shape, so each slot has one candidate per sitting.

The mixed pool (bank v2)
------------------------
Since 2026-09-08 the bank is not official-only: `tools/build_textbook_bank.py`
appends Shin Kanzen and Soumatome items to the same file, so every record now
carries `source` ("official" | "shinkanzen" | "soumatome") and
`needs_number_call`. This script owns the OFFICIAL records only and always
writes `source: "official"`, `needs_number_call: False` — an official item
speaks its own 「N番。」 and is slot-preserved, which is exactly what the
paragraph above is about. Textbook items have no number call, so they are banked
body-only, are slot-FREE, and the composer prepends a harvested call
(`tools/harvest_number_calls.py`).

Usage
-----
    python3 tools/build_choukai_bank.py              # all imports -> logs/
    python3 tools/build_choukai_bank.py --check      # reconcile only, no write
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from build_textbook_bank import build_records as build_textbook_records  # noqa: E402
from choukai_segment import (  # noqa: E402
    EXPECTED_SLOTS, NotSegmented, hint_from_script, segment)

BANK_PATH = ROOT / "logs" / "choukai_bank.json"
BANK_VERSION = 2

# Keep the cut this far inside the surrounding silence, so a soft breath or a
# speech tail the envelope read as quiet is never clipped. The composer lays
# its own canonical pause after the clip, so trimmed silence is not lost.
GUARD_S = 0.25

ITEM_RE = re.compile(r"^(\d+)番。")
SECTION_RE = re.compile(r"^問題([1-5])。")


def _load(path: Path):
    """Import a repo script by path (they are not on the import path)."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GRADE = _load(ROOT / ".agents" / "exam-app" / "scripts" / "grade_answers.py")


class Reconciliation(Exception):
    """The audio and the text on disk disagree about what this paper contains."""


# ---------------------------------------------------------------- text side

def parse_script_blocks(
        path: Path) -> tuple[dict[tuple[str, int], str], dict[str, list[str]]]:
    """`聴解スクリプト.txt` -> ({(問題N, slot): item block}, {問題N: preamble}).

    Blocks are separated by one blank line and an item block starts with
    `N番。`, the same contract `make_choukai_mp3.py`'s parser uses. Everything
    in a section that is NOT an item block is that section's preamble text —
    the `問題N。` marker and the instruction — and the composer prints it above
    the items it lifted from the same sitting, so the printed instruction is
    always the one the audio speaks.

    Blocks before the first `問題1。` are the opening announcement, returned
    under the key `opening`.

    Position matters: 問題5 carries a SECOND lead-in ("まず話を聞いてください。
    それから、二つの質問を聞いて…") that sits between 1番 and 2番, not before
    1番. Filing every non-item block as a preamble printed it in the wrong place
    in the composed script. Each preamble block is therefore tagged with the
    number of items already seen in its section, and the composer replays them
    at that position. (The AUDIO was always right — 2番's clip starts at 1番's
    answer pause and contains the lead-in.)
    """
    text = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    items: dict[tuple[str, int], str] = {}
    preamble: dict[str, list[list]] = {"opening": []}
    section: str | None = None
    seen = 0
    for block in blocks:
        first = block.splitlines()[0]
        sec = SECTION_RE.match(first)
        if sec:
            section = f"問題{sec.group(1)}"
            seen = 0
            preamble.setdefault(section, []).append([0, block])
            continue
        item = ITEM_RE.match(first)
        if item and section:
            seen = int(item.group(1))
            items[(section, seen)] = block
        elif section is None:
            preamble["opening"].append([0, block])
        else:
            preamble[section].append([seen, block])
    return items, preamble


KEY_TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*\**(\d)\**\s*\|\s*(.*?)\s*\|$")


def parse_kaisetsu_cells(md_path: Path) -> dict[str, str]:
    """`聴解.md` -> {問N-M: the 解説 cell}, the per-option grounding lines.

    `exam-app`'s `parse_choukai_keys` already reads the correct-answer column of
    these same tables; this reads the third column, which is the writer's
    「N ✗「script line」→ reason」 grounding. Composing a paper reuses the source
    sitting's own cell rather than re-deriving one, so the booklet says what the
    booklet it came from said.
    """
    text = md_path.read_text(encoding="utf-8")
    marker = re.search(r"#+\s*【?正解[・\s]解説】?", text)
    if not marker:
        return {}
    out: dict[str, str] = {}
    section = None
    for line in text[marker.start():].splitlines():
        head = re.search(r"##\s*問題([1-5])", line)
        if head:
            section = int(head.group(1))
            continue
        row = KEY_TABLE_ROW.match(line.strip())
        if not (row and section):
            continue
        qlabel, _ans, cell = row.groups()
        qlabel = re.sub(r"[*\s]", "", qlabel)
        num = re.match(r"(\d+)", qlabel)
        if not num:
            continue
        key = f"問{section}-{num.group(1)}"
        if section == 5 and "質問" in qlabel:
            key += "-1" if "質問1" in qlabel else "-2"
        out[key] = cell
    return out


def item_key(section: str, slot: int, sub: int | None = None) -> str:
    """The `問N-M` id shared by 詳細解説.json and `parse_choukai_keys`."""
    base = f"問{section[-1]}-{slot}"
    return f"{base}-{sub}" if sub else base


def answer_ids(section: str, slot: int) -> list[str]:
    """The scored answer ids a slot produces — 問題5-2番 carries two."""
    if section == "問題5" and slot == 2:
        return [item_key(section, slot, 1), item_key(section, slot, 2)]
    return [item_key(section, slot)]


# ---------------------------------------------------------------- one sitting

def build_sitting(test_dir: Path) -> list[dict]:
    """Reconcile one imported sitting's audio against its text; emit records."""
    sitting = test_dir.name.removeprefix("imported-n2-")
    audio = test_dir / "聴解.mp3"
    script_path = test_dir / "聴解スクリプト.txt"
    kaisetsu_path = test_dir / "詳細解説.json"
    kaisetsu_vi_path = test_dir / "詳細解説.vi.json"
    booklet = test_dir / "聴解.md"

    for required in (audio, script_path, kaisetsu_path, booklet):
        if not required.is_file():
            raise Reconciliation(f"{test_dir.name}: missing {required.name}")

    script_text = script_path.read_text(encoding="utf-8")
    blocks, preamble_text = parse_script_blocks(script_path)
    kaisetsu = json.loads(kaisetsu_path.read_text(encoding="utf-8"))
    kaisetsu_vi = (json.loads(kaisetsu_vi_path.read_text(encoding="utf-8"))
                   if kaisetsu_vi_path.is_file() else {})
    keys = GRADE.parse_choukai_keys(booklet)
    kaisetsu_cells = parse_kaisetsu_cells(booklet)

    # --- the text must describe the shape the segmenter expects, BEFORE the
    #     audio is touched: a script that is short one item would otherwise
    #     silently align every later slot against the wrong span.
    for section, expected in EXPECTED_SLOTS.items():
        found = sorted(s for (sec, s) in blocks if sec == section)
        if found != list(range(1, expected + 1)):
            raise Reconciliation(
                f"{test_dir.name}: {section} script blocks are {found}, "
                f"expected 1..{expected}"
            )

    seg = segment(audio, hint_from_script(script_text))

    records: list[dict] = []
    for section, count in EXPECTED_SLOTS.items():
        for slot in range(1, count + 1):
            speech_lo, speech_hi = seg.slot_span(section, slot)
            ids = answer_ids(section, slot)

            missing_key = [i for i in ids if i not in keys]
            if missing_key:
                raise Reconciliation(
                    f"{test_dir.name}: no answer key for {', '.join(missing_key)}"
                )
            missing_exp = [i for i in ids if i not in kaisetsu]
            if missing_exp:
                raise Reconciliation(
                    f"{test_dir.name}: 詳細解説.json has no "
                    f"{', '.join(missing_exp)}"
                )

            closing = seg.answers[section][slot - 1]
            records.append({
                "id": f"{sitting}:{section}-{slot}",
                "sitting": sitting,
                "source_test": test_dir.name,
                "kind": "item",
                # Bank v2: the mixed pool carries textbook items too
                # (`build_textbook_bank.py`). An official item speaks its own
                # 「N番。」 and is slot-preserved; a textbook item does not and
                # is slot-free, so the composer must prepend a harvested call.
                "source": "official",
                "needs_number_call": False,
                "section": section,
                "slot": slot,
                "audio": {
                    "start": round(max(0.0, speech_lo - GUARD_S), 3),
                    "end": round(min(seg.duration, speech_hi + GUARD_S), 3),
                    # 問題5-2番 runs to EOF and keeps its own trailing pause and
                    # the closing announcement, so it declares no answer pause.
                    "answer_pause": round(closing.duration, 3),
                },
                "script": blocks[(section, slot)],
                "answers": {i: keys[i] for i in ids},
                "explanation": {i: kaisetsu[i] for i in ids},
                "explanation_vi": {i: kaisetsu_vi[i] for i in ids
                                   if i in kaisetsu_vi},
                "kaisetsu_cell": {i: kaisetsu_cells[i] for i in ids
                                  if i in kaisetsu_cells},
            })

    # --- Section preambles: opening announcement (問題1 only) + the 問題N
    #     instruction + 「では、練習しましょう。」 + the 例 + its confirmation +
    #     「では、始めます。」, lifted as ONE clip. Nothing inside is cut, so the
    #     例 stays coherent and no announcer line is spliced mid-sentence.
    ordered = list(EXPECTED_SLOTS)
    for i, section in enumerate(ordered):
        lo = 0.0 if i == 0 else seg.answers[ordered[i - 1]][-1].end
        hi = seg.preamble_end[section].start
        if hi <= lo:
            raise Reconciliation(
                f"{test_dir.name}: {section} preamble is empty "
                f"({lo:.1f}s -> {hi:.1f}s)"
            )
        records.append({
            "id": f"{sitting}:{section}-preamble",
            "sitting": sitting,
            "source_test": test_dir.name,
            "kind": "preamble",
            "source": "official",
            "section": section,
            "slot": 0,
            "audio": {"start": round(max(0.0, lo - GUARD_S), 3),
                      "end": round(hi + GUARD_S, 3)},
            # [after_item_index, block] — 0 means "before the first item"
            "text": preamble_text.get(section, []),
            # 問題5 needs a lead-in block before EACH of its two items. One
            # import (2022-07) transcribes only 1番's, so its 問題5 preamble
            # cannot supply 2番's and the composer must not draw it — the two
            # halves come from different sittings, so a gap here is silent.
            "complete": (section != "問題5"
                         or any(pos == 1
                                for pos, _t in preamble_text.get(section, []))),
            "opening": [t for _pos, t in preamble_text["opening"]] if i == 0 else [],
        })

    return records


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="reconcile every sitting but write nothing")
    ap.add_argument("--only", action="append", default=None,
                    help="limit to one test dir name (repeatable)")
    args = ap.parse_args(argv)

    dirs = sorted((ROOT / "tests").glob("imported-n2-*"))
    if args.only:
        dirs = [d for d in dirs if d.name in set(args.only)]
    if not dirs:
        print("no imported sittings found under tests/", file=sys.stderr)
        return 1

    all_records: list[dict] = []
    failures = 0
    for test_dir in dirs:
        try:
            records = build_sitting(test_dir)
        except (Reconciliation, NotSegmented) as exc:
            print(f"FAIL  {exc}")
            failures += 1
            continue
        items = [r for r in records if r["kind"] == "item"]
        scored = sum(len(r["answers"]) for r in items)
        print(f"ok    {test_dir.name:<24} {len(items)} items, "
              f"{scored} scored answers, {len(records) - len(items)} glue clips")
        all_records.extend(records)

    if failures:
        print(f"\n{failures} sitting(s) did not reconcile — bank not written")
        return 1

    # --- the textbook half. One writer for one file: a bank half-written by
    #     two scripts could leave official records fresh beside textbook records
    #     from a previous data file, and `bank_version` would not say so.
    textbook, refusals = build_textbook_records()
    for line in refusals:
        print(f"REFUSED  {line}")
    if refusals:
        print(f"\n{len(refusals)} textbook item(s) refused — bank not written. "
              f"A refusal is the guard against a mis-read CD track number "
              f"(build_textbook_bank.py §'The guard'); fix the declaration in "
              f".agents/choukai-audio/references/textbook_items.json or move "
              f"the item to its `excluded` list with a measured reason.")
        return 1
    from collections import Counter as _Counter
    shape = _Counter((r["source"], r["section"]) for r in textbook)
    print(f"ok    textbook items          {len(textbook)} items — "
          + ", ".join(f"{b}/{s} ×{n}" for (b, s), n in sorted(shape.items())))
    all_records.extend(textbook)

    if args.check:
        print(f"\n--check: {len(all_records)} records reconciled, nothing written")
        return 0

    BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
    BANK_PATH.write_text(json.dumps({
        "version": BANK_VERSION,
        "guard_s": GUARD_S,
        "sittings": [d.name for d in dirs],
        "records": all_records,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\nwrote {BANK_PATH.relative_to(ROOT)} — {len(all_records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
