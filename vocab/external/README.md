# Cached external vocabularies

Local copies of the vocabularies this project reads, in
`vocab/external/graphs/`, so definitions can be quoted, terms
enumerated, and work done offline.

**This directory is borrowed material and is not subject to the
vocabulary lints.** C1, C4, C7, C19, C20 and C21 govern what this
project declares, not what other projects declared. `make lint` scans
`vocab/core/` and `vocab/profiles/` only — a `.ttl` here would be
outside the rules' file filters anyway, but a `.yaml` provenance sidecar
would not have been, so the C4 target was scoped explicitly rather than
left to a filename extension.

**A cached copy does not discharge a binding.** Every finding of value
in this project came from fetching a live namespace and grepping it —
`sosa:hasMember` carrying no interval, `qudt:unit` not existing, SOSA's
`Sensor` covering simulation software, DMDO's namespace having no TLD.
The cache answers *what did this say when it was fetched*. Only a live
fetch answers *what does it say*, and a binding is verified against the
live namespace at least once, with the result recorded here.

**Cite a source by URL, not by path.** Every claim in the findings
below was made against a specific fetched artifact, and a reader who
cannot reach the artifact cannot check the claim. A bare
`taxonomy-building/README.md` names a file in a repository the reader
may never have seen.

## What each cached file needs beside it

A `<name>.provenance.yaml` carrying, at minimum:

```yaml
source_url:        # exactly what was fetched
fetched:           # ISO 8601, UTC
http_status:
content_type:      # what was served, not what was expected
sha256:
namespace:         # the URI a consumer would resolve
dereferences:      # yes | no | untested — and what was served if not the graph
disposition:       # bound | borrowed | cited
```

`dereferences` and `disposition` are the two that matter. A file
downloaded from a repository tells you what is in the repository; it
tells you nothing about what a consumer resolving the namespace
receives. Two vocabularies here have already differed on exactly that
point — one returned a 288-byte profile stub, another 404'd under every
accept type while its specification document existed and was correct.

## Register

Twenty graphs are cached. The table below is the register; fill it as
each is verified.

| Vocabulary | Namespace | Dereferences | Disposition |
|---|---|---|---|
| `adms` `dcterms` `dqv` `foaf` `org` `owl-time` `prov-o` `shacl` `skos` `sosa` `ssn` `ssn-ext` `ssn-system` | | | |
| `geosparql` `qudt-schema` `qudt-units` | | | |
| `disaster-event-module-generalized` `disaster-event-module-extensions` `disaster-properties-ontology` | `http://knowwheregraph/ontology/{deo,dmdo,dpo}#` | **no — namespace has no TLD** | **borrowed** |
| `undrr-isc-hazard-classification` | `https://undrr-hip.org/` | untested | untested |

**Not cached, and named in `CLAUDE.md`'s conventions: CF Standard
Names via NERC NVS2 collection P07.** It is the observed-property
vocabulary for Part 2 and it is the one binding `exp-01` showed would
have turned the composite-versus-PM2.5 substitution into a validation
failure. Either cache it or record why not — a convention that names a
vocabulary the cache does not hold is a claim about coverage that
nothing checks.

**If this table grows past a handful of rows, generate it from the
provenance sidecars.** A hand-maintained table keyed by name, sitting
beside the artifacts it describes, is the defect this project spent four
gate rounds on — the corrected value in one place and the residue in the
summary a reader reads first. `scripts/lint-selftest.py --table` is the
worked example of the fix.

## Known findings on cached vocabularies

Recorded here so a reader hits them before quoting a definition. Each is
measured, not inferred.

**DMDO** — `disaster-event-module-*.ttl`, `disaster-properties-ontology.ttl`
Source: <https://github.com/KnowWhereGraph/dmdo>

- Namespace is `http://knowwheregraph/ontology/deo#` — **no TLD**. Not
  resolvable by anyone. **Borrowed, not bound**, permanently.
- The prefix expands with `#`; every core class is declared with `/`.
  So `deo:Hazard`, the form used in the published diagram, is declared
  **nowhere in any file**. Bind `<http://knowwheregraph/ontology/deo/Hazard>`
  or nothing.
- `Hazard`, `Event`, `Disaster`, `DisasterImpact`, `ElementAtRisk` and
  `HazardType` each carry **two URIs** — one under `deo/`, one under
  `dmdo/` — across the event and properties modules of one release.
- `sosa:hasUltimateFeatureOfInterest` is declared here as a bare
  `owl:ObjectProperty`. That is a local stub; the owning namespace is
  SOSA, which does dereference: <http://www.w3.org/ns/sosa/>. Fetch it
  there. Cached locally as `sosa.ttl`.

- **The ontology hedges the subclassing the diagram asserts.**
  `deo:Event`'s own `skos:description` reads *"in that sense this
  concept **can also be mentioned as** a subclass of
  `sosa:FeatureOfInterest`"*. The published diagram draws a solid
  subclass arrow and the paper states it as fact. Three renderings,
  three strengths, ontology weakest. Before treating
  `Hazard ⊑ FeatureOfInterest` as a convergence with anything, confirm
  an actual `rdfs:subClassOf sosa:FeatureOfInterest` triple exists.

- **The event-alignment claim has no vocabulary behind it.** The
  repository README advertises *"alignment of named events (e.g.
  Hurricane Katrina) across different datasets (e.g. NOAA Storm Events,
  FEMA Disaster Declarations Summaries, NOAA Historical Hurricane
  Tracks)"*. Measured across all four cached graphs:

  | Construct | Occurrences |
  |---|---|
  | `owl:sameAs` | 0 |
  | `skos:exactMatch` / `closeMatch` | 0 |
  | `prov:alternateOf` / `specializationOf` / `wasDerivedFrom` | 0 |
  | `dcterms:identifier` / `schema:identifier` | 0 |
  | anything matching `*name*`, `*align*`, `*match*`, `*identif*` | none |

  The alignment is almost certainly done at **instance** level — one
  minted URI per named event, every dataset record pointed at it —
  which leaves no trace in the schema and is a reasonable way to do it.
  It is a description of what the pipeline does with the ontology, not
  a mechanism the ontology supplies. **There is nothing to borrow.**

  This cuts two ways and both belong in ADR-001.

  *For the four-class decomposition:* the one published vocabulary in
  this domain that advertises solving cross-dataset event alignment
  publishes no vocabulary for it. Borrowing CIM's structure was a choice
  between the best available decomposition and none, rather than between
  two candidates — which is a stronger reason of record than "CIM's was
  the best we found."

  *Against it:* KnowWhereGraph demonstrably aligns named events across
  three datasets **without** an alias vocabulary. That is evidence the
  job can be done by instance-level minting plus a precedence rule in
  the transform, and it is the only working system in this domain either
  way. An absence of alternatives is weak evidence for a design; a
  working system that does without it is evidence about cost. ADR-001
  question 1 is recorded as settled and this is the first material
  challenge to it — record it rather than resolve it here.

- **The advertised event-alignment capability has no vocabulary behind
  it.** <https://github.com/KnowWhereGraph/dmdo/blob/main/README.md>
  offers *"alignment of named events (e.g. Hurricane Katrina) across
  different datasets (e.g. NOAA Storm Events, FEMA Disaster
  Declarations Summaries, NOAA Historical Hurricane Tracks)"* — the
  problem ADR-001 exists to solve. Measured across all four cached
  graphs:

  | Construct | Occurrences |
  |---|---|
  | `owl:sameAs` | 0 |
  | `skos:exactMatch`, `skos:closeMatch` | 0 |
  | `prov:alternateOf`, `prov:specializationOf`, `prov:wasDerivedFrom` | 0 |
  | `dcterms:identifier`, `schema:identifier` | 0 |
  | any term matching `*name*`, `*align*`, `*match*`, `*identif*` | none |

  So the alignment is something KnowWhereGraph's pipeline **does with**
  the ontology — most plausibly by minting one URI per named event and
  pointing every dataset record at it — not a mechanism the ontology
  **supplies**. That is a reasonable way to integrate, and it leaves no
  trace in the schema. **There is nothing here to borrow.**

  Two consequences. It gives ADR-001 question 2 no help; the A/B/C fork
  stays gated on L2. And it converts ADR-001's ground from *"we chose
  CIM's decomposition"* into *"we checked the domain alternative and it
  is empty"* — the one published hazard vocabulary advertising this
  capability publishes no vocabulary for it.

- **`deo:Event`'s own definition hedges the `sosa:FeatureOfInterest`
  subclassing.** Its `skos:description` reads *"in that sense this
  concept **can also be mentioned as** a subclass of
  `sosa:FeatureOfInterest`"* — weaker than the diagram's solid subclass
  arrow and weaker than the paper's *"which are subclasses of SOSA's
  `sosa:FeatureOfInterest`"*. Three renderings of one relationship at
  three strengths, ontology weakest. Before treating
  `Hazard ⊑ FeatureOfInterest` as evidence of independent convergence,
  confirm an asserted `rdfs:subClassOf` triple exists rather than a
  suggestion in prose. This is the CURIE-versus-graph failure in a
  different register: the diagram asserts what the graph only mentions.

**UNDRR/ISC HIP** — `undrr-isc-hazard-classification.ttl`
Source: <https://github.com/KnowWhereGraph/dmdo>
Underlying publications, cited in the file's own `terms:description`:
<https://www.undrr.org/publication/hazard-information-profiles-supplement-undrr-isc-hazard-definition-classification>
and
<https://www.undrr.org/publication/hazard-definition-and-classification-review>

- Namespace is `https://undrr-hip.org/` — has a TLD, so unlike DMDO it
  **could** be bindable. Dereference untested.
- Uses the Scientific Taxonomy Pattern: OWL classes with punned
  individuals, structure carried by `hip:broader` (346),
  `hip:isMemberOf` (297), `hip:identifier` (205), `hip:synonym` (185),
  `hip:definitionSource` (159). SKOS supplies **annotation vocabulary
  only** — 298 `skos:definition`, and **no `skos:Concept`, no
  `skos:inScheme`, no `skos:exactMatch`**.
- Against ADR-000 D5's four reasons for choosing SKOS, HIP as shipped
  delivers one: hierarchy, but via `hip:broader` rather than
  `skos:broader`. No cross-scheme mapping, no per-concept deprecation,
  one `owl:versionInfo "v 1.0"` for 9,600 lines.
- Wildfire is `hip:EN0013`, ten synonyms, with an authoritative
  definition adapted from FAO 2010.
- <https://github.com/KnowWhereGraph/dmdo/blob/main/taxonomy-building/README.md>
  is a stub reading "TO ADD" twice with two images, and the root
  README's Contributors section reads "TO ADD" as well. The Scientific
  Taxonomy Pattern is described in a paper, not in the repository —
  Stephen, Shimizu, Schildhauer, Zhu, Janowicz and Hitzler, *"A Pattern
  for Representing Scientific Taxonomies"*, WOP@ISWC 2022, cited at the
  foot of <https://github.com/KnowWhereGraph/dmdo/blob/main/README.md>.
  **Do not cite the repository as the source of a modelling decision** —
  the diagrams carry the pattern and the prose does not.

## Licensing

The project intends to be open source. Cached vocabularies carry their
own licences and the papers behind them are CC BY 4.0. If a definition
is quoted into a `description` in `vocab/`, or the cache is committed,
attribution terms travel with it. Check before the first quote lands;
retrofitting attribution across a schema is expensive.