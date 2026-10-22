# Where the Work Actually Goes

Chapters 1 and 2 built a system, Chapter 3 argued about its parts, and Chapter 4 handed
the model the loop. This chapter is about your time: which activities you will actually
spend your days on, and why it is almost never the one you expect.

*The problem.* I assumed the hard part was writing the prompt. People who do this for a
living say it isn't.

*The question.* If not the prompt, then what?

## Why the Prompt Looks Like the Job

The instructions are the part of an AI system you can read straight through and change in
a sentence.

You can see them. You can alter one word and watch the answer change. They look like the
place where the behaviour is configured, and for the first hour of building something they
genuinely are the thing you are working on. Most writing aimed at beginners shows you a
prompt, because a prompt fits on a page.

Everything else is either invisible from outside or does not exist until you build it. So
this chapter is about **four activities** rather than about Chapter 2's five parts — the
two lists are not the same, and the activities cut across the parts:

| The activity | What it is |
|---|---|
| Choosing what reaches the model | Deciding, per request, what goes into the context |
| Deciding what it may do | Fixing the boundary around the tools, before anything runs |
| Finding out whether it works | Building the thing that tells you, and then using it |
| Controlling what it costs | Noticing when a change makes the bill grow faster than the use |

Writing the instructions is part of the first. It is not one of the four.

## Choosing What Reaches the Model

Chapter 1 established that if you want the model to use information, it has to be in the
request. Chapter 2 named the machinery that puts it there. This is the work of deciding
**what to put in**, every time, for every request.

It is a continuous series of judgements, not a setup task:

- Which documents bear on this question, out of a collection too large to send?
- How much of each one — the whole thing, a section, a sentence?
- How many earlier turns of the conversation still matter?
- What gets dropped when it does not all fit?

Take the support request from Chapter 1. The answer needed one line: order 4471's shipping
record. Choosing it meant passing over the rest of that order's history, the returns
policy, the courier's tracking feed and the customer's three earlier messages — and
deciding how much of whatever was kept to send. None of that is in the instructions. All of
it is a judgement somebody made, for that one request.

Every one of those has a cost on both sides. Send too little and the answer is poorly
informed. Send too much and you pay for it on every call, and the answer gets worse in
ways Chapter 16 explains.

## Deciding What It May Do

This is Chapter 2's tools and Chapter 3's **second** gap — the model cannot act — as a job
rather than as a principle.

The work is not writing the tool. A tool is usually a function that already exists in your
codebase with a description attached. The work is the boundary around it, and it is made
of decisions that are cheap now and expensive later:

| The decision | What it fixes |
|---|---|
| Which tools exist at all | What the model can actually use. It may still ask for one you never described, and your code has nothing to run |
| What each one may touch | Whether a mistake is an inconvenience or an incident |
| What must be checked before it runs | Which bad calls are refused by your code rather than by luck |
| Which cases stop and wait | Where a person is in the loop, from Chapter 4 |

In a running project this is not a one-off. Every new tool is a small design review: what
can this reach, what happens if the model calls it with wrong arguments, and what does the
worst plausible call do? A team that answers those three questions, and decides which cases
should stop and wait, is doing this job. A team that adds tools because they are useful and finds out afterwards
is doing it too, just later and at a worse price.

> **Tip:** The cheapest version of this work is subtraction. A tool that only reads cannot
> change anything. A tool whose scope is one customer's records cannot touch another's. Much
> of the safety in a well-built system comes from what its tools were never allowed to do,
> not from checks catching them doing it.

## Finding Out Whether It Works

Here is the activity that does not exist until you build it.

You can tell whether *this* answer looks reasonable by reading it. You cannot establish
that a feature works by using it, and the reason is in the earlier chapters: Chapter 1
showed the same request can come back differently, and Chapter 4 showed that an
arrangement which succeeds a third of the time still hands you a good first try about a
third of the time. Using it can reveal a failure. It cannot establish that there isn't one.

So knowing whether the thing works means building something that measures it — a set of
cases, a way to decide whether each answer passed, and a number you can compare with last
week's. The field's word for that activity is **evaluation**, and Chapters 30 to 33 are
where you learn to do it.

One part of evaluation has its own name and its own reputation for consuming time:
**error analysis**, which means reading real outputs, sorting the failures into kinds, and
working on the largest kind. Chapter 30 teaches the method.

> **Note:** Practitioners report that evaluation and error analysis together take a
> substantial part of building an application. That is a widely repeated account from
> people doing the work, not a measurement — nobody has timed it across a representative
> set of projects, and the share plainly differs between a prototype and a system with
> users. Take the direction seriously and hold the size loosely. Chapter 6 is about saying
> exactly this kind of thing out loud.

## Controlling What It Costs

Chapter 1 gave the arithmetic and Chapter 2 said where the text lives. The ongoing work is
noticing when a change makes the bill grow faster than the usage.

The things that do it are all easy to miss in a single call:

- An extra paragraph of standing instructions, paid for on every request.
- A reply that got longer because the instructions got vaguer.
- A retrieval step fetching ten passages where three would have done.
- A loop taking six steps instead of two.

Every one of those shows in a monthly total. None of them looks like a problem in the call
you are looking at, and the total on its own does not tell you which of them did it — so the
activity is really two: watching a number, and being able to attribute a change in it to a
change you made. Chapter 53 is where that becomes a method.

## Telling Which Part Failed

Chapter 2 promised this chapter would say how much of the real work telling failures apart
turns out to be. There is no number for it. What there is: it is an activity of its own,
nobody gets to skip it, and it is part of why reading outputs is slow.

A wrong answer is one symptom with five common causes. Retrieval may have found nothing
useful. The context may have been assembled badly, or been too full. The model may have
ignored material that was right there. A check may have passed something it should have
caught. A case that needed a person may never have reached one.

**Nothing in the output tells you which.** The answer looks the same either way, and the
natural response — change the instructions and try again — is the move that tells you
least about which.

Separating them is its own activity, and it is why two things later in this book exist:
recording what actually happened on each request, so a failure can be traced rather than
argued about (Chapter 33), and measuring retrieval and generation separately, so you can
say which half failed (Chapter 32). Both are work you have to do deliberately. Neither
happens because the system is well written.

## Why Finding Out Takes So Long

Two reasons, and they are different in kind.

**It is the activity that decides the other three.** Which of two retrieval arrangements is
better? Is the tool boundary too tight, blocking useful work? Can the instructions be
shortened without making the answers worse? Each of those is a measurement question, and
without a measurement you are changing things and hoping — and because the system is not
repeatable, trying it twice does not settle it either. Chapter 20 is where you learn how
many times is enough.

Not every question is like this. The tool boundary has a part that measurement cannot
decide: some things are refused because of what they would cost if they went wrong, not
because of how often they do. Chapter 3 made that argument. But the questions that *are*
empirical are most of the day-to-day ones.

**And the failures have to be hunted.** Ordinary software has a loud failure class:
something crashes, and the crash announces itself with a stack trace and a timestamp. A
model-based system has that class too — a crash, a timeout, output your code cannot read.
What it has in addition is a failure that announces nothing: a fluent, confident, wrong
answer. The system does not know it is wrong, because knowing would need the very check
you are trying to build.

Some of those failures do reach you. A check you wrote catches the ones you anticipated.
Users report the ones that affect them, slowly and unevenly. What is missing is the class
nobody anticipated and nobody complained about. That class reaches you only if somebody
goes looking for it: reading output nobody has complained about, or measuring over cases
nobody has reported on.

> **Tip:** When you join a team building on models, the most useful question is "how do you
> know it is working?" The quality of the answer tells you more than any description of the
> architecture. "Our users would tell us" is an answer — it describes a real channel — but
> it is the slowest one available, and it only ever returns the failures somebody noticed
> and minded enough to mention.

## What This Does to a Project

The shape of the work is the opposite of what the first week suggests.

| | The first week | The months after |
|---|---|---|
| What you do | Write instructions, get something working | Read outputs, find what is wrong, fix the largest thing |
| What feels productive | Everything. It works almost immediately | Slow. Much of it produces no visible change |
| What you learn | That the idea is possible | Whether it is reliable |

A working demonstration arriving quickly is real, and it is a large part of why these
projects get approved. The trouble is what it suggests about the rest. It does not mean the
work is nearly done, because making something work once and establishing that it works are
not the same activity, and the second has barely started when the first one ends.

> **Warning:** The gap between *a demonstration exists* and *this can be relied on* is where
> the measuring happens, and a plan that has allowed time for the demonstration has allowed
> none for it. That is the practical thing to carry out of this chapter: when you estimate
> work on a system built around a model, put the measuring in the estimate, because it is
> the part that will surprise you.

None of this makes the instructions unimportant — Chapter 18 is a whole chapter on writing
them properly, and a badly specified request wastes everything downstream of it. The claim
is narrower: they are the part you will finish first and think about least.

## Lab: Sort an Account of Real Work

No code, nothing to install, fifteen minutes. The account below is **invented**, which
matters and is said again in step 3: because it was written for this exercise, it cannot
tell you anything about where real engineering time goes. What it can do is show you
whether you can tell the four activities apart in somebody's prose, which is a skill you
need before any real account is worth reading. It has a key, so you can be wrong and find
out.

**Step 1.** Before reading it, write one line: of the four activities, which do you expect
an account like this to spend the most paragraphs on?

*Expected result:* a written prediction. Writing it first is the whole point — you cannot
quietly adjust it afterwards.

### The account

> **1.** We had three weeks before the demo and two engineers, one of whom was new.
>
> **2.** The feature was a support assistant. A customer asks about an order and it
> answers from our own records rather than from anything the model was trained on.
>
> **3.** The first version pasted the customer's entire order history into every request.
> It worked. It also cost about nine cents a question, and the projected monthly figure was
> the first thing anyone outside the team asked about.
>
> **4.** So we cut it down to the three most recent orders plus the returns policy, which
> meant deciding what gets dropped when somebody has forty orders and only three fit.
>
> **5.** We spent two days on the wording of the instruction that tells it to refuse
> anything it cannot answer from the records.
>
> **6.** We gave it one tool, a lookup by order number. We spent longer agreeing that it
> must not issue refunds than we spent writing the lookup itself.
>
> **7.** In week two the platform team moved us onto the new queue, which cost us a day
> and was nobody's fault.
>
> **8.** We had no way of telling whether any of it was working, so we wrote down forty
> real customer questions with the answer each one should have, and started scoring them
> by hand.
>
> **9.** Reading forty scored answers in one sitting, we noticed the bad ones were mostly
> a single kind of mistake: when a customer mentioned two orders, it answered about the
> wrong one.
>
> **10.** We added a sentence to the instruction about which order to prefer, and the
> score went from 31 of 40 to 34 of 40.
>
> **11.** The demo went well. We shipped it to a hundred users the week after.
>
> **12.** Three weeks later a customer was shown the correct details of an order that was
> not theirs. The lookup took an order number and never checked whose order it was.

**Step 2.** Label each of the twelve paragraphs with one of six things: the four
activities, *the instructions*, or **none of these**. *The instructions* is on the list but
is still not one of the four — it is part of the first, as this chapter said at the start.
It is separated out here because telling the two apart in somebody's prose is the whole
exercise.

*Expected result:* the key is below. Six labels, twelve paragraphs.

| Label | Paragraphs | Count |
|---|---|---|
| **None of these** | 1, 2, 7, 11 | 4 |
| **The instructions** | 5, 10 | 2 |
| **Deciding what it may do** | 6, 12 | 2 |
| **Finding out whether it works** | 8, 9 | 2 |
| **Choosing what reaches the model** | 4 | 1 |
| **Controlling what it costs** | 3 | 1 |

Three of those are worth arguing with, so argue with them:

- **Paragraph 3** is cost, not *choosing what reaches the model*. Pasting the whole
  history is a choice about what reaches the model, but what the paragraph is *about* is
  the bill and who asked about it. Paragraph 4 is where that choice gets made.
- **Paragraph 10** is *the instructions*, even though it ends in a number. What they did
  was change some wording; the score is how they checked it. Keep the change and the check
  apart — conflating them is how teams come to believe a reworded prompt fixed something.
- **Paragraph 12** is *deciding what it may do*. The failure happened in production, but
  it was decided in paragraph 6, when a tool was given an order number and no notion of
  whose order it was. That is the point of the Tip in *Deciding What It May Do*: "a tool
  whose scope is one customer's records cannot touch another's".

**Step 3.** Compare the counts with your prediction from step 1.

*Expected result:* **none of these** is the largest label, at four — team, product
description, platform work and shipping are all real paragraphs and none of the four
activities. Among the four activities, *finding out whether it works* and *deciding what it
may do* tie at two, while *choosing what reaches the model* and *controlling what it costs*
have one each. *The instructions* also has two, and is not one of the four.

Now notice what that distribution is worth: **nothing.** I wrote these paragraphs, so I
chose those counts, and I could have made any activity win — including the one this chapter
argues for, which is sitting at joint first. If your prediction looks confirmed here, it is
a coincidence I manufactured. I wrote the ending too, so the account cannot tell you how
often a project goes this way either. The share claim earlier in this chapter rests on what
practitioners report; one invented account is evidence neither for it nor against it.

**Step 4.** Find the sentence where the account says how it knew something had improved.
Write down what it would take to believe it.

*Expected result:* paragraph 10 — "the score went from 31 of 40 to 34 of 40". That is a
measurement, taken on a written-down set of cases, and it is more than most accounts offer.
It is also three answers out of forty, from one run, with no indication of how much the
score moves when nothing changes. Chapter 20 is where you learn whether a difference like
that is real. Noticing that the question is open is this chapter's job; answering it is not.

**Step 5.** Paragraph 12 describes a failure reaching a customer. Work through the five
causes this chapter listed and say which one it was.

*Expected result:* **none of the five** — and the first reason is that the answer was not
even wrong. The details were correct; they went to the wrong person. The chapter's five are
causes of a *wrong answer*, so none of them is in the running. Nor would they be if the
answer had been wrong: retrieval found what it was asked for, the context was assembled
correctly, the model used what it was given, no check was wrong about what it checked (the
authorisation check never existed, so nothing judged badly), and no person was needed. The tool did exactly what it was built to do,
for the wrong person. That is why this chapter says *five common causes* rather than five
causes — a tool that acts with the service's rights instead of the caller's is a sixth, and
Chapter 51 owns it. A list of causes you trust too far is its own failure mode.

**Step 6, optional, and the only step that can tell you anything about the world.** Find
two real written accounts of somebody building an AI feature — an engineering post, a
conference talk, a retrospective. Not a tutorial and not an announcement. Label their
paragraphs the same way, and compare the two with each other. There is no key. If they
disagree with each other, that is the honest finding and two accounts is too small a
sample. Whatever you get, remember you counted words rather than hours: a word count says
what somebody chose to write about.

## Summary, Key Terms, and Review Questions

### Summary

The instructions are the visible part of the job and the part you finish first. The work is
four activities: choosing what reaches the model, deciding what it may do, finding out
whether it works, and controlling what it costs — plus the thing that cuts across all of
them, telling which part failed when an answer is wrong. **Evaluation** is the name for
finding out whether it works, and **error analysis** is the part of it that means reading
real outputs and sorting failures into kinds; practitioners report that the two together
take a substantial part of building an application, which is an account from people doing
the work rather than a measurement. Finding out takes long for two reasons: it decides most
of the other questions, and its failures do not announce themselves the way a crash does,
so the ones nobody anticipated reach you only if somebody reads output nobody complained
about. The practical consequence is an estimate: put the measuring in the plan.

### Key Terms

| Term | Meaning |
|---|---|
| **Evaluation** | Building and using something that tells you whether a system works: a set of cases, a way to judge each answer, and a number you can compare over time |
| **Error analysis** | The part of evaluation that means reading real outputs, sorting the failures into kinds, and working on the largest kind |

### Review Questions

1. Why do beginners consistently overestimate how much of the work is writing instructions?
2. Your colleague says the feature is working because they have tried it several times and it was good. Give two reasons that is weak evidence.
3. Give one question about a system that measurement answers, and one that it cannot, and say what settles the second.
4. A user reports a wrong answer. Name three different parts that could have caused it, and say what you would need in order to tell them apart.
5. A project plan allows two weeks for "build the AI feature" and nothing else. What is missing?

### Review Answers

1. Because the instructions are the only part you can read straight through and change in a sentence, and the only part that fits on a page of an article. The four activities are either invisible from outside or do not exist until somebody builds them.
2. The same request can come back differently, so a handful of good answers is a small sample of a distribution they have not measured. And by Chapter 4's ten-step arithmetic, an arrangement that succeeds a third of the time still hands you a good first try about a third of the time, so "I tried it and it worked" is also what an unreliable system looks like from close up.
3. Measurement answers which of two retrieval arrangements is better — run both over the same cases and compare. It cannot settle whether a tool should be allowed to issue refunds unsupervised, because that turns on what a rare failure would cost rather than on how often it happens; that is a judgement about consequences, and above the legal floor it is a design decision.
4. Any three of: retrieval found nothing useful; the context was assembled badly or was too full; the model ignored material it was given; a check passed something it should have caught; a case needing a person never reached one. To tell them apart you need a record of what actually happened on that request — what was retrieved, what was sent, what came back — and retrieval and generation measured separately.
5. Everything that decides whether it can be relied on: a set of cases, a way to judge answers, the reading of real outputs, and the cycle of fixing the largest failure and measuring again. The two weeks are for making it work once, which is a different activity from establishing that it works.

> **You understand this when** you can name the four activities, say which one decides most
> of the others, and explain why nothing in a wrong answer tells you which part produced it.
