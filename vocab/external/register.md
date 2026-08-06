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

| Graph | Namespace | Dereferences | Disposition |
|---|---|---|---|
| `adms` | <http://www.w3.org/ns/adms#> | **yes** | **bound** |
| `dcterms` | <http://purl.org/dc/terms/> | **yes** | **bound** |
| `disaster-event-module-extensions` | <http://knowwheregraph/ontology/deo#> | **no** | **borrowed** |
| `disaster-event-module-generalized` | <http://knowwheregraph/ontology/deo#> | **no** | **borrowed** |
| `disaster-properties-ontology` | <http://knowwheregraph/ontology/dpo#> | **no** | **borrowed** |
| `dqv` | <http://www.w3.org/ns/dqv#> | **yes** | **bound** |
| `foaf` | <http://xmlns.com/foaf/0.1/> | **yes** | **bound** |
| `geosparql` | <http://www.opengis.net/ont/geosparql#> | **no** | **borrowed** |
| `nvs-p07` | <http://vocab.nerc.ac.uk/collection/P07/current/> | **untested** | **untested** |
| `org` | <http://www.w3.org/ns/org#> | **yes** | **bound** |
| `owl-time` | <http://www.w3.org/2006/time#> | **yes** | **bound** |
| `prov-o` | <http://www.w3.org/ns/prov#> | **yes** | **bound** |
| `qudt-schema` | <http://qudt.org/schema/qudt/> | **yes** | **bound** |
| `qudt-units` | <http://qudt.org/vocab/unit/> | **yes** | **bound** |
| `schema` | <https://schema.org/> | **no** | **borrowed** |
| `shacl` | <http://www.w3.org/ns/shacl#> | **yes** | **bound** |
| `sioc` | <http://rdfs.org/sioc/ns#> | **yes** | **bound** |
| `skos` | <http://www.w3.org/2004/02/skos/core#> | **yes** | **bound** |
| `sosa` | <http://www.w3.org/ns/sosa/> | **yes** | **bound** |
| `ssn-ext` | <http://www.w3.org/ns/ssn/ext/> | **document** | **borrowed** |
| `ssn-system` | <http://www.w3.org/ns/ssn/systems/> | **yes** | **bound** |
| `ssn` | <http://www.w3.org/ns/ssn/> | **yes** | **bound** |
| `undrr-isc-hazard-classification` | <https://undrr-hip.org/> | **no** | **borrowed** |

*23 graphs with a sidecar; 7 borrowed, 15 bound, 1 untested. 1 fetch(es) produced no graph at all.*

## Fetched, produced no graph

A sidecar exists and there is no `.ttl` beside it. Listed because **an attempt that failed is not an attempt not made**, and a row count over successes cannot tell them apart.

| Attempted | Source | HTTP |
|---|---|---|
| `deo` | <http://schema.knowwheregraph.org/lod/ontology/> | 000 |
