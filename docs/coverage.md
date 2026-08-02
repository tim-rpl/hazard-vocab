# Coverage matrix

What a real-time emergency management system needs, and where each
capability lives in this model.

This is the **comprehensiveness instrument**. It is neither a decision
record nor a claims register — it is a checklist that makes "are we
complete?" answerable rather than aspirational. It plays roughly the
role IEC 61968-1's interface reference model plays for CIM.

Rows are drawn from five sources: capabilities of electric-utility
control centres by analogy, ICS functional decomposition, the message
types in the EDXL and NIEM EM domains, the four-phase
mitigation/preparedness/response/recovery lifecycle, and
`docs/sources/HDC-data-source-register.html` — the source register of a
running reference implementation.

**Known method limitation.** A coverage matrix cannot find gaps its
row sources cannot see. The first three sources are all US-centric and
all response-oriented, which is exactly why the lifecycle phases were
invisible until a fourth source was added. Before claiming
completeness, enumerate rows from at least one further independent
frame — UN OCHA cluster functions, the EU Civil Protection Mechanism,
or the clause structure of ISO 22320 — and see what appears.

**What the fifth source surfaced that the first four could not.** The
first four frames are *normative*: they enumerate what a system should
do. The register is *descriptive of one running implementation*, and
what it carries that no normative frame does is **the failure modes of
actual feeds** — a per-source verification tier, provider-level
fallback chains, a property-substitution defect found in production,
curated content that no feed supplies, and readings that are
structurally invalid at a location rather than merely uncertain. None
of these is a capability anyone sets out to build; each is something a
feed did. That is a different blindness from the response-orientation
that hid the lifecycle phases, and it is the reason the five rows below
marked *(register)* exist. Under the C16 reformulation this is frame
F5, and it is the first frame in the list that is falsifiable by
inspection rather than by reading a standard.

**Status values:** `covered` · `partial` · `GAP` · `out of scope`

Update this file when a part or entity changes. A `GAP` row is not a
defect — it is a known, named absence. An *unlisted* capability is the
defect.

---

## Observation and data acquisition

| Capability | Control-centre analogue | Home | Status |
|---|---|---|---|
| Telemetry ingest | SCADA point scanning | Part 2 | `covered` |
| Observation quality and validity | Measurement quality flags | Part 2 (`resultQuality`, ISO 19157) | `covered` |
| Sensor and platform description | RTU / IED inventory | Part 0 `Asset`, SOSA | `covered` |
| **Observing-system health** | `SvStatus`, out-of-service | — | **`GAP`** |
| **Source verification status** *(register)* | Source quality flag on a point | — | **`GAP`** |
| **Provider-level fallback chains** *(register)* | Primary / backup RTU path | — | **`GAP`** |
| **Observation validity conditioned on geometry** *(register)* | Point invalid for its location | — | **`GAP`** |
| Coverage / field-valued results | Contour and profile data | Part 0 (ISO 19123, CIS) | `partial` — primitive named, not modelled |
| Historical archive | Historian | Temporal axis + CAS versioning | `covered` |

> **The health gap is load-bearing.** Nothing currently distinguishes
> "PM2.5 is 0" from "the monitor is dark," or "no aircraft overhead"
> from "the ADS-B feed failed over twice and the third tier is stale."
> A three-tier fallback chain is invisible to the model. Absent must
> not read as zero.

> **Three different confidences, currently conflated into none.**
> *Source verification status* is **confidence in the source**: how
> thoroughly we have established that a publisher's endpoint returns
> what its documentation says it returns. It is carried per-source and
> is a property of *our knowledge of the publisher*, not of any reading.
>
> It is **not** observation quality (ISO 19157, `resultQuality`, a
> property of a datum) and **not** observing-system health (a runtime
> state of the monitor or feed). A reading of impeccable quality can
> arrive from a source nobody has ever confirmed answers; a
> thoroughly-verified source can return a bad datum. Nothing in the
> model carries any of the three, and collapsing them would be worse
> than carrying none.
>
> **The tier values are profile content, not core content.** The
> register's own vocabulary — confirmed-live / documented / unverified —
> is one implementation's encoding of the axis, calibrated to how *it*
> verifies. Another deployment reading national meteorological feeds
> will draw the tiers differently and may need more of them. What the
> core carries is the **axis and its distinctness from the other two**;
> the permissible values are a SKOS scheme a profile binds. Fixing the
> register's five badge names into the core would be invariant 2
> violated by vocabulary rather than by agency name.
>
> **Correction, 2026-08-01 (genericity sweep):** an earlier version of
> this row listed `Fallback` and `Sunsetting` as verification tiers.
> They are not — they are a **different axis**, and the register itself
> separates them, listing verification under `VERIFICATION` and these
> two under `OTHER`. *Fallback* is a source's position in an ordered
> chain (see the row below); *sunsetting* is a lifecycle state of the
> endpoint, orthogonal to how well it has been verified — a sunsetting
> source can be confirmed live, which is exactly the streamflow case.
> Three axes were collapsed into one by copying a legend rather than
> reading it. Recorded rather than silently fixed, because the error
> was mine and it is the failure mode this whole row is about.

> **Provider-level fallback is invisible to the consumer.** Where a
> capability is served by an **ordered set of interchangeable sources**,
> the identity of the source that actually answered — and its position
> in that order — is a fact about the datum, and it does not currently
> survive into anything a consumer can read. This is adjacent to the
> health gap and distinct from it: health says *the primary is down*;
> fallback position says *this value came from the third choice*. The
> two can disagree, and the second is the one a user needs to judge how
> much weight to put on the answer.
>
> Any multi-source deployment has this shape — redundant sensor
> networks, mirrored national feeds, a live service with a cached
> export behind it. The reference implementation supplies the
> discovered requirement (three ADS-B networks in a declared chain; one
> evacuation layer with two export fallbacks plus runtime-discovered
> local services), not the content.

> **Structurally invalid at a location is not poor quality.** An
> observation can be **inapplicable** where it is reported, as distinct
> from uncertain there. `resultQuality` cannot express this: the datum
> is not degraded, there is nothing for it to be a reading *of*.
>
> The discriminator is geometry — a spatial or vertical relation
> between the observation's own reference and the feature it is
> attributed to — which means validity is conditioned on a relation the
> model does not currently evaluate. The failure is silent, because an
> inapplicable value is numerically ordinary.
>
> Instances are not hazard-specific. A pressure level below ground at a
> high-elevation site (the reference implementation's inversion case: at
> ~1100 m the 925 hPa level is routinely underground); a tide gauge
> reading attributed inland of the coastline; a stream stage below the
> gauge datum; a soil-moisture probe reported above the surface. Each is
> the same shape in a different hazard domain, which is what makes it a
> core row rather than a wildfire one.

## Analysis and derivation

| Capability | Control-centre analogue | Home | Status |
|---|---|---|---|
| Gap filling / interpolation | State estimation | Part 3 | `covered` |
| Forecast | Load / generation forecast | Part 3 | `covered` |
| Derived indices | Calculated points | Part 3 | `covered` |
| **Limit and threshold definition** | `OperationalLimit` | — | **`GAP`** |
| **Violation detection** | Limit violation | — | **`GAP`** |
| **Alarm state, acknowledgement, suppression** | Alarm list | — | **`GAP`** |
| Uncertainty representation | — | Part 3 | `partial` — no mature standard |
| **Cascade / interdependency analysis** | Contingency analysis | — | **`GAP`** — requires network topology |

> **Limits and violations are most of what a control centre does.**
> This is where Part 3 (derive the violation) meets Part 6 (escalate to
> public warning), and therefore where the observed/modelled discipline
> gets its hardest test — an alarm is a *derived* fact presented with
> the urgency of an observed one.

## Incident

| Capability | Home | Status |
|---|---|---|
| Incident record and lifecycle | Part 1 | `covered` |
| Hazard classification | Part 1 (UNDRR HIP) | `covered` |
| Hazard intensity / magnitude | Part 1 (slot), profile (filler) | `covered` |
| Incident aggregation (complexes) | Part 0 `partOf` | `covered` (ADR-002) |
| Cascading hazards | Part 1 cascade relations | `partial` — named, not modelled |
| **Operational periods** | — | **`GAP`** — the primary temporal unit in ICS |
| Situation reporting | Part 5 (EDXL-SitRep) | `partial` |

## Agents, resources, and command

| Capability | Control-centre analogue | Home | Status |
|---|---|---|---|
| Personnel | Operator roster | Part 0 `Agent` | `covered` (ADR-002) |
| Crews and teams | Field crews (61968-6) | Part 0 `Agent` + `partOf` | `covered` (ADR-002) |
| Qualification / resource typing | Equipment rating | Part 0 `capability` | `covered` (ADR-002) |
| Resource inventory | Asset register (61968-4) | Part 0 `Asset` | `covered` (ADR-002) |
| Resource status | In-service / out-of-service | Part 5 | `partial` |
| Resource ordering | Work order | Part 5 (EDXL-RM) | `partial` |
| Assignment | Work task | Part 5 | `covered` |
| Span of control / org structure | — | Part 0 `partOf` over `Agent` | `partial` |
| Jurisdiction and authority | Operating agreement | Part 0 `authority` | `covered` (ADR-002) |
| Mutual aid | Interconnection agreement | Part 0 `authority` | `covered` (ADR-002) |

## Intent

| Capability | Control-centre analogue | Home | Status |
|---|---|---|---|
| Plans (IAP) | Switching plan | Part 5 | `partial` — modality named in ADR-002, not modelled |
| Orders (closure, burn ban) | Operating order | Part 5 / Part 6 | `partial` |
| Objectives and strategy | — | Part 5 | **`GAP`** |
| Plan-versus-actual | Plan execution tracking | Part 5 | **`GAP`** |
| **Compliance, violation, and enforcement** | Operating-order compliance | — | **`GAP`** |

> **A mandate can be violated; an observation cannot.** ADR-002
> Decision E imports the alethic/deontic split from SBVR, and SBVR is
> explicit that a deontic statement is not falsified by a
> counterexample the way an alethic one is: a closure order that
> someone drives past is still in force. The consequence was named in
> ADR-002 and never modelled. Nothing represents that an intended or
> mandated statement was complied with, violated, or enforced — which
> means the Part 0 `authority` relation and every Part 5 order are
> write-only. This is not the same row as plan-versus-actual:
> plan-versus-actual compares an intent to an outcome, compliance
> asserts a normative judgement about an agent's conduct against a
> mandate that remains in force either way.

## Exposure and impact

| Capability | Home | Status |
|---|---|---|
| Exposed elements | Part 4 | `covered` |
| Vulnerability | Part 4 | `covered` |
| Risk | Part 4 | `covered` |
| Population | Part 4 | `covered` |
| **Damage assessment** | — | **`GAP`** — post-event observed impact, distinct from pre-event exposure |
| Loss estimation | Part 3 | `partial` |

## Warning and protective action

| Capability | Home | Status |
|---|---|---|
| Public alert | Part 6 (CAP 1.2) | `covered` |
| Alert distribution | Part 6 (EDXL-DE) | `covered` |
| Protective action zones | Part 6 | `covered` |
| Protective action levels | Part 6 | `partial` — **no standard vocabulary exists** |
| Shelter and mass care | Part 5 / Part 6 | **`GAP`** |
| Accessibility / vulnerable populations | Part 4 (ISO 22395) | `partial` |

## Context and networks

| Capability | Home | Status |
|---|---|---|
| Terrain, imagery, hydrography | Part 7 | `covered` |
| Transport networks | Part 7 (ISO 19148) | `covered` |
| **Route analysis / evacuation routing** | Part 7 | **`GAP`** |
| Land cover and fuels | Part 7 (ISO 19144) | `covered` |
| **Infrastructure topology** | — | **`GAP`** — prerequisite for cascade analysis |
| Administrative units | Part 7 | `covered` |

## Record and accountability

| Capability | Control-centre analogue | Home | Status |
|---|---|---|---|
| Provenance | — | Part 0 (PROV-O) | `covered` |
| Audit trail | `ActivityRecord` | Part 0 `Activity` + CAS versioning | `covered` |
| Documents | `Document` | Part 0 `Document` | `covered` (ADR-002) |
| **Curated / testimonial content** *(register)* | Operator standing notes | — | **`GAP`** — pending C10 |
| Cost tracking | Financial systems | — | `out of scope` |
| After-action / lessons | — | — | `out of scope` |

> **Curated content is a candidate fifth modality, and therefore a
> candidate C10 falsifier.** The shape is **expert-authored interpretive
> content that no feed supplies and no computation produces**, governed
> by an editorial rule rather than by a schema, and deliberately held
> apart from application logic so a subject-matter expert can maintain
> it. Every hazard domain has some: what happened on this ground before,
> which is the character of this season, what a place is like to reach.
> The reference implementation's instance is 27 burn-scar narratives, 10
> year narratives, 15 century-scale landmark fires and a set of named
> landscapes, governed by "researched and written, never invented" — the
> feeds supply what is happening, that file supplies what it means.
>
> It is not observed (nobody measured it), not modelled (nothing
> computed it), not intended (it declares nothing anyone will do), and
> not mandated (it obliges nobody). If that reading survives, C10 is
> falsified by a case that already exists in production. The
> counter-reading is that a burn-scar narrative is an *observation with
> a human procedure* — testimony — in which case SOSA's
> `sosa:Procedure` already covers it and C10 survives. **Do not settle
> this here.** The row is `GAP` either way, because nothing in the
> model can currently hold the content; the C10 decision only
> determines whether it lands in Part 2 or forces a fifth modality.


## Operating mode and record integrity

*(added by falsification pass, 2026-07-31)*

| Capability | Control-centre analogue | Home | Status |
|---|---|---|---|
| **Exercise / test / live discriminator** | Dispatcher training simulator mode | — | **`GAP`** |
| **Correction versus supersession** | Bad telemetry versus changed state | — | **`GAP`** |
| Retraction / cancellation | — | Part 6 (CAP `msgType`) | `partial` |
| **Instance-level model version declaration** | — | — | **`GAP`** |
| **Instance-level profile conformance declaration** | — | — | **`GAP`** |
| Time zone / UTC offset requirement | Control room runs UTC | Part 0 (ISO 8601) | `partial` — not required |

> **Exercise mode is safety-critical and CAP already solves it.**
> `status: Actual | Exercise | System | Test | Draft`. Without this
> discriminator, exercise data can escape into live systems. This is the
> single most embarrassing omission found in the falsification pass
> because the fix is free.

> **Correction is not supersession.** Claim L5 says supersession, never
> deletion. But "the earlier fact was wrong" and "the world changed" are
> different statements with different downstream consequences, and the
> model cannot currently tell them apart. A republished perimeter and an
> amended 209 are corrections; a growing fire is supersession.

## Authority, sensitivity, and sharing

*(added by falsification pass, 2026-07-31)*

| Capability | Home | Status |
|---|---|---|
| **Emergency / disaster declaration** | — | **`GAP`** — the legal instrument that changes the `authority` relation |
| **Data sensitivity classification** | — | **`GAP`** |
| **Releasability and sharing restriction** | — | **`GAP`** — EDXL-DE carries distribution restrictions |
| **Tribal and sovereign data governance** | — | **`GAP`** |
| Multilingual warning content | Part 6 (CAP repeated `info` blocks) | **`GAP`** |
| Accessibility of warning content | Part 6 (ISO 22395) | `partial` |

> Sensitivity is an entire missing dimension, not a row. Every fact in
> the model implicitly assumes it is publishable. Opt-in address
> handling in a downstream product is a releasability decision the
> model has no way to express, let alone enforce.

## Lifecycle phases

*(added by falsification pass, 2026-07-31)*

| Phase | Coverage | Status |
|---|---|---|
| Mitigation | Fuels and land cover in Part 7; nothing else | **`GAP`** — treatments, buyouts, code enforcement, mitigation plans |
| Preparedness | Plans in Part 5; exercises absent | `partial` |
| Response | Parts 1-7 as built | `covered` |
| Recovery | — | **`GAP`** — damage assessment, assistance, debris, temporary housing |

> The matrix as originally built covered roughly one and a half of the
> four phases. This was invisible because all three row sources
> (control-centre analogy, ICS, EDXL/NIEM) are response-oriented.

---

## Gap summary, ranked

| # | Gap | Why it ranks here |
|---|---|---|
| 1 | Exercise/test/live discriminator | Safety-critical. Exercise data can escape into live systems. CAP solves it for free |
| 2 | Limits, violations, alarm state | Most of what an operational system does. Absent entirely |
| 3 | Observing-system health | Absent reads as zero. Actively misleading, not merely incomplete |
| 4 | Sensitivity and releasability | An entire missing dimension. Every fact implicitly assumes publishability |
| 5 | Correction versus supersession | L5 conflates two different statements |
| 6 | Operational periods | Primary temporal organizing unit in incident management |
| 7 | Declarations | The legal instrument that changes the `authority` relation |
| 8 | Intent modelling (plans, objectives, plan-vs-actual) | Modality identified in ADR-002 but unmodelled |
| 9 | Instance-level version and profile declaration | Cheap. Blocks nothing until the first breaking change, then blocks everything |
| 10 | Recovery and mitigation phases | Two of four lifecycle phases. Scope decision required, not necessarily a defect |
| 11 | Damage assessment | Distinct from exposure — observed post-event impact |
| 12 | Multilingual warning content | Legal requirement in many jurisdictions |
| 13 | Infrastructure topology and cascade | Large scope. Defer, but name the boundary |
| 14 | Protective action level vocabulary | No standard exists. Authoring opportunity, not adoption |
| 15 | Route analysis | Arguably a service, not a model concern. Decide explicitly |

Gaps 1–5 are the ones that would embarrass this model in front of
someone who has run a control room. Address them before adding hazard
types.

**Rows 16–20, added from frame F5 (the source register).** Ranked
provisionally and separately rather than interleaved into 1–15, so that
the earlier ranking is not silently rewritten. The relative placement
of these five against the existing fifteen is an assertion O should
falsify, not something this pass should assume.

| # | Gap | Why it ranks here |
|---|---|---|
| 16 | Compliance and violation | Every mandate and every order in the model is currently write-only. Named in ADR-002 and not modelled |
| 17 | Source verification status | Cheap to carry, and without it a `Documented` source and a `Confirmed live` one are indistinguishable downstream. Ranks below 16 only because it misleads more quietly |
| 18 | Provider-level fallback chains | Sits inside gap #3 operationally but is a distinct fact — *which tier answered*, not *is the primary up* |
| 19 | Observation validity conditioned on geometry | Narrow today (pressure levels below ground) but it is a validity kind `resultQuality` structurally cannot express |
| 20 | Curated / testimonial content | Blocked on C10. May be a Part 2 observation with a human procedure, may be a fifth modality. Ranks last because the decision is cheap and the content is not time-critical |

## Open scope question

Several rows above are arguably *services* rather than *information
model* — routing, alarm suppression, plan execution tracking. Under
RM-ODP these belong to the computational viewpoint, not the information
viewpoint, and CIM keeps the same separation (61970-301 versus
61968-100).

The model does not currently declare where that line falls. Until it
does, these rows will keep oscillating between `GAP` and `out of
scope`. Worth an ADR.
