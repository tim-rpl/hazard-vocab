# Coverage matrix

What a real-time emergency management system needs, and where each
capability lives in this model.

This is the **comprehensiveness instrument**. It is neither a decision
record nor a claims register — it is a checklist that makes "are we
complete?" answerable rather than aspirational. It plays roughly the
role IEC 61968-1's interface reference model plays for CIM.

Rows are drawn from four sources: capabilities of electric-utility
control centres by analogy, ICS functional decomposition, the message
types in the EDXL and NIEM EM domains, and the four-phase
mitigation/preparedness/response/recovery lifecycle.

**Known method limitation.** A coverage matrix cannot find gaps its
row sources cannot see. The first three sources are all US-centric and
all response-oriented, which is exactly why the lifecycle phases were
invisible until a fourth source was added. Before claiming
completeness, enumerate rows from at least one further independent
frame — UN OCHA cluster functions, the EU Civil Protection Mechanism,
or the clause structure of ISO 22320 — and see what appears.

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
| Coverage / field-valued results | Contour and profile data | Part 0 (ISO 19123, CIS) | `partial` — primitive named, not modelled |
| Historical archive | Historian | Temporal axis + CAS versioning | `covered` |

> **The health gap is load-bearing.** Nothing currently distinguishes
> "PM2.5 is 0" from "the monitor is dark," or "no aircraft overhead"
> from "the ADS-B feed failed over twice and the third tier is stale."
> A three-tier fallback chain is invisible to the model. Absent must
> not read as zero.

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
| Cost tracking | Financial systems | — | `out of scope` |
| After-action / lessons | — | — | `out of scope` |


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

## Open scope question

Several rows above are arguably *services* rather than *information
model* — routing, alarm suppression, plan execution tracking. Under
RM-ODP these belong to the computational viewpoint, not the information
viewpoint, and CIM keeps the same separation (61970-301 versus
61968-100).

The model does not currently declare where that line falls. Until it
does, these rows will keep oscillating between `GAP` and `out of
scope`. Worth an ADR.
