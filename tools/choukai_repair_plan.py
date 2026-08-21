#!/usr/bin/env python3
"""Turn `make findings` into the 聴解 repair work order (REPORT-CHOUKAI.md §5.0).

This tool computes NOTHING of its own, on purpose. The gate owns the
thresholds, `tools/choukai_profile.py` owns the measurement, `FINDING_REPAIR`
owns the artifact a repair touches, and the tier is derived from that artifact.
A fourth copy of any number here would be exactly the defect the audit opened
with (F3, F7) — so every field below is read from `logs/findings.json` or from
`logs/choukai_remediation_state.json`.

    make findings                  # gate --json -> logs/findings.json
    make repair-plan               # every paper -> qa/repair-plan.{json,md}
    make repair-plan 20260819_1    # one paper  -> qa/20260819_1/repair-plan.{json,md}
    make repair-plan TIER=B        # just the batch that must land before a rebuild

Why the tiers matter more than the counts: tier B is FREE if it lands inside a
rebuild window that is happening anyway, and costs ~33 MB of LFS per paper if it
does not (§5B). So the plan prints the rebuild set as a command list rather than
leaving batching to memory.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS = ROOT / "logs" / "findings.json"
STATE = ROOT / "logs" / "choukai_remediation_state.json"

TIER_TITLE = {
    "A": "Tier A — 聴解.md only (booklet + sheet rebuild, no audio)",
    "B": "Tier B — 聴解スクリプト.txt (rides the next `make mp3`; free if batched)",
    "C": "Tier C — section re-authoring (C1 items / C2 whole section, by axis count)",
    "R": "Rebuild only — `make mp3` + `make sheet`, no content change",
}

# Where the rule behind each slug lives. One pointer per finding, so a repair
# starts from the owner doc instead of from the failure message.
OWNER_DOC = {
    "choukai_section_table_missing": "choukai-items.md §'Write the SECTION TABLE'",
    "choukai_elimination_tokens": "choukai-items.md §消去方法",
    "choukai_voice_margin": "choukai-audio SKILL.md Part 2 §Casting (margin in semitones, §D2)",
    "choukai_split_turns": "choukai-audio SKILL.md Part 1 §Block conventions",
    "choukai_contraction_rate": "choukai-audio SKILL.md §Register rule 3",
    "choukai_q3_option_suffix": "choukai-items.md §概要理解",
    "choukai_filler_band": "official_register.md §7.1",
    "choukai_reaction_floor": "official_register.md §1 / §2.1",
    "choukai_service_formula_rate": "choukai-audio SKILL.md §Banned formulas",
    "choukai_q1_question_forms": "choukai-items.md §'Section item mix' 問題1 + jlpt-exam-structure §問題1 Question Forms",
    "choukai_q2_question_mix": "choukai-items.md §'Section item mix' 問題2",
    "choukai_decider_position": "choukai-audio SKILL.md §Register rule 6",
    "choukai_probe_carousel": "choukai-items.md §'Section item mix' 問題1",
    "choukai_q3_talk_band": "choukai-items.md §'Section item mix' 問題3",
    "choukai_q5_speaker_count": "choukai-items.md §統合理解",
    "choukai_q4_done_concentration": "choukai-items.md §即時応答",
    "choukai_q4_stimulus_register": "choukai-items.md §'Section item mix' 問題4",
    "choukai_voice_balance": "choukai-audio SKILL.md Part 2 §Casting",
    "choukai_pause_distribution": "choukai-audio SKILL.md Part 3 §Verify the pause DISTRIBUTION",
}


def load_findings(test_id: str | None, tier: str | None) -> list[dict]:
    if not FINDINGS.is_file():
        raise SystemExit(f"{FINDINGS} not found — run `make findings` first")
    rows = json.loads(FINDINGS.read_text(encoding="utf-8"))["findings"]
    rows = [r for r in rows if r.get("tier")]
    if test_id:
        rows = [r for r in rows if r.get("test_id") == test_id]
    if tier:
        rows = [r for r in rows if r["tier"] == tier.upper()]
    return rows


def declined() -> dict[str, str]:
    """Papers the plan said no to, with the reason — a decline must be visible."""
    if not STATE.is_file():
        return {}
    state = json.loads(STATE.read_text(encoding="utf-8"))
    return {s["test_id"]: s.get("reason", "(no reason recorded — fix the state file)")
            for s in state.get("steps", [])
            if s.get("status") == "declined" and s.get("test_id")}


def render(rows: list[dict], scope: str) -> str:
    by_tier: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_tier[r["tier"]].append(r)

    out = [f"# 聴解 repair plan — {scope}", ""]
    out.append(f"Derived from `logs/findings.json` ({len(rows)} finding(s) carrying a "
               f"tier). Every field here is read, never computed: the gate owns the "
               f"thresholds, `choukai_profile.py` the measurement, `FINDING_REPAIR` the "
               f"artifact, and the tier follows from the artifact (REPORT-CHOUKAI.md §5.0).")
    out.append("")

    for tier in ("A", "B", "C", "R"):
        items = by_tier.get(tier)
        if not items:
            continue
        out += [f"## {TIER_TITLE[tier]}", ""]
        out += ["| paper | finding | automation | measurement | rule |", "|---|---|---|---|---|"]
        for r in sorted(items, key=lambda x: (x.get("test_id") or "", x["slug"])):
            detail = (r.get("detail") or "").replace("\n", " ").replace("|", "/")
            out.append(f"| {r.get('test_id') or '—'} | `{r['slug']}` | {r['automation']} "
                       f"| {detail[:150]} | {OWNER_DOC.get(r['slug'], '—')} |")
        out.append("")

    rebuild = sorted({r["test_id"] for r in rows
                      if r["tier"] in ("B", "R") and r.get("test_id")})
    out += ["## The rebuild set — batch these, do not do them one at a time", ""]
    if rebuild:
        out.append("A script edit is free inside a rebuild window and costs ~33 MB of "
                   "Git LFS per paper outside one. Land every tier-B edit BEFORE running:")
        out.append("")
        out.append("```bash")
        for tid in rebuild:
            out.append(f"make mp3 {tid} && make sheet {tid}")
        out.append("make pages && make check")
        out.append("```")
    else:
        out.append("_Empty — no paper needs its audio rebuilt._")
    out.append("")

    det = sorted({r["test_id"] for r in rows
                  if r["automation"] == "deterministic" and r["tier"] == "B" and r.get("test_id")})
    out += ["## The deterministic subset — `make autofix` writes these", ""]
    if det:
        out.append("```bash")
        for tid in det:
            out.append(f"make autofix {tid}")
        out.append("```")
        out.append("")
        out.append("Everything else is `assisted` or `authoring` on purpose: stripping "
                   "「〜について」 off a 問題3 option is a writing decision, not a "
                   "substitution (§5.0.1).")
    else:
        out.append("_Empty._")
    out.append("")

    dec = declined()
    out += ["## Not in this plan — declined, with the reason", ""]
    if dec:
        out += ["| paper | why it is not repaired |", "|---|---|"]
        for tid, why in sorted(dec.items()):
            out.append(f"| {tid} | {why} |")
        out.append("")
        out.append("An id leaves this list the moment its 聴解 is actually repaired — "
                   "never by widening a threshold (`AGENTS.md` §0.7: an unstated skip is "
                   "the thing that keeps shipping).")
    else:
        out.append("_Nothing declined — or `logs/choukai_remediation_state.json` records "
                   "no `declined` step yet._")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("test_id", nargs="?", help="one paper (default: every paper)")
    ap.add_argument("--tier", help="only tier A, B, C or R")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing files")
    args = ap.parse_args()

    rows = load_findings(args.test_id, args.tier)
    scope = args.test_id or "every generated paper"
    if args.tier:
        scope += f", tier {args.tier.upper()} only"
    md = render(rows, scope)
    if args.stdout:
        print(md)
        return 0

    outdir = ROOT / "qa" / args.test_id if args.test_id else ROOT / "qa"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "repair-plan.md").write_text(md, encoding="utf-8")
    (outdir / "repair-plan.json").write_text(
        json.dumps({"scope": scope, "findings": rows}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print(f"{len(rows)} finding(s) -> {outdir / 'repair-plan.md'}")
    counts = collections.Counter(r["tier"] for r in rows)
    print("  tiers: " + ", ".join(f"{t}={counts[t]}" for t in sorted(counts)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
