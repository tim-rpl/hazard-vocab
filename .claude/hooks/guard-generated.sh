#!/usr/bin/env bash
# PreToolUse guard. Exit 2 blocks the tool call; stderr is fed back.
# Enforces CLAUDE.md invariants 1 and 3.

set -euo pipefail
input=$(cat)

tool=$(printf '%s' "$input" | jq -r '.tool_name // empty')
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')

[[ -z "$path" ]] && exit 0

case "$tool" in
  Write|Edit|NotebookEdit) ;;
  *) exit 0 ;;
esac

# Invariant 1 — build/ is generated
if [[ "$path" == *"/build/"* || "$path" == build/* ]]; then
  echo "BLOCKED: build/ is generated from vocab/. Edit the LinkML source and run 'make gen'. (CLAUDE.md invariant 1)" >&2
  exit 2
fi

# Invariant 3 — no Lean extraction into the implementation
if [[ "$path" == *"/transform/"* || "$path" == transform/* ]]; then
  if printf '%s' "$input" | grep -qiE 'extracted from|Mathlib|theorem |lemma '; then
    echo "BLOCKED: transform/ must not contain Lean-derived code. design/ proves; transform/ implements. (CLAUDE.md invariant 3)" >&2
    exit 2
  fi
fi

exit 0
