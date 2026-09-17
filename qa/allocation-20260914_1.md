# 20260914_1 — 読解/cloze allocation table (written BEFORE any prose exists)

Owner: the stage-3 orchestrator, per `jlpt-test-generation` §"Stage 2 — authoring"
("Pre-assign each of the 13 読解/cloze surfaces a closing-move shape … Pass each
読解 subagent its assigned shapes") and `question-authoring/references/dokkai.md`
§"The rhetorical-MOVE allocation table — filled in before any prose exists".

Themes are the stage-1 draw (`tests/20260914_1/test_spec.json`,
`items.reading_topics`, surface order). 問題9 has no seat in the draw; its theme
is assigned here as the 13th distinct theme (axis 1 requires 13 distinct), and
デジタル化 is the ONLY remaining theme that appears nowhere in the previous
paper `20260911_1` — the other seven unused themes all do.

Denominators (`dokkai.md` §"The denominator"): axis 1 = 13 theme rows (問題12
joint); axis 2 = **13 closings** (問題12 A and B separate, 問題14 outside); axis 3
= 12 passages; MOVE cap = 10 essay surfaces (問題12 A+B as ONE, 実用文 and 問題14
excluded).

| surface | theme | closing shape | final-sentence template (skeleton to write to) | MOVE | voice |
|---|---|---|---|---|---|
| 問題9 cloze | デジタル化 | 説明 | 分類外 — 理由節で言い切る 「…からである。」 | 機構の説明 | 常体 |
| 問題10(1) | 文化・伝統 | 随筆 | 分類外 — 体言＋「…に気づいた。」 | 一人称の前後比較 | 常体 |
| 問題10(2) | 医療・福祉 | 意外な観察 | 分類外 — 原因を述べて閉じる 「…ためだという。」 | **〈想定→実は〉#1** | です・ます |
| 問題10(3) | メディア・情報 | **実用文・分類外**（メール） | 分類外 — 依頼で閉じる | （実用文） | です・ます |
| 問題10(4) | 交通 | 主張 | `A だけではない。B こそが〜` | 機構の説明 | 常体 |
| 問題10(5) | 消費・経済 | **実用文・分類外**（お知らせ／案内） | 分類外 — 案内文で閉じる | （実用文） | です・ます |
| 問題11(1) | 行政・手続き | 条件提示 | `A では/ほど B が多い（相関）` | 数えたことの報告 | 常体 |
| 問題11(2) | 環境 | 反論応答 | `A わけではない` | 反論への応答 | 常体 |
| 問題11(3) | 子育て・家族 | 随筆 | `〜のは B だ（分裂文）` | 一人称の前後比較 | です・ます |
| 問題11(4) | 住まい | 説明 | 分類外 — 順序の言い切り 「…という順になる。」 | 機構の説明 | 常体 |
| 問題12(A) | 科学・技術 | 意外な観察 | 分類外 — 事実の言い切り 「…のほうが先に動いていた。」 | 数えたことの報告（A+B で1） | 常体 |
| 問題12(B) | 科学・技術 | 条件提示 | 分類外 — 限定条件 「…の場合に限って、…が成り立つ。」 | ↑ 同一surface扱い | 常体 |
| 問題13 | 人間関係 | 反論応答 | 分類外 — 「…に応じて変わる。」 | **〈想定→実は〉#2** | です・ます |
| 問題14 | 旅行・観光 | （axis 2 の外 — チラシ） | — | （実用文） | です・ます |

## Tallies — each checked against its own cap before any prose exists

- **closing shape (13 closings, cap 2 each)**: 説明 2 ・ 随筆 2 ・ 意外な観察 2 ・
  実用文・分類外 2 ・ 主張 1 ・ 条件提示 2 ・ 反論応答 2 = 13. ✔ none over 2.
- **final-sentence template (cap 2 each)**: `だけではない…こそが` 1 ・
  `わけではない` 1 ・ `相関 では/ほど` 1 ・ `分裂文 〜のは B だ` 1 ・ 分類外 9. ✔
  Named templates deliberately kept to one use each — official runs 0–1 per
  template (`dokkai.md`, MEASURED over 29 papers + 8 official sittings).
- **not-A-but-B reframe family** (「ではなく」「というより」「よりも…ほう」
  「だけでは…こそ」「わけではない」 — `dokkai.md`: five surfaces of ONE move):
  **2 of 13** (問題10(4), 問題11(2)). `20260821_1` F3 shipped 6 of 11; this plan
  is deliberately far under it.
- **MOVE (10 essay surfaces)**: 〈想定→実は〉 **2** ・ 機構の説明 3 ・
  数えたことの報告 2 ・ 一人称の前後比較 2 ・ 反論への応答 1 = 10. ✔ The skeleton
  is planned at **2**, which is what `qa-report-20260911_1` §9 told the next
  paper to plan (`20260911_1` shipped 10 of 10; caps: plan 2, accept 3).
- **axis 1 (13 theme rows)**: 13 distinct themes, no repeat. ✔
- **axis 3 (12 passages)**: です・ます on 問題10(2), 問題10(3), 問題10(5),
  問題11(3), 問題13 = 5 of 12 — clears `check_dokkai_polite_voice`'s floor of 3.

## Cross-test slot check vs the previous paper (`20260911_1`)

Its closing column was 問題9 随筆 / 10(1) 意外な観察 / 10(2) 実用文 / 10(3) 説明 /
10(4) 実用文 / 10(5) 随筆 / 11(1) 反論応答 / 11(2) 主張 / 11(3) 意外な観察 /
11(4) 条件提示 / 12(A) 条件提示 / 12(B) 反論応答 / 13 説明. **No surface above
carries the same shape as the same surface there** — checked row by row.

## Binding note for the 〈想定→実は〉 rows

Only 問題10(2) and 問題13 may state an attributed assumption and deny it. Every
other row must survive `dokkai.md`'s mechanical test: **delete the denial
sentence — there is none to delete.** In particular a 一人称の前後比較 row
describes the narrator's own PRACTICE before and after, never a belief the
narrator held and corrected (that re-skin is what put nine of `20260911_1`'s ten
essay surfaces on the skeleton).
