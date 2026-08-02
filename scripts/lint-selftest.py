#!/usr/bin/env python3
"""Exercise each drift-lint rule independently against known fixtures.

F1: the previous selftest ran four rules as four Makefile recipe lines.
`make` aborts on the first failure, so rules 2-4 never executed and the
selftest reported one rule's health as four. Every rule/fixture pair is
now its own invocation with an expected outcome.

Each row is a recall test (the rule must fire) or a precision test (the
rule must not fire). A rule with no recall row has never been shown to
catch anything — see claims.md C18.
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
FIX = HERE / "lint-fixtures"
LINT = HERE / "drift-lint.py"

# (rule, fixture, must_fire, why)
CASES = [
    ("inline-attributes", "violating",           True,  "recall"),
    ("is-a-depth",        "violating",           True,  "recall — chain depth 3"),
    ("exact-mappings",    "violating",           True,  "recall"),
    ("role-named",        "violating",           True,  "recall"),
    ("exact-mappings",    "mappings-at-eof",     True,  "recall — F3, list ends the file"),
    ("jurisdiction",      "jurisdiction-in-enum", True, "recall — F4, no agency in prose"),
    ("jurisdiction",      "jurisdiction-foreign", True, "recall — a hazard/country never seen here"),

    ("inline-attributes", "clean",               False, "precision"),
    ("is-a-depth",        "clean",               False, "precision"),
    ("exact-mappings",    "clean",               False, "precision"),
    ("role-named",        "clean",               False, "precision"),
    ("jurisdiction",      "clean",               False, "precision"),
    ("is-a-depth",        "flat-siblings",       False, "precision — F2, Part 0 shape"),
    ("role-named",        "flat-siblings",       False, "precision"),
    ("jurisdiction",      "flat-siblings",       False, "precision"),
    ("jurisdiction",      "generic-acronyms",    False, "precision — CRS, UTC, EPSG are not jurisdictions"),
]


def main() -> int:
    failures = []
    for rule, fixture, must_fire, why in CASES:
        path = FIX / f"{fixture}.yaml"
        if not path.exists():
            failures.append(f"[{rule}] fixture missing: {path}")
            continue
        r = subprocess.run(
            [sys.executable, str(LINT), "--only", rule, "--quiet", str(path)],
            capture_output=True, text=True)
        fired = r.returncode != 0
        ok = fired == must_fire
        mark = "  ok  " if ok else " FAIL "
        print(f"{mark} [{rule}] {fixture}.yaml — {why}")
        if not ok:
            failures.append(
                f"[{rule}] {fixture}.yaml: expected "
                f"{'a violation' if must_fire else 'no violation'}, got the opposite"
                + (f"\n        {r.stdout.strip()}" if r.stdout.strip() else ""))

    rules = subprocess.run([sys.executable, str(LINT), "--rules"],
                           capture_output=True, text=True).stdout.split()
    with_recall = {r for r, _, f, _ in CASES if f}
    unexercised = [r for r in rules if r not in with_recall]
    if unexercised:
        print(f"\n  NOTE: no recall case for: {', '.join(unexercised)} — "
              f"these rules have never been shown to catch anything (C18)")

    if failures:
        print("\nlint-selftest FAILED:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"\nlint-selftest ok — {len(CASES)} rule/fixture pairs, "
          f"{len(with_recall)}/{len(rules)} rules with demonstrated recall")
    return 0


if __name__ == "__main__":
    sys.exit(main())