# Experiment 02 — probing the paraphrase sweep against its own failure mode

**Item:** design gate BV9 · **Source:** `[O → H]` block verification 9,
cheapest next experiment
**Run:** 2026-08-04 · **Status:** complete
**Measures:** the instrument proposed for `CLAUDE.md`'s verification
rule, and C22

**Why it was run.** The paraphrase sweep found `R2` on its first run, at
a site three string sweeps had passed clean. That is one green run over
the case its author had in mind — **C22 rows 12 and 13 exactly**, and
this project has now twice admitted an instrument on that evidence and
twice found it blind. An instrument is not evidence until it has been
probed against its own failure mode.

---

## Predictions, stated before running

- **P1 — a synonym-only restatement does NOT fire.** The sweep keys on
  content words that survive a paraphrase; a synonym restatement is
  exactly the case where none survives.
- **P2 — a restatement sharing one content word DOES fire**, or the
  instrument does nothing at all and R2 was luck.
- **P3 — if P1 holds, the instrument is a candidate C22 row**, and the
  rule proposed for `CLAUDE.md` must state its subject as the
  **proposition**, not as surviving content words.

## What was run

Four sentences planted one at a time into a scratch copy of
`design/ADR-003-observation-model-split.md`, each a restatement of the
withdrawn proposition *SOSA's shape is the reason to prefer option B*.
The sweep is the word list used verbatim at BV8 and BV9:

```
strongest|argues for|rests on|decisive|favou?rs|prefer|discriminat|reason for b
```

| Planted restatement | Result |
|---|---|
| *this is the footing the chosen shape stands on* (O's wording) | **MISSES** |
| *the unified-class route earns its place on that basis alone* | **MISSES** |
| *that is what option B rests on* — control | FIRES |
| *it remains the strongest case for the unified class* — control | FIRES |

**Synonym-only fired 0/2. Controls fired 2/2.**

## Result

**P1 held. P2 held. P3 therefore applies.**

**The paraphrase sweep is strictly better than a string sweep and has a
blind spot it cannot close.** It caught `R2` where three string sweeps
failed, and it cannot see a restatement that shares no content word.
Both are now measured rather than assumed.

**No word-list instrument closes this.** The subject of the defect is a
**proposition**; every grep-shaped instrument keys on **tokens**. That
gap is not a tuning problem — widening the word list until it catches
synonyms makes it fire on everything, and the two controls show the
list is already at the edge where `prefer` and `rests on` are ordinary
English.

## What follows

**1. The rule going to `CLAUDE.md` states its subject and its blind
spot.** A rule that reads *grep the surviving content words* would be
admitted on the same green that admitted the two instruments it
replaces.

**2. The remedy is structural, not instrumental.**
`design/ADR-template.md` already carries it: **state each ground once.**
A ground stated in one section and referenced from everywhere else
**cannot be restated**, so the defect has no site to occupy. That is the
generate-don't-transcribe move that closed the wave table, ADR-004's
counts and the fixtures README, applied to prose — and it is the only
thing in this project's history that has closed a defect class rather
than detected it.

The sweep detects; the template prevents. **P21's `done_when` requires
both**, and the template clause is the half that makes the sweep's blind
spot survivable.

**3. C22.** The instrument is a candidate row: admitted on one green run
over its author's own case, and now probed. It is **not** a row in the
sense the others are — those are instruments that were wrong. This one
is right within a stated subject and blind outside it. **The distinction
belongs in the entry if it is filed**, and whether a bounded instrument
counts is O's to dispose.

## Falsifier for this experiment

A synonym-only restatement of a withdrawn claim, sharing no content word
with it, that the word list above nevertheless fires on. That would mean
the miss was a property of my two sentences rather than of the
instrument, and P1 would not generalise.

**Not run, and named rather than left implicit:** two sentences are a
small sample, and both were written by the same person who wrote the
word list, which is the correlation most likely to produce a false miss.
A stronger version plants restatements written without sight of the word
list.
