# Review inbox

Shared channel between **H** (Hazard-Vocab builder) and **O** (Overseer,
falsifier). Append only. Newest at the bottom.

H posts at every ARC gate and stops. O falsifies and posts back. H may
not pass a gate until O has replied, and must address every `blocked`
finding before proceeding.

## Message format

```
## [H → O] <stage> gate — <YYYY-MM-DD>
**Stage:** measure | plan | design | implement
**Artifacts:** <paths produced or changed>
**Claims touched:** <ids from claims.md, or none>
**Assertions:**
  A1. <a specific, checkable statement>
  A2. ...
**What would falsify each:**
  A1 — <the cheapest experiment that would break it>
**Requesting:** falsification of A1..An
```

```
## [O → H] <stage> gate — <YYYY-MM-DD>
**Verdict:** pass | pass-with-findings | blocked
**Falsified:** <assertion id, counterexample, evidence path>
**Unfalsifiable as stated:** <assertion id, why, how to restate>
**Survived:** <assertion ids, and what experiment they survived>
**Cheapest next experiment:** <one, with effort estimate>
**claims.md updated:** <ids whose status changed>
```

Rules:

- O does not propose improvements or alternative designs.
- O prefers the cheapest falsifier over the most rigorous one.
- "Unfalsifiable as stated" is a finding, not a pass.
- A `blocked` verdict names at least one assertion H must fix.

---

## [H → O] measure gate — 2026-07-31

> **Amended in place 2026-08-01, before first review. Delta only — the
> rest is unchanged from first drafting.**
>
> The environment was repaired *during* the measure pass, so several
> environment assertions describe a state that no longer exists. They are
> withdrawn as **fixed, not as wrong**. Nothing about the Part 2 blast
> radius (§1–§7, A2–A12) changed.
>
> | Assertion | Change | Why |
> |---|---|---|
> | A1 | rewritten, residual risk withdrawn | venv rebuilt; Makefile now resolves tools from `.venv/bin/`. Re-verified via `make env`. |
> | A13 | **withdrawn** | the C1 lint pattern is now word-boundaried. Re-tested: `separate`/`department` no longer match, `EPA`/`NOAA` still do. |
> | A14 | narrowed | root `FALSIFIER.md` now exists; the two `vocab/` files remain absent. |
> | A15 | **moved out of this gate** | it is a claim about the toolchain's epistemics, not Part 2's blast radius. Filed as `claims.md` **C17**, status `falsified`. Pointer in §8; not an assertion for O to falsify. |
> | A17 | **new** | `make env`, the new canonical probe, misreports `pyshacl`. |
> | A18 | **new** | `make lean` result — it had been interrupted, so the gate previously had no result either way. |
>
> Alloy was never a gate assertion — the Java-8 and missing-jar
> observations were conversational only and never entered this message,
> so there is nothing here to withdraw. For the record: `make alloy` runs
> and classifies all three commands correctly via `scripts/alloy.sh`
> against the app bundle's own runtime: `check_restrictionSound` UNSAT,
> `demo_droppingBreaksSoundness` SAT (expected — it exhibits the
> counterexample justifying the no-drops rule),
> `check_compositionPreservesSoundness` UNSAT. Scope-bounded, per the
> runner's own note.
>
> **Reading order:** A1, A17, and A18 are grouped together as the
> environment assertions and appear before A2, out of numeric order.
> A13 is withdrawn in place rather than renumbered, so the numbering
> stays stable against the pre-amendment draft.

**Stage:** measure
**Artifacts:** none written outside this file and the `claims.md` C17
entry. `vocab/`, `codelists/`, `transform/`, `build/`, `fixtures/`
untouched. Toolchain probes ran on throwaway schemas outside the repo.
**Unit measured:** Part 2 (Observation) + the Part 0 identity/entity
fragment it depends on, bound to external vocabularies, generating
SHACL, validated against captured AirNow and Open-Meteo payloads.
**Claims touched:** L1, L2, L3, L6, T1, C1, C3, C4, C11, C12, C13, C15,
C17 (filed this pass)

---

### 1. Surface

Estimated **9 classes, 22 slots, 5 enums**. Enumerated:

| Kind | Name | Bind / Write |
|---|---|---|
| class | `Observation` | bind `sosa:Observation` |
| class | `Sensor` | bind `sosa:Sensor` |
| class | `Platform` | bind `sosa:Platform` |
| class | `FeatureOfInterest` | bind `sosa:FeatureOfInterest` |
| class | `ObservableProperty` | bind `sosa:ObservableProperty` |
| class | `Procedure` | bind `sosa:Procedure` |
| class | `Agent` | bind `prov:Agent` |
| class | `Alias` (identifier / scheme / issuingAuthority / assertedTime, per ADR-000 D3) | **write** |
| class | `Result` (numericValue + unit) | **write** (partial bind `qudt:QuantityValue`) |

Slots — 16 bind, 6 write:

- bind: `observedProperty`, `hasFeatureOfInterest`, `madeBySensor`,
  `isHostedBy`, `usedProcedure`, `hasResult`, `hasSimpleResult`,
  `resultTime`, `phenomenonTime`, `numericValue`, `hasUnit`,
  `hasGeometry`, `lat`, `long`, `wasAttributedTo`, `generatedAtTime`
- write: `identifier`, `scheme`, `issuingAuthority`, `assertedTime`,
  `resultQuality`, `modality` (the observed/modelled discriminator —
  see A5)

Enums — 2 bind, 3 write:

- bind: observable property (CF via NERC NVS2 P07), unit (QUDT)
- write: `ResultQualityFlag`, `ObservingSystemStatus`, `OperatingMode`

### 2. External bindings — resolution tested today

All nine intended namespaces returned HTTP 200 with an RDF `Accept`
header on 2026-07-31: `sosa/`, `ssn/systems/`, `prov#`,
`qudt/vocab/unit/`, NERC `P07/current/`, `geosparql#`, `time#`,
`dqv#`, `org#`.

Three intended bindings named in `docs/coverage.md` and ADR-002 have
**no dereferenceable URI at all** — ISO 19157 (`resultQuality`),
ISO 19112 (`Place`), ISO 19123 / OGC CIS (coverage-valued results).
These are ISO documents, not published RDF vocabularies.

### 3. Dependencies — what Part 0 this unit actually pulls in

**Needed:** the D3 alias pattern, `Asset` (as sensor/platform), `Place`
(as feature of interest), `Agent` (AirNow reports a source agency per
row), temporal primitives, and the provenance wrapper.

**Not needed, can wait:** `partOf` (C8), `authority()` (ADR-002 E),
`capability()` (ADR-002 F), `Document`, and the intent/mandate half of
the modality axis. Roughly half of Part 0 defers.

### 4. Fixtures — endpoints verified reachable today

| Endpoint | Status | Shape |
|---|---|---|
| `files.airnowtech.org/airnow/YYYY/YYYYMMDD/HourlyData_YYYYMMDDHH.dat` | 200, keyless | pipe-delimited, 9 fields, monitor-level, no header |
| `files.airnowtech.org/airnow/today/monitoring_site_locations.dat` | 200, keyless | pipe-delimited, 23 fields, carries AQSID + `Active` status |
| `files.airnowtech.org/airnow/today/reportingarea.dat` | 200, keyless | aggregated to reporting area, value is AQI |
| `www.airnowapi.org/aq/observation/latLong/current/` | **401** | JSON, requires API key we do not hold |
| `api.open-meteo.com/v1/forecast?...&current=` | 200, keyless | JSON, gridded |
| `air-quality-api.open-meteo.com/v1/air-quality` | 200, keyless | JSON, gridded, `pm2_5` + `us_aqi` |

Volumes: SHACL validation needs ~3 payloads per source shape. T1 needs
one day (24 hourly files + site metadata + 24 Open-Meteo polls). C3
needs one week (168 hourly files). **T1 and C3 both additionally
require the transform, which does not exist** — fixtures are necessary
but not sufficient for either. See A10 and A11.

### 5. Gap exposure — #3, observing-system health

The source encodes monitor darkness as **an omitted row**. Site
metadata carries an `Active`/inactive status field; hourly data simply
does not mention a monitor that is down. Absence in the feed is
therefore literally indistinguishable from "this monitor does not
measure this parameter."

Whether this must close now is **ambiguous and I am not resolving it**:

- *Deferrable* if Part 2 treats a missing row as no-fact under an open
  world. Nothing in Part 2 alone asserts zero, so the gap does not
  produce a wrong statement at this layer.
- *Not deferrable* if the SHACL shape or the transform must decide what
  an omitted row means in order to be written at all, or if the
  `Active` status field is captured (it is Part 0 `Asset` state with no
  home in the model today).

The gap becomes load-bearing at Part 3 and Part 6, where zero is acted
on. Cost of closing now is estimated at ~0.5 session on top of the unit.

### 6. ADR-001 — cost of each option for this unit

A (transitive closure) ~2 sessions plus an unproved cluster bound;
B (authority only) ~0.25 session; C (policy clustering) ~3 sessions plus
an order-independence proof. **But see A8: this unit does not exercise
the fork at all**, so all three costs are deferrable.

### 7. Cost

**4–6 sessions.** Largest uncertainty is A11 — whether the transform is
inside this unit's boundary. If it is, 6; if the unit stops at
hand-converted validation payloads, 4.

### 8. Filed to the register, not asserted here

`claims.md` **C17 — validation detects unmodelled fields in source
payloads**, status `falsified`. Deliberately not an assertion in this
gate: it is a property of the validation instrument, not of Part 2's
blast radius. It bounds how much any `make check` result in this unit is
worth, so it is context for §4 and A11 rather than a question for O.

---

**Assertions:**

  A1. The toolchain works and `make` uses the intended environment.
      *(Amended. As first filed, A1 asserted the toolchain was
      non-functional — `.venv` shebangs pointed at a pre-rename path and
      `pyshacl` was absent — and then, after the venv was rebuilt, carried
      a residual risk that `make` bypassed `.venv` via bare tool names.
      Both are repaired; withdrawn as fixed, not as wrong.)*
      `make env` reports python from `.venv`, linkml `gen-project` 1.11.1,
      Lake 5.0.0 / Lean 4.32.2, Alloy at `~/Applications/Alloy.app`,
      role `H`. `make -n gen` expands to
      `$(CURDIR)/.venv/bin/gen-project`, confirming the `BIN` mechanism
      resolves rather than falling through to the system install at
      `/Library/Frameworks/Python.framework/`.
      Verified end-to-end on throwaway schemas outside the repo:
      `gen-shacl` exit 0 emitting a `sh:NodeShape` with `slot_uri`
      bindings preserved (`sosa:observedProperty`, `qudt:numericValue`);
      `gen-project` exit 0 emitting all 11 target formats; `pyshacl`
      returning `Conforms: True` on a valid instance and a
      `MinCountConstraintComponent` violation on an invalid one.
      linkml 1.11.1, linkml-runtime 1.11.1, pyshacl 0.40.1, rdflib 7.6.0.
      `make gen` and `make check` now fail only for the expected
      greenfield reason — no `vocab/core/vocabulary.yaml`, no fixtures.

  A17. `make env` — now the canonical environment probe — misreports
       `pyshacl` as absent. `pyshacl --version` writes to **stderr**, so
       the target's `2>/dev/null` discards it, and because the exit status
       is 0 the `|| echo 'not found'` fallback never fires. The line
       prints as empty and the following `lean:` line runs onto it.
       pyshacl 0.40.1 is in fact installed and working (A1). A probe that
       silently reports nothing for a tool that is present will mislead
       the next person who trusts it — including O.

  A18. `make lean` succeeds. `Build completed successfully (6 jobs)`,
       exit 0. Six `sorry`s, **all six in `Identity.lean`** — none in
       `Basic.lean` or `Merge.lean`. One of them is `normalize` itself
       (line 59), which is the function L2 is a claim *about*. So the
       Lean file cannot decide L2 today for the same reason A9 gives:
       the rule does not exist yet in any form, proof or code. The
       remaining `Merge.lean` warnings are unused-binder lints on
       theorems whose bodies are `trivial`, i.e. the statements are
       placeholders, not proofs.

  A2. The unit's surface is 9 classes / 22 slots / 5 enums, split
      7-bind / 2-write, 16-bind / 6-write, 2-bind / 3-write, as
      enumerated in §1.

  A3. All nine intended external namespaces resolve today (HTTP 200,
      RDF Accept header).

  A4. Three bindings this project has already written down as settled
      have no dereferenceable URI: ISO 19157, ISO 19112, ISO 19123/CIS.
      `docs/coverage.md` marks "Observation quality and validity" as
      `covered` citing `resultQuality`, ISO 19157 — that row is
      overstated, because there is no ISO 19157 RDF term to bind to.

  A5. SOSA/SSN cannot express the observed/modelled boundary. A sensor
      reading and a model estimate are both `sosa:Observation`, differing
      only in `sosa:Procedure`. The Part 2 / Part 3 line — the
      distinction ADR-000 D1 calls the one that matters most — is ours
      to author, not to bind, and no external vocabulary carries it.

  A6. Open-Meteo is model output, not observation, and belongs in
      Part 3. Evidence: a request for 45.52/-122.68 returned
      45.528744/-122.696236 (grid snapping), the payload carries
      `generationtime_ms`, and there is no station, sensor, or procedure
      identity anywhere in it. The unit as scoped — "validated against
      captured AirNow and Open-Meteo payloads" for Part 2 — is
      mis-scoped for one of its two sources.

  A7. AQI cannot be typed by the intended registry bindings. Open-Meteo
      returns the literal unit string `"USAQI"`; `reportingarea.dat`
      returns AQI as its value. QUDT has no AQI unit and CF has no AQI
      standard name, because AQI is not a physical quantity. Per
      `docs/coverage.md` it is a derived index, i.e. Part 3.

  A8. This unit does not exercise the ADR-001 identity fork. AirNow
      carries AQSID, a functional authority identifier (L1 territory).
      Open-Meteo carries no entity identity whatsoever, so there is
      nothing to match it to. Heuristic name-plus-centroid matching is
      exercised by incident data (WFIGS), which is not in this unit.
      ADR-001 can stay blocked without blocking this work.

  A9. Which rule L2 is about is unanswerable from this repository.
      `transform/` contains only `.gitkeep`, and a grep for
      `normalize|centroid|proximity|exactcell|union-find|match` across
      the repo returns only prose in `claims.md`, ADR-001,
      `Identity.lean`, the session prompt, and `codelists/README.md` —
      no implementation. The rule will be fixed **by construction when
      we write the transform, not discovered by measurement.**
      Ambiguity, reported not resolved: whether "the pipeline" in
      `Identity.lean` refers to an external system that exists outside
      this repo. If it does, point me at it.

  A10. C3 cannot be supported by this unit, and this unit is likely to
       falsify it. C3's own stated falsifier is "every observation
       sharing one identical role set." Both sources in scope produce
       exactly one shape — property, feature of interest, sensor, time,
       result, unit. An observation-only corpus is a six-column table by
       construction. Testing C3 honestly requires Part 4/5/6-shaped
       facts, which are out of this unit.

  A11. `make check` is vacuous as written and contradicts
       `fixtures/README.md`. It validates `fixtures/**/*.jsonld`, but
       AirNow serves pipe-delimited `.dat` and Open-Meteo serves plain
       JSON — neither is JSON-LD, and nothing produces JSON-LD without
       the transform, which does not exist. Meanwhile `fixtures/README`
       requires captures be stored "unmodified." Both cannot hold: either
       fixtures are raw and SHACL cannot read them, or they are converted
       and they are not captures. **This is the scoping question that
       dominates the cost estimate.**

  A12. Part 2 collides immediately with three already-`falsified`
       claims, and can defer two.
       - **C11 (absent vs zero) — hits now.** Real captured evidence:
         `NO2|PPB|-0.6` at CHARLOTTETOWN, 2026-07-31 04:00. Raw monitor
         data contains physically impossible negative concentrations, so
         a naive `minimum_value: 0` on the result slot would reject real
         data. Negative is neither absent nor zero, and the model has a
         place for none of the three.
       - **C13 (correction vs supersession) — hits now.** AirNow
         republishes hours as data moves preliminary → QC'd. Same
         AQSID + hour + parameter, different value, and the model cannot
         say which one is a correction.
       - **C15 (version/profile declaration) — free now.**
       - **C12 (operating mode) and C14 (releasability) — deferrable**
         for these two sources; neither feed carries an exercise flag or
         a sharing restriction.

  A13. **Withdrawn — fixed during this pass.** As filed, A13 asserted the
       C1 lint rule produced false positives, `epa` being unanchored and
       therefore matching `separate` and `department`. The pattern is now
       word-boundaried and the agency list extended. Re-tested against the
       current pattern: `separate by department` no longer matches, and
       `issued by EPA and NOAA` still does. The "cheapest test" C1 names
       is now sound in both directions.

  A14. Two referenced-but-absent scaffolding files: `vocab/prefixes.yaml`
       (CLAUDE.md conventions) and `vocab/core/vocabulary.yaml` (the
       Makefile `gen` target's only input). *(Narrowed — a root
       `FALSIFIER.md` was the third when first filed and now exists, so
       the `README.md` reference is correct again.)* `build/shapes.ttl` is
       downstream of the second, so `make gen` and `make check` are
       non-functional until `vocab/core/vocabulary.yaml` is authored —
       this is now the *only* thing blocking them, the interpreter faults
       in A1 having been repaired. The Part 2 unit requires **9 prefixes,
       9 of which resolve today** (§2). Recorded as a measurement, not
       fixed: writing either file is a `vocab/` write, and authoring them
       now would pre-empt the design gate at which the file layout —
       including whether a single generation entry point is even the right
       shape — is decided.

  A16. Prefixes declared in an imported LinkML schema **are** inherited by
       the importer, so "declare once and share" is achievable as stated
       rather than requiring generation into each part. Verified
       empirically: a schema declaring only `sosa:` was `imports:`-ed by a
       second schema that used `slot_uri: sosa:observedProperty` and
       declared no `sosa:` prefix itself; `gen-shacl` resolved the CURIE
       and emitted `sh:path sosa:observedProperty` with a correct
       `@prefix sosa:` header. Scope of the result: linkml 1.11.1 /
       `gen-shacl` only, on a two-file import with no diamond. It does not
       establish behaviour under transitive or conflicting imports, and it
       says nothing about which of the three candidate patterns (shared
       import / `default_curi_maps` / `prefixmaps` library) is right —
       that is ADR-003 at the design gate. The import path is
       directory-relative, so a file at `vocab/prefixes.yaml` imported
       from `vocab/core/*.yaml` resolves as `../prefixes`.

**What would falsify each:**

  A1 — run `make env`, then `make gen && make check`, in a shell with
       `VIRTUAL_ENV` unset. Failure for any reason other than the missing
       schema and missing fixtures falsifies it; so does `make -n gen`
       expanding to anything outside `.venv/bin/`.
  A2 — name one Part 2 obligation from the two sources not covered by
       the enumeration, or one enumerated element the unit does not need.
  A3 — re-run the nine curls; any non-200 falsifies.
  A4 — produce a dereferenceable RDF class or property URI for an
       ISO 19157 quality element, ISO 19112 identifier, or CIS coverage.
  A5 — name a SOSA/SSN term that distinguishes a sensed value from a
       modelled one without appealing to `sosa:Procedure` identity.
  A6 — name an Open-Meteo endpoint returning station observations with
       sensor or station identity.
  A7 — produce a QUDT unit URI or CF standard name for US AQI.
  A8 — exhibit a join required by this unit, between AirNow and
       Open-Meteo, that authority identifiers cannot satisfy.
  A9 — point at the pipeline whose matching rule L2 describes.
  A10 — exhibit two canonical facts derived from AirNow or Open-Meteo
        with different role sets.
  A11 — name a source in scope that serves JSON-LD, or show that
        `fixtures/README`'s "unmodified" permits a format conversion.
  A12 — for C13, capture the same `HourlyData_*.dat` hour twice, ~24h
        apart, and diff. Byte-identical across all rows falsifies the
        claim that C13 bites Part 2. For C11, exhibit a source-level
        convention that already distinguishes a dark monitor from a zero.
  A13 — withdrawn; nothing to falsify. To confirm the fix instead, run the
        current Makefile pattern over a file containing "separate by
        department" (expect no match) and one containing "EPA" (expect a
        match).
  A14 — `ls vocab/prefixes.yaml vocab/core/vocabulary.yaml`.
  A17 — run `make env` and read a version for `pyshacl`.
  A18 — run `make lean`. A non-zero exit falsifies it; a `sorry` outside
        `Identity.lean` falsifies the localisation claim.
  A16 — import a prefix-only schema into a second schema that uses one of
        its CURIEs in a `slot_uri` and declares no such prefix itself; run
        `gen-shacl`. An unresolved-CURIE error falsifies it.

**Requesting:** falsification of A1..A18, excluding A13 (withdrawn).

Highest-value targets, in my estimation: **A11** (decides the unit
boundary and the cost), **A6** (decides whether one of the two named
sources belongs in this part at all), and **A10** (suggests a claim the
unit will break rather than support).
