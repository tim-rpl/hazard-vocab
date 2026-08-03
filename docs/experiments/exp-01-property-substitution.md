# Experiment 01 — property substitution through `gen-shacl` and pyshacl

**Item:** P15 · **Source:** `FALSIFIER.md` §5.1 question 9
**Run:** 2026-08-02 · **Status:** complete
**Measures:** C5, C17, and the defect the source register records

**Prediction, stated in advance:** *from C17, it conforms* — validation
does not catch the substitution.

**Result: the prediction held, and the second half of the experiment
makes it a more useful answer than a bare confirmation.**

---

## What was run

The defect the register records: until build v84 an Oregon statutory
trigger was evaluated against the composite `us_aqi` index while
Washington's ran on PM2.5. Ozone alone can push a composite index past
101 with no smoke present, which produced an impossible ordering — a
longer Oregon exceedance window than Washington's, when Washington's
lower threshold must always give the longer one.

Modelled as one class carrying both sides of the comparison, so SHACL
has a focus node to work with:

```
ExceedanceCheck
  observedProperty   observedUnit   observedValue
  thresholdProperty  thresholdUnit  thresholdValue
  exceeded
```

| Case | Content |
|---|---|
| **A** — the defect | `observedProperty` = a composite US AQI index, unit `USAQI`, value **160**, evaluated against a **PM2.5-specific** statutory threshold of **35.5 µg/m³** (CF `mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air`, QUDT `MicroGM-PER-M3`), concluding `exceeded: true` |
| **B** — correct | the same threshold against a genuine PM2.5 reading of **8 µg/m³**, `exceeded: false` |

Toolchain: linkml 1.11.1 `gen-shacl`, pyshacl 0.40.1, both from `.venv`.

## Results

| Shapes | Case A (the defect) | Case B (correct) |
|---|---|---|
| **`gen-shacl` output, as generated** | **Conforms: True** | Conforms: True |
| **The same shapes plus a hand-written `sh:equals`** | **Conforms: False** — *"The reading is not of the property the threshold is defined against."* | Conforms: True |

**Two attempts to express the constraint in LinkML, both accepted and
both emitting nothing:**

| Construct | `gen-shacl` | Cross-slot constructs emitted |
|---|---|---|
| `equals_expression: "{thresholdProperty}"` on the slot | exit 0 | **0** |
| a class-level `rules:` block with the same postcondition | exit 0 | **0** |

## What this establishes

**1. C5 — its strongest candidate survives, conditionally, and this is
the first affirmative evidence the claim has had.** The canonical layer
*can* convert this class of silent property-substitution error into a
validation failure: `sh:equals` does exactly that, with a usable
message, rejecting A and passing B. C5 asks whether there is a question
the canonical layer answers that cannot be answered today — *"is this
comparison well-typed?"* is one, and it is answerable in SHACL.

The condition is the whole of finding 2.

**2. C17 — a third axis, and the sharpest of the three.** The gap is
**not** expressive poverty in the target language. SHACL Core carries
`sh:equals` and it works. **LinkML accepts the constraint and generates
nothing**, exit 0, no warning. So:

- axis 1 — JSON-LD expansion silently drops keys absent from the context
- axis 2 — `gen-shacl` never consults the term a `slot_uri` binds, so a
  local range may contradict it (A34)
- **axis 3 — LinkML accepts a constraint expression and emits no shape
  for it**
- **axis 4 — the same, for a *conditional* specifically**, recorded
  2026-08-02 from O's B6 run: class-level `rules:` with real
  preconditions and postconditions, and `annotations:` carrying the same
  conditional, both **exit 0 with empty stderr** and emit
  `sh:condition`, `sh:sparql` and `sh:equals` **zero times**

All four fail toward "pass". The third and fourth are the ones where the
author has done the work, believes the constraint is in force, and is
wrong.

**Axis 4 matters beyond axis 3 because ADR-003 depends on it.** Every
affirmative result in this record is an *equality*. Misassignment of
`epistemicKind` is a **conditional**, so nothing here establishes that
it is catchable — which is why ADR-005 records misassignment as
unenforced **indefinitely** rather than until P19.

**3. Invariant 4 has a gap in its wording.** *"Only SHACL-expressible
constraints belong in LinkML"* sets the bar at SHACL-expressibility.
`sh:equals` clears that bar and is still not generable, so a constraint
can satisfy invariant 4 as written and vanish. **Expressible is
necessary and not sufficient; the test is generable.** Reported for the
design gate, not repaired here.

**4. C4 gains a cheaper argument.** `rules` and `equals_expression` are
already on C4's watch list as LinkML-only and non-portable. They are
also, here, non-*functional* — which is a stronger reason to avoid them
than portability, and one that does not depend on ever migrating.

## Incidental finding, and it bears on P8a

LinkML `float` generates `sh:datatype xsd:float`, while JSON-LD numeric
literals default to `xsd:double`. **Every numeric value in a fixture
fails validation** unless the `@context` types it explicitly. Both cases
above failed on this before the context was corrected, and the failure
message points at the datatype rather than at the context.

P8a authors that context by hand. This is the class of thing that makes
a fixture look broken when the context is what is wrong.

## How to re-run

Schema, both instances, generated and hand-supplemented shapes are
reproducible from the tables above. The experiment needs no `vocab/`
content and neither open ADR bears on it.

**The falsifier for this record:** a `gen-shacl` invocation that emits
`sh:equals`, `sh:sparql`, or any other cross-slot construct from a
LinkML source — which would move finding 2 from the generator to the
author.
