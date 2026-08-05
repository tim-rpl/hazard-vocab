# ADR-006 — Two bindings in ADR-002's entity table are wrong

**Status:** accepted
**Date:** 2026-08-04

Supersedes ADR-002 on two rows of its Decision A table. ADR-002 is
accepted and is not edited; the rows carry amendment markers pointing
here, which is the same treatment ADR-004 Decision D gave the `Document`
row.

## Context

Charter v10 added §5.1 **Q12 — what carries the hazard itself**. Eleven
use questions had asked about everything around a hazard and none about
the hazard, and running Q12 against ADR-002 surfaced two bindings that
would land wrong in `vocab/core/` at P6a, when invariant 7 forces a
`description` onto every class.

Both are the same error in different vocabularies, and it is an error
this project has already been bitten by once: **a term that resolves,
means something adjacent, and is wrong.** `qudt:unit` did not exist,
OMS returned a 288-byte stub, and `sosa/thisTermDoesNotExist` returns
byte-identical to a real term. A binding is not verified by its name
reading correctly.

## Decision A — `Activity` does not carry hazard events

ADR-002's row reads:

> | `Activity` | Observation acts, assignments, **hazard events**,
> warning issuances | `prov:Activity` |

**`prov:Activity` is a provenance term for how a data artifact came to
be.** A hazard produces no data artifacts. It burns, floods or shakes.
Observation acts, assignments and warning issuances are activities in
exactly PROV's sense — each produces or transforms a record. A wildfire
is not one of those, and binding it to `prov:Activity` asserts that it
is.

**Decision: `hazard events` leaves the `Activity` row.** The row keeps
observation acts, assignments and warning issuances, and keeps
`prov:Activity`.

**What carries a hazard is deliberately not decided here.** That is Part
1 and out of this unit — see *Recorded, not decided* below.

**Falsifier:** a published `prov:Activity` definition, or a PROV
constraint document, under which a physical process producing no entity
is a well-formed `prov:Activity`.

## Decision B — `Place` does not bind `sosa:FeatureOfInterest`

ADR-002's row reads:

> | `Place` | Zones, jurisdictions, facilities, sampling locations |
> `sosa:FeatureOfInterest`, ISO 19112 |

**`sosa:FeatureOfInterest` is a role, not a kind of thing.** SOSA
defines it as the thing whose property is being estimated — which is a
position in an observation, exactly like `sosa:Platform` and
`sosa:Sensor`. ADR-002's own addendum already flags those two as role
classes. This one sits on the adjacent row of the same table and was
missed.

**This is ADR-002 Decision B — role, not subtype — failing on ADR-002's
own table.** Invariant 6 is the rule; the entity table is where it was
first applied; and the rule was applied to two of the three role classes
in it.

**Decision: `Place` binds ISO 19112 and does not bind
`sosa:FeatureOfInterest`.** A place is a feature of interest *when an
observation is about it*, which is a role assignment in Part 2's
relation, not a class binding in Part 0.

**Falsifier:** a reading of SOSA under which `FeatureOfInterest` is a
kind of thing rather than a role — one that does not equally make
`Platform` and `Sensor` kinds of things, since ADR-002 already rejects
that for those two.

**Second reason this is due now rather than at P6a.** If the Part 1
binding candidate holds — `deo:Hazard ⊑ sosa:FeatureOfInterest` in the
Disaster Event Ontology — then a `Place` bound to
`sosa:FeatureOfInterest` collides with it under C21, two classes
claiming one external URI. `shared-uri` would fire on the design at
authoring time. That is the guard working on a real decision rather than
a fixture, and it is an argument for removing the binding before the
collision rather than after.

## Consequences

- **P6a authors `Place` with ISO 19112 alone and `Activity` without
  hazard events.** Both descriptions land under invariant 7, so both
  would have been written wrong.
- **No slot moves and no class is added or removed.** ADR-004's
  generated surface is untouched — this changes two bindings, not the
  partition. Verified: `derive-surface.py --check` unchanged.
- **`docs/coverage.md:192` is corrected in the same pass**, from
  `covered` to `partial`. See below.

## The coverage row O falsified

`docs/coverage.md:192` read:

> | Incident aggregation (complexes) | Part 0 `partOf` | `covered`
> (ADR-002) |

`partOf(Whole, Part, Interval)` exists. **The thing it would range over
does not.** O falsified the status under `CLAUDE.md`'s rule that a
`covered` status is an assertion H makes and O may break; H applies the
correction. It is now `partial` — the mereology primitive is declared,
its domain is not.

`Incident record and lifecycle` at `:189` is homed in Part 1 and is
**not** touched: Part 1 is out of this unit and O explicitly did not
falsify it.

## Recorded, not decided — Part 1

**ADR-002 Decision B's exemplar relations are stated over three
undeclared types.** Grepped across `design/ADR-001..005`,
`docs/coverage.md` and `vocab/`, the only occurrences of `HazardEvent`,
`Incident` and `HazardType` in the readable tree are these three lines:

```
exposure(Asset, HazardEvent, Measure)                         :57
assignment(Asset, Incident, Agent, Interval)                  :58
authority(Agent, Place, HazardType, Function, Interval)       :182
```

The section whose first line is *"Entities are declared once in Part 0"*
makes its forcing argument with subjects it never declares.

**Why it stayed invisible is structural and is worth recording.**
ADR-000 D1 says the parts segment by epistemic kind. Parts 2, 3, 5 and 6
do. **Parts 1, 4 and 7 are named for subjects.** So the entity core
caught the subjects with no home at all and left the ones with a part
named after them, on the assumption that the part *was* the home. A part
is a statement kind; a hazard is a subject. Part 1 has been standing on
both axes since ADR-000.

**And `sosa:Procedure` confirms the rule rather than breaking it.** It
appears in Part 2's observation relation and in no entity table —
correctly. A procedure is an IR flight protocol, a hand-digitisation
method or a simulation model: a `Document`, or an `Asset` when it is
software. A role filled by an existing entity, which is
role-not-subtype holding where nobody consciously applied it.

**Declaring `Hazard` and `Incident` is deferred**, and the line is:
*correct what would land wrong in `vocab/core/`; defer what would only
make it larger.* Part 2's observations here are AirNow and Open-Meteo,
whose feature of interest is a site. Declaring them now expands P6a's
surface for content this unit does not use, and that surface has already
taken five values.

**A lead, not a finding.** The Disaster Event Ontology and HIP Ontology
from KnowWhereGraph appear to be the only vocabulary carrying a hazard
class — `deo:Event` generalising `deo:Hazard`, `deo:Disaster` and
`deo:DisasterImpact`, all under `sosa:FeatureOfInterest`, with
`deo:ElementAtRisk` mapping to Part 4 and a reified causal relation
covering ADR-002's unmodelled cascades. **Verify by fetch-and-grep when
Part 1 comes up**, on three questions: does the namespace dereference,
does `deo:Hazard`'s *definition* match the intended use rather than only
its name, and are HIP's annotations richer than the UNDRR HIP IDs
already cited. OMS returned a 288-byte stub, ENTSO-E 404'd and
`qudt:unit` did not exist — none of those announced themselves.

If it holds it is a third independent convergence, after CIM's alias
structure and SBVR's alethic/deontic split.

## What this forecloses

Binding `Place` to `sosa:FeatureOfInterest` later without reopening this
ADR, and treating a hazard as a provenance activity. Nothing else — no
slot, no class and no count changes.
