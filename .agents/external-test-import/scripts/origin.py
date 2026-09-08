"""Shared origin flag for test folder names.

imported  → folder name starts with ``imported-``
generated → everything else (no flag)
"""

from __future__ import annotations

IMPORTED_PREFIX = "imported-"
SLUG_RE = __import__("re").compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def test_origin(test_id: str) -> str:
    """Return ``imported`` or ``generated`` from a tests/ folder name."""
    return "imported" if test_id.startswith(IMPORTED_PREFIX) else "generated"


def is_imported(test_id: str) -> bool:
    return test_origin(test_id) == "imported"


def imported_id(slug: str) -> str:
    """Build ``imported-<slug>`` or raise ValueError."""
    slug = slug.strip()
    if slug.startswith(IMPORTED_PREFIX):
        slug = slug[len(IMPORTED_PREFIX):]
    if not slug or not SLUG_RE.match(slug):
        raise ValueError(
            f"invalid slug {slug!r}: use lowercase letters, digits, hyphens "
            f"(e.g. n2-2025-12)"
        )
    return f"{IMPORTED_PREFIX}{slug}"


def choukai_origin(test_dir) -> str:
    """Return ``imported``, ``composed`` or ``tts`` for a test's listening half.

    Orthogonal to :func:`test_origin`: since 2026-09-08 a *generated* paper's
    聴解 is composed from official clips (`tools/compose_choukai.py`) rather
    than synthesized by Edge-TTS, so the folder name no longer says how the
    audio was made. `聴解_チャプター.json`'s ``source`` field does — the composer
    stamps ``composed`` there, `make_choukai_mp3.py` writes segment marks with
    no ``source``, and an import carries the ``external`` stub.

    Takes a pathlib.Path to the test directory.
    """
    import json

    if is_imported(test_dir.name):
        return "imported"
    marks = test_dir / "聴解_チャプター.json"
    if marks.is_file():
        try:
            if json.loads(marks.read_text(encoding="utf-8")).get(
                    "source") == "composed":
                return "composed"
        except (ValueError, OSError):
            pass
    return "tts"
