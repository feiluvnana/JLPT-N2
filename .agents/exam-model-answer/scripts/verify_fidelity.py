#!/usr/bin/env python3
"""
Derive stem/options/passage/script straight from the exam's own source files
(言語知識・読解.md, 聴解.md, 聴解スクリプト.txt) and compare them against what
is hand-typed in tests/<test_id>/詳細解説.json.

Why this exists: 詳細解説.json's stem/options/passage/script text used to be
retyped by hand (or by a one-off per-test "compiler" script) from the exam
source so furigana could be added. Retyping drifts: a 2026-08 audit found 30
items across several tests where the retype had dropped an opening <strong>
tag entirely (the sentence rendered without its target-word bolding), because
nothing checked the retyped copy against the source it was copied from. This
script IS that check, and it replaces the per-test "compiler script" pattern:
run it once per test instead of writing a new script per test.

Usage:
    python3 verify_fidelity.py tests/<test_id>              # report mismatches

A "mismatch" compares text with furigana/<ruby>/<strong> markup stripped from
both sides, so adding furigana is never flagged -- only wording drift is.

This is report-only, on purpose -- there is no --write/auto-fix mode. Two
mismatch shapes are EXPECTED and not bugs, so blind auto-fixing would destroy
real content:
  - 問6 (用法) stems, and any 問9 (文章の文法) cloze item, legitimately prepend
    the section instruction line for readability; the source alone is just
    the bare target word / blank marker.
  - 聴解 script fields legitimately end before the announcer's restated
    question (kept in `stem`/narration instead, not duplicated into `script`)
    and use `<br>` between speaker turns where the source has a bare newline.
Everything else that's flagged -- a dropped <strong>, a passage left empty on
the 2nd+ question of a shared reading passage, option wording that doesn't
match the booklet -- is a real defect: fix it by hand, re-deriving the
wording from the `source` line this script prints.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_model_answer import (  # noqa: E402
    GENGO_TAXONOMY,
    parse_choukai_scripts,
)

KANJI_RANGE = "一-鿿"
STEM_BLOCK_RE = re.compile(
    r"\*\*(?P<num>\d{1,3})\*\*[ \t]*(?P<stem>.*?)(?=\n[ \t]*1[.．][ \t]|\Z)"
    r"(?P<optblock>.*?)(?=\n\*\*\d{1,3}\*\*|\n#{2,3}[ \t]|\Z)",
    re.S,
)
OPT_ITEM_RE = re.compile(r"[1-4][.．][ \t]*(.*?)(?=[ \t\n]*[1-4][.．][ \t]|\Z)", re.S)
SUBSECTION_RE = re.compile(r"^###[ \t]*(.+?)[ \t]*$", re.M)
SECTION_RE = re.compile(r"^##[ \t]*問題(\d+)[ \t]*$", re.M)


def strip_markup(text: str) -> str:
    """Normalize away everything that is allowed to differ: furigana, <ruby>,
    <strong>/**bold**, and whitespace. What's left is the wording itself."""
    if not text:
        return ""
    text = re.sub(r"<ruby>([^<]+)<rt>[^<]*</rt></ruby>", r"\1", text)
    text = re.sub(r"｜?([" + KANJI_RANGE + r"]+)《[^》]+》", r"\1", text)
    text = re.sub(r"《[^》]+》", "", text)
    text = text.replace("<strong>", "").replace("</strong>", "")
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\s+", "", text)
    return text


def _strip_stem_option_spans(text: str, matches) -> str:
    """`text` with every STEM_BLOCK_RE match's span removed, for passage use."""
    out, last = [], 0
    for m in matches:
        out.append(text[last:m.start()])
        last = m.end()
    out.append(text[last:])
    return "".join(out).strip()


def _split_options(optblock: str):
    return [m.group(1).strip() for m in OPT_ITEM_RE.finditer(optblock)]


def derive_gengo_raw(exam_body: str) -> dict:
    """{q_num: {"stem": raw, "options": [raw,...], "passage": raw|None}}"""
    items = {}
    for sec_m in SECTION_RE.finditer(exam_body):
        sec_num = int(sec_m.group(1))
        start = sec_m.end()
        next_sec = SECTION_RE.search(exam_body, start)
        end = next_sec.start() if next_sec else len(exam_body)
        # a language-knowledge section also ends at the answer-key heading
        key_m = re.search(r"^#\s*(?:解答|【?正解)", exam_body[start:end], re.M)
        if key_m:
            end = start + key_m.start()
        body = exam_body[start:end]

        stem_matches = list(STEM_BLOCK_RE.finditer(body))
        subsections = list(SUBSECTION_RE.finditer(body))

        if subsections:
            bounds = [m.start() for m in subsections] + [len(body)]
            sub_texts, sub_stem_matches = [], []
            for i, sm in enumerate(subsections):
                sub_start, sub_end = sm.end(), bounds[i + 1]
                sub_body = body[sub_start:sub_end]
                sub_stems = [m for m in stem_matches
                             if sub_start <= m.start() < sub_end]
                sub_texts.append(_strip_stem_option_spans(sub_body, sub_stems))
                sub_stem_matches.append(sub_stems)

            in_any_sub = {m for stems in sub_stem_matches for m in stems}
            orphan_stems = [m for m in stem_matches if m not in in_any_sub]

            for sub_text, sub_stems in zip(sub_texts, sub_stem_matches):
                passage = sub_text if sub_text.strip() else None
                for m in sub_stems:
                    items[int(m.group("num"))] = {
                        "stem": m.group("stem").strip(),
                        "options": _split_options(m.group("optblock")),
                        "passage": passage,
                    }
            if orphan_stems:
                shared = "\n\n".join(t for t in sub_texts if t.strip())
                for m in orphan_stems:
                    items[int(m.group("num"))] = {
                        "stem": m.group("stem").strip(),
                        "options": _split_options(m.group("optblock")),
                        "passage": shared or None,
                    }
        else:
            leftover = _strip_stem_option_spans(body, stem_matches)
            # drop the one-line instruction sentence at the very top when
            # judging whether real passage prose remains
            instr_free = re.sub(r"^.*?(?:選びなさい|入れなさい)。?", "", leftover,
                                 count=1, flags=re.S).strip()
            passage = leftover.strip() if len(instr_free) > 5 else None
            for m in stem_matches:
                items[int(m.group("num"))] = {
                    "stem": m.group("stem").strip(),
                    "options": _split_options(m.group("optblock")),
                    "passage": passage,
                }
    return items


CHOUKAI_MD_SEC_RE = re.compile(r"^##[ \t]*問題([1-5])[ \t]*$", re.M)
CHOUKAI_ITEM_RE = re.compile(
    r"\*\*(?P<label>\d+番|質問[12])\*\*[ \t]*(?P<opts>(?:1[ \t]*[・.][^\n]*)?)\n?",
)


def derive_choukai_options_from_md(choukai_body: str) -> dict:
    """Printed options for 問題1-3 (問4/5 print only placeholder numerals, so
    they come back empty here -- derive_choukai_raw falls back to the script
    for those)."""
    out = {}
    for sec_m in CHOUKAI_MD_SEC_RE.finditer(choukai_body):
        sec_num = int(sec_m.group(1))
        start = sec_m.end()
        next_sec = CHOUKAI_MD_SEC_RE.search(choukai_body, start)
        end = next_sec.start() if next_sec else len(choukai_body)
        body = choukai_body[start:end]
        for m in re.finditer(r"\*\*(\d+)番\*\*\n((?:[ \t]*[1-4]\.[^\n]*\n?)+)",
                              body):
            n, block = int(m.group(1)), m.group(2)
            opts = [o.strip() for o in
                    re.split(r"[ \t]*[1-4]\.[ \t]*", block) if o.strip()]
            if opts and sec_num in (1, 2, 3):
                out[f"問{sec_num}-{n}"] = opts
    return out


def derive_choukai_raw(choukai_body: str, script_text: str) -> dict:
    """{key_id: {"stem": raw, "options": [raw,...], "script": raw|None}}"""
    items = {}
    md_options = derive_choukai_options_from_md(choukai_body)
    blocks = parse_choukai_scripts(script_text)

    for key_id, block in blocks.items():
        m_head = re.match(r"^(?:\d+番|質問[12])[。.][ \t]*", block)
        if not m_head:
            continue
        rest = block[m_head.end():]
        if key_id in md_options:
            # 問題1-3: booklet prints the options; the script's lead-in
            # sentence up to the first speaker turn is the stem, everything
            # after (including any restated question) is the script.
            speaker_m = re.search(r"^[^\n:：]{1,6}[:：]", rest, re.M)
            if speaker_m:
                stem = rest[:speaker_m.start()].strip()
                script = rest[speaker_m.start():].strip()
            else:
                stem, script = rest.strip(), None
            items[key_id] = {"stem": stem, "options": md_options[key_id],
                              "script": script}
        else:
            # 問題4/5: booklet prints no options -- they are spoken. Split off
            # the trailing "1、…\n2、…\n3、…[\n4、…]" block as options; what
            # remains is stem (問4: the single prompt line) or script (問5:
            # the monologue/dialogue, ending in the restated question).
            opt_m = re.search(
                r"(?:^|\n)1[、.][ \t]*.*$", rest, re.S)
            if opt_m:
                pre = rest[:opt_m.start()].strip()
                opts = [o.strip() for o in
                        re.split(r"(?:^|\n)[1-4][、.][ \t]*", rest[opt_m.start():])
                        if o.strip()]
            else:
                pre, opts = rest.strip(), []
            if key_id.startswith("問4"):
                items[key_id] = {"stem": pre, "options": opts, "script": None}
            else:  # 問5
                items[key_id] = {"stem": pre if "質問" in key_id else "",
                                  "options": opts,
                                  "script": None if "質問" in key_id else pre}
    return items


def load_sources(test_dir: Path):
    gengo_md = (test_dir / "言語知識・読解.md").read_text(encoding="utf-8")
    choukai_md = (test_dir / "聴解.md").read_text(encoding="utf-8")
    script_path = test_dir / "聴解スクリプト.txt"
    script_text = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""
    return gengo_md, choukai_md, script_text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir")
    args = ap.parse_args()

    test_dir = Path(args.test_dir)
    detail_path = test_dir / "詳細解説.json"
    detail = json.loads(detail_path.read_text(encoding="utf-8")) if detail_path.is_file() else {}

    gengo_md, choukai_md, script_text = load_sources(test_dir)
    gengo_raw = derive_gengo_raw(gengo_md)
    choukai_raw = derive_choukai_raw(choukai_md, script_text)

    mismatches = []

    def check(key, field, derived, existing):
        if derived is None:
            return
        if strip_markup(derived) != strip_markup(existing or ""):
            mismatches.append((key, field, derived, existing))

    for q_num, raw in gengo_raw.items():
        d = detail.get(str(q_num), {})
        check(str(q_num), "stem", raw["stem"], d.get("stem"))
        for i, opt in enumerate(raw["options"]):
            existing_opts = d.get("options") or []
            check(str(q_num), f"options[{i}]", opt,
                  existing_opts[i] if i < len(existing_opts) else None)
        check(str(q_num), "passage", raw["passage"], d.get("passage"))

    for key_id, raw in choukai_raw.items():
        d = detail.get(key_id, {})
        check(key_id, "stem", raw["stem"], d.get("stem"))
        for i, opt in enumerate(raw["options"]):
            existing_opts = d.get("options") or []
            check(key_id, f"options[{i}]", opt,
                  existing_opts[i] if i < len(existing_opts) else None)
        check(key_id, "script", raw["script"], d.get("script"))

    if not mismatches:
        print(f"{test_dir}: 詳細解説.json matches the exam source exactly "
              f"(wording-only comparison, furigana ignored).")
        return

    print(f"{test_dir}: {len(mismatches)} field(s) drifted from the exam source "
          f"(see the module docstring for which shapes are expected, not bugs):")
    for key, field, derived, existing in mismatches:
        print(f"  [{key}].{field}")
        print(f"    source : {derived[:160]!r}")
        print(f"    json   : {(existing or '')[:160]!r}")


if __name__ == "__main__":
    main()
