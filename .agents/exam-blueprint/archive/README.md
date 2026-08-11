# Archived pool-growth tooling

`promote_adjunct.py` grows `references/pools.json` by promoting approved
`logs/adjunct_staging.json` rows. Pool growth is paused, so it is parked here
and has no Makefile target. It imports `level_data.py` as a sibling —
**move it back into `../scripts/` to run it** (`git mv`, then invoke it
directly).

**2026-08-11: `classify_level.py`, `expand_pools.py`, `suggest_pool_additions.py`,
and `fetch_openjlpt.py` were deleted, not just archived.** All four existed
solely to classify/fetch/expand `pools.json` against the vendored OpenJLPT
N1–N3 JSON slices (`references/openjlpt/`), which is itself deleted —
exam-blueprint's pool authority is now Shin Kanzen Master (`refs/Shinkanzen/`)
and 日本語総まとめ N2 (`refs/Soumatome/`) exclusively (see exam-blueprint/SKILL.md).
Both are scanned PDFs with no text layer, so there is no scripted equivalent of
the old classify/expand pipeline — growing a pool now means an author reading
the relevant Shinkanzen/Soumatome pages (or the official archive) and hand-adding
entries, the same way `promote_adjunct.py`'s staging rows are already authored
by hand before promotion. If pool growth resumes at volume, a fresh script
would need a new OCR-based extraction of those PDFs (see the Vision OCR
pipeline `tools/vision_ocr.swift` used for `refs/JLPT_N2_NEW/`) — no such
extraction exists yet.
