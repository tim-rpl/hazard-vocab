#!/usr/bin/env python3
"""Sweep tracked files for verbatim reintroduction of a retracted phrase.

Rule 4 of `.claude/rules/gate-messages.md` — *the retraction sweep
searches the retracted string, not the replacement, and it excludes the
inbox and its archive* — was stated and implemented by nothing. Each
sweep was assembled by whoever ran it, which is the shape `CLAUDE.md`
already rules on: **a check that exists only as a command someone must
remember is not a guard.**

WHAT THIS GUARANTEES: no tracked file outside the exclusions contains a
phrase from `retracted.txt`, byte for byte.

WHAT IT DOES NOT: anything about a paraphrase. claims.md C22 row 12 is
that over-read, measured — three restated claims shipped past a green run
of a string sweep, all three in accepted ADRs. A green here means *these
exact strings are absent*, never *the claim is gone*.

WHY THE EXCLUSIONS ARE ASSERTED AND NOT JUST APPLIED
----------------------------------------------------
Two failure directions, and they are not symmetric.

  forgetting an exclusion  -> history reported as live. Noisy, and the
                              first run corrects it.
  over-excluding           -> LIVE TEXT REPORTED AS HISTORY. Silent. A
                              live claim written into an excluded path is
                              invisible, and no match-direction fixture
                              can show that.

So the exclusion set is checked on every run: each path must exist, and
`--selftest` asserts that a planted phrase inside an excluded path is
NOT reported while the same phrase outside one IS. That is the direction
this project has never exercised.

Cost, measured: five phrases over the whole tree in 0.03s. `git grep -F
-f` takes a patterns file, so the cost is the tree walk and growth of
the list is free.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LIST = HERE / "retracted.txt"
FIX = HERE / "sweep-fixtures"

# Each entry carries the reason it is not optional. See retracted.txt.
EXCLUDE = [
    "review-inbox.md",            # append-only channel; hits are history
    "review-inbox-archive",       # rotated history
    "docs/plan/guard-fixtures",   # retired figures BY CONSTRUCTION
    "scripts/retracted.txt",      # contains every phrase
    "scripts/sweep-fixtures",     # deliberate positives for --selftest
]


def phrases(path: pathlib.Path) -> list[str]:
    out = []
    for line in path.read_text().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line.split("\t")[0].strip())
    return out


def sweep(pats: list[str], root: pathlib.Path,
          exclude: list[str]) -> list[str]:
    if not pats:
        return []
    with tempfile.NamedTemporaryFile("w", suffix=".txt",
                                     delete=False) as fh:
        fh.write("\n".join(pats) + "\n")
        pf = fh.name
    try:
        cmd = ["git", "grep", "-n", "-F", "-f", pf, "--"] + \
              [f":!{e}" for e in exclude]
        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        return [l for l in r.stdout.split("\n") if l.strip()]
    finally:
        pathlib.Path(pf).unlink(missing_ok=True)


def check_exclusions(root: pathlib.Path) -> list[str]:
    """An exclusion naming a path that does not exist is over-exclusion
    that will never be noticed — it silences nothing today and silences
    a whole directory the moment one is created at that name."""
    bad = []
    for e in EXCLUDE:
        if not (root / e).exists():
            bad.append(f"exclusion `{e}` names a path that does not "
                       f"exist — an exclusion that silences nothing today "
                       f"silences a directory the moment one appears "
                       f"there")
    return bad


def selftest(root: pathlib.Path) -> int:
    """Assert BOTH directions, and the second is the point."""
    failures = []
    live = FIX / "live-reintroduction.md"
    excluded = FIX / "inside-an-excluded-path.md"
    for p in (live, excluded):
        if not p.exists():
            print(f" FAIL  sweep fixture missing: {p.name}")
            return 1

    # DERIVED from the fixture, not hardcoded. A literal here put the
    # probe string in this file, so the sweep reported ITSELF — and the
    # fix is the one H has been applying all session: a literal
    # describing DATA must be derived; only a literal describing
    # BEHAVIOUR may stand.
    probe = next(l.strip() for l in live.read_text().split("\n")
                 if l.strip() and not l.startswith("#")
                 and not l.startswith("A tracked") and " " in l.strip()
                 and l.strip().endswith("return"))

    # direction 1 — a phrase outside the exclusions IS reported
    hits = sweep([probe], root, [e for e in EXCLUDE
                                 if e != "scripts/sweep-fixtures"])
    got = any("live-reintroduction.md" in h for h in hits)
    print(f"{'  ok  ' if got else ' FAIL '} [sweep] live-reintroduction.md "
          f"— recall: a phrase in a tracked file is reported")
    if not got:
        failures.append("a live reintroduction was not reported")

    # direction 2 — the same phrase INSIDE an excluded path is NOT
    # reported. This is the direction that fails silently and the only
    # one a fixture can demonstrate.
    hits2 = sweep([probe], root, EXCLUDE)
    quiet = not any("sweep-fixtures" in h for h in hits2)
    print(f"{'  ok  ' if quiet else ' FAIL '} [sweep] "
          f"inside-an-excluded-path.md — the OVER-EXCLUDE direction: an "
          f"excluded path is silent, which is why exclusions are asserted")
    if not quiet:
        failures.append("an excluded path was reported")

    bad = check_exclusions(root)
    for b in bad:
        print(f" FAIL  {b}")
    failures += bad

    if failures:
        print("\nsweep-selftest FAILED:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"\nsweep-selftest ok — 2 directions, "
          f"{len(EXCLUDE)} exclusions all present")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if not LIST.exists():
        print(f"FAIL: {LIST.relative_to(ROOT)} is missing — this check "
              f"inspected nothing, and the file is tracked")
        return 1

    if args.selftest:
        return selftest(ROOT)

    bad = check_exclusions(ROOT)
    for b in bad:
        print(f"FAIL: {b}")
    if bad:
        return 1

    pats = phrases(LIST)
    if not pats:
        print(f"  note: {LIST.name} lists no phrases — this check "
              f"inspected nothing")
        return 0

    hits = sweep(pats, ROOT, EXCLUDE)
    if hits:
        for h in hits:
            print(f"FAIL [retracted] {h}")
        print(f"\nA retracted phrase is live in a tracked file. If the "
              f"text is correct and the phrase is not retracted, remove "
              f"it from {LIST.name} with the reason.")
        return 1
    print(f"  ok   [retracted] {len(pats)} phrase(s), "
          f"{len(EXCLUDE)} exclusion(s) — verbatim only; a paraphrase is "
          f"outside this instrument (claims.md C22 row 12)")
    return 0


if __name__ == "__main__":
    sys.exit(main())