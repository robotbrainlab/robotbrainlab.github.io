# Speed: What Makes This Slow

Chapter 15 took the two waits apart from the inside and said where the levers were without
pulling any. Chapter 49 pulled three of them on this book's own system and none of them moved
the number. This chapter is the menu those two were pointing at: what to measure, which lever
belongs to which wait, and how to find out whether a lever applies to you before you build it.

*The problem.* My system is correct and nobody will wait for it.

*The question.* What do I measure, and which lever do I pull?

## The Answer, First

**Almost nobody who says "it is slow" has said which wait they mean**, and until somebody does,
every lever is a guess. Chapter 1 named the two phases and said you feel them separately.
Chapter 15 said why they are different computations. The practical consequence is that *slow*
is at least four complaints:

| What somebody says | Which number moved | Where the lever is |
|---|---|---|
| Nothing happens for ages, then it is fine | The wait before the first token | This chapter's first half |
| It starts quickly and then crawls | The pace of the tokens after it | A shorter reply, or a smaller model |
| It is usually fine and sometimes awful | The slow end of the distribution | Capacity, concurrency, timeouts |
| Each call is quick and the whole thing is slow | The number of calls | Your own design, not the model |

Those four have almost nothing to do with each other. The first is a prefill and queueing
question. The second is decode, where every token costs a read of the parameters. The third is
partly the provider's queue and partly three decisions of your own, and none of it is about the
content of your request. The fourth is a fact about your pipeline that no provider can fix.

**So the order of work is measurement, then attribution, then one lever.** That order is not a
counsel of patience; it is what Chapter 49 cost. That chapter took three levers from this
chapter's list, priced them on its own traffic, and recommended none — and in every case the
reason was a property of the traffic rather than of the lever. Its prompts were below the
provider's minimum for the prefix cache. Its wait at those lengths was a queue rather than a
computation, so quadrupling the prompt moved nothing it could detect. And the expensive model
answered exactly as well as the cheap one on its own cases, so there was nothing to route to.

**A lever that cannot apply to your traffic is not a lever you can evaluate badly. It is one
you can skip.** Finding that out is cheap, and it is the step people leave out — so it opens
this chapter, and *Measuring On Your Own Workload* is the method for doing it properly.

## Two Numbers and a Distribution

Chapter 15 named the two: *time to first token* and *time per token*. It also said plainly
that measuring them on your own system was this chapter's job. So here is what to record, and
then the part that is not obvious.

| Record, per request | Why |
|---|---|
| Time to first token | The first complaint in the table above |
| Time per token, or the total and the token count | The second |
| The total | What a user actually waits, and the only one a product target can be written on |
| Input tokens, output tokens | So a slow request can be attributed rather than argued about |
| Cached input tokens | Whether the prefix cache fired, which Chapter 40 named as a field |
| The model, and every setting that changes the work | So a comparison is between two things that differ in one way |
| The sequence number and the wall-clock time | Chapter 49's hardest lesson, and the next section but one |

**And the first of those is the one you cannot read off a log**, which is worth saying because
it is where most attempts to measure this stop. A call's total time is in your log already:
request in, response out. The wait for the first token is not, unless you asked for the reply as
a stream and timed the arrival of the first piece of it. Chapter 19 owns the protocol — a
long-lived connection carrying one small event per line — and what this chapter needs from it is
the instrumentation: take a clock reading when you send, another when the first event arrives,
another at the last, and the two numbers fall out. Without the stream you have one number and
three complaints, and no way to tell which you are looking at.

That has a consequence worth planning for. A system that does not stream has not measured its
own first-token wait and usually cannot, so *add streaming for the measurement* is a reasonable
first move even where the product has no use for the words appearing one at a time. And
Chapter 19's warning comes with it: a reply your code must validate as a whole cannot be acted
on as it streams, so you stream it, time it, and still wait for the end before using it.

**And the three numbers are related, which is worth checking rather than assuming.** A request's
total is the wait for the first token plus one gap for every token after it:

```{=latex}
\[ \text{total} \approx \text{ttft} + \text{tpt} \times (\text{tokens} - 1) \]
```

That identity is what makes a budget possible, because it turns a target into a cap on
something you control. Here it is against the requests Chapter 49 recorded, along with the part
of this section that changes how you report latency at all.

```python
"""A latency budget, read off requests that actually happened.

    python3 budget.py

No model is called. The numbers come from the runs chapter 49 recorded
on this book's own system, which are still on disk: 144 requests in
`order.json`, each carrying the total and the token counts, and 72 in
`wait.json`, which carry the total too, plus the time to the first
token, the time per token and the chunk count. Chapter 49 owns what
the runs mean.
What this program does with them is the thing this chapter is about -
turning measured requests into a budget you can hold a design to, and
then finding out whether two dozen requests can hold it up.
"""
import json
import pathlib
import random
import statistics as st

CH49 = pathlib.Path.home() / "sandbox" / "ch49"
#  The baseline arm chapter 49 hands on: the grounded shape in the
#  order its step 3 recommends. One arm, so one question answered.
BASE = {"shape": "grounded", "order": "stable-first"}


def rows(name):
    p = CH49 / name
    return json.load(open(p)) if p.exists() else []


def rank(n, p):
    """Which request the p-th percentile IS, by the nearest-rank rule.

    Returned as well as used, because at two dozen requests a p95 is
    one request and the chapter should not be able to quote it without
    saying so.
    """
    return max(1, min(n, round(p / 100 * n)))


def pct(sorted_values, p):
    """The p-th percentile by the nearest-rank rule, so every value
    printed is a request that happened rather than an interpolation
    between two that did."""
    if not sorted_values:
        return float("nan")
    return sorted_values[rank(len(sorted_values), p) - 1]


def boot(stat, units, rounds=10000, seed=0):
    """Chapter 20's bootstrap: resample the UNITS with replacement,
    compute the statistic on each resample, and take the 2.5th and
    97.5th percentiles of those.

    The unit here is a (question, trial) pair rather than a request,
    which is what makes the next function a PAIRED comparison -
    chapter 20's *Compare on the Same Cases*.
    """
    rng = random.Random(seed)
    out = []
    for _ in range(rounds):
        s = [rng.choice(units) for _ in units]
        out.append(stat(s))
    out.sort()
    return out[int(0.025 * rounds)], out[int(0.975 * rounds)]


def paired(wait):
    """Every (question, trial) for which all three shapes ran.

    They all did - 8 questions x 3 trials - which is what lets the
    comparison below be paired rather than two separate samples.
    """
    by = {}
    for r in wait:
        by.setdefault((r["query_id"], r["trial"]), {})[r["shape"]] = r["ttft_s"]
    shapes = sorted({r["shape"] for r in wait})
    return [v for v in by.values() if len(v) == len(shapes)], shapes


def spread(values):
    v = sorted(values)
    return {"n": len(v), "min": v[0], "p50": st.median(v),
            "p90": pct(v, 90), "p95": pct(v, 95), "max": v[-1],
            "mean": st.mean(v)}


if __name__ == "__main__":
    order, wait = rows("order.json"), rows("wait.json")
    if not order or not wait:
        raise SystemExit("  chapter 49's runs are not here; nothing to read")

    base = [r for r in order
            if r["shape"] == BASE["shape"] and r["order"] == BASE["order"]]
    s = spread(r["total_s"] for r in base)
    over = sum(1 for r in base if r["total_s"] > s["mean"])
    print("  ONE ARM, END TO END, in seconds")
    for k in ("n", "min", "p50", "p90", "p95", "max", "mean"):
        print(f"    {k:5s} {s[k]:8.2f}" if k != "n"
              else f"    {k:5s} {s[k]:8d}")
    print(f"    mean / p50                   {s['mean'] / s['p50']:.2f}")
    print(f"    max  / p50                   {s['max'] / s['p50']:.2f}")
    print(f"    requests slower than the mean  {over} of {s['n']}")

    #  The budget identity, checked rather than asserted: a request's
    #  total should be the first token's wait plus one gap for every
    #  token after it.
    err = []
    for r in wait:
        pred = r["ttft_s"] + r["tpt_s"] * (r["chunks"] - 1)
        err.append((pred - r["total_s"]) / r["total_s"])
    print("\n  THE BUDGET IDENTITY, on 72 recorded requests")
    print("    total ~= ttft + tpt x (chunks - 1)")
    print(f"    median relative error        {st.median(err):+.4f}")
    print(f"    worst                        {max(err, key=abs):+.4f}")

    #  And what it is for: a budget turns a target into a cap.
    print("\n  WHAT A 2.00 s TARGET AT THE 95th ALLOWS")
    print("    shape       ttft p95   tpt p50    chunks left")
    for shape in sorted({r["shape"] for r in wait}):
        rs = [r for r in wait if r["shape"] == shape]
        t95 = pct(sorted(r["ttft_s"] for r in rs), 95)
        tpt = st.median(r["tpt_s"] for r in rs)
        left = max(0.0, 2.00 - t95) / tpt
        got = st.median(r["chunks"] for r in rs)
        print(f"    {shape:10s} {t95:8.2f}  {tpt*1000:8.1f} ms "
              f"{left:9.0f}   (sends {got:.0f})")

    #  Now the part the chapter would be dishonest without. Every p95
    #  above is ONE request of twenty-four, and chapter 20's rule is
    #  that the interval goes round the DIFFERENCE, not round each arm
    #  - two overlapping intervals are not the test.
    units, shapes = paired(wait)
    print("\n  WHICH REQUEST EACH p95 IS")
    for shape in shapes:
        v = sorted(u[shape] for u in units)
        print(f"    {shape:10s} p50 {st.median(v):5.2f}   p95 {pct(v, 95):5.2f}"
              f"   = request #{rank(len(v), 95)} of {len(v)}")

    print("\n  AND THE PAIRED DIFFERENCE IN p95, ON THE SAME"
          " QUESTIONS")
    for a, b in [("essay", "grounded"), ("grounded", "upfront"),
                 ("essay", "upfront")]:
        def gap(sample, a=a, b=b):
            return (pct(sorted(u[b] for u in sample), 95)
                    - pct(sorted(u[a] for u in sample), 95))
        d = gap(units)
        lo, hi = boot(gap, units)
        tell = "cannot tell" if lo <= 0 <= hi else "clears zero"
        print(f"    {a:8s} -> {b:8s} {d:+5.2f}   {lo:+5.2f} to {hi:+5.2f}"
              f"   {tell}")
    print(f"    {len(units)} paired units, 8 questions x 3 trials")
```

```text
  ONE ARM, END TO END, in seconds
    n           24
    min       0.98
    p50       1.31
    p90       1.85
    p95       2.18
    max      11.01
    mean      1.74
    mean / p50                   1.33
    max  / p50                   8.43
    requests slower than the mean  3 of 24

  THE BUDGET IDENTITY, on 72 recorded requests
    total ~= ttft + tpt x (chunks - 1)
    median relative error        -0.0061
    worst                        -0.1131

  WHAT A 2.00 s TARGET AT THE 95th ALLOWS
    shape       ttft p95   tpt p50    chunks left
    essay          1.10       7.9 ms       114   (sends 356)
    grounded       1.30      10.8 ms        65   (sends 32)
    upfront        2.13       9.4 ms         0   (sends 28)

  WHICH REQUEST EACH p95 IS
    essay      p50  0.74   p95  1.10   = request #23 of 24
    grounded   p50  0.75   p95  1.30   = request #23 of 24
    upfront    p50  0.87   p95  2.13   = request #23 of 24

  AND THE PAIRED DIFFERENCE IN p95, ON THE SAME QUESTIONS
    essay    -> grounded +0.20   -0.88 to +0.43   cannot tell
    grounded -> upfront  +0.83   -0.22 to +1.36   cannot tell
    essay    -> upfront  +1.03   -1.10 to +1.47   cannot tell
    24 paired units, 8 questions x 3 trials
```

## Report the Distribution, Not the Average

**Read the first block again, because the mean is wrong and it is wrong in the direction that
hides the problem.** Twenty-four requests, one arm, nothing exotic. The middle request took 1.31
seconds. The mean is 1.74. And **three of the twenty-four are slower than the mean** — so a
dashboard showing the average describes a request that almost never happens, and describes it
as worse than the typical one.

The reason is the slowest call: 11.01 seconds, 8.4 times the median. One request in
twenty-four, with no error and no retry — every call in the arm finished because the model
stopped, not because anything failed. Chapter 15 is why it exists — your
request waits to join a batch, so your latency depends on how busy the provider is, and that
is not a property of your prompt. Chapter 49 called this the sharpest evidence in it that the
wait is a queue.

A distribution shaped like that has a name worth having. **Tail latency** is the slow end of
the distribution — the 95th or 99th percentile rather than the middle — and in systems built on
a shared service it is usually the number your users are complaining about, because one user's
five requests include their own worst one. The median is what the system usually does. The tail
is what it does to somebody.

So report at least two numbers and never the mean alone: **a middle and a tail.** The middle
tells you whether the design is right. The tail tells you whether the capacity is.

| If you report | You will conclude |
|---|---|
| The mean | That the system is slower than it usually is, and miss the tail entirely |
| The median alone | That it is fine, and be surprised by the complaints |
| The median and the 95th | What the design does, and what the worst of it does |

**And a tail needs enough requests to have one.** Twenty-four requests give a 95th percentile
that *is* one request — the twenty-third of twenty-four, which the program prints alongside the
figure for exactly this reason, and which is why it takes percentiles by the nearest-rank rule
and quotes a value some request actually produced rather than an interpolation between two. At
two dozen calls a tail is an anecdote with a percentile sign on it. Chapter 20 is the chapter
about not over-reading a number this thin, and its rule applies here without modification —
which the last block of that output is, applied to this chapter's own headline.

## A Budget Turns a Target Into a Cap

The third block of that output is what the identity is for, and it is the most useful thing in
this chapter for an actual design review.

Take a product target — *the 95th percentile is under two seconds* — and subtract what the first
token costs at that percentile. What is left is a time budget, and dividing it by the measured
pace of the tokens gives a cap on the length of the reply. Three shapes from Chapter 49's runs,
and all three read differently:

- *The essay shape* has 1.10 seconds of first-token wait at the 95th and a pace of 7.9
  milliseconds a chunk, so two seconds allows about 114. It sends 356 — a threefold gap, and
  the arithmetic says by how much rather than that it feels slow.
- *The grounded shape* allows about 65 and sends 32, so it meets the target with room, and the
  room is the interesting part: the budget says a reply could be twice as long before anybody
  noticed.
- *The up-front shape* reads as allowing *nothing*: its first-token wait at the 95th is 2.13
  seconds, over the target before a single token of the reply exists. **Read that one against
  the last two blocks before you carry it**, because it is the row that does not survive them.

Every one of those 95th percentiles is the twenty-third request of twenty-four. The program says
so, because a figure that is one request should not be quotable without it. And then it does the
thing this chapter tells you to do two sections from here, which is to put an interval round the
*difference* rather than round each arm — Chapter 20 has a section called *Overlapping Intervals
Are Not the Test*, and its point is that the question is never *where is A* and *where is B* but
*where is B minus A*, which has an interval of its own. The three shapes ran on the same eight
questions three times each, so the comparison can be paired:

- essay to grounded, +0.20 seconds, from −0.88 to +0.43
- grounded to up-front, +0.83, from −0.22 to +1.36
- essay to up-front, +1.03, from −1.10 to +1.47

**All three contain zero, so none of the three designs' first-token waits can be told from
another's at the 95th on this data.** The up-front shape's 2.13 is one slow request and not a
property of the design — its twenty-second request is 1.23 — and Chapter 49 found the same thing
from the other side: on that shape, reordering the prompt so the provider could skip 2,432 of
2,458 tokens of prefill moved the *total* by −0.06 seconds, from −0.30 to +0.20, and quadrupling
the prompt moved the first token by +0.16, from −0.04 to +0.34. Neither clears zero. **The wait
at these lengths is a queue rather than prefill**, which is why the prompt is not the lever on it
either.

**Which leaves a method standing and a ranking withdrawn**, and the two are worth separating
because the method is the part you take to work. The essay row survives anything one request can
do to it: 356 chunks against a 114 budget is a threefold gap, and even at that shape's fastest
observed first token and fastest observed pace the allowance is 205. The up-front row does not
survive, and the section before this one — which said a tail at two dozen calls is an anecdote —
is why it cannot be quoted. **A budget tells you which designs are obviously out. Ranking the
rest needs more requests than this.**

So: a smaller reply is not a lever on a request whose first token has already spent the budget,
and on this system the prompt is not a lever on the first token either. What is left is the
target, or capacity, or finding out what the queue is doing — which is three sections on.

**And none of it is a prediction.** It is arithmetic over the pace of chunks a particular model
produced on a particular day, and every figure moves when the provider is busier. Two caveats
travel with the table. The pace is in *chunks* rather than tokens, and Chapter 49 had to check
that the two are the same thing here — its ratios were 1.04, 1.00 and 1.00 against the
provider's own counts, the 1.04 being the grounded shape in this very table. And the whole
exercise is twenty-four requests a shape. What survives is the method: measure the two numbers,
subtract, divide, put an interval round it, and find out whether the design is obviously out
before you start tuning it.

## What Your Own Design Adds

Most of the latency in a built system is not the model being slow. It is the number and the
size of the calls your design makes, and those are decisions somebody wrote down. Four of them
come up again and again, and each has a chapter that measured it.

| Decision | What it adds, and to which wait | Measured in |
|---|---|---|
| A long prompt | Prefill, growing faster than the text; and cache memory, which is what limits how many requests fit | Chapter 15's arithmetic; Chapter 28's window figure |
| Reranking the candidates | One model pass per candidate, before the answer starts | Chapter 45, at 105 calls |
| An agent loop | The whole wait again per step, each step carrying everything before it | Chapters 34 and 47 |
| A pipeline of stages | The sum of the stages, unless they are independent and run at once | Chapter 34 |

**A long prompt is the one people reach for and the one that costs on three counts at once.**
Chapter 15 has the arithmetic and this chapter will not repeat it, but the shape is worth
having in this order: prefill grows with the length, its attention part grows with the square
of it and is a minority until about 19,200 tokens, the cache you are holding grows with the
length, and every token of the reply then attends over all of it, so a long prompt makes a reply
that starts fast get slower. Chapter 28 put the memory in context: filling a 128,000-token
window costs cache on the order of the model's own weights, every sequence — and Chapter 16's
finding is that the model may not use the far end of it anyway. So the first question about a
slow request is almost always *what are we sending*, and the answer is almost always *more than
the answer needed*.

**Reranking buys ordering and costs a model pass per candidate.** Chapter 26 owns the method and
Chapter 45 measured it on this book's own corpus: 105 model calls, and the gain was not
tellable from zero. That is one corpus and eight queries, so it is not a verdict on reranking —
but it is the right shape for the decision, which is that a reranker is a latency line item
with a quality return you have to measure rather than assume.

**An agent loop multiplies everything.** Chapter 4 owns the loop and its step limit; what
matters for speed is that each step is a whole request, and each step's prompt carries the
history before it, so step eight is not step one. Chapter 35's worked run put tool results at 91.5 per
cent of the context — a plausible construction rather than a measurement, which that chapter
says of itself — and Chapter 48 measured 87.3 per cent on its own fourteen-step run over a
different denominator. The shape is what carries: the results dominate. Chapter 47 then compared
a loop against a fixed path on the same work and found the loop's cost per success 1.70 times
the fixed path's at a matched budget, and 1.85 times on the arm that confounds budget with
design — that chapter's own lesson being not to quote the second figure as the design's. **A
loop's wait is the sum of its steps and its prompt grows as it goes**, which is why a step limit
is a latency decision as much as a cost one.

**And a pipeline of stages costs the sum of them unless they are independent.** Chapter 34's
parallelisation is the case where they are: one call per piece, run at once, so the whole thing
takes about as long as the slowest rather than as long as all of them added up. That is the
cheapest latency win in this chapter and the one least often taken, because it is a change to
the shape of your code rather than a setting. Chapter 19 owns what it takes to run calls at
once without attacking your own rate limit.

## The Lever Menu, and Which Wait Each One Touches

Now the levers. The useful way to hold them is by which number they move, because that is the
question the first section told you to answer first.

| Lever | Moves | Costs you | Applies when |
|---|---|---|---|
| Send less | Both waits, and the memory | Whatever the dropped text was worth | Always worth asking |
| Stream the reply | Not the total; the first-token wait, down to prefill | You cannot check a whole answer as it arrives | The reply is read as it arrives, or you want to measure |
| Prompt-prefix caching | The first token, and the bill | Nothing, if your prompt qualifies | Many requests share a long leading block |
| A response cache of your own | The whole wait, to nothing | Staleness, and a key you have to get right | Requests actually repeat |
| A smaller model | Both waits, and the memory | A different model, whose quality you measure from scratch | The cheap model is good enough on your cases |
| A cascade | The wait, upwards, on every escalation | Both calls when it escalates | The dear model is measurably better where it escalates |
| Fewer or shorter steps | The number of waits | What the steps were doing | A loop or a pipeline |
| Running independent work at once | The sum, down to the slowest | Concurrency to manage | The pieces do not depend on each other |
| Serving it yourself | All of it, in both directions | An operational burden | You have the traffic and the people |

Two of those are worth separating from the rest before going on.

**Streaming does not move the total**, and it is often the best thing on the list. Chapter 19
owns the mechanics and Chapter 1 the reason it works: two systems with the same total time feel
completely different, and the one that shows a word quickly feels responsive. What it does move
is the first-token wait, which falls from the whole generation to whatever prefill takes — and,
as the second section said, it is what makes that number measurable at all. So the thing to
expect is a dashboard whose *total* does not improve after the complaints stop, which is why
streaming has to be kept separate from the levers that move the total. Its one real cost is
Chapter 19's: you cannot stream a reply your code must validate as a whole, because the check
needs all of it — unless the reply is a sequence of independent units, one object or row at a
time, each of which is whole the moment it lands, which is that chapter's own edge case and the
one place the rule relaxes.

**And *send less* is first on the list because it helps both waits and the memory at once
without changing the model**, so nothing about the model's quality has to be established again.
A smaller model and quantisation move all three numbers too, and both of them hand you a
different model whose answers you have to measure from scratch. What sending less costs you is
narrower and easier to reason about: whatever the dropped text was worth, which Chapter 28's
budget arithmetic is how you decide. Chapter 28's budget
arithmetic is where the decision lives for a retrieval system, and the sentence to carry out of
it is that a long window buys the room to be generous and does not remove the need to choose.

## The Queue You Built Yourself

The third complaint in this chapter's opening table — usually fine, sometimes awful — is the one
whose lever is not in the list above, because it is not about the model at all. Three of your own
decisions make a tail, and Chapter 19 owns all three mechanically while this chapter owns what
they do to the number.

**A concurrency limit is a queue.** Chapter 19's semaphore bounds how many calls run at once,
which is what keeps you inside a rate limit and is the right thing to have. What it also does is
hold requests that arrive while it is full. A limit of ten on traffic that offers twelve at once
means two requests wait for a whole call to finish before theirs begins, and their total is
somebody else's total plus their own. That wait is invisible in any measurement that starts when
the call starts — which is most of them — so **measure from when the request arrived, not from
when you got round to it.**

**A retry more than doubles the wait, and the request it doubles was already the slow one.**
Chapter 19's backoff and jitter are what you want when a provider is struggling, and they are
also a latency decision: a request that fails after four seconds, waits a second, and succeeds
in four more took nine, and it lands in your tail. So watch the retry rate, which Chapter 19
says to alarm on, *and separately* the latency of the requests that retried, kept apart from
the rest — the rate tells you the provider is struggling and the latency tells you what it cost
the person waiting.

**And a timeout is a decision about the tail, written as a number.** This is the one worth
restating in latency terms, because Chapter 19 derives it from the token cap and the derivation
is the same arithmetic as this chapter's budget: at a pace of `\(r\)`{=latex} tokens a second a
cap of `\(m\)`{=latex} tokens cannot finish in less than `\(m/r\)`{=latex} seconds, so that is
the floor and Chapter 19's crude `max_tokens / 20 + 10` puts headroom above it. Set the timeout
below the floor and you are cancelling replies that were going to arrive; set it at thirty
seconds out of habit, on a cap of a thousand tokens, and you have built a system that kills its
own long answers. **And put your own pace in it rather than the twenty**: this chapter's three
measured shapes run at 7.9 to 10.8 milliseconds a chunk, which is 93 to 127 a second, four to
six times Chapter 19's rule of thumb — and that chapter's Note says in so many words that the twenty is
one of the figures to measure rather than inherit. The timeout
is where you decide what a hopeless request costs you, and the right place to read it off is
your own distribution: a cap a little above your 99th percentile turns a stuck connection into
a fast failure instead of a held worker.

Those three together are why the same system can have a good median and a tail nobody can
explain from the provider's side. **None of them is visible in a measurement of the call.**

## Prompt-Prefix Caching, and Ordering For It

Chapter 49 owns this term and priced it. What this chapter owes you is what it takes to qualify,
because the lever is unusual in being nearly free when it works and completely inert when it
does not.

The mechanism is that a provider which has already processed a leading run of tokens can reuse
that work rather than redoing it, so the part of prefill that covers those tokens largely goes
away. Three properties follow, and all three are places it fails:

**It matches a prefix, so the first bytes decide everything.** A timestamp at the top of the
prompt, a user's name, a session id, an example list shuffled for variety — any of those
changes byte one and the match is gone for the whole request. This is the failure that is
invisible, because nothing errors; the request simply costs what it always did.

**It has a minimum length, below which it never fires.** Chapter 49 met this one: two of its
three shapes have prompts of about 612 and 637 tokens against a provider minimum of 1,024, so
the lever could not fire for them in either prompt order. A system whose prompts are short has
nothing to tune here, and finding that out is one field in one response.

**And it is a discount on the tokens it covers rather than their removal.** They are still your
tokens; they are cheaper. Chapter 53 owns what that does to the bill.

So the design-time half is Chapter 18's, which put the four blocks of a prompt in the order
instructions, examples, format, then the supplied information, precisely so that the unchanging
part is at the front by construction. **That order is the whole of what you do for this lever.**
Put the stable part first, keep the volatile part — the user's question, the retrieved passages,
anything with a time in it — behind it, and then watch the field.

**And the scoping Chapter 49 found is the thing most accounts of this lever get wrong.** What it
buys is *different* requests sharing a leading block. It is not a request reusing its own
earlier self: that is a response cache, which is the next section and a different mechanism with
a different owner. Chapter 49 priced the lever at $0.19 per thousand requests on traffic where
each question is asked once, and found that pricing it against repeats of the same question
*understates* it by a factor of 2.8. The reason is worth following, because it is a trap you can
walk into with your own logs: on a repeated question the arm *without* the lever reuses its own
earlier self through the same prefix cache, so the repeats flatter the comparison baseline and
the gap between the arms closes. **Price a shared-prefix lever on traffic where each request is
new**, which is what your traffic mostly is.

## A Response Cache of Your Own Is Not the Provider's

The lever with the largest effect in this chapter is the only one that removes the call. A
**response cache** is your own store, keyed on what determines the answer, returning a previous
reply without asking the model at all. It takes the wait to nothing and the cost to nothing, on
the requests it hits.

The two caches in this chapter are easy to confuse and have nothing in common beyond the word.

| | Prompt-prefix cache | Response cache |
|---|---|---|
| Whose | The provider's | Yours |
| What it reuses | The work of processing a leading block | A whole answer |
| What it saves | Part of the first token's wait, and a discount | The entire request |
| What it needs | A shared prefix past a minimum length | The same request arriving twice |
| What it never does | Remove a token from your bill | Produce an answer the model has not already given |

**The whole difficulty is the key**, and getting it wrong is how a response cache becomes a
defect rather than a lever. The key has to be everything that determines the answer, which is
more than the user's question:

- The question, and the instructions and settings sent with it, because a different
  temperature is a different distribution.
- The model, named with its version — Chapter 54 owns why the short name is not a version.
- Whatever retrieval put in the context, because the same question over different passages is a
  different request. This is the one that catches people: a cache keyed on the question alone
  serves yesterday's answer after the documents change.
- **And the caller's scope.** Chapter 51's rule arrives here with nothing added: a cache keyed
  without the caller serves one caller's answer to another, and a per-caller tool with a
  cache that forgot the caller is a per-caller tool no longer. It is the cheapest way to
  undo that chapter's authorisation section.

Two more things, and the first decides whether to build it at all.

**Measure how often your requests actually repeat before building this.** Chapter 49 noted the
difficulty in passing: normal traffic does not ask the identical question twice very often, and
the lever is worth exactly its hit rate. That is a measurement you can take from a log you
already have, in an afternoon, without building anything — the number of requests whose key
would have matched an earlier one. A hit rate of a few per cent is a lever not worth its
staleness; a high one makes this the best thing on the menu, and systems answering a narrow set
of questions — support, documentation, a product catalogue — are where high ones are reported.
How high is a measurement about your traffic and not a figure to carry from here.

**And a cached answer is more consistent than a fresh one, which is not always a virtue.**
Chapter 13 established that the same request can come back differently. A cache freezes one of
those answers and serves it to everybody, so your system looks steadier than it is — and the
day the cache is cleared, behaviour the team believed was settled starts moving again. That is
worth knowing before somebody reports it as a regression.

## Model Routing, and Cascades

**Model routing** is choosing which model serves a request, per request. Chapter 34 uses the
word *routing* for a different thing — one call picking a branch from a menu your code wrote —
and says so in its own Key Terms; the two do not interfere and it is worth being explicit about
which one you mean, because an interviewer may mean either.

The shape is simple and the evidence it needs is not. Route the easy requests to a cheap, fast
model and the hard ones to a capable one, and both numbers in this chapter improve on most of
your traffic. What makes it hard is that *easy* has to be decided before the answer exists,
which means the router is a classifier, and Chapters 30 and 31 are what it takes to believe one.

**A cascade is the version that does not need the classifier**, and Chapter 49 owns the term:
run the cheap model, judge its answer with your own code, and escalate to the capable one when
the answer is unusable. It is attractive because the judgement happens after the fact, where
there is something to judge.

**And it is slower, which the cost argument usually hides.** An escalated request pays both
waits, one after the other, so a cascade's tail is the sum of two models' tails. On latency a
cascade is a lever in the wrong direction for every request it escalates, and it is only a win
overall if the escalation rate is low and the cheap model is fast.

Chapter 49 priced one and the result is the thing to carry into any design review that proposes
it:

- Both models answered *12 of 12* of its cases, so there was nothing the expensive one was
  better at — and the evidence is twelve cases rather than thirty-six rows, because the cheap
  model's three trials came back byte-identical.
- The cascade cost **5.4 times the cheap model** by the point estimate, on an interval that does
  not clear zero at twelve cases, and bought the same answers.
- Three of the twelve escalated, and **all three were correct answers.** The escalation rule was
  a phrase list built to catch a model declining to answer, and it matched correct answers
  worded in the negative — because *cannot* and *does not* are how a refusal and a correct
  negative answer are both worded, and one of the three was *account credit, which does not
  expire*, which is not a refusal in any sense.

That last point is the general one and it is not about cascades. **An escalation rule is a check,
so it has a check's failure modes**, and the one it will have is firing on the cases whose right
answer looks like the failure. Chapter 30's method is how you find that out: read the cases it
fired on. Chapter 49 found all three by printing them.

So the order for this lever: establish that the expensive model is better **on the cases that
escalate**, not on average; then measure what your escalation rule fires on; and only then
price it, remembering that the price includes both calls and both waits.

## If You Serve the Model Yourself

Everything so far is a lever on a hosted service. If you run the model, four more open up —
and Chapter 7 put the right frame on them in one line: this chapter covers serving as a lever
you might pull, not as a thing you will operate. So what follows is enough to recognise the
names, say what each one trades, and know which of Chapter 15's two phases it touches. It is
not enough to run a serving stack, and nothing here should be read as advice to start.

**Continuous batching** is the largest of the four. Chapter 15 established why batching works at
all — one read of the parameters serves every request in the batch — and noted that real systems
do not fill a batch and run it to completion. This is the name for what they do instead:
requests join and leave the batch as they arrive and finish, so a short reply does not wait for
a long one sharing its pass. It works on decode, where the shared read is, and what it buys is
the machine's throughput at a given latency. What it costs is a scheduler with a great deal of
behaviour in it, and a request whose latency now depends on its neighbours even more than
Chapter 15 said.

The second is a **paged key–value cache**, and Chapter 15 pointed at it too. The cache for one
sequence grows as the sequence does, and reserving one contiguous block per request for the
longest reply it might produce wastes most of the memory most of the time. Holding it in fixed
pages, with a table mapping a sequence's positions to pages, lets the unused space serve
somebody else — so the same card holds more conversations, and Chapter 15's arithmetic is where
you see why that is the number that matters. It makes neither phase faster — what it moves is how many
requests fit, which is a throughput lever first and a latency one second — and its cost is a
table consulted on every attention read, plus waste at the granularity of a page rather than of
a sequence.

**Speculative decoding** is the one that looks like cheating and is not. Decode is
memory-bound: reading the parameters is the expensive part and the arithmetic afterwards is
nearly free. So let a small, fast model propose several tokens, then have the large model check
all of them in a single pass — which costs one read of its parameters rather than one per token.
Accepted tokens are kept; the first rejection discards the rest, and the pass has not been
wasted, because the large model's own next token comes out of it, so every pass makes at least
one token of progress. The win is the number of proposals accepted on average, so **the lever's
value is an acceptance rate you have to measure on your own traffic**.

Two things to be exact about, because this is the one mechanism in the chapter no earlier
chapter covers. **What the scheme preserves is the large model's distribution rather than its
output**: with the correct acceptance rule you get a sample from the distribution the large
model would have produced, which is not the same as the sample it would have produced, and the
guarantee is a property of that rule — the looser acceptance rules some implementations
offer trade that guarantee away, and then the quality is a thing to go and measure again. And
the costs are real:
a second model to run and host, sharing the large one's tokeniser, and a verification pass that
does several positions' arithmetic for one read of the weights. That last one is the trade worth
seeing, because it runs against continuous batching: speculation spends the arithmetic slack
that being memory-bound leaves you, so it buys latency where the batch is small and gives up
throughput where the batch is full.

*And quantisation* is Chapter 15's, where the arithmetic is. What belongs here is that it is
a latency lever as well as a memory one — fewer bits per parameter is less to read, and decode
is waiting on exactly that — and that its cost is a quality change you have to measure on your
task, which Chapter 20 is how to do. Chapter 15's own lab is the arithmetic: the same card went
from six conversations to nine on 4-bit weights, and to thirty-seven when the cache was
quantised too, because the cache was the binding constraint all along.

**The honest summary of this section is that these four are most of why a hosted provider is
faster and cheaper than a first attempt at running it yourself.** They are also why the decision
to self-host is not a latency decision: it is a decision about traffic, people and
operations, and Chapter 53's bill is the other half of it.

## Measuring On Your Own Workload

This is the method, and it is the one that makes the rest of the chapter safe to use.

**Ask whether the lever applies before you build it.** Two of Chapter 49's three did not, and
both answers were available in advance: a prompt length against a published minimum, and a
model comparison on twelve cases. **The cheapest step of any lever is the one that finds out it
cannot fire.**

**Interleave the arms and record the order.** This is the mistake Chapter 49 put on its own
record. Its first timing run put each prompt shape in a block, so the shape and the moment it
ran were one variable, and it reported an effect of 0.23 seconds with an interval clear of zero
that was the running order. Interleaving does not remove drift; it makes it visible, which is
why the sequence number is on the list of things to record.

**Put an interval round a latency difference.** Chapter 20 owns this and latency is where it is
most often skipped, because a stopwatch feels like a measurement. Chapter 49's time-to-first-token
comparison is the warning: two runs of the same comparison gave point estimates 0.17 seconds
apart and neither cleared zero.

**And quote the baseline you are measuring against.** Chapter 49 handed one on: **$0.11 per
thousand requests at a median of 1.31 seconds**, on this book's own system, with the mean of
1.74 distorted by a single call of 11.01. Chapter 53 measures the bill against the first half of
that. The second half is this chapter's, and the reason to write it down is that *faster* is not
a claim anybody can check without it.

The product half closes the chapter, because it is the part an engineer forgets. Chapter 1 said
it first: which of the two phases you optimise is a product decision before it is a technical
one. A system that answers in four seconds and starts writing in one is a different product
from one that answers in three and shows nothing until it is done, and the faster of those two
is the one users call slow.

## What This Chapter Has Not Told You

Four things, deliberately.

**How to run a serving stack.** The four self-hosting levers are named so you can recognise them
and say what they trade. Operating them is a different book, and Chapter 7 says so in the map.

**Anything about the model's own speed that Chapter 15 does not already own.** Prefill, decode,
the key–value cache, batching, quantisation, mixture of experts, memory-bound and compute-bound,
and the arithmetic under every figure here — all of it is that chapter's, and this one measures
from outside.

**The bill.** Every lever in this chapter has a price and several were priced here in passing,
but cost as a product constraint, with reasoning tokens and the features that multiply usage,
is Chapter 53's, and it measures against Chapter 49's baseline rather than restating it.

**And how to diagnose a slowdown that arrived without a change of yours.** A provider's model
updates, a region gets busy, a dependency slows down. Attributing that is Chapter 54's subject,
along with pinned versions and the regression suite a provider's update has to pass.

## Summary and Key Terms

### Summary

*Slow* is at least four complaints and almost none of them shares a lever: nothing appears for
seconds, the
words crawl once they start, it is usually fine and sometimes awful, or every call is quick and
the whole thing is slow. So the order of work is measurement, attribution, then one lever —
which is what Chapter 49 cost, having priced three of this chapter's levers on its own traffic
and recommended none, each time for a property of the traffic rather than of the lever. Record
the two numbers Chapter 15 named, the total, the token counts, the cached-token count, the model
and *the sequence number*, and report **a middle and a tail** rather than a mean: on one
twenty-four request arm the median is 1.31 seconds, the mean 1.74, and only three requests are
slower than the mean, while the slowest is 8.4 times the median — **tail latency** on a shared
service is usually what your users are complaining about, and the mean describes a request that
almost never happens. The
three numbers are related by `\(\text{total} \approx \text{ttft} + \text{tpt} \times (\text{tokens} - 1)\)`{=latex},
whose median relative error over 72 recorded requests is 0.6 per cent, with one request out at
11, and which **turns a product target into a cap**:
a two-second target at the 95th allows about 114 chunks on the essay shape, which sends 356.
**And then the same twenty-four requests take the ranking back**: every one of those percentiles
is the twenty-third request of twenty-four, and the paired difference between any two shapes —
Chapter 20's test, since overlapping intervals are not one — contains zero at +0.20, +0.83 and
+1.03. So a budget tells you which designs are obviously out, the essay shape's threefold gap
among them, and needs more requests than this to rank the rest.
In a built system most of the latency is your own design — a long prompt, a reranker's pass per candidate, an agent
loop's whole wait per step with a prompt that grows as it goes, a pipeline whose stages could
have run at once. Of the levers, **streaming leaves the total alone, moves the first-token wait down to prefill
and is what makes that number measurable at all**;
*sending less* is the one that helps both waits and the memory without
handing you a different model to re-measure; prompt-prefix caching
is free when it applies and inert when it does not, since it matches a prefix that any leading
timestamp destroys and has a minimum length Chapter 49's prompts of 612 and 637 tokens fell
under, and Chapter 18's block order is the whole of what you do for it; a **response cache** of
your own is the only lever that removes the call, and its key has to carry the model version,
the retrieved passages and *the caller's scope*, or Chapter 51's authorisation section is
undone; **model routing** needs a classifier you have validated, and a cascade avoids the
classifier at the price of both waits on every escalation — Chapter 49's cost 5.4 times the
cheap model — a point estimate twelve cases cannot separate from zero — for answers both models
got 12 of 12, escalating on three correct answers, because
*cannot* and *does not* are how a refusal and a correct negative are both worded. If you serve the model
yourself there are four more — **continuous batching**, a **paged key–value cache**,
**speculative decoding**, whose value is an acceptance rate and which, under the correct
acceptance rule, returns a sample from the large model's own distribution, and quantisation — and they are most
of why a hosted provider beats a first attempt at running it. And the method under all of it:
ask whether a lever can fire before building it, interleave the arms and record the order, put
an interval round the difference, and write the baseline down, because *faster* is not a claim
anybody can check without one.

### Key Terms

| Term | Meaning |
|---|---|
| **Tail latency** | The slow end of the latency distribution — the 95th or 99th percentile rather than the middle. On a shared service it is usually what users are complaining about, because one user's handful of requests includes their own worst |
| **Response cache** | Your own store of previous answers, keyed on everything that determines the answer, returning one without calling the model. The only lever that removes the request. Not the provider's prefix cache, which discounts work on a request that still happens |
| **Model routing** | Choosing which model serves a request, per request. Needs a judgement about difficulty made before the answer exists, so the router is a classifier. Chapter 34's *routing* is a different thing — one call picking a branch your code then runs |
| **Continuous batching** | Letting requests join and leave a running batch as they arrive and finish, rather than filling a batch and running it to completion, so a short reply does not wait for a long one |
| **Paged key–value cache** | Holding the cache in fixed pages with a table from a sequence's positions to its pages, so memory reserved for a reply that never arrives can serve somebody else |
| **Speculative decoding** | A small model proposes several tokens and the large one checks them in a single pass, which costs one read of its parameters instead of one per token. Accepted tokens are kept and every pass makes at least one token of progress. Under the correct acceptance rule the output is a sample from the large model's own distribution, so the quality is unchanged; the win is the acceptance rate, and the cost is a second model plus the arithmetic slack that being memory-bound leaves you |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The latency identity | `\(\text{total} \approx \text{ttft} + \text{tpt} \times (\text{tokens} - 1)\)`{=latex} — median relative error 0.6% over 72 recorded requests, one of them out at 11% |
| What to report | A middle and a tail, never the mean. On one 24-request arm: median 1.31 s, mean 1.74 s, slowest 11.01 s, and **3 of 24 slower than the mean** |
| A budget, worked | A 2.00 s target at the 95th allows ~114 chunks on the essay shape, which sends 356 — a gap no one request closes. Then test it Chapter 20's way: at 24 requests a p95 *is* one request, and the paired difference between any two shapes contains zero, so the budget rules a design out and does not rank the rest |
| The first question about any lever | Whether it can fire on your traffic. Two of Chapter 49's three could not |
| Why a prefix cache does nothing | A minimum prompt length, and a prefix any leading timestamp destroys. 612 and 637 tokens against 1,024 |
| What a response cache needs in its key | The prompt and settings · the model version · the retrieved passages · *the caller's scope* |
| A cascade's latency | Both waits in sequence on every escalation. Chapter 49's cost 5.4x the cheap model for the same answers — a point estimate on an interval that does not clear zero at 12 cases |
| Where prefill's squared term takes over | About 19,200 tokens, from Chapter 15. *At a thousand tokens* doubling the prompt multiplies prefill by about 2.1 rather than by 4; the factor climbs with the prompt and reaches 3 at the crossover |
| A total timeout from the token cap | The floor is `max_tokens / r` at your own measured pace `\(r\)`{=latex}; Chapter 19's crude `max_tokens / 20 + 10` puts headroom above it and is far better than a flat 30. This chapter's own three shapes run at 93 to 127 a second, not 20 |
