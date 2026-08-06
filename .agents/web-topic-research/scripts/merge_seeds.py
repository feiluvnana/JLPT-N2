#!/usr/bin/env python3
"""
Blend web-harvested topic seeds into test_spec.json — ACROSS THE WHOLE EXAM,
with balance caps so neither the web nor the pool/Shin-Kanzen side dominates.

Usage:
    python merge_seeds.py logs/seeds.json tests/<test_id>/test_spec.json
    python merge_seeds.py logs/seeds.json tests/<test_id>/test_spec.json --reading-ratio 0.5 --listening-ratio 0.4

seeds.json format (written by the agent after web research):
[
  {"seed": "無人店舗の増加", "facts": ["コンビニ大手が実験店を拡大"], "source": "https://..."},
  {"seed": "置き配の定着",   "facts": ["再配達率が約1割まで低下"],   "source": "https://..."}
]
Optional per-seed keys: "surfaces": ["reading","listening","carrier","info"]
(hint about where a seed fits best; omitted = usable anywhere).

Surfaces touched in test_spec.json:
- items.reading_topics        ~reading-ratio replaced by web seeds (問題10-13)
- items.listening_scenarios   ~listening-ratio replaced by web setting seeds
- cloze_topic                 問題9 passage topic: 50/50 web vs pool (RNG)
- info_retrieval_texture      問題14 flyer: one numeric-fact seed if available
- carrier_seeds               問題1-8 example/carrier sentences: texture only
- qr_situation_seeds          問題4 即時応答: up to 3 situational settings

PRE-FLIGHT (all three abort before anything is blended):
- validate_harvest()   harvest hygiene: no two seeds may cite the same source
                       URL, and the harvest must span >= MIN_HARVEST_DOMAINS
                       distinct netlocs. The domain count is printed either way.
- check_topic_reuse()  cross-test topic hygiene: no seed may share a >=2-char
                       content token with a subject either of the previous two
                       tests already used (logs/topics.json; a file that is
                       genuinely absent is tolerated and loudly reported, a file
                       that is present but unreadable is fatal).
                       This is a FLOOR, not the rule — see the function docstring.
- ledger_entry()       the spec's test must already exist in logs/ledger.json,
                       because the harvest_sha stamp written at the end has
                       nowhere to land otherwise (see the function docstring).

SIBLING FILES ARE RESOLVED FROM THE REPO ROOT, NOT FROM THE SPEC OR THE CWD.
logs/ledger.json and logs/topics.json are repo-level state; specs moved from
logs/test_spec.json to tests/<test_id>/test_spec.json (commit 383c83a) and the
two `spec_path.parent / …` lookups left behind pointed at tests/<id>/ledger.json
and tests/<id>/topics.json, which never exist. Both failures were silent: the
harvest_sha stamp went nowhere (exactly the unrecorded-sha hole AGENTS.md §4
now fails on) and the cross-test topic abort printed "no history yet" on every
run in its life. ROOT comes from __file__ so it is also cwd-independent.

ALLOCATION: a small texture cut (info/qr/carrier) is reserved FIRST so every
surface receives seeds even with a thin harvest; the remaining seeds fund
reading/listening, scaled down proportionally if supply < demand. The skill's
recommended harvest (18-25 seeds, >=6 domains — MAX_PER_DOMAIN=2 makes fewer
domains unable to fund every surface's 30% floor) funds all surfaces at full
target ratios.

BALANCE INVARIANTS (enforced, not advisory):
- Web share per replaced surface is clamped to [MIN_WEB, MAX_WEB] = [0.30, 0.60]
  where supply allows. The pool (Shin-Kanzen-calibrated) side always keeps
  >= 40% of every surface.
- No single source domain may supply more than MAX_PER_DOMAIN (2) topic-level
  blended seeds (reading/listening/cloze/info); with fewer than MIN_DOMAINS
  (3) distinct domains, target ratios are scaled down (a one-source test is
  a dominant-source test).
- Tested LINGUISTIC items (grammar points, words, kanji, idioms/keigo) are
  never replaced — the web supplies topics/settings/facts only.

Every blended entry carries {"origin": "pool"|"web", "source": url?} so any
test can be audited. The RNG derives from the spec's own seed: reproducible.
"""

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]            # .agents/web-topic-research/scripts -> repo root
LOGS_DIR = ROOT / "logs"
LEDGER = LOGS_DIR / "ledger.json"   # written by sample_items.py, stamped here
TOPICS = LOGS_DIR / "topics.json"   # written by the build pass; see the SKILL

MIN_WEB = 0.30
MAX_WEB = 0.60
MAX_PER_DOMAIN = 2
MIN_DOMAINS = 3
MIN_HARVEST_DOMAINS = 6   # web-topic-research Step 1: 2 x domains caps the blend
QR_SEEDS = 3          # max situational seeds attached for 即時応答
CARRIER_SEEDS = 6     # max texture seeds attached for 問題1-8 carrier sentences

TOPIC_LOOKBACK = 2        # how many previous tests' subjects block a seed


def domain_of(seed: dict) -> str:
    try:
        return urlparse(seed.get("source", "")).netloc or "unknown"
    except ValueError:
        return "unknown"


def validate_harvest(seeds: list[dict]) -> None:
    """Refuse a harvest that cannot honestly fund a blend.

    Nothing used to look at seeds.json at all, so two failures were invisible:

    1. **Two seeds from one document are one seed.** The harvest on disk when
       this check was written (test 3's) had 22 seeds over 14 domains, but THREE
       of them cited the identical URL (`www.env.go.jp/…/h23_lca_01.pdf`), and
       two of the facts attributed to it are not in that document — mining one
       PDF for three "topics" produces one subject wearing three hats plus
       invented facts. Drop the weaker seeds; do not re-title them.
    2. **Domains, not seed count, cap the blend.** MAX_PER_DOMAIN is 2 and that
       budget is shared across every topic-level surface, so N domains fund at
       most 2N picks. Six domains funds the 30% floor (12 picks) exactly; test 4
       harvested 28 seeds from 5 domains and 聴解 finished at 20% web.

    Both abort rather than warn: a bad harvest cannot be repaired downstream,
    and every surface authored off a starved blend has to be rewritten.
    """
    sources = [s.get("source", "") for s in seeds]
    domains = {domain_of(s) for s in seeds} - {"unknown"}
    print(f"harvest: {len(seeds)} seed(s), domains={len(domains)} "
          f"(minimum {MIN_HARVEST_DOMAINS})")

    problems = []
    dupes = sorted({u for u in sources if u and sources.count(u) > 1})
    for url in dupes:
        names = [s.get("seed", "?") for s in seeds if s.get("source") == url]
        problems.append(f"{len(names)} seeds cite one URL {url} -> {names}; "
                        f"two seeds from one document are one seed — keep the "
                        f"strongest and re-harvest the rest")
    missing = [s.get("seed", "?") for s in seeds if not s.get("source")]
    if missing:
        problems.append(f"seeds with no source URL: {missing}; every seed must "
                        f"come from a page you actually fetched")
    if len(domains) < MIN_HARVEST_DOMAINS:
        problems.append(
            f"only {len(domains)} distinct source domain(s) "
            f"({', '.join(sorted(domains)) or 'none'}); "
            f"MAX_PER_DOMAIN={MAX_PER_DOMAIN} means that funds at most "
            f"{2 * len(domains)} topic-level picks, below the "
            f"{MIN_HARVEST_DOMAINS}-domain / 12-pick 30% floor")
    if problems:
        raise SystemExit("harvest rejected (logs/seeds.json):\n  - "
                         + "\n  - ".join(problems))

    # Non-fatal: two seeds on adjacent subjects get blended onto two different
    # surfaces and read as one topic tested twice (tests 2 and 3 both put
    # フードドライブ in 聴解問題1 AND in the 問題14 fine print). Distinct URLs,
    # so the duplicate-source check above cannot see it.
    # Bar is >=3 chars here, not the >=2 of the cross-test abort: this pass is
    # O(n^2) over one harvest and a 2-char compound (削減/活用/返却) matches
    # anything, so it would bury the real hits (地域通貨, 熱中症予防) in noise.
    for i, a in enumerate(seeds):
        for b in seeds[i + 1:]:
            shared = sorted(t for t in (content_tokens(a.get("seed", ""))
                                        & content_tokens(b.get("seed", "")))
                            if len(t) >= 3)
            if shared:
                print(f"  warning: near-duplicate subjects share {shared} — "
                      f"「{a.get('seed')}」 / 「{b.get('seed')}」; each seed feeds "
                      f"exactly ONE surface, so drop the weaker one")


def content_tokens(text: str) -> set[str]:
    """>=2-char content tokens: kanji runs, katakana runs, latin words.

    Hiragana is deliberately excluded — it carries the grammar, not the subject.
    Tokens are MAXIMAL runs, compared for equality, so 「地域通貨」 matches
    「地域通貨」 and not 「地域猫」. That is the intended conservatism: this feeds a
    hard abort, so it must not fire on two subjects that merely share 生活.
    All-digit tokens are dropped (a shared 2024 is not a shared subject).
    """
    t = str(text)
    toks = set(re.findall(r"[一-鿿]{2,}", t))
    toks |= set(re.findall(r"[ァ-ヶー]{2,}", t))
    toks |= {w.lower() for w in re.findall(r"[A-Za-z0-9]{2,}", t)
             if not w.isdigit()}
    return toks


def previous_subjects(topics_path: Path, lookback: int = TOPIC_LOOKBACK,
                      test_id=None) -> list[tuple[str, str, str]]:
    """[(test_id, surface, subject)] for the last `lookback` tests on record.

    Tolerates a file that is genuinely absent: logs/topics.json is written by
    the build pass, so the first test generated after this check landed has
    nothing to compare to. A file that IS there but cannot be read as history
    is fatal instead — a guard that shrugs at a corrupt history file reports
    "nothing to compare" and looks exactly like a pass.
    Accepts the canonical {"version":1,"history":[…]} container and the two
    obvious variants ({"tests":[…]} / a bare list) so a hand-written file still
    reads.
    """
    if not topics_path.exists():
        return []
    try:
        data = json.loads(topics_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"{topics_path} exists but could not be read as the "
                         f"topic history ({exc}); the cross-test topic check "
                         f"cannot run. Repair the file — do not delete it to "
                         f"fall back on the tolerated-absent path.")
    if isinstance(data, dict):
        rows = data.get("history") or data.get("tests") or []
    elif isinstance(data, list):
        rows = data
    else:
        raise SystemExit(f"{topics_path} is not a topic history "
                         f"({type(data).__name__}); expected "
                         f'{{"version":1,"history":[…]}}')
    rows = [r for r in rows if isinstance(r, dict)
            and (test_id is None or str(r.get("test_id")) != str(test_id))]
    out = []
    for row in rows[-lookback:]:
        for surface, subject in (row.get("surfaces") or {}).items():
            if subject:
                out.append((str(row.get("test_id")), surface, str(subject)))
    return out


def check_topic_reuse(seeds: list[dict], topics_path: Path, test_id=None) -> None:
    """Abort when a seed reuses a subject from either of the previous two tests.

    `(--seed, harvest_sha)` uniqueness is NOT topic uniqueness, and that gap
    shipped three re-skins through a green gate: test 2 repeated test 1's urban
    greening in the same 問題11 slot, and tests 3/4 shared 8 surfaces including a
    地域通貨 flyer that matched down to 20% / 2,000pt and the same ※ note.

    HONEST LIMIT — read this before trusting it. Token overlap is a FLOOR, not
    the rule. 「屋上緑化」 vs 「グリーンパートナー制度」 and 「みどりコイン」 vs
    「さくらコイン」 are the same subject with ZERO shared tokens, and this
    function passes both. Subject identity cannot be mechanized. The whole-paper
    topic table done by a human (jlpt-test-generation §"One topic, one surface")
    stays mandatory; this catches only the easy half — literal reuse.
    """
    prev = previous_subjects(topics_path, test_id=test_id)
    if not prev:
        # Say WHICH of the two very different situations this is, and say it
        # against the absolute path. The old message ("no topics.json history
        # yet") was printed on every run for the life of this check, because
        # the path it probed was tests/<id>/topics.json — a file that never
        # exists. An operator read that as information; it was a broken guard.
        why = ("the file does not exist" if not topics_path.exists() else
               f"it records no subjects outside test {test_id}")
        print(f"  WARNING: cross-test topic check SKIPPED — {topics_path}: "
              f"{why}. Nothing blocks a repeat of the previous papers' "
              f"subjects this run; the human whole-paper topic table "
              f"(jlpt-test-generation §'One topic, one surface') is the only "
              f"guard. Confirm in your report that you did it.")
        return
    tests = sorted({t for t, _, _ in prev})
    index = [(t, surf, subj, content_tokens(subj)) for t, surf, subj in prev]

    hard, soft = [], []
    for s in seeds:
        stoks = content_tokens(s.get("seed", ""))
        if not stoks:
            continue
        for t, surf, subj, ptoks in index:
            shared = sorted(stoks & ptoks)
            if shared:
                hard.append(f"seed 「{s.get('seed')}」 shares {shared} with "
                            f"test {t} {surf} 「{subj}」")
                continue
            near = sorted({f"{a}~{b}" for a in stoks for b in ptoks
                           if a != b and (a in b or b in a)})
            if near:
                soft.append(f"seed 「{s.get('seed')}」 ~ test {t} {surf} "
                            f"「{subj}」 ({', '.join(near)})")
    for line in soft:
        print(f"  warning: possible topic overlap — {line}")
    if hard:
        raise SystemExit(
            "topic reuse against test(s) " + ", ".join(tests) + " "
            f"(from {topics_path}):\n  - " + "\n  - ".join(hard)
            + "\nRe-harvest the colliding seeds. Token overlap is only the "
              "floor: also re-check the whole-paper topic table by hand — a "
              "renamed subject (屋上緑化 -> グリーンパートナー制度) passes this "
              "check and is still a re-skin.")
    print(f"  topic check: {len(seeds)} seed(s) vs {len(prev)} subject(s) from "
          f"test(s) {', '.join(tests)} — no shared content token")


def fits(seed: dict, surface: str) -> bool:
    surfs = seed.get("surfaces")
    return not surfs or surface in surfs


def has_number(seed: dict) -> bool:
    return any(any(c.isdigit() for c in f) for f in seed.get("facts", []))


def clamp_ratio(requested: float, n_domains: int) -> float:
    r = max(MIN_WEB, min(MAX_WEB, requested))
    if n_domains < MIN_DOMAINS:      # thin sourcing -> shrink web share
        r *= n_domains / MIN_DOMAINS
    return r


def as_records(topics: list, key: str) -> list[dict]:
    return [t if isinstance(t, dict) else {key: t, "origin": "pool"}
            for t in topics]


def load_ledger(spec: dict) -> tuple[dict, dict]:
    """(whole ledger, this test's history row) from logs/ledger.json — REQUIRED.

    Every exit from this function that is not the row itself is fatal, on
    purpose. The ledger is the only place the sampler's pool draw survives (so
    unblend() can restore it) and the only place `make check` can read a
    harvest_sha back from. The stamp used to be written under
    `if ledger_path.is_file()` against `spec_path.parent / "ledger.json"` —
    i.e. tests/<id>/ledger.json, which never exists — so the guard was always
    false, nothing was ever stamped, and nothing said so. That is precisely the
    unrecorded-`harvest_sha` hole AGENTS.md §4 describes: `None` is not evidence
    of a different harvest, and tests 2 and 3 passed the rotation check for as
    long as they did because of it.

    A blend whose stamp cannot land must not happen at all, so this is checked
    in pre-flight, before a single record is replaced.
    """
    test_id = spec.get("test_id")
    if test_id is None:
        raise SystemExit(
            "test_spec.json has no test_id, so the harvest_sha stamp has no "
            "logs/ledger.json row to land in. Re-run sample_items.py "
            "--test-id <id> to produce a spec that can be blended.")
    if not LEDGER.exists():
        raise SystemExit(
            f"{LEDGER} does not exist. merge_seeds.py must record which "
            f"harvest this blend came from; without the ledger the rotation "
            f"check in `make check` cannot tell a new harvest from a skipped "
            f"step 3.5. Run sample_items.py first.")
    try:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"{LEDGER} could not be read ({exc}); repair it "
                         f"before blending.")
    rows = [h for h in ledger.get("history", [])
            if isinstance(h, dict) and str(h.get("test_id")) == str(test_id)]
    if not rows:
        known = [str(h.get("test_id")) for h in ledger.get("history", [])
                 if isinstance(h, dict)]
        raise SystemExit(
            f"{LEDGER} has no history entry for test {test_id} "
            f"(it records {known or 'nothing'}). The spec was not produced by "
            f"this repo's sampler, or the ledger was rolled back. Re-run "
            f"sample_items.py --test-id {test_id}, then merge_seeds.py once.")
    return ledger, rows[-1]


def unblend(spec: dict, entry: dict) -> None:
    """Restore the sampler's pool draw so a re-run blends from scratch.

    blend() replaces a budgeted share of the records it is HANDED. Run a second
    time against an already-blended spec it blends on top of its own output:
    the MAX_WEB ceiling applies per run, so the web share compounds, and a seed
    can be written into a second slot while its first copy still sits in the
    spec. Test 4 shipped that way — 規格外野菜 and スマート農業 each in two
    reading slots, 昇降式デスク in two listening slots, 9 of 11 reading topics
    web against a cap of 6 — which left two reading surfaces with no distinct
    topic to author from, so they were written off-contract. Nothing caught it:
    every downstream gate reads the spec, and the spec looked full.

    The sampler's draw is recorded in logs/ledger.json, so it can be put back.
    `entry` is that test's history row, already located (and required to exist)
    by load_ledger() during pre-flight. Without a draw in it there is nothing to
    restore from and re-running would silently keep compounding, so refuse.
    """
    fields = (("reading_topics", "topic"), ("listening_scenarios", "scenario"))
    already = [f for f, k in fields
               if any(isinstance(e, dict) and e.get("origin") == "web"
                      for e in spec.get("items", {}).get(f, []))]
    if not already:
        return
    restored = []
    for field, key in fields:
        pooled = (entry.get("items") or {}).get(field)
        if pooled:
            spec["items"][field] = list(pooled)
            restored.append(field)
    if not restored:
        raise SystemExit(
            f"test_spec.json is already blended ({', '.join(already)}) and "
            f"{LEDGER}'s entry for test {spec.get('test_id')} records no draw "
            f"to restore from. Re-run sample_items.py for a clean spec, then "
            f"merge_seeds.py once.")
    print(f"  note: spec was already blended ({', '.join(already)}) — restored "
          f"the pool draw from the ledger before re-blending")


def take(rng: random.Random, pool: list[dict], n: int, pref) -> list[dict]:
    """Take up to n seeds from pool (mutates pool), preferring pref(seed)."""
    ordered = sorted(pool, key=lambda s: (not pref(s), rng.random()))
    chosen = ordered[:n]
    for s in chosen:
        pool.remove(s)
    return chosen


def blend(rng: random.Random, records: list[dict], pool: list[dict],
          key: str, budget: int, surface: str,
          domain_used: Counter) -> list[dict]:
    """Replace up to `budget` records with web seeds taken from pool
    (mutates pool), honoring the per-domain cap and the MAX_WEB ceiling."""
    budget = min(budget, int(len(records) * MAX_WEB))
    cands = [s for s in pool if fits(s, surface)]
    rng.shuffle(cands)
    chosen = []
    for s in cands:                       # cap re-checked per pick, so one
        if len(chosen) >= budget:         # call can't overdraw a domain
            break
        if domain_used[domain_of(s)] < MAX_PER_DOMAIN:
            chosen.append(s)
            domain_used[domain_of(s)] += 1
    if not chosen:
        return records
    idx = rng.sample(range(len(records)), len(chosen))
    for i, s in zip(idx, chosen):
        records[i] = {key: s["seed"], "origin": "web",
                      "facts": s.get("facts", []),
                      "source": s.get("source", "")}
        pool.remove(s)
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds")
    ap.add_argument("spec")
    ap.add_argument("--reading-ratio", type=float, default=0.5,
                    help="target web fraction of reading topics (clamped 0.30-0.60)")
    ap.add_argument("--listening-ratio", type=float, default=0.4,
                    help="target web fraction of listening scenarios (clamped 0.30-0.60)")
    args = ap.parse_args()

    seeds_path = Path(args.seeds)
    seeds = json.loads(seeds_path.read_text(encoding="utf-8"))
    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    # Pre-flight, before anything is blended: none of these can be repaired
    # downstream (see the function docstrings). The two repo-level history
    # files are resolved from ROOT, never from spec_path.parent — the spec
    # moved to tests/<id>/ and the sibling lookups did not.
    validate_harvest(seeds)
    check_topic_reuse(seeds, TOPICS, spec.get("test_id"))
    ledger, entry = load_ledger(spec)   # fatal if the stamp has nowhere to land

    unblend(spec, entry)                # make re-runs idempotent

    rng = random.Random(f"{spec.get('seed', 0)}-webmerge")
    rng.shuffle(seeds)
    supply = len(seeds)

    domains = {domain_of(s) for s in seeds}
    n_dom = max(1, len(domains - {"unknown"}))
    r_read = clamp_ratio(args.reading_ratio, n_dom)
    r_listen = clamp_ratio(args.listening_ratio, n_dom)

    domain_used: Counter = Counter()
    pool = list(seeds)

    # ---- reserve the one unique texture seed: 問題14 numeric facts ------
    info_res = take(rng, pool, 1 if any(has_number(s) and fits(s, "info")
                                        for s in pool) else 0,
                    lambda s: has_number(s) and fits(s, "info"))
    for s in info_res:                    # counts toward the domain cap NOW,
        domain_used[domain_of(s)] += 1    # so blends can't overdraw later

    # ---- size the big-surface budgets, keep a leftover margin for -------
    # qr/carrier texture (those take whatever the big surfaces don't use)
    reading = as_records(spec["items"]["reading_topics"], "topic")
    listening = as_records(spec["items"]["listening_scenarios"], "scenario")
    want_r = max(1, round(len(reading) * r_read))
    want_l = max(1, round(len(listening) * r_listen))
    want_c = 1                                   # cloze candidate
    margin = min(5, max(2, supply // 4))         # texture margin
    big_supply = max(0, len(pool) - margin)
    if want_r + want_l + want_c > big_supply:
        scale = big_supply / (want_r + want_l + want_c)
        want_r = max(1, int(want_r * scale))
        want_l = max(1, int(want_l * scale))
        spare = big_supply - want_r - want_l - want_c
        if spare > 0:                    # truncation remainder -> largest surface
            want_l += spare

    # ---- 問題10-13 reading topics ---------------------------------------
    reading = blend(rng, reading, pool, "topic", want_r, "reading", domain_used)
    spec["items"]["reading_topics"] = reading

    # ---- 聴解 problem scenarios -----------------------------------------
    listening = blend(rng, listening, pool, "scenario", want_l, "listening",
                      domain_used)
    spec["items"]["listening_scenarios"] = listening

    # ---- 問題9 cloze passage topic (50/50 web vs pool) ------------------
    cloze_cand = [s for s in pool if fits(s, "reading")
                  and domain_used[domain_of(s)] < MAX_PER_DOMAIN]
    if cloze_cand and rng.random() < 0.5:
        s = rng.choice(cloze_cand)
        spec["cloze_topic"] = {"topic": s["seed"], "origin": "web",
                               "facts": s.get("facts", []),
                               "source": s.get("source", "")}
        domain_used[domain_of(s)] += 1
        pool.remove(s)
    else:
        spec["cloze_topic"] = {"origin": "pool",
                               "note": "author picks any pool reading topic register"}

    # ---- 問題14 info-retrieval flyer texture ----------------------------
    if info_res:
        s = info_res[0]
        spec["info_retrieval_texture"] = {
            "detail": s["seed"], "origin": "web",
            "facts": s.get("facts", []), "source": s.get("source", "")}
        # (its domain was already counted at reservation time)

    # ---- 問題4 即時応答 situational settings (from leftovers) ------------
    qr_n = min(QR_SEEDS, 2 if supply < 18 else 3, len(pool))
    qr_res = take(rng, pool, qr_n,
                  lambda s: fits(s, "listening") or fits(s, "carrier"))
    spec["qr_situation_seeds"] = [
        {"detail": s["seed"], "origin": "web", "source": s.get("source", "")}
        for s in qr_res]

    # ---- 問題1-8 carrier-sentence texture (remaining leftovers) ----------
    carr_all = ([s for s in pool if fits(s, "carrier")]
                + [s for s in pool if not fits(s, "carrier")])  # fallback: any
    spec["carrier_seeds"] = [
        {"detail": s["seed"], "origin": "web",
         "facts": s.get("facts", []), "source": s.get("source", "")}
        for s in carr_all[:CARRIER_SEEDS]]

    # ---- stamp WHICH harvest this blend came from -----------------------
    # The RNG is seeded from the spec's own seed, so the same --seed against an
    # unchanged seeds.json reproduces the previous test's blend slot for slot.
    # Recording the harvest identity in both the spec and the ledger lets
    # `make check` tell "a genuinely new harvest" from "step 3.5 was skipped".
    # Every surface must end up with DISTINCT topics: the author needs one
    # subject per 問題, and a spec that repeats itself silently starves a
    # surface (see unblend()). Cheap to assert, impossible to spot by eye.
    for field, key in (("reading_topics", "topic"),
                       ("listening_scenarios", "scenario")):
        names = [r.get(key) for r in spec["items"][field]]
        dups = sorted({n for n in names if names.count(n) > 1})
        if dups:
            raise SystemExit(f"{field} would carry duplicate entries {dups} — "
                             f"blend is broken; do not author from this spec")

    harvest_sha = hashlib.sha1(seeds_path.read_bytes()).hexdigest()[:12]
    spec["harvest_sha"] = harvest_sha
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=1),
                         encoding="utf-8")

    # The stamp lands in BOTH places or the run fails. load_ledger() already
    # proved the row exists, so a zero here means the ledger changed under us —
    # which must not pass silently, because an unrecorded harvest_sha is
    # indistinguishable from a skipped step 3.5 (AGENTS.md §4).
    stamped = 0
    for row in ledger.get("history", []):
        if isinstance(row, dict) and str(row.get("test_id")) == str(spec["test_id"]):
            row["harvest_sha"] = harvest_sha
            stamped += 1
    if not stamped:
        raise SystemExit(f"{LEDGER} lost its entry for test {spec['test_id']} "
                         f"mid-run; harvest_sha {harvest_sha} was not recorded")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"  harvest_sha {harvest_sha} stamped into {spec_path} and "
          f"{LEDGER} ({stamped} entry)")

    # ---- balance report --------------------------------------------------
    def share(recs):
        w = sum(1 for r in recs if r.get("origin") == "web")
        return f"{w} web / {len(recs) - w} pool ({w / len(recs):.0%} web)"

    print("blend report (pool = Shin-Kanzen-calibrated inventory):")
    print(f"  reading_topics      : {share(reading)}")
    print(f"  listening_scenarios : {share(listening)}")
    print(f"  cloze_topic (問9)   : {spec['cloze_topic']['origin']}")
    print(f"  info texture (問14) : "
          f"{'web' if 'info_retrieval_texture' in spec else 'pool'}")
    print(f"  qr seeds (問4)      : {len(spec['qr_situation_seeds'])} attached")
    print(f"  carrier seeds (問1-8): {len(spec['carrier_seeds'])} attached "
          f"(binding cap: <=1/3 of carrier sentences per 問題)")
    dom_report = ", ".join(f"{d}:{c}" for d, c in domain_used.most_common())
    print(f"  domains used        : {dom_report or 'none'}")
    for name, recs, floor in ((u"reading_topics", reading, MIN_WEB),
                              (u"listening_scenarios", listening, MIN_WEB)):
        w = sum(1 for r in recs if r.get("origin") == "web")
        if w / len(recs) < floor * (n_dom / MIN_DOMAINS if n_dom < MIN_DOMAINS else 1):
            print(f"  warning: {name} web share below target — harvest more "
                  f"seeds fitting this surface and re-run")
    if n_dom < MIN_DOMAINS:
        print(f"  warning: only {n_dom} distinct source domain(s) — web ratios "
              f"were scaled down; harvest from more domains for a fuller blend")
    if supply < 18:
        print(f"  note: {supply} seeds supplied; harvest 18-25")
    # Domains, not seed count, cap the blend: MAX_PER_DOMAIN is shared across
    # every topic-level surface, so N domains fund at most 2N picks. 6 domains
    # covers the 30% floor (12 picks) and no more; the default ratios want 16.
    if n_dom < 8:
        print(f"  note: {n_dom} domain(s) => at most {2 * n_dom} topic-level "
              f"web picks. 6 domains funds only the 30% floor (12); the default "
              f"0.5/0.4 ratios need 16 picks (8 domains), full 60% needs 22 "
              f"(11). More seeds from the SAME domains cannot raise the share.")


if __name__ == "__main__":
    main()
