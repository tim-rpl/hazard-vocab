# ADR-001 — Identity resolution strategy

**Status:** accepted — question 1 by prior art, question 2 as **option B**
**Date:** 2026-08-02

## Context

Source records arrive with partial identifier sets. Define
`ids(r) : Set (Scheme × Value)` and a match relation over records.

Two separable questions live here and were previously conflated:

1. **What shape does identity take?** — settled below by prior art.
2. **What establishes identity?** — the three-option fork, still open,
   and still gated on L2.

Claim L2 asserts that heuristic matching (normalised name plus rounded
centroid) is reflexive and symmetric but **not** transitive. See
`design/lean/HazardVocab/Identity.lean` — L2 may be false as filed,
because whether it holds depends on which matching rule is implemented,
and the two candidates fail differently. Settle that first; the
counterexample is what forces question 2.

## Options for question 2

| Option | What it means | Obligation |
|---|---|---|
| A — transitive closure | Union-find over the match graph | Over-merges. Must bound cluster size or diameter and prove the bound |
| B — authority only | Heuristic match never establishes identity, only *suggests* it | Free, given L1. Costs recall on records lacking authority IDs |
| C — policy clustering | Heuristic proposes, a resolution policy disposes | Must prove the policy is order-independent — not free |

## Prior art 1 — the reference implementation already does option B

From `docs/sources/HDC-data-source-register.html`, category 08: an
aircraft identity is built from the first field that actually exists —
ICAO hex, then alternative ICAO fields, then registration, then
callsign, then a position-derived fallback — and if none yield
anything, the aircraft is not rendered at all.

Precedence-ordered alias resolution with a declared authority order and
an explicit refusal in place of a guess. It is option B, implemented,
adopted after a real defect: rows with a blank identifier collapsed
onto one record, so the map could follow one aircraft while the panel
described another.

- Option B degrades gracefully on records lacking an authoritative
  identifier, which was the objection to it.
- The refusal case is what distinguishes B from A. A would have merged
  them.

Aircraft identity is simpler than incident identity — no complexes, no
mereology, no multi-agency republication — so this is evidence, not a
decision. But it is evidence from production rather than reasoning.

## Prior art 2 — the CIM Object Registry, and the shape it settles

Source: `docs/reference/ObjectRegistry_Profile_Specification_v2.1.pdf`
(ENTSO-E, SOC approved 2022-09-21; generated from IEC 61970 CIM17v40).

**This supersedes ADR-000 D3's alias structure.** D3 described a flat
tuple `{identifier, scheme, issuingAuthority, assertedTime}` and named
the CIM classes as a `Name`/`NameType`/`NameTypeAuthority` triple. Both
were wrong: the third class is `NamingAuthority`, and the decomposition
is four classes with a two-level authority relationship the flat tuple
cannot express.

### The structure

```
IdentifiedObject
  mRID          1..1   UUID per RFC 4122, issued by a model authority
  name          0..1   non-unique, human readable
  description   0..1
  aliasName     0..1   retained for backwards compatibility;
                       the profile recommends the Name class instead
  └─ Name       0..*
       name         1..1   free text used as a name OR an alternative identifier
       language     0..1   IETF BCP 47 tag
       mRID         0..1
       ├─ NameType          0..1   the scheme — first class, own mRID
       │    └─ NamingAuthority     authority owning the scheme
       └─ NamingAuthority   0..1   authority owning this specific name

ObjectType
  type          1..1   specialised type when serialised as a generalised class
```

### Four things it establishes

**1. Scheme and authority are first-class and separately owned.** A
`Name` and its `NameType` each associate to a `NamingAuthority`, and
they need not be the same one. Multi-agency republication — a perimeter
carrying an upstream identifier, republished by a different portal —
needs exactly that distinction.

**2. The profile distinguishes a label from an authoritative
identifier.** `Name.IdentifiedObject` is the object a name
*designates*; `Name.UniqueIdentifiedObject` is the object an
alternative identifier *uniquely* designates.

**Translate, don't transcribe.** Two association ends with the same
range and different semantics is a UML artifact — UML cannot say "this
relation has a kind," so it splits into two named ends. Declaratively
that is one relation with the kind as a slot:

```
alias(IdentifiedObject, Name, NameType, NamingAuthority,
      AliasKind, AssertedTime)
```

Exclusivity is then structural rather than a constraint: a tuple
carries one `AliasKind`, so there is nothing to populate twice and
nothing to enforce. This is ADR-002 Decision B applied one level down —
do not create two properties for two semantics; create one relation and
put the kind on it. ADR-000 D4 states the class-to-relation half of
this rule; the association-end-to-role-slot half is the same rule and
should be read into it.

**The binary kind is a degenerate case of what option B needs.**
Precedence is an *order* over schemes, not a flag — "authority scheme
first, heuristic second" generalises to a ranking. That order must be
**total**, because L4 makes merge a join only if conflict resolution is
a total order, and two aliases from different schemes designating
different entities is exactly that conflict.

**Decided 2026-08-02: precedence attaches to `NameType`, and T2 does
not protect it.** Filed as open at two places in this ADR after A32 had
answered it by measurement — scaffolding on a question with an answer.

`AliasKind` is a **type** distinction (does this name designate, or
uniquely designate), not a rank; ordering its two values is meaningless,
because a label does not establish identity at all and so is not low in
the order but outside it. Precedence is an order *between schemes*, and
the scheme is `NameType`. It lives as a `skos:OrderedCollection` in the
code list (A38), which SKOS carries natively and a LinkML enum cannot.

**T2 does not protect the ordering, and this is a checked negative
rather than a caveat.** `parts.als` models constraints as an unordered
set, so **reordering drops nothing** and the soundness assertions are
silent on it; SHACL Core cannot express prefix-extension over an
`rdf:List` without SPARQL; and **the conjunction of two total orders
from two composed profiles is a partial order in general** — T3,
falsified by counterexample. So L4's precondition is unestablished, and
**T3a's tiebreak is the open item** (plan item P11), not the attachment
point.

**3. `ObjectType` is role-not-subtype implemented.** It exists to carry
an object's specialised type when the instance is serialised using a
generalised class — the profile's own example is a Meter serialised as
an `EndDevice` with the type attribute naming it a Meter.

This is a candidate resolution to the SOSA / C7 conflict recorded in
ADR-002: an AirNow site is an `Asset` with `ObjectType` = Platform, its
monitor an `Asset` with `ObjectType` = Sensor. One entity type, role as
data, from a standard rather than from an OWL inference exploiting an
ambiguity. See ADR-002.

**4. CIM has no assertion time.** `Name` carries no temporal attribute.
`assertedTime` comes from PROV-O regardless of whether the rest binds —
and the profile's own §2.4 already binds PROV-O, Time Ontology, and
DCAT for its header metadata, constraining `prov:wasAttributedTo` to a
`prov:Agent`. Independent convergence on domain-standard-for-structure
plus W3C-for-provenance.

### One constraint adopted outright

`IdentifiedObject.name` is explicitly non-unique, must be human
readable, and **must not carry embedded information requiring
parsing**. Adopt this. It is the rule a name-normalising matcher would
have benefited from, and it bears on L2.

### Bind or copy — testable, not assumed

The Version IRI is `http://entsoe.eu/ns/CIM/ObjectRegistry-EU/2.1` —
an **ENTSO-E** namespace, not IEC. ENTSO-E publishes profiles freely,
so it may dereference where the IEC base model would not.

| Result | Action |
|---|---|
| Serves RDFS/OWL | Bind. Record the electricity-domain association the namespace carries and decide whether it is tolerable in a jurisdiction-neutral core |
| Serves a document only | Copy the structure, author locally, cite the profile as normative precedent |
| Does not resolve | As above, plus record that the RDFS is held locally and its provenance |

Verify with fetch-and-grep, not status codes.

## Decision

**Question 1 — settled.** Adopt the four-class decomposition rendered
as relations, with `AliasKind` carrying the label/identifier
distinction, plus `ObjectType` and `assertedTime` from PROV-O. Bind
versus copy pending the dereference test.

**Both halves of this are settled above, and this line filed them as
open inside the Decision section itself.** Corrected 2026-08-02.

- **Precedence attaches to `NameType`**, as a `skos:OrderedCollection`
  in the code list — decided above, and T2 does not protect the
  ordering.
- **`NameType` is a SKOS concept scheme, not a class** — A38, adopted
  in this ADR's structure section. Its content is identity plus label
  plus definition, its values are governed at profile level, and the
  sample instance is `EIC`, a scheme identifier.

Nothing within question 1 remains open.

**Question 2 — decided: B.** Heuristic matches are recorded as
`candidateMatch` facts, never as identity facts. Identity is established
only by an authority scheme, under the precedence order a profile
declares.

### Why B, and what L2's ambiguity costs the decision

L2 is ambiguous between two relations with **opposite truth values** —
grid-cell equality (transitive, so L2 is false) and tolerance proximity
(not transitive, so L2 is true). That ambiguity is not resolved here and
cannot be resolved from this repository (P12).

**It costs this decision nothing, and that is the argument for B.**

| Option | What L2's ambiguity does to it |
|---|---|
| **A** — transitive closure | **Decisive.** Under proximity, union-find over a non-transitive relation over-merges without bound, and the obligation is to prove a cluster bound nobody can state until the relation is known. Under grid-cell equality the closure is just the quotient and is safe. A cannot be chosen without resolving L2 |
| **C** — policy clustering | **Decisive.** The obligation is proving the policy order-independent, and whether that is provable depends on which relation it disposes over |
| **B** — authority only | **None.** The heuristic never establishes identity, so its algebraic properties are not load-bearing. B is *invariant* under the ambiguity |

**B is the only option whose correctness does not depend on a question
this project cannot currently answer.** That is a stronger reason than
the prior art, and it is the reason of record.

The prior art agrees and is worth keeping as corroboration rather than
as grounds: the reference implementation implements B, with an explicit
refusal in place of a guess (register category 08); and the CIM profile
states that `IdentifiedObject.name` is non-unique, is for user interface
and debugging, must not carry embedded information requiring parsing,
and that the mRID is the only unique and persistent identifier in the
exchange. **That profile does not dereference (A30, PA10), so it binds
nothing** — it is a second mature system reaching the same shape
independently, not an authority.

### What B costs, stated

**Recall.** Records carrying no authority identifier are never fused.
The reference implementation's aircraft case shows the shape: an entity
with no resolvable identifier is not rendered at all. Add a recall
metric to `claims.md`, per this ADR's own obligation.

### Consequence for `candidateMatch`

**It exists, and it is Part 0 schema rather than `transform/` content.**
Under B the heuristic still runs — it just produces a different kind of
fact. That fact relates two `Entity` instances and carries provenance,
so it needs a declared shape.

The rule that *derives* it is `transform/`. The relation it derives *to*
is Part 0. That is ADR-000 D4's three layers — signature, constraints,
derivation — with the boundary drawn where D4 draws it.

**So P6b is non-empty**, which resolves the ambiguity PA11 left open in
the direction PA11 flagged as possible but did not assume.

## Obligation

Option B was chosen, so the three-way branch is discharged. What remains:

- **A recall metric in `claims.md`.** B's stated cost is that records
  carrying no authority identifier are never fused. That cost must be
  measurable, not asserted. Proposed as a new claim when fixtures exist:
  *the proportion of source records carrying no resolvable authority
  identifier is X*, falsifiable by counting.
- **The no-embedded-information constraint on `name` becomes a lint
  rule.** Adopted from the CIM profile: `name` is for user interface and
  debugging, and must not carry information requiring parsing.
- **`candidateMatch` is authored in Part 0** (P6b), and its deriving
  rule in `transform/`.

**L2 is not an obligation of this ADR.** Question 2 was decided without
it and is invariant under it. L2 remains `asserted` and ambiguous, and
P12 — determining which relation the reference implementation
implements — remains permanently open. **Anyone reopening L2 should know
it no longer gates anything here.**

## Consequences

- **Part 0's class count does not change, and the alias structure stops
  being a flat tuple.** An earlier draft of this section read *"Part 0
  gains four classes rather than one"* — that is the **literal
  transcription** figure, and it contradicts the *translate, don't
  transcribe* rule stated two sections above it in this same file.
  A31 measures the translation as **the same class count plus two
  slots**: `NameType` becomes a SKOS code list and `NamingAuthority`
  becomes `Agent`, so neither is a new class. Corrected 2026-08-02;
  ADR-004 carries the authoritative counts. ADR-000 D3 is superseded on
  this point and left unedited.
- **Identity is never established heuristically.** A record with no
  authority identifier stands alone. Downstream, that is visible as a
  refusal rather than as a guess — the behaviour the reference
  implementation adopted after a real defect.
- **`candidateMatch` facts accumulate and are never deleted**, which
  keeps them queryable and auditable and puts them under L5's
  monotonicity rather than outside it.
- **Recall is the exposed flank.** If the metric shows most records lack
  an authority identifier, B is still correct and the *pipeline* has a
  coverage problem that no resolution strategy fixes. That is worth
  knowing early and is why the metric is an obligation.
