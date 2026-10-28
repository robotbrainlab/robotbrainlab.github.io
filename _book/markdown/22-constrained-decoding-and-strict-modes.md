# Constrained Decoding and Strict Modes

Chapter 21 built a validator and never once trusted the model to honour a format. This chapter
is about the other end of the problem: what happens when the provider enforces the format in a
**strict mode**, how that is done, and why it is not the end of the matter.

*The problem.* One provider guarantees my format and another ignores it, and on one task the
strict mode made the answers worse.

*The question.* How is a format constraint actually enforced while the model generates, and what
does enforcing it cost?

## What a Constraint Actually Does

Chapter 13 left the model at the moment of choosing: a score for every token in the
vocabulary — its *logit*, Chapter 13's word — a softmax to turn those scores into probabilities, and a rule for
picking one. **A constraint
goes in between.** Before the pick, something crosses out every token the format does not allow,
and the pick happens among what is left.

That is **constrained decoding**, and the implementation is one line.

Here is a working decoder. The model is a stand-in — the score of the next token depends only on
the last one, and the numbers are written out rather than computed, so every figure in this
chapter can be checked by hand.

```python
import math

VOCAB = ["Sure", "!", "{", "}", ":", '"sentiment"', '"positive"', '"negative"']

# A stand-in model. The score of the next token depends only on the last one,
# and the numbers are written out rather than computed, so every figure below
# can be checked by hand. Anything not listed scores 0.0.
NEXT = {
    None:          {"Sure": 6.0, "{": 4.0, '"sentiment"': 1.0},
    "Sure":        {"!": 5.0, "{": 3.0},
    "!":           {"{": 4.0, "Sure": 0.5},
    "{":           {'"sentiment"': 5.0, "}": 1.5},
    '"sentiment"': {":": 6.0, "}": 1.0},
    ":":           {'"positive"': 4.0, '"negative"': 3.0, "Sure": 2.0},
    '"positive"':  {"}": 5.0, ":": 1.0},
    '"negative"':  {"}": 5.0},
    "}":           {},
}

def scores(last):
    row = NEXT[last]
    return [row.get(t, 0.0) for t in VOCAB]

def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    total = sum(e)
    return [v / total for v in e]
```

The format, written as a *grammar* — a set of rules saying which characters may follow
which — compiles into a **state machine**: in each state, the set of tokens that may come next.
Engines call the same object an automaton; this chapter says state machine throughout.

```python
# The grammar, as a state machine: which tokens may come next in each state.
ALLOWED = [
    {"{"},
    {'"sentiment"'},
    {":"},
    {'"positive"', '"negative"'},
    {"}"},
]

def generate(constrained, steps=5):
    out, last, state = [], None, 0
    for _ in range(steps):
        s = scores(last)
        if constrained:
            s = [v if VOCAB[i] in ALLOWED[state] else -math.inf
                 for i, v in enumerate(s)]
            state += 1
        token = VOCAB[max(range(len(VOCAB)), key=lambda i: s[i])]
        out.append(token)
        last = token
    return out

if __name__ == "__main__":
    print("  free:        " + " ".join(generate(False, 7)))
    print("  constrained: " + "".join(generate(True)))
```

```text
  free:        Sure ! { "sentiment" : "positive" }
  constrained: {"sentiment":"positive"}
```

**The free run is the reply from Chapter 21's list** — a polite preamble and then perfectly good
JSON, which does not parse, because the preamble is part of the string. It is printed token by
token above; the string itself is `Sure!{"sentiment":"positive"}`, and `json.loads` rejects it
at character 0. The constrained run
cannot produce the preamble, because at the first step the only token with a score left is `{`.

**The line that does the work is the one that sets a score to negative infinity.** That is
**masking**: a token with a score of `\(-\infty\)`{=latex} gets `\(e^{-\infty} = 0\)`{=latex}
from the softmax, so — as long as at least one token survives — its probability is exactly zero
and no decoding rule can choose it. That condition is not pedantry: mask every token and this softmax
returns `nan` rather than zero, because it shifts by the maximum and
`\(e^{-\infty - (-\infty)}\)`{=latex} is undefined. The lab builds that state on purpose. Nothing is bolted onto the
model. The model computes exactly what it would have computed; the constraint
edits the numbers on their way out.

> **Note:** A real engine does not carry a list of allowed token strings per state. It compiles
> your schema into a state machine over characters and then, for each state, works out which of the
> vocabulary's tokens are legal — which is where the interesting difficulties live, and the
> section after next is about them.

## The Mask, Step by Step

The mechanism is simple. What it costs is the thing worth measuring, and you can measure it: the
**masked mass** at each step, which is how much probability the mask threw away.

```python
import math
from decode import VOCAB, ALLOWED, scores, softmax

last, state = None, 0
print("  step  free pick   p     allowed pick  p      mass masked")
for step in range(1, 6):
    s = scores(last)
    p = softmax(s)
    free = max(range(len(VOCAB)), key=lambda i: s[i])
    keep = [i for i in range(len(VOCAB)) if VOCAB[i] in ALLOWED[state]]
    masked = 1.0 - sum(p[i] for i in keep)
    best = max(keep, key=lambda i: s[i])
    q = softmax([s[i] if i in keep else -math.inf for i in range(len(VOCAB))])
    print(f"  {step:^4}  {VOCAB[free]:<11} {p[free]:.3f} "
          f"{VOCAB[best]:<13} {q[best]:.3f}  {masked:.3f}")
    last, state = VOCAB[best], state + 1
```

```text
  step  free pick   p     allowed pick  p      mass masked
   1    Sure        0.866 {             1.000  0.883
   2    "sentiment" 0.934 "sentiment"   1.000  0.066
   3    :           0.979 :             1.000  0.021
   4    "positive"  0.627 "positive"    0.731  0.142
   5    }           0.945 }             1.000  0.055
```

**Look at step 1 and then at steps 2, 3 and 5.**

At step 1 the model wanted to write *Sure* with a probability of 0.866, and the grammar allowed
only `{`. The mask deleted 88.3 per cent of the probability mass — you can check it by hand, as
`\(1 - 0.117 = 0.883\)`{=latex} — and the single survivor was renormalised to 1.000. The
constraint did not nudge the model. It overruled it.

At steps 2, 3 and 5 the mask removed almost nothing: 6.6, 2.1 and 5.5 per cent. The model was
already going where the grammar wanted, so the constraint was free.

**Most of the time a constraint costs nothing**, because a model asked for JSON mostly produces
JSON — which is a practitioner's observation rather than a measurement, so hold it loosely.
**And the mask deletes whatever the model was going to emit — and whether that costs you
anything depends entirely on what that was.** Chapter 21 drew the same line for repairs: the
envelope or the contents. Step 1 deleted the envelope. *Sure* is a preamble, deleting it is the
whole purpose of the feature, and the 88.3 per cent is therefore the chapter's largest number
and its cheapest deletion. Nothing was lost.

Step 4 is where a cost could have arisen, and did not. The grammar allowed two values, so the
mask removed 14.2 per cent — 8.5 of it the probability on *Sure*, and the remaining 5.7 spread
over the five tokens the stand-in model scores at zero, which is worth noticing on its own: a
mask deletes the floor as well as the rival. What it left was a genuine choice between
`"positive"` and `"negative"`, decided by the model, raising the winner from 0.627 to 0.731.

**A constraint that leaves a real choice is doing what you asked. A constraint that leaves one
option is making the decision itself** — and that is one of the two ways a strict format can
cost you something, which lab step 3 makes you do deliberately. Set state 3 to allow only
`"negative"` and the output becomes `{"sentiment":"negative"}`, against a model that scored
`"positive"` at 4.0 and `"negative"` at 3.0. You did not constrain the format. You picked the
answer. Notice what this run does
*not* show: nowhere in it does the mask delete anything the model needed. For that you need a
schema that forbids the working, and the section after next is about it.

> **Tip:** If you can get at the logprobs, the quantity in that last column is worth logging on
> a sample of calls — not because a large number is bad in itself, as step 1 shows, but because
> *where* it is large tells you something. Large on the envelope means the model keeps trying to
> write a preamble, which is a prompt problem showing up as a decoding statistic. Large on a
> value slot means the model wanted to say something your schema does not allow, which is the
> case worth reading the examples for.

## Why the Support Varies Between Engines

Now the part that answers the first half of the opening problem, and it is not vendor
capriciousness. It is a genuinely awkward computation.

**Your schema is written over characters. Generation happens over tokens.** JSON's syntax is
defined in characters — a `{`, then a `"`, then field characters. The model does not emit
characters; it emits tokens from Chapter 10's vocabulary, and a token can carry several
characters at once. So "which tokens are legal here" is not a question the schema answers
directly, and the cheap way of answering it is wrong.

```python
# The grammar is written over characters. Generation happens over tokens,
# and a real vocabulary has tokens that span more than one character.
VOCAB = ["{", "}", '"', "{}", "}}", '":', '"}', '{"s']

NEXT_CHARS = '{"'      # the characters the grammar will accept next, in order

def first_char_ok(tok):
    """The cheap check: does the token start with a character we allow?"""
    return NEXT_CHARS.startswith(tok[0])

def every_char_ok(tok):
    """Correct, as far as this window reaches: every character the token
    contributes must fit. A token that runs past the window is reported
    illegal, which is the limitation step 5 asks you to find."""
    return NEXT_CHARS.startswith(tok)

print(f"  the grammar will accept {NEXT_CHARS!r} next")
print(f"  {'token':8} {'first char':>11} {'every char':>11}")
for tok in VOCAB:
    print(f"  {tok!r:8} {str(first_char_ok(tok)):>11} {str(every_char_ok(tok)):>11}")
```

```text
  the grammar will accept '{"' next
  token     first char  every char
  '{'             True        True
  '}'            False       False
  '"'            False       False
  '{}'            True       False
  '}}'           False       False
  '":'           False       False
  '"}'           False       False
  '{"s'           True       False
```

**Two rows matter, and they are wrong in opposite directions.**

`{}` begins with a character the grammar wants and then emits one it does not — it closes the
object before the field has been written. The cheap first-character check admits it. **So
checking the first character is too loose**, and it is *almost* right, which is exactly why it
ships.

`{"s` is the other failure. In real JSON it is perfectly legal: `{`, then `"`, then the first
letter of a field name. The window check calls it illegal, because the window is only two
characters long and the token runs past the end of it. **So checking against a short window is
too strict**, and a decoder built that way masks out legal tokens and can leave itself with
none — the dead state the lab builds in step 4.

So neither shortcut works, and the real check runs the *whole* grammar over every character a
candidate token would contribute, for every token in the vocabulary, in every state — asking not
"does this fit what comes next" but "does this leave the grammar satisfiable". With a vocabulary of Chapter 9's size that is not
something you do per step, so engines precompute it: for each state of the state machine, the
set of legal tokens, built once and cached — in practice lazily, as each state is first reached,
and with the cache bounded.

**And that precomputation is where the feature differences come from.** A schema feature that
keeps the state machine small and deterministic is cheap to support. One that makes it large, or
that cannot be decided without looking far ahead, is expensive or impossible:

| Schema feature | Why it is easy or hard |
|---|---|
| A fixed set of field names, in order | A short, deterministic state machine |
| An enum of string values | A small branching table of the allowed strings; the easy case |
| `anyOf` between similar shapes | Branches that stay open for many tokens |
| A regular-expression `pattern` | Fine if it compiles to a small state machine, awful if it does not |
| `minLength` or `maxLength` | Needs a counter, and tokens advance it by varying amounts |
| Recursion, or unbounded nesting | The state is a stack rather than a number |

**So when one provider guarantees your schema and another ignores half of it, the difference is
usually which features survived that compilation** — not how much either of them cares. Read
what the engine says it accepts, and assume the parts it is silent about are not enforced.

> **Warning:** Those feature names and which engine supports which are the most perishable facts
> in this chapter, and the table above is about the *reason*, not a product comparison. The
> reason does not date. Check the current support yourself, and keep Chapter 21's validator
> either way, because a feature silently not enforced looks exactly like a feature enforced and
> satisfied.

## When a Strict Format Makes the Answer Worse

This is the second half of the opening problem and the better interview question, because the
honest answer has two parts that are at very different levels of confidence.

**The mechanism is a derivation, and you have already seen it.** The mask deletes probability
mass, and the mass it deletes is what the model was going to say. Now put that next to
Chapter 16's finding: the model's only scratchpad is its own output, so emitting intermediate
tokens is how later tokens get to condition on partial work. A schema that permits only
`{"answer": …}` forbids the intermediate tokens *entirely*. The model cannot work through the problem
first, because there is nowhere to work: every token it emits must be part of the final object.

**Be exact about what that establishes.** It is a derivation in Chapter 6's sense, and what it
derives is that **the scratchpad is gone** — which follows from what the grammar admits plus
Chapter 16's architectural fact, and the reader can check both. It does *not* derive that the
answers get worse. That needs a third premise the chapter cannot supply: that writing the working
out actually improves the answer on this task. A model may compress the same computation into one
forward pass and be right anyway. So the capability claim is off the ladder and the accuracy claim
is not, and it is the capability claim that tells you where to look — tasks that need working out
rather than looking up.

**The size of the effect is a different matter, and it is much weaker evidence.** Put it on
Chapter 6's ladder honestly: that strict formats cost accuracy on reasoning-heavy tasks has been
*demonstrated* by people showing before-and-after examples, and *studied* in particular settings
with particular schemas and models. It is not settled practice, and the tell is Chapter 6's own:
nobody has written down where it stops holding. Anyone who tells you strict mode costs you *n*
per cent is quoting one setting.

**And the other way is simpler and entirely under your control.** A schema can be so
narrow that the right answer is not expressible in it. An enum of two values when the honest
answer is a third, a `maxLength` shorter than the shortest correct reply, a required field the
case has no value for — in each the mask deletes the right answer because you forbade it. That
one is not a subtle effect at the edge of the evidence; it is arithmetic, it is visible in lab
step 3, and it is far commoner than the reasoning effect.

**The fix for the first follows from the mechanism rather than from the evidence**, which is why it is worth
knowing even though the size is unsettled. Give the model somewhere to work:

```text
  bad   {"answer": "..."}
  good  {"reasoning": "...", "answer": "..."}
```

A field for the working, *before* the answer field, restores the scratchpad inside the schema.
The order matters and it matters for a mechanical reason: tokens condition on what came before
them, so a `reasoning` field after `answer` is written after the answer has been committed and
cannot inform it.

**That fix depends on something worth checking.** It only works if the engine holds you to your
schema's field order — the first row of the table above. JSON itself does not care about key
order, so a grammar that admits any order lets the model emit `answer` first and the field you
added does nothing at all. It is then text that cannot have influenced the answer, which is a different and much less
useful thing.

> **Note:** Whether to show that field to anyone is a separate decision. Chapter 16 is clear
> that a visible trace is not an account of how the answer was reached, so a `reasoning` field
> is there to improve the answer, not to explain it to a user.

## What You Still Have to Test

A guaranteed format is worth having. Here is what it does not buy you.

**It does not buy you correctness.** This is Chapter 21's four layers again: a strict mode moves
layers 1, 2 and often 3 to the provider, and layer 4 — *are the values true* — is untouched. A
constrained decoder will produce `{"sentiment": "positive"}` about a furious review with the
same confidence it produces the right answer. Measuring that is chapters 30 and 31.

**It does not buy you your whole schema.** The engine enforces the subset it compiled. Keep the
validator, and if it never fires, Chapter 21's rule of three tells you what you are entitled to
conclude from that silence.

**And turning it on is a change, so measure it.** This is the part people skip. A strict mode
alters what the model emits, which means it can alter the answers — that is what the previous section was about. So it is a change like any other, and Chapter 20 applies unchanged: run both
versions on the same cases, keep the results paired, and put an interval on the difference.
Nothing about *a provider guarantees the format* tells you whether your answers got better or
worse, and the people who are surprised by a strict mode making things worse are the people who
turned it on without measuring.

**Test the format as well as the content**, because they fail independently and for different
reasons. Two measurements, not one:

| Measure | Catches |
|---|---|
| Validation failure rate | A schema feature the engine did not enforce; a truncated reply |
| Task accuracy, paired against the unconstrained version | The answers getting worse because the model lost its scratchpad |

The first can be zero while the second is terrible. That combination — perfect format, worse
answers — is the exact shape of the opening problem, and it is invisible to anybody measuring
only the first.

## Lab: Build a Constrained Decoder and Break It

Three programs, pure Python, nothing to install, every number checkable by hand. Forty minutes,
and there is a key for every step. Work in a new empty folder.

**Step 1.** Save the model and the grammar — *both* code blocks above, in that order — as
`decode.py`, and run it.

*Expected result:* `Sure ! { "sentiment" : "positive" }` free, and `{"sentiment":"positive"}`
constrained.

**Step 2.** Save the mask program as `mask.py` in the same folder and run it. Check step 1's
masked mass by hand from the `NEXT[None]` row. An `ImportError` naming `ALLOWED` means you
saved only the first block in step 1; seeing `decode.py`'s own two lines first means its demo is
not under `if __name__ == "__main__":`.

*Expected result:* the chapter's table. By hand: the scores are 6.0 for `Sure`, 4.0 for `{`, 1.0
for `"sentiment"` and 0.0 for the other five, so
`\(p(\texttt{\{}) = e^{4-6} / (e^{0} + e^{-2} + e^{-5} + 5e^{-6}) = 0.117\)`{=latex} and the mass
masked is `\(1 - 0.117 = 0.883\)`{=latex}.

**Step 3.** In `ALLOWED`, make state 3 allow only `"negative"`. Run `decode.py` again. What
changed, and what did it cost?

*Expected result:* the output becomes `{"sentiment":"negative"}`. The model preferred
`"positive"` at 4.0 against 3.0, so you have not constrained the format — you have chosen the
answer. A schema whose enum has one member is not a format constraint, and this is the thing to
look for in somebody else's schema.

**Step 4.** Give state 0 an empty allowed set: `set()`. Run `decode.py`. What happens, and why
is that the worst possible behaviour?

*Expected result:* the free line is unchanged and the constrained line becomes
`Sure"sentiment":"positive"}` — the decoder emits `Sure`, the one token the grammar most clearly
forbids, and then carries on through the remaining states as if nothing had happened. Every
score is `-inf`, so `max` returns the first index and the mask silently ceases to mean anything.
Nothing raises. `generate` never calls `softmax`, but try `softmax([-math.inf]*8)` yourself: you
get eight `nan` values rather than eight zeros, because `exp(-inf - -inf)` is not defined — which
is why the claim earlier in this chapter that a masked token gets probability zero needed its
condition. A **dead state** — a grammar state with no legal token — is a bug that produces output
instead of an error, which is why you would want an engine to check its state machine for dead
states when it compiles the schema rather than when it decodes.

**Step 5.** Save the token program as `tokens.py` and run it. Then lengthen the window: set
`NEXT_CHARS` to `'{"sentiment"'` and run it again.

*Expected result:* first the chapter's table. With the longer window, `'{"s'` flips to `True`
and `True`, because the token no longer runs past the end of what the check can see — and
`'{}'` still disagrees, because it is genuinely illegal however far you look. That is the
distinction to take away: `{}` is a *wrong* token and no window length will make it right, while
`{"s` was only ever reported wrong because the check could not see far enough. One is a
correctness problem and the other is a horizon problem, and only the second goes away by looking
further ahead.

**Step 6.** Without running anything: your schema is `{"answer": "yes" | "no"}` and your task is
a question that needs three steps of arithmetic. Predict what strict mode does to your accuracy
and say why.

*Expected result:* the mechanism says the scratchpad is gone, and it says nothing about how much
accuracy you lose — keep those apart, because that is the whole discipline of the section above.
The schema permits no tokens except the object, so there is nowhere for the model to do the three
steps, and Chapter 16 says its only scratchpad is its own output. What follows is that the model
cannot show the working, not that it will get the answer wrong — those are different claims and
only the first is derivable. Measure it; do not predict it. The fix is a `reasoning` field
before `answer`. The honest part of the answer is the second half: you do not know *how much* it
will fall, that is not settled, and the way to find out for your task is Chapter 20 — both
versions, same cases, paired, with an interval on the difference.

**Step 7.** Your provider's strict mode is on. Your validation failure rate over two thousand
replies is zero. Name two things you still do not know.

*Expected result:* whether the parts of your schema the engine did not compile are being
enforced — a `maxLength` or a `pattern` silently ignored looks exactly like one satisfied — and
whether the answers are right, which no constraint on shape can tell you. A third, if you
spotted it: whether the answers got *worse* when you turned it on, which you cannot know unless
you measured before.

## Summary, Key Terms, and Review Questions

### Summary

A format constraint is enforced by **masking**: before each pick, every token the format
forbids has its score set to `\(-\infty\)`{=latex}, so the softmax gives it probability exactly
zero and — as long as one token survives — no decoding rule can choose it. The model computes what it would have computed; the
constraint edits the numbers on the way out, and the format itself is a **state machine** over
the tokens allowed next. Measured on this chapter's decoder, the mask deleted 88.3 per cent of
the probability mass at step 1 — where the model wanted to write *Sure* — and 6.6, 2.1 and 5.5
per cent at three of the other four. **The mask deletes whatever the model was going to emit,
and whether that costs you anything depends on what that was**: step 1's 88.3 per cent was a
polite preamble, so the chapter's largest deletion is also its cheapest, and nowhere in that run
does the mask remove something the model needed. Support varies
between engines because **your schema is written over characters and generation happens over
tokens**: the token `{}` starts with a character the grammar wants and then emits one it does
not, so the cheap first-character check is too loose — while a check against a short window is
too strict, calling the perfectly legal `{"s` illegal because it runs past the end of what the
window can see. The real check runs the whole grammar over every character a candidate token
would contribute, for every token, in every state, asking whether it leaves the grammar
satisfiable — which engines precompute, and which is why features that keep
the state machine small and deterministic are supported while recursion, length bounds and open
branches often are not. A strict format can make answers worse, and the two halves of that
claim sit at very different strengths: the **mechanism is a derivation** — the schema forbids
intermediate tokens and Chapter 16 says the model's only scratchpad is its own output — while
the *size* of the effect is a handful of studies, each in one setting, with nobody having
written down where it stops holding. There is also a second and much commoner way to make
answers worse, which is arithmetic rather than subtlety: **a schema too narrow to express the
right answer**, which deletes it because you forbade it. The fix for the first follows from the
mechanism: a **`reasoning` field before the answer field**, in that order, because tokens
condition only on what came before them — and it works only if the engine holds you to your
schema's field order, since JSON itself does not. And a guaranteed format
buys shape, not sense: keep Chapter 21's validator, measure the failure rate and the task
accuracy separately because they fail independently, and treat turning strict mode on as a
change to be measured Chapter 20's way — paired, same cases, an interval on the difference.

### Key Terms

| Term | Meaning |
|---|---|
| **Constrained decoding** | Restricting each token choice to what the format allows, by editing the scores before the pick. The model is unchanged |
| **Masking** | Setting a forbidden token's score to `\(-\infty\)`{=latex}, which makes its probability exactly zero after the softmax — as long as one token survives. Mask them all and you get `nan`, not zero |
| **Strict mode** | A provider's facility for enforcing a schema during generation, as against asking for it in the prompt |
| **Masked mass** | How much probability the constraint deleted at a step. Small means the constraint was free; large means it overruled the model |
| **Dead state** | A grammar state with no legal token. It does not raise — the mask stops meaning anything and the decoder emits whatever was first |
| **State machine** | What a schema compiles into: a set of states, each with the tokens allowed next. Engines call it an automaton |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The mechanism | Score → `\(-\infty\)`{=latex} for forbidden tokens → softmax gives 0 → pick. One line, and only while one token survives |
| What a constraint costs | The mass it deletes, which costs you only when that was the answer rather than the envelope |
| Why engines differ | Schemas are over characters, generation is over tokens; the legal-token set is precomputed per state |
| Both wrong checks | First character only is too loose (admits `{}`); a short window is too strict (rejects `{"s`) |
| Why strict modes can hurt | No room for intermediate tokens, and the model's only scratchpad is its own output. Also: a schema too narrow to hold the right answer |
| The fix, and its order | A `reasoning` field *before* the answer field — and only if the engine fixes field order |
| What it never buys | Correctness, or the parts of your schema the engine did not compile |

### Review Questions

1. How is a format constraint actually enforced while the model generates?
2. When can a strict output format make the answer worse?
3. Why does schema support vary between providers?
4. Your strict mode has produced valid JSON on every one of two thousand calls. What have you learned?
5. A colleague turns on strict mode and reports that the format problem is solved. What do you ask them to measure?

### Review Answers

1. By masking the scores before the token is picked. The model runs exactly as it would
otherwise and produces a score for every token in the vocabulary; a state machine compiled from
the schema says which tokens are legal at this point; every illegal token's score is set to
negative infinity, so the softmax gives it `\(e^{-\infty} = 0\)`{=latex} and no decoding rule —
greedy, top-k, top-p — can select it; and the pick happens among what is left. State the
condition, because it is the thing somebody will push on: that holds while at least one token
survives, and a state where none does is a dead state, where the mask stops meaning anything
and the decoder emits whatever came first rather than raising. Nothing is added
to the model and nothing is retried. Two details worth volunteering: the renormalisation means
the surviving tokens' probabilities go up, so a state with one legal token has that token at
probability 1 whatever the model thought; and the legal-token set is precomputed per state
rather than worked out per step, because the vocabulary is the size Chapter 9 gives.
2. When the schema leaves the model nowhere to think. The answer has two parts at different
strengths, and saying so is most of a good answer. The mechanism is a derivation: masking
deletes the probability the model had put on the tokens it was going to emit, and if the schema
permits only the final object then the tokens it forbids are the intermediate ones — and the
model's only scratchpad is its own output, so there is nowhere else for the working to happen.
That predicts the damage lands on tasks that need working out rather than looking up. The size
of the effect is much weaker evidence: demonstrations and a few studies in particular settings,
not settled practice, and nobody has written down where it stops holding, so anybody quoting a
percentage is quoting one setting. The fix comes from the mechanism rather than the evidence: a
`reasoning` field *before* the answer field, in that order, because tokens condition only on
what precedes them — after the answer it is text that cannot have influenced it. One caveat
worth volunteering: that only helps if the engine holds you to your schema's field order, since
JSON does not care about it.

**And name the second way, because it is commoner and it is entirely your own doing:** a schema
too narrow to express the right answer. An enum of two values when the honest answer is a third,
a `maxLength` shorter than the shortest correct reply, a required field the case has no value
for. The mask deletes the right answer because you forbade it, and no amount of reasoning space
helps.
3. Because the schema is written over characters and the model generates tokens, so an engine
has to work out, for every state of the state machine it compiles from your schema, which of the
tokens in the vocabulary are legal. Checking only the first character is too loose — `{}` begins
legally where `{"` is wanted and then closes the object — and checking against a short lookahead
window is too strict, because a token like `{"s` is entirely legal and simply runs past the end
of the window. The real check asks whether a token leaves the grammar satisfiable. That set is precomputed and cached, and the cost of the precomputation
depends on the schema's features: a fixed set of fields in order, or an enum of strings, gives a
small deterministic state machine, while `anyOf` keeps branches open, `minLength` needs a counter
that tokens advance by varying amounts, and recursion needs a stack instead of a state number.
The features that survive that compilation are the features the engine supports. So the
practical rule is to read what the engine says it enforces and assume the rest is not enforced —
and keep validating, because a constraint silently not applied is indistinguishable from one
applied and satisfied.
4. That the shape is right, and almost nothing else. You have not learned that your whole schema
is being enforced: the engine compiled a subset, and a `pattern` or a length bound it quietly
dropped produces exactly the result you are looking at. You have not learned that the values are
right, which is Chapter 21's fourth layer and needs a measurement of correctness rather than of
shape. And you have not learned that the answers are as good as they were before you turned it
on, which is the failure this chapter is about — perfect format, worse answers — and which is
invisible to anybody measuring only validity. On the rate itself, two thousand clean calls does
entitle you to something: by the rule of three the format failure rate is under about one in six
hundred and seventy.
5. Two things, separately, because they fail independently. The validation failure rate, which
should now be very low and which still needs measuring, because it is what catches a schema
feature the engine did not compile and a reply truncated at the token cap. And task accuracy,
paired against the unconstrained version on the same cases with an interval on the difference,
because turning strict mode on is a change to what the model emits and therefore a change that
can move the answers. The question to ask them is simply whether they ran the evaluation set
before and after; if they ran it only after, they know the format is fixed and have no idea what
it cost. If the task needs working out rather than looking up, also ask whether the schema has a
field for the working, and whether it comes before the answer.

> **You understand this when** you can say in one sentence what a constraint does to the
> numbers, and name the thing a guaranteed format cannot tell you.
