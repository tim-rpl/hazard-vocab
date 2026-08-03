# ADR-003 — Whether Part 2 and Part 3 are separate parts

**Status:** accepted — **option B**
**Date:** 2026-08-02

## Context

Parts 2 (Observation) and 3 (Model) exist as separate parts. This
contradicts the standard the vocabulary binds to.

**ISO 19156 / OGC OMS treats a simulation result as an `Observation`
with a simulation-typed procedure.** Measurement and forecast are the
same class, distinguished by `procedure`. SOSA/SSN follows the same
pattern. We made the opposite choice and have not defended it in
writing.

This must be settled before Part 2 vocabulary is authored, because it
determines Part 2's shape and every consumer's query surface.

## Two findings from the measure pass

Both verified by fetch-and-grep. They move the argument in opposite
directions and the second is the stronger.

**OMS has no bindable RDF at that URI.** `http://www.opengis.net/ont/om`
returns 288 bytes — a Prez profile stub — with zero occurrences of
`resultQuality`. The ISO TC211 URI 404s. So option B does not align
with a *vocabulary*; it aligns with a *document*. The interoperability
argument stated above is weaker than it reads. (The term the model
needs turned out to be `ssn-system:qualityOfObservation`, which is in
neither of the places either party expected, and which declares no
domain and no range.)

**SOSA's own definition of `Sensor` covers device, agent including
humans, and software including simulation.** That is the OMS position
sitting inside the definition of a class we would bind to — in a
vocabulary that *does* dereference. This argues for option B from
inside the artifact rather than from the paper standard, and it is the
strongest evidence currently available on this question.

## Options

| Option | Shape | Cost |
|---|---|---|
| **A — separate parts (current)** | Part 2 and Part 3 are distinct modules with distinct classes | Every "all readings regardless of provenance" query becomes a union across parts. Paid by every consumer, forever |
| **B — OMS-native** | One `Observation` class; `procedure` carries the distinction; a **required** epistemic-kind slot with a closed vocabulary; a lint forbidding omission | Distinction is a property, not structure — enforceable by validation but not by module boundary |

## The argument for A, and its weakening

A was chosen so the observed/modelled distinction would be
*structural* rather than a property, and therefore enforceable rather
than conventional. The enforcement mechanism was stratification: no
stratum-0 predicate derivable from a stratum-1 body.

That argument has since been weakened on its own terms (see `claims.md`
L6):

- It constrains **derivation only, not presentation**. It does not stop
  a forecast being rendered in an observation-styled card, which is the
  product property that actually matters.
- The stratum assignment is a judgment call at exactly the boundary
  cases that matter: QC'd and gap-filled monitor readings, data
  assimilation, and interpolated contours that EPA publishes as
  observational products. A compiler check on a wrongly-drawn boundary
  yields false confidence rather than safety.

Option B gets the labelling discipline through a required slot and a
closed vocabulary, without the query cost — and a required slot cannot
be omitted any more than a module boundary can be crossed.

> **WITHDRAWN 2026-08-02.** The final clause is true and answers the
> wrong question: a required slot catches **omission**, not
> **misassignment**. See *The enforcement argument, withdrawn* below.
> Retained because this is the Context section, which records what was
> believed before the decision.

## Decision

**Option B. Parts 2 and 3 merge into one `Observation` class,
distinguished by `procedure` and by a required `epistemicKind` slot with
a closed vocabulary.** Part 3 becomes a documented vacancy rather than
being renumbered.

### Why, against this ADR's own bar

The bar this ADR set for itself: *"if the reason A is better cannot be
articulated beyond 'the distinction feels more important as structure,'
the split is not load-bearing and B should win on interoperability
alone."*

> **WITHDRAWN 2026-08-02, and the withdrawal is the point.** This read:
> *"Five gates have passed and nobody has articulated it — not H, not O,
> not the falsification sweep. That alone settles it under the stated
> rule."*
>
> **The bar's antecedent is false.** *What B loses*, below in this same
> file, articulates exactly the reason A is better: a module boundary is
> checkable by reading a file tree, a required slot only by running
> validation. It is well past the disqualified phrase *"the distinction
> feels more important as structure"*. So the bar does not fire and
> *"that alone settles it"* does not follow.
>
> **The decision stands on the evidence table below**, which is
> independent of the bar: **A29, A5, T4 and A7**. A5 and T4 in
> particular make option A *not executable as scoped*, which is forced
> by the payloads rather than chosen.

The evidence accumulated since is one-directional:

| Finding | Bears on |
|---|---|
| **A29 / S8** — SOSA's own `sosa:Sensor` definition reads *"Device, agent (including humans), or **software (simulation)**"*, verified verbatim at `sosa.ttl:154` | The standard we bind classes a simulation as a sensor. A is fighting the vocabulary it imports, not only the one it cites |
| **A5**, survived under experiment | Under A this unit is **not executable as scoped** — Open-Meteo publishes no instrument (S10 probed for one and found none), so it has no Part 2 shape |
| **T4**, falsified by experiment | `sosa:madeBySensor`'s cardinality differs by outcome. Under B it *cannot* be required; under A it can. The A/B choice is forced by the payloads, not chosen |
| **A7** | B costs **+1 slot and +1 enum**. A costs a Part 3 that re-declares the observation shape, plus a union query on every consumer, forever |
| **L6**, weakened on its own terms | Stratification constrains *derivation only, not presentation*, and the stratum assignment is a judgment call at exactly the boundary cases — QC'd and gap-filled readings, data assimilation, EPA's interpolated contours published as observational products |

### The enforcement argument, withdrawn

This section read: *"The one argument that would have favoured A is the
one that fails. A was chosen so the observed/modelled distinction would
be structural and therefore enforceable. L6 shows the enforcement covers
derivation and not presentation; and a **required slot with a closed
vocabulary cannot be omitted any more than a module boundary can be
crossed.** B gets the discipline without the query cost."*

**WITHDRAWN 2026-08-02.** The L6 half stands. The clause in bold is true
and answers a question nobody asked.

**A required slot catches omission. It does not catch misassignment.**
A forecast declared `epistemicKind: observed` is a well-formed instance
and validates clean. Misassignment is precisely what *What B loses*
attributes to A as A's advantage — so this sentence answered a failure
mode nobody raised while leaving the raised one untouched.

**What would catch it is a cross-slot constraint between `epistemicKind`
and `procedure`, and ADR-005 — accepted in the same message as this
decision — establishes that such a constraint is not generable from
LinkML.** This ADR discharged by validation what its sibling says
validation cannot do.

**B still stands, on A29, A5 and A7 — three, not four.** An earlier
draft listed **T4**, and T4 does not discriminate between the options:
its own evidence row above reads *"Under B it cannot be required; under
A it can"*, and `claims.md` agrees. **T4's falsification establishes
that the A/B choice cannot be deferred, not which choice to make.**
`A5` alone carries A's inexecutability. Corrected 2026-08-02.

The three that remain are independent of this argument and of the
bar. What does not stand is the claim that
option B *enforces* what option A's module boundary enforced. It does
not, and the Obligation section records that as a permanent gap rather
than a discharged obligation.

### What B loses, stated rather than assumed away

**A module boundary is checkable by a human reading a file tree; a
required slot is checkable only by running validation.** Under A, a
Part 3 fact in a Part 2 file is visible on inspection. Under B, an
`epistemicKind` of the wrong value is visible only to **instance
validation** — `make check`, not `make lint`. An earlier draft named the
lint here; that was wrong twice over. `make lint` reads schema files and
has never inspected an instance, and `make check` **always could** —
so the instrument was never the missing piece. **What is missing is the
cross-slot constraint between `epistemicKind` and `procedure`, which is
ADR-005's P19.** Corrected 2026-08-02. That is
a real reduction in inspectability and it is the price.

**There is no mitigation, and an earlier draft claimed one.** It read:
*"The mitigation is the lint rule this ADR already required."* `make
lint` reads schema files and has never inspected an instance, so it
could not have been the mitigation for an instance-level property. The
required-slot lint catches omission, which is not this.

Instance validation is `make check`, which exists and always could run —
what it lacks is the constraint. Until that constraint exists,
**misassignment is caught by review or not at all.**

### Note on the interoperability argument, which is weaker than it reads

**OMS publishes no dereferenceable ontology** — `http://www.opengis.net/ont/om`
returns a 288-byte Prez stub with zero occurrences of `resultQuality`,
and the ISO TC211 URI 404s (A24). So "interoperate with ISO 19156" is
not a binding relationship; it is a shape we are borrowing.

**SOSA does dereference, and SOSA follows the same pattern.** That is
the interoperability argument that survives, and it is the one this
decision rests on.

## Obligation

Option B was chosen, so the conditional branch is discharged. What
remains, all of it required:

- **`epistemicKind` is a required slot with a closed vocabulary**, and a
  lint rule forbids its omission. The module boundary is gone; the slot
  is what replaces it, and an unenforced required slot would leave the
  distinction carried by nothing.
- **Parts 2 and 3 merge.** Part 3 is a **documented vacancy**, not
  renumbered — renumbering would break every reference in `claims.md`,
  `docs/coverage.md` and five gate messages to buy tidiness.
- **Propagation, done in the deciding pass rather than deferred:**
  `docs/coverage.md`'s five Part 3 rows now read
  `Part 2, epistemicKind: modelled`; ADR-002's modality table is
  amended; `README.md` is the human's and the change is reported there
  rather than made.
- **A claim for the property the module boundary used to carry, filed
  as an open gap rather than a discharged obligation.** Proposed: *no
  instance carries an `epistemicKind` inconsistent with its
  `procedure`.* Falsifier: one that does.

  **Nothing enforces this today, and nothing is scheduled to.**
  Corrected 2026-08-02, twice over — this paragraph survived both
  commits that exist to retract it, because each searched for the text
  it had written rather than the text it was retracting.

  - It read *"no instrument in this repository inspects an instance."*
    **`make check` does, and always could.** `make lint` reads schema
    files and was never a candidate. The instrument is not what is
    missing.
  - It read *"Until P19."* **ADR-005 no longer supports that**, and a
    measurement makes it sharply false: every affirmative result behind
    ADR-005 is `sh:equals`, misassignment is a **conditional**, and
    `rules:` and `annotations:` carrying one both emit `sh:condition`,
    `sh:sparql` and `sh:equals` **zero times**, exit 0, empty stderr.

  **Misassignment is unenforced indefinitely.** P19 is a candidate
  remedy whose third obligation — a conditional emitted and firing — is
  unmet and may be unmeetable. Until it is met, misassignment is caught
  by review or not at all, and that is **the price of option B rather
  than a temporary state.**

- **The boundary cases are inherited, not resolved.** ADR-003 cited
  QC'd and gap-filled readings, data assimilation, and interpolated
  contours published as observational products as evidence against A's
  enforceability. **Option B does not answer them either** — it forces a
  value where A at least made the difficulty visible as a filing
  decision. `docs/coverage.md`'s gap-filling row moved to `GAP` on
  2026-08-02 for this reason. **Whichever ADR gives `epistemicKind` its
  permissible values must adjudicate them**, and that ADR does not exist
  yet.

- **Curated narrative content has no carrier.** `epistemicKind ∈
  {observed, modelled}` and a written narrative is neither. This is not
  a defect in ADR-003 — C10 already records the question as
  underdetermined — but the closed vocabulary makes it a decision that
  must be taken rather than an absence that can be tolerated.

## Consequences

Either way, the modality axis from ADR-002 survives — four modalities
are a property of statements, not of module boundaries. B relocates
where that property is carried, not whether it exists.