#!/usr/bin/env python3
"""
Blend web-harvested topic seeds into test_spec.json — ACROSS THE WHOLE EXAM,
with balance caps so neither the web nor the pool/Shin-Kanzen side dominates.

Usage:
    python merge_seeds.py logs/seeds.json logs/test_spec.json
    python merge_seeds.py logs/seeds.json logs/test_spec.json --reading-ratio 0.5 --listening-ratio 0.4

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

ALLOCATION: a small texture cut (info/qr/carrier) is reserved FIRST so every
surface receives seeds even with a thin harvest; the remaining seeds fund
reading/listening, scaled down proportionally if supply < demand. The skill's
recommended harvest (18-25 seeds, >=4 domains) funds all surfaces at full
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
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

MIN_WEB = 0.30
MAX_WEB = 0.60
MAX_PER_DOMAIN = 2
MIN_DOMAINS = 3
QR_SEEDS = 3          # max situational seeds attached for 即時応答
CARRIER_SEEDS = 6     # max texture seeds attached for 問題1-8 carrier sentences


def domain_of(seed: dict) -> str:
    try:
        return urlparse(seed.get("source", "")).netloc or "unknown"
    except ValueError:
        return "unknown"


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


def unblend(spec: dict, ledger_path: Path) -> None:
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
    Without it there is nothing to restore from and re-running would silently
    keep compounding, so refuse instead.
    """
    fields = (("reading_topics", "topic"), ("listening_scenarios", "scenario"))
    already = [f for f, k in fields
               if any(isinstance(e, dict) and e.get("origin") == "web"
                      for e in spec.get("items", {}).get(f, []))]
    if not already:
        return
    entry = None
    if ledger_path.is_file():
        for h in json.loads(ledger_path.read_text(encoding="utf-8")).get("history", []):
            if str(h.get("test_id")) == str(spec.get("test_id")):
                entry = h
    if not entry:
        raise SystemExit(
            f"test_spec.json is already blended ({', '.join(already)}) and "
            f"logs/ledger.json has no draw for test {spec.get('test_id')} to "
            f"restore from. Re-run sample_items.py for a clean spec, then "
            f"merge_seeds.py once.")
    for field, key in fields:
        pooled = entry.get("items", {}).get(field)
        if pooled:
            spec["items"][field] = list(pooled)
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

    seeds = json.loads(Path(args.seeds).read_text(encoding="utf-8"))
    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    unblend(spec, spec_path.parent / "ledger.json")   # make re-runs idempotent

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

    harvest_sha = hashlib.sha1(
        Path(args.seeds).read_bytes()).hexdigest()[:12]
    spec["harvest_sha"] = harvest_sha
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=1),
                         encoding="utf-8")

    ledger_path = spec_path.parent / "ledger.json"
    if ledger_path.is_file() and spec.get("test_id") is not None:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        for entry in ledger.get("history", []):
            if str(entry.get("test_id")) == str(spec["test_id"]):
                entry["harvest_sha"] = harvest_sha
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                               encoding="utf-8")

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
        print(f"  note: {supply} seeds supplied; ~22 across >=4 domains funds "
              f"all surfaces at full target ratios")


if __name__ == "__main__":
    main()
