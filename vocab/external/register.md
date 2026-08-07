# External vocabulary register

**Generated in full by `fetch-external.py` from the provenance
sidecars in `graphs/`. Do not edit — edit a sidecar, or the
source list in the generator.**

`README.md` carries the conventions and the findings; this file
carries the measurements. One writer each.

**`dereferences` is a separate live fetch of the namespace, not of
the cached file.** GeoSPARQL is why: `:Geometry` is defined in the
cached graph and undefined in what the namespace serves. A
vocabulary can be *bound* by name and *borrowed* in fact.

**`dereferences` carries its reason in a FIELD**,
`dereference_reason`, not only in free text. F14: the header
used to assert this while the cause lived in prose `detail`,
labelled on 4 of 19 `no` rows — access at 12 rows read as a
bare `HTTP 301` and content at 1, the one argued hardest for,
was the least visible. A generated file of record asserting a
capability it did not have is C23's shape, written by a tool.
A row showing **unlabelled** predates the field and has not
been re-probed. **Every table carries the column**, because the
one sidecar that lacks the field renders in none of the tables
that had one — it is an orphan, and both the orphan and the
failed-fetch tables were reason-free, so the fallback was
unreachable for the only row that needed it.

**5 causes of non-dereference, and they decay differently.**
F15/B8: this heading said *three* over four rows, then *four*
over five. Both times the table beneath it was right. The
number is counted from that table now, so it cannot disagree
with it.

| Reason | Decays how |
|---|---|
| `structural` | never — a host with no TLD cannot resolve for anyone |
| `access` | 403/404/301/expired cert — could change from another network |
| `single-observation` | `000`, no response — one probe, not a property |
| `content` | 200, but the probe term is not defined in what is served |
| `mints-nothing` | 200 and a graph, but no term under its own namespace |

| Graph | Namespace | Dereferences | Why | Detail | Disposition |
|---|---|---|---|---|---|
| `admin-regions-gadm` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `adms` | <http://www.w3.org/ns/adms#> | **no** | `content` | 200 text/html, unparseable | **borrowed** |
| `air-quality-epa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `census-uscb` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `cf-standard-name` | <http://vocab.nerc.ac.uk/standard_name/> | **yes** | `resolves` | 200 text/turtle, `air_temperature` defined. Every subject ends in a trailing `/`; the CURIE carries it (`cfsn:air_temperature/`); it does NOT reach the emitted Turtle — `gen-shacl` writes the full URI in angle brackets and the result reparses. Scheme is `http`, not `https` | **bound** |
| `climate-divisions-observations-noaa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `cropland-types-usda` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `dcterms` | <http://purl.org/dc/terms/> | **yes** | `resolves` | 200 text/turtle, `conformsTo` defined | **bound** |
| `disaster-event-module-extensions` | <http://knowwheregraph/ontology/deo#> | **no** | `structural` | host `knowwheregraph` has no TLD — cannot resolve for anyone, ever | **borrowed** |
| `disaster-event-module-generalized` | <http://knowwheregraph/ontology/deo#> | **no** | `structural` | host `knowwheregraph` has no TLD — cannot resolve for anyone, ever | **borrowed** |
| `disaster-properties-ontology` | <http://knowwheregraph/ontology/dpo#> | **no** | `structural` | host `knowwheregraph` has no TLD — cannot resolve for anyone, ever | **borrowed** |
| `dqv` | <http://www.w3.org/ns/dqv#> | **yes** | `resolves` | 200 text/turtle, `QualityMeasurement` defined | **bound** |
| `earthquake-usgs` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `federal-judicial-district-doj` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `foaf` | <http://xmlns.com/foaf/0.1/> | **yes** | `resolves` | 200 application/rdf+xml, `Document` defined | **bound** |
| `geosparql` | <http://www.opengis.net/ont/geosparql#> | **no** | `content` | 200 text/anot+turtle, 305 triples, but `http://www.opengis.net/ont/geosparql#Geometry` is NOT defined in what the namespace serves | **borrowed** |
| `historical-fires-mtbs` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `hurricane-tracks-noaa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `national-weather-zone-noaa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `nvs-p07` | <http://vocab.nerc.ac.uk/collection/P07/current/> | **untested** | `no-probe` | no probe term declared | **untested** |
| `org` | <http://www.w3.org/ns/org#> | **yes** | `resolves` | 200 text/turtle, `Organization` defined | **bound** |
| `owl-time` | <http://www.w3.org/2006/time#> | **yes** | `resolves` | 200 text/turtle, `Interval` defined | **bound** |
| `prov-o` | <http://www.w3.org/ns/prov#> | **yes** | `resolves` | 200 text/turtle, `Entity` defined | **bound** |
| `qudt-schema` | <http://qudt.org/schema/qudt/> | **yes** | `resolves` | 200 text/turtle, `QuantityValue` defined | **bound** |
| `qudt-units` | <http://qudt.org/vocab/unit/> | **yes** | `resolves` | 200 text/turtle, `M-PER-SEC` defined | **bound** |
| `schema` | <https://schema.org/> | **no** | `content` | 200 text/html, unparseable | **borrowed** |
| `shacl` | <http://www.w3.org/ns/shacl#> | **yes** | `resolves` | 200 text/turtle, `NodeShape` defined | **bound** |
| `sioc` | <http://rdfs.org/sioc/ns#> | **yes** | `resolves` | 200 application/rdf+xml, `Community` defined | **bound** |
| `skos` | <http://www.w3.org/2004/02/skos/core#> | **yes** | `resolves` | 200 application/rdf+xml, `Concept` defined | **bound** |
| `sosa` | <http://www.w3.org/ns/sosa/> | **yes** | `resolves` | 200 text/turtle, `Observation` defined | **bound** |
| `ssn-ext` | <http://www.w3.org/ns/ssn/ext/> | **document** | `mints-nothing` | 200 text/turtle, 145 triples, mints **no term of its own** — `ObservationCollection` is defined here but minted elsewhere | **borrowed** |
| `ssn-system` | <http://www.w3.org/ns/ssn/systems/> | **yes** | `resolves` | 200 text/turtle, `SystemCapability` defined | **bound** |
| `ssn` | <http://www.w3.org/ns/ssn/> | **yes** | `resolves` | 200 text/turtle, `System` defined | **bound** |
| `undrr-isc-hazard-classification` | <https://undrr-hip.org/> | **no** | `single-observation` | no response — one probe, not a property | **borrowed** |
| `void` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |
| `wildfire-nifc` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | `access` | 301, and the redirect target did not serve a graph | **borrowed** |

*36 graphs with a sidecar; 20 borrowed, 15 bound, 1 untested. 0 fetch(es) produced no graph at all.*

**Reason distribution over the 36 rows above** — generated, and its total is asserted equal to the row count. Counting these off the rendered table by hand adds one to every reason that also names a row of the legend: `resolves` 15, `access` 12, `content` 3, `structural` 3, `no-probe` 1, `mints-nothing` 1, `single-observation` 1.

## A term's declaration may span rows — two different reasons

The row-per-file shape breaks for the eleven KWG source
ontologies, and **it breaks in two ways that need different
remedies.**

**Measured across the eleven dataset ontologies, and the
definition matters** (F17): **444 URIs are the subject of some
`rdf:type`**, of which **195 are declared as a class, property
or datatype** — the rest are instances. *Declared* implies a
term declaration, so the stricter count is the one that word
fits; 444 is reported beside it because it is the number first
published and the row-spanning measurement was taken over it.
**Of the 444, 46 appear in more than one file.**

**Ten are in KWG's own namespace, and their declaring file is
arbitrary.** `AdministrativeRegion_2` and `S2Cell_Level13` are
each declared in **10 of 11**; `Region`, `spatialRelation` and
`hasTemporalScope` in 6; `sfWithin` in 3; `hasFIPS`,
`stateName`, `countyName` and **`irwinID`** in 2. For these,
which row holds the declaration carries no meaning — read any
of them.

**`irwinID` is worth naming separately.** It is the only term
in this corpus touching ADR-001's identity apparatus, and a
scheme identifier whose declaring file is arbitrary is a
different kind of problem from a region class.

**Thirty-six are foreign, and are not a row-spanning problem at
all — the declaration is in the wrong file entirely.** They are
stub redeclarations of terms KWG does not own: **sosa 11,
geosparql 7, skos 6, dcterms 5, owl-time 5, schema.org 2**. For
these the register points at the OWNING namespace's row, which
this cache already holds. Anyone opening a KWG ontology for
`sosa:Observation`'s definition gets a bare `owl:Class` with no
axioms, while the real SOSA graph sits in this same directory.

`vocab-conventions.md`'s fifth failure mode — *a vocabulary may
declare a term it does not own* — **at scale, and measured.**
Conflating the two halves would make this register say a SOSA
term's declaration is arbitrary among eleven files, when it is
not arbitrary at all.

## Sidecar with no source row — orphaned

A sidecar with no `.ttl` **and no row in `SOURCES`**. This is not a fetch this project could not make; it is the residue of a source row that was removed. Reported separately because the remedy differs — **re-probe a failure, delete an orphan** — and because listing the two together made the register show an ontology as unobtainable when nothing was trying to obtain it.

| Orphan | Source it recorded | HTTP | Why |
|---|---|---|---|
| `deo` | <http://schema.knowwheregraph.org/lod/ontology/> | 000 | **unlabelled** |
