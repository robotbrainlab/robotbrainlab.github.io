#!/usr/bin/env python3
"""verify-inputs.py - every term a chapter builds on must already be in the book.

It lists every backticked or bolded term that appears in THIS chapter and in no earlier
one. That part is a hint list, not a verdict: a chapter introducing a term for the first
time is normal and most hits are that. Triage each, and declare the count in the record.

It then runs a SECOND check that IS a verdict, and exits 1 on a hit: a term from the
curated list below, used in prose, neither bolded nor defined here, and never printed in
any earlier chapter. The reader was assumed to know a word the book never gave them.

----------------------------------------------------------------------------------
THE DOUBLE PASS, which is the one thing this gate must not report as a defect
----------------------------------------------------------------------------------
Decision 15 teaches the language twice. Part I gets the reader writing Python. Part II
returns to the same ground and explains it. So Part I legitimately uses words Part II
owns: chapter 4 builds a comprehension before chapter 25 explains what an iterator is.

The rule (../GATES.md section 4): a Part I chapter may use a term Part II owns IF it
gives the reader a plain working sentence for it where it is first used. Part II then
owns the full explanation and the `### Key Terms` row.

ALLOW below is that list, and every entry NAMES THE CHAPTER THAT OWNS THE TERM, so a
reader of this file can tell a loan from a mistake. Adding a term to ALLOW without the
owning chapter in the comment is how this list rots.

Usage: python3 tools/verify-inputs.py <chapter.md>
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = re.compile(r"`([^`\n]{2,40})`")
BOLD  = re.compile(r"\*\*([^*\n]{2,40})\*\*")

# ---------------------------------------------------------------- the jargon list
# CURATED, never derived. A term belongs here only if a reader could NOT guess it from
# plain English and the book plans to teach it somewhere. Words that double as ordinary
# English cannot be checked this way and are deliberately absent: "scope", "property",
# "index", "set", "object", "class", "string", "import". The completeness review is what
# catches those. A gate that cries wolf is a gate nobody reads.
JARGON = [
    # the language, mostly owned by Part II
    "iterable", "iterator", "generator", "comprehension", "closure", "decorator",
    "context manager", "coroutine", "awaitable", "event loop", "dunder",
    "data model", "method resolution order", "MRO", "immutable", "mutable",
    "hashable", "f-string", "duck typing", "structural typing",
    # tooling, owned by Part I
    "virtual environment", "wheel", "fixture", "parametrize", "monkeypatch",
    "type hint", "annotation", "traceback", "linter", "formatter",
    "property-based", "continuous integration",
    # concurrency, owned by Part III
    "global interpreter lock", "GIL", "semaphore", "deadlock", "race condition",
    "pickle", "picklable", "start method",
    # data, owned by Part III
    "ORM", "N+1", "migration", "transaction", "autocommit", "query plan",
    "foreign key", "primary key", "idempotent",
]

# A term used EARLIER than the chapter that owns it, on purpose. Name the owning chapter.
ALLOW = {
    "iterable",         # owned by ch 25; ch 4 builds comprehensions over one
    "immutable",        # owned by ch 22; ch 2 and ch 4 need it for tuples and strings
    "mutable",          # owned by ch 22; ch 4 needs it for lists and dicts
    "hashable",         # owned by ch 22; ch 4 needs it for sets and dict keys
    "context manager",  # owned by ch 26; ch 6 opens files with `with`
    "decorator",        # owned by ch 24; ch 12 uses pytest markers
    "traceback",        # owned by ch 8, which teaches reading one
    "type hint",        # owned by ch 14; ch 1 and ch 9 may show one in passing
}


def vocabulary():
    return set(JARGON)


def terms(path):
    text = open(path, encoding="utf-8").read()
    out = {m.group(1).strip() for m in TOKEN.finditer(text)}
    out |= {m.group(1).strip() for m in BOLD.finditer(text)}
    return out


def unescape(s):
    return re.sub(r"\\([^A-Za-z0-9])", r"\1", s)


def used_bare(path, vocab, earlier_text):
    """Vocabulary used in prose, never bolded here, never printed before."""
    text = unescape(open(path, encoding="utf-8").read())
    defined = {unescape(t).lower() for t in terms(path)}
    hits = []
    for term in sorted(vocab):
        if term in ALLOW:
            continue
        pat = re.compile(r"\b" + re.escape(term) + r"(s|es)?\b", re.I)
        if not pat.search(text):
            continue
        if any(term.lower() in d for d in defined):
            continue                       # the chapter introduces it properly
        if pat.search(earlier_text):
            continue                       # the reader has met it
        hits.append(term)
    return hits


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    m = re.match(r"(\d+)-", os.path.basename(path))
    if not m:
        sys.exit(f"{path} is not a numbered chapter")
    n = int(m.group(1))
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

    earlier_text = "".join(open(f, encoding="utf-8").read() for f in earlier)
    bare = used_bare(path, vocabulary(), earlier_text)
    print()
    if bare:
        for b in bare:
            print(f"  BARE  {b!r} - used in prose, not defined here, not printed earlier")
        print(f"\nbare-terms: {len(bare)}  FAIL")
        print("Give the term plainly where you use it, or use words the reader already has.")
        print("If Part II owns it and Part I needs it, add it to ALLOW with the owning chapter.")
        sys.exit(1)
    print("bare-terms: 0  CLEAN - no jargon used before the book gives it")


if __name__ == "__main__":
    main()
