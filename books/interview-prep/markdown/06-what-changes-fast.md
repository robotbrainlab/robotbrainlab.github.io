# What Changes Fast, and What Changes Slowly

Chapters 1 to 5 built a system and said where the work goes. This chapter is about
something else entirely: how to read everything else you are going to read.

*The problem.* Half of what I read is already out of date and I can't tell which half.

*The question.* Is there a way to sort a claim as I read it, rather than finding out later
which parts were worth learning?

## Three Kinds of Claim

Almost everything written about this field is one of three things. They look identical on
the page and they keep company in the same paragraph, which is why the mix is hard to see.

| Kind | What it is | How long it is good for |
|---|---|---|
| **Lasting principle** | A reason, or a shape that does not move: why you would do the thing at all, or what the parts are and how they fit | Years and years. It outlives the thing it was first said about |
| **Current convention** | How competent people work at the moment. True, load-bearing and replaceable | Months to a few years |
| **Dated detail** | A fact with a date on it. A name, a number, a version | Months, sometimes less |

Three examples of the same subject, searching your own documents, one of each kind:

- *Lasting principle.* If you want an answer grounded in your own material, that material
  has to reach the model, and you have to be able to say afterwards which part of it the
  answer came from.
- *Current convention.* Combine keyword search with meaning-based search and then re-order
  the results, rather than using meaning-based search alone. Chapters 26 and 28 are where
  that gets built.
- *Dated detail.* The ceiling on how much text the model you are using will accept, which
  Chapter 2 said every model has.

All three are worth knowing. They are worth knowing differently.

## The Test: What Would Have to Change?

Ask, of any claim: **what would have to happen in the world for this to stop being true?**

| If the answer is | The claim is a | So |
|---|---|---|
| A company ships something, or changes a price | **Dated detail** | Do not memorise it. Know that it exists and where to look |
| The field works out a better way of doing this | **Current convention** | Learn it properly, and hold it loosely |
| The underlying reason turns out to be wrong | **Lasting principle** | Learn it so you can derive the rest |

Worked on three claims:

1. *"Cost scales with the amount of text that moves."* What would have to change? Serving
   the model would have to stop getting more expensive as the text gets longer — a fact
   about the work being done, not about anybody's price list. **Lasting principle**, and it
   is the form Chapter 1 settled on: *cost scales with the text you move.* Note what is *not* the principle: that providers bill
   you per unit of text is how they happen to charge today, and you can run a model on
   hardware you own and be billed nothing per unit at all. **How you pay is the convention;
   that longer text costs more is the principle.** This pair is the whole chapter in one
   example, so it is worth re-reading.
2. *"Prefer a fixed sequence of steps to a free-running loop unless you have measured that
   the loop pays."* What would have to change? Loops would have to get reliable enough that
   the arithmetic in Chapter 4 stops biting. That is possible and it has not happened.
   **Current convention** — and one whose reason you can derive yourself, from Chapter 4's
   arithmetic, rather than having to take on trust.
3. *"This model accepts two hundred thousand units of text."* A product decision, announced
   on a Tuesday. **Dated detail.**

> **Tip:** The test is quick enough to run while reading. You do not need to be right every
> time. You need to stop treating all three as the same kind of thing, because that is what
> makes a field feel like it is moving too fast to learn — you are trying to memorise the
> dated details and derive the principles, which is exactly backwards.

## The Hard Case: A Convention That Looks Like a Principle

The honest difficulty is the middle row. A convention that has been true for a few years,
that everyone around you follows, and that has a good reason attached, is almost
indistinguishable from a principle.

Two signs that you are looking at a convention:

- **It names a technique rather than a reason.** "Re-order the search results" — the step
  named above — is a technique. "The
  thing that retrieves cheaply is not the thing that judges best" is the reason underneath
  it, and the reason is what survives the technique.
- **It has a predecessor you can remember.** If people did something else five years ago
  for the same reason, the reason is the principle and the something is the convention.

When you cannot tell, write down the reason you think is underneath. If you can state it
and it is not the technique restated, you have found a principle. If you cannot, you have a
convention and you should treat it as one.

## How Strong Is the Evidence?

Sorting a claim by how long it will last is one axis. The other is how much you should
believe it now.

The rungs below rise in **how much they tell you about settled practice** — not uniformly in
how well they show that a thing works. Keep those apart, because the table's last column
mixes them on purpose and that is where it is easy to go wrong.

| Strength | What it is | What it supports |
|---|---|---|
| **Announcement** | Somebody says a thing exists, or works | That the claim was made |
| **Demonstration** | It worked, on an example chosen by the person showing you | That it can work once |
| **One study** | Measured, in one setting, with one set of choices | That it worked there |
| **Practitioner report** | A survey, or a set of accounts: what people say they do | What people do. Only weakly whether it works |
| **Settled practice** | Many independent teams, over years, with the failure modes written down | Relying on it, and explaining it to someone else |

There is one more kind of evidence, and it is **not on that ladder at all**:

| Outside the ladder | What it is | What it supports |
|---|---|---|
| **A derivation** | It follows from arithmetic, or from a mechanism you can check yourself | Whatever the arithmetic covers — and it does not date |

Chapter 4's multiplication is one: nobody had to survey anybody to establish that ten steps
at nine-in-ten succeed about a third of the time. It is off the ladder because the ladder
measures how much somebody else's reporting can be trusted, and a derivation needs nobody's
reporting. When a claim can be derived, derive it.

Three things this table is for.

**First, a vendor's own material is an announcement until you can see what it was measured
on.** It may contain numbers, and the numbers may be real. But it was written by the party
that benefits, measured on a problem it chose, and the comparison it draws is the one that
flattered it. A score on a named public test that you could re-run yourself is more than an
announcement. A score on a test only they can run is not, however precise it looks. This is
not an accusation of dishonesty; it is what the genre is.

**Second, evidence that something works and evidence that people use it are different
claims, and neither implies the other on its own.** A practice can be widespread and not
work — much of our received wisdom is exactly that. A practice can be well supported and
barely adopted. So when somebody tells you "everyone is doing X", you have learned about
adoption. That becomes evidence about whether X is a good idea only when the practice has
survived a few years and its failure modes are written down somewhere you can read them —
which is what separates the bottom of this table from the top.

**Third, a survey of practitioners is a practitioner report even when it is published as a
study.** Chapter 4's twenty case studies and eighty-six practitioners is the example: it is
careful work, and what it establishes is what teams *do*, which is why Chapter 4 says the
study tells you the shape rather than the reason. Published form does not set the rung; what
was measured does.

> **Note:** Chapter 5's claim about **how much** of the work is evaluation and error analysis
> is a **practitioner report** — an account from people doing the job, not a measurement.
> That is the strongest evidence available for that particular claim, which is why the
> chapter says so rather than rounding it up. Chapter 5's argument for *what* the four
> activities are does not rest on that report; only the share does. Where the evidence is
> thin, saying so is part of the claim.

### When Two Rungs Are Close

The three-way sort has a hard case and so does this. Take one claim down two candidate
rungs: *"Reordering your search results improves answers."*

- **Is it a demonstration or a study?** If somebody shows you two answers, before and
  after, on a question they picked — demonstration. If they ran a fixed set of questions
  they wrote down in advance and reported how many improved — a study. The question that
  separates them is *who chose the examples, and when.*
- **Is it a study or settled practice?** One team measuring once is a study. What *would*
  make it settled is many teams measuring it, the result holding, and the cases where it
  *does not* help becoming known and written down. **The written-down failure modes are the
  tell** — settled practice comes with them, and a single study rarely does. On this claim
  we are not there: re-ordering results is a current convention, and whether it helps on a
  given set of documents is still something you measure. Chapters 26 and 28 are where you
  measure it.

Notice what just happened: the same claim appeared on both axes. It is a **current
convention** on the first axis and somewhere around **one study** on the second, and those
are two different questions about it — how long it will last, and how much to believe it
now. A claim always has a place on both, and the places need not agree.

Both boundaries turn on the same thing: not how confident the claim sounds, but how much
the claimant could have hidden without lying.

## Saying It Out Loud

Knowing the strength of a claim is only half of it. The other half is being able to say it
in one short sentence, without sounding like you are attacking anybody.

| What you mean | A sentence that says it |
|---|---|
| One study, one setting | "That's one study, and I don't know how much it transfers." |
| A survey, not a measurement | "That's what people report doing, which isn't the same as it working." |
| A vendor's number | "That's their own test. Do we know what it was compared with?" |
| Settled, rely on it | "That one's well established — I'd start from it." |
| It can be derived | "We can work that one out ourselves — we don't have to take their word for it." |
| I would need to check | "I'd want to measure that on our own data before building on it." |

That last one is a promise, so it is worth knowing what keeping it involves. Chapter 20 is
how you tell a real difference from noise, and Chapters 30 to 33 are how you build the
measurement in the first place. Saying "I'd want to measure that" without knowing either is
how a reasonable instinct turns into a stalled project.

These sentences do real work. They end the argument where the argument should end — at what
is known — instead of at whoever is most confident. And the habit protects you from the
specific failure this field produces in large quantities: repeating a plausible claim
confidently because you read it three times, in three articles, all of which were drawing on
the same announcement.

> **Warning:** The common failure is not believing something false. It is **losing track of
> where a belief came from.** You read a claim, it becomes familiar, and six weeks later you
> are asserting it as something you know. Nothing in your memory marks it as a thing you
> read once in a blog post. That is why the strength belongs in the sentence you say out
> loud: saying it is how you keep the label attached.

## How to Read a Release Announcement

An announcement is a genre with a fairly fixed shape, and once you know the shape you can read one
in a minute and extract the two or three facts in it.

What it usually contains, roughly in this order: a claim of improvement, a number, the name
of the test it was measured on, a comparison, a list of capabilities, and a price. Any of them can be
missing — a model you can download and run yourself often has no price at all, and plenty
of announcements name no public test, which is itself the most informative thing on the
page.

Four questions get you what is actually there:

1. **What is the claim, precisely?** "Better at reasoning" is not a claim. "Scores *n* on
   *this named test*" is.
2. **Measured on what?** A named public test tells you something. *Their* internal evaluation
   tells you almost nothing, because you cannot see it and neither can anybody else.
3. **Compared with what?** Against their own previous model is a weaker claim than against
   the best competitor, and the choice of comparison is the most informative thing on the
   page.
4. **What changed about the price and the limits?** This is usually the part that affects
   your work, and it is usually the part written in the smallest type.

Then sort what you found. The capability claim is a **dated detail** — it will be true of a
different model in six months. The price is a **dated detail**. If the announcement
describes a change in how you are expected to *work* — a new way of giving the model tools,
say — that is a candidate **current convention**, and it stays a candidate until you see
evidence that engineers outside the company are working that way.

> **Tip:** The useful question after reading one is not "is this better?" It is "does this
> change anything I am building?" Most of the time the honest answer is no, and the
> announcement was interesting rather than relevant. Interesting and relevant are allowed to
> be different.

## What to Memorise, and What to Look Up

The distinction follows from the sort, with one addition. You memorise what lasts — the
reasons, the shapes, and the failure modes that come with settled practice — and what you
can derive, because a derivation you have to rebuild from scratch every time is not much
use to you. You look up everything with a date on it.

| Memorise | Look up |
|---|---|
| The reasons. Why ground an answer, why limit a tool, why measure before believing | Prices, text ceilings, model names, rate limits |
| The shapes. What the parts of a system are and how they fit | Exact parameter names and interface details |
| The arithmetic you cannot look up quickly. What multiplying per-step reliability does over ten steps | Scores on particular named tests |
| The failure modes, and which part causes which | Which library version fixed which bug |

The reason to put it this way round is not tidiness. **A principle lets you derive the
detail or at least recognise a wrong one, and a list of current prices and limits will
never give you back the principle.** Somebody who has memorised current prices and text ceilings and cannot say why
retrieval exists knows strictly less than somebody who can derive what retrieval is for and
has to look the prices up, and the gap between them grows every month.

This also tells you what to do when something you learned goes out of date. If it was a
dated detail, replace the number and carry on. If it was a convention, learn the new one and
ask what reason it serves — usually the same reason, served better. If a *principle* goes,
that is a real event, and it is rare enough that it is worth noticing properly rather than
quietly updating.

## Lab: Sort Nine Claims

No code, no account, nothing to install. Fifteen minutes, and it has a right answer, which
is the point: you can check yourself before trying this on real writing.

Below is a made-up announcement. It is invented, so nothing in it dates, and it is built to
contain every case in this chapter.

```text
Introducing Northwind-3
-----------------------
Northwind-3 is our strongest model yet. It scores 71.4 on
CodeTask-V, up from 58.2 for Northwind-2, and it
accepts 400,000 units of text in a single request.

Our internal evaluation shows a 30% reduction in tool-calling
errors. Teams building agents tell us they now leave runs
unsupervised for longer.

Because quality depends on what the model is given, we
recommend retrieving supporting passages rather than pasting
whole documents, and keeping any single tool narrow in what
it can reach.

Northwind-3 is available today at $2.50 per million units in
and $10.00 per million out.
```

**Step 1.** Mark each of these nine claims **P** (lasting principle), **C** (current
convention) or **D** (dated detail).

1. Northwind-3 scores 71.4 on CodeTask-V.
2. It accepts 400,000 units of text per request.
3. It costs $2.50 per million units in.
4. Quality depends on what the model is given.
5. Retrieve supporting passages rather than pasting whole documents.
6. Keep any single tool narrow in what it can reach.
7. Northwind-3 is stronger than Northwind-2.
8. Teams leave agent runs unsupervised for longer.
9. Tool-calling errors fell by 30%.

*Expected result:* **D** for 1, 2, 3, 7 and 9; **P** for 4 and 6; **C** for 5; and 8 is the
interesting one — it is a **C** reported as a trend, and it is the only claim here whose
kind depends on whether you believe it. Six of the nine are dated details, which is normal:
that is what an announcement is for.

**Step 2.** For 4 and 6, write the reason in one sentence without naming a technique.

*Expected result:* for 4, something like *the model answers from what is in front of it, so
what you put in front of it decides the answer* — Chapter 1. For 6, something like *a tool
that cannot reach a thing cannot damage it* — Chapter 3. If your sentence names a technique
instead of giving a reason, you have written a **C**.

**Step 3.** Now label the evidence offered for claims 7, 8 and 9: announcement,
demonstration, one study, practitioner report, settled practice, a derivation, or *none*.

*Expected result:* 7 is an **announcement** — the two scores are theirs. 8 is a
**practitioner report**, and a weak one: it is the vendor relaying what teams tell them,
with no number and no count. 9 is an **announcement** too, and this is the trap — it looks
like a study because it has a percentage, but "our internal evaluation" is a test nobody
else can run.

**Step 4.** Answer the four questions from the section above about claim 9, the 30%.

*Expected result:* the claim is a reduction in tool-calling errors, which is precise enough.
It was measured on their own evaluation, which you cannot see. It was compared with
Northwind-2 — their own previous model, not a competitor, which is the weaker of the two
comparisons. And the price went up or down by an amount you cannot tell, because no previous
price is given. That last gap is the one worth noticing: the announcement states a price
without stating the change.

**Step 5.** Write the one sentence you would say in a meeting about claim 9.

*Expected result:* one sentence, under twenty words, naming the evidence without dismissing
the claim — for example *"That's their own internal evaluation against their own last model,
so I'd want to try it on our cases."*

**Step 6, optional.** Now do steps 1 and 3 on a real piece of writing you find yourself.
There is no key for this one, and that is the exercise: the counts you get are yours, and
the only wrong answer is not noticing which kind you were reading.

## Summary, Key Terms, and Review Questions

### Summary

Almost every claim in this field is a **lasting principle** — a reason, or a shape that
does not move — a **current convention**, or a **dated detail**, and you tell them apart by
asking what would have to change in the world for the claim to stop being true: a company
shipping something or changing a price, the field finding a better way, or the reason itself
being wrong. The hard case is a convention that has been true long enough to look like a
principle; the tell is that it names a technique and has a predecessor you can remember.
Separately, ask how strong the evidence is — announcement, demonstration, one study,
practitioner report, settled practice — or a derivation you can check yourself, which
stands outside that ladder because it needs nobody's reporting. Remember
that a vendor's own material is an announcement until you can see what it was measured on,
that a survey of practitioners is a practitioner report however it was published, and that
evidence a thing works and evidence people use it are different claims. Read an announcement
for four things: the precise claim, what it was measured on, what it was compared with, and
what changed about the price and the limits. Say the strength out loud when you repeat a
claim, because the real failure is not believing something false but losing track of where a
belief came from. Memorise the reasons, the shapes, the arithmetic and the failure modes;
look up everything with a date on it.

### Key Terms

| Term | Meaning |
|---|---|
| **Lasting principle** | A reason for doing something, or a shape that does not move, which outlives the technique it was first attached to. It stops being true only if the reason itself is wrong |
| **Current convention** | How competent engineers work at the moment: true, load-bearing and replaceable. It usually names a technique rather than a reason, and usually has a predecessor you can remember |
| **Dated detail** | A fact with a date on it — a name, a number, a version. It stops being true when somebody ships something or changes a price |
| **Practitioner report** | A survey or a set of accounts of what people say they do. It is a practitioner report however it was published, and it supports what people *do* far better than whether it works |
| **Evidence strength** | How much a claim is supported: announcement, demonstration, one study, practitioner report, settled practice — or a derivation, which stands outside the ladder because you can check it yourself |

### Review Questions

1. Give the one question that sorts a claim into the three kinds, and say what each of the three answers looks like.
2. A colleague says "everyone re-orders their search results now." What have you learned, and what have you not?
3. A provider's announcement says their new model is 30% better at coding. List the things you would want to know before repeating that.
4. Why is "losing track of where a belief came from" a worse problem than believing something false?
5. You learn that a convention you relied on has been replaced. What is the first question to ask about the replacement?

### Review Answers

1. *What would have to happen in the world for this to stop being true?* If the answer is that a company ships something or changes a price, it is a dated detail. If it is that the field works out a better way of doing this, it is a current convention. If it is that the underlying reason turns out to be wrong, it is a lasting principle.
2. You have learned something about adoption: the practice is widespread. You have learned nothing yet about whether it would help on your data, because adoption and evidence are separate claims and neither implies the other on its own. Adoption starts to count as evidence once a practice has survived a few years and its failure modes are written down. You also do not know whether "everyone" is a measurement or an impression.
3. What test the 30% was measured on, and whether anybody outside the company can run it; what it was compared against, which is the most informative choice on the page; and what changed about the price and the limits, which is the part most likely to affect your work. The capability claim itself is a dated detail and will attach to a different model within months.
4. Because a false belief can be corrected by meeting the evidence, while a belief with no provenance is rarely put to the test at all: there is nothing in your memory marking it as something you read once, so you assert it with the confidence of something you checked. It also spreads, because you sound sure. Saying the evidence strength out loud is what keeps the label attached.
5. What reason does the new one serve? Usually it is the same reason, served better — which tells you the principle underneath was right and only the technique moved. If it serves a genuinely different reason, something larger has changed and it is worth the time to work out what.

> **You understand this when** you can take a claim you already believe, say which of the
> three kinds it is, name the evidence behind it, and notice if you cannot remember where
> you got it.
