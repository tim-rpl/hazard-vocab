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
    # F11: one mutation per previously-uncovered clause. Each must fail
    # EXACTLY its no-cue fixture. The originals stayed green through the
    # cue path, so these clauses could be deleted with nothing red —
    # C22's falsifier, and its failure direction is the silent one.
    ('stop stripping asterisk-quoted mentions (F11)',
     '    pats = [r"`[^`\\n]{0,300}`", r"\\*[\'\\"][^\'\\"\\n]{0,300}[\'\\"]\\*"]',
     '    pats = [r"`[^`\\n]{0,300}`"]',
     {'retraction-asterisk-nocue.md'}),
    ('stop stripping bare quotes in prose (F11)',
     '        pats.append(r\'\\*?"[^"\\n]{0,300}"?\\*?\')',
     '        pass',
     {'retraction-prose-quote-nocue.md'}),
    ('stop skipping blockquoted units (F11)',
     '            if unit[0][1].lstrip().startswith(">"):',
     '            if False and unit[0][1].lstrip().startswith(">"):',
     {'retraction-blockquote-nocue.md'}),
    ('drop re.I from SIZING_PHRASES (F11)',
     '    r"\\blong pole\\b|\\bL-sized\\b|\\bwidest item\\b|\\bstartable today\\b", re.I)',
     '    r"\\blong pole\\b|\\bL-sized\\b|\\bwidest item\\b|\\bstartable today\\b")',
     {'b2-sizing-capitalised.md'}),
    # F12: the mapping from a probe position back to a source line. The
    # first version of the fixture put its stripped spans in an EARLIER
    # paragraph, where offsets restart, so it asserted a line number
    # without testing the mapping and passed with the fix reverted.
    # Measured: 11 with the fix, 8 without.
    ("revert the F12 position mapping",
     "                jpos = hit.start() + deleted_before(cuts, hit.start())",
     "                jpos = hit.start()",
     {"f12-line-number.md"}),
    ("stop stripping backticked mentions",
     '    pats = [r"`[^`\\n]{0,300}`", r"\\*[\'\\"][^\'\\"\\n]{0,300}[\'\\"]\\*"]',
     '    pats = [r"\\*[\'\\"][^\'\\"\\n]{0,300}[\'\\"]\\*"]',
     {'retraction-backtick-nocue.md'}),
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
