# ADR-007 — No class in this model has a complete predicate set, so no shape is closed

**Status:** proposed
**Date:** 2026-08-07

Supersedes **ADR-005's Obligation property 1** and nothing else. ADR-005
is accepted and is not edited; properties 2 and 3 stand as written and
are load-bearing here.

## Context

ADR-005 Decision B put a second producer on `build/shapes.ttl` — a
project generator running after `gen-shacl` — and bounded it with three
properties. The first is quoted in full, to its end, because its last
sentence is the clause most adverse to this decision:

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

**What forced the question.** `gen-shacl` publishes a **closed** shape
for every non-abstract class. Measured against one fixture, closure
produced four `ClosedConstraintComponent` violations on textbook PROV-O —
including `prov:generatedAtTime` rejected on the only class PROV-O
declares it for, the single external term this project deliberately
reuses.

LinkML cannot express a per-class fix. `shaclgen.py` computes closure as
`self.closed and not (c.mixin or c.abstract)`: the flag is global and the
only per-class lever is a class's modelling status. So the constraint is
**SHACL-expressible and not LinkML-generable**, and a post-process is the
only stage that can carry it — which property 1 forbids, because the fix
is a deletion.

## The scope this decision replaces, and what falsified it

**An earlier ruling drew the line at authorship**: closure over a class
this project does not own is an authority claim it has no standing to
make; closure over a locally authored class is legitimate. Four shapes
would lose the triple and four would keep it.

**That line does not hold, and a measurement broke it.** With external
closure already removed and `owl-time.ttl` loaded as an ontology graph
under RDFS inference, the locally authored `TemporalExtent` shape rejects
`time:hasTime`. Read out of the graph:

```
time:hasBeginning -> rdfs:subPropertyOf time:hasTime
time:hasEnd       -> rdfs:subPropertyOf time:hasTime
```

`TemporalExtent` is ours, closure over it was legitimate under the
authorship rule, and it rejects a triple **entailed by the vocabulary it
binds by slot**.

**`sh:closed` is a claim about a predicate set, and entailment enlarges
predicate sets.** Authorship was never the boundary.

**And it generalises past the one class.** Every locally authored,
non-abstract class in the fragment binds at least one external term, so
every one has a predicate set an external vocabulary can enlarge:

| Class | External term it binds |
|---|---|
| `Identifier` | `prov:generatedAtTime` |
| `Asset` | `sosa:isHostedBy` |
| `Place` | `geo:hasGeometry` |
| `TemporalExtent` | `time:hasBeginning`, `time:hasEnd` |

Those are exactly the four the authorship rule would have kept closed.

## Decision

**Property 1 is replaced by:**

> **1. Deterministic and idempotent.** The generator's output is a
> function of `vocab/`. **The whole pipeline is idempotent: `gen-shacl`
> followed by the stage, run twice over unchanged sources, produces
> byte-identical `build/shapes.ttl`.** No step's result depends on the
> order in which steps ran.
>
> Stated over the pipeline rather than over the stage, because *running
> the stage over its own output changes nothing* is trivially true of any
> deletion and asserts almost nothing. The pipeline is what the cheapest
> test below measures, and an obligation that says less than its own test
> is how a criterion drifts from what it verifies.
>
> The generator may add, remove or rewrite any triple, subject to that
> property alone. What is forbidden is a step whose effect a second run
> could resolve differently — an edit made by judgement, by matching
> prose, or by any rule not stated in the generator.

**And the rule this licenses, unconditional:**

> **`sh:closed` and `sh:ignoredProperties` are removed from every shape.**

## Why no shape is closed, in order of weight

**1. No class in this model has a complete predicate set.** External
classes because we do not own them; local classes because entailment
enlarges them, as the measurement above shows. There is no third
category in the fragment.

**2. Closure contradicts the profile mechanism.** A profile adding a slot
is what T2 exists for. Under closure, a profile-added predicate is a
violation unless the core shape enumerated it in advance — so closure and
extensibility are in direct conflict, and extensibility is the point of
the model.

**3. `sh:ignoredProperties`-with-enumeration has no ceiling.** Keeping
closure and listing the entailed predicates requires every
`rdfs:subPropertyOf` chain above every bound term, refetched whenever an
external vocabulary moves. `adms` moved under this project inside one
week — the source document changed and the namespace began serving
`text/html`. That is a maintenance obligation with no bound, for a
property nothing has asked for.

## The loss, recorded because it is real

**An unexpected predicate on an instance is no longer a validation
error.** A typo'd slot name, a stray triple: not caught.

**Why it is cheap here.** The validation this model needs is whether an
observation's epistemic kind is declared, whether its feature of interest
is present, whether a comparison is well-typed. Closure catches none of
that. And empirically: one fixture has ever run against these shapes, and
closure produced **four false violations on textbook PROV-O and zero true
ones.**

**If it later matters**, the remedy is a targeted `sh:closed` on a class
with no external bindings and no profile extension point. **No such class
exists today**, and the table above is the measurement.

## Measured, three states

Same fixture, `owl-time.ttl` loaded as an ontology graph:

| Shapes | none | `-i rdfs` | `-i owlrl` |
|---|---|---|---|
| as generated | 5 | 7 | — |
| external closure removed | 1 | **3** — the two extras are `time:hasTime` | — |
| **all closure removed** | **1** | **1** | **1** |

The remaining violation is `geo:asWKT`'s datatype in every case, which is
a separate defect and has nothing to do with closure. **18 triples
removed, 9 `sh:targetClass` retained** — every binding survives.

**The literal one-triple edit does not work and its failure looks like
success.** Deleting `sh:closed` while leaving `sh:ignoredProperties`
gives `ConstraintLoadError: You can only use sh:ignoredProperties on a
Closed Shape`, and **pyshacl validates nothing** — five violations to
zero by not running. That is why the rule names both triples, and it is
also why the add/remove/modify axis is the wrong frame: **the axis counts
triples; the property that matters counts whether the output is
reproducible.**

## Why the add/remove/modify axis is dropped rather than widened

**`additive` was a proxy, and the thing it stood for is properties 2 and
3.** What the obligation protects against is two producers that can
fight: a build where the artifact depends on who ran last. Determinism
and idempotence forbid exactly that, and they forbid it for additions
too — an addition made by judgement is as unreproducible as a deletion.

**The axis cannot be widened, only dropped.** Lifting the ban on
*removal* alone still prohibits `sh:closed false`, which is a
**modification**, and a property that permits deleting a triple while
forbidding overwriting it draws a line where nothing turns on it.

**One earlier draft of this decision said the output must be derivable
from the source, and that was false when the rule was
namespace-scoped** — it keyed on `scripts/project-namespaces.txt`, which
is not under `vocab/`. **The unconditional rule removes the key**, so the
output is a function of `vocab/` alone and the property holds as
originally worded. The defect went away with the scope rather than being
worded around.

## The entailment-regime question, answered

**OHIM's shapes are regime-independent for closure.** The measurement
above gives one violation under no inference, RDFS and OWL-RL alike, so
no regime declaration is needed for this constraint and no ADR is needed
to make one.

That does not settle every entailment question — a future constraint
might depend on a regime — but it removes the only place a regime
currently changes the verdict.

## What this forecloses

**A post-process that cannot state its rule is now forbidden outright.**
Under property 1 such a step was permitted so long as it only added;
under determinism it is forbidden however it edits. A narrowing, and the
part of the trade worth naming.

**And the project loses `additive` as a cheap read.** A reviewer could
previously confirm compliance by checking that no generated triple
disappeared. Now they must run the build twice and diff, then with the
steps reversed and diff again — which is ADR-005's own cheapest test,
unchanged, and the reason properties 2 and 3 are not superseded.

## Obligation

- **The cheapest test is ADR-005's and is not weakened:** `make gen`
  twice and `diff`; then with the post-step order reversed and `diff`
  again. Both empty. **That run pair is the idempotence test as well as
  the determinism test** — it is `gen-shacl`-then-stage twice, which is
  exactly what the property now asserts.

- **`sh:path` counts must parse, not grep.** If the post-process
  reserialises through `rdflib`, predicate order and prefix form change,
  and every criterion counting `sh:path` occurrences by string breaks.
  F31 already rules those criteria must parse; **this decision makes that
  mandatory rather than advisable.**

  **So the order is: parse first, then the stage.** F31 is open, and if
  the stage lands while three criteria still grep, all three break on the
  same run for a reason unrelated to what they measure. Sequenced here
  rather than discovered — this ADR creates a dependency on a fix that has
  not shipped, and naming it is cheaper than meeting it by accident.

- **The rule is asserted against the generated file, not the generator.**
  Invariant 4, and both halves, because the second is the direction where
  a rule that strips too much would hide:

  1. after the stage runs, **no shape carries `sh:closed` or
     `sh:ignoredProperties`**;
  2. **the count of `sh:targetClass` after the stage equals the count
     before it.**

  **The second is a conservation property and not a number, deliberately.**
  An earlier draft asserted *all nine `sh:targetClass` remain*. Nine is
  the class count on the day it was written: P6b adds `candidateMatch`,
  Part 1 adds classes, and the assertion goes false while the property it
  protects still holds — the hardcoded-figure defect this project has
  recorded four times, here inside an obligation that outlives the gate
  that wrote it. Conservation guards the same direction and cannot go
  stale.

## Consequences

**This does not license the stage's existence** — ADR-005 Decision B
already did — and it does not decide whether such a stage is in scope for
review under charter v15 §0. The stage lives in `scripts/`, which §0
places out of scope, and writes `build/shapes.ttl`, which §0 lists in
scope as generated output. **That boundary is untested and this is the
first artifact to sit on it.** A question for the charter, not for this
ADR.

**The falsifier.** A pipeline run whose output differs between two
invocations; one whose effect depends on step order; a removal the
generator's stated rule does not produce; or **a class in this model with
a complete predicate set** — no external bindings, no profile extension
point — for which closure would be sound and is now forbidden.
