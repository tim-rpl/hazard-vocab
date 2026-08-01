# Code lists

SKOS concept schemes in Turtle, versioned independently of the schema.

Referenced from LinkML via `PermissibleValue.meaning`. Never inline a
code list as a bare LinkML enum — that forces a schema version bump on
every terminology change and loses hierarchy, cross-scheme mapping, and
per-concept deprecation.

Reuse before authoring. Dereferenceable schemes already exist for:

- physical quantities — CF Standard Names via NERC NVS2 collection P07
- units — QUDT

Author locally only where nothing exists. Known gaps: evacuation and
protective-action levels, hazard mereology (incident complexes).

Cross-scheme mapping is what earns SKOS its place: Oregon Level 1/2/3
to California Warning/Order is `skos:closeMatch`, not a lossy enum
merge.
