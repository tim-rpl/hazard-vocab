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
import argparse
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
FIX = HERE / "lint-fixtures"
LINT = HERE / "drift-lint.py"
LEAN_LINT = HERE / "lean-lint.py"
LEAN_FIX = HERE / "lean-fixtures"

# (rule, fixture, must_fire, why[, expect])
#
# `expect` is an optional substring the failure message must contain.
# Without it "the fixture fired" cannot be distinguished from "the
# fixture fired for the reason it is named for" — a coincidence and a
# true positive are the same green. Splitting a bundled fixture is not
# enough on its own: the exit code is one bit and a file with several
# routes to failure spends it on whichever route survives.
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
    ("shared-uri",        "shared-class-uri",    True,  "recall — C21/B4, two classes on one class_uri", "class_uri"),
    ("shared-uri",        "shared-slot-uri",     True,  "recall — the slot branch, which no fixture reached", "slot_uri"),
    ("shared-uri",        "mixed-construct-identity", True, "recall — BV3-3, exact_mappings vs another class_uri", "exact_mappings"),
    ("shared-uri",        "collision-class-vs-slot", True, "recall — cross-population; kills the one-map repair", "slot `wasAttributedTo`"),
    ("shared-uri",        "collision-same-as",   True,  "recall — reached only through same_as", "same_as"),
    ("shared-uri",        "collision-permissible-meaning", True, "recall — two PermissibleValue.meaning on one URI", "meaning"),
    ("shared-uri",        "near-miss-distinct-uris", False, "precision — distinct URIs; one element naming one URI twice is not a collision"),
    ("exact-mappings",    "mixed-construct-identity", False, "precision — one exact_mappings each, not a len>1 case"),
    ("shared-uri",        "own-namespace",       False, "precision — distinct URIs"),
    ("shared-uri",        "bound-vocabularies",  False, "precision — one class, external bindings"),
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


def validate_cases() -> list[str]:
    """Reject a case row whose fields cannot all take effect.

    `expect` is only evaluated when a row must fire, so a precision row
    carrying one is accepted silently and never checked — a field that
    cannot fire, one edit from being load-bearing. That is the defect
    `expect` was added to close, in `expect` itself. Rejected at load
    rather than ignored at use.
    """
    bad = []
    for i, case in enumerate(CASES):
        if len(case) > 5:
            bad.append(f"CASES[{i}] has {len(case)} fields; max is 5 "
                       f"(rule, fixture, must_fire, why, expect)")
            continue
        if len(case) == 5 and not case[2]:
            bad.append(
                f"CASES[{i}] ({case[0]}/{case[1]}) is a precision row "
                f"(must_fire=False) carrying expect={case[4]!r}. `expect` "
                f"asserts WHY a rule fired and a precision row asserts it "
                f"does not fire, so the field could never be evaluated. "
                f"Drop it, or make the row a recall row")
    for i, case in enumerate(LEAN_CASES):
        if len(case) != 4:
            bad.append(f"LEAN_CASES[{i}] must have exactly 4 fields")
    return bad


MARK_START = "<!-- BEGIN GENERATED:fixtures -->"
MARK_END = "<!-- END GENERATED:fixtures -->"


def fixture_table() -> str:
    """Render the fixture coverage matrix from CASES.

    Generated, not typed. A hand-maintained table keyed by fixture name,
    sitting beside the list it describes, is the defect this project
    spent four gate rounds on — the corrected version in one place and
    the residue in the summary a reader takes the position from. The
    README's table went four fixtures stale within one gate.
    """
    rows = {}
    for case in CASES:
        rule, fixture, must_fire, why = case[:4]
        rows.setdefault(fixture, []).append(
            (rule, "recall" if must_fire else "precision", why))
    for rule, fixture, must_fire, why in LEAN_CASES:
        rows.setdefault(fixture + " (.lean)", []).append(
            (rule, "recall" if must_fire else "precision", why))

    out = ["| Fixture | Rule | Direction | What it regresses |",
           "|---|---|---|---|"]
    for fixture in sorted(rows):
        for rule, direction, why in sorted(rows[fixture]):
            note = why.split("—", 1)[-1].strip() if "—" in why else why
            out.append(f"| `{fixture}` | `{rule}` | {direction} | {note} |")
    n_rules = len({c[0] for c in CASES} | {c[0] for c in LEAN_CASES})
    out.append("")
    out.append(f"*{len(CASES) + len(LEAN_CASES)} rule/fixture pairs across "
               f"{len(rows)} fixtures and {n_rules} rules. "
               f"Generated by `lint-selftest.py --table`; "
               f"`make lint-selftest` fails if this block is stale.*")
    return "\n".join(out)


def sync_readme(check_only: bool) -> int:
    readme = FIX / "README.md"
    if not readme.exists():
        print(" FAIL  scripts/lint-fixtures/README.md is missing")
        return 1
    text = readme.read_text()
    if MARK_START not in text or MARK_END not in text:
        print(f" FAIL  README.md has no {MARK_START} block — the fixture "
              f"table must be generated, not typed")
        return 1
    block = f"{MARK_START}\n\n{fixture_table()}\n\n{MARK_END}"
    new = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
                 lambda _: block, text, flags=re.S)
    if new == text:
        return 0
    if check_only:
        print(" FAIL  scripts/lint-fixtures/README.md fixture table is stale "
              "— run `lint-selftest.py --table --write`")
        return 1
    readme.write_text(new)
    print("  ok   README.md fixture table regenerated")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true",
                    help="sync the README fixture table")
    ap.add_argument("--write", action="store_true",
                    help="with --table, write instead of checking")
    args = ap.parse_args()

    invalid = validate_cases()
    if invalid:
        for m in invalid:
            print(f" FAIL  {m}")
        return 1

    if args.table:
        return sync_readme(check_only=not args.write)

    failures = []
    for case in CASES:
        rule, fixture, must_fire, why = case[:4]
        expect = case[4] if len(case) > 4 else None
        path = FIX / f"{fixture}.yaml"
        if not path.exists():
            failures.append(f"[{rule}] fixture missing: {path}")
            continue
        r = subprocess.run(
            [sys.executable, str(LINT), "--only", rule, "--quiet", str(path)],
            capture_output=True, text=True)
        fired = r.returncode != 0
        ok = fired == must_fire
        reason_ok = True
        if ok and must_fire and expect:
            reason_ok = expect in r.stdout
        mark = "  ok  " if (ok and reason_ok) else " FAIL "
        suffix = f"  [message must mention: {expect}]" if expect else ""
        print(f"{mark} [{rule}] {fixture}.yaml — {why}{suffix}")
        if not ok:
            failures.append(
                f"[{rule}] {fixture}.yaml: expected "
                f"{'a violation' if must_fire else 'no violation'}, got the opposite"
                + (f"\n        {r.stdout.strip()}" if r.stdout.strip() else ""))
        elif not reason_ok:
            failures.append(
                f"[{rule}] {fixture}.yaml: fired, but not for the reason it is "
                f"named for — message does not mention {expect!r}. A fixture "
                f"that fires coincidentally is indistinguishable from one that "
                f"fires correctly unless the message is checked."
                + (f"\n        {r.stdout.strip()}" if r.stdout.strip() else ""))

    # Every fixture must be referenced by at least one case. An
    # unreferenced fixture is a test nobody runs, and it would sit in
    # the directory looking like coverage.
    on_disk = {p.stem for p in FIX.glob("*.yaml")}
    referenced = {c[1] for c in CASES}
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
    with_recall = {c[0] for c in CASES if c[2]}
    unexercised = [r for r in rules if r not in with_recall]
    if unexercised:
        print(f"\n  NOTE: no recall case for: {', '.join(unexercised)} — "
              f"these rules have never been shown to catch anything (C18)")

    if sync_readme(check_only=True):
        failures.append("README fixture table is stale")

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