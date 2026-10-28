# Assembling the Context: Reranking, Citations, Long Context

Chapter 26 left this chapter two questions it declined to answer: how many candidates to keep —
a different number from how many reach the model, as the first section insists — and what
reranking looks like as a step in building something rather than as an arrangement.
Chapter 27 left it a third: a sentence split across two rows, with an offset stored so somebody
could put it back. This chapter is that somebody. What you get for it is the arithmetic of what
fits, the repair for a split answer, a citation a reader can actually check, and an answer to
*long context or retrieval* that is neither a shrug nor a slogan.

*The problem.* I found the right passages. The answer still ignored them, and I can't prove
where it came from.

*The question.* Between a ranked list of passages and a reply you can defend, what are the
decisions, and which of them are yours?

## The Rows Retrieval Hands You

Start from where Chapter 27 stopped: an index of chunks, each carrying its text, its document
and its offset.

```python
"""The index chapter 27 built: rows of chunk text with where they came from."""

DOCS = {
    "refunds.pdf": (
        "Returns are handled by the support team. "
        "A refund is issued to the original payment method within 14 days. "
        "A cancellation after dispatch carries a fee of 10 per cent."
    ),
    "shipping.pdf": (
        "Standard delivery takes three working days. "
        "Express delivery is next day if ordered before noon. "
        "We do not deliver to post office boxes."
    ),
}

def rows(size=60):
    out = []
    for name, text in DOCS.items():
        for n in range(0, len(text), size):
            out.append({"id": f"{name}#{n // size}", "doc": name,
                        "start": n, "text": text[n:n + size]})
    return out

if __name__ == "__main__":
    rs = rows()
    print(f"  {len(rs)} rows across {len(DOCS)} documents\n")
    for r in rs:
        print(f"    {r['id']:16s} start {r['start']:3d}  {r['text'][:30]!r}")
```

```text
  6 rows across 2 documents

    refunds.pdf#0    start   0  'Returns are handled by the sup'
    refunds.pdf#1    start  60  'to the original payment method'
    refunds.pdf#2    start 120  'n after dispatch carries a fee'
    shipping.pdf#0   start   0  'Standard delivery takes three '
    shipping.pdf#1   start  60  ' is next day if ordered before'
    shipping.pdf#2   start 120  'st office boxes.'
```

Two documents cut at sixty characters, deliberately badly, so the problems are visible. The
refund answer is split between rows 0 and 1 exactly as it was in Chapter 27.

**Context assembly** is what happens next: turning some of these rows, plus an instruction, plus
the question, into the request the model is given — spread across Chapter 18's message list
rather than one block of text, but counting against one window all the same. It is the step nobody writes down
and everybody has, and it is made of decisions rather than defaults.

## What Fits Is Arithmetic

```python
"""Building the context: what fits, what gets dropped, what order."""
from store import rows

INSTRUCTION = (
    "Answer using only the passages below. Quote the passage you "
    "used and give its id. If none of them answers the question, "
    "say so."
)
QUESTION = "How long does a refund take?"

def build(instruction, question, passages, budget):
    """Assemble a context under a character budget. The instruction and
    the question go in first, because a passage that displaces the
    instruction has displaced the task."""
    fixed = len(instruction) + len(question)
    if fixed > budget:
        raise ValueError("no room for the instruction and the question")
    left = budget - fixed
    kept, dropped = [], []
    for p in passages:
        block = f"[{p['id']}] {p['text']}\n"
        if len(block) <= left:
            kept.append(p)
            left -= len(block)
        else:
            dropped.append(p)
    return kept, dropped, left

if __name__ == "__main__":
    rs = rows()
    print(f"  instruction {len(INSTRUCTION)} chars, question "
          f"{len(QUESTION)} chars")
    print(f"  {len(rs)} candidate passages, about "
          f"{len(rs[0]['text'])} chars each\n")

    print("  how many passages fit, by budget:")
    print("  budget   kept   dropped   room left")
    for budget in (200, 300, 500, 700):
        kept, dropped, left = build(INSTRUCTION, QUESTION, rs, budget)
        print(f"  {budget:6d}   {len(kept):4d}   {len(dropped):7d}"
              f"   {left:9d}")

    print("\n  at 300 the context holds two passages. Which two is")
    print("  decided by the order you hand them over in, and that")
    print("  order is yours to choose, not the retriever's:\n")
    best_first = rs
    worst_first = list(reversed(rs))
    for name, order in (("as retrieved", best_first),
                        ("reversed    ", worst_first)):
        kept, _, _ = build(INSTRUCTION, QUESTION, order, 300)
        print(f"    {name}: {', '.join(p['id'] for p in kept)}")

    print("\n  look at what 'as retrieved' actually kept: #0 and")
    print("  #2, not #0 and #1. The loop takes whatever FITS in")
    print("  the room left, and #1 is a full-length chunk while")
    print("  #2 is the short tail of its document:")
    for pid in ("refunds.pdf#1", "refunds.pdf#2"):
        r = next(x for x in rs if x["id"] == pid)
        print(f"    {pid}: block of {len(pid) + len(r['text']) + 4}"
              f" chars")
    print("  So a greedy fill silently promotes short passages over")
    print("  the ones ranked above them - and #1 is the neighbour")
    print("  that holds the rest of the refund answer. The budget")
    print("  dropped exactly the passage the expansion was for.\n")

    print("  and the arithmetic has a floor. Try a budget that")
    print("  cannot hold the instruction:")
    try:
        build(INSTRUCTION, QUESTION, rs, 100)
    except ValueError as e:
        print(f"    ValueError: {e}")
    print("  Worth refusing rather than silently truncating: a")
    print("  context with the passages and no instruction is a")
    print("  different request from the one you meant to send.")
```

```text
  instruction 127 chars, question 28 chars
  6 candidate passages, about 60 chars each

  how many passages fit, by budget:
  budget   kept   dropped   room left
     200      1         5          11
     300      2         4           5
     500      5         1          16
     700      6         0         138

  at 300 the context holds two passages. Which two is
  decided by the order you hand them over in, and that
  order is yours to choose, not the retriever's:

    as retrieved: refunds.pdf#0, refunds.pdf#2
    reversed    : shipping.pdf#2, shipping.pdf#1

  look at what 'as retrieved' actually kept: #0 and
  #2, not #0 and #1. The loop takes whatever FITS in
  the room left, and #1 is a full-length chunk while
  #2 is the short tail of its document:
    refunds.pdf#1: block of 77 chars
    refunds.pdf#2: block of 63 chars
  So a greedy fill silently promotes short passages over
  the ones ranked above them - and #1 is the neighbour
  that holds the rest of the refund answer. The budget
  dropped exactly the passage the expansion was for.

  and the arithmetic has a floor. Try a budget that
  cannot hold the instruction:
    ValueError: no room for the instruction and the question
  Worth refusing rather than silently truncating: a
  context with the passages and no instruction is a
  different request from the one you meant to send.
```

**Two numbers, and keeping them apart is the point.** Chapter 26 left this chapter a question —
how many candidates to keep — and it is easy to answer the wrong one, so here are both.

The candidate set is Chapter 26's unit: what the cheap first stage hands the reranker, say the
top hundred. **Sizing it is a trade, and here it is.** Raising it can only help recall, because
the candidate set is a ceiling the reranker cannot raise and a larger set never contains less.
What it costs is one cross-encoder pass per candidate — Chapter 26's two-stage cost is one
embedding, one search and a hundred cross-encoder passes, and the hundred is this number. So
the cost is linear in the size and the benefit is whatever recall the extra candidates add,
which flattens: the fiftieth candidate is far less likely to be the answer than the fifth.

**So raise it until recall stops moving, and read Chapter 26's warning while you do.** A low
recall at your chosen size does not automatically mean *make it bigger*; Chapter 26 says the
money may belong in the first stage instead — a better embedding model, or lexical retrieval
alongside it — because a first stage that ranks the answer two-hundredth will need a candidate
set you cannot afford to cross-encode.

**What the size is emphatically not set by is what will fit in a context window.** That would
cap recall at whatever the budget below happens to allow, which is the mistake Chapter 26
derives against: the candidate set is the ceiling, and the context is a separate, smaller
selection taken after the reranking.

The **context budget** is this chapter's, and it is what survives the reranker into the request.
It is arithmetic: the instruction and the question take 155 characters of whatever budget you
have, every passage after that takes its own length plus its label, and at a budget of 300 you
get two passages and five characters to spare. It falls out of a quantity Chapter 16 owns — the
model's context window — rather than out of anything about retrieval.

**So the pipeline has four stages whose sizes shrink.** Everything, then the candidate set, then
that set reordered, then whatever the budget admits:

| Stage | How many | What sets it |
|---|---|---|
| First-stage retrieval | the whole index | Chapter 27's chunking |
| Candidate set | about a hundred | recall at that size, Chapter 26 |
| Reranked order | the same hundred, resorted | the cross-encoder, Chapter 26 |
| The context | two, here | the budget arithmetic above |

**Reranking is the third row**, and what this chapter adds to Chapter 26's
account of it is the thing that happens next: a reranker produces an *order*, and context
assembly can destroy it. That is not a hypothetical — it is the next paragraph.

**Two things in that output are worth more than the table.**

The first is the **greedy fill**. The loop keeps any passage that fits in the room left, so when
`refunds.pdf#1` is too big it is skipped and the shorter `refunds.pdf#2` is taken instead. The
result is `#0` and `#2`: the second passage in the context is not the second-ranked passage, it
is the highest-ranked one that *happened to be short*. Nothing announces this.

**And notice whose work this would throw away.** The rows here arrive in index order — the
program's own label for it is *as retrieved* — but put a reranker in front of them, which is
the arrangement Chapter 26 spends its second half on, and that order is the output of a
cross-encoder pass over every candidate, bought precisely to get the ordering right. Context
assembly then reorders it by length, for free, silently. That is what reranking looks like as a *step*: its output is an order, and the
step after it can undo that order without anybody deciding to. A reranked list fed to a greedy
fill is two stages disagreeing, and the cheap one wins.

And `refunds.pdf#1` is precisely the row that holds the rest of the refund answer. **The budget
dropped the one passage the next section is about.**

The second is the refusal. A budget too small for the instruction raises rather than truncating,
because a context carrying passages and no instruction is a different request from the one you
meant to send — and it will come back with a plausible answer, so nothing downstream will tell
you.

> **Note:** Budgets here are in characters so they can be counted by hand. In practice they are
> in Chapter 10's tokens, against the model's context window, which Chapter 16 owns and which is
> a dated detail — the figures move. What does not move is the shape: a fixed total, a fixed cost
> for the instruction, and whatever is left divided among passages.

## Rebuilding What the Cuts Split

Chapter 27 showed an answer cut in half by a chunk boundary and said that putting it back was
this chapter's job. Here it is.

```python
"""Chapter 27 split an answer across two rows. Here is the repair."""
from store import DOCS, rows

ANSWER = "A refund is issued to the original payment method within 14 days."

def retrieve(query_terms, rs, k=1):
    """Stand-in for chapters 24 to 26: score by matched terms, take top k.
    The ranking is not the point here; what happens next is."""
    scored = []
    for r in rs:
        hits = sum(1 for t in query_terms if t in r["text"].lower())
        scored.append((hits, r))
    scored.sort(key=lambda p: -p[0])
    return [r for hits, r in scored[:k] if hits]

def expand(row, rs, before=0, after=1):
    """Every row adjacent to this one in the SAME document, by offset.
    This is what chapter 27's stored offset was for."""
    same = sorted([r for r in rs if r["doc"] == row["doc"]],
                  key=lambda r: r["start"])
    i = same.index(row)
    lo, hi = max(0, i - before), min(len(same), i + after + 1)
    return same[lo:hi]

def joined(group):
    return "".join(r["text"] for r in group)

if __name__ == "__main__":
    rs = rows()
    got = retrieve(["refund", "how long"], rs, k=1)
    top = got[0]
    print(f"  retrieved: {top['id']}")
    snippet = top["text"][:52]
    print(f"    {snippet!r}")
    print(f"  holds the whole answer? {ANSWER in top['text']}")
    print("  It says a refund is issued and never says when.\n")

    group = expand(top, rs, before=0, after=1)
    print(f"  expanded to its neighbour: "
          f"{', '.join(r['id'] for r in group)}")
    print(f"  holds the whole answer? {ANSWER in joined(group)}")
    print(f"    {joined(group)[:56]!r}\n")

    print("  what the expansion cost:")
    print(f"    characters to the model: {len(top['text'])}"
          f" -> {len(joined(group))}")
    print(f"    rows spent on one hit: 1 -> {len(group)}\n")

    print("  and it only works because the row stored its offset.")
    print("  Adjacency is a fact about the ORIGINAL document, not")
    print("  about the index: sort these rows by score and they")
    print("  are in no particular order. Rebuild the neighbour")
    print("  from the offset, or you cannot rebuild it at all.\n")

    print("  the limit: expanding pulls in whatever is next, and")
    print("  what is next need not be relevant. Expand the other")
    print("  way round and you get this:")
    wrong = expand(rs[2], rs, before=1, after=0)
    print(f"    {', '.join(r['id'] for r in wrong)}")
    print(f"    {joined(wrong)[:56]!r}")
    print("  which is the tail of the refund rule welded to the")
    print("  head of the cancellation rule, at a boundary nobody")
    print("  chose for meaning. Expansion is cheap and blind.")
```

```text
  retrieved: refunds.pdf#0
    'Returns are handled by the support team. A refund is'
  holds the whole answer? False
  It says a refund is issued and never says when.

  expanded to its neighbour: refunds.pdf#0, refunds.pdf#1
  holds the whole answer? True
    'Returns are handled by the support team. A refund is iss'

  what the expansion cost:
    characters to the model: 60 -> 120
    rows spent on one hit: 1 -> 2

  and it only works because the row stored its offset.
  Adjacency is a fact about the ORIGINAL document, not
  about the index: sort these rows by score and they
  are in no particular order. Rebuild the neighbour
  from the offset, or you cannot rebuild it at all.

  the limit: expanding pulls in whatever is next, and
  what is next need not be relevant. Expand the other
  way round and you get this:
    refunds.pdf#1, refunds.pdf#2
    'to the original payment method within 14 days. A cancell'
  which is the tail of the refund rule welded to the
  head of the cancellation rule, at a boundary nobody
  chose for meaning. Expansion is cheap and blind.
```

**Neighbour expansion** is fetching the rows adjacent to a retrieved row in the original
document and handing all of them over together. It is the cheapest repair for a bad cut and it
is worth understanding exactly what makes it possible.

**A locator is doing all the work, and this is the derivation.** Adjacency is a property of the
original document. An index sorted by score has no notion of it — the rows come back in whatever
order the scores put them. So unless each row recorded *something* that places it in its
document, the neighbour is not merely hard to find, it is not identifiable at all.

**It need not be the offset, and the chapter's own rows show why that matters.** The ids here
are built as `name#n`, so the ordinal is already in the id and `expand` could sort on that
instead. Where the original documents are kept and the chunk text is verbatim, the offset is
recoverable by searching the document for the text — which is exactly what the citation checker
does three sections from here. What cannot be recovered is a position that was never recorded in
*any* form, by a store that kept only the text. Chapter 27 stored an offset and called it
citation metadata; this is its other job, and the general rule is that the locator is the thing
you cannot add later.

**It also costs, in the one currency the last section measured.** Two rows instead of one, 120
characters instead of 60. Expanding every hit by one neighbour halves the number of hits you can
afford, which is why the budget arithmetic and the expansion decision are the same decision
rather than two.

**And it is blind.** The program's last block expands a different row and gets the tail of the
refund rule welded to the head of the cancellation rule — a join at a boundary nobody chose for
meaning. Expansion does not know what a passage is about; it knows what was next to it.

## Order, and the Passage That Gets Ignored

Chapter 25's closing table listed one failure it could not place: the right passage retrieved and
still not used. That lands here, and the honest answer has two parts of very different strength.

**The part that is measured, and not by this chapter.** Chapter 16 records that models use long
inputs unevenly, states it as measured behaviour about particular models rather than a law of
the design, and warns explicitly against the slogan *models ignore the middle* — they do not
ignore it, they use it less reliably, and the size of the effect varies by model and by task.
Chapter 16 owns that finding. This chapter owns what follows from it, which is that **the order
of the passages is a decision you are making whether or not you know it.**

**The part that is yours.** Three things are in your hands and none of them is a default:

| Decision | What it is |
|---|---|
| How many passages | The budget arithmetic above, once the instruction is written |
| In what order | Yours. The retriever's ranking is one option, not an instruction |
| What the instruction asks for | Whether to answer only from the passages, whether to quote, and what to do when none of them answers |

The third is the one that changes the failure you get. An instruction that says *answer using
only the passages below* and *say so if none of them answers the question* gives the model
somewhere to go when retrieval has failed. Without that clause the alternatives are a refusal it
was not asked for or an answer from somewhere else, and Chapter 16 is the reason to expect the
second. **Asking for the quote and the id is what the next section is built on.**

> **Warning:** None of this makes the model use a passage. It is worth being blunt about that,
> because the opposite is a comfortable thing to believe. Placing a passage well and asking for
> a quote changes what you can *check*, not what the model does — and the whole value of the
> next section is that it turns an unverifiable hope into a failing test.

## A Citation a Reader Can Check

A **citation** is a pointer from something the reply says to the text it came from. **Attribution**
is the claim that this text supports that statement. The two are not the same, and almost
everything that goes wrong here lives in the gap.

```python
"""Checking a citation, and finding out what the check cannot see."""
from store import DOCS

# Five claims, each with a citation. One is sound; four are not, and
# between them they exercise every check below.
CITED = [
    {"claim": "A refund goes back to the card you paid with.",
     "doc": "refunds.pdf", "start": 41,
     "quote": "A refund is issued to the original payment method"},
    {"claim": "Refunds are paid within 7 days.",
     "doc": "refunds.pdf", "start": 40,
     "quote": "A refund is issued within 7 days"},
    {"claim": "Express delivery is next day.",
     "doc": "delivery.pdf", "start": 41,
     "quote": "Express delivery is next day"},
    {"claim": "Refunds carry a 10 per cent fee.",
     "doc": "refunds.pdf", "start": 137,
     "quote": "carries a fee of 10 per cent"},
    {"claim": "Standard delivery takes three working days.",
     "doc": "shipping.pdf", "start": 0,
     "quote": "takes three working days"},
]

def check(c):
    """Three things a program can decide, in order."""
    doc = DOCS.get(c["doc"])
    if doc is None:
        return "NO SUCH DOCUMENT"
    at = doc[c["start"]:c["start"] + len(c["quote"])]
    if at == c["quote"]:
        return "QUOTE IS AT THE OFFSET"
    if c["quote"] in doc:
        return f"QUOTE IS IN THE DOC, BUT AT {doc.index(c['quote'])}"
    return "QUOTE IS NOT IN THE DOCUMENT"

if __name__ == "__main__":
    for i, c in enumerate(CITED, 1):
        print(f"  {i}. {c['claim']}")
        print(f"     cites {c['doc']} at {c['start']}")
        print(f"     -> {check(c)}")
    print()
    print("  1 passes every check a program can run.")
    print("  2 fails: the quote is a plausible edit of the real")
    print("    sentence and appears nowhere in the document.")
    print("  3 fails: there is no such document. The quote is")
    print("    real text from shipping.pdf under a filename the")
    print("    model invented.")
    print("  4 PASSES EVERY CHECK AND IS STILL WRONG.")
    print("  5 fails only the third check: the quote is real and")
    print("    in the right document, and the offset is wrong. A")
    print("    true claim with a citation you cannot follow.")
    print()
    print("  Look at 4. The quote is in the document, at exactly")
    print("  the offset claimed. Here it is in context:")
    doc = DOCS["refunds.pdf"]
    print(f"    {doc[109:166]!r}")
    print("  The fee belongs to a cancellation. The claim attaches")
    print("  it to a refund. Every mechanical check passes, because")
    print("  the quote is genuine - it is the ATTRIBUTION that is")
    print("  false, and no string comparison can see that.")
```

```text
  1. A refund goes back to the card you paid with.
     cites refunds.pdf at 41
     -> QUOTE IS AT THE OFFSET
  2. Refunds are paid within 7 days.
     cites refunds.pdf at 40
     -> QUOTE IS NOT IN THE DOCUMENT
  3. Express delivery is next day.
     cites delivery.pdf at 41
     -> NO SUCH DOCUMENT
  4. Refunds carry a 10 per cent fee.
     cites refunds.pdf at 137
     -> QUOTE IS AT THE OFFSET
  5. Standard delivery takes three working days.
     cites shipping.pdf at 0
     -> QUOTE IS IN THE DOC, BUT AT 18

  1 passes every check a program can run.
  2 fails: the quote is a plausible edit of the real
    sentence and appears nowhere in the document.
  3 fails: there is no such document. The quote is
    real text from shipping.pdf under a filename the
    model invented.
  4 PASSES EVERY CHECK AND IS STILL WRONG.
  5 fails only the third check: the quote is real and
    in the right document, and the offset is wrong. A
    true claim with a citation you cannot follow.

  Look at 4. The quote is in the document, at exactly
  the offset claimed. Here it is in context:
    'cancellation after dispatch carries a fee of 10 per cent.'
  The fee belongs to a cancellation. The claim attaches
  it to a refund. Every mechanical check passes, because
  the quote is genuine - it is the ATTRIBUTION that is
  false, and no string comparison can see that.
```

**Three checks are mechanical, and the output gives each of them a case.** Does the cited
document exist — case 3 fails it. Is the quoted text actually in it — case 2 fails it. Is it at
the offset claimed — case 5 fails that one alone, with a quote that is real, in the right
document, and eighteen characters from where the citation says.

Case 3 is worth a second look, because it shows why the first check earns its place rather than
being subsumed by the second. The quote there is *real text*, from `shipping.pdf`, presented
under a filename that does not exist — so a check that only looked for the quote somewhere in
the corpus would pass it. **And note what case 3 is not**: the claim is true and the text
supporting it is in the corpus. What is broken is the citation, not the grounding. That
distinction is the whole of the next three paragraphs.

**What makes these worth building is that they turn a hope into a test.** Before them, "the
reply cites its sources" is something you take on trust. After them it fails loudly on cases 2,
3 and 5, in your own code, without a human reading anything. Be exact about what has been
tested, though: these check the *citation* — that it points at real text in a real place — and
not whether the reply is grounded. Case 3 has a sound grounding and a broken citation; case 4,
below, has the reverse.

**And then case 4, which is the whole point of the section.** The quote is genuine. It is in the
right document. It is at exactly the offset claimed. Every mechanical check passes — and the fee
belongs to a cancellation, while the claim attaches it to a refund. The citation is sound and the
attribution is false.

**So here is the answer to what a citation must support.** Not that the quoted text exists, which
is what the checks establish, but that **the quoted text entails the statement it is attached
to** — and that is a judgement about meaning, which no string comparison reaches. The checks are
necessary and they are not sufficient. What they buy is a much smaller set of surviving
failures, and it is worth knowing its shape. The one this section is about is a real quote,
correctly located, attached to the wrong claim. Two others get through the same door: a
statement the reply made with *no* citation at all, which the checks never examine because they
only look at citations that exist; and a quote that genuinely entails the sentence it is
attached to while the next sentence in the document adds the exception that makes the reply
wrong. That is a much smaller
problem than the one you started with, and it is the one a person has to look at.

> **Tip:** The useful habit is to make the citation carry enough to be checked at all: a document
> id, an offset, and the quoted span. A citation that is only a filename gets you the first test
> and nothing else — you can confirm the document exists and learn nothing about whether it says
> what the reply claims — and a reply that quotes without saying where gets you the first two
> and not the third. Chapters 32 and 33 build on this when the question becomes how to watch it in
> production.

## Long Context or Retrieval

Now the question that gets asked most and answered worst. The honest reply is that these are not
alternatives, and the argument has a derivable half and an observed half.

**The derivable half is arithmetic, in two steps.**

First, a modest corpus does not fit. Chapter 16's window is 128,000 tokens. A hundred documents
of two thousand tokens each is 200,000 tokens, which is about 1.6 times the window — so at a
hundred documents, "put it all in" has already failed, and nothing about a better model changes
a count. Retrieval exists because selection is unavoidable past a size that arrives early.

Second, filling a window is not free. Chapter 15's key-value cache for its example model is
exactly 512 KiB per token, which is the figure to multiply by — its 3.91 GiB at 8,000 tokens is
that number rounded, and rounding it first and multiplying second gives 62.56 rather than the
right answer:

```{=latex}
\[ 512\ \text{KiB} \times 128{,}000 = 65{,}536{,}000\ \text{KiB} = 62.5\ \text{GiB} \]
```

**Against 13 GiB of weights for the same model**, and Chapter 15's own figures say what tens of
gigabytes of cache do to a batch.

**Do not carry the multiple out of here, though, because it does not survive its own
footnote.** Chapter 15's Note says real systems share one set of keys and values across several
heads, which divides this figure by the sharing ratio — and at a ratio of eight the 62.5 GiB
becomes 7.8, which is *less* than the 13 GiB of weights. So "the cache dwarfs the model" is an
artefact of the unshared arithmetic, and the claim that survives at any ratio is the weaker and
still useful one: filling a long window costs cache on the order of the weights themselves,
every sequence, where a short one costs almost nothing.
A **long context** — a model whose maximum input runs to many tens of thousands of tokens — is a
real capability, and it is not a cheap one.

**The observed half is Chapter 16's**, and it cuts the other way from the obvious conclusion:
more in the window does not reliably mean more of it used. That is measured behaviour about
particular models, it varies by model and task, and it is why doubling the passages is not a
strategy. Putting less in and ordering it is the advice Chapter 16 itself gives.

**So what does a long window actually buy?** Three things, none of which is "stop retrieving".
It makes the budget arithmetic above less tight, so you can afford more passages and more
neighbour expansion. It lets a single large document be handed over whole — but that retires
only one of Chapter 27's two reasons for cutting a document up. The other is Chapter 27's
first — a document too long to embed as one vector — and a generation window does nothing about
that, because the
embedding model has its own input limit and Chapter 24's fixed width still has to hold whatever
you give it. And it removes the worst failures of a small window, where the
instruction and two passages were competing for room.

**And what it does not buy.** It does not remove the need to choose what goes in, because the
window is finite at any size and a corpus is not. It does not make selection free, because the
cache cost above is paid on every token you put in. And it does not make a long context better
*used* than a short one, which is the observed half above.

> **Tip:** The sentence to have ready is that they solve different problems. Retrieval answers
> *which text is relevant*, and a long window answers *how much relevant text you can afford to
> show*. A system with a huge window and no retrieval has no answer to the first question past a
> hundred documents; a system with retrieval and a tiny window keeps answering the first question
> well and then cannot act on it. Neither wins in general, and a real system uses both — the
> window to be generous, the retrieval to be selective.

## What To Actually Do

1. **Write the instruction before anything else**, including what to do when no passage answers. It is a fixed
   cost against your budget and it is the thing a greedy fill must never displace.
2. **Do the budget arithmetic.** Instruction plus question plus the passages you intend, against
   the window. If it does not fit, that is a number, not a feeling.
3. **Decide the order of the passages deliberately**, knowing from Chapter 16 that position matters unevenly and
   that the retriever's ranking is one option rather than an instruction.
4. **Fill by rank, not greedily**, or know that you are promoting short passages. If a passage
   does not fit, stop rather than skipping to the next one that does.
5. **Expand to neighbours where the cuts are bad**, and count the cost: each expansion halves
   how many hits you can afford.
6. **Require a citation with a document id, an offset and the quoted span**, and check all three
   mechanically on every reply.
7. **Read the survivors.** Three things get past the checks — a real quote attached to the wrong
   claim, a statement the reply never cited at all, and a quote that entails its sentence while
   the document's next sentence adds the exception — so a sample of passing replies still needs
   a person. Chapters 32 and 33 are how that
   becomes a system rather than a habit.

> **Warning:** Steps 6 and 7 are where this chapter's problem actually gets solved. *I can't
> prove where it came from* is not fixed by better retrieval or a longer window; it is fixed by
> requiring a checkable citation and then checking it. Everything above step 6 improves the odds.
> Only step 6 produces evidence.

## Lab: Assemble, Expand, and Check

Four programs, pure Python, nothing to install. About forty minutes, and there is a key for
every step. Work in a new empty folder.

**Step 1.** Save the first program as `store.py` and run it.

*Expected result:* six rows across two documents. Note that `refunds.pdf#0` ends mid-sentence —
that is Chapter 27's bad cut, kept on purpose.

**Step 2.** Save the second as `assemble.py` and run it.

*Expected result:* the budget table, and the two-passage context at 300 containing `#0` and
`#2`. Before reading on, work out why `#1` is missing.

**Step 3.** The answer is in the block below the table: `#1`'s block is 77 characters and `#2`'s
is 63, and only 68 were left. Now fix it — change the loop so that it *stops* at the first
passage that does not fit instead of skipping it.

*Expected result:* at budget 300 you now get `refunds.pdf#0` alone, with *68* characters of
room left where the greedy version had 5. You have traded a passage for the guarantee that the
context is the top of the ranking rather than a subset chosen by length — and you are now leaving
68 characters unused, which is the honest cost of stopping. Both behaviours are defensible; what
is not defensible is not knowing which one you have.

**Step 4.** Set the budget to `150` and run it.

*Expected result:* `ValueError: no room for the instruction and the question`. Then ask yourself
what the program would have done if `build` had truncated instead, and how you would have found
out.

**Step 5.** Save the third program as `neighbours.py` and run it.

*Expected result:* `refunds.pdf#0` retrieved, not holding the answer; expanded to `#0, #1`,
holding it; 60 characters becoming 120.

**Step 6.** In `neighbours.py`, call `expand(top, rs, before=1, after=1)` instead.

*Expected result:* the same two rows, because `#0` is the first row of its document and there is
nothing before it — `max(0, i - before)` clamps. Worth seeing: the function does not fail at a
document boundary, it just returns less than you asked for, which is the behaviour you want and
the kind of thing to check rather than assume.

**Step 7.** Now combine steps 2 and 5. In `assemble.py`, import `expand` and pass
`expand(rs[0], rs)` as the passages at budget 300.

*Expected result:* they do *not* both fit. 155 characters of instruction and question, plus
two blocks of 77, is 309 against a budget of 300 — so `refunds.pdf#1` is dropped and you are
back to a single passage that does not hold the answer. Nine characters decided it. **The
expansion and the budget are one decision**, which is the point of step 5 of the method.

**Step 8.** Save the fourth program as `cite.py` and run it.

*Expected result:* the five verdicts above. Then, before reading the explanation, work out for
yourself why case 4 is wrong — and why case 5 fails a different check from case 2.

**Step 9.** In `cite.py`, add a sixth entry: the same document, offset and quote as case 4, but
with the claim *"A cancellation after dispatch carries a fee."*

*Expected result:* an identical verdict — `QUOTE IS AT THE OFFSET` — for a claim that is now
true. **The check cannot tell your sixth case from case 4**, and they are opposites: one
attributes the fee to a cancellation and the other to a refund. That is the exact boundary of
what a mechanical citation check buys.

**Step 10.** Write down, for your own data, what a citation would have to carry to be checkable
at all. Then check whether the replies you are getting now carry it.

*Expected result:* a document id, an offset or some other locator, and the quoted span. Most
systems emit the first and call it a citation, which buys the first test and neither of the
others.

## Summary, Key Terms, and Review Questions

### Summary

**Context assembly** is turning retrieved rows, an instruction and a question into the request
the model is given — spread across Chapter 18's message list, and counting against one
window — and it is made of decisions rather than defaults. **What fits is
arithmetic**, and it is the step that comes after reranking rather than a part of it: an
instruction of 127 characters and a question of 28 take 155 of any budget, and
each passage takes its length plus its label — so Chapter 26's unanswered question, how many
candidates to keep, is about the candidate set and not the context: raise it until recall stops
moving, at one cross-encoder pass per candidate, and heed Chapter 26's warning that a low recall
may mean a better first stage rather than a bigger set. The **context budget** is a second and
smaller number, taken after the reranking, and set by this calculation against the window
Chapter 16 owns. The arithmetic gives a ceiling on how many passages fit, never a
judgement about how many help. Two things
in that calculation matter more than the count. A **greedy fill** keeps whatever fits in the
room left, so at a budget of 300 the context held `#0` and `#2` rather than `#0` and `#1`:
the second passage was not the second-ranked one but the highest-ranked *short* one, and `#1`
was the row holding the rest of the answer. And a budget too small for the instruction should
raise rather than truncate, because a context with passages and no instruction is a different
request and will come back with a plausible answer.

**Neighbour expansion** repairs Chapter 27's split answer: fetch the rows adjacent in the
original document and hand them over together, and 60 characters become 120 while the answer
becomes whole. **A recorded locator is what makes it possible, and that is a derivation** — adjacency is
a property of the document, an index sorted by score has no notion of it, so a row that recorded
no locator at all has a neighbour that is not merely hard to find but unidentifiable. The
locator need not be an offset — this chapter's ids carry the ordinal, and a kept document can be
searched for the text — but something has to place the row, and that is the part you cannot add
afterwards.
Expansion is also cheap and blind: expand the wrong way and you get the tail of the refund rule
welded to the head of the cancellation rule.

**Order is a decision, and the finding under it is Chapter 16's**: models use long inputs
unevenly, which is measured behaviour about particular models, varies by model and task, and is
not "models ignore the middle". What this chapter owns is that three things are yours — how many
passages, in what order, and what the instruction asks for — and that none of them makes the
model use a passage. Placing it well changes what you can check, not what happens.

**A citation points at text; attribution claims that text supports a statement.** Three checks
are mechanical: does the document exist, is the quote in it, is it at the offset claimed. Each
catches a different failure, and one case shows why the first matters alone — a real quote from
one document under a filename that does not exist. **But a citation can pass all three and still
be wrong**: the chapter's fourth case quotes genuine text at the exact offset claimed, and
attaches a cancellation fee to a refund. So what a citation must support is not that the quote
exists but that **the quote entails the statement**, which is a judgement no string comparison
reaches. The checks are necessary, not sufficient; what they buy is a much smaller set of
survivors — the wrong-claim one, a statement cited nowhere at all, and a quote undone by the
document's next sentence — and a person has to read a sample.

**Long context and retrieval are not alternatives.** The derivable half is arithmetic: a hundred
documents of two thousand tokens is 200,000 tokens against Chapter 16's 128,000-token window,
about 1.6 times over, so selection becomes unavoidable early; and filling that window costs
`\(512\ \text{KiB} \times 128{,}000 = 62.5\)`{=latex} GiB of key-value cache on Chapter 15's
example model, against 13 GiB of weights. The observed half is Chapter 16's, and it cuts against the obvious
conclusion: more in the window is not reliably more used. A long window buys a looser budget, a
large document handled whole, and the removal of the worst small-window failures. It does not buy
an end to choosing, because a window is finite at any size and a corpus is not. **They answer
different questions** — retrieval which text is relevant, the window how much of it you can
afford to show.

### Key Terms

| Term | Meaning |
|---|---|
| **Context assembly** | Turning retrieved passages, an instruction and a question into the request the model is given — spread across Chapter 18's message list, and counting against one window |
| **Context budget** | How much of the window is left for passages once the instruction and the question are counted. Not the same number as Chapter 26's candidate set, and set by a different thing |
| **Greedy fill** | Keeping any passage that fits in the room remaining. Silently promotes short passages over higher-ranked long ones |
| **Neighbour expansion** | Fetching the rows adjacent to a retrieved row in the original document and supplying them together. Needs some recorded locator — an offset, or an ordinal in the id; costs budget; does not know what is relevant |
| **Citation** | A pointer from something a reply says to the text it came from. Checkable only if it carries a document id, a locator and the quoted span |
| **Attribution** | The claim that the cited text supports the statement it is attached to. No string comparison reaches it; Chapters 32 and 33 are where it gets checked by other means |
| **Long context** | A large maximum input. Buys a looser budget and whole documents; does not remove the need to select, and is not free |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The budget arithmetic | Instruction + question are a fixed cost; each passage costs its length plus its label; the rest is the window, which Chapter 16 owns |
| Why a greedy fill is a trap | It keeps whatever fits, so the context becomes the highest-ranked *short* passages rather than the top of the ranking — undoing a reranker's ordering, for free, with nothing announcing it |
| What to do with too small a budget | Raise, do not truncate. A context without its instruction is a different request and still returns a plausible answer |
| Why neighbour expansion needs a locator | A derivation: adjacency is a property of the document and an index sorted by score has no notion of it. An offset, or an ordinal in the id — but something, recorded at index time |
| What an expansion costs | Each neighbour halves how many separate hits the budget can hold |
| The three mechanical citation checks | Does the document exist; is the quote in it; is it at the offset claimed |
| What a citation must support | That the quote *entails* the statement. The three checks are necessary and not sufficient |
| What still gets past all three | A real quote attached to the wrong claim; a statement with no citation at all, which the checks never look at; and a quote undone by the document's next sentence |
| Why a corpus outgrows a window | 100 documents × 2,000 tokens = 200,000, about 1.6× a 128,000-token window |
| What filling a window costs | Chapter 15's cache is 512 KiB per token, so 128,000 tokens is 62.5 GiB, against 13 GiB of weights. Multiply the per-token figure, not its rounded total — and divide by the head-sharing ratio before quoting any multiple |
| Long context against retrieval | Different questions: which text is relevant, and how much you can afford to show. Neither replaces the other |

### Review Questions

1. Long context or retrieval?
2. What must a citation actually support, and how would you check that it does?
3. You expand every retrieved passage to its neighbours and your answers get worse. Why might that be?
4. How many passages should go in the context?
5. Your replies cite documents and the citations look fine. What have you established?

### Review Answers

1. They are not alternatives, and the way to show that is to split the question. **The arithmetic
is derivable.** A hundred documents of two thousand tokens each is 200,000 tokens, about 1.6
times a 128,000-token window, so selection becomes unavoidable at a corpus size that arrives
early and no better model changes a count. And filling a window is not free: on Chapter 15's
example model the key-value cache is 512 KiB per token, so 128,000 tokens is 62.5 GiB, against
13 GiB of weights, paid on every token you put in. Resist the tempting multiple: Chapter 15
notes that real systems share one set of keys and values across several heads, and at a sharing
ratio of eight the 62.5 GiB becomes 7.8, below the weights rather than five times them. What
survives at any ratio is that a full window costs cache on the order of the model itself, every
sequence, where a short one costs almost nothing. **The quality half is measured, and it is Chapter 16's**, not mine to
assert: models use long inputs unevenly, it varies by model and task, and it is why doubling the
passages is not a strategy. So what a long window actually buys is a looser budget, a large
document handled whole, and the end of the worst small-window failures where the instruction and
two passages competed for room. What it does not buy is an end to choosing, because a window is
finite at any size and a corpus is not. Finish with the formulation: retrieval answers *which
text is relevant*, a long window answers *how much relevant text you can afford to show*, and a
real system uses the window to be generous and retrieval to be selective.
2. It must support that **the quoted text entails the statement it is attached to** — and the
reason that is the right answer is that the things a program *can* check are all weaker than it.
Three of them are mechanical and all three are worth running: does the cited document exist, is
the quoted text actually in it, and is it at the offset claimed. Each catches a different
failure, and the chapter gives each one a case. The second fails the middle check, with a quote
that is a plausible edit of the real sentence and appears nowhere. The fifth fails the third
alone — a real quote, in the right document, eighteen characters from where the citation says —
which is a true claim with a pointer you cannot follow. And the third case fails the first, which
shows why that test earns its place on its own: the quote is *real text* from another document,
presented under a filename
that does not exist, so a check that merely looked for the quote somewhere in the corpus would
pass it. Then the case that matters: the fourth quotes genuine text, in the right document, at
exactly the offset claimed, and attaches a cancellation fee to a refund. Every mechanical check
passes and the citation is still wrong, because what is false is the attribution rather than the
quote. So the checks are **necessary and not sufficient**, and what they buy is worth saying
precisely: after all three pass the survivors are few and nameable — a real quote attached to the
wrong claim, a statement the reply cited nowhere at all (the checks only examine citations that
exist), and a quote that entails its own sentence while the document's next sentence adds the
exception that makes the reply wrong. That is a much smaller problem than the one you started
with, and it is the one a person still has to read a sample of. The practical half of the answer is that
a citation has to *carry* enough to be checked: an id, a locator and the span. Most systems emit
a filename and call it a citation, which buys the first test — the document exists — and
neither of the others, so it tells you nothing about whether the document says what the reply
claims.
3. Several reasons, and they are worth separating because they suggest different fixes. The first
is the budget: each expansion costs the neighbour's length, so expanding every hit by one
neighbour halves how many separate hits you can afford. If the answer needed two different
documents and you spent the room on neighbours of the first, you have traded breadth for depth
without deciding to. The chapter's own numbers show it — 60 characters become 120, and at a
budget of 300 that is the difference between two passages and one. The second is that expansion
is **blind**: it fetches what was adjacent, not what is relevant, so expanding the wrong way
round in the chapter gives the tail of the refund rule welded to the head of the cancellation
rule, which is a passage that now contains a fee and a refund a few words apart. That is exactly
the shape Chapter 27 warned about for a bad parse, arriving by a different route. The third is
Chapter 16's: more text in the window is not reliably more text used, so the neighbour you added
may be diluting rather than helping. The check to run is Chapter 26's measures with and without
expansion on the same queries, paired, with an interval — Chapter 20 — because this is precisely
the sort of change that feels like an improvement and is a measurement.
4. It is arithmetic once you have written the instruction, which is why the instruction comes
first. The instruction and the question are a fixed cost — 155 characters in the chapter's
example — and each passage costs its own length plus its label, all against the model's window,
which Chapter 16 owns. So at a budget of 300 you get two passages, and the number is a
calculation rather than a preference. Two things to add, because they are what the question is
really testing. **Fill by rank and stop**, or know that you are not: a greedy fill that skips a
passage too large and takes the next one that fits turns a ranking you may have paid a reranker
for into the highest-ranked *short* passages, and in the chapter it dropped exactly the neighbour holding the
rest of the answer. And **the expansion decision is the same decision**: every neighbour you add
is a passage you cannot. Then the honest limit: the arithmetic tells you what fits, not what
helps. Whether five passages beat two on your data is Chapter 26's measures and Chapter 20's
interval, and Chapter 16 is the reason not to assume more is better.
5. That the citations are *checkable*, and nothing yet about whether they are right — and the
distinction is the answer. If they carry a document id, a locator and a quoted span, then three
tests can run: the document exists, the quote is in it, the quote is where it says. Passing those
establishes that the reply is pointing at real text in a real place, which rules out two failures
worth ruling out: the fabricated filename and the plausibly-edited quote. **It does not establish
that the quoted text supports the claim**, which is the attribution and is a judgement about
meaning no comparison reaches. So what you have established is a floor, and what gets past it has
a few nameable shapes: a genuine quote attached to the wrong statement, a claim the reply never
cited at all, and a quote undone by the sentence after it in the document. The next step follows
from those shapes: sample the *passing* replies and have somebody read the quote
against the claim, because the failures that survive your checks are invisible to them by
construction. And if the citations do not carry an id, a locator and a span, you have established
nothing at all, because none of the three tests can run — "it cited a document" is not a check.

> **You understand this when** you can say why a citation that passes every mechanical check can
> still be wrong, and name the one decision that the budget arithmetic and the neighbour
> expansion both turn out to be.
