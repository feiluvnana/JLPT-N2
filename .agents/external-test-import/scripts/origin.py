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
