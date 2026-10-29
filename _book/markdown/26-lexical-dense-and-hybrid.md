# Lexical, Dense and Hybrid Retrieval

Chapter 25 ended with a list of limits and handed almost all of them here. This chapter pays
that debt. What you get for it is a second kind of search built from zero, a way to combine two
searches whose scores cannot be compared, the arrangement that lets a score depend on which text
is the question, and three measures that turn an answer key into a number — together with what
each measure does not see.

*The problem.* I have two kinds of search that each fail differently, and no way to say which is
better.

*The question.* How does matching words actually work, how do you combine it with matching
meaning, and how do you measure whether any of it improved?

Everything in this chapter ranks. Nothing in it thresholds, which is the promise chapter 24
made.

## Matching the Words As Written

**Lexical retrieval** scores a document by the query words it contains. The name is worth
keeping separate from "keyword search", because the method is not a filter: it does not ask
*which documents contain these words*, it gives every document a number and sorts.

Start with the units. Chapter 10's tokens are the *model's* pieces, chosen by byte-pair
encoding, and they are not what a lexical index counts. An index counts terms, and a **term** is
whatever the indexer decided to treat as one unit — usually a whitespace-and-punctuation split,
lower-cased, sometimes reduced to a stem so that *servicing* and *serviced* collapse together.
The eight documents below are split on whitespace and lower-cased, and that is the whole of it.

Three quantities decide a score. The first is the obvious one, and the other two are each there
to answer an objection to it.

**Term frequency** is how often a term appears in one document, written
`\(f_{t,d}\)`{=latex}. A document that says *refund* four times is plausibly more about refunds
than one that says it once.

**Document frequency** is how many documents in the collection hold a term at all, written
`\(n_t\)`{=latex}. It exists because term frequency alone rewards the wrong words: *the* appears
constantly and tells you nothing. **Inverse document frequency** turns that around, so a term in
few documents is worth more than a term in many:

```{=latex}
\[ \mathrm{IDF}(t) = \ln\!\left(\frac{N - n_t + 0.5}{n_t + 0.5} + 1\right) \]
```

`\(N\)`{=latex} is the number of documents. Read it with chapter 8's method: inside the
logarithm is a ratio of *documents without the term* to *documents with it*, so the fraction
grows as the term gets rarer, and chapter 8's logarithm compresses the result.

**Document length** is the third, because term frequency also rewards long documents: a page
mentions everything more often than a sentence does, without being more about any of it.

## BM25, and the Two Knobs In It

**BM25** combines those three. It is the standard lexical scoring function, it has been for
decades, and this is the form you will meet:

```{=latex}
\[ \mathrm{score}(q,d) = \sum_{t \in q} \mathrm{IDF}(t) \cdot
   \frac{f_{t,d}\,(k_1+1)}{f_{t,d} + k_1\left(1 - b + b\,\dfrac{|d|}{\mathrm{avgdl}}\right)} \]
```

Work outward from the brackets, as chapter 8 says. The sum runs over the query's terms, so each
term contributes independently and a document matching two query terms gets both
contributions. Each term's contribution is its IDF multiplied by a fraction built from its
term frequency. In the denominator, `\(|d|\)`{=latex} is this document's length and
`\(\mathrm{avgdl}\)`{=latex} is the average length across the collection, so the ratio is *how
long this document is compared with a typical one*.

`\(k_1\)`{=latex} and `\(b\)`{=latex} are the two knobs, and they are constants somebody chose —
conventionally about 1.5 and 0.75. They are not derived from anything, and that matters for how
you talk about this formula.

Here it is from zero, on eight documents.

```python
import math

# Eight short documents. Lower-cased and split on whitespace - that is the
# whole of the "tokenising" here, and it is not the model's tokeniser.
CORPUS = {
    "d1": "the refund policy for every order",
    "d2": "how the refund on a cancelled order is calculated",
    "d3": "refund refund refund refund refund refund",
    "d4": "replacing the seal on pump X-4471-D before servicing the unit",
    "d5": "replacing the seal on pump X-4471-B before servicing the unit",
    "d6": "shipping and returns for damaged goods",
    "d7": "getting your money back on an order you already cancelled",
    "d8": "the payment methods we accept and when we charge the card",
}

def terms(text):
    return text.lower().split()

DOCS = {d: terms(t) for d, t in CORPUS.items()}
N = len(DOCS)
AVGDL = sum(len(t) for t in DOCS.values()) / N

def df(term):
    return sum(1 for t in DOCS.values() if term in t)

def idf_classic(term):
    n = df(term)
    return math.log((N - n + 0.5) / (n + 0.5))

def idf(term):
    # The +1 inside the logarithm is what stops it going negative.
    n = df(term)
    return math.log((N - n + 0.5) / (n + 0.5) + 1)

def bm25(query, doc, k1=1.5, b=0.75):
    dl = len(DOCS[doc])
    total = 0.0
    for term in terms(query):
        tf = DOCS[doc].count(term)
        if tf == 0:
            continue
        norm = tf + k1 * (1 - b + b * dl / AVGDL)
        total += idf(term) * tf * (k1 + 1) / norm
    return total

if __name__ == "__main__":
    print(f"  {N} documents, average length {AVGDL:.3f} terms\n")

    print("  what one term is worth, by how many documents hold it:")
    for term in ("the", "order", "refund", "pump", "x-4471-d"):
        print(f"    {term:9s} in {df(term)} of {N}   idf {idf(term):.4f}"
              f"   classic {idf_classic(term):+.4f}")

    print("\n  term frequency saturates: 'refund' repeated, b=0 so length")
    print("  cannot interfere. k1=1.5, so the ceiling is k1+1 = 2.5 idf:")
    k1 = 1.5
    for tf in (1, 2, 4, 8, 100):
        factor = tf * (k1 + 1) / (tf + k1)
        print(f"    tf {tf:3d}  ->  {factor:.4f} idf   "
              f"({factor / (k1 + 1) * 100:.1f}% of the ceiling)")

    print("\n  'refund policy' ranked:")
    ranked = sorted(DOCS, key=lambda d: bm25("refund policy", d), reverse=True)
    for place, d in enumerate(ranked[:4], 1):
        print(f"    {place}  {bm25('refund policy', d):.4f}  {d}"
              f"  {CORPUS[d][:34]}")
```

```text
  8 documents, average length 8.500 terms

  what one term is worth, by how many documents hold it:
    the       in 5 of 8   idf 0.4925   classic -0.4520
    order     in 3 of 8   idf 0.9445   classic +0.4520
    refund    in 3 of 8   idf 0.9445   classic +0.4520
    pump      in 2 of 8   idf 1.2809   classic +0.9555
    x-4471-d  in 1 of 8   idf 1.7918   classic +1.6094

  term frequency saturates: 'refund' repeated, b=0 so length
  cannot interfere. k1=1.5, so the ceiling is k1+1 = 2.5 idf:
    tf   1  ->  1.0000 idf   (40.0% of the ceiling)
    tf   2  ->  1.4286 idf   (57.1% of the ceiling)
    tf   4  ->  1.8182 idf   (72.7% of the ceiling)
    tf   8  ->  2.1053 idf   (84.2% of the ceiling)
    tf 100  ->  2.4631 idf   (98.5% of the ceiling)

  'refund policy' ranked:
    1  3.1536  d1  the refund policy for every order
    2  1.9761  d3  refund refund refund refund refund
    3  0.9201  d2  how the refund on a cancelled orde
    4  0.0000  d4  replacing the seal on pump X-4471-
```

**Read the IDF column first, because it is where the rarity is.** `x-4471-d` is in one document
of eight and is worth 1.7918. `the` is in five of eight and is worth 0.4925. A query term that
nearly every document holds barely moves a score, and that is the whole job of the inverse.

**The classic column is a trap worth knowing.** The original IDF has no `+1` inside the
logarithm, and when a term is in more than half the collection the fraction drops below one, so
its logarithm goes *negative*: `the` scores `\(-0.4520\)`{=latex}. A negative contribution means
containing a query term actively *lowers* a document's score, which no one wants. The modern
form adds one inside the logarithm, which keeps the fraction above one and the result above
zero for every `\(n_t\)`{=latex}. Adding one is not the only fix — some engines simply floor the
IDF at zero instead — and the two differ in what they do to a near-universal term: the floor
makes it worth exactly nothing, while the `+1` leaves it worth a little. If you ever see a
lexical engine rank a document lower for matching more words, this is the first thing to check.

**Now the saturation, which is the part of BM25 people miss.** Look at the second block. Going
from one mention to two adds 0.43. Going from eight mentions to a hundred adds 0.36 in total.
The fraction climbs towards a ceiling and stops: as `\(f_{t,d}\)`{=latex} grows without limit the
term's contribution approaches `\((k_1+1)\)`{=latex} multiplied by its IDF, which here is 2.5
IDF, and a hundred mentions reach 98.5% of it.

That is why `d3` — the document that is nothing but the word *refund* six times — comes second
and not first. It has the highest term frequency in the collection and it still loses to `d1`,
which matches both query terms once each.

**Both of these are design choices with stated properties, not derivations.** Nothing forces a
saturating curve of that particular shape, and nothing derives 1.5 and 0.75; they were tuned on
test collections, and other shapes exist. What is worth carrying into an interview is not the
constants but the three objections the formula answers in order, and the fact that term
frequency saturates — because the property is what makes BM25 hard to fool, and the constants
are details that will differ between engines.

> **Note:** `\(k_1\)`{=latex} and `\(b\)`{=latex} are tunable, and the defaults above are what
> most engines ship. They are a dated detail in chapter 6's sense, not a lasting principle. The
> lasting parts are the three quantities and the saturation.

## Why the Two Scores Cannot Simply Be Added

You now have two searches. Chapter 24's dense retrieval scores by cosine, and BM25 scores by
matched terms. The obvious move is to add the two numbers, and it is wrong for a reason chapter
24 already established: **a raw cosine has no meaning on its own**, and neither does a BM25
score.

```python
from bm25 import CORPUS, bm25

# Two rankings of the same eight documents for one query. The lexical one is
# BM25 from the first program. The dense one is a stipulated cosine, as in
# chapters 24 and 25 - nothing here shows what a real model would return.
QUERY = "refund on a cancelled order"
DENSE = {"d7": 0.9891, "d2": 0.9874, "d1": 0.9702, "d6": 0.9312,
         "d8": 0.9145, "d3": 0.8871, "d4": 0.6203, "d5": 0.6198}

def ranks(scores):
    order = sorted(scores, key=lambda d: scores[d], reverse=True)
    return {d: place for place, d in enumerate(order, 1)}

def rrf(rank_lists, k=60):
    out = {}
    for rl in rank_lists:
        for doc, place in rl.items():
            out[doc] = out.get(doc, 0.0) + 1 / (k + place)
    return out

if __name__ == "__main__":
    lex = {d: bm25(QUERY, d) for d in CORPUS}
    lex_r, dense_r = ranks(lex), ranks(DENSE)

    print(f"  query: {QUERY}\n")
    print("  doc   BM25     rank    cosine   rank")
    for d in sorted(CORPUS):
        print(f"  {d}   {lex[d]:6.4f}    {lex_r[d]}     "
              f"{DENSE[d]:.4f}    {dense_r[d]}")

    print("\n  not one scale. BM25 here runs"
          f" {min(lex.values()):.4f} to {max(lex.values()):.4f},")
    print(f"  the cosines {min(DENSE.values()):.4f} to"
          f" {max(DENSE.values()):.4f}. Adding them lets one")
    print("  drown the other, and neither range means anything.")

    fused = rrf([lex_r, dense_r])
    print("\n  reciprocal rank fusion, k=60. Ranks only, no scores:")
    for place, d in enumerate(sorted(fused, key=lambda x: fused[x],
                                     reverse=True), 1):
        print(f"    {place}  {fused[d]:.6f}  {d}   "
              f"(lexical {lex_r[d]}, dense {dense_r[d]})")

    print("\n  one document's arithmetic, to check by hand:")
    d = "d7"
    print(f"    {d}: 1/(60+{lex_r[d]}) + 1/(60+{dense_r[d]})")
    print(f"        = {1/(60+lex_r[d]):.6f} + {1/(60+dense_r[d]):.6f}"
          f" = {fused[d]:.6f}")

    print("\n  what k does - the gap between rank 1 and rank 2:")
    for k in (0, 1, 10, 60, 1000):
        gap = 1 / (k + 1) - 1 / (k + 2)
        print(f"    k {k:4d}   1/(k+1) - 1/(k+2) = {gap:.6f}")
```

```text
  query: refund on a cancelled order

  doc   BM25     rank    cosine   rank
  d1   2.1771    3     0.9702    3
  d2   5.5089    1     0.9874    2
  d3   1.9761    4     0.8871    6
  d4   0.6422    5     0.6203    7
  d5   0.6422    6     0.6198    8
  d6   0.0000    7     0.9312    4
  d7   2.7038    2     0.9891    1
  d8   0.0000    8     0.9145    5

  not one scale. BM25 here runs 0.0000 to 5.5089,
  the cosines 0.6198 to 0.9891. Adding them lets one
  drown the other, and neither range means anything.

  reciprocal rank fusion, k=60. Ranks only, no scores:
    1  0.032522  d2   (lexical 1, dense 2)
    2  0.032522  d7   (lexical 2, dense 1)
    3  0.031746  d1   (lexical 3, dense 3)
    4  0.030777  d3   (lexical 4, dense 6)
    5  0.030550  d6   (lexical 7, dense 4)
    6  0.030310  d4   (lexical 5, dense 7)
    7  0.030090  d8   (lexical 8, dense 5)
    8  0.029857  d5   (lexical 6, dense 8)

  one document's arithmetic, to check by hand:
    d7: 1/(60+2) + 1/(60+1)
        = 0.016129 + 0.016393 = 0.032522

  what k does - the gap between rank 1 and rank 2:
    k    0   1/(k+1) - 1/(k+2) = 0.500000
    k    1   1/(k+1) - 1/(k+2) = 0.166667
    k   10   1/(k+1) - 1/(k+2) = 0.007576
    k   60   1/(k+1) - 1/(k+2) = 0.000264
    k 1000   1/(k+1) - 1/(k+2) = 0.000001
```

**Look at the two ranges.** BM25 runs from 0 to 5.5089 and the stipulated cosines run from
0.6198 to 0.9891 — stipulated, so the *range* is one I chose, and a real model's would differ;
what does not depend on my choosing is that the two have no common unit. Added together, the BM25 column decides everything and the cosine column is noise on
top. You could rescale, but into what? There is no unit either number is measured in, so there
is no principled scale to put them on. Any rescaling is a weight you chose.

**Reciprocal rank fusion**[]{idx="RRF"} sidesteps the problem by throwing the scores away and keeping only
the positions:

```{=latex}
\[ \mathrm{RRF}(d) = \sum_{r} \frac{1}{k + \mathrm{rank}_r(d)} \]
```

A document's fused score is the sum, over the rankings it appears in, of one divided by `\(k\)`
plus its position in that ranking. The sum is over rankings, so appearing high in two lists beats
appearing high in one. **It needs nothing from the two systems except an ordering**, which is
exactly what makes it the standard way to combine them: ranks are comparable when scores are
not.

**And it discards real information, which you can see in the output.** `d2` and `d7` tie
*exactly* at 0.032522. One is lexical-first and dense-second, the other is the reverse, and
since the formula sees only `(1, 2)` against `(2, 1)` it cannot tell them apart. The scores that
would break the tie have been thrown away on purpose. That is the price.

**The constant `\(k\)`{=latex} controls how much a top position is worth.** The last block
prints the gap between rank 1 and rank 2 as `\(k\)`{=latex} grows. At `\(k=0\)`{=latex} being
first rather than second is worth 0.5, which is enormous: one system's confident first pick
would dominate. At `\(k=60\)`{=latex} it is worth 0.000264, so the top few positions are
treated as roughly equally good and agreement across lists matters more than any single
list's ordering. The conventional 60 is a choice, not a derivation.

> **Warning:** Fuse the *top of each list*, not the whole collection. Look at `d6` and `d8` in
> the table: both score BM25 0.0000, because they share no term with the query, and yet the
> ranking hands them positions 7 and 8 as though it had an opinion. Feeding that arbitrary tail
> into the fusion gives it votes it has not earned. In practice each system returns its top few
> hundred and only those are fused.

## Writing Down How Much a Document Answers

Chapter 25 established the relevance judgement — one recorded decision that a document does
or does not answer a query — and said an answer key is made of them. Those are binary: yes or
no. For ranking measures that is usually not enough, because documents are not equally good
answers.

**Graded relevance** replaces the yes-or-no with a small scale. Three *non-zero* points is the
common
choice, and the labels have to mean something a second person would apply the same way:

| Grade | What it means |
|---|---|
| 3 | Answers the question on its own |
| 2 | Useful, but the reader has to do some work |
| 1 | Related, and not an answer |
| 0 | Not relevant |

The grades are the expensive part of everything that follows, and they are the only part that
cannot be computed. Two things make them worth the cost. They let a measure distinguish a
ranking that put a partial answer first from one that put the full answer first, which a binary
key cannot see. And they are reusable: the key outlives every change to the retrieval, so the
cost is paid once and the measurements are free afterwards.

> **Tip:** Write the grade definitions down before grading anything, and have a second person
> grade a sample against them. If two people disagree a lot, the definitions are the problem and
> every number built on the key inherits it. This is the cheapest quality check in retrieval and
> it is almost always skipped.

## Three Measures, and What Each One Misses

Now the measures. All three take a ranking and an answer key and return a number, and they
disagree with each other in ways worth knowing.

```python
import math

# One query, and a human's graded judgement of eight documents.
# 3 = answers it fully, 2 = useful, 1 = related, 0 = no.
LABELS = {"d7": 3, "d2": 3, "d1": 2, "d6": 1, "d3": 0,
          "d4": 0, "d5": 0, "d8": 0}

# What one system actually returned, best first.
RANKING = ["d1", "d3", "d2", "d6", "d8", "d7", "d4", "d5"]

def recall_at(ranking, k):
    total = sum(1 for g in LABELS.values() if g > 0)
    found = sum(1 for d in ranking[:k] if LABELS[d] > 0)
    return found / total

def reciprocal_rank(ranking):
    for place, d in enumerate(ranking, 1):
        if LABELS[d] > 0:
            return 1 / place
    return 0.0

def dcg(ranking, k, base=2, exp_gain=False):
    total = 0.0
    for i, d in enumerate(ranking[:k], 1):
        gain = (2 ** LABELS[d] - 1) if exp_gain else LABELS[d]
        total += gain / (math.log(i + 1) / math.log(base))
    return total

def ndcg(ranking, k, base=2, exp_gain=False):
    ideal = sorted(LABELS, key=lambda d: LABELS[d], reverse=True)
    best = dcg(ideal, k, base, exp_gain)
    return dcg(ranking, k, base, exp_gain) / best if best else 0.0

if __name__ == "__main__":
    print("  what came back, with the grade a human gave each one:")
    for i, d in enumerate(RANKING, 1):
        print(f"    {i}  {d}  grade {LABELS[d]}")

    print("\n  recall@k - did the relevant ones arrive at all:")
    for k in (1, 3, 5, 8):
        print(f"    recall@{k}  {recall_at(RANKING, k):.3f}")

    print(f"\n  reciprocal rank: first relevant is at 1, so"
          f" {reciprocal_rank(RANKING):.3f}")

    print("\n  DCG@5, term by term. The discount is log2(i+1):")
    run = 0.0
    for i, d in enumerate(RANKING[:5], 1):
        disc = math.log(i + 1, 2)
        run += LABELS[d] / disc
        print(f"    {i}  grade {LABELS[d]}  / log2({i+1}) = {disc:.4f}"
              f"  -> {LABELS[d]/disc:.4f}   running {run:.4f}")

    ideal = sorted(LABELS, key=lambda d: LABELS[d], reverse=True)
    print(f"\n  the ideal ordering by grade: {' '.join(ideal[:5])}")
    run = 0.0
    for i, d in enumerate(ideal[:5], 1):
        disc = math.log(i + 1, 2)
        run += LABELS[d] / disc
        print(f"    {i}  grade {LABELS[d]}  / log2({i+1}) = {disc:.4f}"
              f"  -> {LABELS[d]/disc:.4f}   running {run:.4f}")

    print(f"\n  nDCG@5 = {dcg(RANKING,5):.4f} / {dcg(ideal,5):.4f}"
          f" = {ndcg(RANKING,5):.4f}")

    print("\n  the log base cancels, because it divides both halves:")
    for base in (2, 10, math.e):
        name = "e" if base == math.e else str(base)
        print(f"    base {name:>2s}  DCG {dcg(RANKING,5,base):7.4f}"
              f"  ideal {dcg(ideal,5,base):7.4f}"
              f"  nDCG {ndcg(RANKING,5,base):.6f}")

    print("\n  the GAIN convention does not cancel:")
    print(f"    gain = grade        nDCG@5 {ndcg(RANKING,5):.4f}")
    print(f"    gain = 2^grade - 1  nDCG@5 "
          f"{ndcg(RANKING,5,exp_gain=True):.4f}")
```

```text
  what came back, with the grade a human gave each one:
    1  d1  grade 2
    2  d3  grade 0
    3  d2  grade 3
    4  d6  grade 1
    5  d8  grade 0
    6  d7  grade 3
    7  d4  grade 0
    8  d5  grade 0

  recall@k - did the relevant ones arrive at all:
    recall@1  0.250
    recall@3  0.500
    recall@5  0.750
    recall@8  1.000

  reciprocal rank: first relevant is at 1, so 1.000

  DCG@5, term by term. The discount is log2(i+1):
    1  grade 2  / log2(2) = 1.0000  -> 2.0000   running 2.0000
    2  grade 0  / log2(3) = 1.5850  -> 0.0000   running 2.0000
    3  grade 3  / log2(4) = 2.0000  -> 1.5000   running 3.5000
    4  grade 1  / log2(5) = 2.3219  -> 0.4307   running 3.9307
    5  grade 0  / log2(6) = 2.5850  -> 0.0000   running 3.9307

  the ideal ordering by grade: d7 d2 d1 d6 d3
    1  grade 3  / log2(2) = 1.0000  -> 3.0000   running 3.0000
    2  grade 3  / log2(3) = 1.5850  -> 1.8928   running 4.8928
    3  grade 2  / log2(4) = 2.0000  -> 1.0000   running 5.8928
    4  grade 1  / log2(5) = 2.3219  -> 0.4307   running 6.3235
    5  grade 0  / log2(6) = 2.5850  -> 0.0000   running 6.3235

  nDCG@5 = 3.9307 / 6.3235 = 0.6216

  the log base cancels, because it divides both halves:
    base  2  DCG  3.9307  ideal  6.3235  nDCG 0.621602
    base 10  DCG 13.0574  ideal 21.0061  nDCG 0.621602
    base  e  DCG  5.6708  ideal  9.1228  nDCG 0.621602

  the GAIN convention does not cancel:
    gain = grade        nDCG@5 0.6216
    gain = 2^grade - 1  nDCG@5 0.5193
```

**Recall@k** is the fraction of all the relevant documents that appear in the top `\(k\)`{=latex}.
It asks *did they arrive*, and nothing else. Here recall@5 is 0.750: three of the four
*relevant* documents are in the top five. All eight are graded — zero is a grade — and what
counts for recall is a grade above zero. **It is blind to order.** The same three documents in any
arrangement inside the top five give 0.750. That makes it the wrong measure for what a user
sees, and the right one for a first pass whose only job is to collect candidates for something
else to sort — which a later section builds.

**And recall has a problem the other two do not**, which is worth knowing because it is the usual
follow-up question. Its denominator is *all* the relevant documents, and on a real collection
nobody knows that number: finding it means judging every document against every query. Eight
documents make it look free. A hundred thousand make it impossible, so in practice the
denominator is whatever the key happens to contain — which means a recall figure is only ever
recall against your key, and a document nobody ever judged is invisible to it. That is chapter
25's invisible miss, still here, one level further up.

**Reciprocal rank** is one divided by the position of the first relevant result; averaged over
many queries it is the **mean reciprocal rank**, or MRR[]{idx="MRR"}. It asks *how far did the reader have to
look*, which is the right question when there is one answer and finding it ends the task.

**Both of these are binary measures, and they need a convention stated too.** Recall and
reciprocal rank take *relevant* or *not*, so a graded key has to be cut somewhere, and the
programs here cut it at a grade above zero. That means a grade-1 document — *related, and not an
answer* — counts as found, and a ranking that puts one first has a reciprocal rank of 1.000. If
your key grades, say where you cut it, for the same reason the chapter insists an nDCG is
meaningless without its gain convention: a reader cannot interpret the number otherwise.

**And here it is worth 1.000, which should stop you.** The first result is `d1`, graded 2, so the
first relevant document is at position one and the reciprocal rank is perfect. Meanwhile a
grade-3 document sits at position six. **MRR says this ranking is flawless, and nDCG[]{idx="nDCG"} says it is
0.6216.** Neither is wrong: MRR measures the distance to the first relevant thing, and this
ranking is genuinely excellent at that. It simply cannot see the difference between a partial
answer and a complete one, because it stops looking after the first non-zero grade.

**Discounted cumulative gain** is the one that sees both grade and position. Each result
contributes its grade divided by a discount that grows with position, and the contributions are
added up:

```{=latex}
\[ \mathrm{DCG}@k = \sum_{i=1}^{k} \frac{g_i}{\log_2(i+1)} \]
```

`\(g_i\)`{=latex} is the grade of the result at position `\(i\)`{=latex}, and
`\(\log_2\)`{=latex} is the first logarithm in this book to a base other than chapter 8's
`\(e\)`{=latex}: `\(\log_2 x\)`{=latex} answers "what power of 2 gives
`\(x\)`{=latex}?", so `\(\log_2 8 = 3\)`{=latex}. It turns out not to matter which base you
use here, for a reason worked out three paragraphs below. Follow the printed
table: position 1 is divided by `\(\log_2 2 = 1\)`{=latex}, so it is undiscounted; position 3 is
divided by 2, so a grade-3 document there contributes 1.5; position 4 is divided by 2.3219. The
running column adds up to 3.9307.

**The logarithm is a convention and not a derivation, and it is worth being exact about which
part is which.** What the discount *must* do is decrease with position. Why a logarithm rather
than any other decreasing function is a choice: it decays slowly, so the difference between
positions 1 and 2 is large while the difference between 10 and 11 is small, which matches a
rough intuition about how people read result lists. That intuition is not a theorem, and
other discounts are in use. Do not claim the log is forced.

**What *is* derivable is that the base does not matter.** Look at the third block: base 2, base
10 and base `\(e\)`{=latex} give DCGs of 3.9307, 13.0574 and 5.6708, and all three give an nDCG
of 0.621602.

Chapter 8 gave you the natural logarithm `\(\ln\)`{=latex} and one property of it. A logarithm
to another base is that one rescaled, and the relation is worth having in front of you because
the rest of this paragraph is just arithmetic on it:

```{=latex}
\[ \log_c x = \frac{\ln x}{\ln c} \]
```

So a term `\(g_i / \log_c(i+1)\)`{=latex} is the same as
`\(g_i \cdot \ln c / \ln(i+1)\)`{=latex}: changing the base multiplies every term by the
*same* constant `\(\ln c\)`{=latex}. Check it against the printed numbers rather than taking
it: base 2 should be `\(\ln 2 = 0.6931\)`{=latex} of base `\(e\)`{=latex}, and
`\(3.9307 / 5.6708 = 0.6931\)`{=latex}. A constant multiplying the DCG multiplies the ideal DCG
by exactly the same amount, so it cancels in the ratio. The normalisation is what buys that, and
the cancelling is exact rather than approximate.

**Normalised discounted cumulative gain**, written nDCG, is the ratio: the DCG of your ranking
divided by the DCG of the best possible
ranking of the same documents. Here 3.9307 divided by 6.3235 gives 0.6216. The ideal is built by
sorting the graded documents by grade, which the program prints: `d7 d2 d1 d6 d3`. Dividing
makes the number comparable across queries, because a query with four relevant documents and a
query with one no longer live on different scales.

**But the gain convention does not cancel, and this is the one that bites.** The last block
computes the same nDCG two ways. Using the grade directly gives 0.6216. Using
`\(2^{g}-1\)`{=latex} — the other standard choice, which weights a grade-3 document far above a
grade-2 one — gives 0.5193. Same ranking, same key, same `\(k\)`{=latex}, two numbers ten points
apart. **So an nDCG is not a number you can compare against one computed by a different
tool** without knowing its gain convention, its `\(k\)`{=latex}, and how it treats a query whose
ideal DCG is zero.

## Two Encoders, or One Model That Sees Both

Chapter 25 proved that a single shared encoder compared by a cosine cannot distinguish *x
answers y* from *y answers x*, and named two escapes: score the two texts together, or encode
the two sides with *different* encoders. Both are arrangements, and the arrangements have names.

A **bi-encoder** encodes the query and each document separately and compares the two vectors
with a cosine. The decisive property is that the document side does not depend on the query, so
**every document vector can be computed once, before any query arrives**.

**Be careful here, because a bi-encoder is not by itself an escape.** Chapter 24's dense
retrieval is a bi-encoder in which both sides go through the *same* model — chapter 24 says so in
as many words, because otherwise the numbers are not comparable — and that is exactly the
arrangement chapter 25 derived cannot answer a directed question. The score is symmetric and no
amount of training changes it.

What escapes is any arrangement that makes the two sides go through *different* functions. The
**two-tower** form is the obvious one: a bi-encoder with a separate query encoder and document
encoder, giving `\(\cos(f(q), g(d))\)`{=latex} with `\(f \neq g\)`{=latex}. It keeps the
precomputation, because `\(g\)`{=latex} still does not depend on the query, and it gives up the
symmetry.

**And there is a cheaper way to the same place**, which chapter 25 also named and which is how
much of current practice does it: keep one shared model and tell it which side it is encoding,
by prefixing the text with a marker such as `query:` or `passage:`. The weights are shared, so
it still looks like a shared encoder — but the *function* applied to a query differs from the one
applied to a document, which is what `\(f \neq g\)`{=latex} asks for. So **"shared weights"
and "symmetric" are not the same claim**: what forces symmetry is putting both sides through the
same function, marker and all. Either way the point stands: you can have a directed score *and*
precomputed documents at the same time.

A **cross-encoder** puts the query and one document through a model *together*, as a single
input, and the model emits one score for the pair. Nothing is precomputed, because the input does
not exist until the query does. In exchange, the model can relate the two texts directly, and the
score is a function of the ordered pair rather than of two independently made vectors — so it
is free to be asymmetric, which is the shape chapter 25 said a directed question needs.

The cost difference is the whole reason for what follows.

```python
from measures import LABELS, dcg, recall_at

# What stage one returned, best first, for the same query as before.
STAGE_ONE = ["d1", "d3", "d2", "d6", "d8", "d7", "d4", "d5"]

def ideal_of(candidates, k):
    # The best any reordering of this candidate set can do: sort it by grade.
    best = sorted(candidates, key=lambda d: LABELS[d], reverse=True)
    return dcg(best, k)

def whole_corpus_ideal(k):
    best = sorted(LABELS, key=lambda d: LABELS[d], reverse=True)
    return dcg(best, k)

if __name__ == "__main__":
    print("  a PERFECT reranker, given the top c of stage one.")
    print("  It reorders by the human's own grades, so nothing can beat it")
    print("  on that candidate set. nDCG@5 against the whole corpus:\n")
    print("  c    candidates                   recall    nDCG@5")
    ideal = whole_corpus_ideal(5)
    for c in (3, 5, 6, 8):
        cands = STAGE_ONE[:c]
        got = ideal_of(cands, 5) / ideal
        rec = sum(1 for d in cands if LABELS[d] > 0) / \
              sum(1 for g in LABELS.values() if g > 0)
        print(f"  {c}    {' '.join(cands):26s}  {rec:.3f}     {got:.4f}")

    print("\n  so the reranker is not the thing that is broken at c=3:")
    print("  d7 has grade 3 and sits sixth in stage one, so no reordering")
    print("  of the first three can put it anywhere.")

    print("\n  the cost, as a count of forward passes through a model:")
    print("    corpus       bi-encoder   cross-encoder")
    for n in (1_000, 100_000, 1_000_000):
        print(f"    {n:9,d}             1   {n:13,d}")
    print("\n    two stages: 1 embedding + 1 search + 100 cross-encoder")
    print("    passes. The MIDDLE one is the only one that grows")
    print("    with n, and that is chapter 29's problem.")
```

```text
  a PERFECT reranker, given the top c of stage one.
  It reorders by the human's own grades, so nothing can beat it
  on that candidate set. nDCG@5 against the whole corpus:

  c    candidates                   recall    nDCG@5
  3    d1 d3 d2                    0.500     0.6740
  5    d1 d3 d2 d6 d8              0.750     0.7530
  6    d1 d3 d2 d6 d8 d7           1.000     1.0000
  8    d1 d3 d2 d6 d8 d7 d4 d5     1.000     1.0000

  so the reranker is not the thing that is broken at c=3:
  d7 has grade 3 and sits sixth in stage one, so no reordering
  of the first three can put it anywhere.

  the cost, as a count of forward passes through a model:
    corpus       bi-encoder   cross-encoder
        1,000             1           1,000
      100,000             1         100,000
    1,000,000             1       1,000,000

    two stages: 1 embedding + 1 search + 100 cross-encoder
    passes. The MIDDLE one is the only one that grows
    with n, and that is chapter 29's problem.
```

**Read the cost block first.** A bi-encoder needs one forward pass at query time, whatever the
collection size, because the documents were encoded in advance. A cross-encoder needs one pass
*per document*, so scoring a million documents means a million passes for one query. That is not
a tuning problem; it is the arrangement.

So the standard arrangement is two stages. **Reranking** means scoring a small set of candidates
with a more expensive method than the one that produced them, and the model that does it is a
**reranker**. The first stage is cheap and runs
over everything — BM25, dense retrieval, or both fused — and returns a **candidate set**, say the
top hundred. The second stage cross-encodes those hundred and reorders them. The cost is one
embedding, one search, and a hundred cross-encoder passes — and **the number of cross-encoder
passes** does not grow with the collection. The search does, which is chapter 29's subject: at a
million documents, comparing the query against every vector stops being free, and that is a
different problem from this one.

> **Note:** Two-stage retrieval with a cross-encoder is a current convention, in chapter 6's
> sense, and not settled practice: it is how most systems are built today, the arrangement is
> what to understand, and the specific models change constantly. Chapter 28 owns reranking as a
> step in assembling a context — how many candidates to keep, where the passages go, and how to
> cite them. This chapter owns only what the two encoder arrangements are and why there are two
> stages.

## What a Reranker Cannot Do, and Why That Is a Derivation

Now the top block, which is the more important half.

The reranker in that program is *perfect*. It does not estimate relevance; it reorders the
candidates by the human's own grades, so no real reranker can beat it. Watch what it achieves as
the candidate set grows: with three candidates it reaches nDCG@5 of 0.6740, with five 0.7530,
and with six 1.0000.

**The reason is not about rerankers at all.** `d7` has the top grade and sits sixth in stage
one's output. A reordering of a set cannot introduce an element that is not in the set, so no
function whatever of the first three candidates can place `d7` anywhere. This is a derivation
and not an observation — it holds for every reranker, every model and every collection, because
it is a property of reordering.

**So the candidate set is a ceiling.** Whatever the second stage is, it cannot retrieve; it can
only permute. If your answers are not in the hundred, buying a better reranker is spending money
on the wrong stage.

**Two quantities, and they are not the same one.** The `recall` column counts how many of the
relevant documents the candidate set contains, and reranking cannot raise it — permuting a list
does not add to it. The `nDCG@5` column is the best score any reordering of that set could
reach. At `c=5` these read 0.750 and 0.7530, which are nearly equal here and have no reason to
be: one counts documents and the other weighs grades by position. Do not read the near-match as
a law.

This is chapter 25's invisible miss, arriving with a number on it. The chapter said a missing
document leaves no trace in a result list; here the trace is in the gap between the reranked
score and 1.0, and you can only see it because somebody wrote the grades down.

## Measuring Hybrid Against Dense on Your Own Data

The chapter's problem said *no way to say which is better*. You now have the measures to try.
Here are both methods and their fusion, on two queries with grades — and the result is not the
one this section was expected to produce.

```python
import math
from bm25 import CORPUS, bm25
from fuse import rrf

# Two queries, and a human's grades for each. Query A is answered by meaning,
# query B by an exact string. The cosines are stipulated, as in chapters 24
# and 25: nothing here shows what a real model returns.
QUERIES = {
    "refund on a cancelled order": {
        "grades": {"d7": 3, "d2": 3, "d1": 2, "d6": 1,
                   "d3": 0, "d4": 0, "d5": 0, "d8": 0},
        "cosine": {"d7": 0.9891, "d2": 0.9874, "d1": 0.9702, "d6": 0.9312,
                   "d8": 0.9145, "d3": 0.8871, "d4": 0.6203, "d5": 0.6198},
    },
    # Chapter 25's residual, fallen the other way: the two notes are 0.0005
    # apart and the wrong one is on top. Nothing predicts which you get.
    "x-4471-d seal": {
        "grades": {"d4": 3, "d1": 0, "d2": 0, "d3": 0,
                   "d5": 0, "d6": 0, "d7": 0, "d8": 0},
        "cosine": {"d5": 0.99978, "d4": 0.99928, "d6": 0.9712, "d1": 0.8310,
                   "d2": 0.8265, "d7": 0.8102, "d8": 0.8044, "d3": 0.7701},
    },
}

def matched_ranks(scores):
    # Only documents that actually matched. An inverted index never returns a
    # document holding none of the query terms, and fusing a tail of zeros
    # would hand arbitrary positions a vote - the Warning earlier in the
    # chapter. fuse.py ranked all eight to show what that warning is about.
    hit = {d: s for d, s in scores.items() if s > 0}
    order = sorted(hit, key=lambda d: hit[d], reverse=True)
    return {d: place for place, d in enumerate(order, 1)}

def dense_ranks(scores):
    order = sorted(scores, key=lambda d: scores[d], reverse=True)
    return {d: place for place, d in enumerate(order, 1)}

def dcg(order, grades, k):
    return sum(grades[d] / math.log(i + 1, 2)
               for i, d in enumerate(order[:k], 1))

def ndcg(order, grades, k):
    ideal = sorted(grades, key=lambda d: grades[d], reverse=True)
    best = dcg(ideal, grades, k)
    return dcg(order, grades, k) / best if best else 0.0

def best_and_worst(fused, grades, k=5):
    # A tie has no ordering, so report the range it spans rather than
    # whichever one sorted() happened to emit.
    hi = sorted(fused, key=lambda d: (fused[d], grades[d]), reverse=True)
    lo = sorted(fused, key=lambda d: (fused[d], -grades[d]), reverse=True)
    return ndcg(hi, grades, k), ndcg(lo, grades, k)

if __name__ == "__main__":
    rows = {}
    for query, spec in QUERIES.items():
        grades, cos = spec["grades"], spec["cosine"]
        lex = {d: bm25(query, d) for d in CORPUS}
        lr, dr = matched_ranks(lex), dense_ranks(cos)
        fused = rrf([lr, dr])
        print(f"  query: {query}")
        print(f"    lexical matched {len(lr)} of {len(CORPUS)} documents")
        got = {}
        for name, order in (("lexical", sorted(lr, key=lambda d: lr[d])),
                            ("dense", sorted(dr, key=lambda d: dr[d]))):
            got[name] = ndcg(order, grades, 5)
            print(f"    {name:8s} {' '.join(order[:4])}"
                  f"   nDCG@5 {got[name]:.4f}")
        hi, lo = best_and_worst(fused, grades)
        got["fused"] = (hi, lo)
        tied = len({round(v, 12) for v in fused.values()}) < len(fused)
        print(f"    fused    nDCG@5 {lo:.4f} to {hi:.4f}"
              f"   ties present: {tied}")
        rows[query] = got
        print()

    print("  the tie on the identifier query, in full:")
    q = "x-4471-d seal"
    lex = {d: bm25(q, d) for d in CORPUS}
    lr = matched_ranks(lex)
    dr = dense_ranks(QUERIES[q]["cosine"])
    fused = rrf([lr, dr])
    for d in ("d4", "d5"):
        print(f"    {d}: lexical {lr[d]}, dense {dr[d]}"
              f"  ->  {fused[d]:.6f}")
    print("    the right note and the wrong one score the SAME.")

    print("\n  the same two notes, under each method. Both forms of the")
    print("  margin are given, because one of each invites a comparison")
    print("  across two scales that the chapter has just forbidden:")
    print(f"    lexical  d4 {lex['d4']:.4f}  d5 {lex['d5']:.4f}"
          f"   ratio {lex['d4']/lex['d5']:.2f}  gap {lex['d4']-lex['d5']:.4f}")
    cos = QUERIES[q]["cosine"]
    print(f"    dense    d5 {cos['d5']:.5f}  d4 {cos['d4']:.5f}"
          f"   ratio {cos['d5']/cos['d4']:.4f}  gap {cos['d5']-cos['d4']:.5f}")
    print("    what matters is not either number: d4 holds the term and")
    print("    d5 does not, so the lexical signal is categorical.")

    print("\n  nDCG@5 across both queries:")
    print("    method    meaning        identifier     mean")
    a_name = "refund on a cancelled order"
    for name in ("lexical", "dense"):
        a, b = rows[a_name][name], rows[q][name]
        print(f"    {name:8s}  {a:.4f}         {b:.4f}         {(a+b)/2:.4f}")
    fa_lo, fa_hi = rows[a_name]["fused"][1], rows[a_name]["fused"][0]
    fb_lo, fb_hi = rows[q]["fused"][1], rows[q]["fused"][0]
    print(f"    fused     {fa_lo:.4f}-{fa_hi:.4f}  {fb_lo:.4f}-{fb_hi:.4f}"
          f"  {(fa_lo+fb_lo)/2:.4f}-{(fa_hi+fb_hi)/2:.4f}")
    print(f"\n    dense's mean {(rows[a_name]['dense']+rows[q]['dense'])/2:.4f}"
          f" sits INSIDE the fused range.")
    print("    So this evidence does not say fusion beat dense.")
```

```text
  query: refund on a cancelled order
    lexical matched 6 of 8 documents
    lexical  d2 d7 d1 d3   nDCG@5 0.9319
    dense    d7 d2 d1 d6   nDCG@5 1.0000
    fused    nDCG@5 0.9319 to 0.9319   ties present: True

  query: x-4471-d seal
    lexical matched 2 of 8 documents
    lexical  d4 d5   nDCG@5 1.0000
    dense    d5 d4 d6 d1   nDCG@5 0.6309
    fused    nDCG@5 0.6309 to 1.0000   ties present: True

  the tie on the identifier query, in full:
    d4: lexical 1, dense 2  ->  0.032522
    d5: lexical 2, dense 1  ->  0.032522
    the right note and the wrong one score the SAME.

  the same two notes, under each method. Both forms of the
  margin are given, because one of each invites a comparison
  across two scales that the chapter has just forbidden:
    lexical  d4 2.8466  d5 1.1867   ratio 2.40  gap 1.6599
    dense    d5 0.99978  d4 0.99928   ratio 1.0005  gap 0.00050
    what matters is not either number: d4 holds the term and
    d5 does not, so the lexical signal is categorical.

  nDCG@5 across both queries:
    method    meaning        identifier     mean
    lexical   0.9319         1.0000         0.9659
    dense     1.0000         0.6309         0.8155
    fused     0.9319-0.9319  0.6309-1.0000  0.7814-0.9659

    dense's mean 0.8155 sits INSIDE the fused range.
    So this evidence does not say fusion beat dense.
```

**The margin block is chapter 25's complaint, quantified.** On the identifier query, the two
near-identical maintenance notes sit 1.6599 apart under BM25 and 0.00050 apart under the cosine.
Both forms of each margin are printed on purpose, because quoting one as a ratio and the other
as a gap is the cross-scale comparison this chapter spent a section forbidding. The thing that
actually matters is not a number at all: `d4` holds the term `x-4471-d` and `d5` does not, so one
gets that term's IDF and the other gets nothing. The lexical signal is categorical. The dense
signal is a residual, it fell the wrong way here, and the dense ranking put the wrong note
first — which cost it 0.6309 against lexical's 1.0000.

**Now read the fused row, because this is where the section turns.** On the identifier query
`d4` and `d5` score *exactly* the same fused value, 0.032522. It is the tie from two sections
ago, arriving where it costs something: `d4` is lexical-first and dense-second, `d5` is the
reverse, and reciprocal rank fusion cannot tell `(1, 2)` from `(2, 1)`. **So the right note and
the wrong note are tied, and which one a user sees is decided by nothing.**

That is why the fused column is a range rather than a number. If the tie breaks towards `d4` the
fused nDCG@5 is 1.0000; if it breaks towards `d5` it is 0.6309. The same structural tie appears
on the meaning query and costs nothing there, because the two tied documents are both grade 3 —
which is the clearest possible illustration that a tie is harmless until it is not.

**And now the honest reading of the means.** Lexical scored 0.9659, dense 0.8155, and fusion
somewhere between 0.7814 and 0.9659. **Dense's 0.8155 sits inside the fused range**, so this
measurement does not establish that fusion beat dense. Fusion never beat lexical on either
query, and its best case only ties it.

**Hybrid retrieval** runs lexical and dense retrieval and combines the rankings. What this
chapter has shown about it is narrower than the usual claim and worth saying exactly: on two
queries with stipulated cosines, fusion put nothing in the top five that lexical had not already
found there, and one of its two results was a coin flip. (It did surface `d6`, a grade-1
document, that lexical missed entirely — at rank 7, where nDCG@5 cannot see it.) That is not a verdict on hybrid retrieval. It is a
demonstration that you cannot get a verdict this way.

> **Warning:** Do not take "fusion is a hedge that trades the best case for a better floor" from
> this. It is a popular formulation and it is false as a general claim, because fusion can beat
> *both* of its inputs outright: a document at rank 2 in both lists scores 0.032258, which wins
> against documents at `(1, 8)` and `(8, 1)` on 0.031099 each, so if that middling document is
> the relevant one, fusion scores 1.0000 where each input scores 0.6309. It runs the other way
> too: that same `(2, 2)` document is beaten by documents at `(1, 3)` and `(3, 1)`, which score
> 0.032266 against its 0.032258, so it falls to third and fusion scores 0.5000 where both inputs
> score 0.6309. The reason is that `\(1/x\)`{=latex} is convex, so spreading two ranks apart
> beats keeping them together — `\(1/61 + 1/63 > 2/62\)`{=latex}. Fusion is not bounded by its
> inputs in either direction. Whether it helps *you* is a measurement.

> **Warning:** Two queries measure nothing, and the range above is the proof rather than a
> caveat: a result that moves 0.19 depending on a tie-break has no business being compared with
> anything. Chapter 20 is how this is done properly — the bootstrap for the interval, and a
> paired comparison, because both methods run on the identical queries and that is exactly the
> case where pairing buys the most.

That is the method, then. Write the key once. Run each configuration over the same queries,
enough of them that one tie cannot move the answer. Compare paired, with an interval. Keep the
configuration that wins and say by how much, with the uncertainty attached.

## Lab: Build Both Searches and Score Them

Four programs, pure Python, nothing to install. About an hour, and there is a key for every
step. Work in a new empty folder.

**Step 1.** Save the first program as `bm25.py` and run it.

*Expected result:* eight documents, average length 8.500 terms; `x-4471-d` worth 1.7918 against
`the` at 0.4925; the classic column negative for `the` at `\(-0.4520\)`{=latex}; and `d1` first
on *refund policy* with `d3` second. `d3` is six repetitions of *refund*; the printed line
truncates the document text at 34 characters, so only five of them show.

**Step 2.** In `bm25.py`, change the `k1 = 1.5` inside `__main__` to `0.0` and run it again.
There are two `k1`s — that one, and the default in `def bm25(...)` — and this step wants the
local one, because it is what the saturation block uses. (Changing the function default instead
leaves that block untouched and silently ties `d3` with `d2` in the ranking below it, which is a
worthwhile thing to try afterwards.)

*Expected result:* the saturation block collapses. Every term frequency gives exactly 1.0000
IDF, because with `\(k_1 = 0\)`{=latex} the fraction becomes
`\(f_{t,d} \cdot 1 / f_{t,d}\)`{=latex}, which is 1 whatever the count. So `\(k_1 = 0\)`{=latex}
means *ignore how often a term appears and only ask whether it appears at all*. The knob
interpolates between presence and count.

**Step 3.** Put the local `k1` back to `1.5`, then set `b` to `0.0` in the `def bm25(...)`
signature — that one is unambiguous, since `b` appears nowhere else — and run it. Watch the
`refund policy` ranking at the bottom.

*Expected result:* both scores *fall* — `d1` from 3.1536 to 2.7362 and `d3` from 1.9761 to
1.8889 — and the reason is worth working out, because the obvious prediction is wrong. `d1` and
`d3` are *both six terms long*, against a collection average of 8.500, so neither was being
penalised for its length; both were being *rewarded* for being shorter than average, and
`\(b = 0\)`{=latex} removes that reward. `d1` falls further because it matches two terms once
each, and the length constant competes with `\(f_{t,d}\)`{=latex} in the denominator — so the
smaller the term frequency, the more of the score that constant decides. The two knobs are
independent: `\(k_1\)`{=latex} controls saturation, `\(b\)`{=latex} controls length.

**Step 4.** Save the second program as `fuse.py` and run it. Check the `d7` arithmetic by hand.

*Expected result:* `d2` and `d7` tied at 0.032522, and `1/62 + 1/61 = 0.016129 + 0.016393`. If
you get a different total, you have added the ranks rather than their reciprocals.

**Step 5.** In `fuse.py`, call `rrf([lex_r, dense_r], k=0)` and run it again.

*Expected result:* **the ordering does not change at all** — it is `d2 d7 d1 d3 d6 d4 d8 d5` at
`\(k = 0\)`{=latex} just as it was at 60, and the same at 1, 10 and 1000. That is worth sitting
with, because it is easy to assume a constant that big must reorder something. What `\(k\)`{=latex}
changes is the *size* of the gaps, not their direction: at `\(k=0\)`{=latex} first place is worth
0.5 more than second rather than 0.000264 more, so one list's top pick would dominate a fusion of
*many* lists — with two lists of eight documents, the agreement between them already decides the
order. And `d2` and `d7` still tie, at every `\(k\)`{=latex}: the tie is structural, since
`\(1/(k+1) + 1/(k+2)\)`{=latex} is the same sum whichever way round it is added.

**Step 6.** Save the third program as `measures.py` and run it. Then answer this before reading
on: MRR says 1.000 and nDCG@5 says 0.6216 for the same ranking. Which one is wrong?

*Expected result:* neither. They measure different things, and the ranking really is perfect at
the thing MRR measures — the first result has a non-zero grade, so the reader looked no further
than position one. nDCG also weighs *how good* each result was and *where* it sat, and it can
see that a grade-3 document is at position six. If you find yourself wanting one number, you
have to say which question you are asking first.

**Step 7.** In `measures.py`, change `RANKING` to put `d7` first and `d1` sixth.

*Expected result:* MRR stays at 1.000 — it was already at its maximum and cannot report the
improvement — while nDCG@5 rises. This is the clearest demonstration in the chapter that a
measure at its ceiling has stopped being able to tell you anything.

**Step 8.** Save the fourth program as `stages.py` and run it.

*Expected result:* a perfect reranker reaching 0.6740 on three candidates, 0.7530 on five and
1.0000 on six. Then say in one sentence why buying a better reranker cannot fix the `c=3` row.

**Step 9.** Save the fifth program as `hybrid.py` and run it.

*Expected result:* lexical 0.9659 mean, dense 0.8155, and the fused mean reported as a *range*,
0.7814 to 0.9659 — with dense's 0.8155 inside it. The reason the fused figure is a range is the
tie the program prints just above: on the identifier query the right note and the wrong one both
score 0.032522. Say what you would need before claiming fusion is better than either method
here. The answer is in chapter 20: an interval, from enough queries that a single tie cannot
move it, computed paired.

**Step 10.** Add a third query to `hybrid.py` whose answer needs meaning *and* an identifier —
something like *the seal on X-4471-D*. Grade the eight documents yourself first, writing the
grade definitions down before you look at any score.

*Expected result:* your own. The point of the step is the order of operations: the grades come
before the scores, or they are not a key, they are a rationalisation.

## Summary, Key Terms, and Review Questions

### Summary

**Lexical retrieval** scores a document by the query terms it contains, and **BM25** is the
standard way to do it. It answers three objections in order: **term frequency** says a document
mentioning a term often is more about it; **inverse document frequency** says a term in few
documents is worth more than a term in many, since otherwise *the* would dominate; and document
length says a long document mentions everything more often without being more about any of it.
Two properties are worth carrying and the constants are not. Term frequency **saturates** — a
hundred mentions reached 98.5% of a ceiling of `\((k_1+1)\)`{=latex} IDF, which is why a document
consisting of *refund* six times lost to one matching two query terms once each — and the
classic IDF goes **negative** for a term in more than half the collection, which is why the
modern form adds one inside the logarithm. `\(k_1\)`{=latex} and `\(b\)`{=latex} are tuned
constants, not derived ones.

Two searches cannot be added, because neither score has a unit: BM25 ran 0 to 5.5089 and the
stipulated cosines 0.6198 to 0.9891, so a sum is whatever weight you implied. **Reciprocal rank fusion**
discards the scores and sums `\(1/(k + \mathrm{rank})\)`{=latex} across rankings, which needs
nothing from either system but an ordering — and pays for it by tying two documents at exactly
0.032522 because `(1, 2)` and `(2, 1)` are indistinguishable to it. Its `\(k\)`{=latex}, usually
60, sets how much a first place is worth: the gap between rank 1 and rank 2 is 0.5 at
`\(k=0\)`{=latex} and 0.000264 at `\(k=60\)`{=latex}.

A **bi-encoder** encodes query and documents separately, so every document vector is computed
before any query arrives and query time costs one forward pass. **A bi-encoder is not by itself
an escape from chapter 25's symmetry limit**: chapter 24's dense retrieval puts both sides
through the *same* model, which is precisely the arrangement that cannot answer a directed
question. The escape is any arrangement that puts the two sides through different *functions*:
the **two-tower** form, with separate query and document encoders giving
`\(\cos(f(q), g(d))\)`{=latex} and `\(f \neq g\)`{=latex}, or — chapter 25's other
sub-variant, and how much of current practice does it — one shared model told which side it is
encoding by a `query:` or `passage:` marker. Both keep the precomputation and give up the
symmetry, so **shared weights and symmetry are different claims**: what forces symmetry is the
same function on both sides. A **cross-encoder** is the first
one: it puts the pair through one model together, so nothing is precomputable and a million
documents cost a million forward passes, and the score is free to be asymmetric. Hence two
stages: retrieve cheaply over everything, then **rerank** a
**candidate set** of about a hundred. **The candidate set is a ceiling, and that is a
derivation**: reordering a set cannot introduce an element not in it, so a *perfect* reranker
reached only 0.6740 on three candidates and 1.0000 on six, and the grade-3 document sitting
sixth in stage one could not be rescued by any reordering of the first three.

Measuring needs **graded relevance** — chapter 25's binary judgement extended to a small scale,
with written definitions two people would apply the same way. **Recall@k** asks only whether the
relevant documents arrived and is blind to their order, which makes it right for a first stage
and wrong for what a user sees. **Reciprocal rank** is one over the position of the first
relevant result, and on the chapter's ranking it is 1.000 while **nDCG@5** is 0.6216: MRR cannot
see a grade-3 document at position six because it stops at the first non-zero grade. **DCG**
divides each grade by `\(\log_2(i+1)\)`{=latex} and sums; the logarithm is a convention, chosen
because it decays slowly, and *not* forced. What is derivable is that the base cancels — base 2,
10 and `\(e\)`{=latex} gave DCGs of 3.9307, 13.0574 and 5.6708 and an identical nDCG of
0.621602, because changing base scales DCG and ideal DCG by the same constant. The **gain**
convention does not cancel: grade directly gave 0.6216 and `\(2^{g}-1\)`{=latex} gave 0.5193, so
two tools' nDCGs are not comparable without knowing both conventions.

**Hybrid retrieval** combines the two rankings, and the attempt to measure it is the chapter's
most useful failure. Lexical scored 0.9659 across the two queries and dense 0.8155, but the
fused score on the identifier query is not a number: `d4` and `d5` tie at *exactly* 0.032522,
being `(1, 2)` and `(2, 1)`, so the right note and the wrong one score the same and the fused
nDCG@5 is 1.0000 or 0.6309 according to a tie-break. The fused mean is therefore a range,
0.7814 to 0.9659, **and dense's 0.8155 falls inside it** — so the measurement does not establish
that fusion beat dense, and fusion never beat lexical at all. The same tie occurs on the meaning
query and costs nothing, because both tied documents are grade 3. **Do not carry away "fusion is
a hedge that trades the best case for a better floor"**: fusion can beat both inputs outright, as
a document at rank 2 in both lists does on 0.032258 against `(1, 8)` and `(8, 1)` on 0.031099.
Fusion is not bounded by its inputs in either direction, and two queries with stipulated cosines
settle nothing — chapter 20 is the interval and the paired comparison.

### Key Terms

| Term | Meaning |
|---|---|
| **Lexical retrieval** | Scoring a document by the query terms it contains. Not a filter: every document gets a number and the list is sorted |
| **Term** | The unit a lexical index counts — usually a lower-cased word, sometimes stemmed. Not the model's token from chapter 10 |
| **Term frequency** | How often a term appears in one document |
| **Document frequency** | How many documents in the collection contain a term at all |
| **Document length** | How many terms a document holds, compared with the collection average. BM25's third input, and the reason a long document is not automatically more relevant |
| **Inverse document frequency** | A weight that rises as a term gets rarer, so a term almost every document holds barely moves a score |
| **BM25** | The standard lexical scoring function, combining term frequency, inverse document frequency and document length, with a saturating term-frequency curve |
| **Reciprocal rank fusion** | Combining rankings by summing one over a constant plus each rank, using positions only and never the scores |
| **Hybrid retrieval** | Running lexical and dense retrieval and combining their rankings |
| **Bi-encoder** | Query and document encoded separately and compared by a cosine, so document vectors are precomputable. With one shared model the score is symmetric |
| **Two-tower** | A bi-encoder with separate query and document encoders, so the score is `\(\cos(f(q), g(d))\)`{=latex} with `\(f \neq g\)`{=latex}: still precomputable, no longer symmetric |
| **Cross-encoder** | Query and document passed through one model together, giving one score for the ordered pair. Not precomputable; free to be asymmetric |
| **Reranking** | Rescoring a small candidate set with a more expensive method than the one that produced it |
| **Reranker** | The model that does the rescoring in the second stage — in current practice usually a cross-encoder |
| **Candidate set** | The documents the first stage passes to the second. A reranker can only permute it, so it is a ceiling |
| **Graded relevance** | A relevance judgement on a small scale rather than yes-or-no, so a partial answer and a full one can be told apart |
| **Recall@k** | The fraction of all relevant documents appearing in the top k. Blind to their order |
| **Reciprocal rank** | One divided by the position of the first relevant result, for a single query |
| **Mean reciprocal rank** | The average of the reciprocal rank over a set of queries |
| **Discounted cumulative gain** | The sum of each result's grade divided by a discount that grows with position |
| **Normalised discounted cumulative gain** | A DCG divided by the DCG of the best possible ranking of the same documents, making it comparable across queries |

### Worth Memorising

| Item | Value or formula |
|---|---|
| BM25 | `\(\sum_{t \in q} \mathrm{IDF}(t) \cdot \dfrac{f_{t,d}(k_1+1)}{f_{t,d} + k_1(1 - b + b|d|/\mathrm{avgdl})}\)`{=latex} |
| Its two knobs | `\(k_1 \approx 1.5\)`{=latex} controls saturation, `\(b \approx 0.75\)`{=latex} controls length normalisation. Tuned constants, not derived |
| What `\(k_1 = 0\)`{=latex} does | Makes term frequency irrelevant: the factor is 1 whatever the count, so only presence matters |
| Term-frequency ceiling | A term's contribution approaches `\((k_1+1)\)`{=latex} IDF. At `\(k_1=1.5\)`{=latex}, 100 mentions reach 98.5% of 2.5 IDF |
| Inverse document frequency | `\(\ln\!\left(\dfrac{N - n_t + 0.5}{n_t + 0.5} + 1\right)\)`{=latex}. Without the `+1` it goes negative for a term in over half the collection |
| Reciprocal rank fusion | `\(\sum_{r} 1/(k + \mathrm{rank}_r(d))\)`{=latex}, conventionally `\(k = 60\)`{=latex}. Uses ranks only, so no score comparability is needed |
| DCG | `\(\sum_{i=1}^{k} g_i / \log_2(i+1)\)`{=latex} |
| nDCG | DCG divided by the DCG of the ideal ordering of the same documents |
| Change of base | `\(\log_c x = \ln x / \ln c\)`{=latex}, so a base-`\(c\)`{=latex} DCG is `\(\ln c\)`{=latex} times the natural-log one |
| The log base cancels | A derivation: changing base scales DCG and ideal DCG by the same `\(\ln c\)`{=latex}. Base 2, 10 and e all gave nDCG 0.621602 |
| The gain convention does not | Grade directly gave 0.6216; `\(2^{g}-1\)`{=latex} gave 0.5193 on the same ranking |
| Why a logarithm at all | Convention, not derivation. It must decrease with position; a log decays slowly, which roughly matches how lists are read |
| Recall@k against MRR | Recall ignores order, so it suits a first stage. MRR stops at the first non-zero grade, so it cannot see a better answer further down |
| The reranking ceiling | A derivation: reordering a set cannot add to it, so the candidate set bounds everything the second stage can achieve |
| Cross-encoder cost | One forward pass per document per query, so a million documents cost a million passes. Hence two stages |
| What forces symmetry | Putting both sides through the *same function*, as chapter 24's dense retrieval does. Shared weights alone do not: one model given a `query:` or `passage:` marker is not symmetric |
| What merely permits asymmetry | A two-tower bi-encoder and a cross-encoder are *free* to be asymmetric, not guaranteed to be |

### Review Questions

1. What is BM25 doing, roughly?
2. What is the difference between a bi-encoder and a cross-encoder, and where does each belong?
3. What is nDCG, and why is there a logarithm in it?
4. You have two rankings of the same documents. How do you combine them?
5. Your reranker is not helping. What do you check first?
6. Is hybrid retrieval better than dense retrieval?

### Review Answers

1. It scores a document by the query terms it contains, and the way to say it is as three
objections answered in order. Term frequency: a document that mentions *refund* four times is
plausibly more about refunds than one that mentions it once. Inverse document frequency, because
term frequency alone rewards the wrong words — *the* appears everywhere and means nothing — so a
term is weighted by how rare it is across the collection. Document length, because long documents
mention everything more often without being more about any of it. Then the two properties worth
knowing above the formula. **Term frequency saturates**: the contribution climbs to a ceiling of
`\((k_1+1)\)`{=latex} IDF, so a hundred mentions are worth about 2.5 IDF and not a hundred times
one mention, which is what stops keyword stuffing from working — in the chapter's corpus a
document of six *refund*s lost to one matching two terms once each. And the classic IDF goes
negative for a term in more than half the collection, which is why the modern form has a `+1`
inside the logarithm. Finish by saying `\(k_1\)`{=latex} and `\(b\)`{=latex} are tuned constants
rather than derived ones, because knowing which parts of a formula are chosen is the thing that
separates understanding it from reciting it.
2. A bi-encoder puts the query through a model and each document through a model separately, then
compares the two vectors with a cosine. A cross-encoder puts the query and one document through a
model *together* and gets one score for the pair. Two consequences follow and they are what the
question is really about. **Cost:** a bi-encoder's document vectors do not depend on the query,
so they are computed once in advance and query time is one forward pass however large the
collection; a cross-encoder cannot precompute anything, so scoring a million documents is a
million forward passes for one query. **Shape:** a cross-encoder's score is a function of the
ordered pair, so it can be asymmetric and can relate the two texts directly, which is exactly
what chapter 25 showed a *shared* encoder with a cosine cannot do for a directed question. Then
the correction that most answers to this question get wrong: a bi-encoder is not automatically
symmetric either. What forces symmetry is putting both sides through the *same function*, which
chapter 24's dense retrieval does. A two-tower bi-encoder uses separate query and document
encoders, so its score is `\(\cos(f(q), g(d))\)`{=latex} with `\(f \neq g\)`{=latex} —
precomputable *and* directed. So does a single shared model told which side it is encoding by a
`query:` or `passage:` marker, which is how much of current practice does it, and which shows
that *shared weights* and *symmetric* are not the same claim. So each belongs where its cost allows: the bi-encoder over
the whole collection, the cross-encoder over a candidate set of about a hundred that the first
stage produced. And the limit worth adding: the
second stage can only permute what the first stage found, so a cross-encoder cannot rescue an
answer that never made the candidate set.
3. nDCG is a ranking score that sees both how good each result is and where it sat. Build it in
three steps. DCG adds up each result's grade divided by a discount that grows with its position,
`\(\sum g_i / \log_2(i+1)\)`{=latex}, so a good answer low down counts for less than the same
answer at the top. The *normalised* part divides that by the DCG of the best possible ordering of
the same documents, which makes the number comparable across queries that have different numbers
of relevant documents. On the chapter's ranking that is 3.9307 over 6.3235, or 0.6216. As for the
logarithm, the honest answer has two halves and the second is the one that impresses. **Why a
decreasing discount at all** is obvious: position matters. **Why specifically a logarithm is a
convention and not a derivation** — it decays slowly, so the gap between positions 1 and 2 is
large and the gap between 10 and 11 is small, which roughly matches how people read a list; that
is a design intuition, not a theorem, and other discounts exist. What *is* derivable is that the
base does not matter: since `\(\log_c x = \ln x / \ln c\)`{=latex}, changing base multiplies
every term by the same `\(\ln c\)`{=latex}, so it scales the DCG and the ideal DCG equally and
the ratio is unchanged — base 2, 10 and `\(e\)`{=latex} all give 0.621602, and 3.9307/5.6708 is
`\(\ln 2\)`{=latex}. What is exact is the cancelling; those two printed figures are rounded, so
their quotient matches `\(\ln 2\)`{=latex} only to six decimals. The thing that genuinely does not cancel is the gain convention: using the
grade directly gives 0.6216 where `\(2^{g}-1\)`{=latex} gives 0.5193, so two nDCGs from different
tools are not comparable until you know both conventions and both `\(k\)`{=latex}.
4. Not by adding the scores, and the reason is the first thing to say: neither score has a unit.
BM25 ran from 0 to 5.5089 on the chapter's corpus while its stipulated cosines ran 0.6198 to
0.9891 — and the ranges are illustrative, the absence of a common unit is not — so a sum
is dominated by whichever happens to have the wider range, and any rescaling that fixes it is a
weight you chose rather than one the data gave you. Chapter 24 already established that a raw
cosine means nothing on its own. The standard answer is reciprocal rank fusion: throw the scores
away, keep the positions, and give each document `\(\sum_r 1/(k + \mathrm{rank}_r(d))\)`{=latex}
with `\(k\)`{=latex} usually 60. It needs nothing from the two systems but an ordering, which is
precisely why it works where addition does not. Then give the two caveats, because they are what
show you have used it. It discards information, so a document ranked first-then-second ties
*exactly* with one ranked second-then-first — 0.032522 in the chapter. And fuse only the top of
each list: a lexical ranking's tail is all zero scores whose order is arbitrary, and feeding that
into the fusion gives it votes it has not earned.
5. Whether the answers are in the candidate set, before anything else. The second stage can only
reorder what the first stage handed it, so if the right document is not in the hundred, no
reranker can place it anywhere — and that is a derivation, not an observation: reordering a set
cannot introduce an element not in the set. The measurement to make is the first stage's recall at
the candidate-set size. The chapter's own numbers show it: a *perfect* reranker, reordering by the
human's own grades, scored 0.6740 on three candidates and 1.0000 on six, and the difference is
entirely whether a grade-3 document was in the set. So check recall@c first; if it is low, the
money belongs in the first stage — a better embedding model, or lexical retrieval alongside
it — and not in the reranker. How many candidates to keep is its own trade and chapter 28's to
make. Only once recall@c is high does the reranker's
quality become the binding constraint.
6. Nobody knows from two queries, and saying so is the answer. The chapter tried it: lexical
scored 0.9659 across its two queries and dense 0.8155, and the fused score could not be reported
as a number at all. On the identifier query the right note and the wrong note **tie exactly** at
0.032522 under reciprocal rank fusion, because one is `(1, 2)` and the other is `(2, 1)` and the
formula cannot tell those apart — so the fused nDCG@5 is 1.0000 or 0.6309 depending on a
tie-break, the fused mean is a range of 0.7814 to 0.9659, and dense's 0.8155 sits inside that
range. A measurement that moves 0.19 on a tie-break is not evidence about anything.

Then refuse the formulation most people offer, because it is the part an interviewer is
listening for. **Fusion is not a hedge that trades the best case for a better floor.** It is not
bounded by its inputs in either direction, and both halves of that are worth being able to show.
*Above:* a document ranked 2 in both lists scores 0.032258 and beats documents at `(1, 8)` and
`(8, 1)` on 0.031099, so fusion can score 1.0000 where both of its inputs score 0.6309.
*Below:* the same `(2, 2)` document scores 0.032258 while documents at `(1, 3)` and `(3, 1)`
each score 0.032266, so it falls to third — fusion 0.5000 against 0.6309 in both inputs. The
reason is that `\(1/x\)`{=latex} is convex, so for a fixed pair of positions, spreading the two
ranks apart beats keeping them together: `\(1/61 + 1/63 > 2/62\)`{=latex}. So the answer is a method rather
than a verdict: write an answer key, run both configurations over the same queries — enough of
them that one tie cannot move the result — and compare them paired with an interval, which is
chapter 20. Whether hybrid helps depends on the mix of queries your users actually send, and
nothing deduces that.

> **You understand this when** you can say why two retrieval scores cannot be added and what
> reciprocal rank fusion gives up instead — and name the one check to run before blaming a
> reranker, with the one-sentence reason it is a derivation rather than a guess.
