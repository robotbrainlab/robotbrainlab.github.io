# The Parts Around the Model

Chapter 1 left the model as a component: text in, text out, charged by the amount. This
chapter puts the five things that get built around it on the table and says what each one
is for. By the end you will be able to look at an AI feature and name its parts, which is
the habit the whole of Part I is training.

*The problem.* The model is one box. Everything I read draws five more boxes around it and
I can't see why any of them are there.

*The question.* What are the other parts, and what does each one do?

## The Cast

Here is the whole cast. Five parts, and the model in the middle of them.

```text
            +-------------------------------------------+
            |                 CONTEXT                   |
            |   instructions · added material · request |
            +----------^----------+---------------------+
                       |          |
     RETRIEVAL --------+          |
     fills in the added material  |
                                  v
                            +-----------+
            TOOLS <-------->|   MODEL   |
      actions it may call   +-----------+
                                  |
                                  v
                              CHECKS
                     verify before anything is used
                                  |
                                  v
                              PEOPLE
                    approve what matters, own the result
```

Chapter 1 ended on four gaps: the model does not know your data, cannot act in the world,
cannot reliably check itself, and is not accountable. Four of the parts above answer one
gap each — retrieval, tools, checks, people, in that order. The fifth, the context, answers
no gap. It is the thing you hand over, and the other four exist to fill it, to act on what
comes back, or to decide whether any of it may be used.

**Chapter 3 is the argument for why those four gaps are real**, and what each part costs
you in return. This chapter is the tour: what each one is, what it is for, and what it
looks like when it is there.

## Context: Everything You Send

Chapter 1 showed one request going out, with three labelled pieces: the instructions, the
added material and the request itself. Those three pieces together have a name. They are
the **context** — the settings from Chapter 1 are not part of it, because they travel
beside the text rather than in it — everything the model gets on this call, assembled
by your code and sent together.

| Piece | What it is | Who writes it |
|---|---|---|
| Instructions | What to do, how to behave, what to refuse | You, usually once, and they ship with every call |
| Added material | Facts this particular answer needs | Your code, freshly, for this call |
| The request | What the user actually asked | The user |

Three things about the context are worth fixing in your mind now, because almost every
later decision in this book is a decision about one of them.

**The context is assembled fresh on every call.** There is no session the model keeps for
you. If a conversation is to continue, the earlier turns are part of what gets sent again.
If a document is to be discussed, the document goes in. Chapter 1 put it as a corollary;
here it is as a design rule: *what is not in the context does not exist.*

**The context is where the money is.** Chapter 1 established that cost grows with the text
you move. What this chapter adds is *where that text lives*: almost all of it is the
context. That turns the size of the context into an engineering decision rather than a
detail, and Chapter 53 is where it becomes a budget.

**The context has a ceiling.** There is a limit on how much text a model will accept in
one call. It is large, and it is not infinite, and real systems hit it. What to do when
more material is relevant than will fit is a genuine engineering problem, and Chapters 28
and 35 are two different answers to it.

> **Note:** You will see the word *prompt* used for all of this, for the instructions
> alone, and for what the user typed. The word is used three ways and the ambiguity is
> genuine, so this book says **context** when it means everything sent, and says
> *instructions* or *the request* when it means one piece.

## Retrieval: Finding the Material

The added material row above says "your code, freshly, for this call". **Retrieval** is the
machinery that does the finding: given a request, search your own material and return the
passages that bear on it, so they can go into the context.

The shape is usually this, whatever the implementation.

1. Something arrives — a question, a ticket, a document to process.
2. Your code searches a collection you control: documents, records, past conversations.
3. The best few passages come back.
4. Those passages are put into the context, with the request.
5. The model answers from what it was given.

Not every system runs those steps in that order — some let the model ask for the search
itself, once it has seen the question — but the job being done is the same one.

Chapter 1's support example is a retrieval system with the retrieval taken out. The line
`Order 4471 shipped on Tuesday by courier` did not come from the model and did not come
from the user. Something looked up order 4471 and put that line in. That something is
retrieval, even when it is a single database query.

> **Tip:** "Retrieval" in this field usually brings to mind searching by meaning rather
> than by keyword, and Chapters 24 to 26 are about that. But a plain database lookup that
> puts a row into the context is doing the same job in the same place. The part is defined
> by where it sits, not by how clever it is.

What retrieval is *for* is narrow and worth stating exactly: it supplies facts the model does
not hold. It does not make the model cleverer, and it cannot fix an
answer that was badly reasoned. What it changes is what the model knows at the moment it
answers — not how well it reasons about it.

## Tools: Letting It Act

A **tool** is an action you allow the model to ask for. Looking up an order. Checking stock.
Sending a message. Running a search. Creating a ticket.

The sentence that matters is this one, and it is the whole of tools in Part I:

> **The model proposes. Your code decides.**

The model itself never reaches out and does anything. It produces a request — *call `refund` with
order 4471 and amount 30* — and that request is text like any other text it produces. Your
code receives it, decides whether to honour it, runs the actual function if it does, and
puts the result back into the context so the model can carry on.

| | What it does | What it does not do |
|---|---|---|
| The model | Asks for a tool, with arguments | Run anything |
| Your code | Defines which tools exist, validates the request, runs it, returns the result | Write the request itself |

Both of them decide something, and the two decisions are different. The model decides
*that* a tool is wanted. Your code decides *whether that happens*. Your code can also
decide the first one — calling a tool itself, or insisting the model use a particular one —
but the model can never decide the second.

Two consequences follow immediately, and both come back later with force.

**You decide what exists.** The model can only use tools you described to it. It may well
ask for something you never offered — a plausible-sounding function that does not exist —
and your code refuses it, because there is nothing there to run.

**You decide what each tool may reach.** A tool that cannot touch a system cannot damage
that system, so what each one is allowed to do is a decision you make once, in your code.

**You decide what happens on the day.** A proposed call is a suggestion arriving in text. It can be
wrong, it can have nonsense arguments, and it can be there because something the model
read told it to ask — which is Chapter 51, and is as alarming as it sounds. Validating it
is your code's job, not the model's.

How the proposal is expressed and handled in practice is Chapter 23. What makes a tool one
the model uses well is Chapter 36.

## Checks: Finding Out Before the User Does

A **check** is anything that verifies the output before it is used. Chapter 1 established
that you cannot predict what the model will produce. A check is what you do about that.

By *shape*, start with something concrete: your code expects an answer and a price it can
do arithmetic with, and what came back is a friendly paragraph with the price written out
in words. A shape check is what notices. Chapter 21 is how you ask for one properly.

Checks come in a range, from cheap and certain to expensive and approximate:

| Check | Catches | Cost |
|---|---|---|
| Does it fit the required shape? | Output your code cannot read | Nothing, and it is certain |
| Does it pass a rule you can write? | A price below zero, a date in the past, a missing citation | Almost nothing |
| Does a second model judge it acceptable? | Rudeness, irrelevance, an answer that ignored the material | A whole extra call, and it is approximate |

Below the bottom of that table there is a person. A person is not a fourth rung of
checking, though: they are the fifth part, and the next section is about them.

Work down that table in order. Anything a rule can decide should be decided by a rule,
because a rule costs nothing and gives the same verdict every time. Judgement is kept for what actually
needs judgement.

> **Warning:** A check that is itself a model call is not a referee standing outside the
> system. It is another component with the same properties as the first: you
> cannot predict what it will say, it can be wrong, and it has to be checked before it is
> trusted. Chapter 31 is
> entirely about how you earn the right to believe one.

There is a second half to checking that is easy to miss on the first pass. A check tells
you about *one* answer, now. Finding out whether the system is any good **in general** is a
different activity, with different machinery, and the book spends Chapters 30 to 33 on it.

## People: Who Actually Decides

The fifth part is **people**: the one engineers forget when they draw the diagram, and
the one every serious system has.

In most systems that do anything consequential, a person still reviews or approves the
cases that matter. Not every case — that would remove the point of building it — but the
ones where being wrong is expensive.

> **Note:** That "most" is current practice rather than a law, and the evidence behind it
> is thinner than it sounds: the figures people quote come from a small number of surveys
> of deployed systems. Treat it as what teams are doing now. The reason underneath it is
> the durable part, and it is next.

The usual arrangement is a threshold. Refunds under a small amount go through; larger ones
reach a queue. Routine replies send themselves; anything touching a complaint waits for a
human. The system does the volume, and a person owns the consequential tail.

The durable reason is not that models are not good enough yet. It is that somebody has to
be accountable for a decision that affects a customer, and accountability does not sit in
a component. How much a person is asked to approve will move as systems get better. That
there is a person who answers for the consequential cases is a different kind of claim. Chapter 3 makes
> that argument properly; Chapter 51 shows what goes wrong when the approval step is
> missing from a place that needed one.

## The Whole Thing Has a Name

A model with some arrangement of those parts around it is a **compound system**: several
components, each doing a job, with the model as one of them rather than as the product.

The name earns its place because it changes what questions you ask. "Is the model any
good?" is not answerable about a compound system, and it is not the question anybody
should be asking. The useful questions are about parts and joins:

- Did retrieval find the right material?
- Was the context assembled well?
- Did the model use what it was given?
- Did the checks catch what they should have?
- Did the right cases reach a person?

A system can fail at any one of those while every other part works perfectly. Telling them
apart is its own skill, and Chapter 5 is about how much of the real work it turns out to
be.

## The Same Small Cast, Arranged Differently

Look at AI products for a week and the five parts keep reappearing in different
proportions. The arrangement is the product; the parts barely change.

Every product here has a context, because a context is what you send — so the interesting
columns are the four that vary.

| Product | Retrieval | Tools | Checks | People |
|---|---|---|---|---|
| Answers questions about a company's documents | The whole point of it | Usually none | Is the answer supported by what was found? | Reviewed when a customer sees it |
| Writes a first draft inside an editor | The parts of your document near the cursor | Formatting, inserting | Mostly the human reading it | The author, always, by design |
| Triages incoming tickets | Similar past tickets | Tagging, routing, replying | A rule about when it may reply unaided | Anything it is unsure about |
| Writes and runs code | The repository | Read a file, write a file, run the tests | **The tests themselves** | A review before it merges |

The last row is worth a second look. Running the tests is both a tool and a check: the
model asks for it like any other action, and the result is the most trustworthy *automatic*
verdict here, because it is a rule and not an opinion — though only about what the tests
actually cover, and not at all if the model wrote them. Where a real, cheap, automatic verdict
exists, the system around the model gets simpler and much more reliable. Where none exists
— "is this summary good?" — everything gets harder. That difference will come up again and
again.

> **Tip:** When you meet a new AI product, do not ask which model it uses. Ask what it
> retrieves, what it is allowed to do, what it checks, and who approves. The answers tell
> you what it actually is. The model name tells you almost nothing.

## What This Chapter Has Not Told You

Deliberately, three things:

- **Why each part is necessary.** You have been told what each part is for. The argument
  that the model cannot do these jobs itself, and what each part costs you in return, is
  Chapter 3.
- **What happens when the model runs the loop itself.** Everything here has your code in
  charge: your code retrieves, your code decides whether a tool runs, your code applies the
  checks. Hand that decision to the model, repeatedly, and the arrangement gets a different
  name and a different set of problems. That is Chapter 4.
- **How any of the parts actually work.** Retrieval is Chapters 24 to 29. Tools are 23 and
  36. Checks are 21, 30 to 33. This was the tour.

## Lab: Name the Parts

No code. You did a version of this in Chapter 1's lab; this time you have the vocabulary.

**Step 1.** Take the three AI features you used for Chapter 1's lab. For each, fill in one
row: retrieval, tools, checks, people. Write *none* where you believe there is none, and
*unknown* where you cannot tell from outside.

*Expected result:* three rows, several *unknown* entries. Users cannot see checks, and that
is normal.

**Step 2.** For one of them, write down what you think the instructions say. You will not
be right, but try: what must the product have told the model about how to behave?

*Expected result:* at least one instruction you are confident about, usually a refusal —
something the product consistently will not do.

**Step 3.** Look for the ceiling. Give one of them far more material than it expects — a
long document, or a very long conversation — then ask it about something from well inside
that material.

*Expected result:* one of three. A refusal, which is the limit stated out loud. An answer
that has quietly lost part of what you gave it. Or no visible effect at all, which means
you have not reached the ceiling yet — modern limits are large. Which part gets lost, and
why long inputs are used unevenly, is Chapter 16.

**Step 4.** Find a place where a person must be in the loop. Ask one of them to do
something consequential and irreversible.

*Expected result:* a refusal, a confirmation step, or a handover to a human. If a product
does something irreversible with no confirmation, you have found a design decision worth
remembering.

**Step 5.** For each of the three, write the single sentence: *this product is a model plus
____.* Fill the blank with parts, not adjectives.

*Expected result:* three sentences that would tell another engineer how the product is
built.

## Summary, Key Terms, and Review Questions

### Summary

Five parts get built around the model. The **context** is everything you send on a call —
instructions, added material and the request — assembled fresh every time, limited in size,
and responsible for most of the cost. **Retrieval** finds the added material in your own
collection and supplies facts the model does not hold. **Tools** are actions the model may
ask for: it proposes, your code decides, runs and returns. **Checks** verify the output
before anybody uses it, from a shape the output must fit through to a person's judgement.
**People** approve the consequential cases and own the result. The whole arrangement is a
**compound system**, and once you see it as parts, "is the model any good?" stops being the
question.

### Key Terms

| Term | Meaning |
|---|---|
| **Context** | Everything sent to the model on one call: the instructions, any added material, and the request |
| **Retrieval** | Searching your own collection for the passages that bear on a request, so they can be put into the context |
| **Tool** | An action the model may ask for. The model proposes it; your code decides whether to run it |
| **Check** | Anything that verifies the output before it is used, from a required shape to a person's judgement |
| **People** | The reviewers and approvers who handle the consequential cases and carry responsibility for them |
| **Compound system** | A system of several parts with the model as one of them, rather than as the whole product |

### Review Questions

1. Your assistant answered correctly yesterday and cannot answer the same question today. Name two parts that could be responsible and say how you would tell them apart.
2. A colleague says their system "lets the model update the database". What is actually happening, and where is the decision made?
3. Why should a rule-based check run before a model-based one, when the model-based one catches more?
4. A product summarises documents and a product writes code. Which has the easier time checking its own output, and why?
5. You are shown a diagram with the model, the context, retrieval, tools and checks. Which part is missing, and what job does it do?

### Review Answers

1. **Retrieval** may have failed to find the material, or the **context** may have been assembled differently — a longer conversation pushing the useful part out, for instance. You tell them apart by looking at what was actually sent: if the right passage was in the context and the answer is still wrong, retrieval did its job and the problem is elsewhere.
2. The model is proposing a tool call, and their code is deciding whether to run it and then running it. The model updates nothing. The decision sits in their code, which is also where the validation has to be.
3. A rule costs nothing and gives the same verdict every time. A model-based check costs a whole extra call and is only approximate — it is a component with the same unpredictability as the first one. You spend judgement only on what needs judgement.
4. The code product. Running the tests is a real, cheap, automatic verdict, and it is a rule rather than an opinion. "Is this summary good?" has no equivalent, which is why everything around it is harder.
5. **People.** They approve the consequential cases and carry the responsibility for them, which is why the threshold for what reaches them is a design decision and not an afterthought.

> **You understand this when** you can look at any AI feature and say what it retrieves,
> what it is allowed to do, what it checks, and who approves.
