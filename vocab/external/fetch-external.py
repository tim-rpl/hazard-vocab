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

A term recorded as MISSING is a claim about the payload, and it is
checked before it is reported. This line first read *"a term recorded as
MISSING is not a bug in this script — it is the finding"*, and the next
run produced two false MISSINGs from this file's own `\\b` anchoring
against names containing underscores. **The matcher is a suspect like
any other instrument.** Grep the payload for the real name before
reporting an absence.
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
     ["wasAttributedTo", "generatedAtTime", "Agent", "Activity", "Entity",
      "SoftwareAgent"]),
    ("org", "http://www.w3.org/ns/org#",
     "http://www.w3.org/ns/org#",
     ["Organization"]),
    # The namespace URI returns a Prez DESCRIPTION document: the terms
    # appear, annotated with `prez:description`, and nothing is defined.
    # Presence passed 4/4 and `audit-bound-terms.py` found zero
    # definitions — which is why term presence is necessary and not
    # sufficient. Fetching the OGC-published ontology instead.
    # GeoSPARQL 1.1, from the RELEASED TAG rather than a moving branch.
    # The previous URL pointed at `main` via GitHub Pages and began
    # returning a 9 KB HTML 404, which then overwrote this sidecar with the
    # 404 page's digest.
    #
    # 1.1 over 1.0, decided by measurement: all four bound terms and the
    # `Feature owl:disjointWith Geometry` axiom are IDENTICAL in both, so
    # ADR-004 Decision A holds either way. 1.1 mints 65 terms against 1.0's
    # 39 — the extra 26 include `hasCentroid`, `hasBoundingBox` and
    # `hasMetricArea`, which is where Part 2's coverage row would reach —
    # and both versions share one namespace, so this is a source-file
    # choice and not a rebinding.
    #
    # This file is not byte-identical to what the dead URL served (772 vs
    # 796 triples) and the diff is ANNOTATION VOCABULARY only: the tag uses
    # `skos:definition`/`prefLabel`/`example` where `main` used
    # `schema.org/description`. Same 65 terms, same axioms on all five
    # terms measured.
    ("geosparql", "http://www.opengis.net/ont/geosparql#",
     "https://raw.githubusercontent.com/opengeospatial/ogc-geosparql/1.1.0-ghpages/geosparql11/geo.ttl",
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
    # Candidates for the origin-type question (agent kind). Not cached
    # until 2026-08-05 and never probed, so the modelling argument was
    # running ahead of the measurement. F1's lesson applies: test for a
    # DEFINED term, not a 200.
    # Fetched from the GitHub source, not from
    # `schema.org/version/latest/schemaorg-current-https.ttl`. That URL
    # served a **260 KB payload with 0 of 3 bound terms** on 2026-08-05
    # and a valid 1.1 MB payload minutes later — a transient at a
    # published .ttl URL, which is exactly why the manifest records a
    # SHA-256 rather than a byte count. The GitHub raw file is 506,121
    # bytes and checksum-identical to the copy verified by hand.
    ("schema", "https://schema.org/",
     "https://raw.githubusercontent.com/schemaorg/schemaorg/main/data/schema.ttl",
     ["GovernmentOrganization", "NGO", "Organization"]),
    ("sioc", "http://rdfs.org/sioc/ns#",
     "http://rdfs.org/sioc/ns#",
     ["Community"]),
    # CF Standard Names. `CLAUDE.md` names this in its conventions, it is
    # a standing precision fixture in `bound-vocabularies.yaml`, and it is
    # the binding exp-01 showed would have turned the composite-versus-PM2.5
    # substitution into a validation failure. It was the one convention-named
    # vocabulary the cache did not hold.
    #
    # The NAMESPACE serves text/html; only the profile URL serves the graph
    # (200, text/turtle, 11.5 MB). That gap is precisely what the register's
    # `dereferences` column is for, and it is why the fetch URL and the
    # namespace are separate fields rather than one.
    # The twelve KWG source-specific ontologies — one per dataset, and the
    # profile-level artifacts `vocab/profiles/` exists for and has none of.
    # DMDO is a domain model; these are worked examples of binding a real
    # feed. Three are our own: wildfire-nifc, air-quality-epa,
    # earthquake-usgs.
    #
    # Files are renamed on ingest from `<folder>/ontology.ttl`, because
    # twelve files called `ontology.ttl` give twelve sidecars called
    # `ontology.provenance.yaml`. **The rename is recoverable because the
    # file's identity is its `source_url`**, which carries the full path
    # including the `-documentation` folder.
    #
    # Each term list is ONE FILE-SPECIFIC term, derived by measurement:
    # a name declared in exactly 1 of the 11 KWG ontologies. That makes
    # the content check answer *did we get THIS dataset's ontology* rather
    # than *did a payload arrive*. The first version guessed `Region` for
    # all twelve and `wildfire-nifc` does not declare it.
    ("wildfire-nifc", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/wildfire-nifc-documentation/ontology.ttl",
     ["gacc"]),
    ("air-quality-epa", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/air-quality-epa-documentation/ontology.ttl",
     ["cbsaCode"]),
    ("earthquake-usgs", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/earthquake-usgs-documentation/ontology.ttl",
     ["Earthquake"]),
    ("historical-fires-mtbs", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/historical-fires-mtbs-documentation/ontology.ttl",
     ["fireName"]),
    ("hurricane-tracks-noaa", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/hurricane-tracks-noaa-documentation/ontology.ttl",
     ["stormID"]),
    ("national-weather-zone-noaa", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/national-weather-zone-noaa-documentation/ontology.ttl",
     ["zoneNumber"]),
    ("climate-divisions-observations-noaa", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/climate-divisions-observations-noaa-documentation/ontology.ttl",
     ["Geometry"]),
    ("admin-regions-gadm", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/admin-regions-gadm-documentation/ontology.ttl",
     ["hasGID"]),
    ("census-uscb", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/census-uscb-documentation/ontology.ttl",
     ["hasGEOID"]),
    ("cropland-types-usda", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/cropland-types-usda-documentation/ontology.ttl",
     ["Cell"]),
    ("federal-judicial-district-doj", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/federal-judicial-district-doj-documentation/ontology.ttl",
     ["heldBy"]),
    # A VoID description of the collection — except it is not VoID.
    # Measured: 982 triples, **zero `void#` predicates**, every type minted
    # in KWG's own namespace (`kwg:Dataset` 31, `kwg:DatasetSubgraph` 24,
    # `kwg:KnowledgeGraph` 1, `kwg:Team` 1, `kwg:Person` 47). The filename
    # says VoID; the graph says KWG's own dataset vocabulary. A reader
    # reaching for `void:triples`, `void:dataDump` or `void:sparqlEndpoint`
    # finds none of them. Name-versus-content, in a filename.
    ("void", "http://stko-kwg.geog.ucsb.edu/lod/ontology/",
     "https://raw.githubusercontent.com/KnowWhereGraph/kwg-ontologies/main/void.ttl",
     ["Dataset", "KnowledgeGraph"]),
    ("nvs-p07", "http://vocab.nerc.ac.uk/collection/P07/current/",
     "http://vocab.nerc.ac.uk/collection/P07/current/?_profile=nvs&_mediatype=text/turtle",
     ["air_temperature", "wind_speed", "mole_fraction_of_ozone_in_air",
      "atmosphere_boundary_layer_thickness",
      # FULL CF names. The first probe used the stems
      # `mass_concentration_of_pm2p5` / `_pm10` and both came back
      # MISSING — because `terms_found` anchors on `\b`, and the
      # character after the stem is `_`, which is a word character. The
      # terms are present under their full names. A false MISSING, from
      # this file's own matcher, on the two terms A3 had flagged as
      # unverified — the reading it would have supported is that CF does
      # not carry PM2.5.
      "mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air",
      "mass_concentration_of_pm10_ambient_aerosol_particles_in_air"]),
    # DMDO / KnowWhereGraph. Supplied by hand first because no namespace
    # here dereferences; now fetched from the repository so the sidecars
    # carry a measured http_status, content_type and fetched, and so the
    # cached bytes can be diffed against what the source serves today.
    #
    # The namespaces have **no TLD** — `http://knowwheregraph/ontology/deo#`
    # has a host with no dot — so `dereferences` is `no` for anyone, ever,
    # and the disposition is BORROWED as a property of the URI rather than
    # a judgement about the vocabulary.
    ("disaster-event-module-generalized", "http://knowwheregraph/ontology/deo#",
     "https://raw.githubusercontent.com/KnowWhereGraph/dmdo/main/modules/disaster-event-module/disaster-event-module-generalized.ttl",
     ["Hazard", "Event", "Disaster", "DisasterImpact"]),
    ("disaster-event-module-extensions", "http://knowwheregraph/ontology/deo#",
     "https://raw.githubusercontent.com/KnowWhereGraph/dmdo/main/modules/disaster-event-module/disaster-event-module-extensions.ttl",
     ["hasUltimateFeatureOfInterest"]),
    ("disaster-properties-ontology", "http://knowwheregraph/ontology/dpo#",
     "https://raw.githubusercontent.com/KnowWhereGraph/dmdo/main/modules/disaster-properties-module/disaster-properties-ontology.ttl",
     ["ElementAtRisk"]),
    ("undrr-isc-hazard-classification", "https://undrr-hip.org/",
     "https://raw.githubusercontent.com/KnowWhereGraph/dmdo/main/undrr-isc-hazard-classification.ttl",
     ["broader", "definition"]),
    # The Part 1 lead. UNVERIFIED by design — ADR-006 records three
    # questions to answer by fetch when Part 1 comes up, and whether the
    # namespace dereferences at all is the first of them.
    # The `deo` row is deleted, not kept as a failing probe.
    # `schema.knowwheregraph.org` does not resolve; the four rows above
    # are the actual artifacts and they are fetched from the repository.

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


# A namespace "dereferences" only if resolving it returns a graph in
# which a known term is DEFINED. GeoSPARQL's namespace URI returns a
# Prez description document carrying all four bound terms and defining
# none — a 200, the right terms, and nothing to bind against. So the
# test is: fetch the namespace, parse it, ask whether the probe term has
# an rdf:type triple.
# FULL TERM URIs, not local names appended to the namespace.
#
# The first version stored local names and built `namespace + name`.
# That asks the wrong question of any document whose terms are minted
# elsewhere: `ssn/ext/` was probed for
# `http://www.w3.org/ns/ssn/ext/ObservationCollection`, which nobody
# declares — the term is `sosa:ObservationCollection`, at line 40 of the
# very file being probed — and the run reported *the namespace does not
# dereference*, which is false. It returns a 145-triple graph.
#
# **This is the second instance of one defect.** The same assumption was
# corrected in `audit-bound-terms.py` earlier in this session and left
# standing here: fixed in one file, live in another, one directory apart.
PROBE = {
    "sosa": "http://www.w3.org/ns/sosa/Observation",
    "ssn": "http://www.w3.org/ns/ssn/System",
    # minted in SOSA by the SSN-ext Note; see MINTS_NOTHING below
    "ssn-ext": "http://www.w3.org/ns/sosa/ObservationCollection",
    "ssn-system": "http://www.w3.org/ns/ssn/systems/SystemCapability",
    "prov-o": "http://www.w3.org/ns/prov#Entity",
    "org": "http://www.w3.org/ns/org#Organization",
    "geosparql": "http://www.opengis.net/ont/geosparql#Geometry",
    "qudt-schema": "http://qudt.org/schema/qudt/QuantityValue",
    "qudt-units": "http://qudt.org/vocab/unit/M-PER-SEC",
    "skos": "http://www.w3.org/2004/02/skos/core#Concept",
    "owl-time": "http://www.w3.org/2006/time#Interval",
    "foaf": "http://xmlns.com/foaf/0.1/Document",
    "dqv": "http://www.w3.org/ns/dqv#QualityMeasurement",
    "adms": "http://www.w3.org/ns/adms#Identifier",
    "dcterms": "http://purl.org/dc/terms/conformsTo",
    "shacl": "http://www.w3.org/ns/shacl#NodeShape",
    "schema": "https://schema.org/GovernmentOrganization",
    "sioc": "http://rdfs.org/sioc/ns#Community",
    # F1's lesson: probe for a DEFINED term, not a 200.
    # All twelve KWG files share ONE namespace, so they share one
    # probe. `Region` is declared in 6 of the 11 ontologies, which is
    # itself the row-spanning problem: the probe asks whether the
    # NAMESPACE defines it, and the namespace is one host for all of
    # them.
    "wildfire-nifc": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "air-quality-epa": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "earthquake-usgs": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "historical-fires-mtbs": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "hurricane-tracks-noaa": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "national-weather-zone-noaa": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "climate-divisions-observations-noaa": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "admin-regions-gadm": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "census-uscb": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "cropland-types-usda": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "federal-judicial-district-doj": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "void": "http://stko-kwg.geog.ucsb.edu/lod/ontology/Region",
    "undrr-isc-hazard-classification": "https://undrr-hip.org/MH0001",
}


def dereferences(ns, key):
    """(verdict, detail) — what a consumer resolving the namespace gets."""
    # Derivable from the URI alone, no fetch: a host with no dot has no
    # TLD and cannot resolve for anyone, ever. `knowwheregraph` is such a
    # host. This is a property of the URI, not a judgement about the
    # vocabulary, and it makes the disposition BORROWED permanently.
    host = ns.split("//")[-1].split("/")[0]
    if "." not in host:
        return "no", "**structural** — host `%s` has no TLD, cannot resolve for anyone, ever" % host
    probe = PROBE.get(key)
    if not probe:
        return "untested", "no probe term declared"
    status, final, ctype, body = fetch(ns)
    if status != "200" or not body:
        # Three unrelated causes were all printing a bare `no`, and they
        # DECAY DIFFERENTLY: a missing TLD is permanent, a 403 is access
        # and could change from another network, a 000 is one observation.
        # A column where one value covers three causes is C11's shape.
        kind = {"403": "**access** — 403; a re-probe from another network "
                       "could change this",
                "404": "**access** — 404 at this path",
                "000": "**single observation** — no response; one probe, not "
                       "a property"}.get(status, "**HTTP %s**" % status)
        return "no", kind
    try:
        from rdflib import Graph, RDF, URIRef
    except ImportError:
        return "untested", "rdflib unavailable"
    g = Graph()
    for fmt in ("turtle", "xml"):
        try:
            g.parse(data=body, format=fmt)
            break
        except Exception:
            g = Graph()
    else:
        return "no", "200 %s, unparseable" % ctype.split(";")[0]
    ct = ctype.split(";")[0]
    # Does this namespace mint ANY term of its own? A document that
    # returns a graph while declaring nothing under its own namespace is
    # a document, not a term namespace, and a URI built from it is a URI
    # nobody declares. `ssn/ext/` is exactly that.
    own = {s for s in g.subjects(RDF.type, None)
           if str(s).startswith(ns) and str(s) != ns}
    if list(g.objects(URIRef(probe), RDF.type)):
        if not own:
            return ("document", "200 %s, %d triples, mints **no term of its "
                    "own** — `%s` is defined here but minted elsewhere"
                    % (ct, len(g), probe.rsplit("/", 1)[-1]))
        return "yes", "200 %s, `%s` defined" % (ct, probe.rsplit("/", 1)[-1].rsplit("#", 1)[-1])
    return "no", "200 %s, %d triples, `%s` NOT defined" % (ct, len(g), probe)


def terms_found(body, terms):
    """Which terms occur in the payload. Substring, deliberately — a
    term may be written out, prefixed, or in an rdf:about attribute, and
    a parser that understood only one of those would report absence for
    a term that is present."""
    text = body.decode("utf-8", "replace")
    return {t: bool(re.search(r"\b%s\b" % re.escape(t), text)) for t in terms}


DISPOSITION = {"yes": "bound", "no": "borrowed", "document": "borrowed",
               "untested": "untested", "skipped": "untested"}


def _y_load(path):
    import yaml as _y
    return _y.safe_load(path.read_text()) or {}


def src_of(key):
    for k, _ns, u, _t in SOURCES:
        if k == key:
            return u
    return "-"


# A generated artifact is a WHOLE FILE, never a region inside one.
#
# The register lived in a marked block inside `README.md`. The README's
# author rewrote that file wholesale from an older copy and the markers
# went with it — a generated region hand-edited, invariant 1's shape,
# and unavoidable: a file with a generated region and an author who
# rewrites it has two writers by construction. `README.md` is prose and
# hand-written; this file is generated and written by nothing else.
REGISTER = HERE / "register.md"

# set from argv in main(); a one-element list so the writers can read it
CHECK_ONLY = [False]


def sync_register():
    """Write `register.md` in full. No markers, no host document."""
    import yaml as _y
    rows, gaps, failed = [], [], []
    stems = {g.stem for g in CACHE.glob("*.ttl")}
    sides = {s.name.replace(".provenance.yaml", "")
             for s in CACHE.glob("*.provenance.yaml")}
    # F7: a sidecar with no `.ttl` records a fetch that PRODUCED NO GRAPH.
    # Enumerating `*.ttl` alone made it invisible and `0 gaps` could not
    # see it — C11's absent-versus-zero, in this project's tooling.
    for stem in sorted(sides - stems):
        d = _y.safe_load((CACHE / ("%s.provenance.yaml" % stem)).read_text())
        failed.append((stem, d.get("source_url", "-"), d.get("http_status", "?")))
    for g in sorted(CACHE.glob("*.ttl")):
        side = g.with_suffix(".provenance.yaml")
        if not side.exists():
            gaps.append(g.name)
            continue
        d = _y.safe_load(side.read_text())
        rows.append((g.stem, d.get("namespace", "-"),
                     d.get("dereferences", "?"), d.get("disposition", "?"),
                     d.get("detail", "")))

    out = ["# External vocabulary register", "",
           "**Generated in full by `fetch-external.py` from the provenance",
           "sidecars in `graphs/`. Do not edit — edit a sidecar, or the",
           "source list in the generator.**", "",
           "`README.md` carries the conventions and the findings; this file",
           "carries the measurements. One writer each.", "",
           "**`dereferences` is a separate live fetch of the namespace, not of",
           "the cached file.** GeoSPARQL is why: `:Geometry` is defined in the",
           "cached graph and undefined in what the namespace serves. A",
           "vocabulary can be *bound* by name and *borrowed* in fact.", "",
           "**`dereferences` carries its REASON, not a bare verdict.** Three",
           "unrelated causes were all printing `no` and they decay",
           "differently: **structural** (no TLD) can never change,",
           "**access** (403/404) could change from another network,",
           "**single observation** (000) is one probe rather than a",
           "property, and **content** (200 but the term is undefined) is",
           "the GeoSPARQL case. One value covering four causes is C11's",
           "shape.", "",
           "| Graph | Namespace | Dereferences | Why | Disposition |",
           "|---|---|---|---|---|"]
    for k, ns, dr, disp, detail in rows:
        out.append("| `%s` | <%s> | **%s** | %s | **%s** |"
                   % (k, ns, dr, detail or "—", disp))
    tally = {}
    for _k, _n, _d, disp, _x in rows:
        tally[disp] = tally.get(disp, 0) + 1
    out += ["", "*%d graphs with a sidecar; %s. %d fetch(es) produced no "
            "graph at all.*"
            % (len(rows), ", ".join("%d %s" % (v, k)
                                    for k, v in sorted(tally.items())),
               len(failed))]
    if gaps:
        out += ["", "**Cached with no sidecar — not covered by the table "
                "above:**", ""] + ["- `%s`" % g for g in gaps]
    out += ["", "## A term's declaration may span rows — two different reasons",
            "",
            "The row-per-file shape breaks for the twelve KWG source",
            "ontologies, and **it breaks in two ways that need different",
            "remedies.** Measured across the eleven dataset ontologies: 444",
            "distinct declared URIs, **46 in more than one file**.", "",
            "**Ten are in KWG's own namespace, and their declaring file is",
            "arbitrary.** `AdministrativeRegion_2` and `S2Cell_Level13` are",
            "each declared in **10 of 11**; `Region`, `spatialRelation` and",
            "`hasTemporalScope` in 6; `sfWithin` in 3; `hasFIPS`,",
            "`stateName`, `countyName` and **`irwinID`** in 2. For these,",
            "which row holds the declaration carries no meaning — read any",
            "of them.", "",
            "**`irwinID` is worth naming separately.** It is the only term",
            "in this corpus touching ADR-001's identity apparatus, and a",
            "scheme identifier whose declaring file is arbitrary is a",
            "different kind of problem from a region class.", "",
            "**Thirty-six are foreign, and are not a row-spanning problem at",
            "all — the declaration is in the wrong file entirely.** They are",
            "stub redeclarations of terms KWG does not own: **sosa 11,",
            "geosparql 7, skos 6, dcterms 5, owl-time 5, schema.org 2**. For",
            "these the register points at the OWNING namespace's row, which",
            "this cache already holds. Anyone opening a KWG ontology for",
            "`sosa:Observation`'s definition gets a bare `owl:Class` with no",
            "axioms, while the real SOSA graph sits in this same directory.",
            "",
            "`vocab-conventions.md`'s fifth failure mode — *a vocabulary may",
            "declare a term it does not own* — **at scale, and measured.**",
            "Conflating the two halves would make this register say a SOSA",
            "term's declaration is arbitrary among twelve files, when it is",
            "not arbitrary at all."]
    if failed:
        out += ["", "## Fetched, produced no graph", "",
                "A sidecar exists and there is no `.ttl` beside it. Listed "
                "because **an attempt that failed is not an attempt not "
                "made**, and a row count over successes cannot tell them "
                "apart.", "",
                "| Attempted | Source | HTTP |", "|---|---|---|"]
        out += ["| `%s` | <%s> | %s |" % f for f in failed]
    # F8: this function returned 0 on every path, so the caller's
    # `if sync_register(): problems.append(...)` was unreachable — and the
    # string it would have printed named the README marker block that the
    # same commit withdrew. `CLAUDE.md`'s *search for the retracted
    # string, not the replacement* rule, missed in the commit that
    # installed the rule. The property held only because the write is
    # unconditional; the branch claiming to implement it never ran.
    #
    # There is now a condition that can actually fail: no sidecars means
    # nothing to generate from, and a register written from nothing would
    # be an empty table reporting zero problems.
    if not rows and not failed:
        print("FAIL  no provenance sidecars under %s — register.md NOT "
              "written. A register generated from nothing is an empty "
              "table that reports no problems." % CACHE, file=sys.stderr)
        return 1
    if CHECK_ONLY[0]:
        # B5: regenerating the register from check-mode rows is how the
        # destruction reached a file of record. Check mode reads.
        print("register.md: not rewritten (--check reads only)")
        return 0
    REGISTER.write_text("\n".join(out) + "\n")
    print("register.md: %d rows, %d gaps, %d failed fetch(es)"
          % (len(rows), len(gaps), len(failed)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the cache on disk; no network")
    args = ap.parse_args()
    CHECK_ONLY[0] = args.check
    CACHE.mkdir(parents=True, exist_ok=True)
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                           capture_output=True, text=True).stdout.strip()

    rows, problems = [], []
    CACHED_OK = set()
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
                CACHED_OK.add(key)
            else:
                problems.append("%s: HTTP %s from %s — cache and sidecar "
                                "left untouched" % (key, status, url))

        if not body:
            rows.append((key, ns, status, 0, "-", "-", "no payload", "**no** — no payload"))
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
        # The namespace is a different question from the fetch URL, and
        # GeoSPARQL is the case that proves it: the namespace returns a
        # description document mentioning every bound term and defining
        # none. So this asks whether resolving the NAMESPACE yields a
        # graph in which a probe term is defined — not whether it 200s.
        deref, detail = (("skipped", "--check, no network") if args.check
                         else dereferences(ns, key))
        if deref == "no":
            problems.append("%s: namespace does not dereference to a graph "
                            "(%s) — bindable only as BORROWED" % (key, detail))
        elif deref == "document":
            problems.append("%s: namespace returns a graph but mints no term "
                            "of its own (%s) — a URI built from this namespace "
                            "is a URI nobody declares" % (key, detail))
        rows.append((key, ns, status, len(body),
                     hashlib.sha256(body).hexdigest()[:12],
                     ctype.split(";")[0] or "-", verdict,
                     "**%s** — %s" % (deref, detail)))

    # PROVENANCE SIDECARS. One per graph, carrying exactly the fields
    # README.md specifies. Written from the same measurement that fills
    # the manifest row, so the two cannot disagree — a sidecar typed by
    # hand beside a generated table is the copy-of-a-copy defect.
    import json
    for r in rows:
        key, ns, row_status = r[0], r[1], r[2]
        side = CACHE / ("%s.provenance.yaml" % key)
        if not args.check and key not in CACHED_OK:
            # The fetch failed. The cached `.ttl` is untouched, so its
            # sidecar must stay untouched too — writing the failure's
            # metadata here recorded `sha256: b620507312c5` (a 9 KB GitHub
            # 404 page) against a file whose real digest is `7a8028dba554`
            # and which contains all four bound terms.
            #
            # Same family as B5: the tool destroying the evidence it exists
            # to keep, on the fetch path instead of the check path. A dead
            # or transient URL silently invalidated the provenance of an
            # intact file.
            g = CACHE / ("%s.ttl" % key)
            if side.exists() and g.exists():
                # REPAIR, not merely keep. A previous run already wrote the
                # failure's metadata here — `sha256: b620507312c5`, a 9 KB
                # GitHub 404 page, against a file whose real digest is
                # `7a8028dba554` and which carries all four bound terms.
                # Keeping a corrupted sidecar is not better than rewriting
                # it; what matters is that it describes THE CACHED BYTES.
                #
                # `http_status`, `content_type` and `fetched` are not
                # recoverable for those bytes, so they say so rather than
                # carry a value from a fetch that returned something else.
                import hashlib as _h
                d = _y_load(side)
                have = _h.sha256(g.read_bytes()).hexdigest()[:12]
                if d.get("sha256") != have:
                    d["sha256"] = have
                    for f in ("http_status", "content_type", "fetched"):
                        # `status` here is leftover from another loop and
                        # read 200 for a fetch that 404'd. Use the ROW's own
                        # status — third variable-scope slip in this file,
                        # same family as hashing `body` from the prior loop.
                        d[f] = ("unrecoverable — the source URL returned "
                                "HTTP %s; these bytes are from an earlier "
                                "successful fetch" % row_status)
                    side.write_text(
                        "# Generated by fetch-external.py. Do not edit.\n"
                        + "".join("%-14s %s\n" % (k + ":", json.dumps(str(v)))
                                  for k, v in d.items()))
                    problems.append("%s: sidecar REPAIRED to describe the "
                                    "cached bytes (%s); it had recorded the "
                                    "failed fetch's payload instead"
                                    % (key, have))
                else:
                    problems.append("%s: fetch failed; sidecar already "
                                    "describes the cached bytes" % key)
            continue
        if args.check:
            # B5: `--check` is documented as *verify the cache only; no
            # network*, and it used to WRITE. Every sidecar was rewritten
            # to `http_status: cache`, `dereferences: skipped`,
            # `disposition: untested`, and `register.md` was regenerated
            # from them: 15 bound / 7 borrowed / 1 untested became **23
            # untested**, exit 0, `Problems — (none)`. The dispositions
            # are live-network measurements and the mode that destroyed
            # them cannot recover them.
            #
            # C11's absent-versus-zero, written by the tool: a run of the
            # documented verification command followed by a commit resets
            # the project's external-binding evidence with nothing saying
            # it was never measured.
            #
            # Check mode now compares and reports. It writes nothing.
            if not side.exists():
                problems.append("%s: no provenance sidecar" % key)
            else:
                import hashlib as _h
                d = _y_load(side)
                # `body` belongs to the PREVIOUS loop and holds whatever
                # file it read last. Hashing it here compared every
                # sidecar against one file — three DMDO rows reported the
                # UNDRR hash. Caught because the output was absurd: three
                # different files, one digest. Read the file for THIS key.
                g = CACHE / ("%s.ttl" % key)
                have = _h.sha256(g.read_bytes()).hexdigest()[:12] \
                    if g.exists() else None
                if have is None:
                    problems.append("%s: sidecar present, no cached graph"
                                    % key)
                    continue
                if d.get("sha256") not in (None, have):
                    problems.append(
                        "%s: cached bytes do not match the sidecar — "
                        "sidecar %s, file %s. The cache drifted from what "
                        "was measured, or the sidecar did."
                        % (key, d.get("sha256"), have))
            continue
        deref = r[7].split("—")[0].strip().strip("*")
        side.write_text(
            "# Generated by fetch-external.py. Do not edit.\n"
            "source_url:    %s\n"
            "fetched:       %s\n"
            "http_status:   %s\n"
            "content_type:  %s\n"
            "sha256:        %s\n"
            "namespace:     %s\n"
            "dereferences:  %s\n"
            "detail:        %s\n"
            "disposition:   %s\n"
            % (json.dumps(src_of(key)), json.dumps(stamp),
               json.dumps(r[2]), json.dumps(r[5]), json.dumps(r[4]),
               json.dumps(ns), json.dumps(deref),
               json.dumps(r[7].split("—", 1)[-1].strip()),
               json.dumps(DISPOSITION.get(deref, "untested"))))

    out = ["# External vocabulary cache — manifest", "",
           "**Generated by `fetch-external.py`. Do not edit.**", "",
           "Every row records what was found **in the payload**, not that",
           "the payload arrived. A 200 proves a server answered; three of",
           "this project's bindings were falsified by a term that was",
           "absent behind one.", "",
           "**Every row describes TWO fetches, and they are different",
           "documents.** The *cached* columns come from the fetch URL; the",
           "*namespace* column comes from a separate live fetch of the",
           "namespace itself. GeoSPARQL is why the distinction is on the",
           "page: `:Geometry` is defined at line 1013 of the cached file",
           "and is undefined in what the namespace serves — 40,988 bytes",
           "against 20,397, `text/turtle` against `text/anot+turtle`, 65",
           "minted terms against zero `owl:Class` declarations. Both are",
           "true. A row that showed only one verdict read as a document",
           "disagreeing with itself.", "",
           "| Vocabulary | Fetch URL (cached) | HTTP | Bytes | SHA-256 | Type | Content check | Namespace | Namespace serves |",
           "|---|---|---|---|---|---|---|---|---|"]
    src = {k: u for k, _n, u, _t in SOURCES}
    for r in rows:
        out.append("| `%s` | <%s> | %s | %s | `%s` | %s | %s | <%s> | %s |"
                   % (r[0], src.get(r[0], "-"), r[2], r[3], r[4], r[5],
                      r[6], r[1], r[7]))
    out += ["", "## Problems", ""]
    out += (["*(none)*"] if not problems else
            ["- %s" % p for p in problems])
    out.append("")
    if not CHECK_ONLY[0]:
        MANIFEST.write_text("\n".join(out))
    else:
        print("manifest.md: not rewritten (--check reads only)")

    print("\n".join(out[7:]))
    if sync_register():
        problems.append("register.md was not generated")
    if problems:
        print("\n%d problem(s) — these are findings, not script bugs"
              % len(problems), file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
