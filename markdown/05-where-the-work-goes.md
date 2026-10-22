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
repeatable, trying it twice does not settle it either.

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

## Lab: Where Did the Time Go?

No code. This one is archaeology, and it is built so you can be wrong.

**Step 1.** Before you read anything, write down your guess: of the four activities, which
do you expect a real engineering account to spend most of its words on? One line.

*Expected result:* a written prediction. The point of writing it first is that you cannot
quietly adjust it later.

**Step 2.** Find two written accounts of somebody building a real AI feature — an
engineering blog post, a conference talk, a long post from somebody who shipped one. Not a
tutorial, and not a product announcement. Take whatever you find first; do not pick the
ones that look most interesting, because that is how you choose your own answer.

*Expected result:* two accounts, chosen before you knew what was in them.

**Step 3.** Go through each one paragraph by paragraph and label it with one of six
things: the four activities, *the instructions*, or **none of these**. A paragraph about the
wording of a prompt is *the instructions*; one about which material goes in is *choosing
what reaches the model*. Expect a lot of *none* — team, motivation, infrastructure and
architecture are all common and are none of the four.

*Expected result:* six counts per account, with *none* often the largest. If you find
yourself forcing a paragraph into an activity, label it *none*; the forcing is how a
prediction gets confirmed by accident.

**Step 4.** Compare the two accounts with each other, and with your guess from step 1.

*Expected result:* one of three. The two accounts agree with each other and with your
guess. They agree with each other and not with your guess — the useful case. Or they
disagree with each other, which tells you two accounts is too small a sample, and is the
honest finding. Whichever you get, remember what you measured: words, not hours. A word
count says what somebody chose to write about.

**Step 5.** In each account, find the sentence where they say how they knew something had
improved, and write it down exactly. If there is no such sentence, write *none* — and note
whether the piece still claims an improvement.

*Expected result:* for each account, either a described measurement or a stated absence.
Both are common, and the absence beside a claimed improvement is the thing worth keeping.

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
