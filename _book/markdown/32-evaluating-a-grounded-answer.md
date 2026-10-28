# Evaluating a Grounded Answer

Chapter 30 gave you named failure modes, and Chapter 31 gave you checks and a way to find out
whether a judge can be trusted. Both of them were about an *answer*. A grounded answer has two
halves — the passages that reached the model and what the model did with them — and a single
verdict on the answer cannot tell you which half failed. This chapter measures them apart. It
also builds the claim-level check Chapter 31 kept pointing at, separates being grounded from
answering the question, and says where your labelled cases come from in the first place.

*The problem.* The passages were right and the answer was still wrong. I don't know which half
to fix.

*The question.* How do you measure a grounded answer so that the number tells you where to work?

## One Number, Two Stages

Score forty cases end to end and you get one figure. Score the same forty twice — once asking
whether the retrieved passages contained an answer at all, once asking whether the answer was
right — and you get four.

```python
"""Forty cases, scored twice: once for retrieval, once for the answer.

Each row records two verdicts a person made while reading the case.
`R` is whether the retrieved passages contained an answer to the
question at all. `A` is whether the answer the system gave was right.
Y is yes, N is no.

The rows are written out, so every count below can be had by hand.
"""

#     R  A   how many cases of this shape
SHAPES = [
    ("Y", "Y", 22),   # retrieval found it, answer right
    ("Y", "N",  8),   # retrieval found it, answer wrong
    ("N", "N",  7),   # retrieval missed it, answer wrong
    ("N", "Y",  3),   # retrieval missed it, answer right anyway
]

CASES = [(r, a) for r, a, n in SHAPES for _ in range(n)]
N = len(CASES)

def count(r, a):
    return sum(1 for cr, ca in CASES if cr == r and ca == a)

if __name__ == "__main__":
    assert N == sum(n for _, _, n in SHAPES) == 40
    right = count("Y", "Y") + count("N", "Y")
    found = count("Y", "Y") + count("Y", "N")
    print(f"  {N} cases.\n")
    print(f"  End-to-end: the answer was right on {right} of {N}"
          f"   {right/N:.1%}")
    print("  That is the number on the dashboard, and it is the")
    print("  only one most systems report.\n")

    print("                           right   wrong")
    for r, label in (("Y", "passages held an answer"),
                     ("N", "passages held none")):
        print(f"  {label:24s}{count(r, 'Y'):6d}{count(r, 'N'):8d}")

    print(f"\n  Retrieval put an answer in the context on"
          f" {found} of {N}   {found/N:.0%}")
    print(f"  Given that it did, the answer was right on"
          f" {count('Y','Y')} of {found}   {count('Y','Y')/found:.0%}\n")

    print("  Now the four cells, which is the whole point.\n")
    print(f"  {count('Y','Y'):2d}  fine.")
    print(f"  {count('Y','N'):2d}  the passages held an answer and the system")
    print("      still got it wrong. Finding MORE passages fixes")
    print("      none of these. Chapter 28's order, trimming and")
    print("      instruction are where this cell is worked on -")
    print("      and chapter 28 is blunt that those change what")
    print("      you can CHECK, not what the model does.")
    print(f"  {count('N','N'):2d}  the passages held no answer, so the answer")
    print("      was wrong. This is retrieval's, and a better")
    print("      prompt will not fix one of them.")
    print(f"  {count('N','Y'):2d}  the passages held no answer and the answer")
    print("      was RIGHT. The end-to-end number counts these as")
    print("      successes. They are not: the system cannot show")
    print("      where the answer came from, so it cannot be")
    print("      checked, and when the document changes nothing")
    print("      about this case will notice.\n")

    gen, ret = count("Y", "N"), count("N", "N")
    print(f"  {right} of {N} told you nothing about where to work.")
    print(f"  {gen} against {ret} says both, in almost equal measure -")
    print("  and the two have little in common.")
```

```text
  40 cases.

  End-to-end: the answer was right on 25 of 40   62.5%
  That is the number on the dashboard, and it is the
  only one most systems report.

                           right   wrong
  passages held an answer     22       8
  passages held none           3       7

  Retrieval put an answer in the context on 30 of 40   75%
  Given that it did, the answer was right on 22 of 30   73%

  Now the four cells, which is the whole point.

  22  fine.
   8  the passages held an answer and the system
      still got it wrong. Finding MORE passages fixes
      none of these. Chapter 28's order, trimming and
      instruction are where this cell is worked on -
      and chapter 28 is blunt that those change what
      you can CHECK, not what the model does.
   7  the passages held no answer, so the answer
      was wrong. This is retrieval's, and a better
      prompt will not fix one of them.
   3  the passages held no answer and the answer
      was RIGHT. The end-to-end number counts these as
      successes. They are not: the system cannot show
      where the answer came from, so it cannot be
      checked, and when the document changes nothing
      about this case will notice.

  25 of 40 told you nothing about where to work.
  8 against 7 says both, in almost equal measure -
  and the two have little in common.
```

**The four cells are the chapter's first claim and the easiest to act on.** Eight cases had an
answer sitting in the context and got it wrong: **finding more passages fixes none of them.**
Chapter 28 spends a section on exactly this cell — the right passage retrieved and still not used
— and its levers are the order of the passages, what gets trimmed and what the instruction asks
for — none of which changes whether the passage arrived. Chapter 28 is also blunt about what
those levers do: they change what you can *check*, not what the model does. Seven had no answer in the context: that is retrieval's, and a better
instruction will not fix one of them. Eight against seven says *both*, in almost equal measure,
and the single 62.5 per cent said nothing at all.

**The fourth cell is the one worth arguing about.** Three cases had no answer in the retrieved
passages and the system answered correctly anyway. The end-to-end figure counts those as
successes. They are not successes: the answer did not come from the passages, so nothing in the
system can show where it did come from, nobody can check it, and when the document changes the
answer will not change with it. **A right answer that no passage supports is a failure of a
grounded system**, because being grounded is the property you were building. One case needs care:
an answer *derived* from the passages — a total from a unit price in one and a quantity in another
— is traceable and does move when either document changes, so whether the passages "held an
answer" is a judgement you have to settle and write down before you score forty cases.

> **Note:** You need both verdicts per case, which means reading each case twice with a different
> question in mind. "Did the passages contain an answer?" is a judgement about the retrieved set
> and nothing else — not whether they were the *best* passages, which is Chapter 26's measures.
> "Was the answer right?" is Chapter 31's territory, with everything that chapter said about
> establishing a judge before believing it.

> **Tip:** Do the retrieval column first and on its own. It is the cheaper of the two to judge,
> because you are reading passages against a question rather than an answer against passages. The
> cases where retrieval failed can then be set aside for the *fix* work — but they still need an
> answer verdict, because that is the only place the fourth cell above comes from.

## Grounded, and What That Buys

An answer is **grounded** when every claim it makes is supported by a passage that was retrieved.
Chapter 28 put the principle in place for citations: a citation points at text, attribution
claims that text supports a statement, and what a citation must support is that the quote
*entails* the statement — a judgement no string comparison reaches. **Groundedness is that same
test applied to every claim in the answer rather than only to the ones carrying a citation**, and
the number it gives you is the share of claims a passage supports.

The word you will also hear is **faithfulness**, and for this purpose it means the same thing:
the answer is faithful to the passages it was given. It is worth knowing both, because an
interviewer may use either, and worth knowing that neither says anything about whether the
passages were right or whether the answer was useful.

The check that produces it is the **claim-level check** — the one Chapter 30 listed as *every
claim supported by a passage* and named the claim-support check, and which Chapter 31 files among
the checks that need a judgement: take the answer
apart into the claims it makes and give each one a verdict against the retrieved passages. Here it is on one answer, which is how
you see what the number costs and what it hides.

```python
"""One grounded answer, taken apart claim by claim.

Three retrieved passages, one question, one answer the system gave,
and the claim-by-claim verdicts a person recorded while reading it.
The verdicts are data, as chapter 31 requires: deciding whether a
passage entails a sentence is a judgement and no program here makes
one.
"""

PASSAGES = {
    "refunds.pdf":
        "Refunds are issued within 14 days of the returned item "
        "arriving at our warehouse. The customer pays return "
        "postage unless the item is faulty.",
    "shipping.pdf":
        "Standard delivery is 3 to 5 working days. Express "
        "delivery is next working day if ordered before 2pm.",
    "faq.html":
        "You can track a return in your account under Orders.",
}

QUESTION = ("How long does a refund take, and do I pay to send "
            "the item back?")

# The answer, as four sentences.
SENTENCES = [
    "Refunds are issued within 14 days of the returned item "
    "arriving at our warehouse, and you will get an email when "
    "it is processed.",
    "You pay return postage unless the item is faulty.",
    "Returns usually arrive at the warehouse in 3 to 5 working "
    "days, so expect about 18 days in total.",
    "You can track the return in your account.",
]

# (sentence index, the claim, supported by, note)
CLAIMS = [
    (0, "refunds are issued within 14 days of arrival at the "
        "warehouse", "refunds.pdf", ""),
    (0, "the customer will get an email when it is processed",
        None, "no passage mentions an email"),
    (1, "the customer pays return postage unless the item is "
        "faulty", "refunds.pdf", ""),
    (2, "returns arrive at the warehouse in 3 to 5 working days",
        None, "shipping.pdf gives 3 to 5 days for DELIVERY to the "
              "customer, which is the other direction"),
    (2, "a refund takes about 18 days in total", None,
        "arithmetic on top of the claim above, which nothing "
        "supports"),
    (3, "you can track the return in your account", "faq.html", ""),
]

def wrap(text, indent, hang=None):
    """Keep every printed line inside 64 characters."""
    hang = indent if hang is None else hang
    out, line = [], indent
    for word in text.split():
        if len(line) + len(word) + 1 > 64:
            out.append(line.rstrip())
            line = hang
        line += word + " "
    out.append(line.rstrip())
    return "\n".join(out)

if __name__ == "__main__":
    print(wrap("Question: " + QUESTION, "  ") + "\n")
    print(f"  {len(PASSAGES)} passages retrieved,"
          f" {len(SENTENCES)} sentences,"
          f" {len(CLAIMS)} claims in the answer.\n")

    supported = [c for c in CLAIMS if c[2]]
    print(f"  Claim by claim: {len(supported)} of {len(CLAIMS)}"
          f" supported   {len(supported)/len(CLAIMS):.0%}\n")
    for i, (_, claim, src, note) in enumerate(CLAIMS, 1):
        mark = "ok" if src else "NO"
        print(wrap(f"{mark} {i}. {claim}", "  ", "        "))
        if src:
            print(f"        from {src}")
        if note:
            print(wrap(note, "        "))

    print("\n  Now the same answer checked a sentence at a time,")
    print("  counting a sentence as supported if any claim in it is.")
    by_sentence = []
    for s in range(len(SENTENCES)):
        claims = [c for c in CLAIMS if c[0] == s]
        by_sentence.append(any(c[2] for c in claims))
    ok = sum(by_sentence)
    print(f"    {ok} of {len(SENTENCES)} sentences supported"
          f"   {ok/len(SENTENCES):.0%}")
    print(f"    {len(supported)} of {len(CLAIMS)} claims supported"
          f"      {len(supported)/len(CLAIMS):.0%}\n")

    print("  Same answer, same passages, two numbers 25 points")
    print("  apart. The coarser one is higher, and it is higher")
    print("  for a reason that has nothing to do with the answer:")
    print("  sentence 1 carries one supported claim and one")
    print("  invented one, and checking by sentence lets the first")
    print("  vouch for the second.\n")

    print("  And the claim that answers the question asked is")
    print("  claim 5, 'about 18 days in total'. It is unsupported,")
    print("  and it is built on claim 4, which reads a real passage")
    print("  as saying something it does not say. Note what it")
    print("  also does with units: refunds.pdf says 14 days and")
    print("  shipping.pdf says 3 to 5 WORKING days, so the sum is")
    print("  two kinds of day added together.")
    print("  This answer carries no citations at all. Had it")
    print("  cited refunds.pdf for the 14 days and shipping.pdf")
    print("  for the 3 to 5, BOTH citations would pass chapter")
    print("  28's three mechanical checks: the document exists,")
    print("  the quote is in it, at the offset claimed. What")
    print("  fails is the thing chapter 28 says those checks")
    print("  cannot reach - whether the quote entails the")
    print("  sentence it is attached to.")
```

```text
  Question: How long does a refund take, and do I pay to send
  the item back?

  3 passages retrieved, 4 sentences, 6 claims in the answer.

  Claim by claim: 3 of 6 supported   50%

  ok 1. refunds are issued within 14 days of arrival at the
        warehouse
        from refunds.pdf
  NO 2. the customer will get an email when it is processed
        no passage mentions an email
  ok 3. the customer pays return postage unless the item is
        faulty
        from refunds.pdf
  NO 4. returns arrive at the warehouse in 3 to 5 working days
        shipping.pdf gives 3 to 5 days for DELIVERY to the
        customer, which is the other direction
  NO 5. a refund takes about 18 days in total
        arithmetic on top of the claim above, which nothing
        supports
  ok 6. you can track the return in your account
        from faq.html

  Now the same answer checked a sentence at a time,
  counting a sentence as supported if any claim in it is.
    3 of 4 sentences supported   75%
    3 of 6 claims supported      50%

  Same answer, same passages, two numbers 25 points
  apart. The coarser one is higher, and it is higher
  for a reason that has nothing to do with the answer:
  sentence 1 carries one supported claim and one
  invented one, and checking by sentence lets the first
  vouch for the second.

  And the claim that answers the question asked is
  claim 5, 'about 18 days in total'. It is unsupported,
  and it is built on claim 4, which reads a real passage
  as saying something it does not say. Note what it
  also does with units: refunds.pdf says 14 days and
  shipping.pdf says 3 to 5 WORKING days, so the sum is
  two kinds of day added together.
  This answer carries no citations at all. Had it
  cited refunds.pdf for the 14 days and shipping.pdf
  for the 3 to 5, BOTH citations would pass chapter
  28's three mechanical checks: the document exists,
  the quote is in it, at the offset claimed. What
  fails is the thing chapter 28 says those checks
  cannot reach - whether the quote entails the
  sentence it is attached to.
```

**Start with the two figures, 75 per cent and 50 per cent, from the same answer and the same
passages.** The difference is entirely the unit: a sentence or a claim. Sentence 1 carries one
claim a passage supports and one claim nothing supports, and checking a sentence at a time lets
the first vouch for the second. Chapter 30 had the same lesson about a different table — a check
catches failures rather than modes — and it is the same mistake in a new place: **the unit you
count in is a claim about the thing you are measuring, and here the coarser unit flattered the
answer.**

**Then the finding that matters more than either figure.** The claim that answers the question
asked — *about 18 days in total* — is unsupported, and built on a claim that reads a real passage
as saying something it does not say. `shipping.pdf` gives three to five working days for delivery
*to* the customer; the answer used it for the return journey. Note what it also does with units:
`refunds.pdf` says 14 days and `shipping.pdf` says three to five *working* days, so the sum adds
two kinds of day together. **And the answer carries no citations at all** — it is four sentences
of prose. Had it cited `refunds.pdf` for the 14 days and `shipping.pdf` for the three to five,
**both citations would pass Chapter 28's three mechanical checks**: the document exists, the quote
is in it, it is at the offset claimed. What fails is exactly the thing Chapter 28 said those
checks cannot reach.

**And decomposing the answer into claims is itself a judgement.** Six claims is what one careful
reader found in four sentences; another reader might find five or seven, and the denominator
moves with them. That is not a reason to skip it — the per-claim verdicts are what tell you which
sentence to fix, which no aggregate does — but it means a groundedness figure is only comparable
against itself, by one person's decomposition rules, held still.

> **Warning:** Do not report a groundedness figure without saying what a claim was. Two teams
> reporting 80 per cent may be decomposing at a granularity two steps apart. It does not even run
> reliably one way: a sentence here counts as supported if any claim in it is, which let sentence
> 1 off and raised the coarse figure — but three supported claims in one sentence beside a single
> unsupported claim in another gives 75 per cent by claim and 50 by sentence, the other way about.

## Grounded Is Not Relevant

A groundedness figure has a failure mode of its own, and it is not subtle once you have seen it.

```python
"""Five answers to one question, scored on two axes.

The question has two parts: how long a refund takes, and who pays
return postage. For each answer: how many of its claims a passage
supports, and which parts of the question it answers. Both columns
are verdicts a person recorded.
"""
from claims import QUESTION, wrap

PARTS = ("how long", "who pays postage")

#  answer, (supported, total), parts answered
ANSWERS = [
    ("Refunds are issued within 14 days of the item arriving at "
     "our warehouse. You pay return postage unless the item is "
     "faulty.", (2, 2), ("how long", "who pays postage")),
    ("Standard delivery is 3 to 5 working days.", (1, 1), ()),
    ("A refund takes about 18 days in total.", (0, 1),
     ("how long",)),
    ("I do not have information about refund timing.", (0, 0), ()),
    ("Refunds are issued within 14 days of the item arriving at "
     "our warehouse.", (1, 1), ("how long",)),
]

def grounded(sup, tot):
    """The share of an answer's claims that a passage supports -
    and for an answer that makes NO claims, the honest answer is
    that the share does not exist. Printing 100% there is the
    single commonest way this measure is made useless."""
    return None if tot == 0 else sup / tot

if __name__ == "__main__":
    print(wrap("Question: " + QUESTION, "  "))
    print(f"  Its parts: {PARTS[0]}; {PARTS[1]}\n")

    print("  #  grounded      answers")
    for i, (text, (sup, tot), parts) in enumerate(ANSWERS, 1):
        g = grounded(sup, tot)
        gs = "no claims" if g is None else f"{sup} of {tot}  {g:4.0%}"
        print(f"  {i}  {gs:13s} {len(parts)} of {len(PARTS)} parts")
    print()
    for i, (text, _, _) in enumerate(ANSWERS, 1):
        print(wrap(f"{i}. {text}", "  ", "     "))

    print("\n  Answer 2 is grounded on every claim it makes and")
    print("  answers neither part of the question. It is a")
    print("  sentence copied out of a passage that was retrieved")
    print("  and is about something else. So a groundedness")
    print("  figure on its own ranks it level with answer 1.\n")

    print("  Answer 4 is the one that breaks a leaderboard, and")
    print("  it takes a decision to score at all. 'I do not have")
    print("  information' IS an assertion, and a false one, since")
    print("  refunds.pdf was retrieved and does give the timing.")
    print("  It is a claim about what the SYSTEM knows, though,")
    print("  not about the documents - so it decomposes to zero")
    print("  claims about the documents, which is the rule used")
    print("  here and exactly the kind of rule that has to be")
    print("  written down. Scored that way it makes no claims,")
    print("  so there is nothing to support and nothing to")
    print("  contradict. Score it 100% - which is what")
    print("  a share of supported claims does if you are not")
    print("  careful about zero - and refusing becomes the best")
    print("  strategy your metric knows. That is why this program")
    print("  prints 'no claims' instead of a number, and why a")
    print("  refusal detector belongs beside it.\n")

    print("  Answer 3 earns 1 of 2 parts while being the answer")
    print("  the chapter has just taken apart. That is correct:")
    print("  relevance asks whether a part of the question was")
    print("  ADDRESSED, not whether the answer to it was right.")
    print("  Correctness is a third verdict, and it is the one")
    print("  the first program's A column records.\n")
    print("  Answer 5 is grounded, true, and answers one part of")
    print("  a two-part question. Relevance is not a yes or no")
    print("  once the question has parts, and a system that")
    print("  reliably answers the first half of every question")
    print("  will look fine on any measure that asks only")
    print("  whether the answer is about the question.\n")

    full = [i for i, (_, _, p) in enumerate(ANSWERS, 1)
            if len(p) == len(PARTS)]
    clean = [i for i, (_, (s, t), _) in enumerate(ANSWERS, 1)
             if t and s == t]
    print(f"  Fully relevant: {full}.  Fully grounded: {clean}.")
    print("  The two columns pick out different answers, which is")
    print("  the whole reason for having both. Only answer 1 is in")
    print("  both lists, and no single number would have told you.")
```

```text
  Question: How long does a refund take, and do I pay to send
  the item back?
  Its parts: how long; who pays postage

  #  grounded      answers
  1  2 of 2  100%  2 of 2 parts
  2  1 of 1  100%  0 of 2 parts
  3  0 of 1    0%  1 of 2 parts
  4  no claims     0 of 2 parts
  5  1 of 1  100%  1 of 2 parts

  1. Refunds are issued within 14 days of the item arriving at
     our warehouse. You pay return postage unless the item is
     faulty.
  2. Standard delivery is 3 to 5 working days.
  3. A refund takes about 18 days in total.
  4. I do not have information about refund timing.
  5. Refunds are issued within 14 days of the item arriving at
     our warehouse.

  Answer 2 is grounded on every claim it makes and
  answers neither part of the question. It is a
  sentence copied out of a passage that was retrieved
  and is about something else. So a groundedness
  figure on its own ranks it level with answer 1.

  Answer 4 is the one that breaks a leaderboard, and
  it takes a decision to score at all. 'I do not have
  information' IS an assertion, and a false one, since
  refunds.pdf was retrieved and does give the timing.
  It is a claim about what the SYSTEM knows, though,
  not about the documents - so it decomposes to zero
  claims about the documents, which is the rule used
  here and exactly the kind of rule that has to be
  written down. Scored that way it makes no claims,
  so there is nothing to support and nothing to
  contradict. Score it 100% - which is what
  a share of supported claims does if you are not
  careful about zero - and refusing becomes the best
  strategy your metric knows. That is why this program
  prints 'no claims' instead of a number, and why a
  refusal detector belongs beside it.

  Answer 3 earns 1 of 2 parts while being the answer
  the chapter has just taken apart. That is correct:
  relevance asks whether a part of the question was
  ADDRESSED, not whether the answer to it was right.
  Correctness is a third verdict, and it is the one
  the first program's A column records.

  Answer 5 is grounded, true, and answers one part of
  a two-part question. Relevance is not a yes or no
  once the question has parts, and a system that
  reliably answers the first half of every question
  will look fine on any measure that asks only
  whether the answer is about the question.

  Fully relevant: [1].  Fully grounded: [1, 2, 5].
  The two columns pick out different answers, which is
  the whole reason for having both. Only answer 1 is in
  both lists, and no single number would have told you.
```

**Answer 2 is grounded on every claim it makes and answers neither part of the question.** It is
a sentence copied out of a passage that happened to be retrieved and is about something else.
Measured on groundedness alone it is level with answer 1, which is correct and complete. So the
second measure is not optional: **answer relevance**, which asks whether the answer addresses
what was asked, and which has nothing to do with whether its claims are supported.

**Answer 4 is the one that breaks a leaderboard, and scoring it takes a decision.** *I do not
have information about refund timing* is an assertion, and a false one, since `refunds.pdf` was
retrieved and does give the timing — it is Chapter 30's mode *Refuses when the answer is there*,
exactly. But it is a claim about what the *system* knows rather than about the documents, so
under the rule used here it decomposes to zero claims about the documents. **That rule is the
kind the Warning above says to write down**, and this is what writing it down looks like. Scored
that way, there is nothing to support and nothing to contradict. Score that 100 per cent — which is what a share of supported
claims does if you are careless about zero — and **refusing becomes the best strategy your metric
knows**. This is why the program prints *no claims* rather than a number, and why a refusal detector —
Chapter 30's, filed by Chapter 31 among the checks code can decide — belongs beside a
groundedness figure rather than after it.

**Answer 3 earns one part of two while being the answer this chapter has just taken apart**, and
that is correct: relevance asks whether a part of the question was *addressed*, not whether the
answer to it was right. Correctness is a third verdict, and it is the one the first program's `A`
column records.

**Answer 5 shows that relevance is not a yes or no.** The question has two parts and the answer
gives one of them, grounded and true. A system that reliably answers the first half of every
question will look fine on any measure that asks only whether the answer is about the question —
so decompose the *question* as well as the answer, and count parts.

> **Note:** Three measures, and each one answers a question the others cannot. Retrieval: was an
> answer there? Groundedness: is what the answer says supported by what was there? Relevance:
> does it answer what was asked? Groundedness can be high while relevance is low, which answer 2
> shows, and answer 3 is 0 per cent grounded while addressing one part, which is the reverse. The only answer in the five above that is
> fully grounded *and* fully relevant is answer 1 — which no single number would have picked out.

## Where the Forty Cases Come From

Everything above needs cases with verdicts on them, and Chapter 30 produced its forty by reading
real failures. That is the best source and it has a limit: you only get cases for the questions
somebody already asked. The other source is your own documents.

```python
"""Generating an evaluation set from your own documents, and the
trap in it.

Eight passages. For each, a question built by reusing the passage's
own words - which is what a generator does - and a question written
the way somebody would actually ask it. Retrieval is word overlap,
ignoring a short stopword list, which is enough to make the point
and is not pretending to be chapter 26's BM25.
"""
import re

PASSAGES = [
    "Refunds are issued within 14 days of the returned item "
    "arriving at our warehouse.",
    "The customer pays return postage unless the item is faulty.",
    "Standard delivery is 3 to 5 working days.",
    "Express delivery is next working day if ordered before 2pm.",
    "You can track a return in your account under Orders.",
    "Orders over 50 pounds qualify for free standard delivery.",
    "A cancelled order is refunded to the original payment method.",
    "Gift cards cannot be refunded or exchanged for cash.",
]

# What a generator produces: the passage's own words, turned round.
GENERATED = [
    "Within how many days are refunds issued after the returned "
    "item arrives at our warehouse?",
    "Who pays return postage unless the item is faulty?",
    "How many working days is standard delivery?",
    "When must an express delivery be ordered to arrive next "
    "working day?",
    "Where in your account can you track a return?",
    "Which orders qualify for free standard delivery?",
    "To what is a cancelled order refunded?",
    "Can gift cards be refunded or exchanged for cash?",
]

# How somebody asks, with no sight of the passage.
ASKED = [
    "I sent my parcel back last week, when do I see the money?",
    "Do I have to cover the cost of posting it back?",
    "How soon will it turn up?",
    "Can I get it tomorrow if I buy it this morning?",
    "How do I check what is happening with my return?",
    "Is postage free if I spend a bit more?",
    "I cancelled, where does the money go?",
    "Can I swap a voucher for cash?",
]

STOP = set("""a an and are as at be been before but by can cannot
day days do does for from have how i if in is it its me must my of
on or over see the their there to under was what when where which
who will with within you your""".split())

def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower())
            if w not in STOP}

def best(query):
    """The index of the single highest-overlap passage, or None when
    nothing overlaps at all. Returning an index on a top score of
    zero is how the first draft of this program counted a hit for a
    question that shares not one word with any passage: the tie went
    to the lowest index, which happened to be the right answer."""
    scores = [(len(words(query) & words(p)), -i)
              for i, p in enumerate(PASSAGES)]
    top = max(scores)
    return None if top[0] == 0 else -top[1]

def hits(queries):
    return [i for i, q in enumerate(queries) if best(q) == i]

if __name__ == "__main__":
    n = len(PASSAGES)
    g, a = hits(GENERATED), hits(ASKED)
    print(f"  {n} passages, and two sets of {n} questions about"
          f" them.\n")
    print(f"  Questions generated FROM the passages:")
    print(f"    right passage ranked first on {len(g)} of {n}"
          f"   {len(g)/n:.0%}")
    print(f"  The same questions as somebody would ask them:")
    print(f"    right passage ranked first on {len(a)} of {n}"
          f"   {len(a)/n:.0%}\n")

    print("  Same passages, same retrieval, same eight facts.")
    print(f"  The generated set says retrieval is perfect. The")
    print(f"  asked set says {len(a)} of {n}.\n")

    print("  The reason is in the overlap, not in the retrieval:")
    for i in range(n):
        og = len(words(GENERATED[i]) & words(PASSAGES[i]))
        oa = len(words(ASKED[i]) & words(PASSAGES[i]))
        mark = "" if i in a else "  <- missed"
        print(f"    passage {i}: {og} shared generated,"
              f" {oa} asked{mark}")
    print("\n  A generated question is made of the passage's own")
    print("  words, and this retriever matches words, so it found")
    print("  all eight. A generated question is not a question")
    print("  about your documents; it is a question about your")
    print("  vocabulary.\n")
    print("  How big the gap is depends on the retriever. The")
    print("  asked questions here are clean paraphrases sharing")
    print("  none or one word with their passages, which is the")
    print("  case chapter 24's embeddings exist to catch, so a")
    print("  dense retriever may well score above 2 of 8 here -")
    print("  and by how much is a measurement to make, not a")
    print("  prediction to publish. What does not depend on the")
    print("  retriever is where the generated questions came")
    print("  from: they were made from the passages.\n")

    print("  That does NOT make generation useless. It gives you")
    print("  two things nothing else does: an answer key you did")
    print("  not have to label, because you know which passage")
    print("  each question came from, and coverage, because you")
    print("  can generate one per passage and see which corners")
    print("  of your documents nobody has ever asked about.")
    print("  What it does not give you is a hard set.\n")

    print("  So use it, and then do the one thing that makes it")
    print("  honest: rewrite the questions away from the")
    print("  passage's wording, keeping the key. The asked set")
    print("  above is that rewrite, and the numbers either side")
    print("  of it are what the rewrite is worth.")
```

```text
  8 passages, and two sets of 8 questions about them.

  Questions generated FROM the passages:
    right passage ranked first on 8 of 8   100%
  The same questions as somebody would ask them:
    right passage ranked first on 2 of 8   25%

  Same passages, same retrieval, same eight facts.
  The generated set says retrieval is perfect. The
  asked set says 2 of 8.

  The reason is in the overlap, not in the retrieval:
    passage 0: 6 shared generated, 0 asked  <- missed
    passage 1: 6 shared generated, 0 asked  <- missed
    passage 2: 3 shared generated, 0 asked  <- missed
    passage 3: 5 shared generated, 0 asked  <- missed
    passage 4: 3 shared generated, 1 asked  <- missed
    passage 5: 5 shared generated, 1 asked  <- missed
    passage 6: 3 shared generated, 1 asked
    passage 7: 5 shared generated, 1 asked

  A generated question is made of the passage's own
  words, and this retriever matches words, so it found
  all eight. A generated question is not a question
  about your documents; it is a question about your
  vocabulary.

  How big the gap is depends on the retriever. The
  asked questions here are clean paraphrases sharing
  none or one word with their passages, which is the
  case chapter 24's embeddings exist to catch, so a
  dense retriever may well score above 2 of 8 here -
  and by how much is a measurement to make, not a
  prediction to publish. What does not depend on the
  retriever is where the generated questions came
  from: they were made from the passages.

  That does NOT make generation useless. It gives you
  two things nothing else does: an answer key you did
  not have to label, because you know which passage
  each question came from, and coverage, because you
  can generate one per passage and see which corners
  of your documents nobody has ever asked about.
  What it does not give you is a hard set.

  So use it, and then do the one thing that makes it
  honest: rewrite the questions away from the
  passage's wording, keeping the key. The asked set
  above is that rewrite, and the numbers either side
  of it are what the rewrite is worth.
```

**Generating a question from a passage gives you two things reading real failures does not.** An answer key
you did not have to label — you know which passage the question came from, because you made it
from that passage, which is Chapter 24's answer key arriving for free. And coverage: one question
per passage tells you which corners of your documents nobody has ever asked about, which reading
real failures can never tell you.

**What it does not give you is a hard set, and the gap is not small.** Retrieval ranks the right
passage first on all eight generated questions and on two of the eight asked ones. The mechanism
is printed beside the result: a generated question shares three to six words with its source
passage, and a real question shares none or one. **A question built from a passage is not a
question about your documents; it is a question about your vocabulary**, and a retriever that
matches words found all eight of them.

**So generate the set, and then do the one thing that makes it honest: rewrite the questions away
from the passage's wording and keep the key.** The rewrite is the work. It is also a part of this
that cannot be automated by the thing you are testing. What this set shows is narrower than the
rule people state: reusing a passage's words flatters a retriever that matches words. Carry the
wider version as a caution rather than a law — a set built by the mechanism under test may well
report that the mechanism works, and the way to find out is to measure the overlap.

> **Warning:** This is the most common way an evaluation set is quietly worthless, and it does
> not announce itself — the numbers are high, the set is large, and every case has a key. If your
> retrieval scores far better on your evaluation set than users report, look at the overlap
> between your questions and your passages before you look anywhere else.

## What To Actually Do

1. **Score every case twice over**, once for whether the retrieved passages held an answer and
   once for whether the answer was right. Two columns, not one.
2. **Read all four of the cells**, and read the right-answer-no-passage cell as a failure. It is the
   one the end-to-end number is lying to you about.
3. **Work on the larger of the two fault cells.** If they are comparable, as they are here, the
   two bodies of work are largely separate — finding passages on one side, Chapter 28's
   assembly and the generation side on the other.
4. **For the answers, decompose into claims** and give each one a verdict against the retrieved
   passages. Write down what you counted as a claim, and keep that rule still.
5. **Report the per-claim verdicts, not only the share.** The share tells you how bad; the
   verdicts tell you which sentence.
6. **Measure relevance as its own number**, and decompose the question when it has parts.
7. **Handle the no-claims answer explicitly.** A refusal has no unsupported claims, so any
   groundedness figure must either exclude it or be paired with a refusal detector.
8. **Build your set from both sources**: real failures for the questions people ask, generated
   questions for coverage and a free answer key.
9. **Rewrite every generated question away from its passage's wording.** Measure the overlap
   before and after if you want to know what the rewrite bought.
10. **Keep both sets apart.** The generated one is for coverage and the real one is for knowing
    how you are doing; averaging them gives a number that means neither.

> **Tip:** Steps 1 to 3 are an afternoon and they decide where a month goes. Everything after
> step 4 is the expensive part, so do them in this order rather than starting with the
> measurement that sounds most sophisticated.

## Lab: Measuring Both Halves

Four programs, pure Python, nothing to install. About fifty minutes, and there is a key for every
step. Work in a new empty folder. The steps say when to save each one; this is the mapping, and the
only ordering that matters is that `claims.py` is saved before `relevance.py`, which imports it:

| Save as | Which block | Imports from |
|---|---|---|
| `separate.py` | the first | nothing |
| `claims.py` | the second | nothing |
| `relevance.py` | the third | `claims.py` |
| `makeset.py` | the fourth | nothing |

**Step 1.** Save `separate.py` and run it.

*Expected result:* 62.5 per cent end to end, 75 per cent retrieval, 73 per cent generation given
good retrieval, and the four cells at 22, 8, 7 and 3.

**Step 2.** Move the three right-answer-no-passage cases into the wrong column: change
`("N", "Y",  3)` to `("N", "N",  3)` and run it again.

*Expected result:* end-to-end falls to 55 per cent while **retrieval and generation are both
unchanged** at 75 and 73. The three cases were never telling you anything about either stage, and
the two stage percentages hold, while the end-to-end figure,
the bottom two cells and the "8 against 7" line all move. The top two cells hold as well, which
is the point: the three cases were never about either stage.

**Step 3.** Put it back. Now make retrieval better and generation worse: change the shapes to
`("Y","Y",22)`, `("Y","N",12)`, `("N","N",3)`, `("N","Y",3)`.

*Expected result:* retrieval rises to 85 per cent, generation falls to 65, and **end-to-end stays
at 62.5 per cent** — the same headline, from a system with a different problem. That is the
argument of the whole section in one edit.

**Step 4.** Save `claims.py` and run it. Read the three passages and the four sentences before
the verdicts.

*Expected result:* 3 of 6 claims supported, 3 of 4 sentences, 25 points apart. Then find claim 4
in `shipping.pdf` for yourself and satisfy yourself that the passage really does say the other
thing.

**Step 5.** Split sentence 1 differently: delete claim 2 (the email) from `CLAIMS` and run it.

*Expected result:* 3 of 5 claims, 60 per cent, and the sentence figure unchanged at 75. **A
reader who simply did not notice a claim produces a higher groundedness figure**, and nothing in
the output marks the difference. Read the program's closing paragraphs while you are there: they
are written against six claims and now contradict the figures printed above them — *25 points
apart* is 15, and *claim 5* is claim 4. That is the moving denominator again, and it is why the
verdicts matter more than the share. This is why step 4 of *What To Actually Do* says to write the
rule down.

**Step 6.** Put it back and save `relevance.py`. Run it.

*Expected result:* answers 1, 2 and 5 at 100 per cent grounded, answer 4 printing `no claims`,
and only answer 1 fully relevant.

**Step 7.** In `relevance.py`, make `grounded` return `1.0` instead of `None` when there are no
claims — which is what a careless division does.

*Expected result:* answer 4 now shows `0 of 0  100%` and sits at the top of the grounded column
beside answers 1, 2 and 5, having said nothing. Then work out what a system optimised against
that metric would learn to do.

**Step 8.** Put it back and save `makeset.py`. Run it.

*Expected result:* 8 of 8 on the generated questions, 2 of 8 on the asked ones, and an overlap
table showing three to six shared words against none or one.

**Step 9.** Make one asked question look more like its passage: change the question for passage 2
from `"How soon will it turn up?"` to `"How many days is standard delivery?"`.

*Expected result:* the asked set rises to 3 of 8, from 25 per cent to 38, and passage 2's asked
overlap rises from 0 to 2. One question rewritten *towards* its passage moved the headline 13
points, which is the whole generated set's effect in miniature — and it is the direction you must
not let a rewrite go.

**Step 10.** In `makeset.py`, remove the `None` return from `best` so that a top score of zero
returns an index again.

*Expected result:* the asked set rises to 3 of 8 — and the extra hit is question 0, which shares
not one word with any of the eight passages and is scored right because the tie went to the
lowest index, which happens to be its own. Four of the eight asked questions have zero overlap
everywhere, so the fake hit was luck about which index the tie fell to. **An earlier version of
this program counted exactly that as a hit.** A retrieval figure that counts a no-overlap tie as a
hit is the kind of defect that only ever moves a number in your favour.

## Summary, Key Terms, and Review Questions

### Summary

A grounded answer has two halves, and one verdict on the answer cannot say which failed. **Score
every case twice** — did the retrieved passages hold an answer, and was the answer right — and
the single 62.5 per cent becomes four cells: 22 fine, **8 where an answer was in the context and
the system got it wrong, which finding more passages fixes none of** — Chapter 28's section on
this cell puts the levers at order, trimming and the instruction, and is blunt that they change
what you can check rather than what the model does — 7 where no answer
was there, which is retrieval's and no prompt work touches, and 3 where **no passage held an
answer and the answer was right anyway.** The end-to-end figure counts those three as successes
and they are failures of a grounded system: the answer did not come from the passages, so nothing
can show where it came from and nothing will notice when the document changes. Eight against seven
says both stages, in almost equal measure, and the headline said nothing.

**An answer is grounded when every claim it makes is supported by a retrieved passage**, which is
Chapter 28's citation principle — the quote must *entail* the statement — applied to every claim
rather than only to the cited ones. **Faithfulness** is the other name for the same property.
Worked on one answer: 3 of 6 claims supported against 3 of 4 sentences, **two figures 25 points
apart from the same answer**, and the whole difference is the unit, because sentence 1 carries one
supported claim and one invented one and checking by sentence lets the first vouch for the second.
The claim that answered the question — *about 18 days* — is unsupported, built on a real passage
read as saying something it does not say, and adds two kinds of day together. The answer
carries no citations at all, and **had it cited the two passages it leaned on, both citations
would have passed Chapter 28's three mechanical checks.** Decomposing into claims is itself a judgement, so a groundedness
figure is comparable only against itself under one rule held still.

**Grounded is not relevant, and the demonstration is one answer.** A sentence copied from a
retrieved passage about something else is grounded on every claim it makes and answers neither
part of the question, so groundedness alone ranks it level with a correct, complete answer.
**Answer relevance** is the second measure, and an answer that makes no claims is the case that
breaks a leaderboard: score it 100 per cent and refusing becomes the best strategy your metric
knows, which is why a groundedness figure needs a refusal detector beside it — Chapter 30's check,
which Chapter 31 files as one code can decide.
Relevance is not a yes or no either — decompose a question with parts and count them.

**Your cases come from two places and neither is enough.** Real failures give you the questions
people ask; generated questions give you an answer key for free, because you know which passage
each came from, and coverage of the corners nobody has asked about. **The trap is that a generated
set is easy by construction**: a word-overlap retriever ranks the right passage first on 8 of 8
generated questions and 2 of 8 asked ones, because a generated question shares three to six words with its
source passage and a real one shares none or one. A question built from a passage is a question
about your vocabulary. So generate, then **rewrite the questions away from the passage's wording
and keep the key** — and keep the two sets apart, because averaging them gives a number that
means neither.

### Key Terms

| Term | Meaning |
|---|---|
| **Grounded** | Every claim the answer makes is supported by a passage that was retrieved. Says nothing about whether the passages were right or the answer useful |
| **Faithfulness** | The same property under the name an interviewer may use: the answer is faithful to the passages it was given |
| **Answer relevance** | Whether the answer addresses what was asked. Independent of groundedness, and not a yes or no once the question has parts |
| **Claim-level check** | Decomposing an answer into its claims and giving each one a verdict against the retrieved passages. The verdicts are what tell you which sentence to fix |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Why two scores per case | One verdict cannot say which stage failed. 62.5 per cent end to end was 75 per cent retrieval and 73 per cent generation given good retrieval |
| The four cells | Fine; answer there and got it wrong (generation's); answer not there (retrieval's); answer not there and right anyway (a failure, counted as a success) |
| The cell people miss | Right answer, no supporting passage. 3 of 40 here. Nothing can show where it came from, and nothing notices when the document changes |
| What grounded means | Every claim supported by a retrieved passage. Chapter 28's entailment test applied to every claim, not only the cited ones |
| Why the unit matters | 3 of 6 claims against 3 of 4 sentences — 25 points, same answer. The coarser unit lets a supported claim vouch for an unsupported one |
| The two independent measures | Groundedness and answer relevance. A sentence copied from an off-topic retrieved passage is 100% grounded and answers nothing |
| The no-claims answer | A refusal has nothing to support, so a careless groundedness figure scores it 100% and rewards refusing. Pair it with a refusal detector |
| Where cases come from | Real failures for the questions people ask; generated questions for a free answer key and coverage |
| The cost of a generated set | With a word-overlap retriever, 8 of 8 generated against 2 of 8 asked on the same passages — a generated question shares 3 to 6 words with its source, a real one none or one. A retriever that does not match words would narrow the gap; by how much is a measurement, not a prediction |

### Review Questions

1. Why measure retrieval and generation separately?
2. What is a claim-level check on a grounded answer?
3. Where do your labelled evaluation cases come from?
4. Your groundedness figure is 95 per cent and users still complain. What do you look at?
5. Somebody shows you an evaluation set of two thousand generated cases. What do you ask?

### Review Answers

1. Because one verdict on the answer cannot say which half failed, and the two halves have little
in common. Score each case twice — did the retrieved passages hold an answer at all, and was
the answer right — and the single figure turns into four cells. In the chapter's forty, 62.5 per
cent end to end was 22 fine, 8 where an answer was sitting in the context and the system still
got it wrong, 7 where nothing in the context answered the question, and 3 where no passage held
the answer and the answer was right anyway. The 8 is where an answer was present and the system still missed it, and finding more passages
fixes none of them — Chapter 28's section on the passage that gets ignored is about this cell,
and its levers are order, trimming and the instruction; the 7 is retrieval's and no instruction will fix one of them; and
8 against 7 says work on both, which the 62.5 per cent could not have told you. The detail that
shows this has been used rather than read is the fourth cell: **a right answer with no supporting
passage is a failure**, not a success, because the answer did not come from the passages, nothing
in the system can show where it did, and when the document changes nothing about that case will
notice — yet the end-to-end figure counts it as a win. The lab makes the argument in one edit:
hold retrieval at 85 per cent and drop generation to 65 and the headline sits at 62.5 per cent,
exactly where it was for a system with a different problem.
2. Decomposing the answer into the claims it makes, and giving each claim a verdict against the
retrieved passages — supported, or not. The share of supported claims is the groundedness figure;
the per-claim verdicts are the part worth having, because they say which sentence to fix, which
no aggregate does. Two things about it are easy to get wrong. The first is the unit: the chapter's
worked answer is 3 of 6 claims supported and 3 of 4 sentences, **25 points apart on the same
answer**, because sentence 1 carries one supported claim and one invented one and checking a
sentence at a time lets the first vouch for the second — so here the coarser unit flattered the
answer, and two teams reporting 80 per cent may be decomposing two steps apart. It does not run
reliably one way: three supported claims in one sentence beside one unsupported claim in another
gives 75 per cent by claim and 50 by sentence. The second is that the
decomposition is itself a judgement: six claims is what one reader found in four sentences, and
another might find five or seven, so the figure is comparable only against itself under a rule
written down and held still. What the check buys over Chapter 28's three mechanical citation
checks is the case those cannot reach: in the worked answer both citations pass all three — the
document exists, the quote is in it, it is at the offset claimed — and the claim is still wrong,
because `shipping.pdf` gives three to five days for delivery *to* the customer and the answer used
it for the return journey. That is Chapter 28's own point about entailment, built into a check.
3. Two sources, and you need both. **Real failures** give you the questions people actually ask:
Chapter 30's forty came from reading real outputs, and that is the better source because the
distribution is real. Its limit is that you only ever get cases for questions somebody has
already asked. **Your own documents** give you the rest: write a question from a passage and you
have a case whose answer key you did not have to label, because you know which passage you made
it from, and you can generate one per passage to find the corners of your documents nobody has
ever asked about. The thing to know — and the reason this is a question worth asking — is that a
generated set is easy by construction. In the chapter's eight passages, a word-overlap retriever ranks
the right passage first on **8 of 8** generated questions and **2 of 8** of the same facts asked
the way a person would ask them — a retriever that does not match words would likely do better
on the asked set, which is a measurement to make rather than a prediction — because a generated question shares three to six words with its source
passage and a real question shares none or one. A question built from a passage is a question
about your vocabulary rather than about your documents. So generate for the key and the coverage,
then rewrite every question away from the passage's wording, keeping the key — and keep the two
sets apart rather than averaging them, because the average measures neither.
4. The two things groundedness cannot see, in this order. First, **answer relevance**: an answer can be
grounded on every claim it makes and answer nothing that was asked. The chapter's example is a
sentence copied out of a retrieved passage about standard delivery, offered to a question about
refunds — 100 per cent grounded, zero parts of the question answered, and level with a correct
answer on any groundedness leaderboard. So measure whether the answer addresses the question, and
decompose the question when it has parts, because a system that reliably answers the first half
of everything looks fine on a measure that asks only whether the answer is about the question.
Second, **the no-claims answer**: a refusal has nothing to support and nothing to contradict, so
a groundedness figure computed carelessly scores it 100 per cent, and a 95 per cent average can
be hiding a pile of answers that said nothing at all. Check what the figure does with zero claims
and put a refusal detector beside it — Chapter 30 named that check and Chapter 31 files it among
the ones code can decide, so it is cheap. And third, the figure's own denominator:
groundedness says nothing about whether the *passages* were right, so if retrieval is handing the
model the wrong passages, a faithful answer to them is exactly what you would see. That is the
retrieval column of question 1, and it is the thing a groundedness figure is structurally unable
to report.
5. How the questions were written, before anything else — and the answer "generated from the
documents" is the one to worry about. Two thousand cases with a free answer key is worth having
for coverage, and it is not a measurement of how the system does on real questions. The specific
thing to ask for is the **word overlap between each question and its target passage**, because
that is where the problem lives: in the chapter's set the generated questions shared three to six
words with their source passages and scored 8 of 8, while the same facts asked naturally shared
none or one and scored 2 of 8. A set that has never been rewritten away from its passages will
report a retrieval figure above what users experience, and furthest above it when the retriever
matches words, and nothing about it looks wrong — the
numbers are high, the set is large, and every case has a key. Then ask two more. Were the
questions generated by the same model that answers them, because an evaluation set written by the
mechanism under test will report that the mechanism works. And is this set kept apart from the
real-failure cases, or averaged with them, because an average of an easy set and a hard one
measures neither.

> **You understand this when** you can say why a right answer with no supporting passage is a
> failure, and what you would ask for before believing a retrieval figure measured on a generated
> set.
