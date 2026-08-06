# Findings carried forward to Part 1

**Opened:** 2026-08-05, during unit 01's implement stage
**Status:** recorded, **not decided** · **Owner:** H

Findings produced while working unit 01 (Part 2 + the Part 0 fragment)
that belong to **Part 1** and were deliberately not decided here.

**Why a document and not a note in an ADR.** Part 1 has not been
measured, planned or designed — it gets its own cycle, and `README.md`
says so. A finding recorded inside a unit-01 ADR is a finding Part 1's
measure gate has no reason to open. This file is the place that gate
looks.

**The line these were held to:** *correct what would land wrong in
`vocab/core/`; defer what would only make it larger.* Neither of the two
below changes a term unit 01 authors.

---

## F-P1-1 — Jurisdiction is a `Place` with an extent, not a classification

**Two jurisdictions over one physical situation is a normal case, not an
edge case.** A fire on a state border; a plume crossing one.

A jurisdiction has geometry and it participates in
`authority(Agent, Place, HazardType, Function, Interval)`. Modelling it
as a classifier **on the hazard** forces a special case for every
situation with two authorities over it.

**Evidence that it is not rare, and it is in production rather than
hypothetical.** The reference implementation already carries two state
thresholds as **separate series**, because an index and a concentration
are not the same quantity — one physical situation, two authorities, two
regimes. `docs/sources/HDC-data-source-register.html` records the
correctness rules that came out of it.

**Falsifier:** a jurisdictional arrangement in the source register or a
captured payload that a classifier-on-the-hazard model expresses without
a special case, *and* that an extent model expresses worse.

**Not decided here** because it needs a carrier, and the carrier is a
Part 1 class this unit does not author.

## F-P1-2 — `authority` already separates two distinct kinds of jurisdiction

`authority(Agent, Place, HazardType, Function, Interval)`:

| Argument | Kind of jurisdiction |
|---|---|
| `Place` | **spatial extent** — who is responsible *here* |
| `Function` | **entitlement to assert** — who may speak to this hazard type at all, regardless of location |

A federal agency's authority over a hazard class is the **second** and
not the first.

**This is worth noticing rather than deriving.** The relation separates
them already, in the form ADR-002 wrote it — which is evidence the
decomposition was right at the time, and it means **neither can be
collapsed into the other** when Part 1 gives them carriers.

**Falsifier:** an authority arrangement expressible with `Place` alone
or with `Function` alone, such that the other argument is redundant in
every real case rather than merely in the common one.

**Interaction with F-P1-1:** if jurisdiction is an extent, `Place`
carries it and `Function` is not a jurisdiction at all but an
entitlement. That reading makes the argument names slightly wrong and
the structure right, which is a better position than the reverse.

## F-P1-3 — the Hazard/Incident distinction is an operational requirement, and a retrospective model shows why

**Found:** 2026-08-05, from `vocab/external/graphs/wildfire-nifc.ttl`
(KWG DMDO v3.0) · **Kind:** measured, from an artifact

**KWG collapses hazard and incident, and loses nothing it needs.** Read
out of the graph with rdflib, not off the names:

| Measured | Value |
|---|---|
| `NIFC_Fire` | `owl:Class`, `subClassOf` **`geosparql:Feature`** and **`sosa:FeatureOfInterest`**, plus four restriction nodes |
| `NIFC_FireObservation` | `subClassOf sosa:Observation` |
| `NIFC_FireObservationCollection` | `subClassOf sosa:ObservationCollection` |
| **`NIFC_IncidentComplexFire`** | **`subClassOf kwg:NIFC_Fire`** — a complex is a *kind of fire*, not a managed occurrence aggregating fires |
| `incidentName` | `owl:DatatypeProperty`, **no domain and no range** |
| `partOf` | **0 occurrences** |
| `contain` (case-insensitive) | **0 occurrences** |

**The missing attribute is the argument.** There is no containment
percentage anywhere in v3.0. Containment is a statement about
**suppression in progress**, and an archive of what happened does not
track it. **OHIM does, and therefore cannot collapse the two.** Two
hazards under one incident is the same shape: a managed occurrence
aggregating phenomena, which `NIFC_IncidentComplexFire ⊑ NIFC_Fire`
cannot express.

**And they do not assert the collapse — they never make the
distinction.** `incidentName` has **no domain**, so nothing in the axioms
says it attaches to a fire at all. *An attribute of the fire* is
convention, not a stated constraint. The distinction has no
representation to be absent from, which is what a retrospective model can
afford.

**So the picture is: a retrospective model of fires with an incident name
attached by habit** — and it is the right model for its purpose. The
finding is not that KWG is wrong. It is that **the attribute forcing our
distinction is exactly the one the retrospective model omits**, which
makes the requirement operational rather than a modelling preference.

**Falsifier:** a live, in-progress hazard-response system that tracks
containment (or any suppression-progress measure) and expresses two
hazards under one managed occurrence **without** distinguishing hazard
from incident.

### Two smaller things carried with it

**`NIFC_Fire ⊑ sosa:FeatureOfInterest` is a second independent instance
of the binding ADR-006 removed.** Two published ontologies bind an entity
to a SOSA role class. That is evidence about **how natural the error is**,
not evidence the decision was wrong — and it is the second reason
`Place`'s binding was worth removing before P6a rather than after.

**`S2Cell_Level13`** — KWG indexes spatially via S2 cells, which is
DGGS-adjacent and bears on how a spatial partition gets keyed.
**`AdministrativeRegion_2`** confirms **jurisdiction-as-region rather
than jurisdiction-as-classifier**, which is F-P1-1 reached from someone
else's artifact.

**And it confirms the Part 2 reading independently.**
`NIFC_FireObservation` is a `sosa:Observation`, `NIFC_Fire` is the
feature of interest, and `NIFC_FirePointOfOrigin` is the ignition
separately — **perimeter-is-an-observation, reached from the data by
someone else**, which is a convergence on ADR-003's subject rather than
on its option.

---

---

## Related, and already recorded elsewhere

- **`HazardEvent`, `Incident` and `HazardType` are declared nowhere** —
  C24, filed `falsified` with all eight counterexamples in four kinds.
  `HazardType` appears in `authority`'s signature, which is why F-P1-2
  cannot be settled without it.
- **Both vocabularies carrying a hazard class are `borrowed`** — DMDO
  permanently, by a namespace with no TLD; UNDRR-HIP by measurement
  (HTTP 000). `vocab/external/README.md`'s generated register. **So Part
  1 authors a hazard vocabulary or borrows structure; it does not bind
  one.** That is measured, not projected.
- **HIP uses SKOS annotations and declares no concept scheme** —
  `skos:Concept` 0, `skos:inScheme` 0, `skos:exactMatch` 0, against
  `skos:definition` 301 and `hip:broader` 346. ADR-000 D5 chose SKOS for
  four properties and annotation-only use delivers at most one of them.
  Cross-scheme mapping is the one that bites, and it is the usual reason
  to adopt an authoritative taxonomy at all.
- **ADR-000 D1's segmentation is mixed** — Parts 2, 3, 5 and 6 segment by
  epistemic kind; **Parts 1, 4 and 7 are named for subjects.** That is
  why the entity core caught the subjects with no home and missed the
  ones with a part named after them. Recorded in ADR-006.
