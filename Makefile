# Resolve tools from .venv when present, so `make` uses the environment
# that was set up rather than whatever happens to be first on PATH.
VENV := $(CURDIR)/.venv
BIN  := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/,)

.PHONY: all gen check lint lint-selftest lean alloy clean env role role-o role-h


all: gen lint check

gen:
	@mkdir -p build
	$(BIN)gen-project -d build vocab/core/vocabulary.yaml
	$(BIN)gen-shacl vocab/core/vocabulary.yaml > build/shapes.ttl
	@echo "generated -> build/"

# Instance validation. Enumerated with `find`, not a glob.
#
# `fixtures/**/*.jsonld` is expanded by sh, which has no `**` — it matches
# exactly one directory level, so a fixture written to `fixtures/x.jsonld`
# or `fixtures/a/b/x.jsonld` is SILENTLY SKIPPED and this target reports
# success. Measured. That is the C17 shape in the one target whose whole
# job is to inspect instances.
#
# The count is printed for the same reason `make lint` prints what it
# inspected: a validator that passes over zero files must not look like a
# validator that passed.
check:
	@test -f build/shapes.ttl || \
		(echo "FAIL: build/shapes.ttl does not exist. Run 'make gen' first."; exit 1)
	@n=$$(find fixtures -name '*.jsonld' 2>/dev/null | wc -l | tr -d ' '); \
	if [ "$$n" -eq 0 ]; then \
		echo "FAIL: no *.jsonld under fixtures/ — this target inspected nothing."; \
		echo "      An empty pass is not a pass. See claims.md C17."; \
		exit 1; \
	fi; \
	echo "checking $$n instance file(s) against build/shapes.ttl"; \
	find fixtures -name '*.jsonld' -print0 \
		| xargs -0 $(BIN)pyshacl -s build/shapes.ttl -df json-ld

lint:
	@echo "C4: no LinkML-only constructs"
	@! grep -rnE --include='*.yaml' --include='*.yml' 'structured_pattern|classification_rules' vocab/ \
		|| (echo "FAIL: non-portable construct (see claims.md C4)"; exit 1)
	@echo "L: no vacuous theorems in design/lean"
	@$(BIN)python scripts/lean-lint.py design/lean
	@echo "C1 + C19: jurisdiction and declarative-drift rules"
	@$(BIN)python scripts/drift-lint.py vocab/core/
	@echo "P: the wave view is derived from the item table"
	@if [ -f docs/plan/derive-waves.py ]; then \
		$(BIN)python docs/plan/derive-waves.py --check; \
	else echo "  skip — docs/plan/derive-waves.py not present"; fi
	@echo "lint ok"

lint-selftest:
	@echo "Exercising each rule independently. See claims.md C18 and F1-F4."
	@$(BIN)python scripts/lint-selftest.py


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
	@printf 'role:    '; if [ "$${HV_ROLE:-}" = "O" ]; then echo 'O  (overseer, via HV_ROLE)'; \
		elif [ -f .role-O ]; then echo 'O  (overseer, via .role-O marker)'; else echo 'H  (builder)'; fi

clean:
	rm -rf build/
	@# alloy exec writes ./<model-basename>/ at the repo root
	@for m in design/alloy/*.als; do \
		d="$$(basename "$${m%.*}")"; \
		[ -n "$$d" ] && [ -d "$$d" ] && rm -rf "$$d" && echo "removed ./$$d/"; \
	done; true

role:
	@if [ "$${HV_ROLE:-}" = "O" ] || [ -f .role-O ]; then echo "O  (overseer)"; else echo "H  (builder)"; fi

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