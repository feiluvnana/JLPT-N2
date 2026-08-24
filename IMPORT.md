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

The pipeline is three steps and nothing else:

1. **Source → the test itself.** Transcribe the booklet/script/audio into the
   repo's deliverables. Fidelity over invention: never "improve" an item,
   never swap a key, keep the source's apparatus (（注N）, （中略）, setting
   labels, printed URLs), and prefer copying the original MP3 over
   synthesizing one.
2. **Check the content by hand.** Diff all 101 keys against the official
   answer sheet (the sheet wins), check coverage in both directions, and
   repair what the source's own print/OCR got plainly wrong — only where the
   correction is determined by the surrounding text or the key. Leave anything
   you would have to guess as printed and flag it. Rasterize the page before
   trusting any doubtful line. Finish with `make booklet`, `make sheet` and
   `make check` (read every line, WARN included). No `exam-qa-review` pass.
3. **Model answer, last.** Once the content is settled and the gate is green:
   author `詳細解説.json` (`exam-model-answer`), then run
   `make model-answer imported-⟨slug⟩`. Japanese only — the per-language
   pipeline was retired 2026-08-21.

Binding points, from those two files:

- This is an **import, not a generation**: the folder id must start with
  `imported-`, and you must never run `sample_items.py` or touch
  `logs/ledger.json` for it.
- **Commit** `tests/imported-⟨slug⟩/` when done.
- **Final report** per `AGENTS.md` §0.7: which skills you read, which steps you
  ran, how the 101 keys reconciled, every repair you made to the source's own
  text, every doubtful line you left as printed, and anything you skipped.
