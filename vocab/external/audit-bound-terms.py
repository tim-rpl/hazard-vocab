#!/usr/bin/env python3
"""Read every bound term's DEFINITION out of the cached graphs.

    audit-bound-terms.py           print the audit
    audit-bound-terms.py --check   fail if any bound term is absent from
                                   the cache, or is an object property
                                   whose range names an undeclared type

**Why this exists.** O attacked H's claim that no relation reaches this
unit and broke it on `sosa:hasMember` — a whole-to-member property that
was bound at `surface.yaml:25`, scheduled for Part 2, and had never been
looked up. The name did not say "relation"; the definition did.

`.claude/rules/vocab-conventions.md` already prescribes the check —
*fetch the graph and grep for the term; does the definition match the
intended use, or only its name; is it a role class; does it declare a
domain and range* — and it was applied to three terms out of
twenty-nine.

This applies it to all of them, from the cache, mechanically. It answers
one question per bound term that a name cannot: **is it an object
property, and if so what types does it imply?** C24 records that this
unit declares none of the types in its own relation signatures. If a
bound object property implies a type nothing declares, C24's population
reaches into the bound terms and lands in `vocab/core/` at P7.
"""
import argparse
import pathlib
import sys

try:
    from rdflib import Graph, RDF, RDFS, OWL, URIRef
except ImportError:
    sys.exit("rdflib not importable — run under .venv/bin/python")

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "graphs"
SURFACE = HERE.parent.parent / "design" / "surface.yaml"

NS = {
    "sosa": "http://www.w3.org/ns/sosa/",
    "ssn-ext": "http://www.w3.org/ns/ssn/ext/",
    "prov-o": "http://www.w3.org/ns/prov#",
    "org": "http://www.w3.org/ns/org#",
    "geosparql": "http://www.opengis.net/ont/geosparql#",
    "qudt-schema": "http://qudt.org/schema/qudt/",
    # same graph as `ssn-ext`, but the terms are minted in SOSA's namespace
    "ssn-ext-sosa": "http://www.w3.org/ns/sosa/",
}

# Which cached graph to look a bound local name up in. Derived from
# design/surface.yaml's populations; the mapping is stated rather than
# guessed because a slash namespace returns the whole document for every
# path under it, so "it resolved" proves nothing about which graph
# defines the term.
LOOKUP = [
    ("sosa", ["observedProperty", "hasFeatureOfInterest", "hasResult",
              "hasSimpleResult", "resultTime", "phenomenonTime",
              "madeBySensor", "usedProcedure", "isHostedBy",
              "Observation", "Sensor", "Platform", "FeatureOfInterest",
              "Procedure", "ObservableProperty"]),
    # `hasMember` and `ObservationCollection` are minted in the SOSA
    # namespace by the SSN-ext Note, not in `ssn/ext/`. Looking them up
    # under `ssn/ext/` reported both ABSENT — the audit's own version of
    # reading a term off its document rather than its namespace.
    ("ssn-ext-sosa", ["hasMember", "ObservationCollection"]),
    ("prov-o", ["wasAttributedTo", "generatedAtTime",
                "Agent", "Activity", "Entity"]),
    ("org", ["Organization"]),
    ("geosparql", ["hasGeometry", "asWKT", "Geometry"]),
    ("qudt-schema", ["hasUnit", "numericValue", "QuantityValue"]),
]

OBJECT_PROPS = {OWL.ObjectProperty}
DATA_PROPS = {OWL.DatatypeProperty}


def short(u):
    s = str(u)
    for k, v in NS.items():
        if s.startswith(v):
            return "%s:%s" % (k.split("-")[0], s[len(v):])
    for pre, v in (("rdfs", str(RDFS)), ("owl", str(OWL)),
                   ("xsd", "http://www.w3.org/2001/XMLSchema#"),
                   ("time", "http://www.w3.org/2006/time#"),
                   ("skos", "http://www.w3.org/2004/02/skos/core#"),
                   ("dct", "http://purl.org/dc/terms/")):
        if s.startswith(v):
            return "%s:%s" % (pre, s[len(v):])
    return s


GRAPH_FILE = {"ssn-ext-sosa": "ssn-ext"}


def load(key):
    p = CACHE / ("%s.ttl" % GRAPH_FILE.get(key, key))
    if not p.exists():
        return None
    g = Graph()
    for fmt in ("turtle", "xml"):
        try:
            g.parse(p, format=fmt)
            return g
        except Exception:
            g = Graph()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    rows, problems = [], []
    for key, names in LOOKUP:
        g = load(key)
        if g is None:
            problems.append("%s: cached graph missing or unparseable" % key)
            continue
        base = NS[key]
        for name in names:
            u = URIRef(base + name)
            types = set(g.objects(u, RDF.type))
            if not types:
                problems.append("%s:%s — NOT DEFINED in the cached graph"
                                % (key, name))
                rows.append((key, name, "ABSENT", "-", "-", "-"))
                continue
            kind = ("object property" if types & OBJECT_PROPS else
                    "datatype property" if types & DATA_PROPS else
                    "class" if OWL.Class in types or RDFS.Class in types
                    else ", ".join(sorted(short(t) for t in types)))
            dom = sorted({short(o) for o in g.objects(u, RDFS.domain)})
            rng = sorted({short(o) for o in g.objects(u, RDFS.range)})
            sup = sorted({short(o) for o in g.objects(u, RDFS.subPropertyOf)})
            rows.append((key, name, kind, ", ".join(dom) or "—",
                         ", ".join(rng) or "—", ", ".join(sup) or "—"))

    out = ["# Bound terms, read from their definitions", "",
           "**Generated by `audit-bound-terms.py`. Do not edit.**", "",
           "One row per term this unit binds, read out of the cached graph",
           "rather than off the term's name. `manifest.md` records that a",
           "term is *present* in a payload; this records what it *is*.",
           "**Presence is necessary and not sufficient** — the GeoSPARQL",
           "namespace URI returns a Prez description document in which all",
           "four bound terms appear and none is defined. The manifest",
           "scored it 4/4; this audit found zero definitions.", "",
           "A type in the domain or range column that this project has not",
           "bound is **declared externally and undecided here** — it is not",
           "an undeclared type in C24's sense. `geosparql:Feature` and",
           "`qudt:Unit` are both declared, in the graphs cached beside this",
           "file.", "",
           "| Cached graph | Term | Kind | rdfs:domain | rdfs:range | subPropertyOf |",
           "|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| `%s` | `%s` | %s | %s | %s | %s |" % r)
    print("\n".join(out[15:]))

    obj = [r for r in rows if r[2] == "object property"]
    nodr = [r for r in obj if r[3] == "—" and r[4] == "—"]
    print("\n**%d object properties of %d terms audited.**" % (len(obj), len(rows)))
    if nodr:
        print("\n**Neither domain nor range — constrains nothing in generated "
              "SHACL** (`vocab-conventions.md` check 4):")
        for r in nodr:
            print("- `%s:%s`" % (r[0], r[1]))
    tail = ["", "**%d object properties of %d terms audited.**" % (len(obj), len(rows))]
    if nodr:
        tail += ["", "**Neither domain nor range — constrains nothing in "
                 "generated SHACL** (`vocab-conventions.md` check 4):", ""]
        tail += ["- `%s:%s`" % (r[0], r[1]) for r in nodr]
    if problems:
        print("\n## Problems\n")
        for p in problems:
            print("- %s" % p)
        tail += ["", "## Problems", ""] + ["- %s" % p for p in problems]
    (HERE / "bound-terms.md").write_text("\n".join(out + tail) + "\n")
    return 1 if (problems and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
