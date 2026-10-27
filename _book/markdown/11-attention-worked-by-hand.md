# Attention, Worked by Hand

This is the chapter the rest of the book has been pointing at. Chapter 9 called a layer a box
of the right shape and promised to open it; this opens the half of it that everybody asks
about in interviews. Everything here is arithmetic at the level of Chapter 8 — dot products,
softmax, and multiplying vectors by numbers and adding them up — assembled in one particular
order. By the end you will have worked
the whole formula on a five-word sentence with four-dimensional vectors, and you will be able
to say what every symbol in it stands for.

*The problem.* Every explanation says the model "pays attention to the relevant words". I want
to know what is actually computed.

*The question.* What arithmetic turns a list of vectors into a list of vectors in which each
position has drawn on the others, and where exactly does "relevant" enter?

## What Each Position Needs

Start with the difficulty rather than the solution.

Chapter 9 left you with one vector per position, each one standing for a single token and
nothing else. The vector at position 5 knows what token sits at position 5. It knows nothing
about positions 1 to 4.

That is useless on its own. Consider the five tokens

```text
  the   cat   sat   on   it
   1     2     3     4    5
```

To do anything sensible with position 5, the model has to bring in something from the other
positions. And the difficulty is that **which other positions matter depends on the content**,
not on anything fixed. Sometimes the useful information is one token back, sometimes forty.
A fixed rule — always look at the previous three — cannot be right in general, because the
useful distance changes with the sentence.

So the thing we need is a procedure that, for each position, works out *for itself* how much
of each other position to take, and then takes that much. **Attention** is that procedure, and
it is built from three ideas you already have.

- Each position produces a request saying what it is looking for.
- Each position produces a label saying what it offers.
- Scoring every request against every label says who should take how much from whom.

Request, label and content are the three views, and the next section gives them their names.

## Three Views of the Same Vector: Query, Key, Value

Every position's vector is turned into three different vectors, by multiplying it by three
different matrices. The matrices are parameters — fitted in training, fixed while you use the
model, exactly as Chapter 9 said.

| View | Written | Read it as |
|---|---|---|
| **Query** | `\(q\)`{=latex} | What this position is looking for |
| **Key** | `\(k\)`{=latex} | What this position offers to others looking |
| **Value** | `\(v\)`{=latex} | What this position actually hands over if chosen |

The three matrices are written `\(W_Q\)`{=latex}, `\(W_K\)`{=latex} and `\(W_V\)`{=latex}, and
the arithmetic is Chapter 8's matrix-times-vector: each output slot is a dot product of one
row of the matrix with the input vector.

Here is the whole example, and everything in this chapter is computed from it. Five tokens,
width four:

```text
  pos  token   x
   1   the     (1, 2, 2, 0)
   2   cat     (0, 2, 1, 2)
   3   sat     (1, 2, 0, 0)
   4   on      (0, 1, 1, 1)
   5   it      (2, 0, 2, 0)
```

The three matrices, kept to zeroes and ones so the arithmetic stays visible:

```text
  W_Q = [ 1 0 0 0 ]    W_K = [ 0 0 0 1 ]    W_V = [ 1 0 0 0 ]
        [ 0 1 1 0 ]          [ 0 1 0 0 ]          [ 0 1 0 1 ]
        [ 0 1 0 0 ]          [ 1 0 0 0 ]          [ 0 1 0 0 ]
        [ 0 0 0 1 ]          [ 0 1 1 0 ]          [ 0 0 1 0 ]
```

Work one out by hand before trusting the table. Position 5 is `\(x = (2, 0, 2, 0)\)`{=latex},
and its query is `\(W_Q x\)`{=latex} — row by row:

```text
  row 1   (1,0,0,0) . (2,0,2,0) = 2
  row 2   (0,1,1,0) . (2,0,2,0) = 0 + 2 = 2
  row 3   (0,1,0,0) . (2,0,2,0) = 0
  row 4   (0,0,0,1) . (2,0,2,0) = 0

  q(it) = (2, 2, 0, 0)
```

All fifteen vectors, the same way:

```text
  pos  token   q              k              v
   1   the     (1, 4, 2, 0)   (0, 2, 1, 4)   (1, 2, 2, 2)
   2   cat     (0, 3, 2, 2)   (2, 2, 0, 3)   (0, 4, 2, 1)
   3   sat     (1, 2, 2, 0)   (0, 2, 1, 2)   (1, 2, 2, 0)
   4   on      (0, 2, 1, 1)   (1, 1, 0, 2)   (0, 2, 1, 1)
   5   it      (2, 2, 0, 0)   (0, 0, 2, 2)   (2, 0, 0, 2)
```

> **Note:** The three matrices above were chosen by hand so that the arithmetic comes out
> legible and the result is worth looking at. In a real model they are fitted, nobody can say
> in advance where the weight will land, and a matrix that merely selects and adds slots the
> way these do would be unusually simple. What is real here is the procedure, not the numbers.

**Why three views and not one?** Because what a position is looking for and what it offers are
different questions. "it" is looking for a thing it might refer to; what "it" offers to other
positions is something else entirely. With one vector doing both jobs, the two uses would pull
it in different directions. And the value is separate again, because *how much to take* and *what to
take* are different decisions — which is the hinge the rest of the chapter turns on.

## The Scores: Every Query Against Every Key

Now the comparison. The score of position `\(i\)`{=latex} attending to position
`\(j\)`{=latex} is the dot product of `\(i\)`{=latex}'s query with `\(j\)`{=latex}'s key.

Chapter 8 built the dot product as agreement: large when both vectors are large in the same
slots. That is exactly what is wanted here. A query and a key that agree slot by slot produce
a high score, which is this procedure's entire definition of "relevant".

Work one by hand. Position 5's query against position 2's key:

```text
  q(it) . k(cat) = (2,2,0,0) . (2,2,0,3)
                 = 2x2 + 2x2 + 0x0 + 0x3
                 = 4 + 4 + 0 + 0
                 = 8
```

Doing that for all 25 pairs gives a grid — queries down the side, keys along the top:

```text
            k:the  k:cat  k:sat  k:on  k:it
  q:the       10     10     10      5     4
  q:cat       16     12     12      7     8
  q:sat        6      6      6      3     4
  q:on         9      7      7      4     4
  q:it         4      8      4      4     0
```

In matrix terms this grid is `\(QK^{\top}\)`{=latex} — the matrix of queries times the matrix of
keys with its rows and columns swapped, which is what the small `\(\top\)`{=latex} means, so
that every row meets every column. Chapter 8's shape rule says
why it comes out square:

```text
  (5 x 4) times (4 x 5)  gives  (5 x 5)
        ^         ^
        these must match
```

**That grid being square in the number of tokens is what decides the cost of a long input**, and the last section of this chapter is about what it costs.

> **Tip:** Read the grid one row at a time. A row is one position asking "how much do I want
> from each of you?" — and it is rows, not columns, that get turned into weights. The columns
> have no meaning of their own.

## Why Divide by the Square Root

Before the scores become weights, every one of them is divided by `\(\sqrt{d_k}\)`{=latex},
the square root of the key's width — the number of slots in it, not its length in Chapter 8's
sense. Here the keys have four slots, so the divisor is `\(\sqrt{4} = 2\)`{=latex}:

```text
            k:the  k:cat  k:sat  k:on  k:it
  q:it         2      4      2      2     0
```

This looks like fussiness and it is not. Here is the same row turned into weights both ways —
first without the division, then with it. Softmax is Chapter 8's: exponentiate each, divide by
the total.

```text
  WITHOUT the division, scores (4, 8, 4, 4, 0)

    e^4 = 54.598   e^8 = 2980.958   e^0 = 1.000
    total = 54.598+2980.958+54.598+54.598+1.000 = 3145.752

    weights   0.017   0.948   0.017   0.017   0.000
```

```text
  WITH the division, scores (2, 4, 2, 2, 0)

    e^2 = 7.389    e^4 = 54.598     e^0 = 1.000
    total = 7.389 + 54.598 + 7.389 + 7.389 + 1.000 = 77.765

    weights   0.095   0.702   0.095   0.095   0.013
```

Undivided, position 2 takes 95 per cent and everything else is noise: attention has stopped
blending and started picking. Divided, position 2 still wins clearly at 0.70 while the others
keep a real share.

**And the reason this matters more as models get bigger is the dot product itself.** A dot
product is a sum of `\(d_k\)`{=latex} terms, so as the vectors get wider the sum has more terms
in it. It does not grow in proportion to `\(d_k\)`{=latex}, though, because the slot-by-slot
products do not all pull the same way — some are positive, some negative, and they partly
cancel. A sum of many terms that partly cancel typically ends up about
`\(\sqrt{d_k}\)`{=latex} times the size of one of them, which is why the divisor is the square
root and not the width itself. **That is the answer to "why the square root" rather than just
"why divide".** Chapter 8's softmax property — *gaps get exaggerated* — then does
the rest: wider vectors give larger scores, larger scores give larger gaps after
exponentiating, and the weights collapse onto a single position. Dividing by
`\(\sqrt{d_k}\)`{=latex} pulls the scores back to roughly the same size whatever the width, so
the same design works at 64 slots and at 4,096.

> **Note:** The weights in the undivided block add to 0.999 rather than 1 as printed, because
> the fifth is 0.0003 and rounds to 0.000. The arithmetic is exact; the printing is to three
> places. This is Chapter 8's rounding point, and it is worth noticing here rather than being
> puzzled by it later.

## Masking: No Looking Ahead

One more thing happens before softmax, and it is there because of how these models are used.

Chapter 9 showed the model producing one token at a time, each pass over an input one token
longer. Position 3's output must not depend on anything after it, because the same arithmetic
has to give the same answer when positions 4 and 5 genuinely do not exist yet — which is the
situation every time the model produces a token. A position that used what follows it would
behave one way on a finished sentence and another way while the sentence was being written.

The **causal mask** enforces that. Before softmax, every score where the key's position is
later than the query's is set to minus infinity. Exponentiating minus infinity gives zero, so
those positions get exactly zero weight and the rest share the whole of it.

```text
            k:the  k:cat  k:sat  k:on  k:it
  q:the        5      .      .      .     .
  q:cat        8      6      .      .     .
  q:sat        3      3      3      .     .
  q:on       4.5    3.5    3.5      2     .
  q:it         2      4      2      2     0
```

The dots are the masked entries. Note that the bottom row — the one this chapter works in
full — is unaffected, because position 5 is last and has nothing ahead of it.

> **Note:** This triangle is what "decoder" means in practice. A model that is allowed to see
> the whole input at once, in both directions, is a different design used for different jobs.
> Everything in this book is the triangle.

## Softmax, and the Weighted Blend

Take the last row, masked and scaled: `\((2, 4, 2, 2, 0)\)`{=latex}. Softmax turns it into
**attention weights** — one per position, all positive, adding to 1.

```text
  step 1   exponentiate
           e^2 = 7.389   e^4 = 54.598   e^2 = 7.389
           e^2 = 7.389   e^0 = 1.000

  step 2   add them
           7.389 + 54.598 + 7.389 + 7.389 + 1.000 = 77.765

  step 3   divide each by the total
           the   7.389 / 77.765 = 0.095
           cat  54.598 / 77.765 = 0.702
           sat   7.389 / 77.765 = 0.095
           on    7.389 / 77.765 = 0.095
           it    1.000 / 77.765 = 0.013
                                  -----
                                  1.000
```

Position 5 has decided to take about seven tenths of its information from position 2. Nothing
told it to. It fell out of a dot product between two vectors that `\(W_Q\)`{=latex} and
`\(W_K\)`{=latex} arranged — here by hand, in a real model by training.

**Now spend the weights.** The output for position 5 is the weighted sum of the *value*
vectors — each value multiplied by its weight, all added up:

```text
  the   0.095 x (1, 2, 2, 2)  =  (0.095, 0.190, 0.190, 0.190)
  cat   0.702 x (0, 4, 2, 1)  =  (0.000, 2.808, 1.404, 0.702)
  sat   0.095 x (1, 2, 2, 0)  =  (0.095, 0.190, 0.190, 0.000)
  on    0.095 x (0, 2, 1, 1)  =  (0.000, 0.190, 0.095, 0.095)
  it    0.013 x (2, 0, 0, 2)  =  (0.026, 0.000, 0.000, 0.026)
                                 ---------------------------
                                 (0.216, 3.378, 1.879, 1.013)
```

Add each column and check it yourself — that is the point of the layout. The result,
`\((0.216,\ 3.378,\ 1.879,\ 1.013)\)`{=latex}, is one vector of width four, the same shape as
the vector that went in, which is what makes a stack of these possible at all.

And look at what it is made of: mostly `\(v\)`{=latex} for "cat", with a little of everything
else. **Position 5 went in standing for "it" and comes out standing largely for "cat".** That
is the whole trick, and there is no step in it that is not arithmetic.

> **Warning:** It is tempting to say the model "resolved the pronoun". It did not. It computed
> a weighted average in which one term happened to dominate, because of matrices chosen — here
> by me, in a real model by training — to make that happen. Attention weights are often
> described as showing what a model "looked at", and they are evidence about one step of
> arithmetic rather than an account of why an answer came out as it did. Chapter 16 is where
> the general version of that caution lives.

## The Formula, All at Once

Everything above, in one line:

```{=latex}
\[ \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V \]
```

Read it with Chapter 8's four steps, innermost bracket outward.

| Piece | What it is | Which section |
|---|---|---|
| `\(Q, K, V\)`{=latex} | The queries, keys and values, one row per position | Three views |
| `\(QK^{\top}\)`{=latex} | Every query dotted with every key: the square grid | The scores |
| `\(\sqrt{d_k}\)`{=latex} | The square root of the key width, here `\(\sqrt{4} = 2\)`{=latex} | Why divide |
| `\(\mathrm{softmax}\)`{=latex} | Each row turned into positive weights adding to 1 | Softmax |
| `\(\cdots V\)`{=latex} | The weights spent on the value vectors | The blend |

The mask is not in the formula. It is applied to the grid before softmax, and it is left out of
the written form by convention rather than because it is optional.

**That is the entire mechanism**, and it is worth noticing how little of it there is: one matrix
multiplication for each of the three views, a fourth to build the grid, a division, a softmax,
and a fifth to spend the weights. Nothing in it is harder than Chapter 8.

## Attention Alone Cannot Tell the Order

Chapter 9 said position has to be supplied separately, and promised the reason here. This is
it — and it is checkable with the numbers already on the page.

Swap two tokens in the input — "cat" and "sat", positions 2 and 3 — and recompute position 5's
row. Nothing else changes.

```text
  original    the  cat  sat  on  it
    scores     4    8    4   4   0
    weights   0.095 0.702 0.095 0.095 0.013
    output   (0.216, 3.378, 1.879, 1.013)

  swapped     the  sat  cat  on  it
    scores     4    4    8   4   0
    weights   0.095 0.095 0.702 0.095 0.013
    output   (0.216, 3.378, 1.879, 1.013)
```

The weight of 0.702 followed "cat" to its new seat, exactly as it should. **And the output is
identical.** Of course it is: the output is a sum, and addition does not care what order you
add in.

So "the cat sat on it" and "the sat cat on it" produce the same vector at position 5. Attention
cannot tell them apart, and nothing in this formula puts the order back. The order of your
words carries no information in it at all.

**That is why position has to be supplied separately.** Something must put "I am the second
token" into the arithmetic, because the shape of the computation never will. There are two
families in use. One adds a position-dependent vector to each token's embedding before the
stack begins, so the vector for "cat" at position 2 differs from the vector for "cat" at
position 7. The other rotates each query and key by an amount that depends on its position, so
that the dot product between them depends on how far apart they are. Both are called
**positional encoding**, and between them they account for nearly everything in current models.
(A third approach adds a position-dependent amount to the scores themselves, just before
softmax.) All of them exist for this one reason.

**And it takes two dot products to see it work.** Take the first family and add to each token's
vector a tiny marker of where it sits — `\((0,0,0,0)\)`{=latex} at position 1,
`\((0,0,0,1)\)`{=latex} at position 2, `\((0,0,0,2)\)`{=latex} at position 3, and so on. Now
"cat" is no longer one vector. At position 2 it is `\((0,2,1,2)+(0,0,0,1) = (0,2,1,3)\)`{=latex}
and at position 3 it is `\((0,2,1,2)+(0,0,0,2) = (0,2,1,4)\)`{=latex}. Push both through
`\(W_K\)`{=latex}, and push "it" at position 5 through `\(W_Q\)`{=latex}:

```text
  cat at position 2   k = (3, 2, 0, 3)
  cat at position 3   k = (4, 2, 0, 3)
  it  at position 5   q = (2, 2, 0, 4)
```

```text
  cat at 2   2x3 + 2x2 + 0x0 + 4x3 = 6 + 4 + 0 + 12 = 22
  cat at 3   2x4 + 2x2 + 0x0 + 4x3 = 8 + 4 + 0 + 12 = 24
```

Without the markers both of those scores were 8, which is why the swap changed nothing. With
them the same word scores 22 in one seat and 24 in another, the two rows of weights no longer
match, and the sum they feed comes out different. **Position is now in the arithmetic**, and it
got there before the dot product rather than inside it.

> **Note:** Those markers are made up and deliberately crude — a real scheme has to keep
> working at position 4,000 as well as position 2, and must not swamp the token's own meaning
> with a number that grows without limit. What is real here is the shape of the fix: something
> position-dependent enters the vectors, and the scores stop being blind.

> **Tip:** This is the answer to "why do models need positional encodings at all", and the
> demonstration above is the answer to give. It takes thirty seconds: swap two words, get the
> same answer, therefore the formula is blind to order. **Swap two words that are not the last
> one.** The final position supplies the query, so changing the token there changes what is
> being asked and the output moves for a reason that has nothing to do with order — which
> would lose you the argument rather than win it.

## Several Heads

One more structural piece, and it is simpler than it sounds.

Everything above is one **attention head**: one set of `\(W_Q\)`{=latex}, `\(W_K\)`{=latex},
`\(W_V\)`{=latex}, one grid, one set of weights. A real layer runs several heads at once, and
they divide the width between them rather than each taking all of it. With a width of 4 and two
heads, each head works in two dimensions, so `\(d_k = 2\)`{=latex} and the divisor becomes
`\(\sqrt{2}\)`{=latex}, which is 1.414 to three places. The scaled column below divides by the
square root itself rather than by the rounded figure, so your own arithmetic may differ in the
last digit.

Here are two heads over the same five tokens. They differ only in `\(W_K\)`{=latex}, so you can
see the effect of one change. Head 1's keys are
`\((x_4,\ x_2 + x_4)\)`{=latex}; head 2's are `\((x_4,\ x_1)\)`{=latex}. Both queries are
`\((x_4,\ x_3)\)`{=latex}, so `\(q\)`{=latex} for position 5 is `\((0, 2)\)`{=latex} in both.

```text
  HEAD 1       k       q.k    scaled    weight
    the      (0, 2)     4      2.828     0.050
    cat      (2, 4)     8      5.657     0.847
    sat      (0, 2)     4      2.828     0.050
    on       (1, 2)     4      2.828     0.050
    it       (0, 0)     0      0.000     0.003

  HEAD 2       k       q.k    scaled    weight
    the      (0, 1)     2      1.414     0.152
    cat      (2, 0)     0      0.000     0.037
    sat      (0, 1)     2      1.414     0.152
    on       (1, 0)     0      0.000     0.037
    it       (0, 2)     4      2.828     0.623
```

**The two heads attend to different places.** Head 1 puts 0.847 of its weight on "cat";
head 2 puts most of its on position 5 itself. Neither is right or wrong — they are two
different questions being asked of the same five tokens, and that is what the extra heads buy.
One head has one set of weights and therefore one opinion about what is relevant; a layer with
sixteen heads has sixteen, computed independently and in parallel.

Each head produces its own output vector, of its own narrower width, by spending its weights on
its own values. Give head 1 the value projection `\((x_1,\ x_2)\)`{=latex} and head 2
`\((x_3,\ x_4)\)`{=latex}, and the blends are:

```text
  HEAD 1    weight    v       contribution
    the      0.050  (1, 2)   (0.050, 0.100)
    cat      0.847  (0, 2)   (0.000, 1.694)
    sat      0.050  (1, 2)   (0.050, 0.100)
    on       0.050  (0, 1)   (0.000, 0.050)
    it       0.003  (2, 0)   (0.006, 0.000)
                             ----------------
                             (0.106, 1.944)

  HEAD 2    weight    v       contribution
    the      0.152  (2, 0)   (0.304, 0.000)
    cat      0.037  (1, 2)   (0.037, 0.074)
    sat      0.152  (0, 0)   (0.000, 0.000)
    on       0.037  (1, 1)   (0.037, 0.037)
    it       0.623  (2, 0)   (1.246, 0.000)
                             ----------------
                             (1.624, 0.111)
```

Two vectors of two slots. Lay them end to end and you have one of four again:

```text
  concatenated   (0.106, 1.944, 1.624, 0.111)
```

and that is multiplied by one further matrix, `\(W_O\)`{=latex}, which mixes the heads back
together. Take

```text
  W_O = [ 1 0 0 1 ]      row 1   0.106 + 0.111 = 0.217
        [ 0 1 1 0 ]      row 2   1.944 + 1.624 = 3.568
        [ 1 1 0 0 ]      row 3   0.106 + 1.944 = 2.050
        [ 0 0 1 1 ]      row 4   1.624 + 0.111 = 1.735

  output   (0.217, 3.568, 2.050, 1.735)
```

One vector of width four, the same shape that went in. **That last matrix is why the heads do
not simply sit in separate lanes**: every row of `\(W_O\)`{=latex} above draws on both of them,
so what leaves the layer is a mixture rather than two answers stapled together.

**Nobody tells a head what to specialise in.** There is no instruction anywhere saying that
head 7 handles pronouns and head 12 handles punctuation. Every head has the same shape and
runs the same procedure; the only thing distinguishing them is that they hold different
numbers, and those numbers are whatever training left behind. People do go looking afterwards,
and sometimes find a head whose weights land somewhere describable across many inputs — but
that is a finding about a particular model, arrived at by measurement, not a design anybody
specified. This is the same honesty Chapter 9 required about the dimensions of an embedding,
and for the same reason.

> **Note:** Head 2's weights add to 1.001 as printed, for the rounding reason given earlier. And
> the two heads here share `\(W_Q\)`{=latex} so that one variable changes at a time; real heads
> differ in all three matrices.

## What It Costs: Big-O at Last

Chapter 8 gave you big-O and promised `\(O(n^2 d)\)`{=latex} would turn up here. This is where.

**First, why every pair at all?** It is a fair question: most of those 25 scores in the
example are small, and in a 10,000-token input the overwhelming majority of the grid will be
near zero. Could the model not compare only the pairs that matter?

It could not, because of the first section of this chapter. Which positions matter depends on
the content, and the content is what the scores are being computed to find out. There is
nothing to prune on until after you have the number you were trying to avoid computing. That
is the circularity at the heart of the cost: the comparison is exhaustive precisely because
the design refuses to decide in advance which comparisons are worth making.

There are designs that compare fewer pairs anyway — by restricting each position to a window,
or to a pattern of positions, or by approximating the grid. The first two buy their speed by
reinstating exactly the kind of fixed rule this chapter opened by rejecting. All of them are a
specialist topic rather than what you will meet in the models this book is about.

Count the work for a single head first. Its grid has `\(n^2\)`{=latex} entries, one for every
pair of positions, and each entry is a dot product of two vectors of width
`\(d_k\)`{=latex} — that many multiplications and that many additions. With one head taking
the whole width, `\(d_k = d\)`{=latex} and the grid costs about `\(n^2 d\)`{=latex}. With
`\(h\)`{=latex} heads it is the same total, because each of the `\(h\)`{=latex} grids is only
`\(d/h\)`{=latex} wide and `\(h \times n^2 \times d/h = n^2 d\)`{=latex}. Either way:

```{=latex}
\[ \text{scores} \;=\; n \times n \times d \;=\; O(n^2 d) \]
```

Put real numbers in it, at a width of 4,096:

```text
   tokens       pairs          multiply-adds
    1,000     1,000,000        4,096,000,000
    2,000     4,000,000       16,384,000,000
   10,000   100,000,000      409,600,000,000
```

**Double the input and the work goes up four times.** That is the practical content of the
`\(n^2\)`{=latex}, and three things follow from it that you will meet all through this book.

**Long inputs are superlinearly expensive.** Chapter 1 told you cost grows with the text you
move. This is the part that grows faster than the text: the dot products in the grid, and the
grid itself, which at 10,000 tokens is a hundred million numbers *per head, per layer*.

**It is a large part of why there is a limit on how much you may send at all.** There is a
length past which this stops being affordable, and where exactly that length sits is an engineering decision
somebody made about memory and money rather than a preference. Chapter 16 names that limit and
is about what else happens near it.

**And it is why re-reading the whole input on every token would be ruinous.** Chapter 9 flagged
that a hundred-token reply means a hundred passes over a growing input. Now you can see the
size of the problem: doing this grid again from scratch on every pass, when all but the last
row and column are unchanged, is the obvious waste. Chapter 15 is where it gets fixed, and what
the fix costs in memory.

> **Note:** `\(O(n^2 d)\)`{=latex} is the attention step. It is not the cost of a whole layer,
> which has other arithmetic in it that grows differently — Chapter 12 is where the rest of the
> layer lives. At short inputs the other part dominates; the squared term wins eventually,
> which is exactly what big-O is for.

## Lab: Two More Rows

Pen, paper and a calculator. Thirty minutes, and there is a key for every step. Everything you
need is the table from "Three views" — queries, keys and values for all five positions — and
the score grid. No code, and nothing to install.

**Step 1.** Compute `\(q(\text{sat}) \cdot k(\text{the})\)`{=latex} by hand, slot by slot, and
check it against the grid.

*Expected result:* `\(q(\text{sat}) = (1,2,2,0)\)`{=latex} and
`\(k(\text{the}) = (0,2,1,4)\)`{=latex}, so the terms are
`\(0 + 4 + 2 + 0 = 6\)`{=latex}. The grid's row 3, column 1 says 6.

**Step 2.** Write out row 3 of the grid, apply the causal mask, and divide by
`\(\sqrt{d_k}\)`{=latex}. Which entries survive, and what are they?

*Expected result:* row 3 is `\((6, 6, 6, 3, 4)\)`{=latex}. Position 3 may see positions 1, 2
and 3 only, so the last two are masked away. Dividing the survivors by 2 gives
`\((3, 3, 3)\)`{=latex}. If you divided before masking you got the same three numbers, which is
fine — the order of those two steps does not matter.

**Step 3.** Apply softmax to those three scores. What do you get, and what does it tell you
about what attention is allowed to do?

*Expected result:* `\(e^3 = 20.086\)`{=latex} three times, total 60.258, and each weight is
`\(20.086 / 60.258 = 0.333\)`{=latex}. **A perfectly even blend.** Three equal scores give three
equal weights, which is worth meeting: nothing in this procedure forces it to pick a winner. It
takes an even third from each when the scores say so. (The three thirds print as 0.999; the
exact value is one third each.)

**Step 4.** Compute position 3's output vector: the weighted sum of the value vectors for
positions 1, 2 and 3.

*Expected result:*

```text
  the   0.333 x (1, 2, 2, 2)  =  (0.333, 0.666, 0.666, 0.666)
  cat   0.333 x (0, 4, 2, 1)  =  (0.000, 1.332, 0.666, 0.333)
  sat   0.333 x (1, 2, 2, 0)  =  (0.333, 0.666, 0.666, 0.000)
                                 ---------------------------
                                 (0.666, 2.664, 1.998, 0.999)
```

**Step 5.** Now row 2, which is the interesting case for the mask. Write it out, mask it,
scale it, and turn it into weights.

*Expected result:* row 2 is `\((16, 12, 12, 7, 8)\)`{=latex}, and position 2 may see only
positions 1 and 2, so three of the five go. Scaled, the survivors are `\((8, 6)\)`{=latex}.
Then `\(e^8 = 2980.958\)`{=latex} and `\(e^6 = 403.429\)`{=latex}, total 3384.387, giving
weights `\((0.881,\ 0.119)\)`{=latex}.

**Step 6.** Compare step 5's weights with step 3's. Both came from the same procedure. Why is
one almost a decision and the other an even split?

*Expected result:* the gap between the scores, not their size. In step 3 all three scores were
equal, so the exponentials were equal. In step 5 the two scores differ by 2, and softmax
exaggerates gaps — `\(e^8\)`{=latex} is about 7.4 times `\(e^6\)`{=latex}, so one position takes
nearly nine tenths. This is the same property that made the division by
`\(\sqrt{d_k}\)`{=latex} necessary, seen from the other side.

**Step 7.** Without recomputing anything: a sixth token is appended, so `\(n\)`{=latex} goes
from 5 to 6. How many new entries appear in the grid, and how many of the old ones change?

*Expected result:* the grid goes from 5 × 5 to 6 × 6, so from 25 entries to 36 — **eleven new
ones**, which is one new row of 6 and one new column of 5. None of the old 25 changes, because
each depends only on its own pair of positions. That observation is the whole idea behind
Chapter 15's fix, and you have just derived the reason it is possible.

**Step 8.** A model has a width of 4,096 and allows 8,000 tokens of input. How many entries are
in one attention grid, and how many multiply-adds does building it take?

*Expected result:* `\(8{,}000^2 = 64{,}000{,}000\)`{=latex} entries, and
`\(64{,}000{,}000 \times 4{,}096 = 262{,}144{,}000{,}000\)`{=latex} multiply-adds — about 262
billion — and that is one layer's attention scores, all of its heads together, for one forward
pass. The heads divide the width between them, so adding heads does not multiply this. Multiply
by the layers to feel why long inputs are priced the way they are.

**Step 9.** Someone shows you a diagram of attention weights and says it proves the model
"understood" that "it" refers to "cat". What two things do you say?

*Expected result:* first, that the weights are a real measurement of one step of arithmetic —
they are not made up, and position 5 genuinely did take 0.702 of its value from position 2.
Second, that this is one head in one layer out of dozens of each, that the blend is then
combined with every other head's by `\(W_O\)`{=latex} and passed through the rest of the stack,
and that a weight is not a reason. The honest sentence is "this head put most of its weight
there", and anything stronger is a claim nobody has the evidence for.

## Summary, Key Terms, and Review Questions

### Summary

**Attention** gives every position a way to take information from the others, in amounts it
works out for itself. Each position's vector is turned into three — a **query** (what it is
looking for), a **key** (what it offers) and a **value** (what it hands over) — by three fitted
matrices. Every query is dotted with every key, giving a square grid of scores,
`\(QK^{\top}\)`{=latex}; the dot product is the procedure's whole definition of relevance. The
scores are divided by `\(\sqrt{d_k}\)`{=latex} because a dot product grows with width and
softmax exaggerates gaps, so without it the weights collapse onto one position — and the
divisor is the *square root* of the width rather than the width itself because the slot-by-slot
products partly cancel, so the total grows like `\(\sqrt{d_k}\)`{=latex} and not like
`\(d_k\)`{=latex}. A **causal
mask** sets every score for a later position to minus infinity, which softmax turns into
exactly zero weight. Softmax then turns each row into **attention weights** that are positive
and add to 1, and the output for that position is the weighted sum of the value vectors — the
same width in as out, which is what lets layers stack. The whole of it is
`\(\mathrm{softmax}(QK^{\top}/\sqrt{d_k})V\)`{=latex}. Because the output is a sum, **that
formula is blind to word order**, which is why **positional encoding** exists at all. A layer runs
several **attention heads** in parallel over slices of the width, each with its own matrices and
its own opinion, and a final matrix mixes their outputs. Building the grid costs
`\(O(n^2 d)\)`{=latex}: double the input and the work goes up four times.

### Key Terms

| Term | Meaning |
|---|---|
| **Attention** | The step in which each position takes a weighted blend of information from the others, in amounts computed from the content rather than fixed in advance |
| **Query** | The vector saying what a position is looking for, made by multiplying its vector by `\(W_Q\)`{=latex} |
| **Key** | The vector saying what a position offers to others, made with `\(W_K\)`{=latex}. Scored against every query |
| **Value** | The vector a position hands over when it is attended to, made with `\(W_V\)`{=latex}. What the weights are spent on |
| **Attention weights** | One row of the grid after scaling, masking and softmax: positive numbers adding to 1, saying how much of each position to take |
| **Causal mask** | Setting every score for a later position to minus infinity before softmax, so it gets exactly zero weight. It makes a position's output depend only on what precedes it, so the arithmetic is the same whether or not the rest of the sentence exists |
| **Attention head** | One complete set of query, key and value matrices and the weights they produce. A layer runs several in parallel over slices of the width, and a final matrix mixes their outputs |
| **Positional encoding** | How a token's position is put into the arithmetic, since the attention formula carries no notion of order. Added to the embedding before the stack, or applied as a rotation to queries and keys, or added to the scores themselves |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The attention formula | `\(\mathrm{softmax}(QK^{\top}/\sqrt{d_k})\,V\)`{=latex} |
| What the three views are for | Query = what I want, key = what I offer, value = what I give |
| Why divide by `\(\sqrt{d_k}\)`{=latex} | A dot product grows with width; without it softmax saturates and attention stops blending. The *square root*, because the slot products partly cancel, so the sum grows like `\(\sqrt{d_k}\)`{=latex} |
| The score grid | `\(n \times n\)`{=latex}, one entry per pair of positions |
| Attention cost | `\(O(n^2 d)\)`{=latex} — double the tokens, four times the work |
| What a row of weights is | Positive, adds to exactly 1, one number per visible position |
| Why positional encoding exists | Attention's output is a sum, so it is blind to the order of its inputs |

### Review Questions

1. Walk through attention on a short sentence, naming every step in order.
2. Why is the score divided by the square root of the key width? What goes wrong without it?
3. Why does attention cost grow with the square of the input length, and name two things that follow in practice.
4. What do several heads give you that one does not?
5. Your colleague says the attention weights prove the model linked "it" to "cat". How do you answer?
6. Why can attention not tell "the cat sat on it" from "the sat cat on it"? Why would swapping the *last* word not make the same point?

### Review Answers

1. Each position's vector is multiplied by three matrices to give a query, a key and a value.
Every query is dotted with every key, giving a square grid of scores — one per pair of
positions. Every score is divided by the square root of the key width. Scores for positions
later than the query are set to minus infinity, so they will vanish. Softmax turns each row
into positive weights adding to 1. The output for a position is the weighted sum of the value
vectors, which has the same width as the vector that went in. That is the whole of it, and it
is one line: `\(\mathrm{softmax}(QK^{\top}/\sqrt{d_k})V\)`{=latex}.
2. Because a dot product is a sum over the width, so it grows as the vectors get wider, and
softmax exaggerates gaps between large numbers. It is the *square root* of the width because
the slot-by-slot products do not all pull the same way — they partly cancel, so a sum of
`\(d_k\)`{=latex} of them ends up about `\(\sqrt{d_k}\)`{=latex} times the size of one, not
`\(d_k\)`{=latex} times. Without the division the biggest score runs
away with nearly all the weight — in this chapter's example, 0.948 instead of 0.702 — and
attention stops being a blend and becomes a hard pick. Dividing by `\(\sqrt{d_k}\)`{=latex}
keeps the scores roughly the same size whatever the width, so one design works at 64 slots and
at 4,096.
3. Because every position is compared with every other, so there are `\(n^2\)`{=latex} pairs per
head, each costing a dot product of the head's width — and since the heads divide the width
between them, the whole layer comes to about `\(n^2 d\)`{=latex} whatever the number of heads. Double the input and the work goes up four
times. Two consequences: long inputs cost more than proportionally, which is why a context
limit is a number somebody chose rather than a preference; and recomputing the whole grid for
every token of a reply would be ruinous, since all but the newest row and column are unchanged
— which is what the key–value cache exists to avoid.
4. Several independent opinions about what is relevant, computed in parallel. One head produces
one set of weights, so it can express one view of which positions matter; with sixteen heads
there are sixteen, each with its own query, key and value matrices and each free to attend
somewhere different. Their outputs are laid end to end and mixed by a further matrix, so
nothing downstream has to choose between them. The width is divided among them rather than
multiplied, so the cost is roughly the same as one head of the full width.
5. That the weights are a genuine measurement — that head really did take about seven tenths of
its blend from that position — and that it is one head in one layer out of dozens of each, after
which everything is mixed again and passed up the stack. A weight says where a blend came from.
It is not a reason, and "the model understood" is a claim about the whole computation made from
a reading of one step of it.
6. Because the output of attention is a sum of the value vectors, and addition does not depend
on order. Swap two tokens and their weights swap with them, so the total is unchanged — this
chapter shows exactly that, with the same output vector before and after. Swapping the last
word would not make the point, because the last position is the one supplying the query: change
the token there and you change what is being asked, so the output changes for a reason that has
nothing to do with order. The demonstration only works on a swap that leaves the querying
position alone. Word order therefore has to be put in separately — added to the embedding
before the stack, applied to the queries and keys as they are formed, or added to the scores
themselves.

> **You understand this when** you can compute one row of attention weights by hand from a
> table of queries and keys, and say what goes wrong if you skip the division.
