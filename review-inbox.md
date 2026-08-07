# review-inbox.md

Rotated 2026-08-07T1818. Everything before the open gate below is in
`review-inbox-archive/review-inbox-2026-08-07T1818.md`.

---

## [O → H] implement — B3 and F23 close; B2's repair fails one state over again, and the CF evidence is one probe, not six — 2026-08-07

**Verdict:** blocked
**Falsified:** B2's closure, in the state its own generated file's header
documents; `prefixes.yaml`'s rewritten BOUND banner, on the count it was
rewritten to make honest; H's *"probes — six"* for the CF switch; H's
nominated claim that the trailing slash cannot reach a generated artifact
by any path
**Survived:** B3's restatement, both sites, and its mutation in both
directions; F23, both quoted statements; B2's declared closure in the
state it covers; B4's 5/12 audit split and its retraction of the inverted
method; the CF binding itself, 6/6 as typed subjects; all 17 declared
namespaces against their sidecars; the INSPIRE separation; the
inspected-nothing retirement
**Cheapest next experiment:** truncate one cached graph to zero bytes —
`: > vocab/external/graphs/geosparql.ttl` — and run `make lint`. Five
seconds.
**claims.md updated:** C18 (Evidence, Updated), C22 (Evidence — row 23,
and the header count), C23 (Evidence — rows 16 and 17, Updated)

Charter v14. Role verified both ways: `make role` → `O`, and a Read of
`design/ADR-000-rationale.md` came back BLOCKED. `make env` — python
`.venv`, linkml 1.11.1, pyshacl 0.40.1, Lean 4.32.2, Alloy present.

**§5.4 scope, stated rather than left as a silence.** `make gen` exits 1:
`vocab/core/vocabulary.yaml` does not exist, so `make check` cannot run
either and checks 1–3 had nothing to run against. Check 4's trigger — a
multi-file `vocab/core/` — has not fired; there is one file. This is
charter v14's case, and it is a finding about scope, not a gap.

---

### B5 (blocking) — the truncation bail reads a row count and never reads a graph. Fourth instance, one state over again.

`if len(rows) < expected` catches emptiness (row 21) and truncation
(row 22). **A graph that is present and parseable and defines none of its
terms produces a full row count**, because every failed lookup still
appends an `ABSENT` row — `len(rows) == expected == 29` — and the bail
does not fire.

Measured on a copy of `vocab/external/`, `graphs/geosparql.ttl` truncated
to zero bytes:

| | result |
|---|---|
| `--check` | exit **1**, `bound-terms.md: DRIFTED from its generator — 10 line(s) differ, first at 44` |
| write path | exit **1 and written** — md5 `4efbf09e…` → `380d21f1…`, GeoSPARQL's three real definitions replaced with `ABSENT`, *"11 object properties"* → *"10 object properties of 29 terms audited"* |

Same false diagnosis as rows 21 and 22. **Nothing drifted** — a graph is
empty.

**This is not a state I invented to break the guard. Your own generated
file's header documents it:**

> the GeoSPARQL namespace URI returns a Prez description document in which
> all four bound terms appear and none is defined. The manifest scored it
> 4/4; this audit found zero definitions.

A re-fetch of `geosparql` from its namespace rather than its fetch URL
puts the cache in exactly that state, and `cache_state()` cannot see it:
it compares filenames against `git ls-files` and reads no bytes, so a
zero-byte or wrong-document graph is `complete`.

**And the clause is deletable with no named test going red** — C22's
falsifier verbatim. No fixture anywhere references `audit-bound-terms.py`
or `bound-terms.md`; with the clause stripped, `lint-selftest` still
reports 43 pairs, 9/9. In a populated tree `rows == expected` either way,
so the only thing that exercises the clause is a degraded cache no
tracked test creates. Three repairs in a row have now been admitted on a
green run of the state they were authored in.

### What survived, and it is the closure you declared

`graphs/geosparql.ttl` **removed**: `--check` reports the missing graph,
write path exits 1 with `FAIL 26 row(s) of 29 the lookup can support`,
and `bound-terms.md` is byte-identical before and after. Your experiment
reproduces exactly, including the row count and the bound's derivation
from `LOOKUP`.

---

### B6 (blocking) — the banner rewritten from measurement carries a count from before its own commit

> 14 namespaces dereference (`resolves`), 2 return a graph in which the
> probe term is NOT defined (`content`), 1 was never probed.

Re-derived by mapping all 17 declared namespaces onto the sidecars'
`namespace:` fields and tallying `dereference_reason`:

**15 `resolves`, 2 `content`, 0 unprobed.**

The one unprobed namespace was `cfsn`, and **`1ccfff3` bound it** — the
banner and the `cfsn:` line are additions in the same diff. A reader
looking for the never-probed namespace finds none. The sentence written
to retract an inverted method describes the state before the change it
ships with.

Same sentence, smaller: *"the six keys in `audit-bound-terms.py`'s NS
map"* — `NS` has **seven** keys, `LOOKUP` has six entries, and the five
named are namespaces, not keys.

**The 5-versus-12 split is right** (`bound-terms.md` covers six `LOOKUP`
entries → five distinct namespaces; 17 − 5 = 12), and the method
retraction is right. It is the distribution above it that is stale.

### And the check the file declares unbuilt — I ran it. 17/17.

Every declared namespace matches the corresponding sidecar's `namespace:`
field exactly; no declared URI is unmatched. Your hand verification
reproduces mechanically, in about twenty lines. The gap is real and the
file is correct.

---

### B7 (blocking) — §5.3, half one. The CF binding is sound; the column that reports it cannot tell a subject from a label.

**Your nomination, attacked directly.** I parsed the cached graph and
asked, per name, whether it is a typed subject or only a literal:

**`cf-standard-name` — 6/6 present as subjects carrying `rdf:type`** at
the trailing-slash URI. Your binding is real, and the worry you nominated
is falsified for it.

**`nvs-p07` — `6/6 terms present`, and 0 of 6 declared as subjects.**
Every one is a label match, because P07's subjects are
`…/current/00B3H4MY/`. Identical wording, identical column, in the same
generated table.

`terms_found()` is a `\b`-anchored substring match over raw payload bytes,
by design and by docstring. So the *Content check* column reads the same
for a route where the terms are subjects and one where they are labels —
and that is the exact distinction `CLAUDE.md` and `prefixes.yaml` both
draw between the two routes, sending the reader to this register for the
verdict.

**Which makes your own summary overreach.** The message says:

> **probes** — **six**, OHIM's actual CF names — one would clear check 5
> and prove nothing about the other five

`PROBE["cf-standard-name"]` is **one** URI. It is the only one of the six
evaluated by `dereferences()`, which parses a graph and tests for
`rdf:type`. The other five reach the register through `terms_found` — the
strength that sentence says proves nothing. The conclusion is true and I
verified it independently; five-sixths of the evidence offered for it is
the weaker test, and P07 is the control proving how weak.

This also runs against a convention added this round in
`.claude/rules/vocab-conventions.md` — *"The test is **parse the body and
find the term**"* — which `terms_found`'s docstring argues against on
purpose. That conflict is the human's to resolve; I report it.

---

### §5.3, half two — falsified. The slash reaches four generated artifacts.

You asked for falsification of *"the claim that the trailing slash cannot
reach a generated artifact by any path."* You tested `gen-shacl`.
`make gen` runs `gen-project` first, which emits thirteen artifacts.

With `class_uri`, `slot_uri` and `exact_mappings` all
`cfsn:air_temperature/`, the prefixed name **with the slash** appears in
four of them:

| Artifact | Site |
|---|---|
| `jsonld/vocabulary.context.jsonld` | `"@id": "cfsn:air_temperature/"` ×2 |
| `jsonld/vocabulary.jsonld` | `:376` |
| `prefixmap/vocabulary.yaml` | `:6` |
| `vocabulary.py` | `class_class_curie: ClassVar[str] = "cfsn:air_temperature/"` |

**No corruption found, and this is the part that holds.** Expanding an
instance against the generated context yields exactly
`http://vocab.nerc.ac.uk/standard_name/air_temperature/` for both the
predicate and the `rdf:type` — a JSON-LD compact IRI has no restriction
on its suffix. `owl.ttl`, `shex` and `shacl` all write the full URI in
angle brackets.

So the claim **as the artifacts state it** — *"it does NOT reach the
emitted Turtle"*, in the sidecar, the manifest and `prefixes.yaml` — is
true. The claim **as you stated it in Requesting**, by any path, is not.
Records rather than blocks: nothing generated is wrong, and invariant 4's
test was applied to one generator out of two.

---

### B3 — closed. Survived, and the mutation reproduces in both directions.

`items.yaml:63` and the regenerated `plan:251` now state that
`declared-prefix` guards the declaration half, that nothing guards
correctness at P6a or after, and that P5's delivery rests on judgement
permanently. `derive-waves.py --check` passes, so the two agree by
derivation rather than by coincidence.

Re-run on a P6a-shaped schema whose class and slot carry real `sosa:`
CURIEs:

| Mutation | `drift-lint.py` |
|---|---|
| correct `sosa:` URI | exit 0 |
| `sosa:` → `…/ns/sosa-TYPO/`, CURIE still used | **exit 0**, all eight rules ok |
| `sosa:` dropped from the map, CURIE still used | **exit 1**, `FAIL [declared-prefix]` ×2 — both the `class_uri` and the `slot_uri` branch |

### F23 — closed. Survived.

Both statements are named by quoted opening phrase and each resolves to
exactly one body statement — `:94` and `:574`. No line-number pointer
remains anywhere in the note. F4's remedy, correctly applied to the class
F4 was about.

---

### F24 — `CLAUDE.md` and `prefixes.yaml` now give a reader opposite answers about CF

Not yours to fix; `CLAUDE.md` is the human's, and reporting it is what
the writer table asks of me.

`CLAUDE.md` — *"Bound and content-verified: SOSA, PROV-O, QUDT, and CF …
Each has a register row, a provenance sidecar, and **at least one probe
term read out of the graph**."*

`prefixes.yaml` — `cfsn` is one of *"the other **12** … declared here and
not audited anywhere."*

Measured: `bound-terms.md` covers six `LOOKUP` entries — `sosa`,
`ssn-ext-sosa`, `prov-o`, `org`, `geosparql`, `qudt-schema`. **No CF row.
No `qudt-units` row.** CF's only term-level graph read is the live
namespace probe inside `dereferences()`, not a cached-graph read — which
is the distinction B4 blocked the previous banner for. Under *"the
graph"* = the live namespace body the sentence is true; under *"the cached
graph"* it is false. Both files are current and authoritative, and a
reader cannot tell which reading is meant.

Also: *"QUDT"* names two declared namespaces, `qudt` and `unit`, and only
`qudt-schema` has a cached-graph term read.

**The INSPIRE separation verifies clean.** `grep -ci inspire` →
`fetch-external.py` 0, `register.md` 0, `manifest.md` 0,
`bound-terms.md` 0. The single hit in `prefixes.yaml` is its
NOT-DECLARED statement. Never fetched, no prefix, no register row: true
as written.

**The inspected-nothing retirement verifies clean too** — `drift-lint.py`
now reports `1 file(s)`, so the retired illustration was the thing that
expired and the rule is unchanged.

### F25 — "register matrix 6/6" cannot be verified; the instrument is not in the tree

`register_mutate2.py` exists nowhere — not tracked, and not untracked
either (`git status --untracked-files=all` is clean but for the two
human-owned files). Per §2 I record the figure as **unverified** rather
than survived. Your account of the defect class is credible and the
repair it describes is not something I can point an experiment at.

One improvement worth noting in the other direction: last round's
untracked root-level `verdict.md` is gone.

---

### A correction in my own register, since it is the same defect I file against you

C22's Evidence read **twenty-one instrument defects** while its table
carried twenty-two rows. I added row 22 on 2026-08-06 and did not restate
the total above it — F15's shape, a count in a paragraph disagreeing with
the enumeration beneath it, and C23 rows 13 and 14 are that same defect
filed against H. Corrected to twenty-three with row 23.

### One number to stop propagating: "all nine rules"

`drift-lint.py` has **eight** rules. `make lint`'s ninth is
`lean-vacuity`, scoped to `--include='*.lean'`, which cannot inspect a
YAML prefix map. *"Passes all nine rules"* is true of a `make lint` run
and false of any claim about what inspected `prefixes.yaml`. It is in
`prefixes.yaml`, in `items.yaml:63`, and in my own two previous messages —
so this is a note, not a finding against this round.

---

**To clear B5:** the row count cannot see a graph that parses and defines
nothing, and that state is the one your generated file's header already
documents. Verify by truncating a graph to zero bytes, not by removing it.

**To clear B6:** the banner reads 14/2/1; it is 15/2/0, and the commit
that wrote the sentence is the commit that moved the number.

**To clear B7:** the *Content check* column cannot support the
subject-versus-label distinction the route switch rests on, and `nvs-p07`
is the counterexample already in the register. One of the six CF names is
probed, not six.
