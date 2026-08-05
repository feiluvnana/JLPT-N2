#!/usr/bin/env python3
"""
Consistency checker for the JLPT pipeline — run with `make check`.

Every failure this catches is a real bug that shipped at least once: a doc naming
a file no script writes, a pacing constant that stopped matching its table, an
answer-key heading the sheet builder needs but no doc mentioned, two graders
drifting apart. The docs are prose and cannot be executed, so this asserts the
handful of facts they duplicate from the code.

Read-only: it never writes to tests/ or logs/.

    python3 tools/check_consistency.py            # everything
    python3 tools/check_consistency.py --tests    # only the per-test contracts
"""

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".agents"
SKILL_DIRS = sorted(p for p in AGENTS.iterdir() if (p / "SKILL.md").is_file())

_fail: list[str] = []
_skip: list[str] = []
_warn: list[str] = []


def load(rel: str):
    """Import one of the pipeline scripts by path."""
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(name: str, ok: bool, detail: str = "") -> bool:
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        _fail.append(f"{name}: {detail}" if detail else name)
    return ok


def skip(name: str, why: str):
    print(f"  skip  {name} — {why}")
    _skip.append(name)


def warn(name: str, ok: bool, detail: str = ""):
    """Report a suspicion without failing the gate.

    For rules that are real but not decidable by string matching — a 解説 may
    legitimately put its own prose in 「」. A warn line is not noise to scroll
    past: resolve each one or say in your final report why it is a false
    positive (AGENTS.md §0.5).
    """
    print(f"  {'ok  ' if ok else 'WARN'}  {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        _warn.append(f"{name}: {detail}")


def docs() -> dict[Path, str]:
    files = {ROOT / "AGENTS.md": (ROOT / "AGENTS.md").read_text(encoding="utf-8")}
    for d in SKILL_DIRS:
        f = d / "SKILL.md"
        files[f] = f.read_text(encoding="utf-8")
    return files


def num(s: str) -> float:
    return float(re.search(r"[\d.]+", s).group())


# ---------------------------------------------------------------- refs on disk
def check_refs():
    print("\nrefs/ paths named in the docs exist")
    seen: dict[str, list[str]] = {}
    for f, text in docs().items():
        for m in re.finditer(r'[`"](refs/[^`"\n]+)[`"]', text):
            p = m.group(1).strip().rstrip("/")
            if any(x in p for x in ("<", ">", "*", "…", "...")):
                continue          # naming pattern, not a concrete file
            seen.setdefault(p, []).append(f.relative_to(ROOT).as_posix())
    missing = {p: w for p, w in seen.items() if not (ROOT / p).exists()}
    check(f"{len(seen)} distinct refs paths resolve", not missing,
          "; ".join(f"{p} (cited in {', '.join(w)})" for p, w in missing.items()))


# ------------------------------------------------------------------ skill wiring
def check_skills():
    print("\nskill wiring (.agents ↔ AGENTS.md ↔ .claude/skills)")
    agents_md = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^\s*\d+\.\s+`([a-z0-9-]+)`", agents_md, re.M))
    names = {d.name for d in SKILL_DIRS}

    check(f"AGENTS.md lists all {len(names)} skills", listed >= names,
          f"unlisted: {sorted(names - listed)}")
    check("AGENTS.md lists no skill that is missing from .agents/", listed <= names,
          f"stale entries: {sorted(listed - names)}")

    bad_fm, bad_link = [], []
    for d in SKILL_DIRS:
        fm = re.search(r"^name:\s*(\S+)", (d / "SKILL.md").read_text(encoding="utf-8"), re.M)
        if not fm or fm.group(1) != d.name:
            bad_fm.append(f"{d.name} (frontmatter: {fm.group(1) if fm else 'none'})")
        link = ROOT / ".claude" / "skills" / d.name
        if not link.is_symlink() or link.resolve() != d.resolve():
            bad_link.append(d.name)
    check("frontmatter name matches directory name", not bad_fm, ", ".join(bad_fm))
    check("every skill is symlinked under .claude/skills/", not bad_link,
          f"missing/broken: {bad_link}")


# --------------------------------------------------- documented output filenames
def check_filename_contracts():
    print("\ndocumented deliverable names appear in the script that writes them")
    contracts = [
        ("解答.html", ".agents/interactive-answer-sheet/scripts/build_interactive.py"),
        ("採点結果.json", ".agents/interactive-answer-sheet/scripts/build_interactive.py"),
        ("採点結果.json", ".agents/exam-answer-grading/scripts/grade_answers.py"),
        ("ユーザー解答.json", ".agents/interactive-answer-sheet/scripts/build_interactive.py"),
        ("ユーザー解答.json", ".agents/interactive-answer-sheet/scripts/serve_sheet.py"),
        ("聴解.mp3", ".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py"),
        ("聴解_チャプター.json", ".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py"),
        ("ledger.json", ".agents/item-pool-sampling/scripts/sample_items.py"),
        ("test_spec.json", ".agents/item-pool-sampling/scripts/sample_items.py"),
        ("adjunct_staging.json", ".agents/item-pool-sampling/scripts/classify_level.py"),
        ("import_meta.json", ".agents/external-test-import/scripts/init_imported_test.py"),
    ]
    for literal, script in contracts:
        src = (ROOT / script).read_text(encoding="utf-8")
        check(f"{literal} written by {Path(script).name}", literal in src)

    # Filenames and commands retired by the merge to a single sheet, and then by
    # the move to one server + a JSON result document, must not come back.
    retired = ["言語知識・読解_解答.html", "聴解_解答.html", "採点結果_",
               "採点結果.md", "user_answers", "マークシート.pdf",
               "make serve 1", "make serve <test_id>"]
    exonerated = re.compile(r"gone|no per-section|legacy|removed|replaces|there are no")
    offenders = []
    for f, text in docs().items():
        # A doc may name a retired file in order to say it is GONE, and that
        # disclaimer can sit anywhere in the sentence — which wraps across
        # lines. So judge each paragraph as a whole.
        line_no = 1
        for para in re.split(r"\n\s*\n", text):
            if not exonerated.search(para):
                for r in retired:
                    if r in para:
                        offenders.append(f"{f.relative_to(ROOT)}:~{line_no} {r}")
            line_no += para.count("\n") + 2
    check("no doc resurrects a retired filename", not offenders, "; ".join(offenders))


# ------------------------------------------------------------------ choukai pacing
def check_pacing():
    print("\nchoukai pacing table ↔ make_choukai_mp3.py constants")
    m = load(".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py")
    doc = (AGENTS / "choukai-mp3-generation" / "SKILL.md").read_text(encoding="utf-8")

    for const in ("GAP_BETWEEN_LINES", "GAP_AFTER_PRE_QUESTION", "GAP_OPTION_READING",
                  "GAP_BETWEEN_SPOKEN_CHOICES", "GAP_AFTER_SHITSUMON1"):
        row = re.search(rf"^\|\s*{const}\s*\|([^|]+)\|", doc, re.M)
        if not row:
            check(f"{const} documented", False, "no row in the pacing table")
            continue
        check(f"{const} = {getattr(m, const)}s", num(row.group(1)) == getattr(m, const),
              f"doc says {num(row.group(1))}, code says {getattr(m, const)}")

    row = re.search(r"^\|\s*ANSWER_PAUSE\s*\|([^|]+)\|", doc, re.M)
    if row:
        documented = {}
        for grp, val in re.findall(r"問([\d/]+):\s*(\d+)\s*s", row.group(1)):
            for n in grp.split("/"):
                documented[f"問題{n}"] = float(val)
        check("ANSWER_PAUSE matches the doc", documented == m.ANSWER_PAUSE,
              f"doc {documented} vs code {m.ANSWER_PAUSE}")

    # The dry-run pause distribution is derivable; assert the doc's numbers.
    expected: dict[float, int] = {}
    for sec, items in m.EXPECTED_ITEMS.items():
        expected[m.ANSWER_PAUSE[sec]] = expected.get(m.ANSWER_PAUSE[sec], 0) + items
    for secs, count in re.findall(r"^\|\s*(\d+) s answer\s*\|\s*(\d+)\s*\|", doc, re.M):
        check(f"dry-run: {count} × {secs}s answer pauses",
              expected.get(float(secs)) == int(count),
              f"doc {count}, derived {expected.get(float(secs))}")
    reading = re.search(r"^\|\s*20 s option-reading\s*\|\s*(\d+)\s*\|", doc, re.M)
    if reading:
        check(f"dry-run: {reading.group(1)} × 20s option-reading pauses",
              int(reading.group(1)) == m.EXPECTED_ITEMS["問題2"],
              f"doc {reading.group(1)}, 問題2 has {m.EXPECTED_ITEMS['問題2']} items")


# ------------------------------------------------------------------- item counts
def check_item_counts():
    print("\n聴解 item counts ↔ EXPECTED_ITEMS ↔ jlpt-exam-structure")
    m = load(".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py")

    sw = (AGENTS / "choukai-script-writing" / "SKILL.md").read_text(encoding="utf-8")
    row = re.search(r"Item counts \(incl\. 例\)\s*\|([^|]+)\|", sw)
    documented = {f"問題{n}": int(v) for n, v in re.findall(r"問題(\d)=(\d+)", row.group(1))} if row else {}
    check("choukai-script-writing item counts", documented == m.EXPECTED_ITEMS,
          f"doc {documented} vs code {m.EXPECTED_ITEMS}")

    struct = (AGENTS / "jlpt-exam-structure" / "SKILL.md").read_text(encoding="utf-8")
    block = struct.split("## 聴解")[1].split("##")[0]
    counts = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) >= 3 and cells[0].isdigit():
            counts[f"問題{cells[0]}"] = int(re.search(r"\d+", cells[2]).group())
    # 問題1-4 print one 例 on top of the scored items; 問題5 has 2 blocks, 3 answers.
    derived = {k: v - 1 for k, v in m.EXPECTED_ITEMS.items() if k != "問題5"}
    check("問題1-4 scored counts = EXPECTED_ITEMS − 例",
          {k: counts.get(k) for k in derived} == derived,
          f"doc {[counts.get(k) for k in derived]} vs derived {list(derived.values())}")
    check("問題5 = 3 answers from 2 blocks",
          counts.get("問題5") == 3 and m.EXPECTED_ITEMS["問題5"] == 2,
          f"doc {counts.get('問題5')} answers, code {m.EXPECTED_ITEMS['問題5']} blocks")
    total = sum(counts.values())
    check(f"聴解 totals {total} = 30 answers", total == 30)


# --------------------------------------------------------------------- taxonomy
def check_taxonomy():
    print("\ngengo taxonomy ↔ jlpt-exam-structure ↔ section scaling")
    g = load(".agents/exam-answer-grading/scripts/grade_answers.py")   # asserts tiling at import
    struct = (AGENTS / "jlpt-exam-structure" / "SKILL.md").read_text(encoding="utf-8")
    block = struct.split("## 言語知識")[1].split("## 聴解")[0]

    doc_rows = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) >= 4 and cells[0].isdigit():
            rng = re.match(r"(\d+)\s*-\s*(\d+)", cells[3])
            doc_rows[f"問{cells[0]}"] = (int(re.search(r'\d+', cells[2]).group()),
                                         (int(rng.group(1)), int(rng.group(2))) if rng else None)
    mismatched = [k for k, (cnt, rng) in doc_rows.items()
                  if k not in g.GENGO_QUESTION_TAXONOMY
                  or g.GENGO_QUESTION_TAXONOMY[k]["total"] != cnt
                  or g.GENGO_QUESTION_TAXONOMY[k]["range"] != rng]
    check(f"{len(doc_rows)} 大問 rows match GENGO_QUESTION_TAXONOMY", not mismatched,
          f"differ: {mismatched}")
    check("gengo table sums to 71", sum(c for c, _ in doc_rows.values()) == 71,
          f"sums to {sum(c for c, _ in doc_rows.values())}")

    sect = {}
    for s in g.GENGO_QUESTION_TAXONOMY.values():
        sect[s["section"]] = sect.get(s["section"], 0) + s["total"]
    grading_doc = (AGENTS / "exam-answer-grading" / "SKILL.md").read_text(encoding="utf-8")
    for label, key, want in (("言語知識", "言語知識", 51), ("読解", "読解", 20)):
        check(f"{label} = {want} items", sect.get(key) == want, f"taxonomy gives {sect.get(key)}")
        check(f"{label} {want} documented in exam-answer-grading",
              re.search(rf"{want} questions max|{want} items", grading_doc) is not None)


# ------------------------------------------- item-level content contracts
# Everything below caught a bug in test 2 as generated: two questions whose
# option list contained the same string twice (so two options were correct),
# a 問題8 key naming the option in the 2nd blank instead of the ★ (3rd) one,
# a cloze blank whose key pointed at a different option than its own
# explanation, and 問題5 2番 printing one option set while the audio spoke
# another. None of it is visible to the shape checks in check_tests().

def gengo_option_sets(md: str, bi) -> dict[int, list[str]]:
    """{question number: [option text, …]} from the question body only.

    Handles every layout in use: four options on their own line (問題1-5, 7, 8),
    one option per line (問題6, 10-14), and options trailing the stem itself on
    one line (test 1's 問題9).
    """
    def split_row(text: str) -> list[str]:
        return [p.strip() for p in re.split(r"(?<![^\s（(])[1-4]\.\s*", text.strip())
                if p.strip()]

    cut = bi.KEY_HEADING.search(md)
    body = md[: cut.start()] if cut else md
    out: dict[int, list[str]] = {}
    cur: int | None = None
    for line in body.splitlines():
        q = bi.GENGO_Q.match(line)
        if q:
            cur = int(q.group(1))
            rest = line[q.end():]
            out[cur] = split_row(rest) if bi.option_run(rest) else []
            continue
        if cur is None or not bi.OPTION.match(line):
            continue
        if bi.option_run(line):  # horizontal row: split it into its options
            out[cur] = split_row(line)
        else:
            out[cur].append(bi.OPTION.match(line).group(2).strip())
    return out


BLANK_RUN = re.compile(r"(?:[＿_]+★?[＿_]*|★)(?:\s*(?:[＿_]+★?[＿_]*|★))+")
JP_CHAR = re.compile(r"[\u3040-\u30ff\u4e00-\u9fffー。、！？（）「」『』…・]")
# Official N2 問題7 across refs/JLPT/ (5 papers): avg ~43, median ~41, IQR ~33–54.
P7_STEM_MIN = 30
P7_PAPER_AVG_MIN = 35
P9_PASSAGE_MIN = 450
# 問題8: official option-chunk mass (5 papers + 2018 sample / imported-n2-2025-07)
P8_OPT_SUM_MIN = 16
P8_LONG_OPTS_MIN = 2  # options with ≥5 JP chars
P8_ASSEMBLED_MIN = 45


def jp_char_count(s: str) -> int:
    return len(JP_CHAR.findall(re.sub(r"\s+", "", s)))


def check_grammar_stem_lengths(gt: str, bi):
    """問題7/9 carrier lengths must sit near the official JLPT band.

    Tests 1–4 shipped 問題7 stems averaging 20–34 JP chars against an official
    ~43 average — keys looked fine, carriers read as textbook drills. Fail hard
    on under-length stems/averages; warn when the paper average is merely soft.
    """
    cut = bi.KEY_HEADING.search(gt)
    body = gt[: cut.start()] if cut else gt
    m7 = re.search(r"^##\s*問題7\b.*?(?=^##\s*問題8\b)", body, re.M | re.S)
    m9 = re.search(r"^##\s*問題9\b.*?(?=^#\s*【?読解|^##\s*問題10\b)", body, re.M | re.S)

    stems7: list[tuple[int, int]] = []
    if m7:
        cur = None
        stem_buf: list[str] = []
        for line in m7.group(0).splitlines():
            q = bi.GENGO_Q.match(line)
            if q:
                if cur is not None and 31 <= cur <= 42:
                    stems7.append((cur, jp_char_count("".join(stem_buf))))
                cur = int(q.group(1))
                rest = line[q.end():]
                # stem may share the line with options; keep text before option run
                if bi.option_run(rest):
                    rest = re.split(r"(?<![^\s（(])[1-4]\.\s*", rest, maxsplit=1)[0]
                stem_buf = [rest]
                continue
            if cur is None:
                continue
            if bi.OPTION.match(line):
                if cur is not None and 31 <= cur <= 42:
                    stems7.append((cur, jp_char_count("".join(stem_buf))))
                cur = None
                stem_buf = []
                continue
            stem_buf.append(line)
        if cur is not None and 31 <= cur <= 42:
            stems7.append((cur, jp_char_count("".join(stem_buf))))

    short = [f"{q}({n})" for q, n in stems7 if n < P7_STEM_MIN]
    avg = (sum(n for _, n in stems7) / len(stems7)) if stems7 else 0.0
    check(f"問題7 stems each ≥{P7_STEM_MIN} JP chars "
          f"(official ~33–54; got {[n for _, n in stems7]})",
          len(stems7) == 12 and not short,
          f"short={short or 'n/a'}; rewrite situation carriers, not the keyed form")
    check(f"問題7 stem average ≥{P7_PAPER_AVG_MIN} JP chars "
          f"(official ~43; got {avg:.1f})",
          len(stems7) == 12 and avg >= P7_PAPER_AVG_MIN,
          "paper still reads as drill-length — lengthen scene-setting")

    if m9:
        # Drop the instruction header and the option lists (from **48** / 48 onward).
        sec = m9.group(0)
        sec = re.sub(r"^##\s*問題9[^\n]*\n", "", sec)
        sec = re.split(r"\n\*\*48\*\*|\n\*\*48\b|\n48\n", sec, maxsplit=1)[0]
        # Also stop at option rows that start a blank's choices without a bold num
        # on their own line (some tests put **48** then options).
        p9 = jp_char_count(sec)
        check(f"問題9 cloze passage ≥{P9_PASSAGE_MIN} JP chars "
              f"(official ~500–700; got {p9})",
              p9 >= P9_PASSAGE_MIN,
              "expand the cloze prose around the four blanks")


def check_mondai8_chunk_lengths(gt: str, opts: dict[int, list[str]], bi):
    """問題8 options must be N2-sized chunks, not four 2-char scraps.

    Official papers (and jlpt.jp 2018 sample) put real phrase mass in the four
    strips — sum often 16–29 JP chars, with several options ≥5. Test 1 shipped
    `わりに/ケーキは/とても/値段の` (sum 13).
    """
    cut = bi.KEY_HEADING.search(gt)
    body = gt[: cut.start()] if cut else gt
    m8 = re.search(r"^##\s*問題8\b.*?(?=^##\s*問題9\b)", body, re.M | re.S)
    stems: dict[int, str] = {}
    if m8:
        cur = None
        buf: list[str] = []
        for line in m8.group(0).splitlines():
            q = bi.GENGO_Q.match(line)
            if q:
                if cur is not None and 43 <= cur <= 47:
                    stems[cur] = "".join(buf)
                cur = int(q.group(1))
                rest = line[q.end():]
                if bi.option_run(rest):
                    rest = re.split(r"(?<![^\s（(])[1-4]\.\s*", rest, maxsplit=1)[0]
                buf = [rest]
                continue
            if cur is None:
                continue
            if bi.OPTION.match(line):
                if cur is not None and 43 <= cur <= 47:
                    stems[cur] = "".join(buf)
                cur = None
                buf = []
                continue
            buf.append(line)
        if cur is not None and 43 <= cur <= 47:
            stems[cur] = "".join(buf)

    bad_sum, bad_long, bad_asm = [], [], []
    for q in range(43, 48):
        o = opts.get(q) or []
        ol = [jp_char_count(x) for x in o]
        ssum = sum(ol)
        long_n = sum(1 for n in ol if n >= 5)
        asm = jp_char_count(stems.get(q, "")) + ssum
        if len(ol) != 4 or ssum < P8_OPT_SUM_MIN:
            bad_sum.append(f"{q}(sum={ssum}, opts={ol})")
        if long_n < P8_LONG_OPTS_MIN:
            bad_long.append(f"{q}(≥5chars:{long_n}, opts={ol})")
        if asm < P8_ASSEMBLED_MIN:
            bad_asm.append(f"{q}(assembled~{asm})")
    check(f"問題8 four options sum ≥{P8_OPT_SUM_MIN} JP chars each item",
          not bad_sum, "; ".join(bad_sum) + " — lengthen option chunks (see question-authoring)")
    check(f"問題8 each item has ≥{P8_LONG_OPTS_MIN} options of ≥5 JP chars",
          not bad_long, "; ".join(bad_long))
    check(f"問題8 assembled sentence ≥{P8_ASSEMBLED_MIN} JP chars",
          not bad_asm, "; ".join(bad_asm))


LEVEL_BAND_PATH = (
    AGENTS / "exam-qa-review" / "references" / "level_band_grammar.txt"
)


def load_level_band(path: Path = LEVEL_BAND_PATH) -> dict[str, list[str]]:
    """Parse TOO_HARD / TOO_EASY / ALLOW sections from the level-band list."""
    sections: dict[str, list[str]] = {"TOO_HARD": [], "TOO_EASY": [], "ALLOW": []}
    if not path.is_file():
        return sections
    cur = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        # Section headers use Markdown ## — strip comments only after that.
        if raw.lstrip().startswith("## "):
            name = raw.lstrip()[3:].split("#", 1)[0].strip().upper()
            cur = name if name in sections else None
            continue
        line = raw.split("#", 1)[0].strip()
        if not line or cur is None:
            continue
        sections[cur].append(line)
    return sections


def _level_band_hits(haystack: str, bans: list[str], allows: list[str]) -> list[str]:
    """Return ban substrings found in haystack, skipping those covered by ALLOW."""
    hits = []
    for ban in bans:
        if ban not in haystack:
            continue
        # ALLOW wins when it appears in the haystack and itself contains the ban
        # (ようがない covers ようが; 言うまでもなく covers までもなく).
        if any(allow in haystack and ban in allow for allow in allows):
            continue
        hits.append(ban)
    return hits


def check_level_band_grammar(gt: str, keys: dict[int, int],
                             opts: dict[int, list[str]], origin: str):
    """Generated 問題7–9 keys must stay inside the N2 band.

    String-decidable half of exam-qa-review §2.5. Imported papers are skipped
    (they reproduce an outside source). Tests 2–4 shipped N1 keys
    (にあって / をもって / ともなると / までもなく) through a green gate.
    """
    if origin != "generated":
        return skip("問題7–9 keys stay inside N2 level band", "imported test")
    band = load_level_band()
    if not band["TOO_HARD"] and not band["TOO_EASY"]:
        return skip("問題7–9 keys stay inside N2 level band",
                    f"missing {LEVEL_BAND_PATH.relative_to(ROOT)}")

    # 文法 answer rows: | 問 | 答 | 解説 |
    gloss: dict[int, str] = {}
    m = re.search(r"^##\s*文法\s*$(.*?)(?=^##\s|\Z)", gt, re.M | re.S)
    if m:
        for q, expl in re.findall(
            r"\|\s*(\d+)\s*\|\s*[1-4]\s*\|\s*([^|]+)\|", m.group(1)
        ):
            gloss[int(q)] = expl.strip()

    hard, easy = [], []
    for q in range(31, 52):
        ans = keys.get(q)
        if ans is None:
            continue
        keyed = (opts.get(q) or [""] * 4)
        keyed_s = keyed[ans - 1] if 1 <= ans <= len(keyed) else ""
        # Prefer the leading 「〜…」 gloss; fall back to full 解説 + keyed text.
        gtext = gloss.get(q, "")
        gm = re.search(r"「([^」]+)」", gtext)
        haystack = f"{keyed_s} {gm.group(1) if gm else gtext}"
        for ban in _level_band_hits(haystack, band["TOO_HARD"], band["ALLOW"]):
            hard.append(f"{q}:{keyed_s or gm and gm.group(1) or '?'}({ban})")
        for ban in _level_band_hits(haystack, band["TOO_EASY"], band["ALLOW"]):
            easy.append(f"{q}:{keyed_s or gm and gm.group(1) or '?'}({ban})")

    check("問題7–9 keys are not N1-hard (level band)", not hard,
          "; ".join(hard) + " — see exam-qa-review/references/level_band_grammar.txt")
    check("問題7–9 keys are not N3–N5-easy (level band)", not easy,
          "; ".join(easy) + " — see exam-qa-review/references/level_band_grammar.txt")


def check_scramble_stars(gt: str, keys: dict[int, int], opts: dict[int, list[str]]):
    """問題8: the key must name the option that lands on ★ (the 3rd blank).

    Both facts are checkable from the Markdown alone: the stem must offer four
    blanks with ★ on the third, and the 解説 cell must spell the word order out
    as `語(n)→語(n)→語(n)→語(n)`, whose 3rd entry is the answer. Test 2 shipped
    with three of five keys naming a different blank, and one 解説 citing option
    numbers that did not exist in the stem.
    """
    stems = {int(n): s for n, s in
             re.findall(r"^\*\*(4[3-7])\*\*\s*(.+)$", gt, re.M)}
    bad_stem = []
    for q in range(43, 48):
        run = BLANK_RUN.search(stems.get(q, ""))
        slots = run.group().split() if run else []
        if len(slots) != 4 or [i for i, s in enumerate(slots) if "★" in s] != [2]:
            bad_stem.append(f"{q}({len(slots)} blanks, ★ at "
                            f"{[i + 1 for i, s in enumerate(slots) if '★' in s]})")
    check("問題8 stems offer 4 blanks with ★ third", not bad_stem, ", ".join(bad_stem))

    mismatch, unparsed = [], []
    for hit in re.finditer(r"^\|\s*(4[3-7])\s*\|\s*([1-4])\s*\|(.*)\|", gt, re.M):
        q, ans, expl = int(hit.group(1)), int(hit.group(2)), hit.group(3)
        seq = [int(d) for d in re.findall(r"[（(]([1-4])[）)]", expl)]
        if sorted(seq) != [1, 2, 3, 4]:
            unparsed.append(f"{q}(order={seq or 'none'})")
        elif seq[2] != ans:
            mismatch.append(f"{q}: key={ans} but ★(3rd) is option {seq[2]}")
    check("問題8 解説 spells the word order as a 1-4 permutation", not unparsed,
          f"{', '.join(unparsed)} — write `語(1)→語(4)→語(2)→語(3)`")
    check("問題8 keys name the option on ★", not mismatch, "; ".join(mismatch))

    # The option strips ARE the missing span, so the stem must not already
    # contain them. Test 3 shipped all five items with the whole sentence
    # written out in the stem AND chopped into the options, so every permutation
    # read `…本番でパニックになってパニックになってうろたえる…`. The star and
    # permutation checks above pass happily on that — neither reads the stem's
    # own words. Two signals, both chosen to leave honest repetition alone
    # (test 2's 46 legitimately says 新しい町 in the stem and 新しい in an option):
    # an option butting straight up against the blanks, and a long option
    # already spelled out somewhere in the stem.
    echoes = []
    for q in range(43, 48):
        run = BLANK_RUN.search(stems.get(q, ""))
        if not run:
            continue
        head, tail = stems[q][: run.start()].strip(), stems[q][run.end():].strip()
        for opt in opts.get(q, []):
            if not opt:
                continue
            if head.endswith(opt):
                echoes.append(f"{q}: stem already ends with 「{opt}」 before the blanks")
            elif tail.startswith(opt):
                echoes.append(f"{q}: stem resumes with 「{opt}」 after the blanks")
            elif len(opt) >= 4 and (opt in head or opt in tail):
                echoes.append(f"{q}: 「{opt}」 is already written in the stem")
    check("問題8 options do not repeat text already in the stem", not echoes,
          "; ".join(echoes))


# Latin script is a drafting artefact, never exam content: a passage that still
# says 「単なる無音の contrast ではない」 (test 3, 問題9) got half-written in
# English and never finished. Loan words belong in katakana. The allowlist is
# the handful of initialisms official papers really do print.
LATIN_OK = {"SNS", "AI", "IT", "CO", "PC", "DVD", "CD", "BOX", "QR", "URL",
            "FAX", "TV", "WEB", "ATM", "IC", "LED", "USB", "AM", "PM",
            "TTS", "MP"}          # the last two name the pipeline, not content
LATIN_RUN = re.compile(r"[A-Za-z]{2,}")
RUBY_MARKUP = re.compile(r"<[^>]+>")


def check_no_latin_prose(name: str, text: str):
    bad = sorted({w for w in LATIN_RUN.findall(RUBY_MARKUP.sub(" ", text))
                  if w.upper() not in LATIN_OK})
    check(f"{name}: no un-transliterated Latin words", not bad,
          f"{bad} — write it in katakana or Japanese")


def check_dokkai_numbered_markers(name: str, gt_prose: str):
    blocks = re.split(r"(?:^##\s*問題(?:9|10|11|12|13|14)\b|^###\s*\(\d+\))", gt_prose, flags=re.M)
    mismatches = []
    for idx, block in enumerate(blocks[1:], 1):
        if not re.search(r"\*\*\d+\*\*", block):
            continue
        parts = re.split(r"\n(?=\*\*\d+\*\*)", block, maxsplit=1)
        passage = parts[0]
        questions = parts[1] if len(parts) > 1 else ""
        p_markers = set(re.findall(r"([①②③④⑤])\*\*", passage))
        q_markers = set(re.findall(r"([①②③④⑤])\*\*", questions))
        if p_markers != q_markers:
            mismatches.append(f"section {idx}: passage has {sorted(p_markers)} vs questions have {sorted(q_markers)}")
    check(f"{name}: passage numbered markers match questions 1-to-1", not mismatches,
          "; ".join(mismatches) + " — every passage marker ①/② must be referenced by a question stem")


# 解説 cells decide items, so a quote inside one is load-bearing. When it is
# invented, the item it justifies is usually broken too and nothing shows:
# test 2's 聴解 key quoted four lines of dialogue that were not in the script;
# test 4's 問題2-6番 key quoted a 「3日前」 rule the script gives as 1週間前, and
# named two speakers (アンさん・キムさん) the script never introduces.
QUOTE = re.compile(r"「([^」]{14,})」")
QUOTE_ELLIPSIS = re.compile(r"[…‥]+")


def _flat(s: str) -> str:
    """Strip what varies between a quote and its source but carries no meaning:
    whitespace, table/emphasis markup, and the quote marks themselves (a nested
    quote is 『』 inside 「」 but 「」 in the passage)."""
    return re.sub(r"[\s「」『』]|\*\*|<[^>]+>", "", s)


def check_explanation_quotes(name: str, key_section: str, source: str):
    """A long 「…」 span in a key table should occur in the passage or script.

    Reported, not enforced: a 解説 may legitimately put its own wording in 「」,
    so this cannot be decided by matching alone. What it catches is the class
    of bug where it is NOT the explanation that is wrong — test 2's 聴解 key
    quoted four lines of dialogue that were nowhere in the script, and test 4's
    問題4-10番 key quoted an option 「本当ですか！ぜひお願いしたいです」 that the
    script never speaks. A quote nobody can find usually means the item was
    keyed against a draft that no longer exists.
    """
    src = _flat(source)
    missing = []
    for q in QUOTE.findall(key_section):
        parts = [_flat(p) for p in QUOTE_ELLIPSIS.split(q)]
        if any(len(p) >= 14 and p not in src for p in parts):
            missing.append(q[:38] + ("…" if len(q) > 38 else ""))
    warn(f"{name}: 解説 quotes trace to the passage/script", not missing,
         f"not found in the source: {missing} — quote by copy-paste; if the "
         f"line really is not there, the ITEM is wrong, not the explanation")


def check_spec_blend(spec: dict):
    """The blend contract the authoring step reads off logs/test_spec.json.

    Two invariants no other gate can see, both violated by test 4's spec:
    every surface needs a DISTINCT topic (a duplicate silently starves one
    問題, which then gets authored off-contract), and the pool side keeps >=40%
    of every blended surface (AGENTS.md §5). merge_seeds.py compounds both when
    it is re-run over its own output.
    """
    for field, key in (("reading_topics", "topic"),
                       ("listening_scenarios", "scenario")):
        recs = spec.get("items", {}).get(field, [])
        names = [r.get(key) if isinstance(r, dict) else r for r in recs]
        dups = sorted({n for n in names if names.count(n) > 1})
        check(f"test_spec {field}: one distinct topic per surface", not dups,
              f"repeated: {dups} — re-run merge_seeds.py (it restores the "
              f"pool draw first); do not author from a spec that repeats itself")
        web = sum(1 for r in recs if isinstance(r, dict) and r.get("origin") == "web")
        over = recs and web > int(len(recs) * 0.60)
        check(f"test_spec {field}: pool keeps >=40% ({web}/{len(recs)} web)",
              not over,
              f"web share {web}/{len(recs)} exceeds the MAX_WEB ceiling — "
              f"merge_seeds was re-run over an already-blended spec")


def check_pool_infrastructure():
    print("\npool expansion / adjunct staging")
    oj = AGENTS / "item-pool-sampling" / "references" / "openjlpt"
    for name in ("vocab-n2.json", "kanji-n2.json", "NOTICE.md"):
        check(f"openjlpt/{name} exists", (oj / name).is_file())
    staging = ROOT / "logs" / "adjunct_staging.json"
    check("logs/adjunct_staging.json exists", staging.is_file())
    if staging.is_file():
        data = json.loads(staging.read_text(encoding="utf-8"))
        check("adjunct_staging.json version == 1", data.get("version") == 1,
              f"got {data.get('version')!r}")
        bad = []
        for e in data.get("entries", []):
            if not e.get("item") or not e.get("category"):
                bad.append("missing item/category")
            elif e.get("level") != "N2":
                bad.append(f"{e.get('item')}: level {e.get('level')!r}")
        check("adjunct staging rows are N2 with item+category", not bad,
              "; ".join(bad[:5]))


ADJUNCT_CAP = 0.20


def check_spec_adjunct(spec: dict):
    """Adjunct draws from logs/adjunct_staging.json must carry provenance."""
    for cat, items in spec.get("items", {}).items():
        adjunct = [x for x in items if isinstance(x, dict) and x.get("origin") == "adjunct"]
        if not adjunct:
            continue
        cap = int(len(items) * ADJUNCT_CAP)
        check(f"test_spec {cat}: adjunct within {ADJUNCT_CAP:.0%} cap "
              f"({len(adjunct)}/{len(items)})",
              len(adjunct) <= cap if cap >= 1 else len(adjunct) == 0,
              f"cap allows {cap}, got {len(adjunct)} — sample_items ADJUNCT_CAP")
        for a in adjunct:
            label = a.get("item", "?")
            check(f"test_spec adjunct {cat}/{label}: has item+level N2+evidence",
                  bool(a.get("item")) and a.get("level") == "N2"
                  and isinstance(a.get("evidence"), list),
                  str(a)[:80])


def check_rotation_inputs():
    """The two knobs that decide whether a new test is actually new.

    Pool items rotate because the ledger excludes what previous tests drew.
    Web topics have no such memory: `merge_seeds.py` seeds its RNG from the
    spec's own seed, so the SAME `--seed` plus an unchanged `logs/seeds.json`
    reproduces the previous test's blend slot for slot. Test 3 was generated
    with test 2's seed (20260804) against test 2's untouched harvest and came
    out a re-skin of it — same デジタルデトックス, same クラフトツーリズム,
    same ハイブリッドワーク down to the 「約7割」 figure, and the same web
    scenario in the same 聴解 slot. Every other gate passed.
    """
    led = ROOT / "logs" / "ledger.json"
    if led.is_file():
        hist = json.loads(led.read_text(encoding="utf-8")).get("history", [])
        by_seed: dict[int, list[dict]] = {}
        for h in hist:
            if h.get("seed") is not None:
                by_seed.setdefault(h["seed"], []).append(h)
        # Sharing a seed is only safe when the harvest differs: the blend is a
        # pure function of (seed, seeds.json). merge_seeds stamps harvest_sha,
        # so two entries that agree on the seed must disagree on the harvest.
        clash = []
        for s, entries in by_seed.items():
            if len(entries) < 2:
                continue
            shas = [e.get("harvest_sha") for e in entries]
            if len(set(shas)) < len(shas):
                ids = [str(e.get("test_id")) for e in entries]
                clash.append(f"seed {s} shared by tests {ids} with the same "
                             f"harvest ({shas[0] or 'unrecorded'})")
        check("no two tests share both a --seed and a web harvest", not clash,
              "; ".join(clash) + " — merge_seeds replays the previous blend "
              "slot for slot; re-harvest logs/seeds.json or pick a new seed")

        shas = [h["harvest_sha"] for h in hist if h.get("harvest_sha")]
        dup = sorted({x for x in shas if shas.count(x) > 1})
        check(f"each test blended its own web harvest ({len(shas)} recorded)",
              not dup, f"harvest_sha reused: {dup} — step 3.5 was skipped")

    spec_path, seeds_path = ROOT / "logs" / "test_spec.json", ROOT / "logs" / "seeds.json"
    if not (spec_path.is_file() and seeds_path.is_file()):
        return skip("every web entry in test_spec traces to logs/seeds.json",
                    "no test_spec.json or seeds.json")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    check_spec_blend(spec)
    check_spec_adjunct(spec)
    harvest = {s["seed"] for s in json.loads(seeds_path.read_text(encoding="utf-8"))}

    blended: list[tuple[str, str]] = []
    for key, field in (("topic", "reading_topics"), ("scenario", "listening_scenarios")):
        for e in spec.get("items", {}).get(field, []):
            if isinstance(e, dict) and e.get("origin") == "web":
                blended.append((field, e.get(key, "")))
    for field in ("info_retrieval_texture", "cloze_topic"):
        e = spec.get(field)
        if isinstance(e, dict) and e.get("origin") == "web":
            blended.append((field, e.get("detail") or e.get("topic", "")))

    orphans = [f"{f}:「{t}」" for f, t in blended if t not in harvest]
    check(f"every web entry in test_spec traces to logs/seeds.json "
          f"({len(blended)} blended)", not orphans,
          "; ".join(orphans) + " — the spec was blended from a harvest that has "
          "since been replaced; re-run merge_seeds")


def check_answer_positions(d, keys: dict[int, int], ck: dict[str, int], g):
    """Keys must sit where sample_items.py put them (the balance contract).

    logs/test_spec.json prescribes the answer position of every item so no
    number is over-used; authoring is supposed to place the correct choice
    there. Only the test that spec belongs to can be checked.
    """
    spec_path = ROOT / "logs" / "test_spec.json"
    if not spec_path.is_file():
        return skip("keys match logs/test_spec.json answer_positions", "no test_spec.json")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if str(spec.get("test_id")) != d.name:
        return skip(f"keys match logs/test_spec.json answer_positions",
                    f"spec is for test {spec.get('test_id')}, not {d.name}")
    pos = spec.get("answer_positions") or {}

    want: dict[str, int] = {}
    for tag, meta in g.GENGO_QUESTION_TAXONOMY.items():
        lo, hi = meta["range"]
        n = tag[1:]
        row = pos.get(f"問題{n}_語彙") or pos.get(f"問題{n}") or []
        for q, a in zip(range(lo, hi + 1), row):
            want[str(q)] = a
    choukai_ids = {1: [f"問1-{i}" for i in range(1, 6)],
                   2: [f"問2-{i}" for i in range(1, 7)],
                   3: [f"問3-{i}" for i in range(1, 6)],
                   4: [f"問4-{i}" for i in range(1, 12)],
                   5: ["問5-1", "問5-2-1", "問5-2-2"]}
    for n, ids in choukai_ids.items():
        for qid, a in zip(ids, pos.get(f"聴解_問題{n}") or []):
            want[qid] = a

    have = {str(q): a for q, a in keys.items()} | dict(ck)
    off = {q: (a, have.get(q)) for q, a in want.items() if have.get(q) != a}
    check(f"keys match logs/test_spec.json answer_positions ({len(want)} prescribed)",
          not off, f"prescribed vs actual: {off}")


def check_script_shape(script_text: str, ct: str, m):
    """聴解 script ↔ booklet: same instructions, options spoken only where the
    booklet prints none (jlpt-exam-structure's 'Printed in booklet' column)."""
    drift = [ln for ln in re.findall(r"^問題[1-5]では、.*$", ct, re.M)
             if ln.strip() not in script_text]
    check("問題N instructions are identical in booklet and script", not drift,
          f"booklet wording absent from the script: {[d[:34] + '…' for d in drift]}")

    secs = re.split(r"^問題([1-5])。$", script_text, flags=re.M)
    spoken = {int(secs[i]): len(re.findall(r"^[1-4]、", secs[i + 1], re.M))
              for i in range(1, len(secs), 2)}
    # 問題1/2 print their options; 問題3 speaks 4 per item, 問題4 speaks 3;
    # 問題5 speaks 4 for 1番 only — 2番's are printed.
    ei = m.EXPECTED_ITEMS
    want = {1: 0, 2: 0, 3: 4 * ei["問題3"], 4: 3 * ei["問題4"], 5: 4}
    check("options are spoken exactly where the booklet prints none",
          spoken == want, f"spoken option lines {spoken}, expected {want}")

    if (tail := re.split(r"^2番。まず話を聞いてください。", script_text, flags=re.M)):
        if len(tail) > 1 and re.search(r"^[1-4]、", tail[1], re.M):
            check("問題5 2番 does not speak its printed options", False,
                  "options for the two-question item are printed in the booklet only")
        else:
            check("問題5 2番 does not speak its printed options", True)

    ascii_punct = re.findall(r"(?<!\d)[,.](?!\d)", script_text)
    check("no ASCII , or . in the script (TTS mis-times them)", not ascii_punct,
          f"{len(ascii_punct)} found — use 、 and 。")


EXAMPLE_PREMARK = re.compile(r"\*\*[（(]([1-4])[)）]\*\*")


def check_example_premarks(ct: str, st: str, bi):
    """The 例 the marksheet pre-marks must be the answer the announcer declares.

    問題1-4 each open with a practice 例 whose answer the script announces
    (「最もよいものは◯番です…答えはこのように書きます」) while the booklet's
    answer grid shows that same number pre-marked — one demonstration, seen and
    heard together. Tests 2 (問題3) and 4 (問題4) shipped grids pre-marking a
    different number than the announcement; nothing caught it because 例 rows
    are not among the 30 scored keys.
    """
    cut = bi.KEY_HEADING.search(ct)
    lines = ct[cut.start():].splitlines() if cut else []
    marks: list[int] = []
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells or cells[0] != "例":
            continue
        m = EXAMPLE_PREMARK.search(line)
        if not m:
            # horizontal grid (tests 1-3): 例 is a column header; its bubbles
            # sit in the first cell of the next data row.
            for nxt in lines[i + 1:]:
                ncells = [c.strip() for c in nxt.split("|")[1:-1]]
                if not ncells or set(nxt.strip()) <= set("|-: "):
                    continue
                m = EXAMPLE_PREMARK.search(ncells[0])
                break
        if m:
            marks.append(int(m.group(1)))

    announced: list[int] = []
    secs = re.split(r"^問題([1-5])。$", st, flags=re.M)
    for i in range(1, len(secs), 2):
        if secs[i] != "5":       # 問題5 has no 例 (この問題には練習はありません)
            hit = re.search(r"最もよいものは([1-4])番です", secs[i + 1])
            if hit:
                announced.append(int(hit.group(1)))

    check(f"例 pre-marks match the script's announcements ({marks} vs {announced})",
          len(marks) == 4 and marks == announced,
          "the grid demonstrates a different answer than the announcer declares "
          "— fix the marksheet 例 row (or the 例 itself), not just one of them")


# --------------------------------------------------------------- per-test checks
def check_tests():
    g = load(".agents/exam-answer-grading/scripts/grade_answers.py")
    m = load(".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py")
    bi = load(".agents/interactive-answer-sheet/scripts/build_interactive.py")
    key_heading = re.compile(r"^#+\s*(解答|【?正解)", re.M)
    expected_choukai = ([f"問{s}-{i}" for s, n in ((1, 5), (2, 6), (3, 5), (4, 11))
                         for i in range(1, n + 1)]
                        + ["問5-1", "問5-2-1", "問5-2-2"])

    dirs = sorted(p for p in (ROOT / "tests").glob("*") if p.is_dir()) if (ROOT / "tests").is_dir() else []
    if not dirs:
        print("\nper-test contracts")
        skip("tests/", "no test directories on disk")
        return

    for d in dirs:
        print(f"\nper-test contracts: {d.relative_to(ROOT)}")
        origin = "imported" if d.name.startswith("imported-") else "generated"
        if origin == "imported":
            slug = d.name[len("imported-"):]
            check("imported- slug is non-empty kebab-case",
                  bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)),
                  f"got {d.name!r}")
        meta = d / "import_meta.json"
        if origin == "imported":
            if not meta.is_file():
                check("imported test has import_meta.json", False,
                      "run init_imported_test.py")
            else:
                try:
                    mdata = json.loads(meta.read_text(encoding="utf-8"))
                except json.JSONDecodeError as e:
                    check("import_meta.json parses", False, str(e))
                    mdata = {}
                check("import_meta.json origin is imported",
                      mdata.get("origin") == "imported",
                      f"got {mdata.get('origin')!r}")
                check("import_meta.json test_id matches folder",
                      mdata.get("test_id") == d.name,
                      f"meta={mdata.get('test_id')!r} folder={d.name!r}")
        elif meta.is_file():
            check("generated test has no import_meta.json", False,
                  "import_meta.json is only for imported-* folders — "
                  "rename to imported-<slug> or remove the meta file")

        gengo, choukai = d / "言語知識・読解.md", d / "聴解.md"
        if not (gengo.is_file() and choukai.is_file()):
            check("both Markdown sources present", False,
                  f"missing {[f.name for f in (gengo, choukai) if not f.is_file()]}")
            continue

        gt, ct = gengo.read_text(encoding="utf-8"), choukai.read_text(encoding="utf-8")
        for f, text in ((gengo, gt), (choukai, ct)):
            check(f"{f.name}: answer-key heading present (build_interactive aborts without it)",
                  key_heading.search(text) is not None)
            check(f"{f.name}: no `# 問題N` h1 section header",
                  not re.search(r"^# 問題[1-5]\b", text, re.M),
                  "use `# 【問題】` + `## 問題N` (jlpt-exam-structure)")

        keys = g.parse_gengo_keys(gengo)
        check("71 gengo answer keys parse", len(keys) == 71,
              f"got {len(keys)}, missing {[q for q in range(1, 72) if q not in keys]}")
        ck = g.parse_choukai_keys(choukai)
        check("30 choukai answer keys parse with the expected labels",
              sorted(ck) == sorted(expected_choukai),
              f"missing {[k for k in expected_choukai if k not in ck]}, "
              f"unexpected {[k for k in ck if k not in expected_choukai]}")

        # No question may offer the same option twice — a silent second correct
        # answer, and the radio-count checks below cannot see it.
        opts = gengo_option_sets(gt, bi)
        dupes = {q: [o for o in set(v) if v.count(o) > 1] for q, v in opts.items()}
        dupes = {q: v for q, v in dupes.items() if v}
        check("no gengo question repeats an option", not dupes,
              "; ".join(f"{q}: {v}" for q, v in sorted(dupes.items())))
        wrong_n = {q: len(v) for q, v in opts.items() if len(v) != 4}
        check("every gengo question parses to exactly 4 options", not wrong_n, f"{wrong_n}")
        check_scramble_stars(gt, keys, opts)
        check_grammar_stem_lengths(gt, bi)
        # Official papers include short particle strips; the drill-length defect
        # is a generation failure mode — do not fail imported transcriptions.
        if origin == "generated":
            check_mondai8_chunk_lengths(gt, opts, bi)
        check_level_band_grammar(gt, keys, opts, origin)
        check_answer_positions(d, keys, ck, g)
        for f in (gengo, choukai):
            body = f.read_text(encoding="utf-8")
            cut = bi.KEY_HEADING.search(body)
            check_no_latin_prose(f.name, body[: cut.start()] if cut else body)

        gcut = bi.KEY_HEADING.search(gt)
        gengo_prose = gt[: gcut.start()] if gcut else gt
        gengo_rubies = re.findall(r"<ruby>.*?</ruby>", gengo_prose, re.S)
        check(f"{gengo.name}: no furigana (<ruby>) in 言語知識・読解", not gengo_rubies,
              f"found {len(gengo_rubies)} <ruby> tags in prose — Dokkai uses only （注N） notes for over-the-level words")
        check_dokkai_numbered_markers(gengo.name, gengo_prose)

        # Only the 読解 key table quotes running text; the 文字・語彙 and 文法
        # tables put grammar glosses in 「」 by design, which is not a quote.
        gcut = bi.KEY_HEADING.search(gt)
        dokkai = re.search(r"^##\s*読解\s*$(.*)", gt[gcut.start():] if gcut else "",
                           re.M | re.S)
        if gcut and dokkai:
            check_explanation_quotes(gengo.name, dokkai.group(1), gt[: gcut.start()])

        # Official July 2025 (~50+ 注, 中略 in 中文, 長文 ~1000) is the bar.
        # Generated tests 1–4 under-annotated; warn so authoring cannot ignore it.
        if origin == "generated":
            notes = len(re.findall(r"（注\d+）|\(注\d+\)", gt))
            warn(f"{d.name}: 読解 has substantial （注N） glosses "
                 f"(official July 2025 ≈50+; got {notes})",
                 notes >= 15,
                 "add glosses on N1/rare terms in 問題10–13 — see question-authoring")
            easy_note_match = re.findall(
                r"（注\d+）\s*(選択|信号|技術|文化|質|準備|手順|設計|現象|経由|偏り|維持|継続|前提|細部|バランス|指示|対応|理由|関係|方法)(?::|：)",
                gt
            )
            warn(f"{d.name}: 読解 （注N） notes do not target easy/basic N3–N5 words",
                 not easy_note_match,
                 f"found glosses on easy/standard words: {set(easy_note_match)} — notes must target N1+/rare/specialized terms")
            warn(f"{d.name}: 読解 uses （中略） at least once",
                 "中略" in gt,
                 "official 中文/長文 cut with （中略）; generated tests shipped none")
            m13 = re.search(r"^##\s*問題13\b.*?(?=^##\s*問題14\b)", gt, re.M | re.S)
            if m13:
                body13 = re.split(r"\*\*67\*\*", m13.group(0), maxsplit=1)[0]
                n13 = jp_char_count(body13)
                warn(f"{d.name}: 問題13 長文 ≥850 JP chars "
                     f"(official ~900–1100; got {n13})",
                     n13 >= 850,
                     "主張理解 is under-length vs refs/JLPT")
            m7 = re.search(r"^##\s*問題7\b.*?(?=^##\s*問題8\b)", gt, re.M | re.S)
            if m7:
                dialogueish = (
                    len(re.findall(r"[「『]", m7.group(0))) >= 2
                    or bool(re.search(r"（[^）]{2,12}）", m7.group(0)))
                )
                warn(f"{d.name}: 問題7 includes dialogue or setting-label stems",
                     dialogueish,
                     "official papers mix （会社で）/インタビュー/dialogue turns")

        script = d / "聴解スクリプト.txt"
        if script.is_file():
            st = script.read_text(encoding="utf-8")
            ccut = bi.KEY_HEADING.search(ct)
            if ccut:
                check_explanation_quotes(choukai.name, ct[ccut.start():],
                                         st + ct[: ccut.start()])
            blocks = [b.strip() for b in re.split(r"\n\s*\n", st) if b.strip()]
            try:
                m.validate_script(blocks)
                check(f"聴解スクリプト.txt passes validate_script ({len(blocks)} blocks)", True)
            except SystemExit as e:
                check("聴解スクリプト.txt passes validate_script", False, str(e).replace("\n", " ")[:300])
            check_script_shape(st, ct, m)
            check_example_premarks(ct, st, bi)
        else:
            check("聴解スクリプト.txt present", False, "canonical name required")

        if (d / "聴解.mp3").is_file():
            check("聴解_チャプター.json accompanies the MP3", (d / "聴解_チャプター.json").is_file(),
                  "re-run make mp3 to regenerate chapter marks")

        sheet = d / "解答.html"
        if not sheet.is_file():
            check("解答.html present", False, "run make sheet")
            continue

        html = sheet.read_text(encoding="utf-8")
        check("解答.html has no emoji in the report labels",
              not re.search("[🟢🟡🔴]", html), "4cad944 removed them; rebuild the sheet")

        # Radio-group shape. Every one of these caught a real bug: a single
        # bubble per horizontally-laid-out question (unanswerable beyond
        # option 1), and 質問1/質問2 colliding with 1番/2番 in 問題5.
        groups: dict[str, int] = {}
        for hit in re.finditer(r'<input[^>]*type="radio"[^>]*name="q_([^"]+)"', html):
            groups[hit.group(1)] = groups.get(hit.group(1), 0) + 1

        check(f"one radio group per question ({len(groups)} groups)", len(groups) == 101,
              f"expected 101, got {len(groups)}")
        missing = [k for k in list(map(str, range(1, 72))) + expected_choukai if k not in groups]
        check("every scored question has a radio group", not missing, f"missing {missing}")
        oversized = {k: n for k, n in groups.items() if n > 4}
        check("no question shares a group name with another",
              not oversized, f"over-filled groups: {oversized}")
        thin = {k: n for k, n in groups.items() if n < 3}
        check("no question offers fewer than 3 options", not thin,
              f"under-filled groups: {thin} (horizontal option rows must yield 4 bubbles)")
        gengo_bad = {k: n for k, n in groups.items() if k.isdigit() and n != 4}
        check("all 71 gengo questions offer exactly 4 options", not gengo_bad, f"{gengo_bad}")
        q4 = {k: n for k, n in groups.items() if k.startswith("問4-") and n != 3}
        check("問題4 (即時応答) offers exactly 3 options", not q4, f"{q4}")


# ------------------------------------------------- the two graders must agree
JS_HARNESS = r"""
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const blocks = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const js = blocks[blocks.length - 1];

// The sheet's script is DOM-bound at load; stub just enough to evaluate it.
const noop = () => {};
const el = new Proxy({}, {get: (t, k) => (k === 'style' || k === 'dataset' ? {} :
  k === 'value' || k === 'textContent' || k === 'innerHTML' ? '' :
  k === 'children' || k === 'querySelectorAll' ? [] : typeof k === 'string' ? noop : undefined),
  set: () => true});
global.document = {getElementById: () => el, querySelector: () => el,
  querySelectorAll: () => [], addEventListener: noop, createElement: () => el,
  body: el, documentElement: el};
global.window = {addEventListener: noop};
global.localStorage = {getItem: () => null, setItem: noop, removeItem: noop};
global.alert = noop; global.confirm = () => true; global.fetch = () => Promise.reject();
global.Blob = function(){}; global.URL = {createObjectURL: () => '', revokeObjectURL: noop};

const sandbox = {};
new Function('ctx', js + '\nctx.computeResult = computeResult; ctx.ANSWER_KEY = ANSWER_KEY;')(sandbox);

// Deterministic simulated answers: correct unless the index is divisible by 3.
const ans = {};
Object.keys(sandbox.ANSWER_KEY).sort().forEach((k, i) => {
  const correct = sandbox.ANSWER_KEY[k];
  ans[k] = (i % 3 === 0) ? (correct % 4) + 1 : correct;
});
fs.writeFileSync(process.argv[3], JSON.stringify(ans));
process.stdout.write(JSON.stringify(sandbox.computeResult(ans)));
"""


def first_diff(a, b, path: str = "") -> str:
    """Where two 採点結果.json documents stop agreeing — one readable location."""
    if isinstance(a, dict) and isinstance(b, dict):
        only_a, only_b = set(a) - set(b), set(b) - set(a)
        if only_a or only_b:
            return f"{path or '/'}: JS-only {sorted(only_b)}, Python-only {sorted(only_a)}"
        for k in a:
            if a[k] != b[k]:
                return first_diff(a[k], b[k], f"{path}.{k}")
        return ""
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return first_diff(x, y, f"{path}[{i}]")
        return ""
    return f"{path}: Python {a!r} vs JS {b!r}"


def check_grader_parity():
    print("\nin-page grader ↔ grade_answers.py (same answers, same 採点結果.json)")
    if not (ROOT / "tests").is_dir():
        return skip("grader parity", "no tests/ on disk")
    sheets = sorted((ROOT / "tests").glob("*/解答.html"))
    if not sheets:
        return skip("grader parity", "no 解答.html built")
    if subprocess.run(["which", "node"], capture_output=True).returncode != 0:
        return skip("grader parity", "node not installed")

    g = load(".agents/exam-answer-grading/scripts/grade_answers.py")
    for sheet in sheets:
        d = sheet.parent
        with tempfile.TemporaryDirectory() as tmp:
            harness = Path(tmp) / "h.js"
            harness.write_text(JS_HARNESS, encoding="utf-8")
            answers = Path(tmp) / "a.json"
            r = subprocess.run(["node", str(harness), str(sheet), str(answers)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                check(f"{d.name}: JS grader runs under node", False,
                      r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "no stderr")
                continue

            js_doc = json.loads(r.stdout)
            flat = json.loads(answers.read_text(encoding="utf-8"))
            ua = {"言語知識_読解": {k: v for k, v in flat.items() if not k.startswith("問")},
                  "聴解": {k: v for k, v in flat.items() if k.startswith("問")}}
            res = g.grade(g.parse_gengo_keys(d / "言語知識・読解.md"),
                          g.parse_choukai_keys(d / "聴解.md"), ua)
            py_doc = g.result_payload(res, d.name)

            # Only the timestamp may differ: 採点結果.json must be byte-comparable
            # whichever grader wrote it, since screen 1 and screen 3 both read it.
            py_doc.pop("graded_at", None)
            js_doc.pop("graded_at", None)
            sec = py_doc["summary"]["sections"]
            raw = " + ".join(f"{s['raw_correct']}/{s['raw_total']}" for s in sec.values())
            check(f"{d.name}: 採点結果.json agrees field for field ({raw})",
                  py_doc == js_doc, first_diff(py_doc, js_doc))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", action="store_true", help="only the per-test contracts")
    args = ap.parse_args()

    print("JLPT pipeline consistency check")
    if not args.tests:
        check_refs()
        check_skills()
        check_filename_contracts()
        check_pacing()
        check_item_counts()
        check_taxonomy()
        check_pool_infrastructure()
        print("\nrotation inputs (why a new test is actually new)")
        check_rotation_inputs()
    check_tests()
    check_grader_parity()

    print()
    if _warn:
        print(f"{len(_warn)} warning(s) — resolve each or say why it is a false "
              f"positive in your final report:")
        for w in _warn:
            print(f"  - {w}")
        print()
    if _fail:
        print(f"FAILED — {len(_fail)} problem(s):")
        for f in _fail:
            print(f"  - {f}")
        return 1
    print(f"All checks passed{f' ({len(_skip)} skipped)' if _skip else ''}"
          f"{f', {len(_warn)} warning(s)' if _warn else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
