# What to Skip for Now

Chapter 7 said this chapter is the whole argument for what to leave out, and it is also the last
chapter of the book, which makes the two jobs the same one. Everything here claims to be
essential. Most of it is, to somebody.

*The problem.* Everything claims to be essential.

*The question.* What do I not learn, how do I know when that stops being true, and where does
going down a level end?

## The Answer, First

**Stopping is a decision somebody makes, not a place anybody arrives at.** That is Chapter 7's
sentence and this chapter is the argument for it, which comes in three parts and one rule.

| The three parts | What each gives you |
|---|---|
| What a conversation does not reach | A measurement, taken over this book's own hundred questions |
| What to postpone, and the trigger for each | A list where every row has a condition attached, so postponing is not forgetting |
| Where going down a level ends | The argument, and a threshold you can apply the same afternoon |

**And the rule, which is Chapter 7's and is the most useful sentence in this book to act on:**
learn the thing you are about to use, and let the layer underneath wait until something you
cannot explain makes you go down a level. What this chapter adds is the threshold — **go down
when you have hit the same wall twice, not once** — and the argument for why the rule needs one.

**The reason a threshold is needed at all is that the costs are not symmetric.** Going down a
level too early costs weeks and produces nothing you can show anybody. Going down too late costs
one confused afternoon and then you go down. A rule facing costs that lopsided should be biased
heavily towards staying where you are, and *once* is not a bias — it is the absence of one.

## What a Conversation Does Not Reach

This is the one part of the chapter that can be measured rather than argued, and the measurement is
of this book's own question bank: a hundred questions, each keyed to the chapter that teaches it,
and all but thirteen of them written from the plan before any chapter existed. **The thirteen are
the bank's own declared exception** — questions 1 to 13 cover Chapters 1 to 7 and were written by
somebody who had read them, which that page says outright, and a question reverse-engineered from
an answer cannot test whether the answer is there. Hold that against the first row of the table
below, where all thirteen of them sit. Count where they fall.

```text
  the hundred questions, by part

    part               questions   chapters
    I   (1-17)              35        17
    II  (18-39)             51        22
    III (40-50)              5        11
    IV  (51-57)              9         7

  and eight chapters carry none at all:
    7, 40, 42, 43, 44, 46, 48, 57
    - six of the eight are labs
```

**Eighty-six of the hundred are in Parts I and II**, which is the material you can be asked to
*explain*. The eleven labs of Part III are the largest body of work in the book — the real model
calls, the real corpus, the measurements almost everything in Part IV rests on — and they carry
five questions between them.

**That is not a flaw in the bank and it is the most useful fact in this chapter.** The bank's own
header says why: the labs are tested through the chapters they rest on, and the ones that do
appear are there to be *described* rather than explained. Lab 44 is examined by the retrieval
questions on Chapter 26; lab 46 by those on Chapters 30 and 31. So the labs are not unexamined.
They are examined *somewhere else*, and the thing being examined is not the lab.

**Which gives the asymmetry to hold on to, and it cuts both ways.** The work that makes you able
to answer is not the work you are answering about. Nobody will ask you to reproduce a bootstrap
interval over eight queries; they will ask whether a difference is real, and you will answer well
because you once did the former. **So do not study for the questions, and do not mistake the
questions for the point.** A candidate who has read Parts I and II and done no labs can answer
eighty-six of a hundred questions and will come apart on the first follow-up, because the
follow-up is always *how do you know*.

**And the practical reading of the table is narrower than it looks.** It says what *this* book's
author expected a conversation to reach, all but thirteen of it written before the chapters
existed. It is a judgement rather than a survey, exactly as Chapter 7 says of its own reading
plans, and the right use of it is as a prior rather than as a syllabus.

### What a Survey Says Instead

A survey does now exist, of a kind, and it disagrees with the table above in two places — which is
the most useful thing a second instrument can do. Fifty-four first-hand accounts of AI-engineer
interviews, dated 2025 and 2026, counted by theme:

```text
  what came up, in 54 accounts

    project deep-dive          22
    RAG and retrieval          21
    practical coding           25
    managerial or behavioural  21
    DSA                        14
    LLM theory                 14
    classical ML               10
    production                  9
    agents                      8
    system design               7
    evaluation                  5

  the counts overlap: one account reports several themes
```

**Read it as what it is.** These are self-selected reviews on public sites, which Chapter 6 calls
a practitioner report and says supports what people *do* far better than whether it works. The
counts are lower bounds, because a short review omits what it does not mention. And it is one
market in one year. It is a better instrument than the table above for *what gets asked* and a
worse one than anything in this book for whether a practice is any good.

**Then the two disagreements, and the first is uncomfortable.** **Evaluation came up in 5 of the
54.** This book spends seven chapters and four labs on it — Chapters 20 and 30 to 33, plus 41 and
46 — which is the largest single thread in it. So the emphasis cannot be justified by what is
*asked*, and it was never meant to be: the hiring-side accounts in the same study rank evaluation
first among the things that separate a strong candidate from an average one, which is a claim about
what *distinguishes* rather than about what is said out loud. **Both can be true, and holding both
is the point of this section.** The most-asked question is not the most-revealing one, which is
why the second thing an interviewer does is ask how you know.

**And the second disagreement is a hole in the bank rather than a difference of emphasis.**
Managerial and behavioural questions came up in 21 of the 54 — level with retrieval and just
behind the project — and **this book's hundred questions contain none of them.** That is not a
subject this book teaches and it is not going to become one. What the count says is narrower and
worth acting on: a fifth of what you will be asked is not in here, nobody can prepare it from a
technical book, and the sentence to carry is that the bank is an acceptance test for *this
material* rather than for an interview.

**One more thing the survey names**, and it is the cleanest illustration of what this chapter is
about. Four subjects come up in those accounts that this book does not teach: two of them are now
a paragraph each, because they are architecture and measurement rather than fashion and the book
was simply missing them. The other two — classical machine learning, and data-structures
problems — stay out, and Chapter 17 and the deferral table below say why. **A named refusal is the
whole of what this chapter has to offer**, and four of them from somebody else's evidence are
worth more than any number of mine.

## What to Postpone, and the Trigger for Each

A list of things not to learn is useless without the condition that ends each deferral, because
*later* with no trigger attached is how a deferral becomes a gap you forgot you chose. So every
row here has one.

| Postpone | Until |
|---|---|
| The theory behind Chapter 17's thirteen | You meet one of them twice — the next section is what that means — or you are about to tune a model, which Chapter 17 names as the one place its boundary genuinely bites. Chapter 56's order is what to read when one of those fires, or when you choose to read anyway; and for the three it says have no book, a second hit buys the research literature or Chapter 17's three-part answer and nothing else |
| Training a model from scratch | You are training one. Chapter 7 puts it among what this book leaves out and Chapter 14 gives the shape of the loop and stops, which is what a conversation reaches |
| Operating a serving stack | You have the traffic and the people. Chapter 52 names the four self-hosting levers and says plainly that self-hosting is a decision about traffic, people and operations rather than about latency |
| The other kinds of model, and classical machine learning | A job asks for them. Chapter 17 lists them as outside this book *without* being gaps in it, because they are other kinds of model rather than parts of this one — which is why no amount of this book makes them nearer |
| Collections of prompting techniques | Something you write stops working and you cannot say why. Chapter 18 owns the prompt as a specification, which is the durable half; a catalogue of tricks is Chapter 6's *dated detail* with a longer shelf life than most |
| Model and vendor comparisons | You are choosing one — and then you do not read the comparison, you run Chapter 43's measurement or Chapter 49's on your own data, because Chapter 24's own bank question is why a public benchmark is a starting point rather than a verdict |

**Two things about that table are worth saying out loud.** The first is that none of the six is on
it because it is unimportant — four of the six are somebody's whole career. They are on it because
nothing you do in the next year depends on them, and a thing you will not use is a thing you will
not retain.

**The second is that every one of the six triggers is an event rather than a date.** *Until you are
training one.* *Until something stops working.* *Until a job asks.* That is deliberate, and it is
the difference between a deferral and a vague intention: an event arrives and tells you, where a
date arrives and you move it. The first row is the one that carries a *count* as well — meet one of
them twice — and the next section is why it needs one.

## The Regress, and Where to Stop

Chapter 7 names the problem in one sentence: every prerequisite has a prerequisite, and **the
regress has no natural bottom.** It is worth seeing how fast it runs, because the descent is
steeper than it feels while you are making it.

You want to understand why the embedding geometry carries meaning, which Chapter 17 tells you is
representation learning. That sends you to how models are fitted, which sends you to
optimisation, which sends you to multivariable calculus and to probability, which send you to
analysis and measure theory — and those have prerequisites of their own. **Four levels down from
a question about retrieval you are reading about measure-theoretic probability**, and you have
not yet got back anything you can use on the question you started with.

**And the regress is wider than it is deep, which is the part that surprises people.** Chapter
17's list is thirteen items, and each has its own descent. Going down one level *below* the
thirteen is not one book — Chapter 56's books sit at the level of the thirteen rather than
underneath them — and
it is thirteen descents that share some of their lower levels and not all of them. There is no single floor under this material, which is precisely why nobody arrives
at the bottom and announces it.

So the rule has to come from the costs rather than from the subject, and the costs are lopsided.

| Going down | Costs | Produces |
|---|---|---|
| Too early | Weeks, and the thing you were building | Nothing you can show anybody, because you stopped |
| Too late | One confused afternoon | The descent, now with a reason attached |

**Which is the whole argument for the threshold: hit the same wall twice.** The first time you
cannot explain something, the likeliest cause is not a missing layer underneath — it is that the
explanation you read was bad, or that you read it too quickly, or that you are missing one fact
at the level you are already on. Go and find a second explanation at the *same* level first. That
costs an hour. If you hit the same wall again, from a different direction, with a better source,
then the level is the problem and the descent has a reason — and now you know what you are going
down *for*, which is the thing that makes it finish.

**The second hit is also what makes the trip short**, which is the part worth being concrete
about. Somebody who goes down because they are curious reads a book. Somebody who goes down
because the same wall stopped them twice reads the three sections that are about their wall, gets
the thing they came for, and comes back up. **A descent with a question in it terminates. A
descent without one is a syllabus.**

**And there is one honest exception, which Chapter 17 names itself.** If you are going to do the
thing, the level below is not optional: *if you ever do your own fine-tuning, you will be
choosing a step size.* The rule is about postponing theory you are not using, and the moment you
use it the deferral is over. That is the same shape as the trigger table above — an event, not a
judgement — and it is why the two sections are one argument.

## What This Chapter Has Not Told You

Four things, deliberately.

**What to learn.** That is Chapter 56, and the two chapters are one argument read from opposite
ends: it says which five books and in what order, and this one says what the order is allowed to
leave out and for how long. Neither is useful without the other, and the overlap between them is
meant to be nothing.

**Whether any of it is worth learning.** Every row of the deferral table is somebody's subject and
several are somebody's life's work. A judgement about what fits in the time you have is not a
judgement about what is worth knowing, which is Chapter 17's own wording and holds here with
nothing added.

**What a particular conversation will reach.** The measurement in the second section is over this
book's own hundred questions, all but thirteen of which were written from a plan by one person
before any chapter existed. Chapter 7 says the same of its reading plans: it is a judgement rather than a survey,
nobody has counted what gets asked, and the answer would vary by company, role and year. Use it as a
prior.

**And when to stop deferring something nothing has triggered.** The table's conditions are events,
and an event that never happens leaves a row deferred for ever. That is usually the correct
outcome and occasionally it is not, and no rule on this page tells you which — the honest version
is that you should re-read the table once a year and ask whether anything on it has quietly become
your job.

## What You Can Do Now

Not a summary of the book, which is what Chapter 7 is for, but the shape of what fifty-seven
chapters were for.

You can say what a model is as a component and what it costs you. You can compute an attention
row by hand, say what a key–value cache costs at eight thousand tokens, and name the thirteen
things you cannot explain. You can write an evaluation set, put an interval round a difference, and
say which differences a set that size cannot see. You can build a retrieval pipeline, measure
each stage separately, and say which of its stages is not paying for itself. You can read a bill
and say where it went, say which of four complaints *slow* is before reaching for a lever, attack
your own system and say what the attack did and did not establish, and run a provider's model
update against your own suite before it runs against your users. And
you can say all of it out loud in forty-five minutes, in the order that conversation rewards,
with a number or a named check behind every claim.

**What you cannot do is anything on this chapter's deferral table, and you can name all of it.**
That is the position the book was written to put you in, and it is a better one than it sounds,
because the alternative on offer was never *knowing everything*. It was not knowing which was
which.

## Summary and Key Terms

### Summary

Stopping is a decision somebody makes rather than a place anybody arrives at, which is Chapter 7's
sentence, and this chapter is its argument in three parts. **What a conversation reaches can be
measured** on this book's own hundred questions: 35 fall in Part I, 51 in Part II, **5 in the
eleven labs of Part III** and 9 in Part IV, with eight chapters carrying none and six of those
eight being labs. That is not a flaw in the bank — the labs are examined through the chapters they
rest on, which the bank says itself — and it is the most useful asymmetry in the chapter: **the
work that makes you able to answer is not the work you are answering about**, so do not study for
the questions and do not mistake them for the point, because the follow-up is always *how do you
know*. **Then six things to postpone, each with the condition that ends the deferral**, because
*later* with no trigger is how a deferral becomes a gap you forgot you chose: the theory behind
Chapter 17's thirteen, training a model from scratch, operating a serving stack, the other kinds
of model, collections of prompting techniques, and model and vendor comparisons — and every one of
the six triggers is an event rather than a date, which is the difference between a deferral and an
intention, with the first row carrying a count as well. **And the regress has no natural bottom**: four levels below a question about retrieval
is measure-theoretic probability, and the regress is wider than it is deep, because Chapter 17's
thirteen is thirteen descents rather than one. So the rule comes from the costs, which are
lopsided — going down too early costs weeks and produces nothing, going down too late costs one
confused afternoon — and the threshold is **the same wall twice, not once**: the first time, the
likeliest cause is a bad explanation at the level you are already on, and an hour spent finding a
second one is cheaper than a descent. The second hit gives the descent a question, and **a descent
with a question in it terminates where a descent without one is a syllabus**. One honest
exception, which is Chapter 17's own: if you are going to do the thing, the level below is not
optional, and the moment you use the theory the deferral is over.

### Key Terms

**This chapter introduces none**, the third in a row. Chapter 6 owns *dated detail* and the ladder
it belongs to, Chapter 7 owns the working rule this chapter argues for, and Chapter 17 owns the
thirteen the deferral table's first row points at. What is new here is a threshold and a table of
conditions, neither of which is a term. There is no *Worth Memorising* table either: the one thing
in the chapter to carry is the rule, and it is a sentence rather than a figure.
