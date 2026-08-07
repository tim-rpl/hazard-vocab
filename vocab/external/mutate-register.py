#!/usr/bin/env python3
"""Mutations for the three block repairs, on a throwaway copy.

B6 (arity), B7 (drift), B8 (derived heading), and O's falsification of my
nominated attack line — a PERMUTATION the distribution's sum cannot see.

Nothing in the repository is written.
"""
import importlib.util
import pathlib
import re
import shutil
import sys
import tempfile

SRC = pathlib.Path(__file__).parent


def sub(path, old, new, n=1):
    """Replace, and RAISE if the target is not there.

    Every mutation here used a bare `str.replace`. A target that has moved
    matches nothing, returns silently, and the mutation then reports a
    mismatch for a reason unrelated to what it tests. `CLAUDE.md` names
    the shape; this is the second time it has bitten this file, because
    the previous fix repaired one call site and left the class.

    Third time, in fact: the edit that introduced THIS helper anchored on
    `def build(` — a function that does not exist here — so the helper
    was never inserted and every rewritten call site raised NameError.
    The insertion of a fail-loud helper, failing silently.
    """
    t = path.read_text()
    if old not in t:
        raise AssertionError("MISS mutation target in %s: %r"
                             % (path.name, old[:70]))
    path.write_text(t.replace(old, new, n))


def load(d, check=False):
    spec = importlib.util.spec_from_file_location("fx_%d" % id(d),
                                                  d / "fetch-external.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.CACHE = d / "graphs"
    m.REGISTER = d / "register.md"
    m.CHECK_ONLY[0] = check
    return m


def fresh():
    d = pathlib.Path(tempfile.mkdtemp()) / "external"
    shutil.copytree(SRC, d)
    return d


bad = []
CASES = 0


def case(label, fn, expect):
    global CASES
    CASES += 1
    d = fresh()
    try:
        got = fn(d)
    except AssertionError as e:
        got = "AssertionError: %s" % e
    ok = expect(got)
    print("%-52s %s" % (label[:50], "ok" if ok else "*** MISMATCH ***"))
    print("   %s" % (got if isinstance(got, str) else got))
    if not ok:
        bad.append(label)
    shutil.rmtree(d.parent)


# control
d = fresh()
m = load(d)
rc = m.sync_register()
print("control: sync_register rc=%d" % rc)
m2 = load(d, check=True)
print("control: --check rc=%d (0 = no drift, no arity fault)\n"
      % m2.sync_register())
if rc:
    sys.exit("control red")
BASE_CAUSES = int(re.search(r"\*\*(\d+) causes of non-dereference",
                            (d / "register.md").read_text()).group(1))
print("control: DECAY has %d rows\n" % BASE_CAUSES)
shutil.rmtree(d.parent)


# B6 — drop a header column. The write must be REFUSED, not silently
# rendered with a dropped column.
def b6(d):
    f = d / "fetch-external.py"
    sub(f, '"| Graph | Namespace | Dereferences | Why | Detail | Disposition |",\n'
           '           "|---|---|---|---|---|---|"]',
           '"| Graph | Namespace | Dereferences | Why | Disposition |",\n'
           '           "|---|---|---|---|---|"]')
    m = load(d)
    before = (d / "register.md").read_text()
    rc = m.sync_register()
    unchanged = (d / "register.md").read_text() == before
    return "rc=%d, register unchanged=%s" % (rc, unchanged)


case("B6 — header loses a column", b6,
     lambda g: g == "rc=1, register unchanged=True")


# B7 — hand-edit the committed register. --check must SEE it.
def b7(d):
    p = d / "register.md"
    t = p.read_text()
    # DERIVED, not hardcoded. This read "35 graphs with a sidecar" and the
    # register grew to 36, so the replace matched nothing, no drift was
    # introduced, and the mutation reported a MISMATCH for a reason that
    # had nothing to do with drift detection.
    #
    # This is the SAME bare-str.replace defect self-reported one round
    # ago, in this same file. That fix repaired the instance and left the
    # class — every other replace here was still silent on a miss. All of
    # them now raise.
    m = re.search(r"(\d+) graphs with a sidecar", t)
    if not m:
        raise AssertionError("MISS mutation target: no 'N graphs with a sidecar'")
    p.write_text(t.replace(m.group(0),
                           "%d graphs with a sidecar" % (int(m.group(1)) - 1), 1))
    return "check rc=%d" % load(d, check=True).sync_register()


case("B7 — committed register hand-edited", b7,
     lambda g: g == "check rc=1")


# B8 — add a decay row. The heading must FOLLOW, not be restated.
def b8(d):
    f = d / "fetch-external.py"
    sub(f, '    ("mints-nothing", "200 and a graph, but no term under its own namespace"),',
           '    ("mints-nothing", "200 and a graph, but no term under its own namespace"),\n'
           '    ("invented", "a sixth cause, added by the mutation"),')
    m = load(d)
    m.REASON_VERDICT["invented"] = "no"
    m.sync_register()
    head = int(re.search(r"\*\*(\d+) causes of non-dereference",
                         (d / "register.md").read_text()).group(1))
    # DERIVED from the control, not hardcoded. This asserted "6 causes",
    # and splitting `content` into `content` + `not-a-graph` made the
    # table six rows, so the mutation produced seven and the probe
    # reported a mismatch about its own stale expectation. Third instance
    # in this file of a probe naming a datum instead of deriving one.
    return "heading follows the table: %s" % (head == BASE_CAUSES + 1)


case("B8 — one more decay row is added", b8,
     lambda g: g == "heading follows the table: True")


# O's §5.3 falsification — a PERMUTATION. The sum cannot see it; the
# per-row invariant can.
def pick(d, reason):
    """A sidecar carrying `reason`, chosen from the cache rather than named.

    This hardcoded `adms` as the `resolves` subject. A live re-fetch moved
    `adms` to `content` — the ADMS namespace stopped defining `Identifier`
    — and the mutation then raised MISS on a target that was correct when
    written. Same class as the hardcoded row count in B7's mutation: a
    probe that names a datum instead of deriving one goes stale with the
    world, not with the code.
    """
    for p in sorted(d.glob("graphs/*.provenance.yaml")):
        if 'dereference_reason: "%s"' % reason in p.read_text():
            return p
    raise AssertionError("no sidecar with dereference_reason %r" % reason)


def perm(d):
    a, b = pick(d, "resolves"), pick(d, "access")
    sub(a, 'dereference_reason: "resolves"', 'dereference_reason: "access"')
    sub(b, 'dereference_reason: "access"', 'dereference_reason: "resolves"')
    m = load(d)
    rc = m.sync_register()
    return "rc=%d" % rc


case("O's permutation — two reasons swapped", perm,
     lambda g: g == "rc=1")


# and the same permutation with the per-row invariant DELETED, to prove
# that invariant is what catches it and not something else.
def perm_nocheck(d):
    f = d / "fetch-external.py"
    t = f.read_text()
    # FAIL LOUDLY on a missed target. This was a bare `str.replace`
    # against a line that had since moved, so the mutation applied
    # nothing, the run behaved like the control, and the matrix reported
    # a MISMATCH for a reason that had nothing to do with the invariant.
    # `CLAUDE.md` names this shape; it was in the probe checking for it.
    old = "        incoherent += check_reason_agrees(d, g.stem)"
    if old not in t:
        raise AssertionError("MISS mutation target: %r" % old)
    f.write_text(t.replace(old, "        pass", 1))
    a, b = pick(d, "resolves"), pick(d, "access")
    sub(a, 'dereference_reason: "resolves"', 'dereference_reason: "access"')
    sub(b, 'dereference_reason: "access"', 'dereference_reason: "resolves"')
    m = load(d)
    rc = m.sync_register()
    line = re.search(r"legend: (.*?)\.\n",
                     (d / "register.md").read_text(), re.S).group(1)
    return "rc=%d, distribution: %s" % (rc, line.strip()[:60])


case("  ...same permutation, invariant deleted", perm_nocheck,
     lambda g: g.startswith("rc=0"))


# the reason map itself: make it disagree with dereferences()
def map_drift(d):
    f = d / "fetch-external.py"
    sub(f, '    "mints-nothing": "document",     # NOT "no" — a document resolves',
           '    "mints-nothing": "no",')
    return load(d).sync_register()


case("REASON_VERDICT made to disagree with dereferences()", map_drift,
     lambda g: isinstance(g, str) and g.startswith("AssertionError"))

# F26: this read `%d/6` while the sibling probe derives the same figure
# from `len(STATES)` — two files disagreeing about a rule stated in one of
# them, and the affected number is the one this gate asked O to verify.
# Seven cases would have printed `6/6`. Fourth instance of the hardcoded
# number, in the file written to close that class.
print("\n%d/%d mutations behave as claimed" % (CASES - len(bad), CASES))
sys.exit(1 if bad else 0)
