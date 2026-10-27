#!/usr/bin/env python3
"""verify-record.py - the checklist gate: complete, evidenced, fresh, and in order.

Every chapter in markdown/ must have a record in records/ that is fully ticked, carries
both review verdicts, and whose sha256 still matches the chapter. A record written after
the chapter, or a chapter edited after its record, both fail.

Why a gate and not a habit: the French project's chapters 1-19 were built with the
checklist as prose. Prose is what gets skipped.

Usage: python3 tools/verify-record.py
"""
import glob, hashlib, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def field(text, name):
    # [^\S\n]* and not \s* : \s matches newlines, so an EMPTY field read the next
    # line's content and looked filled. That made "written:" report as "reviewed:" and
    # produced a spurious "stages out of order". LEDGER-DEFECTS entry 11, third instance.
    m = re.search(rf"^{name}:[^\S\n]*(.*)$", text, re.M)
    return (m.group(1).strip() if m else "")


def main():
    # A chapter is a NUMBERED markdown file. "_" drafts, the preface, and the generated
    # appendices are not chapters and have no hand-written record: Appendix C is produced by
    # tools/glossary.py and its correctness is that gate's job, not a checklist's. Before this
    # was explicit, enabling the glossary made this gate report "C-glossary: NO RECORD".
    chapters = sorted(f for f in glob.glob(os.path.join(ROOT, "markdown", "*.md"))
                      if re.match(r"\d+-", os.path.basename(f))
                      and not os.path.basename(f).startswith("00-"))
    problems = []
    for ch in chapters:
        stem = os.path.basename(ch)[:-3]
        rec = os.path.join(ROOT, "records", f"{stem}.md")
        if not os.path.exists(rec):
            problems.append(f"{stem}: NO RECORD")
            continue
        text = open(rec, encoding="utf-8").read()
        open_boxes = re.findall(r"^- \[ \] (.+)$", text, re.M)
        if open_boxes:
            problems.append(f"{stem}: {len(open_boxes)} unticked box(es), first: {open_boxes[0][:60]}")
        for name in ("sources", "non-scope", "begun", "written", "reviewed", "absolutes",
                     "new-terms", "covers-misses", "sha256",
                     "completeness-review", "fix-verification"):
            if not field(text, name):
                problems.append(f"{stem}: `{name}:` is empty")
        begun, written, reviewed = (field(text, k) for k in ("begun", "written", "reviewed"))
        if begun and written and reviewed and not (begun <= written <= reviewed):
            problems.append(f"{stem}: stages out of order ({begun} / {written} / {reviewed})")
        want = field(text, "sha256")
        if want:
            got = hashlib.sha256(open(ch, "rb").read()).hexdigest()
            if got != want:
                problems.append(f"{stem}: STALE - the chapter changed after it was reviewed")
    for p in problems:
        print(f"  {p}")
    print(f"\n{len(chapters)} chapter(s), {len(problems)} problem(s)")
    if not chapters:
        # Say so out loud. A gate that prints CLEAN over nothing is how the French
        # project's scope gate passed a whole 48-chapter build without ever running.
        print("VACUOUS - no chapters exist yet, so this gate checked nothing")
        sys.exit(0)
    print("CLEAN - every chapter recorded, evidenced and fresh" if not problems else "FAIL")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
