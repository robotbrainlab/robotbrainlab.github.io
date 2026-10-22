#!/usr/bin/env python3
"""verify-inputs.py - every term a chapter builds on must already be in the book.

The French book's chapter 38 taught "take the nous form of the present" and ran that
rule on two verbs the book had never printed. Every gate passed it: the coverage gate
checks the sources against the book and never the book against itself, and nothing asks
whether an input a chapter depends on was ever given to the reader.

This lists every backticked term that appears in THIS chapter and in no earlier one. It
is a hint list, not a verdict: a chapter introducing a term for the first time is normal
and most hits are that. Triage each, and declare the count in the record.

Usage: python3 tools/verify-inputs.py <chapter.md>   # prints the list and `new-terms: N`
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = re.compile(r"`([^`\n]{2,40})`")


def terms(path):
    text = open(path, encoding="utf-8").read()
    return {m.group(1).strip() for m in TOKEN.finditer(text)}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    n = int(re.match(r"(\d+)-", os.path.basename(path)).group(1))
    earlier = sorted(f for f in glob.glob(os.path.join(ROOT, "markdown", "*.md"))
                     if re.match(r"(\d+)-", os.path.basename(f))
                     and int(re.match(r"(\d+)-", os.path.basename(f)).group(1)) < n)
    seen = set()
    for f in earlier:
        seen |= terms(f)
    new = sorted(terms(path) - seen)
    for t in new:
        print(f"  {t}")
    print(f"\nnew-terms: {len(new)}  (earlier chapters read: {len(earlier)})")
    print("Triage each: introduced here on purpose, or built on without ever being given?")


if __name__ == "__main__":
    main()
