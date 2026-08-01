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
