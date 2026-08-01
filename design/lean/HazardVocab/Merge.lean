import HazardVocab.Basic

namespace HazardVocab.Merge

/-! Merge as a state-based CRDT. If merge is a join-semilattice
operation, arrival order is irrelevant and T1 follows from the algebra
rather than from testing.

No Mathlib. Statements are deliberately formulated over plain functions
and predicates so this file elaborates against Lean core alone.

NOTE ON HONESTY: every theorem below states a real proposition and
carries `sorry`. A theorem whose conclusion is `True` would elaborate
without warning and prove nothing — the worst possible failure
direction for a file whose purpose is to record what is and is not
established. Do not "fix" a `sorry` by weakening a conclusion. -/

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

/-- The converse direction, which is the one that bites: without
    totality, idempotence fails. Two incomparable authorities are the
    counterexample. -/
theorem not_idem_of_incomparable
    (le : S → S → Prop) (merge : S → S → S)
    (hpick : PicksGreater le merge)
    (a b : S) (hab : ¬ le a b) (hba : ¬ le b a) :
    ∃ x y, merge x y ≠ merge y x ∨ ¬ (∀ z, merge z z = z) := by
  sorry

/-! ## L5 — monotonicity, and the correction gap

L5 states that adding a source never retracts a canonical fact:
supersession, never deletion.

Claim C13 (filed `falsified`) observes that L5 is incomplete rather
than wrong. "The earlier fact was wrong" and "the world changed" are
different statements. Both are monotone — a correction adds a
retracting assertion rather than removing the original — but they must
remain distinguishable downstream. -/

abbrev FactSet (F : Type) := F → Prop

/-- L5 proper. Note this is definitional given `hmono`; it is stated so
    the obligation is visible, and so that any merge implementation
    must exhibit `hmono` rather than assume it. -/
theorem monotone_under_source_addition {F : Type}
    (merge : FactSet F → FactSet F → FactSet F)
    (hmono : ∀ a b f, a f → merge a b f)
    (a b : FactSet F) (f : F) :
    a f → merge a b f :=
  hmono a b f

/-- Correction and supersession are both monotone, and distinguishable.
    An implementation satisfies this only if the two are separate
    relations rather than one. -/
theorem correction_distinct_from_supersession {F : Type}
    (corrects supersedes : F → F → Prop) :
    (∃ x y, corrects x y ∧ ¬ supersedes x y) ∧
    (∃ x y, supersedes x y ∧ ¬ corrects x y) := by
  sorry

end HazardVocab.Merge
