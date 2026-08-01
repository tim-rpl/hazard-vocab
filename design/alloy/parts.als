// Structural claims about profiles and parts.
// See claims.md T2, C1, C2.
//
// Deliberately tiny — abstraction, not translation. If this grows past
// ~10 signatures you have translated the schema and it will rot.
//
// CONVENTION: a command named demo_* is EXPECTED to be SAT. It exists
// to exhibit a counterexample that justifies a rule. Everything else
// named check_* must come back UNSAT. scripts/alloy.sh enforces this.

module parts

// ---------------------------------------------------------------- parts

sig Part {
  imports : set Part
}

// Parts form a strict dependency order: Part n may reference Parts < n.
fact partsAcyclic {
  no p : Part | p in p.^imports
}

// ------------------------------------------------------------- profiles

sig Constraint {}

sig Instance {
  satisfies : set Constraint
}

one sig Base {
  constraints : set Constraint
}

sig Profile {
  adds  : set Constraint,   // constraints the profile introduces
  drops : set Constraint    // base constraints the profile relaxes away
}

fact dropsAreFromBase {
  all p : Profile | p.drops in Base.constraints
}

// The constraint set an instance is actually checked against.
fun effective [p : Profile] : set Constraint {
  (Base.constraints - p.drops) + p.adds
}

pred valid [i : Instance, cs : set Constraint] {
  cs in i.satisfies
}

// T2 — profile restriction is sound.
// If a profile only ADDS, anything valid under the profile is valid
// under the base. This is the property that lets a wildfire-Oregon
// profile be checked without re-checking the core.
assert check_restrictionSound {
  all p : Profile, i : Instance |
    (no p.drops and valid[i, effective[p]]) implies valid[i, Base.constraints]
}
check check_restrictionSound for 6

// Why the no-drops rule exists. Without it, soundness fails.
// EXPECTED SAT — the counterexample is the point.
assert demo_droppingBreaksSoundness {
  all p : Profile, i : Instance |
    valid[i, effective[p]] implies valid[i, Base.constraints]
}
check demo_droppingBreaksSoundness for 6

// Profile composition: conjunction of two add-only profiles is add-only,
// so composed profiles stay sound. Needed for
// wildfire-profile + jurisdiction-profile.
pred composes [p, q, r : Profile] {
  r.adds  = p.adds + q.adds
  r.drops = p.drops + q.drops
}

assert check_compositionPreservesSoundness {
  all p, q, r : Profile, i : Instance |
    (composes[p, q, r] and no p.drops and no q.drops and
     valid[i, effective[r]]) implies valid[i, Base.constraints]
}
check check_compositionPreservesSoundness for 6
