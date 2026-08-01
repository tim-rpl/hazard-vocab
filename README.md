# Canonical Hazard Vocabulary

A declarative, multi-hazard vocabulary for emergency and hazard data —
the reference model that source feeds are transformed into.

- **Structure** — LinkML (`vocab/`)
- **Code lists** — SKOS concept schemes (`codelists/`)
- **Transformation** — Datalog / Mangle (`transform/`)
- **Design checking** — Lean and Alloy (`design/`)

Everything in `build/` is generated. The source of truth is `vocab/`.

## Parts

Segmented by **epistemic kind**, not subject matter. Weather and air
quality are not parts — they appear in Part 2 as observations and
Part 3 as forecasts, the same class with different procedures.

| Part | Scope |
|---|---|
| 0 | Foundation — identity, time, geometry, coverage, sampling, agents, provenance |
| 1 | Hazard — process, event, area, intensity, cascade relations |
| 2 | Observation — sensed state |
| 3 | Model — forecast, interpolation, derivation |
| 4 | Exposure — exposed elements, vulnerability, risk |
| 5 | Response — incidents, resources, assignments, missions |
| 6 | Warning — zones, protective actions, alerts |
| 7 | Context — terrain, hydrography, transport, land cover |
| R | Registry — observable properties, units, code lists (cross-cutting) |

Parts form a module dependency order: Part *n* may reference Parts < *n*,
never >.

## Status

Pre-alpha. See `claims.md` — most claims are `asserted` and untested.
Do not depend on this yet.

## Layout

```
vocab/core/         Parts 0-7, jurisdiction-neutral
vocab/profiles/     hazard and jurisdiction bindings
codelists/          SKOS concept schemes (Turtle)
transform/          Mangle/Datalog rules
design/             Lean, Alloy, ADRs — never executed in production
fixtures/           real captured payloads
build/              GENERATED
```

## Development

See `CLAUDE.md` for invariants. See `FALSIFIER.md` for the
falsification pass charter.

```
make gen && make check
```

## License

TBD — intended to be open source.
