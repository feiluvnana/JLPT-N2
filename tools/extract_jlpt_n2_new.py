#!/usr/bin/env python3
"""Extract each past paper in refs/JLPT_N2_NEW/ into agent-readable Markdown.

    python3 tools/extract_jlpt_n2_new.py --all
    python3 tools/extract_jlpt_n2_new.py "refs/JLPT_N2_NEW/1. N2 7-2010"
    python3 tools/extract_jlpt_n2_new.py --all --only booklet,audio

Writes three files into every exam folder, beside the sources they come from:

| file                  | from                        |
| --------------------- | --------------------------- |
| `booklet.md`          | the exam booklet PDF        |
| `script.md`           | the listening script PDF    |
| `audio_inspection.md` | the listening MP3           |

Answer keys are NOT written here — they live in one PDF at the archive root and
are handled by `tools/extract_jlpt_n2_key.py`, which writes `key.md` alongside
these files.

## The script PDFs need OCR

All 33 booklet PDFs carry a complete text layer, so `booklet.md` is an exact
extraction. The script PDFs mostly do not: 30 of them draw every dialogue line
as a 1-bit stencil bitmap and keep only the 問題/N番 setup lines and
`（正解:N）` as real text. pypdf, pdfminer and poppler all return the same
partial text, because the dialogue simply is not there as text.

So `script.md` is a merge. Real text wins wherever it exists — it is exact — and
the rasterised lines are filled in by macOS Vision OCR (`tools/vision_ocr.swift`,
compiled on first use). OCR'd runs are fenced with `[OCR ▼]` / `[OCR ▲]` because
they are ~98% character-accurate, not exact: errors cluster on kanji that carry
furigana (整理→軽理, 一応→一思). **Never quote an OCR'd line as official
wording** — check it against the PDF first. Ruby lines are dropped from OCR'd
runs, since Vision emits them as separate half-height lines that read as noise.

Pass `--no-ocr` for a text-layer-only run.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import pdfplumber
except ImportError:  # pragma: no cover - dependency guard
    sys.exit("pdfplumber is required: pip install pdfplumber")

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "refs" / "JLPT_N2_NEW"
OCR_SRC = ROOT / "tools" / "vision_ocr.swift"
OCR_BIN = ROOT / "tools" / ".build" / "vision_ocr"
OCR_DPI = 300  # 500 measured worse: the stencils' own resolution is ~240 DPI

# `extract_pdf_text.py` already owns pypdf-with-pdfminer-fallback and the
# mojibake guard; import it rather than growing a second copy.
_spec = importlib.util.spec_from_file_location(
    "extract_pdf_text",
    ROOT / ".agents" / "external-test-import" / "scripts" / "extract_pdf_text.py")
extract_pdf_text = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(extract_pdf_text)

RUNNING_HEADER = re.compile(r"^JLPT\s*[・･]?\s*N2\s*[・･]?\s*\d{1,2}\s*[/.]\s*\d{4}\s*$")
PAGE_NUMBER = re.compile(r"^\d{1,3}$")
MONDAI_HEADING = re.compile(r"^(問題\s*\d{1,2})\b")  # promoted to a heading for navigation
SILENCE_END = re.compile(r"silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)")
VOLUME = re.compile(r"(mean_volume|max_volume):\s*(-?[0-9.]+) dB")

# Buckets from official-audio-analysis §2: structural gap / 問3・問4 answer time /
# 問5 answer time / 問1・問2 answer time / 問題2 option-reading time.
PAUSE_BUCKETS = (
    (2.5, 5.0, "~3 s", "structural gap"),
    (5.0, 9.5, "~8 s", "answer time 問題3・問題4"),
    (9.5, 11.5, "~10 s", "answer time 問題5 / 質問1→質問2"),
    (11.5, 16.0, "~12 s", "answer time 問題1・問題2"),
    (16.0, 60.0, "~20 s", "問題2 option-reading time"),
)


# ---------------------------------------------------------------------------
# locating an exam's three sources
# ---------------------------------------------------------------------------

def classify_folder(folder: Path) -> dict:
    """Sort a folder's files into booklet / script / audio."""
    pdfs = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".pdf")
    mp3s = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".mp3")
    scripts = [p for p in pdfs if "script" in p.name.lower()]
    booklets = [p for p in pdfs if p not in scripts]
    return {
        "booklet": booklets[0] if len(booklets) == 1 else None,
        "script": scripts[0] if len(scripts) == 1 else None,
        "audio": mp3s[0] if len(mp3s) == 1 else None,
        "extra_booklets": booklets[1:],
        "extra_scripts": scripts[1:],
        "extra_audio": mp3s[1:],
    }


def exam_label(folder: Path) -> str:
    m = re.search(r"N2\s*[-. ]?\s*(\d{1,2})[-. ](\d{4})", folder.name)
    return f"N2 {int(m.group(1))}/{m.group(2)}" if m else folder.name


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12]


def provenance(tool_note: str, sources: list[Path], extra: list[str] = ()) -> list[str]:
    lines = [f"> Machine-extracted by `tools/extract_jlpt_n2_new.py` ({tool_note}) from:"]
    for s in sources:
        lines.append(f"> - `{rel(s)}` (sha1 `{sha1(s)}`)")
    lines += [f"> {e}" for e in extra]  # `extra` entries carry no `>` of their own
    lines.append("> Regenerate rather than hand-edit.")
    return lines


# ---------------------------------------------------------------------------
# booklet.md — plain text-layer extraction
# ---------------------------------------------------------------------------

def tidy(line: str) -> str:
    """Squeeze the padding a PDF text layer leaves between runs."""
    return re.sub(r"[ \t]{2,}", " ", line).strip()


def is_noise(line: str) -> bool:
    """Running headers and bare page numbers; the `## page N` heading carries both."""
    return bool(RUNNING_HEADER.match(line) or PAGE_NUMBER.match(line))


def render_pages(pages: list[str]) -> list[str]:
    out: list[str] = []
    for n, raw in enumerate(pages, start=1):
        body: list[str] = []
        for line in raw.splitlines():
            line = tidy(line)
            if not line or is_noise(line):
                if line == "" and body and body[-1] != "":
                    body.append("")
                continue
            heading = MONDAI_HEADING.match(line)
            if heading and len(line) < 200:
                if body and body[-1] != "":
                    body.append("")
                body.append(f"### {line}")
            else:
                body.append(line)
        while body and body[-1] == "":
            body.pop()
        out += [f"## page {n}/{len(pages)}", ""] + (body or ["*(no text on this page)*"]) + [""]
    return out


def build_booklet(folder: Path, src: Path) -> str:
    pages = extract_pdf_text._pypdf_pages(src)
    joined = "\n".join(pages)
    engine = "pypdf"
    if extract_pdf_text.looks_like_mojibake(joined):
        alt = extract_pdf_text._pdfminer_pages(src)
        if alt and extract_pdf_text.jp_ratio("\n".join(alt)) > extract_pdf_text.jp_ratio(joined):
            pages, engine = alt, "pdfminer"
    empty = sum(1 for p in pages if not p.strip())
    extra = [f"{len(pages)} pages, extracted with {engine}; no OCR needed "
             "(this PDF's content is all real text)."]
    if empty:
        extra.append(f"**{empty} of {len(pages)} pages have no text layer** — "
                     "likely scanned; treat those pages as missing.")
    head = [f"# {exam_label(folder)} — 問題冊子（booklet, extracted）", ""]
    head += provenance("text layer", [src], extra) + [""]
    return "\n".join(head + render_pages(pages)).rstrip() + "\n"


# ---------------------------------------------------------------------------
# script.md — text layer merged with OCR of the rasterised lines
# ---------------------------------------------------------------------------

def ensure_ocr_binary() -> Path | None:
    """Compile tools/vision_ocr.swift on first use. Returns None if unavailable."""
    if OCR_BIN.is_file() and OCR_BIN.stat().st_mtime >= OCR_SRC.stat().st_mtime:
        return OCR_BIN
    if sys.platform != "darwin" or not shutil.which("swiftc"):
        return None
    OCR_BIN.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["swiftc", "-O", str(OCR_SRC), "-o", str(OCR_BIN)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"warning: could not build the OCR helper:\n{proc.stderr}", file=sys.stderr)
        return None
    return OCR_BIN


def text_lines(page) -> list[dict]:
    """Cluster the page's real text-layer words into lines."""
    words = page.extract_words()
    lines: list[dict] = []
    for w in sorted(words, key=lambda w: (round(w["top"], 1), w["x0"])):
        for ln in lines:
            if abs(ln["top"] - w["top"]) <= 3:
                ln["words"].append(w)
                ln["bottom"] = max(ln["bottom"], w["bottom"])
                break
        else:
            lines.append({"top": w["top"], "bottom": w["bottom"], "words": [w]})
    for ln in lines:
        ln["text"] = tidy(" ".join(w["text"] for w in sorted(ln["words"], key=lambda w: w["x0"])))
        ln["ocr"] = False
    return [ln for ln in lines if ln["text"]]


def stencil_boxes(page) -> list[dict]:
    """The rasterised text runs: 1-bit image stencils tall enough to be a line."""
    return [im for im in page.images if (im["bottom"] - im["top"]) >= 13]


def run_ocr(binary: Path, pngs: list[Path]) -> dict[str, list[dict]]:
    """OCR a batch of page renders; returns {png name: [line, ...]} in 0..1 coords."""
    proc = subprocess.run([str(binary)] + [str(p) for p in pngs],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"warning: OCR helper failed: {proc.stderr}", file=sys.stderr)
        return {}
    out: dict[str, list[dict]] = {}
    current = None
    for line in proc.stdout.splitlines():
        if line.startswith("--- ") and line.endswith(" ---"):
            current = Path(line[4:-4]).name
            out[current] = []
            continue
        parts = line.split("\t")
        if current is None or len(parts) != 6:
            continue
        x0, top, x1, bottom, conf, text = parts
        out[current].append({"x0": float(x0), "top": float(top), "x1": float(x1),
                             "bottom": float(bottom), "conf": float(conf),
                             "text": text.strip()})
    return out


def merge_page(page, ocr_rows: list[dict]) -> tuple[list[dict], int]:
    """Interleave OCR'd lines with the page's real text lines, top to bottom."""
    real = text_lines(page)
    if not ocr_rows:
        return real, 0

    heights = [(r["bottom"] - r["top"]) for r in ocr_rows]
    median_h = statistics.median(heights) if heights else 0.0
    merged = list(real)
    kept = 0
    for row in ocr_rows:
        if not row["text"]:
            continue
        # Vision emits furigana as its own half-height line; interleaved ruby
        # reads as noise, so drop it and say so in the file header.
        if median_h and (row["bottom"] - row["top"]) < 0.6 * median_h:
            continue
        top = row["top"] * float(page.height)
        bottom = row["bottom"] * float(page.height)
        mid = (top + bottom) / 2
        # Wherever the page has real text on this line, that text is exact —
        # prefer it and drop the OCR duplicate.
        if any(ln["top"] - 3 <= mid <= ln["bottom"] + 3 for ln in real):
            continue
        merged.append({"top": top, "bottom": bottom, "text": row["text"], "ocr": True})
        kept += 1
    merged.sort(key=lambda ln: ln["top"])
    return merged, kept


def render_script_pages(pages: list[list[dict]]) -> list[str]:
    out: list[str] = []
    for n, lines in enumerate(pages, start=1):
        out += [f"## page {n}/{len(pages)}", ""]
        if not lines:
            out += ["*(no text on this page)*", ""]
            continue
        in_ocr = False
        for ln in lines:
            text = tidy(ln["text"])
            if not text or is_noise(text):
                continue
            if ln["ocr"] and not in_ocr:
                out.append("[OCR ▼]")
                in_ocr = True
            elif not ln["ocr"] and in_ocr:
                out.append("[OCR ▲]")
                in_ocr = False
            heading = MONDAI_HEADING.match(text)
            out.append(f"### {text}" if heading and len(text) < 200 else text)
        if in_ocr:
            out.append("[OCR ▲]")
        out.append("")
    return out


def build_script(folder: Path, src: Path, use_ocr: bool) -> tuple[str, dict]:
    binary = ensure_ocr_binary() if use_ocr else None
    stats = {"pages": 0, "ocr_lines": 0, "rasterised_pages": 0, "ocr": bool(binary)}

    with pdfplumber.open(str(src)) as pdf:
        stats["pages"] = len(pdf.pages)
        rasterised = [i for i, p in enumerate(pdf.pages) if stencil_boxes(p)]
        stats["rasterised_pages"] = len(rasterised)

        ocr_by_page: dict[int, list[dict]] = {}
        if binary and rasterised:
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(
                    ["pdftoppm", "-r", str(OCR_DPI), "-png", str(src), f"{tmp}/pg"],
                    check=True, capture_output=True)
                pngs = sorted(Path(tmp).glob("pg-*.png"))
                index = {p.name: i for i, p in enumerate(pngs)}
                wanted = [p for p in pngs if index[p.name] in rasterised]
                for name, rows in run_ocr(binary, wanted).items():
                    ocr_by_page[index[name]] = rows

        pages = []
        for i, page in enumerate(pdf.pages):
            merged, kept = merge_page(page, ocr_by_page.get(i, []))
            stats["ocr_lines"] += kept
            pages.append(merged)

    extra = [f"{stats['pages']} pages."]
    if stats["rasterised_pages"] == 0:
        extra.append("This PDF's dialogue is real text throughout — no OCR was needed.")
    elif not binary:
        extra.append(
            f"**{stats['rasterised_pages']} of {stats['pages']} pages draw their dialogue as "
            "images, and OCR was not run** — those lines are missing from this file. "
            "Only the 問題/N番 setup lines and （正解:N） survive as text.")
    else:
        extra.append(
            f"**{stats['ocr_lines']} lines are OCR, not text.** This PDF draws its dialogue as "
            f"1-bit stencil bitmaps on {stats['rasterised_pages']} of {stats['pages']} pages, so "
            "no text extractor can reach it. Those runs are fenced `[OCR ▼]` … `[OCR ▲]` and are "
            "**~98% character-accurate, not exact** — errors cluster on kanji carrying furigana "
            "(整理→軽理, 一応→一思). Verify against the PDF before quoting any of it as official "
            "wording. Furigana ruby is dropped from OCR'd runs. Everything outside the fences is "
            "the exact PDF text layer.")

    head = [f"# {exam_label(folder)} — 聴解スクリプト（listening script, extracted）", ""]
    note = "text layer + Vision OCR" if stats["ocr_lines"] else "text layer"
    head += provenance(note, [src], extra) + [""]
    return "\n".join(head + render_script_pages(pages)).rstrip() + "\n", stats


# ---------------------------------------------------------------------------
# audio_inspection.md — the measurements official-audio-analysis calls for
# ---------------------------------------------------------------------------

def probe(mp3: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,bit_rate:stream=codec_name,sample_rate,channels",
         "-of", "default=noprint_wrappers=1", str(mp3)],
        capture_output=True, text=True, check=True).stdout
    return dict(line.split("=", 1) for line in out.splitlines() if "=" in line)


def analyse_audio(mp3: Path) -> dict:
    """One decode pass gives loudness and every silence at once."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp3),
         "-af", "volumedetect,silencedetect=noise=-35dB:d=0.4", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    volumes = {k: float(v) for k, v in VOLUME.findall(out)}
    silences = [(float(end) - float(dur), float(dur))
                for end, dur in SILENCE_END.findall(out)]
    return {"volumes": volumes, "silences": silences, **probe(mp3)}


def hhmmss(seconds: float) -> str:
    return f"{int(seconds) // 60}:{seconds % 60:04.1f}"


def build_audio(folder: Path, mp3: Path) -> str:
    data = analyse_audio(mp3)
    duration = float(data.get("duration", 0.0))
    long_pauses = [(s, d) for s, d in data["silences"] if d >= 2.5]
    short_gaps = [d for s, d in data["silences"] if 0.4 <= d < 2.5]

    lines = [f"# {exam_label(folder)} — 聴解音声 inspection", ""]
    lines += provenance("ffprobe + ffmpeg", [mp3], [
        "Measured per `.agents/official-audio-analysis/SKILL.md` "
        "(`silencedetect=noise=-35dB`, one pass at `d=0.4`).",
    ]) + [""]

    lines += [
        "## Basics", "",
        "| Parameter | Value | Official band |",
        "| --- | --- | --- |",
        f"| duration | {hhmmss(duration)} ({duration / 60:.1f} min) | ~50–52 min |",
        f"| codec / sample rate / channels | {data.get('codec_name', '?')} / "
        f"{data.get('sample_rate', '?')} Hz / {data.get('channels', '?')} | — |",
        f"| bit rate | {int(data.get('bit_rate', 0)) // 1000} kb/s | — |",
        f"| mean volume | {data['volumes'].get('mean_volume', float('nan')):.1f} dB | −17 to −18 dB |",
        f"| max volume | {data['volumes'].get('max_volume', float('nan')):.1f} dB | — |",
        "",
        "## Long-pause histogram (≥2.5 s)", "",
        "| Bucket | Count | Meaning |",
        "| --- | --- | --- |",
    ]
    counted = 0
    for lo, hi, name, meaning in PAUSE_BUCKETS:
        n = sum(1 for _, d in long_pauses if lo <= d < hi)
        counted += n
        lines.append(f"| {name} ({lo:g}–{hi:g} s) | {n} | {meaning} |")
    lines += [f"| **total** | **{len(long_pauses)}** | {len(long_pauses) - counted} outside every bucket |", ""]

    if short_gaps:
        lines += [
            "## Dialogue pacing (0.4–2.5 s gaps)", "",
            f"- {len(short_gaps)} gaps; median **{statistics.median(short_gaps):.2f} s**, "
            f"mean {statistics.fmean(short_gaps):.2f} s "
            f"(official turn gap ≈ 1.0–1.5 s, the pipeline uses 1.3 s)",
            "",
        ]

    lines += [
        "## Long-pause timeline", "",
        "Ordered `(start, duration)`. Attribute sections from the signatures in "
        "`official-audio-analysis` §3 — a `20 s → talk → 12 s` cycle is 問題2, "
        "`3 s ×3 → 8 s` is 問題3/問題5's spoken choices, a dense run of lone 8 s "
        "pauses is 問題4. Counts are measured, section labels are not.", "",
        "| # | start | duration |",
        "| --- | --- | --- |",
    ]
    lines += [f"| {i} | {hhmmss(s)} | {d:.2f} s |"
              for i, (s, d) in enumerate(long_pauses, start=1)]
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------

def process(folder: Path, only: set[str], use_ocr: bool) -> list[str]:
    notes: list[str] = []
    found = classify_folder(folder)
    for kind in ("booklet", "script", "audio"):
        for extra in found[f"extra_{kind}s" if kind != "audio" else "extra_audio"]:
            notes.append(f"ignored extra {kind}: {extra.name}")

    if "booklet" in only:
        if found["booklet"]:
            (folder / "booklet.md").write_text(
                build_booklet(folder, found["booklet"]), encoding="utf-8")
        else:
            notes.append("no booklet PDF — booklet.md not written")

    if "script" in only:
        if found["script"]:
            text, stats = build_script(folder, found["script"], use_ocr)
            (folder / "script.md").write_text(text, encoding="utf-8")
            if stats["rasterised_pages"] and not stats["ocr"]:
                notes.append(f"script.md is missing its dialogue "
                             f"({stats['rasterised_pages']} rasterised pages, OCR off)")
            elif stats["ocr_lines"]:
                notes.append(f"script.md: {stats['ocr_lines']} OCR lines")
        else:
            notes.append("no script PDF — script.md not written")

    if "audio" in only:
        if found["audio"]:
            (folder / "audio_inspection.md").write_text(
                build_audio(folder, found["audio"]), encoding="utf-8")
        else:
            notes.append("no MP3 — audio_inspection.md not written")
    return notes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="*", type=Path, help="exam folders to extract")
    ap.add_argument("--all", action="store_true", help="every folder under refs/JLPT_N2_NEW/")
    ap.add_argument("--only", default="booklet,script,audio",
                    help="comma-separated subset of booklet,script,audio")
    ap.add_argument("--no-ocr", action="store_true",
                    help="skip OCR; script.md then omits the rasterised dialogue")
    args = ap.parse_args()

    folders = list(args.folders)
    if args.all:
        folders += sorted(d for d in ARCHIVE.iterdir() if d.is_dir())
    if not folders:
        ap.error("pass one or more folders, or --all")

    only = {s.strip() for s in args.only.split(",") if s.strip()}
    unknown = only - {"booklet", "script", "audio"}
    if unknown:
        ap.error(f"unknown --only value(s): {', '.join(sorted(unknown))}")

    if "script" in only and not args.no_ocr and ensure_ocr_binary() is None:
        print("warning: no OCR helper (needs macOS + swiftc) — the rasterised "
              "dialogue will be missing from script.md", file=sys.stderr)

    failures = 0
    for folder in folders:
        if not folder.is_dir():
            print(f"ERROR not a directory: {folder}", file=sys.stderr)
            failures += 1
            continue
        try:
            notes = process(folder, only, not args.no_ocr)
        except Exception as e:  # keep going; one bad paper must not stop the sweep
            print(f"ERROR {folder.name}: {e}", file=sys.stderr)
            failures += 1
            continue
        suffix = ("  [" + "; ".join(notes) + "]") if notes else ""
        print(f"ok {folder.name}{suffix}")

    if failures:
        sys.exit(f"{failures} folder(s) failed")


if __name__ == "__main__":
    main()
