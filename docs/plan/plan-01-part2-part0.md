# Plan 01 — Part 2 (Observation) + the Part 0 fragment it depends on

**Stage:** plan · **Status:** block response filed, awaiting O
**Opened:** 2026-08-01 · **Last amended:** 2026-08-02 (amendment 8)

> **Blocks B and C cleared. Block A answered a second time** —
> amendment 7 removed P5's clause 3 and left nine of the ten local terms
> owned by no definition of done (BV4). Amendment 8 names every one of
> them **against `build/shapes.ttl`** so the criteria are checkable
> rather than prose. Verification pending.

Sequenced work items in topological order for the unit measured in
[`measure-01-part2-part0.md`](../measure/measure-01-part2-part0.md).
Items, dependencies and ordering only — *how* is the design stage.

Assertions are numbered **PA1–PA42** to avoid collision with the measure
document's A1–A40. Items live in [`items.yaml`](items.yaml); every item-keyed table below
is generated from it by [`derive-waves.py`](derive-waves.py) and checked
by `make lint`. The gate message for this document is in
`review-inbox.md`.

**Where a summary and the item table disagree, the table governs and the
summary is the bug.** Three occurrences: the P10 edge (amendment 3), and
the P6b wave rendering twice (amendments 5 and 7). **The rule has not
once caught a defect before O did** — see PA26, which downgrades the
wave view to non-normative rather than correcting it a fourth time.

## Amendment history — removed

**Deleted 2026-08-02, not migrated.** It was the fifth hand-maintained
list keyed by item id, and its failure mode is forgetting to append — a
failure it committed twice, once in the very row that records the
omission (row 6, "Recorded late").

Git is already this log and cannot forget:

```
git log --oneline -- docs/plan/
```

Every amendment since 2026-08-01 has a commit whose message states what
changed and why. A second copy maintained by hand added nothing except a
sixth place to be wrong.

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

 **Edges are typed**, because conflating two kinds of
dependency was the largest defect in the first draft of this section:

- **blocks-start** — the item cannot begin until its predecessor
  finishes. A hard sequence edge.
- **blocks-trust** — the item can begin and finish, but its *output is
  not evidence* until the predecessor lands. Not a sequence edge; a
  claim about what the result means.

<!-- BEGIN GENERATED:items - docs/plan/derive-waves.py. Edit items.yaml, not this. -->

| # | Item | Produces | Blocks-start | Blocks-trust | In-unit | Notes |
|---|---|---|---|---|---|---|
| **P1** | Name L2's relation | `Identity.lean` defines both candidate relations; H proposes the restatement | — | — | excused — completion needs an O session; the claim change is O's | Completion needs an **O session** — only O changes a claim's status. External dependency, not a work item |
| **P2** | Decide ADR-001 question 2 | design gate; A/B/C chosen or explicitly deferred | P1 | — | excused — decided at the design gate 2026-08-02 (ADR-001) | Blocks **P6b only**, not P6a — see PA11 |
| **P3** | Decide ADR-003 | design gate; Part 2's shape | — | — | excused — decided at the design gate 2026-08-02 (ADR-003) | Blocks P7 |
| **P4** | Rebuild `parts.als` under F10 | constraints by extension; T2 gets evidence or is recorded as unevidenced | — | — | excused — serves the first profile, a later unit | Blocks **nothing in this unit**; blocks the first profile, which is a later unit — see PA8 |
| **P5** | `vocab/prefixes.yaml`, 23 binding **identities**, external graphs cached | the binding surface — **external identity only** (PA25) | P20 | — | **required** | Blocks P6a, P7, P10 |
| **P6a** | Part 0 entity + alias core — the ADR-001 question-1 shape | `vocab/core/part0-*.yaml` | P5, P17 | P10 | **required** | Settled by ADR-001 Q1. Does **not** wait on P2. P17 carries PA29/PA30's preconditions, now an edge (BV12) |
| **P6b** | `candidateMatch` relation — Part 0 | a Part 0 relation binding two `Entity` instances, with provenance | P2 | P10 | **required** | **Non-empty.** ADR-001 chose option B, under which heuristic matches are recorded as `candidateMatch` facts. The deriving rule is `transform/`; the relation is Part 0 (ADR-000 D4) |
| **P7** | Part 2 — the observation shape, **excluding absence** | `vocab/core/part2-observation.yaml` | P3, P6a | P10 | **required** | Slot count depends on P9's boundary — see PA12 |
| **P8a** | Fixture capture, JSON-LD context, `make check` executing against P7's shape | `fixtures/`, a `check` that runs | P7 | **C17 axis 1** | **required** | "Green" ≠ "validating" — see PA13 |
| **P8b** | Context extended for P9's slots, check re-run | an up-to-date `check` | P9 | **C17 axis 1** | **required** | Not rework — the price of PA7's ordering. See PA15 |
| **P9** | The absence and health model | `absenceReason`, `observingSystemStatus`, the sentinel decoding | P7, P8a | **P14** | **required** | Closes ranked gap #3. Last **modelling** item. Authors `observingSystemStatus` — P5 does not (PG7) |
| **P10** | Range-vs-`slot_uri` drift check | C17 axis 2 closed | P5 | — | **required** | **Blocks-trust on P6a, P6b, P7** — see PA6 |
| **P11** | Name T3a's tiebreak | L4's precondition | — | — | excused — serves the merge unit, not this one | Outside this unit. Listed because merge work is the next unit and it has no predecessor — startable any time |
| **P12** | Determine the implemented matching rule | closes L2's second half | **source access this repo lacks** | — | excused — cannot close from this repository | Permanently open — see PA9 |
| **P13** | Fixture capture rules | `fixtures/README.md` — ordering key, F9 trap, per-fixture tier | — | — | **required** | Blocks P14. H's file. See PA22 |
| **P14** | Capture the T1 snapshot series | ≥24 consecutive hourly AirNow snapshots | P13 | — | **required** | **~24h irreducible floor.** **Blocks-trust on P9** — the edge is in P9's row, not only here (PA27) |
| **P15** | The §5.1 q9 experiment — PM2.5 threshold vs composite AQI | **DONE.** [`exp-01`](../experiments/exp-01-property-substitution.md) — C5 has affirmative evidence; C17 gains a third axis; invariant 4 has a wording gap | — | — | excused — done 2026-08-02 | Ran 2026-08-02. Prediction held on the generated path |
| **P16** | ~~Allowlist this project's own namespace~~ | **DONE before it was filed** — landed undeclared in commit `e1b1bdf` (BV13). Verified: all three BV8 namespaces now pass | — | — | excused — done before it was filed (BV13) | Closed. See PA35 |
| **P17** | Decide P6a's two preconditions — the carrier class for statement-level slots (PA30) and whether `crs` is a slot (PA29) | a design-gate record; A1's class count confirmed or moved 14 to 15 | — | — | excused — decided at the design gate 2026-08-02 (ADR-004) | **BV12.** PA30 called this a new blocks-start edge on P3's sibling; the design gate is not an item, so it could not be an edge. Now it is |
| **P18** | Decide how cross-slot constraints reach `make check` | a design-gate record choosing one of three: hand-written SHACL beside generated (breaks invariant 1), a generator emitting them from LinkML `annotations:`, or out-of-scope | — | — | excused — decided at the design gate 2026-08-02 (ADR-005) | **C5's carrier.** `exp-01` shows `sh:equals` catches the substitution and `gen-shacl` cannot emit it. Without this item C5's affirmative evidence has nothing to rest on |
| **P19** | Cross-slot constraint generator | SHACL `sh:equals` and kin emitted from LinkML `annotations:`, after `gen-shacl` | — | — | excused — ADR-005's implementation; not required by plan 01's scope statement, and C5 stays `asserted` until it exists | ADR-005. **C5's affirmative evidence depends on this, and it is outside plan 01's scope statement** — recorded rather than smoothed over |
| **P20** | Restate P5 and the four prose passages over ADR-004's generated worklist | a plan of record whose live sites name the enumerated list, not a retired count | — | — | **required** | **Repair, not discovery.** The criterion-4 retired-figure sweep is a gate duty and is deliberately NOT an item — a gate duty in the item graph makes the graph model the process rather than the work. **Twelve live sites, and the number has moved twice in two days — treat the census as dated, never as fixed.** Eight censused 2026-08-03 — `items.yaml` P5 item and `done_when` (source), the item and done tables (generated from them), PA5, T4a, PA19, T4 — plus two found by O on 2026-08-04 (BV7-4): PA25's *'PA19 was right about the 23'*, 27 lines above PA19's own marker, and PA25's `assertedTime` paragraph, whose `the 23 —` an em-dash hides from the enumeration. Plus **two more H found on 2026-08-04** by widening its own marker checker to anchor on the determiner (`the 23`, `the ten`) instead of on a following noun: PA28's *'every one of the ten'* and *'nine of the ten'*. All twelve are marked and none corrected. **The second of those two also asserted a decided question was open** — ADR-004 Decision C — and that half is withdrawn in place rather than deferred, because a stale figure misleads about a quantity while a stale open-question misleads about what is settled. **The first version of this criterion named four literal strings, covered three phrasings, and could not see PA19's `23 external identities` or T4's `23 external bindings` — two of its own eight sites (BV6-1).** A criterion satisfiable without doing the thing it exists for; eighth instance of *the subject is narrower than the claim*, inside the definition of done written to close the seventh. `23 bind / 10 write of 33` is the figure ADR-004 retires as unrecoverable. **No new total** — that would be a sixth figure agreeing with a fifth by accident |
| **P21** | Clear the design-gate rationale residues, in one pass | `docs/residuals-01-design-gate.md` with every entry moved to Cleared | — | — | **required** | **`FALSIFIER.md` §3.1.** A rationale defect inside a decided ADR records; a decision defect blocks. Eight gate rounds produced eight partial passes, and a partial retraction is worse than none — withdrawn at one site, standing at another, the document disagreeing with itself. Same repair shape as **P20**: one pass over a written list. **A marker is not a repair** — marked sites tell a reader the passage is stale and name the owner; restating them is this item's work |

<!-- END GENERATED:items -->


**PA4 — the order is three waves plus two items with no wave.** The
first draft wrote this as `P1 · P5 · P4 ‖ P3 · P2 · P10 · P6 · P7 · P8 ·
P9`, which was pseudo-notation that did not say what `·` and `‖` bind
and contradicted its own prose. Waves instead:

**Generated from the item table by [`derive-waves.py`](derive-waves.py).** Levels are computed from the
`Blocks-start` column. **Blocks-trust edges are deliberately not levels** —
per PA6 they constrain whether an item's output is evidence, not when it
can start.

The hand-maintained copy that stood here drifted from the item table
**five times in five amendments**, and the fifth was the repair for the
fourth. `derive-waves.py --check` fails if this block is stale.

<!-- BEGIN GENERATED:waves - docs/plan/derive-waves.py. Edit items.yaml, not this. -->

| Wave | Items |
|---|---|
| **1** | **P1**, **P3**, **P4**, **P11**, **P13**, **P15**, **P16**, **P17**, **P18**, **P19**, **P20**, **P21** |
| **2** | **P2**, **P5**, **P14** |
| **3** | **P6a**, **P6b**, **P10** |
| **4** | **P7** |
| **5** | **P8a** |
| **6** | **P9** |
| **7** | **P8b** |
| **—** | **P12** — not startable here: source access this repo lacks |

<!-- END GENERATED:waves -->


**On its first run the generator found more drift than BV9 named.** The
hand table had **P14 in wave 1** while its own row gives it
`blocks-start: P13`, and **P6a in wave 3** when it is level 2. BV9 caught
P15's absence; two further disagreements were sitting beside it,
unreported by four consecutive reviews of that table.

**Wave 1 has an internal order** — by external latency, not by size. See
PA17.

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

**PA5 — P5 is the long pole. It is no longer startable today.** This
read *"startable today … it has no predecessor"* until 2026-08-03, when
**P20** was added and P5 gained a `blocks-start` edge on it: P5's own
definition of done is stated over a population ADR-004 retired, so the
restatement precedes the work. P5 is now wave 2. It is still the widest
item and everything in wave 3 still waits on it.

Amended for the dependency only. **Every figure from here to the end of
PA5's justification — including the T4a paragraph below — is P20's
subject and is deliberately untouched.** Scope widened 2026-08-04: this
read *"the rest of this paragraph"* and *"the sentence below"*, both
singular, which did not obviously reach a passage two paragraphs down.
`23` and `10` here are the retired population; correcting them while
seven other live sites stand is the partial retraction this project has
been bitten by three times. It goes in one pass or not at all.

The 23 bindings are content-verified (A3 as amended, S4) and the 10
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

<!-- BEGIN GENERATED:done - docs/plan/derive-waves.py. Edit items.yaml, not this. -->

| # | Done when | Size |
|---|---|---|
| **P1** | Both candidate relations are defined in `Identity.lean` and L2's entry names which one it is about. **Needs an O session** — H cannot close it | S |
| **P2** | **MET 2026-08-02.** ADR-001 records option **B** with its reason: B is the only option whose correctness does not depend on resolving L2 | S |
| **P3** | **MET 2026-08-02.** ADR-003 records option **B**; `docs/coverage.md` and ADR-002's modality table amended in the same pass | S |
| **P4** | `parts.als` models constraints by extension; **the M1 mutation changes the output**; the header's C1/C2 claims are true or removed | M |
| **P5** | `prefixes.yaml` resolves every prefix used; all 23 external terms are content-verified by fetch-and-grep; external graphs are cached locally. **The ten local terms are NOT declared here** — clause 3 removed, see PA25. **[Marked 2026-08-04, figure untouched: `23 external terms` and `the ten local terms` are the population ADR-004 retires as unrecoverable; its generated worklist replaces them, and **P20** owns the restatement. A marker is not a retraction — the censused sites go in one pass.]** | **L** |
| **P6a** | **P17 answers PA29 and PA30's decisions first** (a blocks-start edge, not a sentence — BV12). Then: `build/shapes.ttl` carries an `sh:path` for **`id`, `identifierValue`, `identifierScheme`, `issuingAuthority`, `assertedTime`, `elevation`, `sourceVerificationTier`**, and for `crs` or PA29's substitute (**PA28**); `operatingMode`, `modelVersion`, `profileConformance` likewise (PG5); **for each of those seven, cardinality and range are identical under both ADR-003 options**; `make gen` runs to completion, which requires `vocab/core/vocabulary.yaml` (PG11); the core validates under `make lint` (P16 is **done**, BV13); `flat-siblings.yaml` still passes | M |
| **P6b** | `build/shapes.ttl` carries an `sh:path` for the `candidateMatch` relation's slots, and no heuristic match appears as an identity fact | S–0 |
| **P7** | `make gen` produces `build/shapes.ttl` from Part 2 + P6a with no LinkML error, **and it carries an `sh:path` for `procedureKind`** — or ADR-003's record states the slot does not exist (PA28) | M |
| **P8a** | **Under ADR-003 option B:** `make check` executes against ≥1 real AirNow **and** ≥1 real Open-Meteo capture and reports violations it can see. **Under option A:** AirNow only — Open-Meteo has no Part 2 shape to validate against (A5), and the Open-Meteo captures are retained as Part 3 fixtures for a later unit. See PA21 | M |
| **P8b** | The context maps P9's slots; `make check` re-run and green | S |
| **P9** | All three absence semantics and all three sentinel channels round-trip distinguishably (A16, F5, F6), **and `build/shapes.ttl` carries an `sh:path` for `observingSystemStatus` and `absenceReason`** (PA28) | **L** |
| **P10** | A check compares each `slot_uri`'s external range against the local **effective** range — via `linkml_runtime` `SchemaView.induced_slot`, **not raw YAML** (PA34) — and fails on disagreement; the `sosa:observedProperty` case from A34 fires; it survives a schema using `slot_usage` or a mixin | M |
| **P11** | T3a's entry names a tiebreak, or records that none exists | S |
| **P12** | — permanently open | — |
| **P13** | The ordering key is named (`ValidTime` UTC, not `LocalTimeString`), the F9 seasonal-offset trap is recorded, and the verification tier and capture timestamp are required per fixture | S |
| **P14** | ≥24 consecutive hourly AirNow snapshots exist under P13's rules, with gaps recorded rather than silently skipped | S work, **~24h floor** |
| **P15** | **MET 2026-08-02.** A PM2.5-specific threshold and a composite `us_aqi` reading run through `gen-shacl` and pyshacl, result recorded against the prediction stated in advance — [`exp-01`](../experiments/exp-01-property-substitution.md) | S |
| **P16** | **MET before it was filed** (BV13). All three BV8 namespaces pass `drift-lint.py`, and `bound-vocabularies.yaml` / `redirect-service.yaml` still behave | S |
| **P17** | **MET 2026-08-02.** ADR-004: no `crs` slot (`asWKT` range constrained to `geo:wktLiteral`); `Statement` is a Part 0 class binding `prov:Entity`; A1's class count moves **14 to 15** | S |
| **P18** | **MET 2026-08-02.** ADR-005 picks option **B** — cross-slot constraints declared in LinkML `annotations:` and emitted by a project generator — and states why A and C were rejected | S |
| **P19** | `exp-01`'s case A raises a violation under `make check`, and the `sosa:observedProperty` case from A34 does too — both from `annotations:` in the source, with nothing hand-written under `build/` | M |
| **P20** | **Re-derive the census first; do not carry the one in `notes`.** A 2026-08-03 census bounded a 2026-08-04 criterion and two live sites fell outside it (BV7-4) — one because an em-dash defeats the enumeration's pattern, one because its hit was filtered as noise. The census is a measurement with a date, not a definition. Then: every censused site names **ADR-004's generated worklist** and states no count — P5's item and `done_when`, and **the plan's copies** of PA5, PA19, T4 and T4a. The register copies at `claims.md` are **out of scope**: restating a register claim is a proposal H makes and O disposes, and T4a's Evidence already carries the note. **The guard is derived, not remembered:** re-run `grep -ohE '(23|ten|10) [a-z]+( [a-z]+)?' docs/plan/ -r | sort | uniq -c | sort -rn` **before writing it**, and build the pattern from what it returns. As of 2026-08-04 that is six phrasings for `23` — `bind`, `binding`, `bindings`, `external terms`, `external identities`, `external bindings` — plus `(ten|10) local( terms)?` and `10 write of`. **Verified by putting each measured phrasing back one at a time and watching the guard fail**, not by observing that the guard exists. Quoted (`*"…"*`) and blockquoted (`>`) text is exempt, as in `derive-surface.py`, and **the exemption is probed against a retraction before shipping** — historical sites stay: the closed measure document, quoted originals, amendment records. `derive-waves.py --check` and `derive-surface.py --check` both pass | S |
| **P21** | Every entry in `docs/residuals-01-design-gate.md` is under **Cleared** with the repair named and the marker removed, and each cleared entry's own falsifier has been **run** and returns nothing. Then: the ADR states its ground in one section and references it elsewhere, per `ADR-template.md`. **Verified by the paraphrase sweep, not a string sweep** — restate each withdrawn claim without reusing its wording and grep the content words that survive, which is the instrument that would have caught R1 and the one a string sweep cannot be | S |

<!-- END GENERATED:done -->


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

Ranking wave 1 by size put P5 first and left P1's O-turnaround
un-started, so the wall clock paid for it serially at the end.
**P5 left wave 1 on 2026-08-03** when P20 became its predecessor, which
strengthens this argument rather than weakening it: the size-first
ranking would now start an item that cannot start. Ranking
by latency starts the externally-blocked items first and does P5's work
*while* they are pending:

<!-- BEGIN GENERATED:latency - docs/plan/derive-waves.py. Edit items.yaml, not this. -->

| Order | Item | Why here |
|---|---|---|
| 1 | **P1** | **long** — an O session; start it so the wait runs alongside |
| 2 | **P3** | **long** — a design-gate decision; start it so the wait runs alongside |
| 3 | **P17** | **long** — a design-gate decision; start it so the wait runs alongside |
| 4 | **P18** | **long** — a design-gate decision; start it so the wait runs alongside |
| 5 | **P4** | short — fills the wait |
| 6 | **P11** | short — fills the wait |
| 7 | **P13** | short — fills the wait |
| 8 | **P15** | short — fills the wait |
| 9 | **P16** | short — fills the wait |
| 10 | **P19** | short — fills the wait |
| 11 | **P20** | short — fills the wait |
| 12 | **P21** | short — fills the wait |

<!-- END GENERATED:latency -->


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

<!-- BEGIN GENERATED:membership - docs/plan/derive-waves.py. Edit items.yaml, not this. -->

**Plan 01 is done when these meet their criteria:** **P5**, **P6a**, **P6b**, **P7**, **P8a**, **P8b**, **P9**, **P10**, **P13**, **P14**, **P20**, **P21**.

**Excused, each with its reason:**

- **P1** — completion needs an O session; the claim change is O's
- **P2** — decided at the design gate 2026-08-02 (ADR-001)
- **P3** — decided at the design gate 2026-08-02 (ADR-003)
- **P4** — serves the first profile, a later unit
- **P11** — serves the merge unit, not this one
- **P12** — cannot close from this repository
- **P15** — done 2026-08-02
- **P16** — done before it was filed (BV13)
- **P17** — decided at the design gate 2026-08-02 (ADR-004)
- **P18** — decided at the design gate 2026-08-02 (ADR-005)
- **P19** — ADR-005's implementation; not required by plan 01's scope statement, and C5 stays `asserted` until it exists

*12 required, 11 excused, 23 items. Both lists are projections of one field, so the set difference cannot disagree (BV21).*

<!-- END GENERATED:membership -->


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

Two new items — **P13 in wave 1, P14 in wave 2**:

*(Both items' criteria are now rows in the generated table above.)*

> **Corrected 2026-08-04 (BV6-3). This read *"both wave 1"*, and it is
> BV17/BV24's surviving half.** That defect was *"P14 was in wave 1 while
> its own row gives it `blocks-start: P13`"*; the item table was
> corrected and **this sentence — the one the assertion originally came
> from — was not.** The generator then removed the drifting table from
> under the claim and left the claim, so nothing disagreed with it any
> more.
>
> **The argument survives, and it is worth stating why rather than
> asserting it.** PA22's point is the ~24h irreducible floor: the capture
> must be *started* early or the wall clock pays for it at the end. The
> floor belongs to **P14**, whose predecessor **P13 is in wave 1 and is
> S-sized**. So the capture is startable as early as PA22 requires — P13
> then P14, both inside the wait that P1's O-turnaround and P3's
> design-gate decision already impose. **What is false is "both wave 1",
> not "start it early".**

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

**PA25 — Block A. The ten-row table, and it repairs PA19 by removing
clause 3 from P5 rather than by narrowing it.**

O's experiment reproduces here: a LinkML slot with no `range`, no
`required` and no `multivalued` emits `sh:maxCount 1`, and
`multivalued: true` removes it. **Declaring a slot chooses a
cardinality, silently.** So clause 3 of P5's criterion — *"the 10 local
terms are declared"* — is authoring form, and PA19's identity/form split
does not reach the ten. PA19 was right about the 23 and wrong to let
clause 3 ride on the same argument.

> **`the 23` and `the ten` here are the retired population; P20 owns the
> restatement.** Marked 2026-08-04. This site is 27 lines above PA19's
> own marker, so a reader arriving here has not passed one — which is
> why the census that bounded P20 needed widening rather than the marker
> moving.

| # | Term | Class · Part | Authored at | ADR-dependent? |
|---|---|---|---|---|
| 1 | `id` | `Entity` · 0 | **P6a** | No. The *minting rule* is open (A10) but the form is 1..1 under every option |
| 2 | `identifierValue` | `Identifier` · 0 | **P6a** | No — ADR-001 **Q1** settled it |
| 3 | `identifierScheme` | `Identifier` → SKOS · 0 | **P6a** | No — Q1 |
| 4 | `issuingAuthority` | `Identifier` → `Agent` · 0 | **P6a** | No — Q1 |
| 5 | `assertedTime` | `Identifier` · 0 | **P6a** | No — **and it may not belong in this list**, see below |
| 6 | `crs` | `Geometry` · 0 | **P6a**, if at all | No — conditional on a GeoSPARQL decision, not on either ADR |
| 7 | `elevation` | `Place` · 0 | **P6a** | No |
| 8 | **`procedureKind`** | `Procedure` · **2** | **P7** | **YES — ADR-003** |
| 9 | **`observingSystemStatus`** | absence/health · 2 | **P9** | No — and P5 must not claim it (PG7) |
| 10 | `sourceVerificationTier` | **carrier undecided — P17** · 0 | **P6a** | No |

**One of ten is ADR-dependent. It is a Part 2 slot and it is authored at
P7, which blocks-start on P3.** Nine are authored at P6a or P9 and none
of those is ADR-dependent.

**The repair: clause 3 leaves P5 entirely.** Not narrowed — removed. The
ten have no external identity to resolve; a term with no external URI
*is* its name, and everything else about it is local form authored where
its class is authored. P5 resolves the 23 external identities, declares
prefixes, and caches graphs. That is the resolve-and-cache reading
applied consistently instead of applied to three clauses out of four.

> **`23 external identities` is the retired population. P20 owns the
> restatement.** ADR-004 retires `23 bind / 10 write of 33` as
> unrecoverable; the replacement is its generated worklist, not another
> total. Marked 2026-08-04, figure deliberately untouched — a marker is
> not a retraction, and the eight censused sites go in one pass.

O pre-empted the weaker repair — reading "declared" as *enumerated* —
and was right that it fails: a clause satisfiable by transcription is
not a definition of done. **Removal is the repair that survives that
objection**, because the ten are then covered by items whose criteria
already bite.

**PA18's abort still does not fire, but for a different reason than
PA19 gave.** Not "P5 does not author form" — it did, and that was the
defect. The reason is that **once clause 3 is removed, every
ADR-dependent term is authored behind its ADR's edge**: `procedureKind`
at P7, and P7 waits on P3. The Part 2 exemption is sound; PA19's
justification for it was not.

> **The design-gate question this paragraph calls open was decided, and
> this is the worse of BV7-4's two sites because it is not only a
> figure.** `ADR-004` **Decision C** settled it and `claims.md:630`
> records it: **`assertedTime` and `prov:generatedAtTime` are one
> slot.** So *"whether `assertedTime` binds `prov:generatedAtTime`
> specifically is a design-gate question"* and *"I am not moving the
> count"* now tell a reader a decided question is open. Marked
> 2026-08-04; the figures stay for **P20**, but **the openness claim is
> withdrawn here rather than deferred**, because a stale figure
> misleads about a quantity and a stale open-question misleads about
> what is settled.
>
> `24 bind / 9 write` is itself a retired figure — ADR-004 retires the
> whole `bind / write of N` family and replaces it with a generated
> worklist. P20 owns that half.

**A third double-count, found while building the table.**
`assertedTime` is item 5 of the ten *and* `prov:generatedAtTime` is
among A3's five PROV terms in the 23 — and ADR-001 §4 states plainly
that "`assertedTime` comes from PROV-O." If they are the same slot the
surface is **24 bind / 9 write**, not 23/10. **I am not moving the
count**: A1 is the measure document's and whether `assertedTime` binds
`prov:generatedAtTime` specifically is a design-gate question. Recorded
here because it is the third instance this week of one slot claimed
twice — after `observingSystemStatus` (P5/P9, PG7) and PA12's P7/P9.

**Falsifier for PA25:** a term in the table authored at an item other
than the one named, or an ADR-dependency the table misses.

**PA26 — Block B. The wave table is a derived view, it has drifted
three times in three amendments, and it is now labelled non-normative.**

PG1's third rendering was wrong the same way as the first two. The item
table gives P6b exactly one blocks-start edge — **P2** — and no
dependency on P6a. "Branching off P6a" still asserts P6a precedes it,
and P6a waits on P5, the L-sized long pole, so the rendering put P6b
behind work it does not wait on. PA11's entire point is that P6b's
dependencies are *narrower* than first claimed.

O's diagnosis is the one that matters: **the wave table has no cell for
an item whose predecessor finished two waves earlier.** The abstraction
does not fit the graph, and I have now bent it three times rather than
saying so.

Two changes:

1. **P6b is shown on its own line, startable when P2 lands, with no
   dependency on the P6a chain.**
2. **The wave table is marked derived and non-normative.** Three drifts
   in three amendments is enough evidence that a hand-maintained second
   copy of the graph is a liability. The standing rule — *the table
   governs* — was added in the same amendment that violated it, which as
   O says makes it a way of describing defects rather than catching
   them. Labelling the view as derived is weaker than deleting it and
   stronger than another correction; **the honest position is that this
   is mitigation, not a fix.** A generated view would be the fix.

**Falsifier for PA26:** a fourth drift between the wave view and the
item table.

**PA27 — Block C. The P14 → P9 edge is now in the table, as
blocks-trust.**

P14 was added to produce the 24 snapshots and **the dependency did not
come with it** — the only record was prose in a Notes cell, and under
the document's own governing rule the table is the plan. P9's criterion
was satisfiable against the single snapshot C11 already measured, which
is precisely the state PG3 was filed against.

On the typing PA6 introduced, this is **blocks-trust**: P9 can be
authored without P14, and its output is not evidence until P14 lands.
Same shape as P10's edge. Adding the item and omitting its edge is a
new failure mode worth naming — **an item added to close a finding can
leave the finding open if the reason it was added lives only in prose.**

**Falsifier for PA27:** a reading of P9's criterion satisfiable with
fewer than 24 snapshots once the edge is in place.

---

> **`the ten` here and below is the retired population — P20 owns the
> restatement, and this passage was outside the census until
> 2026-08-04.** Marked, figure untouched.

**PA28 — Block A. Every one of the ten is now named in a definition of
done, and the criteria are stated against generated output rather than
against prose.**

BV4 is accepted in full. Removing clause 3 fixed the ADR-ordering defect
and created a worse one: **nine of the ten had no owner at all**, and
your probe proves P6a was declarable done with none of its eight. My
"the criteria already bite" was an assertion, and you checked it instead
of arguing with it.

The repair is not to put the terms back in prose. `sh:path` appears once
per slot in `gen-shacl` output and an absent slot is absent — verified
here — so **the criteria now name terms against `build/shapes.ttl`**,
which makes them mechanically checkable and makes your probe's file fail
rather than pass.

| Item | Added to its definition of done |
|---|---|
| **P6a** | `build/shapes.ttl` contains an `sh:path` for **`id`, `identifierValue`, `identifierScheme`, `issuingAuthority`, `assertedTime`, `elevation`, `sourceVerificationTier`** — and for `crs` **or** the PA29 substitute |
| **P7** | an `sh:path` for **`procedureKind`**, or ADR-003's record states it does not exist as a distinct slot |
| **P9** | an `sh:path` for **`observingSystemStatus`** and **`absenceReason`** |

**What clears the block, in your terms:** rebuild your probe file — the
eight Part 0 classes, PG5's three slots, one bound slot, none of the
eight local terms — and P6a's criterion now **fails**, because
`shapes.ttl` will carry no `sh:path` for seven of them. The clause that
was vacuously true is gone.

**And the first clause is fixed too.** *"No Part 0 slot's cardinality or
range differs by ADR outcome"* was satisfied best by declaring no slots
— §4 question 2 applied to a definition of done, which is a check I had
not thought to run on my own criteria. It now reads: *for each of the
seven Part 0 terms named above, its cardinality and range are identical
under both ADR-003 options.* Vacuity is no longer available to it.

**Falsifier:** a file satisfying every clause of P6a while missing a
term the clause names.

**PA29 — BV5. `crs` carries its condition and its substitute, to PG6's
standard.**

PA25 said "P6a, if at all — conditional on a GeoSPARQL decision", and
`GeoSPARQL` appears once in this plan, in that cell. P2 is ADR-001 Q2
and P3 is ADR-003; neither is this decision, and no item makes it.

Stated to the standard PG6 set:

- **If a distinct `crs` slot is carried:** P6a's criterion requires an
  `sh:path` for it.
- **If it is not** — because GeoSPARQL puts the CRS inside the
  `wktLiteral` (A26) — P6a's criterion instead requires that
  **`asWKT`'s range is `geo:wktLiteral`**, so the CRS has a documented
  carrier rather than silently none. **The surface is then 23/9 of 32**,
  per A1's own arithmetic.
- **The decision belongs to the design gate** and is now recorded as a
  P6a precondition rather than as an unowned aside.

**PA30 — BV6 and PG10 are one defect: A1's Part 0 fragment has no class
for statement-level properties, and it is short by one.**

Four slots have no home among A1's eight Part 0 classes — `Entity`,
`Identifier`, `Asset`, `Place`, `Agent`, `Activity`, `TemporalExtent`,
`Geometry`:

| Slot | Source | Proposed carrier |
|---|---|---|
| `sourceVerificationTier` | A24 | statement-level |
| `operatingMode` | C12 / PA23 | statement-level (`Statement`, PG10) |
| `modelVersion` | C15 / PA23 | statement-level |
| `profileConformance` | C15 / PA23 | statement-level |

**You are right that PA25 invented a class.** `Alias` does not occur in
the measure document; the only near hit is `AliasKind`, which A32 is at
pains to call **a type distinction, not a class**. A1's Part 0 class for
items 2–5 is **`Identifier`**, and PA25's Class column is corrected to
say so.

The larger consequence I am **reporting and not acting on**: ADR-002
records `Statement` as "the sixth [entity], already covered by the
provenance layer and needs no new class." Four slots now want to hang
off it. If they land on `Statement`, **A1's class count moves 14 → 15**;
if they land on `Activity`, ADR-002's provenance reading has to carry
them. Either answer changes a measure-document number, and `measure-01`
is not mine to edit at a plan gate — the same handling as PA23 and the
`assertedTime` double-count.

**Scheduled, so it is not silent:** the decision is a **P6a
precondition**, alongside PA29's. P6a cannot start until both are
answered, which is a new blocks-start edge on **P3**'s sibling — the
design gate — not on P3 itself.

**PA31 — BV7. The fourth drift was already in the file, and the label
did not prevent it.** P15 was absent from the wave table from the moment
amendment 6 added it, and **amendment 7 re-read that table specifically
to fix a drift and did not see it.** P15 is now in wave 1.

You are right that this is stronger evidence for generation-over-labelling
than PA26's own argument, and for the reason you give: it is a drift the
label did not prevent, not one it retroactively excused. **PA26's
falsifier has fired.** Recorded as fired rather than explained away —
the mitigation is worth less than PA26 claimed, and a generated view is
the fix.

**PA32 — BV8. P6a's lint clause is unsatisfiable as the tooling stands,
and by PA14 that makes it an item.**

The jurisdiction rule runs `check_uri` over every `prefixes:` entry, and
a Part 0 core file must declare this vocabulary's own namespace. Your
three-host table reproduces: no namespace this project can choose is
admitted — `w3id.org/hazard-vocab/` fails as an unallowlisted shared-redirect
path, and any self-hosted or example host fails as an unknown host.

So *"the entity and alias core validates under `make lint`"* cannot be
met by any real file. Same class as PG11, same disposition: **this
unit's output depends on it, so it is an item** — **P16**, allowlist
this project's own namespace. `scripts/` is human-owned; naming an item
does not assign it.

**The direction is the interesting part and it is yours:** this is the
**precision** half of C18 firing on the first file the project authors
*for itself*. All five earlier counterexamples were about content
borrowed from elsewhere.

**PA33 — PG9 and PG11 closed, the same way PG5 was.** Neither scheduled
nor excluded is the one state a plan may not leave a known-falsified
claim in, and PA23 set that standard while leaving two more in it.

- **C13** — `falsified`, and BV2 keeps it there. **Deferred with a
  reason:** the correction/supersession pair is Part 0 statement-level
  content that lands on the same unowned carrier as PA30's four slots.
  It cannot be scheduled before PA30's decision, and scheduling it into
  this unit would repeat exactly the defect PA30 records. Design gate.
- **C14** — releasability. **Deferred with a reason:** ADR-002 calls it
  "a dimension, not a row", and A1 measures no slot for it. Out of this
  unit's surface; it belongs to whichever unit authors the statement
  layer.
- **PG11 / `vocabulary.yaml`** — no item produced `make gen`'s entry
  point. **Added to P6a's definition of done:** `make gen` runs to
  completion, which requires `vocab/core/vocabulary.yaml` to exist and
  import what P6a authors.

**PA34 — two design-gate items from the owner, recorded here so they are
not discovered later.**

- **P10 must use `linkml_runtime`'s `SchemaView`, not YAML parsing.** It
  compares a slot's *effective* range against the bound term's published
  range, and effective means after `slot_usage`, mixins and inheritance
  — none of which raw YAML shows. `SchemaView.induced_slot(slot, class)`
  gives the resolved form. **Built on YAML parsing, P10 would work on
  flat schemas and break silently on the first mixin**, which is the
  failure direction that has cost this project the most. Recorded in
  P10's definition of done.
- **`drift-lint.py` carries a recall prediction in its docstring**: raw
  YAML does not resolve `imports:`, so `is-a-depth` will compute depth
  per file and miss chains crossing file boundaries, and `role-named`,
  `jurisdiction` and `exact-mappings` degrade the same way against
  inherited or `slot_usage`-added content. **False negatives — F2 in a
  new dress and in the worse direction.** The trigger is stated: recheck
  the first time `vocab/core/` holds more than one file. **That is P6a
  or the unit after it.** Flag it as a finding when it fires; do not
  work around it.

---

**PA35 — BV9–BV12. The wave view is generated now, and the generator
found more drift than BV9 named.**

Four repairs landed in prose instead of in the table, which is the third
time this plan has been blocked on prose-not-table and the fifth
wave-table drift in five amendments — the fifth being the repair for the
fourth. I have said twice that generation is the fix and the label is
mitigation. This acts on it.

[`derive-waves.py`](derive-waves.py) reads the item table's
`Blocks-start` column, computes topological levels and prints the view.
`--check` fails if the embedded block is stale. **The hand-maintained
copy is deleted**, not annotated.

**On its first run it failed, and not only where BV9 said.** BV9 caught
that P15 was absent. The generator also found:

- **P14 was in wave 1** while its own row gives it `blocks-start: P13`.
- **P6a was in wave 3** when it is level 2.

Both were sitting beside the drift BV9 reported, unnoticed by four
consecutive reviews of that table. That is the argument for generation
stated as a measurement rather than as a principle: the hand copy was
wrong in three places and the review process found one.

Two properties worth stating, because a generator can be wrong silently:

- **Blocks-trust edges are deliberately not levels.** Per PA6 they
  constrain whether an item's output is evidence, not when it can start.
  A generator that levelled them would have moved P9 behind P14 and
  changed the plan.
- **Prose in the dependency column is not read as an edge.** P12's cell
  says "source access this repo lacks"; it is reported as *not startable
  here* rather than parsed into a dependency or silently dropped.

**Falsifier:** an item whose generated level contradicts its own row, or
a `--check` pass over a document whose wave block disagrees with the
item table.

**PA36 — BV10 and BV12. Two edges that were prose are now edges, and one
of them required inventing the item it points at.**

- **BV10** — P16's relation to P6a lived in a Notes cell. It is moot:
  P16 is closed (PA35a below), and P6a's criterion no longer references
  it.
- **BV12** — PA30 called its precondition *"a new blocks-start edge on
  P3's sibling — the design gate."* **The design gate is not an item, so
  it could not be an edge.** That is why the repair landed in prose: I
  described an edge to something the table cannot name. The fix is
  **P17**, an item that decides PA29's `crs` question and PA30's carrier
  question, with `P6a blocks-start: P5, P17`.

I named this failure mode in BR-3 and again in PA27 — *an item added to
close a finding can leave the finding open if the reason lives only in
prose* — and then did it twice more in one amendment.

**PA37 — BV11. PA25's Class column now says what PA30 says it says.**
Rows 2–5 read `Identifier`; row 10 reads *carrier undecided — P17*.
PA30 asserted the correction had been made and it had not, which is
§5.2 item 4 inside a single document.

**PA35a — BV13. P16 was done before it was filed, and the change was
undeclared.** `own-namespace.yaml` and a 50-line `drift-lint.py` change
landed in commit `e1b1bdf` — my P15 commit — and my P15 message declared
none of it. P16 is closed and *"blocked by P16"* is out of P6a's
criterion.

The declare-don't-discover rule puts the assertion in the next
`[H → O]` message; the P15 result **was** that message. O found it by
checking `git status` and mtimes, for the second consecutive pass.

**PA38 — BV14 and BV15/C20, declared per the tooling rule, verified by
running.**

| Change | Verified |
|---|---|
| `make lint-selftest` | **26 pairs, 7/7 rules with demonstrated recall** (was 23, 6/6) |
| `documented` rule — requires `description` and `examples`, rejects `TODO`/`TBD`/`FIXME` | present; `undocumented.yaml` fixture in place |
| BV14 fix — `default_prefix` honoured only when it agrees with `id:` | `default-prefix-escape.yaml` present as a **recall** case |

**BV14's framing is the part to carry, and it is not about this fix.**
BV8 was a **precision** failure; its repair introduced a **recall**
failure; and the fixture shipped with the repair demonstrated precision
only. *A repair that closes one direction and is tested in that
direction alone is how a fix introduces a counterexample.* That is the
seventh C18 counterexample and the first introduced by a repair.

**BV15/C20** — invariant 7 claimed lint enforced `description` and
`examples` and nothing did, so P6a's *"validates under `make lint`"*
would have admitted a fully undocumented core. C6 rests on invariant 7
and has no other guard.

**PA39 — C5's carrier is now an item.** O's disposition is sharper than
my "conditional": the shape that makes C5 true **cannot be generated**,
**cannot be hand-added where validation reads** (invariant 1 forbids
editing `build/`, and `make check` reads only `build/shapes.ttl`), and
appears in **no item's definition of done** — `sh:equals` occurs zero
times in `docs/plan/`. That is BV4's shape applied to a claim instead of
to a slot: the thing the conclusion rests on is unowned.

**P18** owns it, and it is a decision item, not an implementation:
hand-written SHACL beside generated (breaks invariant 1), a generator
emitting cross-slot constraints from LinkML `annotations:` (preserves
single-source, real work), or accepting them as out of scope and losing
C5's affirmative evidence with them.

Worth recording what O noted about the register: **the restatement C5's
own entry proposed during the sweep — "raises a validation violation
under `make check`" — has now been executed, and on the generated path
it conforms.** Had that restatement been adopted, C5 would be entering
`falsified` today. The claim survives because it was not sharpened, and
that is not a comfortable reason to survive.

**PA40 — BV16, and the diagnosis matters more than the third attempt.**

`RecordedNotDeleted` was not a tie. **`Monotone merge` implies it for
every `rel`** — the `rel x y` hypothesis is discarded — so conjuncts 2
and 3 of `AdequateC13` were discharged by properties of `merge` alone.
O's theorem is now in the file as
`recorded_is_implied_by_monotone_for_any_rel`, kept as a refutation.

**The smaller finding is the one that explains both failures.**
`Distinguishes corrects supersedes` and `Monotone merge` **quantify over
disjoint variables**. Neither could imply the other — there is no shared
subject for an implication to run through. So they were never two halves
of one condition; they were two conditions, and proving they do not
imply each other demonstrated nothing about their relationship. My
commentary called them independent halves; that was wrong for a better
reason than the bidirectional overreach it replaced.

**Third attempt:** `DistinguishesIn` requires the witnesses to be facts
**present in a set**, and `PreservesDistinction merge corrects
supersedes` requires merging not to destroy the distinction. All three
subjects appear; the witnesses live in the merged set.
`union_preserves_distinction` shows it is meetable and
`retracting_merge_loses_distinction` shows it bites.

**And its limit is stated in the file rather than left to a fourth
round:** it does not establish that the relations are the ones an
implementation actually uses, and nothing at this abstraction can,
because they are parameters. C13 is discharged by an implementation
exhibiting the condition for **its own** merge and relations — and
`transform/` is still one `.gitkeep`.

---

**PA41 — BV21, BV22 and BV24 closed together, by making every
item-keyed view a projection of one source.**

You counted what the last four blocks were actually about: **five
hand-maintained lists keyed by item id.** BV9 was list 1 against list 2.
BV17 was list 2 against itself. BV21 is list 4. BV24 is lists 3 and 5.
Generating the wave view stopped it dead for one list and was never
applied to the rest — which is the same shape as BV14 and BV18: a repair
applied in one direction and not beside it.

[`items.yaml`](items.yaml) is now the source. Every item-keyed table in
this document is generated from it into a marked block:

| Block | Was |
|---|---|
| item table | list 1, hand |
| wave view | list 2, generated since amendment 9 |
| definition-of-done | list 3, hand, two shapes (BV17) |
| latency ranking | list 4, hand, stale since amendment 6 (BV24) |
| in-unit / excused | list 5, hand (BV21) |

**BV21 is not fixed, it is dissolved.** The required list and the excused
list are both projections of one `in_unit` field, so a set difference
between them cannot disagree — there is no second copy to drift. That is
the difference between checking a duplicate and not having one.

**The amendment history is deleted, not migrated.** It was the sixth
list, its failure mode is forgetting to append, and it committed that
failure twice — once in the row that records the omission. `git log
--oneline -- docs/plan/` is the same log and cannot forget.

**PA42 — BV22, and it is BV18's direction a third time.** The done check
matched any 3-or-4-cell row starting `| **Pnn** |` anywhere in the file,
so a blank criterion passed and a row planted in an unrelated table
passed. Both failed toward *has a definition of done*. **Making the
criteria a field removes the parser and the hole together** — there is
no longer a document to scan.

The generator now validates the source: empty `done_when`, empty `size`,
`excused` with no reason, `long` latency with no reason, and a
`blocks_start` naming a nonexistent id all fail.

**One defect found in my own generator while testing it, and it is worth
recording because it is the same family.** A missing field was reported
by the validator and then *raised out of the formatter three frames
down* — the run crashed rather than failing. A generator that crashes
instead of reporting fails in the wrong direction. It now bails before
rendering. **I found this by mutating, not by reading**, which is the
check that was missing on both sides this round.

Verified with a control: unmutated → exit 0; blank criterion, excused
without reason, missing size, nonexistent dependency, and a hand-edited
generated block → exit 1 each.

---

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

> **Read this before the claim below. `23 external bindings` is the
> retired population, and P20 owns the restatement.** ADR-004 retires
> `23 bind / 10 write of 33` as unrecoverable and replaces it with its
> generated worklist. The marker sits **above** the claim rather than
> after it because this passage is under *Claim proposed* — a reader
> arriving here takes the figure as the live population of a claim being
> made, which is the site most likely to be read as current. Marked
> 2026-08-04; figure untouched, because a marker is not a retraction and
> the eight censused sites go in one pass. `claims.md` T4a's Evidence
> already carries the register-side note.

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
