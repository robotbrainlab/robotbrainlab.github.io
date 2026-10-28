# Why It Fails the Way It Does

This half of the book has been notation and mechanism. This chapter spends them. Each of
the characteristic failures of these systems turns out to be a consequence of something you
have already worked by hand, and the useful thing about that is the conclusion it forces: most
of them are not bugs, nobody is going to fix them, and knowing which is which is what tells
you where to put your engineering.

*The problem.* It invents citations with a straight face, and I'd like to know whether that is
a bug or the design.

*The question.* Which of these failures come from the mechanism itself, which come from how it
is used, and what follows for the things I build?

## There Is No Step Where Truth Is Checked

Walk the pipeline once more, which you can now do from memory. Text becomes tokens.
Tokens become vectors. The vectors pass up a stack, each layer adding to a running sum. The
last position's vector becomes one score per vocabulary entry. Softmax makes those scores into
probabilities. Something picks one.

**Point at the step that consults anything.** There isn't one. There is no source consulted, no check, no
moment where a claim is compared against anything. The whole computation is arithmetic on
numbers that were fitted to make likely text likely, and "likely" is the only quantity in it.

So when a model produces a citation that does not exist, nothing has gone wrong in the sense
that a program has gone wrong. A plausible-looking reference is exactly what a plausible
continuation of "according to the paper by" looks like. The author name is a likely author
name. The year is a likely year. The title is a likely title. **Each piece is individually the
most ordinary thing in the world**, and the assembly is a citation that was never written.

This is what **hallucination** means, and the word is unfortunate because it suggests a
malfunction. The mechanism is working exactly as described in Chapters 9 to 14. What is
missing is a step that was never there.

> **Note:** That is why "the model lied" is the wrong frame, and not only because it is
> impolite. Lying requires knowing the truth and choosing otherwise. There is no represented
> truth to diverge from — there is a probability distribution over tokens, which is a different
> kind of object entirely. The practical consequence is that you cannot fix this by asking the
> model to be more careful, because carefulness is not the faculty that is missing.

**And now the part that matters for your work.** Since nothing in the model checks, the
checking has to live outside it. That is not a workaround; it is the architecture, and it is
one of the four gaps Chapter 2's parts answer. Retrieval puts the source in the request so the
continuation is constrained by something real. Citations let a person verify. Checks test the
output against a rule. None of these makes the model truthful. They make the system's output
checkable, which is a different and achievable thing.

> **Warning:** *Fluency* is not a signal here. The model's prose is as fluent for the
> invented citation as for the real one, because fluency is what the probabilities measure.
> A hedge — "I believe", "if I recall" — is itself a likely continuation in contexts where
> people hedge, not a report of an internal uncertainty. Chapter 31 is where you build
> something that does measure.

## The Failures That Come From Tokens

Chapter 10 gave you the mechanism and one example. Here is the family, because an interviewer
will ask about a different member of it than the one you prepared.

**Counting letters.** A word arrives as one index, or two, or three. A token's spelling is not
in the input, so a question about the letters inside a word is a question about something the
model was not given. What it has instead is whatever it absorbed about spelling in training,
which is recall rather than counting.

**Spelling tasks generally.** Reversing a word, finding words that rhyme, counting syllables,
working with anagrams. All of them ask about structure below the token.

**Arithmetic with digits.** Numbers are cut into pieces like everything else, and the pieces do
not respect place value. Take an addition, and a tokeniser that happens to cut it this way:

```text
  the sum      3721  +  1949

  as digits    3 7 2 1  +  1 9 4 9
  as tokens    37  21   +  19  49
```

Addition is "add the units, carry, add the tens". **There is no units column here.** The 1 and
the 9 that should be added first are each buried inside a two-digit piece, and the model is
given the pieces. Whatever it does to produce an answer, it is not the procedure you were
taught, because the procedure's first step refers to something it cannot see.

Models have got better at this without gaining the ability to see the digits as digits, and the
mechanism underneath has not changed.

> **Note:** The split above is illustrative. Different tokenisers cut numbers differently and
> some cut every digit separately, which is reported to help — and if it does, the help comes
> from the cutting rather than from the model. What does not vary is that the model works on whatever pieces it is
> given, and that nothing guarantees those pieces line up with place value.

> **Tip:** All of these have the same engineering answer, and it is the one from Chapter 10:
> if the answer must be right, do not ask the model to compute it — have it write code that
> computes it, or compute it in your own code. A model that cannot count the letters in
> "strawberry" can write a correct program to count the letters in anything.

## The Context Window, and What Falls Out of It

Every model has a limit on how many tokens it will accept at once. That limit is its **context
window**, and the two earlier chapters said where it comes from: Chapter 11's attention grid is square in
the number of tokens, Chapter 15's key–value cache grows with it, and somebody has to decide where the cost stops
being worth paying.

Two things follow that surprise people.

**It counts the reply too.** The limit is on the request and the reply together, so a long
prompt leaves less room to answer in — and a reply can stop simply because the two reached the
limit, which is one of the ways off Chapter 13's ordinary three, and the one it pointed here
for. Spend one and see:

```text
  the window                      128,000 tokens
  the document you pasted         120,000
  your instructions and question    1,500
                                  -------
  left for the reply                6,500
```

Nobody told you that. You will find out when a long answer stops mid-sentence, and the reply
will report that it hit the limit rather than that it finished.

**It is not memory.** Nothing persists between calls, as Chapter 9 said. The whole conversation is
re-sent on every request, which is also why a long conversation costs more each turn.

**And something has to go when it fills.** This is where products differ, and the differences
are invisible from outside. Some drop the oldest turns. Some summarise what they drop. Some
refuse. Chapter 18 is where a conversation that will not fit gets truncated on purpose and Chapter 35
is where an agent's context is managed deliberately; the point here
is that when a model "forgets" what you said twenty minutes ago, the usual explanation is not
that the model forgot, but that your words were not in the request.

**The sharper version, and the one to know.** When a conversation is truncated, what is
dropped is chosen by a rule in somebody's product code, and that rule does not know what
mattered. The instruction you gave at the start — the one that said "always answer in
French" — is the oldest thing in the conversation.

## Long Inputs Are Not Used Evenly

Here is a finding rather than a mechanism, and Chapter 6's discipline applies: say what kind
of claim it is.

**The claim.** When a long input contains one relevant passage, models are better at using it
when it sits near the beginning or the end than when it sits in the middle. The effect has
been measured across several models and several tasks, and it is a repeated experimental
result rather than a single study — more than one study, and short of settled practice, because
Chapter 6's tell for settled practice is written-down failure modes and nobody has written down
where this stops holding — and still a finding about particular models rather than a law of the
design.

**What it means for you.** Putting more in the context does not reliably mean more of it gets
used. Doubling the retrieved passages in the hope that the right one is in there somewhere is
a strategy that costs twice as much and may work less well. Chapter 28 is where you decide
what to put in and in what order, and this is the reason it is a decision at all.

> **Note:** Do not state this as "models ignore the middle". They do not ignore it; they use
> it less reliably. And the effect's size varies by model and by task, so the useful version
> in an interview is "it has been measured repeatedly, the position of a passage matters, and
> I would measure it on my own data before designing around a number from a paper."

## Why Thinking Out Loud Works

This is the one with a genuinely satisfying explanation, and the mechanism follows from Chapter
9 alone.

Recall two facts. **One forward pass does a fixed amount of arithmetic for the input it is
given** — a fixed number of layers, run once each, and no more of them for a harder question —
and produces exactly one token. **And the model
has no memory between passes**; the only thing carried forward is the text so far.

Put those together. A problem that needs several steps of work cannot get several steps of
work out of one forward pass. The pass is as long as it is. And nothing carries from one pass to
the next: no scratchpad, no variable holding a partial result, nowhere to put an intermediate
answer.

**Except one place. The output.**

If the model emits its intermediate steps as tokens, those tokens become part of the input for
every later pass. The partial result is now in the context, where later tokens can condition
on it. **The model's only scratchpad is its own output** — which is a strange and slightly
undignified fact about the design, and it is why a problem needing several steps has nowhere to
put them unless they are emitted. That the working *improves the answer* is a separate and
weaker claim: the mechanism cannot reach it, because a model may compress the same computation
into one pass and be right anyway. On Chapter 6's ladder it has been demonstrated and studied
in particular settings and is short of settled practice, so how much it buys on your task is
something to measure. Chapter 22 makes the same split for strict output formats.

```text
  without intermediate tokens
    [ question ] -> passes -> answer

  with them
    [ question ] -> passes -> step 1
    [ question, step 1 ] -> passes -> step 2
    [ question, step 1, step 2 ] -> passes -> answer
```

Three rounds instead of one — and each round is one pass per token it emits, as Chapter 9
said — with the third round reading the first two. That is more total
computation applied to the problem, and the extra computation is applied to a question that
has already been partly answered.

> **Note:** That is the mechanism, and it is the whole of what this book says about it. Why
> models have got better at producing useful intermediate steps, and what training does to make
> them do it, is on Chapter 17's list.

## What It Costs, and What the Trace Is Not

Two things to say about intermediate reasoning that people get wrong in opposite directions.

**It is expensive, and in the dear half.** Intermediate tokens are output tokens. A 200-token
chain of working before a 50-token answer is 250 output tokens where you wanted 50 — five
times the output bill — and Chapter 15 says each of those 250 passes reads the whole cache,
which is growing as it goes. Then, where the product keeps it, the working sits in the
context for the rest of the conversation, being re-read.

```text
  answer alone        50 output tokens
  working + answer   250 output tokens     5x

  and every one of the 250 is a pass over a growing cache
```

So it is a lever with a price, not a free improvement, which is why products increasingly make
it conditional — on by default for hard tasks, off for easy ones. That last is a current
convention rather than a property of the design, and it is the kind of detail that moves. Chapter 53 is the bill.

**And the trace is not a log.** This is the one that catches people out, and it follows from
the first section of this chapter.

The intermediate steps are *generated text*. They are produced by exactly the same process as
everything else: plausible continuations, one token at a time, with no step that consults the
computation that is actually happening in the layers. So a chain of working is a plausible
account of how one might reach that answer. It is not a record of how this answer was reached,
because no such record exists — there is nothing in the mechanism that writes one.

The consequence is sharper than it sounds. A model can produce correct working and a wrong
answer, or wrong working and a right answer, and both are ordinary. You cannot read the trace
to find out why it got something wrong; you can only read it as more output, to be checked
like any other output.

> **Note:** This is worth being precise about in an interview, because the sloppy version
> — "the reasoning is fake" — is wrong in the other direction. The intermediate tokens are
> doing real work: later passes genuinely condition on them, which is why the working can change
> the answer at all.
> They are causally involved and they are not a description of the cause. Both halves are true
> and the useful answer says both.

## Which of These You Can Fix

Worth separating, because the engineering is different for each.

| Failure | Where it comes from | What you can do |
|---|---|---|
| Invented facts | No step checks truth | Put sources in the request; check the output; cite |
| Letters, spelling, digits | Tokens, from Chapter 10 | Move the task into code |
| Forgetting things said earlier | Something was dropped from the request | Decide what to drop, deliberately |
| Uneven use of long inputs | Measured behaviour, not a design rule | Put less in, and order it; measure |
| Needing to think out loud | One pass gets no deeper for a harder question | Ask for working where it earns its cost |

**None of the rows says "use a better model".** Better models are reported to make the first
and the second less frequent — Chapter 10 says so for the token-level case — and nothing about
either mechanism predicts a rate, so that half is a report rather than a consequence. What does
not change is why either happens. The third and fifth are properties of how
the thing is used and of the design. The fourth is measured behaviour that varies by model, so
a better model can move it — and what you put in the context is still yours.

## Lab: Diagnose Six Failures

No code. Twenty minutes, and there is a key for every step. For each, say which mechanism
produced it and what you would do.

**Step 1.** A model summarises a document and attributes a quotation to a person who is not
mentioned in it.

*Expected result:* no step checks truth, so a plausible attribution is a plausible
continuation. The engineering is outside the model: the source in the request, a citation the
reader can follow, and a check that every quoted string appears in the source. Note that the
last of those is a rule your code can apply, not a judgement.

**Step 2.** Asked to add two four-digit numbers, a model is confidently wrong in the third
digit.

*Expected result:* tokenisation. The digits are cut into pieces that do not respect place
value, so there is no units column to carry from. Have it write the code, or do the arithmetic
in yours.

**Step 3.** Your chat application is told at the start to answer only in French. Forty turns
later it answers in English.

*Expected result:* the first thing to check is whether the instruction is still in the request,
and the usual answer is that it is not. It was the oldest thing in the conversation, and
whatever rule drops text when the window fills does not know it mattered. Check what you
actually send before blaming the model: forty turns of chat may still fit inside a large
window, in which case the instruction is present and simply not being followed.
The fix is not a sterner instruction — it is to put the instruction back in on every request,
which costs tokens and is worth it.

**Step 4.** A model asked to count the letters in a word gets it wrong, then writes a correct
program to count them.

*Expected result:* both behaviours are the same mechanism. A token's spelling is not in its
input, so counting the letters is recall; writing the program is ordinary text production, which is what it is
good at. This is the single most useful pattern in the chapter: move the task to where the
answer is checkable.

**Step 5.** You add twenty more retrieved passages to a prompt and quality falls.

*Expected result:* two things at once, and you should name both. Long inputs are not used
evenly, so the relevant passage may now sit where it is used less reliably. And the extra
passages cost tokens on every request. Neither is a reason never to retrieve more; both are
reasons to measure rather than assume.

**Step 6.** A model produces three paragraphs of correct-looking working and then a wrong
answer. Your colleague says the working proves it was "reasoning properly" and something went
wrong at the end.

*Expected result:* the working is generated text, produced the same way as everything else,
and is not a record of the computation. It can be correct while the answer is wrong, and that
is ordinary rather than a sign of a late failure. Say both halves: the intermediate tokens did
real work, because later passes conditioned on them — and they are not an account of how the
answer was produced, because nothing in the mechanism writes one.

**Step 7.** Which of the six could be fixed by a better model, and which could not?

*Expected result:* steps 1, 2 and 4 are *reported* to get less frequent with better models, and do not change in
kind — the mechanism that produces them is the mechanism that produces everything else. Step 3 is not about the model at
all — it is a decision in somebody's product code. Step 5 is half yours: how much you put in is
your decision, and how evenly a long input is used varies by model, so measure it. Step 6 is a property of the design and will not change while the
scratchpad is the output.

## Summary, Key Terms, and Review Questions

### Summary

No step in the computation consults anything or checks anything, so a fabricated citation is
an ordinary plausible continuation rather than a malfunction — which is what **hallucination**
means and why asking the model to be careful cannot fix it. The checking lives outside the
model, which is what Chapter 2's checks were for. A family of failures comes from tokens:
counting letters, spelling, reversal, rhyme and arithmetic with digits all ask about structure
below the token, and the engineering answer to all of them is to move the task into code. The
**context window** is a limit on the request and the reply together, it is not memory, the whole
conversation is re-sent every call, and something has to give when it fills — commonly the
oldest thing, which is often the instruction that mattered. Long inputs are not used evenly: a
repeatedly measured finding that a passage's position affects how reliably it is used, which
makes what you put in the context a decision rather than a default. And **intermediate
reasoning** works because one forward pass runs its layers once however hard the question is,
and the model has no memory between passes, so emitting the steps as tokens is the only way to carry partial work
forward — the model's only scratchpad is its own output. That costs output tokens, the dear
half, and the visible trace is generated text rather than a record: the intermediate tokens do
real work *and* are not an account of how the answer was produced.

### Key Terms

| Term | Meaning |
|---|---|
| **Hallucination** | Output that is fluent, plausible and not true. Not a malfunction: no step in the computation checks anything, so a plausible continuation is all the mechanism can produce |
| **Context window** | The maximum number of tokens a model will accept at once. A cost limit rather than a memory, counting the reply as well as the request. The whole conversation is re-sent every call, and something is dropped — or the call refused — when it fills |
| **Intermediate reasoning** | Emitting the steps of a problem as tokens so that later passes can condition on them. The only way to carry partial work forward, because one pass runs its layers once however hard the question is, and nothing persists between passes |

### Review Questions

1. Why is hallucination the default behaviour rather than a defect?
2. Why does asking a model to work step by step improve accuracy, and why is the visible reasoning not a reliable account of how it answered?
3. Your chat application forgets an instruction given forty turns ago. What happened, and what do you do?
4. Name three failures that come from tokenisation and say what they have in common.
5. A colleague wants to double the retrieved passages in the prompt "so the answer is in there somewhere". What do you say?
6. Which of this chapter's failures would a better model fix?

### Review Answers

1. Because there is no step in the computation where anything is checked. Text becomes tokens,
tokens become vectors, the vectors pass up the stack, the last one becomes a score per
vocabulary entry, and softmax makes those into probabilities — and "likely" is the only
quantity anywhere in it. A citation that does not exist is assembled from a likely author, a
likely year and a likely title, each the most ordinary continuation of what came before. The
mechanism is working as described; what is missing was never there. Which is why the checking
has to live outside the model — sources in the request, citations a reader can follow, rules
your code can apply.
2. Because one forward pass does a fixed amount of arithmetic for the input it is given — no
more layers for a harder question — and produces one token, and nothing persists between
passes. A problem needing several steps cannot get several steps out
of one pass, and there is no scratchpad to hold a partial result — except the output. Emitting
the steps as tokens puts them in the context, where later passes can condition on them, so
more computation is applied and it is applied to a partly-answered question. The trace is not a
reliable account because it is generated text, produced the same way as everything else, with
no step consulting what the layers actually did. Both halves matter: the tokens do real work,
and they are not a description of the cause.
3. Most likely the instruction is no longer in the request — it was the oldest thing in the conversation,
and the rule that drops text when the window fills does not know what mattered. Nothing was
forgotten by the model, because the model has no memory: your words simply were not in the
request. The fix is to re-send the instruction on every call rather than to word it more
firmly, and to decide deliberately what gets dropped rather than leaving it to a default.
4. Counting the letters in a word, reversing or rhyming or counting syllables, and arithmetic
with digits. What they have in common is that they all ask about structure *below* the token:
the model is given seat numbers, not spellings, so the thing being asked about is not in its
input. They also share an answer — if it has to be right, move the task into code, which the
model is good at writing.
5. That it costs twice as much on every request and may work less well. Long inputs are not
used evenly: a passage's position affects how reliably it is used, measured repeatedly across
models and tasks, so burying the right passage among twenty others is not a neutral act. The
honest version is that this is a thing to measure on their own data rather than to assume in
either direction — and that ordering what goes in is a decision, not a default.
6. The rate of invented facts and token-level mistakes is reported to fall with better models, without the
reason for either changing. The only other one that moves with the model is the uneven use of long
inputs, which varies by model and by task and is a thing to measure rather than to assume. The
rest are not about the model: an instruction falling out of the window is a decision in
somebody's product code, how much you put in the context is a decision in yours, and needing to think out loud is a property of the design that will hold
for as long as one pass does fixed work and the output is the only scratchpad.

> **You understand this when** you can say why a fabricated citation and a correct answer are
> produced by exactly the same process, without calling either one a bug.
