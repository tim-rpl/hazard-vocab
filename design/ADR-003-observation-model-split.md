# ADR-003 — Whether Part 2 and Part 3 are separate parts

**Status:** proposed — BLOCKED pending the design gate
**Date:** —

## Context

Parts 2 (Observation) and 3 (Model) exist as separate parts. This
contradicts the standard the vocabulary binds to.

**ISO 19156 / OGC OMS treats a simulation result as an `Observation`
with a simulation-typed procedure.** Measurement and forecast are the
same class, distinguished by `procedure`. SOSA/SSN follows the same
pattern. We made the opposite choice and have not defended it in
writing.

This must be settled before Part 2 vocabulary is authored, because it
determines Part 2's shape and every consumer's query surface.

## Options

| Option | Shape | Cost |
|---|---|---|
| **A — separate parts (current)** | Part 2 and Part 3 are distinct modules with distinct classes | Every "all readings regardless of provenance" query becomes a union across parts. Paid by every consumer, forever |
| **B — OMS-native** | One `Observation` class; `procedure` carries the distinction; a **required** epistemic-kind slot with a closed vocabulary; a lint forbidding omission | Distinction is a property, not structure — enforceable by validation but not by module boundary |

## The argument for A, and its weakening

A was chosen so the observed/modelled distinction would be
*structural* rather than a property, and therefore enforceable rather
than conventional. The enforcement mechanism was stratification: no
stratum-0 predicate derivable from a stratum-1 body.

That argument has since been weakened on its own terms (see `claims.md`
L6):

- It constrains **derivation only, not presentation**. It does not stop
  a forecast being rendered in an observation-styled card, which is the
  product property that actually matters.
- The stratum assignment is a judgment call at exactly the boundary
  cases that matter: QC'd and gap-filled monitor readings, data
  assimilation, and interpolated contours that EPA publishes as
  observational products. A compiler check on a wrongly-drawn boundary
  yields false confidence rather than safety.

Option B gets the labelling discipline through a required slot and a
closed vocabulary, without the query cost — and a required slot cannot
be omitted any more than a module boundary can be crossed.

## Decision

TBD at the design gate.

**The bar:** if the reason A is better cannot be articulated beyond
"the distinction feels more important as structure," the split is not
load-bearing and B should win on interoperability alone. Fighting the
standard you bind to needs a stated reason.

## Obligation

- If A: state what B could not enforce, and add a claim with a
  falsifier.
- If B: Parts 2 and 3 merge; renumber or leave Part 3 as a documented
  vacancy. Update `README.md`, `docs/coverage.md`, and ADR-002's
  modality table, which currently maps modalities onto parts.

## Consequences

Either way, the modality axis from ADR-002 survives — four modalities
are a property of statements, not of module boundaries. B relocates
where that property is carried, not whether it exists.