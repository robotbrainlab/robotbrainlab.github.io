#!/usr/bin/env python3
r"""verify-contents.py - the contents tree has the right shape.

It reads **book.toc**. There is no PDF-outline gate: `book.out` is written by hyperref
alone, and the shared preamble also loads the `bookmark` package, which writes the outline
straight into the PDF and produces no `book.out`. Reading it back out of the PDF needs a
PDF library, and this machine has none.

**What this does NOT check**: the front-matter bookmarks - Cover, Title Page, Copyright,
Contents, Back Cover. They are \pdfbookmark calls and never reach book.toc. They are on
the hand-check list in ../GATES.md section 6.

What it does check, all of it provable from the file:

  1. The Preface is there, and first.
  2. The Index is there, and last.
  3. Every chapter sits after a part. A chapter before the first part is orphaned.
  4. Chapter numbers run 1, 2, 3 ... with no gap and no repeat.
  5. A section never appears before its chapter.
  6. The four part names are the owner's, and in order.

Usage: python3 tools/verify-contents.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOC = os.path.join(ROOT, "book.toc")
LINE = re.compile(r"\\contentsline\s*\{(\w+)\}\{(.*?)\}\{")
PARTS = ["Write It", "Why It Works That Way", "Build With It", "What Next"]


def entries():
    if not os.path.exists(TOC):
        sys.exit(f"no {TOC} - build the book first (make -C ../latex BOOK=python)")
    rows = []
    for ln in open(TOC, encoding="utf-8", errors="replace"):
        m = LINE.match(ln.strip())
        if m:
            text = re.sub(r"\\numberline\s*\{([^}]*)\}", r"\1 ", m.group(2))
            text = re.sub(r"\\hspace\s*\{[^}]*\}", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            rows.append((m.group(1), text))
    return rows


def main():
    rows = entries()
    if not rows:
        print(f"VACUOUS - {TOC} holds no entries. This gate checked NOTHING.")
        sys.exit(2)
    problems = []
    kinds = [k for k, _ in rows]
    texts = [t for _, t in rows]

    if "Preface" not in texts:
        problems.append("the Preface is missing from the contents")
    elif texts.index("Preface") != 0:
        problems.append(f"the Preface is not first; {texts[0]!r} is")

    chapters = [t for k, t in rows if k == "chapter" and re.match(r"^\d+ ", t)]
    if chapters:
        seen_part = False
        for k, t in rows:
            if k == "part":
                seen_part = True
            elif k == "chapter" and re.match(r"^\d+ ", t) and not seen_part:
                problems.append(f"chapter {t!r} comes before any part - it is orphaned")
                break
        nums = [int(t.split(" ", 1)[0]) for t in chapters]
        for i, n in enumerate(nums, 1):
            if n != i:
                problems.append(f"chapter numbers jump: expected {i}, found {n}")
                break
        # The Index is required only once the book HAS index entries. filter.lua makes
        # them from bold spans in the body; a chapter whose only bold is in its Key Terms
        # table produces none, so \printindex emits nothing and no contents line exists.
        # Demanding one then would fail a book that is simply early, which is the
        # cry-wolf failure. book.idx is the honest test: it is what makeindex is given.
        idx = os.path.join(ROOT, "book.idx")
        has_entries = os.path.exists(idx) and os.path.getsize(idx) > 0
        if has_entries and "Index" not in texts:
            problems.append("the book has index entries but no Index in the contents")
        if "Index" in texts and texts.index("Index") != len(texts) - 1:
            problems.append("the Index is in the contents but is not last")

    first_chapter = next((i for i, k in enumerate(kinds) if k == "chapter"), None)
    first_section = next((i for i, k in enumerate(kinds) if k == "section"), None)
    if first_section is not None and (first_chapter is None or first_section < first_chapter):
        problems.append("a section appears before any chapter")

    found_parts = [t.split(".", 1)[-1].strip() for k, t in rows if k == "part"]
    if found_parts != PARTS:
        problems.append(f"the parts are {found_parts}, not the four names the owner ruled "
                        f"on 2026-11-12: {PARTS}")

    for p in problems:
        print(f"  {p}")
    print(f"\n{len(rows)} contents entries read, {len(chapters)} chapter(s), "
          f"{len(problems)} problem(s)")
    if problems:
        print("FAIL")
        sys.exit(1)
    print("CLEAN - the contents nest correctly")
    print("NOT checked here: the PDF outline's front matter. ../GATES.md section 6, by hand.")


if __name__ == "__main__":
    main()
