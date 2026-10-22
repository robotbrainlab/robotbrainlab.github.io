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

WORDS = r"always|never|all|only|every|any|none|must|cannot|can't|impossible|guarantee[sd]?|identical|the same"
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
