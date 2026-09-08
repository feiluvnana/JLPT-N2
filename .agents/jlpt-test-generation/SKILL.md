---
name: jlpt-test-generation
description: End-to-end workflow for generating a complete JLPT mock exam (N1-N5, primarily N2). Use this skill whenever the user asks to create, generate, or build a JLPT test, mock exam, 模擬試験, practice test, or any subset of one (言語知識, 文字・語彙, 文法, 読解, 聴解/choukai), or asks to regenerate/fix exam deliverables. This is the entry-point skill for generation — it owns the 5-stage pass structure and the per-stage reading map, and routes to the specialized skills. Consult it FIRST before any generated exam work, even for partial requests like "make a listening section" or "create N2 grammar questions". For importing an external PDF/past paper, use external-test-import instead.
---

# JLPT Test Generation (Orchestrator)

**Importing an existing exam** (PDF, past paper, script, MP3) → stop and read
`external-test-import/SKILL.md`; those live in `tests/imported-<slug>/`. This
file is for **generating** new mocks only.

**Read this file to the end before your first tool call.** `AGENTS.md` §0 is
the compliance rule and says what to report at the end; §2–3 own layout,
deliverable filenames, and `refs/` paths.

## The 5-stage pipeline

**Orchestrate, don't work.** The context owning the request spawns subagents and
does no content work itself. State flows between stages **through files on disk
only** — an orchestrator paraphrasing content into a prompt is the "memory of
what I meant" that shipped every historical mis-key.

Two context-isolation rules, non-negotiable in any harness: **(a) no long
single-run authoring** — defects cluster in whatever one context writes last;
**(b) QA is a context that authored nothing** — an author cannot audit its own
intent.

| Stage | Job | Contexts |
|-------|-----|----------|
| 1. Blueprint | Sample the item pools; draw a THEME per themed surface | 1 |
| 2. Author | 文字・語彙 (問1–6) ǀ 文法 (問7–9) ǀ 読解 (問10–14) | **3, in parallel** |
| 3. Build + gate | **Compose 聴解** (`make mp3 <id> SEED=<rng>`), booklet HTML, 解答.html, `make check`, whole-paper topic table | 1 |
| 4. QA | `exam-qa-review` in full — blind-solve, all 101 items, root-cause table | 1 **fresh** |
| 5. Model answer | `詳細解説.json` (JA) + `詳細解説.vi.json` (VI) → `make model-answer` | **2, one per language**, no shared context |

**The fix loop.** Every QA finding costs a fix + a fresh-eyes re-review of the
touched items. **Exception:** a round returning FAIL with ≤3 findings may be
fixed directly, with the same rigor (root-cause, `make check`, read the diff),
stated in the final report. Capped at **2 fresh-eyes rounds**; if round 2 still
FAILs, apply its findings directly and say explicitly which were fixed without
independent re-verification. PASS closes the *paper*, not the *generator* — an
open row in QA's root-cause table blocks the next run until applied or rejected
with a reason.

**`make sample <next>` may not run while any test's QA is open** — not while a
round is being written, not while findings are being applied. It writes
`logs/ledger.json`, the file the open review is auditing, and doing so reds
`make check` for every finished paper on disk. (`20260818_1` was sampled at
11:31 during round 3 of `20260817_3` and did exactly that — R3-6.)

**No subagents available:** approximate with new sessions, one stage each,
handing off through disk. The split that survives every fallback is
**authoring vs QA**.

## Per-stage reading map

Each subagent reads exactly these, from disk, at the start of its stage — never
the orchestrator's summary — and nothing else:

| Stage | Reads | Writes |
|-------|-------|--------|
| 1 Blueprint | `exam-blueprint/SKILL.md` | `tests/<id>/test_spec.json`, `logs/ledger.json` |
| 2 文字・語彙 | `test_spec.json` + `question-authoring/SKILL.md` + `references/moji-goi.md` + `jlpt-exam-structure/SKILL.md` | 問1–6 fragment |
| 2 文法 | same, with `references/bunpou.md` | 問7–9 fragment |
| 2 読解 | same, with `references/dokkai.md` | 問10–14 fragment |
| 3 Build+gate | `exam-app/SKILL.md`, `choukai-audio/SKILL.md` (**Part 0**), this file's topic-table § | merged `言語知識・読解.md`, the whole 聴解 half, HTML/MP3, `logs/topics.json` row, gate report |
| 4 QA | `exam-qa-review/SKILL.md` | `qa/qa-report-<id>.md` |
| 5 Model answer | `exam-model-answer/SKILL.md` | `詳細解説.json`, `詳細解説.vi.json`, `模範解答.html` |

Stage-2 authors write fragments to `tests/<id>/_sections/<問題range>.md`: booklet
body, then key/解説 rows under a literal `<!-- KEY -->` marker. Stage 3 merges
mechanically — bodies in booklet order, then ONE key heading at the end followed
by key tables in the same order. The sheet builder's `strip_key()` truncates at
that heading, so **a fragment must never carry its own**. Parallel authors never
share a file. **There is no 聴解 author**: stage 3 composes the listening half
from official clips, and a composed paper carries no セクション構成表 because
nobody chose its items' 場面, 決め手 or 質問型 — the archive did.

### Subagent prompt template

> Read, in full, from disk: [stage's reading-map row]. Your inputs are [files];
> your only outputs are [files]. Author ONLY what `tests/<id>/test_spec.json`
> prescribes — items, topics and `answer_positions` are the contract; do not
> substitute, and treat every `origin` field as binding. Report at the end: what
> you read, what you ran, what you wrote, and anything you skipped and why.
>
> (読解 only) Your assigned closing-move shape per surface is: [surface → shape].

## Stage 1 — blueprint

```bash
make sample <id> SEED=<n>          # -> test_spec.json + ledger
```

- **The seed is an RNG output, never a number you write down.** Run
  `python3 -c "import secrets; print(secrets.randbelow(10**8))"` and use it
  verbatim — agent-"picked" seeds are date-shaped and collide across sessions.
  Must be unused (`logs/ledger.json`).
- No harvest step. Each themed surface gets `{theme, origin:"authored",
  avoid:[…]}`; the author invents the subject (`exam-blueprint` Part II).
- Do not run while another test's QA is open (above).

## Stage 2 — authoring

Construction rules: `question-authoring` core + the one reference file from the
reading map.

```bash
make scaffold-sections <id>
```

- Author ONLY items in `test_spec.json`; keys go where `answer_positions` says.
- **文字・語彙 stems are quota-bound too** — 問題1/2/5 median 17 JP chars, ≥9 of
  15 comma-free, ≥7 of 25 問題1–5 stems in です・ます with ≥1 first-person and ≤2
  institution-actor, 問題4 median ≤30 and none past 44 (`moji-goi.md` Part 0).
  Fourteen papers missed all of these before they were written down.
- 問題1/2 2×2 matrices: build BY HAND against `moji-goi.md`, then check with
  `python3 tools/matrix_helper.py validate --reading <かな> <4 options>`. **The
  two generators are hard-disabled** (F4, qa-report-20260819_1).
- **Tested items are ALWAYS pool-sampled. Topics are not.** Since 2026-09-07 a
  `reading_topics`/`listening_scenarios` entry is `{theme, origin:"authored",
  avoid:[…]}` — a THEME plus every subject previous papers used under it. The
  author invents a subject not in `avoid` and not a re-wording of one, then
  writes the passage/dialogue from it (`exam-blueprint` Part II). The grammar,
  vocabulary and kanji pools are untouched by this and remain absolutely binding.
- **`avoid` is only as good as the record**, so Stage 3's `logs/topics.json` row
  is now load-bearing for the NEXT paper's draw, not just for its topic pass.
- Answer keys go at the END of each Markdown source, never inline.
- **Pre-assign each of the 13 読解/cloze surfaces a closing-move shape** from
  `dokkai.md`'s list before spawning, without exceeding its per-shape cap — four
  subagents blind to each other converge on the same "safe" default (documented
  3×). Pass each 読解 subagent its assigned shapes.

## Stage 3 — build + gate

```bash
SEED=$(python3 -c "import secrets; print(secrets.randbelow(10**8))")
make autofix <id> && make lint-draft <id> && make verify-scramble <id> \
  && make mp3 <id> SEED=$SEED \
  && make booklet <id> && make sheet <id> && make check
```

- **`make mp3` runs FIRST now and writes the entire 聴解 half** — script,
  booklet, audio, chapters and the 30 choukai `詳細解説` entries — by drawing
  official clips (`choukai-audio` Part 0). It must precede `make booklet`,
  which renders the `聴解.md` it produces.

- Run `autofix`/`lint-draft` first — contractions, reaction turns, absolute
  quantifiers, missing blanks, at zero token cost before QA.
- `make check` validates every test on disk. **Read every line, including
  WARN.** Fix failures before stage 4: a mis-keyed item is invisible once the
  MP3 is built.
- **A WARN naming this test is resolved, or recorded as deferred-to-QA WITH THE
  REASON, in writing, in `qa/` or the stage-3 report** — a WARN carried silently
  is indistinguishable from one nobody read. (Round 2 of `20260904_1` was handed
  an exit-0 gate as its entry condition while a live
  `check_goi_option_set_valence` WARN named 問題5-24 of that paper; the
  disposition existed only in the orchestrator's prompt, which no reviewer
  reads, and it turned out to be a true positive.)
- **A repair made to clear one gate check is not verified by that check
  passing.** After ANY edit to 問題10–14 prose — （注N） glosses included —
  re-grep every 問題7/8/9 keyed form across the whole 読解 half, record the counts
  AND the frames (文末／連用／連体) in the hand-off, and re-read the edited
  passage's closing move. (`20260903_1` F2: a gloss rewritten to clear a
  byte-identical-gloss FAIL planted 問題8-44's own drawn target in its own frame,
  in printed booklet text, and `make check` went green.)
- Then the **whole-paper topic pass** (below) — no script does it — and
  **append this test's row to `logs/topics.json`** (`surfaces`, `shapes`,
  `claim`, `persona`; format in `exam-blueprint` §"logs/topics.json").

## One topic, one surface (whole-paper pass, stage 3)

The failure mode that survives every automated gate: the same content on two
surfaces of one paper, or recycled from recent papers. Build ONE table — 問題9
cloze, each 問題10–13 passage, the 問題14 flyer, every 聴解 item — with a column
per test (this one and the two before), plus `theme`, `closing move` (読解), and
the DRAWN topic string. Then read it:

- **Fill the theme column from the SHIPPED surface**, not the spec draw — a
  drafted passage wanders off its tag. Apply `exam-blueprint` §"The four theme
  rules" and put the counts in your report.
- **The closing-move column is a 読解 rule** (`dokkai.md` §"Thirteen surfaces").
  Two passages on unrelated subjects both ending 「〜だけでは足りない、〜こそが要る」
  are one essay written twice; official ships that move 5–9 times per 読解 half.
- **Read each surface against its OWN draw before reading it against the
  others.** Nothing compares a shipped surface's SUBJECT to the
  `test_spec.json` string it came from, so a passage can wander off its draw with
  every line green and silently spend a cooldown. (`20260904_3` drew
  「高齢者向け軽スポーツの**普及**」 and shipped a passage arguing **定着**, which
  is `20260904_2` 問題9's subject one paper earlier — the mechanism behind
  qa-report-20260904_3 F1.) **This is a READ, not a gate, and that is measured:**
  the obvious predicate — counting drawn-topic tokens surviving into
  `logs/topics.json` — was run over all 23 papers on 2026-09-05, reports 1–6
  zero-overlap draws on *every* paper (median 3–4, because a surface legitimately
  writes 「自動で走るバス」 for 「自動運転バス」), and does not fire on the founding
  case. A predicate that flags every paper and misses its own founding case is
  refuted. So: put the drawn string in the table and say, per surface, whether
  the shipped subject is the one drawn. A surface that moved is either re-angled
  back onto its draw (no stamp) or stamped `"origin": "reauthored"` in spec AND
  ledger with a note (`exam-qa-review` §"A fix that changes WHAT a surface tests").
- **A 読解 topic and a 聴解 scenario may name one subject and no check sees it.**
  `check_surface_subjects()` matches maximal kanji runs for equality, so
  「健康保険組合からの人間ドック補助案内」 and 「人事部からの健康診断のお知らせ」 — one
  paper, one subject, both 睡眠・健康 — share nothing it can see
  (qa-report-20260904_3 F5). Read the 読解 rows and 聴解 rows as ONE list.
- **No topic appears twice in this paper**, even in a different register (a
  問題14 flyer spelling out a 聴解 item's keyed answer; one subject serving both
  問題9 and 問題10(1)).
- **The drawn `quick_response` phrases are content — give every one its own
  row** (11 in a current paper), with the setting you invented for it. They are
  the surfaces nobody thinks of as topics because nobody *chose* their subject.
  (`20260817_3` wrote a 問題9 cloze on 「何をどう書けばよいのか分からないまま紙に
  向かう心細さ」 while its own 問題4-1番 stimulus was 「この申請書の書き方がよく
  分からないのですが」.) Check them against 問題9's subject specifically — the
  cloze is the other unpooled surface.
- **Errand identity is checked HERE now.** It used to be a draw-time comparison
  of pool `key` fields; with authored scenarios there is no key, so the only
  place two items running one errand becomes visible is the `shapes` column of
  `logs/topics.json`. Read it across three papers, every time — this row is no
  longer backed up by a spec-time check.
- **No topic repeats the previous test, especially in the same 聴解 slots.** Do
  it as a table read from `logs/topics.json` (a lookup, not a re-derivation) and
  read each ROW across the columns. A shared domain in one row is a finding even
  when errand keys and theme tags differ — `20260818_1` put 自動車学校の危険予測運転
  in 問題3-4番 directly after `20260817_3`'s 問題3-4番 整備担当が運転の癖を伝える話
  (tagged 教育 and 交通, so no tag matched). `check_slot_theme_repeat()` WARNs
  only the half a tag can see (問題2/3/5 slots — 問題4's scenes are invented so its
  tags measure the tagger; 問題1's mix is quota-bound), which is why this row read
  stays mandatory. **Two repairs, and the cheap one is usually right:** RE-SLOT
  (swap two talks, re-order their spoken options so each key still lands where
  `answer_positions` says, re-derive both 解説) costs no new authoring; a reroll
  costs a fresh 220–300-char talk, four new options, and a scenario that must
  itself clear cooldown/theme/slot rules.
- **A topic/domain match in the 2-tests-back column is a minor finding** — note
  it so a domain doesn't become a crutch one skip apart.
- **聴解 rows are now a DRAW audit, not a topic audit.** The listening items are
  official and their subjects were never chosen by anyone here, so errand
  identity, 問題5 decision structure, slot-theme adjacency and 問題14-vs-聴解
  detail overlap are no longer authoring rules — nothing in the paper can be
  re-angled to fix them. What replaces them, and what this pass must still do:
  read `logs/choukai_draws.json` and confirm **no clip id repeats the previous
  paper in the same slot**. The composer already spends least-used clips first,
  so this is a verification, not a repair. If a repeat is unavoidable (the slot's
  ten candidates are exhausted), say so in the report rather than re-drawing
  forever.
- **The 読解 half still owns every topic rule above**, and a 読解 passage may now
  legitimately share a domain with a 聴解 item, because no one picked the 聴解
  item's domain. Only a shared *decisive detail* — a number or condition the
  reader could carry from one surface to the other — is still a finding.
- **問題12 (A/B) gets its own cross-test column** — one topic per paper.
- **A duplicated topic in the spec is a sampler defect**: `check_spec_blend`
  fails a repeated draw. `--reroll` the category; never hand-invent a substitute.

## Stage 4 — QA

Read `exam-qa-review/SKILL.md` in full and run it with fresh eyes. A test that
hasn't survived this pass is not done, whatever the gate says.

### Closing a finding includes re-grepping its notes

A repair is finished when **every note that narrates the finding says what is now
on disk.** After applying a fix, grep for the finding id and for the strings the
fix removed, in all four places a repair gets narrated:

1. the 構成表 / 解説 cells in `聴解.md` and `言語知識・読解.md` — a fix that adds or
   changes a script or passage line must re-derive **every** cell citing that
   item, not only the one the finding named (`20260821_1` NF-3: F6 wrote a new
   deciding line into the script and the 構成表 and left the 解説 quoting the old);
2. `logs/topics.json`'s `notes` for that test;
3. `test_spec.json` and `logs/ledger.json`, if the fix changed what a recorded
   draw shipped as;
4. the QA report's disposition column.

**A note that says a step is 未実施 after you implemented it is the same class of
defect as a note quoting a removed string**, and both are worse than no note: the
next paper's blueprint reads these fields and will chase a fixed bug or trust an
invalidated claim (`20260817_3`, `20260821_1` NF-5).

**Do not pin a repo-wide number in a note.** A warning total is true for one
minute; state the per-test invariant instead ("the only WARN naming this test is
X"), and if you quote a total, date it and say what would move it.

## Stage 5 — model answer (FINAL)

```bash
make scaffold-explanations <id>            # -> 詳細解説.json
make scaffold-explanations <id> LANG=vi    # -> empty 詳細解説.vi.json
make model-answer <id>                     # -> 模範解答.html
```

- **Only AFTER stage 4 returns `QA: PASS`** and all item/option/audio fixes are
  frozen. Generating it earlier is prohibited — any later fix desynchronizes it.
- **The scaffold PRE-FILLS every `options_analysis` line, and a pre-filled line
  is not an authored one.** A fresh scaffold is 100 % placeholders (393/393 on
  `20260904_2`), and they are well-formed, correctly tagged and inside every
  band — so **both 2021 imports shipped 100 % placeholder Japanese panes green**
  and only a human read caught it. `check_kaisetsu_no_scaffold_placeholders`
  FAILs them now. Replace every line with a reason drawn from THAT item; never
  delete a line, which breaks per-option parity.
- Then scaffold and author `詳細解説.vi.json` **in a second subagent that has not
  seen the Japanese set** — a translation is a defect. Both panes print the exam's
  own wording (stored once, in `詳細解説.json`); only the explanation switches.
- **Every field is capped** by `exam-model-answer`'s terseness bands; the gate
  FAILs an over-cap field. Cut padding, never a concrete reason.
- Concise, learner-friendly prose; zero pipeline metadata (`[kanji-n2.json]`,
  `[N1]`); all four options get individual concrete explanations; furigana
  (`《...》`) on target kanji/stems/key vocabulary.
- Re-run `make check` afterwards.

## Taking the exam

`make serve` (no id — one server lists every test), answer, press 「採点する」:
the page writes `採点結果.json` + `ユーザー解答.json`. CLI: `make grade <id>`.

## Invariants (every run)

- Japanese file names for all deliverables (`AGENTS.md` §2).
- Markdown is the single editable source, and **every source edit carries its
  rebuild in the same change**: `聴解スクリプト.txt` → `make mp3 <id>`; either
  `.md` → `make booklet <id> && make sheet <id>`. Artifacts carry the sha of the
  bytes they were built from and the gate compares them — but the gate is the
  backstop, not the workflow. Never hand-edit a sha.
- `聴解.md` and `聴解スクリプト.txt` stay synchronized: printed 例 options ↔ spoken
  例; any script item change requires a key check.
- After script/audio edits, re-run the dry-run validators in `choukai-audio`.
- **言語知識・読解 items are always original.** Never copy questions from the
  copyrighted textbooks in `refs/` into 問題1–14 — calibration only. The sampled
  topic gives WHAT to write about; compose the words yourself, no web fetch.
- **聴解 is the deliberate exception, since 2026-09-08.** The listening half is
  lifted verbatim from official past papers by `make mp3` (`choukai-audio`
  Part 0) — that is the point of the rework, not a violation of the line above.
  It also means a composed paper is **personal study material**: its listening
  items are real exam content, so a composed 聴解 must not be presented as
  original work, and `make pages` publishes it.
- Commit `tests/<id>/` and updated `logs/` together with the pipeline changes
  that produced them.
