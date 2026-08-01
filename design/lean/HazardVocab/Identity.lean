import HazardVocab.Basic

namespace HazardVocab.Identity

open HazardVocab

/-! ## L1 — Authority match

Note what this is NOT: an equivalence relation on all records. It is a
*partial* equivalence — symmetric and transitive, but reflexive only on
records that actually carry an identifier in the scheme. Records
lacking one are not related to themselves.

That is the correct behaviour, and it is why the resolution policy in
ADR-001 needs a fallback rather than a total relation. -/

def authorityMatch (s : String) (a b : Record) : Prop :=
  ∃ v, (⟨s, v⟩ : Ident) ∈ a.idents ∧ (⟨s, v⟩ : Ident) ∈ b.idents

theorem authorityMatch_symm (s : String) (a b : Record) :
    authorityMatch s a b → authorityMatch s b a := by
  rintro ⟨v, ha, hb⟩; exact ⟨v, hb, ha⟩

/-- Transitivity requires functionality. Without it, a record carrying
    two values in the same scheme bridges two unrelated entities. -/
theorem authorityMatch_trans (s : String) (rs : List Record)
    (hf : Functional s rs) (a b c : Record)
    (_ : a ∈ rs) (_ : b ∈ rs) (_ : c ∈ rs) :
    authorityMatch s a b → authorityMatch s b c → authorityMatch s a c := by
  sorry

/-- Reflexive only where the scheme is present. -/
theorem authorityMatch_refl_iff (s : String) (a : Record) :
    authorityMatch s a a ↔ ∃ v, (⟨s, v⟩ : Ident) ∈ a.idents := by
  sorry

/-! ## L2 — Heuristic match

**Read this before writing the counterexample.**

Claim L2 as filed asserts heuristic matching is not transitive. Whether
that is true depends on which rule is actually implemented, and the two
candidates fail differently:

* `exactCellMatch` — normalised name equality AND rounded-cell
  equality. Both conjuncts are equalities on projections, so both are
  equivalence relations, and their conjunction IS transitive. L2 is
  FALSE for this rule. The defect is different: boundary artifacts.
  Two records of one fire 100 m apart across a cell edge never match.

* `proximityMatch` — normalised name equality AND centroid within a
  threshold. Proximity is not transitive. L2 is TRUE for this rule.

**First task: determine which one the pipeline implements.** Then prove
the corresponding statement and correct L2 in `claims.md` to name the
rule. An unqualified L2 is unfalsifiable because it does not say which
relation it is about. -/

def normalize (s : String) : String := sorry  -- strip fire/complex/the/incident, punctuation

def exactCellMatch (a b : Record) : Prop :=
  normalize a.name = normalize b.name ∧ a.centroid = b.centroid

def proximityMatch (eps : Int) (a b : Record) : Prop :=
  normalize a.name = normalize b.name ∧
  (a.centroid.1 - b.centroid.1).natAbs ≤ eps.natAbs ∧
  (a.centroid.2 - b.centroid.2).natAbs ≤ eps.natAbs

/-- Exact-cell matching IS transitive. L2 does not apply to it. -/
theorem exactCellMatch_trans (a b c : Record) :
    exactCellMatch a b → exactCellMatch b c → exactCellMatch a c := by
  sorry

/-- Exact-cell matching has boundary artifacts: two records arbitrarily
    close in space can fail to match. This is the defect that replaces
    non-transitivity for this rule. -/
theorem exactCellMatch_boundary :
    ∃ a b : Record, normalize a.name = normalize b.name ∧
      (a.centroid.1 - b.centroid.1).natAbs = 1 ∧ ¬ exactCellMatch a b := by
  sorry

/-- L2 proper: proximity matching is not transitive. -/
theorem proximityMatch_not_trans :
    ∃ (eps : Int) (a b c : Record),
      proximityMatch eps a b ∧ proximityMatch eps b c ∧
      ¬ proximityMatch eps a c := by
  sorry

/-! ## L3 — Identity partitions the record set

Holds for whichever resolution strategy ADR-001 selects. Under option B
(authority only), the partition is the quotient by `authorityMatch`
together with singleton classes for unidentified records. -/

/-- Whichever strategy ADR-001 selects, the resulting relation is an
    equivalence on the records it relates, and canonical entities are
    its quotient. Restate concretely once the ADR is decided — but do
    NOT restate the conclusion as `True`; see the honesty note in
    Merge.lean. -/
theorem identity_partitions
    (rel : Record → Record → Prop)
    (hsymm : ∀ a b, rel a b → rel b a)
    (htrans : ∀ a b c, rel a b → rel b c → rel a c)
    (a b c : Record) :
    rel a b → rel b c → (rel a c ∧ rel c a) := by
  sorry

end HazardVocab.Identity
