#!/usr/bin/env python3
"""Every automatic index entry is a term, or at least shaped like one.

Born 2026-10-28, from a build that broke. `latex/tools/filter.lua` turns every bold span of
four words or fewer into an `\\index{...}` entry, because in this book bold marks a new term.
Chapter 20 bolded a NUMBER for emphasis - `**-0.050 to +0.200**`, with a Unicode minus - so
makeindex was handed an entry starting with 0xE2, letter-grouped it on that first byte, and
wrote an invalid UTF-8 sequence into book.ind. XeLaTeX replaced it with U+FFFD and the glyph
gate failed. Nothing else in the suite looks at the index at all, and chapter 19 had already
shipped `\\index{4}` unnoticed.

One rule, objective and provable from the log: **an entry starts with an ASCII letter.** A
number or a sign is not a term, and makeindex groups letters bytewise, so a leading multi-byte
character becomes a broken group heading - which is precisely what happened.

A first draft of this gate also rejected a non-ASCII character ANYWHERE in an entry. That was
too strict and it was wrong about the mechanism: chapter 7 indexes the four part names, "I ·
Understand" and its three siblings, and their middle dot is harmless because the letter group
comes from the first character. Only the first character can break makeindex, and rule 1
already covers it.

The rule cannot tell a term from ordinary emphasis - `**read**` passes and is not a term. That
judgement stays with review. This catches the ones that are not judgement calls.

Fix a hit by un-bolding the span, or by naming the entry the way `filter.lua` documents:
`[**8,000 tokens**]{.noindex}` to opt out, `[**4**]{idx="rate times duration"}` to choose.
"""
import glob, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ENTRY = re.compile(r"\\index\{(.*?)\}")

def findings():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "latex", "chapters", "*.tex"))):
        for n, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
            for raw in ENTRY.findall(line):
                entry = raw.split("@")[0]          # sort key, which is what makeindex groups on
                if not entry:
                    continue
                if not entry[0].isascii() or not entry[0].isalpha():
                    out.append((os.path.basename(path), n, raw,
                                "starts with %r - not a term, and makeindex groups on it" % entry[0]))
    return out

def main():
    bad = findings()
    for f, n, entry, why in bad:
        print(f"  {f}:{n}  \\index{{{entry}}}  {why}")
    print(f"\n{len(bad)} bad index entr{'y' if len(bad)==1 else 'ies'}")
    if bad:
        print("Un-bold the span, or use [**x**]{.noindex} / [**x**]{idx=\"term\"} - see filter.lua.")
        return 1
    print("CLEAN - every index entry is shaped like a term")
    return 0

if __name__ == "__main__":
    sys.exit(main())
