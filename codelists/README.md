# Code lists

SKOS concept schemes in Turtle, versioned independently of the schema.

Referenced from LinkML via `PermissibleValue.meaning`. Never inline a
code list as a bare LinkML enum — that forces a schema version bump on
every terminology change and loses hierarchy, cross-scheme mapping, and
per-concept deprecation.

Reuse before authoring. Dereferenceable schemes already exist for:

- physical quantities — CF Standard Names via NERC NVS2 collection P07
- units — QUDT

Author locally only where nothing exists. Known gaps: protective
actions, hazard mereology (incident complexes), and derived indices.

Cross-scheme mapping is what earns SKOS its place: Oregon Level 1/2/3
to California Warning/Order is `skos:closeMatch`, not a lossy enum
merge.

## The gap is protective actions, not evacuation levels

Naming the gap "evacuation levels" understates it, and the
understatement is the kind that gets designed into a scheme and then
has to be undone.

ADR-002 rescoped Part 6 from evacuation to **protective actions**.
Evacuate is one protective action. Shelter in place is another, and it
is not a level on the same ladder — it is the opposite instruction,
issued under a different hazard, and a scheme built as an ordered
evacuation ladder has nowhere to put it. So are: close a road, close an
airspace, boil water, mask or limit outdoor exertion, curtail
operations, ban burning, restrict access. The Oregon
Ready / Set / Go ladder is one jurisdiction's ordering of one action
type, which makes it a good `skos:orderedCollection` inside the scheme
and a bad shape for the scheme itself.

Two consequences for whoever authors this:

- The top-level scheme is **action kind**, not level. Ordering is a
  property of some branches and not others, and it is
  jurisdiction-specific where it exists — so it belongs in a
  jurisdiction profile's collection, not in the core scheme's
  hierarchy. Building level-ordering into the concept hierarchy is how
  the scheme acquires a US-Pacific-Northwest shape it cannot later
  shed.
- `skos:closeMatch`, not `skos:exactMatch`, across jurisdictions. It is
  already the right relation for Oregon Level 1/2/3 to California
  Warning / Order, and it is more obviously right once the scheme
  covers actions that only some jurisdictions issue at all.

Note that no standard vocabulary exists for any of this
(`docs/coverage.md`, "Protective action levels"). This is the one place
in the repository where authoring rather than binding is the expected
outcome, which raises rather than lowers the bar on getting the axis
right.

## Derived indices have no external scheme either

Composite air-quality indices — US AQI and the per-pollutant sub-indices
published alongside it — have no CF standard name and no QUDT unit,
because they are neither physical quantities nor units. They are
piecewise functions of a quantity, defined by regulation and revised by
regulation.

They therefore need a local SKOS scheme, and the reason to be careful
is recorded in the source register: a statutory threshold expressed in
µg/m³ was tested against a composite index, and ozone alone pushed the
index past the trigger with no smoke present. A scheme that lets the
index and the quantity it derives from occupy the same slot reproduces
that defect. Keep the index concepts distinguishable from the CF
concepts they derive from, and record the derivation.
