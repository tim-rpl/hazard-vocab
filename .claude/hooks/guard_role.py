#!/usr/bin/env python3
"""Role-based access guard (PreToolUse).

The session is O (Overseer) when either HV_ROLE=O is set or a .role-O
marker file exists in the project root. Otherwise it is H and this hook
is a no-op.

Exit 2 blocks the tool call; stderr is fed back to the model.

Scope, stated honestly: this is friction, not a security boundary. It
exists to prevent accidental anchoring, which is the actual risk. A
session determined to route around it can.

Design notes, from [O -> H] measure gate finding F7:

  * design/lean/ and design/alloy/ are EXEMPT. FALSIFIER.md §1 grants O
    the right to read and run those artifacts, and §4 requires reading
    them to rule out vacuity. The previous guard denied what the charter
    granted.

  * Bash commands are inspected only where a READING command takes a
    blocked path as an argument. The previous guard substring-matched
    the entire command string, so O could not write a gate message that
    merely NAMED the forbidden directory in prose -- obstructing the one
    artifact O must produce while stopping nothing determined.

  * Parsed with the standard library, not jq. A missing jq exits 127,
    which is not 2, so the guard silently passed everything.
"""

from __future__ import annotations

import json
import os
import pathlib
import fnmatch
import re
import shlex
import sys

# Commands that read file contents. Only these have their arguments
# checked against blocked paths.
READERS = {
    "cat", "bat", "less", "more", "head", "tail", "nl", "od", "xxd",
    "strings", "grep", "egrep", "fgrep", "rg", "ag", "ack", "sed", "awk",
    "cut", "sort", "uniq", "wc", "diff", "cmp", "open", "code", "vim",
    "vi", "nano", "emacs", "python", "python3", "perl", "ruby", "node",
}

SEPARATORS = {"|", "||", "&&", ";", "&", "(", ")"}

# Readers whose FIRST non-flag argument is a search pattern, not a file.
# `grep -v '^./design/' list.txt` is an EXCLUSION — it asks not to see the
# rationale — and blocking it shapes how O can search for anything else.
# See [O -> H] design gate block verification 4.
PATTERN_FIRST = {"grep", "egrep", "fgrep", "rg", "ag", "ack", "sed", "awk"}

# Regex metacharacters. A token carrying these is a pattern, not a path.
REGEX_CHARS = set("^$*+?[]{}()|\\")

WRITE_ALLOWED = ("claims.md", "review-inbox.md")


RATIONALE = "ADR-000-rationale.md"
GLOB_CHARS = "*?[]{}"


def is_blocked(path: str) -> bool:
    """True for the rationale only. False for everything else.

    The previous version had a `return True` fallthrough for anything
    under design/ that was not lean/, alloy/, or ADR-NNN with NNN > 000.
    That blocked `design/surface.yaml` and `design/derive-surface.py` —
    the artifacts of a declared change — and contradicted charter v8,
    FALSIFIER.md §1, and this docstring, all of which say everything
    else under design/ is readable. It cost a gate two unverified
    mutation rows. See [O -> H] design gate block verification 5, BV5-3.

    Globs are resolved by the SHELL, so the hook only ever sees the
    unexpanded token: `design/*` reads eleven files including this one.
    A glob is therefore blocked when it COULD match the rationale, which
    is what fnmatch answers. `design/ADR-003*` does not; `design/ADR-*`
    does, and blocking it is correct because it expands to include the
    rationale. BV5-2.
    """
    if not path:
        return False
    p = path.replace("\\", "/").strip("'\"")
    if any(ch in p for ch in GLOB_CHARS):
        tok = p.lstrip("./").replace("{", "").replace("}", "")
        target = "design/" + RATIONALE
        return (fnmatch.fnmatch(target, tok)
                or fnmatch.fnmatch(RATIONALE, tok)
                or fnmatch.fnmatch(target, tok.rstrip("/") + "/*"))
    parts = [seg for seg in p.split("/") if seg not in ("", ".")]
    return bool(parts) and parts[-1] == RATIONALE


PATHISH = re.compile(r"[\w./~-]+")
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?.*?^\1\s*$", re.S | re.M)


def strip_heredocs(command: str) -> str:
    """Remove heredoc BODIES, keeping the command that introduces them.

    A heredoc body is content being written, not a path being read —
    that is F7. Stripping it lets the rest of the command parse normally
    instead of defeating the parser.
    """
    return HEREDOC.sub("<<HEREDOC", command)


def blocked_reads(command: str) -> list[str]:
    """Blocked paths appearing as arguments to a reading command.

    FAILS CLOSED. The first version returned [] when shlex raised --
    which it does on any unbalanced quote, including an ordinary
    apostrophe in a comment -- so `cat design/ADR-000-rationale.md # it's
    blocked` passed. A guard that gives up on hard input is a guard with
    a one-character bypass.
    """
    command = strip_heredocs(command)
    try:
        tokens = shlex.split(command, comments=False, posix=True)
    except ValueError:
        # Unparseable after heredoc stripping. Do NOT give up: scan every
        # path-like token. Coarser, and errs toward blocking.
        return [t for t in PATHISH.findall(command) if is_blocked(t)]
    # Flags that consume the NEXT token. `-e PATTERN` supplies the
    # pattern, so the first positional is then a FILE, not a pattern —
    # the previous version swallowed it anyway. `-f FILE` supplies a
    # file of patterns, which is itself a read.
    PATTERN_FLAGS = {"-e", "--regexp"}
    FILE_FLAGS = {"-f", "--file"}
    RECURSIVE_FLAGS = {"-r", "-R", "--recursive", "-rn", "-rl", "-ri",
                       "-rni", "-rin", "-rnE", "-rE", "-rh", "-roh",
                       "-rhE", "-rohE", "-rc"}
    ALWAYS_RECURSIVE = {"rg", "ag", "ack"}

    hits, cmd_position, pattern_pending, reading = [], True, False, False
    expect = None
    # A recursive search reaches the rationale by DIRECTORY TRAVERSAL and
    # never names it, so no token is inspectable. Disclosed by O after a
    # root-level `grep -r` returned a line of the blocked file. Require
    # an explicit exclusion instead; the block names the fix.
    recursive = False
    excluded = False
    base_cmd = ""
    roots = []
    for tok in tokens:
        if tok in SEPARATORS:
            cmd_position, reading, pattern_pending, expect = True, False, False, None
            continue
        if cmd_position:
            cmd_position = False
            base = pathlib.PurePath(tok).name
            reading = base in READERS
            pattern_pending = base in PATTERN_FIRST
            base_cmd = base
            if base in ALWAYS_RECURSIVE:
                recursive = True
            continue
        if expect == "pattern":
            expect, pattern_pending = None, False
            continue
        if expect == "file":
            expect = None
            if is_blocked(tok):
                hits.append(tok)
            continue
        if tok.startswith("-"):
            if tok in PATTERN_FLAGS:
                expect = "pattern"
            elif tok in FILE_FLAGS:
                expect = "file"
            if base_cmd in PATTERN_FIRST and tok in RECURSIVE_FLAGS:
                recursive = True
            if "exclude" in tok or "design" in tok:
                excluded = True
            continue
        if pattern_pending:
            # first positional of a grep-family command is the pattern
            pattern_pending = False
            continue
        # Regex metacharacters only disqualify a token in the PATTERN
        # slot. Applying it to every reader let `wc -l design/*` through,
        # because `*` is a regex character and also a glob. BV5-2.
        if reading and is_blocked(tok):
            hits.append(tok)
        if recursive:
            roots.append(tok)

    # A recursive search whose roots are all OUTSIDE design/ cannot reach
    # the rationale, and blocking it would make the guard obstruct the
    # searching O is required to do — which is F7's lesson.
    def reaches_design(r: str) -> bool:
        r = r.strip("'\"").rstrip("/")
        return r in ("", ".", "..", "/") or r.split("/")[0] == "design"

    if recursive and not excluded and not hits:
        if not roots or any(reaches_design(r) for r in roots):
            hits.append("<recursive search with no exclusion>")
    return hits


def main() -> int:
    role = os.environ.get("HV_ROLE", "")
    root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    if role != "O" and not pathlib.Path(root, ".role-O").exists():
        return 0

    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path") or ""
    command = ti.get("command") or ""

    charter = ("See FALSIFIER.md §1 (charter v8). Only "
               "design/ADR-000-rationale.md is blocked — numbered ADRs, "
               "design/lean/ and design/alloy/ are all permitted.")

    if path and is_blocked(path):
        print(f"BLOCKED: role O may not read the design rationale. {charter}",
              file=sys.stderr)
        return 2

    for hit in blocked_reads(command):
        if hit.startswith("<recursive"):
            print("BLOCKED: a recursive search reaches the design rationale "
                  "by directory traversal without naming it, so no path in "
                  "this command is inspectable. Re-run with an explicit "
                  "exclusion, e.g. --exclude-dir=design, or scope the "
                  "search to a directory. "
                  "NOTE: this covers grep-family recursion only — a "
                  "traversal piped from find or ls remains outside the "
                  "guard, which is friction, not a boundary.",
                  file=sys.stderr)
        else:
            print(f"BLOCKED: role O may not read the design rationale "
                  f"(reading command targets {hit}). {charter}",
                  file=sys.stderr)
        return 2

    if tool in ("Write", "Edit", "NotebookEdit") and path:
        if not path.endswith(WRITE_ALLOWED):
            print("BLOCKED: role O may only write claims.md and "
                  "review-inbox.md. Findings go to H. See FALSIFIER.md §8.",
                  file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())