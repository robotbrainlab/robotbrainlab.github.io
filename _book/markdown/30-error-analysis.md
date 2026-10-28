# Error Analysis: Naming the Failure Modes

Chapter 5 named this activity and said what it is: reading real outputs, sorting the failures
into kinds, and working on the largest kind. This chapter is the method. What you get for it is
a way to turn *sometimes bad* into a list with counts against it, a demonstration of what goes
wrong when the sorting is left to the wording of the notes, and the argument for letting your
own failures choose what you measure rather than measuring what everybody measures.

*The problem.* My application is "sometimes bad". That's all I can say about it, so I don't know
what to fix.

*The question.* How do you get from a feeling about an application to a list of things worth
fixing, in an order?

## "Sometimes Bad" Is Not a Finding

It is a report of a feeling, and the feeling is usually accurate. What it lacks is any of the
three things that would let you act: *which* kinds of wrong, *how often* each, and *which one is
worth a week*.

The method has four steps and the first one is the one people skip.

1. Read actual outputs. Not metrics, not summaries, not a dashboard — the text your application
   produced, beside the input that produced it.
2. Write one short note on each failure, in your own words, *before* you have any categories.
3. Group the notes into a small set of named kinds — each one a **failure mode** — and count
   them.
4. Let those modes decide what you measure.

Here is step 1 and step 2 already done, on a support-answering application.

```python
"""Forty failures from a support-answering application, each with the
one-line note a person wrote after reading the output.

The notes are the raw material of this chapter. They were written while
reading outputs, before anybody knew what the categories would be -
which is the point, and why they are untidy.
"""

NOTES = [
    "said refunds take 7 days, the policy says 14",
    "quoted the cancellation fee for a refund question",
    "answered about shipping when asked about returns",
    "cited policy.pdf but the quote is not in it",
    "said 'within 14 days' without saying what takes 14 days",
    "invented a phone number",
    "refused, said it had no information, the passage was there",
    "answered in German, the question was English",
    "said refunds take 30 days, no idea where from",
    "gave the fee as 10% then said 15% two lines later",
    "cited the right document, wrong paragraph",
    "answered about returns when asked about shipping",
    "said 'contact support' instead of answering",
    "quoted a passage that was about a different product",
    "refused because the question mentioned a competitor",
    "invented an email address for the returns team",
    "said the policy was updated last week, no such thing",
    "cited shipping.pdf for a refund answer",
    "gave three different delivery times in one answer",
    "answered the question asked two turns earlier",
    "said refunds are instant, policy says 14 days",
    "told the user to read the attached policy, nothing attached",
    "quoted the right sentence, attached it to the wrong claim",
    "refused, cited a safety policy that does not apply",
    "said 'approximately 14 days' where the policy says exactly 14",
    "answered in a formal register, the brand voice is casual",
    "invented a case reference number",
    "said the fee is waived for members, no such rule anywhere",
    "cited a document that does not exist",
    "gave the UK policy to a US customer",
    "answered about the old policy, the new one was in the passages",
    "refused to give a figure that is in the passages",
    "said 'I cannot access that document' about a supplied passage",
    "listed four steps, the policy has three",
    "contradicted itself on whether postage is refunded",
    "invented a manager's name to escalate to",
    "quoted the FAQ instead of the policy on a legal question",
    "answered a different customer's question from the history",
    "said refunds take 14 working days, policy says 14 days",
    "gave an answer with no citation at all",
]

if __name__ == "__main__":
    print(f"  {len(NOTES)} failures, read and noted one at a time\n")
    for i, n in enumerate(NOTES[:6], 1):
        print(f"    {i:2d}. {n}")
    print(f"    ... and {len(NOTES) - 6} more\n")
    print("  There is no structure here yet. That is correct: the")
    print("  notes come first and the categories come out of them.")
```

```text
  40 failures, read and noted one at a time

     1. said refunds take 7 days, the policy says 14
     2. quoted the cancellation fee for a refund question
     3. answered about shipping when asked about returns
     4. cited policy.pdf but the quote is not in it
     5. said 'within 14 days' without saying what takes 14 days
     6. invented a phone number
    ... and 34 more

  There is no structure here yet. That is correct: the
  notes come first and the categories come out of them.
```

**The notes are untidy on purpose, and that is the whole discipline of step 2.** They were
written while reading, one at a time, by somebody who did not yet know what the categories would
be. Had the categories existed first, the notes would have been pushed into them — and the
categories you start with tend to be the ones you already believe in, which is exactly what
error analysis is for escaping.

> **Tip:** Forty is a working number rather than a magic one: enough that a real pattern repeats
> and few enough to read in an afternoon. If you have thousands of failures, take forty at
> random, because the forty somebody complained about are not a sample of your failures — they
> are a sample of what annoyed somebody enough to write in, and the mode shares you get from
> them are that selection's shares rather than your application's.

## Grouping Is Judgement, Not String Matching

Step 3 is where people reach for a program, so it is worth seeing a program try.

```python
"""Why the grouping cannot be read off the notes, shown by trying."""
import collections
from group import MODE
from notes import NOTES

# The verb each note opens with is the obvious thing to group on, and
# it is the thing a program can see without understanding anything.
VERBS = ["cited", "quoted", "invented", "refused", "said", "answered",
         "gave", "told", "listed", "contradicted"]

def by_verb():
    out = collections.defaultdict(list)
    for i, note in enumerate(NOTES):
        verb = next((v for v in VERBS if v in note), "other")
        out[verb].append(i)
    return out

TRUTH = {i: mode for mode, idx in MODE.items() for i in idx}

if __name__ == "__main__":
    groups = by_verb()
    print(f"  grouping on the verb gives {len(groups)} groups,"
          f" against 8 real modes\n")
    print("  verb           notes   real modes in it")
    for verb, idx in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        modes = {TRUTH[i] for i in idx}
        tag = "one" if len(modes) == 1 else f"{len(modes)}  <- mixed"
        print(f"  {verb:13s} {len(idx):4d}    {tag}")

    mixed = sum(1 for idx in groups.values()
                if len({TRUTH[i] for i in idx}) > 1)
    split = sum(1 for idx in MODE.values()
                if len({next((v for v in VERBS if v in NOTES[i]), "other")
                        for i in idx}) > 1)
    print(f"\n  groups holding more than one real mode: "
          f"{mixed} of {len(groups)}")
    print(f"  real modes split across groups:          "
          f"{split} of {len(MODE)}")

    print("\n  It fails in both directions at once, which is the")
    print("  point. 'said' collects five different modes because")
    print("  almost every failure is something the model said. And")
    print("  one mode is spread over 'cited', 'quoted' and 'gave',")
    print("  because the same kind of wrong gets described three")
    print("  ways by the person writing the notes.\n")
    print("  Deciding that two notes are the same kind of wrong")
    print("  needs somebody who read both outputs. The notes")
    print("  are a record of that reading, not a substitute.")
```

```text
  grouping on the verb gives 10 groups, against 8 real modes

  verb           notes   real modes in it
  said            11    5  <- mixed
  answered         7    3  <- mixed
  cited            5    2  <- mixed
  quoted           4    2  <- mixed
  invented         4    one
  refused          3    one
  gave             3    3  <- mixed
  told             1    one
  listed           1    one
  contradicted     1    one

  groups holding more than one real mode: 5 of 10
  real modes split across groups:          6 of 8

  It fails in both directions at once, which is the
  point. 'said' collects five different modes because
  almost every failure is something the model said. And
  one mode is spread over 'cited', 'quoted' and 'gave',
  because the same kind of wrong gets described three
  ways by the person writing the notes.

  Deciding that two notes are the same kind of wrong
  needs somebody who read both outputs. The notes
  are a record of that reading, not a substitute.
```

**It fails in both directions at the same time, which is what makes the demonstration worth
having.** Five of the ten verb groups hold more than one real failure mode — *said* alone
collects five of them, because almost every failure is something the model said. And six of the
eight real modes are split across verb groups, because the same kind of wrong gets written down
three different ways by the person taking the notes: *Citation does not support* appears under
*cited*, *quoted* and *gave*.

**So the grouping is a judgement about what the failures have in common**, and what they have in
common is not reliably in the words of the note. It is in the two outputs the note-taker read. A program
working from the notes has only their wording to go on, and the demonstration above is what
that gets you.

> **Warning:** This is the step that gets delegated to a model, and the delegation is worth
> thinking about rather than refusing. A model can propose groupings and will do it quickly.
> What it cannot do is notice that two failures share a *cause* it has not been told about,
> which is the thing you are reading for. Chapter 31 is where a model's judgements get checked
> before you rely on one, and that order — check it, then rely on it — is the whole of the
> advice.

## A Small Set, With Counts

```python
"""Grouping the notes into named failure modes, and counting them.

A PERSON did the grouping. The program only counts and sorts, because
deciding that two notes are the same kind of wrong is the judgement
this chapter is about and no program working from the notes makes
it for you.
"""
from notes import NOTES

# note index -> the mode a person put it in, after reading all forty
MODE = {
    "Contradicts the passage": [0, 8, 13, 20, 24, 29, 30, 33, 38],
    "Citation does not support": [1, 3, 10, 17, 22, 28, 36, 39],
    "Invents a detail": [5, 15, 16, 26, 27, 35],
    "Refuses when the answer is there": [6, 14, 23, 31, 32],
    "Answers a different question": [2, 11, 19, 37],
    "Contradicts itself": [9, 18, 34],
    "Not an answer at all": [4, 12, 21],
    "Wrong register or language": [7, 25],
}

def counts():
    return sorted(((len(v), k) for k, v in MODE.items()), reverse=True)

if __name__ == "__main__":
    assigned = sorted(i for v in MODE.values() for i in v)
    print(f"  {len(assigned)} notes assigned to {len(MODE)} modes")
    print(f"  every note used exactly once? "
          f"{assigned == list(range(len(NOTES)))}\n")

    total = len(NOTES)
    running = 0
    print("  mode                               n    share   running")
    for n, name in counts():
        running += n
        print(f"  {name:33s} {n:2d}   {n/total:5.0%}    {running/total:5.0%}")

    print(f"\n  the top three are {sum(n for n, _ in counts()[:3])}"
          f" of {total}. That is where the work is.")
    print("  the bottom three are 8 of 40 between them, and none of")
    print("  them on its own would repay a week.")

    print("\n  one note from each of the top two, to show they really")
    print("  are different kinds of wrong:")
    for name in ("Contradicts the passage", "Citation does not support"):
        print(f"    {name}:")
        print(f"      {NOTES[MODE[name][0]]!r}")
```

```text
  40 notes assigned to 8 modes
  every note used exactly once? True

  mode                               n    share   running
  Contradicts the passage            9     22%      22%
  Citation does not support          8     20%      42%
  Invents a detail                   6     15%      57%
  Refuses when the answer is there   5     12%      70%
  Answers a different question       4     10%      80%
  Not an answer at all               3      8%      88%
  Contradicts itself                 3      8%      95%
  Wrong register or language         2      5%     100%

  the top three are 23 of 40. That is where the work is.
  the bottom three are 8 of 40 between them, and none of
  them on its own would repay a week.

  one note from each of the top two, to show they really
  are different kinds of wrong:
    Contradicts the passage:
      'said refunds take 7 days, the policy says 14'
    Citation does not support:
      'quoted the cancellation fee for a refund question'
```

**Three things about that table matter more than the numbers in it.**

**The modes are named after what went wrong, not after a part of the system.** *Contradicts the
passage* is a description of an output. "Retrieval problem" would be a guess at a cause, and
naming a mode after a guess means every count afterwards is a count of your guess. The causes
come later, and some modes turn out to have two.

**The counts are the point, and they are cheap.** Twenty-two per cent against five per cent is
the difference between a fortnight that moves the application and a fortnight that does not.
Without counts, every mode is a candidate and the one you fix is the one that annoyed you most
recently.

**And `every note used exactly once? True` is not decoration.** It is the check that the
grouping is a **partition** rather than a set of labels — that no note was quietly dropped because
it fitted nowhere, and none counted twice because it fitted twice. A note that fits nowhere is easy to lose — it gets
left for later and then forgotten — which is exactly what that line is for.

> **Note:** Eight modes is more than this chapter would like. The useful target is five or six,
> because a list you cannot hold in your head is a list you will not use — and the bottom three
> here are candidates for merging or for being set aside as "known and rare". Resist merging the
> top ones to tidy the list, though: *Contradicts the passage* and *Citation does not support*
> are both about a passage and they are fixed in completely different places.

## Letting the Modes Choose the Metrics

Now step 4, which is the chapter's real claim and the thing most commonly done backwards.

```python
"""Letting the failure modes choose the metrics.

Five checks you might build, and which of this application's forty
actual failures each one would catch. Marked failure by failure, not
mode by mode, because a check catches failures and a mode is a group
of them - so most checks cover a mode only in part.
"""
from group import MODE
from notes import NOTES

ALL = set(range(len(NOTES)))

# A score is not a check: it returns a number, not a decision about a
# failure, so it has no set. That is the point of its row.
CHECKS = [
    ("A 1-to-5 quality score from a model", None),
    ("Exact match against a reference answer", set(ALL)),
    ("Every claim supported by a passage",
     {0, 3, 5, 8, 9, 15, 16, 17, 18, 20,
      22, 26, 27, 28, 30, 33, 34, 35, 37, 38}),
    ("Chapter 28's three citation checks", {3, 10, 28}),
    ("A refusal detector", {6, 12, 14, 21, 23, 31, 32}),
]

# The three usable ones: when one of these fires it says WHAT is
# wrong with the answer, not merely that something is. A score says
# 3.2 and exact match says 'not the reference', and neither tells
# you which of eight things happened.
ACTIONABLE = [2, 3, 4]

TRUTH = {i: m for m, idx in MODE.items() for i in idx}

def full_modes(caught):
    return [m for m, idx in MODE.items() if set(idx) <= caught]

if __name__ == "__main__":
    for _, s in CHECKS:
        assert s is None or s <= ALL
    total = len(NOTES)
    print(f"  {total} failures in {len(MODE)} modes\n")
    print("  check                                   caught  modes full")
    for name, s in CHECKS:
        if s is None:
            print(f"  {name:38s}      -       -")
            continue
        print(f"  {name:38s} {len(s):3d} {len(s)/total:4.0%}"
              f"  {len(full_modes(s)):3d}")

    print("\n  Read the rows from the bottom up.\n")
    print("  A refusal detector and the claim-support check each")
    print("  cover a whole mode, which is what makes them worth")
    print("  building. Chapter 28's three mechanical citation")
    print("  checks catch 3 of the 8 failures in the one mode they")
    print("  are for, because chapter 28 says so itself: they are")
    print("  necessary and not sufficient. A citation can name a")
    print("  real document, quote it exactly, at the right offset,")
    print("  and still not support the sentence it is attached to.")

    print("\n  Exact match catches all 40 and is useless, which is")
    print("  the row to think hardest about. Every failure differs")
    print("  from the reference answer - and so does every correct")
    print("  answer worded differently. Coverage is not the test;")
    print("  chapter 31 is where firing ONLY on failures gets")
    print("  measured.")

    print("\n  The 1-to-5 score has no number in its row at all.")
    print("  It returns a 3.2, not a decision about a failure, so")
    print("  there is nothing to count and nothing to fix.")

    real = [CHECKS[i] for i in ACTIONABLE]
    best = max(real, key=lambda kv: len(kv[1]))
    print(f"\n  Best of those: '{best[0]}'")
    print(f"  at {len(best[1])} of {total}. Perfect it - never miss, never")
    print(f"  false-alarm - and {total - len(best[1])} of your failures are")
    print("  untouched.")

    union = set().union(*(s for _, s in real))
    left = sorted(ALL - union)
    print(f"\n  All {len(real)} together: {len(union)} of {total}"
          f" ({len(union)/total:.0%}).")
    print(f"  {len(left)} failures left, in these modes:")
    for m, idx in MODE.items():
        miss = [i for i in idx if i in left]
        if miss:
            tag = "  <- none covered" if len(miss) == len(idx) else ""
            print(f"    {m:33s} {len(miss)} of {len(idx)}{tag}")
    print("\n  That is the honest list of what you cannot yet")
    print("  measure, and it is worth writing down as it stands.")
```

```text
  40 failures in 8 modes

  check                                   caught  modes full
  A 1-to-5 quality score from a model         -       -
  Exact match against a reference answer  40 100%    8
  Every claim supported by a passage      20  50%    2
  Chapter 28's three citation checks       3   8%    0
  A refusal detector                       7  18%    1

  Read the rows from the bottom up.

  A refusal detector and the claim-support check each
  cover a whole mode, which is what makes them worth
  building. Chapter 28's three mechanical citation
  checks catch 3 of the 8 failures in the one mode they
  are for, because chapter 28 says so itself: they are
  necessary and not sufficient. A citation can name a
  real document, quote it exactly, at the right offset,
  and still not support the sentence it is attached to.

  Exact match catches all 40 and is useless, which is
  the row to think hardest about. Every failure differs
  from the reference answer - and so does every correct
  answer worded differently. Coverage is not the test;
  chapter 31 is where firing ONLY on failures gets
  measured.

  The 1-to-5 score has no number in its row at all.
  It returns a 3.2, not a decision about a failure, so
  there is nothing to count and nothing to fix.

  Best of those: 'Every claim supported by a passage'
  at 20 of 40. Perfect it - never miss, never
  false-alarm - and 20 of your failures are
  untouched.

  All 3 together: 28 of 40 (70%).
  12 failures left, in these modes:
    Contradicts the passage           3 of 9
    Citation does not support         3 of 8
    Answers a different question      3 of 4
    Not an answer at all              1 of 3
    Wrong register or language        2 of 2  <- none covered

  That is the honest list of what you cannot yet
  measure, and it is worth writing down as it stands.
```

**Start with the row that catches everything, because it shows that coverage is not the test.**
Exact match against a reference answer fires on all forty failures and fully covers all eight
modes. It is also useless. Every failure differs from the reference answer — and so does every
correct answer worded differently, so a check that fires on everything has told you nothing
about which outputs are wrong. Catching failures and firing *only* on failures are two
different properties, and Chapter 31 is where the second one gets measured.

**Then the row with no number in it at all.** A model asked to score outputs out of five returns
a 3.2: a number, not a decision about a failure. There is nothing to count in its row because it
decides nothing, and nothing follows from it — a 3.2 does not say which of eight things went
wrong, so it cannot say what to fix. Threshold it at 3 and you do have a check — and still not
one that names a mode, so you are back where you started. Chapter 31 is about whether such a
score is even a reliable
*measurement*; what is wrong with it here is simpler, which is that it is not actionable.

**Now the three usable checks: when one of these fires it says *what* is wrong with the answer,
not merely that something is.** Two of them close a whole mode: the claim-support check covers *Invents a detail* 6 of 6 and *Contradicts itself* 3
of 3, and a refusal detector covers *Refuses when the answer is there* 5 of 5. A mode a check
closes rather than dents is what makes the check worth a week.

**And the third row is a warning against reading a check's name instead of its coverage.**
Chapter 28's three mechanical citation checks — does the document exist, is the quote in it, is
it at the offset claimed — catch 3 of the 8 failures in *Citation does not support*, the one
mode they are named for. Chapter 28 says why itself: the three are necessary and not sufficient.
A citation can name a real document, quote it exactly, at the offset it claims, and still not
support the sentence it is attached to. Chapter 28 names three shapes that get past its three
checks, and the five failures here are of two kinds: four point at something real that does not
settle the claim, and one is an answer carrying no citation at all.

> **Note:** A check catches failures; a mode is a group of them. So the ordinary case is a mode
> covered in part, and the table has a column for it. Marking coverage mode by mode instead
> would have credited those citation checks with all eight failures and been wrong about five.
> It runs the other way too: a check reaches outside the mode it was built for, which is why the
> refusal detector's row says 7 while *Refuses when the answer is there* holds 5. It also catches
> two of the three *Not an answer at all* failures — a "contact support" and a "read the attached
> policy" with nothing attached.

**Then the arithmetic that answers the question.** The best of the three catches 20 of 40.
**Perfect it — get it to never miss and never false-alarm — and 20 of your failures are
untouched.** That is the cost of choosing a metric before you know your failures: you can
succeed completely at measuring half of them.

**And the modes tell you which checks to build, in order.** The claim-support check — the one
Chapter 32 builds — is the most coverage for one piece of work, at 20 failures, and it closes
two modes outright. A refusal
detector is seven more and nearly free. Chapter 28's citation checks are built already and worth
keeping for the 3 they catch, as long as nobody records them as covering the mode. All three
together reach 28 of 40, and the 12 left sit in five modes — with *Wrong register or language*
not covered at all.

**That is the answer to why the modes choose the metrics.** A conventional metric measures what
is conventional to measure, which is whatever the last application needed. Your modes are a
description of what *your* application does wrong, so a check derived from them is guaranteed to
be about a real failure — and the count tells you how much of your problem it covers before you
build it. It also tells you what no check of yours reaches, which is a gap you have written down
rather than one you have not noticed.

> **Warning:** The reverse order is seductive because the conventional metrics already exist.
> You can have a number this afternoon, a dashboard by Friday, and a quarter of careful work on
> something that was never your problem. The forty notes take an afternoon too, and they are
> what tells you which number to want.

## What To Actually Do

1. **Get enough real outputs, with their inputs, to give about forty failures** — sampled rather
   than selected. The ones somebody complained about are a sample of what annoyed somebody, not
   of your failures, so the shares you count from them are the wrong shares. Chapter 20's
   bootstrap rests on the same kind of assumption, stated out loud: that your cases are a sample
   of the input you care about.
2. **Read them and write one line per failure**, in your own words, with no categories in mind.
   Resist naming the categories while you read; you will be wrong and then committed.
3. **Group the notes only afterwards** and name each group after what went wrong, not after the part
   of the system you suspect.
4. **Count, and check the partition.** Every note in exactly one mode, nothing dropped, nothing
   double-counted.
5. **Aim for five or six modes.** Merge the small ones or set them aside explicitly; never merge
   two large ones that are fixed in different places.
6. **Work out what each mode would take to detect**, and let that list be your metrics. Build the
   check that covers the most failures per unit of work.
7. **Write down the modes you cannot measure**, so that the gap is a known gap rather than a
   silent one.
8. **Then fix the largest mode**, and keep the notes — Chapter 33 is about the cases that failed
   becoming the set you run on every change.

> **Tip:** The whole of steps 1 to 4 is an afternoon, and the output is a table with counts.
> That table is also the most persuasive artefact you can take to anybody who has to approve
> the work, because "twenty-two per cent of our failures are one thing and here are nine
> examples" is an argument, and "it's sometimes bad" is not.

## Lab: Forty Notes and a Table

Four programs, pure Python, nothing to install. About forty minutes, and there is a key for
every step. Work in a new empty folder.

**Step 1.** Save the first program as `notes.py` and run it. Then read all forty notes in the
source, which takes about three minutes. Everything after this refers to a note by its index in
`NOTES`, counting from 0, so note 7 is the eighth in the list — the program's own listing
numbers from 1, which is the one place the two disagree.

*Expected result:* forty notes and no structure. Before going on, write down on paper how many
distinct kinds of failure you think are in there. Keep the number.

**Step 2.** Save the *third* program as `group.py` — note that `bykeyword.py` imports from it, so
save this one first — and run it.

*Expected result:* eight modes, the top three holding 23 of 40, and
`every note used exactly once? True`. Compare the eight against the number you wrote down in
step 1.

**Step 3.** Break the partition deliberately: remove `33` from `"Contradicts the passage"` and
run it again.

*Expected result:* `39 notes assigned` and `every note used exactly once? False`. That is the
check earning its place, and the failure it catches is the one nothing else in the method would
show you: a note left behind.

**Step 4.** Put it back, then move one note between two modes — take `13` out of *Contradicts
the passage* and put it in *Citation does not support* — and run it.

*Expected result:* the counts change, the partition check still passes, and nothing warns you.
**A partition check cannot tell you the grouping is right, only that it is a grouping.** Note
13 is *"quoted a passage that was about a different product"*, and you can argue it either way;
that argument is the work, and the protection against getting it wrong is a second person
reading the same notes, or a written criterion for each mode that a note can be tested against.
Note 24 is a second case you can argue: *"approximately 14 days"* where the policy says exactly
14 is a loss of precision rather than a contradiction, and nothing in the table says so.

**Step 5.** Save the *second* program as `bykeyword.py` and run it.

*Expected result:* ten verb groups against eight real modes, five groups mixed, six modes split.
Then find the mode that is split across *cited*, *quoted* and *gave* for yourself.

**Step 6.** In `bykeyword.py`, add more verbs to `VERBS` — try `"stated"`, `"claimed"`,
`"wrote"` — and run it again.

*Expected result:* nothing improves. None of those words appears in the notes, so the groups are
identical. The problem was never the vocabulary; it is that the verb a note starts with is not
what the failure has in common with other failures.

**Step 7.** Save the fourth program as `metrics.py` and run it.

*Expected result:* no number at all against the 1-to-5 score, 100 per cent against exact match,
50 per cent against the claim-support check, and *Wrong register or language* uncovered by any
of them. Before step 8, decide for yourself which row you would build from.

**Step 8.** In `metrics.py`, add a check of your own to `CHECKS` — "the answer is in the
question's language", which catches note 7 and nothing else — and add its position to
`ACTIONABLE`.

*Expected result:* 1 failure, 2 per cent, 0 modes closed, and the three together become four at
29 of 40. Two things are worth noticing. The check is trivial to build and it is still the right
thing to build *last*, which the `caught` column makes obvious and intuition does not. And it does *not*
close *Wrong register or language*, which drops from 2 of 2 uncovered to 1 of 2: note 25 is a
register failure in the right language, so the obvious check for the mode's name covers half of
it.

**Step 9.** Now do it backwards, which is the thing the chapter warns against. Pick a metric
first — "the answer should be under 100 words" — and work out which of the eight modes it
catches.

*Expected result:* none of them. Not one of the forty failures is about length. You could
measure it for a quarter, report it weekly, improve it, and change nothing — which is the whole
argument of this chapter in one made-up metric.

**Step 10.** Write the first three notes for your own application.

*Expected result:* three lines in your own words, or the discovery that you are not keeping
failures anywhere. If it is the second, that is the finding, and the first step is to start
keeping them.

## Summary, Key Terms, and Review Questions

### Summary

*Sometimes bad* is a report of a feeling, and it lacks the three things that let you act: which
kinds of wrong, how often each, and which is worth a week. The method has four steps. **Read
real outputs** beside their inputs — not metrics, not a dashboard. **Write one short note per
failure in your own words, before you have any categories**, because the categories you start
with tend to be the ones you already believe and escaping those is what the exercise is for. **Group the
notes afterwards and count.** **Then let the modes choose what you measure.**

**The grouping is a judgement about the outputs rather than about the notes' wording, and the
chapter shows a program grouping on the wording and failing in both directions at once.** Grouping the forty notes on their opening verb gives ten groups against
eight real modes: five of the ten hold more than one real mode — *said* alone holds five, because
almost every failure is something the model said — and six of the eight real modes are split
across verb groups, because the same kind of wrong gets written down three ways. *Citation does
not support* turns up under *cited*, *quoted* and *gave*. **What the failures have in common is
not reliably in the words of the note; it is in the outputs the note-taker read.** Five of the
ten verb groups hold notes from one mode only — though three of those hold a single note, and
not one of the five holds a whole mode — so the wording carries a little of the distinction, and
the other five hold several modes, which is why you cannot work from the wording alone.

The named modes come with counts, and three things about the table matter more than the numbers.
**Name a mode after what went wrong, not after the part of the system you suspect**, or every
count afterwards is a count of your guess. **The counts are the point and they are cheap** — 22
per cent against 5 per cent is the difference between a fortnight that moves the application and
one that does not. And `every note used exactly once? True` is a real check: it proves the
grouping is a *partition*, with nothing dropped and nothing double-counted — and a note that
fits nowhere is the one most easily left behind.

**Then the claim the chapter is for.** Marking the checks failure by failure rather than mode by
mode is what makes the table honest, because a check catches failures and a mode is a group of
them, so a mode covered in part is the ordinary case. Exact match against a reference answer
catches all forty and closes all eight modes, and is useless: every failure differs from the
reference and so does every correct answer worded differently, so **coverage is not the test**.
A 1-to-5 score has no number in its row at all, because it returns a 3.2 rather than a decision
about a failure. Of the three usable checks — the ones that, when they fire, say *what* is wrong
rather than only that something is — the best catches 20 of 40. **Perfect it and 20 failures
are untouched**, which is the cost of choosing a metric before knowing your failures. Read the other way, the modes say what to build: the
claim-support check, which Chapter 32 builds, is 20 failures for one piece of work and closes
*Invents a detail* and *Contradicts itself* outright, and a refusal detector is seven more and nearly free. Chapter
28's three mechanical citation checks catch 3 of the 8 failures in the mode they are named for,
which is Chapter 28's own point that they are necessary and not sufficient — and crediting them
with the mode would have been wrong about five failures. All three together reach 28 of 40, and
the 12 left sit in five modes with *Wrong register or language* untouched, which you write down
rather than inventing a metric for. A conventional metric measures what was conventional for
somebody else's application; a check derived from your modes is guaranteed to be about a real
failure, with its coverage known before you build it.

### Key Terms

| Term | Meaning |
|---|---|
| **Failure mode** | A named kind of wrong output, named after what went wrong rather than after the part of the system suspected of causing it |
| **Partition** | Every failure in exactly one mode, nothing dropped and nothing counted twice. Checkable, and worth checking |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The four steps | Read outputs; note each failure; group and count; let the modes choose the metrics |
| Why the notes come first | Categories you start with tend to be the ones you already believe, and the exercise exists to escape them |
| How many failures | Forty is a working number: enough for a pattern to repeat, few enough to read in an afternoon. Sampled, not selected |
| Why the verb grouping fails | It failed both ways on verbs: 5 of 10 groups held several modes, and 6 of 8 modes were split across groups |
| How to name a mode | After the output, never after the suspected cause. "Contradicts the passage", not "retrieval problem" |
| The check on the grouping | Every note in exactly one mode. It proves a partition, and not that the partition is right |
| What a 1-to-5 score gives you | A number, not a decision about a failure. It may correlate with quality and still name no mode |
| The cost of a metric chosen first | The best actionable check here covers 20 of 40. Perfect it and 20 failures remain |
| Which check to build first | The one covering the most failures per unit of work — one check here was 20 failures and closed two modes |

### Review Questions

1. You have forty bad outputs and no metrics. What do you do first?
2. Why let the failure modes choose the metrics rather than measuring what is conventional?
3. Why can a program working from the notes alone not do the grouping for you?
4. Your error analysis produces fourteen failure modes. What has gone wrong?
5. Somebody proposes scoring every answer out of five with a model. What do you say?

### Review Answers

1. Read them, with their inputs, and write one line per failure in my own words — and the part
worth emphasising is **before** having any categories. The categories you start with tend to be the ones
you already believe in, so writing them first turns the exercise into confirming what you
suspected; the notes have to be untidy at this stage and that is correct. Then group the notes,
name each group after **what went wrong** rather than the part of the system I suspect, count
them, and check that the result is a partition — every note in exactly one mode, nothing dropped
and nothing counted twice. The counts are what I actually came for: in the chapter's example the
top three of eight modes held 23 of 40 failures, and the bottom three held 8 between them, so
one fortnight is worth spending and another is not. Two details that show the method has been
used rather than read: sample the forty rather than taking the ones somebody complained about,
because the complaints are a sample of what annoyed
somebody rather than of your failures, and expect to land on five or six modes rather than
fifteen. Then and only then work out what each mode would take to detect.
2. Because a conventional metric measures what was conventional for somebody else's application,
and the cost of that is arithmetic rather than aesthetic. In the chapter's example the best of the
three usable checks covers 20 of 40 — so **you could perfect
it, never miss and never false-alarm, and leave 20 of your failures completely untouched.** That
is what choosing a metric before knowing your failures buys. Read the other way, the modes tell
you what to build and in what order: "every claim supported by a passage" is 20 failures for one
piece of work and closes two modes outright, *Invents a detail* and *Contradicts itself*, while
a refusal detector is seven more and nearly free. Two details show the table has been used
rather than recited. The first is that a check catches *failures*, not modes, so coverage has to
be marked failure by failure: Chapter 28's three mechanical citation checks sound like the whole
of *Citation does not support* and catch 3 of its 8, which is Chapter 28's own point that they
are necessary and not sufficient. The second is that the check with the best coverage of all is
the worthless one — exact match catches every failure and every correct paraphrase too, so
coverage alone was never the criterion. And the modes tell you what you *cannot* measure: 12
failures survive all three checks, with *Wrong register or language* untouched, which becomes a
written-down gap instead of a silent one. A check derived from your own modes is guaranteed to
be about a real failure with its coverage known before you build it, and a conventional metric
chosen before the analysis has neither.
3. Because what the failures have in common is not reliably in the words of the notes — it is in
the outputs the note-taker read, and the notes record only part of what the reader saw. The chapter demonstrates it rather than asserting it: group the
forty notes on their opening verb and it **fails in both directions at once.** Five of the ten
verb groups hold more than one real failure mode, with *said* alone holding five, because almost
every failure is something the model said. And six of the eight real modes are split across verb
groups, because one person writing notes describes the same kind of wrong three different ways —
*Citation does not support* appears under *cited*, *quoted* and *gave*. Adding more verbs does
not help, because the problem was never the vocabulary. What a program can do is count the
groups and check the partition; what it cannot do is see the outputs the notes were written
from. On delegating it to a
model: a model will propose groupings quickly, and what it cannot do is notice that two failures
share a cause nobody has named yet, which is the thing you are reading for — so check its
judgements first, which is Chapter 31.
4. Probably nothing is wrong with the reading; the grouping has stopped before it finished.
Fourteen modes usually means the groups are describing *symptoms* rather than kinds — two notes
about a wrong date and a wrong fee are one mode, not two — or that the naming has crept toward
the specific, so each mode holds one or two notes and the counts cannot distinguish anything.
The target is five or six, for a plain reason: a list you cannot hold in your head is a list you
will not use. So merge the small ones, or set them aside explicitly as known and rare, and keep
the count of what you set aside. **But do not merge two large modes to tidy the list.** The
chapter's top two are both about a passage and sound similar — *Contradicts the passage* and
*Citation does not support* — and they are fixed in completely different places, so merging them
would produce a mode of 17 failures with no single fix and would have destroyed the only
information the table carries. If after merging you still have fourteen that each resist merging,
the honest conclusion is that the application has more than one serious problem and the counts
are the thing to argue from.
5. That it may well give a number that moves in roughly the right direction and will not tell
them what to fix, and the way to show that is the mode table rather than an opinion. In the chapter's
example a one-to-five score has no coverage figure at all, because it returns a 3.2 rather than
a decision about a failure — not because the scores are random, but because a single number
cannot say *which* of eight things went wrong, so nothing follows from it. Then separate the two objections, because they are usually run together. The
one that belongs here is that it is **not actionable**: a score of 3.2 is not a thing you can
work on. The other is whether the score is even a reliable measurement — whether it
agrees with a person, which is Chapter 31's, where a judge gets validated before anybody relies
on it, and whether the same output gets the same score twice, which is Chapter 20's repeated
runs. So the reply is not "never use
a model to judge", it is: run the error analysis first, so you know what the modes are; build
pass-or-fail checks per mode rather than a score; use code wherever code can decide; and keep the
model for the modes that genuinely need judgement, after you have checked that its judgement
agrees with yours.

> **You understand this when** you can say why the notes have to be written before the categories
> exist, and give the arithmetic for what a metric chosen before an error analysis costs you.
