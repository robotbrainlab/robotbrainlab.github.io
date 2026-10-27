# The Maths This Book Uses

This is the first chapter of the second half, and it is the shortest kind of chapter there
is: a vocabulary list. Nearly all of it is used by the nine chapters that follow, the rest
by Part II, and nothing in it is harder than arithmetic.

*The problem.* I can follow an argument in words, but the moment someone writes a formula I
stop reading.

*The question.* What is the smallest set of notation that lets me read the rest, and can I
learn it by doing the arithmetic rather than by taking anybody's word for it?

## How to Read a Formula at All

Before any particular notation, the habit that makes all of it readable.

**A formula is a sentence.** It has a subject on the left, a verb somewhere, and objects on
the right. What makes it feel impenetrable is not the ideas but three things that are easy to
fix: unfamiliar letters, operations written as symbols rather than words, and the fact that
nobody reads it aloud to you.

So read it in this order, every time:

1. **Name every symbol.** Not "what does it do" — just "what is this one". A letter you
   cannot name is a letter you cannot think with.
2. **Say what shape each one is.** A single number? A list of numbers? A grid?
3. **Read the operations outward from the innermost brackets**, exactly as you would evaluate
   them.
4. **Substitute the smallest numbers that could possibly work**, and do it by hand.

Step 4 is the one people skip and the one that does the work. A formula you have evaluated
once with two-digit numbers is no longer notation; it is a procedure you happen to know.
Nearly every section below has one.

> **Tip:** If you get stuck, the problem is almost always step 1. Go back and find the symbol
> you have been silently skipping. In this field it is usually a subscript — the small letter
> below the line, which is nearly always "which one of them" and nearly never anything harder.

## Vectors, and What a Dimension Is

A **vector** is an ordered list of numbers. That is the whole definition.

```text
  a = (2, 0, 1, 3)
```

That is a vector with four **dimensions**, which is to say four slots. "Dimension" sounds
spatial and the word comes from geometry, but here it means a position in a list and nothing
more. A model that works in 4,096 dimensions is handling lists of 4,096 numbers.

Two things about those slots matter for everything later.

**The order is fixed and it carries all the meaning.** Slot 3 of one vector is comparable with
slot 3 of another, and with nothing else. Two vectors can only be compared at all if they
have the same number of slots.

**A single slot, on its own, usually means nothing you could name.** You cannot look at slot 3
and say "that one is about cooking". This is not a gap in the explanation — it is a real
property of the vectors this book deals with, and Chapter 9 says why.

> **Note:** The word *vector* gets used for two different things that happen to share a
> notation: a list of numbers you chose (the three numbers describing a product, say) and a
> list of numbers that came out of a model. The arithmetic is identical. What differs is
> whether anybody can tell you what a slot means.

## The Dot Product, and Why It Measures Agreement

Take two vectors with the same number of slots. Multiply them slot by slot, and add up the
results. That is the **dot product**, written `\(a \cdot b\)`{=latex}.

With `\(a = (2, 0, 1, 3)\)`{=latex} and `\(b = (1, 4, 0, 1)\)`{=latex}:

```text
  slot    a     b     a x b
    1     2     1       2
    2     0     4       0
    3     1     0       0
    4     3     1       3
                      ----
                        5
```

So `\(a \cdot b = 5\)`{=latex}. In notation, with `\(n\)`{=latex} slots:

```{=latex}
\[ a \cdot b = \sum_{i=1}^{n} a_i b_i \]
```

Read that with the four steps. `\(a_i\)`{=latex} is slot `\(i\)`{=latex} of `\(a\)`{=latex}.
The `\(\sum\)`{=latex} says: for each `\(i\)`{=latex} from 1 to `\(n\)`{=latex}, work out
`\(a_i b_i\)`{=latex}, and add all of those together. It is the table above, written in one
line.

**Why it behaves like agreement.** Look at what each slot contributes. Two large numbers in
the same slot contribute a large positive amount. A large number paired with zero contributes
nothing. A positive paired with a negative subtracts. So the total is large when the two
vectors are large *in the same slots*, and small when they put their weight in different
places. That is what "agreement" means here, and it is why this one operation turns up
wherever two lists of numbers have to be compared.

**And now the trade-off, which matters more than the definition.** The dot product grows when
the vectors grow, whatever their direction. Take `\(c = 10a = (20, 0, 10, 30)\)`{=latex} —
the same direction as `\(a\)`{=latex}, ten times longer:

```text
  a . b  =   5
  c . b  =  50     ten times larger, same direction
```

Nothing about the agreement changed. Only the length did. So a dot product on its own cannot
tell you whether two things are alike — a long vector will out-score a short one that points
the same way, whenever it agrees with that other vector at all. That is the problem the next section exists to fix.

## Cosine Similarity

The **length** of a vector, written `\(\lVert a \rVert\)`{=latex}, is what you would measure
with a ruler if the slots were coordinates: square every slot, add them, take the square root.

```text
  ||a|| = sqrt(2^2 + 0^2 + 1^2 + 3^2) = sqrt(14) = 3.742
  ||b|| = sqrt(1^2 + 4^2 + 0^2 + 1^2) = sqrt(18) = 4.243
```

**Cosine similarity** is the dot product with the lengths divided out:

```{=latex}
\[ \cos(a, b) = \frac{a \cdot b}{\lVert a \rVert \, \lVert b \rVert} \]
```

```text
  cos(a, b) = 5 / (3.742 x 4.243) = 5 / 15.877 = 0.315
```

Now do the same for `\(c = 10a\)`{=latex}. The dot product was ten times bigger, but so is the
length, and the tens cancel:

```text
  cos(c, b) = 50 / (37.42 x 4.243) = 50 / 158.77 = 0.315
```

**Identical.** Dividing by the lengths throws away magnitude and keeps direction alone, which
is usually what you wanted. The result always falls between `\(-1\)`{=latex} and
`\(1\)`{=latex}: 1 means the same direction, 0 means no agreement, and `\(-1\)`{=latex} means
opposite.

It is called cosine similarity because that fraction *is* the cosine of the angle between the
two vectors. You never need the angle, and nothing in this chapter computes one.

> **Warning:** Cosine similarity measures direction. It does not measure whether two things
> mean the same, whether one answers the other, or whether either is any good. A high score
> says the two lists of numbers point the same way. What follows from that depends entirely on
> where the numbers came from, and Chapter 25 is about the cases where the answer is "nothing
> useful".

## Sums and Products, Written Down

Two symbols, and they work the same way.

`\(\sum\)`{=latex} (capital sigma) means **add these up**. `\(\prod\)`{=latex} (capital pi)
means **multiply these together**. Both are written the same way, and all four parts are
instructions:

```text
      n
     ___
     \        symbol:  add up (or multiply, for a product)
     /__  x   below:   start the counter i at 1
     i=1  i   above:   stop when i reaches n
              beside:  what to do with each i
```

So `\(\sum_{i=1}^{4} a_i\)`{=latex} with `\(a = (2, 0, 1, 3)\)`{=latex} is
`\(2 + 0 + 1 + 3 = 6\)`{=latex}, and `\(\prod_{i=1}^{4} a_i\)`{=latex} is
`\(2 \times 0 \times 1 \times 3 = 0\)`{=latex}.

That is all there is to it. The reason these look harder than they are is that the interesting
part is usually the expression beside the symbol, not the symbol — and that expression is
often itself a formula you already know. The dot product above is just
`\(\sum a_i b_i\)`{=latex}: sigma, with a multiplication beside it.

> **Tip:** You met `\(\prod\)`{=latex} in Chapter 4 without the notation. "Ten steps, each
> right nine times in ten" is a product: `\(0.9^{10} = 0.349\)`{=latex}. Compounding error is
> a `\(\prod\)`{=latex}, and that is why it falls so fast — multiplying numbers below one
> always shrinks them.

## Matrices, and Multiplying Them

A **matrix** is a grid of numbers: rows and columns. You can read it as a stack of vectors,
and which way you read it depends on what you are doing.

```text
  A =  [ 1  2  0 ]     two rows, three columns:
       [ 0  1  3 ]     "a 2 x 3 matrix"
```

**Matrix multiplication is the dot product, done for every pair.** To multiply
`\(A\)`{=latex} by `\(B\)`{=latex}, take each *row* of `\(A\)`{=latex} and each *column* of
`\(B\)`{=latex}, and put their dot product where that row meets that column.

With `\(A\)`{=latex} above and

```text
  B =  [ 2  1 ]     three rows, two columns:
       [ 0  4 ]     "a 3 x 2 matrix"
       [ 1  0 ]
```

the top-left entry of the answer is row 1 of `\(A\)`{=latex} dotted with column 1 of
`\(B\)`{=latex}:

```text
  (1, 2, 0) . (2, 0, 1) = 1x2 + 2x0 + 0x1 = 2
```

All four entries, worked the same way:

```text
          col 1              col 2
  row 1   1x2+2x0+0x1 = 2    1x1+2x4+0x0 = 9
  row 2   0x2+1x0+3x1 = 3    0x1+1x4+3x0 = 4

  AB =  [ 2  9 ]
        [ 3  4 ]
```

**The shape rule, which is the only part worth memorising.** A row of `\(A\)`{=latex} and a
column of `\(B\)`{=latex} must have the same number of slots, or the dot product is not
defined. So the columns of `\(A\)`{=latex} must equal the rows of `\(B\)`{=latex}, and the
answer takes the rows of `\(A\)`{=latex} and the columns of `\(B\)`{=latex}:

```text
  (2 x 3) times (3 x 2)  gives  (2 x 2)
        ^         ^
        these must match
```

When you read later that something "has shape 4096 × 11008", that is a grid of about 45
million numbers, and the shape rule is what tells you what it can be multiplied by.

## Exponentials and Logarithms

One number turns up constantly: `\(e\)`{=latex}, about `\(2.718\)`{=latex}. Raising it to a
power is written `\(e^x\)`{=latex} or `\(\exp(x)\)`{=latex}, and the two mean the same.

```text
  e^0 = 1       e^1 = 2.718      e^2 = 7.389      e^3 = 20.086
```

**What matters is how fast that grows, and that it is always positive.** Each step of 1 in
`\(x\)`{=latex} multiplies the answer by `\(e\)`{=latex}: divide the figures above and
`\(7.389 / 2.718 = 2.719\)`{=latex}, which is `\(e\)`{=latex} to the rounding — the two
figures were each rounded on the way, which is the same effect step 9 of the lab makes
explicit. Equal steps in, multiplication out. And
`\(e^x\)`{=latex} is always positive, for every `\(x\)`{=latex} including negative ones:
`\(e^{-2} = 0.135\)`{=latex}. That property is the entire reason softmax works, two sections
from now.

A **logarithm** undoes it. `\(\ln(y)\)`{=latex} answers "what power of `\(e\)`{=latex} gives
`\(y\)`{=latex}?", so `\(\ln(7.389) = 2\)`{=latex}. The one property to carry:

```{=latex}
\[ \ln(xy) = \ln x + \ln y \]
```

**A logarithm turns multiplication into addition.** Check it:

```text
  ln(2 x 3) = ln(6)  = 1.792
  ln 2 + ln 3 = 0.693 + 1.099 = 1.792
```

That is why logarithms appear wherever many probabilities get multiplied together. Multiply a
thousand numbers below one and you get something too small for a computer to hold; add their
logarithms instead and nothing overflows. Chapter 14 uses exactly this.

## Softmax, Read as a Formula

**Softmax** turns a list of scores into a list of probabilities. It comes back in two later
chapters by name, so it is worth doing by hand once here.

```{=latex}
\[ p_i = \frac{\exp(z_i)}{\sum_{j=1}^{V} \exp(z_j)} \]
```

Read it with the four steps from the start of this chapter. `\(z\)`{=latex} is the list of
scores and `\(z_i\)`{=latex} is score number
`\(i\)`{=latex}; `\(V\)`{=latex} is how many there are. The top is "`\(e\)`{=latex} to the
power of this score". The bottom is "add up `\(e\)`{=latex} to the power of *every* score".
So each answer is one score's share of the total.

Worked on three scores, `\(z = (2.0,\ 1.0,\ 0.1)\)`{=latex}:

```text
  step 1   exponentiate each score
           e^2.0 = 7.389     e^1.0 = 2.718     e^0.1 = 1.105

  step 2   add them up
           7.389 + 2.718 + 1.105 = 11.212

  step 3   divide each by that total
           7.389 / 11.212 = 0.659
           2.718 / 11.212 = 0.242
           1.105 / 11.212 = 0.099
                                 -----
                                 1.000
```

Four properties follow straight from the arithmetic, and all four get used later:

| Property | Why |
|---|---|
| Every result is positive | `\(e^x\)`{=latex} is always positive, whatever the score was |
| They add to exactly 1 | Every share is divided by the same total |
| The order is preserved | A bigger score always gets a bigger share |
| Gaps get exaggerated | Scores 2.0 and 1.0 differ by 1; their shares differ by a factor of 2.7 |

That last one is the interesting one. The scores went in roughly evenly spread, and the
probabilities came out heavily favouring the top. Softmax does not just normalise — it
sharpens. Chapter 13 is about controlling how much.

> **Note:** Nothing about softmax knows what the scores mean. It is arithmetic on a list. When
> you see it inside the attention formula in Chapter 11 and again on the way to a word in
> Chapter 13, it is doing the same three steps both times.

## Big-O: How Cost Grows

**Big-O** notation says how a cost grows as an input gets bigger. It is not a measurement of
time and it carries no units.

`\(O(n)\)`{=latex} — read "order *n*" — means: double the input, double the work. `\(O(n^2)\)`{=latex}
means: double the input, quadruple the work.

```text
      n        n^2
  1,000      1,000,000
  2,000      4,000,000      n doubled,  work x 4
  4,000     16,000,000      n doubled again,  work x 4 again
```

**What it deliberately throws away.** Constants and smaller terms. Something taking
`\(3n^2 + 500n + 9000\)`{=latex} operations is simply `\(O(n^2)\)`{=latex}, because once
`\(n\)`{=latex} is large the squared term is all that matters. So big-O cannot tell you which
of two programs is faster today — one `\(O(n^2)\)`{=latex} program can beat another by a
factor of fifty. It tells you which one gets worse faster, which is the question that decides
whether something survives a bigger input.

A cost can grow in more than one thing at once. You will meet `\(O(n^2 d)\)`{=latex} in
Chapter 11: quadratic in one quantity `\(n\)`{=latex} and linear in another `\(d\)`{=latex}.
Read it as "double `\(n\)`{=latex} and the work goes up four times; double `\(d\)`{=latex} and
it doubles."

> **Tip:** When somebody says an approach "does not scale", the useful reply is "in what?" A
> cost that is quadratic in the number of documents and linear in their length is a different
> engineering problem from the other way round, and the fix is different too.

## Lab: Nine Lines of Arithmetic

No code and nothing to install, though you may use a calculator. Twenty minutes, and there is
a key, so you can be wrong and find out. Use these two vectors throughout:

```text
  u = (3, 1, 0, 2)
  v = (1, 0, 3, 2)
```

**Step 1.** Compute `\(u \cdot v\)`{=latex}, slot by slot, writing the table out.

*Expected result:* `\(3{\times}1 + 1{\times}0 + 0{\times}3 + 2{\times}2 = 3 + 0 + 0 + 4 = 7\)`{=latex}.

**Step 2.** Compute `\(\lVert u \rVert\)`{=latex} and `\(\lVert v \rVert\)`{=latex}.

*Expected result:* both are `\(\sqrt{14} = 3.742\)`{=latex} — `\(9+1+0+4\)`{=latex} and
`\(1+0+9+4\)`{=latex} both come to 14. Two different vectors of the same length; that is
exactly the case a dot product cannot distinguish by magnitude.

**Step 3.** Compute `\(\cos(u, v)\)`{=latex}.

*Expected result:* `\(7 / (3.742 \times 3.742) = 7 / 14 = 0.5\)`{=latex}. Note what happened:
when both lengths are the same, the division is by the square of that length, and the
arithmetic came out clean.

**Step 4.** Now double `\(u\)`{=latex} to `\(u' = (6, 2, 0, 4)\)`{=latex}. Compute
`\(u' \cdot v\)`{=latex} and `\(\cos(u', v)\)`{=latex}.

*Expected result:* the dot product is 14, twice what it was. The cosine is still 0.5. If your
cosine moved, you have divided by the old length.

**Step 5.** Write `\(u \cdot v\)`{=latex} in sigma notation, then say in words what each of
the four parts of the symbol is telling you to do.

*Expected result:* `\(\sum_{i=1}^{4} u_i v_i\)`{=latex}, and four instructions — add up; start
the counter at 1; stop at 4; the thing to add is slot `\(i\)`{=latex} of `\(u\)`{=latex} times
slot `\(i\)`{=latex} of `\(v\)`{=latex}.

**Step 6.** Multiply these two matrices, or say why you cannot:

```text
  P =  [ 1  0  2 ]        Q =  [ 1  1 ]
       [ 3  1  0 ]             [ 0  2 ]
```

*Expected result:* **you cannot.** `\(P\)`{=latex} is 2 × 3 and `\(Q\)`{=latex} is 2 × 2; a
row of `\(P\)`{=latex} has three slots and a column of `\(Q\)`{=latex} has two, so the dot
product is undefined. The shape rule is the whole answer. If you got a grid of numbers, you
multiplied something by something it does not fit.

**Step 7.** Apply softmax to `\(z = (1.0,\ 1.0,\ 3.0)\)`{=latex}. The exponentials you need
are `\(e^{1} = 2.718\)`{=latex} and `\(e^{3} = 20.086\)`{=latex}.

*Expected result:* total `\(2.718 + 2.718 + 20.086 = 25.522\)`{=latex}, and dividing each
exponential by it gives `\((0.106,\ 0.106,\ 0.787)\)`{=latex}. Two equal scores give two equal
shares, and a score two higher takes about four fifths of the whole. That is the sharpening, in
one line.

Your three figures add to 0.999 rather than 1, and that is not a mistake: the two exponentials
you were handed had already been rounded to three places before you divided by them. Carried
to four places the shares are `\((0.1065,\ 0.1065,\ 0.7870)\)`{=latex} and they do sum to
exactly 1. Step 9 makes the same point on purpose.

**Step 8.** Without computing anything: a process is `\(O(n^2)\)`{=latex} and takes 3 seconds
at `\(n = 1{,}000\)`{=latex}. Roughly what does it take at `\(n = 10{,}000\)`{=latex}?

*Expected result:* about 300 seconds. Ten times the input is a hundred times the work. Note
the "roughly": big-O throws away constants, so this is the growth and not a promise.

**Step 9.** Check `\(\ln(4 \times 5) = \ln 4 + \ln 5\)`{=latex}, using
`\(\ln 4 = 1.386\)`{=latex}, `\(\ln 5 = 1.609\)`{=latex} and `\(\ln 20 = 2.996\)`{=latex}.

*Expected result:* `\(1.386 + 1.609 = 2.995\)`{=latex} against `\(\ln 20 = 2.996\)`{=latex}.
They agree to the rounding, which is the point — the last digit differs because the three
logarithms were each rounded, not because the rule is approximate.

## Summary, Key Terms, and Review Questions

### Summary

A **vector** is an ordered list of numbers and a **dimension** is one slot in it; the order
carries the meaning and a single slot usually names nothing. The **dot product** multiplies
two vectors slot by slot and adds the results, which makes it large when both put their weight
in the same slots — but it also grows with length, so **cosine similarity** divides the lengths
out and keeps direction alone, landing between −1 and 1. `\(\sum\)`{=latex} means add these up
and `\(\prod\)`{=latex} means multiply them, and both are read as four instructions: what to
do, where to start, where to stop, and what to do it to. A **matrix** is a grid, and
multiplying two matrices is the dot product of every row with every column, which is why the
columns of the first must match the rows of the second. `\(e^x\)`{=latex} is always positive
and turns equal steps into multiplication; a **logarithm** undoes it and turns multiplication
into addition. **Softmax** exponentiates every score and divides by the total, giving positive
numbers that sum to 1, in the same order, with the gaps exaggerated. **Big-O** says how a cost
grows rather than how long it takes, and throws away constants on purpose.

### Key Terms

| Term | Meaning |
|---|---|
| **Vector** | An ordered list of numbers. Two vectors can be compared only if they have the same number of slots |
| **Dimension** | One slot in a vector. A position in a list, not a direction in space, and usually not nameable on its own |
| **Dot product** | Multiply two vectors slot by slot and add the results. Large when both are large in the same slots — and also larger when either is simply longer |
| **Cosine similarity** | The dot product divided by both lengths, which removes magnitude and keeps direction. Always between −1 and 1 |
| **Length** | What a ruler would measure if the slots were coordinates: square every slot, add them, take the square root |
| **Logarithm** | The inverse of raising `\(e\)`{=latex} to a power. It turns multiplication into addition, which is why it appears wherever many probabilities are combined |
| **Matrix** | A grid of numbers, read as rows or as columns depending on what you are doing |
| **Softmax** | Turns a list of scores into positive numbers that sum to 1, preserving their order and exaggerating the gaps between them |
| **Big-O** | How a cost grows as an input grows, with constants and smaller terms deliberately discarded. Not a measurement of time |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Dot product | `\(a \cdot b = \sum_i a_i b_i\)`{=latex} |
| Cosine similarity | `\(a \cdot b / (\lVert a \rVert \lVert b \rVert)\)`{=latex}, between −1 and 1 |
| Softmax | `\(p_i = \exp(z_i) / \sum_j \exp(z_j)\)`{=latex} |
| Matrix shape rule | (m × k) times (k × n) gives (m × n); the inner numbers must match |
| Logarithms turn products into sums | `\(\ln(xy) = \ln x + \ln y\)`{=latex} |
| `\(e\)`{=latex} | About 2.718. `\(e^x\)`{=latex} is positive for every `\(x\)`{=latex} |
| Quadratic growth | `\(O(n^2)\)`{=latex}: ten times the input, a hundred times the work |

### Review Questions

1. You meet a formula containing a symbol you cannot name. What is the first thing you do, and why that first?
2. Two *pairs* of vectors have the same cosine similarity as each other, but very different dot products. What does that tell you about them?
3. You are asked to multiply a 3 × 5 matrix by a 3 × 5 matrix. What do you say?
4. Name two properties of softmax that follow directly from the fact that `\(e^x\)`{=latex} is always positive.
5. A colleague says their retrieval step "does not scale". What do you ask them?

### Review Answers

1. Name it — just name it, before asking what it does. A letter you cannot name is a letter you cannot think with, so every later step is guesswork built on it. Then say what shape it is: a single number, a list, or a grid. In this field the symbol being silently skipped is usually a subscript, and a subscript is almost always "which one of them" rather than anything harder. Only once every symbol has a name and a shape is it worth reading the operations, and only then is it worth substituting small numbers — which is the step that turns the formula from notation into a procedure you know.
2. That within each pair the vectors sit at the same angle, and that one pair is simply longer than the other. Cosine ignores length by construction, so two pairs with identical cosines can have dot products differing by any factor you like, purely because one pair is longer. If the number you care about is "are these alike", the cosine is the one to look at.
3. That it is not defined. A row of the first has five slots and a column of the second has three, so there is no dot product to take. The inner numbers of (3 × 5) and (3 × 5) do not match. Either the second needs transposing — making it 5 × 3, which would give a 3 × 3 answer — or one of the shapes is wrong.
4. Every output is positive, because every power of `\(e\)`{=latex} is positive; and the outputs can be read as probabilities at all, because positive numbers each divided by their own total necessarily land between 0 and 1 and sum to exactly 1. Order preservation follows too, since `\(e^x\)`{=latex} is increasing.
5. In what? A cost can grow in the number of documents, the length of each one, the number of users, or several at once, and the fix differs for each. Ask which quantity is growing, and what the growth is in that quantity — linear, quadratic, or something else. Also ask what the constant is, because big-O discards it and a quadratic process on small inputs is often perfectly fine.

> **You understand this when** you can take a formula you have not seen before, name every
> symbol in it, say what shape each one is, and work it out with two-digit numbers.
