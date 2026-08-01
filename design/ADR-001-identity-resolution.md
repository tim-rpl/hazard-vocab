# ADR-001 — Identity resolution strategy

**Status:** proposed — BLOCKED pending L2
**Date:** —

## Context

Source records arrive with partial identifier sets. Define
`ids(r) : Set (Scheme × Value)` and a match relation over records.

Claim L2 asserts that heuristic matching (normalized name plus rounded
centroid) is reflexive and symmetric but **not** transitive. Confirm L2
in `design/Identity.lean` before completing this ADR — the counter-
example is what forces the choice below.

## Options

| Option | What it means | Obligation |
|---|---|---|
| A — transitive closure | Union-find over the match graph | Over-merges. Must bound cluster size or diameter and prove the bound |
| B — authority only | Heuristic match never establishes identity, only *suggests* it | Free, given L1. Costs recall on records lacking authority IDs |
| C — policy clustering | Heuristic proposes, a resolution policy disposes | Must prove the policy is order-independent — not free |

## Decision

TBD.

Leaning B: heuristic matches recorded as `candidateMatch` facts rather
than identity facts. They stay in the store, remain queryable and
auditable, and never silently fuse two distinct entities. Option A is
what naive pipelines do implicitly, without the bound.

## Obligation

- If A: state and prove the cluster bound. New claim.
- If B: none beyond L1. Add a recall metric to `claims.md`.
- If C: prove policy order-independence. New claim, and it is the
  hardest of the three.

## Consequences

TBD.
