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

**`dereferences` carries its REASON, not a bare verdict.** Three
unrelated causes were all printing `no` and they decay
differently: **structural** (no TLD) can never change,
**access** (403/404) could change from another network,
**single observation** (000) is one probe rather than a
property, and **content** (200 but the term is undefined) is
the GeoSPARQL case. One value covering four causes is C11's
shape.

| Graph | Namespace | Dereferences | Why | Disposition |
|---|---|---|---|---|
| `admin-regions-gadm` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `adms` | <http://www.w3.org/ns/adms#> | **yes** | 200 text/turtle, `Identifier` defined | **bound** |
| `air-quality-epa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `census-uscb` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `climate-divisions-observations-noaa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `cropland-types-usda` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `dcterms` | <http://purl.org/dc/terms/> | **yes** | 200 text/turtle, `conformsTo` defined | **bound** |
| `disaster-event-module-extensions` | <http://knowwheregraph/ontology/deo#> | **no** | **structural** — host `knowwheregraph` has no TLD, cannot resolve for anyone, ever | **borrowed** |
| `disaster-event-module-generalized` | <http://knowwheregraph/ontology/deo#> | **no** | **structural** — host `knowwheregraph` has no TLD, cannot resolve for anyone, ever | **borrowed** |
| `disaster-properties-ontology` | <http://knowwheregraph/ontology/dpo#> | **no** | **structural** — host `knowwheregraph` has no TLD, cannot resolve for anyone, ever | **borrowed** |
| `dqv` | <http://www.w3.org/ns/dqv#> | **yes** | 200 text/turtle, `QualityMeasurement` defined | **bound** |
| `earthquake-usgs` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `federal-judicial-district-doj` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `foaf` | <http://xmlns.com/foaf/0.1/> | **yes** | 200 application/rdf+xml, `Document` defined | **bound** |
| `geosparql` | <http://www.opengis.net/ont/geosparql#> | **no** | 200 text/anot+turtle, 306 triples, `http://www.opengis.net/ont/geosparql#Geometry` NOT defined | **borrowed** |
| `historical-fires-mtbs` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `hurricane-tracks-noaa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `national-weather-zone-noaa` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `nvs-p07` | <http://vocab.nerc.ac.uk/collection/P07/current/> | **untested** | no probe term declared | **untested** |
| `org` | <http://www.w3.org/ns/org#> | **yes** | 200 text/turtle, `Organization` defined | **bound** |
| `owl-time` | <http://www.w3.org/2006/time#> | **yes** | 200 text/turtle, `Interval` defined | **bound** |
| `prov-o` | <http://www.w3.org/ns/prov#> | **yes** | 200 text/turtle, `Entity` defined | **bound** |
| `qudt-schema` | <http://qudt.org/schema/qudt/> | **yes** | 200 text/turtle, `QuantityValue` defined | **bound** |
| `qudt-units` | <http://qudt.org/vocab/unit/> | **yes** | 200 text/turtle, `M-PER-SEC` defined | **bound** |
| `schema` | <https://schema.org/> | **no** | 200 text/html, unparseable | **borrowed** |
| `shacl` | <http://www.w3.org/ns/shacl#> | **yes** | 200 text/turtle, `NodeShape` defined | **bound** |
| `sioc` | <http://rdfs.org/sioc/ns#> | **yes** | 200 application/rdf+xml, `Community` defined | **bound** |
| `skos` | <http://www.w3.org/2004/02/skos/core#> | **yes** | 200 application/rdf+xml, `Concept` defined | **bound** |
| `sosa` | <http://www.w3.org/ns/sosa/> | **yes** | 200 text/turtle, `Observation` defined | **bound** |
| `ssn-ext` | <http://www.w3.org/ns/ssn/ext/> | **document** | 200 text/turtle, 145 triples, mints **no term of its own** — `ObservationCollection` is defined here but minted elsewhere | **borrowed** |
| `ssn-system` | <http://www.w3.org/ns/ssn/systems/> | **yes** | 200 text/turtle, `SystemCapability` defined | **bound** |
| `ssn` | <http://www.w3.org/ns/ssn/> | **yes** | 200 text/turtle, `System` defined | **bound** |
| `undrr-isc-hazard-classification` | <https://undrr-hip.org/> | **no** | **single observation** — no response; one probe, not a property | **borrowed** |
| `void` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |
| `wildfire-nifc` | <http://stko-kwg.geog.ucsb.edu/lod/ontology/> | **no** | **HTTP 301** | **borrowed** |

*35 graphs with a sidecar; 19 borrowed, 15 bound, 1 untested. 1 fetch(es) produced no graph at all.*

## Fetched, produced no graph

A sidecar exists and there is no `.ttl` beside it. Listed because **an attempt that failed is not an attempt not made**, and a row count over successes cannot tell them apart.

| Attempted | Source | HTTP |
|---|---|---|
| `deo` | <http://schema.knowwheregraph.org/lod/ontology/> | 000 |
