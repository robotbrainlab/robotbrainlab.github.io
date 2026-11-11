# Embeddings, and Choosing One for Your Data

*The problem.* Two sentences that mean the same thing share no words. I don't see how any program
could notice that.

*The question.* What does an embedding model produce, and how do you choose one for your own
documents?

## What an Embedding Model Produces

Start by separating two things the word *embedding* is used for.

Chapter 9 has one already: the *embedding table* inside a generative model, a matrix with one
row per vocabulary entry, where looking a token up is how it enters the computation. That table
is internal to the computation, it holds one row per token rather than one vector per text, and
it is not what you search with.

This chapter is about something else: an **embedding model**, a separate model with a different
job. You give it a
piece of text, it gives you back one vector of a fixed width, and that is all it does. It does
not continue your text, it does not answer, and it has no output tokens. One text in, one list
of numbers out, the same width every time.

| | A generative model | An embedding model |
|---|---|---|
| You send | A prompt | A piece of text |
| You get | Tokens, one at a time | One vector, of fixed width |
| Width | A vocabulary's worth of scores per step | A few hundred to a few thousand numbers, once |
| Useful for | Producing text | Comparing texts with arithmetic |

The vector it returns is that text's **embedding**, and its width is fixed by the model. A
model with 768 dimensions gives you 768 numbers for a word, for a sentence and for a page.

> **Warning:** This book does not explain *why* the arrangement of those numbers carries
> anything useful. Chapter 9 says the same of its table and means it: the coordinates are
> whatever made the model's training objective work, nobody chose them, and no dimension means
> anything on its own. That question is representation learning, it is on Chapter 17's list of
> what this book deliberately leaves out, and you can do everything in this chapter and the
> five after it without an answer to it. What you can check is what the numbers *do*, which is
> the rest of this chapter.

## Closeness, Applied

Chapter 8 built the tool for this and you already have it: the dot product grows with magnitude,
which is why *cosine similarity* exists, and the cosine of two vectors is their dot product
divided by the product of their lengths. Chapter 8 also showed that the cosine does not change
when you scale a vector, which is worth having and is not the reason a page and a sentence are
comparable. That reason is the one above: the model returns the same fixed width whatever goes
in.

So apply it. Three sentences, with their vectors written out:

```python
import math

# Four numbers per sentence, written out rather than computed. Producing them
# needs an embedding model; what this chapter is about is what you do with
# them once you have them.
VECTORS = {
    "the flight was delayed":        [0.80, 0.50, 0.20, 0.10],
    "my plane left late":           [0.70, 0.60, 0.10, 0.20],
    "the flight attendant was kind": [0.20, 0.10, 0.90, 0.40],
}

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def length(a):
    return math.sqrt(dot(a, a))

def cosine(a, b):
    return dot(a, b) / (length(a) * length(b))

if __name__ == "__main__":
    names = list(VECTORS)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            print(f"  {cosine(VECTORS[a], VECTORS[b]):.3f}  {a}")
            print(f"         vs  {b}")
```

```text
  0.978  the flight was delayed
         vs  my plane left late
  0.439  the flight was delayed
         vs  the flight attendant was kind
  0.386  my plane left late
         vs  the flight attendant was kind
```

**Check the first one by hand**, because the whole chapter rests on being able to. Carry five
decimals through the lengths — at four, the rounding is enough to push the quotient to 0.979:

```{=latex}
\[ \frac{0.90}{\sqrt{0.94}\;\sqrt{0.90}} \;=\; \frac{0.90}{0.96954 \times 0.94868} \;=\; 0.978 \]
```

**Now read the three numbers carefully, because the obvious reading is the wrong one.**

*The flight was delayed* and *my plane left late* share **no content words at all** — not
*flight*, not *plane*, not *delayed*, not *late* — and their vectors point almost the same way,
at 0.978. *The flight was delayed* and *the flight attendant was kind* share three words
including the subject, and sit at 0.439.

So the answer to the opening problem is this: **the program does not notice that two sentences
mean the same thing.** What a model does is place each text somewhere, and *if* it places two
texts close together, cosine will report that — which is a measurable fact about its output, and
enough to build a search on, because you can rank by it.

**Now the honest part, and it is the hinge of the chapter.** Those four-number vectors were
written down by hand, not measured. Nothing above shows that a real model puts *the flight was
delayed* and *my plane left late* at 0.978; it shows that cosine reports 0.978 for the vectors I
chose. Whether a real model does that for *your* paraphrases, in your language and your domain,
is an empirical property of that model — and the second half of this chapter is how you find out
whether a model works on your data, which is a different measurement and the one that decides
anything. That is not a caveat bolted on to the demonstration. It is the reason the second half
exists, and the reason you cannot take a leaderboard's word for it, or this book's. A high cosine is not evidence that the model understood anything, nor a
demonstration that two texts mean the same — **Chapter 25 is about the gap
between closeness and relevance**, and the answer there is not a simple yes.

That distinction is worth holding onto, because every one of the next five chapters depends on
it. What you have is a number. What you want is relevance. They are not the same thing and the
rest of Part II is largely about the distance between them.

## Ranking

One more step and you have search. Embed the query with the same model — not a different one, or the numbers are not comparable —
compare it with every document, and sort.

```python
from close import VECTORS, cosine

QUERY = [0.75, 0.55, 0.15, 0.15]     # "why was my plane late"

ranked = sorted(VECTORS, key=lambda d: cosine(QUERY, VECTORS[d]), reverse=True)
for place, doc in enumerate(ranked, 1):
    print(f"  {place}  {cosine(QUERY, VECTORS[doc]):.3f}  {doc}")
```

```text
  1  0.995  the flight was delayed
  2  0.994  my plane left late
  3  0.415  the flight attendant was kind
```

That is **dense retrieval**, complete. Embed everything once and keep the vectors; embed the
query at search time; sort by cosine; take the top few. Five chapters from now you will be
making this fast over millions of documents rather than three, which is Chapter 29's, and the
arithmetic will not have changed.

**And a raw cosine has no meaning on its own**, which is the other thing to take from that
output. 0.995 does not mean 99.5 per cent relevant. It is not comparable with another model's 0.995, because
the two models' vectors live in different spaces; it is not comparable across queries, because
the spread of scores depends on what the query was; and it is not comparable across corpora. So a
cut-off learned in one place — *treat anything above 0.7 as a hit* — does not travel, and a
number that worked for months can stop working the day you change model. What travels is the
*order*, which is why everything in these chapters ranks rather than thresholds. If you must have
a cut-off, derive it on your own set, with your own answer key, and re-derive it whenever the
model changes.

**Two more details are worth noticing in that output.** The top two are separated by 0.0002, which is
nothing — a ranking can be stable in its top *set* and unstable in its *order*, and if you care
about which of two near-ties comes first you need a tie-break your code controls rather than a
third decimal place. And the gap down to third place is huge, 0.994 to 0.415, which is the shape
you hope for and will not always get.

## Why the Best Model Is a Property of Your Data

Now the question that matters, and the one with a real answer.

There is no best embedding model, in the way there is no best lens. A model is fitted on some
distribution of text, and it does well on text like that. Three things about *your* text decide
which model suits it:

**Language.** A model fitted mostly on English does worse on your German support tickets, and a
multilingual model usually trades some English quality for the rest. If your documents are in
one language, say so when you choose.

**Domain.** Legal clauses, clinical notes, error logs and product reviews do not look like each
other, and none of them looks much like the general web text most models see most of.

**Document length.** This is the one people forget, and it has two halves. The first is a hard
limit: **every embedding model has a maximum input length**, counted in tokens, and text past it
is cut off — commonly with no error at all, so you get a vector back and it describes the first
part of your document. Some services reject the request instead, which is the kinder failure and
not the one to plan for. Find that number before you do anything else, because it decides whether
your documents can be embedded whole at all. The second half is softer: within the limit, a model
fitted on sentences still has to compress two thousand words into the same fixed width as a
sentence, and models differ a great deal in how well they do that. Those two facts are not in
tension: the fixed width is what makes a page and a sentence *comparable* at all, and it is also
what forces the compression that makes them unequally well *represented*. Whether your documents arrive as sentences, paragraphs or pages is a property of your
corpus, and Chapter 27 is where you decide how to split them — a decision that interacts with
this one.

**So the way to choose is to measure, on your own documents, with your own queries.** Here is the
smallest version of it. Two candidate models, four of your documents, four of your queries, and
the cosine scores each one gave:

```python
# Two candidate embedding models, run over the same four documents and the
# same four queries. These scores are invented, exactly as the first
# program's vectors were, and they are here to show the shape of the
# comparison rather than to report a measurement.
DOCS = ["short-1", "short-2", "long-1", "long-2"]

SCORES = {
    "model A": {
        "q1 (short)": [0.91, 0.44, 0.30, 0.22],
        "q2 (short)": [0.38, 0.88, 0.25, 0.31],
        "q3 (long)":  [0.71, 0.40, 0.66, 0.35],
        "q4 (long)":  [0.33, 0.29, 0.41, 0.74],
    },
    "model B": {
        "q1 (short)": [0.62, 0.68, 0.40, 0.35],
        "q2 (short)": [0.30, 0.77, 0.41, 0.38],
        "q3 (long)":  [0.45, 0.39, 0.81, 0.44],
        "q4 (long)":  [0.36, 0.40, 0.48, 0.79],
    },
}

# Which document each query is actually about. This is the part only you can
# supply, and the chapter's whole argument is that it is the input that matters.
ANSWER = {"q1 (short)": "short-1", "q2 (short)": "short-2",
          "q3 (long)": "long-1",  "q4 (long)": "long-2"}

# Two ways of grouping the same four queries. Which grouping you use is
# itself a decision about your data, and that is what the second one shows.
BY_LENGTH   = {"q1 (short)": "short", "q2 (short)": "short",
               "q3 (long)": "long",   "q4 (long)": "long"}
BY_LANGUAGE = {"q1 (short)": "en", "q3 (long)": "en",
               "q2 (short)": "de", "q4 (long)": "de"}

def score(rows):
    """Which queries each model got top-1 right."""
    return {q: DOCS[max(range(len(DOCS)), key=lambda i: s[i])] == ANSWER[q]
            for q, s in rows.items()}

def tally(hits, grouping):
    out = {}
    for query, group in grouping.items():
        got, total = out.get(group, (0, 0))
        out[group] = (got + hits[query], total + 1)
    return "   ".join(f"{g} {a}/{b}" for g, (a, b) in sorted(out.items()))

for place, (model, rows) in enumerate(SCORES.items()):
    hits = score(rows)
    if place:
        print()
    for query, scores in rows.items():
        top = DOCS[max(range(len(DOCS)), key=lambda i: scores[i])]
        print(f"  {model}  {query}  top: {top:8}"
              f" {'ok' if hits[query] else 'MISSED'}")
    print(f"  {model}  overall {sum(hits.values())}/4")
    print(f"    by length    {tally(hits, BY_LENGTH)}")
    print(f"    by language  {tally(hits, BY_LANGUAGE)}")
```

```text
  model A  q1 (short)  top: short-1  ok
  model A  q2 (short)  top: short-2  ok
  model A  q3 (long)  top: short-1  MISSED
  model A  q4 (long)  top: long-2   ok
  model A  overall 3/4
    by length    long 1/2   short 2/2
    by language  de 2/2   en 1/2

  model B  q1 (short)  top: short-2  MISSED
  model B  q2 (short)  top: short-2  ok
  model B  q3 (long)  top: long-1   ok
  model B  q4 (long)  top: long-2   ok
  model B  overall 3/4
    by length    long 2/2   short 1/2
    by language  de 2/2   en 1/2
```

**Both models score three out of four, and they are not interchangeable.** A is perfect on the
short documents and misses one of the long; B is the other way round. The overall figure — the
one a benchmark gives you — is identical, so it cannot choose between them.

**And now look at the second breakdown, because it is the one that catches people.** Grouped by
language the two models are *also* identical: de 2/2 and en 1/2, both of them. Grouped by length
they are opposites. Same four queries, same eight results, two groupings, and only one of them
distinguishes the models at all.

So the breakdown is not a trick that rescues you from the average. **It only separates the models
if you group by a property they differ on**, and choosing that grouping is a judgement you make
about your corpus before you run anything. Group by the wrong property and you are
no closer to choosing than the headline left you — and you learn one real thing, that the
property does not discriminate, with the added hazard of feeling thorough.

**And look at what the program needed that no benchmark can give you.** Not the vectors: those
came from the models. The `ANSWER` line — your **answer key**, which document each query is actually about. That is
the only input here that has to come from you, it is the thing that makes the measurement about
*your* data, and it is also the thing people skip, because writing down forty queries and their
answers is dull and reading a leaderboard is quick.

> **Note:** Counting how often the right document came top is the crudest possible score, and it
> is deliberately crude here. It ignores whether the right answer came second instead of tenth,
> which usually matters. **Chapter 26 builds the proper ranking measures from zero** — recall at
> k, mean reciprocal rank, normalised discounted cumulative gain — and Chapter 20 is how you tell
> whether a difference between two models is real rather than luck on four queries. Four queries
> decides nothing; the shape of the argument is what this program is for.

## What a Public Benchmark Score Is

Benchmark tables for embedding models are genuinely useful and they are routinely read for more
than they say. Put one on Chapter 6's ladder and the answer falls out.

A public benchmark is *one study*, run once, on a fixed set of documents and queries that
somebody else chose. It supports exactly what Chapter 6 says one study supports: that it worked
there. What it does not tell you is how the ordering transfers to a different language mix, a
different domain, a different document length, or your queries — and the chapter you just read
shows two models tying on a headline while differing completely underneath.

**It is still the right place to start**, and saying only the sceptical half is its own mistake.
A leaderboard narrows a field of hundreds to a shortlist of three or four in an afternoon, and
nothing else does that. Use it for the shortlist; decide with your own data.

Four things to look at while you are there, and none of them is the top line:

| Look at | Because |
|---|---|
| Which tasks the score averages | Retrieval, classification and clustering are different jobs, and an average hides which one it won |
| The languages in the mix | A high average can be an English score with a multilingual tax |
| The document lengths | A model that tops a sentence-similarity table may not hold a page |
| Vector width and cost | 3,072 numbers per document is four times the storage of 768, for a gain you have not measured |

> **Warning:** The specific benchmarks, which models lead them, and the vector widths on offer
> are the fastest-moving facts in this chapter and will be stale sooner than anything else in
> this book. The method survives: shortlist from the leaderboard, measure on your own set, break
> the result down by the property of your data you most care about.

## Lab: Measure Two Models on Your Own Terms

Three programs, pure Python, nothing to install. Thirty minutes, and there is a key for every
step. Work in a new empty folder.

**Step 1.** Save the first program as `close.py` and run it.

*Expected result:* 0.978, 0.439 and 0.386, in that order. Check the first by hand against the
displayed arithmetic.

**Step 2.** Multiply every number in *my plane left late* by 10 and run it again.

*Expected result:* **nothing changes.** All three cosines are identical to three decimal places,
because the cosine divides by the lengths, which is Chapter 8's result and the reason cosine is
the standard choice here. Note what this does *not* show: nothing says a longer document gets a
longer vector, and many models return vectors of length one anyway, so do not reach for this when
you want to know why a page and a sentence are comparable.

**Step 3.** Now add a fourth sentence whose vector is `[0.80, 0.50, 0.20, 0.10]` — identical to
the first — but call it something unrelated, say *the coffee was cold*. Run it again.

*Expected result:* the output grows from three pairs to six, because four sentences make six
pairs — and two of those six are worth reading twice. *The flight was delayed* and *the coffee
was cold* sit at exactly 1.000, and *my plane left late* and *the coffee was cold* sit at 0.978,
which is the number the chapter's paraphrase pair got. You have not broken anything;
you stated that two texts have the same embedding and the arithmetic believed you. The lesson is
about where trust lives: the cosine is a fact about two vectors, and whether those vectors
deserved to be that close is a fact about the model, which no arithmetic on the output can tell
you.

**Step 4.** Save the ranking program as `rank.py` in the same folder and run it.

*Expected result:* the chapter's three lines. If you see `close.py`'s own output first, its demo
loop is not under `if __name__ == "__main__":`.

**Step 5.** Change `QUERY` to `[0.20, 0.15, 0.85, 0.45]` and run it again.

*Expected result:* *the flight attendant was kind* comes first, at 0.996, and the other two fall
to 0.467 and 0.430. Nothing about the ranking code changed — you moved the query, and
the order followed. Worth doing once because it makes concrete that the index is fixed and the
query is what moves.

**Step 6.** Save the comparison program as `choose.py` and run it. Then answer: if your corpus is
two thousand pages of contracts, which model do you pick, and what does the overall score tell
you?

*Expected result:* both models go 3/4 overall; A is 2/2 on short and 1/2 on long, B the reverse.
On this evidence you would try *B* first, because your documents are long. The overall score
tells you nothing at all — it is the same for both — and that is the point of the step. Four
queries is not enough to decide, as the Note above says; it is enough to show you which number
to look at.

**Step 7.** In `choose.py`, swap `BY_LANGUAGE` so that q1 and q2 are `en` and q3 and q4 are
`de`. Run it. What happens, and what does it tell you about breakdowns?

*Expected result:* model A reads en 2/2, de 1/2 and model B reads en 1/2, de 2/2 — so grouped
this way the two models now look different, where under the chapter's own grouping they looked
identical. Nothing about either model changed. You relabelled the queries, and the grouping that
distinguishes two models is a property of how you cut the data, not of the models. Which is why
the grouping has to come from what you know about your corpus, and not from whichever cut makes
the numbers look decisive.

**Step 8.** In `choose.py`, change `ANSWER` so that `q3 (long)` points at `short-1` instead of
`long-1`. Run it again. What happens, and what have you actually done?

*Expected result:* model A now scores 4/4 and model B 2/4, so A looks clearly better. What you
did was change the labels, not the models — and this is the one lever in the whole procedure that
is yours, which is why the answers have to be written down by someone who knows the documents,
before anybody runs a model. A wrong answer key does not produce an error; it produces a
confident ranking of models, pointing the wrong way.

**Step 9.** A colleague picks the top model from a benchmark table and asks why you want to spend
two days measuring. Give the one-sentence answer, and then the concession.

*Expected result:* because the table's ordering was produced on somebody else's documents and
queries, and the chapter's own example has two models with identical headline scores that are not
interchangeable — so the table cannot tell you which to pick, only which three to try. The
concession matters: the leaderboard did the expensive part, which is narrowing hundreds to a
shortlist, and two days is the right amount of work only for the shortlist.

## Summary, Key Terms, and Review Questions

### Summary

An **embedding model** is a separate model with a different job from a generative one: one piece
of text in, one vector of fixed width out, every time — not Chapter 9's internal *embedding
table*, which is not what you search with. The vector is that text's **embedding**, and this book
does not explain why its arrangement carries anything useful; that is representation learning,
it is on Chapter 17's list, and nothing in these chapters needs it. What you can check is what
the numbers do. Chapter 8's *cosine similarity* is the tool, and it is scale-free. What makes a
page and a sentence comparable is not that, but the fixed width. Applied to three sentences: *the flight was
delayed* and *my plane left late* share no content words and sit at **0.978** on the chapter's
stipulated vectors, while *the flight was delayed* and *the flight attendant was kind* share
three words and sit at **0.439**. Those vectors were written down rather than measured, which is
why the second half of the chapter exists. Read
that correctly — the program did not notice that two sentences mean the same thing; it placed
them close, which is a measurable fact about its output and enough to rank on, and **not**
evidence of meaning. Chapter 25 owns the gap between closeness and relevance. Embed the query with the same
model, sort by cosine, take the top few, and that is dense retrieval complete. A raw cosine has **no meaning on its own** —
not across models, not across queries, not across corpora — so rank by it and do not threshold
on it. Every embedding model also has a **maximum input length**, past which your text is cut off
with no error, and that is the first thing to find out. **The best model is a property of your
data**, through language, domain and document length, so measure: two candidate models over four
documents and four queries both scored 3/4 overall while A went 2/2 on short documents and 1/2
on long, and B the reverse. Grouped by language, though, the two were *identical* — so a
breakdown only helps when you group by the property that matters for your corpus, and choosing
that property is a judgement you make before you run anything. The one input no benchmark can supply is **which document each query is
actually about**, and it is the one people skip. A public benchmark is *one study* on Chapter
6's ladder — it worked there, on somebody else's corpus — which makes it the right way to
shortlist three models in an afternoon and the wrong way to pick one.

### Key Terms

| Term | Meaning |
|---|---|
| **Embedding model** | A model whose whole job is to turn one piece of text into one vector of fixed width. No output tokens, nothing to continue |
| **Embedding** | The vector an embedding model returns for a given text. Its width is the model's, and it is the same for a word, a sentence and a page |
| **Dense retrieval** | Embedding every document once, embedding the query at search time with the *same* model, and ranking by cosine |
| **Answer key** | Which document each of your queries is actually about. The only input in the procedure that has to come from you |

### Worth Memorising

| Item | Value or formula |
|---|---|
| What you get back | One vector, fixed width, per text. A few hundred to a few thousand numbers |
| The comparison | Chapter 8's cosine. Scale-free: multiplying a vector by 10 does not move it |
| What a high cosine is | A fact about two vectors. **Not** evidence that two texts mean the same |
| Dense retrieval | Embed the documents once, embed the query per search with the same model, sort by cosine |
| What decides the model | Your language, your domain, your document length. Length first: it is the one that gets forgotten |
| The hard limit | Every embedding model has a maximum input length. Past it, text is cut off, usually with no error |
| A raw cosine | Has no meaning on its own. Not comparable across models, queries or corpora — rank, do not threshold |
| What a benchmark is | One study, somebody else's corpus. A shortlist of three, not a choice of one |
| The input only you have | The answer key: which document each query is about |

### Review Questions

1. How would you choose an embedding model for your own data?
2. Why is a public benchmark score a starting point rather than a verdict?
3. Two sentences with no words in common get a cosine of 0.978. What has that established?
4. What is the difference between the embedding table in Chapter 9 and an embedding model?
5. Your documents are 40-page contracts. What does that fact alone tell you about model choice?

### Review Answers

1. Shortlist from a public table, then measure the shortlist on your own documents with your own
queries. The measurement needs one thing nobody can give you: an answer key, which is which
document each query is actually about — forty or so queries, written down by somebody who knows
the corpus, before any model is run. Then score each candidate and, crucially, **break the score
down by whatever property of your data you most care about**, because an overall figure can be
identical for two models that are not interchangeable: the chapter's two both score 3/4, while
one is 2/2 on short documents and 1/2 on long and the other is the reverse. The properties worth
breaking down by are language, domain and document length, and length is the one that gets
forgotten. Two things to add unprompted: the crude score of *did the right document come top* is
enough to show the shape but not enough to decide, so use Chapter 26's ranking measures and
Chapter 20's interval to say whether a difference is real; and the choice interacts with how you
split your documents, which is Chapter 27.
2. Because it is one study, in Chapter 6's sense, run on a fixed set of documents and queries
somebody else chose, so what it supports is that those models ranked that way *there*. Your
language mix, your domain and your document lengths are all different, and the ordering is not
guaranteed to survive any of them — the chapter's own pair of models have identical overall
scores and opposite strengths, which is what an average can do to a difference that
matters. Say the concession too, because it is the part that shows you have used one: a
leaderboard narrows hundreds of models to three or four in an afternoon and nothing else does
that, so it is exactly right for the shortlist and wrong for the decision. And when you are
reading one, look at what the average is averaging, at the language mix, at the document lengths
and at the vector width, rather than at the top line.
3. That the model placed those two texts close together. That is a fact about the model's output,
it is measurable, and it is enough to rank on — which is the whole basis of dense retrieval. It
is **not** evidence that the model understood the sentences or that they mean the same thing, and
the distinction is not pedantry: you can hand two unrelated texts the same vector and the cosine
will report 1.000 quite happily, because the arithmetic has no access to anything but the
numbers. Whether closeness tracks the relevance you actually want is a separate question with a
genuinely unsatisfying answer, and Chapter 25 owns it.
4. Different models, different jobs, different outputs. Chapter 9's embedding table is a matrix
*inside* a generative model with one row per vocabulary entry; looking a token up in it is how
that token enters the computation. It is internal, it is per-token, and it is not what you search with. An embedding model is a model of its own: you give it a piece of text of any length and it
returns one vector of fixed width, with no output tokens and nothing to continue. The shared word
is unfortunate and the two are not interchangeable in any direction.
5. First, that you need the maximum input length of every candidate before anything else, because
forty pages will exceed most of them and the usual failure is silent: you get a vector describing
the first part of the contract and no error. Then: document length is your first filter on
quality too, and most of the shortlist will be wrong for you. A model fitted on sentences has to
compress forty pages into the same fixed width as a sentence, and models differ a great deal in how well they do that — so a sentence-similarity
leaderboard is close to useless for you, and you want candidates evaluated on long-document
retrieval. It also tells you the choice is entangled with a decision you have not made yet: how
to split the contracts before embedding them, because you will almost certainly not embed forty
pages as one vector. That is Chapter 27, and the two decisions should be made together rather
than in sequence.

> **You understand this when** you can say what a cosine of 0.978 does and does not establish,
> and name the one input a benchmark cannot give you.
