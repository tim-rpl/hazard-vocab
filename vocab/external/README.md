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

**The register is a separate, wholly generated file: `register.md`.**
It is produced from the per-graph provenance sidecars and is not edited
by hand.

It lives in its own file rather than in a block inside this one, and the
reason is a defect this file caused. A generated region embedded in a
prose document has **two writers** — a generator that owns the block and
a human who rewrites the document — and the human wins silently. That is
what happened: a wholesale rewrite of this file dropped the
`BEGIN/END GENERATED:register` markers, the generator's sync became a
no-op, and several messages reported row counts from the generator's
output rather than from the file. Invariant 1's shape, inside a
human-owned file.

One writer per file removes the class rather than the instance. This
file is prose and is written by hand; `register.md` is generated and is
written by nothing else.

## Known findings on cached vocabularies

Recorded here so a reader hits them before quoting a definition. Each is
measured, not inferred.

**DMDO** — `disaster-event-module-*.ttl`, `disaster-properties-ontology.ttl`
Source: <https://github.com/KnowWhereGraph/dmdo>

- **Last commit April 2024.** The repository is dormant, not in
  progress. That converts the defects below from *current state of an
  active project* into *permanent properties of the artifact* — the
  no-TLD namespace, the `#`-versus-`/` mismatch and the duplicate
  `Hazard` URIs will not be fixed. It also means the cached checksums
  should hold indefinitely, and a checksum change would itself be news.

- **The Operational Module has no ontology.** Its directory holds a
  38-byte README containing only a title, one `.graphml` and PNG
  figures; no `.ttl` exists under any plausible name. The root README's
  image paths point at `modules/operational-module/` while the directory
  is `disaster-operational-module/` — a broken path. So **DMDO covers
  Parts 1, 2 and 4; Part 5 is figures.** An earlier note here said
  otherwise, taken from a paper's description of the module rather than
  from the artifact — the same diagram-over-graph gradient recorded
  below, a fifth time.

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

  Measured across **the three DMDO alignment modules** —
  `disaster-event-module-generalized`,
  `disaster-event-module-extensions`, `disaster-properties-ontology`.
  The fourth cached graph is a republished UNDRR-ISC classification list
  and is scoped out deliberately; see the correction below.

  | Construct | Occurrences in the three DMDO modules |
  |---|---|
  | `owl:sameAs` | 0 |
  | `skos:exactMatch` / `closeMatch` | 0 |
  | `prov:alternateOf` / `specializationOf` / `wasDerivedFrom` | 0 |
  | `dcterms:identifier` / `schema:identifier` | 0 |
  | any `deo:`/`dmdo:`/`dpo:` term matching `*name*`, `*align*`, `*match*`, `*identif*` | none |

  **Two rows of an earlier version of this table were false, and both
  failed the way this file's own rules warn about.**

  *`dcterms:identifier | 0` was a count of a literal CURIE, not of a
  term.* The HIP graph binds `terms:` to
  `<http://purl.org/dc/terms/>` — the same namespace `dcterms:`
  denotes — and writes `terms:identifier`, which occurs **twice**. A
  grep for the literal prefix returns 0 while the term is present.
  **Resolve the prefix before counting**; this is the CURIE-versus-URI
  failure a third time, and this file states the rule.

  *The pattern row dropped its own scoping.* The measurement was
  `(deo|dmdo|dpo):` prefixed and correct; the row was written as
  *"anything matching …"*, which is false — `hip:identifier` occurs
  **205** times and `hip:vernacularName` once. **A row written wider
  than the command that produced it is a false row**, however sound the
  command.

  Neither correction touches the argument: the three DMDO modules are
  clean on every construct and every pattern. Per-concept identifiers
  in a published classification list are expected and are not an
  alignment mechanism.

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