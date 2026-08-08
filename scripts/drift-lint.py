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

KNOWN UPCOMING FAILURE — raw YAML does not resolve `imports:`.

`yaml.safe_load` sees one file. Once vocab/core/ splits into
part0-entities.yaml, part0-foundation.yaml, part2-observation.yaml with
imports between them:

  * `is-a-depth` EXEMPTS a class whose parent is declared in another
    file — from the rule entirely, at any depth. Not "computes depth per
    file and misses the chain", which was this note's earlier wording and
    understated it: `if cur not in parents: break` skips the `while/else`,
    so the depth test never executes. Measured 2026-08-07; see the
    trigger section below for the numbers. FALSE NEGATIVES, the worse
    direction, and silent.
  * `role-named` and `jurisdiction` miss classes, slots and enums
    inherited from an imported schema.
  * `exact-mappings` misses mappings added by `slot_usage` or a mixin.

The fix is linkml_runtime's SchemaView, which resolves imports, mixins,
inheritance and slot_usage into an induced view. Deferred deliberately:
there is nothing to resolve while vocab/ is empty, and a SchemaView
rewrite tested against zero schemas would be the same mistake this file
already records four times.

**THE TRIGGER IS NOT "more than one file".** An earlier version of this
note said it was, and named P6a. P6a arrived, `vocab/core/` holds three
files, and nothing degraded — because the mechanism needs a term
RESOLVED ACROSS a boundary, not merely two files present.

The trigger is the first of these:

  * an `is_a` or `mixins` naming a class declared in an imported schema.
    **`is-a-depth` does not under-count the chain; it EXEMPTS the class
    from the rule entirely, at any depth.** Measured 2026-08-07 on the
    same five-class chain authored twice:

        one file,  A->B->C->D->E          FAIL x2  (D depth 3, E depth 4)
        E's parent in another file         FAIL x1  (D only; E unreported)

    `E` has true depth 4 and is checked at no depth. The `break` on a
    parent defined elsewhere skips the `while/else`, so the depth test
    never runs for that chain. An earlier version of this note said the
    rule "computes depth per file and misses the chain" — under-counting.
    That was too weak: it declines to check. **Prediction TESTED and
    CONFIRMED, in the false-negative direction.**
  * a `slots:` list naming a slot declared in an imported schema —
    `role-named`, `jurisdiction`, `documented`, `declared-prefix` and
    `shared-uri` then see the reference and not the declaration.

Until one of those exists the prediction is **untested, not falsified**,
and a trigger stated as a file count would have read as a falsification.
A prediction is only checkable if its trigger names the mechanism.

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
# No upper bound. It was 8, then 12, and `NWCGIRWINIDENTIFIER` (19)
# cleared both — see [H -> O] plan gate, F13 case c3. Guessing a third
# number is not a fix. Any all-caps identifier of two or more characters
# is treated as an acronym; legitimate long all-caps terms are rare in a
# vocabulary that otherwise uses camelCase and PascalCase, and the
# allowlist below handles the ones that occur.
ACRONYM = re.compile(r"^[A-Z][A-Z0-9]+$")

# Namespaces that publish domain-neutral vocabularies. A prefix pointing
# anywhere else is jurisdiction-specific until declared otherwise — an
# agency namespace in a `prefixes:` block is the cheapest signal
# available, and nothing inspected it until F12.
#
# HOST IS THE WRONG GRANULARITY FOR REDIRECT SERVICES. w3id.org and
# purl.org are permanent-identifier redirects; anyone can register a
# namespace under either, so allowlisting them by host admits every
# scheme published there. `https://w3id.org/nwcg/irwin/` passed while
# `https://w3id.org/linkml/` had to keep passing. See [H -> O] plan
# gate, F13 cases c1 and c2.
#
# So: single-authority hosts match on host; shared infrastructure
# matches on host plus path prefix.

# The project's own namespaces, declared OUTSIDE any schema. See
# scripts/project-namespaces.txt for why this is not derived from `id:`
# or `default_prefix`.
def _project_namespaces() -> list[str]:
    f = pathlib.Path(__file__).parent / "project-namespaces.txt"
    if not f.exists():
        return []
    return [ln.strip().rstrip("/#") for ln in f.read_text().split("\n")
            if ln.strip() and not ln.lstrip().startswith("#")]


PROJECT_NAMESPACES = _project_namespaces()


SINGLE_AUTHORITY_HOSTS = {
    "w3.org", "www.w3.org",
    "opengis.net", "www.opengis.net",
    "qudt.org", "www.qudt.org",
    "xmlns.com", "schema.org", "rdfs.org",
    "vocab.nerc.ac.uk", "unitsofmeasure.org", "cfconventions.org",
    "dublincore.org", "id.loc.gov",
}

# Hosts where registration is open to anyone. A namespace here is
# generic only if its path prefix is explicitly allowlisted.
SHARED_NAMESPACE_HOSTS = {
    "w3id.org", "www.w3id.org",
    "purl.org", "www.purl.org",
    "purl.oclc.org", "purl.obolibrary.org",
}

# host/path prefixes on shared infrastructure that ARE generic.
# Each entry admits exactly one namespace, not a host.
SHARED_ALLOWED_PREFIXES = {
    "w3id.org/linkml",        # LinkML metamodel
    "purl.org/dc/terms",      # DCMI Terms
    "purl.org/dc/elements",   # Dublin Core Elements
}

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
    # F11: every external vocabulary CLAUDE.md commits to binding.
    # The original list was populated from a partial reading of the
    # conventions section it exists to serve — CF appeared in the same
    # sentence as SOSA and QUDT and was omitted anyway. Each entry below
    # carries the reason it is domain-neutral.
    "CF",    # CF Standard Names — international climate/forecast vocabulary
    "NVS",   # NERC Vocabulary Server — international term registry
    "DQV",   # W3C Data Quality Vocabulary
    "ADMS",  # W3C Asset Description Metadata Schema
    "DCAT",  # W3C Data Catalog Vocabulary
    "DCT",   # DCMI Terms
    "OMS",   # ISO 19156 Observations, Measurements and Samples
    "UCUM",  # Unified Code for Units of Measure
    "SSN",   # W3C Semantic Sensor Network
    "GEO",   # GeoSPARQL
    "TIME",  # W3C Time Ontology
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
    """Slots are first-class. No inline `attributes:` on a class.

    NO CLAIM COVERS THIS RULE. It was labelled C19 for several gates and
    C19 was never filed — the register goes C18 to C20. A guard citing a
    claim that does not exist sends a reader nowhere, and it means the
    property has no falsifier and no status. Propose the claim or drop
    the rule; do not leave it citing a number.
    """
    bad = []
    for name, cls in (doc.get("classes") or {}).items():
        if isinstance(cls, dict) and cls.get("attributes"):
            bad.append(f"{path}: class `{name}` uses inline `attributes:` — "
                       f"declare a top-level slot and reference it")
    return bad


def rule_is_a_depth(path, doc):
    """`is_a` CHAIN DEPTH <= 2. No claim covers this rule — see
    rule_inline_attributes.

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
    """At most one `exact_mappings` per class. Serves C21.

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

    # SELF-REFERENCE IS DECLARED OUTSIDE THE SCHEMA.
    #
    # A schema may use its own namespace freely, but it does not get to
    # say which namespace that is. Three attempts derived the exemption
    # from inside the file and all three were escapable, because a
    # self-declared field cannot constrain itself:
    #
    #   BV8  — no namespace passed at all                  (precision)
    #   BV14 — `default_prefix` nominated any namespace     (recall)
    #   BV19 — `id:` nominated any namespace                (recall)
    #   BV23 — `default_prefix` naming any ANCESTOR of `id:`,
    #          because the agreement test matched both ways (recall)
    #
    # `id:` and `default_prefix` count as self ONLY when they fall under
    # a namespace listed in scripts/project-namespaces.txt, which a
    # schema author does not edit while authoring a schema. Neither
    # widens the other: both are tested against the external list, so
    # there is no agreement test left to match in the wrong direction.
    if not PROJECT_NAMESPACES:
        bad.append(f"{path}: scripts/project-namespaces.txt is missing or "
                   f"empty, so no namespace counts as the project's own "
                   f"and every schema's own terms will fire. Declare the "
                   f"project namespace there")

    def under_project(uri) -> bool:
        u = str(uri).rstrip("/#")
        return any(u == ns or u.startswith(ns.rstrip("/#") + "/") or
                   u == ns.rstrip("/#") for ns in PROJECT_NAMESPACES)

    own = []
    if doc.get("id") and under_project(doc["id"]):
        base = str(doc["id"]).rstrip("/#")
        own += [base, base + "/"]
    dp = doc.get("default_prefix")
    if dp and isinstance(doc.get("prefixes"), dict) and dp in doc["prefixes"]:
        dp_uri = str(doc["prefixes"][dp]).rstrip("/#")
        if under_project(dp_uri):
            own.append(dp_uri)


    def is_self(uri: str) -> bool:
        u = str(uri).rstrip("/#")
        return any(u == o.rstrip("/#") or u.startswith(o) for o in own if o)

    def check(kind, name):
        n = str(name)
        if ACRONYM.match(n) and n not in GENERIC_ACRONYMS:
            bad.append(f"{path}: {kind} `{n}` is an acronym and not a "
                       f"generic international term — jurisdiction-specific "
                       f"schemes belong in vocab/profiles/. If this is "
                       f"genuinely domain-neutral, add it to "
                       f"GENERIC_ACRONYMS with a reason")

    def check_uri(kind, where, value):
        """A prefix or CURIE pointing outside the generic-namespace
        allowlist. F12: CLAUDE.md says code lists are SKOS schemes
        referenced via `PermissibleValue.meaning`, so once the project
        follows its own conventions, names are the place jurisdiction
        content is LEAST likely to appear."""
        v = str(value)
        if is_self(v):
            return
        if "://" in v:
            rest = v.split("://", 1)[1]
            host = rest.split("/")[0].split(":")[0].lower()
            hostpath = f"{host}/{'/'.join(rest.split('/')[1:])}".rstrip("/#")
            if host in SHARED_NAMESPACE_HOSTS:
                if not any(hostpath.startswith(a) for a in SHARED_ALLOWED_PREFIXES):
                    bad.append(f"{path}: {kind} `{where}` declares namespace "
                               f"`{v}` on `{host}`, which is a public "
                               f"permanent-identifier redirect — anyone may "
                               f"register there, so the path must be "
                               f"allowlisted, not the host")
            elif host not in SINGLE_AUTHORITY_HOSTS:
                bad.append(f"{path}: {kind} `{where}` declares namespace "
                           f"`{v}` on host `{host}`, which is not a known "
                           f"generic vocabulary host — jurisdiction-specific "
                           f"namespaces belong in vocab/profiles/")
        elif ":" in v:
            pfx = v.split(":", 1)[0]
            declared = doc.get("prefixes") or {}
            if pfx in declared and is_self(declared[pfx]):
                return
            if pfx and pfx not in declared and pfx.upper() not in GENERIC_ACRONYMS:
                bad.append(f"{path}: {kind} `{where}` uses CURIE prefix "
                           f"`{pfx}`, which is neither declared in this file "
                           f"nor a known generic vocabulary")

    prefixes = doc.get("prefixes") or {}
    if isinstance(prefixes, dict):
        for pfx, uri in prefixes.items():
            check_uri("prefix", pfx, uri)

    for n, c in (doc.get("classes") or {}).items():
        check("class", n)
        if isinstance(c, dict):
            for f in ("class_uri", "meaning"):
                if c.get(f):
                    check_uri(f"class {f}", n, c[f])
    for n, sl in (doc.get("slots") or {}).items():
        check("slot", n)
        if isinstance(sl, dict):
            for f in ("slot_uri", "meaning"):
                if sl.get(f):
                    check_uri(f"slot {f}", n, sl[f])
    for n, e in (doc.get("enums") or {}).items():
        check("enum", n)
        for pv, body in ((e or {}).get("permissible_values") or {}).items():
            check("permissible value", pv)
            if isinstance(body, dict) and body.get("meaning"):
                check_uri("permissible value meaning", pv, body["meaning"])
    return bad


PLACEHOLDER = {"", "todo", "tbd", "fixme", "xxx", "tk", "n/a", "-", "..."}


def rule_declared_prefix(path, doc):
    """Every CURIE prefix used is declared in this file's `prefixes:` map.

    This is P5 clause 1 — *prefixes.yaml resolves every prefix used* —
    mechanized. Without it the clause is met by judgement: `prefixes: {}`
    passes every other rule, and no instrument checks the population.

    IT IS NOT COVERED BY `jurisdiction`. That rule flags an undeclared
    CURIE prefix only when the prefix is not in GENERIC_ACRONYMS — and
    GENERIC_ACRONYMS is exactly `sosa`, `prov`, `qudt`, `geo`, `dct` and
    the rest of clause 1's population. Being a known generic vocabulary
    says the prefix is not a jurisdiction; it says nothing about whether
    the file declares it. Two questions, one allowlist, and the second
    was uncovered.

    KNOWN LIMITATION, same as the rest of this file: raw YAML does not
    resolve `imports:`, so a prefix declared in an imported schema reads
    as undeclared here. Recorded rather than worked around — the trigger
    is a term RESOLVED ACROSS a file boundary — an `is_a`/`mixins` naming
    an imported class, or a `slots:` list naming an imported slot. Not
    "more than one file", which was this note's earlier wording and is
    already met without any degradation. See the module docstring; the
    trigger is stated there once and nowhere else.
    """
    bad = []
    declared = set(doc.get("prefixes") or {})

    def check(kind, where, value):
        v = str(value)
        if "://" in v or ":" not in v:
            return
        pfx = v.split(":", 1)[0]
        if pfx and pfx not in declared:
            bad.append(f"{path}: {kind} `{where}` uses CURIE prefix "
                       f"`{pfx}:` which this file does not declare. Add it "
                       f"to `prefixes:` — a prefix map that does not resolve "
                       f"every prefix used is the clause it exists to meet, "
                       f"unmet")

    for n, c in (doc.get("classes") or {}).items():
        if not isinstance(c, dict):
            continue
        for f in ("class_uri", "meaning"):
            if c.get(f):
                check(f"class {f}", n, c[f])
        for m in (c.get("exact_mappings") or []):
            check("class exact_mappings", n, m)
    for n, sl in (doc.get("slots") or {}).items():
        if not isinstance(sl, dict):
            continue
        for f in ("slot_uri", "meaning"):
            if sl.get(f):
                check(f"slot {f}", n, sl[f])
        for m in (sl.get("exact_mappings") or []):
            check("slot exact_mappings", n, m)
    for ename, e in (doc.get("enums") or {}).items():
        for pv, body in ((e or {}).get("permissible_values") or {}).items():
            if isinstance(body, dict) and body.get("meaning"):
                check("permissible value meaning", f"{ename}.{pv}",
                      body["meaning"])
    return bad


def rule_documented(path, doc):
    """Invariant 7: every class and slot carries a `description` and at
    least one `examples` entry.

    `CLAUDE.md` invariant 7 said "Lint enforces it" and nothing did. A
    schema with eight classes, twelve slots, every description the
    literal string TODO and zero examples passed clean and generated its
    shapes at exit 0. See claims.md C20.

    This matters beyond documentation: C6 (LLM-legibility) rests on
    invariant 7 and has no other guard.
    """
    bad = []

    def check(kind, name, body):
        if not isinstance(body, dict):
            body = {}
        d = str(body.get("description") or "").strip()
        if d.lower().rstrip(".") in PLACEHOLDER:
            bad.append(f"{path}: {kind} `{name}` has "
                       f"{'no description' if not d else f'a placeholder description ({d!r})'}"
                       f" — invariant 7")
        if not body.get("examples"):
            bad.append(f"{path}: {kind} `{name}` has no `examples` entry — "
                       f"invariant 7. One example grounds a reader, human "
                       f"or model, better than three sentences")

    for n, c in (doc.get("classes") or {}).items():
        check("class", n, c)
    for n, sl in (doc.get("slots") or {}).items():
        check("slot", n, sl)
    return bad


def rule_shared_uri(path, doc):
    """C21: no two schema elements assert identity to the same external
    URI, by any construct.

    Identity-asserting constructs, all collected into ONE map:

      classes  — `class_uri`, `exact_mappings`, `same_as`
      slots    — `slot_uri`,  `exact_mappings`, `same_as`
      enums    — `PermissibleValue.meaning`

    `close_mappings`, `related_mappings` and `narrow_mappings` are NOT
    identity assertions and are deliberately not collected.

    THE FIRST VERSION CALLED collect() TWICE WITH A FRESH MAP EACH TIME,
    classes then slots, so the two never met and three constructs were
    outside its subject by construction — verified by probe:

      class via class_uri + SLOT via exact_mappings   -> passed
      class via class_uri + class via same_as         -> passed
      two PermissibleValue.meaning on one URI         -> passed

    The third is the one that matters: `meaning` is the route CLAUDE.md
    names to every SKOS code list. See [O -> H] design gate block
    verification 5, "Your C21 restatement — adopted, with the ground
    corrected."

    Measured for `class_uri` collisions: gen-shacl emits ONE NodeShape
    carrying the union of both elements' property shapes, each with
    sh:minCount 1, at exit 0.
    """
    bad = []
    claims = {}

    def claim(kind, name, uri, via):
        claims.setdefault(str(uri), []).append((kind, name, via))

    def scan(kind, items, uri_field):
        for name, body in (items or {}).items():
            if not isinstance(body, dict):
                continue
            if body.get(uri_field):
                claim(kind, name, body[uri_field], uri_field)
            for m in (body.get("exact_mappings") or []):
                claim(kind, name, m, "exact_mappings")
            sa = body.get("same_as")
            for m in ([sa] if isinstance(sa, str) else (sa or [])):
                claim(kind, name, m, "same_as")

    scan("class", doc.get("classes"), "class_uri")
    scan("slot", doc.get("slots"), "slot_uri")
    for ename, e in (doc.get("enums") or {}).items():
        for pv, body in ((e or {}).get("permissible_values") or {}).items():
            if isinstance(body, dict) and body.get("meaning"):
                claim("permissible value", f"{ename}.{pv}", body["meaning"],
                      "meaning")

    for uri, holders in claims.items():
        # Distinct ELEMENTS, not distinct claims. One element naming the
        # same URI through two constructs is redundant, not a collision —
        # it asserts identity with itself. Flagging it was a precision
        # failure found by the near-miss control.
        if len({(k, n) for k, n, _ in holders}) > 1:
            where = ", ".join(f"{k} `{n}` (via {v})"
                              for k, n, v in sorted(holders))
            bad.append(f"{path}: {where} each claim `{uri}` as an identity. "
                       f"Two elements asserting one URI assert they are "
                       f"equivalent, which is almost never true and "
                       f"generates one merged shape at exit 0 (claims.md "
                       f"C21). Use close_ or related_mappings for anything "
                       f"short of equivalence")
    return bad


PLACEHOLDER = {"", "todo", "tbd", "fixme", "xxx", "tk", "n/a", "-", "..."}


RULES = {
    "inline-attributes": rule_inline_attributes,
    "is-a-depth": rule_is_a_depth,
    "exact-mappings": rule_exact_mappings,
    "role-named": rule_role_named,
    "jurisdiction": rule_jurisdiction,
    "documented": rule_documented,
    "declared-prefix": rule_declared_prefix,
    "shared-uri": rule_shared_uri,
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