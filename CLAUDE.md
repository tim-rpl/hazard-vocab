# Canonical Hazard Vocabulary

A declarative, multi-hazard vocabulary for emergency and hazard data.
LinkML for structure, SKOS for code lists, Datalog for transformation.

This project is **falsification-driven**. `claims.md` is the source of truth
for what is asserted versus what has been tested.

## Invariants

These are not preferences. Violating one is a bug.

1. **Nothing under `build/` is hand-edited.** Every artifact there is
   generated from `vocab/` via `make gen`. If a generated file needs to
   change, change the source.

2. **No jurisdiction-specific content in Parts 0–7.** Agency names,
   national identifier schemes, and national code lists live in
   `vocab/profiles/`. If `NWCG`, `FEMA`, `IRWIN`, `EPA`, `NIFC`, or any
   other agency name appears in `vocab/core/`, that is a bug — the core
   must retarget to flood or earthquake without edits.

3. **Lean is never extracted to executable code.** `design/` proves
   properties about the design. `transform/` is the implementation.
   They are independent; deleting `design/` must break nothing.

4. **Only SHACL-expressible constraints belong in LinkML.** If a
   constraint cannot survive `make gen`, it does not go in the schema.

5. **Prefer mixins and slot reuse over `is_a` depth.** Slots are
   first-class. Deep inheritance is the thing that migrates worst.

6. **Role, not subtype.** Entities are declared once in Part 0. Parts
   1-7 assign roles in relations. There is no `ExposedElement` class
   and no `Resource` class — there is an `Asset` that appears in an
   exposure relation and in an assignment relation. See ADR-002.

7. **Every class and slot needs a `description` and an `examples`
   entry.** Free documentation and grounding for both humans and
   models. Lint enforces it.

## Roles and the ARC gate

You are **H** (Hazard-Vocab builder) unless a `.role-O` marker file
exists in the project root or `HV_ROLE=O` is set — in which case you are
**O** (Overseer). Read `FALSIFIER.md`; it supersedes this file for your
session.

Check with `make role` if unsure. If you are H and `make role` prints
`O`, stop and say so — the marker was left behind after a review.

H works in four stages, gated:

| Stage | Produces | Not |
|---|---|---|
| **measure** | Blast radius — what exists, what is touched, how big | Any solution |
| **plan** | Sequenced work items in topological order | How to do them |
| **design** | The approach, and what it forecloses | The implementation |
| **implement** | The artifact | Scope beyond the plan |

At the end of every stage, post to `review-inbox.md` in the message
format given there, then **stop and wait for O**. Do not begin the next
stage until O has replied. Address every `blocked` finding first.

## Before implementing

Check `claims.md` and `docs/coverage.md`. Do not build on a claim with status `asserted`
without saying so explicitly in your response.

If a task would require violating an invariant, stop and say so rather
than working around it.

## Layout

```
vocab/core/         LinkML — Parts 0-7, jurisdiction-neutral
vocab/profiles/     LinkML — hazard and jurisdiction bindings
codelists/          SKOS concept schemes (Turtle)
transform/          Mangle/Datalog rules
design/             Lean proofs, Alloy models, ADRs — never executed
docs/coverage.md    capability matrix — what is covered, what is a GAP
fixtures/           Real captured payloads for validation
build/              GENERATED. Do not edit.
```

## Commands

```
make gen      # LinkML -> SHACL, JSON Schema, Mangle decls, docs
make check    # SHACL validate build/ against fixtures/
make lean     # build design/ proofs
make alloy    # run Alloy structural checks
```

## Conventions

- External vocabularies are referenced by URI, never transcribed.
  Bind to SOSA, PROV-O, QUDT, CF (via NERC NVS2 collection P07),
  INSPIRE. - Prefixes are declared once and shared, not repeated per part.
  Target: `vocab/prefixes.yaml`. Not yet authored — see ADR-003.
- Code lists are SKOS concept schemes, versioned independently of the
  schema. LinkML enums reference them via `PermissibleValue.meaning`.
- One ADR per structural decision, in `design/`. Numbered, dated,
  never edited after acceptance — supersede instead.
