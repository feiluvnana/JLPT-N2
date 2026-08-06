# QA review — tests/4 (adversarial pass, `exam-qa-review`)

Reviewer: fresh-eyes context (authored nothing in test 4; read only `AGENTS.md`,
`.agents/exam-qa-review/SKILL.md`, and test 4's own files before starting).
Date of review: 2026-08-06. Sources reviewed at `言語知識・読解.md` sha
(see `make check` stamp), `聴解.md`, `聴解スクリプト.txt`, `tests/4/test_spec.json`,
`logs/ledger.json`, `logs/seeds.json`.

---

## 1. Verdict

**QA: FAIL (39 findings, 25 automatic)**

The paper may not be served or committed. Fix list is §3; the generator work
list is §4.

Entry condition: `make check` is green **for tests/4** (all per-test contracts
`ok`, 3 WARN). The gate's 25 FAIL lines belong to tests 1, 2, 3 and to one
repo-level check (`logs/seeds.json` reuses a URL). Test 4's own contracts pass,
so QA was allowed to start.

---

## 2. Blind-solve diff

All 71 言語知識・読解 items were answered from the item bodies, and all 30 聴解
items from `聴解スクリプト.txt`, before consulting the answer tables. Structural
caveat: both Markdown sources embed their answer tables in the same file, so
key-blindness cannot be perfect — each answer below was derived from the item
first, and every disagreement is filed as a finding rather than resolved in the
key's favour.

Reviewer agreed with the key on 92 of 101 items. Disagreements:

| Item | Key | Reviewer | Resolution |
|---|---|---|---|
| 43 | 1 | **3** | Finding A1 — key 1 cannot occupy ★. Slot 1 must be option 2 (「なお何か」+ noun phrase), slot 2 must be option 1 (the conditional 「ございましたら」), so option 1 is structurally the 2nd piece, never the 3rd. |
| 44 | 4 | 4 **or 2** | Finding A3 — two natural orderings; ★=4 and ★=2 both read. |
| 45 | 3 | 3 **or 2** | Finding A4 — the two adjunct phrases float around the fixed pair 2+3. |
| 47 | 1 | *unanswerable* | Finding A2 — no ordering yields grammatical Japanese against the printed stem. |
| 12 | 1 | 1 **or 4** | Finding A5 — 完全自動 is an attested compound and reads naturally in the stem. |
| 15 | 3 | 3 **or 2** | Finding A6 — 事業本部を設立した is standard corporate Japanese. |
| 49 | 2 | **4** | Finding A7 — the following sentence elaborates; it does not qualify. ただし is the wrong relation. |
| 50 | 3 | 3 **or 2** | Finding A8 — 元も子もない結果 fits the 結果 frame at least as well. |
| 聴解問4-8番 | 2 | 2 **or 3** | Finding A16 — a yes/no prompt with one natural affirmative and one natural negative reply. |

Reviewer errors (reviewer was wrong, key stands — recorded for the trail):
none. Every disagreement resolved against the item.

Items where the key stands but the elimination is tight, with the deciding fact
recorded (not findings): **19** (しんみり requires a somber register,
incompatible with 「温かい励まし」); **4** (省/鑑/顧/惟 all read ～みる — the
distractors do engage the tested reading); **聴解問4-3番** (存じ上げる takes a
person as its object, so 行き方 selects 存じております).

---

## 3. Findings — the fix list

### Automatic fails (each one fails the whole paper until fixed and re-reviewed)

| # | Item | Class | Evidence | Fix |
|---|---|---|---|---|
| A1 | 問題8 **43** | mis-key | Stem 「なお何か」 forces slot 1 = opt 2 「ご不明な点が少しでも」; the conditional 「ございましたらすぐに」 (opt 1) must follow it at slot 2. ★ (slot 3) is therefore 「事務局まで」 (opt 3), with 「お気軽に」 last. The 解説 spells the order as 「なお何か(2) → ご不明な点が少しでも(4) → ございましたらすぐに(1) → 事務局まで(3)」 — its numbers do not match its own texts (opt 4 *is* 「お気軽に」). | Re-key to 3, rewrite the 解説 order with numbers that resolve to the printed option texts. |
| A2 | 問題8 **47** | unanswerable / broken Japanese | Stem: 「…内容をいったん ＿ ＿ ＿★＿ ＿ ならない。」 Option 3 is 「計画そのものを」. Any ordering puts two を-marked objects in one clause (「内容をいったん計画そのものを白紙に戻してから」). 立ち返る is intransitive (に立ち返る), so 「計画そのものを」 has no verb but 白紙に戻して. The 解説 splices 「計画そのものをいったん白紙に戻してから…」 — i.e. against a stem in which 「内容を」 does not exist. | Restore the stem the 解説 assumes (delete 「内容を」), or replace option 3. Then re-splice. |
| A3 | 問題8 **44** | second ★ answer | Key order 3→2→4→1 gives 「省エネ活動をはじめとする環境保全の総合的な実現を急いで目指している」 (★=4). The floating adverb 「急いで」 also reads first: 1→3→2→4 = 「当地域では、急いで省エネ活動をはじめとする環境保全の総合的な実現を目指している」 (★=2), which is *more* idiomatic. | Replace 「急いで」 with a non-floating constituent. (Also: 「環境保全の総合的な実現」 is awkward Japanese.) |
| A4 | 問題8 **45** | second ★ answer | 「見直したのをちょうど」+「きっかけに、思い切って」 is a fixed adjacent pair; options 1 「健康的な体づくりのために」 and 4 「自分の意識改革として」 are both free adjuncts. Pair at slots 2–3 → ★=3 (key); pair at slots 3–4 → ★=2 (「生活習慣を 健康的な体づくりのために 自分の意識改革として 見直したのをちょうど きっかけに…」), equally natural. | Anchor one adjunct grammatically (e.g. bind it to the final verb) so only one ordering survives. |
| A5 | 問題3 **12** | second defensible answer | 「最新の洗濯機は、（　）自動で乾燥まで行なってくれる」 — key 全 (全自動) ✓, but option 4 完全 yields 「完全自動で乾燥まで行なってくれる」, an attested compound (完全自動運転 etc.) reading naturally here. No fact makes it impossible. Option set also mixes three single-char prefixes with one two-char word. | Two changes, not one: drop 完全 (it is a noun/adverb, not a member of the tested 接頭語 class) and tighten the stem so it excludes 半 as well — 半自動 is also a real word, so only the context can eliminate it (e.g. 「ボタン一つで洗濯から乾燥まで（　）自動で…」). Do **not** substitute an affix that forms no real word with 自動 (副自動・準自動): `question-authoring` 問題3 requires every option to be a real, productive affix attachable to that specific stem. |
| A6 | 問題4 **15** | second defensible answer | 「当社はアジア市場における新たな事業（　）を設立した」 — 事業拠点 (key) and 事業本部 (opt 2) are both standard; 事業本部 is an extremely common corporate term. | Replace 本部, or add a constraint to the stem that only 拠点 satisfies (e.g. 「現地法人の…」 / a location reading). |
| A7 | 問題9 **49** | mis-key / second answer | Prior sentence: 「雑談や偶発的な出会いの機会を減らしてしまう側面もある」. Following: 「画一的なアジェンダのみで終わる会議では、…斬新なアイデアが生まれにくくなる」 — that *spells out* the same negative, it does not qualify it. ただし introduces a proviso/exception, so the key is mis-used; opt 4 つまり (restatement/consequence) fits. | Re-key to 4, or rewrite the second sentence into a genuine qualification. Note すなわち/つまり-class connectives are the highest-risk shape in `exam-qa-review` step 2. |
| A8 | 問題9 **50** | second defensible answer | 「偶発的な対話からインスピレーションを得ていた人々にとっては、（　）とも言えるだろう」. Key 気が気でない状態 describes an emotion the local context never establishes; opt 2 元も子もない結果 fits the 「結果」 frame (efficiency gained, the very source of ideas lost). Cannot be shown impossible. | Replace opt 2, or rewrite the frame so an emotional state is the only fit. |
| A9 | 問題1 **1** | non-word distractors + **the target itself is unauthorable** | Options 2–4 (もてあそわる / まねわる / ひるがえわる) are **not Japanese words**; the 解説 invents spellings for them (弄わる / 招わる / 翻わる — the real verbs are 弄ぶ・招く・翻る), violating `exam-qa-review` step 3 "each a real word". **But the option set cannot be repaired.** The printed okurigana 「わる」 locks every option to the ～わる class (step 3 conjugation lock). `question-authoring` 問題1 then requires each distractor to be **either** (a) a reading of 労 or a same-radical/visual-component kanji, **or** (b) a real N2 word in the same semantic field. 労 reads only ロウ / いたわ(る) / ねぎら(う); no look-alike kanji (栄・営・学・券・努) yields a real ～わる verb; and the real ～わる verbs (ことわる・かわる・くわわる・まじわる・さわる・たまわる・おわる・そなわる・おそわる) are all unrelated kanji in unrelated fields — which is why `question-authoring` line 171 cites **this very item's earlier set** (`ことわる=断る, さわる=触る, かわる=代わる`) as the failure. Both branches are unsatisfiable, so an earlier fix round traded a branch-(a) violation for invented non-words. | **Do not patch the options — re-sample the target.** 労わる must leave the 問題1 draw (see A24 for its second defect). Draw a target whose kanji carries ≥2 plausible readings or has same-radical look-alikes in the same conjugation class, in the shape `question-authoring` models: 措置→そち/しょち/そうち, or 収まった→さだまった/しずまった/やすまった. |
| A10 | 問題1 **2** | **off-level key (N3)** + distractors eliminable on sight | Two defects. (1) `openjlpt/vocab-n3.json` lists 賢い/かしこい as an **N3** headword; step 2.5's second question ("would this appear as a headed item in an N3 or easier book?") answers yes, so the KEY is TOO_EASY for an N2 問題1 item. The gate's level-band check covers only 問題7–9 grammar via `references/level_band_grammar.txt`, so no gate sees a vocab key. (2) The distractors あやしい/たくましい/おそろしい are readings of 怪しい/逞しい/恐ろしい — unrelated kanji, unrelated semantic fields, so neither branch of the 問題1 rule is met either. | **Re-sample the target** (an N2-band ～い adjective). If 賢い were kept, branch (b) is at least constructible (さかしい=賢しい, するどい=鋭い are same-form, same-field) — but the band failure alone disqualifies it. |
| A24 | 問題1 **1** | non-standard orthography, sourced from the pool | The paper prints the target as 「労わる」. The vendored reference corpus spells it **労る** (`openjlpt/vocab-n1.json`), which is the standard okurigana; 労わる is a widespread but non-standard spelling. The defect originates upstream: `.agents/item-pool-sampling/references/pools.json` line 78 carries `労わる`. A 問題1 item cannot test a reading off a spelling the reference corpus does not use — and the extra 「わ」 is what forced the ～わる option class in A9. | Fix `pools.json` to 労る (or drop the entry), then re-sample. Do not merely re-spell the stem in the paper: the pool would re-draw the same defect next test. |
| A25 | pipeline | authoring contract was not produced by the pipeline | `logs/test_spec.json` — the blueprint AGENTS.md §2 names, the file `sample_items.py` writes (`SPEC = LOGS_DIR / "test_spec.json"`, line 30) and the file `merge_seeds.py` takes as its argument — **does not exist**. And the current sampler writes `answer_positions` into every spec it emits (lines 348–351), yet **no** on-disk spec (tests 1, 2, 3, 4) contains that key. So the four `tests/*/test_spec.json` files were not written by the current sampler: they are hand-made or stale. Two independent confirmations from the draw counts themselves — test 4's spec lists 5 `word_formation` items where `DRAW` says 3, and 18 `listening_scenarios` where `DRAW` says 21 (M10). Consequences: A22 (no answer balance), A23 (no blend provenance to trace), and the gate's "every web entry traces to logs/seeds.json" check **SKIPs** — a silent pass. | Re-run `sample_items.py --seed <n> --test-id 4` to regenerate a real contract (this also re-draws 労わる/賢い), then re-key the paper to the emitted `answer_positions`, or explicitly document test 4 as a pre-pipeline paper. |
| A11 | 読解 **52** opt 3 | broken Japanese | 「休憩時間を長をとることで、社員の疲労を軽減させる。」 — double を; should be 「長く」. Broken Japanese anywhere is an automatic fail. | Fix to 「休憩時間を長くとることで」. |
| A12 | 聴解 問題2 **2番** | fabricated distractors + invented 解説 quotes (×2) | Script (block 「2番。会社で男の人と女の人が昇降式デスク…」) never mentions 通路/移動スペース or 配線工事. Options 3 「オフィス内の移動スペースが狭くなること」 and 4 「パソコンの配線工事が必要になること」 are raised by nobody. The 解説 asserts 「通路の広さは前と変わらないよ」 and 「配線工事は特に必要なかったんだ」 — neither line exists. | Add the two lines to the dialogue **or** replace both options with points the dialogue raises and denies. Re-quote by copy-paste. |
| A13 | 聴解 問題2 **3番** | fabricated distractor + invented quote | The アナウンサー block says nothing about water. Option 4 「寝る前に冷たい水をたくさん飲む」 is ungrounded; 解説 quotes 「冷たい水を一気に…」. | Same as A12. Also 解説's key quote drops 「やや」/「エアコンを」 — re-paste verbatim. |
| A14 | 聴解 問題2 **4番** | fabricated distractor + invented quotes (×2) | Script says only 「道路工事による迂回やルートの変更はございません」. 解説 quotes 「新しい駅へのルートの追加はございません」 (not said) and 「増便をお望みの声も多く…当面は難しい」 (not said); option 4 「沿線の住民から増便の要望が寄せられたため」 is ungrounded. | Same as A12. |
| A15 | 聴解 問題2 **6番** | fabricated distractors (×2) + 解説 contradicts the script | Options 3 (他のアルバイトも休みを希望) and 4 (連絡がメール) are never spoken. Worse, the 解説 says option 1 is wrong because 「代わりに出られる人もこちらで探せる」 — the script says the opposite: 「代わりに出られる人を**自分で**探してくれても構わない」. | Same as A12, and rewrite the option-1 explanation from the actual line. |
| A16 | 聴解 問題4 **8番** | two defensible answers + target not tested | Prompt 「新しい部署の仕事にも、だいぶ慣れてきましたか。」 is a yes/no question: opt 2 「おかげさまで、だいぶ慣れてきました」 (yes) and opt 3 「いいえ、まだ板についていません」 (no) are both natural, appropriate replies. Separately, the drawn target 「板につく」 (`test_spec.json` quick_response) appears **only in the wrong option** — the prompt never uses it, so the sampled item is not tested. Opt 2 is also a verbatim echo of the prompt. | Rewrite the prompt to use 板につく (e.g. 「新しい仕事、そろそろ板についてきましたね。」) and give the key an idiomatic non-echo reply; make opt 3 inappropriate rather than merely negative. |
| A17 | 聴解 問題4 **5番** | target not tested | Drawn target 「気が利く」 appears only in wrong option 3 (「ええ、気が利くほうだと思います」). The prompt tests 恐縮 deflection instead. | Move 気が利く into the prompt, or record the substitution in the spec. |
| A18 | 聴解 問題3 **1番** | keyed option states what the source does not | Key 1 is 「**初級クラスにおける**教材選定のポイント」; the talk never mentions 初級 or any level. A hostile examinee rejects the key for exactly that word. | Delete 「初級クラスにおける」 from the key or have the 講師 say it. |
| A19 | 聴解 問題1 **3番 + 4番** | topic repeated inside the paper | 3番 = a woman explains the taxi 配車アプリ and the man downloads it; 4番 = a 係員 explains the taxi 配車アプリ and the man registers on it. Two consecutive items, same errand. `tests/4/test_spec.json` specified it: `"タクシー:配車アプリの使い方"` and `"タクシー乗り場:アプリ会員登録"`. | Re-scenario one of the two (fix belongs upstream in sampling — see R7). |
| A20 | 問題9 + 問題10(1) + 問題13 | topic repeated inside the paper | 問題9 cloze argues face-to-face 雑談/偶発的な出会い is being eroded by digital efficiency; 問題10(1) is an entire passage on 雑談 raising workplace 心理的安全性; 問題13 argues 静寂/余白 is being eroded by information flow. Three surfaces, one thesis. | Re-topic 問題10(1) or 問題13. |
| A21 | 問題11(2) | passage carried over from another test | test 4's スマート農業 passage vs `tests/3` 問題11: char-level similarity **0.589**, verbatim runs of 33 / 27 / 22 / 21 / 20 chars (e.g. 「がかかるものの、作業負担の軽減や先進的なイメージが若者の新規就農を」), the same 注1 担い手 + 注2 農薬散布, the same examples (自動走行トラクター / ドローンによる農薬散布 / AI自動収穫ロボット), and the **identical question stem in the identical item slot**: 「農業におけるスマート農業の導入について、筆者の主張に合うものはどれか。」 = item 59 in both papers. | test 3 was generated after test 4 (ledger: test 4 `2026-08-04 14:55`, test 3 `2026-08-05 18:53`), so the later paper is the copier — repair belongs in **test 3**. Test 4's own defect is that nothing detects the collision (R7). Either way the pair cannot both ship. |
| A22 | all 101 keys | answer-position balance never applied | Distribution 1/2/3/4 = **38 / 27 / 22 / 14** (position 1 = 38% of keys; expected ≈25 each). 言語知識・読解 27/18/16/10, 聴解 11/9/6/4. `tests/4/test_spec.json` contains **no `answer_positions` key at all**, so the gate's "keys match answer_positions (0 prescribed)" is a vacuous pass. Same in tests 1, 2, 3 (verified): all four specs lack the field; test 2 = 53/25/11/13, test 3 = 50/30/16/5. | Re-balance keys toward ≈25 each, and fix the sampler/gate (R8). |
| A23 | provenance | fabricated harvest stamp / step 3.5 skipped | `logs/ledger.json` records `harvest_sha "20260805c3d4"` for test 4. `sha1(logs/seeds.json)[:12]` = `dc34edede771` (test 3's stamp). Test 4's stamp is a date + `c3d4` — the same hand-made pattern as test 2's `20260804a1b2`. `tests/4/test_spec.json` carries **no** `harvest_sha` (which `merge_seeds.py` writes at line 467) and **zero** `"origin"` fields, so the blend never ran for test 4. AGENTS.md §4: "never by hand-writing a sha." | Either declare test 4 an offline pure-pool run explicitly and delete the fake stamp, or re-harvest and re-run `merge_seeds.py`. Do not hand-edit the sha. |

### Minor findings

| # | Item | Evidence | Fix |
|---|---|---|---|
| M1 | 問題13 instruction | 「後の問いに対する答えとして最もよいものを**,** 1・2・3・4から」 — ASCII comma (line 391). The gate only bans ASCII `,`/`.` in the script. | Replace with 、 |
| M2 | 読解 apparatus | 9 in-body `（注N）` glosses against the ~15 floor (official July 2025 = 30). Gate WARN. | Add N1/rare glosses in 問題10–13 |
| M3 | 聴解 casting | Gate WARN: 例(問題1) `男1/男2`, 問題2-1番 `教授/学生`, 問題5-1番 `先生/女`, 問題5-2番 `係員/女` each resolve to one voice. Worst in the 例, where 男1 assigns the task 「君は店の予約をお願いできるかな」 — if both men sound identical the practice item stops teaching the format. | Recast in `SPEAKER_MAP`; regenerate MP3 |
| M4 | 29 解説 cells | Gate WARN lists 15 読解 + 14 聴解 quotes not in the source. Most are paraphrases presented as verbatim 「…」 — e.g. 57 quotes 「完璧な言語習得よりも、互いを理解しようとする姿勢こそが重要だと考える」 where the passage reads 「完璧な言語習得を目指すことよりも、違いを認め合い互いを理解しようと努力する姿勢こそが何よりも重要だと考えている」; 55 quotes 「日中のパフォーマンスを低下させる」 where the passage says 「日中の集中力や判断力が低下してしまう」. Keys remain supportable; the quotes are invented. (The subset that is *substantively* false is filed separately as A12–A15.) | Re-paste every quote from the source |
| M5 | 問題11 (1)–(4) | All four passages end with the same template 「筆者は、…こそが…と考えている/主張する」, and all four opinion items (57/59/61/63) are keyed to that one sentence. The opinion question degenerates into last-sentence retrieval, 4× in a row. | Remove the summary sentences; make the position inferable from the argument |
| M6 | 問題7 **33** | Option 3 「3日間に限って」 is grammatical and semantically possible; only less idiomatic than にわたって. No impossibility statement can be written for it. | Replace opt 3 |
| M7 | cross-surface | 「願ってもない」 is used twice in one paper: 問題9-50 distractor 1 and 聴解問題4-10番 **key**. | One point, one surface |
| M8 | 聴解 問題4 | 8番 and 9番 are consecutive items both about 慣れる. 「田中さん」 addressed in 例/3番/4番, 「田中くん」 in 問題2-1番. | Vary items and names |
| M9 | 問題9 passage | 「対面対話の機会が失われていくことに**焦慮**を抱く人が」 — 焦慮 is rare/N1 and 「焦慮を抱く」 is an unusual collocation (危惧/不安 are standard), unglossed, inside the passage the cloze keys off. | Replace with 危惧/不安 |
| M10 | spec vs paper | `word_formation` lists 5 items (未記入, 遅刻がち unused) for 問題3's 3 slots, and `listening_scenarios` lists 18 where the taxonomy needs 21. **Corrected on re-review: the code is not at fault** — `sample_items.py` `DRAW` is already `word_formation: 3` and `listening_scenarios: 21`. A spec with 5 and 18 cannot have come from the current sampler, which is further evidence for A25. | No `DRAW` change. Regenerate the spec (A25); the two unused items are recorded in `logs/ledger.json` as drawn, so the ledger entry for test 4 needs the same regeneration |
| M11 | spec vs paper | `listening_scenarios` says 「バス会社:路線変更のお知らせ」 but the script is a 減便 announcement that explicitly denies route change (「ルートの変更はございません」); 「日本語教室:教材の選定」 vs the paper's 語学教室. | Align labels or re-sample |
| M12 | 聴解 問題5-2番 | 解説 cites the option as 「西が丘アパート（大学まで徒歩5分、家賃5万円）」; the booklet prints 「西が丘アパート（大学に近くて家賃が安い）」. | Quote the printed option |
| M13 | cross-test / rhetoric | tests/2's 沈黙 passage ("silence is thinking time, not awkwardness") and test 4's 問題13 ("silence and 余白 are not waste") make the same argument one test apart. Within test 4, the "a seemingly useless thing is actually valuable" template runs three times (雑談 / 手書き / 余白). | Vary the rhetorical shape |
| M14 | 問題2 **7** | Option 4 求める (もとめる) is not a reading of つとめる at all, so it dies before the 務/努/勤 discrimination begins. | Use a fourth つとめる spelling or a visually closer kanji |

---

## 4. Root-cause table (step 6.5)

Recurrence counted by reading the other tests on disk, not from memory.

| Findings | Code | Tests showing the class | Owning file | Concrete proposed edit |
|---|---|---|---|---|
| A1, A2, A3, A4 | `GATE-WRONG` + `RULE-UNENFORCEABLE` | 問題8 floating-adjunct double answers documented in tests 2, 3, 4 (≥3); the 解説-numbering hole is live in test 4 and invisible in all | `tools/check_consistency.py`; `question-authoring` 問題8 | Gate: resolve each `解説` order token **to the option text** and assert `resolved[2] == key option text` (today it only checks that the parenthesised digits form a 1–4 permutation whose 3rd equals the key, so a 解説 whose labels contradict its own texts passes). Add: assembled sentence must not contain two を-marked objects, and no option may duplicate a case-marked phrase already in the stem (catches A2). Skill: require the author to list, in the 解説, every alternative ordering tried and the grammatical fact that kills it. |
| A5, A6, A7, A8, M6 | `RULE-UNENFORCEABLE` | Two-defensible-answer items documented in tests 2, 3, 4 (≥3) | `question-authoring` (問題3–7, 問題9) | Make the impossibility line mandatory and structural: for every wrong option the 解説 must carry one of exactly three tags — `[非存在コロケーション]` / `[本文が否定]` / `[文法衝突]` — plus the fact. An option that can only be tagged "less natural" must be replaced. Add an explicit ban: a distractor that is itself an attested compound with the same head as the key (完全自動 vs 全自動, 事業本部 vs 事業拠点) is disallowed. |
| A9, A10, A24, M14 | `GATE-WRONG` (doc claims a check the gate does not have) + `RULE-UNENFORCEABLE` + pool-data defect | 問題1 defects in tests 1 (慌てて conjugation leak), 4 (twice: unrelated-kanji set, then non-words) — and `question-authoring` line 171 already names test 4's earlier set, so this item has now failed the rule in two different directions (≥2 tests, ≥2 rounds) | `tools/check_consistency.py`; `question-authoring` 問題1; `item-pool-sampling/references/pools.json` | **The documented check does not exist.** `question-authoring` line ~178 states "`make check` WARNs when a distractor reading is not a listed reading of the target kanji or of a same-radical kanji in `openjlpt/kanji-n2.json`" — the gate references `kanji-n2.json` in exactly two places: an existence check (line 1108) and a comment (line 1129). No such WARN is implemented, and none fired on three invented non-words. Fix in three parts: (1) implement it, and make the *real-word* half a **FAIL** — every 問題1 option must be a headword in `openjlpt/vocab-*.json` or a listed reading of a kanji in the target; a non-word is not a distractor. (2) `pools.json` must carry the distractor set (reading + source kanji) alongside each 問題1 target, so the sampler can refuse a target for which no compliant set exists (A9 is unauthorable by construction — that must be caught at draw time, not review time). (3) Validate every `pools.json` headword spelling against the `openjlpt` headword and fail on a mismatch (catches 労わる vs 労る). |
| A10 (band half) | `GATE-BLIND` | Not audited in 1–3; the gate has never checked a vocab key | `tools/check_consistency.py`; `question-authoring` | The level-band gate reads only `references/level_band_grammar.txt` (問題7–9 grammar). Add the vocab half: fail when a 問題1–6 **key** is a headword in `openjlpt/vocab-n3.json` and absent from `vocab-n2.json` (賢い), and warn when a key appears only in `vocab-n1.json`. See the calibration caveat in §5 before wiring the N1 side — that list's labels are not a band verdict. |
| A12, A13, A14, A15, M4 | `GATE-WRONG` | 解説-quote failures WARN in **all four** tests (1/2/3/4) — 4/4 systemic; ungrounded 聴解 distractors documented in test 1 and confirmed here | `tools/check_consistency.py`; `choukai-script-writing` | Promote the quote check from WARN to **FAIL for `聴解.md`**: the script is a closed text, so after normalising `…`, `（注N）` and quote marks every 解説 quote must be a substring of it. Add a companion check: every printed 問題1–3 option must share a content word (≥2 JP chars, non-stopword) with its own script block — that is what A12–A15 violate. |
| A16, A17 | `GATE-WRONG` | 2 items in test 4; not audited in 1–3 | `tools/check_consistency.py`; `item-pool-sampling` | The "問題1/2/4 test the items test_spec drew" check currently searches the whole 問題4 region, so a target sitting in a *wrong option* satisfies it. Restrict the search for `quick_response` targets to the prompt line (`N番。…`) plus the keyed reply. |
| A18 | `RULE-MISSING` | 1 (test 4) | `question-authoring` 問題3 (概要理解) | Add: a 問題3 key may contain no qualifier (level, audience, place, time) that the talk does not state; the key must be assemblable from words the speaker uses. |
| A19, A20, A21, M13 | `GATE-BLIND` + `RULE-UNENFORCEABLE` | Same-errand 聴解 pairs documented in test 4 (previous round) and live again here; cross-test passage copy = tests 3↔4, plus test 2 copying test 1's 注 notes (≥2) | `item-pool-sampling/scripts/sample_items.py`; `tools/check_consistency.py`; `web-topic-research` | Sampler: reject a draw in which two `listening_scenarios` share a head noun or the same object of the errand (「タクシー:配車アプリ」×2 must not be drawable), and reject a `reading_topics` entry whose head noun matches any topic in the previous two ledger draws. Gate: add a cross-test similarity check over **generated** tests' 読解 passages — fail on `difflib` ratio ≥0.45 or any verbatim run ≥20 JP chars, and fail on an identical question stem in the same item slot. Today the gate compares only `（注N）` definition lines and `例。` blocks byte-identically, which is why a 59%-similar passage with an identical stem passed. |
| A22, A25 | `PIPELINE-GAP` + `GATE-WRONG` | **4/4** — no test's spec has `answer_positions`; skew 53/25/11/13 (t2), 50/30/16/5 (t3), 38/27/22/14 (t4); `logs/test_spec.json` missing repo-wide | `tools/check_consistency.py`; `jlpt-test-generation` workflow | Correction to the obvious diagnosis: **the sampler is not at fault** — `sample_items.py` lines 348–351 already emit `answer_positions`, and line 30/372 write the spec to both `logs/test_spec.json` and `tests/<id>/test_spec.json`. The specs on disk lack the field and the logs copy is gone, so they did not come from it. Gate edits: **FAIL** when `answer_positions` is absent or empty (today: "0 prescribed — ok"); **FAIL** when `logs/test_spec.json` is missing while `tests/*/test_spec.json` exist; convert the web-trace check from **SKIP** to FAIL on a missing blueprint (a skip reads as a pass); and fail when any one answer position holds >32% of the 101 keys. These three vacuous outcomes are why four consecutive papers are answer-1-heavy with nobody noticing. |
| A23 | `RULE-IGNORED` + `GATE-WRONG` | Hand-made stamps in tests 2 and 4 (2/4); test 4's spec has no blend at all | process (AGENTS.md §0.4); `tools/check_consistency.py` | Process: step 3.5 was skipped and its evidence fabricated — no skill change needed, but it must be reported per §0.7. Gate: `harvest_sha` validation is format-only (`[0-9a-f]{12}`), so a date-plus-hex string passes. Require each ledger `harvest_sha` to equal `sha1` of a harvest on disk **or** to be mirrored by `spec["harvest_sha"]`; and require a spec with zero `"origin"` fields to carry an explicit `"offline": true`. |
| M2 | `GATE-WRONG` (already known) | 4/4 (9/6/29/5 in-body glosses) | `tools/check_consistency.py` | Promote the <15 in-body gloss WARN to FAIL for generated tests. |
| M3 | `RULE-UNENFORCEABLE` | 4/4 (WARN in every test) | `choukai-mp3-generation` (`SPEAKER_MAP`) | Make the two-party distinct-voice rule a FAIL for the 例 and for any item whose answer depends on who said what; give `SPEAKER_MAP` a documented contrasting-pair table rather than leaving casting to label names. |
| M5 | `RULE-UNENFORCEABLE` | Not audited in 1–3; template is 4/4 in test 4's own four passages | `question-authoring` 問題11 | Forbid a passage-final 「筆者は…と考えている/主張する」 summary sentence as the deciding line for the opinion question; the position must be inferable from the argument body. |
| M10 | `PIPELINE-GAP` | 1 (test 4) | `item-pool-sampling` | `DRAW["word_formation"]` must equal the 問題3 slot count (3), otherwise the ledger records untested items as used. |
| A11, M1, M7, M8, M9, M11, M12, M14 | `RULE-IGNORED` (mostly) | — | — | No skill change: existing rules cover broken Japanese, ASCII punctuation, one-point-one-surface, and quoting the printed option. Report as process failures. Two exceptions worth mechanising: extend the ASCII `,`/`.` check from the script to the booklet Markdown (M1 — `GATE-BLIND`), and add a booklet-option-vs-解説 text equality check for 問題5 (M12 — `GATE-BLIND`). |

**Blocking effect:** every code above other than `RULE-IGNORED` blocks the next
generation run (`AGENTS.md` §6). The `GATE-WRONG` entries are the dangerous
ones — A22 in particular means "green" has never been evidence about answer
balance for any of the four papers.

---

## 5. Coverage statement

**Steps run.** Step 1 (key-by-key proof) on all 101 items. Step 2 + 2b
(distractor impossibility / plausibility) on all 101. Step 2.5 (level band) on
問題7–9 keys — all twelve 問題7 keys (にともなって, ざるを得ない, にわたって,
次第, だからといって, を問わず, にかけては, ようがない, ことだ, を通して,
どころではない, をめぐって) plus 問題8/9 keys sit inside the N2 band; no N1
form is keyed and no N3-or-easier form is the sole point; 模倣 (N1, in
`openjlpt/vocab-n1.json`) appears only as passage vocabulary and is glossed in
問題12's own stem as 「模倣（真似）」, so it is not what the item keys on.

**Vocabulary band audit (added on re-review of A9/A10), and a warning to the
fixing agent.** Every tested 問題1–6 key and every 即時応答 idiom was looked up in
`openjlpt/vocab-n1/n2/n3.json`. Exactly **one** key is a clear band failure:
賢い/かしこい, an N3 headword absent from the N2 list (A10). The lookup also
returns "N1" for 把握, 模索, 妥協, 転換, 審査, じっくり, 前もって, 逃す, 省みる,
労る and "N3" for 依頼, 実施, 克服, 考慮, 偶然, 徐々に — **do not act on those
labels.** That corpus is an aggregate word list, not a JLPT band ruling: 把握・
転換・審査・じっくり・克服・考慮 are standard N2 exam vocabulary and are correctly
keyed here. Treating the labels as verdicts would be the same mis-measurement
this report codes `GATE-WRONG` elsewhere. Only 賢い fails on both the corpus and
the step 2.5 question ("would an N3 book head this?"). Step 3
(mechanical reads) on 問題1–14. Step 4 (聴解 structure) on all 30 items + 4 例.
Step 5 (topic table) below. Step 6 (provenance) against `tests/4/test_spec.json`
+ `logs/ledger.json` + `logs/seeds.json`. Step 6.5 (root cause) in §4.

**Question-type mapping** (step 4): 問題1 asks 何をしますか / 何をしなければ
なりませんか ✓, 問題2 asks どこを修正するように / 何が課題 / どうして / 何に一番
困っている ✓, 問題3 asks 何について ✓, 問題4 三択 ✓, 問題5 = 1番 unprinted +
2番 two questions ✓. No swap (the 問題1↔問題2 swap of the earlier round is gone).
All four 例 are answerable from their printed options and the announced number
matches the option the dialogue supports (例 announcements `[2,4,1,1]` = marksheet
pre-marks ✓, verified independently of the gate).

**Topic table** (one row per surface, incl. each 聴解 item; tests 3 and 2 are the
other generated papers on disk):

| Surface | test 4 | test 3 | test 2 |
|---|---|---|---|
| 問題9 cloze | デジタル化と対面対話 | 習慣化の仕組み | 選択肢と満足度 |
| 問題10(1) | 雑談の効用 ⚠ same thesis as 問題9 / 問題13 (A20) | 味覚と季節感 | 奨学金申請案内 |
| 問題10(2) | 図書館休館・電子書籍案内 | リサイクル自転車販売会案内 | ゴミ分別案内 |
| 問題10(3) | 手書き文字の価値 | 観光公害とマナー | 沈黙の役割 ⚠ echo of test 4 問題13 (M13) |
| 問題10(4) | 在宅勤務と生活リズム | 集中力を高める環境 | 夜間講座スケジュール |
| 問題10(5) | 規格外品の活用 | 職人の道具作り | 言語獲得と脳 |
| 問題11(1) | 多文化共生 | キャッシュレスと金銭感覚 | 時間の使い方と余白 |
| 問題11(2) | スマート農業 ❌ near-duplicate of test 3, identical stem at item 59 (A21) | スマート農業と担い手 | 雪と生活の知恵 |
| 問題11(3) | 古民家リノベーション | 地域コミュニティ再構築 | ペットと社会 |
| 問題11(4) | 伝統行事の継承 | 伝統工芸の現代的継承 (distinct: 道具作り) | 匂いと記憶 |
| 問題12 A/B | 模倣と独創 | 副業と機密保持 | ウォーキング1万歩 |
| 問題13 | デジタル時代の心の余白 ⚠ (A20, M13) | 郷土料理と記憶 | 昆虫食 |
| 問題14 flyer | 電子地域通貨キャンペーン | 防災訓練の企画案内 | 社内食堂アンケート |
| 聴解 問1-1 | 郵便局:再配達 | ハローワーク:失業給付 | 博物館:音声ガイド |
| 聴解 問1-2 | 出張:遅延連絡 | 塾:体験授業 | 家電売り場:商品選び |
| 聴解 問1-3 | タクシー:配車アプリ ❌ (A19) | 家電量販:配送日 | コンビニ:新サービス |
| 聴解 問1-4 | タクシー乗り場:アプリ登録 ❌ (A19) | 銀行:口座開設 | 研修:電話応対 |
| 聴解 問1-5 | マンション:設備点検 | 保険:契約内容確認 | レンタカー:返却場所 |
| 聴解 問2-1 | 大学:レポート指導 | 大学:事務窓口 | スーパー:てまえどり |
| 聴解 問2-2 | 会社:昇降式デスク | 会社:在宅勤務制度 | 講演会:防災 |
| 聴解 問2-3 | ラジオ:熱中症予防 | コンサート:入場方法 | 社内食堂アンケート |
| 聴解 問2-4 | バス会社:夜間減便 | 就職課:面接対策 | ボランティア:役割分担 |
| 聴解 問2-5 | 自転車シェアリング | 天気予報と週末 | 管理人室:騒音相談 |
| 聴解 問2-6 | アルバイト:シフト変更 | 電気工事:立ち会い日程 | 保育園:送迎時間 |
| 聴解 問3-1 | 語学教室:教材選定 | 開発:仕様変更 | 図書館:電子書籍説明 |
| 聴解 問3-2 | 見本市:名札と来場者情報 | 倉庫:在庫確認 | サークル:合宿計画 |
| 聴解 問3-3 | 会社:新製品プレゼン資料 ⚠ test 1 spec has 「会社:新製品のプレゼン」 (different item; no passage overlap found) | 保険窓口:内容変更 | プール:利用証更新 |
| 聴解 問3-4 | 市:路上喫煙禁止区域 | 研修会:グループワーク | 税務署:確定申告 |
| 聴解 問3-5 | 商店街:スタンプラリー | フードバンクと地域福祉 | ラジオ:食生活 |
| 聴解 問5-1 | 大学:研究室配属 | 観光案内:モデルコース | 会社:経費精算変更 |
| 聴解 問5-2 | 留学生センター:アパート探し | 文房具:法人契約 / 地域センター:食品寄付 | 留守番電話 / 講演会受付 / 企画会議 |

問題12 A/B themes are distinct across the three papers (模倣 / 副業 / ウォーキング) — the
three-in-a-row 働き方 pattern the skill warns about is not present. The 問題14 flyer
(地域通貨) shares no decisive detail with any listening item.

**`make check` WARN lines for tests/4 and their resolution** (3 WARNs):

1. `言語知識・読解.md: 解説 quotes trace to the passage/script` — **real, not a false
   positive.** 15 quotes. Filed as M4; the substantively false subset is filed
   separately. Spot-verified two by hand: 57's quote rewrites the passage's final
   sentence; 55's 「日中のパフォーマンスを低下させる」 replaces 「日中の集中力や
   判断力が低下してしまう」.
2. `読解 has substantial （注N） glosses (got 9)` — **real.** Filed as M2.
3. `聴解 item speaker pairs cast distinguishable voices` — **real.** Filed as M3.
   (A fourth WARN class, `聴解.md: 解説 quotes…`, is reported unprefixed but its
   14 quotes are test 4's — verified by matching them against
   `tests/4/聴解スクリプト.txt`; four of them are substantively false → A12–A15.)

Repo-level gate FAIL touching this review: `logs/seeds.json cites a distinct
source per seed — reused https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf`.
Not test 4's harvest (see A23) but it blocks the next run.

**Artifact freshness** (no staleness found): `聴解スクリプト.txt` 12:14 →
`聴解.mp3` / `聴解_チャプター.json` 12:18 (gate confirms `script_sha 35cc569a3e1b`
matches) → `言語知識・読解.md` 12:54 = `.html` / `解答.html` 12:54 with matching
`src_sha` stamps. The stale-MP3 and stale-HTML classes that hit tests 1 and 2 are
absent here.

**URLs fetched (step 6.5 spot-check, 2 of 22):**
- `https://www.maff.go.jp/j/kanbo/smart/index.html` → 200, MAFF 「スマート農業」
  page, subject matches the seed. Harvest is real, not invented.
- `https://www.env.go.jp/recycle/yoki/c_3_report/pdf/h23_lca_01.pdf` → 200, a
  real 377 KB MOE PDF (binary; title not extractable through the fetcher). This
  is the URL the gate flags as used by two seeds.

---

## 6. Skips — stated explicitly

1. **`聴解.mp3` was not listened to.** Audio content was verified structurally
   (script ↔ booklet instruction equality, `script_sha` ↔ chapter JSON, 例
   pre-mark ↔ announcement, spoken-option placement) but no waveform, pacing, or
   pronunciation check was performed. The voice-casting finding M3 comes from the
   gate's `SPEAKER_MAP` resolution, not from hearing the file.
2. **Tests 1–3 were not re-audited item by item.** Recurrence counts in §4 come
   from (a) `make check` output for those tests, (b) direct reads of the passages
   and specs named in the rows, and (c) defect classes already documented in
   `exam-qa-review`. Rows marked "not audited in 1–3" say so.
3. **Step 6.3 and 6.4 (web fact consistency, blend balance 30–60%, ≤2 seeds per
   domain, carrier-sentence cap) could not be run:** `tests/4/test_spec.json`
   contains no `"origin"` entries and no `harvest_sha`, so there is no blend to
   audit. That absence is itself finding A23.
4. **Key-blindness was structural, not perfect** — both Markdown sources carry
   their answer tables inline (§2).
5. **This pass ran in the main context rather than a subagent.** The session
   forbids spawning agents unless the user requests it; `AGENTS.md` §6's
   non-negotiable requirement (QA must not be an authoring context) is satisfied,
   since this context authored nothing in test 4 and read only `AGENTS.md`,
   `exam-qa-review/SKILL.md`, and the test's files.
6. **No fixes were applied and no skill files were edited**, per the user's
   instruction that a different agent will do the repairs. Note that
   `exam-qa-review` §"Boundaries" would normally have this reviewer add newly
   found defect classes (non-word 問題1 distractors; a 解説 permutation whose
   labels contradict its own option texts; a 即時応答 target tested only in a
   distractor; answer-position skew with no `answer_positions` in the spec) to
   that skill in the same session — that edit is **left open** and should be made
   by whoever applies §4.

---

## 7. Re-review requirement

After the fixes: regenerate booklet HTML + `解答.html` (+ MP3 if the script
changed), re-run `make check` and read every line including WARN, then send the
changed items **and their whole 問題** back through steps 1–4 with fresh eyes,
and rebuild §5's topic table if any topic moved. Items whose 問題 must be
re-reviewed in full: 問題1, 問題3, 問題4, 問題8, 問題9, 読解 問題10 (1), 問題11 (2),
聴解 問題1, 問題2, 問題3, 問題4. That is most of the paper — the fix round is
large enough to need its own QA pass, not a spot check.
