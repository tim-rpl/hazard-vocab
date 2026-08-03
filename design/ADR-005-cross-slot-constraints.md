# ADR-005 — How cross-slot constraints reach validation

**Status:** accepted
**Date:** 2026-08-02

Decides plan item **P18**. This is C5's carrier, and C5 is the only
external claim in the register.

## Context

Experiment `docs/experiments/exp-01-property-substitution.md` established
three things by measurement:

1. A composite AQI evaluated against a **PM2.5-specific** statutory
   threshold — the defect the source register records, which shipped for
   four builds — **validates clean** against generated SHACL.
2. A hand-written `sh:equals` **catches it exactly**, rejecting the
   substitution and passing the correct case.
3. LinkML accepts `equals_expression` and a class-level `rules:` block
   and **emits nothing for either**, exit 0, no warning.

So the constraint is expressible in the target language and not
generable from the source language. Invariant 4 was corrected in
consequence: *generable*, not *expressible*.

Three options were on the table.

| Option | Cost |
|---|---|
| **A** — hand-written SHACL merged beside generated | Breaks **invariant 1**: `make check` reads `build/shapes.ttl` only, `make gen` regenerates it wholesale, and nothing under `build/` may be hand-edited |
| **B** — a generator emitting cross-slot constraints from LinkML `annotations:` | Preserves single-source. Real work |
| **C** — accept cross-slot constraints as out of scope | Loses C5's only affirmative evidence |

## Decision

**Option B.** Cross-slot constraints are declared in LinkML
`annotations:` and emitted as SHACL by a project generator that runs
after `gen-shacl`.

**Why not A.** Invariant 1 is what makes `build/` trustworthy. A
hand-maintained shapes file beside a generated one is a second copy of
the constraint set — the defect that consumed the plan gate, in the one
directory the project has declared must never be hand-edited.

**Why not C.** C5 is the only external claim in the register and has
been unanswered since it was written. `exp-01` produced its first
affirmative evidence. Choosing C discards that evidence *and* leaves the
motivating defect uncatchable — a determination assistant that cannot
tell a composite index from the quantity a statute names.

**Why `annotations:` and not `rules:`.** `annotations:` survives
`make gen` as data and is a LinkML core construct. `rules:` and
`equals_expression` are on C4's watch list as non-portable, and
`exp-01` showed they are also non-*functional* — a stronger reason,
and one that does not depend on ever migrating.

## What this costs, and where it lands

**It is not free and it is not in this unit.** The generator is real
work, and the scope statement of plan 01 — *Part 2 plus the Part 0
fragment it depends on, bound, generating SHACL, validated against
captured payloads* — does not require it.

**So C5's affirmative evidence depends on work outside plan 01, and that
should be recorded rather than smoothed over.** The plan carries the
implementation as an item excused from plan 01 with that reason stated.
C5 stays `asserted`: the shape that would make it true is now decided
and owned, and is not yet built.

This resolves the contradiction O found in P18's bookkeeping — *"a
design-gate decision"* offered as a reason to excuse an item whose own
notes said C5 had nothing to rest on without it. The decision belongs
here and is made; the implementation belongs to a later unit and is
named.

## Obligation

- A new claim when the generator exists: *every cross-slot constraint
  declared in `annotations:` appears in `build/shapes.ttl`*. Falsifier:
  one that does not.
- The `sosa:observedProperty` case from A34 and the `us_aqi` case from
  `exp-01` are its first two test cases.
