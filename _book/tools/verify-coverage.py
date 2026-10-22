#!/usr/bin/env python3
"""verify-coverage.py - does the chapter contain what the plan said it would?

Every other gate in this suite runs chapter -> plan, which catches invention and is
structurally blind to omission. The French project added the reverse check late and it
immediately found a whole method section missing from a chapter that two reviews had
passed.

This reads the chapter's "Covers" cell in TOC.md, splits it on semicolons, and reports
any item whose distinctive words are all absent from the chapter. Hits are hints: an
item can be present under different words. Triage each and declare the count.

Usage: python3 tools/verify-coverage.py <chapter.md>   # prints misses and `covers-misses: N`
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set("""a an the and or of to in on for with by as is are be that this those these
it its from at into than then when where which who what how why not no than more most
you your they their we our i me my can may will would could should each both any all
one two three four five first second next last own same other another some such only
very much many few less least over under above below between within without about
across after before during through while because so if but yet still even just also
them he she his her him us do does did done has have had been being was were am""".split())
WORD = re.compile(r"[A-Za-z][A-Za-z@/+.-]{3,}")


def covers_for(stem_number):
    toc = open(os.path.join(ROOT, "TOC.md"), encoding="utf-8").read().split("\n")
    for ln in toc:
        if re.match(rf"^\|\s*{stem_number}\s*\|", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 5:
                return cells[3]
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    n = int(re.match(r"(\d+)-", os.path.basename(path)).group(1))
    covers = covers_for(n)
    if covers is None:
        sys.exit(f"no row for chapter {n} in TOC.md")
    body = open(path, encoding="utf-8").read().lower()
    misses = 0
    for item in [c.strip() for c in covers.split(";") if c.strip()]:
        words = [w.lower() for w in WORD.findall(item)
                 if w.lower() not in STOP and not w.startswith("**")]
        words = [w.strip("*`") for w in words]
        if words and not any(w in body for w in words):
            misses += 1
            print(f"  MISSING? {item[:90]}")
    print(f"\ncovers-misses: {misses}")
    print("Triage each with one grep before treating it as an omission.")


if __name__ == "__main__":
    main()
