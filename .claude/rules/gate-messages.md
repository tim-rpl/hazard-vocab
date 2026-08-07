---
paths: review-inbox.md
description: Message formats and rules for the H ↔ O gate protocol
---

# Gate message protocol

`review-inbox.md` is the shared channel between **H** (the OHIM builder) and **O** (Overseer, falsifier). Append only. Newest at the
bottom. Never rewrite an earlier message except when H amends its own
un-reviewed gate in place.

## Withdrawing a claim from a reviewed message

The no-rewrite rule is correct and it leaves the channel as the only
document here with no retraction mechanism. A closed document takes a
superseding note, a generated file regenerates, an ADR is superseded by
a numbered successor. **A reviewed inbox message can only be answered,
never marked** — so a withdrawn claim stays legible as an assertion at
its original site, and a reader arriving there has nothing pointing
forward.

That is the correct trade and it needs a stated remedy rather than an
assumption:

1. **A reviewed message is never marked, edited, or annotated.** Not
   even to say a claim in it was withdrawn. The record is what was
   written when it was written.
2. **The withdrawal lives in the withdrawing message**, and it
   **indexes every reached site by quoted opening phrase** — not by line
   number, which goes stale on the next edit including the one that
   writes it (F23). A withdrawal that names its own sites is findable
   from the retraction side; one that does not is findable from neither.
3. **Never assert that an unmarked earlier occurrence "stands as the
   record of a withdrawn claim."** It does not. It stands as an
   assertion, and saying otherwise is an unchecked claim inside a
   withdrawal — which has happened, inside a withdrawal of an unchecked
   claim.
4. **The retraction sweep searches the retracted string, not the
   replacement, and it excludes the inbox and its archive.** Hits there
   are history and are expected; hits anywhere else are live.

So the asymmetry is deliberate and bounded: **the channel is
append-only and therefore only ever findable forward.** Anything that
must be findable backward belongs in a document that supports
supersession — a claim in `claims.md`, a note in a closed document, or a
successor ADR.

H posts at every ARC gate and stops. O falsifies and posts back. H may
not pass a gate until O has replied, and must address every `blocked`
finding before proceeding.

## Gate

```
## [H → O] <stage> gate — <YYYY-MM-DD>
**Stage:** measure | plan | design | implement
**Artifacts:** <paths produced or changed>
**Claims touched:** <ids from claims.md, or none>
**Assertions:**
  A1. <a specific, checkable statement>
  A2. ...
**What would falsify each:**
  A1 — <the cheapest experiment that would break it>
**Requesting:** falsification of A1..An
```

```
## [O → H] <stage> gate — <YYYY-MM-DD>
**Verdict:** pass | pass-with-findings | blocked
**Falsified:** <assertion id, counterexample, evidence path>
**Unfalsifiable as stated:** <assertion id, why, how to restate>
**Survived:** <assertion ids, and the experiment each survived>
**Cheapest next experiment:** <one, with effort estimate>
**claims.md updated:** <ids whose status changed>
```

## Contest

H may contest a finding **once**, with evidence. O then withdraws or
holds. If O holds and H still disagrees, the human adjudicates and the
outcome is recorded here either way — including when O is overruled.

```
## [H → O] contest — <YYYY-MM-DD>
**Contesting:** <finding id from the [O → H] message>
**O said:** <one line, in O's words>
**Evidence against:** <what you ran, what it showed, paths>
**Requesting:** withdraw or hold
```

```
## [O → H] contest response — <YYYY-MM-DD>
**Finding:** <id>
**Resolution:** withdraw | hold
**Reasoning:** <what survives H's evidence, or what does not>
**claims.md updated:** <ids, if the withdrawal changes a status>
```

```
## [HUMAN] adjudication — <YYYY-MM-DD>
**Finding:** <id>
**Ruling:** uphold O | overrule O
**Reasoning:**
```

## Rules

- O does not propose improvements or alternative designs.
- O prefers the cheapest falsifier over the most rigorous one.
- "Unfalsifiable as stated" is a finding, not a pass.
- A `blocked` verdict names at least one assertion H must fix.
- `survived` requires an experiment O actually ran. Reading an
  assertion and finding it plausible is not evidence.
- H contests at most once per finding. A second contest is not a
  contest, it is a refusal.
- An overruled finding stays in the log. A governance record showing
  where the reviewer was wrong is worth more than one showing the
  reviewer was always right.