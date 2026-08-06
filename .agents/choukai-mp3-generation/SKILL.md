---
name: choukai-mp3-generation
description: Single owner of synthesizing the choukai exam MP3 from the TTS script — voice assignment, official pacing, silence insertion, concatenation, and loudness. Use whenever generating, fixing, or tuning the listening audio, whenever the user mentions the MP3, voices sounding wrong (e.g., male narrator instead of the official female announcer), rushed pacing, or missing answer pauses. Do not write ad-hoc TTS loops — use scripts/make_choukai_mp3.py.
---

# Choukai MP3 Generation

## Executable & File Paths

- **Script location**: `.agents/choukai-mp3-generation/scripts/make_choukai_mp3.py`
- **Input text script**: `tests/<test_id>/聴解スクリプト.txt` (canonical name — see choukai-script-writing)
- **Output audio**: `tests/<test_id>/聴解.mp3` + per-question files in `tests/<test_id>/segments/`
- **Output chapters**: `tests/<test_id>/聴解_チャプター.json` — the start offset
  of every 問題 and every 例/N番 item, accumulated by the assembler as it
  concatenates (exact by construction; never recover these with
  `silencedetect` after the fact). Consumed by `interactive-answer-sheet` to
  drive the chapter dropdown in `解答.html`. Regenerate the MP3 to
  refresh it. It also carries `"script_sha"` — see the next section.

## `script_sha`: the MP3 says which script it was built from

`聴解_チャプター.json` is written as
`{"script_sha": …, "duration": …, "chapters": […]}`, where `script_sha` is the
**first 12 hex digits of sha1 over the raw bytes of `聴解スクリプト.txt`**
(`source_sha()` in the generator). `make check` recomputes it and fails when it
disagrees, which is the only mechanical evidence that the audio on disk speaks
the script on disk.

It exists because that failure shipped four times at once: commit `4df5631`
rewrote the 問題N instructions in `聴解スクリプト.txt` for tests 1, 2, 3, 4 **and**
`imported-n2-2025-07`, and re-ran `make mp3` for **test 3 only**
(`git log -1 -- tests/N/聴解.mp3`: t1 `99fdb9e`, t2 `99fdb9e`, t3 `4df5631`,
t4 `99fdb9e`, import `d3beca8`). Four shipped papers played superseded
instructions against booklets printing the new ones, through a green gate and a
full QA round.

- It is a **content** hash, deliberately not an mtime. Mtimes are
  checkout-unstable: after that commit test 3's `聴解.mp3` looked older than its
  script even though its audio was current, and its reviewer had to reconstruct
  git history to clear it, while the three genuinely stale papers looked exactly
  the same.
- **Never hand-edit the sha.** The only way to make it agree is to rebuild:
  `make mp3 <test_id>`. Editing the script without rebuilding in the same change
  is a defect (`jlpt-test-generation`, Invariants).
- The HTML deliverables use the same 12-hex convention as
  `<!-- src_sha: <file name>=<sha> -->` stamps (`build_booklet.py`'s
  `src_sha_comments()`, shared with `build_interactive.py`), so booklet and
  answer-sheet staleness is detected the same way.

## Execution

Prerequisites: `pip install edge-tts` (free, no key; ffmpeg required).

Run from workspace root:
```bash
python .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt
```
→ Outputs `聴解.mp3` inside `tests/<test_id>/`.

A cold build of a full N2 script (~250 lines → ~45 min of audio) takes about a
minute. Lines are synthesized concurrently (`TTS_JOBS = 8`); lower it if the
endpoint starts throttling:
```bash
python .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt --jobs 3
```
The floor is the final `loudnorm` encode (~35 s for a 45-minute file) — that pass
reads the whole assembled stream, so it cannot be split.

## Cleanup & Segment Retention

- **Automatic Cleanup**: Upon successful generation of `聴解.mp3`, the temporary `segments/` directory is automatically cleaned up and deleted to save disk space.
- **Retaining Segments**: If you need to keep per-question audio blocks for debugging or drilling, pass the `--keep-segments` flag:
  ```bash
  python .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/<test_id>/聴解スクリプト.txt --keep-segments
  ```



## Voice model (matches the official recording)

- **Narrator/announcer = FEMALE** (`ja-JP-NanamiNeural`, rate −10%). The
  official announcer is female; a male narrator was a real user complaint.
- Dialogue: male roles → `ja-JP-KeitaNeural`, female roles → Nanami at
  different rates so she is distinguishable from the narrator.
- 男1/男2 separated by rate (edge-tts free tier has only 2 ja-JP voices;
  `pitch` support varies by version — the script feature-detects it).
- **Speech rate is verified, not just chosen for voice contrast.** The
  per-speaker `rate` values in `SPEAKER_MAP` exist to make voices
  distinguishable, but they also determine whether the exam underestimates N2
  level — a correctly-paced recording of speech that's too slow is still an
  easier exam. Verified against `official-audio-analysis` step 5: dialogue
  lines (±0–6%) measure ~378 morae/min (natural/brisk N1-N2 range); narrator
  (−10%) measures ~295 morae/min, which only affects unscored instructions.
  **Any change to a rate value must be re-verified against that step** before
  shipping — nothing else in the pipeline checks speech rate.

## Casting: the narration and `SPEAKER_MAP` are one decision, and two speakers need two voices

`SPEAKER_MAP` decides which voice reads a `label:` line; the item's narration
tells the examinee who is speaking. Nothing in the audio reconciles them, so
both of these are **the author's** job at the moment the label is chosen — and
both shipped broken:

- **A narration that states a gender must resolve to a voice of that gender.**
  If the block says 「係員の**男の人**」/「〜の男の人」, the label on those lines must
  map to `MALE` (Keita); 「〜の女の人」 must map to `FEMALE` (Nanami). Test 3
  shipped **three** items where it did not — 係員の男の人, アナウンサーの男の人,
  職員の男の人, all three labels mapped FEMALE — so the announcer introduced a man
  and a woman's voice spoke. Resolve it by rewording the narration or by picking
  a label whose mapping already matches; **remapping an existing label is a
  last resort**, because labels are shared across every test and a remap
  silently changes the voice every other paper's already-built audio used —
  and `script_sha` cannot see that, because the map is not part of the hashed
  script. A remap means re-running `make mp3` for every affected test.
- **A two-party item whose two labels resolve to the SAME voice is a defect.**
  Same `voice` value separated only by a few percent of `rate` is not a
  distinguishable second person: the examinee cannot tell who said the deciding
  line, which is the whole task in 問題1/2/5. **All four papers shipped at
  least one**: test 1 three items (店員+女, 職員+女, 店員+女 — all Nanami),
  test 2 one (専門家+アナウンサー), test 3 one, test 4 one (教授+学生, both
  Keita). Cast one male and one female label per two-party item; `男1`/`男2`
  rate-splitting exists for the three-person conversation, where a third voice
  does not exist, not as a general licence.
- **Scan the WHOLE block for the narration, not its first line.** 問題5's 2番
  puts the situation on the block's **second** line (the 例-less section's
  item marker is its own line), which is exactly why a first-line-only pass
  missed test 3's third mismatch.

`make check` now checks both — the gender contradiction as a failure, the
one-voice pair as a WARN — but the map lookup belongs in authoring: read the
label out of `SPEAKER_MAP` before you write the narration around it, as
`choukai-script-writing` §"One voice per person" also requires.

## Pacing table (from official Dec 2025 N2 audio — do not guess new values)

| Constant | Value | Meaning |
|---|---|---|
| GAP_BETWEEN_LINES | 1.3 s | between dialogue turns |
| GAP_AFTER_PRE_QUESTION | 3 s | 問1: question → conversation |
| GAP_OPTION_READING | **20 s** | 問2 only: read printed options (most-missed pause) |
| GAP_BETWEEN_SPOKEN_CHOICES | 3 s | 問3/問5 spoken choices |
| GAP_AFTER_SHITSUMON1 | 10 s | 問5: between 質問1 and 質問2 |
| ANSWER_PAUSE | 問1/2: 12 s, 問3/4: 8 s, 問5: 10 s | after each item block |

To recalibrate against official recordings in `refs/JLPT/`, use `official-audio-analysis`
and update ONLY these constants.

## Engineering rules (each fixed a real bug)

- Synthesize per line → convert to 24 kHz mono WAV → concat WAVs → encode MP3
  ONCE with `loudnorm=I=-17:TP=-1.0:LRA=11`. Never concat MP3 segments directly.
- Retry synthesis (3×, backoff); cache segments in `tests/<test_id>/segments/`
  so re-runs skip finished lines. The cache key is a hash of
  **text + voice + rate**, not the line's position — keying on position alone
  meant a reworded line or a remapped speaker silently reused the old audio.
- **Parse into a plan, then synthesize, then assemble — in that order.** The
  plan pins every segment path and every gap duration up front, which is what
  makes the parallel passes safe: two tasks can never target the same file, and
  the assembled output is byte-identical to a sequential build (verified by
  running both versions over one set of cached segments).
- **Silence files are all created before block assembly begins.** Creating them
  lazily let two blocks shell out to ffmpeg for the same `_sil_1.3.wav`
  simultaneously; the loser got a truncated gap. Nothing downstream can detect
  that — the file is still valid audio, just the wrong length.
- Chapter offsets stay a strictly in-order running sum. Block durations are
  measured in parallel, but `clock` must accumulate block by block.
- **Script validation is a hard gate.** `validate_script()` runs before any
  synthesis and refuses to build on a missing 例, a wrong item count, an
  answer spoken aloud, an authoring annotation, or an unmapped speaker label.
  See `choukai-script-writing/SKILL.md` for the full table.
- **Every speaker label must be in `SPEAKER_MAP`.** An unmapped label does not
  raise — `voice_for()` falls back to the narrator, so the line is read by the
  announcer instead of the character. The validator now catches this.
- Item detection regex is `^(例。|\d+番。)` — WITH the 。, so a line that merely
  opens with a number and a 読点 (a spoken choice 「1、…」, or an enumerating
  lead-in like 「1番、2番。…」) is not mistaken for a question item. Note no
  official N2 paper carries that enumerating 問題5 line — 1番 gets its own
  lead-in and 2番's options are printed (see `choukai-script-writing`); the
  guard is defensive.

## Dry-run before synthesis (no network needed)

Simulate block parsing + pause assignment. Expected for a full N2 — these
follow directly from `ANSWER_PAUSE` above and the 33 item blocks
(問題1=6, 問題2=7, 問題3=6, 問題4=12, 問題5=2, 例 included):

| Pause | Count | Source |
|---|---|---|
| 12 s answer | 13 | 問題1 (6) + 問題2 (7) |
| 8 s answer | 18 | 問題3 (6) + 問題4 (12) |
| 10 s answer | 2 | 問題5 |
| 20 s option-reading | 7 | 問題2 only (例+6) |

**These counts describe OUR build, not the official file.** `pause_after()`
appends an answer pause after every item block, 例 included, while the official
recording follows an 例 straight into the 「最もよいものは◯番です…」
confirmation. So the official Dec 2025 audio measures 12 × 12 s and 17 × 8 s
where the table above says 13 and 18 (see `official-audio-analysis`). `make check`
asserts the table against `EXPECTED_ITEMS`/`ANSWER_PAUSE`, so do not "correct"
it toward the official histogram — change `pause_after()` first if the
deviation is ever worth closing.

The 33 item blocks are fixed; the TOTAL block count is not — the scripts on disk
run **43–46 blocks** (tests 1–4: 46, 44, 43, 43; `imported-n2-2025-07`: 46), and
the first, since-removed test 4 (removed in 9a794d5, last at b9b90de) was 56 —
all valid; the difference is only how instruction and announcer text is split.
So do not treat any total as a target: `validate_script()` enforces the 33 item
blocks and their distribution and merely *prints* the total
(`script OK: N blocks, …`).
Estimated length ≈ 45 min with TTS at these rates — the four built tests
measure **41.1–46.7 min** per their 聴解_チャプター.json (official ≈ 51.4 min;
human actors speak slower, and the remaining gap is acceptable).

