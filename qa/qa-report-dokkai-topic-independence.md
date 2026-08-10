# 読解 topic-independence audit — all three generated tests (2026-08-10)

Defect class: the 読解 half repeats subjects across passages, and repeats one
argumentative CLOSING MOVE across nearly every passage. Rules added this pass:

- `question-authoring/references/dokkai.md` §"Thirteen surfaces, thirteen different essays"
- `exam-blueprint` §"The four theme rules" rule 3 (reading = one surface per theme)
  and §"The four rules bind the SHIPPED surfaces"
- `jlpt-test-generation` §"One topic, one surface" (theme column + closing-move column)
- `exam-qa-review` §5 (both columns are QA's to judge)
- Gate: `check_topics_themes()` (FAIL) and `check_dokkai_rhetorical_monotony()` (WARN)
- Sampler: `THEME_CAP["reading_topics"] = 1` + `sample_distinct_theme()`

Closing-move marker band, measured on the 問題10→end region of the 31-sitting
archive: **official 5–9 per 読解 half (median 6)**; gate ceiling 12.

| test | themes before | closing-move markers before | status |
|---|---|---|---|
| 20260810_1 | 働き方 ×5 | 29 | **REPAIRED** — 13/13 distinct, 11 markers |
| 20260807_1 | 働き方 ×3, 睡眠・健康 ×2, 食 ×2, 消費・経済 ×2 | 19 | audited, not yet repaired |
| 20260810_2 | 食 ×2, スポーツ・余暇 ×2, 環境 ×2 | 28 | audited, not yet repaired |

## 20260807_1 — repair list

Headline set: 問題9 科学・技術 / 問題12 地域活性化 / 問題13 働き方 / 問題14 環境 /
聴解問題5 文化・伝統＋スポーツ・余暇 — five distinct, no re-authoring needed there.
Rule 2 therefore closes 働き方, 環境, 地域活性化, 科学・技術, 文化・伝統 and
スポーツ・余暇 to the remaining 読解 surfaces.

Re-tags that need no rewriting (the passage already sits in the other theme):

- 問題11(2) キャッシュレス決済と小規模店 → `デジタル化` (was 消費・経済)
- 問題11(4) 買い物のかたちの変化（通販・レビュー） → `消費・経済`

Four surfaces must change SUBJECT (theme in parentheses is the free slot to aim at —
available: 医療・福祉, 防災, 住まい, 教育, 子育て・家族, 人間関係, メディア・情報, 旅行・観光):

| surface | current subject | why it must move |
|---|---|---|
| 問題10(3) 短文 | サテライトオフィス試行の進め方 | `働き方`, and 問題13 owns that theme as a headline |
| 問題10(4) 短文 | 短い運動を生活に組み込む習慣 | `睡眠・健康`, duplicates 問題10(1) 睡眠時間と起床リズム |
| 問題11(1) 中文 | 食品ロス（家庭と事業） | `食`, duplicates 問題10(5) 食料自給／`環境` is blocked by 問題14 |
| 問題11(3) 中文 | 同一労働同一賃金と待遇差 | `働き方`, blocked by 問題13 |

Closing move: 19 markers, `だけで` ×15 — the section argues "X alone is not
enough" in almost every item, including the option rows.

## 20260810_2 — repair list

Headline set: 問題9 子育て・家族 / 問題12 環境 / 問題13 デジタル化 / 問題14 旅行・観光 /
聴解問題5 — check 聴解問題5's subjects before tagging.

Three surfaces must change SUBJECT, all 短文 (cheap):

| surface | current subject | why it must move |
|---|---|---|
| 問題10(3) | 休日の予定に余白を残すことの大切さ | `スポーツ・余暇`, duplicates 問題11(3) eスポーツ観戦文化 |
| 問題10(4) | 米粉商品の普及と品質確保 | `食`, duplicates 問題11(1) 昆虫食 |
| 問題10(5) | プラスチック容器包装の収集ルール変更案内 | `環境`, blocked by 問題12 生物多様性（headline） |

問題10(5) is the paper's notice — its replacement must still be a notice
(`dokkai.md` passage inventory: one notice, one business email per paper).

Closing move: 28 markers, `だけで` ×17, `求められ/欠かせな` ×6.

## Method note

Theme counts are taken from the SHIPPED surfaces, re-tagged by reading each
passage — not from `test_spec.json`, whose web seeds and `cloze_topic` carry no
theme at all. That gap is what let 20260810_1 ship five workplace surfaces green.
