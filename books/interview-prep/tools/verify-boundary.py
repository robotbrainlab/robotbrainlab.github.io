#!/usr/bin/env python3
"""verify-boundary.py - the book teaches what the model computes, never the theory.

BOOK-GUIDE.md §6 draws an exact line: notation yes, machine-learning and deep-learning
theory no. The line has four decided boundary cases and two chapters that exist to name
what was left out. Everything else is a breach.

A gate is needed because the breach is always plausible. The honest explanation of why
normalisation is there IS numerical stability; the honest answer to why embeddings carry
meaning IS representation learning. A writer reaching for the real reason does not feel
like a writer breaking a rule, which is exactly why memory is not a control here.

Exemptions live in tools/boundary-exemptions.tsv, keyed by chapter and term, each with
its reason. An undeclared hit fails the build.

Usage: python3 tools/verify-boundary.py [FILE ...]
"""
import csv, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN = [
    "backpropagation", "back-propagation", "backprop",
    "gradient descent", "gradient", "chain rule",
    "optimiser", "optimizer", "Adam", "AdamW", "learning rate schedule", "warmup",
    "initialisation", "initialization", "Xavier", "He init",
    "regularisation", "regularization", "dropout", "weight decay",
    "bias-variance", "bias–variance", "overfitting", "underfitting",
    "inductive bias", "scaling law", "Chinchilla",
    "convolutional", "recurrent neural", "LSTM", "GRU", "RNN", "CNN",
    "representation learning", "manifold", "loss landscape", "numerical stability",
    "why depth helps", "update rule", "preference objective",
]


def exemptions():
    path = os.path.join(ROOT, "tools", "boundary-exemptions.tsv")
    allowed = {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            allowed.setdefault(row["chapter"], set()).add(row["term"].lower())
    return allowed


def chapter_of(path):
    """A chapter's number, or an appendix's letter. Appendices used to all return "?", so one
    exemption would have covered every one of them at once."""
    base = os.path.basename(path)
    m = re.match(r"(\d+)-", base)
    if m:
        return str(int(m.group(1)))
    m = re.match(r"([A-Z])-", base)
    return m.group(1) if m else "?"


def check(path, allowed):
    ch = chapter_of(path)
    ok = allowed.get(ch, set())
    out, fence = [], False
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        for term in FORBIDDEN:
            if term.lower() in ok:
                continue
            if re.search(r"\b" + re.escape(term) + r"\b", ln, re.I):
                out.append((i, term, ln.strip()[:70]))
    return out


def main():
    allowed = exemptions()
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "markdown", "*.md")))
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    total = 0
    for f in files:
        for ln, term, txt in check(f, allowed):
            total += 1
            print(f"{os.path.basename(f)}:{ln}  theory outside the boundary: {term!r}\n      {txt}")
            print(f"      declare it in tools/boundary-exemptions.tsv with a reason, or cut it")
    print(f"\n{len(files)} file(s), {total} finding(s)")
    print("CLEAN - the boundary holds" if not total else "FAIL")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
