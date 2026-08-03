# Makefile for JLPT N2 Mock Exam Pipeline

.PHONY: help grade sheet booklet mp3 open sample merge-seeds

# Handle positional arguments for targets (e.g., "make grade 1", "make sheet 1", "make booklet 1", "make mp3 1")
TARGET_CMDS := grade sheet booklet mp3 open
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

help:
	@echo "=========================================================================="
	@echo "                      JLPT N2 Mock Exam Commands                          "
	@echo "=========================================================================="
	@echo "  make grade 1          Grade test 1 (reads tests/1/user_answers*.json)"
	@echo "  make grade TEST=2     Grade test 2"
	@echo "  make sheet 1          Build interactive answer sheets for test 1 (HTML)"
	@echo "  make booklet 1        Build booklet HTML for test 1 (言語知識・読解.html & 聴解.html)"
	@echo "  make mp3 1            Synthesize listening audio for test 1 (聴解.mp3)"
	@echo "  make open 1           Open both answer sheets for test 1 in browser"
	@echo "  make open TEST=2      Open answer sheets for test 2"
	@echo "  make sample           Sample question pool (item-pool-sampling)"
	@echo "  make merge-seeds      Merge logs/seeds.json into logs/test_spec.json"
	@echo "=========================================================================="

grade:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$(TEST)

grade-%:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$*

sheet:
	python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/$(TEST)

sheet-%:
	python3 .agents/interactive-answer-sheet/scripts/build_interactive.py tests/$*

booklet:
	python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/$(TEST)/言語知識・読解.md tests/$(TEST)/聴解.md

booklet-%:
	python3 .agents/exam-booklet-generation/scripts/build_booklet.py tests/$*/言語知識・読解.md tests/$*/聴解.md

mp3:
	python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/$(TEST)/聴解スクリプト.txt

mp3-%:
	python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/$*/聴解スクリプト.txt

open:
	$(BROWSER_CMD) "tests/$(TEST)/言語知識・読解_解答.html" "tests/$(TEST)/聴解_解答.html"

open-%:
	$(BROWSER_CMD) "tests/$*/言語知識・読解_解答.html" "tests/$*/聴解_解答.html"

# Browser opener: macOS 'open', Linux 'xdg-open'
BROWSER_CMD := $(shell command -v open >/dev/null 2>&1 && echo open || echo xdg-open)

sample:
	python3 .agents/item-pool-sampling/scripts/sample_items.py --seed $(SEED)

merge-seeds:
	python3 .agents/web-topic-research/scripts/merge_seeds.py logs/seeds.json logs/test_spec.json
