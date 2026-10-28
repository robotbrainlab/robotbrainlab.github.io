# Regression Sets, Criteria Drift and Traces

Chapters 30 to 32 built a measurement: failure modes, checks and judges, and the two halves of a
grounded answer. All of it measures one moment. This chapter is about the measurement surviving
contact with time — the set you keep so that a fix cannot quietly break something else, the way
your own standard moves while you are using it, and the per-request record without which none of
it has anything to feed on.

*The problem.* I fixed one thing and broke another, and I only found out from a user.

*The question.* What do you keep, how often do you run it, and how do you notice when the thing
doing the measuring has changed?

## A Score Is a Net; A Regression Set Is a List

The set you run on every change is a **regression set**, and Chapter 20 — which said the set must
not change while you are comparing — handed the business of it growing to this chapter. Here is
why it has to grow, and the mistake the name of the activity invites.

```python
"""Twenty cases across three versions of the same application.

P is pass, F is fail, recorded by the same verdict applied the same
way each time. Version 2 is a change made to fix what version 1 got
wrong; version 3 is a change made after reading what version 2 did.

Written out, so every count below can be had by hand.
"""

#    v1 v2 v3   how many cases of this shape
SHAPES = [
    ("F", "P", "P", 4),   # v2 fixed these
    ("F", "F", "P", 2),   # still wrong in v2, fixed in v3
    ("P", "F", "P", 3),   # v2 BROKE these
    ("P", "P", "P", 9),   # never a problem
    ("F", "F", "F", 2),   # never right
]

CASES = [(a, b, c) for a, b, c, n in SHAPES for _ in range(n)]
N = len(CASES)
VERSIONS = ("v1", "v2", "v3")

def score(v):
    return sum(1 for c in CASES if c[v] == "P")

if __name__ == "__main__":
    assert N == 20
    print(f"  {N} cases, three versions.\n")
    for i, name in enumerate(VERSIONS):
        print(f"    {name}  {score(i)} of {N} pass   {score(i)/N:.0%}")
    print("\n  Read as a score, version 2 is 5 points better than")
    print("  version 1 and that is the whole of what you know.\n")

    fixed = [i for i, c in enumerate(CASES) if c[0] == "F" and c[1] == "P"]
    broke = [i for i, c in enumerate(CASES) if c[0] == "P" and c[1] == "F"]
    print(f"  Read case by case, version 2 fixed {len(fixed)} and broke"
          f" {len(broke)}.")
    print(f"  The score is the net of those two: {score(0)} + {len(fixed)}"
          f" - {len(broke)} = {score(1)}.")
    print("  A score is a net. A regression set is a list, and the")
    print("  list is what you can act on.\n")

    # The set you would have built after reading version 1.
    failed_v1 = [i for i, c in enumerate(CASES) if c[0] == "F"]
    print(f"  Now the trap. After version 1 you keep the cases that")
    print(f"  failed, which is {len(failed_v1)} of the {N}. Run just those")
    print("  against version 2:")
    f_fixed = [i for i in failed_v1 if CASES[i][1] == "P"]
    f_broke = [i for i in failed_v1 if CASES[i][0] == "P"
               and CASES[i][1] == "F"]
    print(f"    {len(f_fixed)} now pass, {len(f_broke)} regressions found.")
    print(f"\n  It reports no regressions, and there were {len(broke)}.")
    print("  They are not in the set and never could be: every one")
    print("  of them PASSED version 1, which is why the set does")
    print("  not contain them. A set of past failures cannot catch")
    print("  a case that has never failed.\n")

    print("  So keeping the cases that failed is necessary and not")
    print("  sufficient. The set has to carry the cases that pass")
    print(f"  as well - here all {N} - or you are blind to the one")
    print("  thing a regression set exists to catch.\n")

    kept = [i for i, c in enumerate(CASES) if "F" in c[:2]]
    print(f"  A middle course: keep every case that has EVER failed,")
    print(f"  which after version 2 is {len(kept)} of {N}. Run that")
    print("  set on the next change and watch what it does NOT")
    print("  say:")
    k_reg = [i for i in kept
             if CASES[i][1] == "P" and CASES[i][2] == "F"]
    k_fix = [i for i in kept
             if CASES[i][1] == "F" and CASES[i][2] == "P"]
    print(f"    {len(k_reg)} regressions, {len(k_fix)} fixes.\n")
    print(f"  Zero regressions again - and this time all {len(broke)} of")
    print("  the breakages ARE in the set. They were failing when")
    print("  the set was taken, so on the next comparison they go")
    print("  from fail to pass and read as FIXES. A before-and-")
    print("  after comparison CANNOT report a case that was")
    print("  already failing as a regression. It reports a")
    print("  standing failure, which is a list somebody has to")
    print("  read rather than an alarm that fires.\n")
    print("  What the middle course actually buys is the change")
    print("  AFTER that one: those cases are in the set now, so")
    print("  the next time one of them breaks it is caught. And")
    print("  notice where they came from - not from this set,")
    print("  which could not see them, but from somebody reading")
    print("  real output. That is chapter 30, and it is why the")
    print("  last section of this chapter is about traces.")
```

```text
  20 cases, three versions.

    v1  12 of 20 pass   60%
    v2  13 of 20 pass   65%
    v3  18 of 20 pass   90%

  Read as a score, version 2 is 5 points better than
  version 1 and that is the whole of what you know.

  Read case by case, version 2 fixed 4 and broke 3.
  The score is the net of those two: 12 + 4 - 3 = 13.
  A score is a net. A regression set is a list, and the
  list is what you can act on.

  Now the trap. After version 1 you keep the cases that
  failed, which is 8 of the 20. Run just those
  against version 2:
    4 now pass, 0 regressions found.

  It reports no regressions, and there were 3.
  They are not in the set and never could be: every one
  of them PASSED version 1, which is why the set does
  not contain them. A set of past failures cannot catch
  a case that has never failed.

  So keeping the cases that failed is necessary and not
  sufficient. The set has to carry the cases that pass
  as well - here all 20 - or you are blind to the one
  thing a regression set exists to catch.

  A middle course: keep every case that has EVER failed,
  which after version 2 is 11 of 20. Run that
  set on the next change and watch what it does NOT
  say:
    0 regressions, 5 fixes.

  Zero regressions again - and this time all 3 of
  the breakages ARE in the set. They were failing when
  the set was taken, so on the next comparison they go
  from fail to pass and read as FIXES. A before-and-
  after comparison CANNOT report a case that was
  already failing as a regression. It reports a
  standing failure, which is a list somebody has to
  read rather than an alarm that fires.

  What the middle course actually buys is the change
  AFTER that one: those cases are in the set now, so
  the next time one of them breaks it is caught. And
  notice where they came from - not from this set,
  which could not see them, but from somebody reading
  real output. That is chapter 30, and it is why the
  last section of this chapter is about traces.
```

**Start with the two readings of version 2.** As a score it is five points better. Case by case it
fixed four and broke three, and the five points are the net of those two. **A score tells you the
net; only a list tells you what to do**, and the three broken cases are three pieces of work that
the score has cancelled against four pieces of good news.

**Then the mistake, which the program is really about.** The obvious set to keep is the cases that
failed — it is what the activity is called, and chapter 30's forty are exactly that. Run that set
against version 2 and it reports four fixes and *no regressions*. There were three. They are not
in the set and never could have been: every one of them *passed* version 1, which is precisely why
a set of past failures does not contain them. A **regression** is a case that passed before a
change and fails after it, so **a set of past failures cannot catch a case that has never
failed.**

**So keeping the cases that failed is necessary and not sufficient.** The set has to carry passing
cases too — and once the set grows, a score *on* it stops being comparable with last month's
score on a smaller set, which is why the thing you report is a list of cases and never a score
movement. The drift section below is the same wound from the other side. Two ways to do that, and they cost differently:

- **Keep everything.** Here that is all twenty, and it catches every regression. It is also the
  whole evaluation set run on every change, which is the cost you are deciding about.
- **Keep every case that has ever failed.** After version 2 that is eleven of the twenty — and run
  it on the next change and it reports *no regressions again*, with five fixes. The three
  breakages are in the set this time, and that is exactly why: they were *failing* when the set
  was taken, so the next comparison sees them go from fail to pass and reads them as fixes. **A
  before-and-after comparison cannot report a case that was already failing as a regression** — it
  reports a standing failure, which is a list somebody reads rather than an alarm that fires. What
  the smaller set buys is the change *after* that one: those cases are in it now, so the next time
  one of them breaks it is caught.

> **Note:** And notice where the three new cases came from. Not from the eight-case set, which
> could not see them — from somebody reading real output, which is Chapter 30 and the reason the
> last section of this chapter is about traces. A smaller set is one change behind only for the
> breakages you learn about by some other route; one that nobody ever notices never enters it at
> all, which is this chapter's opening problem.

> **Note:** Neither option is "the regression set", and the choice is a budget rather than a
> principle. What is not negotiable is that a set made only of past failures reports *no
> regressions* with a confidence it has not earned — which is worse than reporting nothing,
> because it reads as a green light. That blindness is specific: it is a blindness to cases that
> have *never* failed, and it does not expire: such a case stays outside the set until it fails
> and somebody notices by another route.

> **Tip:** When does it run? On every change you would otherwise have to remember to check:
> prompt, model, retrieval settings, chunking, the documents themselves. Chapter 20's point about
> treating every change as an experiment is the same point from the other end — if it is worth
> changing, it is worth knowing what it broke.

## Running It Once Is Not Running It

A regression comparison is two scores subtracted, and Chapter 20 already said what one run of one
score is worth. What that does to a *comparison* is worse than what it does to a score, and it is
worth seeing.

```python
"""The same twenty cases, run five times against each of two versions.


Each row is one case and five runs, recorded. Version B is a change
made to fix case 19. Chapter 20 owns trials and what they measure;
what this program is about is what happens to a REGRESSION comparison
when you run the set once.
"""

from itertools import combinations

GRID_A = """
PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP
PPPPP PPPPP PPPPP PPPPP PPPPP PFPFP FPPFP PPFPF FFPFF FFFFF
"""
GRID_B = """
PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP PPPPP
PPPPP PPPPP PPPPP PPPPP PPPPP FPPPF PFPFP FPPFP FPFFF PPPPP
"""

def rows(grid):
    return grid.split()

A, B = rows(GRID_A), rows(GRID_B)
N, RUNS = len(A), len(A[0])

def majority(row):
    return "P" if row.count("P") * 2 > RUNS else "F"

def sub_verdict(row, idx, tie_fails):
    """The verdict over a chosen subset of the runs. `tie_fails` is the
    decision this chapter is about: when half the runs failed, is that
    a regression? The rule stated above says no - a case is not a
    regression until it fails MORE often than it passed - and the
    first version of this program said yes. The table below is why
    that mattered more than the number of repeats did."""
    picked = [row[i] for i in idx]
    fails = len(picked) - picked.count("P")
    if fails * 2 > len(picked):
        return "F"
    if fails * 2 == len(picked) and tie_fails:
        return "F"
    return "P"

def say(n, one, many):
    return f"{n} {one if n == 1 else many}"

if __name__ == "__main__":
    assert N == 20 and len(B) == N and RUNS == 5
    assert all(len(r) == RUNS for r in A + B)

    print(f"  {N} cases, {RUNS} runs of each against each version.\n")
    flaky = [i for i in range(N)
             if 0 < A[i].count("P") < RUNS or 0 < B[i].count("P") < RUNS]
    print(f"  {N - len(flaky)} cases gave the same verdict all five times.")
    print(f"  {len(flaky)} did not: cases {flaky}.\n")

    print("  First, compare one run against one run - run 1 of each,")
    print("  which is what a regression set run once gives you.")
    for r in range(RUNS):
        broke = [i for i in range(N) if A[i][r] == "P" and B[i][r] == "F"]
        fixed = [i for i in range(N) if A[i][r] == "F" and B[i][r] == "P"]
        tag = "   <- the run you did" if r == 0 else ""
        print(f"    run {r+1}: {say(len(broke), 'regression', 'regressions')},"
              f" {say(len(fixed), 'fix', 'fixes')}{tag}")

    print("\n  Now compare the majority of five against the majority")
    print("  of five:")
    mb = [i for i in range(N)
          if majority(A[i]) == "P" and majority(B[i]) == "F"]
    mf = [i for i in range(N)
          if majority(A[i]) == "F" and majority(B[i]) == "P"]
    print(f"    {say(len(mb), 'regression', 'regressions')},"
          f" {say(len(mf), 'fix', 'fixes')}: cases {mf}.\n")

    print("  Case 19 is the change. It is the only thing version B")
    print("  did, and the five-run comparison says so. Every other")
    print("  regression and fix any single run reported came from")
    print("  cases 15 to 18, which are not stable in EITHER")
    print("  version - so the comparison was reporting the dice.\n")

    worst = max(
        sum(1 for i in range(N) if A[i][r] == "P" and B[i][r] == "F")
        for r in range(RUNS))
    anyspur = sum(
        1 for r in range(RUNS)
        if any(A[i][r] == "P" and B[i][r] == "F" for i in range(N)))
    print(f"  Of the {RUNS} runs available, {anyspur} would have reported")
    print(f"  at least one regression that is not there, and the")
    print(f"  worst of them would have reported {worst}.\n")

    print("  The rule that follows is narrow and cheap: a case is")
    print("  not a regression until it fails more often than it")
    print("  passed. Which is chapter 20's trials, applied to a")
    print("  comparison rather than to a score - and the reason a")
    print("  regression set is run with repeats and not once.\n")

    print("  How many repeats is the next question, and the five")
    print("  runs here can answer it, because every smaller")
    print("  number of repeats is a subset of them. Both columns")
    print("  count the ways of picking k runs that report a")
    print("  regression which is not there.\n")
    print("    repeats   of   tie reads FAIL   tie reads PASS")
    for k in (2, 3, 4, 5):
        subs = list(combinations(range(RUNS), k))
        row = []
        for tie_fails in (True, False):
            row.append(sum(1 for idx in subs if any(
                sub_verdict(A[i], idx, tie_fails) == "P"
                and sub_verdict(B[i], idx, tie_fails) == "F"
                for i in range(N))))
        print(f"    {k:^7d} {len(subs):^5d} {row[0]:^15d}"
              f" {row[1]:^15d}".rstrip())
    print("\n  Read the two columns against each other, because")
    print("  that is the finding: at FOUR repeats the same data")
    print("  gives 5 of 5 or 0 of 5 depending on nothing but how")
    print("  a two-two split is read. The tie-break matters more")
    print("  than the number of repeats does, and the chapter")
    print("  stated the right one twice before this program got")
    print("  it wrong: a case is not a regression until it fails")
    print("  MORE often than it passed, so a two-two split is")
    print("  not one.\n")
    print("  With the rule applied properly, the right-hand")
    print("  column is what you get: two repeats leaves 6 of 10")
    print("  and three leaves 7 of 10, so the cheap answer is")
    print("  not an answer on this set, and four clears it. Do")
    print("  not carry 'four' anywhere - the number is a fact")
    print("  about four cases that are unstable here. Chapter")
    print("  20's 'two or three, then stop' was derived for")
    print("  averaging WITHIN a case to narrow a score, which is")
    print("  a different quantity from a per-case verdict.\n")
    print("  What to carry is the other half: a case near")
    print("  fifty-fifty crosses any threshold you set, whatever")
    print("  you spend on repeats. Those four cases are the")
    print("  finding. Fix them or take them out of the set.")
```

```text
  20 cases, 5 runs of each against each version.

  16 cases gave the same verdict all five times.
  4 did not: cases [15, 16, 17, 18].

  First, compare one run against one run - run 1 of each,
  which is what a regression set run once gives you.
    run 1: 2 regressions, 2 fixes   <- the run you did
    run 2: 1 regression, 3 fixes
    run 3: 1 regression, 2 fixes
    run 4: 1 regression, 2 fixes
    run 5: 1 regression, 2 fixes

  Now compare the majority of five against the majority
  of five:
    0 regressions, 1 fix: cases [19].

  Case 19 is the change. It is the only thing version B
  did, and the five-run comparison says so. Every other
  regression and fix any single run reported came from
  cases 15 to 18, which are not stable in EITHER
  version - so the comparison was reporting the dice.

  Of the 5 runs available, 5 would have reported
  at least one regression that is not there, and the
  worst of them would have reported 2.

  The rule that follows is narrow and cheap: a case is
  not a regression until it fails more often than it
  passed. Which is chapter 20's trials, applied to a
  comparison rather than to a score - and the reason a
  regression set is run with repeats and not once.

  How many repeats is the next question, and the five
  runs here can answer it, because every smaller
  number of repeats is a subset of them. Both columns
  count the ways of picking k runs that report a
  regression which is not there.

    repeats   of   tie reads FAIL   tie reads PASS
       2     10          8               6
       3     10          7               7
       4      5          5               0
       5      1          0               0

  Read the two columns against each other, because
  that is the finding: at FOUR repeats the same data
  gives 5 of 5 or 0 of 5 depending on nothing but how
  a two-two split is read. The tie-break matters more
  than the number of repeats does, and the chapter
  stated the right one twice before this program got
  it wrong: a case is not a regression until it fails
  MORE often than it passed, so a two-two split is
  not one.

  With the rule applied properly, the right-hand
  column is what you get: two repeats leaves 6 of 10
  and three leaves 7 of 10, so the cheap answer is
  not an answer on this set, and four clears it. Do
  not carry 'four' anywhere - the number is a fact
  about four cases that are unstable here. Chapter
  20's 'two or three, then stop' was derived for
  averaging WITHIN a case to narrow a score, which is
  a different quantity from a per-case verdict.

  What to carry is the other half: a case near
  fifty-fifty crosses any threshold you set, whatever
  you spend on repeats. Those four cases are the
  finding. Fix them or take them out of the set.
```

**Four of the twenty cases are not stable in either version**, and they are the whole story. The
single-run comparison reports two regressions and two fixes; the five-run comparison reports no
regressions and one fix. **Only one of those things happened.** Every other regression and fix
that a single run reported came from the four unstable cases, so the comparison was reporting the
dice rather than the change.

**And every one of the five available runs would have reported at least one regression that is not
there.** Not the unlucky run — all five. A single-run regression comparison on this set does not
have a good day.

**The rule that follows is narrow and cheap: a case is not a regression until it fails more often
than it passed.** That is Chapter 20's trials, applied to a comparison instead of to a score, and
it is the reason a regression set is run with repeats rather than once.

**How many repeats is a separate question, and the five runs answer it, because every smaller
number of repeats is a subset of them — but the answer turns out not to be a number.** At four
repeats the same data reports a regression that is not there on 5 of the 5 ways to pick them, or
on 0 of 5, **depending on nothing but how a two-two split is read.** The tie-break matters more
than the count does, and this chapter had already stated the right one twice before its own
program got it wrong: a case is not a regression until it fails *more often* than it passed, so
a two-two split is not one.

**With the rule applied properly, two repeats leaves 6 of 10 and three leaves 7 of 10**, so the
cheap answer is not an answer on this set, and four clears it. Do not carry *four* anywhere: that
number is a fact about the four cases that are unstable here. Chapter 20's *two or three, then
stop* was derived for averaging within a case to narrow a score, which is a different quantity
from a per-case verdict. **What to carry is the other half** — a case near fifty-fifty crosses any
threshold you set, whatever you spend on repeats, so those four cases are the finding. Fix them
or take them out of the set.

> **Warning:** The failure this prevents is specific and it is expensive. A spurious regression
> sends somebody to debug a case that was never broken, and when they find nothing wrong the
> lesson they learn is that the regression set cries wolf. A set nobody believes is worse than no
> set, because it still costs the run.

## Criteria Drift

Now the part that is hardest to believe until you have measured it: the thing doing the measuring
moves.

```python
"""Forty outputs, labelled twice by the same person a month apart.

Nothing about the outputs changed between the two passes. The second
pass was done without looking at the first, which is the only way the
count at the bottom means anything.
"""

#    week 1, week 5   how many
SHAPES = [
    ("P", "P", 28),   # pass both times
    ("P", "F",  6),   # passed then, fails now
    ("F", "P",  1),   # failed then, passes now
    ("F", "F",  5),   # fail both times
]

PAIRS = [(a, b) for a, b, n in SHAPES for _ in range(n)]
N = len(PAIRS)

def score(i):
    return sum(1 for p in PAIRS if p[i] == "P")

if __name__ == "__main__":
    assert N == 40
    stricter = sum(1 for a, b in PAIRS if a == "P" and b == "F")
    looser = sum(1 for a, b in PAIRS if a == "F" and b == "P")
    print(f"  {N} outputs, labelled twice, unchanged in between.\n")
    print(f"    week 1:  {score(0)} of {N} pass   {score(0)/N:.1%}")
    print(f"    week 5:  {score(1)} of {N} pass   {score(1)/N:.1%}\n")
    print(f"  The same outputs, {abs(score(0)-score(1))/N:.1%} apart.")
    print("  Nothing was deployed and nothing was fixed. What moved")
    print("  is the person holding the standard.\n")

    print(f"  {stricter + looser} of the {N} labels changed:"
          f" {stricter} became FAIL and {looser}")
    print("  became PASS. That is the number to keep. The")
    print("  direction is worth noticing and this set cannot")
    print("  settle it: 6 of 7 one way would come up about once")
    print("  in eight from a fair coin, which is chapter 20's")
    print("  question and not a finding here. The argument for a")
    print("  direction is the mechanism rather than the count.")
    print("  Reading output teaches you what to look for, and")
    print("  much of what you learn is a new way for an answer to")
    print("  be wrong - so a standard that moves has a reason to")
    print("  move one way, and that way flatters the past.\n")

    print("  What this costs you is any comparison across time. If")
    print(f"  version A was scored in week 1 at {score(0)/N:.1%} and")
    print("  version B is scored in week 5, the difference between")
    print("  them contains a change you made and a change you")
    print(f"  underwent, and on this set the second one is {abs(score(0)-score(1))/N:.1%}.")
    print("  A 5-point improvement measured that way sits well")
    print("  inside your own drift.\n")

    print("  How to notice it is the whole of the method, and it")
    print("  is cheap: keep the old labels, and re-label a sample")
    print("  of old outputs WITHOUT looking at what you said last")
    print("  time. The flip count is your drift. Looking first")
    print("  does not measure anything, because you will agree")
    print("  with yourself.\n")

    print("  And when the flips go one way, you have learned a")
    print("  criterion you did not have before. Write it down and")
    print("  re-label the whole set against it, or you have two")
    print("  standards in one set and no way to tell which case")
    print("  was judged by which.")
```

```text
  40 outputs, labelled twice, unchanged in between.

    week 1:  34 of 40 pass   85.0%
    week 5:  29 of 40 pass   72.5%

  The same outputs, 12.5% apart.
  Nothing was deployed and nothing was fixed. What moved
  is the person holding the standard.

  7 of the 40 labels changed: 6 became FAIL and 1
  became PASS. That is the number to keep. The
  direction is worth noticing and this set cannot
  settle it: 6 of 7 one way would come up about once
  in eight from a fair coin, which is chapter 20's
  question and not a finding here. The argument for a
  direction is the mechanism rather than the count.
  Reading output teaches you what to look for, and
  much of what you learn is a new way for an answer to
  be wrong - so a standard that moves has a reason to
  move one way, and that way flatters the past.

  What this costs you is any comparison across time. If
  version A was scored in week 1 at 85.0% and
  version B is scored in week 5, the difference between
  them contains a change you made and a change you
  underwent, and on this set the second one is 12.5%.
  A 5-point improvement measured that way sits well
  inside your own drift.

  How to notice it is the whole of the method, and it
  is cheap: keep the old labels, and re-label a sample
  of old outputs WITHOUT looking at what you said last
  time. The flip count is your drift. Looking first
  does not measure anything, because you will agree
  with yourself.

  And when the flips go one way, you have learned a
  criterion you did not have before. Write it down and
  re-label the whole set against it, or you have two
  standards in one set and no way to tell which case
  was judged by which.
```

**The same forty outputs, unchanged, scored 85 per cent in week 1 and 72.5 per cent in week 5.**
Nothing was deployed and nothing was fixed. Seven labels changed, six of them from pass to fail.
That is **criteria drift**: your standard moving as you see more output, and it moves because
reading output teaches you what to look for.

**What it costs is any comparison across time.** A version scored in week 1 against a version
scored in week 5 differs by a change you made *and* a change you underwent, and on this set the
second is 12.5 points. A five-point improvement measured that way sits well inside it.

**How to notice it is the whole of the method, and it is cheap.** Keep the old labels. Re-label a
sample of old outputs **without looking at what you said last time**, and count the flips. That
count is your drift. Looking first measures nothing, because you will agree with yourself —
which is the same anchoring problem Chapter 31 handles for a judge by showing it the same answer
twice.

**And when the flips go one way, you have learned a criterion.** That is good news badly packaged:
write the criterion down and re-label the whole set against it, or you have two standards inside
one set and no way to tell which case was judged by which.

> **Note:** The direction is worth noticing and this set cannot settle it. Six of seven flips one
> way comes up about once in eight from a fair coin, so the count is suggestive and Chapter 20
> owns the question of whether it is real. The argument for a direction is the mechanism: most of
> what reading output teaches you is a new way for an answer to be wrong, and a standard that
> moves for that reason moves one way — which flatters the past.

> **Warning:** Drift is not a mistake to be eliminated, and it is a property of a *person's*
> judgement rather than of measurement. A check written in code does not move on its own, and any
> change to it is an edit you can see — which is one of Chapter 31's reasons for preferring code
> wherever code can decide, and Chapter 20's requirement that the same answer twice gets the
> same verdict twice is the same preference from the other end. What has to be eliminated is
> *silent* drift: the version where the standard moves, nobody counts it, and the movement is
> reported as progress.

> **Note:** Two cases sit outside that. A code check comparing an answer against your documents
> *does* change verdict when the documents change, silently — the hazard the trace section names
> again. And a model judge is neither a person nor code: it does not learn a new criterion, but
> shown the same answer twice it held its verdict on only 17 of 20 in Chapter 31, so its standard
> is unrepeatable rather than learned — and it moves outright when the model under it changes,
> which is Chapter 54's. Where a person is judging, a standard that stopped moving would more likely mean
> you had stopped reading output than that you had got it right. What has to be eliminated is *silent*
> drift: the version where the standard moves, nobody counts it, and the movement is reported as
> progress.

## Traces, and What You Decide Not to Capture

Everything above runs on cases, and cases come from somewhere. A **trace** is the record of one
request through the application, and it is where cases come from — which makes the decision about
what a trace holds a decision about what you can measure later.

Keeping these records and being able to read them is what the field calls **observability**,
and *tracing* is the part of it this section is about. An interviewer asking whether you have
observability is asking whether a request that went wrong can be reconstructed after the fact.

```python
"""One request's trace, and the decision about what goes in it.

The trace is a record of one request through the application. FIELDS
lists what this one captures; CONTENT marks the fields that hold text
somebody typed or that came out of your documents. QUESTIONS is what
you might need the trace to answer later, and which fields each needs.
"""

FIELDS = {
    "request_id":      "7f3a1c",
    "at":              "2026-10-28T09:14:02Z",
    "user":            "u_8812",
    "question":        "when do I get my refund",
    "retrieval_query": "when do I get my refund",
    "candidates":      "[(refunds.pdf#2, 0.81), (shipping.pdf#1, 0.44)]",
    "passages_sent":   "[refunds.pdf#2]",
    "model":           "a-model-id-and-version",
    "prompt_tokens":   "1180",
    "output_tokens":   "96",
    "tool_calls":      "[lookup_order(8812) -> 14ms]",
    "output":          "Refunds are issued within 14 days of...",
    "retrieval_ms":    "38",
    "model_ms":        "1420",
    "total_ms":        "1502",
    "verdict":         "fail - contradicts the passage",
}

CONTENT = {"question", "retrieval_query", "passages_sent", "output"}

QUESTIONS = [
    ("Which stage was slow?", {"retrieval_ms", "model_ms", "total_ms"}),
    ("What did this request cost?", {"prompt_tokens", "output_tokens"}),
    ("Did retrieval return the right passage?", {"candidates"}),
    ("Was the model the one I think it was?", {"model"}),
    ("Why did it say that?", {"passages_sent", "output"}),
    ("Can this become a regression case?", {"question", "output"}),
    ("Is this the same failure as yesterday's?", {"output"}),
    ("How many users hit this?", {"user", "verdict"}),
]

if __name__ == "__main__":
    print(f"  One trace, {len(FIELDS)} fields,"
          f" {len(CONTENT)} of them content.\n")
    for k, v in FIELDS.items():
        mark = "  <- content" if k in CONTENT else ""
        print(f"    {k:17s} {v[:30]}{mark}")

    print("\n  Now drop every content field - keep the ids, the")
    print("  counts, the timings and the verdict - and ask what")
    print("  the trace can still answer.\n")
    kept = set(FIELDS) - CONTENT
    for q, needs in QUESTIONS:
        ok = needs <= kept
        print(f"    {'yes' if ok else 'NO '}  {q}")

    lost = [q for q, needs in QUESTIONS if not needs <= kept]
    print(f"\n  {len(QUESTIONS) - len(lost)} of {len(QUESTIONS)} survive."
          f" The {len(lost)} that do not are these:")
    for q in lost:
        print(f"    {q}")

    print("\n  Read that list and the shape of the decision shows.")
    print("  What survives is everything that needs only ids,")
    print("  counts and timings - including one real evaluation")
    print("  question, whether retrieval returned the right")
    print("  passage, which a document id answers with no text")
    print("  at all. What is lost is everything that needs the")
    print("  TEXT: why it said that, whether it is the same")
    print("  failure as yesterday's, and whether this can become")
    print("  a regression case - because a case needs an input")
    print("  and an output to be a case at all. So the content")
    print("  fields are what links a trace to a regression set.\n")

    print("  Which is why the decision is a decision and not a")
    print("  default. What it is NOT is all-or-nothing: ids,")
    print("  counts and timings on every request cost very")
    print("  little and answer most of the list, and content on a")
    print("  sample - with a window after which it is deleted -")
    print("  buys the other half at a fraction of the exposure.")
    print("  Sample within the failures rather than across every")
    print("  request: chapter 30 needs forty failures, taken at")
    print("  random from them, and not forty thousand successes.\n")

    print("  Three fields are worth naming as ones to think")
    print("  twice about. The whole document a passage came from,")
    print("  because you already have it and the id finds it -")
    print("  unless your documents change under you, in which")
    print("  case the id no longer finds what was SENT, and the")
    print("  passage text is the only record of it. Anything a")
    print("  caller sent you as a credential. And anything you")
    print("  cannot delete on request, which is a property of")
    print("  where you put the trace rather than of the field.")
```

```text
  One trace, 16 fields, 4 of them content.

    request_id        7f3a1c
    at                2026-10-28T09:14:02Z
    user              u_8812
    question          when do I get my refund  <- content
    retrieval_query   when do I get my refund  <- content
    candidates        [(refunds.pdf#2, 0.81), (shipp
    passages_sent     [refunds.pdf#2]  <- content
    model             a-model-id-and-version
    prompt_tokens     1180
    output_tokens     96
    tool_calls        [lookup_order(8812) -> 14ms]
    output            Refunds are issued within 14 d  <- content
    retrieval_ms      38
    model_ms          1420
    total_ms          1502
    verdict           fail - contradicts the passage

  Now drop every content field - keep the ids, the
  counts, the timings and the verdict - and ask what
  the trace can still answer.

    yes  Which stage was slow?
    yes  What did this request cost?
    yes  Did retrieval return the right passage?
    yes  Was the model the one I think it was?
    NO   Why did it say that?
    NO   Can this become a regression case?
    NO   Is this the same failure as yesterday's?
    yes  How many users hit this?

  5 of 8 survive. The 3 that do not are these:
    Why did it say that?
    Can this become a regression case?
    Is this the same failure as yesterday's?

  Read that list and the shape of the decision shows.
  What survives is everything that needs only ids,
  counts and timings - including one real evaluation
  question, whether retrieval returned the right
  passage, which a document id answers with no text
  at all. What is lost is everything that needs the
  TEXT: why it said that, whether it is the same
  failure as yesterday's, and whether this can become
  a regression case - because a case needs an input
  and an output to be a case at all. So the content
  fields are what links a trace to a regression set.

  Which is why the decision is a decision and not a
  default. What it is NOT is all-or-nothing: ids,
  counts and timings on every request cost very
  little and answer most of the list, and content on a
  sample - with a window after which it is deleted -
  buys the other half at a fraction of the exposure.
  Sample within the failures rather than across every
  request: chapter 30 needs forty failures, taken at
  random from them, and not forty thousand successes.

  Three fields are worth naming as ones to think
  twice about. The whole document a passage came from,
  because you already have it and the id finds it -
  unless your documents change under you, in which
  case the id no longer finds what was SENT, and the
  passage text is the only record of it. Anything a
  caller sent you as a credential. And anything you
  cannot delete on request, which is a property of
  where you put the trace rather than of the field.
```

**Read the field list first, because the shape of a trace is the teaching.** It is not a log line.
It records the input, what retrieval was asked and what it returned with scores, which model and
version, each tool call, the output, the tokens and the time per stage. Every one of those is
there because some question needs it, and the program's second half is that mapping made explicit.

**Then the content decision.** Four of the sixteen fields hold free text — what somebody typed,
what came out of your documents, and what the model wrote. Drop them and five of the eight questions survive — including one real evaluation
question, whether retrieval returned the right passage, because a document id answers that without
any text at all. What is lost is everything that needs the text: why it said that, whether this is
the same failure as yesterday's, and whether this can become a regression case. Chapter 20 defines a case as an input plus whatever marks the
answer right or wrong, and this chapter's first step keeps the output beside it; *the input is
content either way* — so a content-free trace cannot feed the set
this chapter
opened with.

**Which is why it is a decision and not a default, and why it is not all-or-nothing.** Ids, counts
and timings on every request cost very little and answer most of the list. Content on a *sample*,
with a window after which it is deleted, buys the rest at a fraction of the exposure — and sample
*within* the failures rather than across every request, because Chapter 30 needs forty failures
and not forty thousand successes.

**And content-free is not the same as low exposure.** The fields that survive still put a user id
beside a timestamp and a verdict, which identifies a person without a word of text — so the
deletion question applies to a content-free trace too.

**Three fields are worth naming as ones to think twice about.** The whole document a passage came
from, because you already have it and the id finds it — *unless your documents change under you*,
in which case the id no longer finds what was sent and the passage text is the only record of it. Anything a caller sent as a credential. And
anything you cannot delete on request — which is a property of where you put the trace rather
than of the field, and the reason that choice belongs with the schema rather than after it.

> **Note:** Chapter 54 attributes a failure using traces and owns what happens when a provider
> changes under you, including where your customers' text goes once you send it. This chapter owns
> only what your own trace holds and why.

## What To Actually Do

1. **Keep every case that has ever failed**, with its input, its output and the verdict. That is
   the minimum, and the chapter's first program is why it is not enough.
2. **Add passing cases until the set covers the behaviour you would notice breaking.** If you can
   afford the whole evaluation set, run the whole evaluation set.
3. **Run it on every change you would otherwise have to remember to check** — prompt, model,
   retrieval settings, chunking, the documents.
4. **Run each case more than once** and call a case a regression only when it fails *more often*
   than it passed — a tie is not a regression, and that rule matters more than the count does.
   One run of a comparison reports the dice.
5. **Report regressions as a list of cases, never as a score movement.** The score is a net and
   hides the trade.
6. **Keep your old labels, with their dates.** The date is what makes a flip count mean anything.
7. **Re-label a sample of old outputs blind**, on a schedule, and count the flips. That count is
   your drift, and it belongs beside any improvement you report.
8. **When the flips go one way, write the new criterion down** and re-label the whole set against
   it. Two standards in one set is the state to avoid.
9. **Trace every one of your requests** with ids, retrieval candidates and scores, model and tool
   calls, tokens and per-stage timings. That part is cheap and answers most operational questions.
10. **Decide the content fields deliberately**: which text you keep, for how long, on what sample,
    and where. Write the decision down beside the schema, because it is the ceiling on what you
    can measure later.

> **Tip:** Steps 6 and 7 are the two that get skipped, and they are the cheapest on the list. A
> dated label costs a column. A blind re-label of twenty old outputs costs an hour and is the only
> thing that will ever tell you your improvement was your own standard moving.

## Lab: The Set, the Dice and the Drift

Four programs, pure Python, nothing to install. About fifty minutes, and there is a key for every
step. Work in a new empty folder. None of them imports another, so save each one as you reach it:

| Save as | Which block |
|---|---|
| `regress.py` | the first |
| `trials.py` | the second |
| `drift.py` | the third |
| `trace.py` | the fourth |

**Step 1.** Save `regress.py` and run it. Read the five shapes in the source before the output.

*Expected result:* 60, 65 and 90 per cent across the three versions; version 2 fixed 4 and broke
3; the past-failures set of 8 reports 4 fixes and 0 regressions.

**Step 2.** Make version 2 a pure improvement: change `("P", "F", "P", 3)` to `("P", "P", "P", 3)`
and run it.

*Expected result:* version 2 now scores 80 per cent, 0 regressions, and the past-failures set
reports the same 4 fixes it did before. **The set gave the right answer this time and it was not
doing any more work** — it cannot distinguish "no regressions" from "no regressions I can see",
and nothing in its output marks the difference.

**Step 3.** Put it back. Now make the regression worse than the fix: change the fix shape to
`("F", "P", "P", 1)`, the regression shape to `("P", "F", "P", 5)` and the always-pass shape to
`("P", "P", "P", 10)`, so the twenty cases still add up.

*Expected result:* version 1 at 75 per cent, version 2 down to 11 of 20 at 55, with 1 fix and 5
regressions — and the past-failures set, now only 5 cases, *still reports 0 regressions*. The
blindness does not scale with how bad the regression is. If you forget the third edit, the
program's `assert N == 20` stops it, which is what that line is for. **And read the program's own
narration while you are here:** it still prints *version 2 is 5 points better than version 1*,
because that sentence is a fixed string and version 2 is now 20 points worse. Every one of these
lab edits does that somewhere, which is the moving-denominator problem of Chapter 32's step 5 in
a new place.

**Step 4.** Save `trials.py` and run it.

*Expected result:* 4 unstable cases; run 1 reports 2 regressions and 2 fixes; all five runs report
at least one regression; the five-run majority reports 0 regressions and 1 fix, case 19.

**Step 5.** Make the flaky cases flakier: in `GRID_A`, change case 15's row from `PFPFP` to
`PFFPF`, which drops it to 2 of 5.

*Expected result:* the majority comparison now reports case 15 as a *fix*, because its majority
verdict in A has crossed from pass to fail while B's has not. A case sitting near the majority
threshold crosses it for free, so repeats move the problem rather than removing it — and the cases
that do that are the ones worth fixing or removing from the set. The same threshold hides the
opposite case just as quietly: a case that passed reliably in A and fails two times in five in B
keeps a majority of pass and is reported as no regression, though the change made it fail forty
per cent of the time.

**Step 6.** Save `drift.py` and run it. Then change the drift to go the other way: swap the counts,
`("P", "F", 1)` and `("F", "P", 6)`.

*Expected result:* the two weeks swap — 72.5 per cent then 85.0 — with the same 7 flips and the
same 12.5-point gap, now in the other direction. **The flip count does not care which way the
standard moved**, so the two numbers are for different things: the flip count says how
unrepeatable your judgement is, and the *net* movement says how much it biases a score measured
across time. Six flips each way would be twelve flips of drift and no bias at all. Keep both.

**Step 7.** In `drift.py`, make the two passes agree: `("P", "F", 0)` and `("F", "P", 0)`, with the
stable counts raised to 34 and 6.

*Expected result:* both weeks at 85 per cent and 0 flips. That is what a set with a stable standard
looks like, and it is the only state in which a comparison across time means anything.

**Step 8.** Save `trace.py` and run it. Read the sixteen fields and decide, before the second half
prints, which ones you would drop.

*Expected result:* 5 of 8 questions survive without the content fields, and the 3 that do not are
the ones needing the text.

**Step 9.** Drop the `candidates` field from `CONTENT`'s complement by adding it to `CONTENT`, and
run it.

*Expected result:* "Did retrieval return the right passage?" now fails too, so 4 of 8 survive. A
document id is not content, and treating it as content costs you the one evaluation question a
content-free trace could still answer.

**Step 10.** Add a question of your own to `QUESTIONS` — "Which version of the prompt produced
this?" — and work out which field it needs.

*Expected result:* no field in the list answers it. The trace records the model and version and
not the prompt version, which Chapter 54 treats as part of one versioned artefact. A question with
no field is how you find the field you forgot.

## Summary, Key Terms, and Review Questions

### Summary

Chapters 30 to 32 measure one moment; this chapter is about the measurement surviving time.

**A score is a net and a regression set is a list.** Version 2 of the chapter's twenty cases is
five points better and that figure is four fixes minus three breakages. The mistake almost
everybody makes is the obvious one: keep the cases that failed. Run that set against version 2 and
it reports four fixes and **no regressions**, when there were three — they are not in the set and
never could have been, because every one of them *passed* version 1. **A set of past failures
cannot catch a case that has never failed.** So the set carries passing cases too: everything, or
every case that has *ever* failed. Run that on the next change and it reports no regressions
again, because the three breakages were *failing* when the set was taken, so they read as fixes:
**a before-and-after comparison cannot report an already-failing case as a regression.** What the
smaller set buys is the change after that one.

**Running it once is not running it.** Four of the twenty cases are unstable in both versions, and
a single-run comparison reports two regressions and two fixes where the five-run majority reports
one fix. All five available runs would have reported a regression that is not there. **A case is
not a regression until it fails more often than it passed** — Chapter 20's trials applied to a
comparison rather than a score. The cost of getting this wrong is not a wrong number; it is
somebody debugging a case that was never broken, and a set nobody believes afterwards.

**Criteria drift is the measurement moving.** The same forty outputs, unchanged, scored 85 per cent
in week 1 and 72.5 in week 5, with seven labels changed and six of them from pass to fail. That
destroys any comparison across time: a version scored in week 1 against one scored in week 5
differs by a change you made and a change you underwent, 12.5 points of it here. Notice it by
keeping the old labels and re-labelling a sample **blind** — looking first measures nothing,
because you will agree with yourself. When the flips go one way you have learned a criterion:
write it down and re-label the whole set, or you have two standards in one set. Drift is not a
mistake to eliminate, and it belongs to a person's judgement rather than to a check in code,
which does not move on its own. **Silent** drift is the thing to eliminate — including a code
check whose documents changed under it.

**A trace is the record of one request, and it is where cases come from.** Input, retrieval query
and candidates with scores, model and version, tool calls, output, tokens, per-stage timings. Four
of the chapter's sixteen fields hold text; drop them and five of eight questions survive —
including whether retrieval returned the right passage, which a document id answers with no text.
What is lost is everything needing the text, and **a case needs an input and an output to be a
case**, so a content-free trace cannot feed a regression set. The decision is not all-or-nothing:
ids, counts and timings on everything; content on a sample of the *failures*, with a deletion
window. And three fields to think twice about — the whole source document unless your documents
change under you, anything sent as a credential,
and anything you cannot delete on request.

### Key Terms

| Term | Meaning |
|---|---|
| **Regression set** | The cases you run on every change. Past failures are the minimum and cannot catch a case that has never failed, so it carries passing cases too |
| **Regression** | A case that passed before the change and fails after it — established over repeated runs, not from one |
| **Criteria drift** | Your own standard moving as you see more output, measured by re-labelling old outputs blind and counting the flips |
| **Trace** | The record of one request: input, retrieval and its candidates, model and version, tool calls, output, tokens and per-stage timings |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Score against list | A score is the net of fixes and breakages. Version 2 was +1 case = 4 fixed − 3 broken, which is +5 points on twenty cases |
| The blind spot in a failures-only set | It reported 0 regressions when there were 3, because all three passed the previous version |
| The two honest sets | Everything, or every case that has ever failed — the second reports the breakage it missed as a standing failure, not as a regression, and catches the NEXT breakage of that case |
| When a case is a regression | When it fails *more often* than it passed — a tie is not one, and that tie-break moved this set's result from 5 of 5 to 0 of 5 at four repeats |
| What one run costs | 2 regressions and 2 fixes reported against 1 real fix; all 5 available runs reported a regression that was not there |
| Criteria drift, measured | The same 40 outputs: 85% in week 1, 72.5% in week 5, 7 flips, 6 of them to fail |
| How to measure drift | Re-label a sample of old outputs without looking at the old label, and count the flips |
| What a trace holds | Input, retrieval query and candidates with scores, model and version, tool calls, output, tokens, per-stage timings |
| The content trade | Drop the 4 content fields of 16 and 5 of 8 questions survive; the 3 lost are the ones needing the text, including whether a case can exist at all |

### Review Questions

1. What goes into a regression set, and when does it run?
2. What is criteria drift, and how do you notice it?
3. What do you record in a trace, and what do you deliberately not record?
4. Your regression set has reported no regressions for three months. What do you check?
5. A colleague says the application is 8 points better than last quarter. What do you ask?

### Review Answers

1. Every case that has ever failed — input, output and verdict — and enough passing cases to cover
the behaviour you would notice breaking. The first half is what the activity is called and it is
the trap: a set of past failures **cannot catch a case that has never failed**, which is not a
subtlety but arithmetic. In the chapter's twenty cases, version 2 fixed four and broke three, and
the past-failures set of eight reported four fixes and zero regressions, because all three
breakages had *passed* version 1 and so were never in the set. The blindness does not scale with
severity either: make the regressions five and the fix one, and the same set still reports zero.
So either keep the whole evaluation set, or keep every case that has ever failed — which does not
report the breakage it missed as a regression at all, because that case was failing when the set
was taken and so reads as a fix on the next comparison; what it buys is the change after that
one. When it
runs: on every change you would otherwise have to remember to check, which is prompt, model,
retrieval settings, chunking and the documents themselves. And it runs each case **more than once**, calling a case a
regression only when it fails *more often* than it passed — a tie is not one, and that tie-break
mattered more on this set than the number of repeats did; a single run
of the chapter's set reported two regressions and two fixes where the real answer was one fix, and
every one of the five available runs would have reported a regression that was not there.
2. Your own standard moving as you see more output. The demonstration is forty outputs labelled
twice, a month apart, with nothing about the outputs changed: 85 per cent in week 1 and 72.5 in
week 5, seven labels flipped, six of them from pass to fail. It is not a mistake, and it belongs to a person's judgement
rather than to a check in code, which does not move on its own — one of Chapter 31's reasons for
preferring code, with the caveat that a check comparing against your documents does change
verdict when they change. Where a person is judging, the mechanism is plain:
reading output teaches you what to look for, and much of what you learn is a new way for an answer
to be wrong. What it destroys is comparison across time, because a version scored in week 1
against one scored in week 5 differs by a change you made *and* a change you underwent, which on
this set is 12.5 points, so a five-point improvement sits well inside it. You notice it by keeping
the old labels with their dates and re-labelling a sample of old outputs **blind** — without
looking at what you said last time, because looking first measures nothing, you will simply agree
with yourself. The flip count is the drift, and it belongs beside any improvement you report. And
when the flips go one way you have learned a criterion, so write it down and re-label the whole
set against it; otherwise you have two standards inside one set and no way to tell which case was
judged by which. The thing to eliminate is not drift but **silent** drift.
3. Record the input; what retrieval was asked and what it returned, with candidate ids and scores;
which model and which version; each tool call with its timing; the output; the tokens in and out;
and the time per stage. Every field is there because some question needs it, and the useful way to
decide is to write the questions down and see which field answers each. What you deliberately do
not record is the part people skip. Three fields are worth thinking twice about. The whole document a
passage came from, because you already have it and the id finds it; anything a caller sent as a
credential; and anything you cannot delete on request, which is a property of *where* you put the
trace rather than of the field. Then the real decision, which is the text. Four of the chapter's
sixteen fields hold free text — what somebody typed, what came out of your documents and what the
model wrote — and dropping them leaves five
of eight questions answerable — including one genuine evaluation question, whether retrieval
returned the right passage, because a document id answers that with no text at all. What goes is
everything needing the text: why it said that, whether this is the same failure as yesterday's,
and whether this can become a regression case — and **a case needs an input and an output to be a
case**, so a content-free trace cannot feed the regression set. That is why it is not
all-or-nothing: ids, counts and timings on every request, content on a sample of the *failures*
with a window after which it is deleted.
4. Whether the set can see a regression at all, and in this order. First, what is in it: if it was
built from past failures, zero regressions is what it reports whether or not a never-failed case
broke, because such a case is not in it — and a case already in the set that was failing when the
set was taken cannot read as a regression at all — it reads as a fix if the change repaired it
and as a standing failure if it did not, so the set is silent in that direction too. The chapter's set of eight reported zero
against three real breakages and zero against five, so the number carries no information until you
know the set holds passing cases. Second, whether it is being run on the changes that matter — a
set that runs on prompt edits and not on a model upgrade, a re-chunking or a document refresh will
be silent through the changes most likely to break something. Third, whether it is run with
repeats: a set run once is noisy in both directions, so three months of silence from a single-run
set is less reassuring than it sounds, though noise would more likely produce false alarms than
false silence. Fourth, whether the verdicts still mean what they did — if nobody has re-labelled a
sample blind, the standard may have moved under the set, and a case that drifts from pass to fail
in your own judgement will not show up as a regression because nothing re-ran its label. The
honest summary is that "no regressions" is a claim about the set before it is a claim about the
application.
5. What was labelled when, before anything about the application. An 8-point improvement across a
quarter is a difference between two measurements made three months apart, and the chapter's forty
outputs moved 12.5 points with nothing changed but the person reading them — so the first question
is whether any old output has been re-labelled blind in that time, and what the flip count was. If
the answer is that nobody has, the 8 points cannot be separated from drift and the number is not
yet a number. Then three more. Was it the same set, or did cases get added — because adding a case
because a version got it wrong is Chapter 20's point about having stopped measuring. Was each case
run more than once, or is the figure two single runs subtracted. And is 8 points outside the
interval round it, which is Chapter 20's bootstrap and the one piece of arithmetic that answers
whether the difference is real at all. None of those questions is about the application, which is
the point: an improvement claimed across time is a claim about the measuring apparatus first.

> **You understand this when** you can say why a set of past failures reports no regressions
> whether or not a never-failed case broke, and name the one cheap thing that tells you your improvement was
> your own standard moving.
