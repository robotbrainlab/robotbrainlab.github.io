# What the Model Is Made Of

Chapter 1 held the model as a black box: text in, text out, charged by the amount. This
chapter opens the box and names the three things inside it. By the end you will be able to
say what shape the input takes, what shape the output takes, and what sits between them —
and you will have run one whole pass of a very small model with a pen.

*The problem.* I know text goes in and text comes out. I don't know what is in between, or
what shape it has.

*The question.* What are the actual pieces, what shape is each one, and what does a single
call make the model compute?

## The Short Answer

Three stages, in order, every time.

```text
  text  -->  a list of whole numbers
             one number per piece of text, from a fixed list

  numbers  -->  a list of vectors
                each number is a row looked up in a table

  vectors  -->  a stack of layers  -->  one vector
                then one score per entry in the fixed list,
                turned into probabilities that add to 1
```

So the thing you get back from a single call is not a word. It is a **probability
distribution**: one number for every entry the model is able to produce, saying how likely
that one is to come next. Something outside the model then picks one. That pick, and
the settings that steer it, belong to Chapter 13.

Everything else in this chapter is detail on those three stages, plus one fact that follows
from them and surprises nearly everybody: a single pass produces exactly one of those
distributions, so a hundred-token reply is a hundred passes.

## From Text to Numbers

A model does not work on letters or on words. Before anything else happens, your text is cut
into pieces, and each piece is replaced by its position in a fixed list.

That fixed list is the model's **vocabulary**: every entry the model can read or produce,
numbered. Nearly all of them are pieces of text, and a handful are not — Chapter 13 meets one
of those. A vocabulary is built once, before training, and does not change while
you are using the model.
Each piece is called a token, and tokens are what you are billed for.

```text
  "the cat sat"  -->  ["the", " cat", " sat"]  -->  [0, 1, 2]
```

Three facts about the vocabulary are worth having now, because the rest of the chapter leans
on them.

**It is finite and fixed.** A model with a vocabulary of 128,000 entries can produce those
128,000 things and nothing else. Any text it writes is a sequence drawn from that list.

**The pieces are not words.** They are usually fragments — part of a word, a word with its
leading space, a punctuation mark. This is why asking a model to count the letters in a word
asks about something the piece does not carry: a piece arrives as a seat number, and a seat
number is not spelled. Chapter 10 is where that is worked out properly.

**Every token is just an index.** The number is a seat number, not a quantity: nothing in
the model treats token 1 as one more than token 0. It is used to find a row and for nothing
else.

> **Note:** Why the pieces are fragments rather than words, how the list is built, why your
> short question can cost more than somebody else's long one, and how to count tokens before
> you send them — all of that is Chapter 10, which is where tokens are taught properly. For
> this chapter you need only the shape: a fixed numbered list, and your text arriving as a
> list of indexes into it.

## The Embedding Table: Coordinates Nobody Chose

An index is useless for arithmetic, so the first thing the model does with it is look it up.

The **embedding table** is a matrix with one row per vocabulary entry. Each row is a vector,
and looking up that row is how a token enters the model: from here on the arithmetic works
on the vector and never on the token. The rows are called embeddings. A vocabulary of 128,000 entries and vectors of 4,096 slots makes a table of
128,000 × 4,096 numbers:

```text
  128,000 x 4,096 = 524,288,000 numbers
```

Half a billion numbers, and that is before a single layer. The number of slots in each
row — 4,096 here — is the model's **width**, and it is the same number all the way through:
the vectors going into and out of every layer have that many slots. Width is usually written
`\(d\)`{=latex} in formulas. Other shapes do appear *inside* a layer — Chapter 8's
"shape 4096 × 11008" was one of them — and Chapter 12 is where those live.

Looking up three tokens gives three rows, which is a 3 × 4,096 matrix: one vector per
position, in the order you sent them.

**Position is supplied separately, and this is worth knowing before anybody asks.** A row
says *which* token this is. It says nothing about *where* in the input the token sits, and
the two rows for a word used twice in a sentence are the same row. So the model is given the
position as well. Chapter 11 is where it arrives, and why leaving it out would make word
order invisible.

**Now the part that matters, and it is the honest answer to a question interviewers ask.**
Nobody chose those coordinates. They are not a description of the token written down by a
linguist; no committee decided that slot 57 would be about cooking. They are **whatever made
next-token prediction work** — the training process adjusted them until the model got better
at guessing what comes next, and these are the numbers it stopped at. And no dimension means
anything. You cannot read slot 57 of any row and say what it is for.

That is not a simplification for beginners. It is the state of the art, and it is why
Chapter 8 told you a single slot usually names nothing.

> **Warning:** You will meet confident explanations of what the dimensions of an embedding
> "represent". Treat any such claim as something to check rather than something to repeat.
> The rows are certainly not random — they were fitted, and how they sit relative to each
> other is useful. Chapter 24 covers the separate models built to produce vectors you can
> search with, which is where that usefulness is put to work.
> But *why* the arrangement carries meaning at all is a question this book does not answer,
> and Chapter 17 lists it among the things you will not be able to explain when you finish.

## A Stack of Identical Layers

The list of vectors now goes through a stack.

A **layer** is a block of arithmetic that takes one vector per position and returns one
vector per position, with the same width in as out. The layers are **identical in shape and
different in content**: every one is built the same way, and every one holds its own numbers,
fitted separately. A model with 32 layers runs 32 blocks of the same shape, in order, and
each of them has its own set of numbers. That number of layers is the model's **depth**.

```text
  rows  -->  layer 1  -->  layer 2  -->  ...  -->  layer 32
             |            |                        |
             same width in and out, every time
```

Two consequences of "same width in and out".

**The stack can be any depth.** Because the shape coming out of a layer is the shape going
into one, you can put thirty-two of them in a row, or ninety-six, without changing anything
else. That is the whole reason the design *can be* scaled by stacking. What more depth buys is
Chapter 12's, and why it buys it is on Chapter 17's list.

**There is no loop.** The vectors go through layer 1, then layer 2, and so on to the end,
once. Nothing goes back. The model does not re-read or reconsider, and one pass over a hard
question costs exactly what one pass over an easy one of the same length costs: the same
amount of arithmetic runs either way. Chapter 16 is where that fact turns into something you can use.

What is *inside* a layer is Chapter 11 (the attention block, worked by hand) and Chapter 12
(the other block, what the running vector accumulates, and what nobody can tell you about
depth). For this chapter a layer is a box of the right shape, and that is enough to see the
pass end to end.

> **Tip:** When you read that a model "has 32 layers and a width of 4,096", you now know
> exactly what both numbers mean: a depth of thirty-two blocks in a row, each moving lists
> of 4,096-slot vectors. Depth, width and the vocabulary size describe most of the model's
> shape.

## What Comes Out Is a Distribution, Not a Word

The stack gives back one vector per position, same as it took. For the next token, only the
last position's vector matters — it is the one that has seen the whole input, and Chapter 11
shows how.

That vector has `\(d\)`{=latex} slots, and you need one number per vocabulary entry. So the
final step multiplies it by a matrix with one column per entry. Shape rule from Chapter 8:

```text
  (1 x 4,096) times (4,096 x 128,000)  gives  (1 x 128,000)
             ^              ^
             these must match
```

One raw score for every token in the vocabulary. Then softmax — the formula from Chapter 8 —
turns those scores into positive numbers that add to exactly 1. That is the **next-token
distribution**, and it is what one call to the model computes.

> **Note:** In many models the matrix that produces those scores is the embedding table used
> a second time and read the other way round — the same table that turned a token into a
> vector now turns a vector into a score for that token. Some models keep a separate matrix
> for it. Nothing in this chapter depends on which. Chapter 13 gives those raw scores their
> name and shows how one of them becomes a word.

## The Whole Thing, in Five Tokens and Four Dimensions

Now do it. A vocabulary of five entries and a width of four, so every number fits on the
page.

The vocabulary and its embedding table:

```text
  id  token   embedding
   0  the     (1, 0, 2, 0)
   1  cat     (0, 2, 1, 1)
   2  sat     (2, 1, 0, 1)
   3  mat     (0, 1, 3, 0)
   4  on      (1, 1, 1, 2)
```

**Stage 1.** The input is "the cat sat", which is ids `\((0, 1, 2)\)`{=latex}.

**Stage 2.** Look up those three rows. The result is a 3 × 4 matrix — one vector per
position:

```text
  position 1   the   (1, 0, 2, 0)
  position 2   cat   (0, 2, 1, 1)
  position 3   sat   (2, 1, 0, 1)
```

**Stage 3.** Those go through the stack. We are not opening the stack here, so take its
answer for the last position as given:

```text
  h = (0, 1, 1, 2)
```

**Stage 4.** One score per vocabulary entry. Taking the first case from the note above, that
is the dot product of `\(h\)`{=latex} with every row of the table. Slot by slot, all five:

```text
  token   row            row . (0, 1, 1, 2)          score
  the     (1, 0, 2, 0)   0 + 0 + 2 + 0                 2
  cat     (0, 2, 1, 1)   0 + 2 + 1 + 2                 5
  sat     (2, 1, 0, 1)   0 + 1 + 0 + 2                 3
  mat     (0, 1, 3, 0)   0 + 1 + 3 + 0                 4
  on      (1, 1, 1, 2)   0 + 1 + 1 + 4                 6
```

**Stage 5.** Softmax those five scores. Exponentiate each, add them up, divide:

```text
  e^2 = 7.389     e^5 = 148.413    e^3 = 20.086
  e^4 = 54.598    e^6 = 403.429

  total = 7.389 + 148.413 + 20.086 + 54.598 + 403.429
        = 633.915

  the     7.389 / 633.915 = 0.012
  cat   148.413 / 633.915 = 0.234
  sat    20.086 / 633.915 = 0.032
  mat    54.598 / 633.915 = 0.086
  on    403.429 / 633.915 = 0.636
                            -----
                            1.000
```

**That list of five numbers is the model's entire output for this call.** "on" at 0.636,
"cat" at 0.234, and three long shots. The model has not produced a word. It has produced a
ranking with weights, and it is now finished until somebody calls it again.

Notice what the arithmetic shows that prose cannot. The scores came from dot products
against the embedding rows, so **a token scores highly when its row agrees with
`\(h\)`{=latex} slot by slot** — the same "agreement" Chapter 8 built. And softmax
sharpened the gaps, exactly as it did there: scores spread over 2 to 6 came out as
probabilities spread over 0.012 to 0.636.

> **Note:** The numbers in that table are invented, and a real table's numbers would be
> fitted from training. The *arithmetic* is the real thing, at the real shape — change 5 to
> 128,000 and 4 to 4,096 and nothing about the procedure differs.

## Parameters: the Numbers That Were Fitted

A **parameter** is one of the numbers inside the model: training set it, and inference never
changes it. The embedding table is parameters. Every layer's numbers are parameters. The
final matrix is parameters.

The count is what a model's name usually reports. "A 7B model" means about seven billion
parameters. That one number tells you roughly what hardware it needs and roughly what it
costs to run, which is why it is the first thing anybody says about a model.

Our five-token toy has 20 parameters in its embedding table, and a real model of the shape
above has 524,288,000 in that table alone. Where the rest of them sit — how many are in each
layer and in which part of it — is Chapter 12, and what one parameter occupies in memory is
Chapter 15.

> **Note:** Vocabulary sizes around 100,000 to 200,000 entries, widths of a few thousand,
> and depths of a few dozen to a hundred describe the models of the moment. The figures will
> move. The three quantities — vocabulary, width, depth — and the fact that the embedding
> table is the first of them multiplied by the second will not.

Two things parameters are *not*, both of which get muddled:

- **Not your data.** Nothing you send on a call becomes a parameter. The numbers were fixed
  before you arrived, which is Chapter 1's point about training and inference, now with a
  name for the thing that stays fixed.
- **Not the settings.** Temperature and the rest are dials outside the model's own numbers:
  they act on the scores and on the picking, never on the parameters. Chapter 13 owns them.

## One Pass, One Token

One **forward pass** is the whole journey above: look up, through the stack once, one
distribution out. And it yields exactly one distribution — one guess about one position.

So how does a model write a paragraph? By being called again. Something picks a token from
the distribution, appends it to the input, and runs another forward pass over the longer
input. Then again. A reply of a hundred tokens is a hundred forward passes, each one working
on an input one token longer than the last. A model used this way is called
**autoregressive**: its own output becomes part of its next input.

```text
  pass 1   the cat sat             -->  on
  pass 2   the cat sat on          -->  the
  pass 3   the cat sat on the      -->  mat
```

Three things fall out of this, and all three are easy to get wrong.

**The loop is not in the model.** The model has no memory between passes and no notion that
it is in the middle of a sentence. Appending the token and calling again is done by the
program around it. This is the same observation as Chapter 1's "the memory is in the
product", one level further down.

**The reply arrives a piece at a time because it is produced a piece at a time.** The
streaming you see in products is not a visual effect; it is one token per pass, shown as
each pass finishes.

**Re-reading the whole input on every pass sounds ruinously wasteful, and it would be.** A
naive implementation would redo all the work for every earlier position on every pass. Real
systems do not, and the mechanism that saves them — along with the memory bill it brings —
is Chapter 15.

> **Tip:** This is the fact to reach for when somebody asks why long outputs cost more than
> long inputs. A long input is read once. A long output is one pass per token, over an input
> that keeps growing.

## Lab: Run a Forward Pass by Hand

No installation and nothing to set up beyond Python, which you have. Twenty-five minutes,
and there is a key for every step, so you can be wrong and find out.

A different five-token model. Its vocabulary and embedding table:

```text
  id  token   embedding
   0  i       (2, 0, 1, 0)
   1  like    (0, 2, 0, 1)
   2  cold    (1, 1, 1, 0)
   3  tea     (0, 2, 1, 2)
   4  .       (1, 0, 0, 1)
```

**Step 1.** The input is "i like cold". Write down the list of ids, then the matrix of rows
the lookup produces, and say its shape.

*Expected result:* ids `\((0, 1, 2)\)`{=latex}; rows `\((2,0,1,0)\)`{=latex},
`\((0,2,0,1)\)`{=latex}, `\((1,1,1,0)\)`{=latex}; shape 3 × 4 — three positions, width four.
If you wrote 4 × 3 you have the shape rule the wrong way round.

**Step 2.** The stack returns `\(h = (1, 2, 1, 1)\)`{=latex} for the last position. Compute
the five scores by hand, writing each dot product out slot by slot.

*Expected result:*

```text
  i      (2,0,1,0) . h = 2 + 0 + 1 + 0 = 3
  like   (0,2,0,1) . h = 0 + 4 + 0 + 1 = 5
  cold   (1,1,1,0) . h = 1 + 2 + 1 + 0 = 4
  tea    (0,2,1,2) . h = 0 + 4 + 1 + 2 = 7
  .      (1,0,0,1) . h = 1 + 0 + 0 + 1 = 2
```

**Step 3.** Without computing the softmax: which token is most likely, and which is least?
Why can you answer that from the scores alone?

*Expected result:* "tea" is most likely and "." is least. Softmax preserves order — Chapter
8's third property — so the ranking is already decided by the scores. Only the *sizes* of
the probabilities need the arithmetic.

**Step 4.** Say precisely what the model has *not* done at this point, and who does it.

*Expected result:* it has not chosen a token. It has produced five numbers. Choosing is done
outside the model, by the code that called it, under settings that Chapter 13 teaches. A
model that always produced its top-scoring token would be one particular choice among
several, not the only possibility.

**Step 5.** Now run it. In a new empty folder, save this as `forward.py`:

```python
import math

vocab = ["i", "like", "cold", "tea", "."]
table = [(2, 0, 1, 0),        # i
         (0, 2, 0, 1),        # like
         (1, 1, 1, 0),        # cold
         (0, 2, 1, 2),        # tea
         (1, 0, 0, 1)]        # .

ids = [0, 1, 2]                      # "i like cold"
rows = [table[i] for i in ids]       # the lookup
h = (1, 2, 1, 1)                     # what the stack returned

scores = [sum(a * b for a, b in zip(row, h)) for row in table]
total = sum(math.exp(s) for s in scores)
probs = [math.exp(s) / total for s in scores]

for word, s, p in zip(vocab, scores, probs):
    print(f"{word:>5}   score {s:>2}   p {p:.3f}")
```

*Expected result:* exactly this, and your five scores from step 2 in the middle column.

```text
      i   score  3   p 0.015
   like   score  5   p 0.112
   cold   score  4   p 0.041
    tea   score  7   p 0.826
      .   score  2   p 0.006
```

**Step 6.** Count the parameters in this toy's embedding table. Then count them for a model
with a vocabulary of 50,000 and a width of 2,048.

*Expected result:* 5 × 4 = 20 for the toy. 50,000 × 2,048 = 102,400,000 for the other — a
hundred million parameters in the lookup table alone, in a model far smaller than the ones
people call large.

**Step 7.** Change one number: set `h` to `(1, 0, 1, 1)`, so the second slot is zero. Run it
again. Which scores moved, which did not, and why?

*Expected result:*

```text
      i   score  3   p 0.348
   like   score  1   p 0.047
   cold   score  2   p 0.128
    tea   score  3   p 0.348
      .   score  2   p 0.128
```

"i" and "." did not move, because their rows have 0 in slot 2 and that slot now contributes
nothing either way. The other three fell, each by twice its own slot-2 value. And the
prediction is destroyed: "tea" has gone from 0.826 to a tie with "i" at 0.348. One slot out
of four, in one vector, did that. Be exact about what it shows: these numbers are invented and
four slots is not 4,096, so it says nothing about how far a real model moves when one slot
changes. What it shows is that nothing in this arithmetic protects any one score from any one
slot.

**Step 8.** The model must produce the reply "tea ." — two tokens. How many forward passes,
and what is the input to each?

*Expected result:* two passes. The first sees "i like cold" and yields a distribution from
which "tea" is taken; the second sees "i like cold tea" and yields one from which "." is
taken. Each pass reads everything before it. If you answered one, you have the central point
of the last section still to re-read.

## Summary, Key Terms, and Review Questions

### Summary

Text is cut into tokens and each token is replaced by its index into the model's
**vocabulary**, a numbered list fixed before training and unchanged while you use the model.
Each index is looked up in the **embedding table**, a matrix with one row per vocabulary
entry, giving one vector per position; the number of slots in those vectors is the model's
**width**, the same from one layer to the next all the way through. Those coordinates were
chosen by nobody — they are whatever made next-token prediction work, and no dimension means
anything. The vectors pass through a stack of **layers** — the count of them is the model's
**depth** — identical in shape and each holding its own numbers, with the same width in as
out, once, with no loop. The last position's vector is then multiplied by a matrix with one
column per vocabulary entry to give one score per entry, and softmax turns those scores into
the **next-token distribution** — one probability for every token the model can produce,
adding to 1. That distribution is the whole output of one **forward pass**, so a long reply
is many passes, each over a slightly longer input, which is what **autoregressive** means. A
**parameter** is one of the fitted numbers inside all of this, and the count is what a
model's name reports.

### Key Terms

| Term | Meaning |
|---|---|
| **Vocabulary** | The fixed, numbered list of every entry a model can read or produce — nearly all pieces of text, and a few that are not. Built once, before training, and fixed while you use the model |
| **Embedding table** | A matrix with one row per vocabulary entry. Looking a token up in it is how that token enters the model; the rows are called embeddings |
| **Width** | The number of slots in the vectors moving from layer to layer, the same all the way through. Written `\(d\)`{=latex} in formulas |
| **Layer** | A block of arithmetic taking one vector per position and returning one per position, same width in as out. Every layer has the same shape and its own numbers |
| **Depth** | The number of layers in the stack. The last of the three numbers — vocabulary, width, depth — that describe most of a model's shape |
| **Next-token distribution** | One probability for every entry in the vocabulary, adding to 1, saying how likely each is to come next. The entire output of one call |
| **Forward pass** | One journey through the model — lookup, the stack once, one distribution out. It produces exactly one distribution |
| **Autoregressive** | Producing output one token at a time, with each token appended to the input before the next pass |
| **Parameter** | One number inside the model, set by training and unchanged by inference. The count is what "a 7B model" reports |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Embedding table size | vocabulary × width numbers. 128,000 × 4,096 = 524,288,000 |
| The output step | One score per vocabulary entry, so the final shape is (1 × `\(d\)`{=latex}) times (`\(d\)`{=latex} × vocabulary) |
| What one forward pass yields | Exactly one next-token distribution |
| Passes for a reply | One per token produced, each over an input one token longer |
| The three top-level shape numbers | Vocabulary, width, depth. There are more inside a layer, which is Chapter 12's |

### Review Questions

1. What does one call to a model actually compute, and what has it not done?
2. Somebody tells you that dimension 412 of a model's embeddings encodes formality. What do you say?
3. A model has 32 layers. What is identical between layer 3 and layer 29, and what is not?
4. Why is a 500-token reply so much dearer than a 500-token prompt?
5. Your vocabulary has 200,000 entries and your width is 4,096. How many numbers are in the embedding table, and why might that matter for a small model?
6. What does "autoregressive" mean, and where does the loop live?

### Review Answers

1. It computes one next-token distribution: one probability for every entry in the
vocabulary, adding to 1, for the single position after everything you sent. It has not
chosen a token, produced a word, or decided anything about the rest of the reply. Choosing
is done by the code around the model, and a long reply is that whole computation repeated
once per token.
2. That the claim needs checking rather than repeating, and that the honest default is the
opposite: the coordinates are whatever made next-token prediction work, nobody chose them,
and no dimension means anything on its own. The rows are not random — they were fitted, and
useful things follow from how they sit relative to each other — but naming what one slot
does is a different and much stronger claim. Why the arrangement carries meaning at all is
outside what this book explains.
3. Their shape is identical: both take one vector per position and return one per position,
with the same width in as out. That is what lets them be stacked at all. Their numbers are
not identical — each layer holds its own parameters, fitted separately. "Identical layers"
means identical in structure, never in content.
4. The prompt is read in one pass. The reply is one pass per token, and each of those passes
works on an input that is one token longer than the last. So the reply is both more passes
and more work with each successive pass, which is also why providers charge more for output
than for input.
5. 200,000 × 4,096 = 819,200,000 numbers — over eight hundred million parameters before a
single layer. In a small model that can be a large share of the total, so the vocabulary size
is a real design decision rather than a detail, and it sets the size of the output step too.
6. It means the model's own output becomes part of its next input: pick a token from the
distribution, append it, run another forward pass, repeat. The loop lives in the program
around the model. The model itself has no memory between passes and no idea that it is
part-way through a sentence.

> **You understand this when** you can say what a single call computes without using the
> word "answer", and explain why writing a hundred tokens means running the model a hundred
> times.
