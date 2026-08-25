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
   correction is determined by the surrounding text or the key.
   When a line will not resolve, climb the ladder and stop at the first rung
   that settles it: re-read the extract in context → cross-check the same fact
   elsewhere in the source → **rasterize the page and read the image
   yourself**. That last rung is slow and expensive, so spend it only on
   decisive lines (問題5 統合理解, near-synonym options, anything the official
   key depends on) — crop to the line at high dpi rather than re-reading whole
   pages. A line may be left as printed only after you have actually looked at
   the ink; say which page you verified it on. Finish with `make booklet`,
   `make sheet` and `make check` (read every line, WARN included). No
   `exam-qa-review` pass.
3. **Model answer, last.** Once the content is settled and the gate is green:
   author `詳細解説.json` (Japanese), then `詳細解説.vi.json` (Vietnamese) **in a
   separate context** — the two sets are written from the items, never
   translated from each other, and both stay inside `exam-model-answer`'s
   terseness bands. Then run `make model-answer imported-⟨slug⟩`.
   **Solve each item from the source before you explain it, and confirm the
   official key.** Derive the answer first, then compare with the key, then
   write — an explanation written backwards from the key will justify a wrong
   key just as fluently as a right one. If your solve disagrees, re-read, then
   climb the ladder on the deciding line; if it still disagrees, the source
   wins (never re-key an official item) and you report the disagreement.

Binding points, from those two files:

- This is an **import, not a generation**: the folder id must start with
  `imported-`, and you must never run `sample_items.py` or touch
  `logs/ledger.json` for it.
- **Commit** `tests/imported-⟨slug⟩/` when done.
- **Final report** per `AGENTS.md` §0.7: which skills you read, which steps you
  ran, how the 101 keys reconciled, every repair you made to the source's own
  text, every doubtful line you left as printed, and anything you skipped.
