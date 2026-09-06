# geno-arena shortcuts
PYTHON ?= python3
SCORE  := $(PYTHON) harness/score.py

.PHONY: score score-blind compare blind-generate help

help:
	@echo "Targets:"
	@echo "  make score           # score solutions/ → results/batch-001.*"
	@echo "  make score-blind     # score solutions-blind/ → results/batch-002.*"
	@echo "  make compare         # diff batch-001 vs batch-002 scoreboards"
	@echo "  make blind-generate  # Groq → solutions-blind/ (needs GROQ_API_KEY)"

score:
	$(SCORE) --solutions-root solutions --batch-id batch-001

score-blind:
	$(SCORE) --solutions-root solutions-blind --batch-id batch-002 \
		--agent-note "blind"

compare:
	$(PYTHON) harness/compare_batches.py

blind-generate:
	$(PYTHON) harness/blind_batch.py
