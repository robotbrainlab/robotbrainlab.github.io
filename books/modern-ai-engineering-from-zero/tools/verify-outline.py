#!/usr/bin/env python3
"""verify-outline.py - the PDF outline has the right shape.

Why this exists: the outline was wrong three times in a row and the reader found all three
-- the front matter was missing from it, then the sub-parts sat beside Part I instead of
under it, then the chapters sat beside the sub-parts instead of under them. Every other
gate passed each time, because they all read Markdown and none of them opens the PDF.

A reader navigates a thousand-page book by its outline. It is part of the book.

Checks, from latex/book.out (hyperref writes it on every build):
  1. The front matter is present and at the top level: Cover, Title Page, Copyright,
     Contents, Preface -- and Index and Back Cover at the back.
  2. Levels never jump by more than one going deeper, so nothing is orphaned.
  3. Every sub-part is one level under a part.
  4. Every chapter is one level under whatever opened its part -- a sub-part where the part
     has them, the part itself where it does not.
  5. Sections are one level under their chapter.

Usage: python3 tools/verify-outline.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "latex", "book.out")
WANT_FRONT = ["Cover", "Title Page", "Copyright", "Contents", "Preface"]
WANT_BACK = ["Index", "Back Cover"]
ENTRY = re.compile(r"^\\BOOKMARK \[(-?\d+)\]\[-\]\{[^}]*\}\{(.*?)\}")


def entries():
    if not os.path.exists(OUT):
        sys.exit(f"no {OUT} - build the book first (cd latex && make)")
    rows = []
    for line in open(OUT, encoding="utf-8", errors="replace"):
        m = ENTRY.match(line.strip())
        if not m:
            continue
        raw = m.group(2).replace("\\376\\377", "")
        text = re.sub(r"\\(\d{3})", lambda x: chr(int(x.group(1), 8)), raw)
        rows.append((int(m.group(1)), text.replace("\x00", "").strip()))
    return rows


def main():
    rows = entries()
    if not rows:
        sys.exit("the outline is empty")
    problems = []
    top = [t for l, t in rows if l == -1]

    for name in WANT_FRONT + WANT_BACK:
        if name not in top:
            problems.append(f"{name!r} is missing from the top level of the outline")

    if top[:len(WANT_FRONT)] != WANT_FRONT:
        problems.append(f"the front matter is out of order: {top[:len(WANT_FRONT)]}")

    prev = rows[0][0]
    for i, (lvl, text) in enumerate(rows):
        if lvl > prev + 1:
            problems.append(f"{text!r} jumps from level {prev} to {lvl} - it is orphaned")
        prev = lvl

    # Every entry below the top must sit under something exactly one level shallower.
    stack = {}
    for lvl, text in rows:
        stack[lvl] = text
        if lvl > -1 and (lvl - 1) not in stack:
            problems.append(f"{text!r} at level {lvl} has no parent at level {lvl - 1}")

    # A part that has sub-parts must have its chapters under them, not beside them.
    for i, (lvl, text) in enumerate(rows):
        if not re.match(r"^\d+ ", text):
            continue
        parent = next((t for l, t in reversed(rows[:i]) if l == lvl - 1), None)
        if parent is None:
            problems.append(f"chapter {text!r} has no parent in the outline")

    for p in problems:
        print(f"  {p}")
    print(f"\n{len(rows)} outline entries, {len(problems)} problem(s)")
    print("CLEAN - the outline nests correctly" if not problems else "FAIL")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
