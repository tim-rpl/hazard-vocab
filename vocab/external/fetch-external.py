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
    # ADDED, not substituted, 2026-08-07. The W3C document is being edited
    # under a live binding: 11,134 -> 12,687 bytes between two fetches in
    # one session, and the earlier copy carried
    # `# deprecated - now maintained by Semic (see adms.var)` while the
    # newer one does not. A switch made now binds to whichever side of a
    # migration the fetch happens to catch.
    #
    # So both are cached and the question was answered MECHANICALLY rather
    # than argued.
    #
    # **ANSWERED, and the strong form is not licensed.** Both URLs serve
    # 12,687 bytes, digest `c79e72752851`, byte-identical by `cmp`, both
    # declaring 2/2 terms as typed subjects under `w3.org/ns/adms#`.
    #
    # `cmp`-identical bytes licenses *two documents that agree today*, not
    # *one document*. The test that settles it is the redirect, and it
    # answers a **third** way:
    #
    #   `https://www.w3.org/ns/adms.ttl`
    #     -> HTTP/2 **307 Temporary Redirect**
    #        location: https://uri.semic.eu/w3c/ns/adms.ttl
    #
    # Not a 200, so they are not two independently served files. Not a
    # 301/302 either. **A 307 says THIS URL IS TEMPORARILY SERVING FROM
    # THAT URL** — it does not say the origin has no document of its own,
    # only that it is not serving it right now.
    #
    # So the licensed statement is: **two URLs currently resolve to one
    # body, revocably.** Not *there is one document* — the evidence below
    # names a w3.org document that existed and was retired, which is the
    # second document the strong phrasing denies. Third restatement of
    # this sentence; the first two each claimed more than the measurement
    # carried. `resolved_url` in each sidecar records the redirect rather
    # than leaving it to a hand probe with no residue.
    #
    # And the timeline is now exact. SEMIC's file carries
    # `last-modified: Mon, 22 May 2023`, unchanged for three years, while
    # this cache moved 11,134 -> 12,687 bytes within one session. So
    # nothing was EDITED: **w3.org turned the redirect on between two of
    # our fetches**, and the 11,134-byte copy carrying
    # `# deprecated - now maintained by Semic` was w3.org's own, which it
    # has stopped serving. Inference, from the last-modified date and the
    # banner, not from a fetch of the retired document — that is no longer
    # reachable.
    #
    # **The conclusion this comment used to draw is DELETED, not
    # repaired.** It read that `CLAUDE.md`'s ADMS line needs no
    # disambiguation while the redirect stands. **`CLAUDE.md` has never
    # named ADMS** — `grep -niE 'adms|semic'` matches nothing and
    # `git log --all -S adms -- CLAUDE.md` finds no commit. Its bound list
    # is SOSA, PROV-O, QUDT and CF, and the paragraph explicitly declines
    # to make per-namespace claims at all. Three passes were spent
    # sharpening a sentence about a referent that does not exist.
    #
    # What the peer check is for, stated without it: if the redirect is
    # withdrawn, w3.org serves a second document and the guard says so.
    #
    # The row stays. It cost 12 KB and one register row to replace an
    # argument with a measurement, and it keeps replacing it: `DIGEST_PEER`
    # below now fails if the two ever stop agreeing, which is the only
    # form in which "they are the same document" can remain true rather
    # than having been true once.
    #
    # No `PROBE` entry: the namespace is the same URI `adms` already
    # probes, and probing it twice measures one thing twice.
    ("adms-semic", "http://www.w3.org/ns/adms#",
     "https://uri.semic.eu/w3c/ns/adms.ttl",
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
    # ELEVEN KWG source-specific ontologies — one per dataset — plus
    # `void.ttl`, which is NOT one of them. F16: this read *twelve* and
    # *one per dataset*, and the twelfth is the catalogue whose own
    # section below shows it is a collection description, not a dataset
    # ontology. The heading was wrong by exactly the file the section
    # beneath it proves is not one. Eleven is the number every
    # measurement here uses. These are the
    # profile-level artifacts `vocab/profiles/` exists for and has none of.
    # DMDO is a domain model; these are worked examples of binding a real
    # feed. Three are our own: wildfire-nifc, air-quality-epa,
    # earthquake-usgs.
    #
    # Files are renamed on ingest from `<folder>/ontology.ttl`, because
    # eleven files called `ontology.ttl` give eleven sidecars called
    # `ontology.provenance.yaml`. **The rename is recoverable because the
    # file's identity is its `source_url`**, which carries the full path
    # including the `-documentation` folder.
    #
    # Each term list is ONE FILE-SPECIFIC term, derived by measurement:
    # a name declared in exactly 1 of the 11 KWG ontologies. That makes
    # the content check answer *did we get THIS dataset's ontology* rather
    # than *did a payload arrive*. The first version guessed `Region` for
    # all eleven and `wildfire-nifc` does not declare it.
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
    # CF Standard Names, the BOUND route. Same authority and same NVS2
    # service as P07 below, and it carries the same terms with READABLE
    # local parts: `…/standard_name/air_temperature/` against P07's
    # `…/P07/current/00B3H4MY/`. That is not cosmetic — ADR-000 D5 chose
    # SKOS partly for cross-scheme mapping, and a binding nobody can
    # review by eye is an unverifiable act every time it is made.
    #
    # SCHEME: `http://`, not `https://`. The declared subjects are `http`;
    # `https` would mint URIs nothing declares, and it is precisely the
    # hole `declared-prefix` does not cover — the prefix would be declared
    # and `jurisdiction` would pass it, the host being unchanged.
    #
    # TRAILING SLASH: every one of the 5,676 subjects ends in `/`. The
    # CURIE carries it — `cfsn:air_temperature/` — and it does NOT reach
    # the emitted Turtle: `gen-shacl` writes
    # `sh:path <http://vocab.nerc.ac.uk/standard_name/air_temperature/>`,
    # a full URI with no prefixed name, and the result reparses. Tested
    # before binding, which is invariant 4: what appears in the generated
    # shapes, not what the source language accepts.
    #
    # All SIX of OHIM's CF names are probed, not one. One would clear
    # `vocab-conventions.md` check 5 while proving nothing about the
    # other five.
    ("cf-standard-name", "http://vocab.nerc.ac.uk/standard_name/",
     "http://vocab.nerc.ac.uk/standard_name/?_profile=nvs&_mediatype=text/turtle",
     ["air_temperature", "wind_speed", "mole_fraction_of_ozone_in_air",
      "atmosphere_boundary_layer_thickness",
      "mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air",
      "mass_concentration_of_pm10_ambient_aerosol_particles_in_air"]),
    # SUPERSEDED as the CF route, 2026-08-06, by `cf-standard-name` above.
    # Retained as a cached artifact because it is the graph the
    # measurement was made against — 5,686 concepts, every subject ending
    # in `/`, **0 with a local part any reader can align to a CF name**.
    # Nothing binds from it, so it stays unprobed and reads
    # `disposition: untested`, which is the honest record for a
    # collection this project cites and does not use.
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
# A fact about a namespace that a future reader will trip over, carried
# into the sidecar's `detail` beside the measured verdict. Not a
# substitute for a field — `dereference_reason` exists because free text
# could not be counted (F14) — but the shape of a URI is not a category,
# and the alternative is that someone redoes the reasoning.
# Sources that MUST cache byte-identical payloads, and why. A pair here
# asserts a claim about the world — *these two URLs resolve to one body* —
# which is true when measured and can stop being true silently. The
# register would then carry two rows that agree by habit.
DIGEST_PEER = {
    ("adms", "adms-semic"):
        "W3C 307s to SEMIC, so both URLs currently resolve to one body. "
        "A 307 is the origin DECLINING to serve its own copy, revocably — "
        "if w3.org resumes serving it, a second document is back in play "
        "and the register must stop implying otherwise",
}

SIDECAR_NOTE = {
    "cf-standard-name":
        "Every subject ends in a trailing `/`; the CURIE carries it "
        "(`cfsn:air_temperature/`); it does NOT reach the emitted Turtle — "
        "`gen-shacl` writes the full URI in angle brackets and the result "
        "reparses. Scheme is `http`, not `https`",
}

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
    # Trailing slash included — it is part of the declared URI, and a
    # probe without it asks about a term nobody minted.
    "cf-standard-name": "http://vocab.nerc.ac.uk/standard_name/air_temperature/",
    # F1's lesson: probe for a DEFINED term, not a 200.
    # All eleven KWG ontologies plus `void.ttl` share ONE namespace, so
    # they share one
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
        return "no", "structural", "host `%s` has no TLD — cannot resolve for anyone, ever" % host
    probe = PROBE.get(key)
    if not probe:
        return "untested", "no-probe", "no probe term declared"
    status, final, ctype, body = fetch(ns)
    if status != "200" or not body:
        # Three unrelated causes were all printing a bare `no`, and they
        # DECAY DIFFERENTLY: a missing TLD is permanent, a 403 is access
        # and could change from another network, a 000 is one observation.
        # A column where one value covers three causes is C11's shape.
        code, kind = {
            "403": ("access", "403 — a re-probe from another network could change this"),
            "404": ("access", "404 at this path"),
            "301": ("access", "301, and the redirect target did not serve a graph"),
            "000": ("single-observation", "no response — one probe, not a property"),
        }.get(status, ("access", "HTTP %s" % status))
        return "no", code, kind
    try:
        from rdflib import Graph, RDF, URIRef
    except ImportError:
        return "untested", "no-parser", "rdflib unavailable"
    g = Graph()
    for fmt in ("turtle", "xml"):
        try:
            g.parse(data=body, format=fmt)
            break
        except Exception:
            g = Graph()
    else:
        # SPLIT from `content`, 2026-08-07. One value covered two causes
        # that decay differently, in the field added to stop exactly that
        # (F14) — the fourth time in this column and the first inside the
        # repair for it. `adms` is why it mattered: its namespace began
        # serving `text/html`, which is content negotiation and could
        # change tomorrow, and the column reported it identically to
        # GeoSPARQL's `Geometry`-absent-from-a-real-graph, which is a
        # modelling fact about the vocabulary.
        return ("no", "not-a-graph",
                "200 %s, and it does not parse as RDF — what the namespace "
                "serves is not a graph" % ctype.split(";")[0])
    ct = ctype.split(";")[0]
    # Does this namespace mint ANY term of its own? A document that
    # returns a graph while declaring nothing under its own namespace is
    # a document, not a term namespace, and a URI built from it is a URI
    # nobody declares. `ssn/ext/` is exactly that.
    # The last segment of the probe URI, for the human-readable detail.
    # `rsplit("/", 1)[-1]` returns the EMPTY STRING for a URI ending in a
    # slash, and every one of CF Standard Names' 5,676 subjects does —
    # the first `cf-standard-name` run reported ``  `` defined ``, a
    # verdict naming no term. The label is cosmetic and the verdict was
    # right, which is exactly why it would have survived: nothing about
    # the run looked wrong except a pair of empty backticks.
    def label(u):
        return u.rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1] or u

    own = {s for s in g.subjects(RDF.type, None)
           if str(s).startswith(ns) and str(s) != ns}
    if list(g.objects(URIRef(probe), RDF.type)):
        if not own:
            return ("document", "mints-nothing", "200 %s, %d triples, mints **no term of its "
                    "own** — `%s` is defined here but minted elsewhere"
                    % (ct, len(g), label(probe)))
        return "yes", "resolves", "200 %s, `%s` defined" % (ct, label(probe))
    return "no", "content", ("200 %s, %d triples, but `%s` is NOT defined "
                             "in what the namespace serves" % (ct, len(g), probe))


# The verdict each reason implies. This is a SECOND statement of what
# `dereferences()` returns, so it is asserted against that function rather
# than trusted: `_assert_reason_map()` walks every literal return in the
# source and fails if any pair is missing or disagrees. A hand-written map
# beside the code it describes is the hand-maintained duplicate this
# project keeps paying for — B8 is the same defect in a heading.
REASON_VERDICT = {
    "structural": "no",
    "access": "no",
    "single-observation": "no",
    "content": "no",
    "not-a-graph": "no",
    "mints-nothing": "document",     # NOT "no" — a document resolves
    "resolves": "yes",
    "no-probe": "untested",
    "no-parser": "untested",
}


def _assert_reason_map():
    """Every `(verdict, reason)` pair `dereferences()` can return must be
    in REASON_VERDICT and must agree with it.

    Written because my first version of `check_reason_agrees` GUESSED the
    map — `mints-nothing` was assumed to imply `no` — and the guess
    reported a false positive against `ssn-ext`, a sidecar that was right.
    An instrument asserting a relation it invented is C22's shape.
    """
    src = pathlib.Path(__file__).read_text()
    body = src.split("def dereferences(", 1)[1].split("\ndef ", 1)[0]
    pairs = set(re.findall(r'return \(?"(\w+)", "([\w-]+)"', body))
    pairs |= {(v, r) for v, r in
              re.findall(r'"(\w+)", \{[^}]*\}\.get', body)}   # none today
    # the dict-dispatched access/single-observation codes
    for reason in re.findall(r'\("([\w-]+)", "[^"]*"\),', body):
        pairs.add(("no", reason))
    bad = ["%s -> %s (map says %s)" % (r, v, REASON_VERDICT.get(r))
           for v, r in sorted(pairs) if REASON_VERDICT.get(r) != v]
    if bad:
        raise AssertionError("REASON_VERDICT disagrees with dereferences(): "
                             + "; ".join(bad))
    return sorted(pairs)


def terms_found(body, terms):
    """Which terms OCCUR in the payload. Substring, deliberately — a
    term may be written out, prefixed, or in an rdf:about attribute, and
    a parser that understood only one of those would report absence for
    a term that is present.

    This is a PRESENCE CENSUS and not a binding test. B7: the column it
    fed said `6/6 terms present` for `cf-standard-name`, whose six names
    are typed subjects, and `6/6 terms present` for `nvs-p07`, where
    **0 of 6** are — P07's subjects are `…/current/00B3H4MY/` and the
    names appear only as labels. Identical wording, same column, opposite
    facts, and the subject-versus-label distinction is exactly what the
    CF route change rests on.

    `vocab-conventions.md`'s *parse the body and find the term* is the
    rule for a BINDING; this is fine for a census. Both are kept and the
    column is labelled for what it measures — see `terms_declared`.
    """
    text = body.decode("utf-8", "replace")
    return {t: bool(re.search(r"\b%s\b" % re.escape(t), text)) for t in terms}


def terms_declared(body, ns, terms):
    """Which terms are TYPED SUBJECTS in the parsed graph.

    The strong test `terms_found` is not. A name counts only if some
    subject carrying an `rdf:type` has a URI under `ns` whose last
    segment — trailing slash stripped, because every CF Standard Name
    subject ends in one — equals the name.

    Returns None when the payload does not parse, so *unparseable* and
    *nothing declared* stay distinguishable; a single boolean would make
    them the same cell, which is C11's shape.
    """
    n = _parse_graph(body)
    if n is None:
        return None
    g, RDF = n
    out = {}
    subs = {}
    for s in set(g.subjects(RDF.type, None)):
        u = str(s)
        if u.startswith(ns):
            subs.setdefault(u.rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1],
                            u)
    for t in terms:
        out[t] = t in subs
    return out


def _parse_graph(raw):
    """(graph, RDF) or None. Both serialisations, quietly — two cached
    `.ttl` files are RDF/XML."""
    try:
        from rdflib import Graph, RDF
    except ImportError:
        return None
    import logging
    lg = logging.getLogger("rdflib")
    prior = lg.level
    lg.setLevel(logging.ERROR)
    try:
        for fmt in ("turtle", "xml"):
            g = Graph()
            try:
                g.parse(data=raw, format=fmt)
                return g, RDF
            except Exception:
                continue
        return None
    finally:
        lg.setLevel(prior)


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
CACHE_STATE = [None]      # set once in main(); see cache_state()


# The causes of non-dereference and how each decays. ONE source for both
# the count in the heading and the rows of the table — B8 is what a
# hand-maintained count beside its own table costs, twice in two rounds.
DECAY = [
    ("structural", "never — a host with no TLD cannot resolve for anyone"),
    ("access", "403/404/301/expired cert — could change from another network"),
    ("single-observation", "`000`, no response — one probe, not a property"),
    ("content", "200 and a real graph, but the probe term is not defined "
                "in it — a fact about the VOCABULARY, and stable"),
    ("not-a-graph", "200, and the body does not parse as RDF at all — "
                    "content negotiation, and could change tomorrow"),
    ("mints-nothing", "200 and a graph, but no term under its own namespace"),
]


def manifest_comparable(text):
    """The part of `manifest.md` a check-mode run can legitimately compare.

    B10: `manifest.md` had NO comparison at all. O replaced line 7 — header
    prose — with *"THIS LINE WAS HAND-EDITED BY O AND IS FALSE."* and
    `make lint` exited 0: a tracked, wholly generated file of record
    carrying a false hand-written line at a green build.

    It cannot be compared whole, and that is the honest reason it had no
    check rather than an excuse for none. Three per-row cells are live
    measurements a `--check` run does not make — **HTTP**, **Type** and
    **Namespace serves** read `cache`, `-` and `skipped` offline — and the
    `## Problems` section is a report about THIS run. Everything else is
    generator-controlled and must match: all header prose, and per row the
    vocabulary, URL, byte count, digest and content verdict.

    So the comparison is narrowed to what is knowable, and says so. A
    narrowed check that names its scope is not the same artifact as no
    check; the failure it cannot see is stated instead of implied.
    """
    # BLANKED BY NAME, not by position. This read `LIVE = {3, 6, 9}` and
    # I nominated it for attack on the ground that a column inserted
    # before index 9 would silently shift what is compared, the run still
    # reporting success. B7 then added *Terms declared* at index 8 and it
    # did exactly that — the nomination, collected. Positions are read
    # off the header row, so the header is the single source and a moved
    # column moves with it.
    LIVE = {"HTTP", "Type", "Namespace serves"}
    out, live_idx = [], None
    for line in text.split("## Problems")[0].splitlines():
        if line.startswith("| Vocabulary |"):
            names = [c.strip() for c in line.strip().strip("|").split("|")]
            live_idx = {i for i, n in enumerate(names) if n in LIVE}
            missing = LIVE - {n for n in names}
            if missing:
                raise AssertionError(
                    "manifest_comparable: no column named %s — the header "
                    "changed and this would have silently compared the "
                    "wrong cells" % sorted(missing))
        elif line.startswith("| `"):
            if live_idx is None:
                raise AssertionError(
                    "manifest_comparable: a data row before the header row")
            cells = line.strip().strip("|").split("|")
            cells = ["" if i in live_idx else c for i, c in enumerate(cells)]
            line = "|%s|" % "|".join(cells)
        out.append(line)
    # rstrip: the committed file has a blank line before `## Problems` and
    # the in-memory form is compared before that heading is appended, so
    # the two differ by one trailing empty line and nothing else. That
    # reported `0 line(s) differ` — a drift report naming no drifted line,
    # which is C11's absent-versus-zero in a diagnostic.
    return "\n".join(out).rstrip()


# THE CACHE'S STATE SPACE, enumerated before it is checked.
#
# Three consecutive repairs fixed three states of ONE defect, each
# authored and verified in the state it was written for: an emptied
# cache (C22 row 21), a truncated table from a missing graph (row 22),
# and a graph that is present and parseable and defines nothing (row 23).
# The common cause is that `cache_state()` compared FILENAMES against
# `git ls-files` and read no bytes.
#
#   | # | State                          | filename | digest | parse |
#   |---|--------------------------------|----------|--------|-------|
#   | 1 | unfetched (cached == tracked)  | catches  |   —    |   —   |
#   | 2 | a listed graph has no file     | catches  | catches| catches|
#   | 3 | zero-byte file                 | MISSES   | catches| catches|
#   | 4 | truncated file                 | MISSES   | catches| catches|
#   | 5 | wrong document served & cached | MISSES   | catches| MISSES|
#   | 6 | valid graph, zero triples      | MISSES   | MISSES | catches|
#   | 7 | `.ttl` holding RDF/XML         | MISSES   | MISSES | catches|
#
# So neither predicate alone closes it and the pair does. Digest catches
# any drift from the bytes that were measured; parse catches bytes that
# were always bad, which a sidecar written from them would agree with.
#
# State 7 is not hypothetical and is why the parse tries two formats:
# **`foaf.ttl` and `skos.ttl` are RDF/XML.** A Turtle parse of either
# RAISES, so a single-format predicate would report the cache degraded on
# every run, forever — a guard that cannot be satisfied gets deleted.
def cache_state(keys=None):
    """`unfetched` | `complete` | `partial` | `degraded`, plus the reasons.

    F19: the cache is INPUT and `graphs/*.ttl` is gitignored, so a fresh
    clone must not fail. `unfetched` is the `.gitkeep` case — note what
    was inspected and pass. The literal test *zero `.ttl`* is never true
    on a clone, because the four hand-supplied graphs are tracked; the
    test is **cached == tracked**.

    `keys` limits the byte-level checks to the graphs a caller actually
    reads. `audit-bound-terms.py` passes its six; a caller that reads
    everything passes None. Parsing all 36 costs ~4.8s and the six cost
    a fraction of that, so the scope is a real saving and not a dodge —
    a degraded graph nobody reads cannot corrupt the file being written.
    """
    cached = {p.name for p in CACHE.glob("*.ttl")}
    try:
        out = subprocess.run(["git", "ls-files", "graphs/*.ttl"],
                             cwd=str(CACHE.parent), capture_output=True,
                             text=True, timeout=10)
        tracked = {pathlib.Path(l).name for l in out.stdout.split() if l}
    except Exception:
        tracked = set()
    if cached == tracked:
        return "unfetched", [], cached
    listed = {"%s.ttl" % s[0] for s in SOURCES}
    if not cached >= listed:
        return "partial", sorted("%s: listed, not cached" % m[:-4]
                                 for m in listed - cached), cached

    scope = listed if keys is None else {"%s.ttl" % k for k in keys}
    bad = []
    for name in sorted(scope & cached):
        g = CACHE / name
        stem = name[:-4]
        raw = g.read_bytes()
        side = CACHE / ("%s.provenance.yaml" % stem)
        if side.exists():
            import yaml as _y
            d = _y.safe_load(side.read_text()) or {}
            have = hashlib.sha256(raw).hexdigest()[:12]
            want = d.get("sha256")
            if want and not str(want).startswith("unrecoverable") \
                    and want != have:
                bad.append("%s: cached bytes %s, sidecar recorded %s — the "
                           "file is not what was measured" % (stem, have, want))
                continue
        n = _triples(raw)
        if n is None:
            bad.append("%s: does not parse as Turtle or RDF/XML" % stem)
        elif n == 0:
            bad.append("%s: parses to ZERO triples" % stem)
    if bad:
        return "degraded", bad, cached
    return "complete", [], cached


def _triples(raw):
    """Triple count, trying both serialisations. None if neither parses.

    Two cached `.ttl` files are RDF/XML — the extension names the cache's
    convention, not the payload's format — so a Turtle-only check reports
    a permanent false failure on `foaf` and `skos`.
    """
    try:
        from rdflib import Graph
    except ImportError:
        return 1          # no parser: do not manufacture a failure
    import logging
    # The Turtle attempt on an RDF/XML payload emits a dozen "does not
    # look like a valid URI" warnings per file before it raises. They are
    # the probe working, not a finding, and left unsilenced they bury the
    # lint output they are printed into.
    lg = logging.getLogger("rdflib")
    prior = lg.level
    lg.setLevel(logging.ERROR)
    try:
        return _parse_any(Graph, raw)
    finally:
        lg.setLevel(prior)


def _parse_any(Graph, raw):
    for fmt in ("turtle", "xml"):
        g = Graph()
        try:
            g.parse(data=raw, format=fmt)
            return len(g)
        except Exception:
            continue
    return None



def check_tables(lines):
    """Every data row must emit exactly the cells its header declares.

    B6: the main table's header declared five columns and all 35 data rows
    emitted six. GFM silently drops the overflow, so `detail` rendered
    under the heading *Disposition* and the bound/borrowed distinction
    vanished from every row. Nothing in the build measured it — O's
    cheapest experiment was to count header cells against row cells, and
    its absence is why it shipped.
    """
    def arity(line):
        return len(line.strip().strip("|").split("|"))

    # B9: this returned `[]` for a table with a header, a separator and
    # ZERO rows — the same value it returns for a correct table. It was
    # commissioned to ask *did this table render what it declared* and it
    # asked *did the rows disagree with the header*, which are the same
    # question on every input except the empty one. And the empty one is
    # reachable: with the `.ttl` cache gone and the sidecars present,
    # `rows` is empty while `failed` and `orphans` are not, so the bail
    # below did not fire and the register was REWRITTEN as a header with
    # no rows, at a clean arity check and a clean drift check — a
    # generator emptied of input still equals itself.
    def close(problems, header, rows_seen):
        if header is not None and rows_seen == 0:
            problems.append(
                "register.md: the table at line %d has a header and NO "
                "rows. A table that rendered nothing is not a table that "
                "agreed with its header." % (header[0] + 1))

    problems, header, sep, rows_seen = [], None, False, 0
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            close(problems, header, rows_seen)
            header, sep, rows_seen = None, False, 0
            continue
        if header is None:
            header = (i, arity(line))
            continue
        if not sep:
            sep = True                       # the |---|---| rule
            if arity(line) != header[1]:
                problems.append("table at line %d: separator declares %d "
                                "cells, header declares %d"
                                % (header[0] + 1, arity(line), header[1]))
            continue
        rows_seen += 1
        if arity(line) != header[1]:
            problems.append(
                "register.md line %d: row emits %d cells, its header at "
                "line %d declares %d — the overflow renders nowhere"
                % (i + 1, arity(line), header[0] + 1, header[1]))
    close(problems, header, rows_seen)       # a table ending the file
    return problems


def check_reason_agrees(d, key):
    """A sidecar against every field of it that can be re-derived offline.

    O falsified the nominated attack line: the distribution's sum cannot
    see a PERMUTATION of reasons, and a permuted sidecar becomes
    internally contradictory — `dereferences: "yes"` and
    `http_status: "200"` alongside `dereference_reason: "access"`, four
    fields with one disagreeing and nothing comparing them. The sum is an
    invariant over the whole; this is an invariant per row, which is what
    a permutation breaks.
    """
    out = []
    reason, deref = d.get("dereference_reason"), d.get("dereferences")
    if reason is not None and reason not in REASON_VERDICT:
        out.append("%s: dereference_reason %r is not one `dereferences()` "
                   "can return" % (key, reason))
    elif reason is not None and deref != REASON_VERDICT[reason]:
        out.append("%s: dereference_reason %r requires dereferences %r, "
                   "found %r — the two disagree and only one can be right"
                   % (key, reason, REASON_VERDICT[reason], deref))
    # Three more fields are DERIVABLE and nothing was deriving them. The
    # sidecars are generated and tracked, and O's census — *there are
    # three generated files* — is three DOCUMENTS; the 36 sidecars carry
    # the same banner. The prescribed experiment, run the generator and
    # diff, cannot be run on them at all: `http_status`, `content_type`,
    # `fetched` and `detail` are live measurements. But `source_url`,
    # `namespace` and `disposition` are functions of `SOURCES` and
    # `DISPOSITION`, so they are checkable offline and now are — 3 fields
    # × 35 listed sidecars that previously had nothing.
    listed = {s[0]: (s[1], s[2]) for s in SOURCES}
    if key in listed:
        ns, url = listed[key]
        for field, want in (("namespace", ns), ("source_url", url),
                            ("disposition",
                             DISPOSITION.get(d.get("dereferences"), "untested"))):
            if d.get(field) != want:
                out.append("%s: %s is %r, derivable value is %r"
                           % (key, field, d.get(field), want))
    return out


def sync_register():
    """Write `register.md` in full. No markers, no host document."""
    import yaml as _y
    _assert_reason_map()          # the map is checked before it is used
    rows, gaps, failed, orphans, incoherent = [], [], [], [], []
    stems = {g.stem for g in CACHE.glob("*.ttl")}
    sides = {s.name.replace(".provenance.yaml", "")
             for s in CACHE.glob("*.provenance.yaml")}
    listed = {s[0] for s in SOURCES}
    # F7: a sidecar with no `.ttl` records a fetch that PRODUCED NO GRAPH.
    # Enumerating `*.ttl` alone made it invisible and `0 gaps` could not
    # see it — C11's absent-versus-zero, in this project's tooling.
    #
    # But a sidecar with no `.ttl` AND no row in SOURCES is a different
    # thing, and reporting the two together said something false: `deo`
    # was listed as a failed fetch for eight days after its source row was
    # deliberately DELETED, so the register showed an ontology this project
    # could not obtain when nothing was trying to obtain one. The remedy
    # differs too — re-probe a failure, delete an orphan.
    for stem in sorted(sides - stems):
        d = _y.safe_load((CACHE / ("%s.provenance.yaml" % stem)).read_text())
        if stem not in listed:
            orphans.append((stem, d.get("source_url", "-"),
                            d.get("http_status", "?"),
                            d.get("dereference_reason") or "unlabelled"))
            continue
        # The reason column belongs here too. Without it the `**unlabelled**`
        # fallback below was UNREACHABLE for the only sidecar that lacks the
        # field: `deo` never fetches, so the repair path never rewrites it,
        # and it renders only in this table — which had no reason column.
        # A fallback no input can reach is a guard clause no fixture covers.
        failed.append((stem, d.get("source_url", "-"), d.get("http_status", "?"),
                       d.get("dereference_reason") or "unlabelled"))
    for g in sorted(CACHE.glob("*.ttl")):
        side = g.with_suffix(".provenance.yaml")
        if not side.exists():
            gaps.append(g.name)
            continue
        d = _y.safe_load(side.read_text())
        incoherent += check_reason_agrees(d, g.stem)
        rows.append((g.stem, d.get("namespace", "-"),
                     d.get("dereferences", "?"), d.get("disposition", "?"),
                     d.get("dereference_reason") or "unlabelled",
                     d.get("detail", "")))

    def _reason(v):
        # ONE sentinel, rendered in one place. Carrying the rendered
        # `**unlabelled**` in the tuple put markup into the tally key, so
        # the generated distribution said `` `**unlabelled**` `` — the
        # mutation that was supposed to prove the fallback reachable
        # found it instead.
        return "**unlabelled**" if v == "unlabelled" else "`%s`" % v

    out = ["# External vocabulary register", "",
           "**Generated in full by `fetch-external.py` from the provenance",
           "sidecars in `graphs/`. Do not edit — edit a sidecar, or the",
           "source list in the generator.**", "",
           "`README.md` carries the conventions and the findings; this file",
           "carries the measurements. One writer each.", "",
           "**EVERY VERDICT IN THIS FILE HAS A SHELF LIFE.** `dereferences`",
           "is a live measurement of somebody else's server, stamped with a",
           "`fetched:` date in each sidecar. These verdicts were true when",
           "fetched and decay independently of this repository — a",
           "namespace that resolved can start serving HTML, and a source",
           "document can be edited under a live binding. Both happened to",
           "`adms` on 2026-08-07, between two fetches in one session.",
           "Stated once, here, rather than per row: a per-row staleness note",
           "is a hand-written claim beside a generated one, which is the",
           "defect this file has paid for three times.", "",
           "**`dereferences` is a separate live fetch of the namespace, not of",
           "the cached file.** GeoSPARQL is why: `:Geometry` is defined in the",
           "cached graph and undefined in what the namespace serves. A",
           "vocabulary can be *bound* by name and *borrowed* in fact.", "",
           "**`dereferences` carries its reason in a FIELD**,",
           "`dereference_reason`, not only in free text. F14: the header",
           "used to assert this while the cause lived in prose `detail`,",
           "labelled on 4 of 19 `no` rows — access at 12 rows read as a",
           "bare `HTTP 301` and content at 1, the one argued hardest for,",
           "was the least visible. A generated file of record asserting a",
           "capability it did not have is C23's shape, written by a tool.",
           "A row showing **unlabelled** predates the field and has not",
           "been re-probed. **Every table carries the column**, because the",
           "one sidecar that lacks the field renders in none of the tables",
           "that had one — it is an orphan, and both the orphan and the",
           "failed-fetch tables were reason-free, so the fallback was",
           "unreachable for the only row that needed it.", "",
           # B8: F15 recurred in its own repair. The heading said *three*
           # over four rows, was corrected to *four*, and the correction
           # shipped over FIVE — off by one in the same direction twice.
           # A count in a heading beside the table it counts is a
           # hand-maintained duplicate of something already on the page,
           # so it is generated now and cannot disagree.
           "**%d causes of non-dereference, and they decay differently.**"
           % len(DECAY),
           "F15/B8: this heading said *three* over four rows, then *four*",
           "over five. Both times the table beneath it was right. The",
           "number is counted from that table now, so it cannot disagree",
           "with it.", "",
           "| Reason | Decays how |",
           "|---|---|"] + [
           "| `%s` | %s |" % d for d in DECAY] + [
           "",
           # B6: this header declared FIVE columns while every data row
           # emitted six. GFM drops cells past the header, so `detail`
           # rendered under the heading *Disposition* and the
           # bound/borrowed/untested distinction — the one
           # `vocab-conventions.md` says decides what a binding is worth —
           # was invisible on all 35 rows of a file of record. Introduced
           # by the F14 repair, which put `Why` in the row format and not
           # here. `check_tables()` below now measures arity.
           "| Graph | Namespace | Dereferences | Why | Detail | Disposition |",
           "|---|---|---|---|---|---|"]
    for k, ns, dr, disp, reason, detail in rows:
        out.append("| `%s` | <%s> | **%s** | %s | %s | **%s** |"
                   % (k, ns, dr, _reason(reason), detail or "—", disp))
    tally = {}
    for _k, _n, _d, disp, _r, _x in rows:
        tally[disp] = tally.get(disp, 0) + 1
    # The reason distribution is GENERATED, and its total is asserted
    # against the row count. Counting it by hand off the rendered file
    # over-reported every reason that also names a row of the legend
    # table above — access 13 for 12, content 3 for 2 — because the
    # instrument could not tell a legend from a datum. The total was the
    # tell: 40 cells over 35 rows. Stated here so nobody counts again.
    rtally = {}
    for _k, _n, _d, _p, reason, _x in rows:
        rtally[reason] = rtally.get(reason, 0) + 1
    assert sum(rtally.values()) == len(rows), (
        "reason distribution %d != %d rows" % (sum(rtally.values()), len(rows)))
    out += ["", "*%d graphs with a sidecar; %s. %d fetch(es) produced no "
            "graph at all.*"
            % (len(rows), ", ".join("%d %s" % (v, k)
                                    for k, v in sorted(tally.items())),
               len(failed)),
            "",
            "**Reason distribution over the %d rows above** — generated, and "
            "its total is asserted equal to the row count. Counting these off "
            "the rendered table by hand adds one to every reason that also "
            "names a row of the legend: %s."
            % (len(rows), ", ".join("%s %d" % (_reason(k), v) for k, v in
                                    sorted(rtally.items(), key=lambda x: -x[1])))]
    if gaps:
        out += ["", "**Cached with no sidecar — not covered by the table "
                "above:**", ""] + ["- `%s`" % g for g in gaps]
    out += ["", "## A term's declaration may span rows — two different reasons",
            "",
            "The row-per-file shape breaks for the eleven KWG source",
            "ontologies, and **it breaks in two ways that need different",
            "remedies.**", "",
            "**Measured across the eleven dataset ontologies, and the",
            "definition matters** (F17): **444 URIs are the subject of some",
            "`rdf:type`**, of which **195 are declared as a class, property",
            "or datatype** — the rest are instances. *Declared* implies a",
            "term declaration, so the stricter count is the one that word",
            "fits; 444 is reported beside it because it is the number first",
            "published and the row-spanning measurement was taken over it.",
            "**Of the 444, 46 appear in more than one file.**", "",
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
            "term's declaration is arbitrary among eleven files, when it is",
            "not arbitrary at all."]
    if failed:
        out += ["", "## Fetched, produced no graph", "",
                "A sidecar exists and there is no `.ttl` beside it. Listed "
                "because **an attempt that failed is not an attempt not "
                "made**, and a row count over successes cannot tell them "
                "apart.", "",
                "| Attempted | Source | HTTP | Why |", "|---|---|---|---|"]
        out += ["| `%s` | <%s> | %s | %s |"
                % (f[0], f[1], f[2], _reason(f[3])) for f in failed]
    if orphans:
        out += ["", "## Sidecar with no source row — orphaned", "",
                "A sidecar with no `.ttl` **and no row in `SOURCES`**. This "
                "is not a fetch this project could not make; it is the "
                "residue of a source row that was removed. Reported "
                "separately because the remedy differs — **re-probe a "
                "failure, delete an orphan** — and because listing the two "
                "together made the register show an ontology as "
                "unobtainable when nothing was trying to obtain it.", "",
                "| Orphan | Source it recorded | HTTP | Why |",
                "|---|---|---|---|"]
        out += ["| `%s` | <%s> | %s | %s |"
                % (o[0], o[1], o[2], _reason(o[3])) for o in orphans]
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
    if not rows and not failed and not orphans:
        print("FAIL  no provenance sidecars under %s — register.md NOT "
              "written. A register generated from nothing is an empty "
              "table that reports no problems." % CACHE, file=sys.stderr)
        return 1
    # B9: the bail above was the ONLY thing standing between an emptied
    # cache and a rewritten register, and it could not fire in the state
    # that matters — sidecars present, graphs gone, so `failed` and
    # `orphans` are non-empty while `rows` is empty. Its own comment
    # describes exactly the file it then let through. The register's rows
    # come from the graphs; a register with no rows is not a register.
    state, why, cached = cache_state()
    if state == "degraded":
        # B5's class, generalised. `fetch-external.py` already refused to
        # write from an EMPTIED cache — *an emptied generator still equals
        # itself* — and a degraded one is the same sentence: the register
        # would describe bytes nobody can read as though they were the
        # measurement.
        print("FAIL  the cache is DEGRADED — register.md NOT %s:"
              % ("checked" if CHECK_ONLY[0] else "written"), file=sys.stderr)
        for w in why:
            print("        %s" % w, file=sys.stderr)
        return 1
    if state == "partial":
        print("FAIL  the cache is PARTIAL — register.md NOT %s:"
              % ("checked" if CHECK_ONLY[0] else "written"), file=sys.stderr)
        for w in why:
            print("        %s" % w, file=sys.stderr)
        return 1
    if state == "unfetched":
        # F19. The cache is INPUT and nobody has fetched it, which is the
        # `.gitkeep` case one directory over: note what was inspected and
        # pass. Refusing to WRITE is the other half — a register built
        # from an unfetched cache would replace 35 measured rows with the
        # handful a checkout ships, which is B5's family.
        print("register.md: not %s — the cache is unfetched (%d cached, "
              "all of them tracked). This check inspected nothing. Run "
              "`fetch-external.py` to populate it."
              % ("checked" if CHECK_ONLY[0] else "written", len(cached)))
        return 0
    if not rows and (failed or orphans):
        print("FAIL  %d sidecar(s) under %s and NO cached graph — "
              "register.md NOT written. Every row of the register comes "
              "from a `.ttl`; this would emit a header with no rows, and "
              "an emptied generator still equals itself."
              % (len(failed) + len(orphans), CACHE), file=sys.stderr)
        return 1
    # PEER CHECK — on `resolved_url`, NOT on bytes.
    #
    # B8: comparing digests could not fail while the redirect stood.
    # `fetch()` runs `curl -sS -L`, so both rows fetch the SAME endpoint
    # and their byte identity is ENTAILED by the 307 — the guard asserted
    # a consequence of the thing it was meant to watch. The decisive state
    # is the redirect being withdrawn with the bodies still identical: the
    # digest check stays silent, and at that instant the licensed sentence
    # has degraded from *two URLs resolve to one body* to *two bodies that
    # agree today* — the phrasing retracted at pass 1, reappearing inside
    # the guard offered as the retraction's support.
    #
    # `resolved_url` was already in every sidecar and read by nothing:
    # F10 closed as a field and not as an assertion, the fourth recurrence
    # of that distinction. It is the datum that settles it.
    import yaml as _yp
    for (x, y), why in DIGEST_PEER.items():
        sx, sy = (CACHE / ("%s.provenance.yaml" % k) for k in (x, y))
        if not (sx.exists() and sy.exists()):
            continue
        dx, dy = (_yp.safe_load(s.read_text()) or {} for s in (sx, sy))
        ex, ey = dx.get("resolved_url"), dy.get("resolved_url")
        if ex is None or ey is None:
            incoherent.append(
                "%s/%s: no `resolved_url` — the peer claim cannot be "
                "checked, and an unfalsifiable guard is not a guard"
                % (x, y))
        elif ex == ey:
            # Endpoints agree, so the bodies came from ONE URL and can
            # differ only if the two fetches straddled a change there.
            # Kept as a SECONDARY check: B8's finding was that bytes alone
            # cannot fail while the redirect stands, not that bytes are
            # uninformative. Asserting both is strictly stronger than
            # either, and this half is C26's shelf-life event caught in
            # the act.
            px, py = CACHE / ("%s.ttl" % x), CACHE / ("%s.ttl" % y)
            if px.exists() and py.exists() \
                    and px.read_bytes() != py.read_bytes():
                incoherent.append(
                    "%s and %s resolve to one endpoint (%s) and their "
                    "cached bodies DIFFER — the two fetches straddled a "
                    "change at that URL, so neither describes it now"
                    % (x, y, ex))
        else:
            px, py = CACHE / ("%s.ttl" % x), CACHE / ("%s.ttl" % y)
            same = (px.exists() and py.exists()
                    and px.read_bytes() == py.read_bytes())
            incoherent.append(
                "%s and %s no longer resolve to one endpoint — %s vs %s. "
                "The bodies %s. The licensed statement has degraded from "
                "*two URLs resolve to one body* to *two %s*. %s"
                % (x, y, ex, ey,
                   "still agree" if same else "differ too",
                   "bodies that agree today" if same else "diverged documents",
                   why))
    bad = check_tables(out) + incoherent
    text = "\n".join(out) + "\n"
    if CHECK_ONLY[0]:
        # B5: regenerating the register from check-mode rows is how the
        # destruction reached a file of record. Check mode reads.
        #
        # B7: and it read NOTHING. `--check` printed `Problems — (none)`
        # while the committed register was five lines behind its own
        # generator, asserting the `**unlabelled**` fallback unreachable,
        # reporting `0 fetch(es) produced no graph`, and rendering an
        # orphan table — three statements that cannot all hold. For a
        # wholly generated file, "up to date" means BYTE-IDENTICAL to what
        # the generator emits, and that is checkable without writing.
        if not REGISTER.exists():
            bad.append("register.md: absent, and it is generated")
        elif REGISTER.read_text() != text:
            have = REGISTER.read_text().splitlines()
            want = text.splitlines()
            diff = [i for i in range(max(len(have), len(want)))
                    if have[i:i + 1] != want[i:i + 1]]
            bad.append(
                "register.md: DRIFTED from its generator — %d line(s) "
                "differ, first at %d. The committed file is not what "
                "`sync_register()` emits, so it is stale by exactly the "
                "last generator edit that was not followed by a write."
                % (len(diff), diff[0] + 1 if diff else 0))
        print("register.md: not rewritten (--check reads only)")
        for b in bad:
            print("  %s" % b)
        return 1 if bad else 0
    if bad:
        # A malformed table is not written. The whole point of B6 is that
        # the rendered file looked fine while dropping a column.
        for b in bad:
            print("FAIL  %s" % b, file=sys.stderr)
        return 1
    REGISTER.write_text(text)
    print("register.md: %d rows, %d gaps, %d failed fetch(es), %d orphan(s)"
          % (len(rows), len(gaps), len(failed), len(orphans)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the cache on disk; no network")
    args = ap.parse_args()
    CHECK_ONLY[0] = args.check
    CACHE.mkdir(parents=True, exist_ok=True)
    CACHE_STATE[0] = cache_state()[0]
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                           capture_output=True, text=True).stdout.strip()

    rows, problems = [], []
    CACHED_OK = set()
    for key, ns, url, terms in SOURCES:
        path = CACHE / ("%s.ttl" % key)
        if args.check:
            if not path.exists():
                # F19: on a fresh clone this fired 31 times and none of the
                # 31 described anything wrong — the cache is gitignored, so
                # `not cached` is the EXPECTED state of a tree nobody has
                # run the fetch in. A problem list whose entries are all
                # expected trains a reader to stop reading it.
                if CACHE_STATE[0] != "unfetched":
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
            rows.append((key, ns, status, 0, "-", "-", "no payload",
                         "**no** — no payload", "no-probe", "—", final))
            continue

        found = terms_found(body, terms)
        missing = sorted(t for t, ok in found.items() if not ok)
        if missing:
            problems.append("%s: %d/%d terms MISSING from the payload: %s"
                            % (key, len(missing), len(terms),
                               ", ".join(missing)))
        # B7: TWO measurements, reported separately, because one column
        # said `6/6 terms present` for a route whose terms are subjects
        # and for one whose terms are only labels. `nvs-p07` is the
        # control and it now reads `0/6 declared` beside its `6/6 occur`.
        declared = terms_declared(body, ns, terms) if terms else None
        if declared is None:
            strong = "unparseable" if terms else "—"
        else:
            nd = sum(1 for v in declared.values() if v)
            strong = "**%d/%d declared**" % (nd, len(terms))
            # Recorded on the NETWORK path only, exactly as the
            # dereference verdicts are. Several of these are documented
            # facts — `ssn-ext` mints into SOSA's namespace by design —
            # so failing `make lint` on them would be a guard that cannot
            # be satisfied, and those get deleted. The COLUMN is written
            # in both modes; the problem entry is a finding about an
            # external vocabulary, not about this tree.
            if nd < len(terms) and not args.check:
                problems.append(
                    "%s: %d/%d bound terms are NOT typed subjects under `%s` "
                    "— present by substring only, which is a presence census "
                    "and not a binding"
                    % (key, len(terms) - nd, len(terms), ns))
        verdict = ("**not content-verified** — no term list" if not terms
                   else "%d/%d occur" % (len(terms) - len(missing),
                                         len(terms)))
        # The namespace is a different question from the fetch URL, and
        # GeoSPARQL is the case that proves it: the namespace returns a
        # description document mentioning every bound term and defining
        # none. So this asks whether resolving the NAMESPACE yields a
        # graph in which a probe term is defined — not whether it 200s.
        deref, reason, detail = (("skipped", "not-probed", "--check, no network")
                                 if args.check else dereferences(ns, key))
        if key in SIDECAR_NOTE and not args.check:
            detail = "%s. %s" % (detail, SIDECAR_NOTE[key])
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
                     "**%s** — %s" % (deref, detail), reason, strong,
                     final))

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
            "dereference_reason: %s\n"
            "resolved_url:  %s\n"
            "disposition:   %s\n"
            % (json.dumps(src_of(key)), json.dumps(stamp),
               json.dumps(r[2]), json.dumps(r[5]), json.dumps(r[4]),
               json.dumps(ns), json.dumps(deref),
               json.dumps(r[7].split("—", 1)[-1].strip()),
               json.dumps(r[8]),
               # The URL curl ENDED at. `fetch()` follows redirects and
               # this was thrown away, so a source that redirects looked
               # identical to one that does not — and `adms` turned out to
               # be a **307 Temporary Redirect** to SEMIC, discovered by
               # hand because nothing recorded it. A hand probe leaves no
               # sidecar; this does.
               # ALWAYS the real endpoint. This wrote the sentinel
               # `"same as source_url"` when the two agreed, which reads
               # well and cannot be compared — so the first check to need
               # the field had to decode it first. A field written for a
               # reader rather than for a check is F10's problem in the
               # repair for F10's problem.
               json.dumps(r[10] if len(r) > 10 and r[10] else src_of(key)),
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
           "| Vocabulary | Fetch URL (cached) | HTTP | Bytes | SHA-256 | Type | Terms occur (substring) | Terms declared (typed subject) | Namespace | Namespace serves |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    src = {k: u for k, _n, u, _t in SOURCES}
    for r in rows:
        out.append("| `%s` | <%s> | %s | %s | `%s` | %s | %s | %s | <%s> | %s |"
                   % (r[0], src.get(r[0], "-"), r[2], r[3], r[4], r[5],
                      r[6], r[9] if len(r) > 9 else "—", r[1], r[7]))
    # The register's own problems belong IN this section. They used to be
    # printed after it, so `--check` rendered `## Problems — *(none)*` and
    # then reported that the register had drifted from its generator, two
    # lines apart. A problems section that does not include the problems
    # is B7's shape in the reporting rather than in the file.
    reg_rc = sync_register()
    if reg_rc:
        problems.append("register.md: see the lines above — it is generated, "
                        "and it is not what its generator emits")
    # B10: the manifest is generated and was never compared to anything.
    # Narrowed to what an offline run can know — see manifest_comparable().
    if args.check and CACHE_STATE[0] != "unfetched":
        if not MANIFEST.exists():
            problems.append("manifest.md: absent, and it is generated")
        else:
            want = manifest_comparable("\n".join(out) + "\n")
            have = manifest_comparable(MANIFEST.read_text())
            if want != have:
                w, h = want.splitlines(), have.splitlines()
                d = [i for i in range(max(len(w), len(h)))
                     if w[i:i + 1] != h[i:i + 1]]
                problems.append(
                    "manifest.md: DRIFTED from its generator — %d line(s) "
                    "differ, first at %d (comparing header prose and the "
                    "network-independent row cells; HTTP, Type and "
                    "Namespace-serves are live measurements this mode does "
                    "not make)" % (len(d), d[0] + 1 if d else 0))
    out += ["", "## Problems", ""]
    out += (["*(none)*"] if not problems else
            ["- %s" % p for p in problems])
    out.append("")
    if not CHECK_ONLY[0]:
        MANIFEST.write_text("\n".join(out))
    else:
        print("manifest.md: not rewritten (--check reads only)")

    print("\n".join(out[7:]))
    if problems:
        print("\n%d problem(s) — these are findings, not script bugs"
              % len(problems), file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
