---
paths: vocab/**
description: Declarative authoring conventions — how to avoid importing OO shape
---

# Authoring conventions for vocab/

This vocabulary adopts structure from standards that are UML or OWL
class-shaped — CIM, SOSA/SSN, INSPIRE, ISO 19156. The recurring failure
is importing their *shape* along with their *content*.

## Translate, don't transcribe

ADR-000 D4 covers half the rule: a class with N slots maps mechanically
to an N-ary relation. The other half is the same rule at the
association level and has already been violated once.

**Two association ends with the same range and different semantics is a
UML artifact.** UML cannot say "this relation has a kind," so it splits
into two named ends. Declaratively that is one relation with the kind
as a slot. See ADR-001, the `alias` relation.

The tell: any place the vocabulary ends up with **two slots on one
class that differ only in what they mean**. If you are about to write
that, you are transcribing. Write one slot plus a kind, taken from a
closed vocabulary.

## Slots are first-class

Never use `attributes:` inline on a class. Declare slots at the top
level and reference them by name from `slots:`. This is the difference
between a property-centric and a class-centric model, and LinkML makes
the class-centric path the easier one.

A slot defined once and used by four classes is correct. Four
near-identical slots inlined on four classes is drift, even when the
generated SHACL is identical.

## Composition over inheritance

Prefer `mixins:` and slot reuse. `is_a` depth beyond 2 is drift —
it is the construct that migrates worst (C4) and the one that breaks
locality for a reader or a model trying to understand a fragment
without loading the whole schema (C6).

## One `exact_mappings` per class, at most

`exact_mappings` asserts equivalence. Two of them on one class assert
the two targets are equivalent to each other, which is almost never
true and is exactly the `sosa:Platform` ≡ `sosa:Sensor` bug recorded in
ADR-002.

Use `close_mappings`, `related_mappings`, or `narrow_mappings` unless
equivalence is genuinely intended and stated.

## Roles are relations, not classes

No class may be named for a role something plays: `ExposedElement`,
`Resource`, `Responder`, `Evacuee`, `Observer`, `Reporter`. Entities are
declared once in Part 0; Parts 1–7 assign roles in relations. See
ADR-002 Decision B.

When an external vocabulary offers only a role class — as SOSA does
with `Platform` and `Sensor` — bind the entity and carry the role as a
value. See the `ObjectType` pattern in ADR-001.

## Before binding any external term

1. **Fetch the graph and grep for the term.** A 200 on a slash namespace
   proves nothing — the whole ontology document is returned for every
   path under it.
2. **Does the term's definition match the intended use, or only its
   name?** `sosa:hasMember` reads like a mereological relation and its
   published definition carries no interval, which ADR-002 Decision C
   says is wrong in every case `partOf` covers.
3. **Is it a role class?** If so, do not bind an entity to it.
4. **Does it declare a domain and range?** A property with neither
   constrains nothing in generated SHACL.
5. **Record what you verified and how.** Status-code-only is not
   content-verified and must not be recorded as such.

### Five failure modes measured in published vocabularies

Each of these was found in a real vocabulary this project considered.
None announced itself.

**The namespace has no TLD.** `http://knowwheregraph/ontology/deo#`
resolves for nobody, ever. A vocabulary whose namespace cannot
dereference can only be **borrowed** — copy the structure, cite the
source, author locally, and record that no consumer can fetch it. This
is CIM's position, and it is a property of the namespace rather than a
judgement about the vocabulary's quality.

**The CURIE in the paper is not the URI in the graph.** DMDO's prefix
expands with `#` while every core class is declared with `/`, so
`deo:Hazard` — the form in the published diagram — is declared nowhere,
in any file. **Bind what `grep` finds declared, never a CURIE read from
a diagram, a paper or a table.** Third instance of this shape here: the
SOSA slash-namespace, an `sh:or` count that was a substring of
`sh:order`, and this.

**One concept, two URIs.** `.../deo/Hazard` and `.../dmdo/Hazard` are
the same class in two modules of one release. Check for this before
binding either, and record which one you chose and why — that decision
is not recoverable from the schema later.

**SKOS annotations are not a SKOS concept scheme.** A vocabulary can use
`skos:definition` several hundred times and declare no `skos:Concept`,
no `skos:inScheme` and no `skos:exactMatch`. ADR-000 D5 chose SKOS for
four properties — hierarchy, cross-scheme mapping, per-concept
deprecation, independent versioning — and annotation-only use delivers
at most the first. **Cross-scheme mapping is the one that bites**, since
alignment is the usual reason to adopt an authoritative taxonomy at all.

**A vocabulary may declare a term it does not own.** DMDO declares
`sosa:hasUltimateFeatureOfInterest` as a bare `owl:ObjectProperty`. That
is a stub for local reasoning, not the definition — fetch the owning
namespace for the real one.

### Borrowed, bound, cited

Three relationships, and the distinction decides what a binding is worth.
See ADR-001.

| | Namespace | What it constrains |
|---|---|---|
| **Bound** | dereferences | still only what the local declaration says — `gen-shacl` never consults the term |
| **Borrowed** | does not dereference | nothing. Copy the structure, cite the source |
| **Cited** | irrelevant | documentation only, by intent |

Record which of the three every external vocabulary is, with the
dereference result behind it.

**`vocab/external/register.md` is the register.** It is a **wholly
generated** file, produced from the per-provenance sidecars beside the
cached graphs in `vocab/external/graphs/`. Do not edit it, and do not
add a generated block to `vocab/external/README.md`, which is prose and
hand-written.

An earlier version of this line named `README.md` as the register. That
was true when written and became false when the register moved to its
own file — because a generated block inside a hand-written document has
two writers and the author wins silently. Following the stale line would
rebuild exactly the defect `CLAUDE.md`'s one-writer-per-file invariant
exists to prevent. Retracted here rather than corrected silently,
because this is the file to follow when authoring `vocab/`.

**Keep the cache outside anything the lints scan.** `vocab/core/` and
`vocab/profiles/` are the authored vocabulary; `vocab/external/` is
borrowed material and is not subject to C1, C4, C7, C19, C20 or C21 —
those rules are about what this project declares, not about what other
projects declared. The lint targets are scoped accordingly.

## Checks

`make lint` enforces the mechanical subset. `make lint-selftest`
verifies the lint rules themselves catch violations — see claims.md
C18, which records that no lint rule in this project has ever been
observed catching a real violation.