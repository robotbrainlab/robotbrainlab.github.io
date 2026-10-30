# The Stack: Layers and the Residual Stream

Chapter 11 opened half of a layer. This chapter opens the other half, puts the two together,
and then stacks the result ninety-six times. It also answers a question that sounds reasonable
and has no good answer — where in a model a particular fact is kept — and it is worth knowing
why the question is wrong rather than merely being told it is.

*The problem.* One attention step is clear enough. A model has ninety-six of them and I don't
know what that accumulates.

*The question.* What does a layer actually do to the vectors passing through it, what is left
after ninety-six of those, and where do the parameters sit?

## A Layer Does Not Replace, It Adds

Start with the single most useful fact about the design, because it is not what people expect.

A layer does not take a vector and hand back a different vector. It takes a vector, works out
a *change*, and adds that change to what it was given:

```text
  out  =  in  +  (something computed from in)
```

That addition is called a **residual connection**, and the vector being added to as it passes
up through the stack is the **residual stream**. It starts as the token's embedding, with
whatever Chapter 11's positional encoding adds to it, and from there everything a layer
computes is written into that one running vector, by addition, one contribution at a time.

A picture that helps, with the usual caution about pictures. Think of the residual stream as a
long document that every layer may annotate. A layer reads the whole document, decides what to
add, and appends its contribution. It cannot erase what is there — it can only add something
that cancels it out — and the next layer reads the sum of everything written so far.

Where that picture stops being accurate: the contributions are not kept separate. They are
added into the same four thousand numbers, so once two layers have written, no inspection of
the result can separate them. That matters later in this chapter.

**Why build it this way rather than letting each layer transform the vector outright?** One
reason is plain enough to state without any theory: if each layer only ever *adds*, then a
layer with nothing useful to contribute can add approximately nothing and the information
already in the stream passes through untouched. A stack where each layer replaced its input
would have to relearn, at every level, how to carry forward what it did not want to change.

## What Is in a Layer

Each layer makes two contributions to the stream, not one, and each gets its own residual
connection.

```text
  x                      the stream arriving

  x  =  x + attention(x)      the attention block writes
  x  =  x + feedforward(x)    the feed-forward block writes

                         the stream leaving, same width
```

The **attention block** is Chapter 11 in full: queries, keys, values, the grid, the mask,
softmax, the blend, the heads and their mixing matrix. Its defining property is that it moves
information *between positions*. It is the only part of the model that does.

The **feed-forward block** is the other half, and it is the opposite: it works on each
position entirely on its own, with no reference to any other position. Position 5's vector
goes in, position 5's contribution comes out, and if you deleted every other token it would
make no difference to this block at all.

| | Attention block | Feed-forward block |
|---|---|---|
| Looks at | Every position | One position, in isolation |
| What it is | Chapter 11's formula | Two matrices with a function between them |
| Cost grows | With `\(n^2\)`{=latex} | With `\(n\)`{=latex} |
| Share of a layer's parameters | Smaller | Larger — the arithmetic is below |

So a layer is: *gather from elsewhere, then think about it here.* Twice per layer, ninety-six
times over, into one running vector.

## The Feed-Forward Block, Worked

It is two matrix multiplications with one non-linear step between them, and the middle is
*wider* than the ends. That middle width is written `\(d_{ff}\)`{=latex}, and it runs from
about two and a half times the width to four times it, depending on the design — the smaller
end being usual where the block has three matrices rather than two.

```text
  width 4  -->  [ W_up ]  -->  width 8  -->  activation
                                              |
  width 4  <--  [ W_down ]  <--  width 8  <---
```

Carry on with Chapter 11's example. Its worked attention produced
`\((0.216,\ 3.378,\ 1.879,\ 1.013)\)`{=latex} for position 5, whose vector arriving at the
layer was `\((2, 0, 2, 0)\)`{=latex}. The attention block's residual connection adds them:

```text
  arriving        (2,     0,     2,     0    )
  attention   +   (0.216, 3.378, 1.879, 1.013)
                  ---------------------------
  stream now      (2.216, 3.378, 3.879, 1.013)
```

That sum is what the feed-forward block receives. Here is `\(W_{up}\)`{=latex}, eight rows of
four, chosen so you can follow it:

```text
  W_up = [  1  1  0  0 ]      [  1 -1  0  0 ]
         [  0  1  1  0 ]      [  0  1 -1  0 ]
         [  1  0  0  1 ]      [  0  0  1 -1 ]
         [  0  0  1  1 ]      [ -1  0  1  0 ]
```

Rows 1 to 4 add pairs of slots. Rows 5 to 8 *subtract* them, which is the interesting part.
Multiplying out:

```text
  row 1   2.216 + 3.378  =   5.594
  row 2   3.378 + 3.879  =   7.257
  row 3   2.216 + 1.013  =   3.229
  row 4   3.879 + 1.013  =   4.892
  row 5   2.216 - 3.378  =  -1.162
  row 6   3.378 - 3.879  =  -0.501
  row 7   3.879 - 1.013  =   2.866
  row 8   3.879 - 2.216  =   1.663
```

Now the **activation function**, which is the one step in this block that is not a matrix
multiplication. The simplest and the one you can do in your head is to keep positives and
replace negatives with zero:

```text
  before  5.594 7.257 3.229 4.892 -1.162 -0.501 2.866 1.663
  after   5.594 7.257 3.229 4.892  0.000  0.000 2.866 1.663
```

**Look at what that did.** Rows 5 to 8 were comparisons — is slot 1 bigger than slot 2, is
slot 3 bigger than slot 4. Two of them came out negative and have been switched off entirely.
So what passes on from here depends on *which comparisons held*, and that is something no
amount of matrix multiplication can do on its own: multiplying by a matrix and then by another
matrix is the same as multiplying by one combined matrix, however many you put in a row.
Without the activation, this block's `\(W_{up}\)`{=latex} and `\(W_{down}\)`{=latex} would do
no more than a single 4-by-4 matrix could, and no condition could be expressed in it at all.

Then `\(W_{down}\)`{=latex} takes the eight back to four:

```text
  W_down = [ 0 1 0 0 1 0 0 1 ]
           [ 1 0 0 1 0 1 0 0 ]
           [ 0 0 1 0 0 0 1 0 ]
           [ 0 1 1 0 0 0 0 1 ]
```

```text
  row 1   7.257 + 0.000 + 1.663          =   8.920
  row 2   5.594 + 4.892 + 0.000          =  10.486
  row 3   3.229 + 2.866                  =   6.095
  row 4   7.257 + 3.229 + 1.663          =  12.149
```

And the second residual connection adds that to the stream:

```text
  stream       ( 2.216,  3.378,  3.879,  1.013)
  feed-forward ( 8.920, 10.486,  6.095, 12.149)
               ------------------------------
  stream now   (11.136, 13.864,  9.974, 13.162)
```

**That is one complete layer.** A vector of four numbers went in, two blocks wrote into it, and
a vector of four numbers came out — ready for the next layer, which will do the same thing with
its own numbers.

> **Warning:** You will often hear the stronger version of this — that without the activations
> the whole stack would collapse into one matrix. That is not true, and Chapter 11's numbers
> show why: attention is not a linear step either. Double every input vector in Chapter 11's
> example and its output does not double. It goes from `\((0.216, 3.378, 1.879, 1.013)\)`{=latex}
> to `\((0.001, 7.996, 3.999, 2.000)\)`{=latex}, because softmax turned the weights
> `\((0.095, 0.702, 0.095, 0.095, 0.013)\)`{=latex} into
> `\((0.000, 0.999, 0.000, 0.000, 0.000)\)`{=latex}, which print as adding to 0.999 for the
> rounding reason you have met twice — the saturation of Chapter 11's scaling section, arriving
> uninvited. **The collapse argument is about the block, not the stack.** It
> is still the reason the activation is there.

> **Note:** Real models use a smoother activation than the keep-positives rule above, and most
> now use a gated form with three matrices rather than two. The shape of the argument does not
> change: two or three matrices, a non-linear step, applied at each position on its own, with
> the middle wider than the ends.

## Normalisation

One step has been left out of the diagram, and it belongs in a sentence.

Before each block reads the stream, the stream is **normalised** — rescaled so its numbers sit
in a predictable range, with a small set of learned parameters allowing the scale to be
adjusted.

Why it is there: **without it the numbers grow as contributions are added layer after layer,
and a very deep stack stops computing reliably.** That is the whole of the honest answer, and
this book does not go further, because the rest of it is a subject — numerical stability — that
Chapter 17 lists among the things you are not going to be able to explain.

> **Tip:** This is a good example of a question where the right interview answer is short and
> stops. "It keeps the scale of the stream under control as layers add to it, which matters
> because the stack is deep" is correct and complete at this level. Reaching for more is how
> people talk themselves into trouble.

## Ninety-Six of Them

Now stack it. Every layer has the same shape and its own numbers — Chapter 9's point, now with
the inside visible — and the stream arrives at the end carrying the sum of every contribution
made along the way. Depths of a few dozen to a hundred are usual; the worked model later in
this chapter has thirty-two layers, and the arithmetic is the same at any depth.

The design now has all of its pieces, and it has a name. A stack of identical layers, each one
an attention block and a feed-forward block with a residual connection and a normalisation
step, is a **transformer**; where Chapter 11's mask is in place, so that every position may
look only backwards, it is called *decoder-only*. That is the shape of every model this book
has shown producing a next token. An interviewer will use the word for the whole design, and
what it refers to is what Chapters 11 and 12 have built — not an account of why it works,
which is on Chapter 17's list.

**And there is a second arrangement, which this book uses without ever having named it.** Take
Chapter 11's mask away and every position may look in both directions; the stack then has no
next token to produce, and what it gives you instead is a vector per position computed with the
whole sequence in view. That is *encoder-only*, and it is what Chapter 24's embedding models
are — the thing that turns a document into the fixed-width vector this book has been retrieving
with since Chapter 24. Chapter 26's bi-encoder and cross-encoder are a different question laid
on top of this one: that is whether you encode two texts separately or together, where this is
whether a position may look forwards.

> **Note:** The two arrangements have well-known model families attached, one each, and the
> question is usually asked by naming them rather than by describing them. Those names are
> Chapter 6's *dated detail* and the arrangement is not, which is why the mask is the thing to
> hold: *encoder-only* reads the whole sequence and produces representations, *decoder-only*
> looks backwards and produces continuations, and an encoder-only stack is the right shape for
> search and classification for the same reason it cannot write you a sentence.

What more layers let the model do is easy to say at the level of mechanism: more layers means
more separate opportunities to gather from other positions and more separate opportunities to
compute something at each position.

And the second layer is where that stops being abstract. The vector this chapter built —
`\((11.136,\ 13.864,\ 9.974,\ 13.162)\)`{=latex} — is what passes into layer 2 at position 5. It is not the embedding of "it" any more. It is the embedding of "it" plus what
position 5 gathered from "cat" plus what the feed-forward block made of the two together, and
layer 2's queries and keys are computed from *that*. So position 5 now offers a different key
to every other position than it did at layer 1, and asks a different question.

**That is what depth buys, mechanically: each round gathers from, and computes on, what the
last round assembled.** A result put together at layer 20 is available to be gathered from, by a
different position, at layer 21 — and the thing being gathered did not exist in the input at
all.

**And then there is the part nobody can tell you.** *Why* a deeper stack is better at the
things these models are better at — why thirty-two layers beats sixteen by more than it costs,
where the returns stop — is an open question in the research, not a settled explanation anybody
is keeping from you. It is on Chapter 17's list, and the honest version in an interview is "the
mechanism is more rounds of gather-and-compute; why depth buys what it buys is not something I
can derive, and nobody has a clean account of it."

> **Warning:** You will meet confident stories about what particular layers "do" — early layers
> handle syntax, middle layers handle facts, late layers handle output format. There is real
> measurement behind some of this, and it is a finding about particular models arrived at by
> probing them, not a design anybody specified and not shown to be a rule that transfers. Treat it the way
> Chapter 6 says to treat any claim: ask what it was measured on.

## Where Is the Fact Stored?

This is the question, and it is worth being precise about why it has no clean answer.

The question assumes a filing system: that somewhere in the model there is a place holding
*Paris is the capital of France*, which could in principle be pointed at. Nothing in the
mechanism supports that assumption, for three reasons that are each visible in the arithmetic
above.

**Everything is added into the same numbers.** The stream at position 5 after one layer was
`\((11.136,\ 13.864,\ 9.974,\ 13.162)\)`{=latex}. Which part of that came from attention, which
from the feed-forward block, which was the original token? The three contributions were
`\((2,0,2,0)\)`{=latex}, `\((0.216, 3.378, 1.879, 1.013)\)`{=latex} and
`\((8.920, 10.486, 6.095, 12.149)\)`{=latex} — but having added them, there is no operation
you can perform on the result that recovers them. A sum does not say what was added. Ninety-six
layers in, the stream is a sum of a very large number of contributions and nothing marks where
any of them came from.

**No parameter belongs to anything.** `\(W_{down}\)`{=latex}'s row 3 above was used to compute
part of this token's contribution, and the identical row will be used again on unrelated tokens
in unrelated sentences. A parameter is not allocated to a
fact. It is used again on input after input, with nothing to say which of them it was for.

**And a fact is not a thing the model holds.** What the model holds is numbers that make
likely continuations likely. "Paris" being a probable continuation of "the capital of France
is" is a property of how the whole computation lands, in the same way that a bridge's ability
to hold a lorry is a property of the bridge rather than of a part of it you could point to.

So the honest answer to "where is it stored" is: **it is not stored anywhere, in the sense the
question means.** What can be said is weaker and true. Measurement can show that changing
particular parameters changes particular behaviour — that is a real research result and
techniques exist that exploit it. What it does not show is an address, and a model with
billions of parameters contributing to every output does not have one.

> **Note:** This is not a limitation of current understanding that better tools will clear up.
> The filing-system picture is wrong about the mechanism rather than merely incomplete, which
> is why "we don't know yet" is a worse answer than "the question assumes something that is
> not there".

## Where the Parameters Actually Sit

Chapter 9 said a parameter is a fitted number and that the count is what a model's name
reports. Now you can see where they are. Take a model of a common shape: width 4,096, a
feed-forward middle of 11,008, and 32 layers.

**One attention block.** Four matrices — `\(W_Q\)`{=latex}, `\(W_K\)`{=latex},
`\(W_V\)`{=latex} and the mixing matrix `\(W_O\)`{=latex} — each 4,096 by 4,096:

```text
  4,096 x 4,096 = 16,777,216
  16,777,216 x 4 = 67,108,864
```

**One feed-forward block.** Two matrices, 4,096 by 11,008 and back:

```text
  4,096 x 11,008 = 45,088,768
  45,088,768 x 2 = 90,177,536
```

**One layer, and then all of them.**

```text
  attention        67,108,864
  feed-forward     90,177,536
                  -----------
  one layer       157,286,400
  x 32 layers   5,033,164,800
```

Two things in that table are worth carrying.

**The feed-forward block holds more parameters than attention does** — 57 per cent of a layer
here — even though attention is the part everybody talks about and the part that was hard to
understand. The thing that gathers between positions is the cheaper half.

**And the layers hold almost everything.** Add Chapter 9's embedding table at a vocabulary of
128,000:

```text
  the layers   5,033,164,800
  embedding      524,288,000    counted once, as in the
                                models that reuse it for
                                the output step (ch 9)
               --------------
               5,557,452,800
```

About nine parameters in ten are in the stack. That is why "where do the parameters sit" has
a short answer — *in the layers, mostly in the feed-forward blocks* — even though "where is the
fact" has none.

> **Note:** The three shape numbers above are illustrative of a common size and not any
> particular model. Widths, feed-forward multipliers and depths all vary, newer designs add
> matrices the arithmetic above does not count, and the count a model is sold under may include
> or exclude the embedding table. The *method* — count a matrix, multiply by how many of them
> there are — is what transfers.

## Lab: One Layer, By Hand

Pen, paper and a calculator. Twenty-five minutes, and there is a key for every step. Nothing
to install.

The stream arriving at a position is `\((1, 2, 0, 1)\)`{=latex}, and this layer's attention
block has computed a contribution of `\((0.5, -1, 3, 1)\)`{=latex}.

**Step 1.** Apply the attention block's residual connection. What is the stream now?

*Expected result:* `\((1.5,\ 1,\ 3,\ 2)\)`{=latex}. Add, do not replace — if you wrote
`\((0.5, -1, 3, 1)\)`{=latex} you have done what most people expect a layer to do, and it is
the thing this chapter exists to correct.

**Step 2.** The feed-forward block uses the same `\(W_{up}\)`{=latex} as the chapter. Compute
all eight numbers.

*Expected result:*

```text
  row 1   1.5 + 1    =   2.5       row 5   1.5 - 1    =   0.5
  row 2   1   + 3    =   4.0       row 6   1   - 3    =  -2.0
  row 3   1.5 + 2    =   3.5       row 7   3   - 2    =   1.0
  row 4   3   + 2    =   5.0       row 8   3   - 1.5  =   1.5
```

**Step 3.** Apply the activation. Which slots are switched off, and what does that tell you
about what this block can express?

*Expected result:* only row 6, which becomes 0. Everything else is already positive. The block
can express a condition — *this signal passes on only when slot 2 exceeds slot 3* — and that
is something no sequence of matrix multiplications could do by itself, because a product of
matrices is just another matrix.

**Step 4.** Apply the chapter's `\(W_{down}\)`{=latex} to those eight numbers.

*Expected result:*

```text
  row 1   4.0 + 0.5 + 1.5          =   6.0
  row 2   2.5 + 5.0 + 0.0          =   7.5
  row 3   3.5 + 1.0                =   4.5
  row 4   4.0 + 3.5 + 1.5          =   9.0
```

**Step 5.** Apply the second residual connection. What leaves the layer?

*Expected result:* `\((1.5, 1, 3, 2) + (6, 7.5, 4.5, 9) = (7.5,\ 8.5,\ 7.5,\ 11)\)`{=latex}.
Note the width: four in, four out, which is what lets the next layer run at all.

**Step 6.** Someone asks you which part of `\((7.5, 8.5, 7.5, 11)\)`{=latex} came from the
attention block. What do you answer, and what would you need to answer it?

*Expected result:* you cannot tell from the vector. You happen to know, because you did the
addition and still have the pieces on your page — but the vector itself does not carry them,
and the model keeps no record. You would need the inputs and all the matrices, and to redo the
computation. After ninety-six layers nobody has that on a page.

**Step 7.** A model has a width of 2,048, a feed-forward middle of 5,632, and 24 layers. How
many parameters are in its layers, and what share is feed-forward?

*Expected result:*

```text
  attention     2,048 x 2,048 x 4 = 16,777,216
  feed-forward  2,048 x 5,632 x 2 = 23,068,672
  one layer                          39,845,888
  24 layers                         956,301,312
```

The feed-forward share is `\(23{,}068{,}672 / 39{,}845{,}888 = 0.579\)`{=latex}, so about 58
per cent — the same story as the chapter's larger example, because the ratio depends on the
feed-forward multiplier and not on the size.

**Step 8.** Without computing: your 24-layer model is replaced by a 48-layer one of the same
width. Roughly what happens to the parameter count, and what happens to the attention cost on a
long input?

*Expected result:* the layer parameters roughly double, since each layer holds the same number
and there are twice as many. The attention cost also doubles, because `\(O(n^2 d)\)`{=latex} is
per layer and there are twice as many layers — depth multiplies the cost, it does not change
how it grows with `\(n\)`{=latex}.

## Summary, Key Terms, and Review Questions

### Summary

A layer does not replace the vector it is given; it computes a change and **adds** it, which is
a **residual connection**, and the running vector every layer adds into is the **residual
stream**. Each layer writes twice: the **attention block** of Chapter 11, which is the only
part that moves information between positions, and the **feed-forward block**, which works on
each position in isolation — two matrices with an **activation function** between them and a
middle between about two and a half and four times the width of the ends. The activation is what stops that block's two matrices from
collapsing into one, and it is where a condition is expressed — not, as is often said, what
stops the whole stack collapsing, since attention is not a linear step either. The stream is
**normalised** before each block, which keeps its numbers in range as a deep stack adds to it.
More layers means more rounds of gather-and-compute; why depth buys what it buys is on Chapter
17's list. **Where a fact is stored has no clean answer** because contributions are added into
the same numbers and cannot be separated afterwards, because a parameter is used again on input
after input rather than belonging to anything, and because what the model holds is numbers that
make likely continuations likely rather than facts at addresses. Most parameters sit in the layers, and more of them in
the feed-forward blocks than in attention — about 57 per cent of a layer at a common shape, with
roughly nine in ten of all parameters in the stack rather than the embedding table.

### Key Terms

| Term | Meaning |
|---|---|
| **Residual connection** | Adding a block's output to the vector that went into it, rather than replacing it. What lets a layer contribute nothing and pass its input through |
| **Residual stream** | The running vector passing up through the stack, which every block adds into. By the end it is a sum of every contribution made along the way, with nothing marking which is which |
| **Attention block** | The half of a layer that moves information between positions — Chapter 11's formula in full. The only part of a model that does |
| **Feed-forward block** | The half of a layer that works on each position alone: two matrices with an activation between them, the middle between about two and a half and four times the width of the ends. Holds more of a layer's parameters than attention does |
| **Activation function** | The step in the feed-forward block that is not a matrix multiplication, such as keeping positives and zeroing negatives. Without it the block's two matrices would collapse into one |
| **Transformer** | A stack of identical layers, each adding an attention block's output and a feed-forward block's output into the residual stream. *Decoder-only* adds that every position may look only backwards |
| **Normalisation** | Rescaling the stream to a predictable range before each block reads it, so the numbers do not grow out of hand as layer after layer adds to them |

### Worth Memorising

| Item | Value or formula |
|---|---|
| What a layer does | `\(x \leftarrow x + \mathrm{attention}(x)\)`{=latex}, then `\(x \leftarrow x + \mathrm{feedforward}(x)\)`{=latex} |
| Attention block parameters | `\(4d^2\)`{=latex} — four matrices of `\(d \times d\)`{=latex} |
| Feed-forward block parameters | `\(2 \times d \times d_{ff}\)`{=latex}, with the middle width `\(d_{ff}\)`{=latex} between about `\(2.5d\)`{=latex} and `\(4d\)`{=latex} |
| Which half is bigger | Feed-forward, at roughly 57 per cent of a layer |
| Where the parameters are | In the layers — about nine in ten, at a common shape |
| Matrices compose | `\(W_2(W_1 x) = (W_2 W_1)x\)`{=latex}, which is why a block without its activation is one matrix |

### Review Questions

1. What is the residual stream, and what does a layer do to it?
2. Why does "where is that fact stored in the model" have no clean answer?
3. What would go wrong if you removed the activation function from every feed-forward block?
4. Which of a layer's two blocks holds more parameters, and which costs more on a long input?
5. Why is normalisation there? Answer in one sentence and stop.
6. A colleague says layer 40 of a model "is where it does arithmetic". What do you ask?

### Review Answers

1. It is the running vector that passes up through the stack, one per position. A layer does
not replace it: it computes a change and adds it, twice — once from the attention block, which
gathers from other positions, and once from the feed-forward block, which works on this
position alone. Because each block only adds, a layer with nothing to contribute can add
nearly nothing and the stream passes through. By the end the stream is a sum of every
contribution every layer made.
2. Because the mechanism has no addresses. Every block's output is *added* into the same
numbers, and a sum does not say what was added, so after a few layers nothing in the stream
marks what came from where. A parameter is used again on input after input, so no parameter belongs to a
fact. And what the model holds is numbers that make a likely continuation likely,
not propositions in slots. Measurement can show that changing particular parameters changes
particular behaviour, which is real, but that is not an address.
3. Every feed-forward block would collapse. A matrix multiplication followed by another is a
single matrix multiplication, so without a non-linear step between them the block's two
matrices would do no more than one matrix of the same shape, and no condition could be
expressed in it — *pass this on only when that comparison holds*, which is why the chapter's
example sends differences through it. Note what would **not** happen: the whole stack would not
collapse to one matrix, because attention is not linear either. That is the common overstated
version of this answer.
4. The feed-forward block holds more parameters, at roughly 57 per cent of a layer at a common
shape, because its two matrices are 4,096 by 11,008 while attention's four are 4,096 by 4,096. But attention costs more on a long input, because its work
grows with `\(n^2\)`{=latex} and the feed-forward block's grows with `\(n\)`{=latex} — it is
applied at each position independently. More parameters and more cost are different questions.
5. It keeps the scale of the stream under control as layer after layer adds to it, which
matters because the stack is deep. That is the whole answer at this level, and the rest of it
is a subject this book deliberately does not teach.
6. What it was measured on, and how. There is genuine work probing what particular layers
respond to, and it produces findings about particular models rather than rules that transfer —
so the questions are which model, which probe, and whether anybody has shown the same thing
elsewhere. The mechanism gives no reason to expect a layer to have a job, since every layer has
the same shape and differs only in the numbers training left in it.

> **You understand this when** you can say what a layer adds to, in what order, and why that
> makes "which part of this vector came from attention" an unanswerable question.
