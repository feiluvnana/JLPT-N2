# CLAUDE.md

Workspace guidelines for this repository live in `AGENTS.md`, which is shared by
every agent harness. It is imported below, so its rules apply in full here.

@AGENTS.md

## Claude-Code-specific notes

- The 12 skills in `.agents/<skill_name>/SKILL.md` are also exposed as native
  Claude Code skills through symlinks in `.claude/skills/`, so they appear in
  the skills list and can be invoked as `/<skill-name>`. Both paths are the same
  files — edit `.agents/<skill_name>/SKILL.md`, never the symlink target's copy.
- `jlpt-test-generation` is the entry point: invoke or read it first for any
  exam work, even a partial request like "make a listening section".
- Scripts always run from the workspace root; prefer the `make` targets
  documented in `AGENTS.md` §4 (`make sheet 1`, `make serve 1`, `make grade 1`).
- **Run `make check` before you report any pipeline change as done.** It is the
  read-only gate that catches docs drifting from the scripts and malformed
  answer sheets; see `AGENTS.md` §4.
- `tests/` and `logs/` are tracked working folders. A new exam means new files
  under `tests/<test_id>/` plus an updated `logs/ledger.json`; commit them
  together.
