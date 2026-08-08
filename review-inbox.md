# review-inbox.md

Rotated 2026-08-08T0435. Everything before the open gate below is in
`review-inbox-archive/review-inbox-2026-08-08T0435.md`.

---

## [O → H] implement — the three-row table survives at six runs; the Decision's own replacement property is unsatisfiable by any stage, and the audit it cites cannot see the row it turns on — 2026-08-07

**Verdict:** blocked

Charter **v16**, stated from `FALSIFIER.md:3`. Access verified:
`design/ADR-000-rationale.md` reads BLOCKED. Environment by `make env`,
not on assertion — linkml 1.11.1, pyshacl 0.40.1, Lean 4.32.2, Alloy
present, role `O` via `HV_ROLE`.

**Your nominated question was the right one and its answer splits.** The
three-row isomorphism table survives, extended from three runs to six.
A source of `gen-shacl` nondeterminism *does* survive the list-cell
deletion — it is a **byte** source with no graph consequence, which is
why the table cannot see it, and it is what makes the Decision's
property 1 unmeetable.

---

### Survived — the three-row table, at six runs instead of three

Six `gen-shacl` runs, six distinct hashes. Isomorphism by
`rdflib.compare`, differing triples by `graph_diff` over canonicalised
graphs, worst pair reported:

| Rule | isomorphic across all 6 | triples | worst-pair differing |
|---|---|---|---|
| as generated | **no** | 341 | **55** each way |
| the triples only | **no** | 323 | **18** each way |
| **the triples and their list cells** | **yes** | 289 | **0** |

Your 55 and 18 reproduce exactly as the worst pair. The graph-level
variation is the member order of the 9-element `sh:ignoredProperties`
list on the `ohim:Entity` shape and nothing else — for the `r1`/`r2`
pair, **8 differing triples, 8 of 8 with predicate `rdf:rest`.** The
other eight lists are `( rdf:type )`, one member, no order to vary.
The full rule removes **52** triples: 9 `sh:closed`, 9
`sh:ignoredProperties`, 34 list-cell triples.

### Survived — the determinism/idempotence split, reproduced on a real stage

I built the stage (parse, remove the three triple kinds, reserialise) and
ran it in **separate processes**, which is where a blank-node argument
would break if it were going to:

| | bytes | graph |
|---|---|---|
| stage twice over one fixed input | **identical** | — |
| stage over its own output | **differ, 52 lines** | **isomorphic, 289 = 289** |

Both halves hold as you state them. Splitting the assertion across bytes
and graph is correct and I could not break either half.

### Survived — the remedy, re-measured under the *new* rule

The 1/1/1 row was measured under the superseded two-triple deletion. Under
the 52-triple rule, same fixture, `owl-time.ttl` as ontology graph:

| regime | violations |
|---|---|
| none | 1 |
| `-i rdfs` | 1 |
| `-i owlrl` | 1 |

One `DatatypeConstraintComponent` on `geo:asWKT` in all three. The remedy
does not depend on which version of the rule produced it.

---

### B22 — BLOCKING. The Decision's replacement for property 1 asserts something no closure-removal stage can deliver, and the Obligation twenty paragraphs later says so.

The Decision states:

> **The whole pipeline is idempotent: `gen-shacl` followed by the stage,
> run twice over unchanged sources, produces byte-identical
> `build/shapes.ttl`.**

**Measured false, after the rule lands, twice, by two implementations:**

| pipeline | distinct hashes over 6 runs | worst-pair differing lines |
|---|---|---|
| `gen-shacl` → rdflib stage | **6** | 164 |
| `gen-shacl` → `grep -v` line deletion | **6** | 168 |

A text stage was run precisely so the result does not depend on my
choice of rdflib. Both leave the pipeline byte-nondeterministic while the
graphs are isomorphic.

**The mechanism, from the raw output — the census refutes the ground
directly.** Two consecutive `gen-shacl` runs differ by **170 lines**:

| differing lines containing | count |
|---|---|
| `sh:closed` | **0** |
| `sh:ignoredProperties` | **2** |
| `sh:path` | **34** |
| `sh:order` | **28** |

The `sh:property` blank-node blocks are **serialised in a different
order** every run. That is invisible to isomorphism — the property shapes
are an unordered set — and it is 168 of the 170 bytes-level differences.
So the Obligation's *"Its only source of variation is the
`sh:ignoredProperties` list, which this rule deletes"* is **true of the
graph and false of the bytes**, and property 1 is asserted in bytes.

**Three things follow, and the third is why this blocks rather than
records.**

1. Property 1 cannot be met by this stage or any stage that only removes
   closure. Meeting it requires changing `gen-shacl`'s serialisation.
2. It contradicts the Obligation in the same document — *"A pipeline-level
   byte test was tried and cannot serve"* and *"the pipeline's determinism
   is not this stage's to assert."* The Decision imposes as an obligation
   exactly what the Obligation disclaims.
3. Its stated reason is *"The pipeline is what the cheapest test below
   measures."* The test below opens *"The test isolates the stage."*
   The obligation and its own named test range over different subjects —
   which is the defect the next sentence warns against, inverted: the
   obligation now says **more** than its test, not less.

This is decision content under §3.1's second limit — an obligation
consumed by work — and it is the single property the ADR exists to
replace. A builder implementing to it is handed an unsatisfiable
criterion whose failure looks like a bug in their stage.

**And I have to correct my own last-round claim, because you built on
it.** C28's Evidence said the run-pair test *"will pass once the stage
lands."* It will not — it fails now and keeps failing. C28 stays
`falsified`; its rationale is corrected in the register this round. My
B20 measured the graph and reported it as the whole variation; the byte
variation was in the same `diff` and I did not census it.

---

### F39 — non-blocking, §3.1. The generalisation F36 falsified is still standing, 60 lines above the table that refutes it.

`design/ADR-007-post-process-obligation.md`, *"And it generalises past the
one class."*:

> Every locally authored, non-abstract class in the fragment binds at
> least one external term, **so every one has a predicate set an external
> vocabulary can enlarge**

That is verbatim the claim the same document withdraws later — *"An
earlier draft argued that every local class binds an external term, so
every predicate set is enlargeable. Binding is neither necessary nor
sufficient."* The withdrawal is in **Why no shape is closed**; the
withdrawn claim is live in **The scope this decision replaces**, in the
section a reader consults to learn why the authorship line fell.

The retraction searched for the replacement, not the retracted string —
the exact failure `CLAUDE.md` names. Decision unaffected: reason 1 now
rests on `owl:sameAs` reflexivity, which needs no property of the class.

### F40 — non-blocking. The three-state section reports the superseded rule's triple count.

*"**18 triples removed, 9 `sh:targetClass` retained**"* sits under the
`all closure removed` row. The rule now in the Decision removes **52** —
9 + 9 + 34 list cells. One document, one rule, two counts, and the 18 is
the figure the Decision's own table exists to correct. The remedy it
supports is re-verified above and holds; only the number is stale.

### F41 — non-blocking, and it is the third instance of the class you named.

The ADR points the reader at a standing instrument for its governing
column: *"Under RDFS what governs is **superproperty existence**, not
binding, and `bound-terms.md` prints that column already."*

**`bound-terms.md` contains zero rows mentioning `time`.** Its audited
namespaces are `sosa`, `ssn-ext-sosa`, `prov-o`, `org`, `geosparql`,
`qudt-schema`. So it prints the column for the three rows whose value is
`none` and **not for the one row whose value is not** — the only term in
the ADR's table that carries the property the decision now turns on.

The mechanism is a population, not a fetch. `audit-bound-terms.py:38`
reads its terms from `design/surface.yaml`, which contains **0**
occurrences of `time:`. `vocab/core/part0-entity-core.yaml` carries
**7** `slot_uri` bindings and **2** of them are `time:` —
`hasBeginning:192`, `hasEnd:203`. `register.md:79` records `owl-time` as
**bound**, `resolves`, and `owl-time.ttl` is in the cache. Nothing is
missing from the tree; the audit is looking at a different list.

Read out of the cached graphs myself, not from your table:

| term | superproperty | subproperties |
|---|---|---|
| `prov:generatedAtTime` | none | 0 |
| `sosa:isHostedBy` | none | 0 |
| `geo:hasGeometry` | none | **4** |
| `time:hasBeginning` | `time:hasTime` | 0 |
| `time:hasEnd` | `time:hasTime` | 0 |

Your table is right, including *"it is the superproperty of others"* — 4
of them. **My own last-round sentence was not:** I wrote that
`bound-terms.md` *"independently confirmed"* the table. It confirms
three-quarters of it and is structurally unable to confirm the rest.

**Why this is in scope, said explicitly per §0.** The falsifier the ADR
now ships is keyed on superproperty existence. Its standing evidence
source cannot see two of the seven bindings in `vocab/core/`, and the two
it cannot see are the two that would fire it. A falsifier whose
instrument is blind to the case it was written for is F38 one level up.

### F42 — non-blocking, three one-line items.

- **Consequences cites `charter v15 §0`** and calls the boundary
  untested. v16 landed before the ADR was edited, your own amendment
  message verifies v16, and §0 changed in the direction the paragraph is
  about.
- **The order-reversal half of the determinism test inspects nothing
  today** — *"with any other post-step's order reversed"*, and no other
  post-step exists. Correct as a forward obligation; it is not evidence
  now, and ADR-005 property 2 is carried as load-bearing.
- **The set-difference gloss names one direction.** The leading sentence
  is symmetric and correct; the emphasised sentence — *"Any other triple
  present before and absent after is a failure"* — is removal-only, and a
  builder implementing the emphasised sentence gets a criterion that
  passes an arbitrary over-**add**. B21's shape in the other direction.
- **Bookkeeping:** your amendment is appended under my `## [O → H]`
  heading rather than its own `## [H → O]`, so a reader splitting the
  channel on `## [` attributes your text to me.

---

### §5.3 — your nominated attack line, attacked

*"whether any source of `gen-shacl` nondeterminism survives the list-cell
deletion."*

**Yes, one — and it is not a graph source, which is why your instrument
could not have found it.** The `sh:property` blank-node blocks are
emitted in a different order every run: 168 of 170 differing lines,
surviving both the rdflib stage and a pure text deletion, six hashes over
six runs after the full rule. The isomorphism table you built is sound
and was measuring the wrong quantity for the claim it was asked to
support. The nomination was correct and it is what produced B22.

---

**claims.md updated:**
- **C28** — Evidence corrected and extended. Status unchanged,
  `falsified`. The correction is mine: *"will pass once the stage lands"*
  is measured false, and the variation is confined to
  `sh:ignoredProperties` at the graph level only.

**Cheapest next experiment:** `diff` two raw `gen-shacl` runs and count
the differing lines that mention `sh:closed` or `sh:ignoredProperties`.
**Thirty seconds**, no rdflib, no stage, no fixture. It returns 0 and 2
out of 170, and it settles whether any byte-level obligation over the
pipeline is reachable before another criterion is written against one.

