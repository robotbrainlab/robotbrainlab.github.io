#!/usr/bin/env python3
"""verify-inputs.py - every term a chapter builds on must already be in the book.

The French book's chapter 38 taught "take the nous form of the present" and ran that
rule on two verbs the book had never printed. Every gate passed it: the coverage gate
checks the sources against the book and never the book against itself, and nothing asks
whether an input a chapter depends on was ever given to the reader.

This lists every backticked or bolded term that appears in THIS chapter and in no earlier
one. It is a hint list, not a verdict: a chapter introducing a term for the first time is
normal and most hits are that. Triage each, and declare the count in the record.

It then runs a SECOND check that is a verdict, and exits 1 on a hit.

    Chapter 6 used "reranker" and "context window". Both appear ZERO times in chapters 1-5,
    and chapter 6 neither bolded nor defined either: it leaned on the reader knowing field
    jargon the book had not given them. This gate reported `new-terms: 0` and was right to,
    because chapter 6 contains no backticks at all -- the gate was structurally blind to
    plain prose. BOOK-GUIDE section 7: do not assume a term has been met before the book
    gives it.

The second check walks a curated list of the field's jargon (JARGON below) and flags any
of those terms a chapter uses WITHOUT bolding or defining it, when no earlier chapter
printed it. A term that must be used early on purpose goes in ALLOW, with the reason in
that chapter's record.

Usage: python3 tools/verify-inputs.py <chapter.md>   # list, `new-terms: N`, then the verdict
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = re.compile(r"`([^`\n]{2,40})`")
BOLD  = re.compile(r"\*\*([^*\n]{2,40})\*\*")

# ---------------------------------------------------------------- the jargon list
# Deliberately CURATED, not derived. The first version of this check built its vocabulary
# by splitting TOC.md on word boundaries: it caught the real defect and also flagged
# "combine", "choice", "minutes" and "pair" - 30 false positives on one chapter. A gate
# that cries wolf is a gate nobody reads (BOOK-GUIDE section 14.6, rule 1), so the list is
# written out by hand and grows when a chapter needs a term added.
#
# A term belongs here if a reader could not guess it from plain English and the book plans
# to teach it somewhere. Add the chapter that owns it in the comment, so the next person
# knows whether an early use is a loan or a mistake.
JARGON = [
    # Only terms with NO ordinary-English sense. The first list included "judge",
    # "attention", "trace" and "span"; chapter 2's "a second model judge it acceptable",
    # chapter 3's "approval given without real attention" and chapter 5's "a stack trace"
    # were all flagged as defects and none was one. A word that doubles as plain English
    # cannot be checked this way, so it is not in this list and this gate will never catch
    # it - the completeness review is what catches those.
    "tokeniser", "tokenizer", "context window", "embedding", "cosine similarity",
    "nearest neighbour", "top-k", "reranker", "rerank", "retrieval-augmented", "RAG",
    "self-attention", "residual stream", "logit", "softmax", "greedy decoding",
    "beam search", "constrained decoding", "few-shot", "zero-shot", "chain of thought",
    "fine-tuning", "fine-tune", "LoRA", "distillation", "quantisation", "quantization",
    "prompt injection", "jailbreak", "guardrail", "LLM-as-judge", "pass@k", "pass^k",
    "KV cache", "prefill", "agentic", "multi-agent", "orchestrator",
    "Model Context Protocol", "hallucination", "idempotent", "semantic search",
]
ALLOW = set()   # a term used early on purpose; argue the case in the chapter's record


def vocabulary():
    return set(JARGON)


def terms(path):
    text = open(path, encoding="utf-8").read()
    out = {m.group(1).strip() for m in TOKEN.finditer(text)}
    out |= {m.group(1).strip() for m in BOLD.finditer(text)}
    return out


def unescape(s):
    r"""Drop Markdown backslash-escapes before matching.

    A term the chapter must escape for pandoc is a different string from the one in
    JARGON: chapter 38 writes `pass\^k` in prose, because two bare carets in one
    paragraph become a superscript, and the Key Terms row carries the escape too. So
    the term was bolded AND defined and was reported BARE anyway - entry 56's bug in
    a second place. Unescape both sides and they agree.
    """
    return re.sub(r"\\([^A-Za-z0-9])", r"\1", s)


def used_bare(path, vocab, earlier_text):
    """Vocabulary words this chapter uses in prose, never bolded here, never printed before."""
    text = unescape(open(path, encoding="utf-8").read())
    defined = {unescape(t).lower() for t in terms(path)}
    hits = []
    for term in sorted(vocab):
        if term in ALLOW:
            continue
        pat = re.compile(r"\b" + re.escape(term) + r"(s|es)?\b", re.I)
        if not pat.search(text):
            continue
        # `defined` is lower-cased, so an upper-case entry in JARGON could never match it:
        # a chapter naming "RAG" or the "KV cache" in bold was reported BARE anyway. Fold the
        # term too, which is what the line above always meant to do.
        if any(term.lower() in d for d in defined):
            continue                       # the chapter introduces it properly
        if pat.search(earlier_text):
            continue                       # the reader has met it
        hits.append(term)
    return hits


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    n = int(re.match(r"(\d+)-", os.path.basename(path)).group(1))
    earlier = sorted(f for f in glob.glob(os.path.join(ROOT, "markdown", "*.md"))
                     if re.match(r"(\d+)-", os.path.basename(f))
                     and int(re.match(r"(\d+)-", os.path.basename(f)).group(1)) < n)
    seen = set()
    for f in earlier:
        seen |= terms(f)
    new = sorted(terms(path) - seen)
    for t in new:
        print(f"  {t}")
    print(f"\nnew-terms: {len(new)}  (earlier chapters read: {len(earlier)})")
    print("Triage each: introduced here on purpose, or built on without ever being given?")

    earlier_text = "".join(open(f, encoding="utf-8").read() for f in earlier)
    bare = used_bare(path, vocabulary(), earlier_text)
    print()
    if bare:
        for b in bare:
            print(f"  BARE  {b!r} - used in prose, not defined here, not printed earlier")
        print(f"\nbare-terms: {len(bare)}  FAIL")
        print("Give the term plainly, or use words the reader already has.")
        sys.exit(1)
    print("bare-terms: 0  CLEAN - no field jargon used before the book gives it")


if __name__ == "__main__":
    main()
