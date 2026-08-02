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

`bound-vocabularies.yaml` is the standing guard against F11 recurring:
the allowlist was originally populated from a partial reading of the
conventions section it exists to serve. Adding a vocabulary to
`CLAUDE.md` without adding it here will now fail loudly.