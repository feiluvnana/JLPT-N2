# IMPORT.md — the prompt for importing an external test

Copy everything below the line to the agent, filling in the ⟨⟩ placeholders.
The **slug** is lowercase letters/digits/hyphens (e.g. `n2-2025-12`); the
folder will be `tests/imported-⟨slug⟩/`. The script PDF and MP3 are optional —
delete those lines if you don't have them.

---

Import an external JLPT exam into this repository as `tests/imported-⟨slug⟩/`.

Source files:
- Booklet PDF: `⟨path/to/booklet.pdf⟩`
- Listening script PDF (optional): `⟨path/to/script.pdf⟩`
- Listening audio MP3 (optional): `⟨path/to/audio.mp3⟩`

Before your first tool call, read `AGENTS.md` end to end, then read
`.agents/external-test-import/SKILL.md` end to end — it owns the whole import
workflow and this prompt does not override any of it.

Binding points, all from those two files:

1. This is an **import, not a generation**: the folder id must start with
   `imported-`, and you must never run `sample_items.py` or touch
   `logs/ledger.json` for it.
2. **Fidelity over invention**: author the Markdown deliverables from the PDF
   extracts, reconcile all 101 answer keys against the source's answer sheet
   (the answer sheet wins), and prefer copying the original MP3 over
   synthesizing one.
3. Finish with `make booklet`, `make sheet`, and `make check` (read every
   line, including WARN), then the fidelity QA pass the skill prescribes.
4. **Model answer (FINAL STEP)**, once all 101 keys are reconciled and the
   gate is green: author `詳細解説.json` (`exam-model-answer`), then run
   `make model-answer imported-⟨slug⟩` last. Japanese only — the per-language
   pipeline was retired 2026-08-21.
5. **Commit** `tests/imported-⟨slug⟩/` when done.
6. **Final report** per `AGENTS.md` §0.7: which skills you read, which steps
   you ran, how the 101 keys reconciled (and any the extract disagreed on),
   and anything you skipped and why.
