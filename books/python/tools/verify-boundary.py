#!/usr/bin/env python3
"""verify-boundary.py - the book teaches the Fundamentals stage, and stops there.

../GATES.md section 2.2 draws the line. This book has THREE boundaries, not one:

  1. The Advanced and Mastery material. Descriptors, metaclasses, variance, performance
     tuning and the C API are above this book. Chapter 51 says where they are.
  2. The shell, the editor and Git. Owned by *Linux and Git from Zero*. The book points
     at it and teaches none of it.
  3. Building a web service. Owned by *APIs to FastAPI*. Part III teaches the Python a
     service needs and stops short of the service.

A gate is needed because the breach is always plausible, which is the same reason the
finished book needed one. The honest answer to "why does @property work" IS the
descriptor protocol. The honest answer to "how do I serve this" IS a web framework. A
writer reaching for the real answer does not feel like a writer breaking a rule.

Chapter 51 is the chapter whose JOB is to name everything above, so it is exempt from
nearly all of it. Exemptions live in tools/boundary-exemptions.tsv, keyed by chapter and
term, each with its reason. An undeclared hit fails the build.

Usage: python3 tools/verify-boundary.py [FILE ...]
"""
import csv, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN = [
    # --- 1. Above this book: the Advanced stage
    "descriptor", "descriptor protocol", "__get__", "__set_name__",
    "metaclass", "__init_subclass__", "__mro_entries__",
    "covariant", "contravariant", "variance",
    "micro-optimisation", "micro-optimization",
    # --- 1. Above this book: the Mastery stage, and CPython itself
    "bytecode", "C API", "C extension", "Cython", "reference counting", "refcount",
    "PyObject", "CPython internals", "free list", "peephole",
    # --- 2. Owned by Linux and Git from Zero
    "interactive rebase", "git rebase", "git cherry-pick", "detached HEAD",
    "staging area", "git reflog", "git bisect",
    # --- 3. Owned by APIs to FastAPI
    "FastAPI", "Flask", "Django", "uvicorn", "ASGI", "WSGI", "APIRouter",
    "dependency injection", "OAuth2", "JWT", "response model", "request model",
    "path operation", "OWASP",
]


def exemptions():
    path = os.path.join(ROOT, "tools", "boundary-exemptions.tsv")
    allowed = {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            allowed.setdefault(row["chapter"], set()).add(row["term"].lower())
    return allowed


def chapter_of(path):
    """A chapter's number, or an appendix's letter."""
    base = os.path.basename(path)
    m = re.match(r"(\d+)-", base)
    if m:
        return str(int(m.group(1)))
    m = re.match(r"([A-Z])-", base)
    return m.group(1) if m else "?"


def check(path, allowed):
    ch = chapter_of(path)
    ok = allowed.get(ch, set())
    out, fence = [], False
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        for term in FORBIDDEN:
            if term.lower() in ok:
                continue
            if re.search(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", ln, re.I):
                out.append((i, term, ln.strip()[:70]))
    return out


def main():
    allowed = exemptions()
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md")))
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    if not files:
        print("VACUOUS - no Markdown to read. This gate checked NOTHING.")
        sys.exit(2)
    total = 0
    for f in files:
        for ln, term, txt in check(f, allowed):
            total += 1
            print(f"{os.path.basename(f)}:{ln}  outside this book: {term!r}\n      {txt}")
            print("      declare it in tools/boundary-exemptions.tsv with a reason, or cut it")
    print(f"\n{len(files)} file(s) read, {total} finding(s)")
    print("CLEAN - the boundary holds" if not total else "FAIL")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
