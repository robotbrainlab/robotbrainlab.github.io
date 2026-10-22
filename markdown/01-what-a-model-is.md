# What a Model Is, and What You Get From It

This chapter answers the question underneath every other question in this book: when an
engineer says they are "using a model", what exactly is in their hands? By the end you
will know what you get, what you choose, what you are charged for, what you wait for, and
the one thing you do not control at all.

*The problem.* Everyone talks about "using AI" and I picture training something. I have no
idea what you actually get, or how.

*The question.* What is the thing an engineer actually holds, and what can it do?

## The Short Answer

A **model** is a service. Your program sends it some text. It sends some text back. You
are charged for the amount of text that moves in both directions, and you wait: a
noticeable pause before the first word, and longer still for a long reply.

That is the whole of it. Everything else in this book is about what you send, what you do
with what comes back, and how you find out whether any of it was any good.

The sentence is worth reading twice, because it contradicts the picture most people start
with. You do not download a brain. You do not teach it your business. You do not own it.
You make a request over a network to a program running on somebody else's machine, in the
same way your application might request a currency rate or a map tile.

> **Note:** "A service you call" describes how most applications use a model, not all of
> them. You can run a model on hardware you control, and some teams do. That changes who
> pays the electricity bill and who is woken at night; it does not change the shape of the
> exchange, which is still text in, text out. This book teaches the common case and says
> where the other one differs.

## Using Is Not Training

Two completely different activities get called "doing AI", and confusing them is the most
common beginner's error in this field.

**Training** is the process that produced the model. It consumed an enormous amount of
text and an enormous amount of computation, it happened once, it was done by a large
organisation, and it finished before you ever heard of the result. What it produced is a
very large collection of numbers.

**Inference** is what you do. You send text to the finished model and it computes a reply.
Nothing is learned: the numbers do not change because you called it, so the model itself
carries nothing from one call to the next. Products that appear to remember you, store your
earlier messages and send them again with the next request. The memory is in the product.
It is never in the model.

| | Training | Inference |
|---|---|---|
| Who does it | A handful of large organisations | You, on every request |
| How often | Once, over weeks or months | As often as your application runs |
| What changes | The model's numbers | Nothing |
| What you need | Thousands of specialised processors | A network connection |

The model you call was trained once and its numbers are now fixed. Two things are true of
it, and the second surprises people.

The first: it will not get better at your task overnight. A weakness you find today is
still there tomorrow — unless the provider swaps the model underneath you, and more on
that in a moment.

The second: it will not repeat itself exactly either. Two identical requests usually come
back worded differently. That has nothing to do with the numbers being fixed. It comes
from the way a reply is produced — one piece at a time, with an element of chance at each
step. Chapter 13 shows where the chance enters and what it means for testing anything.

Providers do replace models underneath you, and a replacement can change behaviour without
warning. Pinning a version is how teams stop that happening silently, and Chapter 54
shows how.

> **Tip:** When you read a claim about "AI", ask which activity it describes. "We trained
> a model on our documents" and "we sent our documents to a model" are different sentences
> with different costs, different risks and different failure modes. A surprising amount of
> confused writing comes from using the first to describe the second.

A model trained once on general material, then pointed at many tasks it was never
specifically built for, is called a **foundation model**. The name tells you its intended
use: it is a foundation you build on, not a finished product.

There is a third activity — continuing a finished model's training on examples of your own
— and it is a real option with real costs. It is the last lever to reach for rather than
the first, and Chapter 39 is where it is taught. Until then, assume the model is fixed.

## The Exchange

Strip away the libraries and a request looks like this.

You send:

- **Instructions.** What you want done, in words.
- **The input.** The thing you want it done to.
- **Settings.** A small number of switches that change how the reply is produced — how
  adventurous the wording is allowed to be, how long the reply may run. Chapter 13 teaches
  them.

You get back:

- **Generated text.** Which may be prose, or a list, or something structured that your
  code can read.
- **An accounting of how much text moved**, which is what you are billed on.

Here is one exchange with the three parts of the request marked. The settings are not
shown, because they travel beside the text rather than in it, and the accounting comes
back with the reply. Nothing here is special to any provider.

```text
WHAT YOUR PROGRAM SENDS
  instructions
    You are a support assistant. Answer in two sentences.
    If the answer is not in the notes below, say you do not know.
  added material
    Order 4471 shipped on Tuesday by courier. Tracking KP-9930.
  the request
    Has my order gone out yet?

WHAT COMES BACK
    Yes — order 4471 shipped on Tuesday by courier.
    You can track it with the reference KP-9930.
```

Two things in that exchange are worth marking, because the rest of Part I grows out of
them. The model had never heard of order 4471. It answered because the order's details
were put there by somebody's code, in the request itself. And the instruction *"say you do
not know"* is in there because, left alone, the model would have answered anyway.

That is the whole interface. There is no query language to learn, nothing to configure, no
index to build. The absence is disorienting at first. Most components you call accept only
the requests they were built for and refuse everything else, so the limit on what you can
ask is obvious, and the answer, when it comes, is the right kind of thing. A model's
interface sets no such limit: you can ask it anything, and it will almost always produce
something that looks like an answer. Your difficulty moves somewhere else entirely — to
finding out whether what came back is right.

> **Note:** The amount of text is not measured in words or characters. It has its own unit
> with its own rules, and those rules explain several things that look like bugs. Chapter
> 10 defines it properly. Until then, "the amount of text" is accurate enough.

## What It Knows

A model's knowledge came from the text it was trained on. That gives you three facts with
real consequences.

**It knows a great deal, generally.** Common knowledge, how language works, how code is
usually written, how documents are usually shaped. This breadth is what makes a foundation
model useful on a task nobody prepared it for.

**Its knowledge stops at a date.** Training consumed text gathered up to some point and no
further. That point is the model's **training cut-off**. Anything after that point is absent
— not wrong, absent. The model has no way of
knowing that it is missing something, which is why it will often answer a question about
last week with the confidence it uses for a question about last century.

**It has not seen your private material.** Your internal documents, your database, your
customer's order history were not in the training text. Anything of yours that was
published openly may well have been — but you cannot build on that, because the model may
hold a distorted memory of an old version and has no way to fetch the current one.

And the model itself cannot look anything up. It computes a reply from what you sent and
what it absorbed in training, and from nothing else. Products that search the web or read
your files do it with machinery around the model, which is what Chapter 2 is about.

> **Warning:** A model will answer a question about your data as readily as any other
> question. It does not say "I have no access to that." It produces something plausible,
> because producing something plausible is what it does. Chapter 16 explains why this is
> the design working as intended rather than a defect.

This has a practical corollary that will shape most of your work. **If you want the model
to use information, you have to put that information in the request.** Not in a
configuration file, not in a database it connects to — in the text you send, on that call.
Chapter 2 is about the machinery that gets built to do this well.

## What You Choose, and What You Do Not

| You choose | You do not choose |
|---|---|
| Which model to call | What that model knows |
| What text you send it | How it was trained |
| The settings on the call | What it will say to a given request |
| What your code does with the reply | Whether the provider changes it next month |

The right-hand column is uncomfortable and it is worth sitting with. A model is a
component whose behaviour you influence but do not specify. You cannot read its rules,
because it has none written down. You cannot patch it. When it does something you do not
want, your options are to change what you send, change which model you call, or put a
check around the result and handle the bad cases.

Nearly all of the engineering in this book lives in those three options, and most of it
lives in the third.

## What It Costs

You are charged for the text you send *and* the text you get back, usually at different
rates, with the reply costing more. Providers quote the price per large block of text, so
a single request costs a tiny fraction of a currency unit and the number looks like
nothing at all.

It stops looking like nothing when you multiply it. Two habits make the bill, and both are
invisible on a single call:

- **A long request, sent many times.** If you attach a page of instructions to every
  request, you pay for that page on every request, for the lifetime of the feature.
- **A long reply.** Replies cost more than requests, and a model asked an open question
  will happily produce six paragraphs where one would have done.

Here is the shape of the arithmetic, with made-up rates to show the mechanism rather than
any real price. Say text you send costs 1 unit per million words, and text you get back
costs 4 — the reply is dearer, as it usually is.

A feature sends 500 words of instructions and a 500-word document, and gets back a
200-word summary. That is 1,000 words in and 200 out:

```text
  in    1,000 words  x 1 unit per million  =  0.0010 units
  out     200 words  x 4 units per million =  0.0008 units
                                      per call  0.0018 units
  x 10,000 calls a day                          18 units a day
  x 30 days                                    540 units a month
```

Now add half a page of standing instructions — 250 more words — to every request. The
input goes from 1,000 words to 1,250, so the call costs 0.00125 + 0.0008 = 0.00205 units:
20.5 a day, about 615 a month.

The feature has not changed and no user has noticed. The bill is up about 14 per cent, for
as long as the feature exists. Note what did *not* happen: the input grew by a quarter and
the bill grew by a seventh, because the dearer half of the exchange is the reply. **Which
half of
the exchange you are growing decides how much a change costs you.**

> **Note:** Every price in this field changes, and the cheap model of this year is the
> expensive one of next. The arithmetic above is durable. The numbers are not, which is
> why this book gives you the first and almost never the second.

Chapter 53 takes cost seriously, with the levers that actually move it. For now, carry one
idea: **cost scales with the text you move, so the length of what you send is an
engineering decision and not a matter of taste.**

## What You Wait For

A model does not reply instantly. That delay is its **latency**. It is long enough to
feel, and it behaves differently from the delays you are used to.

A database query is mostly over when it is over. A model's reply arrives in two distinct
phases, and you experience them separately:

1. **The wait before anything appears.** The model has to read everything you sent before
   it can produce a single word. Send more, wait longer.
2. **The pace of the words after that.** The reply is produced a piece at a time, in
   order, and arrives as a stream. A long reply therefore takes longer than a short one —
   not because it is harder, but because there is more of it to produce.

This is why interfaces built on models show text appearing progressively. It is not a
visual effect. It is the shape of the underlying process, exposed to the user because
hiding it would mean waiting for the whole reply before showing anything.

> **Tip:** Two systems with the same total response time can feel completely different. One
> that shows its first word quickly and then types steadily feels responsive. One that
> shows nothing and then delivers everything at once feels broken, even when it finishes
> first. Which of the two phases you optimise is a product decision before it is a
> technical one.

Chapter 15 explains why the two phases exist and what they cost; Chapter 52 is about
measuring and reducing them. Here, the point is smaller: **latency is a property you design
around, not a number you can ignore.**

## Why "It Is a Service" Is the Useful Picture

Hold the model as a component with four properties: it takes text, it returns text, it
charges by the amount, and it takes a moment. Everything in the rest of Part I follows from
treating it that way.

A component that cannot see your data needs something to fetch that data. A component that
cannot act in the world needs something to act for it. A component that cannot reliably
check itself needs something to check it. And a component that is not accountable for what
it does needs somebody who is, wherever the consequences are serious.

Four gaps, and the next chapter is the five parts that get built around them.

## Lab: What Is This Thing Made Of?

No code. This lab trains the habit the rest of the book depends on: looking at an AI
product and seeing its parts instead of its demonstration.

**Step 1.** Find three AI features you can actually use. A coding assistant, a search box
that answers in sentences, a support chat, a summarising button in an application you
already have. Use each one twice.

*Expected result:* three products in front of you, used, not read about.

**Step 2.** For each, write one line saying what text you think was sent on your behalf.
Your typed request is part of it. What else must have been included for the answer to come
out as it did — a page of yours, a document, an earlier message in the conversation?

*Expected result:* at least one product where the answer clearly used information you
never typed. That information was put into the request by somebody's code.

**Step 3.** For each, note which of the two waits you felt: a pause before anything
appeared, a steady stream of words, or both.

*Expected result:* you can name the phases in a product you used today.

**Step 4.** For each, write down what evidence you were given that the feature works.
Count a measured claim and a demonstration as different things.

*Expected result:* mostly demonstrations. This is the normal answer, and it is the reason
a later part of this book spends so long on measurement.

**Step 5.** Ask one of them a question about something that happened in the last few days,
and one about your own private information.

*Expected result:* one of three things, and all three are worth having. A confident answer
that cannot possibly be grounded in anything the model knows — keep it, it is the most
useful thing in this lab. Or a correct answer, which means it did not come from the model
at all: something fetched it and put it in the request, and that is Chapter 2. Or a
refusal — "I cannot browse the web", "I have no access to your account" — which is the
product telling you where its boundary is.

## Summary, Key Terms, and Review Questions

### Summary

A model is a service: text in, text out, charged by the amount, answered in a noticeable
pause before the first word and longer for a long reply. It was trained once by somebody
else and is fixed while you use it.
It knows a great deal in general, knows nothing after its training cut-off, and knows
nothing of yours — and it will not tell you when it is out of its depth. You choose the
model, the text you send, the settings and what your code does with the reply. You do not
choose what it knows or how it behaves. Cost grows with the text you move; the wait has two
phases, one before the first word and one that paces the rest.

### Key Terms

| Term | Meaning |
|---|---|
| **Model** | A service that takes text and returns generated text, charged by the amount of text |
| **Training** | The one-time process that produced the model's numbers. Not something you do on a request |
| **Inference** | Running a finished model to get a reply. This is what "using a model" means |
| **Foundation model** | A model trained once on general material, then used for many tasks it was not specifically built for |
| **Training cut-off** | The point in time after which no text reached the model's training. It knows nothing later, and cannot tell that it does not |
| **Latency** | The delay between sending a request and receiving the reply, felt as a wait before the first word and a pace after it |

### Review Questions

1. A colleague says "we trained the model on our support tickets". What two different things
could they mean, and how would the costs differ?
2. You ask a model about an event from last week and get a confident, detailed answer. Give
two reasons the answer might be worthless.
3. Your feature sends half a page of standing instructions with every request. The feature
is unchanged for six months. What happens to its cost, and what decides how much it costs
you?
4. Why does a long reply take longer to arrive than a short one, even on the same model?
5. Name the one thing in the exchange you do not control, and the three options you have
when the model does something you do not want.

### Review Answers

1. They may mean **inference** — sending ticket text in each request, which costs per call
and changes nothing permanently. Or they may mean continuing the model's **training** on
those tickets, which is a one-off project with its own costs and leaves them owning a model
they must maintain. Chapter 39 covers the second.
2. The event may fall after the model's training cut-off, so it cannot know about it; and
the model has no way to signal that it is missing information, so it produces something
plausible instead of refusing.
3. You pay for that page on every single call, for six months. How much it adds depends on
which half of the exchange it grows: input is the cheaper half, so a page that grows the
input by a quarter raises the bill by less than a quarter — in the worked example, a quarter
more input gave about a seventh more bill.
4. The reply is produced a piece at a time, in order. More pieces take more time. The length
of the reply, not its difficulty, sets that part of the wait.
5. You do not control what the model knows or how it behaves. Your three options are: change
what you send, change which model you call, or check the reply and handle the bad cases.

> **You understand this when** you can explain to someone why a model cannot answer a
> question about your own documents unless you put those documents in the request.
