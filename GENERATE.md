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
   from memory or design one. There is no web harvest step — every 読解
   passage and 聴解 dialogue is written directly from its sampled
   `reading_topics`/`listening_scenarios` entry (`exam-blueprint` Part II).
3. **Gate and QA are both mandatory**: `make check` with every line read
   (including WARN), the whole-paper one-topic-one-surface table, then
   `exam-qa-review` with fresh eyes, looping fix → fresh re-review until
   `QA: PASS`. Apply or explicitly reject every entry in QA's root-cause
   table.
4. **Model answer (FINAL STEP)**: After `QA: PASS`, and only then, build the
   explanation deliverable — all questions and keys must be locked first.
   a. Author `tests/⟨test_id⟩/詳細解説.json` (Japanese) — it also owns the exam
      wording both panes print.
   b. Author `tests/⟨test_id⟩/詳細解説.vi.json` (Vietnamese) **in a separate
      context from (a)**. The two sets are WRITTEN, not translated: a context
      still holding the Japanese explanations reproduces their sentences and
      their framing without ever deciding to. One subagent per language, each
      reading the paper rather than the other's file.
   c. Both sets must sit inside `exam-model-answer`'s terseness bands — the gate
      FAILs a field over the cap, and cutting to band never means replacing a
      concrete reason with a generic one.
   d. Run `make model-answer ⟨test_id⟩` LAST.
5. **Commit** `tests/⟨test_id⟩/` and the updated `logs/` together when done.
6. **Final report** per `AGENTS.md` §0.7: which skills you read, which stages
   you ran, the seed you used, every WARN you resolved or justified, and
   anything you skipped and why.
