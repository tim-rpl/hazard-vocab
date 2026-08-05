#!/usr/bin/env python3
"""Cache the external vocabularies this project binds, and verify them.

    fetch-external.py            fetch, verify, write manifest.md
    fetch-external.py --check    verify the CACHE only; no network

**This is P5's caching clause, started early.** P5's `done_when` reads
*"all external terms are content-verified by fetch-and-grep; external
graphs are cached locally."* Those are one operation, so this does both
and records the result.

**Why fetch-and-grep and not a status code.** A 200 proves a server
answered, not that a term exists. `http://www.w3.org/ns/sosa/thisTermDoesNotExist`
returns a payload byte-identical to a real term's, `qudt:unit` did not
exist, OMS returns a 288-byte stub with zero occurrences of the term it
was cited for, and the ENTSO-E URI 404s. Three of this project's own
bindings were falsified that way. So every entry below carries the terms
it is bound for, and the manifest records **which terms were found in
the payload**, not that the payload arrived.

A term recorded as MISSING is not a bug in this script. It is the
finding, and it belongs in the gate.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "graphs"
MANIFEST = HERE / "manifest.md"

# (key, namespace URI, fetch URL, [terms that MUST appear in the payload])
#
# The term lists come from design/surface.yaml's bound populations, plus
# the terms CLAUDE.md commits to binding. A vocabulary with no term list
# is cached but NOT content-verified, and the manifest says so rather
# than implying otherwise.
SOURCES = [
    ("sosa", "http://www.w3.org/ns/sosa/",
     "http://www.w3.org/ns/sosa/",
     ["observedProperty", "hasFeatureOfInterest", "hasResult",
      "hasSimpleResult", "resultTime", "phenomenonTime", "madeBySensor",
      "usedProcedure", "isHostedBy", "Observation", "Sensor", "Platform",
      "FeatureOfInterest", "Procedure", "ObservableProperty"]),
    ("ssn", "http://www.w3.org/ns/ssn/",
     "http://www.w3.org/ns/ssn/",
     ["System", "hasSubSystem"]),
    ("ssn-ext", "http://www.w3.org/ns/ssn/ext/",
     "https://www.w3.org/ns/ssn/ext/",
     ["hasMember", "ObservationCollection"]),
    ("ssn-system", "http://www.w3.org/ns/ssn/systems/",
     "http://www.w3.org/ns/ssn/systems/",
     ["SystemCapability", "OperatingRange"]),
    ("prov-o", "http://www.w3.org/ns/prov#",
     "http://www.w3.org/ns/prov-o#",
     ["wasAttributedTo", "generatedAtTime", "Agent", "Activity", "Entity"]),
    ("org", "http://www.w3.org/ns/org#",
     "http://www.w3.org/ns/org#",
     ["Organization"]),
    # The namespace URI returns a Prez DESCRIPTION document: the terms
    # appear, annotated with `prez:description`, and nothing is defined.
    # Presence passed 4/4 and `audit-bound-terms.py` found zero
    # definitions — which is why term presence is necessary and not
    # sufficient. Fetching the OGC-published ontology instead.
    ("geosparql", "http://www.opengis.net/ont/geosparql#",
     "https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl",
     ["hasGeometry", "asWKT", "Geometry", "wktLiteral"]),
    ("qudt-schema", "http://qudt.org/schema/qudt/",
     "http://qudt.org/schema/qudt/",
     ["QuantityValue", "hasUnit", "numericValue"]),
    ("qudt-units", "http://qudt.org/vocab/unit/",
     "http://qudt.org/vocab/unit/",
     ["MicroGM-PER-M3", "PPB", "DEG_C", "PERCENT", "M-PER-SEC", "UNITLESS"]),
    ("skos", "http://www.w3.org/2004/02/skos/core#",
     "http://www.w3.org/2004/02/skos/core",
     ["ConceptScheme", "OrderedCollection", "broader", "prefLabel"]),
    ("owl-time", "http://www.w3.org/2006/time#",
     "http://www.w3.org/2006/time",
     ["Interval", "ProperInterval", "hasBeginning", "hasEnd"]),
    ("foaf", "http://xmlns.com/foaf/0.1/",
     "http://xmlns.com/foaf/0.1/",
     ["Document"]),
    ("dqv", "http://www.w3.org/ns/dqv#",
     "https://www.w3.org/ns/dqv.ttl",
     ["QualityMeasurement", "hasQualityMeasurement"]),
    ("adms", "http://www.w3.org/ns/adms#",
     "https://www.w3.org/ns/adms.ttl",
     ["Identifier", "schemeAgency"]),
    ("dcterms", "http://purl.org/dc/terms/",
     "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl",
     ["conformsTo", "issued"]),
    ("shacl", "http://www.w3.org/ns/shacl#",
     "https://www.w3.org/ns/shacl.ttl",
     ["NodeShape", "path", "equals", "condition", "sparql"]),
    # The Part 1 lead. UNVERIFIED by design — ADR-006 records three
    # questions to answer by fetch when Part 1 comes up, and whether the
    # namespace dereferences at all is the first of them.
    ("deo", "http://schema.knowwheregraph.org/",
     "http://schema.knowwheregraph.org/lod/ontology/",
     []),
]


def fetch(url):
    """curl, following redirects, asking for turtle. Returns
    (status, final_url, content_type, body_bytes).

    Body goes to a FILE and metadata to stdout. The first version sent
    both to stdout and split the `-w` block off the end, which broke on
    the one payload whose last line had no trailing newline: DQV's final
    `skos:definition` line was parsed as the HTTP status, the entry was
    recorded as failed, and the same run reported 2/2 of its terms
    present. An instrument disagreeing with itself in one row — caught
    because the row was absurd, not because anything checked it.
    """
    fmt = "%{http_code}\n%{url_effective}\n%{content_type}\n"
    with tempfile.NamedTemporaryFile(delete=False) as fh:
        tmp = pathlib.Path(fh.name)
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "45",
             "-H", "Accept: text/turtle, application/rdf+xml;q=0.8, */*;q=0.1",
             "-w", fmt, "-o", str(tmp), url],
            capture_output=True, text=True)
        meta = (r.stdout or "").splitlines()
        status, final, ctype = (meta + ["000", url, ""])[:3]
        body = tmp.read_bytes()
    finally:
        tmp.unlink(missing_ok=True)
    return status, final, ctype, body


def terms_found(body, terms):
    """Which terms occur in the payload. Substring, deliberately — a
    term may be written out, prefixed, or in an rdf:about attribute, and
    a parser that understood only one of those would report absence for
    a term that is present."""
    text = body.decode("utf-8", "replace")
    return {t: bool(re.search(r"\b%s\b" % re.escape(t), text)) for t in terms}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the cache on disk; no network")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)

    rows, problems = [], []
    for key, ns, url, terms in SOURCES:
        path = CACHE / ("%s.ttl" % key)
        if args.check:
            if not path.exists():
                problems.append("%s: not cached" % key)
                continue
            body, status, final, ctype = path.read_bytes(), "cache", url, "-"
        else:
            status, final, ctype, body = fetch(url)
            if status == "200" and body:
                path.write_bytes(body)
            else:
                problems.append("%s: HTTP %s from %s" % (key, status, url))

        if not body:
            rows.append((key, ns, status, 0, "-", "-", "no payload"))
            continue

        found = terms_found(body, terms)
        missing = sorted(t for t, ok in found.items() if not ok)
        if missing:
            problems.append("%s: %d/%d terms MISSING from the payload: %s"
                            % (key, len(missing), len(terms),
                               ", ".join(missing)))
        verdict = ("**not content-verified** — no term list" if not terms
                   else "%d/%d terms present" % (len(terms) - len(missing),
                                                 len(terms)))
        rows.append((key, ns, status, len(body),
                     hashlib.sha256(body).hexdigest()[:12],
                     ctype.split(";")[0] or "-", verdict))

    out = ["# External vocabulary cache — manifest", "",
           "**Generated by `fetch-external.py`. Do not edit.**", "",
           "Every row records what was found **in the payload**, not that",
           "the payload arrived. A 200 proves a server answered; three of",
           "this project's bindings were falsified by a term that was",
           "absent behind one.", "",
           "| Vocabulary | Namespace | HTTP | Bytes | SHA-256 | Type | Content check |",
           "|---|---|---|---|---|---|---|"]
    for key, ns, status, n, sha, ctype, verdict in rows:
        out.append("| `%s` | `%s` | %s | %s | `%s` | %s | %s |"
                   % (key, ns, status, n, sha, ctype, verdict))
    out += ["", "## Problems", ""]
    out += (["*(none)*"] if not problems else
            ["- %s" % p for p in problems])
    out.append("")
    MANIFEST.write_text("\n".join(out))

    print("\n".join(out[7:]))
    if problems:
        print("\n%d problem(s) — these are findings, not script bugs"
              % len(problems), file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
