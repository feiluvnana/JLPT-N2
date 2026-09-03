#!/usr/bin/env python3
"""Upload the repo's large binaries to GitHub Releases — once each, and only again when they change.

`refs/` is 2.5 GB of scanned PDFs and MP3s and the exam audio adds ~600 MB more.
None of it is in git (AGENTS.md §3), so the Releases are the only copy a fresh
clone or a CI run can fetch. Three rules follow, and this script exists to
enforce all of them:

1. **One release per kind, reused forever.** `audio` holds one `<test_id>.mp3`
   per test; `refs` holds one zip per top-level `refs/` folder. Both tags are
   stable addresses — `build_interactive.py` and `build_model_answer.py`
   hard-code `…/releases/download/audio/<test_id>.mp3` as the player's fallback
   URL, so a new tag would silently 404 every deployed sheet. This script never
   creates a release whose tag already exists; it looks the tag up first and
   only creates what is genuinely missing.

2. **The archive ships as zips, one per kind.** 264 loose assets meant 264
   uploads, 264 names for GitHub to rewrite, and no way to say "give me the
   Shinkanzen set". `refs/Shinkanzen/`, `refs/Soumatome/` and
   `refs/JLPT_N2_NEW/` each become one `<name>.zip`, stored uncompressed —
   PDFs and MP3s are already compressed, so deflating them costs minutes of CPU
   to save nothing. Unzip a file back into `refs/` and the tree is restored.

3. **A file is uploaded once.** The first version of this script re-pushed
   every asset with `--clobber` on every run: 2.5 GB over the wire to change
   nothing. Now each run reads the release's existing asset list and skips
   whatever has not changed, tracked in `logs/upload_manifest.json`.

Change detection differs by asset kind, because a zip is a derived artifact:

* A plain file (the exam MP3s) is unchanged when the remote asset's size matches
  and the manifest's sha256 still matches the bytes on disk.
* A zip is unchanged when its **members** are: the manifest stores a fingerprint
  over every member's path, size and sha256, and the zip is only rebuilt and
  re-uploaded when that fingerprint moves. Hashing the zip itself would be
  useless — two zips of identical inputs differ in their stored mtimes. Their
  SIZES do not, though, so a zip with no manifest record is rebuilt and its size
  compared with the remote asset's: equal means it is already up there and only
  the bookkeeping was lost. The manifest is flushed after every single asset, so
  a run killed at 90% keeps the 90%.

Either way the manifest also records the (size, mtime_ns) each sha was computed
from, so a re-run does not re-hash gigabytes it already knows. On a machine that
has never run this (a fresh clone, CI), mtimes differ but the shas still match,
so files are hashed once and still not re-uploaded.

Usage:
    python3 tools/upload_files.py [tests|refs|all] [test_id]
    python3 tools/upload_files.py all --dry-run     # say what would upload
    python3 tools/upload_files.py refs --force      # rebuild and re-upload
    # or via Makefile:
    make upload-files [TARGET=tests|refs|all] [TEST=<id>]
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
REFS = ROOT / "refs"
MANIFEST = ROOT / "logs" / "upload_manifest.json"

# What counts as a binary the archive owns. Everything else under refs/ (the
# *.md extracts, answer_keys.json) is in git and must NOT be duplicated here.
REFS_EXTS = {".pdf", ".mp3"}

# The two stable tags. Never rename one: the deployed sheets fetch their audio
# from `releases/download/audio/<test_id>.mp3` (exam-app), and `refs` is what
# AGENTS.md §3 tells a reader to pull the archive from.
TAGS = {
    "tests": ("audio", "JLPT N2 Listening Audio (聴解.mp3)",
              "One MP3 per test — mock exams and imported papers. "
              "Asset name is the test id."),
    "refs": ("refs", "JLPT N2 Reference Archive (refs/)",
             "The refs/ binaries, one zip per source: official past papers "
             "(JLPT_N2_NEW), Shin Kanzen Master (Shinkanzen) and 日本語総まとめ "
             "(Soumatome). Unzip into refs/ to restore the tree."),
}

# `refs-audio`/`refs-pdf` were the previous split. Nothing was ever uploaded to
# them, so they are accepted as aliases rather than kept alive.
ALIASES = {"refs-audio": "refs", "refs-pdf": "refs"}


def ensure_gh_cli() -> None:
    if not shutil.which("gh"):
        sys.exit("Error: 'gh' (GitHub CLI) is not installed or not in PATH.\n"
                 "Install via: brew install gh (macOS) or see https://cli.github.com/")


def require_push_access() -> None:
    """Fail early, and legibly, when the ACTIVE `gh` account cannot write here.

    GitHub answers an unauthorized asset delete with 404 rather than 403, so
    `gh release upload --clobber` run under a read-only account dies on
    `HTTP 404: Not Found (…/releases/assets/<id>)` — which reads like a corrupt
    release, not like an auth problem, and sends the reader looking at the wrong
    thing (2026-09-03: a second logged-in account was active on the machine and
    had pull-only access to the repo). One API call up front says it plainly.
    """
    proc = subprocess.run(["gh", "api", "repos/{owner}/{repo}", "--jq", ".permissions.push"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return      # no repo context, offline, or an old gh — let the upload report it
    if proc.stdout.strip() == "true":
        return
    who = subprocess.run(["gh", "api", "user", "--jq", ".login"],
                         capture_output=True, text=True).stdout.strip()
    sys.exit(f"Error: the active gh account ({who or 'unknown'}) has no push access to "
             f"this repo, so `gh release upload` would fail with a misleading HTTP 404.\n"
             f"       Pick the account that owns the repo — `gh auth status` lists who is "
             f"logged in, `gh auth switch --user <owner>` activates one — then re-run.")


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


def file_sha256(path: Path, cached: dict | None) -> str:
    """sha256 of `path`, reusing a cached value when the file is untouched.

    Hashing the whole archive costs ~20 s; doing it on every run for files whose
    (size, mtime_ns) have not moved since the recorded hash is pure waste.
    """
    st = path.stat()
    if (cached and cached.get("sha256")
            and cached.get("size") == st.st_size
            and cached.get("mtime_ns") == st.st_mtime_ns):
        return cached["sha256"]
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stat_record(path: Path, sha: str) -> dict:
    st = path.stat()
    return {"size": st.st_size, "mtime_ns": st.st_mtime_ns, "sha256": sha}


def release_assets(tag: str) -> dict[str, int] | None:
    """`{asset name: size}` for an existing release, or None if the tag has none.

    None means "no release here yet"; an empty dict means "the release exists and
    is empty". Collapsing the two would make us try to create a release that is
    already there.
    """
    proc = subprocess.run(["gh", "release", "view", tag, "--json", "assets"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        err = (proc.stderr or "").lower()
        if "not found" in err:
            return None
        # Anything else (auth, network, rate limit) must NOT be read as "missing"
        # — creating a second release under a taken tag fails, and treating every
        # asset as absent would re-upload the whole archive.
        sys.exit(f"Error: could not read release '{tag}':\n{proc.stderr.strip()}")
    data = json.loads(proc.stdout or "{}")
    return {a["name"]: a["size"] for a in data.get("assets", [])}


def ensure_release(tag: str, title: str, notes: str, dry_run: bool) -> dict[str, int]:
    assets = release_assets(tag)
    if assets is not None:
        return assets
    if dry_run:
        print(f"  [dry-run] would create GitHub Release '{tag}'", flush=True)
        return {}
    print(f"  Creating GitHub Release '{tag}'...", flush=True)
    subprocess.run(["gh", "release", "create", tag, "--title", title, "--notes", notes],
                   check=True)
    return {}


def upload(tag: str, staged: Path) -> None:
    print(f"    -> {staged.name} ({staged.stat().st_size / 1e6:.1f} MB)", flush=True)
    subprocess.run(["gh", "release", "upload", tag, str(staged), "--clobber"], check=True)


# --------------------------------------------------------------------------- #
# tests: one MP3 per test, asset name == test id
# --------------------------------------------------------------------------- #

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
    # name IS the test id — never sanitize it into something else.
    return [(d / "聴解.mp3", f"{d.name}.mp3") for d in available]


def sync_files(tag: str, files: list[tuple[Path, str]], remote: dict[str, int],
               manifest: dict, force: bool, dry_run: bool) -> None:
    pending, skipped = [], 0
    for path, name in files:
        key = f"{tag}/{name}"
        entry = manifest.get(key)
        sha = file_sha256(path, entry)
        if not force and remote.get(name) == path.stat().st_size:
            # Either we have a matching sha on record, or the asset is up there at
            # exactly this size and we have no record at all (first run after this
            # script changed, or a fresh clone). A size match on a multi-megabyte
            # binary is evidence enough to adopt rather than push the same bytes
            # again; the sha stored now makes every later run exact.
            if entry is None or entry.get("sha256") == sha:
                manifest[key] = stat_record(path, sha)
                skipped += 1
                continue
        pending.append((path, name, sha))

    report(tag, len(files), skipped, [(p, n) for p, n, _ in pending], dry_run)
    if dry_run or not pending:
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        for path, name, sha in pending:
            staged = Path(tmpdir) / name
            try:
                os.link(path, staged)          # copying 575 MB just to rename it
            except OSError:                    # is slower than the upload itself
                shutil.copy2(path, staged)
            upload(tag, staged)
            manifest[f"{tag}/{name}"] = stat_record(path, sha)
            save_manifest(manifest)     # per asset — an interrupted run keeps what it sent
            staged.unlink(missing_ok=True)
    print(f"  ✓ Uploaded {len(pending)} file(s) to release '{tag}'.", flush=True)


# --------------------------------------------------------------------------- #
# refs: one zip per top-level folder
# --------------------------------------------------------------------------- #

def refs_groups() -> list[tuple[str, list[Path]]]:
    """`[(asset name, member paths)]` — one entry per top-level refs/ folder."""
    if not REFS.is_dir():
        print(f"No refs directory found at {REFS}.", flush=True)
        return []
    groups = []
    for d in sorted(p for p in REFS.iterdir() if p.is_dir()):
        members = sorted(p for p in d.rglob("*")
                         if p.is_file() and p.suffix.lower() in REFS_EXTS)
        if members:
            groups.append((f"{d.name}.zip", members))
    # A binary sitting directly in refs/ belongs to no group and would be left
    # behind in silence — the one failure mode that looks exactly like success.
    loose = [p for p in sorted(REFS.iterdir())
             if p.is_file() and p.suffix.lower() in REFS_EXTS]
    if loose:
        print(f"  ! {len(loose)} binary/ies sit directly in refs/ and are in no zip: "
              + ", ".join(p.name for p in loose)
              + "\n    Move each into its source folder (refs/<Source>/…) — the zips are "
                "per top-level folder.", flush=True)
    if not groups:
        print(f"No {'/'.join(sorted(REFS_EXTS))} files found under {REFS}.", flush=True)
    return groups


def fingerprint(members: list[Path], cache: dict) -> tuple[str, dict]:
    """A hash over what the zip WOULD contain, plus the refreshed member cache.

    Hashing the built zip instead would be useless: zip entries carry mtimes, so
    two zips of byte-identical inputs differ. The members are the real input.
    """
    h = hashlib.sha256()
    fresh = {}
    for m in members:
        rel = str(m.relative_to(REFS))
        sha = file_sha256(m, cache.get(rel))
        fresh[rel] = stat_record(m, sha)
        h.update(f"{rel}\0{fresh[rel]['size']}\0{sha}\n".encode("utf-8"))
    return h.hexdigest(), fresh


def build_zip(dest: Path, members: list[Path]) -> Path:
    # ZIP_STORED, not ZIP_DEFLATED: PDFs and MP3s are already compressed, so
    # deflating 2.5 GB of them burns minutes of CPU to save a rounding error.
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_STORED, allowZip64=True) as zf:
        for m in members:
            zf.write(m, arcname=str(m.relative_to(REFS)))
    return dest


def sync_zips(tag: str, groups: list[tuple[str, list[Path]]], remote: dict[str, int],
              manifest: dict, force: bool, dry_run: bool) -> None:
    pending, skipped = [], 0
    for name, members in groups:
        key = f"{tag}/{name}"
        entry = manifest.get(key) or {}
        fp, fresh = fingerprint(members, entry.get("members", {}))
        entry = {**entry, "members": fresh, "fingerprint": fp,
                 "member_count": len(members),
                 "member_bytes": sum(v["size"] for v in fresh.values())}
        manifest[key] = entry
        if not force and name in remote and entry.get("uploaded_fingerprint") == fp:
            skipped += 1
            continue
        # No record of having uploaded THIS content, but the release holds an asset
        # by that name. Rebuilding settles it without a transfer: a ZIP_STORED
        # archive's SIZE is a function of its members (names + bytes), not of when
        # it was built, so a rebuilt zip whose size matches the remote one IS the
        # remote one. This is the interrupted-run case — two 1 GB zips landed, the
        # process was killed before it could write them down — and rebuilding costs
        # seconds against re-uploading gigabytes.
        pending.append((name, members, fp))

    report(tag, len(groups), skipped,
           [(REFS / n, n) for n, _, _ in pending], dry_run,
           sizer=lambda n: manifest[f"{tag}/{n.name}"]["member_bytes"])
    if dry_run or not pending:
        return
    sent = adopted = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for name, members, fp in pending:
            print(f"    building {name} ({len(members)} file(s))...", flush=True)
            staged = build_zip(Path(tmpdir) / name, members)
            size = staged.stat().st_size
            if not force and remote.get(name) == size:
                print(f"    = {name} already on the release at {size / 1e6:.1f} MB "
                      f"— recording it, not re-sending.", flush=True)
                adopted += 1
            else:
                upload(tag, staged)
                sent += 1
            manifest[f"{tag}/{name}"]["uploaded_fingerprint"] = fp
            manifest[f"{tag}/{name}"]["uploaded_size"] = size
            # Write down every asset as it lands. A 2 GB run that dies half way
            # must not lose the half it finished — that is how the previous
            # version turned one interruption into a second full upload.
            save_manifest(manifest)
            staged.unlink(missing_ok=True)
    parts = [f"{sent} zip(s) uploaded" if sent else "",
             f"{adopted} already present" if adopted else ""]
    print(f"  ✓ Release '{tag}': " + ", ".join(p for p in parts if p) + ".", flush=True)


# --------------------------------------------------------------------------- #

def report(tag: str, total: int, skipped: int, pending: list[tuple[Path, str]],
           dry_run: bool, sizer=None) -> None:
    if skipped:
        print(f"  {skipped} of {total} already on release '{tag}' and unchanged — skipped.",
              flush=True)
    if not pending:
        print(f"  ✓ Release '{tag}' is up to date ({total} asset(s)).", flush=True)
        return
    mb = sum((sizer(p) if sizer else p.stat().st_size) for p, _ in pending) / 1e6
    print(f"  {'would upload' if dry_run else 'Uploading'} {len(pending)} asset(s) "
          f"({mb:.1f} MB) to release '{tag}'...", flush=True)
    if dry_run:
        for path, name in pending:
            print(f"    [dry-run] {path.relative_to(ROOT)} -> {name}", flush=True)


def main():
    ap = argparse.ArgumentParser(
        description="Upload exam audio and the refs/ archive to GitHub Releases, "
                    "skipping anything already uploaded and unchanged.")
    ap.add_argument("target", nargs="?", default="tests",
                    choices=["tests", "refs", "all", "refs-audio", "refs-pdf"],
                    help="What to upload: 'tests' (mock/imported exam MP3s), "
                         "'refs' (one zip per refs/ folder), or 'all' (default: tests)")
    ap.add_argument("test_id", nargs="?", default=None,
                    help="Specific test id when target is 'tests' (default: all tests)")
    ap.add_argument("--force", action="store_true",
                    help="Rebuild and re-upload every asset even if unchanged")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would be uploaded; touch nothing")
    args = ap.parse_args()

    if args.target in ALIASES:
        print(f"Note: '{args.target}' is now '{ALIASES[args.target]}' — the refs "
              f"binaries ship as one zip per folder in a single release.", flush=True)
        args.target = ALIASES[args.target]

    ensure_gh_cli()
    if not args.dry_run:
        require_push_access()
    manifest = load_manifest()
    targets = ["tests", "refs"] if args.target == "all" else [args.target]

    try:
        for t in targets:
            tag, title, notes = TAGS[t]
            if t == "tests":
                files = tests_audio_files(args.test_id)
                if not files:
                    continue
                print(f"\n[{tag}] {len(files)} test audio file(s)", flush=True)
                remote = ensure_release(tag, title, notes, args.dry_run)
                sync_files(tag, files, remote, manifest, args.force, args.dry_run)
            else:
                groups = refs_groups()
                if not groups:
                    continue
                print(f"\n[{tag}] {len(groups)} archive(s): "
                      + ", ".join(f"{n} ({len(m)} files)" for n, m in groups), flush=True)
                remote = ensure_release(tag, title, notes, args.dry_run)
                sync_zips(tag, groups, remote, manifest, args.force, args.dry_run)
    finally:
        # Whatever we did manage to upload before an interruption must be written
        # down, or the next run pushes those gigabytes a second time.
        if not args.dry_run:
            save_manifest(manifest)
            print(f"\nManifest: {MANIFEST.relative_to(ROOT)} ({len(manifest)} asset(s))",
                  flush=True)


if __name__ == "__main__":
    main()
