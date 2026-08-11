# Makefile for JLPT N2 Mock Exam Pipeline

.PHONY: help check check-tests grade sheet keyless serve pages preview-pages booklet mp3 sample \
       init-import extract-pdf extract-archive extract-keys

# Positional test-id argument: "make grade 1", "make sheet 2", "make sample 5".
# Equivalent: "make grade TEST=1". `serve` is deliberately NOT here: one server
# covers every test, so it takes no id. `pages` builds every test by default;
# "make pages 1" (or TEST=1) narrows it to one.
TARGET_CMDS := grade sheet keyless booklet mp3 pages sample
FIRST_GOAL   := $(firstword $(MAKECMDGOALS))

ifneq ($(filter $(FIRST_GOAL),$(TARGET_CMDS)),)
  POS_ARG := $(word 2,$(MAKECMDGOALS))
  ifneq ($(POS_ARG),)
    # Define dummy target for positional argument so make does not fail with 'No rule to make target'
    $(eval $(POS_ARG):;@:)
  endif
endif

TEST ?= $(if $(POS_ARG),$(POS_ARG),1)
# No default seed on purpose: the seed must be an RNG output passed explicitly
# (SEED=$$(python3 -c "import secrets; print(secrets.randbelow(10**8))")),
# never a hand-picked or remembered number — see exam-blueprint/SKILL.md.
SEED ?=
SLUG ?=
# GitHub Pages build output. Gitignored: CI builds it, nothing commits it.
SITE ?= _site
PAGES_PORT ?= 8766
# pages narrows to one test only when an id was given explicitly (positional or
# TEST= on the command line); a bare `make pages` builds all tests.
PAGES_TEST = $(if $(POS_ARG),$(POS_ARG),$(if $(filter command line,$(origin TEST)),$(TEST),))

help:
	@echo "=========================================================================="
	@echo "                      JLPT N2 Mock Exam Commands                          "
	@echo "=========================================================================="
	@echo "  make check            Verify docs/code/tests consistency (read-only)"
	@echo "  make check-tests      Same gate, per-test contracts only (skips doc/code checks)"
	@echo "  make sample 5 SEED=n  Sample question pool -> tests/5/test_spec.json + ledger"
	@echo "                        (SEED required, from an RNG: python3 -c 'import secrets; print(secrets.randbelow(10**8))')"
	@echo "  make booklet 1        Build booklet HTML for test 1 (言語知識・読解.html & 聴解.html)"
	@echo "  make mp3 1            Synthesize listening audio for test 1 (聴解.mp3)"
	@echo "  make sheet 1          Build interactive answer sheet for test 1 (解答.html)"
	@echo "  make keyless 1        Blind-solve render for QA: qa/1/keyless.md (no keys)"
	@echo "  make serve            Serve ALL tests: list -> exam -> result (no test id)"
	@echo "  make grade 1          Grade test 1 (reads tests/1/ユーザー解答*.json)"
	@echo "  make pages            Build the static GitHub Pages site into _site/ (all tests)"
	@echo "  make pages 1          Same, only test 1"
	@echo "  make preview-pages    Serve _site/ locally to check the Pages build"
	@echo "  make init-import SLUG=n2-2025-12   Scaffold tests/imported-<slug>/"
	@echo "  make extract-pdf PDF=a.pdf OUT=tests/imported-x/_extract/a.txt"
	@echo "  make extract-archive  refs/JLPT_N2_NEW/*/ -> booklet.md script.md audio_inspection.md"
	@echo "  make extract-keys     Answer-key PDF -> per-exam key.md + answer_keys.json"
	@echo "  (any per-test target also takes TEST=<id>; default TEST=1)"
	@echo "=========================================================================="

check:
	python3 tools/check_consistency.py

check-tests:
	python3 tools/check_consistency.py --tests

sample:
	@test -n "$(SEED)" || (echo 'usage: make sample <id> SEED=$$(python3 -c "import secrets; print(secrets.randbelow(10**8))")'; \
	  echo 'the seed must be an RNG output, never a number an agent picked (exam-blueprint/SKILL.md)'; exit 1)
	python3 .agents/exam-blueprint/scripts/sample_items.py --seed $(SEED) --test-id $(TEST)

booklet:
	python3 .agents/exam-app/scripts/build_booklet.py tests/$(TEST)/言語知識・読解.md tests/$(TEST)/聴解.md

mp3:
	python3 .agents/choukai-audio/scripts/make_choukai_mp3.py tests/$(TEST)/聴解スクリプト.txt

sheet:
	python3 .agents/exam-app/scripts/build_interactive.py tests/$(TEST)

# The QA blind-solve render: the same paper with the keys truncated away, into
# qa/<id>/keyless.md. Not a deliverable — tests/<id>/ has a fixed file contract.
keyless:
	python3 .agents/exam-app/scripts/build_interactive.py tests/$(TEST) --keyless

serve:
	python3 .agents/exam-app/scripts/serve_sheet.py

grade:
	python3 .agents/exam-app/scripts/grade_answers.py --test-dir tests/$(TEST)

# The static twin of `make serve`: same three screens, answers kept in the
# browser's localStorage because GitHub Pages has no server and no disk.
pages:
	python3 .agents/exam-app/scripts/build_pages.py $(PAGES_TEST) --out $(SITE) $(PAGES_FLAGS)

preview-pages:
	@test -d $(SITE) || (echo "no $(SITE)/ — run make pages first"; exit 1)
	python3 -m http.server -d $(SITE) $(PAGES_PORT)

init-import:
	@test -n "$(SLUG)" || (echo "usage: make init-import SLUG=n2-2025-12"; exit 1)
	python3 .agents/external-test-import/scripts/init_imported_test.py --slug $(SLUG)

extract-pdf:
	@test -n "$(PDF)" && test -n "$(OUT)" || (echo "usage: make extract-pdf PDF=a.pdf OUT=out.txt"; exit 1)
	python3 .agents/external-test-import/scripts/extract_pdf_text.py "$(PDF)" -o "$(OUT)"

# Turn the refs/JLPT_N2_NEW/ past-paper archive into agent-readable Markdown.
# Read-only with respect to the PDFs/MP3s; writes only the .md/.json beside them.
extract-archive:
	python3 tools/extract_jlpt_n2_new.py --all

extract-keys:
	python3 tools/extract_jlpt_n2_key.py
