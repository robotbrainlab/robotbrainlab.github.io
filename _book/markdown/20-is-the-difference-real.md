# Is the Difference Real?

Chapter 18 said to change one thing and run it more than once. This chapter is the second half
of that sentence: what *more than once* has to mean, and what you are allowed to conclude when
you have done it.

The reason it matters is unflattering. Most prompt work is done by changing something, looking
at a handful of outputs, deciding it is better, and keeping it. That procedure cannot distinguish an improvement from a coincidence,
and the arithmetic below says it usually is not distinguishing them.

*The problem.* I changed the prompt and it looks better. I have no idea whether it actually is.

*The question.* What does it take to know that a change helped, and what does a single
comparison really tell you?

## The Set You Measure On

You cannot answer the question with examples you look at. You need a fixed set of cases and a
judgement you can apply to each one the same way every time.

For this chapter a **case** is an input plus whatever lets you mark the answer right or wrong.
That is all the statistics need. Three properties matter:

**The judgement is mechanical.** Given the same answer twice, it gives the same verdict twice.
If a person is reading the answers and deciding, you have a second source of variation on top of
everything below, and you cannot separate it from the first. A judgement that wanders is a
problem to fix rather than to average away — though where you cannot fix it, repeated judging at
least bounds it, which is what trials are for below. Chapter 31 is where a judgement gets
built and checked properly.

**The cases are independent.** Forty rephrasings of one question are worth far less than forty
cases — closer to one — and the arithmetic in this chapter cannot tell. It counts rows, so it
will happily hand you a narrow interval on a set that is four questions wearing forty hats.

**The set does not change while you are comparing.** Add a case because B got it wrong and you
have stopped measuring. Chapter 33 is about the set growing over time, which is a different
activity from running a comparison.

> **Note:** Where the cases come from, how to turn real failures into them, and how to build a
> judgement you can trust are chapters 30, 31 and 33. This chapter assumes you have forty cases
> and a verdict for each, because that is the smallest thing you can do statistics to. Forty is
> not a recommendation; by the end of the chapter it will be clear what it is.

## One Run Is Not a Score

Start with a single prompt, forty cases, and a model that gets any given case right about 70 per
cent of the time. Run the whole set five times.

```python
import random, statistics

CASES = 40
P = 0.70          # this model gets each case right 70% of the time

def one_run():
    return sum(1 for _ in range(CASES) if random.random() < P)

random.seed(20)
for run in range(1, 6):
    right = one_run()
    print(f"  run {run}: {right}/{CASES} = {right / CASES:.3f}")

scores = sorted(one_run() / CASES for _ in range(10_000))
print(f"  over 10,000 runs: lowest {scores[0]:.3f}, highest {scores[-1]:.3f}")
print(f"  middle 95%: {scores[250]:.3f} to {scores[9750]:.3f}")
print(f"  standard deviation: {statistics.stdev(scores):.3f}")
```

```text
  run 1: 29/40 = 0.725
  run 2: 30/40 = 0.750
  run 3: 35/40 = 0.875
  run 4: 25/40 = 0.625
  run 5: 31/40 = 0.775
  over 10,000 runs: lowest 0.450, highest 0.925
  middle 95%: 0.550 to 0.825
  standard deviation: 0.073
```

**Read runs 3 and 4 again.** 0.875 and 0.625. Same prompt, same forty cases, same model, nothing
changed between them. A quarter of the whole scale, from nothing at all.

Now imagine those two runs were your before and after. You would have measured a twenty-five
point improvement from a change you did not make, and you would have believed it, because
twenty-five points is a lot and your eyes were on the outputs rather than on the arithmetic.

**And the spread is not luck, it is arithmetic.** Each case is a coin weighted to 0.70, so forty
of them have a standard deviation of

```{=latex}
\[ \sqrt{n p (1-p)} = \sqrt{40 \times 0.70 \times 0.30} = \sqrt{8.4} = 2.90 \text{ cases} \]
```

which as a score is `\(2.90 / 40 = 0.072\)`{=latex} — one standard deviation — and the program
measured 0.073 over ten thousand runs. Two standard deviations either side is about
`\(\pm 0.14\)`{=latex}.

Hold on to the number 0.14. The difference this chapter goes on to chase is 0.075.

**Now be careful what that spread is measuring, because this program makes two different things
coincide.** `one_run()` treats every case as its own coin at 0.70, so a fresh run of the same
forty cases is arithmetically the same thing as drawing forty new cases. Real evaluation sets
are not like that: most cases are reliably right or reliably wrong, and only a few are genuinely
uncertain. Three sets that all score about 0.700:

```python
import random, statistics

# Three evaluation sets that all score about 0.700, differing only in
# how uncertain the model is on each case.
SETS = {
    "every case a 0.70 coin":       [0.70]*40,
    "28 right, 12 wrong, reliably": [0.98]*28 + [0.02]*12,
    "24 right, 8 wrong, 8 coins":   [0.98]*24 + [0.02]*8 + [0.50]*8,
}

def run(per_case, repeats=1):
    """Score the set once, judging each case `repeats` times and averaging."""
    total = 0.0
    for q in per_case:
        hits = sum(1 for _ in range(repeats) if random.random() < q)
        total += hits / repeats
    return total / len(per_case)

random.seed(20)
for name, per_case in SETS.items():
    scores = [run(per_case) for _ in range(5_000)]
    print(f"  {name:30s} {statistics.fmean(scores):.3f}"
          f"   sd {statistics.stdev(scores):.3f}")
```

```text
  every case a 0.70 coin         0.699   sd 0.074
  28 right, 12 wrong, reliably   0.691   sd 0.022
  24 right, 8 wrong, 8 coins     0.693   sd 0.040
```

**The middle line is the one to notice.** A system that is reliably right on twenty-eight cases
and reliably wrong on twelve scores exactly 0.700 in about half its runs, and lands within one
case of it in nine out of ten; its run-to-run spread is under a third of the coin model's. So 0.14 means two different things and you have to say which:

- **It is always the spread over which forty cases you happened to draw.** That is what the next
  section computes, and it does not depend on how certain the model is per case.
- **It is the spread over repeated runs only when the model is as uncertain per case as the
  coin.** A near-deterministic system moves much less between runs.

The coin is the worst case, which is why a plus-or-minus is built from it. Runs 3 and 4 above are
real and so is the arithmetic; just do not quote fourteen points as run-to-run noise for a system
you have not measured that way.

> **Warning:** The seed is in that program so that your numbers match the book's. It does not
> make the variation go away, and nothing you can set makes a real provider repeat itself
> exactly. Temperature zero does not either: Chapter 13 gives four reasons — floating-point
> addition order, batching, expert routing and the provider changing something under you — and
> none of them is a setting you control. What those four cause is the *run-to-run* kind of
> variation, the second reading above, and at temperature zero it is small — near-ties flipping,
> not a coin on every case. Small is not zero, and you do not know how small on your own set
> until you run it twice. **Repeated runs are not a workaround for a temperature you forgot to
> set. They are the measurement.**

## An Interval You Can Justify

So a score needs an interval around it. The textbook move is to reach for a named distribution
and a formula. This book does not, and the reason is worth saying plainly, because it is the
part people get wrong when asked.

**There is a formula for this one, and it is not the reason to learn the formula.** A
proportion has a well-known interval, and at forty cases and a score of 0.70 it is perfectly
serviceable. The trouble is that it is a formula for *one* statistic. The number this chapter
actually needs an interval on is the **paired difference** between two prompts on the same
cases, and its formula needs more than the two scores — you have to bring in how often the two
disagree. For right-or-wrong marks that formula is still a one-liner, and it agrees with the
bootstrap everywhere in this chapter. But change the score to an average of per-case marks, or
to a ranking measure, and the shape of the formula changes with it. Every one is a thing to
derive, look up, or get subtly wrong.

**The bootstrap is one procedure for all of them.** Draw forty cases from your forty, with
replacement, compute *whatever your statistic is* on that sample, and do it ten thousand times.
The spread of those ten thousand numbers is an estimate of how much your statistic would move
if you had drawn a different forty cases of the same kind. Take the 2.5th and 97.5th percentiles
and you have a 95 per cent interval.

Its assumption is weaker than a named distribution's and it is one you can state out loud:
**that your cases are a sample of the kind of input you care about.** If that is false, no
method on this page helps you, and you have an evaluation-set problem rather than a statistics
problem.

That is the whole method, and it is three lines of the program below.

```python
import random

# 40 cases. 1 means the answer was judged right.
# Both right 26, A only 2, B only 5, both wrong 7.
A = [1]*26 + [1]*2 + [0]*5 + [0]*7
B = [1]*26 + [0]*2 + [1]*5 + [0]*7

def score(results):
    return sum(results) / len(results)

def interval(results, trials=10_000):
    n = len(results)
    scores = []
    for _ in range(trials):
        sample = [results[random.randrange(n)] for _ in range(n)]
        scores.append(score(sample))
    scores.sort()
    return scores[int(0.025 * trials)], scores[int(0.975 * trials)]

random.seed(20)
for name, results in (("A", A), ("B", B)):
    lo, hi = interval(results)
    print(f"  {name}: {score(results):.3f}   95% interval {lo:.3f} to {hi:.3f}")
```

```text
  A: 0.700   95% interval 0.550 to 0.825
  B: 0.775   95% interval 0.650 to 0.900
```

**Prompt A scores 0.700, with an interval from 0.550 to 0.825** — the same two numbers the
previous section's ten thousand actual runs produced.

**That match is exact for a reason, and the reason is worth more than the match.** `A` holds
exactly 28 ones out of 40, so resampling it with replacement *is* drawing from a list that is
exactly 70 per cent ones — which is the distribution the previous section sampled directly. The
two procedures are not independent and then agreeing; they are one distribution reached two
ways. The exact binomial percentiles are 0.550 and 0.825 as well, so all three agree, and they
had to.

What that does show is that the bootstrap recovers the right *width*. What it cannot show is
that your interval is in the right *place*: it is anchored on the score you measured — look at
A's, which runs further below 0.700 than above it — so if you drew an unlucky forty cases, the
whole interval moves with them. A
confidence interval is a statement about the procedure, not a promise about this one run.

> **Tip:** Ten thousand resamples is not a tuning parameter to agonise over. A thousand is
> visibly lumpy at the percentiles; ten thousand is smooth and takes a fraction of a second on
> forty cases. The number that matters is the number of *cases*, not the number of resamples —
> resampling cannot create information that forty cases do not contain.

## Overlapping Intervals Are Not the Test

A's interval runs to 0.825 and B's starts at 0.650, so they overlap heavily. The obvious
conclusion is that there is no evidence of a difference.

**That conclusion happens to be right here and the reasoning is wrong**, and it is wrong in a
way that will cost you later. Two intervals overlapping does not mean the difference is
uncertain, and two intervals not overlapping is a stricter condition than the one you actually
care about. The question is not *where is A* and *where is B*. The question is *where is B minus
A*, and that has an interval of its own.

So compute the thing you want an interval on.

## Compare on the Same Cases

Here is the move that buys more than any other in this chapter, and it costs nothing.

Run both prompts on the *same* cases, keep each case's two results together, and resample
*cases* rather than results. Each resample draws forty cases and asks what B minus A was on those forty.

```python
import random

A = [1]*26 + [1]*2 + [0]*5 + [0]*7
B = [1]*26 + [0]*2 + [1]*5 + [0]*7

def difference(pairs):
    return sum(b - a for a, b in pairs) / len(pairs)

def interval(pairs, trials=10_000):
    n = len(pairs)
    diffs = []
    for _ in range(trials):
        sample = [pairs[random.randrange(n)] for _ in range(n)]
        diffs.append(difference(sample))
    diffs.sort()
    return diffs[int(0.025 * trials)], diffs[int(0.975 * trials)]

pairs = list(zip(A, B))
random.seed(20)
lo, hi = interval(pairs)
print(f"  B - A = {difference(pairs):+.3f}   95% interval {lo:+.3f} to {hi:+.3f}")

agree = sum(1 for a, b in pairs if a == b)
a_only = sum(1 for a, b in pairs if a == 1 and b == 0)
b_only = sum(1 for a, b in pairs if a == 0 and b == 1)
print(f"  {agree} cases agree, {a_only} only A gets right, {b_only} only B")
```

```text
  B - A = +0.075   95% interval -0.050 to +0.200
  33 cases agree, 2 only A gets right, 5 only B
```

The interval on the difference runs from −0.050 to +0.200, and **it contains zero.** B might be
seven and a half points better, and it might be five points worse, and forty cases cannot tell
you which.

**Now see what the pairing bought.** Run the same comparison without it — resample A's results
and B's results independently, as if they had been measured on different sets:

```python
random.seed(20)
out = []
for _ in range(10_000):
    a = sum(A[random.randrange(40)] for _ in range(40)) / 40
    b = sum(B[random.randrange(40)] for _ in range(40)) / 40
    out.append(b - a)
out.sort()
print(f"  unpaired: 95% interval {out[250]:+.3f} to {out[9750]:+.3f}")
```

```text
  unpaired: 95% interval -0.125 to +0.275
```

0.400 wide against 0.250, on exactly the same data — the unpaired interval is about 1.6 times
the paired one. Note what pairing did and did not do. It did *not* remove the variation that
comes from which cases you drew: the 0.250 that is left is entirely that. What it removed is the
part of that variation the two prompts *share* — a hard case hurts both of them, and when you
subtract, the shared part cancels. What survives is how the two prompts differ on the same
inputs. Nothing was assumed and no case was added.

**And the last line of the program is the one to take to an interview.** Thirty-three of the
forty cases came out the same way under both prompts. Those cases carry no information about
which prompt is better — they are the same evidence for both. The entire comparison rests on the
seven cases where the two prompts disagree: five for B, two for A. Lab step 6 measures this: move
cases between both-right and both-wrong and the interval does not budge.

Five against two. Put that way, nobody would claim a result. It is the same number as +0.075
out of 40, which sounds much more impressive, and that is exactly why it is worth computing both
ways.

## How Many Cases, and How Many Trials

Two different questions with two different answers, and they are easy to confuse because both
sound like "run it more".

**Cases tell you about the range of inputs.** More cases narrow the interval on the difference.
Keep the shape of the forty-case result and ask what a larger set of the same kind would show:

```python
import random

# Keep the pattern of the 40 cases and ask what a bigger set of the same
# kind would show: 65% both right, 5% only A, 12.5% only B, 17.5% both wrong.
PATTERN = [(1, 1)]*26 + [(1, 0)]*2 + [(0, 1)]*5 + [(0, 0)]*7

def interval(pairs, trials=2_000):
    n = len(pairs)
    diffs = []
    for _ in range(trials):
        s = [pairs[random.randrange(n)] for _ in range(n)]
        diffs.append(sum(b - a for a, b in s) / n)
    diffs.sort()
    return diffs[int(0.025*trials)], diffs[int(0.975*trials)]

random.seed(20)
for k in (1, 2, 5, 10, 25):
    pairs = PATTERN * k
    lo, hi = interval(pairs)
    verdict = "B is better" if lo > 0 else "cannot tell"
    print(f"  {len(pairs):5d} cases   {lo:+.3f} to {hi:+.3f}   {verdict}")
```

```text
     40 cases   -0.050 to +0.200   cannot tell
     80 cases   -0.013 to +0.163   cannot tell
    200 cases   +0.020 to +0.135   B is better
    400 cases   +0.035 to +0.113   B is better
   1000 cases   +0.049 to +0.101   B is better
```

**Two hundred cases is where this difference starts to become visible.** Not forty, and not
eighty. If somebody asks how many cases are enough, that table is the answer in its proper form:
enough to see the difference you care about, and you find the number by computing it rather than
by choosing a round one.

**Read the table for what it is, though.** `PATTERN * k` replicates the forty-case mix exactly,
so every row shows what the interval looks like when the larger set has precisely this
composition. A real draw of two hundred cases varies, and you can work out exactly how much:
across every possible draw of two hundred from those rates, weighted by how likely each is,
this interval clears zero 72 times in a hundred. At four hundred cases it is 95. So two hundred is where you would *start* to see this
difference, and four hundred is where you could count on it — which is the distinction between
a typical interval and a detection rate, and it is the one people skip.

The shape of the table is the familiar one. Width shrinks with the square root of the count, so
each halving of the interval costs four times the cases: eighty gives you 0.176 of width, and
a thousand gets you to 0.052, which is 3.4 times
narrower for 12.5 times the cases — and `\(\sqrt{12.5} = 3.54\)`{=latex}.

**Trials tell you about the model's own variation on one input.** That is the first section's
problem, and more cases do not touch it. If you run each case once, the right-or-wrong you
record is one sample of something that was never certain.

**And there is arithmetic for how many, which is the same law applied to a different quantity.**
Judge a case `\(k\)` times and average, and that case's own variance is divided by
`\(k\)`{=latex}, so the run-to-run spread shrinks as `\(1/\sqrt{k}\)`{=latex}. The `run()`
function above already takes the argument; this continues that program:

```python
flips = SETS["24 right, 8 wrong, 8 coins"]
random.seed(20)
for k in (1, 2, 3, 5, 10):
    scores = [run(flips, repeats=k) for _ in range(5_000)]
    print(f"  {k:2d} repeat(s) per case   run-to-run sd "
          f"{statistics.stdev(scores):.3f}")
```

```text
   1 repeat(s) per case   run-to-run sd 0.041
   2 repeat(s) per case   run-to-run sd 0.028
   3 repeat(s) per case   run-to-run sd 0.023
   5 repeat(s) per case   run-to-run sd 0.018
  10 repeat(s) per case   run-to-run sd 0.013
```

**Look at what each repeat costs and buys.** The second one takes the spread from 0.041 to
0.028, a saving of 0.013 for one extra pass over the set. Going from three repeats to ten —
seven more passes — buys 0.010, less than the second repeat managed on its own, for seven times
the work. That is the
square-root law being unkind in the usual way, and it gives you the rule: **two or three
repeats, then stop**, unless the within-case variation is itself the thing you are measuring.

Repeats never narrow the interval that matters for a comparison, because they add no new inputs.
What they do is stop run-to-run noise from masquerading as a difference.

The practical rule follows from what each one buys:

| If | Then |
|---|---|
| The judgement is noisy, or the model is sampled at a real temperature | Repeat the cases and average before you compare |
| You want to detect a smaller difference | More cases |
| The interval is wide and nothing else is wrong | More cases |
| The interval is wide and repeated runs of *the same* prompt disagree | Fix that first, with repeats or a lower temperature |

> **Warning:** There is a wrong way to spend repeats, and it is the obvious one. Running the
> same case three times and recording three separate rows triples your apparent case count and
> narrows your interval, while adding no new inputs at all. Average the repeats *within* the
> case, so one case is still one row. The interval is computed over cases, because cases are
> what you drew from the world.

## Every Change Is an Experiment

The statistics above are easy. The discipline around them is what people do not do.

**Write the prediction down before you run it.** Not the hope — the number. *I expect this to
move the score from 0.70 to about 0.80.* A prediction you wrote down turns a run into a test of
something; a prediction you form afterwards turns every result into a confirmation, because the
result is always consistent with some story.

**One change at a time**, which is Chapter 18's rule and the reason it exists. Two changes and a
better score tell you that the pair is better than the pair, which is not something you can
build on, and if one of them was a regression you have hidden it.

**Keep the runs.** A file with the date, what changed, the score, the interval, and the
prediction. It costs a line per experiment and it is the only thing that will tell you, in two
months, whether the last twenty changes added up to anything — which is a question people ask
and almost nobody can answer.

**And accept "cannot tell" as a result.** It is the honest reading of the paired interval above,
and it is more useful than a decision, because it tells you what to do next: get more cases, or
go and find a difference big enough to see. What it does not license is keeping B because B
*looks* better. You measured, the measurement came back inconclusive, and "it looks better" is
the thing the measurement was there to replace.

> **Tip:** The cheapest way out of "cannot tell" is often not more cases. What you are really
> short of is effect against noise, and a verdict that is only right-or-wrong throws away most
> of what happened — so a measurement aimed at the specific failure you care about can move
> further between the two versions for the same forty cases. It is the ratio that improves, not
> the width on its own: a richer measurement can be noisier too. Designing one is chapters 30
> and 31, and that is why they come before the rest of the measurement chapters.

## Lab: Measure a Difference You Cannot See

Five programs, pure Python, nothing to install. Every number is reproducible from the seed
except in step 5, which asks for a shuffle and promises no number. Forty-five minutes, and there
is a key for every step.

**Step 1.** Save the five-runs program as `runs.py` and run it.

*Expected result:* exactly the output in the chapter, because the seed is fixed: 0.725, 0.750,
0.875, 0.625, 0.775, then a lowest of 0.450, a highest of 0.925, a middle 95 per cent of 0.550
to 0.825, and a standard deviation of 0.073.

**Step 2.** Change `CASES` to 400, leaving `P` alone. What happens to the standard deviation,
and does it match `\(\sqrt{n p (1-p)} / n\)`{=latex}?

*Expected result:* the standard deviation falls to about 0.023, and the formula gives
`\(\sqrt{400 \times 0.7 \times 0.3}/400 = 9.17/400 = 0.023\)`{=latex}. Ten times the cases for
about a third of the spread — the square root again.

**Step 3.** Save the bootstrap program as `boot.py` and run it. Then change `trials` to 100,
and change `random.seed(20)` to `random.seed(21)` and then to `22`.

*Expected result:* first `A: 0.700  0.550 to 0.825` and `B: 0.775  0.650 to 0.900`. With 100
resamples A's interval comes out 0.575 to 0.825 at seed 20, 0.525 to 0.825 at 21 and 0.550 to
0.800 at 22 — the endpoints move by a few hundredths. Nothing is averaged at either count:
`interval()` sorts and returns one order statistic, the third smallest of 100 or the 251st of
10,000. At 100 a single number moving moves the endpoint; at 10,000 that order statistic sits in
a part of the distribution that has been sampled far more densely, so it barely moves. The score in the middle never moves, because it is not
resampled. Note what you had to do to see this: the seed is why re-running the program
unchanged gives the same answer every time, which is the point of having one.

**Step 4.** Halve the set. Save the paired program as `paired.py` and give it a twenty-case set
of the same shape —
`[1]*13 + [1]*1 + [0]*3 + [0]*3` for `A` and `[1]*13 + [0]*1 + [1]*3 + [0]*3` for `B`. What
happens to the interval, and what happens to the measured difference?

*Expected result:* A scores 0.700 and B scores 0.800, so the difference *grew* to +0.100 — and
the interval went from 0.250 wide to 0.400 wide, −0.100 to +0.300. A smaller set gave you a
bigger apparent improvement and less ability to believe it, which is the trap this whole chapter
is about. Four informative cases, three to one.

**Step 5.** Put `paired.py` back to forty cases and run it. Then break the pairing: shuffle `B`
before zipping it with `A`.

*Expected result:* the paired interval is `-0.050 to +0.200`, and the difference `+0.075` does
not change when you shuffle, because a sum does not care about order. The interval does change,
and it gets wider — you have thrown away the information about which case each result belongs
to. That is the whole value of pairing, visible as a number.

**Step 6.** Forty cases, and the honest answer is "cannot tell". Without running anything,
predict what the interval would do if B had won 8 of the disagreements and A had won 2. Then
edit the lists and check.

*Expected result:* ten informative cases instead of seven, with B taking eight, so the
difference doubles to `\((8 - 2)/40 = +0.150\)`{=latex} — and the interval is +0.000 to
+0.300. It lands on zero rather than clearing it, which is still not a result — and the landing
is that tidy partly because a score on forty cases moves in steps of 1/40, so the 2.5th
percentile has few places it can fall. The closed form puts the lower end at +0.002, which
clears zero by nothing worth having. Doubling the effect on forty cases was not enough; that is
how little forty cases can see. The point to
take is that the interval is driven by the disagreements and the total count; the cases the two
prompts agree on are ballast, whether they agree on a right answer or a wrong one. The next part
of this step measures that.

Keeping the two and the five, move cases between both-right and both-wrong: build `A` as
`[1]*20 + [1]*2 + [0]*5 + [0]*13` and `B` as `[1]*20 + [0]*2 + [1]*5 + [0]*13`. What happens to
the interval?

*Expected result:* **nothing at all.** It is −0.050 to +0.200, the same two numbers, although A
has fallen from 0.700 to 0.550 and B from 0.775 to 0.625. Try 15 both-right and 18 both-wrong,
or 30 and 3 — still −0.050 to +0.200 every time. That is the chapter's claim turned into a
measurement: for this statistic the interval depends on how many cases disagree, which way, and
how many cases there are in total. The scores themselves do not enter it.

**Step 7.** Save the sample-size program as `howmany.py` and run it. Then work out, from the
table alone, roughly how many cases you would need to detect a difference of 0.02 of this shape.

*Expected result:* the printed table, and then an estimate. At 1,000 cases the half-width is
`\((0.101 - 0.049)/2 = 0.026\)`{=latex}, which is already bigger than 0.02, so 1,000 is not
enough. The half-width shrinks with the square root, so the count you need is about
`\(1000 \times (0.026/0.02)^2 = 1690\)`{=latex} — call it seventeen hundred. Changing the loop to
`for k in (50,):` runs 2,000 cases and gives +0.057 to +0.093, a half-width of 0.018, which is
inside 0.02 with a little room. The useful conclusion is not the number. It is that small differences are expensive
to prove, and that is a reason to stop chasing them rather than a reason to build a bigger set.

**Step 8.** You read that a new prompt improved a score from 71 per cent to 78 per cent on an
internal evaluation. What do you ask?

*Expected result:* how many cases, and were both prompts run on the same ones. Then: how many
times was each case run, what was the interval on the difference, and who or what decided
right or wrong. Seven points on forty cases is inside the noise of a single run; seven points on
two thousand paired cases with a mechanical judgement is a result. The number you were given
distinguishes the two not at all, which is why it is the wrong number to report on its own.

**Step 9.** Save the three-sets program as `models.py` and run it. All three sets score about
0.700. Before you look at the numbers, say which one you expect to vary most between runs, and
why.

*Expected result:* 0.074, 0.022 and 0.040. The coin set varies most, because every one of its
forty cases is genuinely uncertain; the reliable set varies least, because thirty-seven or
thirty-eight of its forty cases come out the same way every time. All three have the same
case-sampling spread of about 0.072, which is the distinction this chapter asks you to keep:
*which cases you drew* against *what the model did on them*.

**Step 10.** Append the repeats loop to `models.py` and run it. Then decide, from the output
alone, how many repeats you would actually pay for.

*Expected result:* 0.041, 0.028, 0.023, 0.018, 0.013 at one, two, three, five and ten repeats.
The second repeat buys 0.013 for one extra pass; the seven passes from three to ten buy 0.010
between them. Two or three, and spend the rest of the budget on cases — which buy something
repeats never do, namely a wider range of inputs. Check the law while you are there: 0.041
divided by `\(\sqrt{10}\)`{=latex} is 0.013.

## Summary, Key Terms, and Review Questions

### Summary

A single run is not a score. Forty cases at a true 0.70 have a standard deviation of
`\(\sqrt{np(1-p)}/n = 0.072\)`{=latex}, so two of those span about ±0.14, and five seeded runs of
one unchanged prompt gave 0.625 and 0.875 among them. **Say which spread you mean**: ±0.14 is
always the spread over which forty cases you drew, and it is the run-to-run spread only when the
model is as uncertain per case as a 0.70 coin — a system reliably right on 28 and wrong on 12
hits exactly 0.700 in half its runs and stays within one case of it in nine out of ten, at a
run-to-run spread of 0.022. A seed makes the book's numbers
match yours; nothing makes a provider repeat itself, and temperature zero does not, for Chapter
13's four reasons, which cause the run-to-run kind and cause little of it. So a score needs an
interval, and the **bootstrap** gives you one with no formula to derive: resample your cases with
replacement, compute your statistic on each resample, and take the 2.5th and 97.5th percentiles.
A proportion has a perfectly good closed form; the reason to use the bootstrap is that it is the
same three lines for the paired difference, for an average of per-case marks and for a ranking
measure. On this data it returns 0.550 to 0.825 for a score of 0.700, which is exactly what ten
thousand real runs give — and it had to be, because resampling a list of exactly 28 ones *is*
that distribution. It shows the bootstrap recovers the right **width**; the interval is
anchored on the score you measured, so it says nothing about being in the right place.
**Overlapping intervals are not the test**: compute an interval on the difference, and compute it
**paired**, both prompts on the same cases, resampling cases rather than results. That took the
width from 0.400 to 0.250 here, about a factor of 1.6 — not by removing the variation from which
cases you drew, which is all that 0.250 is, but by cancelling the part of it both prompts share.
It still contains zero around +0.075, so the answer is *cannot tell*, and the reason is the last
line of the program: 33 cases agree, 7 disagree, five to two. Move cases between both-right and
both-wrong and the interval does not move at all. **Cases** buy resolution on the range of inputs
and **trials** buy it on the model's own variation; repeats divide a case's own variance by `\(k\)`{=latex},
so the second is worth more than the seven passes from three to ten — two or three, then stop — and they are averaged
*within* a case, never recorded as extra rows. Two hundred cases of this shape is where +0.075
starts to be visible, but a real draw of two hundred clears zero only 72 times in a hundred and
four hundred manages 95, which is the difference between a typical interval and a detection rate.
Width shrinks with the square root, so each halving costs four times the cases. Write the
prediction down first, change one thing, keep a file of the runs, and let **cannot tell** be an
answer.

### Key Terms

| Term | Meaning |
|---|---|
| **Case** | One input plus whatever marks the answer right or wrong. The unit the statistics count — and they count rows, so forty rephrasings of one question are worth nearer one case than forty |
| **Bootstrap** | Estimating how much a statistic would move by resampling your own cases with replacement. One procedure for every statistic you score, where a closed form is a different formula each time |
| **Confidence interval** | The range a measurement would fall in most of the time if you repeated it. Here, the 2.5th to 97.5th percentiles of the resampled scores |
| **Paired comparison** | Running both versions on the same cases and keeping the results together, so the part of case-to-case variation the two versions share cancels when you subtract |
| **Trials** | Repeated runs of the same case, which measure the model's own variation. Averaged within the case, never counted as extra cases |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Spread of a score | `\(\sqrt{n p (1-p)} / n\)`{=latex} — one standard deviation over **which cases you drew**. 40 cases at 0.70 is 0.072, so two of them is the ±0.14 that spans 95 per cent. Run-to-run spread is a different number and is smaller unless the model is uncertain on every case |
| The bootstrap | Resample your cases with replacement, score each, take the 2.5th and 97.5th percentiles |
| What to put an interval on | The **difference**, paired. Never two separate intervals and a look |
| Cost of resolution | Width shrinks as `\(1/\sqrt{n}\)`{=latex}, so halving it costs four times the cases |
| What carries the comparison | Only the cases where the two versions disagree. Count them and say them out loud |
| What pairing is worth | Here, 0.400 wide down to 0.250. It cancels the variation the two versions share, so the more they agree, the more it buys |
| Cases against trials | Cases for the range of inputs, trials for the model's variation. Neither fixes the other |
| How many trials | Averaging `\(k\)`{=latex} judgements divides a case's own variance by `\(k\)`{=latex}. Two or three, then stop |
| Typical interval vs detection | A table built from a fixed mix shows the usual interval. Whether a real draw clears zero is a separate number, and lower |

### Review Questions

1. How do you decide whether prompt B is better than prompt A?
2. What is a bootstrap interval, and why use one here rather than a named distribution?
3. How many cases and how many trials are enough?
4. Two scores have overlapping confidence intervals. What, if anything, does that tell you?
5. Why does pairing narrow the interval when it adds no data?
6. Your evaluation runs each of 40 cases three times and records 120 rows. What is wrong?

### Review Answers

1. Run both on the same fixed set of cases with a mechanical judgement, keep the results paired
per case, and compute a bootstrap interval on **B minus A** rather than on each score
separately. If that interval contains zero, the honest answer is that you cannot tell, and the
next question is whether the set is big enough to see a difference the size you care about. Two
things to say unprompted. First, forty cases carry a plus-or-minus of about fourteen points on
which cases you drew, so a seven-point gap between two single runs of a forty-case set is
nothing — and be precise about which spread that is, because the run-to-run spread is that large
only when the model is genuinely uncertain on most cases, and far smaller when it is reliably
right or wrong on each. Second, the comparison rests only on the cases where the two prompts
disagree, so count those and say the number: five against two persuades nobody, and it is the
same data as "+7.5 per cent".
2. A bootstrap interval is built by drawing a sample of the same size from your own cases, with
replacement, computing your statistic on it, repeating that ten thousand times, and taking the
2.5th and 97.5th percentiles. It estimates how much your statistic would move if you had
happened to draw a different set of cases of the same kind. Be careful not to overclaim the
reason: a proportion does have a perfectly good closed-form interval, and at forty cases it
works. The reason to use the bootstrap is that it is **one** procedure for every statistic you
will score. The number you actually want an interval on is the paired difference between two
versions on the same cases, whose formula needs more than the two scores — it needs how often
they disagree, and for right-or-wrong marks it is still a one-liner that agrees with the
bootstrap everywhere in this chapter. Move to an average
of per-case marks or a ranking measure and it is a different formula again, each one a thing to
derive, look up or get subtly wrong. The bootstrap needs no formula, its assumption is one you
can state out loud: that your cases are a sample of the inputs you care about. On the honest
side, do not oversell the chapter's consistency check. The interval the bootstrap gave from one
run of forty cases matched the spread of ten thousand actual runs exactly — but it had to,
because the list being resampled held exactly 28 ones out of 40, so resampling it *is* drawing
from that same distribution. What it demonstrates is that the method recovers the right width.
It cannot tell you the interval is in the right place: a bootstrap interval is anchored on the
score you measured, so an unlucky set of cases moves the whole thing.
3. They are different questions. **Cases** buy resolution on the range of inputs: the interval
narrows as one over the square root of the count, so each halving costs four times as many, and
the honest answer is "enough to see the difference you care about" — for a difference of 0.075 of
the shape in this chapter, two hundred is where it starts to show and four hundred is where you
could count on it, because a real draw of two hundred clears zero only about three times in
four. You find those numbers by computing, not by picking a round one. **Trials** buy resolution
on the model's own variation on a single input, which more cases never touch, and they have
arithmetic of their own: averaging `\(k\)`{=latex} judgements of a case divides that case's
variance by `\(k\)`{=latex}, so on this chapter's mixed set the run-to-run spread goes 0.041,
0.028, 0.023 at one, two and three repeats and only reaches 0.013 at ten. The second repeat buys
more than the seven passes from three to ten, so two or three and stop, unless the within-case
variation is itself
what you are measuring. The trap worth naming is recording repeats as extra rows: that narrows
the interval while adding no new inputs, which is the appearance of precision rather than
precision.
4. On its own, almost nothing. Overlap is not the test, in either direction. The quantity you
care about is the difference, and it has an interval of its own, which is narrower than you
would guess from two overlapping intervals when the comparison is paired — and *clearer* than
you would guess from two that barely miss each other, because non-overlap is a stricter
condition than the one you want, so two intervals that just fail to touch mean a difference
comfortably clear of zero. Compute the interval on the difference, and
compute it paired. In this chapter's data the intervals overlapped heavily *and* the paired
interval on the difference also contained zero — but the first fact was not the evidence for the
second.
5. Because it removes a source of variation rather than adding information. Unpaired, each
resample draws one set of cases for A and a different set for B, so the difference it computes
is charged for the luck of both draws. Paired, each resample draws one set of cases and both
prompts face it, so the case difficulty cancels and what is left is how the two prompts differ
on the same inputs. On this chapter's forty cases that took the width from 0.400 to 0.250, a
factor of 1.6, with no extra runs and no assumption. It works because the two prompts agree on most cases: the
more they agree, the more pairing buys.
6. The 120 rows are being counted as 120 cases, and they are not — they are 40 cases run three
times. The interval is computed over the things you drew from the world, and you drew forty
inputs. Recording them as 120 narrows the interval by about the square root of three without a
single new input, which is a precision you have not earned. Average the three runs within each
case so one case stays one row; the repeats then do the job they are for, which is reducing the
model's own run-to-run variation inside each case rather than pretending to be more cases.

> **You understand this when** somebody tells you a change improved their score by seven points
> and your first two questions are how many cases and whether both versions saw the same ones.
