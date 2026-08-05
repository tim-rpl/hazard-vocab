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
