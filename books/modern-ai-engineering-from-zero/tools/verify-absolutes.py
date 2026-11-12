#!/usr/bin/env python3
"""verify-absolutes.py - list every absolute in a chapter so each one can be tested.

Thirteen of twenty findings in one French review round were an absolute with its
counter-example sitting in the same chapter. No gate can test an absolute, so this one
does not try. It produces the list and the count, and the chapter's record must declare
that many as tested. verify-record.py fails when the numbers disagree.

That coupling is the point: a prose instruction to "check every always" is what gets
skipped. A number that must match is not.

Usage: python3 tools/verify-absolutes.py <chapter.md>   # prints the list and `absolutes: N`
"""
import os, re, sys

# "nothing", "nobody", "no X" and "almost" were missing until 2026-10-23. Chapter 7 shipped
# "Nothing here is a lab" in its own four-parts table while carrying a lab 120 lines below,
# and this gate listed none of it. An absolute whose counter-example is in the same file is
# exactly what the gate exists to surface, so the list now covers the negative forms too.
# `no \w+` was tried and dropped: it added ~27 hits per chapter, nearly all of them "no idea",
# "no longer", "no code". A hint list too long to read is the same failure as a gate that cries
# wolf, so only the forms that have actually carried a defect here are listed.
WORDS = (r"always|never|all|only|every|any|none|nothing|nobody|no one|almost|must|cannot|can't"
         r"|impossible|guarantee[sd]?|identical|the same")
RX = re.compile(r"\b(" + WORDS + r")\b", re.I)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    hits, fence = [], False
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        for m in RX.finditer(ln):
            hits.append((i, m.group(0), ln.strip()[:90]))
    for i, word, txt in hits:
        print(f"{i:5d}  {word:<12} {txt}")
    print(f"\nabsolutes: {len(hits)}")
    print("Test each against a counter-example IN THE BOOK, not only in this chapter.")


if __name__ == "__main__":
    main()
