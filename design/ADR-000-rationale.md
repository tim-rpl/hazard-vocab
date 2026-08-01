# ADR-000 — Foundational rationale

**Status:** accepted
**Date:** 2026-07-31

> This file records *why*, not *what*. It is rationale, not normative
> content. The falsifier session must not read it — anchoring on this
> reasoning defeats the purpose of an independent falsification pass.

## Context

There is no international standard for wildfire or hazard data
analogous to IEC CIM for electric utilities. What exists is a stack of
partial standards, each covering one horizontal slice, with no
unifying model:

- **Terminology** — ISO 22300:2025 (TC 292), NWCG PMS 205
- **Hazard taxonomy** — UNDRR/ISC Hazard Information Profiles (302
  hazards, 8 groups, 48 clusters)
- **Information model** — NIEM Model v6.0 (OASIS Standard Dec 2025,
  submitted to ISO/IEC JTC 1 June 2026; core + governed domain
  namespaces, XML/JSON/RDF); INSPIRE Natural Risk Zones (UML, generic
  hazard/exposure/vulnerability/risk core with a forest fire use case)
- **Observation** — ISO 19156:2023 / OGC OMS, W3C SOSA/SSN 2023
- **Messaging** — OASIS EDXL (CAP 1.2, DE 2.0, RM, SitRep),
  ISO/TR 22351 EMSI
- **Doctrine** — ISO 22320, 22322, 22324
- **Spatial index** — ISO 19170-1 / OGC DGGS

## Decisions

### D1 — Segment by epistemic kind, not subject matter

Parts 0–7 are Foundation, Hazard, Observation, Model, Exposure,
Response, Warning, Context.

CIM's own segmentation (transmission / distribution / market) is
organized by system-of-use and is largely a committee artifact. Do not
copy it.

Segmenting by epistemic kind makes the observed/modelled boundary
structural rather than a property, which is the distinction that
matters most in this domain. It is also hazard-portable: swap the
Part 1 taxonomy and the other seven parts survive.

Subject matter (weather, air quality, hydrology) is *not* a part.
Weather appears in Part 2 as station observation and Part 3 as
forecast — the same class with different procedures. Making weather a
part would force the same for air quality and hydrology, reconstructing
a source inventory and discarding the epistemic split.

### D2 — Observable properties are a registry, not a part

A cross-cutting vocabulary axis, orthogonal to the parts, analogous to
CIM keeping `ReadingType`/`MeasurementKind` separate from the class
model. CF Standard Names for physical quantities, QUDT for units,
SKOS concept schemes for domain code lists.

### D3 — No jurisdiction-specific content in the reference model

An earlier draft placed a national wildfire identifier scheme in
Part 0. This breaks the portability D1 buys. The test: any element
naming a national agency is profile content.

Part 0 provides the *pattern* — an internally-minted stable URI plus an
alias set of `{identifier, scheme, issuingAuthority, assertedTime}`,
following CIM's `Name`/`NameType`/`NameTypeAuthority` triple. Which
schemes exist and their precedence order is profile content.

This is also better within any single profile: "scheme X is the
canonical key" fails on every record lacking one, whereas an alias set
with declared precedence degrades gracefully.

### D4 — Declarative, not object-oriented

Published CIM has no methods — it is an ER model in UML. The real OO
commitments are single inheritance, class-based identity, and
closed-world attribute sets, and all three fit this domain badly:
sources are partial by nature, extension is by third parties, and
profiles need to compose.

Constraint sets compose by conjunction; OO models require tooling to
subset (cf. CGMES profiling). Three layers: signature, constraints,
derivation. The derivation layer is what CIM structurally cannot
express and is the main prize — the transform becomes part of the
specification rather than bespoke code per source.

*Superseded reasoning:* an earlier version of this argument claimed
UML reification destroys hyperedge structure. That objection does not
apply — the hypergraph is a downstream projection, and a class with N
slots maps mechanically to an N-ary relation. The case for declarative
rests on vocabulary fit and profile composition alone.

### D5 — LinkML for structure, SKOS for code lists

LinkML because slots are first-class and independent of classes
(property-centric, not class-centric), because `slot_uri` / `class_uri`
/ `mappings` bind directly to external vocabularies rather than
transcribing them, because mixins and imports give extension without
inheritance depth, and because it compiles to SHACL, JSON Schema,
RDFS/OWL, SQL DDL, and docs from one source.

Rejected: SHACL alone (constraint language, not vocabulary language —
better as a target); OWL (description logic semantics surprise
everyone expecting a schema; generate RDFS-level output instead); CUE
(elegant unification semantics that model profile composition well,
but no URI binding and no term-registry interop); raw Datalog `.decl`
(nowhere for definitions, mappings, or docs).

SKOS for code lists because they have a different change rate and
governance than structure, and because SKOS provides hierarchy,
cross-scheme mapping (Oregon Level 1/2/3 ↔ California Warning/Order),
per-concept deprecation, and independent versioning. LinkML enums
reference SKOS concepts via `PermissibleValue.meaning`.

### D6 — Datalog for transformation, Lean and Alloy for design

Datalog (Mangle) is the implementation. Lean proves properties about
the merge and identity algebra — roughly a CvRDT with an
identity-resolution equivalence — and constrains how the Datalog is
written. Alloy handles bounded structural claims where a counterexample
at small scope is what you actually want.

Neither Lean nor Alloy runs in CI or touches data. Both are deletable.

### D7 — Falsification-driven, not spec-first

A comprehensive specification written before L2 is tested is a
specification whose foundation is about to change. Agentic
implementation removes the friction that used to make premature
commitment self-correcting: slow implementation gives time to notice
you are wrong; fast implementation converts a bad foundation into a
large sunk cost in an afternoon.

Capture accumulated thinking as ADRs and claims — both are capture,
neither is commitment. The comprehensive spec is generated later from
`vocab/` and `claims.md`, once claims carry statuses other than
`asserted`.

## Consequences

- Part 1 and Part 5 are the most jurisdiction-contaminated and will
  carry the most profile content. Parts 3 and 6 came out cleanest.
- Part 5 (Response) is currently unfilled — there is no public feed for
  resource assignment. Aircraft position is a Part 2 observation, not a
  Part 5 assignment.
- Coverage-valued results (grids, contours, DEM, radar) need ISO 19123
  / OGC CIS as a Part 0 primitive. OMS handles discrete observations
  well and fields badly.
- The `⚠` gaps where no standard exists: hazard mereology (incident
  complexes), uncertainty representation, and evacuation levels.
  Evacuation is the one with an actual constituency waiting for it.

## Deliberately not decided here

- Which identity resolution option (see ADR-001).
- Whether the standard or the substrate is the asset. These imply very
  different levels of investment in this repository, and the question
  is open.
