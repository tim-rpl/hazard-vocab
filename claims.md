# Claims Register

Every normative or structural assertion this project makes, with its
falsification status. This file is the source of truth for what is
believed versus what is known.

**Status values**

| Status | Meaning |
|---|---|
| `asserted` | Believed, no evidence either way. Do not build on it silently. |
| `examined` | Read critically and found unfalsifiable or untestable as stated, with a restatement proposed. Evidence about the claim, not about the world. Does not imply the claim is wrong — only that it cannot currently be tested. |
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

- **Status:** `falsified`
- **Falsifier:** a scheme where one identifier maps to two distinct
  real-world entities, or one entity holds two identifiers in the same
  scheme.
- **Evidence:** 2026-08-02 — claims sweep. **Two defects, one of them
  fatal to the claim as written.**

  **(1) The Falsifier field cannot falsify the claim.** Both disjuncts
  negate the claim's own antecedent. "Functionally-unique" *is* the
  hypothesis; a scheme where one entity holds two identifiers is not a
  counterexample to L1, it is a scheme outside L1's subject. Exhibiting
  either condition leaves L1 untouched. Same shape as L6.

  **(2) Reflexivity is false as stated**, and the repository already
  said so before this entry was ever read. `design/lean/HazardVocab/
  Identity.lean:9-15` calls `authorityMatch` a *partial* equivalence —
  "reflexive only on records that actually carry an identifier in the
  scheme" — and `Basic.lean:11-13` declares `idents` may be empty,
  calling partial identification "the normal case". The register entry
  and the design artifact have contradicted each other since the
  scaffold commit and nothing reconciled them.

  Machine-checked against the project toolchain (Lean 4.32.2, via
  `lake env lean`, no Mathlib, no `sorry`, exit 0). `authorityMatch`
  copied verbatim from `Identity.lean:17`:

  - `L1_not_reflexive` — `¬ ∀ s a, authorityMatch s a a`, witness a
    WFIGS record with `idents = []`.
  - `L1_not_transitive` — `¬ ∀ s a b c, …`, witness `a` carrying
    `IRWIN/A`, `b` carrying both `IRWIN/A` and `IRWIN/B`, `c` carrying
    `IRWIN/B`. This is exactly the Falsifier's second disjunct, and it
    breaks transitivity rather than the functionality hypothesis —
    which is why the falsifier reads as though it bites when it does
    not.

  A control (`1 = 2` by `rfl`) confirmed the harness reports errors
  rather than passing silently.
- **Updated:** 2026-08-02
- **Consequence:** L3 asserts the resolution relation is an equivalence.
  L1 was the only entry claiming an equivalence was available. See L1a.

### L1a — Authority match is a partial equivalence, given functionality
On the records that carry a value in scheme `s`, and where `s` is
functional over the record set, `authorityMatch s` is reflexive,
symmetric and transitive. Records carrying no value in `s` are related
to nothing, including themselves.

- **Status:** `scoped-down`
- **Narrower than:** L1, which is false as stated. Both entries stay.
- **Falsifier:** a record set over which the scheme is functional and
  every record carries a value in it, exhibiting a failure of
  reflexivity, symmetry or transitivity.
- **Evidence:** — *(not tested. `authorityMatch_symm` is proved in
  `Identity.lean:20`; `authorityMatch_trans` and
  `authorityMatch_refl_iff` both carry `sorry`, confirmed by
  `make lean` on 2026-08-02.)*
- **Updated:** 2026-08-02
- **Note:** functionality is a property of the issuing authority, not of
  our data. `Basic.lean:28` declares `SchemeInjective` an `axiom` for
  the same reason. Whether any real scheme satisfies it is a separate,
  untested question and L1a does not assert it.

### L2 — Heuristic match is NOT transitive
Normalized-name-plus-rounded-centroid matching is reflexive and
symmetric but fails transitivity:
`∃ a b c. m(a,b) ∧ m(b,c) ∧ ¬m(a,c)`

- **Status:** `asserted`
- **Falsifier:** a proof that the relation is transitive under the
  actual normalizer and centroid rounding in use.
- **Note:** This claim is asserted as *true*. Confirming it is the
  first task. It forces the identity design fork (see ADR-001).
- **Evidence:** 2026-08-01 — **unfalsifiable as stated.** "Rounded
  centroid" admits two relations and L2's truth value flips between
  them. (a) *Grid-cell equality* — round each centroid to a cell, then
  compare cells: this is a conjunction of two equality relations, which
  is transitive, and **L2 is false**. (b) *Tolerance proximity* —
  `|centroid_a − centroid_b| < ε`: not transitive, and **L2 is true**.
  No source access is needed to establish this; it does not depend on
  the reference implementation. The entry must name which relation it is
  about before either a proof or a counterexample can settle it.
  Measure-gate finding, 2026-08-01, superseding A11's reason for
  withholding.

  **Provenance correction, 2026-08-02 (claims sweep).** This finding was
  not new on 2026-08-01. `design/lean/HazardVocab/Identity.lean:37-57`
  names both relations — `exactCellMatch` and `proximityMatch` — states
  that L2 is FALSE for the first and TRUE for the second, and ends
  "**First task: determine which one the pipeline implements** … An
  unqualified L2 is unfalsifiable because it does not say which relation
  it is about." That text has been in the repository since the scaffold
  commit `023d10d`. The measure gate rediscovered it rather than found
  it. Recorded because the same gap — a design artifact contradicting or
  pre-empting its register entry with nothing reconciling the two — is
  what falsified L1.
- **Updated:** 2026-08-02

### L3 — Identity partitions the record set
Whichever resolution strategy is chosen, the resulting relation is an
equivalence and canonical entities are its quotient.

- **Status:** `asserted`
- **Falsifier:** a resolution strategy that produces overlapping,
  non-disjoint clusters.
- **Evidence:** 2026-08-02 — claims sweep. **Unfalsifiable as stated;
  status unchanged because neither reading has been tested.** "The
  resulting relation" admits two readings and L3's content collapses
  under both:

  (a) *The match relation itself.* Then L3 is **contradicted from
  inside this register**: L2 asserts that heuristic matching is not
  transitive, so it is not an equivalence, so "whichever resolution
  strategy is chosen" is false the moment heuristic matching is one of
  them. L2 and L3 cannot both hold under this reading.

  (b) *The reflexive-symmetric-transitive closure of the match
  relation.* Then L3 is **true by construction** — the closure of any
  relation is an equivalence and every equivalence partitions its
  carrier. Nothing about identity resolution is being asserted; this is
  a definition wearing a claim's clothes.

  The Falsifier field belongs to reading (b) and is unreachable under
  it: a closure cannot produce overlapping clusters. Under reading (a)
  the falsifier is reachable and L2 already satisfies it.

  **The Lean obligation does not settle this either.** `identity_
  partitions` (`Identity.lean:100`) takes symmetry and transitivity as
  *hypotheses* and concludes `rel a c ∧ rel c a`. It states neither
  reflexivity, nor disjointness, nor a quotient — it restates symm+trans
  and is adjacent-and-weaker in the sense of FALSIFIER §4 question 3. It
  carries `sorry` (`make lean`, 2026-08-02).

  **Restatement that would be falsifiable:** name the closure operator,
  then assert the non-trivial part — *the closure of the chosen match
  relation does not merge two records that name distinct real-world
  entities.* That is false under reading (a) whenever heuristic matching
  chains across a boundary, which is checkable against captured data,
  and it is not true by construction.
- **Updated:** 2026-08-02

---

## Merge

### T1 — Confluence
The canonical fact set is independent of source arrival order.

- **Status:** `asserted`
- **Falsifier:** two orderings of the same source set producing
  different canonical fact sets.
- **Cheapest test:** replay one day of captured fixtures in N shuffled
  orders; diff the outputs.
- **Evidence:** — *(untested. Statement audited 2026-08-02 and it
  survives the audit: the subject is named, the falsifier is executable
  by a third party, and a world in which it is false is describable.
  **This is not evidence for T1** — nothing was run against it.)*
- **Updated:** 2026-08-02
- **Blocked on, measured 2026-08-02:** the cheapest test names "captured
  fixtures". `fixtures/` contains three `.gitkeep` files and a README,
  and `transform/` contains one `.gitkeep`. There is nothing to replay
  and nothing to replay it through.
- **Note on the Lean obligation.** `fold_order_irrelevant`
  (`Merge.lean`, one of the file's two remaining `sorry`s as of
  2026-08-02) takes `Assoc merge` and `Comm merge` as hypotheses.
  Those are what T1 needs established, not assumed, so discharging its
  `sorry` would not establish T1 — it establishes that *if* the
  implemented merge is a commutative semigroup, order does not matter.
  FALSIFIER §4 question 3. Same shape as T2's Alloy assertion.

### L4 — Merge is a join iff conflict resolution is a total order
Merge is associative, commutative, and idempotent only if the conflict
resolver is a total order on `(authority, validTime, tiebreak)`.

- **Status:** `falsified`
- **Falsifier:** a conflict case where the resolver is a partial order,
  or where two authorities are incomparable and no tiebreak exists.
- **Watch:** two evacuation authorities publishing different levels for
  the same zone at the same time is the likely first counterexample.
- **Evidence:** 2026-08-02 — claims sweep. **The "only if" is false, and
  the counterexample is the merge L5 mandates.**

  L5 requires that adding a source never retracts a canonical fact:
  supersession is a new fact, never a deletion. A merge with that
  property is accumulation — union of fact sets. Union is associative,
  commutative and idempotent, and there is **no conflict resolver in it
  at all**, hence none that is a total order on
  `(authority, validTime, tiebreak)`. Every antecedent of L4's
  consequent holds and the condition L4 declares necessary is absent.

  Machine-checked (Lean 4.32.2, `lake env lean`, no Mathlib, no `sorry`,
  exit 0): `union_assoc`, `union_comm`, `union_idem` over
  `FactSet F := F → Prop`.

  **L4's own Lean obligation was false as stated, independently.**
  `not_idem_of_incomparable` — labelled in the file as "the converse
  direction, which is the one that bites" — was refutable: take
  `S := Unit`, `le := fun _ _ => False`, `merge := fun _ _ => ()`.
  `PicksGreater` holds vacuously, `¬ le a b` and `¬ le b a` hold, and
  the conclusion `∃ x y, merge x y ≠ merge y x ∨ ¬ (∀ z, merge z z = z)`
  fails. Its `sorry` could never have been discharged as written.

  **Discharged 2026-08-02 (B1 block verification).** The false
  obligation is gone from `Merge.lean`. The refutation is retained in
  the file as `refute_not_idem`, and the removed statement is quantified
  there verbatim — verified by diffing the theorem against its deleted
  text, so this is a refutation of what actually stood, not of a weaker
  restatement. The true content is now `underdetermined_of_incomparable`
  (**proved, no `sorry`**): incomparability does not break the algebra,
  it underdetermines the merge — given any conforming `merge`, a second
  conforming `merge'` exists disagreeing on the incomparable pair. Its
  hypotheses were machine-checked satisfiable at `S := Bool` before this
  was recorded, so it is not vacuous (FALSIFIER §4 question 2).

  The other obligation, `semilattice_of_total_resolver`, is the
  **sufficiency** direction. L4 asserts necessity. So the file
  formalises the direction L4 does not claim and got the direction L4
  does claim wrong — the second half is now repaired, the first stands.

  **Root defect: the subject is not named.** "Merge" denotes both the
  accumulating fact-set merge of L5 and a per-subject conflict-resolving
  pick, and L4 is false under the first. This is L2's failure mode in a
  second section of the register, and unlike L2 no disambiguation is
  needed to settle it — the union witness is valid under the plain
  reading of the words as written.
- **Updated:** 2026-08-02
- **Consequence:** T3's Consequence field records that "L4 makes
  merge-as-join conditional on conflict resolution being a total order."
  That reading of L4 no longer stands as a general statement. T3's
  falsification is unaffected — it is about profile composition — but
  its stated consequence for L4 should be re-derived against L4a.

### L4a — A total-order resolver is sufficient for a picking merge
For a merge that resolves conflicts on one subject by selecting a single
value, if the conflict resolver is a total order on
`(authority, validTime, tiebreak)` and the merge picks the greater under
it, then the merge is associative, commutative and idempotent.

- **Status:** `scoped-down`
- **Narrower than:** L4, which is false as stated. Both entries stay.
  L4a claims **sufficiency only**. Necessity is withdrawn, not narrowed:
  the union witness shows a join needs no resolver whatsoever.
- **Falsifier:** a total order and a picking merge under it for which
  associativity, commutativity or idempotence fails.
- **Evidence:** — *(not tested. `semilattice_of_total_resolver`
  (`Merge.lean`) states exactly this and still carries `sorry` —
  confirmed by a forced `make lean` rebuild, 2026-08-02, in which it is
  one of the file's only two remaining `sorry`s.)*
- **Updated:** 2026-08-02
- **Note:** the operationally interesting question survives the loss of
  necessity and is not asserted by either entry — *which* subjects
  require a picking merge rather than accumulation. The Watch case (two
  evacuation authorities, same zone, same instant) is a question about
  that boundary, not about the algebra.

### T3 — Profile composition preserves scheme precedence
The composition of a hazard profile and a jurisdiction profile yields a
total order over identifier schemes whenever each profile's own order is
total and neither reorders the base.

- **Status:** `falsified`
- **Falsifier:** two add-only profiles whose composed order contains an
  incomparable pair.
- **Evidence:** 2026-08-01 — witness, no solver required:

  > Base order over schemes: `ICAO`.
  > Hazard profile, add-only, total, does not reorder the base:
  > `ICAO < IRWIN`.
  > Jurisdiction profile, add-only, total, does not reorder the base:
  > `ICAO < AQSID`.
  > Composition is conjunction. `IRWIN` and `AQSID` are related by
  > neither profile, so they are **incomparable**. Not a total order.

  Every antecedent holds and the consequent fails. The proposed test
  (`order : seq Constraint` in the Alloy model, ~0.5 session) is not
  needed; a two-line witness settles it, per FALSIFIER §8.
- **Updated:** 2026-08-01
- **Origin:** proposed by H in the 2026-08-01 measure gate, promoted to
  the register by O under FALSIFIER §6 because it is about the artifact
  rather than about that gate's work.
- **Note on provenance:** filed directly as `falsified` rather than
  entering as `asserted`, because the counterexample existed before the
  claim was written. Same deviation from the register rules as C17, and
  recorded for the same reason — so it is visible rather than silent.
- **Consequence:** L4 makes merge-as-join conditional on conflict
  resolution being a total order. Profile composition, as currently
  designed, does not deliver one. L4 is not wrong; nothing establishes
  its precondition. See T3a.

### T3a — Profile composition preserves precedence, given a tiebreak
The composition of two add-only profiles yields a total order over
identifier schemes **if and only if** a tiebreak relation is defined
over schemes introduced by different profiles.

- **Status:** `scoped-down`
- **Narrower than:** T3, which is false as stated. Both entries stay.
- **Falsifier:** a composition rule that produces a total order over
  independently-introduced schemes without any cross-profile tiebreak;
  or a tiebreak that is itself partial.
- **Cheapest test:** name the tiebreak, then check that composing two
  add-only profiles under it is associative and commutative — otherwise
  order of profile application decides precedence, and L4 fails a
  different way.
- **Evidence:** — *(not yet tested; the tiebreak does not exist yet)*
- **Updated:** 2026-08-01

### L5 — Monotonicity
Adding a source never retracts a canonical fact. Supersession is modeled
as a new fact with later validity, not as deletion.

- **Status:** `asserted`
- **Falsifier:** any rule whose body contains negation over source
  presence, or any transform that deletes rather than supersedes.
- **Evidence:** — *(untested; `transform/` contains one `.gitkeep`.
  Statement audited 2026-08-02. **Not evidence for L5.**)*
- **Updated:** 2026-08-02
- **Audit finding, 2026-08-02 — the falsifier is a syntactic proxy and
  is narrower than the claim.** Absence of negation-over-source-presence
  and absence of deletion are *sufficient* for monotonicity, not
  necessary conditions for its failure. A rule that aggregates — `max`
  or `argmax` over `validTime`, a `latest-wins` projection — retracts a
  previously derivable canonical fact without containing either
  construct, so it passes the falsifier and breaks the claim. A grep
  that returns clean would therefore be an instrument reporting success
  having inspected the wrong thing (FALSIFIER §4). The proxy is still
  worth running; it is not equivalent to the claim.
- **Audit finding, 2026-08-02 — L5's Lean obligation is empty, and the
  file's corrected header note now vouches for it.**
  `monotone_under_source_addition` (`Merge.lean`) takes `hmono : ∀ a b
  f, a f → merge a b f` as a hypothesis and its proof body is
  `hmono a b f` — the hypothesis applied to its own arguments. It
  carries no `sorry` and elaborates clean, which is the FALSIFIER §4
  "artifact can be empty" failure in the form the `: True :=` lint does
  not catch. The honesty note rewritten at the B1 repair lists it under
  *what this file now guarantees* as "carries none — it is proved".
  That is literally true and it is the one theorem in the file this
  sweep had already recorded as establishing nothing. **Discharging its
  `sorry` was never the obligation; exhibiting `hmono` for a real merge
  is.**

  **Resolved 2026-08-02 (plan-gate block response 2, BV1).** The empty
  theorem is gone. `Monotone` is now a definition, and two statements
  stand where it did — both verified by elaborating the file from source
  with `lake env lean HazardVocab/Merge.lean` rather than by a `lake
  build` replay, which reports only `sorry` at `Merge.lean:88` and
  `:112`, i.e. `fold_order_irrelevant` and `semilattice_of_total_resolver`:

  - `retracting_merge_not_monotone` — `merge a b := b` is refuted against
    `Monotone` by a witness, not asserted.
  - `union_merge_monotone` — union satisfies it, so the obligation is
    satisfiable rather than impossible.

  **Status stays `asserted`.** Neither theorem is about *this project's*
  merge; `transform/` still contains one `.gitkeep`. What changed is that
  the file now separates merges instead of restating its own hypothesis,
  so L5's obligation is stated where an implementation can be measured
  against it. The aggregation gap in the falsifier above is untouched.
- **Audit finding — L5 is partly a policy, not a claim.** "We will not
  write deletions" is satisfiable by fiat at any moment. The falsifiable
  content is whether the *domain* permits it: can every real retraction
  be expressed additively? C13 (`falsified`) already records one case
  where the answer needed a second relation. That is the half worth
  testing.

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
- **Evidence:** 2026-08-02 — claims sweep. **Unfalsifiable as stated.
  Status unchanged; there is no `transform/` to test against and the
  defect is in the statement, not the artifact.**

  "In a stratified program, no observation predicate is derivable from a
  model-predicate body" is a **theorem of stratified Datalog**, true of
  every stratified program by the definition of stratification. It says
  nothing about this project's design and no state of this repository
  could contradict it.

  The Falsifier field confirms this rather than repairing it: "a
  legitimate pipeline that must cycle between strata" does not
  contradict the claim — it exhibits a program that is *not stratified*,
  and so falls outside the claim's antecedent. **Identical shape to
  L1's falsifier**, which also negates its own antecedent. Two of the
  register's six `L*` entries share this defect.

  The claim's Watch field already names the real, contingent assertion —
  that the stratum boundary can be drawn where we intend to draw it, with
  QC'd and gap-filled readings on the observation side. That is
  falsifiable and is not what L6 says.

  **Restatement that would be falsifiable:** *every predicate in
  `transform/` is assigned to a stratum, the assignment is acyclic, and
  the predicates carrying QC'd or gap-filled monitor readings sit in the
  observation stratum.* The first two clauses are decidable by the
  Mangle compiler; the third is a decision recorded in the source that a
  reviewer can contradict with a case.
- **Updated:** 2026-08-02

---

## Structure

### T2 — Profile restriction is sound
Profile-valid implies base-valid, for every profile. Holds iff profiles
only add constraints, never relax them.

- **Status:** `asserted`
- **Falsifier:** a profile that widens a cardinality, removes a
  required slot, or extends an enum's permissible values.
- **Cheapest test:** Alloy, once two profiles exist.
- **Evidence:** — **none, and the Alloy model cannot supply any.**
  Recorded 2026-08-01 after reading `design/alloy/parts.als`, not merely
  running it. `make alloy` returns UNSAT for `check_restrictionSound`
  and `check_compositionPreservesSoundness` with
  `demo_droppingBreaksSoundness` SAT as intended. Applying FALSIFIER §4's
  three questions:

  1. **What it states.** For every profile `p` with no drops and every
     instance `i`: `(Base.constraints + p.adds) ⊆ i.satisfies` implies
     `Base.constraints ⊆ i.satisfies`.
  2. **Vacuity.** Not vacuous by empty quantification — the hypotheses
     are satisfiable. It holds by **set algebra**: `A ∪ B ⊆ S ⟹ A ⊆ S`.
     Nothing profile-, LinkML- or SHACL-specific appears in it.
     Confirmed scope-free: raising every `check ... for 6` to `for 20`
     gives identical output.
  3. **Does it state what T2 needs?** **No — it assumes T2's
     conclusion.** `effective[p]` is *defined* as
     `(Base.constraints - p.drops) + p.adds`, so `adds` can only shrink
     the valid-instance set. But T2's own falsifier includes "extends an
     enum's permissible values", which in LinkML is an **addition that
     relaxes** — `sh:in` gains a member and more instances validate. The
     model can represent that only as a `drop`, and cannot detect it
     being classified as an `add`. The assertion therefore establishes
     "if relaxations are correctly classified as drops, profiles that do
     not drop are sound", which is circular with respect to T2.

  **Also inert:** deleting `sig Part` and `fact partsAcyclic` outright
  leaves every result identical. The `Part` signature, the `imports`
  relation and the acyclicity fact are referenced by no assertion in the
  file. The header cites "claims.md T2, C1, C2"; **C1 and C2 are tested
  by nothing there.**
- **Updated:** 2026-08-01

### T4 — The binding surface is decidable before either open ADR
Neither ADR-001's resolution nor ADR-003's changes the form of any of
the 23 external bindings; both add or relocate local slots only.

- **Status:** `falsified`
- **Falsifier:** an external binding whose `slot_uri`, range or
  cardinality differs between ADR-003 option A and option B, or between
  ADR-001 options A, B and C.
- **Evidence:** 2026-08-02 — **`sosa:madeBySensor`**, one of the 23.
  Two schemas identical but for that slot's `required`, through
  `gen-shacl` (linkml 1.11.1), then both payload shapes through pyshacl
  (0.40.1):

  | Shape | Open-Meteo observation | AirNow observation |
  |---|---|---|
  | option A, `required: true` (emits `sh:minCount 1`) | **Conforms: False** | Conforms: True |
  | option B, `required: false` | Conforms: True | Conforms: True |

  **The divergence is forced by the payloads, not chosen.** The
  Open-Meteo air-quality response publishes no instrument of any kind —
  zero top-level keys matching `id|station|sensor|instrument|site`. Under
  ADR-003 option B, Part 2 carries that response, so `madeBySensor`
  cannot be required. Under option A it is Part 3, Part 2's fixtures are
  AirNow only, every one carries a site, and required is available.
  Which payloads Part 2 must accept is exactly what ADR-003 decides, so
  the binding's admissible cardinality is not decidable before it.
- **Updated:** 2026-08-02
- **Origin:** proposed by H in the 2026-08-02 plan gate as the
  load-bearing assumption of the whole ordering; promoted to the register
  by O under FALSIFIER §6 because it is about the artifact rather than
  about the plan's work.
- **Note on provenance:** filed directly as `falsified` rather than
  entering as `asserted`, because the counterexample existed before the
  entry was written. Same deviation as C17 and T3, recorded for the same
  reason.
- **Consequence:** the plan's own abort condition (PA18) triggers on
  this. Whether it triggers on the item P5 depends on which of the
  plan's two readings of P5 is authoritative — "resolve and cache the
  bindings" (PA16) or "author them in final form" (PA5, PA18). Under the
  first, T4's falsification does not touch P5 and lands on P7. See T4a.

### T4a — Binding *identity* is decidable before either open ADR
The `slot_uri` of each of the 23 external bindings — which external term
it is — is fixed independently of ADR-001 and ADR-003. Their local
`range` and cardinality are not.

- **Status:** `scoped-down`
- **Narrower than:** T4, which is false as stated. Both entries stay.
- **Falsifier:** an external binding that resolves to a *different
  external term* under a different ADR outcome, rather than to the same
  term with a different local form.
- **Evidence:** — *(the claim itself is not yet tested. The T4
  counterexample moves a cardinality and leaves `slot_uri` fixed, which
  is consistent with T4a but does not establish it across all 23.)*

  **Scope boundary measured 2026-08-02** at the plan block-verification
  gate, because the plan now rests P5 on this claim. T4a's
  identity/form split is available **only for the 23 bound slots**. A1
  counts **33** slots in the unit: 23 carrying an external URI and **10
  with no usable external term, which "must be defined"**. For those 10
  there is no external identity to resolve, so "identity decidable,
  form not" has no content — the name *is* the identity and everything
  else about the slot is local form.

  **And declaring a local slot commits a cardinality**, verified
  through `gen-shacl` (linkml 1.11.1). A slot with no `range`, no
  `required` and no `multivalued`:

  ```yaml
  slots:
    procedureKind:
      description: No range declared at all.
  ```

  emits

  ```
  sh:property [ sh:description "No range declared at all." ;
                sh:maxCount 1 ; sh:order 0 ;
                sh:path ex:procedureKind ]
  ```

  — no `sh:datatype`, but `sh:maxCount 1`. Control: adding
  `multivalued: true` removes it. So the default is a choice made
  silently, and it is the same kind of constraint (`sh:maxCount` /
  `sh:minCount` on a property shape) that T4's counterexample moved.

  **This does not falsify T4a**, which is about the 23. It bounds it:
  T4a covers 23 of the 33 slots, and the plan's P5 covers all 33.

  **The mismatch is closed on the plan's side, 2026-08-02** (plan-gate
  block response 2, PA25). `docs/plan/plan-01-part2-part0.md` withdrew
  PA19 and removed clause 3 from P5: P5's item row and its
  definition-of-done now cover the 23 external identities only, and
  state explicitly that the ten local terms are not declared there. So
  P5 and T4a are about the same 23 slots and no longer disagree.

  **T4a itself is still untested** — the 23 have not been re-derived
  under the opposite ADR outcome. Nothing here is evidence for the
  claim; it removes an inconsistency between the claim and the plan
  resting on it.
- **Updated:** 2026-08-02

### C1 — Parts are jurisdiction-neutral
Parts 0–7 contain no agency-specific identifier, code list, or
authority. All such content is confined to `vocab/profiles/`.

- **Status:** `asserted`
- **Falsifier:** grep `vocab/core/` for agency names. Any hit falsifies.
- **Cheapest test:** a CI lint rule. Write it early.
- **Evidence:** 2026-08-01 — the cheapest test exists and does not work
  in two independent ways, so C1 has no usable guard. (1) `make lint`'s
  C1 grep targets `vocab/core/`, which contains one `.gitkeep` and no
  YAML. **It currently passes over zero files** — a clean result that
  inspects nothing (FALSIFIER §4). (2) The pattern is a fixed list of
  agency names. `AQSID` — an EPA AQS site identifier, and the exact
  content A17 named as the first genuine recall test — **does not
  match**. Run against an identical file in a scratchpad, `grep` exit 1,
  lint passes. Naming the agency in the adjacent prose makes it fire;
  the identifier scheme itself does not. C1's guard detects prose
  mentioning agencies, not jurisdiction-specific content.
  **Superseded the same day.** The grep was replaced by
  `scripts/drift-lint.py`, whose `jurisdiction` rule matches **by shape**
  — an acronym-form identifier not on a generic allowlist — rather than
  by a list of agency names. Verified by running it: `AQSID` and `IRWIN`
  are caught with no agency named anywhere in the file, and `DWD`/`JMA`
  are caught too, so it is not a US denylist. The gap that motivated the
  entry above is closed.

  **Two holes remain, both measured 2026-08-01.**
  - *Recall.* The rule inspects **names only** — class, slot, enum and
    permissible-value names. It does not inspect `prefixes:`, `meaning`,
    `slot_uri` or `class_uri`. A schema declaring
    `airnow: https://airnow.gov/scheme/` and carrying
    `meaning: airnow:AQSID` on a permissible value named
    `siteIdentifier` passes clean, exit 0. This matters because
    CLAUDE.md's Conventions designate `PermissibleValue.meaning` as the
    way to reference a code list — so once the project follows its own
    convention, names are where jurisdiction content is least likely to
    be. The `ACRONYM` bound is also 8 characters, so a 9+ character
    acronym passes; the docstring's stated limitation ("a
    jurisdiction-specific scheme with a non-acronym name passes") does
    not cover that case.
  - *Precision.* See C18.

  Status unchanged: C1 is a claim about our files, and there are no
  files yet. The evidence is about the instrument, not the claim.
- **Updated:** 2026-08-01

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
- **Evidence:** 2026-08-02 — claims sweep, per the standing instruction
  to examine claims no gate will ever touch. **Two defects. Status
  unchanged — `vocab/core/` holds one `.gitkeep`, so there are no Parts
  to retarget.**

  **(1) Half the claim is a mood, not a property.** "Touching Parts 4
  and 7 **lightly**" has no threshold, so no observed amount of churn in
  Parts 4 and 7 could contradict it. The Falsifier field covers only the
  other half — "structural change to Parts 2, 3, 5, or 6" — which is
  crisp and executable by a third party via `git diff --stat`. As
  written, a second hazard could rewrite Part 4 outright and C2 would
  survive by construction. Same failure as C16's "comprehensive".

  **(2) The Known scope limit and the Cheapest test contradict each
  other.** The scope limit restricts C2 to "areal geophysical hazards
  with observable extent" and then argues earthquake is not one — the
  event is point-like and instantaneous and the area is a modelled
  ShakeMap. The cheapest test then prescribes earthquake. If the scope
  limit holds, earthquake is outside C2's subject and writing it cannot
  falsify C2; if earthquake can falsify C2, the scope limit does not
  hold. The prescribed experiment cannot settle the claim it is attached
  to, whichever way that is resolved. §5.2 question 1.

  **Restatement that would be falsifiable:** name the churn bound —
  *adding a second hazard changes no slot, class or enum in Parts 2, 3,
  5 or 6, and adds only permissible values (no new or modified slots) in
  Parts 4 and 7* — and pick a hazard the scope limit admits. Volcanic
  ash or riverine flood-with-hazmat are inside the stated scope;
  earthquake is the test of the scope limit itself and is a **separate**
  experiment, not this one.
- **Updated:** 2026-08-02

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
- **Evidence:** 2026-08-02 — claims sweep. **Half falsifiable, half
  not. Status unchanged; nothing to canonicalise.**

  The second disjunct of the falsifier is crisp and executable: "every
  observation sharing one identical role set" is a count of distinct
  role sets, and `1` falsifies. Anyone can run it.

  The first is not. "Predominantly n-ary" against "arity distribution
  **concentrated** at 2" names no threshold, and the two are not
  complements — a distribution with 55% of facts at arity 2 is neither
  clearly concentrated nor clearly predominantly n-ary, and the author
  of the claim would decide. Requirement 2 of a falsifiable statement
  (executable by someone who is not its author) fails on this half.

  **Restatement:** fix the bound before the data is seen — e.g. *fewer
  than half of canonical facts have arity 2, and at least ten distinct
  role sets occur.* Any numbers chosen in advance work; choosing them
  after plotting the distribution does not.
- **Updated:** 2026-08-02

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
- **Evidence:** 2026-08-02 — claims sweep. **Unfalsifiable as stated,
  and its guard currently inspects nothing. Status unchanged.**

  **(1) No target format is named.** "Another declarative capture
  format" is unquantified over: migration to SHACL-plus-JSON-Schema and
  migration to, say, an OWL/ODM stack are different projects with
  different costs. Without a named target the claim has no truth value.

  **(2) The claim states a cost; the falsifier tests a construct list.**
  Even a clean run of the lint establishes only that three named LinkML
  constructs are absent. It does not bound the day of scripting, which
  is what C4 asserts. Conclusion overreaches evidence in the sense of
  §5.2 question 1 — and in the direction that matters, since the absent
  constructs are the *cheap* obstacles and the expensive ones (semantics
  that survive `gen-shacl` but have no analogue in the target) are not
  inspected at all.

  **(3) The guard inspects zero files, and unlike C1 this entry did not
  record it.** `make lint` on 2026-08-02 prints `C4: no LinkML-only
  constructs` followed by `note: no schema files found — these rules
  inspected nothing`. C1's entry records exactly this state for the
  jurisdiction rule; C4 shares the condition and recorded nothing. That
  asymmetry is why the entry read as unexamined.

  **Restatement:** name one target format and one artifact — *the
  vocabulary as it stands at tag X can be re-expressed in format Y with
  no loss of any constraint that `make check` enforces.* Then the
  falsifier is a constraint that survives `gen-shacl` and has no
  analogue in Y, and it is executable without reference to anyone's
  estimate of a day.
- **Updated:** 2026-08-02

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
- **Evidence:** 2026-08-02 — claims sweep, per the standing instruction
  to examine claims no gate will ever touch. **The falsifier is not an
  experiment, and the candidate this claim has been waiting for has been
  sitting in `FALSIFIER.md` unrecorded. Status unchanged — see below for
  why it does not move in either direction.**

  **The falsifier is unexecutable by construction.** "Inability to name
  one" is a fact about a person, not about the world: it is unbounded in
  time, not reproducible, and cannot be run by anyone other than
  whoever failed to think of an example. There is no state of the world
  that exhibits it. A claim of the form "there exists an X" is falsified
  only by a proof that no X exists, which for an open-ended space of
  user questions is not available. C5 as written can be *satisfied* but
  never *falsified*, and the register currently treats those as the same
  thing.

  **A concrete candidate exists and was never carried into this entry.**
  `FALSIFIER.md` §5.1 question 9 is grounded in a real defect: a
  PM2.5-specific statutory threshold was evaluated against a composite
  air-quality index for four builds, producing an impossible result that
  survived because nothing in the data model distinguished the two
  quantities. The charter states outright that this "is the strongest
  concrete case for the canonical layer existing". C5's Evidence field
  has read `—` throughout. The charter and the register have not been
  reconciled since §5.1 was written.

  **It does not satisfy C5 yet, and C17 is the reason.** C5 needs two
  things: a question unanswerable today (established — the substitution
  survived four builds) *and* one the canonical layer answers. The
  second is not established and current evidence runs against it: C17's
  second axis shows `gen-shacl` emits property shapes from the local
  `range` without consulting `slot_uri`, so a threshold declared against
  the wrong observed property generates a passing shape, exit 0, no
  warning. As the toolchain stands the canonical layer would **not**
  catch the defect that motivates it.

  **Restatement that would be falsifiable, and its experiment:** *a
  statutory threshold declared against `mmi:PM2.5` and evaluated against
  an instance carrying a composite AQI as its `sosa:observedProperty`
  raises a validation violation under `make check`.* Falsifier: it
  conforms. That is one schema fragment and two instances, it can be run
  by anyone, and it fails today — which makes it the strongest available
  test of C5 and simultaneously a second measurement of C17.
- **Updated:** 2026-08-02

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
- **Evidence:** — *(untested; `vocab/core/` holds one `.gitkeep`.
  Statement audited 2026-08-02. **Not evidence for C6.**)*
- **Updated:** 2026-08-02
- **Audit finding, 2026-08-02 — the cheapest test's instrument is one
  this register has already falsified.** The procedure ends "Validate
  against `build/shapes.ttl`. Record the pass rate." C17 is `falsified`
  on precisely that instrument, in two independent ways: JSON-LD
  expansion silently discards keys absent from the hand-authored
  `@context`, so a model that invents fields scores as conformant; and
  `gen-shacl` never consults `slot_uri`, so a model that binds an
  external term to a contradictory local range also scores as
  conformant. Both failures run in C6's favour — they inflate the pass
  rate — and they are concentrated on exactly the mistakes a model with
  no context is most likely to make. The number C6 promises to track is
  therefore an upper bound of unknown tightness, not a measurement.
  §5.2 question 1.

  This does not make C6 unfalsifiable. It means a *high* pass rate is
  not evidence, while a *low* one still is: the instrument fails toward
  "pass", so failures it does report are real. C6 can be falsified as
  written and cannot currently be confirmed.
- **Audit note:** "hand-holding" in the Falsifier is soft, but the
  Cheapest test pins it — no follow-up questions, no corrections, no
  examples beyond `vocab/`, one shot per payload. A third party can run
  that. This half of the entry is sound.

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
- **Evidence:** — *(untested against content; `vocab/core/` is empty and
  `make lint` reports `ok [role-named] 0 file(s)`. Statement audited
  2026-08-02. **Not evidence for C7.**)*
- **Updated:** 2026-08-02
- **Audit finding, 2026-08-02 — the guard exists and covers only the
  first clause.** The `role-named` rule is implemented and has
  demonstrated recall: `make lint-selftest` on 2026-08-02 reports it
  firing on `violating.yaml` and clean on `clean.yaml` and
  `flat-siblings.yaml`. It tests **names**. C7's second clause — "any
  entity requiring a `sameAs` to itself under a different role" — is a
  structural property no word list can see, and nothing tests it.
- **Audit finding — the word-list falsifier is bypassable without
  intent.** The rule matches a fixed role-noun list, so a class that is
  a role in substance under a non-role name (`EngagedAsset`,
  `CommittedResource`, `AffectedStructure`) passes clean. This is the
  same recall shape as C1's names-only limitation, and it is the more
  likely failure here: the obvious names are the ones an author
  avoids after reading invariant 6.

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
- **Evidence:** — *(untested; Part 0 does not exist. Statement audited
  2026-08-02. **Not evidence for C8.**)*
- **Updated:** 2026-08-02
- **Audit note, 2026-08-02 — survives the audit, with one soft edge.**
  The claim is two statements and both are checkable by a third party.
  The second ("no part-whole relation is defined outside Part 0") is a
  grep. The first is decidable once the relation exists, because the
  Falsifier names a concrete incompatibility — exclusive membership
  versus permitted overlap — and exclusivity is a cardinality, which is
  SHACL-expressible and so survives `make gen` (invariant 4). "Need
  incompatible semantics" would otherwise be a judgment call; the named
  pair rescues it.

  Soft edge: exclusive-versus-overlap is one incompatibility and the
  Falsifier reads as though it were the only one. Transitivity is a
  second and is not named — crew membership in a strike team in a
  division composes, sub-sampling a sample composes, a fire in a complex
  arguably does not (the complex does not inherit the fire's perimeter).
  Nothing in the entry would catch that, and the Watch field is pointing
  at it without saying so.

### C9 — No Part 0–7 element requires a natural-person identifier
The core is usable with `Person` reduced to "an agent that filled a
position." All identification is profile content.

- **Status:** `asserted`
- **Falsifier:** any required slot in `vocab/core/` carrying a name,
  contact detail, or personal identifier.
- **Cheapest test:** lint rule. Same shape as C1.
- **Evidence:** — *(untested; `vocab/core/` is empty. Statement audited
  2026-08-02. **Not evidence for C9.**)*
- **Updated:** 2026-08-02
- **Audit note, 2026-08-02 — survives the audit; falsifiable and
  executable.** "Any **required** slot in `vocab/core/` carrying a name,
  contact detail, or personal identifier" is decidable from the schema
  by a third party, and the `required: true` qualifier is what makes it
  crisp — an optional `name` slot does not falsify it, which is the
  right boundary for a claim about what the core *requires*.
- **Audit finding — the cheapest test is not built.** "Same shape as C1"
  names a rule that does not exist. `scripts/drift-lint.py` implements
  five rules as of 2026-08-02 (`inline-attributes`, `is-a-depth`,
  `exact-mappings`, `role-named`, `jurisdiction`); none inspects
  personal-identifier slots. C7's guard was written and C9's was not,
  and the two entries read identically. Recorded so the asymmetry is
  visible: C9 is currently unguarded.

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
- **Evidence:** 2026-08-02 — claims sweep. **One disjunct of the
  falsifier is executable, the other is not. Status unchanged.**

  "An operational statement fitting **none** of the four" is a clean
  falsifier: anyone can produce a candidate statement and argue it, and
  the four modalities are defined well enough to adjudicate a miss.

  "Or fitting **two irreducibly**" is not. The entry supplies no
  reduction procedure, so whether a dual fit is irreducible or merely
  unreduced is decided by whoever is defending the claim — requirement 2
  fails. The entry's own candidate list shows the problem rather than
  the case: a road closure is plainly both mandated (an order with legal
  force) and intended (an operational plan), and C10 survives that only
  if someone rules the pair reducible. Nothing says who or on what
  grounds.

  **Restatement:** make the reduction explicit — *for every operational
  statement, either exactly one modality applies, or the statement
  decomposes into two statements each carrying exactly one modality and
  linked by a declared relation.* Then a road closure is not a
  counterexample (it decomposes into a mandate and the plan that
  implements it, which is the right answer), and the falsifier becomes a
  statement that neither fits one modality nor decomposes — which a
  third party can test by attempting the decomposition and failing.

  Counterfactual analysis, the third candidate listed, is the one that
  looks hardest under the restatement and is worth attempting first.
- **Updated:** 2026-08-02

### C11 — Absent is distinguishable from zero
For every observation-bearing source, the model can express "no reading
because the observing system is unavailable" distinctly from "reading
is zero."

- **Status:** `falsified`
- **Evidence:** 2026-08-01 — measured, replacing the earlier citation of
  `docs/coverage.md` (our own file is not evidence). AirNow Oregon
  subset, 103 sites, `ValidTime` 2026-08-02T04:00:00Z, one request.
  **Three absence states occur independently in a single snapshot:**

  | `Status` | `PM25_Measured` | `PM25` null | rows |
  |---|---|---|---|
  | Active | 1 | no | 74 |
  | Inactive | 1 | yes | 24 |
  | Active | 1 | yes | 3 |
  | Active | 0 | yes | 1 |
  | Inactive | 0 | yes | 1 |

  Equipped-but-dark (24), live-but-no-datum-this-hour (3), and
  not-equipped (2) are distinct facts, and one not-equipped site is
  `Active` — a state no two-value absence flag can express. Marginal
  distributions alone would not establish independence; this is the
  cross-tabulation.

  **Three in-band sentinel channels in the same record**, none of them
  typed: `PM25` null; `PM25_AQI_SORT` = **-999** on exactly those 29
  rows; and `PM25_AQI_LABEL`, which equals `str(PM25_AQI)` for every
  present row and `'ND'` for every absent one — a stringified quantity
  with an absence token in band. Declared `range: string`, `'206'` and
  `'ND'` validate identically.

  **A fourth channel in a different field:** `Elevation` = exactly 0 on
  **26 of 103 rows (25%)**, where the next most frequent value occurs
  twice, there are 73 distinct values, and the nonzero minimum is 4.0 m.
  Missing-as-zero, in the field the geopotential-height comparison
  consumes.

  **Reproducibility defect recorded 2026-08-02 (claims sweep). The
  falsification stands; the evidence cannot currently be re-run by
  anyone else.** The 103-site AirNow snapshot this rests on is not in
  the repository: `fixtures/airnow/` contains a single empty `.gitkeep`,
  and `fixtures/` is not gitignored, so this is absence rather than
  exclusion. A reader can check the reasoning and cannot check the
  numbers. This is the evidence-side form of the falsifiability
  requirement that an experiment be executable by someone who is not its
  author, and it applies register-wide — T4's `gen-shacl`/pyshacl runs
  rest on Open-Meteo and AirNow payloads that are equally absent.
  Status unchanged: the cross-tabulation is internally consistent and
  the three absence states are independently describable, so the claim
  does not revert on this.
- **Updated:** 2026-08-02
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

  **Evidence upgraded 2026-08-02 (claims sweep).** The original evidence
  cited another entry in this register, which is the failure C11's own
  correction names — our own file is not evidence. A repository artifact
  now supplies it, and it is worse than the citation suggested.

  `correction_distinct_from_supersession` in
  `design/lean/HazardVocab/Merge.lean` was the obligation this claim
  would have been discharged by. **It was false as stated and its
  `sorry` could never be closed.** It quantified over *arbitrary*
  relations `corrects` and `supersedes` and concluded both are non-empty
  and mutually distinct; the diagonal breaks it. Machine-checked as
  `refute_correction_distinct` (Lean 4.32.2, `lake env lean` against
  this project's toolchain, no Mathlib, no `sorry`, exit 0; a `1 = 2`
  control confirmed the harness reports errors rather than passing
  silently).

  **Correction, 2026-08-02:** this entry previously described that
  refutation as instantiating both relations at `fun _ _ => False`. That
  witness is also valid, but it is **not the one the artifact uses** —
  `refute_correction_distinct` takes both at `fun _ _ => True`. The
  register described a refutation the file does not contain. Same
  register-versus-artifact defect this sweep filed against others;
  recorded rather than quietly overwritten.

  **Restated 2026-08-02 (B1 block verification).** The false obligation
  is gone. `Distinguishes` is now a **definition** — each relation holds
  somewhere the other does not — and `collapsed_implementation_fails`
  (**proved, no `sorry`**) establishes `¬ Distinguishes r r`: one
  relation cannot do both jobs. That is C13's complaint, machine-checked,
  and it is the honest form — distinguishability is an adequacy
  condition an implementation exhibits, not a theorem about arbitrary
  relations.

  **Status stays `falsified`, and the artifact does not discharge it.**
  Two gaps. First, `collapsed_implementation_fails` is one unfolding
  step from `Distinguishes`; the content sits in the definition H
  authored, not in the theorem. Second, `Distinguishes` ranges over
  arbitrary `F → F → Prop` with **no tie to `FactSet`, to `merge`, or to
  monotonicity** — so an implementation could exhibit it for two
  relations having nothing to do with the merge and read as discharging
  C13. What C13 needs is that the *implemented* correction and
  supersession relations are distinguishable **and both monotone under
  L5**. The artifact states the first half over any relations at all and
  says nothing about the second (FALSIFIER §4 question 3).

  **BV2 answered in part, 2026-08-02 (plan-gate block response 2).**
  `Merge.lean` gains
  `AdequateC13 merge corrects supersedes := Distinguishes corrects
  supersedes ∧ Monotone merge`, plus
  `monotone_does_not_give_distinguishes` — both elaborate from source,
  no `sorry`. The monotonicity half of BV2 is now stated.

  **The tie to the merge is still absent, and the new theorem is the
  proof of it.** `corrects` and `supersedes` remain arbitrary
  `F → F → Prop`, unconstrained by `merge`; `AdequateC13` conjoins two
  conditions rather than relating them. The scenario BV2 named — exhibit
  `Distinguishes` for two relations having nothing to do with the merge,
  pair it with any monotone merge, and read as having discharged C13 —
  satisfies `AdequateC13` exactly as before. `monotone_does_not_give_
  distinguishes` establishes that the two conjuncts are independent,
  which is what a conjunction of unrelated obligations looks like when
  it is checked.

  The file's commentary states "neither half implies the other"; one
  direction is machine-checked and the converse (`Distinguishes` without
  `Monotone merge`) is not stated as a theorem. Recorded because the
  §4 discipline is to read what an artifact states, not what its
  surrounding prose claims for it.
- **Updated:** 2026-08-02
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
- **Updated:** 2026-08-02
- **Reformulation that IS testable:** *every capability named in
  reference frameworks F1..Fn appears as a row.* Name the frameworks
  explicitly, then the claim has a falsifier. Until the framework list
  is fixed, "comprehensive" is a mood, not a property.
- **Precondition still unmet, checked 2026-08-02 (claims sweep).** The
  reformulation is not yet testable, because F1..Fn have not been fixed.
  `docs/coverage.md:11` states that rows are drawn from **five
  sources** — which are input provenance, not a framework list — and
  `:19-24` says so explicitly, noting the first three are US-centric and
  that a fourth surfaced capabilities the others could not, then
  recommending "the clause structure of ISO 22320" be tried "before
  claiming completeness". That is a framework named as a candidate, not
  a list adopted. `grep` for framework names across `docs/coverage.md`
  returns ISO 22320, ISO 19157 and ISO 19123 as row-level citations and
  no enumerated F1..Fn anywhere.

  Consequence: the register has carried a testable reformulation for two
  days with nothing able to run it, and the entry did not say so.
  Status unchanged — C16 remains `falsified` as originally stated, and
  its replacement remains unrunnable rather than untested.

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

  **Second axis, same failure direction, added 2026-08-01 and reproduced
  by O.** `gen-shacl` emits property shapes from the local `range`
  without ever consulting the `slot_uri` it binds, so a local range that
  *contradicts* the external term produces a passing shape. Run on a
  throwaway schema, linkml 1.11.1: a slot declared `range: string` and
  bound to `sosa:observedProperty` generated

  ```
  [ sh:datatype xsd:string ; sh:nodeKind sh:Literal ;
    sh:maxCount 1 ; sh:path sosa:observedProperty ]
  ```

  where SOSA declares `schema:rangeIncludes sosa:ObservableProperty` and
  SSN adds `owl:allValuesFrom sosa:ObservableProperty` with
  `owl:cardinality 1`. **Exit 0, empty stderr, no warning.** Nothing in
  `make gen` or `make check` inspects the external term. Every external
  binding is exposed, and the error is invisible precisely where a
  binding is wrong.
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

- **Status:** `falsified`
- **Falsifier:** a file violating C1, C4, or the vacuity rule that the
  lint does not catch (recall failure); or a compliant file that makes
  it fire (precision failure).
- **Evidence:** 2026-08-01 — **both halves falsified, by three
  independent experiments.** Since this entry was written the lint
  gained a fourth section (`C19: no OO drift in vocab/`) and a
  `lint-selftest` target, so the "recall has never been exercised" note
  below is superseded: recall has now been exercised and it fails.

  **Precision failure — the false positive is the Part 0 shape the
  measure gate scopes.** The `is_a` rule counts `is_a` declarations
  *per file*, not chain depth, while its message says "depth >2". A file
  with one abstract base and three depth-1 subclasses —

  ```yaml
  classes:
    Entity:  {description: Base.}
    Asset:   {is_a: Entity}
    Place:   {is_a: Entity}
    Agent:   {is_a: Entity}
  ```

  — fails with `FAIL: ... has 3 is_a declarations — depth >2 is drift
  (C19)`. That file complies with invariant 5 and is the planned Part 0
  fragment. `make lint` will reject the first Part 0 file authored, for
  being correct.

  **Recall failure 1 — the drift rule misses its own target case on file
  position.** The `exact_mappings` awk tests its counter only on the
  first non-list line after the block; at EOF that line never comes.
  Two `exact_mappings` on one class, with the list ending the file,
  gives `EXIT=0`. The identical content with one more class after it
  fails. This is the Platform ≡ Sensor case the rule was written for.

  **Recall failure 2 — C1's grep misses `AQSID`.** See C1's Evidence.

  **The self-test does not detect any of this, and demonstrates one rule
  of four.** `DRIFT_CHECKS` is four recipe lines; the first matches
  `violating.yaml` and make aborts the recipe, so rules 2–4 never run
  against the fixture. `lint-selftest` prints "ok — violation caught"
  and exits 0. Decomposed into three variants, each stripping the
  earlier violations, all four rules do fire individually — so the rules
  work and the instrument reporting on them does not.

  **Round 2, same day — all four defects above closed, two new ones
  found. Status unchanged, evidence entirely replaced.** The shell
  recipe was rewritten as `scripts/drift-lint.py` with five named rules
  reporting independently. Verified by running the linter against all
  seven fixtures rather than through `lint-selftest`, since the
  selftest was the instrument under suspicion:

  | Fixture | exit | Fires |
  |---|---|---|
  | `violating.yaml` | 1 | four separate FAILs, `jurisdiction` `ok` in the same run |
  | `mappings-at-eof.yaml` | 1 | exact-mappings |
  | `jurisdiction-in-enum.yaml` | 1 | `AQSID`, `IRWIN` |
  | `jurisdiction-foreign.yaml` | 1 | `DWD`, `JMA` |
  | `clean` / `flat-siblings` / `generic-acronyms` | 0 | none |

  Rules now report separately instead of aborting after the first;
  is-a is resolved transitively ("chain depth 3 (max 2)") rather than
  counted per file; mappings-at-EOF fails; `AQSID` is caught by shape.

  **New precision failure — 8 for 8 on external vocabularies this
  project has committed to binding.** `CF`, `NVS`, `DQV`, `ADMS`,
  `DCAT`, `DCT`, `OMS` and `UCUM` all fire. `GENERIC_ACRONYMS` carries
  `SOSA`, `PROV`, `QUDT`, `SSN`, `ISO`, `OGC`, `W3C` and others, but not
  `CF` — which CLAUDE.md's Conventions name in the same sentence as
  three of the allowlisted ones — and not `NVS`. `DQV` and `ADMS` are
  the terms the measure gate settled on for result quality and absence
  reason. Milder than the earlier `is_a` false positive: the message
  names the fix, it fails loudly rather than passing silently, and it
  costs one line per term. But the first file binding CF will hit it.

  **New recall gap:** the rule inspects names only, not `prefixes:`,
  `meaning`, `slot_uri` or `class_uri`. See C1.

  **Round 3, 2026-08-02 — both round-2 defects closed, verified by
  re-running the original counterexamples rather than by reading a
  report. Status unchanged; two holes remain.**

  | Case | Round 2 | Now |
  |---|---|---|
  | The eight committed vocabularies (`CF NVS DQV ADMS DCAT DCT OMS UCUM`) | 8 FAILs | **0 FAILs** |
  | Jurisdiction carried only in `prefixes:` / `meaning` | exit 0 | **fires** — matched by namespace host |
  | `CALFIREINC`, 10 chars, past the 8-char bound | exit 0 | **fires** — bound removed, not raised |
  | *Control:* `w3id.org` + `purl.org` + `w3.org` declared together | — | **exit 0** — legitimate shared-redirect namespaces still pass |

  The control is the one that mattered: `w3id.org` and `purl.org` are
  public redirects anyone may register under, and LinkML's own namespace
  lives on `w3id.org`, so host-level matching alone would have had to
  choose between a false positive on every schema and a false negative on
  every registrable path. Host-plus-path for shared redirects avoids
  both. `make lint-selftest` reports 20 rule/fixture pairs, 5/5 rules
  with demonstrated recall.

  **Still open, and why the status does not move.** Two
  jurisdiction-specific schemes still pass all five rules:
  - `id.loc.gov` is allowlisted as a single-authority vocabulary host,
    but it is the US Library of Congress and LCSH/LCNAF are national
    schemes reused internationally. Arguably a deliberate judgement; it
    should carry its reason inline the way the eight above now do.
  - A scheme with a camelCase name, no URI, and the jurisdiction carried
    only in its `description` passes. This is the rule's documented
    limitation, and closing the URI routes makes it the primary
    remaining one. The real test — whether an identifier is declared by
    some profile — cannot run until profiles exist.

  **Re-verified 2026-08-02** at the plan block-verification gate, by
  re-running the counterexample rather than by reading PA2's table: the
  `id.loc.gov` case still exits **0** with all five rules `ok`. F14 is
  open, unchanged. `make lint-selftest` still reports 20 rule/fixture
  pairs, 5/5 rules with demonstrated recall.

  **One instrument improvement worth recording, since §4 is about
  instruments that report success having inspected nothing:**
  `make lint` now prints `0 file(s)` per rule and the line *"note: no
  schema files found — these rules inspected nothing"*. The clean
  result now declares its own vacuity instead of reading as a pass.
  This is why C1's *"it currently passes over zero files"* is no longer
  silent.

  **Round 4, 2026-08-02 — the vacuity rule now parses instead of
  matching text, and a sixth counterexample is open. Status unchanged.**
  Verified by running each case, not by reading H's tooling declaration:

  | Case | `scripts/lean-lint.py` |
  |---|---|
  | *Control* — `theorem t : True := by trivial` | exit **1**, fires |
  | `theorem t : (0:Nat) = 0 := rfl` (weakened conclusion) | exit **0**, uncaught |
  | `theorem t (x : Nat) : x = x := rfl` (weakened conclusion) | exit **0**, uncaught |
  | `theorem t {P : Prop} (h : P) : P := h` (hypothesis from itself) | exit **0**, uncaught |

  Both documented gaps confirmed present. `make lint-selftest` now
  reports **22 rule/fixture pairs, 6/6 rules with demonstrated recall** —
  the 20 / 5-of-5 figures in the dated blocks above are superseded, not
  wrong when written. `design/lean/HazardVocab/Merge.lean` now contains
  the literal `True := by trivial` inside a comment and
  `lean-lint.py design/lean` exits **0**: BR-7's precision failure is
  closed by parsing, and the repository's own file is a live precision
  case. The Watch below predicted a fourth precision failure "when
  `vocab/` gains README or documentation files"; it arrived in
  `design/lean/` instead, which is the right prediction with the wrong
  location.

  **F14 re-run 2026-08-02, exit 0, five rules `ok`.** Unchanged and open.

  **Sixth counterexample — precision, and it is the first about this
  project's own namespace rather than a borrowed one.** The jurisdiction
  rule's `check_uri` is applied to every entry in `prefixes:`, against
  `SINGLE_AUTHORITY_HOSTS` / `SHARED_ALLOWED_PREFIXES`
  (`scripts/drift-lint.py`). A Part 0 core file must declare the
  vocabulary's own namespace as its `default_prefix`, and no host it
  could choose is admitted:

  | Declared namespace | `drift-lint.py` |
  |---|---|
  | `https://w3id.org/hazard-vocab/` | exit **1** — shared redirect, path not allowlisted |
  | `https://hazard-vocab.org/ns/` | exit **1** — host not a known generic vocabulary host |
  | `https://example.org/hv/` | exit **1** — same |

  That is a compliant file — jurisdiction-neutral core content, invariant
  2 satisfied — making the rule fire, which is C18's precision half.
  Root cause is the one F14 and the eight-vocabulary case share: a fixed
  allowlist standing in for a judgement. Unlike those, this one is not
  about a borrowed vocabulary — it fires on the first file this project
  authors for itself.

  **Entry repaired 2026-08-02 (claims sweep).** The measure-gate
  evidence block above was inserted after the `Falsifier` field while
  the original template stubs were left in place, so this entry carried
  two `Evidence` fields and two `Updated` fields, and an orphan
  `- **Evidence:** —` was the last line of the file. The empty stubs are
  deleted. Fields below that describe tooling since replaced are marked
  superseded rather than deleted — the precision failures they record
  actually happened, and an empty template stub is not history. No other
  entry in the register carries duplicate fields; C18 was the only one.
- **Updated:** 2026-08-02
- **Cheapest test — superseded 2026-08-02.** *"Two throwaway files per
  rule — one violating, one compliant — run `make lint`, confirm it
  fails on the first and passes on the second, delete both. Under an
  hour for all three rules."* Superseded in three ways: there are five
  rules, not three; the fixtures are no longer throwaway but a committed
  suite under `scripts/lint-fixtures/`; and the round-1 evidence showed
  `make lint` was the wrong harness for this test, because the recipe
  aborted after the first failing rule so rules 2–4 never ran against
  the fixture. `make lint-selftest` now enumerates 20 rule/fixture pairs
  by name. Retained because it records what the test was believed to
  cost before any of that was known.
- **Note — superseded 2026-08-02.** *"Recall has never been exercised.
  Every firing of these rules to date has been a false positive, because
  `vocab/core/` is empty and `design/lean/` contains no violating
  theorem. No rule has ever been observed catching a real violation. A
  guard that has only ever been wrong is not yet a guard."* False as of
  the round-2 rewrite and confirmed again on 2026-08-02: `make
  lint-selftest` reports 5/5 rules with demonstrated recall against
  committed violating fixtures. It remains true that **no rule has
  fired on `vocab/` content**, because there is none — recall is
  demonstrated against fixtures, not against the material.
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