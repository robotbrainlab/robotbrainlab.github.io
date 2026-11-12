# What to Learn Next

Chapter 17 listed thirteen things this book left out and gave each one its real name where it has
one, so that every gap in your knowledge is one you can say out loud. That chapter pointed here and
said this is where the books are. Here they are, and there are five of them.

*The problem.* I can hold a conversation about all of this now. I want to know what I actually
don't know.

*The question.* Which of the thirteen has a book, which book, in what order, and what do I do
that is not reading?

## The Answer, First

**Five books, one system, and one habit.** That is the whole programme, and the reason it is this
short is that Chapter 17's list is short: thirteen named gaps, of which ten are settled material
somebody has already written down well, and three are not.

| What to do | Why it is on a list this short |
|---|---|
| Read the statistics first | It is the only item whose method you are already using and cannot derive |
| Then the one general text | It closes eight of Chapter 17's thirteen on its own |
| Then the two applied fields, when the work asks | Retrieval and ranking; evaluation science. Each is the field behind something this book did at application depth |
| Then the learning theory, or never | It closes two of the thirteen and is the one most people should skip |
| Read one complete system you did not write | The only item that is not a book, and the one that changes how you read code |

Plus the habit, which is not a book either: **keep up by reading backwards**, which is Chapter 6's
ladder used as a filter rather than as a feed, and which the last section is about.

**The order matters more than the list**, and it is not the obvious one. The obvious order puts
the deep-learning text first, because that is where most of the thirteen are. The useful order
starts with the statistics, for a reason about you rather than about the subject: Chapter 20's
bootstrap is a method you have now used on real data a dozen times, and you cannot say why it
works. **Every one of Chapter 17's thirteen is something you have never needed. This one is not on
that list at all — it is a tool already in your hand with a sealed lid.**

**And one thing to be clear about before any of it.** Chapter 17 said the boundary is not
permanent and that the sensible order is the system first and the theory second, *not instead*.
This chapter is the second half of that sentence. Nothing below is remedial, and nothing below is
urgent either — you are weeks from a conversation and none of these books will change what you say
in it. They change what you can do in the year after, and **Chapter 57 is the argument for how long
each of them can wait**, which is this chapter read from the other end.

## Where the Theory Begins, With the Books

Chapter 17's thirteen against the books. The chapter numbers are this book's, because that is
where you met each gap.

| The gap, and where you met it | Where it is written down |
|---|---|
| Why the embedding geometry carries meaning — representation learning (9) | Goodfellow, Bengio and Courville, *Deep Learning* |
| How the gradient is computed — backpropagation (14) | *Deep Learning* |
| What step size to use — optimiser design (14) | *Deep Learning* |
| Initialisation | *Deep Learning* |
| Regularisation | *Deep Learning* |
| What is behind Chapter 12's one sentence on normalisation — numerical stability (12) | *Deep Learning* in outline; beyond that it is a field of its own |
| Why gradient descent arrives anywhere — optimisation theory (14) | *Deep Learning* in outline; beyond that, likewise |
| Why one objective rather than another — objective design (14) | *Deep Learning* for objective design in general. *Not* for Chapter 14's own preference objective, which postdates it and is in the research literature |
| Inductive bias | Shalev-Shwartz and Ben-David, *Understanding Machine Learning* |
| Generalisation theory | Shalev-Shwartz and Ben-David |
| Why depth helps (12) | *Nowhere settled.* Chapter 17 says why: an open research question, not a withheld account |
| Why models got better at producing useful intermediate steps (16) | *Nowhere settled*, and Chapter 17 could not give it a name at this level |
| Scaling laws | *No book.* They postdate the general text and live in the research literature |

**So eight of the thirteen are one book** — five of them in full, two in outline and one only in
its general form — which is why *Deep Learning* is the second thing to read rather than the fifth:
it closes more of Chapter 17's list than everything else here put together. Two more are the
learning-theory text, which makes ten.

**And three of them have no book, which is the honest row of that table.** Saying *nowhere settled* to
somebody who asks why depth helps is a better answer than naming a book that does not contain it,
and Chapter 17 has already given you the three-part form to say it in: name the thing, say what
you know that borders it, say what you would do if you needed it.

**Then the three books that close none of the thirteen**, and they are on the list because this
book leaned on their subjects rather than skipping them:

| Book | What it is the field behind |
|---|---|
| Efron and Tibshirani, *An Introduction to the Bootstrap* | Chapter 20's method, named in sixteen chapters of this book and derived in none of them |
| Manning, Raghavan and Schütze, *Introduction to Information Retrieval* | Chapters 26 and 29, which taught retrieval and ranking as far as an application needs |
| Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* | The live comparison Chapter 20 names as a different thing and this book never makes |

**Those three are the ones most likely to be useful at work inside a year**, which is a different
ranking from how much theory they close — and it is the ranking to use, because the gap that
costs you something is the one next to work you are actually doing.

## Why the Statistics Come First

The case for the order is three sentences long and worth having, because the obvious order is
defensible and this one is better.

**You are already using it.** Chapter 20 gave you the bootstrap in three lines of Python —
resample the units with replacement, compute the statistic, take the middle ninety-five per cent
of the results — and from there it appears in fifteen more chapters of this book. You have put an
interval round a retrieval comparison, a grader comparison, a latency difference, a cost
difference and a model-snapshot difference. In none of those did you know why resampling your own
sample tells you anything about the world.

**It is the only item on this chapter's list that can make you wrong in public.** Chapter 17's
thirteen are subjects you have never needed; this one is a tool you reach for, and a tool you
cannot derive is
a tool you will eventually use outside the conditions it holds under. Chapter 20 was careful about
some of those conditions — that the interval is anchored on the score you measured rather than
centred on it, that pairing cancels only what two versions share, that overlapping intervals are
not the test. It did not tell you where any of that comes from, and the difference between
following those rules and understanding them is the difference between being right on the cases
the book covered and being right on a case it did not.

**And it is the narrowest of the five.** The other four are each a field; this one is a method, and
the difference matters because the failure mode of a reading list is not choosing the wrong book —
it is opening a field's standard text, reading ninety pages, and concluding that you do not have
the time. Start with the one you will finish.

## Reading One Complete System You Did Not Write

The one item on the list that is not a book, and the one most people skip because it has no
obvious stopping point.

**You have already done the smallest version.** Chapter 45 is a parser, a chunker, an index, a
retriever, a reranker, a context assembler, a model call, a citation check and a trace, measured
end to end, and you read every line of it. What that bought is a shape in your head: you know what the parts of such a system
are and roughly how big each one should be. What it cannot buy is the thing only somebody else's
code teaches, which is **how much of a real system is none of those parts.**

So the next one is code you did not write, and the criteria are short:

| Look for | Because |
|---|---|
| It is a system, not a library | A library has an interface and a system has a shape; you are reading for the shape |
| Its own documentation says how it is put together | If the architecture has to be reconstructed from the code, you will reconstruct it wrong |
| Somebody operates it | Code nobody runs has no error handling worth reading, and the error handling is half of what you came for |
| You can run it | A system you have run and broken is a system you have read |

**And read it in one particular order**, because the instinct is to start at the entry point and
the entry point is the least informative file in any repository. Start with the thing you already
understand — find the model call, or the retrieval step, or the place the prompt is assembled —
and read outwards from there until you stop recognising anything. The boundary where you stop
recognising things is the chapter of this book that does not exist, and it is different for
everybody, which is why nobody can hand you a reading order for somebody else's code.

**What you are looking for is the ratio.** In this book's own pipeline almost every line is doing
the thing the chapter is about. In a system somebody operates, most of the lines are configuration,
retries, limits, migrations, feature flags, metrics and the handling of cases that happen twice a
year. Chapter 52's own finding is the one to hold while you read: most of the latency in a built
system is not the model being slow, it is the number and the size of the calls the design makes —
and the same is true of the code. **Most of a real system is not the subject of this book, and
seeing that for yourself is worth more than being told it**, which is why this item is on the list
at all.

## Keeping Up Without Chasing Announcements

The habit, and it is a filter rather than a feed.

Chapter 6 owns what changes fast and gave you the ladder: an announcement, a demonstration, one
study, a practitioner report, settled practice — and, standing outside the ladder because you can
check it yourself, a derivation. **Used as a reading habit, that ladder runs backwards.** The
material arrives at you in the order the ladder is weakest first: announcements are pushed,
demonstrations are shared, studies are posted, practitioner reports are published occasionally,
and settled practice is not news. So anything that reaches you without being sought is, almost by
construction, at the bottom.

Which gives three rules, and the first is the one that saves the time.

**Read nothing because it arrived.** The test is not *is this interesting* but *would I have gone
looking for this*. Chapter 6's distinction is the filter: a *dated detail* — a name, a number, a
version — is worth reading only when you are about to depend on it, and a *lasting principle* is
worth reading whenever you meet it, because it will still be true when the technique it arrived
attached to is gone.

**Read the thing the announcement is about, not the announcement.** If something matters enough
to change what you build, it has a specification, a price list, a published figure or a paper
behind it, and that document is both shorter and more reliable than the writing about it. Chapter
54 is the operational version of the same rule, about data retention specifically: a provider's own
page, read on the day, for the endpoints you actually call.

**And let the work pull.** This is the rule that replaces a feed, and it is Chapter 7's rule for
reading this book — the one Chapter 57 turns into a threshold — working just as well afterwards. A
thing you cannot explain in a system you are responsible for is a far better reading prompt than
anything anybody posts, because it comes with the one piece of information a feed cannot give you:
that you need it.

**And that is also the answer to say out loud when somebody asks how you keep up**, in place of a
list of sources: *I read the primary document when I am about to depend on something, I let
problems at work decide what I read, and I do not read announcements.* It is a better answer than
naming five newsletters, and it is the only one of the two that anybody can check.

## The Answer to the Question You Will Be Asked

*What do you not know yet, and how would you go about learning it?* is the one question in this
part of the book that is about you rather than about a system, and it is the easiest to answer
badly. The bad answer is a list of topics, delivered in the tone of somebody apologising. The
good one has two halves and this book has given you both.

**The first half is Chapter 17's and it is already written down.** Thirteen named gaps, each with
its real name where it has one, and two of them not gaps at all but open questions — why depth
helps, and why models got better at producing useful intermediate steps. *I can tell you exactly what
I have not studied* is a sentence very few candidates can say, and the reason you can is that you
spent a chapter on the list rather than on the material.

**The second half is this chapter, and it is shorter than it looks.** Five books, in an order with
a reason: the statistics first because it is the method already in my hands, then the one general
text because it closes eight of the thirteen, then retrieval and evaluation science when the work
asks for them, and the learning theory possibly never. One system I did not write, read outwards
from the part I already understand. And a habit that is a filter rather than a feed: the primary
document when I am about to depend on something, the work deciding what I read, and no
announcements.

**Then the sentence that makes it an answer rather than a plan.** Say which one you are doing
now. A reading list is a statement about intentions and a chapter you are halfway through is a
statement about you, and the difference is audible.

## What This Chapter Has Not Told You

Five things, deliberately.

**What is in the books.** This chapter names them and does not summarise them, because a summary
of a field's standard text is the thing that stops people reading it. Chapter 17 names each
subject in one line; that is the summary, and it is deliberately not more.

**Papers, and how to read them.** Some of Chapter 17's thirteen reach past the books entirely —
scaling laws and the rest of objective design into the research literature, and two that nobody
has settled — and reading papers is a different skill with its own failure mode, the one
Chapter 6 is about, where a demonstration reads as a result. This chapter says where they are and
stops.

**Classical machine learning, and the two other architectures.** Chapter 17 lists convolutional and
recurrent models and classical machine learning among the subjects outside this book without being
gaps in it, and Chapter 57 carries the reason as a deferral with a trigger. The standard text for
the third is Hastie, Tibshirani and Friedman's *The Elements of Statistical Learning*; it is named
here and deliberately not on the route, because nothing in the fifty-five chapters before this one
leaned on it.

**Which system to read.** The criteria are here and no system is named, for Chapter 6's reason: a
named repository is a *dated detail* and the criteria are not. A list of three projects written
today would be the most quickly wrong page in the book.

**And how long any of it takes.** There is no schedule here, because the only honest one depends
on how much of your week is yours, and a schedule you miss is worse than none. What the chapter
offers instead is an order, which is the part that transfers.

## Summary and Key Terms

### Summary

Chapter 17 named thirteen gaps; this chapter says which have a book. **Eight of the thirteen are
one book** — representation learning, backpropagation, optimiser design, initialisation and
regularisation in full, numerical stability and optimisation theory in outline, and objective design
only in its general form — which is Goodfellow, Bengio and Courville's *Deep Learning*. Two more are Shalev-Shwartz
and Ben-David's *Understanding Machine Learning*: inductive bias and generalisation theory. **And
three have no book**: why depth helps and why models got better at producing useful intermediate
steps are open questions rather than withheld accounts — Chapter 17 says so in terms of the first
and says of the second only that it has no tidy name at this level — and scaling
laws postdate the general text and live in the research literature. Three further books close none
of the thirteen and are on the list because this book leaned on their subjects — Efron and
Tibshirani's *An Introduction to the Bootstrap* for Chapter 20's method, named in sixteen chapters
here and derived in none; Manning, Raghavan and Schütze's *Introduction to Information Retrieval*
for Chapters 26 and 29; and Kohavi, Tang and Xu's *Trustworthy Online Controlled Experiments* for
the live comparison Chapter 20 names and this book never makes. **Those three are the ones most
likely to matter at work inside a year**, which is a different ranking from how much theory they
close, and it is the one to use. **Read the statistics first** — not the deep-learning text, which
is the obvious choice — because the bootstrap is the only item on the list that is already a tool
in your hands, because it is the only one that can make you wrong in public, and because it is the
narrowest — a method where the other four are each a field — and a reading list fails by being
abandoned rather than by being wrong. **Then one
complete system you did not write**, which the smallest version of — Chapter 45's pipeline — has
already shown you the shape of; what somebody else's code adds is how much of a real system is
none of those parts, so look for a system rather than a library, with its own architecture
document, that somebody operates and you can run, and read outwards from the part you already
understand rather than from the entry point. **And keep up with a filter rather than a feed**:
Chapter 6's ladder runs backwards in the order things reach you, so read nothing because it
arrived, read the primary document rather than the writing about it, and let a thing you cannot
explain in a system you are responsible for decide what you read next — which is Chapter 7's rule
for reading this book, working just as well afterwards.

### Key Terms

**This chapter introduces none.** Chapter 17 named the subjects, Chapter 6 owns the ladder and its
three kinds of claim, and everything here is a book title or an order to do things in. For the same
reason there is no *Worth Memorising* table: the only things in the chapter worth carrying are five
authors and one rule, and a table would not help you remember either.
