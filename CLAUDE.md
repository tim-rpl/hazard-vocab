# OHIM — Operational Hazard Information Model

A declarative, multi-hazard information model for **live** hazard and
emergency data. LinkML for structure, SKOS for code lists, Datalog for
transformation. Namespace `https://w3id.org/ohim/`.

*"Operational" is the posture — live acquisition rather than
retrospective integration — not the subject. See `README.md`.*

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

You are **H** (the OHIM builder) unless a `.role-O` marker file
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

**`review-inbox.md` is tracked, not ignored.** It is the gate
protocol's only record, and a role that can read committed state but not
your working tree cannot verify against it. That cost a disposal: two
proposed claims could not be ruled on because the `[H → O]` message
existed in neither the working tree nor git, so the wording was
unavailable and §1 forbids O inventing it.

Archiving is not a substitute. An archive holds what was rotated out; an
untracked live file holds what is current, and any working-tree loss
takes it with no recovery and no trace.

**Tooling changes are declared, not discovered.** A change to
`scripts/`, `Makefile`, or `.claude/` gets an assertion in the next
`[H → O]` message naming what changed and what verifies it. H did not
make the change and must verify rather than trust it; O verifies
deliberately rather than discovering it several gates later.

**A rename has as many subjects as the thing has names — and one of
them may be a common noun that must not be renamed at all.**

Measured on this project's own rename, from `hazard-vocab` to `ohim`:

| Subject | Example | Action |
|---|---|---|
| the **URI** | `https://w3id.org/hazard-vocab/` | rename |
| the **prefix** | `hv:` | rename — a separate substitution |
| the **name** | `# Canonical Hazard Vocabulary` | rename |
| the **self-description** | *"a declarative, multi-hazard **vocabulary**"* | rename — the project changed genre, so the word is stale |
| the **common noun** | *"the one published hazard **vocabulary** advertising this"*, about someone else's artifact | **leave** — renaming it makes the sentence false |

The URI and the prefix are two substitutions, not one. Applying the
first and not the second left a `default_prefix` naming a prefix that no
longer existed — the lookup failed open, the fixture passed on its `id:`
alone, and the selftest still read 8/8. Silent in one file, cosmetic in
another, green in both.

The self-description is the one a census misclassifies as generic,
because it uses the same word the common noun does. The test is not the
word; it is **whether the sentence is about this artifact.**

And exclude generated and archived material from the census population.
`.lake/build/**` is gitignored and rewritten on the next build;
`review-inbox-archive/**` is a historical record, and rewriting an
archive makes it say something that was never said. Use `git ls-files`.

**A generated artifact is a whole file, never a region inside one.**
A generated block embedded in a hand-written document has two writers —
a generator that owns the block and an author who rewrites the document
— and the author wins silently. The register is now `register.md`,
generated, with nothing else writing it.

The instance behind the rule, stated so it is checkable:

- A **working-tree** rewrite of `vocab/external/README.md` dropped its
  `BEGIN/END GENERATED:register` markers. **It was never committed in
  that state** — every committed revision that carried the register
  carried the markers, with the block's row count tracking the sidecars
  at each. So the loss is *invisible in git history*, and a reader
  checking this account against the commits will find nothing. That is
  the whole of what an untracked working-tree event looks like.
- The row counts reported during the no-op period **did not come from
  the generator's output.** The old `sync_register()` had its `print`
  after its `return`, so a run with the markers absent produced no
  output at all. They came from a **remembered earlier run** whose
  numbers were true when printed and had since stopped being true — a
  distinct and worse case than reading a stale file, because there was
  no read.

An earlier version of this paragraph said the counts came from the
generator's output. That clause was not reproducible from the
repository.

Where a document must show generated content, it links to the generated
file rather than embedding it. Any generator that cannot find its target
**fails loudly** — a sync that returns quietly when its markers are
absent is the "inspected nothing" shape inside a generator instead of a
check.

**And every generator runs in `make lint`.** An instrument nobody
invokes is an instrument nobody runs, and a check that exists only as a
command someone must remember is not a guard. Three defects shipped in
one round because the register generator's own checks had no target.

**"Inspected nothing" splits two ways, and only one of them passes.**

| Case | Verdict | Why |
|---|---|---|
| the **input** is empty — no schema files under the scanned path | **note and pass** | an expected state; failing would block every run until content exists. Say so in the output: *"no schema files found — these rules inspected nothing."* |
| the **tool** is absent — a tracked generator is not on disk | **fail** | not an expected state. The tree is broken, and a soft note there reports a clean run over a missing check |

Both print the same sentence and mean opposite things, which is why they
must be distinguished at the point of the check rather than left to a
reader.

*The example for the first case used to be "`vocab/core/` holds one
`.gitkeep`". It no longer does — `prefixes.yaml` landed 2026-08-06, and
`drift-lint.py` inspects a real authored file for the first time. The
rule is unchanged; its illustration was the thing that expired.*

**Mutate a copy, never the working tree.** This applies to every role.
`cp` the file or the tree to a scratch path outside the repository,
mutate there, measure, discard. Do not edit a tracked file and restore
it — not with `git restore`, `git checkout --`, `git checkout-index`,
`git stash`, or by writing the original bytes back from memory.

**Why, stated because both roles did it for a whole session.** An
in-place mutate-and-restore worked every time until a scaffolding command
overwrote an uncommitted edit in the file it was verifying. It was caught
because a count went 7 then 6, and recoverable because the file had been
diffed beforehand. **Both were luck, and that a practice worked every
time is the property that makes it unsafe rather than the outcome.**

`FALSIFIER.md` §1 states this for O, whose write scope makes any tree
write a breach. It is here because the risk is the same for H and the
scope rule is not what makes it unsafe — the overwrite is.

A tracked probe that copies is not an exception to remember; it is the
shape. Two of this project's probes already do it, and the shell
one-liners beside them did not.

**A claim about a file's contents is checkable by whoever reads it, and
the writer's ownership of that file is not evidence for it.** Ownership
decides who may change a file. It says nothing about what is in one.
Grep before relaying a stated fact, exactly as you would before
declaring a change — and the same before building on one.

The price, from the instance that produced the rule: **three restatement
passes, four sites reached, one guard rationale built on it, three gate
messages carrying it** — all downstream of a single sentence asserting
that `CLAUDE.md` named ADMS among its bound vocabularies. It never has,
in any revision. The claim was made by the file's own writer, about that
file, without opening it; it was then relayed and sharpened three times
without a grep, because ownership was read as authority.

Every pass was a genuine improvement to a claim with nothing to attach
to. The sharpening was real and the referent was not — which is why
*verify everything* is the wrong lesson and **ownership is not
evidence** is the right one. The check cost one grep and was available
throughout.

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

The Part 2 / Part 3 split was the one flagged as most likely to break
first, because it contradicts ISO 19156, which treats a simulation
result as an `Observation` with a simulation-typed procedure. **ADR-003
is accepted — option B: the parts are merged, and `epistemicKind`
carries the distinction.** Its stated ground was falsified twice and
restated, and the ADR now records that no stated ground discriminates
option B from option A. The decision stands; read the ADR before relying
on any reason for it.

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

- **External vocabularies are referenced by URI, never transcribed.**
  Prefixes live in `vocab/core/prefixes.yaml`.

  **Bound, with a register row and a provenance sidecar:** SOSA, PROV-O,
  QUDT, and CF via NERC NVS2's `standard_name` collection.

  **"Content-verified" means two different things and the register
  distinguishes them; this line must not.** A term read out of a
  **cached graph** by `audit-bound-terms.py` — `sosa`, `ssn-ext-sosa`,
  `prov-o`, `org`, `geosparql`, `qudt-schema`, and nothing else — is a
  stronger claim than a term found in a **live namespace body** by
  `dereferences()`. CF has the second and not the first. So does
  `qudt-units`. **Read `vocab/external/register.md` for which, per
  namespace; do not read a claim about it here.**

  An earlier version of this line said *"at least one probe term read out
  of the graph"*, which is true under one reading and false under the
  other, and `prefixes.yaml` lists `cfsn` among those *"not audited
  anywhere"*. Two current, authoritative files giving a reader opposite
  answers — the ambiguity was in the phrase *the graph*.

  **Committed and not bound: INSPIRE.** Never fetched, no prefix, no
  register row. That commitment is **unmet, not met**, and it is stated
  separately because a list of five reads as five equally grounded
  bindings when four are.

  **The CF route changed 2026-08-06.** This line read *NVS2 collection
  P07*. Same authority, same service — but P07's local parts are opaque
  (`…/P07/current/00B3H4MY/`) and `standard_name`'s are the CF names
  (`…/standard_name/air_temperature/`). **A binding nobody can align by
  eye is unverifiable every time it is made.** All six names are present
  in the graph as typed subjects, verified; **one of them is a `PROBE`
  entry** and the other five reach the register through a substring
  match over payload bytes. The conclusion holds and five-sixths of the
  evidence for it is the weaker test — `nvs-p07` is the control, at 6/6
  present with 0 of 6 as subjects. See `vocab/external/register.md`. P07 stays in the source list as the
  artifact the measurement was made against, `untested` — the honest
  record for something cited and not used.
- Code lists are SKOS concept schemes, versioned independently of the
  schema. LinkML enums reference them via `PermissibleValue.meaning`.
- One ADR per structural decision, in `design/`. Numbered, dated,
  never edited after acceptance — supersede instead.