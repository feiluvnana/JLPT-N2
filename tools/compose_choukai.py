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

Slot-preserving draws
---------------------
Item *k* of 問題N is drawn only from item *k* of 問題N in some sitting. Official
runs 「N番。」 continuously into the situation line with no pause between them,
so renumbering would mean cutting inside speech; keeping the slot means every
cut lands in a structural silence and the announcer's own numbering stays
correct. Each slot has one candidate per sitting, so ten.

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


def draw(bank: dict, seed: int, used: Counter,
         attempts: int = 400) -> tuple[dict, dict]:
    """Pick one record per slot and one preamble per section.

    Two objectives, in order: spend the least-used clips first (so the ten
    sittings rotate evenly across the suite rather than one being mined), then
    among equally-fresh combinations prefer a flat answer-key spread.
    """
    rng = random.Random(seed)
    items: dict[tuple[str, int], list[dict]] = {}
    preambles: dict[str, list[dict]] = {}
    for rec in bank["records"]:
        if rec["kind"] == "item":
            items.setdefault((rec["section"], rec["slot"]), []).append(rec)
        else:
            preambles.setdefault(rec["section"], []).append(rec)

    for section, count in SECTIONS.items():
        for slot in range(1, count + 1):
            if (section, slot) not in items:
                sys.exit(f"bank has no candidates for {section}-{slot}")

    best = None
    for _ in range(attempts):
        picked = []
        for section, count in SECTIONS.items():
            for slot in range(1, count + 1):
                pool = items[(section, slot)]
                fewest = min(used[r["id"]] for r in pool)
                fresh = [r for r in pool if used[r["id"]] == fewest]
                picked.append(rng.choice(fresh))
        score = (sum(used[r["id"]] for r in picked), key_spread(picked))
        if best is None or score < best[0]:
            best = (score, picked)

    _, picked = best
    chosen_items = {f"{r['section']}-{r['slot']}": r["id"] for r in picked}
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
    out = []
    for section, count in SECTIONS.items():
        for slot in range(1, count + 1):
            out.append(index[clips[f"{section}-{slot}"]])
    return out


def render_script(index: dict, clips: dict, pres: dict) -> str:
    """`聴解スクリプト.txt` — exactly what the composed audio says.

    The 例 is absent here and present in the audio, the same divergence every
    `tests/imported-*` sitting carries: the official script PDFs do not print
    the practice items, so no transcript of them exists in this repo. The 例
    audio rides inside the section preamble clip, uncut.
    """
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
            parts.append(index[clips[f"{section}-{slot}"]]["script"])
            parts.extend(block for pos, block in pre if pos == slot)
    return "\n\n".join(p.strip() for p in parts if p.strip()) + "\n"


def render_booklet(index: dict, clips: dict, pres: dict) -> str:
    """`聴解.md` — printed options, mark sheet, and the key/解説 tables."""
    L = ["# 【聴解】", ""]

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
            rec = index[clips[f"{section}-{slot}"]]
            exp = rec["explanation"]
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
            rec = index[clips[f"{section}-{slot}"]]
            for key, ans in rec["answers"].items():
                cell = rec["kaisetsu_cell"].get(key, "")
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

    def add_clip(rec: dict, chapter: str | None) -> None:
        nonlocal n
        n += 1
        dst = work / f"{n:03d}_clip.wav"
        cut(source_for(rec), rec["audio"]["start"], rec["audio"]["end"], dst)
        plan.append(("clip", dst, chapter))

    def add_pause(seconds: float) -> None:
        nonlocal n
        n += 1
        dst = work / f"{n:03d}_sil.wav"
        silence(seconds, dst)
        plan.append(("pause", dst, None))

    for section, count in SECTIONS.items():
        add_clip(index[pres[section]], section)
        add_pause(AFTER_PREAMBLE)
        for slot in range(1, count + 1):
            add_clip(index[clips[f"{section}-{slot}"]], f"{section} {slot}番")
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
        for rec in ordered_items(index, clips):
            data.update(rec[field])
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
        clips, pres = draw(bank, args.seed, used)

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
        "clips": clips,
        "preambles": pres,
    })
    DRAWS_PATH.write_text(
        json.dumps(draws, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    sittings = Counter(index[i]["sitting"] for i in clips.values())
    print(f"  drew from {len(sittings)} sittings: "
          + ", ".join(f"{k}×{v}" for k, v in sorted(sittings.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
