# ADR-001 — Identity resolution strategy

**Status:** proposed — structure settled, relation BLOCKED pending L2
**Date:** —

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

Open: does precedence attach to `AliasKind` or to `NameType`? A profile
declares which schemes exist *and their ordering*, so T2 applies — a
profile may extend the order but never reorder what the base fixed.

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

Open within question 1: whether precedence attaches to `AliasKind` or
`NameType`, and whether `NameType` is a class or a SKOS concept scheme
(see ADR-000 D5).

**Question 2 — TBD.** Leaning B: heuristic matches recorded as
`candidateMatch` facts rather than identity facts. They stay in the
store, remain queryable and auditable, and never silently fuse two
distinct entities. Option A is what naive pipelines do implicitly,
without the bound.

## Obligation

- Resolve L2 first. The structure above is neutral between A, B, and C.
- If A: state and prove the cluster bound. New claim.
- If B: none beyond L1. Add a recall metric to `claims.md`.
- If C: prove policy order-independence. New claim, and the hardest of
  the three.
- Either way: the no-embedded-information constraint on `name` becomes
  a lint rule.

## Consequences

TBD for question 2. For question 1: Part 0 gains four classes rather
than one, and the alias structure stops being a flat tuple. ADR-000 D3
is superseded on this point and is left unedited, per the rule that
ADRs record what was believed when they were accepted.