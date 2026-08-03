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

**Consequence:** `crs` leaves the local-slot list. **No total is
asserted here** — see the partition below, and the note that no number
in this ADR is the unit's slot total.

## Decision B — a `Statement` class

Four slots have no carrier among A1's eight Part 0 classes —
`sourceVerificationTier` (A24), and `operatingMode`, `modelVersion`,
`profileConformance` (C12, C15, scheduled by PA23).

ADR-002 recorded `Statement` as *"the sixth [entity], but is already
covered by the provenance layer and needs no new class."* **That was
right when nothing hung off it and is wrong now.**

**Decision: `Statement` is a Part 0 class binding `prov:Entity`.**

**Counts, stated precisely, because an earlier draft of this line
mislabelled them and the corrected version landed only in the table
sixty lines below.** It read *"A1's Part 0 class count moves 14 → 15"* —
14 is the **unit** total, not a Part 0 count.

- **This unit's Part 0 fragment: 8 → 9 classes.**
- **The unit: 14 → 15 classes.**
- **Part 0 itself is larger than either** and is not counted here. A8
  pulls 8 elements into this unit and **defers `Document`**, which
  ADR-002 lists as a Part 0 entity. A number describing the fragment is
  not a number describing Part 0.

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

## Decision C — `assertedTime` binds `prov:generatedAtTime`

Deferred to this gate at PA25 and decided here rather than carried
again. They are **one slot**: `assertedTime` is the local name and
`prov:generatedAtTime` is its `slot_uri`.

**Why they are the same.** An alias is a `prov:Entity` — a thing
asserted — and the time it was generated *is* the time it was asserted.
ADR-001 §4 already stated that `assertedTime` comes from PROV-O; what
was missing was saying which term, and therefore whether the slot was a
bind or a write. It is a bind.

**It adds a bound slot and no new external URI.** Those are different
populations and an earlier draft conflated them — the sentence read
*"it does not add to the bind count"*, which contradicts the table
below, which shows the bound-slot count **unchanged at 16**.

Precisely: `prov:generatedAtTime` was already among the external URIs
A3 enumerated, **and the slot binding it was already counted in the 16
under the URI's name rather than ours.** The bound-slot count is
therefore **unchanged at 16**; the local-slot count goes **10 → 9** at
this decision, and **→ 8** once Decision A removes `crs`.

An earlier draft said the bound count moved 16 → 17. It does not — that
counted one slot twice, which is the defect this ADR's own partition
section is about.

## Reconciliation of the surface figure — the partition, and what it found

O asked for an explicit slot partition rather than another restatement.
It does not reconcile, and the reason is the finding.

**The `23` was never a count of slots.** A3's enumeration reads *"21
external slot URIs"* and then lists 35 terms of three different kinds:

| Kind | Terms | Count |
|---|---|---|
| **`slot_uri`** — a bound slot | `observedProperty`, `hasFeatureOfInterest`, `hasResult`, `hasSimpleResult`, `resultTime`, `phenomenonTime`, `madeBySensor`, `usedProcedure`, `isHostedBy`, `hasMember`, `wasAttributedTo`, `generatedAtTime`, `hasGeometry`, `asWKT`, `hasUnit`, `numericValue` | **16** |
| **`class_uri`** — a bound class | `Observation`, `Sensor`, `Platform`, `FeatureOfInterest`, `Procedure`, `ObservableProperty`, `ObservationCollection`, `prov:Agent`, `prov:Activity`, `prov:Entity`, `org:Organization`, `geo:Geometry`, `qudt:QuantityValue` | **13** |
| **`meaning`** — a permissible-value URI, **content-verified** | 6 QUDT units | **6** |
| **`meaning`** — a permissible-value URI, **status-code only** | 6 NVS2 P07 standard names | **6** |

**41 external URIs of three kinds, reported as one number.** `23` is
none of them.

**And the value row splits again on verification tier.** A3 set the six
NVS2 P07 standard names apart deliberately: they returned 200 on
per-term paths and **their payloads were never inspected**, where the
six QUDT units were content-verified. Folding them into one `12` would
hand P5 a single work list over two evidence tiers — the finding of this
section applied to its own repair. They are two rows above.

**And `33` inherits the same defect**, because it was `23 + 10` — a
mixed-kind URI count added to a local-slot count. A31's `35–36` counts
something else again: the unit's slots after the alias translation.
**The two baselines are not comparable, so the reconciliation table this
section previously carried was arithmetic over incommensurable
quantities**, and its agreement with the earlier figure was the
coincidence it admitted to being.

### What P5 actually has to do

This is the figure P5 needs, and it is a work list rather than a total:

**A slot partition, stated as slots.** Two disjoint sets over the slots
A1 enumerated. Classes and permissible values are **separate
populations and are never summed with slots** — that summing is the
defect this whole section is about.

| Slot population | Count |
|---|---|
| Slots carrying an external `slot_uri` | **16** |
| Slots with no external term, defined locally | **8** |
| **Distinct total of A1's enumerated slots** | **24** |

**Two removals, not one.** Decision A removes `crs` and Decision C
removes `assertedTime`, both from A1's ten: `10 − 2 = 8`, total **24**.
An earlier draft carried 9 and 25 — it applied one removal and then
**added `epistemicKind`, which A1 never enumerated**, into a row labelled
*A1's enumerated slots*.

**`epistemicKind` is a slot this unit needs that A1 did not enumerate.**
It belongs beside the list, not inside it — and it is the first
demonstrated member of a class this ADR has been asserting exists.
**D10's nominated falsifier — *the enumerated list is itself
incomplete* — has therefore already fired**, by at least one, on
evidence this ADR was carrying without drawing the conclusion.

**`assertedTime` does not move the first row, and an earlier draft said
it did.** That draft read **17**, adding `assertedTime` to a set that
**already contained `prov:generatedAtTime`** — the URI it binds. One
slot counted under two names. Decision C settles that they are one slot;
it does not create a second.

`17 + 9 = 26` was therefore the same defect this section diagnoses four
lines above it, in this ADR's own words: *"33 inherits the same defect,
because it was 23 + 10 — a mixed-kind URI count added to a local-slot
count."* Corrected 2026-08-02. **The distinct total is 25.**

Separate populations, listed and not added:

| Population | Count |
|---|---|
| Classes carrying an external `class_uri` | 13 |
| Permissible-value URIs, content-verified (QUDT units) | 6 |
| Permissible-value URIs, **status-code only** (NVS2 P07) | 6 — verify before binding |

### 25 is not the unit's slot total, and no number here is

**A1 never enumerated the schema's slots.** It enumerated *external
URIs* and *local terms* — two populations that do not sum to a schema,
which is why every total derived from it has been wrong. `25` is the
count of **the slots A1 enumerated**, and it is the last figure this ADR
will assert.

**The unit's slot total is unknown, and P5's first output is the
authoritative count.** That quantity has taken four values across four
gates — `23/9 of 32`, `24/9 of 33`, `17 + 9 = 26`, `25`, and now `24` —
and each was arithmetic over a population nobody had fixed. **The
replacement baseline is the enumerated list, not a number**; the number
comes from the artifact.

**What P5 works from:** the **16** bound slots and the **8** local ones
by name, the 13 class bindings, the 6 verified value URIs, the 6 that
need verifying first, and **`epistemicKind`**. Not a total.

**Slots: 16 bound + 8 local = 24 of A1's enumerated slots**, plus
`epistemicKind` outside that list. It is not the unit's slot total and
is not claimed to be one.

**`23 bind / 10 write of 33` and `35–36` are both retired rather than
reconciled.** Neither is recoverable, and carrying either forward would
be a fifth figure agreeing with a fourth by accident. The four counts
above are what P5 works from.

**Falsifier:** a term in the `slot_uri` row that is a class, or in the
`class_uri` row that is a property, on inspection of its published
graph.

## Class counts — three documents, three numbers, and a mislabel

| Source | Says | Verdict |
|---|---|---|
| ADR-001 Consequences | *"Part 0 gains four classes rather than one"* | **Wrong.** That is the *literal transcription* figure, which this ADR's own *translate, don't transcribe* rule rejects two sections earlier. Corrected in ADR-001 |
| A31 | the translation is *"the same class count and +2 slots"* | Correct — `NameType` became a code list, `NamingAuthority` became `Agent` |
| ADR-004, as first written | *"A1's **Part 0** class count moves 14 → 15"* | **Mislabelled**, and it survived in Decision B until 2026-08-02 after being corrected here. 14 is the *unit* total. **This unit's Part 0 fragment goes 8 → 9**; the unit goes 14 → 15; **Part 0 itself is larger and neither figure describes it** |

The mislabel matters because this ADR declares itself the superseding
authority on the count, so the wrong label is what the next reader
inherits.

**Corrected: Part 0 is 8 classes → 9 with `Statement`. The unit is 14 →
15.**

## Decision D — the binding construct where two classes share a URI (B4)

`Statement` binds `prov:Entity`. Our abstract `Entity` must not also
bind it, and the choice of construct is not neutral:

- **`class_uri` on both** merges them into **one SHACL node shape
  carrying the union of their required slots** — every `Entity` would
  inherit `Statement`'s obligations.
- **`exact_mappings` on both** asserts the equivalence ADR-002's own
  addendum names as the false claim, and is what the `exact-mappings`
  lint rule exists to catch.

**Decision: `Statement` carries `class_uri: prov:Entity`. Our `Entity`
carries no external `class_uri` at all.**

Our `Entity` is an abstraction over `Agent`, `Asset`, `Place`,
`Activity`, `Document` and `Statement` — a local convenience for slot
reuse. It is not `prov:Entity`, which is specifically *a thing produced*
and which `prov:Activity` is explicitly not. Binding our abstraction to
it would have been convenience mistaken for identity.

`Entity` may carry `close_mappings` to nothing in particular; it needs
no external term, and a class without one is not a defect.

**The real collision is `Document`, not `Entity`, and an earlier draft
of this decision foreclosed a binding nobody had proposed.** Our
abstract `Entity` was never a candidate for `prov:Entity`. **ADR-002's
entity table is**, and it still reads:

> | `Document` | IAPs, situation reports, delegation letters, orders as
> legal instruments | `prov:Entity`, `foaf:Document` |

**Two external class URIs on one class, one of which `Statement` now
takes.** O ran both constructs: `class_uri` on both fires `shared-uri`;
the mixed construct — `class_uri` on one, `exact_mappings` on the other
— **passes both rules** and is exactly the equivalence ADR-002's own
addendum names as the false claim.

**Decision: `Document` carries `class_uri: foaf:Document` and nothing
else.** `prov:Entity` is `Statement`'s alone.

`Document` *is* a `prov:Entity` in the ordinary sense — so is
`Statement`, so is any produced thing — which is the point: a URI that
fits every produced thing distinguishes none of them, and asserting it
on two classes either merges their shapes or asserts a falsehood.
`foaf:Document` is the term that says something. The PROV relationship
is recorded here, in prose, rather than as an equivalence the tooling
would have to be lied to about.

**ADR-002's table is amended in the same pass**, so the row a reader
inherits matches this decision.

**Guarded rather than remembered:** the `shared-uri` rule fails on two
classes sharing a `class_uri`, with `shared-class-uri.yaml` carrying the
case. **Its slot branch had no fixture until 2026-08-02** — deleting
that branch changed no outcome while the report read 8/8. Now
mutation-covered on both branches at 33 pairs.

## Consequences

- `crs` leaves the write list; `asWKT`'s range constraint enters P6a's
  definition of done.
- `assertedTime` leaves the local-slot list and binds
  `prov:generatedAtTime`.
- **The surface is the four populations in the partition above, not a
  pair of totals.** An earlier draft of this line read *"23 bind / 9
  write of 32"* — the figure this same ADR declares unrecoverable sixty
  lines earlier. Withdrawn 2026-08-02.
- `Statement` enters Part 0. **This unit's Part 0 fragment is 9
  classes; the unit is 15.** Part 0 itself is larger — `Document` is a
  Part 0 entity per ADR-002 and is deferred by A8 — so neither figure
  describes Part 0. Recorded here because
  `docs/measure/measure-01-part2-part0.md` is a closed measure document
  and is not edited at a design gate.
- P6a is unblocked on both counts.
- ADR-002's Decision A table is amended to carry `Statement` as a sixth
  entity rather than as a note saying it needs no class.
