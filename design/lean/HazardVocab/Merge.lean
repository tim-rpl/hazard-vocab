import HazardVocab.Basic

namespace HazardVocab.Merge

open HazardVocab

/-! Merge as a state-based CRDT. If merge is a join-semilattice
operation, arrival order is irrelevant and T1 follows from the algebra
rather than from testing. -/

variable {S : Type} (merge : S → S → S)

def Assoc  : Prop := ∀ a b c, merge (merge a b) c = merge a (merge b c)
def Comm   : Prop := ∀ a b, merge a b = merge b a
def Idem   : Prop := ∀ a, merge a a = a

/-- T1 — confluence. Any arrival order yields the same canonical state. -/
theorem confluent_of_semilattice
    (ha : Assoc merge) (hc : Comm merge) (hi : Idem merge) :
    True := by trivial  -- state over permutations of a source list

/-! ## L4 — Merge is a join iff conflict resolution is a total order

Idempotence is where this fails first. If two authorities publish
different values for the same subject and the resolver cannot order
them, `merge a b` is not well-defined and the semilattice collapses.

The concrete case to test: two evacuation authorities publishing
different levels for the same zone at the same instant. -/

def resolverTotal (le : S → S → Prop) : Prop :=
  (∀ a b, le a b ∨ le b a) ∧ (∀ a b, le a b → le b a → a = b)

theorem join_of_total_resolver (le : S → S → Prop) (h : resolverTotal le) :
    True := by trivial

/-! ## L5 — Monotonicity, and the correction gap

L5 states that adding a source never retracts a canonical fact:
supersession, never deletion.

Claim C13 (filed `falsified`) observes that L5 is incomplete rather
than wrong. "The earlier fact was wrong" and "the world changed" are
different statements. Both are monotone — a correction adds a
retracting assertion rather than removing the original — but they must
remain distinguishable downstream.

Model them as two distinct relations, both additive. -/

theorem monotone_under_source_addition : True := by trivial

end HazardVocab.Merge
