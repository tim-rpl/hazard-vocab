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

Naming: `<hazard>-<jurisdiction>.yaml`, e.g. `wildfire-us-or.yaml`.

If you find yourself wanting to put something here into `vocab/core/`,
re-read invariant 2 in `CLAUDE.md`.
