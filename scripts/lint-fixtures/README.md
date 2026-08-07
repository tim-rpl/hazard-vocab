# Lint fixtures

Small LinkML and Lean files with known-correct outcomes, used by
`make lint-selftest` to exercise the rules in `scripts/drift-lint.py`
and `scripts/lean-lint.py`.

**These are not part of the vocabulary.** They live under `scripts/`
deliberately: `make lint` scans `vocab/core/` and `design/lean/`, and
these are purpose-built violations that would fail the build if they
landed there. Lean fixtures live in `scripts/lean-fixtures/` for the
same reason.

## Why they exist

`claims.md` C18 asserts the lint rules detect what they claim to
detect. It has been falsified repeatedly on both precision and recall,
and before these fixtures existed **every firing of every rule had been
a false positive.** A guard with no test is a guard that has only ever
been observed being wrong.

Each fixture is a **regression** for a specific finding, named in its
header comment. Do not edit one to make a rule pass; the fixture records
what the rule got wrong.

## Mutation, not just coverage

A fixture that fires proves the rule fires. It does not prove the rule
fires **because of the thing the fixture is named for.**

`id-claims-foreign-namespace.yaml` was named for the `id:` gate in the
self-reference exemption and never reached it: its `id:` is a
*descendant* of the prefix it would need to exempt, so it fired on the
redirect-service rule instead. Deleting the entire `id:` branch left the
selftest green.

**So: for every guard clause, delete it and confirm a NAMED test
notices.** Not that some test fails — that the test claiming to cover
that clause fails. Three of six mutations run against this linter in one
review changed nothing, and two of those three were the finding.

`lint-selftest` runs one such mutation automatically, on
`project-namespaces.txt`. The rest are manual and belong in the tooling
declaration when a guard changes.

**The probe tests what you suspect; the control tests what you assume.**

Three findings in two rounds came from the control rather than from the
targeted probe: the near-miss control that exposed a rule firing on one
element naming one URI twice, a deictic-cardinality residue found by a
control run against a section nobody was editing, and a staleness test
that passed because its search string targeted a filename where the
generated table renders stems.

A control is not a formality confirming the probe. It is the only part
of the experiment testing the thing you did not think to question — and
a control that cannot fail is indistinguishable from a check that cannot
fire.

## Probe a guard against this project's own discipline, not only against
its target

A guard over prose must be probed against the correction patterns this
project *requires*, not only against the defect it was written for.

A restatement guard shipped during the design gate fired on
*"An earlier draft read 17 bound + 9 local"* — which is a **retraction**,
not a restatement, and every ADR here carries one. It would have failed
`make lint` on the historical record the project is built on, forcing
deletion to make the build pass. That is the opposite of what five
rounds of findings asked for.

The generalisation: **generation does not exempt the generator, and a
guard shipped without adversarial probing is the same artifact class as
a claim shipped without a falsifier.**

## Convention

| | |
|---|---|
| Naming | `<what-it-tests>.yaml`, lowercase, hyphenated |
| Header | A comment saying DELIBERATELY CLEAN or DELIBERATELY VIOLATING, what it tests, and the finding it regresses |
| Registration | Every fixture must appear in at least one `CASES` row in `scripts/lint-selftest.py`. An unreferenced fixture fails the selftest |
| Coverage | Each rule needs at least one **recall** case (must fire) and one **precision** case (must not). `lint-selftest` names any rule lacking recall |

## Current fixtures

The table below is **generated from `CASES` in `scripts/lint-selftest.py`.**
Do not edit it. A hand-maintained table keyed by fixture name is the
defect this project spent four gate rounds on — the corrected version in
one place, the residue in the summary a reader reads. This table went
four fixtures stale within one gate before it was generated.

<!-- BEGIN GENERATED:fixtures -->

| Fixture | Rule | Direction | What it regresses |
|---|---|---|---|
| `bound-vocabularies` | `declared-prefix` | precision | every prefix used is declared |
| `bound-vocabularies` | `jurisdiction` | precision | F11, every vocabulary CLAUDE.md binds |
| `bound-vocabularies` | `shared-uri` | precision | one class, external bindings |
| `clean` | `exact-mappings` | precision | precision |
| `clean` | `inline-attributes` | precision | precision |
| `clean` | `is-a-depth` | precision | precision |
| `clean` | `jurisdiction` | precision | precision |
| `clean` | `role-named` | precision | precision |
| `collision-class-vs-slot` | `shared-uri` | recall | cross-population; kills the one-map repair |
| `collision-permissible-meaning` | `shared-uri` | recall | two PermissibleValue.meaning on one URI |
| `collision-same-as` | `shared-uri` | recall | reached only through same_as |
| `comment-mentions-pattern (.lean)` | `lean-vacuity` | precision | BR-7, the pattern written out in a comment |
| `default-prefix-ancestor` | `jurisdiction` | recall | BV23, default_prefix naming an ancestor of id: |
| `default-prefix-escape` | `jurisdiction` | recall | BV14, default_prefix nominating a foreign namespace |
| `default-prefix-only` | `jurisdiction` | precision | the ONLY case reaching the positive default_prefix branch |
| `flat-siblings` | `is-a-depth` | precision | F2, Part 0 shape |
| `flat-siblings` | `jurisdiction` | precision | precision |
| `flat-siblings` | `role-named` | precision | precision |
| `generic-acronyms` | `jurisdiction` | precision | CRS, UTC, EPSG are not jurisdictions |
| `id-branch-only` | `jurisdiction` | recall | BV25, the ONLY case reaching the id: gate |
| `id-claims-foreign-namespace` | `jurisdiction` | recall | F13 redirect rule; does NOT reach the id: gate (BV25) |
| `jurisdiction-foreign` | `jurisdiction` | recall | a hazard/country never seen here |
| `jurisdiction-in-enum` | `jurisdiction` | recall | F4, no agency in prose |
| `jurisdiction-in-uri` | `jurisdiction` | recall | F12, generic names, agency in the URI |
| `long-acronym` | `jurisdiction` | recall | F13 c3, past every guessed bound |
| `mappings-at-eof` | `exact-mappings` | recall | F3, list ends the file |
| `mixed-construct-identity` | `exact-mappings` | precision | one exact_mappings each, not a len>1 case |
| `mixed-construct-identity` | `shared-uri` | recall | BV3-3, exact_mappings vs another class_uri |
| `near-miss-distinct-uris` | `shared-uri` | precision | distinct URIs; one element naming one URI twice is not a collision |
| `own-namespace` | `declared-prefix` | precision | the project's own prefix, declared |
| `own-namespace` | `documented` | precision | a documented file with examples |
| `own-namespace` | `jurisdiction` | precision | BV8, the project's own id: and default_prefix |
| `own-namespace` | `shared-uri` | precision | distinct URIs |
| `redirect-service` | `jurisdiction` | recall | F13 c1/c2, w3id.org and purl.org |
| `shared-class-uri` | `shared-uri` | recall | C21/B4, two classes on one class_uri |
| `shared-slot-uri` | `shared-uri` | recall | the slot branch, which no fixture reached |
| `undeclared-generic-prefix` | `declared-prefix` | recall | P5 clause 1; sosa: used, not declared |
| `undocumented` | `documented` | recall | C20, placeholder descriptions and no examples |
| `vacuous-theorem (.lean)` | `lean-vacuity` | recall | a theorem concluding True |
| `violating` | `exact-mappings` | recall | recall |
| `violating` | `inline-attributes` | recall | recall |
| `violating` | `is-a-depth` | recall | chain depth 3 |
| `violating` | `role-named` | recall | recall |

*43 rule/fixture pairs across 28 fixtures and 9 rules. Generated by `lint-selftest.py --table`; `make lint-selftest` fails if this block is stale.*

<!-- END GENERATED:fixtures -->

`bound-vocabularies.yaml` is the standing guard against F11 recurring:
the allowlist was originally populated from a partial reading of the
conventions section it exists to serve. Adding a vocabulary to
`CLAUDE.md` without adding it here will now fail loudly.