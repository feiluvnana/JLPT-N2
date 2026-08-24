#!/usr/bin/env python3
"""Upload exam audio (tests/<id>/聴解.mp3) and reference files (refs/ .mp3 & .pdf) to GitHub Releases.

Usage:
    python3 tools/upload_files.py [tests|refs-audio|refs-pdf|all] [test_id]
    # or via Makefile:
    make upload-files [TARGET=tests|refs-audio|refs-pdf|all] [TEST=<id>]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
REFS = ROOT / "refs"


def ensure_gh_cli() -> None:
    if not shutil.which("gh"):
        sys.exit("Error: 'gh' (GitHub CLI) is not installed or not in PATH.\n"
                 "Install via: brew install gh (macOS) or see https://cli.github.com/")


def ensure_release(tag: str, title: str, notes: str) -> None:
    check_release = subprocess.run(
        ["gh", "release", "view", tag],
        capture_output=True, text=True
    )
    if check_release.returncode != 0:
        print(f"Creating GitHub Release '{tag}'...", flush=True)
        subprocess.run(
            ["gh", "release", "create", tag,
             "--title", title,
             "--notes", notes],
            check=True
        )


def upload_tests_audio(tag: str = "audio", test_id: str | None = None) -> None:
    ensure_gh_cli()
    ensure_release(
        tag=tag,
        title="JLPT N2 Listening Audio (聴解.mp3)",
        notes="Audio files for JLPT N2 mock exams and imported papers."
    )

    available_dirs = [d for d in sorted(TESTS.iterdir()) if d.is_dir() and (d / "聴解.mp3").is_file()]
    if not available_dirs:
        print(f"No tests with 聴解.mp3 found under {TESTS}.", flush=True)
        return

    if test_id and test_id.lower() != "all":
        matched = [d for d in available_dirs if d.name == test_id]
        if not matched:
            print(f"Warning: No test folder matches '{test_id}'.", flush=True)
            print("Available test IDs with 聴解.mp3:", flush=True)
            for d in available_dirs:
                print(f"  - {d.name}", flush=True)
            sys.exit(1)
        target_dirs = matched
    else:
        target_dirs = available_dirs

    with tempfile.TemporaryDirectory() as tmpdir:
        staged_files = []
        for d in target_dirs:
            mp3 = d / "聴解.mp3"
            staged = Path(tmpdir) / f"{d.name}.mp3"
            try:
                os.link(mp3, staged)
            except OSError:
                shutil.copy2(mp3, staged)
            staged_files.append(staged)

        print(f"\n[1/1] Uploading {len(staged_files)} test audio file(s) to release '{tag}'...", flush=True)
        for sf in staged_files:
            print(f"  -> Uploading {sf.name} ({sf.stat().st_size / 1e6:.1f} MB)...", flush=True)
            subprocess.run(
                ["gh", "release", "upload", tag, str(sf), "--clobber"],
                check=True
            )

    print(f"✓ Successfully uploaded {len(target_dirs)} test audio file(s) to GitHub Release '{tag}'.", flush=True)


def upload_refs_files(kind: str = "audio", tag: str | None = None) -> None:
    ensure_gh_cli()
    if not REFS.is_dir():
        print(f"No refs directory found at {REFS}.", flush=True)
        return

    ext = ".mp3" if kind == "audio" else ".pdf"
    default_tag = "refs-audio" if kind == "audio" else "refs-pdf"
    release_tag = tag or default_tag
    title = f"JLPT N2 Reference {'Audio Archive' if kind == 'audio' else 'PDF Archive'} (refs/)"
    notes = f"Reference {ext.upper()} files from official past exams and textbooks."

    ensure_release(tag=release_tag, title=title, notes=notes)

    files = sorted(REFS.rglob(f"*{ext}"))
    if not files:
        print(f"No *{ext} files found under {REFS}.", flush=True)
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        staged_files = []
        for f in files:
            rel = f.relative_to(REFS)
            safe_name = str(rel).replace("/", "__").replace(" ", "_")
            staged = Path(tmpdir) / safe_name
            try:
                os.link(f, staged)
            except OSError:
                shutil.copy2(f, staged)
            staged_files.append((f, staged))

        print(f"\nUploading {len(staged_files)} refs {ext} file(s) to release '{release_tag}'...", flush=True)
        for orig, sf in staged_files:
            print(f"  -> Uploading {orig.name} ({sf.stat().st_size / 1e6:.1f} MB) as {sf.name}...", flush=True)
            subprocess.run(
                ["gh", "release", "upload", release_tag, str(sf), "--clobber"],
                check=True
            )

    print(f"✓ Successfully uploaded {len(files)} refs {ext} file(s) to GitHub Release '{release_tag}'.", flush=True)


def main():
    ap = argparse.ArgumentParser(description="Upload tests audio and refs files (.mp3, .pdf) to GitHub Releases.")
    ap.add_argument("target", nargs="?", default="tests",
                    choices=["tests", "refs-audio", "refs-pdf", "all"],
                    help="What to upload: 'tests' (mock tests MP3), 'refs-audio', 'refs-pdf', or 'all' (default: tests)")
    ap.add_argument("test_id", nargs="?", default=None,
                    help="Specific test id when target is 'tests' (default: all tests)")
    ap.add_argument("--tag", default=None,
                    help="Override release tag")
    args = ap.parse_args()

    if args.target == "tests":
        upload_tests_audio(tag=args.tag or "audio", test_id=args.test_id)
    elif args.target == "refs-audio":
        upload_refs_files(kind="audio", tag=args.tag or "refs-audio")
    elif args.target == "refs-pdf":
        upload_refs_files(kind="pdf", tag=args.tag or "refs-pdf")
    elif args.target == "all":
        upload_tests_audio(tag=args.tag or "audio")
        upload_refs_files(kind="audio", tag="refs-audio")
        upload_refs_files(kind="pdf", tag="refs-pdf")


if __name__ == "__main__":
    main()
