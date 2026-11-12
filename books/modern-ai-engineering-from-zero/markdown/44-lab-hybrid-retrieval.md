# Lab: Hybrid Retrieval With a Reranker, Measured

Chapter 26 built BM25 from zero, combined two rankings whose scores cannot be compared, and
computed three measures — all on eight invented documents with stipulated cosines. Its last
section tried to say whether hybrid retrieval beat dense retrieval, and ended by refusing to:
*that is not a verdict on hybrid retrieval, it is a demonstration that you cannot get a verdict
this way.* This chapter builds the way that can. Forty real documents, real embeddings, the graded
key the book ships, and chapter 20 deciding which differences are real — and on chapter 26's own
question it arrives, honestly, at the same answer chapter 26 gave.

*The problem.* I want to stop guessing which retrieval is better.

*The question.* With a key, two measures and eight queries, which of these differences can you
actually establish — and what does the honest answer cost?

> **Note:** As in chapters 40 to 43, the `text` blocks are one real run. The BM25 half is
> arithmetic and reproduces exactly. The dense half rests on embeddings, which chapter 43 found
> drift in their third or fourth decimal, so a cosine here can move in its last printed digit —
> and it uses `text-embedding-3-small`, the smaller of chapter 43's two and the one that puts the
> toaster first on `q4`. The rankings and the measures reproduced on two runs. **The reranker is
> the part to expect to differ**: it is a chat model, and across three runs its point estimates,
> its ceilings and both of its intervals held while its distinct-score counts and tie ranges moved, and step 5's whole point is that its *scale* decides how much of its output is an
> ordering at all — so if your distinct-score counts differ from the table, your tie ranges and
> point estimates will too, and the tie range is the figure to read.

> **Note:** What this lab costs before you run it. It embeds the forty documents once and the
> eight queries a few times — a fraction of a penny — and then makes [**80 joint scorings**]{.noindex} in step
> 5 — and 80 more, because step 5 runs twice on two scales. Each sends a whole document, which
> makes it the expensive part by more than an order of magnitude and still about a penny. The
> figure to watch is the product that step 5 is about: queries times candidates times scales. An
> hour, most of it reading.

## Step 1: The Key, and What It Will Support

Make a folder, put the corpus in it, and set the key:

```text
  mkdir -p ~/sandbox/ch44 && cd ~/sandbox/ch44
  python3 -m venv .venv && source .venv/bin/activate
  cp -r <where you unpacked the book's labs>/corpus .
  export OPENAI_API_KEY="sk-..."
```

Everything in this lab is measured against one file, so read the file first. A key's shape
decides which measures mean anything, and chapter 26 attaches a warning to each measure that is
really a warning about the key.

```python
"""The eight queries, the graded key, and what it will support.

Chapter 26 built the measures on a key it invented. This is the one
the book ships, read before anything is measured against it, because
a key's shape decides which measures mean anything.
"""

import os
import pathlib

ROOT = pathlib.Path(os.environ.get("CORPUS", "corpus"))
DOCS = ROOT / "docs"


def rows(name):
    text = (ROOT / name).read_text().strip().split("\n")
    return [tuple(l.split("\t")) for l in text[1:]]


def queries():
    return dict(rows("queries.tsv"))


def key():
    """{query_id: {doc_id: grade}}, every pair, zeros included."""
    out = {}
    for qid, doc, grade in rows("judgements.tsv"):
        out.setdefault(qid, {})[doc] = int(grade)
    return out


def ids():
    return sorted(p.stem for p in DOCS.glob("*.md"))


if __name__ == "__main__":
    qs, k, docs = queries(), key(), ids()
    graded = sum(len(v) for v in k.values())
    print(f"  {len(qs)} queries, {len(docs)} documents,"
          f" {graded} judged pairs")
    print(f"  every query judged against every document:"
          f" {graded == len(qs) * len(docs)}\n")

    scale = sorted({g for v in k.values() for g in v.values()})
    print(f"  grades present: {scale}")
    for g in scale:
        n = sum(1 for v in k.values() for x in v.values() if x == g)
        print(f"    {g}  {n:3d} pairs")

    print("\n  relevant documents per query, and how many are the top grade:")
    top = max(scale)
    for qid in sorted(k):
        rel = [d for d, g in k[qid].items() if g > 0]
        best = [d for d, g in k[qid].items() if g == top]
        print(f"    {qid}  {len(rel)} relevant,"
              f" {len(best)} at grade {top}   {qs[qid][:28]}")
```

```text
  8 queries, 40 documents, 320 judged pairs
  every query judged against every document: True

  grades present: [0, 1, 2]
    0  286 pairs
    1   25 pairs
    2    9 pairs

  relevant documents per query, and how many are the top grade:
    q1  8 relevant, 3 at grade 2   How long do I have to return
    q2  4 relevant, 1 at grade 2   Why is my refund taking so l
    q3  3 relevant, 0 at grade 2   How much does delivery cost 
    q4  3 relevant, 1 at grade 2   What is HL-2208?
    q5  3 relevant, 0 at grade 2   Is a refund 14 days or 30 da
    q6  4 relevant, 1 at grade 2   My parcel arrived damaged. W
    q7  4 relevant, 1 at grade 2   What does Harbour Plus inclu
    q8  5 relevant, 2 at grade 2   Can I return a clearance ite
```

**The second line is the one that changes what this chapter can claim.** Every query is judged
against every document: 320 pairs for 8 queries over 40 documents, with none missing. Chapter 26
says a recall figure is only ever recall against your key, because on a real collection nobody
knows the true denominator — finding it means judging every document against every query. Here
somebody did, so the *denominator* is complete, and that is a luxury of forty documents and not a
thing to expect twice. **It is not the same as the key being right.** The corpus `README.md` says
in terms that the grades are one person's and that recall against this file is recall against this
file; complete coverage removes one of those two limits and leaves the other where it was.

> **Warning:** The corpus declares what was *planted* in it, so that no lab reports as a finding
> something the corpus was built to contain — and four of its planted rows carry this chapter. One
> names this chapter by number: a near-duplicate pair differing in one clause, for *fusion and
> reranking on near-ties*. Another is the identifier that similarity cannot match, which is step
> 2's subject. And the two queries below with no top-grade document are the planted split answer
> and the planted contradiction, which is *why* their best documents are partial. None of that is
> a discovery. What is not planted is every number in steps 4, 5 and 6.

**The grades are 0, 1 and 2, and chapter 26's table has four rows.** Its scale is 3 for *answers
it on its own*, 2 for *useful but the reader has to work*, 1 for *related and not an answer*, 0
for *not relevant*. This key has two non-zero points rather than three, and the mapping is a
*merge* rather than a deletion: its 2 is chapter 26's 3, and its 1 covers both of chapter 26's 2
and 1, since the `README.md` defines grade 1 as naming the right policy without the figure *or
holding half of a two-part answer* — which is chapter 26's 2. That matters in one specific way:
nDCG weighs grades, so a scale with fewer rungs can express fewer distinctions, and the ideal
ranking this chapter divides by is built from a flatter set of grades than chapter 26's was.

**And two queries have no top-grade document at all.** q3 and q5 are answered by grade-1
documents only — *related, and not an answer* — so their ideal DCG is built entirely from
partial answers. A perfect ranking on those two queries still means putting the least-bad
documents first, and an nDCG of 1.000 there is a weaker claim than an nDCG of 1.000 on q1.

> **Tip:** This is five minutes of reading a file and it is the cheapest insurance in the chapter.
> Three things in step 4 would be misread without it: recall means something unusually
> strong here, nDCG means something slightly weaker, and two of the eight queries are not asking
> what the other six are asking.

## Step 2: BM25 Over Forty Real Documents

Chapter 26's formula, unchanged, on a collection that was not built for it.

```python
"""BM25 over the shipped corpus, chapter 26's formula unchanged.

Chapter 26 built this on eight invented documents. The formula here
is the same, including the +1 inside the logarithm that stops the IDF
going negative, and k1 and b at the conventional 1.5 and 0.75. What
is new is the collection: forty real documents, and a term list
built by splitting on anything that is not a letter or a digit,
because the corpus has hyphens, full stops and markdown in it.
"""

import math
import re

from key import DOCS, ids

WORD = re.compile(r"[a-z0-9][a-z0-9.\-]*")


def terms(text):
    """Chapter 26's unit: not the model's token. Lower-cased, split on
    non-word characters, and hyphens and dots KEPT inside a run so
    that `hl-2208-f` and `9.50` survive as single terms."""
    return WORD.findall(text.lower())


def load():
    return {i: terms((DOCS / f"{i}.md").read_text()) for i in ids()}


BODY = load()
N = len(BODY)
AVGDL = sum(len(t) for t in BODY.values()) / N
DF = {}
for _toks in BODY.values():
    for _t in set(_toks):
        DF[_t] = DF.get(_t, 0) + 1


def idf(term):
    n = DF.get(term, 0)
    return math.log((N - n + 0.5) / (n + 0.5) + 1)


def bm25(query, doc, k1=1.5, b=0.75):
    toks = BODY[doc]
    dl = len(toks)
    total = 0.0
    for term in terms(query):
        tf = toks.count(term)
        if tf == 0:
            continue
        norm = tf + k1 * (1 - b + b * dl / AVGDL)
        total += idf(term) * tf * (k1 + 1) / norm
    return total


def ranked(query):
    """Only documents that matched a term. An inverted index never
    returns a document holding none of them, and chapter 26's Warning
    is that fusing a tail of zeros hands arbitrary positions a vote."""
    hit = {d: bm25(query, d) for d in BODY}
    hit = {d: s for d, s in hit.items() if s > 0}
    return sorted(hit, key=lambda d: -hit[d]), hit


if __name__ == "__main__":
    from key import queries
    print(f"  {N} documents, average length {AVGDL:.1f} terms,"
          f" {len(DF)} distinct terms\n")
    print("  what one term is worth here:")
    for t in ("the", "refund", "delivery", "hl-2208-f", "pa20"):
        print(f"    {t:10s} in {DF.get(t, 0):2d} of {N}"
              f"   idf {idf(t):.4f}")
    print("\n  how many documents each query matches at all:\n")
    for qid, q in sorted(queries().items()):
        order, scores = ranked(q)
        print(f"    {qid}  {len(order):2d} of {N} matched"
              f"   top: {order[0] if order else '-'}")
```

```text
  40 documents, average length 174.3 terms, 1430 distinct terms

  what one term is worth here:
    the        in 40 of 40   idf 0.0123
    refund     in 15 of 40   idf 0.9727
    delivery   in 26 of 40   idf 0.4364
    hl-2208-f  in  1 of 40   idf 3.3081
    pa20       in  1 of 40   idf 3.3081

  how many documents each query matches at all:

    q1  37 of 40 matched   top: refunds-faq
    q2  40 of 40 matched   top: where-is-my-refund
    q3  40 of 40 matched   top: delivery-exceptions
    q4  39 of 40 matched   top: product-kettle-hl-2208
    q5  40 of 40 matched   top: how-to-start-a-return
    q6  29 of 40 matched   top: missing-item-in-a-parcel
    q7  35 of 40 matched   top: plan-harbour-plus
    q8  39 of 40 matched   top: refunds-faq
```

**The term list is the one decision this program makes that chapter 26 did not have to.** Its
eight documents were lower-cased and split on whitespace, and that was the whole of the
tokenising. Forty real documents have hyphens, full stops, markdown and product codes in them, so
splitting on whitespace alone would leave `` `HL-2208-F` `` glued to a backtick and `9.50` next to
a comma. The pattern here keeps hyphens and dots *inside* a run and breaks on everything else, so
`hl-2208-f` and `9.50` survive as single terms — which is the whole reason BM25 can see an
identifier at all.

**And it costs something, which is the half of this to insist on.** Keeping a dot inside a run
keeps a *sentence-final* dot too: 253 of the corpus's 1,430 distinct terms end in a full stop. The
damage is visible on `q6`, which tokenises to `damaged.` — a term no document holds, where
`damaged` is in four of them. The one discriminating word in *My parcel arrived damaged* is thrown
away before BM25 sees it, and that is why `q6` matches 29 of 40 where the others match 35 or more.
Stripping a trailing dot is one line, and it is left undone here so that the cost is visible:
chapter 26's warning is that a term is whatever the indexer decided, and that decision is upstream
of every number below.

**Read the IDF column and then read `the`.** It is in all forty documents and worth 0.0123 —
close enough to nothing that a query containing it is barely affected, which is the inverse doing
its job. And `hl-2208-f` is in one document of forty and worth 3.3081, two hundred and seventy
times as much. Chapter 26's classic IDF would have made `the` *negative* here, since it is in more
than half the collection; the `+1` inside the logarithm is what keeps it a small positive number
instead.

**Now the matched counts, because they are a trap this corpus sets and chapter 26's eight
documents could not.** Most queries match 37, 39 or 40 of the forty documents. Not because the
corpus is about everything, but because a query like *How much does delivery cost to the Scottish
Highlands?* contains *the* and *to*, and `the` is in all forty documents while `to` is in
thirty-three. A document matching only those words scores almost nothing — and it still gets a
*position*. Chapter 26's Warning is exactly this:
feeding that tail into a fusion hands arbitrary positions a vote they have not earned, and step 3
is where it would happen.

**And `q4` is the first real result, though not for the reason it looks like.** The query *What is
HL-2208?* puts the kettle's own page first, where chapter 43 put the *toaster* through the smaller
of its two embedding models — a cosine has no way to represent the difference between a document's
subject and a sentence inside it, and the toaster's page mentions the kettle in passing. So BM25
wins here. *But not categorically*, and the difference matters. `hl-2208` is in *two* of the
forty documents, at an IDF of 2.7973: the toaster's page holds the string too, which chapter 43
says in as many words. (Chapter 43 counted *three* for the same string, and both counts are right:
it searched for `HL-2208` as written, which also matches the `HL-2208-K` inside
`sku-conventions`, while this chapter's term list has split that into a separate term. A term is whatever the indexer
decided, again.) So the kettle wins 4.5825 to 3.5430 on saturating term frequency
alone — it says the code twice — and it wins *despite* being the longer page, 117 terms against
102, which the length normalisation counts against it: at equal term frequency the toaster would
win. It does not win because it holds a term the other lacks. Chapter 26's categorical case was a document that *did not hold the term at all*, and
the example of that on this corpus is `hl-2208-f`, in one document at an IDF of 3.3081, which is
chapter 43's identifier query rather than one of this key's eight.

## Step 3: Dense, and Fusing Two Scales That Do Not Compare

The dense half is chapter 43's, kept here so this chapter stands alone.

```python
"""Dense retrieval over the same forty documents.

Chapter 43 embedded this corpus and cached the vectors; this is the
same thing, kept here so the chapter stands alone. One model, both
sides, which chapter 26 is careful to say is a bi-encoder and NOT an
escape from chapter 25's symmetry - the escape is step 5's.
"""

import json
import math
import os
import pathlib
import urllib.request

from key import DOCS, ids

MODEL = "text-embedding-3-small"
URL = "https://api.openai.com/v1/embeddings"
CACHE = pathlib.Path("vectors.json")
TIMEOUT = 120


def embed(texts):
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    body = json.dumps({"model": MODEL, "input": texts}).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {k}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    rows = sorted(d["data"], key=lambda x: x["index"])
    return [x["embedding"] for x in rows], d["model"]


def vectors():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    docs = ids()
    vecs, served = embed([(DOCS / f"{i}.md").read_text() for i in docs])
    out = {"ids": docs, "model": served, "docs": vecs}
    CACHE.write_text(json.dumps(out))
    return out


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x*x for x in a))
                  * math.sqrt(sum(y*y for y in b)))


def ranked(query, cache=None):
    cache = cache or vectors()
    qv, _ = embed([query])
    qv = qv[0]
    scores = {d: cosine(qv, v) for d, v in zip(cache["ids"], cache["docs"])}
    return sorted(scores, key=lambda d: -scores[d]), scores


if __name__ == "__main__":
    from key import queries
    cache = vectors()
    print(f"  {len(cache['ids'])} documents, model {cache['model']},"
          f" {len(cache['docs'][0])} numbers each\n")
    print("  top document per query:\n")
    for qid, q in sorted(queries().items()):
        order, _ = ranked(q, cache)
        print(f"    {qid}  {order[0]}")
```

```text
  40 documents, model text-embedding-3-small, 1536 numbers each

  top document per query:

    q1  how-to-start-a-return
    q2  where-is-my-refund
    q3  delivery-exceptions
    q4  product-toaster-hl-2209
    q5  where-is-my-refund
    q6  damaged-on-arrival
    q7  plan-harbour-plus
    q8  returns-clearance
```

**One line of that is worth pausing on: `q4` returns the toaster.** The same query that BM25 got
right. Two methods, the same forty documents, and they disagree on the first result — which is the
disagreement this whole chapter exists to adjudicate rather than to argue about.

Now the fusion. Chapter 26 established why the two scores cannot be added: a BM25 score and a
cosine have no common unit, there is no principled scale to put them on, and any rescaling is a
weight you chose. Reciprocal rank fusion throws the scores away and keeps the positions.

```python
"""Reciprocal rank fusion, chapter 26's formula and its warning.

The warning is the whole of the care needed here: fuse the TOP of
each list, not the collection. On this corpus BM25 matches 37 or
more of the forty documents for most queries, because `the` is in
all forty - so a tail of near-zero scores would arrive with
positions it has not earned.
"""

K = 60
DEPTH = 10


def ranks(order, depth=DEPTH):
    return {d: place for place, d in enumerate(order[:depth], 1)}


def rrf(rank_lists, k=K):
    out = {}
    for rl in rank_lists:
        for doc, place in rl.items():
            out[doc] = out.get(doc, 0.0) + 1 / (k + place)
    return out


def fused_order(lex_order, dense_order, depth=DEPTH, k=K):
    """Returns (order, scores, ties) - ties being the fused values
    shared by more than one document, which chapter 26 shows RRF
    cannot break because it threw the scores away."""
    f = rrf([ranks(lex_order, depth), ranks(dense_order, depth)], k)
    order = sorted(f, key=lambda d: -f[d])
    seen = {}
    for d, v in f.items():
        seen.setdefault(round(v, 12), []).append(d)
    ties = {v: ds for v, ds in seen.items() if len(ds) > 1}
    return order, f, ties


if __name__ == "__main__":
    import dense
    import lexical
    from key import key, queries

    cache = dense.vectors()
    k = key()
    print(f"  fusing the top {DEPTH} of each list, k = {K}\n")
    print("  query  fused top 3                    ties")
    for qid, q in sorted(queries().items()):
        lex, _ = lexical.ranked(q)
        den, _ = dense.ranked(q, cache)
        order, scores, ties = fused_order(lex, den)
        n = sum(len(v) for v in ties.values())
        print(f"    {qid}   {' '.join(d[:9] for d in order[:3]):30s} {n}")

    print("\n  a tie only costs something when the documents in it")
    print("  have different grades AND it lands where the measure")
    print("  looks. Chapter 26: RRF cannot tell (1, 2) from (2, 1),")
    print("  because it threw the scores away.\n")
    costly = 0
    for qid, q in sorted(queries().items()):
        lex, _ = lexical.ranked(q)
        den, _ = dense.ranked(q, cache)
        order, scores, ties = fused_order(lex, den)
        for val, docs in sorted(ties.items(), reverse=True):
            grades = {k[qid].get(d, 0) for d in docs}
            inside = min(order.index(d) for d in docs) < 5
            if len(grades) > 1 and inside:
                costly += 1
                lr, dr = ranks(lex), ranks(den)
                print(f"    {qid}: {len(docs)} documents at {val:.6f},")
                print(f"         first of them at rank"
                      f" {min(order.index(d) for d in docs) + 1}")
                for d in docs:
                    print(f"      grade {k[qid].get(d, 0)}  {d[:22]:22s}"
                          f" lex {lr.get(d, '-')}, dense {dr.get(d, '-')}")
    print(f"\n  ties that straddle a grade inside the top 5: {costly}")
```

```text
  fusing the top 10 of each list, k = 60

  query  fused top 3                    ties
    q1   how-to-st refunds-f returns-c  6
    q2   where-is- refunds-f refund-to  2
    q3   delivery- internati delivery-  10
    q4   product-k product-t data-and-  18
    q5   where-is- refunds-p refunds-f  2
    q6   missing-i damaged-o returns-s  8
    q7   plan-harb plan-comp price-mat  6
    q8   returns-c refunds-f returns-s  4

  a tie only costs something when the documents in it
  have different grades AND it lands where the measure
  looks. Chapter 26: RRF cannot tell (1, 2) from (2, 1),
  because it threw the scores away.

    q3: 2 documents at 0.015873,
         first of them at rank 5
      grade 0  refunds-faq            lex 3, dense -
      grade 1  delivery-fees          lex -, dense 3
    q4: 2 documents at 0.032522,
         first of them at rank 1
      grade 2  product-kettle-hl-2208 lex 1, dense 2
      grade 1  product-toaster-hl-220 lex 2, dense 1
    q4: 2 documents at 0.015873,
         first of them at rank 3
      grade 0  data-and-privacy       lex 3, dense -
      grade 1  sku-conventions        lex -, dense 3
    q6: 2 documents at 0.032522,
         first of them at rank 1
      grade 1  missing-item-in-a-parc lex 1, dense 2
      grade 2  damaged-on-arrival     lex 2, dense 1

  ties that straddle a grade inside the top 5: 4
```

**The depth is the whole of the care here.** BM25 matched 40 of 40 documents on three queries, so
fusing the full lists would hand a document that shares only the word *the* a position of 23 and
let it vote. The program fuses the top ten of each list, which is chapter 26's Warning followed
rather than quoted.

**Then the ties, and there are a great many of them.** Between two and eighteen documents per
query share a fused score with something else. Most of those cost nothing: a tie between two
documents the key grades 0 is invisible to any measure. **Four of them are not like that**, and
two of those four sit at rank one.

**Look at `q4`.** The kettle — grade 2, lexical first and dense second — and the toaster — grade
1, lexical second and dense first — score *exactly* 0.032522. That is not an approximation; it
is `1/61 + 1/62` against `1/62 + 1/61`, and reciprocal rank fusion cannot tell `(1, 2)` from
`(2, 1)` because it threw away the scores that would break it. So on the chapter's headline
identifier query, which of the right and the nearly-right document a user sees first is decided by
nothing at all. `q6` does the same thing with a grade-1 and a grade-2 document.

**And 0.032522 is the number chapter 26 printed, by hand, for its invented pair.** The arithmetic
does not know what corpus it is on.

> **Warning:** A tie in a fused ranking is not a tie in your results list — something has to come
> first, and what decides it is whatever your sort function does with equal keys. That is a
> property of your code rather than of your retrieval, it will differ between implementations, and
> it is invisible unless you look for it. Step 4 reports what it costs.

## Step 4: The Measures, With Their Conventions Said Out Loud

Chapter 26 ends each measure with a warning that is really an instruction: say where you cut a
graded key for a binary measure, and never report an nDCG without its gain convention, its
`\(k\)`{=latex} and its handling of a zero ideal. So the program prints its conventions before it
prints a number.

```python
"""recall@k and nDCG@k over the eight shipped queries.

Chapter 26 built both from zero and attached a warning to each: a
recall figure is recall against your key, and an nDCG is meaningless
without its gain convention, its k, and how it treats a query whose
ideal is zero. So the conventions are declared here rather than
buried, and the program prints them.

  gain      the grade itself, not 2^g - 1
  discount  log2(i + 1)
  k         5 for both measures
  relevant  any grade above 0, which folds grade 1 into grade 2
  ideal     the key's documents sorted by grade
"""

import math
import random

import dense
import lexical
from fuse import DEPTH, fused_order
from key import key, queries

K = 5
GAIN = "grade"


SEED = 44
TRIALS = 10_000


def paired(a, b, trials=TRIALS, seed=SEED):
    """Chapter 20's paired bootstrap, resampling QUERIES and keeping
    each query's pair of marks together. Step 6 is where it is read;
    it lives here so that every import in this lab points backwards."""
    rng = random.Random(seed)
    n = len(a)
    diffs = sorted(
        sum(b[i] - a[i] for i in (rng.randrange(n) for _ in range(n))) / n
        for _ in range(trials))
    return diffs[int(0.025 * trials)], diffs[int(0.975 * trials)]


def recall_at(order, grades, k=K):
    total = sum(1 for g in grades.values() if g > 0)
    found = sum(1 for d in order[:k] if grades.get(d, 0) > 0)
    return found / total if total else 0.0


def dcg(order, grades, k=K):
    return sum(grades.get(d, 0) / math.log(i + 1, 2)
               for i, d in enumerate(order[:k], 1))


def ndcg(order, grades, k=K):
    ideal = sorted(grades, key=lambda d: -grades[d])
    best = dcg(ideal, grades, k)
    return dcg(order, grades, k) / best if best else 0.0


def tie_range(fused_scores, grades, k=K):
    """A tie has no ordering, so report the range it spans rather than
    whichever one sort() happened to emit. Chapter 26 does the same,
    and on this corpus four ties straddle a grade inside the top 5."""
    hi = sorted(fused_scores, key=lambda d: (fused_scores[d],
                                             grades.get(d, 0)), reverse=True)
    lo = sorted(fused_scores, key=lambda d: (fused_scores[d],
                                             -grades.get(d, 0)), reverse=True)
    return ndcg(lo, grades, k), ndcg(hi, grades, k)


def orders(cache=None):
    """The three rankings per query, so every later step reads one
    set of results rather than recomputing them differently."""
    cache = cache or dense.vectors()
    out = {}
    for qid, q in sorted(queries().items()):
        lex, _ = lexical.ranked(q)
        den, dsc = dense.ranked(q, cache)
        fus, fsc, ties = fused_order(lex, den)
        out[qid] = {"lexical": lex, "dense": den, "fused": fus,
                    "fused_scores": fsc, "dense_scores": dsc,
                    "ties": ties}
    return out


if __name__ == "__main__":
    k, res = key(), orders()
    print(f"  conventions: gain = {GAIN}, discount = log2(i+1), k = {K},")
    print(f"  relevant = grade > 0, fusion depth = {DEPTH}, 40 documents,")
    print(f"  a query whose ideal DCG is 0 scores 0 and none here is,")
    print(f"  and a key that judged every query against every one.\n")
    for measure, fn in (("recall@5", recall_at), ("nDCG@5", ndcg)):
        print(f"  {measure}\n")
        print("    query   lexical   dense    fused")
        means = {m: 0.0 for m in ("lexical", "dense", "fused")}
        for qid in sorted(res):
            row = [fn(res[qid][m], k[qid]) for m in
                   ("lexical", "dense", "fused")]
            for m, v in zip(means, row):
                means[m] += v / len(res)
            print(f"    {qid}     " + "   ".join(f"{v:.3f}" for v in row))
        print("    mean    " + "   ".join(f"{means[m]:.3f}" for m in
                                         ("lexical", "dense", "fused")))
        print()
    print("  and the fused nDCG@5 is partly arbitrary, because four")
    print("  ties straddle a grade. The range each query spans:\n")
    lo_m = hi_m = 0.0
    for qid in sorted(res):
        lo, hi = tie_range(res[qid]["fused_scores"], k[qid])
        lo_m += lo / len(res)
        hi_m += hi / len(res)
        flag = "  <- the tie decides it" if hi - lo > 1e-9 else ""
        print(f"    {qid}   {lo:.3f} to {hi:.3f}{flag}")
    print(f"    mean  {lo_m:.3f} to {hi_m:.3f}")
```

```text
  conventions: gain = grade, discount = log2(i+1), k = 5,
  relevant = grade > 0, fusion depth = 10, 40 documents,
  a query whose ideal DCG is 0 scores 0 and none here is,
  and a key that judged every query against every one.

  recall@5

    query   lexical   dense    fused
    q1     0.250   0.500   0.500
    q2     0.750   1.000   1.000
    q3     0.333   1.000   0.667
    q4     0.667   1.000   1.000
    q5     1.000   1.000   1.000
    q6     0.500   0.750   0.750
    q7     0.500   0.500   0.500
    q8     0.800   0.600   0.800
    mean    0.600   0.794   0.777

  nDCG@5

    query   lexical   dense    fused
    q1     0.333   0.884   0.836
    q2     0.847   1.000   1.000
    q3     0.469   0.885   0.671
    q4     0.840   0.882   0.978
    q5     0.733   1.000   1.000
    q6     0.635   0.860   0.744
    q7     0.739   0.739   0.739
    q8     0.629   0.763   0.818
    mean    0.653   0.877   0.848

  and the fused nDCG@5 is partly arbitrary, because four
  ties straddle a grade. The range each query spans:

    q1   0.836 to 0.836
    q2   1.000 to 1.000
    q3   0.671 to 0.853  <- the tie decides it
    q4   0.860 to 1.000  <- the tie decides it
    q5   1.000 to 1.000
    q6   0.744 to 0.847  <- the tie decides it
    q7   0.739 to 0.739
    q8   0.818 to 0.818
    mean  0.834 to 0.887
```

**Dense beats lexical on both measures and it is not close.** Recall@5 of 0.794 against 0.600,
and nDCG@5 of 0.877 against 0.653. On this corpus, with this key, matching meaning finds more of
the graded material than matching words does and puts it higher.

**Fusion is slightly worse than dense on both.** 0.777 against 0.794, and 0.848 against 0.877.
That is not what the usual claim about hybrid retrieval predicts, and before reading anything into
it, read the bottom block.

**The fused nDCG@5 is a range, not a number, and the range is 0.834 to 0.887.** Three of the eight
queries have a tie that straddles a grade inside the top five, so their fused score depends on how
the sort broke it. Call that span the **tie range**: the interval a measure covers when the
ranking's ties have no ordering, which is a fact about your sort rather than about your retrieval. **Dense's 0.877 sits inside that range.** Chapter 26 reached the same conclusion
on two invented queries and this chapter reaches it on eight real ones: the measurement does not
say fusion beat dense, and it does not say dense beat fusion either.

**Fusion's best query is `q4` — and it is the coin flip this step has just condemned.** It scores
0.978 there against dense's 0.882 and lexical's 0.840, which looks like fusion repairing the
identifier query. But `q4`'s own tie range is 0.860 to 1.000, because the kettle and the toaster
are the tied pair, and at the bottom of that range fusion's 0.860 *loses* to dense's 0.882. So the
query where fusion looks best is the one the chapter has already called decided by nothing. **It
does beat both inputs on `q8` as well**, by 0.055, and that one is not a tie. It loses on `q1`,
`q3` and `q6`, and by more than it wins: the three losses total 0.378 against 0.151 of wins, which
is where the negative mean comes from. So the honest summary of the fused column is two wins and
three heavier losses, with the better of the two wins resting on a coin landing.

> **Note:** Recall and nDCG disagree about `q8` and the disagreement is the clearest illustration
> in the chapter of what each measure cannot see. Lexical's recall@5 is 0.800 and dense's is 0.600
> — lexical found more. Lexical's nDCG@5 is 0.629 and dense's is 0.763 — dense ordered better. Both
> are true, they are answers to different questions, and a single number would have hidden one of
> them.

## Step 5: A Reranker, and the Ceiling It Cannot Pass

Chapter 26 defines three arrangements and the qualifier between them is the part to get right. A
*bi-encoder* embeds the two sides separately, so the document side is precomputed — and its
score is symmetric only when both sides go through the *same function*. A *two-tower* bi-encoder,
or one shared model told which side it is encoding by a marker, keeps the precomputation and gives
up the symmetry. A *cross-encoder* puts the query and one document through a model *together* and
emits one score for the ordered pair, so nothing is precomputed and the score is free to be
asymmetric — which is the shape chapter 25 said a directed question needs. Step 3's dense retrieval
is the first kind with one shared model, which is why it is symmetric; this step is the third.

```python
"""A reranker: one model scoring the query and a document together.

Chapter 26 names three arrangements. A bi-encoder embeds the two
sides separately, so the document side is precomputed - and its
score is symmetric only when BOTH sides go through the same
function, which is chapter 26's point and chapter 25's. A two-tower
bi-encoder, or one shared model told which side it is encoding, is
asymmetric and keeps the precomputation. A cross-encoder puts the
query and one document through a model TOGETHER and emits one score
for the ordered pair: nothing is precomputed and the score is free
to be asymmetric.

This is the cross-encoder ARRANGEMENT with a chat model doing the
joint scoring - not a purpose-built cross-encoder, which is a small
trained model and a different artefact. It runs twice, because the
first scale it is given cannot express an order.
"""

import json
import os
import re
import urllib.request

from key import DOCS, key, queries
from measure import K, ndcg, orders, paired, recall_at, tie_range

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 120
DEPTH = 10

COARSE = (
 "Score how well the document answers the question.\n"
 "0 = not relevant, 5 = related, 10 = answers it fully.\n"
 "Reply with the number only.\n\n"
 "Question: {q}\n\nDocument:\n{doc}"
)
FINE = (
 "Score how well the document answers the question, 0 to 100.\n"
 "Use the whole range: two documents should get the same score\n"
 "only if they are equally good. Reply with the number only.\n\n"
 "Question: {q}\n\nDocument:\n{doc}"
)


def score(prompt, q, doc_id):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt.format(
            q=q, doc=(DOCS / f"{doc_id}.md").read_text()[:4000])}],
        "max_tokens": 6, "temperature": 0,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    text = d["choices"][0]["message"]["content"]
    m = re.search(r"-?\d+(\.\d+)?", text)
    return (float(m.group()) if m else 0.0), d["model"]


def ceiling(candidates, grades, k=K):
    """What the best possible reranker reaches on this candidate set:
    reorder it by the human's own grades. Chapter 26's derivation - a
    permutation cannot introduce what the set does not hold."""
    best = sorted(candidates, key=lambda d: -grades.get(d, 0))
    return ndcg(best, grades, k)


if __name__ == "__main__":
    k, res = key(), orders()
    served = None
    print(f"  candidate set: the fused top {DEPTH}, {len(res)} queries,")
    print(f"  {len(res) * DEPTH * 2} joint scorings over two scales\n")

    for name, prompt in (("0 to 10", COARSE), ("0 to 100", FINE)):
        print(f"  scale {name}\n")
        print("    query  distinct  point   tie range      ceiling")
        tot = {"pt": 0.0, "lo": 0.0, "hi": 0.0, "ceil": 0.0}
        pts, was = [], []
        for qid in sorted(res):
            cands = res[qid]["fused"][:DEPTH]
            scored = {}
            for d in cands:
                scored[d], served = score(prompt, queries()[qid], d)
            order = sorted(cands, key=lambda d: -scored[d])
            pt = ndcg(order, k[qid])
            lo, hi = tie_range(scored, k[qid])
            ceil = ceiling(cands, k[qid])
            for key_, v in (("pt", pt), ("lo", lo), ("hi", hi),
                            ("ceil", ceil)):
                tot[key_] += v / len(res)
            pts.append(pt)
            was.append(ndcg(res[qid]["fused"], k[qid]))
            print(f"      {qid}    {len(set(scored.values())):2d} of"
                  f" {DEPTH}   {pt:.3f}   {lo:.3f} to {hi:.3f}"
                  f"    {ceil:.3f}")
        print(f"      mean            {tot['pt']:.3f}   {tot['lo']:.3f}"
              f" to {tot['hi']:.3f}    {tot['ceil']:.3f}")
        first = sum(was) / len(was)
        inside = tot["lo"] <= first <= tot["hi"]
        print(f"      the first stage scored {first:.3f}, which is"
              f" {'INSIDE' if inside else 'outside'}")
        print(f"      that range")
        lo, hi = paired(was, pts)
        print(f"      chapter 20: {(sum(pts)-sum(was))/len(pts):+.3f}"
              f"   95% {lo:+.3f} to {hi:+.3f}\n")

    print(f"  model that replied: {served}\n")
    print("  and what the candidate set costs, which is the thing to")
    print("  measure before buying a better reranker:\n")
    print("    depth   ceiling   candidate recall   calls per query")
    for d in (5, DEPTH, 15):
        c = sum(ceiling(res[q]["fused"][:d], k[q]) / len(res) for q in res)
        r = sum(recall_at(res[q]["fused"][:d], k[q], d) / len(res)
                for q in res)
        print(f"      {d:2d}     {c:.3f}       {r:.3f}              {d}")
```

```text
  candidate set: the fused top 10, 8 queries,
  160 joint scorings over two scales

  scale 0 to 10

    query  distinct  point   tie range      ceiling
      q1     3 of 10   1.000   0.840 to 1.000    1.000
      q2     3 of 10   1.000   0.847 to 1.000    1.000
      q3     3 of 10   1.000   1.000 to 1.000    1.000
      q4     2 of 10   1.000   0.722 to 1.000    1.000
      q5     3 of 10   0.765   0.384 to 0.765    1.000
      q6     3 of 10   0.931   0.823 to 0.988    1.000
      q7     3 of 10   0.739   0.739 to 0.739    0.739
      q8     2 of 10   0.916   0.763 to 1.000    1.000
      mean            0.919   0.765 to 0.936    0.967
      the first stage scored 0.848, which is INSIDE
      that range
      chapter 20: +0.071   95% -0.041 to +0.176

  scale 0 to 100

    query  distinct  point   tie range      ceiling
      q1     8 of 10   0.924   0.924 to 1.000    1.000
      q2     5 of 10   1.000   0.896 to 1.000    1.000
      q3     5 of 10   1.000   1.000 to 1.000    1.000
      q4     3 of 10   1.000   0.840 to 1.000    1.000
      q5     6 of 10   0.671   0.416 to 0.671    1.000
      q6     5 of 10   0.823   0.823 to 0.879    1.000
      q7     4 of 10   0.739   0.739 to 0.739    0.739
      q8     6 of 10   0.916   0.887 to 0.916    1.000
      mean            0.884   0.816 to 0.901    0.967
      the first stage scored 0.848, which is INSIDE
      that range
      chapter 20: +0.036   95% -0.089 to +0.148

  model that replied: gpt-4o-mini-2024-07-18

  and what the candidate set costs, which is the thing to
  measure before buying a better reranker:

    depth   ceiling   candidate recall   calls per query
       5     0.903       0.777              5
      10     0.967       0.891              10
      15     1.000       0.984              15
```

**What this is and is not.** A purpose-built cross-encoder is a small model trained to score
pairs, and this is a chat model asked to do the same job in one line of prompt. The *arrangement*
is the same — the query and the document go through one model together, the score is a function of
the ordered pair, and nothing can be precomputed — and chapter 26 is explicit that the arrangement
is the thing to understand, because the specific models change constantly.

**Read the `distinct` column before anything else, because it decides what the rest of the table
means.** On the first scale the reranker returned **two or three different numbers for ten
candidates**. It was asked for 0, 5 or 10, and it obliged. A scorer with three values cannot order
ten documents; it can only sort them into three buckets, and inside a bucket the order is whatever
the sort function does with equal keys. Python's sort is stable, so inside each flat block the
*fused* order survives untouched — which means a good part of that column's 0.919 is step 3's
ranking wearing step 5's name.

**So apply this chapter's own instrument to its own step.** The tie range on the first scale is
0.765 to 0.936, and **the first stage's 0.848 sits inside it**. By the rule step 4 used to refuse
fusion a verdict, the reranking gain on this scale is a tie-break rather than a measurement. It
would have been easy not to look: the point estimate went up, and the Key Term that catches it is
two pages earlier and was invented for somebody else's step.

**Then widen the scale, because the fault is in the question and not in the model.** Asked for 0
to 100 and told to use the range, the same model returns between three and eight distinct scores,
and the tie range narrows from 0.171 wide to 0.085. **And the point estimate falls**, from 0.919 to
0.884 — the better-measured reranker looks *worse*. The coarse figure sitting near the top of a
wide tie range and the fine one near the bottom of a narrow one is consistent with the first
number carrying an ordering it inherited, and does not prove it. The first stage's 0.848 is still inside the narrower range, so the gain is
still not established, and chapter 20 agrees on both scales: +0.071 with 95 per cent from −0.041
to +0.176, and +0.036 from −0.089 to +0.148.

**The ceiling is the figure in this step that does not depend on the reranker at all**, because it is arithmetic on the key
rather than a measurement of a model. It is what a *perfect* reranker reaches: reorder the
candidate set by the human's own grades, which no real reranker can beat. Chapter 26 derives why
that is a ceiling rather than an estimate — a reordering cannot introduce a document the set does
not hold — and it holds for every reranker, every model and every collection, because it is a
property of permutation. Call the gap between the first stage and that ceiling the **reranking
headroom**: 0.119 at this depth, and no reranker can win more of it than that.

**And the last block is where this step's advice actually is.** At a depth of five the ceiling is
0.903; at ten it is 0.967; at *fifteen* it is 1.000, with the candidate set holding 98.4 per cent
of the graded material. Five more candidates — forty more calls, about another penny — remove every
ceiling this step is about, including `q7`'s. At depth ten `q7`'s ceiling is 0.739 and the reranker
reached exactly that, because two of its four relevant documents were outside the top ten; at
depth fifteen there is nothing left for a reranker to be blamed for. **Measure the candidate set
before you buy a reranker**, because deepening it is a parameter and improving a reranker is a
project. How deep is chapter 28's question, and chapter 26's own example says a hundred.

**One more thing a mean hides: the reranker damaged `q5` on both scales.** It arrives at 1.000 from
the first stage and leaves at 0.765 on one scale and 0.671 on the other — and its tie range on the
first scale runs down to 0.384, so the damage could have been twice as large and the printed
number would not have shown it.

> **Warning:** The reranker and the key are both opinions about relevance, and they were not
> written by the same person. When the reranker disagrees with the key, nothing in this lab says
> which is right — chapter 31 is where a judgement gets validated, and the corpus `README.md` says
> in terms that these grades are one person's. What the lab measures is agreement with the key,
> which is the only thing it can measure, and `q5` is a reminder that the key is the standard here
> by stipulation rather than by proof.

> **Note:** The cost argument for two stages is real and this lab is too small to show it. Chapter
> 26's figures are a million cross-encoder passes against one embedding; here it is 10 candidates
> out of 40 documents, so one call per document would be 320 calls against this step's 80 on one
> scale — a saving of four, not of ten thousand. Take the arrangement from this step and the arithmetic from chapter 26.

## Step 6: And Is Any of It Real?

Six intervals are about to be printed and the chapter has not yet earned the right to call any of
the differences behind them real. Eight queries is a sample, every method saw the same eight, and chapter 20 is the
chapter that makes that a paired comparison with an interval on the difference.

```python
"""Is any of that difference real? Chapter 20, on eight queries.

The bootstrap itself is in measure.py, so that every import in this
lab points at an earlier step.

Chapter 26 computed its measures and stopped. Chapter 20 is the
chapter that will not let you: a mean over eight queries is a
sample, the comparison is paired because every method saw the same
eight, and the interval goes on the DIFFERENCE and not on either
mean. Eight is a small number and the output says so.
"""

from key import key
from measure import K, TRIALS, ndcg, orders, paired, recall_at


def per_query(res, k, fn, method):
    return [fn(res[qid][method], k[qid]) for qid in sorted(res)]


if __name__ == "__main__":
    k, res = key(), orders()
    print(f"  {len(res)} queries, paired, {TRIALS} resamples, k = {K}\n")
    for name, fn in (("recall@5", recall_at), ("nDCG@5", ndcg)):
        marks = {m: per_query(res, k, fn, m)
                 for m in ("lexical", "dense", "fused")}
        print(f"  {name}")
        for a, b in (("lexical", "dense"), ("lexical", "fused"),
                     ("dense", "fused")):
            d = (sum(marks[b]) - sum(marks[a])) / len(res)
            lo, hi = paired(marks[a], marks[b])
            verdict = ("clears zero" if lo > 0 or hi < 0
                       else "contains zero: cannot tell")
            print(f"    {b:7s} - {a:7s}  {d:+.3f}"
                  f"   95% {lo:+.3f} to {hi:+.3f}")
            print(f"                              {verdict}")
        print()
    print("  how many of the eight each pair disagrees on, which is")
    print("  what a paired comparison actually rests on:\n")
    for name, fn in (("recall@5", recall_at), ("nDCG@5", ndcg)):
        marks = {m: per_query(res, k, fn, m)
                 for m in ("lexical", "dense", "fused")}
        for a, b in (("lexical", "dense"), ("dense", "fused")):
            n = sum(1 for x, y in zip(marks[a], marks[b]) if x != y)
            print(f"    {name:8s} {b:7s} against {a:7s}:"
                  f" {n} of {len(res)}")
```

```text
  8 queries, paired, 10000 resamples, k = 5

  recall@5
    dense   - lexical  +0.194   95% +0.029 to +0.371
                              clears zero
    fused   - lexical  +0.177   95% +0.073 to +0.271
                              clears zero
    fused   - dense    -0.017   95% -0.125 to +0.075
                              contains zero: cannot tell

  nDCG@5
    dense   - lexical  +0.223   95% +0.110 to +0.352
                              clears zero
    fused   - lexical  +0.195   95% +0.111 to +0.300
                              clears zero
    fused   - dense    -0.028   95% -0.095 to +0.031
                              contains zero: cannot tell

  how many of the eight each pair disagrees on, which is
  what a paired comparison actually rests on:

    recall@5 dense   against lexical: 6 of 8
    recall@5 fused   against dense  : 2 of 8
    nDCG@5   dense   against lexical: 7 of 8
    nDCG@5   fused   against dense  : 5 of 8
```

**Two of the three retrieval comparisons clear zero and one does not, and the one that does not is
the one chapter 26 asked about.**

**Dense beats lexical, and the interval clears zero on both measures.** +0.194 on recall with 95
per cent between +0.029 and +0.371, and +0.223 on nDCG between +0.110 and +0.352. Eight queries is
few and it was enough here, because the effect is large and the two methods disagree on six or
seven of the eight.

**Fusion beats the lexical baseline, and that row is easy to skip.** +0.177 on recall with 95 per
cent from +0.073 to +0.271, and +0.195 on nDCG from +0.111 to +0.300. Both clear zero. It is a real
result about hybrid retrieval and it is not the one anybody argues about — the argument is always
whether fusion beats the *better* of its two inputs, and a chapter that reported only that argument
would be dropping an established finding for being unsurprising.

**Fusion against dense cannot be told apart.** −0.017 on recall and −0.028 on nDCG, and both
intervals contain zero. There is a second reason to refuse it as well, though not an independent
one — the tie range from step 4, computed from the same eight per-query scores, has dense's figure
inside it. The point estimate is negative and the honest report is *cannot tell*, which is chapter
26's answer to chapter 26's question, reached with eight real queries instead of two invented
ones.

**And the reranking gain does not clear zero either.** +0.071 on nDCG, 95 per cent between −0.041
and +0.176 on the coarse scale, +0.036 from −0.089 to +0.148 on the finer one. Reporting either as
an improvement would be reporting the sample size as a finding — and step 5 gives a second and
sharper reason, which is that the first stage's score sits inside the reranked tie range on both
scales.

**Then read the last block, because it says where each interval's width comes from.** The
comparison between fusion and dense on recall@5 rests on [**two queries of eight**]{.noindex} — the other six
score identically under both, so they contribute nothing but a zero to every resample. Chapter 20
closes with exactly this: the comparison rests only on the cases that disagree. Be careful with
the next step, because it is easy to get backwards. Adding queries the two methods handle
identically *does* narrow the interval, since the width falls with the total count — what it does
not do is help the interval clear zero, because the mean difference is diluted at the same rate.
More agreeing queries buy precision about a difference of nearly nothing.

> **Tip:** The useful thing to take from a *cannot tell* is a number for what it would take to
> settle it, and the arithmetic has to be done on the spread rather than on the effect. Width falls
> as one over the square root of the count, so an effect a tenth the size needs a tenth the width
> and therefore a hundred times the queries — eight hundred, reasoning from the ratio alone. The
> measured spread is kinder, and the question has to be put precisely or the arithmetic answers a
> different one. Asked for an effect a tenth the size of the one that cleared zero, at the spread
> these eight queries actually show, the normal approximation gives **about seventy-five queries on
> nDCG and about two hundred and twenty on recall** — not eight hundred, and the two differ because
> the recall differences are more scattered. Settling *this* difference, which is a smaller target
> again, needs about fifty on nDCG and nearer three hundred on recall. Both are keys to write
> rather than models to buy. Both are keys to write rather than models to buy.
> And chapter 20's warning applies to the estimate itself: a figure like that is the typical
> interval at that size, not a promise of detection.

## What To Actually Do

1. **Read your key before you measure against it.** Its grade scale decides what nDCG can express,
   and whether it judged every document decides whether your recall is recall.
2. **Declare the conventions with every number.** The gain, the discount, the `\(k\)`{=latex}, and
   where you cut a graded key for a binary measure. An nDCG without them cannot be compared with
   anybody else's.
3. **Fuse the top of each list, never the whole collection.** On this corpus BM25 matches 40 of 40
   documents on some queries, and the tail would arrive with positions it has not earned.
4. **Look for ties that straddle a grade.** A fused ranking has many ties; the ones that cost
   something are the ones inside the measure's `\(k\)`{=latex} with different grades either side.
   Report the range, not the number your sort happened to produce.
5. **Measure two things about the candidate set, at two depths, before buying a reranker.** Its
   *recall* is how much of the graded material it holds — 0.891 at depth ten here — and the
   *ceiling* is the best score any reordering of it could reach, 0.967. Chapter 26 keeps those
   apart. On one of these eight queries the reranker was already at the ceiling, and five more
   candidates took it to 1.000.
6. **Count the distinct scores your reranker returns.** Fewer distinct scores than candidates
   means it is bucketing, not ordering, and the order inside a bucket is your sort function's
   opinion rather than the model's.
7. **Put an interval on every difference, paired**, and then look at how many queries the pair
   actually disagrees on. That count is where the width comes from.
8. **Treat a *cannot tell* as a measurement.** It tells you the effect is smaller than your
   evidence can see, and the arithmetic says how much more evidence that would take.

## Summary, Key Terms, and Review Questions

### Summary

Chapter 26 built BM25, reciprocal rank fusion and three measures on eight invented documents with
stipulated cosines, and ended by refusing to give a verdict on hybrid retrieval. This chapter
gives one, on forty real documents with real embeddings and the graded key the book ships. **Read
the key first**: 320 pairs for 8 queries over 40 documents with none missing, so recall here is
recall and not recall-against-whatever-was-judged — a luxury of forty documents; grades of 0, 1
and 2 against chapter 26's four rungs, so the scale expresses fewer distinctions; and two queries
with no top-grade document at all, whose ideal ranking is built from partial answers. **BM25
unchanged** over a corpus not built for it, with one decision chapter 26 did not have to make: the
term pattern keeps hyphens and dots inside a run, which is the only reason `hl-2208-f` exists as a
term at all — and it is worth an IDF of 3.3081 against `the`'s 0.0123. Most queries match 37 or
more of the forty documents, because *the* is in all of them, which is chapter 26's Warning about
fusing a tail made concrete. **The identifier query is the chapter's first result**: BM25 puts the
kettle first where chapter 43's embedding model put the toaster. **Fused with reciprocal rank
fusion at depth ten**, the kettle and the toaster land on exactly 0.032522 — the figure chapter 26
computed by hand for `(1, 2)` against `(2, 1)` — so which one a reader sees is decided by the sort
function. Four ties straddle a grade inside the top five and two of them are at rank one. **Then
the measures, conventions printed**: dense beats lexical at recall@5 0.794 against 0.600 and nDCG@5
0.877 against 0.653, while **fusion comes in slightly below dense on both** — and the fused nDCG is
a range of 0.834 to 0.887 because of those ties, with dense's 0.877 inside it. **Fusion beats both
of its inputs on two queries** — the identifier query, whose top two are the tied pair, and `q8`,
which is not — and loses on three by more than it wins, 0.378 against 0.151.
**A reranker** — a chat model scoring the query and one document together, which is the
cross-encoder *arrangement* rather than the artefact — lifted nDCG@5 from 0.848 to 0.919 against a
**ceiling of 0.967** — but the gain is not a measurement, because asked for 0, 5 or 10 the model
returned **two or three distinct scores for ten candidates**, so inside each flat block the fused
order survived a stable sort and the first stage's 0.848 sits inside the reranked **tie range** of
0.765 to 0.936. Widen the scale to 0 to 100 and it returns three to eight distinct scores, the tie
range narrows to 0.816–0.901 — and the point estimate *falls* to 0.884, because the first figure
was inflated by the ordering it inherited. What is solid is the **reranking headroom**, which is
arithmetic on the key: 0.119 at this depth. The ceiling is chapter 26's
derivation and `q7` is where it bites: its ceiling is 0.739, the reranker reached exactly that, and
two of its four relevant documents never entered the top ten. `q5` is the other half of the lesson,
going from 1.000 to 0.765 on one scale and 0.671 on the other. **And then chapter 20, which
settles one of the three comparisons and refuses the other two.** Dense over lexical clears zero on
both measures (+0.194 and +0.223). Fusion against dense does not (−0.017 and −0.028, both intervals
containing zero, and the tie range besides). The reranking gain does not either: +0.071 with 95 per
cent from −0.041 to +0.176. The recall comparison between fusion and dense rests on **two queries
of eight**, which is where that interval's width comes from, and distinguishing an effect a tenth
the size of the one that cleared zero needs of the order of a hundred queries rather than eight —
a key to write rather than a model to buy.

### Key Terms

| Term | Meaning |
|---|---|
| **Reranking headroom** | The gap between what your first stage scores and what a perfect reranker on the same candidate set would score. What a second stage can possibly win, before you buy one. It is 0.119 at a depth of ten here, and at a depth of fifteen the ceiling is 1.000 and the headroom 0.152 — a deeper set gives a reranker *more* to win, not less, so measure it before buying anything |
| **Tie range** | The span a measure covers when a ranking's ties have no ordering, so the number depends on your sort rather than on your retrieval. Report it instead of whichever end came out |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Read the key first | Its grade scale bounds what nDCG expresses; whether every document was judged decides whether recall is recall |
| What an nDCG needs beside it | The gain convention, the discount, the `\(k\)`{=latex}, where a graded key was cut for a binary measure, and what a query whose ideal DCG is zero scores |
| Fusion depth | Fuse the top of each list. BM25 matched 40 of 40 on some queries here, and `the` is why |
| The RRF tie | `(1, 2)` and `(2, 1)` both score 0.032522 at k=60. Four ties straddled a grade; two were at rank one |
| The candidate set is a ceiling | A permutation cannot introduce what the set does not hold. One query's ceiling was 0.739 and the reranker reached exactly it |
| What eight queries bought | Two retrieval verdicts of three. Dense over lexical and fusion over lexical both cleared zero; fusion over dense did not, and neither did the reranking gain |
| When a reranker is not ranking | When it returns fewer distinct scores than candidates. Two or three of ten here, so the reported gain was a stable sort preserving the first stage |
| Where an interval's width comes from | The queries the two methods disagree on. Two of eight, for fusion against dense on recall |

### Review Questions

1. You have eight queries with graded labels and three retrieval methods. What do you compute, and
   what do you report?
2. Your hybrid retrieval scores slightly below your dense retrieval. What do you conclude?
3. What is the first thing to check before buying a better reranker?
4. Why is an nDCG of 0.877 not comparable with an nDCG of 0.877 from somebody else's tool?
5. A reranker raised your mean nDCG and you want to ship it. What would stop you?

### Review Answers

1. Compute two measures rather than one, because they answer different questions and disagree:
recall@k asks whether the relevant documents arrived and is blind to their order, and nDCG@k
weighs both grade and position. Then compute the *difference* between methods, paired, with an
interval on it, because every method saw the same eight queries and a mean over eight is a sample —
that is chapter 20 and it is the step that turns three numbers into a verdict. Report the
conventions beside every figure: the gain, the discount, the `\(k\)`{=latex}, and where you cut a
graded key for recall. And report how many of the eight the two methods actually disagreed on,
because that count is where the interval's width comes from — in this chapter one comparison rested
on two queries of eight. What you do *not* report is a single mean with no interval, which is the
form in which most retrieval comparisons are offered.
2. That you cannot tell, and the two reasons are worth giving separately. First the interval: the
difference was −0.028 on nDCG@5 with 95 per cent from −0.095 to +0.031, which contains zero, so
eight queries cannot separate them. Second, and specific to fusion: reciprocal rank fusion throws
the scores away and keeps the ranks, so `(1, 2)` and `(2, 1)` tie exactly, and on this corpus four
such ties straddled a grade inside the top five — which makes the fused nDCG a range of 0.834 to
0.887 depending on nothing but the sort. Dense's 0.877 sits inside that range. So the measurement
is consistent with fusion being better, worse or identical. And be careful with the obvious
rescue, which is to point at a query where fusion beat both inputs. There are two, and the
better-looking of them is the identifier query, whose fused top two are *the tied pair*: its range
runs from 0.860 to 1.000 and at the bottom of it fusion loses to dense. The other, `q8`, is a real
win of 0.055. The honest version is that fusion traded — better on two queries, worse on three,
and losing by more than it won. What it *does*
establish is the comparison nobody argues about: fusion beat the lexical baseline with an interval
clearing zero on both measures.
3. The candidate set's recall. A reranker can only permute what the first stage handed it, and a
permutation cannot introduce a document the set does not hold — that is a derivation and it holds
for every reranker, every model and every collection. So compute what a *perfect* reranker would
score on that candidate set by reordering it with your own grades: that is the ceiling, and the gap
between your first stage and it is all a second stage can win. On this chapter's eight queries the
ceiling was 0.967 against a first stage of 0.848, and on one query the ceiling was 0.739 and the
reranker had already reached it exactly — two of that query's four relevant documents were outside
the top ten, so no reranker whatever would have helped and a deeper candidate set was the only
thing that could — and five more candidates took the mean ceiling to 1.000 for about one more
penny. Then say the second thing to measure, which is the reranker's own granularity: if it
returns fewer distinct scores than you gave it candidates, it is bucketing rather than ordering,
and whatever order you see inside a bucket came from your sort and not from the model.
4. Because the number depends on conventions that do not cancel. The gain convention is the one
that bites: using the grade directly against using `\(2^g - 1\)`{=latex} gave chapter 26 0.6216 and
0.5193 for the same ranking and the same key, ten points apart. The `\(k\)`{=latex} matters,
the treatment of a query whose ideal DCG is zero matters, and where a graded key is cut for a
binary measure matters. The log base is the one thing that *does* cancel, exactly, because it
multiplies the DCG and the ideal DCG by the same constant. And the key itself is the largest
difference of all: this chapter's recall is recall against a file that judged every pair, which is
unusual, and its grades are one person's. So quote the conventions or the number is not
information.
5. Four things, and the first is the one nobody checks. **Count the distinct scores the reranker
returned.** Asked for 0, 5 or 10 it gave two or three different numbers for ten candidates, which
is a bucketing and not an ordering — inside each bucket the order was whatever the sort did with
equal keys, which here meant the first stage's order surviving untouched, so part of the reported
gain was the stage it was supposed to be improving. Ask for a finer scale and the point estimate
*fell*, from 0.919 to 0.884. **Second, the tie range**: the first stage's 0.848 sits inside the
reranked range on both scales, which by this chapter's own rule for fusion makes the gain a
tie-break rather than a measurement. **Third the interval**, which agrees: +0.071 from −0.041 to
+0.176, and +0.036 from −0.089 to +0.148. **Fourth the per-query column**, because a mean hides
direction: one query arrived at a perfect 1.000 and left at 0.765. And say where the cheap win is:
at a depth of fifteen the ceiling is 1.000 and the candidate set holds 98 per cent of the graded
material, so five more candidates were worth more than any reranker — chapter 53 is where the
per-call arithmetic belongs.

> **You understand this when** you can say which of this chapter's comparisons eight queries
> settle and which they do not, and name the two things to measure before buying a reranker.
