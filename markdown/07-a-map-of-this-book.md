# A Map of This Book

Six chapters in, you have the shape of a system and a way to read claims about it. This
chapter is the map: what the rest of the book contains, in what order, and what it leaves
out on purpose.

*The problem.* There's clearly a lot here. I don't know what order to learn it in, or what
I can safely leave until later.

*The question.* What is the shape of the whole thing, and which parts can wait?

## The Four Parts

| Part | Chapters | The question it answers | What to ignore while you are in it |
|---|---|---|---|
| **I · Understand** | 1–17 | What is this thing, and what is it made of? | Every setting, price and product name. This part is what the thing is, not how you drive it |
| **II · Use** | 18–39 | How do I make each part work, and how do I know it does? | Serving your own models, and the bill |
| **III · Apply** | 40–50 | Can I build the whole thing and measure it? | Scale and deployment. Everything runs on one machine |
| **IV · What Next** | 51–57 | What can go wrong, what makes it slow, what breaks, what it costs — and what I say out loud | Nothing. Chapter 57 is where the book says what to skip |

Part IV's first four chapters are *four threads* asked of the whole system: what can go
wrong and what limits the damage (51), what makes it slow (52), what it costs (53), and how
it breaks and how you diagnose that (54). Chapter 55 then designs a system out
loud, and 56 and 57 say what to learn next and what to leave.

The order is not arbitrary. Part II is unreadable without Part I's vocabulary; Part III is
a waste of time before Part II, because a lab you cannot measure teaches you nothing; and
Part IV asks questions — *what would you do about this failure?* — that only make sense once
you have built something.

## Why Part I Has Two Halves

Part I is in two halves, and both of them are *Understand*.

- **Mental Model**, chapters 1–7, is the half you have just read. It is the system *around*
  the model: what the model is as a component, what the other parts are for, why they are
  assembled that way, what an agent loop actually is, where the work goes, and how to read
  what you read. While you are in it, ignore what is *inside* the model — the second half
  opens it.
- **Inside the Model**, chapters 8–17, is the model itself: what it is made of, how text
  becomes numbers, how attention works with the arithmetic done by hand, what a stack of
  layers accumulates, how scores become a word, how it learned to do this, what it costs
  from the inside, and why it fails in the particular ways it does. While you are in it,
  ignore how the model was trained beyond the shape of that last loop.

Neither is a part of its own, because they answer the same question. The first says what the
model is *for*; the second says what it *does* when it answers. You can read Part II after
the first half alone, and you will understand every instruction in it. You will not
understand *why* any of them work until you have read the second.

> **Note:** The second half uses real notation and does the arithmetic. It does **not** teach
> machine-learning or deep-learning theory — no loss surfaces, no optimisers, no proofs.
> Chapter 8 gives you exactly the mathematics the book uses and nothing more, and Chapter 17
> marks the line where the theory you are skipping begins, so you know what you have skipped
> rather than not knowing it is there.

## The One System the Labs Build

Part III is eleven chapters that are each a single lab, and they are not eleven separate
exercises. They build **one small system**, each lab starting where the last one stopped.

| Labs | What gets built |
|---|---|
| 40–42 | A model call you can measure, an evaluation set with two prompts compared properly, and a fixed output shape your code can check, with one tool |
| 43–45 | Two ways of turning text into numbers, tested against each other; retrieval with a re-ordering step, measured; then the pipeline joined end to end |
| 46–48 | Failure modes named and a judge you can trust, a fixed path against a loop, and context and tools measured |
| 49–50 | Cost and latency measured and reduced, then an attack on the thing you just built |

Two design decisions are worth knowing before you get there.

**The book ships the data.** About forty short public-domain documents, eight queries with
a hand-made judgement of how
well each document answers each one, and one deliberately awkward PDF with a table and a
scanned page.
Every lab runs on those. No lab says "use your own documents", for the reason Chapter 6
would give you: an expected result that depends on the reader's files holds for nobody, so
you could never tell whether your run was right.

**Every step has an expected result.** Not exact output — Chapter 1 established that the
same request can come back differently — but the shape the output takes, or which assertion
must pass, or a range your number should fall in. Where a real run is shown, the book says
plainly that your numbers will differ.

> **Tip:** Labs are easy to skip, and reading about measuring something is not the same
> state of knowledge as having measured it. If you are short of time, do fewer labs
> properly rather than all of them quickly.

## Which Chapters Carry the Most Weight

This book is written for a particular situation: the one where you have to explain this
material out loud, to somebody who will notice a wrong answer. That is why some chapters
matter more than others, and it is worth saying plainly before the table below.

And here I have to be careful, because Chapter 6 just taught you to ask where a claim comes
from, and this one is a **judgement**, not a measurement. Nobody has surveyed what questions
get asked, and if they had, the answer would vary by company, role and year. What follows is
reasoning about which chapters the rest of the book leans on hardest — treat it as a
suggestion about reading order and not as a prediction.

| Weight | Chapters | Why |
|---|---|---|
| Heaviest | 1–7, 18, 20, 30–33 | Almost everything else refers back to them. The mental model, the prompt as a specification, and the ability to say how you would know something works — including whether a difference is real |
| Heavy | 23, 26, 28, 34, 51, 53, 54 | Tool calls, retrieval and its assembly, when a loop is warranted, security, cost, diagnosing a failure. The questions with a wrong answer somebody will notice |
| Depends on the role | 8–17, 19, 21–22, 29, 36–39, 52 | The model's internals, reliability engineering, output shapes, scale, tool design and agents, adaptation, speed. Which of these matters depends entirely on what the work is |
| Last, and worth it | 55 | One whole system designed out loud, which is the only chapter that rehearses saying the rest |

One related sentence is worth adding, because it answers a different question from the
table: **chapters 18 to 29 are the half of Part II a conversation reaches first** — calling
a model, and retrieval. They are where
the questions start, because they are the part of the system somebody can ask you to
describe without first agreeing what the system is.

Appendix B is a hundred questions with answers of 150 to 180 words each, which is about what
sixty seconds of speech holds. That length is the point: it is **interview depth** — the
mechanism, the trade-off, and how you would check it — and it is the depth this whole book
aims at. Not exhaustive, and not a summary either.

## What This Book Leaves Out, On Purpose

A book that admits what it skipped is more useful than one that implies it covered
everything.

| Left out | Why, and where it is |
|---|---|
| Machine-learning and deep-learning theory | It is a different subject and a longer book. Chapter 17 marks where it starts; Chapter 56 names the standard books |
| Training a model from scratch | It is outside what this book is for — building applications on models somebody else trained. Chapter 14 gives the shape of the loop and stops |
| Vendor comparisons and product tours | They are **dated detail** in Chapter 6's sense — wrong by spring. The book organises by capability and names no leader, so there is nowhere for it to date |
| Serving models at scale | Chapter 52 covers it as a lever you might pull, not as a thing you will operate |
| Everything an interview does not reach | Chapter 57 is the whole argument, including where to stop |

That last row is the important one, and it is the hardest thing in the book to act on. Every
prerequisite has a prerequisite. You can want to understand retrieval, so you read about
how text becomes numbers, which sends you to linear algebra, which sends you to proofs, and
a month later you have not built anything. **The regress has no natural bottom**, which means stopping is a
decision somebody has to make rather than a place you arrive at. Chapter 57 argues for where
to stop. Until then, the working rule is the one this book is built on: learn the thing you
are about to use, and let the layer underneath wait until something you cannot explain makes
you go down a level.

## How to Read It

| If you have | Read |
|---|---|
| Months | Straight through, labs included. The order is the argument |
| Weeks | Part I's first half, then 18 and 20, then 30–33, then labs 40 and 41, then 55. Add labs 43–45 if you can — lab 46 works on the outputs they produce, so it is not one you can jump straight to. Then the "heavy" row as time allows |
| Days | Chapters 1–7, Chapter 55, Appendix A (the cheat sheet) and Appendix B (the question bank). Accept that you will be answering from a mental model rather than from experience, and say so if asked |
| Already building something | Whichever chapter names the problem you have now. The book is written to be entered in the middle; every chapter says which chapter owns the concepts it leans on |

That last row needs one piece of machinery explained. Every concept in this book has one
**concept owner** — a single chapter that teaches it, with every other chapter referring to
it by number instead of re-teaching it. So when a chapter says "Chapter 28 owns this", that is not the book being
coy — it is telling you exactly where the full treatment is, and promising that you are not
going to meet three partial explanations of the same thing.

## Lab: Place Eight Questions

No code. Ten minutes. This one has a key, so you can check yourself.

Below are eight questions of the kind this book is preparing you for. For each, name the
part — **I**, **II**, **III** or **IV** — whose chapters answer it. You are not answering
the questions; you are placing them.

1. "Why does your system need a retrieval step at all?"
2. "Your answers got worse after a provider updated the model. What do you do?"
3. "How would you tell whether prompt A is better than prompt B?"
4. "What is actually inside the thing you are calling?"
5. "Walk me through building this and show me the numbers you got."
6. "What does one request cost, and what makes the bill grow faster than usage?"
7. "Why can't the model just check its own answer?"
8. "A web page tells your agent to email its data somewhere. What happens?"

*Expected result:* I for 1, 4 and 7 — each is a question about what the thing is and why it
is assembled that way. II for 3, because comparing two prompts properly is a method you
learn and not a thing you build once. III for 5, which is the only question that cannot be
answered without having done the labs. IV for 2, 6 and 8 — failure, cost and security are
all Part IV, and all three assume you have built something to break.

If you placed 7 in Part II, you were thinking of Chapters 31 and 32, which build the
checks — and that is a reasonable reading. Part I — Chapter 3 — is where the *reason* a
self-check is not independent lives, and the question as asked is a *why*.

If you placed 3 in Part III, look again: Part III *does* the comparison, but Chapter 20 is
where you learn whether a difference is real. The habit of separating *the method* from *the
exercise that uses it* is much of what separates Part II from Part III.

## Summary, Key Terms, and Review Questions

### Summary

The book is four parts: **Understand** (1–17, what this is and what it is made of),
**Use** (18–39, how to make each part work and know that it does), **Apply** (40–50, eleven
labs that build one small system in order, on data the book ships), and **What Next** (51–57,
what can go wrong, what makes it slow, what breaks, what it costs, and saying it out
loud). Part I has two halves — *Mental Model*,
the system around the model, and *Inside the Model*, the model itself — which are one part
because they answer the same question in two directions. Which chapters carry most weight is
a judgement and not a measurement, and it is offered as reading order rather than
prediction. The book deliberately omits machine-learning theory, training from scratch,
vendor comparisons and operating models at scale, and for each of those but the vendor
comparisons it marks where the subject begins,
because the regress of prerequisites has no natural bottom and stopping is a decision rather
than a destination. Every concept has one **concept owner**, so the book can be entered in the
middle.

### Key Terms

| Term | Meaning |
|---|---|
| **Interview depth** | Knowing something well enough to give the mechanism, the trade-off, and how you would check it, in about a minute of speech. Not exhaustive, and more than a summary |
| **Concept owner** | The single chapter that teaches a given concept. Every other chapter refers to it by number rather than re-teaching it, so the reader never meets three partial explanations of one thing |

### Review Questions

1. Why are *Mental Model* and *Inside the Model* two halves of one part rather than two parts?
2. Why does the book ship the data its labs use, instead of telling you to use your own documents?
3. The chapter ranks some chapters as carrying more weight than others. What kind of claim is that, and how should you treat it?
4. What does "the regress of prerequisites has no natural bottom" mean in practice, and what is the working rule it implies?
5. You have one week. What is the argument for reading Chapter 55 even though you will not have done most of the labs?

### Review Answers

1. Because they answer the same question from two directions: the first says what the model is *for* as a component in a system, the second says what it *does* when it answers. Part II is readable after the first half alone; the second half is what makes Part II's instructions make sense rather than merely usable.
2. Because an expected result that depends on the reader's files holds for nobody — you could run a lab correctly and have no way to tell. Shipped data means every step can state what you should see, so the lab can be checked rather than merely performed.
3. It is a judgement, not a measurement: nobody has surveyed what gets asked, and the answer would vary by company, role and year anyway. It is reasoning rather than reporting, so the honest label is the one the chapter gives it: a judgement. Treat it as a suggested reading order and not as a prediction about any particular conversation.
4. Every prerequisite has a prerequisite, so following them downwards never terminates on its own — you can go from retrieval to how text becomes numbers to linear algebra to proofs and build nothing. The working rule is to learn the thing you are about to use, and go down a level only when something you cannot explain forces you to.
5. Because Chapter 55 is the only chapter that rehearses *saying* the material, and that is a separate skill from knowing it. Having a structure for talking through a system — what you would clarify, what you would measure, what you would not build yet — is worth more in a short conversation than one more chapter of content you cannot yet organise.

> **You understand this when** you can say what each of the four parts answers, name which
> half of Part I you have just finished, and say what the book leaves out and where it says
> so.
