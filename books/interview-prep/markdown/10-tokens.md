# Tokens

Chapter 9 said your text arrives at the model as a list of indexes into a fixed vocabulary,
and left four questions open: why the pieces are fragments rather than words, how the list
is built, why your short question can cost more than somebody else's long one, and how to
count before you send. This chapter answers all four, and the way it answers the second is
by building a vocabulary by hand, from a corpus of five words, so that nothing here has to
be taken on trust.

*The problem.* I was billed for "tokens". I don't know what one is, or why my short question
cost more than someone else's long one.

*The question.* What is a token, where does the list of them come from, and what does
knowing that let me predict about my bill and my waiting?

## Why Not Words, and Why Not Letters

A **token** is one entry in the model's vocabulary — one of the pieces text gets cut into
before anything else happens. The obvious question is why the pieces are not simply words,
and the answer is worth working through, because it explains nearly everything odd about
tokens afterwards.

**Words fail for two reasons, and the first is arithmetic.** Chapter 9 showed that the
embedding table holds one row per vocabulary entry, and that the last step of a forward pass
produces one score per vocabulary entry. Both of those grow with the vocabulary. English has
hundreds of thousands of word forms before you count names, product codes, typos and
hyphenations, so suppose you wanted 500,000 entries at a width of 4,096:

```text
  500,000 x 4,096 = 2,048,000,000 numbers
```

Two billion parameters in the lookup table alone — and, where the output matrix is a separate
one rather than the embedding table read backwards, the same again. That is more than many
whole models.

**The second reason is worse, because no size of vocabulary fixes it.** A word that is not in
the list has no row. Not a poor row — no row at all. Every name you have never heard of, every
new product, every misspelling, every word in a language that was not planned for arrives as
nothing. The usual patch is one shared "a word I do not have" entry that all of them map to,
which keeps the program running and throws the word itself away: every unknown name becomes
the same unknown name. That is not a quality problem, it is a hole.

**Letters fix the hole and create a different one.** An alphabet, digits and punctuation make
a vocabulary of a hundred-odd entries. Every *word* is representable — no word arrives as
nothing — and the lookup table is tiny. But an English word runs about five characters, so cutting at letters makes the list of
pieces several times longer than cutting at words — and Chapter 9 showed that every piece of
a reply costs one whole forward pass. Several times the pieces is several times the passes,
and the input grows the same way.

So the two obvious answers fail in opposite directions: words give you a vocabulary too large
to hold and still cannot represent everything, letters leave no unknown words but make the
sequences too long.

**The working answer is to let the corpus decide where to cut.** Keep single characters in
the vocabulary, so nothing is ever unrepresentable. Then add, as extra entries, the
*combinations* that turn up often enough to be worth a seat of their own. A piece that is
part of a word rather than a whole one is called a **subword**, and the result is a
compromise that leans exactly where the text leans:

- Common words end up as one token each.
- Rare words are spelled out of several pieces.
- Nothing is ever unrepresentable, because the single pieces are still in there.

**And "single pieces" means bytes, not letters** — which is where the *byte* in the usual name
comes from. A vocabulary built from the letters of one alphabet would still have no answer for
a script nobody planned for. A computer stores text as bytes, there are exactly 256 of them,
and every one of them is in the vocabulary from the start. Any text whatever can therefore be
represented, in the worst case one token per byte. That is the convention for the models this
book is about; a tokeniser built without it falls back to the shared unknown entry instead,
and loses the text. Keep that worst case in mind: it is the
ceiling that the section on other languages lands against.

The rest of this chapter is what that does to you.

## Building the Vocabulary: Merge the Commonest Pair

The usual way to pick those combinations is **byte-pair encoding**, usually shortened to BPE[]{idx="BPE"}.
The name sounds forbidding and the procedure is four lines:

1. Start with a vocabulary of every single character in the corpus — in a real run, every one
   of the 256 bytes.
2. Count every adjacent pair of symbols across the whole corpus.
3. Merge the commonest pair into one new symbol, and add it to the vocabulary.
4. Go back to step 2. Stop when the vocabulary is the size you wanted.

That is the whole idea. It is greedy compression: at each step, take the saving that is worth
most right now, and never reconsider. A real run starts from the 256 bytes; the worked example
below starts from letters instead, because a corpus of five English words contains nothing
else and letters are what you can read. The list of merges, in the order they were made, is the
**merge list**, and it is kept — the same merges are replayed, in the same order, every time
text is tokenised afterwards.

Now do it. Here is a corpus of five words, with how often each occurs:

```text
  cat        7
  cats       3
  hat        5
  hats       2
  catalyst   1
```

The alphabet is the seven letters that occur: a, c, h, l, s, t, y. Every word starts as its
letters, kept apart:

```text
  c a t          7
  c a t s        3
  h a t          5
  h a t s        2
  c a t a l y s t  1
```

**Merge 1.** Count every adjacent pair, weighting each by how often its word occurs. `at`
occurs once in every one of the five words, so it scores `\(7+3+5+2+1 = 18\)`{=latex}:

```text
  pair   where it occurs                       count
  at     cat, cats, hat, hats, catalyst        18
  ca     cat, cats, catalyst                   11
  ha     hat, hats                              7
  ts     cats, hats                             5
  ta     catalyst                                1
  al     catalyst                                1
  ly     catalyst                                1
  ys     catalyst                                1
  st     catalyst                                1
```

`at` wins. Merge it, and the corpus becomes:

```text
  c at           7
  c at s         3
  h at           5
  h at s         2
  c at a l y s t  1
```

That is what "compression" means here, and it is countable. The corpus held 64 symbols before
the merge and holds 46 after. The saving is 18 — the pair's count exactly, because each of
those 18 occurrences became one symbol instead of two. **Merge the commonest pair** is just
another way of saying *take the biggest saving available this step*.

**Merge 2.** Count again — and notice that the counts have changed, because the symbols have.

```text
  pair    count
  c+at    11        (cat 7, cats 3, catalyst 1)
  h+at     7        (hat 5, hats 2)
  at+s     5        (cats 3, hats 2)
  at+a     1
  a+l      1
  l+y      1
  y+s      1
  s+t      1
```

`cat` wins at 11. The vocabulary now holds a piece that is a whole word, and nobody put it
there — it arrived because the letters kept turning up together.

**Merges 3, 4 and 5.** The same procedure, three more times:

```text
  merge 3   h + at    = hat     at 7
  merge 4   cat + s   = cats    at 3
  merge 5   hat + s   = hats    at 2
```

Five merges. Stop there, and the vocabulary is the seven letters plus the five merged
symbols — twelve entries:

```text
  a  c  h  l  s  t  y  at  cat  hat  cats  hats
```

## What the Merges Bought

Tokenise the five words with that vocabulary by replaying the merges in order:

```text
  word       tokens                     how many
  cat        cat                             1
  cats       cats                            1
  hat        hat                             1
  hats       hats                            1
  catalyst   cat a l y s t                   6
```

**Four of the five words are now one token each, and the fifth is six.** Nothing about
"catalyst" is harder than "cats". It is longer, and more to the point it is *rarer*, so none
of the five merges was spent on it. The merges went where the corpus was dense.

This is the single most useful fact in the chapter, and it is now a thing you have watched
happen rather than a thing you have been told:

> **A token is not a unit of meaning or a unit of length. It is a unit of frequency in
> somebody else's corpus.**

Most surprises about token counts for the rest of your career follow from that sentence. Your
short question cost more than somebody else's long one because theirs was made of pieces the
corpus had seen a great deal and yours was not.

> **Note:** The merge list is part of the model, fixed when the model was built, exactly like
> the embedding table of Chapter 9. As a caller you do not choose it and cannot change it, and
> two models with different vocabularies can cut the same sentence into different numbers of
> pieces — can, not must: step 8 of the lab builds a different vocabulary that happens to give
> the same count. A token count
> is therefore a fact about a *particular* model, never about your text on its own.

## The Space Belongs to the Word

One convention catches everybody once, so meet it now.

Real tokenisers attach the space *before* a word to the word, rather than treating it as a
separate piece. So in the sentence "the cat sat", the pieces are "the", " cat", " sat" — the
two that follow a space carry it, and the one at the start does not. That is why Chapter 9's
worked example listed the vocabulary as `the, cat, sat, mat, on`: those stand for the pieces
as a tokeniser would hold them, printed without their leading spaces so the table would read.

Two consequences, and the second one costs people real money.

**"cat" and " cat" are different tokens.** They have different rows, different indexes, and
there is nothing that tells the model they are related other than the fact that they usually
turn up in similar places. A word at the start of a line and the same word mid-sentence are
genuinely different inputs.

**A trailing space changes everything after it.** If your instructions end with a space where
the model expects to continue, the next piece can no longer carry its own
leading space, and the model has to produce a different token than the one it would otherwise
have produced. This is a real source of "why did the output format change when I only edited
whitespace".

> **Tip:** When a prompt behaves strangely after an edit that "changed nothing", check the
> whitespace at the end of it first. It is the cheapest thing to check and it is wrong
> surprisingly often.

## Input Tokens and Output Tokens

Your bill and your waiting both have two halves, and the halves are counted separately.

**Input tokens** are everything you send on the call: the instructions, any material your
code attached, and the request itself — all of Chapter 2's context, counted as pieces.
**Output tokens** are what comes back.

They are priced differently, and output costs several times input, which Chapter 1 worked
through with made-up rates. What Chapter 1 could not say, because the word had not been
given to you, is what the unit is. It is this one. Not words, not characters, not requests.

They also behave differently in time, and Chapter 9 is why:

| | Input tokens | Output tokens |
|---|---|---|
| What they are | Everything you send | Everything that comes back |
| What they cost | The cheaper rate | Several times more |
| What they do to the wait | Set how long before the first word appears | Set how long the rest takes, one pass each |
| Who controls them | You, exactly | You, by capping it or asking for less |

The last row is the one worth sitting with. You can count your input before you send it, to
the token. You cannot count your output in advance — you can cap it, and you can ask for
brevity, but within that cap the model decides when it stops. Chapter 13 is where stop conditions and
length limits live, Chapter 15 is why the two halves cost such different amounts of time from
the inside, and Chapter 53 is what to do about the bill.

> **Warning:** A long reply is the expensive half and the slow half at once. An instruction
> that produces six paragraphs where one would do is not a style problem; it is a cost and
> latency problem with a style-shaped cause.

## Why Code and Other Languages Cost More

Both follow from the merge procedure, and once you have watched it run neither is surprising.

**Code.** The merges were bought with a corpus that is mostly prose, so the pieces that got
seats are mostly prose. Code then pays in three ways at once. Its punctuation is dense, and
each mark that did not earn a merge is a token on its own. Its indentation is runs of spaces,
which are often several tokens of nothing. And its identifiers are made-up compounds —
`get_user_by_id`, `maxRetryCount` — that no corpus has seen often enough to merge, so each
one is cut into several pieces.

**Other languages.** English dominated the corpora these vocabularies were built from, so the
merges were spent on English. A language written in another script often has no merged pieces
at all, and falls back towards that ceiling of one token per byte — a piece per character
where merges joined that character's bytes, several per character where they did not, because
a character outside the common range is itself stored as more than one byte. The same meaning, in the same number of characters, can cost several times more
than it does in English.

> **Note:** How much more is a dated detail and a vendor-specific one. It moves whenever a
> model ships a new vocabulary, and newer vocabularies have generally narrowed the gap. The
> *reason* for the gap — merges are spent where the corpus is dense — does not move, and
> neither does the advice: if you serve a language other than English, measure its token cost
> yourself before you price anything.

Both cases are the same case. You are not being charged for difficulty. You are being charged
for how well your text matches the corpus somebody else compressed.

## Why It Cannot Count the Letters in a Word

Here is the one everybody meets. Ask a model how many times a letter appears in a word and it
will often get it wrong, with complete confidence, while being able to write you a working
program that gets it right.

Chapter 9 has already given you the answer, so put the two halves together. The word arrives
as one index, or two, or three. That index is looked up in the embedding table, and from
there the arithmetic works on the vector and never on the token. **A token's spelling is not
in the input.** Nothing in the model's input says that this piece is made of ten characters of
which three are the same, because the piece is a seat number and the seat number is not
spelled. Some of the pieces may be single letters — `catalyst` above came out as five of them
after `cat` — but even then it is the seat number that arrives, not the letter.

So the model is not counting badly. It is answering a question about something it was not
given, from whatever it absorbed about that word's spelling during training — which is
real, but is recall rather than counting, and recall of a thing nobody was being tested on.

Two things follow that are worth saying out loud in an interview.

**It is not a bug and a better model does not necessarily fix it.** It is a consequence of the
input representation. Models have got better at these questions without gaining the ability
to see letters; the representation has not changed.

**The fix is not to ask harder.** If the answer has to be right, do not ask the model to count
— have it write the code that counts, or do the counting in your own code. This is one
instance of a pattern that recurs through this book: a check that code can do belongs in code.

Chapter 16 is where this sits alongside the rest of the model's characteristic failures,
including what tokenisation does to arithmetic and to digits.

## Counting Before You Send

Two ways, and you need both.

**The rough one, for deciding things.** English prose runs about four characters to the token,
or about three-quarters of a word. So:

```text
  1,000 tokens  ~  750 words  ~  4,000 characters of prose
```

That is enough to answer "will this document fit", "roughly what will this feature cost", and
"is this instruction block worth trimming". It is also enough to spot an error of the kind
that matters — a number ten times too big.

**The exact one, for anything you are billed on.** Count with the tokeniser belonging to the
model you are calling. That program — the one that cuts text into tokens and maps each to its
index, using one model's vocabulary and merge list — is its **tokeniser**. Providers publish
theirs, or an endpoint that counts for you, and the
count is a function of the vocabulary and the merge list, so a count from the wrong model does
not carry. Your reply also
reports what was actually used, which is the figure to trust and the figure to log.

> **Warning:** Do not estimate the input to a feature that runs ten thousand times a day. The
> rule of thumb is for sizing a decision, not for sizing a bill. The gap between four
> characters per token and the truth for *your* text — which may be full of code, names, or
> another language — is exactly the gap that makes a feature cost three times what you
> budgeted.

> **Note:** "About four characters" is a current convention and a dated one. It is a property
> of today's English-heavy vocabularies, not a law, and a model with a larger vocabulary cuts
> the same prose into fewer pieces. Measure it for your own text and your own model rather
> than carrying the number around.

## Lab: Build a Vocabulary by Hand

Pen and paper for the first half, then about thirty lines of Python. Thirty minutes, and there is
a key for every step.

The corpus, five words with their counts:

```text
  run      6
  runs     4
  sun      5
  suns     1
  runner   2
```

**Step 1.** Write down the alphabet — every distinct character that occurs — and say how many
entries the vocabulary starts with.

*Expected result:* e, n, r, s, u. Five entries. Note that `t`, `a` and the rest of the
alphabet are *not* in it: the vocabulary is built from this corpus and nothing else.

**Step 2.** Split every word into characters and count every adjacent pair, weighting each
pair by how often its word occurs. Which pair wins, and with what count?

*Expected result:* `un` at 18. It occurs once in each of the five words, so it scores
`\(6+4+5+1+2 = 18\)`{=latex}. The full table, which is worth writing out because step 3
depends on it:

```text
  un  18     ru  12     su  6     ns  5
  er   2     ne   2     nn  2
```

**Step 3.** Merge `un` into one symbol, rewrite the corpus, and count the pairs again. Which
pair wins now, and why is its count not 18?

*Expected result:* `run` at 12, from `r + un`. The count is 12 and not 18 because `ru` only
occurred in the three words beginning with r — run (6), runs (4) and runner (2). Merging
changes which pairs exist, so every count has to be taken again from the new corpus. The new
table:

```text
  run  12     sun  6     uns  5     er  2     ne  2     unn  2
```

**Step 4.** Carry on to five merges in total. Write down the five merges in order.

*Expected result:*

```text
  merge 1   u + n     = un      at 18
  merge 2   r + un    = run     at 12
  merge 3   s + un    = sun     at 6
  merge 4   run + s   = runs    at 4
  merge 5   ???
```

Merge 5 is the interesting one, and it is step 5.

**Step 5.** At merge 5 the remaining pairs are `er` at 2, `ne` at 2 and `runn` at 2, with
`suns` at 1. Three pairs are tied at the top. What does the procedure as stated tell you to
do?

*Expected result:* **nothing — the procedure does not say.** "Merge the commonest pair" has no
answer when three are equally common, and this is not a hole in the explanation; it is a hole
in the idea, which each implementation settles in its own way — often by accident rather than
by design, taking whatever order a sort or a dictionary happens to give. Different
settlements give different vocabularies from the same corpus. For the rest of this lab, break ties
alphabetically, so merge 5 is `e + r = er`.

**Step 6.** With those five merges, tokenise all five words. How many tokens is each?

*Expected result:*

```text
  run      run            1
  runs     runs           1
  sun      sun            1
  suns     sun s          2
  runner   run n er       3
```

`suns` and `runs` are the same shape and differ only in how often they occurred — four times
against once — and that alone is why one is a single token and the other is two.

**Step 7.** Now the program. In a new empty folder, save this as `merges.py`:

```python
from collections import Counter

corpus = {"run": 6, "runs": 4, "sun": 5, "suns": 1, "runner": 2}
words = {tuple(w): n for w, n in corpus.items()}

def pair_counts(words):
    counts = Counter()
    for word, n in words.items():
        for pair in zip(word, word[1:]):
            counts[pair] += n
    return counts

def apply_merge(words, a, b):
    out = {}
    for word, n in words.items():
        new, i = [], 0
        while i < len(word):
            if i + 1 < len(word) and word[i] == a and word[i + 1] == b:
                new.append(a + b)
                i += 2
            else:
                new.append(word[i])
                i += 1
        out[tuple(new)] = n
    return out

for step in range(1, 6):
    counts = pair_counts(words)
    # highest count first, then alphabetical: the tie-break of step 5
    (a, b), n = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    print(f"merge {step}: {a} + {b} = {a + b}  at {n}")
    words = apply_merge(words, a, b)

for word, n in words.items():
    print(f"  {''.join(word):<8} {' '.join(word):<12} {len(word)} token(s)")
```

*Expected result:* exactly this, matching your steps 4, 5 and 6 line for line.

```text
merge 1: u + n = un  at 18
merge 2: r + un = run  at 12
merge 3: s + un = sun  at 6
merge 4: run + s = runs  at 4
merge 5: e + r = er  at 2
  run      run          1 token(s)
  runs     runs         1 token(s)
  sun      sun          1 token(s)
  suns     sun s        2 token(s)
  runner   run n er     3 token(s)
```

**Step 8.** Change the tie-break and watch the vocabulary change. Replace the sort key with
`key=lambda kv: (kv[1], kv[0]), reverse=True`, which still takes the commonest pair but
settles ties the other way round. Re-run. Which merge differs, and what happens to `runner`?

*Expected result:* merges 1 to 4 are identical, because nothing was tied. Merge 5 becomes
`run + n = runn` instead of `e + r = er`, and `runner` comes out as `runn e r` rather than
`run n er` — still 3 tokens, but different pieces, from the same corpus and the same rule.
**The tie-break is not part of the idea and it changes the vocabulary**, which is step 5's
point made by a program rather than by an argument.

**Step 9.** Now make a word commoner and watch a different word get dearer. Change `suns` from
1 to 7, leave everything else alone, re-run with the original tie-break. What is `runner` now,
and why?

*Expected result:* **four tokens**, up from three, in a word you did not touch.

```text
merge 1: u + n = un  at 24
merge 2: r + un = run  at 12
merge 3: s + un = sun  at 12
merge 4: sun + s = suns  at 7
merge 5: run + s = runs  at 4
  run      run          1 token(s)
  runs     runs         1 token(s)
  sun      sun          1 token(s)
  suns     suns         1 token(s)
  runner   run n e r    4 token(s)
```

`suns` is now common enough to win merge 4, which pushes `runs` to merge 5 and leaves no merge
at all for `er`. There are still five merges; they were simply spent elsewhere. **At a fixed
vocabulary size the merges are zero-sum**, so every piece of text that is well compressed is
well compressed at the expense of some other text — which is "Why Code and Other Languages
Cost More" in one experiment, and the reason your language, your code and your identifiers
cost what they do.

**Step 10.** Estimate, with the rule of thumb, what it would cost to send the program in step
7 to a model as input.

*Expected result:* the program is about 1,100 characters, so about 275 tokens at four
characters each. Then the part that matters: it is **code**, so expect the real count to be
well above that — dense punctuation, runs of indentation and made-up identifiers like
`pair_counts` and `apply_merge` are exactly what the merges were not spent on. The rule of
thumb sized the decision; only the tokeniser of the model you are calling can size the bill.

## Summary, Key Terms, and Review Questions

### Summary

A **token** is one entry in the model's vocabulary, and the pieces are subwords rather than
words because words make the embedding table and the output step enormous while still leaving
text they cannot represent, and single characters make the sequence several times longer, at
one forward pass each. The base vocabulary is the 256 bytes, which is why nothing is ever
unrepresentable and why the worst case is one token per byte. **Byte-pair encoding** builds the vocabulary by
starting from the 256 single bytes, counting every adjacent pair across a corpus, merging the
commonest, and repeating; the ordered **merge list** is kept and replayed on every piece of
text afterwards. The result is that common words become one token and rare ones are spelled
out of several, so **a token is a unit of frequency in somebody else's corpus**, not a unit of
meaning or of length. The leading space belongs to the word, so "cat" and " cat" are different
tokens. **Input tokens** and **output tokens** are counted and priced separately, output costs
several times more and sets how long the rest of the reply takes, and only the input can be
counted before you send. Code and non-English text cost more because the merges were spent on English prose.
A model has no way to count the letters in a word, because a token's spelling is not in its
input; a right answer is recall of the spelling rather than counting. Count
roughly at four characters to the token, and exactly with the tokeniser of the model you are
calling.

### Key Terms

| Term | Meaning |
|---|---|
| **Token** | One entry in a model's vocabulary — usually a piece text is cut into. Beyond the single bytes, which are always there, which pieces earned an entry is a matter of frequency in the corpus the vocabulary was built from — not of meaning or length |
| **Subword** | A token that is part of a word rather than a whole one. What makes it possible to represent a word the vocabulary has never seen |
| **Tokeniser** | The program that cuts text into tokens and maps them to indexes, using one model's vocabulary and merge list. A count does not carry from one model's tokeniser to another's |
| **Byte-pair encoding (BPE)** | Building a vocabulary by starting from the 256 single bytes and repeatedly merging the commonest adjacent pair in a corpus until the vocabulary is the size wanted. Starting from bytes is what makes any text at all representable |
| **Merge list** | The merges, in the order they were made. Kept with the model and replayed in that order to tokenise any later text |
| **Input tokens** | Everything you send on a call — instructions, attached material and the request. Countable exactly before you send |
| **Output tokens** | Everything that comes back. Priced several times higher than input, one forward pass each, and not knowable in advance |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Rule of thumb, English prose | 1 token ≈ 4 characters ≈ ¾ of a word; 1,000 tokens ≈ 750 words |
| What a token really measures | Frequency in the corpus the vocabulary was built from, not meaning or length |
| The merge step | Merge the commonest adjacent pair; recount; repeat |
| Why a word is one token | It was common enough for a merge to be spent on it |
| Which half is dear | Output, at several times input, and one forward pass per token |
| What a token count is a fact about | One particular model. A count does not carry across vocabularies |
| The worst case | One token per byte — the most byte-pair encoding can ever charge you |

### Review Questions

1. Why not just give the model a vocabulary of words? Give both reasons.
2. A corpus has `low` 8 times and `lowest` 2 times. On the first merge, what is the count for the pair `lo`, and why?
3. Your colleague says a document is "about 3,000 tokens" because they counted 3,000 words. What do you tell them?
4. Why does the same sentence, translated, cost several times as many tokens in one language as in another?
5. A model tells you "strawberry" has two letter R's. Explain what went wrong without using the word "bug".
6. You trim 200 words of instructions from a prompt that runs ten thousand times a day. What do you need to know before claiming a saving?

### Review Answers

1. First, size: the embedding table holds one row per entry and the output step produces one
score per entry, so a 500,000-word vocabulary at a width of 4,096 is over two billion
parameters in the lookup table alone, and the same again wherever the output matrix is
separate rather than the embedding table read backwards. Second, and worse,
coverage: a word not in the list has no row at all, so every name, typo, new product and
unplanned language would arrive as one shared "unknown" entry, with the word itself thrown
away. Subwords fix the second completely — all 256 single bytes are in the vocabulary from the
start, so any text at all can be represented — and the first well enough.
2. Ten. The pair is counted once per occurrence of each word, weighted by that word's count,
so `lo` scores 8 from `low` plus 2 from `lowest`. The thing to get right is that you are
counting across the corpus with weights, not counting distinct words.
3. That words and tokens are different units, and the direction of the error is predictable:
English prose runs about three-quarters of a word to the token, so 3,000 words is nearer 4,000
tokens. Then that the rule of thumb is only for sizing a decision — if the document is going
into a feature they are billed for, count it with the tokeniser of the model they are calling,
because the number is a property of that model's vocabulary and not of the text.
4. Because the merges were spent on whichever language dominated the corpus the vocabulary was
built from, which has been English. A language in another script may have no merged pieces at
all and fall back to one or more tokens per character. Nothing about the language is harder;
the compression simply was not bought for it.
5. A token's spelling is not in the model's input. The word arrives as one index, or two, and
from the lookup onwards the arithmetic works on a vector and never on the characters — so it is
answering a question about something it was never given, from what it absorbed about the
word's spelling in training. That is recall, not counting. If the answer must be right, have
it write code that counts, or count in your own code.
6. Three things. How many tokens those 200 words actually are, for the model you call, rather
than 267 by the rule of thumb — and if the text is code or identifiers, the gap can be large.
That input is the cheaper half, so the saving is smaller than the same cut to the output would
be. And whether quality held: a shorter instruction is only a saving if the feature still
works, which is a measurement and not a reading.

> **You understand this when** you can explain why "cats" and "catalyst" cost one token and
> six, without mentioning length or difficulty.
