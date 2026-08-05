# Makefile for JLPT N2 Mock Exam Pipeline

.PHONY: help check grade sheet serve booklet mp3 sample merge-seeds init-import extract-pdf \
       classify promote-adjunct fetch-openjlpt suggest-pool expand-pools

# Handle positional arguments for targets (e.g., "make grade 1", "make sheet 1", "make booklet 1", "make mp3 1").
# `serve` is deliberately NOT here: one server covers every test, so it takes no id.
TARGET_CMDS := grade sheet booklet mp3
FIRST_GOAL   := $(firstword $(MAKECMDGOALS))

ifneq ($(filter $(FIRST_GOAL),$(TARGET_CMDS)),)
  POS_ARG := $(word 2,$(MAKECMDGOALS))
  ifneq ($(POS_ARG),)
    # Define dummy target for positional argument so make does not fail with 'No rule to make target'
    $(eval $(POS_ARG):;@:)
  endif
endif

TEST ?= $(if $(POS_ARG),$(POS_ARG),1)
SEED ?= 20260803
SLUG ?=

help:
	@echo "=========================================================================="
	@echo "                      JLPT N2 Mock Exam Commands                          "
	@echo "=========================================================================="
	@echo "  make grade 1          Grade test 1 (reads tests/1/ユーザー解答*.json)"
	@echo "  make grade TEST=2     Grade test 2"
	@echo "  make sheet 1          Build interactive answer sheet for test 1 (解答.html)"
	@echo "  make serve            Serve ALL tests: list -> exam -> result (no test id)"
	@echo "  make booklet 1        Build booklet HTML for test 1 (言語知識・読解.html & 聴解.html)"
	@echo "  make mp3 1            Synthesize listening audio for test 1 (聴解.mp3)"
	@echo "  make check            Verify docs/code/tests consistency (read-only)"
	@echo "  make sample           Sample question pool (item-pool-sampling)"
	@echo "  make merge-seeds      Merge logs/seeds.json into logs/test_spec.json"
	@echo "  make classify ITEM=x CATEGORY=y   Classify item level; optional STAGE=1"
	@echo "  make promote-adjunct  Promote approved staging rows into pools.json"
	@echo "  make fetch-openjlpt   Refresh OpenJLPT N1-N3 vocab/kanji slices"
	@echo "  make suggest-pool     Diff OpenJLPT N2 vs pools (WRITE_STAGING=1 to stage)"
	@echo "  make expand-pools     Batch-expand pools from OpenJLPT + curated topics"
	@echo "  make init-import SLUG=n2-2025-12   Scaffold tests/imported-<slug>/"
	@echo "  make extract-pdf PDF=a.pdf OUT=tests/imported-x/_extract/a.txt"
	@echo "=========================================================================="

check:
	python3 tools/check_consistency.py

check-tests:
	python3 tools/check_consistency.py --tests

grade:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$(TEST)

grade-%:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$*

sheet:
	python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/$(TEST)

sheet-%:
	python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/$*

serve:
	python3 .agents/interactive-answer-sheet/scripts/serve_sheet.py

booklet:
	python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/$(TEST)/言語知識・読解.md tests/$(TEST)/聴解.md

booklet-%:
	python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/$*/言語知識・読解.md tests/$*/聴解.md

mp3:
	python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/$(TEST)/聴解スクリプト.txt

mp3-%:
	python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/$*/聴解スクリプト.txt

sample:
	python3 .agents/item-pool-sampling/scripts/sample_items.py --seed $(SEED)

classify:
	@test -n "$(ITEM)" || (echo "usage: make classify ITEM=措置 CATEGORY=context_words [STAGE=1]"; exit 1)
	python3 .agents/item-pool-sampling/scripts/classify_level.py --item "$(ITEM)" \
		$(if $(CATEGORY),--category "$(CATEGORY)",) $(if $(STAGE),--stage,)

promote-adjunct:
	python3 .agents/item-pool-sampling/scripts/promote_adjunct.py

fetch-openjlpt:
	python3 .agents/item-pool-sampling/scripts/fetch_openjlpt.py

suggest-pool:
	python3 .agents/item-pool-sampling/scripts/suggest_pool_additions.py \
		$(if $(WRITE_STAGING),--write-staging,)

expand-pools:
	python3 .agents/item-pool-sampling/scripts/expand_pools.py

merge-seeds:
	python3 .agents/web-topic-research/scripts/merge_seeds.py logs/seeds.json logs/test_spec.json

init-import:
	@test -n "$(SLUG)" || (echo "usage: make init-import SLUG=n2-2025-12"; exit 1)
	python3 .agents/external-test-import/scripts/init_imported_test.py --slug $(SLUG)

extract-pdf:
	@test -n "$(PDF)" && test -n "$(OUT)" || (echo "usage: make extract-pdf PDF=a.pdf OUT=out.txt"; exit 1)
	python3 .agents/external-test-import/scripts/extract_pdf_text.py "$(PDF)" -o "$(OUT)"


