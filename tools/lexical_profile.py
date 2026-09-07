#!/usr/bin/env python3
"""Lexical-load measurement for 読解 prose and 聴解 scripts — ONE parser, both
corpora, two consumers.

Why this file exists (audit 2026-09-07). Every 読解 difficulty number the rules
were built on measured the SHAPE of the prose — passage length, sentence length,
kanji density, （注N） counts — and all four can sit inside their bands while the
paper is far harder than any official sitting, because none of them can see
WHICH WORDS the passage uses. Measured across all 31 official sittings and all 23
generated papers, with leave-one-out on both sides:

    words absent from every other N2 source   official cur  10.2–16.4 %  (med 12.2)
                                              official all   8.4–20.9 %  (med 15.5)
                                              generated     12.9–29.9 %  (med 21.2)

Every generated paper sat above the current-era official median and the four most
recent sat above all 31 official papers, while `make check` was green. The
qualitative split is the finding: official papers' novel words are invented names
and transparent compounds (森田様, 回収日, 割引後), generated papers' are
specialist terminology (約款, 血小板, 内水氾濫, 経管栄養, 逐語訳) — which is why
the generated papers also gloss 36–50 % of their novel words against official's
13 %. Kanji DENSITY is flat across the same 23 papers (Spearman +0.05); novelty
climbs (+0.72). Density was the wrong instrument.

So the measurement lives here, once:

  * `tools/check_consistency.py` imports this module for its novelty checks —
    the gate keeps owning the THRESHOLDS, this file owns the MEASUREMENT;
  * `--baseline` prints the official tables in the Markdown shape
    `dokkai.md` / `official_calibration.md` carry, so refreshing a doc is a
    paste, not a retype.

METHOD, stated once, because every number below depends on it:

  * **Word proxy** — a maximal kanji run of 2–4 characters bounded by non-kanji
    (`WORD`). No tokenizer is installed and none is a dependency of this repo, so
    this is a proxy: it sees Sino-Japanese compounds, which is where the load
    actually sits, and misses kana and okurigana vocabulary entirely. It is
    applied IDENTICALLY to both corpora, and the kanji-run length distributions
    match (official mean 2.30, generated 2.23), so it is not skewed by one side.
  * **Reference** — every OTHER sitting's `booklet.md` + `script.md` in
    `refs/JLPT_N2_NEW/`, plus the six textbook extracts — of which
    `refs/Hajimete/vocab_reference.md`, a curated 2500-word N2 list, is the one
    that speaks most directly to the question. A word in any of them is
    demonstrably N2 material.
  * **Leave-one-out** — an official paper is scored against the other 30
    sittings, never against itself. A generated paper is scored against all 31,
    i.e. a LARGER reference than official papers get, so the comparison is
    conservative against this module's own finding.
  * **Glosses are credit** — a word defined in a `（注N）用語：定義` line is not
    novel load; it is apparatus. `unglossed_per_1k` is the number the gate reads.

Usage:
    python3 tools/lexical_profile.py --official [--era cur|all]
    python3 tools/lexical_profile.py --tests 20260904_3 …   (default: every test)
    python3 tools/lexical_profile.py --baseline [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "refs" / "JLPT_N2_NEW"
TESTS = ROOT / "tests"
SHINKANZEN = ROOT / "refs" / "Shinkanzen"
SOUMATOME = ROOT / "refs" / "Soumatome"

sys.path.insert(0, str(ROOT / "tools"))

# The word proxy. Bounded on both sides so 「東京都庁」 yields one 4-char token
# rather than three overlapping bigrams — cross-boundary bigrams are noise that
# a run-length difference between corpora would turn into a false signal.
WORD = re.compile(r"(?<![一-鿿])([一-鿿]{2,4})(?![一-鿿])")
KANJI = re.compile(r"[一-鿿]")
JP_CHAR = re.compile(r"[぀-ヿ一-鿿ー。、！？（）「」『』…・]")

# `（注3）魚粉：いわし…` -> headword 魚粉. Both the official spacing
# (`（注1） 気がね：遠慮`) and the generated one (`（注1）過疎：…`) parse.
GLOSS_HEAD = re.compile(r"[（(]注\s*\d*[）)]\s*([^：:）)\n]{1,20})\s*[：:]")

# The SIX textbook extracts. Every one is tracked in git (`AGENTS.md` §3), so
# this module works on a fresh clone with no `refs/` binaries present.
HAJIMETE = ROOT / "refs" / "Hajimete"

TEXTBOOK_EXTRACTS = (
    SHINKANZEN / "dokkai_reference.md",
    SHINKANZEN / "goi_reference.md",
    SHINKANZEN / "choukai_script.md",
    SHINKANZEN / "kanji_tables.md",
    SOUMATOME / "goi_reference.md",
    # Added 2026-09-07. The other four are graded EXERCISE volumes, so what they
    # contribute is the incidental vocabulary of drill prose; this one is a flat,
    # curated 2500-word N2 list, which is a much better statement of "a word an
    # N2 candidate has met" — the exact judgement this module exists to make.
    # `_read()` returns "" when it is absent, so a clone without it degrades to
    # the previous reference rather than failing; the gate's numbers move when it
    # lands, which is why `check_dokkai_lexical_load`'s thresholds are documented
    # as refreshable from `--baseline`.
    HAJIMETE / "vocab_reference.md",
)

CURRENT_ERA = (
    "13. N2 12-2022", "14. N2 7-2023", "14. N2 12-2023", "15. N2 7-2024",
    "15. N2 12-2024", "16. N2 7-2025", "17.N2 12-2025",
)


# Numeral runs are not vocabulary. 「六十五歳」「十五分」「五年以上」「二千円」 are
# spelled in kanji throughout both corpora and parse as 2–4-char kanji runs, so
# without this filter a paper's "novel words" list is padded with arithmetic that
# no reader has to learn. Dropping them changes both corpora identically; it was
# added because the gate's own failure message was being diluted by them, and the
# thresholds in `check_consistency.py` were re-derived afterwards.
_NUMERAL = "〇一二三四五六七八九十百千万億兆数何"
_COUNTER = ("歳", "分", "年", "円", "人", "回", "日", "月", "時", "件", "個", "番",
            "度", "割", "名", "冊", "軒", "台", "枚", "本", "秒", "週", "階",
            "点", "組", "種", "倍", "頭", "匹", "泊", "限", "以上", "以下",
            "以内", "程度", "余", "半", "代", "位", "階建", "人前", "年間",
            "週間", "日間", "時間", "か月", "ヶ月")


def _is_numeral_run(word: str) -> bool:
    """True for 「六十五歳」「十五分」「二年」「三十」 — a number, optionally with a
    counter, and nothing else."""
    body = word
    for c in sorted(_COUNTER, key=len, reverse=True):
        if body.endswith(c):
            body = body[: -len(c)]
            break
    return bool(body) and all(ch in _NUMERAL for ch in body)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except (FileNotFoundError, NotADirectoryError):
        return ""


def words(text: str) -> list[str]:
    return [w for w in WORD.findall(text) if not _is_numeral_run(w)]


def gloss_headwords(raw: str) -> set[str]:
    """Kanji-words appearing in a `（注N）` DEFINITION LINE's headword."""
    out: set[str] = set()
    for head in GLOSS_HEAD.findall(raw):
        out.update(words(head))
    return out


# --------------------------------------------------------------------------
# Reference corpus
# --------------------------------------------------------------------------

@dataclass
class Reference:
    """Per-sitting vocabularies plus the textbook floor, so leave-one-out is a
    set subtraction rather than 31 re-reads."""
    sittings: dict[str, set[str]] = field(default_factory=dict)
    textbook: set[str] = field(default_factory=set)
    _full: set[str] | None = None

    @property
    def available(self) -> bool:
        return bool(self.sittings) and bool(self.textbook)

    def full(self) -> set[str]:
        if self._full is None:
            v = set(self.textbook)
            for w in self.sittings.values():
                v |= w
            self._full = v
        return self._full

    def excluding(self, sitting: str | None) -> set[str]:
        if sitting is None or sitting not in self.sittings:
            return self.full()
        v = set(self.textbook)
        for name, w in self.sittings.items():
            if name != sitting:
                v |= w
        return v


_REFERENCE: Reference | None = None


def reference() -> Reference:
    """Built once per process — 36 file reads, ~4 MB."""
    global _REFERENCE
    if _REFERENCE is not None:
        return _REFERENCE
    ref = Reference()
    if REFS.is_dir():
        for d in sorted(p for p in REFS.iterdir() if p.is_dir()):
            vocab = set(words(_read(d / "booklet.md")))
            vocab |= set(words(_read(d / "script.md")))
            if vocab:
                ref.sittings[d.name] = vocab
    for f in TEXTBOOK_EXTRACTS:
        ref.textbook |= set(words(_read(f)))
    _REFERENCE = ref
    return ref


# --------------------------------------------------------------------------
# Per-paper measurement
# --------------------------------------------------------------------------

@dataclass
class LexProfile:
    corpus: str
    paper: str
    prose_chars: int = 0
    word_tokens: int = 0
    novel_tokens: int = 0
    unglossed_tokens: int = 0
    gloss_headwords: int = 0
    novel_share: float = 0.0          # % of word tokens that are novel
    unglossed_share: float = 0.0
    unglossed_per_1k: float = 0.0     # THE number the gate reads
    novel_words: list[str] = field(default_factory=list)
    unglossed_words: list[str] = field(default_factory=list)


def _profile(corpus: str, paper: str, prose: str, raw: str,
             exclude_sitting: str | None) -> LexProfile:
    ref = reference()
    known = ref.excluding(exclude_sitting)
    glossed = gloss_headwords(raw)
    toks = words(prose)
    p = LexProfile(corpus=corpus, paper=paper,
                   prose_chars=len(JP_CHAR.findall(prose)),
                   word_tokens=len(toks),
                   gloss_headwords=len(glossed))
    if not toks or not p.prose_chars:
        return p
    novel = [w for w in toks if w not in known]
    unglossed = [w for w in novel if w not in glossed]
    p.novel_tokens = len(novel)
    p.unglossed_tokens = len(unglossed)
    p.novel_share = 100.0 * len(novel) / len(toks)
    p.unglossed_share = 100.0 * len(unglossed) / len(toks)
    p.unglossed_per_1k = 1000.0 * len(unglossed) / p.prose_chars
    p.novel_words = sorted(set(novel))
    p.unglossed_words = sorted(set(unglossed))
    return p


_DOKKAI_MOD = None


def _dokkai():
    """`dokkai_profile` owns passage extraction — one parser, per `AGENTS.md` §4.
    Imported lazily so `--help` works without it, and registered in
    `sys.modules` before execution because `@dataclass` resolves a class's
    `__module__` through it (a bare `module_from_spec` gives `None.__dict__`)."""
    global _DOKKAI_MOD
    if _DOKKAI_MOD is None:
        import importlib.util
        path = ROOT / "tools" / "dokkai_profile.py"
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = mod
        spec.loader.exec_module(mod)
        _DOKKAI_MOD = mod
    return _DOKKAI_MOD


def _prose_of(pp) -> str:
    """問題10–13 passage prose. 問題14 is excluded: its flyer is dates, prices and
    place names, so a novelty measure over it reports the invented town's name."""
    return "\n".join(x.text for x in pp.passages if x.section in (10, 11, 12, 13))


def profile_official(era: str = "cur") -> list[LexProfile]:
    D = _dokkai()
    out = []
    for pp in D.profile_official(era=era):
        raw = _read(REFS / pp.paper / "booklet.md")
        out.append(_profile("official", pp.paper, _prose_of(pp), raw, pp.paper))
    return out


def profile_tests(test_ids: list[str] | None = None) -> list[LexProfile]:
    D = _dokkai()
    out = []
    for pp in D.profile_tests(test_ids):
        raw = _read(TESTS / pp.paper / "言語知識・読解.md").split("\n# 解答")[0]
        # An import IS an official sitting retyped, so it must not be scored
        # against a reference containing itself. Map it back to its archive
        # folder when one is present; otherwise score it like a generated paper
        # and let the caller read the corpus label.
        exclude = _import_sitting(pp.paper)
        corpus = "imported" if pp.paper.startswith("imported-") else "generated"
        out.append(_profile(corpus, pp.paper, _prose_of(pp), raw, exclude))
    return out


_IMPORT_RE = re.compile(r"^imported-n2-(\d{4})-(\d{2})$")


def _import_sitting(test_id: str) -> str | None:
    """`imported-n2-2025-12` -> `17.N2 12-2025`, by matching the archive folder
    names rather than hard-coding the map (folder prefixes change)."""
    m = _IMPORT_RE.match(test_id)
    if not m:
        return None
    year, month = m.group(1), str(int(m.group(2)))
    for name in reference().sittings:
        if re.search(rf"\b{month}-{year}\b", name.replace(".", ". ")):
            return name
    return None


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def _band(vals: list[float], fmt: str = "{:.2f}") -> str:
    if not vals:
        return "n/a"
    return (f"{fmt.format(statistics.median(vals))} "
            f"[{fmt.format(min(vals))}–{fmt.format(max(vals))}]")


def print_profiles(profiles: list[LexProfile]) -> None:
    print(f"{'corpus':10}{'paper':22}{'chars':>7}{'words':>7}"
          f"{'novel%':>9}{'unglossed%':>12}{'unglossed/1k':>14}{'glossHW':>9}")
    for p in profiles:
        print(f"{p.corpus:10}{p.paper:22}{p.prose_chars:7}{p.word_tokens:7}"
              f"{p.novel_share:9.2f}{p.unglossed_share:12.2f}"
              f"{p.unglossed_per_1k:14.2f}{p.gloss_headwords:9}")


def format_baseline_tables() -> str:
    off_cur = profile_official("cur")
    off_all = profile_official("all")
    off_old = [p for p in off_all if p.paper not in CURRENT_ERA]
    tests = profile_tests()
    gen = [p for p in tests if p.corpus == "generated"]

    L = []
    L.append("# 読解 lexical-load baseline "
             "(measured by `tools/lexical_profile.py`)")
    L.append("")
    L.append("Word proxy: a kanji run of 2–4 chars bounded by non-kanji, over "
             "問題10–13 passage prose. Reference: every OTHER sitting's "
             "`booklet.md` + `script.md` plus the five textbook extracts — "
             "leave-one-out for official papers, all 31 sittings for generated "
             "ones (a LARGER reference, so the gap below is conservative). "
             "`（注N）`-defined headwords are credited as apparatus, not load.")
    L.append("")
    L.append("| corpus | n | novel words, % of tokens | UNGLOSSED novel / 1000 chars | gloss headwords |")
    L.append("|---|---|---|---|---|")
    for label, rows in (("official, current era (12/2022–12/2025)", off_cur),
                        ("official, 2010–7/2022", off_old),
                        ("generated", gen)):
        if not rows:
            continue
        L.append(f"| {label} | {len(rows)} | "
                 f"{_band([p.novel_share for p in rows])} | "
                 f"{_band([p.unglossed_per_1k for p in rows])} | "
                 f"{_band([float(p.gloss_headwords) for p in rows], '{:.0f}')} |")
    L.append("")
    if off_cur:
        vals = [p.unglossed_per_1k for p in off_cur]
        L.append(f"**The gate reads `unglossed_per_1k`.** Official current era "
                 f"measures {min(vals):.2f}–{max(vals):.2f} "
                 f"(median {statistics.median(vals):.2f}); the ceiling sits above "
                 f"the observed maximum, as every threshold in this repo does.")
        L.append("")
        hw = [p.gloss_headwords for p in off_cur]
        L.append(f"**Gloss headwords are capped, not floored.** Official current "
                 f"era carries {min(hw)}–{max(hw)} kanji-word gloss headwords per "
                 f"paper; a paper that needs many more is importing a technical "
                 f"register and paying for it with footnotes.")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--official", action="store_true")
    ap.add_argument("--tests", nargs="*", default=None)
    ap.add_argument("--era", choices=("cur", "all"), default="cur")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--words", metavar="PAPER",
                    help="list one paper's unglossed novel words")
    a = ap.parse_args()

    if not reference().available:
        print("lexical_profile: no reference corpus on this machine — "
              "`refs/JLPT_N2_NEW/*/booklet.md` and the textbook extracts are "
              "tracked in git; a clone missing them is broken, not offline.",
              file=sys.stderr)
        return 2

    if a.baseline:
        if a.json:
            rows = profile_official("all") + profile_tests()
            print(json.dumps([r.__dict__ for r in rows], ensure_ascii=False,
                             indent=2, default=list))
        else:
            print(format_baseline_tables())
        return 0

    profiles: list[LexProfile] = []
    if a.official:
        profiles += profile_official(a.era)
    if a.tests is not None or not a.official:
        profiles += profile_tests(a.tests or None)

    if a.words:
        for p in profiles:
            if p.paper == a.words:
                print(f"{p.paper}: {p.unglossed_tokens} unglossed novel tokens, "
                      f"{len(p.unglossed_words)} distinct")
                print("  " + " ".join(p.unglossed_words))
                return 0
        print(f"no such paper: {a.words}", file=sys.stderr)
        return 2

    print_profiles(profiles)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
