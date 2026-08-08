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

**And it generalises past the one class** — though **not** by the route
this section first gave, which is withdrawn here and not only in *Why no
shape is closed* below. It argued that every local class binds an external
term, and that binding therefore made every predicate set enlargeable.
**Binding is neither necessary nor sufficient**; see reason 1, where the
ground is `owl:sameAs` reflexivity under OWL-RL, which needs no property
of the class at all.

What the four have in common is a fact, not a mechanism:

| Class | External term it binds | Superproperty? |
|---|---|---|
| `Identifier` | `prov:generatedAtTime` | none |
| `Asset` | `sosa:isHostedBy` | none |
| `Place` | `geo:hasGeometry` | none — it *is* the super, of 4 |
| `TemporalExtent` | `time:hasBeginning`, `time:hasEnd` | **`time:hasTime`** |

Those are exactly the four the authorship rule would have kept closed —
**and only one of them is enlargeable by RDFS.** The table refutes the
generalisation it was offered as evidence for.

## Decision

**Property 1 is replaced by:**

> **1. Deterministic and idempotent.** **The stage's** output is a
> function of its input. Run twice over one fixed `build/shapes.ttl`:
> byte-identical. Run over its own output: the **graph** is unchanged —
> **isomorphic, not byte-identical**, because reserialising relabels blank
> nodes. No step's result depends on the order in which steps ran.
>
> **The pipeline's byte-determinism is not asserted and is not
> reachable.** `gen-shacl` orders the `sh:property` blank-node blocks
> differently on every run; that is `claims.md` C28, `falsified`, and it
> is not this stage's to fix.
>
> The generator may add, remove or rewrite any triple, subject to that
> property alone. What is forbidden is a step whose effect a second run
> could resolve differently — an edit made by judgement, by matching
> prose, or by any rule not stated in the generator.

**And the rule this licenses, unconditional:**

> **`sh:closed` and `sh:ignoredProperties` are removed from every shape,
> together with the RDF list cells reachable from each removed
> `sh:ignoredProperties`.**

**The list cells are not a detail.** Removing the `sh:ignoredProperties`
triple alone orphans its list, and the orphaned cells are the entire
source of `gen-shacl`'s nondeterminism. Measured over three runs, by
graph isomorphism rather than by hash:

| Rule | graphs isomorphic across runs | triples |
|---|---|---|
| as generated | **no** — 55 differ | 341 |
| the triple only | **no** — 18 differ, all `rdf:first`/`rdf:rest` | 323 |
| **the triple and its list cells** | **yes** | 289 |

So a rule naming only the triple achieves neither the deletion it
intends nor the determinism its obligation asserts.

## Why no shape is closed, in order of weight

**1. No class in this model has a complete predicate set.** External
classes because we do not own them. Local classes because **`owl:sameAs`
reflexivity under OWL-RL adds a predicate to every instance**, whatever
the class binds — so no closed shape survives OWL-RL at all, and the
conclusion needs no property of the class.

**The ground this replaces was falsified, and it was falsified by
evidence already printed on every `make lint`.** An earlier draft argued
that every local class *binds an external term*, so every predicate set
is enlargeable. Binding is neither necessary nor sufficient. Measured, in
the graphs this project caches:

| Bound term | Superproperty |
|---|---|
| `prov:generatedAtTime` | **none** |
| `sosa:isHostedBy` | **none** |
| `geo:hasGeometry` | **none** — it *is* the superproperty of others |
| `time:hasBeginning` | `time:hasTime` |

**One of four.** Under RDFS what governs is **superproperty existence**,
not binding, and `bound-terms.md` prints that column already — **as of this round.**
It did not when the sentence was first written: the audit's population was
a hardcoded list of six namespaces with no OWL-Time entry, so
`bound-terms.md` had **zero** rows mentioning `time` and could not print
the one value the falsifier turns on. F41. The population is now read from
`vocab/core/`, and the two `time:` bindings are audited. This is
ADR-003's pattern a second time: the stated ground fails and the decision
holds on a stronger one.

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
a separate defect and has nothing to do with closure.

**The row measures the superseded two-triple rule and removed 18
triples.** The rule now in the Decision removes **52** — 9 `sh:closed`,
9 `sh:ignoredProperties` and 34 list-cell triples — and the remedy was
re-measured under it: **1 violation under none, RDFS and OWL-RL alike.**
All 9 `sh:targetClass` survive either way. One document must not carry two
counts for one rule, and 18 is the figure this table exists to correct.

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

**The 1/1/1 row is vacuous as evidence of regime-independence, and
saying otherwise was a tautology.** It is measured *after* every
`sh:closed` is removed — and closure is the only construct in these
shapes whose verdict a regime could change. So no regime can alter a
closure verdict once closure is gone; the row restates the deletion
rather than testing anything about regimes.

**What survives is smaller and is not vacuous:** the one remaining
violation, `geo:asWKT`'s datatype, is **stable across all three
regimes** — no inference, RDFS, OWL-RL. That is a real measurement about
one constraint, and it is the whole of the claim.

**So no regime declaration is needed for closure**, because closure is
gone. Whether a future constraint needs one is open, and this decision
does not answer it.

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

- **The test isolates the stage, and its two halves are measured
  differently for a reason.**

  > **Determinism.** Run the stage twice over the **same**
  > `build/shapes.ttl` and `diff` — empty. Then with any other post-step's
  > order reversed and `diff` — empty.

  **The order-reversal half inspects nothing today**, because no other
  post-step exists. It is a forward obligation and not present evidence,
  and ADR-005 property 2 is what it carries forward. Stated here because a
  criterion that cannot fail reads as a criterion that passed — and this
  ADR's own falsifier ships that distinction.
  >
  > **Idempotence.** Run the stage over its own output: the **graph** is
  > unchanged. Not the bytes.

  **Determinism is a byte property over a fixed input** — verified,
  byte-identical over two runs on one input, because the stage is a pure
  deletion.

  **Idempotence cannot be a byte property.** Re-serialising relabels blank
  nodes, so a second pass that removes nothing still changes the bytes.
  Measured: byte-identical **False**, graph unchanged **True**. Asserting
  it in bytes would fail for a reason that has nothing to do with the
  stage.

  **A pipeline-level byte test was tried and cannot serve — and an earlier
  draft of the Decision asserted it anyway.** `make gen` is not
  byte-deterministic and does not become so when the rule lands.

  **Censused over LIST MEMBER ORDER, not over predicate objects, because a
  count over blank nodes is undefined until you say how they are named.**

  Which predicates even admit a label census is a property of the schema
  and is measurable:

  | predicate | object kind | comparable across parses |
  |---|---|---|
  | `sh:closed` | Literal | yes |
  | `sh:path` | URIRef | yes |
  | `sh:order` | Literal | yes |
  | `sh:ignoredProperties` | **BNode** | **no** |
  | `sh:property` | **BNode** | **no** |
  | `sh:in` | **BNode** | **no** |

  **So an earlier draft's *"exactly one predicate varies"* was an artifact
  of the reading.** It compared object multisets; rdflib relabels blank
  nodes on every parse, so the three predicates that read as invariant are
  the three pointing at labelled things, and the one that read as varying
  was reporting its list head's label. Four vary or none do depending on
  how bnodes are identified — it was never a fact about the graph.

  **The census that is a fact about the graph, over eight runs:**

  | list | members | distinct member orders |
  |---|---|---|
  | `ohim:Entity` `sh:ignoredProperties` | 9 | **8** |
  | the other eight `sh:ignoredProperties` | 1 | 1 each |
  | **`sh:in`** — the `AliasKind` enum, **not deleted by this rule** | 2 | **1** |

  **`sh:in` is the control and it could have gone the other way.** It is a
  blank-node list this rule leaves in place. Without it the census supports
  *blank-node lists vary*, which is a claim about rdflib; with it the claim
  is **one nine-member list is emitted in an arbitrary order**, which is a
  claim about `gen-shacl` and is what this decision needs.

  **The byte difference is a different quantity and it survives the
  deletion.** The `sh:property` blank-node blocks are *serialised* in a
  different order every run — invisible to isomorphism, because property
  shapes are an unordered set — so the pipeline stays byte-nondeterministic
  after the rule. Reproduced with a pure `grep -v` text stage as well as an
  rdflib one: **three runs, three hashes.** A pipeline byte obligation
  fails now and keeps failing.

  **An earlier draft censused this by GREP and the figures were wrong in
  both directions**, reporting `sh:closed` 0 and `sh:ignoredProperties` 2 as
  stable. Over all fifteen pairs of six runs, `sh:closed` gives **0 or 2**
  and `sh:ignoredProperties` gives 2. **A grep over a unified diff counts
  lines inside changed hunks, not differing content** — a `sh:closed` line
  identical in both runs enters the census because a neighbour moved. That
  is a fact about grepping diffs and not about any predicate, and it will
  recur anywhere a diff is counted rather than parsed.

  Two readings were wrong before the list census was right, and the rule
  from both is one sentence: **say what a figure counts — and if it counts
  blank nodes, say how they are named, or the figure is reporting the
  parser.**

  **And the pipeline's determinism is not this stage's to assert.** It is
  `gen-shacl`'s, it is filed at C28 as `falsified`, and a stage obligation
  ranging over it holds this project responsible for a dependency's
  behaviour.

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

- **The rule is asserted against the generated file, not the generator**
  (invariant 4), as a **set difference**:

  > The graph after the stage differs from the graph before it **only** by
  > triples whose predicate is `sh:closed` or `sh:ignoredProperties`,
  > together with the RDF list cells reachable from the latter. **Any
  > other difference in either direction is a failure** — a triple present
  > before and absent after, or absent before and present after.

  **Two weaker criteria were tried and both admitted a broken build.**

  The first asserted *all nine `sh:targetClass` remain*. Nine was the
  class count that day; P6b and Part 1 make it false while the property it
  protects still holds — the hardcoded figure, and the first instance
  inside an obligation that outlives its gate.

  The second replaced it with **conservation** of that count, and it is
  worse. A maximal over-strip — `sh:closed`, `sh:ignoredProperties` **and
  all 40 `sh:property` triples** — passes it: 9 targets before, 9 after,
  deterministic, `Conforms: True`, **zero violations. Nine shapes
  constraining nothing, reported as success.** Conservation counts shapes,
  not what is in them; a stale number was replaced by a criterion guarding
  the wrong noun.

  The difference assertion catches that over-strip on its first run and
  carries no number at all.

## Consequences

**This does not license the stage's existence** — ADR-005 Decision B
already did — and it does not decide whether such a stage is in scope for
review under §0.

**Charter v16 answers it, and the answer came from this ADR's own first
case.** §0 now reads *in scope for what it produces, and for any property
of the produced artifact that only two or more runs can reveal* —
determinism, idempotence, order-independence. The stage lives in
`scripts/`, which §0 places out of scope, and writes `build/shapes.ttl`,
which §0 lists in scope as generated output; **a cross-run property is in
scope by the amendment.**

An earlier draft of this paragraph cited **v15** and called the boundary
untested. It was tested — by B20 — and v16 landed before this paragraph
was last edited.

**The falsifier.** Any of:

- **the stage** producing different output from two runs over one input,
  or output depending on step order;
- a removal the generator's stated rule does not produce, or any triple
  removed that the difference assertion does not license;
- **a class in this model whose predicate set no entailment regime can
  enlarge** — no bound term with a superproperty, no bound term that is
  itself a superproperty, and closed under `owl:sameAs` reflexivity — for
  which closure would be sound and is now forbidden.

**The third is stated over superproperty existence, not over binding.** An
earlier version asked whether a class *binds an external term*, which is
the ground F36 falsified: three of four bound terms have no superproperty.
A falsifier keyed on binding is conservative — it will not wrongly
overturn the decision — but **it cannot detect the case it was written
for**, which is this project's fixture-that-cannot-fail defect in a
falsifier.
