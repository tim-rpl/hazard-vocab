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


def is_blocked(path: str) -> bool:
    """True for the RATIONALE under design/, False for everything else.

    What is blocked is the reasoning O exists to test independently, not
    every file in the directory.

      * design/lean/, design/alloy/ -- artifacts O must run and may need
        to read to answer §4's vacuity questions (F7).
      * design/ADR-000-rationale.md -- the pre-decision rationale. This
        is what anchoring means and it stays blocked.
      * design/ADR-NNN-*.md for NNN > 000 -- decisions of record. At a
        design gate these ARE the artifact under review. Blocking them
        would leave O reviewing H's summary of a decision instead of the
        decision, which is the prose-versus-artifact defect this project
        has spent six gate blocks on.
    """
    if not path:
        return False
    p = path.replace("\\", "/").strip("'\"")
    parts = [seg for seg in p.split("/") if seg not in ("", ".")]
    if "design" not in parts:
        return False
    i = parts.index("design")
    tail = parts[i + 1:]
    if not tail:
        return True
    if tail[0] in ("lean", "alloy"):
        return False
    if tail[0].startswith("ADR-") and not tail[0].startswith("ADR-000"):
        return False
    return True


HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?.*?^\1\s*$",
                     re.S | re.M)
PATHISH = re.compile(r"[\w./~-]+")


def strip_heredocs(command: str) -> str:
    """Remove heredoc BODIES, keeping the command that introduces them.

    A heredoc body is content being written, not a path being read --
    that is F7. Stripping it lets the rest of the command be parsed
    normally instead of defeating the parser.
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
    hits, cmd_position, pattern_pending = [], True, False
    reading = False
    for tok in tokens:
        if tok in SEPARATORS:
            cmd_position, reading, pattern_pending = True, False, False
            continue
        if cmd_position:
            cmd_position = False
            base = pathlib.PurePath(tok).name
            reading = base in READERS
            pattern_pending = base in PATTERN_FIRST
            continue
        if tok.startswith("-"):
            continue
        if pattern_pending:
            # first non-flag argument to a grep-family command is the
            # pattern being searched FOR, not a file being read
            pattern_pending = False
            continue
        if set(tok) & REGEX_CHARS:
            continue
        if reading and is_blocked(tok):
            hits.append(tok)
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
        print(f"BLOCKED: role O may not read the design rationale "
              f"(reading command targets {hit}). {charter}", file=sys.stderr)
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