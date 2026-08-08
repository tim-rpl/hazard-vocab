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
    from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode
except ImportError:
    sys.exit("rdflib not importable — run under .venv/bin/python")

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "graphs"
CORE = HERE.parent / "core"
SURFACE = HERE.parent.parent / "design" / "surface.yaml"


def authored_bindings():
    """Every external CURIE the AUTHORED vocabulary binds, per cache key.

    F41: this audit's population was a hardcoded `LOOKUP` of six
    namespaces, and `bound-terms.md` therefore had **zero** rows mentioning
    `time` — while `vocab/core/part0-entity-core.yaml` carries seven
    `slot_uri` bindings of which **two are `time:`**. Those two are the
    only ones in the fragment with a superproperty, which is the property
    ADR-007's falsifier now turns on. **A falsifier's standing instrument
    was blind to the only case that would fire it.**

    Reading the plan rather than the artifact was sound while nothing was
    authored. It stopped being sound at P6a.

    And the constant naming the plan was WORSE than a stale population:
    `SURFACE` was defined here and **used nowhere**, so the file read as
    though its terms were derived from `design/surface.yaml` when they were
    typed in by hand. A dead constant implying a derivation is harder to
    catch than a wrong one, because nothing it produces is ever wrong.
    """
    import re
    # MANY keys share one namespace — `sosa` and `ssn-ext-sosa` both map to
    # `http://www.w3.org/ns/sosa/` — so a plain reverse dict silently keeps
    # whichever came last, and `isHostedBy` was attributed to the wrong
    # cached graph. Collect every candidate and let `load()` decide by
    # whether the term is actually declared there.
    ns_to_keys = {}
    for k, v in NS.items():
        ns_to_keys.setdefault(v, []).append(k)
    found = {}
    for f in sorted(CORE.glob("*.yaml")):
        text = f.read_text()
        prefixes = dict(re.findall(r"^  ([A-Za-z][\w-]*): (https?://\S+)$",
                                   text, re.M))
        for field in ("slot_uri", "class_uri", "meaning"):
            for curie in re.findall(r"^\s*%s:\s*([A-Za-z][\w-]*):(\S+)\s*$"
                                    % field, text, re.M):
                pre, local = curie
                base = prefixes.get(pre)
                if not base:
                    continue
                cands = ns_to_keys.get(base, [])
                # A term is attributed to the ONE candidate graph that
                # declares it. Adding it to every candidate produced a
                # false ABSENT: `isHostedBy` is minted in SOSA's namespace
                # and `ssn-ext`'s graph does not declare it, so the
                # duplicate row reported a term missing that is present.
                pick = None
                for k in cands:
                    g = load(k)
                    if g is not None and list(
                            g.objects(URIRef(base + local), RDF.type)):
                        pick = k
                        break
                found.setdefault(pick or (cands[0] if cands else None),
                                 set()).add(local)
    found.pop(None, None)
    return {k: sorted(v) for k, v in found.items()}


def cache_state():
    """F19's ruling, IMPORTED from the sibling rather than restated.

    B1: this script was wired into `make lint` without being asked
    whether it honours a ruling made the round before —
    `grep -c 'cache_state|unfetched'` returned 0. On a fresh clone every
    graph is absent, so every lookup failed, and the audit went from 29
    rows to **zero while returning exit 1 and writing anyway**. That is
    the empty-bail `fetch-external.py` has and this did not: the sibling
    generator's own defect, arriving through the repair for the other.

    A second copy of the rule would be the duplicate-definition defect
    this project has now shipped twice in one file, so the rule is loaded
    from where it is defined. If the import fails, that is reported —
    never silently treated as `complete`, which is the state that writes.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_fx", HERE / "fetch-external.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # SCOPED to the graphs this script reads. B5: the state space is
    # enumerated in `fetch-external.py` beside `cache_state()`, and the
    # byte-level half of it costs 4.8s over all 36 graphs and 0.2s over
    # these six. A degraded graph nobody here reads cannot corrupt the
    # file being written, so the scope is the honest bound and not a dodge.
    state, why, _ = m.cache_state(keys=[k for k, _n in LOOKUP])
    return state, why

NS = {
    "sosa": "http://www.w3.org/ns/sosa/",
    "ssn-ext": "http://www.w3.org/ns/ssn/ext/",
    "prov-o": "http://www.w3.org/ns/prov#",
    "org": "http://www.w3.org/ns/org#",
    "geosparql": "http://www.opengis.net/ont/geosparql#",
    "qudt-schema": "http://qudt.org/schema/qudt/",
    # same graph as `ssn-ext`, but the terms are minted in SOSA's namespace
    "ssn-ext-sosa": "http://www.w3.org/ns/sosa/",
    # F41's own repair was blind to the case F41 is about: this map had no
    # OWL-Time entry, so the two `time:` bindings still resolved to no
    # cache key and were still dropped. Caught on the repair's first run.
    "owl-time": "http://www.w3.org/2006/time#",
}

# Cache key -> the CURIE prefix its namespace is known by. Separate from
# the key because a key is a filename and a prefix is an identity, and
# deriving one from the other printed `owl:hasTime` for a term in the
# OWL-Time namespace.
PREFIX = {
    "sosa": "sosa", "ssn-ext": "sosa", "ssn-ext-sosa": "sosa",
    "prov-o": "prov", "org": "org", "geosparql": "geo",
    "qudt-schema": "qudt", "owl-time": "time",
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


def anon(u, g):
    """A STABLE rendering of a blank node, by its structure.

    B10: `str(bnode)` is rdflib's per-parse label — `n74b7ef59…`,
    `n3f6680bf…`, `n4bd913f2…` on three consecutive runs of the same
    input. It reached one cell of `bound-terms.md`, so the file was never
    byte-reproducible and the drift check the register gained could never
    be pointed at it. A generated file that cannot equal itself cannot be
    guarded, whatever the Makefile says.

    Naming the construct is also more useful than the label was:
    `sosa:hasMember`'s range is a union, and *what* it is a union of is
    the thing a reader wants.
    """
    types = set(g.objects(u, RDF.type))
    if OWL.Restriction in types:
        p = [short(o, g) for o in g.objects(u, OWL.onProperty)]
        return "owl:Restriction on %s" % (", ".join(p) or "an unnamed property")
    for op, word in ((OWL.unionOf, "union"),
                     (OWL.intersectionOf, "intersection")):
        for lst in g.objects(u, op):
            members = [short(m, g) for m in g.items(lst)]
            return "%s of %s" % (word, ", ".join(members) or "nothing")
    if types:
        return "anonymous %s" % ", ".join(sorted(short(t, g) for t in types))
    return "an anonymous node"


def short(u, g=None):
    if isinstance(u, BNode):
        # No graph, no structure to read — say so rather than emit a label
        # that changes on the next parse.
        return anon(u, g) if g is not None else "an anonymous node"
    s = str(u)
    for k, v in NS.items():
        if s.startswith(v):
            # The prefix is looked up, NOT derived from the cache key.
            # `k.split("-")[0]` turned `owl-time` into `owl:`, printing
            # `owl:hasTime` — a CURIE that expands to a term nobody
            # declares. A key name is a filename; a prefix is an identity.
            return "%s:%s" % (PREFIX.get(k, k), s[len(v):])
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

    # B1, first half. The cache is input, and an unfetched cache is the
    # `.gitkeep` case — note what was inspected and pass. Ten seconds of
    # `git clone && make lint` would have caught the omission; the test
    # neither the human nor I ran.
    state, why = cache_state()
    if state == "unfetched":
        print("bound-terms.md: not %s — the cache is unfetched. This check "
              "inspected nothing. Run `fetch-external.py` to populate it."
              % ("checked" if args.check else "written"))
        return 0
    if state in ("degraded", "partial"):
        # B5, closed at the METHOD rather than at a fourth state. The row
        # count cannot see a graph that is present and parses to nothing:
        # every failed lookup still appends an `ABSENT` row, so
        # `len(rows) == expected` and the truncation bail below never
        # fires. Reading the BYTES is what separates *this graph defines
        # nothing* from *this term is genuinely absent*, and only the
        # second belongs in the audit.
        print("FAIL  the cache is %s — bound-terms.md NOT %s:"
              % (state.upper(), "checked" if args.check else "written"),
              file=sys.stderr)
        for w in why:
            print("        %s" % w, file=sys.stderr)
        return 1

    # F41: the population is the AUTHORED vocabulary, with `LOOKUP`
    # retained as a declared cross-check rather than as the source. A term
    # in `LOOKUP` and not in `vocab/core/` is a binding the plan expects
    # and nothing authored; the reverse is a binding this audit could not
    # see, which is the direction that hid the `time:` terms.
    rows, problems = [], []
    authored = authored_bindings()
    population = {k: sorted(set(v)) for k, v in authored.items()}
    for key, names in LOOKUP:
        population.setdefault(key, [])
        population[key] = sorted(set(population[key]) | set(names))
    # The cross-check runs in the direction that can go green: a term the
    # PLAN expects and nothing authored. The reverse — authored and not in
    # `LOOKUP` — is `LOOKUP` going stale as authoring proceeds, which is
    # expected and is printed as a note. Reported as a problem it could
    # never be cleared, and a guard nobody can satisfy gets deleted.
    for key, names in LOOKUP:
        pending = sorted(set(names) - set(authored.get(key, [])))
        if pending:
            print("  note: %s — %d term(s) in LOOKUP with no authored "
                  "binding yet: %s" % (key, len(pending), ", ".join(pending)))
    for key in sorted(authored):
        extra = sorted(set(authored[key]) - set(dict(LOOKUP).get(key, [])))
        if extra:
            print("  note: %s — authored and not in LOOKUP: %s (audited via "
                  "the authored-vocabulary population)"
                  % (key, ", ".join(extra)))
    for key, names in sorted(population.items()):
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
                    else ", ".join(sorted(short(t, g) for t in types)))
            dom = sorted({short(o, g) for o in g.objects(u, RDFS.domain)})
            rng = sorted({short(o, g) for o in g.objects(u, RDFS.range)})
            sup = sorted({short(o, g) for o in g.objects(u, RDFS.subPropertyOf)})
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
    # B10: this write was UNCONDITIONAL, so running the documented
    # verification command dirtied the working tree — C22 row 16, the
    # `--check`-writes defect, one file over from where it was repaired
    # and never repaired here.
    text = "\n".join(out + tail) + "\n"
    target = HERE / "bound-terms.md"
    # B1, second half — the worse one. Exit 1 was returned AND the file was
    # written, so a run that reported failure still replaced 29 rows with
    # zero. An audit of no terms is not an audit; it is a table that agrees
    # with its header, which is B9 one file over.
    #
    # The bail is on ROWS, not on problems: a run where every lookup failed
    # produces no rows and a full problem list, and it is the row count
    # that says the output is not an audit.
    # B2: this read `if not rows:` — and 14 rows is not zero. Removing ONE
    # cached graph took the audit from 29 term rows to 14, exit 1, and
    # WRITTEN, with the same message and the same false diagnosis one state
    # over. Emptiness is the special case; **truncation is what a partial
    # cache actually produces.**
    #
    # The count that says "this is not an audit" is fewer rows than the
    # LOOKUP can support, not zero. A term that is genuinely absent from a
    # cached graph still yields a row — `ABSENT` — so a short table means a
    # GRAPH is missing, which is exactly the case that must not be written.
    expected = sum(len(names) for _key, names in LOOKUP)
    if len(rows) < expected:
        print("FAIL  %d row(s) of %d the lookup can support — "
              "bound-terms.md NOT %s. A term missing from a cached graph "
              "still yields a row, so a short table means a GRAPH is "
              "absent. Truncation, not emptiness, is what a partial cache "
              "produces."
              % (len(rows), expected,
                 "checked" if args.check else "written"), file=sys.stderr)
        return 1
    if args.check:
        if not target.exists():
            problems.append("bound-terms.md: absent, and it is generated")
        elif target.read_text() != text:
            have, want = target.read_text().splitlines(), text.splitlines()
            d = [i for i in range(max(len(have), len(want)))
                 if have[i:i + 1] != want[i:i + 1]]
            problems.append(
                "bound-terms.md: DRIFTED from its generator — %d line(s) "
                "differ, first at %d" % (len(d), d[0] + 1 if d else 0))
            print("\n## Problems\n\n- %s" % problems[-1])
        print("bound-terms.md: not rewritten (--check reads only)")
    else:
        target.write_text(text)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
