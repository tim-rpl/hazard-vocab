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



GUARD_FIX = HERE / "guard-fixtures"

# F10: `check_retired` was the ninth rule in `make lint` and the only one
# with no fixture pair. O named that twice as the proximate reason
# something shipped — B2's two blind spots, then B3's exemption
# granularity — because a probe leaves no residue in the repository and
# nothing re-runs it.
#
# Each row regresses a defect that actually shipped. `must_fire` is the
# direction; the fixture's own header names what it is for.
GUARD_CASES = [
    ("b3-yaml-no-blank-line.yaml", True,
     "B3 — no blank line, so a paragraph-scoped exemption ate the file"),
    ("b2-wrapped-phrase.md", True,
     "B2 — phrase split by a hard wrap, invisible to splitlines()"),
    ("b2-capitalised.md", True,
     "B2 — RETIRED_PHRASES had no re.IGNORECASE"),
    ("b3-table-cue-elsewhere.md", True,
     "B3 — a cue in one table row must not exempt another"),
    ("b3-sentence-scope.md", True,
     "B3 — cue in one sentence, figure in another, same paragraph"),
    ("b1-sizing-wrapped.md", True,
     "B1/B3 — a wrapped sizing claim; this shape was false and invisible"),
    # F11: each of these asserts its phrase with NO retraction cue in the
    # sentence, so the clause the fixture is named for is the ONLY thing
    # that can decide the verdict. The originals carried a cue AND a
    # quotation, so they stayed green through the cue path and six of ten
    # clauses could be deleted with nothing going red — C22's falsifier
    # verbatim, and its failure direction is the silent one: widening an
    # exemption leaves the run green either way.
    ("retraction-backtick-nocue.md", False, "F11 — the backtick strip alone"),
    ("retraction-asterisk-nocue.md", False, "F11 — the asterisk-quote strip alone"),
    ("retraction-prose-quote-nocue.md", False, "F11 — the prose bare-quote strip alone"),
    ("retraction-blockquote-nocue.md", False, "F11 — the blockquote skip alone"),
    ("b2-sizing-capitalised.md", True, "F11 — re.I on SIZING_PHRASES alone"),
    ("f13-unbalanced-quote.md", True,
     "F13 — one unbalanced `\"` exempted the next ~300 characters"),
    ("retraction-blockquote.md", False, "a blockquoted retraction"),
    ("retraction-asterisk-quote.md", False, "mention, not use: *'quoted'* + cue"),
    ("retraction-backtick-mention.md", False, "mention, not use: `backticked` + cue"),
    ("retraction-negation.md", False, "a negation IS the repair"),
    ("clean.md", False, "control — no figure, no sizing claim"),
    # F12: the only case asserting a LINE NUMBER. The 11 pairs before it
    # asserted fire/no-fire only, so a guard reporting the wrong line was
    # invisible to its own harness.
    ("f12-line-number.md", True, "F12 — the reported line must be the real one", 11),
]


def selftest_guard():
    """Run every fixture pair. Returns a list of failures.

    Asserted per fixture, in isolation, so a failure names the case —
    *exactly this named test fails* rather than *a named test fails*,
    which is the form that would have caught the slot branch and the
    `id:` branch while both sat uncovered at 8/8.
    """
    out, seen = [], set()
    for case in GUARD_CASES:
        name, must_fire, why = case[:3]
        want_line = case[3] if len(case) > 3 else None
        f = GUARD_FIX / name
        seen.add(name)
        if not f.exists():
            out.append("guard fixture missing: %s" % name)
            continue
        found = check_retired([f])
        fired = bool(found)
        if fired and want_line is not None:
            got = int(found[0].split(":")[1].split(" ")[0])
            if got != want_line:
                out.append("guard fixture `%s`: the violation is on line %d "
                           "and the guard reported line %d" % (name, want_line, got))
        if fired != must_fire:
            out.append("guard fixture `%s` (%s): expected %s, got %s"
                       % (name, why,
                          "a violation" if must_fire else "no violation",
                          "a violation" if fired else "none"))
    # An unreferenced fixture is a test nobody runs, sitting in the
    # directory looking like coverage.
    for f in sorted(GUARD_FIX.glob("*")):
        if f.is_file() and f.name not in seen:
            out.append("guard fixture `%s` is referenced by no case" % f.name)
    return out


def strip_mentions(joined, is_yaml):
    """Strip mention forms, recording WHERE and HOW MUCH was removed.

    F12: the previous version threw the spans away, so a hit position in
    the stripped text could not be mapped back to a line in the original.
    """
    cuts, probe, out, at = [], joined, [], 0
    pats = [r"`[^`\n]{0,300}`", r"\*['\"][^'\"\n]{0,300}['\"]\*"]
    if not is_yaml:
        # F13: the closing quote used to be OPTIONAL — `"?`. Paragraphs are
        # joined into one line before this runs, so the `\n` bound no longer
        # applies and a single unbalanced `"` exempted the next ~300
        # characters: a figure 20 characters after a stray quote was exempt,
        # at ~250 exempt, past 300 it fired. A mention is a QUOTED SPAN; an
        # unbalanced quote is not one, so the closer is required.
        pats.append(r'\*?"[^"\n]{0,300}"\*?')
    for pat in pats:
        res, last, acc = [], 0, []
        for m in re.finditer(pat, probe):
            acc.append(probe[last:m.start()])
            res.append((len("".join(acc)), m.end() - m.start()))
            last = m.end()
        acc.append(probe[last:])
        probe = "".join(acc)
        # shift earlier cuts that now sit after these
        cuts = sorted(cuts + res)
    return probe, cuts


def deleted_before(cuts, pos):
    """Total length removed at or before `pos` in the stripped text."""
    return sum(n for off, n in cuts if off <= pos)


def sentence_of(text, pos):
    """The retraction's scope is the sentence, not the block.

    Boundaries: sentence punctuation, a table-cell pipe, and a YAML key.
    A cue three table rows away, or in a different field of the same
    file, does not retract anything here.
    """
    L = max((text.rfind(d, 0, pos) for d in (". ", "! ", "? ", "|", "; ")),
            default=-1)
    R = min((r for r in (text.find(d, pos) for d in (". ", "! ", "? ", "|", "; "))
             if r != -1), default=len(text))
    return text[L + 1:R]


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

    **And the same mismatch has a write case, which cost seven lines of
    argument the same round.** P20's marker-clearing loop cut from a
    marker's first line to the next blank line; the markers had no blank
    line before the paragraph that followed, so it took PA17's latency
    rationale with them (F3). A **line-delimited edit against a
    paragraph-delimited structure** — this function's defect, in the
    editor instead of the search. Both axes, one round, two instruments:
    *match and edit on the structure the document has, not on the one the
    tool finds convenient.*
    """
    bad = []
    for path in paths:
        is_yaml = path.suffix in (".yaml", ".yml")
        lines = path.read_text().splitlines()
        # UNITS, not blocks. A unit is the smallest thing a retraction can
        # scope over, and it differs by structure:
        #
        #   YAML       one line — each field is its own record, and
        #              `items.yaml` has no blank line, so a paragraph rule
        #              made the whole file one unit (B3)
        #   table row  one line — a cue in row 3 does not retract row 20;
        #              two 26-line generated tables went exempt end to end
        #   prose      the paragraph, so a hard-wrapped phrase is still
        #              found (B2, the half that was right)
        #
        # Offsets are kept so a hit reports ITS OWN line. The first version
        # reported the unit's start, which put every `items.yaml` finding
        # at line 1 — a guard whose output cannot be acted on.
        units, cur = [], []
        for i, line in enumerate(lines, 1):
            # The table-row clause that stood here is REMOVED, measured
            # redundant 2026-08-05. `sentence_of` bounds on `|`, so a
            # table cell is already its own exemption scope whether or not
            # its row is its own unit. Deleting it changed nothing: 11/11
            # fixtures, the document, 64/64 on the two-axis probe, and all
            # four retraction forms.
            #
            # It is deleted rather than kept because **a clause nothing
            # depends on is a clause no fixture can cover** — F10's own
            # matrix could not isolate it, which is how the redundancy was
            # found, and keeping it would leave a permanent hole in the
            # matrix that looked like coverage.
            solo = (is_yaml or line.lstrip().startswith(">"))
            if solo or not line.strip():
                if cur:
                    units.append(cur); cur = []
                if solo and line.strip():
                    units.append([(i, line)])
                continue
            cur.append((i, line))
        if cur:
            units.append(cur)

        for unit in units:
            if unit[0][1].lstrip().startswith(">"):
                continue          # blockquoted — a retraction
            joined, offsets, at = "", [], 0
            for ln, txt in unit:
                txt = re.sub(r"\s+", " ", txt).strip()
                offsets.append((at, ln))
                joined += txt + " "
                at = len(joined)
            # An ASTERISK-WRAPPED quotation is rhetorical in either file
            # type — `*"…"*` and `*'…'*` are emphasis plus quotation, and
            # a document quoting the phrase it retracts uses them. YAML's
            # own quotes are the OUTER `"` of the scalar, which is syntax,
            # and stripping those is what exempted `items.yaml` wholesale
            # before B3. So: strip the rhetorical form everywhere, and the
            # bare form only where it cannot be syntax.
            # MENTION vs USE. `backticks` and *'asterisk quotes'* mark a
            # phrase being *talked about*; bare prose is a phrase being
            # *asserted*. The exemption is about exactly that difference,
            # so both mention forms are stripped before matching and a
            # bare-prose reintroduction still fires — probed below.
            probe, cuts = strip_mentions(joined, is_yaml)
            for hit in sorted(list(RETIRED_PHRASES.finditer(probe))
                              + list(SIZING_PHRASES.finditer(probe)),
                              key=lambda m: m.start()):
                if any(c in sentence_of(probe, hit.start()).lower()
                       for c in RETRACTION_CUES):
                    continue
                # F12: offsets index `joined`; the hit is in `probe`,
                # from which spans have been DELETED. Mapping a probe
                # position onto joined offsets under-reports by the length
                # of everything stripped before it — a figure on file line
                # 7 reported as 4, and the item table's last row at :270
                # reported :268. Exact for YAML only, because there each
                # line is its own unit and every offset is 0.
                #
                # `deleted` records how much was removed before each probe
                # position, so a probe offset maps back to a joined offset.
                jpos = hit.start() + deleted_before(cuts, hit.start())
                line_no = [ln for off, ln in offsets if off <= jpos][-1]
                bad.append("%s:%d — %r is a retired figure or a sizing "
                           "claim, outside a retraction. ADR-004's "
                           "generated worklist is the replacement and it "
                           "states no total."
                           % (path.name, line_no, hit.group(0)))
                break
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

    gerrs = selftest_guard()
    if gerrs and "--check" in sys.argv:
        print("FAIL  the retired-figure guard fails its own fixtures:\n  "
              + "\n  ".join(gerrs), file=sys.stderr)
        return 1

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
