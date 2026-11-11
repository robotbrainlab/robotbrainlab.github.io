#!/usr/bin/env python3
"""Every chapter's record must name the bank questions the bank assigns it.

BOOK-GUIDE §15: a chapter is not done until its questions in
markdown/B-interview-bank.md can be answered from it. The failure mode is not
disagreeing with the bank - it is never looking. Chapter 19 read its range as
39-41 when it owned 39-42, shipped to review with no answer to q42, and needed
a whole new section (LEDGER-DEFECTS entry 30). Chapter 15 made the same error
less expensively: its record said "29, 30 and 31" where the bank assigns 29-32,
and q32 happened to be answered anyway.

Both were a REMEMBERED range standing in for a grep. This checks the record
mentions each number the bank gives that chapter, which is weak - a record can
name a question it never answered - but it catches the one error that has
actually happened twice.

    python3 tools/verify-bank.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    bank = (ROOT / "markdown" / "B-interview-bank.md").read_text(encoding="utf-8")
    owned = {}
    for q, _, ch in re.findall(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|$", bank, re.M):
        owned.setdefault(int(ch), []).append(int(q))

    records = sorted(ROOT.glob("records/[0-9][0-9]-*.md"))
    problems = []
    checked = 0
    for f in records:
        n = int(f.name[:2])
        mine = owned.get(n)
        if not mine:
            continue
        text = f.read_text(encoding="utf-8")
        # a record is written before the chapter closes; only hold closed ones to it
        if re.search(r"(?m)^reviewed:\s*$", text):
            continue
        checked += 1
        # Records write ranges ("bank questions 39 to 42", "52 and 53"), so expand
        # every range in the record before asking which numbers it names. Without
        # this the check flags the interior of every range it meets, which is the
        # cry-wolf failure of LEDGER-DEFECTS entry 18.
        # The optional q is load-bearing: records write "q54", and \b does not
        # match between "q" and "5", so a plain \b54\b misses every one of them.
        named = {int(x) for x in re.findall(r"(?<!\d)q?(\d{1,3})\b", text)}
        for a, b in re.findall(r"(?<!\d)q?(\d{1,3})\s*(?:to|-|–|and)\s*q?(\d{1,3})\b", text):
            a, b = int(a), int(b)
            if 0 < b - a < 30:
                named.update(range(a, b + 1))
        absent = [q for q in mine if q not in named]
        if absent:
            problems.append((n, absent, mine))

    print()
    for n, absent, mine in problems:
        qs = ", ".join(str(q) for q in absent)
        print(f"  ch{n:02d}: record never names bank question(s) {qs} "
              f"(the bank assigns it {mine})")
    print(f"\n{checked} closed chapter(s) with bank questions, {len(problems)} problem(s)")
    if problems:
        print("Grep the bank by chapter number; never recall a range. Entry 30.")
        sys.exit(1)
    print("CLEAN - every closed chapter's record names the questions it owns")


if __name__ == "__main__":
    main()
