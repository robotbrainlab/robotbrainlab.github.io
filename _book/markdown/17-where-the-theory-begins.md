# Where the Theory You're Skipping Begins

Nine chapters ago this book started opening the model, and six times it stopped and said *not
this*, about thirteen different things in all. This chapter collects those points in one place. It is short, it is a
list, and it is the one chapter here you should be able to recite — because the difference
between a gap you can name and a gap you cannot is the difference between sounding bounded and
sounding ignorant.

*The problem.* I can explain the computation now. I want to know exactly what I still cannot
explain.

*The question.* What did this book deliberately leave out, what is each of those things
actually called, and what do I say when somebody asks me one of them?

## The List

Every row is a place where an earlier chapter stopped on purpose. None of them is a gap in the
explanation; each is a decision, and here is the whole of it.

| What you cannot explain | Where you met it | What it actually is |
|---|---|---|
| Why the embedding geometry carries meaning | 9 | **Representation learning**: why fitting a model to predict text arranges its vectors so that the arrangement is useful for anything else |
| Anything beyond one sentence on why normalisation is there | 12 | **Numerical stability**: how quantities behave through long chains of arithmetic, and what keeps them in a usable range |
| Why depth helps | 12 | An open research question. Not a settled account being withheld |
| How the gradient is computed | 14 | **Backpropagation**: the procedure that gets a derivative for every parameter in one backward sweep |
| Why repeating the update rule — gradient descent — arrives anywhere | 14 | **Optimisation theory**: when a procedure like this converges, to what, and how fast |
| What step size to use and how to change it | 14 | **Optimiser design** |
| Why the preference objective is the right thing to minimise | 14 | **Objective design**: why that expression, rather than another, is what you want a model to minimise |
| Why models got better at producing useful intermediate steps | 16 | What training does to make a model emit intermediate work that helps. There is no tidy name to give this one at the level this book works at |

And five more that the book never needed, listed so the set is complete rather than
convenient:

| What you cannot explain | What it actually is |
|---|---|
| **Initialisation** | What the parameters are set to before training begins, and why the choice matters |
| **Regularisation** | The techniques that stop a model fitting its training data too closely |
| **Inductive bias** | What a design assumes about the world before it sees any data |
| **Generalisation theory** | Why a model fitted to one body of text works on text it never saw — the bias–variance trade-off, and what learning theory proves about it |
| **Scaling laws** | The relationships between model size, data, compute and loss — and their derivation |

Three further subjects are outside this book without being gaps in it: convolutional and
recurrent architectures, and classical machine learning. They are other kinds of model rather
than parts of this one, which is why they are not on the list above.

**Thirteen things.** You can read that list in a minute, which is the point: a boundary you can
recite is a boundary you can defend.

## What They Have in Common

Look down the "what it actually is" column and one pattern runs through all of it.

**Every item is on the far side of "the numbers are given".** Not one of them is needed to
follow the arithmetic of a single reply. Chapters 9 to 13, 15 and 16 took that computation
apart completely — tokens, the
embedding table, attention, the stack, the output distribution, the sampling, the cost, the
failures — and at no point did any of it require knowing why the numbers came to be what they
are.

That is not a coincidence; it is the line the book was built on. The numbers are given, and
everything downstream of them is arithmetic you can do by hand. **The things you skipped are
the things on the other side of "the numbers are given".**

Which has a consequence worth stating plainly, because it is the thing to say when somebody
suggests you have missed the real subject. For the work of building applications on top of
these models — choosing what goes in the request, deciding what the model may do, finding out
whether the output was any good, controlling what it costs — none of the thirteen is load
bearing — with one edge: if you ever do your own fine-tuning, which is Chapter 39, you will be
choosing a step size. They are load bearing for building a model, which is a different job.

> **Note:** "Different job" is not "lesser job", and the boundary is not a judgement about
> what is worth knowing. It is a judgement about what fits in one book read in the time you have.
> Chapter 56 is where to go next, and it names the books.

## What to Say When Somebody Pushes

The practical half of this chapter. An interviewer asks why depth helps, or how
backpropagation works, and you have not studied it. There is a good answer and it has three
parts, in this order.

**Name the thing correctly.** "That is optimisation theory" or "that is representation
learning" or "that is backpropagation — the backward sweep that gets a derivative for every
parameter". Naming it accurately is most of the work, because it demonstrates that you know
where you are rather than that you have wandered off a map.

**Say what you do know that borders it.** You know a great deal that touches each of these.
You can state the training objective as a formula. You can state the update rule and say what
each symbol means. You can say what each of Chapter 14's three stages changes. What you have not done
is derive why the rule converges — and the border is exactly that sharp.

**Say what you would do if you needed it.** Not "I would look it up", which says nothing.
Something specific: "if I were debugging a training run I would need it, and I would start
with the standard text rather than a blog post, because this is settled material and not a
moving target."

Put together, for the depth question:

> "Honestly, nobody has a clean account of that. The mechanism is that more layers means more
> rounds of gathering from other positions and computing at each one, and a result assembled
> at layer twenty can be gathered from at layer twenty-one. *Why* that buys what it buys —
> why thirty-two layers beats sixteen by more than it costs, where the returns stop — is an
> open research question, and I have not studied the attempts at it. What I can tell you is
> what a layer does, which half of it holds the parameters, and what depth costs at
> inference."

**That is a good answer to a question you cannot answer**, and it is better than a confident
reconstruction, because an interviewer who asks it usually knows the answer is not clean.

> **Tip:** The failure mode is not saying "I don't know". It is saying "I don't know" and
> stopping — or worse, producing a plausible-sounding derivation. You have spent nine chapters
> learning that a plausible continuation is not the same as a true one. Do not become one.

## What a Boundary Is Not

Three things it is not, because each is a way people get this wrong.

**It is not a claim that the material is easy.** Nothing above was omitted because it is
simple. Backpropagation is a few lines of calculus and a great deal of care; optimisation
theory is a field.

**It is not permanent.** You are weeks from an interview, not at the end of your career. Chapter 56 exists because the sensible order is to learn the system first and the
theory second — not instead.

**And it is not the same as not knowing it is there.** This is the whole reason the chapter
exists. A person who has never heard of representation learning and a person who can say "that
is representation learning, and I have not studied it" are in completely different positions,
and only one of them can have a conversation about it.

## Lab: Write Your Own Boundary

No code and no calculator. Fifteen minutes, and there is a key for the parts that have one.

**Step 1.** Close the book. Write down as many of the thirteen as you can, from memory — and
for the eight that came from a chapter, the chapter where you met each.

*Expected result:* the key is the two tables above — the first carries the chapters, the second
is five items that were never needed and so never met. Score yourself out of thirteen, and look
up every one you missed: those are the ones most likely to come up unprepared.

**Step 2.** For each of the thirteen, write one sentence saying what it actually is. Then check
them against the tables above.

*Expected result:* the table's sentence is the key for each. These are one-line definitions,
not subjects you are expected to summarise, and the test is whether you can say one without
reaching for the book.

**Step 3.** Pick the three you find hardest to say out loud. For each, write the three-part
answer from this chapter: name it, say what you know that borders it, say what you would do if
you needed it.

*Expected result:* three short paragraphs, each about forty words. The middle part carries the
answer: if you cannot say what you know that borders a gap, you do not yet know where the gap
is.

**Step 4.** Now the other direction. Write down three things you *can* explain about what a
model computes, which you could not have explained before Chapter 8.

*Expected result:* no key, and that is deliberate — this one is about you. If the list is hard
to write, the fix is not more theory; it is to go back and do one chapter's arithmetic with a
pen.

**Step 5.** A colleague says the book you have read is "just the API layer" and that you do
not really understand the models. Write two sentences in reply.

*Expected result:* something close to: *"I can compute an attention row by hand and tell you
what a key–value cache costs at eight thousand tokens. What I have not studied is why training
converges — which is a different subject, and I can tell you exactly which one."* The reply
works because it is specific in both directions. A vague defence of the boundary sounds like a
vague understanding of the material.

## Summary, Key Terms, and Review Questions

### Summary

Thirteen things were left out of this book on purpose, and they are listed here so that each is
a gap you can name rather than one you do not know about. Eight of them are places an earlier
chapter stopped and said so: why the embedding geometry carries meaning (Chapter 9); the
subject behind Chapter 12's one sentence on normalisation, and why depth helps (Chapter 12);
how the gradient is computed, why repeating the update rule — gradient descent — converges, how
a step size is chosen, and why the preference objective is the right thing to minimise (Chapter
14); and why models got better at producing useful intermediate steps (Chapter 16). Five more —
initialisation, regularisation, inductive bias, scaling laws and generalisation theory — were
never needed. **Every one of them sits on the far side of "the numbers are given", and not one is needed to
follow the arithmetic of a single reply**, which is the line the book was built on. When somebody pushes past it, the answer
has three parts: name the thing correctly, say what you know that borders it, and say what you
would do if you needed it. A boundary is not a claim that the material is easy, it is not
permanent, and it is not the same as not knowing the material is there.

### Key Terms

| Term | Meaning |
|---|---|
| **Backpropagation** | The procedure that computes a derivative for every parameter in one backward sweep through the model. How the gradient of Chapter 14's update rule is obtained. Not taught in this book |
| **Optimisation theory** | The study of when a procedure like the update rule converges, to what, and how fast. Not taught in this book |
| **Optimiser design** | Choosing and adapting the step size and the form of the update. Not taught in this book |
| **Objective design** | Why one expression rather than another is the right thing for a model to minimise. The question Chapter 14 states its preference objective without answering. Not taught in this book |
| **Representation learning** | Why fitting a model to predict text arranges its vectors so that the arrangement is useful for other things. The question Chapter 9 refused. Not taught in this book |
| **Numerical stability** | How quantities behave through long chains of arithmetic, and what keeps them in a usable range. The subject behind Chapter 12's one sentence on normalisation. Not taught in this book |
| **Initialisation** | What the parameters are set to before training begins, and why the choice matters |
| **Regularisation** | The techniques that stop a model fitting its training data too closely |
| **Inductive bias** | What a design assumes about the world before it sees any data |
| **Generalisation theory** | Why a model fitted to one body of text works on text it never saw — the bias–variance trade-off, and what learning theory proves about it |
| **Scaling laws** | The relationships between model size, data, compute and loss, and their derivation |

### Review Questions

1. An interviewer asks why depth helps. You have not studied that. What do you say?
2. What do all thirteen items on the list have in common, and why does that matter?
3. Somebody says you have learned "just the API layer". What is the two-sentence reply?
4. What is the difference between a boundary and ignorance?
5. Name the four items that came from Chapter 14 and say what each one is.

### Review Answers

1. Name it, border it, and say what you would do. "Nobody has a clean account of that — it is
an open research question rather than a settled explanation I have skipped. The mechanism is
that more layers means more rounds of gathering from other positions and computing at each
one, so a result assembled at layer twenty can be gathered from at layer twenty-one. Why that
buys what it buys, and where the returns stop, I have not studied. What I can tell you is what
a layer does, that the feed-forward block holds more of the parameters than attention does,
and what depth costs at inference." The answer works because every sentence in it is true and
the boundary is drawn exactly.
2. Every one of them sits on the far side of **"the numbers are given"** — none is needed to
follow the arithmetic of a single reply. That matters for two reasons. It explains why the book could take
the whole computation apart without any of them — the numbers are given, and everything after
that is arithmetic. And it gives you the sentence to use when somebody suggests you have
missed the real subject: these are load bearing for building a model, which is a different job
from building applications on one.
3. "I can compute an attention row by hand and tell you what a key–value cache costs at eight
thousand tokens. What I have not studied is why training converges — which is a different
subject, and I can tell you exactly which one." It works because it is specific in both
directions: a concrete thing known and a named thing not known. A vague defence of a boundary
sounds like a vague grasp of the material.
4. A boundary is a decision you can state, with a name on each side of it. Ignorance is not
knowing the thing exists. The person who says "that is representation learning and I have not
studied it" and the person who has never heard the phrase are in entirely different positions,
and only the first can have the conversation. That is the whole reason this chapter is in the
book.
5. Backpropagation — the procedure that computes a derivative for every parameter in one
backward sweep, which is how the gradient in the update rule is obtained. Optimisation theory
— when repeating that update rule, which is gradient descent, converges, to what, and how
fast. Optimiser design — what step size to use and how to adjust it as training proceeds. And
why the preference objective is the right thing to minimise, which Chapter 14 states and says
outright it is not deriving. All four sit on the far side of the two lines Chapter 14 wrote
down and did not derive: the update rule and the preference objective.

> **You understand this when** you can name all thirteen, say which side of the line each sits
> on, and answer the depth question out loud without either guessing or stopping at "I don't
> know".
