#!/usr/bin/env python3
"""Generate every item-keyed view in the plan document from one source.

Four of the last five plan-gate blocks were one defect: **hand-maintained
lists keyed by item id, disagreeing with each other.**

    BV9   the wave view vs the item table
    BV17  the done table vs itself - two shapes, different column counts
    BV21  PA18's membership lists vs the item table
    BV24  PA17's ranking and the amendment history

Generating the wave view stopped it dead for one list and was never
applied to the rest. This applies it to all of them.

`items.yaml` is the source. Everything item-keyed in the document is a
view of it, injected between markers. The set differences BV21 was about
become structurally impossible rather than checked, because both sides
are projections of one field.

    derive-waves.py            print every block
    derive-waves.py --write    inject them into the document
    derive-waves.py --check    exit 1 if any block is stale

Ownership: generates content for a document H owns. If it belongs under
`scripts/` with its own target, that is the human's call.
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
DOC = HERE / "plan-01-part2-part0.md"
SRC = HERE / "items.yaml"

BEGIN = "<!-- BEGIN GENERATED:%s - docs/plan/derive-waves.py. Edit items.yaml, not this. -->"
END = "<!-- END GENERATED:%s -->"
EDGE_RE = re.compile(r"^P\d+[ab]?$")

FIELDS = ("item", "produces", "blocks_start", "blocks_trust",
          "done_when", "size", "in_unit", "latency")


def key(i):
    m = re.match(r"P(\d+)([ab]?)", i)
    return (int(m.group(1)), m.group(2))


def load():
    items = yaml.safe_load(SRC.read_text())["items"]
    e = []
    for i, f in items.items():
        for req in FIELDS:
            if req not in f:
                e.append("%s has no `%s`" % (i, req))
        # BV22: a blank criterion is not a criterion. The old parser
        # accepted one because it only checked that a row existed.
        if not str(f.get("done_when", "")).strip():
            e.append("%s has an empty `done_when`" % i)
        if not str(f.get("size", "")).strip():
            e.append("%s has an empty `size`" % i)
        if f.get("in_unit") not in ("required", "excused"):
            e.append("%s `in_unit` must be required|excused" % i)
        if f.get("in_unit") == "excused" and not f.get("excused_because"):
            e.append("%s is excused with no reason" % i)
        if f.get("latency") not in ("short", "long"):
            e.append("%s `latency` must be short|long" % i)
        if f.get("latency") == "long" and not f.get("latency_because"):
            e.append("%s is long-latency with no reason" % i)
    return items, e


def deps(field):
    out, prose = [], []
    for part in str(field).split(","):
        tok = part.strip().strip("*`— ")
        if not tok:
            continue
        (out if EDGE_RE.match(tok) else prose).append(tok)
    return out, prose


def levels(items):
    graph, unstartable = {}, {}
    for i, f in items.items():
        d, prose = deps(f["blocks_start"])
        if prose:
            unstartable[i] = prose
        else:
            graph[i] = d
    e = []
    for i, d in graph.items():
        for x in d:
            if x not in items:
                e.append("%s depends on %s, which is not an item" % (i, x))
    level, downstream, remaining = {}, {}, dict(graph)
    n = 0
    while remaining:
        for i, d in list(remaining.items()):
            bad = [x for x in d if x in unstartable or x in downstream]
            if bad:
                downstream[i] = bad
                del remaining[i]
        ready = [i for i, d in remaining.items() if all(x in level for x in d)]
        if not ready:
            break
        for i in ready:
            level[i] = n
            del remaining[i]
        n += 1
    return level, unstartable, downstream, remaining, e


def render(items):
    lv, unstart, down, cyc, errs = levels(items)
    ids = sorted(items, key=key)
    b = {}

    b["items"] = ["| # | Item | Produces | Blocks-start | Blocks-trust | In-unit | Notes |",
                  "|---|---|---|---|---|---|---|"]
    for i in ids:
        f = items[i]
        m = ("**required**" if f["in_unit"] == "required"
             else "excused — %s" % f["excused_because"])
        b["items"].append("| **%s** | %s | %s | %s | %s | %s | %s |" % (
            i, f["item"], f["produces"], f["blocks_start"],
            f["blocks_trust"], m, f["notes"]))

    b["waves"] = ["| Wave | Items |", "|---|---|"]
    for n in range(max(lv.values(), default=-1) + 1):
        mem = sorted((i for i, l in lv.items() if l == n), key=key)
        b["waves"].append("| **%d** | %s |" % (n + 1, ", ".join("**%s**" % m for m in mem)))
    for i in sorted(unstart, key=key):
        b["waves"].append("| **—** | **%s** — not startable here: %s |"
                          % (i, "; ".join(unstart[i])))
    for i in sorted(down, key=key):
        b["waves"].append("| **—** | **%s** — downstream of %s, not startable here |"
                          % (i, ", ".join(sorted(down[i], key=key))))
    if cyc:
        b["waves"].append("| **cycle** | %s |" % ", ".join(sorted(cyc, key=key)))

    b["done"] = ["| # | Done when | Size |", "|---|---|---|"]
    for i in ids:
        b["done"].append("| **%s** | %s | %s |" % (i, items[i]["done_when"], items[i]["size"]))

    w1 = sorted((i for i, l in lv.items() if l == 0), key=key)
    longs = [i for i in w1 if items[i]["latency"] == "long"]
    shorts = [i for i in w1 if items[i]["latency"] == "short"]
    b["latency"] = ["| Order | Item | Why here |", "|---|---|---|"]
    for n, i in enumerate(longs + shorts, 1):
        f = items[i]
        why = ("**long** — %s; start it so the wait runs alongside" % f["latency_because"]
               if f["latency"] == "long" else "short — fills the wait")
        b["latency"].append("| %d | **%s** | %s |" % (n, i, why))

    req = [i for i in ids if items[i]["in_unit"] == "required"]
    exc = [i for i in ids if items[i]["in_unit"] == "excused"]
    b["membership"] = ["**Plan 01 is done when these meet their criteria:** %s."
                       % ", ".join("**%s**" % i for i in req), "",
                       "**Excused, each with its reason:**", ""]
    for i in exc:
        b["membership"].append("- **%s** — %s" % (i, items[i]["excused_because"]))
    b["membership"] += ["", "*%d required, %d excused, %d items. Both lists are "
                        "projections of one field, so the set difference cannot "
                        "disagree (BV21).*" % (len(req), len(exc), len(ids))]
    return b, errs


def splice(text, name, body):
    beg, end = BEGIN % name, END % name
    if beg not in text or end not in text:
        return None
    i, j = text.index(beg), text.index(end)
    return text[:i] + beg + "\n\n" + body + "\n\n" + text[j:]



RETIRED_ENUMERATION = (
    "grep -ohE '(23|ten|10|24|33|32) [a-z]+( [a-z]+)?' docs/plan/ -r "
    "| sort | uniq -c | sort -rn")

# P20's guard. The phrasings are DERIVED, by the command above, run
# 2026-08-05 — not remembered. BV6-1 named four literal strings, covered
# three phrasings and missed two of the six that occur; BV7-4 then found
# two more that no noun-anchored pattern could see, because `the 23 —`
# ends in an em dash and `the 23 and` has no noun at all. So this anchors
# on the DETERMINER as well.
RETIRED_PHRASES = re.compile(
    r"\b23 (bind|bindings?|external terms|external identities|external bindings)\b"
    r"|\b(ten|10) local( terms)?\b|\b10 write of\b|\bthe 23\b|\bthe ten\b"
    r"|\b24 bind\b|\b23/10\b|\b23/9\b|\b24/9\b|\bof 32\b|\bof 33\b",
    re.IGNORECASE)   # B2: absent here while SIZING_PHRASES had it

# Sizing claims about an item. Subject B, added 2026-08-05: the census
# matches numerals and "P5 is the long pole" is not one.
SIZING_PHRASES = re.compile(
    r"\blong pole\b|\bL-sized\b|\bwidest item\b|\bstartable today\b", re.I)

# A retraction is allowed to name what it retracts — that is the whole
# correction discipline. RESIDUAL, stated: a genuine reintroduction that
# happens to contain one of these cues passes. The check is deliberately
# permissive in that one direction rather than forbidding the historical
# record, which is the defect a stricter version of this guard shipped
# with and had to be narrowed out of.
RETRACTION_CUES = ("read ", "restated", "retire", "retired", "withdraw",
                   "corrected", "earlier draft", "until 2026", "was, until",
                   "no count is stated", "census", "amended",
                   # A NEGATED claim is not an assertion of it. "P5 is no
                   # longer the long pole" is the correction, and a guard
                   # that fires on it forbids stating the repair.
                   "no longer", "not the long pole")


def check_retired(paths):
    """Two blind spots the 12/12 probe could not see, both fixed here.

    **Case.** `RETIRED_PHRASES` had no `re.IGNORECASE` while
    `SIZING_PHRASES` did, so `The 23`, `The ten` and `Ten local terms`
    all passed. Both patterns now carry it.

    **Input shape.** This iterated `splitlines()` against a document
    hard-wrapped at ~72 columns, so **seven of eight phrases passed when
    split across a wrap, including all four sizing phrases** —
    `plan:385` was one line-break away from firing. Blocks are now
    joined and matched with whitespace collapsed, and the reported line
    is the block's first line.

    The probe missed both because it **varied the phrase and not the
    shape of the input**. Deriving the subject of a search from a
    recorded enumeration was the right discipline applied to the wrong
    axis: *deriving the subject of a search does not derive the shape of
    its input.*
    """
    bad = []
    for path in paths:
        is_yaml = path.suffix in (".yaml", ".yml")
        lines = path.read_text().splitlines()
        # Group into blocks so a phrase broken by a hard wrap is still one
        # string. A blank line, or a change in blockquote status, ends a
        # block — a `>` line must not merge with the prose beside it or the
        # exemption would leak across the boundary.
        blocks, cur, start = [], [], 1
        for i, line in enumerate(lines, 1):
            quoted = line.lstrip().startswith(">")
            if not line.strip() or (cur and quoted != cur[0][1]):
                if cur:
                    blocks.append((start, cur)); cur = []
                start = i + 1
                continue
            if not cur:
                start = i
            cur.append((line, quoted))
        if cur:
            blocks.append((start, cur))

        for first, rows in blocks:
            if rows[0][1]:            # blockquoted block — a retraction
                continue
            joined = re.sub(r"\s+", " ", " ".join(r[0] for r in rows))
            probe = joined if is_yaml else re.sub(
                r'\*?"[^"\n]{0,300}"?\*?', "", joined)
            hit = RETIRED_PHRASES.search(probe) or SIZING_PHRASES.search(probe)
            if not hit:
                continue
            if any(c in joined.lower() for c in RETRACTION_CUES):
                continue
            bad.append("%s:%d — %r is a retired figure or a sizing claim, "
                       "outside a retraction. ADR-004's generated worklist is "
                       "the replacement and it states no total."
                       % (path.name, first, hit.group(0)))
    return bad


def main():
    items, ferrs = load()
    # Bail before rendering. A missing field must be reported, not
    # raised out of a formatter three frames down - a generator that
    # crashes instead of reporting fails in the wrong direction.
    if ferrs:
        print("FAIL\n  " + "\n  ".join(ferrs), file=sys.stderr)
        return 1
    blocks, lerrs = render(items)
    errors = lerrs
    text = DOC.read_text()

    if "--write" in sys.argv:
        for name, lines in blocks.items():
            new = splice(text, name, "\n".join(lines))
            if new is None:
                print("no markers for %s" % name, file=sys.stderr)
                return 1
            text = new
        DOC.write_text(text)
        print("wrote %d blocks" % len(blocks), file=sys.stderr)
        return 1 if errors else 0

    retired = check_retired([SRC, DOC])
    if retired and "--check" in sys.argv:
        print("FAIL\n  " + "\n  ".join(retired), file=sys.stderr)
        return 1

    if "--check" not in sys.argv:
        for name, lines in blocks.items():
            print("--- %s ---" % name)
            print("\n".join(lines))
            print()
        return 0

    stale = []
    for name, lines in blocks.items():
        beg, end = BEGIN % name, END % name
        if beg not in text or end not in text:
            stale.append("%s: markers missing" % name)
            continue
        cur = text[text.index(beg) + len(beg):text.index(end)].strip()
        if cur != "\n".join(lines).strip():
            stale.append("%s: stale — run --write" % name)
    if errors or stale:
        print("FAIL\n  " + "\n  ".join(errors + stale), file=sys.stderr)
        return 1
    lv, unstart, down, _, _ = levels(items)
    print("ok — %d items, %d generated blocks, %d levelled, %d not startable here"
          % (len(items), len(blocks), len(lv), len(unstart) + len(down)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
