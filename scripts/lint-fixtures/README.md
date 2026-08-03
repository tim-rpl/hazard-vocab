# Lint fixtures

Small LinkML schemas with known-correct outcomes, used by
`make lint-selftest` to exercise the rules in `scripts/drift-lint.py`.

**These are not part of the vocabulary.** They live under `scripts/`
deliberately: `make lint` scans `vocab/core/`, and these are
purpose-built violations that would fail the build if they landed
there.

## Why they exist

`claims.md` C18 asserts the lint rules detect what they claim to
detect. That claim was `falsified` twice — once on precision, once on
recall — and every firing of the rules before these fixtures existed
was a false positive. A guard with no test is a guard that has only
ever been observed being wrong.

Each fixture is a **regression** for a specific finding, named in its
header comment. Do not edit one to make a rule pass; the fixture
records what the rule got wrong.

## Mutation, not just coverage

A fixture that fires proves the rule fires. It does not prove the rule
fires **because of the thing the fixture is named for** — and that gap
has now produced ten counterexamples to claims.md C18.

`id-claims-foreign-namespace.yaml` was named for the `id:` gate in the
self-reference exemption and never reached it: its `id:` is a
*descendant* of the prefix it would need to exempt, so it fired on the
redirect-service rule instead. Deleting the entire `id:` branch left the
selftest at 7/7 and green.

**So: for every guard clause, delete it and confirm a NAMED test
notices.** Not that some test fails — that the test claiming to cover
that clause fails. Three of six mutations run against this linter in one
review changed nothing, and two of those three were the finding.

`lint-selftest` runs one such mutation automatically, on
`project-namespaces.txt`. The rest are manual and belong in the tooling
declaration when a guard changes.

## Convention

| | |
|---|---|
| Naming | `<what-it-tests>.yaml`, lowercase, hyphenated |
| Header | A comment saying DELIBERATELY CLEAN or DELIBERATELY VIOLATING, what it tests, and the finding it regresses |
| Registration | Every fixture must appear in at least one `CASES` row in `scripts/lint-selftest.py`. An unreferenced fixture fails the selftest |
| Coverage | Each rule needs at least one **recall** case (must fire) and one **precision** case (must not). `lint-selftest` names any rule lacking recall |

## Current fixtures

| Fixture | Regresses |
|---|---|
| `violating.yaml` | recall for all four drift rules at once |
| `clean.yaml` | precision baseline |
| `flat-siblings.yaml` | **F2** — the Part 0 entity-core shape, depth 1, which the per-file `is_a` count rejected |
| `mappings-at-eof.yaml` | **F3** — two `exact_mappings` with the list ending the file |
| `jurisdiction-in-enum.yaml` | **F4** — a national scheme as a permissible value, no agency in prose |
| `jurisdiction-foreign.yaml` | genericity — `DWD`, `JMA`, from a hazard and country this project has never touched |
| `generic-acronyms.yaml` | precision — `EPSG`, `UTC`, `WKT`, `TAI` are not jurisdictions |
| `jurisdiction-in-uri.yaml` | **F12** — generic names with the jurisdiction carried entirely in `prefixes:` and `slot_uri` |
| `bound-vocabularies.yaml` | **F11** — every external vocabulary `CLAUDE.md` commits to binding must pass |
| `own-namespace.yaml` | **BV8** — the project's own declared namespace must pass |
| `default-prefix-escape.yaml` | **BV14** — `default_prefix` nominating a foreign namespace |
| `id-claims-foreign-namespace.yaml` | F13's redirect rule. **Does not reach the `id:` gate** — see BV25 |
| `default-prefix-ancestor.yaml` | **BV23** — `default_prefix` naming an ancestor of `id:`; the ordinary shape |
| `id-branch-only.yaml` | **BV25** — the only fixture reaching the `id:` gate |
| `undocumented.yaml` | **C20** — placeholder descriptions, no examples |

`bound-vocabularies.yaml` is the standing guard against F11 recurring:
the allowlist was originally populated from a partial reading of the
conventions section it exists to serve. Adding a vocabulary to
`CLAUDE.md` without adding it here will now fail loudly.