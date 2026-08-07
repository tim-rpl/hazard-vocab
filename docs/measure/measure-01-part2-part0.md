# Measure 01 — Part 2 (Observation) + the Part 0 fragment it depends on

**Stage:** measure · **Status:** closed, `pass-with-findings`
**Opened:** 2026-08-01 · **Closed:** 2026-08-01

**Unit of work measured**

> Part 2 (Observation) plus the Part 0 identity and entity fragment it
> depends on, bound to external vocabularies, generating SHACL,
> validated against captured AirNow and Open-Meteo payloads.

**Review record.** Falsified by O across two rounds — a `blocked`
verdict (F1–F9, S1–S11, two rulings) and a `pass-with-findings` block
verification (F10–F12). Gate messages, verdicts and the block response
live in `review-inbox.md` and its archive. **This document is the
measurement; the inbox is the channel.**

**Amendment history.** Three in-place amendments before O's first
reply, all corrections to H's own work by the same method — fetch and
grep, or run the tool:

| # | What it corrected |
|---|---|
| 1 | A 200 on a slash-namespace URI proves nothing. Falsified three of H's own bindings. |
| 2 | Owner hypotheses verified. Two "write" entries had standard terms. |
| 3 | The CIM Object Registry profile read in full. Two adopted classes translate away. |

**Superseded, 2026-08-06 — not edited below.** Two statements in this
document's body are now false. **They are named, not located** — the
first version of this note carried three line numbers and **all three
were stale by exactly the note's own length**, because inserting 22
lines shifted the body it pointed at. A note whose stated purpose is to
stop a reader being sent somewhere wrong, sending them somewhere wrong.
F4 deleted three prose line-pointers for this reason; this is the same
class, and the remedy is the same. **Name the statement.**

**1. The sentence beginning *"`vocab/core/vocabulary.yaml` and
`vocab/prefixes.yaml` remain absent"*** — in the artifacts paragraph.
Both halves have changed. The prefix map is now
**`vocab/core/prefixes.yaml`** and it **exists**, written 2026-08-06;
`vocab/vocabulary.yaml` was never the path and `vocab/core/vocabulary.yaml`
is still absent.

**2. The sentence beginning *"1 — `vocab/prefixes.yaml` plus the 23
external"*** — in the sequencing paragraph. The path is corrected as
above, and *the 23 external* is a **retired figure**, superseded by
ADR-004's generated worklist with no count stated.

**Why the path moved, and it is a measurement:** `vocab/prefixes.yaml`
is scanned by nothing — `drift-lint.py` targets `vocab/core/`, C4's grep
targets core plus profiles — while `vocab/core/prefixes.yaml` is scanned
by all nine rules and falls inside invariant 2's scope. A prefix map no
instrument inspects is the thing claims.md C18 records.

**This is a closed document and its body stands as written.** The live
statements are restated in `docs/plan/items.yaml` and the plan of
record.

Later corrections: **A40** withdrawn (the tool it denied now exists),
**A1** restated (nine items plus a non-slot, now ten numbered),
**A36** narrowed and **A39** corrected — both self-falsifications found
without `design/` access.

**Load-bearing results, most stable first**

1. **A16 / S9** — one AirNow record carries three independent absence
   semantics, established by cross-tabulation, plus three in-band
   sentinel channels (`-999`, `'ND'`, `Elevation == 0` on 25% of rows).
2. **A34 / S3** — `gen-shacl` silently emits shapes contradicting the
   ontology being bound. Exit 0, no warning. Recorded as C17 axis 2.
3. **A30 / S1 / PA10** — the CIM namespace does not dereference, and
   per the project owner this is general to CIM. Copy-and-cite is
   settled, not contingent.
4. **A5** — under ADR-003 option A this unit is not executable as
   scoped. Survived its own falsifier under experiment.
5. **A27 / S6** — `sosa:Sensor ⊑ ssn:System`; `sosa:Platform` is not.
   The C7 conflict is real and narrower than first filed.

---


**Stage:** measure

**Artifacts:**
- `docs/coverage.md` — five `GAP` rows added (source verification status,
  provider-level fallback chains, observation validity conditioned on
  geometry, compliance/violation/enforcement, curated/testimonial
  content); the register added as row-source frame F5 with a note on
  what it surfaced that the first four could not; ranked gaps 16–20
  appended separately rather than interleaved into 1–15.
- `codelists/README.md` — the protective-action axis, and derived
  indices as a second authoring gap.
- No writes to `vocab/`, `codelists/*.ttl`, `transform/`, `build/`.
  `vocab/core/vocabulary.yaml` and `vocab/prefixes.yaml` remain absent
  and remain findings; not scaffolded.

**Claims touched:** L1, L2, L3, T1, C1, C3, C4, C5, C6, C7, C8, C10,
C11, C13, C15, C16, C17, C18

**Environment:** `make env` — python `.venv`, linkml 1.11.1, pyshacl
0.40.1, Lean 4.32.2, Alloy present, role `H`. `make lint` passes.
`make gen` / `make check` fail on the absent `vocabulary.yaml`, as
recorded. **This environment has outbound network access**, which the
reference implementation's does not; every probe cited below was run
here on 2026-08-01 and is re-runnable.

---

### Assertions

#### Surface

**A1.** Under ADR-003 **option A**, the unit requires **14 classes** and
**33 slots**, all of which must be authored locally as LinkML elements.
"Bind" never means import — it means a local element carrying an
external `class_uri` / `slot_uri`. **23 of the 33 slots carry an
external URI that is content-verified; 10 have no usable external term
and must be defined** — and `crs` may not be a slot at all, which would
make it 23 of 32.

*Count history, because it moved twice and both moves were corrections
to my own work:* filed as 22/11 → **21/12** by amendment 1 (three
bindings falsified by re-probe) → **23/10** by amendment 2 (two terms
found that I had wrongly filed as "write").

*Part 0 fragment (8 classes):* `Entity` (abstract), `Identifier`,
`Asset`, `Place`, `Agent`, `Activity`, `TemporalExtent`, `Geometry`.
*Part 2 (6 classes):* `Observation`, `ObservationCollection`, `Result`,
`ObservableProperty`, `Procedure`, `ResultQuality`.

**The 10 slots with no usable external term** *(restated at the block
response; the earlier enumeration listed nine plus a non-slot — see
BR-2)*:

1. `id`
2. `identifierValue`
3. `identifierScheme`
4. `issuingAuthority`
5. `assertedTime`
6. **`crs`**
7. `elevation`
8. `procedureKind`
9. `observingSystemStatus`
10. `sourceVerificationTier`

Items 2–5 are ADR-000 D3's alias tuple, superseded by ADR-001; ADMS is
the nearest external fit and is partial. **`crs` is item 6 and is in the
10** — that is what makes "23 of 32" arithmetically possible, since
dropping it can only take 33 to 32 if it was counted. Per A26 it is
**conditional**: GeoSPARQL carries the CRS inside the `wktLiteral`, so
`crs` may not be a slot at all, and if it is dropped the count is
**23 bind / 9 write of 32**. `elevation` (7) has no external term that
is *tight enough* — see **A26**. `procedureKind` (8) may not exist as a
distinct slot; ADR-003-dependent.

**`id`'s minting rule is not a slot** and was wrongly carried in the
enumeration. It is an open design question — what generates `id` for a
source that publishes no identifier (A10, Open-Meteo) — and it is
recorded as such, not counted.

*Moved to bind by amendment 2:* `resultQuality`, `absenceReason`.

*Enums to write:* `AbsenceReason`, `ObservingSystemStatus`,
`SourceVerificationTier`, `ProcedureKind` — 4 required by this unit.
`OperatingMode` (C12, CAP `status`) is a fifth that costs one slot and
is not required by these payloads.

**Falsifier:** name a class or slot in the list that no field of a
captured AirNow or Open-Meteo payload requires, or a payload field that
none of them can carry.

**A2.** **The three most expensive bindings are role-class mismatches in
SOSA, and they are expensive because they contradict C7 — not because
they fail to resolve.** `sosa:Sensor`, `sosa:Platform` and
`sosa:FeatureOfInterest` are named for roles, which is what ADR-002
Decision B and C7 forbid. ADR-002's own table binds `Asset` to *both*
`sosa:Platform` and `sosa:Sensor`; LinkML takes one `class_uri`, and
putting the other in `exact_mappings` asserts Platform ≡ Sensor, which
SOSA denies — it relates them by `sosa:hosts`. The forcing case is in
the first fixture: an AirNow **site** is a Platform and its **PM2.5
monitor** is a Sensor, and under role-not-subtype both are `Asset`.
`sosa:madeBySensor` has range `sosa:Sensor`, so a range of `Asset` is
incompatible under OWL and invisible under SHACL — which is invariant 4
doing real work rather than rhetorical work.

**Falsifier:** a `class_uri` / `mappings` assignment for `Asset` that
types both the site and the monitor and that `gen-owl` does not render
as an equivalence between `sosa:Platform` and `sosa:Sensor`.

**A2 — reasoning corrected by A28.** "SOSA denies it" was too strong:
there are **no disjointness axioms anywhere** in SOSA, SSN or SSN-ext,
so one individual may be typed both Platform and Sensor without
inconsistency. The conclusion survives on the narrower argument that
`exact_mappings` asserts *class equivalence* — every Platform a Sensor —
which is a different and false claim. See A27 for the `ssn:System`
workaround, which covers Sensor, Actuator and Sampler and **fails on
Platform**, and A29 for what SOSA's Sensor definition does to ADR-003.

**A3 — AMENDED 2026-08-01, in place, before O's reply. The original
assertion was over-claimed and its own re-probe falsified it. Both the
original and the correction are kept.**

**A3 as originally filed:** *"Every external slot URI in scope resolves
from here today"*, evidenced by HTTP 200 under `Accept: text/turtle`
for the SOSA, PROV, ORG, GeoSPARQL, QUDT and NVS2 P07 terms.

**Why that evidence was worthless for most of the list.** A slash
namespace serves the same document for every term under it:

```
GET http://www.w3.org/ns/sosa/hasSimpleResult      -> 200, 27326 bytes
GET http://www.w3.org/ns/sosa/thisTermDoesNotExist -> 200, 27326 bytes
byte-identical
```

**A 200 on such a URI proves the namespace document dereferences and
says nothing whatever about the term.** The correct check is to fetch
the graph and grep for the term; the bogus term appears 0 times in the
returned graph, `sosa:hasSimpleResult` once. Re-run under the correct
method, three of the originally claimed bindings fail:

| Term | Original claim | Re-probe | Reality |
|---|---|---|---|
| `qudt:unit` | binds | **404** under both accept types, 0 definitions in the QUDT schema graph | wrong URI — the property is **`qudt:hasUnit`** (200, 1 definition) |
| `sosa:resultQuality` | binds | **0 occurrences** in the SOSA graph | **does not exist in SOSA.** Moves to the write list, or binds outside SOSA to OMS `om:resultQuality` / ISO 19157 — a binding this pass has not measured |
| `sosa:ObservationCollection`, `sosa:hasMember` | binds | **0 occurrences** in the SOSA namespace document | URIs are correct and in the `sosa:` namespace, but they are **defined in `http://www.w3.org/ns/ssn/ext/`**, a different document. Dereferencing the term returns a graph that does not define it |

One further correction, in the other direction: my first GeoSPARQL grep
reported 0 for `geo:hasGeometry`, `geo:asWKT` and `geo:Geometry`. That
was a **grep defect, not a term absence** — the published document uses
prefix `gsp:`. All three are present. I am reporting it because a
false negative found by accident is evidence the method was loose in
both directions.

**A3 restated.** 21 external slot URIs are **content-verified** —
present in a fetched graph, not merely 200: 15 SOSA core terms
(`Observation`, `observedProperty`, `hasFeatureOfInterest`, `hasResult`,
`hasSimpleResult`, `resultTime`, `phenomenonTime`, `madeBySensor`,
`usedProcedure`, `isHostedBy`, `Sensor`, `Platform`,
`FeatureOfInterest`, `Procedure`, `ObservableProperty`), 2 in
`ssn/ext/`, 5 PROV, 1 ORG, 3 GeoSPARQL, 3 QUDT schema
(`hasUnit`, `numericValue`, `QuantityValue`), 6 QUDT units. The six
NVS2 P07 standard names returned 200 on **per-term paths**, which is
stronger than a namespace 200 but is still status-code-only — I did not
inspect those payloads and am not claiming I did.

The quantity-kind half of the original assertion stands and is
content-verified: `unit:MicroGM-PER-M3` has
`qudt:hasQuantityKind quantitykind:Density`, `unit:DEG_C` has
`quantitykind:BoilingPoint`. Quantity kinds are many-per-unit and
generic, so property must come from CF/P07 and unit from QUDT
independently — confirming ADR-000 D2.

**Falsifier:** fetch each graph and grep. The method that produced the
original claim cannot falsify anything, which is the finding.

**What this says about the rest of this message.** Every other assertion
resting on an HTTP status code alone is suspect by the same argument.
A12 (AirNow capturable) is not — it is evidenced by a returned feature
and a record count, not a 200. A4 was evidenced by absence-of-content
and is strengthened rather than weakened by this correction; see the
amendment appended to it.

**A4.** **US AQI has no external term on either axis.** No CF standard
name, no QUDT unit — `USAQI` is Open-Meteo's own string, and AirNow
publishes five index fields (`OZONE_AQI`, `PM25_AQI`, `PM10_AQI`,
`PM_AQI`, `OZONEPM_AQI`) with no URI behind any of them. An AQI is a
piecewise function of a quantity defined by regulation, not a quantity
and not a unit. It must be authored as a local SKOS scheme, and under
option A it is Part 3 content sitting in a Part 2 payload.

**Falsifier:** a resolving CF or QUDT URI for US AQI or any of its
sub-indices.

**A4 — evidence upgraded 2026-08-01.** Originally this rested partly on
reasoning ("an index defined by regulation is not a CF standard name").
It is now a searched negative, with a working control in each search:

- **CF / NVS2 P07**, whole collection fetched (1.75 MB):
  `air_quality|aqi|quality_index` → **0 matches**. Control: `pm2p5` →
  62 matches, so the fetch and the search both work.
- **QUDT unit vocabulary**, whole graph fetched (2.39 MB):
  `AirQuality|AQI` → **0 matches**.

Open-Meteo's own `hourly_units` reports `us_aqi` as `"USAQI"` — a
string that is not a unit — alongside `pm2_5` as `"μg/m³"`, in the same
response. The negative is now searched rather than assumed.

#### ADR-003 dependency — measured under option A

**A5.** **This unit as scoped is not executable under option A.** The
register classifies Open-Meteo Air Quality as "**Tiers 2 and 3 — model
and forecast**": a modelled value at an arbitrary point. Under A it
produces Part 3 instances, so "validated against captured AirNow and
Open-Meteo payloads" validates AirNow only, and the Open-Meteo half of
the fixture set has no Part 2 shape to validate against until Part 3
exists. Under B both validate against one shape. The scope of the first
unit of work therefore already presupposes B, or it silently drops half
its fixtures.

**Falsifier:** a Part 2 reading of the Open-Meteo air-quality response
that does not require a simulation-typed procedure. Cheapest form:
point at a response field that reports an instrument.

**A6.** **Even a single AirNow row is split by option A, and C17 makes
the split silent.** One feature carries `PM25` (measured — Part 2) and
`PM25_AQI` / `PM_AQI` / `OZONEPM_AQI` (derived indices — Part 3) in the
same record. Validating that fixture against Part-2-only shapes leaves
the index fields unmodelled; per C17, JSON-LD expansion discards keys
absent from the `@context`, so they vanish **with no violation raised**.
A + C17 = the derived half of every AirNow row silently disappears and
`make check` reports success.

**Falsifier:** `gen-shacl` a Part-2-only schema with `sh:closed true`,
expand a real AirNow feature under a context omitting the `*_AQI` keys,
and observe a violation.

**A7.** **The option-B delta for this unit is +2 named things now, and
what B removes is a future duplicate rather than any part of the present
surface.** Under B: one required `epistemicKind` slot, one closed enum,
one lint rule forbidding omission. **Nothing in the 14/33 collapses,
because Part 3 does not exist yet.** The number the design gate should
reason with is what A costs *later*: Part 3 authored under A re-declares
the observation shape — **6 classes and roughly 20 of the 33 slots** —
plus a permanent union query on every consumer, forever.

**This assertion has a real counter and O should press it:** if Part 3
under A shares a LinkML **mixin** with Part 2, the duplication falls to
near zero and A's entire cost reduces to the union query. Mixins are
invariant 5's stated preference, so that is the likely authoring. If so,
**the 6-classes/20-slots figure is wrong and the honest count is: A
costs one union query per consumer, B costs one slot and one enum.**

**Falsifier:** author Part 3 under A re-declaring fewer than 4 classes.
If a mixin does it, A7's headline number is falsified and the
parenthetical is the measurement.

#### Part 0 dependencies

**A8.** **Part 2 pulls in 8 Part 0 elements and can defer the rest.**
Pulls: `Entity` + the alias set, `Identifier`, `Asset`, `Place`,
`Agent`, `Activity`, `TemporalExtent`, `Geometry`. Defers: `Document`,
`authority(Agent, Place, HazardType, Function, Interval)`,
`capability(...)`, `Person`, and the CAS/versioning layer. Part 0 is the
largest part and this unit needs well under half of it.

**Falsifier:** an AirNow or Open-Meteo field that cannot be modelled
without a deferred element.

**A9.** **`partOf` is conditionally required, and the condition is a
modelling choice rather than a fact about the source — report as
ambiguity, do not resolve here.** An AirNow feature is one *site*
carrying up to three parameters (`OZONE` / `PM25` / `PM10`) with
per-parameter `_Measured` and `_Unit`, plus `MonitorType: Permanent`.
Modelling the individual monitors as distinct `Asset`s requires
`partOf(site, monitor, interval)` **and requires minting monitor
identities the feed does not publish** — invented identity, which is
exactly what `fixtures/README.md` forbids. Treating the site as the
sensor avoids `partOf` entirely and loses per-parameter capability
(`PM25_Measured`, which A16 shows is load-bearing). Worth ±1 session.

**Falsifier:** an AirNow field that identifies an individual monitor.

**A10.** **Open-Meteo carries no identifier of any kind, so
`authorityMatch` is not reflexive on its records — `Identity.lean`'s
partial-equivalence note is exercised by the first fixture pair.**
AirNow has `AQSID` (an EPA AQS site ID — jurisdiction-specific,
therefore profile content under D3 and C1). Open-Meteo returns a
coordinate, an elevation and a series, and nothing else; it also
**snaps the request** — 44.06 in, 44.100006 out — so the returned
coordinate is a model cell centre, not the point asked about, and
`sosa:hasFeatureOfInterest` would be pointing at a grid cell rather than
a place. Identity must be minted from (endpoint, coordinate, property,
time): a position-derived fallback, structurally identical to the
aircraft case in register category 08.

**Falsifier:** an identifier field in any Open-Meteo response.

#### L2 — which matching rule is implemented

**A11.** **The register names the rule, and it is `exactCellMatch`, not
`proximityMatch` — so L2 as filed does not describe the rule the
reference implementation uses.** Register category 01, WFIGS Fire
Perimeters: perimeter services are merged "then de-duplicated by **name
plus rounded centroid**." A rounded centroid is equality on a
projection, so the conjunction of two equalities is transitive, L2 is
**FALSE** for this rule, and the real defect is the boundary artifact
`Identity.lean` already names — two records of one fire 100 m apart
across a cell edge never match. Separately, register category 08 is
ADR-001 **option B** in production, as ADR-001 already records.

**This decides nothing.** It does not resolve ADR-001, and it does not
change L2's status: it says L2 is *unfalsifiable as filed* because it
does not name its relation. The evidence is one sentence of a
human-owned document describing a codebase that is not in this
repository.

**Falsifier:** the dedup implementation using a distance threshold
rather than a rounded cell. Cheapest form: read the dedup function —
which requires access this repository does not have, so the honest cost
is "unknowable from here; ~0 sessions given the source."

#### Fixtures

**A12.** **AirNow is capturable from this environment, which does not
make the register wrong.** Probed 2026-08-01: item
`2d718d2733a74d1689d72b922c0ac4f4` resolves to
`https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/Air%20Now%20Current%20Monitor%20Data%20Public/FeatureServer/0`;
`returnCountOnly=true` → **4446** features; `maxRecordCount` **10000**,
so the entire national set is one request. The register's "max 1000
records" is the *application's* cap, not the service's — which means the
reference implementation sees roughly 22% of national sites. The
register's `Documented` tier is correct **about its own environment**,
which blocks outbound access; per `fixtures/README.md` the tier is to be
recorded as *observed-here*, not silently upgraded in the register,
which is human-owned.

Open-Meteo Air Quality and Forecast both return 200 here and are
`Confirmed live` in the register; the GFS/HRRR endpoint is `Documented`
and was not probed (out of this unit's scope).

**Falsifier:** the same query failing from a clean environment.

**A13.** **Fixture volumes, by purpose.**
- *SHACL validation:* 1 AirNow national snapshot (4446 features, one
  request) + 1 Oregon subset (103 features) + 2 Open-Meteo AQ responses
  — **both response shapes**, because a single-coordinate request
  returns a JSON object and a multi-coordinate request returns an
  **array**, verified here. A fixture set covering only one shape
  validates a schema that the other breaks.
- *T1 confluence replay:* ≥24 consecutive hourly AirNow snapshots. The
  feed is hourly and arrival order is only testable across arrival
  times; one day is the minimum window that contains a supersession.
- *C3 arity:* one week = 168 snapshots ≈ 750k features before
  canonicalisation. The only item here with a real storage cost, and the
  cheaper order is to run the arity distribution on one day first and
  see whether it has stabilised.

**Falsifier:** an arity distribution that stabilises inside one day,
which makes the week unnecessary.

**A14.** **`make check` cannot validate a captured payload today, and
the missing step is the one C17 already falsified.** `check` globs
`fixtures/**/*.jsonld`; every capture is EsriJSON or Open-Meteo JSON,
and `fixtures/*/*.jsonld` currently matches nothing. **Nothing in the
Makefile converts one to the other**, so the conversion is a
hand-authored `@context` — and per C17 that context determines what
validation can see. The artifact `make check` validates is therefore a
*derivative* of the capture, and "capture, don't invent" is satisfied at
the capture layer while being defeated one layer down. (pyshacl does
accept multiple data-graph files — `--help`: "The file(s)" — so that is
not a defect; but it merges them into one graph, so fixtures sharing a
node IRI will interfere.)

**Falsifier:** a `make` target producing `.jsonld` from a raw capture
without a hand-written mapping.

**A15.** **Three register sources have no capturable payload, and none
of them blocks this unit.** GDELT, USA Structures and the wildfire
camera layer are `Unverified`. None is in Part 2's air/weather scope, so
the constraint lands on the *next* unit — USA Structures is the Part 4
exposure source. Not probed here, deliberately: probing it is next
unit's measurement. Record the absence; it is a fixture gap, not a
licence to synthesise.

**Falsifier:** a successful capture from any of the three.

#### Claims and gaps in scope

**A16.** **Gap #3 cannot be deferred, because a single AirNow record
carries three distinct absence semantics and the first fixture already
contains all three.** Measured on the Oregon subset, 103 sites,
`ValidTime` 2026-08-01T21:00Z:

| Field | Distribution | What it means |
|---|---|---|
| `Status` | 78 `Active`, 25 `Inactive` | the **site's lifecycle state** |
| `PM25_Measured` | 101 × `1`, 2 × `0` | whether the site **measures PM2.5 at all** |
| `PM25` | **32 null**, with `PM25_AQI_LABEL: "ND"`, `PM25_Unit: null` | **no datum this hour** |

So 101 sites are equipped for PM2.5 and 32 have no reading, and those
are different facts from the 25 that are `Inactive`. A single `absent`
flag collapses all three, and the collapse is lossy in the direction
that matters — "this monitor does not measure PM2.5" and "this monitor
measured nothing this hour" have opposite implications for whether to go
looking elsewhere.

Worse: `PM25_AQI_SORT` is **`-999`** on exactly those 32 rows. That is a
sentinel inside a numeric field. Modelled as a plain number slot it
validates cleanly and reads as an extreme negative AQI — C17's wrong
failure direction, in the first payload, with a concrete value.

This is C11's falsification restated with a count, and it is in the
first fixture rather than a future one.

**Falsifier:** a Part 2 schema with one absence slot that round-trips
all three states distinguishably.

**A17.** **C18's recall half becomes exercisable for the first time in
this unit.** `make lint`'s C1 pattern already includes `\bairnow\b` and
`\bepa\b`; the AirNow scheme, the `AQSID` field and the EPA AGOL org are
all legitimately *profile* content. So the first genuine recall test is
whether the lint fires when that content is misplaced into
`vocab/core/`. Until this unit produces content, every firing to date
has been a false positive — the rule has never been observed catching a
real violation.

**Falsifier:** put `AQSID` in a `vocab/core/*.yaml` and observe
`make lint` pass. Under 5 minutes; it is the cheapest experiment in this
message and it should be run before any core content is authored, not
after.

**A18.** **The unit touches 10 `asserted` claims and 4 `falsified` ones,
and the falsified ones are not equally survivable.** Asserted: L1, L2,
L3, T1, C1, C3, C4, C5, C6, C7. Falsified: **C11, C13, C15, C17** (and
C12, which is untouched but free).

- **C17 must be closed inside this unit, not around it.** It is the
  difference between "validated against captured payloads" meaning
  something and meaning nothing (A6, A14).
- **C11 must be closed** (A16).
- **C13 bites the T1 replay specifically.** AirNow republishes hourly. A
  *corrected* reading for hour N and the *new* reading for hour N+1 are
  currently indistinguishable, so a confluence test cannot separate a
  genuine order-dependence from a correction — T1 would fail for a
  reason that is not T1.
- **C15 and C12 are one slot each and free now.**

**Falsifier:** run the T1 replay across two AirNow snapshots containing
a republished `ValidTime` and show the diff is attributable without a
correction relation.

**A19.** **Gap collisions.** #3 — close now (A16). #2 (limits,
violations, alarms) — *touched but not closed*: OAR 437-002-1081
(35.5 µg/m³) and WAC 296-820 (20.5 µg/m³) are Part 3 / Part 6 content,
so this unit's obligation is only to make property and unit legible
enough that a threshold comparison is *checkable*, which is the whole of
the C5 restatement below. #1, #5, #9 — cheap; deferring is a choice, not
a necessity. Of the new rows, **#17 (source verification tier) is one
slot and belongs in this unit if it belongs anywhere**, because the tier
is a property of the fixture being validated.

#### Findings on files that are not mine

**A20.** **Two of the three READMEs named for correction were already
correct at HEAD.** Commit `3728437` applied the two-axes correction to
`vocab/profiles/README.md` and the verification-tier constraint to
`fixtures/README.md`. Only `codelists/README.md` needed the change, and
it was made. Reporting rather than re-writing.

**Falsifier:** `git show 3728437 -- vocab/profiles/README.md fixtures/README.md`

**A21.** **`README.md` (human-owned) is stale in four places, one of
which pre-decides an open ADR.**
1. It says weather and air quality "appear in Part 2 as observations and
   Part 3 as forecasts, **the same class with different procedures**" —
   which is **option B's semantics**, asserted in prose, while the parts
   table below it states option A's structure. The README already
   contradicts itself on the question ADR-003 exists to decide.
2. Part 5 is "Response — incidents, resources, assignments, missions".
   ADR-002 Decision E **rescoped Part 5 to Intent and Action**.
3. It places incidents in Part 5; `docs/coverage.md` places "Incident
   record and lifecycle" in Part 1.
4. Development says `make gen && make check`; neither passes.
   The licence is `TBD`, which CLAUDE.md treats as a commitment the
   README carries.

**Falsifier:** any of the four reading correctly against ADR-002,
`docs/coverage.md`, or a passing `make`.

#### Cost

**A22.** **5–7 sessions under option A with ADR-003 decided first;
7–9 if decided after.** 1 — `vocab/prefixes.yaml` plus the 23 external
bindings and 10 local terms. 2 — Part 0 fragment (8 classes, 13 slots).
1–2 — Part 2 (6 classes, 20 slots) and `gen-shacl`. 1 — capture, the
JSON-LD context, and repairing `make check`. 1 — the absence and health
model (A16), the only item carrying unresolved design content.

**The largest uncertainty is C17, not ADR-003.** ADR-003's cost is
bounded and now quantified (A7). C17 is unbounded: if closing it means
abandoning JSON-LD expansion as the validation path, the fixture
pipeline is redesigned and this estimate is wrong by an unknown amount
rather than by one session. Second uncertainty: `partOf` (A9), ±1.

**Falsifier:** a way to make expansion fail closed on unmapped keys that
costs less than one session. If one exists, A22's headline uncertainty
is wrong and ADR-003 reclaims the top slot.

---

### Amendment 2 — verification of owner hypotheses, 2026-08-01

The project owner supplied hypotheses about terms I had filed as
"write", explicitly as things to verify rather than accept. Every one
was checked by the amendment-1 method: fetch the graph, grep for the
term. **Nothing below was bound on say-so.** Two hypotheses were right
and change the counts; three were wrong or half-wrong; two things
neither of us anticipated turned up.

| # | Hypothesis | Verdict |
|---|---|---|
| H1 | `nilReason` is standardized and dereferenceable | **Confirmed, and larger than stated** |
| H2 | INSPIRE narrows it to Unpopulated/Unknown/Withheld | **Confirmed, but not at the codelist URI** |
| H3 | nilReason covers the three absence semantics | **2 of 3** — gap #3 narrows, survives |
| H4 | DQV is the current W3C answer for result quality | **Confirmed** |
| H5 | `resultQuality` exists in ISO 19156 / OMS | **Falsified as stated** — but the term exists elsewhere |
| H6 | Four vocabularies, four non-overlapping things | **Confirmed — and SSN says so in its own definition** |
| H7 | GeoSPARQL carries CRS inside the WKT literal | **Confirmed** (caveat on my source document) |
| H8 | `geo:altitude` is Basic Geo, and may be too loose | **Confirmed, and it is too loose** |
| H9 | `sosa:Sensor ⊑ ssn:System`, so `Asset → ssn:System` preserves C7 | **Half-confirmed. Sensor yes, Platform no** |

**A23 — `absenceReason` moves from write to bind, and the owner's
hypothesis understated the register.** `http://www.opengis.net/def/nil/OGC/0/`
serves **8** members, not the 6 named: `inapplicable`, `missing`,
`template`, `unknown`, `withheld`, `unpopulated`, **`AboveDetectionRange`**,
**`BelowDetectionRange`**. Content-verified on `unknown`, which returns a
real `skos:Concept` — `skos:prefLabel "Unknown"@en`, a definition ("The
correct value is not known to, or not computable by, the sender of this
data. However, the correct value probably exists"), `skos:inScheme
ogc:nil`, `skos:topConceptOf ogc:nil`. The other seven are 200 on
per-term register paths, which is stronger evidence than a slash
namespace but is not content-verification; I checked one in full, not
eight.

The two detection-range members matter here and neither of us predicted
them: an air-quality monitor below its detection limit is a real and
frequent case, and it is neither "missing" nor "zero" — which is C11's
exact subject.

**H2 confirmed with a trap.** `http://inspire.ec.europa.eu/codelist/VoidReasonValue`
returns an **HTML single-page-app shell** ("ShowVoc") under
`Accept: text/turtle` — the semantic URI is not content-negotiable. The
RDF is at `.../VoidReasonValue/VoidReasonValue.en.rdf`, which returns
13 087 bytes containing Unpopulated (9), Unknown (10), Withheld (8).
Anyone binding INSPIRE from the obvious URI gets an HTML page and a 200.

**H3 — nilReason covers 2 of the 3 absence semantics from A16, so
gap #3 narrows rather than closes.**

| A16 state | Covered by nilReason? |
|---|---|
| `PM25_Measured: 0` — the site does not measure PM2.5 | **Yes** — `inapplicable` |
| `PM25: null`, `"ND"` this hour | **Yes** — `unknown` or `missing` |
| `Status: Inactive` — 25 of 103 Oregon sites | **No** |

`Status: Inactive` is not a reason a *value* is absent. It is a state of
the **Asset over time**, true whether or not anyone asks for a reading,
and it is what makes "the monitor is dark" different from "this hour
has no datum." nilReason is a property of a missing value; observing-
system health is a property of a system. **`observingSystemStatus`
stays on the write list**, and gap #3 is now precisely bounded rather
than merely asserted: it is the system-state third, not all three.

**Falsifier:** an OGC nil member, or any dereferenceable code list
member, that means "the observing system is out of service."

**A24 — `resultQuality` moves from write to bind, but not to the term
the hypothesis named.**

The claim that OMS/ISO 19156 has it is **falsified as a binding**:
`http://www.opengis.net/ont/om` returns **288 bytes** — a Prez profile
stub (`prez:currentProfile profile:open-object`) — with **0**
occurrences of `resultQuality`. `http://def.isotc211.org/iso19156/2011/Observation`
**404s**. ISO 19156 may well define the concept in the specification;
it does not publish a dereferenceable RDF ontology at either URI, so
there is nothing to bind to. My original "does not exist in SOSA" was
correct and incomplete.

The term that does exist is **`ssn-system:qualityOfObservation`**,
which neither of us named:

> "Relation linking an Observation to the adjudged quality of the
> Result. This is complimentary to the SystemCapability information
> recorded for the Sensor that made the Observation."

Two caveats I am not smoothing over: it declares **no `rdfs:domain` and
no `rdfs:range`**, so it constrains nothing by itself and the range is
our choice (DQV is the obvious candidate); and it carries
`rdfs:isDefinedBy ssn:` while living in the `ssn-system` document — a
small inconsistency in the published graph.

**H4 confirmed:** DQV resolves with all probed terms present —
`QualityMeasurement`, `hasQualityMeasurement`, `inDimension`,
`Dimension`, `Metric`, `value`, `QualityAnnotation`,
`QualityCertificate`.

**A25 — H6 is confirmed, and SSN states the separation itself.** The
four-way split is not our inference: `ssn-system:qualityOfObservation`'s
own definition says it is *"complimentary to the SystemCapability
information recorded for the Sensor."* The standard draws the line the
hypothesis predicted.

| Vocabulary | Answers | Verified |
|---|---|---|
| `ssn-system` | what a **sensor is capable of** | all named terms present **except `DriftRate` — the actual term is `ssn-system:Drift`**. Also present and unnamed: `DetectionLimit`, `Selectivity`, `ResponseTime`, `SystemLifetime`, `BatteryLifetime`, `MaintenanceSchedule`, `OperatingPowerRange`, `SurvivalRange` |
| DQV | what a **particular result is worth** | 8/8 terms present |
| QUDT | **uncertainty on a value** | `standardUncertainty` and `relativeStandardUncertainty` both present |
| OGC nil | **why a value is absent** | 8 members (A23) |

**QUDT carries nothing for validity, fitness or verification tier —
confirmed by the AQI method.** Whole schema graph (115 706 bytes)
grepped: `validity` **0**, `verification` **0**, `nilReason` **0**,
`absent` **0**. `fitness` returns exactly **1** hit, which is the words
"FITNESS FOR A PARTICULAR PURPOSE" inside a UCUM licence disclaimer.
`sourceVerificationTier` stays on the write list with a searched
negative behind it.

**This separation belongs in an ADR** — four vocabularies, four
questions, and the failure mode is substituting one for another. Not
authoring it; flagging it for the design gate.

**A26 — the two geometry bindings, both hypotheses confirmed.**

*CRS.* No CRS property found in the GeoSPARQL graph; `gsp:asWKT` is
typed `gsp:wktLiteral`, described as "A Well-known Text serialization
of a Geometry object", and `gsp:Geometry`'s description locates the CRS
inside the position rather than beside it. So a separate `crs` slot is
**probably redundant**, and the real question — do we make consumers
parse literals? — is a design-gate decision, not a binding. **Caveat on
my own evidence:** the document served is a **Prez catalogue rendering**
(`prez:description`, `prez:label`), not the OWL ontology. It is OGC
describing its own terms, which is good evidence the terms exist and
weak evidence about their axioms. I did not obtain the ontology itself.

*Elevation — the hypothesis is right and the answer is no.* The
property is `geo:alt` in WGS84 Basic Geo (`wgs84_pos#`), and its own
change log defines it as *"decimal metres above local reference
ellipsoid."* That is **ellipsoidal height**. The register's
geopotential-height rule compares a site's elevation against the
geopotential height of the 925 hPa level to discard levels that are
underground — and geopotential height is referenced to the **geoid**,
not the ellipsoid. The two differ by the geoid undulation, on the order
of **tens of metres** in Oregon. Feeding an ellipsoidal height into that
comparison introduces an error of the same magnitude as the decision it
is making, in the one computation built specifically to stop the app
reporting an inversion from beneath the ground the user is standing on.

`geo:alt` is not tight enough. A datum-explicit term is required and I
have not found one. Separately: **AirNow publishes `Elevation` with no
stated datum** (e.g. 38.7 for Goose Bay), so the fixture cannot resolve
this either — it is an unknown in the source, not only in the
vocabulary.

**Falsifier:** a dereferenceable elevation property that names its
vertical datum, or evidence that geoid/ellipsoid separation is below
the resolution the pressure-level comparison needs.

**A27 — H9 is half-confirmed. `sosa:Sensor ⊑ ssn:System` holds;
`sosa:Platform` is not a `ssn:System`, and the AirNow site is a
Platform.**

Confirmed by axiom (`ssn.ttl:182`): `sosa:Sensor rdfs:subClassOf
ssn:System`. Same for `sosa:Actuator` and `sosa:Sampler`. So the
monitor half of the forcing case works exactly as hypothesised.

`sosa:Platform` has **no `rdfs:subClassOf ssn:System`**. Its only
axioms are restrictions — `hosts allValuesFrom ssn:System`,
`ssn:inDeployment allValuesFrom ssn:Deployment`. `ssn:System` carries
the mirror restriction, `isHostedBy allValuesFrom sosa:Platform`.
Platform and System are two branches related by hosting, not by
subsumption. **So `Asset → ssn:System` types the PM2.5 monitor and
fails to type the AirNow site**, which is precisely the entity C7
needs it to cover. The owner flagged low confidence on Platform and was
right to.

**There is an escape hatch, and it is an inference rather than an
assertion — O should weigh it as such.** SOSA's own definition:

> "A Platform is an entity that hosts other entities, particularly
> Sensors, Actuators, Samplers, **and other Platforms**."

But `sosa:hosts allValuesFrom ssn:System`. If a Platform hosts a
Platform, the hosted Platform is *inferred* to be a `ssn:System`. SOSA's
prose and its axioms therefore only reconcile if Platform and System
overlap — and **nothing forbids it**, which is A28. The hatch works, by
OWL inference, from an ambiguity in the standard. That is not a
foundation I would build on without saying out loud that it is one.

**Falsifier:** a `sosa:Platform rdfs:subClassOf ssn:System` axiom
anywhere in a published SSN graph, which would make the hatch an
assertion and H9 fully correct.

**A28 — unanticipated: there are no disjointness axioms anywhere in
SOSA, SSN or SSN-ext.** `grep -c disjoint` over all three graphs
returns **0**. This corrects A2's reasoning in my favour and against my
framing:

- **A2 said** SOSA "denies" Platform ≡ Sensor. That was too strong.
  Nothing in SOSA denies anything — one individual can be typed
  `sosa:Platform` and `sosa:Sensor` simultaneously with no
  inconsistency.
- **A2's conclusion survives on a different argument.** The problem was
  never co-typing an individual; it is that `exact_mappings` asserts
  **class equivalence**, which makes *every* Platform a Sensor and every
  Sensor a Platform. That is a much stronger and plainly false claim
  than "this AirNow site is both."

So the C7 / SOSA conflict is **softer than I filed it** and still real.
It is not an OWL contradiction. It is that SOSA segments by role at the
class level and C7 forbids exactly that, and the workaround (`ssn:System`
+ `hosts`) covers three of the four role classes and not the fourth.

Per the owner's instruction, I am not working around it: if C7 and SOSA
are genuinely incompatible on Platform, that is a more valuable finding
than a patch, and it needs its own ADR at the design gate.

**A29 — unanticipated, and it bears directly on ADR-003.** SOSA's own
definition of `sosa:Sensor`:

> "Device, agent (including humans), or **software (simulation)**
> involved in, or implementing, a Procedure."

SOSA classifies a simulation as a Sensor. That is the OMS position —
that a simulated result is an Observation with a simulation-typed
procedure — stated in the definition of the class we would bind `Asset`
to, in the standard ADR-003 says we are fighting.

**Reporting, not deciding.** ADR-003 remains open and this session does
not touch it. But it is evidence from the standard rather than from
reasoning, it was not in ADR-003 when it was written, and it points the
same way as ADR-003's own stated bar. O should decide whether it
belongs in the ADR before the design gate opens.

**Falsifier:** a SOSA or SSN axiom distinguishing simulation-implemented
Sensors from instrument Sensors. `ssn:implements → sosa:Procedure` is
the place to look, and it does not appear to make the distinction.

**Where the owner was wrong, stated plainly, since it was asked for:**
`DriftRate` is `Drift`; ISO 19156/OMS has no dereferenceable ontology to
bind `resultQuality` from; `sosa:Platform` is not a `ssn:System`; and
the INSPIRE codelist URI serves HTML. **Where the owner was right and I
was wrong:** `absenceReason` and `resultQuality` both had standard terms
and I had filed both as "write" — that is 2 of my 12 write-list entries
overturned, and the four-vocabulary separation was correct in full.

---

### Amendment 3 — ADR-001, the CIM Object Registry profile, and gate closure

Read: `design/ADR-001` (revised), and
`docs/reference/ObjectRegistry_Profile_Specification_v2.1.pdf` in full —
13 pages, all 8 tables, the class diagram, and Annex A sample data.
ADR-001's reading of the profile is **accurate on every point I
checked**, with two omissions noted at A36. Same method throughout:
fetch, grep, and where argument would not settle it, run the tool.

**A30 — Q1. The ENTSO-E namespace does not dereference. Content-verified
negative.** `http://entsoe.eu/ns/CIM/ObjectRegistry-EU/2.1` → **404**
under `text/turtle`, `application/rdf+xml` and `text/html`. The body is
**368 539 bytes of ENTSO-E website HTML**, and it is **byte-identical to
the response for `http://entsoe.eu/ns/CIM/completely/made/up/path`** — a
generic site 404, not a vocabulary. Grep of that body:
`IdentifiedObject` 0, `NamingAuthority` 0, `NameType` 0, `ObjectType` 0,
`Name` 2 (incidental HTML). The `https` variant and the trailing-slash
variant also 404; `http://iec.ch/TC57/CIM100` returns **403**.

The Version IRI in §2.1 of the PDF (line 85) matches what ADR-001
records, so the IRI is right and simply is not served.

**ADR-001's third row applies:** copy the structure, author locally,
cite the profile as normative precedent, record that the RDFS is held
locally with its provenance. A side effect worth having: the question of
whether an electricity-domain namespace is tolerable in a
jurisdiction-neutral core is now **moot**, because there is nothing to
bind. Invariant 2 is not tested by this decision after all.

*(The owner is re-checking ENTSO-E independently. This is what this
environment returned on 2026-08-01; if a served copy exists elsewhere,
that supersedes the measurement, not the method.)*

**A31 — Q2. Surface delta: literal transcription costs +4 classes and
+13 slots; the translate-don't-transcribe rule reclaims all of it.**

Transcribed literally, the profile is **5 root classes** (not four —
`IdentifiedObject`, `Name`, `NameType`, `NamingAuthority`, `ObjectType`),
**14 attributes and 6 association ends = 20 slots**.

Translated under ADR-001's own rule plus the two rulings at A37–A38:

| Profile element | Translates to | New classes | New slots |
|---|---|---|---|
| `IdentifiedObject` | our `Entity` — already counted | 0 | 0 (`mRID` → `id`) |
| `Name` | the `alias` relation, one class | **1** | 6 + `alias` on Entity = **7** |
| `NameType` | **SKOS code list** (A38) | 0 | 0 — slot already counted |
| `NamingAuthority` | **`Agent`** (A37) | 0 | 0 — slot already counted |
| `ObjectType` | one slot, if adopted at all (A34) | 0 | 0–1 |

Against what A1 filed from ADR-000 D3 (one `Identifier` class, 5 slots),
the corrected structure is **the same class count and +2 slots**, or +3
with `objectType`. **A1's totals move from 14 classes / 33 slots to
14 classes / 35–36 slots**, and one SKOS code list is added to
`codelists/`.

The measurement worth keeping is the **difference between the two
columns: 4 classes and 13 slots.** That is what ADR-001's
translate-don't-transcribe rule is worth on this one profile, and it is
the first number in this gate that quantifies a convention rather than
asserting one.

**Falsifier:** author the alias structure and find it needs a class per
profile element after all.

**A32 — Q3. Precedence attaches to `NameType`. T2 cannot protect it as
either is currently stated, so L4's hypothesis is unmet.** Three parts,
and the third is a negative result.

*Where it attaches.* `AliasKind` is a **type** distinction (does this
name designate, or uniquely designate), not a rank. Ordering its two
values is meaningless — a label does not establish identity at all, so
it is not low in the order, it is **outside** it. Precedence is an order
*between schemes*, and the scheme is `NameType`. The aircraft chain from
register category 08 — ICAO hex, then alternative ICAO, then
registration, then callsign — is an order over NameTypes, not over
kinds. **Attach to `NameType`.**

This composes with A38: an order over concepts in a SKOS scheme is
`skos:OrderedCollection` with an `rdf:List` of members. SKOS has the
construct natively; LinkML does not.

*The profile contributes nothing here.* I checked all 8 tables —
**no attribute anywhere in `Name`, `NameType`, or `NamingAuthority`
expresses rank or precedence.** The prior art settles the shape and is
silent on the order. This must be authored.

*T2 cannot protect it — three independent reasons.*

1. **The Alloy model cannot be asked the question.** `parts.als`
   represents constraints as `set Constraint` with `adds` / `drops`.
   An ordering is not a set. **Reordering drops nothing**, so
   `check_restrictionSound` and `check_compositionPreservesSoundness`
   are both silent on it — a profile could invert the base order and
   satisfy every existing assertion.
2. **SHACL Core cannot express prefix-extension.** "Profile order
   extends base order as a prefix" requires recursion over `rdf:List`.
   That is SHACL-SPARQL, and **invariant 4 admits only
   SHACL-expressible constraints into LinkML**. So either invariant 4
   bends or precedence lives outside the schema.
3. **Two total orders do not compose into a total order.** This is the
   one that bites hardest. `vocab/profiles/README.md` and `parts.als`
   commit to an instance being checked against the **composition** of a
   hazard profile and a jurisdiction profile. Composition is
   conjunction. The conjunction of two total orders over overlapping
   scheme sets is a **partial** order in general — incomparable pairs
   are exactly what it produces. **L4 says merge is a join only if
   conflict resolution is a total order.** So profile composition, as
   designed, can destroy the property L4 depends on.

**Conclusion: precedence is currently convention, not constraint, and
L4's hypothesis is unmet.** Not a defect in L4 — a gap between L4 and
the machinery meant to enforce it.

**Falsifier, and it is cheap:** add `order : seq Constraint` to
`parts.als` and assert that composing two add-only profiles preserves
the base order as a prefix. Alloy returns a counterexample in seconds
if I am right. **~0.5 session**, and it is the single cheapest
experiment added by this amendment.

**A33 — Q5, answered by experiment rather than argument: binding a
domain-less, range-less property costs nothing, because `gen-shacl`
never consults the external term.** Ran `gen-shacl` (linkml 1.11.1) on a
throwaway schema in the scratchpad — not in `vocab/` — with two slots:
one bound to `ssn-system:qualityOfObservation` (no domain, no range),
one to `sosa:observedProperty` (both declared).

Generated for the domain-less, range-less binding:

```
[ sh:class <.../ResultQuality> ;
  sh:maxCount 1 ; sh:minCount 1 ;
  sh:nodeKind sh:BlankNodeOrIRI ;
  sh:path ssn-system:qualityOfObservation ]
```

A fully constraining property shape. **`slot_uri` sets `sh:path` and
nothing else**; every constraint comes from our local `range`,
`required` and `multivalued`. So the answer to Q5 is: **it is bindable,
it costs nothing in validation power, and what it buys is a shared IRI
and no entailment.** Anyone reasoning over our data with SSN loaded
gains nothing from the term, because the term entails nothing.

**A34 — and the same experiment produced a finding larger than the
question. `make gen` silently emits shapes that contradict the ontology
we bind to.**

The control slot was declared `range: string` and bound to
`sosa:observedProperty`. `gen-shacl` emitted:

```
[ sh:datatype xsd:string ; sh:nodeKind sh:Literal ;
  sh:maxCount 1 ; sh:path sosa:observedProperty ]
```

But `sosa:observedProperty` declares `schema:rangeIncludes
sosa:ObservableProperty` (sosa.ttl:258), and SSN adds
`owl:allValuesFrom sosa:ObservableProperty` **and
`owl:cardinality 1`** (ssn.ttl:230–231). So the generated shape
**validates a string literal where the bound standard requires an
IRI-identified `ObservableProperty`**, and permits absence where SSN
requires exactly one.

**Exit code 0. No warning. Nothing in `make gen` or `make check` looks
at the external term at all.**

This is C17's failure direction on a second axis. C17 says validation
cannot see fields the context omits; this says validation cannot see
that our range **contradicts** the term we claim to bind. Every one of
the 23 bindings in A1 is exposed to it, and the error is invisible
precisely where a binding is wrong — which is the case the binding
exercise exists to catch.

**Falsifier:** a `make gen` or lint step that compares each `slot_uri`'s
declared range against the local `range` and fails on disagreement.
Estimated 0.5–1 session; needs the external graphs cached locally, which
A30 makes necessary anyway.

**A35 — Q4. `ObjectType` does not violate C7, and should still not be
adopted as-is. Ruling with the argument, since intuition is what
produced the conflict.**

*It passes C7's letter.* C7's falsifier is "any class in `vocab/core/`
named for a role, or any entity requiring a `sameAs` to itself under a
different role." `ObjectType` is not a role name — it is the name of a
*slot's* type, and the role appears as a **value**. No class is named
for a role and no `sameAs` is required. Passes.

*Three reasons it does not generalise, and the second is disqualifying.*

1. **It is a repair, not a design.** §3.6 is explicit: it carries the
   specialised type "when the instance object is serialised using a
   generalised class" — the profile's example is a Meter serialised as
   an `EndDevice`. It exists because CIM **does** subtype (Meter ⊑
   EndDevice) and a profile may serialise at the superclass. It is a
   lossy-serialisation repair for a subtyping model. We would be
   importing the repair without having the damage.
2. **`type` is `1..1` (Table 8). A single value cannot express
   simultaneous roles** — which is the entire case C7 exists for.
   ADR-002's forcing case is a fire station that is *both* a Part 4
   exposed element and a Part 5 resource. With `1..1` you pick one and
   are back to `sameAs` between two records: **C7's own falsifier,
   reintroduced through the slot.** For the narrow Platform/Sensor case
   the roles are arguably intrinsic and one value may suffice; for the
   roles ADR-002 was actually written about, it does not.
3. **`type` is `String`, unconstrained** (Table 8) — no code list, no
   enum. Adopting as-is imports free text where we would want a
   SKOS-bound value.

**Ruling: usable for the AirNow Platform/Sensor case specifically;
not a general answer to role-not-subtype.** If adopted it must be
adopted narrowly, with `0..*` cardinality and a bound value set — and
**both are divergences from the profile and must be recorded as such**,
not absorbed silently. Whether that narrow adoption is preferable to the
`ssn:System` + `hosts` route in A27 is a design-gate choice between two
imperfect options, and I am not making it.

**A36 — the profile contains the exact violation invariant 2 forbids,
and then deprecates it. This is the strongest evidence in the document
and ADR-001 omits it.**

`IdentifiedObject` (Table 1) carries **six** attributes, not the four
ADR-001 lists. The two omitted are:

- `energyIdentCodeEic` 0..1 — *"(deprecated, European) ... the EIC code
  (Energy Identification Code) ... For details on EIC scheme please
  refer to ENTSO-E web site."*
- `shortName` 0..1 — *"(deprecated, European)"*

Both carry the **«European» stereotype** in the class diagram.

**A36 — NARROWED at the block response (human finding H1). The original
wording overclaimed and the corrected version is better evidence.**

I wrote that "a standards body did it the wrong way." That is wrong in a
way that matters. The «European» stereotype means these are **ENTSO-E
regional extensions, not canonical CIM** — the base IEC 61970
`IdentifiedObject` does not carry them. So the finding is not about a
standards body polluting a core class; it is about **a regional profile
injecting jurisdiction-specific attributes onto a shared root class,
discovering that was a mistake, and deprecating them in favour of the
generic mechanism** (Table 1: `aliasName` "is planned for retirement",
recommending "replace aliasName with the Name class").

That is narrower and more useful. It is evidence about the
**regional-extension failure mode** — which is precisely the failure
`vocab/profiles/` exists to prevent, and precisely the boundary
invariant 2 draws. A profile that reaches up into the core is the thing
being guarded against, and here is a mature standards process doing it
and then reversing.

The same pattern appears in the metadata rules:
R:CSA:ALL:wasAttributedTo:usage says `prov:wasAttributedTo` "should
normally be the 'X' EIC code of the actor" (line 208) — a regional
scheme named inside an otherwise generic provenance rule.

**Cite; do not adopt.** Proposed for C1's entry as supporting evidence
for the discipline — not as evidence about C1's truth over our own
files, which only inspecting our own files can supply.

**A37 — Tension 1 resolved. `NamingAuthority` is a role class; C7 is not
narrower than stated; the adoption should translate it to `Agent`.**

The profile settles this against itself. §3.5: *"Authority responsible
for creation and management of names of a given name type and/or name;
**typically an organization or an enterprise system**."* Its complete
attribute set (Table 7) is `name` 1..1, `description` 0..1, `mRID` 1..1
— **nothing specific to being a naming authority.** It is an
organization, described by what it does. Annex A confirms it:
`<cim:NamingAuthority.name>LIO</cim:NamingAuthority.name>` — an
organisation code.

So `NamingAuthority` is the same UML artifact ADR-001 already diagnosed
one level down. UML cannot say "this Agent appears here in the
naming-authority role", so it makes a class — exactly as UML could not
say "this relation has a kind" and made two association ends.
**ADR-001's own translate-don't-transcribe rule resolves the tension it
raised**, applied one level up: `Agent` fills the authority position in
the `alias` relation.

C7 survives unmodified. −1 class.

**A38 — Tension 2 resolved. `NameType` is a code list wearing a class.
D5 holds; part of the adoption is redundant.**

Four pieces of evidence:

1. **Its content is a SKOS concept's content.** Table 5: `name` 1..1,
   `description` 0..1, `mRID` 1..1. Identity plus label plus
   definition, nothing else.
2. **§3.4 describes a controlled vocabulary in as many words:** *"Type
   of name. Possible values for attribute 'name' are implementation
   dependent but **standard profiles may specify types**."* Values
   governed at profile level is the definition of a code list, and it
   is where `vocab/profiles/` already puts scheme declarations.
3. **The sample instance is a scheme identifier:** Annex A,
   `<cim:NameType.name>EIC</cim:NameType.name>`.
4. **D5's stated reason applies exactly** — different change rate and
   governance from structure. Adding a naming scheme should not bump the
   schema version, which is the whole argument for SKOS over inline
   enums.

**Residual, stated rather than smoothed:** `NameType` has an association
to `NamingAuthority` (Table 6), which plain SKOS does not model. That is
one property on the concept (`dct:publisher` or a local term), not a
reason to keep the class. And per A32 the precedence order lives here
too, as a `skos:OrderedCollection` — a second thing SKOS carries and a
LinkML enum cannot.

**Ruling: three classes plus a code list, not four classes.** −1 class,
+1 SKOS scheme. Both tensions resolve the same way and in D5's and C7's
favour, which is worth noticing: the adopted structure needed
translating twice, and ADR-001 had already written the rule that does it.

**A39 — Q6. Unresolved from primary source, but the profile changes what
turns on it.** The matching rule is still not determinable from this
repository — the reference implementation's source is not here, and
A11's evidence (the register's "de-duplicated by name plus rounded
centroid" = `exactCellMatch`) is unchanged.

What the profile adds is **normative rather than evidential**:
R:452:ALL:IdentifiedObject.name:rule (lines 162–169) states that `name`
"is not required to be unique", "must be a human readable identifier
without additional embedded information that would need to be parsed",
is "used for purposes such as User Interface and data exchange
debugging", and that **"the MRID ... is the only unique and persistent
identifier used for this data exchange."**

Under the adopted structure, therefore, **no name-based rule establishes
identity at all** — whichever rule is implemented, it can only propose.

**CORRECTED at the block response (human finding H2). The original
sentence contradicted A30 in the same message.** I wrote that this was
"option B, derived from the standard rather than from the aircraft
implementation, and stronger evidence because it is normative." A30 —
four assertions earlier — established that the ENTSO-E namespace **does
not dereference**. We are borrowing a shape, not conforming to a
standard, and **a standard we borrow from binds nothing.** Calling its
statement "normative" for us was exactly the internal inconsistency
FALSIFIER §5.2 now checks for.

Restated: the profile's rule about `name` and `mRID` is **prior art for
option B, not a decision** — it sits *alongside* the aircraft case
(register category 08) as evidence from a second mature system that
reached the same shape independently. Two independent instances of prior
art is a stronger position than one, and it is a different and weaker
claim than "the standard requires it." ADR-001 records it that way.

**It does not decide ADR-001 question 2** — B still has to be chosen
over A and C, and L2 still gates the reasoning. But the cost of getting
it wrong has dropped: the structure is neutral between the three, and
the profile independently rules out the thing option A does.

The honest caveat on the constraint as a lint rule: a *normaliser* does
not extract embedded information, it canonicalises for comparison. The
constraint is violated by the **input** — "Bedrock Fire" carries a type
token — rather than by the matcher. That is a weaker reading than
ADR-001 implies, and the rule is still worth adopting.

**Cost to settle definitively:** ~0 sessions given the reference source,
unknowable without it. Unchanged from A11.

**A40 — WITHDRAWN at the block response. See BR-1.** The assertion was
true when filed on 2026-08-01 and is false now: `make lint-selftest`
exists at `Makefile:50` and passes. Kept in place per the register
principle that deleting a failure destroys its value. Original text
follows.

**A40 (withdrawn) — `make lint-selftest` does not exist, so C18's recall
is still unexercised.** The fixtures landed and are well-formed:
`scripts/lint-fixtures/violating.yaml` encodes a role-named class, two
`exact_mappings` asserting the Platform ≡ Sensor equivalence from A2,
inline attributes and `is_a` depth 3; `clean.yaml` is the compliant
counterpart. But `grep -nE 'selftest|drift|lint-fixtures' Makefile`
returns **no match**, and the current `lint` target contains only the
C1 agency grep, the C4 construct grep and the vacuity rule — **none of
the four rules the fixtures exercise exists.**

The fixtures are a specification for rules not yet written. **C18's
recall half remains unexercised**, exactly as A17 filed it, and the
claim of demonstrated recall cannot be cited yet. Recording it because
a guard believed to be demonstrated is worse than one known to be
absent.

*(The owner is updating the Makefile. When the target lands, the
experiment is `make lint-selftest` and it takes seconds — which would
make it the first demonstrated-recall lint rule in the repository and
the cheapest experiment in this message. `Makefile` and `scripts/` are
human-owned; reporting, not editing.)*

---

### Amendment 3 — what the owner got right, and what they did not

**Right:** the profile reading is accurate throughout — the four-class
identity decomposition, the two association ends with the same range,
`NamingAuthority` as the correct class name against ADR-000 D3's
`NameTypeAuthority`, `Name` carrying no temporal attribute, the PROV-O /
Time / DCAT binding in §2.4, and the `IdentifiedObject.name` constraint.
Both tensions were real and both resolve.

**Not right, or incomplete:** `IdentifiedObject` has **six** attributes,
not four — and the two omitted are the most interesting content in the
document (A36). The profile has **five** root classes, not four.
`make lint-selftest` does not exist (A40). And the "translate, don't
transcribe" rule is load-bearing in two more places than ADR-001 applies
it — `NamingAuthority` and `NameType` (A37, A38) — which is the rule
working, not failing.

---

### Claims proposals (O's file — proposing, not editing)

**C5 — restate around the property-substitution defect.** Proposed:
*the canonical layer converts a class of silent property-substitution
errors into validation failures.* Grounding: register category 03
records that until build v84 Oregon's trigger ran on composite `us_aqi`
while Washington's ran on PM2.5, producing an impossible ordering — a
longer Oregon window than Washington's, when Washington's lower
threshold must always give the longer one. Both rules are PM2.5-specific
(35.5 and 20.5 µg/m³). With `observedProperty` bound to a CF/P07 concept
and `unit` bound to QUDT, comparing a `USAQI`-dimensioned index against
a µg/m³ threshold is a property-and-unit mismatch **SHACL can reject**.
This is the first candidate answer to C5 that is not an engineering
argument: it names a question ("is this comparison well-typed?") that
cannot be asked today. It is also narrower than C5 as filed and O should
check whether it is *too* narrow to satisfy the original.

**C10 — a candidate falsifier is now available; flagging as testable,
not deciding.** The register's category 10 is curated content: 27
burn-scar narratives, 10 year narratives, 15 century-scale fires,
governed by "researched and written, never invented," supplied by no
feed. It is arguably not observed, not modelled, not intended and not
mandated. The counter-reading is that it is an observation with a human
procedure — testimony — which SOSA's `sosa:Procedure` already covers and
which leaves C10 intact. **Both readings are live and this pass does not
choose.** Filed as a `docs/coverage.md` row (#20) that is `GAP` under
either reading. Cheapest test: take three burn-scar narratives and try
to write each as a Part 2 observation with a human procedure; if any
requires a slot that has no observational meaning, C10 falls.

**C11 — sharpen the evidence.** Current evidence cites
`docs/coverage.md`, which is our own file. Proposed replacement: the
product **already implements** absent-≠-zero — the register records that
an unparseable evacuation level is drawn grey and labelled
`LEVEL UNREADABLE` rather than dropped, that unknown structure occupancy
is drawn grey and never dropped, that an unknown air-quality contour
renders transparent rather than being guessed, and that emptiness is
never presented as safety. **The gap is not that the behaviour is
missing; it is that the vocabulary cannot express what the product
already enforces.** A16 supplies the count: three distinct absence
semantics and a `-999` sentinel in one record.

**C16 — the register is frame F5.** Under the reformulation already in
C16, the frame list gains a fifth entry, and it is the first that is
falsifiable by inspection rather than by reading a standard. Noted in
`docs/coverage.md`.

**C18 — the recall half has never been exercised.** Every firing of C1,
C4 and the vacuity rule to date has been a **false positive**, because
`vocab/core/` is empty and no violating theorem exists. No rule has been
observed catching a real violation. Proposed note for the entry: *a
guard that has only ever been wrong is not yet a guard* — and this unit
is the first that can test it (A17).

**L2 — not proposing a status change.** A11 is a measurement, not a
verdict: the register names the rule as name-plus-rounded-centroid,
which is `exactCellMatch`, for which L2 is false. But the register
describes a codebase this repository cannot read. Proposed only that the
entry record *which relation it is about*, since without that it is
unfalsifiable as filed.

**C1 — supporting evidence, from amendment 3.** C1 currently has no
evidence in either direction. A36 supplies some: the ENTSO-E Object
Registry profile carries `energyIdentCodeEic` and `shortName` as
«European»-tagged attributes on the root identity class, and deprecates
both in favour of the `Name` class. A standards body committed the
violation C1 forbids and then migrated to the structure C1 requires.
Evidence *for* the discipline, not for the claim's truth about our own
files — those are different things and only the second changes C1's
status.

**L4 — the hypothesis is unmet by the current machinery. Proposing a
new claim rather than a status change.** L4 says merge is a join iff
conflict resolution is a total order. A32 finds that nothing enforces
the order: `parts.als` models constraints as an unordered set so
reordering drops nothing; SHACL Core cannot express prefix-extension
over an `rdf:List`; and the conjunction of two total orders from two
composed profiles is a partial order in general. Proposed new claim,
entering as `asserted`:

> **T3 — profile composition preserves scheme precedence.** The
> composition of a hazard profile and a jurisdiction profile yields a
> total order over identifier schemes whenever each profile's own order
> is total and neither reorders the base.
>
> **Falsifier:** two add-only profiles whose composed order contains an
> incomparable pair. **Cheapest test:** add `order : seq Constraint` to
> `design/alloy/parts.als` and check it. Alloy returns a counterexample
> in seconds if the claim is false. ~0.5 session.

Filed this way because L4 is not wrong — it states a condition, and the
finding is that nothing establishes the condition. Deleting or weakening
L4 would hide that. T3 makes the gap falsifiable on its own terms, and
it is the highest-value cheap experiment this gate produced.

**C17 — a second axis, proposed as an addition to the existing entry
rather than a new claim.** C17 records that JSON-LD expansion silently
discards keys absent from the `@context`. A34 finds a second silent
failure in the same direction: `gen-shacl` emits shapes from our local
`range` without ever consulting the `slot_uri` it binds, so a local
range that **contradicts** the external term's declared range produces a
passing shape with exit code 0 and no warning — demonstrated with
`sosa:observedProperty`, whose range is `sosa:ObservableProperty` and
for which a `range: string` declaration generated
`sh:datatype xsd:string`. Both axes fail toward "pass". Proposed as
evidence on C17 because the consequence is identical and splitting it
would obscure that.

**C18 — the demonstrated-recall claim is not yet available.** A40: the
lint fixtures landed but `make lint-selftest` does not exist and none of
the four rules they exercise is in the `lint` target. C18's note stands
unchanged — every firing to date is still a false positive.

---

**What would falsify each:** stated inline under each assertion above,
in the form the protocol requires. The three cheapest, in order:
**A17** (under 5 minutes, and it should be run before core content
exists rather than after), **A3** (re-run the URI probes),
**A12** (one HTTP request).

**Requesting:** falsification of A1–A40, and rulings on two things:

1. Whether **A5** — that the first unit of work as scoped presupposes
   ADR-003 option B — is a measurement or an attempt to decide the ADR.
   If the latter, strike A5 and rescope the unit to AirNow only.
2. Whether **A29** — SOSA defining a Sensor as including "software
   (simulation)" — belongs in ADR-003 before the design gate opens. It
   is evidence from the standard, it postdates the ADR's drafting, and
   it points the same way as the ADR's own stated bar. I am reporting
   it and not acting on it.

**Three amendments have been made in place, before any O reply**, as the
protocol permits. All three were produced by the same method — fetch,
grep, or run the tool — rather than by argument, and all three corrected
me:

- **Amendment 1 (A3, A4)** — a 200 on a slash-namespace URI proves
  nothing; `sosa:hasSimpleResult` and a term I invented return
  byte-identical documents. Re-probing by grep falsified three of my
  own bindings.
- **Amendment 2 (A23–A29)** — verification of owner hypotheses. Two of
  my "write" entries had standard terms; three hypotheses were wrong or
  half-wrong; two findings (A28 no-disjointness, A29
  simulation-as-Sensor) were anticipated by neither of us.
- **Amendment 3 (A30–A40)** — the CIM Object Registry profile, read in
  full. The namespace does not dereference (A30). Two adopted classes
  translate away (A37, A38). And the experiment run to answer a narrow
  question about SHACL produced a larger finding than the question
  (A34).

**Gate closed. This message stops moving here.** Anything still open is
filed as a stated ambiguity with an estimate, which is what the measure
stage is for: `partOf` (A9, ±1 session), the matching rule (A39,
unknowable without the reference source), `ObjectType` versus
`ssn:System` for the Platform case (A27/A35, a design-gate choice
between two imperfect options), and ADR-001 question 2 (gated on L2).

**Stability ranking, so O can spend its effort well.** Most stable:
**A16**, the three absence semantics and the `-999` sentinel — from a
returned payload, re-runnable in one request, and unchanged across all
three amendments. Least stable: **the bind/write count**, which moved
22/11 → 21/12 → 23/10 → 14 classes / 35–36 slots across three
amendments, every move a correction to my own arithmetic or my own
method.

**The three cheapest experiments this gate produced**, in order:
**A40** — `make lint-selftest` once the target exists; seconds, and it
is the first demonstrated recall in the repository.
**T3 / A32** — `order : seq Constraint` in `parts.als`; ~0.5 session,
and it tests whether L4's precondition is enforceable at all.
**A17** — put `AQSID` in a `vocab/core/*.yaml` and watch `make lint`;
under 5 minutes, and it should be run before any core content exists
rather than after.

---
