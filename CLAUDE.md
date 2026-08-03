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

4. **Only SHACL-*generable* constraints belong in LinkML.**
   Expressibility is necessary and not sufficient. `sh:equals` is SHACL
   Core, works, and is the constraint that makes claims.md C5 true — and
   linkml 1.11.1 accepts both `equals_expression` and a class-level
   `rules:` block carrying it, exits 0, and emits **no cross-slot
   construct at all**. A constraint can satisfy "SHACL-expressible" and
   vanish silently.

   **The test is what appears in `build/shapes.ttl`,** not what the
   source language accepts. If a constraint matters, assert its
   generated form — the same discipline P6a's criteria now use.

5. **Prefer mixins and slot reuse over `is_a` depth.** Slots are
   first-class. Deep inheritance is the thing that migrates worst.

6. **Role, not subtype.** Entities are declared once in Part 0. Parts
   1-7 assign roles in relations. There is no `ExposedElement` class
   and no `Resource` class — there is an `Asset` that appears in an
   exposure relation and in an assignment relation. See ADR-002.

7. **Every class and slot needs a `description` and an `examples`
   entry.** Free documentation and grounding for both humans and
   models, and the only guard claims.md C6 has.

   Enforced by `drift-lint.py`'s `documented` rule, which also rejects
   placeholder descriptions (`TODO`, `TBD`, `FIXME`, and the like).
   Before that rule existed this invariant said "Lint enforces it" and
   nothing did — a schema with eight classes, twelve slots, `TODO`
   throughout and zero examples passed clean. See claims.md C20.

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

At the end of every stage, post to `review-inbox.md` in the format
defined in `.claude/rules/gate-messages.md`, then **stop and wait for
O**. Do not begin the next
stage until O has replied. Address every `blocked` finding first.

## Who writes what

One writer per file. Anyone else who wants a change requests it through
`review-inbox.md`.

| File | Writer | Others |
|---|---|---|
| `vocab/`, `codelists/`, `transform/` | H | hook blocks O |
| `docs/coverage.md` | H | O falsifies statuses; H applies |
| `design/ADR-*` | H, at design gates | O cannot read them |
| `design/lean/`, `design/alloy/` | H | O may read and run |
| `claims.md` | O (status, evidence, updated) | H proposes new claims in gate messages |
| `review-inbox.md` | both, append-only | own message formats |
| `README.md` | human | H proposes corrections in the gate |
| `CLAUDE.md`, `FALSIFIER.md`, `Makefile`, `scripts/`, `.claude/` | human | governance config and tooling |
| anything not listed | human | ask in the gate before editing |

`README.md` is the human's because it carries commitments — status,
licence, and how the method is described — not only descriptions. When
it goes stale, H reports the staleness as a finding rather than fixing
it.

The three READMEs under `vocab/profiles/`, `codelists/`, and
`fixtures/` ARE H's. They document H's own directories.

**Default deny.** If a file is not in this table, it is the human's.
H asks in the gate rather than assuming.

**Tooling changes are declared, not discovered.** A change to
`scripts/`, `Makefile`, or `.claude/` gets an assertion in the next
`[H → O]` message naming what changed and what verifies it. H did not
make the change and must verify rather than trust it; O verifies
deliberately rather than discovering it several gates later.

**A declared change is verified by a second instrument, never by the
one that made it.** An editing script reporting success is not evidence
the edit landed — a bare `str.replace` against a string that has moved
matches nothing, returns silently, and lets the script print that it
succeeded. That has now shipped twice from two independent workers,
including once in a repair for the same defect.

So: the editing step must **fail loudly on a missed target**, and the
result must then be confirmed by something else — `grep` the file,
`git diff` the commit, mutate and re-run. Confirming that a file is
*present* is what a declaration already asserts. Confirming what is
*in* it is the check.

**For a retraction, search for the retracted string, not the
replacement.** Grepping for the text you just wrote proves the new text
is present. It cannot see the old claim still standing three sections
down, and a statement withdrawn in one place and surviving in another is
worse than one never withdrawn — the document now disagrees with itself
and the reader has no way to tell which is current.

This has produced three residues across three accepted ADRs in one
round, each in a section a reader takes as authoritative. The check that
finds them costs one `grep -n` per retracted phrase, against every file
that could carry it — not only the file you edited.

`make lint-selftest` enumerates every rule/fixture pair by name and
fails on any fixture no case references, so the tooling's own coverage
is inspectable rather than asserted. See
`scripts/lint-fixtures/README.md`.

**A `covered` status in `docs/coverage.md` is an assertion H is
making.** O may falsify it — "you marked X covered, here is a case it
does not handle" — and reports that in `[O → H]`. H applies the
correction. O never edits the file.

The same holds for `claims.md` in reverse: H may propose a new claim or
a restatement, but only O changes a status.

## Source of truth for source data

`docs/sources/HDC-data-source-register.html` is the authoritative
inventory of what the reference implementation reads: 29 external
services in 11 categories, with per-source verification status, item
IDs, endpoints, and refresh behaviour. It supersedes any earlier
source table in this repository or in a prompt.

It also records defects and the correctness rules that came out of
them. Those are design input, not trivia — read them before modelling
the category they belong to.

## The conventions are bets, not settled law

Every convention in this repository — the epistemic-kind segmentation,
the entity core, role-not-subtype, the four modalities, declarative
capture — was decided analytically before any vocabulary existed. None
has yet met the material.

**If authoring vocabulary feels like fighting a convention rather than
being guided by it, that is a finding.** Report it in the gate. Do not
work around it silently, and do not treat a convention as load-bearing
because it is written down.

The Part 2 / Part 3 split is the one most likely to break first: it
contradicts ISO 19156, which treats a simulation result as an
`Observation` with a simulation-typed procedure. See ADR-003, which is
open.

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
  INSPIRE. Prefixes live in `vocab/prefixes.yaml`.
- Code lists are SKOS concept schemes, versioned independently of the
  schema. LinkML enums reference them via `PermissibleValue.meaning`.
- One ADR per structural decision, in `design/`. Numbered, dated,
  never edited after acceptance — supersede instead.