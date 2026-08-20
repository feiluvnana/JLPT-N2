#!/usr/bin/env python3
"""
Topological & Permutation Verifier for JLPT N2 問題8 (文の組み立て).

Extracts 問題8 scramble sentences (43..47) from 言語知識・読解.md, enumerates all
24 orderings, filters them through a SMALL list of impossible junctions, and
checks the keyed ★ against whatever survives.

WHAT THIS TOOL CAN AND CANNOT DECIDE — read before trusting a line of output.

`IMPOSSIBLE_JUNCTIONS` knows four patterns (stacked case particles, a handful of
conjugation clashes, a dangling particle before punctuation). Japanese
word-order uniqueness turns on semantics and on connective subcategorisation,
neither of which is in that list, so a surviving permutation is NOT a
grammatical sentence and 「24 permutations possible」 is NOT a finding. Until
2026-08-19 the tool printed exactly that line for every item of every paper —
`RESULT: WARNING (24 permutations possible)` — and returned success, so it read
the same for a sound item and for a broken one and decided nothing. A genuine
second defensible answer at 20260817_3 問題8-44 went straight through it
(qa-report-20260817_3 F1).

So the tool now decides THREE things, and says which is which:

  1. NEGATIVE evidence it really has: the keyed ★ is not among the surviving
     orderings, or the junction filter killed every ordering. Both are FAIL.
  2. The AUTHOR'S ARTIFACT: the item's 解説 must carry a per-card uniqueness
     proof that includes the LAST SLOT — for each card, why it cannot be the
     final card before the fixed tail. That is what 問題8-44's author never
     wrote and what the reviewer had to reconstruct by hand; it is required
     here, and a missing one is a FAIL.
  3. The CONSTRUCTION rule: how many separately-orderable units sit in front of
     the final predicate (`free_unit_count`). At most one may, and two is an
     ITEM defect no proof can argue away. See that function's own comment.

Uniqueness itself is still the 解説's claim, not this tool's finding. When more
than one ordering survives the filter, the verdict is UNDECIDED, never WARNING.

Usage:
    python3 tools/verify_scramble.py tests/20260813_2
    python3 tools/verify_scramble.py tests/20260813_2 --verbose
"""

import argparse
import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Common impossible junctions in Japanese grammar
IMPOSSIBLE_JUNCTIONS = [
    # Double subject/object particles without coordinate structure
    r"(?:を|が|に|へ|で|と|から|より)[ \t]*(?:を|が|へ|より)",
    # Conjugation clashes
    r"(?:ない|なかった|ている|ていた)[ \t]*(?:ます|ました|ません|でした)",
    r"(?:て|で)[ \t]*(?:です|でした)",
    # Dangling particles before punctuation
    r"[をがにへでと][ \t]*[。！？]",
]
JUNCTION_RE = re.compile("|".join(IMPOSSIBLE_JUNCTIONS))


def parse_mondai8_items(gengo_md: str) -> list:
    """Extract (q_num, lead_in, tail, [opt1..4], key, kaisetsu_order)"""
    m8 = re.search(r"##\s*問題8.*?(?=##\s*問題9|#+\s*解答|#+\s*【?正解|\Z)", gengo_md, re.S)
    if not m8:
        return []

    # Extract key table
    key_map = {}
    key_split = re.split(r"^#+\s*(?:解答|【?正解)", gengo_md, flags=re.M)
    if len(key_split) > 1:
        for line in key_split[1].splitlines():
            line = line.strip()
            if line.startswith("|") and line.endswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 3 and parts[0].isdigit():
                    q = int(parts[0])
                    if 43 <= q <= 47 and parts[1].isdigit():
                        key_map[q] = {
                            "key": int(parts[1]),
                            "kaisetsu": parts[2]
                        }

    items = []
    # Pattern for 問題8 stem: lead-in ___ ___ ★ ___ tail
    q_blocks = list(re.finditer(r"\*\*(\d+)\*\*[ \t]*(.*?)(?=\n\*\*\d+\*\*|\Z)", m8.group(0), re.S))
    for qb in q_blocks:
        qn = int(qb.group(1))
        if not (43 <= qn <= 47):
            continue
        text = qb.group(2).strip()

        # Split stem and options
        m_opts = re.search(r"\n[ \t]*1[.．][ \t]*(.+)", text)
        if not m_opts:
            continue
        stem_raw = text[:m_opts.start()].strip()
        opts_raw = text[m_opts.start():].strip()

        # Extract 4 options
        opts = [o.strip() for o in re.findall(r"[1-4][.．][ \t]*([^\n]+?)(?=[ \t]+[1-4][.．]|\n|\Z)", opts_raw)]
        if len(opts) != 4:
            continue

        # Extract lead-in and tail around the 4 blanks
        blank_pattern = r"(?:[＿_ー―\s]*[（(]?\s*[＿_ー―]+\s*[）)]?[＿_ー―\s]*|[\s　]*_{2,}[\s　]*)"
        m_star = re.search(r"★", stem_raw)
        if not m_star:
            # Try splitting by underscores
            parts = re.split(r"[_＿]{2,}|[―ー]{2,}", stem_raw)
            lead_in = parts[0].strip() if parts else ""
            tail = parts[-1].strip() if len(parts) > 1 else ""
        else:
            # Lead in before first blank sequence, tail after star and trailing blanks
            prefix = stem_raw[:m_star.start()]
            suffix = stem_raw[m_star.end():]
            lead_in = re.sub(r"[_＿―ー\s　]+$", "", prefix).strip()
            tail = re.sub(r"^[_＿―ー\s　]+", "", suffix).strip()

        k_info = key_map.get(qn, {"key": 0, "kaisetsu": ""})
        items.append({
            "num": qn,
            "lead_in": lead_in,
            "tail": tail,
            "options": opts,
            "key": k_info["key"],
            "kaisetsu": k_info["kaisetsu"]
        })

    return items


# The 解説's uniqueness proof has to cover the LAST slot, not just the tested
# connective's own junction. 問題8-44 shipped with a proof that 「テ形『見て』は
# 『うえで』に接続できない」 — true, and it only blocks 見て BEFORE うえで; it
# never rules out 見て as the FINAL card, which is exactly the rival ordering QA
# found. One of these phrases must appear, and every card must be named.
LAST_SLOT_MARKERS = ("最終スロット", "最後のスロット", "末尾スロット", "最終位置",
                     "最後には立て", "最後に立て", "末尾に立て", "文末に置け",
                     "最終スロットの証明", "最後のカード")
PROOF_PREFIX = 4        # chars of a card that count as "the 解説 names it"


# --- The invalid-leg class (R2-F1, qa-report-20260818_1-round2) -------------
# The last-slot proof above can be PRESENT and still prove nothing, because two
# structural legs keep getting written that are false by construction. Both are
# string-decidable, so they are checked here rather than left to a reader:
#
#   (a) "placing X last leaves Y in the middle, where it loses its receiver /
#       connects to nothing" — applied to a card that CAN sit mid-sentence. Two
#       card shapes always can: a card ending in a PLAIN-FORM PREDICATE (a
#       連体修飾句 of whatever noun follows) and a card that is a bare ADVERBIAL
#       PHRASE whose receiving predicate is printed AFTER the blanks (an
#       adverbial can be fronted over any number of clauses, so it never needs an
#       adjacent receiver).
#   (b) "the ordering A→B is impossible because two particles run together" —
#       true only for STACKED CASE particles (を+が …), which is
#       IMPOSSIBLE_JUNCTIONS[0]. Two ordinary particle phrases in a row
#       (「観光客にも地元の人に…」) are everyday Japanese.
#
# Founding cases, both from `20260818_1`, both of which this predicate fires on:
#   45 (round 2): 「『おかげで』を最後に置くと『子どもの急な熱にも』が受け手を失う」 —
#      にも-adverbial, receiver 「慌てずに済んでいる」 printed after the blanks. The
#      item really had two grammatical orderings (★=1 and ★=3).
#   47 (round 1, F9): 「…『高齢の利用者が今も多い』が…どのカードとも結べない」 —
#      plain-predicate card; the rival 4→3→1→2 reads fine and had to be excluded
#      SEMANTICALLY instead.
#   44 (found by the same re-read): 「『タイ料理やインド料理まで』を最後に置くと
#      『作れるように』が受け手を失って」 — false in the ordering it excludes, where
#      『なったと』 still sits right after it.
#   43 (same re-read): 「『観光客にも→地元の人に』は助詞が連続して不可」 — arm (b).
#
# What this CANNOT decide, and it is the whole remaining question: whether a
# rival ordering that IS grammatical is also semantically impossible. Excluding
# it "by the contradiction it creates" is legal and is what 45/47 now do; whether
# the named contradiction is real is a reader's judgment. This predicate only
# stops the two legs that are false before anyone reads them.
#   (c) "「Xを」は他動詞を要求するので［Xを→その動詞］は連続した塊になる" — false.
#       A case particle licenses a predicate SOMEWHERE LATER in the clause, never
#       an adjacent one; Japanese scrambles co-arguments of one verb freely.
#       Legal adjacency comes from a 連体修飾 head, a quotative 「と」, a
#       subcategorised particle (「に→基づいて」) or a fixed 呼応 template — see
#       `bunpou.md` §"At most ONE card may be a free co-argument of the final
#       predicate", which the same round added.
#
# Founding cases for arm (c), all from `qa-report-20260819_1-round2` R2-F3, run
# against the PRE-FIX revision of `tests/20260819_1/言語知識・読解.md` before this
# detector was accepted — it fires on all four items that print the leg:
#   43 「『畑に出る日を』の『を』は他動詞を要求し…［畑に出る日を→決めているそうだ］も
#      連続した塊になる」 — load-bearing: the item really had two ★ answers
#      (rival 2→4→1→3), and was re-cut.
#   47 「『客の感じ方を』の『を』は他動詞を要求し…」 — same, rival 2→4→1→3, re-cut.
#   45 「『受け付けを』の『を』は他動詞を要求し…」 — the item stands, but on the
#      topic/は-stacking argument the 解説 never made.
#   44 「『あの技術を』の『を』は他動詞を要求し…『受け継ぐ人が』…」 — the conclusion
#      is right and the reason is not: adjacency comes from the 連体修飾 head
#      「受け継ぐ人」. This case still FIRES, with a different message. The report
#      proposed exempting a 連体修飾/引用 partner, and the same report requires the
#      run to fire on 44 — the leg is false whether or not its conclusion holds,
#      and a proof rewritten onto the real source no longer matches the regex, so
#      the exemption is expressed as the MESSAGE, never as suppression.
#
# ARM (c) IS PARTICLE-GENERAL — widened 2026-08-20, and here is the case that
# forced it. `20260819_1` 問題8-46 shipped 「『心細いものは』の『は』は述語を要求し、
# 四枚のうち述語は『ない』だけなので、［心細いものは→ない］も塊になる」: the identical
# false inference with は in place of を. The rival 1→2→3→4 puts 「ない」 later but
# not adjacent, so the leg excludes nothing (the real exclusion is the 呼応
# template 「AほどBはない」, source 4). `TRANSITIVITY_LEG`'s 他動詞 anchor is blind
# to it BY CONSTRUCTION, and the anchor's stated justification above — that a
# proof arguing 「『が』は存在を表す述語を要求し…」 is legal — was itself an instance
# of the class, not an exception to it. A case or topic particle constrains
# ORDER, never ADJACENCY, whatever the particle. `PREDICATE_DEMAND_LEG` below is
# the general form; the 他動詞 arm is kept as-is so its four founding cases stay
# covered verbatim, and overlapping matches are reported once.
# `20260810_2` 問題8-45 is the second paper carrying the ITEM class (two free
# co-arguments of one verb: 「契約書の細部にも」 vs 「説明を…理解したうえで」). Its 解説
# is a bare word-order line with no uniqueness proof at all, so no text detector
# can fire on it — `missing_proof()` already FAILs it ("no last-slot proof; cards
# never named"), verified when this arm landed. The construction half of that
# class is a human rule in `bunpou.md`; it is not string-decidable.
RECEIVER_LEG = re.compile(r"受け手を失|受け手がな|受け手をなく|受けるものがな"
                          r"|結べな|むすべな|掛からな|かからな|つながらな|宙に浮")
PARTICLE_RUN_LEG = re.compile(r"助詞が連続|助詞が二つ続|助詞の連続")
# Anchored on 他動詞 on purpose: a proof arguing from a が-existence predicate
# (「『が』は存在を表す述語を要求し…」, 20260819_1 問題8-45) or from a 形式名詞's
# 連体修飾 slot is LEGAL and uses the same 「〜を要求し…塊になる」 wording, so a
# window-based 「を…要求し…連続した塊」 pattern would false-fire on both.
TRANSITIVITY_LEG = re.compile(r"他動詞を要求|他動詞を必要と|他動詞が必要"
                              r"|他動詞を取るので|自動詞では受けられ")
# The particle-GENERAL form of the same leg: any claim that a card demands a
# PREDICATE and is therefore glued to it. 「他動詞を要求」 is a substring of
# 「動詞を要求」, so this subsumes the arm above; the two are de-duplicated by
# offset in `illegal_legs()`.
PREDICATE_DEMAND_LEG = re.compile(
    r"(?:述語|動詞|用言|述部)を(?:要求|必要と|求め|取る)")
# ...but only when the card making the demand ENDS in a case or topic particle,
# which is what makes the demand FORWARD-looking and therefore false. The same
# 「〜を要求し…塊になる」 wording is LEGAL when a BOUND element points BACKWARD at
# its own host — 「そうだ」/「からだ」/「ときほど」 demanding a 普通形 or a 連体修飾
# 述語 **直前** (sources 1 and 3). Those cards end in だ/ほど, not in a case
# particle, and the 直前 guard below covers the ones that do (a clause closer
# like 「見つかった場合は」 would otherwise qualify on its own 「は」).
# 「の」 is deliberately absent: it is the one particle that really does demand an
# immediately following noun, and `_fixed_to_left()` merges on it for that reason.
CASE_TOPIC_END = re.compile(
    r"(?:には|とは|では|へは|からは|までは|にも|でも|とも|へも|までも|をも"
    r"|から|まで|より|[はがをにへとも])$")
# The conclusion half — without it the sentence is an ordinary junction remark,
# not a gluing argument.
ADJACENCY_CLAIM = re.compile(r"塊|連続|隣接|直後に置|すぐ後ろ|直結")
CLAIM_WINDOW = 80    # chars after the demand in which the 塊 conclusion may sit
# A card that is a 連体修飾 head: a plain-form predicate inside the card, followed
# by a short head noun + particle at the card's end (「受け継ぐ人が」, 「借りた本を」).
RENTAI_HEAD_CARD = re.compile(
    r"(?:[うくぐすずつづぬふぶぷむゆる]|た|ない|い)[ぁ-んァ-ヶ一-龯々]{1,6}[がをはにもとで]$")
# A card carrying a quotative 「と」 (the other lexical source of adjacency).
QUOTATIVE_CARD = re.compile(r"と$|と(?:いう|言う|思|考|聞|述)")
# A plain-form predicate tail: the う-column (dictionary form), い-adjective,
# 〜た, 〜だ, 〜ない. Deliberately NOT て形 or ます形 — those genuinely cannot host
# a following noun, so a structural leg about them is legal.
PLAIN_PREDICATE_END = re.compile(r"(?:[うくぐすずつづぬふぶぷむゆる]|い|た|だ|ない)$")
# A bare adverbial phrase: case/topic particle tail with no predicate of its own.
ADVERBIAL_PARTICLE_END = re.compile(
    r"(?:にも|でも|へも|とも|までも|には|とは|では|から|まで|に|は|も|へ|と|で)$")
LEG_WINDOW = 30      # chars between a card's name and the leg that excludes it
FREE_UNIT_MAX = 1    # bunpou.md: at most ONE freely-orderable pre-predicate unit
# The construction rule was written on 2026-08-19 (as the co-argument count) and
# re-scoped to UNITS on 2026-08-20. Every paper below was authored before it
# existed; each prints its measurement and does NOT fail, exactly as
# `SETTING_ADJACENCY_GRANDFATHERED` and `MOJI_GLYPH_GRANDFATHERED` do in
# `tools/check_consistency.py`. An id leaves this set the moment its 問題8 is
# re-cut. Measured 2026-08-20 — items reading n >= 2:
#   20260807_1 none      20260810_1 44,46,47   20260810_2 43,45,46,47
#   20260811_1 43,44,45,47                     20260812_1 47
#   20260812_2 44,46,47  20260813_1 43,44,45,46,47                20260813_2 43,47
#   20260814_1 43,45,46  20260817_1 43,46,47   20260817_2 43,44,45
#   20260817_3 none      20260818_1 43,47
# 33 of the 65 items on those 13 papers, against round 3's estimate of one
# (`20260810_2` 問題8-45). The gap is REAL and is stated rather than tuned away:
# round 3 scanned only for *[adjunct clause] + [free を-object]*, and the rule it
# proposed covers every pair of free units — two bare co-argument NPs
# (`20260813_1` 問題8-44: 「自分の言動には」/「常に責任を」) are the same defect and
# were never counted. 20260807_1 and 20260817_3 are in the set for symmetry only;
# every item of theirs reads <= 1 today, so removing them changes nothing.
FREE_UNIT_GRANDFATHERED = {
    "20260807_1", "20260810_1", "20260810_2", "20260811_1", "20260812_1",
    "20260812_2", "20260813_1", "20260813_2", "20260814_1", "20260817_1",
    "20260817_2", "20260817_3", "20260818_1",
}


def frontable_class(card: str, tail: str) -> str:
    """Why a 'connects to nothing' leg is false for this card, or ''."""
    c = re.sub(r"[\s。、]+$", "", re.sub(r"\s", "", card))
    if PLAIN_PREDICATE_END.search(c):
        return ("ends in a plain-form predicate, so it can always sit "
                "mid-sentence as a 連体修飾句 of the following noun")
    if ADVERBIAL_PARTICLE_END.search(c) and re.search(r"[^\s。、]", tail or ""):
        return (f"is a bare adverbial phrase whose receiving predicate is "
                f"printed AFTER the blanks (「{tail}」), so it can be fronted "
                f"and never needs an adjacent receiver")
    return ""


def _first_named_card(item: dict, after: str) -> str:
    """The card named earliest in `after` — '' if none is."""
    best, pos = "", len(after) + 1
    for o in item["options"]:
        key = re.sub(r"\s", "", o)[:PROOF_PREFIX]
        i = after.find(key)
        if 0 <= i < pos:
            best, pos = o, i
    return best


def _last_named_card(item: dict, before: str) -> tuple[str, int]:
    """The card named latest in `before`, and where — ('', -1) if none is."""
    best, pos = "", -1
    for o in item["options"]:
        key = re.sub(r"\s", "", o)[:PROOF_PREFIX]
        i = before.rfind(key)
        if i > pos:
            best, pos = o, i
    return best, pos


def illegal_legs(item: dict) -> list[str]:
    """Every invalid structural leg the 解説's uniqueness proof leans on."""
    text = re.sub(r"\s", "", item.get("kaisetsu", ""))
    if not text:
        return []
    out = []
    for mo in RECEIVER_LEG.finditer(text):
        card, pos = _last_named_card(item, text[:mo.start()])
        if pos < 0 or mo.start() - pos > LEG_WINDOW:
            continue
        why = frontable_class(card, item["tail"])
        if why:
            out.append(f"「{card}」 is excluded with a 「{mo.group(0)}…」 leg, but it "
                       f"{why} — exclude it SEMANTICALLY (name the reading its "
                       f"mid-sentence use produces and the contradiction that "
                       f"reading creates), never structurally")
    for mo in PARTICLE_RUN_LEG.finditer(text):
        window = text[max(0, mo.start() - LEG_WINDOW):mo.start()]
        named = [o for o in item["options"]
                 if re.sub(r"\s", "", o)[:PROOF_PREFIX] in window]
        if len(named) < 2:
            continue
        clash = False
        for left, right in itertools.permutations(named, 2):
            lseg = left[-4:]
            pair = lseg + right[:4]
            if any(m.start() < len(lseg) < m.end()
                   for m in JUNCTION_RE.finditer(pair)):
                clash = True
        if not clash:
            out.append(f"「{mo.group(0)}」 is claimed for "
                       + " / ".join(f"「{o}」" for o in named)
                       + " but no seam among them stacks CASE particles — two "
                         "ordinary particle phrases in a row are everyday "
                         "Japanese (「私にも彼に似たところがある」). Exclude that "
                         "ordering by what it MEANS")
    spans = []
    for mo in TRANSITIVITY_LEG.finditer(text):
        card, pos = _last_named_card(item, text[:mo.start()])
        if pos < 0 or mo.start() - pos > LEG_WINDOW:
            continue
        spans.append((mo.start(), mo.end()))
        out.append(_predicate_demand_message(item, card, mo.group(0), text, mo))
    # Arm (c), particle-general (20260819_1 問題8-46: the same leg stated on 「は」).
    for mo in PREDICATE_DEMAND_LEG.finditer(text):
        if any(s <= mo.end() and mo.start() <= e for s, e in spans):
            continue                      # already reported by the 他動詞 arm
        card, pos = _last_named_card(item, text[:mo.start()])
        if pos < 0 or mo.start() - pos > LEG_WINDOW:
            continue
        if not CASE_TOPIC_END.search(_clean(card)):
            continue                      # bound element pointing at its host
        if "直前" in text[pos:mo.start()]:
            continue                      # backward-looking: sources 1/3, legal
        if not ADJACENCY_CLAIM.search(text[mo.end():mo.end() + CLAIM_WINDOW]):
            continue                      # no gluing conclusion drawn
        out.append(_predicate_demand_message(item, card, mo.group(0), text, mo))
    return out


def _predicate_demand_message(item: dict, card: str, leg: str,
                              text: str, mo) -> str:
    """The 'a particle constrains ORDER, never ADJACENCY' finding."""
    partner = _first_named_card(item, text[mo.end():mo.end() + LEG_WINDOW * 3])
    p = re.sub(r"[\s。、]+$", "", re.sub(r"\s", "", partner or ""))
    if p and (RENTAI_HEAD_CARD.search(p) or QUOTATIVE_CARD.search(p)):
        return (f"「{card}」 is tied to 「{partner}」 with a 「{leg}…」 leg. "
                f"The CONCLUSION holds — 「{partner}」 is a 連体修飾/引用 host, so its "
                f"own argument cannot leave it — but the REASON does not: a case "
                f"or topic particle licenses a predicate somewhere later in the "
                f"clause, never an adjacent one. Restate the adjacency from the "
                f"連体修飾 head (or the quotative), not from the particle")
    return (f"「{card}」 is tied to 「{partner or '(unnamed card)'}」 with a "
            f"「{leg}…」 leg, which is false by construction: a case or topic "
            f"particle constrains ORDER — its predicate sits SOMEWHERE LATER in "
            f"the clause — never ADJACENCY, and Japanese scrambles pre-predicate "
            f"material freely. If nothing else fixes 「{card}」's position, the "
            f"item has TWO ★ answers and must be RE-CUT — move that unit into "
            f"the stem, or replace the card with one whose host forces adjacency "
            f"(連体修飾 head / quotative 「と」 / subcategorised particle / fixed "
            f"呼応 template). If the conclusion is right on one of those four "
            f"sources, keep the order and restate the proof from it (that is the "
            f"20260819_1 問題8-46 repair: the 呼応 template 「AほどBはない」). See "
            f"bunpou.md §'At most ONE card may be a FREELY-ORDERABLE "
            f"PRE-PREDICATE UNIT'")


# --- The free-unit count (R3-S2, qa-report-20260819_1-round3) ---------------
# `bunpou.md` §"At most ONE card may be a FREELY-ORDERABLE PRE-PREDICATE UNIT"
# is the only thing standing between a 問題8 item and two ★ answers, and until
# 2026-08-20 NOTHING recorded that anyone had counted: this module returns
# `RESULT: UNDECIDED` on every item by design, `make check` reads none of it,
# and the 24-permutation walk lived entirely in whichever reviewer chose to do
# it. Round 1 of `20260819_1` did not, and passed 問題8-43 and -47, both of
# which had a second grammatical ★.
#
# The one property that HAS caused every non-unique 問題8 item on disk is
# string-decidable off the 解説's own word-order line, so it is counted here:
# how many separately-orderable units sit in front of the final predicate.
#
# METHOD. Read the word order out of the 解説 (`カード(3)→カード(4)→…`), then
# merge each adjacent pair whose adjacency is forced by one of the four sources
# `bunpou.md` licenses — 連体修飾 head, quotative 「と」, a subcategorising
# particle or 形式名詞 slot, a 呼応 template — plus the bound predicate tails
# (「そうだ」「からだ」「ない」…) that cannot stand anywhere but after their host.
# What survives is a list of blocks; the last one carries the final predicate,
# a leading discourse connective (「つまり」) is fixed to clause-initial position
# and does not count, and everything else is a free unit.
#
# DIRECTION OF ERROR — read this before trusting a green line. The merger is
# deliberately GENEROUS: every rule above merges on a string test, so an
# adjacency it cannot recognise is the only way to over-count, and a glue that
# is not really lexical is the way to under-count. `FREE UNITS: n` is therefore
# a LOWER bound on the real count, and a FAIL means "even a generous merger
# cannot pin two of these units". n ≤ 1 is NOT proof of uniqueness — the 24
# orderings still have to be walked, and this tool still says UNDECIDED.
#
# FOUNDING CASES, all run before this landed (2026-08-20):
#   `20260819_1` 問題8-45 as shipped through round 3 —
#      申請書に不備が / あった場合は / 受け付けを / 断らねばならない → FREE UNITS: 2.
#      [申請書に不備があった場合は] merges (連体修飾 head 「あった場合は」), and
#      「受け付けを」 does NOT merge with 「断らねばならない」, because transitivity
#      is not a source of adjacency. That is exactly the item the re-scoped rule
#      was written for: the old wording counted ONE free co-argument and passed
#      it. Re-cut the same day to 申請書の / 不備が / 見つかった場合は /
#      課長に報告せねばならない → FREE UNITS: 1.
#   `20260810_2` 問題8-45 — 説明を / しっかりと理解したうえで / 契約書の細部にも /
#      目を通しておくべきだ → FREE UNITS: 2 (the うえで clause merges its own
#      object; 「契約書の細部にも」 is a second free adjunct). This paper is the
#      second carrying the ITEM class and its 解説 prints no proof at all, so
#      `missing_proof()` already FAILs it — this check names WHY.
#   `20260819_1` 問題8-43 and -47 in their PRE-round-2 revision — reconstructed
#      from `qa-report-20260819_1-round2` R2-F1/R2-F2 (畑に出る日を / 客の感じ方を
#      still on cards) → FREE UNITS: 2 each. Both were re-cut; both now read 1.
#   Every other 問題8 item on all 14 papers reads ≤ 1 (measured 2026-08-20).
# A card that cannot START a clause: it opens with a particle, a bound
# connective, a 形式名詞, or an auxiliary that needs a host. Such a card attaches
# to whatever precedes it (or, in slot 1, to the printed lead-in) — its position
# is not its own.
BOUND_OPENING = re.compile(
    r"^(?:[はもがをにでへとやか]|から|まで|より|ば|ばかり|だけ|しか|こそ|さえ"
    r"|場合|とき|時|こと|もの|ため|ところ|うえ|上|はず|わけ|ほう|方|まま|うち"
    r"|かぎり|限り|以上|かわり|代わり|たび|度|あげく|末|際|おり|折|おかげ|せい"
    r"|くらい|ぐらい|ほど|次第|しだい|一方|あまり|ゆえ|とおり|通り|どころ|くせ"
    r"|そうだ|ようだ|よう|らしい|ということ|ものだ|はずだ|わけだ|のだ|んだ"
    r"|ちがい|違い|かもしれ|べき|つもり|つつ|ながら|しか|ない|なかった|だろう"
    r"|でしょう|いく|くる|おく|みる|ある|いる|しまう|しまった|きった|くれ|もらう"
    r"|やる|ねば|なければ|ざる|得ない|えない|とはいえ|といって|といえ|といった"
    r"|ものの|のに|ので|し|つ|た|て|で)")
# A card that CLOSES a subordinate clause. Everything to its left belongs to
# that clause and cannot scramble out of it (bunpou.md source 1, generalised
# from 連体修飾 to every subordinate clause), so a closer absorbs its left.
CLAUSE_CLOSER = re.compile(
    r"(?:場合は?|ときは?|時に?は?|うえで|上で|おかげで|せいで|ために|ため|ので"
    r"|のに|ものの|くせに|ばかりに|とはいえ|といっても|からといって|につれて"
    r"|に伴って|に沿って|に基づいて|に限らず|に応じて|に当たって|にあたって"
    r"|に先立って|をきっかけに|を通じて|をはじめ|ように|ないことには|ない限りは?"
    r"|限りは?|次第|しだい|一方|ながら|つつ|まま|たら|なら|ても|でも|ば|とき"
    r"|ことがない|あげく|末に|以上は?|反面|半面|どころか|かぎり)$")
SUBCAT_GOVERNOR = re.compile(
    r"^(?:基づ|従って|したがって|沿って|際して|先立|当たって|あたって|対して"
    r"|関して|おいて|わたって|渡って|よって|とって|ついて|かけて|限らず"
    r"|かかわらず|応じて|通じて|つれて|伴って|ともなって|加えて|比べて|反して"
    r"|即して|こたえて|向けて|かわって|代わって|ともに|限り)")
QUOTATIVE_VERB = re.compile(r"^(?:言|いう|いっ|思|考|聞|述|自慢|決|定|感じ|話)")
CONNECTIVE_CARD = re.compile(
    r"^(?:つまり|しかし|だが|ところが|そのため|だから|また|なお|むしろ|さらに"
    r"|そして|ただし|要するに|例えば|たとえば|なぜなら|一方|したがって)[、,]?$")
# 呼応 templates that lexically order their two halves (bunpou.md source 4).
KOOU_PAIRS = ((r"(?:だけでなく|のみならず|ばかりでなく|ばかりか)$", r"も[、,]?$"),
              (r"ほど$", r"は$"),
              (r"(?:をはじめ|を始め)$", r"まで$"))


def _clean(card: str) -> str:
    return re.sub(r"[\s。、　]+$", "", re.sub(r"[\s　]", "", card))


def _fixed_to_left(left: str, right: str) -> str:
    """Why `right` cannot leave `left`'s side, or '' — bunpou.md sources 1-4."""
    L, R = _clean(left), _clean(right)
    if BOUND_OPENING.match(R):
        return "opens with a bound element, so it cannot start a clause"
    if RENTAI_HEAD_CARD.search(R) and re.search(r"[をがにへでとの]$", L):
        # Only material that could BE an argument of the modifying clause is
        # inside it. A テ形/連用 adverbial of the MAIN verb sitting in front of a
        # 連体修飾 card is not (`20260819_1` 問題8-43 pre-fix: 「基づいて」 +
        # 「畑に出る日を」 — the を-object was free, and the item had two ★).
        return ("連体修飾 head — the modifying clause's own argument cannot "
                "leave it (source 1)")
    if SUBCAT_GOVERNOR.match(R) and re.search(r"[にをとへからより]$", L):
        return "subcategorised particle (source 3)"
    if L.endswith("と") and QUOTATIVE_VERB.match(R):
        return "quotative 「と」 (source 2)"
    if L.endswith("の"):
        return "「の」 requires an immediately following noun (source 1)"
    for lpat, rpat in KOOU_PAIRS:
        if re.search(lpat, L) and re.search(rpat, R):
            return "fixed 呼応 template ordering its two halves (source 4)"
    return ""


def kaisetsu_order(item: dict) -> list[int]:
    """The 解説's word order as 1-based option numbers, or [] if unparsable."""
    head = re.split(r"｜", item.get("kaisetsu", ""))[0]
    nums = [int(n) for n in re.findall(r"[（(]([1-4])[）)]", head)]
    return nums if sorted(nums) == [1, 2, 3, 4] else []


def free_unit_count(item: dict) -> tuple[int, list[str]]:
    """(free pre-predicate units, one label per block). (-1, []) if unread."""
    order = kaisetsu_order(item)
    if not order:
        return -1, []
    cards = [item["options"][n - 1] for n in order]
    blocks: list[list[str]] = [[cards[0]]]
    for prev, cur in zip(cards, cards[1:]):
        if _fixed_to_left(prev, cur):
            blocks[-1].append(cur)
        else:
            blocks.append([cur])
        # A subordinate clause absorbs everything to its left: its arguments and
        # adjuncts cannot scramble out of it.
        if CLAUSE_CLOSER.search(_clean(cur)) and len(blocks) > 1:
            merged = [c for b in blocks for c in b]
            blocks = [merged]
    free = [b for b in blocks[:-1]
            if not (len(b) == 1 and CONNECTIVE_CARD.match(_clean(b[0])))]
    return len(free), ["＋".join(b) for b in blocks]


def missing_proof(item: dict) -> str:
    """'' when the 解説 carries a last-slot proof naming every card."""
    text = re.sub(r"\s", "", item.get("kaisetsu", ""))
    if not text:
        return "no 解説 cell for this item"
    gaps = []
    if not any(mk in text for mk in LAST_SLOT_MARKERS):
        gaps.append("no last-slot proof (say, per card, why it cannot be the "
                    "FINAL card before the fixed tail — a junction argument "
                    "about the tested connective does not cover slot 4)")
    unnamed = [o for o in item["options"]
               if re.sub(r"\s", "", o)[:PROOF_PREFIX] not in text]
    if unnamed:
        gaps.append("cards never named in the proof: "
                    + " / ".join(f"「{o}」" for o in unnamed))
    return "; ".join(gaps)


def analyze_scramble(item: dict, verbose: bool = False,
                     grandfathered: bool = False):
    qn = item["num"]
    opts = item["options"]
    L = item["lead_in"]
    T = item["tail"]
    key = item["key"]

    print(f"\n-------------------------------------------------------------")
    print(f"問題8 [{qn}番] ★ Key: {key}")
    print(f"  Lead-in : 「{L}」")
    print(f"  Options : 1. {opts[0]} | 2. {opts[1]} | 3. {opts[2]} | 4. {opts[3]}")
    print(f"  Tail    : 「{T}」")
    if item["kaisetsu"]:
        print(f"  解説    : {item['kaisetsu']}")

    valid_perms = []

    for perm in itertools.permutations(range(4)):
        # perm is 0-indexed tuple of length 4, e.g. (1, 3, 0, 2)
        assembled = L + opts[perm[0]] + opts[perm[1]] + opts[perm[2]] + opts[perm[3]] + T
        assembled_clean = re.sub(r"\s+", "", assembled)

        # Check for obvious impossible junctions
        has_clash = False
        junction_pairs = [
            (L, opts[perm[0]]),
            (opts[perm[0]], opts[perm[1]]),
            (opts[perm[1]], opts[perm[2]]),
            (opts[perm[2]], opts[perm[3]]),
            (opts[perm[3]], T)
        ]
        for left, right in junction_pairs:
            lseg = left[-4:]
            pair_str = lseg + right[:4]
            boundary = len(lseg)
            # A junction defect is a clash AT THE SEAM between two adjacent
            # option strings — a match that lands entirely inside one side's
            # own text (e.g. こと's own と + a real trailing object/subject
            # particle: 「会議のことを」, 「両親のことが」) is not a junction at
            # all, and previously self-triggered a FAIL on both option's own
            # tail regardless of what actually sits next to it (20260817_1 QA
            # G-NEW-2: items 46/47, a common, grammatical ことを/ことが
            # construction, both flagged "0 valid permutations").
            if any(mo.start() < boundary < mo.end()
                   for mo in JUNCTION_RE.finditer(pair_str)):
                has_clash = True
                break

        if not has_clash:
            star_opt_num = perm[2] + 1  # 3rd blank (index 2) is ★
            perm_str = f"({perm[0]+1})→({perm[1]+1})→**({perm[2]+1})**→({perm[3]+1})"
            valid_perms.append((perm_str, star_opt_num, assembled_clean))

    print(f"  Candidate Valid Permutations ({len(valid_perms)} / 24):")
    for p_str, star_val, sentence in valid_perms:
        star_match = "✓ (Matches Key)" if star_val == key else f"❌ (Key mismatch: ★ is {star_val} vs key {key})"
        print(f"    - {p_str} => ★={star_val} {star_match}")
        if verbose:
            print(f"      Full: 「{sentence}」")

    # The author's artifact, checked before the permutation verdict because it
    # is the only uniqueness EVIDENCE that exists (see the module docstring).
    missing = missing_proof(item)
    if missing:
        print(f"  => ARTIFACT: MISSING — {missing}")
    else:
        print(f"  => ARTIFACT: ok (解説 carries a last-slot proof naming every card)")

    illegal = illegal_legs(item)
    for leg in illegal:
        print(f"  => PROOF LEG INVALID — {leg}")

    n_free, blocks = free_unit_count(item)
    if n_free < 0:
        print("  => FREE UNITS: unread (the 解説 carries no parsable "
              "`カード(n)→…` word order, so the construction rule cannot be "
              "counted here — count it by hand against bunpou.md)")
    else:
        print(f"  => FREE UNITS: {n_free}  [{' ｜ '.join(blocks)}]")
        if n_free >= FREE_UNIT_MAX + 1 and grandfathered:
            print(f"  => FREE UNITS over the cap ({n_free} > {FREE_UNIT_MAX}) — "
                  f"GRANDFATHERED: this paper was authored before the rule "
                  f"existed (2026-08-19/20). Measurement recorded, exit code "
                  f"unaffected; clearing it means re-cutting this item.")
        elif n_free >= FREE_UNIT_MAX + 1:
            print(f"  => FREE UNITS FAIL — {n_free} separately-orderable units "
                  f"sit in front of the final predicate, and at most "
                  f"{FREE_UNIT_MAX} may. Japanese does not order pre-predicate "
                  f"material, and an adjunct CLAUSE scrambles against an object "
                  f"exactly as freely as a second argument does, so this item "
                  f"has TWO ★ answers whatever the 解説 argues. RE-CUT it: move "
                  f"one unit into the stem before the first blank, fold it into "
                  f"the predicate card, or replace the card with one whose host "
                  f"forces adjacency (連体修飾 head / quotative 「と」 / "
                  f"subcategorised particle / fixed 呼応 template). See "
                  f"bunpou.md §'At most ONE card may be a FREELY-ORDERABLE "
                  f"PRE-PREDICATE UNIT'")

    matching_perms = [p for p in valid_perms if p[1] == key]
    if not valid_perms:
        print(f"  => RESULT: FAIL (0 orderings survive the junction filter — "
              f"the filter is crude, so this usually means a card was "
              f"mis-transcribed, not that the item is unsolvable)")
        return False
    if not matching_perms:
        print(f"  => RESULT: FAIL (the keyed ★={key} is not among the "
              f"{len(valid_perms)} surviving orderings — the key names a card "
              f"the tool cannot place in slot 3)")
        return False
    if len(valid_perms) == 1:
        print(f"  => RESULT: PASS (one ordering survives and its ★={key} "
              f"matches; uniqueness is still the 解説's claim, not this "
              f"tool's finding)")
        return (not missing and not illegal
                and (grandfathered or n_free <= FREE_UNIT_MAX))
    others = sorted({p[1] for p in valid_perms} - {key})
    print(f"  => RESULT: UNDECIDED — {len(valid_perms)} of 24 orderings survive "
          f"a filter that knows {len(IMPOSSIBLE_JUNCTIONS)} junction patterns, "
          f"so this tool has NOT verified uniqueness. Rival ★ values among the "
          f"survivors: {others or 'none'}. The 解説's per-card proof, including "
          f"the LAST slot, is the evidence — read it against these orderings.")
    return not missing and not illegal and (grandfathered or
                                            n_free <= FREE_UNIT_MAX)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("test_dir", help="Path to tests/<test_id>")
    ap.add_argument("--verbose", action="store_true", help="Print full assembled sentences")
    args = ap.parse_args()

    test_dir = Path(args.test_dir)
    gengo_path = test_dir / "言語知識・読解.md"
    if not gengo_path.is_file():
        print(f"Error: Not found: {gengo_path}", file=sys.stderr)
        sys.exit(1)

    items = parse_mondai8_items(gengo_path.read_text(encoding="utf-8"))
    if not items:
        print(f"No 問題8 items found in {gengo_path}")
        sys.exit(0)

    print(f"Loaded {len(items)} 問題8 scramble items from {test_dir.name}")
    all_ok = True
    for it in items:
        ok = analyze_scramble(it, verbose=args.verbose,
                              grandfathered=test_dir.name in FREE_UNIT_GRANDFATHERED)
        if not ok:
            all_ok = False

    print("\n-------------------------------------------------------------")
    print("This tool decides four things: whether the keyed ★ survives its "
          "own junction filter, whether the 解説 carries the per-card last-slot "
          "proof, whether that proof leans on one of the three structural legs "
          "that are false by construction (`illegal_legs`), and how many "
          "freely-orderable units sit in front of the final predicate "
          "(`free_unit_count`, FAIL at 2). It does NOT decide uniqueness, and it "
          "cannot tell whether a SEMANTIC exclusion is sound — read the module "
          "docstring before quoting an UNDECIDED line as a pass.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
