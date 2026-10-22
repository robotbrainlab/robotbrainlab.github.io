# The Agent Loop, and How Much Freedom It Actually Gets

Chapter 2 put five parts around the model and left your code in charge of the sequence:
your code retrieved, your code decided whether a tool ran, your code applied the checks. This
chapter hands one of those decisions to the model, repeatedly, and looks at what that
changes. It is the arrangement everybody means by *agent*, and the gap between how it
sounds and how it is actually deployed is the most useful thing in the chapter.

*The problem.* "Agent" sounds like it does the whole job by itself. That can't be how
anyone ships this.

*The question.* What is an agent, really, and how much is it actually allowed to do?

## One Change, and It Is Not a Small One

An **agent** is the arrangement you already know, given a loop: the model decides what to
do next, something happens, the model sees the result, and it decides again — until the
job is done or you stop it.

Nothing new has been added. There is no extra component, no different kind of model. The
tools are the tools of Chapter 2. What changed is **who decides the order**.

| | Chapter 2's arrangement | An agent |
|---|---|---|
| What happens first | Your code decides | Your code decides |
| What happens next | **Your code decides** | **The model decides** |
| How many times | Once, or a number you wrote | Until a stopping condition is met |
| What the sequence looks like | Fixed in your code, whatever it branches on | Decided as it goes |

That second row is the whole chapter.

## The Loop, Step by Step

Here is one run. The task is a support request: *"Where is my order, and if it is late,
refund the delivery fee."*

```text
  TURN 1   model: I need the order. Call lookup_order(4471).
           code : checks the call, runs it, returns the result
           result: shipped 2 Nov, promised 1 Nov, delivery fee 4.99

  TURN 2   model: It is late. Call refund(order=4471, amount=4.99).
           code : checks the call -- under the limit, so it runs it
           result: refunded

  TURN 3   model: Done. Reply to the customer.
           code : no tool asked for, so the loop ends
```

Three turns. Each one is a complete exchange of the kind Chapter 1 showed: text out, text
back. The only new thing is that the result of each turn is added to what gets sent on the
next one, so the model is deciding turn 3 with turns 1 and 2 in front of it.

Each pass through that cycle is a **step**. The number of steps is not fixed, and that is
the point: the model takes as many as it judges it needs.

> **Note:** Your code still decides whether each tool call runs, exactly as in Chapter 2.
> Handing over the loop does not hand over that. The model chooses what to *ask for*; your
> code is still the thing that says yes.

## Where the Control Flow Went

Every program you have written so far decides its own order. The order might depend on
data — an `if`, a `while` — but the *rules* for choosing are in the code, and you can read
them.

In an agent, the rules for choosing are not in the code. They are in a model's judgement,
produced fresh on each step, and Chapter 1 established that you cannot predict what a model
will produce.

So **your program's control flow is now generated at run time by something that is not
determined**. Three things follow:

**You cannot read the program and know what it does.** You can read what it is *allowed* to
do — the tools you offered. The sequence it actually takes is not written anywhere until it
happens.

**Two identical runs can take different paths.** Same request, same data, different number
of steps and a different order. Chapter 13 explains where that variation comes from; here it
is enough to know the path is not repeatable.

**A mistake on step 2 is still being acted on at step 9.** This one deserves its own
section.

## Compounding

A single model call is usually right. A sequence of them is a different question, and the
arithmetic is unkind.

Suppose each step is right nine times out of ten — which would be a good model on a
well-chosen task. Then a run of several steps succeeds only if *every* step was right:

```text
  steps     chance the whole run is right
      1     0.900
      3     0.729
      5     0.590
      7     0.478
     10     0.349
     20     0.122
```

**Seven steps is where nine-in-ten per step becomes worse than a coin toss.** At twenty
steps it is one run in eight.

Now the same table for a step that is right ninety-nine times in a hundred:

```text
  steps     chance the whole run is right
     10     0.904
     20     0.818
```

The difference between those two tables is the whole argument for everything in Part II
about measurement. A per-step improvement that looks marginal — 0.9 to 0.99 — is the
difference between a system that fails most long runs and one that mostly completes them.

> **Note:** That table assumes a wrong step sinks the run. Real agents sometimes notice and
> recover — a failed search retried with better words, a tool error read and worked around —
> so the true numbers are better than the table. The *shape* is not: whatever the per-step
> figure is, multiplying it by itself enough times takes it to the floor.

> **Warning:** Two things make it worse than the table suggests, though. A wrong step does not
> just fail, it produces a *result*, and that result goes into the next step as though it
> were true. And a model that has already committed to a plan tends to keep going rather
> than reconsider. So errors do not only accumulate — they get built on.

This is also why "it worked when I tried it" is such weak evidence for an agent. One
successful run out of a distribution that succeeds a third of the time is not surprising;
it is expected, one time in three.

## Stopping

A loop needs a reason to end. An agent has three, and you need all of them:

| Ends when | Why you need it |
|---|---|
| The model says it is done | The normal case |
| A step limit is reached | The model may never say it is done |
| Something your code refuses | A loop heading somewhere it should not go |

The **stopping condition** is the set of rules that end the run. The step limit is the one
beginners leave out, and leaving it out is how you discover that a model asked the same
question forty times while the bill ran.

> **Tip:** Set the step limit at something you have a reason for, and log every run that
> hits it. A run that hits the limit is not a failure to be retried. It is a task the
> system did not know how to finish, and the record of what it tried is worth more than the
> answer would have been.

## How Much Freedom Real Systems Give

Here is where the word *agent* and the practice part company.

One study of agents deployed in production — twenty case studies and a survey of
eighty-six practitioners — found that **68% ran at most ten steps before a person
intervened**. Most also used ordinary models with careful instructions rather than
anything trained for the job, and most were judged mainly by people looking at the output.

> **Note:** That is one study, and one study is not a settled fact. Treat the shape as
> informative and the exact figures as indicative. The shape is what matters here: deployed
> agents are kept on short runs with a person close by, which is the opposite of the
> picture the word suggests.

The reason is in the table above. Ten steps at nine-in-ten is a run that works a third of
the time. Shortening the leash is not timidity, it is arithmetic.

## Freedom Is a Dial, Not a Switch

"Is it an agent?" is the wrong question, because the interesting systems sit between the
two ends.

| How much the model decides | What it looks like |
|---|---|
| Nothing | Your code calls the model once, in a place you chose |
| Which of a few things to do next | Your code offers a short menu; the model picks; your code runs the step |
| How many steps, and in what order | The model runs the loop until it stops |

Real systems mix these. A fixed path for the part you understand, a loop only for the part
that genuinely varies. Chapter 34 names the arrangements in the middle of that table and
says when each is worth it; the point here is that the dial exists.

And the principle from Chapter 3 applies with full force. Every part you add removes one
failure and introduces another — and the loop is a part. It removes *having to know the
sequence in advance*, which is a real and sometimes impossible requirement. It introduces
a path you cannot predict, errors that compound, and a cost per task that is decided at run
time rather than written down — a step limit caps it, but only by cutting the work off.

**So: the least freedom that solves the problem.** Not because autonomy is dangerous in the
abstract, but because each extra step is multiplied into the number at the bottom of that
first table.

## Approval Points

An **approval point** is a step the loop cannot pass without a person. It is how Chapter
3's fourth gap is actually implemented, and it is usually one line in the code that decides
whether a tool call runs.

The practical design is almost always a threshold rather than a rule about kinds:

- Refunds under a small amount go through; over it, a person approves.
- Replies to routine questions send themselves; anything touching a complaint waits.
- A file can be read freely; writing one needs a confirmation.

What makes this work is that the agent **stops and waits** rather than asking and
continuing. A loop that proposes an action, is refused, and tries a slightly different
route to the same action has not been controlled — it has been inconvenienced.

> **Warning:** The approval point has to be in your code, not in the instructions. Telling
> the model *"always ask before refunding over £50"* is a request, and Chapter 1 established
> that you cannot rely on what comes back. Checking the amount before you run the refund is
> a guarantee.

## Lab: Watch a Loop

No code. You are looking for the loop from outside, and for where it is bounded.

**Step 1.** Use an AI feature that clearly does several things for one request — a coding
assistant that edits files and runs commands, a research tool that searches and then
summarises, an assistant that can use more than one app. Give it a task needing at least
three distinct actions.

*Expected result:* visible intermediate steps. Most such products show them, because
watching is the only way a user can tell it is still working.

**Step 2.** Count the steps. Then run a *similar but not identical* task and count again.

*Expected result:* different counts. If they are identical every time, you are probably
looking at a fixed path rather than a loop — which is a finding, not a failure.

**Step 3.** Find the stopping condition. Give it something open-ended enough that it should
run a long time, and watch for the limit — a message about running out of steps, a pause
asking whether to continue, or a stop with the task unfinished.

*Expected result:* some ceiling, stated or unstated. If you cannot find one, note what you
tried; "I could not reach it" is different from "there is none".

**Step 4.** Find an approval point. Ask for something consequential and watch whether it
stops and waits, asks and continues anyway, or simply does it.

*Expected result:* one of those three. The second is the interesting one: a product that
asks and proceeds regardless has an approval point in its instructions and not in its code.

**Step 5.** Make it fail early. Give it a task whose first step you know will go wrong — a
file that does not exist, a search with no results. Watch what it does on the next step.

*Expected result:* either a recovery, or a plan carried on as though the failed step had
worked. The second is compounding, visible.

## Summary, Key Terms, and Review Questions

### Summary

An **agent** is the same arrangement as before with one change: the model decides what
happens next, repeatedly, instead of your code deciding. Nothing is added; control flow
moves. That means you cannot read the program and know its sequence, two runs can differ,
and a mistake early is still being built on later. Compounding is the governing fact: at
nine-in-ten per step, seven steps is worse than a coin toss and twenty is one run in eight.
A loop needs a **stopping condition** — the model saying it is done, a step limit, and your
code refusing. Deployed systems are kept short and supervised, which one study puts at most
agents running ten steps or fewer before a person intervenes. Freedom is a dial, and the
right setting is the least that solves the problem.

### Key Terms

| Term | Meaning |
|---|---|
| **Agent** | A system in which the model decides what to do next, repeatedly, rather than your code deciding the sequence |
| **Step** | One pass through the loop: the model decides, something runs, the result comes back |
| **Stopping condition** | The set of rules that end a run — the model finishing, a step limit, or your code refusing |
| **Approval point** | A step the loop cannot pass without a person, enforced in your code rather than requested in the instructions |

### Review Questions

1. What exactly is added to a system to turn it into an agent, and what is taken away?
2. Each step of your agent is right 90% of the time. Your task needs ten steps. Roughly how often does a whole run succeed, and what does that tell you about demonstrations?
3. Give two reasons a step limit is not optional.
4. A colleague says their agent is safe because the instructions tell it to ask before deleting anything. What is wrong with that, and what would you do instead?
5. Why can two identical requests to the same agent take different numbers of steps?

### Review Answers

1. Nothing is added — no new component, no different model. What is taken away is your code's control of the sequence: the model decides what happens next, repeatedly, until a stopping condition is met.
2. About a third of the time — 0.9 to the tenth is 0.349. A demonstration that worked tells you almost nothing, because a system that succeeds a third of the time produces a successful run roughly every third attempt.
3. The model may never decide it is done, so without a limit the loop can run indefinitely and the bill with it. And a run that hits the limit is a signal worth recording: it marks a task the system could not finish.
4. The instruction is a request, not a guarantee — you cannot rely on what comes back, and nothing stops the model proposing the delete anyway. The approval point belongs in the code that decides whether the call runs, where refusing it is certain.
5. The model decides each step fresh, and its output is not repeatable. The same request can produce a different plan, a different order, and a different number of steps.

> **You understand this when** you can explain why a system that is right nine times out of
> ten per step is a bad bet over twenty steps.
