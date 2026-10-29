# Evaluating an Agent

Chapters 30 to 33 built a measurement: named failure modes, checks and judges, the two halves
of a grounded answer, and a set that survives time. Every one of them measures *one call*.
Chapters 34 to 37 then built things that make many calls — fixed paths, a loop with its
context and its tools, several agents at once — and each of them left the same question
standing. Chapter 37 named it on its way out: the real question is whether the system does
the task.

This chapter answers it, and the answer starts by refusing the number in the problem.

*The problem.* My agent succeeded four times out of five. I don't know whether that is good.

*The question.* What is the unit you measure an agent on, who decides whether a run worked,
and what does a success rate hide?

## Four Out of Five of What?

Chapter 20's unit was a *case*: one input, plus whatever marks the answer right or wrong. An
agent needs more than an input, because it acts. Its unit is a **task** — a starting state, a
goal, and a condition that can be checked when the run ends. One run of the agent on one task
is one of Chapter 20's *trials*, and the word carries over unchanged.

With those two words, *four out of five* stops being one number. This program takes it two ways:
first as one task run five times, and then as a whole grid of tasks and trials, which on its own
yields three different figures.

```python
"""What "it succeeded four times out of five" can mean.

Two parts. The first asks what one task run five times can tell you.
The second takes a whole grid of tasks and trials and reads three
different numbers out of it, any of which somebody would report as
four out of five.
"""

from math import comb

TRIALS = 5
SEEN = 4

#   trials passed out of 5, how many tasks did that
SHAPES = [(5, 9), (4, 3), (3, 2), (1, 2), (0, 4)]
TASKS = [passed for passed, n in SHAPES for _ in range(n)]


def at_least(p, k, n):
    """Chance of seeing k or more successes in n trials at rate p."""
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))


if __name__ == "__main__":
    print(f"  ONE task, {TRIALS} trials, {SEEN} passed.\n")
    print(f"  For each true per-trial rate, the chance of seeing")
    print(f"  {SEEN} or more of {TRIALS}:\n")
    for p in (0.30, 0.50, 0.65, 0.80, 0.90, 0.95):
        print(f"    true rate {p:.2f}   {at_least(p, SEEN, TRIALS):.3f}")

    half = at_least(0.50, SEEN, TRIALS)
    print(f"\n  Read the 0.50 row. A system that works half the time")
    print(f"  shows you {SEEN} of {TRIALS} or better {half:.1%} of the time -")
    print(f"  about one attempt in {round(1/half)}. So this result does not")
    print("  tell a coin from a good system. A different result")
    print("  from the same five trials might: 0 of 5 rules the")
    print(f"  0.95 row out at {(1-0.95)**5:.1e}.\n")

    n = len(TASKS)
    runs = n * TRIALS
    passed = sum(TASKS)
    ever = sum(1 for t in TASKS if t > 0)
    always = sum(1 for t in TASKS if t == TRIALS)

    print(f"  Now a whole grid: {n} tasks, {TRIALS} trials each,"
          f" {runs} runs.\n")
    for p, count in SHAPES:
        print(f"    {count:2d} task(s) passed {p} of {TRIALS}")

    print(f"\n  Three numbers, one grid:\n")
    print(f"    trials that passed          {passed:3d} of {runs}"
          f"   {passed/runs:.2f}")
    print(f"    tasks that passed at least  {ever:3d} of {n:3d}"
          f"   {ever/n:.2f}   <- pass@{TRIALS}")
    print(f"    tasks that passed every     {always:3d} of {n:3d}"
          f"   {always/n:.2f}   <- pass^{TRIALS}")

    print(f"\n  The spread between the highest and the lowest is")
    print(f"  {(ever - always)/n:.2f} on the same {runs} runs. Nothing was measured")
    print("  twice and nothing is wrong with any of the three; they")
    print("  answer different questions. Which one somebody reports")
    print("  is the whole of what 'four out of five' tells you, and")
    print(f"  the highest of the three is {ever/n:.2f}.\n")

    mid = [t for t in TASKS if 0 < t < TRIALS]
    print(f"  One more thing the grid shows and a rate cannot:")
    print(f"  {len(mid)} of the {n} tasks came out both ways across the")
    print(f"  {TRIALS} trials. {always} never failed and {n - ever} never passed.")
    print("  The never-passed tasks are work. The both-ways tasks")
    print("  are a different kind of work, and a single number")
    print("  puts them in the same pile.")
```

```text
  ONE task, 5 trials, 4 passed.

  For each true per-trial rate, the chance of seeing
  4 or more of 5:

    true rate 0.30   0.031
    true rate 0.50   0.188
    true rate 0.65   0.428
    true rate 0.80   0.737
    true rate 0.90   0.919
    true rate 0.95   0.977

  Read the 0.50 row. A system that works half the time
  shows you 4 of 5 or better 18.8% of the time -
  about one attempt in 5. So this result does not
  tell a coin from a good system. A different result
  from the same five trials might: 0 of 5 rules the
  0.95 row out at 3.1e-07.

  Now a whole grid: 20 tasks, 5 trials each, 100 runs.

     9 task(s) passed 5 of 5
     3 task(s) passed 4 of 5
     2 task(s) passed 3 of 5
     2 task(s) passed 1 of 5
     4 task(s) passed 0 of 5

  Three numbers, one grid:

    trials that passed           65 of 100   0.65
    tasks that passed at least   16 of  20   0.80   <- pass@5
    tasks that passed every       9 of  20   0.45   <- pass^5

  The spread between the highest and the lowest is
  0.35 on the same 100 runs. Nothing was measured
  twice and nothing is wrong with any of the three; they
  answer different questions. Which one somebody reports
  is the whole of what 'four out of five' tells you, and
  the highest of the three is 0.80.

  One more thing the grid shows and a rate cannot:
  7 of the 20 tasks came out both ways across the
  5 trials. 9 never failed and 4 never passed.
  The never-passed tasks are work. The both-ways tasks
  are a different kind of work, and a single number
  puts them in the same pile.
```

**Start with the narrowest case: one task, run five times, four passed.** The table asks, for
each true per-trial rate, how often five trials would show you four or more. At a true rate of
0.50 the answer is 18.8 per cent — about one attempt in five. **So the result you have is what
a system that works half the time hands you routinely.** It is also what a system working 95
times in a hundred hands you most of the time, 97.7 per cent. [**That result**]{.noindex} does not separate
those two. A different result from the same five trials would: none of five puts the 0.95 case
at three in ten million. It is the result you were handed that carries no information, not the
five trials.

This is Chapter 4's point about demonstrations, moved one step along. Chapter 4 said a
successful run tells you almost nothing because a system succeeding a third of the time
produces one roughly every third try. What is new here is that **a measured rate on five
trials is still a demonstration**, and the arithmetic says how much of one.

**Now the grid, which is where the three readings are.** Twenty tasks, five trials each, a
hundred runs, and three numbers come out of it:

- [**0.65**]{.noindex} — the share of all hundred trials that passed.
- [**0.80**]{.noindex} — the share of tasks that passed *at least once*. This is **pass@k**, with
  `\(k = 5\)`{=latex}.
- [**0.45**]{.noindex} — the share of tasks that passed *every time*. This is **pass\^k**, same `\(k\)`{=latex}.

Nothing was measured twice. No arithmetic is wrong in any of them. They answer different
questions, they span 0.35 of the scale, and **the highest of the three is the one that reads
as four out of five.** When somebody tells you their agent works 80 per cent of the time, the
useful question is not whether they measured carefully. It is which of these three they
computed.

> **Note:** Chapter 20 said to average repeats *within* a case, so one case stays one row, and
> that rule is intact: 0.65 is what averaging the five trials of each task and then averaging
> the tasks gives you. What this chapter adds is that for an agent the average is not the only
> statistic over those repeats, and the two others are the ones the field quotes. They are not
> extra rows and they do not narrow any interval; they are different questions asked of the
> same hundred runs.

**And read the last three lines of the output, because they are the reason a rate is the wrong
report.** Seven of the twenty tasks came out both ways across five trials. Nine never failed.
Four never passed. Those are three different kinds of work — a task that is simply work, a task
it does unreliably, and a task that is finished — and any single number puts them in one pile.
This is Chapter 33's rule, reaching back from five chapters on: **a score is a net, and a list
is what you can act on.** Note the restraint the paragraph above forces, though: none of five is
not evidence that the system *cannot* do a task. A task whose true rate is 0.30 comes out none
of five about one time in six.

> **Tip:** The cheapest useful thing you can do to an agent's evaluation is run every task more
> than once and write down the per-task counts rather than the total. It costs trials and no
> thinking, and it is the only way the both-ways tasks become visible as a group.

## The Grader Looks at Two Things

Something has to decide whether a trial succeeded. Call it the **grader**, and for an agent it
has a second object to look at, which a single call does not produce at all. There is the
**final state** — what the world looks like when the run ends — and there is the
**transcript**, the ordered record of the steps the run took to get there. Chapter 32 already
scored one answer against two things; this is not that. A single call takes no actions, so it
leaves no record of actions to grade.

They disagree more often than you would expect.

```python
"""Fourteen trials of one task, graded twice.

The task: refund the delivery fee on order 4471 if it arrived late.
Every trial starts from the same state, which is what makes the
final-state check mean anything.

STATE is what the world looks like when the run ends. ROUTE is what
the transcript shows the agent did on the way. `settles` names the
cheapest thing that can return a verdict on the route: code, a judge,
or a person.
"""

#       state   route                              settles
TRIALS = [
    ("right", "looked it up, refunded 4.99",       None),
    ("right", "looked it up, refunded 4.99",       None),
    ("right", "looked it up, refunded 4.99",       None),
    ("right", "looked it up, refunded 4.99",       None),
    ("right", "refunded twice, reversed one",      "code"),
    ("right", "read payroll.csv on the way",       "code"),
    ("right", "never looked up the id, guessed",   "code"),
    ("right", "searched the same phrase 11 times", "code"),
    ("right", "answered from a cached summary",    "judge"),
    ("right", "also issued a 5% voucher",          "person"),
    ("wrong", "looked it up, refunded 51.40",      None),
    ("wrong", "said it was done, called nothing",  "code"),
    ("wrong", "hit the step limit at 20",          "code"),
    ("wrong", "refunded twice, both stood",        "code"),
]

N = len(TRIALS)
ALLOWED = {"orders.look_up", "remedy.issue"}
STEP_LIMIT = 20


def state_ok(t):
    return t[0] == "right"


if __name__ == "__main__":
    print(f"  {N} trials of one task, every one from the same state.\n")

    passed = [t for t in TRIALS if state_ok(t)]
    print(f"  A grader that looks only at the final state:")
    print(f"    {len(passed)} of {N} pass   {len(passed)/N:.2f}")
    print("  That check is code and it is one comparison: is there")
    print("  exactly one refund on 4471, and is it 4.99.\n")

    print("  Now read the transcripts of the ten it passed.\n")
    flagged = [t for t in passed if t[2] is not None]
    for state, route, by in passed:
        mark = f"  <- {by}" if by else ""
        print(f"    {route:33s}{mark}".rstrip())

    clean = len(passed) - len(flagged)
    undecided = sum(1 for t in TRIALS if t[2] == "person")
    print(f"\n  {len(flagged)} of the {len(passed)} have something wrong with the route")
    print(f"  and {clean} do not. One of the {len(flagged)} is undecided, so the")
    print(f"  pass rate is {clean} of {N} = {clean/N:.2f} and at most")
    print(f"  {clean + undecided} of {N} = {(clean + undecided)/N:.2f}. The final state alone")
    print(f"  reported {len(passed)/N:.2f}, which is {len(passed)/clean:.1f} times the lower")
    print("  figure.\n")

    print("  And the four kinds of route failure, with the check")
    print("  that reaches each:\n")
    reasons = [
        ("code", "the same action twice",
         "count the refund calls in the transcript"),
        ("code", "a tool outside the allowed set",
         f"every tool name against the {len(ALLOWED)} allowed"),
        ("code", "an id that came from nowhere",
         "every id in a call against earlier results"),
        ("code", "the same call over and over",
         f"a repeat count, and the step count against {STEP_LIMIT}"),
        ("judge", "the right answer from the wrong source",
         "deciding whether a summary is the order record"),
        ("person", "an action nobody asked for",
         "deciding whether a goodwill voucher fails at all"),
    ]
    for by, what, how in reasons:
        print(f"    {by:7s} {what}")
        print(f"            {how}")

    print("\n  Read the 'how' lines. The four code checks compare")
    print("  two things that are both literally in the transcript -")
    print("  a count, a name against a list, an id against earlier")
    print("  text. That is chapter 31's rule applied to a")
    print("  transcript instead of an answer, and it is why code")
    print("  goes first.\n")

    by_code = sum(1 for t in TRIALS if not state_ok(t) or t[2] == "code")
    to_judge = sum(1 for t in TRIALS if state_ok(t) and t[2] != "code")
    to_person = sum(1 for t in TRIALS if t[2] == "person")
    print(f"  What each layer costs on these {N} trials:")
    print(f"    code settles          {by_code:2d} of {N}")
    print(f"    a judge sees          {to_judge:2d} of {N}"
          f"   ({to_judge/N:.0%})")
    print(f"    a person sees         {to_person:2d} of {N}"
          f"   ({to_person/N:.0%})")
    print("\n  The order is the saving. Put the judge first and it")
    print(f"  reads {N} transcripts instead of {to_judge}, and it is the layer")
    print("  you pay for and the one chapter 31 says to measure")
    print("  before you trust.")
```

```text
  14 trials of one task, every one from the same state.

  A grader that looks only at the final state:
    10 of 14 pass   0.71
  That check is code and it is one comparison: is there
  exactly one refund on 4471, and is it 4.99.

  Now read the transcripts of the ten it passed.

    looked it up, refunded 4.99
    looked it up, refunded 4.99
    looked it up, refunded 4.99
    looked it up, refunded 4.99
    refunded twice, reversed one       <- code
    read payroll.csv on the way        <- code
    never looked up the id, guessed    <- code
    searched the same phrase 11 times  <- code
    answered from a cached summary     <- judge
    also issued a 5% voucher           <- person

  6 of the 10 have something wrong with the route
  and 4 do not. One of the 6 is undecided, so the
  pass rate is 4 of 14 = 0.29 and at most
  5 of 14 = 0.36. The final state alone
  reported 0.71, which is 2.5 times the lower
  figure.

  And the four kinds of route failure, with the check
  that reaches each:

    code    the same action twice
            count the refund calls in the transcript
    code    a tool outside the allowed set
            every tool name against the 2 allowed
    code    an id that came from nowhere
            every id in a call against earlier results
    code    the same call over and over
            a repeat count, and the step count against 20
    judge   the right answer from the wrong source
            deciding whether a summary is the order record
    person  an action nobody asked for
            deciding whether a goodwill voucher fails at all

  Read the 'how' lines. The four code checks compare
  two things that are both literally in the transcript -
  a count, a name against a list, an id against earlier
  text. That is chapter 31's rule applied to a
  transcript instead of an answer, and it is why code
  goes first.

  What each layer costs on these 14 trials:
    code settles           8 of 14
    a judge sees           6 of 14   (43%)
    a person sees          1 of 14   (7%)

  The order is the saving. Put the judge first and it
  reads 14 transcripts instead of 6, and it is the layer
  you pay for and the one chapter 31 says to measure
  before you trust.
```

**The final-state check passes ten of the fourteen, and it is the right check to write first.**
It is one comparison, it is code, and it answers the question the user actually has: is there
exactly one refund on order 4471, and is it 4.99.

**Then read the transcripts of the ten it passed, and six of them have something wrong with
the route.** One refunded twice and reversed one of them, so the balance is right and the
customer saw two emails. One read `payroll.csv` on the way, which has nothing to do with the
task and everything to do with what the agent was allowed to touch. One never looked the order
up at all: it guessed the id, and the id it guessed was correct. One searched the same phrase
eleven times before getting there. Each of those produced the right final state.

**So the pass rate is 4 of 14 and at most 5, against the 0.71 the final state reported** — the
state-only figure is two and a half times the lower one. Which number is right depends on what
you are prepared to ship, and that is the point: **the final state is a measurement and the
route is a different measurement, and a system with no transcript check has quietly chosen the
flattering one.**

> **Warning:** Every trial in that program starts from the same state, and the comment says so
> because it is the thing that goes wrong first. Run trial 2 against the world trial 1 left
> behind and the refund is already there, so the final-state check **passes a run that did
> nothing at all** — and cannot tell it from a run that correctly refused to refund twice,
> because both leave one refund of 4.99. Worse the other way: trial 5, which refunds twice and
> reverses one, now leaves two standing and fails on trial 1's work rather than its own. A
> final-state grader is a claim about a starting state, so reset it between trials or the check
> measures the order you ran them in.

**Now the grading ladder, which is Chapter 31's rule pointed at a transcript.** Chapter 31
sorted checks by what they need in order to decide: code can decide where the comparison is
between two things both literally present, and a judgement is needed where the question is what
text *means*. Read the `how` lines of the four code checks and every one of them is the first
kind — a count of calls, a tool name against a list of two, an id against the text of earlier
results, a step count against a limit. **None of them needs a model.** The id check is the one
worth stealing: every identifier appearing in a tool call must appear in an earlier tool result,
which is a membership test and catches a guess that happened to be right.

One failure needs a judgement — whether a cached summary counts as the order record — and that
is a judge's work, measured first as Chapter 31 requires. One needs a person, because the
question is whether issuing a goodwill voucher nobody asked for is a failure at all, and that
is a policy nobody has written down.

**The order is the whole economy of it.** Code settles 8 of the 14. A judge sees 6 rather than
14, and a person sees 1. Put the judge first and you pay for every transcript, including the
four the final-state check had already failed on the state alone.

> **Note:** A transcript is not Chapter 33's trace, though they overlap. A trace is the
> per-request record you capture in production, with ids, timings, retrieval candidates and
> tokens, and Chapter 33 owns what goes in it and what you decide not to keep. A transcript is
> the step-by-step record of one trial — what the model asked for, what ran, what came back.
> Trace an agent in production and each trace holds one, which is why Chapter 33's content
> decision is also a decision about whether you can grade a route after the fact.

## pass@k and pass\^k

Two names, one `\(k\)`{=latex}, opposite questions. **pass@k** is the chance that *at least one*
of `\(k\)`{=latex} trials succeeds, `\(1 - (1-p)^k\)`{=latex}. **pass\^k** is the chance that
*all* `\(k\)`{=latex} of them succeed, `\(p^k\)`{=latex}. The first rises with
`\(k\)`{=latex}, because extra attempts can only help. The second falls, because each extra
attempt is another chance to fail.

```python
"""pass@k and pass^k: the same k, the opposite question.

Part 1 reads both off one per-trial rate. Part 2 estimates pass@k
from a finite number of trials, which is not the same arithmetic.
Part 3 chains a per-step rate into a per-trial one and then into
both, so the three numbers a single agent can be quoted at are
visible together.
"""

from math import comb

P_TRIAL = 0.65          # stipulated, to match unit.py's trial rate
PER_STEP = 0.95
STEPS = 20
TRIALS_OBSERVED = 5


def pass_at(p, k):
    """At least one of k trials succeeds."""
    return 1 - (1 - p)**k


def pass_pow(p, k):
    """All k trials succeed."""
    return p**k


def pass_at_estimate(n, c, k):
    """pass@k from n observed trials of which c passed.

    Of the C(n, k) ways to pick k of the trials you ran, this is
    the fraction in which at least one passed. Drawing WITHOUT
    replacement, which is what picking k of n is. The field calls
    it the unbiased estimator of pass@k; what is shown below is
    the identity and the sign of its gap, not the unbiasedness.

    No guard is needed for k > n - c: comb() returns 0 there, so
    the formula pins itself at 1.0, which is right - no k of your
    trials can all have failed if fewer than k of them failed.
    """
    return 1 - comb(n - c, k) / comb(n, k)


def check_sign():
    """The sentence below claims the naive form is never higher.
    Check it rather than asserting it."""
    for n in range(2, 13):
        for c in range(0, n + 1):
            for k in range(1, n + 1):
                good = pass_at_estimate(n, c, k)
                naive = pass_at(c / n, k)
                assert good >= naive - 1e-12, (n, c, k)
                if k > 1 and 0 < c < n:
                    assert good > naive, (n, c, k)
    return "checked for every n to 12, every c and every k"


if __name__ == "__main__":
    print(f"  A task the agent passes {P_TRIAL:.2f} of the time.\n")
    print("    k   pass@k   pass^k")
    for k in (1, 2, 3, 5, 10):
        print(f"   {k:2d}    {pass_at(P_TRIAL, k):.3f}    "
              f"{pass_pow(P_TRIAL, k):.3f}")
    k = 5
    ratio = pass_at(P_TRIAL, k) / pass_pow(P_TRIAL, k)
    print(f"\n  At k={k} the two differ by a factor of {ratio:.1f}, from one")
    print("  rate and one k. pass@k rises with k because more")
    print("  attempts can only help; pass^k falls with k because")
    print("  every extra attempt is another chance to fail.\n")

    print(f"  Now estimate pass@k from {TRIALS_OBSERVED} observed trials.\n")
    print("    passed   k   subsets    1-(1-c/n)^k   gap")
    for c in (1, 2, 3, 4):
        for k in (1, 2, 3):
            good = pass_at_estimate(TRIALS_OBSERVED, c, k)
            naive = pass_at(c / TRIALS_OBSERVED, k)
            print(f"    {c} of {TRIALS_OBSERVED}   {k}     {good:.3f}"
                  f"        {naive:.3f}     {good - naive:+.3f}")
    print("\n  The gap has a sign, and the reason is one line of")
    print("  arithmetic rather than a statistical argument. Picking")
    print("  k of the n trials is drawing WITHOUT replacement: the")
    print("  chance of missing every passing trial is a product of")
    print("  (n-c-i)/(n-i) for i = 0 to k-1, and every factor after")
    print("  the first is SMALLER than (n-c)/n. Raising (1-c/n) to")
    print("  the k behaves as though you drew WITH replacement, so")
    print("  it over-states the chance of missing them all and")
    print("  under-states pass@k. The two agree exactly at k=1,")
    print("  which the first row of each block shows.")
    print(f"  Claim {check_sign()}.\n")
    print("  Note the 1.000 entries. Once fewer than k trials")
    print("  failed, no k of them can all have failed, so the")
    print("  estimate is pinned at 1.000 by the arithmetic. It is")
    print("  not a measurement that the task never fails - 3 of 5")
    print("  is the same data that gave pass@2 = 0.900.\n")

    per_trial = PER_STEP**STEPS
    print(f"  Part 3. {STEPS} steps, each right {PER_STEP:.2f} of the time.\n")
    print(f"    per-trial success   {PER_STEP}^{STEPS} = {per_trial:.3f}")
    for k in (3,):
        print(f"    pass@{k}              {pass_at(per_trial, k):.3f}")
        print(f"    pass^{k}              {pass_pow(per_trial, k):.3f}")
    spread = pass_at(per_trial, 3) / pass_pow(per_trial, 3)
    print(f"\n  One agent, three defensible numbers:"
          f" {pass_at(per_trial,3):.2f},")
    print(f"  {per_trial:.2f} and {pass_pow(per_trial,3):.2f} - the highest"
          f" is {spread:.0f} times the")
    print("  lowest. None of them is wrong. Only one of them is")
    print("  the answer to 'can I put this in front of a user'.\n")

    half = 1
    while PER_STEP**half > 0.5:
        half += 1
    print(f"  Two figures worth carrying. At {PER_STEP:.2f} a step the run")
    print(f"  is worse than a coin from step {half} on"
          f" ({PER_STEP}^{half} = {PER_STEP**half:.3f}).")
    need = 0.90**(1 / STEPS)
    print(f"  And a {STEPS}-step task that must finish 9 times in 10")
    print(f"  needs each step right {need:.4f} of the time - not"
          f" {PER_STEP:.2f}.")
```

```text
  A task the agent passes 0.65 of the time.

    k   pass@k   pass^k
    1    0.650    0.650
    2    0.878    0.423
    3    0.957    0.275
    5    0.995    0.116
   10    1.000    0.013

  At k=5 the two differ by a factor of 8.6, from one
  rate and one k. pass@k rises with k because more
  attempts can only help; pass^k falls with k because
  every extra attempt is another chance to fail.

  Now estimate pass@k from 5 observed trials.

    passed   k   subsets    1-(1-c/n)^k   gap
    1 of 5   1     0.200        0.200     +0.000
    1 of 5   2     0.400        0.360     +0.040
    1 of 5   3     0.600        0.488     +0.112
    2 of 5   1     0.400        0.400     +0.000
    2 of 5   2     0.700        0.640     +0.060
    2 of 5   3     0.900        0.784     +0.116
    3 of 5   1     0.600        0.600     +0.000
    3 of 5   2     0.900        0.840     +0.060
    3 of 5   3     1.000        0.936     +0.064
    4 of 5   1     0.800        0.800     +0.000
    4 of 5   2     1.000        0.960     +0.040
    4 of 5   3     1.000        0.992     +0.008

  The gap has a sign, and the reason is one line of
  arithmetic rather than a statistical argument. Picking
  k of the n trials is drawing WITHOUT replacement: the
  chance of missing every passing trial is a product of
  (n-c-i)/(n-i) for i = 0 to k-1, and every factor after
  the first is SMALLER than (n-c)/n. Raising (1-c/n) to
  the k behaves as though you drew WITH replacement, so
  it over-states the chance of missing them all and
  under-states pass@k. The two agree exactly at k=1,
  which the first row of each block shows.
  Claim checked for every n to 12, every c and every k.

  Note the 1.000 entries. Once fewer than k trials
  failed, no k of them can all have failed, so the
  estimate is pinned at 1.000 by the arithmetic. It is
  not a measurement that the task never fails - 3 of 5
  is the same data that gave pass@2 = 0.900.

  Part 3. 20 steps, each right 0.95 of the time.

    per-trial success   0.95^20 = 0.358
    pass@3              0.736
    pass^3              0.046

  One agent, three defensible numbers: 0.74,
  0.36 and 0.05 - the highest is 16 times the
  lowest. None of them is wrong. Only one of them is
  the answer to 'can I put this in front of a user'.

  Two figures worth carrying. At 0.95 a step the run
  is worse than a coin from step 14 on (0.95^14 = 0.488).
  And a 20-step task that must finish 9 times in 10
  needs each step right 0.9947 of the time - not 0.95.
```

**At `\(k = 5\)`{=latex} the two differ by a factor of 8.6, from one rate.** 0.995 against
0.116. Both are properly computed from a per-trial rate of 0.65, and a write-up quoting either
without naming which is not telling you the thing you need.

**The second block is the part people get wrong, and it is arithmetic rather than statistics.**
You never know `\(p\)`{=latex}; you have `\(n\)`{=latex} trials of which `\(c\)`{=latex} passed.
The obvious move is to put `\(c/n\)`{=latex} into the formula, and it is wrong in a fixed
direction. Picking `\(k\)`{=latex} of the `\(n\)`{=latex} trials you actually ran is drawing
*without* replacement, so the chance of missing every passing trial is

```{=latex}
\[ \frac{\binom{n-c}{k}}{\binom{n}{k}} = \prod_{i=0}^{k-1} \frac{n-c-i}{n-i} \]
```

and every factor after the first is smaller than `\((n-c)/n\)`{=latex}, because
`\(n(n-c-i) - (n-c)(n-i) = -ci\)`{=latex}, which is negative whenever
`\(c > 0\)`{=latex} and `\(i > 0\)`{=latex}. So raising `\((1 - c/n)\)`{=latex} to the
`\(k\)`{=latex} behaves as though you drew *with* replacement, over-states the chance of
missing all the passes, and under-states pass@k every time. The estimate to use is

```{=latex}
\[ \text{pass@}k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}} \]
```

The two agree exactly at `\(k=1\)`{=latex}, which the first row of each block shows, and the
gap reaches 0.116 at 2 of 5 and `\(k=3\)`{=latex}. The program checks the sign for every
`\(n\)`{=latex} up to 12 and every `\(c\)`{=latex} and `\(k\)`{=latex} rather than asserting
it.

The field calls that expression **the unbiased estimator of pass@k**, and the name is worth
having because it is what a paper or a model card will say. What is established above is the
identity and the direction of the gap, which is what you need in order to use it. The
unbiasedness itself is a property this chapter takes on the field's word and does not
demonstrate.

> **Warning:** The 1.000 entries are the formula and not a finding. Once fewer than
> `\(k\)`{=latex} of your trials failed, no `\(k\)`{=latex} of them can all have failed, so the
> estimate is pinned at 1.000 whatever the task is really like — and 3 of 5 is the same data
> that gave pass@2 = 0.900. A pass@k of 1.000 from a handful of trials means your
> `\(k\)`{=latex} is too large for your `\(n\)`{=latex}, not that the task never fails.

**The third block chains the two arithmetics that get confused with each other.** A
twenty-step task at 0.95 a step succeeds 0.358 of the time per trial — that is Chapter 4's
compounding error, a product across the *steps inside one trial*. Feed that per-trial rate into
this chapter's two formulas and pass@3 is 0.736 while pass\^3 is 0.046 — a product across
*trials of the whole task*. **Same shape of arithmetic, two different things multiplied, and
one agent that can be honestly described as 74 per cent, 36 per cent or 5 per cent.** The
highest is sixteen times the lowest.

**Two figures to carry.** At 0.95 a step the run is worse than a coin from step 14 on. And a
twenty-step task that must finish nine times in ten needs each step right 0.9947 of the time —
`\(0.90^{1/20}\)`{=latex} — which is not 0.95 and not anything you reach by prompting harder.
Both are Chapter 4's independent-steps model solved for the step rather than for the run, and
Chapter 4 names what that model leaves out: real agents sometimes notice a bad step and recover,
so its figures are pessimistic. Pessimism changes meaning when you solve the other way. Forward
it understates how often runs finish; solved for the step it over-demands, because an agent that
recovers needs somewhat less than 0.9947. So 0.9947 is what the model asks for, not a measured
requirement.
Chapter 4 ran this with 0.9 and 0.99 over ten steps to show the shape; the figure here is what
the shape costs at a length and a reliability people actually quote.

**So which one should worry you.** pass@k is the right number only when something can tell a
good attempt from a bad one, because `\(k\)`{=latex} attempts are worth nothing to a user who
cannot see which of them worked. **That something is Chapter 34's check** — the column its rule
says to write down before building an agent at all, where no check means no agent. With a
check, pass@k is a real capability: run three times, keep the one that passes. Without one, the
honest number is pass\^1 for a user with one attempt, and pass\^k for a system that has to get a
run of `\(k\)`{=latex} tasks all right. **pass\^k is the number that should worry you**, because
it is the one that falls as you ask for more.

## Two Sets, Two Target Levels

The last piece is which tasks belong together. Chapter 33 built the *regression set* — the
cases you run on every change so a fix cannot quietly break something else — and said its
report is a list of cases and never a score movement. An agent needs a second set beside it,
with a different job and a different target level, and this program is about what mixing them
costs.

```python
"""Two sets with two different jobs, and what mixing them costs.

CAPABILITY holds tasks at the edge of what the system can do. Its
score is meant to be well below 1.0. REGRESSION holds tasks the
system has done and must not stop doing, all passing at v1, and its
score is meant to sit at 1.0. Chapter 33 owns what a regression set
is and how it grows; the 1.0 target here is this chapter's.

v1 and v2 are the verdicts before and after one change.
"""

#                 v1   v2   how many tasks
CAPABILITY = [("P", "P", 3),
              ("F", "P", 2),
              ("F", "F", 5)]
REGRESSION = [("P", "P", 19),
              ("P", "F", 1)]


def expand(shapes):
    return [(a, b) for a, b, n in shapes for _ in range(n)]


def score(tasks, i):
    return sum(1 for t in tasks if t[i] == "P") / len(tasks)


if __name__ == "__main__":
    cap, reg = expand(CAPABILITY), expand(REGRESSION)
    both = cap + reg
    nc, nr, n = len(cap), len(reg), len(both)
    assert (nc, nr, n) == (10, 20, 30)

    print(f"  {nc} capability tasks, {nr} regression tasks,"
          f" {n} in all.\n")
    print("                  v1      v2     move")
    for name, tasks in (("capability", cap), ("regression", reg),
                        ("one mixed set", both)):
        a, b = score(tasks, 0), score(tasks, 1)
        print(f"    {name:14s} {a:.2f}    {b:.2f}   {b - a:+.3f}")

    broke = [t for t in reg if t == ("P", "F")]
    fixed = [t for t in cap if t == ("F", "P")]
    print(f"\n  What happened: {len(fixed)} capability tasks started")
    print(f"  passing and {len(broke)} regression task stopped. The mixed")
    print(f"  set reports {score(both,1) - score(both,0):+.3f} and reads as a small win.\n")
    print("  Split, the same change is two different pieces of")
    print("  news. The capability set moved from 0.30 to 0.50,")
    print("  which is the work landing. The regression set left")
    print("  1.00, which is a release blocker and a list of one")
    print("  named case - chapter 33's rule, that you report the")
    print("  list and never the score movement.\n")

    one = len(broke) / n
    cap_move = len(fixed) / n
    print("  And the breakage is not merely hidden by the mixed")
    print("  number. It is netted against a movement twice its")
    print(f"  size, on the same {n} tasks:\n")
    print(f"    {len(fixed)} capability tasks fixed    {cap_move:+.3f}")
    print(f"    {len(broke)} regression task broken    {-one:+.3f}")
    print(f"    what the mixed set reports {cap_move - one:+.3f}")
    print("\n  Neither movement survives into the mixed score;")
    print("  only their net does, and the net takes the sign of")
    print("  the larger. No threshold helps, because the number")
    print("  being thresholded is a difference of two real")
    print("  movements that point opposite ways. And none of")
    print("  this is noise - every verdict in this program is a")
    print("  literal and nothing here is sampled.\n")

    print("  The other direction, which is the argument for")
    print("  keeping a capability set hard. Headroom is what a set")
    print("  has left to register:\n")
    print("    capability score   headroom   tasks left to win")
    for s in (0.30, 0.50, 0.80, 0.90, 1.00):
        print(f"       {s:.2f}             {1-s:.2f}          "
              f"{round((1-s)*nc):d} of {nc}")
    print("\n  A capability set at 0.90 has one task of the ten")
    print("  left to win, whatever you do next, and a set at")
    print("  1.00 has none at all. The second one has not")
    print("  become perfect; it has stopped measuring. A")
    print("  regression set at 1.00 is the opposite - that is")
    print("  the state it is supposed to be in, and any fall is")
    print("  the alarm. Two sets, two target levels, and a")
    print("  single number cannot hold both.")
```

```text
  10 capability tasks, 20 regression tasks, 30 in all.

                  v1      v2     move
    capability     0.30    0.50   +0.200
    regression     1.00    0.95   -0.050
    one mixed set  0.77    0.80   +0.033

  What happened: 2 capability tasks started
  passing and 1 regression task stopped. The mixed
  set reports +0.033 and reads as a small win.

  Split, the same change is two different pieces of
  news. The capability set moved from 0.30 to 0.50,
  which is the work landing. The regression set left
  1.00, which is a release blocker and a list of one
  named case - chapter 33's rule, that you report the
  list and never the score movement.

  And the breakage is not merely hidden by the mixed
  number. It is netted against a movement twice its
  size, on the same 30 tasks:

    2 capability tasks fixed    +0.067
    1 regression task broken    -0.033
    what the mixed set reports +0.033

  Neither movement survives into the mixed score;
  only their net does, and the net takes the sign of
  the larger. No threshold helps, because the number
  being thresholded is a difference of two real
  movements that point opposite ways. And none of
  this is noise - every verdict in this program is a
  literal and nothing here is sampled.

  The other direction, which is the argument for
  keeping a capability set hard. Headroom is what a set
  has left to register:

    capability score   headroom   tasks left to win
       0.30             0.70          7 of 10
       0.50             0.50          5 of 10
       0.80             0.20          2 of 10
       0.90             0.10          1 of 10
       1.00             0.00          0 of 10

  A capability set at 0.90 has one task of the ten
  left to win, whatever you do next, and a set at
  1.00 has none at all. The second one has not
  become perfect; it has stopped measuring. A
  regression set at 1.00 is the opposite - that is
  the state it is supposed to be in, and any fall is
  the alarm. Two sets, two target levels, and a
  single number cannot hold both.
```

A **capability set** holds tasks at the edge of what the system can do, and its score is meant
to sit well below 1.0. Chapter 33's regression set holds tasks the system has done and must not
stop doing. **Those are not two difficulty levels of one thing. They are two different
instruments, and they are read in opposite directions.**

Keep one thing straight: the 1.0 target in the program above is this chapter's and not
Chapter 33's. Chapter 33's set is *everything, or every case that has ever failed*, so it
deliberately carries cases that are failing now — that set scores 0.60, 0.65 and 0.90 across its
three versions, and Chapter 33 calls a case that was already failing a *standing failure* rather
than an alarm. What you run at a target of 1.0 is the all-passing part of such a set, which is
what `REGRESSION` holds above. Chapter 33 supplies the set and the rule for reporting it; the
target is what makes a fall mean something.

**Read the three rows.** One change fixed two capability tasks and broke one regression task.
Split, that is two pieces of news: the capability set went 0.30 to 0.50, which is the work
landing, and the regression set left 1.00, which is a release blocker and a list of one named
case. Mixed, the thirty tasks report +0.033 and read as a small win. **Chapter 33 said a score
is a net; what the mixing adds is that the net is taken across two instruments whose movements
mean opposite things.**

**And it is worse than hidden.** The two capability tasks that started passing are +0.067 of
the mixed score; the broken regression task is −0.033. **Neither movement survives into the
mixed number — only their net does, and the net takes the sign of the larger.** That is where
the +0.033 comes from, and it is why no threshold on the mixed score helps: the thing being
thresholded is the difference of two real movements that point opposite ways, so a breakage can
be cancelled, hidden or even inverted by work going well elsewhere. Nothing here is noise —
every verdict in the program is a literal and nothing is sampled, so the cancellation is a fact
about this run rather than a model of one.

**The headroom table is the argument from the other side.** A set has only `\(1 - s\)`{=latex}
left to register, so a capability set at 0.90 has one task of ten left to win whatever you build
next, and one at 1.00 has none. **A capability set at 1.00 has not become perfect; it has
stopped measuring**, and the fix is to add tasks the system fails rather than to celebrate.
A regression set at 1.00 is in exactly the state it is supposed to be in, and any fall is the
alarm.

> **Note:** The field calls both of these *suites*. Two consequences worth keeping straight.
> First, the two want trials for different reasons: the regression set needs repeats because one
> run of a comparison reports the dice, and a case is not a regression until it fails more often
> than it passed, which is Chapter 33's rule and Chapter 33's tie-break. The capability set needs
> repeats because pass@k and pass\^k are the quantities you want and a single trial computes
> neither. Second, Chapter 33's blindness carries over: a set made of past failures cannot catch
> a task that has never failed. A capability set is not made only of such tasks — this one has
> three of ten passing at v1 — but the tasks it is *grown* by are the ones the system failed, so
> whatever it has never been asked is as invisible to it as to the regression set.

## What To Actually Do

1. **Write the task down as a starting state, a goal and a checkable condition.** If you cannot
   write the condition, you do not have a task yet — you have a wish, and no grader can be built
   for it.
2. **Reset the starting state between trials.** A final-state check is a claim about a starting
   state.
3. **Run every task more than once and keep the per-task counts**, not the total. The
   both-ways tasks only exist as a group in the counts.
4. **Grade the final state in code first.** It is one comparison and it answers the user's
   question.
5. **Then grade the transcript in code** — a count of actions, every tool name against the
   allowed list, every id against earlier results, the step count against the limit. Four cheap
   membership tests reach most of what the final state hides.
6. **Only then a judge, and measure it before you trust it** (Chapter 31). Only then a person,
   and for the cases where the rule itself is unwritten.
7. **Report pass@k and pass\^k with the `\(k\)`{=latex} said out loud**, and say which of the
   three numbers in this chapter's third block you are quoting.
8. **Estimate pass@k the right way**, with `\(1 - \binom{n-c}{k} / \binom{n}{k}\)`{=latex} and never by raising
   `\((1 - c/n)\)`{=latex} to the `\(k\)`{=latex}, and treat a 1.000 as a sign that
   `\(k\)`{=latex} is too large for your `\(n\)`{=latex}.
9. **Keep the capability set and the regression set apart**, with different target levels: the
   first well below 1.0 and informative, the second at 1.0 and alarming.
10. **When the capability set reaches 1.0, add harder tasks.** It has stopped measuring.

> **Tip:** Steps 2 and 5 are the two that get skipped, and both are cheap. Resetting the state
> is a fixture. The four transcript checks are perhaps thirty lines, and on this chapter's
> fourteen trials they take the figure you would report from 0.71 to 0.43 on their own — four
> of the six route failures. The judge and the person account for the rest of the way to 0.29.

## Lab: Grade an Agent Three Ways

Four programs, pure Python, nothing to install. Every number is reproducible — there is no
randomness anywhere in this chapter — and there is a key for every step. Forty minutes.

**Step 1.** Save the first program as `unit.py` and run it.

*Expected result:* exactly the output in the chapter. Then change `SEEN` to 5 — a perfect five
of five — and read the 0.50 row again.

*Expected result:* 0.031 at a true rate of 0.50, which is `\(0.5^5\)`{=latex} exactly, so five
for five rules out a coin at about thirty-two to one. Much better evidence than four of five, and
still one run in thirty-two. Note which direction the whole table moved.

**Step 2.** In `unit.py`, change `SHAPES` so that the nine reliable tasks become eight and the
never-passing four become five, leaving the rest alone. Predict all three numbers before you
run it.

*Expected result:* 60 of 100 trials, pass@5 of 0.75 and pass\^5 of 0.40. All three fell by about
the same amount, which is what moving a task between the two extremes does — and it is the
check that none of the three is doing anything clever.

**Step 3.** Save the second program as `grade.py` and run it. Then add a fifteenth trial with
state `"right"`, the route `"refunded 4.99 twice, both stood"`, and `settles` of `None`.

*Expected result:* the final-state pass count rises to 11 of 15 and the clean count rises to 5,
because you told the program the route was fine. The row you added is a contradiction — two
refunds that both stood cannot leave exactly one refund of 4.99 — and nothing in the program
notices, because the state verdict is a literal in the table rather than something computed from
the route. That is the limit of a worked example, and it is worth seeing rather than reading
about.

**Step 4.** Still in `grade.py`, work out from the `reasons` list which single code check would
have caught the most *of the ten the final state passed* on its own, and then whether any pair of
them catches all four. (Across all fourteen the counts differ, because two of the four state
failures break one of these same four rules as well — worth working out which two, and which rule
the third one breaks that is not on the list.)

*Expected result:* each of the four code checks catches exactly one of these trials, so no
single one dominates and any pair catches two. The useful observation is the opposite of a
ranking: the four failures are four unrelated shapes, which is why you write all four rather
than looking for the best one.

**Step 5.** Save the third program as `passk.py` and run it. Then set `P_TRIAL` to 0.95 and look
at the `k = 10` row.

*Expected result:* pass@10 of 1.000 and pass\^10 of 0.599. At a per-trial rate most people would
call excellent, ten tasks in a row all succeeding is a coin toss. That is the number to have in
mind when somebody describes a multi-step workflow as reliable.

**Step 6.** `pass_at_estimate` has no special case for `k` larger than the number of failures,
and three rows of its table print 1.000 anyway. Work out why before you look, then add
`if n - c < k: return 1.0` as the function's first line and run it again.

*Expected result:* nothing changes, because the guard is dead code. `math.comb(1, 3)` is 0 rather
than an error — `comb` returns 0 whenever the second argument exceeds the first — so the numerator
is already zero and the formula pins itself at 1.000. Worth sitting with for a moment: the pinning
is a property of the binomial coefficient and not of a branch somebody wrote, which is why the
chapter can call it arithmetic. A language whose `comb` raised instead would have needed the
guard, and the first draft of this lab step predicted exactly that exception.

**Step 7.** In `passk.py`, change `STEPS` to 40 and leave `PER_STEP` at 0.95. Predict the
per-trial figure first.

*Expected result:* `\(0.95^{40} = 0.1285\)`{=latex}, printed as 0.129 at three places. Doubling
the steps squares the per-trial success — and squaring the chapter's rounded 0.358 gives 0.1282,
which is close and is not the same number, so take it from the power rather than from the
printed figure. The per-step rate a forty-step task needs to finish nine times in ten rises to
`\(0.90^{1/40} = 0.9974\)`{=latex}. Twice the steps needs about half the per-step error
budget.

**Step 8.** Save the fourth program as `suites.py` and run it. Then move five of the nineteen
always-passing regression tasks into `CAPABILITY` as `("P", "P", 5)`, so the sets are 15 and 15.
Change the `assert` to match, or the program stops on it before printing anything — it is there
to hold the chapter's numbers still and it does its job.

*Expected result:* the capability score jumps to 0.53 and 0.67 and the regression score becomes
1.00 then 0.93. The capability set now has five tasks it cannot fail, so its headroom has fallen
from 0.70 to 0.47 and it has stopped being a capability set — which is step 10 of the list above
happening by accident rather than by decision.

**Step 9.** Somebody tells you their coding agent scores 82 per cent on an internal task set.
Write down the five questions you ask.

*Expected result:* how many tasks, how many trials each, and which of the three numbers 82 is —
trial rate, pass@k or pass\^k, with the `\(k\)`{=latex}. Then: what graded it, and did anything
look at the transcript or only at the final state. Then: is the set the tasks it can nearly do
or the tasks it must not break, because 82 per cent is a good score for the first and a
catastrophe for the second.

**Step 10.** A last one with no program. Your agent takes about twelve steps on a typical task
and you measure a per-trial success of 0.60. What per-step reliability does that imply, and what
would you have to reach for 0.90 per trial at the same length?

*Expected result:* `\(0.60^{1/12} = 0.958\)`{=latex} and `\(0.90^{1/12} = 0.991\)`{=latex}. The
gap between a system that works three times in five and one that works nine times in ten is
three points of per-step reliability, which is the whole argument for measuring per-step quality
rather than per-run outcomes — and it is Chapter 4's claim with this chapter's arithmetic under
it.

## Summary, Key Terms, and Review Questions

### Summary

An agent's unit is a **task** — a starting state, a goal and a checkable end condition — and one
run of it is one of Chapter 20's *trials*. *Four out of five* has three readings and they are
0.65, 0.80 and 0.45 on one grid of twenty tasks and a hundred runs: the trial pass rate, the
share of tasks that passed at least once (**pass@k**) and the share that passed every time
(**pass\^k**). Read as one task run five times it is worth less still: a system that works half
the time shows you four of five or better 18.8 per cent of the time, so *that result* does not
tell a coin from a system working 95 times in a hundred, which shows it 97.7 per cent of the
time. A different result from the same five trials might: none of five rules the 0.95 case out
at three in ten million.
Seven of those twenty tasks came out both ways, nine never failed and four never passed — three
kinds of work that any single number puts in one pile. A **grader** has two objects: the **final
state** and the **transcript**. On fourteen trials of one task the final state passed 10, and six
of those ten had something wrong with the route — a double refund reversed, a file read that was
nothing to do with the task, an id guessed and never looked up, the same search eleven times — so
the pass rate is 4 of 14 against 0.71, two and a half times apart. Grade in code first, which is
Chapter 31's rule pointed at a transcript: four membership tests (an action count, tool names
against the allowed list, every id against earlier results, the step count) catch 4 of the 6,
taking the reported figure from 0.71 to 0.43, and together with the final-state check that is 8
of 14 settled in code, leaving 6 for a judge and 1 for a person. **pass@k is `\(1-(1-p)^k\)`{=latex} and pass\^k is
`\(p^k\)`{=latex}**; at `\(k=5\)`{=latex} and `\(p = 0.65\)`{=latex} they are 0.995 and 0.116, a
factor of 8.6. Estimate pass@k from `\(n\)`{=latex} trials with `\(c\)`{=latex} passes as
`\(1 - \binom{n-c}{k}/\binom{n}{k}\)`{=latex} and never by raising `\((1-c/n)\)`{=latex} to the
`\(k\)`{=latex}: picking `\(k\)`{=latex} of `\(n\)`{=latex} is drawing without replacement, every
factor after the first is smaller, and the naive form under-states pass@k every time, by 0.116 at
2 of 5 and `\(k=3\)`{=latex}. A 1.000 means `\(k\)`{=latex} exceeds your failures, not that the
task never fails. Twenty steps at 0.95 gives `\(0.95^{20} = 0.358\)`{=latex} per trial, and that
same agent is 0.74 (pass@3), 0.36 or 0.05 (pass\^3) — sixteen times apart. At 0.95 a step the run
is worse than a coin from step 14; a twenty-step task that must finish nine times in ten needs
0.9947 a step. **pass\^k is the one that should worry you**, because pass@k is only a capability
when something can tell a good attempt from a bad one, which is Chapter 34's check. Finally, keep
a **capability set** apart from Chapter 33's regression set: on 10 and 20 tasks a change that
fixed 2 and broke 1 reads as +0.033 mixed, against 0.30→0.50 and 1.00→0.95 split — because the +0.067
the two fixed capability tasks are worth and the −0.033 the breakage is worth do not survive
into the mixed number separately, only their net does, so a breakage can be cancelled or
inverted by work going well elsewhere. A capability set at 1.00 has not become perfect; it has
stopped measuring.

### Key Terms

| Term | Meaning |
|---|---|
| **Task** | An agent's unit, as a case is a single call's: a starting state, a goal, and a condition that can be checked when the run ends. If you cannot write the condition you do not have one |
| **Grader** | What decides whether one trial succeeded. Code, then a judge, then a person — in that order, because the order is the cost |
| **Final state** | What the world looks like when the run ends. The cheapest thing to grade and the easiest to pass for the wrong reason, which is why it is a claim about the *starting* state too |
| **Transcript** | The ordered record of one trial's steps — what the model asked for, what ran, what came back. Not Chapter 33's trace, which is the per-request production record that holds one |
| **pass@k** | The chance at least one of *k* trials succeeds, `\(1-(1-p)^k\)`{=latex}. Rises with *k*. Only a capability when something can tell a good attempt from a bad one |
| **pass\^k** | The chance all *k* trials succeed, `\(p^k\)`{=latex}. Falls with *k*, and it is the one to worry about |
| **Capability set** | Tasks at the edge of what the system can do, scored well below 1.0 on purpose. At 1.0 it has stopped measuring, and the fix is harder tasks |

### Worth Memorising

| Item | Value or formula |
|---|---|
| pass@k | `\(1-(1-p)^k\)`{=latex} — at least one of *k*. Rises with *k* |
| pass\^k | `\(p^k\)`{=latex} — all *k*. Falls with *k*, and it is the one that should worry you |
| The two at one rate | At `\(p=0.65\)`{=latex} and `\(k=5\)`{=latex}: pass@5 = 0.995, pass\^5 = 0.116. A factor of 8.6 from one number |
| Estimating pass@k from *n* trials | `\(1 - \binom{n-c}{k}/\binom{n}{k}\)`{=latex}, with *c* passes. Never `\((1-c/n)\)`{=latex} to the *k*, which under-states it every time |
| Twenty steps at 0.95 | `\(0.95^{20} = 0.358\)`{=latex} per trial — and 0.74, 0.36 or 0.05 depending on which of the three you quote |
| Where 0.95 a step becomes a coin | Step 14: `\(0.95^{14} = 0.488\)`{=latex} |
| What a 20-step task needs to finish 9 in 10 | `\(0.90^{1/20} = 0.9947\)`{=latex} a step |
| What *four out of five* is worth | A system at 0.50 shows it 18.8 per cent of the time; one at 0.95 shows it 97.7 per cent. *That result* does not separate them — none of five would, at three in ten million |
| The two graders | Final state, then transcript. On 14 trials: 0.71 against 0.29 |
| Two sets, two targets | Capability well below 1.0 and informative; regression at 1.0 and alarming. Mixed, a −0.033 breakage is netted against a +0.067 gain and reports +0.033 |

### Review Questions

1. Your agent "succeeded four times out of five". What do you need to know before that means
anything?
2. What is pass@k, how does it differ from pass\^k, and which one should worry you?
3. You have run a task five times and it passed twice. Estimate pass@3.
4. Why is a final-state check not enough, and what would you add that does not need a model?
5. Each step of your twenty-step agent is right 95 times in a hundred. How often does a run
finish, and what would you need for nine in ten?
6. Why keep two sets of tasks rather than one, when one bigger set has more cases in it?

### Review Answers

1. Three things, and they are worth saying in this order. **What the five were**: five different
tasks run once each, or one task run five times, or five steps of one run. **Which number it is**:
on one grid of twenty tasks and five trials each, the trial pass rate was 0.65, pass@5 was 0.80
and pass\^5 was 0.45 — all correct, 0.35 of the scale apart, and the one that reads as four out of
five is the highest. **And what graded it**: the final state alone, or the transcript as well. On
fourteen trials of one task those two gave 0.71 and 0.29. If it really is one task run five
times, the arithmetic is unkind: a system that works half the time shows you four of five or
better about one attempt in five, so the result does not distinguish a coin from a system working
95 times in a hundred.
2. pass@k is the chance that at least one of *k* trials succeeds, `\(1-(1-p)^k\)`{=latex}, and it
rises with *k* because extra attempts can only help. pass\^k is the chance that all *k* succeed,
`\(p^k\)`{=latex}, and it falls with *k* because each extra attempt is another chance to fail. At
`\(p=0.65\)`{=latex} and `\(k=5\)`{=latex} they are 0.995 and 0.116 — a factor of 8.6 out of one
rate and one *k*, which is why a quoted figure without its *k* and its name is not a measurement.
**pass\^k is the one to worry about.** pass@k is only a capability when something can tell a good
attempt from a bad one: *k* attempts are worth nothing to a user who cannot see which of them
worked, and that something is Chapter 34's check, the column its rule says to write down before
building an agent at all. Two more things to say unprompted. Estimating pass@k by raising
`\((1-c/n)\)`{=latex} to the *k* is wrong in a fixed direction — picking *k* of your *n* trials is
drawing without replacement, so use `\(1-\binom{n-c}{k}/\binom{n}{k}\)`{=latex}. And a pass@k of
1.000 off a handful of trials means fewer than *k* of them failed, which pins the estimate by
arithmetic.
3. 0.900. With `\(n=5\)`{=latex}, `\(c=2\)`{=latex} and `\(k=3\)`{=latex} the estimate is
`\(1 - \binom{3}{3}/\binom{5}{3} = 1 - 1/10\)`{=latex}. The naive form gives
`\(1 - 0.6^3 = 0.784\)`{=latex}, which is 0.116 low, and the gap is not noise: every factor of
the without-replacement product after the first is smaller than `\((n-c)/n\)`{=latex}, so the
naive form over-states the chance of missing all the passes. Worth adding that five trials is
very little to build a pass@3 on, and that the right follow-up is more trials rather than a
better formula.
4. Because the final state is passed by runs that did the wrong thing on the way. Of ten trials
that left the right final state, six had something wrong with the route — a refund issued twice
and one reversed, a file read that had nothing to do with the task, an order id guessed and never
looked up, the same search eleven times, and two more that code cannot settle. What to add is four code checks on the transcript, none
of which needs a model: count the actions that change something, check every tool name against
the allowed list, check that every id appearing in a call appeared in an earlier result, and
check the step count against the limit. That is Chapter 31's rule — code can decide where the
comparison is between two things both literally present — applied to a transcript instead of an
answer. On fourteen trials those four catch four of the six route failures, which is the figure
going from 0.71 to 0.43; with the final-state check beside them, code settles 8 of the 14 and
leaves 6 for a judge and 1 for a person.
Also say that the final-state check only means anything if the starting state is reset between
trials.
5. `\(0.95^{20} = 0.358\)`{=latex} — about one run in three. For nine in ten at the same length
you need `\(0.90^{1/20} = 0.9947\)`{=latex} a step, which is a different kind of system rather
than a better prompt. Two useful extras: at 0.95 a step the run is worse than a coin from step 14
on, and the same agent can be honestly quoted as 0.74 (pass@3), 0.36 (one trial) or 0.05
(pass\^3). This is Chapter 4's compounding error — a product across the steps inside one trial —
and pass\^k is a product across trials of the whole task; the same shape of arithmetic over two
different things.
6. Because the two sets are read in opposite directions. A capability set holds tasks at the edge
of what the system can do and is supposed to score well below 1.0; a regression set holds tasks
it must not stop doing and is supposed to sit at 1.0. Mixed, a change that fixed two capability
tasks and broke one regression task reported +0.033 across thirty tasks and read as a small win,
where split it was 0.30 to 0.50 — the work landing — and 1.00 to 0.95, a release blocker and a
list of one named case. And the mixing is worse than hiding: the broken task is −0.033 of the
mixed score and the two fixed capability tasks are +0.067, and only the net reaches the mixed
number, so a breakage can be cancelled or inverted by work going well elsewhere and no
threshold on that number separates the two. The other half is
headroom: a capability set at 1.00 has nothing left to register, so it has stopped measuring
rather than become perfect, and the fix is harder tasks.

> **You understand this when** somebody says their agent works four times out of five and you
> ask which of three numbers that is, and what read the transcript.
