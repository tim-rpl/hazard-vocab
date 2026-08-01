# Claims Register

Every normative or structural assertion this project makes, with its
falsification status. This file is the source of truth for what is
believed versus what is known.

**Status values**

| Status | Meaning |
|---|---|
| `asserted` | Believed, no evidence either way. Do not build on it silently. |
| `tested` | An experiment was run and the claim survived. Evidence linked. |
| `falsified` | A counterexample exists. Linked. Claim must be withdrawn or scoped. |
| `scoped-down` | Falsified as originally stated; a narrower version survives. State the narrower version. |
| `abandoned` | No longer relevant. Say why. |

**Rules**

- New claims enter as `asserted`.
- Only the falsifier session changes a status.
- A `falsified` claim stays in the file. Deleting failures destroys the
  value of the register.
- Every status change records date and evidence path.

---

## Identity

### L1 — Authority match is an equivalence relation
Matching records on a functionally-unique identifier scheme is
reflexive, symmetric, and transitive.

- **Status:** `asserted`
- **Falsifier:** a scheme where one identifier maps to two distinct
  real-world entities, or one entity holds two identifiers in the same
  scheme.
- **Evidence:** —
- **Updated:** —

### L2 — Heuristic match is NOT transitive
Normalized-name-plus-rounded-centroid matching is reflexive and
symmetric but fails transitivity:
`∃ a b c. m(a,b) ∧ m(b,c) ∧ ¬m(a,c)`

- **Status:** `asserted`
- **Falsifier:** a proof that the relation is transitive under the
  actual normalizer and centroid rounding in use.
- **Note:** This claim is asserted as *true*. Confirming it is the
  first task. It forces the identity design fork (see ADR-001).
- **Evidence:** —
- **Updated:** —

### L3 — Identity partitions the record set
Whichever resolution strategy is chosen, the resulting relation is an
equivalence and canonical entities are its quotient.

- **Status:** `asserted`
- **Falsifier:** a resolution strategy that produces overlapping,
  non-disjoint clusters.
- **Evidence:** —
- **Updated:** —

---

## Merge

### T1 — Confluence
The canonical fact set is independent of source arrival order.

- **Status:** `asserted`
- **Falsifier:** two orderings of the same source set producing
  different canonical fact sets.
- **Cheapest test:** replay one day of captured fixtures in N shuffled
  orders; diff the outputs.
- **Evidence:** —
- **Updated:** —

### L4 — Merge is a join iff conflict resolution is a total order
Merge is associative, commutative, and idempotent only if the conflict
resolver is a total order on `(authority, validTime, tiebreak)`.

- **Status:** `asserted`
- **Falsifier:** a conflict case where the resolver is a partial order,
  or where two authorities are incomparable and no tiebreak exists.
- **Watch:** two evacuation authorities publishing different levels for
  the same zone at the same time is the likely first counterexample.
- **Evidence:** —
- **Updated:** —

### L5 — Monotonicity
Adding a source never retracts a canonical fact. Supersession is modeled
as a new fact with later validity, not as deletion.

- **Status:** `asserted`
- **Falsifier:** any rule whose body contains negation over source
  presence, or any transform that deletes rather than supersedes.
- **Evidence:** —
- **Updated:** —

---

## Epistemic separation

### L6 — No laundering
In a stratified program, no observation predicate is derivable from a
model-predicate body.

- **Status:** `asserted`
- **Falsifier:** a legitimate pipeline that must cycle between strata.
  Data assimilation is the suspected case.
- **Known limitation:** this covers *derivation only*, not presentation.
  It does not prevent rendering a forecast in an observation-styled UI.
  Do not cite this claim as covering the product property.
- **Watch:** QC'd and gap-filled monitor readings are model-touched but
  legitimately observations. The stratum assignment is a judgment call,
  and a compiler check on a wrongly-drawn boundary yields false
  confidence.
- **Evidence:** —
- **Updated:** —

---

## Structure

### T2 — Profile restriction is sound
Profile-valid implies base-valid, for every profile. Holds iff profiles
only add constraints, never relax them.

- **Status:** `asserted`
- **Falsifier:** a profile that widens a cardinality, removes a
  required slot, or extends an enum's permissible values.
- **Cheapest test:** Alloy, once two profiles exist.
- **Evidence:** —
- **Updated:** —

### C1 — Parts are jurisdiction-neutral
Parts 0–7 contain no agency-specific identifier, code list, or
authority. All such content is confined to `vocab/profiles/`.

- **Status:** `asserted`
- **Falsifier:** grep `vocab/core/` for agency names. Any hit falsifies.
- **Cheapest test:** a CI lint rule. Write it early.
- **Evidence:** —
- **Updated:** —

### C2 — Parts are hazard-neutral
A second hazard type can be added by writing a Part 1 profile and
touching Parts 4 and 7 lightly, with Parts 2, 3, 5, and 6 unchanged.

- **Status:** `asserted`
- **Falsifier:** any hazard requiring structural change to Parts 2, 3,
  5, or 6.
- **Known scope limit:** claimed only for **areal geophysical hazards
  with observable extent** (fire, flood, volcanic, debris flow, hazmat
  plume, severe weather). Earthquake is a suspected counterexample —
  the event is point-like and instantaneous, and the "area" is a
  ShakeMap, which is modelled rather than observed, so the Part 1 /
  Part 3 boundary may sit elsewhere. Pandemic is expected to break
  Part 4 outright.
- **Cheapest test:** write Parts 2, 3, and 6 for earthquake. Do not use
  flood — it is too similar to wildfire to be a real test.
- **Evidence:** —
- **Updated:** —

### C3 — Hyperedges are the native shape
Canonical facts are predominantly n-ary with diverse role sets, not
binary and not uniform.

- **Status:** `asserted`
- **Falsifier:** arity distribution concentrated at 2, or every
  observation sharing one identical role set (in which case it is a
  six-column table and neither the hypergraph nor the varying-role
  claim is real).
- **Cheapest test:** canonicalize one week of captured data; plot arity
  distribution and count distinct role sets.
- **Evidence:** —
- **Updated:** —

---

## Approach

### C4 — LinkML does not lock us in
The vocabulary can migrate to another declarative capture format for
roughly a day of scripting.

- **Status:** `asserted`
- **Falsifier:** dependence on LinkML-only expressiveness
  (`structured_pattern`, `rules`, `classification_rules`) or deep `is_a`
  chains that do not translate.
- **Cheapest test:** a lint rule rejecting those constructs.
- **Evidence:** —
- **Updated:** —

### C5 — The canonical layer unlocks something
There exists at least one question users would ask that cannot be
answered today and that the canonical layer answers.

- **Status:** `asserted`
- **Falsifier:** inability to name one. "It would be cleaner" and "the
  flood version would be easier" are engineering arguments, not
  vocabulary arguments — they do not satisfy this claim.
- **Note:** this is the only external claim in the register. If it
  cannot be answered, the rest is well-built infrastructure with no
  demonstrated demand.
- **Evidence:** —
- **Updated:** —

### C6 — The vocabulary is LLM-legible
A model given only `vocab/` and a raw source payload, with no other
context, produces a conformant canonical instance.

- **Status:** `asserted`
- **Falsifier:** it does not, or does so only with hand-holding —
  follow-up questions, corrections, or supplied examples beyond what
  `vocab/` contains.
- **Cheapest test:** a fresh session with no `CLAUDE.md`, no ADRs, and
  no conversation history. Hand it `vocab/core/part2-observation.yaml`
  and one raw Open-Meteo response. Ask for a conformant instance.
  Validate against `build/shapes.ttl`. Record the pass rate over ~10
  payloads drawn from different sources.
- **Note — this doubles as a schema-clarity test.** Where a model
  guesses wrong is usually where a human would too: a missing
  `description`, an implicit default, an ambiguous slot name, or an
  external URI whose semantics do not match the local use. The failures
  localise the ambiguity, which makes this the cheapest schema review
  available and the only claim in the register that produces a number
  you can track as the vocabulary grows.
- **Note — untestable until `vocab/core/` has content.** Like C2 and
  C5, no gate will touch this claim in the normal course of work. It is
  a claims-sweep item, not a gate item.
- **Watch:** a passing result proves legibility of what `vocab/` says,
  not that `vocab/` says the right thing. C6 and C5 are independent —
  a perfectly legible vocabulary that models the wrong domain would
  pass this and fail that.
- **Evidence:** —
- **Updated:** —

---

## Entity core

*(added by ADR-002)*

### C7 — No entity is subtyped by a role it plays
Entities are declared once in Part 0. Parts 1–7 assign roles in
relations. No class exists whose name is a role.

- **Status:** `asserted`
- **Falsifier:** any class in `vocab/core/` named for a role
  (`ExposedElement`, `Resource`, `Responder`, `Evacuee`), or any entity
  requiring a `sameAs` to itself under a different role.
- **Cheapest test:** lint rule on a role-noun word list.
- **Evidence:** —
- **Updated:** —

### C8 — `partOf` is the only mereology primitive
Crews, incident complexes, and sub-sampling all use
`partOf(Whole, Part, Interval)`. No part-whole relation is defined
outside Part 0.

- **Status:** `asserted`
- **Falsifier:** a part-whole case where the three uses need
  incompatible semantics — e.g. one requiring exclusive membership and
  another permitting overlap.
- **Watch:** a fire can belong to a complex while retaining its own
  identity and perimeter. Verify this is the same relation as crew
  membership and not a homonym.
- **Evidence:** —
- **Updated:** —

### C9 — No Part 0–7 element requires a natural-person identifier
The core is usable with `Person` reduced to "an agent that filled a
position." All identification is profile content.

- **Status:** `asserted`
- **Falsifier:** any required slot in `vocab/core/` carrying a name,
  contact detail, or personal identifier.
- **Cheapest test:** lint rule. Same shape as C1.
- **Evidence:** —
- **Updated:** —

### C10 — The four modalities are exhaustive
Observed, modelled, intended, and mandated cover every operational
statement an emergency management system makes.

- **Status:** `asserted`
- **Falsifier:** an operational statement fitting none of the four, or
  fitting two irreducibly.
- **Candidates to test first:** a burn ban (mandate or plan?); a road
  closure (both?); counterfactual analysis, which is modelled but
  conditioned on an intent not taken.
- **Note:** weakest and most interesting claim in the register.
- **Evidence:** —
- **Updated:** —

### C11 — Absent is distinguishable from zero
For every observation-bearing source, the model can express "no reading
because the observing system is unavailable" distinctly from "reading
is zero."

- **Status:** `falsified`
- **Evidence:** `docs/coverage.md` — observing-system health is a
  named gap. Nothing represents feed state, monitor availability, or
  fallback-tier position.
- **Updated:** 2026-07-31
- **Consequence:** ranked gap #2. Must be closed before the model is
  used operationally.

---

## Operating mode and integrity

*(added by falsification pass, 2026-07-31)*

### C12 — Exercise data cannot be mistaken for live data
Every statement carries an operating-mode discriminator, and no
consumer can render exercise or test data as actual.

- **Status:** `falsified`
- **Evidence:** no operating-mode field exists anywhere in the model.
  CAP provides `status: Actual | Exercise | System | Test | Draft` and
  we do not carry it.
- **Updated:** 2026-07-31
- **Consequence:** ranked gap #1. Safety-critical and free to fix.

### C13 — Correction is distinguishable from supersession
The model can express "the earlier fact was wrong" separately from
"the world changed."

- **Status:** `falsified`
- **Evidence:** claim L5 specifies supersession only. A republished
  perimeter (correction) and a grown fire (supersession) are currently
  indistinguishable.
- **Updated:** 2026-07-31
- **Note:** L5 is not wrong, but it is incomplete. Do not withdraw it —
  add correction as a second, distinct relation.

### C14 — Every fact carries a releasability determination
Sensitivity, sharing restriction, and sovereign data governance are
expressible.

- **Status:** `falsified`
- **Evidence:** no sensitivity dimension exists. Every fact implicitly
  assumes publishability.
- **Updated:** 2026-07-31
- **Note:** this is a dimension, not a row. Likely a Part 0 relation
  over `Statement`, not a slot on each class.

### C15 — Instances declare their model version and profile
An instance is self-describing with respect to which vocabulary version
and which profile it conforms to.

- **Status:** `falsified`
- **Evidence:** not modelled.
- **Updated:** 2026-07-31
- **Note:** costs nothing now, blocks everything at the first breaking
  change.

---

## Method

### C16 — The coverage matrix is complete
`docs/coverage.md` enumerates every capability a real-time emergency
management system requires.

- **Status:** `falsified`
- **Evidence:** the 2026-07-31 pass added three whole sections
  (operating mode, sensitivity, lifecycle phases) that the original
  three row sources could not surface. Completeness of an open-ended
  domain is not testable as stated.
- **Updated:** 2026-07-31
- **Reformulation that IS testable:** *every capability named in
  reference frameworks F1..Fn appears as a row.* Name the frameworks
  explicitly, then the claim has a falsifier. Until the framework list
  is fixed, "comprehensive" is a mood, not a property.

### C17 — Validation detects unmodelled fields in source payloads
`make check` fails when a captured payload contains a field the model
does not declare.

- **Status:** `falsified`
- **Evidence:** JSON-LD expansion silently discards keys absent from the
  `@context`. An undeclared key against a `sh:closed true` shape raised no
  violation until the key was added to the context, at which point
  `ClosedConstraintComponent` fired. Validation therefore checks only what
  the hand-authored context maps. Experiment run during the session-01
  measure pass on 2026-07-31; linkml 1.11.1 `gen-shacl`, pyshacl 0.40.1,
  rdflib 7.6.0.
- **Updated:** 2026-08-01
- **Consequence:** `make check` fails toward "pass". If a source appends
  a column, validation succeeds and the drift is invisible. Wrong
  failure direction for a falsification-driven project.
- **Note on provenance of this entry:** filed directly as `falsified`
  rather than entering as `asserted`, at the project owner's direction,
  because the counterexample was produced before the claim was written.
  This deviates from the two register rules above ("new claims enter as
  `asserted`", "only the falsifier session changes a status"). Recorded
  here so the deviation is visible rather than silent.

### C18 — The lint rules detect what they claim to detect
`make lint` fires on content that violates C1, C4, or the vacuous-theorem
rule, and does not fire on content that complies.

- **Status:** `asserted`
- **Falsifier:** a file violating C1, C4, or the vacuity rule that the
  lint does not catch (recall failure); or a compliant file that makes
  it fire (precision failure).
- **Cheapest test:** two throwaway files per rule — one violating, one
  compliant — run `make lint`, confirm it fails on the first and passes
  on the second, delete both. Under an hour for all three rules.
- **Note — recall has never been exercised.** Every firing of these
  rules to date has been a false positive, because `vocab/core/` is
  empty and `design/lean/` contains no violating theorem. No rule has
  ever been observed catching a real violation. A guard that has only
  ever been wrong is not yet a guard.
- **Watch — three precision failures observed and fixed:** `epa`
  matching *separate* and *department* (unanchored pattern, fixed with
  `\b` boundaries); the vacuity rule matching its own documentation in
  `design/lean/README.md` (fixed by scoping to `--include='*.lean'`);
  C1 and C4 scanning non-source files (fixed by scoping to
  `*.yaml`/`*.yml`). Common root cause: over-broad grep. Expect a
  fourth when `vocab/` gains README or documentation files.
- **Consequence if falsified on recall:** C1, C4, and the vacuity rule
  are unenforced, and any `tested` status resting on a clean `make lint`
  is unsupported.
- **Evidence:** —
- **Updated:** —