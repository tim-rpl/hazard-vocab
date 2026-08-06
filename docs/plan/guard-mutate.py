#!/usr/bin/env python3
"""F10's mutation matrix: delete a guard clause, assert the EXACT set of
fixtures that fails.

O's form — *the strongest is not "a named test fails" but "exactly this
named test fails."* A clause deletion that reddens some test proves the
clause is reached; it does not prove the fixture claiming to cover it is
what reaches it, nor that nothing else was covering it by accident.

Runs against a throwaway copy. Nothing in the repository is written.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

SRC = pathlib.Path(__file__).resolve().parent

MUTATIONS = [
    # Each mutation deletes ONE clause, faithfully. The first version of
    # this matrix mutated crudely — "match per line" was implemented as
    # "keep only the unit's first line" — and mismatched for that reason
    # rather than because the guard was wrong.
    ("drop re.IGNORECASE from RETIRED_PHRASES",
     "    re.IGNORECASE)   # B2: absent here while SIZING_PHRASES had it",
     "    )",
     {"b2-capitalised.md"}),
    ("YAML uses paragraph units instead of one per line (pre-B3)",
     '            solo = (is_yaml or line.lstrip().startswith(">"))',
     '            solo = (line.lstrip().startswith(">"))',
     {"b3-yaml-no-blank-line.yaml"}),
    ("drop `|` from sentence_of's delimiters",
     '    L = max((text.rfind(d, 0, pos) for d in (". ", "! ", "? ", "|", "; ")),',
     '    L = max((text.rfind(d, 0, pos) for d in (". ", "! ", "? ", "; ")),',
     {"b3-table-cue-elsewhere.md"}),
    ("exempt on the unit instead of the sentence (the B3 defect)",
     "                if any(c in sentence_of(probe, hit.start()).lower()",
     "                if any(c in probe.lower()",
     # Both, and this is derivable rather than observed: with the
     # redundant row-as-unit clause deleted, a table is one unit, so a
     # unit-scoped exemption necessarily merges its cells. The sentence
     # clause is now the ONLY thing separating them.
     {"b3-sentence-scope.md", "b3-table-cue-elsewhere.md"}),
    ("stop stripping backticked mentions",
     '            probe = re.sub(r"`[^`\\n]{0,300}`", "", joined)',
     '            probe = joined',
     set()),
]


def fresh():
    d = pathlib.Path(tempfile.mkdtemp()) / "plan"
    shutil.copytree(SRC, d)
    return d


def failing(d):
    """Set of guard-fixture names the selftest reports as failing."""
    r = subprocess.run([sys.executable, str(d / "derive-waves.py"), "--check"],
                       capture_output=True, text=True)
    return set(re.findall(r"guard fixture `([^`]+)`", r.stderr))


base = fresh()
if failing(base):
    sys.exit("control is red: %s" % failing(base))
print("control: all 10 fixture pairs pass\n")
shutil.rmtree(base.parent)

bad = []
for label, old, new, expect in MUTATIONS:
    d = fresh()
    f = d / "derive-waves.py"
    t = f.read_text()
    if old not in t:
        sys.exit("MISS mutation target: %s" % label)
    f.write_text(t.replace(old, new, 1))
    got = failing(d)
    ok = got == expect
    print("%-56s %s" % (label[:54], "ok" if ok else "*** MISMATCH ***"))
    print("   expected: %s" % (sorted(expect) or "none"))
    print("   got:      %s" % (sorted(got) or "none"))
    if not ok:
        bad.append(label)
    shutil.rmtree(d.parent)

print("\n%d/%d mutations produce EXACTLY the expected failure set"
      % (len(MUTATIONS) - len(bad), len(MUTATIONS)))
sys.exit(1 if bad else 0)
