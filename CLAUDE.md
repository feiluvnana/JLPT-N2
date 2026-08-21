# CLAUDE.md

Workspace guidelines for this repository live in `AGENTS.md`, which is shared
by every agent harness. It is imported below, so its rules apply in full here —
**start with `AGENTS.md` §0**, the read-everything-first compliance rule.

@AGENTS.md

## Claude-Code-specific notes

- The 9 skills in `.agents/<skill_name>/SKILL.md` are also exposed as native
  Claude Code skills through symlinks in `.claude/skills/`, invocable as
  `/<skill-name>`. Both paths are the same files — edit `.agents/`, never a
  copy.
- Scripts run from the workspace root; prefer the `make` targets in
  `AGENTS.md` §4. `make serve` takes no test id — one server covers every
  test.
- **Run `make check` before you report any pipeline change as done**, and read
  every line of its output (AGENTS.md §4).
