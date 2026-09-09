# `refs/External/` — material fetched from the open web

Added 2026-09-09. Everything here came from **jlpt.jp**, the JEES/Japan
Foundation official site, which publishes these files for free download. Same
rules as every other `refs/` folder (`AGENTS.md` §3): the binaries are
gitignored and ride the `refs` release, the `*.md` extracts are tracked.

**Read §1 before treating anything here as new listening material.** Two of the
three folders are re-releases of sittings this repo already has.

---

## 1. What is a duplicate, and how that was measured

The 『日本語能力試験公式問題集』 volumes are **retired real sittings**, not new
items. Measured, not assumed — two independent tests:

**Printed options against `refs/JLPT_N2_NEW/*/booklet.md`** (exact extracts).
48 printed 問題1/問題2 option strings were taken out of the 2018 volume's
listening booklet and grepped across all 31 archive booklets: **42 hit. 38 of
them land on `7. N2 12-2016`**; the other 4 are the 問題1 and 問題2 **例** option
lists, which land on `9. N2 7-2018` — 例 items are reused across papers
independently of the scored ones.

**Script text against `refs/JLPT_N2_NEW/*/script.md` and the ten
`tests/imported-*/聴解スクリプト.txt`.** ~200 ten-character windows per volume,
sampled across the whole script:

| volume | best match | second | background |
|---|---|---|---|
| 公式問題集 第二集 (2018) | **40.7 % → `7. N2 12-2016`** | 2.1 % | ~2 % |
| 公式問題集 第一集 (2012) | **37.9 % → `2. N2 7-2011`** | 2.5 % | ~2 % |

A ~40 % window hit against a ~2 % floor is identity — the missing 60 % is OCR
error in the archive's own extract, not different content. The archive copies of
both sittings are 1-bit stencil scans; these PDFs are the same papers born
digital.

So:

| folder | listening items | novel? |
|---|---|---|
| `official_workbook_2018/` | 問題1 ×5, 問題2 ×6, 問題3 ×5, 問題4 ×12, 問題5 ×3 | **No** — is `7. N2 12-2016` |
| `official_workbook_2012/` | full paper | **No** — is `2. N2 7-2011` |
| `mondaireishuu_2009/` | **5 with audio** (one per 大問); the PDFs print 9 | **Yes** — pre-dates the first new-format sitting (2010-07). Four are banked, see §4 |

Reproduce either test from this folder's PDFs plus the archive extracts; both
are string containment, no tooling.

---

## 2. `official_workbook_2018/` — 『日本語能力試験公式問題集 第二集』N2 (= 12-2016)

<https://www.jlpt.jp/samples/sampleindex.html>

Files: `N2V/N2G/N2R/N2L/N2script/N2answer/N2sheet.pdf`,
`N2Q1..N2Q5.mp3` (one MP3 per 大問, 642/823/611/487/522 s, 128 kbps).

**Its value is not new audio — it is exact text for a sitting that is otherwise
a stencil bitmap.** `textbook_bank_plan.md` §6.4 names the cost of importing one
of the 21 un-imported archive sittings as "every quoted line needs checking
against a page that is a 1-bit stencil bitmap". For 12-2016 that cost is now
zero:

- `script.md` — **exact**, from the PDF's embedded text layer (`pdffonts` shows
  CID Type 0C, `uni yes`), not OCR;
- `booklet_choukai.md` — **exact** printed 問題1/問題2 option lists;
- `key.md` — the full 正答表, all sections.

Extracts were written with the repo's own owner tool, so they are reproducible:

```bash
make extract-pdf PDF=refs/External/official_workbook_2018/N2script.pdf \
                 OUT=refs/External/official_workbook_2018/script.md
```

It routes CID-keyed fonts through pdfminer, which interleaves the **furigana
per character** (`授\nじゅ\n業\nぎょう\nで先…`). The text is exact; it is just not
laid out for reading by eye. `pdftotext -nopgbrk` on the same PDF puts each ruby
run on its own line above the main line instead, which reads better — use that
for a visual check, and this file as the extract of record.

## 3. `official_workbook_2012/` — 『公式問題集 第一集』N2 (= 7-2011)

Same layout. `N2Q2.mp3` is served from `sample2017/` upstream, the other four
from `sample2012/`; `N2Q1/3/4/5` are 35–39 kbps against Q2's 128 kbps, so the
volume is not one encode.

`script.md` is exact, same as above. **`N2L.pdf` has no usable text layer** —
the listening booklet pages are images, so there is no exact printed-option
list for 7-2011 here, only the script.

## 4. `mondaireishuu_2009/` — 『新しい「日本語能力試験」問題例集』N2

<https://www.jlpt.jp/samples/sample09.html>

`N2Sample.mp3` (554 s), `N2-mondai.pdf` (24 pp), `N2-script.pdf` (5 pp),
`N2-kaitou.pdf`, `N2-seikai.pdf`.

**The only genuinely new official listening material found — and four of its
items are now in the clip bank** (`textbook_bank_plan.md` §7:
`mondaireishuu:問1-1 / 問2-1 / 問3-1 / 問4-1`, one per 大問). Nine items,
published 2009 to demonstrate the then-new format, so they were never a sitting
and are in no archive folder.

Checked per item against all 31 `script.md` and the ten
`tests/imported-*/聴解スクリプト.txt`, one distinctive phrase each (研究室の前の
けいじ / 出張の準備 / 箱に入れ / 前髪 / 通信販売 / 充電式 / 佐藤さんって / 残って
仕事 / タバコ): **no listening-script hit for any of the nine.** The
`1. N2 12-2010` hits on 通信販売 and 一石二鳥 are in that sitting's 読解 booklet,
not its audio.

**One caveat.** 問題1-1番 (授業で先生が…宿題を確認しますか) IS `9. N2 7-2018`'s
問題1 **例** — its four printed options match that sitting's `booklet.md`
verbatim, and it is also the 2018 workbook's own 問題1 例. It does not show up in
any `script.md` because the official script PDFs never print the 例
(`choukai-audio` Part 0, "What the bank cannot give you"). That cuts both ways:
it is a duplicate of a 例, but it is also the first 例 transcript this repo has,
and a 例 is never drawn into a scored slot. The rest are unencumbered.

**The MP3 carries ONE item per 大問, not two.** jlpt.jp says so on the page and
the file confirms it: five answer pauses, five 「N番。」 calls, every one of its
554 seconds accounted for (the per-item offsets are in `textbook_bank_plan.md`
§7). The booklet and script PDFs print a second item per 大問 that has no audio,
so those four are text-only and unbankable.

The 問題2 item lays the **full** 20.19 s option-reading pause, 11.90 s into the
clip — the measurement no Shin Kanzen track in the whole book can pass
(`textbook_bank_plan.md` §3, max 10.1 s) and the one that bottlenecks 問題2. The
問題3/4/5 answer pauses run 5.2 s against official's 8 s, which does not matter:
the composer discards and re-lays every answer pause.

問題5's item is `excluded` — 86.2 s against its 105–250 s band, because it is the
old one-question 統合理解 shape. It is kept with its measurement because it is
the only 問題5 item in any source whose options are SPOKEN.

**Every PDF in this folder is a scan with no text layer** — script, booklet and
key all have to be read off the page. The script pages are clean typeset
images (not stencil), so they read reliably at Read-tool resolution.

## 5. jlpt.jp is fully mined

**And so is the official corpus itself.** `refs/JLPT_N2_NEW/` holds 2010-07
through 2025-12 with no gap except the cancelled 2020-07 — 31 of 31 sittings the
current format has ever run. The Vietnamese prep sites and YouTube channels that
publish 「Choukai JLPT N2 12/2014 (Script)」-style sets are redistributing those
same sittings, re-encoded, so **no web source can add an official N2 sitting to
this repo.** Anything the web offers beyond §4 is either a copy of the archive or
a third-party-authored mock.

`sample2009…sample2026` were probed for a third volume:
`https://www.jlpt.jp/samples/sample<YYYY>/pdf/N2script.pdf` and
`.../mp3/N2Q1.mp3` return 404 for every year except **2012** and **2018** (plus
one stray `sample2017/mp3/N2Q2.mp3`). There is no 第三集. The braille page
(`tenji.html`) carries no audio.

## 6. What was rejected, and why

Nothing below is in this folder; each was checked and turned down.

| source | what it has | why not |
|---|---|---|
| Jリサーチ出版『日本語能力試験完全模試N2』 | 3 full mock papers, **audio free** (credentials printed on the product page) | script, key and printed options are in the paid book only. Audio alone is unbankable: 問題1/問題2 options are never spoken, and no 大問's key is recoverable from audio |
| スリーエー『新完全マスター聴解N2』free audio | the same recordings as `refs/Shinkanzen/` | already in the pool |
| スリーエー『JLPT聴解N2 ポイント＆プラクティス』 | free audio | same shape as the row above — text is in the book |
| japanesetest4you.com | 5-item listening sets, answer key, transcript PDF link | no audio on the page, no source attribution, and the options are **picture legends** — the class `textbook_bank_plan.md` §4 already excludes because `render_booklet` prints a flat 1–4 list |
| jlptsensei.com / jlptsamurai.com "free practice test" | repackaged jlpt.jp files | duplicates of §2–§4 |
| archive.org | textbook scans, YouTube lecture rips | pirated uploads of the same two publishers; nothing exam-format with audio **and** script |

The pattern is one constraint, not many: **audio is widely free, exam text is
not.** A clip needs a transcript, a key, and — for 問題1/問題2 — a printed option
list, and no open source publishes all three beside a recording except jlpt.jp.

## 7. Restoring the binaries

Same as every `refs/` folder:

```bash
gh release download refs --pattern 'External.zip' --dir /tmp
unzip -n /tmp/External.zip -d refs/
```
