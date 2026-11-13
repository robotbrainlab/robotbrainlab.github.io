#!/usr/bin/env python3
"""patch.py - apply exact-match edits one at a time, writing after each.

Why: three batches of edits have now aborted on one mismatched string and discarded every
edit before it, because the write came after the loop. This applies each edit, writes
immediately, reports what matched and what did not, and exits non-zero if anything missed
-- so a mismatch costs one edit, not the batch.

[STATED 2026-11-14] THIS IS THE ONLY WAY TO EDIT A FILE IN THIS BOOK. See ../GATES.md
section 8. It takes the exact text to remove, never a position, so a span cannot be cut
without quoting it -- and quoting it means having read it. Every applied edit is appended
to records/EDITS.log, and verify-record.py reads that log: a file this tool touched while
a chapter was open must be named in that chapter's `files-read-back:` field.

    python3 tools/patch.py <file> <edits.json>

edits.json: [{"label": "...", "old": "...", "new": "...", "count": 1}, ...]
`count` is the number of occurrences expected; it defaults to 1.
"""
import datetime, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "records" / "EDITS.log"


def log(path, label, removed, added):
    """One line per applied edit. The gate reads this; do not edit it by hand."""
    LOG.parent.mkdir(parents=True, exist_ok=True)
    try:
        rel = path.resolve().relative_to(ROOT)
    except ValueError:
        rel = path.resolve()
    when = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"{when}\t{rel}\t{label}\t-{removed}\t+{added}\n")

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path = pathlib.Path(sys.argv[1])
    edits = json.loads(pathlib.Path(sys.argv[2]).read_text())
    missed = []
    for e in edits:
        label, old, new = e["label"], e["old"], e.get("new", "")
        want = e.get("count", 1)
        text = path.read_text()
        n = text.count(old)
        if n != want:
            missed.append(f"{label}: expected {want}, found {n}")
            print(f"  MISS  {label:<28} expected {want}, found {n}")
            continue
        path.write_text(text.replace(old, new))
        after = path.read_text().count(old)
        log(path, label, len(old) * n, len(new) * n)
        print(f"  ok    {label:<28} {n} -> {after}")
    if missed:
        print(f"\n{len(missed)} edit(s) did not apply:")
        for m in missed:
            print(f"  {m}")
        sys.exit(1)
    print(f"\nall edits applied, and logged to {LOG.relative_to(ROOT)}")
    print("NOW READ THE FILE. A removal you did not read is a removal you cannot judge.")

if __name__ == "__main__":
    main()
