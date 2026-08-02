#!/usr/bin/env python3
"""Declarative-drift and jurisdiction lints for LinkML schemas.

Replaces the grep/awk rules that lived in the Makefile. Those produced
four false positives and two recall failures across their short life —
every one of them a consequence of pattern-matching text instead of
reading structure. See claims.md C18 and the [O -> H] measure gate,
findings F1-F4.

Each rule reports independently. A failure in one does not prevent the
others from running, which was F1: `make` aborts a recipe on the first
failing line, so a four-line recipe reported one rule's health as four.

Usage:
    drift-lint.py PATH...            lint files or directories
    drift-lint.py --rules            list rule ids
    drift-lint.py --only RULE PATH   run a single rule (used by selftest)

Exit 0 if every rule passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "drift-lint: PyYAML not installed. Activate .venv or `pip install pyyaml`.\n"
    )
    sys.exit(127)

MAX_IS_A_DEPTH = 2

ROLE_NOUNS = {
    "exposedelement", "resource", "responder", "evacuee", "observer",
    "reporter", "victim", "owner", "operator", "requester", "provider",
    "sender", "recipient", "assignee", "custodian",
}

# C1: jurisdiction-specific content must not appear in the core.
#
# A DENYLIST OF AGENCY NAMES DOES NOT GENERALISE. The first version of
# this rule carried `nwcg`, `irwin`, `airnow`, `wfigs` and so on -- a
# US-wildfire list, derived from one reference implementation. A flood
# profile using `DWD` or a seismic one using `JMA` would have passed
# clean. That is the failure C1 exists to prevent, committed inside
# C1's own guard.
#
# Domain-neutral test instead: jurisdiction-specific identifier schemes
# are almost always ACRONYMS; generic core concepts almost never are.
# `AQSID`, `IRWIN`, `NWCG`, `DWD`, `JMA`, `INSEE` are caught without
# naming any of them. `Asset`, `Place`, `Observation` are not.
#
# The allowlist below is only for acronyms that are themselves
# international and domain-neutral. Adding a national scheme to it
# defeats the rule -- put the scheme in vocab/profiles/ instead.
ACRONYM = re.compile(r"^[A-Z][A-Z0-9]{1,7}$")

GENERIC_ACRONYMS = {
    # identity and encoding
    "ID", "IDS", "URI", "URL", "IRI", "UUID", "URN", "UTF8",
    # time
    "UTC", "TAI", "GMT", "ISO8601",
    # space
    "CRS", "SRS", "WKT", "GML", "WGS84", "EPSG", "DEM", "DGGS",
    # generic standards bodies and formats these parts already cite
    "ISO", "OGC", "W3C", "RDF", "OWL", "SKOS", "SHACL", "XSD",
    "JSON", "XML", "CSV", "SI", "QUDT", "PROV", "SOSA", "SSN",
    # measurement
    "MIN", "MAX", "AVG", "SUM", "STDDEV", "NA", "NIL",
}


def load(path: pathlib.Path):
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as exc:
        return {"__parse_error__": str(exc)}


def schema_files(paths):
    out = []
    for p in paths:
        p = pathlib.Path(p)
        if p.is_dir():
            out += sorted(list(p.rglob("*.yaml")) + list(p.rglob("*.yml")))
        elif p.suffix in (".yaml", ".yml"):
            out.append(p)
    return out


# --------------------------------------------------------------- rules

def rule_inline_attributes(path, doc):
    """C19: slots are first-class. No inline `attributes:` on a class."""
    bad = []
    for name, cls in (doc.get("classes") or {}).items():
        if isinstance(cls, dict) and cls.get("attributes"):
            bad.append(f"{path}: class `{name}` uses inline `attributes:` — "
                       f"declare a top-level slot and reference it")
    return bad


def rule_is_a_depth(path, doc):
    """C19: `is_a` CHAIN DEPTH <= 2.

    F2: the previous rule counted `is_a` declarations per file. Three
    siblings under one abstract base is depth 1 and was rejected — the
    exact shape of the Part 0 entity core, i.e. compliant content.
    """
    classes = doc.get("classes") or {}
    parents = {n: (c or {}).get("is_a") for n, c in classes.items()
               if isinstance(c, dict)}
    bad = []
    for name in classes:
        depth, seen, cur = 0, {name}, parents.get(name)
        while cur:
            depth += 1
            if cur in seen:
                bad.append(f"{path}: class `{name}` has a cyclic `is_a` chain")
                break
            seen.add(cur)
            if cur not in parents:      # parent defined elsewhere
                break
            cur = parents.get(cur)
        else:
            if depth > MAX_IS_A_DEPTH:
                bad.append(f"{path}: class `{name}` has is_a chain depth "
                           f"{depth} (max {MAX_IS_A_DEPTH}) — prefer mixins")
    return bad


def rule_exact_mappings(path, doc):
    """C19: at most one `exact_mappings` per class.

    Two assert the targets are equivalent to each other — the
    sosa:Platform == sosa:Sensor bug in ADR-002.

    F3: the previous awk missed the violation when the mappings list
    ended the file, because it only tested on the next non-list line.
    """
    bad = []
    for name, cls in (doc.get("classes") or {}).items():
        if not isinstance(cls, dict):
            continue
        m = cls.get("exact_mappings") or []
        if len(m) > 1:
            bad.append(f"{path}: class `{name}` has {len(m)} exact_mappings "
                       f"({', '.join(map(str, m))}) — this asserts they are "
                       f"equivalent to each other. Use close_ or related_")
    return bad


def rule_role_named(path, doc):
    """C7: roles are relations, not classes."""
    bad = []
    for name in (doc.get("classes") or {}):
        if name.lower() in ROLE_NOUNS:
            bad.append(f"{path}: class `{name}` is named for a role — "
                       f"entities are declared once, roles ride on relations")
    return bad


def rule_jurisdiction(path, doc):
    """C1: no jurisdiction-specific content in vocab/core/.

    Matches identifiers, not prose (F4), and by shape rather than by a
    denylist of agency names, so it generalises to hazards and
    jurisdictions this project has never seen.

    Known limitation, stated: this is a heuristic proxy. The real test
    is whether an identifier is declared by some profile, which cannot
    be run until profiles exist. A jurisdiction-specific scheme with a
    non-acronym name passes. Recorded against C1.
    """
    bad = []

    def check(kind, name):
        n = str(name)
        if ACRONYM.match(n) and n not in GENERIC_ACRONYMS:
            bad.append(f"{path}: {kind} `{n}` is an acronym and not a "
                       f"generic international term — jurisdiction-specific "
                       f"schemes belong in vocab/profiles/. If this is "
                       f"genuinely domain-neutral, add it to "
                       f"GENERIC_ACRONYMS with a reason")

    for n in (doc.get("classes") or {}):
        check("class", n)
    for n in (doc.get("slots") or {}):
        check("slot", n)
    for n, e in (doc.get("enums") or {}).items():
        check("enum", n)
        for pv in ((e or {}).get("permissible_values") or {}):
            check("permissible value", pv)
    return bad


RULES = {
    "inline-attributes": rule_inline_attributes,
    "is-a-depth": rule_is_a_depth,
    "exact-mappings": rule_exact_mappings,
    "role-named": rule_role_named,
    "jurisdiction": rule_jurisdiction,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--only", help="run a single rule")
    ap.add_argument("--rules", action="store_true", help="list rule ids")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.rules:
        for r in RULES:
            print(r)
        return 0

    files = schema_files(args.paths)
    active = {args.only: RULES[args.only]} if args.only else RULES
    if args.only and args.only not in RULES:
        sys.stderr.write(f"drift-lint: unknown rule `{args.only}`\n")
        return 2

    failed = False
    for rid, fn in active.items():
        problems = []
        for f in files:
            doc = load(f)
            if "__parse_error__" in doc:
                problems.append(f"{f}: YAML parse error: {doc['__parse_error__']}")
                continue
            problems += fn(f, doc)
        if problems:
            failed = True
            for p in problems:
                print(f"FAIL [{rid}] {p}")
        elif not args.quiet:
            print(f"  ok   [{rid}] {len(files)} file(s)")

    if not files and not args.quiet:
        print("  note: no schema files found — these rules inspected nothing")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())