#!/usr/bin/env python3
"""Build the STATIC deployment of the exam app — the GitHub Pages version.

    python3 .agents/exam-app/scripts/build_pages.py
    # or: make pages          (preview it with: make preview-pages)

`make serve` and GitHub Pages are the same three screens; only the storage
differs. There is no server on Pages to POST to and no disk to write, so the
sheets are rebuilt with `--storage local` and the answers and results live in
the browser's localStorage under keys that spell out the very files they stand
in for — local_store.py owns that key schema and is the only place it is
written down.

Everything else is shared, not copied: the test list is `index_view.py` (the
same cards `make serve` renders, fed from localStorage instead of `/api/tests`),
and the sheets come from `build_interactive.build()`.

Output tree (default `_site/`, gitignored — CI builds it, nothing commits it):

    _site/.nojekyll                    Pages must not run Jekyll over this
    _site/index.html                   screen 1, with the deployed-tests manifest
    _site/tests/<id>/解答.html         screens 2 and 3, storage=local
    _site/tests/<id>/聴解.mp3          the audio the player streams

Nothing under `tests/` on disk is written or modified.
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TESTS = ROOT / "tests"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_interactive  # noqa: E402
import index_view         # noqa: E402
import serve_sheet        # noqa: E402

MARKER = ".nojekyll"      # also our "this directory is a build output" flag
AUDIO = "聴解.mp3"


def deployable(test_id: str | None = None) -> list[Path]:
    """Test folders that can be built into the site, in the list's own order."""
    if not TESTS.is_dir():
        return []
    dirs = [d for d in TESTS.iterdir()
            if d.is_dir() and (d / "言語知識・読解.md").is_file()
            and (d / "聴解.md").is_file()]
    if test_id:
        dirs = [d for d in dirs if d.name == test_id]
    return sorted(dirs, key=lambda p: serve_sheet.natural_key(p.name))


def prepare_out(out: Path, force: bool) -> None:
    """Make `out` an empty build directory, refusing to eat anything else.

    A stale sheet from a deleted test would otherwise stay deployed, so the
    directory is emptied — but only when it is recognisably one of ours (it has
    the .nojekyll marker) or it is empty. Anything else needs --force, because
    `--out docs` pointed at a real folder must not silently delete it.
    """
    if out.exists():
        if not out.is_dir():
            sys.exit(f"--out {out} exists and is not a directory")
        entries = list(out.iterdir())
        if entries and not (out / MARKER).exists() and not force:
            sys.exit(f"{out} is not empty and was not built by this script "
                     f"(no {MARKER}). Pass --force to overwrite it, or pick "
                     f"another --out.")
        for p in entries:
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    out.mkdir(parents=True, exist_ok=True)
    (out / MARKER).write_text("", encoding="utf-8")


def copy_audio(src: Path, dst: Path) -> int:
    """Copy the ~30 MB MP3, skipping it when the destination is already it."""
    if dst.is_file() and dst.stat().st_size == src.stat().st_size \
            and dst.stat().st_mtime >= src.stat().st_mtime:
        return 0
    shutil.copy2(src, dst)
    return src.stat().st_size


def build_site(out: Path, test_id: str | None = None, with_audio: bool = True,
               force: bool = False) -> list[dict]:
    dirs = deployable(test_id)
    if not dirs:
        sys.exit(f"no deployable tests in {TESTS}"
                 + (f" matching {test_id!r}" if test_id else "")
                 + " (each needs 言語知識・読解.md and 聴解.md)")

    prepare_out(out, force)
    manifest, copied = [], 0
    for d in dirs:
        dest = out / "tests" / d.name
        # The sheet is REBUILT, never copied from tests/<id>/: that one is the
        # server build and would POST to an /api/ that does not exist on Pages.
        build_interactive.build(d, storage="local", out_dir=dest)

        mp3 = d / AUDIO
        has_audio = mp3.is_file()
        if has_audio and with_audio:
            copied += copy_audio(mp3, dest / AUDIO)
        elif has_audio:
            print(f"  ! {d.name}: --no-audio, 聴解.mp3 not deployed")
        else:
            print(f"  ! {d.name}: no 聴解.mp3 (run make mp3 {d.name})")

        # The static half of what the list needs; the progress half comes from
        # localStorage in the page. Same field names as serve_sheet.progress_of.
        manifest.append({
            "id": d.name,
            "origin": serve_sheet.test_origin(d.name),
            "has_sheet": True,
            "has_audio": has_audio and with_audio,
        })

    (out / "index.html").write_text(index_view.index_html("local", manifest),
                                    encoding="utf-8")
    print(f"  {out / 'index.html'}  ({len(manifest)} test(s) listed)")
    if copied:
        print(f"  copied {copied / 1e6:.0f} MB of audio")
    return manifest


def main():
    ap = argparse.ArgumentParser(
        description="Build the static GitHub Pages deployment of the exam app.")
    ap.add_argument("test_id", nargs="?", default=None,
                    help="deploy only this test (default: every test in tests/)")
    ap.add_argument("--out", type=Path, default=ROOT / "_site",
                    help="output directory (default: _site/)")
    ap.add_argument("--no-audio", action="store_true",
                    help="skip the 聴解.mp3 copies (fast rebuilds; player will 404)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite --out even if this script did not create it")
    args = ap.parse_args()

    tests = build_site(args.out, test_id=args.test_id,
                       with_audio=not args.no_audio, force=args.force)
    size = sum(f.stat().st_size for f in args.out.rglob("*") if f.is_file())
    print(f"\nStatic site: {args.out}  ({len(tests)} test(s), {size / 1e6:.0f} MB)")
    print("Answers and results are stored in the browser (localStorage), not on disk.")
    print(f"Preview: python3 -m http.server -d {args.out} 8766   # or: make preview-pages")


if __name__ == "__main__":
    main()
