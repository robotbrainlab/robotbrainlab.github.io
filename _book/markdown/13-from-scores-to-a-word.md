# From Scores to a Word

Chapter 9 ended with a list of probabilities and a flat refusal to pick one. This chapter picks
one. It is the last step of the pipeline and the only one you control from the outside: the
settings on your call act here and nowhere else. It also answers the question in its opening
problem, which is the most common surprise in this whole field and has nothing to do with
machine learning.

*The problem.* I set temperature to zero and still got two different answers.

*The question.* How does a distribution become one word, what do the settings actually do to
the numbers, and why is none of it a guarantee?

## Where We Are

Chapter 9's worked example ended here. A vocabulary of five, and one forward pass just
finished:

```text
  token   score     p
  the       2     0.012
  cat       5     0.234
  sat       3     0.032
  mat       4     0.086
  on        6     0.636
```

Those raw scores have a name. They are the **logits** — one per vocabulary entry, straight out
of the final matrix multiplication, before anything has been done to them. They are not
probabilities: they can be negative, they do not add to anything in particular, and only their
*differences* matter — for a reason the next section works out in one line.

Everything in this chapter happens between that table and one token. The model is finished. It
has handed over five numbers and taken no view on which of them you should use.

## Greedy: Take the Biggest

The simplest rule is to take the highest-scoring token every time. That is **greedy decoding**,
and it is what "temperature zero" means in practice.

Here it picks "on", because 6 is the largest logit. Note that you do not need the softmax at
all to do this: softmax preserves order — Chapter 8's third property — so the biggest logit is
the biggest probability, and converting them changes nothing about which one wins.

**And this is where the earlier claim about differences gets paid.** Add 5 to every logit, so
they become `\((7, 10, 8, 9, 11)\)`{=latex}. Every term on the top of the softmax gains a
factor of `\(e^5\)`{=latex}, and so does the total on the bottom — so it cancels, and every
probability comes out exactly as before. Logits carry no zero point. Only the gaps between
them mean anything, which is why a logit of 6 tells you nothing on its own.

Greedy sounds like it should be the good option, and it is the right choice for some work and
the wrong one for a surprising amount of it. Two reasons.

**It is locally greedy, and text is not local.** Taking the most likely next token at every
step is not guaranteed to produce the most likely sentence, and usually does not. A high-scoring first token can lead into a
corner where every continuation is poor, while a second-choice first token opens onto something
much better. Nothing in the procedure looks ahead.

**It makes the model repeat itself.** Once a loop begins — a phrase, a sentence shape, a list
item — the tokens that continue the loop are exactly the ones made likely by the loop so far,
and greedy takes them every time. Anyone who has watched a model produce the same paragraph
four times has watched this.

So the alternative is to *sample*: treat the probabilities as probabilities and draw one. "on"
about 636 times in a thousand, "cat" about 234 times, "the" about 12. The rest of this chapter is about
reshaping that distribution before you draw from it.

## Temperature

**Temperature** divides the logits before softmax. That is the whole definition:

```{=latex}
\[ p_i = \frac{\exp(z_i / T)}{\sum_{j} \exp(z_j / T)} \]
```

Chapter 8's softmax with one extra symbol. And its effect follows from the property Chapter 8
ended on — *gaps get exaggerated* — because dividing the logits divides the gaps between them.

Work the same five logits at three settings.

```text
  T = 1     logits unchanged       (2, 5, 3, 4, 6)
            e^2 = 7.389   e^5 = 148.413   e^3 = 20.086
            e^4 = 54.598  e^6 = 403.429
            total = 633.915

            the 0.012   cat 0.234   sat 0.032
            mat 0.086   on  0.636
```

```text
  T = 0.5   logits doubled         (4, 10, 6, 8, 12)
            total = 188,220.242

            the 0.000   cat 0.117   sat 0.002
            mat 0.016   on  0.865
```

```text
  T = 2     logits halved          (1, 2.5, 1.5, 2, 3)
            total = 46.857

            the 0.058   cat 0.260   sat 0.096
            mat 0.158   on  0.429
```

Read down the "on" column: 0.636, then 0.865, then 0.429. **Below 1, temperature sharpens the
distribution; above 1, it flattens it.** The order never changes — dividing every logit by the
same positive number cannot reorder them — so temperature does not change what the model thinks
is most likely. It changes how much of the rest is in play.

| | Low temperature | High temperature |
|---|---|---|
| The distribution | Sharper | Flatter |
| Top token's share | Goes up | Goes down |
| What you get | Predictable, repetitive | Varied, sometimes incoherent |
| Where it belongs | Extraction, classification, code | Drafting, brainstorming, variety |

> **Note:** The numbers at `\(T = 2\)`{=latex} print as adding to 1.001, for the rounding reason
> you have now met three times. And at `\(T = 0.5\)`{=latex} "the" prints as 0.000 — it has not
> been removed, it is about 0.0003. Nothing here deletes an option; temperature only moves
> weight around.

**And now the thing the formula makes obvious.** Temperature zero would mean dividing by zero,
which is not defined. What most providers do at `\(T = 0\)`{=latex} is not compute that limit — they
switch to greedy decoding and take the biggest logit, and the rest clamp the temperature to
something tiny, which comes to the same thing. So "temperature zero" is not a temperature
at all. It is a different procedure wearing the same dial, and that matters for the last section
of this chapter.

## Top-k and Top-p

Temperature reshapes the whole distribution. The other two settings cut parts of it away
entirely, and then renormalise what is left so it still adds to 1.

**Top-k** keeps the `\(k\)`{=latex} highest-scoring tokens and discards the rest. At
`\(k = 2\)`{=latex}, on the `\(T = 1\)`{=latex} distribution above:

```text
  kept     on  0.636    cat  0.234      total kept 0.870
  renormalised
           on  0.636 / 0.870 = 0.731
           cat 0.234 / 0.870 = 0.269
```

Three tokens now have probability exactly zero and cannot be produced however many times you
sample.

**Top-p**, also called nucleus sampling, keeps the smallest set of tokens whose probabilities
add to at least `\(p\)`{=latex}. Sort by probability and accumulate:

```text
  on    0.636    running total 0.636
  cat   0.234    running total 0.870
  mat   0.086    running total 0.956   <- first to reach 0.9
  sat   0.032
  the   0.012
```

At `\(p = 0.9\)`{=latex} you keep *three* tokens, not two: after two the total is 0.870, which
is short of 0.9, so "mat" comes in and the total overshoots to 0.956. Renormalising:

```text
  on  0.636 / 0.956 = 0.665
  cat 0.234 / 0.956 = 0.245
  mat 0.086 / 0.956 = 0.090
```

**The difference between them is the whole reason top-p exists.** Top-k keeps the same *number*
of options whatever the distribution looks like. When the model is confident — one token at
0.98 — top-k with `\(k = 40\)`{=latex} keeps thirty-nine options that should never have been in
play. When the model is genuinely uncertain across a hundred near-equal tokens, the same setting
throws away sixty of them for no reason. Top-p keeps however many it takes to cover the mass,
so it is narrow where the model is sure and wide where it is not. The cost is that the number
of options is no longer something you can state in advance.

> **Tip:** These interact, and the order is: temperature first, then the cut, then draw. Raising
> temperature and tightening top-p at the same time is a common way to get much less than you
> asked for, because the tail the flattening opened up is cut away again. Change one at a time — which is
> Chapter 18's discipline, arriving early.

## How a Reply Ends

A reply has to stop. Three things stop it in the ordinary case, and only one of them is the
model's doing.

**The model emits a stop token.** A vocabulary also holds entries that are not pieces of text —
Chapter 10's list of merged pieces is not the whole of it — and one of them means *this is the
end*. That entry is the **stop token**, often called an end-of-sequence token. When it is
sampled, generation stops. This is the mechanism to understand, because it is not special: the
stop token is a seat in the vocabulary like any other, it gets a logit like any other, and it is
chosen by exactly the procedure above. **A model finishes talking by predicting that it has
finished.**

Which means it has a probability, and you can read it. Suppose a forward pass somewhere in a
reply gives these three logits:

```text
  token     logit     p
  more        2      0.245
  text        1      0.090
  <end>       3      0.665
```

```text
  e^2 = 7.389   e^1 = 2.718   e^3 = 20.086
  total = 7.389 + 2.718 + 20.086 = 30.193
  7.389 / 30.193 = 0.245
  2.718 / 30.193 = 0.090
  20.086 / 30.193 = 0.665
```

Two times in three this reply stops here; one time in three it carries on. Nothing about that
is a special case — it is the softmax of Chapter 8 over a vocabulary that happens to contain an
entry meaning *stop*. And at temperature zero it would stop every time, which is one reason a
greedy reply and a sampled reply from the same prompt can be very different lengths.

**You set a maximum.** Every API takes a limit on how many tokens may be generated. Hitting it
truncates the reply mid-sentence, which is a different outcome from finishing, and your code
should be able to tell them apart — the response says which happened.

**You supply a stop condition.** A **stop condition** — providers call it a stop sequence, and
it is not Chapter 4's stopping condition — is a string you nominate; when the generated text
contains it, generation halts and the string is normally not returned. Useful
when you have asked for one item of a list and do not want four.

> **Note:** Two more things end a reply outside the ordinary case, and neither is in the list
> above. The input can simply fill up, which Chapter 16 is about. And your own code can cancel
> the request part-way, which Chapter 19 covers. If you are writing the code that handles a
> reply, those are two more outcomes to tell apart.

> **Warning:** The maximum is a guillotine, not a budget. A model asked for a long answer with a
> short maximum does not write a shorter answer — it writes the same long answer and has it cut
> off. If you want brevity, ask for brevity in the instructions and set the maximum as a safety
> net above what you expect, not at it.

## Why Temperature Zero Is Still Not a Guarantee

Now the opening problem, and it deserves a real answer rather than a shrug. Set temperature to
zero, get greedy decoding, take the biggest logit every time — and still get different text on
two identical calls. There is no randomness in that procedure. So where does the variation come
from?

**Four places that bite in practice, and none of them is the model being unpredictable.**

**Floating-point addition is not associative.** Adding a list of numbers in a different order
can give a slightly different answer, because each intermediate result is rounded to a fixed
number of digits. This is a property of the arithmetic hardware, not of models. A GPU splits a
long addition across thousands of units and then combines their partial sums, so the answer's
last digits depend on how the work was split — and nothing in your call fixes that split.

**Your request is batched with other people's.** Providers run many requests together for
efficiency. How many, and which ones, depends on who else is calling at that moment — and the
batch's shape changes how the arithmetic is grouped, which by the point above changes the last
digits. Chapter 15 is where batching is explained properly.

Those two combine into the case that is easiest to see. Suppose two logits are 6.0000001 and 6.0000000;
greedy takes the first. Change the last digit through a different summation order and greedy
takes the second — **a different token, and from there the reply may diverge entirely.** The difference is
not in the model, the prompt or the settings. It is a tie broken the other way.

**Some models route tokens to different parts of themselves.** In a model built with experts,
which part handles your token can depend on what else is in the batch, so your output can
depend on your neighbours. Chapter 15 explains what those experts are.

**And what runs underneath you can change.** Providers update models, sometimes without a new
name — and they also change the hardware and the libraries the same model runs on, which moves
the last digits without moving a single parameter. Chapter 54 is about pinning versions and
noticing when one moves.

> **Note:** Some providers offer a seed parameter and describe the result as *best effort*
> rather than guaranteed. That wording is accurate and worth taking literally: a seed fixes the
> random draw, and the sources above are not random draws.

**What to do about it, in one line each.** Do not write tests that assert on exact output
strings; assert on shape, on a property, or on a check. Log the output you actually got, so
"it changed" is a comparison and not a memory. And where the answer must be stable, stabilise
it in your code rather than hoping — a fixed format, a validator, a cache — rather than in the
model.

## Why One Good Output Proves Nothing

This chapter ends with the consequence, because it is the most expensive mistake in the
material so far.

You have seen a distribution with five entries, three of which have a real chance of being
drawn. One call samples one path through that distribution, at every token. The reply you got
is one draw from a very large space of replies your prompt could have produced, and the next
one will be a different draw.

So when you change a prompt, run it, and the output looks better: **you have one sample from
each of two distributions.** That is not evidence that the new prompt is better. It is not even
weak evidence, unless you know something about how much the output varies from call to call —
and you do not, because you ran it once.

This is the single most common error made by people who are otherwise doing everything right,
and it is why Chapter 20 exists: repeated runs, a measurement with an interval around it, and a
verdict you could defend. This half of the book is mechanism; Chapter 20 is where the book
turns to how you would know.

> **Tip:** The habit to build now, before Chapter 20 gives you the statistics: **run it five
> times before you believe it.** Five is not a number with a theory behind it. It is small
> enough to do every time and usually enough to show you the spread is there at all — and
> Chapter 20, which says how small a spread can be, is why *usually* is the honest word.

## Lab: Draw From a Distribution

Pen and paper for the first half, then about twenty lines of Python. Thirty minutes, and there
is a key for every step.

A vocabulary of four and one forward pass, with these logits:

```text
  token    logit
  yes        3
  no         1
  maybe      2
  .          0
```

**Step 1.** Compute the probabilities at `\(T = 1\)`{=latex}. The exponentials you need are
`\(e^0 = 1\)`{=latex}, `\(e^1 = 2.718\)`{=latex}, `\(e^2 = 7.389\)`{=latex} and
`\(e^3 = 20.086\)`{=latex}.

*Expected result:* total `\(20.086 + 2.718 + 7.389 + 1 = 31.193\)`{=latex}, and the
probabilities are yes 0.644, no 0.087, maybe 0.237, "." 0.032.

**Step 2.** Now `\(T = 0.5\)`{=latex}. What are the new logits, and without computing the
softmax, what will happen to "yes"?

*Expected result:* the logits double to `\((6, 2, 4, 0)\)`{=latex}, and "yes" goes up, because
halving the temperature doubles every gap and softmax exaggerates gaps. The order cannot change.
(For the record it becomes 0.865.)

**Step 3.** Which token does greedy decoding pick, and does it pick a different one at
`\(T = 0.5\)`{=latex}?

*Expected result:* "yes", both times. Greedy takes the largest logit, and dividing every logit
by the same positive number cannot change which is largest. **Temperature has no effect on
greedy decoding at all** — which is worth knowing before you spend an afternoon tuning it on a
call that is already greedy.

**Step 4.** Apply top-k with `\(k = 2\)`{=latex} to the `\(T = 1\)`{=latex} distribution.

*Expected result:* keep yes (0.644) and maybe (0.237), total 0.881. Renormalised,
`\(0.644 / 0.881 = 0.731\)`{=latex} and `\(0.237 / 0.881 = 0.269\)`{=latex}.

**Step 5.** Apply top-p with `\(p = 0.8\)`{=latex} to the same distribution. How many tokens
survive, and why is it not one?

*Expected result:* two. "yes" alone is 0.644, which is short of 0.8, so "maybe" is added and
the running total reaches 0.881. The rule is *the smallest set that reaches `\(p\)`{=latex}*,
so it overshoots — it is not allowed to stop below the threshold.

**Step 6.** In a new empty folder, save this as `sample.py` and run it:

```python
import math, random

vocab = ["yes", "no", "maybe", "."]
logits = [3, 1, 2, 0]

def probs(logits, T):
    scaled = [z / T for z in logits]
    total = sum(math.exp(z) for z in scaled)
    return [math.exp(z) / total for z in scaled]

random.seed(13)
for T in (0.5, 1.0, 2.0):
    p = probs(logits, T)
    draws = random.choices(vocab, weights=p, k=1000)
    counts = {w: draws.count(w) for w in vocab}
    print(f"T={T}  p={[round(x, 3) for x in p]}")
    print(f"      counts {counts}")
```

*Expected result:* exactly this, because the seed is fixed.

```text
T=0.5  p=[0.865, 0.016, 0.117, 0.002]
      counts {'yes': 873, 'no': 17, 'maybe': 108, '.': 2}
T=1.0  p=[0.644, 0.087, 0.237, 0.032]
      counts {'yes': 629, 'no': 96, 'maybe': 241, '.': 34}
T=2.0  p=[0.455, 0.167, 0.276, 0.102]
      counts {'yes': 467, 'no': 153, 'maybe': 271, '.': 109}
```

The counts track the probabilities, which is the only thing a probability means. At
`\(T = 2\)`{=latex} the full stop came up 109 times in a thousand; at
`\(T = 0.5\)`{=latex} it came up twice.

**Step 7.** Change the seed to any other number and run it again. What stays the same and what
moves?

*Expected result:* the probabilities are identical, because they do not depend on the seed. The
counts all move, most of them by tens. **That is what one sample looks like against a
thousand**, and you
have just watched a thousand of them to see the shape — which is exactly the evidence you do
*not* have when you change a prompt, run it once, and like the answer.

**Step 8.** No arithmetic. You ask for a single JSON object, set the maximum to 50 tokens and
supply the stop condition `\n\n`. Name the four different ways that call can come back, and
say how your code tells them apart.

*Expected result:* (1) the model samples its stop token, and the reply is complete; (2) the
maximum is reached at 50 tokens and the JSON is cut off mid-string; (3) the model emits a blank
line, the stop condition matches, and generation halts wherever it happened to be; (4) your own
code cancels or times out first. The response says which of the first three happened — every
API reports a reason for finishing — and **that field is the thing to log**, because cases 2
and 3 both produce text that looks like an answer and is not one. Note what this means for the
maximum: at 50 tokens you have not asked for a shorter object, you have arranged for a broken
one.

**Step 9.** A colleague says their feature is deterministic because they set temperature to
zero. Name two reasons that may not hold.

*Expected result:* any two of: floating-point addition is not associative, so a different
summation order on the GPU changes the last digits and can flip which of two near-equal logits
is largest; their request is batched with others, and the batch's composition changes that
order; a model with experts may route their token differently depending on the batch; and the
provider may have changed the model, or the hardware and libraries it runs on.

## Summary, Key Terms, and Review Questions

### Summary

The raw scores coming out of the final matrix multiplication are the **logits**, one per
vocabulary entry, and only their differences matter. **Greedy decoding** takes the largest and
is what temperature zero does in practice; it is locally greedy, so it is not guaranteed to produce the most
likely sentence, and it makes models repeat themselves. **Temperature** divides the logits
before softmax — below 1 it sharpens the distribution, above 1 it flattens it, and it never
changes the order, so it has no effect at all on greedy decoding. **Top-k** keeps a fixed number
of tokens and **top-p** keeps the smallest set whose probabilities reach `\(p\)`{=latex}, both
renormalising what survives; top-p adapts to how confident the model is and top-k does not. In the
ordinary case a reply ends when the model samples a **stop token** — an ordinary vocabulary
entry meaning *finished* — or when your maximum truncates it, or when a **stop condition** you
supplied is matched; outside it, the input can fill up or your code can cancel.
**Temperature zero is not a guarantee**: floating-point addition is not associative, batching
changes the summation order, expert routing can depend on your neighbours, and what the
provider runs underneath you can change. Some of those move the last digits of a score, which
flips a near-tie; others change the computation outright. Where a near-tie does flip, the reply
may diverge from that token on; where none is close enough, the greedy path is identical. And because one call
is one draw, **one good output is not evidence**, which is the problem Chapter 20 solves.

### Key Terms

| Term | Meaning |
|---|---|
| **Logits** | The raw scores from the final matrix multiplication, one per vocabulary entry, before softmax. Can be negative; only the differences between them matter |
| **Greedy decoding** | Always taking the highest-scoring token. What "temperature zero" does in practice, since dividing by zero is not defined |
| **Temperature** | A number the logits are divided by before softmax. Below 1 sharpens the distribution, above 1 flattens it, and it never changes the order |
| **Top-k** | Keeping only the `\(k\)`{=latex} highest-scoring tokens and renormalising. Keeps the same number of options however confident the model is |
| **Top-p** | Also called nucleus sampling. Keeping the smallest set of tokens whose probabilities add to at least `\(p\)`{=latex}, then renormalising. Narrow where the model is confident, wide where it is not, at the cost of not knowing in advance how many survive |
| **Stop token** | An entry in the vocabulary meaning *finished*, scored and sampled like any other token. Often called an end-of-sequence token. A model stops talking by predicting that it has stopped |
| **Stop condition** | A string you nominate that halts generation when it appears. Providers call it a stop sequence; it is not Chapter 4's stopping condition. One of the ordinary ways a reply ends, alongside the model's own stop token and your maximum |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Temperature | `\(p_i = \exp(z_i/T) / \sum_j \exp(z_j/T)\)`{=latex} |
| What temperature does | Below 1 sharpens, above 1 flattens, never reorders |
| Temperature and greedy | No effect whatsoever — greedy takes the largest logit either way |
| Top-p against top-k | Top-p keeps the smallest set reaching `\(p\)`{=latex}; top-k keeps a fixed count |
| The order of operations | Temperature, then the cut, then draw |
| Why `\(T=0\)`{=latex} is not a guarantee | Float order, batching, expert routing, provider change |

### Review Questions

1. What does temperature do to the numbers?
2. Why is temperature zero still not a guarantee of the same output twice?
3. Your call is set to greedy decoding and a colleague suggests lowering the temperature to make it more reliable. What do you say?
4. When would you prefer top-p to top-k, and why?
5. Name the ordinary ways a reply can end, say which one is the model's doing, and name one way that is not on that list.
6. You change a prompt, run it once, and the answer is better. What have you learned?

### Review Answers

1. It divides every logit by `\(T\)`{=latex} before softmax. Because softmax exaggerates gaps
and dividing the logits divides the gaps, a temperature below 1 sharpens the distribution
towards the top token and a temperature above 1 flattens it towards the rest. In the chapter's
example the top token goes from 0.636 at `\(T = 1\)`{=latex} to 0.865 at
`\(T = 0.5\)`{=latex} and down to 0.429 at `\(T = 2\)`{=latex}. It never changes the order,
because dividing every logit by the same positive number cannot reorder them — so it changes
how much of the rest is in play, not what the model thinks is most likely.
2. Because temperature zero is greedy decoding, and the thing greedy depends on — which logit
is largest — can change for reasons that have nothing to do with the model. Floating-point
addition is not associative, so a different summation order gives different last digits; a GPU
splits a long addition across many units and combines their partial sums, and how it splits
depends on what else was in your batch. Two
logits a hair apart can swap, greedy takes the other token, and from there the reply may diverge.
Models with expert routing can also depend on batch composition, and the provider may have
changed the model, or the hardware and libraries it runs on. Nothing there is randomness in the
usual sense, which is why a seed does not fix it.
3. That temperature has no effect on greedy decoding at all. Greedy takes the largest logit, and
dividing every logit by the same positive number cannot change which is largest — so the dial
they are reaching for is already disconnected. If the output is varying anyway, the cause is one
of the four in this chapter, and the fix is in their code: assert on shape rather than on
strings, log what came back, and stabilise with a validator or a cache rather than a setting.
4. When the model's confidence varies across the generation, which it usually does. Top-k keeps
the same number of options whether the model is certain or not — so it leaves thirty-nine bad
options in play when one token is at 0.98, and cuts away good ones when a hundred tokens are
near-equal. Top-p keeps however many it takes to cover the mass, so it is narrow where the model
is sure and wide where it is not. The cost is that the number of options is no longer something
you can state in advance.
5. The model samples a stop token — an ordinary entry in the vocabulary meaning *finished*,
chosen by the same procedure as any other token, and the only one of the ordinary three that is
the model's doing. Your maximum truncates the reply, which is a cut rather than an ending and
reports itself differently. And a stop condition you nominated is matched in the generated
text. Off that list: the input can fill up, and your own code can cancel the request.
6. Almost nothing. You have one sample from each of two distributions, and you have no idea how
much either varies from call to call, because you drew once from each. The output you liked may
be an ordinary result of the new prompt or an unusually good one, and nothing distinguishes
those from where you are standing. Run it several times before believing it, and Chapter 20 is
where that becomes a measurement with an interval around it.

> **You understand this when** you can explain to a colleague why their temperature-zero
> pipeline is not reproducible, without using the word "random".
