# ADR-002 — Entity core and the modality axis

**Status:** proposed
**Date:** 2026-07-31

## Context

Parts 0–7 segment **statements** by epistemic kind. Nothing segmented
**subjects** — the things statements are about.

The symptom: agents appear three times and are defined nowhere (as
`prov:Agent` in Part 0 provenance, as issuing authority in Part 6, and
implicitly inside the empty Part 5). Assets are never named at all,
despite aircraft, sensors, and structures all being assets.

A second gap surfaced by analogy to electric-utility control centres:
of the four modalities an operational system distinguishes, we had
carefully separated only two.

## Decision A — Five abstract entities in Part 0

| Entity | Covers | Binds to |
|---|---|---|
| `Agent` | Person, Organization, Crew/Team, Automated System | `prov:Agent`, `org:Organization` |
| `Asset` | Equipment, vehicles, aircraft, sensors, facilities, infrastructure | `sosa:Platform`, `sosa:Sensor` |
| `Place` | Zones, jurisdictions, facilities, sampling locations | `sosa:FeatureOfInterest`, ISO 19112 |
| `Activity` | Observation acts, assignments, hazard events, warning issuances | `prov:Activity` |
| `Document` | IAPs, situation reports, delegation letters, orders as legal instruments | `prov:Entity`, `foaf:Document` |

`Statement` — the reified assertion with provenance — is the sixth, but
is already covered by the provenance layer and needs no new class.

## Decision B — Role, not subtype

Entities are declared once in Part 0. Parts 1–7 assign them **roles in
relations**. No entity is subtyped by the role it plays.

The forcing case: a fire station is both a Part 4 exposed element and a
Part 5 resource. So is a hospital, a bulldozer, an airbase. Under
subtyping it becomes two objects with a `sameAs` between them, and
reconciliation never ends. Under roles it is one `Asset` appearing in
two relations.

```
exposure(Asset, HazardEvent, Measure)            — Part 4
assignment(Asset, Incident, Agent, Interval)     — Part 5
```

Same for people: a person is not a "responder." A person *plays* a
responder role in an assignment, may play an evacuee role in a
protective action, and an observer role in a citizen report —
sometimes simultaneously.

Two consequences:

- **This is why the hypergraph projection is correct.** Roles live on
  incidences, not on nodes. The entity/role split is the reason
  hyperedges are the right downstream representation, and it produces
  per-incidence role data by construction.
- **It is the not-OO argument again.** Role-as-subtype is the classic
  OO failure (`FireStation extends Building implements Resource,
  ExposedElement`). Role-as-relation is what a declarative model does
  naturally.

## Decision C — One mereology primitive

```
partOf(Whole, Part, Interval)
```

Used three times: crews composed of personnel, incident complexes
absorbing fires, OMS sub-sampling and derived samples.

The interval is non-negotiable. Crews reconstitute, complexes absorb
and split, samples derive. `partOf` without temporal validity is wrong
in every one of those cases. Define once in Part 0 rather than three
times in three parts.

## Decision D — Person carries no required identifying attributes

Named individuals pull in PII, and the adjacent standards know it —
EDXL-TEP and HAVE are patient tracking.

`Person` exists in the core as an abstract entity with **no required
identifying attributes**. Identification is entirely profile content,
and a profile must be able to constrain `Person` to pseudonymous or
role-only. The core must remain usable with `Person` reduced to
"an agent that filled a position."

Grep-testable, like C1.

## Decision E — Four modalities, not two

Parts 2 and 3 separated *observed* from *modelled*. That is two of
four. The full set, with its control-centre analogue:

| Modality | Control centre | Emergency management | Home |
|---|---|---|---|
| **is** — observed | SCADA telemetry | Monitors, perimeters, positions | Part 2 |
| **will be** — modelled | State estimation, contingency analysis | Forecast, spread model, plume | Part 3 |
| **shall be** — intended | Switching plan, work order | IAP, resource order, closure order | Part 5 (rescoped) |
| **must be** — mandated | Operating agreement, interconnection | Jurisdiction, mutual aid, delegation | Part 0 (`authority`) |

Intent is not prediction. A switching plan is not a forecast of what
the network will do; it is a declaration of what an operator will make
it do. Collapsing intent into Part 3 is the same category error as
collapsing forecast into observation.

**Part 5 is rescoped** from "Response — resources and assignments" to
"Intent and Action" — plans, orders, assignments, and the actions taken
against them.

**Mandate becomes a Part 0 relation:**

```
authority(Agent, Place, HazardType, Function, Interval)
```

This single n-ary relation covers jurisdictional responsibility, mutual
aid compacts, unified command, and delegation of authority. It is
standing structure, not response action, which is why it belongs in the
core rather than in Part 5.

## Decision F — Capability as a relation

```
capability(Agent | Asset, CapabilityType, Level, Interval)
```

Covers crew qualifications, position codes, resource typing, and
aircraft capability class. Part 0. The `CapabilityType` filler is a
SKOS scheme; which scheme is profile content.

## Obligation

New claims for `claims.md`:

- **C7** — no entity is subtyped by a role it plays
- **C8** — `partOf` is the only mereology primitive; no part-whole
  relation is defined outside Part 0
- **C9** — no Part 0–7 element requires a natural-person identifier
- **C10** — the four modalities are exhaustive for operational
  emergency management

C10 is the weakest and most interesting. Candidate falsifiers: standing
constraints that are neither mandate nor plan (a burn ban is arguably
mandate; a road closure is arguably both), and counterfactual analysis
("what if the wind shifts") which is modelled but conditioned on an
intent that was not taken.

## Consequences

- Parts 4, 5, and 6 get **simpler** — they stop defining subjects and
  start defining roles over shared ones.
- Part 0 grows substantially and is now the largest part. Accept this;
  the entity core is genuinely foundational.
- Corrects an earlier error: aircraft was described as "Part 2, not
  Part 5." More precisely, the aircraft is a Part 0 `Asset`, its
  position is a Part 2 observation, and its dispatch is a Part 5
  assignment. Three statements about one entity.
- Does not resolve the gaps listed in `docs/coverage.md`. The entity
  core makes them expressible; it does not fill them.