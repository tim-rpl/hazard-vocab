#!/usr/bin/env python3
"""Generate ADR-004's surface counts from design/surface.yaml.

Four block rounds, one quantity, five values, and every residue at a
decision or summary line while the correction sat in an analysis
section. That is the plan gate's defect — hand-maintained lists keyed by
an identifier — closed there by generating the views and deleting the
copies. This is the third instance of the class.

    derive-surface.py            print the blocks
    derive-surface.py --write    inject them into ADR-004
    derive-surface.py --check    exit 1 if stale or inconsistent

STATED LIMIT. This closes the *arithmetic* class only. It cannot catch a
prose claim about what a tool does — BV4-1 and BV4-2 were sentences
about lint behaviour, not figures, and generation would have missed both.
The answer to that class is O's: **the search key for a tooling change
is the tool's behaviour, not its name.**
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
DOC = HERE / "ADR-004-slot-carriers.md"
SRC = HERE / "surface.yaml"
BEGIN = "<!-- BEGIN GENERATED:%s - design/derive-surface.py. Edit surface.yaml, not this. -->"
END = "<!-- END GENERATED:%s -->"


def load():
    d = yaml.safe_load(SRC.read_text())
    e = []
    for k in ("slot_uri", "class_uri", "meaning_verified", "meaning_unverified",
              "local_slots", "removed_from_local", "not_enumerated_by_a1"):
        if k not in d:
            e.append("surface.yaml has no `%s`" % k)
    if e:
        return d, e
    # A term may not sit in two populations at once. This is the defect
    # that produced 17: one slot counted under two names.
    seen = {}
    for pop in ("slot_uri", "class_uri", "meaning_verified", "meaning_unverified"):
        for term in d[pop]:
            if term in seen:
                e.append("`%s` is in both %s and %s" % (term, seen[term], pop))
            seen[term] = pop
    for name in list(d["local_slots"]) + list(d["removed_from_local"]):
        if name in seen:
            e.append("`%s` is a local slot and also in %s" % (name, seen[name]))
    for name in d["not_enumerated_by_a1"]:
        if name in d["local_slots"]:
            e.append("`%s` is flagged not-enumerated-by-A1 and also counted "
                     "as one of A1's local slots — this is how 25 happened" % name)
    for name, reason in d["local_slots"].items():
        if not str(reason).strip():
            e.append("local slot `%s` has no reason" % name)
    return d, e


def render(d):
    nb, nl = len(d["slot_uri"]), len(d["local_slots"])
    b = {}
    b["partition"] = [
        "| Slot population | Count |", "|---|---|",
        "| Slots carrying an external `slot_uri` | **%d** |" % nb,
        "| Slots with no external term, defined locally | **%d** |" % nl,
        "| **Distinct total of A1's enumerated slots** | **%d** |" % (nb + nl),
        "",
        "**Removed from A1's local list by an accepted decision:**",
        "",
    ]
    for k, v in d["removed_from_local"].items():
        b["partition"].append("- `%s` — %s" % (k, v))
    b["partition"] += [
        "",
        "**Needed by this unit and NOT enumerated by A1** — reported "
        "separately and never counted in a row labelled *A1's enumerated "
        "slots*, which is exactly how the arithmetic looked closed at 25:",
        "",
    ]
    for k, v in d["not_enumerated_by_a1"].items():
        b["partition"].append("- `%s` — %s" % (k, v))

    b["populations"] = [
        "| Population | Count | Note |", "|---|---|---|",
        "| Classes carrying an external `class_uri` | %d | |" % len(d["class_uri"]),
        "| Permissible-value URIs, content-verified | %d | QUDT units |" % len(d["meaning_verified"]),
        "| Permissible-value URIs, **status-code only** | %d | NVS2 P07 — **verify before binding** |"
        % len(d["meaning_unverified"]),
        "",
        "**Never summed with slots.** A permissible value is not a schema "
        "element; a class is not a slot. Summing them is what produced "
        "`23`, `33` and every figure derived from them.",
    ]

    b["worklist"] = [
        "**What P5 works from — names, not a total:**", "",
        "- **%d bound slots:** %s" % (nb, ", ".join("`%s`" % s for s in d["slot_uri"])),
        "- **%d local slots:** %s" % (nl, ", ".join("`%s`" % s for s in d["local_slots"])),
        "- **%d class bindings:** %s" % (len(d["class_uri"]),
                                         ", ".join("`%s`" % s for s in d["class_uri"])),
        "- **%d value URIs verified**, **%d to verify first**"
        % (len(d["meaning_verified"]), len(d["meaning_unverified"])),
        "- **plus %s**, which A1 did not enumerate"
        % ", ".join("`%s`" % s for s in d["not_enumerated_by_a1"]),
    ]
    return b


def main():
    d, errs = load()
    if errs:
        print("FAIL\n  " + "\n  ".join(errs), file=sys.stderr)
        return 1
    blocks = render(d)
    text = DOC.read_text()

    if "--write" in sys.argv:
        for name, lines in blocks.items():
            beg, end = BEGIN % name, END % name
            if beg not in text or end not in text:
                print("no markers for %s" % name, file=sys.stderr)
                return 1
            i, j = text.index(beg), text.index(end)
            text = text[:i] + beg + "\n\n" + "\n".join(lines) + "\n\n" + text[j:]
        DOC.write_text(text)
        print("wrote %d blocks" % len(blocks), file=sys.stderr)
        return 0

    if "--check" not in sys.argv:
        for name, lines in blocks.items():
            print("--- %s ---\n%s\n" % (name, "\n".join(lines)))
        return 0

    # BV5-1: the generator's boundary was one paragraph too high. A
    # hand-typed restatement of the counts sat below END GENERATED and
    # nothing checked it. Proximity is the wrong test — a number near a
    # marker may be a date or a historical narrative — so this targets
    # the *shapes a restatement takes* instead.
    outside = text
    for name in blocks:
        beg, end = BEGIN % name, END % name
        if beg in outside and end in outside:
            i, j = outside.index(beg), outside.index(end) + len(end)
            outside = outside[:i] + outside[j:]
    # Fire only on the CURRENT generated values. An earlier version
    # matched any numeral in these shapes, which forbade the historical
    # record this project requires — "an earlier draft read 17 bound + 9
    # local" is a retraction, not a restatement, and every ADR here
    # carries one. Narrowing to live values lets the record stand.
    #
    # RESIDUAL, stated rather than claimed solved: a coincidental phrase
    # carrying a live value still fires — "16 bound volumes" would. No
    # pattern can separate that from a real restatement, so the check is
    # deliberately noisy in that one direction rather than silent.
    nb, nl = len(d["slot_uri"]), len(d["local_slots"])
    live = {r"%d\s+bound" % nb, r"%d\s+local" % nl,
            r"=\s*%d\s+of A1" % (nb + nl),
            r"%d\s+class bindings" % len(d["class_uri"]),
            r"%d\s+value URIs" % len(d["meaning_verified"])}
    restated = []
    for pat in live:
        for m in re.finditer(pat, outside):
            restated.append("a LIVE generated count is restated by hand "
                            "outside the blocks: %r" % m.group(0))
    if restated:
        print("FAIL\n  " + "\n  ".join(sorted(set(restated))), file=sys.stderr)
        return 1

    stale = []
    for name, lines in blocks.items():
        beg, end = BEGIN % name, END % name
        if beg not in text or end not in text:
            stale.append("%s: markers missing" % name)
            continue
        cur = text[text.index(beg) + len(beg):text.index(end)].strip()
        if cur != "\n".join(lines).strip():
            stale.append("%s: stale — run --write" % name)
    if stale:
        print("FAIL\n  " + "\n  ".join(stale), file=sys.stderr)
        return 1
    print("ok — %d bound + %d local = %d of A1's enumerated slots; "
          "%d not enumerated by A1" % (len(d["slot_uri"]), len(d["local_slots"]),
          len(d["slot_uri"]) + len(d["local_slots"]), len(d["not_enumerated_by_a1"])),
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
