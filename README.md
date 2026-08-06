# OHIM — Operational Hazard Information Model

A declarative, multi-hazard information model for **live** hazard and
emergency data — the canonical form that source feeds are transformed
into.

Namespace: `https://w3id.org/ohim/`

There is no international standard for hazard data analogous to IEC CIM
for electric utilities. What exists is a stack of partial standards,
each covering one slice, with no unifying model. This project assembles
one, and does not assume it is correct.

## Where this sits

The closest published work is the **Disaster Management Domain Ontology**
(DMDO) from the KnowWhereGraph project. The relationship in one sentence:

> DMDO integrates published data about **what happened**. OHIM
> canonicalises live feeds about **what is happening**.

That difference in tense, not in domain, is what OHIM's distinctive
content is for. Source verification tier, absent-versus-zero, candidate
matches that suggest identity without asserting it, an epistemic
discriminator on every observation, and correction distinguished from
supersession — every one is an operational-data concern a curated
reference graph does not have, because a published dataset is labelled
once, at publication, by someone who looked.

**"Operational" here means the posture, not the subject.** DMDO uses the
word for its operations domain — processes, tasks, resources. OHIM uses
it for live acquisition as against retrospective integration. Part 5
covers the operations subject, and DMDO's module for it is figures with
no ontology.

Borrowing note: DMDO's namespace, `http://knowwheregraph/ontology/deo#`,
has no top-level domain and cannot resolve for anyone, so it can be
**borrowed and cited but never bound**. Its last commit is April 2024.
See `vocab/external/README.md`.

| Layer | Technology |
|---|---|
| Structure | LinkML (`vocab/`) |
| Code lists | SKOS concept schemes (`codelists/`) |
| Transformation | Datalog / Mangle (`transform/`) |
| Design checking | Lean and Alloy (`design/`) |

Everything in `build/` is generated. The source of truth is `vocab/`.

## Status

**Pre-alpha. Do not depend on this.** No vocabulary has been authored
yet; the repository holds the design record, the claims register, and
the toolchain.

**The work is scoped in units, and unit 01 is Part 2 plus the fragment
of Part 0 it depends on.** Its design gate is closed and implementation
is open. **Part 0 is therefore authored to the extent Part 2 needs it,
and later units will extend it** — LinkML is additive, so a class added
for Part 1 does not invalidate one authored for Part 2. Read "the design
gate passed" as *settled for this unit*, not as *the foundation is
complete*.

**Part 1 has not been measured, planned or designed.** It gets its own
cycle.

See `claims.md`. Many entries are `falsified` with evidence attached,
and **none is `tested`**. That is the intended state — a register
recording only successes would be worthless.

## Method

This project is **falsification-driven**, and falsification is used as
a governance check on every artifact type, not only on proofs.

Two roles work against the same repository:

- **H** — the builder. Authors the vocabulary, code lists, transform,
  ADRs, proofs, plans, and the coverage matrix.
- **O** — the overseer. Reads only what H produced, never the design
  rationale, and tries to break it. Writes only claim statuses and
  review messages.

H works in four gated stages — **measure → plan → design →
implement**. At the end of each, H posts to `review-inbox.md` and
stops. O falsifies and replies. H may not pass a gate until O has
posted, and must address every `blocked` finding. H may contest a
finding once; unresolved disputes are adjudicated by a human and the
outcome is recorded either way, including when O is overruled.

`CLAUDE.md` holds the invariants, the file-ownership rule, and the
declare-don't-discover rule for tooling changes. `FALSIFIER.md` holds
O's charter and carries a version number O must state, so a stale
charter fails loudly rather than silently. `docs/coverage.md` is the
comprehensiveness instrument — a capability checklist with explicit,
ranked gaps.

**Guards are themselves guarded.** `make lint-selftest` exercises every
lint rule against fixtures with known-correct outcomes, in both
directions, and fails on any fixture no case references. Before those
fixtures existed, every firing of every rule had been a false positive.

## Parts

Segmented by **epistemic kind**, not subject matter. Weather and air
quality are not parts — they appear in Part 2 as observations and
Part 3 as forecasts: the same class with different procedures.

| Part | Scope |
|---|---|
| 0 | Foundation — entity core, identity, time, geometry, coverage, sampling, provenance |
| 1 | Hazard — process, event, area, intensity, cascade relations *(not yet started; a later unit)* |
| 2 | Observation — sensed and modelled state, distinguished by `procedure` and a required `epistemicKind` |
| 3 | *vacant* — merged into Part 2 by ADR-003; the number is retained rather than renumbered |
| 4 | Exposure — exposed elements, vulnerability, risk |
| 5 | Intent and Action — plans, orders, resources, assignments, missions |
| 6 | Warning — zones, protective actions, alerts |
| 7 | Context — terrain, hydrography, transport, land cover |
| R | Registry — observable properties, units, code lists (cross-cutting) |

Parts form a module dependency order: Part *n* may reference Parts < *n*,
never >.

### Entity core

Part 0 declares six abstract entities. Parts 1–7 assign them **roles in
relations** — no entity is subtyped by a role it plays, so a fire
station is one `Asset` appearing in both an exposure relation and an
assignment relation rather than two objects joined by `sameAs`.

`Agent` · `Asset` · `Place` · `Activity` · `Document` · `Statement`

`Statement` is the reified assertion. It was recorded as needing no
class until four slots hung off it — source verification tier, operating
mode, model version, profile conformance — and a discriminator that must
sit on *every* assertion needs a class that **is** the assertion. See
ADR-004.

**The core is known to be incomplete, deliberately.** Subjects appear as
arguments in the relation signatures below and are declared nowhere —
`HazardEvent`, `Incident`, and in `authority`, `HazardType` — along with
structural primitives (`Interval`, `Measure`, `Level`) that nothing
binds and code-list references (`CapabilityType`, `Function`) with no
scheme. See `claims.md` C24, filed `falsified` with all eight.

`HazardEvent` and `Incident` are the two that matter most, and they are
distinct: the **hazard** is the phenomenon, the **incident** is the
managed occurrence with a name, a lifecycle, an authority and a
containment figure. Two hazards can be one incident, which is what
`partOf` was written for.

Both are Part 1 content. Unit 01's Part 2 observations — air quality and
weather — take a *site* as their feature of interest, not a hazard, so
declaring them now would expand this unit's surface for content it does
not use. The line held throughout: **correct what would land wrong in
`vocab/core/`; defer what would only make it larger.**

ADR-006 removed a wrong carrier (hazard events were listed under
`Activity`) and deliberately added none. The question *what carries the
hazard* is therefore **unanswered rather than wrongly answered**, which
is the better of the two states and is not the same as answered.

Three Part 0 relations carry the structure the parts share:
`partOf(Whole, Part, Interval)` for crews, incident complexes and
sub-sampling; `authority(Agent, Place, HazardType, Function, Interval)`
for jurisdiction, mutual aid and delegation; and
`capability(Agent | Asset, CapabilityType, Level, Interval)` for
qualifications and resource typing.

### Modalities

Four, of which the first two carry most standards work and the last two
are usually missed:

| Modality | Emergency management | Home |
|---|---|---|
| **is** — observed | monitors, perimeters, positions | Part 2, `epistemicKind: observed` |
| **will be** — modelled | forecast, spread model, plume | Part 2, `epistemicKind: modelled` |
| **shall be** — intended | incident action plan, resource order, closure | Part 5 |
| **must be** — mandated | jurisdiction, mutual aid, delegation | Part 0 |

Intent is not prediction. Collapsing it into a forecast is the same
category error as collapsing forecast into observation.

The first two modalities share a class and are distinguished by a
required slot rather than by a module boundary. That is a deliberate
trade: a module boundary is checkable by reading a file tree, a required
slot only by running validation. See ADR-003.

## Layout

```
CLAUDE.md            invariants, file ownership, gate protocol
FALSIFIER.md         O's charter, with a version number
claims.md            falsification register
review-inbox.md      H <-> O channel, append-only

vocab/core/          Parts 0-7, jurisdiction-neutral
vocab/profiles/      hazard and jurisdiction bindings
codelists/           SKOS concept schemes (Turtle)
transform/           Mangle/Datalog rules
fixtures/            real captured payloads

design/ADR-000-*     the rationale — the only file O may not read
design/ADR-NNN-*     decisions of record — readable; at a design gate
                     they are the artifact under review
design/lean/         proofs; never extracted to executable code
design/alloy/        structural models

docs/coverage.md     capability matrix with ranked gaps
docs/plan/           gated plans
docs/prompts/        session-opening prompts for H and O
docs/reference/      external specifications
docs/sources/        source register for the reference implementation

scripts/             lint rules and their fixtures
build/               GENERATED — do not edit
```

## Development

```
make env             resolved toolchain and current role
make gen             LinkML -> SHACL, JSON Schema, Mangle decls, docs
make check           SHACL validation against fixtures/
make lint            jurisdiction, declarative-drift, and vacuity rules
make lint-selftest   exercises every lint rule against known fixtures
make lean            design proofs — `sorry` means unproved
make alloy           structural models — scope-bounded
make clean
```

`make gen` and `make check` are non-functional until
`vocab/core/vocabulary.yaml` exists. That is a recorded finding, not an
oversight.

A clean result from any of these is a claim about that tool's coverage
until you have checked what it inspected. Several artifacts in this
repository have passed while asserting nothing. See `FALSIFIER.md` §4.

## Design commitments

- **Reuse over authorship.** External vocabularies are referenced by
  URI, never transcribed — SOSA, PROV-O, QUDT, CF via NERC NVS2,
  ADMS, DQV, DCAT, GeoSPARQL.
- **Jurisdiction-neutral core.** No agency name, national identifier
  scheme, or national namespace appears in `vocab/core/`. All of it
  lives in `vocab/profiles/`, so the model retargets from wildfire to
  flood or earthquake without core edits. Enforced by a lint that tests
  by shape rather than by a list of agency names.
- **Declarative, not object-oriented.** Slots are first-class and
  independent of classes. Profiles compose by conjunction rather than
  requiring tooling to subset. Structure adopted from class-shaped
  standards is **translated, not transcribed**.
- **Generated artifacts are never hand-edited.** One source, many
  serializations.
- **Constraints must be *generable*, not merely expressible.** A
  constraint the source language accepts but the generator silently
  drops is not in force. The test is what appears in `build/shapes.ttl`.

## Open questions

Recorded rather than deferred, each with an ADR or a claim behind it:

- **Whether the standard or the substrate is the asset.** These imply
  very different levels of investment here, and the question is open.
- **Whether a heuristic match can ever establish identity.** Decided no
  (ADR-001), but the claim underneath remains ambiguous between two
  relations with opposite truth values. The decision was chosen for
  being invariant under that ambiguity rather than for resolving it.
- **Whether the four modalities are exhaustive.** Curated narrative
  content is a live candidate falsifier: it is neither observed,
  modelled, intended nor mandated, and `epistemicKind` admits only the
  first two.
- **What carries a hazard.** Nothing in the entity core is a thing that
  happens in the world — every entity is a participant in data
  collection or a data artifact. A hazard process, a hazard event, and
  the managed occurrence that has a name, a lifecycle and an authority
  are three different subjects, and none is declared.
- **Whether the parts segment by one axis.** Parts 2, 3, 5 and 6 segment
  by epistemic kind, as stated. Parts 1, 4 and 7 are named for subject
  matter. A part is a kind of statement and a hazard is a subject; the
  two are different axes and Part 1 stands on both.

Five questions that were open here have been decided: the observation
and model split (ADR-003, merged — with its stated ground since
restated), identity resolution (ADR-001, authority-only), slot carriers
(ADR-004), how cross-slot constraints reach validation (ADR-005, a
generator over `annotations:` — decided and not yet built), and two role
classes removed from the entity core (ADR-006).

## License

TBD — intended to be open source.