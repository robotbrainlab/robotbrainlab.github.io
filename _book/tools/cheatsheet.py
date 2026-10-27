#!/usr/bin/env python3
"""cheatsheet.py - build Appendix A from every chapter's `### Worth Memorising` table.

Why generated, like the glossary: `TOC.md` puts Appendix A last in the writing order, and
HANDOVER section 3.1 flagged it as the one end-loaded item left - ten pages of "the numbers,
defaults and formulas worth memorising", assembled in the last three days from 57 finished
chapters, from memory. That is the one way this book may not be written.

So each chapter carries its own numbers and this collects them. A chapter adds a
`### Worth Memorising` table inside its `## Summary, Key Terms, and Review Questions`
section, after Key Terms:

    ### Worth Memorising

    | Item | Value or formula |
    |---|---|
    | Ten steps at nine-in-ten | 0.9^10 = 0.349, about a third |

**The section is optional.** A chapter with no number or formula worth carrying has none, and
most of Part I is like that - its material is principles, which the glossary and the chapters
already hold. `TOC.md` is explicit that this appendix is numbers, defaults and formulas.

    python3 tools/cheatsheet.py            # write markdown/A-cheat-sheet.md
    python3 tools/cheatsheet.py --check    # exit 1 if the file is missing or stale

It fails on the same item appearing twice with different values, because that is two chapters
disagreeing about a number rather than a formatting problem.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "markdown", "A-cheat-sheet.md")
ROW = re.compile(r"^\|\s*(?P<item>[^|]+?)\s*\|\s*(?P<value>.+?)\s*\|\s*$")

# Part boundaries, from TOC.md. Update here if the plan's parts ever change.
PARTS = [(1, 7, "Part I · Mental Model"), (8, 17, "Part I · Inside the Model"),
         (18, 39, "Part II · Use"), (40, 50, "Part III · Apply"),
         (51, 57, "Part IV · What Next")]

HEADER = """# Cheat Sheet

The numbers, defaults and formulas worth carrying in your head, in the order the book
introduces them. Every line came from the chapter that teaches it, so nothing here was
written from memory.
"""


def part_of(n):
    for lo, hi, name in PARTS:
        if lo <= n <= hi:
            return name
    return "Unplaced"


def chapters():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md"))):
        m = re.match(r"(\d+)-", os.path.basename(p))
        if m and int(m.group(1)) > 0:
            out.append((int(m.group(1)), p))
    return out


def rows_of(path):
    """The rows of this chapter's `### Worth Memorising` table, if it has one."""
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^### Worth Memorising\s*$(.*?)(?=^#{2,3}\s|\Z)", text, re.M | re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        r = ROW.match(line)
        if r and r.group("item").lower() not in ("item", "**item**"):
            rows.append((r.group("item"), r.group("value")))
    return rows


def collect():
    seen, clashes, by_part = {}, [], {}
    for n, path in chapters():
        for item, value in rows_of(path):
            key = item.lower().strip("*")
            if key in seen and seen[key][0] != value:
                clashes.append((item, seen[key][1], n))
            seen.setdefault(key, (value, n))
            by_part.setdefault(part_of(n), []).append((n, item, value))
    return by_part, clashes


def render(by_part):
    out = [HEADER.rstrip("\n")]
    for _, _, name in PARTS:
        rows = by_part.get(name)
        if not rows:
            continue
        out.append(f"\n## {name}\n")
        out.append("| Item | Value or formula | Ch |")
        out.append("|---|---|---|")
        for n, item, value in rows:
            out.append(f"| {item} | {value} | {n} |")
    return "\n".join(out) + "\n"


def main():
    by_part, clashes = collect()
    for item, a, b in clashes:
        print(f"  CLASH  {item!r} given different values in chapter {a} and chapter {b}")
    if clashes:
        print(f"\ncheat sheet: {len(clashes)} clash(es)  FAIL")
        print("Two chapters disagree about a number. Fix the chapters.")
        sys.exit(1)
    body = render(by_part)
    total = sum(len(v) for v in by_part.values())
    if "--check" in sys.argv:
        if not os.path.exists(OUT):
            print(f"cheat sheet: {OUT} missing  FAIL")
            sys.exit(1)
        if open(OUT, encoding="utf-8").read() != body:
            print("cheat sheet: stale  FAIL - run python3 tools/cheatsheet.py")
            sys.exit(1)
        print(f"cheat sheet: {total} item(s), up to date  CLEAN")
        return
    open(OUT, "w", encoding="utf-8").write(body)
    print(f"cheat sheet: wrote {total} item(s) -> {OUT}")


if __name__ == "__main__":
    main()
