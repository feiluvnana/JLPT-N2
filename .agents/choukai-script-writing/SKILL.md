---
name: choukai-script-writing
description: Single owner of the choukai TTS script file format — the .txt containing ONLY the text spoken in an official JLPT listening exam. Use whenever creating or editing the listening script, whenever the user mentions the TTS script, narration text, or the choukai audio source file. The MP3 generator's timing engine parses this file, so its block conventions are load-bearing — violating them silently corrupts the audio pacing.
---

# Choukai Script Writing

## File Location & Naming (Japanese File Names)

The TTS script file is written to the test folder:
- Path: `tests/<test_id>/聴解スクリプト.txt` (or `tests/<test_id>/script.txt`, e.g., `tests/1/script.txt`).

## Content rule: official narration ONLY

The file contains exactly what the announcer and voice actors say — nothing
else. No headers, no usage notes, no markers. Required elements (see
jlpt-exam-structure for the exact announcer lines):

opening line → per-section instruction → 「では、練習しましょう。」→ 例 →
「最もよいものは◯番です。…では、始めます。」→ items → … →
「これで、聴解試験を終わります。」

問題5 instead says 「この問題には練習はありません。」

## Block conventions (parser contract)

- Blocks are separated by ONE blank line. **One block = one audio unit.**
- Item blocks start with `例。` or `N番。` followed by the situation +
  question ON THE SAME LINE: `1番。会社で女の人と男の人が話しています。…か。`
- Section markers are their own blocks: `問題1。` (numbered, with 。).
- Instruction text (問題1では、…) is its own block.
- **The two-question 問題5 item must be ONE block**: instruction line,
  dialogue lines, 質問1。…, 質問2。… — a blank line inside it puts the
  12-second answer pause in the wrong place (this bug happened; don't repeat it).
- 問題1/2: repeat the question as the block's last line.
- 問題3/4/5 spoken choices: one per line, format `1、…。` `2、…。` (読点 after
  the digit — the parser and pacing engine key on `^[1-4]、`).

## Speaker labels

Dialogue lines: `男:` `女:` `男1:` `男2:` `夫:` `妻:` `学生:` `先生:` `店員:`
`医者:` `部長:` `店長:` `専門家:` `レポーター:` `教室の人:` — half or full-width
colon. Unlabeled lines = narrator. Any NEW label must be added to the voice
map in choukai-mp3-generation before use.

## Validation (run after every edit)

```python
import re, sys; from pathlib import Path
script_path = Path(sys.argv[1] if len(sys.argv) > 1 else "tests/1/script.txt")
t = script_path.read_text(encoding="utf-8")
blocks = [b for b in re.split(r"\n\s*\n", t) if b.strip()]
# N2 full exam: 48 blocks; item blocks: 22 with 12s answers (問1:6 問2:7 問3:6 問5:3),
# 13 with 8s (問4: 例+12). Check unmapped speaker labels = none.
```

Assert block count, pause distribution, and speaker coverage before shipping.
Common corruption to grep for: mojibake bytes (), stray Latin/Cyrillic words,
wrong speaker attribution inside 例 dialogues.


