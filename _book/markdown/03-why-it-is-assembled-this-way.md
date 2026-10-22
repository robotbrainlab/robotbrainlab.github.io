# Why It Is Assembled This Way

Chapter 2 named the five parts and said what each one does. This chapter makes the
argument underneath them: why each gap is real rather than a limitation somebody will fix,
and what you pay for closing it. Every part you add buys something and costs something,
and knowing the price is the difference between designing a system and copying a diagram.

*The problem.* Why not just ask the model? Why does every real system wrap it in so much
machinery?

*The question.* Which jobs can the model genuinely not do, and what does each fix cost me?

## The Shape of the Argument

Four gaps, in the order Chapter 2 gave them. For each one, three questions:

1. **Is it real?** Or is it a limitation of today's models that will close on its own?
2. **What closes it?**
3. **What does closing it cost?**

The third question is the one this chapter exists for. If a part had no cost there would be
no decision to make, and the interesting design decisions all live in what you give up.

## It Does Not Know Your Data

### Is the gap real?

Yes, and it is permanent, which is not obvious.

The easy version of this gap is the one Chapter 1 gave: the model's training stopped at a
date, so it has not seen anything since. That half does shrink — models get retrained, and
newer ones tend to know more recent things.

The half that does not shrink is everything else:

- **Your data is private.** It is not in any training set and you do not want it to be.
- **Your data changes constantly.** An order's status is different this afternoon. No
  amount of training reaches that.
- **Your data is different per reader.** Two users ask the same question and the correct
  answer differs, because they are allowed to see different things. A model's knowledge is
  one body of knowledge, identical for everyone who calls it.

That last point is the one to keep. Even a model trained this morning on everything your
company owns would answer every user from the same store, and could not be told that this
user may not see that record. It would be wrong wherever permissions differ or the data has
moved since — which, in most companies, is most of the time.

> **Note:** You may have heard that continuing a model's training on your own documents
> solves this. It does not. Training is a snapshot too, so the data still goes stale; and
> weights carry no notion of who is allowed to see what, so per-reader scope is still
> impossible. It also puts your private material into a set of weights, which is the thing
> the first point says you would rather avoid. It is one of several reasons Chapter 39
> treats tuning as the last lever rather than the first.

### What closes it, and what it costs

Retrieval closes it, and the price is a second system that can be wrong on its own.

| You gain | You pay |
|---|---|
| Answers about material the model never saw | A search system to build, fill and keep current |
| Material that is current as of this request | Latency: a search has to happen somewhere in the request |
| Per-user answers, because you choose what to fetch | Context space, which is finite and not free |
| A citation — a pointer back to the passage an answer came from — when you keep track of what you fetched | **A new failure mode: retrieving the wrong thing** |

The last row is the important one. Before retrieval, a wrong answer meant the model was
wrong. After retrieval, a wrong answer might mean the search found nothing useful, or found
something misleading, and the model faithfully used it. **You have not removed the failure.
You have split it in two**, and telling the halves apart becomes work you now have to do.

## It Cannot Act in the World

### Is the gap real?

Yes, and this one is not even a limitation. It is what the component is.

A model produces text. That is the whole of its output. Text that says
`refund(order=4471)` is still text; it refunds nothing. Something else has to read that
text and make a refund happen, and that something is a program somebody wrote.

This will not change with better models, because it is not about capability. A model that
could act directly would be a model wired to a system that executes what it says — which
is exactly the arrangement we are describing, with the wire hidden.

> **Tip:** This is worth being precise about in conversation, because the loose version —
> "the model called the API" — hides the part that matters. Something decided to
> honour the request. If you cannot say what decided, you cannot say what would have
> stopped it.

### What closes it, and what it costs

Tools close it, and the price is everything a tool can reach.

| You gain | You pay |
|---|---|
| The system can do things, not only say them | Every tool is a way in, and it has to be secured |
| The model can fetch what it needs mid-answer | A tool that is slow makes the whole answer slow |
| Actions can be logged, and some can be compensated — if you build that | A tool that is down takes a working feature with it |
| — | **Actions can happen that nobody intended** |

That last cost deserves its own sentence, because it is different in kind from the others.
A wrong answer is a wrong answer. A wrong **action** has already happened by the time you
read it. You can sometimes issue a second action that compensates — re-charge the card, send
a correction — but that is not an undo, and for a deleted record or a message somebody has
already read there is often nothing to issue.

An **irreversible action** is one of these: something a tool does that no later action
undoes. This is the whole reason Chapter 2 insisted that your code decides, and it is why
the cheapest safety measure in this book is declining to give a tool an irreversible action
at all. Chapter 51 spends a long time on what a tool may touch.

## It Cannot Reliably Check Itself

### Is the gap real?

Yes, and the reason is structural rather than a matter of effort.

Ask a model whether its last answer was correct and it produces another answer. That second
answer comes from the same process as the first and works from the same information, so it
stands in the same relation to the truth as the first did: usually right, sometimes
confidently wrong, and not consulting any record either way. **A confident answer and a
confident check are the same kind of object.**

You can often improve things by asking in a way that makes the model look harder, and
Chapter 31 is about where that does and does not work. But the structural point stands: a
check that shares a component's failure modes is not an independent check. It will tend to
be wrong in the same places, for the same reasons.

> **Warning:** This is why "I asked it to double-check and it said it was sure" is worth
> very little as evidence. What the model says about its own confidence is produced the
> same way as everything else it says. It is not reading off a measurement of whether the
> answer is right, because it has none to read.

### What closes it, and what it costs

Checks close it, partially, and the price depends entirely on which kind you can afford.

| Kind of check | You gain | You pay |
|---|---|---|
| A rule your code applies | The same verdict every time, for nothing | It only catches what you thought to write down |
| A second model asked to judge | Catches what rules cannot describe | Another call, and another component that can be wrong |
| A person | Real judgement | Time, money, and a queue |

The deeper cost is one the table cannot show: **every check is built against somebody's
idea of what might go wrong.** A rule is built narrowly, against one named failure. A model
judge is built broadly — "is this rude?" covers rudeness nobody listed — but it is still
built against a question somebody thought to ask. Either way, a system is blind to the
failures nobody imagined. That is not an argument against checking. It is the reason
Chapters 30 to 33 start by reading real failures rather than by writing checks.

There is also a cost in the other direction, and it is the one teams discover late. **A
check that is too strict rejects good answers.** Say your rule is that an answer must cite
a source. A reply that answers the question perfectly from a single obvious fact, without
citing anything, now fails — and your users see a refusal where a good answer was waiting.

Every check that has a setting has this shape. Tighten it and you block more bad output and
more good output; loosen it and you let more of both through. You can escape the trade by
building a *better* check, which is real work; you cannot escape it by choosing a cleverer
threshold on the check you have.

## It Is Not Accountable

### Is the gap real?

Yes — but not in the way it is usually told, and the usual telling gets the design wrong.
It is also the only one of the four where adding the part that closes it leaves the cause
exactly where it was.

Here is the version to discard first: *without a person in the loop, nobody is answerable.*
That is false. If your company deploys a system that refuses a loan, loses a customer's
money or publishes something defamatory, **your company is answerable**, whether or not
anybody looked at the decision. Automating something does not move responsibility onto the
thing you automated it with. In many fields that is written into law.

So **accountability** — somebody who can be asked to answer for a decision, and who bears a
consequence for it — **never actually moves.** It sits with the operator — you, your team,
your company — from the first line of code. What the model cannot do is **carry any of it
for you**:

- It cannot be asked to explain a decision in terms a person can defend.
- It cannot be sanctioned, struck off, called in front of a regulator, or sued.
- It cannot notice that this particular case is the one that should not be decided by rule.

That is the real gap, and it is sharper than the usual one. **You are answerable for
decisions you did not see and could not have defended.** The system
produced them; the responsibility was yours the whole time.

> **Note:** This is usually filed under "ethics" and set aside. It is better understood as a
> design constraint, like a rate limit: there is a set of decisions your organisation cannot
> defend making unseen, and the system has to be built so those reach somebody who can.
> Where that set is drawn is partly law and partly judgement — the legal floor is not yours
> to move, and everything above it is a design decision you own.

**Does a better model close this?** It can shrink the part of the set you draw yourself — a
system you trust more is one you choose to supervise less closely. It cannot touch the part
the law draws, and it does not change who is answerable. That is why this gap is unlike the
first three: progress moves its cost, never its cause.

### What closes it, and what it costs

People close it — not by becoming accountable, but by being how an accountable organisation
discharges what it already owes.

| You gain | You pay |
|---|---|
| A decision somebody can defend, on the cases that need defending | The system is now as fast as its queue |
| Judgement on the cases nobody anticipated | Reviewers are expensive, and good ones are scarce |
| A record of who decided what, and on what evidence | Approval is a bottleneck that grows with volume |
| — | **Rubber-stamping, which looks like review and is not** |

The last row is the failure that catches people out. That is **rubber-stamping**: approval
given without real attention. Show a reviewer a
hundred confident approvals an hour and most will approve nearly all of them: almost every
one is fine, and
attention does not survive that. The effect has two halves, and the second is less obvious
than the first — volume wears attention down, and a confident recommendation pulls a
reviewer toward agreeing with it even when there is plenty of time. You then pay the full
cost of review and receive very little of its value.

> **Note:** That is a well-studied effect in people supervising automated systems rather
> than something peculiar to this field, and it is one of the sturdier findings behind any
> claim in this chapter. Expect it; design against it.

So the question is never *should a person review this?* It is **which cases, how many an
hour, and with what put in front of them** — and above the legal floor, that is a design
decision like any other.

## The Pattern

Read those four together and the shape is the same every time.

> **Every part you add removes one failure and introduces another.**

| The part | Removes | Introduces |
|---|---|---|
| Retrieval | Answering from nothing | Retrieving the wrong thing |
| Tools | Being unable to act | Acting wrongly |
| Checks | Shipping bad output unnoticed | Blocking good output, and a false sense of safety |
| People | Decisions made unseen that nobody could defend | Delay, cost, and rubber-stamping |

This is not pessimism, and it is not an argument for building less. It is the reason
compound systems are **designed** rather than assembled: you are choosing which failures
you would rather have.

Two consequences follow, and they run through the rest of the book.

**The simplest arrangement that solves the problem is usually right.** Not because simple
is virtuous, but because every part is a failure you are buying. A part that is not earning
its cost should not be there, and the way you find out whether it earns its cost is to
measure — which is why so much of this book is about measurement.

**Where a cheap, automatic verdict exists, take it.** Chapter 2 noted that a system which
can run its own tests has an advantage over one that can only ask whether a summary is
good. Now you can see why: its check is the one kind whose cost stays small. Not nothing —
a test suite is a rule, so it still only catches what somebody wrote down, and it tells you
nothing at all if the model wrote the tests. Small is rare enough.

## Lab: What Does It Cost Them?

No code. Chapter 2's lab asked what parts a product has. This one asks what it paid.

**Step 1.** Take one product from Chapter 2's lab that clearly retrieves — one that answers
from documents or from your own data. Ask it something whose answer you can verify yourself.

*Expected result:* an answer you can check. Keep it.

**Step 2.** Now ask it something that sounds like it should be in its material but is not —
a plausible neighbouring question about something that does not exist.

*Expected result:* one of three. It says it does not know — which usually means an
instruction told it to, as in Chapter 1's exchange, rather than that anything checked. It
answers from general knowledge without saying so, which is the retrieval cost in action. Or
it invents something, which is the same cost, further along.

**Step 3.** For a product with tools, find the most irreversible thing it can do. Do not do
it. Work out what stands between you and it: a confirmation, a limit, a person, or nothing.

*Expected result:* either a step you can describe — a confirmation, a limit, a person — which
is somebody's answer to the cost in the tools table. Or nothing at all between you and it,
which is also an answer, and a more interesting one.

**Step 4.** Find a queue. Use a product where something you submit is reviewed, and notice
how long it takes and what you are told while waiting.

*Expected result:* a wait you can measure, and usually a message designed to make it
bearable. Both are the price of the fourth gap.

**Step 5.** Write one sentence for a product you use: *it pays ____ so that it can ____.*

*Expected result:* a sentence about trade-offs rather than features. If you cannot write
one, you do not yet know what the product chose, which is itself worth knowing.

## Summary, Key Terms, and Review Questions

### Summary

Four gaps, four parts, four prices. The model does not know your data — permanently, because
your data is private, changing and different per reader — so retrieval closes it and you pay
with a second system that can be wrong on its own. It cannot act, because it only produces
text, so tools close it and you pay with every surface a tool can reach, including actions
that cannot be undone. It cannot reliably check itself, because a check from the same
component shares its failures, so checks close it and you pay for what they were not built
to catch, and for the good answers a strict check rejects. It is not accountable —
accountability stays with you
whatever you build — so people are how you discharge it on the cases that need defending,
and you pay in delay, cost and the risk of rubber-stamping. The pattern is the lesson:
**every part removes one failure and
introduces another**, which is why the simplest arrangement that works is usually right.

### Key Terms

| Term | Meaning |
|---|---|
| **Accountability** | Somebody who can be asked to answer for a decision, and who bears a consequence for it. A property of people and organisations, never of a component |
| **Irreversible action** | Something a tool does that cannot be undone once it has happened — a refund, a message, a deletion. The reason a tool's reach is decided before it is offered |
| **Rubber-stamping** | Approval given without real attention, usually because the volume is too high for any. It costs what review costs and delivers none of its value |

### Review Questions

1. A colleague says the "does not know your data" gap will disappear once models can be
retrained cheaply every week. Give the strongest reason they are wrong.
2. What is the difference in kind between a wrong answer and a wrong action, and what does
that difference imply about which tools you offer?
3. Why is asking a model to check its own answer weaker evidence than it feels?
4. Your system sends 100 cases an hour to a human reviewer who approves 99 of them. What
have you bought, and what have you paid?
5. A teammate proposes adding a second model to judge every answer. Name two costs, and name
the question you would ask before agreeing.

### Review Answers

1. Per-reader scope. Even a model retrained this morning on everything the company owns
answers every user from the same body of knowledge, so it cannot be told that this user may
not see that record. Freshness is the half of the gap that shrinks; privacy and per-reader
scope are not.
2. A wrong answer can be read and discarded. A wrong action has already happened — the
refund is paid, the message is sent. So the decision about which tools to offer is made
before anything runs, and the cheapest protection is not offering an irreversible one.
3. The check comes from the same component and works from the same information, so it tends
to fail in the same places. It is not consulting a record. And what it says about its own
confidence is produced the same way as everything else it says, so it is not a measurement
of whether the answer is right.
4. You have bought defensibility on those cases: somebody looked, and could account for the
decision afterwards. You were accountable either way — that never moved. You are paying the
full cost of review, and at 100 an hour you are probably also paying for rubber-stamping, so
the value may be much lower than the cost. The fix is fewer, better-chosen cases, not a
faster reviewer.
5. It costs a whole extra call per answer, in money and latency, and it adds a component
with the same kind of unpredictability as the first — a different model will not fail in
exactly the same places, but it is not an independent referee either. The question to ask
first: what failure are we trying to catch, and could a rule catch it instead?

> **You understand this when** you can say, for any part of an AI system, what failure it
> removes and what failure it introduces.
