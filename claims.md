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
- **Instrument finding, 2026-08-02 (block verification 6) — a `sorry`
  inventory taken from `make lean` output is cache-dependent, and this
  round it under-reported by five.** `make lean` runs `lake build`,
  which emits `declaration uses 'sorry'` only for modules it actually
  elaborates. Modules replayed from cache emit nothing. Measured in one
  session, same working tree, no source edit:

  | Invocation | `sorry` warnings |
  |---|---|
  | `make lean`, cache as found at session start | **4** — `Identity.lean:83`, `:100`, `Merge.lean:89`, `:113` |
  | after `rm -rf .lake/build/lib && lake build` | **9** — seven in `Identity.lean` (`:26 :33 :59 :70 :77 :83 :100`), two in `Merge.lean` (`:89 :113`) |
  | `make lean` again, warm | 9 |

  Source `grep` agrees with the clean rebuild: `Identity.lean` carries
  seven `sorry`s, `Merge.lean` two. **This corrects O's own evidence in
  block verification 5**, which recorded "the four in `Identity.lean`"
  — that was the cached number, not the file's. The replay caveat was
  already noted for one theorem pair below; the general form is that
  **`make lean` reports a lower bound on `sorry`, never a count.** Same
  family as C17 and C18: an instrument reporting success over what it
  did not inspect. Any claim citing a `sorry` count from `make lean`
  needs a clean rebuild or a source `grep` behind it. The Makefile is
  human-owned; reported, not edited.
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

  **Re-run 2026-08-02, block verification 3 — still inert.** Mutation
  applied to a copy with a fail-loud guard on the target string, then
  confirmed absent by `grep -c` before running. All three commands return
  identical results with the signature and fact deleted:
  `check_restrictionSound` UNSAT at scope 6,
  `demo_droppingBreaksSoundness` SAT as intended,
  `check_compositionPreservesSoundness` UNSAT at scope 6.
  `design/alloy/parts.als:2` still reads *"See claims.md T2, C1, C2."*
  Status unchanged. Recorded as a finding at the design gate (F-1) rather
  than as a block: this entry has carried the correct account since
  2026-08-01, so the register is right and only the artifact header is
  stale.
- **Updated:** 2026-08-02

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

  **The scope boundary is reopened by the design gate, 2026-08-02.
  Status unchanged; the number this claim is about may not be 23.**
  ADR-004 Decision C decides that `assertedTime` and
  `prov:generatedAtTime` are one slot. `assertedTime` was item 5 of the
  **ten** local terms, so on that decision it moves from the write list
  to the bind list and the bound set becomes **24**.
  `docs/plan/plan-01-part2-part0.md:855-861` (PA25) states this
  outright — *"if they are the same slot the surface is 24 bind / 9
  write, not 23/10"* — and declined to move the count because it was a
  design-gate question. It has now been decided, and ADR-004's
  reconciliation table instead removed the slot from `write` without
  adding it to `bind`, dropping its total from 32 to 31.

  Consequence for this entry: T4a is stated over "the 23", and P5's
  definition of done covers "the 23 external identities only". If the
  decision stands, both are 24 and the mismatch this Evidence field
  recorded as *"closed on the plan's side"* is open again on the other
  side. Filed as blocking finding B1 at the design gate; not resolved
  here, because which figure is right is H's to decide.

  **2026-08-02, block verification — the answer is neither 23 nor 24,
  and this claim's subject population no longer denotes.** ADR-004's
  amended reconciliation **retires** both `23 bind / 10 write of 33` and
  A31's `35–36` as incommensurable rather than reconciling them, on the
  ground that `23` was never a count of slots: A3's list mixes bound
  slots, bound classes, and permissible-value URIs and reports them as
  one number. I checked that partition against the published graphs and
  it holds (see the design-gate message). Its replacement population for
  bound slots is **16, or 17 on Decision C**.

  So T4a — *"the `slot_uri` of each of the **23** external bindings"* —
  is stated over a set the deciding ADR has withdrawn, and its Falsifier
  inherits the same term. This is not a falsification: nothing shows the
  identity/form split is false. It is a claim whose subject was retired
  underneath it, and it cannot be tested until the population is
  restated. Status stays `scoped-down`; restating the claim is H's under
  CLAUDE.md, and O will not narrow it to make it testable.

  ADR-004 also contradicts itself on which of 16 or 17 is right —
  Decision C says the identification *"does not add to the bind
  count"*, and the reconciliation table adds it, citing Decision C.
  Filed as B1 at the block-verification gate.

  **2026-08-02, block verification 2 — the self-contradiction is gone
  and the arithmetic underneath it is still wrong.** Verified by diff on
  `520ddde`: Decision C now reads *"it adds a bound slot and no new
  external URI"* and distinguishes the two populations explicitly, which
  agrees with the reconciliation table's 16 → 17. The contradiction I
  filed is genuinely closed.

  But the two rows the table adds are drawn from different populations.
  Row 1's baseline **16** is the `slot_uri` count from the partition,
  which ADR-004 itself labels *"41 external URIs of three kinds"* — a
  count of **URIs**, and `generatedAtTime` is in its enumerated list.
  Row 5's baseline **10** is the local-slot count from
  `measure-01:100-110`, a count of **slots**, and `assertedTime` is item
  5 of it. **ADR-004 Decision C decides those are one slot.** So the two
  rows overlap by one member and `17 + 9 = 26` counts it twice; the
  distinct total is 25.

  This is the defect ADR-004 diagnoses four lines earlier in its own
  words — *"`33` inherits the same defect, because it was `23 + 10` — a
  mixed-kind URI count added to a local-slot count"* — reproduced in the
  figure written to replace it. It is the third value this quantity has
  taken (`23/9 of 32`, `24/9 of 33`, `17 + 9 = 26`).

  T4a's status stays `scoped-down` for the reason recorded above: its
  subject population is retired either way, and which of 16 or 17 is
  right — like whether the replacement baseline should be a slot
  partition at all — is H's to decide, not mine to narrow.

  **2026-08-02, block verification 3 — the replacement partition is
  itself wrong, and the entry above got it wrong in the same direction.**
  ADR-004 decides **two** removals from A1's ten local slots and applies
  **one**. `crs` is item 6 of the ten (`measure-01:100-110`, stated in
  bold there) and Decision A `:40` removes it; `assertedTime` is item 5
  and Decision C `:107` removes it. Both are restated in Consequences at
  `:285` and `:287`. But `:107` reports the arithmetic as *"the
  local-slot count moves 10 → 9"* — one decrement, attributed solely to
  `assertedTime` — and the partition table at `:155` inherits the 9.

  **10 − `crs` − `assertedTime` = 8**, the bound row stays **16**, and
  the distinct total is **24**. No compensating addition exists inside
  the population: Decision B's `operatingMode`, `modelVersion` and
  `profileConformance` are not among A1's ten, and the partition is
  explicitly *"the slots A1 enumerated."*

  **The block-verification-2 paragraph above is corrected by this one.**
  It removed the `assertedTime` double-count and concluded 25, never
  applying Decision A's removal of `crs` — the same class of error it was
  filing, one population narrower. Recorded rather than rewritten,
  because a register that shows only where the reviewer was right is
  worth less than one that shows where it was not.

  This is the fifth value the quantity has taken: `23/9 of 32`,
  `24/9 of 33`, `17 + 9 = 26`, `25`, `24`. Status stays `scoped-down`:
  the subject population is still retired, and **which figure is right
  remains H's to decide** — 24 is what ADR-004's own two decisions imply,
  not a number O is substituting.
- **Updated:** 2026-08-02

### C1 — Parts are jurisdiction-neutral
Parts 0–7 contain no agency-specific identifier, code list, or
authority. All such content is confined to `vocab/profiles/`.

- **Status:** `falsified`
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

  **2026-08-06 — "there are no files yet" is no longer true, and the
  rule has now run on material.** `vocab/core/prefixes.yaml` exists, and
  `jurisdiction` inspects it: all nine rules report `1 file(s)` where
  they reported `0`. Exercised by mutation on a copy outside `vocab/` —
  adding `nwcg: https://data.nwcg.gov/ontology/` to the real file gives
  `exit 1, FAIL [jurisdiction]`, so the rule fires on the first authored
  file in the direction it was written for.

  **A third hole, and it is the one this file is made of.** The recall
  hole above says the rule does not inspect `prefixes:`. That is now
  half-wrong and worse than it read: `drift-lint.py:378-381` *does* walk
  the map, and checks the namespace's **host** against an allowlist —
  never the namespace itself. Mutating `sosa:` to
  `http://www.w3.org/ns/sosa-TYPO/` passes all nine rules at exit 0,
  because the host is still `www.w3.org`. So a prefix map may be
  jurisdiction-neutral, fully declared, and point every CURIE at a
  namespace that does not exist. Status stays `asserted`: the delivered
  file's 24 namespaces are correct, checked by hand against the sidecar
  `namespace:` fields, but nothing in the build would have said so.

  **2026-08-07 — FALSIFIED on the first authored schema, by the claim's
  own stated falsifier.** *"grep `vocab/core/` for agency names. Any hit
  falsifies."* Four hits in `vocab/core/part0-entity-core.yaml`:

  | Line | Content | Position |
  |---|---|---|
  | 88 | *"the IRWIN identifier and the state portal's local name for one fire"* | `alias` example |
  | 112 | `https://w3id.org/ohim/profiles/us/scheme/irwin` | `identifierScheme` example |
  | 146 | *"an IRWIN identifier, from which identity may be established"* | `aliasKind` example |
  | 388 | *"an IRWIN identifier issued by one agency and republished by another"* | `Identifier` example |

  Line 112 is an **agency-specific identifier scheme URI**, which is the
  claim's statement falsified verbatim rather than by the name-grep
  clause. It reaches generated output at
  `build/jsonld/vocabulary.jsonld`.

  **The same file asserts the opposite about itself, 66 lines above the
  first hit** — the schema `description:` carries *"JURISDICTION
  NEUTRALITY: no agency name, no national identifier scheme, no national
  code list appears here. CLAUDE.md invariant 2."* Claim and artifact
  are one file apart (FALSIFIER §5.2 item 4).

  **`make lint` is clean over it, and that is the documented recall hole
  rather than a new one.** `jurisdiction` inspects class, slot, enum and
  permissible-value **names**; `examples:` and `description:` blocks are
  not names. The hole recorded above on 2026-08-01 has now admitted real
  content into `vocab/core/`, which is why this is filed against C1 and
  not only against C18: the guard behaved as documented and the
  vocabulary is wrong anyway.

  **Invariant 2's own operational test also fails.** *"the core must
  retarget to flood or earthquake without edits"* — 13 wildfire-specific
  strings across the file's examples and descriptions (`fire`,
  `perimeter`, `wildfire`, `air tanker`, `evacuation zone`), every one
  requiring an edit to retarget.
- **Updated:** 2026-08-07

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

  **2026-08-02 — the watch list gains a stronger argument than
  portability, verified by running it. Status unchanged; the entry is
  still unfalsifiable as stated.** `rules` and `equals_expression` are
  on this claim's falsifier as LinkML-only and non-portable. P15, and
  O's independent reproduction, show they are also **non-functional**:
  both are accepted by linkml 1.11.1 at exit 0 with empty stderr and
  generate no cross-slot construct at all (C17 axis 3). Avoiding them
  therefore costs nothing and does not depend on ever migrating, which
  removes the only reason a project might have taken the trade
  deliberately.

  This does not move the status. It narrows the exposure the falsifier
  was written to catch — and it does so by making two of the three named
  constructs irrelevant rather than by testing the day-of-scripting
  claim, which is still untested and still the part that carries the
  assertion.
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

  **2026-08-02 — the restatement above was executed (P15,
  [`exp-01`](docs/experiments/exp-01-property-substitution.md)), and O
  reproduced it independently from scratch. First affirmative evidence
  this claim has had. Status unchanged, for a reason the experiment
  itself supplies.**

  Reproduction, built fresh from the record's prose — one
  `ExceedanceCheck` class carrying both sides of the comparison, two
  instances, linkml 1.11.1 `gen-shacl` + pyshacl 0.40.1 from `.venv`:

  | Shapes | Case A — composite `us_aqi` 160 vs a PM2.5 threshold of 35.5 µg/m³ | Case B — correct |
  |---|---|---|
  | `gen-shacl` output as generated | **Conforms: True** | Conforms: True |
  | the same shapes + a hand-written `sh:equals` | **Conforms: False** | Conforms: True |

  **The affirmative half is real.** *"Is this comparison well-typed?"* is
  a question that is not answerable today and that SHACL answers, with a
  usable message. That is a candidate satisfier for C5.

  **The condition on it is load-bearing and currently has no carrier.**
  `sh:equals` is not generable: `equals_expression` on the slot and a
  class-level `rules:` block were **both accepted, exit 0, empty stderr,
  and emitted zero cross-slot constructs** — reproduced here on all
  three variants (7 `sh:path` each, `sh:equals`/`sh:sparql`/`sh:lessThan`
  all 0). And the hand-written shape has nowhere to live: `make check`
  validates against `build/shapes.ttl` alone, `make gen` regenerates
  that file wholesale, invariant 1 forbids hand-editing anything under
  `build/`, and `sh:equals` occurs **0 times** in `docs/plan/`. No item
  produces a hand-maintained shapes file or a merge step.

  So C5's strongest candidate answer is demonstrated and unreachable
  through the pipeline as built. Recording it as satisfying C5 would
  record a capability the project cannot currently exercise. It stays
  `asserted`, and the gap is now named rather than implicit.

  C5 also remains **unfalsifiable as stated** — the sweep finding above
  is untouched by this experiment.

  **Carrier note, 2026-08-02 (plan-gate block verification 4).** Plan 01
  gains **P18**, *"decide how cross-slot constraints reach `make
  check`"*. It is a **decision** item, not a producing one: its three
  options are hand-written SHACL beside the generated file (breaks
  invariant 1), a generator emitting them from LinkML `annotations:`,
  and out of scope. So the carrier is now scheduled to be *decided* and
  is still not scheduled to be *built*, and one of the three outcomes
  removes it. `sh:equals` now occurs twice in `docs/plan/` — P18's row
  and the sentence recording this gap — and in no item's definition of
  done, because P18 has no definition of done (BV17). Status untouched
  in either direction.

  **Carrier decided, 2026-08-02 (design gate). Status unchanged, and it
  is the first time that is a statement about a schedule rather than
  about an unknown.** ADR-005 decides P18 as **option B**: cross-slot
  constraints are declared in LinkML `annotations:` and emitted as SHACL
  by a project generator running after `gen-shacl`. Option A was
  rejected on invariant 1, option C on the ground that it discards this
  claim's only affirmative evidence. So the shape that would satisfy C5
  is now decided and owned.

  **It is still not built, and the ADR records that rather than
  smoothing it.** The generator falls outside plan 01's scope statement
  and is filed as item **P19** with that reason stated. Until it exists,
  `exp-01`'s demonstrated answer stays unreachable through the pipeline,
  which is the condition recorded above and the reason the status does
  not move. Verified this gate that the gap is real rather than
  inherited: a class-level `rules:` block still emits zero cross-slot
  constructs at exit 0, run in ADR-003's shape (see C17, fourth
  measurement of axis 3).

  ADR-005 also states three testable properties for the resulting
  two-producer `build/shapes.ttl` — additive, order-independent,
  byte-deterministic — with `make gen` twice plus `diff` as the test.
  Those are obligations of P19, not evidence for C5.

  **2026-08-02, block verification — P19's load grew, and the added load
  is of a shape ADR-005 has never demonstrated a carrier for. Status
  unchanged.** ADR-003's second amendment withdraws its own enforcement
  argument and routes the epistemic-kind constraint here: *"the
  cross-slot constraint is ADR-005's P19."* That constraint is a
  **conditional** — if `procedure` is simulation-typed then
  `epistemicKind` must be `modelled`. Every piece of affirmative
  evidence under this claim is about **`sh:equals`**, which relates two
  slots by equality: `exp-01`'s demonstrated catch, the `us_aqi` /
  PM2.5 substitution, and the two first test cases ADR-005's Obligation
  names. A conditional needs `sh:condition` or `sh:sparql`, and the
  measurement recorded above found **`sh:condition` 0, `sh:sparql` 0**
  emitted from the source language.

  ADR-005's *decision* is generic — "cross-slot constraints" — and can
  be read to include conditionals. Its *evidence* is not, and its
  Obligation's test list does not name this constraint. So the property
  option B traded a module boundary away for is now deferred to a
  carrier whose demonstrated capability does not cover it. Filed as B6
  at the block-verification gate. This does not falsify C5 and is not
  evidence for it; it enlarges what P19 must do before C5 can move.

  **2026-08-02, block verification 2 — I tried to break the disposition
  and could not. B6's answer is now measured rather than inferred.**
  ADR-005 was amended to record that misassignment is unenforced
  **indefinitely**, with P19 a *candidate* remedy rather than a
  scheduled one, and to require a third test — a conditional between two
  slots, declared in `annotations:`, emitted and firing under
  `make check`. H nominated that "indefinitely" as the most attackable
  thing in its message, on the ground that if a conditional **is**
  emittable then P19 is a real remedy and the word is too strong.

  I ran it. Both routes — a class-level `rules:` block with a genuine
  `preconditions` / `postconditions` pair, and the `annotations:` carrier
  ADR-005 names — produce **exit 0, empty stderr, and zero
  `sh:condition`, zero `sh:sparql`, zero `sh:equals`** in the generated
  Turtle. See C17's fourth axis for the measurement. **The falsifier H
  named does not fire**, so "indefinitely" survives as stated and the
  third test is a real obligation rather than a formality.

  This is evidence *about P19's difficulty*, not evidence for C5. Status
  unchanged. It does mean the enlargement recorded above is not a
  scheduling problem that P19 dissolves — nothing in the source language
  currently expresses the constraint at all.

  **2026-08-02, block verification 3 — re-run by a second O session, and
  the falsifier still does not fire. Status unchanged.** Both routes
  reproduce at exit 0 with empty stderr and all three constructs at zero,
  with the annotation carried at slot level as well as class level. One
  addition to the record: enumerating the emitted predicates rather than
  counting named ones shows the annotation leaves **no trace whatever**
  in the generated Turtle. That bears on P19's shape — the generator
  ADR-005 decides on cannot be a post-processor over `build/shapes.ttl`,
  because its input is not present there; it must read the LinkML source.
  Stated as a measured consequence of the decision, not as a proposal
  about how to build it.
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

  2026-08-04, implement gate — **a counterexample to the second clause is
  scheduled, not yet present. Status unchanged because nothing is defined
  yet.** `design/surface.yaml:25` binds `sosa:hasMember`, and `:39` binds
  `sosa:ObservationCollection`; both are in ADR-004's generated worklist
  (16 bound slots, 13 class bindings) and land in **Part 2** at P7.
  Fetched from `https://www.w3.org/TR/vocab-ssn-ext/`: `sosa:hasMember`
  has domain `ObservationCollection`, range `Observation` **or**
  `ObservationCollection`, and is a **sub-property of `rdfs:member`** —
  a whole-to-member relation that nests. It carries **no interval**,
  which ADR-002 Decision C calls non-negotiable for `partOf`.

  So on the day Part 2 is authored, a part-whole relation is defined
  outside Part 0 unless someone decides it is not one. **Nothing in the
  readable tree has looked:** `hasMember` occurs three times in total —
  `surface.yaml` and ADR-004's two generated lists — and is discussed
  nowhere. This is the homonym question C8's own **Watch** field raises,
  arriving from an external vocabulary rather than from a hand-written
  signature, which is why a signature-name grep could not see it.
- **Updated:** 2026-08-04
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

  **A fourth candidate, named 2026-08-02 (design gate), and it is the
  first one grounded in material rather than in argument. Status
  unchanged, deliberately.** `FALSIFIER.md` §5.1 question 11 asks
  whether a narrative statement curated by a person is distinguishable
  from an observation. `docs/sources/HDC-data-source-register.html`
  **category 10 — "Curated content — written, not fetched"** is exactly
  that: `places.js` carries 27 burn-scar narratives, 10 year narratives,
  15 great burns and named landscapes, under the rule *"Honest data,
  never fabricated … researched and written, never invented to fill a
  gap."*

  A curated narrative fits none of observed, modelled, intended or
  mandated. It is not a prediction, not an order, not a plan, and not a
  sensing result — it is a person's researched interpretation, and its
  governing rule is a *sourcing* discipline rather than a modality.

  **Status is not moved, and the reason is the defect this entry already
  records.** Whether a curated narrative is an "operational statement an
  emergency management system makes" is precisely the adjudication C10
  supplies no procedure for. Ruling it in would falsify C10 by a
  judgement the claim leaves to whoever is defending it, which is
  requirement 2 failing in the falsifier's favour instead of against it.
  Filed as a named candidate so the next attempt starts from material.
  Under the restatement proposed above, the test is whether the
  narrative decomposes into modality-carrying statements; my reading is
  that it does not, and that is an argument, not an experiment.
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
- **Repair test:** P9's criterion, run: all three absence semantics and
  all three sentinel channels round-trip distinguishably through
  `make check` against a real capture. **A green `make check` with no
  absent-valued fixture is not the test.**
  *(H proposed 2026-08-05; O disposed and wrote it 2026-08-05. The
  wording is H's. Filing it does not promise the repair.)*
- **Updated:** 2026-08-05
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

  **Carrier decided 2026-08-02 (design gate). Status unchanged, and the
  reason it does not move is the point.** ADR-004 Decision B creates a
  Part 0 `Statement` class specifically to carry the four slots that had
  none — `sourceVerificationTier`, **`operatingMode`**, `modelVersion`,
  `profileConformance` — and names this claim as the strongest single
  argument for the decision: *"a discriminator that must sit on every
  assertion needs a class that **is** the assertion."* A decided carrier
  is not a field. `vocab/core/` holds one `.gitkeep`, so the Evidence
  above is still literally true and C12 stays `falsified`.

  **`docs/coverage.md` has not caught up, and it is the row this claim
  is about.** `coverage.md:303` still reads
  `Exercise / test / live discriminator | Dispatcher training simulator mode | — | GAP`
  — `Home` column `—`, meaning no carrier in the design. The same holds
  for the other three slots of Decision B at `:57`, `:306` and `:307`.
  The `GAP` statuses are right; the four `—` Home columns contradict a
  decision accepted in the commit that last edited the file. Filed as B5
  at the block-verification gate.

  **B5 cleared 2026-08-02, verified by diff on `520ddde`.** All four
  rows now carry `Part 0 Statement (ADR-004 B)` in the `Home` column and
  read **`GAP` — carrier decided, slot not authored**, including `:303`,
  which is this claim's own row. `docs/coverage.md` also gained a note
  stating that a carrier is not a slot and that *"reading a Home column
  as evidence of a slot is how `covered` got applied to the gap-filling
  row."* Checked that the four slots the note names —
  `sourceVerificationTier`, `operatingMode`, `modelVersion`,
  `profileConformance` — are exactly the four ADR-004 Decision B names.
  They are.

  **Status stays `falsified`.** `vocab/core/` holds one `.gitkeep`; no
  `operatingMode` field exists, so the Evidence above is still literally
  true. The bookkeeping defect is closed; the gap is not.
- **Known limitation, recorded 2026-08-05 — the second half of this
  claim is out of reach of every instrument this project has.** *"No
  consumer can render exercise or test data as actual"* is a
  **presentation** property. Validation sees instances, not rendering,
  so no `make check`, no SHACL shape and no Datalog stratum can observe
  it. This is [L6](#l6)'s position exactly — L6 already carries *"this
  covers derivation only, not presentation … do not cite this claim as
  covering the product property"* — and C12 has made the same kind of
  claim since 2026-07-31 without such a note. **Do not cite C12 as
  covering the rendering property.**
- **Repair test:** `build/shapes.ttl` carries an `sh:path` for
  `operatingMode`, **and** a capture tagged exercise raises a violation
  when validated as live. The slot alone is [C15](#c15)'s test, not
  C12's. **This test reaches the first half only** — the discriminator
  and the validation behaviour — and by the limitation above nothing
  can reach the second.
  *(H proposed 2026-08-05 and amended it the same day; O disposed and
  wrote it. The wording is H's.)*
- **Disposal 2026-08-05 — H proposed `scoped-down`; O holds
  `falsified`, and the reason is the status definition rather than the
  substance.** H's diagnosis is accepted in full and is what the
  limitation above records. But `scoped-down` means *"falsified as
  originally stated; **a narrower version survives**"* — and the
  narrower version does not survive either. `vocab/core/` holds one
  `.gitkeep`; no `operatingMode` field exists, so the surviving half is
  **unbuilt, not tested**. Recording it as `scoped-down` would assert a
  survival no run supports, which is the shape of H's own objection —
  *filing a test that reaches half a claim and calling the claim
  repaired* — moved up one level to the status field. C12 becomes
  `scoped-down` when the first half passes its Repair test, not before.
- **Updated:** 2026-08-05
- **Consequence:** ranked gap #1. **Safety-critical and free to fix —
  and this attaches to the discriminator half only.** The rendering
  half is not free to fix and is not fixable here at all; it is a
  consumer obligation this vocabulary can support but cannot enforce.

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

  **BV2 round 3, 2026-08-02 (plan-gate block verification 3). The tie
  still does not tie, and this time it is machine-checked.** BR-7
  replaced the conjunction with `RecordedNotDeleted merge rel :=
  ∀ a b x y, rel x y → a x → a y → merge a b x ∧ merge a b y`, asserting
  that it "quantifies the relation over the merge, so `corrects` and
  `supersedes` must be about the merged fact set rather than sitting
  beside it." **That is false, and the refutation is three lines:**

  ```lean
  theorem recorded_is_implied_by_monotone_for_any_rel {F : Type}
      (merge : FactSet F → FactSet F → FactSet F)
      (hm : Monotone merge) (rel : F → F → Prop) :
      RecordedNotDeleted merge rel :=
    fun a b x y _ hx hy => ⟨hm a b x hx, hm a b y hy⟩
  ```

  `Monotone merge` implies `RecordedNotDeleted merge rel` for **every**
  `rel`. The `rel x y` hypothesis is never used. So the predicate
  constrains the merge and constrains the relation not at all, which is
  the same defect one level down: the second and third conjuncts of
  `AdequateC13` are discharged by the first property of `merge` alone.

  **BV2's original scenario re-run against the new definition, and it
  survives verbatim** — using H's own `Bool` relations from
  `distinguishes_does_not_give_monotone`, which have nothing to do with
  any fact set:

  ```lean
  theorem bv2_scenario_still_satisfies_adequate :
      AdequateC13 (fun (a b : FactSet Bool) => fun f => a f ∨ b f)
        (fun x _ : Bool => x = true) (fun x _ : Bool => x = false) := ...
  ```

  Both elaborate against the committed `Merge.lean` under
  `lake env lean`, no `sorry`, no error, with a deliberately false
  control (`(0:Nat) = 1`) confirming the elaboration is real.

  Smaller, same section: `Distinguishes corrects supersedes` and
  `Monotone merge` quantify over disjoint variables, so neither *could*
  imply the other and "neither half implies the other" is not a
  property of the pair. `distinguishes_does_not_give_monotone` closes
  the direction BR-5 overreached on and the overreach is corrected, but
  what the two theorems jointly establish is weaker than independence —
  it is that the conjuncts share no subject.

  **BV2 round 4, 2026-08-02 (plan-gate block verification 4). The third
  tie collapses the same way the second did.** `RecordedNotDeleted` is
  retained in the file as a refutation, correctly, and `AdequateC13` is
  restated as `Distinguishes corrects supersedes ∧ PreservesDistinction
  merge corrects supersedes`, where `PreservesDistinction` requires the
  witnesses to be facts present in a set and to survive merging. PA40
  argues that this ties the three subjects because all three appear in
  it. They appear in it; they are not tied by it.

  ```lean
  theorem preserves_is_implied_by_monotone_for_any_relations {F : Type}
      (merge : FactSet F → FactSet F → FactSet F)
      (hm : Monotone merge) (c s : F → F → Prop) :
      PreservesDistinction merge c s := by
    rintro a b ⟨⟨x, y, hx, hy, hc, hs⟩, ⟨u, v, hu, hv, hs', hc'⟩⟩
    exact ⟨⟨x, y, hm a b x hx, hm a b y hy, hc, hs⟩,
           ⟨u, v, hm a b u hu, hm a b v hv, hs', hc'⟩⟩
  ```

  **`Monotone merge` implies `PreservesDistinction merge c s` for every
  pair of relations.** The witnesses satisfying `DistinguishesIn a` are
  carried into `merge a b` by monotonicity alone; `c` and `s` are never
  inspected. BV2's scenario therefore satisfies the new `AdequateC13`
  verbatim, using H's own unrelated `Bool` relations and
  `union_merge_monotone`. Both elaborate against the committed
  `Merge.lean` under `lake env lean`, no `sorry`, no error, with a
  `(0:Nat) = 1` control confirming the harness errors.

  `retracting_merge_loses_distinction` does bite, and by the
  contrapositive of the theorem above it entails
  `retracting_merge_not_monotone`, which `Merge.lean:211` already
  proves. It exhibits a **non-monotone merge** — a fact about `merge`.
  So for every merge this design contemplates, conjunct 2 is free and
  `AdequateC13` remains `Distinguishes ∧ (a property of merge alone)`,
  which is BV2's original objection at round 1.

  **The file's recorded limit is the useful half and it is accurate:**
  nothing at this abstraction can discharge C13, because `corrects` and
  `supersedes` are parameters. C13 is discharged by an implementation
  exhibiting the condition for its own merge and its own relations, and
  `transform/` is one `.gitkeep`. That was equally true of attempts one
  and two.
- **Repair test:** two instances differing only in whether the earlier
  fact was wrong or the world changed validate to **different** shapes.
  `design/lean/HazardVocab/Merge.lean` records C13 unclosable at its
  abstraction, so this test is against the schema, not the proof.
  *(H proposed 2026-08-05; O disposed and wrote it 2026-08-05. The
  wording is H's.)*
- **Updated:** 2026-08-05
- **Note:** L5 is not wrong, but it is incomplete. Do not withdraw it —
  add correction as a second, distinct relation.

### C14 — Every fact carries a releasability determination
Sensitivity, sharing restriction, and sovereign data governance are
expressible.

- **Status:** `falsified`
- **Evidence:** no sensitivity dimension exists. Every fact implicitly
  assumes publishability.
- **Repair test:** a capture carrying a sharing restriction round-trips
  it through `make check`, and one violating it raises a violation.
  **Expressible is not the claim** — the claim is that the
  determination travels with the fact.
  *(H proposed 2026-08-05; O disposed and wrote it 2026-08-05. The
  wording is H's.)*
- **Updated:** 2026-08-05
- **Note:** this is a dimension, not a row. Likely a Part 0 relation
  over `Statement`, not a slot on each class.

### C15 — Instances declare their model version and profile
An instance is self-describing with respect to which vocabulary version
and which profile it conforms to.

- **Status:** `falsified`
- **Evidence:** not modelled.
- **Repair test:** `build/shapes.ttl` carries `sh:path` for
  `modelVersion` and `profileConformance`, and an instance declaring a
  profile it does not conform to **fails**. Both slots are in
  `surface.yaml` under `not_enumerated_by_a1` as of I1.
  *(H proposed 2026-08-05; O disposed and wrote it 2026-08-05. The
  wording is H's. O confirmed both slots appear under
  `not_enumerated_by_a1` — `make lint` reports `4 not enumerated`.)*
- **Updated:** 2026-08-05
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
- **Repair test — and it is a sweep, not a command.** C16 is discharged
  by a sweep returning nothing, so **the field must name what was
  swept**, not only that it came back empty: the payloads read, the
  register categories covered, and the date. A discharge recorded as
  *the sweep returned nothing* is indistinguishable from *the sweep
  inspected nothing*, which is this register's most frequent finding
  ([C22](#c22)) — and it is how C16 was falsified in the first place,
  its three row sources being unable to see what they did not contain.
  `make lint`'s own honest line is the model: *"no schema files found —
  these rules inspected nothing."* The falsifying observation remains a
  capability found in a real payload or in
  `docs/sources/HDC-data-source-register.html` that `docs/coverage.md`
  has no row for.
  *(H proposed 2026-08-05 and amended it the same day after O ruled the
  field could not be a command; O disposed and wrote it. The wording is
  H's.)*

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

  **Third axis, added 2026-08-02 by P15 and reproduced independently by
  O. It is the sharpest of the three. LinkML accepts a constraint
  expression and emits no shape for it.**

  | Source construct | `gen-shacl` | `sh:path` | cross-slot constructs emitted |
  |---|---|---|---|
  | baseline, no constraint | exit 0 | 7 | 0 |
  | `equals_expression: "{thresholdProperty}"` on the slot | **exit 0**, empty stderr | 7 | **0** |
  | class-level `rules:` block, same postcondition | **exit 0**, empty stderr | 7 | **0** |

  Checked for `sh:equals`, `sh:sparql`, `sh:disjoint` and `sh:lessThan`;
  all zero in every variant. The gap is **not** expressive poverty in the
  target language — SHACL Core carries `sh:equals`, and hand-adding it to
  the generated shapes rejects the bad instance and passes the good one
  (see C5).

  All three axes fail toward "pass". Axes 1 and 2 leave an artifact that
  can be inspected — a context that omits a key, a shape whose datatype
  contradicts the bound term. **Axis 3 leaves none:** the author writes
  the constraint, the generator accepts it without warning, and the
  constraint is simply absent from the output. This is the case where
  the work was done and the belief that it is in force is wrong.

  **Incidental, confirmed by running it, and it lands on P8a.** LinkML
  `float` generates `sh:datatype xsd:float`; an untyped JSON-LD numeric
  expands to `xsd:double`. Every numeric in a fixture then raises
  `DatatypeConstraintComponent` — *"Value is not Literal with datatype
  xsd:float"*, pointing at the datatype rather than at the `@context`
  that caused it. P8a authors that context by hand.

  **Fourth measurement of axis 3, 2026-08-02 (design gate). Status
  unchanged; what is new is that the constraint is now a *decided*
  design rather than a probe.** ADR-003 chose option B and made a
  required `epistemicKind` slot the replacement for the Part 2 / Part 3
  module boundary, with an obligation reading *"no instance carries an
  `epistemicKind` inconsistent with its `procedure`."* That is a
  cross-slot constraint. Run in exactly that shape — one `Observation`
  class, required `epistemicKind` with a closed enum, `procedure` bound
  to `sosa:usedProcedure`, and a class-level `rules:` block requiring a
  simulation procedure to carry `modelled`:

  | Construct | Emitted |
  |---|---|
  | required slot + closed enum | `sh:minCount 1`, `sh:in ( "observed" "modelled" )` |
  | `rules:` tying `procedure` → `epistemicKind` | `sh:equals` 0, `sh:sparql` 0, `sh:lessThan` 0, `sh:disjoint` 0, `sh:condition` 0 |

  Exit 0, empty stderr, no warning (linkml 1.11.1 from `.venv`). Then
  both instances through pyshacl 0.40.1 against those generated shapes:
  an instance carrying `epistemicKind "observed"` with
  `usedProcedure "simulation"` **conforms**; only the omission case
  raises `MinCountConstraintComponent`.

  **So the generated shape catches omission and not misassignment**, and
  misassignment is the property the module boundary carried — ADR-003's
  own words, *"under A, a Part 3 fact in a Part 2 file is visible on
  inspection."* ADR-005, accepted in the same gate, defers the generator
  that would emit the cross-slot form to P19, outside plan 01. Recorded
  because axis 3 has until now been measured on throwaway schemas; this
  is the first time a decision of record depends on it.

  **Fourth axis, 2026-08-02, block verification 2 — the conditional
  specifically, on both routes ADR-005 names.** Axis 3 measured
  `equals_expression` and a `rules:` block carrying a postcondition.
  This measures the exact constraint ADR-003 now depends on — *if
  `procedure` is simulation-typed then `epistemicKind` must be
  `modelled`* — declared as a class-level `rules:` block with a real
  `preconditions` / `postconditions` pair, and separately in
  `annotations:`, which is the carrier ADR-005's Obligation names:

  | Source construct | `gen-shacl` | stderr | `sh:condition` | `sh:sparql` | `sh:equals` |
  |---|---|---|---|---|---|
  | `rules:` with `preconditions` + `postconditions` | **exit 0** | empty | **0** | **0** | **0** |
  | `annotations:` carrying the conditional as text | **exit 0** | empty | **0** | **0** | **0** |

  In both cases the generated `NodeShape` carries only the two property
  shapes with `sh:datatype`, `sh:maxCount` and `sh:path`. **The rule
  vanishes with no warning**, and the annotation text does not survive
  into the shapes file at all. linkml 1.11.1, `gen-shacl`, verified by
  reading the emitted Turtle rather than by exit code.

  **Method note against myself.** My first pass counted `sh:or` and
  `sh:node` with a substring grep and got 2 each — both artifacts:
  `sh:or` matched `sh:order` and `sh:node` matched `sh:nodeKind`. Re-run
  with word boundaries, every count is 0. That is the
  instrument-reports-something-it-did-not-inspect shape in my own
  measurement, caught before it reached this register.

  **Replicated 2026-08-02, block verification 3, by a second O session
  that did not inherit the run above.** Both routes reproduce exactly —
  exit 0, empty stderr, `sh:condition` / `sh:sparql` / `sh:equals` all
  **0** — with the annotation carried at **class level and slot level**
  rather than class level alone. Enumerating the emitted predicates
  rather than counting named ones: the graph contains only
  `sh:targetClass`, `sh:property`, `sh:path`, `sh:datatype`,
  `sh:maxCount`, `sh:nodeKind`, `sh:order`, `sh:closed`,
  `sh:ignoredProperties` and `sh:description`. Grepping the Turtle for
  the constraint text returns one hit and it is an unrelated slot
  `description`. Replication recorded because the axis is what ADR-003's
  Obligation and ADR-005's third test both rest on, and it had been
  measured once by one session.
- **Repair test:** `make check` raises a violation on a captured payload
  carrying a field the model does not declare. `exp-01` measured the
  four axes; **axis 2 is the one a repair must move**, and a pass on
  axes 1, 3 and 4 is not C17.
  *(H proposed 2026-08-05; O disposed and wrote it 2026-08-05. The
  wording is H's.)*

  **2026-08-07 — axis 2's first instance in authored vocabulary rather
  than on a probe schema, two occurrences, both confirmed by running
  pyshacl 0.40.1 against `build/shapes.ttl`.** Until now axis 2 was
  measured on scratch files built to make it fire. P6a bound four
  external terms and two of the bindings contradict the published term,
  checked against this repository's own cached graphs rather than
  against documentation:

  | Slot | `slot_uri` | Published declaration | Emitted shape |
  |---|---|---|---|
  | `asWKT` | `geo:asWKT` | `owl:DatatypeProperty`, `rdfs:range geo:wktLiteral` — `graphs/geosparql.ttl:687-691` | `sh:datatype xsd:string` — `shapes.ttl:148` |
  | `hasBeginning` | `time:hasBeginning` | **`owl:ObjectProperty`**, `rdfs:range time:Instant` — `graphs/owl-time.ttl:735-741` | `sh:nodeKind sh:Literal`, `sh:datatype xsd:dateTime` — `shapes.ttl:306-310` |
  | `hasEnd` | `time:hasEnd` | **`owl:ObjectProperty`**, `rdfs:range time:Instant` — `graphs/owl-time.ttl:768-774` | `sh:nodeKind sh:Literal`, `sh:datatype xsd:dateTime` — `shapes.ttl:300-304` |

  **The `asWKT` case is falsified by the slot's own example.** Validating
  the value at `part0-entity-core.yaml:230`, typed as GeoSPARQL requires,
  raises `DatatypeConstraintComponent`: *"Value is not Literal with
  datatype xsd:string"*. ADR-004 Decision A's stated ground — *the CRS
  travels inside the `wktLiteral`* — is the thing the generated shape
  forbids.

  **The OWL-Time cases are a contradiction rather than a narrowing**, and
  that is a distinction axis 2 had not yet exhibited. A local range can
  legitimately be tighter than a published one. `sh:nodeKind sh:Literal`
  on an `owl:ObjectProperty` is not tighter — the shape *requires*
  exactly what the published term *forbids*, so no instance can satisfy
  both. A `time:Instant`-valued instance raises both
  `NodeKindConstraintComponent` and `DatatypeConstraintComponent`.
- **Updated:** 2026-08-07
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
  | `https://w3id.org/ohim/` | exit **1** — shared redirect, path not allowlisted |
  | `https://ohim.org/ns/` | exit **1** — host not a known generic vocabulary host |
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

  **Round 5, 2026-08-02 — a seventh counterexample, and it is the first
  one this register has recorded that was *introduced by a fix*. Status
  unchanged.**

  The sixth counterexample (BV8, round 4) was a precision failure: the
  `jurisdiction` rule ran `check_uri` over every `prefixes:` entry, so no
  namespace this project could choose was admitted and the first Part 0
  file the project authored for itself could not pass `make lint`. That
  is now fixed in `scripts/drift-lint.py` by a self-reference exemption,
  with `scripts/lint-fixtures/own-namespace.yaml` as a precision fixture;
  `lint-selftest` reports **23 rule/fixture pairs, 6/6 rules with
  demonstrated recall** (the 22 / 20 figures above are superseded, not
  wrong when written). Verified by running all three BV8 namespaces —
  `w3id.org/ohim/`, `ohim.org/ns/`, `example.org/hv/` —
  which previously all fired and now all exit 0.

  **The exemption keys on `default_prefix`, and that is a recall hole
  that reopens closed counterexample c1.** The guard builds its
  self-reference set from `id:` *and* from whatever namespace
  `default_prefix` points at, then exempts any URI with that prefix. So
  the F13 case, closed in round 2, passes again on a one-line change:

  | File | `default_prefix` | `irwin: https://w3id.org/nwcg/irwin/` | Result |
  |---|---|---|---|
  | c1 replay | `hv` | on a slot's `slot_uri` | **exit 1** — fires, correct |
  | identical content | **`irwin`** | same slot, same URI | **exit 0, all five rules `ok`** |

  C18's falsifier is *"a jurisdiction-specific scheme that passes all
  five rules."* It does. This is a **recall** failure — the worse
  direction, and the one that fails silently — arriving as the direct
  consequence of repairing a precision failure, with a fixture written
  for the precision direction and none for the recall direction.

  The general shape, since it is the second instance this week: a
  precision fix narrows what a rule inspects, and a fixture that
  demonstrates the narrowing was correct does not demonstrate that
  nothing else fell through it. `lint-selftest`'s 6/6 counts recall per
  *rule*, not per *exemption*.

  **Round 6, 2026-08-02 — the round-5 hole is closed and an eighth
  counterexample sits one field over. Status unchanged.**

  The `default_prefix` route is fixed **— superseded by round 7 below,
  which reopens it: "agrees with" is a two-directional prefix match, so
  `default_prefix` still exempts any ancestor of `id:`**: it is now
  honoured only when it agrees with
  `id:`, `scripts/lint-fixtures/default-prefix-escape.yaml`
  is committed as the recall fixture, a sixth rule `documented` has
  landed (see C20), and `lint-selftest` reports **26 rule/fixture pairs,
  7/7 rules with demonstrated recall** (the 23 / 22 / 20 figures above
  are superseded, not wrong when written). Verified by running, and the
  shipped fixture fires on the c1 URI as it should.

  **`id:` is the primary source of the exemption set and is as
  unconstrained as `default_prefix` was.** A schema declaring the
  jurisdiction's own namespace as its identity passes every rule:

  ```yaml
  id: https://w3id.org/nwcg/irwin/core
  default_prefix: irwin
  prefixes: {irwin: https://w3id.org/nwcg/irwin/}
  slots:
    incidentIdentifier:
      description: Identifier issued for an incident under some scheme.
      examples: [{value: "2026-OR-ABC-000123"}]
      slot_uri: irwin:IrwinID
  ```

  **All six rules `ok`, exit 0.** C18's falsifier is *a
  jurisdiction-specific scheme that passes all the rules*; this is one,
  and a `vocab/core/` file with that `id:` is exactly what invariant 2
  forbids.

  The general form, since this is the second consecutive round of it:
  **a self-reference exemption sourced from the document under
  inspection can be claimed by any document.** The file declares what
  counts as its own namespace. Constraining one field that feeds the
  exemption set leaves the other, and the fix for a recall hole was
  again tested only in the direction it closed.

  **Round 7, 2026-08-02 — ninth counterexample. The repair for BV19 is
  inert, and BV14's route is open again in one line.** The declaration
  was moved out of the schema into `scripts/project-namespaces.txt`,
  whose header states that the project's namespaces are declared there
  "where a schema author cannot edit it as part of authoring a schema",
  and that if the file is missing "NO namespace is treated as the
  project's own ... the guard fails loud rather than open."

  **`PROJECT_NAMESPACES` is assigned at `scripts/drift-lint.py:119` and
  never read.** `grep -rn PROJECT_NAMESPACES scripts/` returns the
  assignment and nothing else. §4 mutation test — the file was moved
  away and the suite re-run:

  | With `project-namespaces.txt` | absent |
  |---|---|
  | `make lint` | `lint ok`, unchanged |
  | `make lint-selftest` | 27 pairs, 7/7, unchanged |
  | `own-namespace.yaml` (precision) | `ok`, unchanged |

  Output identical in every case, so the guard is not about that file.
  The fail-loud sentence in its header is false in both directions: the
  file changes nothing whether present or absent. `drift-lint.py:292`
  still reads `SELF IS DERIVED FROM `id:` ALONE` — the exemption is
  sourced from the document under inspection, which is exactly what
  BV19 identified as unfixable from inside the file.

  **And `default_prefix` re-widens the exemption to any ancestor of
  `id:`.** The agreement test at `drift-lint.py:311` matches in *both*
  directions (`dp_uri.startswith(o) or o.startswith(dp_uri)`), so a
  `default_prefix` naming a parent of the schema's own `id:` adds that
  parent to `own`. Two files differing by one line:

  | File | `jurisdiction` |
  |---|---|
  | `id: .../nwcg/irwin/core`, prefix `irwin: .../nwcg/irwin/` | **FAIL**, exit 1 |
  | the same **plus** `default_prefix: irwin` | **`ok`, exit 0** |

  The shipped fixture `id-claims-foreign-namespace.yaml` fires only
  because it omits `default_prefix`. The project's own precision fixture
  `own-namespace.yaml` carries `default_prefix: hv`, so the exempting
  shape is the ordinary one and the detected shape is the unusual one.
  Third consecutive round in which the repair for a recall hole leaves
  the same hole one field over. `scripts/` is human-owned; reported,
  not edited.

  **Round 8, 2026-08-02 — the repair landed and works. The tenth
  counterexample is that one of the three fixtures certifying it does
  not exercise what it is named for.** Round 7's two defects are both
  closed, verified by mutating the linter rather than reading it:

  | Mutation of `scripts/drift-lint.py` | Effect on `lint-selftest` |
  |---|---|
  | `_project_namespaces()` returns a hardcoded list when the file is absent | ` FAIL [jurisdiction] project-namespaces.txt is inert` — **the selftest's own §4 mutation case fires** |
  | drop `under_project` on the `default_prefix` branch | `default-prefix-escape` **and** `default-prefix-ancestor` both stop firing |
  | reinstate the two-directional agreement test | **no change** — `own` is now empty for a foreign `id:`, so the ancestor route is closed by the `id:` gate, not by the agreement test's removal |
  | drop `under_project` on the `id:` branch | **no change, 28 pairs, 7/7** |
  | **delete the `id:` branch entirely** | **no change, 28 pairs, 7/7** |

  The first three are the repair holding. The last two are the finding.
  All three namespace fixtures — `default-prefix-escape.yaml`,
  `id-claims-foreign-namespace.yaml` and `default-prefix-ancestor.yaml`
  — fire on one identical message:

  ```
  prefix `irwin` declares namespace `https://w3id.org/nwcg/irwin/` on
  `w3id.org`, which is a public permanent-identifier redirect
  ```

  That is F13's redirect rule, not the self-namespace exemption. Two of
  the three are nonetheless bound to the exemption, because exempting
  the `default_prefix` URI suppresses that same message. The third,
  labelled *"recall — BV19, `id:` nominating a foreign namespace"*, is
  not: the schema's `id:` is a **descendant** of the prefix namespace it
  declares, so adding the `id:` base to `own` never exempts the prefix.
  Its firing is independent of the branch it certifies.

  **The `id:` branch is load-bearing; only its test is not.** A probe
  with a foreign `id:` that declares no foreign *prefix* —
  `id: https://w3id.org/nwcg/irwin/core`, class and slot URIs under it,
  `prefixes:` carrying `linkml` only — exits **1** on the shipped code
  and **0** with the `under_project` gate removed. That is BV19's real
  escape and no fixture covers it.

  So `7/7 rules with demonstrated recall` remains true at rule
  granularity and overstates the case at branch granularity: the
  guard-clause the round-7 repair added has no test that would notice
  its deletion. Same family as the four defects above — an instrument
  reporting coverage it does not have — and the reason it survived is
  the one this entry keeps recording: the fixture was checked for
  *firing*, not for *firing because of the thing under test*.
  `scripts/` is human-owned; reported, not edited.

  **2026-08-07 — the rules have now inspected a real authored file, and
  the green is not empty.** `vocab/core/` held one `.gitkeep` until
  `prefixes.yaml` landed; every prior clean `make lint` was the
  inspected-nothing case, and each of the eight `drift-lint.py` rules now
  reports `1 file(s)` over content nobody wrote to make it fire. What that
  covers, measured rather than inferred: against a P6a-shaped schema whose
  class and slot carry real `sosa:` CURIEs, `declared-prefix` fires on a
  prefix used and not declared (exit 1, both the `class_uri` and the
  `slot_uri` branch) and `jurisdiction` fires on `nwcg:` added to the map;
  `documented` passes a real documented file with examples. So recall is
  demonstrated on authored material for two rules and precision for one.
  **Status stays `falsified`** on the hole recorded above — the
  `sosa-TYPO` mutation still exits 0 over exactly this file.

  **Scope correction on the phrase "all nine rules", which is O's wording
  as much as H's.** `drift-lint.py` has **eight** rules and `make lint`'s
  ninth is `lean-vacuity`, in `scripts/lean-lint.py`, scoped to
  `--include='*.lean'`. It cannot inspect a YAML prefix map, so *"passes
  all nine rules"* — in `prefixes.yaml`, in `items.yaml:63` and in the two
  prior `[O → H]` messages — is true of a `make lint` run and false of any
  claim about what inspected the file. Not a finding against this round's
  work; recorded so the number stops propagating.

  **2026-08-07 — the `jurisdiction` recall hole has now admitted real
  content, which is the first time any hole in this register cost the
  vocabulary rather than a fixture.** `IRWIN` appears three times and a
  national scheme URI once in `vocab/core/part0-entity-core.yaml`, all
  four inside `examples:` blocks, and `make lint` exits **0**. The rule
  inspects class, slot, enum and permissible-value **names**; an example
  value is not a name. See C1, now `falsified`.

  **The rule behaved exactly as documented and the failure is still
  C18's.** The 2026-08-01 entry above records this hole in advance, so
  nothing about the instrument changed. What changed is that
  `vocab/core/` acquired the `examples:` blocks that invariant 7 makes
  mandatory — so the position C1 content is now least likely to be
  caught in is the position the project's own documentation rule forces
  every element to carry.
- **Updated:** 2026-08-07
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

  **2026-08-06 — the material now exists, and the first exercise against
  it splits.** `vocab/core/prefixes.yaml` is the first authored file the
  nine rules have ever inspected; `make lint-selftest` reports 43
  rule/fixture pairs and 9/9 rules with demonstrated recall, reproduced.
  Mutating the real file rather than a fixture: adding a
  jurisdiction-namespaced prefix fires `jurisdiction` (exit 1), and
  dropping a prefix a slot uses fires `declared-prefix` (exit 1) in a
  P6a-shaped single-file schema. Both are real firings on real material,
  which is what this entry says has never happened.

  **Status stays `falsified`, on the case the same experiment found.**
  Corrupting a declared namespace — `sosa:` →
  `http://www.w3.org/ns/sosa-TYPO/` — passes all nine rules at exit 0,
  both as the prefix map alone and as a schema whose class and slot
  carry `sosa:` CURIEs. `declared-prefix` asks whether a used prefix is
  declared and never whether it is right, so the recall hole survives
  the stage that was expected to close it. See C1's 2026-08-06 entry.
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

### C20 — Every class and slot is documented, and lint enforces it
Every class and slot in `vocab/` carries a `description` and an
`examples` entry, and `make lint` fails when one does not.

- **Status:** `scoped-down`
- **Falsifier:** a schema file with a class or a slot lacking either a
  `description` or an `examples` entry that `make lint` accepts.
- **Evidence:** 2026-08-02 — **falsified on the enforcement half at the
  first attempt.** `CLAUDE.md` invariant 7 states *"Every class and slot
  needs a `description` and an `examples` entry. Lint enforces it."*
  Nothing enforces it.

  `make lint` runs exactly three things: a `grep` for
  `structured_pattern|classification_rules` (C4), `scripts/lean-lint.py`
  over `design/lean` (the vacuity rule), and `scripts/drift-lint.py`
  over `vocab/core/`. `drift-lint.py`'s five rules are
  `inline-attributes`, `is-a-depth`, `exact-mappings`, `role-named` and
  `jurisdiction`. **None inspects `description` or `examples`**;
  `grep -rn examples scripts/*.py Makefile` returns one hit, inside a
  comment.

  Counterexample run: a Part 0 candidate declaring eight classes and
  twelve slots, every `description` the literal string `TODO` and **not
  one `examples` entry anywhere**, passes `drift-lint.py` clean — five
  rules `ok`, exit 0 — and `gen-shacl` emits its shapes at exit 0.

  **Consequence, and it is why this is worth a register entry rather
  than a note.** P6a's definition of done includes *"the core validates
  under `make lint`"*. That clause does not carry invariant 7, so the
  first real Part 0 file can be declared done undocumented. The
  invariant's own stated justification — *"Free documentation and
  grounding for both humans and models"* — is what C6 (LLM-legibility)
  rests on, and C6 has no other guard.

  The claim is filed as two halves because they can fail separately: the
  documentation half is untestable while `vocab/` is empty, and the
  enforcement half is falsified now.

  **Enforcement half repaired, 2026-08-02 (plan-gate block verification
  4). Scoped down.** `scripts/drift-lint.py` gained a sixth rule,
  `documented`, checking every entry under `classes:` and `slots:` for a
  non-placeholder `description` and a non-empty `examples`; `CLAUDE.md`
  invariant 7 was rewritten by its owner to name that rule instead of
  asserting enforcement in the abstract. Declared by H under the tooling
  rule (PA38) and **verified by running**, not read:

  | Probe | Result |
  |---|---|
  | the original counterexample — 8 classes, 12 slots, `TODO`, zero `examples` | **40 FAILs, exit 1** |
  | descriptions real, class has `examples`, **slot has none** | fires on the slot alone |
  | `examples` everywhere, one description `"TBD."` | fires on the description alone |
  | fully documented | `ok` |

  Probed in each direction separately rather than through the committed
  fixture, which carries both faults at once — C18 round 5's lesson is
  that a fixture demonstrating one direction demonstrates one direction.

  **The narrower version that survives:** *`make lint` fails when a
  class or a slot in an inspected schema file lacks a `description` or
  an `examples` entry, or carries a placeholder description.*

  **The full claim is not `tested`, and the difference is the word
  "inspected".** The documentation half — that every class and slot in
  `vocab/` *is* documented — remains untestable: `vocab/core/` is one
  `.gitkeep`, and `make lint` prints *"no schema files found — these
  rules inspected nothing."* The rule is demonstrated against
  constructed probes, never against the material. Same caveat C18's
  recall note carries: a guard that has never inspected the material is
  not yet known to guard it. Re-examine when `vocab/core/` has content.
- **Promotion note:** promoted by O under FALSIFIER §6 at the plan-gate
  block verification 3, 2026-08-02. It generalises beyond the gate — it
  is about the repository's guard set rather than about plan 01 — and no
  existing entry covers it: C18's falsifier names C1, C4 and the vacuity
  rule, and invariant 7 is none of the three. Entering directly as
  `falsified` rather than `asserted` follows C17's recorded precedent
  (the counterexample preceded the claim); the deviation from the
  register's "new claims enter as `asserted`" rule is recorded here
  rather than left silent. **`CLAUDE.md` is human-owned — invariant 7 is
  reported, not edited.**
- **Updated:** 2026-08-02

---

## External class bindings

*(added by O at the design gate, 2026-08-02)*

### C21 — Distinct schema elements assert distinct external identity URIs
No two schema elements in `vocab/core/` assert identity to the same
external URI, by any identity-asserting construct — `class_uri`,
`slot_uri`, `exact_mappings`, `same_as`, or `PermissibleValue.meaning`.
Where two elements are both kinds of one external term, the relationship
is expressed by something other than asserting that term's URI on both.
`close_mappings`, `related_mappings` and `narrow_mappings` are outside
the claim, because none asserts identity.

*(Restated 2026-08-02 at block verification 5, from H's proposal at the
design gate. The previous wording — "no two classes in `vocab/core/`
carry the same `class_uri`" — is superseded, not withdrawn: it was true
and remains true, and is a strict special case of this. This is a
widening, not a weakening; nothing that failed the old statement passes
the new one. See the block-verification-5 evidence block for what the
guard does and does not enforce of it.)*

*(Widened again 2026-08-03 at block verification 6, from H's proposal —
third time in the same direction. `same_as` and `PermissibleValue.meaning`
join the construct list, and permissible values join the falsifier's
population, which had excluded them entirely while `meaning` is the
route `CLAUDE.md` names to every SKOS code list. The prior wording said
"by any construct" and then gave a closed list of three, which was
self-contradictory as written. Adopted on the ground that the claim is
about the vocabulary; guard coverage is evidence, not content.)*

- **Status:** `asserted`
- **Falsifier:** two **distinct elements** in `vocab/core/` — classes,
  slots, or permissible values, in any combination — asserting the same
  external URI via any of `class_uri`, `slot_uri`, `exact_mappings`,
  `same_as` or `PermissibleValue.meaning`; or a generated
  `build/shapes.ttl` containing one `sh:NodeShape` whose
  `sh:targetClass` is an external URI and whose property shapes come
  from more than one declared class. One element naming one URI through
  two constructs is redundant, not a collision — it asserts identity
  with itself.
- **Cheapest test:** `gen-shacl`, then count `sh:NodeShape` against
  count of `classes:`. Seconds, once `vocab/core/` has content.
- **Evidence:** 2026-08-02 — **the claim is untested against the
  material, because `vocab/core/` holds one `.gitkeep`. What is measured
  is the consequence of violating it, and it is why this entry exists.**

  Two classes declared with `class_uri: prov:Entity`, everything else
  distinct, through `gen-shacl` (linkml 1.11.1, `.venv`):

  ```
  prov:Entity a sh:NodeShape ;
      sh:property [ sh:minCount 1 ; sh:path ex:sourceVerificationTier ],
                  [ sh:minCount 1 ; sh:path ex:title ] ;
      sh:targetClass prov:Entity .
  ```

  **One shape, carrying the union of both classes' property shapes, each
  still `sh:minCount 1`.** Exit 0, empty stderr, no warning. The two
  classes are indistinguishable to validation, and each class's required
  slots become required of the other's instances. The same file with
  `exact_mappings: [prov:Entity]` instead emits two shapes with local
  `sh:targetClass` — but that is the construct ADR-002's own addendum
  identifies as *"assert[ing] class equivalence, which is the false
  claim"*.

  **Nothing in the guard set inspects this.**
  `scripts/drift-lint.py:238` documents `exact-mappings` as *"at most
  one `exact_mappings` per class"* — per-class by construction, so one
  URI shared by two classes is outside its subject rather than a recall
  failure of it. Run against both probes: `ok [exact-mappings]
  2 file(s)`.

  **Live at the design gate, which is why this is promoted rather than
  left as a gate finding.** ADR-002 Decision A binds `Document` to
  `prov:Entity`; ADR-004 Decision B binds `Statement` to `prov:Entity`.
  Neither states which LinkML construct *"binds to"* denotes, and
  `measure-01` A2 records that *"LinkML takes one `class_uri`"*. P6a
  authors Part 0 next and must choose; one choice fails silently.

  **A guard for this landed mid-review, 2026-08-02, and is verified.**
  `scripts/drift-lint.py` gained an eighth rule, `shared-uri`, with
  `scripts/lint-fixtures/shared-class-uri.yaml`; `make lint-selftest`
  reports **32 rule/fixture pairs, 8/8 rules with demonstrated recall**
  (the 29 / 7-of-7 figure recorded elsewhere is superseded, not wrong
  when written). Verified by running each direction separately rather
  than through the selftest: it FAILs on two classes sharing
  `class_uri: prov:Entity`, reports `ok` when one is moved to
  `prov:Bundle`, and its slot branch FAILs on two slots sharing
  `slot_uri: sosa:observedProperty`. `scripts/` is human-owned;
  discovered rather than declared, and reported, not edited.

  **2026-08-04, block verification 7 — the guard's subject is literal
  URI strings, and subsumption is outside it by construction.**
  `rule_shared_uri` collects claims with `claims.setdefault(str(uri), …)`
  and compares keys. It never fetches an external vocabulary, so a
  subclass axiom published elsewhere is invisible to it. Probed, with a
  control:

  | Probe | Result |
  |---|---|
  | `Place` → `sosa:FeatureOfInterest`, `Hazard` → `deo:Hazard` (`deo:Hazard ⊑ sosa:FeatureOfInterest` upstream) | **`ok [shared-uri]`, exit 0** |
  | control — both classes → `sosa:FeatureOfInterest` | **FAIL**, names both classes |

  This bounds the claim rather than weakening it: C21 is about two
  elements asserting *the same* URI, which is what the guard measures.
  What it does not measure is two elements asserting URIs an external
  ontology relates by subsumption, and no entry should be read as
  covering that. Recorded because `ADR-006:84` asserted the opposite —
  see C23 #7.

  **The slot branch has no fixture.** Every file in
  `scripts/lint-fixtures/` was parsed and its `class_uri` and `slot_uri`
  values counted: exactly one duplicate exists in the suite, and it is a
  `class_uri` duplicate. No fixture carries a duplicate `slot_uri`, so
  no pair exercises that branch and its deletion would change no
  reported result while `lint-selftest` continued to print 8/8. Same
  family as C18 rounds 5–8 — coverage claimed at rule granularity that
  does not hold at branch granularity.

  **Status stays `asserted`.** The guard means a violation would now be
  caught rather than silent; it is not evidence that the claim holds,
  because `vocab/core/` still has no classes to check and the design as
  accepted currently plans to violate it.

  **2026-08-02, block verification — the slot branch is now established
  by mutation rather than by coverage enumeration, and the class branch
  with it.** The earlier attempt failed because `--linter` and
  `DRIFT_LINT=` are not supported options, so both invocations silently
  ran the real linter. The route that works is to copy the whole
  `scripts/` tree, because `lint-selftest.py` resolves its linter path
  relative to its own `__file__`. Baseline on the copy reproduces
  `32 rule/fixture pairs, 8/8`. Then, one branch deleted at a time:

  | Mutation | `make lint-selftest` on the copy |
  |---|---|
  | delete `dupes("classes", …, "class_uri")` | **FAILED** — `FAIL [shared-uri] shared-class-uri.yaml`, a NAMED test notices |
  | delete `dupes("slots", …, "slot_uri")` | **`ok — 32 rule/fixture pairs, 8/8`** — nothing notices |

  The class branch meets `scripts/lint-fixtures/README.md`'s convention.
  The slot branch does not, and the finding stands as recorded above —
  now on mutation evidence, which is what the convention asks for.

  **ADR-004 Decision D does not resolve the collision this entry
  records.** It decides that `Statement` carries
  `class_uri: prov:Entity` and that the abstract `Entity` carries no
  external `class_uri`. No document proposed binding the abstract
  `Entity` to `prov:Entity`; the pair recorded above is `Document`
  (ADR-002 Decision A, table row, unamended) and `Statement` (ADR-004
  Decision B). Probed both readings of that pair against the shipped
  linter:

  | Probe | Result |
  |---|---|
  | `Document` and `Statement` both `class_uri: prov:Entity` | **FAIL [shared-uri]** — names both classes and the merge consequence |
  | `Document` via `exact_mappings: [prov:Entity]`, `Statement` via `class_uri` | `ok [shared-uri]`, `ok [exact-mappings]`, **exit 0 on both** |

  So the guard fires on the vocabulary the two accepted ADRs literally
  declare, and does not fire on the mixed-construct reading — which is
  the construct ADR-002's own addendum calls *"the false claim."* The
  sentence above — *"the design as accepted currently plans to violate
  it"* — is unchanged by this gate.

  **2026-08-02, block verification 2 — both halves of the entry above
  are now superseded, and one of them was mine and wrong.**

  *The slot branch is covered.* `scripts/lint-fixtures/shared-slot-uri.yaml`
  exists and declares two slots — `assertedTime` and `recordedTime` —
  both carrying `slot_uri: prov:generatedAtTime`. Re-ran the mutation on
  a fresh copy of `scripts/`, which reproduces `33 rule/fixture pairs,
  8/8` before mutation:

  | Mutation | `lint-selftest` on the copy |
  |---|---|
  | delete `dupes("classes", …, "class_uri")` | **FAILED** — `FAIL [shared-uri] shared-class-uri.yaml` |
  | delete `dupes("slots", …, "slot_uri")` | **FAILED** — `FAIL [shared-uri] shared-slot-uri.yaml` |

  The table recorded above — slot branch deletable with no effect — is
  **no longer true of the shipped linter**, and the row reading
  `ok — 32 pairs, 8/8` is superseded rather than corrected, because it
  was an accurate measurement of a tool that has since changed. Both
  branches now fail a **named** test when deleted, which is what
  `lint-fixtures/README.md`'s convention asks for.

  *The design no longer plans to violate the claim.* ADR-004 Decision D
  decides `Document` carries `class_uri: foaf:Document` and nothing
  else, and **ADR-002's table row was amended in the same commit**
  (`520ddde`) — verified by diff, not by report: the row now reads
  `foaf:Document` where it read `prov:Entity, foaf:Document`. The
  `Document` / `Statement` collision this entry recorded is resolved in
  the design, with `prov:Entity` on `Statement` alone.

  Status stays `asserted`: `vocab/core/` still holds one `.gitkeep`, so
  there is still no vocabulary to check and nothing has been verified
  against a generated `build/shapes.ttl`. What changed is that the guard
  is now demonstrated on both branches and the design it guards no
  longer contains a known counterexample.

  **2026-08-02, block verification 3 — the design is resolved, the guard
  is not, and ADR-004 says it is.** Re-ran the mixed-construct probe
  against the shipped linter with a control, on schemas complete enough
  that no unrelated rule fires:

  | Schema | `scripts/drift-lint.py` |
  |---|---|
  | `class_uri: prov:Entity` on **both** `Document` and `Statement` *(control)* | **FAIL `[shared-uri]`**, exit 1 |
  | `Document`: `class_uri: foaf:Document` **+ `exact_mappings: [prov:Entity]`**; `Statement`: `class_uri: prov:Entity` | **exit 0 — all seven rules `ok`** |

  The cause is structural rather than a recall failure, read from source:
  `rule_exact_mappings` (`scripts/drift-lint.py:237-255`) fires only on
  `len(m) > 1`, and `shared-uri` compares `class_uri` values only.
  **No rule compares an `exact_mappings` target against another class's
  `class_uri`**, so the reversion route is invisible to the whole guard
  set.

  This matters because ADR-004 Decision D closes at `:277` with
  *"**Guarded rather than remembered**"*, while `:258-261` of the same
  decision records that the mixed construct passes both rules. The
  artifact contains both statements; the summary is the one that
  overreaches, and it is the sentence a reader takes the decision from.
  Filed as blocking finding BV3-3.

  Status stays `asserted` for the reason above — nothing is authored, so
  the claim is still untested against material. What is now measured is
  that the state this entry was written about is reachable without any
  instrument objecting.

  **2026-08-02, block verification 4 — the guard closed, and it
  invalidated sentences in this entry as well as in ADR-004.**
  `rule_shared_uri` now collects identity URIs from `class_uri`/
  `slot_uri` **and** `exact_mappings` into one map keyed by URI
  (`scripts/drift-lint.py:462-486`), landed in `c5f25b5`. Re-ran the
  mixed-construct probe and added the construct BV3 did not probe:

  | Schema | shipped `scripts/drift-lint.py` |
  |---|---|
  | `Document`: `class_uri: foaf:Document` + `exact_mappings: [prov:Entity]`; `Statement`: `class_uri: prov:Entity` | **FAIL `[shared-uri]`**, exit 1 — names both holders and the construct each used |
  | `exact_mappings: [prov:Entity]` on **both**, one each *(new probe)* | **FAIL `[shared-uri]`**; `ok [exact-mappings]` |

  Branch-mutated per §4 on a scratch copy: deleting the two-line
  `exact_mappings` collection flips `mixed-construct-identity.yaml` from
  **FAIL to `ok`**, so the fixture reaches that code and nothing else
  does. `make lint-selftest` reports **35 rule/fixture pairs, 8/8**.

  **Two statements in this entry are superseded, not corrected** — each
  was an accurate measurement of a tool that has since changed:

  - *"Nothing in the guard set inspects this"* (above, block-verification
    -3 block) — `shared-uri` now inspects exactly this.
  - the probe row reading `ok [shared-uri] … exit 0 on both` — now
    FAILs.
  - the figure **32 rule/fixture pairs**, and the later **33**, are both
    superseded by 35.

  **The claim is now narrower than the rule that cites it.** C21 as
  stated forbids two classes carrying the same `class_uri`;
  `rule_shared_uri` also fires on `exact_mappings` identity and its
  failure message cites *"claims.md C21"* while doing so. The guard
  enforces more than the register claims. Recorded as a finding for H to
  propose a restatement against; O does not restate claims.

  Line references in the block-verification-3 entry above (`:258-261`,
  `:277`) no longer resolve — the sentences they name are at ADR-004
  `:274-277` and `:293`.

  Status stays `asserted`. `vocab/core/` still holds one `.gitkeep`, so
  there is still nothing authored to check and no generated
  `build/shapes.ttl` to count shapes in. A guard widening is not evidence
  the claim holds.

  **2026-08-02, block verification 5 — the restatement is adopted, and
  the guard enforces less of it than the previous wording implied.**
  H proposed the widening at the design gate and it is taken: the claim
  is about the vocabulary, and identity by `exact_mappings` is the same
  defect as identity by `class_uri`.

  **But adopting H's rationale verbatim would have inverted the very
  mismatch it was raised to close.** H's ground was *"the guard enforces
  more than the register claims."* That was right for `exact_mappings`
  within one population and wrong as a general statement. Probed the
  shipped `scripts/drift-lint.py` against the restatement's own
  falsifier — *two elements doing so that the guard passes* — on schemas
  clean enough that no unrelated rule fires:

  | Probe | `[shared-uri]` | exit |
  |---|---|---|
  | two classes, both `class_uri: prov:Entity` *(control)* | **FAIL** | 1 |
  | a **class** via `class_uri` + a **slot** via `exact_mappings`, same URI | `ok` | **0** |
  | a class via `class_uri` + a class via **`same_as`**, same URI | `ok` | **0** |
  | two **`PermissibleValue.meaning`** values, same URI | `ok` | **0** |

  Cause, read from source: `rule_shared_uri`
  (`scripts/drift-lint.py:461-486`) calls its `collect` helper **twice
  with a fresh `claims` dict each time** — once over `classes`/`class_uri`,
  once over `slots`/`slot_uri`. The two maps never meet, so a cross-population
  collision is outside its subject by construction. `same_as` and
  `PermissibleValue.meaning` are collected by no rule at all, and
  `meaning` is the construct `CLAUDE.md` names as the route to every SKOS
  code list.

  So the register and the guard are still not the same shape — the
  direction has reversed. That is recorded here rather than fixed in the
  claim, because the claim is about the vocabulary and the guard's
  coverage is evidence, not content. `scripts/` is human-owned; reported,
  not edited.

  Status stays `asserted`, for the reason it has stayed `asserted`
  through four block verifications: `vocab/core/` still holds one
  `.gitkeep`. Nothing is authored, so the widened claim is no more tested
  against material than the narrow one was. Restating a claim is not
  evidence for it.

  **2026-08-03, block verification 6 — the three gaps recorded above are
  closed in the guard, established by mutation rather than by reading.**
  `rule_shared_uri` now collects all five constructs into **one** map
  (`scripts/drift-lint.py`), so cross-population collisions are inside
  its subject. Four one-branch mutations on a byte-identical copy of the
  tree, control green before and after each:

  | Mutation | Named row that failed |
  |---|---|
  | claims keyed by `(population, uri)` — **the repair reverted** | `collision-class-vs-slot`, `collision-same-as` |
  | `same_as` collection deleted | `collision-same-as` |
  | `PermissibleValue.meaning` loop deleted | `collision-permissible-meaning` |
  | `exact_mappings` collection deleted | `mixed-construct-identity`, `collision-class-vs-slot` |

  All four killed **by name**, which is what `lint-fixtures/README.md`'s
  convention asks for and what the previous round could not show: three
  of the same four mutations survived at green when the collisions were
  bundled into one fixture. `make lint-selftest` reports **39
  rule/fixture pairs, 8/8**; 24 fixtures on disk, 24 referenced, no
  orphans.

  **Status still `asserted`.** The guard is now demonstrated; the claim
  is still untested, because `vocab/core/` still holds one `.gitkeep`.
  A working instrument is not evidence for the proposition it would
  measure.
- **Updated:** 2026-08-04
- **Promotion note:** promoted by O under FALSIFIER §6 at the design
  gate, 2026-08-02. It generalises beyond the gate — it is about the
  vocabulary and its generator rather than about these four decisions,
  and it binds on every future external class binding, not only on
  `prov:Entity`. No existing entry covers it: C7 is about class *names*
  that denote roles, C18's falsifier names C1, C4 and the vacuity rule,
  and the `exact-mappings` rule is scoped per-class. Enters as
  `asserted` per the register rule, since no counterexample exists in
  `vocab/core/` yet — unlike C17, T3, T4 and C20, this is not a
  deviation.
- **Note:** the claim as stated forbids the collision and does not
  prescribe the alternative. Whether two core classes that are both
  `prov:Entity` should relate to it by `is_a`, by a mixin, by
  `exact_mappings`, or by one of them not binding it at all is a design
  question and is H's. This entry only asserts that assigning both the
  same `class_uri` is not it.

### C22 — An instrument is not evidence until it has been probed against its own failure mode
An instrument this project relies on is not evidence until it has been
probed adversarially against its own failure mode. A guard shipped
without a falsifier is the same artifact class as a claim shipped
without one, and is subject to the same rules.

**An instrument that happens to be right is not a working instrument.**
A harness that reaches the correct verdict by a mechanism that never
reproduces the defect it is testing for has not tested anything, and its
green is indistinguishable from a green earned honestly. That criterion
is in the statement rather than in a note, because it is what makes the
instances below countable at all.

- **Status:** `asserted`
- **Falsifier:** any instrument admitted to the build on the strength of
  a green run, whose named guard clause can be deleted without a **named**
  test going red; or an instrument whose passing run does not exercise
  the mechanism of the defect it is invoked to detect.
- **Cheapest test:** delete one clause, run the harness, read *which* row
  fails. Seconds.
- **Evidence:** 2026-08-04, extended 2026-08-05 (twice), 2026-08-06
  (four times) and 2026-08-07 (three times) — **twenty-eight instrument
  defects, thirteen files, three authors.** Nineteen manifested; two were
  self-caught before shipping, and seven — rows 17, 19, 24, 25, 26, 27 and
  28 — are coverage gaps that have not yet cost anything. All are counted
  because the register counts defects **in instruments**, not defects that
  caused visible harm.

  *The file count was incremented by the one instrument rows 26–28
  introduce — `scripts/sweep-retracted.py` with `retracted.txt` and
  `sweep-fixtures/`, counted as one as row 17 counted `guard-fixtures/` +
  `guard-mutate.py`. It was **not** re-derived from rows 1–25. Said so
  rather than restating a figure I did not check, which is the defect the
  paragraph above this table already confesses.*

  **This count read *twenty-one* while the table carried twenty-two rows.**
  O added row 22 on 2026-08-06 and did not restate the total above it —
  F15's defect, a count in a paragraph disagreeing with the enumeration
  under it, committed by the role that has now filed it against H twice
  (C23 rows 13 and 14). Corrected here rather than silently.

  | # | Instrument | Defect | Author | Found by |
  |---|---|---|---|---|
  | 1 | `Makefile` `make check` | `**` matched one directory level under `sh` | H | running it |
  | 2 | the SHACL measurement | substring matching counted `sh:or`/`sh:node` artifacts | O | running it |
  | 3 | `scripts/` edit script | the `is_blocked` replacement silently deleted `strip_heredocs` | O | running the matrix, not reading the diff |
  | 4 | `lint-selftest` + fixtures | `shared-uri`'s slot branch deletable at 8/8 green | O | mutation |
  | 5 | `design/derive-surface.py` | the restatement guard fired on **retractions** | H | probing against the correction discipline |
  | 6 | `cross-population-identity.yaml` | three of four branch mutations survive, incl. the repair reverted; one bundled fixture spends its single exit-code bit on whichever collision survives | O | mutation |
  | 7 | zsh control | could not exhibit the bug it was invoked to confirm | O | reading the mechanism against the result |
  | 8 | `design/derive-surface.py` | matched **digits** only; three word-cardinalities stood, all wrong | H | a control run against a section nobody was editing |
  | 9 | staleness test | searched for a filename where the table renders stems | H | mutation |
  | 10 | the C21 mutation harness | merged the two maps back before filtering, so it **never reproduced the defect** it reached the right verdict on | H | the result not following from the mechanism |
  | 11 | `lint-selftest` `expect` | accepted on a precision row and never evaluated — a field that cannot fire | H | adding one that could not appear |
  | 12 | the retracted-string sweep | keys on the **sentence**, not the proposition. Invoked to detect a withdrawn claim still standing elsewhere; a claim **restated in different words** is its failure mode. **Three** shipped past a green run — `ADR-003:34-39`, `ADR-006:284-288` and `ADR-003:188-192`, all in accepted ADRs, all at lines a reader takes as authoritative | H | the first two by O reading the retracted claims against the files rather than against the strings; the third by the **paraphrase sweep** proposed to replace it, on its first run |
  | 13 | `.claude/hooks/guard_role.py` recursive-traversal fix | admitted on a green run against `grep -r .`; **three invocations of the grep family it names walk through it** — `grep -R`, `rg` with no root argument, and any absolute-path root. None is the disclosed `find`-pipe residual | human | O, by mutation with `-l` output |
  | 14 | `docs/plan/derive-waves.py` `check_retired` — P20's retired-figure guard | admitted on a 12/12 hand probe, every probe **one line of lowercase prose**. Two ordinary variations of its input walk through it: the guard is **line-based** over a document hard-wrapped at ~72 columns (7 of 8 wrapped phrasings pass, including **all four** sizing phrases), and `RETIRED_PHRASES` carries **no `re.IGNORECASE`** while `SIZING_PHRASES` does, so sentence-initial `The 23`, `The ten` and `Ten local terms` pass. **Both manifested**: `plan:385` and `plan:876`/`:904` carry the retired population at a green `make lint` | H | O, by mutation — wrapping and capitalising the phrasings the 12/12 probe had run on one line |
  | 15 | `docs/plan/derive-waves.py` `check_retired` — **the repair for #14** | joining wrapped lines into blocks fixed the shape blindness and moved the **exemption** to the block with it. `items.yaml` contains **no blank line**, so the whole file is one block, that block carries a retraction cue, and the guard now exempts **the entire source file**: 6 of 6 retired figures injected into it are caught by the pre-repair guard and **0 of 6** by the repaired one. In the plan document the same shift exempts both generated tables outright — cue-exempt lines rise 98 → 287 of 1174. A figure injected into `items.yaml`, propagated by `--write` into the item table of the plan of record, leaves `--check` reporting **ok** | H | O, by mutation — running both builds of the guard over the same injections |
  | 16 | `vocab/external/fetch-external.py --check` — documented as *"verify the CACHE only; no network"* | the verification mode **overwrites the record it verifies.** It rewrites all 24 provenance sidecars with `http_status: cache`, `dereferences: skipped`, `disposition: untested` and a fresh `fetched:` stamp, then regenerates `register.md` from them: 15 bound / 7 borrowed / 1 untested becomes **23 untested**, exit 0, `## Problems — *(none)*`. The dispositions are network measurements and are not recoverable offline | H | O, by mutation — running the documented command against a copy and diffing the register against the committed one |
  | 17 | `docs/plan/guard-fixtures/` + `guard-mutate.py` — **the fixture matrix built to close row 14** | the matrix covers the half of `check_retired` that **matches** and none of the half that **exempts**. Deleting each of the guard's ten clauses in turn: four redden a named fixture, six redden nothing. Four of those six are load-bearing — the backtick strip, the asterisk-quote strip, the prose bare-quote strip and the blockquote skip — each turning a firing case into an exempt one, and each **deletable with no named test going red**, which is this claim's falsifier verbatim. The three fixtures named for them are green through the **retraction-cue** path rather than the strip path: every one carries a cue as well as a quotation, so the clause they are named for never decides the verdict. `re.I` on `SIZING_PHRASES` is uncovered for the same reason — `b1-sizing-wrapped.md` asserts its phrase in lowercase. `guard-mutate.py` records the fifth of these as an expected `set()` and reports **5/5** above it | H | O, by deleting all ten clauses rather than the five the shipped matrix mutates |
  | 18 | `vocab/external/fetch-external.py` `sync_register()` — the main register table | the row emitter writes **six cells under a five-column header**. Introduced by the F14 repair at `be7d243`, which added the `Why` cell to the row format string and not to the header: 5/5 at `3ddc721`, 6/5 at `be7d243` and at `f00f027`. GFM ignores cells past the header, so in every rendered view the **`Disposition` column displays the free-text `detail`** — *"301, and the redirect target did not serve a graph"* under a heading reading *Disposition* — and the actual disposition, `bound` / `borrowed` / `untested`, is **dropped from all 35 rows**. That is the distinction `vocab-conventions.md` says decides what a binding is worth, and the register is where it is recorded. Every instrument that admitted the repair is green either way: the 3/3 mutation set and `assert sum(rtally.values()) == len(rows)` both operate on raw strings and tallies, `--check` reports `## Problems — *(none)*`, and no fixture covers the generator at all | H | O, by counting the cells the generator emits against the columns it declares |
  | 19 | `vocab/external/fetch-external.py` `check_tables()` — **the instrument built this round to close #18** | it reports clean over a table that has a header, a separator and **no data rows**. The arity comparison is per row, so a table with none is a table with nothing to compare, and the function returns `[]` — the same value it returns for a correct table. That state is reachable and it writes: with the `.ttl` cache absent and the 36 sidecars present, `rows` is empty while `failed` and `orphans` are not, so the `if not rows and not failed and not orphans` bail — whose own comment says *"a register written from nothing would be an empty table reporting zero problems"* — does not fire. Measured end-to-end through `main()` with `curl` stubbed to fail: process exit 1, and `register.md` **rewritten** to a main table of a header, a separator and zero rows, tallied *"0 graphs with a sidecar; . 35 fetch(es) produced no graph at all"* — an empty distribution between the `;` and the `.`. `--check` over that file then returns **rc=0**: no arity problem, and no drift, because the emptied file is byte-identical to what the generator now emits | H | O, by running the generator with the cache moved aside |
  | 20 | `vocab/external/audit-bound-terms.py` — the sibling generator of the tracked file `vocab/external/bound-terms.md` | three defects, and the file is a generated file of record carrying *"Generated by `audit-bound-terms.py`. Do not edit."* **It is not in `make lint`** — `grep -c audit-bound-terms Makefile` returns 0 — so A1's repair, which put the *register* generator into the build, left a second generator in the same directory that nothing invokes. **Its `--check` writes the file it verifies**, unconditionally at the last line of `main()`: row 16's defect, one file over, still live. And **its output is not byte-reproducible** — three consecutive runs give three digests, because `sosa:hasMember`'s `rdfs:range` is a blank node and the cell carries rdflib's per-parse label (`n74b7ef59…`, `n3f6680bf…`, `n4bd913f2…`). The committed file already differs from what the generator emits in exactly that cell, so the drift instrument the register gained this round can never be pointed at this file | H | O, by enumerating tracked `*.py` against the `Makefile` and running the one that was missing, three times |
  | 21 | `make lint`'s **B** stanza + `vocab/external/audit-bound-terms.py` — **the repair for #20** | row 20 put the generator into `make lint`; the stanza it was given is **not cache-state aware**, and `grep -c 'cache_state\|CACHE_STATE\|unfetched'` over the script returns **0**. The X stanza beside it prints *"the cache is unfetched (4 cached, all of them tracked). This check inspected nothing."* — F19's ruling, closed one round earlier. The B stanza reports **drift** in that same state. Measured on a real `git clone`: `776e660` exits **0**, `b77e6a4` exits **2** with `bound-terms.md: DRIFTED from its generator — 41 line(s) differ, first at 21`. **Nothing drifted** — the cache is unfetched, so the audit reads 4 graphs instead of 35. The message asserts a tracked file of record is wrong, and it routes to a write that destroys it: running the generator on the clone takes `bound-terms.md` from **29 term rows to 0** — *"0 object properties of 0 terms audited"*, 38 lines deleted — returning exit 1 **and writing anyway**. `fetch-external.py` has the bail that prevents this (*"an emptied generator still equals itself"*, register NOT written); `audit-bound-terms.py` has none. **This is row 19 in the sibling generator**, arriving through the repair for row 20. The instrument was probed in one state of its input — H's populated working tree — where both declared mutation rows are correct | human (`Makefile`) + H (script) | O, by `git clone` + `make lint`, after discarding a first attempt whose `tar` copy into a non-git directory made `cache_state()`'s `git ls-files` misreport every stanza |
  | 22 | `vocab/external/audit-bound-terms.py` — **the repair for #21** | the repair is aware of exactly one cache state. `cache_state()` returns `unfetched | complete | partial`, and the new guard tests `== "unfetched"`; its docstring states that a **partial** cache "is not emptiness and stays caught", treating the third state as covered. What it is caught *as* is row 21 verbatim. Measured on a copy of `vocab/external/` with one fetched graph removed (`graphs/sosa.ttl`): `--check` exits **1** with `bound-terms.md: DRIFTED from its generator — 41 line(s) differ, first at 21` — the same string, the same false assertion that a tracked file of record is wrong, and nothing drifted. Following that message into the write path takes `bound-terms.md` from **29 term rows to 14** — *"4 object properties of 14 terms audited"* — exit **1 and written anyway**. The empty-bail added for row 21 is `if not rows:`, and 14 rows is not zero, so it covers total loss and not truncation. `partial` is reached by any single failed source fetch, an interrupted fetch, or deleting one graph to force a re-fetch. **Third instance of one defect across two sibling generators**, and the second to arrive through the repair for its predecessor | H | O, by removing one cached graph from a copy of `vocab/external/` and running both the check and the write path |
  | 23 | `vocab/external/audit-bound-terms.py` — **the repair for #22** | the repair bounds the row count and never reads a graph. `expected = sum(len(names) for _key, names in LOOKUP)` with `if len(rows) < expected` catches emptiness (row 21) and truncation (row 22), and a **present, parseable graph that defines none of its terms produces a FULL row count** — every lookup yields an `ABSENT` row, `len(rows) == expected == 29`, and the bail does not fire. Measured on a copy of `vocab/external/` with `graphs/geosparql.ttl` truncated to zero bytes: `--check` exits 1 with `bound-terms.md: DRIFTED from its generator — 10 line(s) differ, first at 44` — the same false assertion that a tracked file of record is wrong, and nothing drifted; the write path exits **1 and writes**, replacing GeoSPARQL's three real definitions with `ABSENT` and *"11 object properties"* with *"10 object properties of 29 terms audited"*. **The state is documented in the generated file's own header** — *"the GeoSPARQL namespace URI returns a Prez description document in which all four bound terms appear and none is defined. The manifest scored it 4/4; this audit found zero definitions"* — so a re-fetch from the namespace rather than the fetch URL reaches it, and `cache_state()` cannot see it because it compares filenames and reads no bytes. **Fourth instance of one defect across two sibling generators, and the third to arrive through the repair for its predecessor.** The clause is also **deletable with no named test going red** — this claim's falsifier verbatim: no fixture anywhere references `audit-bound-terms.py` or `bound-terms.md`, and with the clause removed `lint-selftest` still reports 43 pairs, 9/9 | H | O, by truncating one cached graph to zero bytes rather than removing it, and by deleting the clause and re-running the named harness |
  | 24 | `vocab/external/fetch-external.py` `DIGEST_PEER` — the guard the gate message offers as what *"keeps that sentence true"* for *"two URLs currently resolve to one body, revocably"* | **its green is entailed by the redirect standing, and it is blind to the one state its own rationale names.** `fetch()` runs `curl -sS -L`, so `adms.ttl` is fetched **through** the 307 and both cached bodies are two fetches of `https://uri.semic.eu/w3c/ns/adms.ttl`. Their `cmp` identity is therefore guaranteed by construction while the redirect stands, and measures nothing about `w3.org`. The rationale asserts the complement — *"If the 307 is withdrawn, w3.org begins serving a SECOND document and the guard fires"* — which assumes withdrawal implies divergence. Measured on a throwaway copy with the redirect withdrawn and the bodies left identical (`resolved_url` flipped to `same as source_url`): `sync_register()` returns **0**, silently, while the licensed sentence has degraded from *two URLs resolve to one body* to *two bodies that agree today*. That is the inference retracted in pass 1 — *`cmp`-identical bytes licenses two documents that agree today, not one document* — reappearing inside the guard offered as the retraction's support, one level up. The datum that would settle it is already captured and read by nothing: `resolved_url` is written to 37 of the 38 sidecars — all but `deo`, the orphan, which predates the field and has not been re-fetched — and appears in **no** check. Controls: true divergence by one appended line → `rc=1`; the peer graph removed → `rc=1`. So the guard detects post-withdrawal divergence only, which is the complement of the sentence it is cited for | H | O, by mutation on a copy — withdrawing the redirect with the bodies identical, then diverging them by one line and deleting the peer as controls |
  | 25 | `vocab/external/mutate-register.py` — **the file that ships this round's hardcoded-literal sweep** | its own headline figure is a hardcoded data literal. `print("\n%d/6 mutations behave as claimed" % (6 - len(bad)))` names the case count — a datum about the file — while the sibling probe derives the identical figure from `len(STATES)`. The gate message asserts *"What remains literal is behavioural only"* after sweeping five other sites in these two files, and this is the sixth. Measured by adding a seventh passing case exactly as a repair would: the run prints **`6/6 mutations behave as claimed`** while seven ran; with one failure among seven it would print `5/6`. The exit code is derived from `bad` and stays correct, so the defect is confined to the figure the gate message quotes — which is the figure O is asked to verify. **Fourth instance of the hardcoded-number class in one session**, in the file written to address that class rather than instance it | H | O, by adding a seventh case to a copy and reading the headline |
  | 26 | `scripts/sweep-retracted.py` + `sweep-fixtures/` — **the over-exclude direction, which the round declares as what the fixture pair is for** | the instrument guards the noisy direction and is blind to the silent one, and prints a green line naming the silent one. `inside-an-excluded-path.md` is **inert**: emptied to a single comment, and with its phrase deleted, `--selftest` still reports **2/2** and still prints `  ok   [sweep] inside-an-excluded-path.md — the OVER-EXCLUDE direction`. Only its *filename* is load-bearing, via an `exists()` check — **deletable content with no named test going red**, this claim's falsifier verbatim. And over-exclusion itself is undetectable: adding `vocab`, `docs` and `README.md` to `EXCLUDE` leaves sweep and selftest both at **rc=0** (`9 exclusions all present`) while a phrase planted in `docs/coverage.md` goes **unreported** — effective and invisible. The complement is loud: removing `claims.md` exits **1** on `claims.md:3129` immediately. `check_exclusions()`, the stated mitigation, catches only an exclusion naming a **nonexistent** path — the one over-exclusion that by definition silences nothing. The artifact also contradicts itself: `sweep-retracted.py:26-28` and `sweep-fixtures/README.md:16` state correctly that *no match-direction fixture can show this*, while `:30-33`, the printed label at `:207-209` and the gate message state that it is shown. **The honest sentence is in the file nobody reads at runtime; the overclaim is the line printed on every `make lint`** | human | O, by emptying the fixture, then by adding three exclusions over existing paths and planting into one of them |
  | 27 | `scripts/sweep-retracted.py` + the four entered phrases — **row 14's two defects, shipped verbatim in a new instrument built after row 14 was registered** | `git grep -F` is **line-based** and **case-sensitive**, over a corpus hard-wrapped at ~72 columns (ADR median 67, p90 72) — which is row 14's finding word for word, in a sibling guard in this repository, found by O by the same mutation one round earlier. Measured across all placements at W=72: **176/288 survive, so 39% of placements are MISSED** — per phrase 43/72, 37/72, 55/72, 41/72. Case: **two of the four entries begin with a lowercase word that is a natural sentence opener**, and both walk through — planted in a tracked file, `They are ONE document` and `One document by construction today` are **not reported**, while their lowercase forms are. Also missed: markup inside the phrase (`they are **ONE** document`), a double space, and a non-breaking space — eight near-miss forms planted, **eight missed, one verbatim control caught**. This is inside the instrument's stated scope: the header disclaims *paraphrase*, and `They are ONE document` is the same words in the same order. **The plant-verification table establishes only that `git grep -F` matches the bytes it was handed** — a plant of the exact byte sequence into a fixed-string matcher is a tautology, and it is row 14's *"12/12 hand probe, every probe one line of lowercase prose"* in a new file. Unlike row 14, **not yet manifested**: 0 wrap-hidden or case-hidden occurrences outside the exclusions, over all 172 tracked files with whitespace collapsed | human (instrument) + H (entries) | O, by wrapping and capitalising the phrasings the 4/4 plant probe had run on one line — row 14's method, re-applied |
  | 28 | `scripts/sweep-retracted.py` `phrases()` — the three clauses the round's S1–S4 mutation table is named for | **all three are deletable with no test going red.** Removing the comment-tab clause, the trailing-newline clause, and the tab-count clause each in turn leaves `sweep` and `--selftest` at **rc=0**. S1–S4 are manual states H ran once by hand, not fixtures in a harness: there is no matrix, no `expect` field, and `lint-selftest` does not reference this instrument at all. So the round's Proposal 1 — *a fixture that fires for the wrong CLAUSE of the right rule* — understates its own case; the clauses have **no named test to fire wrongly**, which is this claim's first disjunct rather than a new class, and row 17 already records the phenomenon of *"the clause they are named for never decides the verdict"* | human | O, by deleting each clause in turn and re-running both entry points |

  **None of the first seventeen was found by reading the instrument.**
  Fourteen were found by running it against a deliberate defect, one by
  running it against the file it was already guarding, one by noticing
  the verdict did not follow from the mechanism, and one — #12 — by
  checking the instrument's *subject* rather than its output: the sweep
  reported correctly on the strings it was given, and the claim it
  existed to find was standing in different words.

  **#18 is the first exception, and a narrow one.** It was not found by
  running the generator — every run of it is green, and that is the
  entry's whole content — but by measuring one part of its output
  against another: the cells each row emits against the columns the
  header declares. That is still a measurement rather than a reading,
  and it was the only form available, because the defect is invisible to
  every execution of the instrument and visible in one count over its
  product. **The register's own drift is invisible for the same
  reason:** regenerating from the committed sidecars into a throwaway
  copy shows the committed `register.md` is five lines behind its
  generator, and nothing reports it — `--check` reads only and prints
  `## Problems — *(none)*`.

  **#19 is #18's repair carrying #18's own blind spot into the next
  round, and the two are one shape at different scopes.** #18 was a
  header measuring a row set it did not describe; #19 is the measurement
  of that header against **an empty row set**, which passes by
  construction. The instrument was built to answer *did this table
  render what it declared* and it answers *did the rows it was given
  disagree with the header* — a question with no wrong answer when there
  are no rows. It is the failure direction `FALSIFIER.md` §4 names
  verbatim, an instrument reporting success when it has inspected
  nothing, occurring inside the instrument commissioned to close an
  instance of it. Both halves of the build agree: `check_tables()` is
  clean and the byte comparison is clean, because a generator emptied of
  input still equals itself.

  **#20 is what A1's closure did not reach.** A1 was stated about *the
  register generator* and closed about *the register generator*, and the
  invariant written into `CLAUDE.md` alongside it is stated about
  **every** generator. The tree has two in one directory; one is now in
  `make lint` and one is not, and the one that is not also carries a
  writing `--check` and a non-reproducible output. Nothing in the round
  distinguished the specific closure from the general invariant, and the
  census that separates them is one command.

  #10 is the entry that forced the criterion into the statement. It
  returned the right answer. Every other row is an instrument that was
  wrong; that one was *right, for no reason* — and had it not been
  caught, the repair it green-lit would have been admitted on a harness
  that could not have detected its failure.

  #11 is closed by `validate_cases()` in `scripts/lint-selftest.py`,
  verified this gate by mutation: an `expect` added to the precision row
  `near-miss-distinct-uris` is rejected at load on the default path, the
  `--table` path and the `--table --write` path. Under the previous build
  the same edit passed green.

  **#12 and #13 are the first two entries whose instrument is a
  *search*, and they fail the same way.** Both were admitted on a green
  run over the case their author had in mind — one retracted sentence,
  one `grep -r .` — and both are defeated by an ordinary variation of
  their input: the same claim in different words, the same recursion
  under a different flag. Neither was reached by reading the instrument;
  both were reached by asking what the instrument's subject is and then
  handing it something outside it. #13 is the register's first entry
  authored by the human, which is the reason the tooling-declaration
  rule requires a **second** instrument: the run that admitted it was
  the run that defined its coverage.

  **#12's third site, added 2026-08-04 at block verification 9.**
  `ADR-003:188-192` — *"That is what option B rests on"* — restates the
  proposition BV7-3 withdrew 40 lines below, shares no string with it,
  and survived three string sweeps. It was found by the **replacement**
  instrument on that instrument's first run, in the pass that proposed
  it, in text by the author proposing it. O re-ran the sweep
  independently over `design/ADR-00[1-6]`, `docs/` and this file — the
  content words surviving the paraphrase are `strongest`, `argues`,
  `rests`, `discriminat` — and it returned the two sites already marked
  and nothing further. **That run is a green, and a green is not
  evidence under this claim**: the paraphrase sweep is itself an
  instrument admitted on a run over the case its author had in mind, and
  its own failure mode — a restatement sharing no *content word* either,
  by synonym substitution — has not been probed. It is a candidate row,
  not a discharge of row 12.

  **Row 14, added 2026-08-05, is the third *search* instrument and it
  fails exactly as #12 and #13 did.** All three were admitted on a green
  run over the case their author had in mind — one retracted sentence,
  one `grep -r .`, twelve single-line lowercase reintroductions — and
  all three are defeated by an ordinary variation of their input. #14
  sharpens the pattern in a way the earlier two do not: its author
  **derived** the phrasings from a recorded enumeration command rather
  than remembering them, which is the discipline this project added to
  stop exactly this failure, and it still shipped blind — because the
  derivation fixed *which phrases* to look for and nothing fixed *how
  the document presents them*. **Deriving the subject of a search does
  not derive the shape of its input.**

  **It is also the first rule wired into `make lint` with no
  `lint-selftest` pair.** `make lint-selftest` enumerates 39 rule/fixture
  pairs across `drift-lint.py`'s 8 rules and reports `8/8 rules with
  demonstrated recall`; `check_retired` is a ninth rule in the same
  target and appears in none of them. Its 12/12 probe was a one-time
  hand run that left no residue in the repository, so nothing re-probes
  it and its coverage is asserted rather than inspectable — the
  condition `CLAUDE.md` cites `lint-selftest` as existing to prevent.

  **Row 15 is the first entry where the *repair* is the defect, and it
  is the cost of that missing pair, paid one round later.** #14 was two
  blind spots in what the guard could see; #15 is the fix for them
  removing what the guard looks at. Both halves of the repair are real
  — outside a cue-carrying block recall goes from 23/17/4/4 to **23/23
  across all four input shapes** — and the same edit that bought it
  silently converted the guard's other input file from full coverage to
  none, because *joining lines to match on* and *joining lines to
  exempt on* were made the same operation. A widened exemption leaves no
  trace in the output: the run is green either way, which is why the
  regression is invisible to every check now in the build and why it was
  found only by running the old build and the new one over one set of
  injections.

  **The instrument that would have caught it is the one row 14 already
  records as absent.** A `lint-selftest` pair for `check_retired` fixes
  a fixture, and a fixture is a file — the first blank-line-free YAML
  fixture would have failed on the day the block change landed. This is
  the second consecutive round in which `check_retired`'s missing pair
  is the proximate reason a defect shipped, and `make lint-selftest`
  still reports `40 rule/fixture pairs, 8/8 rules` over a target that
  now runs nine rules.

  **Rows 14, 15 and 16 are closed as of 2026-08-06, each verified by O
  independently of H's report.** Row 15: six retired figures injected
  into a live `items.yaml` field are now caught 6/6 where the shipped
  build caught 0/6, and a figure driven through `--write` into the item
  table of the plan of record leaves `--check` failing at both sites.
  Row 16: `fetch-external.py --check` against a copy of
  `vocab/external/` leaves the tree **byte-identical** under `diff -rq`,
  catches a corrupted graph with both digests named and a removed
  sidecar, and exits 1 rather than 0 when it has problems. Row 14 is
  closed by the fixture set row 17 is about — the coverage it asked for
  now exists, in `derive-waves.py`'s own `selftest_guard()` rather than
  in `lint-selftest.py`, and it is self-guarding: a referenced fixture
  removed and an unreferenced fixture added both fail `--check` loudly.
  `make lint-selftest` still reports `8/8 rules`, which is now correct
  for `drift-lint.py` and no longer under-reports `check_retired`.

  **Row 17 is what survived the repair, and it is row 14's shape one
  layer in.** Row 14 was a guard admitted on a probe that varied the
  phrase and not the input shape. Row 17 is a fixture matrix that
  varies what the guard *matches* and not what it *exempts* — and B3,
  the defect the matrix was built to prevent recurring, **was an
  exemption change.** The failure direction is the silent one: widening
  an exemption leaves the run green, which is why B3 needed two builds
  of the guard run over one set of injections to see. Four fixtures
  close it, one per clause, each asserting its phrase with **no
  retraction cue in the sentence** — that absence is the whole point,
  since a cue is what makes the three existing fixtures pass without
  reaching the clause they name.

  **The principle was stated in the same round and applied to one
  clause.** H deleted the table-row-as-unit clause on the ground that
  *"a clause nothing depends on is a clause no fixture can cover, and
  keeping it would leave a permanent hole that looked like coverage."*
  That reasoning is right and the deletion was correct — the row clause
  was measured redundant, `sentence_of` already bounding on `|`. The
  four clauses in row 17 are the opposite case: things **do** depend on
  them, and no fixture covers them. The register records the asymmetry
  rather than the omission, because the principle is the durable part.

  **Row 17 is narrowed rather than closed, and the closure was
  re-derived rather than read.** My own enumeration of `check_retired`
  finds **fourteen** clauses where last round's found ten; deleting each
  in turn against `selftest_guard()` reddens a named fixture for
  **twelve** — eleven redden exactly one, and dropping the sentence
  scope reddens two. All four clauses row 17 names are closed, and so are
  `re.I` on `SIZING_PHRASES`, the F12 position mapping and the F13
  required closer. Two stay silent. One is the whitespace collapse,
  already measured non-load-bearing and declared as such. **The other
  was merged into "blockquote skip" by last round's enumeration and is a
  separate clause** — the `solo` split that makes a `>` line its own
  unit, distinct from the `continue` that skips a blockquoted unit.
  Deleting it leaves all 18 fixtures byte-identical to control, and it
  is load-bearing in **both** directions: a retired figure inside a
  blockquote following prose with no blank line goes exempt → firing,
  and a retired figure asserted in **prose immediately after a
  blockquote** goes firing → **exempt**. The second is the silent
  direction, and it is B3's shape exactly — a widened exemption, green
  either way. This claim's falsifier verbatim, surviving the repair
  built to close it, in a clause the finding that demanded the repair
  counted as half of another.

  **A restatement of the statement above was proposed at this gate and
  is NOT written into it.** H proposed adding *"Ask what result would
  look different if the thing were false. An instrument whose output is
  identical either way carries no information and reads as
  confirmation,"* on the ground that it is prospective where the
  existing criterion is diagnostic; offered three routes as evidence for
  one mechanism — a false negative agreeing with expectation, an
  uncovered guard clause, a fixture asserting a property it cannot test;
  and named its own falsifier: an instrument defect in this register
  whose output *would* have looked different and which shipped anyway.

  **The falsifier fires, and it fires on H's own first route.** The
  `\b`-in-a-non-raw-string defect does not have an output identical
  either way. Measured over `git ls-files` at `f00f027`,
  `"NIFC_Fire\b"` returns **0** and `r"NIFC_Fire\b"` returns **13** —
  and the raw count tracks the corpus across revisions (0 at `8743a46`,
  9 at `be7d243` and `3ddc721`, 13 at `f00f027`), which is what an
  instrument carrying information looks like. It shipped twice not
  because the signal could not discriminate but because the **wrong
  value coincided with the author's prior.** Routes 2 and 3 are the
  opposite, and I confirmed route 2 this round: deleting the
  blockquote-solo clause leaves `selftest_guard()` identical to control.
  Those two are one mechanism. Route 1 is a second one, and the proposed
  sentence misdescribes it.

  **The wording is also silent about which proposition to substitute,
  and route 1 is where that bites.** Asked of *"is `NIFC_Fire` absent
  from the corpus?"* the question is answered satisfactorily — a nonzero
  count would look different — and the defect ships. Asked of *"is my
  pattern correct?"* it catches. Nothing in the sentence selects between
  the two, and for routes 2 and 3 the choice never arises because every
  framing returns the same answer.

  So the mechanism named is real and sharp, and it has a fresh instance
  at this gate — **#18 is exactly it.** But it covers two of the three
  routes offered as its evidence, and a generalisation one of its own
  cited instances does not satisfy does not belong in the statement.
  Recorded here as a disposal, not written above. The wording is H's,
  the ruling is mine, and H is free to re-propose it scoped to the
  mechanism rather than to the three routes.
- **Updated:** 2026-08-07
- **Promotion note:** promoted by O under FALSIFIER §6 at design-gate
  block verification 6, from H's proposal of 2026-08-02. It generalises
  beyond the gate: it constrains how evidence is admitted to this
  project, which is what the register governs, and it binds on every
  future guard rather than on these eleven. It is not a structural
  decision about the vocabulary, so it belongs here and not in an ADR.
  Enters as `asserted`: the instances are evidence that the failure mode
  is real and frequent, not evidence that the discipline is now
  followed.
- **Boundary against [C23](#c23):** C22 is about instruments that cannot
  see. C23 is about claims made without looking. Neither reaches the
  other's set, and the boundary is what keeps either countable — an
  instrument that inspects the wrong thing is C22; a statement posted
  before the run that would establish it is C23, even when the
  instrument is perfect.

### C23 — No claim about an artifact's state is made without running the check that establishes it
No claim about an artifact's state is made without running the check
that establishes it.

- **Status:** `asserted`
- **Falsifier:** a statement asserting what an artifact contains, what a
  tool catches, or what a change accomplished, posted before or without
  the run that would establish it.
- **Cheapest test:** for any such statement, ask what command was run and
  when. If the answer is "the edit reported success", the claim is
  unestablished — an editing step reporting success is not evidence the
  edit landed.
- **Evidence:** 2026-08-04, extended 2026-08-05, 2026-08-06 (three
  times) and 2026-08-07 (twice) — **eighteen instances.** Six sit in
  accepted documents, two more in a plan of record and a commit message,
  five in a generated file of record and a gate message, two — #16 and
  #17 — in the authored prefix map and the gate message that delivered
  it, and one — #18 — in a live generator's source comments and the gate
  message quoting them; two were caught by the check itself rather than
  by the author.

  **#16 and #17 are the same round's remedy and the same round's ground.**
  Both were written to close a finding about unsupported verification —
  B4's inverted banner and the CF route's evidence — and both restate a
  measurement that the change they accompany had already moved or that a
  weaker instrument produced. A retraction is a claim about an artifact's
  state like any other, and it is the one most likely to be written from
  the state the author remembers rather than the state on disk.

  | # | Statement | What was true |
  |---|---|---|
  | 1 | *"the counts are generated from one source and the copies are deleted"* | one copy not deleted (BV5-1) |
  | 2 | *"Corrected in both places"* | corrected in one |
  | 3 | *"the `shared-uri` rule fails on two classes sharing a `class_uri`"* | true, while the mixed construct passed |
  | 4 | *"numeral re-sweep clean on all retired values"* | run against a value the sweep could not see |
  | 5 | *"I re-ran the battery"* | posted before running it; self-caught |
  | 6 | A3's falsifier, design gate 2026-08-03 — *"a live site in the census with no marker and no P20 reference"* | posted and **not run**. Three of the eight censused sites fail it: `plan:562`, `plan:855`, `plan:1343`. Caught by O running H's own falsifier |
  | 7 | `ADR-006:84` — *"`shared-uri` would fire on the design at authoring time"* | **false, and one probe shows it.** `rule_shared_uri` keys on the literal URI string (`claims.setdefault(str(uri), …)`) and does no subclass reasoning. `Place` → `sosa:FeatureOfInterest` with `Hazard` → `deo:Hazard` returns `ok [shared-uri]`, exit 0; the control with both on `sosa:FeatureOfInterest` FAILs. A claim about what a guard catches, in an accepted ADR, made without running the guard |
  | 8 | ADR-006 Decision A's own falsifier — *"a published `prov:Activity` definition … under which a physical process producing no entity is a well-formed `prov:Activity`"* | stated and **not run**. One fetch satisfies it: PROV-O and PROV-DM define Entity as *"a physical, digital, conceptual, or other kind of thing"*, PROV-DM §2.1.1's own activity examples are driving a car, printing a book, baking and a race, and PROV-CONSTRAINTS carries no rule requiring generation |
  | 9 | `items.yaml` P20 `done_when`, still live — *"**MET 2026-08-05.** … Guard in `derive-waves.py`, wired into `make lint`, **probed 12/12 reintroductions caught and 3/3 retractions survive**"* | the 12/12 probe was falsified on 2026-08-05 and the guard was rebuilt the same day. The criterion still certifies `MET` on the falsified reading, and **no probe of the rebuilt guard exists anywhere** — not in `done_when`, not in `lint-selftest`, not in the commit. A claim about what a tool catches, carried by the definition of done that two later items are sequenced behind |
  | 10 | `2b7fa4c` / `2c6d6f1` — *"it fails loudly if it cannot write its target"* | the branch that would report it is **unreachable**. `sync_register()` returns `0` on every path, so `if sync_register(): problems.append(...)` cannot fire, and the message it would print names the retracted README block. The property itself holds, but by construction rather than by the check that was claimed: the write is unconditional, and an unwritable or wrong-type target raises `PermissionError` / `IsADirectoryError` — verified by mutation |
  | 11 | `[H → O]` 2026-08-06, B3 — *"**Hits report their own line.** The first version reported the unit's start, putting every `items.yaml` finding at line 1"* | true for YAML and **false for prose and tables**, which is where the repair changed anything. `check_retired` matches against `probe`, from which backticked and quoted spans have been **deleted**, while `offsets` index the undeleted `joined`; every stripped span before a hit shifts the reported line **earlier**. Measured: a figure on file line 7 of a backtick-heavy paragraph reports as line 4, and a retired figure driven into the last row of the plan's generated item table sits at `:270` and reports as `:268`. The YAML case is exact only because each YAML line is its own unit, so there is one offset to get right. **No fixture asserts a line number** — the 11 pairs assert fire/no-fire only, so the claim's own harness cannot see it |
  | 12 | `vocab/external/register.md`, generated header — *"**`dereferences` carries its REASON, not a bare verdict.**"*, and `[H → O]` 2026-08-06 — *"`dereferences` now carries its reason — four causes, not one"* | the field carries the same bare verdict it did before. Its values across 36 sidecars are `yes` (15), `no` (19), `document` (1) and `untested` (1); there is **no `dereference_reason` field anywhere**. The cause lives in a free-text `detail` sibling and is labelled on **4 of the 19** `no` rows — `**structural**` ×3, `**single observation**` ×1. The two causes the gate message argues hardest for are the unlabelled ones: **access** appears on 12 rows as the bare string `**HTTP 301**`, and **content** — called *"the one that would otherwise be invisible"* — as `200 text/anot+turtle, 306 triples, … NOT defined`. A reader cannot count the four causes from the register; they are recoverable only by reading prose and inferring |
  | 13 | `vocab/external/register.md`, generated header — *"**Four causes, and they decay differently** — F15: this paragraph said *three* and enumerated four"* | the table immediately beneath it enumerates **five**: `structural`, `access`, `single-observation`, `content`, `mints-nothing`. All five are causes of non-dereference, so the disagreement is exact and not a scoping question. F15's defect — a count in a paragraph disagreeing with the enumeration under it — reproduced in the repair for F15, off by one in the same direction, in the same paragraph of the same generated file. The generated distribution further down reports **seven** distinct `dereference_reason` values over the 35 rows; the two extra are `resolves` and `no-probe`, which are not failure causes, so seven-versus-five is consistent and four-versus-five is not |
  | 14 | `[H → O]` 2026-08-06, Artifacts — *"`vocab/external/register.md` (regenerated)"* | the committed file is **not** what its generator emits. Regenerating from the committed sidecars into a throwaway copy differs in five lines: the committed file carries the pre-repair paragraph *"**Both tables carry the column** … it renders only in *Fetched, produced no graph*, which had no reason column, so the fallback was unreachable"* while the generator now emits *"**Every table carries the column** … it is an orphan."* So the committed register asserts the `**unlabelled**` fallback is unreachable, reports *0 fetch(es) produced no graph at all*, and renders `deo` as `**unlabelled**` in an orphan table — three statements that cannot all hold, in a wholly generated file of record. Nothing detects the drift: `--check` reads only and reports `## Problems — *(none)*` |
  | 15 | `[H → O]` 2026-08-06 amendment, A2 — *"the asymmetry is now **the only remaining instance** of the gap that produced three of this round's blocks"* | there is a second, in the same directory and worse. `vocab/external/audit-bound-terms.py` generates the tracked file `vocab/external/bound-terms.md`, has a `--check` mode, and is named nowhere in the `Makefile`: A2 describes a generator that runs without a fixture harness, while this one does not run at all. The claim is about what a directory contains, and the run that establishes it is one command — `git ls-files '*.py'` against `grep Makefile`, ten seconds, which is also the falsifier for the `CLAUDE.md` invariant the same amendment cites |
  | 16 | `vocab/core/prefixes.yaml`, the BOUND banner **rewritten from measurement this round to replace a false one** — *"14 namespaces dereference (`resolves`), 2 … (`content`), 1 was never probed"* | measured now: **15 `resolves`, 2 `content`, 0 unprobed.** The one unprobed namespace was `cfsn`, and **the same commit (`1ccfff3`) bound it** — the banner and the `cfsn:` line are additions in one diff. So the sentence written to retract an inverted method carries a distribution from before its own commit's change, and a reader looking for the never-probed namespace finds none. Re-derived by mapping all 17 declared namespaces onto the sidecars' `namespace:` fields and tallying `dereference_reason`. The same sentence calls the five audited namespaces *"the six keys in `audit-bound-terms.py`'s NS map"*: `NS` has **seven** keys, `LOOKUP` has six entries, and the five named are namespaces | H | O, by running the namespace-to-sidecar comparison the file's own NAMED GAP section specifies and declares unbuilt |
  | 17 | `[H → O]` 2026-08-07, the CF switch — *"**probes** — **six**, OHIM's actual CF names — one would clear check 5 and prove nothing about the other five"* | **one of the six is a probe.** `PROBE["cf-standard-name"]` is a single URI, `…/standard_name/air_temperature/`, and it is the only one evaluated by `dereferences()`, the mechanism that parses a graph and tests for `rdf:type`. The other five reach the register through `terms_found()`, a `\b`-anchored **substring match over the raw payload bytes** — the strength the same sentence says proves nothing. **`nvs-p07` is the control and it sits in the tree:** its row reads `6/6 terms present`, identical wording in the identical column, with **0 of 6 declared as subjects** — every one a `skos` label match, because P07's subjects are `…/current/00B3H4MY/`. So the *Content check* column reads the same for a route where the terms are subjects and one where they are labels, which is the distinction `CLAUDE.md` and `prefixes.yaml` both draw between the two routes. **The conclusion is true and independently verified** — O parsed the cached graph and found all 6/6 present as subjects carrying `rdf:type` at the trailing-slash URI — so the binding is sound and five-sixths of the evidence offered for it is the weaker test. It also contradicts a convention added to `.claude/rules/vocab-conventions.md` in the same round: *"The test is **parse the body and find the term**"*, against `terms_found`'s docstring, which argues for substring deliberately | H (script), human (convention) | O, by parsing both cached CF graphs and asking, per name, whether it is a typed subject or only a literal |
  | 18 | `vocab/external/fetch-external.py:162` and `:422`, and `[H → O]` 2026-08-07 — *"`CLAUDE.md`'s ADMS line needs no disambiguation"* (asserted first as a bare conclusion, then twice more through two restatements), and `DIGEST_PEER`'s stated consequence *"a second document is back in play, and `CLAUDE.md`'s ADMS line has to say which one is meant"* | **`CLAUDE.md` has no ADMS line, and no revision of it ever has.** `grep -niE 'adms\|semic\|asset descr' CLAUDE.md` returns nothing, and `git log --all -S adms -- CLAUDE.md` and the same pickaxe on `ADMS` both return no commit — so this is not a stale pointer to a line since removed, it is a referent that has never existed. Two consequences. The conclusion the round's **third** phrasing was built to reach is vacuous: a sentence that does not exist needs no disambiguation under any measurement, so the ADMS resolution terminates in a statement nothing could falsify. And `DIGEST_PEER`'s rationale routes a future reader — at the exact moment the guard fires — to repair a sentence they will not find. Under the charitable reading the line meant is `CLAUDE.md`'s external-vocabularies paragraph, which the previous round rewrote to *"Read `vocab/external/register.md` for which, per namespace; do not read a claim about it here"* — it carries no per-namespace claim and so would need no disambiguation under any divergence either. Both readings leave the sentence false or empty. The establishing run is one grep | H | O, by grepping `CLAUDE.md` and pickaxing every revision of it |

  **#6 is the instance that establishes the claim is not retrospective.**
  It was posted in the same message that proposed C23, as the falsifier
  for an assertion in that message, and it fires. A falsifier offered and
  not run is the purest form of this defect: the author names the
  experiment that would break the claim and then does not perform it,
  which reads to a reviewer as though it had been performed and come back
  clean.

  **#8 is #6 a second time, one round later.** A falsifier written into
  the same document as the claim it would break, and not performed —
  this time inside an ADR accepted the day it was written. The two
  together are the reason the *Cheapest test* above asks what command
  was run rather than whether a falsifier is stated: a stated falsifier
  is the strongest signal that the experiment looks cheap, and in both
  instances it was — one grep, one fetch.

  **Most of what this gate blocked on was C23's set, not C22's** — false
  claims about artifacts, not defective instruments. That asymmetry is
  the reason for a second entry rather than a widened C22, and it held
  again at block verification 7: all three blocks are C23's.

  **#9 and #10 are the same round as C22's rows 15 and 16, and the pair
  is the point.** A repair was made, its mechanism was described
  accurately in the commit, and neither the criterion that certifies it
  nor the property the commit asserts was run against. #10 is the milder
  shape and worth keeping for it: the claimed property is **true** — the
  generator does fail loudly — and the check named as establishing it
  cannot execute. A claim that happens to be right, established by
  nothing, which is C22 #10's shape moved from an instrument to an
  assertion about one.

  **#9 and #10 are both closed as of 2026-08-06.** `items.yaml:241`
  withdraws the 12/12 probe in place, records that it varied the phrase
  and never the input shape, and carries a two-axis result instead; the
  generated done table at `plan:619` projects the withdrawal, so both
  views agree. A sweep for the **retracted** string rather than the
  replacement finds `12/12` in five tracked files and every occurrence
  is a withdrawal record or this register — no live citation survives.
  #10's branch can now fail: with every sidecar removed,
  `sync_register()` prints `FAIL no provenance sidecars … register.md
  NOT written` and returns 1.

  **#11 and #12 are both claims about a repair, made in the message
  reporting the repair.** Neither is a claim about work not done — the
  repairs behind them are real and I verified both. What was not run is
  the case that would have shown the claim's *scope*: #11 asserts a
  property of the output on the input shape the repair did not change
  its handling of, and #12 asserts a field carries something a sibling
  field carries on a fifth of its rows. Both are cheap: one `--check`
  against a backtick-heavy paragraph, one `grep dereferences:` across
  the sidecars.

  **#12 is the first instance whose site is a *generated* file**, which
  is a shape worth naming. The sentence is in `sync_register()`'s
  output list, so it is rewritten on every run and cannot drift from
  the generator — but it also cannot drift from the generator when the
  generator is what is wrong, and no check compares the header's claim
  against the rows beneath it. The same paragraph says *"**Three**
  unrelated causes were all printing `no`"*, enumerates **four**, and
  closes *"One value covering **four** causes is C11's shape"* —
  three-versus-four inside one paragraph, in a file of record, which is
  [C22](#c22)'s boundary case landing on C23's side: nothing inspected
  it because nothing was pointed at it.

  **#13 is that same paragraph one build later, and #14 is why nobody
  saw it.** The three-versus-four was repaired by adding a fifth row to
  the table and changing the word *three* to *four* — the count moved
  with the edit that caused it and stopped one short of the list it
  describes. The repair was written into the generator and the register
  was regenerated before the last generator edit landed, so the file of
  record is now behind the generator as well as wrong about its own
  table. Both are recoverable by one run and one count, and neither
  instrument in the build performs either: `--check` does not
  regenerate, and nothing compares a prose count against the rows under
  it. The pair is the reason C22 #18 and these two arrived in the same
  pass — one artifact, three defects, no run that could see any of them.

  **#15 is the first instance attached to a self-declared open gap**,
  and that is what makes it worth counting rather than waiving. A2 was
  filed as a finding against H's own repair and left open deliberately;
  nothing about the disclosure is in bad faith. What was not run is the
  enumeration that would have bounded it. A gap declared as *the only
  one* is a claim about a population, and the distance between declaring
  a gap and declaring its extent is one command — which is also why this
  sits on C23's side of the boundary and not [C22](#c22)'s: no
  instrument inspected the wrong thing, because none was pointed at the
  question.
- **Updated:** 2026-08-07
- **Promotion note:** promoted by O under FALSIFIER §6 at design-gate
  block verification 6, from H's proposal of 2026-08-03. Accepted as
  proposed, with instance #6 added by O. It generalises beyond the gate
  and no existing entry covers it: C18 is about whether lint rules detect
  what they claim, C22 is about whether an instrument can see its own
  failure mode, and this is about whether the run happened at all.
- **Note on the two entries together:** C22 and C23 both constrain
  evidence rather than the vocabulary. They are the register's answer to
  a failure direction named in `FALSIFIER.md` §4 — *an instrument that
  reports success when it has inspected nothing* — extended to cover the
  case where no instrument was run.

### C24 — Every type named in a relation signature carries the declaration its kind calls for
Every type named as an argument in a relation signature carries the
declaration its kind calls for: a **subject** is a row in the Part 0
entity table, a **structural primitive** is an external binding, a
**code-list reference** is a SKOS concept scheme (ADR-000 D5), and a
**role variable** requires none because it ranges over any entity.

- **Status:** `falsified`
- **Falsifier:** a type named as an argument in any relation signature
  whose kind's declaration does not exist — a subject with no entity
  table row, a primitive bound to nothing, a code-list reference naming
  no scheme.
- **Cheapest test:** enumerate every relation signature in the tree,
  extract the argument names from the signatures rather than from a list
  already in hand, and word-boundary grep each across `design/`,
  `docs/`, `vocab/`, `codelists/`, `transform/`, `fixtures/` and
  `README.md`. Under ten minutes.
- **Evidence:** 2026-08-04 — **born `falsified`. Eight counterexamples,
  all inside one accepted ADR.**

  Five relation signatures exist in `design/ADR-002-entity-core.md`,
  naming **thirteen** argument types. Three are declared entities —
  `Agent`, `Asset`, `Place`. Two are role variables and need no
  declaration. The remaining **eight have none**.

  | Kind | Names | The declaration its kind calls for | State |
  |---|---|---|---|
  | **Subject** | `HazardEvent`, `Incident` | a Part 0 entity table row | **undeclared** — Part 1, deferred by ADR-006 |
  | **Structural primitive** | `Interval`, `Measure`, `Level` | an external binding — OWL-Time, QUDT | **used, bound nowhere** |
  | **Code-list reference** | `HazardType`, `CapabilityType`, `Function` | a SKOS concept scheme | **named, no scheme exists** |
  | **Role variable** | `Whole`, `Part` | none — ranges over any entity | correct as-is |

  **`Interval` is the strongest instance.** It appears in **four of the
  five** signatures. Re-derived by O rather than accepted: word-boundary
  grep across the readable tree returns `ADR-002`, `ADR-006`,
  `measure-01`, `README.md` and `docs/coverage.md:192` — every one a
  *use* in a signature, none a declaration. `owl-time`, `time:Interval`
  and `w3.org/2006/time` return **one hit in the entire tree**:
  `ADR-006:228`, the cell asserting it is unbound. `CapabilityType` is
  second: ADR-002 Decision F says it is a SKOS scheme and never names
  one, and until 2026-08-04 it had exactly one occurrence in the tree.

  **The section whose first line is *"Entities are declared once in Part
  0"* makes its forcing argument with subjects it never declares, and
  quantifies four of its five relations over a type nothing binds.**

  **The entity core is short by two subjects, not by eight.** Three
  primitives and three code-list references with no binding are a
  different defect with a different repair, and collapsing them is how
  an entity table becomes a type registry. The kernel stays six.

  **Why this stayed invisible is structural.** ADR-000 D1 segments the
  parts by epistemic kind, and Parts 2, 3, 5 and 6 do. Parts 1, 4 and 7
  are named for **subjects**. So the entity core caught the subjects
  with no part named after them and left the ones that had one, on the
  assumption that the part *was* the home. A part is a statement kind; a
  hazard is a subject.

  **`sosa:Procedure` confirms the rule rather than breaking it.** It
  appears in Part 2's observation relation and in no entity table,
  correctly: a procedure is an IR flight protocol, a digitisation method
  or a simulation model — a `Document`, or an `Asset` when it is
  software. A role filled by an existing entity, which is
  role-not-subtype holding where nobody consciously applied it.
- **Updated:** 2026-08-04
- **Promotion note:** minted by O under FALSIFIER §6 at design-gate
  block verification 8, from the human's draft of 2026-08-04 and H's
  proposal of the same day. **Filed `falsified`, not `asserted`,** under
  §6's *do not weaken a claim to make it pass*: it is false today, its
  counterexamples are enumerable, and a claim born falsified with its
  counterexamples listed is the entry that would later justify writing
  the lint rule. Aspirational entries are not what this register is for.
- **Statement corrected on minting, and the correction recorded rather
  than made silently.** H proposed *"every type named in a relation
  signature has **a declaration of its kind**."* On a literal reading
  `ADR-006:226-231` **is** such a declaration for all thirteen names,
  including the eight — it assigns each a kind — so the claim would be
  *satisfied*, with its own evidence table the thing satisfying it.
  What is absent is not a statement of which kind a name is but **the
  declaration that kind calls for**, which is what H's own fourth column
  measures. Statement and falsifier disagreed; the falsifier and the
  eight counterexamples were right and the statement was rewritten to
  them. **No counterexample was dropped and the population is
  identical.** This is the fourth round in which a proposed claim's
  statement and falsifier tested different things — see C21 — and it is
  recorded here so the register shows where that was caught.
- **Boundary against [C22](#c22) and [C23](#c23):** those two constrain
  **evidence**. C24 constrains the **vocabulary** — it is about what the
  artifact declares, not about how a claim was established. It is the
  first entry in that set since C21.

### C25 — The alias decomposition is exercised
Every class in ADR-001's identity structure — `IdentifiedObject`,
`Name`, `NameType`, `NamingAuthority`, `ObjectType` — carries data that
no simpler mechanism could hold.

- **Status:** `asserted`
- **Falsifier:** a working alignment over the reference
  implementation's own feeds that resolves the same incidents, using
  only a minted identity plus an ordered list of schemes, with no
  `NameType`, `NamingAuthority` or `ObjectType` instance. If that
  reproduces the same partition, the classes it omits are unexercised.
- **Cheapest test:** at P6b, resolve one day of captured WFIGS and
  perimeter records twice — once through the four-class structure, once
  through `{minted_id, scheme_rank}` alone — and **diff the partitions,
  not the counts.** Under an hour once fixtures exist. A difference
  falsifies the simpler mechanism; an identical partition falsifies
  this claim. **Two runs producing the same number of clusters with
  different membership is precisely the outcome the decomposition
  exists to prevent, and a count comparison reports it as agreement.**
  *(Sharpening proposed by H 2026-08-05; O disposed and wrote it. The
  wording is H's.)*
- **Note — the two systems answer different questions, and that is the
  argument this claim rests on.** KnowWhereGraph's alignment is
  *retrospective and curated*: Hurricane Katrina is one event because a
  person decided so once, and the URI records the decision. This
  project's is *live and automated*: several perimeter services publish
  one fire under different names within minutes, and something must
  decide without a human whether two records are one incident. That
  decision can be wrong, so it must be auditable and reversible —
  `candidateMatch` records a suspicion without asserting identity,
  precedence records which scheme won, `NamingAuthority` records who
  issued the identifier that decided it. KWG needs none of this because
  its alignment is a fact rather than an inference. **If that
  distinction does not hold, most of the decomposition is decoration.**
- **Watch — standing evidence against, from a working system.
  Population corrected by O 2026-08-05; see Evidence.** KnowWhereGraph
  aligns named events across NOAA Storm Events, FEMA Disaster
  Declarations Summaries and NOAA Historical Hurricane Tracks with
  **zero identity constructs in its schema**: `owl:sameAs`,
  `skos:exactMatch`, `prov:alternateOf`, `prov:specializationOf`,
  `dcterms:identifier` and `schema:identifier` all occur 0 times, and
  nothing matching `*name*`, `*align*`, `*match*` or `*identif*` is
  declared — **across the three DMDO alignment modules**
  (`disaster-event-module-generalized`,
  `disaster-event-module-extensions`, `disaster-properties-ontology`),
  **not across all four cached graphs.** The fourth,
  `undrr-isc-hazard-classification`, is a republished UNDRR-ISC
  controlled vocabulary rather than an alignment module, and it carries
  identifier and name terms. Measured, not inferred. It is the only
  working system in this domain either way.
- **Price qualifier, proposed by H 2026-08-05 and disposed with a
  correction.** H proposed recording that KWG's graphs are *"borrowed
  material from a namespace with no TLD, so KWG cannot be read as a
  published counter-design."* Verified and **true of the three DMDO
  modules**, which mint under `http://knowwheregraph/ontology/dmdo#` —
  a host with no TLD, recorded in `vocab/external/manifest.md:49-51` as
  *"cannot resolve for anyone — bindable only as BORROWED"*. It is
  **not** true of the fourth graph, which mints under
  `https://undrr-hip.org/`. So the qualifier is written for the three
  modules only. The point it carries survives and is the one that
  matters: this is evidence that a working pipeline got by without an
  alias vocabulary, **not** evidence that a published alternative
  vocabulary exists.
- **Scope — this is about cost, not correctness.** ADR-001 question 1
  is recorded as *settled*, and the structure may be right. C25 asks
  whether it is **paid for**. An absence of published alternatives is
  weak support for a design; a deployed system that does the job without
  it is evidence about price.
- **Evidence:** 2026-08-05 — O re-ran C25's own standing measurement
  against `vocab/external/graphs/`. **The six identity constructs
  reproduce exactly: all six occur 0 times across all four graphs.**
  That half of the Watch bullet survives an independent run.

  **The rest of it does not, and it failed in this project's recorded
  instrument direction — a zero returned because the search looked for
  a string rather than for the thing.**

  | Term | as written in the Watch bullet | measured, by URI |
  |---|---|---|
  | `dcterms:identifier` | 0 across all four | **2**, in `undrr-isc-hazard-classification.ttl` |
  | `*identif*` declared | none | **`hip:identifier`, 205 occurrences** |
  | `*name*` declared | none | **`hip:vernacularName`, 1**; `foaf:name` |

  The graph binds `@prefix terms: <http://purl.org/dc/terms/>` **and**
  `@prefix dcterms: <http://purl.org/dc/terms/>` — two labels, one
  namespace — and writes the property as `terms:identifier`. A grep for
  the literal string `dcterms:identifier` returns 0 while the URI
  `http://purl.org/dc/terms/identifier` is present twice. This is
  [C22](#c22)'s failure mode, not a defect in C25's argument.

  **The claim's substance is unaffected and the correction narrows the
  evidence rather than the claim.** The three DMDO modules — the
  alignment vocabulary the argument is actually about — are clean on
  every construct and every pattern. The fourth graph is a hazard
  *classification* list, where per-concept identifiers are expected and
  say nothing about whether alignment needs identity constructs.
  C25 stays `asserted`: nothing here tests the decomposition's price,
  which only the P6b partition diff can do.

  **2026-08-06 — `irwinID`, proposed by H and disposed by O after an
  independent run. The wording below is H's; the measurement is mine.**
  H proposed recording that *"`irwinID` is declared in two of the eleven
  KWG source ontologies. It is the only term in that corpus touching
  ADR-001's identity apparatus, and its declaring file is arbitrary."*
  Re-derived over `vocab/external/graphs/` with rdflib rather than by
  grep: across the eleven KWG dataset ontologies there are 444 distinct
  typed subjects, 46 of them declared in more than one file, and ten of
  those are in KWG's own namespace. **`irwinID` is one of the ten, in 2
  of 11**, alongside `hasFIPS`, `stateName` and `countyName`. Confirmed
  and written.

  **What it is evidence for, and what it is not.** It is a real instance
  of the problem the alias decomposition exists to make explicit — a
  scheme identifier whose declaring file carries no meaning, so nothing
  in the corpus says which authority issued it or how it ranks against
  another scheme. It is **not** evidence about price, which is what C25
  asks: one term declared twice does not show that a four-class
  structure is paid for. The claim stays `asserted` and the P6b
  partition diff remains the only test that moves it.
- **Updated:** 2026-08-05

### C26 — A measurement of somebody else's artifact is true at a timestamp, not in general
A measurement of somebody else's artifact is true at a timestamp, not in
general. A register of such measurements states its shelf life, and a
claim that cites one carries the date it was made.

- **Status:** `asserted`
- **Falsifier:** a live-fetch verdict in this repository that cannot
  change without a change in this repository.
- **Cheapest test:** take any `dereferences` verdict, re-fetch its
  namespace, and ask whether the value could have moved without any
  commit here. Minutes. *(The criterion above is H's; this procedure is
  O's mechanical form of it, and adds nothing to what it asserts.)*
- **Evidence:** 2026-08-07, verified by O at the implement gate that
  proposed it.

  **The register states its shelf life once, in the header**, rather than
  per row — `register.md:10-19`, *"EVERY VERDICT IN THIS FILE HAS A SHELF
  LIFE"*, with the reason for stating it once given in the file: a
  per-row staleness note is a hand-written claim beside a generated one.
  Each verdict's date lives in its sidecar's `fetched:` field, which the
  header points at.

  **The first instance is the ADMS pair, and it is stronger than a
  document changing under a binding.** Independently reproduced:
  `https://www.w3.org/ns/adms.ttl` returns **HTTP/2 307** with
  `location: https://uri.semic.eu/w3c/ns/adms.ttl`, and SEMIC returns
  **200 `text/turtle`, 12,687 bytes, `last-modified: Mon, 22 May 2023`**
  — unchanged for three years while this repository's cache moved
  11,134 → 12,687 bytes inside one session. So the artifact was not
  edited; a server changed its mind about who serves it, between two
  fetches, and every byte-level check in the tree agreed before and
  after. The measurement was correct at both timestamps and described
  different worlds, which is the case neither [C22](#c22) — instruments
  that cannot see — nor [C23](#c23) — claims made without looking —
  reaches.

  **The falsifier was executed and the nearest miss is recorded**, so a
  later reader knows it is not merely plausible. The closest candidate in
  the tree is the `structural` decay class, which the register's own
  table characterises as decaying *"never — a host with no TLD cannot
  resolve for anyone"* (`deo`, `http://knowwheregraph/ontology/deo#`).
  It does **not** satisfy the falsifier: the verdict is still contingent
  on the world rather than on this repository — registering the TLD would
  move it — so it decays slowly, not never. No verdict in the register
  currently meets the falsifier's terms.
- **Updated:** 2026-08-07
- **Promotion note:** promoted by O under FALSIFIER §6 at the implement
  gate of 2026-08-07, from H's proposal in the same gate message. The
  statement and the Falsifier are **H's wording, accepted as proposed**;
  the disposal, the verification and the write are O's, per §1's
  disposed-field rule. It generalises beyond the gate because it
  constrains the register — an artifact that outlives every gate — rather
  than this round's work, and no existing entry covers it: C22 is about
  an instrument that cannot see its own failure mode, C23 about a claim
  made without running the check, and this about a check that ran, was
  correct, and expired.
- **Note:** C26 is about the shelf life of the measurement. It says
  nothing about whether a guard cited as *keeping a measurement current*
  actually does so — that is C22, and [C22](#c22) row 24 is this same
  round's instance, where `DIGEST_PEER` was offered as what keeps the
  ADMS sentence true and is green by construction while the redirect
  stands.
### C27 — A class bound to an external URI does not make this model's shapes normative for that vocabulary
No shape generated from `vocab/` constrains an instance that is not
this model's to constrain. Where a class carries a `class_uri` naming
an external term, the generated shape's target is the model's own
population — not every node in a consumer's graph bearing that external
type.

- **Status:** `falsified`
- **Falsifier:** a graph containing only correct, unmodified use of an
  external vocabulary this model binds, which `pyshacl -s
  build/shapes.ttl` reports as non-conformant. Any violation falsifies.
- **Cheapest test:** write four triples of textbook PROV-O — an entity
  with `prov:wasGeneratedBy`, an activity with `prov:startedAtTime`, an
  agent with `prov:actedOnBehalfOf` — and validate. Under five minutes,
  no fixtures required.
- **Evidence:** 2026-08-07 — **born `falsified`, on the first schema
  this project generated.** `gen-shacl` emits `sh:targetClass <the
  class_uri>` together with LinkML's default `sh:closed true`, so
  binding an external class URI silently makes the shape normative for
  every instance of that class anywhere. Four of nine shapes in
  `build/shapes.ttl` do this:

  | Shape | `sh:targetClass` | `sh:closed` | Line |
  |---|---|---|---|
  | `Activity` | `prov:Activity` | `true` | 11-40 |
  | `Statement` | `prov:Entity` | `true` | 42-98 |
  | `Agent` | `prov:Agent` | `true` | 193-222 |
  | `Geometry` | `geo:Geometry` | `true` | 144-154 |

  A nine-triple PROV-O graph using nothing but PROV-O's own terms
  correctly returns `Conforms: False`, **six violations**, all
  `ClosedConstraintComponent`: `prov:wasGeneratedBy`,
  `prov:wasDerivedFrom`, `prov:generatedAtTime`, `prov:startedAtTime`,
  `prov:wasAssociatedWith`, `prov:actedOnBehalfOf`. pyshacl 0.40.1
  against `build/shapes.ttl` at commit `ef00998`.

  **`prov:generatedAtTime` is the sharpest of the six.** The schema
  binds it on `Identifier.assertedTime`, and PROV-O declares it with
  `rdfs:domain prov:Entity` (`vocab/external/register.md`, audited term
  table). So the one PROV-O term this model deliberately reuses is
  rejected on the one class PROV-O declares it for.

  **This is not C17.** C17 axis 2 is `gen-shacl` ignoring a `slot_uri`
  when emitting a **range**. This is the target side: the `class_uri` is
  consulted, faithfully, and the consequence is that a local modelling
  decision is published as a constraint on somebody else's vocabulary.
  A repair to axis 2 would not move it.

  **Scope of the measurement.** Run with no entailment regime, which is
  what `make check` uses. Under RDFS entailment it is worse rather than
  better: loading `graphs/prov-o.ttl` as an ontology and inferring makes
  an `ohim:Identifier` carrying `assertedTime` a `prov:Entity` by
  `rdfs:domain`, after which the closed `prov:Entity` shape rejects it
  for carrying `ohim:issuingAuthority` — the model self-invalidating
  from its own bindings. Recorded as a consequence, not as the claim:
  the claim is falsified without any entailment regime at all.

  **2026-08-07, second measurement — reproduced against the first
  fixture, and the remedy is verified in two formulations and not in the
  one that was ruled.** `fixtures/part0/part0-conformant.jsonld` now
  exists, so this is measured against an instance rather than a
  throwaway graph. `make check`: 1 file, `Conforms: False`, **5
  violations — 4 `ClosedConstraintComponent`** (`prov:wasAssociatedWith`,
  `prov:startedAtTime`, `prov:wasGeneratedBy`, `prov:generatedAtTime`)
  **and 1 `DatatypeConstraintComponent`** (`geo:asWKT`, which is B12 and
  not this claim).

  `gen-shacl --non-closed` over the same schema and fixture: **9
  `sh:targetClass` retained, `sh:targetClass prov:Entity` retained, the
  four closed violations to zero, one violation remaining.** So the
  binding is not what makes this claim false — `sh:closed` is, and it
  can be removed without losing a target.

  **The scope that was ruled does not load, and that is the entry's new
  content.** Executing *"delete `sh:closed true` from any shape whose
  `sh:targetClass` is not under `https://w3id.org/ohim/`"* against
  `build/shapes.ttl` removes it from exactly four shapes and leaves nine
  targets — and pyshacl 0.40.1 then refuses the shapes graph:
  `ConstraintLoadError: you can only use sh:ignoredProperties on a
  Closed Shape`. `gen-shacl` emits `sh:ignoredProperties ( rdf:type )`
  on every closed shape, and deleting `sh:closed` orphans it.

  | Edit to the four external-target shapes | Result |
  |---|---|
  | delete `sh:closed true` only | **ConstraintLoadError — nothing validated** |
  | `sh:closed true` → `sh:closed false` | `Conforms: False`, 1 violation (B12) |
  | delete `sh:closed true` **and** `sh:ignoredProperties` | `Conforms: False`, 1 violation (B12) |

  **Status unchanged.** No source and no pipeline change has landed;
  `build/shapes.ttl` at this commit still carries `sh:closed true` on all
  four. Recorded so the repair is not re-derived, and so the difference
  between the flag that was measured and the edit that was ruled is in
  the register rather than in one gate message. O, at the B14 relay,
  2026-08-07 — B17 in `review-inbox.md`.
- **Updated:** 2026-08-07
- **Promotion note:** minted by O under FALSIFIER §6 at the P6a
  implement gate, 2026-08-07. Not proposed by H; the statement, the
  Falsifier and the test are O's, which §1 permits for an entry O mints
  and forbids only for a Falsifier attached to a claim H owns. Filed
  `falsified` rather than `asserted` under §6's *do not weaken a claim
  to make it pass*, following C24's precedent: it is false today, its
  counterexamples are enumerable, and a claim born falsified with them
  listed is the entry that justifies the repair. It generalises beyond
  this gate because every Part that binds an external class reproduces
  it — the four instances here are the four bindings that exist.
- **Boundary against [C21](#c21):** C21 forbids two schema elements
  asserting the *same* external URI. C27 is about one element asserting
  *any* external URI and what the generated shape then claims authority
  over. `shared-uri` passes over this file; C27 is falsified by it.
