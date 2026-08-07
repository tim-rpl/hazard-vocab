#!/usr/bin/env python3
"""Every enumerated cache state, against both generators, on throwaway copies.

B5's class, not B5's fourth instance. The table in `fetch-external.py`
beside `cache_state()` says which predicate catches which state; this runs
all of them and asserts that `bound-terms.md` and `register.md` are
byte-identical afterwards in every failing state.

Nothing in the repository is written.
"""
import hashlib
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

SRC = pathlib.Path(__file__).parent
PY = sys.executable
# THE RULE THIS FILE FOLLOWS, stated because it was learned three times:
# a literal describing BEHAVIOUR is fine — `rc=1`, `untouched=True` are
# the contract under test and cannot go stale. A literal describing DATA
# must be DERIVED. Three probes broke on data literals before this was
# written down: a row count, a source key, and a table size. Each was
# correct when written and each went stale with the world rather than
# with the code, so each reported a mismatch about its own expectation.


def _tracked():
    """The graphs a checkout ships, read from git rather than listed.

    This was four filenames typed out. They are the `.gitignore`
    exceptions, and any change to that list would have left the probe
    asserting a cache state the repository no longer has.
    """
    out = subprocess.run(["git", "ls-files", "graphs/*.ttl"],
                         cwd=str(SRC), capture_output=True, text=True)
    names = {pathlib.Path(l).name for l in out.stdout.split() if l}
    if not names:
        raise AssertionError("no tracked graphs — this probe cannot build "
                             "the `unfetched` state and would silently "
                             "test something else")
    return names


TRACKED = _tracked()


def _audit_keys():
    """The graphs `audit-bound-terms.py` actually reads, from its LOOKUP."""
    spec = importlib.util.spec_from_file_location(
        "_au", SRC / "audit-bound-terms.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {k for k, _n in m.LOOKUP}


AUDIT_KEYS = _audit_keys()


def _fetched(in_scope, exclude=()):
    """A cached, non-tracked graph to degrade — chosen, not named.

    The subject was a hardcoded filename, and removing it found a real
    hole: the audit reads only the six graphs in its `LOOKUP`, and
    `cache_state(keys=…)` is scoped to them deliberately — *a degraded
    graph nobody reads cannot corrupt the file being written*. The
    hardcoded subject happened to be one the audit reads, so the earlier
    8/8 tested the in-scope half and asserted nothing about the other.

    Both halves are now subjects, and the out-of-scope cases assert the
    scoping decision rather than assuming it: the audit must pass and the
    REGISTER must still fail, because the register reads every graph.
    """
    for p in sorted(SRC.glob("graphs/*.ttl")):
        stem = p.name[:-4]
        if p.name in TRACKED or p.name in exclude or p.stat().st_size <= 1000:
            continue
        if (stem in AUDIT_KEYS) == in_scope:
            return p.name
    raise AssertionError("no %s graph available to degrade"
                         % ("in-scope" if in_scope else "out-of-scope"))


SUBJECT = _fetched(True)                  # the audit reads this one
OTHER = _fetched(True, exclude=(SUBJECT,))
OUTSIDE = _fetched(False)                 # the audit does not


def fresh():
    d = pathlib.Path(tempfile.mkdtemp()) / "external"
    shutil.copytree(SRC, d)
    # the copy has no .git, so `git ls-files` returns nothing and every
    # state would read `unfetched`. Give it the tracked set explicitly.
    subprocess.run(["git", "init", "-q"], cwd=d.parent, check=True)
    for f in TRACKED:
        subprocess.run(["git", "add", "-f", "external/graphs/%s" % f],
                       cwd=d.parent, check=True)
    return d


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else None


def run(d, script, *args):
    r = subprocess.run([PY, str(d / script), *args],
                       capture_output=True, text=True, cwd=str(d))
    return r.returncode, (r.stdout + r.stderr)


# state -> mutation. None = control.
STATES = [
    ("6 complete (control)", None, 0),
    ("1 unfetched — only tracked graphs",
     lambda d: [p.unlink() for p in d.glob("graphs/*.ttl")
                if p.name not in TRACKED], 0),
    ("2 a listed graph has no file",
     lambda d: (d / "graphs" / SUBJECT).unlink(), 1),
    ("3 zero-byte file",
     lambda d: (d / "graphs" / SUBJECT).write_bytes(b""), 1),
    ("4 truncated file",
     lambda d: (d / "graphs" / SUBJECT).write_bytes(
         (d / "graphs" / SUBJECT).read_bytes()[:400]), 1),
    ("5 wrong document cached",
     lambda d: (d / "graphs" / SUBJECT).write_bytes(
         (d / "graphs" / OTHER).read_bytes()), 1),
    ("6 valid graph, zero triples",
     lambda d: (d / "graphs" / SUBJECT).write_bytes(
         b"@prefix x: <http://example.org/> .\n"), 1),
    ("7 .ttl holding RDF/XML (already true in the cache)", None, 0),
    # The scoping decision, asserted rather than assumed. The audit reads
    # six graphs; degrading a seventh must NOT stop it writing, and must
    # still stop the register, which reads all of them.
    ("8 out-of-scope graph zero-byte — audit unaffected",
     lambda d: (d / "graphs" / OUTSIDE).write_bytes(b""), 0),
]

bad = []
for label, mutate, want in STATES:
    d = fresh()
    before_bt = digest(d / "bound-terms.md")
    before_rg = digest(d / "register.md")
    if mutate:
        mutate(d)
    rc_a, out_a = run(d, "audit-bound-terms.py")          # WRITE path
    rc_r, out_r = run(d, "fetch-external.py", "--check")
    reg_note = ""
    if mutate and want == 0 and label.startswith("8"):
        # the register must see what the audit is right to ignore
        reg_note = "  register rc=%d" % rc_r
        if rc_r == 0:
            bad.append(label + " (register did not see it)")
    after_bt = digest(d / "bound-terms.md")
    after_rg = digest(d / "register.md")
    untouched = (before_bt == after_bt) and (before_rg == after_rg)
    # in a passing state the write path legitimately rewrites an identical
    # file, so "untouched" is about CONTENT, which the digest already is.
    ok = (rc_a == want) and untouched
    print("%-46s audit rc=%d  untouched=%-5s %s%s"
          % (label[:44], rc_a, untouched,
             "ok" if ok else "*** MISMATCH ***", reg_note))
    first = [l for l in out_a.splitlines() if "FAIL" in l or "not written" in l]
    if first:
        print("      %s" % first[0][:120])
    if not ok:
        bad.append(label)
    shutil.rmtree(d.parent)

print("\n%d/%d states behave as enumerated" % (len(STATES) - len(bad), len(STATES)))
sys.exit(1 if bad else 0)
