#!/usr/bin/env python3
"""chapter.py - the staged driver. Each stage refuses until the last one is evidenced.

    python3 tools/chapter.py begin    NN-slug
    python3 tools/chapter.py written  NN-slug
    python3 tools/chapter.py reviewed NN-slug

`begin` refuses once the chapter file exists, because a checklist ticked after the
writing protects nothing. `written` refuses until every box before it carries evidence.
`reviewed` refuses until both review verdicts are recorded, and writes the sha256 last,
so editing one character afterwards makes the record stale and fails the gate.

The French project built nineteen chapters with its checklist as prose and found that
prose is what gets skipped. This is the same checklist with a lock on it.
"""
import hashlib, os, re, shutil, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGES = ("begin", "written", "reviewed")


def paths(stem):
    return (os.path.join(ROOT, "markdown", f"{stem}.md"),
            os.path.join(ROOT, "records", f"{stem}.md"))


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def unticked(text, upto):
    """Unticked boxes in the sections at or before `upto`."""
    order = ["## Before writing", "## While writing", "## After writing"]
    end = len(text)
    if upto + 1 < len(order):
        nxt = text.find(order[upto + 1])
        if nxt != -1:
            end = nxt
    start = text.find(order[0])
    return re.findall(r"^- \[ \] (.+)$", text[start:end], re.M)


def thin(text, upto):
    """Boxes ticked with no evidence after them."""
    order = ["## Before writing", "## While writing", "## After writing"]
    end = len(text)
    if upto + 1 < len(order):
        nxt = text.find(order[upto + 1])
        if nxt != -1:
            end = nxt
    start = text.find(order[0])
    bad = []
    for line in re.findall(r"^- \[x\] (.+)$", text[start:end], re.M):
        if "—" not in line and " - " not in line:
            bad.append(line)
    return bad


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in STAGES:
        sys.exit(__doc__)
    stage, stem = sys.argv[1], sys.argv[2]
    chapter, record = paths(stem)

    if stage == "begin":
        if os.path.exists(chapter):
            sys.exit(f"REFUSED: {chapter} already exists. `begin` runs BEFORE the chapter.")
        if os.path.exists(record):
            sys.exit(f"REFUSED: {record} already exists.")
        os.makedirs(os.path.dirname(record), exist_ok=True)
        text = open(os.path.join(ROOT, "tools", "record-template.md"), encoding="utf-8").read()
        text = text.replace("NN-slug", stem).replace("# Chapter NN", f"# Chapter {stem}")
        text = text.replace("begun:", f"begun: {now()}")
        open(record, "w", encoding="utf-8").write(text)
        print(f"opened {record}\nRead the sources in full NOW, then write the chapter.")
        return

    if not os.path.exists(record):
        sys.exit(f"REFUSED: no record. Run `chapter.py begin {stem}` first.")
    text = open(record, encoding="utf-8").read()

    if stage == "written":
        if not os.path.exists(chapter):
            sys.exit(f"REFUSED: {chapter} does not exist yet.")
        miss = unticked(text, 1)
        if miss:
            sys.exit("REFUSED: unticked before/while writing:\n  - " + "\n  - ".join(miss))
        weak = thin(text, 1)
        if weak:
            sys.exit("REFUSED: ticked with no evidence:\n  - " + "\n  - ".join(weak))
        for field in ("sources", "non-scope", "absolutes", "new-terms"):
            if re.search(rf"^{field}:\s*$", text, re.M):
                sys.exit(f"REFUSED: `{field}:` is empty.")
        text = re.sub(r"^written:.*$", f"written: {now()}", text, flags=re.M)
        open(record, "w", encoding="utf-8").write(text)
        print("written recorded. Now the completeness review, then the fix-verification pass.")
        return

    # The stages are an order, not a checklist. `reviewed` used to pass with `written:`
    # empty, so the stage could be -- and twice was -- skipped entirely.
    if re.search(r"^written:\s*$", text, re.M):
        sys.exit(f"REFUSED: `written:` is empty. Run `chapter.py written {stem}` first.")

    # And refuse a FABRICATED `written:`. Checking only for emptiness let the field be filled
    # in by hand, which happened on chapters 2, 3, 5, 6 and 8 - and three of those hand-written
    # times were impossible: later than the `reviewed` stamp the driver had just written, or
    # earlier than `begun`. A record's whole job is to be evidence, and the hash covers the
    # chapter rather than the record, so nothing else catches an invented timestamp in range.
    # LEDGER-DEFECTS entry 19.
    stamps = {}
    for field in ("begun", "written"):
        m = re.search(rf"^{field}:\s*(\S+)", text, re.M)
        if m:
            try:
                stamps[field] = datetime.fromisoformat(m.group(1))
            except ValueError:
                sys.exit(f"REFUSED: `{field}:` is not an ISO timestamp: {m.group(1)!r}")
    if "begun" in stamps and "written" in stamps:
        if stamps["written"] < stamps["begun"]:
            sys.exit(f"REFUSED: `written:` ({stamps['written']}) is BEFORE `begun:` "
                     f"({stamps['begun']}). That did not happen. Run "
                     f"`chapter.py written {stem}` and let the clock write it.")
        if stamps["written"] > datetime.now(stamps["written"].tzinfo):
            sys.exit(f"REFUSED: `written:` ({stamps['written']}) is in the future. "
                     f"Run `chapter.py written {stem}`.")
    miss = unticked(text, 2)
    if miss:
        sys.exit("REFUSED: unticked after writing:\n  - " + "\n  - ".join(miss))
    for field in ("completeness-review", "fix-verification", "covers-misses"):
        if re.search(rf"^{field}:\s*$", text, re.M):
            sys.exit(f"REFUSED: `{field}:` is empty.")
    digest = hashlib.sha256(open(chapter, "rb").read()).hexdigest()
    text = re.sub(r"^reviewed:.*$", f"reviewed: {now()}", text, flags=re.M)
    text = re.sub(r"^sha256:.*$", f"sha256: {digest}", text, flags=re.M)
    open(record, "w", encoding="utf-8").write(text)
    print(f"reviewed recorded. sha256 {digest[:16]}…\nAny edit from here makes the record stale.")


if __name__ == "__main__":
    main()
