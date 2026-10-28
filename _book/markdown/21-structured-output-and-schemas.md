# Structured Output and Schemas

Chapter 2 said that a shape check is what notices when a model's answer is not the answer your
code expected. This chapter is how you ask for a shape and how you check it, and it is the
shortest distance between a demo and a program.

*The problem.* The model gives me a paragraph when I need a field my code can read.

*The question.* How do you get output a program can act on, and what do you do on the occasions
when you do not get it?

## Why a Program Must Never Trust Prose

Start with the reason, because it is not "prose is untidy".

A paragraph has no contract. When your code reads *The sentiment is positive, with high
confidence*, it has to find the word "positive" somewhere in a sentence whose wording nobody
promised. That works until the model writes *mostly positive*, or *positive, though the second
half is negative*, or *I would call this positive*. Each of those contains the word. Two of them
mean something else.

**And the deeper reason is Chapter 9's.** The model produces one token at a time, each chosen
from a distribution over the vocabulary. Nothing in that machinery has a notion of *the format I
promised*. A reply that came out as clean JSON ninety-nine times came out that way because clean
JSON was the likeliest continuation ninety-nine times, not because anything enforced it. The
hundredth reply is not a bug in the model; it is the same unconstrained process arriving
somewhere else. Nor does turning the sampling off change it — at temperature zero the token
chosen is simply the highest-scoring one, and nothing in *that* enforces a format either. What
*can* constrain the choice is a provider's strict mode, which is the next section but one and
then Chapter 22.

So the rule, and it is the answer to give when asked:

**A program must never trust prose, because prose has no contract — your code would have to
guess what the words mean, and a guess that is right ninety-five times in a hundred is a defect
five times in a hundred.** What you want instead is a format narrow enough that a parser either
accepts it or tells you it did not, which converts an unbounded guessing problem into a check
with two outcomes.

> **Note:** This is not an argument that the model is unreliable and prose is bad. For a person
> reading the answer, prose is the right output and a schema would be worse. The rule is about
> what *code* consumes. Chapter 19 draws the same kind of line for streaming: who the consumer
> is decides what you can do with a partial reply.

## Asking for a Fixed Format

Asking is the easy half, and it is one of Chapter 18's four parts — the output format block.
Three things make it work.

**Give the shape, not a description of the shape.** Put the exact skeleton you want — the field
names, the types, a `null` where a value may be absent — in Chapter 18's **output format** block,
rather than a sentence about what the fields are. Keep the examples block for a worked
input-and-output pair, which is a different job: one shows the contract, the other shows what a
good answer looks like inside it.

**Say what to do when the answer is not available.** A model asked for a `confidence` field will
produce one whether or not it has any basis for it. If you want `null`, say `null`; otherwise you
have invited an invention and Chapter 16 says why you will get one.

**Ask for nothing but the format.** *Return only the JSON object, with no explanation and no code
fence.* You will still get code fences sometimes, which the last section of this chapter deals
with, but you get fewer.

> **Note:** The validator here is hand-written so that you can see what a schema check *is*,
> and so the lab needs nothing installed. The published standard for writing the same thing
> declaratively is **JSON Schema** — an object with `"type"`, `"properties"` and `"required"`,
> which is also the form a provider's strict mode expects, though each engine accepts its own
> subset of it. In production you declare the schema that way and let a library check it; what you do not do is skip the check because the
> library is not installed.

**And then there is the other way of asking**, which is to use a provider's own facility for
constraining output to a schema — a strict mode, where the format is enforced during generation
rather than requested in the prompt. That changes the odds considerably and it changes them in
ways worth understanding, including a case where it makes answers worse. **Chapter 22 is about
that**, and everything in this chapter applies whichever way you asked, because none of it
trusts the asking.

## A Schema Is a Contract Your Code Enforces

Here is a validator. It is about thirty lines, it has no dependencies, and writing one by hand
is worth doing once, because it makes plain what a **schema** actually is: a list of claims
about a value, tested in order, and enforced by you.

```python
import json

SCHEMA = {
    "sentiment":  {"type": str,   "allowed": {"positive", "negative", "neutral"}},
    "confidence": {"type": float, "min": 0.0, "max": 1.0},
    "reason":     {"type": str,   "max_len": 200},
}
```

Three fields, each with the claims you are prepared to enforce on it. And the function that
enforces them:

```python
def validate(text):
    """Return (ok, why). The first three layers, in order; it stops at the
    first failure. `e.msg` and `e.pos` are worth logging, but their wording
    changes between Python versions, so this returns a stable reason."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False, "not JSON"
    if not isinstance(data, dict):
        return False, f"not an object: {type(data).__name__}"
    for field, rule in SCHEMA.items():
        if field not in data:
            return False, f"missing field: {field}"
        v = data[field]
        if rule["type"] is float and type(v) is int:
            v = float(v)
        if type(v) is not rule["type"]:
            return False, f"{field}: wanted {rule['type'].__name__}, got {type(v).__name__}"
        if "allowed" in rule and v not in rule["allowed"]:
            return False, f"{field}: {v!r} not allowed"
        if "min" in rule and not rule["min"] <= v <= rule["max"]:
            return False, f"{field}: {v} outside {rule['min']} to {rule['max']}"
        if "max_len" in rule and len(v) > rule["max_len"]:
            return False, f"{field}: {len(v)} characters, limit {rule['max_len']}"
    extra = sorted(set(data) - set(SCHEMA))
    if extra:
        return False, f"unexpected: {extra}"
    return True, "ok"
```

**The use of `type()` rather than `isinstance()` is deliberate, and the place it matters is the
coercion line.** `type(v) is int` is what decides whether to promote an integer to a float, and
in Python `isinstance(True, int)` is true — so an `isinstance` version of that line turns a JSON
`true` into 1.0, which then passes the range check and is accepted as a confidence. By default
`json.loads` returns only exact built-in types, so `type()` costs nothing here and the one case
where the two differ is the one that would hurt. Do not tidy it.

And here are eleven replies of the kind you actually get, in the same file:

```python
REPLIES = [
    '{"sentiment": "positive", "confidence": 0.9, "reason": "battery"}',
    '```json\n{"sentiment": "positive", "confidence": 0.9, "reason": "ok"}\n```',
    'Sure! Here is the JSON:\n{"sentiment": "negative", "confidence": 0.8, "reason": "no"}',
    "{'sentiment': 'neutral', 'confidence': 0.5, 'reason': 'mixed'}",
    '{"sentiment": "positive", "confidence": 0.9, "reason": "ok",}',
    '{"sentiment": "Positive", "confidence": 0.9, "reason": "ok"}',
    '{"sentiment": "positive", "confidence": 90, "reason": "ok"}',
    '{"sentiment": "positive", "reason": "ok"}',
    '{"sentiment": "positive", "confidence": 0.9, "reason": "ok", "notes": "hm"}',
    '{"sentiment": "positive", "confidence": 0.9, "reason": "the review',
    '{"sentiment": "Positive", "confidence": 90, "reason": "ok"}',
]

if __name__ == "__main__":
    for i, r in enumerate(REPLIES, 1):
        ok, why = validate(r)
        print(f"  {i:2d}  {'OK ' if ok else 'BAD'}  {why}")
```

```text
   1  OK   ok
   2  BAD  not JSON
   3  BAD  not JSON
   4  BAD  not JSON
   5  BAD  not JSON
   6  BAD  sentiment: 'Positive' not allowed
   7  BAD  confidence: 90.0 outside 0.0 to 1.0
   8  BAD  missing field: confidence
   9  BAD  unexpected: ['notes']
  10  BAD  not JSON
  11  BAD  sentiment: 'Positive' not allowed
```

**One of eleven.** Ten failures, every one of them something a real model does, in nine
distinguishable ways — and the important thing about the list is not how long it is but how
*different* its entries are — the eleventh is the exception that makes the point, being replies
6 and 7 at once.

Replies 2 to 5 and 10 never reach the schema at all: they are not JSON. **Notice that all five
print the same reason**, because the status *not JSON* is all a parser gives you about the
category, while the five causes are completely different: a code fence, prose around the object,
single quotes, a trailing comma, and a reply that stopped mid-string. This is Chapter 19's point
about reading the error's body and not only its status, arriving in a new place. `json.loads`
raises a `JSONDecodeError` carrying `e.msg` and `e.pos`, and those are what you log.

> **Note:** The validator above deliberately does not *return* `e.msg`. The wording of a
> `JSONDecodeError` is the interpreter's, and it changes between Python versions — the trailing
> comma in reply 5 is reported differently on 3.12 and on 3.13 — so a message built from it
> would make this chapter's printed output depend on which Python you have. Log it; do not
> branch on it, and do not show it to a user.

Reply 10 is the one to look at twice, because an unterminated string is usually not a formatting
mistake — it is a reply that hit the token cap, which Chapter 13 calls a guillotine rather than a
budget. Your validator reports *not JSON* and is telling you the truth while burying the cause,
so read the response's own **finish reason** as well.

Replies 6 to 9 and 11 are JSON, and they are the ones worth the chapter. `"Positive"` is valid
JSON, the right type, in the right field, and not a value your code can use. `90` is a plausible
confidence on a scale nobody specified. Reply 8 simply left a field out. Reply 9 added one. And
reply 11 has *both* of reply 6's and reply 7's faults, which is why it reports only the first:
a validator that stops at the first failure tells you the first thing wrong, not every thing
wrong.

> **Warning:** Reply 9 is a policy decision disguised as a failure, and you have to make it
> deliberately. Rejecting unexpected fields catches a model that is drifting away from your
> format, and it breaks the day you add a field and an old consumer sees it. Accepting them
> lets you add fields freely, and it lets an invented `"confidence_explanation"` through
> unnoticed for a year. Pick one, write down why, and apply it everywhere.

## The Four Layers, and Which Two You Get for Free

The validator above checks a stack of claims, and it is worth naming the stack — the
**validation layers** — because the top of it is not a validation problem at all.

| Layer | Question | Who answers it |
|---|---|---|
| 1 | Does it parse? | `json.loads` |
| 2 | Is it the right shape? | Your schema |
| 3 | Are the values possible? | Your schema, if you wrote the ranges |
| 4 | Are the values *true*? | Nothing on this page |

**Layers 1 and 2 are mechanical and you should never skip them.** Layer 3 is mechanical too, and
it is the one people leave out: a `confidence` field with no range, a `quantity` with no upper
bound, a date with no sanity check. Reply 7 passes layers 1 and 2 and fails 3, and it took one
line of schema to catch.

**Layer 4 is a different activity.** Take a reply that calls a review positive with a confidence
of 0.95 and a reason of `"praises the battery"`, about a review whose whole complaint is the
battery. It is perfectly valid and completely wrong. No schema can see that, and a stricter schema
will not help. Chapters 30 and 31 are where measuring *correctness* lives, and Chapter 31 in
particular is where a judgement of content gets built and checked.

**So say this part out loud when asked**, because it is the distinction that separates somebody
who has run this in production from somebody who has read about it: **a schema check tells you
the answer is shaped like an answer. It does not tell you the answer is right, and the two
failures need completely different machinery.**

## Measuring How Often It Fails

You cannot decide what to do about validation failures until you know the rate, and the rate is
a proportion — which Chapter 20 has already given you the tools for. Its bootstrap works here
unchanged.

```python
import random

def interval(results, trials=10_000):
    """Chapter 20's bootstrap, on a failure rate."""
    n = len(results)
    rates = []
    for _ in range(trials):
        s = [results[random.randrange(n)] for _ in range(n)]
        rates.append(sum(s) / n)
    rates.sort()
    return rates[int(0.025 * trials)], rates[int(0.975 * trials)]

TRUE_RATE = 0.02        # 1 reply in 50 fails validation

random.seed(21)
for n in (40, 200, 2_000):
    failures = [1 if random.random() < TRUE_RATE else 0 for _ in range(n)]
    seen = sum(failures)
    lo, hi = interval(failures)
    print(f"  {n:5d} replies: {seen:3d} failed = {seen/n:.3f}"
          f"   interval {lo:.3f} to {hi:.3f}")

print("\n  and when you have seen no failure at all:")
lo, hi = interval([0] * 40)
print(f"    40 replies, 0 failed: bootstrap says {lo:.3f} to {hi:.3f}")
for n in (40, 200, 2_000):
    print(f"    0 failures in {n:5d}  ->  rule of three: up to {3/n:.3f}")
```

```text
     40 replies:   1 failed = 0.025   interval 0.000 to 0.075
    200 replies:   5 failed = 0.025   interval 0.005 to 0.050
   2000 replies:  31 failed = 0.015   interval 0.011 to 0.021

  and when you have seen no failure at all:
    40 replies, 0 failed: bootstrap says 0.000 to 0.000
    0 failures in    40  ->  rule of three: up to 0.075
    0 failures in   200  ->  rule of three: up to 0.015
    0 failures in  2000  ->  rule of three: up to 0.002
```

**Forty replies tell you almost nothing.** One failure in forty reads as two and a half per cent,
and the interval runs from zero to seven and a half. The lower end is an artefact rather than a
finding: you *saw* a failure, so the rate is certainly not zero, and the bootstrap only reaches
zero because thirty-six per cent of resamples of a list with one `1` in it happen to contain no
`1` at all. What forty replies cannot tell you is whether the rate is one in four hundred or one
in thirteen, and those two need different plans. Two thousand replies put it between 1.1 and 2.1
per cent, which is a number you can plan around.

**And now the part Chapter 20 did not need, because this chapter has rare events and that one
did not.** Look at the zero-failure line. The bootstrap returns 0.000 to 0.000, and it is not
being modest — it is resampling a list of forty zeros, and no amount of resampling a list with
no failures in it will ever produce one. **The bootstrap cannot see a failure it has never
observed.** Quoting that interval would be the most confident possible way of being wrong.

What you use instead is one line of arithmetic. If the true rate were `\(p\)`{=latex}, the chance
of seeing no failure in `\(n\)`{=latex} tries is `\((1-p)^n\)`{=latex}, and that is above five per
cent — so still quite possible — for any `\(p\)`{=latex} up to

```{=latex}
\[ 1 - 0.05^{1/n} \;=\; 1 - 0.05^{1/40} \;=\; 0.072 \]
```

which is where the **rule of three** comes from: `\(\ln 20 = 2.996\)`{=latex}, so the bound is
about `\(3/n\)`{=latex}, and `\(3/40 = 0.075\)`{=latex} against the exact 0.072. Clean runs on
forty replies are consistent with one reply in thirteen failing — fourteen on the exact bound,
thirteen on the rule of three, and the rule of three is the one you will quote.

**Do not read the two 0.075s as the same number.** The bootstrap's upper end for *one* failure in
forty is 0.075, and the rule of three for *zero* failures in forty is also 0.075, and they are
different quantities that happen to coincide at this sample size. A rate on forty replies moves
in steps of 1/40, and for one failure in forty the 97.5th percentile lands on the third of those
steps — `\(P(X \le 2) = 0.922\)`{=latex} and `\(P(X \le 3) = 0.983\)`{=latex}, so 3/40 is
where it has to fall, whatever the seed. Three fortieths is also what the rule of three gives.
Change the forty and they part company.

> **Tip:** This is the arithmetic to reach for whenever somebody says a thing has never
> happened. It converts "we have never seen it" into a number, and the number is usually larger
> than the person expects. If you need to be sure a failure rate is under one in a thousand, you
> need about three thousand clean runs, and there is no way to talk your way out of it.

## What to Do With a Failure

Four options, and they are in order of how much you should like them.

**Reject.** The reply failed, so you do not use it. For anything where a wrong answer is worse
than no answer, this is the right default and the rest of this section is a distraction.

**Retry — and know what your temperature setting does to that.** Above temperature zero the
model samples, so a second attempt is a genuinely different draw and a plain retry often works.
**At temperature zero it is not.** Greedy decoding takes the highest-scoring token every time,
so a retry is no longer a fresh draw from a distribution and retrying unchanged is close to
paying twice for one answer. Close to, not exactly: Chapter 13 is clear that temperature zero is
not a guarantee either, for reasons that have nothing to do with sampling. What you cannot count
on is the retry *helping*. Structured extraction is usually run at temperature zero, which makes this the
common case rather than the exception, so **change something in the retry**: send the validator's
own message back, because *missing field: confidence* is a far more useful instruction than *that
was wrong*. Cap the attempts and count them either way, or you have built an expensive loop that
hides a broken prompt.

**Repair**, but only the kinds that cannot change what the reply means. Three edits qualify:

```python
import re
from check import REPLIES, validate

def repair(text):
    """Three edits that cannot change what the JSON means."""
    t = text.strip()
    t = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", t)      # a fenced code block
    i, j = t.find("{"), t.rfind("}")                   # prose either side
    if i != -1 and j > i:
        t = t[i:j+1]
    t = re.sub(r",(\s*[}\]])", r"\1", t)               # a trailing comma
    return t

before = after = 0
for n, r in enumerate(REPLIES, 1):
    ok0, _ = validate(r)
    ok1, why = validate(repair(r))
    before += ok0
    after += ok1
    mark = "ok" if ok1 else "still bad"
    moved = " <- repaired" if ok1 and not ok0 else ""
    print(f"  {n:2d}  {mark:9s} {why if not ok1 else ''}{moved}")
print(f"\n  {before}/{len(REPLIES)} valid as sent,"
      f" {after}/{len(REPLIES)} after repair")
```

```text
   1  ok        
   2  ok         <- repaired
   3  ok         <- repaired
   4  still bad not JSON
   5  ok         <- repaired
   6  still bad sentiment: 'Positive' not allowed
   7  still bad confidence: 90.0 outside 0.0 to 1.0
   8  still bad missing field: confidence
   9  still bad unexpected: ['notes']
  10  still bad not JSON
  11  still bad sentiment: 'Positive' not allowed

  1/11 valid as sent, 4/11 after repair
```

One in eleven becomes four in eleven, and every one of those three edits removes something that
was never part of the data: a code fence, text outside the braces, a comma JSON does not allow.
None of them touches a value.

**Two of the three are doing the work.** Disable the fence rule and the count is still four,
because the brace slice already throws away the fence along with everything else outside the
object. The fence rule earns its place only when a reply fences something that is not an object —
a bare array, or an object with a comment after the closing brace — and it costs one line, so
keep it. But do not count edits and assume each one bought you something; disable them one at a
time and look.

One more thing to notice before the next part. Reply 7's message says `90.0` where the model
actually sent `90`. That is the int-to-float coercion showing in the output, and if you log the
validator's message beside the raw reply, somebody will one day compare the two and wonder which
is wrong. Log the raw text as well as the reason.

**Now look at what is left, because the line between repair and invention runs straight through
it.** Reply 4 uses single quotes, and `ast.literal_eval` would parse it happily — which is why
you should not, because you would have quietly accepted Python literals from a model asked for
JSON, and a Python literal can contain things JSON cannot. Reply 6 could be lower-cased. Reply 7
could be divided by a hundred. Both of those are **guesses about what the model meant**, and
both will be right most of the time, which is exactly what makes them dangerous: you will not
find out about the time `90` meant ninety.

So the line is: **repair the envelope, never the contents.** If the fix requires you to know what
the model intended, it is not a repair, and the honest version of it is a retry or a rejection.

**Record.** Whatever you do with the reply, keep the failure: the raw text, the validator's
message, and the input that produced it. That file is how you find out that eighty per cent of
your failures are one prompt and one field, which is a prompt you can fix — and Chapter 30 is
the discipline of actually reading them.

> **Warning:** The failure you must never choose is the fifth one, which is to catch the
> exception, log a line nobody reads, and carry on with a default value. That turns a loud
> failure into a wrong answer with no fingerprints, and the field it silently sets to `"neutral"`
> will be in a report somebody makes a decision from.

## Lab: Nine Ways to Fail, and What to Do About Them

Three programs, pure Python, nothing to install, every number reproducible from the seed. Forty
minutes, and there is a key for every step. **Work in a new empty folder**, because `repair.py`
imports from `check.py` and a stale copy of either will quietly change your answers.

**Step 1.** Save the schema, the validator and the eleven replies as `check.py` and run it.

*Expected result:* exactly the eleven lines in the chapter — one `OK` and ten `BAD`. The reasons
are stable across Python versions because the validator does not pass the interpreter's own
parse message through.

**Step 2.** Reply 7 is `"confidence": 90`. Delete the `"min"` and `"max"` from the schema's
`confidence` rule and run it again. What happens, and which layer did you just remove?

*Expected result:* reply 7 now passes, so the count goes to two of eleven. You removed layer 3,
the check that the values are *possible*, and the result is a program that will cheerfully act
on a confidence of ninety. This is the layer people leave out, and it costs one line to put
back. Reply 11 still fails, because it meets the enum check first.

**Step 3.** Now delete the `type` check as well, and run it again. Then look at reply 11 and say
what the validator has not told you.

*Expected result:* reply 7 still passes and nothing else changes, because every other reply fails
earlier — at the parse, at a missing field, at the enum or at the extra field. Reply 11 is the
point of the step: it has `"Positive"` *and* a confidence of 90, and the validator reports only
the enum, because it returns at the first failure. So a clean second run after a fix is not
evidence the reply was nearly right; it is evidence you have reached the next problem. If you
want all of them at once, collect the failures into a list instead of returning — which is
worth doing for a report and not worth doing in the request path, where the first failure is
already enough to reject on.

**Step 4.** Put `check.py` back the way it was first — both the `type` check and the `min` and
`max` you deleted in steps 2 and 3 — because `repair.py` imports from it and will report a
different answer against a weakened schema. Then save the repair program as `repair.py` in the
same folder and run it.

*Expected result:* the chapter's eleven lines and `1/11 valid as sent, 4/11 after repair`. If
you get `2/11` and `5/11`, you did not restore the schema and reply 7 is passing a range check
that is no longer there. If you get an import error, `check.py` must be in the same directory;
if you see check.py's own eleven lines first, its demo loop is not under
`if __name__ == "__main__":`.

**Step 5.** Add a fourth repair that lower-cases the `sentiment` value, and run it again. How
many pass now, and what did you just agree to?

*Expected result:* five of eleven — reply 6 joins them, and reply 11 does not, because
lower-casing its sentiment only moves it on to its second fault. What you agreed to is that
`"Positive"` and
`"positive"` mean the same thing, which they almost certainly do. But you have moved from
repairing the envelope to editing the contents, and the next request of this kind will be to map
`"very positive"` onto `"positive"`, which is a different claim entirely. If you want this, put
it in the schema as a case-insensitive enum rather than in the repair step, so it reads as a
decision about the contract instead of a patch.

**Step 6.** Save the rate program as `rate.py` and run it. Then explain why the forty-reply
interval contains zero when you know the true rate is 0.02.

*Expected result:* the chapter's figures. The interval contains zero because one failure in
forty is also what you would often see if the rate were very small, and the bootstrap is
resampling a list with a single 1 in it — plenty of resamples contain no 1 at all. Knowing the
true rate is a luxury of the simulation; the interval is what you would have without it.

**Step 7.** Set `TRUE_RATE` to 0.0 and run it. What does the bootstrap report for all three
sample sizes, and what should you report instead?

*Expected result:* 0.000 to 0.000 at every size, because there is no failure in any of the lists
to resample. You should report the rule-of-three bound for the size you ran: up to 0.075 at
forty, 0.015 at two hundred, 0.002 at two thousand. "We saw no failures" and "the failure rate
is zero" are different sentences and only the first is true.

**Step 8.** You need confidence that a format failure happens less than once in five hundred
replies. How many clean runs does that take, and what do you do if you cannot afford them?

*Expected result:* the rule of three inverted — `\(3/n = 1/500\)`{=latex} gives
`\(n = 1500\)`{=latex} clean runs. If you cannot afford fifteen hundred, the answer is not to
run fewer and claim the same thing; it is to stop needing the guarantee. Make the failure cheap
instead: reject and retry, cap the attempts, record every failure, and alarm on the rate. A
system that handles a one-in-fifty failure gracefully does not need to prove it is one in five
hundred.

**Step 9.** A colleague's extraction pipeline parses the model's reply with a regular expression
that pulls out the first number it finds, and it has worked for three months. Name three ways it
fails, and what you would replace it with.

*Expected result:* it finds a number in a date, a citation, or a quantity in the input that the
model repeated; it finds the right number in the wrong units because nothing fixed the units;
and it silently picks up the first of two numbers when the model starts answering in a
sentence — and because every one of those produces *a number*, nothing ever raises. The
replacement is a field with a name, a type, and a range, in a schema, validated on every reply,
with failures recorded. Three months of working is not evidence of a contract; it is evidence
that the likeliest continuation has been stable.

## Summary, Key Terms, and Review Questions

### Summary

**A program must never trust prose, because prose has no contract**: your code would have to
guess what the words mean, and a guess that is right ninety-five times in a hundred is a defect
five times in a hundred. The reason is Chapter 9's — a reply that was clean JSON ninety-nine
times was clean because that was the likeliest continuation, not because anything enforced it.
So ask for a fixed format: show the exact shape rather than describing it, say what to do when a
value is unavailable, and ask for nothing but the format. A provider's **strict mode** changes
the odds and Chapter 22 is about it; nothing in this chapter depends on how you asked. **A
schema is a contract your code enforces**, and a hand-written validator makes plain what it is:
a list of claims tested in order. Of eleven realistic replies, one passed. Five were not JSON at
all, and **all five report the same reason**, because a parse status names the category and not
the cause — one of them was an unterminated string, which usually means the token cap rather than
a formatting slip, so read the finish reason too. The other five were valid JSON and unusable:
`"Positive"` for an enum, `90` for a confidence, a missing field, an extra one, and one reply
with two faults that reports only the first. Validation has
**four layers** — it parses, it is the right shape, the values are possible, the values are
true — and the first three are mechanical while the fourth is a different activity belonging to
chapters 30 and 31. **A schema check tells you the answer is shaped like an answer; it does not
tell you the answer is right.** Measure the failure rate with Chapter 20's bootstrap: one
failure in forty gives an interval of 0.000 to 0.075, whose lower end is an artefact of
resampling a single `1` rather than evidence that the rate might be zero, while two thousand
replies place it between 0.011 and 0.021. But **the bootstrap cannot see a failure it has never
observed** — on forty clean replies it reports 0.000 to 0.000 — so for a rare event use **the
rule of three**: zero failures in `\(n\)`{=latex} tries leaves the rate as high as
`\(3/n\)`{=latex}, which at forty is one reply in thirteen. Then handle the failures: **reject**
by default, **retry** with the validator's own message fed back, **repair the envelope and never
the contents** (three meaning-preserving edits took one of eleven to four of eleven, and only two of the three
did any of the work), and **record**
every failure with its input. The option never to choose is the silent default.

### Key Terms

| Term | Meaning |
|---|---|
| **Schema** | The list of claims your code makes about a reply — fields, types, allowed values, ranges — and enforces on every one. A contract you check, not a request you hope was honoured |
| **Validation layers** | Parses / right shape / values possible / values true. The first three are mechanical; the fourth needs a judgement and belongs elsewhere |
| **Rule of three** | With no failures in `\(n\)`{=latex} tries, the rate can still be about `\(3/n\)`{=latex}. What to use when a bootstrap has no failure to resample |
| **Repair** | Editing a reply so it parses, restricted to things that were never part of the data: a code fence, text outside the braces, a comma JSON disallows |
| **Finish reason** | The response's own statement of why generation stopped. What distinguishes a truncated reply from a malformed one |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Why not prose | No contract, so your code guesses. Right 95 times in 100 is a defect 5 times in 100 |
| The four layers | Parses · right shape · values possible · values true. Only the first three are free |
| Rule of three | 0 failures in `\(n\)`{=latex} → the rate may be `\(3/n\)`{=latex}. Exactly, `\(1 - 0.05^{1/n}\)`{=latex} |
| 0 in 40 | Consistent with a 7.5 per cent failure rate |
| The repair line | Repair the envelope, never the contents. Needing to know what the model meant makes it a retry |
| Failure options | Reject · retry · repair · record. Never a silent default |

### Review Questions

1. Why must a program never trust prose?
2. You are asking for JSON. How do you measure how often you do not get it, and what do you do with the failures?
3. Your validator has passed every reply for a month. What can you conclude?
4. A reply is valid JSON, matches your schema, and is wrong. What caught it, and what should have?
5. When is repairing a reply acceptable, and when is it not?

### Review Answers

1. Because prose has no contract. To act on a paragraph your code has to locate meaning inside
wording that nobody promised — it finds "positive" in *mostly positive* and in *positive, though
the second half is negative*, and two of those mean something else. Underneath that is the
mechanism from Chapter 9: the model emits one token at a time from a distribution, and nothing
in it has a notion of the format you asked for. A reply that arrived as clean JSON ninety-nine
times did so because that was the likeliest continuation, not because anything enforced it, so
the hundredth is the same unconstrained process arriving somewhere else rather than a
malfunction, and that holds at temperature zero too, where the token taken is just the
highest-scoring one. A fixed
format replaces the guess with a parser that either accepts the reply or tells you it did not.
And the limit is worth volunteering: this is a rule about what code consumes. For a person
reading the answer, prose is the right output.
2. Measure it as a proportion, with an interval, because the raw rate is misleading at small
numbers: one failure in forty looks like two and a half per cent and the bootstrap interval runs
from 0.000 to 0.075, containing zero, while two thousand replies place the rate between 0.011
and 0.021. The thing to add, because it is where people go wrong, is that **a bootstrap cannot
see a failure it has never observed** — forty clean replies give an interval of 0.000 to 0.000,
which is the most confident possible way of being wrong — so for a run with no failures you use
the rule of three: the rate may still be about `\(3/n\)`{=latex}, one reply in thirteen at forty
tries. For the failures themselves there are four options in order of preference: **reject**,
which is right whenever a wrong answer is worse than no answer; **retry**, which works unusually
well above temperature zero, where sampling makes the second attempt a genuinely different draw,
and is worth nothing at temperature zero unless you change something — so feed the validator's
own message back; **repair**, strictly limited to edits that
cannot change meaning — a code fence, prose outside the braces, a trailing comma, which together
took one of eleven replies to four of eleven; and **record**, always, with the raw text and the input,
because the failures cluster and the clusters are fixable. The fifth option, catching the error
and substituting a default, is the one to name as unacceptable.
3. That the rate is low, not that it is zero, and you can put a number on it. If the month was
forty replies, the rule of three says the rate could still be seven and a half per cent — one in
thirteen. If it was two thousand, you are entitled to about one in six hundred and seventy. The
bootstrap is no help here and will tell you the rate is exactly zero, because it has no failure
to resample. The second thing to conclude is narrower than it sounds: a validator that has never
fired has also never been tested, so you do not know it works. Feed it a deliberately bad reply
and watch it fail before you trust its silence.
4. Your schema caught nothing, because there was nothing for it to catch: layers one, two and
three were all satisfied. What should have caught it is a measurement of *correctness*, which is
a different activity from validation and needs different machinery — a check or a judge over a
set of cases with known answers, built and validated as chapters 30 and 31 describe. The useful
way to say this is that a schema check tells you the answer is shaped like an answer. Tightening
the schema will not help, and the instinct to tighten it after a wrong-but-valid answer is the
mistake worth naming.
5. Acceptable when the edit removes something that was never part of the data and could not
change what the reply means: a surrounding code fence, text outside the braces, a comma JSON
does not permit. Not acceptable when the edit requires you to know what the model intended —
lower-casing an enum value, dividing a number by a hundred because you think it was a
percentage, or parsing single-quoted output with `ast.literal_eval`, which quietly accepts
Python literals from a model you asked for JSON. Those are guesses, they are right most of the
time, and being right most of the time is what hides the case where `90` meant ninety. The rule
is to repair the envelope and never the contents; if you want case-insensitive values, that
belongs in the schema as part of the contract, not in a patch applied after the fact.

> **You understand this when** you can say what a schema check does *not* tell you, and put a
> number on a failure you have never seen.
