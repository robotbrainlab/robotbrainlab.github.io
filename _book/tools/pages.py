#!/usr/bin/env python3
"""pages.py - each chapter's printed page range, read out of the built PDF.

    python3 tools/pages.py            # every chapter, with its TOC.md estimate
    python3 tools/pages.py 09         # one chapter

Why this exists. A chapter's length has been mis-measured twice by subtracting folios
by hand: chapter 5 was reported as 12 printed pages when it was 8, and chapter 8 as 15
when it was 12. Both times the pages counted into the chapter were the PART II, PART III,
PART IV and APPENDIX A opener pages sitting immediately after the last written chapter --
pages that move the moment the next chapter lands. The number then reached the record,
`README.md` and `HANDOVER.md`, where it read as a measurement.

So the rule is the same one `build-probe.sh` enforces for overfull boxes: do not count by
hand, and do not trust a count the build did not produce. A chapter ends where the next
opener begins, and only the PDF knows where that is.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "latex", "book.pdf")


def openers():
    """(pdf page, label) for every chapter, part and appendix opener, in order."""
    out = subprocess.run(["pdftotext", "-layout", PDF, "-"],
                         capture_output=True, text=True).stdout
    found = []
    for i, page in enumerate(out.split("\f"), 1):
        text = page.strip()
        if not text:
            continue
        head = text.splitlines()[0].strip()
        m = re.match(r"^(CHAPTER|APPENDIX)\s+(\S+)", head)
        if m:
            found.append((i, f"{m.group(1).title()} {m.group(2)}", m.group(2)))
        elif re.match(r"^PART\s", head):
            found.append((i, head, None))
    return found


def offset(pages):
    """Printed folio minus pdf page, taken from a running head."""
    out = subprocess.run(["pdftotext", "-layout", PDF, "-"],
                         capture_output=True, text=True).stdout.split("\f")
    for i, page in enumerate(out, 1):
        m = re.match(r"^\s*(\d{1,3})\s+Chapter\s", page.strip())
        if m:
            return int(m.group(1)) - i
    return 0


def estimates():
    """{chapter number: estimated pp} from TOC.md's tables."""
    est = {}
    path = os.path.join(ROOT, "TOC.md")
    for line in open(path, encoding="utf-8"):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 7:
            continue
        if re.fullmatch(r"\d+", cells[1]) and re.fullmatch(r"\d+", cells[-2]):
            est[int(cells[1])] = int(cells[-2])
    return est


def main():
    if not os.path.exists(PDF):
        sys.exit(f"no PDF at {PDF} - run `cd latex && make` first")
    found = openers()
    if not found:
        sys.exit("found no openers in the PDF - has the layout changed?")
    off = offset(found)
    est = estimates()
    want = sys.argv[1].lstrip("0") if len(sys.argv) > 1 else None

    rows = []
    for idx, (page, label, num) in enumerate(found):
        if num is None:                      # a part opener is not a chapter
            continue
        end = found[idx + 1][0] - 1 if idx + 1 < len(found) else None
        if end is None:
            continue                          # the last one runs into the back matter
        rows.append((num, page + off, end + off, end - page + 1))

    print(f"{'ch':>4}  {'printed':>9}  {'pp':>3}  {'est':>3}  {'of est':>6}")
    total = 0
    for num, first, last, count in rows:
        if want and num.lstrip("0") != want:
            continue
        e = est.get(int(num)) if num.isdigit() else None
        share = f"{round(100 * count / e)}%" if e else "-"
        print(f"{num:>4}  {first:>4}-{last:<4}  {count:>3}  {e if e else '-':>3}  {share:>6}")
        total += count
    if not want:
        print(f"\n{len(rows)} chapter(s), {total} printed pages")


if __name__ == "__main__":
    main()
