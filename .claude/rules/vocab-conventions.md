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

1. Fetch the graph and grep for the term. A 200 on a slash namespace
   proves nothing — the whole ontology document is returned for every
   path under it.
2. Does the term's definition match the intended use, or only its name?
3. Is it a role class? If so, do not bind an entity to it.
4. Does it declare a domain and range? A property with neither
   constrains nothing in generated SHACL.
5. Record what you verified and how. Status-code-only is not
   content-verified and must not be recorded as such.

## Checks

`make lint` enforces the mechanical subset. `make lint-selftest`
verifies the lint rules themselves catch violations — see claims.md
C18, which records that no lint rule in this project has ever been
observed catching a real violation.