#!/usr/bin/env python3
"""Structural segmentation of an official N2 聴解 recording into its items.

This is the committed implementation of the two-threshold envelope method
`.agents/choukai-audio/references/official_pacing.md` §1 prescribes and §7
describes as "not committed (one-shot analysis)". It is committed now because
`tools/build_choukai_bank.py` cuts real audio at the offsets it returns — an
offset that is one second wrong clips a speaker's first mora, and a method that
lives only in a report cannot be re-run against the file it mis-cut.

Why not `silencedetect=noise=-35dB`
-----------------------------------
The 2023-12 and 2024-12 sittings lay a soft ~-34 dBFS marker tone over the last
~2.5 s of every answer pause. It is not speech and takes no answer time, but it
sits above a -35 dB gate, so a fixed-threshold pass reports their 12 s answer
pause as 9 s and their 8 s pause as 5 s. Measured on this repo's own copies,
naive detection also mis-read one 問題4 answer pause in 2025-07 as 4.4 s.

So a pause is a maximal run below an *extended* threshold, min(-25, LUFS-8)
dBFS, that contains at least `CORE_MIN_S` of *core* silence below -60 dBFS.
The extended threshold swallows the marker tone and very quiet speech tails;
the core requirement stops room tone alone from reading as a pause.

Attribution: structural first, transcript second
------------------------------------------------
問題1 and 問題2 are recovered from pause shape alone, and unambiguously in all
ten sittings on disk: 問題2 is the only section with a long option-reading
pause before every item, so its ~20 s runs bracket it and 問題1 is what
precedes them.

問題3/4/5 need more. `official_pacing.md` §1 says attribution is "structural,
never content-based", and that holds where there is no transcript — but two
purely structural rules were tried here and both are refuted by the archive.
The gap signature (問題3/5 read spoken choices ~3.1 s apart, 問題4 reads three
responses continuously ~2.2 s apart) mis-sorted 9 of 10 sittings; the bands
overlap. Spacing (問題4 is eleven items ~33 s apart against 問題3's ~90 s) is
much better but still leaves 4 of 10 ambiguous, because 問題4's instruction and
例 pauses are the same length and the same distance apart as its item pauses.

So `segment` takes an `item_hint` derived from the sitting's own
`聴解スクリプト.txt`, fits a per-sitting duration model on 問題1/2, and picks
the tail assignment that fits. That is not a weaker method than the structural
one — for these ten papers the transcript is exact and hand-verified, which is
strictly better evidence than a pause histogram. Sittings with no transcript
are simply not bankable, and say so.

A file whose shape is not a sane N2, or whose audio does not match the
transcript it was given, raises `NotSegmented` rather than being folded in with
guessed numbers.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------- constants

SR = 16_000            # decode rate for the envelope (official_pacing §7)
FRAME_MS = 20          # RMS frame for pause detection
CORE_DBFS = -60.0      # literal silence
EXT_CAP_DBFS = -25.0   # extended threshold is min(this, LUFS - 8)
EXT_BELOW_LUFS = 8.0
CORE_MIN_S = 0.30      # a pause must contain this much core silence

# Structural pause signatures, in seconds. Bands are deliberately wide: they
# separate CLASSES of pause from each other, they are not calibration figures.
# The calibrated values live in choukai-audio/SKILL.md's pacing table.
OPTION_READING = (16.0, 26.0)   # 問題2 only: read the printed options (~20.2 s)
ANSWER_12 = (9.5, 16.0)         # 問題1/2 answer time (~12.2 s)
ANSWER_8 = (5.5, 9.5)           # 問題3/4 answer time, 問題5-1番 (~8.3 s)
ANSWER_10 = (9.0, 13.0)         # 問題5 質問1 → 質問2 (~10.0 s)
SPOKEN_CHOICE = (2.6, 4.2)      # 問題3/5 between spoken choices (~3.1 s)
SPOKEN_RESPONSE = (1.9, 2.6)    # 問題4 between the three responses (~2.2 s)

# Floor for a pause that CLOSES an item in the 問題3/4/5 tail. Below ANSWER_8
# on purpose: an answer pause with a stray sound inside it reads short (4.44 s
# in 2025-07 問題4), and only its START is used, so the transcript fit is what
# rejects strays — not the duration.
ANSWER_SPLIT = 4.0

# Pacing constants, mirrored from choukai-audio/SKILL.md's measured table and
# used only to predict how long an item of a given shape should run.
TURN_GAP = 0.9
GAP_AFTER_PRE_QUESTION = 3.0
GAP_BEFORE_REPEATED_QUESTION = 3.0
GAP_BETWEEN_SPOKEN_CHOICES = 3.1
GAP_BETWEEN_SPOKEN_RESPONSES = 2.2
GAP_OPTION_READING = 20.2
GAP_AFTER_SHITSUMON1 = 10.0

# Mean relative error per item above which a tail alignment is rejected rather
# than trusted. A correct fit on the ten sittings runs well under this; the
# ceiling exists so a recording that is NOT the paper its transcript describes
# fails loudly instead of producing plausible-looking offsets.
TAIL_FIT_MAX = 0.30

MIN_REPORTED_PAUSE = 1.5        # shorter runs are turn gaps, not structure

# No official item is shorter than this, so a section's first item may not be
# snapped closer than this to its own answer pause.
MIN_ITEM_SPAN = 12.0

# Item counts per 大問, excluding 例 (which official prints nowhere and which
# this repo's imports therefore do not carry). All 31 sittings run this shape.
EXPECTED_SLOTS = {"問題1": 5, "問題2": 6, "問題3": 5, "問題4": 11, "問題5": 2}


class NotSegmented(Exception):
    """The recording's pause shape is not a recognisable N2 paper."""


def _in(band: tuple[float, float], value: float) -> bool:
    return band[0] <= value < band[1]


def label(path: Path) -> str:
    """A readable id for messages: every sitting's file is named 聴解.mp3."""
    return f"{path.parent.name}/{path.name}"


# ---------------------------------------------------------------- measurement

@dataclass(frozen=True)
class Pause:
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Pause({self.start:.2f}→{self.end:.2f} {self.duration:.2f}s)"


def decode_mono(path: Path) -> np.ndarray:
    """Decode to 16 kHz mono float samples in [-1, 1]. The ONLY MP3 decode.

    Both measurements below run off this one array. Decoding a 42-minute
    sitting twice — once for the envelope, once for `loudnorm` — doubled the
    cost of a bank build for a number that never moves the threshold.
    """
    raw = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
        capture_output=True, check=True,
    ).stdout
    samples = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if samples.size == 0:
        raise NotSegmented(f"{label(path)}: decoded to zero samples")
    return samples


def integrated_lufs(samples: np.ndarray, name: str = "audio") -> float:
    """Integrated loudness via `loudnorm`, fed the already-decoded samples.

    Never `volumedetect`: its `mean_volume` runs ~4 dB below the gated
    K-weighted figure, and reading one as the other is how the pipeline's
    loudness target was wrong by 2 dB for months (official_pacing §"The
    loudness target was a unit error"). Piping raw s16le back into ffmpeg
    keeps the gated K-weighted measurement while skipping a second MP3 decode.
    """
    pcm = (np.clip(samples, -1.0, 1.0) * 32767.0).astype("<i2").tobytes()
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats",
         "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
         "-af", "loudnorm=I=-15:TP=-1.0:LRA=11:print_format=json",
         "-f", "null", "-"],
        input=pcm, capture_output=True, check=True,
    ).stderr.decode("utf-8", "replace")
    blob = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", out, re.S)
    if not blob:
        raise NotSegmented(f"{name}: loudnorm printed no JSON summary")
    value = float(json.loads(blob.group(0))["input_i"])
    if not math.isfinite(value):
        raise NotSegmented(f"{name}: loudnorm reported input_i={value}")
    return value


def rms_envelope(samples: np.ndarray) -> np.ndarray:
    """One dBFS value per 20 ms frame of the decoded signal."""
    step = SR * FRAME_MS // 1000
    usable = (samples.size // step) * step
    frames = samples[:usable].reshape(-1, step)
    rms = np.sqrt(np.mean(np.square(frames), axis=1))
    # -120 dBFS floor keeps digital-zero frames finite for comparison.
    return 20.0 * np.log10(np.maximum(rms, 1e-6))


def find_pauses(envelope: np.ndarray, lufs: float,
                min_duration: float = MIN_REPORTED_PAUSE) -> list[Pause]:
    """Maximal sub-extended runs holding >= CORE_MIN_S of sub-core silence."""
    extended = min(EXT_CAP_DBFS, lufs - EXT_BELOW_LUFS)
    frame_s = FRAME_MS / 1000.0
    core_frames_needed = max(1, round(CORE_MIN_S / frame_s))

    quiet = envelope < extended
    core = envelope < CORE_DBFS

    pauses: list[Pause] = []
    # Run-length encode `quiet` and test each run for enough core silence.
    edges = np.flatnonzero(np.diff(quiet.astype(np.int8)))
    bounds = np.concatenate(([0], edges + 1, [quiet.size]))
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        if not quiet[lo]:
            continue
        if (hi - lo) * frame_s < min_duration:
            continue
        if int(core[lo:hi].sum()) < core_frames_needed:
            continue
        pauses.append(Pause(lo * frame_s, hi * frame_s))
    return pauses


# ---------------------------------------------------------------- attribution

@dataclass
class Segmentation:
    """Where every structural boundary of one official paper sits."""

    path: Path
    duration: float
    lufs: float
    pauses: list[Pause]
    # section -> list of the answer pause that CLOSES each slot, in slot order.
    answers: dict[str, list[Pause]] = field(default_factory=dict)
    # 問題2 only: the option-reading pause that OPENS each slot.
    option_reading: list[Pause] = field(default_factory=list)
    # 問題5-2番's 質問1 → 質問2 pause.
    shitsumon_gap: Pause | None = None
    # The pause that closes each section's preamble (instruction + 例).
    preamble_end: dict[str, Pause] = field(default_factory=dict)
    # Fitted speech rate (s/char) and mean relative fit error, for reporting.
    rate: float = 0.0
    fit_cost: float = 0.0

    def slot_span(self, section: str, slot: int) -> tuple[float, float]:
        """Speech span of one item: [start, end], excluding its answer pause.

        `slot` is 1-based. The item starts where the previous structural pause
        ended: the previous item's answer pause, or the section preamble for
        slot 1. 問題2 is NOT special — its ~20 s option-reading pause sits
        inside the item, after the announcer reads the question.
        """
        answers = self.answers[section]
        if not 1 <= slot <= len(answers):
            raise NotSegmented(f"{section} has no slot {slot}")
        if slot == 1:
            start = self.preamble_end[section].end
        else:
            start = answers[slot - 2].end
        return start, answers[slot - 1].start


CACHE_DIR = Path(__file__).resolve().parent / ".cache" / "choukai_envelope"


def measure(path: Path) -> tuple[np.ndarray, float]:
    """(envelope, LUFS) for one recording, cached on disk.

    Decoding a 42-minute sitting costs ~25 s and the bank build reads all ten,
    so the derived envelope is cached per (path, size, mtime). Both figures
    come from the same single decode.
    """
    stat = path.stat()
    # hashlib, not hash(): PYTHONHASHSEED randomises str hashing per process,
    # so a built-in hash would miss the cache on every fresh run.
    tag = hashlib.sha1(
        f"{path.resolve()}|{stat.st_size}|{int(stat.st_mtime)}|{FRAME_MS}|{SR}"
        .encode("utf-8")
    ).hexdigest()[:16]
    cached = CACHE_DIR / f"{path.stem}-{tag}.npz"
    if cached.is_file():
        try:
            blob = np.load(cached)
            return blob["envelope"], float(blob["lufs"])
        except Exception:
            cached.unlink(missing_ok=True)   # corrupt cache: fall through

    samples = decode_mono(path)
    lufs = integrated_lufs(samples, path.name)
    envelope = rms_envelope(samples)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cached, envelope=envelope, lufs=np.float64(lufs))
    return envelope, lufs


SPEAKER_LABEL_RE = re.compile(r"^[^:：]{1,6}[:：]")
ITEM_MARKER_RE = re.compile(r"^(?:例|\d+)番。")
SECTION_MARKER_RE = re.compile(r"^問題([1-5])。")


def hint_from_script(text: str) -> dict[str, list[tuple[int, int, int]]]:
    """`聴解スクリプト.txt` -> {問題N: [(spoken chars, lines, choice lines)]}.

    Speaker labels are stripped because nobody reads 「男:」 aloud. Lines are
    counted separately from characters because every line boundary costs a turn
    gap — two items of equal length at 4 vs 12 turns differ by ~7 s — and
    spoken choice lines (`1、…`) are counted again because their gap is 3.1 s
    against an ordinary turn's 0.9 s.
    """
    out: dict[str, list[tuple[int, int, int]]] = {}
    section: str | None = None
    for block in (b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()):
        lines = block.splitlines()
        marker = SECTION_MARKER_RE.match(lines[0])
        if marker:
            section = f"問題{marker.group(1)}"
            out.setdefault(section, [])
            continue
        if section is None or not ITEM_MARKER_RE.match(lines[0]):
            continue
        spoken = [SPEAKER_LABEL_RE.sub("", ln).strip() for ln in lines]
        choices = sum(1 for ln in lines if SPOKEN_CHOICE_RE.match(ln))
        out[section].append(
            (sum(len(s) for s in spoken), len(spoken), choices))
    return out


SPOKEN_CHOICE_RE = re.compile(r"^[1-4]、")


def expected_gaps(section: str, slot: int, lines: int,
                  choice_lines: int = 0) -> float:
    """Structural pause time inside one item's span, in seconds.

    Everything here is a value from `choukai-audio/SKILL.md`'s pacing table,
    which is itself measured over the 31-sitting archive — this function does
    not introduce a new number, it just says which of them apply to an item of
    a given shape. It exists so the alignment fits ONE free parameter (speech
    rate) instead of a per-section gap coefficient it has no data to fit.

    `GAP_OPTION_READING` IS counted for 問題2. Each of its items runs
    「N番。」 + situation + question -> ~20 s to read the printed options ->
    the talk -> the question again, so the option-reading pause sits inside the
    item, not between items. An earlier revision measured 問題2 spans from that
    pause's end instead; the clips it cut were missing the announcer's question
    entirely, and the composed audio ran a 12 s answer pause straight into the
    next 20 s pause with no speech between them.
    """
    dialogue = max(lines - choice_lines, 0)
    gaps = 0.0
    if section in ("問題1", "問題2"):
        # situation+question, dialogue, then the question read again
        gaps += GAP_AFTER_PRE_QUESTION + GAP_BEFORE_REPEATED_QUESTION
        gaps += TURN_GAP * max(dialogue - 3, 0)
    elif section == "問題3":
        gaps += GAP_AFTER_PRE_QUESTION
        gaps += TURN_GAP * max(dialogue - 2, 0)
        gaps += GAP_BETWEEN_SPOKEN_CHOICES * choice_lines
    elif section == "問題4":
        gaps += GAP_BETWEEN_SPOKEN_RESPONSES * max(lines - 1, 0)
    if section == "問題2":
        gaps += GAP_OPTION_READING
    if section == "問題5":
        gaps += TURN_GAP * max(dialogue - 1, 0)
        gaps += GAP_BETWEEN_SPOKEN_CHOICES * choice_lines
        if slot == 2:
            # 質問1's answer time sits INSIDE 2番's span, before 質問2 is read
            gaps += GAP_AFTER_SHITSUMON1
    return gaps


def _predict_model(known: list[tuple[int, int, float]]) -> tuple[float, float]:
    """Least-squares fit of `seconds = a*chars + b*lines` over known items.

    Calibrated per sitting rather than hard-coded, because narration rate and
    turn-gap length both vary between recordings. 問題1 and 問題2's eleven
    items are located by pause structure alone with no ambiguity anywhere in
    the archive, so they are the training set that predicts the tail.
    """
    A = np.array([[c, l] for c, l, _ in known], dtype=float)
    y = np.array([s for _, _, s in known], dtype=float)
    (a, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(a), float(b)


def _align_tail(candidates: list[Pause], predicted: list[float],
                free_before: set[int], region_start: float,
                allowed: list[set[int] | None] | None = None,
                origin: list[float | None] | None = None
                ) -> tuple[list[Pause], float] | None:
    """Pick one closing pause per predicted item, in order, by best fit.

    Monotonic DP over (item, candidate): every item's answer pause must come
    after the previous item's, and an assignment costs the relative error
    between the speech span it implies and the span the transcript predicts.
    `free_before` holds the item indices that OPEN a section. The span before
    those also contains the section's instruction and 例, whose length the
    transcript does not describe — but that is a one-sided unknown, not a free
    pass: the preamble can only ADD time, so the span must still be at least
    the item's own predicted length. Scoring them as entirely free let the DP
    park a section-opener's pause anywhere monotonic, which is how 3 of 10
    sittings ended up with 問題2 slot 1 closing before its own option-reading
    pause.

    `allowed[i]`, when given, restricts item i to those candidate indices.
    `origin[i]`, when given, measures item i's span from that absolute time
    rather than from the previous item's answer pause — 問題2 needs it, because
    each of its items begins after its own ~20 s option-reading pause and those
    pauses are the one anchor the archive never breaks.

    Returns (chosen pauses, total cost), or None if no assignment fits.
    """
    n_items, n_cand = len(predicted), len(candidates)
    if n_cand < n_items:
        return None
    INF = float("inf")
    cost = [[INF] * n_cand for _ in range(n_items)]
    back = [[-1] * n_cand for _ in range(n_items)]

    def step_cost(i: int, span: float) -> float:
        if span <= 0:
            return INF
        if i in free_before:
            # one-sided: overshoot is the preamble, undershoot is impossible
            return max(predicted[i] - span, 0.0) / max(predicted[i], 1.0)
        return abs(span - predicted[i]) / max(predicted[i], 1.0)

    def ok(i: int, j: int) -> bool:
        return allowed is None or allowed[i] is None or j in allowed[i]

    def span_from(i: int) -> float | None:
        return None if origin is None else origin[i]

    for j in range(n_cand):
        if not ok(0, j):
            continue
        base = span_from(0)
        base = region_start if base is None else base
        cost[0][j] = step_cost(0, candidates[j].start - base)

    for i in range(1, n_items):
        fixed = span_from(i)
        for j in range(i, n_cand):
            if not ok(i, j):
                continue
            best, best_k = INF, -1
            for k in range(i - 1, j):
                if cost[i - 1][k] == INF:
                    continue
                base = candidates[k].end if fixed is None else fixed
                total = cost[i - 1][k] + step_cost(
                    i, candidates[j].start - base)
                if total < best:
                    best, best_k = total, k
            cost[i][j], back[i][j] = best, best_k

    end = min(range(n_cand), key=lambda j: cost[n_items - 1][j])
    if cost[n_items - 1][end] == INF:
        return None
    out, j = [], end
    for i in range(n_items - 1, -1, -1):
        out.append(candidates[j])
        j = back[i][j]
    return list(reversed(out)), cost[n_items - 1][end]


def segment(path: Path, item_hint: dict[str, list[tuple[int, int]]] | None = None
            ) -> Segmentation:
    """Segment one official 聴解 MP3 into sections and item slots.

    `item_hint` maps each 問題 to one (chars, lines, choice_lines) triple per
    item, taken from that sitting's own `聴解スクリプト.txt`. It is required:
    pause shape alone mis-reads at least one item in 4 of the 10 sittings on
    disk (see the attribution comment below for the four failure modes).
    """
    envelope, lufs = measure(path)
    duration = envelope.size * FRAME_MS / 1000.0
    pauses = find_pauses(envelope, lufs)

    seg = Segmentation(path=path, duration=duration, lufs=lufs, pauses=pauses)

    # --- Attribution is ONE global alignment against the transcript.
    #
    #     Earlier revisions matched each structural pause against a duration
    #     band (a ~20 s option-reading pause opens every 問題2 item, a ~12 s
    #     answer pause closes 問題1/2, ~8 s closes 問題3/4). That works on most
    #     sittings and then fails on the ones that matter, because the archive
    #     does not lay these pauses down consistently:
    #
    #       - 2024-07 問題2-6番 closes with 9.28 s, under any sane 12 s floor.
    #       - 2022-12 問題1-5番 closes with 17.70 s — inside the OPTION_READING
    #         band, so a band matcher reads it as 問題2's 例 and loses an item.
    #       - 2025-07 問題4-10番 reads 4.44 s: ~0.8 s of something above the
    #         extended threshold sits inside the pause and splits it.
    #       - whether 問題2's 例 gets an option-reading pause at all varies
    #         5 sittings to 5.
    #
    #     Every one of those is unambiguous the moment the transcript is
    #     consulted: the items are 25–100 s long and their lengths are known.
    #     So candidates are simply "pauses long enough to close an item", and a
    #     monotonic DP assigns one to each of the 29 items by fitting measured
    #     spans against predicted ones. Section-opening items are free — the
    #     instruction and 例 sit in that span and the transcript omits them.
    if item_hint is None:
        raise NotSegmented(
            f"{label(path)}: segmentation needs item_hint (the sitting's own "
            f"聴解スクリプト.txt) — pause shape alone mis-reads at least one "
            f"item in 4 of the 10 archive sittings"
        )

    # section, slot, chars, lines, choice_lines
    items: list[tuple[str, int, int, int, int]] = []
    free_before: set[int] = set()
    for name, count in EXPECTED_SLOTS.items():
        hint = item_hint.get(name, [])
        if len(hint) != count:
            raise NotSegmented(
                f"{label(path)}: item_hint has {len(hint)} entries for {name}, "
                f"expected {count}"
            )
        for slot, (chars, lines, choices) in enumerate(hint, start=1):
            if slot == 1:
                free_before.add(len(items))
            items.append((name, slot, chars, lines, choices))

    candidates = [p for p in pauses if p.duration >= ANSWER_SPLIT]
    if len(candidates) < len(items):
        raise NotSegmented(
            f"{label(path)}: only {len(candidates)} pauses of {ANSWER_SPLIT}s+ "
            f"for {len(items)} items"
        )

    # --- 問題2's option-reading pauses are the one anchor the archive never
    #     breaks: six ~20 s runs, one opening each item. Take the LAST six of
    #     the band. A seventh, when present, is always at the FRONT and is
    #     either 問題2's 例 (5 sittings) or — in 2022-12 — 問題1-5番's unusually
    #     long answer pause, and dropping it from the front is right in both
    #     cases. Without this anchor the DP reads each option pause as the
    #     preceding item's answer pause and 問題2 comes out shifted by one slot.
    option = [p for p in pauses if _in(OPTION_READING, p.duration)]
    want2 = EXPECTED_SLOTS["問題2"]
    if len(option) < want2:
        raise NotSegmented(
            f"{label(path)}: found {len(option)} option-reading pauses "
            f"({OPTION_READING[0]}–{OPTION_READING[1]}s), need {want2}"
        )
    option = option[-want2:]
    seg.option_reading = option

    # Each 問題2 item is measured from its own option pause and must close
    # before the next one opens.
    index_of = {id(p): i for i, p in enumerate(candidates)}
    allowed: list[set[int] | None] = [None] * len(items)
    origin: list[float | None] = [None] * len(items)
    for i, (sec, slot, *_rest) in enumerate(items):
        if sec != "問題2":
            continue
        lo = option[slot - 1].end        # mask only: where its answer may fall
        # Slot 6 has no following option pause to bound it. Left unbounded the
        # DP overshoots into 問題3's preamble — 問題3-1番 is a one-sided opener
        # and absorbs the error for free — so bound it by the widest
        # option-to-option span this same recording uses, plus a margin.
        widest = max((option[k + 1].start - option[k].end
                      for k in range(want2 - 1)), default=180.0)
        hi = (option[slot].start if slot < want2
              else lo + widest * 1.15)
        # The mask pins WHICH pause may close this slot — between its own
        # option-reading pause and the next one. The span itself is still
        # measured from the previous item, because the option pause belongs to
        # this item and its 20 s are part of what the clip must contain.
        allowed[i] = {index_of[id(c)] for c in candidates
                      if lo < c.start < hi}
        if not allowed[i]:
            raise NotSegmented(
                f"{label(path)}: 問題2 slot {slot} has no candidate answer "
                f"pause between {lo:.1f}s and "
                f"{'EOF' if hi == math.inf else f'{hi:.1f}s'}"
            )

    # Seed the speech rate from the whole file, then refit on the alignment it
    # produces. One refit is enough: the seed is high by the preambles' share of
    # speech (~10%), and the second pass has the item spans to measure against.
    spoken_total = sum(c for _, _, c, _, _ in items)
    gaps_total = sum(expected_gaps(sec, sl, ln, ch)
                     for sec, sl, _, ln, ch in items)
    speech_time = duration - sum(p.duration for p in pauses)
    rate = max((speech_time - gaps_total), 1.0) / max(spoken_total, 1)

    chosen: list[Pause] | None = None
    fit_cost = float("inf")
    used_rate = rate
    for _ in range(2):
        used_rate = rate
        predicted = [rate * chars + expected_gaps(sec, slot, lines, choices)
                     for sec, slot, chars, lines, choices in items]
        result = _align_tail(candidates, predicted, free_before, 0.0,
                             allowed, origin)
        if result is None:
            raise NotSegmented(
                f"{label(path)}: no monotonic assignment of {len(items)} items "
                f"onto {len(candidates)} candidate pauses"
            )
        chosen, fit_cost = result
        measured = []
        for i, (sec, slot, chars, lines, choices) in enumerate(items):
            if i in free_before:
                continue
            base = origin[i] if origin[i] is not None else chosen[i - 1].end
            span = chosen[i].start - base
            measured.append(
                (chars, span - expected_gaps(sec, slot, lines, choices)))
        num = sum(c * s for c, s in measured)
        den = sum(c * c for c, _ in measured)
        if den:
            rate = max(num / den, 0.01)

    scored = len(items) - len(free_before)
    if fit_cost / max(scored, 1) > TAIL_FIT_MAX:
        raise NotSegmented(
            f"{label(path)}: best alignment averages {fit_cost / scored:.2f} "
            f"relative error per item, over the {TAIL_FIT_MAX} ceiling — the "
            f"audio does not match the transcript it was given"
        )

    seg.answers = {}
    for i, (sec, slot, _, _, _) in enumerate(items):
        seg.answers.setdefault(sec, []).append(chosen[i])
    # 問題5-2番 runs to EOF: it keeps its own 質問1 pause, 質問2 and the closing
    # announcement, because it is always the last unit of a composed paper.
    seg.answers["問題5"][-1] = Pause(duration, duration)

    # --- Where each section's preamble ends, i.e. where its first item starts.
    #
    #     This cannot be "the last pause before the first item", because the
    #     only boundary the alignment knows for that item is the ANSWER pause
    #     that CLOSES it — and the last pause before that sits inside the item,
    #     a few seconds from its end. Taking it literally gave every section a
    #     3-second first clip.
    #
    #     The item's own predicted length is what locates the start: look back
    #     `predicted` seconds from the answer pause and snap to the nearest real
    #     pause in the preamble region. 問題2 needs none of this — its slot 1
    #     opens at its option-reading pause, which is measured.
    section_first = {sec: i for i, (sec, slot, *_r) in reversed(list(enumerate(items)))
                     if slot == 1}
    prev_section_end = 0.0
    for si, (name, count) in enumerate(EXPECTED_SLOTS.items()):
        i = section_first[name]
        _, _, chars, lines, choices = items[i]
        want = rate * chars + expected_gaps(name, 1, lines, choices)
        close = seg.answers[name][0].start
        target = close - want
        # p.start, not p.end: a pause that STRADDLES the section boundary is
        # the previous section's own closing answer pause, and snapping to it
        # gives the new section a negative-length preamble (2022-12 問題3).
        window = [p for p in pauses
                  if p.start >= prev_section_end
                  and p.end <= close - MIN_ITEM_SPAN]
        if not window:
            raise NotSegmented(
                f"{label(path)}: no pause between {prev_section_end:.1f}s and "
                f"{close:.1f}s to open {name}-1番"
            )
        seg.preamble_end[name] = min(window, key=lambda p: abs(p.end - target))
        prev_section_end = seg.answers[name][-1].end

    seg.rate = used_rate
    seg.fit_cost = fit_cost / max(scored, 1)
    return seg


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("audio", nargs="+", type=Path)
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="print every recovered slot span")
    args = ap.parse_args(argv)

    failures = 0
    for path in args.audio:
        script = path.parent / "聴解スクリプト.txt"
        hint = (hint_from_script(script.read_text(encoding="utf-8"))
                if script.is_file() else None)
        try:
            seg = segment(path, hint)
        except NotSegmented as exc:
            print(f"NOT SEGMENTED  {exc}")
            failures += 1
            continue
        counts = "  ".join(f"{k}:{len(v)}" for k, v in seg.answers.items())
        print(f"ok  {path.parent.name:<22} {seg.duration / 60:5.1f} min  "
              f"LUFS {seg.lufs:6.2f}  {counts}")
        if args.verbose:
            for name in EXPECTED_SLOTS:
                for slot in range(1, len(seg.answers[name]) + 1):
                    lo, hi = seg.slot_span(name, slot)
                    print(f"      {name}-{slot}番  {lo:8.2f} → {hi:8.2f}  "
                          f"({hi - lo:6.2f}s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
