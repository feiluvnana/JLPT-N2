# GENERATE.md — the prompt for generating a new mock test

Copy everything below the line to the agent, filling in the ⟨⟩ placeholder.
Pick a **test id** that does not exist under `tests/` (no `imported-` prefix).
You do not supply a seed — the agent must obtain one from an RNG.

---

Generate a complete JLPT N2 mock exam as test `⟨test_id⟩` in this repository.

Before your first tool call, read `AGENTS.md` end to end, then read
`.agents/jlpt-test-generation/SKILL.md` end to end — it owns the whole
workflow (the 4-stage pipeline, the per-stage reading map, and the subagent
prompt template) and this prompt does not override any of it.

Binding points, all from those two files:

1. **Orchestrate, don't work.** Run the 4 stages as subagents — blueprint;
   the 4 authoring sections in parallel; build+gate; QA — each reading exactly
   its reading-map row from disk. Do none of the content work in your own
   context. If your harness has no subagents, use the documented fallback,
   whose one non-negotiable split is authoring vs QA in different contexts.
2. **Use exactly the id `⟨test_id⟩`, and obtain the seed from an RNG** — run
   `python3 -c "import secrets; print(secrets.randbelow(10**8))"` (or a
   platform equivalent) and use the printed value verbatim; never type a seed
   from memory or design one. Re-harvest `logs/seeds.json` fresh for this
   test (skip the web blend only if you have no web access, and say so), and
   verify the blend report before authoring.
3. **Gate and QA are both mandatory**: `make check` with every line read
   (including WARN), the whole-paper one-topic-one-surface table, then
   `exam-qa-review` with fresh eyes, looping fix → fresh re-review until
   `QA: PASS`. Apply or explicitly reject every entry in QA's root-cause
   table.
4. **Commit** `tests/⟨test_id⟩/` and the updated `logs/` together when done.
5. **Final report** per `AGENTS.md` §0.7: which skills you read, which stages
   you ran, the seed and harvest you used, every WARN you resolved or
   justified, and anything you skipped and why.
