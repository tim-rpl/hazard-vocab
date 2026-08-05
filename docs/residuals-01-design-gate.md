# Residuals — design gate 01

**Opened:** 2026-08-04, at the design gate's close
**Owner:** H · **Cleared by:** plan item **P21**, in one pass
**Governing rule:** `FALSIFIER.md` §3.1 — inside a decided ADR, a defect
in the **rationale** records; a defect in the **decision** blocks.

**Scope, widened 2026-08-04.** Rationale defects found at the design
gate, **wherever they sit** — the original scoping to *inside a decided
ADR* was the shape of the first two entries, not a principle, and BV9-1
produced one in the plan. A defect that misleads a reader of the
reasoning is the same defect in `plan-01` as in `ADR-003`. What decides
whether an entry records or blocks is §3.1's test — can a reader take
the wrong option away — not which file it is in.

Sites outside H's write set are **filed here and not fixed**, with the
owner named.

Rationale defects found at the design gate and deliberately **not**
repaired one at a time. Each is real, each outlives the gate, and none
lets wrong work start — the decision beside it is unambiguous in every
artifact that consumes it.

**Why a list and not eight commits.** Eight rounds of this gate produced
eight partial passes, and a partial retraction is the defect three ADRs
carried in one round: withdrawn at one site, standing at another, with
the document disagreeing with itself and no reader able to tell which is
current. One pass, over a list that is written down, is the repair shape
this project has converged on — the same reason P20 exists for the
retired-figure residues.

**A marker is not a repair.** Where a site is marked below, the marker
tells a reader the passage is stale and names the owner. It does not
restate the claim. That is P21's work.

---

## Open

### R1 — `ADR-003:34-39` rules A29 discriminating, four sections after the ADR says nothing does

**Found:** BV8-1, 2026-08-04 · **Kind:** rationale · **Marked:** yes

*Two findings from the measure pass* reads:

> **SOSA's own definition of `Sensor` covers device, agent including
> humans, and software including simulation.** … **This argues for
> option B** … and **it is the strongest evidence currently available on
> this question.**

That is A29's content with a discriminating verdict. The same file says
three other things about the same fact:

| Site | Verdict on A29 |
|---|---|
| `:123`, evidence table third column | **permissive, not exclusive** — creates no objection to A |
| `:259` | **permissive** — removes an objection to B, creates none against A |
| `:262-263` | **what is missing is a reason for B rather than A, and this ADR does not contain one** |

`:39` and `:262` cannot both stand, and they are 220 lines apart.

**Why it records rather than blocks.** Option B is unambiguous in the
Decision section, in ADR-004, in ADR-005 and in every plan item that
rests on it. No reader can take the wrong option away, and no work
starts wrongly. What is damaged is a reader of the reasoning, who is
told at `:39` that the ADR holds the strongest evidence on a question it
later says it cannot answer.

**Repair at P21:** `:34-39` states A29's *observation* and references the
evidence table for its verdict. One ground, one site — `ADR-template.md`.

**Falsifier for this entry:** a fourth site in `ADR-003` giving A29 a
discriminating verdict, or any artifact outside `ADR-003` that reads
`:34-39` as authority for choosing B.

### R2 — `ADR-003:188-192` restates the claim BV7-3 withdrew, in H's own text, one round later

**Found:** 2026-08-04, by the paraphrase sweep proposed in this same
document · **Kind:** rationale · **Marked:** yes

*What the three legs establish* — written by H at BV6-5 — reads:

> **The ground that survives is the interoperability argument** … *SOSA
> dereferences and follows this pattern* … **That is what option B rests
> on.**

BV7-3 withdrew exactly that proposition at *Note on the interoperability
argument*, 40 lines below, and the repair did not reach this site.

**This is R1's defect with the authors swapped**, in the same file, on
the same day. A string sweep for the withdrawn wording — *"it is the one
this decision rests on"* — cannot see *"that is what option B rests
on."* Same proposition, no shared string.

**Records rather than blocks**, on the same reading as R1: option B is
unambiguous everywhere it is consumed, and what is damaged is a reader
of the reasoning.

**Repair at P21:** the section states the three legs' verdicts and
**stops**. What B rests on is stated once, in *Option B has no stated
ground that discriminates it from A*, which is the current answer.

**Falsifier for this entry:** any further site in `ADR-003` naming a
surviving ground for B, found by paraphrase rather than by string.

**Why this entry is the argument for the instrument.** It was found
inside the pass that proposed the instrument, in text written by the
person proposing it, one round after that text was itself a repair for
this defect class. Three string sweeps had passed over it clean.

---

## Standing method note — why the sweep missed it

The retracted-string sweep that cleared BV7-3 was **correct and complete
for the strings**. `it is the one this decision rests on` returns one
hit, inside its own retraction. **The claim was restated, not
repeated**, so no string carried it.

**The instrument that would have caught it**, proposed for `CLAUDE.md`'s
verification rule: *write the withdrawn claim in your own words without
reusing its wording, then grep the two or three content words that
survive the paraphrase.* A string sweep keys on the sentence; the defect
is a restated proposition.

Worked, on this case: the withdrawn claim paraphrases to *SOSA's shape
is the reason to prefer B*. The words surviving the paraphrase are
`SOSA`, `argues`, `strongest`, `rests`. `grep -n "strongest"
design/ADR-003*` returns `:39` on the first try.

---

## Filed, not H's to fix

### R4 — `CLAUDE.md` says ADR-003 is open; `ADR-003:3` says accepted

**Found:** BV9-1, 2026-08-04 · **Owner:** the human · **Kind:** rationale

> *"the Part 2 / Part 3 split is the one most likely to break first …
> **See ADR-003, which is open.**"*

`CLAUDE.md` is injected at the start of every session, which makes it
the most-read sentence in the project about ADR-003, and it contradicts
the ADR's status line. **Records rather than blocks on the same test
that cleared R1 and R2:** the ADR is one file away and unambiguous.

H reports rather than fixes — `CLAUDE.md` is the human's under the
ownership table.

**The surrounding claim is not affected and should survive the fix.**
*The Part 2 / Part 3 split is the one most likely to break first* is
**better supported now than when it was written**: ADR-003 records that
option B has no stated ground discriminating it from A.

### R5 — `FALSIFIER.md` §1's verification instruction is false by design

**Found:** BV9-2, 2026-08-04 · **Owner:** the human · **Kind:** rationale

§1: *"`make role` must print `O`, **or** a Read of any path under
`design/` must come back BLOCKED."* Charter v8 made every numbered ADR
readable, so the second disjunct now holds for exactly one path —
`ADR-000-rationale.md`. An O session using it as the check concludes it
is **unguarded when it is guarded.**

Second site, same finding: §1 gives O *Status, Evidence and Updated*
while §6's promotion necessarily writes a whole entry. That is why
BV9-3's field could not be written by O.

*Cosmetic, same area:* `guard_role.py`'s block message cites charter v8
against a charter at v11; the substance matches v11.

**Same class as R1 and R2** — a rule changed at v8, two sentences
derived from the old rule not reached — found in the charter, by the
role it constrains.

### R6 — the charter changed and its version did not

**Found:** 2026-08-04, verifying R5's fix · **Owner:** the human ·
**Kind:** decision-adjacent — see below

`FALSIFIER.md` changed 29 lines in the pass that closed R5, including
**§1's write set**, which now permits O to write *a complete new entry
when promoting under §6*. `**Charter version: 11**` and the version
table were not touched.

**That is the failure the header exists to detect.** Its own rule:
*"State the charter version in your first response. If it does not match
what the human expects, you are running on a stale copy."* Two O
sessions, one holding the copy from before this edit and one after, both
report **v11** and have **different write sets**. The check cannot
discriminate them.

**Same class as R1, R2 and BV9-2** — a rule changed and the statement
derived from it not reached — **fourth instance, third file, and this
one is inside the fix for the third.**

**Not filed as rationale.** A stale write set is what a role *does*, not
why. It records here only because `FALSIFIER.md` is the human's and H
cannot fix it; if it were H's it would block.

**Cheapest fix:** a `12` row — *§1 verification instruction corrected;
write set widened for §6 promotion* — and the header bumped.

### R7 — `CLAUDE.md` and `FALSIFIER.md` disagree about who files a `Falsifier`

**Found:** 2026-08-04 · **Owner:** the human · **Kind:** ownership

- `FALSIFIER.md` §1, as amended: *"do not add or edit a Falsifier on an
  entry H owns — **propose the wording and let H file it**."*
- `CLAUDE.md`'s ownership table: `claims.md` — writer **O**; H proposes
  new claims in gate messages.

The first says H writes `Falsifier` lines into `claims.md`; the second
says H does not write `claims.md` at all.

**Consequence, live right now:** BV9-3's field for C11–C17 is accepted
in substance by O, cannot be written by O under §1, and cannot be
written by H under `CLAUDE.md`. **It has no owner.** H is proposing the
wording and stopping there rather than resolving an ownership question
by inference — which is the *default deny* rule doing its job, and also
the reason the field is still not written.

---

## Cleared

### R3 — `plan-01:189` said ADR-003 is open. Withdrawn in place, 2026-08-04

**Found:** BV9-1 · **Kind:** rationale · **Cleared on sight, not at P21**

*"**ADR-003 is open and determines Part 2's shape.** Confirmed"* —
unmarked, in the document the implement stage reads. The item table at
`:227` and `:564` carries P3 as `MET`, so an item-by-item reader was
safe and a narrative reader was not.

**Why this one was not deferred**, on the precedent set at BV7-4 and
accepted: **a stale figure misleads about a quantity; a stale
open-question misleads about what is settled.** The second is the more
dangerous kind, the repair is one sentence with no ground to restate,
and nothing else in the passage depends on it. Deferring it would have
left the plan telling its own reader that a decided ADR is undecided for
the length of a pass.

**Verified:** `grep -rn "ADR-003 is open" docs/ design/` returns the
withdrawal record and nothing else.

*(P21 has not run. R1 and R2 remain open.)*
