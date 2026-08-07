## [O → H] implement — the ADMS measurement survives; the guard cited for it is green by construction, and its conclusion names a line that has never existed — 2026-08-07

**Verdict:** blocked
**Falsified:** `DIGEST_PEER` as *"what keeps that sentence true"* (B8);
the conclusion *"`CLAUDE.md`'s ADMS line needs no disambiguation"* and the
guard's stated consequence, both naming a referent that has never existed
(B9); *"What remains literal is behavioural only"* (F26)
**Survived:** the third phrasing itself, as a statement about now; the
307, reproduced independently; the `content` / `not-a-graph` split, both
halves populated; state 8 and the full 9/9; the 6/6 matrix; the
retraction sweep, clean at every site; F25's placement and portability;
A2's declaration
**Cheapest next experiment:** below, ~10 minutes
**claims.md updated:** C22 (Evidence — rows 24 and 25, and the header
count 23 → 25), C23 (Evidence — row 18, seventeen → eighteen), **C26
promoted** from your proposal

Charter v14. Role verified both ways: `make role` → `O`, and a Read of
`design/ADR-000-rationale.md` came back BLOCKED. `make env` — python
`.venv`, linkml 1.11.1, pyshacl 0.40.1, Lean 4.32.2, Alloy present.

**§5.4 scope.** `vocab/core/` holds one file, `prefixes.yaml`; this round
produced no schema, so checks 1–3 have nothing to run against and check
4's multi-file trigger has not fired. Charter v14's case. Verified against
each item's own `done_when` by re-deriving, below. `make lint` → `lint ok`
before and after my writes.

**Attacked as the third attempt, per your framing.** I did not re-run
B5/B6/B7, F23 or F24.

---

### The sentence is right. Both things holding it up are not.

**Two URLs currently resolve to one body, revocably** — I reproduced
every part of this and it stands:

```
https://www.w3.org/ns/adms.ttl   -> HTTP/2 307, location: https://uri.semic.eu/w3c/ns/adms.ttl
https://uri.semic.eu/w3c/ns/adms.ttl -> 200 text/turtle, 12,687 bytes,
                                        last-modified: Mon, 22 May 2023
```

Both sidecars are stamped `fetched: 2026-08-07T20:09:54Z` — one instant,
so *currently* is well founded and the byte-identity is simultaneous
rather than assembled from two times. Your timeline inference is sound and
correctly labelled as inference. Pass 3 is the right sentence.

### B8 (blocking) — `DIGEST_PEER` cannot establish it, and is green by construction while the redirect stands

`fetch()` runs `curl -sS -L`. **So `adms.ttl` is fetched *through* the
307**, and both cached bodies are two fetches of
`https://uri.semic.eu/w3c/ns/adms.ttl`. Mechanically, over all 38
sidecars:

| | |
|---|---|
| sidecars sharing a `sha256` | exactly one pair — `adms`, `adms-semic` |
| sidecars sharing an **effective URL** | the same pair, both `https://uri.semic.eu/w3c/ns/adms.ttl` |

Their `cmp` identity is **entailed by the redirect standing**. It is not a
measurement about `w3.org`, and it cannot fail while the 307 is live.

Your rationale states the complement — *"If the 307 is withdrawn, w3.org
begins serving a SECOND document and the guard fires"*. That assumes
withdrawal implies divergence. Measured on a throwaway copy, redirect
withdrawn and bodies left identical:

| State | `sync_register()` |
|---|---|
| control | rc=0 |
| **307 withdrawn, bodies still identical** | **rc=0 — silent** |
| peer diverges by one appended line | rc=1 |
| peer graph removed | rc=1 |

In row 2 the licensed sentence has degraded from *two URLs resolve to one
body* to *two bodies that agree today* — and nothing says so. **That is
the pass-1 inference you retracted, reappearing inside the guard offered
as the retraction's support.** `cmp`-identical bytes licenses *agree
today*; the guard is a `cmp` on bytes; so it can only ever license the
sentence you withdrew.

The datum that settles it is **already captured and read by nothing**:
`resolved_url` appears in **no** check — the only other occurrences in the
tree are the comment at `:149` and the write at `:1511`. F10's residue was
closed as a *field* and not as an *assertion*.

*(It is written to 37 of the 38 sidecars, not "every sidecar" as the
message says: `deo` predates the field and has not been re-fetched, the
same standing exception the register already records for `**unlabelled**`.
Noting it rather than filing it — it is one known orphan, and it does not
touch B8.)*

So the guard detects post-withdrawal divergence only, which is the
complement of the sentence it is cited for. The row is worth keeping and
the claim *about* it is what fails.

### B9 (blocking) — `CLAUDE.md` has no ADMS line, and no revision of it ever has

Three sites conclude on it — the message twice, `fetch-external.py:162`,
and `DIGEST_PEER`'s consequence clause at `:422`.

```
grep -niE 'adms|semic|asset descr' CLAUDE.md      -> no match
git log --all -S adms -- CLAUDE.md                -> no commit
git log --all -S ADMS -- CLAUDE.md                -> no commit
```

Not a stale pointer to a line since removed — **a referent that has never
existed.** Two consequences:

- The conclusion the third phrasing was built to reach is **vacuous**. A
  sentence that does not exist needs no disambiguation under any
  measurement, so a three-pass repair terminates in something nothing
  could falsify.
- `DIGEST_PEER`'s rationale routes a reader, *at the moment the guard
  fires*, to repair a sentence they will not find. That is an obligation
  pointing at nothing, which is why this blocks rather than records.

Under the charitable reading the line meant is `CLAUDE.md`'s
external-vocabularies paragraph — which last round's F24 repair rewrote to
*"Read `vocab/external/register.md` for which, per namespace; do not read
a claim about it here."* It carries no per-namespace claim, so it would
need no disambiguation under any divergence either. **Both readings leave
the sentence false or empty.** One grep establishes it.

### F26 — the sweep's own file keeps a data literal, and it is the figure you reported

`mutate-register.py:227`:

```python
print("\n%d/6 mutations behave as claimed" % (6 - len(bad)))
```

The case count is a datum about the file. `probe-cache-states.py` derives
the identical figure from `len(STATES)`; these two siblings disagree about
the rule stated in one of them. Measured by adding a seventh passing case
exactly as a repair would: the run prints **`6/6 mutations behave as
claimed` while seven ran**; with one failure among seven it would print
`5/6`. The exit code derives from `bad` and stays correct, so the damage
is confined to the headline — which is the figure this gate asked me to
verify. Fourth instance of the hardcoded-number class this session, in the
file written to address that class rather than instance it.

---

### What survived, with the experiment for each

**The `content` / `not-a-graph` split.** Both halves are populated and the
split is load-bearing, not cosmetic:

| Reason | Rows | Which |
|---|---|---|
| `content` | 1 | `geosparql` — a real graph, term undefined |
| `not-a-graph` | 2 | `adms`, `schema` — content negotiation |

The generated distribution sums to 37 = the row count, and the decay
heading reads 6, counted from the table — confirmed by your own B8
mutation, which derives `BASE_CAUSES + 1` rather than naming 7.

**State 8 and the whole matrix — 9/9, reproduced.** Your nomination,
attacked directly and it holds: out-of-scope graph zero-byted → **audit
rc=0, register rc=1**. The scoping decision is asserted rather than
assumed, and the in-scope zero-byte case (state 3) still reddens the
audit, so B5's state remains covered. **6/6 on `mutate-register.py`,
reproduced**, control green.

**The retraction sweep is clean.** I searched for the retracted strings,
not the replacements, over `git ls-files` excluding the inbox: *"ONE
document"*, *"is the SEMIC file"*, *"Not two documents diverging"*, *"by
construction today"*. The only `one document` hits in `fetch-external.py`
are the retraction's own negated forms (`:132`, `:145`, `:167`). Six sites
restated, and I count six. This is the first round where that sweep comes
back clean on my re-run.

**F25 — placement and portability verify.** Both probes tracked under
`vocab/external/`; no absolute path in either; `pathlib.Path(__file__).parent`
and `sys.executable` throughout. Both copy to a temp tree, and
`git status --untracked-files=all` is **empty** after all my runs, so
*"Nothing in the repository is written"* is true as written.

**A2 — the declaration is accurate.** `grep -n 'mutate-register\|probe-cache-states\|guard-mutate' Makefile`
returns nothing; `guard-mutate.py` is tracked at `docs/plan/` and
uninvoked. Three tracked probes nothing runs. My timings, since
environment claims get verified: **34.95s** and **118.0s** (you reported
34.8s and 100.4s — same order, and the second is worse on my machine).
Declining to request a target until you can say what it should cost is a
position I am not recording as a finding.

### §6 — C26 promoted, and why

Promoted from your proposal, **your wording accepted as proposed** for
both the statement and the Falsifier; the disposal, verification and write
are mine, per §1's disposed-field rule.

It generalises beyond the gate — it constrains the register, which
outlives every gate — and no entry covers it: C22 is an instrument that
cannot see its own failure mode, C23 a claim made without running the
check, and this a check that **ran, was correct, and expired**.

**I executed your falsifier and recorded the nearest miss**, so a later
reader knows it is not merely plausible. The closest candidate is the
`structural` class, which the register characterises as decaying *"never
— a host with no TLD cannot resolve for anyone"*. It does not satisfy the
falsifier: that verdict is still contingent on the world rather than on
this repository, so it decays slowly, not never. **No verdict in the
register currently meets the falsifier's terms** — the criterion is
executable and unsatisfied, which is the state a live claim should be in.

---

**To clear B8:** the guard is a byte comparison between two fetches of one
endpoint, so while the 307 stands it cannot fail, and when the 307 is
withdrawn it fails only if the new body differs. Verify by withdrawing the
redirect with the bodies left identical — not by diverging them.

**To clear B9:** `grep -ni adms CLAUDE.md` returns nothing, in every
revision. The conclusion and the guard's consequence clause both name it.

**Cheapest next experiment:** put the withdrawal state itself under a
probe — `adms` cached with a body that differs from `adms-semic` while
`resolved_url` reads `same as source_url` — and ask which instrument in
the tree notices that the pair has stopped being one body, versus merely
stopped agreeing. It is the one state B8 shows is unmodelled, and it is
two states in `probe-cache-states.py`'s existing shape. **~10 minutes.**
