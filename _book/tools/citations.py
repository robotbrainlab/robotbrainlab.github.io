#!/usr/bin/env python3
"""List one chapter's cross-chapter citations with the cited TOC row beside each.

This is a REVIEW AID, not a gate, and it is deliberately not wired into
check-all.sh. Chapters 23 and 25 each shipped a citation crediting a claim to
the wrong chapter - chapter 23 credited chapter 51's premise to chapter 16 and
chapter 21's sentence to chapter 20 - and both survived a completeness review
because checking a citation means reading the other chapter's TOC row.

It is not a gate because it cannot be one. The book cites chapters in a dozen
shapes ("chapter 13 is where...", "that is chapter 26's", "see chapter 9"),
and only seven of 537 citations use a form stating ownership outright. A
pattern wide enough to catch the rest flags mostly correct prose, which is
LEDGER-DEFECTS entry 18: a gate that cries wolf is worse than no gate.

So this prints and exits 0. Read it beside the chapter and ask of each line:
does the chapter I am pointing at actually own this?

    python3 tools/citations.py 26
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def toc_rows():
    rows = {}
    for line in (ROOT / "TOC.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|", line)
        if m and 1 <= int(m.group(1)) <= 57:
            rows.setdefault(int(m.group(1)), (m.group(2).strip(), m.group(4).strip()))
    return rows


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    want = sys.argv[1].zfill(2)
    hits = sorted(ROOT.glob(f"markdown/{want}-*.md"))
    if not hits:
        sys.exit(f"no chapter file for {want}")
    path = hits[0]
    rows = toc_rows()
    own = int(want)

    cites = collections.defaultdict(list)
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith(("    ", "\t")):
            continue                      # program source and printed output
        for m in re.finditer(r"[Cc]hapters?\s+(\d+)(?:\s*(?:to|-|and|,)\s*(\d+))?", line):
            for g in m.groups():
                if g:
                    cites[int(g)].append((i, line.strip()))

    print(f"{path.name}: cites {len(cites)} other chapter(s)\n")
    for n in sorted(cites):
        title, covers = rows.get(n, ("(NOT IN TOC)", ""))
        flag = "  <-- SELF" if n == own else ""
        print(f"=== chapter {n}: {title}{flag}")
        if covers:
            print(f"    covers: {covers[:160]}")
        for i, line in cites[n]:
            print(f"    L{i}: {line[:110]}")
        print()
    total = sum(len(v) for v in cites.values())
    print(f"{total} citation(s). Check each against the covers line above it.")


if __name__ == "__main__":
    main()
