# Resolve tools from .venv when present, so `make` uses the environment
# that was set up rather than whatever happens to be first on PATH.
VENV := $(CURDIR)/.venv
BIN  := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/,)

.PHONY: all gen check lint lean alloy clean env role role-o role-h

all: gen lint check

gen:
	@mkdir -p build
	$(BIN)gen-project -d build vocab/core/vocabulary.yaml
	$(BIN)gen-shacl vocab/core/vocabulary.yaml > build/shapes.ttl
	@echo "generated -> build/"

check:
	$(BIN)pyshacl -s build/shapes.ttl -df json-ld fixtures/**/*.jsonld

lint:
	@echo "C1: no jurisdiction-specific content in core"
	@! grep -rniE '\b(nwcg|irwin|nifc|fema|ornl|airnow|noaa|usgs|epa|landfire|nhd|iroc|wfigs|wfdss|inspire-eu)\b' vocab/core/ \
		|| (echo "FAIL: agency reference in vocab/core/ (see claims.md C1)"; exit 1)
	@echo "C4: no LinkML-only constructs"
	@! grep -rnE 'structured_pattern|classification_rules' vocab/ \
		|| (echo "FAIL: non-portable construct (see claims.md C4)"; exit 1)
	@echo "lint ok"

lean:
	cd design/lean && lake build

alloy:
	@./scripts/alloy.sh design/alloy/parts.als

env:
	@printf 'python:  '; if [ -n "$(BIN)" ]; then echo "$(BIN)python  [.venv]"; \
		else echo "$$(command -v python3)  [SYSTEM — no .venv]"; fi
	@printf 'linkml:  '; $(BIN)gen-project --version 2>/dev/null || echo 'not found'
	@printf 'pyshacl: '; $(BIN)pyshacl --version 2>&1 | head -1 || echo 'not found'
	@printf 'lean:    '; (cd design/lean && lake --version 2>/dev/null | head -1) || echo 'not found'
	@printf 'alloy:   '; ls -d $$HOME/Applications/Alloy.app /Applications/Alloy.app 2>/dev/null | head -1 || echo 'not found'
	@printf 'role:    '; if [ -f .role-O ]; then echo 'O  (overseer)'; else echo 'H  (builder)'; fi

clean:
	rm -rf build/
	@# alloy exec writes ./<model-basename>/ at the repo root
	@for m in design/alloy/*.als; do \
		d="$$(basename "$${m%.*}")"; \
		[ -n "$$d" ] && [ -d "$$d" ] && rm -rf "$$d" && echo "removed ./$$d/"; \
	done; true

role:
	@if [ -f .role-O ]; then echo "O  (overseer)"; else echo "H  (builder)"; fi

role-o:
	@echo "NOTE: this is project-global. If an H session is open anywhere,"
	@echo "      it will start being blocked mid-task. Prefer, from a terminal:"
	@echo "        HV_ROLE=O claude"
	@echo ""
	@touch .role-O
	@echo "role: O — design/ blocked; writes limited to claims.md and review-inbox.md"
	@echo "Start a NEW Claude Code session. Do not reuse the H panel."

role-h:
	@rm -f .role-O
	@echo "role: H — full access restored"