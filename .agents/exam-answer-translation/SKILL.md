---
name: exam-answer-translation
description: Single owner of shipping the model answer (模範解答.html) in languages beside Japanese — the per-language explanation file 詳細解説.<lang>.json, its scaffold/merge tooling, the shared UI label set, and the in-page language switcher contract. Use whenever a test's model answer must be readable in the learner's own language, whenever a translation is added, refreshed after an explanation edit, or reported missing/stale, and whenever a new target language is introduced. This skill never picks the language — GENERATE.md declares which languages a paper ships with.
---

# Model-Answer Translation (詳細解説の多言語化)

`exam-model-answer` owns the Japanese explanations and the page that renders
them. This skill owns everything that makes that same page readable in another
language, and nothing else.

**This skill is language-agnostic on purpose.** It never names a target
language, never assumes one, and never hard-codes label text for one. The
language list for a paper is declared in `GENERATE.md` (imports point at the
same list). Every command below takes the code as an argument.

---

## What a translation is — and what it must never touch

The exam's own wording is fidelity-locked. `詳細解説.json`'s `stem`,
`options`, `passage`, and `script` are copies of `言語知識・読解.md`,
`聴解.md`, and `聴解スクリプト.txt`, verified by
`exam-model-answer`'s `verify_fidelity.py` and by `make check`. A translation
therefore **adds a second reading of the explanation, it never replaces the
Japanese question**:

| Element | In the translated view |
| --- | --- |
| Stem, options, section banners | Japanese only, always visible, furigana intact |
| 読解 passage / 聴解 script | Japanese box stays; the translation renders **below it**, never in place of it |
| `why_correct`, `options_analysis`, `points` | swapped for the translation |
| UI labels (tabs, headings, badges) | swapped for the translation |

Translating a stem or an option into the Japanese slot is a defect, not a
feature — the learner is being tested on that wording.

## Writing quality — same bar as the Japanese

- **Translate the explanation, keep the Japanese object.** The tested word,
  the grammar pattern, and any quoted line stay in Japanese inside the
  translated sentence (`「代理」 đọc là「だいり」…`). Stripping them leaves an
  explanation the learner cannot map back onto the question.
- **Plain, short sentences**, matching the Japanese source's register: it is
  written for a learner, not for a linguist. Do not add content the Japanese
  does not have, and do not summarise away content it does have — one source
  sentence, one translated sentence.
- **Every option keeps its verdict.** `options_analysis[i]` must argue the
  same way round as its source; exactly one is the correct option. Reordering
  or merging entries breaks the `[正解]`/`[不正解]` tagging, which is applied
  by position.
- **No furigana markup in the translation.** `《…》` belongs to the Japanese
  text. Japanese quoted *inside* a translated sentence may carry it and will
  render as `<ruby>`.
- Emoji-free, no pipeline metadata, same as the Japanese explanations.

## Workflow

```bash
make scaffold-translation <id> TLANG=<code> TLABEL="<native name>"
#   -> tests/<id>/_translation/<code>/meta.json + chunk-NN.json work packets
#   -> .agents/exam-answer-translation/ui/<code>.json  (created on first use)

#   write one chunk-NN.target.json per packet, and translate ui/<code>.json once

make merge-translation <id> TLANG=<code>
#   -> validates, then writes tests/<id>/詳細解説.<code>.json

make model-answer <id>
#   -> rebuilds 模範解答.html with the language switcher
```

`TLANG`/`TLABEL`, not `LANG`/`LABEL`: `make LANG=vi` would also overwrite the
shell's locale for every command the recipe shells out to.

### The work packets

`scaffold_translation.py` splits the items into packets of 20 (`--chunk-size`)
so the work parallelises across contexts. **A packet is read-only**: the
translator writes the sibling `chunk-NN.target.json`, holding nothing but the
translations —

```json
{"shared": {"p3": "…"},
 "items": {"57": {"why_correct": "…", "options_analysis": ["…"], "points": ["…"]}}}
```

— with every ref, every item key of that packet, and arrays exactly as long as
their source counterpart. Keeping the Japanese out of the output is what stops
a 40k-character rewrite from arriving truncated. `stem`/`options` ride along in
the packet as reference context and are not translated.

Do not prefix an `options_analysis` entry with `[正解]`/`[不正解]` or a
translated equivalent: the page tags each option by index against the official
key, and a hand-typed tag would print twice — and could contradict the key.

Reading passages and listening scripts are **deduplicated into the packet's
`shared` block**: 問題11 spends one passage over three items, so it is
translated once and `merge_translation.py` expands it back onto every item
that referenced it. Two different translations of one passage is the defect
this prevents.

`tests/*/_translation/` is gitignored working state — the deliverable is
`詳細解説.<lang>.json`.

### Translator brief (one packet, one context)

The work parallelises one packet per context. Give each translator exactly this
task, substituting the packet path and the language:

> Read `.agents/exam-answer-translation/SKILL.md` end to end, then translate
> exactly one packet: `tests/<id>/_translation/<lang>/chunk-NN.json` into
> `…/chunk-NN.target.json`. Touch no other file, run no `make` target.

and hold it to the rules above plus these, which is where a packet actually
goes wrong:

1. **Every ref in `shared`, every key in `items`.** A packet with 20 items
   produces 20 item entries. `options_analysis` and `points` keep the source's
   length and order — the page tags options by index.
2. **Nothing is summarised.** One source sentence becomes one translated
   sentence. A shortened explanation is a defect, not concision; the merge
   cannot detect it, so it ships.
3. **A 読解 passage** is translated whole, keeping its paragraph breaks, its
   `（注1）` note lines, and any markdown table's pipe structure.
   **A 聴解 script** keeps its speaker labels (`男:`, `女:`, `店員:` …) and its
   line count — translate line by line.
4. **Japanese stays where the explanation points at it**: the tested word, the
   grammar pattern, and quoted lines from the passage/script remain Japanese
   inside the translated sentence. Existing `《…》` furigana may ride along; do
   not invent readings that are not already in the source.
5. Valid JSON, UTF-8, no `[正解]`-style tags, no emoji, no pipeline metadata.
6. Verify before reporting:
   `python3 -c "import json;d=json.load(open(PATH));print(len(d['items']),len(d['shared']))"`

### The merge is the gate

`merge_translation.py` refuses to write while a `.target.json` is missing or
unparseable, any target is empty, any array is the wrong length, any item is
missing or unknown to its packet, any target is a verbatim paste of its
Japanese source, the UI file is missing or still template Japanese, or
`詳細解説.json` has changed since the packets were scaffolded (digest
mismatch — the explanations moved underneath the translation). Read its
docstring; every refusal names the item.

### UI labels

One file per language, `.agents/exam-answer-translation/ui/<lang>.json`,
cloned from `_template.json` (whose values are the Japanese originals the
builder falls back to). It is shared by every test, so labels cannot drift
between papers; `merge_translation.py` copies it into each
`詳細解説.<lang>.json` under `_meta.ui`. Keep `{n}` in `question_label`.

## Deliverable & page contract

| Deliverable | File Name | Written by |
| --- | --- | --- |
| Per-language explanations | `詳細解説.<lang>.json` | `merge_translation.py` |
| Model answer page (all languages in one file) | `模範解答.html` | `build_model_answer.py` (`exam-model-answer`) |

`build_model_answer.py` discovers `詳細解説.*.json` by glob — no language is
named in the builder either. With no translation file present it emits exactly
the Japanese-only page it always did. With one or more present it adds a
header switcher (日本語 + one button per `_meta.label`), remembers the choice
in `localStorage`, and renders every explanation pane once per language with
`data-lang`, so a single self-contained HTML file serves every language
offline.

## Ordering rule

Translation runs **after** `模範解答.html`'s inputs are frozen — i.e. after
`QA: PASS` for a generated paper, after key reconciliation for an import, on
the same `詳細解説.json` the Japanese page was built from. A translation made
from a pre-QA draft describes a paper that no longer exists; the digest check
in the merge is what catches it.

When a QA fix later edits an explanation, re-scaffold (`--force`), re-translate
the affected items, re-merge, and rebuild. `make check` fails a
`詳細解説.<lang>.json` whose digest no longer matches `詳細解説.json`, and
fails a `模範解答.html` that is missing a language present on disk.
