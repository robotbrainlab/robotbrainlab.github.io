# Lab: Two Embedding Models, and the Query That Breaks Them

Chapter 24 built dense retrieval and chapter 25 catalogued where it fails, and both of them said,
at every point an argument turned on a number, that the vectors were written out by hand and that
nothing in them showed what a real model does. Chapter 25's Note asks for one thing: *check the
premise on your own data in one line as soon as you have a model.* This chapter is that line, and
then the search it makes possible — forty real documents embedded twice, a dozen queries read by
hand, and the query that breaks both models.

*The problem.* I want to see dense search fail on an exact term with my own eyes.

*The question.* What does a real embedding model actually do with the cases chapters 24 and 25
could only stipulate — and what can twelve queries read by hand tell you?

> **Note:** As in chapters 40 to 42, the `text` blocks are one real run, and here the split between
> what reproduces and what does not is itself one of the chapter's results. **The cosines move.**
> The same string embedded twice does not come back quite the same, so any figure a program
> re-fetches drifts by a few ten-thousandths, on both models: a margin printed as 0.1102 was
> 0.1101 on another run, and step 5's lower range end moved from 0.361 to 0.365 — the third
> decimal, not the fourth. So read the digits as one run's, quote them to two places, and build
> nothing on a third. **Every count held across four runs**, one of them with the forty document
> vectors re-fetched from scratch: the twelve first results, the two groupings in step 5, and step
> 6's listing. [**Two ranks are not safe**]{.noindex}, and step 4 says why. The three delivery
> pages in the `PA20` top three on the smaller model are separated by less than the drift, and the
> order inverted on one run in dozens. `sku-conventions`'s fourth place rests on a gap about ten
> times the drift, which held on every run but one — enough to be worth checking and not enough to
> be worth trusting silently. A rank whose margin is of the order of the noise is a lesson rather
> than a defect. What the cache does is hold the *document* side still, which is why
> steps 3 to 6 can move on the query side only.

> **Note:** What this lab costs before you run it. It embeds forty documents twice — about 9,700
> tokens each way — and about a hundred short texts besides. Embeddings are the cheapest thing a
> provider sells, and the whole lab is a small fraction of a penny; it is the first lab in the book
> whose cost is not worth a sentence of planning. Thirty-five minutes, nearly all of it reading.

## Step 1: Embed Forty Documents, Twice

Make a folder, put the corpus in it, and set the key:

```text
  mkdir -p ~/sandbox/ch43 && cd ~/sandbox/ch43
  python3 -m venv .venv && source .venv/bin/activate
  cp -r <where you unpacked the book's labs>/corpus .
  export OPENAI_API_KEY="sk-..."
```

```python
"""Embed the shipped corpus twice, and keep the vectors in a file.

Chapters 24 and 25 argued with vectors written out by hand and said
so at every point the argument turned on one. These are real. The
cache matters more than it looks, and not for the reason you would
guess: the same string embedded twice does not come back quite the
same, so fetching the forty documents once holds one side of every
comparison still.
"""

import json
import os
import pathlib
import urllib.request

ROOT = pathlib.Path(os.environ.get("CORPUS", "corpus"))
CORPUS = ROOT / "docs"
URL = "https://api.openai.com/v1/embeddings"
TIMEOUT = 120
MODELS = ("text-embedding-3-small", "text-embedding-3-large")
CACHE = pathlib.Path("vectors.json")


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def embed(texts, model):
    """One call for a batch. Returns (vectors, prompt_tokens, served).

    `served` is the model string the response came back with. These
    two models have no dated snapshot to pin, so the name you asked
    for is all there is - which makes printing what replied the only
    check available. Chapter 54 owns what happens when it moves.
    """
    body = json.dumps({"model": model, "input": texts}).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    rows = sorted(d["data"], key=lambda x: x["index"])
    return ([x["embedding"] for x in rows],
            d["usage"]["prompt_tokens"], d["model"])


def docs():
    paths = sorted(CORPUS.glob("*.md"))
    return [p.stem for p in paths], [p.read_text() for p in paths]


if __name__ == "__main__":
    ids, texts = docs()
    out = {"ids": ids}
    print(f"  {len(ids)} documents from {CORPUS}\n")
    for m in MODELS:
        vecs, tokens, served = embed(texts, m)
        out[m] = vecs
        print(f"  asked for {m}")
        print(f"    replied   {served}")
        print(f"    {len(vecs[0])} numbers per document, {tokens} tokens in")
    CACHE.write_text(json.dumps(out))
    size = CACHE.stat().st_size
    floats = sum(len(v) for m in MODELS for v in out[m])
    print(f"\n  wrote {CACHE}, {size/1e6:.1f} MB for {len(ids)} documents")
    print(f"  the same {floats} numbers as 4-byte floats would be"
          f" {floats*4/1e6:.2f} MB")
    print(f"  one vector of {len(out[MODELS[1]][0])} floats is"
          f" about {len(json.dumps(out[MODELS[1]][0]))/1024:.0f} kB"
          " as text")
```

```text
  40 documents from corpus/docs

  asked for text-embedding-3-small
    replied   text-embedding-3-small
    1536 numbers per document, 9740 tokens in
  asked for text-embedding-3-large
    replied   text-embedding-3-large
    3072 numbers per document, 9740 tokens in

  wrote vectors.json, 3.8 MB for 40 documents
  the same 184320 numbers as 4-byte floats would be 0.74 MB
  one vector of 3072 floats is about 62 kB as text
```

**Three things in that output are worth more than they look.**

**The first two lines of each block are the model check, and here it buys less than usual.**
Chapters 40 to 42 pinned a dated snapshot and printed the name that replied, because the provider
publishes one. These two embedding models have no dated snapshot to pin: `text-embedding-3-small`
is the whole of the name there is. So printing what replied is the only check available, every
figure in this chapter is a figure about those two names rather than about two fixed sets of
weights, and a name that starts serving something else is chapter 54's subject with nothing in
between.

**The token count is identical for both models**, 9,740 either way, because both read the same
forty documents — and the same input gives the same count only if the two vocabularies agree, so
that equal total is consistent with their sharing one and does not establish it; what would is a string the two vocabularies disagree about. Chapter 40 measured that
directly and found the
embedding endpoint's vocabulary disagreeing with the chat model's by a factor of 3.25 on one
string; here the two embedding models agree exactly, which is a fact about these two and not a
rule.

**The width is fixed and it is the whole of what you get.** 1,536 numbers for one model and 3,072
for the other, and that width does not change with the document: the eight-hundred-word warranty
document and the shortest page in the corpus come back the same size. That is chapter 24's fixed
width, and it is the premise under every failure chapter 25 lists — one vector has to stand for
the whole text, so anything appearing once competes for that room with everything else.

**And the storage is not small, on either reading.** Forty documents of a few hundred words each
produce 3.8 MB of JSON, with one of the larger vectors taking about 62 kB written out as text —
and the same numbers as four-byte floats are 0.74 MB, which is the figure to scale with, since
nobody stores vectors as decimal text. A real collection is a
million documents, and the arithmetic from there is chapter 29's subject rather than this
chapter's — but the number is worth having in your hand once, because *embed everything* sounds
free and is not.

> **Note:** The cache is doing two jobs, and neither is saving money at this price. It holds the
> document side of every comparison still, so any difference between two runs of step 3, 4, 5 or 6
> has to come from the query — which is how the opening Note's split was found. And it keeps the
> forty vectors consistent with each other, which matters because a corpus half embedded by one
> call and half by another is a corpus whose documents are not strictly comparable. What it does
> not do is make anything exact, and two of this chapter's programs do not use it at all: `premise`
> and `check25` embed every text fresh on every run, which is why their figures drift even though
> the cache exists. The one other thing to watch is that the file is keyed by model name, and a
> name that starts serving something else is chapter 54's subject.

## Step 2: Chapter 25's Premise, on a Real Model

Chapter 25's argument rests on a premise it could not check: that a model places two texts
differing in one token very close together. It stipulated 0.99983 for a pair of maintenance notes
differing in a part code, and 0.99976 for a sentence and its negation, and it said in a Note that
both were typed numbers and that the premise is an observation this book cannot derive. Here is
the one line it asks for.

```python
"""Chapter 25's premise, checked on a real model.

Chapter 25 stipulated two pairs of vectors and said at each one
that it could not show a model really places such texts that close.
Its Note asks for exactly this check, in one line, as soon as a
model is to hand. Here are its two pairs, plus a paraphrase pair of
chapter 24's kind and a floor of this chapter's own.
"""

import json
import math

from embed import MODELS, embed

PAIRS = [
 ("a part code, one token in ten",
  "Replace the seal on pump X-4471-B before servicing the unit.",
  "Replace the seal on pump X-4471-D before servicing the unit."),
 ("a negation, one token in five",
  "Your refund was approved.",
  "Your refund was not approved."),
 ("one question, two phrasings",
  "How long do I have to send something back?",
  "What is the return window for an unwanted item?"),
 ("two topics, as a floor",
  "Your refund was approved.",
  "The kettle boils one litre in about two minutes forty."),
]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x*x for x in a))
                  * math.sqrt(sum(y*y for y in b)))


if __name__ == "__main__":
    texts = [t for _, a, b in PAIRS for t in (a, b)]
    print("  cosine between the two texts of each pair:\n")
    print(f"  {'pair':30} {'small':>8} {'large':>8}")
    got = {}
    for m in MODELS:
        vecs, _, _ = embed(texts, m)
        got[m] = [cosine(vecs[i], vecs[i+1])
                  for i in range(0, len(vecs), 2)]
    for i, (label, _, _) in enumerate(PAIRS):
        print(f"  {label:30} {got[MODELS[0]][i]:8.4f}"
              f" {got[MODELS[1]][i]:8.4f}")
    print("\n  chapter 25 stipulated 0.99983 for the first pair")
    print("  and 0.99976 for the second.")
```

```text
  cosine between the two texts of each pair:

  pair                              small    large
  a part code, one token in ten    0.9911   0.9829
  a negation, one token in five    0.8158   0.7719
  one question, two phrasings      0.6474   0.6154
  two topics, as a floor           0.0556   0.0469

  chapter 25 stipulated 0.99983 for the first pair
  and 0.99976 for the second.
```

**Chapter 25's conclusions survive this table and its numbers do not, and the two halves of that
sentence have to be kept apart.**

**The part-code pair is close, and nowhere near as close as the chapter said.** 0.9911 against a
stipulated 0.99983 — a distance of 0.0089 where the chapter had 0.00017, fifty times larger. So
the stipulated figure was not just illustrative, it was crowded into a corner of the range the
model does not use for this. Read the bottom row to see how much range there is: two texts about
different things sit at 0.0556, not at 0.99. **A real cosine uses the whole interval**, and the
0.999s in chapters 24 and 25 are a property of numbers somebody typed.

**The negation pair is the one that refutes the stipulated figure outright.** 0.8158, against a
stipulated 0.99976. *Your refund was approved* and *Your refund was not approved* are not nearly
identical as vectors on a real model; 0.8158 leaves room that 0.99976 does not.

**But read the third row before concluding anything comfortable.** Two phrasings of one question
sit at 0.6474, and a higher cosine means closer — so **a sentence sits nearer to its own negation
than two wordings of one question sit to each other.** That is chapter 25's worry surviving in
weaker form rather than going away: the model has put the opposite of a statement closer to it
than a paraphrase of a different statement, and *not* is still one token among five.

**And chapter 24's paraphrase premise is in that row too, answered.** Chapter 24 stipulated 0.978
for two sentences that mean the same thing with no words in common, and said in terms that whether
a real model does that is an empirical property of the model. It is 0.6474 here, so that figure
was typed as well — and against a floor of 0.0556 it is a model noticing a paraphrase
comfortably, which is chapter 24's conclusion holding while its number does not.

### What to measure instead

The bottom row is the instrument the rest of this chapter uses. Call it the **similarity floor** —
the cosine between two texts of your own that have nothing to do with each other. Chapter 24's
rule is that a raw cosine has no meaning on its own, and the floor is how you make a *difference*
of cosines readable: a gap of 0.015 is small or large only against the spread the model is using.
Both of these models put it at about 0.05, and the two figures are printed side by side for that
reason only — to show the scales are not the same thing, never to be subtracted. One pair of
sentences gives you an order of magnitude and not a constant, so measure several unrelated pairs
before you lean on it: the larger model's value moved from 0.0469 to 0.0462 across four runs of
this program.

### And does the conclusion hold when the numbers do not?

Chapter 25's claim was never that the negation wins. It was narrower: that the ordering between a
true answer and its negation is decided by a residual you have no handle on. So rank them.

```python
"""Does chapter 25's CONCLUSION survive its numbers being wrong?

The stipulated pairs sat at 0.9998. The real ones do not. So ask
what chapter 25 actually claimed - that you cannot tell from the
score which of the two documents you hold - and rank them.
"""
from embed import MODELS, embed
from premise import cosine

TESTS = [
 ("was my refund approved?",
  ["Your refund was approved.", "Your refund was not approved."]),
 ("X-4471-D seal replacement",
  ["Replace the seal on pump X-4471-B before servicing the unit.",
   "Replace the seal on pump X-4471-D before servicing the unit.",
   "Maintenance schedule for all pumps in the B wing."]),
]

def arrangement(m):
    """Chapter 25's own bolded claim, which is about the ARRANGEMENT
    of three texts and not about any one number: the two answers are
    closer to each other than either is to the query."""
    q = "was my refund approved?"
    yes = "Your refund was approved."
    no = "Your refund was not approved."
    v, _, _ = embed([q, yes, no], m)
    pair, hit, miss = cosine(v[1], v[2]), cosine(v[0], v[1]), cosine(v[0], v[2])
    print(f"    the two answers, to each other   {pair:.4f}")
    print(f"    the query to the true answer     {hit:.4f}")
    print(f"    the query to the negation        {miss:.4f}")
    print(f"    nearer each other than the negation is to")
    print(f"      the query?      {pair > miss}")
    print(f"    nearer each other than the ANSWER is to")
    print(f"      the query?      {pair > hit}")


if __name__ == "__main__":
    for m in MODELS:
        print(f"\n  {m}")
        for q, docs in TESTS:
            vecs, _, _ = embed([q] + docs, m)
            qv, dv = vecs[0], vecs[1:]
            scored = sorted(zip(docs, (cosine(qv, v) for v in dv)),
                            key=lambda p: -p[1])
            print(f"    {q!r}")
            for place, (d, c) in enumerate(scored, 1):
                print(f"      {place}  {c:.4f}  {d[:44]}")
            top, second = scored[0][1], scored[1][1]
            print(f"      margin {top - second:.4f}")
        print("    chapter 25's arrangement claim:")
        arrangement(m)
```

```text

  text-embedding-3-small
    'was my refund approved?'
      1  0.8582  Your refund was approved.
      2  0.7480  Your refund was not approved.
      margin 0.1101
    'X-4471-D seal replacement'
      1  0.7474  Replace the seal on pump X-4471-D before ser
      2  0.7323  Replace the seal on pump X-4471-B before ser
      3  0.2471  Maintenance schedule for all pumps in the B 
      margin 0.0150
    chapter 25's arrangement claim:
    the two answers, to each other   0.8158
    the query to the true answer     0.8582
    the query to the negation        0.7481
    nearer each other than the negation is to
      the query?      True
    nearer each other than the ANSWER is to
      the query?      False

  text-embedding-3-large
    'was my refund approved?'
      1  0.8003  Your refund was approved.
      2  0.6749  Your refund was not approved.
      margin 0.1254
    'X-4471-D seal replacement'
      1  0.7419  Replace the seal on pump X-4471-D before ser
      2  0.7281  Replace the seal on pump X-4471-B before ser
      3  0.3153  Maintenance schedule for all pumps in the B 
      margin 0.0138
    chapter 25's arrangement claim:
    the two answers, to each other   0.7719
    the query to the true answer     0.8003
    the query to the negation        0.6749
    nearer each other than the negation is to
      the query?      True
    nearer each other than the ANSWER is to
      the query?      False
```

**The negation case comes out right, with room to spare.** A margin of about 0.11 against a floor of
0.0556 — the gap between the true answer and its negation is twice the distance to an unrelated
text. Chapter 25's illustration had the negation winning; on this model it loses clearly, and the
chapter's own hedge is what makes that an acceptable outcome rather than an error: it said *the
point is not that it always will, and these are typed numbers.*

**The part-code case comes out right by almost nothing, which is the claim that holds.** The
margin is 0.0150, and the query's score for either note sits about 0.50 above its score for the
off-topic maintenance schedule. Be careful how that is said, because chapter 25 corrects this
exact slip in its own text: 0.50 is a *difference of two scores from the query*, not a distance
between any pair of documents — the notes are 0.544 and 0.554 away from the schedule. Either way
the shape is the same. **The quantity deciding which note you get is about a thirtieth of the
quantity separating a relevant document from an irrelevant one**, and that is chapter 25's point,
measured instead of stipulated: when two documents differ only in an identifier, a cosine has
almost nothing to rank them on. Not nothing, on this model, on this pair. Almost nothing.

**And the last four lines are chapter 25's own emphasis, which is about an arrangement rather than
a number.** Its claim was that the two answers are *closer to each other than either is to the
query*, and the three figures needed to test it are now all on the page. The pair sits at 0.8158.
The query is 0.8582 from the true answer and 0.7481 from the negation. So the pair is nearer each
other than the *negation* is to the query, and *not* nearer than the *answer* is — the
arrangement half holds, on both models, identically.

**That narrows this chapter's thesis and it is worth narrowing.** It is not that chapter 25's
conclusions all survive while its numbers do not. The conclusion it drew — that the score gives
you no handle on this ordering — survives. The arrangement it drew it from does not: on a real
model the true answer is the nearest of the three things to the query, which is the opposite of
what a reader of chapter 25's figures would expect, and it is exactly why that chapter said to
check.

> **Warning:** Do not read any of this as *a real model handles negation*. Two sentences is not a
> measurement, this is two models on one phrasing, and the thing chapter 25 denies is still true:
> 0.8582 is not readable as *approved*. You cannot look at that number and know which document you
> are holding, because a raw cosine means nothing on its own — only the order of two of them does,
> and the order is what came out right here.

## Step 3: A Dozen Queries, Read by Hand

Now the search. It compares the query against every document and sorts, which is chapter 29's
exhaustive search, and at forty documents it is not a compromise but the right answer.

```python
"""Brute-force search over the corpus, both models, a dozen queries.

Chapter 29 owns exhaustive search and counts comparisons rather than
milliseconds; this is that, at a size where it is the right answer.
Chapter 24's rule is the one to keep in mind while reading the
output: a raw cosine has no meaning on its own and is not comparable
across models, so rank and do not threshold.
"""

import json
import pathlib

from embed import CACHE, CORPUS, MODELS, ROOT, embed
from premise import cosine

# The corpus ships eight queries with graded judgements, which
# chapter 44 needs. These four are for reading by hand only, so they
# are here and not in the corpus: adding rows there without
# judgements would quietly break that chapter's labels.
EXTRA = [
 ("q9",  "HL-2208-F"),
 ("q10", "Do you deliver to PA20?"),
 ("q11", "What does the letter at the end of a product code mean?"),
 ("q12", "What is covered for ninety days?"),
]


def queries(path=None):
    path = path or ROOT / "queries.tsv"
    rows = pathlib.Path(path).read_text().strip().split("\n")[1:]
    return [tuple(r.split("\t")) for r in rows] + EXTRA


def corpus():
    d = json.loads(CACHE.read_text())
    return d["ids"], d


def rank(qvec, vectors):
    """Compare against every document. Chapter 29's exhaustive search:
    the work is one comparison per document and nothing is skipped."""
    return sorted(range(len(vectors)),
                  key=lambda i: -cosine(qvec, vectors[i]))


def holds(term, ids):
    """Which documents contain the string, as written.

    This is chapter 26's lexical retrieval with the scoring taken
    out: an unranked boolean match. It is not the retrieval your
    users get; it is a check on the one they do.
    """
    return [i for i in ids
            if term.lower() in (CORPUS / f"{i}.md").read_text().lower()]


if __name__ == "__main__":
    ids, cache = corpus()
    qs = queries()
    print(f"  {len(qs)} queries, {len(ids)} documents,"
          f" {len(qs) * len(ids)} comparisons per model\n")
    # One model's listing is a page of reading on its own, so this
    # prints the first. Change the slice for the other.
    for m in MODELS[:1]:
        vecs, _, _ = embed([q for _, q in qs], m)
        print(f"  {m}, top 3 by rank:\n")
        for (qid, q), qv in zip(qs, vecs):
            top = rank(qv, cache[m])[:3]
            print(f"    {qid:4} {q[:46]}")
            for place, i in enumerate(top, 1):
                print(f"           {place}  {ids[i]}")
        print()
```

```text
  12 queries, 40 documents, 480 comparisons per model

  text-embedding-3-small, top 3 by rank:

    q1   How long do I have to return something?
           1  how-to-start-a-return
           2  gift-returns
           3  returns-standard
    q2   Why is my refund taking so long?
           1  where-is-my-refund
           2  refund-to-a-closed-card
           3  refunds-faq
    q3   How much does delivery cost to the Scottish Hi
           1  delivery-exceptions
           2  international-delivery
           3  delivery-fees
    q4   What is HL-2208?
           1  product-toaster-hl-2209
           2  product-kettle-hl-2208
           3  sku-conventions
    q5   Is a refund 14 days or 30 days?
           1  where-is-my-refund
           2  refunds-policy
           3  refunds-faq
    q6   My parcel arrived damaged. What do I do?
           1  damaged-on-arrival
           2  missing-item-in-a-parcel
           3  wrong-item-sent
    q7   What does Harbour Plus include?
           1  plan-harbour-plus
           2  plan-comparison
           3  about-us
    q8   Can I return a clearance item?
           1  returns-clearance
           2  returns-standard
           3  gift-returns
    q9   HL-2208-F
           1  product-toaster-hl-2209
           2  product-kettle-hl-2208
           3  product-lamp-hl-3310
    q10  Do you deliver to PA20?
           1  international-delivery
           2  shipping-partners
           3  delivery-exceptions
    q11  What does the letter at the end of a product c
           1  sku-conventions
           2  stock-codes-and-statuses
           3  returns-standard
    q12  What is covered for ninety days?
           1  warranty-full
           2  warranty-summary
           3  returns-standard
```

**Read that as a person demonstrating a search would read it, which is to say approvingly.** Nine
of the twelve top-threes are hard to fault. A question about returning something returns the
return pages. A question about a damaged parcel returns the damage page and then two
near-neighbours about missing and wrong items. Harbour Plus returns the Harbour Plus page and the
plan comparison. This is what chapter 25 means by a plausible list, and it is twelve of them
rather than the five it warns about.

**Now look at q4 and q9 and notice that you have to know the corpus to see anything wrong.** The
query is *What is HL-2208?* and the first result is `product-toaster-hl-2209` — the toaster. The
kettle is HL-2208. For the bare part code in q9 the first result is the toaster again.

**And q10 is the one that would have got past me.** *Do you deliver to PA20?* returns
international delivery, then the shipping partners, then the delivery exceptions page. Every one of
those is about delivery. Nothing in that list is absurd. PA20 is a Scottish postcode and the page
that lists it is third.

> **Note:** The corpus was built to contain this failure and says so. Its `README.md` lists what
> was planted and names this chapter: *identifiers that similarity cannot match — SKU codes, policy
> section numbers, a plan name*, needed by *43: one query where an exact string beats a dense
> ranking*. So nothing in step 4 is a discovery, and a lab that reported it as one would be
> reporting its own fixture. What was [**not**]{.noindex} planted is how the failure behaves — which document
> wins instead, by how much, and whether both models fail the same way — and that is what the next
> two steps read.

## Step 4: The Query That Breaks Them

The useful question is not whether the identifier query fails. It is where the document holding the
string actually ranked, and the corpus can answer that without the dense index at all.

```python
"""Where does the document that holds the string actually rank?

The corpus README declares this failure planted - it was built to
contain identifiers similarity cannot match - so nothing here is a
discovery. What is not planted is HOW it fails, whether the two
models fail the same way, and whether the ranks are even stable,
which is what this reads.
"""

from embed import MODELS, embed
from premise import cosine
from search import corpus, holds, rank

# A term, and the query somebody would type to find it.
CASES = [
 ("HL-2208",   "What is HL-2208?"),
 ("HL-2208-F", "HL-2208-F"),
 ("PA20",      "Do you deliver to PA20?"),
 ("ninety days", "What is covered for ninety days?"),
]


def scored(qv, m, ids, cache, places):
    """The top few with their cosines, because a rank is a fact about
    the documents only if the gap that decided it is bigger than the
    noise. Chapter 24's near-tie, and step 2's floor is the yardstick.

    Takes the query vector rather than the query, so this reads the
    same embedding the ranks above were computed from. Re-fetching it
    would let the two halves of one run disagree, which is the defect
    this step exists to describe.
    """
    return [(ids[i], cosine(qv, cache[m][i]))
            for i in rank(qv, cache[m])[:places]]


if __name__ == "__main__":
    ids, cache = corpus()
    kept = {}
    print("  the term, the documents that contain it as written,")
    print("  and where those documents ranked:\n")
    for m in MODELS:
        vecs, _, _ = embed([q for _, q in CASES], m)
        print(f"  {m}\n")
        for (term, q), qv in zip(CASES, vecs):
            kept[(m, q)] = qv
            hits = holds(term, ids)
            order = rank(qv, cache[m])
            places = sorted(order.index(ids.index(h)) + 1 for h in hits)
            print(f"    {term:12} in {len(hits)} of {len(ids)} docs,"
                  f" ranked {places}")
            print(f"      top 1 was {ids[order[0]]}")
        print()

    print("  and now the gaps that decided those ranks:\n")
    for m, q in ((MODELS[1], "What is HL-2208?"),
                 (MODELS[0], "Do you deliver to PA20?")):
        print(f"    {m}")
        print(f"      {q}")
        for name, c in scored(kept[(m, q)], m, ids, cache, 5):
            print(f"        {c:.4f}  {name}")
        print()
```

```text
  the term, the documents that contain it as written,
  and where those documents ranked:

  text-embedding-3-small

    HL-2208      in 3 of 40 docs, ranked [1, 2, 3]
      top 1 was product-toaster-hl-2209
    HL-2208-F    in 1 of 40 docs, ranked [2]
      top 1 was product-toaster-hl-2209
    PA20         in 1 of 40 docs, ranked [3]
      top 1 was international-delivery
    ninety days  in 2 of 40 docs, ranked [1, 27]
      top 1 was warranty-full

  text-embedding-3-large

    HL-2208      in 3 of 40 docs, ranked [1, 2, 4]
      top 1 was product-kettle-hl-2208
    HL-2208-F    in 1 of 40 docs, ranked [1]
      top 1 was product-kettle-hl-2208
    PA20         in 1 of 40 docs, ranked [2]
      top 1 was international-delivery
    ninety days  in 2 of 40 docs, ranked [1, 37]
      top 1 was warranty-full

  and now the gaps that decided those ranks:

    text-embedding-3-large
      What is HL-2208?
        0.4130  product-kettle-hl-2208
        0.4072  product-toaster-hl-2209
        0.2834  product-chair-hl-5512
        0.2831  sku-conventions
        0.2821  product-lamp-hl-3310

    text-embedding-3-small
      Do you deliver to PA20?
        0.3612  international-delivery
        0.3609  shipping-partners
        0.3607  delivery-exceptions
        0.3593  delivery-fees
        0.3255  changing-a-delivery-address
```

**`HL-2208-F` is the whole argument in one row.** It is an **identifier query**: a query whose
intent is an exact string — a code, a surname, an invoice number, a postcode — rather than a
topic. The string occurs in exactly one of the forty documents. There is no ambiguity to resolve,
no judgement to make, nothing to weigh. One model puts that document second and the other puts it
first. A search over forty documents, looking for a string that is in one of them, and the simpler
model gets it wrong.

**And the document that beat it is the interesting part.** `product-toaster-hl-2209` is not an
unrelated page that crept in. Its line 22 reads *Matches the HL-2208 kettle in all three
finishes* — so the toaster document genuinely contains the string `HL-2208`. Both documents hold
it; one is *about* it and one mentions it in passing, and the small model prefers the mention.
That is chapter 25's *similarity is not relevance* on a real corpus: the cosine has no way to
represent the difference between a document's subject and a sentence inside it, because the vector
describes the whole text at one fixed width.

**`PA20` is the failure neither model fixes.** The postcode is in one document and both models put
`international-delivery` first — a page about delivery abroad, for a query about a Scottish
postcode. Chapter 25 says inspection finds a present error and never a missing one; this is a
present error that does not look like one, and the only reason it is visible here is that the
previous column tells you where the right document went.

**`ninety days` is the near-miss worth keeping.** The phrase appears twice: in the warranty
document, which both models rank first and correctly, and in the kettle's page, which says its
limescale filter is covered for ninety days. That second document ranks [**27th of 40**]{.noindex} on
one model and [**37th of 40**]{.noindex} on the other. The top result is right, the list looks right, and a
document holding the exact phrase sits near the bottom — which is the shape of the failure chapter
25 says you cannot see by looking.

**And the last two blocks are why two of those ranks are worth less than they look.** On the
larger model the chair, `sku-conventions` and the lamp come in at 0.2834, 0.2831 and 0.2821, so the
whole of third, fourth and fifth place spans thirteen ten-thousandths. `sku-conventions` is one of
the three documents holding the string, and the gap deciding whether it is fourth or fifth is the
ten ten-thousandths between it and the lamp. It came out fourth on every run but one here; the
exception is worth more than the rule, because nothing about `ranked [1, 2, 4]` tells you that the
4 is resting on a thousandth.

**The `PA20` result is the same shape and it splits by model.** On the larger model the three
delivery pages are 0.3937, 0.3766 and 0.3733 — a clear 0.017 between first and second, and the page
that lists the postcode is second. On the smaller one they are 0.3612, 0.3609 and 0.3607: three
pages inside five ten-thousandths, which against a floor of about 0.05 is one per cent of the
spread the model is using. So *the page that lists it is third* is a tie reported as a ranking on
that model, and on one run in dozens the order inverts and puts it first. **The finding is solid on
the larger model and a near-tie on the smaller**, and the difference between saying those two
things is the whole of chapter 24's rule about ranking rather than thresholding.

> **Warning:** These are the two places in the lab where a printed rank is not reliable, and it is
> not the provider being unreliable. The same string embedded twice comes back very slightly
> different — usually by less than a ten-thousandth of a cosine, occasionally by several — which is
> nothing at all, unless two documents are closer together than that. Then it decides a rank.
> Measure the gap before you quote the position: chapter 24 puts it exactly, that a ranking can be
> stable in its top *set* and unstable in its *order*, and that if you care which of two near-ties
> comes first you need a tie-break your code controls rather than a third decimal place.

> **Tip:** `holds()` is four lines and it is the most useful thing in this lab. Say what it is
> plainly: it is chapter 26's lexical retrieval with the scoring taken out — an unranked boolean
> match. What makes it a check rather than a competing search is where it sits: you run it against
> a term you already hold, to find out where the dense ranking put the document, and it is not the
> retrieval your users get. As a check it is close to free, and it converts *the results look
> fine* into *the document containing the term ranked 27th*. If you have an identifier your users
> search for, you can run this before you build anything.

## Step 5: The Two Models, Compared the Only Way That Is Allowed

Two models, twelve queries, and a rule from chapter 24 that rules out the obvious comparison: a
raw cosine has no meaning on its own and is not comparable across models, so nothing below puts one
model's score beside the other's. What transfers is the order.

```python
"""The two models, compared the only way chapter 24 allows.

A raw cosine has no meaning on its own and is not comparable across
models, so nothing below compares a small score with a large one.
What is comparable is the ORDER, and chapter 24's other rule applies
to the breakdown: grouping separates two models only if you group by
a property they differ on.
"""

from embed import MODELS, embed
from premise import cosine
from search import corpus, queries, rank

# The property to group by, and the TEST, because step 4 has four
# exact-string cases and this has three. The test is what the query
# WANTS: a specific string that has to match (q4, q9, q10), or a
# topic that happens to contain an exact phrase (q12, which asks
# what is covered rather than for the words `ninety days`). The
# second grouping below reports what happens if you disagree with
# that reading, which is the honest way to show a judgement call.
IDENTIFIER = {"q4", "q9", "q10"}
EXACT_STRING = IDENTIFIER | {"q12"}

if __name__ == "__main__":
    ids, cache = corpus()
    qs = queries()
    tops, scores = {}, {}
    for m in MODELS:
        vecs, _, _ = embed([q for _, q in qs], m)
        tops[m] = {qid: ids[rank(qv, cache[m])[0]]
                   for (qid, _), qv in zip(qs, vecs)}
        scores[m] = [max(cosine(qv, v) for v in cache[m])
                     for qv in vecs]

    a, b = MODELS
    print("  the scales are different, which is why only the order")
    print("  is compared below:\n")
    for m in MODELS:
        s = scores[m]
        print(f"    {m}")
        print(f"      best-match cosine: {min(s):.3f} to {max(s):.3f},"
              f" mean {sum(s)/len(s):.3f}")

    same = [qid for qid, _ in qs if tops[a][qid] == tops[b][qid]]
    print(f"\n  same document first on {len(same)} of {len(qs)} queries\n")
    print(f"  {'query':5} {'small':24} large")
    for qid, q in qs:
        mark = " " if tops[a][qid] == tops[b][qid] else "*"
        print(f"  {mark}{qid:4} {tops[a][qid][:23]:24} {tops[b][qid][:23]}")

    for name, group in (("identifier queries", IDENTIFIER),
                        ("any exact string", EXACT_STRING)):
        print(f"\n  grouped by {name}:\n")
        for label, want in ((name, True), ("the rest", False)):
            g = [qid for qid, _ in qs if (qid in group) == want]
            agree = sum(tops[a][q] == tops[b][q] for q in g)
            print(f"    {label:20} {agree} of {len(g)} agree")
```

```text
  the scales are different, which is why only the order
  is compared below:

    text-embedding-3-small
      best-match cosine: 0.360 to 0.650, mean 0.514
    text-embedding-3-large
      best-match cosine: 0.361 to 0.662, mean 0.496

  same document first on 10 of 12 queries

  query small                    large
   q1   how-to-start-a-return    how-to-start-a-return
   q2   where-is-my-refund       where-is-my-refund
   q3   delivery-exceptions      delivery-exceptions
  *q4   product-toaster-hl-2209  product-kettle-hl-2208
   q5   where-is-my-refund       where-is-my-refund
   q6   damaged-on-arrival       damaged-on-arrival
   q7   plan-harbour-plus        plan-harbour-plus
   q8   returns-clearance        returns-clearance
  *q9   product-toaster-hl-2209  product-kettle-hl-2208
   q10  international-delivery   international-delivery
   q11  sku-conventions          sku-conventions
   q12  warranty-full            warranty-full

  grouped by identifier queries:

    identifier queries   1 of 3 agree
    the rest             9 of 9 agree

  grouped by any exact string:

    any exact string     2 of 4 agree
    the rest             8 of 8 agree
```

**The last three lines are the step, and they are chapter 24's rule arriving with a number on it.**
Chapter 24 says a breakdown only separates two models if you group by a property they differ on.
Grouped by nothing, these two models put the same document first on ten of twelve queries, which
reads as *no meaningful difference*. Grouped by whether the query is an identifier query, they
agree on [**nine of nine**]{.noindex} ordinary queries and on [**one of three**]{.noindex}
identifier queries. The whole of
the difference between these two models, on this corpus, lives in a quarter of the queries.

**So a twelve-query comparison that did not group would have reported the wrong answer**, and it
would have reported it as a reassuring one. Nine of nine is not a weak signal — it is the two
models being indistinguishable where most of the traffic is, which is exactly why the three
queries where they differ are easy to average away.

**The grouping was named before the result, and the second grouping is why that is not enough.**
Chapter 25's identifier failure and the corpus README both name the property, so the three queries
were not picked for disagreeing. But step 4 ran *four* exact-string cases and this step groups
*three* of them — and the one it leaves out, `ninety days`, is the one the two models agree on.
Count it and the headline is two of four against eight of eight instead of one of three against
nine of nine. Both groupings are printed for that reason.

**So the step owes you the test rather than the list.** The question is what the query *wants*: a
specific string that has to match, or a topic that happens to contain an exact phrase. *What is
HL-2208?* and `HL-2208-F` and *Do you deliver to PA20?* want the string. *What is covered for
ninety days?* wants to know what is covered, and the phrase is how the document happens to say
it — which is also why *What does the letter at the end of a product code mean?* is not one,
though it is about identifiers: it asks for a convention. Apply the test and the group is three.
Disagree with the reading and it is four, and the chapter's conclusion does not turn on which: the
difference between these two models sits on exact-string queries and nowhere else that rank one
can see.

**Picking the grouping after seeing which queries differ is a different thing entirely**, and
chapter 24 is where it is demonstrated: its own lab relabels four queries by language, makes two
identical-looking models look different, and concludes that the grouping which distinguishes two
models is a property of how you cut the data rather than of the models.

**And this comparison looks at rank one and nothing else.** Below it the two models plainly do
differ on ordinary queries: step 4 prints `HL-2208` at ranks 1, 2, 3 for one model and 1, 2, 4 for
the other, and `PA20` moving from third to second — with the 4 and the 3 being the two positions
the gaps in that step call ties. So the claim is narrow — the two put a
different *document first* only on exact-string queries — and what they do at ranks two and three
across the other nine, this program never asked.

**Read the two score ranges and then stop reading them.** Both sit between about 0.36 and 0.66:
similar, which is luck rather than a property, and no reason to compare
them. The two models have different widths, were trained differently, and place their floors in
different places — 0.0556 against 0.0469 in step 2. A difference between two models' cosines on
the same query is not a quantity.

> **Warning:** The thing not to conclude from this step is *use the larger model*. Two of three
> identifier queries improved, one did not, and this lab measures twelve queries on forty
> documents with no repetition — chapter 20 would have something to say about an interval on three
> queries. What the step establishes is narrower and more useful: **the two models differ where
> chapter 25 said dense retrieval is weak, and nowhere else that twelve queries can see.** The
> decision between them is a cost and latency question on top of a measurement that chapter 44
> runs properly.

## Step 6: What Twelve Top-Threes Cannot Tell You

One step left, and it is the one that makes the next chapter necessary. Everything above was read
by eye. Chapter 25's whole argument is that reading by eye finds a wrong result that is present and
never a right one that is missing — so put the corpus's own judgements beside the rankings and see
what twelve plausible top-threes were hiding.

```python
"""What reading twelve top-threes by hand cannot tell you.

Chapter 25's point: inspection finds a wrong result that is present
and never a right one that is missing. The corpus ships graded
judgements - chapter 44 turns them into measures, which is not this
chapter's job. One listing is enough here.
"""
import pathlib

from embed import MODELS, ROOT, embed
from search import corpus, queries, rank


def judged(path=None):
    path = path or ROOT / "judgements.tsv"
    rows = pathlib.Path(path).read_text().strip().split("\n")[1:]
    out = {}
    for r in rows:
        qid, doc, grade = r.split("\t")[:3]
        if int(grade) > 0:
            out.setdefault(qid, []).append((doc, int(grade)))
    return out


if __name__ == "__main__":
    ids, cache = corpus()
    j = judged()
    qs = [(qid, q) for qid, q in queries() if qid in j]
    for m in MODELS[:1]:
        vecs, _, _ = embed([q for _, q in qs], m)
        print(f"  {m}: where every document somebody graded")
        print(f"  relevant actually ranked\n")
        for (qid, q), qv in zip(qs, vecs):
            order = [ids[i] for i in rank(qv, cache[m])]
            places = sorted((order.index(d) + 1, d, g)
                            for d, g in j[qid])
            shown = [p for p, _, _ in places if p <= 3]
            missed = [(p, d, g) for p, d, g in places if p > 3]
            print(f"    {qid}  {len(shown)} of {len(places)} graded"
                  f" documents in the top 3")
            for p, d, g in missed:
                print(f"         grade {g} at rank {p:2}  {d}")
```

```text
  text-embedding-3-small: where every document somebody graded
  relevant actually ranked

    q1  3 of 8 graded documents in the top 3
         grade 2 at rank  4  returns-clearance
         grade 1 at rank  7  refunds-policy
         grade 1 at rank  9  return-postage-labels
         grade 1 at rank 10  warranty-full
         grade 1 at rank 16  international-delivery
    q2  3 of 4 graded documents in the top 3
         grade 1 at rank  4  refunds-policy
    q3  2 of 3 graded documents in the top 3
         grade 1 at rank  5  plan-harbour-plus
    q4  3 of 3 graded documents in the top 3
    q5  3 of 3 graded documents in the top 3
    q6  2 of 4 graded documents in the top 3
         grade 1 at rank  4  warranty-full
         grade 1 at rank  8  how-to-start-a-return
    q7  2 of 4 graded documents in the top 3
         grade 1 at rank  7  delivery-fees
         grade 1 at rank 16  returns-clearance
    q8  2 of 5 graded documents in the top 3
         grade 2 at rank  4  how-to-start-a-return
         grade 1 at rank  7  return-postage-labels
         grade 1 at rank 20  plan-harbour-plus
```

**On q1, eight documents were judged relevant and three of them were in the list I read.** A
grade-2 document — the higher of the two grades — sat at rank 4, one place below where I stopped
looking, and four more at 7, 9, 10 and 16. I read that top three in step 3 and called it hard to
fault, which it was. It was also missing five of the eight documents somebody had written down as
answering the question, and nothing about the three I could see said so.

**And q4 is the row that closes the argument.** All three of its graded documents are in the top
three, and the top one is the toaster. A listing that asks only *were the right documents found*
is satisfied by q4 and silent about the thing step 4 spent a page on. Found and ordered are
different questions, and you need both.

**Be exact about what is and is not being declined here.** *Three of eight in the top three* is
recall@3's two numbers, and chapter 26 built that measure already, so nothing is being kept from
you. What this step declines is the division and the average: it does not reduce the eight queries
to one figure, and it does not score the ranks below three, which is what chapter 26's discounted
measures are for. Chapter 44 does both over these same judgements, and adds the other half of the
answer — a retrieval method that matches strings as written. This step's job was to put the ranks
beside a list I had already approved.

**And now the uncomfortable part, which is in the output above and not in my reading of it.** I
said in step 3 that nine of the twelve top-threes were hard to fault. Count the graded documents
in this listing and four of those nine held a document the judgements grade *zero*: q3 at rank 2,
and q6, q7 and q8 at rank 3. One of them is `about-us`, which the corpus README names as the one
document that answers no query at all — and I praised that list. So the division is not
*inspection finds every present error*. It is narrower: **inspection found the present errors I
went looking for, and the judgements found four more sitting in top threes I had approved.**

**What the twelve queries did buy, then.** The toaster beating the kettle was found by reading, which is worth having and is chapter 25's one
concession to inspection — and the postcode page not coming first was found the same way, though
step 4 is where its exact position turned out not to be a position at all. The kettle's page at 27th was not found by reading — it was found by `holds()`, and
reading is what chapter 25 says will never find it.
Chapter 25's division is exact: inspection is sound for errors that are there, and blind to
everything else.

## What To Actually Do

1. **Embed your corpus twice before choosing a model**, cache the vectors in a file, and compare
   rankings rather than scores. The cache is what makes every later question free.
2. **Measure your similarity floor first** — two texts of your own with nothing in common — since no
   margin means anything until you know where the model's zero is.
3. **Check the premise rather than quoting it.** A stipulated 0.9998 and a measured 0.9911 are
   different arguments, and one of them is about your data.
4. **Write down your identifier queries and find where the document holding the string ranked.**
   It is four lines, it needs no answer key, and it is the cheapest real test of a dense index.
5. **Group a two-model comparison by a property the models differ on**, and choose the grouping
   before you look. Ten of twelve agreeing hid nine of nine against one of three.
6. **Never compare two models' raw cosines.** Different widths, different training, different
   floors. Only the order transfers.
7. **Stop before concluding anything about what is missing.** Inspection is sound for a present
   error and blind to an absent answer, and the only thing that closes the gap is a key written
   down before the search ran.

## Summary, Key Terms, and Review Questions

### Summary

Forty shipped documents embedded twice — 1,536 numbers one way and 3,072 the other, 9,740 tokens
either way, 3.8 MB of vectors for forty short pages — and then chapter 25's premise checked instead
of quoted, and the result is in three parts. **Its conclusion survives, its numbers do not, and
the arrangement it drew the conclusion from holds only half way.** Two maintenance notes differing in a
part code came in at 0.9911 against a stipulated 0.99983, a distance fifty times larger; a sentence
and its negation at 0.8158 against a stipulated 0.99976 — and since a higher cosine is nearer,
**that pair sits closer together than two phrasings of one question** at 0.6474 — which is chapter
25's worry in weaker form rather than a refutation. **And its bolded claim is about an arrangement
rather than a figure**, so the three numbers it needs are measured too: the pair at 0.8158, the
query 0.8582 from the true answer and 0.7481 from the negation. Chapter 25 said the pair is nearer
each other than *either* is to the query; it is nearer than the negation and not nearer than the
answer, so the claim as stated fails while one half of its comparison holds, identically on both
models. Then two texts about different things at 0.0556, which is the
**similarity floor** and the instrument that makes every other margin readable. Ranked rather than
compared, the negation case comes out right by about 0.11 — twice the floor — so chapter 25's
illustration does not reproduce, while the part-code case comes out right by 0.0150, about a thirtieth of
the 0.50 that separates the query's score for a relevant document from its score for an irrelevant
one — a difference of two scores and not a distance between a pair, which is chapter 25's own
correction — and that is its claim measured rather than stipulated. Then a dozen queries over the forty documents by exhaustive search, 480
comparisons a model, and nine of the twelve top-threes are hard to fault. **The three that are not
are the identifier queries**, and the corpus `README.md` declares that failure planted, so none of
it is a discovery: what was not planted is the behaviour. `HL-2208-F` is in exactly one document and
one model ranks it second, behind the toaster page — which genuinely contains the string, in the
sentence *Matches the HL-2208 kettle in all three finishes*, so both documents hold it and
similarity prefers the passing mention to the subject. `PA20` is in one document and **both** models
put international delivery first. And `ninety days` appears twice, with the second document ranking
27th and 37th while the top result is right and the list looks right. Compared the only way chapter
24 allows — by order, never by score — the two models put the same document first on ten of twelve
queries, which reads as no difference; grouped by the property they differ on they agree on **nine of
nine ordinary queries and one of three identifier queries**, so the whole difference lives in a
quarter of the set and an ungrouped comparison would have reported the reassuring answer. Count
`ninety days` as an exact-string query too and it is two of four against eight of eight; the
chapter prints both groupings and states the test, because that judgement is the hazard the step
warns about. The grouping
was named by chapter 25 and the corpus before the result, which is what stops it being
manufactured. Last, the judgements the corpus ships, laid beside the ranks: on one query **eight
documents were judged relevant and three were in the top three**, with a grade-2 document one place
below where the reading stopped. Those two figures are recall@3's, which chapter 26 already built;
what this chapter declines is to average them over the set and to score the ranks below three,
which chapter 44 does over these same judgements. And the listing convicts the reading as well as
the ranking: **four of the nine top-threes called hard to fault in step 3 held a document graded
zero**, one of them `about-us`, which the corpus names as the document that answers no query at
all. So the division is narrower than chapter 25's sentence sounds — inspection found the present
errors that were looked for, and the judgements found four more in lists that had been approved.
The two it did find, the toaster and the postcode page, were found by reading; the kettle's page at
27th was found by `holds()`, which is four lines.

### Key Terms

| Term | Meaning |
|---|---|
| **Identifier query** | A query whose intent is an exact string — a code, a surname, an invoice number, a postcode — rather than a topic. The test is what the query wants: the string itself, or a subject that happens to contain one. Chapter 25 names this as a case dense retrieval is weak on, and it is the one worth listing separately whenever you compare two models |
| **Similarity floor** | The cosine between two texts of your own that have nothing to do with each other. Until you have measured it no margin means anything, and it is per model: about 0.05 for both of these two. One pair gives an order of magnitude and not a constant — measure several |

### Worth Memorising

| Item | Value or formula |
|---|---|
| What a real cosine looks like | The whole range, not the top of it. Floor about 0.05, one question two ways about 0.65, two texts differing in a code about 0.99 |
| Chapter 25's stipulated pairs, measured | 0.9911 where it said 0.99983; 0.8158 where it said 0.99976. The conclusion held; the numbers and the arrangement did not |
| Its arrangement claim, tested | The pair at 0.8158, the query 0.8582 from the answer and 0.7481 from the negation. Nearer each other than the negation is to the query, not nearer than the answer is |
| The identifier margin | 0.0150 between two notes differing in a part code, against about 0.50 between the query's scores for a relevant and an irrelevant document — about a thirtieth |
| Comparing two models | By order only. Different widths, different floors; a difference of two models' cosines is not a quantity |
| Why a grouping must be chosen first | Ungrouped, 10 of 12 agreed. Grouped by query kind, 9 of 9 against 1 of 3 — or 8 of 8 against 2 of 4 if an exact phrase counts, which is the judgement to state rather than bury |
| When a rank is not a rank | When the gap that decided it is of the order of the drift between two embeddings of one string. Three delivery pages inside 0.0005, against a floor of 0.05 |
| What a top three hides | On one query, 3 of 8 judged-relevant documents, with a grade 2 at rank 4 |

### Review Questions

1. Chapter 25 says a part number is almost no signal. You now have a real model. What do you
   measure, and what do you expect to find?
2. Why can you not compare two embedding models by their cosine scores?
3. Your twelve-query comparison of two models shows the same first result on ten of them. What have
   you learned?
4. What is the cheapest test of a dense index that needs no answer key?
5. You read twelve top-threes and they all look reasonable. What do you know, and what do you do
   next?

### Review Answers

1. Measure three things and keep them apart. First the pair itself: two texts differing only in the
identifier, embedded, with the cosine between them — 0.9911 here against the 0.99983 chapter 25
stipulated, so expect the conclusion to hold and the figure to be far less extreme, because a real
model uses the whole range. Second the floor: two texts of your own with nothing in common, which
came in at 0.0556 and is what makes the rest readable. Then rank a query naming one of the two
identifiers against both documents and an unrelated one: the margin between the right note and the
wrong one was 0.0150, against about 0.50 between the query's score for a relevant document and
its score for an irrelevant one — about a thirtieth, which is chapter 25's *almost no signal* as a
measurement. Say *between the query's two scores* and not *the distance to the unrelated
document*, because chapter 25 corrects that confusion in its own text and the two are different
quantities. The honest addition is that the right note *won*:
the failure is not that ranking is random, it is that the quantity deciding the order is a
thirtieth of the quantity separating topics, and nothing in the score tells you which situation you
are in.
2. Because a raw cosine has no meaning on its own, which is chapter 24's rule, and across two
models it has even less. The two have different widths — 1,536 against 3,072 here — were trained
differently, and put their floors in different places: two unrelated texts sat at 0.0556 for one
and 0.0469 for the other, so the same number means a different thing in each. What transfers is the
*order*, and that is what you compare: which document each model puts first, and where the document
you wanted ranked. The two score ranges in this chapter happen to look similar, both between
about 0.36 and 0.66, and that is luck rather than a property and still not a licence to subtract
one from the other.
3. Almost nothing, and the reason is chapter 24's rule about breakdowns: a comparison separates two
models only if you group by a property they differ on. Ungrouped, these two agreed on ten of
twelve. Grouped by whether the query is an identifier query — a property chapter 25 and the
corpus's own README both name, so not one chosen after seeing the answer — they agreed on nine of
nine ordinary queries and one of three identifier queries. The whole difference between the models
lives in a quarter of the set, and averaging over twelve queries is precisely what hides it. So
what you have learned from the ten is that the two models are indistinguishable on the queries
where most traffic is, which is worth knowing and is not what *ten of twelve* sounds like. And
twelve queries is too few to put an interval on three of them, which is chapter 20's objection and
chapter 44's job.
4. Write down the identifiers your users actually search for, find which documents contain each one
as written, and look at where those documents ranked. It needs no judgements, because the corpus
answers the question itself: a string either is in a document or is not. Four lines of code turned
*the results look fine* into *the document holding the term ranked 27th of 40* in this chapter, and
caught a case where the first result was a page that mentions the product in passing rather than
the page about it. It *is* a retrieval method — chapter 26's lexical retrieval with the scoring taken out — but it is
not the retrieval your users get: you run it as a check, against a term you already hold, to find
out where the dense ranking put the document. It is the cheapest real test there is.
5. That nothing *present* in those thirty-six results is obviously wrong, which is worth something:
inspection is a sound way to find errors that are there, and in this chapter it found three. What
you do not know is anything about what is missing, and the chapter has the number: on one query,
eight documents had been judged relevant and three were in the top three, with a grade-2 document
sitting at rank 4 — one place below where the reading stopped — and four more at 7, 9, 10 and 16. A
top three that is hard to fault and a top three that is missing five of eight look identical,
because a missing document leaves no trace in a list. What you do next is get a key: queries with
the documents that answer them, written down by somebody who knows the corpus, before the search
runs. Then a measure over it, which is chapter 26, and a method that matches strings as written,
which is chapter 26 as well and chapter 44's lab.

> **You understand this when** you can say what a measured cosine looks like against a stipulated
> one, name the test of a dense index that needs no answer key, and say what has to be true of a
> margin before a rank is worth quoting.
