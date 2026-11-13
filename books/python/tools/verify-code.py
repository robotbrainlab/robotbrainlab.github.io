#!/usr/bin/env python3
"""verify-code.py - the book's code runs, and prints what the book says it prints.

This is the gate the finished book never needed and this one cannot do without.

A snippet that does not run, or an output typed from memory, is the commonest way a
programming book is wrong. The last digit is exactly where a reader looks:

    >>> 0.1 + 0.2
    0.30000000000000004

WHAT IT RUNS, and it is deliberately narrow (the verify-arithmetic lesson: a gate that
cries wolf is a gate nobody reads):

  1. A ```python block that contains a `>>> ` prompt is a doctest. It is RUN, and every
     printed line must match. This is where the book makes its claims about what Python
     prints, so this is where a machine is worth having.
  2. Every other ```python block is COMPILED, never executed. A block can open a file,
     call a service or start a thread; running those is the lab's job, not a gate's.
     Compiling still catches the commonest defect in a typed-out sample: it is not valid
     Python.
  3. ```bash and the rest are not touched at all.

  Blocks within one chapter share a namespace, in document order, because that is how a
  reader meets them: a class defined in block 3 is still there in block 7.

HOW TO OPT OUT of running a block, when the output genuinely cannot be reproduced - a
timing, a path, a random value:

    ```python {.norun}

filter.lua reads the FIRST class, so the block is still highlighted as Python. Say in the
chapter why the output cannot be reproduced; an unexplained .norun is a defect a review
should catch.

Usage:
    python3 tools/verify-code.py                     # every chapter
    python3 tools/verify-code.py markdown/02-*.md    # one
"""
import doctest, glob, io, os, re, sys, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^```+\s*([^\s{]*)\s*(\{[^}]*\})?\s*$")


def blocks(path):
    """(start line, language, attributes, text) for every fenced block."""
    out, cur, lang, attrs, start = [], None, "", "", 0
    for i, ln in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        m = FENCE.match(ln.strip()) if ln.lstrip().startswith("```") else None
        if m and cur is None:
            lang, attrs, cur, start = (m.group(1) or "").lower(), m.group(2) or "", [], i
            continue
        if ln.lstrip().startswith("```") and cur is not None:
            out.append((start, lang, attrs, "\n".join(cur)))
            cur = None
            continue
        if cur is not None:
            cur.append(ln)
    if cur is not None:
        out.append((start, lang, attrs, "\n".join(cur)))
    return out


def check(path):
    """(problems, ran, compiled, skipped) for one chapter."""
    problems, ran, compiled, skipped = [], 0, 0, 0
    name = os.path.basename(path)
    shared = {"__name__": "__chapter__"}
    parser = doctest.DocTestParser()
    for start, lang, attrs, text in blocks(path):
        if lang not in ("python", "py", "python3"):
            continue
        if ".norun" in attrs:
            skipped += 1
            continue
        if ">>>" in text:
            try:
                test = parser.get_doctest(text + "\n", shared, name, path, start)
            except ValueError as e:
                problems.append(f"{name}:{start}  not a readable doctest: {e}")
                continue
            if not test.examples:
                problems.append(f"{name}:{start}  has a >>> prompt but no example to run")
                continue
            out = io.StringIO()
            runner = doctest.DocTestRunner(verbose=False,
                                           optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
            try:
                runner.run(test, out=out.write)
            except Exception:
                problems.append(f"{name}:{start}  raised while running:\n"
                                + "      " + traceback.format_exc().strip().replace("\n", "\n      "))
                continue
            ran += 1
            if runner.failures:
                detail = out.getvalue().strip().replace("\n", "\n      ")
                problems.append(f"{name}:{start}  the book prints something this code does "
                                f"not:\n      {detail}")
        else:
            try:
                compile(text, f"{name}:{start}", "exec")
                compiled += 1
            except SyntaxError as e:
                problems.append(f"{name}:{start}  is not valid Python: line {e.lineno}, {e.msg}")
    return problems, ran, compiled, skipped


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md")))
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    if not files:
        print("VACUOUS - no Markdown to read. This gate checked NOTHING.")
        sys.exit(2)
    allp, ran, comp, skip = [], 0, 0, 0
    for f in files:
        p, r, c, s = check(f)
        allp += p
        ran += r
        comp += c
        skip += s
    for p in allp:
        print(f"  {p}")
    print(f"\n{len(files)} file(s) read, {ran} doctest block(s) run, "
          f"{comp} block(s) compiled, {skip} marked .norun, {len(allp)} problem(s)")
    if allp:
        print("FAIL - run it and paste what it actually printed. Never type the output.")
        sys.exit(1)
    if ran == 0 and comp == 0:
        print("CLEAN - but no Python was found to run. That is correct only before "
              "chapter 1 exists.")
        sys.exit(0)
    print("CLEAN - every runnable sample runs and prints what the book says")


if __name__ == "__main__":
    main()
