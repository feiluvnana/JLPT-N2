#!/usr/bin/env python3
"""Upload the repo's large binaries to GitHub Releases — once each, and only again when they change.

`refs/` is 2.5 GB of scanned PDFs and MP3s and the exam audio adds ~600 MB more.
None of it is in git (AGENTS.md §3), so the Releases are the only copy a fresh
clone or a CI run can fetch. Two rules follow, and this script exists to enforce
both:

1. **One release per kind, reused forever.** The tags `audio`, `refs-audio` and
   `refs-pdf` are stable addresses — `build_interactive.py` and
   `build_model_answer.py` hard-code
   `…/releases/download/audio/<test_id>.mp3` as the player's fallback URL, so a
   new tag would silently 404 every deployed sheet. This script never creates a
   release whose tag already exists; it looks the tag up first and only creates
   what is genuinely missing.

2. **A file is uploaded once.** The previous version re-pushed every asset with
   `--clobber` on every run: 264 files and 2.5 GB over the wire to change
   nothing. Now each run reads the release's existing asset list and skips any
   file whose remote size matches and whose local content has not changed since
   the last upload, tracked in `logs/upload_manifest.json`.

The manifest holds, per `<tag>/<asset name>`: the source path relative to the
repo, the size, and the sha256 — plus the (size, mtime_ns) the sha was computed
from, so a re-run does not re-hash gigabytes it already knows. On a machine that
has never run this (a fresh clone, CI), mtimes differ but the sha still matches,
so the files are hashed once and still not re-uploaded.

Usage:
    python3 tools/upload_files.py [tests|refs-audio|refs-pdf|all] [test_id]
    python3 tools/upload_files.py all --dry-run     # say what would upload
    python3 tools/upload_files.py refs-pdf --force  # re-upload regardless
    # or via Makefile:
    make upload-files [TARGET=tests|refs-audio|refs-pdf|all] [TEST=<id>]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
REFS = ROOT / "refs"
MANIFEST = ROOT / "logs" / "upload_manifest.json"

# The three stable tags. Never rename one: the deployed sheets fetch their audio
# from `releases/download/audio/<test_id>.mp3` (exam-app), and the refs tags are
# what AGENTS.md §3 tells a reader to pull the archive from.
TAGS = {
    "tests": ("audio", "JLPT N2 Listening Audio (聴解.mp3)",
              "Audio files for JLPT N2 mock exams and imported papers."),
    "refs-audio": ("refs-audio", "JLPT N2 Reference Audio Archive (refs/)",
                   "Reference .MP3 files from official past exams and textbook CDs."),
    "refs-pdf": ("refs-pdf", "JLPT N2 Reference PDF Archive (refs/)",
                 "Reference .PDF files from official past exams and textbooks."),
}

# GitHub rewrites anything outside this set in an uploaded asset's name, so the
# name we ask for and the name the release ends up holding would differ — and a
# name-keyed "already uploaded?" check would miss every time, re-pushing the
# whole archive forever. Sanitize to the safe set ourselves, so what we upload
# is exactly what we look for.
SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")
# Everything SAFE_NAME keeps, plus the space — a space maps 1-to-1 onto `_`, so
# a name built only from these characters loses nothing and needs no disambiguator.
REVERSIBLE = re.compile(r"^[A-Za-z0-9._\- ]*$")


def ensure_gh_cli() -> None:
    if not shutil.which("gh"):
        sys.exit("Error: 'gh' (GitHub CLI) is not installed or not in PATH.\n"
                 "Install via: brew install gh (macOS) or see https://cli.github.com/")


def asset_name(rel: Path) -> str:
    """A deterministic, collision-free, GitHub-safe asset name for a refs path.

    `refs/JLPT_N2_NEW/15. N2 12-2024/Nghe N2 T12-2024.mp3` →
    `JLPT_N2_NEW__15._N2_12-2024__Nghe_N2_T12-2024.mp3`.

    Non-ASCII segments — Vietnamese and Japanese file names are all over the
    archive — collapse to `_`, which can make two different paths share a name.
    Those get a short digest of the full relative path appended. Paths that are
    already ASCII do not, so the common case stays readable, and a name never
    changes because a sibling file appeared or went away.
    """
    flat = str(rel).replace("/", "__")
    safe = SAFE_NAME.sub("_", flat).strip("_") or "asset"
    if not REVERSIBLE.match(flat):
        digest = hashlib.sha256(str(rel).encode("utf-8")).hexdigest()[:8]
        stem, dot, ext = safe.rpartition(".")
        safe = f"{stem}-{digest}{dot}{ext}" if dot else f"{safe}-{digest}"
    return safe


def load_manifest() -> dict:
    if MANIFEST.is_file():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"Warning: {MANIFEST} is not valid JSON — starting a fresh manifest.",
                  flush=True)
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2,
                                   sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path, entry: dict | None) -> str:
    """sha256 of `path`, reusing the manifest's value when the file is untouched.

    Hashing the whole archive costs ~20 s; doing it on every run for files whose
    (size, mtime_ns) have not moved since the recorded hash is pure waste.
    """
    st = path.stat()
    if (entry and entry.get("sha256")
            and entry.get("size") == st.st_size
            and entry.get("mtime_ns") == st.st_mtime_ns):
        return entry["sha256"]
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def release_assets(tag: str) -> dict[str, int] | None:
    """`{asset name: size}` for an existing release, or None if the tag has none.

    None means "no release here yet"; an empty dict means "the release exists and
    is empty". Collapsing the two would make us try to create a release that is
    already there.
    """
    proc = subprocess.run(
        ["gh", "release", "view", tag, "--json", "assets"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        err = (proc.stderr or "").lower()
        if "release not found" in err or "not found" in err:
            return None
        # Anything else (auth, network, rate limit) must NOT be read as "missing"
        # — creating a second release under a taken tag fails, and treating every
        # asset as absent would re-upload the archive.
        sys.exit(f"Error: could not read release '{tag}':\n{proc.stderr.strip()}")
    data = json.loads(proc.stdout or "{}")
    return {a["name"]: a["size"] for a in data.get("assets", [])}


def ensure_release(tag: str, title: str, notes: str, dry_run: bool) -> dict[str, int]:
    assets = release_assets(tag)
    if assets is not None:
        return assets
    if dry_run:
        print(f"[dry-run] would create GitHub Release '{tag}'", flush=True)
        return {}
    print(f"Creating GitHub Release '{tag}'...", flush=True)
    subprocess.run(["gh", "release", "create", tag, "--title", title, "--notes", notes],
                   check=True)
    return {}


def sync(tag: str, title: str, notes: str, files: list[tuple[Path, str]],
         manifest: dict, force: bool, dry_run: bool) -> None:
    """Upload every `(path, asset_name)` in `files` that the release does not
    already hold in its current form."""
    remote = ensure_release(tag, title, notes, dry_run)

    pending: list[tuple[Path, str, str]] = []   # (path, asset, sha)
    skipped = 0
    for path, name in files:
        key = f"{tag}/{name}"
        entry = manifest.get(key)
        sha = file_sha256(path, entry)
        if not force and remote.get(name) == path.stat().st_size:
            if entry and entry.get("sha256") == sha:
                skipped += 1
                manifest[key] = record(path, sha)      # refresh the mtime cache
                continue
            if not entry:
                # The asset is up there at exactly this size and we have no record
                # of it (first run after this script changed, or a fresh clone).
                # Adopt it rather than pushing the same bytes again; the size match
                # on a multi-megabyte binary is evidence enough, and the sha we
                # store now makes every later run exact.
                skipped += 1
                manifest[key] = record(path, sha)
                continue
        pending.append((path, name, sha))

    if skipped:
        print(f"  {skipped} file(s) already on release '{tag}' and unchanged — skipped.",
              flush=True)
    if not pending:
        print(f"✓ Release '{tag}' is up to date ({len(files)} file(s)).", flush=True)
        return

    total_mb = sum(p.stat().st_size for p, _, _ in pending) / 1e6
    verb = "would upload" if dry_run else "Uploading"
    print(f"  {verb} {len(pending)} file(s) ({total_mb:.1f} MB) to release '{tag}'...",
          flush=True)

    if dry_run:
        for path, name, _ in pending:
            print(f"    [dry-run] {path.relative_to(ROOT)} -> {name}", flush=True)
        return

    # gh takes the asset name from the file name on disk, so each upload is staged
    # under the name we want. Hard-link when the filesystem allows it: copying
    # 2.5 GB into a temp dir just to rename it is the one thing slower than the
    # upload itself.
    with tempfile.TemporaryDirectory() as tmpdir:
        for path, name, sha in pending:
            staged = Path(tmpdir) / name
            try:
                os.link(path, staged)
            except OSError:
                shutil.copy2(path, staged)
            print(f"    -> {name} ({staged.stat().st_size / 1e6:.1f} MB)", flush=True)
            subprocess.run(["gh", "release", "upload", tag, str(staged), "--clobber"],
                           check=True)
            manifest[f"{tag}/{name}"] = record(path, sha)
            staged.unlink(missing_ok=True)

    print(f"✓ Uploaded {len(pending)} file(s) to GitHub Release '{tag}'.", flush=True)


def record(path: Path, sha: str) -> dict:
    st = path.stat()
    return {"path": str(path.relative_to(ROOT)), "size": st.st_size,
            "mtime_ns": st.st_mtime_ns, "sha256": sha}


def tests_audio_files(test_id: str | None) -> list[tuple[Path, str]]:
    available = [d for d in sorted(TESTS.iterdir())
                 if d.is_dir() and (d / "聴解.mp3").is_file()]
    if not available:
        print(f"No tests with 聴解.mp3 found under {TESTS}.", flush=True)
        return []
    if test_id and test_id.lower() != "all":
        matched = [d for d in available if d.name == test_id]
        if not matched:
            print(f"Warning: No test folder matches '{test_id}'.", flush=True)
            print("Available test IDs with 聴解.mp3:", flush=True)
            for d in available:
                print(f"  - {d.name}", flush=True)
            sys.exit(1)
        available = matched
    # The player's fallback URL is `…/download/audio/<test_id>.mp3`, so the asset
    # name IS the test id — do not sanitize it into something else.
    return [(d / "聴解.mp3", f"{d.name}.mp3") for d in available]


def refs_files(ext: str) -> list[tuple[Path, str]]:
    if not REFS.is_dir():
        print(f"No refs directory found at {REFS}.", flush=True)
        return []
    # Case-insensitive: the archive carries both `.pdf` and `.PDF`.
    files = sorted(p for p in REFS.rglob("*")
                   if p.is_file() and p.suffix.lower() == ext)
    if not files:
        print(f"No *{ext} files found under {REFS}.", flush=True)
        return []
    out, seen = [], {}
    for f in files:
        name = asset_name(f.relative_to(REFS))
        if name in seen:
            sys.exit(f"Error: {f} and {seen[name]} both map to asset '{name}' — "
                     f"rename one, or the release can only hold one of them.")
        seen[name] = f
        out.append((f, name))
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Upload exam audio and refs binaries to GitHub Releases, "
                    "skipping anything already uploaded and unchanged.")
    ap.add_argument("target", nargs="?", default="tests",
                    choices=["tests", "refs-audio", "refs-pdf", "all"],
                    help="What to upload: 'tests' (mock/imported exam MP3s), "
                         "'refs-audio', 'refs-pdf', or 'all' (default: tests)")
    ap.add_argument("test_id", nargs="?", default=None,
                    help="Specific test id when target is 'tests' (default: all tests)")
    ap.add_argument("--force", action="store_true",
                    help="Re-upload every file even if the release already has it")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would be uploaded; touch nothing")
    args = ap.parse_args()

    ensure_gh_cli()
    manifest = load_manifest()
    targets = ["tests", "refs-audio", "refs-pdf"] if args.target == "all" else [args.target]

    try:
        for t in targets:
            tag, title, notes = TAGS[t]
            files = (tests_audio_files(args.test_id) if t == "tests"
                     else refs_files(".mp3" if t == "refs-audio" else ".pdf"))
            if not files:
                continue
            print(f"\n[{tag}] {len(files)} local file(s)", flush=True)
            sync(tag, title, notes, files, manifest, args.force, args.dry_run)
    finally:
        # Whatever we did manage to upload before an interruption must be written
        # down, or the next run pushes those gigabytes a second time.
        if not args.dry_run:
            save_manifest(manifest)
            print(f"\nManifest: {MANIFEST.relative_to(ROOT)} ({len(manifest)} asset(s))",
                  flush=True)


if __name__ == "__main__":
    main()
