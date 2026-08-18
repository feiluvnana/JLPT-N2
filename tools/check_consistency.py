#!/usr/bin/env python3
"""
Consistency checker for the JLPT pipeline — run with `make check`.

Every failure this catches is a real bug that shipped at least once: a doc naming
a file no script writes, a pacing constant that stopped matching its table, an
answer-key heading the sheet builder needs but no doc mentioned, two graders
drifting apart. The docs are prose and cannot be executed, so this asserts the
handful of facts they duplicate from the code.

Hardening round 1 added the check classes that round-1 QA on generated papers
found the gate blind to, every threshold measured on the July 2025 official paper (a
check a real paper fails is a wrong check, not a finding). It was measured from
an in-tree import that has since been deleted; the live copy is the archive
extract `refs/JLPT_N2_NEW/16. N2 7-2025/booklet.md`:
問題11 stem shape, （注N） band/pairing, the 問題5 2番 lead-in, artifact staleness
stamps, 問題14 解説 grounding, 読解 passage length floors, ledger draw counts,
harvest hygiene, 問題9 category tags, 聴解 voice casting, cross-test verbatim
reuse, verbatim-lift keys, pool level-band drift, （中略） placement, and spec
target-item substitution.

Round 2 added: 問題1 spec↔pool↔paper, pools.json `kanji_reading` entry shape,
問題8 bare adverbs (WARN), self-declared fabricated distractors, ledger↔spec
draw equality, harvest_sha provenance, the sampler's `rotation` block, 問題11
opinion-stem coverage, 問題13's closing stem, and 問題7 解説 option numbering.

Round 2 also RE-CALIBRATED every length/count threshold against the 31-sitting
archive — `.agents/question-authoring/references/official_calibration.md`,
which is now the evidence of record. Read §9 before touching a constant. Eight
of them had been derived from ONE paper (July 2025) and were failing real
official exams: 読解 floors for 問題10/13/14, the 問題10 per-passage floor, the
（注N） gloss floor, `P7_STEM_MIN`, `P8_OPT_SUM_MIN`, `P8_ASSEMBLED_MIN`, plus
`P8_LONG_OPTS_MIN` (retired) — and the 問題11 per-passage pairing rule, which
6 of the 7 current official papers fail. A sample of one cannot tell a rule
from a coincidence; every surviving constant now carries its measured band.

CAVEAT — the in-tree calibration anchor is gone. The `tests/imported-n2-2025-07`
folder every threshold below was measured on was deleted, so the checks that
compared a generated test against it (cross-test verbatim reuse; the
imported-only exemptions) lost their strongest comparison; check_tests now
prints an explicit `skip` for that half instead of letting it pass silently
(the generated↔generated comparison still runs).
The archive extracts replace it as the READING anchor —
`refs/JLPT_N2_NEW/<sitting>/booklet.md` and `key.md` are exact text, and
`script.md`'s fenced [OCR ▼]…[OCR ▲] dialogue is ~98% character-accurate, so it
is evidence for order and shape but never for official wording or a calibration
measurement. Re-anchoring the text-comparison checks needs a pre-extracted
fixture, because this gate must never open a PDF — it stays read-only and
finishes in seconds.

Read-only: it never writes to tests/ or logs/.

    python3 tools/check_consistency.py            # everything
    python3 tools/check_consistency.py --tests    # only the per-test contracts
"""

import argparse
import collections
from difflib import SequenceMatcher
import hashlib
import importlib.util
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import unicodedata
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


# The imported-/generated folder-name flag, owned by external-test-import.
ORIGIN = load(".agents/external-test-import/scripts/origin.py")

# Reuse lint_draft.py's contraction pattern list rather than maintaining a
# second, narrower copy — the two diverged (this file's own set missed とど-,
# ちゃえ, なくちゃ and the trailing-particle context on てる/でる etc.), which
# let a script pass lint_draft's PASS-banded measurement while still WARNing
# here on the same text (20260817_1 QA G9: 34.2/10k via lint_draft vs.
# 18.6/10k via this file, both claiming to measure the same official band).
_LINT_DRAFT = load("tools/lint_draft.py")
CONTRACTION_RE = _LINT_DRAFT.CONTRACTION_RE


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
    # The sign is load-bearing: SPEAKER_MAP rates read "+4%" / "-8%", and
    # dropping the minus collapsed 男1(+4)/男2(-8) — the skill's own sanctioned
    # three-person split, 12 points apart — into a 4-point gap that warned.
    return float(re.search(r"[+-]?[\d.]+", s).group())


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
        ("解答.html", ".agents/exam-app/scripts/build_interactive.py"),
        ("採点結果.json", ".agents/exam-app/scripts/build_interactive.py"),
        ("採点結果.json", ".agents/exam-app/scripts/grade_answers.py"),
        ("ユーザー解答.json", ".agents/exam-app/scripts/build_interactive.py"),
        ("ユーザー解答.json", ".agents/exam-app/scripts/serve_sheet.py"),
        ("聴解.mp3", ".agents/choukai-audio/scripts/make_choukai_mp3.py"),
        ("聴解_チャプター.json", ".agents/choukai-audio/scripts/make_choukai_mp3.py"),
        ("ledger.json", ".agents/exam-blueprint/scripts/sample_items.py"),
        ("test_spec.json", ".agents/exam-blueprint/scripts/sample_items.py"),
        ("import_meta.json", ".agents/external-test-import/scripts/init_imported_test.py"),
        ("模範解答.html", ".agents/exam-model-answer/scripts/build_model_answer.py"),
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


# ---------------------------------------------- the two deployments of one app
def check_deployments():
    """`make serve` and GitHub Pages must stay ONE app with TWO storage backends.

    The static build exists because Pages has no server and no disk. Everything
    that makes the two deployments the same app is a shared module, and the one
    thing that differs — where answers live — is chosen at build time. Both
    halves of that are checkable, and both are exactly the kind of thing that
    drifts silently: a second copy of the list markup nobody updates, or a
    localStorage key the sheet writes and the list reads under another name.
    """
    print("\nserve ↔ GitHub Pages (one app, one storage backend per build)")
    scripts = AGENTS / "exam-app" / "scripts"
    src = {f.name: f.read_text(encoding="utf-8")
           for f in scripts.glob("*.py")}

    for name in ("index_view.py", "local_store.py", "build_pages.py"):
        check(f"{name} present", name in src, "the static build needs it")
    if not {"index_view.py", "local_store.py", "build_pages.py"} <= set(src):
        return

    # Screen 1 is rendered ONCE. serve_sheet.py used to hold its own copy of the
    # cards and CSS; a second copy is how the two lists stop looking alike.
    for name in ("serve_sheet.py", "build_pages.py"):
        check(f"{name} imports the shared test list", "index_view" in src[name],
              "render screen 1 through index_view, never a private copy")
    owners = [n for n, t in src.items() if "INDEX_CSS = " in t]
    check("only index_view.py defines the list stylesheet", owners == ["index_view.py"],
          f"also defined in {[o for o in owners if o != 'index_view.py']}")

    # The sheet writes these keys and the list reads them. One definition, in
    # local_store.py; anything else spelling out the prefix is a second copy.
    ls = load(".agents/exam-app/scripts/local_store.py")
    hardcoded = [n for n, t in src.items()
                 if n != "local_store.py" and ls.STORAGE_PREFIX in t]
    check(f"localStorage keys defined once ({ls.STORAGE_PREFIX}/<id>/<file>)",
          not hardcoded, f"prefix also hard-coded in {hardcoded}")
    check("the store keys ARE the deliverable filenames",
          (ls.ANSWERS_JSON, ls.RESULT_JSON) == ("ユーザー解答.json", "採点結果.json"),
          f"got {ls.ANSWERS_JSON}, {ls.RESULT_JSON}")

    # Exactly one backend may be live in a built sheet: a server build must not
    # even carry the localStorage code, or a future edit could write both.
    bi = load(".agents/exam-app/scripts/build_interactive.py")
    check("build_interactive knows both backends and defaults to the server one",
          set(bi.LIST_HREF) == {"server", "local"} and bi.LIST_HREF["server"] == "/",
          f"LIST_HREF={bi.LIST_HREF}")
    for d in sorted((ROOT / "tests").glob("*/解答.html")):
        html = d.read_text(encoding="utf-8")
        mode = re.search(r'const STORAGE = "(\w+)"', html)
        check(f"{d.parent.name}: 解答.html is the server build",
              bool(mode) and mode.group(1) == "server",
              f"storage={mode.group(1) if mode else 'unstamped'} — "
              f"run make sheet {d.parent.name} (make pages writes the local "
              f"build into _site/, never into tests/)")
        check(f"{d.parent.name}: the server sheet carries no localStorage store",
              ls.STORAGE_PREFIX not in html,
              "two live stores would desync the list and the sheet")

    # Pages is a build artifact, never a committed deliverable.
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    check("_site/ is gitignored", "_site/" in gitignore,
          "the static site is rebuilt by CI from tests/, not committed")
    check(".nojekyll is written into the site",
          ".nojekyll" in src["build_pages.py"],
          "Jekyll would otherwise drop paths starting with _ ")

    mk = (ROOT / "Makefile").read_text(encoding="utf-8")
    for target in ("pages:", "preview-pages:"):
        check(f"Makefile has `make {target[:-1]}`", target in mk)
    doc = (AGENTS / "exam-app" / "SKILL.md").read_text(encoding="utf-8")
    check("exam-app documents the static build",
          "make pages" in doc and "localStorage" in doc,
          "the skill owns both deployments — document the second one")

    # A builder property, not a paper property (it used to be checked per test):
    # 4cad944 removed the traffic-light emoji from the report labels.
    check("build_interactive.py writes no emoji into the report labels",
          not re.search("[🟢🟡🔴]", src["build_interactive.py"]),
          "4cad944 removed them")


def check_makefile_help():
    """`make help` is hand-written; nothing else stops it drifting from the
    target list, while the SKILL.md files get exactly this class of drift
    checked by check_filename_contracts."""
    print("\nMakefile help ↔ .PHONY targets")
    mk = (ROOT / "Makefile").read_text(encoding="utf-8")
    phony: set[str] = set()
    for m in re.finditer(r"^\.PHONY:((?:.*\\\n)*.*)", mk, re.M):
        phony |= set(m.group(1).replace("\\\n", " ").split())
    missing = [t for t in sorted(phony)
               if t != "help" and f"make {t}" not in mk]
    check(f"every .PHONY target appears in `make help` ({len(phony)} targets)",
          not missing, f"undocumented: {missing}")


# ------------------------------------------------------------------ choukai pacing
def check_pacing():
    print("\nchoukai pacing table ↔ make_choukai_mp3.py constants")
    m = load(".agents/choukai-audio/scripts/make_choukai_mp3.py")
    doc = (AGENTS / "choukai-audio" / "SKILL.md").read_text(encoding="utf-8")

    for const in ("GAP_BETWEEN_LINES", "GAP_AFTER_PRE_QUESTION", "GAP_OPTION_READING",
                  "GAP_BETWEEN_SPOKEN_CHOICES", "GAP_AFTER_SHITSUMON1",
                  # Added with shape_pauses(): the inter-segment gaps above are
                  # only real because segment padding is trimmed, and these two
                  # decide what happens to a pause INSIDE one utterance.
                  "GAP_WITHIN_TURN_MAX", "SHAPE_PAUSE_FLOOR"):
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
    # SCORED items only: `pause_after()` gives an 例 the short instruction pause,
    # not answer time, because official runs the practice item straight into its
    # 「最もよいものは◯番です…」 confirmation. Counting the 例 here is what made the
    # documented histogram read 13 × 12 s / 18 × 8 s against the archive's 12 and
    # 17, a mismatch the doc then explained away as ours-not-theirs.
    expected: dict[float, int] = {}
    for sec, items in m.EXPECTED_ITEMS.items():
        scored = items - (1 if sec in m.NEEDS_EXAMPLE else 0)
        expected[m.ANSWER_PAUSE[sec]] = expected.get(m.ANSWER_PAUSE[sec], 0) + scored
    for secs, count in re.findall(r"^\|\s*(\d+) s answer\s*\|\s*(\d+)\s*\|", doc, re.M):
        check(f"dry-run: {count} × {secs}s answer pauses",
              expected.get(float(secs)) == int(count),
              f"doc {count}, derived {expected.get(float(secs))}")
    reading = re.search(r"^\|\s*20 s option-reading\s*\|\s*(\d+)\s*\|", doc, re.M)
    if reading:
        check(f"dry-run: {reading.group(1)} × 20s option-reading pauses",
              int(reading.group(1)) == m.EXPECTED_ITEMS["問題2"],
              f"doc {reading.group(1)}, 問題2 has {m.EXPECTED_ITEMS['問題2']} items")

    # A pause inside one turn must stay under the gap BETWEEN turns, or a
    # speaker's own sentence break sounds like the other person's cue.
    check("GAP_WITHIN_TURN_MAX < GAP_BETWEEN_LINES",
          m.GAP_WITHIN_TURN_MAX < m.GAP_BETWEEN_LINES,
          f"{m.GAP_WITHIN_TURN_MAX} vs {m.GAP_BETWEEN_LINES}: a within-turn pause "
          f"at or above the turn gap makes one speaker sound like two")
    check("SHAPE_PAUSE_FLOOR > GAP_WITHIN_TURN_MAX",
          m.SHAPE_PAUSE_FLOOR > m.GAP_WITHIN_TURN_MAX,
          f"{m.SHAPE_PAUSE_FLOOR} vs {m.GAP_WITHIN_TURN_MAX}: with the floor at or "
          f"below the cap, shaping would lengthen pauses it was meant to leave "
          f"alone — including the ~0.1 s 促音 closures it must never touch")


# ------------------------------------------------------------------- item counts
def check_item_counts():
    print("\n聴解 item counts ↔ EXPECTED_ITEMS ↔ jlpt-exam-structure")
    m = load(".agents/choukai-audio/scripts/make_choukai_mp3.py")

    sw = (AGENTS / "choukai-audio" / "SKILL.md").read_text(encoding="utf-8")
    row = re.search(r"Item counts \(incl\. 例\)\s*\|([^|]+)\|", sw)
    documented = {f"問題{n}": int(v) for n, v in re.findall(r"問題(\d)=(\d+)", row.group(1))} if row else {}
    check("choukai-audio item counts", documented == m.EXPECTED_ITEMS,
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
    g = load(".agents/exam-app/scripts/grade_answers.py")   # asserts tiling at import
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
    grading_doc = (AGENTS / "exam-app" / "SKILL.md").read_text(encoding="utf-8")
    for label, key, want in (("言語知識", "言語知識", 51), ("読解", "読解", 20)):
        check(f"{label} = {want} items", sect.get(key) == want, f"taxonomy gives {sect.get(key)}")
        check(f"{label} {want} documented in exam-app",
              re.search(rf"{want} questions max|{want} items", grading_doc) is not None)


# ------------------------------------------- item-level content contracts
# Everything below catches content bugs: two questions whose
# option list contained the same string twice (so two options were correct),
# a 問題8 key naming the option in the 2nd blank instead of the ★ (3rd) one,
# a cloze blank whose key pointed at a different option than its own
# explanation, and 問題5 2番 numbering its candidates in one order while the
# audio enumerated them in another. None of it is visible to the shape checks
# in check_tests().

def gengo_option_sets(md: str, bi) -> dict[int, list[str]]:
    """{question number: [option text, …]} from the question body only.

    Handles every layout in use: four options on their own line (問題1-5, 7, 8),
    one option per line (問題6, 10-14), and options trailing the stem itself on
    one line (e.g. 問題9).
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
# 文法 constants, RE-MEASURED on the 31-sitting archive
# (.agents/question-authoring/references/official_calibration.md §7/§9).
# Every one of these was derived from a single paper (July 2025) and three of
# the four failed real official papers — the gate was enforcing standards no N2
# exam meets, which is the same defect class as a wrong key.
#
# 問題7 stems, n=180 over the last 15 sittings: mean 43.1, median 39, min 17;
# 38 stems (21%) under 30, 17 (9%) under 25, 3 under 20. So the per-stem FAIL at
# 30 was fiction. It is now a WARN at 20 — even 20 clips 3 official stems, which
# is exactly why it may not fail the gate. The PAPER AVERAGE is the real rule
# and it survives: current-era per-paper averages are 36/48/39/51/43/38/43.
P7_STEM_MIN = 20            # WARN threshold only — see check_grammar_stem_lengths
P7_PAPER_AVG_MIN = 35       # survives the archive (min observed 36); author to 43
P9_PASSAGE_MIN = 450        # survives the current era (min 498); 7/2021 ran 393
# 問題8, 64 of 75 items over the last 15 sittings (§7). Bands, not one paper:
# option sum 9–41 (median 20), assembled 30–78 (median 47), options ≥5 JP chars
# 0–4 per item (median 2) — and 51% of all official options are under 5 chars.
P8_OPT_SUM_MIN = 9          # was 16, which failed 13 of 64 official items (20%)
P8_ASSEMBLED_MIN = 30       # was 45, which failed 10 of 29 current-era items (34%)
# P8_LONG_OPTS_MIN is RETIRED: at 2 it failed 24 of 64 official items (38%), and
# the archive's own floor for the measure is 0. What replaces it is a
# paper-level WARN — an item may legitimately be four short strips, but a whole
# 問題8 with no chunk of any weight anywhere is a drill shape.
P8_LONG_OPTS_PAPER_MIN = 1  # WARN: ≥5-char options summed over the five items


def jp_char_count(s: str) -> int:
    return len(JP_CHAR.findall(re.sub(r"\s+", "", s)))


def check_grammar_stem_lengths(gt: str, bi):
    """問題7/9 carrier lengths must sit near the official JLPT band.

    Generated papers have shipped 問題7 stems averaging 20–34 JP chars against an official
    ~43 average — keys looked fine, carriers read as textbook drills. The PAPER
    AVERAGE is the enforceable rule (official 36–51, n=7 current era); the
    per-stem floor is a WARN, because the archive shows official papers ship
    short individual carriers freely — 21% under 30 chars, min 17
    (official_calibration §7). A gate that fails an official paper is a wrong
    gate, so the stem-level signal may suggest but must not decide.
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
                if cur is not None:
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
                if cur is not None:
                    stems7.append((cur, jp_char_count("".join(stem_buf))))
                cur = None
                stem_buf = []
                continue
            stem_buf.append(line)
        if cur is not None:
            stems7.append((cur, jp_char_count("".join(stem_buf))))

    short = [f"{q}({n})" for q, n in stems7 if n < P7_STEM_MIN]
    avg = (sum(n for _, n in stems7) / len(stems7)) if stems7 else 0.0
    check("問題7 parses to 12 stems", len(stems7) == 12,
          f"got {len(stems7)} — the length band cannot be measured")
    warn(f"問題7 stems each ≥{P7_STEM_MIN} JP chars "
         f"(official median 39, min 17; got {[n for _, n in stems7]})",
         not short,
         f"short={short or 'n/a'} — official ships 21% of stems under 30 chars, "
         f"so this is a suspicion, not a verdict; the paper average below is "
         f"the rule (official_calibration §7)")
    check(f"問題7 stem average ≥{P7_PAPER_AVG_MIN} JP chars "
          f"(official per-paper 36–51, mean 43.1; got {avg:.1f})",
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
    strips — sum often 16–29 JP chars, with several options ≥5.
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

    bad_sum, bad_asm, long_total = [], [], 0
    for q in range(43, 48):
        o = opts.get(q) or []
        ol = [jp_char_count(x) for x in o]
        ssum = sum(ol)
        long_total += sum(1 for n in ol if n >= 5)
        asm = jp_char_count(stems.get(q, "")) + ssum
        if len(ol) != 4 or ssum < P8_OPT_SUM_MIN:
            bad_sum.append(f"{q}(sum={ssum}, opts={ol})")
        if asm < P8_ASSEMBLED_MIN:
            bad_asm.append(f"{q}(assembled~{asm})")
    check(f"問題8 four options sum ≥{P8_OPT_SUM_MIN} JP chars each item "
          f"(official band 9–41, median 20)",
          not bad_sum, "; ".join(bad_sum) + " — lengthen option chunks (see question-authoring)")
    check(f"問題8 assembled sentence ≥{P8_ASSEMBLED_MIN} JP chars "
          f"(official band 30–78, median 47)",
          not bad_asm, "; ".join(bad_asm))
    # The retired per-item ≥5-char rule, restated at the level the archive
    # actually supports: 51% of official options are under 5 chars and 38% of
    # official ITEMS carry fewer than two long ones, so per item it is noise —
    # but no official 問題8 is five items of nothing but scraps.
    warn(f"問題8 carries some phrase mass across its five items "
         f"({long_total} options of ≥5 JP chars; official median 2 per item)",
         long_total >= P8_LONG_OPTS_PAPER_MIN,
         "every option in the whole 大問 is a short strip — official mixes "
         "2–3 char particles with 8–12 char clauses (official_calibration §7)")


# R5. 問題8 construction rule 1 — "no bare adverb on a card" (question-authoring
# 「exactly ONE of the 24 orderings」). An adverb constrains neither its left nor
# its right neighbour, so it fits every slot and multiplies the valid orderings;
# avoid bare adverbs on cards which read naturally in multiple slots (e.g., ほとんど自分の時間を / 直接窓口に / 一度原点に).
#
# ONLY THE DECIDABLE HALF IS HERE, and it is a small half. Counting the 24
# orderings is not machinable at all — that stays with question-authoring's link
# table and exam-qa-review.
#
# 2026-08-11: the corpus-attested branch (an option matching a generic
# 2-6-char 〜に/〜と shape AND attested as a lexical headword in openjlpt) was
# retired with openjlpt — Shinkanzen/Soumatome have no text layer to build a
# replacement lexical index from, and the shape alone (BARE_ADVERB_SHAPE) is
# far too loose to flag on its own (it also matches ordinary noun+particle
# cards like お客様に, 状況に — construction rule 2 *requires* cards to end
# that way). Only the unambiguous 3-char-stem+的に shape remains, which needs
# no corpus: a miss here is not a pass — the link table in question-authoring
# is the rule.
#
# WARN, NOT FAIL — the flat ban is contradicted by the archive. Official 問題8
# ships bare adverbs and bare particles as standalone cards: 12/2023-47 「一度」,
# 12/2024-43 「もう」, 7/2025-43 「もちろん」, 7/2025-44 「珍しく」, 12/2024-44
# 「だけ」「する」「して」 — 4 of 29 current-era items (14%) carry one, and 51% of
# all official options are under 5 JP chars (official_calibration §7, §9). The
# real invariant is single-solution uniqueness, which a bare adverb ENDANGERS
# but does not by itself violate, and uniqueness is not machinable.
# 3-char stem + 的に is unambiguously adverbial (積極的に/具体的に/一方的に);
# a 2-char stem is not (目的に is a noun taking に), hence the exact {3}.
NA_ADVERB_SHAPE = re.compile(r"^.{3}的に$")


def check_mondai8_bare_adverbs(name: str, opts: dict[int, list[str]]):
    hits = []
    for q in range(43, 48):
        for i, opt in enumerate(opts.get(q) or [], 1):
            o = opt.strip()
            if not o:
                continue
            if NA_ADVERB_SHAPE.match(o):
                hits.append(f"{q}-{i}「{o}」")
    warn(f"{name}: no 問題8 option is a bare adverb", not hits,
         "; ".join(hits) + " — an adverb alone constrains neither neighbour, so "
         "it multiplies the valid orderings; check this item's link table for a "
         "second defensible ★ before shipping it. Official DOES ship bare "
         "adverb cards (一度/もう/もちろん/珍しく), so this is a suspicion, not a "
         "verdict — the rule is uniqueness, not the ban "
         "(question-authoring 問題8; official_calibration §7)")


LEVEL_BAND_PATH = (
    AGENTS / "question-authoring" / "references" / "level_band_grammar.txt"
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
                             opts: dict[int, list[str]], origin: str,
                             test_id: str = ""):
    """Generated 問題7–9 keys must stay inside the N2 band.

    String-decidable half of exam-qa-review §2.5. Imported papers are skipped
    (they reproduce an outside source). Generated papers have shipped N1 keys
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
          "; ".join(hard) + " — see question-authoring/references/level_band_grammar.txt")
    check("問題7–9 keys are not N3–N5-easy (level band)", not easy,
          "; ".join(easy) + " — see question-authoring/references/level_band_grammar.txt")

    # 問題8 keys are option STRIPS, so the banned form never appears whole in one:
    # an item has tested 〜ば〜ほど with the option reading 「触れるほど」 and the
    # loop above saw nothing. The spec names the grammar point it drew, so match
    # that instead — the only place 問題8's target is written down.
    spec_path = ROOT / "tests" / test_id / "test_spec.json"
    if not spec_path.is_file():
        return
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if str(spec.get("test_id")) != test_id:
        return skip(f"{test_id}: 問題8 target grammar points stay inside the N2 band",
                    f"spec is for test {spec.get('test_id')}, not {test_id}")
    p8 = []
    for entry in spec.get("items", {}).get("grammar_p8", []):
        label = entry.get("item") if isinstance(entry, dict) else entry
        probe = (label or "").replace("〜", "").replace("～", "")
        for group in ("TOO_HARD", "TOO_EASY"):
            for ban in _level_band_hits(probe, band[group], band["ALLOW"]):
                p8.append(f"{label} ({group}: {ban})")
    check(f"{test_id}: 問題8 target grammar points stay inside the N2 band "
          f"({len(spec.get('items', {}).get('grammar_p8', []))} drawn)", not p8,
          "; ".join(p8) + " — the pool handed the author a banned form; delete "
          "it from pools.json and re-sample (exam-blueprint)")


def check_grammar_p8_targets(gt: str, opts: dict[int, list[str]], test_id: str):
    """問題8: each drawn grammar_p8 target must surface in its printed item.

    20260811_1 shipped 問題8-45 with spec AND ledger recording 「〜に基づいて」
    while the printed item tested a まず/次に/さらに sequencing scramble — the
    author substituted the construction and left no record, and no gate line
    looked at the assembled text (QA F1, qa/qa-report-20260811_1.md §5):
    check_scramble_stars() proves only the ★/key mechanics, and the level-band
    pass reads only the drawn LABEL, never the paper.

    WARN, not FAIL: a target can legitimately surface inflected (「〜ずじまい」
    as 「行かずじまい」), so absence of the literal string is evidence of a
    silent substitution, not proof. The probe therefore also accepts each
    segment with up to 2 trailing chars trimmed (「に基づいて」→「に基づ」 still
    matches 「に基づき」). Resolve each hit by reading the item, and either
    restore the drawn target or record the substitution (origin "reauthored"
    is NOT a valid provenance for tested pool items — re-sample instead,
    exam-blueprint 'Rotation model').
    """
    spec_path = ROOT / "tests" / test_id / "test_spec.json"
    if not spec_path.is_file():
        return
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if str(spec.get("test_id")) != test_id:
        return skip(f"{test_id}: 問題8 items realize their drawn grammar_p8 targets",
                    f"spec is for test {spec.get('test_id')}, not {test_id}")
    entries = spec.get("items", {}).get("grammar_p8", [])
    if not entries:
        return

    m8 = re.search(r"^##\s*問題8\b.*?(?=^##\s*問題9\b)", gt, re.M | re.S)
    sec = m8.group(0) if m8 else ""
    blocks: dict[int, str] = {}
    cur = None
    for line in sec.splitlines():
        # Item numbers print as bold-only (`**47**`) with no trailing
        # punctuation before the stem text — a stricter pattern silently
        # matched nothing, so blocks[] stayed empty and every target had to
        # be found inside the option strips alone (missing stem-only targets
        # like 47's にちがいない tail, caught only by reading the rendered gate
        # output against the actual Markdown, not by trusting the check).
        qm = re.match(r"^\s*\*{0,2}(4[3-7])\*{0,2}[\.．、]?", line)
        if qm:
            cur = int(qm.group(1))
            blocks[cur] = line
        elif cur is not None:
            blocks[cur] += line
    missing = []
    for i, entry in enumerate(entries):
        q = 43 + i
        label = str(entry.get("item") if isinstance(entry, dict) else entry)
        core = re.search(r"[（(]([^）)]+)[）)]", label)
        core = core.group(1) if core else label
        # Only the FIRST segment is the grammar marker itself; later segments
        # (「…する」「…てしまった」) are realization placeholders that conjugate
        # freely on the paper and would warn on every legitimate item.
        segs = [s for s in re.split(r"[〜～…]", core) if len(s) >= 2][:1]
        # A target may straddle two option strips in assembled order
        # (20260811_1 問題8-47: 「…ことを」+「きっかけに」 realizes
        # 〜をきっかけに), so probe every ordered option pair as well —
        # '§' keeps unrelated pairs from matching across the join.
        o = opts.get(q) or []
        pairs = "§".join(a + b for a in o for b in o if a != b)
        hay = re.sub(r"\s+", "", blocks.get(q, "") + "".join(o) + "§" + pairs)
        for seg in segs:
            probes = {seg[: len(seg) - k] for k in range(3) if len(seg) - k >= 2}
            # な-adjective/noun stems take で, not て, before a て-form marker
            # (心配でたまらない, 残念でたまらない) — probe that variant too, or
            # every such target WARNs on its own most textbook-standard use
            # (20260817_1 QA G5: 問題8-47 感情強調〜てたまらない realized as
            # 心配でたまらない, a real false positive).
            if seg.startswith("て") and len(seg) > 1:
                de = "で" + seg[1:]
                probes |= {de[: len(de) - k] for k in range(3) if len(de) - k >= 2}
            if not any(p in hay for p in probes):
                missing.append(f"{q}:「{label}」 (segment 「{seg}」 absent)")
                break
    warn(f"{test_id}: 問題8 items realize their drawn grammar_p8 targets "
         f"({len(entries)} drawn)", not missing,
         "; ".join(missing) + " — the printed item does not contain its drawn "
         "grammar point (silent substitution shipped as 20260811_1 問題8-45): "
         "rewrite the item around the drawn target, or re-sample the slot; "
         "never leave spec/ledger recording a construction the paper does not test")


def check_scramble_stars(gt: str, keys: dict[int, int], opts: dict[int, list[str]]):
    """問題8: the key must name the option that lands on ★ (the 3rd blank).

    Both facts are checkable from the Markdown alone: the stem must offer four
    blanks with ★ on the third, and the 解説 cell must spell the word order out
    as `語(n)→語(n)→語(n)→語(n)`, whose 3rd entry is the answer. A paper has
    shipped with three of five keys naming a different blank, and one 解説
    citing option numbers that did not exist in the stem.
    """
    m8 = re.search(r"^##\s*問題8\b.*?(?=^##\s*問題9\b)", gt, re.M | re.S)
    m8_text = m8.group(0) if m8 else ""
    stems = {int(n): s for n, s in re.findall(r"^\*\*(\d+)\*\*\s*(.+)$", m8_text, re.M)}
    q_list = sorted(stems.keys()) if stems else list(range(43, 48))
    bad_stem = []
    for q in q_list:
        run = BLANK_RUN.search(stems.get(q, ""))
        slots = run.group().split() if run else []
        if len(slots) != 4 or [i for i, s in enumerate(slots) if "★" in s] != [2]:
            bad_stem.append(f"{q}({len(slots)} blanks, ★ at "
                            f"{[i + 1 for i, s in enumerate(slots) if '★' in s]})")
    check("問題8 stems offer 4 blanks with ★ third", not bad_stem, ", ".join(bad_stem))

    mismatch, unparsed = [], []
    for hit in re.finditer(r"^\|\s*(\d+)\s*\|\s*([1-4])\s*\|(.*)\|", gt, re.M):
        q = int(hit.group(1))
        if q not in q_list:
            continue
        ans, expl = int(hit.group(2)), hit.group(3)
        raw_matches = re.findall(r"語[（(]([1-4])[）)]|[（(]([1-4])[）)]", expl)
        seq = [int(m[0] or m[1]) for m in raw_matches]
        if sorted(seq) != [1, 2, 3, 4]:
            unparsed.append(f"{q}(order={seq or 'none'})")
        elif seq[2] != ans:
            mismatch.append(f"{q}: key={ans} but ★(3rd) is option {seq[2]}")
    check("問題8 解説 spells the word order as a 1-4 permutation", not unparsed,
          f"{', '.join(unparsed)} — write `語(1)→語(4)→語(2)→語(3)`")
    check("問題8 keys name the option on ★", not mismatch, "; ".join(mismatch))

    # The option strips ARE the missing span, so the stem must not already
    # contain them. A paper has shipped all five items with the whole sentence
    # written out in the stem AND chopped into the options, so every permutation
    # read `…本番でパニックになってパニックになってうろたえる…`. The star and
    # permutation checks above pass happily on that — neither reads the stem's
    # own words. Two signals, both chosen to leave honest repetition alone
    # (item 46 in one paper legitimately says 新しい町 in the stem and 新しい in an option):
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
# says 「単なる無音の contrast ではない」 (問題9) got half-written in
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


def check_dokkai_span_anchor_bold(name: str, gt_prose: str):
    """Every `「…」とあるが`-anchored stem must point at a BOLDED, MARKED
    passage span — never a bare 「quote」 with no marker at all.

    20260817_1 shipped three span-anchored stems (57, 59, 67) as plain
    「quoted text」とあるが with neither ①/② nor bold in the stem OR the
    passage — a reader opening the booklet had no visual cue for which words
    the question pointed at. check_dokkai_numbered_markers above could not
    catch it: it only compares passage markers vs question markers as SETS,
    so a passage/question pair with zero markers on both sides matches
    trivially. This check reads the stem shape directly instead.

    A marker present but not bolded (20260817_2's `②その結果`/`⑤…`) is the
    milder half of the same defect — WARN, not FAIL, since a bare marker at
    least gives the set-match check above something to pair, and it already
    shipped that way in one paper.
    """
    bare_quote = []
    for m in re.finditer(r"^\*\*(\d+)\*\*\s*([^\n]*?とあるが)", gt_prose, re.M):
        q, anchor = m.groups()
        if "「" in anchor and "」" in anchor and not re.search(r"[①②③④⑤]", anchor):
            bare_quote.append(q)
    check(f"{name}: とあるが stems anchor on a bolded ①/② marker, never a bare 「quote」",
          not bare_quote,
          f"item(s) {bare_quote} quote passage text in 「」 with no ①/②/③ marker in "
          f"the stem — bold the exact span in the passage as ①**…** and reference it "
          f"the same way in the stem (question-authoring/references/dokkai.md "
          f"§\"Marked-span quoting\")")

    unbolded_markers = sorted(set(re.findall(r"[①②③④⑤](?!\*\*)", gt_prose)))
    warn(f"{name}: every ①/② marker is immediately bolded (①**…**), never bare",
         not unbolded_markers,
         f"marker(s) {unbolded_markers} appear without an immediately-following ** — "
         f"bold the whole marked span, not just the circled number")


# The marked span is a POINTER into the passage, not a highlighter over the
# answer. Both numbers are measured on the 31-sitting archive (55 spans quoted
# in 問題10–13 stems, `[①-⑦]…(とあるが|とは|のはなぜ|について、筆者)`): min 2,
# median 8, p95 23, max 34. Generated papers ran median 22, max 72, with 19 of
# 57 spans (33%) over the official p95 against official's 1 of 55 (1.8%).
SPAN_JP_MAX = 35        # FAIL above — official max 34 plus one char of headroom
SPAN_JP_WARN = 25       # WARN above — 54 of 55 official spans sit at or below
SPAN_MARK = re.compile(r"([①-⑦])\*\*(.+?)\*\*")
SPAN_NOTE = re.compile(r"[（(]注\d*[）)]")


def dokkai_span_pairs(gt_prose: str):
    """Every `[①-⑦]**span**` in 問題10–14, in reading order, passage side paired
    with the stem that references it.

    Yields `(passage_occurrence, stem_occurrence_or_None)`. A marker char is
    reused by every passage (each numbers its own spans ①②③…), so pairing is
    positional, not by character: a passage span pairs with the NEXT stem
    bearing the same marker, and the search stops at the next passage span
    bearing it — that boundary is what keeps 問題10's five ①s apart.
    """
    start = re.search(r"^##\s*問題10\b", gt_prose, re.M)
    region = gt_prose[start.start():] if start else gt_prose
    occ = []
    for lineno, line in enumerate(region.splitlines(), 1):
        stem = re.match(r"^\*\*(\d+)\*\*", line)
        for m in SPAN_MARK.finditer(line):
            occ.append({"line": lineno, "mark": m.group(1), "span": m.group(2),
                        "stem": stem.group(1) if stem else None})
    for i, o in enumerate(occ):
        if o["stem"]:
            continue
        partner = None
        for cand in occ[i + 1:]:
            if cand["mark"] != o["mark"]:
                continue
            if cand["stem"] is None:
                break
            partner = cand
            break
        yield o, partner


def check_dokkai_span_anchor_identity(name: str, gt_prose: str):
    """A marked span must be the SAME characters in the passage and in the stem,
    and short enough to be a pointer rather than the answer itself.

    `check_dokkai_span_anchor_bold` above proves a marker and bold EXIST on both
    sides; it never compares what they enclose. 20260817_2's item 57 bolded 72
    JP chars of passage — 「特定空き家に指定されると、所有者に修繕や解体の指導・
    勧告が行われ、これに従わない場合は、住宅用地に対する固定資産税の軽減措置（注4）
    が打ち切られる」 — while its stem quoted only the 12-char opening clause. Both
    defects at once: the reader sees two different spans for one ①, and the bold
    runs a highlighter over the sentence that IS the key, so the item is keyable
    by eye without reading the paragraph (2026-08-18, user report).

    A （注N） gloss inside the bold is the same rule's other half — dokkai.md
    already says the gloss sits OUTSIDE the bold, and 20260810_2/20260812_1 both
    shipped one inside, which is why their two sides differed by exactly the
    gloss. Reported separately so the repair is obvious.

    Lengths are gated because the identity rule alone picks no winner: told only
    "make the two sides match", an author can as easily lengthen the stem as
    shorten the bold, and lengthening is the wrong direction.
    """
    mismatched, gloss_in_bold, orphan, too_long, long_warn = [], [], [], [], []
    for passage, stem in dokkai_span_pairs(gt_prose):
        if SPAN_NOTE.search(passage["span"]):
            gloss_in_bold.append(f"{passage['mark']}「{passage['span']}」")
        if stem is None:
            orphan.append(f"{passage['mark']}「{passage['span'][:20]}…」")
        elif SPAN_NOTE.sub("", passage["span"]) != stem["span"]:
            mismatched.append(
                f"item {stem['stem']} {passage['mark']}: passage bolds "
                f"[{jp_char_count(passage['span'])} chars]「{passage['span']}」 but the stem quotes "
                f"[{jp_char_count(stem['span'])} chars]「{stem['span']}」")
        n = jp_char_count(SPAN_NOTE.sub("", passage["span"]))
        where = f"item {stem['stem']}" if stem else f"line {passage['line']}"
        if n > SPAN_JP_MAX:
            too_long.append(f"{where} {passage['mark']} = {n} JP chars")
        elif n > SPAN_JP_WARN:
            long_warn.append(f"{where} {passage['mark']} = {n} JP chars")

    check(f"{name}: passage span and stem quote are the same characters",
          not mismatched,
          "; ".join(mismatched) + " — the two sides of one ① must be "
          "character-identical; shorten the PASSAGE bold to the stem's span "
          "(never lengthen the stem), then re-check the key is still not "
          "answerable from the span alone (question-authoring/references/"
          "dokkai.md §\"Marked-span quoting\")")

    check(f"{name}: no （注N） gloss inside a bolded marked span",
          not gloss_in_bold,
          "; ".join(gloss_in_bold) + " — move the gloss outside the bold "
          "(①**重ね合わせ**（注2）, never ①**重ね合わせ（注2）**); inside, it makes "
          "the passage and stem spans differ by construction")

    check(f"{name}: every marked passage span is quoted by a stem",
          not orphan,
          "; ".join(orphan) + " — an ① with no stem referencing it points the "
          "reader at nothing")

    check(f"{name}: marked spans stay pointer-sized (≤{SPAN_JP_MAX} JP chars)",
          not too_long,
          "; ".join(too_long) + f" — official spans run 2–34 JP chars (median 8, "
          f"n=55 over 31 sittings); past {SPAN_JP_MAX} the bold stops pointing at "
          "a phrase and starts underlining the answer. Move the span onto the "
          "clause the question actually turns on, in BOTH the passage and the stem")

    warn(f"{name}: marked spans near the official median (≤{SPAN_JP_WARN} JP chars)",
         not long_warn,
         "; ".join(long_warn) + f" — 54 of 55 official spans are ≤{SPAN_JP_WARN} "
         "(median 8); author to a phrase, not a sentence")


# ------------------------------------------------------- 読解 passage anatomy
# One splitter, four checks. （注N） numbering restarts per passage, passage
# length is measured per passage, （中略） has to sit INSIDE one, and the same
# regions feed the 問題11 stem check — so the scoping lives in one place.
PASSAGE_MARKER = re.compile(r"^(?:###\s*|\*\*)\(\d+\)", re.M)
NOTE_DEF = re.compile(r"^\s*[（(]注(\d*)[）)]\s*([^：:）)]{1,24})\s*[：:](.*)$")
NOTE_MARK = re.compile(r"[（(]注(\d*)[）)]")


def dokkai_section(body: str, n: int) -> str:
    """The 問題N block of the passage prose (`body` already has keys cut off)."""
    m = re.search(rf"^##\s*問題{n}\b.*?(?=^##\s*問題{n + 1}\b|\Z)", body, re.M | re.S)
    return m.group(0) if m else ""


def passage_scopes(sec: str, n: int) -> list[str]:
    """One region per passage — the scope （注N） numbers restart in.

    問題11 marks its passages `### (1)` / `**(1)**`; 問題10 has none, so each of
    its five passages is the run up to the next stem (a passage's note block
    sits with its own markers either way). 問題12–14 number their notes once
    across the whole section (official July 2025 does the same), so they are a
    single scope — splitting A/B there has invented four orphans in a generated paper.
    """
    if n == 11:
        parts = PASSAGE_MARKER.split(sec)
        return parts[1:] or [sec]
    if n == 10:
        # No `\s*` after `^`: it lets the lookahead also succeed on the blank
        # line above the stem, which doubles every split point.
        parts = re.split(r"(?=^\*\*5[2-6]\*\*)", sec, flags=re.M)
        if len(parts) > 2:      # fold the tail after **56** back into passage 5
            parts = parts[:-2] + [parts[-2] + parts[-1]]
        return parts
    return [sec]


def passage_prose(sec: str, bi) -> str:
    """The passage text only: no instruction line, no stems, no option rows.

    Keeps （注N） definition lines, which are part of the reading apparatus the
    candidate has to process. This function's own measurement of July 2025 is
    問題10 1249 / 問題11 2451 / 問題12 572 / 問題13 989 / 問題14 604 JP chars
    (official_calibration §2). Three different numbers for that one paper are on
    record across the repo because the counting method was never named beside
    them; the method here is JP chars only (the JP_CHAR class), passage region
    only, （注N） definition lines kept — say so wherever you quote a number.
    """
    keep = []
    for ln in sec.splitlines():
        if re.match(r"^##\s*問題", ln) or re.match(r"^\s*\*\*\d+\*\*", ln):
            continue
        if bi.OPTION.match(ln) or bi.option_run(ln):
            continue
        keep.append(ln)
    return "\n".join(keep)


# RE-MEASURED on the archive (official_calibration §2, §9). The old floors were
# ~90% of ONE paper (July 2025) and three of the five failed real official
# papers — the gate was demanding lengths no N2 exam reaches. The window is the
# 7 sittings 12/2022–12/2025, because 問題11 changed from 3 passages to 4 in
# 12/2022 and its length jumped with it; averaging older papers in would set
# 問題11 far too low.
#
#   大問   official min / median / max (n=7)   old floor   new floor
#   問題10      1143 / 1225 / 1329               1150 → FAILED 12/2023 by 7 chars
#   問題11      2449 / 2556 / 2685               2250   kept (4-passage format ONLY)
#   問題12       532 /  551 /  592                510   kept
#   問題13       814 /  904 / 1061                900 → FAILED 12/2022 and 7/2024
#   問題14       489 /  604 /  638                560 → FAILED 12/2024 and 12/2025
DOKKAI_FLOOR = {10: 1100, 11: 2250, 12: 510, 13: 800, 14: 450}
# 問題14 stays in JP chars, floored at 450, rather than switching to all-char at
# 620. All-char is the truer measure of that section (the flyer is dates, prices
# and times, so JP-char counting reads ~25% short, and all-char lands on JEES's
# published 700字程度) — but this one section would then be the only one counted
# a different way, and a mixed-unit table is exactly how the repo ended up with
# three different lengths on record for one paper. One unit for all five, and
# the floor set under the observed JP-char minimum of 489.
#
# Per passage: official current-era minima are 問題10 157 (12/2023 passage 5,
# below JEES's own 200字 spec — short 短文 are allowed) and 問題11 507.
DOKKAI_PASSAGE_FLOOR = {10: 150, 11: 400}
# In-body （注N） markers per paper: official current era 27–61, median 39.
GLOSS_MARKER_MIN = 25

# The "X alone is not enough — what really matters is Y" closing family. Two
# passages on unrelated subjects that both end this way are one essay written
# twice, and no theme tag can see it: 20260810_1 ran the move in NINE of its ten
# essay-type passages, so its keys became the soft-sounding option beside
# 「Xさえすれば十分」 strawmen and eight 読解 items were answerable without
# reading a passage (question-authoring/references/dokkai.md §"Thirteen
# surfaces, thirteen different essays").
#
# MEASURED over the 問題10→end region of the 31-sitting archive, stems and
# options included (the strawman distractors are part of the defect):
#   official  5 5 5 6 6 9 9  (n=7 current era; max 9)
#   generated 19 / 28 / 29
# WARN, not FAIL, and the ceiling sits at 12 — official max plus a third — so no
# real paper trips it and the line means "this paper argues one way only", not
# "you used こそ". It is a rewrite instruction: the fix is varying the CLOSING
# MOVE of each passage (dokkai.md lists the six official shapes), never
# find-and-replacing the markers, which leaves thirteen identical arguments
# behind different wording.
RHETORIC_MARKERS = {
    "だけで": re.compile(r"だけで(は|も)?(?!き)"),
    "こそ": re.compile(r"こそ"),
    "て初めて": re.compile(r"[てで]初めて"),
    "求められ/欠かせな": re.compile(r"求められ|欠かせな"),
    "ではないだろうか": re.compile(r"ではないだろうか|のではないか|ではないか。"),
}
RHETORIC_CEILING = 12


def check_dokkai_rhetorical_monotony(name: str, body: str):
    """One paper, thirteen different essays — not one essay thirteen times.

    `body` is the 言語知識・読解 source with the key tables already cut; the
    region measured is 問題10 to the end of it, matching how the official band
    above was measured.
    """
    m = re.search(r"^##\s*問題10\b", body, re.M)
    if not m:
        return
    region = body[m.start():]
    counts = {k: len(v.findall(region)) for k, v in RHETORIC_MARKERS.items()}
    total = sum(counts.values())
    split = " ".join(f"{k}={v}" for k, v in counts.items() if v)
    warn(f"{name}: 読解 closing-move variety ({total} markers, official 5-9)",
         total <= RHETORIC_CEILING,
         f"{split} — {total} uses of the 「〜だけでは足りない、〜こそが要る」 "
         f"family against an official band of 5-9 per 読解 half (ceiling "
         f"{RHETORIC_CEILING}). Label each passage's closing move and rewrite "
         f"until no more than two share one; then re-check that the keys did "
         f"not inherit it (question-authoring/references/dokkai.md "
         f"§'Thirteen surfaces, thirteen different essays')")


# The "not-A(system/singular)-but-B(human/relational) reframe" shape
# specifically — one narrow slice of the broader RHETORIC_MARKERS family, but
# the one dokkai.md caps at 2 SHARED PASSAGES (not 12 raw hits paper-wide).
# 20260812_1 shipped 6 of 13 closings on this exact shape while
# check_dokkai_rhetorical_monotony() stayed green (6 raw hits under its
# ceiling of 12) because that check counts markers anywhere in the WHOLE
# passage body (by design, to catch strawman distractors) — its hits landed
# mid-passage and even inside one distractor option's own printed text, not
# on the 6 closings that actually shared this shape (qa/qa-report-20260812_1.md
# F2). A per-passage, closing-region-only proxy is added here instead of
# narrowing the existing check, which stays as designed for its own
# documented purpose (qa-report F2's root-cause table, option 2).
REFRAME_CLOSING = re.compile(
    r"だけでは|だけのものではなく|にとどまらない|にすぎない.{0,20}ではなく"
    r"|である前に.{0,20}だ|の中にこそ"
    r"|こそが?.{0,15}(だ|になっている|を作り上げている|が要る|にほかならない)")
# Bare 「ではなく」 was tried and dropped: it is an ordinary contrastive
# connector that appears in unrelated argumentative and descriptive prose
# (measured: it alone fires this check on EVERY one of the 4 prior generated
# papers, none of which QA flagged for this defect — a check that fails 100%
# of the archive trains the operator to ignore it, exactly what a gate must
# not do). The narrower family above stays close to dokkai.md's own named
# example phrase ("〜だけでは足りない、〜こそが要る") instead of any A-vs-B
# contrast. 「である前に…だ」/「の中にこそ」 were added after 20260812_1 QA
# round 2 (F3): a fix pass swapped 「ではなく」 for 「である前に」 to dodge this
# very check while shipping the identical shape — confirmed absent from all 4
# prior papers before adding, so this extension does not reproduce the
# bare-「ではなく」 cry-wolf mistake (qa/qa-report-20260812_1.md F3 root-cause).
# The bare 「こそが」 alternative was added after 20260813_1 QA round 2 (F1):
# the check's only 「こそ」 variant was the narrow 「の中にこそ」 phrase, which
# missed ordinary 「〜こそが〜だ/になっている/を作り上げている」 closings — the
# shape's OWN named example phrasing in dokkai.md ("Cこそが") — and reported a
# false "0 matched" on two passages that genuinely shared the 主張 shape
# (qa-report-20260813_1.md F1 root-cause).
# This marker family is a proxy, not a shape-classification proof — a fix that
# dodges these specific tokens while keeping the same argument can still slip
# through; the mandatory human read of all 13 closings against dokkai.md's six
# named shapes (exam-qa-review) is what actually enforces the rule.
REFRAME_CLOSING_SPAN = 2000  # JP chars from the end of a passage's prose
# Was 150. qa-report-20260813_2.md ROUND 2 (F-CLOSING-2): 問題11(4) and 問題13
# both carried a literal override phrase (ではなく / だけでは) well before their
# final sentence — 問題11(4)'s sat ~225 JP chars before the passage's end — so
# a fix (or an author) could relocate the phrase earlier in the closing
# paragraph, keep the final sentence phrased as a correlation, and dodge this
# check entirely while the true dokkai.md-forced shape was still 主張. 2000 JP
# chars comfortably exceeds every passage in this repo (問題13, the longest
# non-cloze passage class, runs ~800-1070; 問題11 ~500-2700 for all 4 combined,
# each individual passage well under 1000) and every current-era official
# sitting (問題13 max ~1000, `references/official_calibration.md`), so in
# practice this now scans each passage's FULL prose, not just its tail — the
# root-cause table's "scan the whole passage body" option, implemented by
# widening the existing window rather than adding a second code path.
REFRAME_SHAPE_CAP = 2        # dokkai.md's own stated per-shape ceiling


def check_dokkai_closing_reframe(name: str, body: str, bi):
    """No more than 2 読解 passages may close on the same reframe shape.

    Scans the last `REFRAME_CLOSING_SPAN` JP characters of each passage's own
    prose (via `passage_prose`, which already strips stems/options and
    distractor text, so a hit is never scattered through the body or inside
    an option's own printed text). `REFRAME_CLOSING_SPAN` is set wide enough
    to cover any passage's full prose in practice (see its own comment) —
    scanning only a short tail let an override phrase escape detection by
    sitting earlier in the closing paragraph while the final sentence still
    read as a correlation (qa-report-20260813_2.md ROUND 2, F-CLOSING-2).
    """
    hits: dict[str, str] = {}
    m9 = re.search(r"^##\s*問題9\b.*?(?=^##\s*問題10\b)", body, re.M | re.S)
    if m9:
        prose9 = passage_prose(m9.group(0), bi)
        tail = jp_tail(prose9, REFRAME_CLOSING_SPAN)
        if REFRAME_CLOSING.search(tail):
            hits["問題9"] = tail[-40:]
    for n in (10, 11, 12, 13):
        sec = dokkai_section(body, n)
        if not sec:
            continue
        for i, scope in enumerate(passage_scopes(sec, n), 1):
            prose = passage_prose(scope, bi)
            tail = jp_tail(prose, REFRAME_CLOSING_SPAN)
            if not tail.strip():
                continue
            if REFRAME_CLOSING.search(tail):
                label = f"問題{n}" if len(passage_scopes(sec, n)) == 1 else f"問題{n}({i})"
                hits[label] = tail[-40:]
    warn(f"{name}: no more than {REFRAME_SHAPE_CAP} 読解 passages match this "
         f"marker family for the 「not-A-but-B」 reframe closing "
         f"({len(hits)} matched — a marker-family PROXY, not a shape-"
         f"classification proof: a fix can dodge these exact tokens while "
         f"keeping the same argument, as 20260812_1's own F2→F3 did)",
         len(hits) <= REFRAME_SHAPE_CAP,
         f"{sorted(hits)} — dokkai.md caps any one closing shape at "
         f"{REFRAME_SHAPE_CAP} shared passages; rewrite the extras onto a "
         f"different catalogued shape (説明/意外な観察/反論応答/随筆/条件提示) "
         f"and re-check that any key relying on the old closing's content "
         f"still matches the new one. A green run here is NOT proof the "
         f"paper complies — read all 13 closings against dokkai.md's six "
         f"named shapes yourself and write which one each is "
         f"(question-authoring/references/dokkai.md "
         f"§'Thirteen surfaces, thirteen different essays')")


def jp_tail(text: str, n: int) -> str:
    """Last `n` JP characters of a passage's CLOSING (JP_CHAR class), order preserved.

    `passage_prose()` deliberately keeps the trailing （注N） glossary block
    (needed for the length checks), but those definition lines sit AFTER the
    passage's actual closing sentence — a 5-gloss passage can push the whole
    tail window into glossary text and never reach the closing at all. Strip
    glossary lines first so the window lands on prose.
    """
    no_gloss = "\n".join(ln for ln in text.splitlines()
                          if not re.match(r"^\s*（注\d*）|^\s*\(注\d*\)", ln))
    chars = [c for c in no_gloss if JP_CHAR.match(c)]
    return "".join(chars[-n:])


# F-ABS-QUANT (qa-report-20260813_2.md). A 読解 distractor eliminable purely by
# spotting an absolute quantifier or categorical denial — before the passage is
# even opened — is an automatic QA fail per exam-qa-review/SKILL.md's own
# ground-rule list, but nothing on the authoring or gate side ever told an
# author to avoid writing one, and all 8 generated papers on disk shipped at
# least one. WARN only, never check()/FAIL: the scan cannot tell an
# on-sight-eliminable use (「同居の問題はすべて解決する」) apart from a
# content-dependent one that merely CONTAINS the token
# (「戸籍謄本もすべてオンライン提出できる」, real 20260813_1 text, judged NOT a
# violation) — that call is a human's (question-authoring/references/dokkai.md
# §"読解 distractors — no free eliminations"). Closed set, matching
# exam-qa-review's own parenthetical exactly (「全く」 added as the same word's
# kanji spelling, not a new marker).
ABS_QUANT_MARKERS = {
    "すべて": re.compile(r"すべて"),
    "まったく/全く": re.compile(r"まったく|全く"),
    "のみ": re.compile(r"のみ"),
    "だけで十分": re.compile(r"だけで十分"),
    "無関係": re.compile(r"無関係"),
    "存在しない": re.compile(r"存在しない"),
}
ABS_QUANT_QRANGE = range(52, 72)  # 問題10-14, per gengo_option_sets' numbering


def check_dokkai_abs_quantifiers(name: str, opts: dict[int, list[str]]):
    """WARN: flag 問題10-14 options carrying an absolute-quantifier/categorical-
    denial marker as CANDIDATES for the F-ABS-QUANT ground rule — a human must
    still judge whether each hit is truly eliminable on sight or merely
    contains the token in a content-dependent sentence (see constant comment
    above and dokkai.md).
    """
    hits = []
    for q in ABS_QUANT_QRANGE:
        for opt in opts.get(q, []):
            found = sorted(k for k, pat in ABS_QUANT_MARKERS.items() if pat.search(opt))
            if found:
                hits.append(f"問{q} {found}: 「{opt}」")
    warn(f"{name}: 問題10-14 options carry no on-sight absolute-quantifier/"
         f"categorical-denial marker ({len(hits)} candidate(s) to judge by hand)",
         not hits,
         "; ".join(hits) + " — eliminable purely by this marker, without "
         "checking the passage, is an automatic QA fail (exam-qa-review); a "
         "content-dependent use is fine — judge each by hand against the "
         "passage (question-authoring/references/dokkai.md "
         "§'読解 distractors — no free eliminations')")


# The 読解 surfaces of a logs/topics.json row, and which of them are headline
# surfaces (exam-blueprint §"The four theme rules").
READING_SURFACE = re.compile(r"^問題(9|1[0-4])(\(|$)")
HEADLINE_READING = ("問題9", "問題12", "問題13", "問題14")


def surface_group(key: str) -> str:
    """`問題12(A)` and `問題12(B)` are ONE surface; `問題10(3)` is its own."""
    return key.split("(")[0] if key.startswith("問題12") else key


def _headline_parts(themes: dict) -> tuple[set[str], set[str]]:
    """(reading-headline themes, 聴解問題5 themes) — the two halves of the
    5-surface headline set (`exam-blueprint` §"The four theme rules": 問題9
    cloze, 問題12 A/B as ONE surface, 問題13, 問題14, 聴解問題5). `問題12` only
    ever appears as `問題12(A)`/`問題12(B)` keys, never the bare literal
    `問題12` — folding through `surface_group()` is required, or 問題12 silently
    never enters the headline set at all (the bug this helper fixes; verified
    against every row on disk, no test's own-paper clash check changes).
    Shared by `check_topics_themes()` (same-test clash, rule 1) and
    `check_theme_repeat_cross_test()` (cross-test repeat, rule 4) so the
    5-surface list has one owner.
    """
    head = {v for k, v in themes.items() if surface_group(k) in HEADLINE_READING}
    m5 = {v for k, v in themes.items() if k.startswith("聴解問題5")}
    return head, m5


def headline_theme_set(themes: dict) -> set[str]:
    """The paper's 5-surface headline theme set, flattened to one set."""
    head, m5 = _headline_parts(themes)
    return head | m5


def check_topics_themes():
    """The four theme rules, applied to the SHIPPED paper.

    `sample_items.check_theme_spread()` sees only the draw, and a spec records
    no theme at all for its `cloze_topic` or for any `"origin": "web"` entry.
    20260810_1 drew two `働き方` reading topics — at the cap of the day — and
    shipped FIVE workplace-institution reading surfaces (問題9 熱中症対策 /
    問題10(4) 育休メール / 問題11(1) メンタルヘルス / 問題11(4) 転職と定着 /
    問題12 ワーケーション) with every gate green, because the cloze and the two
    web seeds were invisible and one passage had been authored away from its
    pool tag. The only record of what a paper actually tests is
    logs/topics.json, so that is where the rule has to be enforced.

    Rows written before the `themes` field WARN rather than fail — the field is
    additive, and a missing theme map is "unrecorded", not "compliant".
    """
    print("\ntopic themes (one 読解 surface, one theme)")
    path = ROOT / "logs" / "topics.json"
    if not path.is_file():
        return skip("logs/topics.json themes", "no topics.json on disk")
    lv = load(".agents/exam-blueprint/scripts/level_data.py")
    rows = json.loads(path.read_text(encoding="utf-8")).get("history", [])
    for row in rows:
        tid = str(row.get("test_id"))
        if ORIGIN.is_imported(tid):
            continue
        surfaces = row.get("surfaces", {})
        themes = row.get("themes")
        if not themes:
            warn(f"{tid}: records themes for its surfaces", False,
                 "no `themes` map — the four theme rules cannot be checked on "
                 "this paper (exam-blueprint §'logs/topics.json')")
            continue

        bad = sorted({v for v in themes.values() if v not in lv.THEMES})
        check(f"{tid}: themes come from the closed THEMES vocabulary", not bad,
              f"off-list: {bad} — pick the nearest value or say the surface "
              f"does not belong; never widen the list (exam-blueprint)")

        reading = [k for k in surfaces if READING_SURFACE.match(k)]
        missing = sorted(k for k in reading if k not in themes)
        check(f"{tid}: every 読解 surface carries a theme", not missing,
              f"untagged: {missing} — the cloze and every web seed inherit a "
              f"theme too; an untagged surface is uncounted, not exempt")

        by_theme: dict[str, set[str]] = {}
        for k in reading:
            if k in themes:
                by_theme.setdefault(themes[k], set()).add(surface_group(k))
        dupes = {t: sorted(g) for t, g in by_theme.items() if len(g) > 1}
        check(f"{tid}: no theme on two 読解 surfaces", not dupes,
              "; ".join(f"{t} x{len(g)} {g}" for t, g in dupes.items())
              + " — all thirteen 読解 surfaces take different themes "
                "(exam-blueprint rule 3). 19 themes carry reading entries "
                "against 13 surfaces, so a repeat is a re-angle or a re-draw, "
                "never a pool limit")

        head, m5 = _headline_parts(themes)
        clash = sorted(head & m5)
        check(f"{tid}: headline surfaces take five different themes",
              not clash,
              f"聴解問題5 shares {clash} with a 読解 headline surface — the five "
              f"headline surfaces (問題9/12/13/14/聴解問題5) are the paper's "
              f"spine and must not double up (exam-blueprint rule 1)")


# Cross-test rule 4 (exam-blueprint §"The four theme rules"): zero
# headline-theme repeat against the immediately-previous generated paper, and
# at most ONE repeat against the paper two back. This recurred once already
# (20260811_1) and again at 20260813_2 (qa-report-20260813_2.md F-THEME2BACK)
# because no automated check ever compared the 5-surface headline SET across a
# pair of tests — check_topics_themes() above only checks the clash WITHIN one
# test's own five surfaces (rule 1), never against another test (rule 4).
def check_theme_repeat_cross_test():
    print("\ncross-test headline theme repeat (rule 4)")
    path = ROOT / "logs" / "topics.json"
    if not path.is_file():
        return skip("cross-test headline theme repeat (rule 4)",
                     "no logs/topics.json on disk")
    rows = json.loads(path.read_text(encoding="utf-8")).get("history", [])
    history = [r for r in rows if not ORIGIN.is_imported(str(r.get("test_id")))]

    for prev, cur in zip(history, history[1:]):
        pid, cid = str(prev.get("test_id")), str(cur.get("test_id"))
        pthemes, cthemes = prev.get("themes"), cur.get("themes")
        if not pthemes or not cthemes:
            continue  # check_topics_themes() already WARNs the missing map
        overlap = sorted(headline_theme_set(pthemes) & headline_theme_set(cthemes))
        warn(f"{cid}: no headline theme repeats {pid}'s (immediately previous, rule 4)",
             not overlap,
             f"{overlap} shared with {pid} — exam-blueprint 'The four theme "
             f"rules' rule 4 allows ZERO headline-theme repeat against the "
             f"immediately-previous paper; re-draw one of the two surfaces "
             f"carrying the shared theme")

    for back2, cur in zip(history, history[2:]):
        bid, cid = str(back2.get("test_id")), str(cur.get("test_id"))
        bthemes, cthemes = back2.get("themes"), cur.get("themes")
        if not bthemes or not cthemes:
            continue
        overlap = sorted(headline_theme_set(bthemes) & headline_theme_set(cthemes))
        warn(f"{cid}: at most one headline theme repeats {bid}'s (two papers back, rule 4)",
             len(overlap) <= 1,
             f"{overlap} shared with {bid} — exam-blueprint rule 4 allows at "
             f"most ONE headline-theme repeat against the paper two back, not "
             f"{len(overlap)}; re-draw one of the repeated headline surfaces "
             f"(this exact miss recurred at 20260813_2 against 20260812_2 — "
             f"問題12=食, 問題14=住まい — after the same failure mode at "
             f"20260811_1; qa-report-20260813_2.md F-THEME2BACK)")


def check_dokkai_lengths(name: str, body: str, bi):
    """読解 passages must reach the official length band (G8).

    The bands were documented in three prose places and gated in none, so an
    author could not verify one without measuring and nobody did: multiple
    generated papers have shipped a short 問題11 and a short 問題14.
    """
    short, thin = [], []
    for n, floor in DOKKAI_FLOOR.items():
        sec = dokkai_section(body, n)
        if not sec:
            continue
        got = jp_char_count(passage_prose(sec, bi))
        if got < floor:
            short.append(f"問題{n}({got}<{floor})")
        if n in DOKKAI_PASSAGE_FLOOR:
            for i, sc in enumerate(passage_scopes(sec, n), 1):
                got_p = jp_char_count(passage_prose(sc, bi))
                if got_p < DOKKAI_PASSAGE_FLOOR[n]:
                    thin.append(f"問題{n}({i}):{got_p}<{DOKKAI_PASSAGE_FLOOR[n]}")
    check(f"{name}: 読解 sections reach the official length floor "
          f"{DOKKAI_FLOOR}", not short,
          "; ".join(short) + " — lengthen the passage prose, not the stems. "
          "The floors sit under the observed minimum of the 7 current-era "
          "sittings; author to the MEDIAN 1225/2556/551/904/604, not to the "
          "floor (official_calibration §2)")
    check(f"{name}: every 問題10/11 passage reaches {DOKKAI_PASSAGE_FLOOR}", not thin,
          "; ".join(thin) + " — official current-era per-passage minima are "
          "157 (問題10) and 507 (問題11) JP chars; medians 241 and 655 "
          "(official_calibration §2)")


NOTE_CHUU = re.compile(r"（中略）")


def check_chuuryaku(name: str, body: str):
    """（中略） has to cut a passage, not float under the instruction (G18).

    Generated papers have carried a bare `（中略）` line directly beneath the
    問題11 instruction, attached to no passage — and that stray marker is
    exactly what made the old `"中略" in gt` substring WARN pass.
    """
    stray, inside = [], 0
    for n in (11, 12, 13):
        sec = dokkai_section(body, n)
        if not sec:
            continue
        whole = len(NOTE_CHUU.findall(sec))
        within = sum(len(NOTE_CHUU.findall(re.sub(r"^##\s*問題\d+[^\n]*\n", "", sc)))
                     for sc in passage_scopes(sec, n))
        inside += within
        if whole > within:
            stray.append(f"問題{n}({whole - within} outside any passage)")
    check(f"{name}: every （中略） sits inside a 問題11–13 passage", not stray,
          "; ".join(stray) + " — a marker under the instruction line cuts "
          "nothing; move it into the passage (question-authoring)")
    check(f"{name}: 読解 cuts at least one passage with （中略） ({inside} in-passage)",
          inside >= 1,
          "official 中文/長文 cut with （中略）; generated tests shipped none")


def check_note_pairing(name: str, body: str):
    """（注N） markers and definitions pair 1-to-1 per passage (G2c).

    An orphan either way is an automatic QA fail and both have shipped: a
    paper has defined 格段/精神論/屋上緑化 for passages that no longer contain
    them, and papers have printed a 注5 marker in 問題13 with only four
    definitions.
    """
    bad = []
    for n in (9, 10, 11, 12, 13, 14):
        sec = dokkai_section(body, n)
        if not sec:
            continue
        for i, sc in enumerate(passage_scopes(sec, n), 1):
            marks, defs = set(), set()
            for ln in sc.splitlines():
                d = NOTE_DEF.match(ln)
                if d:
                    defs.add(d.group(1) or "1")
                else:
                    marks |= {m.group(1) or "1" for m in NOTE_MARK.finditer(ln)}
            if marks != defs:
                unmarked = sorted(defs - marks)
                undefined = sorted(marks - defs)
                bad.append(f"問題{n}({i}): "
                           + (f"defined but never marked 注{unmarked} " if unmarked else "")
                           + (f"marked but never defined 注{undefined}" if undefined else ""))
    check(f"{name}: （注N） markers and definitions pair 1-to-1 per passage", not bad,
          "; ".join(bad).strip() + " — a note the passage never marks (or a "
          "marker with no note) is an automatic fail (exam-qa-review)")



def pool_entry_text(entry) -> str:
    """The label of a pools.json entry, whichever shape it is on disk.

    `reading_topics` and `listening_scenarios` are the two categories whose
    entries are OBJECTS — `{"topic": …, "theme": …}` /
    `{"scenario": …, "theme": …}` — under the closed `THEMES` vocabulary that
    `exam-blueprint` owns; every other category is a bare string. Anything
    in this file that touches a pool must go through here, or it will start
    comparing dicts the day a category grows a tag.
    """
    if isinstance(entry, dict):
        for k in ("topic", "scenario", "item"):
            if entry.get(k):
                return str(entry[k])
        return ""
    return str(entry)


# R2. 問題1 targets: spec ↔ pool ↔ paper.
#
# The paper↔spec half is check_spec_target_items() (the 問題1 section must
# actually print what the spec drew). The spec↔pool half was checked NOWHERE,
# and that is the half that decides whether the drawn item is *valid*: a paper
# shipped 領(えり), 線(すじ) and 爆(は.ぜる) — printed kanji that do not have the
# keyed reading — and a pool audit removed 103 such entries.
# Anchoring the paper on the audited pool closes the class for good.
#
# NOT anchored on `openjlpt/kanji-n*.json`: that file is KANJIDIC-derived and
# lists 表外 readings (`領: ['えり']`, `線: ['すじ']` are IN it), so a
# (kanji, reading) check built on it passes the exact defects it targets.
# exam-blueprint says this in as many words — the pool is the authority.
KANJI_READING_ENTRY = re.compile(r"^(?P<word>[^（()）]+)[（(](?P<yomi>[^）)]+)[）)]$")
KANA_YOMI = re.compile(r"^[ぁ-ゖゝゞー]+$")
HAS_KANJI = re.compile(r"[一-鿿]")


def check_pool_kanji_reading_shape():
    """pools.json `kanji_reading` entries must be printable words (G-R2).

    Rule 1 of exam-blueprint's 「kanji_reading validity rule」: the entry
    reads `語(よみ)`, `語` carries at least one kanji, and `よみ` is hiragana
    with no `.` and no katakana. A dot (`爆(は.ぜる)`) is a raw KANJIDIC kunyomi
    — a single kanji with its okurigana detached, which cannot be underlined as
    a word; katakana (`療(リョウ)`) is a raw on-reading dump, a bound morpheme.
    Both shipped, both are undrawable, and this check is what stops a future
    hand-added entry (pool growth is manual now that `expand_pools.py` and its
    openjlpt source are deleted — see exam-blueprint/SKILL.md) from
    reintroducing the same shape.
    """
    print("\npools.json kanji_reading entries are printable 語(よみ) words")
    pools_path = AGENTS / "exam-blueprint" / "references" / "pools.json"
    if not pools_path.is_file():
        return skip("pools.json kanji_reading entry shape", "no pools.json")
    pools = json.loads(pools_path.read_text(encoding="utf-8"))
    entries = [pool_entry_text(e) for e in pools.get("kanji_reading", [])]
    bad = []
    for e in entries:
        m = KANJI_READING_ENTRY.match(e)
        if not m:
            bad.append(f"{e} (not `語(よみ)`)")
        elif not HAS_KANJI.search(m.group("word")):
            bad.append(f"{e} (no kanji in the word)")
        elif "." in m.group("yomi"):
            bad.append(f"{e} (raw KANJIDIC kunyomi — okurigana detached)")
        elif not KANA_YOMI.match(m.group("yomi")):
            bad.append(f"{e} (reading is not hiragana)")
    check(f"pools.json kanji_reading entries are shaped 語(よみ) "
          f"({len(entries)} entries)", not bad,
          "; ".join(bad[:6]) + " — a dotted kunyomi or a katakana on-reading is "
          "not a printable word; delete the entry (exam-blueprint "
          "'The kanji_reading validity rule')")


def check_spec_pool_kanji_reading(d, spec: dict):
    """Every 問題1 target the spec drew must still be a pool entry (R2)."""
    pools_path = AGENTS / "exam-blueprint" / "references" / "pools.json"
    if not pools_path.is_file():
        return skip(f"{d.name}: 問題1 targets come from pools.json", "no pools.json")
    pool = {pool_entry_text(e) for e in
            json.loads(pools_path.read_text(encoding="utf-8")).get("kanji_reading", [])}
    drawn, orphan = 0, []
    for entry in spec.get("items", {}).get("kanji_reading", []):
        # An adjunct row comes from logs/adjunct_staging.json, not the pool.
        if isinstance(entry, dict) and entry.get("origin") == "adjunct":
            continue
        label = pool_entry_text(entry)
        if not label:
            continue
        drawn += 1
        if label not in pool:
            orphan.append(label)
    check(f"{d.name}: 問題1 targets are pools.json kanji_reading entries "
          f"({drawn} drawn)", not orphan,
          f"not in the pool: {orphan} — either the sampler did not draw them "
          f"(a hand-edited spec) or the 2026-08-06 audit removed them as "
          f"undrawable; re-sample rather than authoring an off-pool target "
          f"(exam-blueprint)")


def check_note_band(name: str, gt: str):
    """（注N） definitions must not be circular (G2a).

    2026-08-11: the above-band half of this check (a term glossed by （注N）
    that a vendored N2 vocabulary file also lists as standard N2) was retired
    with openjlpt — there is no remaining grep-able word/level index to check
    it against (Shinkanzen/Soumatome are scanned PDFs, no text layer), and the
    repo has moved off openjlpt as an authority by design (exam-blueprint
    SKILL.md). Catching an above-band gloss is now on the author/QA reading
    against Shinkanzen/Soumatome and the official archive, same as every
    other 問題1–6 band judgment call question-authoring already asks for.

    What remains machinable without any corpus: a definition assembled from
    the term's own kanji (洗髪：髪の毛を洗うこと) teaches nothing, regardless of
    what inventory the term is in.

    This is a per-character substring heuristic, not a semantic one — it also
    fires on a compound term whose definition legitimately reuses one of its
    own characters while adding real new content (20260817_1 QA G6: 量子ビット
    glossed via 量子コンピュータ, 顧客ロイヤルティ glossed via 顧客 as its own
    necessary grammatical subject — both hand-judged non-circular, since each
    definition supplies a predicate/mechanism the term's own kanji do not).
    Treat every hit here as READ-BOTH-AND-DECIDE, not an automatic reword: true
    circularity is "the definition's only content is the headword's own
    kanji restated" (needs 調整 defining 調整), not "shares a character."
    """
    self_ref = []
    for ln in gt.splitlines():
        m = NOTE_DEF.match(ln)
        if not m:
            continue
        term, defn = m.group(2).strip(), m.group(3).strip()
        kanji = [c for c in term if "一" <= c <= "鿿"]
        if len(kanji) >= 2 and all(c in defn for c in kanji):
            self_ref.append(f"{term}：{defn[:12]}…")
    warn(f"{name}: （注N） definitions introduce words the term does not contain",
         not self_ref,
         f"candidates (read each, do not reword on sight): {self_ref} — flag "
         f"only if the definition's sole content is the headword's own kanji "
         f"restated with no added predicate/mechanism (question-authoring)")


def check_note_band_reuse(name: str, gt: str):
    """A （注N） headword must never also be tested as ordinary vocabulary
    elsewhere in this SAME paper's 問題1–6 (items 1–30) — a same-paper
    self-contradiction the paper proves against itself, not a judgment call.

    Until 2026-08-17 this rule (question-authoring/references/dokkai.md
    §'（注N） glosses') existed only as author-honor-system prose, and it kept
    shipping anyway: `20260811_1` glossed 抑える in 読解 while it was
    `問題2` item 8's own key (仰える/迎える/抑える/押える); `20260813_1` glossed
    負担 in 読解 while `問題4` item 11's own stem used it unglossed
    ("住民の負担を軽減する"). Both prove the term is ordinary, already-tested
    N2 vocabulary — the note's own implicit claim that it needs explaining is
    falsified by the paper itself. This check is a plain substring search
    against 問題1–6's own stems and options, no wordlist required.
    """
    m7 = re.search(r"^##\s*問題7\b", gt, re.M)
    p16_text = gt[: m7.start()] if m7 else ""
    hits = []
    for ln in gt.splitlines():
        m = NOTE_DEF.match(ln)
        if not m:
            continue
        term = m.group(2).strip()
        if len(term) >= 2 and term in p16_text:
            hits.append(term)
    check(f"{name}: no （注N） headword is reused as plain vocabulary in 問題1-6",
          not sorted(set(hits)),
          f"{sorted(set(hits))} — glossed in 読解 but ALSO appears as a "
          f"stem/option word in this same paper's 問題1-6, which proves it is "
          f"ordinary N2 vocabulary and must not be glossed "
          f"(question-authoring/references/dokkai.md §'（注N） glosses')")


# 問題11. The four banned pure-retrieval shapes appear ZERO times across the
# last 15 sittings — not in 問題11 and not in 問題10/12/13/14 either
# (official_calibration §4). Fully corroborated at n=15; this one stays a FAIL.
P11_BANNED_STEM = re.compile(r"(?:本文|文章|この文章)で(?:述べられて|説明されて)|として正しいもの|主な目的は|(?:内容|説明)と合っている")
# R14 — THE PER-PASSAGE PAIRING RULE IS FICTION. DO NOT RESTORE IT.
#
# Two stricter versions of this check have now been written and both were
# wrong, in the same way, for the same reason: they were derived from July 2025
# alone. Measured over the 28 current-era 問題11 pairs (7 sittings × 4 passages,
# official_calibration §4):
#
#     13 pairs one-of-each  |  13 pairs two-事実把握  |  2 pairs two-考え
#
# July 2025 is the ONLY sitting in the whole 31-paper archive where all four
# pairs are one-of-each. So:
#   * "every pair is exactly one 事実把握 + one 考え/主張" would fail 6 of the 7
#     current official papers;
#   * "every PASSAGE asks a 考え/主張 question" (the version before it) would
#     fail the same 6 — 13 of 28 official pairs have no 考え/主張 stem at all.
# A check an official paper fails is a wrong check, not a finding.
#
# What actually holds at n=7, and is all this may assert:
#   * EVERY paper carries ≥1 考え/主張 stem somewhere in 問題11's eight — the
#     observed range is 1–4 (12/2023 and 12/2024 ship exactly 1). Zero is the
#     only defect the archive supports. → FAIL.
#   * 事実把握 comes first in 26 of 28 pairs, and the 2 exceptions are the two
#     two-考え pairs, so a pair that opens 考え and closes 事実 occurs ZERO
#     times. → WARN (n=28 with no counter-example, but ordering is a style
#     regularity, not an answerability defect).
#   * 「筆者」 is NOT required: 10 of 56 current-era stems (18%) omit it, and 37
#     of 125 (30%) over 15 sittings. Those are span-anchored instead, which the
#     classifier below already reads as 事実把握. Never gate on 筆者 alone.
#
# The classifier itself is kept: the SPAN ANCHOR is tested first, and that
# order is load-bearing — 「売れた理由とあるが、筆者はなぜ売れたと考えているか」 is
# 事実把握 even though it contains 考えて, because it is anchored on a span.
# Enumerating 事実把握 shapes instead does not work: the list in
# question-authoring is examples, and a stem reading 「筆者は、…理由として何を
# 挙げているか」 is a sixth shape that such a list false-failed.
P11_SPAN_ANCHOR = re.compile(r"とあるが|によると|[①②③④⑤]")
P11_OPINION_STEM = re.compile(
    r"筆者の(?:考え|主張|評価|意見)|最も言いたい|最も伝えたい|言いたいことは"
    r"|筆者は[^。]*どう考えて|筆者が[^。]*大切に")
P11_AUTHOR = re.compile(r"筆者")


def classify_p11_stem(stem: str) -> str:
    """`事実把握` / `考え主張` / `未分類` — by SHAPE, per question-authoring."""
    if P11_SPAN_ANCHOR.search(stem):
        return "事実把握"
    if P11_OPINION_STEM.search(stem):
        return "考え主張"
    if P11_AUTHOR.search(stem):
        return "事実把握"
    return "未分類"


def check_mondai11_stems(name: str, body: str):
    sec = dokkai_section(body, 11)
    if not sec:
        return
    pairs = []
    for sc in passage_scopes(sec, 11):
        stems = [m.group(2).strip() for m in
                 re.finditer(r"^\s*\*\*(5[7-9]|6[0-4])\*\*\s*(.+)$", sc, re.M)]
        if stems:
            pairs.append(stems)
    banned = [s[:30] for p in pairs for s in p if P11_BANNED_STEM.search(s)]
    check(f"{name}: 問題11 uses no pure-retrieval stem shape", not banned,
          f"{banned} — 「本文で述べられて…」「…として正しいもの」「…の主な目的は」"
          f"「…の内容と合っている」 occur 0 times in 15 official sittings "
          f"(question-authoring 問題11; official_calibration §4)")

    kinds = [[classify_p11_stem(s) for s in p] for p in pairs]
    opinions = sum(k.count("考え主張") for k in kinds)
    shapes = "; ".join(f"({i}) {'+'.join(k)}" for i, k in enumerate(kinds, 1))
    check(f"{name}: 問題11 asks at least one 考え/主張 question across its "
          f"{sum(len(p) for p in pairs)} stems (got {opinions}; official 1–4)",
          opinions >= 1,
          f"{shapes} — every official paper carries 1–4 考え/主張 stems in "
          f"問題11, but they are NOT one per passage (13 of 28 official pairs "
          f"are two 事実把握). Add one 「筆者の考えに合うのはどれか」/「筆者が最も"
          f"言いたいことは何か」 somewhere in the four passages "
          f"(official_calibration §4)")
    inverted = [f"({i})" for i, k in enumerate(kinds, 1)
                if len(k) == 2 and k[0] == "考え主張" and k[1] == "事実把握"]
    warn(f"{name}: 問題11 pairs put the 事実把握 stem first", not inverted,
         f"inverted: {inverted} — official opens with the span-anchored stem in "
         f"26 of 28 pairs and never closes on one (the 2 exceptions are "
         f"two-考え pairs). A style regularity, not an answerability defect "
         f"(official_calibration §4)")


def check_mondai13_closer(name: str, body: str):
    """問題13's last item (69) is a 考え/主張 stem in 7 of 7 current papers.

    Offered as the replacement for the strictness R14 correctly loses: 問題11 is
    irregular (13/13/2 across 28 pairs), but 問題13 is not — items 67/68 are
    span- or 筆者によると-anchored and 69 closes on the whole passage, in every
    current-era sitting (official_calibration §4).

    WARN, not FAIL, on n=7 with a heuristic classifier: 7/7 means a FAIL would
    fail no official paper *in the sample*, but a 3-item 大問 measured on seven
    papers is thin evidence for a hard gate, and the classifier reads shapes
    rather than intent. Promote it if a later measurement widens the sample.
    """
    sec = dokkai_section(body, 13)
    if not sec:
        return
    m = re.search(r"^\s*\*\*69\*\*\s*(.+)$", sec, re.M)
    if not m:
        return
    kind = classify_p11_stem(m.group(1))
    warn(f"{name}: 問題13 closes on a 考え/主張 question (69 is {kind})",
         kind == "考え主張",
         f"「{m.group(1)[:34]}」 — official 長文 ends on 「筆者が最も言いたいこと"
         f"は何か」/「筆者の考えに合うのはどれか」 in 7 of 7 current sittings, "
         f"with 67/68 carrying the anchored retrieval "
         f"(official_calibration §4)")


# G4. A quotable flyer span has to CARRY A CONDITION. The first version of this
# check searched the whole flattened flyer, so a 【…】 block title or an ■ section
# header satisfied "two distinct 「…」 spans present in the flyer" while
# constraining nothing: tests/3's item 70 quotes one real 区分B row plus
# 「回収対象と出し方」, which is the header above it, and reads green as a
# two-constraint item while being a single-constraint lookup.
#
# The condition-bearing rows are the ones a candidate has to cross-reference:
# table rows, `・`/`-`/`*` bullets, `※` footnotes, numbered rules and 区分A/B-style
# labelled rows. Headers are the opposite of a constraint — they name where the
# conditions live. Measured on tests/1 and tests/2, whose 問題14 解説 quote table
# cells (「18歳以上・初心者」「10月15日（火）19:00〜20:30」) and bullet rules
# (「料金は9月30日までに銀行振込でお支払いください」), both still ground 2+ spans.
FLYER_HEADER = re.compile(r"^\s*(?:#{1,6}\s|■|□|◆|▼|【[^】]*】\s*$|\*\*[^*]+\*\*\s*$)")
FLYER_CONDITION = re.compile(r"^\s*(?:\||[・･\-*＊]|※|\(?\d+[.．、)）]|"
                             r"区分\s*[A-Za-zＡ-Ｚａ-ｚ])")


def flyer_condition_text(sec: str, bi) -> str:
    """The 問題14 flyer's condition-bearing rows only — no titles, no headers."""
    rows = []
    for ln in passage_prose(sec, bi).splitlines():
        stripped = ln.strip()
        if not stripped or set(stripped) <= set("|-: `"):
            continue
        if FLYER_HEADER.match(ln) or not FLYER_CONDITION.match(ln):
            continue
        rows.append(stripped)
    return "\n".join(rows)


def check_mondai14_quotes(name: str, body: str, key_dokkai: str, bi):
    """70 and 71 must each combine TWO flyer cells, and the 解説 must prove it (G7).

    Generated papers have written 71 as 「このお知らせの内容と合っているものはどれか」,
    which collapses to a one-cell lookup. One quote in the 解説 means one
    constraint, so the artifact is the check.
    """
    # The flyer's conditions only — not the stems, the printed options, or the
    # section headers, or a 解説 that quotes its own option (or the title of the
    # block its one condition sits in) would count as grounded.
    sec = dokkai_section(body, 14)
    conditions = _flat(flyer_condition_text(sec, bi))
    if not conditions or not key_dokkai:
        return
    thin = []
    for hit in re.finditer(r"^\|\s*(70|71)\s*\|\s*[1-4]\s*\|(.*)\|", key_dokkai, re.M):
        spans = {_flat(s) for s in re.findall(r"「([^」]+)」", hit.group(2))}
        grounded = {s for s in spans if s and s in conditions}
        if len(grounded) < 2:
            thin.append(f"{hit.group(1)}({len(grounded)} of {len(spans)} quotes "
                        f"land on a condition-bearing flyer row)")
    check(f"{name}: 問題14 解説 quotes the two flyer cells its key combines",
          not thin,
          "; ".join(thin) + " — write 70 and 71 as person-scenarios failing "
          "exactly one condition and quote BOTH source cells. A 【…】 block "
          "title or an ■ section header is not a constraint and no longer "
          "counts: quote the table row, bullet, ※ footnote or 区分 row that "
          "actually decides the item (question-authoring 問題14)")


# 問題9 (G13). Four blanks, four categories — but the category of a blank was
# written down nowhere, so nobody could check it and every paper collided two.
P9_TAGS = {"論理接続", "文末モーダル", "内容推論", "慣用・形式名詞"}


# R16. 問題7 解説 cells enumerate the distractors as `1「…」・3「…」・4「…」`, and
# that numbering is the only place the explanation and the printed option list
# are tied together. A cell naming a string option N does not carry is either
# explaining a draft that no longer exists or renumbering the options in the
# reader's head — the same failure family as a mis-keyed 問題8 ★, and the
# existing quote WARN cannot see it because it only reads 読解/聴解 tables.
P7_OPTION_REF = re.compile(r"([1-4])\s*[「]([^」]+)[」]")


def check_mondai7_option_refs(name: str, key_bunpou: str,
                             opts: dict[int, list[str]]):
    bad = []
    for hit in re.finditer(r"^\|\s*(3[1-9]|4[0-2])\s*\|\s*[1-4]\s*\|(.*)\|",
                           key_bunpou, re.M):
        q, cell = int(hit.group(1)), hit.group(2)
        o = opts.get(q) or []
        for n, quoted in P7_OPTION_REF.findall(cell):
            n = int(n)
            if n > len(o):
                bad.append(f"{q}: cites option {n}, the item has {len(o)}")
                continue
            fq, fo = _flat(quoted), _flat(o[n - 1])
            # Containment, not equality: a cell legitimately abbreviates
            # 「待ち遠しいわけがない」 to 「わけがない」 (the tested tail). What is
            # forbidden is naming a string the option does not contain at all.
            if fq and fo and fq not in fo and fo not in fq:
                bad.append(f"{q}-{n}: 解説 says 「{quoted}」, option {n} is "
                           f"「{o[n - 1]}」")
    check(f"{name}: 問題7 解説 option numbers match the printed options",
          not bad, "; ".join(bad[:6]) + " — renumber the 解説 against the "
          "option row as printed, or the explanation defends a different item "
          "(question-authoring 'Name the reason each distractor is IMPOSSIBLE')")


def check_mondai9_tags(name: str, key_bunpou: str):
    tags: dict[int, str | None] = {}
    for q, expl in re.findall(r"\|\s*(4[89]|5[01])\s*\|\s*[1-4]\s*\|\s*([^|]+)\|",
                              key_bunpou):
        t = re.match(r"\s*\[([^\]]+)\]", expl)
        tags[int(q)] = t.group(1) if t else None
    present = [t for t in tags.values() if t]
    ok = (len(tags) == 4 and len(present) == 4 and set(present) <= P9_TAGS
          and len(set(present)) == 4 and present.count("内容推論") == 1)
    check(f"{name}: 問題9 解説 cells carry four distinct category tags "
          f"incl. one [内容推論]", ok,
          f"got {tags} — open each 問題9 解説 with one of "
          f"{sorted(P9_TAGS)}, all four distinct, exactly one [内容推論] "
          f"(question-authoring 問題9)")


# 問題9 options are grammar/phrase scale on every official current-era paper
# (112 options, max 14 JP chars). Generated papers repeatedly shipped a
# `[内容推論]` blank whose four choices were 読解-length thesis paraphrases
# (20–40 chars, 「〜ことにある」 mini-summaries) — bunpou.md now forbids that,
# and this gate enforces the archive ceiling with a 2-char headroom so a
# 14-char official item never false-positives.
P9_OPTION_MAX = 16


def check_mondai9_option_lengths(name: str, opts: dict[int, list[str]]):
    bad = []
    for q in (48, 49, 50, 51):
        for i, o in enumerate(opts.get(q) or [], 1):
            n = jp_char_count(o)
            if n > P9_OPTION_MAX:
                bad.append(f"{q}-{i}({n}「{o}」)")
    check(f"{name}: 問題9 options each ≤{P9_OPTION_MAX} JP chars "
          f"(official current-era max 14)",
          not bad,
          f"long={bad[:6]} — rewrite as short grammar/phrase forms; "
          f"[内容推論] does not authorize 読解-length paraphrases "
          f"(question-authoring/references/bunpou.md 問題9)")


# 読解 keys (G16). A key far longer than its three distractors is findable by
# string length alone: a paper has shipped three in a row (67/68/69 — 94/107/63 JP
# chars against 31–36 means) and another shipped one (66 — 55 vs 31). Measured
# silent on other generated papers and the July 2025 official paper, so the
# length signal alone is safe.
#
# The verbatim-lift test is reported, not required: with the haystack restricted
# to PASSAGE prose (it has to be — the options are printed in the same file, so
# searching the whole section makes "verbatim" vacuously true) three keys from
# one paper are verbatim lifts and a 66 from another is a 統合理解 meta-statement
# (「Aは…とし、Bは…と述べている」) that appears in no passage. Both are the same
# defect for the candidate: the key is identifiable without reading.
#
# CORROBORATED by the archive and unchanged: over 138 keyed 読解 options in the
# current era the longest official key is 61 JP chars and the highest key/mean
# ratio is 1.55, so ZERO official items trip the pair (official_calibration §9).
# The pair is what must stay — neither half alone is safe, because 29% of
# official keys ARE the longest of their four options. Nothing in this gate
# assumes otherwise, and nothing should: `question-authoring`'s 「keep all four
# options within ±40% of each other」 is a target, not an invariant — 95% of
# official items sit at max/min ≤1.8 but 12/2025-66 reaches 2.10.
LONG_KEY_MIN = 50
LONG_KEY_RATIO = 1.7


def check_verbatim_keys(name: str, body: str, keys: dict[int, int],
                        opts: dict[int, list[str]], bi):
    passages = "\n".join(passage_prose(dokkai_section(body, n), bi)
                         for n in range(10, 15))
    flat = _flat(re.sub(r"（注\d+）|\(注\d+\)", "", passages))
    hits = []
    for q in range(52, 72):
        a, o = keys.get(q), opts.get(q) or []
        if a is None or len(o) != 4 or not 1 <= a <= 4:
            continue
        keyed_opt = o[a - 1]
        kl = jp_char_count(keyed_opt)
        others = [jp_char_count(x) for i, x in enumerate(o) if i != a - 1]
        mean = sum(others) / len(others) if others else 0.0

        flat_opt = _flat(keyed_opt).rstrip("。")
        lcs_len = 0
        if flat_opt and flat:
            match = SequenceMatcher(None, flat_opt, flat).find_longest_match(0, len(flat_opt), 0, len(flat))
            lcs_len = match.size

        is_long_key = (kl >= LONG_KEY_MIN and mean > 0 and kl >= LONG_KEY_RATIO * mean)
        # For items 52–69 (問題10–13), key must be genuinely paraphrased:
        # LCS >= 15 chars and >= 50% of option, or LCS >= 20 chars
        is_verbatim_lift = (q not in (70, 71) and ((lcs_len >= 15 and lcs_len >= 0.50 * len(flat_opt)) or lcs_len >= 20))
        # Short keys must not be pure verbatim lifts:
        is_short_pure_lift = (q not in (70, 71) and flat_opt
                               and lcs_len >= 0.85 * len(flat_opt))

        if is_long_key or is_verbatim_lift or is_short_pure_lift:
            reason = []
            if is_long_key:
                reason.append(f"{kl} chars vs {mean:.0f} mean")
            if is_verbatim_lift:
                reason.append(f"LCS={lcs_len} chars ({lcs_len/len(flat_opt):.0%}) in passage")
            if is_short_pure_lift and not is_verbatim_lift:
                reason.append(f"short key is {lcs_len/len(flat_opt):.0%} verbatim "
                              f"({lcs_len} of {len(flat_opt)} chars) — must be paraphrased")
            hits.append(f"{q}({', '.join(reason)})")

    check(f"{name}: no 読解 key is far longer than its distractors or a verbatim lift", not hits,
          "; ".join(hits) + f" — paraphrase the key to ~25–40 chars (official "
          f"keys top out at 61) and keep the four options close in length; a "
          f"key MAY be the longest (29% of official ones are), it may not be "
          f"long AND {LONG_KEY_RATIO}× the others (official max ratio 1.55). "
          f"Flagged at ≥{LONG_KEY_MIN} JP chars and ≥{LONG_KEY_RATIO}× mean, "
          f"LCS ≥15 chars and ≥50% of key, LCS ≥20 chars, or "
          f"LCS ≥85% of key (question-authoring 問題10–14; "
          f"official_calibration §9)")


# A per-item length/verbatim threshold set at the official 1.8-ratio band
# (check_verbatim_keys, LONG_KEY_RATIO) cannot see a DISTRIBUTIONAL habit:
# measured over 200 読解 items across ten generated papers (2026-08-17 audit),
# the key was the longest of the four options 73.5% of the time (58.5%
# strictly longer than all three distractors) against an official baseline of
# 29% (official_calibration §9) — a test-taker who always guesses the longest
# option would score ~74% without reading anything. No single item in that
# measurement was egregious enough to trip LONG_KEY_RATIO; the bias only
# showed up averaged across a whole paper, and recurred in every one of the
# ten papers (60-90% each) despite the softer per-item gate already existing.
# Fix (2026-08-17, this repo's own house policy — stricter than the official
# archive on this one axis, on purpose): a hard per-item cap at max/min <=1.3,
# FAIL not WARN. See check_dokkai_option_length_balance() and
# question-authoring/references/dokkai.md §'読解 keys — all four options
# within ~30% of each other, no exceptions'. This distributional check ensures
# that keys are unpredictable (~20–35% longest, matching official baseline).
DOKKAI_OPTION_RATIO_MAX = 1.3


def check_dokkai_option_length_balance(name: str, opts: dict[int, list[str]]):
    bad = []
    for q in range(52, 72):
        o = opts.get(q) or []
        if len(o) != 4:
            continue
        lens = [jp_char_count(x) for x in o]
        mx, mn = max(lens), min(lens)
        if mn == 0:
            continue
        ratio = mx / mn
        if ratio > DOKKAI_OPTION_RATIO_MAX:
            bad.append(f"{q}({lens}, {ratio:.2f}x)")
    check(f"{name}: every 読解 item's four options sit within "
          f"max/min <= {DOKKAI_OPTION_RATIO_MAX} JP chars of each other",
          not bad,
          f"{'; '.join(bad)} — lengthen the short distractors (a real, "
          f"passage-groundable clause, not filler) toward the key, or tighten "
          f"an over-long key; a length outlier is answerable by string length "
          f"alone without reading the passage (question-authoring/references/"
          f"dokkai.md §'読解 keys — all four options within ~30% of each "
          f"other, no exceptions')")


LONGEST_KEY_RATE_MAX = 0.35

# The (tied-)longest rate above is only half the measurement, and on its own it
# is gameable — which is what shipped. Re-measured 2026-08-18 (user report: "the
# longest key applies to both dokkai and choukai"), over 219 official 読解 items
# in 31 sittings parsed out of booklet.md:
#
#            official   the 11 papers on disk
#   strict     20 %          25 %
#   tied       30 %          30 %
#   key/mean   1.00          1.02
#
# The tied rates MATCH. The strict rates do not, and the reason is visible in the
# per-paper numbers: nine of the eleven papers sit at exactly 6/20 = 30 % tied,
# i.e. authored straight at the top of the "20–35 %" target this file's own
# message printed — but they reach it by making the key the UNIQUELY longest
# option, where official reaches the same 30 % partly through ties. Official is
# 20 % strict / 30 % tied; a paper at 30 % / 30 % has no ties at all.
#
# That distinction matters because max/min <=1.30 (above) deliberately clusters
# the four options into a narrow band: inside a narrow band, "the key is a
# hair longer than all three" is a reliable tiebreak, so 20260810_2 keying
# 37 vs [31,31,32], 41 vs [33,33,34], 37 vs [29,30,31], 38 vs [31,31,32],
# 36 vs [28,28,31] and 38 vs [30,30,31] is a readable pattern even though every
# single item is inside every per-item rule.
#
# So: FAIL above 35 % tied (unchanged) AND above 30 % strict, and author to the
# official 20 %. One paper at 30 % strict is unremarkable (binomial p~0.11 at
# n=20); six of eleven at 30 % is the paper-generator's habit, not chance.
DOKKAI_STRICT_LONGEST_MAX = 0.30
DOKKAI_LENGTH_GRANDFATHERED = {
    "20260807_1", "20260810_1", "20260810_2", "20260811_1",
    "20260812_1", "20260812_2", "20260813_1", "20260813_2",
    "20260814_1"
}


def check_dokkai_longest_key_rate(name: str, keys: dict[int, int],
                                   opts: dict[int, list[str]],
                                   origin: str = "generated"):
    n = n_longest = n_strict = 0
    strict_items: list[str] = []
    for q in range(52, 72):
        a, o = keys.get(q), opts.get(q) or []
        if a is None or len(o) != 4 or not 1 <= a <= 4:
            continue
        lens = [jp_char_count(x) for x in o]
        n += 1
        if lens[a - 1] == max(lens):
            n_longest += 1
            if lens.count(lens[a - 1]) == 1:
                n_strict += 1
                others = sorted(l for i, l in enumerate(lens, 1) if i != a)
                strict_items.append(f"{q}({lens[a - 1]} vs {others})")
    if n == 0:
        return skip(f"{name}: 読解 longest-key rate", "no keyed 読解 items")
    rate = n_longest / n
    strict_rate = n_strict / n
    strict_name = (f"{name}: 読解 key is not UNIQUELY the longest option "
                   f"({n_strict}/{n} = {strict_rate:.0%}, official 20%, target <= 30%)")
    strict_detail = (
        f"{n_strict} of {n} keyed 読解 items ({strict_rate:.0%}) key the option that is "
        f"longer than all three distractors: {', '.join(strict_items)} — official is "
        f"20% strict / 30% tied over 219 items in 31 sittings, ours 25% / 30%. "
        f"Reaching the tied target by making the key uniquely longest is the same "
        f"tell the tied rate was meant to stop, and max/min <=1.30 makes a "
        f"one-character lead readable. Lengthen the longest DISTRACTOR to meet or "
        f"pass the key (a passage-groundable clause, never filler), or let them tie "
        f"(question-authoring/references/dokkai.md §'読解 keys')")
    if origin != "generated":
        warn(strict_name, strict_rate <= 0.40, strict_detail)
    elif name in DOKKAI_LENGTH_GRANDFATHERED:
        warn(strict_name, strict_rate <= DOKKAI_STRICT_LONGEST_MAX,
             strict_detail + GRANDFATHER_NOTE)
    else:
        check(strict_name, strict_rate <= DOKKAI_STRICT_LONGEST_MAX, strict_detail)
    if origin == "generated":
        if name in DOKKAI_LENGTH_GRANDFATHERED:
            warn(f"{name}: correct answer is not predictably the longest option "
                 f"({n_longest}/{n} = {rate:.0%}, target <= 35%)",
                 rate <= LONGEST_KEY_RATE_MAX,
                 f"{n_longest} of {n} keyed 読解 items ({rate:.0%}) are the (tied-)"
                 f"longest of their four options [pre-rule paper — a FAIL for any id not grandfathered]")
        else:
            check(f"{name}: correct answer is not predictably the longest option "
                  f"({n_longest}/{n} = {rate:.0%}, target <= 35%)",
                  rate <= LONGEST_KEY_RATE_MAX,
                  f"{n_longest} of {n} keyed 読解 items ({rate:.0%}) are the (tied-)"
                  f"longest of their four options — official baseline is 29% "
                  f"(target 20%–35%, question-authoring/references/dokkai.md §'読解 keys — unpredictable option lengths'); "
                  f"lengthen distractors so that distractors are often longer than the key, "
                  f"and vary key length rank across items (rank 1: ~4-6, rank 2: ~4-6, rank 3: ~4-6, rank 4: ~4-6)")
    else:
        warn(f"{name}: correct answer is not habitually the longest option "
             f"({n_longest}/{n} = {rate:.0%})",
             rate <= 0.45,
             f"{n_longest} of {n} keyed 読解 items ({rate:.0%}) are longest")


# 解説 cells decide items, so a quote inside one is load-bearing. When it is
# invented, the item it justifies is usually broken too and nothing shows: a
# 聴解 key has quoted four lines of dialogue that were not in the script; a
# 問題2-6番 key has quoted a 「3日前」 rule the script gives as 1週間前, and
# named two speakers (アンさん・キムさん) the script never introduces.
QUOTE = re.compile(r"「([^」]{14,})」")
QUOTE_ELLIPSIS = re.compile(r"[…‥]+")


def _flat(s: str) -> str:
    """Strip what varies between a quote and its source but carries no meaning:
    whitespace, table/emphasis markup, and the quote marks themselves (a nested
    quote is 『』 inside 「」 but 「」 in the passage).

    The circled span markers ①〜⑦ go with the `**` they always sit beside: both
    are the marked-span apparatus, and where the marker falls inside a sentence
    is a typographic decision, not prose. Stripping only `**` made every 解説
    quote spanning a marker's position look missing the moment the span was
    re-cut (2026-08-18, the marked-span shrink pass across eight papers) —
    a quote whose text never changed reported as not found in the source.
    """
    return re.sub(r"[\s「」『』①-⑦]|\*\*|<[^>]+>", "", s)


# An in-word annotation: 「（注3）」, 「（タイムパフォーマンス）」, 「（約4割）」 —
# short, no sentence break, no nesting. Bounded at 24 chars and rejecting 。 so
# a parenthesised SENTENCE (which a 解説 would quote as part of the text) is
# left alone.
IN_WORD_ANNOTATION = re.compile(r"[（(][^（()）。]{1,24}[)）]")


def strip_annotations(s: str) -> str:
    return IN_WORD_ANNOTATION.sub("", s)


# R6. A 解説 that says a distractor is 言及なし / 未言及 / 今回の話ではない is
# the author stating, in writing, that the option has no basis in the passage
# or the script. question-authoring is explicit that this is not a distractor:
# 「An option with no quotable line is fabricated noise: delete it and take one
# from the script」 — every wrong 聴解 option must be MENTIONED then eliminated,
# and every 読解 distractor must be wrong for a nameable reason in the source.
# This is the sister of the 解説-quote WARN and the opposite kind of evidence:
# that check guesses whether a quote is real, this one reads an admission, so
# it FAILs. Generated papers have shipped ~20 ungrounded 聴解 options between them.
FABRICATED_ADMISSION = re.compile(r"言及なし|未言及|言及されていない|今回の話ではない")


def check_fabricated_distractors(name: str, key_section: str):
    hits = []
    for line in key_section.splitlines():
        if not FABRICATED_ADMISSION.search(line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        label = cells[0] if cells else line.strip()[:12]
        term = FABRICATED_ADMISSION.search(line).group()
        hits.append(f"{label}「{term}」")
    check(f"{name}: no 解説 declares a distractor unmentioned in the source",
          not hits,
          "; ".join(hits[:6]) + " — the 解説 admits the option has no basis in "
          "the passage/script, which makes it fabricated noise, not a "
          "distractor: replace it with a real statement from the source that "
          "is reassigned/superseded/denied (question-authoring "
          "'聴解 dialogues' and 'Distractor plausibility')")


# G1. A 聴解 問題1–3 解説 cell carries one grounding line per option, in the
# shape choukai-audio mandates — `N ✗「script line」→ 理由` — and marks
# the one that is right, either with a circle (`3 ○「…」`) or by tagging its own
# line （正解）. That annotation is the author writing the correct answer into
# the paper in a machine-readable place, so a cell whose （正解） sits on a
# different digit than the 正解 column is a MIS-KEY stated twice in one row.
#
# tests/3 問題1-1番 ships exactly that: the key column says 4, and the 解説 tags
# option 3 「発券機に行こう」→ 決定された行動（正解）. Nothing saw it —
# check_answer_positions proved only that a 4 sits where the spec wanted a 4
# (see its label), and the quote WARN found the quote in the script because the
# quote is real; it is the KEY that is wrong.
#
# Silent by construction where the convention is not used: a cell with no
# digit-plus-mark grounding lines (a paper's prose cells, every 問題4 cell) is
# skipped rather than demanded, so this can only ever fire on a contradiction
# the author already wrote down. The convention does NOT hold in
# 言語知識・読解 — zero ○/（正解） annotations across generated papers' 文字・語彙,
# 文法 and 読解 key tables, which state the key in prose (「…から3」) — so this
# check is 聴解-only until that changes.
# WENT SILENT, 2026-08-13: this check printed `ok … (0 annotated cells)` for the
# five most recent papers — i.e. the mis-key guard has been inert on every test
# since `20260811_1`, on two independent counts:
#   1. the 番号 column changed form. It shipped as `| 1 |` in the first three
#      papers and `| 1番 |` since, and the row filter was `cells[0].isdigit()`,
#      which rejects `1番`. Now normalized via CHOUKAI_ITEM_LABEL.
#   2. the 解説 convention drifted. Newer cells mark only the WRONG options
#      (`1 ✗「…」／2 ✗「…」`) and name the key in prose (`…ため、4が正解。`), so
#      `declared_correct_options` found no ○ and no （正解） and skipped the row
#      by design. PROSE_CORRECT now reads that form too.
# Both are the same lesson as the check's own docstring: a guard that is "silent
# by construction where the convention is not used" turns itself off the moment
# the convention drifts, and nothing reports that it stopped looking. The
# annotated-cell count in the label is the tell — a 0 there is a dead check, not
# a clean paper.
GROUNDING_MARK = re.compile(r"([1-4])\s*([✗×✕✖☓○◯〇])")
CORRECT_TAG = re.compile(r"[（(]正解[)）]")
PROSE_CORRECT = re.compile(r"(?:^|[。、])(?:正解は)?([1-4])\s*(?:番)?が正解")
CIRCLE_MARKS = "○◯〇"
# Both 番号 column forms in use: `1`/`1番`/`例`, plus 問題5's `2番-質問1`.
CHOUKAI_ITEM_LABEL = re.compile(r"^(例|\d+)(番)?(?:-質問[12])?$")


def declared_correct_options(cell: str) -> tuple[set[int], int]:
    """{option numbers the cell declares correct}, and how many it annotates.

    A grounding line runs from its own `N ✗`/`N ○` mark to the next one (or the
    end of the cell), which is the only split that works for both layouts in
    use: `<br>`-separated lines (tests/3) and lines run together inside one
    cell (tests/2, separated by 。 alone).
    """
    hits = list(GROUNDING_MARK.finditer(cell))
    declared: set[int] = set()
    for i, h in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(cell)
        if h.group(2) in CIRCLE_MARKS or CORRECT_TAG.search(cell[h.end():end]):
            declared.add(int(h.group(1)))
    prose = {int(p.group(1)) for p in PROSE_CORRECT.finditer(cell)}
    return declared | prose, len(hits) + len(prose)


def check_choukai_kaisetsu_keys(name: str, ct: str, bi):
    cut = bi.KEY_HEADING.search(ct)
    if not cut:
        return
    section, bad, annotated = None, [], 0
    for line in ct[cut.start():].splitlines():
        head = re.match(r"^#+\s*問題([1-5])", line)
        if head:
            section = int(head.group(1))
            continue
        if section not in (1, 2, 3) or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 3 or not CHOUKAI_ITEM_LABEL.match(cells[0]):
            continue
        keyed = re.fullmatch(r"\**\s*([1-4])\s*\**", cells[1])
        if not keyed:
            continue
        declared, _ = declared_correct_options(cells[2])
        if not declared:
            continue
        annotated += 1
        if declared != {int(keyed.group(1))}:
            label = cells[0] if not cells[0].isdigit() else f"{cells[0]}番"
            bad.append(f"問題{section}-{label}: 正解欄 {keyed.group(1)}, "
                       f"解説 marks {sorted(declared)} as （正解）")
    check(f"{name}: every 聴解 解説 marks the option the key column names "
          f"({annotated} annotated cells)", not bad,
          "; ".join(bad) + " — the paper states two different answers for one "
          "item. Re-solve it from 聴解スクリプト.txt and fix whichever is wrong; "
          "do NOT just renumber the 解説 (choukai-audio 'The keyed "
          "option must be quotable'). keys-match-answer_positions cannot see "
          "this: it proves slot agreement only")


def check_explanation_quotes(name: str, key_section: str, source: str):
    """A long 「…」 span in a key table should occur in the passage or script.

    Reported, not enforced: a 解説 may legitimately put its own wording in 「」,
    so this cannot be decided by matching alone. What it catches is the class
    of bug where it is NOT the explanation that is wrong — a 聴解 key has
    quoted four lines of dialogue that were nowhere in the script, and a
    問題4-10番 key has quoted an option 「本当ですか！ぜひお願いしたいです」 that the
    script never speaks. A quote nobody can find usually means the item was
    keyed against a draft that no longer exists.
    """
    # Strip inline （注N） markers from the source: a 解説 quotes the sentence
    # without them, so 「…大脳辺縁系に直接伝達される」 failed to match a passage
    # reading 「…大脳辺縁系（注3）に直接伝達される」. That produced five false
    # positives in one paper and buried the one real miss (問66's 「過去の情熱」
    # against the passage's 「当時の情熱」) among them.
    #
    # R15: （注N） is not the only parenthetical a quote drops. A passage
    # reading 「タイパ（タイムパフォーマンス）が」 does not match a 解説 quoting
    # 「タイパが」, and every in-word gloss — an acronym expansion, a reading, a
    # unit — reproduces that false positive. Strip ALL short in-word `（…）`
    # annotations, and strip them from BOTH sides: symmetric stripping cannot
    # break a match that already held (it only ever removes text both strings
    # carry), while stripping the source alone would newly break a 解説 that
    # quotes the parenthetical verbatim.
    src = _flat(strip_annotations(source))
    missing = []
    for q in QUOTE.findall(key_section):
        parts = [_flat(strip_annotations(p)) for p in QUOTE_ELLIPSIS.split(q)]
        if any(len(p) >= 8 and p not in src for p in parts):
            missing.append(q[:38] + ("…" if len(q) > 38 else ""))
    warn(f"{name}: 解説 quotes trace to the passage/script", not missing,
         f"not found in the source: {missing} — quote by copy-paste; if the "
         f"line really is not there, the ITEM is wrong, not the explanation")


# ------------------------------------------------- one subject, one surface
# R18. Two surfaces of one paper covering the same SUBJECT starves a 問題, and
# the exact-duplicate check in check_spec_blend only sees byte-equal topics. The
# fuzzy half is token overlap — but the first version of it compared EVERY
# ≥2-char kanji/katakana run of every surface, and that is unusable:
#
#   MEASURED 2026-08-06, sampling pools.json exactly as sample_items.py draws
#   (21 listening_scenarios + 12 reading_topics, 300 random draws):
#       272/300 draws collided on the scenarios alone, 286/300 with the reading
#       topics added — i.e. it FAILED 95% of legitimate draws.
#
# A gate that fails 95% of honest draws cannot be satisfied by re-drawing. It
# trains the operator to re-seed until the gate goes green, which selects the
# paper by gate-satisfaction instead of by quality — strictly worse than having
# no check. A run's six collisions were every one of them naming vocabulary,
# not subject: 確認, 説明, 注意, 会社.
#
# The cause is that a pool entry is NOT a subject string. `exam-blueprint`
# names the convention: a listening scenario is `場所:用件`
# (`{"scenario": "会社:会議の準備"}`), so the token before the colon is the
# SETTING and the token after it is drawn from a small errand vocabulary —
# 案内 ×14, 相談 ×10, 手続 ×8, 説明 ×6, 確認 ×5 across 240 entries. Two items
# set in a 会社, or two items where somebody 確認s something, are not one
# subject; official papers do both in every sitting.
#
# So the fix is not to scope by origin. Scoping `token_map` to
# `"origin": "web"` would clear that run (none of its six pairs is web×web), but
# both skills forbid it in as many words — `exam-blueprint` §"Topic themes":
# 「Scoping it by origin instead would exempt an offline all-pool paper from the
# theme rule entirely」, and `exam-blueprint` §"How to comply": 「Scope by
# surface, not by origin」. A pool-origin 問題13 beside a web-origin 問題9 on one
# subject is exactly the defect, and that run's own 注意 pair is web×pool.
#
# What IS decidable is DISTINCTIVENESS. Strip the setting prefix, drop the
# errand vocabulary, and fail only on a token the pool does not itself reuse:
#
#   MEASURED on the same 300 draws: 0/300 false positives — a pool×pool
#   collision on a token the pool uses once is impossible by construction, so
#   this tier fires only on a blended or hand-edited spec.
#   MEASURED against the five re-skin subjects this repo actually shipped:
#   デジタルデトックス (pool freq 0), 屋上緑化 (0), フードドライブ (0),
#   ハイブリッドワーク (0), 地域通貨 (1) — all five caught.
#
# WHAT THIS DELIBERATELY DOES NOT CATCH, so it is not "restored" later: the pool
# contains genuine near-duplicate entries (確定申告 ×2, 音声ガイド ×2, 定期券 ×2,
# 返却場所 ×2, 睡眠 ×4), and a draw hits one of those pairs ~26% of the time. A
# tier for them was measured at 77–152/300 depending on the token floor, i.e.
# noise a reader learns to scroll past, and it duplicates a layer that already
# exists: `sample_items.py`'s `check_domain_collision()` / `check_theme_spread()`
# warn on it after the draw, with `--reroll listening_scenarios` as the
# documented remedy. And the renamed subject (「屋上緑化」 vs
# 「グリーンパートナー制度」) shares zero tokens by construction —
# `exam-blueprint` §"The honest limit": 「Subject identity cannot be
# mechanized.」 The mandatory whole-paper topic table pass is the real rule; this
# is the floor under it.
#
# Tokenization matches `merge_seeds.content_tokens()` — kanji runs, katakana
# runs and latin words as SEPARATE maximal runs. One combined kanji+katakana
# class (what this check used to use) glues 「フードドライブ受付」 into a single
# token, so it does not match 「フードドライブの持ち込み条件」; that is why two of
# the five shipped defects above were missed before. Keep the two in sync.
SETTING_PREFIX = re.compile(r"^[^:：]{1,12}[:：]")
# The `用件` half of `場所:用件`, plus the generic abstractions essay-style
# reading topics are titled with. Every entry here is an errand, a process or a
# relation noun — never a subject noun, because dropping a subject noun is what
# would make this check vacuous.
ERRAND_TOKENS = {
    "案内", "相談", "手続", "説明", "確認", "見直", "準備", "調整", "手配",
    "依頼", "変更", "受付", "解説", "紹介", "予約", "見積", "注意", "注意事項",
    "申込", "問合", "連絡", "対応", "報告", "検討", "利用", "参加", "募集",
    "開催", "実施", "選択", "比較", "確保", "意義", "役割", "効用", "価値",
    "効果", "影響", "変化", "課題", "問題", "方法", "仕組", "評価", "関係",
    "時間", "仕上", "業者", "会議", "イベント", "セミナー", "講演会",
    "スケジュール", "サービス", "ルール", "マナー", "トラブル", "キャンセル",
}


def subject_tokens(text: str) -> set[str]:
    """The tokens of a surface string that name its SUBJECT.

    Setting prefix removed, errand vocabulary removed, hiragana excluded (it
    carries the grammar, not the subject). Runs are maximal and compared for
    equality, so 「地域通貨」 matches 「地域通貨」 and not 「地域猫」.
    """
    t = SETTING_PREFIX.sub("", str(text))
    toks = set(re.findall(r"[一-鿿]{2,}", t))
    toks |= set(re.findall(r"[ァ-ヶー]{2,}", t))
    toks |= {w.lower() for w in re.findall(r"[A-Za-z0-9]{2,}", t)
             if not w.isdigit()}
    return toks - ERRAND_TOKENS


_pool_subject_freq: collections.Counter | None = None


def pool_subject_freq() -> collections.Counter:
    """How many pool entries each subject token appears in (memoized).

    The distinctiveness ruler. A token the pool spells across several entries
    is the pool's own vocabulary; a token it uses at most once is a subject.
    """
    global _pool_subject_freq
    if _pool_subject_freq is not None:
        return _pool_subject_freq
    freq: collections.Counter = collections.Counter()
    pools_path = AGENTS / "exam-blueprint" / "references" / "pools.json"
    if pools_path.is_file():
        pools = json.loads(pools_path.read_text(encoding="utf-8"))
        for cat in ("listening_scenarios", "reading_topics"):
            for e in pools.get(cat, []):
                for tok in subject_tokens(pool_entry_text(e)):
                    freq[tok] += 1
    _pool_subject_freq = freq
    return freq


def check_surface_subjects(token_map: dict[str, list[str]]):
    name = "no two spec surfaces share a distinctive subject token"
    freq = pool_subject_freq()
    if not freq:
        # With no pool there is no distinctiveness ruler, and every token would
        # read as distinctive — which is the 95%-false-failure mode above.
        return skip(name, "no pools.json to measure token distinctiveness against")
    surfaces = [(s, subject_tokens(s)) for s in token_map]
    collisions = []
    for i in range(len(surfaces)):
        for j in range(i + 1, len(surfaces)):
            (s1, t1), (s2, t2) = surfaces[i], surfaces[j]
            rare = sorted(t for t in t1 & t2 if freq[t] <= 1)
            if rare:
                collisions.append(f"「{s1}」 x 「{s2}」 share {rare}")
    check(name, not collisions,
          "; ".join(collisions) + " — one subject, one surface: two 問題 on the "
          "same subject starve each other. Re-harvest the seed or "
          "`--reroll` the category; never re-seed until the gate goes green "
          "(exam-blueprint 'One topic, one surface')")


# Calibrated against every consecutive-pair max ratio on disk at write time:
# the confirmed defect (20260811_1↔20260812_1's two 引っ越し業者 scenarios)
# scored 0.833; the highest UNFLAGGED historical pair (20260810_1↔20260810_2's
# two 銀行:口座開設 scenarios) scored 0.778. subject_tokens() cannot see either
# — it filters common errand nouns like 業者/口座 as non-distinctive, and its
# kanji-run matching does not span a hiragana particle like 「との」, so a
# same-institution-same-errand pair phrased in free text (not the pool's own
# `場所:用件` shorthand) tokenizes to nothing shared even when a human reads
# them as the same scenario. Raw string similarity catches what token-based
# subject matching structurally cannot.
CROSS_TEST_SCENARIO_RATIO = 0.8


def check_cross_test_listening_subjects():
    """No 聴解1/2/3/5 errand repeats the IMMEDIATELY PREVIOUS test's (G-new).

    `check_topics_themes()`'s rule-4 comparison only covers the 5-surface
    headline set (問題9/12/13/14/聴解問題5); `check_surface_subjects()` only
    covers collisions WITHIN one spec. Neither compares the other 19 pool-drawn
    `listening_scenarios` (問題1/2/3) against the previous test's — 20260812_1
    shipped 聴解問題1-4番 (引っ越し業者, 見積もり) one test after 20260811_1's own
    聴解問題1-2番 (引っ越し業者, 見積もり) through a fully green gate
    (qa/qa-report-20260812_1.md F1) because that comparison had no owner.
    """
    print("\ncross-test 聴解1/2/3/5 subject repeat (previous test only)")
    history = [h for h in ledger_history() if str(h.get("test_id")) != "legacy"]
    for prev, cur in zip(history, history[1:]):
        pid, cid = str(prev.get("test_id")), str(cur.get("test_id"))
        prev_scen = [pool_entry_text(e) for e in prev.get("items", {}).get("listening_scenarios") or []]
        cur_scen = [pool_entry_text(e) for e in cur.get("items", {}).get("listening_scenarios") or []]
        if not prev_scen or not cur_scen:
            continue
        collisions = []
        for cs in cur_scen:
            for ps in prev_scen:
                r = SequenceMatcher(None, cs, ps).ratio()
                if r >= CROSS_TEST_SCENARIO_RATIO:
                    collisions.append(f"「{cs}」(this) x 「{ps}」({pid}) ratio={r:.2f}")
        check(f"{cid}: no 聴解1/2/3/5 errand repeats {pid}'s (immediately previous)",
              not collisions,
              "; ".join(collisions) + " — a listening scenario repeated one "
              "test apart is an automatic-fail cross-test topic repeat "
              "(exam-qa-review); re-author the surface onto a different "
              "institution/errand and record `origin: reauthored` + a note "
              "in test_spec.json and logs/ledger.json")


def check_spec_blend(spec: dict):
    """The blend contract the authoring step reads off tests/<id>/test_spec.json.

    Two invariants no other gate can see, both violated by a shipped spec:
    every surface needs a DISTINCT topic (a duplicate silently starves one
    問題, which then gets authored off-contract), and the pool side keeps >=40%
    of every blended surface (exam-blueprint 'Balanced blend'). merge_seeds.py compounds both when
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

    # Two surfaces of one paper on one SUBJECT starves a 問題 (jlpt-test-generation 'One topic, one surface',
    # exam-blueprint §"One topic, one surface"). The exact-duplicate check
    # above catches the easy half; this is the fuzzy half, and what makes it
    # decidable is DISTINCTIVENESS, not origin — see check_surface_subjects.
    token_map: dict[str, list[str]] = {}
    for field, key in (("reading_topics", "topic"), ("listening_scenarios", "scenario")):
        for r in spec.get("items", {}).get(field, []):
            t = r.get(key) if isinstance(r, dict) else r
            if t:
                token_map.setdefault(t, []).append(field)
    for field in ("info_retrieval_texture", "cloze_topic"):
        e = spec.get(field)
        if isinstance(e, dict):
            t = e.get("detail") or e.get("topic")
            if t:
                token_map.setdefault(t, []).append(field)

    check_surface_subjects(token_map)


def check_pool_infrastructure():
    print("\npool expansion / adjunct staging")
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


# Kanji↔kana spellings of the same grammar tail. `grammar_p7` shipped both
# 〜気味 and 〜ぎみだ and the sampler drew both into one paper, keying one grammar
# point twice — and 〜がち/〜がちだ the same way. No reading source in refs/ or
# references/ can bridge those automatically (Shinkanzen/Soumatome are scanned
# PDFs with no text layer, so there is no grep-able index to build one from).
# So this is a fold TABLE, not a boundary — extend it when a new pair appears,
# and prefer deleting one spelling from pools.json over teaching the gate to
# tolerate two. Longest key first, so 以上 folds before 上.
KANA_FOLD = {"気味": "ぎみ", "次第": "しだい", "以上": "いじょう", "一方": "いっぽう",
             "同時": "どうじ", "限り": "かぎり", "抜き": "ぬき", "反面": "はんめん",
             "通り": "とおり", "際": "さい", "末": "すえ", "上": "うえ"}


def pool_skeleton(entry: str) -> str:
    """`〜次第(で)` → `しだい`: what two pool entries in one category must differ by.

    Strips the 〜/～ placeholder and the parenthetical example gloss, folds the
    kanji spellings above to kana, and drops a trailing だ/です. All three steps
    are load-bearing: without the last two, `〜がち`/`〜がちだ` and
    `〜気味`/`〜ぎみだ` — the exact pairs that shipped a paper's double-keyed
    grammar point — compare as distinct entries.
    """
    e = re.sub(r"[（(][^）)]*[）)]", "", entry).replace("〜", "").replace("～", "").strip()
    for kanji, kana in sorted(KANA_FOLD.items(), key=lambda kv: -len(kv[0])):
        e = e.replace(kanji, kana)
    return re.sub(r"(だ|です)$", "", e)


def check_pool_grammar_band():
    """pools.json grammar entries must sit inside the N2 band and be distinct (G17).

    `grammar_p8` shipped `相対比較(〜ば〜ほど)` — `〜ば〜ほど` is TOO_EASY on
    exam-qa-review's level-band list AND on question-authoring's banned list.
    A paper keyed it at item 46 and the keyed-option check could not see it,
    because the option string reads 「触れるほど」. Checking the DATA closes the
    class permanently: the pool is what the sampler draws from.
    """
    print("\npools.json grammar entries ↔ level band")
    pools_path = AGENTS / "exam-blueprint" / "references" / "pools.json"
    band = load_level_band()
    if not pools_path.is_file() or not (band["TOO_HARD"] or band["TOO_EASY"]):
        return skip("pools.json grammar entries stay inside the N2 band",
                    "no pools.json or level_band_grammar.txt")
    pools = json.loads(pools_path.read_text(encoding="utf-8"))
    cats = [c for c in pools if "grammar" in c]
    out_of_band, dupes = [], []
    for cat in cats:
        for entry in pools[cat]:
            # The band list spells forms without the 〜 placeholder, so strip it
            # before matching: 相対比較(〜ば〜ほど) only reads as `ばほど` that way.
            probe = entry.replace("〜", "").replace("～", "")
            for ban in _level_band_hits(probe, band["TOO_HARD"], band["ALLOW"]):
                out_of_band.append(f"{cat}/{entry} (TOO_HARD: {ban})")
            for ban in _level_band_hits(probe, band["TOO_EASY"], band["ALLOW"]):
                out_of_band.append(f"{cat}/{entry} (TOO_EASY: {ban})")
        groups: dict[str, list[str]] = {}
        for entry in pools[cat]:
            groups.setdefault(pool_skeleton(entry), []).append(entry)
        dupes += [f"{cat}: {v}" for v in groups.values() if len(v) > 1]
    check(f"pools.json grammar entries stay inside the N2 band "
          f"({sum(len(pools[c]) for c in cats)} entries in {cats})",
          not out_of_band,
          "; ".join(out_of_band) + " — delete the entry; a banned form in the "
          "pool ships as a key sooner or later (exam-blueprint)")
    check("no grammar category lists one point under two spellings", not dupes,
          "; ".join(dupes) + " — keep one spelling per point, or the sampler "
          "draws both and the test keys it twice (exam-blueprint)")


def check_ledger_draw_counts(sample):
    """Every ledger entry must record exactly DRAW[cat] items (G11).

    Entries `2`, `4` and `4-removed` record 語形成 5 / 即時応答 12 /
    reading_topics 11 against today's DRAW of 3 / 11 / 12: items burning
    rotation cooldown for questions the papers never asked. A count that
    disagrees with DRAW is a ledger defect, not history.
    """
    led = ROOT / "logs" / "ledger.json"
    if not led.is_file():
        return skip("ledger draw counts match sample_items.DRAW", "no logs/ledger.json")
    off = []
    skipped_pre_stamp = 0
    for h in json.loads(led.read_text(encoding="utf-8")).get("history", []):
        tid = str(h.get("test_id"))
        if tid == "legacy":            # the pre-ledger backfill has no draw shape
            continue
        recorded_draw = h.get("draw")
        if recorded_draw:
            for cat, want in recorded_draw.items():
                got = len(h.get("items", {}).get(cat) or [])
                if got != want:
                    off.append(f"test {tid}/{cat}: {got} recorded, recorded draw says {want}")
        else:
            skipped_pre_stamp += 1
            continue

    if skipped_pre_stamp > 0:
        skip("pre-stamp ledger draw counts", f"{skipped_pre_stamp} entries have no recorded 'draw' dict")
    check("ledger draw counts match recorded draw dicts",
          not off,
          "; ".join(off) + " — ledger history entries must record their own draw shape")


def check_harvest_hygiene():
    """Two seeds from one document are one seed (G12).

    logs/seeds.json carries three seeds citing the identical env.go.jp PDF, and
    two of the three facts drawn from it are not in that document. merge_seeds.py
    now aborts on this; the gate keeps a stale bad harvest from sitting on disk.
    """
    seeds_path = ROOT / "logs" / "seeds.json"
    if not seeds_path.is_file():
        return skip("logs/seeds.json cites a distinct source per seed", "no seeds.json")
    seeds = json.loads(seeds_path.read_text(encoding="utf-8"))
    srcs = [s.get("source", "") for s in seeds if isinstance(s, dict)]
    dup = sorted({u for u in srcs if u and srcs.count(u) > 1})
    check(f"logs/seeds.json cites a distinct source per seed ({len(seeds)} seeds)",
          not dup,
          f"reused {len(dup)} URL(s): {dup} — two seeds from one document are "
          f"one seed; drop the weaker and re-harvest (exam-blueprint)")


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


def ledger_history() -> list[dict]:
    led = ROOT / "logs" / "ledger.json"
    if not led.is_file():
        return []
    return json.loads(led.read_text(encoding="utf-8")).get("history", [])


def generated_specs() -> list[tuple[Path, dict]]:
    """(dir, spec) for every GENERATED test that owns its own spec."""
    out: list[tuple[Path, dict]] = []
    tests_root = ROOT / "tests"
    if not tests_root.is_dir():
        return out
    for d in sorted(tests_root.glob("*")):
        if not d.is_dir() or ORIGIN.is_imported(d.name):
            continue
        p = d / "test_spec.json"
        if not p.is_file():
            continue
        spec = json.loads(p.read_text(encoding="utf-8"))
        if str(spec.get("test_id")) == d.name:
            out.append((d, spec))
    return out


# G9 (GATE-WRONG). check_ledger_spec_agreement() below enforces ledger == spec
# and neither side against the pool, so ALIGNING the two on a string the
# rotation matcher cannot resolve turns it green *while breaking rotation* —
# which is what a repair pass did to tests/2. Two shapes, both green today:
#
#   (a) an INFLECTED surface form. The pool entry is 「〜ずじまい」; the paper
#       realizes it as 「行かずじまい」; ledger and spec were both edited to say
#       「行かずじまい」. sample_items.recency_map() keys on the raw string and on
#       head(), neither of which normalizes the tilde, so 「〜ずじまい」 never
#       enters the recency map, is permanently un-cooled, and is redrawable one
#       test after it was asked (quick_response draws 11 of 196 ≈ 5.6%/draw).
#       All ~115 other bound-form entries kept their tilde: the convention was
#       inverted for exactly one item.
#   (b) an item in NO pool category and no adjunct staging row (tests/2 records
#       キャンセル and お疲れ様でした under paraphrase; the draw was テニスコート
#       and はじめまして). An off-pool item can never rotate, because no future
#       draw can hit it.
#
# The fix is to anchor BOTH files on the pool, which is the only string the
# sampler will ever compare against. Comparison is raw, then tilde-stripped,
# then head()-folded — the same three forms recency_map() and head() can see.
def _pool_forms(text: str) -> set[str]:
    t = str(text).strip()
    bare = t.lstrip("〜～")
    return {t, bare, t.split("(")[0].split("（")[0].strip(),
            bare.split("(")[0].split("（")[0].strip()} - {""}


def check_draw_provenance():
    """Every recorded draw must name a POOL entry, not the paper's surface form."""
    print("\ndraw provenance (a recorded item must be redrawable)")
    pools_path = AGENTS / "exam-blueprint" / "references" / "pools.json"
    if not pools_path.is_file():
        return skip("recorded draws resolve to pools.json", "no pools.json")
    pools = json.loads(pools_path.read_text(encoding="utf-8"))
    known = {cat: {f for e in entries for f in _pool_forms(pool_entry_text(e))}
             for cat, entries in pools.items() if isinstance(entries, list)}

    staging = ROOT / "logs" / "adjunct_staging.json"
    staged: set[str] = set()
    if staging.is_file():
        for e in json.loads(staging.read_text(encoding="utf-8")).get("entries", []):
            staged |= _pool_forms(e.get("item", ""))

    specs = {d.name: spec for d, spec in generated_specs()}
    sources: dict[str, list[tuple[str, dict]]] = {}
    for h in ledger_history():
        tid = str(h.get("test_id"))
        if tid != "legacy" and h.get("items"):
            sources.setdefault(tid, []).append(("logs/ledger.json", h["items"]))
    for tid, spec in specs.items():
        if spec.get("items"):
            sources.setdefault(tid, []).append(
                (f"tests/{tid}/test_spec.json", spec["items"]))

    for tid in sorted(sources):
        # merge_seeds.py blends web topics into the SPEC's reading_topics and
        # listening_scenarios, and the ledger keeps a copy with no origin field.
        # Those are traced by check_harvest_provenance (they must resolve to a
        # seed still in logs/seeds.json), not by the pool — so exempt exactly
        # the strings the spec marks `origin: web`, and nothing else.
        web_texts = {pool_entry_text(e)
                     for cat in (specs.get(tid, {}).get("items") or {}).values()
                     for e in cat
                     if isinstance(e, dict) and e.get("origin") == "web"}
        orphans = []
        for where, items in sources[tid]:
            for cat, entries in items.items():
                if cat not in known:
                    continue                # not a sampled category
                for entry in entries or []:
                    if isinstance(entry, dict) and entry.get("origin") == "web":
                        continue            # merge_seeds blend; check_harvest_provenance owns it
                    if isinstance(entry, dict) and entry.get("origin") == "adjunct":
                        evidence = entry.get("evidence")
                        ok = (bool(entry.get("item")) and entry.get("level") == "N2"
                              and isinstance(evidence, list))
                        # openjlpt was deleted 2026-08-11 (exam-blueprint SKILL.md) —
                        # a citation into a corpus no longer in the repo is not
                        # evidence, it is a dangling pointer. 20260811_1 shipped an
                        # adjunct row citing it 32 minutes after the deletion commit.
                        stale = ok and any("openjlpt" in str(e).lower() for e in evidence)
                        if not ok:
                            orphans.append(f"{where} {cat}:「{entry.get('item')}」"
                                           f"(adjunct row missing item/level/evidence)")
                        elif stale:
                            orphans.append(f"{where} {cat}:「{entry.get('item')}」"
                                           f"(adjunct evidence cites deleted openjlpt corpus — "
                                           f"re-cite against Shinkanzen/Soumatome or the official archive)")
                        continue
                    if (isinstance(entry, dict) and entry.get("origin") == "reauthored"
                            and cat in ("reading_topics", "listening_scenarios")):
                        # A 読解/聴解 surface can be rewritten off its drawn topic/
                        # scenario after sampling (e.g. to fix a cross-test theme
                        # collision found in a later stage) — the tested pool ITEMS
                        # never move, only the self-composed prose's seed does, so
                        # this is not the "surface form instead of headword" mistake
                        # the bare check below guards against. Require a `note`
                        # explaining why, same evidentiary bar as `adjunct`.
                        if not entry.get("note"):
                            orphans.append(f"{where} {cat}:「{pool_entry_text(entry)[:20]}」"
                                           f"(reauthored row missing note)")
                        continue
                    text = pool_entry_text(entry)
                    if (not text or text in web_texts
                            or _pool_forms(text) & (known[cat] | staged)):
                        continue
                    orphans.append(f"{where} {cat}:「{text[:20]}」")
        uniq = sorted(set(orphans))
        check(f"test {tid}: every recorded draw resolves to a pools.json entry "
              f"({sum(len(i) for _, i in sources[tid])} items)", not uniq,
              f"{len(uniq)} unresolvable: " + "; ".join(uniq[:10])
              + (" …" if len(uniq) > 10 else "") + " — record the POOL "
              "entry-string, never the paper's inflected surface form "
              "(「〜ずじまい」, not 「行かずじまい」) and never a substitute that "
              "is in no pool: sample_items.recency_map() keys on the pool "
              "string, so an unresolvable entry is permanently un-cooled and "
              "redrawable next test. Re-sample; do NOT reconcile by hand "
              "(exam-blueprint 'Rotation model')")


def check_ledger_spec_agreement():
    """R11: a ledger entry and its spec must record the SAME draw.

    The ledger is the rotation state and the spec is the authoring contract,
    and `sample_items.py` writes both from one draw — so a disagreement means
    one side was hand-edited afterwards. Both consequences are silent: the
    ledger burns cooldown on an item no paper ever asked, and the substitute
    the spec names never rotates at all. A paper has carried three of them at
    once (paraphrase テニスコート→キャンセル, はじめまして→お疲れ様でした,
    quick_response 〜ずじまい→行かずじまい).

    It is an EQUALITY check on purpose — except on the two surfaces
    `merge_seeds.py` blends. merge_seeds replaces reading topics and listening
    scenarios in the SPEC only and never rewrites the ledger's item lists (it
    touches nothing but `harvest_sha`), so a blended category can only be
    checked for containment: every entry the spec still credits to the pool
    must be one the ledger recorded. The web entries themselves are covered by
    the seeds.json traceability check below.
    """
    print("\nledger ↔ test_spec (one draw, two files)")
    hist = ledger_history()
    if not hist:
        return skip("ledger history matches each test_spec", "no logs/ledger.json")
    specs = {d.name: spec for d, spec in generated_specs()}
    if not specs:
        return skip("ledger history matches each test_spec", "no generated specs")
    for entry in hist:
        tid = str(entry.get("test_id"))
        if tid == "legacy" or tid not in specs:
            continue                    # v1 backfill / a test no longer on disk
        led_items = entry.get("items") or {}
        spec_items = specs[tid].get("items") or {}
        off = []
        for cat in sorted(set(led_items) | set(spec_items)):
            led = sorted(pool_entry_text(x) for x in (led_items.get(cat) or []))
            spec_all = spec_items.get(cat) or []
            web = [e for e in spec_all
                   if isinstance(e, dict) and e.get("origin") == "web"]
            kept = sorted(pool_entry_text(e) for e in spec_all if e not in web)
            if web:
                extra = [x for x in kept if x not in led]
                if extra:
                    off.append(f"{cat}: spec keeps {extra} which the ledger "
                               f"never recorded")
            elif kept != led:
                only_spec = [x for x in kept if x not in led]
                only_led = [x for x in led if x not in kept]
                off.append(f"{cat}: spec-only {only_spec}, ledger-only {only_led}")
        check(f"test {tid}: ledger history entry records the same draw as "
              f"tests/{tid}/test_spec.json", not off,
              "; ".join(off) + " — one side was edited after sampling; the "
              "ledger burns cooldown on items the paper never asked and the "
              "substitutes never rotate. Re-sample rather than reconciling by "
              "hand (exam-blueprint 'Rotation model'). Equality here is "
              "NOT enough on its own: record the POOL entry-string, never the "
              "paper's inflected surface form — aligning both files on a "
              "string the sampler cannot resolve satisfies this check while "
              "breaking rotation, which is what check_draw_provenance() above "
              "exists to catch")


def check_harvest_provenance():
    """R12: a harvest_sha must identify a real harvest, not a date-shaped string.

    The existing stamp check is `[0-9a-f]{12}`, which accepts invalid hex stamps —
    a forgery in exactly the shape someone reaching for a plausible value would
    type. Three facts make the stamp mean something again, and all three are
    decidable:
      (a) `merge_seeds.py` writes the SAME sha into the spec and into the
          matching ledger entry, so the two must agree;
      (b) a spec with no `"origin": "web"` entry was never blended, so a
          harvest_sha on it is a claim about work that did not happen;
      (c) some ledger entry must equal `sha1(logs/seeds.json)` — otherwise no
          stamp on disk corresponds to the harvest on disk.
    (a) and (b) FAIL; (c) WARNs, because it cannot distinguish a forged stamp
    from the legitimate window after step 3.5 re-harvests for the NEXT test and
    before merge_seeds runs. Read a (c) warning as "the recorded harvests no
    longer exist on disk" and say which of the two it is.
    """
    print("\nharvest provenance (a stamp must name a real harvest)")
    hist = ledger_history()
    specs = generated_specs()
    led_sha = {str(h.get("test_id")): h.get("harvest_sha") for h in hist}

    disagree, unblended = [], []
    for d, spec in specs:
        spec_sha = spec.get("harvest_sha")
        if d.name in led_sha and led_sha[d.name] != spec_sha:
            disagree.append(f"{d.name}: spec {spec_sha!r} vs ledger "
                            f"{led_sha[d.name]!r}")
        web = 0
        for field in ("reading_topics", "listening_scenarios"):
            web += sum(1 for e in spec.get("items", {}).get(field, [])
                       if isinstance(e, dict) and e.get("origin") == "web")
        for field in ("info_retrieval_texture", "cloze_topic"):
            e = spec.get(field)
            if isinstance(e, dict) and e.get("origin") == "web":
                web += 1
        if spec_sha and web == 0:
            unblended.append(f"{d.name}: harvest_sha {spec_sha} but 0 web entries")
    check("spec and ledger record the same harvest_sha", not disagree,
          "; ".join(disagree) + " — merge_seeds.py writes both in one run; a "
          "difference means one was edited by hand (exam-blueprint)")
    check("only a blended spec carries a harvest_sha", not unblended,
          "; ".join(unblended) + " — an unblended pure-pool run must record no "
          "harvest at all; a stamp with no web entry to explain it is the "
          "forgery shape the 12-hex regex cannot see (exam-blueprint)")

    seeds_path = ROOT / "logs" / "seeds.json"
    recorded = {s for s in led_sha.values() if s}
    if not seeds_path.is_file() or not recorded:
        return skip("a recorded harvest_sha matches logs/seeds.json",
                    "no seeds.json or no stamps recorded")
    on_disk = hashlib.sha1(seeds_path.read_bytes()).hexdigest()[:12]
    warn(f"a recorded harvest_sha matches logs/seeds.json ({on_disk})",
         on_disk in recorded,
         f"ledger records {sorted(recorded)} — either logs/seeds.json was "
         f"edited after blending (the stamps now name a harvest that no longer "
         f"exists, so the no-two-tests-share-a-harvest check is comparing "
         f"ghosts) or step 3.5 has re-harvested for the next test and "
         f"merge_seeds has not run yet. Say which in your report "
         f"(exam-blueprint)")


# R10/R17. `sample_items.py` writes the rotation it actually enforced into the
# spec, so a paper drawn WITHOUT rotation says so in a file instead of in a
# console nobody kept. The gate re-checks the claim: an unverified claim allows
# a draw to repeat items from previous tests.
#
# GRANDFATHER SCOPE, stated exactly: the two specs on disk on 2026-08-06
# (tests/1 and tests/2) were written before `sample_items.py` emitted the key,
# so they cannot carry it and re-sampling them would rewrite the contract their
# 101 keys were placed against (exam-blueprint §"Workflow & Scripts"). They
# are exempted BY NAME, not by a date rule and not by "the key is absent" —
# a timestamp cannot separate them (test 2's spec is stamped today, from a
# reroll that predates the emission by hours) and an absence rule would exempt
# every future test too. Any id not in this set MUST carry the key. Delete an
# entry the moment that test is re-sampled; the exemption prints as a `skip`
# line, so it stays visible in the output rather than passing silently.
ROTATION_GRANDFATHERED = {"1"}


def check_spec_rotation(d, spec: dict, sample, pools: dict):
    """R10: every item must clear ITS OWN category's cooldown window.

    Previously this checked every category against the single
    `rotation.cooldown` scalar the spec records — documented as "the WEAKEST
    level applied to any category" (exam-blueprint 'Rotation model'), i.e.
    whichever category's pool was thin enough to force relaxation that draw.
    That under-checks every category deeper than the thinnest one: a
    grammar_p8/word_formation relaxation down to 2 let this gate accept a
    kanji_reading item (305x headroom, real window ~300 draws) that repeated
    only 7 draws back. `20260817_1` shipped exactly that via a hand
    substitution during QA that never ran `--reroll` — this gate re-reads
    `spec["items"]` fresh off disk regardless of how an item got there, so a
    per-category check catches a silent substitution the same as a bad draw.
    Fixed 2026-08-17; see exam-blueprint SKILL.md 'Rotation model'.
    """
    name = f"{d.name}: test_spec records the rotation it was drawn under"
    rot = spec.get("rotation")
    if not isinstance(rot, dict):
        if d.name in ROTATION_GRANDFATHERED:
            return skip(name, "spec predates the sampler's rotation stamp "
                              "(grandfathered by name; re-sample to clear)")
        return check(name, False,
                     "no `rotation` key — the spec was produced by a "
                     "rotation-less sampler, so nothing proves this paper does "
                     "not redraw the previous test's items. Re-run "
                     "sample_items.py --seed <n> --test-id "
                     f"{d.name} (exam-blueprint 'Rotation is proved in the "
                     "spec')")
    check(name, rot.get("recency_source") == "ledger",
          f"recency_source={rot.get('recency_source')!r} — only 'ledger' names "
          f"a source this gate can re-check (exam-blueprint)")

    per_cat_name = f"{d.name}: rotation claim holds — nothing drawn appears " \
                   "inside its own category's cooldown window"
    if rot.get("legacy"):
        return skip(per_cat_name,
                    "spec is grandfathered legacy — generated before this "
                    "gate checked each category against its OWN "
                    "cooldown_for() window instead of the spec's single "
                    "weakest-category scalar; never re-sample an "
                    "already-authored test to clear this "
                    "(exam-blueprint 'Rotation model')")

    hist = ledger_history()
    self_idx = next((i for i, h in enumerate(hist)
                      if str(h.get("test_id")) == d.name), None)
    prior = hist[:self_idx] if self_idx is not None else \
        [h for h in hist if str(h.get("test_id")) != d.name]
    if not prior:
        return skip(per_cat_name, "no other draws in the ledger to rotate against")

    clashes = []
    for cat, xs in (spec.get("items") or {}).items():
        if cat not in sample.DRAW or cat not in pools:
            continue
        cool = sample.cooldown_for(cat, len(pools[cat]))
        if cool <= 0:
            continue
        recent: dict[str, str] = {}
        for entry in prior[-cool:]:
            tid = str(entry.get("test_id"))
            for xs2 in (entry.get("items") or {}).values():
                for x2 in xs2:
                    t2 = pool_entry_text(x2)
                    recent.setdefault(t2, tid)
                    recent.setdefault(sample.head(t2), tid)
        for x in xs:
            t = pool_entry_text(x)
            if not t:
                continue
            tid = recent.get(t) or recent.get(sample.head(t))
            if tid:
                clashes.append(f"{cat}:「{t}」 (test {tid}, needs its own "
                                f"{cool}-draw cooldown)")
    check(per_cat_name, not clashes,
          "; ".join(clashes[:6]) + " — an item was drawn, or hand-substituted, "
          "inside its OWN category's cooldown window (cooldown_for(cat, "
          "current pool depth), never the spec's single weakest-category "
          "scalar). If a target proves undrawable mid-authoring, "
          "`--reroll <category>` — never substitute an item from memory "
          "(exam-blueprint 'Rotation model')")


def check_rotation_inputs():
    """The two knobs that decide whether a new test is actually new.

    Pool items rotate because the ledger excludes what previous tests drew.
    Web topics have no such memory: `merge_seeds.py` seeds its RNG from the
    spec's own seed, so the SAME `--seed` plus an unchanged `logs/seeds.json`
    reproduces the previous test's blend slot for slot. Using an un-updated
    harvest causes a test to come out as a re-skin of a previous test.
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
        # so two entries that agree on the seed must EACH carry a harvest_sha
        # and disagree on it.
        #
        # An unrecorded harvest is a failure, not an excuse. Treat a missing sha as
        # unknown-and-therefore-unsafe; fix it by re-harvesting and re-running
        # merge_seeds for that test, not by hand-writing a sha.
        clash = []
        for s, entries in by_seed.items():
            if len(entries) < 2:
                continue
            ids = [str(e.get("test_id")) for e in entries]
            shas = [e.get("harvest_sha") for e in entries]
            unrecorded = [i for i, sha in zip(ids, shas) if not sha]
            if unrecorded:
                clash.append(f"seed {s} shared by tests {ids}, and "
                             f"{unrecorded} record no harvest_sha "
                             f"(unrecorded ≠ different)")
            elif len(set(shas)) < len(shas):
                clash.append(f"seed {s} shared by tests {ids} with the same "
                             f"harvest ({shas[0]})")
        check("no two tests share both a --seed and a web harvest", not clash,
              "; ".join(clash) + " — merge_seeds replays the previous blend "
              "slot for slot; re-harvest logs/seeds.json or pick a new seed")

        shas = [h["harvest_sha"] for h in hist if h.get("harvest_sha")]
        invalid_shas = [f"test {h.get('test_id')}: {h.get('harvest_sha')}"
                        for h in hist if h.get("harvest_sha") and not re.fullmatch(r"[0-9a-f]{12}", str(h.get("harvest_sha")))]
        check("every ledger harvest_sha is a valid 12-hex sha1 stamp", not invalid_shas,
              "; ".join(invalid_shas) + " — invalid placeholder sha in ledger history")
        dup = sorted({x for x in shas if shas.count(x) > 1})
        check(f"each test blended its own web harvest ({len(shas)} recorded)",
              not dup, f"harvest_sha reused: {dup} — step 3.5 was skipped")

    seeds_path = ROOT / "logs" / "seeds.json"
    harvest: set[str] = set()
    harvest_on_disk = ""
    if seeds_path.is_file():
        harvest = {s["seed"] for s in json.loads(seeds_path.read_text(encoding="utf-8"))}
        harvest_on_disk = hashlib.sha1(seeds_path.read_bytes()).hexdigest()[:12]

    specs = generated_specs()

    if not specs:
        return skip("test_spec blend contract", "no generated test_spec.json files")

    sample = load(".agents/exam-blueprint/scripts/sample_items.py")
    pools_path = AGENTS / "exam-blueprint" / "references" / "pools.json"
    pools = json.loads(pools_path.read_text(encoding="utf-8")) if pools_path.is_file() else {}
    for d, spec in specs:
        print(f"  {d.name}/test_spec.json")
        check_spec_blend(spec)
        check_spec_adjunct(spec)
        check_spec_rotation(d, spec, sample, pools)
        check_spec_pool_kanji_reading(d, spec)
        if not harvest:
            continue
        blended: list[tuple[str, str]] = []
        for key, field in (("topic", "reading_topics"), ("scenario", "listening_scenarios")):
            for e in spec.get("items", {}).get(field, []):
                if isinstance(e, dict) and e.get("origin") == "web":
                    blended.append((field, e.get(key, "")))
        for field in ("info_retrieval_texture", "cloze_topic"):
            e = spec.get(field)
            if isinstance(e, dict) and e.get("origin") == "web":
                blended.append((field, e.get("detail") or e.get("topic", "")))
        if not blended:
            continue
        # R19. Only the spec whose OWN harvest is the one on disk can be checked.
        #
        # This used to validate every spec against the single current
        # logs/seeds.json, which put the gate in direct conflict with the
        # pipeline it gates: `exam-blueprint` §"Step 0" makes the harvest a
        # per-test input — 「A harvest is an input to one test, not a file that
        # lives in the repo. Re-harvest it, every time.」 — and leaving the
        # previous harvest in place is precisely what once turned a paper into
        # a re-skin of the one before it. So performing step 3.5 correctly for
        # test N NECESSARILY orphans every web entry of test N−1, and the gate
        # has failed an older test for the newer one having been generated
        # properly — once failing all 13 of a test's blended entries for no
        # reason but that.
        #
        # The property worth keeping is that a spec's web entries trace to a
        # REAL harvest rather than being invented during authoring — and that is
        # exactly when this check has evidence: while a test is being built, its
        # harvest IS logs/seeds.json. Afterwards the harvest is gone by design
        # and the honest answer is "cannot verify", which is a skip, not a pass
        # and not a failure. The skip prints, so an unverifiable spec stays
        # visible instead of going quiet.
        #
        # To verify the whole history instead, merge_seeds.py would have to
        # archive each harvest it consumes (logs/harvests/<harvest_sha>.json)
        # and this check would look the spec's own harvest_sha up there. That is
        # a pipeline change, not a gate change; until it lands, this is the most
        # the gate can honestly assert.
        spec_sha = spec.get("harvest_sha")
        trace = (f"{d.name}: every web entry in test_spec traces to "
                 f"logs/seeds.json ({len(blended)} blended)")
        if not harvest_on_disk or spec_sha != harvest_on_disk:
            skip(trace,
                 f"spec was blended from harvest {spec_sha or 'unrecorded'}, "
                 f"logs/seeds.json is {harvest_on_disk or 'absent'} — a harvest "
                 f"is a per-test input and is re-harvested for the next test "
                 f"(exam-blueprint Step 0), so this spec's seeds are no "
                 f"longer on disk to check against")
            continue
        orphans = [f"{f}:「{t}」" for f, t in blended if t not in harvest]
        check(trace, not orphans,
              "; ".join(orphans) + " — logs/seeds.json IS this spec's own "
              "harvest (sha matches), so a web entry missing from it was "
              "invented rather than blended; re-run merge_seeds")


def check_answer_positions(d, keys: dict[int, int], ck: dict[str, int], g):
    """Keys must sit where sample_items.py put them (the balance contract).

    tests/<test_id>/test_spec.json prescribes the answer position of every item so no
    number is over-used; authoring is supposed to place the correct choice
    there. Only the test that spec belongs to can be checked.

    SLOT AGREEMENT ONLY — and the label says so, because green here was read as
    evidence about the keys themselves and it never was. This compares two
    numbers: the digit in the 正解 column and the digit the spec reserved. A key
    written to satisfy the spec rather than the passage agrees with it perfectly,
    which is exactly how tests/3's 聴解 問題1-1番 (key 4, 解説 tagging option 3
    （正解）) stayed green. Content correctness is exam-qa-review step 1, and its
    one string-decidable corner is check_choukai_kaisetsu_keys.
    """
    label_tail = " (slot agreement only — content correctness is exam-qa-review step 1)"
    spec_path = d / "test_spec.json"
    if not spec_path.is_file():
        return skip("keys match test_spec.json answer_positions" + label_tail,
                    "no test_spec.json")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if str(spec.get("test_id")) != d.name:
        return skip("keys match test_spec.json answer_positions" + label_tail,
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
    check(f"keys match test_spec.json answer_positions ({len(want)} prescribed)"
          + label_tail, not off, f"prescribed vs actual: {off}")


# 2026-08-11: check_mondai1_key_band() and check_moji2_stem_kana() were
# retired here along with openjlpt (exam-blueprint/SKILL.md; no replacement
# word/reading/level index — Shinkanzen/Soumatome have no text layer). Both
# encoded real rules that shipped real defects (kanji_reading validity rule
# 2b — 免れる keyed the harder of two 訓読み before an audit fixed it; a 問題2
# stem printing kana that matched no option's reading) and both are now on
# the author/QA to verify by hand against Shinkanzen/Soumatome and the
# official archive, not on this gate.


MOJI2_SEC = re.compile(r"^##\s*問題2\b(.*?)(?=^##\s*問題3\b)", re.M | re.S)
MOJI4_SEC = re.compile(r"^##\s*問題4\b(.*?)(?=^##\s*問題5\b)", re.M | re.S)
KANA_RUN = re.compile(r"[ぁ-ゔァ-ヴー]+")


def check_moji4_blank_stems(name: str, gt: str, keys: dict[int, int],
                            opts: dict[int, list[str]]):
    """Every 問題4 stem is a printed （　） and prints no answer word (G16/F1).

    A stem that prints its answer word in the sentence (e.g. 「…を目指すコンテスト」)
    makes the row self-answering and doubles the option line. Official booklets
    print every stem with （　） — the instruction asks for the best word to put IN it —
    so the stem never holds the answer. This is the string-decidable half: a stem line with no blank,
    or whose key option text appears in the sentence, is the defect regardless of content
    quality. Imported transcriptions that do not use **N** stem lines match no
    stems and pass vacuously.
    """
    sec = MOJI4_SEC.search(gt)
    if not sec:
        return
    missing, leaking = [], []
    for ln in sec.group(1).splitlines():
        ln = ln.strip()
        m = re.match(r"\*\*(\d+)\*\*(.*)", ln)
        if not m:
            continue
        q = int(m.group(1))
        stem = m.group(2)
        if "（　）" not in stem and not BLANK_RUN.search(stem):
            missing.append(f"{q}: no blank — {stem[:34]}")
        key_i = keys.get(q)
        row = opts.get(q) or []
        if key_i and 1 <= key_i <= len(row) and row[key_i - 1] in stem:
            leaking.append(f"{q}: prints its key {row[key_i - 1]!r} in the stem")
    check(f"{name}: every 問題4 stem prints （　） and no answer word",
          not missing and not leaking,
          "; ".join(missing + leaking) + " — the 問題4 instruction asks for the "
          "best word to put in （　）; a stem that prints the blank's answer is "
          "self-answering (question-authoring 問題4)")


def check_spec_target_items(d, gt: str, st: str, bi):
    """The paper must test the items the spec drew (G19).

    A paper's 問題4 8番 has tested 「本日は遠方からお越しいただき…」 while the spec drew
    「こちらこそ、いつもお世話になっております。」 — an unrecorded substitution, so the
    ledger burned an item the paper never asked and the substitute never
    rotates. Only the three categories that are literal substrings of their own
    stems are decidable here; grammar_p7/context_words often are not, and stay
    with exam-qa-review §6.1.
    """
    spec_path = d / "test_spec.json"
    if not spec_path.is_file():
        return skip(f"{d.name}: 問題1/2/4 test the sampled items",
                    "no test_spec.json")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if str(spec.get("test_id")) != d.name:
        return skip(f"{d.name}: 問題1/2/4 test the sampled items",
                    f"spec is for test {spec.get('test_id')}, not {d.name}")

    cut = bi.KEY_HEADING.search(gt)
    body = gt[: cut.start()] if cut else gt
    p4 = re.split(r"^問題([1-5])。$", st, flags=re.M)
    haystacks = {
        "kanji_reading": dokkai_section(body, 1),
        "orthography": dokkai_section(body, 2),
        "quick_response": "".join(p4[i + 1] for i in range(1, len(p4), 2)
                                  if p4[i] == "4"),
    }
    missing = []
    for cat, hay in haystacks.items():
        for entry in spec.get("items", {}).get(cat, []):
            item = entry.get("item") if isinstance(entry, dict) else entry
            if not item:
                continue
            # kanji_reading/orthography are written `軍(いくさ)` — the reading is
            # an annotation, and 副(フク) prints its options in hiragana, so only
            # the base form is decidable. Idiom entries inflect (顔が広い appears
            # as 顔が広くて), so a one-character trim counts as found.
            # A leading 〜 is pool NOTATION for a bound form, never printable
            # text: pools.json stores 「〜かと思いきや」-style entries (7 in
            # quick_response, 108 of 112 in grammar_p7) and the paper spells
            # them 「大人しいかと思いきや」. Probing with the tilde attached can
            # never match, so a correctly authored item read as missing.
            base = re.sub(r"\s*[（(][^）)]*[）)]\s*$", "", item).strip().lstrip("〜～")
            probes = [item, base, base.rstrip("。")]
            if len(base) >= 4:
                probes.append(base.rstrip("。")[:-1])
            if any(p and p in hay for p in probes):
                continue
            # G6. 問題1/2 print the target CONJUGATED — 慌てる as 「**慌てて**」,
            # 潔い as 「**潔く**」 — which official papers do freely (7/2025 marks
            # 「**収まった**」, 「**辛い**」). A dictionary-form probe can never
            # match one of those, and the one-character trim above is gated on
            # `len(base) >= 4`, which a 3-char 慌てる and a 2-char 潔い never
            # reach. tests/1 read as three unrecorded substitutions for items it
            # tests correctly.
            #
            # The repair is a KANJI-STEM probe, deliberately narrowed twice so a
            # single kanji cannot false-pass on an unrelated word: it applies
            # only to entries whose base ends in kana (an inflecting word — 交渉
            # and 措置 keep the strict probe), and it must land on a **bold**
            # span that STARTS with the stem, i.e. on the marked target itself,
            # not on running prose. Lowering the `>= 4` threshold instead would
            # buy nothing (trimming a 2-char base yields the same lone kanji)
            # while weakening the compound entries.
            if cat in ("kanji_reading", "orthography"):
                stem = re.sub(r"[ぁ-ゖ]+$", "", base.rstrip("。"))
                if stem and stem != base.rstrip("。") and re.search(r"[一-鿿]", stem):
                    marked = re.findall(r"\*\*([^*\n]+)\*\*", hay)
                    if any(sp.startswith(stem) for sp in marked):
                        continue
            missing.append(f"{cat}:「{item[:24]}」")
    check(f"{d.name}: 問題1/2/4 test the items test_spec.json drew "
          f"({sum(len(spec.get('items', {}).get(c, [])) for c in haystacks)} targets)",
          not missing,
          "; ".join(missing) + " — author only the sampled items, or re-sample; "
          "a silent substitution corrupts rotation (exam-blueprint)")


def check_script_shape(script_text: str, ct: str, m, test_id: str = ""):
    """聴解 script ↔ booklet: same instructions, options spoken only where the
    booklet prints none (jlpt-exam-structure's 'Printed in booklet' column)."""
    drift = [ln for ln in re.findall(r"^問題[1-5]では、.*$", ct, re.M)
             if ln.strip() not in script_text]
    check("問題N instructions are identical in booklet and script", not drift,
          f"booklet wording absent from the script: {[d[:34] + '…' for d in drift]}")

    # Check for instruction drift from canonical official wording (warn)
    canon_drift = []
    if "問題用紙のせんたくしを読んで" in ct or "問題用紙の選択肢を読んで" in ct:
        canon_drift.append("問題2: uses 'せんたくしを読んで' instead of '問題用紙を見て'")
    if re.search(r"問題5では、.*メモをとってもかまいません", ct) and "問題用紙にメモを" not in ct:
        canon_drift.append("問題5: missing '問題用紙に' before 'メモをとっても'")
    if "選びなさい" in ct:
        canon_drift.append("聴解 instruction uses '選びなさい' instead of '選んでください'")
    warn("問題N instructions follow official wording", not canon_drift,
         "; ".join(canon_drift))


    secs = re.split(r"^問題([1-5])。$", script_text, flags=re.M)
    spoken = {int(secs[i]): len(re.findall(r"^[1-4]、", secs[i + 1], re.M))
              for i in range(1, len(secs), 2)}
    # 問題1/2 print their options; 問題3 speaks 4 per item, 問題4 speaks 3;
    # 問題5 prints NOTHING for either item, so it speaks 4 for 1番 plus 4 under
    # each of 2番's two questions = 12.
    ei = m.EXPECTED_ITEMS
    want = {1: 0, 2: 0, 3: 4 * ei["問題3"], 4: 3 * ei["問題4"], 5: 12}
    check("options are spoken exactly where the booklet prints none",
          spoken == want, f"spoken option lines {spoken}, expected {want}")

    # 問題5's 2番 gets a spoken lead-in of its OWN, as a block before 「2番。」 —
    # never as the first line of the item block, where it would sit after the
    # 「2番。」 marker and be read as part of the situation. Official prints 2番's
    # options and therefore speaks no lead-in at all; this repo prints nothing
    # for 問題5, so the lead-in has to be heard or the examinee is never told the
    # choices are spoken. The anchor is 「2番。」 alone: an earlier version split
    # on the full sentence, i.e. it assumed the text was there and only checked
    # what followed, which is a gate written around the shape it is judging.
    check(f"{test_id}: 問題5 2番 lead-in is spoken, and precedes 「2番。」",
          not re.search(r"^2番。(問題用紙に何も印刷|まず話を聞いてください)",
                        script_text, re.M),
          "the lead-in must be its own block BEFORE 「2番。」, not the item "
          "block's opening line — 「2番。」 must be followed by the situation "
          "(jlpt-exam-structure §問題5, choukai-audio §'Spoken vs printed choices')")

    # 2番 SPEAKS its four choices, twice — once under 質問1, once under 質問2 —
    # because nothing is printed for it. The inverse of this check (「2番 does
    # not speak its printed options」) was correct only while the booklet
    # carried the option list; leaving it in would now forbid the only thing
    # that makes the item answerable.
    p5 = re.split(r"^問題5。$", script_text, maxsplit=1, flags=re.M)
    tail = re.split(r"^2番。", p5[-1], flags=re.M)
    spoken_2ban = len(re.findall(r"^[1-4]、", tail[-1], re.M)) if len(tail) > 1 else 0
    check("問題5 2番 speaks four choices under each of its two questions",
          spoken_2ban == 8,
          f"{spoken_2ban} spoken choice lines after 「2番。」, expected 8 — "
          f"問題5 prints nothing, so 質問1 and 質問2 each need their four "
          f"choices read aloud (jlpt-exam-structure §問題5)")

    ascii_punct = re.findall(r"(?<!\d)[,.](?!\d)", script_text)
    check("no ASCII , or . in the script (TTS mis-times them)", not ascii_punct,
          f"{len(ascii_punct)} found — use 、 and 。")


# G3. 問題5 2番 enumerates four candidates aloud, then reads them back as a
# numbered choice list under each question. Two facts about official papers make
# that pair checkable, both measured on the archive extracts
# (`refs/JLPT_N2_NEW/*/script.md` + `booklet.md`; the dialogue there is OCR,
# good enough for ORDER and SHAPE, never for wording). Official carries the
# numbered list in the BOOKLET and this repo speaks it instead, but the rules
# are about the relationship between the enumeration and the numbered list, so
# they survive the move intact — only the file the list is read from changed.
#
#   ORDER — the numbered list is the enumeration order. July 2025 speaks
#   1つ目 夕日通り / 2つ目 西が丘 / 3つ目 さくら公園 / 最後 東山 and prints
#   1 夕日通り / 2 にしがおか / 3 さくら公園 / 4 東山. Dec 2014 (1〜4つ目, 4 方法)
#   and July 2019 (まず/2つ目/それから/4つ目, 4 校舎) do the same. Dec 2025
#   enumerates by the printed number itself (「1番の自転車は…」), which is the
#   same rule with the labels made explicit.
#
#   DECIDER — the line that resolves each question names an ATTRIBUTE of a
#   candidate, never its ordinal: 「鳥が見られる所？」「お寺の近くっていう所」
#   (7/2025), 「1番安定性が高いのにする」「折りたためる自転車なら」 (12/2025),
#   「僕はCDだな」 (12/2014). In 31 sittings no 問題5 candidate item speaks a
#   `Nつ目` back-reference after its enumeration.
#
# Both broke in one repair of tests/3: the printed list was re-ordered to move
# the key (spoken 個別面談/模擬面接/AI/座談会, printed AI/模擬面接/個別面談/座談会)
# while the audio still resolved 質問1 with 「それなら、3つ目の方法がぴったりです
# ね」 — an ordinal pointing at printed slot 3 while the key sat at slot 1, i.e.
# two defensible answers manufactured by editing the booklet alone.
#
# Decidable only where the script actually uses ordinal labels; papers that
# enumerate by name or by 「N番の」 resolve nothing here and are left to
# exam-qa-review step 4.
P5_ORDINAL = re.compile(r"([1-4１-４一二三四])つ目|(最後)")
_KANJI_DIGIT = {"一": 1, "二": 2, "三": 3, "四": 4}


def _ordinal_value(m: re.Match) -> int:
    if m.group(2):
        return 99                       # 最後 — terminal, closes the run
    tok = unicodedata.normalize("NFKC", m.group(1))
    return _KANJI_DIGIT.get(tok, 0) or int(tok)


def choukai_p5_2ban_options(script_text: str) -> list[str]:
    """The four candidate names 問題5 2番 SPEAKS under 質問1, in spoken order.

    These used to be read out of the booklet, because 2番 was the one 問題5 item
    whose options were printed. This repo prints nothing for 問題5 at all, so the
    numbered list the key points at is the spoken one and the script is now its
    only home — the ordering rule below is unchanged, it just has one file to
    read instead of two.
    """
    p5 = re.split(r"^問題5。$", script_text, maxsplit=1, flags=re.M)
    tail = re.split(r"^2番。", p5[-1], flags=re.M)
    if len(tail) < 2:
        return []
    block = tail[-1].split("\n\n")[0]
    q1 = re.split(r"^質問1。", block, maxsplit=1, flags=re.M)
    if len(q1) < 2:
        return []
    q1_span = re.split(r"^質問2。", q1[-1], maxsplit=1, flags=re.M)[0]
    return [o.strip().rstrip("。") for _, o in
            re.findall(r"^([1-4])、(.+)$", q1_span, re.M)]


# 問題5 prints NOTHING — for 1番 (official) and, in this repo, for 2番 too. The
# booklet carries a bare bubble row per question and a メモ area, never an option
# list. This is the check that keeps the two halves of that decision together:
# the moment someone re-adds a printed list under 質問1, the audio is still
# speaking the same four choices and the paper has two option lists to
# desynchronise (which is the defect the printed-vs-spoken column exists to
# prevent, one level up).
def check_mondai5_prints_nothing(name: str, ct: str, bi):
    cut = bi.KEY_HEADING.search(ct)
    body = ct[: cut.start()] if cut else ct
    sec = re.search(r"^##\s*問題5\b.*", body, re.M | re.S)
    if not sec:
        return
    printed = re.findall(r"^\s+([1-4])\.\s*(\S.*)$", sec.group(0), re.M)
    check(f"{name}: 問題5 prints no options (both items are spoken)",
          not printed,
          f"{len(printed)} printed option line(s) under 問題5 "
          f"({[o for _, o in printed][:4]}) — 問題5 carries only the bubble rows "
          f"「**質問1** 1 ・ 2 ・ 3 ・ 4」 and メモ space; its choices are read "
          f"aloud (jlpt-exam-structure §聴解)")


def check_mondai5_enumeration(name: str, script_text: str, ct: str, bi):
    p5 = re.split(r"^問題5。$", script_text, maxsplit=1, flags=re.M)
    tail = re.split(r"^2番。", p5[-1], flags=re.M)
    if len(tail) < 2:
        return
    block = tail[-1].split("\n\n")[0]
    # Scan the DIALOGUE only. The block now also carries the numbered choice
    # lists read back under 質問1/質問2, and those name every candidate — an
    # ordinal's span would run into them and match all four, resolving nothing.
    block = re.split(r"^質問1。", block, maxsplit=1, flags=re.M)[0]
    marks = list(P5_ORDINAL.finditer(block))
    if not marks:
        return skip(f"{name}: 問題5 2番 choice order = spoken enumeration order",
                    "the script enumerates without Nつ目/最後 labels — "
                    "exam-qa-review step 4 owns it")

    # (a) A `Nつ目` that does not continue the ascending run is a back-reference
    #     to an already-introduced candidate, i.e. the ordinal deciding the item.
    back, highest = [], 0
    for hit in marks:
        val = _ordinal_value(hit)
        if val > highest:
            highest = val
        elif not hit.group(2):
            back.append(hit.group(0))
    check(f"{name}: 問題5 2番 decides by attribute, not by ordinal", not back,
          f"{back} spoken after the enumeration closed — official resolves with "
          f"「鳥が見られる所？」/「折りたためる自転車なら」, never 「Nつ目のに"
          f"します」. An ordinal decider ties the answer to a numbered SLOT, so "
          f"re-ordering the choice list silently re-keys the item: name the "
          f"candidate instead (choukai-audio 問題5 2番)")

    # (b) Candidate n of the enumeration must be choice n of the numbered list.
    opts = choukai_p5_2ban_options(script_text)
    if len(opts) != 4:
        return
    flat_opts = [_flat(o) for o in opts]
    seen, unresolved = [], 0
    for i, hit in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(block)
        span = _flat(block[hit.start():end])
        found = [n for n, o in enumerate(flat_opts, 1) if o and o in span]
        if len(found) == 1:
            seen.append(found[0])
        else:
            unresolved += 1
    if len(seen) < 2:
        return skip(f"{name}: 問題5 2番 choice order = spoken enumeration order",
                    f"only {len(seen)} of {len(marks)} enumerated candidates match "
                    f"a numbered choice by name")
    check(f"{name}: 問題5 2番 choice order = spoken enumeration order "
          f"({len(seen)} of {len(marks)} candidates resolved)",
          seen == sorted(seen),
          f"enumerated candidates land on choice slots {seen} — the four are "
          f"read back in the order the audio introduced them (7/2025, 12/2014, "
          f"7/2019). Both halves live in 聴解スクリプト.txt now, so fix it there "
          f"and run `make mp3 {name}`; re-ordering the choice list alone "
          f"re-keys the item (jlpt-exam-structure 問題5 2番)")


# G15. REGISTER. Every generated paper so far passed this gate while sounding
# nothing like the official recording, and the difference is countable — see
# `choukai-audio/references/official_register.md`, measured over the 31-sitting
# archive (321 k chars, 3 215 turns) against generated papers:
#
#   short reaction turns (<=12 ch)   official 18 %   generated 6 %
#   turns opening with a filler      official 35 %   generated 18 %
#   hesitation tokens per paper      official 27     generated 0-4  (band 9-48)
#   flat 「〜ではありません」/10 k       official 0.4    generated 17.1
#
# Re-measured 2026-08-13 (official_register.md §7) after 8 papers had shipped
# against these rules: every counted measure above is now inside the band, and
# five UNCOUNTED ones are outside it — 問題1 counter settings 42 % vs 6 %, 問題2
# 「一番/優先」 keys 52 % vs 6 %, 問題4 already-done distractors 9/11 vs 1/11.4,
# 問題3 options suffixed 「〜について」 60 % vs 1 %, 問題5 three-party items 0 vs one
# per sitting. Fixing a counted tell grows an uncounted one, so those five are
# written as per-section QUOTAS in choukai-items.md §"Section item mix" and read
# off the セクション構成表 by exam-qa-review §4; they are not yet gated here.
#
# The FAIL-class rows below are not style: each makes items solvable by pattern.
# 問題3's triple denial names three of the four options aloud and rejects each;
# an identical closing turn across a section's items teaches the shape of the
# key; a 問題4 option set of はい/いいえ/では is answerable without the prompt
# (when almost every 「まだ〜ていません」 option is a wrong answer, the shape is
# the key).
#
# Thresholds are set at or below the official MINIMUM, never at its median, so a
# paper is only flagged when it is outside the archive's whole range.
P3_DENIAL_RE = re.compile(r"(話ではありません|論じているのでもありません"
                          r"|取り上げているわけでもありません|わけでもありません)")
FILLERS = ("あのう", "あの、", "えー", "えっと", "ええと", "うーん", "まあ、", "あ、", "ああ、")
# Measured over the 31 archive extracts with THIS token list: median 27, range
# 9-48 (official_register.md §7.1). Two-sided, because the papers went through
# the top (23-58) after the one-sided floor was added: over-hesitating is a tell
# too. The floor is the archive MINIMUM, per this file's stated threshold policy
# — the old 13 sat above three sittings, both 2025 papers among them.
FILLER_MIN, FILLER_MAX = 9, 48
REACTION_MAX_CH = 12
Q4_SHAPE_RE = re.compile(r"^(はい|いいえ|いえ|では)[、。]")


def script_turns(script_text: str, m) -> list[str]:
    """Spoken text of every speaker-tagged line (the narrator is not a turn)."""
    out = []
    for line in script_text.splitlines():
        hit = m.SPEAKER_RE.match(line.strip())
        if hit and hit.group(1) in m.SPEAKER_MAP:
            out.append(hit.group(2).strip())
    return out


def check_script_register(name: str, script_text: str, m):
    """Dialogue must read as people talking, not one template per section (G15)."""
    turns = script_turns(script_text, m)
    if not turns:
        return skip(f"{name}: 聴解 script register", "no speaker-tagged turns")

    # --- FAIL: the 問題3 denial sweep (0 in 31 official sittings) -------------
    p3 = re.split(r"^問題3。$", script_text, maxsplit=1, flags=re.M)
    p3 = re.split(r"^問題4。$", p3[-1], maxsplit=1, flags=re.M)[0] if len(p3) > 1 else ""
    sweeps = P3_DENIAL_RE.findall(p3)
    check(f"{name}: 問題3 monologues do not deny the other options",
          not sweeps,
          f"{len(sweeps)} denial phrase(s) in 問題3 — the close 「Xの話ではありません"
          f"し、Yについて論じているのでもありません…」 appears 0 times in 31 official "
          f"sittings and has shipped in every item of a generated 問題3. It reads "
          f"the wrong options out and rejects them, so the item is solvable from "
          f"the negations alone. Official 概要理解 distractors are topic-level "
          f"near-misses the talk never mentions "
          f"(question-authoring/references/choukai-items.md 問題3)")

    # --- FAIL: a 問題3 monologue that names its own distractors --------------
    # Stronger than the phrase list above, which only catches the wordings we
    # happened to ship: one paper wrote 「〜を主に論じているのではありません」 and
    # slipped through. This counts how many of the item's OWN four spoken
    # options the talk mentions. Official monologues mention the keyed topic and
    # nothing else — usually paraphrased, so even that often scores 0.
    named = []
    for block in re.split(r"\n\s*\n", p3):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines or not m.ITEM_RE.match(lines[0]):
            continue
        opts = [o for _, o in re.findall(r"^([1-4])、(.+?)。?$", "\n".join(lines), re.M)]
        talk = "\n".join(l for l in lines if not re.match(r"^[1-4]、", l))
        hits = [o for o in opts if len(o) >= 5 and o.rstrip("。") in talk]
        if len(hits) >= 2:
            named.append(f"{lines[0][:4]} mentions {hits}")
    check(f"{name}: 問題3 monologues do not name their own distractors",
          not named,
          "; ".join(named) + " — a 概要理解 talk that lists the other options "
          "(to reject them, or at all) is answerable from the list instead of "
          "the content. Official talks mention only their own subject "
          "(choukai-items.md 問題3)")

    # --- FAIL: a 問題3 lead-in that names the topic answers the question -----
    topical = [ln.split("。")[0] for ln in re.findall(r"^(?:例|\d+番)。.*$", p3, re.M)
               if "について" in ln or "の話" in ln]
    check(f"{name}: 問題3 lead-ins name the setting, not the topic", not topical,
          f"{topical} — official 問題3 says 「ラジオで女の人が話しています。」 and "
          f"nothing more, in every item of every sitting, because 「何について話して"
          f"いますか」 IS the task. Generated papers wrote 「…◯◯の注意点について"
          f"話しています」 over a keyed option naming that same ◯◯, i.e. read the "
          f"answer out before the talk began (choukai-items.md 問題3)")

    # --- FAIL: an identical closing turn reused across items -----------------
    closers = collections.Counter()
    for block in re.split(r"\n\s*\n", script_text):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines or not m.ITEM_RE.match(lines[0]):
            continue
        spoken = [t for t in (m.SPEAKER_RE.match(l) for l in lines) if t
                  and t.group(1) in m.SPEAKER_MAP]
        if spoken:
            closers[spoken[-1].group(2).strip()] += 1
    reused = {t: n for t, n in closers.items() if n > 1 and len(t) > 4}
    check(f"{name}: no two 聴解 items end on the same turn", not reused,
          "; ".join(f"「{t}」×{n}" for t, n in sorted(reused.items())) +
          " — one closing turn reused across most items of a section "
          "which teaches the shape of the key rather than testing listening "
          "(choukai-audio §Banned formulas)")

    # --- WARN: register floors (official minimum, not median) ----------------
    reactions = [t for t in turns if len(t) <= REACTION_MAX_CH]
    share = len(reactions) / len(turns)
    warn(f"{name}: 聴解 dialogue carries short reaction turns "
         f"({share * 100:.0f}% of {len(turns)})", share >= 0.12,
         f"official is 18% (589/3215 turns <=12 chars: 「はい。」「そうですか。」"
         f"「うん。」); below ~12% the conversation never lets the other speaker "
         f"land, and the audio loses the 0.9 s turn gaps that make it breathe "
         f"(official_register.md §1)")

    fillers = sum(script_text.count(f) for f in FILLERS)
    warn(f"{name}: 聴解 dialogue hesitates like a person ({fillers} tokens)",
         FILLER_MIN <= fillers <= FILLER_MAX,
         f"official measures a median of {27} over this FILLERS list with a band "
         f"of {FILLER_MIN}–{FILLER_MAX} across 31 sittings (the earlier figure "
         f"'median 41, never fewer than 13' was wrong in both halves — 12/2024 "
         f"and 7/2025 measure 9 — see official_register.md §7.1, which is why "
         f"this floor is 9 and not 13). Under the floor: no human wrote it. OVER "
         f"the ceiling is its own tell — a script performing hesitancy; papers "
         f"have shipped at 58. The real deficit is not fillers: official carries "
         f"うん 11.3/paper against our 4.2, so spend the budget on the OTHER "
         f"speaker acknowledging, not the current one stalling. Keep all of it "
         f"out of the ANNOUNCER's lines (choukai-audio §Register)")

    denials = len(re.findall(r"(ではありません|じゃありません|必要は?ありません"
                             r"|しなくていい)", script_text))
    per10k = denials / max(len(script_text) / 10000, 1e-9)
    warn(f"{name}: wrong options are eliminated, not contradicted "
         f"({per10k:.1f} flat denials/10k chars)", per10k <= 6.0,
         f"official measures 1.4/10k for this whole family and 0.4 for bare "
         f"「〜ではありません」; papers written without the rule measure over ten "
         f"times that. Prefer reassigning the task to a named third party, "
         f"deferring it (その前に/後回し), refusing it (難しい/見送), or noting it is "
         f"already done — and rotate the device across a section's items "
         f"(choukai-items.md §Eliminated ≠ contradicted)")

    q4 = re.split(r"^問題4。$", script_text, maxsplit=1, flags=re.M)
    q4 = re.split(r"^問題5。$", q4[-1], maxsplit=1, flags=re.M)[0] if len(q4) > 1 else ""
    replies = [r for _, r in re.findall(r"^([1-3])、(.+)$", q4, re.M)]
    if replies:
        shaped = [r for r in replies if Q4_SHAPE_RE.match(r)]
        pct = len(shaped) / len(replies)
        warn(f"{name}: 問題4 replies open with content, not はい/いいえ/では "
             f"({pct * 100:.0f}% of {len(replies)})", pct <= 0.20,
             f"official: 1.3% of 1113 replies (94% open with content); generated "
             f"papers have run over half. A set of 「はい、〜」/「いいえ、まだ〜ていません」"
             f"/「では、〜」 is solvable without hearing the prompt — write three "
             f"stances on the prompt instead (choukai-items.md §即時応答)")


# G16. SECTION-LEVEL defects. Every 聴解 defect that has cleared both a green
# gate AND a fresh-eyes QA was a repeat across a section's items, invisible one
# item at a time: G15 above counts tokens, check_choukai_kaisetsu_keys reads one
# row, nothing ever put two KEYS side by side. `20260813_2` 問題1 shipped
# 「本人確認書類を提示する」 as the key of BOTH 1番 and 2番, reached by the same
# interrupting line, past all of it.
#
# Thresholds follow this file's policy — at or beyond the archive's whole range,
# never at its median — so a FAIL means "no official sitting looks like this",
# while the authoring TARGETS (tighter) live in choukai-items.md §"Section item
# mix". Measured 2026-08-13 over the 31 script.md extracts; method and per-paper
# numbers in choukai-audio/references/official_register.md §7.
#
#   quantity                          official                 gate FAILs at
#   問題3 options ending 「について」      8 of 685 (1 %)           > 2 per paper
#   問題3 talk, spoken chars           median 305, p10 251,     any item < 175
#                                     min 177 (n=149)
#   問題4 items w/ an already-done      median 1, max 3          > 3
#     (もう/すでに/さっき) distractor      of 11-12 items
#   問題5 items with >=3 speakers      >=1 in 31/31 sittings    0
#   two consecutive lines, one label   0 (our format contract)  any
#
# The judgment half — is this item a service counter, is this talk a person's
# 主張 — cannot be decided by regex, so it is WARN-only below and belongs to
# exam-qa-review §4, which reads the セクション構成表's columns.
ALREADY_DONE_RE = re.compile(r"(もう|すでに|既に|さっき)")
COUNTER_RE = re.compile(r"(窓口|受付|フロント|レジ|店で|店に|店員|客|電話をかけ"
                        r"|問い合わせ|カウンター)")
BROADCAST_RE = re.compile(r"(ラジオ|テレビ|ニュース|講演|講座|インタビュー|番組|広報)")
P3_TALK_FLOOR = 175
P3_TALK_TARGET = 220

# GRANDFATHER SCOPE, stated exactly: the eight papers on disk on 2026-08-13 were
# authored before any of these rules existed, and every one breaches at least the
# セクション構成表 row (an artifact none of them could have written). Clearing a
# breach means re-authoring items and rebuilding the MP3, which is a decision
# about those papers, not about this gate — so they are exempted BY NAME and
# their breaches print as WARN lines carrying the same measurement a FAIL would,
# never as `ok` and never as silence. Any id not in this set FAILS. Delete an id
# the moment that test's 聴解 is repaired; do not add one to quiet a new paper.
CHOUKAI_SECTION_GRANDFATHERED = {
    "20260807_1", "20260810_1", "20260810_2", "20260811_1",
    "20260812_1", "20260812_2", "20260813_1",
    # 20260813_2 removed 2026-08-14: its 聴解 was re-authored against the G16/G17
    # rules (duplicate key, split turns, 問題3 talks and options, 問題4 distractor
    # shapes, 問題5 three-party, contractions, paraphrased keys, 構成表) and it
    # now clears them un-grandfathered. This set shrinks one repaired paper at a
    # time; never add an id back to quiet a regression.
}
GRANDFATHER_NOTE = " [pre-rule paper — a FAIL for any id not grandfathered]"


def _gated(test_id: str, name: str, ok: bool, detail: str):
    """FAIL for a paper authored under the rule, WARN for one that predates it."""
    if test_id in CHOUKAI_SECTION_GRANDFATHERED:
        return warn(name, ok, detail + GRANDFATHER_NOTE)
    return check(name, ok, detail)


def choukai_item_label(first_line: str) -> str:
    return "例" if first_line.startswith("例。") else first_line.split("番。")[0] + "番"


def choukai_key_table(ct: str, bi) -> dict[tuple[int, str], int]:
    """{(問題, '1番'): keyed option} from the 【正解・解説】 tables.

    The 番号 column has shipped in two forms — `1` in the first three papers,
    `1番` since — so both normalize here. `check_choukai_kaisetsu_keys` read only
    the first form, which is half of why it went silent (see its docstring).
    """
    cut = bi.KEY_HEADING.search(ct)
    if not cut:
        return {}
    out, sec = {}, None
    for line in ct[cut.start():].splitlines():
        head = re.match(r"^#+\s*問題([1-5])", line)
        if head:
            sec = int(head.group(1))
            continue
        if sec is None or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 2 or not CHOUKAI_ITEM_LABEL.match(cells[0]):
            continue
        keyed = re.fullmatch(r"\**\s*([1-4])\s*\**", cells[1])
        if keyed:
            lab = cells[0] if not cells[0].isdigit() else f"{cells[0]}番"
            out[(sec, lab)] = int(keyed.group(1))
    return out


def choukai_printed_options(ct: str, bi) -> dict[tuple[int, str], dict[int, str]]:
    """問題1/2 printed option lists, from the booklet body only."""
    cut = bi.KEY_HEADING.search(ct)
    body = ct[:cut.start()] if cut else ct
    out: dict[tuple[int, str], dict[int, str]] = collections.defaultdict(dict)
    sec = item = None
    for line in body.splitlines():
        head = re.match(r"^#+\s*問題([1-5])", line)
        if head:
            sec, item = int(head.group(1)), None
            continue
        lab = re.match(r"^\*\*(例|\d+番)\*\*", line)
        if lab:
            item = lab.group(1)
            continue
        opt = re.match(r"^\s*([1-4])[.．、]\s*(.+?)\s*$", line)
        if opt and sec and item:
            out[(sec, item)][int(opt.group(1))] = opt.group(2)
    return out


def choukai_span(script_text: str, n: int) -> str:
    parts = re.split(rf"^問題{n}。$", script_text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    return (re.split(rf"^問題{n + 1}。$", parts[1], maxsplit=1, flags=re.M)[0]
            if n < 5 else parts[1])


def choukai_item_blocks(span: str, m, scored_only: bool = False) -> list[list[str]]:
    out = []
    for block in re.split(r"\n\s*\n", span):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines or not m.ITEM_RE.match(lines[0]):
            continue
        if scored_only and lines[0].startswith("例。"):
            continue
        out.append(lines)
    return out


def spoken_choices(lines: list[str], top: int = 4) -> dict[int, str]:
    hits = (re.match(rf"^([1-{top}])、(.+?)。?$", l) for l in lines)
    return {int(h.group(1)): h.group(2) for h in hits if h}


def p3_talk_chars(lines: list[str]) -> int:
    """Spoken characters of a 問題3 talk: no lead-in, no choices, no question."""
    body = []
    for line in lines[1:]:
        if re.match(r"^[1-4]、", line) or "何について" in line:
            continue
        body.append(re.sub(r"^[^\s:：]{1,6}[:：]", "", line))
    return len(re.sub(r"\s", "", "".join(body)))


def check_choukai_key_duplication(test_id: str, ct: str, st: str, m, bi):
    """No two items in one section may be keyed to the same thing (G16)."""
    keys, printed = choukai_key_table(ct, bi), choukai_printed_options(ct, bi)
    name = f"{test_id}: no two 聴解 items in a section share a key"
    dup, seen_any = [], 0
    for sec in (1, 2, 3):
        if sec == 3:
            src = {choukai_item_label(l[0]): spoken_choices(l)
                   for l in choukai_item_blocks(choukai_span(st, 3), m, True)}
        else:
            src = {lab: o for (s, lab), o in printed.items()
                   if s == sec and lab != "例"}
        first: dict[str, str] = {}
        for lab, opts in src.items():
            keyed = keys.get((sec, lab))
            if not keyed or keyed not in opts:
                continue
            seen_any += 1
            norm = re.sub(r"[\s。、・]", "", opts[keyed])
            if norm in first:
                dup.append(f"問題{sec}-{first[norm]}と{lab} both keyed "
                           f"「{opts[keyed]}」")
            first[norm] = lab
    if not seen_any:
        return skip(name, "no key column this gate can pair with an option list")
    _gated(test_id, f"{name} ({seen_any} keys compared)", not dup,
           "; ".join(dup) + " — the second item tests nothing the first did not. "
           "Rewrite one item's task (choukai-items.md §'Write the SECTION TABLE')")


def check_choukai_countable_mix(test_id: str, ct: str, st: str, m, bi):
    """The section-mix rules a regex can decide (G16)."""
    keys = choukai_key_table(ct, bi)
    bad = []

    p3 = choukai_item_blocks(choukai_span(st, 3), m, True)
    suffixed = [f"{choukai_item_label(l[0])}-{n}" for l in p3
                for n, t in spoken_choices(l).items() if t.endswith("について")]
    if len(suffixed) > 2:
        bad.append(f"問題3: {len(suffixed)} options suffixed 「〜について」, official "
                   f"8 of 685 — write the bare noun phrase (一人旅をするよさ)")
    short = [f"{choukai_item_label(l[0])}={p3_talk_chars(l)}" for l in p3
             if p3_talk_chars(l) < P3_TALK_FLOOR]
    if short:
        bad.append(f"問題3: talk shorter than any of the archive's 149 — "
                   f"{', '.join(short)} chars, official median 305 / p10 251 / "
                   f"min 177, target {P3_TALK_TARGET}+")

    p4 = choukai_item_blocks(choukai_span(st, 4), m, True)
    done, akey = [], []
    for lines in p4:
        lab = choukai_item_label(lines[0])
        opts = spoken_choices(lines, top=3)
        keyed = keys.get((4, lab))
        if any(ALREADY_DONE_RE.search(t) for n, t in opts.items() if n != keyed):
            done.append(lab)
        if keyed in opts and opts[keyed].startswith("あ"):
            akey.append(lab)
    if len(done) > 3:
        bad.append(f"問題4: {len(done)} of {len(p4)} items carry an already-done "
                   f"(もう/すでに/さっき) distractor ({', '.join(done)}), official "
                   f"median 1 max 3 — the shape becomes the key")

    p5 = choukai_item_blocks(choukai_span(st, 5), m)
    voices = []
    for lines in p5:
        labs = {h.group(1) for h in (m.SPEAKER_RE.match(l) for l in lines)
                if h and h.group(1) in m.SPEAKER_MAP}
        voices.append((choukai_item_label(lines[0]), sorted(labs)))
    if voices and not any(len(v) >= 3 for _, v in voices):
        bad.append("問題5: no item has 3+ speakers (" +
                   "; ".join(f"{lab} {v}" for lab, v in voices) +
                   "), against 31/31 sittings — 統合理解 is 2人以上の意見を整理; "
                   "cast 男1+男2+女 (choukai-items.md §統合理解)")

    _gated(test_id, f"{test_id}: 聴解 section mix inside the archive's range",
           not bad, " ⁄ ".join(bad))


def check_choukai_same_speaker_lines(test_id: str, st: str, m):
    """One turn is one line — no two consecutive lines share a label (G16)."""
    bad, prev = [], None
    for line in st.splitlines():
        hit = m.SPEAKER_RE.match(line.strip())
        lab = hit.group(1) if hit and hit.group(1) in m.SPEAKER_MAP else None
        if lab and lab == prev:
            bad.append(f"{lab}:{hit.group(2).strip()[:20]}…")
        prev = lab
    _gated(test_id, f"{test_id}: 聴解 script has no split turns", not bad,
           f"{len(bad)} line(s) repeat the previous speaker — " +
           "; ".join(f"「{b}」" for b in bad[:4]) +
           ". One turn is one line: a split turn buys a 0.9 s turn gap where "
           "official has a 0.40 s within-turn pause, and inflates the "
           "reaction-turn rate without adding a reaction — only the OTHER "
           "speaker's turn counts (choukai-audio §'Block conventions')")


def check_choukai_section_table(test_id: str, ct: str, bi):
    """The セクション構成表 exists and covers every scored item (G16)."""
    name = f"{test_id}: 聴解.md carries the セクション構成表"
    cut = bi.KEY_HEADING.search(ct)
    tail = ct[cut.start():] if cut else ct
    head = re.search(r"^#+\s*セクション構成表", tail, re.M)
    if not head:
        return _gated(test_id, name, False,
                      "no セクション構成表 heading — one row per item "
                      "(場面 / 主導 / 正解 / 消去方法 / 質問型), after the answer-key "
                      "heading. QA reads its columns first "
                      "(choukai-items.md §'Write the SECTION TABLE')")
    rows = {c.strip() for line in tail[head.start():].splitlines()
            if line.lstrip().startswith("|")
            for c in [line.split("|")[1]] if CHOUKAI_ITEM_LABEL.match(c.strip())}
    rows |= {f"{r}番" for r in rows if r.isdigit()}
    want = {lab for (_, lab) in choukai_key_table(ct, bi) if lab != "例"}
    missing = sorted(want - rows)
    _gated(test_id, f"{name} ({len(rows & want)}/{len(want)} items)",
           not missing, f"no row for {missing[:8]} — a partial table audits a "
           f"partial section")


# G17. THE WRITING. G15 counts how often people react, G16 how the section is
# built; this is the sentences themselves, measured against the three Shin Kanzen
# 実力養成編 chapters that name what N2 listening tests
# (official_register.md §7.6). Two of the four findings are gateable:
#
#   縮約形 per 10 k spoken chars   official 37.3 [22.4-67.4] n=31   ours 0.0-23.9
#   keyed 問題1/2 option is a       (not measurable on official:     ours 75 %
#     verbatim token-match          their options are kana-leaning)
#
# The other two are recorded and NOT gated, on purpose. 問題4 question-replies:
# official's per-sitting range is 0-15, so a threshold at the archive minimum is
# 0 and catches nothing. Option kanji ratio: only 2-6 of 31 booklet.md extracts
# expose their listening option blocks, so no per-sitting distribution exists to
# threshold against. Inventing either number would be the exact failure this file
# keeps a §7.1 about.
CONTRACTION_MIN = 22.4          # the archive MINIMUM, not its median (37.3)
KEY_VERBATIM_MAX = 0.50         # design threshold — see the note above


def check_choukai_contractions(test_id: str, st: str, m):
    """Dialogue is spoken Japanese, not written Japanese (G17)."""
    spoken = "".join(h.group(2) for h in
                     (m.SPEAKER_RE.match(l.strip()) for l in st.splitlines())
                     if h and h.group(1) in m.SPEAKER_MAP)
    if not spoken:
        return skip(f"{test_id}: 聴解 dialogue contracts like speech", "no turns")
    rate = 10000 * len(CONTRACTION_RE.findall(spoken)) / len(spoken)
    warn(f"{test_id}: 聴解 dialogue contracts like speech ({rate:.1f}/10k)",
         rate >= CONTRACTION_MIN,
         f"official runs {CONTRACTION_MIN}-67.4 with a median of 37.3, in 31/31 "
         f"sittings; seven of the eight papers on disk sit BELOW the archive "
         f"minimum and one contains no contracted form at all. 〜てる/〜とく/"
         f"〜ちゃう/〜なきゃ are the first chapter of Shin Kanzen's 実力養成編 "
         f"(p.16) because parsing them IS the tested skill — a script written in "
         f"「〜ています」「〜ておきます」「〜なければなりません」 stops testing it. Keigo "
         f"is no excuse: official service-counter items still measure 37.5 "
         f"(choukai-audio §Register rule 3)")


def check_choukai_key_paraphrase(test_id: str, ct: str, st: str, m, bi):
    """A keyed option restates the deciding line; it does not copy it (G17).

    KNOWN BLIND SPOT (found 2026-08-18): tokens require 2+ kanji or 3+
    katakana chars, so a key written mostly in hiragana (a verb reused as its
    own kana spelling, e.g. 説明する -> せつめいする) yields zero tokens and
    silently skips this check entirely — `total` never counts it. A key can
    also dodge a match by swapping only the register of ONE katakana word
    (スマホ -> スマートフォン) while keeping the deciding verb (見せる)
    unchanged. Neither is caught here; both are real, shipped defects — see
    choukai-items.md §'The 解説 QUOTES the script; the OPTION restates it'.
    This gate is a coarse WARN, not proof of a genuine paraphrase.
    """
    keys, printed = choukai_key_table(ct, bi), choukai_printed_options(ct, bi)
    verbatim, total = [], 0
    # 問題2 ONLY. 言い換え is Shin Kanzen's ポイント理解 chapter (IV-2), and
    # 課題理解 keys legitimately reuse the script's words — official 7/2025
    # 問題1 keys 「本のデータをとうろくする」 against 「本のデータを登録してくれる？」,
    # 「当日のしりょうをいんさつする」 against 「当日配る資料の印刷は」. In 問題1 the
    # discrimination is WHICH action and WHEN, not vocabulary, so scoring it for
    # paraphrase would flag the official paper. Caught while authoring against
    # this check's first draft, which covered 問題1 and 問題2 together.
    for sec in (2,):
        blocks = {choukai_item_label(l[0]): "".join(l)
                  for l in choukai_item_blocks(choukai_span(st, sec), m, True)}
        for (s, lab), opts in printed.items():
            if s != sec or lab == "例" or lab not in blocks:
                continue
            keyed = keys.get((sec, lab))
            if not keyed or keyed not in opts:
                continue
            tokens = set(re.findall(r"[一-鿿]{2,}|[゠-ヿ]{3,}", opts[keyed]))
            if not tokens:
                continue
            total += 1
            if all(t in blocks[lab] for t in tokens):
                verbatim.append(f"問題{sec}-{lab}「{opts[keyed]}」")
    if not total:
        return skip(f"{test_id}: 聴解 keys paraphrase the script",
                    "no key/option pair this gate can compare")
    share = len(verbatim) / total
    warn(f"{test_id}: 聴解 keys paraphrase the script "
         f"({len(verbatim)}/{total} are verbatim token-matches)",
         share <= KEY_VERBATIM_MAX,
         "; ".join(verbatim[:4]) + f" — every content word of these keys is "
         f"already in their own dialogue, so the item is answerable by catching "
         f"one noun. Shin Kanzen IV-2 (p.52): 「選択肢では、話の中の長い説明を、別の"
         f"言い方で簡単に短くまとめている」. Swap one content word for its result or "
         f"category, or merge two speakers' turns into one option. The 解説 still "
         f"quotes the script verbatim — quotable is not copyable. Threshold "
         f"{KEY_VERBATIM_MAX:.0%} is a DESIGN choice, not a measured band: "
         f"official options are kana-leaning, so token-matching them against a "
         f"kanji script would understate their overlap "
         f"(choukai-items.md §'The 解説 QUOTES the script')")


# 聴解 keys carry no length information (G16). Measured 2026-08-18 after the
# user reported "it tends to make the longer key the correct answer": across the
# 11 papers on disk the key was the UNIQUELY LONGEST of its options in 52 % of
# 問題1, 72 % of 問題2, 60 % of 問題3, 50 % of 問題4 (3 options) and 45 % of
# 問題5 — so a candidate who understood nothing, read the printed 問題1/2 lists
# and always marked the longest line scored better than one who understood half
# the audio. 問題2 at 72 % is the worst surface this repo has shipped.
#
# The official archive, measured the same way over 460 length-varying items in
# 31 sittings (問題1/2 printed options from booklet.md, 問題3/4 spoken options
# from script.md): 28 % uniquely longest, and the key's length divided by its
# distractors' mean is 1.00 at the median — official keys are AVERAGE length.
# Per-sitting rate over the six sittings with >=20 parsed items: 13/20/24/24/26/29 %.
# Ours ran 1.24 (問題1) to 1.36 (問題2).
#
# The defect is NOT that our options vary in length — official varies MORE
# (median max/min 2.55 in 問題1, against a 読解 rule of 1.30). It is that the
# length varies WITH correctness, because the key was written as a full
# proposition while its distractors were left as short topic labels:
# 20260812_2 問題2-2番 keyed 「雨の日は車がなかなかつかまらないこと」 (18 JP chars)
# against 「料金の見方」(5) / 「クーポンの使い方」(8) / 「支払い方法の登録」(8).
# So this gate measures rank, never spread, and the repair is to raise the
# DISTRACTORS to the key's grammatical shape (choukai-items.md §'Key length
# carries no information'), not to trim every option to one size.
#
# Strictly-longest, not (tied-)longest as check_dokkai_longest_key_rate counts:
# 聴解 options are short enough that all-four-equal sets are common (they are
# excluded here as carrying no signal), and a tie does not hand the item to
# "mark the longest". The two baselines land in the same place anyway — 28 %
# here against 読解's 29 %, so the 35 % ceiling is the same number.
CHOUKAI_LONGEST_KEY_MAX = 0.35
CHOUKAI_KEY_RATIO_MAX = 1.15    # WARN: median key/distractor-mean; official 1.00

# Pre-rule papers: every paper on disk failed this the day it was written, so
# the gate would have nothing to protect if it failed them all. Each id comes
# off this list as its 聴解 is repaired; the set must reach empty.
CHOUKAI_LENGTH_GRANDFATHERED: set[str] = set()


def choukai_all_option_sets(ct: str, st: str, m, bi) -> dict[tuple[int, str], dict[int, str]]:
    """Every keyable 聴解 option list: 問題1/2 printed, 問題3/4/5 spoken.

    One dict so the length gate measures the whole section the way a candidate
    meets it, rather than one 問題 at a time (n=5 or 6 per section is too small
    to separate a real bias from noise — the whole section is ~27 items).
    """
    out: dict[tuple[int, str], dict[int, str]] = {}
    out.update(choukai_printed_options(ct, bi))
    for sec, top in ((3, 4), (4, 3), (5, 4)):
        for lines in choukai_item_blocks(choukai_span(st, sec), m, True):
            ch = spoken_choices(lines, top)
            if len(ch) == top:
                out[(sec, choukai_item_label(lines[0]))] = ch
    return out


def check_choukai_longest_key_rate(test_id: str, ct: str, st: str, m, bi):
    """The key must not be findable by length alone, in any 聴解 section (G16)."""
    keys = choukai_key_table(ct, bi)
    opts = choukai_all_option_sets(ct, st, m, bi)
    n = n_longest = 0
    worst: list[str] = []
    ratios: list[float] = []
    for (sec, label), a in sorted(keys.items()):
        om = opts.get((sec, label))
        # 問題5-2番 reads ONE list under both 質問 — the key table has two rows
        # for it and both point at that list, which is correct, not a duplicate.
        if not om:
            continue
        lens = [jp_char_count(om[i]) for i in sorted(om)]
        if a not in om or len(set(lens)) < 2:
            continue          # all-equal sets carry no length signal at all
        n += 1
        kl = lens[a - 1]
        others = [l for i, l in enumerate(lens, 1) if i != a]
        ratios.append(kl / (sum(others) / len(others)))
        if kl == max(lens) and lens.count(kl) == 1:
            n_longest += 1
            worst.append(f"問題{sec}-{label}(key {kl} vs {sorted(others)})")
    if n == 0:
        return skip(f"{test_id}: 聴解 longest-key rate", "no keyed 聴解 option list")
    rate = n_longest / n
    med = statistics.median(ratios)
    name = (f"{test_id}: 聴解 key is not findable by length "
            f"({n_longest}/{n} = {rate:.0%} uniquely longest, target <= 35%)")
    detail = (f"{n_longest} of {n} length-varying 聴解 items ({rate:.0%}) key the "
              f"UNIQUELY LONGEST option: {', '.join(worst[:8])}"
              f"{' …' if len(worst) > 8 else ''} — official is 28% over 460 items "
              f"in 31 sittings, per-sitting 13–29%. Raise the DISTRACTORS to the "
              f"key's grammatical shape and specificity (a full proposition, not a "
              f"topic label), harvested from the script and grounded in the 解説 "
              f"cell; do not trim all four to one length — official option spread "
              f"is WIDER than ours (choukai-items.md §'Key length carries no "
              f"information')")
    if test_id in CHOUKAI_LENGTH_GRANDFATHERED:
        warn(name, rate <= CHOUKAI_LONGEST_KEY_MAX, detail + GRANDFATHER_NOTE)
    else:
        check(name, rate <= CHOUKAI_LONGEST_KEY_MAX, detail)
    warn(f"{test_id}: 聴解 keyed option is average length "
         f"(median key/distractor-mean {med:.2f}, official 1.00)",
         med <= CHOUKAI_KEY_RATIO_MAX,
         f"the median 聴解 key is {med:.2f}x its distractors' mean length over "
         f"{n} items — official sits at 1.00, i.e. the key is neither longer nor "
         f"shorter than what surrounds it. A rate under 35% with a ratio this "
         f"high means the key is still habitually long, just not quite top rank "
         f"(choukai-items.md §'Key length carries no information')")


# 模範解答 explains the options the candidate actually saw (G18). 詳細解説.json stores its
# own copy of every option's text — hand-authored, furigana included — and
# build_model_answer.py PREFERS that copy over the one it parses out of the booklet
# (`detail.get("options") or raw_q.get("options")`). So when an option is rewritten in
# 言語知識・読解.md or 聴解.md and the JSON is not updated, 模範解答.html keeps explaining
# the OLD wording: the answer document and the exam disagree, and nothing said so.
#
# Measured 2026-08-18 while repairing the longest-key bias: 722 of the ~1100 stored
# options were ALREADY stale at HEAD, before that pass touched anything — every paper
# affected, up to 138 in one. Two separate defects hide in there: an explanation that
# argues against wording the booklet no longer has, and a 選択肢 list in 模範解答.html
# that a candidate cannot match to the paper they just sat.
#
# There is no way to catch this by reading either file alone, which is why it rotted for
# as long as it did. Trailing 。 is normalized: 問題5's spoken labels carry it in the
# script and not in the stored option, and that difference is not drift.
def check_model_answer_option_sync(test_id: str, gt: str, ct: str, st: str, m, bi):
    path = ROOT / "tests" / test_id / "詳細解説.json"
    if not path.is_file():
        return skip(f"{test_id}: 詳細解説.json options match the booklet",
                    "no 詳細解説.json (run make scaffold-explanations)")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return check(f"{test_id}: 詳細解説.json parses", False, str(e))
    gopts = gengo_option_sets(gt, bi)
    copts = choukai_all_option_sets(ct, st, m, bi)

    def norm(x: str) -> str:
        return re.sub(r"《[^》]*》", "", x).strip().rstrip("。")

    stale, compared = [], 0
    for key, entry in sorted(data.items()):
        stored = entry.get("options") if isinstance(entry, dict) else None
        if not stored:
            continue
        if key.isdigit():
            src = gopts.get(int(key))
        else:
            mm = re.match(r"^問([1-5])-(.+)$", key)
            if not mm:
                continue
            label = mm.group(2)
            if not (label.startswith("例") or label.endswith("番")):
                label += "番"
            om = copts.get((int(mm.group(1)), label))
            src = [om[i] for i in sorted(om)] if om else None
        if not src or len(src) != len(stored):
            continue
        compared += 1
        for i, (a, b) in enumerate(zip(stored, src), 1):
            if norm(a) != norm(b):
                stale.append(f"{key}-{i}(模範解答「{norm(a)[:24]}」vs 問題冊子「{norm(b)[:24]}」)")
    if not compared:
        return skip(f"{test_id}: 詳細解説.json options match the booklet",
                    "no option list could be paired with the booklet")
    check(f"{test_id}: 詳細解説.json options match the booklet ({compared} items)",
          not stale,
          f"{len(stale)} stored option(s) differ from the printed paper: "
          f"{'; '.join(stale[:5])}{' …' if len(stale) > 5 else ''} — build_model_answer.py "
          f"prefers the STORED text, so 模範解答.html is explaining wording this test does "
          f"not contain. Re-sync the `options` arrays (and any 解説 prose quoting them) "
          f"whenever an option is rewritten (exam-model-answer)")


# 文字・語彙 keys carry no length information either (G18). The same 2026-08-18 sweep
# found the tell in a third place, measured against the archive's own 問題4/5/6 (parsed
# from booklet.md), counting only items whose four options are not all the same length:
#
#              official          ours (before)
#   問題4        4 % (n=194)      21 %   <- already below the 25 % chance line
#   問題5       15 % (n=123)      36 %
#   問題6       16 % (n=124)      31 %
#
# 問題4 is excluded from the gate on purpose: single-word 文脈規定 options are near-equal
# by construction, ours already sits under chance, and official's 4 % is a property of
# same-part-of-speech word sets rather than a fairness rule — gating it would push
# authors to pad words. 問題5/6 are gated together (10 items a paper; each alone is too
# small to separate habit from noise) at 30 %, against a 15–16 % official baseline.
#
# The cause was the shape this repo now names in choukai-items.md: in 問題5 the key was
# written as a PHRASE while its distractors stayed bare single words — 20260810_1 keyed
# 「一般の人々」 against 専門家 / 関係者 / 会員, and 20260810_2 keyed 「細かく切って」
# against 茹でて / 焼いて / 煮て. Raise the distractors to the key's grain.
MOJI_LONGEST_KEY_MAX = 0.30


def check_moji_longest_key_rate(test_id: str, gt: str, keys: dict[int, int], bi):
    opts = gengo_option_sets(gt, bi)
    n = n_longest = 0
    worst = []
    for q in list(range(23, 28)) + list(range(28, 33)):   # 問題5 + 問題6
        a, o = keys.get(q), opts.get(q) or []
        if a is None or len(o) != 4 or not 1 <= a <= 4:
            continue
        lens = [jp_char_count(x) for x in o]
        if len(set(lens)) < 2:
            continue
        n += 1
        if lens[a - 1] == max(lens) and lens.count(max(lens)) == 1:
            n_longest += 1
            worst.append(f"問{q}({lens[a-1]} vs {sorted(l for i,l in enumerate(lens,1) if i!=a)})")
    if n == 0:
        return skip(f"{test_id}: 問題5/6 longest-key rate", "no length-varying items")
    rate = n_longest / n
    check(f"{test_id}: 問題5/6 key is not the longest option "
          f"({n_longest}/{n} = {rate:.0%}, official 15–16%, target <= 30%)",
          rate <= MOJI_LONGEST_KEY_MAX,
          f"{n_longest} of {n} length-varying 問題5/6 items ({rate:.0%}) key the uniquely "
          f"longest option: {', '.join(worst[:6])}{' …' if len(worst) > 6 else ''} — "
          f"official is 15% (問題5, n=123) and 16% (問題6, n=124) over 31 sittings. In 問題5 "
          f"this is usually a PHRASE key against bare single-word distractors; give all "
          f"four the same grain (question-authoring/references/moji-goi.md)")


def check_choukai_judgment_mix(test_id: str, st: str, ct: str, m, bi):
    """The mix rules only a human can settle — WARN, and QA owns them (G16)."""
    keys = choukai_key_table(ct, bi)
    out = []

    p1 = choukai_item_blocks(choukai_span(st, 1), m, True)
    counter = [choukai_item_label(l[0]) for l in p1 if COUNTER_RE.search(l[0])]
    if len(counter) > 2:
        out.append(f"問題1: {len(counter)} of {len(p1)} items at a service counter "
                   f"({', '.join(counter)}), official 6 % (9/153) — official 問題1 "
                   f"is someone ASSIGNING work")

    shapes = collections.Counter()
    for lines in choukai_item_blocks(choukai_span(st, 2), m, True):
        q = lines[-1]
        shapes["理由" if re.search(r"どうして|理由|なぜ", q) else
               "一番/優先" if re.search(r"一番|最も|優先", q) else
               "どのように" if re.search(r"どのように|どんな", q) else "何/どれ"] += 1
    if shapes["一番/優先"] > 2:
        out.append(f"問題2: {shapes['一番/優先']} items keyed by 「一番/優先」, "
                   f"official 6 % (8/141) — one answer-marking device doing the "
                   f"whole section")
    if shapes["理由"] < 2:
        out.append(f"問題2: {shapes['理由']} 理由 (どうして) item(s) — official 37 % "
                   f"(52/141), the section's largest class")

    p3 = choukai_item_blocks(choukai_span(st, 3), m, True)
    talks = [choukai_item_label(l[0]) for l in p3 if BROADCAST_RE.search(l[0])]
    if len(talks) < 3:
        out.append(f"問題3: only {len(talks)} of {len(p3)} items are a broadcast, "
                   f"lecture or interview — the rest are procedure "
                   f"announcements, i.e. 課題理解 content in a 概要理解 slot")

    akey = [choukai_item_label(l[0]) for l in
            choukai_item_blocks(choukai_span(st, 4), m, True)
            if (lambda o, k: k in o and o[k].startswith("あ"))(
                spoken_choices(l, top=3), keys.get((4, choukai_item_label(l[0]))))]
    if len(akey) > 2:
        out.append(f"問題4: {len(akey)} keyed replies open with 「あ」 "
                   f"({', '.join(akey)}) — a shared opener on the KEY is a shape "
                   f"to sort by (no measured band: official keys are not in the "
                   f"extracts, so judge it)")

    span = "\n".join(l for l in choukai_span(st, 1).splitlines()
                     if not re.search(r"何をしますか|何をしなければ|まず何", l))
    rate = span.count("まず") / max(len(span) / 10000, 1e-9)
    if rate > 19:
        out.append(f"問題1: 「まず」 {rate:.1f} per 10 k inside the dialogue, "
                   f"official median 5.5 max 19.1 — it marks the answer; order "
                   f"tasks by content (その前に / 〜が終わったら)")

    warn(f"{test_id}: 聴解 section mix (judgment calls)", not out,
         " ⁄ ".join(out) + " — quotas in choukai-items.md §'Section item mix'; no "
         "regex settles these, so resolve or explain each and read the "
         "セクション構成表's columns (exam-qa-review §4)")


def check_voice_casting(script_text: str, m, origin: str, test_id: str = ""):
    """Narration gender must agree with the voice SPEAKER_MAP will synthesize (G14)."""
    mismatch, indistinct = [], []
    for block in re.split(r"\n\s*\n", script_text):
        lines = [ln for ln in block.strip().splitlines() if ln.strip()]
        if not lines or not m.ITEM_RE.match(lines[0]):
            continue
        labels: list[str] = []
        for ln in lines:
            hit = m.SPEAKER_RE.match(ln)
            if hit and hit.group(1) in m.SPEAKER_MAP and hit.group(1) not in labels:
                labels.append(hit.group(1))
        for lab in labels:
            gender = "男" if m.SPEAKER_MAP[lab]["voice"] == m.MALE else "女"
            other = "女" if gender == "男" else "男"
            if re.search(rf"{re.escape(lab)}の{other}の人", block):
                mismatch.append(f"{lines[0][:8]} 「{lab}の{other}の人」 but "
                                f"SPEAKER_MAP casts {lab} as {gender}")
        # Same voice at a near-identical rate makes two speakers one person to
        # the ear. Only TWO-PARTY items are decidable here: edge-tts ships two
        # ja-JP voices, so a three-speaker item (問題5's 夫/妻/店員) MUST reuse
        # one, and official 問題5 casts same-gender pairs too — flagging those
        # would reject the reference paper.
        indistinct_pairs = []
        if len(labels) == 2:
            l1, l2 = labels
            v1, v2 = m.SPEAKER_MAP[l1]["voice"], m.SPEAKER_MAP[l2]["voice"]
            r1 = num(m.SPEAKER_MAP[l1].get("rate", "0")) if "rate" in m.SPEAKER_MAP[l1] else 0.0
            r2 = num(m.SPEAKER_MAP[l2].get("rate", "0")) if "rate" in m.SPEAKER_MAP[l2] else 0.0
            # Identity comes from PITCH, not rate (choukai-audio §voices):
            # 女(+0Hz)/職員(-14Hz)/係員(+18Hz) share NanamiNeural yet are
            # distinct people to the ear. Ignoring pitch made this line warn
            # on every such sanctioned pair — adjudicated GATE-WRONG in
            # qa/qa-report-20260811_1.md §6.
            p1 = num(m.SPEAKER_MAP[l1].get("pitch", "0")) if "pitch" in m.SPEAKER_MAP[l1] else 0.0
            p2 = num(m.SPEAKER_MAP[l2].get("pitch", "0")) if "pitch" in m.SPEAKER_MAP[l2] else 0.0
            if v1 == v2 and abs(r1 - r2) < 10 and abs(p1 - p2) < 10:
                indistinct_pairs.append(f"{l1}/{l2}")
        if indistinct_pairs:
            indistinct.append(f"{lines[0][:8]} {indistinct_pairs}")
    check(f"{test_id}: 聴解 narration gender matches SPEAKER_MAP's voice",
          not mismatch,
          "; ".join(mismatch) + " — rename the speaker or recast it in "
          "choukai-audio's SPEAKER_MAP; the audio and the booklet "
          "must describe the same person")
    if origin == "generated":
        warn(f"{test_id}: 聴解 item speaker pairs cast distinguishable voices",
             not indistinct,
             "; ".join(indistinct) + " — speaker labels resolve to one voice or near-identical rate; "
             "prefer contrasting voices (choukai-audio)")


def check_artifact_freshness(d):
    """Deliverables must carry the sha of the source they were built from (G4).

    Rebuilding a script without regenerating MP3 results in papers speaking superseded
    問題N instructions. mtimes cannot see this (they are checkout-unstable), so
    make_choukai_mp3.py stamps `script_sha` into 聴解_チャプター.json and
    build_booklet.py stamps `<!-- src_sha: <name>=<sha> -->` into every HTML.

    An external MP3 has no TTS timeline to stamp (write_external_chapters.py
    writes `source: external`), so the audio half is skipped for it — that is
    the one exemption, and it is why the check passes an imported paper whose
    MP3 came from the source sitting rather than from edge-tts.
    """
    script = d / "聴解スクリプト.txt"
    chapters = d / "聴解_チャプター.json"
    if script.is_file() and chapters.is_file():
        try:
            data = json.loads(chapters.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            data = {}
            check("聴解_チャプター.json parses", False, str(e))
        want = hashlib.sha1(script.read_bytes()).hexdigest()[:12]
        if data.get("source") == "external":
            skip(f"{d.name}: 聴解.mp3 was built from today's 聴解スクリプト.txt",
                 "external MP3 (no TTS timeline to stamp)")
        else:
            got = data.get("script_sha")
            check(f"{d.name}: 聴解.mp3 was built from today's "
                  f"聴解スクリプト.txt (script_sha {want})", got == want,
                  f"聴解_チャプター.json records {got!r} — run `make mp3 {d.name}`; "
                  f"the shipped audio speaks a superseded script "
                  f"(jlpt-test-generation Invariants)")
            # …and with today's PACING. script_sha covers the words only: three
            # documented gaps (問題4 inter-reply, 問題1/2 repeat-of-question, the
            # 例 answer pause) were wrong in the code for the whole life of the
            # eight papers, and fixing them leaves every MP3 stale with nothing
            # else to show it — the constants are not in the script bytes.
            mk = load(".agents/choukai-audio/scripts/make_choukai_mp3.py")
            want_p, got_p = mk.pacing_sha(), data.get("pacing_sha")
            check(f"{d.name}: 聴解.mp3 was built with today's pacing "
                  f"(pacing_sha {want_p})", got_p == want_p,
                  f"聴解_チャプター.json records {got_p!r} — run `make mp3 "
                  f"{d.name}`; the audio is timed by superseded constants "
                  f"(choukai-audio Part 3 §script_sha)")

    # HTML: WARN on a missing stamp (no built HTML carries one yet — the rebuild
    # belongs to the paper-repair pass), FAIL when a stamp is present and stale.
    stale, unstamped = [], []
    # 解答.html embeds 聴解_チャプター.json VERBATIM for its chapter dropdown, so a
    # rebuilt MP3 leaves the sheet seeking to the previous build's offsets — the
    # 2026-08-13 pacing fixes moved every offset in all eight papers. The three
    # Markdown/script stamps could not see it, because none of those files
    # changed. Stamping the chapter JSON as a fourth source makes `make sheet`
    # mandatory after `make mp3`, which it always was in fact.
    html_sources = {"言語知識・読解.html": ["言語知識・読解.md"],
                    "聴解.html": ["聴解.md"],
                    "解答.html": ["言語知識・読解.md", "聴解.md", "聴解スクリプト.txt",
                                  "聴解_チャプター.json"]}
    for html_name, srcs in html_sources.items():
        page = d / html_name
        if not page.is_file():
            continue
        stamps = dict(re.findall(r"<!-- src_sha: (.+?)=([0-9a-f]{12}) -->",
                                 page.read_text(encoding="utf-8")))
        for src_name in srcs:
            src = d / src_name
            if not src.is_file():
                continue
            want = hashlib.sha1(src.read_bytes()).hexdigest()[:12]
            if src_name not in stamps:
                unstamped.append(f"{html_name}←{src_name}")
            elif stamps[src_name] != want:
                stale.append(f"{html_name} records {src_name}={stamps[src_name]}, "
                             f"source is {want}")
    check(f"{d.name}: built HTML matches the Markdown it stamps", not stale,
          "; ".join(stale) + " — run `make booklet` and `make sheet`; the "
          "Markdown is the single source of truth (exam-app)")
    warn(f"{d.name}: built HTML records its source sha", not unstamped,
         f"{len(unstamped)} stamp(s) missing ({unstamped[:3]}…) — rebuild with "
         f"`make booklet {d.name} && make sheet {d.name}` to stamp them "
         f"(exam-app)")


# Cross-test reuse (G15). Apparatus and 例 dialogues carried over verbatim:
# avoid byte-identical 例 blocks across generated tests or from official papers.
# Only a GENERATED test can be at fault — the import reproduces an outside source.
def test_note_lines(gt: str) -> set[str]:
    return {unicodedata.normalize("NFKC", ln.strip()) for ln in gt.splitlines() if NOTE_DEF.match(ln)}


def test_example_blocks(st: str) -> set[str]:
    return {unicodedata.normalize("NFKC", b.strip()) for b in re.split(r"\n\s*\n", st) if b.strip().startswith("例。")}


def test_choukai_example_options(ct: str) -> set[str]:
    opts = set()
    lines = ct.splitlines()
    for i, line in enumerate(lines):
        if "**例**" in line or "例" in line:
            for nxt in lines[i:i + 10]:
                for m in re.finditer(r"[1-4]\.\s*([^\s|]+)", nxt):
                    opt = m.group(1).strip()
                    if len(opt) >= 6:
                        opts.add(unicodedata.normalize("NFKC", opt))
    return opts


def check_cross_test_reuse(name: str, mine: dict, others: dict[str, dict]):
    for kind, label, fix in (
            ("notes", "（注N） definition line",
             "rewrite the gloss for THIS passage — avoid copying glosses from another test"),
            ("examples", "例。block",
             "author a fresh 例 dialogue (choukai-audio); avoid copying 例 dialogues from reference papers"),
            ("choukai_options", "聴解 例 option line",
             "author fresh 例 booklet options (choukai-audio)")):
        shared = []
        for other, data in others.items():
            if kind in mine and kind in data:
                for dup in sorted(mine[kind] & data[kind]):
                    shared.append(f"{str(dup)[:34]}… also in {other}")
        check(f"{name}: no {label} is byte-identical to another test's", not shared,
              "; ".join(shared[:4]) + f" — {fix}")


EXAMPLE_PREMARK = re.compile(r"\*\*[（(]([1-4])[)）]\*\*")


def check_example_premarks(ct: str, st: str, bi):
    """The 例 the marksheet pre-marks must be the answer the announcer declares.

    問題1-4 each open with a practice 例 whose answer the script announces
    (「最もよいものは◯番です…答えはこのように書きます」) while the booklet's
    answer grid shows that same number pre-marked — one demonstration, seen and
    heard together. Generated papers have shipped grids pre-marking a
    different number than the announcement (in 問題3 and in 問題4); nothing
    caught it because 例 rows are not among the 30 scored keys.
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
            # horizontal grid (an earlier layout convention): 例 is a column
            # header; its bubbles sit in the first cell of the next data row.
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


BANNED_COLLOCATIONS_PATH = (
    AGENTS / "question-authoring" / "references" / "banned_collocations.txt"
)


def check_banned_collocations(d, gt: str, ct: str, st: str, origin: str):
    if origin != "generated" or not BANNED_COLLOCATIONS_PATH.is_file():
        return
    banned = [ln.split("#")[0].strip() for ln in BANNED_COLLOCATIONS_PATH.read_text(encoding="utf-8").splitlines()
              if ln.strip() and not ln.strip().startswith("#")]
    found = []
    text = gt + "\n" + ct + "\n" + (st or "")
    for b in banned:
        if b and b in text:
            found.append(b)
    check(f"{d.name}: contains no banned collocations", not found,
          f"found banned collocation(s): {found} — see question-authoring/references/banned_collocations.txt")


# --------------------------------------------------------------- per-test checks
def check_tests():
    g = load(".agents/exam-app/scripts/grade_answers.py")
    m = load(".agents/choukai-audio/scripts/make_choukai_mp3.py")
    bi = load(".agents/exam-app/scripts/build_interactive.py")
    key_heading = re.compile(r"^#+\s*(解答|【?正解)", re.M)
    expected_choukai = ([f"問{s}-{i}" for s, n in ((1, 5), (2, 6), (3, 5), (4, 11))
                         for i in range(1, n + 1)]
                        + ["問5-1", "問5-2-1", "問5-2-2"])

    dirs = sorted(p for p in (ROOT / "tests").glob("*") if p.is_dir()) if (ROOT / "tests").is_dir() else []
    if dirs and not any(ORIGIN.is_imported(p.name) for p in dirs):
        # The cross-test reuse checks compare generated tests with each other,
        # but their strongest comparison — against the official paper others
        # copy from — needs an imported test on disk, and the calibration
        # anchor tests/imported-n2-2025-07 was deleted. Say so instead of
        # letting that half of the check pass silently.
        skip("cross-test 例/（注N） reuse vs an official import",
             "no tests/imported-* on disk — only generated↔generated "
             "comparison runs; re-import a reference paper to restore it")
    if not dirs:
        print("\nper-test contracts")
        skip("tests/", "no test directories on disk")
        return

    # Reuse across tests can only be seen with every test in hand (G15).
    reuse: dict[str, dict[str, set[str]]] = {}
    for p in dirs:
        gp, sp, cp = p / "言語知識・読解.md", p / "聴解スクリプト.txt", p / "聴解.md"
        reuse[p.name] = {
            "notes": test_note_lines(gp.read_text(encoding="utf-8")) if gp.is_file() else set(),
            "examples": test_example_blocks(sp.read_text(encoding="utf-8")) if sp.is_file() else set(),
            "choukai_options": test_choukai_example_options(cp.read_text(encoding="utf-8")) if cp.is_file() else set(),
        }

    for d in dirs:
        print(f"\nper-test contracts: {d.relative_to(ROOT)}")
        origin = ORIGIN.test_origin(d.name)
        if origin == "imported":
            slug = d.name[len(ORIGIN.IMPORTED_PREFIX):]
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
        exp_g_count = 75 if len(keys) == 75 else 71
        check(f"{exp_g_count} gengo answer keys parse", len(keys) == exp_g_count,
              f"got {len(keys)}, missing {[q for q in range(1, exp_g_count + 1) if q not in keys]}")
        ck = g.parse_choukai_keys(choukai)
        exp_c = ([f"問{s}-{i}" for s, n in ((1, 5), (2, 6), (3, 5), (4, 12)) for i in range(1, n + 1)] + ["問5-1", "問5-2", "問5-3-1", "問5-3-2"]) if len(ck) == 32 or "問5-3-1" in ck else expected_choukai
        check(f"{len(exp_c)} choukai answer keys parse with the expected labels",
              sorted(ck) == sorted(exp_c),
              f"missing {[k for k in exp_c if k not in ck]}, "
              f"unexpected {[k for k in ck if k not in exp_c]}")

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
            check_mondai8_bare_adverbs(d.name, opts)
            check_grammar_p8_targets(gt, opts, d.name)
        check_level_band_grammar(gt, keys, opts, origin, d.name)
        check_moji4_blank_stems(d.name, gt, keys, opts)
        st_text = (d / "聴解スクリプト.txt").read_text(encoding="utf-8") if (d / "聴解スクリプト.txt").is_file() else ""
        check_banned_collocations(d, gt, ct, st_text, origin)
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
        check_dokkai_span_anchor_bold(gengo.name, gengo_prose)
        check_dokkai_span_anchor_identity(gengo.name, gengo_prose)
        check_note_pairing(d.name, gengo_prose)
        check_note_band(d.name, gt)
        check_note_band_reuse(d.name, gt)
        if origin == "generated":
            check_dokkai_lengths(d.name, gengo_prose, bi)
            check_dokkai_rhetorical_monotony(d.name, gengo_prose)
            check_dokkai_closing_reframe(d.name, gengo_prose, bi)
            check_dokkai_abs_quantifiers(d.name, opts)
            check_dokkai_option_length_balance(d.name, opts)
            check_chuuryaku(d.name, gengo_prose)
            check_mondai11_stems(d.name, gengo_prose)
            check_mondai13_closer(d.name, gengo_prose)
        check_verbatim_keys(d.name, gengo_prose, keys, opts, bi)
        check_dokkai_longest_key_rate(d.name, keys, opts, origin=origin)

        # Only the 読解 key table quotes running text; the 文字・語彙 and 文法
        # tables put grammar glosses in 「」 by design, which is not a quote.
        gcut = bi.KEY_HEADING.search(gt)
        dokkai = re.search(r"^##\s*読解\s*$(.*)", gt[gcut.start():] if gcut else "",
                           re.M | re.S)
        if gcut and dokkai:
            passages_prose_src = "\n".join(passage_prose(dokkai_section(gt[:gcut.start()], n), bi) for n in range(10, 15))
            check_explanation_quotes(gengo.name, dokkai.group(1), passages_prose_src)
            if origin == "generated":
                check_mondai14_quotes(d.name, gengo_prose, dokkai.group(1), bi)
        if gcut:
            check_fabricated_distractors(gengo.name, gt[gcut.start():])
        bunpou = re.search(r"^##\s*文法\s*$(.*?)(?=^##\s|\Z)",
                           gt[gcut.start():] if gcut else "", re.M | re.S)
        if bunpou and origin == "generated":
            check_mondai9_tags(d.name, bunpou.group(1))
            check_mondai9_option_lengths(d.name, opts)
            check_mondai7_option_refs(d.name, bunpou.group(1), opts)
        elif origin == "generated":
            check(f"{d.name}: 問題9 解説 cells carry four distinct category "
                  f"tags incl. one [内容推論]", False,
                  "no `## 文法` answer-key table to read (question-authoring)")
        if origin == "generated":
            check_cross_test_reuse(d.name, reuse[d.name],
                                   {k: v for k, v in reuse.items() if k != d.name})
        else:
            skip(f"{d.name}: no （注N）/例。block is byte-identical to another test's",
                 "an imported paper is what others copy, not the copier")

        # Official July 2025 (~50+ 注, 中略 in 中文, 長文 ~1000) is the bar.
        # Generated papers have under-annotated; warn so authoring cannot ignore it.
        if origin == "generated":
            # Count IN-BODY （注N） markers in the passage region: every gloss
            # occurs at least twice (marker + definition line) and 解説
            # back-references add more, so counting raw occurrences across the
            # file roughly doubled the total — generated papers have cleared
            # this bar on 6–9 real glosses while one reported 10 that was
            # really 5. Counting
            # definition lines instead is format-specific (the official July
            # 2025 paper glosses in-body and measures 5 that way, not 30), and
            # 注 numbers restart per passage so distinct numbers undercount.
            # Markers-minus-definitions is the one metric that holds for both.
            notes_body = gt[: gcut.start()] if gcut else gt
            notes_prose = "\n".join(
                ln for ln in notes_body.splitlines()
                if not re.match(r"\s*[（(]注\d*[）)]\s*\S+?\s*(?::|：)", ln))
            notes = len(re.findall(r"（注\d*）|\(注\d*\)", notes_prose))
            # Floor RE-MEASURED: the archive's current-era band is 27–61
            # in-body markers, median 39 (official_calibration §3), so the old
            # floor of 15 was "half of official" and passed every
            # under-annotated paper — generated papers have shipped
            # 9/6/29/15 under it.
            # Raised to 25, which is `question-authoring`'s authoring target and
            # sits just under the observed minimum of 27.
            warn(f"{d.name}: 読解 has substantial （注N） glosses "
                 f"(official current-era band 27–61, median 39; got {notes})",
                 notes >= GLOSS_MARKER_MIN,
                 f"under {GLOSS_MARKER_MIN} in-body markers — the count is "
                 f"earned in 問題11 (median 5.5 per passage) and 問題13 "
                 f"(median 7); official 問題12 and 問題14 carry ZERO, so do not "
                 f"spread a quota across 問題10 (question-authoring; "
                 f"official_calibration §3)")
            # The gloss BAND is check_note_band (openjlpt membership + circular
            # definitions) — the old 21-word alternation here could never cover
            # the class and missed 鑑賞/割引/便箋/蘇る. （中略） placement is
            # check_chuuryaku and the 問題13 length floor is check_dokkai_lengths,
            # both of which run for every test.
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
                key_region = ct[ccut.start():]
                # The セクション構成表's free-text audit notes (e.g. a cross-test
                # comparison quoting a PRIOR test's old structure) sit after the
                # key tables and are not claims about THIS script — stop the
                # quote-traceability scan at that heading (20260817_1 QA G8).
                sec_table = re.search(r"^#+\s*セクション構成表", key_region, re.M)
                if sec_table:
                    key_region = key_region[:sec_table.start()]
                check_explanation_quotes(choukai.name, key_region,
                                         st + ct[: ccut.start()])
                check_fabricated_distractors(choukai.name, ct[ccut.start():])
                check_choukai_kaisetsu_keys(d.name, ct, bi)
            blocks = [b.strip() for b in re.split(r"\n\s*\n", st) if b.strip()]
            if origin == "generated":
                try:
                    m.validate_script(blocks)
                    check(f"聴解スクリプト.txt passes validate_script ({len(blocks)} blocks)", True)
                except SystemExit as e:
                    check("聴解スクリプト.txt passes validate_script", False, str(e).replace("\n", " ")[:300])
                check_script_shape(st, ct, m, d.name)
                check_example_premarks(ct, st, bi)
            check_mondai5_prints_nothing(d.name, ct, bi)
            check_mondai5_enumeration(d.name, st, ct, bi)
            check_voice_casting(st, m, origin, d.name)
            # Register is a GENERATION failure mode: an imported official paper
            # is the reference these thresholds came from, and its script.md is
            # partly OCR, so measuring it here would flag the yardstick.
            if origin == "generated":
                check_script_register(d.name, st, m)
                # G16 — section-level, i.e. what item-by-item review cannot see.
                check_choukai_key_duplication(d.name, ct, st, m, bi)
                check_choukai_countable_mix(d.name, ct, st, m, bi)
                check_choukai_same_speaker_lines(d.name, st, m)
                check_choukai_section_table(d.name, ct, bi)
                check_choukai_judgment_mix(d.name, st, ct, m, bi)
                check_choukai_longest_key_rate(d.name, ct, st, m, bi)
                check_model_answer_option_sync(d.name, gt, ct, st, m, bi)
                check_moji_longest_key_rate(d.name, gt, keys, bi)
                # G17 — the sentences themselves, vs Shin Kanzen 実力養成編.
                check_choukai_contractions(d.name, st, m)
                check_choukai_key_paraphrase(d.name, ct, st, m, bi)
            check_spec_target_items(d, gt, st, bi)
        else:
            check("聴解スクリプト.txt present", False, "canonical name required")

        if (d / "聴解.mp3").is_file():
            check("聴解_チャプター.json accompanies the MP3", (d / "聴解_チャプター.json").is_file(),
                  "re-run make mp3 to regenerate chapter marks")
        check_artifact_freshness(d)

        sheet = d / "解答.html"
        if not sheet.is_file():
            check("解答.html present", False, "run make sheet")
            continue

        html = sheet.read_text(encoding="utf-8")

        # Radio-group shape. Every one of these caught a real bug: a single
        # bubble per horizontally-laid-out question (unanswerable beyond
        # option 1), and 質問1/質問2 colliding with 1番/2番 in 問題5.
        groups: dict[str, int] = {}
        for hit in re.finditer(r'<input[^>]*type="radio"[^>]*name="q_([^"]+)"', html):
            groups[hit.group(1)] = groups.get(hit.group(1), 0) + 1

        exp_total_keys = exp_g_count + len(exp_c)
        check(f"one radio group per question ({len(groups)} groups)", len(groups) == exp_total_keys,
              f"expected {exp_total_keys}, got {len(groups)}")
        missing = [k for k in list(map(str, range(1, exp_g_count + 1))) + exp_c if k not in groups]
        check("every scored question has a radio group", not missing, f"missing {missing}")
        oversized = {k: n for k, n in groups.items() if n > 4}
        check("no question shares a group name with another",
              not oversized, f"over-filled groups: {oversized}")
        thin = {k: n for k, n in groups.items() if n < 3}
        check("no question offers fewer than 3 options", not thin,
              f"under-filled groups: {thin} (horizontal option rows must yield 4 bubbles)")
        gengo_bad = {k: n for k, n in groups.items() if k.isdigit() and n != 4}
        check(f"all {exp_g_count} gengo questions offer exactly 4 options", not gengo_bad, f"{gengo_bad}")
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
    if shutil.which("node") is None:
        return skip("grader parity", "node not installed")

    g = load(".agents/exam-app/scripts/grade_answers.py")
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
        check_makefile_help()
        check_deployments()
        check_pacing()
        check_item_counts()
        check_taxonomy()
        check_pool_infrastructure()
        check_pool_grammar_band()
        check_pool_kanji_reading_shape()
        print("\nrotation inputs (why a new test is actually new)")
        check_rotation_inputs()
        check_ledger_draw_counts(load(".agents/exam-blueprint/scripts/sample_items.py"))
        check_ledger_spec_agreement()
        check_harvest_hygiene()
        check_harvest_provenance()
        check_topics_themes()
        check_theme_repeat_cross_test()
        check_cross_test_listening_subjects()
        check_draw_provenance()
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
