# Where Dense Search Fails

Chapter 24 built dense retrieval and left a debt: it said twice that a high cosine is a fact
about two vectors and not evidence that two texts mean the same, and handed the gap here. This
chapter pays it, and what you get for it is the ability to say where ranking by closeness fails
and why, to tell which of those failures is a derivation and which is an observation, and to
know what a page of plausible results does and does not entitle you to conclude.

*The problem.* My semantic search is clever about meaning and completely useless when I search
for a part number.

*The question.* Where does ranking by closeness fail, why, and what can you tell about it by
looking?

A note on the first word of the problem. **Semantic search** is what people usually call this,
and it is the phrase you will hear; Chapter 24's term for the mechanism is dense retrieval, and
they mean the same thing. This chapter uses the book's term except where it is quoting the
complaint.

## A Part Number Is Almost No Signal

Take two maintenance notes that differ in one token out of ten, and a query naming one of the
two parts.

```python
import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x*x for x in a)) * math.sqrt(sum(y*y for y in b)))

# Two maintenance notes that differ in one token out of ten, and a query
# naming one of the two parts. The vectors are written out; they sit close
# together for the reason the chapter gives, not because that is convenient.
B = [0.71, 0.52, 0.30, 0.18]      # ...pump X-4471-B before servicing
D = [0.70, 0.53, 0.30, 0.19]      # ...pump X-4471-D before servicing
SCHEDULE = [0.64, 0.49, 0.33, 0.22]
QUERY = [0.69, 0.54, 0.29, 0.20]  # "X-4471-D seal replacement"

DOCS = {"X-4471-B note": B, "X-4471-D note": D, "maintenance schedule": SCHEDULE}

if __name__ == "__main__":
    print(f"  the two notes, compared with each other: {cosine(B, D):.5f}")
    print(f"  the whole distance between them: {1 - cosine(B, D):.5f}\n")

    ranked = sorted(DOCS, key=lambda d: cosine(QUERY, DOCS[d]), reverse=True)
    for place, doc in enumerate(ranked, 1):
        print(f"  {place}  {cosine(QUERY, DOCS[doc]):.5f}  {doc}")
    a, b = (cosine(QUERY, DOCS[d]) for d in ranked[:2])
    print(f"\n  the right note wins by {a - b:.5f}")
```

```text
  the two notes, compared with each other: 0.99983
  the whole distance between them: 0.00017

  1  0.99978  X-4471-D note
  2  0.99928  X-4471-B note
  3  0.99712  maintenance schedule

  the right note wins by 0.00050
```

A reader doing the arithmetic will ask how the winning margin, 0.00050, can be three times the
distance between the two notes, 0.00017. The margin is not a distance between a pair at all: it
is the *difference of two distances from the query*, 0.00072 for the wrong note against 0.00022
for the right one. The query sits a little to one side of the pair, so it is slightly nearer one
of them, and that difference is what the margin reports. What matters is that all three numbers
are tiny.

**The right note came first, and look at what by.** Five parts in ten thousand, out of a
distance between the two notes of 0.00017.

**Be careful what that demonstrates, because it is less than it looks.** These vectors were
written down, so the chapter has not shown that a model *does* place two such texts this close.
What it shows is the consequence *if* it does, and the consequence is the point: when two
documents sit 0.00017 apart, a search that ranks by cosine has nothing else to rank them on. The
ordering is decided by the residual, and five parts in ten thousand is not a quantity any model
is stable to.

**That dense retrieval loses to lexical retrieval on identifier queries is an observation, not
a derivation**, and it belongs on Chapter 6's ladder rather than off it. Where on the ladder is
not something this chapter can settle for you: that would take the practitioner reports and the
written-down failure modes, and the honest statement is that the claim is widely made and that
you should check it on your own identifier queries, which Step 8 of the lab asks you to do.

What a mechanism can offer in its place is a *sketch* of why, and the sketch is Chapter 24's
fixed width — one vector of a few hundred numbers has to stand for the whole text, and a string
appearing once has to compete for that room with everything else in the document. That is a
reason to expect the failure. It is a sketch and not a calculation, and the reason it cannot be
a calculation is simple: this book never says how the tokens become one vector. It declines to,
in Chapter 9's Warning and again in Chapter 24's. Without that step there is no arithmetic to
do, so nothing here computes what a token is "worth" — and the 0.00017 above is a distance
between two stipulated vectors, not a token's share of anything.

**The cases are the familiar ones:** a part number, a surname, an invoice number, an error code,
a SKU, a date, a version string. The thing you are searching *for* is a small part of the thing
you are searching *with*.

**And Chapter 10 has something to add, though not what you might expect.** A rare code is not
one token: `X-4471-B` is cut into several pieces, because no corpus saw it often enough to merge
it. That raises the number of tokens it occupies and lowers the specificity of each — the pieces
are mostly common fragments, a letter, a hyphen, a two-digit group, each appearing in countless
other strings — so little of what survives is specific to *this* code.

> **Note:** The vectors here are written out, as Chapter 24's were, and for the same reason: a
> real embedding model is not available to a lab that installs nothing. Be exact about what that
> costs. The premise — that a model places two texts differing in one character close
> together — is an observation about trained models, and this book cannot derive it; it is the
> kind of claim Chapter 9's Warning and Chapter 24's both decline to explain. What *is*
> derivable, and what this section turns on, is the consequence: given two documents that close
> together, a cosine has nothing left to separate them with. Check the premise on your own data
> in one line as soon as you have a model.

## Similarity Is Symmetric. Relevance Is Not.

Now the second failure. Part of this one is a derivation, and the derivation is the half that
needs no numbers at all — so read the printed numbers as the illustration and the paragraph
after them as the argument.

```python
from codes import cosine

QUERY   = [0.62, 0.55, 0.31, 0.22]      # "was my refund approved?"
APPROVED = [0.64, 0.54, 0.30, 0.21]     # "Your refund was approved."
REFUSED  = [0.63, 0.55, 0.31, 0.20]     # "Your refund was not approved."

print(f"  approved  {cosine(QUERY, APPROVED):.5f}")
print(f"  refused   {cosine(QUERY, REFUSED):.5f}")
print(f"  and the two answers, compared with each other:"
      f" {cosine(APPROVED, REFUSED):.5f}\n")

# Cosine is symmetric. Relevance is not.
print(f"  cos(query, approved) = {cosine(QUERY, APPROVED):.5f}")
print(f"  cos(approved, query) = {cosine(APPROVED, QUERY):.5f}")
print(f"  identical: {cosine(QUERY, APPROVED) == cosine(APPROVED, QUERY)}")
```

```text
  approved  0.99958
  refused   0.99970
  and the two answers, compared with each other: 0.99976

  cos(query, approved) = 0.99958
  cos(approved, query) = 0.99958
  identical: True
```

**Read the third number first.** *Your refund was approved* and *Your refund was not approved*
are 0.99976 similar to each other — **closer to each other than either is to the query.** They
are opposite in meaning and nearly identical as vectors, because *not* is one token among five.

So the ordering between the true answer and its negation is decided by whatever is left after
that. Here the negation won; the point is not that it always will, and these are typed numbers.

**The claim that survives is about the score rather than the outcome**, and it is worth being
careful about how it is put. It is tempting to say a cosine has no term representing polarity,
but that proves far too much: a cosine has no term representing *anything*, since no single
number in these vectors means a nameable thing — Chapter 9 says so outright. The same sentence
would therefore deny the method any handle on topic, and Chapter 24's paraphrase with no shared
words refutes that.

The narrow claim is about what the number gives you to work with. Whatever separates these two
sentences is whatever the model left after *not*, and that residual reaches you only as one
number that also carries everything else about both texts. So you have *no handle on that
ordering*: you cannot tune it, you cannot put a threshold on it, and you cannot tell from the
score which of the two documents you are holding. A search that cannot tell *approved* from *not
approved* is not a search for whether your refund was approved, and no amount of looking at the
scores will tell you which case you are in.

**Now the structural half, which holds for every model and needs no numbers.** Cosine is
symmetric: `\(\cos(a,b) = \cos(b,a)\)`{=latex}, as the last two lines show, and it follows
immediately from Chapter 8's formula: the dot product is symmetric, and the denominator is the
two lengths multiplied together, which multiplication leaves unchanged.

**Relevance is not symmetric.** That word is worth pinning down, because it is what dense
retrieval is estimating: **relevance** is whether this document answers that question, for this
asker. A one-line answer can
be exactly what a long question needs,
while that long question is useless as an answer to the one-line query. A glossary entry is
relevant to *what does idempotent mean*; the question is not relevant to the entry. A summary answers a
request for a summary, and the document it summarises does not.

So similarity and relevance have different shapes. **One is a symmetric function of two texts.
The other is a directed judgement about whether this document answers that question, and it
depends on who is asking and why.**

**Here is the impossibility that follows, stated no wider than it holds.** Put two texts through
*the same* encoder and compare them with a cosine, and you get one number — so that arrangement
cannot distinguish *x answers y* from *y answers x*. The question has a direction and the number
does not.

**And here is what removes it**, because an argument like that is only worth having if you know
its escapes. Score the query and the document *together*, with a model that sees both at once,
and the score is free to be asymmetric — that is Chapter 26's reranking. Or encode the two sides
differently, with separate query and document encoders, or with a marker that tells one model
which side it is embedding: then the score is `\(\cos(f(q), g(d))\)`{=latex} with
`\(f \neq g\)`{=latex}, which is *not* symmetric in the two texts.

> **Note:** That separately encoded sides are common in current retrieval models is a statement
> about today's practice, not a lasting principle, and it is the kind of detail to check rather
> than memorise. The lasting part is the shape of the argument: one encoder and a cosine give
> you one symmetric number, and two encoders or a joint score do not.

So the honest conclusion is narrow: a single shared encoder
compared by cosine is the wrong shape for a directed question, and getting the right shape means
changing the arrangement rather than improving the model.

> **Tip:** This is the sentence to have ready, because it is the question's real answer rather
> than a list of failure cases: similarity is a symmetric number computed from two texts, and
> relevance is a directed judgement that depends on the asker. Dense retrieval uses the first as
> an estimate of the second, which is a useful approximation and never an identity. Then carry
> the edge, because it is what shows you have used this: the symmetry goes away as soon as the
> two sides are encoded differently or scored together, so the limit is a property of *one
> shared encoder with a cosine*, not of retrieval.

## Why You Cannot Judge This by Eye

Here is the failure that costs the most, because it is the one that hides.

```python
from codes import cosine

QUERY = [0.70, 0.50, 0.30, 0.20]   # "can I get a refund on an order
                                   #  I cancelled six weeks ago?"

# Six documents. Only one of them answers that question, and you know which
# because somebody wrote it down - not because anything here can tell.
DOCS = {
    "overview of refunds":        [0.71, 0.51, 0.29, 0.19],
    "refund policy summary":      [0.70, 0.52, 0.30, 0.18],
    "how refunds are calculated": [0.69, 0.49, 0.31, 0.21],
    "shipping and returns":       [0.68, 0.50, 0.32, 0.20],
    "payment methods":            [0.66, 0.48, 0.33, 0.23],
    "refund for a cancelled order after 30 days": [0.55, 0.61, 0.38, 0.30],
}
ANSWERS = {"refund for a cancelled order after 30 days"}

ranked = sorted(DOCS, key=lambda d: cosine(QUERY, DOCS[d]), reverse=True)
print("  what you would look at - the top three:")
for place, doc in enumerate(ranked[:3], 1):
    print(f"    {place}  {cosine(QUERY, DOCS[doc]):.4f}  {doc}")
print("\n  where the one that answers the question actually came:")
for place, doc in enumerate(ranked, 1):
    if doc in ANSWERS:
        print(f"    {place}  {cosine(QUERY, DOCS[doc]):.4f}  {doc}")
```

```text
  what you would look at - the top three:
    1  0.9998  overview of refunds
    2  0.9998  how refunds are calculated
    3  0.9996  shipping and returns

  where the one that answers the question actually came:
    6  0.9716  refund for a cancelled order after 30 days
```

**The top two print as the same number**, 0.9998 against 0.9998. Printed to ten places they are
0.9998056809 and 0.9997993270, so the difference between them is about six parts in a
million — Chapter 24's near-tie, arriving where it matters. Which of those two comes first is
not a fact about the documents.

**Now look at the top three and ask yourself whether anything is wrong.** *Overview of refunds*,
*how refunds are calculated*, *shipping and returns* — for a question about a refund, those are
three entirely reasonable results. Nothing in them is absurd. Nothing in them is off-topic.
There is nothing to notice.

**And the only document that answers the question is sixth of six.** Last.

This is the asymmetry that makes retrieval hard to improve by inspection:

| What you can see by looking | What you cannot |
|---|---|
| Whether the results you got are plausible | Whether the result you needed was there |
| That nothing in the top few is obviously absurd | What the top few displaced |
| That the scores are high | That a high score is not evidence of meaning — which is this chapter's own conclusion, and the negation case is why |

**Everything in the first column is about the documents in front of you. Everything that
matters is about the one that is not.** A missing document leaves no trace in a result list.
There is no gap where it should have been, no warning, no low score — the list is simply three
plausible things, which is exactly what a good list also looks like.

**And this one does not rest on the invented vectors**, which is worth saying because the other
two sections had to be careful about exactly that. Delete the answering document and the top
three cannot change, because removing an item ranked below third cannot reorder the three above
it — for any numbers whatsoever. A corpus that never held the answer and a ranking that buried
it therefore produce the *same* result list, so no inspection of that list can tell them apart.
The vectors decide which case this example is; they do not decide that the two cases look alike.

That is why the most common report about a search system is that it *seems* fine, and why
seeming fine is consistent with being badly broken.

## What You Can Conclude Without an Answer Key

So what does looking buy you? Something, and it is worth naming, because the answer is not
*nothing*.

**You can conclude that a result is wrong.** If a query about refunds returns a page about
payroll, you have found a real defect by inspection, and no judgements were needed. Inspection
is a sound way to find *present* errors.

**From the result list, you can conclude nothing about what is missing.** Not whether anything
is, not how much, not which queries are affected. The information is not in the list, and no
amount of staring adds it. Someone who knows the corpus *can* tell you a document is missing —
but they are using knowledge from outside the list, which is the whole point, and writing that
knowledge down is what the next section is about.

The thing that closes the gap is the one Chapter 24 named: an *answer key* — for each query,
which documents actually answer it, written down by somebody who knows the corpus, before any
search is run. Each of those recorded decisions is a **relevance judgement**, and they are what
the key is made of. With it you can say how often the right document was found and where it ranked.
Without it, every statement of the form *our search works well* is a statement about how the
results looked to whoever last looked.

**Chapter 26 turns that key into measures** — it builds the standard ranking measures from zero
and names what each one does and does not capture. Chapter 20 is how you decide whether a
difference between two systems is real rather than luck on a handful of queries. This chapter's
job is narrower: to establish that the key is not optional, and why.

> **Warning:** The expensive version of this mistake is a demonstration. Somebody runs five
> queries they thought of, in front of a room, and the results look reasonable — because results
> usually do. That is a demonstration on Chapter 6's ladder, which supports "it can work once",
> and the five queries were chosen by the person showing you. It is not evidence about the other
> ten thousand queries, and the thing it is least able to detect is the thing most likely to be
> wrong.

## And What to Do About It

This chapter is a list of limits, so it owes you the shape of the answer even though it owns
none of it.

| Failure | Where it is handled |
|---|---|
| Part numbers, names, codes, rare words | Chapter 26: lexical retrieval, which matches the words and strings as written, combined with dense |
| Similarity is not relevance | Chapter 26's reranking, which scores a query and a document *together* rather than comparing two vectors |
| You cannot see what is missing | Chapter 26's measures, on Chapter 24's answer key |
| Documents too long or badly split to match | Chapter 27 — not a limit of dense retrieval, a limit of the pipeline around it |
| The right passage retrieved and still not used | Chapter 28 — the same |

**None of this makes dense retrieval a bad idea.** Matching two texts with no words in common is
something lexical retrieval cannot do at all, and dense retrieval can — that capability is real,
and Chapter 24's vectors were stipulated, so take the capability on its own terms rather than
from that demonstration. The conclusion is narrower and more useful: **dense retrieval is one
signal, it is strong on meaning and weak on identifiers, it is symmetric where the task is
directed, and its failures are invisible to inspection.** Each of those last three limits is
what Chapter 26 takes up; Chapters 27 and 28 handle the two pipeline failures in the table
above, which are not limits of dense retrieval at all.

## Lab: Find the Failures Yourself

Three programs, pure Python, nothing to install. Thirty minutes, and there is a key for every
step. Work in a new empty folder.

**Step 1.** Save the first program as `codes.py` and run it.

*Expected result:* the two notes at 0.99983 of each other, so a distance of 0.00017 between
them, and the right note winning by 0.00050.

**Step 2.** Change `D`'s second number from `0.53` to `0.50` and run it again.

*Expected result:* the wrong note now comes first — `X-4471-B` at 0.99928 against `X-4471-D` at
0.99903 — and the two notes are still 0.99981 of each other, so they are still describing almost
the same text. Three hundredths on one of four numbers was enough.

**And read the last line of the output, which now says something false:** *the right note wins
by 0.00025*. It says that because the program takes the top result and calls it right, which is
the assumption this whole chapter is attacking, written into a print statement. Fix the label if
you like; the more useful thing is to notice how easily that assumption gets into code, and that
nothing failed when it did.

**Step 3.** Save the second program as `negate.py` in the same folder and run it.

*Expected result:* approved 0.99958, refused 0.99970, the two answers 0.99976 of each other, and
`identical: True` for the two directions of the cosine. If you see `codes.py`'s own output
first, its demo is not under `if __name__ == "__main__":`.

**Step 4.** Which number in that output is the one to quote, and why?

*Expected result:* 0.99976 — the two answers compared with each other. It is higher than either
answer's similarity to the query, which says the true answer and its negation are closer to each
other than either is to the question. That is the fact that makes the ordering between them
arbitrary. The 0.99970 beating 0.99958 is just which way the arbitrary fell this time.

**Step 5.** Save the third program as `eye.py` and run it. Then cover the second half of the
output and ask yourself, from the top three alone, whether this search is working.

*Expected result:* the top three are *overview of refunds*, *how refunds are calculated* and
*shipping and returns*, and from them alone the honest answer is that you cannot tell. They are
plausible. The document that answers the question is sixth. Nothing in the first three indicates
that, and that is the whole point of the step.

**Step 6.** In `eye.py`, delete the line for *refund for a cancelled order after 30 days*
entirely, and run it again.

*Expected result:* the top three are *identical* — and notice this is not an experiment, it is a
consequence, the one the body states. Removing an item ranked below third cannot change the top
three, for any numbers whatsoever. That is why this section does not depend on the invented
vectors: a corpus missing the answer and a ranking burying it produce the same top three, so
neither can be diagnosed from one. The one thing that does change is the last line, which now
has a heading and nothing under it.

**Step 7.** Your colleague demonstrates the search with five queries and all twenty-five results
look sensible. What have you learned, and what would you ask for?

*Expected result:* that the system returns plausible results on five queries somebody chose,
which on Chapter 6's ladder is a demonstration and supports *it can work once*. You have learned
nothing about what those five queries missed, and nothing about the queries nobody tried. Ask
for an answer key — a set of queries with the documents that actually answer them, written down
independently — and for where the right document ranked on each.

**Step 8.** Give an example of a query that meaning-based search gets wrong, and say why in one
sentence of mechanism rather than one of complaint.

*Expected result:* any identifier will do — *invoice 4471-B*, *error E0432*, *the Nakamura
contract* — and the sketch is that the vector describes the whole text at a fixed width, so a
string appearing once has to compete for that room with everything else in the document. Say
*sketch* rather than *calculation*, because nothing here computes a token's share. The negation
case is the other good answer: *was my refund approved* gives a score that cannot tell you
whether you have the answer or its negation, because *not* is one token among five. Then do the
check the body asks for: twenty identifier queries from your own data, with where each answer
ranked.

## Summary, Key Terms, and Review Questions

### Summary

Dense retrieval fails in three ways, and they do not stand on the same kind of support. **A part
number is almost no signal**: two maintenance notes differing in one token of ten sat 0.99983
from each other — a distance of 0.00017 — and the right note won by 0.00050, which is the
difference of two distances from the query rather than a distance between any pair. That dense
retrieval loses to lexical retrieval on such queries is an *observation*; what a mechanism
offers is a sketch, Chapter 24's fixed width, since one vector must hold the whole text and a
string appearing once competes for that room with everything else. It is a sketch and not a
calculation, because this book never says how tokens become one vector. Names, invoice numbers,
error codes, SKUs and version strings are all that case, and Chapter 10 compounds it, since a
rare code is cut into pieces that are mostly common fragments, so little of what survives is
specific to this code. **Similarity is symmetric and relevance is not.**
*Your refund was approved* and *Your refund was not approved* sat 0.99976 from each other —
closer to each other than either was to the question — so what separates them is a residual, and
the claim that survives is about the score rather than the outcome: that residual reaches you as
one number carrying everything else too, so you cannot tune it, threshold it, or tell from the
score which document you hold. Structurally,
`\(\cos(a,b) = \cos(b,a)\)`{=latex} follows from Chapter 8's formula, while relevance is a
directed judgement that depends on who is asking: a glossary entry answers *what does idempotent
mean* and the question does not answer the entry. A better model narrows that gap and cannot
close it, because the two are not the same kind of object. **And the failures are invisible.** A
top three of *overview of refunds*, *how refunds are calculated* and *shipping and returns* is
entirely plausible while the only document that answers the question sits sixth of six; delete
that document and the top three *cannot* change, which is why a buried answer and an absent one
produce the same list. Everything inspection can see is about the documents in front of you, and
everything that matters is about the one that is not. So you can conclude by eye that a *present*
result is wrong, and from the list alone nothing about what is missing — someone who knows the
corpus can tell you, and that is knowledge from outside the list.
What closes the gap is Chapter 24's *answer key*, written before any search is run; Chapter 26
turns it into measures and Chapter 20 says whether a difference is real. None of this makes
dense retrieval a bad idea: matching two texts with no words in common is something lexical
retrieval cannot do at all, and that capability is the reason to use it. It makes it *one
signal*: strong on meaning, weak on identifiers, symmetric where the task is directed, and
failing where you cannot see. Each of those last three is what Chapter 26 takes up.

### Key Terms

| Term | Meaning |
|---|---|
| **Semantic search** | What dense retrieval is usually called. The same thing, in the words people use when they complain about it |
| **Relevance** | Whether this document answers that question, for this asker. A directed judgement, not a distance |
| **Relevance judgement** | One recorded decision that a given document does or does not answer a given query. The unit an answer key is made of |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Why identifiers fail | A sketch, not a calculation: the vector holds the whole text at a fixed width, so a string appearing once competes for that room with everything else |
| What kind of claim that is | An observation on Chapter 6's ladder. The mechanism gives a reason to expect it, not a derivation |
| The illustration | Two notes differing in one character, on stipulated vectors: 0.99983 apart, so a distance of 0.00017 |
| Similarity against relevance | `\(\cos(a,b) = \cos(b,a)\)`{=latex} always. Relevance depends on which is the question |
| The negation case | On stipulated vectors, a true answer and its negation sat closer to each other than either did to the query |
| What the negation case proves | Nothing about which one ranks first. It is a claim about the score: you get no handle on that ordering, so you cannot tune or threshold it |
| What inspection finds | A wrong result that is present. Not a right result that is missing from the list |
| What a five-query demo is | A demonstration on Chapter 6's ladder: it can work once |

### Review Questions

1. Give me a query that meaning-based search gets wrong, and say why.
2. Why is similarity not the same thing as relevance?
3. Your search returns three plausible results for every query you try. What do you know?
4. A colleague says a better embedding model will fix your part-number problem. Is that right?
5. What is the cheapest thing you can do to find out whether your retrieval is any good?

### Review Answers

1. Any identifier. *Invoice 4471-B*, *error code E0432*, *the Nakamura contract* — and the
mechanism is the thing to lead with, not the example. The embedding describes the whole text at
a fixed width, so a string appearing once has to compete for that room with everything else in
the document. Call that a *sketch* of why rather than a calculation, because it takes a step this
book does not supply: how the tokens become one vector. On two stipulated vectors a token of ten
left the two notes 0.99983 from each other — a distance of 0.00017 — so which of them a query
ranks first is decided by a residual that small. Chapter 10's tokeniser compounds it, because a
rare code is cut into pieces that are mostly common fragments, so little of what survives is
specific to this code. The second good answer is the negation case: for *was my refund approved*,
the score cannot tell you whether you are holding the answer or its negation, because *not* is
one token among five. And finish with the check, because a sketch is not a plan: write down
twenty identifier queries with the documents that actually answer them, and see where each one
ranked.
2. Because they are different kinds of object, and the structural argument is better than any
list of cases. Similarity is a symmetric number computed from two texts —
`\(\cos(a,b) = \cos(b,a)\)`{=latex} falls straight out of Chapter 8's formula, since the dot
product is symmetric and the denominator is the two lengths multiplied together, which
multiplication leaves unchanged. Relevance is a *directed* judgement about whether this
document answers that question, and it depends on who is asking and what for: a glossary entry
is relevant to *what does idempotent mean*, and the question is not relevant to the entry; a
summary answers a request for a summary, and the document it summarises does not. Dense
retrieval uses the first as an estimate of the second, which is a useful approximation and never
an identity. The consequence worth adding is the one that shows you have used this, and it is a
statement about the *arrangement* rather than about retrieval: one shared encoder compared by a
cosine gives you a single symmetric number, so no better model makes that arrangement able to
tell *x answers y* from *y answers x*. Changing the arrangement does. Score the query and the
document together, or encode the two sides with different encoders, and the score is free to be
asymmetric.
3. That the results are plausible, which is almost what you knew before. Plausible is what a
good list looks like and also what a badly broken one looks like, because a missing document
leaves no trace in a result list — no gap, no warning, no low score. The chapter's own example
has a top three that is entirely reasonable while the one document answering the question sits
sixth, and deleting that document leaves the top three unchanged. So what you know is that
nothing *present* is obviously wrong, which is worth something: inspection is a sound way to
find errors that are there. What you do not know is anything about what is missing — not
whether, not how much, not which queries. And if the queries were chosen by whoever is showing
you, you have a demonstration in Chapter 6's sense and nothing more.
4. Partly, and the word is doing a lot of work. A better model will narrow the gap, because some
models place identifiers better than others and the difference is measurable — Chapter 24 is how
you would find out. But the sketch of the problem is about the arrangement rather than the
model's quality: the vector has a fixed width and must describe the whole text, so a string
appearing once competes for that room with everything else, and a better model still has the
same room to allocate. The thing that actually fixes identifier search is a method that matches
the words and strings as written, which is lexical retrieval, combined with the dense signal
rather than replacing it — Chapter 26. So the honest answer is: a better model is worth
measuring and should not be expected to fix this; what fixes it is not a model.
5. Write an answer key. Take thirty or forty real queries — from your logs if you have them —
and, for each, have somebody who knows the corpus write down which documents actually answer it,
before anybody runs a search. That is the cheapest thing because it is the only missing input:
everything else, the retrieval and the scoring, you already have. With it you can say how often
the right document was found and where it ranked; without it every claim about your search being
good is a claim about how the results looked to whoever last looked. Chapter 26 is the measures
you then compute, and Chapter 20 is how you tell whether a difference between two configurations
is real rather than luck on forty queries.

> **You understand this when** you can explain why a plausible top three tells you almost
> nothing, in one sentence that does not use the word *bad* — and say what has to change about
> the arrangement, not the model, for a symmetric score to answer a directed question.
