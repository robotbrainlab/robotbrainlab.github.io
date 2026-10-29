# Adapting a Model: Prompt, Retrieve or Tune

Chapter 14 said what the three training stages do, and ended with a Warning pointed here: "we'll
do some fine-tuning on our docs" is the most common wrong first answer in this field, and this is
the chapter about when it is genuinely right and what it costs you. Chapters 24 to 29 built the
other lever in full. Chapters 30 to 33 and 38 built the thing that decides between them.

So this chapter is mostly about a choice, and the choice has an order. The one piece of
machinery it does add is the arithmetic of a low-rank adapter, because you cannot judge what
tuning costs without it.

*The problem.* People keep asking whether I fine-tuned it. I don't know how to answer, or when I
should.

*The question.* Which lever does a given ask actually need, and what do you take on by reaching
for the last one?

## Three Levers, and What Each One Can Reach

There are three places to put what the model does not currently do: the request itself, the
documents you retrieve into it, and the model's own parameters. This chapter calls the third one
*tuning*, and what it means is running Chapter 14's second or third stage on data of your own.
The field's verb for it is to **fine-tune**, and its word for the result is a *fine-tuned* model
— the phrasing an interviewer will use, and the phrasing of the question this chapter exists to
answer. Chapter 14 owns what those stages do; this chapter owns when you would run one.

Chapter 14's last section already decided most cases between the three. Knowledge is overwhelmingly a pretraining
phenomenon; what a later stage is good at is shaping *how* the model responds rather than *what
it knows*; and no stage gives the model a way to look anything up.

Put twelve real asks through that.

```python
"""Twelve things people ask for, sorted by what each one actually needs.

NEEDS says what the ask requires that the model does not already have:
"facts" is information it has never seen and something you own
holds, "behaviour" is how it responds to what it has, "neither" is
a job for code or a tool. A per-customer plan counts as the first:
chapter 2 says a single database query that puts a row into the
context is retrieval, because the part is defined by where it sits.
PROMPT says whether an instruction in the request reaches it.

The point of the table is the count at the bottom, not any one row.
"""

#  what is asked for                      needs        prompt  changes
ASKS = [
    ("answer from our policy handbook",    "facts",     False,  False),
    ("know last month's releases",         "facts",     False,  True),
    ("know who is on which plan",          "facts",     False,  True),
    ("quote the right contract clause",    "facts",     False,  True),
    ("stop opening with 'Certainly!'",     "behaviour", True,   False),
    ("answer in the question's language",  "behaviour", True,   False),
    ("return JSON matching a schema",      "behaviour", True,   False),
    ("follow the 12-step refund rule",     "behaviour", True,   False),
    ("write in our terse house register",  "behaviour", False,  False),
    ("sort tickets into 40 categories",    "behaviour", False,  False),
    ("be better at arithmetic",            "neither",   False,  False),
    ("add two numbers from an invoice",    "neither",   False,  False),
]


def lever(needs, prompt):
    """The cheapest lever that can reach the ask."""
    if needs == "neither":
        return "code or a tool"
    if needs == "facts":
        return "retrieval"
    return "the prompt" if prompt else "tuning, maybe"


if __name__ == "__main__":
    print(f"  {len(ASKS)} asks, sorted by what each one needs.\n")
    for ask, needs, prompt, _ in ASKS:
        print(f"    {ask:34s} {lever(needs, prompt)}")

    facts = [a for a in ASKS if a[1] == "facts"]
    beh = [a for a in ASKS if a[1] == "behaviour"]
    neither = [a for a in ASKS if a[1] == "neither"]
    by_prompt = [a for a in beh if a[2]]
    volatile = [a for a in facts if a[3]]
    left = [a for a in beh if not a[2]]

    print(f"\n    {len(facts)} need facts the model has not seen")
    print(f"    {len(beh)} are about behaviour, {len(by_prompt)} of them")
    print(f"      reached by an instruction in the request")
    print(f"    {len(neither)} are not a model's job at all")
    print(f"\n  So {len(left)} of the {len(ASKS)} are left where tuning is even a")
    print("  candidate, and 'maybe' is doing real work in that")
    print("  word - both of them have a prompt that works and is")
    print("  long, which is a cost question and not a capability")
    print("  one.\n")

    print(f"  Read the {len(facts)} facts rows again, because they are the")
    print("  ones people bring to fine-tuning. Chapter 14 settled")
    print("  what that stage sees: about one part in two hundred")
    print(f"  thousand of the tokens pretraining saw. And {len(volatile)} of those")
    print(f"  {len(facts)} are marked as changing, which decides them alone -")
    print("  a tuned model is as stale as the day its data was")
    print("  frozen, and retrieval reads the current row.\n")

    # The cost argument for tuning, which is the one people reach for.
    GUIDE = 900          # tokens of house-style instruction per call
    CALLS = 100_000
    EXAMPLES = 100_000   # curated examples for a tune
    PER_EXAMPLE = 500    # tokens each
    PASSES = 3           # times the tune reads the set

    prompt_tokens = GUIDE * CALLS
    tune_tokens = EXAMPLES * PER_EXAMPLE * PASSES
    print("  Now price the one argument that survives, on the")
    print("  house-register row. A style guide re-sent every call")
    print("  against a tune that reads a curated set three times:\n")
    print(f"    {GUIDE}-token guide x {CALLS:,} calls   "
          f"{prompt_tokens:,} tokens")
    print(f"    {EXAMPLES:,} examples x {PER_EXAMPLE} x {PASSES} passes "
          f"{tune_tokens:,} tokens")
    print(f"\n  The tune is {tune_tokens/prompt_tokens:.2f} times the prompt, before")
    print("  anyone serves the result. And the comparison is")
    print("  worse than that for tuning, because a fixed guide at")
    print("  the front of every request is the single most")
    print("  cacheable thing a request contains - chapter 52's")
    print("  subject - while the tune's tokens are spent once and")
    print("  again at every base-model change. The saving is real")
    print("  only where the guide is long, the volume is enormous")
    print("  and the prefix cannot be cached.")
```

```text
  12 asks, sorted by what each one needs.

    answer from our policy handbook    retrieval
    know last month's releases         retrieval
    know who is on which plan          retrieval
    quote the right contract clause    retrieval
    stop opening with 'Certainly!'     the prompt
    answer in the question's language  the prompt
    return JSON matching a schema      the prompt
    follow the 12-step refund rule     the prompt
    write in our terse house register  tuning, maybe
    sort tickets into 40 categories    tuning, maybe
    be better at arithmetic            code or a tool
    add two numbers from an invoice    code or a tool

    4 need facts the model has not seen
    6 are about behaviour, 4 of them
      reached by an instruction in the request
    2 are not a model's job at all

  So 2 of the 12 are left where tuning is even a
  candidate, and 'maybe' is doing real work in that
  word - both of them have a prompt that works and is
  long, which is a cost question and not a capability
  one.

  Read the 4 facts rows again, because they are the
  ones people bring to fine-tuning. Chapter 14 settled
  what that stage sees: about one part in two hundred
  thousand of the tokens pretraining saw. And 3 of those
  4 are marked as changing, which decides them alone -
  a tuned model is as stale as the day its data was
  frozen, and retrieval reads the current row.

  Now price the one argument that survives, on the
  house-register row. A style guide re-sent every call
  against a tune that reads a curated set three times:

    900-token guide x 100,000 calls   90,000,000 tokens
    100,000 examples x 500 x 3 passes 150,000,000 tokens

  The tune is 1.67 times the prompt, before
  anyone serves the result. And the comparison is
  worse than that for tuning, because a fixed guide at
  the front of every request is the single most
  cacheable thing a request contains - chapter 52's
  subject - while the tune's tokens are spent once and
  again at every base-model change. The saving is real
  only where the guide is long, the volume is enormous
  and the prefix cannot be cached.
```

**Read the lever column before the counts.** Four of the twelve need facts the model has never
seen and something you own holds, and Chapter 14 is careful about what settles those. Its ratio — the tuning stage sees about
one part in two hundred thousand of the tokens pretraining saw — bounds the *share* of a model's
knowledge that stage could account for, and Chapter 14 says in terms that it does [**not**]{.noindex} settle
whether tuning on a few thousand documents of your own installs their contents as recallable
facts: a small curated set is exactly the case where repeated exposure might help. What settles
that is weaker evidence, and Chapter 14 names it as such — practitioners report it does not work
reliably, which sits on Chapter 6's ladder rather than in any arithmetic. **What does settle three
of the four outright is staleness**: they are marked as changing, a tuned model is as old as the
day its data was frozen, and retrieval reads the current row.

Two of the twelve are not a model's job at all. Chapter 16 owns why arithmetic is hard for a
model, and the answer there is a tool rather than any amount of training.

**And one row of the facts group is worth a sentence, because it is the one people reclassify.**
Knowing which customer is on which plan is a live record lookup, not a search through documents,
and it is still the first group: Chapter 2 says in terms that a single database query putting a
row into the context *is* retrieval, and that the part is defined by where it sits rather than by
how clever it is. Which is the useful reading anyway — what rules a tune out there is not the
shape of the lookup, it is that the answer changes under you.

One more row deserves a note. *Return JSON matching a schema* is marked as reached by an
instruction, and that column asks only whether an instruction gets you there — which it largely
does. The lever an interviewer wants named is neither of this chapter's three: Chapters 21 and 22
own asking for a format, validating it, and the strict modes that enforce one during generation.
The row is here to rule tuning out, and it does.

**So two of the twelve are left where tuning is even a candidate**, and both of those have a
prompt that already works. That is the shape of the real decision: by the time you have ruled
out the facts cases and the prompt cases, what remains is not a capability question but a cost
question.

**And the cost question is the one that does not survive contact with arithmetic.** The argument
for tuning the house register is that a 900-token style guide is re-sent on every call. At a
hundred thousand calls that is 90 million tokens — against 150 million for a tune that reads a
hundred thousand curated examples three times. The tune is 1.67 times the prompt before anybody
serves the result, and the comparison gets worse: a fixed guide at the front of every request is
the single most cacheable thing a request contains, which is Chapter 52's subject, while the
tune's tokens are spent again at every base-model change. **The saving is real only where the
guide is long, the volume is enormous, and the prefix cannot be cached.**

> **Note:** The order to work in is prompt, then retrieval, then tuning, and the reason is not
> that tuning is bad. It is that the first two are reversible in an afternoon and the third is
> not, which is the whole of the next section but one. Chapter 34's ladder made the same move for
> a different decision: climb from the bottom and stop when your evaluation set passes.

> **Warning:** There is one genuinely good reason to tune that the table above does not contain,
> because it is not an ask. You have a behaviour a prompt reaches *unreliably* — it works eight
> times in ten and the ninth is wrong in a way you cannot instruct away. That is a capability
> case rather than a cost case, and it is the one worth the obligations below. Chapter 20 is how
> you tell eight in ten from nine in ten, and Chapter 38 is how you tell it on a run of steps.

## The Parameter Arithmetic

If you do tune, you almost certainly will not change every parameter. The technique that made
that practical is **low-rank adaptation**, which the field calls LoRA[]{idx="LoRA"}, and it belongs to a
family called **parameter-efficient fine-tuning**, PEFT[]{idx="PEFT"}. Both names come up by their
abbreviations and neither is hard once you can count a matrix, which Chapter 12 taught.

The idea in one line: leave every parameter frozen, and beside each matrix you want to adapt,
train two small ones whose product has the same shape. A matrix of shape `\(d \times d\)`{=latex}
has an update of `\(d^2\)`{=latex} numbers; a pair `\(B\)`{=latex} of shape
`\(d \times r\)`{=latex} and `\(A\)`{=latex} of shape `\(r \times d\)`{=latex} has
`\(2dr\)`{=latex}, and what the model computes is `\(W + BA\)`{=latex}. The number
`\(r\)`{=latex} is the **adapter rank**, and it is the only thing that sets the saving. The word
is the linear-algebra one — how many independent directions the pair can express — and not
Chapter 26's rank, which is a position in a result list.

```python
"""What a low-rank adapter changes, and what it does not save.

The model is chapter 12's shape: width 4,096, feed-forward middle
11,008, 32 layers, vocabulary 128,000. Every count below is that
chapter's arithmetic continued, so the totals match its table.

A full tune is allowed to change every parameter. An adapter leaves
them all frozen and trains a pair of small matrices beside chosen
ones: for a matrix of shape (rows, cols), a (rows, r) and an
(r, cols) in place of a (rows, cols) update.
"""

D_MODEL = 4_096
D_FF = 11_008
LAYERS = 32
VOCAB = 128_000

# Bytes held per parameter. Declared, not derived: a common
# arrangement at the time of writing, and a current convention -
# nothing a provider ships changes it, and a cheaper way of holding
# that state would.
BYTES_WEIGHT = 2        # every parameter, just to run the model
BYTES_TRAINING = 14     # per TRAINABLE parameter, on top of the above


def attn_params():
    return 4 * D_MODEL * D_MODEL


def ff_params():
    return 2 * D_MODEL * D_FF


def total_params():
    layer = attn_params() + ff_params()
    return layer * LAYERS + VOCAB * D_MODEL


def adapter(rows, cols, r):
    """Parameters in one low-rank pair replacing a (rows, cols) update."""
    return r * (rows + cols)


def gb(n_bytes):
    return n_bytes / 1_000_000_000


if __name__ == "__main__":
    total = total_params()
    layer = attn_params() + ff_params()
    assert attn_params() == 67_108_864
    assert ff_params() == 90_177_536
    assert layer == 157_286_400
    assert total == 5_557_452_800      # chapter 12's table
    print(f"  Chapter 12's model: {total:,} parameters.\n")

    print("  One square attention matrix, and one low-rank pair")
    print(f"  standing in for its update ({D_MODEL} x {D_MODEL}):\n")
    full_one = D_MODEL * D_MODEL
    print(f"    the matrix itself          {full_one:>12,}")
    for r in (4, 8, 16, 64):
        a = adapter(D_MODEL, D_MODEL, r)
        print(f"    a pair at rank {r:<2d}          {a:>12,}"
              f"   1 in {full_one // a}")
    print(f"\n  The ratio is {D_MODEL}/(2r), so the rank is the only")
    print("  thing that sets it. Rank 8 is one parameter in 256.\n")

    print("  Now place the pairs. Rank 8, and three choices of")
    print("  which matrices to adapt:\n")
    r = 8
    pair_sq = adapter(D_MODEL, D_MODEL, r)
    pair_ff = adapter(D_MODEL, D_FF, r)
    PLACES = [
        ("two attention matrices", 2 * LAYERS * pair_sq),
        ("all four attention", 4 * LAYERS * pair_sq),
        ("attention and feed-forward", LAYERS * (4 * pair_sq + 2 * pair_ff)),
    ]
    for name, n in PLACES:
        print(f"    {name:28s} {n:>10,}   {n/total:.4%}")

    trainable = PLACES[0][1]
    print(f"\n  Take the first: {trainable:,} trainable against")
    print(f"  {total:,}, a factor of {total // trainable:,}.\n")

    print("  And here is the thing the factor does not buy. The")
    print("  frozen parameters still have to be in memory, because")
    print("  the model still has to run:\n")
    base = total * BYTES_WEIGHT
    full_mem = base + total * BYTES_TRAINING
    lora_mem = base + trainable * BYTES_TRAINING
    print(f"    weights, either way        {gb(base):7.2f} GB")
    print(f"    full tune, per-parameter   {gb(full_mem - base):7.2f} GB")
    print(f"    adapter, per-parameter    {gb(lora_mem - base):7.4f} GB")
    print(f"\n    full tune, in all          {gb(full_mem):7.2f} GB")
    print(f"    adapter, in all            {gb(lora_mem):7.2f} GB")
    print(f"\n  So the trainable count falls by {total // trainable:,} and the")
    print(f"  memory falls by {full_mem / lora_mem:.1f}. Those are different")
    print("  numbers because the frozen weights are most of the")
    print("  second one and none of the first. An adapter makes a")
    print("  tune fit on hardware you have; it does not make the")
    print("  model smaller, and it does not make one request")
    print("  cheaper to serve.")
    print("  Chapter 15 owns what running the thing costs.\n")

    print("  One more number, since it is the one that decides")
    print("  whether you keep several. An adapter is a file:\n")
    for name, n in PLACES:
        print(f"    {name:28s} {gb(n * BYTES_WEIGHT)*1000:7.1f} MB")
    print(f"    the base model              {gb(base)*1000:7.0f} MB")
    print("\n  Which is why one base model with a shelf of adapters")
    print("  is an arrangement people actually run, and twelve")
    print("  full tunes of the same model is not.")
```

```text
  Chapter 12's model: 5,557,452,800 parameters.

  One square attention matrix, and one low-rank pair
  standing in for its update (4096 x 4096):

    the matrix itself            16,777,216
    a pair at rank 4                 32,768   1 in 512
    a pair at rank 8                 65,536   1 in 256
    a pair at rank 16               131,072   1 in 128
    a pair at rank 64               524,288   1 in 32

  The ratio is 4096/(2r), so the rank is the only
  thing that sets it. Rank 8 is one parameter in 256.

  Now place the pairs. Rank 8, and three choices of
  which matrices to adapt:

    two attention matrices        4,194,304   0.0755%
    all four attention            8,388,608   0.1509%
    attention and feed-forward   16,121,856   0.2901%

  Take the first: 4,194,304 trainable against
  5,557,452,800, a factor of 1,325.

  And here is the thing the factor does not buy. The
  frozen parameters still have to be in memory, because
  the model still has to run:

    weights, either way          11.11 GB
    full tune, per-parameter     77.80 GB
    adapter, per-parameter     0.0587 GB

    full tune, in all            88.92 GB
    adapter, in all              11.17 GB

  So the trainable count falls by 1,325 and the
  memory falls by 8.0. Those are different
  numbers because the frozen weights are most of the
  second one and none of the first. An adapter makes a
  tune fit on hardware you have; it does not make the
  model smaller, and it does not make one request
  cheaper to serve.
  Chapter 15 owns what running the thing costs.

  One more number, since it is the one that decides
  whether you keep several. An adapter is a file:

    two attention matrices           8.4 MB
    all four attention              16.8 MB
    attention and feed-forward      32.2 MB
    the base model                11115 MB

  Which is why one base model with a shelf of adapters
  is an arrangement people actually run, and twelve
  full tunes of the same model is not.
```

**The first table is the whole mechanism.** At Chapter 12's width of 4,096, a rank-8 pair holds
65,536 numbers against the matrix's 16,777,216 — one parameter in 256. The ratio is
`\(d/2r\)`{=latex} exactly, so it is set by the rank and by nothing else. Doubling the rank
halves the saving and doubles what the adapter can express, and that is the only trade in it.

**The second table is the choice people actually make**: which matrices get a pair. Two of the
four attention matrices in each of 32 layers comes to 4,194,304 trainable parameters, 0.0755 per
of the model.

**And the third table is the part that gets misremembered.** The trainable count falls by a
factor of 1,325. The *memory* falls by a factor of 8.0. Those are different numbers for a reason
you can state in one sentence: **the frozen parameters still have to be in memory, because the
model still has to run.** 11.11 GB of weights is a cost both arrangements pay, and it is most of
the adapter's total and none of the saving. An adapter makes a tune fit on hardware you have. It
does not make the model smaller, it does not make a forward pass cheaper, and it does not make a
single request cheaper to serve — Chapter 15 owns what running the thing costs. **What it does
make cheaper is serving *several* variants**, and that is the next table.

> **Note:** The bytes-per-parameter figures in that program are declared rather than derived, and
> the docstring says so. Two bytes a parameter to hold the model, and fourteen more for each
> parameter you are allowed to change, is one common arrangement at one moment; the counts are
> a current convention in Chapter 6's sense and the method is not — nothing a
> provider ships changes the figure, and the field working out a cheaper way to hold that state
> would. The range in use is roughly 6 to 18. What the fourteen are made of —
> what a training procedure keeps per parameter, and how the step size in Chapter 14's update
> gets chosen and adjusted — is on Chapter 17's list of what this book black-boxes. **This is
> the one place where something on that list is load-bearing for a reader**: run your own tune
> and you will have to choose a step size, and the honest answer is Chapter 17's — name it, say
> what you know that borders it, say what you would do if you needed it.

**The last table is why anyone cares.** The trained pair is an **adapter**, and at rank 8 on two
matrices it is an 8.4 MB file beside an 11-gigabyte model. One base model with a shelf of adapters is an arrangement people
run; twelve full tunes of the same model is not.

## What You Take On

Chapter 14's Warning said tuning is the last lever to reach for. Here is the bill, and almost
none of it is about accuracy.

```python
"""What owning weights costs you, which a prompt does not.

Part 1 is the obligation list: what has to still exist, and who has
to still care, for each arrangement.
Part 2 is the one that is arithmetic. Every time the provider ships
a base model you want, a tuned system needs a fresh tune that has
to pass its own gate. Two different questions come out of that and
they have different answers, which is the point of the table.
Part 3 is distillation, which is this chapter's extreme case: you
own the weights AND you had to generate the data.
"""

#                                          prompt  tuned
OBLIGATIONS = [
    ("an evaluation set you can re-run",     True,  True),
    ("a release decision per base change",   True,  True),
    ("the training set still exists",        False, True),
    ("the training set is still licensed",   False, True),
    ("the previous weights, for rollback",   False, True),
    ("somewhere to serve the weights",       False, True),
    ("somebody who owns the re-tune",        False, True),
]

BASE_CHANGES = 3          # over eighteen months, declared
GATE_PASS = 0.80          # a re-tune passes its gate this often

# Distillation, part 3. Teacher is chapter 12's model.
TEACHER = 5_557_452_800
STUDENT = 810_000_000    # declared, like the figures above
EXAMPLES = 100_000
TOKENS_OUT = 500


def all_pass(p, k):
    """Chapter 38's pass^k: every one of k gates passes."""
    return p**k


if __name__ == "__main__":
    print("  What has to still be true, for each arrangement.\n")
    print("                                        prompt  tuned")
    for what, a, b in OBLIGATIONS:
        print(f"    {what:34s}  {'y' if a else '-':^5s}  "
              f"{'y' if b else '-':^5s}".rstrip())
    p_only = sum(1 for _, a, b in OBLIGATIONS if a)
    t_only = sum(1 for _, a, b in OBLIGATIONS if b)
    print(f"\n    {p_only} obligations against {t_only}. The {t_only - p_only} extra are the")
    print("    answer to what owning a tuned model costs you, and")
    print("    not one of them is about accuracy.\n")

    print(f"  Part 2. {BASE_CHANGES} base-model changes, and a re-tune that")
    print(f"  clears its gate {GATE_PASS:.0%} of the time:\n")
    print("    changes   took every one   current at the end")
    for k in range(1, BASE_CHANGES + 2):
        print(f"      {k:2d}           {all_pass(GATE_PASS, k):.3f}"
              f"            {GATE_PASS:.3f}")
    end = all_pass(GATE_PASS, BASE_CHANGES)
    print("\n  Read the two columns against each other, because")
    print("  only one of them multiplies. Being on the current")
    print(f"  base at the end needs the LATEST tune to have passed")
    print(f"  and nothing else, so it stays at {GATE_PASS:.2f} however many")
    print("  changes went by - a tune that fails its gate is")
    print("  another tune, and you try again at the next release.")
    print(f"  Having taken EVERY change is chapter 38's pass^k, and")
    print(f"  after {BASE_CHANGES} it is {end:.3f}.\n")
    print("  So the compounding is real and it is not about where")
    print("  you end up. It is about never having fallen behind,")
    print("  which is what you care about if each base model")
    print("  brought something you needed rather than something")
    print(f"  you merely wanted: one more change takes that to")
    print(f"  {all_pass(GATE_PASS, BASE_CHANGES + 1):.3f}, and the other column does not move at all.\n")
    print("  What differs between the two arrangements is what a")
    print("  failure costs. A prompt that fails its re-evaluation")
    print("  is text you edit. A tune that fails its gate is")
    print("  another tune, and the gap until it passes is time on")
    print("  a base model you chose to leave.\n")

    print("  Part 3. Distillation, where you own all of it.\n")
    ratio = TEACHER / STUDENT
    gen = EXAMPLES * TOKENS_OUT
    print(f"    teacher    {TEACHER:>13,} parameters")
    print(f"    student    {STUDENT:>13,}   1 in {ratio:.1f}")
    print(f"\n  The student is {ratio:.1f} times smaller, and the point of")
    print("  it is that it is cheaper to run - chapter 15's")
    print("  subject, not this one. What it costs YOU is the data,")
    print("  because the teacher has to produce it:\n")
    print(f"    {EXAMPLES:,} examples x {TOKENS_OUT} tokens   {gen:,} tokens")
    print("    generated, then read by the tune")
    print("\n  So distillation is a tune whose training set did not")
    print("  exist until you paid to generate it, and every")
    print("  obligation in part 1 applies to it twice: once for")
    print("  the student's weights and once for the teacher you")
    print("  used, whose version is now part of how your student")
    print("  behaves and is a thing you have to write down.")
```

```text
  What has to still be true, for each arrangement.

                                        prompt  tuned
    an evaluation set you can re-run      y      y
    a release decision per base change    y      y
    the training set still exists         -      y
    the training set is still licensed    -      y
    the previous weights, for rollback    -      y
    somewhere to serve the weights        -      y
    somebody who owns the re-tune         -      y

    2 obligations against 7. The 5 extra are the
    answer to what owning a tuned model costs you, and
    not one of them is about accuracy.

  Part 2. 3 base-model changes, and a re-tune that
  clears its gate 80% of the time:

    changes   took every one   current at the end
       1           0.800            0.800
       2           0.640            0.800
       3           0.512            0.800
       4           0.410            0.800

  Read the two columns against each other, because
  only one of them multiplies. Being on the current
  base at the end needs the LATEST tune to have passed
  and nothing else, so it stays at 0.80 however many
  changes went by - a tune that fails its gate is
  another tune, and you try again at the next release.
  Having taken EVERY change is chapter 38's pass^k, and
  after 3 it is 0.512.

  So the compounding is real and it is not about where
  you end up. It is about never having fallen behind,
  which is what you care about if each base model
  brought something you needed rather than something
  you merely wanted: one more change takes that to
  0.410, and the other column does not move at all.

  What differs between the two arrangements is what a
  failure costs. A prompt that fails its re-evaluation
  is text you edit. A tune that fails its gate is
  another tune, and the gap until it passes is time on
  a base model you chose to leave.

  Part 3. Distillation, where you own all of it.

    teacher    5,557,452,800 parameters
    student      810,000,000   1 in 6.9

  The student is 6.9 times smaller, and the point of
  it is that it is cheaper to run - chapter 15's
  subject, not this one. What it costs YOU is the data,
  because the teacher has to produce it:

    100,000 examples x 500 tokens   50,000,000 tokens
    generated, then read by the tune

  So distillation is a tune whose training set did not
  exist until you paid to generate it, and every
  obligation in part 1 applies to it twice: once for
  the student's weights and once for the teacher you
  used, whose version is now part of how your student
  behaves and is a thing you have to write down.
```

**Start with the obligation table, because it is the answer to the interview question.** A prompt
has two standing obligations: an evaluation set you can re-run, and a decision to make when the
base model changes. A tuned model has those two and five more. The training set has to still
exist and still be licensed for this use. The previous weights have to still exist, because a
rollback is a file rather than an edit. The weights have to be served from somewhere. And
somebody has to own the re-tune, which is a person and not a line item.

**Then the part that is arithmetic, and it is two questions rather than one.** Every base-model
change you want to take puts a fresh tune in front of a gate. **Being on the current base model at
the end needs only the latest tune to have passed**, so at an 80 per cent gate it is 0.80 however
many changes have gone by — a tune that fails is another tune, and you try again at the next
release. **Having taken every change is the one that multiplies**: three at 80 per cent is 51.2 per
cent, and one more than you planned for is 41.0. That is Chapter 38's pass\^k, and it is the
figure to care about when each base model brought something you needed rather than something you
merely wanted. **Neither number is a claim that tuning is unreliable.** The first is a claim about
multiplying, and what differs
between the two arrangements is what a failure costs: a prompt that fails its re-evaluation is
text you edit, and a tune that fails its gate is another tune.

**Distillation** is the same bill, twice. A student at one-seventh the parameters is cheaper to
run, which is Chapter 15's subject and the whole point of doing it. What it costs *you* is that
the training set did not exist until you paid a teacher to generate it — a hundred thousand
examples at five hundred tokens is 50 million tokens of generation before the tune starts — and
every obligation above now applies to two sets of weights, because the teacher's version is part
of how your student behaves and is a thing you have to write down.

> **Tip:** Write the rollback down before the release, not after. "We would go back to the
> previous adapter" is a sentence; "the previous adapter is at this path, it was built from this
> data, it passed this gate on this date, and switching back is this one change" is a rollback.
> The second one takes an hour and the first one takes a week, and you find out which you have on
> the day you need it.

## The Two Things It Does That You Did Not Ask For

A tune has a target. It also has effects on everything else, and a generator's data has holes
where the generator's blind spots are. Both are measurable and neither is visible by default.

```python
"""The two things a tune does that you did not ask it to do.

Part 1: it moves tasks you never touched, and you only see that if
you kept a set for them. The target set is 40 cases of the thing
the tune was for; the general set is 40 cases of everything else
the system was already doing.

Part 2: synthetic data. The real inputs arrive in eight shapes; a
generator writes the five it knows about. Replacing and adding are
not two strengths of the same move - they do different things to
the three it does not know.
"""

from math import sqrt

TARGET_N, GENERAL_N = 40, 40
TARGET_BEFORE, TARGET_AFTER = 0.55, 0.85
GENERAL_BEFORE, GENERAL_AFTER = 0.90, 0.775   # 36 and 31 of 40

#  mode                        real cases   the generator knows it
MODES = [
    ("plain question",               9, True),
    ("question with an order id",     7, True),
    ("two questions at once",         6, True),
    ("complaint, no question",        5, True),
    ("question in another language",  4, True),
    ("pasted email thread",           4, False),
    ("question about a screenshot",   3, False),
    ("abuse",                         2, False),
]

SYNTHETIC_TOTAL = 200


def spread(n, p):
    """Chapter 20's spread of a score over which cases you drew."""
    return sqrt(n * p * (1 - p)) / n


if __name__ == "__main__":
    tb, ta = TARGET_BEFORE, TARGET_AFTER
    gb, ga = GENERAL_BEFORE, GENERAL_AFTER

    def cases(score, n):
        """A score on n cases is a count of cases. If it is not a
        whole number of them, the score cannot happen - which is
        how the general set's first figure here was caught."""
        k = round(score * n)
        assert abs(k - score * n) < 1e-9, (score, n)
        return k

    print(f"  Part 1. {TARGET_N} target cases, {GENERAL_N} general ones.\n")
    print("               before    after     move     cases")
    print(f"    target      {tb:.3f}    {ta:.3f}   {ta-tb:+.3f}"
          f"   {cases(tb, TARGET_N)} then {cases(ta, TARGET_N)}")
    print(f"    general     {gb:.3f}    {ga:.3f}   {ga-gb:+.3f}"
          f"   {cases(gb, GENERAL_N)} then {cases(ga, GENERAL_N)}")
    print("\n  The tune did what it was for. It also moved a set")
    print("  nobody trained on, by more than a third as much, in")
    print("  the other direction - and the general set is the one")
    print("  that was already in production.\n")

    sd = spread(GENERAL_N, gb)
    visible = 2 * sd
    print(f"  Could {GENERAL_N} general cases even see that? Chapter 20's")
    print(f"  spread at {gb:.2f} on {GENERAL_N} cases is {sd:.3f}, so two of them")
    print(f"  is {visible:.3f}:\n")
    for fall in (0.03, 0.06, 0.09, 0.12):
        seen = "yes" if fall >= visible else "no"
        print(f"    a fall of {fall:.2f}   past two spreads: {seen}")
    print(f"\n  So this set sees the {gb-ga:.3f} it was shown and would")
    print(f"  miss anything under {visible:.3f}. That is the number")
    print("  to argue about before a tune, not after: a general")
    print("  set is sized by the smallest side effect you would")
    print("  refuse to ship, and 40 cases is not a lot of refusing.\n")

    print("  Part 2. Eight shapes of real input, and a generator")
    print("  that knows five of them.\n")
    known = [m for m in MODES if m[2]]
    unknown = [m for m in MODES if not m[2]]
    real_total = sum(n for _, n, _ in MODES)
    known_real = sum(n for _, n, _ in known)
    per_known = SYNTHETIC_TOTAL // len(known)

    print("    mode                          real  replaced  added")
    for name, n, k in MODES:
        rep = per_known if k else 0
        add = n + (per_known if k else 0)
        print(f"    {name:28s}  {n:>4d}  {rep:>8d}  {add:>5d}")
    print(f"    {'':28s}  {real_total:>4d}  "
          f"{per_known*len(known):>8d}  "
          f"{real_total + per_known*len(known):>5d}")

    unk_real = sum(n for _, n, _ in unknown)
    added_total = real_total + per_known * len(known)
    share_before = unk_real / real_total
    share_after = unk_real / added_total
    print(f"\n  Replacing: {len(unknown)} of the {len(MODES)} modes fall to zero, and")
    print(f"  they are {unk_real} of the {real_total} real cases - "
          f"{share_before:.1%} of the")
    print("  traffic now absent from the training data.\n")
    print("  Adding: every mode survives, and that is the whole")
    print("  difference. What it does instead is dilute them:\n")
    print(f"    {f'the {len(unknown)} unknown modes, in real traffic':40s}"
          f"{share_before:>5.1%}")
    print(f"    {f'the same {len(unknown)} after adding {per_known*len(known)}':40s}"
          f"{share_after:>5.1%}")
    print(f"\n  A factor of {share_before/share_after:.1f}, which is what adding 200 to 40")
    print("  does to any share. Dilution is a number you can see")
    print("  and correct; absence is not.")
    print("\n  Those are not two degrees of the same thing. One")
    print("  changes the MIX, which a tune can be told about and")
    print("  which you can measure. The other removes three")
    print("  shapes of input from the data entirely, and the")
    print("  generator cannot tell you it did, because not")
    print("  knowing about them is exactly why they are missing.")
    print("  That is the whole of the rule: added to real data,")
    print("  never substituted for it.")
```

```text
  Part 1. 40 target cases, 40 general ones.

               before    after     move     cases
    target      0.550    0.850   +0.300   22 then 34
    general     0.900    0.775   -0.125   36 then 31

  The tune did what it was for. It also moved a set
  nobody trained on, by more than a third as much, in
  the other direction - and the general set is the one
  that was already in production.

  Could 40 general cases even see that? Chapter 20's
  spread at 0.90 on 40 cases is 0.047, so two of them
  is 0.095:

    a fall of 0.03   past two spreads: no
    a fall of 0.06   past two spreads: no
    a fall of 0.09   past two spreads: no
    a fall of 0.12   past two spreads: yes

  So this set sees the 0.125 it was shown and would
  miss anything under 0.095. That is the number
  to argue about before a tune, not after: a general
  set is sized by the smallest side effect you would
  refuse to ship, and 40 cases is not a lot of refusing.

  Part 2. Eight shapes of real input, and a generator
  that knows five of them.

    mode                          real  replaced  added
    plain question                   9        40     49
    question with an order id        7        40     47
    two questions at once            6        40     46
    complaint, no question           5        40     45
    question in another language     4        40     44
    pasted email thread              4         0      4
    question about a screenshot      3         0      3
    abuse                            2         0      2
                                    40       200    240

  Replacing: 3 of the 8 modes fall to zero, and
  they are 9 of the 40 real cases - 22.5% of the
  traffic now absent from the training data.

  Adding: every mode survives, and that is the whole
  difference. What it does instead is dilute them:

    the 3 unknown modes, in real traffic    22.5%
    the same 3 after adding 200              3.8%

  A factor of 6.0, which is what adding 200 to 40
  does to any share. Dilution is a number you can see
  and correct; absence is not.

  Those are not two degrees of the same thing. One
  changes the MIX, which a tune can be told about and
  which you can measure. The other removes three
  shapes of input from the data entirely, and the
  generator cannot tell you it did, because not
  knowing about them is exactly why they are missing.
  That is the whole of the rule: added to real data,
  never substituted for it.
```

**Part 1 is the one that ships.** The tune did its job: the target set went from 0.55 to 0.85.
The general set — forty cases of what the system was already doing, which nothing in the tune
touched — went from 0.90 to 0.775, which is 36 of its 40 cases and then 31. **A tune is a change
to the model, so everything the model does
is in scope**, and the only reason that fall is visible at all is that somebody kept a set for
the thing they were not changing.

**Then the question the program asks next, which is the useful one.** *Could* forty general cases
have seen it? Chapter 20's spread at 0.90 on forty cases is 0.047, so two of them is 0.095: this
set sees the 0.125 fall it was shown and would miss anything smaller. **That is a number to argue
about before a tune rather than after.** A general set is sized by the smallest **side effect** you
would refuse to ship, and forty cases is not a lot of refusing.

> **Note:** Two spreads is a rule of thumb and not Chapter 20's instrument for this question.
> Chapter 20's own tool for a before-and-after on the same cases is the paired bootstrap on the
> difference, and run on this set it first clears zero at four flipped cases — a fall of 0.100
> against the 0.095 above. The rule of thumb lands within one case of the right answer here,
> which is why it is worth having; do the paired version when the decision is close.

**And the general set is Chapter 38's distinction doing its work.** The target set is Chapter
38's capability set — it is supposed to be well below 1.0 and it is what the tune is for. The
general set is Chapter 33's regression set — it is supposed to stay where it was, and a fall in it is a release blocker rather
than a number to net against the gain. That is the **evaluation gate**, and it has two conditions: a tune is not released because the
target improved, but because the target improved and nothing else moved.

**Part 2 is about data, and the rule has a mechanism under it.** **Synthetic data** — examples a
model wrote, standing in for examples people produced — is the cheapest way to get a training set
and the easiest to get wrong. Real inputs arrive in eight shapes. A generator writes the five it knows about. [**Replacing**]{.noindex} the real set with 200 synthetic
examples takes three of the eight modes to zero — 22.5 per cent of the traffic, now absent from
the training data entirely. [**Adding**]{.noindex} the 200 to the 40 keeps every mode and dilutes the three
unknown ones from 22.5 per cent of the data to 3.8 per cent, a factor of 6.0, which is simply
what adding 200 to 40 does to any share.

**Those are not two strengths of the same move.** Dilution changes the mix, and a mix is
something you can see in a table and correct by weighting. Absence removes three shapes of input,
and **the generator cannot warn you, because not knowing about those shapes is exactly why they
are missing.** Synthetic data goes *beside* real data, never instead of it, and that is the
reason rather than a convention.

> **Warning:** The three missing modes in that table are the ones worth looking at: a pasted
> email thread, a question about a screenshot, and abuse. A generator asked for "customer support
> questions" writes customer support questions. It does not write the thing somebody sends when
> they are furious, or the thread with four quoted replies, because those are not what the
> request asked for — and they are a fifth of your traffic.

## What To Actually Do

1. **Say what the ask needs before saying which lever to use**: facts the model has not seen,
   behaviour, or neither. Four of this chapter's twelve asks are decided by that word alone.
2. [**For facts, retrieve**]{.noindex} — on a practitioner report rather than on arithmetic, since Chapter 14
   is explicit that its ratio does not reach this case, and on staleness outright for anything
   that changes. A live record lookup counts as retrieval here; Chapter 2 defines the part by
   where it sits.
3. **For behaviour, write the prompt first** and measure it (Chapter 20). Most behaviour asks stop
   here.
4. **Tune for a behaviour a prompt reaches unreliably**, not for one a prompt reaches expensively
   — and if it is the cost, do the token arithmetic and check whether the prefix caches first.
5. **Use an adapter, and know what it saves.** Trainable parameters, by a factor in the
   thousands. Memory, by a factor of about eight at this shape. Serving cost, not at all.
6. **Keep a general set as well as a target set**, sized by the smallest regression you would
   refuse to ship, and work out before you start what that set can actually see.
7. **Release behind a gate that requires both**: the target moved and nothing else did.
8. **Add synthetic data, never substitute it**, and list the modes your generator does not know
   about before you trust its output.
9. **Write the rollback down as a path, a provenance and one change**, before the release.
10. **Say out loud who owns the next re-tune**, because the base model will change and the
    arithmetic above is about how often that goes well.

> **Tip:** The useful answer to "did you fine-tune it?" is not yes or no. It is: *here is what the
> ask needed, here is the lever that reaches it, and here is what I measured* — and if the answer
> is no, say which of this chapter's four facts rows your case looked like. Nobody asking that
> question wants a yes; they want to know whether you know the difference.

## Lab: Price the Levers

Four programs, pure Python, nothing to install, no randomness anywhere. Forty minutes, and there
is a key for every step.

**Step 1.** Save the first program as `choose.py` and run it. Then change the house-register row's
`prompt` field to `True`.

*Expected result:* the count of candidates for tuning falls from 2 to 1, and the behaviour row
counted as prompt-reachable rises to 5. The cost block does not change, because it is computed
from constants rather than from the table — which is worth noticing, since it means the program
cannot tell you that you have just removed its own example.

**Step 2.** In `choose.py`, work out what `CALLS` would have to be for the tune's tokens and the
prompt's to come out equal, then set it and check.

*Expected result:* the tune is 150 million tokens and the guide is 900 a call, so
`\(150{,}000{,}000 / 900 = 166{,}667\)`{=latex} calls. At that figure the ratio prints 1.00. Note
what you have proved and what you have not: the two token counts are equal, and nothing about
serving, caching or the obligations in the third program is in either of them.

**Step 3.** Save the second program as `lora.py` and run it. Then set the rank to 64 in the
placement block by changing `r = 8`.

*Expected result:* the trainable count rises eightfold to 33,554,432 — 0.6038 per cent — and the
memory total rises from 11.17 GB to about 11.58 GB. The trainable factor prints as 165, because
the program floors it and the true ratio is 165.625, and the memory factor barely moves, from 8.0
to 7.7. (The surrounding prose still says "Rank 8", and one widened number now overflows its
column: a program's sentences are fixed text and only its numbers follow the constants.) That is the asymmetry again: eight times the
trainable parameters buys you almost nothing back in memory, because the frozen weights were
never the thing you were saving.

**Step 4.** In `lora.py`, change `BYTES_TRAINING` to 6 — roughly what you would hold if the
training procedure kept nothing per parameter beyond the number that says which way to move it.

*Expected result:* the full tune falls from 88.92 GB to 44.46 GB and the adapter from 11.17 GB to
11.14 GB, so the memory factor falls from 8.0 to 4.0. The adapter's advantage is almost entirely
a statement about what a training procedure holds per trainable parameter, which is why that
constant is declared at the top rather than buried.

**Step 5.** Save the third program as `owning.py` and run it. Then set `GATE_PASS` to 0.95 and
read the `pass^k` column again.

*Expected result:* 0.950, [**0.902**]{.noindex}, 0.857, 0.815 in the left column, and 0.950 all the way down
the right one. Note the second row: by hand `\(0.95^2\)`{=latex} is 0.9025 and you would write 0.903, and the
program prints `0.902`. Not half-to-even — 0.95 has no exact binary form, so the square comes out
as 0.90249999999999996891…, a hair below the tie, and ordinary nearest-rounding gives 0.902. The
figure is not wrong and neither are you. Then read the lesson: a gate that passes 19 times in 20
still leaves a 14 per cent chance of having skipped a base model somewhere in three changes
(`\(1 - 0.95^3 = 0.1426\)`{=latex}), and improving the
gate helps a great deal without making the multiplication go away.

**Step 6.** In `owning.py`, add an obligation of your own to the list and predict what the
printed counts do before you run it.

*Expected result:* whatever you added, the two counts move by one each if you marked both columns
and only the tuned count moves if you marked one. The step is here because the list is the answer
to a question an interviewer asks in exactly these words, and a list you have edited once is a
list you can produce under pressure.

**Step 7.** Save the fourth program as `effects.py` and run it. Then change `GENERAL_N` to 200,
leaving the scores alone.

*Expected result:* the spread falls from 0.047 to 0.021 and two of them to 0.042, so the set now
sees a fall of 0.06 that forty cases missed. Five times the general cases roughly halves the
smallest side effect you can refuse to ship, which is Chapter 20's square root in its least
surprising form.

**Step 8.** In `effects.py`, mark the `abuse` mode as known to the generator.

*Expected result:* two modes fall to zero under replacement rather than three, and the absent
share drops from 22.5 to 17.5 per cent. **The dilution factor does not stay at 6.0 — it becomes
5.9**, and working out why is the step. `per_known` is `SYNTHETIC_TOTAL // len(known)`, so sharing
200 among six known modes gives 33 each and 198 added rather than 200, and the factor is 238/40.
The chapter's claim that 6.0 is "what adding 200 to 40 does to any share" is true of the figures
it ships and the program does not add 200 once you change the table. That is what testing a claim
rather than reading it gets you, and it is the chapter's own sentence that was loose.

**Step 9.** No program. Somebody tells you they fine-tuned a model on their documentation and it
is much better at answering questions about their product. What do you ask?

*Expected result:* first, better than what — a prompt with the documents retrieved into it, or
nothing? That is the comparison that decides whether the tune did anything the cheap lever would
not have. Then: what did the general set do, and how big was it, and what fall could it have
seen. Then: how old is the documentation in the training set, and what happens when it changes.
The last question is the one that usually ends the conversation.

**Step 10.** No program. You have a behaviour that a prompt gets right 8 times in 10, and you are
considering a tune. Write down, before doing anything, what you would need to see to call the tune
a success — and what you would need to see to abandon it.

*Expected result:* a number on the target set with an interval (Chapter 20), a floor on the
general set, and a date. The one that people leave out is the third: a tune without a decision
date becomes a thing somebody is still trying in six weeks, and the obligations in the third
program start accruing on the day you begin rather than on the day you release.

## Summary, Key Terms, and Review Questions

### Summary

There are three levers and an order to try them in: the prompt, retrieval, then tuning. Sort an
ask by what it *needs* — facts the model has not seen, behaviour, or neither — and most cases
decide themselves. Of twelve real asks, 4 need facts — where Chapter 14's one-part-in-two-hundred-
thousand ratio bounds the *share* of knowledge that stage explains and explicitly does not settle
whether a small curated set comes back, so the case rests on a practitioner report plus staleness;
2 are not a model's job; 6 are behaviour and 4 of those are reached by an instruction in the
request. **That leaves 2 of 12
where tuning is even a candidate, and both have a prompt that already works**, so the question is
cost rather than capability — and the cost argument loses: a 900-token guide over 100,000 calls is
90 million tokens against 150 million for the tune, and a fixed prefix is the most cacheable thing
a request contains (Chapter 52). The case that *does* justify a tune is a behaviour a prompt
reaches **unreliably**. **Low-rank adaptation** (LoRA) freezes every parameter and trains a pair
`\(B\)`{=latex}, `\(A\)`{=latex} beside chosen matrices, computing `\(W + BA\)`{=latex}: a
`\(d \times d\)`{=latex} update costs `\(d^2\)`{=latex} and the pair costs `\(2dr\)`{=latex}, a
ratio of `\(d/2r\)`{=latex} set by the **adapter rank** alone — at Chapter 12's width, rank 8 is
one parameter in 256. Two attention matrices across 32 layers is 4,194,304 trainable, 0.0755 per
cent of 5,557,452,800. **The trainable count falls 1,325-fold and the memory only 8.0-fold**,
because the frozen weights still have to be in memory to run; an adapter makes a tune fit on your
hardware and makes no single request cheaper to serve — though it does make serving *several*
variants cheap, because it is an 8.4 MB file, which is why one base
model with a shelf of adapters is a real arrangement. **What you take on** is five standing
obligations a prompt does not have — the training set exists and is licensed, the old weights
exist, somewhere serves them, somebody owns the re-tune — and a gate per base-model change: three
changes at 80 per cent leaves you having taken every one 51.2 per cent of the time — Chapter 38's
pass\^k — while being current at the end needs only the latest tune and stays at 0.80,
and a prompt's failure is text you edit where a tune's is another tune. **Distillation** is that
bill twice, with 50 million tokens of teacher output bought before the tune starts. A tune moves
what you did not train on: target 0.55→0.85 and general 0.90→0.775 here — 36 of 40 cases and then
31 — and Chapter 20's spread says 40 general cases see that 0.125 fall and would miss anything
under 0.095, so size the general
set by the smallest regression you would refuse to ship. The **evaluation gate** requires both:
the target moved and nothing else did. And **synthetic data** goes beside real data, never instead
of it: replacing takes 3 of 8 modes to zero, 22.5 per cent of traffic absent, where adding keeps
every mode and merely dilutes those three to 3.8 per cent, a factor of 6.0. Dilution you can see
and correct; absence the generator cannot warn you about, because not knowing is why it happened.

### Key Terms

| Term | Meaning |
|---|---|
| **Low-rank adaptation** | Freezing every parameter and training a pair of small matrices beside chosen ones, so the model computes `\(W + BA\)`{=latex}. Called LoRA[]{idx="LoRA"}, and the reason a tune fits on hardware you have |
| **Adapter** | The trained pair itself, as a file you keep beside the base model. Megabytes against the model's gigabytes, which is what makes a shelf of them practical |
| **Adapter rank** | The `\(r\)`{=latex} in `\(B\)`{=latex} of shape `\(d \times r\)`{=latex}. It alone sets the saving, at `\(d/2r\)`{=latex}, and doubling it doubles what the adapter can express |
| **Parameter-efficient fine-tuning** | The family low-rank adaptation belongs to: changing few parameters rather than all of them. PEFT[]{idx="PEFT"} in speech and in writing |
| **Distillation** | Training a smaller model on a larger one's output. The student is cheaper to run; what it costs you is that its training set did not exist until you generated it |
| **Evaluation gate** | The rule a tune has to pass to be released: the target set moved *and* nothing else did. Two conditions, and the second is the one that gets dropped |
| **Side effect** | A change to a task the tune was not for. Visible only if you kept a set for the thing you were not changing, and only if that set is big enough to see it |
| **Synthetic data** | Training examples a model wrote rather than people. Added to real data, never substituted for it, because a generator's blind spots become absences nothing in the data can report |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The order to try the three levers | Prompt, then retrieval, then tuning. The first two are reversible in an afternoon |
| What decides the lever | What the ask *needs*: facts the model has not seen, behaviour, or neither |
| Low-rank adaptation | `\(W + BA\)`{=latex}, with `\(B\)`{=latex} as `\(d \times r\)`{=latex} and `\(A\)`{=latex} as `\(r \times d\)`{=latex} |
| What a pair saves on one matrix | `\(d^2\)`{=latex} becomes `\(2dr\)`{=latex}, a ratio of `\(d/2r\)`{=latex}. At `\(d = 4{,}096\)`{=latex}, rank 8 is one parameter in 256 |
| The asymmetry that gets misremembered | Trainable count falls 1,325-fold; memory only 8.0-fold. The frozen weights still have to be in memory |
| What an adapter does not make cheaper | A forward pass, the model's size, or one request's serving. Serving several variants it does make cheaper |
| What owning weights costs | Five standing obligations a prompt has not, none of them about accuracy |
| Base-model changes | A gate each. Current at the end needs only the latest tune, so it stays at the gate's own rate; having taken *every* change multiplies — three at 80 per cent is 51.2 per cent |
| Sizing a general set | By the smallest regression you would refuse to ship. 40 cases at 0.90 see the 0.125 fall and miss anything under 0.095 |
| Synthetic data | Added, never substituted. Replacing took 3 of 8 modes to zero; adding diluted them 6.0-fold |

### Review Questions

1. Prompt, retrieve or tune? How do you choose?
2. What does owning a fine-tuned model cost you that prompting does not?
3. What does a low-rank adapter actually save, and what does it not?
4. Your tune improved the target task by 30 points. What do you check before releasing it?
5. Why add synthetic data to real data rather than using it instead?
6. Somebody says they will fine-tune on their documentation so the model knows their product.
What do you say?

### Review Answers

1. Sort the ask by what it **needs** before reaching for any lever. If it needs facts the model
has never seen, retrieve — Chapter 14's arithmetic is that the tuning stage sees about one part in
two hundred thousand of the tokens pretraining saw, and if the facts change at all then a tuned
model is stale from the day its data was frozen. If it needs a behaviour, write the prompt and
measure it; most behaviour asks stop there. If it needs neither — arithmetic, a lookup — it is
code or a tool. On twelve real asks that leaves two where tuning is even a candidate, and both of
those had a working prompt, which makes it a cost question. **Then the honest case for tuning is
narrower than people expect**: a behaviour a prompt reaches *unreliably*, not one it reaches
expensively. The cost version usually loses the arithmetic — a 900-token guide over a hundred
thousand calls is 90 million tokens against 150 million for the tune — and loses it worse once
you notice that a fixed prefix is the single most cacheable thing in a request.
2. Five standing obligations, and not one of them is about accuracy. The training set has to
still exist and still be licensed for the use. The previous weights have to still exist, because
a rollback is a file rather than an edit. The weights have to be served from somewhere. And
somebody has to own the next re-tune. On top of those, every base-model change you want to take
puts a fresh tune in front of a gate, and the gates multiply: three changes at an 80 per cent
pass rate leaves you having taken every one of them 51.2 per cent of the time, which is Chapter
38's pass\^k — where being on the current base at the end needs only the latest tune to have
passed and stays at 0.80, so it is falling behind that multiplies and not where you end up. The structural difference worth saying out loud is what a failure costs — a prompt that
fails its re-evaluation is text you edit, and a tune that fails its gate is another tune.
Distillation is the same bill twice, because the training set did not exist until you paid a
teacher to generate it.
3. It saves **trainable parameters**, by a factor set entirely by the rank: a
`\(d \times d\)`{=latex} update is `\(d^2\)`{=latex} numbers and the pair is `\(2dr\)`{=latex}, a
ratio of `\(d/2r\)`{=latex}, so at a width of 4,096 and rank 8 it is one parameter in 256 — two
attention matrices across 32 layers being 4,194,304 against 5,557,452,800, a factor of 1,325.
What it saves in **memory** is a different and much smaller number, 8.0 at this shape, because
the frozen parameters still have to be in memory for the model to run: 11.11 GB of weights is a
cost both arrangements pay and is most of the adapter's total. And it saves **nothing** on a
forward pass, on the model's size, or on serving one request — though a shelf of 8.4 MB adapters
beside one base model is far cheaper to keep resident than a full tune per variant. The thing it genuinely buys beyond fitting on
your hardware is that an adapter is an 8.4 MB file, so one base model can carry a shelf of them.
4. What the general set did — and whether you have one. A tune changes the model, so everything
the model does is in scope, and a 30-point gain on the target can sit beside a 12.5-point fall on
forty cases of what the system was already doing. Then check whether that set could have seen a
smaller fall: Chapter 20's spread at 0.90 on forty cases is 0.047, so two of them is 0.095 and
anything under that is invisible. Size the set by the smallest regression you would refuse to
ship, and do it before the tune rather than after. The release rule is the **evaluation gate**
and it has two conditions — the target moved *and* nothing else did — which is Chapter 38's capability set beside Chapter 33's
regression set, doing exactly their jobs: the gain belongs to one instrument and
the fall to the other, and they are not netted.
5. Because replacing and adding do different things to the modes your generator does not know
about. A generator writes the shapes of input it knows; on eight real shapes and five known ones,
replacing the real set takes three modes to zero and removes 22.5 per cent of the traffic from
the training data entirely, while adding keeps every mode and dilutes those three from 22.5 per
cent to 3.8 per cent — a factor of 6.0, which is just what adding 200 examples to 40 does to any
share. Dilution is a number you can see in a table and correct by weighting. Absence is not, and
the reason is the sharp part: **the generator cannot warn you, because not knowing about those
shapes is exactly why they are missing.** The modes that go are the predictable ones — the furious
message, the pasted thread, the screenshot question — because a generator asked for support
questions writes support questions.
6. Ask what "knows their product" means, because the sentence contains the error. Knowledge is
overwhelmingly a pretraining phenomenon and the tuning stage sees about one part in two hundred
thousand of the tokens pretraining saw; what that stage is reliably good at is shaping how the
model responds rather than what it knows. So the first question is: better than what — better than
a prompt with the documentation retrieved into it, or better than nothing? Only the first
comparison tells you the tune did something the cheap lever would not have. Then: how old is the
documentation in that training set, and what happens on the day it changes — because the retrieval
answer reads the current document and the tuned answer is as old as its data. And then the general
set, how big it was, and what size of fall it could have seen. It is not never right to tune, and
Chapter 14's Warning says so; it is the last lever, and this is the shape of the conversation that
establishes whether somebody reached it in order.

> **You understand this when** somebody asks whether you fine-tuned it and your answer is what the
> ask needed, which lever reaches that, and what you measured — not yes or no.
