#!/usr/bin/env python3
"""Vacuity check for Lean files: no theorem may conclude `True`.

A theorem concluding `True` elaborates with NO warning of any kind — no
`sorry`, no linter message — and states no proposition. See FALSIFIER.md
§4.

WHY THIS IS NOT A GREP. The original rule was `grep ':[[:space:]]*True
[[:space:]]*:='` over `design/lean/`. It matched its own documentation
in `design/lean/README.md`. The fix was `--include='*.lean'`, which was
a workaround: the problem was matching text rather than structure, and
comments are text. It then fired on a header note explaining this very
failure mode — fourth precision failure for one rule, fifth
counterexample to claims.md C18.

Comments are stripped before matching. That is the actual fix: a rule
about theorem statements must not see prose.

Two further failure modes this rule does NOT catch, recorded so the
guard is not mistaken for coverage:
  * a conclusion weakened by other means (`0 = 0`, `x = x`)
  * a theorem proving a hypothesis from itself, which is literally true
    and useless and is the only one of the three that looks like
    completed work
Both are review items. See Merge.lean's header note.
"""
from __future__ import annotations

import pathlib
import re
import sys

VACUOUS = re.compile(r":\s*True\s*:=")


def strip_comments(src: str) -> str:
    """Blank out Lean block and line comments, preserving line numbers."""
    out, i, depth = [], 0, 0
    while i < len(src):
        if src.startswith("/-", i):
            depth += 1
            out.append("  "); i += 2; continue
        if src.startswith("-/", i) and depth:
            depth -= 1
            out.append("  "); i += 2; continue
        if depth:
            out.append("\n" if src[i] == "\n" else " "); i += 1; continue
        if src.startswith("--", i):
            j = src.find("\n", i)
            j = len(src) if j == -1 else j
            out.append(" " * (j - i)); i = j; continue
        out.append(src[i]); i += 1
    return "".join(out)


def main() -> int:
    paths = [pathlib.Path(p) for p in (sys.argv[1:] or ["design/lean"])]
    files = []
    for p in paths:
        files += sorted(p.rglob("*.lean")) if p.is_dir() else [p]

    bad = []
    for f in files:
        for n, line in enumerate(strip_comments(f.read_text()).split("\n"), 1):
            if VACUOUS.search(line):
                bad.append(f"{f}:{n}: theorem concludes `True` — states no "
                           f"proposition and emits no warning. See "
                           f"FALSIFIER.md §4")
    if bad:
        for b in bad:
            print(f"FAIL [lean-vacuity] {b}")
        return 1
    print(f"  ok   [lean-vacuity] {len(files)} file(s), comments excluded")
    return 0


if __name__ == "__main__":
    sys.exit(main())