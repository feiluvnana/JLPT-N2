#!/usr/bin/env python3
"""文字・語彙 (問題1–6) measurement — ONE parser, both corpora, two consumers.

Why this file exists (REPORT-GOI.md §F10, §D1): every 文字・語彙 number the rules
are built on used to live in prose, with the gate re-implementing it, and nothing
forcing the two to agree. Three of those numbers turned out to be unreproducible.
So the measurement lives here, once:

  * `tools/check_consistency.py` imports this module for its 文字・語彙 checks —
    the gate keeps owning the THRESHOLDS, this file owns the MEASUREMENT;
  * `--baseline` prints the official tables in the Markdown shape
    `moji-goi.md` / `official_calibration.md` carry, so refreshing a doc is a
    paste, not a retype.

Usage:
    python3 tools/goi_profile.py --official [--era cur|all]
    python3 tools/goi_profile.py --tests 20260819_1 …      (default: every test)
    python3 tools/goi_profile.py --baseline [--json]

KNOWN LIMIT, stated rather than hidden: `booklet.md` is a text-layer extract and
the 問題1/2/5 UNDERLINE does not survive it, so an official record's `target` is
always None. Every measure here is therefore built on stems, option sets and
keys — never on an inferred official target. That absence is why the 訓読み band
cannot be re-derived from the archive (§F10.3).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "refs" / "JLPT_N2_NEW"
TESTS = ROOT / "tests"

# Same definition as `check_consistency.jp_char_count()`; the gate asserts the
# two agree (`check_goi_profile_parse_agreement`), so this may not drift.
JP_CHAR = re.compile(r"[぀-ヿ一-鿿ー。、！？（）「」『』…・]")
KANJI = re.compile(r"[一-鿿]")
KANA = re.compile(r"[぀-ヿー]")
HIRAGANA = re.compile(r"[ぁ-ゟ]")

# Current era = the format this repo models (問題3 at 3 items): 12/2022 onward.
CURRENT_ERA = ("13. N2 12-2022", "14. N2 7-2023", "14. N2 12-2023",
               "15. N2 7-2024", "15. N2 12-2024", "16. N2 7-2025",
               "17.N2 12-2025")

# --- register classifiers (§F7). Two flat token lists, printed here because
# they ARE the definition: the gate's register half is a WARN precisely because
# these will mis-bucket edge cases. Applied identically to both corpora.
PERSONAL = ("私", "僕", "俺", "わたし", "ぼく", "母", "父", "祖母", "祖父", "娘",
            "息子", "妻", "夫", "兄", "姉", "弟", "妹", "家族", "友人", "友達",
            "彼", "彼女", "子ども", "子供", "うち", "自分", "部屋", "昨日", "今朝",
            "夕食", "朝食", "犬", "猫", "先輩", "後輩", "隣", "実家")
INSTITUTIONAL = ("市", "町", "県", "国", "政府", "省", "会社", "当社", "本社",
                 "支店", "部長", "課長", "社長", "担当者", "職員", "当店", "学校",
                 "大学", "委員会", "協会", "組織", "予算", "事業", "申請", "制度",
                 "規定", "条例", "契約", "工場", "銀行", "病院", "議会", "当局")
# 「でした」 does not contain 「です」 as a substring (で-し-た), so it was measured
# as PLAIN until 2026-08-21 — a real polite stem counted against the floor.
# Found while repairing 20260817_2. Both corpora are re-measured with the fixed
# list, so the archive bands moved with it.
POLITE = ("です", "ます", "ました", "ません", "でした", "でしょう", "ください",
          "ですか", "ますか", "でしたか")
POLITE_FINAL = re.compile(r"(です|ます|ました|ません|ませんか|ますか|でした|"
                          r"でしたか|でしょう|ください|ましょう)[。、！？]?$")
FIRST_PERSON = ("私", "僕", "俺", "わたし", "ぼく", "わたくし")


def jp(s: str) -> int:
    return len(JP_CHAR.findall(re.sub(r"\s+", "", s)))


# --------------------------------------------------------------------------
# Parsing — one record type from both sides:
#   {corpus, paper, mondai, no, stem, options[4], key, target}
# --------------------------------------------------------------------------
MARKER = re.compile(r"(?<![0-9０-９])([1-4])[ 　]+(?=\S)")
# 「1 週間」「2 時間」 inside an option sentence is a quantity, not an option
# marker — without this the last item of every 問題6 mis-parses (and it is why
# the audit behind REPORT-GOI.md lost 30 items it did not have to).
COUNTER = re.compile(r"^(?:週間?|時間?|日間?|人|回|年|月|分|個|冊|枚|件|割|度|歳|"
                     r"本|台|倍|杯|階|軒|着|色|種|位|キロ|メートル|ページ|"
                     r"か月|カ月|ヶ月)")
MAX_OPT_CH = 60          # a 問題6 option is a sentence; longer means a swallow
# Page footers the text layer leaves at the end of a section's last item.
FOOTER = re.compile(r"(?:N2\s*)?\d{1,2}/\d{4}\s*$|(?:文\s*法|読\s*解|言語知識)\s*$")
RUBY_LINE = re.compile(r"^[ぁ-ゟァ-ヶー]{1,10}$")
# An instruction line ends the previous item: the archive prints them with no
# heading and sometimes OCR'd as 「間題」 (6. N2 7-2015 swallowed one into a
# 問題3 option before this).
INSTRUCTION = re.compile(r"選びなさい|[問間]題\s*\d")
FULLWIDTH = str.maketrans("０１２３４５６７８９", "0123456789")


def _official_region(md: str) -> list[str]:
    """The 文字・語彙 lines of one `booklet.md`, ruby lines dropped.

    Located by the 問題1 instruction line and bounded by the 問題7 one — the
    `###` headings are unreliable (12/2022 prints 「間題 4」 with no heading and
    loses its 問題5 heading entirely). A short all-kana line following a
    kanji-final line is dropped as ruby.
    """
    lines = [ln.strip() for ln in md.translate(FULLWIDTH).splitlines()]
    start = end = None
    for i, ln in enumerate(lines):
        if start is None and re.search(r"問題\s*1\b.*読み方", ln):
            start = i
        if start is not None and re.search(r"問題\s*7\b", ln):
            end = i
            break
    if start is None:
        return []
    kept: list[str] = []
    for ln in lines[start:end or len(lines)]:
        if not ln or ln.startswith(("##", ">", "|")):
            continue
        if RUBY_LINE.match(ln) and kept and KANJI.search(kept[-1][-1:]):
            continue                      # furigana of the previous line
        kept.append(ln)
    return kept


def _blobs(lines: list[str], numbers: list[int]) -> dict[int, str]:
    """Join the region's lines into one text blob per item number."""
    out: dict[int, str] = {}
    want = list(numbers)
    cur: int | None = None
    for ln in lines:
        if INSTRUCTION.search(ln):
            cur = None
            continue
        m = re.match(r"^(\d{1,2})[ 　]+(.*)$", ln)
        if m and want and int(m.group(1)) == want[0]:
            cur = want.pop(0)
            out[cur] = m.group(2)
            continue
        if cur is not None:
            out[cur] = f"{out[cur]} {ln}"
    return out


def split_options(blob: str) -> tuple[str, list[str]] | None:
    """`stem 1 a 2 b 3 c 4 d` -> (stem, [a, b, c, d]); None if it does not parse.

    Options are assigned to SLOTS by their printed digit, not by sequence, so
    the two-column 問題5 layout (which prints 1/3 then 2/4) parses too. Two
    passes: first with the counter filter (which is what keeps 「病院で 1 週間」
    inside a 問題6 option sentence from reading as option 1), then without it,
    because a 問題3 option set IS four counter-like single kanji (割/率/値/比).
    """
    blob = FOOTER.sub("", blob).strip()
    for drop_counters in (True, False):
        cands = [m for m in MARKER.finditer(blob)
                 if not (drop_counters and COUNTER.match(blob[m.end():]))]
        first: dict[int, int] = {}
        for m in cands:
            first.setdefault(int(m.group(1)), m.start())
        if len(first) < 4:
            continue
        order = sorted(first.items(), key=lambda kv: kv[1])
        bounds = [p for _, p in order] + [len(blob)]
        opts = {d: MARKER.sub("", blob[pos:bounds[i + 1]], count=1).strip()
                for i, (d, pos) in enumerate(order)}
        stem, out = blob[:order[0][1]].strip(), [opts[d] for d in (1, 2, 3, 4)]
        if stem and all(o and len(o) <= MAX_OPT_CH for o in out):
            return stem, out
    return None


def official_items(era: str = "all") -> list[dict]:
    """Every parsable official 問題1–6 item across the archive."""
    keys = json.loads((REFS / "answer_keys.json").read_text(encoding="utf-8"))
    out: list[dict] = []
    for sitting, exam in keys["exams"].items():
        if era == "cur" and sitting not in CURRENT_ERA:
            continue
        booklet = REFS / sitting / "booklet.md"
        if not booklet.is_file():
            continue
        moji = [it for it in exam["items"] if it["section"] == "文字・語彙"]
        lines = _official_region(booklet.read_text(encoding="utf-8"))
        blobs = _blobs(lines, [it["no"] for it in moji])
        for it in moji:
            blob = blobs.get(it["no"])
            parsed = split_options(blob) if blob else None
            if not parsed:
                continue
            stem, opts = parsed
            # A 問題1–5 option is a WORD (no 。) and a 問題6 option is a
            # SENTENCE — the cheapest test that a layout accident (a swallowed
            # neighbour, a stray page footer) did not parse as an option row.
            sentences = sum("。" in o for o in opts)
            if sentences != (4 if it["mondai"] == 6 else 0):
                continue
            if any(jp(o) == 0 for o in opts):
                continue
            out.append({"corpus": "official", "paper": sitting,
                        "mondai": it["mondai"], "no": it["no"],
                        "stem": stem, "options": opts,
                        "key": it["answer"], "target": None})
    return out


GEN_SEC = re.compile(r"^##\s*問題(\d+)", re.M)
GEN_STEM = re.compile(r"^\*\*(\d+)\*\*(.*)$")
GEN_OPT = re.compile(r"^\s*[1-4][.、]")


def generated_items(md: str, paper: str = "") -> list[dict]:
    """Every 問題1–6 item of one `言語知識・読解.md`, keys from its own table."""
    body = md.split("# 解答")[0]
    keys = _generated_keys(md)
    out: list[dict] = []
    mondai = None
    for ln in body.splitlines():
        sec = GEN_SEC.match(ln)
        if sec:
            n = int(sec.group(1))
            mondai = n if 1 <= n <= 6 else None   # 問題7+ is 文法/読解, not ours
            continue
        if mondai is None:
            continue
        st = GEN_STEM.match(ln.strip())
        if st:
            out.append({"corpus": "generated", "paper": paper,
                        "mondai": mondai, "no": int(st.group(1)),
                        "stem": st.group(2).strip(), "options": [],
                        "key": keys.get(int(st.group(1))),
                        "target": _marked_span(st.group(2))})
            continue
        if out and GEN_OPT.match(ln):
            out[-1]["options"] += [p.strip() for p in
                                   re.split(r"(?<![^\s（(])[1-4][.、]\s*", ln.strip())
                                   if p.strip()]
    return [r for r in out if len(r["options"]) == 4]


def _marked_span(stem: str) -> str | None:
    """The bold span 問題1/2 underlines — the printed target, tail included."""
    m = re.findall(r"\*\*([^*]+)\*\*", stem)
    return m[0] if m else None


def _generated_keys(md: str) -> dict[int, int]:
    """{no: key} from whichever key-table shape the paper uses."""
    tail = md[md.find("# 解答"):] if "# 解答" in md else ""
    keys: dict[int, int] = {}
    for row in re.findall(r"^\|([^\n]*)\|\s*$", tail, re.M):
        cells = [c.strip() for c in row.split("|")]
        nums = [c for c in cells if re.fullmatch(r"\d+", c)]
        if len(nums) >= 2:
            no, key = int(nums[-2]), int(nums[-1])
            if 1 <= no <= 71 and 1 <= key <= 4:
                keys.setdefault(no, key)
    return keys


def generated_paper(test_id: str) -> list[dict]:
    md = (TESTS / test_id / "言語知識・読解.md")
    return generated_items(md.read_text(encoding="utf-8"), test_id) \
        if md.is_file() else []


# --------------------------------------------------------------------------
# Measures — every one of them applied identically to both corpora
# --------------------------------------------------------------------------
def register_class(stem: str) -> str:
    p = any(t in stem for t in PERSONAL)
    i = any(t in stem for t in INSTITUTIONAL)
    return "both" if p and i else "personal" if p else \
        "institutional" if i else "neutral"


def is_wago_set(options: list[str]) -> bool:
    """A 問題2 和語 item: any option carries okurigana/kana (§F3)."""
    return any(HIRAGANA.search(o) for o in options)


def is_bare_compound_set(options: list[str]) -> bool:
    """A 問題2 pseudo-compound grid item: all four are bare 2-kanji strings."""
    return all(len(o) == 2 and not KANA.search(o) for o in options)


def kana_tail(span: str) -> str:
    """The printed target's trailing kana — 「頻繁に」 -> 「に」 (§F9)."""
    m = re.search(r"([ぁ-ゟ]+)$", span or "")
    return m.group(1) if m else ""


def measures(items: list[dict]) -> dict:
    """Every number the 文字・語彙 rules cite, for one paper or one corpus."""
    by = lambda *ns: [r for r in items if r["mondai"] in ns]
    s125 = by(1, 2, 5)
    s15 = by(1, 2, 3, 4, 5)
    m: dict = {"n": len(items)}
    for tag, rows in (("125", s125), ("1", by(1)), ("2", by(2)), ("3", by(3)),
                      ("4", by(4)), ("5", by(5)), ("6", by(6))):
        lens = [jp(r["stem"]) for r in rows]
        if lens:
            m[f"stem_{tag}"] = {"n": len(lens), "median": statistics.median(lens),
                                "mean": round(sum(lens) / len(lens), 1),
                                "min": min(lens), "max": max(lens)}
    if s125:
        m["comma_free"] = sum("、" not in r["stem"] for r in s125) / len(s125)
    if s15:
        m["polite"] = sum(any(t in r["stem"] for t in POLITE)
                          for r in s15) / len(s15)
        m["polite_final"] = sum(bool(POLITE_FINAL.search(r["stem"]))
                                for r in s15) / len(s15)
        m["first_person"] = sum(any(t in r["stem"] for t in FIRST_PERSON)
                                for r in s15) / len(s15)
        cls = [register_class(r["stem"]) for r in s15]
        m["institutional"] = cls.count("institutional") / len(cls)
        m["personal"] = (cls.count("personal") + cls.count("both")) / len(cls)
        m["n_15"] = len(s15)
        m["n_institutional"] = cls.count("institutional")
    if by(2):
        rows = by(2)
        m["wago_2"] = sum(is_wago_set(r["options"]) for r in rows)
        m["compound_2"] = sum(is_bare_compound_set(r["options"]) for r in rows)
        m["n_2"] = len(rows)
        m["opt_len_2"] = [len(o) for r in rows for o in r["options"]]
    if by(6):
        m["opt_len_6"] = [jp(o) for r in by(6) for o in r["options"]]
    dup = option_reuse(items)
    m["option_reuse"] = {k: v for k, v in dup.items()}
    m["longest_key"] = longest_key_rate(by(5, 6))
    return m


def option_reuse(items: list[dict]) -> dict[int, list[str]]:
    """{mondai: [option strings printed in two items of that 大問]} (§F6)."""
    out: dict[int, list[str]] = {}
    for mondai in range(1, 7):
        where: dict[str, set[int]] = {}
        for r in items:
            if r["mondai"] != mondai:
                continue
            for o in r["options"]:
                where.setdefault(re.sub(r"\s+", "", o), set()).add(r["no"])
        rep = sorted(o for o, qs in where.items() if len(qs) > 1)
        if rep:
            out[mondai] = rep
    return out


def longest_key_rate(rows: list[dict]) -> tuple[int, int]:
    """(items keying the uniquely longest option, length-varying items)."""
    n = hit = 0
    for r in rows:
        lens = [jp(o) for o in r["options"]]
        k = r.get("key")
        if not k or len(set(lens)) < 2:
            continue
        n += 1
        if lens[k - 1] == max(lens) and lens.count(max(lens)) == 1:
            hit += 1
    return hit, n


def per_paper(items: list[dict]) -> dict[str, dict]:
    papers: dict[str, list[dict]] = {}
    for r in items:
        papers.setdefault(r["paper"], []).append(r)
    return {p: measures(rows) for p, rows in sorted(papers.items())}


def band(values: list[float]) -> str:
    vs = [v for v in values if v is not None]
    if not vs:
        return "n/a"
    return f"{min(vs):g}–{max(vs):g} (median {statistics.median(vs):g})"


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------
def _pct(x) -> str:
    return "n/a" if x is None else f"{x:.0%}"


def print_profile(label: str, items: list[dict]) -> None:
    pooled, papers = measures(items), per_paper(items)
    print(f"\n{label}: {len(papers)} paper(s), {pooled['n']} items, "
          f"{pooled['n'] * 4} options")
    for tag in ("1", "2", "3", "4", "5", "6"):
        s = pooled.get(f"stem_{tag}")
        if s:
            print(f"  問題{tag} stem  n={s['n']:<4} median {s['median']:<5g} "
                  f"mean {s['mean']:<5} range {s['min']}–{s['max']}")
    print(f"  問題1/2/5 per-paper median stem: "
          f"{band([p['stem_125']['median'] for p in papers.values() if 'stem_125' in p])}")
    print(f"  comma-free share (問題1/2/5):     "
          f"{band([round(p['comma_free'] * 100) for p in papers.values() if 'comma_free' in p])} %")
    print(f"  polite share (問題1–5):           "
          f"{band([round(p['polite'] * 100) for p in papers.values() if 'polite' in p])} %")
    print(f"  institution-actor share:         "
          f"{band([round(p['institutional'] * 100) for p in papers.values() if 'institutional' in p])} %")
    print(f"  問題4 per-paper median / max:     "
          f"{band([p['stem_4']['median'] for p in papers.values() if 'stem_4' in p])}"
          f" / max {max((p['stem_4']['max'] for p in papers.values() if 'stem_4' in p), default=0)}")
    print(f"  問題2 和語 items per paper:        "
          f"{band([p['wago_2'] for p in papers.values() if 'wago_2' in p])}")
    print(f"  問題2 bare-compound items:        "
          f"{band([p['compound_2'] for p in papers.values() if 'compound_2' in p])}")
    ol6 = pooled.get("opt_len_6") or []
    if ol6:
        print(f"  問題6 option sentences: n={len(ol6)} mean "
              f"{sum(ol6) / len(ol6):.1f} median {statistics.median(ol6):g} "
              f"range {min(ol6)}–{max(ol6)}")
    hit, n = pooled["longest_key"]
    if n:
        print(f"  問題5/6 longest-key rate: {hit}/{n} = {hit / n:.0%}")
    print("  repeated option inside one 大問, per paper "
          "(pooled across papers is meaningless — official repeats none):")
    for p, mm in papers.items():
        flags = [f"問題{k}: {', '.join(v)}" for k, v in mm["option_reuse"].items()]
        if flags:
            print(f"    {p}: {'; '.join(flags)}")
    if not any(mm["option_reuse"] for mm in papers.values()):
        print("    none")


def print_paper_matrix(items: list[dict]) -> None:
    """The per-paper work matrix (§5.4) — regenerated, never retyped."""
    print("\n| paper | stem125 | comma-free | polite | 和 | 熟 | 問4 med/max | "
          "inst | reuse |")
    print("|---|---|---|---|---|---|---|---|---|")
    for p, m in per_paper(items).items():
        print(f"| `{p}` | {m.get('stem_125', {}).get('median', '-'):g} | "
              f"{_pct(m.get('comma_free'))} | {_pct(m.get('polite'))} | "
              f"{m.get('wago_2', '-')} | {m.get('compound_2', '-')} | "
              f"{m.get('stem_4', {}).get('median', '-'):g}/"
              f"{m.get('stem_4', {}).get('max', '-')} | "
              f"{_pct(m.get('institutional'))} | "
              f"{'; '.join(f'問題{k}: ' + ', '.join(v) for k, v in m['option_reuse'].items()) or '-'} |")


def baseline() -> None:
    """The official tables in the Markdown the owner docs carry (§D1)."""
    allera, cur = official_items("all"), official_items("cur")
    for label, rows in (("all 31 sittings", allera), ("current era (n=7)", cur)):
        pooled, papers = measures(rows), per_paper(rows)
        print(f"\n### {label} — {len(papers)} sittings, {pooled['n']} items "
              f"parsed\n")
        print("| measure | n | median | mean | range | per-paper band |")
        print("|---|---|---|---|---|---|")
        for tag in ("1", "2", "3", "4", "5"):
            s = pooled.get(f"stem_{tag}")
            if not s:
                continue
            pp = [p[f"stem_{tag}"]["median"] for p in papers.values()
                  if f"stem_{tag}" in p]
            print(f"| 問題{tag} stem (JP chars) | {s['n']} | {s['median']:g} | "
                  f"{s['mean']} | {s['min']}–{s['max']} | {band(pp)} |")
        ol6 = pooled["opt_len_6"]
        print(f"| 問題6 option sentence | {len(ol6)} | "
              f"{statistics.median(ol6):g} | {sum(ol6) / len(ol6):.1f} | "
              f"{min(ol6)}–{max(ol6)} | — |")
        hit, n = pooled["longest_key"]
        print(f"\n- 問題1/2/5 per-paper median stem: "
              f"{band([p['stem_125']['median'] for p in papers.values()])}")
        print(f"- comma-free 問題1/2/5 stems: "
              f"{band([round(p['comma_free'] * 100) for p in papers.values()])} %")
        print(f"- any polite marker, 問題1–5: "
              f"{band([round(p['polite'] * 100) for p in papers.values()])} %"
              f"; sentence-final "
              f"{band([round(p['polite_final'] * 100) for p in papers.values()])} %")
        print(f"- first person: "
              f"{band([round(p['first_person'] * 100) for p in papers.values()])} %"
              f"; institution-actor "
              f"{band([round(p['institutional'] * 100) for p in papers.values()])} %")
        print(f"- 問題2 和語 items of 5: "
              f"{band([p['wago_2'] for p in papers.values() if 'wago_2' in p])}"
              f"; bare 2-kanji items of 5: "
              f"{band([p['compound_2'] for p in papers.values() if 'compound_2' in p])}")
        print(f"- 問題4 stem per-paper median: "
              f"{band([p['stem_4']['median'] for p in papers.values() if 'stem_4' in p])}"
              f", longest single stem "
              f"{max(p['stem_4']['max'] for p in papers.values() if 'stem_4' in p)}")
        print(f"- 問題5/6 uniquely-longest-key rate: {hit}/{n} = {hit / n:.0%}")
        reuse = sum(len(v) for p in papers.values()
                    for v in p["option_reuse"].values())
        print(f"- repeated option inside one 大問: {reuse} across "
              f"{len(papers)} sittings")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--official", action="store_true")
    ap.add_argument("--tests", nargs="*", default=None)
    ap.add_argument("--era", choices=("cur", "all"), default="all")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--matrix", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.baseline:
        baseline()
        return 0
    items: list[dict] = []
    if a.official or a.tests is None and not a.matrix:
        items += official_items(a.era)
    if a.tests is not None or a.matrix or not a.official:
        ids = a.tests or [d.name for d in sorted(TESTS.iterdir())
                          if d.is_dir() and not d.name.startswith("imported-")]
        gen = [r for t in ids for r in generated_paper(t)]
        if a.json:
            print(json.dumps(per_paper(gen), ensure_ascii=False, indent=1,
                             default=str))
            return 0
        if a.matrix:
            print_paper_matrix(gen)
            return 0
        items += gen
    if a.json:
        print(json.dumps(per_paper(items), ensure_ascii=False, indent=1,
                         default=str))
        return 0
    for corpus in ("official", "generated"):
        rows = [r for r in items if r["corpus"] == corpus]
        if rows:
            print_profile(corpus, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
