#!/usr/bin/env python3
"""verify-record.py - the checklist gate: complete, evidenced, fresh, and in order.

Every chapter in markdown/ must have a record in records/ that is fully ticked, carries
both review verdicts, and whose sha256 still matches the chapter. A record written after
the chapter, or a chapter edited after its record, both fail.

Why a gate and not a habit: the French project's chapters 1-19 were built with the
checklist as prose. Prose is what gets skipped.

Usage: python3 tools/verify-record.py
"""
import glob, hashlib, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _absolutes():
    """Import verify-absolutes.py by path: its name has a hyphen, so `import` cannot."""
    spec = importlib.util.spec_from_file_location(
        "verify_absolutes", os.path.join(ROOT, "tools", "verify-absolutes.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ABS = _absolutes()

EDITS = os.path.join(ROOT, "records", "EDITS.log")


def edited_between(begun, reviewed):
    """Files tools/patch.py edited between two ISO timestamps. Form, not judgement:
    it says WHICH files to read, never whether they were read well."""
    if not os.path.exists(EDITS):
        return set()
    out = set()
    for line in open(EDITS, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        when, path = parts[0], parts[1]
        if begun <= when <= reviewed:
            out.add(path)
    return out


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
                     "new-terms", "covers-misses", "files-read-back", "sha256",
                     "completeness-review", "fix-verification"):
            if not field(text, name):
                problems.append(f"{stem}: `{name}:` is empty")
        begun, written, reviewed = (field(text, k) for k in ("begun", "written", "reviewed"))
        if begun and written and reviewed and not (begun <= written <= reviewed):
            problems.append(f"{stem}: stages out of order ({begun} / {written} / {reviewed})")
        # An `amended:` field is how a closed chapter records a later change
        # (tools/chapter.py amend). Each entry must be dated and reasoned, and
        # dated at or after the review it comes after - otherwise the field is
        # decoration and a re-hash can hide behind it.
        if re.search(r"(?m)^amended:", text):
            entries = re.findall(r"(?m)^  - (\S+): (.+)$", text)
            block = re.search(r"(?m)^amended:(.*(?:\n  - .*)*)", text).group(1)
            if not entries:
                problems.append(f"{stem}: `amended:` has no dated entries")
            if len([l for l in block.splitlines() if l.strip()]) != len(entries):
                problems.append(f"{stem}: `amended:` has a line that is not "
                                f"'  - <timestamp>: <reason>'")
            for when, why in entries:
                if len(why.strip()) < 15:
                    problems.append(f"{stem}: amendment {when} has no real reason")
                if reviewed and when < reviewed:
                    problems.append(f"{stem}: amendment {when} predates "
                                    f"`reviewed:` ({reviewed})")

        # [2026-11-13] The coupling the finished book only DESCRIBED. Its
        # verify-absolutes.py said this gate fails when the numbers disagree; this gate
        # only checked the field was non-empty, so the number on the record was a
        # statement and not a measurement. Here it is a measurement.
        said = field(text, "absolutes")
        if said:
            m = re.match(r"(\d+)", said.strip())
            if not m:
                problems.append(f"{stem}: `absolutes:` must START with the number tested, "
                                f"not {said[:30]!r}")
            else:
                real = ABS.count(ch)
                if int(m.group(1)) != real:
                    problems.append(f"{stem}: record says absolutes: {m.group(1)}, "
                                    f"the gate counts {real}")

        # [STATED 2026-11-14] Every file tools/patch.py touched while this chapter was
        # open must be named in `files-read-back:`. The failure this catches is real and
        # recent: on 2026-11-13 a span of several files was removed by computing two
        # offsets and splicing, without reading what sat between them, and the only
        # verification afterwards was a grep for the words that had been removed. Three
        # false statements survived that in GATES.md alone. A grep checks form. Only
        # reading checks what a removal left behind.
        begun_s, reviewed_s = field(text, "begun"), field(text, "reviewed")
        if begun_s and reviewed_s:
            touched = edited_between(begun_s, reviewed_s)
            named = field(text, "files-read-back")
            for f in sorted(touched):
                if f not in named:
                    problems.append(f"{stem}: patch.py edited {f} while this chapter was "
                                    f"open, and `files-read-back:` does not name it")

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
