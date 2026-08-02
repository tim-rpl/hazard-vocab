# Plan 01 — Part 2 (Observation) + the Part 0 fragment it depends on

**Stage:** plan · **Status:** **`blocked`** — three open blocks, unanswered
**Opened:** 2026-08-01 · **Last amended:** 2026-08-02

> **Do not read this document as current.** O's plan-gate block
> verification of 2026-08-02 falsified **PA19** by its own falsifier
> (P5's clause 3 declares the ten local terms, two of which are
> ADR-dependent), found **PG1 still uncleared** at its third rendering,
> and filed **PG8** — the P14→P9 edge exists only as prose in a Notes
> cell. PA4, PA5, PA18, PA19, PA20 and PA22 all rest on points now under
> challenge. See `review-inbox.md`.

Sequenced work items in topological order for the unit measured in
[`measure-01-part2-part0.md`](../measure/measure-01-part2-part0.md).
Items, dependencies and ordering only — *how* is the design stage.

Assertions are numbered **PA1–PA24** to avoid collision with the measure
document's A1–A40. Items are **P1–P15**, with P6 and P8 each split. The
gate message for this document is in `review-inbox.md`.

**Where a summary and the item table disagree, the table governs and the
summary is the bug.** That has now happened twice — the P10 edge
(amendment 3) and the P6b wave rendering (amendment 5, PA20).

## Amendment history

| # | Date | What changed |
|---|---|---|
| 1 | 2026-08-01 | Tooling changed after PA1 was written. PA1 and PA2 restated to current state; PA10 added. |
| 2 | 2026-08-02 | **Form fix.** This document was migrated out of the append-only inbox and kept the inbox's shape: PA1 and PA2 asserted things in the present tense that a later section corrected 235 lines below. In a channel that is correct; in a document it is a false statement with a distant retraction. PA1 and PA2 now state the current position, with what they originally claimed recorded beneath. No plan content changed in this amendment. |
| 3 | 2026-08-02 | **Conflict review — plan content did change.** Ten conflicts and ambiguities found on a read-through of the item table and PA4–PA9. Two would have misled O materially: the **P10 edge was recorded two contradictory ways** (in the sequence *and* as a soft block on the wrong item), and **P6 was blocked on P2 when only part of it is** — the entity and alias core is settled by ADR-001 question 1. Also fixed: P7/P9 double-counting the same slots, an ambiguous order notation that contradicted its own prose, an undefined definition-of-done for P8, inconsistent treatment of tooling as plan items, and an unjustified "early" on P4. New assertions **PA11–PA14**; PA4 and PA6 restated; the item table gained **typed edges**. Net effect on the order: **the critical path is one design-gate turnaround shorter.** |
| 5 | 2026-08-02 | **Block response to O's `blocked` verdict.** **T4 falsified** by O in four minutes — the experiment was on H's own cheapest-test list, and `sosa:madeBySensor`'s cardinality differs by ADR-003 outcome because Open-Meteo publishes no instrument. **The abort condition it was supposed to fire did not fire, because it named the wrong item** (**PA19**): P5 is resolve-and-cache, form is authored at P7, and P7 already waits on P3. PA5's justification withdrawn and re-based on T4a; PA18's T4 clause withdrawn and replaced with the Part 0 case that would genuinely require re-derivation. **PG1** — the wave rendering put P6b on the path to P7 and was cancelling PA11's headline benefit; the item table governs (**PA20**). **PG6** — P8a and the unit done-criteria presupposed option B; both now conditional (**PA21**). **PG2** accepted, M2 dropped from P4. **PG3/PG4** — two new wave-1 items, **P13** (capture rules) and **P14** (the 24-snapshot series, the only uncompressible latency in the plan), and PA17's premise corrected (**PA22**). **PG5** — C12 and C15 scheduled into P6a rather than left silent (**PA23**). **PA6 kept**, per O's ruling. |
| 6 | 2026-08-02 | **P15 and PA24 added from the claims sweep** — the §5.1 question 9 experiment, scheduled into wave 1 with its prediction attached. **Recorded late:** this amendment was made while responding to the claims sweep and no history row was written at the time, which is the omission this table exists to prevent. **It does not address O's second plan-gate verdict** — Blocks A (PA19 falsified), B (PG1, third rendering) and C (PG8, the missing P14→P9 edge) are **open and unanswered** as of this row. Nothing below has been revised for them. |
| 4 | 2026-08-02 | **Completability review.** Amendment 3 made the plan consistent; this one makes it finishable. One further conflict found: **P9 adds slots to Part 2 after P8 has authored the JSON-LD context**, so P8's output goes stale the moment P9 lands — a rework loop the single item P8 concealed. Split into **P8a / P8b** and the second pass justified rather than planned away (**PA15**). Four gaps closed: **every item now has a falsifiable definition of done** and an ordinal size (**PA16**) — an item that cannot be declared finished is the plan-stage form of an unfalsifiable claim; **wave 1 is ordered by external latency rather than by size** (**PA17**), which changes which item is picked up first; and the plan gains **abort conditions and a unit-level definition of done** (**PA18**). |

**Convention.** Per [`docs/README.md`](../README.md), corrections stay
recorded rather than being edited away, and current state goes first.
Where an assertion was superseded, the original claim is kept under it
so the record of being wrong survives.

---

### Tooling declaration (first application of the declare-don't-discover rule)

**PA1 — the tooling changed twice, I verified it by running it rather
than by reading the summary, and the declaration rule is now in
effect.** Current state, verified 2026-08-02:

| Change | Verified how | Result |
|---|---|---|
| **20** rule/fixture pairs, 5/5 rules with demonstrated recall | `make lint-selftest` | **confirmed**, exit 0 |
| `GENERIC_ACRONYMS` carries F11's eight with inline reasons | read the set | **confirmed** — `CF NVS DQV ADMS DCAT DCT OMS UCUM` |
| **the acronym upper bound is gone**, not raised | read `ACRONYM` | **confirmed** — a third guessed number would have been a third counterexample |
| namespace inspection (`prefixes:`, `slot_uri`, `class_uri`, `meaning`) | `drift-lint.py` on constructed files | **confirmed** |
| single-authority hosts by host; shared redirects by host **plus path** | c1/c2 + a positive control | **confirmed** — see PA2 |
| four new fixtures (`jurisdiction-in-uri`, `bound-vocabularies`, `redirect-service`, `long-acronym`) | listing + selftest | **confirmed** |
| `CLAUDE.md` carries "Tooling changes are declared, not discovered" | `grep -c` | **confirmed** — 1 in `CLAUDE.md`, 0 in the fixtures README |
| `scripts/lint-fixtures/README.md` is the fixtures convention document | read it | **confirmed** — 48 lines, opens "Small LinkML schemas with known-correct outcomes" |
| orphan detection | read `lint-selftest.py:68–81` | **inspection only** — not tested, because testing it means writing a stray file into human-owned `scripts/` |

**Superseded — what PA1 claimed on 2026-08-01, and why it is kept.**
PA1 originally reported that the governance change had not landed where
it governs: the new `CLAUDE.md` text had been written to
`scripts/lint-fixtures/README.md` (179 lines) while `CLAUDE.md` (168
lines) remained the previous version, the two diverging from char 4010.
It concluded that **the declaration rule was not in effect** and that
**the fixtures convention document did not exist** — the file at that
path being a copy of `CLAUDE.md` containing the tell *"See
`scripts/lint-fixtures/README.md`"*, a pointer to itself.

That was accurate when filed and is false now. It was a transfer error —
both files delivered in one batch, the governance content saved to the
README path — and it is corrected. **Both statements are now wrong and
neither should be read as current.**

Worth keeping for one reason: the first thing the declare-don't-discover
rule asked H to verify was the rule itself, and it was not where it said
it was. That is the rule working on its first application.

Both files are human-owned. Reported, not fixed.

**PA2 — C18 stays `falsified`. The guard has been broken four times,
twice by O and twice by H, and a fourth counterexample is open now.**

*Closed.* F13 — a jurisdiction-specific scheme passing all five rules
via three independent mechanisms — is fixed, and the falsifier is met
including the hard half:

| Case | When filed | Now |
|---|---|---|
| c1 — IRWIN on `w3id.org/nwcg/irwin/` | exit 0, all five ok | **fires** — "public permanent-identifier redirect — anyone may register there, so the path must be allowlisted, not the host" |
| c2 — CalFire on `purl.org/calfire/incident/` via `meaning` | exit 0, all five ok | **fires** |
| c3 — `NWCGIRWINIDENTIFIER`, 19 chars | exit 0, all five ok | **fires** — bound removed rather than raised |
| c4 — *control*, agency-owned host | fires | fires |

**The hard half is what mattered**, and it holds: a file declaring
`linkml: https://w3id.org/linkml/`, `dct: http://purl.org/dc/terms/` and
`sosa: http://www.w3.org/ns/sosa/` together **passes clean, exit 0**.
Host-plus-path for shared redirects keeps the legitimate namespaces
while closing the registrable ones.

The design point PA2 made stands and is now implemented: **host is the
wrong granularity for redirect services.** `w3id.org` and `purl.org` are
public permanent-identifier redirects, anyone may register under either,
and `w3id.org` cannot be removed because LinkML's own namespace lives on
it. The fix was never another allowlist entry.

*Open — F14, a fourth counterexample.* Three closed counterexamples do
not establish that no fourth exists, so H looked. It took one attempt:

```yaml
prefixes:
  lcsh: https://id.loc.gov/authorities/subjects/
slots:
  subjectHeading:
    slot_uri: lcsh:sh85147610
```

**exit 0, all five rules ok.** `id.loc.gov` is matched **by host** as a
single-authority vocabulary host — but it is the **US Library of
Congress**, and LCSH and LCNAF are national schemes that happen to be
reused internationally. By invariant 2's own wording ("national
identifier schemes ... live in `vocab/profiles/`") that is jurisdiction
content passing clean.

Same *class* as F13, one step over: F13 was a shared host treated as
single-authority; **F14 is a national authority treated as generic.**
Whether `id.loc.gov` belongs on the allowlist is a judgement rather than
a bug — presumably added for the international-reuse reason — but the
judgement should be explicit and carry its reason the way the F11
entries do.

*Open — PA2c, the declared hole, now primary by elimination.*
`irwinIncidentIdentifier` — camelCase, no URI, jurisdiction carried
entirely in the `description` — passes clean. That is the docstring's
stated limitation, not a new finding. It matters because closing the URI
routes makes it **the primary remaining one**, and the docstring's own
answer stands: the real test is whether an identifier is declared by
some profile, which cannot run until profiles exist. That test arrives
with **P6a**, not before.

**Falsifier, unchanged:** *a jurisdiction-specific scheme that passes
all five rules.* Neither F14 nor PA2c is a block. `scripts/` is
human-owned; reporting.

Counterexample files are in the session scratchpad, not in `scripts/`.

**PA10 — CIM does not dereference as a class. Standing constraint, not
an open question.** A30 established that
`http://entsoe.eu/ns/CIM/ObjectRegistry-EU/2.1` returns a generic 404
page. Per the project owner this is general to CIM rather than
particular to the ENTSO-E profile — IEC publishes no dereferenceable RDF
for the base model either, consistent with
`http://iec.ch/TC57/CIM100` → 403.

The CIM structure is therefore held locally with its provenance cited to
the profile PDF, **permanently**, and no future session should re-probe
expecting a different answer. This does not change ADR-001, which
already selected the copy-and-cite row of its own bind-or-copy table. It
changes that selection from *contingent on a probe* to *settled*.

**Falsifier:** any IEC or ENTSO-E CIM namespace serving RDFS or OWL
under content negotiation. Cheap to re-test, expected to stay negative.

---
### Ordering constraints, stated rather than assumed around

**PA3 — three declared constraints hold, and a fourth is load-bearing
and was not named.**

- **ADR-001 question 2 is gated on L2, and L2 is unfalsifiable as
  stated.** Confirmed. Naming the relation is upstream of all identity
  work. **But the naming splits into two items, not one**, and only one
  of them is blocked: *which relation the claim is about* is answerable
  here and now; *which relation the reference pipeline implements* needs
  source access this repository does not have (A11, A39). The first is
  P1 and unblocks ADR-001. The second is P12 and may never be
  answerable. **Conflating them is what made L2 unfalsifiable in the
  first place**, so the plan separates them permanently.
- **ADR-003 is open and determines Part 2's shape.** Confirmed, and the
  measured delta is +0 classes / +2 slots translated (A7). That number
  is why ADR-003 does **not** gate Part 0 and does gate Part 2 — the
  cost of deciding late is two slots and one enum, not a rebuild.
- **T3 falsified, T3a has no tiebreak, so L4's precondition is
  unestablished.** Confirmed. Everything depending on merge-as-join is
  downstream of P11.
- **Fourth, unnamed: C17 has two open axes and both make "validated"
  mean less than it says.** Expansion drops unmapped keys; `gen-shacl`
  never consults the term it binds. Until at least the second is closed,
  P8a produces a green `make check` that is not evidence. This is not a
  blocker on authoring — it is a blocker on *believing the result*.
  **This bullet is where the blocks-start / blocks-trust distinction in
  the item table came from**; the first draft named the distinction here
  and then failed to apply it to P10 twenty lines later. See PA6.

**Falsifier for PA3:** an item in the sequence below whose stated
dependency does not actually block it — demonstrated by starting it.

---

### The plan

Twelve items. **Edges are typed**, because conflating two kinds of
dependency was the largest defect in the first draft of this section:

- **blocks-start** — the item cannot begin until its predecessor
  finishes. A hard sequence edge.
- **blocks-trust** — the item can begin and finish, but its *output is
  not evidence* until the predecessor lands. Not a sequence edge; a
  claim about what the result means.

| # | Item | Produces | Blocks-start | Blocks-trust | Notes |
|---|---|---|---|---|---|
| **P1** | Name L2's relation | `Identity.lean` defines both candidate relations; H proposes the restatement | — | — | Completion needs an **O session** — only O changes a claim's status. External dependency, not a work item |
| **P2** | Decide ADR-001 question 2 | design gate; A/B/C chosen or explicitly deferred | P1 | — | Blocks **P6b only**, not P6a — see PA11 |
| **P3** | Decide ADR-003 | design gate; Part 2's shape | — | — | Blocks P7 |
| **P4** | Rebuild `parts.als` under F10 | constraints by extension; T2 gets evidence or is recorded as unevidenced | — | — | Blocks **nothing in this unit**; blocks the first profile, which is a later unit — see PA8 |
| **P5** | `vocab/prefixes.yaml`, 23 binding **identities**, 10 local terms declared, external graphs cached | the binding surface — **identity, not form** (PA19) | — | — | Blocks P6a, P7, P10 |
| **P6a** | Part 0 entity + alias core — the ADR-001 question-1 shape | `vocab/core/part0-*.yaml` | P5 | P10 | Settled by ADR-001 Q1. Does **not** wait on P2 |
| **P6b** | `candidateMatch` relation, if the resolution strategy needs one | a Part 0 relation, or nothing | P2 | P10 | May be empty under option B — see PA11 |
| **P7** | Part 2 — the observation shape, **excluding absence** | `vocab/core/part2-observation.yaml` | P3, P6a | P10 | Slot count depends on P9's boundary — see PA12 |
| **P8a** | Fixture capture, JSON-LD context, `make check` executing against P7's shape | `fixtures/`, a `check` that runs | P7 | **C17 axis 1** | "Green" ≠ "validating" — see PA13 |
| **P9** | The absence and health model | `absenceReason`, `observingSystemStatus`, the sentinel decoding | P7, P8a | — | Closes ranked gap #3. Last **modelling** item |
| **P8b** | Context extended for P9's slots, check re-run | an up-to-date `check` | P9 | **C17 axis 1** | Not rework — the price of PA7's ordering. See PA15 |
| **P10** | Range-vs-`slot_uri` drift check | C17 axis 2 closed | P5 | — | **Blocks-trust on P6a, P6b, P7** — see PA6 |
| **P11** | Name T3a's tiebreak | L4's precondition | — | — | Outside this unit. Listed because merge work is the next unit and it has no predecessor — startable any time |
| **P12** | Determine the implemented matching rule | closes L2's second half | **source access this repo lacks** | — | Permanently open — see PA9 |
| **P13** | Fixture capture rules | `fixtures/README.md` — ordering key, F9 trap, per-fixture tier | — | — | Blocks P14. H's file. See PA22 |
| **P14** | Capture the T1 snapshot series | ≥24 consecutive hourly AirNow snapshots | P13 | — | **~24h irreducible floor.** Blocks P9's falsifier. See PA22 |
| **P15** | The §5.1 q9 experiment — PM2.5 threshold vs composite AQI | evidence on **C5, C17 and the motivating defect at once** | — | — | ~30 min. No `vocab/` needed, neither ADR blocks it. **Prediction attached.** See PA24 |

**PA4 — the order is three waves plus two items with no wave.** The
first draft wrote this as `P1 · P5 · P4 ‖ P3 · P2 · P10 · P6 · P7 · P8 ·
P9`, which was pseudo-notation that did not say what `·` and `‖` bind
and contradicted its own prose. Waves instead:

| Wave | Items | Why together |
|---|---|---|
| **1** | **P13 → P14**, then **P1, P3, P4, P5, P11** | P13/P14 first — see PA17. The rest have no predecessors and run alongside P14's 24-hour wait |
| **2** | **P2, P10** | P2 needs P1; P10 needs P5. Independent of each other |
| **3** | **P6a → P7 → P8a → P9 → P8b**, with **P6b branching off P6a in parallel** | The authoring chain. **P6b is a branch, not a link** — see PA20. P9 is the last modelling item; P8b is a mechanical re-run behind it (PA15) |
| **—** | **P12** | Never startable here |

P6b may be empty (PA11), in which case the branch disappears.
**Wave 1 has an internal order** — by external latency, and the ranking
changed in amendment 5. See PA17.

**PA20 — the item table is the plan; PA4's wave rendering was wrong,
and it was cancelling PA11's headline benefit.** The table has P7
blocks-start on `P3, P6a` — P6b is nowhere in P7's dependencies. The
wave row rendered the chain as `P6a → P6b → P7`, which puts P6b *on the
path to P7*. Since P6b blocks-start on P2, and P2 on P1, and P1 needs an
O session (PA16), that rendering silently put a design-gate decision and
an O turnaround back in front of P7 — **giving back exactly the
shortening PA11 claims as the largest single ordering change in
amendment 3.**

Two renderings of one graph, one wrong. Same defect class amendment 3
recorded fixing for the P10 edge, which is not a coincidence: both times
the table was right and the prose summary drifted. **The table
governs.** Where a summary and the table disagree, the summary is the
bug.

**Falsifier:** a reason P7 needs `candidateMatch` to exist. If one is
found, the table is wrong instead and P6b becomes a real link.

**PA19 — P5 is resolve-and-cache, not author-in-final-form, and that
is why T4's falsification costs one paragraph rather than the order.**
O found the plan using both readings: PA5 and PA18 treated P5 as
authoring the bindings in their final form; PA16's done-criterion
treated it as resolving and caching them. The criterion is the one that
governs, and it settles the question on its own text — **none of its
four clauses mentions cardinality or range**:

> *`prefixes.yaml` resolves every prefix used; all 23 external terms are
> content-verified by fetch-and-grep; the 10 local terms are declared;
> external graphs are cached locally.*

A prefix map carries no cardinality. A cached graph carries the
external term's own axioms, not ours. Content-verification by
fetch-and-grep establishes that a term **exists** — which is T4a — not
what form we give the slot that binds it.

**Where form is actually authored:** Part 2 slots at **P7**, which
already blocks-start on **P3**. `sosa:madeBySensor` — O's
counterexample — is a Part 2 slot. So the dependency T4's falsification
reveals is **already carried by an existing edge**, and nothing in PA4
moves.

What does change:

- **T4 stays falsified.** O's experiment is correct and the contest it
  anticipated is the one I would have made, so I am not making it.
  Under option B `madeBySensor` cannot be required, because Open-Meteo
  publishes no instrument (S10, and A5's falsifier came back empty);
  under option A it can be. That is a form difference forced by the ADR.
- **T4a is what P5 needs and what P5 has.** Identity decidable, form
  not.
- **PA5's justification is withdrawn and replaced**; its conclusion
  stands.
- **PA18's T4 clause is withdrawn** and replaced with one that names the
  case that would actually require re-derivation: a **Part 0** slot
  whose form is ADR-dependent, since P6a does not wait on P3.

**The residual risk, stated rather than assumed away.** P6a
blocks-start on P5 alone. If any Part 0 slot's cardinality turns out to
be ADR-dependent, it is authored against an unresolved decision. A7
measured ADR-003's delta as one slot and one enum, both in Part 2, so
this is not expected — but *not expected* is not *checked*, and the
check is cheap: it is the first clause of P6a's done-criterion below.

**Falsifier for PA19:** a clause of P5's done-criterion that cannot be
satisfied without choosing a cardinality or a range.

**PA5 — P5 is the long pole and is startable today.** It has no
predecessor, it is the widest item, and everything in wave 3 waits on
it. The 23 bindings are content-verified (A3 as amended, S4) and the 10
local terms are enumerated (A1 as restated).

**Justification corrected — this rested on T4, which is falsified.** It
now rests on **T4a**: the *identity* of the 23 bindings is decidable
before either ADR; their *cardinality and range* are not. P5 resolves
identity and caches graphs (PA19); it authors no cardinality. So PA5's
conclusion survives on the narrower claim, and the part T4 was carrying
— that the bindings' *form* is settled — was never P5's to carry. See
PA19 for why this is a one-paragraph correction rather than a
re-derivation.

**Falsifier:** a binding in P5 whose form changes under either ADR
outcome. `epistemicKind` under ADR-003 option B is the candidate — it is
a *new* slot, not a change to an existing binding, which is why it does
not falsify this.

**PA6 — P10 blocks trust in P6a, P6b and P7, and does not block their
start. The first draft got this edge wrong in both directions.**

The substance is unchanged and correct: `gen-shacl` silently emits
shapes contradicting the bound term (A34, reproduced at S3), so slots
authored before P10 exists carry no check that their range agrees with
the term they bind, and the error is invisible exactly where a binding
is wrong.

What was wrong was the edge. The first draft put P10 *in the sequence*
before P6 while the table recorded it as a **soft** block on P8 — two
statements that cannot both be true. Neither was right:

- **P10 does not block P6a from starting.** Nothing breaks if you author
  Part 0 first. Presenting it as a sequence step overstated it.
- **P10 does not block P8 either.** By the time P8 runs, the drift is
  already authored in. Recording it against P8 pointed at the wrong
  item.

The honest statement is the third one: **P10 determines whether P6a,
P6b and P7 produced what they claim to have produced.** Doing it first
is strongly preferable — catching 33 slots at authoring time beats
auditing them retroactively, and P5 must cache the external graphs
anyway, so the cache is one artifact serving two items — but that is an
efficiency argument, not a dependency, and it should not have been
dressed as one.

**Falsifier:** implement P10 after P6a and P7 and find it catches
nothing that inspection would have caught.

**PA11 — P6 splits, and the P2 dependency is narrower than the first
draft claimed.** ADR-001 separates *what shape identity takes*
(question 1, **settled** — the four-class decomposition translated to an
`alias` relation) from *what establishes identity* (question 2, open,
gated on L2). The first draft made all of P6 wait on P2. That is wrong:

- **P6a — the entity and alias core — is settled by question 1** and
  waits on nothing but P5. Options A, B and C do not change the alias
  structure.
- **P6b — a `candidateMatch` relation — is the only part question 2
  touches.** Under option B, heuristic matches are recorded as
  `candidateMatch` facts rather than identity facts, which is a Part 0
  relation. Under A (transitive closure) there is nothing to record.
  Under C it is a relation plus a policy.

So P2 blocks a possibly-empty item, not the entity core. **This shortens
the critical path by one design-gate turnaround**, which is the largest
single ordering change in this revision.

**Ambiguity, stated rather than resolved:** whether `candidateMatch`
belongs in Part 0 at all, or in `transform/` as a derived relation, is a
design question. If it is transform content, P6b leaves the schema plan
entirely and P2 blocks nothing in this unit. **Do not resolve this
here** — it is the design gate's.

**Falsifier for PA11:** an ADR-001 option under which the alias
structure itself changes shape.

**PA12 — P7 and P9 were double-counting the same slots.** The first
draft gave P7 as "6 classes, 20 slots" and P9 as "the absence and health
model" — but `absenceReason` and `observingSystemStatus` are inside
P7's 20. Either P7 authors them, making P9 redundant, or P7 stops short,
making its count wrong.

Resolved by boundary rather than by count: **P7 authors the observation
shape excluding absence; P9 authors absence.** P7's slot count is
therefore *not* fixed at 20 in this plan, and pinning it is measure's
job, not plan's. The measure document's A1 count stands as a count of
the unit's total surface, which is what it was.

**PA7 — P9 is last on purpose, and it is the only item I expect to
change shape.** It carries the unresolved design content. F5 and F6
added two sentinel channels after A16 filed one, and both came from
looking at more rows. Modelling before P8a means modelling against three
absence semantics found in one snapshot; modelling after means modelling
against whatever 24 snapshots contain.

**Falsifier:** capture the 24 T1 snapshots and find no absence encoding
beyond `Status` / `_Measured` / `null` / `-999` / `'ND'` /
`Elevation == 0`.

**PA13 — "P8 produces a working `make check`" needs a definition of
done, and the honest one is weaker than it sounds.** *(Refined by PA15,
which splits P8 into P8a and P8b, and by PA16, which gives each its own
criterion. The argument below is unchanged and applies to both.)* A14 established
that `make check` cannot validate a captured payload today: it globs
`.jsonld`, every capture is EsriJSON or Open-Meteo JSON, and nothing
converts one to the other. P8 closes that — but the conversion is a
hand-authored `@context`, and per C17 axis 1 expansion silently drops
every key the context omits.

So P8's definition of done is **`make check` executes against real
captures and reports violations it can see** — not "validation is
sound". C17 axis 1 is explicitly out of this unit (below), which means
**P8 ships a green check that is not yet evidence.** That is acceptable
only because it is written down here.

**Falsifier:** a definition of done for P8 that does not depend on the
hand-authored context.

**PA8 — P4 is in wave 1 and blocks nothing in this unit, and "early" now
has a reason attached.** The first draft said P4 "should be done early"
without saying early relative to what, which made it a preference
wearing a constraint's clothes. The constraint is real but it is
downstream of this unit: **P4 blocks the first profile.** T2 has no
evidence on inspection (F10), profile composition is what
`vocab/profiles/` exists for, and T3's falsification came from a
counterexample nobody needed a solver to find. Authoring a profile
before P4 builds on an unevidenced soundness claim.

Since P4 has no predecessor, wave 1 costs nothing and removes a future
blocker.

**PA9 — P12 is a permanently open item, not a task.** It cannot be
started from this repository. Naming it keeps L2's two halves separated
so nobody re-conflates them when P1 lands and L2 looks settled.

**PA14 — tooling items are plan items, and the first draft applied that
rule inconsistently.** It listed P10 (a drift check, which lives in
`scripts/` or the `Makefile`) as a plan item while dropping the
jurisdiction-rule extension as "not a plan item — `scripts/` is
human-owned". Both are human-owned tooling; the two cannot be treated
differently on that ground.

The rule this plan uses: **human-owned tooling appears as a plan item
when this unit's output depends on it, and as a finding when it does
not.** P10 qualifies — every slot in wave 3 is unverified without it.
The jurisdiction-rule extension does not: F14 and PA2c are precision and
recall holes in a guard, and a guard that misses something does not
corrupt what P6a authors. It stays a finding.

H does not implement either. Naming an item does not assign it.

---

**PA15 — P8 runs twice, and the first draft hid that as a single item.**
P7 authors the observation shape *excluding* absence (PA12). P9 adds
`absenceReason`, `observingSystemStatus` and the sentinel decoding
afterwards. But P8 authors the JSON-LD context in between — and per C17
axis 1, **the context determines what validation can see.** So P9's
slots are invisible to the check P8 just got running, until the context
is updated and `make check` re-run.

The plan's edges said P7 → P8 → P9 and stopped, which reads as one pass.
It is two:

- **P8a** — capture, context and `make check` executing against P7's
  shape. Its purpose is to put real fixtures in front of P9.
- **P8b** — context extended for P9's slots, check re-run.

This is not rework and should not be planned away. PA7's reason for
putting P9 last is that it should model against whatever 24 snapshots
contain rather than against three absence semantics from one — which
requires the captures to exist first. **The second pass is the price of
that ordering, and it is worth paying.** What was wrong was leaving it
implicit, because an unnamed second pass is indistinguishable from
having forgotten it.

**Falsifier:** a context authored at P8a that already maps P9's slots
without knowing what P9 decides they are.

**PA16 — every item now has a definition of done, because an item that
cannot be declared finished is the plan-stage form of an unfalsifiable
claim.** The first draft gave completion criteria for P8 only (PA13) and
"Produces" cells for the rest, which name an artifact rather than a
condition.

| # | Done when | Size |
|---|---|---|
| **P1** | Both candidate relations are defined in `Identity.lean` and L2's entry names which one it is about. **Needs an O session** — H cannot close it | S |
| **P2** | ADR-001 question 2 records A, B or C, or records a deferral with its reason | S |
| **P3** | ADR-003 records A or B, and `docs/coverage.md` plus ADR-002's modality table agree with it | S |
| **P4** | `parts.als` models constraints by extension; **the M1 mutation changes the output**; the header's C1/C2 claims are true or removed | M |
| **P5** | `prefixes.yaml` resolves every prefix used; all 23 external terms are content-verified by fetch-and-grep; the 10 local terms are declared; external graphs are cached locally | **L** |
| **P6a** | **No Part 0 slot's cardinality or range differs by ADR-003 or ADR-001 outcome** (the PA19 residual — check first, it is cheap); the entity and alias core validates under `make lint`; `flat-siblings.yaml`'s shape passes as it does today; `operatingMode`, `modelVersion` and `profileConformance` are declared (PG5) | M |
| **P6b** | Either a `candidateMatch` relation exists, or a line records that the chosen option needs none | S–0 |
| **P7** | `make gen` produces `build/shapes.ttl` from Part 2 + P6a with no LinkML error | M |
| **P8a** | **Under ADR-003 option B:** `make check` executes against ≥1 real AirNow **and** ≥1 real Open-Meteo capture and reports violations it can see. **Under option A:** AirNow only — Open-Meteo has no Part 2 shape to validate against (A5), and the Open-Meteo captures are retained as Part 3 fixtures for a later unit. See PA21 | M |
| **P8b** | The context maps P9's slots; `make check` re-run and green | S |
| **P9** | All three absence semantics and all three sentinel channels round-trip distinguishably (A16, F5, F6) | **L** |
| **P10** | A check compares each `slot_uri`'s external range against the local `range` and fails on disagreement; the `sosa:observedProperty` case from A34 fires | M |
| **P11** | T3a's entry names a tiebreak, or records that none exists | S |
| **P12** | — permanently open | — |

Sizes are **ordinal, not estimates.** The measure gate's 5–7 sessions
was measured against a surface that has moved four times; absolute
numbers would be false precision. Relative size survives that and is
what the ordering actually needs. **P5 and P9 are the two large items**,
and they sit at opposite ends of the chain.

**Falsifier:** an item declared done under its criterion that a later
item then has to reopen. P8a is the deliberate exception (PA15).

**PA17 — wave 1 should be started in order of *external* latency, not
in order of size, and this changes what is done first.** PA5 says P5 is
the long pole, and it is — in H's own work. But **P1 and P3 both block
on someone else**: P1 cannot close without an O session changing L2's
status, and P3 is a design-gate decision. P4 is H's but produces a
claims change that O must record.

Ranking wave 1 by size puts P5 first and leaves P1's O-turnaround
un-started, so the wall clock pays for it serially at the end. Ranking
by latency starts the externally-blocked items first and does P5's work
*while* they are pending:

| Order | Item | Why here |
|---|---|---|
| 1 | **P13** | Tiny, and **P14 cannot start until it exists** (PA22). Minutes |
| 2 | **P14** | **The only irreducible latency in the plan** — ~24h, hourly feed, uncompressible. Everything below runs alongside it |
| 3 | **P15** | 30 minutes, and it is the highest-value experiment available anywhere in the project (PA24). Fits inside P14's wait |
| 4 | **P1** | Longest *chaseable* latency — needs an O session, and P2 waits behind it |
| 5 | **P3** | Design-gate decision; blocks P7 at the far end of the chain |
| 6 | **P5** | The large item, and the one that fills the wait |
| 7 | **P4** | H's own work, blocks nothing in this unit |
| 8 | **P11** | Smallest, no predecessor, no successor here |

**Amendment 5 corrected the ranking's premise, not just its contents.**
PA17 originally justified itself with *"every other latency in the plan
is a turnaround that can be chased"* — true of every item it ranked, and
false of the one it had left out. A ranking by external latency that
omits the only uncompressible latency ranks the wrong things carefully.

This does not change the dependency graph. It changes which startable
item is picked up first, which is the only thing a wave with five
members leaves undetermined — and the first draft left it undetermined
while implying by PA5 that the answer was P5.

**Falsifier:** an O turnaround shorter than the work in P5, which would
make the two orderings equivalent.

**PA18 — abort conditions, and a definition of done for the unit.**
The plan has falsifiers per assertion but no statement of what result
sends it back to measure rather than forward.

**Back to measure if:**

- ~~**T4 is falsified** — a binding changes form under an ADR outcome.
  P5 leaves the front of the order, PA4 and PA5 both fall, and the
  ordering has to be re-derived rather than patched.~~
  **Withdrawn 2026-08-02. T4 was falsified and this condition did not
  fire, because it was written against the wrong item.** Binding *form*
  is authored at P7, which already blocks-start on P3. The dependency
  T4's falsification reveals was already in the graph. Replaced by:
- **A binding's form proves to be authored before the ADR that
  determines it.** Concretely: a **Part 0** slot whose cardinality or
  range differs by ADR-003 or ADR-001 outcome. P6a blocks-start on P5
  only, not on P3, so such a slot would be authored against an
  unresolved decision — and *that* would require re-deriving the order
  rather than patching it. A **Part 2** slot does not qualify: P7
  already waits on P3. See PA19.
- **P1 finds L2 false under *both* candidate relations.** The plan
  assumes one of the two readings survives. If neither does, ADR-001's
  question 2 is not gated on L2 at all and the identity items need
  re-measuring.
- **P9 finds a fourth absence semantics that the first three cannot
  express.** Gap #3 was measured as three states; a fourth changes the
  Part 0 fragment, not just Part 2, and that is upstream of P6a.

**Not an abort — proceed and record:** F14 and PA2c (guard holes),
C17 axis 1 (validation is not sound), T2 unevidenced. Each is a known
weakness with a named consequence, which is the condition for carrying
something rather than stopping for it.

**Plan 01 is done when:** P6a, P7, P8a, P8b, P9, P10, P13 and P14 all
meet their criteria above, and the unit's original scope statement is
true — *Part 2 plus the Part 0 fragment it depends on, bound to external
vocabularies, generating SHACL, validated against captured AirNow and
Open-Meteo payloads* — with **two qualifications attached**:

1. **PA13** — "validated" means the check executes and reports what the
   context lets it see, not that validation is sound.
2. **PA21** — "and Open-Meteo" holds **under ADR-003 option B only**.
   Under option A the clause reads *AirNow*, and the Open-Meteo captures
   are retained as Part 3 fixtures for a later unit.

P2, P6b, P4, P11 and P12 are not in that list. P2 and P6b may resolve to
nothing; P4 and P11 serve later units; P12 cannot close here.

---

**PA21 — P8a's and the unit's definitions of done presupposed ADR-003
option B, and now carry the conditional.** Both said "validated against
captured AirNow **and** Open-Meteo payloads". A5 established, and O
confirmed by experiment, that under option A the Open-Meteo half has no
Part 2 shape to validate against. P3 resolves in wave 1, long before
P8a — but as written, **if P3 chose A, P8a could never be declared done,
and neither could the unit.**

This is A5 carried forward as an assumption instead of as a conditional,
which is the specific thing O ruled A5 should be kept to prevent. The
substitute under A is stated rather than left to be improvised: **Part 2
validates against AirNow only, and the Open-Meteo captures are retained
as Part 3 fixtures for a later unit.** Nothing is discarded; the
boundary moves.

**Falsifier:** an ADR-003 option A reading under which an Open-Meteo
air-quality response validates against a Part 2 shape.

**PA22 — the 24-snapshot capture is a plan item, it belongs in wave 1,
and the capture rule has to be written before it starts.** Two absences,
and they compound.

PA7's whole justification for putting P9 last is *"modelling after means
modelling against whatever 24 snapshots contain"*, and A13 sets the same
floor. **No item produced them.** P8a's criterion said "≥1 real AirNow"
— one. The 24 were load-bearing in the reasoning and absent from the
work.

The ordering consequence is the sharper half, and PA17 got it wrong by
omission. PA17 ranks wave 1 by external latency because *"every other
latency in the plan is a turnaround that can be chased."* **The snapshot
capture is the exception: the feed is hourly, so 24 consecutive
snapshots have an irreducible ~24-hour floor that cannot be
compressed.** It is the only wall-clock in the plan that no amount of
attention shortens. Started in wave 1 it costs nothing, because
everything else in wave 1 and 2 runs alongside it. Started at P8a it is
a day P9 spends waiting.

And it cannot start until the capture rule exists. BR-6 accepted F9's
consequence — `LocalTimeString` carries a standard-time offset in
August, so the T1 replay's ordering key has two published forms that
disagree by an hour, seasonally — and deferred writing it to this gate.
It was not written. **Collecting 24 snapshots under an unstated ordering
convention is the cheapest way to have to collect them twice.**

Two new items, both wave 1:

| # | Item | Done when | Size |
|---|---|---|---|
| **P13** | Fixture capture rules in `fixtures/README.md` | The ordering key is named (`ValidTime` UTC, not `LocalTimeString`), the F9 seasonal-offset trap is recorded, and the verification tier and capture timestamp are required per fixture | S |
| **P14** | Capture the T1 snapshot series | ≥24 consecutive hourly AirNow snapshots exist under P13's rules, with gaps recorded rather than silently skipped | S work, **~24h floor** |

`fixtures/README.md` is H's under the ownership table, so P13 is H's to
write.

**Falsifier for PA22:** a way to obtain 24 consecutive hourly snapshots
in less than 24 hours. An archive endpoint would do it — none is known,
and the register does not list one.

**PA23 — C12 and C15 are scheduled, not deferred.** Both are
`falsified`; A18 recorded both as one slot each and free. They appeared
in neither the plan nor its exclusions list, which is the one option O
correctly says a plan cannot take.

**Scheduling both, into P6a**, for asymmetric reasons:

- **C12 — operating mode.** Ranked gap **#1**. Its own entry reads
  "safety-critical and free to fix", and CAP already supplies the
  vocabulary (`Actual | Exercise | System | Test | Draft`). A
  discriminator that stops exercise data being rendered as live is not
  something to carry as a known absence while authoring the first real
  content. One slot on `Statement`.
- **C15 — instance-level version and profile declaration.** Free now and
  blocking at the first breaking change (A18, gap #9). The argument for
  doing it late is that nothing needs it yet; the argument for doing it
  now is that it costs one slot now and a migration later.

**This moves a measure-stage number**, and the honest thing is to say so
rather than quietly re-count: A1's surface was 33 slots. These add three
— `operatingMode`, `modelVersion`, `profileConformance`. **A1 is the
measure document's and I am not editing it**; recording the delta here,
where the scheduling decision is made.

**Falsifier:** either slot turning out to need more than a declaration
and an enum — for example, if operating mode has to propagate through
derivation rather than sit on a statement.

---

**PA24 — the §5.1 question 9 experiment is scheduled, with its
prediction attached. It is the highest-value item currently available
anywhere in this project, and it has been sitting unrecorded.**

The experiment: express a **PM2.5-specific statutory threshold** and a
**composite `us_aqi` reading** in one schema, run `gen-shacl`, and
validate with pyshacl. Thirty minutes. It needs no `vocab/` content and
neither open ADR blocks it.

It measures three things at once:

- **C5** — the only *external* claim in the register, unanswered since
  it was written. Its strongest candidate answer is exactly this:
  whether the canonical layer turns a silent property-substitution
  error into a validation failure.
- **C17** — whether validation can see a mismatch at all.
- **The motivating defect itself** — the register records a
  PM2.5-specific threshold evaluated against a composite index for four
  builds, which produced an impossible ordering.

**Prediction, stated in advance and kept attached: from C17, it
conforms** — that is, validation does *not* catch the substitution.
Recording the prediction is what makes the result informative in both
directions. If it conforms, C5's strongest candidate fails on the
current tooling and C17's consequence is demonstrated on the case that
motivated the project. If it does not conform, C5 has its first
affirmative answer and C17 is narrower than filed.

**The finding is about the project, not the claim.** C5 has been
`asserted` and unanswered throughout, and its best available test was
written down in `FALSIFIER.md` §5.1 the whole time without ever being
scheduled. A question list that O reads and the plan does not is a
second place for work to go missing — which is the same shape as PG3,
PG4 and PG5, and the third instance this week.

**Falsifier for PA24:** an experiment that measures C5 more directly, or
evidence that a threshold and a reading cannot be expressed in one
schema without `vocab/` content.

### O's cheapest-experiment list

| Experiment | Disposition |
|---|---|
| `is_a` chain depth, transitive | **done** — F2 cleared, verified |
| Split `lint-selftest` per rule | **done** — F1 cleared; **20** pairs as of 2026-08-02 |
| `AQSID` in `vocab/core/` (A17) | **done** — was F4, ran negative, now fixed |
| T3 via `order : seq Constraint` in Alloy | **dropped.** T3 was falsified by counterexample without a solver. The experiment would confirm something already known, and the 0.5-session estimate was wrong by the whole amount |
| Add the eight vocabularies to `GENERIC_ACRONYMS` | **done** — verified in PA1 |
| Extend jurisdiction rule to namespaces | **done for the redirect case, open for two others.** Host-plus-path landed and closes F13. **F14** (`id.loc.gov`, a national authority allowlisted as generic) and **PA2c** (jurisdiction in prose only) remain. A **finding, not a plan item**, per PA14 |
| Rebuild the Alloy model (F10) | **survives as P4**, wave 1 |

---

### What this plan does not do

- **It does not decide ADR-001 or ADR-003.** P2 and P3 are placeholders
  for design-gate decisions with their dependencies named.
- **It does not resolve whether `candidateMatch` is schema or
  transform.** PA11 names it as an open design question, and the answer
  changes whether P6b exists.
- **It does not schedule profile authoring.** T2 is unevidenced (F10)
  and T3 is falsified; authoring two composing profiles before P4 and
  P11 would build on both.
- **It does not close C17 axis 1**, and PA13 records what that costs:
  P8a and P8b ship a green `make check` that is not yet evidence. Whether
  JSON-LD expansion is the validation path at all is design work.
- **It no longer omits C12 and C15.** PA23 schedules both into P6a.
  They were previously neither scheduled nor excluded, which is the one
  state a plan may not leave a known-falsified claim in.
- **It gives no session estimates.** A22's 5–7 was measured against a
  surface that has since moved three times and an order this revision
  has changed again. Re-estimating here would be re-doing measure with
  less information than measure had.

---

### Claim proposed

**T4 — the binding surface is decidable before either open ADR.**
Neither ADR-001's resolution nor ADR-003's changes the form of any of
the 23 external bindings; both add or relocate local slots only.

- **Falsifier:** an external binding whose `slot_uri`, range or
  cardinality differs between ADR-003 option A and option B, or between
  ADR-001 options A, B and C.
- **Cheapest test:** author P5 and re-derive it under the opposite
  choice for each ADR. If nothing moves, T4 survives; if anything moves,
  P5 leaves the front of the order and PA4 is wrong.
- Enters `asserted`. It is the load-bearing assumption of this entire
  ordering — PA4 and PA5 both fall if it is false — and it should be the
  first thing O attacks.

---

**What would falsify each:** stated inline. The three cheapest, in
order: **T4** (re-derive one binding under the opposite ADR-003 choice —
minutes, and PA4 and PA5 both fall if it breaks), **PA11** (name an
ADR-001 option under which the alias structure itself changes shape —
minutes, and it restores P2 to the critical path), **PA6** (implement
P10 after P6a and P7, and count what it catches that inspection would
not have).
