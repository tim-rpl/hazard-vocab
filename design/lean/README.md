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