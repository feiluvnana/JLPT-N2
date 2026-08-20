# JLPT N2 Mock Exam Workshop

Generates, calibrates, renders, and grades **official-quality JLPT mock exams**
(primarily N2), plus imports real past papers into the same format.

Each test is a folder under `tests/<test_id>/` holding a complete sitting:

- `言語知識・読解.html` — Language Knowledge & Reading booklet (A4 print geometry, furigana)
- `聴解.html` + `聴解.mp3` — Listening booklet and synthesized audio with official pacing
- `聴解スクリプト.txt` — the narration script the audio is built from
- `解答.html` — one merged answer sheet: 101 items (71 言語知識・読解 + 30 聴解),
  radio bubbles, embedded audio player, **in-page 180-point grading**
- `採点結果.json` — the grading result, read back by the result screen

Item selection is never left to a language model's memory: grammar points,
vocabulary, kanji, listening scenarios, and reading topics are drawn by a
seeded RNG from a non-repeating pool, blended with a fresh web topic harvest,
and every draw is recorded in `logs/ledger.json` so papers don't repeat.
Difficulty is calibrated against 31 sittings of real N2 past papers and the
Shin Kanzen Master textbooks in `refs/`.

> **Scope of this file.** README owns **environment setup only** — what to
> install and how to verify it. Everything else has exactly one owner
> elsewhere, and this file deliberately does not restate it:
>
> | You want | Read |
> | --- | --- |
> | The rules, directory layout, file-naming contract, command router | **`AGENTS.md`** |
> | To generate a new mock exam | `GENERATE.md` → `.agents/jlpt-test-generation/SKILL.md` |
> | To import an external PDF / past paper | `IMPORT.md` → `.agents/external-test-import/SKILL.md` |
> | How any one subsystem works | the 10 skills in `.agents/<name>/SKILL.md` |
>
> If this file and an owner file ever disagree, **the owner wins** — and the
> disagreement is a defect to fix, not to route around.

---

## Prerequisites

| # | Requirement | Needed for | Required? |
| - | --- | --- | --- |
| 1 | **Python ≥ 3.10** | everything (CI runs 3.12) | **yes** |
| 2 | `markdown`, `pykakasi` | booklet + answer-sheet rendering, furigana | **yes** |
| 3 | `edge-tts` + **internet** | `make mp3` — Microsoft Edge TTS, free, no API key | for listening audio |
| 4 | **ffmpeg** *and* **ffprobe** on `PATH` | `make mp3` — concat, loudness, duration | for listening audio |
| 5 | `pdfplumber`, `pypdf`, `pdfminer.six` | PDF extraction (`make extract-*`, imports) | for imports/refs |
| 6 | **GNU Make + a POSIX shell** | the `make` targets use `test -n … \|\| ( … )` | **yes** |
| 7 | **Git + Git LFS** | `refs/` is **2.3 GB / 261 PDFs and MP3s** behind LFS | **yes** |
| 8 | **Git symlink support** | `.claude/skills/*` are 10 symlinks into `.agents/*` | **yes** |
| 9 | **Noto Serif CJK JP + Noto Sans CJK JP** | the booklet CSS names these two fonts explicitly | for correct print output |
| 10 | **Node.js** | one gate check compares the in-page grader with `grade_answers.py` | optional (check skips) |
| 11 | **poppler** (`pdftoppm`) | `make extract-archive` page rasterisation | optional |
| 12 | `mutagen` | MP3 duration in `write_external_chapters.py` | optional |

There is no `requirements.txt` — install the Python packages with the one-liner
in your platform's section below.

---

## Setup — macOS

```bash
# 1. System tools
brew install python git git-lfs ffmpeg node poppler
brew install --cask font-noto-serif-cjk-jp font-noto-sans-cjk-jp

# 2. Python packages
python3 -m pip install markdown pykakasi edge-tts pdfplumber pypdf pdfminer.six mutagen

# 3. Clone WITH the LFS payload (2.3 GB — the past-paper archive)
git lfs install
git clone <repo-url> jlpt && cd jlpt

# 4. Verify
make check
```

To skip the 2.3 GB download for now, clone with
`GIT_LFS_SKIP_SMUDGE=1 git clone …` and fetch later with `git lfs pull`. The
pipeline runs fine without it — only reading the reference PDFs/MP3s needs it,
and the agent-readable extracts (`booklet.md`, `script.md`, `key.md`,
`audio_inspection.md` — 124 files) are plain text and always present.

---

## Setup — Windows

### Recommended: WSL2 + Ubuntu

Everything behaves exactly as it does on macOS, and you avoid all four native
Windows incompatibilities listed under [Native Windows](#native-windows-git-bashmsys2).

```powershell
wsl --install -d Ubuntu     # then reboot and open Ubuntu
```

```bash
# Inside Ubuntu
sudo apt update
sudo apt install -y python3 python3-pip make ffmpeg git git-lfs nodejs \
                    poppler-utils fonts-noto-cjk
pip install markdown pykakasi edge-tts pdfplumber pypdf pdfminer.six mutagen

# CRLF must stay off — see Troubleshooting
git config --global core.autocrlf false

git lfs install
git clone <repo-url> ~/jlpt && cd ~/jlpt
make check
```

⚠️ **Clone into the WSL filesystem (`~/jlpt`), not `/mnt/c/...`.** Cross-OS
file I/O against a 2.3 GB `refs/` tree is dramatically slower.

To open the exam in your normal Windows browser, run `make serve` in WSL and
visit <http://127.0.0.1:8765> — WSL2 forwards localhost automatically.

### Native Windows (Git Bash/MSYS2)

Workable, but two things in the repo assume a Unix host today:

1. **`tools/check_consistency.py:3449`** calls `subprocess.run(["which", "node"])`.
   Windows has no `which.exe` and the call has no `try/except`, so `make check`
   aborts with `FileNotFoundError` before the grader-parity check. Run it from
   **Git Bash** (which provides `which`), or change that line to
   `shutil.which("node")`.
2. **The `Makefile` hardcodes `python3`.** The python.org installer only creates
   `python.exe` / `py.exe`; `python3.exe` exists in the Microsoft Store build.
   Either use the Store build, or add a `python3` shim, or call the scripts
   directly (`python .agents/exam-app/scripts/build_interactive.py tests/1`).

Then:

```powershell
winget install Python.Python.3.12 Git.Git GitHub.GitLFS Gyan.FFmpeg OpenJS.NodeJS.LTS
winget install ezwinports.make        # or use MSYS2 / choco install make
```

- **Fonts** — download **Noto Serif CJK JP** and **Noto Sans CJK JP** from
  <https://github.com/notofonts/noto-cjk/releases>, then right-click →
  *Install for all users*. (`Yu Gothic`, already on Windows, covers the app UI.)
- **Symlinks** — enable **Developer Mode** (Settings → System → For developers),
  then `git config --global core.symlinks true`, **before cloning**. Without it
  the 10 files under `.claude/skills/` check out as text stubs containing a path,
  the skills stop resolving, and `make check` fails
  `every skill is symlinked under .claude/skills/`.
- **Console encoding** — set `PYTHONUTF8=1`. `make check` prints Japanese
  filenames (`聴解.mp3`), and the Windows console code page (cp1252/cp932)
  raises `UnicodeEncodeError` on them. (File I/O itself is safe: every one of
  the repo's ~112 `read_text`/`write_text` calls passes `encoding=` explicitly.)

Then run the same Python-package and clone steps as macOS, in Git Bash.

### Not available on Windows — and not needed

`tools/extract_jlpt_n2_new.py` builds a Swift + Vision OCR helper only when
`sys.platform == "darwin"`, so `script.md`'s OCR layer can't be regenerated off
a Mac. This costs you nothing: all 124 extracts are already committed, so you
never need to re-run `make extract-archive`.

---

## Verify your install

```bash
python3 --version                              # ≥ 3.10
python3 -c "import markdown, pykakasi, edge_tts, pdfplumber, pypdf, pdfminer; print('py deps ok')"
ffmpeg -version | head -1 && ffprobe -version | head -1
git lfs env | head -1
make check                                     # read EVERY line, including WARN
```

`make check` is the read-only gate (`tools/check_consistency.py`). Every check
in it exists because that exact inconsistency shipped broken at least once, and
each failure message *is* its own documentation — it names the rule, the
incident, and the repair. **A FAIL blocks the work; a WARN must be resolved or
explicitly justified.** Green is the floor, not a verdict on a paper's content.

---

## Everyday commands

`make help` prints the full list; **`AGENTS.md` §4 is the authoritative router**
(it maps every target to the skill that documents it). The short version:

```bash
make serve            # ONE server for every test → http://127.0.0.1:8765 (no test id)
make sheet 1          # rebuild tests/1/解答.html
make booklet 1        # rebuild both booklet HTMLs
make mp3 1            # re-synthesize tests/1/聴解.mp3
make grade 1          # CLI grading → 採点結果.json
make check            # the gate
make pages            # static GitHub Pages build → _site/
```

Per-test targets take the id positionally (`make sheet 1`) or as `TEST=1`;
default is `TEST=1`. `make serve` takes no id — one server covers every test.

### Taking a test

```bash
make serve
```

Opens the test list; pick a test, answer all 101 items with the 聴解 audio
playing in-page, submit, and the result screen scores it out of 180 with
per-section pass/fail. Answers land in `ユーザー解答.json`, the result in
`採点結果.json`.

### Generating a new mock exam

Don't improvise it — copy the prompt in **`GENERATE.md`** to an agent. It runs a
4-stage pipeline (blueprint → 4 parallel authoring sections → build+gate →
fresh-eyes QA) with a seeded RNG draw and a mandatory adversarial QA pass.

### Importing a real past paper

Copy the prompt in **`IMPORT.md`**. Imported tests live in
`tests/imported-<slug>/` — the `imported-` prefix is what marks a folder as
external rather than generated.

### Publishing

`make pages` builds a static, server-free twin of the app into `_site/`
(answers kept in `localStorage`); `make preview-pages` serves it on
<http://127.0.0.1:8766>. Pushing to `master` deploys it via
`.github/workflows/pages.yml` — enable it once in **Settings → Pages → Source:
GitHub Actions**. `_site/` is a build artifact: gitignored, never committed.

---

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `make check` fails **`built HTML matches the Markdown it stamps`** on a clean checkout | CRLF. `.gitattributes` has no `* text=auto`, and Git for Windows defaults to `core.autocrlf=true`, so line endings change the source hash the HTML stamps. `git config --global core.autocrlf false`, then re-clone. |
| `make check` fails **`every skill is symlinked under .claude/skills/`** | Symlinks checked out as text stubs. Enable Developer Mode + `core.symlinks true`, then re-clone. |
| `FileNotFoundError: 'which'` during `make check` | Native Windows shell. Use Git Bash or WSL — see [Native Windows](#native-windows-git-bashmsys2). |
| `UnicodeEncodeError` while printing 聴解 / 解答 filenames | Windows console code page. `set PYTHONUTF8=1`. |
| `make mp3` fails immediately | `ffmpeg`/`ffprobe` not on `PATH`, or no internet for the Edge TTS endpoint. |
| `聴解.mp3` fails the gate as built from a superseded script | The script changed after the audio. `make mp3 <id>` re-synthesizes and rewrites `聴解_チャプター.json`. |
| Booklet renders Japanese in the wrong typeface | Noto Serif/Sans CJK JP not installed — the CSS falls back to a generic `serif`. |
| `refs/` PDFs are ~130-byte text files | LFS pointers. `git lfs install && git lfs pull`. |
| `skip grader parity — node not installed` | Expected. Install Node.js to enable that check. |

---

## Contributing (and for agents)

**Read `AGENTS.md` end to end before your first change** — start with §0, the
read-everything-first compliance rule. Every defect this repo has shipped came
from skipping a rule that was already written down, not from a hard problem.

Then: run `make check` and read every line before reporting anything as done,
and put content changes through the `exam-qa-review` pass in a context that
did not author them.
