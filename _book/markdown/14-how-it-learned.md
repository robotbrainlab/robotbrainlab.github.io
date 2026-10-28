# How It Learned to Do This

Every chapter so far has taken the model's numbers as given. This one says where they came
from — far enough to answer the questions an interview asks, and then it stops, on purpose and
visibly. By the end you will be able to write down what training optimises, say what each of
the three stages changes, and say exactly which sentence is the last one this book will
explain.

*The problem.* Somebody trained this on "the internet". That sentence explains nothing.

*The question.* What was being optimised, how were the numbers changed, and what does each
stage of training actually buy?

## The Objective, and Why It Needs No Labels

Chapter 9 said the model produces one probability for every vocabulary entry. Training is the
process of making those probabilities better — and "better" has a precise meaning that is
worth getting exactly right, because it explains nearly everything else.

**The model is asked to predict the next token, and the text supplies the answer.**

Take a sentence from the training data. Cut it anywhere. Everything before the cut is the
input; the token immediately after the cut is the correct answer. Move the cut along one token
and you have another example. A thousand-token document is a thousand training examples, and
nobody had to label any of them.

```text
  the cat sat on the mat
  ^^^^^^^^^^^ input       ^^^ answer
```

This is why the stage can consume an enormous amount of text: **the text is its own answer
key.** There is no annotation step, no agreement between labellers, no cost per example beyond
the compute. It is the single most consequential fact about how these models came to exist,
and it is the reason the word "unsupervised" gets used, though "self-supervised" is the more
accurate one — there *are* labels, and the text is where they come from.

The objective, written down:

```{=latex}
\[ \mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \log p(t_i \mid t_1 \ldots t_{i-1}) \]
```

Read it with Chapter 8's four steps. `\(t_i\)`{=latex} is the token at position
`\(i\)`{=latex}; `\(p(t_i \mid t_1 \ldots t_{i-1})\)`{=latex} is the probability the model gave
to that token, having seen everything before it; `\(\log\)`{=latex} is Chapter 8's logarithm;
`\(\sum\)`{=latex} runs over every position; `\(\frac{1}{N}\)`{=latex} averages. The minus sign
makes it a quantity to *minimise* rather than maximise.

In words: **the loss is the average surprise, over every position, at the token that actually
came next.** Training adjusts the numbers to reduce it.

## Cross-Entropy: How Wrong Was That Guess?

That quantity has a name. `\(-\log p\)`{=latex} of the correct answer is the **cross-entropy**
loss, and it is worth computing once to see how it behaves.

Chapter 9's worked example ended with this distribution after "the cat sat":

```text
  the 0.012   cat 0.234   sat 0.032   mat 0.086   on 0.636
```

Suppose the text really did continue with "on". The loss for that one prediction is

```text
  -ln(0.636) = 0.453
```

Now suppose it continued with "cat" instead — a reasonable word the model thought less likely:

```text
  -ln(0.234) = 1.452
```

And suppose it continued with "the", which the model nearly ruled out:

```text
  -ln(0.012) = 4.423
```

Three properties fall straight out of those numbers, and all three matter.

**The loss depends only on the probability of the right answer.** What the model thought about
the other four tokens never enters. A model that puts 0.636 on the correct token scores 0.453
whether the remaining 0.364 was spread evenly or piled on one rival.

**Being confidently wrong is punished enormously.** Going from 0.234 to 0.012 — still not zero
— takes the loss from 1.452 to 4.423. As the probability of the true token approaches zero the
loss grows without limit. That asymmetry is the point: a model that assigns almost nothing to
something that then happens is making the worst kind of mistake.

**And a perfect prediction scores zero.** `\(-\log 1 = 0\)`{=latex}. The loss is never
negative, because a probability is never above 1.

> **Note:** Logarithms here are natural logs, as in Chapter 8. Some sources use base 2, which
> multiplies every number above by about 1.44 and changes the units from *nats* to *bits*.
> Nothing about the argument changes; if you compare a loss figure with somebody else's, check
> which they used.

## Perplexity

Cross-entropy is in awkward units. **Perplexity** fixes that by exponentiating it:

```{=latex}
\[ \mathrm{perplexity} = \exp(\mathcal{L}) \]
```

And it has a reading that makes it genuinely useful. Suppose a model is completely undecided
across a vocabulary of five, giving each token 0.2. The loss is
`\(-\ln(0.2) = 1.609\)`{=latex}, and the perplexity is `\(\exp(1.609) = 4.998\)`{=latex} —
which is exactly 5, since exponentiating `\(-\ln(0.2)\)`{=latex} undoes the logarithm and
leaves `\(1/0.2\)`{=latex}. Exactly the number of options.

That is the general case: **a uniform choice among `\(V\)`{=latex} options has perplexity
`\(V\)`{=latex}.** So perplexity reads as *the number of equally likely options the model is
effectively choosing between*. A perplexity of 3 means the model is about as uncertain as
someone picking at random from three things. A perplexity of 128,000 — the vocabulary size
Chapter 9 uses for a
real model — means it did no better overall than a uniform guess.

Work a short sequence. Four predictions, with these probabilities for the tokens that actually
came next:

```text
  position   p       -ln p
     1     0.636     0.453
     2     0.234     1.452
     3     0.086     2.453
     4     0.636     0.453
                     -----
           average   1.203

  perplexity = e^1.203 = 3.330
```

So across those four tokens the model was about as uncertain as a fair choice between three and
four options. That is a number you can compare: between two models on the same text, or for
one model as training proceeds.

> **Warning:** Perplexity is a measure of how well a model predicts *some particular text*. It
> is not a measure of whether answers are correct, useful or safe, and two models' perplexities
> are only comparable on the same text with the same vocabulary — a model whose tokeniser cuts
> the text into fewer pieces is being asked a different question. Interview answers that treat
> perplexity as a quality score are the ones that get followed up on.

## The Loop, From Outside

The training loop has four steps, and it is simpler than people expect.

```text
  1. take a batch of text
  2. run it forward, getting a distribution at every position
  3. compute the loss against the tokens that actually came next
  4. change every parameter a little, in the direction
     that reduces the loss

  then go back to 1, a very large number of times
```

How many times is set by how much text there is: the first stage works through its corpus
once, or close to it, and the number of steps is the number of batches that takes. Running
over the same text many times is not what these models do, and *why* is outside this book along
with everything else about why the training works.

Steps 1 to 3 you can already do — they are Chapters 9 to 13 run forwards and then one
logarithm. Step 4 is the one this book does not open, and here is the whole of it:

```{=latex}
\[ \theta \leftarrow \theta - \eta \, \nabla_{\theta}\mathcal{L} \]
```

One sentence of notation, and then we stop. `\(\theta\)`{=latex} stands for all the parameters
at once. `\(\nabla_{\theta}\mathcal{L}\)`{=latex} is the **gradient** — for each parameter, how
much the loss would rise if that parameter rose, computed for all of them together.
`\(\eta\)`{=latex} is the step size. The rule says: move every parameter a small distance in
the direction that reduces the loss, and repeat.

**That line is the edge of this book.** How the gradient is computed for billions of parameters
is called backpropagation. Why repeating this rule arrives anywhere useful is optimisation
theory. What step size to use, and how to adjust it, is optimiser design. None of the three is
in these pages, Chapter 17 lists all of them, and the honest interview answer is "I can state
the update rule and I can tell you what it does; I have not studied why it works."

> **Tip:** That answer is a good one, and it is better than an improvised version of the real
> explanation. Interviewers can tell the difference between a boundary somebody has drawn
> deliberately and one they have fallen off.

What is worth carrying instead is the *shape* of the loop, because three practical facts come
straight out of it. Training happens once, before you ever call the model — Chapter 1's point,
now with a mechanism. Nothing you send at inference runs step 4, so answering your request
changes no parameter. (Whether what you send is kept and used in a *later* training run is a
different question, and a matter of the provider's policy rather than of the loop.) And steps 1 and 4 are the same whatever the data is.
What step 3 compares changes for one of the three stages, and so does what step 2 has to run
for it — a point the third stage's own section makes concrete. That is why the next section is
about data rather than about algorithms.

## Three Stages, Three Kinds of Data

A model you can talk to was made in three stages. The loop above is involved in all three; what
differs is the data — and, for the third stage only, the loss at step 3.

**Pretraining** runs the loop on an enormous quantity of general text. This is where
essentially
all of the model's knowledge of language, facts, code and document structure comes from, and it
accounts for the overwhelming majority of the computation ever spent on the model. What comes
out is a model that *continues text*. Ask it a question and it may well continue with more
questions, because that is a thing documents do.

**Supervised fine-tuning** runs the same loop, with the same cross-entropy objective, on a much
smaller set of curated examples: a request, and a good response to it. Nothing about the
mechanism changes — it is still predicting the next token — but the text it is now predicting
is the text of a helpful reply. This is the stage that turns a text continuer into something
that answers.

That distinction has a name you will meet on every provider's model list. A model that has had
only the first stage is a **base model**; one that has had the later stages is usually called
an instruct or chat model. You can call a base model, and the result is instructive: give it
"What is the capital of France?" and it may well continue with "What is the capital of Spain?
 What is the capital of Italy?", because a list of questions is a thing documents contain. It
is not being unhelpful. It is doing the only job it was ever trained for.

**Preference optimisation** is the one that is genuinely different. Its data is not a single
correct answer. It is *pairs*: for the same request, one reply people preferred and one they
did not. Training adjusts the model to make the preferred kind more likely relative to the
other.

| | Data | What it gives | Rough share of the compute |
|---|---|---|---|
| **Pretraining** | Enormous, general, unlabelled text | Knowledge, language, code, structure | Nearly all of it |
| **Supervised fine-tuning** | Thousands to millions of request–response pairs, curated | Answering rather than continuing; format; tone | A small fraction |
| **Preference optimisation** | Pairs of replies, one preferred | Which of the things it could say it tends to say | A small fraction |

**And the sizes are worth putting numbers on, because the ratio is the point.** Orders of
magnitude, for a model of the moment:

```text
  pretraining     trillions of tokens
  fine-tuning     tens of thousands to a few million examples
  preference      tens of thousands of pairs
```

Put one pair of those side by side. Ten trillion tokens is about 7.5 trillion words, at Chapter
10's three-quarters of a word to the token — which at a hundred thousand words a book is
**seventy-five million books**. A hundred thousand
fine-tuning examples of five hundred tokens each is fifty million tokens — **one part in two
hundred thousand** of what the first stage saw.

```text
  pretraining     10,000,000,000,000 tokens
  fine-tuning             50,000,000 tokens

  the second is 0.0005 per cent of the first
```

That ratio is the whole argument of the last section of this chapter, arrived at by arithmetic
rather than by assertion. It is also where the compute shares in the table come from: the work
of training is dominated by running the loop over tokens, so a stage that sees one part in two
hundred thousand of the tokens accounts for about that share of the computation. A stage
that sees one part in two hundred thousand of the tokens cannot be where the *bulk* of a
model's knowledge came from. Note what that does and does not reach: it is a claim about share
of exposure, and it says nothing on its own about whether one small corpus comes back.

> **Note:** Those figures are dated details of the worst kind — they have moved by an order of
> magnitude more than once and will again. What does not move is the *shape*: the first stage
> is larger than the other two by a factor with many zeroes in it. Check the ratio, not the
> numbers.

> **Note:** The names vary and the boundaries blur. You will meet "instruction tuning" for the
> second stage, and "alignment", "RLHF" or "post-training" covering the second and third
> together. The three-way split by *what the data looks like* — raw text, correct answers,
> ranked pairs — is the durable version and the one to reason with.

## The Preference Objective

Chapter 8 said you should be able to read a formula by naming its symbols. Here is one worth
being able to recognise, because interviewers ask about it by name.

```{=latex}
\[ \mathcal{L}_{\text{DPO}} = -\log \sigma\!\left( \beta \log \frac{\pi(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right) \]
```

Name the symbols. `\(\mathcal{L}_{\text{DPO}}\)`{=latex} is this stage's own loss, and the
subscript is there because it is not the cross-entropy above. `\(x\)`{=latex} is the
request. `\(y_w\)`{=latex} is the reply people
preferred — *w* for winner — and `\(y_l\)`{=latex} the one they did not. `\(\pi\)`{=latex} is
the model being trained and `\(\pi_{\text{ref}}\)`{=latex} is the same model as it was before
this stage started, kept fixed as a reference. `\(\beta\)`{=latex} is a setting controlling how
hard to push. `\(\sigma\)`{=latex} is the logistic function, written `\(\sigma(z) = 1/(1 + e^{-z})\)`{=latex},
which squashes any number into the range 0 to 1 and gives exactly `\(0.5\)`{=latex} at zero.

In words, working outward from the inner brackets: for each of the two replies, take how much
*more* likely this model makes it than the reference model did. Subtract the loser's figure
from the winner's. The loss is small when that difference is large and positive. So the
procedure **raises the preferred reply's probability relative to the rejected one, measured
against where the model started** — and subtracting the loser's figure is what rules out the
easy win. Make *both* replies ten times more likely and the two figures each rise by the same
amount, so the difference is unchanged and the loss does not move. Only the gap counts. The
reference model in the denominators does something else: it sets the zero point, so both
figures are measured from where the model was before this stage began.

**And this is what the third stage does to the loop.** Step 2 no longer runs one model over
one stretch of text: it runs *two* models — the one being trained and the frozen reference —
over *two* replies, to get the four probabilities the formula needs. Step 3 then compares two
whole replies rather than scoring one next token. Steps 1 and 4 are unchanged.

This is **direct preference optimisation**, usually called DPO. It is stated here and not
derived; why this particular expression is the right thing to minimise is outside this book.

**But you can put numbers in it, and you should.** Take `\(\beta = 0.5\)`{=latex}, and write
`\(r_w\)`{=latex} and `\(r_l\)`{=latex} for the two logarithms — how much more likely this
model makes each reply than the reference did. They are logarithms, so
`\(r_w = 2\)`{=latex} means the winner has become `\(e^2 = 7.389\)`{=latex} times as likely
and `\(r_l = -1\)`{=latex} means the loser has fallen to `\(e^{-1} = 0.368\)`{=latex} of what
it was. Three cases:

```text
  state of training        r_w    r_l    arg    sigma   loss
  before this stage       0.0    0.0    0.0    0.500   0.693
  moved the right way     2.0   -1.0    1.5    0.818   0.201
  moved the wrong way    -1.0    2.0   -1.5    0.182   1.701
```

The middle column is `\(0.5 r_w - 0.5 r_l\)`{=latex}, and the loss is
`\(-\ln \sigma(\text{arg})\)`{=latex}. Check the first row by hand: both logarithms are zero,
so the argument is zero, `\(\sigma(0) = 0.5\)`{=latex}, and
`\(-\ln(0.5) = 0.693\)`{=latex}. **That row is where every example starts**, because at the
moment the stage begins the model *is* the reference.

Now the point from two paragraphs ago, in one line. Make both replies ten times more likely:
both logarithms rise by `\(\ln 10\)`{=latex}, the subtraction cancels it, and the loss stays
at 0.693. The model has changed and the objective has not noticed.

> **Note:** There is an older approach to the same job, where human rankings are used to train
> a separate model that scores replies, and the main model is then trained against that scorer.
> That is reinforcement learning from human feedback, RLHF. DPO's selling point is that it skips
> the separate scorer and optimises the preferences directly. Both are in use; the thing to be
> able to say is what the *data* is — pairs of replies with a preference between them — because
> that is what does not change.

## What Each Stage Cannot Do

This is the part with practical consequences, and it is where most expensive mistakes in this
material begin.

**No stage gives the model a way to look things up.** Chapter 1 said the model itself cannot
fetch anything, and no amount of training changes that. Training moves numbers; it does not
attach a database.

**Knowledge is overwhelmingly a pretraining phenomenon**, and that much is arithmetic. Whether
fine-tuning on a few thousand of your own documents installs their contents as recallable facts
is a separate question the ratio does not settle — a small curated set is exactly the case where
repeated exposure might help rather than hurt. What practitioners report is that it does not
work reliably, and Chapter 20 is how you would find out for your own case. The stage is
small, the examples are few, and what it is good at is shaping *how* the model responds rather
than *what it knows*. The reliable way to make a model use your information is still Chapter
1's: put the information in the request.

**And nothing in training is a test of whether anything is true.** Every stage optimises
agreement with text that people produced — tokens that continue a document, replies people
wrote, replies people preferred. None of those is a test of correctness. Chapter 16 is where
that becomes the characteristic failure of these systems.

> **Warning:** "We'll do some fine-tuning on our docs" is the most common wrong first answer in this
> field. It is not never right — Chapter 39 is about when it genuinely is, and what it costs
> you — but it is the last lever to reach for and not the first, and the reason is in this
> section rather than in anybody's opinion.

What each stage *can* do is worth stating just as plainly. Pretraining gives the model
essentially everything it knows. Supervised fine-tuning gives it a job and a format. Preference
optimisation
chooses between the things it was already capable of saying. That last one is the subtlest and
the most useful to be able to say out loud: **a preference stage is not where knowledge comes
from — nothing in its objective rewards adding any, and what it changes is which of its existing
behaviours come out.**

## Lab: Compute a Loss

Pen, paper and a calculator, then ten lines of Python. Twenty-five minutes, and there is a key
for every step.

A model with a vocabulary of four has just made three predictions. In each case the probability
it gave to the token that actually came next is shown.

```text
  position   token that came next    p
     1              yes            0.500
     2              no             0.250
     3              yes            0.125
```

The exponentials and logs you need: `\(\ln 2 = 0.693\)`{=latex}, `\(\ln 4 = 1.386\)`{=latex},
`\(\ln 8 = 2.079\)`{=latex}, `\(e^{1.386} = 3.999\)`{=latex}.

**Step 1.** Compute the cross-entropy loss for each of the three predictions.

*Expected result:* `\(-\ln(0.5) = \ln 2 = 0.693\)`{=latex};
`\(-\ln(0.25) = \ln 4 = 1.386\)`{=latex};
`\(-\ln(0.125) = \ln 8 = 2.079\)`{=latex}. Note what happened: each halving
of the probability added the same 0.693 to the loss. That is the logarithm of Chapter 8 doing
what logarithms do.

**Step 2.** Compute the average loss over the three positions, then the perplexity.

*Expected result:* `\((0.693 + 1.386 + 2.079)/3 = 4.158/3 = 1.386\)`{=latex}, and
`\(\exp(1.386) = 3.999\)`{=latex} — which is 4, since 1.386 is `\(\ln 4\)`{=latex} rounded.
The model was about as uncertain, on average, as a fair choice between four things — which
over a vocabulary of four means it did no better overall
than a uniform guess, even though it was better than uniform at position 1 and worse at
position 3.

**Step 3.** Without computing anything: the model is retrained and now gives the correct token
a probability of 1.0 at all three positions. What are the loss and the perplexity?

*Expected result:* loss 0 and perplexity 1. `\(-\log 1 = 0\)`{=latex} and
`\(\exp(0) = 1\)`{=latex}. A perplexity of 1 means no uncertainty at all — one option. It is
the
floor, and no model reaches it on real text, because real text is not perfectly predictable.

**Step 4.** The model gives the correct token 0.5 at position 1 and the *wrong* tokens 0.3,
0.1 and 0.1. A second model gives the correct token 0.5 and the wrong ones 0.48, 0.01 and 0.01.
Which has the lower loss at that position?

*Expected result:* **neither — they are identical, at 0.693.** The loss depends only on the
probability assigned to the token that actually came next. Everything the model thought about
the alternatives is invisible to it. This is worth meeting, because it is the first thing
people guess wrong about cross-entropy.

**Step 5.** In a new empty folder, save this as `loss.py` and run it:

```python
import math

# probability given to the token that actually came next
ps = [0.636, 0.234, 0.086, 0.636]

losses = [-math.log(p) for p in ps]
average = sum(losses) / len(losses)

for p, l in zip(ps, losses):
    print(f"  p={p:.3f}   -ln p = {l:.3f}")
print(f"average loss = {average:.3f}")
print(f"perplexity   = {math.exp(average):.3f}")
```

*Expected result:*

```text
  p=0.636   -ln p = 0.453
  p=0.234   -ln p = 1.452
  p=0.086   -ln p = 2.453
  p=0.636   -ln p = 0.453
average loss = 1.203
perplexity   = 3.329
```

Those are the chapter's own four positions. Note that the printed perplexity is 3.329 while
computing `\(e^{1.203}\)`{=latex} from the rounded average gives 3.330 — the program averaged
before rounding and you did not.

**Step 6.** Change the first probability to 0.001 and run it again. What happens to the
average,
and what does that tell you about one bad prediction in a long document?

*Expected result:* the loss at that position jumps to 6.908 and the average to 2.817, giving a
perplexity of 16.719. **One confidently wrong prediction dominated three reasonable ones.**
That
is the asymmetry from earlier in the chapter, and it is why one confidently wrong prediction
costs more than several mildly wrong ones.

**Step 7.** Name the three stages of training, say what data each one consumes, and say which
one your company would be changing by "fine-tuning on our support tickets".

*Expected result:* pretraining on enormous general text; supervised fine-tuning on curated
request–response pairs; preference optimisation on pairs of replies with a preference between
them. Fine-tuning on support tickets is the second stage, and what it would reliably change is
the *shape* of replies — tone, format, the house way of saying things. What it would not
reliably do is install the tickets' contents as facts the model can recall — reliably being the
word, since the ratio argument bounds the share of knowledge and not this particular case.

## Summary, Key Terms, and Review Questions

### Summary

Training optimises next-token prediction, and the text supplies its own answers, which is why
the first stage can consume so much of it. The objective is **cross-entropy**: the average of
`\(-\log p\)`{=latex} over every position, where `\(p\)`{=latex} is the probability the model
gave to the token that actually came next. It depends only on the correct token's probability,
it punishes confident wrongness without limit, and it is zero for a perfect prediction.
**Perplexity** is its exponential, and reads as the number of equally likely options the model
is effectively choosing between — a uniform choice among `\(V\)`{=latex} options has perplexity
`\(V\)`{=latex}. The loop is: run forward, compute the loss, move every parameter a little in
the direction that reduces it, repeat. That last step is
`\(\theta \leftarrow \theta - \eta \nabla_{\theta}\mathcal{L}\)`{=latex}, and it is the edge of
this book. Three stages use that loop on three kinds of data, the third with a loss of its own:
**pretraining** on enormous
general text, which is where essentially all knowledge comes from; **supervised fine-tuning**
on curated request–response pairs, which turns a text continuer into something that answers;
and **preference optimisation** on pairs of replies with a preference between them, stated once
as the DPO objective. No stage gives the model a way to look anything up, knowledge is
overwhelmingly a pretraining phenomenon, and nothing in training tests whether anything is
true.

### Key Terms

| Term | Meaning |
|---|---|
| **Cross-entropy** | The training objective: the average of `\(-\log p\)`{=latex} over every position, where `\(p\)`{=latex} is the probability given to the token that actually came next. Zero for a perfect prediction, unbounded for a confident mistake |
| **Perplexity** | The exponential of the cross-entropy. Reads as the number of equally likely options the model is effectively choosing between; a uniform choice among `\(V\)`{=latex} options has perplexity `\(V\)`{=latex} |
| **Gradient** | For each parameter, how much the loss would rise if that parameter rose. The update rule moves every parameter a small step against it. How it is computed is outside this book |
| **Pretraining** | Running the loop on an enormous quantity of general text. Where essentially all of a model's knowledge comes from, and nearly all of the computation |
| **Supervised fine-tuning** | Running the same loop with the same objective on curated request–response pairs. Turns a model that continues text into one that answers |
| **Base model** | A model that has had only pretraining. It continues text rather than answering, which is what the later stages change |
| **Direct preference optimisation (DPO)** | The preference objective written as one formula: raise the preferred reply's probability relative to the rejected one, both measured against the model as it was before this stage. Stated in this book, not derived |
| **Preference optimisation** | Training on pairs of replies with a preference between them, to make the preferred kind more likely relative to the other. Changes which of its existing behaviours come out; nothing in its objective rewards adding knowledge |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The objective | `\(\mathcal{L} = -\frac{1}{N}\sum_i \log p(t_i \mid t_1 \ldots t_{i-1})\)`{=latex} |
| Perplexity | `\(\exp(\mathcal{L})\)`{=latex}; a uniform choice among `\(V\)`{=latex} options gives `\(V\)`{=latex} |
| The update rule | `\(\theta \leftarrow \theta - \eta \nabla_{\theta}\mathcal{L}\)`{=latex} — and that is the edge of this book |
| The three stages | Pretraining, supervised fine-tuning, preference optimisation |
| Where knowledge comes from | Pretraining, overwhelmingly |
| What the loss ignores | Everything except the probability of the token that actually came next |

### Review Questions

1. Name the training stages and say what each one changes.
2. Why can the first stage consume so much more data than the other two?
3. A model gives the correct next token a probability of 0.5. Another gives it 0.5 but is
much more confident about its second choice. Which has the lower loss?
4. What does a perplexity of 20 mean, and what would you need to know before comparing it
with somebody else's figure?
5. Your colleague wants to do some fine-tuning on the company's documents so the model
"knows" them. What do you say?
6. Which line of this chapter is the edge of the book, and what is on the other side of it?

### Review Answers

1. **Pretraining** runs next-token prediction over an enormous quantity of general text; it is
where essentially all the model's knowledge of language, facts, code and structure comes from,
and it accounts for nearly all the computation. What it produces continues text rather than
answering. **Supervised fine-tuning** runs the same loop with the same cross-entropy objective
on a much smaller set of curated request–response pairs, which turns a continuer into something
that answers, and sets format and tone. **Preference optimisation** uses pairs of replies
with a
preference between them and shifts which of the model's existing behaviours come out; it does
not where knowledge comes from, because nothing in its objective rewards adding any.
2. Because its data needs no labels. Cut any text anywhere: what comes before is the input and
the next token is the correct answer, so a thousand-token document is a thousand examples and
the text is its own answer key. The other two stages need curated material — someone writing a
good response, or people choosing between two replies — which is slow and expensive per
example.
3. Neither; they are identical. Cross-entropy is `\(-\log p\)`{=latex} of the token that
*actually came next*, so what the model believed about every other token is invisible to the
loss. Two models that agree on the correct token's probability score the same however
differently they spread the rest.
4. That the model was about as uncertain as a fair choice between twenty options, on the text
it was measured on. Before comparing it you would need to know that the figure is over the same
text, and above all that the tokeniser matches — a model whose vocabulary cuts the text
into fewer pieces is being asked a different question, so the numbers are not comparable. And
perplexity measures prediction of particular text, not whether answers are correct or useful.
The one thing you do *not* need to check is the logarithm base: a base-2 loss is about 1.44
times a natural one, and exponentiating in the matching base cancels that exactly, so two
perplexities over the same text agree whichever base was used to compute them.
5. That it is the last lever rather than the first, and that the stage they are reaching for
shapes *how* the model responds rather than *what it knows*. Knowledge is overwhelmingly a
pretraining phenomenon — that part is arithmetic — and practitioners report that a few thousand fine-tuning examples do not reliably install their
contents as recallable facts, and nothing in training attaches a database. The reliable way to
make the model use the documents is to put the relevant parts in the request. Chapter 39 is
where fine-tuning is genuinely the right answer, and what it costs.
6. `\(\theta \leftarrow \theta - \eta \nabla_{\theta}\mathcal{L}\)`{=latex} — move every
parameter a small step in the direction that reduces the loss. On the other side of it are how
the gradient is computed for billions of parameters, which is backpropagation; why repeating
the rule arrives anywhere useful, which is optimisation theory; and how the step size is chosen
and adjusted, which is optimiser design. Chapter 17 lists all three, and the right thing to say
is that the boundary is deliberate.

> **You understand this when** you can write the training objective down, say what each of the
> three stages changes, and name the one line whose explanation you are deliberately skipping.
