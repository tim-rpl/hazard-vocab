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

> **The ground stated here on 2026-08-04 was false, and the falsifier
> that breaks it is the one this section wrote and did not run.**
> Withdrawn the same day under BV7-1. It read:
>
> *"`prov:Activity` is a provenance term for how a data artifact came to
> be. A hazard produces no data artifacts. It burns, floods or shakes.
> Observation acts, assignments and warning issuances are activities in
> exactly PROV's sense — each produces or transforms a record. A wildfire
> is not one of those, and binding it to `prov:Activity` asserts that it
> is."*
>
> **It is false in both halves**, and one fetch of the W3C
> Recommendation settles it. Re-verified independently by H at
> `https://www.w3.org/TR/prov-dm/`:
>
> - `prov:Entity` — *"An entity is a **physical**, digital, conceptual,
>   or other kind of thing with some fixed aspects; entities may be real
>   or imaginary."* Not restricted to data artifacts; physical is the
>   first word in the list.
> - `prov:Activity` — *"…acts upon or with entities; it **may** include
>   consuming, processing, transforming, modifying, relocating, using,
>   or **generating** entities."* Generation is one item in a `may`
>   list, not a requirement.
> - §2.1.1's worked examples include **driving a car between two
>   locations**, a physical process producing no record.
>
> **So a wildfire is a well-formed `prov:Activity`** — it consumes,
> transforms and relocates physical entities. The removal below is a
> modelling choice this project makes, **not** a conformance
> requirement, and nothing in PROV forbids Part 1 from binding
> `prov:Activity` to a hazard class later.
>
> This is the error this ADR's own Context section names — *a term that
> resolves, means something adjacent, and is wrong* — committed by this
> ADR two paragraphs after naming it, against `prov:Activity` instead of
> against `qudt:unit`. The reading was of the term's **name**, not its
> **definition**.

**The ground, rebuilt on the entity core's own axis.**

`Activity` in ADR-002's table is not "anything PROV would class as an
activity". It is this project's entity kind for **acts performed in
producing, handling and issuing data and decisions** — its members are
observation acts, assignments and warning issuances, and every one of
them is something a responder or a system *does*.

**A hazard event is a subject, not one of those acts.** It is what
Parts 1, 2, 4 and 6 make statements *about*: a thing observed, a thing
assets are exposed to, a thing warnings are issued for. Grouping it with
the acts that produce those statements puts the subject of the record
and the making of the record in one class, which is the distinction the
whole part structure is built on.

**Decision: `hazard events` leaves the `Activity` row.** The row keeps
observation acts, assignments and warning issuances, and keeps
`prov:Activity`.

**What carries a hazard is deliberately not decided here.** That is Part
1 and out of this unit — see *Recorded, not decided* below. **Decision A
removes a carrier and adds none**, so Q12 is now *unanswered* rather
than *wrongly answered*; that is recorded as a finding rather than
presented as an improvement.

**Falsifier, restated so it tests the ground now given:** a statement
this unit needs to make about a hazard event that `Activity`'s slots, as
authored at P6a, serve as well as they serve an observation act — i.e.
evidence that the class is homogeneous on the axis this decision uses.
Testable at P6a, against a real file, and it does not depend on reading
`prov:Activity` narrowly.

**Not a falsifier of this decision:** any PROV definition or constraint
document. PROV permits it either way, which is exactly what the
withdrawal above establishes.

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

> **WITHDRAWN 2026-08-04 under BV7-2. This section claimed a guard would
> catch something it cannot see, in the dangerous direction.** It read:
>
> *"If the Part 1 binding candidate holds — `deo:Hazard ⊑
> sosa:FeatureOfInterest` — then a `Place` bound to
> `sosa:FeatureOfInterest` collides with it under C21… **`shared-uri`
> would fire on the design at authoring time.**"*
>
> **It would not.** `rule_shared_uri` keys on **literal URI strings** —
> `claims.setdefault(str(uri), …)` at `scripts/drift-lint.py:467` — and
> never fetches an external vocabulary, so a subsumption axiom published
> in DEO is outside its subject by construction. C21 is about two
> elements asserting **the same** URI, and the register says so.
>
> Re-run by H on the shipped linter, with a control:
>
> | Probe | Result |
> |---|---|
> | the scenario above — `Place` → `sosa:FeatureOfInterest`, `Hazard` → `deo:Hazard` | **`ok   [shared-uri] 1 file(s)`, exit 0** |
> | control — both classes → `sosa:FeatureOfInterest` | **FAIL**, naming both classes, exit 1 |
>
> The collision exists only where `Hazard` binds
> `sosa:FeatureOfInterest` **directly**, which is not the candidate
> named. **An accepted ADR telling a reader at P6a that a check will
> happen, when it cannot, is worse than saying nothing** — the check
> would be skipped and nothing would report it. C21's evidence now
> carries the bound.

**Second reason this is due now rather than at P6a — restated, and it is
not a guard.** If the Part 1 candidate holds, `deo:Hazard` is declared
a subclass of `sosa:FeatureOfInterest`, and a `Place` also bound to
`sosa:FeatureOfInterest` puts a hazard and a place under one external
class. **Nothing in this repository detects that**, now or at P6a. It is
caught by reading the ADR or not at all, which is the reason for
deciding it here rather than deferring it to authoring time.

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

**ADR-002 Decision B's exemplar relations are stated over eight
undeclared types, and an earlier version of this section said three.**
Corrected 2026-08-04. *"Three"* came from a grep for a list already in
hand rather than from the signatures, and this ADR carried it verbatim —
the subject narrower than the claim, one document downstream.

**Derived rather than remembered**, by extracting every argument name
from every signature in `ADR-002` and checking each against the entity
table. **Five signatures, not the two quoted before:**

```
exposure(Asset, HazardEvent, Measure)                         :57
assignment(Asset, Incident, Agent, Interval)                  :58
partOf(Whole, Part, Interval)                                 :110
authority(Agent, Place, HazardType, Function, Interval)       :182
capability(Agent | Asset, CapabilityType, Level, Interval)    :193
```

**Thirteen argument types. Three are declared entities** — `Agent`,
`Asset`, `Place`. The other ten are **four different kinds of thing**,
and "declared" means something different for each. Collapsing them is
how an entity table becomes a type registry:

| Kind | Names | Declared by | State |
|---|---|---|---|
| **Subjects** | `HazardEvent`, `Incident` | the entity table | **the two the `[HUMAN]` finding named** — Part 1, deferred |
| **Structural primitives** | `Interval`, `Measure`, `Level` | a binding — OWL-Time, QUDT | **used, bound nowhere** |
| **Code-list references** | `HazardType`, `CapabilityType`, `Function` | a SKOS concept scheme, per ADR-000 D5 | **named, no scheme exists** |
| **Role variables** | `Whole`, `Part` | nothing — they range over any entity | correct as-is |

**So the entity core is not short by eight. It is short by two
subjects**, and three primitives and three code lists are used without
being bound anywhere. Different defects, different repairs. **The kernel
stays six.**

**`Interval` is the sharpest of them.** It appears in **four of the five
signatures**, nothing binds it — not an entity table, not an ADR, not
OWL-Time — and the temporal axis is discussed throughout
`docs/coverage.md`. `CapabilityType` is the other worth naming: ADR-002
Decision F already says it is a SKOS scheme and then never names one.

The section whose first line is *"Entities are declared once in Part 0"*
makes its forcing argument with subjects it never declares — and
quantifies four of its five relations over a type nothing binds.

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
