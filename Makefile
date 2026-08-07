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
	@# vocab/core/ and vocab/profiles/ only. Scanning vocab/ reaches
	@# vocab/external/, where cached graphs and their .yaml provenance
	@# sidecars live — content this rule is not about.
	@#
	@# grep has THREE exit codes and `! grep ... 2>/dev/null` conflates
	@# them: 1 is no-match (pass), 2 is an error (must fail), and
	@# suppressing stderr then inverting turns an error into a pass
	@# having inspected nothing. Rename a target directory and the rule
	@# goes green. Same shape as the ** glob in make check.
	@for d in vocab/core vocab/profiles; do \
		test -d "$$d" || { echo "FAIL: $$d is missing — C4 inspected nothing"; exit 1; }; \
	done
	@out=$$(grep -rnE --include='*.yaml' --include='*.yml' \
			'structured_pattern|classification_rules' \
			vocab/core/ vocab/profiles/); rc=$$?; \
	if [ $$rc -eq 2 ]; then \
		echo "FAIL: grep errored — C4 inspected nothing"; exit 1; \
	elif [ $$rc -eq 0 ]; then \
		echo "$$out"; \
		echo "FAIL: non-portable construct (see claims.md C4)"; exit 1; \
	fi
	@echo "L: no vacuous theorems in design/lean"
	@$(BIN)python scripts/lean-lint.py design/lean
	@echo "jurisdiction and declarative-drift rules — C1, C7, C20, C21"
	@# C19 was never filed. This label cited it for several gates; the
	@# rules serve the four claims above. A tool citing a claim that
	@# does not exist sends a reader nowhere.
	@$(BIN)python scripts/drift-lint.py vocab/core/
	@echo "P: the wave view is derived from the item table"
	@test -f docs/plan/derive-waves.py \
		|| { echo "FAIL: docs/plan/derive-waves.py is missing — this check inspected nothing, and the file is tracked"; exit 1; }
	@$(BIN)python docs/plan/derive-waves.py --check
	@echo "S: the surface counts are derived from design/surface.yaml"
	@test -f design/derive-surface.py \
		|| { echo "FAIL: design/derive-surface.py is missing — this check inspected nothing, and the file is tracked"; exit 1; }
	@$(BIN)python design/derive-surface.py --check
	@echo "X: the external register is what its generator emits"
	@test -f vocab/external/fetch-external.py \
		|| { echo "FAIL: vocab/external/fetch-external.py is missing — this check inspected nothing, and the file is tracked"; exit 1; }
	@$(BIN)python vocab/external/fetch-external.py --check
	@echo "B: bound-terms.md is what its generator emits"
	@# Added after B10, and deliberately after the two repairs it depends
	@# on: this script wrote its own output during --check, and one cell
	@# carried rdflib's per-parse blank-node label, so wiring it earlier
	@# would have failed every run for a reason that is not drift. A
	@# stanza that fails for the wrong reason gets muted, which is worse
	@# than one that is absent.
	@test -f vocab/external/audit-bound-terms.py \
		|| { echo "FAIL: vocab/external/audit-bound-terms.py is missing — this check inspected nothing, and the file is tracked"; exit 1; }
	@$(BIN)python vocab/external/audit-bound-terms.py --check
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