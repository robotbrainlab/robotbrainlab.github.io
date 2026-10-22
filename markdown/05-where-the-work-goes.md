# Where the Work Actually Goes

The last four chapters built up a system and then argued about its parts. This one is
about your time: which of those parts you will actually spend your days on, and why it is
almost never the one you expect. It is the one most likely to change how you plan a
project.

*The problem.* I assumed the hard part was writing the prompt. People who do this for a
living say it isn't.

*The question.* If not the prompt, then what?

## Why Everyone Guesses Wrong

The instructions are the part of an AI system you can read straight through and change in
a sentence.

You can read them. You can change one word and watch the answer change. They look like the
place where the intelligence is configured, and for the first hour of building something
they genuinely are the thing you are working on. Almost everything written for people starting out shows
you a prompt, because a prompt fits on a slide.

The parts you cannot see are the ones that take the time:

| What you can see | What you spend your time on |
|---|---|
| The instructions | What else goes into the request, and how it got there |
| | What the system is allowed to do |
| | Whether the answers are any good, and how you would know |
| | What it costs, and whether that can continue |

That is the chapter in a table. The rest of it says what those four are and which one wins.

## Four Activities

### Choosing what reaches the model

Chapter 1 established that if you want the model to use information, it has to be in the
request. Chapter 2 named the machinery that puts it there. This is the work of deciding
**what to put in**, every time, for every request.

It is a continuous series of judgements, not a setup task:

- Which documents are relevant to this question, out of a collection too large to send?
- How much of each one — the whole thing, a section, a sentence?
- How many earlier turns of the conversation still matter?
- What gets dropped when it does not all fit?

Every one of those has a cost on both sides. Send too little and the answer is poorly
informed. Send too much and you pay for it on every call, and the answer gets worse in
ways Chapter 16 explains.

### Deciding what it may do

This is Chapter 2's tools and Chapter 3's fourth gap, as a job rather than as a principle.

The work is not writing the tool. The work is the boundary around it: which tools exist at
all, what each one may touch, what has to be checked before it runs, and which cases stop
and wait for a person. Those decisions are made before anything runs, they are hard to
change later, and getting them wrong is the mistake with no undo.

### Finding out whether the output was any good

Here is where most people are most surprised.

You cannot tell whether an AI feature works by using it. You can tell whether *this* answer
looks reasonable. Chapter 1 established that the same request can come back differently;
Chapter 4 showed that a run which works a third of the time still produces a working demo
on the first try, one time in three.

So knowing whether a system works means building something that measures it — a set of
cases, a way to decide whether each answer passed, and a number you can compare against
last week's. **That machinery does not exist until you build it**, and nothing else in the
project tells you whether it is time to build it.

### Controlling what it costs

Chapter 1 gave the arithmetic and Chapter 2 said where the text lives. The ongoing work is
noticing when a change makes the bill grow faster than the usage: an extra paragraph of
instructions, a longer reply, a retrieval step that fetches ten passages where three would
have done, a loop that takes six steps instead of two.

None of these shows in a single call. Every one of them shows in a monthly total — though
telling which of them did it is work in itself.

## Which One Takes the Most Time

Practitioners who build these systems report that one of the four dominates: **working out
whether the output was any good**, and specifically the part of it that means reading real
outputs, sorting the failures into kinds, and fixing the largest kind. That activity has a
name — **error analysis** — and Chapter 30 is where you learn to do it.

> **Note:** "Takes a substantial part of development" is what practitioners report, not
> something measured in a controlled way, and the share will differ between a prototype and
> a system with real users. Treat it as a strong and widely-repeated impression rather than
> a figure. The direction is not seriously disputed; the exact weight is not knowable.

## Why It Dominates

Not because it is harder than the rest. Because it is the only one that tells you what to
do next.

Consider the others. Choosing what reaches the model — which of your two retrieval
arrangements is better? Deciding what it may do — is the tool boundary too tight, blocking
work, or too loose? Controlling what it costs — can you shorten the instructions without
making the answers worse?

**Every one of those questions is answered by measurement.** Without it you are changing
things and hoping, and because the system is not repeatable you cannot even tell whether a
change helped by trying it twice.

There is a second reason, and it is the one that catches teams out. In ordinary software,
the failures are mostly things that *crash* — and a crash announces itself. Here the
failures are answers: fluent, confident, and wrong in a way nothing in the system notices.
Nobody reports them. They do not appear in a log as errors. **The only way they reach you
is if somebody goes looking.**

> **Tip:** When you join a team building on models, the single most useful question is "how
> do you know it is working?" The quality of the answer tells you more about the project
> than any description of its architecture. "Our users would tell us" is not an answer; it
> is a description of how failures are currently found, which is to say, slowly and by
> accident.

## What This Does to a Project

The shape of the work is the opposite of what the first week suggests.

| | The first week | The months after |
|---|---|---|
| What you do | Write instructions, get something working | Read outputs, find what is wrong, fix the largest thing |
| What feels productive | Everything. It works almost immediately | Slow. Much of it produces no visible change |
| What you learn | That the idea is possible | Whether it is reliable |

The demo arriving in an afternoon is real, and it is why these projects get approved. It is
also why they get estimated wrongly: the afternoon is not 10% of the work with 90% to
follow, it is a different activity altogether, and the second one has barely started when
the first one ends.

> **Warning:** The gap between *a demo exists* and *it can be relied on* is where most of
> the schedule actually goes, and it is almost never in the plan. If you take one practical
> thing from Part I, take this: when you estimate work on a system built around a model,
> the measuring is the project, and the prompt is the warm-up.

## Lab: Where Did the Time Go?

No code. This one is archaeology rather than observation.

**Step 1.** Find a written account of somebody building a real AI feature — an engineering
blog post, a conference talk, a long post from somebody who shipped one. Not a tutorial,
and not a product announcement.

*Expected result:* an account that describes problems, not just an architecture. If it has
no problems in it, it is marketing; find another.

**Step 2.** Mark every paragraph with which of the four activities it is about: what
reaches the model, what it may do, whether the output was good, what it costs.

*Expected result:* an uneven split. Most accounts of real work spend more on the third than
on the other three together. Some spend almost all of it there.

**Step 3.** Find the sentence where they say how they knew something had improved. Write it
down exactly.

*Expected result:* either a description of a measurement, or an absence. Both are common.
The absence is worth noticing, because the piece will usually still claim an improvement.

**Step 4.** Count how much of the account is about the instructions.

*Expected result:* usually a small fraction, and often one paragraph near the start — which
is the reverse of the attention prompts get in material aimed at beginners.

**Step 5.** Write one sentence: *if I built this, the thing I would have underestimated is
____.*

*Expected result:* a sentence about one of the four activities. Keep it. You can check it
against your own experience later, which is the only way this chapter can be proved to you
rather than asserted.

## Summary, Key Terms, and Review Questions

### Summary

The instructions are the visible part of an AI system and the smallest part of the job. The
work is in four activities: choosing what reaches the model, deciding what it may do,
finding out whether the output was any good, and controlling what it costs. Practitioners
report that the third dominates — and specifically **error analysis**, the reading of real
outputs and sorting of failures into kinds that Chapter 30 teaches. It dominates for two
reasons: it is the only activity that tells you what to do about the other three, and the
failures here do not announce themselves the way a crash does, so they reach you only if
somebody goes looking. The practical consequence is an estimate: the demo is an afternoon,
and the measuring is the project.

### Key Terms

| Term | Meaning |
|---|---|
| **Error analysis** | Reading real outputs, sorting the failures into kinds, and fixing the largest kind. The activity practitioners report spending most of their time on |

### Review Questions

1. Why do beginners consistently overestimate how much of the work is writing instructions?
2. Your colleague says the feature is working because they have tried it several times and it was good. Give two reasons that is weak evidence.
3. Of the four activities, why does measuring dominate the other three rather than sitting beside them?
4. What is different about the *kind* of failure in a system built around a model, compared with ordinary software, and what does that difference cost you?
5. A project plan allows two weeks for "build the AI feature" and nothing else. What is missing, and roughly how would you expect the real shape to differ?

### Review Answers

1. Because the instructions are the only part you can see and change directly, and the only part that fits in an article. Everything else — what reaches the model, what it is allowed to do, whether it works, what it costs — is either invisible from outside or has to be built before it can be observed.
2. The same request can come back differently, so a few good answers are a small sample of a distribution they have not measured. And a system that succeeds a third of the time still produces a good first try one time in three, so "I tried it and it worked" is exactly what an unreliable system looks like from close up.
3. Because it is the only one that answers the questions the other three raise. Which retrieval is better, whether the tool boundary is too tight, whether shorter instructions hurt the answers — each is a measurement question. Without it you change things and hope.
4. Ordinary software mostly fails by crashing, and a crash announces itself. Here it fails by producing a fluent, confident, wrong answer that nothing in the system notices and nobody reports. The cost is that failures reach you only if somebody deliberately goes looking, so the work of looking has to be built and staffed.
5. The plan is for the demo, which is the afternoon's work. Missing is everything that decides whether it can be relied on: a set of cases, a way to judge answers, the reading of real outputs, and the cycle of fixing the largest failure and measuring again. Expect that part to dominate the schedule and to produce little visible change while it runs.

> **You understand this when** you can say why "I tried it and it worked" tells you almost
> nothing about whether a system works.
