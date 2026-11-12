# What It Costs From the Inside

Chapter 1 told you the wait has two phases and that you feel them differently. This chapter
says why, and the answer turns out to explain most of the cost of running these systems: why
the first token is slow, why memory rather than arithmetic is usually the binding constraint,
why your request is run alongside strangers', and why a model with a hundred billion
parameters can be cheaper per token than one with fifty.

*The problem.* My first token takes two seconds and the rest arrive in a stream. Nobody has
told me why.

*The question.* What is the machine actually doing during each of those two waits, what does
it have to keep in memory while it does, and which of those things is the one that costs?

## Two Different Computations

The two phases are not the same work at different speeds. They are different work.

**Prefill** is what happens to your input. The whole prompt is there at once, so every
position can be computed at the same time: the embedding lookups, the attention grids, the
feed-forward blocks, all of it, for all `\(n\)`{=latex} tokens together. One pass through the
stack handles the lot.

**Decode** is what produces the reply, and it is Chapter 9's loop: one forward pass per token,
each pass producing one distribution, each token appended before the next pass runs.

| | Prefill | Decode |
|---|---|---|
| Handles | The whole prompt at once | One token at a time |
| Passes through the stack | One | One per output token |
| Positions computed per pass | All of them | One |
| What limits it | Arithmetic | Memory traffic — see below |
| What you feel | The wait before the first word | The pace of the words after it |

**And that last row is the thing to understand**, because it is where the surprise lives. The
two phases are limited by different resources, which is why they behave so differently when
you change things.

## Why the First Token Is Slow

Prefill has to do all the work for every position in your prompt before a single token can be
produced. Chapter 11 counted it: building the attention grid is about `\(n^2 d\)`{=latex}
operations per layer, and the feed-forward blocks add their own work at every position.

So the wait before the first word grows with the prompt. Send twice as much and prefill does
more than twice the work, for the reason Chapter 11 gave — the grid is square in
`\(n\)`{=latex}.

That wait has a name: **time to first token**, shortened to TTFT[]{idx="TTFT"}, which is what you will see
on a dashboard and hear in an interview. The pace of the words after it is **time per token**.
This chapter is why they are two different numbers; measuring them on your own system is
Chapter 52.

Then decode starts, and each token takes roughly the same time as the one before it —
roughly, and two sections below says what makes it drift. The
arithmetic for one new token is tiny by comparison: one position, not `\(n\)`{=latex} of them.

**But decode is not fast because it is doing less arithmetic.** It is doing almost no
arithmetic, and it is still not instant, and the reason is the one thing a beginner never
guesses: **to compute one token, every parameter the pass uses has to be read out of memory.**
Chapter 12 counted them — about five billion in the layers of a modest model. Reading five
billion numbers takes time whatever you do with them, and for one token you do almost nothing
with them.

Put the two side by side for one decode token of a seven-billion-parameter model at two bytes
each. Each parameter the pass uses is used once, in a multiply and an add:

```text
  bytes read     7,000,000,000 x 2  =  14,000,000,000
  operations     7,000,000,000 x 2  =  14,000,000,000

  one operation per byte read
```

**One operation per byte**, on hardware designed to do hundreds of operations for every byte
it fetches. The arithmetic unit is idle almost all the time, waiting. A step with that shape is
called **memory-bound**, as against **compute-bound** when the arithmetic is the thing you are
waiting on — and decode is the most memory-bound step in this book. Prefill is the opposite:
the same single read of the parameters serves every position in the prompt at once, so the
operations multiply by `\(n\)`{=latex} while the bytes do not.

That is why decode is described as limited by memory traffic rather than by arithmetic. The
processor is waiting for numbers to arrive. It is also why the next two sections matter more
than anything about raw speed.

> **Note:** This is the mechanism behind every "it is slow" conversation you will have about
> these systems, and the two halves have different cures. A long *prompt* makes prefill slow,
> and the cure is to send less. A long *reply* makes decode slow, and the cure is to ask for
> less. Chapter 52 is where the levers are; this chapter is why they exist.

## The Key–Value Cache

Chapter 11 left a problem on the table. Each decode pass runs attention over the whole
sequence so far — but all of it except the newest token is unchanged from last time, so
recomputing the keys and values for every earlier position on every pass is pure waste.

The fix is to keep them. The **key–value cache** holds the key and value vector for every
position, in every layer, for the whole sequence so far. Prefill writes it for the whole
prompt at once; then on each decode pass the model computes
`\(k\)`{=latex} and `\(v\)`{=latex} for the one new position, appends them, and attends against
the lot.

That turns the work per decode token from "recompute everything" into "compute one position and
read the rest", which is the difference between a system that works and one that does not.

In writing and in speech the key–value cache is the **KV cache**, and that is how an
interviewer will ask about it.

**And it is also the memory bill.** Here is the calculation, and it is worth being able to do
it from memory, because it is the one that decides how many users fit on a machine.

For each token you store a key and a value — that is the 2 — in every layer, each of width
`\(d\)`{=latex}, at some number of bytes per number:

```{=latex}
\[ \text{cache} = 2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes} \]
```

Put the shape of Chapter 12's worked model in it: 32 layers, width 4,096, two bytes per number.

```text
  per token   2 x 32 x 4,096 x 2  =  524,288 bytes  =  512 KiB
```

**Half a mebibyte per token.** Now multiply by a conversation:

```text
   1,000 tokens      524,288,000 bytes    0.49 GiB
   8,000 tokens    4,194,304,000 bytes    3.91 GiB
  32,000 tokens   16,777,216,000 bytes   15.63 GiB
```

> **Note:** Two units, and the difference has embarrassed a lot of people at the moment a model
> did not fit. A **GiB** is 1,024³ bytes and a **GB** is 1,000³, about 7 per cent smaller. A
> card sold as "40GB" holds 40 GiB; a model quoted at 14 GB holds 14 thousand million bytes,
> which is 13.0 GiB. This chapter quotes memory in GiB and model sizes in GB, because that is
> how each is sold.

And then by the number of people talking to it at once:

```text
  ten users at 8,000 tokens each  =  39.1 GiB
```

That is on top of the model's own parameters, on a card with a fixed amount of memory. **The
cache, not the model, is usually what decides how many conversations fit.** A model that takes
13 GiB of weights and leaves 27 GiB free on a 40 GiB card can serve six of those
conversations at once, which is
far fewer than the weights alone would suggest.

> **Note:** Notice what the cache does *not* depend on: how hard the question is, or how
> good the answer is. It depends on the number of tokens and nothing else. A user who pastes a
> long document into a chat and then asks three short questions is occupying that memory for the
> whole conversation. This is the mechanism behind every limit you have ever met on how much you
> may send.

> **Note:** Real systems shave this figure. Several heads can be made to share one set of keys
> and values, which divides the figure by the number of heads sharing; the cache can be stored
> at fewer bytes per number than the weights; and it can be held in pages rather than one block
> so the space is not wasted. The arithmetic above is the shape, and the shape is what you
> reason with.

## Why Doubling the Prompt More Than Doubles the Work

Three things grow when your prompt gets longer, and they grow at different rates. Putting them
side by side is the clearest way to see why "it is just a bit more text" is wrong.

```text
  what grows            how
  -------------------------------------------
  prefill, the rest     with n
  prefill, attention    with n squared
  cache memory          with n
  decode, per token     with n, in cache reads
```

And the first two deserve numbers, because "with n squared" is the half everybody quotes and
the smaller half for most prompts. Multiply-adds in one layer, at Chapter 12's shape:

```text
  tokens      the rest        attention       attention's
                                                 share
   1,000   157,286,400,000     8,192,000,000       5%
   2,000   314,572,800,000    32,768,000,000       9%
  19,200 3,019,898,880,000 3,019,898,880,000      50%
  32,000 5,033,164,800,000 8,388,608,000,000      62%
```

So at a thousand tokens the squared term is one part in twenty, and doubling the prompt
multiplies prefill by 2.1 rather than by 4. The two halves are equal at 19,200 tokens, and
only past that does the squared term run the show. **"Prefill is quadratic" is true of
attention and not of prefill**, until the prompt is long — and knowing where "long" starts is
the difference between an answer and a slogan.

The first is Chapter 11's grid. The second is the section above. **The third is the one people
miss**: every decode pass attends over the whole cache, so as the conversation gets longer
each new token costs more to produce than the last. A reply that starts fast gets slower.

So doubling the prompt more than doubles the prefill arithmetic — the attention part of it
quadruples, and that part is a minority until the prompt is long — doubles the memory you are
holding, and makes every token of the reply more expensive. None of those is "a bit more text".

> **Tip:** This is the honest answer to "why can't I just put everything in the prompt". Not
> "because the model gets confused" — that is Chapter 16's separate and also-true point — but
> because three different costs rise at once and one of them faster than proportionally, and somebody is paying
> for it.

## Batching: Your Request Runs With Others

Decode is limited by reading the parameters out of memory. Read them once and you can compute
one token. Read them once and you could just as easily compute a token for *fifty* different
conversations, because the expensive part — getting the numbers — has already happened.

That is **batching**, and it is why providers do it. One read of the parameters serves every
request in the batch, so the cost per request falls — but by how much depends entirely on how
much cache each request is also reading, and that is worth doing rather than guessing. With
short conversations the cache is almost nothing beside the 13 GiB of weights, and a batch of
fifty really does approach a fiftyfold saving: at 100 tokens each it is about forty-two times.
At the 8,000 tokens the next paragraph picks, it is about *four*.

**But only the read of the parameters is shared, and nothing else is.** Every request in the
batch has its own cache to read and its own arithmetic to do, so the saving flattens as the
batch grows. At 8,000 tokens each — on a machine large enough to hold them, which the lab's is
not — fifty conversations read fifty lots of 3.91 GiB of cache against one shared 13 GiB of
weights — the unshared reads have already overtaken the thing
being shared. And past some batch size the machine runs out of arithmetic rather than memory
traffic — it becomes compute-bound — and every token gets slower. That is the answer to
*then why not batch ten thousand*,
and it is the sentence to have ready when somebody asks.

Three consequences, and all three show up in your work.

**It is why the price per token is what it is.** You are not paying for a machine to yourself.
You are paying a share of a machine that is serving many people at once, and the published
price reflects that. Chapter 53 is what to do about the bill that results.

**It is one of the reasons Chapter 13's temperature-zero problem exists.** The batch's shape
changes how the arithmetic is grouped, and a different grouping changes the last digits, and a
near-tie between two logits can flip. Your output can depend on who else was calling at that
moment. Chapter 13 gave the consequence; this is the mechanism behind two of its four causes.

**And it is why your own latency is not entirely yours.** If the system is busy, your request
waits to join a batch. If it is quiet, it may run in a small batch and finish sooner.

> **Note:** Serving systems do not fill a batch and then run it to completion. They add and
> remove requests as they arrive and finish, so the batch is a moving population — which is a
> serving technique in its own right and belongs to Chapter 52. What matters here is the
> mechanism underneath it: the parameters are read once and shared.

## Quantisation: Bits Per Parameter

If decode is limited by reading parameters, then making each parameter *smaller* makes decode
faster. That is **quantisation**: storing each number in fewer bits.

The arithmetic is as simple as it looks. For a model with seven billion parameters:

```text
  16 bits   2 bytes each    14.0 GB
   8 bits   1 byte each      7.0 GB
   4 bits   half a byte      3.5 GB
```

Halve the bits, halve the memory, and roughly halve the time spent reading. It is the single
biggest lever on the size of machine a model needs, which is why a model that will not fit on
a card at 16 bits will often fit comfortably at 4.

**What it costs you is precision.** Each number is stored less exactly, and the outputs change
— usually a little, sometimes in ways that matter for a particular task. What practitioners
report is that the effect is small at 8 bits and usually acceptable at 4: a practitioner report
on Chapter 6's ladder rather than anything this chapter measures, and that *usually* is doing
real work in the sentence. It is a thing to measure on your own task rather than to assume, and
Chapter 20 is how you would measure it.

> **Note:** Quantisation applies to the weights, and separately to the cache from two sections
> ago — the two are chosen independently, and halving the cache's bits halves that 512 KiB per
> token as well. Where a published figure says "a 7B model in 4 GB", it is counting weights.

## Mixture of Experts

The last piece, and it is the one that makes model sizes confusing to compare.

Chapter 12 showed that most of a layer's parameters are in the feed-forward block. A
**mixture-of-experts** model replaces that one block with several — say eight — and adds a
small piece of arithmetic that chooses which two of the eight each token goes through. The
abbreviation is MoE[]{idx="MoE"}.

So the model *holds* eight feed-forward blocks per layer and *uses* two. Take Chapter 12's
numbers, with attention at 67,108,864 parameters and one feed-forward block at 90,177,536:

```text
  total     67,108,864 + 8 x 90,177,536  =  788,529,152
  active    67,108,864 + 2 x 90,177,536  =  247,463,936

  active share  247,463,936 / 788,529,152  =  0.314
```

**Under a third of the parameters run for any given token.** This is what the terms *total
parameters* and **active parameters** mean, and why a model advertised at a very large number
can be cheap per token: the number in the name is the first figure and the cost follows the
second.

What it does not make cheap is memory. All eight blocks have to be *there*, because the next
token may route differently — and in a batch they are all needed anyway, because a batch's
tokens between them route almost everywhere. The saving on reading the parameters is real at
one request and shrinks as the batch fills, which is why serving these models well is harder
than the active-parameter figure makes it sound. So this design trades memory — which you
can buy — for arithmetic
and memory traffic, which is what you are waiting on.

> **Note:** Eight experts with two active is one arrangement among many, and a dated detail:
> designs routing two of eight sit at the modest end, and some route eight of two hundred and
> fifty-six, which puts the active share near a thirtieth rather than near a third. The
> arithmetic is the same; the fraction is not.

> **Note:** Which experts a token goes through can depend on what else is in the batch, because
> the routing balances load across experts. That is the third of Chapter 13's four causes of
> non-determinism, and now you can see where it comes from.

## Lab: Size a Machine

Pen, paper and a calculator. Twenty minutes, and there is a key for every step. Nothing to
install.

You are sizing a machine to serve one model. Its shape: **32 layers, width 4,096, 7 billion
parameters, weights at 16 bits.** That is more than Chapter 12 counted for the same shape,
because this model's feed-forward blocks are the gated three-matrix form Chapter 12's Note on
real feed-forward blocks mentions — three matrices of 4,096 by 11,008 instead of two comes
to 7.0 billion. The card has [**40 GiB**]{.noindex} of memory. Your product allows
conversations up to [**8,000 tokens**]{.noindex}, and the cache is stored at 2 bytes per number.

**Step 1.** How much memory do the weights take?

*Expected result:* `\(7{,}000{,}000{,}000 \times 2 = 14{,}000{,}000{,}000\)`{=latex} bytes —
14.0 GB, which is 13.0 GiB — the two units from the Note earlier in the chapter, and the
reason this step is worth doing rather than skipping.

**Step 2.** How much cache does one 8,000-token conversation need?

*Expected result:* `\(2 \times 32 \times 4{,}096 \times 2 = 524{,}288\)`{=latex} bytes per
token, and `\(524{,}288 \times 8{,}000 = 4{,}194{,}304{,}000\)`{=latex} bytes — **3.91 GiB.**

**Step 3.** How many such conversations fit at once?

*Expected result:* 40 − 13.0 = 27.0 GiB free, and `\(27.0 / 3.91 = 6.9\)`{=latex}, so **six**.
Not 6.9 — you cannot serve nine tenths of a conversation, and in practice you would leave
headroom and say five.

**Step 4.** Your product manager wants to allow 32,000-token conversations instead. How many
fit now, and what would you say?

*Expected result:* the cache per conversation becomes
`\(524{,}288 \times 32{,}000 = 16{,}777{,}216{,}000\)`{=latex} bytes, 15.63 GiB, so
`\(27.0 / 15.63 = 1.7\)`{=latex} — **one.** Quadrupling the allowed length cut capacity from
six to one, which is a sixfold increase in the cost per conversation for a feature most users
will not use. That is the conversation to have, and the arithmetic is the whole of your side
of it.

**Step 5.** Someone suggests 4-bit weights. How much does that free, and how many 8,000-token
conversations fit then?

*Expected result:* the weights drop to
`\(7{,}000{,}000{,}000 \times 0.5 = 3{,}500{,}000{,}000\)`{=latex} bytes — 3.5 GB, 3.3 GiB.
Free memory rises from 27.0 to 36.7 GiB, and `\(36.7 / 3.91 = 9.4\)`{=latex}, so **nine**
conversations rather than six. Then the part that is not arithmetic: you would have to measure
whether the 4-bit model is still good enough at your task, because nothing above tells you
that.

**Step 6.** The cache is also stored at 4 bits instead of 16. What happens?

*Expected result:* the per-token figure falls from 524,288 bytes to a quarter of that,
131,072 bytes, so an 8,000-token conversation needs 0.98 GiB. With 4-bit weights too, 36.7
GiB free gives **thirty-seven** conversations. **The cache was the binding constraint all
along** — and that is the point of the whole lab. Most people reach for the weights first,
because that is the number in the model's name.

**Step 7.** Without computing: your traffic doubles overnight and every conversation is the
same length. What happens to the arithmetic the machine does per token, and what happens to
the memory it needs?

*Expected result:* the arithmetic per token barely changes, because the parameters are read
once for the whole batch and twice as many requests share that one read. The memory roughly
doubles, because every conversation needs its own cache. **Doubling the load is a memory
problem, not an arithmetic one**, which is the opposite of most people's intuition and follows
directly from the first two sections.

## Summary, Key Terms, and Review Questions

### Summary

The two waits are two different computations. **Prefill** handles the whole prompt in one pass,
with every position computed together, and is limited by arithmetic — whose attention part
grows with `\(n^2\)`{=latex}, so a longer prompt makes the first token slower than
proportionally.
**Decode** is one pass per output token, does almost no arithmetic, and is limited by having to
read every parameter it uses out of memory for each token. The **key–value cache** stores each
position's key and value in every layer so decode does not recompute them, at a cost of
`\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} — 512
KiB per
token at a common shape, so 3.91 GiB for an 8,000-token conversation and 39 GiB
for ten of them. That cache, not the weights, usually decides how many conversations fit.
**Batching** works because the parameters are read once and shared across many requests, which
is why the price per token is what it is and why your output can depend on who else was
calling. **Quantisation** stores each parameter in fewer bits, halving memory and read time
each time the bits halve, at a cost in precision you have to measure. And a
**mixture-of-experts** model holds many feed-forward blocks and runs a few, so its **active
parameters** are a fraction of its total — under a third in the worked example — which is why
a very large model can be cheap per token while still needing all of that memory.

### Key Terms

| Term | Meaning |
|---|---|
| **Prefill** | The pass that processes the whole prompt, every position at once. Limited by arithmetic, whose attention part grows with the square of the prompt length and overtakes the rest on a long one. What you wait for before the first word |
| **Decode** | One forward pass per output token. Does almost no arithmetic and is limited by reading every parameter the pass uses out of memory once per token |
| **Key–value cache (KV cache)** | The stored keys and values for every position in every layer, so decode attends to earlier positions without recomputing them. Costs `\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} |
| **Compute-bound** | A step whose speed is set by the arithmetic it has to do rather than by how fast its numbers arrive. Prefill is; a large enough batch becomes so |
| **Memory-bound** | A step whose speed is set by how fast numbers arrive from memory rather than by the arithmetic done with them. At two bytes per parameter, decode does about one operation for every byte it reads, on hardware built for hundreds |
| **Batching** | Running many requests through the same forward pass, so one read of the parameters serves all of them. Close to free up to a point — each request still reads its own cache and does its own arithmetic — which is why the price per token is low and why your neighbours affect your output |
| **Quantisation** | Storing each parameter in fewer bits. Halving the bits halves the memory and roughly halves the time spent reading, at a cost in precision that has to be measured |
| **Mixture of experts (MoE)** | Replacing one feed-forward block per layer with several and routing each token through a few of them. The model holds all of them and runs some |
| **Active parameters** | The parameters that actually run for a given token, as against the total the model holds. Cost follows the active figure; the name usually quotes the total |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Key–value cache | `\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} |
| At a common shape | 32 layers, `\(d\)`{=latex} 4,096, 2 bytes: 512 KiB per token |
| An 8,000-token conversation | 3.91 GiB of cache, on top of the weights |
| Weights at 7 billion parameters | 14 GB at 16 bits, 7 GB at 8, 3.5 GB at 4 |
| What limits each phase | Prefill: arithmetic. Decode: reading the parameters the pass uses |
| What batching shares, and what it does not | The parameters are read once and shared; each request's own cache is not. So the saving is large at short contexts and small at long ones — about 4x at 8,000 tokens each |

### Review Questions

1. Why is the first token slow and every token after it fast?
2. Your prompt doubles in length. Why does the work more than double?
3. What is the key–value cache, and how big is it?
4. Why do providers run your request alongside other people's, and what does that do to you?
5. A model is advertised with a very large parameter count but a low price per token. How is
that possible?
6. You need to serve more conversations on the same card. Name two levers, say which one
people reach for first, and name a third that is not about bits at all.

### Review Answers

1. Because they are different computations. The first token requires prefill: the whole prompt
processed in one pass, every position at once, with attention's grid growing as the square of
the prompt length — so the wait before the first word grows faster than the prompt does, and
faster still once that part dominates. Every
token after it is one decode pass over a single new position, which is almost no arithmetic.
Decode is not instant either, but what limits it is reading out of memory every parameter the
pass uses, once per token, not the arithmetic it then does.
2. Three things grow and none of them grows linearly in the way people expect. Prefill's
attention arithmetic grows with the square of the length, so it roughly quadruples. The
key–value cache grows with the length, so the memory you are holding doubles. And every decode
pass attends over the whole cache, so each token of the reply costs more to produce than it
did — a reply that starts fast gets slower. "A bit more text" is three costs rising at once,
one of them faster than proportionally.
3. The stored key and value vectors for every position in every layer, kept so that decode does
not recompute them on every pass. Its size is `\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} — at 32 layers, a width of 4,096 and two bytes,
that is 512 KiB per token, so 3.91 GiB for an 8,000-token conversation and about 39 GiB for ten
of them. It depends on nothing but the number of tokens, and it is usually what decides how
many conversations fit on a card rather than the weights.
4. Because decode is limited by reading the parameters out of memory, and that read serves the
whole batch at once — so fifty requests cost far less than fifty, and the price per token
reflects a shared machine. Only that read is shared, though: each request still reads its own
cache and does its own arithmetic, so the saving flattens as the batch grows and eventually
the machine becomes compute-bound instead. What it does to you: your request may wait to
join a batch, so your
latency depends on how busy the system is; and the batch's composition changes how the
arithmetic is grouped, which changes the last digits of the scores and can flip a near-tie —
which is why temperature zero is not a guarantee.
5. Because it is a mixture-of-experts model, and the number in the name is the total rather
than the active parameters. Each layer holds many feed-forward blocks and routes each token
through a few, so the arithmetic and the memory traffic per token follow the smaller figure —
under a third of the total in this chapter's example. What it does not make cheap is memory:
every block has to be there, because the next token may route differently.
6. Quantisation and the cache. Quantisation is what people reach for first, because the weights
are the number in the model's name — and in this chapter's lab it took capacity from six
conversations to nine. The cache is the bigger lever and the less obvious one: storing it at
fewer bits as well took the same machine from nine to thirty-seven, because at a long
conversation length the cache, not the weights, was the binding constraint. And the third lever
is not about bits: shortening the conversations you allow. Step 4 priced it — going from 8,000
tokens to 32,000 took the same machine from six conversations to one.

> **You understand this when** you can work out how many conversations fit on a card, and say
> which of the weights and the cache is the one actually stopping you.
