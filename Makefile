# Makefile for JLPT N2 Mock Exam Pipeline

.PHONY: help grade template pdf mp3 sample merge-seeds

# Handle positional arguments for targets (e.g., "make grade 1", "make template 1", "make pdf 1", "make mp3 1")
TARGET_CMDS := grade template pdf mp3
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
	@echo "  make grade 1          Grade test 1 (using tests/1/マークシート.pdf)"
	@echo "  make grade TEST=2     Grade test 2"
	@echo "  make template 1       Generate answer template & mark sheet for test 1"
	@echo "  make pdf 1            Build A4 PDFs for test 1 (言語知識・読解.pdf & 聴解.pdf)"
	@echo "  make mp3 1            Synthesize listening audio for test 1 (聴解.mp3)"
	@echo "  make sample           Sample question pool (item-pool-sampling)"
	@echo "  make merge-seeds      Merge logs/seeds.json into logs/test_spec.json"
	@echo "=========================================================================="

grade:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$(TEST)

grade-%:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$*

template:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$(TEST) --create-template

template-%:
	python3 .agents/exam-answer-grading/scripts/grade_answers.py --test-dir tests/$* --create-template

pdf:
	python3 .agents/exam-pdf-generation/scripts/build_pdf.py tests/$(TEST)/言語知識・読解.md tests/$(TEST)/聴解.md

pdf-%:
	python3 .agents/exam-pdf-generation/scripts/build_pdf.py tests/$*/言語知識・読解.md tests/$*/聴解.md

mp3:
	python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/$(TEST)/聴解スクリプト.txt

mp3-%:
	python3 .agents/choukai-mp3-generation/scripts/make_choukai_mp3.py tests/$*/聴解スクリプト.txt

sample:
	python3 .agents/item-pool-sampling/scripts/sample_items.py --seed $(SEED)

merge-seeds:
	python3 .agents/web-topic-research/scripts/merge_seeds.py logs/seeds.json logs/test_spec.json
