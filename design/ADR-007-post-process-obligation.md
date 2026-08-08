# ADR-007 — The build's second producer is bounded by determinism, not by addition

**Status:** proposed
**Date:** 2026-08-07

Supersedes **ADR-005's Obligation property 1** and nothing else. ADR-005
is accepted and is not edited; properties 2 and 3 stand as written and
are load-bearing here.

## Context

ADR-005 Decision B put a second producer on `build/shapes.ttl` — a
project generator running after `gen-shacl` — and bounded it with three
properties. The first is quoted in full below, to its end, because its
last sentence is the clause most adverse to this decision and the
proposal that preceded this ADR stopped one sentence short of it:

> **1. Additive.** The generator **extends** `gen-shacl`'s output and
> never modifies or removes a triple it emitted. **A cross-slot
> constraint is a new shape, not an edit to an existing one.**

The other two, unchanged and relied on:

> **2. Order-independent.** Running the generator before or after any
> other post-step yields the same graph. This is T1's property applied
> to the build rather than to the data, and it is required for the same
> reason.
>
> **3. Deterministic.** Two runs over unchanged sources produce
> **byte-identical** `build/shapes.ttl`. Without this, `make gen`
> produces spurious diffs and nobody can tell a real change from
> serialisation noise.

**What forced the question.** P6a's fragment binds four classes to
external classes with `class_uri`, and `gen-shacl` publishes a **closed**
shape over each. Measured against one fixture of textbook PROV-O: four
`ClosedConstraintComponent` violations, including `prov:generatedAtTime`
rejected on the only class PROV-O declares it for — the single external
term this project deliberately reuses. Closure over a `sh:targetClass`
this project does not own is a claim it has no standing to make.

LinkML cannot express the fix. `shaclgen.py` computes closure as
`self.closed and not (c.mixin or c.abstract)`: the flag is global and the
only per-class lever is a class's modelling status. So the constraint is
**SHACL-expressible and not LinkML-generable per class**, and a
post-process is the only stage that can carry it — which property 1
forbids, because the fix is a deletion.

## Decision

**Property 1 is replaced by:**

> **1. Deterministic and idempotent.** The generator's output is a
> function of `vocab/` together with the project's declared namespaces.
> Two runs over unchanged inputs produce byte-identical
> `build/shapes.ttl`, and running the generator over its own output
> changes nothing. **No step's result depends on the order in which
> steps ran.**
>
> The generator may add, remove or rewrite any triple, subject to that
> property alone. What is forbidden is a step whose effect a second run
> could resolve differently — an edit made by judgement, by matching
> prose, or by any rule not stated in the generator.

## Why the add/remove/modify axis is dropped rather than widened

**`additive` was a proxy, and the thing it stood for is properties 2 and
3.** What the obligation protects against is two producers that can
fight: a build where the artifact depends on who ran last. Determinism
and idempotence forbid exactly that, and they forbid it for additions
too — an addition made by judgement is as unreproducible as a deletion
made by judgement.

**And the axis cannot be widened, only dropped.** Lifting the ban on
*removal* alone still prohibits `sh:closed false`, which is a
**modification** and one of the two edits measured to work. A property
that permits deleting a triple and forbids overwriting it is drawing a
line where nothing turns on it.

**The measurement that settles which edit is needed also shows why the
axis is the wrong frame.** Deleting `sh:closed` alone — the edit as first
ruled — leaves `sh:ignoredProperties ( rdf:type )` on a shape that is no
longer closed, which SHACL forbids:

```
ConstraintLoadError: ClosedConstraintComponent: You can only use
sh:ignoredProperties on a Closed Shape (sh:closed).
```

**`make check` then performs no validation at all**, and the violation
count falls from five to zero **by not running.** Deleting both triples
gives one violation, which is the datatype defect that has nothing to do
with closure.

So the correct edit removes **two** triples from each of four shapes.
Under property 1 as written that is twice forbidden; under determinism it
is one rule applied twice. **The axis counts triples; the property that
matters counts whether the output is reproducible.**

## What the rule may key on, stated because *the source* is not enough

The first draft of this decision said the output must be *derivable from
the source*. That is false as stated: the rule keys on
`scripts/project-namespaces.txt`, which is **not under `vocab/`**. It is
tracked, it is already asserted by `drift-lint.py`'s `jurisdiction` rule,
and it today contains exactly one line — `https://w3id.org/ohim/`.

Hence *`vocab/` together with the project's declared namespaces*. The
declared-namespace file is an input to the build on the same footing as
the schema, and pretending otherwise would make the obligation unmeetable
by the rule it was written to permit.

## The rule this licenses, in full

**`sh:closed` and `sh:ignoredProperties` are removed from any shape whose
`sh:targetClass` is not under a namespace listed in
`scripts/project-namespaces.txt`.**

Total, mechanical, and idempotent — a second pass finds nothing to
remove. Measured on P6a's fragment: **four shapes lose both triples**
(`prov:Agent`, `prov:Activity`, `prov:Entity`, `geo:Geometry`); **four
keep them** (`ohim:Place`, `ohim:Asset`, `ohim:Identifier`,
`ohim:TemporalExtent`); and `ohim:Entity` already carries `sh:closed
false` because it is abstract, so it is unaffected either way.

## What this forecloses

**A post-process that cannot state its rule is now forbidden outright.**
Under property 1 such a step was permitted so long as it only added;
under determinism it is forbidden however it edits. That is a narrowing,
not a widening, and it is the part of the trade worth naming.

**And the project loses `additive` as a cheap read.** A reviewer could
previously confirm compliance by checking that no generated triple
disappeared. Now they must run the build twice and diff, then run it with
the steps reversed and diff again — which is ADR-005's own cheapest test,
unchanged, and the reason properties 2 and 3 are not superseded.

## Obligation

- **The cheapest test is ADR-005's and is not weakened:** `make gen`
  twice and `diff`; then with the post-step order reversed and `diff`
  again. Both empty. Idempotence adds one run: the post-step over its own
  output, `diff` empty.

- **`sh:path` counts must parse, not grep.** If the post-process
  reserialises through `rdflib`, predicate order and prefix form change,
  and every criterion counting `sh:path` occurrences by string breaks.
  F31 already rules those criteria must parse; **this decision makes that
  mandatory rather than advisable**, and a criterion still grepping when
  the stage lands is a criterion measuring serialisation.

- **The removal rule is asserted against the generated file, not against
  the generator.** Invariant 4: after the stage runs, no shape whose
  `sh:targetClass` is outside the declared namespaces carries `sh:closed`
  or `sh:ignoredProperties`, and every shape inside them still carries
  both. Both halves, because the second is the over-reach direction.

## Consequences

**This does not license the stage's existence** — ADR-005 Decision B
already did — and it does not decide whether such a stage is in scope for
review under charter v15 §0. The stage lives in `scripts/`, which §0
places out of scope, and writes `build/shapes.ttl`, which §0 lists in
scope as generated output. **That boundary is untested and this is the
first artifact to sit on it.** It is a question for the charter, not for
this ADR.

**The falsifier.** A pipeline run whose output differs between two
invocations; or one whose effect depends on step order; or a removal the
generator's stated rule does not produce. Any of the three falsifies the
property and the decision with it.
