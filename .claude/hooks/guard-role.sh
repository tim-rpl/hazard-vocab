#!/usr/bin/env bash
# Role-based access guard. The session is O (Overseer) when EITHER:
#   - HV_ROLE=O is set in the environment (terminal launch), or
#   - a .role-O marker file exists in the project root (VS Code panel)
# Otherwise the session is H (builder) and this hook is a no-op.
#
#   make role-o    switch to Overseer
#   make role-h    switch back to builder
#   make role      print current role
#
# Exit 2 blocks the tool call and feeds stderr back to the model.

set -euo pipefail
input=$(cat)

role="${HV_ROLE:-}"
if [[ -z "$role" && -f "${CLAUDE_PROJECT_DIR:-.}/.role-O" ]]; then
  role="O"
fi
[[ "$role" != "O" ]] && exit 0

tool=$(printf '%s' "$input" | jq -r '.tool_name // empty')
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')
cmd=$(printf '%s'  "$input" | jq -r '.tool_input.command // empty')

# O must not read design/ — ADRs would anchor it on the reasoning it exists to test.
if [[ "$path" == *design/* ]] || [[ "$cmd" == *design/* ]]; then
  echo "BLOCKED: role O may not access design/. It contains the rationale you exist to test independently. See FALSIFIER.md." >&2
  exit 2
fi

# O writes only to claims.md and review-inbox.md.
case "$tool" in
  Write|Edit|NotebookEdit)
    case "$path" in
      *claims.md|*review-inbox.md) exit 0 ;;
      *) echo "BLOCKED: role O may only write claims.md and review-inbox.md. Do not edit vocab/, codelists/, or transform/. See FALSIFIER.md." >&2
         exit 2 ;;
    esac ;;
esac

exit 0
