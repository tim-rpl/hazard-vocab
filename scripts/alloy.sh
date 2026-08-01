#!/usr/bin/env bash
# Run an Alloy model headless and translate its output into an exit code.
#
# Alloy's exit status does not distinguish "assertion holds" from
# "counterexample found" — both are a successful JVM run. For a `check`
# command a counterexample means the assertion is FALSE, which for us is
# a failure, so we parse the output.
#
# Resolution order:
#   1. $ALLOY_BIN                     explicit override
#   2. Alloy.app/Contents/MacOS/alloy native CLI launcher (macOS .pkg)
#   3. $ALLOY_JAR                     explicit jar, run with bundled or system java
#   4. jar in common locations
#
# Note: the macOS bundle ships BOTH `alloy` (CLI) and `alloy-gui` (GUI).
# Use the former. It carries its own JRE under Contents/runtime/.

set -uo pipefail

APP=""
for a in /Applications/Alloy.app "$HOME/Applications/Alloy.app"; do
  [[ -d "$a" ]] && { APP="$a"; break; }
done
[[ -z "$APP" ]] && APP="$(find /Applications "$HOME/Applications" -maxdepth 2 -name 'Alloy.app' 2>/dev/null | head -1)"

RUNNER=()

if [[ -n "${ALLOY_BIN:-}" && -x "${ALLOY_BIN}" ]]; then
  RUNNER=("$ALLOY_BIN")
elif [[ -n "$APP" && -x "$APP/Contents/MacOS/alloy" ]]; then
  RUNNER=("$APP/Contents/MacOS/alloy")
else
  JAR="${ALLOY_JAR:-}"
  if [[ -z "$JAR" ]]; then
    for p in \
      "$APP/Contents/Resources/org.alloytools.alloy.dist.jar" \
      "$HOME/.alloy/org.alloytools.alloy.dist.jar" \
      "$HOME/Downloads/org.alloytools.alloy.dist.jar" \
      "/usr/local/lib/alloy/org.alloytools.alloy.dist.jar"
    do
      [[ -f "$p" ]] && { JAR="$p"; break; }
    done
  fi
  if [[ -z "$JAR" ]]; then
    echo "alloy: no launcher or jar found." >&2
    echo "  Set ALLOY_BIN=/Applications/Alloy.app/Contents/MacOS/alloy" >&2
    echo "  or  ALLOY_JAR=/path/to/org.alloytools.alloy.dist.jar" >&2
    exit 127
  fi
  JAVA="java"
  [[ -x "$APP/Contents/runtime/Contents/Home/bin/java" ]] && \
    JAVA="$APP/Contents/runtime/Contents/Home/bin/java"
  RUNNER=("$JAVA" -jar "$JAR")
fi

MODEL="${1:-design/alloy/parts.als}"
[[ -f "$MODEL" ]] || { echo "alloy: no such model: $MODEL" >&2; exit 1; }

echo "runner: ${RUNNER[*]}"
echo "model:  $MODEL"
echo "output: ./$(basename "${MODEL%.*}")/"
echo

# NOTE: `exec` writes its output directory to the CURRENT WORKING
# DIRECTORY, named after the model file's basename minus extension —
# not alongside the model. design/alloy/parts.als produces ./parts/.
# It refuses to overwrite a non-empty directory, hence -f.
#
# `exec` prints one line per command:
#     NN. check <name>   1/1   SAT
#     NN. run   <name>   1/1   UNSAT
#
# Alloy semantics, which invert the intuitive reading:
#   check + SAT    counterexample FOUND  -> assertion is FALSE  -> FAIL
#   check + UNSAT  no counterexample     -> holds in scope      -> pass
#   run   + SAT    instance found        -> expected            -> pass
#   run   + UNSAT  predicate unsatisfiable -> usually an over-constrained
#                  model, not a result   -> WARN
#
# Convention: a command named demo_* is EXPECTED to be SAT. Such commands
# exist to exhibit the counterexample that justifies a rule.

OUTDIR="$(basename "${MODEL%.*}")"

out="$("${RUNNER[@]}" exec -f "$MODEL" 2>&1)"
status=$?
echo "$out"
echo

if [[ $status -ne 0 ]]; then
  echo "FAIL: alloy exited $status." >&2
  echo "Discover sub-commands with: ${RUNNER[*]} help" >&2
  exit $status
fi

fail=0; warn=0; seen=0

while read -r line; do
  kind=$(awk '{print $2}' <<< "$line")
  name=$(awk '{print $3}' <<< "$line")
  verdict=$(awk '{print $NF}' <<< "$line")
  [[ "$kind" == "check" || "$kind" == "run" ]] || continue
  seen=$((seen+1))

  if [[ "$kind" == "check" ]]; then
    if [[ "$name" == demo_* ]]; then
      if [[ "$verdict" == "SAT" ]]; then
        echo "  ok    $name — counterexample exhibited as intended"
      else
        echo "  WARN  $name — expected a counterexample, found none. The rule it justifies may be unnecessary, or the model no longer exercises it." >&2
        warn=$((warn+1))
      fi
    elif [[ "$verdict" == "SAT" ]]; then
      echo "  FAIL  $name — counterexample found; assertion does not hold" >&2
      fail=$((fail+1))
    else
      echo "  pass  $name — no counterexample in scope"
    fi
  else
    if [[ "$verdict" == "SAT" ]]; then
      echo "  ok    $name — instance found"
    else
      echo "  WARN  $name — no instance; predicate is unsatisfiable (over-constrained model?)" >&2
      warn=$((warn+1))
    fi
  fi
done <<< "$out"

echo
if [[ $seen -eq 0 ]]; then
  echo "WARN: no commands parsed. Output format may have changed." >&2
  exit 0
fi
echo "NOTE: scope-bounded. Absence of a counterexample at small scope is"
echo "      evidence, not proof. Do not record a claim as \`tested\` on"
echo "      this alone without saying the scope."
[[ $fail -gt 0 ]] && { echo "FAILED: $fail assertion(s)." >&2; exit 1; }
[[ $warn -gt 0 ]] && echo "$warn warning(s)." >&2
exit 0