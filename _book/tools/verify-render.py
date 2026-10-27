#!/usr/bin/env python3
"""verify-render.py - catch Markdown that renders wrong on the PAGE.

Ported from the French book, where every check below was earned by a shipped defect
and no other gate caught any of them. 0 overfull boxes, 0 missing glyphs and a clean
voice gate all pass a chapter whose practice items collapsed into one paragraph.

Checks:
  1. Consecutive BOLD item markers (**A1.**) with no blank line - these are paragraphs,
     not list syntax, so two non-blank lines become ONE paragraph and the items collapse.
     A real "1. " marker is a list and is left alone: matching it fired on every Review
     Questions block, which was a fault in this gate and not in the chapter.
  2. A table row followed directly by text - the row absorbs it.
  3. A heading with no blank line after it.
  4. Orphaned table rows: a run of `|...|` with no `|---|` as its second line. A note
     inserted INSIDE a table splits it, and every row after the split renders as
     literal text with visible pipes. Check 2 cannot see it, because a blank line
     follows the row and `>` is exempt.
  5. Unbalanced backticks on a line. A code span cannot cross a line break, so an odd
     count means the span never closes and the rest of the line renders as code.
  8. A ```text block line wider than 64 characters.
  7. A blockquote starting directly under ordinary text mid-sentence - usually the
     remains of an edited-away callout.
  6. Unbalanced maths delimiters. This book writes maths as raw LaTeX spans
     (`\\(x\\)`{=latex}) and fenced blocks (```{=latex}). An unclosed \\( swallows the
     rest of the line into maths mode; an unclosed raw fence swallows the chapter.

Usage: python3 tools/verify-render.py [FILE ...]
"""
import glob, os, re, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Bold paragraph markers only - **A1.**, **3.** - which are NOT list syntax and so do
# collapse into one paragraph. A real ordered-list marker ("1. ") makes a tight
# \begin{enumerate} and is correct; matching it here was a false positive that fired on
# every Review Questions block in chapter 1. Verified against the generated .tex.
ITEM  = re.compile(r"^\*\*[A-Z]?\d+[.)]\*\*")
ROW   = re.compile(r"^\s*\|.*\|\s*$")
DELIM = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
HEAD  = re.compile(r"^#{1,6}\s")


def check(path):
    out, fence = [], False
    lines = open(path, encoding="utf-8").read().split("\n")
    for i, ln in enumerate(lines):
        stripped = ln.lstrip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if ITEM.match(ln) and ITEM.match(nxt):
            out.append((i + 1, "items run together into one paragraph", ln[:60]))
        elif ROW.match(ln) and nxt.strip() and not ROW.match(nxt) and not nxt.startswith(("#", ">", "<")):
            out.append((i + 1, "table row followed directly by text - the row absorbs it", ln[:60]))
        elif HEAD.match(ln) and nxt.strip():
            out.append((i + 1, "heading with no blank line after it", ln[:60]))
        if ln.count("`") % 2:
            out.append((i + 1, "unbalanced backticks - a code span never closes", ln[:60]))
        if ln.count("\\(") != ln.count("\\)"):
            out.append((i + 1, "unbalanced \\( \\) - maths mode never closes", ln[:60]))
        # 7. A '>' line directly under ordinary text. A blockquote can interrupt a
        # paragraph, so the paragraph ends there and the rest becomes a quote - which is
        # what an edited-away callout leaves behind. It split a sentence in chapter 2 and
        # every other gate passed it.
        if (nxt.lstrip().startswith(">") and ln.strip() and not ln.lstrip().startswith((">", "#", "|", "-", "*"))
                and not ln.rstrip().endswith((":", "."))):
            out.append((i + 1, "text runs straight into a blockquote - the paragraph ends "
                               "here and the rest renders as a quote", ln[-58:]))

    # 8. BOOK-GUIDE section 8: a ```text block is at most 64 characters wide, so it never
    # runs into the margin. Nothing checked it, and chapters 1 and 4 both drifted past it.
    fence8, lang = False, ""
    for i, ln in enumerate(lines):
        st = ln.lstrip()
        if st.startswith("```"):
            lang = st[3:].strip() if not fence8 else ""
            fence8 = not fence8
            continue
        if fence8 and lang == "text" and len(ln) > 64:
            out.append((i + 1, f"text block line is {len(ln)} characters - the limit is 64",
                        ln[:60]))

    if fence:
        out.append((0, "the file ends inside a code fence - one never closes", ""))

    fence, i = False, 0
    while i < len(lines):
        if lines[i].lstrip().startswith("```"):
            fence = not fence
            i += 1
            continue
        if fence or not ROW.match(lines[i]):
            i += 1
            continue
        start = i
        while i < len(lines) and ROW.match(lines[i]):
            i += 1
        run = lines[start:i]
        if not (len(run) >= 2 and DELIM.match(run[1])):
            out.append((start + 1, "orphaned table rows - no |---| delimiter, renders as "
                                   "literal text with pipes", run[0][:60]))
    return out


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md")))
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    total = 0
    for f in files:
        for ln, why, txt in check(f):
            total += 1
            print(f"{os.path.basename(f)}:{ln}  {why}\n      {txt}")
    print(f"\n{len(files)} file(s), {total} finding(s)")
    print("CLEAN - renders as written" if not total else "FAIL")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
