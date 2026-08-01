namespace HazardVocab

/-- An identifier: a scheme plus a value within that scheme. -/
structure Ident where
  scheme : String
  value  : String
deriving DecidableEq, Repr

/-- A source record as it arrives from a feed, before canonicalisation.
    `idents` may be empty — partial identification is the normal case. -/
structure Record where
  source     : String
  idents     : List Ident
  name       : String
  centroid   : Int × Int   -- scaled fixed-point lat/lon
deriving DecidableEq, Repr

/-- A scheme is *functional* over a record set when each record carries
    at most one value in it. Required for L1 transitivity. -/
def Functional (s : String) (rs : List Record) : Prop :=
  ∀ r ∈ rs, ∀ v₁ v₂,
    ⟨s, v₁⟩ ∈ r.idents → ⟨s, v₂⟩ ∈ r.idents → v₁ = v₂

/-- A scheme is *injective* over a record set when a value denotes at
    most one real-world entity. This cannot be proved from the data —
    it is an assumption about the issuing authority, and belongs in the
    profile that declares the scheme. -/
axiom SchemeInjective : String → Prop

end HazardVocab
