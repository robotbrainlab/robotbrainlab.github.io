#!/usr/bin/env python3
"""verify-voice.py - the book must contain the subject and nothing else.

It never mentions a website, a roadmap, a learning path, numbered steps or tracks, the
research it was planned from, its own build, or the person it was written for. A reader
finishes it without learning how it was made.

This gate exists because in the French book the coverage, scope and correctness gates
ALL passed a chapter that opened "Your first tutor opened the course...". Voice was
simply not being checked. Ported, with this book's own origins in the pattern list.

It also catches a repo-style reference printed in learner-facing prose: "Chapter 12:384"
is a line number, and a PDF has pages. The records may cite lines freely; the book may
not.

Usage: python3 tools/verify-voice.py [FILE ...]
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = [
    (r"\broadmap\b",                      "the roadmap this book was planned from"),
    (r"\bnumbered (?:path|step)s?\b",     "the roadmap's numbered steps"),
    (r"\bthe (?:nine|9) (?:topics|subject areas)\b", "the planning taxonomy"),
    (r"\bTowards Intelligence\b",         "the website"),
    (r"\brobotbrainlab\b",                "the website"),
    (r"\bdata-intelligence\b",            "a website path"),
    (r"\bthe (?:web)?site\b",             "the website"),
    (r"\bresearch notes\b",               "the material the book was planned from"),
    (r"\bBOOK-GUIDE\b|\bTOC\.md\b|\bHANDOVER\b", "a build document"),
    (r"\bthis book was (?:built|written|planned)\b", "an origin statement"),
    (r"\bwe (?:decided|chose|agreed)\b",  "an origin statement"),
    (r"\bthe owner\b|\bDeepak\b",         "the reader named as a person"),
    (r"\byour (?:tutor|instructor|class|course)\b", "attribution to a teacher"),
    (r"Chapter \d+:\d+",                  "a line number - the book has pages"),
    (r"\bas (?:I|we) (?:said|wrote) (?:earlier|above) in chat\b", "an origin statement"),
]
COMPILED = [(re.compile(p, re.I), why) for p, why in PATTERNS]


def check(path):
    out = []
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        for rx, why in COMPILED:
            m = rx.search(ln)
            if m:
                out.append((i, why, m.group(0), ln.strip()[:70]))
    return out


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md")))
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    total = 0
    for f in files:
        for ln, why, hit, txt in check(f):
            total += 1
            print(f"{os.path.basename(f)}:{ln}  {why}: {hit!r}\n      {txt}")
    print(f"\n{len(files)} file(s), {total} finding(s)")
    print("CLEAN - the book never refers to its own origins" if not total else "FAIL")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
