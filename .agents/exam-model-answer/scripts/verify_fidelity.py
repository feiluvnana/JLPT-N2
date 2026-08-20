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
  - 聴解 script fields may use `<br>` between speaker turns where the source
    has a bare newline. (The restated question IS part of `script` for 問題1-4
    and for a one-question 問5; only a two-question 問5 keeps 質問1/質問2 in
    `stem` alone, since one talk feeds two items.)
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
SECTION_RE = re.compile(r"^##[ \t]*問題(\d+)(?:[ \t]+\S.*)?$", re.M)


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


def _strip_stem_option_spans(text: str, matches, offset: int = 0) -> str:
    """`text` with every STEM_BLOCK_RE match's span removed, for passage use.

    `offset` rebases the match spans, which are indices into the WHOLE section
    body, onto `text` when `text` is a slice of that body (one ### subsection).
    Without it the cut landed `offset` characters too late: the passage of a
    問題10/問題11 subsection kept the head of its own stem (`…**52** 市が`), and
    every later subsection -- where the offset exceeds the subsection's own
    length -- had nothing removed at all, so the numbered option lines (and, on
    a two-question passage, the next item's whole block) were served to the
    learner as part of the reading text. Found 2026-08-20 in 20260819_1 and
    present in every earlier paper's 詳細解説.json passages.
    """
    out, last = [], 0
    for m in matches:
        start, end = m.start() - offset, m.end() - offset
        if end <= 0 or start >= len(text):
            continue
        out.append(text[last:max(last, start)])
        last = max(last, end)
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
                sub_texts.append(
                    _strip_stem_option_spans(sub_body, sub_stems, sub_start))
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
    """Printed options for 問題1-2 (問3/4/5 print only placeholder numerals, so
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


SPEAKER_LINE_RE = re.compile(r"^[^\n:：]{1,6}[:：]")
SPOKEN_QUESTION_RE = re.compile(r"^質問([12])[。.][ \t]*(.*)$")
SPOKEN_OPTION_RE = re.compile(r"^([1-4])[、.][ \t]*(.*)$")


def _split_spoken_block(rest: str):
    """(narration_lines, option_groups, questions) for a 問題3/4/5 script block.

    The booklet prints no options for these sections, so they come out of the
    script itself. Three shapes have to survive the same splitter:
      問題3/問5 one-question — narration, then ONE numbered option group;
      問題4                 — one prompt line, then ONE 3-option group;
      問5 two-question      — narration, 質問1 + group, 質問2 + group.
    Anything after an option group that is neither a further 質問 nor a further
    numbered option is the announcer's instruction for the NEXT item (or the
    closing 「これで、聴解試験を終わります。」) and is dropped: it used to be
    concatenated onto the last option's text.
    """
    narration, groups, questions = [], [], []
    cur, seen_opts = None, False
    for line in rest.splitlines():
        line = line.strip()
        if not line:
            continue
        m_q = SPOKEN_QUESTION_RE.match(line)
        if m_q:
            questions.append((int(m_q.group(1)), m_q.group(2).strip()))
            cur = None
            continue
        m_o = SPOKEN_OPTION_RE.match(line)
        if m_o:
            if m_o.group(1) == "1" or cur is None:
                cur = []
                groups.append(cur)
            cur.append(m_o.group(2).strip())
            seen_opts = True
            continue
        cur = None
        if not seen_opts and not questions:
            narration.append(line)
    return narration, groups, questions


def _narration_parts(lines: list):
    """(lead_in, trailing_narration) around the block's speaker turns.

    The lead-in ("ラジオで、店長が話しています。") and the restated question
    ("店長は何について話していますか。") are the announcer's, not a speaker's:
    together they are what the item ASKS, and the booklet prints neither.
    """
    speakers = [i for i, l in enumerate(lines) if SPEAKER_LINE_RE.match(l)]
    if not speakers:
        return "\n".join(lines).strip(), ""
    return ("\n".join(lines[:speakers[0]]).strip(),
            "\n".join(lines[speakers[-1] + 1:]).strip())


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
            # 問題1-2: booklet prints the options; the script's lead-in
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
            continue

        # 問題3/4/5: the options are spoken, not printed.
        narration, groups, questions = _split_spoken_block(rest)
        lead_in, tail = _narration_parts(narration)

        if key_id.startswith("問4"):
            # 即時応答: the whole prompt is the stem, there is no transcript
            # to show separately.
            items[key_id] = {"stem": "\n".join(narration),
                             "options": groups[0] if groups else [],
                             "script": None}
        elif len(questions) >= 2 and len(groups) >= 2:
            # 問5 統合理解, two questions over one talk. It has to become TWO
            # entries: 聴解.md keys the rows 問5-N-1/問5-N-2 and the answer key
            # is per question, so a single 8-option entry could never be tagged
            # against one answer value (build_model_answer.explanation_box_html
            # tags [正解] by index). Each half keeps its own 4 options.
            script = "\n".join(narration)
            for group, (q_n, q_text) in zip(groups, questions):
                items[f"{key_id}-{q_n}"] = {
                    "stem": f"{lead_in}質問{q_n}　{q_text}",
                    "options": group,
                    "script": script,
                }
        else:
            # 問題3 概要理解 / 問5 one-question: the announcer's lead-in and
            # restated question make the stem; the whole narration is the
            # transcript.
            items[key_id] = {"stem": f"{lead_in}{tail}",
                             "options": groups[0] if groups else [],
                             "script": "\n".join(narration)}
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
