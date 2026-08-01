# Profiles

Everything jurisdiction-specific or hazard-specific lives here.

A profile declares:

- which identifier schemes exist and their **precedence order** for
  identity resolution
- which SKOS concept schemes fill which enums
- which authorities are trusted, and their total order for conflict
  resolution (required by claim L4)
- which intensity measure applies to the hazard type
- any additional constraints — profiles may only **add**, never relax
  (claim T2)

## Two axes, not one file

Hazard and jurisdiction are **separate concerns and separate files**.

```
profiles/hazard/wildfire.yaml         which intensity measure, which hazard taxonomy branch
profiles/jurisdiction/us-or.yaml      which identifier schemes, which authorities, which code lists
```

An instance is checked against the **composition** of one hazard
profile and one jurisdiction profile — never against a single file
whose name concatenates both. Composition is conjunction of constraint
sets, which is why `design/alloy/parts.als` proves
`check_compositionPreservesSoundness`: if two profiles each only add
constraints, their composition only adds constraints, and T2 survives
composition rather than having to be re-argued per pair.

The earlier `<hazard>-<jurisdiction>.yaml` naming is superseded
(ADR-002). It was wrong in a way worth naming: it makes the number of
files the product of the two axes rather than their sum, so adding a
second hazard duplicates every jurisdiction file, and a change to
Oregon's authority order has to be applied in as many places as there
are hazards. It also has no place to put a hazard-neutral jurisdiction
fact, which is most of what a jurisdiction profile contains.

If you find yourself wanting to put something here into `vocab/core/`,
re-read invariant 2 in `CLAUDE.md`.
