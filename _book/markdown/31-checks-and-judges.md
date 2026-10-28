# Checks and Judges, and Validating a Judge

Chapter 30 left you with a list of named failure modes and counts against them, and with the
instruction to let those modes decide what you measure. This chapter builds the measuring. It
has two halves that are easy to run together and must not be: *what to build*, which is a
pass-or-fail check for each mode and code wherever code can decide, and *what to establish
before you believe it*, which is that your judge agrees with you on the failures and not only
on the passes, that it agrees with itself, and that it is not answering a question about
presentation order instead of about the answers.

*The problem.* I asked a model to score my outputs out of five. The scores look reasonable and
mean nothing.

*The question.* How do you build a judgement you can act on, and how do you establish that it
can be trusted?

## Why the Score Out of Five Fails

Chapter 30 gave half the answer: a number between one and five cannot say which of eight things
went wrong, so nothing follows from it. Here is the other half, and it is about the score as a
*measurement* rather than as a guide.

**A score has to be interpreted before it can be used, and the interpretation is yours, not the
model's.** Is 3 acceptable? Is the difference between 3 and 4 the same size as the difference
between 4 and 5? When the average moves from 3.4 to 3.6, did two answers get much better or did
twenty get slightly better, and does it matter which? Every one of those questions has to be
answered before the number means anything, and none of them is answered by the number.

**A pass-or-fail verdict per failure mode has none of those problems**, because the thing it
returns is the thing you act on. "Nine of the sixty answers contradict a passage" is a count of a
named failure, which is the shape chapter 30 taught you to want. There is no scale to calibrate
and no threshold to argue about, and when the count moves you know exactly what changed.

> **Note:** This is not an argument against using a model to decide. It is an argument about what
> you ask it for: a verdict on one named thing, not an impression of overall quality. The rest of
> this chapter is about a model being asked for verdicts, and about how little you should believe
> one before you have checked it. Two of those checks carry over to a score much as they do to a
> verdict — the same answer twice, and the same answer with an arbitrary element of the prompt
> varied — because neither needs a label. What a score cannot have is the comparison against your own two groups, which is most
> of this chapter.

## Code First, and Not as a Compromise

Before any of that, there is a question most people skip: does this check need a judgement at
all? Here are chapter 30's eight modes with the checks aimed at them, each sorted by
what it needs in order to return a verdict.

```python
"""What code can decide, and what is left for a judge.

Chapter 30 left this application with eight named failure modes and the
checks aimed at them. This sorts every check into one of three kinds,
because the kind decides who runs it - and the sorting is the answer to
"when do you use a model as a judge".
"""

# mode, the check that would catch it, and what the check needs in
# order to return a verdict.
CHECKS = [
    ("Citation does not support", "the cited document exists",
     "code", "a filename against a list of filenames"),
    ("Citation does not support", "the quote appears in that document",
     "code", "a substring test"),
    ("Citation does not support", "the quote is at the offset claimed",
     "code", "two integers and a slice"),
    ("Refuses when the answer is there", "the answer declines to answer",
     "code", "a phrase list, once you have read your own refusals"),
    ("Refuses when the answer is there", "the passages do answer the question",
     "judge", "deciding whether a passage answers a question"),
    ("Wrong register or language", "the answer is in the question's language",
     "code", "a stopword test; a character range sorts scripts"),
    ("Not an answer at all", "the answer contains a figure when one was asked for",
     "code", "a digit test against the question"),
    ("Contradicts itself", "the answer gives two values in one unit",
     "code", "pulling the numbers out and comparing them"),
    ("Contradicts itself", "two statements are about the same thing",
     "judge", "deciding what two sentences are about"),
    ("Invents a detail", "every phone number and email in the answer is in a passage",
     "code", "a regular expression and a substring test"),
    ("Contradicts the passage", "the answer's figures match the passage's",
     "code", "pulling both out and comparing literal figures"),
    ("Contradicts the passage", "the answer does not weaken what the passage states",
     "judge", "deciding whether 'approximately 14 days' is 14 days"),
    ("Citation does not support", "the quote supports the sentence it is attached to",
     "judge", "deciding whether one piece of text entails another"),
    ("Answers a different question", "the answer is about what was asked",
     "judge", "deciding what two pieces of text are about"),
    ("Wrong register or language", "the answer is in the brand's register",
     "judge", "comparing a tone against examples of a tone"),
    ("Invents a detail", "every claim in the answer is in a passage",
     "judge", "splitting the answer into claims, then entailment"),
]

if __name__ == "__main__":
    code = [c for c in CHECKS if c[2] == "code"]
    judge = [c for c in CHECKS if c[2] == "judge"]
    print(f"  {len(CHECKS)} checks: {len(code)} code, {len(judge)} judge\n")
    print("  CODE CAN DECIDE THESE. Do not ask a model.")
    for mode, check, _, needs in code:
        print(f"    {check}")
        print(f"      needs: {needs}")
    print("\n  THESE NEED A JUDGEMENT.")
    for mode, check, _, needs in judge:
        print(f"    {check}")
        print(f"      needs: {needs}")

    print("\n  Read the 'needs' lines and the rule appears on its own.")
    print("  Every code check needs a comparison between two things")
    print("  that are both literally present: a filename, a substring,")
    print("  an offset, a digit. Every judge check needs a decision")
    print("  about what text MEANS - entailment, aboutness, tone - and")
    print("  there is no substring test for any of them.")

    modes = {c[0] for c in CHECKS}
    both = sorted(m for m in modes
                  if {c[2] for c in CHECKS if c[0] == m} == {"code", "judge"})
    print(f"\n  {len(both)} of the {len(modes)} modes here are split, with")
    print("  part decidable in code and part not:")
    for m in both:
        print(f"    {m}")
    has_code = sorted(m for m in modes
                      if "code" in {c[2] for c in CHECKS if c[0] == m})
    print(f"\n  And {len(has_code)} of the {len(modes)} have SOME part code can")
    print("  decide, which is the practical finding. A mode is not")
    print("  'a code mode' or 'a judge mode'; running the code part")
    print("  first leaves the judge less to do and less to be wrong")
    print("  about.")
```

```text
  16 checks: 9 code, 7 judge

  CODE CAN DECIDE THESE. Do not ask a model.
    the cited document exists
      needs: a filename against a list of filenames
    the quote appears in that document
      needs: a substring test
    the quote is at the offset claimed
      needs: two integers and a slice
    the answer declines to answer
      needs: a phrase list, once you have read your own refusals
    the answer is in the question's language
      needs: a stopword test; a character range sorts scripts
    the answer contains a figure when one was asked for
      needs: a digit test against the question
    the answer gives two values in one unit
      needs: pulling the numbers out and comparing them
    every phone number and email in the answer is in a passage
      needs: a regular expression and a substring test
    the answer's figures match the passage's
      needs: pulling both out and comparing literal figures

  THESE NEED A JUDGEMENT.
    the passages do answer the question
      needs: deciding whether a passage answers a question
    two statements are about the same thing
      needs: deciding what two sentences are about
    the answer does not weaken what the passage states
      needs: deciding whether 'approximately 14 days' is 14 days
    the quote supports the sentence it is attached to
      needs: deciding whether one piece of text entails another
    the answer is about what was asked
      needs: deciding what two pieces of text are about
    the answer is in the brand's register
      needs: comparing a tone against examples of a tone
    every claim in the answer is in a passage
      needs: splitting the answer into claims, then entailment

  Read the 'needs' lines and the rule appears on its own.
  Every code check needs a comparison between two things
  that are both literally present: a filename, a substring,
  an offset, a digit. Every judge check needs a decision
  about what text MEANS - entailment, aboutness, tone - and
  there is no substring test for any of them.

  6 of the 8 modes here are split, with
  part decidable in code and part not:
    Citation does not support
    Contradicts itself
    Contradicts the passage
    Invents a detail
    Refuses when the answer is there
    Wrong register or language

  And 7 of the 8 have SOME part code can
  decide, which is the practical finding. A mode is not
  'a code mode' or 'a judge mode'; running the code part
  first leaves the judge less to do and less to be wrong
  about.
```

**The column sorts the checks by what they need, and claims nothing about coverage.** Chapter 30
is emphatic that a check catches failures rather than modes, and these are no exception: *the
answer's figures match the passage's* passes "said refunds take 14 working days, policy says 14
days", because the figures do match.

**The rule is in the `needs` column rather than in anybody's opinion.** Every check in the first
list compares two things that are both literally present — a filename against a list of
filenames, a quote against a document, two integers, a digit. Every check in the second list
needs a decision about what text *means*: whether one piece of text entails another, what two
pieces of text are about, whether a tone matches a tone. There is no substring test for any of
those, and that is the line.

**So the answer to when you use a model as a judge is: when the check needs a decision about
meaning, and not before.** Not because code is more virtuous, but because a code check is
cheap, identical every time, and has no verdict of its own to validate. Every model
judgement you add is a second thing that can be wrong, and the rest of this chapter is the bill
for it.

**And a mode is not a code mode or a judge mode.** Six of the eight here split, with part
decidable in code and part not, and seven of the eight have some part code can decide. *Refuses
when the answer is there* is the one to study: detecting a refusal is a phrase list, and deciding
that the answer *was* there is a judgement about what a passage means — so the code half alone
fires on a correct refusal, which is why the mode is named the way chapter 30 named it. *Invents a
detail* is the clearest: a regular expression finds every phone number and email in the answer
and tests each against the passages, which is two of that mode's six failures for an afternoon's
work, and what is left — every *claim* supported by a passage — is the hard entailment problem
Chapter 32 builds. Run the cheap part first and the judge has less to do and less to be wrong about.

> **Warning:** The failure here is not using a model where code would do; it is reaching for the
> model *first* and never going back. A judge that has to decide whether the cited document
> exists is being asked to do a `in` test from memory, which it will sometimes get wrong, and
> every one of those errors lands in your numbers as if it were a finding about your
> application.

## A Judge Is a Classifier, So Measure It Like One

Now the **judge**. It returns pass or fail on one named mode, which means it is a thing that sorts
answers into two groups — and there is a settled way to find out whether such a thing works,
which is to compare its groups against yours on cases where you have decided for yourself.

The field's name for the arrangement is **LLM-as-a-judge**, and that is what an interviewer
will call it. The name is wider than what this chapter builds: it is used wherever a model
scores output, including the score out of five this chapter's first section threw out.

**You have to label some cases by hand**, because every figure below is a comparison against
your own verdicts and there is nobody else's to compare against. The set here is sixty: an input, an answer, and my own verdict on each.

```python
"""Sixty cases, my labels, and two judges' verdicts, all recorded.

Each row is one case: my own label, then judge A's verdict, then judge
A's verdict on a SECOND showing of the same answer, then judge B's.
F is fail, P is pass, and a dash means the case was not shown twice.

The rows are written out rather than generated, so every count below
can be arrived at by hand from this table.
"""

#        mine  A   A2   B
ROWS = """
F  F  F  F
F  F  F  F
F  F  F  F
F  F  F  F
F  F  P  F
F  P  P  F
F  P  P  F
F  P  F  F
F  P  P  F
F  P  P  F
F  P  P  P
F  P  P  P
P  F  F  F
P  F  F  F
P  P  P  F
P  P  F  F
P  P  P  F
P  P  P  F
P  P  P  F
P  P  P  F
P  P  -  F
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
P  P  -  P
"""

CASES = [line.split() for line in ROWS.strip().splitlines()]
MINE = [c[0] for c in CASES]
A    = [c[1] for c in CASES]
A2   = [c[2] for c in CASES]
B    = [c[3] for c in CASES]
N = len(CASES)

def table(mine, judge):
    """The four counts. Nothing else in this file is new arithmetic."""
    return {
        "both fail":  sum(1 for m, j in zip(mine, judge) if m == "F" and j == "F"),
        "missed":     sum(1 for m, j in zip(mine, judge) if m == "F" and j == "P"),
        "false alarm":sum(1 for m, j in zip(mine, judge) if m == "P" and j == "F"),
        "both pass":  sum(1 for m, j in zip(mine, judge) if m == "P" and j == "P"),
    }

def report(name, judge):
    t = table(MINE, judge)
    agree = t["both fail"] + t["both pass"]
    fails = t["both fail"] + t["missed"]
    alarms = t["both fail"] + t["false alarm"]
    print(f"  {name}")
    print(f"    agrees with me on            {agree:3d} of {N}"
          f"   {agree/N:4.0%}")
    print(f"    of the {fails} failures, catches  {t['both fail']:3d}"
          f"        {t['both fail']/fails:4.0%}")
    print(f"    of its {alarms:2d} alarms, real        "
          f"{t['both fail']:3d}        {t['both fail']/alarms:4.0%}")
    print(f"    missed {t['missed']}, false alarms {t['false alarm']}\n")

if __name__ == "__main__":
    assert all(len(c) == 4 for c in CASES)
    fails = MINE.count("F")
    print(f"  {N} cases. I labelled {fails} of them fail"
          f" and {MINE.count('P')} pass.\n")

    print("  A judge that says PASS to everything:")
    nothing = ["P"] * N
    t = table(MINE, nothing)
    print(f"    agrees with me on            "
          f"{t['both pass']:3d} of {N}   {t['both pass']/N:4.0%}")
    print(f"    of the {fails} failures, catches    0           0%\n")
    print("  That is the number every other number has to beat,")
    print("  and it comes free.\n")

    report("Judge A, the first one written:", A)
    report("Judge B, after one change to its instructions:", B)

    print("  Read the two judges by their single number and A wins")
    print("  by 85 to 82. Read them by what a judge is FOR, which is")
    print("  finding the failures, and B catches 10 where A catches")
    print("  5 - at the cost of 9 false alarms against 2. Which of")
    print("  those you want depends on what a false alarm costs you.")
    print("  What is certain is that the single number cannot tell")
    print("  you, and that it moved in the OPPOSITE direction to the")
    print("  catching: 48 of the 60 cases are passes, so agreeing")
    print("  with me about a pass is most of what it measures.\n")

    pairs = [(a, a2) for a, a2 in zip(A, A2) if a2 != "-"]
    same = sum(1 for a, a2 in pairs if a == a2)
    print(f"  Judge A, shown {len(pairs)} of the same answers a second time:")
    print(f"    same verdict both times      {same:3d} of {len(pairs)}"
          f"   {same/len(pairs):4.0%}")
    flipped = [i for i, (a, a2) in enumerate(zip(A, A2))
               if a2 != "-" and a != a2]
    print(f"    flipped on cases             {flipped}")
    caught_then_flipped = [i for i in flipped if MINE[i] == "F" and A[i] == "F"]
    print(f"\n  Of the 5 failures A caught, {len(caught_then_flipped)}"
          f" flipped to pass on")
    print("  a second showing. So '5 of 12' is itself a number that")
    print("  moves, and the two agreement figures above inherit")
    print("  every bit of that movement.")
```

```text
  60 cases. I labelled 12 of them fail and 48 pass.

  A judge that says PASS to everything:
    agrees with me on             48 of 60    80%
    of the 12 failures, catches    0           0%

  That is the number every other number has to beat,
  and it comes free.

  Judge A, the first one written:
    agrees with me on             51 of 60    85%
    of the 12 failures, catches    5         42%
    of its  7 alarms, real          5         71%
    missed 7, false alarms 2

  Judge B, after one change to its instructions:
    agrees with me on             49 of 60    82%
    of the 12 failures, catches   10         83%
    of its 19 alarms, real         10         53%
    missed 2, false alarms 9

  Read the two judges by their single number and A wins
  by 85 to 82. Read them by what a judge is FOR, which is
  finding the failures, and B catches 10 where A catches
  5 - at the cost of 9 false alarms against 2. Which of
  those you want depends on what a false alarm costs you.
  What is certain is that the single number cannot tell
  you, and that it moved in the OPPOSITE direction to the
  catching: 48 of the 60 cases are passes, so agreeing
  with me about a pass is most of what it measures.

  Judge A, shown 20 of the same answers a second time:
    same verdict both times       17 of 20    85%
    flipped on cases             [4, 7, 15]

  Of the 5 failures A caught, 1 flipped to pass on
  a second showing. So '5 of 12' is itself a number that
  moves, and the two agreement figures above inherit
  every bit of that movement.
```

Start with the judge that says pass to everything, because it is the **baseline** — what every
other number has to beat, and it costs nothing. On this set it agrees with me 48 times in 60, which is
80 per cent. It finds no failures at all. **Any single agreement figure has that number buried in
it**, and on a working application the baseline is high precisely because the application mostly
works — a system that failed half the time would have a baseline of 50 per cent and a far more
honest-looking judge.

**Then judge A, at 85 per cent.** Five points above doing nothing, and those five points are
the whole of what that figure is worth. Split the figure and you can see where it comes from: of the 12 answers I
called fail it catches 5, and of its 7 alarms 5 are real — which is the property chapter 30 left
open, not whether a check catches failures but whether it fires only on them. **Those are the
two numbers, and neither is deducible from the 85.**

> **Note:** An interviewer will call these *precision* and *recall*: precision is the share of
> the judge's alarms that are real, 5 of 7 here, and recall is the share of real failures it
> catches, 5 of 12. They are worth knowing by those names. Chapter 26's *recall@k* is a
> different quantity that shares the word — it is the share of the relevant documents that reach
> the top k of a ranking, and blind to their order — so do not carry one into the other.

**Then judge B, which is worse by the single number and better at the job.** One change to its
instructions, and it catches 10 of the 12 failures where A caught 5. Its agreement figure drops
from 85 to 82. **The number went down while the thing the judge exists for went up**, and the
reason is arithmetic rather than subtle: 48 of the 60 cases are passes, so agreeing with me about
a pass is most of what the single figure measures, and B buys its 5 extra failures with 7 extra
false alarms.

**Which of A and B you want is a real decision and the figures do not make it for you.** B's 9
false alarms are 9 answers somebody has to read and clear. If clearing one is cheap, take B. If
your judge gates a release, 9 false alarms will teach everybody to ignore it, and that is worse
than A's 7 misses. What is not a decision is which numbers to look at: the single one cannot
distinguish these two judges in the direction that matters.

**And then the question that is prior to all of it: does the judge agree with itself?** Twenty of
these answers — the twelve I called fail and eight of the passes, chosen that way so that a flip
could be traced to the catch count — were shown to judge A a second time, unchanged. It gave the same verdict on 17 and
flipped on 3 — rows 4, 7 and 15 of the table, counting from zero — and one of the flips is a
failure it had caught, so "5 of 12" could have been
printed as "4 of 12" from the same judge and the same answers. That figure is its **self-agreement**, and what it bounds is how much
of any other figure you can rely on: on the answers a judge flips, the number you measured is
whichever showing you happened to use. A verdict it does not hold twice is not only about the
answer. Chapter 20 requires a verdict that does not wander and hands the
building of one to this chapter: this is where you find out whether yours does, and the way is to
show it the same answer twice and count.

> **Tip:** Self-agreement needs no labels at all — only the same input twice. Run it first. A
> judge at 85 per cent with itself on twenty showings does not need validating against your
> labels yet; it needs its instructions tightened until it stops
> changing its mind — and where they cannot be, chapter 20's trials are what bound it.

## How Much Each Number Is Worth

Three figures came out of judge A: 85 per cent, 42 per cent, 71 per cent. They are printed to the
same precision and they are not worth the same, because they do not rest on the same evidence.

```python
"""How much each of the three numbers is worth, given 60 labels.

Chapter 20's resampling procedure, applied to judge A's three figures.
The point is not the method, which is chapter 20's; it is that the
three numbers rest on 60, 12 and 7 labels and read as if they rested
on the same amount of evidence.
"""
import random
from judge import MINE, A, N

def figures(pairs):
    """The three numbers, from a list of (my label, judge verdict)."""
    hits = sum(1 for m, j in pairs if m == "F" and j == "F")
    fails = sum(1 for m, j in pairs if m == "F")
    alarms = sum(1 for m, j in pairs if j == "F")
    agree = sum(1 for m, j in pairs if m == j)
    return (agree / len(pairs),
            hits / fails if fails else None,
            hits / alarms if alarms else None)

def interval(index, rounds=10000, seed=31):
    r = random.Random(seed)
    pairs = list(zip(MINE, A))
    out = []
    for _ in range(rounds):
        sample = [pairs[r.randrange(N)] for _ in range(N)]
        v = figures(sample)[index]
        if v is not None:
            out.append(v)
    out.sort()
    return out[len(out) // 40], out[len(out) * 39 // 40]

if __name__ == "__main__":
    agree, caught, real = figures(list(zip(MINE, A)))
    rows = [
        ("agrees with me",        agree,  N,                 0),
        ("of failures, caught",   caught, MINE.count("F"),   1),
        ("of its alarms, real",   real,   A.count("F"),      2),
    ]
    print(f"  Judge A's three figures, each with the number of")
    print(f"  labels it is computed from, and chapter 20's")
    print(f"  resampled 95% interval round it.\n")
    print("  figure                 value   labels   interval")
    for name, value, labels, idx in rows:
        lo, hi = interval(idx)
        print(f"  {name:22s} {value:5.0%}   {labels:6d}"
              f"   {lo:4.0%} to {hi:4.0%}")

    print("\n  All three are printed to the same number of digits")
    print("  and not one of them is worth the same as another. The")
    print("  85% rests on all 60 labels. The 42% rests on the 12")
    print("  cases I called fail, and the only lever on it is")
    print("  labelling more FAILURES - more passes do not help.")
    print("  The 71% rests on 7 alarms, and an interval that wide")
    print("  is a way of saying you do not know.\n")

    print("  So the practical answer to 'how many should I label' is")
    print("  not a number of cases. It is: enough of the cases you")
    print("  call FAIL, because that is the figure you are going to")
    print("  act on, and in a working application they are the rare")
    print("  ones. 60 labels bought 12 of them.")
```

```text
  Judge A's three figures, each with the number of
  labels it is computed from, and chapter 20's
  resampled 95% interval round it.

  figure                 value   labels   interval
  agrees with me           85%       60    75% to  93%
  of failures, caught      42%       12    12% to  73%
  of its alarms, real      71%        7    33% to 100%

  All three are printed to the same number of digits
  and not one of them is worth the same as another. The
  85% rests on all 60 labels. The 42% rests on the 12
  cases I called fail, and the only lever on it is
  labelling more FAILURES - more passes do not help.
  The 71% rests on 7 alarms, and an interval that wide
  is a way of saying you do not know.

  So the practical answer to 'how many should I label' is
  not a number of cases. It is: enough of the cases you
  call FAIL, because that is the figure you are going to
  act on, and in a working application they are the rare
  ones. 60 labels bought 12 of them.
```

**The intervals are the finding, and the method is Chapter 20's**, applied here rather than
rebuilt. The 85 per cent rests on all 60 labels and lands between 75 and 93. The 42 per cent —
the figure you are actually going to act on — rests on the 12 cases I called fail, and lands
anywhere between 12 and 73. The 71 per cent rests on 7 alarms and runs from 33 to 100, which is
a way of writing *I do not know*.

**So the practical answer to "how many cases should I label" is not a number of cases.** It is:
enough of the cases you call *fail*, because the catch rate is computed from those alone and
more passes do nothing for it. Sixty labels bought twelve failures. If you want the catch rate to
mean something, label failures — which, in a working application, means reading a great many
passes to find them, and is the reason this is the expensive part.

> **Warning:** Do not read the narrow interval on the single figure as a reason to prefer it. It
> is narrow because it is mostly a measurement of how often the application is fine, which you
> already knew. A precise number about the wrong quantity is the trap this whole chapter is
> about.

## Position Bias

One more thing can be wrong with a judge, and it has nothing to do with labels. Ask a model which
of two answers is better and the order you print them in changes the verdict.

```python
"""The same judge, the same forty pairs, two presentation orders.

A pairwise judge is asked which of two answers is better. Every pair
was shown to it twice: once with the new answer first, once with the
old answer first. Each row records which answer it picked each time,
and my own reading of that pair.

Written out rather than generated. 10+2+10+2+8+8 = 40.
"""

#        new-first  old-first   mine
ROWS = (
    [("new", "new", "new")] * 10 +   # picked new both ways, I agree
    [("new", "new", "old")] * 2 +    # picked new both ways, I do not
    [("old", "old", "old")] * 10 +   # picked old both ways, I agree
    [("old", "old", "new")] * 2 +    # picked old both ways, I do not
    [("new", "old", "new")] * 8 +    # picked whichever was FIRST
    [("new", "old", "old")] * 8      # ditto
)

NEW_FIRST = [r[0] for r in ROWS]
OLD_FIRST = [r[1] for r in ROWS]
MINE      = [r[2] for r in ROWS]
N = len(ROWS)

def rate(picks):
    return picks.count("new") / len(picks)

if __name__ == "__main__":
    assert N == 40 and len(MINE) == 40
    print(f"  {N} pairs, each judged twice.")
    print(f"  I read them myself and picked the new answer on"
          f" {MINE.count('new')}.\n")

    print("  Showing the NEW answer first:")
    print(f"    new wins {NEW_FIRST.count('new'):2d} of {N}"
          f"    {rate(NEW_FIRST):4.0%}")
    print("  Showing the OLD answer first:")
    print(f"    new wins {OLD_FIRST.count('new'):2d} of {N}"
          f"    {rate(OLD_FIRST):4.0%}\n")
    print("  Same judge, same pairs, same answers. The only thing")
    print("  that changed is which one was printed first, and the")
    print("  headline moved 40 points. Neither figure is a")
    print("  measurement of the answers.\n")

    flip = [i for i in range(N) if NEW_FIRST[i] != OLD_FIRST[i]]
    first = [i for i in flip
             if NEW_FIRST[i] == "new" and OLD_FIRST[i] == "old"]
    print(f"  Pairs where the verdict flipped with the order:"
          f" {len(flip)} of {N}  {len(flip)/N:.0%}")
    print(f"  Of those, the judge picked whichever was shown first:"
          f" {len(first)}")
    print("  That count is the DIRECTION of the order effect and")
    print("  the line above it is its SIZE. Sixteen flips split")
    print("  8 and 8 would be a judge with no preference at all,")
    print("  just an unrepeatable verdict - which is worth knowing")
    print("  too, and is what you cannot see by running one order.\n")

    keep = [i for i in range(N) if NEW_FIRST[i] == OLD_FIRST[i]]
    kept = [NEW_FIRST[i] for i in keep]
    print(f"  Keeping only the {len(keep)} pairs it was consistent on:")
    print(f"    new wins {kept.count('new'):2d} of {len(keep)}"
          f"    {rate(kept):4.0%}")
    halves = kept.count("new") + len(flip) / 2
    print(f"  Or scoring every flipped pair half each:")
    print(f"    new wins {halves:4.1f} of {N}  {halves/N:4.0%}\n")

    print("  Both repairs land on 50%, and so did my own reading")
    print("  of the forty. Do not read that as a validation. It is")
    print("  one set, and the two are not the same procedure, so")
    print("  they can disagree - step 7 of the lab separates them")
    print("  by three points with two edits. What the repairs buy is")
    print("  that the arbitrary choice is gone: neither answer is")
    print("  privileged by being printed first.\n")

    agree = sum(1 for i in keep if NEW_FIRST[i] == MINE[i])
    print(f"  And the number to look at before trusting any of it:")
    print(f"  on the {len(keep)} consistent pairs the judge agrees with")
    print(f"  me on {agree}  {agree/len(keep):.0%}. The {len(flip)} it flipped on")
    print("  are not judgements at all, so the honest report is a")
    print(f"  verdict on {len(keep)} pairs and a refusal on {len(flip)}.")
```

```text
  40 pairs, each judged twice.
  I read them myself and picked the new answer on 20.

  Showing the NEW answer first:
    new wins 28 of 40     70%
  Showing the OLD answer first:
    new wins 12 of 40     30%

  Same judge, same pairs, same answers. The only thing
  that changed is which one was printed first, and the
  headline moved 40 points. Neither figure is a
  measurement of the answers.

  Pairs where the verdict flipped with the order: 16 of 40  40%
  Of those, the judge picked whichever was shown first: 16
  That count is the DIRECTION of the order effect and
  the line above it is its SIZE. Sixteen flips split
  8 and 8 would be a judge with no preference at all,
  just an unrepeatable verdict - which is worth knowing
  too, and is what you cannot see by running one order.

  Keeping only the 24 pairs it was consistent on:
    new wins 12 of 24     50%
  Or scoring every flipped pair half each:
    new wins 20.0 of 40   50%

  Both repairs land on 50%, and so did my own reading
  of the forty. Do not read that as a validation. It is
  one set, and the two are not the same procedure, so
  they can disagree - step 7 of the lab separates them
  by three points with two edits. What the repairs buy is
  that the arbitrary choice is gone: neither answer is
  privileged by being printed first.

  And the number to look at before trusting any of it:
  on the 24 consistent pairs the judge agrees with
  me on 20  83%. The 16 it flipped on
  are not judgements at all, so the honest report is a
  verdict on 24 pairs and a refusal on 16.
```

**The same judge, the same forty pairs, the same answers, and a 40-point swing.** Showing the new
answer first gives it a 70 per cent win rate; showing the old answer first gives it 30 per cent.
Neither figure is a measurement of the answers. Whichever one you happened to run is the one you
would have reported, and nothing in the output would have looked wrong.

That is **position bias** — a judge preferring an answer for where it was printed rather than for
what it says — and the count of flipped pairs is how you measure it: 16 of 40 here, and all 16 went to
whichever answer came first. **That count is what you cannot see by running one order**, which is the
practical argument for running both every time.

**Both repairs remove the arbitrary choice and neither is free.** Keeping only the 24 pairs the judge was consistent on
gives 50 per cent; scoring each flipped pair half to each side also gives 50 per cent. They agree
here and they need not — two changed lines in the lab separate them by three points. The first repair
discards 40 per cent of your data and assumes the pairs the judge was consistent on are not
systematically different from the ones it flipped, which is an assumption and not a fact. The
second keeps everything and dilutes every real result towards a tie.

**And the honest report is two numbers, not one.** On the 24 pairs where the judge held a verdict
it agrees with me on 20, which is 83 per cent. On the 16 it flipped on, it has no verdict at all.
Reporting "the judge agrees with me 83 per cent of the time, on 60 per cent of the pairs" is
longer than "83 per cent" and it is the thing that is true.

> **Note:** A pairwise judge is only one shape. The same question applies to any judge whose
> prompt has an arbitrary element: swap the order of the passages, rename the options, put the
> question before the answer instead of after. Vary the arbitrary thing, run both, and count the
> flips. That is the whole procedure, and it is cheap because it needs no labels.

## What To Actually Do

1. **Take the modes from your error analysis** and write down, per mode, the check that would
   catch it and what the check needs in order to decide.
2. **Build every check that needs only a comparison between things that are present.** Those are
   free, repeatable, and have no verdict of their own to validate.
3. **For what is left, write a judge per mode**, returning pass or fail on that one named thing.
   Never a score, and never one judge for everything.
4. **Measure its self-agreement before anything else**, by showing it the same answer twice. It needs no labels,
   and a judge that changes its mind does not need validating yet — it needs fixing.
5. **If the judge has an arbitrary element, vary it and count the flips.** Order of two answers,
   order of passages, naming of options. Report the flip count.
6. **Then label by hand.** Enough cases that you have a usable number of *failures*, not a
   usable number of cases.
7. **Compute the do-nothing baseline first** — what a judge that always says pass would score — and never report
   an agreement figure without it beside.
8. **Report two numbers per judge:** of the real failures, how many it caught; of its alarms, how
   many were real. Put Chapter 20's interval on both, and expect them to be wide.
9. **Decide which error you can afford** before you tune the judge, because every tightening
   trades one for the other and the single figure will not tell you which way you went.
10. **Keep the labels.** They do not go stale when you change the
    judge, and Chapter 33 is about the set they become.

> **Tip:** Steps 4 and 5 need no labels and will often end the exercise on their own. A judge
> that disagrees with itself, or that is answering a question about print order, cannot be
> rescued by more labelling — and both are an afternoon to discover.

## Lab: Validating a Judge

Four programs, pure Python, nothing to install. About fifty minutes, and there is a key for every
step. Work in a new empty folder. **Save them in this order**, because two of them import from
the others:

| Save as | Which block | Imports from |
|---|---|---|
| `judge.py` | the second | nothing |
| `codefirst.py` | the first | nothing |
| `howsure.py` | the third | `judge.py` |
| `position.py` | the fourth | nothing |

**Step 1.** Save `judge.py` and run it. Read the sixty rows in the source before you read the
output.

*Expected result:* a baseline of 80 per cent, judge A at 85 with 5 of 12 caught, judge B at 82
with 10 of 12. Write down, before step 2, which judge you would ship.

**Step 2.** Change one row: take the last `F  P  P  P` row and make it `F  F  F  F`, so that
judge A now catches a failure it had missed, and holds that verdict on the second showing.

*Expected result:* A's agreement goes to 87 per cent and its catch rate to 6 of 12. Notice that
one case moved the catch rate by 8 points and the headline by 2 — the figure you care about is
the one that moves, which is another way of saying it is the one with least evidence behind it.

**Step 3.** Put it back. Now make the set harder: change the first ten `P  P  -  P` rows to
`F  P  -  P`, so there are 22 failures and judge A misses all ten new ones.

*Expected result:* the baseline falls to 63 per cent and A falls to 68. **A's catch rate falls to
5 of 22, and its agreement figure still beats the baseline by 5 points.** The gap between a judge
and the do-nothing baseline is not a measure of the judge; it moves with how often your
application fails.

**Step 4.** Put it back and save `codefirst.py`. Run it, then read the `needs` column on its own,
ignoring the check names.

*Expected result:* sixteen checks — nine code, seven judge — with 6 of 8 modes split and 7 of 8
holding a code part. Then pick one judge check and try to write it in code. A good one to try is *the answer is
in the brand's register*; work out what you would have to compare, and where it stops being a
comparison.

**Step 5.** In `codefirst.py`, move one check from `judge` to `code` — take *the answer is about
what was asked* and claim a keyword overlap test will do it.

*Expected result:* 10 code and 6 judge, and **8 of 8 modes now have a code part** — while the
split count stays at 6, because that mode had only the one check and has gone from judge-only to
code-only rather than becoming split. Then say why the counts are now wrong: chapter 30's *Answers a different question* includes "answered the question asked two
turns earlier", and a keyword test on the question and the answer passes that one, because the
earlier question shares the vocabulary. Moving a check between the columns is a claim about what
code can decide, and it is checkable against your own failures.

**Step 6.** Save `howsure.py` and run it.

*Expected result:* intervals of 75–93, 12–73 and 33–100. Then change `seed=31` to `seed=32` and
run it again: only the catch rate's upper end moves, from 73 to 71, and the other four ends do
not move at all. A resampled interval is supposed to be that stable at ten thousand rounds — if
yours is not, you have too few rounds or far too few labels.

**Step 7.** Save `position.py` and run it. Then make the two repairs disagree: change
`[("new", "new", "old")] * 2` to `* 4` and `[("old", "old", "old")] * 10` to `* 8`.

*Expected result:* consistent-pairs gives 58 per cent and half-each gives 55, so the two repairs
now differ by three points on the same data. My own labels did not move. Which of the two is
right is not settled by this program, and that is the point: they are different procedures for
the same hole.

**Step 8.** Put step 7's edit back, then make the bias go the other way. Change
`[("new", "old", "new")] * 8` and `[("new", "old", "old")] * 8` to `[("old", "new", "new")] * 8`
and `[("old", "new", "old")] * 8`, so the judge now prefers whichever answer is printed *second*.

*Expected result:* new-first drops to 30 per cent and old-first rises to 70, the flip count is
still 16 of 40, both repairs still give 50 per cent, and the one line that changes is the count
of flips that went to whichever answer was printed first, which falls from 16 to 0. **The flip
count is the measurement that does not care which direction the bias runs**, which is why it is
the one to report — and the first-position count is how you read the direction off it.

**Step 9.** Replace the second-showing entry with a dash on every row except the first two, so
that only two answers were ever shown twice.

*Expected result:* `same verdict both times 2 of 2  100%` and an empty list of flips. **A judge
that was checked twice on two answers prints a perfect self-agreement figure**, in the same
format and to the same precision as the figure from twenty, and the *percentage* says nothing
about which you are looking at. That is why step 4 of *What To Actually Do* says to count, and
why every rate in this chapter is printed with its denominator beside it: a rate without its
denominator is not a measurement.

**Step 10.** Write down, for one check in your own application, which of the two errors you can
afford: a missed failure or a false alarm.

*Expected result:* one sentence naming a cost. If you cannot name one, you cannot tune the judge,
because every change trades one error for the other and you have no rate of exchange.

## Summary, Key Terms, and Review Questions

### Summary

A score out of five fails twice over. Chapter 30 gave the first reason — it cannot say which of
your failure modes went wrong, so nothing follows from it. The second is that it has to be
interpreted before it can be used, and the interpretation is yours: whether 3 is acceptable,
whether 3-to-4 is the same size a step as 4-to-5, whether a move from 3.4 to 3.6 was two answers
or twenty. **A pass-or-fail verdict on one named mode has none of that**, because what it returns
is what you act on.

**Before writing any judge, ask whether the check needs a judgement at all.** Sorted by what each
check needs in order to decide, nine of sixteen need only a comparison between things that are
both literally present — a filename, a substring, an offset, a digit — and seven need a decision
about what text *means*. That is the line, and it is the answer to when to use a model: when the
check needs a decision about meaning, and not before. **A mode is not a code mode or a judge
mode**: six of the eight split, and seven of the eight have a part code can decide, so run the
cheap part first and leave the judge less to be wrong about.

**A judge returns pass or fail, so it is a thing that sorts answers into two groups, and it gets
measured against groups you made by hand.** There is no way round labelling some cases yourself.
Then: **the baseline comes first.** A judge that says pass to everything agrees with me on 48 of
60, which is 80 per cent, and finds nothing — and every single agreement figure has that number
buried in it, high exactly because a working application mostly works. **Judge A's 85 per cent is
five points of value**, and splitting it gives the two figures that matter: of 12 failures it
catches 5, and of its 7 alarms 5 are real. **Judge B is worse by the single number and better at
the job** — 10 of 12 caught against A's 5, agreement down to 82, and 9 false alarms against 2 — because 48 of the 60 cases are passes, so the
single figure mostly measures agreement about passes. Which of them you want depends on what a
false alarm costs you; what is certain is that the one number cannot tell you. **And prior to all
of it, a judge has to agree with itself**: shown 20 of the same answers twice, A held its verdict
on 17, and one of the three flips was a failure it had caught, so "5 of 12" could have printed as
"4 of 12". A judge's self-agreement bounds how much of every other figure you can rely on —
on the answers it flips, what you measured is whichever showing you used — and it is one of the two
measurements here that need no labels at all, the other being the flip count below.

**The three figures are not worth the same, because they do not rest on the same evidence.**
Chapter 20's resampling puts 85 per cent between 75 and 93 on 60 labels, 42 per cent between 12
and 73 on 12 failures, and 71 per cent between 33 and 100 on 7 alarms. So **the answer to "how
many should I label" is a number of failures, not a number of cases**: the catch rate is computed
from the failures alone and more passes do nothing for it.

**Last, position bias: the judge preferring an answer for where it was printed rather than for
what it says.** The same judge on the same forty pairs reports a 70 per cent win rate with the new
answer printed first and 30 per cent with it printed second — a 40-point swing with nothing
changed but the order, and whichever you ran is what you would have reported. **The flip count is
the measurement**: 16 of 40, all to whichever came first, and it is what you cannot see from a
single order. Both repairs give 50 per cent here and neither is free — discarding the
flipped pairs throws away 40 per cent of the data and assumes the rest are not systematically
different, while scoring them half each dilutes every real result towards a tie. The honest report
is two numbers: agrees with me on 20 of the 24 pairs it held a verdict on, and no verdict on the
other 16.

### Key Terms

| Term | Meaning |
|---|---|
| **Judge (LLM-as-a-judge)** | A model asked to return a verdict on one named thing about one output. Pass or fail on a named failure mode, never a score out of five. The field's name is used wherever a model scores output, whatever it returns, so it is wider than this chapter's version |
| **Baseline** | What a judge that always says pass would score on your set. Every agreement figure has to be read against it, and on a working application it is high |
| **Self-agreement** | How often a judge gives the same verdict on the same answer shown twice. Every point of flipping is a point any other figure could have landed elsewhere, and measuring it needs no labels |
| **Position bias** | A judge preferring an answer for where it was printed rather than for what it says. Measured by showing each pair both ways and counting the flips |

### Worth Memorising

| Item | Value or formula |
|---|---|
| When to use a judge rather than code | When the check needs a decision about what text means. Code handles every comparison between things that are both literally present |
| What a judge returns | Pass or fail on one named failure mode. One judge per mode, never a score |
| The three cheap measurements, in order | Self-agreement (no labels); flip count under an arbitrary change (no labels); then the baseline (no judge needed) |
| The baseline | What "always pass" scores. 48 of 60 here, 80 per cent, finding nothing |
| The two numbers to report | Of the real failures, how many caught; of its alarms, how many real. 5 of 12 and 5 of 7 for judge A |
| Their interview names | Recall is the share of real failures caught; precision the share of alarms that are real. Chapter 26's recall@k is a different quantity — relevant documents reaching the top k |
| Why one number hides it | 48 of 60 cases are passes, so agreement is mostly agreement about passes. Judge B caught 10 of 12 against A's 5 and scored 82 against 85 |
| How many cases to label | Enough *failures*, not enough cases. 60 labels bought 12 failures; the catch rate's interval was 12% to 73% |
| Position bias, measured | Show each pair both ways and count the flips: 16 of 40 here, a 70%-against-30% swing in the headline |

### Review Questions

1. When do you use a model as a judge rather than code?
2. How do you establish that a judge can be trusted?
3. What is position bias, and what does it do to your numbers?
4. Your judge agrees with your labels 92 per cent of the time. What do you ask next?
5. You tighten a judge's instructions and its agreement figure falls. What has probably happened,
   and how would you check?

### Review Answers

1. When the check needs a decision about what text *means*, and not before. The test is
mechanical: look at what the check needs in order to return a verdict. If it is a comparison
between two things that are both literally present — a filename against a list of filenames, a
quote against a document, an offset against a slice, a digit against a question — then code
decides it, and code is cheap, identical every time, and has no verdict of its own that you have
to validate. If it needs entailment, aboutness or tone, there is no substring test and you
need a judgement. The part people get wrong is treating this as a whole-mode decision: of the
eight failure modes in the chapter's example, six split across the two columns and **seven have
some part code can decide**. *Invents a detail* is the clearest case — a regular expression finds
every phone number and email and tests each against the passages, which is two of that mode's
six failures for an afternoon, and only "every *claim* supported by a passage" is left for a judge. So the practical
rule is: run the cheap part first, because every model judgement you add is a second thing that
can be wrong, and its errors land in your numbers looking exactly like findings about your
application.
2. By measuring it as a thing that sorts answers into two groups, against groups you made by
hand — and in a particular order, because the cheap measurements come first and often end the
exercise. **Self-agreement first**: show it the same answer twice and count. It needs no labels,
and a judge that changes its mind cannot be validated, only fixed; in the chapter's example A held
its verdict on 17 of 20, and one of the three flips was a failure it had caught, so "5 of 12"
could equally have printed as "4 of 12". **Then the flip count under any arbitrary change** —
order of two answers, order of passages, naming of options — which also needs no labels.
**Only then label by hand** — and the first thing to compute from those labels is the
**baseline**: what a judge that always says pass would score, 48 of 60 or 80 per cent here, so
judge A's 85 per cent is five points of value and not eighty-five. Then report two numbers rather
than one: of the real failures how many it caught
(5 of 12), and of its alarms how many were real (5 of 7). Neither is deducible from the 85.
Finally, put Chapter 20's interval on both and expect them to be wide — 12 to 73 per cent on the
catch rate here — because the catch rate rests on the twelve cases you called fail and not on the
sixty.
3. A judge preferring an answer for where it was printed rather than for what it says. What it
does to your numbers is best said with the example: the same judge, the same forty pairs, the same
answers, printed in two orders, reports a 70 per cent win rate for the new answer when the new
answer comes first and 30 per cent when it comes second. **A 40-point swing with nothing changed
but the order**, and whichever order you happened to run is the figure you would have reported,
with nothing in the output looking wrong. The measurement is the flip count: show every pair both
ways and count the pairs where the verdict changed — 16 of 40 here, all of them to whichever
answer came first. That count is what you cannot see by running one order, and it does not care
which direction the bias runs — step 8 of the lab reverses the direction and the count does not
move. The repairs both work and neither is free: keeping only
the consistent pairs gives 50 per cent but discards 40 per cent of your data and assumes the
flipped pairs are not systematically different, while scoring each flipped pair half to each side
keeps everything and dilutes every real result towards a tie. They agree on this set and they need
not in general. The honest report is two numbers — agrees with me on 20 of the 24 pairs it held a
verdict on, no verdict on the other 16 — and the same procedure applies to any arbitrary element
of a judge's prompt, not just to pairs.
4. What the baseline is — and nothing else until that is answered. Ninety-two per cent sounds
strong and may be worth nothing: if the application fails on 8 per cent of the set, a judge that
says pass to everything also scores 92, and finds nothing. So the first question is how often your
own labels say fail, because that single figure is mostly a measurement of how often the
application is fine. Then split the 92 into the two numbers that matter: of the cases you labelled
fail, how many did the judge catch, and of its alarms, how many were real. Then ask how many
labelled *failures* are behind the first of those: if the set is sixty cases with twelve
failures, the catch rate rests on twelve and Chapter 20's interval round it will be wide enough to
be uninformative. And then the cheap one that should have come first: does the judge agree with
itself on the same answer twice? A judge at 92 per cent with your labels and 85 with itself has
not been measured, it has been sampled once.
5. Most likely the judge got better at the job and the single figure moved the wrong way, which it
can do whenever your set is mostly passes. Tightening usually makes a judge fail more answers, so
it catches more real failures and raises more false alarms — and when the extra false alarms
outnumber the extra catches, as they easily do on a set with four times as many passes to
false-alarm on, they cost more agreement than the extra catches buy. The arithmetic is not about
weighting: every case counts the same either way, and a judge that never false-alarms has an
agreement figure that tracks its catch rate exactly, however many passes the set holds. The chapter's two
judges are exactly this: B caught 10 of 12 failures against A's 5, and its agreement fell from 85
to 82, because 48 of the 60 cases are passes. **How to check is the point of the answer**: split
both figures. If the catch rate rose and the alarm-accuracy fell, that is the trade and the only
remaining question is which error you can afford. If the catch rate did *not* rise, the tightening
did something else — and the first thing to check is self-agreement, which the chapter's own
set does not record for judge B — only for A — and which is the first column I would add: the
same answer shown twice will tell you within the hour whether the new instruction made the judge
less certain rather than more exact. The thing not to do is revert on the single
figure, which cannot distinguish a judge that got worse from one that got better in the direction
you built it for.

> **You understand this when** you can say what the baseline is before quoting any agreement
> figure, and name the two measurements worth making before you label a single case.
