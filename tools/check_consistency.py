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
        ("採点結果.md", ".agents/interactive-answer-sheet/scripts/build_interactive.py"),
        ("user_answers.json", ".agents/interactive-answer-sheet/scripts/build_interactive.py"),
        ("聴解.mp3", ".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py"),
        ("聴解_チャプター.json", ".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py"),
        ("ledger.json", ".agents/item-pool-sampling/scripts/sample_items.py"),
        ("test_spec.json", ".agents/item-pool-sampling/scripts/sample_items.py"),
    ]
    for literal, script in contracts:
        src = (ROOT / script).read_text(encoding="utf-8")
        check(f"{literal} written by {Path(script).name}", literal in src)

    # Filenames retired by the merge to a single sheet must not come back.
    retired = ["言語知識・読解_解答.html", "聴解_解答.html", "採点結果_",
               "user_answers_gengo", "user_answers_choukai", "マークシート.pdf"]
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
    # 問題1-4 print one 例 on top of the scored items; 問題5 has 3 blocks, 4 answers.
    derived = {k: v - 1 for k, v in m.EXPECTED_ITEMS.items() if k != "問題5"}
    check("問題1-4 scored counts = EXPECTED_ITEMS − 例",
          {k: counts.get(k) for k in derived} == derived,
          f"doc {[counts.get(k) for k in derived]} vs derived {list(derived.values())}")
    check("問題5 = 4 answers from 3 blocks",
          counts.get("問題5") == 4 and m.EXPECTED_ITEMS["問題5"] == 3,
          f"doc {counts.get('問題5')} answers, code {m.EXPECTED_ITEMS['問題5']} blocks")
    total = sum(counts.values())
    check(f"聴解 totals {total} = 32 answers", total == 32)


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
    check("gengo table sums to 75", sum(c for c, _ in doc_rows.values()) == 75,
          f"sums to {sum(c for c, _ in doc_rows.values())}")

    sect = {}
    for s in g.GENGO_QUESTION_TAXONOMY.values():
        sect[s["section"]] = sect.get(s["section"], 0) + s["total"]
    grading_doc = (AGENTS / "exam-answer-grading" / "SKILL.md").read_text(encoding="utf-8")
    for label, key, want in (("言語知識", "言語知識", 54), ("読解", "読解", 21)):
        check(f"{label} = {want} items", sect.get(key) == want, f"taxonomy gives {sect.get(key)}")
        check(f"{label} {want} documented in exam-answer-grading",
              re.search(rf"{want} questions max|{want} items", grading_doc) is not None)


# --------------------------------------------------------------- per-test checks
def check_tests():
    g = load(".agents/exam-answer-grading/scripts/grade_answers.py")
    m = load(".agents/choukai-mp3-generation/scripts/make_choukai_mp3.py")
    key_heading = re.compile(r"^#+\s*(解答|【?正解)", re.M)
    expected_choukai = ([f"問{s}-{i}" for s, n in ((1, 5), (2, 6), (3, 5), (4, 12))
                         for i in range(1, n + 1)]
                        + ["問5-1", "問5-2", "問5-3-1", "問5-3-2"])

    dirs = sorted(p for p in (ROOT / "tests").glob("*") if p.is_dir()) if (ROOT / "tests").is_dir() else []
    if not dirs:
        print("\nper-test contracts")
        skip("tests/", "no test directories on disk")
        return

    for d in dirs:
        print(f"\nper-test contracts: {d.relative_to(ROOT)}")
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
        check("75 gengo answer keys parse", len(keys) == 75,
              f"got {len(keys)}, missing {[q for q in range(1, 76) if q not in keys]}")
        ck = g.parse_choukai_keys(choukai)
        check("32 choukai answer keys parse with the expected labels",
              sorted(ck) == sorted(expected_choukai),
              f"missing {[k for k in expected_choukai if k not in ck]}, "
              f"unexpected {[k for k in ck if k not in expected_choukai]}")

        script = d / "聴解スクリプト.txt"
        if script.is_file():
            blocks = [b.strip() for b in re.split(r"\n\s*\n", script.read_text(encoding="utf-8")) if b.strip()]
            try:
                m.validate_script(blocks)
                check(f"聴解スクリプト.txt passes validate_script ({len(blocks)} blocks)", True)
            except SystemExit as e:
                check("聴解スクリプト.txt passes validate_script", False, str(e).replace("\n", " ")[:300])
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

        check(f"one radio group per question ({len(groups)} groups)", len(groups) == 107,
              f"expected 107, got {len(groups)}")
        missing = [k for k in list(map(str, range(1, 76))) + expected_choukai if k not in groups]
        check("every scored question has a radio group", not missing, f"missing {missing}")
        oversized = {k: n for k, n in groups.items() if n > 4}
        check("no question shares a group name with another",
              not oversized, f"over-filled groups: {oversized}")
        thin = {k: n for k, n in groups.items() if n < 3}
        check("no question offers fewer than 3 options", not thin,
              f"under-filled groups: {thin} (horizontal option rows must yield 4 bubbles)")
        gengo_bad = {k: n for k, n in groups.items() if k.isdigit() and n != 4}
        check("all 75 gengo questions offer exactly 4 options", not gengo_bad, f"{gengo_bad}")
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
new Function('ctx', js + '\nctx.buildReport = buildReport; ctx.ANSWER_KEY = ANSWER_KEY;')(sandbox);

// Deterministic simulated answers: correct unless the index is divisible by 3.
const ans = {};
Object.keys(sandbox.ANSWER_KEY).sort().forEach((k, i) => {
  const correct = sandbox.ANSWER_KEY[k];
  ans[k] = (i % 3 === 0) ? (correct % 4) + 1 : correct;
});
fs.writeFileSync(process.argv[3], JSON.stringify(ans));
process.stdout.write(sandbox.buildReport(ans));
"""


def check_grader_parity():
    print("\nin-page grader ↔ grade_answers.py (same answers, same raw scores)")
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

            # The report also lists per-大問 rows (`3 / 5`); keep only the three
            # section totals, whose denominators are the section sizes.
            js_raw = {int(t): int(c) for c, t in re.findall(r"\|\s*(\d+) / (\d+)\s*\|", r.stdout)
                      if int(t) in (54, 21, 32)}
            flat = json.loads(answers.read_text(encoding="utf-8"))
            ua = {"言語知識_読解": {k: v for k, v in flat.items() if not k.startswith("問")},
                  "聴解": {k: v for k, v in flat.items() if k.startswith("問")}}
            res = g.grade(g.parse_gengo_keys(d / "言語知識・読解.md"),
                          g.parse_choukai_keys(d / "聴解.md"), ua)
            py_raw = {s["raw_total"]: s["raw_correct"] for s in res["summary"]["sections"].values()}

            check(f"{d.name}: raw scores agree "
                  f"({py_raw.get(54)}/54 + {py_raw.get(21)}/21 + {py_raw.get(32)}/32)",
                  js_raw == py_raw, f"JS {js_raw} vs Python {py_raw}")


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
    check_tests()
    check_grader_parity()

    print()
    if _fail:
        print(f"FAILED — {len(_fail)} problem(s):")
        for f in _fail:
            print(f"  - {f}")
        return 1
    print(f"All checks passed{f' ({len(_skip)} skipped)' if _skip else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
