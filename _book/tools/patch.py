#!/usr/bin/env python3
"""patch.py - apply exact-match edits one at a time, writing after each.

Why: three batches of edits have now aborted on one mismatched string and discarded every
edit before it, because the write came after the loop. This applies each edit, writes
immediately, reports what matched and what did not, and exits non-zero if anything missed
-- so a mismatch costs one edit, not the batch.

    python3 tools/patch.py <file> <edits.json>

edits.json: [{"label": "...", "old": "...", "new": "...", "count": 1}, ...]
`count` is the number of occurrences expected; it defaults to 1.
"""
import json, pathlib, sys

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
        print(f"  ok    {label:<28} {n} -> {after}")
    if missed:
        print(f"\n{len(missed)} edit(s) did not apply:")
        for m in missed:
            print(f"  {m}")
        sys.exit(1)
    print("\nall edits applied")

if __name__ == "__main__":
    main()
