# Design proofs

Properties of the identity and merge algebra. These constrain how the
Datalog in `transform/` is written.

**This package is never extracted to executable code** (CLAUDE.md
invariant 3). `design/` proves; `transform/` implements. Deleting this
directory must break nothing.

```
lake build
```

## Files

| File | Claims |
|---|---|
| `HazardVocab/Basic.lean` | Shared definitions — records, identifiers |
| `HazardVocab/Identity.lean` | L1, L2, L3 |
| `HazardVocab/Merge.lean` | T1, L4, L5 |

Every unproved statement carries `sorry`. A `sorry` here is the same
signal as `asserted` in `claims.md`: believed, not established. Do not
remove a `sorry` by weakening the statement.

**The absence of a `sorry` is not the signal for `tested`.** A theorem
whose conclusion is `True` elaborates with no warning of any kind and
states no proposition. Both files previously contained such theorems.
`make lint` now fails on the literal `: True :=` pattern, but a
conclusion can be weakened by other means and the lint will not catch
it — read what each theorem states. See `FALSIFIER.md` §4.

Current: 11 `sorry` declarations, 7 in `Identity.lean` and 4 in
`Merge.lean`. `monotone_under_source_addition` is the one theorem
genuinely proved, and it holds definitionally from its hypothesis —
stated so that any merge implementation must exhibit monotonicity
rather than assume it.

## The library name predates the rename, and stays

**`HazardVocab` is this library's Lake name, its directory and its module
namespace. It is not the project's name and it is not being changed.**
Recorded 2026-08-05, when the project became **OHIM — Operational Hazard
Information Model**.

**The decision, with the cost measured rather than estimated.**
`lakefile.toml` declares `HazardVocab` as both `name` and `lean_lib`, so
the directory must match it. A rename is the lakefile, the manifest, the
directory, four `.lean` files and their namespaces, and this README —
**plus seven citations elsewhere that are used as evidence rather than as
prose:**

| Citing file | Sites | What the citation is |
|---|---|---|
| `claims.md` | 6 | paths to theorem locations, cited as **evidence** for a claim's status |
| `design/ADR-001-identity-resolution.md` | 1 | a decision's supporting reference |
| `FALSIFIER.md` | 1 | §5.2 item 4's worked example, `Identity.lean` |

**Moving the files makes evidence stale**, and `claims.md` is O's while
`FALSIFIER.md` is the human's — so a rename here is a retraction pass on
the register under two other owners, not a substitution here.

**Against that: zero external consumers.** Nothing outside this
repository imports this library. `design/lean/` is never extracted to
executable code (invariant 3), so no generated artifact carries the name
either.

**If it is ever renamed, it is its own plan item**, and its `done_when`
names those eight citations explicitly. A rename folded into a
documentation pass is how a citation goes stale while every file involved
looks edited.
