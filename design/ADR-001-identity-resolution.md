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

## Prior art — the reference implementation already does option B

From `docs/sources/HDC-data-source-register.html`, category 08:

> An identity is built from the first field that actually exists — ICAO
> hex, then alternative ICAO fields, then registration, then callsign,
> then a position-derived fallback — and if none of those yield
> anything, the aircraft is not rendered at all.

This is precedence-ordered alias resolution with a declared authority
order and an explicit refusal in place of a guess. It is option B,
implemented, and it was adopted in response to a real defect: rows
arriving with a blank identifier field collapsed onto one record, so
the map could follow one aircraft while the panel described another.

Two things this establishes:

- Option B degrades gracefully on records lacking an authoritative
  identifier, which was the objection to it.
- The refusal case matters. "Not rendered at all" is the behaviour that
  distinguishes B from A — A would have merged them.

This does not decide the ADR. Aircraft identity is a simpler problem
than incident identity (no complexes, no mereology, no multi-agency
republication), and L2 is still unresolved. But it is evidence, and it
is evidence from production rather than from reasoning.

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