#!/usr/bin/env python3
"""Compose one test's 聴解 half out of official clips.

Replaces the Edge-TTS path (`.agents/choukai-audio/scripts/make_choukai_mp3.py`)
for generated papers. Instead of synthesizing speech from an authored script,
this draws whole items from `logs/choukai_bank.json` — real recordings from the
ten imported official sittings — and lays them out with the pacing table's
pauses between them.

What it writes, all from the drawn records:

    聴解スクリプト.txt   the exact transcript of the clips it used
    聴解.md             booklet: instructions, printed options, mark sheet, keys
    聴解.mp3            the composed audio, one loudnorm pass
    聴解_チャプター.json  real per-問題/per-item offsets
    詳細解説.json        the 30 choukai entries, merged in beside 問1-71
    詳細解説.vi.json     the same, Vietnamese pane

Two kinds of clip, two placement rules
--------------------------------------
**Official** items are drawn slot-preserving: item *k* of 問題N only ever comes
from item *k* of 問題N in some sitting. Official runs 「N番。」 continuously into
the situation line with no pause between them, so renumbering would mean cutting
inside speech; keeping the slot means every cut lands in a structural silence and
the announcer's own numbering stays correct. Each slot has one candidate per
sitting, so ten.

**Textbook** items (Shin Kanzen, Soumatome — `tools/build_textbook_bank.py`) are
banked body-only because their tracks speak no number call at all. They are
therefore slot-FREE, and this file prepends a harvested official 「N番。」
(`tools/harvest_number_calls.py`) plus `AFTER_NUMBER_CALL`, the pause that
follows one in official audio. All eleven calls come from one sitting, so a
composed paper's prepended numbers are one announcer.

`OFFICIAL_ONLY_TESTS` and `TEXTBOOK_SLOTS` decide the mix. Exactly ONE paper is official-only — the
reference point that says what the pool sounded like before the textbooks were
added; every other paper takes `TEXTBOOK_SLOTS` of its slots from the textbook
pool per 大問.

Answer positions are a SELECTION constraint here, not an authoring one: lifted
options cannot be reordered, because 問題3/4/5 speak them aloud. The draw
therefore searches candidate combinations for a flat key distribution instead
of placing keys where a spec told it to.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import hashlib
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_PATH = ROOT / "logs" / "choukai_bank.json"
DRAWS_PATH = ROOT / "logs" / "choukai_draws.json"

SECTIONS = {"問題1": 5, "問題2": 6, "問題3": 5, "問題4": 11, "問題5": 2}

# Pauses the composer LAYS DOWN between clips, from choukai-audio/SKILL.md's
# measured table. The clips carry their own internal rhythm, so these are only
# the structural gaps between units.
ANSWER_PAUSE = {"問題1": 12.0, "問題2": 12.0, "問題3": 8.0, "問題4": 8.0,
                "問題5": 10.0}
# NOTE: 問題2's ~20 s option-reading pause is NOT laid down here. It sits
# inside each 問題2 clip, between the announcer's question and the talk, and is
# lifted with the item.
AFTER_PREAMBLE = 3.0      # instruction/例 block -> first item

# The pause an official item lays between its 「N番。」 and the situation line:
# median 2.68 s over the 290 banked items (references/textbook_bank_plan.md §1).
# A textbook item gets the same, so a prepended call is indistinguishable in
# rhythm from a native one.
AFTER_NUMBER_CALL = 2.7

# The ONE official-only paper. It is not an exemption — it is the control: a
# paper composed purely from the ten sittings, kept so the suite still contains
# a reference the textbook pool can be compared against by ear.
OFFICIAL_ONLY_TESTS = {"20260807_1"}

# Slots per 大問 that every OTHER paper fills from the textbook pool. Chosen
# from what the pool can carry without over-mining it: 22 textbook 問題4 items
# over 4 slots x 22 papers is ~4 uses each, against ~1.6 for an official 問題4
# item, and 4 textbook 問題3 items over 1 slot x 22 papers is ~5.5. Raising a
# number here re-mines the same few clips; grow the pool first
# (.agents/choukai-audio/references/textbook_items.json).
#
# 問題1/問題2/問題5 are absent on purpose and it is a SOURCE limit, not a policy
# one — their options are printed rather than spoken and the printed lists are
# not in either answer booklet, and neither book lays the 10 s 質問1 pause an
# official 問題5-2番 carries inside itself. See textbook_bank_plan.md §6.
TEXTBOOK_SLOTS = {"問題3": 1, "問題4": 4}

SR = 48_000               # official recordings are 48 kHz
LOUDNORM = "loudnorm=I=-15:TP=-1.0:LRA=11"

FURIGANA_RE = re.compile(r"《[^》]*》")


def strip_furigana(text: str) -> str:
    """Booklet options print plain; 詳細解説 stores them with 《…》 ruby."""
    return FURIGANA_RE.sub("", text)


# ---------------------------------------------------------------- the draw

def load_bank() -> dict:
    if not BANK_PATH.is_file():
        sys.exit(f"no clip bank at {BANK_PATH.relative_to(ROOT)} — "
                 f"run `python3 tools/build_choukai_bank.py` first")
    return json.loads(BANK_PATH.read_text(encoding="utf-8"))


CALLS_PATH = ROOT / "logs" / "choukai_number_calls.json"
_CALLS: dict | None = None


def number_call(slot: int) -> dict:
    """The harvested official 「N番。」 span for this slot.

    Textbook clips are banked body-only, so the composer speaks the number
    itself. The spans come from `tools/harvest_number_calls.py`, which verifies
    each is 0.6–1.2 s of speech followed by a 1.2 s+ pause and prefers a single
    sitting for all eleven.
    """
    global _CALLS
    if _CALLS is None:
        if not CALLS_PATH.is_file():
            sys.exit(f"no number calls at {CALLS_PATH.relative_to(ROOT)} — "
                     f"run `python3 tools/harvest_number_calls.py` first "
                     f"(a textbook clip carries no 「N番。」 of its own)")
        _CALLS = json.loads(CALLS_PATH.read_text(encoding="utf-8"))["calls"]
    if str(slot) not in _CALLS:
        sys.exit(f"no harvested 「{slot}番。」 — re-run "
                 f"tools/harvest_number_calls.py")
    return _CALLS[str(slot)]


def load_draws() -> dict:
    if DRAWS_PATH.is_file():
        return json.loads(DRAWS_PATH.read_text(encoding="utf-8"))
    return {"version": 1, "history": []}


def usage_counts(draws: dict, exclude: str = "") -> Counter:
    """How many papers have already used each bank record."""
    used: Counter = Counter()
    for row in draws["history"]:
        if row["test_id"] == exclude:
            continue
        used.update(row["clips"].values())
        used.update(row.get("preambles", {}).values())
    return used


def resolve(rec: dict, section: str, slot: int) -> dict:
    """One drawn record placed in one slot — the fields every renderer reads.

    An OFFICIAL record already carries `script`, `answers`, `explanation`,
    `explanation_vi` and `kaisetsu_cell` keyed `問N-M`, and because it is
    slot-preserved those keys are already this slot's. A TEXTBOOK record cannot
    carry them: it is slot-free, so the `問N-M` key is only known once the draw
    places it, and its transcript is banked without the 「N番。」 the composer
    prepends. This is the one place that difference is resolved; everything
    downstream sees the same shape.
    """
    if not rec.get("needs_number_call"):
        return {"record": rec, "section": section, "slot": slot,
                "script": rec["script"], "answers": rec["answers"],
                "explanation": rec["explanation"],
                "explanation_vi": rec["explanation_vi"],
                "kaisetsu_cell": rec["kaisetsu_cell"]}
    lines = rec["script_lines"]
    key = f"問{section[-1]}-{slot}"
    return {
        "record": rec, "section": section, "slot": slot,
        "script": "\n".join([f"{slot}番。{lines[0]}"] + lines[1:]),
        "answers": {key: rec["answer"]},
        "explanation": {key: dict(rec["explanation_payload"])},
        "explanation_vi": {key: dict(rec["explanation_vi_payload"])},
        "kaisetsu_cell": {key: rec["kaisetsu_cell_text"]},
    }


def key_spread(picked: list[dict]) -> float:
    """Chi-square-ish penalty for an uneven answer-position distribution.

    問題4 keys run 1–3 and every other section 1–4, so the two are scored
    separately; mixing them would make a perfectly flat paper look skewed.
    """
    penalty = 0.0
    for section_group, n_opts in ((("問題4",), 3),
                                  (("問題1", "問題2", "問題3", "問題5"), 4)):
        keys = [v for r in picked if r["section"] in section_group
                for v in r["answers"].values()]
        if not keys:
            continue
        counts = Counter(keys)
        expect = len(keys) / n_opts
        penalty += sum((counts.get(k, 0) - expect) ** 2
                       for k in range(1, n_opts + 1)) / expect
    return penalty


def draw(bank: dict, seed: int, used: Counter, test_id: str,
         attempts: int = 400) -> tuple[dict, dict]:
    """Pick one record per slot and one preamble per section.

    Two objectives, in order: spend the least-used clips first (so the pool
    rotates evenly across the suite rather than a few clips being mined), then
    among equally-fresh combinations prefer a flat answer-key spread.

    The source policy sits on top of that. Official candidates are indexed by
    (section, slot) because they are slot-preserved; textbook candidates are
    indexed by section alone because they carry no number call and can go
    anywhere. For a paper outside `OFFICIAL_ONLY_TESTS`, `TEXTBOOK_SLOTS[section]`
    of that 大問's slots are chosen at random and filled from the textbook pool
    WITHOUT REPEATS — a slot-free clip is otherwise free to land in two slots of
    the same paper, which would print the same item twice.
    """
    rng = random.Random(seed)
    official: dict[tuple[str, int], list[dict]] = {}
    textbook: dict[str, list[dict]] = {}
    preambles: dict[str, list[dict]] = {}
    for rec in bank["records"]:
        if rec["kind"] != "item":
            preambles.setdefault(rec["section"], []).append(rec)
        elif rec.get("needs_number_call"):
            textbook.setdefault(rec["section"], []).append(rec)
        else:
            official.setdefault((rec["section"], rec["slot"]), []).append(rec)

    for section, count in SECTIONS.items():
        for slot in range(1, count + 1):
            if (section, slot) not in official:
                sys.exit(f"bank has no official candidates for {section}-{slot}")

    # How many slots of each 大問 come from the textbook pool, and which ones.
    wanted = {} if test_id in OFFICIAL_ONLY_TESTS else {
        section: min(n, SECTIONS[section], len(textbook.get(section, [])))
        for section, n in TEXTBOOK_SLOTS.items()}
    for section, n in TEXTBOOK_SLOTS.items():
        if wanted.get(section, n) < n and test_id not in OFFICIAL_ONLY_TESTS:
            print(f"  note: {section} wanted {n} textbook slot(s), the bank "
                  f"has {len(textbook.get(section, []))} item(s)")

    def freshest(pool: list[dict], exclude: set[str]) -> dict:
        """Least-used first; among equals, the rng picks."""
        avail = [r for r in pool if r["id"] not in exclude]
        fewest = min(used[r["id"]] for r in avail)
        return rng.choice([r for r in avail if used[r["id"]] == fewest])

    best = None
    for _ in range(attempts):
        picked: list[tuple[str, int, dict]] = []
        for section, count in SECTIONS.items():
            slots = list(range(1, count + 1))
            from_textbook = set(rng.sample(slots, wanted.get(section, 0)))
            spent: set[str] = set()
            for slot in slots:
                if slot in from_textbook:
                    rec = freshest(textbook[section], spent)
                    spent.add(rec["id"])
                else:
                    rec = freshest(official[(section, slot)], set())
                picked.append((section, slot, rec))
        records = [r for _s, _n, r in picked]
        score = (sum(used[r["id"]] for r in records),
                 key_spread([resolve(r, s, n) for s, n, r in picked]))
        if best is None or score < best[0]:
            best = (score, picked)

    _, picked = best
    chosen_items = {f"{section}-{slot}": rec["id"] for section, slot, rec in picked}
    chosen_pre = {}
    for section in SECTIONS:
        pool = [r for r in preambles[section] if r.get("complete", True)]
        if not pool:
            sys.exit(f"bank has no complete {section} preamble")
        fewest = min(used[r["id"]] for r in pool)
        fresh = [r for r in pool if used[r["id"]] == fewest]
        chosen_pre[section] = rng.choice(fresh)["id"]
    return chosen_items, chosen_pre


# ---------------------------------------------------------------- rendering

def by_id(bank: dict) -> dict[str, dict]:
    return {r["id"]: r for r in bank["records"]}


def ordered_items(index: dict, clips: dict[str, str]) -> list[dict]:
    """Every drawn clip, in paper order, already placed in its slot."""
    out = []
    for section, count in SECTIONS.items():
        for slot in range(1, count + 1):
            out.append(resolve(index[clips[f"{section}-{slot}"]], section, slot))
    return out


def placed_by_slot(index: dict, clips: dict[str, str]) -> dict[str, dict]:
    return {f"{p['section']}-{p['slot']}": p
            for p in ordered_items(index, clips)}


def render_script(index: dict, clips: dict, pres: dict) -> str:
    """`聴解スクリプト.txt` — exactly what the composed audio says.

    The 例 is absent here and present in the audio, the same divergence every
    `tests/imported-*` sitting carries: the official script PDFs do not print
    the practice items, so no transcript of them exists in this repo. The 例
    audio rides inside the section preamble clip, uncut.
    """
    placed = placed_by_slot(index, clips)
    parts: list[str] = []
    parts.extend(index[pres["問題1"]].get("opening", []))
    for section, count in SECTIONS.items():
        pre = index[pres[section]]["text"]
        # A preamble block tagged `pos` sits AFTER item `pos` — pos 0 means
        # before the first item. 問題5 has two such blocks: its 2番 lead-in at
        # pos 1 and 「これで、聴解試験を終わります。」 at pos 2. Emitting them
        # before the item instead put the lead-in ahead of 1番 and the closing
        # announcement ahead of 2番.
        parts.extend(block for pos, block in pre if pos == 0)
        for slot in range(1, count + 1):
            parts.append(placed[f"{section}-{slot}"]["script"])
            parts.extend(block for pos, block in pre if pos == slot)
    return "\n\n".join(p.strip() for p in parts if p.strip()) + "\n"


def render_booklet(index: dict, clips: dict, pres: dict) -> str:
    """`聴解.md` — printed options, mark sheet, and the key/解説 tables."""
    L = ["# 【聴解】", ""]
    placed = placed_by_slot(index, clips)

    def instruction(section: str) -> str:
        body = [t for pos, t in index[pres[section]]["text"]
                if pos == 0 and not t.strip().startswith(f"{section}。")]
        return body[0].strip() if body else ""

    def lead_in(section: str, after: int) -> str:
        """問題5's spoken lead-ins, by the item they precede.

        Selected by content, not position: pos 0 holds three blocks (the 問題5。
        marker, the section instruction and 1番's lead-in) and only the last is
        wanted, while pos 1 holds 2番's lead-in alone.
        """
        body = [t.strip() for pos, t in index[pres[section]]["text"]
                if pos == after]
        if after == 0:
            body = [t for t in body if t.startswith("問題用紙に何も印刷")]
        return body[0] if body else ""

    for section, count in SECTIONS.items():
        L += [f"## {section}", instruction(section), ""]
        for slot in range(1, count + 1):
            exp = placed[f"{section}-{slot}"]["explanation"]
            if section in ("問題1", "問題2"):
                L.append(f"**{slot}番**")
                for i, opt in enumerate(exp[f"問{section[-1]}-{slot}"]["options"], 1):
                    L.append(f" {i}. {strip_furigana(opt)}")
                L.append("")
            elif section == "問題3":
                L.append(f"**{slot}番** 1 ・ 2 ・ 3 ・ 4")
            elif section == "問題4":
                L.append(f"**{slot}番** 1 ・ 2 ・ 3")
            elif section == "問題5" and slot == 1:
                # spoken choices; the booklet prints only the bubbles
                L += ["**1番**", lead_in("問題5", 0), "",
                      "**1番** 1 ・ 2 ・ 3 ・ 4", "", "ーメモー", ""]
            else:
                # 問題5-2番's choices are NOT spoken by official, so they must
                # be printed — both question read-backs share one option list.
                L += ["**2番**", lead_in("問題5", 1), ""]
                for q in (1, 2):
                    L.append(f"**質問{q}**")
                    for i, opt in enumerate(exp[f"問5-2-{q}"]["options"], 1):
                        L.append(f" {i}. {strip_furigana(opt)}")
                    L.append("")
        if section in ("問題3", "問題4"):
            L += ["", "ーメモー", ""]

    L += ["# 解答用紙(マークシート)", "",
          "答えの番号に○をつけてください。"
          "（出典の台本に練習問題「例」の行がないため、例の欄はありません。）", ""]
    for section, count in SECTIONS.items():
        L.append(f"## {section}")
        if section == "問題5":
            L += ["| 1番 | 2番-質問1 | 2番-質問2 |", "|---|---|---|",
                  "| 1 2 3 4 | 1 2 3 4 | 1 2 3 4 |", ""]
            continue
        opts = "1 2 3" if section == "問題4" else "1 2 3 4"
        groups = [range(1, 7), range(7, count + 1)] if count > 6 else [range(1, count + 1)]
        for group in groups:
            nums = list(group)
            if not nums:
                continue
            L += ["| " + " | ".join(f"{n}番" for n in nums) + " |",
                  "|" + "---|" * len(nums),
                  "| " + " | ".join(opts for _ in nums) + " |", ""]

    L += ["# 【正解・解説】※解き終わってから見てください", ""]
    for section, count in SECTIONS.items():
        L += [f"## {section}", "| 番号 | 正解 | 解説 |", "|---|---|---|"]
        for slot in range(1, count + 1):
            item = placed[f"{section}-{slot}"]
            for key, ans in item["answers"].items():
                cell = item["kaisetsu_cell"].get(key, "")
                label = f"{slot}番"
                if key.startswith("問5-2-"):
                    label = f"2番-質問{key[-1]}"
                L.append(f"| {label} | {ans} | {cell} |")
        L.append("")

    L += ["## 得点の目安",
          "- 27〜30問：合格ライン以上",
          "- 18〜26問：合格圏内",
          "- 17問以下：N2聴解の聞き取りを強化", ""]
    return "\n".join(L)


# ---------------------------------------------------------------- audio

def cut(src: Path, start: float, end: float, dst: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error",
         "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(src),
         # Two of the ten imported sittings (2023-12, 2024-07) carry an
         # embedded cover image, so their MP3 has a second, video stream.
         # -map 0:a:0 pins the output to the audio one. It does NOT silence the
         # "[png] Invalid PNG signature" line those two print — that comes from
         # ffmpeg's INPUT probe and survives -vn, -map and stream selection
         # alike (checked 2026-09-08); only dropping below `error` hides it, and
         # a real decode error is worth more than a quiet log. The line is
         # cosmetic: `check=True` still catches an actual failure.
         "-map", "0:a:0",
         "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", "-y", str(dst)],
        check=True)


def silence(seconds: float, dst: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error",
         "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono",
         "-t", f"{seconds:.3f}", "-c:a", "pcm_s16le", "-y", str(dst)],
        check=True)


def wav_seconds(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def build_audio(index: dict, clips: dict, pres: dict, out_mp3: Path,
                work: Path) -> dict:
    """Cut every clip, lay the pauses between them, encode once."""
    plan: list[tuple[str, Path, str | None]] = []   # kind, wav, chapter label
    sources: dict[str, Path] = {}

    def source_for(rec: dict) -> Path:
        """Where this clip's audio lives — a sitting's MP3, or a textbook CD."""
        if "path" in rec["audio"]:
            path = ROOT / rec["audio"]["path"]
            if not path.is_file():
                book = "Soumatome" if rec["source"] == "soumatome" else "Shinkanzen"
                sys.exit(
                    f"missing textbook audio {rec['audio']['path']} for clip "
                    f"{rec['id']}. The CDs are release assets, not git objects "
                    f"(AGENTS.md §3) — restore with:\n"
                    f"  gh release download refs --pattern '{book}.zip' "
                    f"--dir /tmp && unzip -n /tmp/{book}.zip -d refs/")
            return path
        key = rec["source_test"]
        if key not in sources:
            path = ROOT / "tests" / key / "聴解.mp3"
            if not path.is_file():
                sys.exit(
                    f"missing source audio {path.relative_to(ROOT)} for clip "
                    f"{rec['id']}. The exam MP3s are release assets, not git "
                    f"objects (AGENTS.md §3) — restore with:\n"
                    f"  gh release download audio --pattern "
                    f"'{key}.mp3' --dir tests/{key}/")
            sources[key] = path
        return sources[key]

    n = 0

    def add_span(src: Path, start: float, end: float,
                 chapter: str | None) -> None:
        nonlocal n
        n += 1
        dst = work / f"{n:03d}_clip.wav"
        cut(src, start, end, dst)
        plan.append(("clip", dst, chapter))

    def add_clip(rec: dict, chapter: str | None) -> None:
        add_span(source_for(rec), rec["audio"]["start"], rec["audio"]["end"],
                 chapter)

    def add_pause(seconds: float) -> None:
        nonlocal n
        n += 1
        dst = work / f"{n:03d}_sil.wav"
        silence(seconds, dst)
        plan.append(("pause", dst, None))

    def add_item(rec: dict, slot: int, chapter: str) -> None:
        """One item, with its number call — spoken by the clip, or prepended.

        The chapter mark goes on the NUMBER, not on the body: an examinee
        jumping to 「7番」 expects to hear the announcer say it.
        """
        if not rec.get("needs_number_call"):
            add_clip(rec, chapter)
            return
        call = number_call(slot)
        add_span(ROOT / "tests" / call["source_test"] / "聴解.mp3",
                 call["start"], call["end"], chapter)
        add_pause(AFTER_NUMBER_CALL)
        add_clip(rec, None)

    for section, count in SECTIONS.items():
        add_clip(index[pres[section]], section)
        add_pause(AFTER_PREAMBLE)
        for slot in range(1, count + 1):
            add_item(index[clips[f"{section}-{slot}"]], slot,
                     f"{section} {slot}番")
            last = section == "問題5" and slot == count
            if not last:
                add_pause(ANSWER_PAUSE[section])
            # 問題5-2番 ends the paper: it carries its own trailing pause and
            # the closing announcement, so nothing is appended after it.

    listing = work / "concat.txt"
    listing.write_text(
        "".join(f"file '{p.as_posix()}'\n" for _, p, _ in plan),
        encoding="utf-8")
    merged = work / "merged.wav"
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error",
         "-f", "concat", "-safe", "0", "-i", str(listing),
         "-c", "copy", "-y", str(merged)], check=True)
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error",
         "-i", str(merged), "-af", LOUDNORM,
         "-c:a", "libmp3lame", "-b:a", "128k", "-ar", str(SR),
         "-y", str(out_mp3)], check=True)

    chapters, offset = [], 0.0
    for _kind, path, chapter in plan:
        if chapter:
            chapters.append({"label": chapter, "start": round(offset, 3)})
        offset += wav_seconds(path)
    return {"duration": round(offset, 3), "chapters": chapters}


# ---------------------------------------------------------------- explanations

def merge_explanations(test_dir: Path, index: dict, clips: dict) -> None:
    """Replace the 30 choukai entries in both panes, leaving 問1-71 untouched."""
    for name, field in (("詳細解説.json", "explanation"),
                        ("詳細解説.vi.json", "explanation_vi")):
        path = test_dir / name
        data = (json.loads(path.read_text(encoding="utf-8"))
                if path.is_file() else {})
        for key in [k for k in data if k.startswith("問")]:
            del data[key]
        for item in ordered_items(index, clips):
            data.update(item[field])
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("test_id")
    ap.add_argument("--seed", type=int,
                    help="required unless --replay (which reuses the recorded "
                         "seed)")
    ap.add_argument("--replay", action="store_true",
                    help="reuse this test's RECORDED draw from "
                         "logs/choukai_draws.json instead of drawing. Required "
                         "with --no-audio: the draw depends on how many papers "
                         "have spent each clip, so re-drawing with the same "
                         "seed later gives a DIFFERENT paper, and the rewritten "
                         "text would then describe audio that is not on disk")
    ap.add_argument("--no-audio", action="store_true",
                    help="rewrite the text deliverables only, keeping the MP3. "
                         "Valid ONLY when the draw is unchanged (same seed and "
                         "same bank draw), because the audio is a pure function "
                         "of the draw — use it after a rendering fix, never "
                         "after a re-draw")
    args = ap.parse_args(argv)

    if args.seed is None and not args.replay:
        sys.exit("--seed is required (an RNG output, never a chosen number)")
    test_dir = ROOT / "tests" / args.test_id
    if not test_dir.is_dir():
        sys.exit(f"no such test: {test_dir.relative_to(ROOT)}")

    bank = load_bank()
    index = by_id(bank)
    draws = load_draws()

    if args.replay:
        prior = next((r for r in draws["history"]
                      if r["test_id"] == args.test_id), None)
        if prior is None:
            sys.exit(f"--replay: no recorded draw for {args.test_id} in "
                     f"{DRAWS_PATH.relative_to(ROOT)}")
        clips, pres = prior["clips"], prior["preambles"]
        args.seed = prior["seed"]
    else:
        if args.no_audio:
            sys.exit("--no-audio without --replay would re-draw the paper and "
                     "leave the text describing audio that is not on disk; "
                     "pass --replay to re-render the existing draw")
        used = usage_counts(draws, exclude=args.test_id)
        clips, pres = draw(bank, args.seed, used, args.test_id)

    (test_dir / "聴解スクリプト.txt").write_text(
        render_script(index, clips, pres), encoding="utf-8")
    (test_dir / "聴解.md").write_text(
        render_booklet(index, clips, pres), encoding="utf-8")
    merge_explanations(test_dir, index, clips)

    if not args.no_audio:
        work = Path(tempfile.mkdtemp(prefix=f"choukai-{args.test_id}-"))
        try:
            marks = build_audio(index, clips, pres,
                                test_dir / "聴解.mp3", work)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        marks["source"] = "composed"
        marks["bank_version"] = bank["version"]
        # Same contract as the TTS path: mechanical evidence that the audio on
        # disk speaks the script on disk. `pacing_sha` has no analogue — the
        # pauses come from the pacing table via this file, and the speech comes
        # from the archive, so there are no synthesis constants to hash.
        marks["script_sha"] = hashlib.sha1(
            (test_dir / "聴解スクリプト.txt").read_bytes()).hexdigest()[:12]
        (test_dir / "聴解_チャプター.json").write_text(
            json.dumps(marks, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        print(f"{args.test_id}: {marks['duration'] / 60:.1f} min, "
              f"{len(marks['chapters'])} chapters")
    else:
        # The script bytes just changed, so the stamp that proves "this MP3
        # speaks this script" has to be re-taken. Legitimate here and only here:
        # the audio is a pure function of the draw, the draw did not move, and
        # the caller asserted that by passing --no-audio.
        marks_path = test_dir / "聴解_チャプター.json"
        if marks_path.is_file():
            marks = json.loads(marks_path.read_text(encoding="utf-8"))
            if marks.get("source") == "composed":
                marks["script_sha"] = hashlib.sha1(
                    (test_dir / "聴解スクリプト.txt").read_bytes()
                ).hexdigest()[:12]
                marks_path.write_text(
                    json.dumps(marks, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
                print(f"{args.test_id}: text rewritten, script_sha refreshed")

    draws["history"] = [r for r in draws["history"]
                        if r["test_id"] != args.test_id]
    draws["history"].append({
        "test_id": args.test_id,
        "seed": args.seed,
        # The mix is the point of the mixed pool, so it is RECORDED rather than
        # left to be re-derived by joining this file against the bank.
        "sources": dict(sorted(Counter(
            index[i].get("source", "official")
            for i in clips.values()).items())),
        "clips": clips,
        "preambles": pres,
    })
    DRAWS_PATH.write_text(
        json.dumps(draws, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    mix = Counter(index[i].get("source", "official") for i in clips.values())
    sittings = Counter(index[i]["sitting"] for i in clips.values()
                       if index[i].get("source", "official") == "official")
    print("  source mix: "
          + ", ".join(f"{k} ×{v}" for k, v in sorted(mix.items()))
          + (" (official-only paper)" if args.test_id in OFFICIAL_ONLY_TESTS
             else ""))
    print(f"  drew from {len(sittings)} sittings: "
          + ", ".join(f"{k}×{v}" for k, v in sorted(sittings.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
