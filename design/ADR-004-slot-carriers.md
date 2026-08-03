# ADR-004 — Carriers for CRS and for statement-level slots

**Status:** accepted
**Date:** 2026-08-02

Decides plan item **P17**. Two questions, unrelated except that both are
"which class does this slot land on", and both blocked P6a.

## Decision A — no distinct `crs` slot

GeoSPARQL carries the coordinate reference system **inside the WKT
literal**, as a URI prefix on the value:

```
<http://www.opengis.net/def/crs/EPSG/0/4326> POINT(-121.31 44.06)
```

Measured (A26): the GeoSPARQL vocabulary declares no separate CRS
property; `geo:asWKT` is typed `geo:wktLiteral`, and `geo:Geometry`'s own
description locates the CRS within the position.

**Decision: no `crs` slot. Instead, `asWKT`'s range is constrained to
`geo:wktLiteral`**, so the CRS has a declared carrier rather than an
implicit one.

**Why, and it is not an appeal to minimalism.** A separate `crs` slot is
a **second copy of a fact the literal already carries**, and the two can
disagree. This project has just spent an entire gate on that exact
defect in a different medium — five hand-maintained lists keyed by item
id, four gate blocks, and the repair was to delete the copies rather
than to check them. A duplicated CRS is the same shape with a worse
failure mode, because the disagreement would be between a schema and a
payload rather than between two documents.

**What it costs, stated.** Consumers must parse a literal to read the
CRS rather than reading a property. That is a real cost and it is
narrower than it sounds: the CRS is needed for reprojection, and
anything reprojecting is already parsing the geometry.

**Consequence:** A1's surface moves to **23 bind / 9 write of 32**, by
A1's own arithmetic.

## Decision B — a `Statement` class. A1 moves 14 → 15

Four slots have no carrier among A1's eight Part 0 classes —
`sourceVerificationTier` (A24), and `operatingMode`, `modelVersion`,
`profileConformance` (C12, C15, scheduled by PA23).

ADR-002 recorded `Statement` as *"the sixth [entity], but is already
covered by the provenance layer and needs no new class."* **That was
right when nothing hung off it and is wrong now.**

**Decision: `Statement` is a Part 0 class binding `prov:Entity`.
A1's Part 0 class count moves 14 → 15.**

**Why not `Activity`, which was the alternative.** `prov:Activity` is
the *act* — the retrieval, the observation, the derivation.
`prov:Entity` is the *thing produced*, and an assertion is a thing
produced, not an act. A verification tier is a property of *what we were
told*, not of the telling; a model version is a property of the
assertion, not of the process that emitted it. Putting them on
`Activity` would type an assertion as its own production.

**This is the role-not-subtype rule (ADR-002 Decision B) applied
correctly, not an exception to it.** `Statement` is not a role — it is
not `Observer` or `Resource`. It is a distinct kind of thing that
participates in relations, which is exactly what a Part 0 entity is.

**Consequence worth naming:** C12 is ranked gap #1 and safety-critical —
exercise data must not render as live. A discriminator that must sit on
**every** assertion needs a class that **is** the assertion. That is the
strongest single argument for this decision and it is the one that
would have forced it eventually.

## Consequences

- `crs` leaves the write list; `asWKT`'s range constraint enters P6a's
  definition of done.
- `Statement` enters Part 0. A1's class count is **15**, recorded here
  because `docs/measure/measure-01-part2-part0.md` is a closed measure
  document and is not edited at a design gate.
- P6a is unblocked on both counts.
- ADR-002's Decision A table is amended to carry `Statement` as a sixth
  entity rather than as a note saying it needs no class.
