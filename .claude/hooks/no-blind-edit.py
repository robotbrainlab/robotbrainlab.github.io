#!/usr/bin/env python3
"""Refuse a Bash command that edits a file in place without quoting what it removes.

[STATED 2026-11-14] Added at the owner's request, after this happened on 2026-11-13:
passages were removed from eight files by computing two offsets and splicing the text
between them. Nothing read those passages. The checks afterwards were a grep, a line
count and a syntax check - all three check form, none of them reads. Three false
statements survived it in books/python/GATES.md alone.

THE RULE: an edit that removes text must quote the exact text it removes. If you cannot
quote it, you have not read it, and you cannot judge what the removal leaves behind.

Use instead:
  * the Edit tool, which refuses to edit a file this conversation has not read, and
    takes exact old/new text; or
  * python3 books/python/tools/patch.py <file> <edits.json>, which does the same and
    logs every edit to records/EDITS.log.

DO NOT WORK AROUND THIS. If a command is blocked and you believe it is safe, say so to
the owner and let him decide. Finding another spelling of the same blind edit is the
failure this hook exists to stop.

It is deliberately narrow. A gate that cries wolf is a gate that gets switched off.
"""
import json, re, sys

ALLOW = ("patch.py",)          # the sanctioned editor

IN_PLACE = [
    (re.compile(r"\bsed\s+(-[a-zA-Z]*i|--in-place)\b"), "sed -i rewrites the file in place"),
    (re.compile(r"\bperl\s+(-[a-zA-Z]*i)\b"), "perl -i rewrites the file in place"),
    (re.compile(r"\bruby\s+(-[a-zA-Z]*i)\b"), "ruby -i rewrites the file in place"),
]

READS = (".read_text(", ".read()", ".readlines(", ".readline(")
WRITES = (".write_text(", "open(")


def read_modify_write(cmd):
    """A python invocation that both reads a file and writes one."""
    if not re.search(r"\bpython3?\b", cmd):
        return False
    if not any(r in cmd for r in READS):
        return False
    if ".write_text(" in cmd:
        return True
    # open(..., "w") / open(..., 'w')
    return bool(re.search(r"open\([^)]*['\"][wa]\+?['\"]", cmd))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0                                   # never block on a parse failure
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if any(a in cmd for a in ALLOW):
        return 0
    why = None
    for rx, reason in IN_PLACE:
        if rx.search(cmd):
            why = reason
            break
    if not why and read_modify_write(cmd):
        why = "this reads a file and writes it back, so it can remove text nobody read"
    if not why:
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Blocked: {why}.\n"
                "An edit that removes text must QUOTE the exact text it removes. If you "
                "cannot quote it, you have not read it.\n"
                "Use the Edit tool (it requires having read the file, and takes exact "
                "old/new text), or books/python/tools/patch.py, which also logs the edit.\n"
                "Do not look for another spelling of the same blind edit. If you believe "
                "this command is safe, say so and let the owner decide.\n"
                "Rule: .claude/CLAUDE.md, \"Standing rules, in every kind of session\". "
                "For the Python book it is also books/python/GATES.md section 8."),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
