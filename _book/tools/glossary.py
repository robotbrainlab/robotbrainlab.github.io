#!/usr/bin/env python3
"""glossary.py - build Appendix C from every chapter's Key Terms table.

Why generated rather than written: BOOK-GUIDE.md section 5 says "every bolded term goes in
the glossary", but the book also bolds whole phrases for emphasis, which is house style and
which both of Part I's reviewers accepted. Chapters 1-7 hold 29 Key Terms and 161 distinct
bolded spans, so a glossary built from bold spans would be 132 parts noise - the
crying-wolf failure of LEDGER-DEFECTS.md entry 18. The Key Terms tables are the curated
list, one per chapter, already written and already reviewed. So they are the source.

This also makes the glossary impossible to fall behind: it is regenerated, never edited.

    python3 tools/glossary.py            # write markdown/C-glossary.md
    python3 tools/glossary.py --check    # exit 1 if the file is missing or stale

It fails on a term defined twice with different wording. That is not a glossary problem, it
is a concept-ownership problem (BOOK-GUIDE.md section 4: every concept is owned by one
chapter), and LEDGER-TAUGHT.md is where it gets settled. Fix the chapters, not this file.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "markdown", "C-glossary.md")
ROW = re.compile(r"^\|\s*\*\*(?P<term>[^*|]+)\*\*\s*\|\s*(?P<meaning>.+?)\s*\|\s*$")

HEADER = """# Glossary

Every term the book defines, with the chapter that owns it. A term is defined in exactly one
chapter; every other chapter refers to it rather than redefining it.

| Term | Meaning | Ch |
|---|---|---|
"""


def chapters():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md"))):
        m = re.match(r"(\d+)-", os.path.basename(p))
        if m:
            out.append((int(m.group(1)), p))
    return [(n, p) for n, p in out if n > 0]


def key_terms(path):
    """The rows of this chapter's `### Key Terms` table."""
    text = open(path, encoding="utf-8").read()
    #  The lookahead matters: the old pattern required ANOTHER `### `
    #  heading after Key Terms, so a chapter whose Key Terms is its last
    #  section had every term silently dropped - and nothing caught it,
    #  because check-all.sh only fails on a STALE glossary and a chapter
    #  dropped at generation is dropped identically at comparison. Found
    #  by chapter 51's review; `cheatsheet.py` already did it this way.
    m = re.search(r"^### Key Terms\s*$(.*?)(?=^#{2,3}\s|\Z)", text,
                  re.M | re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        r = ROW.match(line.strip())
        if r:
            rows.append((r.group("term").strip(), r.group("meaning").strip()))
    return rows


def collect():
    terms, clashes = {}, []
    for n, path in chapters():
        for term, meaning in key_terms(path):
            key = term.lower()
            if key in terms and terms[key][1] != meaning:
                clashes.append((term, terms[key][2], n))
            terms.setdefault(key, (term, meaning, n))
    return terms, clashes


def render(terms):
    lines = [HEADER.rstrip("\n")]
    for key in sorted(terms):
        term, meaning, n = terms[key]
        lines.append(f"| **{term}** | {meaning} | {n} |")
    return "\n".join(lines) + "\n"


def main():
    check = "--check" in sys.argv
    terms, clashes = collect()
    for term, a, b in clashes:
        print(f"  CLASH  {term!r} defined in chapter {a} and chapter {b}, differently")
    if clashes:
        print(f"\nglossary: {len(clashes)} clash(es)  FAIL")
        print("A concept has two owners. Settle it in LEDGER-TAUGHT.md and fix the chapters.")
        sys.exit(1)
    body = render(terms)
    if check:
        if not os.path.exists(OUT):
            print(f"glossary: {OUT} missing  FAIL")
            sys.exit(1)
        if open(OUT, encoding="utf-8").read() != body:
            print("glossary: stale  FAIL - run python3 tools/glossary.py")
            sys.exit(1)
        print(f"glossary: {len(terms)} terms, up to date  CLEAN")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(body)
    print(f"glossary: wrote {len(terms)} terms from {len(chapters())} chapter(s) -> {OUT}")


if __name__ == "__main__":
    main()
