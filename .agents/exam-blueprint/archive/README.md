# Archived pool-growth tooling

These five scripts grow `references/pools.json` (classification, staging,
promotion, OpenJLPT expansion). Pool growth is paused, so they are parked here
and have no Makefile targets. They import `level_data.py` as a sibling —
**move a script back into `../scripts/` to run it** (`git mv`, then invoke it
directly). Restore them if the sampler starts reporting exhausted categories.
