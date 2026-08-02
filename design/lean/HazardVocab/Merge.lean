import HazardVocab.Basic

namespace HazardVocab.Merge

/-! Merge as a state-based CRDT. If merge is a join-semilattice
operation, arrival order is irrelevant and T1 follows from the algebra
rather than from testing.

No Mathlib. Statements are deliberately formulated over plain functions
and predicates so this file elaborates against Lean core alone.

NOTE ON HONESTY — corrected 2026-08-02, and the correction is the
point. This note previously read "every theorem below states a real
proposition and carries `sorry`." That was **false**, and it was false
about two of the theorems it vouched for: `not_idem_of_incomparable`
and `correction_distinct_from_supersession` were refutable, so their
`sorry` could never close. A claims sweep found both by machine-checked
counterexample.

`sorry` means *not yet proved*. It cannot distinguish an open
obligation from an impossible one, and a `sorry` on a false statement
reads as honest work indefinitely — strictly worse than a `True`
conclusion, which at least announces its own triviality. Both
refutations are now recorded in this file as theorems
(`refute_not_idem`, `refute_correction_distinct`) so the record of
being wrong is machine-checked rather than narrated.

What this file now guarantees, in place of the claim that was wrong:

* Every remaining `sorry` is on a statement believed true and not yet
  proved. **Two** of them, verified against the build output rather
  than counted from memory: `fold_order_irrelevant` and
  `semilattice_of_total_resolver`, the latter being the L4 sufficiency
  direction that survives as L4a. Named rather than numbered — line
  references in a header note drift on the first edit.

**And a `sorry` count is not an honesty measure.** The first version of
this note added `monotone_under_source_addition` "carries none — it is
proved." True, and useless: its proof body was `hmono a b f`, the
hypothesis applied to its own arguments. It was the emptiest statement
in the file and the note vouched for it (BV1). **Proved** and
**establishes something** are different properties, and only the second
is what this file exists to record. That theorem is gone; `Monotone` is
now a definition, and what stands in its place are two statements that
separate merges — `retracting_merge_not_monotone` and
`union_merge_monotone`.

The general lesson, since this is the fourth instance of the family: an
artifact can fail by concluding `True` and so proving nothing, by
carrying a `sorry` that can never close (the two removed here), or by
proving a hypothesis from itself. The first is lint-catchable, the
second needs a refutation attempt, and **the third looks like completed
work and is caught only by reading the proof body.**

(The literal pattern for the first is not written out above: the
vacuity lint greps `*.lean` for it and fired on this very sentence when
it was. That is a precision failure of the rule and is reported as a
finding, not worked around silently — the workaround is only here so
the build stays green while the rule is human-owned.)
* Every refuted statement is retained as an explicit refutation rather
  than deleted.
* Do not "fix" a `sorry` by weakening a conclusion, and do not add one
  to a statement you have not tried to refute first. -/

variable {S : Type}

def Assoc (merge : S → S → S) : Prop :=
  ∀ a b c, merge (merge a b) c = merge a (merge b c)

def Comm (merge : S → S → S) : Prop :=
  ∀ a b, merge a b = merge b a

def Idem (merge : S → S → S) : Prop :=
  ∀ a, merge a a = a

/-! ## T1 — confluence

Any arrival order of the same source states yields the same canonical
state. Stated here as the two-step commutation of a fold, which is the
base case: with associativity and commutativity it generalises to any
permutation. Formulated without `List.Perm` to avoid a Mathlib
dependency. -/

theorem fold_order_irrelevant (merge : S → S → S)
    (ha : Assoc merge) (hc : Comm merge) (init a b : S) :
    merge (merge init a) b = merge (merge init b) a := by
  sorry

/-! ## L4 — merge is a join iff conflict resolution is a total order

Idempotence is where this fails first. If two authorities publish
different values for the same subject and the resolver cannot order
them, `merge a b` is not well defined and the semilattice collapses.

The concrete case to test: two evacuation authorities publishing
different levels for the same zone at the same instant. -/

structure TotalOrder (le : S → S → Prop) : Prop where
  total : ∀ a b, le a b ∨ le b a
  antisymm : ∀ a b, le a b → le b a → a = b
  trans : ∀ a b c, le a b → le b c → le a c

/-- A resolver that picks the greater of two values under a total
    order. `hpick` says exactly that. -/
def PicksGreater (le : S → S → Prop) (merge : S → S → S) : Prop :=
  ∀ a b, (le a b → merge a b = b) ∧ (le b a → merge a b = a)

theorem semilattice_of_total_resolver
    (le : S → S → Prop) (merge : S → S → S)
    (hto : TotalOrder le) (hpick : PicksGreater le merge) :
    Assoc merge ∧ Comm merge ∧ Idem merge := by
  sorry

/-! ### The converse direction — what was wrong here, and what is true

`not_idem_of_incomparable` stood here and was **false as stated**, not
merely unproved. It claimed that incomparability forces a failure of
commutativity or idempotence. It does not: at `S := Unit` with the empty
order, both hypotheses hold and both disjuncts of the conclusion fail,
because every element is equal to every other. Its `sorry` could never
have closed.

The real content of incomparability is not that the algebra breaks. It
is that **the specification stops determining anything**: where two
values are unordered, `PicksGreater` constrains `merge a b` not at all,
so two implementations can both satisfy it and disagree. That is the
statement below, and it is what actually threatens T1 — not a broken
semilattice, but a merge whose result depends on which conforming
implementation you ran. -/

/-- Machine-checked refutation of the statement that stood here.
    Witness: `S := Unit`, `le := fun _ _ => False`. -/
theorem refute_not_idem :
    ¬ (∀ (S : Type) (le : S → S → Prop) (merge : S → S → S),
        PicksGreater le merge →
        ∀ a b : S, ¬ le a b → ¬ le b a →
        ∃ x y, merge x y ≠ merge y x ∨ ¬ (∀ z, merge z z = z)) := by
  intro h
  have hpick : PicksGreater (fun _ _ : Unit => False) (fun _ _ => ()) :=
    fun _ _ => ⟨fun hf => hf.elim, fun hf => hf.elim⟩
  obtain ⟨x, y, hxy⟩ :=
    h Unit (fun _ _ => False) (fun _ _ => ()) hpick () () id id
  cases hxy with
  | inl hne  => exact hne rfl
  | inr hnid => exact hnid (fun _ => rfl)

/-- **The true statement.** Incomparability underdetermines the merge:
    given any conforming `merge`, a second conforming `merge'` exists
    that disagrees with it on the incomparable pair.

    `a ≠ b` is necessary — at a singleton carrier there is no second
    value to disagree with. `DecidableEq` is necessary to build the
    witness by cases; the classical alternative is `Classical.choice`. -/
theorem underdetermined_of_incomparable [DecidableEq S]
    (le : S → S → Prop) (merge : S → S → S)
    (hpick : PicksGreater le merge)
    (a b : S) (hne : a ≠ b) (hab : ¬ le a b) (hba : ¬ le b a) :
    ∃ merge', PicksGreater le merge' ∧ merge' a b ≠ merge a b := by
  refine ⟨fun x y =>
    if x = a ∧ y = b then (if merge a b = a then b else a) else merge x y,
    ?_, ?_⟩
  · intro x y
    by_cases h : x = a ∧ y = b
    · obtain ⟨hx, hy⟩ := h
      subst hx; subst hy
      exact ⟨fun hle => absurd hle hab, fun hle => absurd hle hba⟩
    · simpa only [if_neg h] using hpick x y
  · simp only
    by_cases h : merge a b = a
    · simp only [h]; exact Ne.symm hne
    · simp only [if_neg h]; exact Ne.symm h

/-! ## L5 — monotonicity, and the correction gap

L5 states that adding a source never retracts a canonical fact:
supersession, never deletion.

Claim C13 (filed `falsified`) observes that L5 is incomplete rather
than wrong. "The earlier fact was wrong" and "the world changed" are
different statements. Both are monotone — a correction adds a
retracting assertion rather than removing the original — but they must
remain distinguishable downstream. -/

abbrev FactSet (F : Type) := F → Prop

/-- Monotonicity as a property a merge either has or lacks. L5 is the
    assertion that the implemented merge has it. -/
def Monotone {F : Type} (merge : FactSet F → FactSet F → FactSet F) : Prop :=
  ∀ a b f, a f → merge a b f

/-! `monotone_under_source_addition` stood here and was **empty** — its
proof body was `hmono a b f`, the hypothesis applied to its own
arguments. It elaborated, carried no `sorry`, and established nothing.
The corrected header note then vouched for it as "proved", which is
true and is exactly why the note was not sufficient: *proved* and
*establishes something* are different properties, and only the second
is what this file is for. Found by a claims sweep (BV1).

L5 was never discharged by proving an implication from its own
hypothesis. It is discharged by an implementation **exhibiting**
`Monotone` for its actual merge — and the file's contribution is to say
what that rules out. -/

/-- Retraction by deletion violates L5, exhibited rather than asserted.
    `merge a b := b` discards everything in `a`. -/
theorem retracting_merge_not_monotone :
    ¬ Monotone (fun (_ b : FactSet Unit) => b) := by
  intro h
  exact h (fun _ => True) (fun _ => False) () trivial

/-- Union is monotone, so L5 is satisfiable — the obligation is real
    rather than impossible. Together with the above, `Monotone` is a
    property that genuinely separates merges. -/
theorem union_merge_monotone {F : Type} :
    Monotone (fun (a b : FactSet F) => fun f => a f ∨ b f) :=
  fun _ _ _ ha => Or.inl ha

/-! ### Correction versus supersession — a condition, not a theorem

`correction_distinct_from_supersession` stood here, universally
quantified over `corrects` and `supersedes`, and was **false as
stated**: take both relations to be the same one and each conjunct
asserts `P ∧ ¬P`. Its `sorry` could never have closed either.

The error was of kind, not of detail. Distinguishability is not a
property that holds of arbitrary relations — it is an **adequacy
condition an implementation must exhibit**. Naming it as a definition
and proving that the collapsed implementation fails it says the true
thing, and says it without a `sorry`. This is C13 stated where it can
be checked. -/

/-- The adequacy condition C13 requires: each relation holds somewhere
    the other does not. -/
def Distinguishes {F : Type} (corrects supersedes : F → F → Prop) : Prop :=
  (∃ x y, corrects x y ∧ ¬ supersedes x y) ∧
  (∃ x y, supersedes x y ∧ ¬ corrects x y)

/-- Machine-checked refutation of the statement that stood here: it
    quantified over all pairs of relations, and the diagonal breaks it. -/
theorem refute_correction_distinct :
    ¬ (∀ (F : Type) (corrects supersedes : F → F → Prop),
        Distinguishes corrects supersedes) := by
  intro h
  obtain ⟨⟨_, _, hc, hs⟩, _⟩ := h Unit (fun _ _ => True) (fun _ _ => True)
  exact hs hc

/-- **The true statement, and it needs no `sorry`.** One relation used
    for both jobs cannot satisfy the condition — which is exactly C13's
    complaint about a model that carries supersession alone. An
    implementation discharges C13 by exhibiting `Distinguishes` for its
    own two relations; it cannot be discharged in general. -/
theorem collapsed_implementation_fails {F : Type} (r : F → F → Prop) :
    ¬ Distinguishes r r := by
  rintro ⟨⟨_, _, hc, hs⟩, -⟩
  exact hs hc

/-! ### Tying C13 to the merge (BV2)

`Distinguishes` alone is not C13. It ranges over arbitrary relations
with no tie to `FactSet`, to `merge`, or to monotonicity — so an
implementation could exhibit it for two relations having nothing to do
with the merge and read as having discharged the claim.

C13 sits next to L5 for a reason: correction and supersession must be
**distinguishable** *and* both recorded additively, under a merge that
**does not retract**. That pairing is the condition; neither half
implies the other, which is why both must be exhibited. -/

/-- The condition C13 actually requires. -/
def AdequateC13 {F : Type}
    (merge : FactSet F → FactSet F → FactSet F)
    (corrects supersedes : F → F → Prop) : Prop :=
  Distinguishes corrects supersedes ∧ Monotone merge

/-- The halves are independent: a monotone merge tells you nothing about
    whether the two relations are distinguishable. Witness: union, which
    is monotone, paired with one relation used for both jobs. -/
theorem monotone_does_not_give_distinguishes {F : Type} (r : F → F → Prop) :
    Monotone (fun (a b : FactSet F) => fun f => a f ∨ b f) ∧
    ¬ AdequateC13 (fun (a b : FactSet F) => fun f => a f ∨ b f) r r :=
  ⟨union_merge_monotone, fun h => collapsed_implementation_fails r h.1⟩

end HazardVocab.Merge
