# Cost: What This Costs Me

Chapter 15 said why a token costs what it does, from the inside. Chapter 49 priced three levers
on this book's own system and recommended none, leaving a baseline of eleven cents per thousand
requests. Chapter 52 took the latency half of that baseline and turned a product target into a
cap. This chapter takes the other half: the bill, what is in it, and what to do when it arrives
and nobody can say where it went.

*The problem.* The bill arrived and I cannot account for it.

*The question.* Where did the money go, and what should a request be allowed to cost?

## The Answer, First

**A bill is a sum of per-request token counts at three prices, and a provider's own breakdown
splits it by the model, the day and the key or project it was billed to, and by nothing else.** That is the whole difficulty, and it is
a difficulty about records rather than about money. The console shows a total per model per day.
Your traffic is not organised by model or by day; it is organised by what the requests were
*for* — which customer, which feature, which prompt shape, which design decision somebody made
in a meeting. Nothing on the provider's side knows about any of that, so nothing on the
provider's side can tell you that the number went up because a retrieval step started fetching
ten passages instead of three.

Chapter 5 put this as two activities rather than one: watching a number, and being able to
attribute a change in it to a change you made. The second is the one this chapter is about, and
it has a short answer. **Cost attribution** is splitting a bill by something you can change, and
there are two ways to get it.

The cheap one is to make the provider's own grouping the grouping you want: a separate key or
project per feature, per environment, per customer tier, and the console's own breakdown becomes
the split. Chapter 51 arrived at the same setting from the other direction, because a key scoped
to one project with a spending cap reaches much less when it leaks. It costs nothing, it needs no
code, and what it cannot do is split a bill by anything finer than a key.

The other is to record the provider's own token counts with every request, labelled with what the
request was for, at the time you make it. That is the one that answers questions nobody thought
of in advance, and it is the one that cannot be done retrospectively: a month of traffic whose
counts were not stored can be re-estimated from the prompts if you kept them and can never be
reconciled against the bill, because your tokeniser's count is not the one you were charged for.
**The fix starts with the next request rather than with the last one.**

Three things follow, and they are the shape of the chapter:

| The question | What answers it |
|---|---|
| What is in a bill? | Three token counts and three prices. The formula is this chapter's |
| Where did it go? | A key per group, or records you kept — grouped by something you can change |
| What should it be? | A cap you wrote down before the design, like Chapter 52's latency budget |

**And the third is the one that is skipped.** A cost per request is a product constraint in
exactly the way a latency target is, and almost nobody writes one down — so the first time
anybody asks what a request may cost is after the bill, when the answer has already been
decided by a hundred small choices nobody priced.

## The Arithmetic That Turns a Count Into a Bill

Several chapters have counted tokens and said, in so many words, that a count is not a bill.
Chapter 37 said it of two agent designs whose token counts rank one way and whose prices may
rank the other. Chapter 34 said it of a loop's quadratic and handed over "the arithmetic that
turns one into the other". Here it is, and it is one line:

```{=latex}
\[ \text{cost} = (\text{in} - \text{cached}) \times p_{\text{in}}
  + \text{cached} \times p_{\text{cached}}
  + \text{out} \times p_{\text{out}} \]
```

Four things about it are worth more than the line itself.

**The three prices are different, and output is the dear one.** On the small model this book
uses, input is $0.15 per million tokens, a cached input token $0.075, and output $0.60 — so one
output token costs four input tokens. On a reasoning model priced a few paragraphs from here it
is eight. Chapter 10 said you control your input exactly and your output only by capping it or asking for
less;
this is the other half of that asymmetry, and it is why an instruction that produces six
paragraphs where one would do is a cost problem with a style-shaped cause.

**A cached token is subtracted and charged again, never dropped.** Chapter 49 owns the
prompt-prefix cache and Chapter 52 said what it takes to qualify, and both are careful that the
discount covers tokens you still sent. The formula says it precisely: the cached count comes
out of the fresh term and goes into its own at half the rate. A prefix cache can therefore cut the input half of a bill
by the gap between the two input rates — half of it on the small model here, nine tenths on the
reasoning model in the next section — and can never remove a line from it.

**Reasoning tokens need no term of their own, which is exactly the problem.** The provider
counts them inside the output figure. They are charged at the output rate, they are not sent to
you, and the next section is what they do to the total.

**And the count is the provider's, not yours.** Chapter 10 owns the tokeniser and Chapter 40
warned that a corpus priced with one model's vocabulary can cost three times as much under
another's. The consequence for a bill is a rule with no exceptions: **read the counts out of the
response and store them.** Your own estimate of a prompt's length is a planning tool; the
provider's count is what you are charged for, and the gap between them is not something you
can reason about from outside.

## Reasoning Tokens: Output You Pay For and Never See

Chapter 40 printed a field called `reasoning_tokens` out of a response, found a zero in it, and
said it was this chapter's. It is not zero on a model that has a reasoning mode, and it is the
only part of a bill whose text you never see, because the tokens it counts are charged to you
and not sent to you.

Chapter 16 owns what they are, and the sentence to carry from it is that the model's only
scratchpad is its own output: a model that works through a problem has to write the working down.
That chapter puts the price of a visible chain at about five times the answer alone. A reasoning mode is the same mechanism with the working withheld. The provider generates
it, charges for it at the output rate, counts it inside the output figure, and returns the answer
without it.

The tokens it generated and did not send you are **reasoning tokens**. They are the subject of
this section, and the only thing about them a cost chapter needs is how many there are.

So the question this chapter asks is the narrow one: what does the setting cost? One model, one
question at a time, and nothing changing between arms but the effort setting.

```python
"""What a reasoning mode costs, read off the provider's own counts.

    python3 reason.py

Chapter 40 printed `reasoning_tokens` as a zero and said this chapter
owned it. Here it is not zero. One model, one question at a time, and
the only thing that changes between arms is the effort setting - so
the comparison is within a model rather than across two, and nothing
here is a claim about reasoning as a technique. Chapter 16 owns why
working step by step helps at all; this program prices it.

36 calls in the arms, and one more at the end to show what a cap
below the working buys. Temperature is not set, because a reasoning model does not
take it, so chapter 13's warning applies with nothing to turn off -
which is why every cell is three trials and chapter 20's interval
goes round the difference. The per-call log goes to the error stream,
so what is printed below is the summary and the log is for whoever
is watching it run. A finished run is written to `reason.json`; if an
earlier one is on disk the summary is printed for it too, which is
how a measurement this thin says whether it reproduced.

Prices per million tokens, read on 30 October 2026 and written down
rather than fetched, as chapter 49's are.
"""
import json
import os
import pathlib
import random
import re
import statistics as st
import sys
import time
import urllib.request

MODEL = "gpt-5-mini-2025-08-07"
URL = "https://api.openai.com/v1/chat/completions"
PRICE = {"in": 0.250, "cached": 0.025, "out": 2.000}
EFFORTS = ["minimal", "low", "medium", "high"]
TRIALS = 3
CAP = 8000

#  Three questions with one right answer each, short enough that the
#  reply is a number and the visible half of the output is tiny. The
#  grader is code, so it gives the same verdict every time - which
#  chapter 31 is careful to say is not the same as being right.
QUESTIONS = [
    ("pens",
     "Pens are 1.25 for a pack of three. Notebooks are 2.40 each."
     " I buy 12 pens and 3 notebooks and pay with 20. What change"
     " do I get? Reply with the amount only.", 7.80),
    ("tank",
     "A tank holds 240 litres and is three-quarters full. A pump"
     " removes 15 litres a minute. How many minutes until it is"
     " empty? Reply with the number only.", 12.0),
    ("parts",
     "Three machines make 450 parts in 5 hours. How many hours do"
     " five machines need to make 1,350 parts? Reply with the"
     " number only.", 9.0),
]


def call(prompt, effort, cap=CAP):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    payload = {"model": MODEL, "reasoning_effort": effort,
               "max_completion_tokens": cap,
               "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        URL, json.dumps(payload).encode(),
        {"Authorization": f"Bearer {key}",
         "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            break
        except Exception as exc:          # noqa: BLE001 - chapter 19
            if attempt == 3:
                raise
            print(f"      retry {attempt + 1}: {type(exc).__name__}",
                  file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    u = d["usage"]
    out = u["completion_tokens"]
    reasoning = u["completion_tokens_details"]["reasoning_tokens"]
    return {"text": d["choices"][0]["message"]["content"] or "",
            "in_tokens": u["prompt_tokens"],
            "cached": u["prompt_tokens_details"]["cached_tokens"],
            "out_tokens": out, "reasoning": reasoning,
            "visible": out - reasoning,
            "finish": d["choices"][0]["finish_reason"],
            "seconds": round(time.time() - t0, 3)}


def bill(r):
    """The same formula as where.py. Reasoning tokens need no term:
    they are already inside the output count, which is the whole
    point - the provider charges them at the output rate and does
    not send them to you."""
    fresh = r["in_tokens"] - r["cached"]
    return ((fresh * PRICE["in"] + r["cached"] * PRICE["cached"]
             + r["out_tokens"] * PRICE["out"]) / 1_000_000)


def first_number(text):
    m = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    return float(m.group()) if m else None


def boot(stat, units, rounds=10000, seed=0):
    """Chapter 20's bootstrap, resampling the UNITS with replacement.
    A unit is a (question, trial) pair, which is what makes the
    comparison below paired rather than two separate samples."""
    rng = random.Random(seed)
    out = []
    for _ in range(rounds):
        out.append(stat([rng.choice(units) for _ in units]))
    out.sort()
    return out[int(0.025 * rounds)], out[int(0.975 * rounds)]


def summarise(runs, label):
    print(f"\n  {len(runs)} calls, {label}")
    print("  ONE MODEL, ONE QUESTION AT A TIME, FOUR SETTINGS")
    print("    effort   visible  reasoning       range   invis  right")
    for effort in EFFORTS:
        rs = [r for r in runs if r["effort"] == effort]
        vis = st.median(r["visible"] for r in rs)
        rea = st.median(r["reasoning"] for r in rs)
        lo = min(r["reasoning"] for r in rs)
        hi = max(r["reasoning"] for r in rs)
        share = sum(r["reasoning"] for r in rs) / sum(
            r["out_tokens"] for r in rs)
        right = sum(1 for r in rs if r["right"])
        print(f"    {effort:8s} {vis:7.0f} {rea:10.0f}"
              f" {lo:6.0f}-{hi:<6.0f} {100 * share:4.0f}%"
              f"  {right} of {len(rs)}")

    print("\n  AND THE BILL, per 1,000 requests")
    print("    effort       $/1,000   x minimal")
    base = st.mean(bill(r) for r in runs if r["effort"] == "minimal")
    for effort in EFFORTS:
        rs = [r for r in runs if r["effort"] == effort]
        m = st.mean(bill(r) for r in rs) * 1000
        print(f"    {effort:8s} {m:12.4f} {m / (base * 1000):10.1f}")


if __name__ == "__main__":
    runs = []
    for trial in range(1, TRIALS + 1):
        for qid, prompt, answer in QUESTIONS:
            for effort in EFFORTS:          # interleaved: chapter 49
                r = call(prompt, effort)
                got = first_number(r["text"])
                r.update(question=qid, trial=trial, effort=effort,
                         right=got is not None
                         and abs(got - answer) < 0.005)
                runs.append(r)
                print(f"    {trial} {qid:5s} {effort:7s}"
                      f" out {r['out_tokens']:4d}"
                      f" reasoning {r['reasoning']:4d}"
                      f" {'right' if r['right'] else 'WRONG'}",
                      file=sys.stderr)

    summarise(runs, MODEL)

    #  Chapter 20's test: the interval goes round the DIFFERENCE, on
    #  the same questions, not round each arm.
    by = {}
    for r in runs:
        by.setdefault((r["question"], r["trial"]), {})[r["effort"]] = r
    units = [v for v in by.values() if len(v) == len(EFFORTS)]
    print(f"\n  PAIRED DIFFERENCE IN COST, {len(units)} units")
    print("    3 questions x 3 trials, $ per 1,000 requests")
    for a, b in [("minimal", "low"), ("low", "medium"),
                 ("medium", "high"), ("minimal", "high")]:
        def gap(sample, a=a, b=b):
            return (st.mean(bill(u[b]) for u in sample)
                    - st.mean(bill(u[a]) for u in sample)) * 1000
        d = gap(units)
        lo, hi = boot(gap, units)
        tell = "cannot tell" if lo <= 0 <= hi else "clears zero"
        print(f"    {a:8s} -> {b:7s} {d:+8.4f}"
              f" {lo:+.4f} to {hi:+.4f} {tell}")

    #  The failure that only a reasoning mode has: the cap can be
    #  spent entirely on tokens you never see.
    print("\n  WHAT A CAP BELOW THE WORKING BUYS")
    short = call(QUESTIONS[0][1], "high", cap=256)
    print(f"    reply            {short['text']!r}")
    print(f"    output tokens    {short['out_tokens']}")
    print(f"    of them working  {short['reasoning']}")
    print(f"    finished because {short['finish']}")
    print(f"    and it cost      ${bill(short) * 1000:.4f} per 1,000")

    #  And whether a 36-call measurement reproduced. Chapter 49 kept
    #  its first timing run on disk for the same reason.
    earlier = pathlib.Path("reason-run1.json")
    if earlier.exists():
        print("\n  THE SAME 36 CALLS, AN EARLIER RUN")
        summarise(json.load(open(earlier)), "run 1")

    total = sum(bill(r) for r in runs) + bill(short)
    print(f"\n  THIS PROGRAM'S OWN BILL: {len(runs) + 1} calls,"
          f" ${total:.4f}")
    json.dump(runs, open("reason.json", "w"), indent=1)
```

```text

  36 calls, gpt-5-mini-2025-08-07
  ONE MODEL, ONE QUESTION AT A TIME, FOUR SETTINGS
    effort   visible  reasoning       range   invis  right
    minimal       10          0      0-0         0%  1 of 9
    low           10         64      0-128      87%  9 of 9
    medium        10         64     64-192      91%  9 of 9
    high          10        128     64-704      96%  9 of 9

  AND THE BILL, per 1,000 requests
    effort       $/1,000   x minimal
    minimal        0.0325        1.0
    low            0.1747        5.4
    medium         0.2601        8.0
    high           0.5163       15.9

  PAIRED DIFFERENCE IN COST, 9 units
    3 questions x 3 trials, $ per 1,000 requests
    minimal  -> low      +0.1422 +0.0853 to +0.1991 clears zero
    low      -> medium   +0.0853 +0.0427 to +0.1280 clears zero
    medium   -> high     +0.2562 +0.0711 to +0.4982 clears zero
    minimal  -> high     +0.4838 +0.2418 to +0.7829 clears zero

  WHAT A CAP BELOW THE WORKING BUYS
    reply            ''
    output tokens    256
    of them working  256
    finished because length
    and it cost      $0.5255 per 1,000

  THE SAME 36 CALLS, AN EARLIER RUN

  36 calls, run 1
  ONE MODEL, ONE QUESTION AT A TIME, FOUR SETTINGS
    effort   visible  reasoning       range   invis  right
    minimal       10          0      0-0         0%  1 of 9
    low           10         64      0-192      88%  9 of 9
    medium        10        128     64-192      91%  9 of 9
    high          10        128     64-384      94%  9 of 9

  AND THE BILL, per 1,000 requests
    effort       $/1,000   x minimal
    minimal        0.0325        1.0
    low            0.1889        5.8
    medium         0.2601        8.0
    high           0.3881       11.9

  THIS PROGRAM'S OWN BILL: 37 calls, $0.0094
```

**The first column is the whole finding and it is a column of one number.** The visible reply is
**10 to 13 tokens in all 72 calls across both runs** — it is a price or a count, because that is
what the questions asked for — and it is 10 to 13 at every setting. The billed output over the
same 72 calls runs from 10 to 717. **Everything the money bought is invisible**, and at the
dearest setting 96 per cent of the output tokens are tokens nobody will ever read.

The bill follows the counts, as it must:

| Setting | Reasoning tokens, median | Share of output | Cost, against the cheapest setting |
|---|---|---|---|
| Minimal | 0 | 0 per cent | 1.0 |
| Low | 64 | 87 per cent | 5.4 |
| Medium | 64 | 91 per cent | 8.0 |
| High | 128 | 96 per cent | 15.9 |

**And for once in this part of the book, a difference clears zero.** Chapter 52 compared three
prompt shapes' first-token waits and could not separate any pair of them from zero on two dozen
requests. Here all
four paired differences clear it: the step from the cheapest setting to the dearest is +$0.4838
per thousand requests with 95 per cent from +0.2418 to +0.7829, on nine paired units — three
questions, three trials, every unit having run at all four settings. The reason is not a better
measurement. It is that a token count barely varies where a wait varies enormously, which is the
same fact *Cost Per Request Is a Product Constraint* turns into a budget.

**The multiplier is roughly five to sixteen, and the dearest setting is the least predictable of
the four.** The earlier run printed below the current one puts the same four settings at 1.0,
5.8, 8.0 and 11.9 against the current 1.0, 5.4, 8.0 and 15.9. The two agree *exactly* on the
cheapest and the middle settings and differ by a third at the dearest, and their ranges say why:
the dearest setting's reasoning spend runs 64 to 384 tokens on one run and 64 to 704 on the
other, while the medium setting runs 64 to 192 on both. **A setting is a budget hint rather than
a token count**, and what it produces depends mostly on the question and partly on the day. The
dearest setting spent 256, 512 and 704 reasoning tokens on three trials of the shop arithmetic
and 64, 128 and 64 on three trials of the tank.

### What the Counts Do Not Say

Two refusals, and both matter more than the figures.

**This is not evidence that a reasoning mode improves answers.** It looks like evidence: the
cheapest setting got 2 of 18 right across both runs and every other setting got 54 of 54. But
three questions chosen because they need arithmetic are not a sample of anything, Chapter 16
already owns why working step by step helps, and a grader that checks the first number in a reply
is a rule in exactly Chapter 31's sense — it gives the same verdict every time, which is not the
same as being right. **What the counts establish is that the setting is neither free nor
cosmetic**, which is the only thing a cost chapter needs from them.

**And they are not a figure to carry to another model.** The prices here are one reasoning model's
on one day; the multiplier is within that model and says nothing about the gap between a reasoning
model and a plain one. Chapter 49's baseline was measured on a different model entirely, so
**nothing in this chapter multiplies that baseline by these factors** — the two numbers cannot be
composed, and the temptation to compose them is the shape of a defect this book has paid for
before.

### The Failure That Only a Reasoning Mode Has

The last block of that output is the one to remember, because it is a way to pay full price for
nothing. A plain model truncated by its cap costs full price too — Chapter 19 and Chapter 13 both
treat that case — and the difference is that its reply holds the part it got through, which you
can read, judge or salvage. Here there is nothing to read.

Asked the same question at the dearest setting with the output cap set to 256 tokens, the call
came back with **an empty reply, 256 output tokens, all 256 of them working, and a finish reason
of `length`.** The same setting's median answered call spends 128 tokens of working, so this one
spent twice that and produced nothing. In money it cost $0.5255 per thousand requests, which is a
little more than that setting's own average on this run and a third more than on the earlier one
— **the comparison moves between runs and the fact that the money bought nothing does not.** The
cap was spent entirely on tokens the provider does not return, and the model never reached the
part that would have been sent.

**So a token cap on a reasoning model is not the safety net it is on a plain one.** Chapter 19
derives a cap from what a reply may cost and a timeout from the cap; Chapter 13 owns the stop
conditions. All of that still holds, and this adds one rule to it: **a cap below the working buys
nothing at full price**, and the way it shows up in your logs is an empty string and a finish
reason, not an error. Alarm on that finish reason, which Chapter 19 says to do for the ordinary
case and which here is the difference between a bill you can explain and one you cannot.

## Where the Money Went

Chapter 49 made 288 calls and published what the 216 of them it could price cost — the other 72
were streamed, and a streamed reply carries no usage block, which is that chapter's own first
lesson about this and this chapter's too. Its records are still on disk, which
makes them the right thing to practise attribution on: the bill is known, so a split of it can
be checked rather than believed. The 144 requests of its prompt-ordering run carry the
provider's own token counts; its 36 routed rows carry dollars, verdicts and
answers, and no token counts and no model name — which is why the cascade arithmetic below is in
dollars and everything above it is in tokens. That asymmetry
is itself the section's lesson arriving early — a record you did not keep is a question you
cannot ask.

```python
"""Where the money went, and what a cap on it allows.

    python3 where.py

No model is called. Two of chapter 49's files are still on disk.
`order.json` holds 144 requests, each with the provider's own token
counts - input, cached and output - and the dollars that chapter
computed from them. `route.json` holds 36 routed rows - three trials of
twelve cases - each with what
its cheap call, its dear call and the cascade cost, and no token
counts and no model name at all - so the cascade section below is in
dollars, those dollars are chapter 49's own rather than recomputed
here, and everything above it is in tokens. Chapter 49 owns what the
runs mean.
What this program does with them belongs here: turn a token count into
a bill, find out which half of the bill is which half of the traffic,
and price a cascade against the rate it actually escalated at.

Prices per million tokens, read on 30 October 2026 and written down
rather than fetched, so every figure recomputes when they change.
"""
import json
import pathlib
import statistics as st

CH49 = pathlib.Path.home() / "sandbox" / "ch49"
CAP = 0.25          # dollars per 1,000 requests: a cap, written down
PRICE = {"gpt-4o-mini-2024-07-18": {"in": 0.150, "cached": 0.075, "out": 0.600},
         "gpt-4o-2024-08-06": {"in": 2.500, "cached": 1.250, "out": 10.000}}


def rows(name):
    p = CH49 / name
    return json.load(open(p)) if p.exists() else []


def bill(in_tokens, cached, out_tokens, model):
    """The whole arithmetic of a bill, in one place.

    Cached tokens are a DISCOUNT on tokens you still sent, so they are
    subtracted from the fresh count and charged again at their own
    rate - never dropped. Reasoning tokens need no term of their own:
    the provider counts them inside the output figure, which is why
    this function cannot see them and the other program in this
    chapter has to ask for them by name.
    """
    p = PRICE[model]
    fresh = in_tokens - cached
    return ((fresh * p["in"] + cached * p["cached"] + out_tokens * p["out"])
            / 1_000_000)


def per_1k(money, n):
    return money / n * 1000


if __name__ == "__main__":
    order, route = rows("order.json"), rows("route.json")
    if not order or not route:
        raise SystemExit("  chapter 49's runs are not here; nothing to read")

    #  1. The formula against the figures chapter 49 published from the
    #     same rows. If the two do not agree there is no point reading
    #     on, so this is the first thing printed.
    print("  THE PRICE LIST, read on 30 October 2026, per million")
    for name in sorted(PRICE):
        p = PRICE[name]
        print(f"    {name}")
        print(f"      ${p['in']:.3f} in, ${p['cached']:.3f} cached,"
              f" ${p['out']:.3f} out")

    mine = sum(bill(r["in_tokens"], r["cached_tokens"], r["out_tokens"],
                    r["model"]) for r in order)
    theirs = sum(r["dollars"] for r in order)
    print("\n  THE FORMULA, CHECKED AGAINST CHAPTER 49'S OWN FIGURE")
    print("    (in - cached) x p_in + cached x p_cached + out x p_out")
    print(f"    this program  ${mine:.7f}")
    print(f"    chapter 49    ${theirs:.7f}")
    print(f"    agree to 1e-9 {abs(mine - theirs) < 1e-9}")

    #  2. Which half of the traffic is which half of the bill. The
    #     token share and the money share are different numbers and the
    #     gap is the price ratio.
    print("\n  TOKENS ARE NOT MONEY, by prompt shape and prompt order")
    print("    shape      order            in      out  out% of  out% of")
    print("                                                tokens    money")
    groups = sorted({(r["shape"], r["order"]) for r in order})
    for shape, order_name in groups:
        rs = [r for r in order if (r["shape"], r["order"]) == (shape, order_name)]
        ti = sum(r["in_tokens"] for r in rs)
        to = sum(r["out_tokens"] for r in rs)
        mi = sum(bill(r["in_tokens"], r["cached_tokens"], 0, r["model"])
                 for r in rs)
        mo = sum(bill(0, 0, r["out_tokens"], r["model"]) for r in rs)
        print(f"    {shape:9s}  {order_name:14s} {ti:6d} {to:7d} "
              f"{100 * to / (ti + to):7.1f}% {100 * mo / (mi + mo):7.1f}%")
    ti = sum(r["in_tokens"] for r in order)
    to = sum(r["out_tokens"] for r in order)
    mi = sum(bill(r["in_tokens"], r["cached_tokens"], 0, r["model"])
             for r in order)
    mo = sum(bill(0, 0, r["out_tokens"], r["model"]) for r in order)
    print(f"    {'ALL 144':9s}  {'':14s} {ti:6d} {to:7d} "
          f"{100 * to / (ti + to):7.1f}% {100 * mo / (mi + mo):7.1f}%")

    #  3. The grouping decides the number. These two arms sent the
    #     identical input tokens, so nothing about a token count can
    #     explain the gap - and the gap itself depends on which
    #     requests you pool, which is chapter 49's own trap.
    print("\n  THE SAME TOKENS, A DIFFERENT BILL - AND WHICH BILL")
    print("    upfront shape, 8 questions, 3 trials each")
    print("    pooled over      order              in  cached   $/1,000")
    paid = {}
    for which, keep in (("trial 1 only", lambda r: r["trial"] == 1),
                        ("all 3 trials", lambda r: True)):
        for order_name in ("question-first", "stable-first"):
            rs = [r for r in order if r["shape"] == "upfront"
                  and r["order"] == order_name and keep(r)]
            ti = sum(r["in_tokens"] for r in rs)
            tc = sum(r["cached_tokens"] for r in rs)
            m = per_1k(sum(bill(r["in_tokens"], r["cached_tokens"],
                                r["out_tokens"], r["model"]) for r in rs),
                       len(rs))
            paid[(which, order_name)] = m
            print(f"    {which:15s}  {order_name:14s} {ti:6d}  {100 * tc / ti:4.0f}%"
                  f"   ${m:.4f}")
    first = (paid[("trial 1 only", "question-first")]
             - paid[("trial 1 only", "stable-first")])
    pooled = (paid[("all 3 trials", "question-first")]
              - paid[("all 3 trials", "stable-first")])
    print(f"    the ordering lever, first outing   ${first:.4f} per 1,000")
    print(f"    the same lever, pooled             ${pooled:.4f} per 1,000")
    print(f"    the pool understates it by         {first / pooled:.1f} times")
    print("    because trials 2 and 3 of the question-first arm are")
    print("    the SAME question again, served from the same cache -")
    print("    which is the factor of 2.8 chapter 49 warns about, and")
    print("    its 66 per cent pooled cache figure is the row above.")

    #  4. What the provider's own breakdown would have shown for all of
    #     it, which is the reason every number above had to be recorded
    #     by the program that made the calls.
    models = sorted({r["model"] for r in order})
    print(f"\n  A BREAKDOWN BY MODEL: {len(order)} calls,"
          f" {len(models)} row")
    print(f"    {models[0]}   ${theirs:.4f}")
    print("    every split above came from the records, not the bill")

    #  5. A cascade priced against the rate it escalated at. Chapter 49
    #     owns the term, the 12-of-12 verdicts and the reason the rule
    #     fired; what belongs here is the break-even.
    n = len(route)
    esc = [r for r in route if r["escalated"]]
    rate = len(esc) / n
    cheap = per_1k(sum(r["cheap_dollars"] for r in route), n)
    dear = per_1k(sum(r["capable_dollars"] for r in route), n)
    casc = per_1k(sum(r["cascade_dollars"] for r in route), n)
    dear_esc = per_1k(sum(r["capable_dollars"] for r in esc), len(esc))
    print("\n  A CASCADE'S BREAK-EVEN, per 1,000 requests")
    print(f"    cheap alone                      ${cheap:.4f}")
    print(f"    dear alone                       ${dear:.4f}")
    print(f"    the cascade, as it ran           ${casc:.4f}")
    print(f"    escalated                        {len(esc)} of {n} rows"
          f"  = {100 * rate:.0f}%")
    print(f"    cheap + rate x dear ON AVERAGE   ${cheap + rate * dear:.4f}")
    print(f"    cheap + rate x dear WHERE IT     ${cheap + rate * dear_esc:.4f}")
    print(f"      ESCALATED (${dear_esc:.4f} per 1,000)")
    print(f"    break-even rate = 1 - cheap/dear  {1 - cheap / dear:.2f}")
    print("    so the money said yes at any rate under that, and")
    print("    chapter 49's twelve cases said the dear model answered")
    print("    nothing the cheap one had not. The cheap condition to")
    print("    check is the money; the dear one is the quality.")

    #  6. And the point of all of it: a cap, turned into a cap on the
    #     one thing the design controls. Chapter 52 does this with a
    #     latency target; the arithmetic is the same shape.
    #  6a. What a four-times-longer prompt costs, which is the long
    #      context on this chapter's list of multipliers.
    def in_per_1k(shape, order_name, keep=lambda r: True):
        rs = [r for r in order if r["shape"] == shape
              and r["order"] == order_name and keep(r)]
        return per_1k(sum(bill(r["in_tokens"], r["cached_tokens"], 0,
                               r["model"]) for r in rs), len(rs))

    short_in = in_per_1k("grounded", "stable-first")
    long_cold = in_per_1k("upfront", "question-first",
                          lambda r: r["trial"] == 1)
    long_warm = in_per_1k("upfront", "stable-first")
    print("\n  WHAT A FOUR-TIMES-LONGER PROMPT COSTS")
    print("    input only, dollars per 1,000 requests")
    print(f"    612 tokens                      ${short_in:.4f}")
    print(f"    2,458 tokens, nothing cached    ${long_cold:.4f}"
          f"   x{long_cold / short_in:.2f}")
    print(f"    2,458 tokens, 99% cached        ${long_warm:.4f}"
          f"   x{long_warm / short_in:.2f}")
    print("    4 times the prompt is 4 times the input bill when")
    print("    nothing caches and 2 times when everything does.")

    print(f"\n  WHAT A ${CAP:.2f} PER 1,000 CAP ALLOWS")
    print("    shape     order          $ in  allows  sends    over")
    for shape, order_name, keep in (
            ("grounded", "stable-first", lambda r: True),
            ("essay", "stable-first", lambda r: True),
            ("upfront", "stable-first", lambda r: True),
            ("upfront", "question-1st", lambda r: r["trial"] == 1)):
        want = "question-first" if order_name == "question-1st" else order_name
        rs = [r for r in order if r["shape"] == shape
              and r["order"] == want and keep(r)]
        n = len(rs)
        in_k = per_1k(sum(bill(r["in_tokens"], r["cached_tokens"], 0,
                               r["model"]) for r in rs), n)
        left = max(0.0, CAP - in_k)
        allows = left / 1000 / (PRICE[rs[0]["model"]]["out"] / 1_000_000)
        out = [r["out_tokens"] for r in rs]
        over = sum(1 for v in out if v > allows)
        print(f"    {shape:9s} {order_name:13s} {in_k:5.3f} {allows:7.0f}"
              f" {st.median(out):6.0f} {over:4d}/{n}")
    print("    The last row is the first outing only, which is the")
    print("    arrangement chapter 49 priced at 3.4 times the")
    print("    baseline. `sends` is the median reply; `over` counts")
    print("    the requests whose OWN reply exceeds the allowance.")
    for shape in ("grounded", "essay", "upfront"):
        v = [r["in_tokens"] for r in order if r["shape"] == shape]
        print(f"    {shape:9s} input {min(v)} to {max(v)} tokens a request")
    print("    - so unlike chapter 52's latency budget, which rested")
    print("    on one request of twenty-four, this arithmetic barely")
    print("    moves from request to request.")
```

```text
  THE PRICE LIST, read on 30 October 2026, per million
    gpt-4o-2024-08-06
      $2.500 in, $1.250 cached, $10.000 out
    gpt-4o-mini-2024-07-18
      $0.150 in, $0.075 cached, $0.600 out

  THE FORMULA, CHECKED AGAINST CHAPTER 49'S OWN FIGURE
    (in - cached) x p_in + cached x p_cached + out x p_out
    this program  $0.0313899
    chapter 49    $0.0313899
    agree to 1e-9 True

  TOKENS ARE NOT MONEY, by prompt shape and prompt order
    shape      order            in      out  out% of  out% of
                                                tokens    money
    essay      question-first  15294    8287    35.1%    68.4%
    essay      stable-first    15297    8210    34.9%    68.2%
    grounded   question-first  14694     948     6.1%    20.5%
    grounded   stable-first    14697     912     5.8%    19.9%
    upfront    question-first  58980     931     1.6%     8.6%
    upfront    stable-first    58980     703     1.2%     8.6%
    ALL 144                   177942   19991    10.1%    38.2%

  THE SAME TOKENS, A DIFFERENT BILL - AND WHICH BILL
    upfront shape, 8 questions, 3 trials each
    pooled over      order              in  cached   $/1,000
    trial 1 only     question-first  19660     0%   $0.3911
    trial 1 only     stable-first    19660    99%   $0.2039
    all 3 trials     question-first  58980    66%   $0.2703
    all 3 trials     stable-first    58980    99%   $0.2038
    the ordering lever, first outing   $0.1872 per 1,000
    the same lever, pooled             $0.0665 per 1,000
    the pool understates it by         2.8 times
    because trials 2 and 3 of the question-first arm are
    the SAME question again, served from the same cache -
    which is the factor of 2.8 chapter 49 warns about, and
    its 66 per cent pooled cache figure is the row above.

  A BREAKDOWN BY MODEL: 144 calls, 1 row
    gpt-4o-mini-2024-07-18   $0.0314
    every split above came from the records, not the bill

  A CASCADE'S BREAK-EVEN, per 1,000 requests
    cheap alone                      $0.1066
    dear alone                       $1.7758
    the cascade, as it ran           $0.5764
    escalated                        9 of 36 rows  = 25%
    cheap + rate x dear ON AVERAGE   $0.5506
    cheap + rate x dear WHERE IT     $0.5764
      ESCALATED ($1.8792 per 1,000)
    break-even rate = 1 - cheap/dear  0.94
    so the money said yes at any rate under that, and
    chapter 49's twelve cases said the dear model answered
    nothing the cheap one had not. The cheap condition to
    check is the money; the dear one is the quality.

  WHAT A FOUR-TIMES-LONGER PROMPT COSTS
    input only, dollars per 1,000 requests
    612 tokens                      $0.0919
    2,458 tokens, nothing cached    $0.3686   x4.01
    2,458 tokens, 99% cached        $0.1862   x2.03
    4 times the prompt is 4 times the input bill when
    nothing caches and 2 times when everything does.

  WHAT A $0.25 PER 1,000 CAP ALLOWS
    shape     order          $ in  allows  sends    over
    grounded  stable-first  0.092     264     35    0/24
    essay     stable-first  0.096     257    348   22/24
    upfront   stable-first  0.186     106     28    0/24
    upfront   question-1st  0.369       0     34    8/8
    The last row is the first outing only, which is the
    arrangement chapter 49 priced at 3.4 times the
    baseline. `sends` is the median reply; `over` counts
    the requests whose OWN reply exceeds the allowance.
    grounded  input 573 to 646 tokens a request
    essay     input 598 to 671 tokens a request
    upfront   input 2455 to 2460 tokens a request
    - so unlike chapter 52's latency budget, which rested
    on one request of twenty-four, this arithmetic barely
    moves from request to request.
```

**The first block is the formula agreeing with Chapter 49 to the ninth decimal place**, which is
the only reason to trust anything below it. That chapter computed its dollars inside the program
that made the calls; this one recomputes them from the stored counts and the same dated price
list, and the two agree at $0.0313899 across 144 requests. A reconciliation like that costs four
lines and is what separates an attribution from an estimate.

**Then the number this chapter exists for.** Across all 144 requests, output is **10.1 per cent
of the tokens and 38.2 per cent of the money.** Those are two different facts about the same
traffic, and a team that has been looking at token counts has been looking at the first one. The
gap is the price ratio, moved by whatever came back cached: output costs four times a fresh
input token here and eight times a cached one, so every output token carries that much more
weight into the total than its share of the count suggests.

And the per-shape rows say that the gap is not a constant you can carry:

| Prompt shape | Output's share of the tokens | Of the money |
|---|---|---|
| Essay | 35 per cent | 68 per cent |
| Grounded | 6 per cent | 20 per cent |
| Up-front | 1 to 2 per cent | 9 per cent |

**So "which half dominates" has a different answer for every design in the same system.** On the
essay shape — the same retrieval asked for a long answer, with its output cap at 700 tokens
against the other two shapes' 120 — more than two-thirds of the money is the reply, and halving
the whole input half of it would save less than a sixth of the bill. On the up-front shape, which sends a long document with every request,
ninety-one per cent of the money is input and shortening the reply is nearly pointless. Chapter
52's lever menu asks which wait you are trying to move; the cost question is the same shape, and
this is the number that answers it. Chapter 40 called noticing it a habit worth starting early.

## The Grouping Decides the Number

The third block is the one to be uncomfortable about, and it is the chapter's method lesson.

Two arms of Chapter 49's up-front shape sent **the identical 58,980 input tokens** — the same
eight questions, the same document, three trials each — and were billed $0.2703 and $0.2038 per
thousand requests. No token count can explain a gap like that, which is the plainest possible
demonstration that a count is not a bill. The difference is cached tokens, and the formula is
where it shows up.

**But look at what the gap is worth, and then at which requests were pooled to get it.** On the
first trial alone, the question-first arm cached nothing and the stable-first arm cached 99 per
cent, and the ordering lever is worth $0.1872 per thousand requests — which is Chapter 49's own
$0.19, recomputed from the same rows rather than measured again here. Pooled over all three
trials it is worth $0.0665 — **2.8 times smaller, for the same lever on the same traffic.** The
reason is that trials two and three of the question-first arm are the same eight questions asked
again, and a repeated request is served from the same cache whatever order its blocks are in. So
the pooled figure is measuring the lever against an arm that is quietly getting the benefit by
another route.

That 2.8 is not a coincidence and not this chapter's discovery: it is the factor Chapter 49 warns
about in its own Worth Memorising table, and the 66 per cent pooled cache figure in the output
above is the exact figure that chapter put on its record as a mistake it nearly shipped. **Which
makes the general rule the thing to carry.** An attribution is a grouping, and a grouping is an
arm design — so everything Chapter 20 says about comparisons applies to a bill. If you group a
bill by a lever, the requests inside each group have to differ in that lever and in nothing
else, and here they differed in whether they were the first outing of a question.

**And a bill grouped the wrong way does not look wrong.** It looks like a number, it is
arithmetically correct to the last digit, and it understates a lever by a factor of three while
giving no sign that anything is amiss. That is the cost version of a problem Chapter 49 met
twice and put on its own record both times, and it is the reason the next section is about
records rather than about arithmetic.

## What the Provider Cannot Tell You, and What to Record

The fourth block is three lines long and it is the argument for the whole method. All 144 of
those requests went to one model on one key, and a provider's console groups a bill by model, day
and key — so its breakdown of this traffic is **one row with one number on it**. Every split in this section —
by shape, by order, by half of the bill, by trial — came out of records the program kept while it
was making the calls. None of it could have been recovered afterwards.

A key per feature would have given none of it, which is the limit of the cheap route from the
first section: these 144 requests are one feature of one system, and every split that mattered is
*inside* it. So record the usage block with every request, and label it. Chapter 33 owns the
trace and this is one more thing on it rather than a second system:

| Record | Why |
|---|---|
| Input tokens, cached input tokens, output tokens | The three terms of the formula |
| Reasoning tokens | Billed inside the output count, and the next section is why that matters |
| The model, with its version | Prices differ by model, and Chapter 54 owns why the short name is not a version |
| What the request was *for* | The feature, the customer, the pipeline stage. This is the field that makes a grouping possible, and nothing else on the list can be derived into it |
| The prompt shape or design, if you run more than one | The per-shape rows above exist only because Chapter 49 recorded this |
| The sequence number and the wall-clock time | Chapter 52 asked for these for latency; a bill wants them for the same reason |

**The fourth row is the one that gets left out**, because it is the only one that is not already
in the response. The provider tells you the counts; nobody but you knows that this call was the
reranking step for a free-tier user. A team that records the counts and not the label has a very
precise measurement of a bill it still cannot account for.

**A spending cap is not an attribution, and you want both.** Chapter 51 noted in passing that a
provider key in the wrong hands shows up as somebody else's traffic on your bill, and that a key
scoped to one project with a cap reaches much less than an organisation-wide one. The cap is
what stops the damage; the records are what tell you it happened and to which project. Both are
account settings somebody has to go and change, and neither of them costs anything.

## Features That Multiply Usage

The settings and designs that cost real money are not increments. They are multipliers, and
each one is a line somebody can add in an afternoon. This book has measured several of them, in
chapters that were about something else at the time, and putting the figures in one place is the
most useful page in this chapter for a design review.

| The decision | What it multiplies the usage by | Measured in |
|---|---|---|
| A reasoning mode, at the dearest setting | 11.9 and 15.9 times the same model's cheapest setting, on two runs | This chapter, 3 questions |
| Six agents duplicating the work | 6.03 times one agent | Chapter 37 |
| Six agents dividing the work, running to a step limit | 4.56 times at ten steps, 13.79 at twenty | Chapter 37 |
| Doubling one loop's step limit | 3.4 times the tokens, from ten steps to twenty | Chapter 34 |
| Reranking the candidates | About thirteen extra model calls a request | Chapter 45, at 105 calls for 8 queries |
| Quadrupling the prompt | 4.0 times the input bill cold, 2.0 with the prefix cache full | `where.py` above, on Chapter 49's shapes |

**Read the second and third rows together, because they are the ones that are usually got
backwards.** Chapter 37's finding is that several agents are not expensive for being several:
six that genuinely divide the work cost 0.61 of one agent, because the re-send cost falls with
the length of each run. What costs is *duplication* — six agents each doing the whole task — and
non-termination, which is six stopping conditions where there was one. So "we are adding agents"
is not a cost claim in either direction until somebody says whether the work is divided and what
stops each one.

**The last row is the long context, and it is the one multiplier that halves.** `where.py` prices
Chapter 49's two prompt lengths side by side: 612 input tokens cost $0.0919 per
thousand requests and 2,458 cost $0.3686 — four times the prompt for four times the input bill,
exactly proportional, because nothing about input pricing is non-linear. With the prefix cache
full it is $0.1862, or twice rather than four times. **So a long prompt is the only multiplier
here with a lever against it that costs nothing**, which is why Chapter 52 puts prompt ordering on
its menu and why *The Economics of Caching and Cascades*, two sections below, prices what that
ordering is really worth.

**And the step-limit row is why a step limit is a cost decision.** Chapter 34's arithmetic has a
square in it, because a loop re-sends its whole record every step: ten steps to twenty doubles
the calls and multiplies the tokens by 3.4, and twenty to forty by 3.7. A limit set to thirty
out of caution is not thirty-tenths of a limit set to ten.

**Then the part this chapter owes all three of those chapters.** Each of them counted *tokens*
and said in so many words that a count is not a bill, and handed the conversion here. The
conversion is the formula from the second section, and the term that breaks the ranking is the
cached one. Chapter 37's Note works it through for its own two designs: one agent's twelve calls
share one growing prefix, so much of what it re-sends comes back as a cache hit, while six
agents have six separate prefixes each reused across two calls. **So the token count can say
dividing is cheaper while the bill says otherwise**, and which it says is a measurement of the
cached fraction per design rather than anything you can derive. The figure that survives any
caching arrangement is the duplication one, because six agents each doing the whole task is six
of everything.

The fifth row is the one this book cannot finish, and that is the lesson. Chapter 44 established
that at a candidate depth of fifteen its set already held 98 per cent of the graded material, so
five more candidates were worth more than any reranker, and said the per-call arithmetic belonged
here. Here is as much of it as the records allow: the reranker is about thirteen extra model
calls a request and deepening the candidate set is [**none**]{.noindex}, because it is one more
retrieval and no model pass. What it is in money, nobody can now say. Chapter 45 recorded the token counts of
the answer call and not of the 105 scoring calls, so the one design decision this book priced in
calls cannot be priced in money after the fact — **which is the previous section's rule arriving
as a bill of its own.**

## Budget Them Rather Than Switching Them On

Every multiplier above shares a shape: it is off, somebody turns it on, and the bill moves by a
factor rather than by a margin. The practice that follows is short.

**Price the multiplier on your own traffic before you turn it on, at the cap you already hold.**
Chapter 52's first rule for a latency lever was to find out whether it can fire at all, and the
cost version is cheaper still, because a multiplier does not need a measurement to be bounded —
a reasoning mode's output cannot exceed the cap you set, several agents cannot exceed their
number times a run, and a loop cannot exceed its step limit. **The worst case is arithmetic, and
it is the number to take to the conversation**, because the typical case is what everybody
quotes and the limit is what you will be billed for on the day something goes wrong.

**Then decide what you will turn off to pay for it.** That sounds like a budgeting cliché and it
is a technical instruction: the multipliers compose. A reasoning mode inside an agent loop inside
a design that runs several agents multiplies three times, and each of the three was signed off
by somebody who was looking at one of them. The only place that composition is visible is a cost
per request with a cap on it, which is *Cost Per Request Is a Product Constraint*, two sections
below.

**And put the cap in the code rather than in the document.** Chapter 4 owns the step limit,
Chapter 19 the token cap and the timeout, and Chapter 13 the stop conditions; every one of them
is also a spending control, and the difference between a budget and an intention is whether
something refuses when it is exceeded.

## The Economics of Caching and Cascades

Four levers have an economics worth doing on paper before anybody builds them, because in each
case the arithmetic decides it and the arithmetic is small.

**A prompt-prefix cache is a discount on the input half, and its ceiling is the gap between the
two input rates.**
Chapter 49 owns the term and the minimum length; what belongs here is the size of the prize. The
discount is the cached count times the difference between the two input rates, and **how big
that difference is, is a price-list fact rather than a property of caching**: it is half the
input rate on the small model Chapter 49 used and nine tenths of it on the reasoning model
earlier in this chapter. So a request whose entire input comes back cached pays half as much for
it on the first and a tenth on the second, and exactly as much for its reply on both — the two
numbers are the same fact read from either end, and *nine tenths off* and *a tenth of the price*
are easy to write for each other. Worked on Chapter 49's own up-front shape, where 19,456 of
19,660 input tokens came back cached: its input bill falls from $0.3686 per thousand requests to
$0.1862, a cut of **49 per cent of the half the lever touches**. Its total falls from $0.3911 to
$0.2039, which is 48 per cent — and only 46.6 points of that 48 are the cache, because the two
arms' replies differ by 64 output tokens and that is 1.2 points of the fall. **This chapter's own
grouping rule applies to its own worked example**: decompose, rather than credit a lever with
everything that moved beside it.

**And that is the lever at nearly full strength on the design Chapter 35 priced and rejected**,
which costs 3.4 times the baseline before the lever and 1.8 times after it. A discount of that
size on a design you would not otherwise have chosen is not a saving; it is a reason to look again
at why you are sending the document.

**A response cache of your own is the only one of the four that removes a line from the bill**,
and Chapter 52 owns the term, the key and the warning about staleness. Its economics are the
simplest in this chapter: the saving is the hit rate times the whole cost, because a hit costs
nothing at all. That makes it the only lever whose value you can read off a log you already
have, by counting how many requests would have matched an earlier key — and the only one whose
value is a property of your traffic rather than of your prompts.

**A cascade's break-even is one line and it is almost always satisfied.** Run the cheap model on
everything and the dear one on the share your own code escalates, and the design pays whenever

```{=latex}
\[ c_{\text{cheap}} + e \times c_{\text{dear}} < c_{\text{dear}}
  \quad\text{that is}\quad e < 1 - \frac{c_{\text{cheap}}}{c_{\text{dear}}} \]
```

where `\(e\)`{=latex} is the **escalation rate**, the share of requests that go on to the second
call. The cascade block of `where.py` works it out over the 36 rows of Chapter 49's
twelve routed cases: the cheap model at $0.1066 per thousand against the dear one at $1.7758 puts
the break-even at an escalation rate of 0.94. Chapter 49 escalated on 9 of those 36 rows, a rate
of 0.25, and its cascade cost $0.5764 per thousand — under a third of always-dear, exactly as the
arithmetic says.

**So the money condition on a cascade is nearly free to satisfy, and it is not the condition that
matters.** With a sixteen-fold price gap, a cascade saves money at any escalation rate below
about nineteen in twenty, which no real escalation rule reaches. What sank Chapter 49's cascade
was the other condition entirely: both models answered 12 of 12 of its cases, so the second call
bought nothing, and the design paid 5.4 times the cheap model for the same answers. Chapter 52
says the order to establish it in — the dear model must be better *on the cases that escalate* —
and the economics add only that the cheap test is the one everybody does.

**One detail in that formula is worth more than the formula.** The multiplier is the dear model's
cost *on the cases that escalate*, not its average cost. The two are not the same: Chapter 49's
dear calls come to $1.8792 per thousand requests over the escalating rows against $1.7758 over
all of them, because the cases a decline-detector fires on are the ones with longer answers. Using the average puts the predicted
cascade at $0.5506 against the $0.5764 it actually cost, four and a half per cent low. **The escalating
cases are selected, so every quantity you average over them is selected too** — which is the same
sentence as Chapter 52's rule about quality, applied to the bill.

**And the fourth lever has no quality question at all.** Chapter 19 owns the batch endpoint:
upload the requests, collect the results hours later, pay substantially less. It is the only
lever in this chapter that is a pure discount — the same model, the same prompt and the same kind
of answer, since Chapter 13 is clear that an identical request can come back differently — and
what it costs is latency measured in hours rather than seconds. So it is the first thing to
ask about any workload nobody is waiting for: a nightly re-grading, an evaluation run, a backfill
of embeddings, Chapter 33's regression set. **The discount, the turnaround and even the existence
of such an endpoint are a provider's to change**, which that chapter says in its own Note, so it
is a thing to check rather than to assume.

## Cost Per Request Is a Product Constraint

A **cost per request** is a cap somebody writes down before the design exists, in the way a
latency target is. Chapter 52 took a two-second target at the 95th percentile and turned it into
a cap on the length of the reply. The cost version is the same move with easier arithmetic, and
it is the last block of `where.py`, back in *Where the Money Went*.

Take a cap of twenty-five cents per thousand requests — rather more than twice the baseline
Chapter 49 handed on, so a cap with room in it. Subtract what the input costs, which you know
before the model answers. What is left, divided by the output rate, is the longest reply the
design may produce.

| Shape | Input, per 1,000 | Reply the cap allows | Median reply | Requests over |
|---|---|---|---|---|
| Grounded | $0.092 | 264 tokens | 35 | 0 of 24 |
| Essay | $0.096 | 257 tokens | 348 | 22 of 24 |
| Up-front, stable first | $0.186 | 106 tokens | 28 | 0 of 24 |
| Up-front, question first, first outing | $0.369 | none | 34 | 8 of 8 |

**Every row reads immediately, which is the point of the exercise.** The grounded shape — the
design the system already had — sits inside the cap with room for a reply seven times as long. The
essay shape is out, and not marginally: twenty-two of its twenty-four requests produce a reply
longer than the cap allows, and the two that do not are both exactly three tokens under it. The
up-front shape with the stable block first is inside, at a reply allowance of 106 against a median
of 28, which is the one row where the cache discount is what keeps a design legal. And the same
shape with the question in front of the document has spent $0.369 of a $0.25 cap on its input
alone, before a single token of the reply exists, so the cap rules it out without reference to
what it says.

**And this is where a cost budget turns out to be a firmer instrument than a latency one.**
Chapter 52's budget table had the same shape and had to be partly withdrawn, because every
percentile in it was the twenty-third request of twenty-four and the paired difference between
any two shapes contained zero. Nothing like that happens here. The input token counts run from
573 to 646 a request on the grounded shape, 598 to 671 on the essay shape and 2,455 to 2,460 on
the up-front one — no shape's own spread is a seventh of itself, against a total-latency spread on
the same traffic of eleven times — because a token count is a property of the text and a wait is a
property of a queue. **So the cost arithmetic is near-deterministic where the latency arithmetic
was noise-dominated**, and a cost cap can be held against a design on two dozen requests in a way
a latency target cannot.

That is worth being precise about, because it is the one place in Part IV where two budgets built
the same way deserve different amounts of confidence. The reply length still varies — 254 to 409
tokens on the essay shape — so the conclusion is *this design exceeds the cap on almost every
request*, not *this design costs exactly this*. What has gone away is the variation in the
expensive input, and with it the need to argue about whether twenty-four requests were enough.

**Two more things belong on the cap before it is useful.**

**Price the worst case, not the median.** The cap above is tested against each request's own
reply, which is why the essay row says 22 of 24 rather than *over on average*. A cap that holds
on the median and fails on a third of requests is a cap somebody will have to explain, and the
arithmetic for the worst case is already in your hand: the token cap you set is the longest reply
you can be billed for, which is Chapter 19's number doing a second job.

**And write the cap where something refuses.** Chapter 51 noted that a provider key scoped to one
project with a spending cap reaches far less than an organisation-wide one; the same is true of a
key scoped per feature. A cap in a design document is a hope. A cap that is a project-level
spending limit, a token cap and a step limit is three places where the bill stops rising while
somebody works out why it was rising.

## What This Chapter Has Not Told You

Five things, deliberately.

**Why a token costs what it does.** Prefill and decode, the key–value cache, batching,
quantisation, mixture of experts, active parameters — all of it is Chapter 15's, and the one
sentence of it this chapter rests on is that you are paying a share of a shared machine. The
prices in this chapter are a consequence of that chapter's arithmetic and are not derived here.

**Negotiated and committed-use pricing.** Everything above uses a published list price. Providers
discount for volume and for commitments, and the shape of a bill under a commitment is a
different exercise: the marginal request becomes nearly free up to the commitment and the
question becomes whether you will reach it. Nothing here is wrong under such a contract, but the
levers' *relative* worth changes, and the arithmetic to redo is the formula in the second
section with your own numbers in it.

**Whether to serve the model yourself.** Chapter 52 named the four serving levers and said
plainly that it was not enough to run a stack, and the cost half is the same answer: the
break-even is utilisation, so it is a question about how much traffic you have and how steady it
is, not about the price per token. A machine you rent by the hour costs the same whether it is
busy or idle, which is the whole of the difference from everything in this chapter.

**The parts of the bill that are not tokens.** Embedding a corpus, storing and serving the
vectors, adapting a model — Chapters 24, 29 and 39 own those three decisions, and each has a price
that is not in the formula here. The one worth naming is re-embedding: Chapter 54 owns the
index migration a change of embedding model forces, and it is a cost event rather than a rate.

**And the largest line, which is people.** Every measurement in this chapter and in Chapter 49
cost somebody an afternoon, and the afternoons dominate the bills in this book by orders of
magnitude. That is not a reason to skip the measurement — an afternoon that finds a lever cannot
fire has paid for itself — but a chapter that priced a thousand requests at eleven cents and said
nothing about it would be giving a misleading account of where the money in a small system
actually goes.

## Summary and Key Terms

### Summary

A bill is a sum of per-request token counts at three prices, and the arithmetic that turns a
count into a bill is
`\(\text{cost} = (\text{in} - \text{cached}) \times p_{\text{in}} + \text{cached} \times p_{\text{cached}} + \text{out} \times p_{\text{out}}\)`{=latex}
— which Chapters 34 and 37 both counted tokens and handed over, because the cached term is what
makes a token count rank two designs one way and the bill rank them the other. Output is the dear
half: four times input on the small model here, eight times on the reasoning model, and over
Chapter 49's 144 recorded requests output is **10.1 per cent of the tokens and 38.2 per cent of
the money** — 35 and 68 per cent on its essay shape against 1 and 9 on its up-front one, so
*which half dominates* has a different answer for every design in one system. A cached token is
subtracted and charged again rather than dropped, and how large that discount is, is a
price-list fact: the discount is half the input rate on one of this chapter's two models and nine
tenths of it on the other, which is to say you pay half on the first and a tenth on the second.
**Reasoning tokens** need no term of their own, which is the problem — the provider counts them
inside the output figure, charges the output rate and does not return them. Measured within one
model on three questions at four effort settings, the visible reply is **10 to 13 tokens in all 72
calls** while the billed output runs to 717, 96 per cent of the dearest setting's output is
withheld, and the cost runs 1.0, 5.4, 8.0 and 15.9 times the cheapest setting with all four
paired differences clearing zero — the first budget in Part IV that does, because a token count
barely varies where a wait varies enormously. That is not evidence a reasoning mode improves
answers, and the multiplier does not compose with Chapter 49's baseline, which is a different
model. **A cap below the working buys nothing at full price**: at 256 tokens the reply came back
empty with all 256 billed and a finish reason of `length`, costing more than an answered call at
the same setting. **Cost attribution** is splitting a bill by something you can change, and there are two routes:
a separate key or project per feature, which costs nothing and cannot split finer than a key, and
recording the counts yourself, which answers questions nobody asked in advance and cannot be done
retrospectively. The provider's own breakdown of those 144 requests is one row with one number on
it, and every split that mattered was inside one feature — so record the three counts, the
reasoning count, the model with its version and, the row everybody omits, *what the request was
for*. And the grouping decides the number: two
arms that sent the identical 58,980 input tokens were billed $0.2703 and $0.2038 per thousand, and
the lever between them is worth $0.1872 per thousand on a first outing and $0.0665 pooled over
repeats — the factor of 2.8 Chapter 49 put on its own record, because an attribution is a
grouping and a grouping is an arm design. The features that cost money are multipliers rather
than increments — duplicated agents at 6.03 times one, agents running on to a twenty-step limit
at 13.79, one loop's limit doubled at 3.4 times the tokens, a reranker at about thirteen extra
model calls a request — they compose, and each one's worst case is arithmetic from a cap you
already hold, so price it before switching it on and put the cap where something refuses. On the
levers: a prefix cache is a discount on the input half, its ceiling is the gap between the two
input rates, and on Chapter 49's up-front shape it cut the input bill by 49 per cent and the total
by 48 — of which 46.6 points are the cache and 1.2 a 64-token difference in the replies — on the
design Chapter 35 rejected; a response cache is the only lever that removes a line, worth
exactly its hit rate; a cascade's break-even is
`\(e < 1 - c_{\text{cheap}}/c_{\text{dear}}\)`{=latex}, which at a sixteenfold price gap is an
**escalation rate** of 0.94, so the money condition is nearly free and the quality condition is
the one that sank Chapter 49's — and the multiplier is the dear model's cost *on the escalating
cases*, $1.8792 per thousand requests over those rows against $1.7758 over all of them, because
escalating cases are selected.
A batch endpoint is the one lever with no quality question at all. Finally, **cost per request**
is a product constraint in the way a latency target is: a cap of $0.25 per thousand allows 257
output tokens on the essay shape, which exceeds it on 22 of its 24 requests, and leaves the
up-front shape's question-first order with no allowance at all because its input alone is $0.369.
Unlike Chapter 52's latency budget, which rested on one request of twenty-four, no shape's input
counts here spread by a seventh of themselves — 573 to 646 tokens a request on one retrieved
shape, 598 to 671 on the other — so a cost cap can be held against a design on two dozen
requests, and a latency target cannot.

### Key Terms

| Term | Meaning |
|---|---|
| **Reasoning tokens** | Output tokens a model produced as working and the provider does not return. Counted inside the output figure and charged at the output rate, so they are the one line on a bill that cannot be reconstructed from your own logs. Measured here at up to 96 per cent of a request's output, with the visible reply unchanged at 10 to 13 tokens |
| **Cost attribution** | Splitting a bill by something you can change — a feature, a customer, a prompt shape, a pipeline stage. Either a key or project per group, so the provider's own breakdown is the split, or the per-request token counts recorded with a label at the time of the call. The second is the only one that splits inside a feature, and it cannot be done afterwards: nothing on the provider's side knows what a request was for, and your own tokeniser's count is not the one you were charged |
| **Cost per request** | What one request is allowed to cost, written down before the design exists. Subtract the input cost, divide the remainder by the output rate, and the cap becomes a cap on the length of the reply — the same move Chapter 52 makes with a latency target, on arithmetic that varies far less |
| **Escalation rate** | The share of requests a cascade passes on to the dear model. A cascade saves money whenever the rate is below `\(1 - c_{\text{cheap}}/c_{\text{dear}}\)`{=latex}, which a large price gap makes nearly certain — so it is the quality condition rather than this one that decides. The dear cost to multiply by is the one measured on the cases that escalate, which are selected |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The bill, from the counts | `\((\text{in} - \text{cached}) \times p_{\text{in}} + \text{cached} \times p_{\text{cached}} + \text{out} \times p_{\text{out}}\)`{=latex} — and reasoning tokens are already inside `out` |
| Output is the dear half | 4x input on this book's small model, 8x on its reasoning model. Over 144 recorded requests, output is **10.1% of the tokens and 38.2% of the money**; on the essay shape, 35% and 68% |
| What a reasoning mode costs | 1.0, 5.4, 8.0, 15.9 times the cheapest setting, with the visible reply 10 to 13 tokens at every one and 96% of the dearest setting's output withheld. Two runs agree exactly on the cheapest and middle settings and differ by a third at the dearest |
| A cap below the working | Empty reply, finish reason `length`, the whole cap billed: 256 output tokens where the same setting's median answered call spends 128 of working |
| A cascade's break-even | `\(e < 1 - c_{\text{cheap}}/c_{\text{dear}}\)`{=latex} — 0.94 at a sixteenfold gap, so the money condition is nearly free. Multiply by the dear model's cost **where it escalated**: $1.8792 per 1,000 over those rows against $1.7758 over all of them, a 4.5% difference in the predicted cascade |
| The multipliers | Duplicated agents 6.03x; agents running to a 20-step limit 13.79x; one loop's limit from 10 to 20, 3.4x the tokens; a reranker about 13 model calls a request |
| The grouping decides the number | The same lever on the same traffic: $0.1872 per 1,000 on a first outing, $0.0665 pooled over three trials of the same questions — Chapter 49's factor of 2.8 |
| A cost cap, worked | $0.25 per 1,000 allows 257 output tokens on the essay shape, which sends 348 and exceeds it on 22 of 24 requests. Input spans 573 to 671 tokens a request across the two retrieved shapes, so this does not rest on one request the way a latency tail does |
