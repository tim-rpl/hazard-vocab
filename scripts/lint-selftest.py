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
LEAN_LINT = HERE / "lean-lint.py"
LEAN_FIX = HERE / "lean-fixtures"

# (rule, fixture, must_fire, why)
CASES = [
    ("inline-attributes", "violating",           True,  "recall"),
    ("is-a-depth",        "violating",           True,  "recall — chain depth 3"),
    ("exact-mappings",    "violating",           True,  "recall"),
    ("role-named",        "violating",           True,  "recall"),
    ("exact-mappings",    "mappings-at-eof",     True,  "recall — F3, list ends the file"),
    ("jurisdiction",      "jurisdiction-in-enum", True, "recall — F4, no agency in prose"),
    ("jurisdiction",      "jurisdiction-foreign", True, "recall — a hazard/country never seen here"),
    ("jurisdiction",      "jurisdiction-in-uri", True,  "recall — F12, generic names, agency in the URI"),
    ("jurisdiction",      "redirect-service",    True,  "recall — F13 c1/c2, w3id.org and purl.org"),
    ("jurisdiction",      "long-acronym",        True,  "recall — F13 c3, past every guessed bound"),

    ("inline-attributes", "clean",               False, "precision"),
    ("is-a-depth",        "clean",               False, "precision"),
    ("exact-mappings",    "clean",               False, "precision"),
    ("role-named",        "clean",               False, "precision"),
    ("jurisdiction",      "clean",               False, "precision"),
    ("is-a-depth",        "flat-siblings",       False, "precision — F2, Part 0 shape"),
    ("role-named",        "flat-siblings",       False, "precision"),
    ("jurisdiction",      "flat-siblings",       False, "precision"),
    ("jurisdiction",      "generic-acronyms",    False, "precision — CRS, UTC, EPSG are not jurisdictions"),
    ("jurisdiction",      "bound-vocabularies",  False, "precision — F11, every vocabulary CLAUDE.md binds"),
    ("jurisdiction",      "own-namespace",       False, "precision — BV8, the project's own id: and default_prefix"),
    ("jurisdiction",      "default-prefix-escape", True, "recall — BV14, default_prefix nominating a foreign namespace"),
    ("jurisdiction",      "id-claims-foreign-namespace", True, "recall — F13 redirect rule; does NOT reach the id: gate (BV25)"),
    ("jurisdiction",      "default-prefix-ancestor", True, "recall — BV23, default_prefix naming an ancestor of id:"),
    ("jurisdiction",      "id-branch-only",      True,  "recall — BV25, the ONLY case reaching the id: gate"),
    ("documented",        "undocumented",        True,  "recall — C20, placeholder descriptions and no examples"),
    ("documented",        "own-namespace",       False, "precision — a documented file with examples"),
]


# Lean vacuity rule. Separate binary, same discipline: a guard nobody
# exercises is a guard that has only ever been observed being wrong.
# (rule, fixture, must_fire, why)
LEAN_CASES = [
    ("lean-vacuity", "vacuous-theorem",          True,
     "recall — a theorem concluding True"),
    ("lean-vacuity", "comment-mentions-pattern", False,
     "precision — BR-7, the pattern written out in a comment"),
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

    # Every fixture must be referenced by at least one case. An
    # unreferenced fixture is a test nobody runs, and it would sit in
    # the directory looking like coverage.
    on_disk = {p.stem for p in FIX.glob("*.yaml")}
    referenced = {f for _, f, _, _ in CASES}
    orphans = sorted(on_disk - referenced)
    missing = sorted(referenced - on_disk)
    if orphans:
        print()
        for o in orphans:
            print(f" FAIL  fixture `{o}.yaml` is referenced by no case — "
                  f"add a row to CASES or delete it")
        failures.append(f"unreferenced fixtures: {', '.join(orphans)}")
    if missing:
        for m in missing:
            print(f" FAIL  case references `{m}.yaml`, which does not exist")
        failures.append(f"missing fixtures: {', '.join(missing)}")

    for rule, fixture, must_fire, why in LEAN_CASES:
        path = LEAN_FIX / f"{fixture}.lean"
        if not path.exists():
            failures.append(f"[{rule}] fixture missing: {path}")
            continue
        r = subprocess.run([sys.executable, str(LEAN_LINT), str(path)],
                           capture_output=True, text=True)
        fired = r.returncode != 0
        ok = fired == must_fire
        print(f"{'  ok  ' if ok else ' FAIL '} [{rule}] {fixture}.lean — {why}")
        if not ok:
            failures.append(
                f"[{rule}] {fixture}.lean: expected "
                f"{'a violation' if must_fire else 'no violation'}, "
                f"got the opposite")

    # §4 mutation test on the external declaration. BV23: the config
    # file was added, never read, and moving it away changed nothing —
    # while its own header promised to fail loud. Verifying PRESENCE is
    # what a declaration already asserts; this verifies EFFECT.
    pns = HERE / "project-namespaces.txt"
    if pns.exists():
        stash = pns.read_text()
        try:
            pns.unlink()
            r = subprocess.run(
                [sys.executable, str(LINT), "--only", "jurisdiction",
                 "--quiet", str(FIX / "own-namespace.yaml")],
                capture_output=True, text=True)
            if r.returncode == 0:
                print(" FAIL  [jurisdiction] project-namespaces.txt is inert — "
                      "removing it changed no output (BV23)")
                failures.append("project-namespaces.txt has no effect")
            else:
                print("  ok   [jurisdiction] project-namespaces.txt — "
                      "removing it makes the guard fail loud (BV23 mutation)")
        finally:
            pns.write_text(stash)
    else:
        print(" FAIL  scripts/project-namespaces.txt is missing")
        failures.append("project-namespaces.txt missing")

    lean_on_disk = {p.stem for p in LEAN_FIX.glob("*.lean")}
    lean_orphans = sorted(lean_on_disk - {f for _, f, _, _ in LEAN_CASES})
    if lean_orphans:
        for o in lean_orphans:
            print(f" FAIL  fixture `{o}.lean` is referenced by no case")
        failures.append(f"unreferenced lean fixtures: {', '.join(lean_orphans)}")

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
    total = len(CASES) + len(LEAN_CASES)
    print(f"\nlint-selftest ok — {total} rule/fixture pairs, "
          f"{len(with_recall) + 1}/{len(rules) + 1} rules with demonstrated "
          f"recall (including lean-vacuity)")
    return 0


if __name__ == "__main__":
    sys.exit(main())