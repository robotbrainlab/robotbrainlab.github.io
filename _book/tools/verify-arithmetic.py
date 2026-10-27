#!/usr/bin/env python3
"""verify-arithmetic.py - evaluate every printed equation and check it holds.

Born 2026-10-27 from chapter 8. Six arithmetic errors shipped in a chapter whose whole
argument is "do it by hand and check", written by somebody who had run the body's numbers
through Python and then invented the lab's vectors while writing and never checked them. Three
of the six were printed equations that simply do not hold:

    7.389 + 2.718 + 1.105 = 11.213      (it is 11.212)
    7.389 / 11.213 = 0.659              (the divisor was the wrong total)
    3.742 x 4.243 = 15.875              (it is 15.877; 15.875 is the UNROUNDED product)

A machine should find those, not a reviewer. This finds exactly that class: a line, or a maths
span, that is nothing but arithmetic and an answer.

    python3 tools/verify-arithmetic.py                 # every chapter
    python3 tools/verify-arithmetic.py markdown/08.md  # one

**Deliberately narrow.** It only looks at statements that are PURE arithmetic end to end, so
`in 1,000 words x 1 unit per million = 0.0010 units` is skipped - it carries words, and
guessing at prose arithmetic is how a gate starts crying wolf (LEDGER-DEFECTS entry 18). It
will not catch a claim made in a sentence ("both come to 14"), which is what the completeness
review is for. It compares at the precision the answer was printed to, so writing 0.315 for
0.314934 passes and writing 0.316 does not.
"""
import ast, glob, operator, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}
# a pure-arithmetic chunk: digits, . , spaces and the operators. At least one operator.
PURE = re.compile(r"^[\d\s.,()+*/^x×-]+$")
HASOP = re.compile(r"[+*/^×]|(?<=[\d) ])x(?=[ \d(])|(?<=\d)-(?=\d)")
SPAN = re.compile(r"`\\\((.+?)\\\)`\{=latex\}")


def normalise(s):
    s = s.replace("×", "*").replace("^", "**").replace(",", "")
    s = re.sub(r"\\times|\\cdot", "*", s)
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"(?<=[\d)\s])x(?=[\s\d(])", "*", s)   # the book writes 3 x 4
    s = re.sub(r"\\sqrt\s*(\d+(?:\.\d+)?)", r"(\1)**0.5", s)
    return s.strip()


def ev(node):
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError("not a number")
        return node.value
    if isinstance(node, ast.BinOp):
        return OPS[type(node.op)](ev(node.left), ev(node.right))
    if isinstance(node, ast.UnaryOp):
        return OPS[type(node.op)](ev(node.operand))
    raise ValueError("unsupported")


def value(expr):
    """The number an arithmetic string evaluates to, or None if it is not pure arithmetic."""
    s = normalise(expr)
    if not s or not PURE.match(expr.replace("\\times", "x").replace("\\,", " ")):
        return None
    if not HASOP.search(expr):
        return None
    try:
        return float(ev(ast.parse(s, mode="eval").body))
    except Exception:
        return None


def decimals(s):
    m = re.search(r"\.(\d+)\s*$", s.strip().rstrip("."))
    return len(m.group(1)) if m else 0


def check_statement(raw, path, lineno, problems):
    """A chain like `a + b = c = d`: every pure-arithmetic part must agree."""
    parts = [p for p in raw.split("=") if p.strip()]
    if len(parts) < 2:
        return
    vals = []
    for p in parts:
        v = value(p)
        if v is None:
            # a bare number counts as a stated answer
            t = normalise(p)
            try:
                v = float(t)
            except Exception:
                v = None
        if v is not None:
            vals.append((p.strip(), v))
    if len(vals) < 2:
        return
    places = min(decimals(p) for p, _ in vals)
    rounded = {round(v, places) for _, v in vals}
    if len(rounded) > 1:
        shown = "  =  ".join(f"{p} [{v:.6g}]" for p, v in vals)
        problems.append(f"{os.path.basename(path)}:{lineno}  does not hold: {shown}")


def check(path):
    problems, inblock, n = [], False, 0
    for lineno, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.startswith("```"):
            inblock = not inblock
            continue
        if inblock:
            # Do NOT pre-filter the line with PURE here: PURE's character class has no "=",
            # so every equation in a text block failed the test and only maths spans were
            # ever checked. The gate reported CLEAN over a line it had not read.
            # check_statement does the deciding - it needs two evaluable parts or it returns.
            raw = line.rstrip("\n")
            if "=" in raw:
                n += 1
                check_statement(raw, path, lineno, problems)
        for m in SPAN.finditer(line):
            inner = m.group(1)
            if "=" in inner:
                n += 1
                check_statement(inner, path, lineno, problems)
    return problems, n


def main():
    files = sys.argv[1:] or sorted(f for f in glob.glob(os.path.join(ROOT, "markdown", "*.md"))
                                   if re.match(r"\d+-", os.path.basename(f)))
    allp, total = [], 0
    for f in files:
        p, n = check(f)
        allp += p
        total += n
    for p in allp:
        print(f"  {p}")
    print(f"\n{len(files)} file(s), {total} equation(s) checked, {len(allp)} problem(s)")
    if allp:
        print("FAIL - recompute it, or print the figure you actually divided by")
        sys.exit(1)
    print("CLEAN - every printed equation holds")


if __name__ == "__main__":
    main()
