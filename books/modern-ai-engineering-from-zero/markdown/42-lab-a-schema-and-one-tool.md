# Lab: A Schema and One Tool

Chapter 21 built a validator and ran it against eleven replies written out by hand. Chapter 22
built a decoder and masked its tokens. Chapter 23 walked the five steps of a tool call over six
proposals, also written out by hand. All three said, in their own words, that the measurement was
somebody else's job. This is that job: the same schema asked for two ways against a real model,
the failure rate measured on real replies, and one tool a real model proposes while your code
refuses it.

*The problem.* I want output my code can trust, and one action the model can ask for but not take.

*The question.* What does a schema actually buy you when the replies are real — and what is left
over that no schema can reach?

> **Note:** As in chapters 40 and 41, the `text` blocks are one real run, and what you should
> expect to reproduce differs by figure. **Steps 3 and 4 came back identical on two independent
> runs of their one hundred and twenty calls** — the same zero failures, the same 0.900 both ways,
> the same two cases wrong — and **step 4's narrow-schema table on three**, down to the one reply
> that returned a currency symbol. Step 5's first column held across three runs as well. **Two
> things moved.** The `order_id` in step 6's view of the log is invented by the model and
> deliberately unconstrained by this lab, so it was a copied order number twice and a placeholder
> word once. And separately, on one run m4's cell in step 5's `enforced` column came back
> `HL-8815-A` rather than `HL-5512-A` — a different invented code, refused for the same reason.
> Treat the proposals as one sample of what a model does with an under-specified field, read your
> own, and expect the shape rather than the characters.

## Step 1: The Schema, and the Validator You Keep Anyway

Make a folder, put the corpus in it, and set the key:

```text
  mkdir -p ~/sandbox/ch42 && cd ~/sandbox/ch42
  python3 -m venv .venv && source .venv/bin/activate
  cp -r <where you unpacked the book's labs>/corpus .
  export OPENAI_API_KEY="sk-..."
```

Every program takes the corpus from `./corpus`, or from `CORPUS` if you put it elsewhere, and
nothing is installed: the standard library is enough for the last time in this part.

> **Note:** What this lab costs before you run it. It makes 164 calls: 2 in step 2, then 120 in
> step 3 and 2 more in its truncation check, 20 in step 4, and 20 in step 5 — a 2-call probe and
> then three ways of constraining one argument over six messages. Each sends one corpus
> document of a few hundred tokens, and the whole lab comes to about a penny on a small model. The
> figure to watch is the same product as chapter 41's — cases times modes times trials — and step
> 3 is 20 by 2 by 3. Forty-five minutes, most of it reading output.

The task is extraction, and the schema has three fields chosen so that each one can fail in a
different way: a string with a length limit, a string from a closed set, and a boolean.

```python
"""The schema, the validator, and twenty cases to ask about.

The validator is chapter 21's, unchanged in kind: a list of claims
tested in order, stopping at the first failure. The cases are the
shape chapter 41 used, on purpose - the point here is the FORMAT,
so the answers being familiar is a help.
"""

import json
import os
import pathlib

CORPUS = pathlib.Path(os.environ.get("CORPUS", "corpus")) / "docs"

UNITS = ["days", "hours", "pounds", "pence", "years", "none"]

SCHEMA = {
    "value": {"type": str,  "max_len": 20},
    "unit":  {"type": str,  "allowed": set(UNITS)},
    "found": {"type": bool},
}

# The same three fields as a JSON Schema, which is what a provider's
# strict mode expects. Chapter 21 named this form; chapter 22 owns
# what an engine does with it.
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "value": {"type": "string", "maxLength": 20},
        "unit":  {"type": "string", "enum": UNITS},
        "found": {"type": "boolean"},
    },
    "required": ["value", "unit", "found"],
    "additionalProperties": False,
}

#  id,  question, document, expected value, expected unit
CASES = [
 ("c01", "How many days do I have to return a standard item?",
  "returns-standard", "30", "days"),
 ("c02", "How many days do I have to return a clearance item?",
  "returns-clearance", "14", "days"),
 ("c03", "Within how many days of the goods arriving is a refund issued?",
  "refunds-policy", "14", "days"),
 ("c04", "What is the goodwill cap per order, in pounds?",
  "refunds-policy", "20", "pounds"),
 ("c05", "What is the standard delivery charge on an order under 40 pounds?",
  "delivery-fees", "3.99", "pounds"),
 ("c06", "What is the named-day delivery charge?",
  "delivery-fees", "5.99", "pounds"),
 ("c07", "What is the next-day delivery charge?",
  "delivery-fees", "7.99", "pounds"),
 ("c08", "What is the flat charge for a two-person delivery?",
  "delivery-fees", "19.99", "pounds"),
 ("c09", "What is the surcharge for the Scottish Highlands and islands?",
  "delivery-exceptions", "9.50", "pounds"),
 ("c10", "What is the surcharge for Northern Ireland?",
  "delivery-exceptions", "6.50", "pounds"),
 ("c11", "How many hours do I have to report cosmetic damage on delivery?",
  "damaged-on-arrival", "48", "hours"),
 ("c12", "How many days is a return postage label valid for?",
  "return-postage-labels", "21", "days"),
 ("c13", "How many days is a repair itself covered for?",
  "warranty-full", "90", "days"),
 ("c14", "How many years does the warranty run for?",
  "warranty-full", "2", "years"),
 ("c15", "How much does Harbour Plus cost per year, in pounds?",
  "plan-harbour-plus", "29", "pounds"),
 ("c16", "How many years of warranty does Harbour Plus give?",
  "plan-harbour-plus", "3", "years"),
 ("c17", "For how many years are order records kept?",
  "data-and-privacy", "7", "years"),
 ("c18", "How much does a replacement limescale filter cost, in pounds?",
  "product-kettle-hl-2208", "4.50", "pounds"),
 ("c19", "How many working days can a bank transfer refund take?",
  "refund-to-a-closed-card", "10", "working days"),
 ("c20", "Within how many working days does stage two of a complaint "
  "get a reply?", "complaints-process", "10", "working days"),
]


def validate(text):
    """Return (ok, why). Chapter 21's four layers, the first three."""
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
        if type(v) is not rule["type"]:
            return False, (f"{field}: wanted {rule['type'].__name__},"
                           f" got {type(v).__name__}")
        if "allowed" in rule and v not in rule["allowed"]:
            return False, f"{field}: {v!r} not allowed"
        if "max_len" in rule and len(v) > rule["max_len"]:
            return False, (f"{field}: {len(v)} characters,"
                           f" limit {rule['max_len']}")
    extra = sorted(set(data) - set(SCHEMA))
    if extra:
        return False, f"unexpected: {extra}"
    return True, "ok"


if __name__ == "__main__":
    print(f"  {len(CASES)} cases, {len(SCHEMA)} fields,"
          f" {len(UNITS)} units allowed")
    missing = [c[2] for c in CASES
               if not (CORPUS / f"{c[2]}.md").exists()]
    print(f"  documents missing from the corpus: {len(missing)}")

    bad = [c for c in CASES if c[4] not in SCHEMA["unit"]["allowed"]]
    print(f"\n  cases whose true unit the enum cannot hold: {len(bad)}")
    for cid, q, doc, val, unit in bad:
        print(f"    {cid}  the document says {unit!r}, and the")
        print(f"         enum has no member for it")
```

```text
  20 cases, 3 fields, 6 units allowed
  documents missing from the corpus: 0

  cases whose true unit the enum cannot hold: 2
    c19  the document says 'working days', and the
         enum has no member for it
    c20  the document says 'working days', and the
         enum has no member for it
```

**The last four lines are the chapter, and they are already visible before a single call has been
made.** I wrote the unit list without looking at the corpus and it looks complete: days, hours,
pounds, pence, years, and a member for an answer with no unit. The corpus states two of these
twenty figures in [**working days**]{.noindex} — a bank transfer takes *up to 10 working days*, and stage two
of a complaint gets a reply *within ten working days* — and *working days* is not *days*. Ten
working days is a fortnight.

So the schema cannot hold the right answer on two of the twenty cases, and no *validation*
failure will ever report it. Only step 4's measurement of the answers will, which is what step 4
is for. Chapter 22 names this as one of the two ways a strict
format makes an answer worse, and calls it the commoner one and the one that is arithmetic rather
than subtlety. It is also, as the next three steps show, not a fact about strictness at all.

> **Note:** The program's last check is the cheap one worth copying: it opens every document a
> case names before anything is asked. Chapter 41's build step asserted that each expected answer
> appears in its own document; this one asserts only that the document exists, because here the
> expected answers are in the chapter and the thing that goes stale is a filename.

## Step 2: Ask for the Format, and Measure What You Got

The client is chapter 40's, and the only new thing in it is the second way of asking. Note what
the two ways share: the same prompt, the same model, the same temperature, the same cases. The
format instruction stays in the prompt even when the provider is enforcing the schema, because
the two are not alternatives — one tells the model what you want and the other stops it emitting
anything else.

```python
"""The client, and the two ways of asking for a format.

Chapter 40 built this shape: key from the environment, model pinned
to a dated snapshot, one timeout, no retry. What is new is the second
mode, where the format is enforced during generation rather than
requested in the prompt - chapter 22 owns how that works.
"""

import json
import os
import urllib.error
import urllib.request

from schema import CORPUS, JSON_SCHEMA

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 120

PROMPT = (
 "Answer the question using only the document below.\n"
 'Reply with JSON only, in exactly this shape and nothing else:\n'
 '{{"value": "<the value, digits only, no unit>",\n'
 '  "unit": "<one of: days, hours, pounds, pence, years, none>",\n'
 '  "found": <true or false>}}\n'
 "No explanation and no code fence.\n\n"
 "Document:\n{doc}\n\nQuestion: {q}"
)


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def post(body):
    req = urllib.request.Request(URL, json.dumps(body).encode(), {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def ask(question, doc_id, strict=False, max_tokens=80):
    """Return (text, finish_reason, model). `strict` is the provider's
    own facility; everything else is identical between the two."""
    doc = (CORPUS / f"{doc_id}.md").read_text()
    body = {
        "model": MODEL,
        "messages": [{"role": "user",
                      "content": PROMPT.format(doc=doc, q=question)}],
        "max_tokens": max_tokens, "temperature": 0,
    }
    if strict:
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": "answer", "strict": True,
                            "schema": JSON_SCHEMA},
        }
    d = post(body)
    c = d["choices"][0]
    return c["message"]["content"], c["finish_reason"], d["model"]


if __name__ == "__main__":
    from schema import CASES, validate
    cid, q, doc, val, unit = CASES[0]
    print(f"  {cid}: {q}\n  expected {val!r} {unit!r}\n")
    for mode in (False, True):
        try:
            text, why, model = ask(q, doc, strict=mode)
        except urllib.error.HTTPError as e:
            detail = json.load(e)["error"]["message"]
            print(f"  strict={mode}: HTTP {e.code}")
            print(f"    {detail[:120]}")
            continue
        ok, reason = validate(text)
        print(f"  strict={mode}  {'OK ' if ok else 'BAD'} {reason}")
        print(f"    finish={why}  model={model}")
        print(f"    {text[:70]!r}")
```

```text
  c01: How many days do I have to return a standard item?
  expected '30' 'days'

  strict=False  OK  ok
    finish=stop  model=gpt-4o-mini-2024-07-18
    '{"value": "30","unit": "days","found": true}'
  strict=True  OK  ok
    finish=stop  model=gpt-4o-mini-2024-07-18
    '{"value":"30","unit":"days","found":true}'
```

**Two things in that output are worth stopping on, and one of them is an absence.**

The replies differ, and only in whitespace. The asked reply has a space after each colon and the
enforced one has none, which is a hint about where each came from: one is the model writing JSON
the way JSON is usually written, and the other is a decoder whose grammar, on this path, admits
no optional whitespace — which is this engine's choice and not a property of strict grammars. The
same provider's *tool* path returns whitespace under enforcement, as step 5's log shows.

And the `model` field says `gpt-4o-mini-2024-07-18`, which is the snapshot the request pinned.
Chapter 40 is why that is printed rather than assumed, and chapter 54 owns what happens when a
name moves under you.

The absence is the error branch. The program catches an `HTTPError` and prints the provider's own
message, because the first thing you want to know about a strict mode is **which parts of your
schema the engine will accept at all**. This schema was accepted whole, including the `maxLength`
that step 4 turns into a weapon. A schema the engine will not compile fails loudly at this point,
which is the pleasant case; chapter 22's warning is about the other one.

## Step 3: Enforce the Format, and Measure the Same Thing

Now the measurement both of the earlier chapters deferred. Twenty cases, two modes, three trials,
and every reply written to a file before any arithmetic touches it.

```python
"""Ask twenty cases both ways, record every reply, and measure.

Two measurements, because chapter 22 says they fail independently:
the validation failure rate here, and what the format cost the
answers in task.py. Every reply is written to replies.tsv first -
the measuring reads the file, so a re-run of the arithmetic costs
nothing and the raw text survives the arithmetic. The model column
is there because every figure below is a figure about one snapshot.
"""

import pathlib
import random

from ask import ask
from schema import CASES, validate

LOG = pathlib.Path("replies.tsv")
SEED = 42
TRIALS = 3


def run():
    rows = []
    for mode in ("asked", "strict"):
        for trial in range(1, TRIALS + 1):
            for cid, q, doc, val, unit in CASES:
                text, why, model = ask(q, doc, strict=(mode == "strict"))
                ok, reason = validate(text)
                rows.append((cid, mode, str(trial), "1" if ok else "0",
                             reason, why, model,
                             text.replace("\t", " ").replace("\n", " ")))
            print(f"  {mode} trial {trial}: {len(CASES)} calls done")
    LOG.write_text("case\tmode\ttrial\tvalid\treason\tfinish"
                   "\tmodel\ttext\n" +
                   "\n".join("\t".join(r) for r in rows) + "\n")
    print(f"  wrote {LOG}, {len(rows)} rows")


def rows():
    text = LOG.read_text().strip().split("\n")[1:]
    return [tuple(l.split("\t", 7)) for l in text]


def interval(marks, trials=10_000):
    """Chapter 20's bootstrap, on a failure rate."""
    rng = random.Random(SEED)
    n = len(marks)
    rates = sorted(sum(marks[rng.randrange(n)] for _ in range(n)) / n
                   for _ in range(trials))
    return rates[int(0.025 * trials)], rates[int(0.975 * trials)]


if __name__ == "__main__":
    if not LOG.exists():
        run()
    rs = rows()
    print(f"\n  validation failures, {len(CASES)} cases x {TRIALS}"
          f" trials:\n")
    for mode in ("asked", "strict"):
        fails = [0 if r[3] == "1" else 1 for r in rs if r[1] == mode]
        n, seen = len(fails), sum(fails)
        lo, hi = interval(fails)
        print(f"    {mode:7} {seen} of {n} failed = {seen/n:.3f}"
              f"   interval {lo:.3f} to {hi:.3f}")
        if seen == 0:
            print(f"            no failure seen, so that interval is")
            print(f"            a list of zeros resampled. The rule of")
            print(f"            three: up to {3/n:.3f}, one in"
                  f" {round(n/3)}.")
    print("\n  every reason given, both modes:\n")
    for mode in ("asked", "strict"):
        bad = sorted({r[4] for r in rs if r[1] == mode and r[3] == "0"})
        print(f"    {mode:7} {bad if bad else 'none'}")
```

```text
  asked trial 1: 20 calls done
  asked trial 2: 20 calls done
  asked trial 3: 20 calls done
  strict trial 1: 20 calls done
  strict trial 2: 20 calls done
  strict trial 3: 20 calls done
  wrote replies.tsv, 120 rows

  validation failures, 20 cases x 3 trials:

    asked   0 of 60 failed = 0.000   interval 0.000 to 0.000
            no failure seen, so that interval is
            a list of zeros resampled. The rule of
            three: up to 0.050, one in 20.
    strict  0 of 60 failed = 0.000   interval 0.000 to 0.000
            no failure seen, so that interval is
            a list of zeros resampled. The rule of
            three: up to 0.050, one in 20.

  every reason given, both modes:

    asked   none
    strict  none
```

**Nothing failed, either way, and that is the result rather than a disappointment.** The
**validation failure rate** is the proportion of real replies your schema rejects, and here it is zero out
of sixty on both modes. Four things follow, and the fourth is the one worth having.

**The bootstrap has nothing to resample.** It reports 0.000 to 0.000 on both rows, which is
chapter 21's most confident possible way of being wrong, and the program says so in the output
rather than leaving the figure to be quoted. What you report instead is chapter 21's rule of
three: sixty clean replies leave the rate as high as one in twenty.

**One in twenty is not a guarantee of anything.** It is a weaker claim than most people think
they have bought, and it is what a lab-sized run buys. Chapter 21 does the inverse arithmetic:
to be entitled to one in five hundred you need fifteen hundred clean calls, and there is no way
to talk around it.

**So this measurement cannot tell the two modes apart.** Both are zero, both bounds are one in
twenty, and a difference smaller than one in twenty is invisible here. Saying *the strict mode
fixed our format problem* on this evidence would be reporting the sample size as a finding.

**And the thing the strict mode actually gives you is not on this table.** A guarantee is a claim
about every future reply, and a measurement is a claim about sixty past ones. The reason to turn
it on is that the first kind of claim is the kind you want; the reason to keep the validator is
that the guarantee covers the part of your schema the engine compiled and nothing else.

### The failure the guarantee does not cover

A validator that has never fired has also never been tested — chapter 21's line, and sixty clean
replies is exactly the position it warns about. So make it fire, with the cause chapter 21 named
as the usual one.

```python
"""Make the validator fire, because one that never has is untested.

Chapter 21's reply 10 was an unterminated string, and it said the
cause is usually the token cap rather than a formatting slip. Here
is that on a real call, both ways of asking.
"""
from ask import ask
from schema import CASES, validate

cid, q, doc, val, unit = CASES[0]
print(f"  {cid}, max_tokens small enough to cut the reply in half:\n")
for mode in (False, True):
    text, why, model = ask(q, doc, strict=mode, max_tokens=8)
    ok, reason = validate(text)
    print(f"    strict={str(mode):5}  {'OK ' if ok else 'BAD'} {reason}")
    print(f"      finish_reason={why}")
    print(f"      {text!r}")
```

```text
  c01, max_tokens small enough to cut the reply in half:

    strict=False  BAD not JSON
      finish_reason=length
      '{"value": "30","unit":'
    strict=True   BAD not JSON
      finish_reason=length
      '{"value":"30","unit":"days'
```

**Both modes produced something that is not JSON, and the enforced one is the interesting half.**
Every token in `{"value":"30","unit":"days` was legal where it stood. The grammar was satisfied at
every step and the object is still unparseable, because the reply stopped before the grammar was
*finished*. A format guarantee is a guarantee about which tokens may come next, and running out of
tokens is not a token.

So the validator's `not JSON` is correct and its cause is elsewhere, which is why the
`finish_reason` is printed beside it: `length` rather than `stop` is what separates a truncated
reply from a malformed one, and chapter 21 owns that signal. **This is the one format failure a
strict mode cannot remove**, and it is the second of the two things chapter 22's table leaves
to the validation failure rate.

## Step 4: Then Measure What the Schema Cost the Answers

Chapter 22's instruction is to run two measurements because they fail independently, and that the
first can be zero while the second is terrible. The first is zero. Here is the second, on the same
one hundred and twenty replies, with chapter 20's paired bootstrap and chapter 41's grader.

```python
"""What the format cost the answers, which is the other measurement.

Chapter 22 says the two fail independently and the failure rate
can be zero while the answers are worse. The rate was zero both
ways, so this is where any difference has to show up. Chapter 20's
paired bootstrap unchanged, and chapter 41's exact-match method on
two fields, with .strip() on the value as the declared
normalisation and the unit compared raw.
"""

import json
import random

from rate import LOG, rows
from schema import CASES

SEED = 42
KEY = {cid: (val, unit) for cid, q, doc, val, unit in CASES}


def marks(mode):
    """One mark per case: the mean over its trials of (value right AND
    unit right). Averaged WITHIN the case, so one case is one row."""
    per = {}
    for cid, m, trial, valid, reason, finish, model, text in rows():
        if m != mode:
            continue
        want_v, want_u = KEY[cid]
        got = json.loads(text) if valid == "1" else {}
        hit = (str(got.get("value", "")).strip() == want_v
               and got.get("unit") == want_u)
        per.setdefault(cid, []).append(1 if hit else 0)
    return [sum(v) / len(v) for cid, v in sorted(per.items())]


def paired(a, b, trials=10_000):
    rng = random.Random(SEED)
    n = len(a)
    d = sorted(sum(b[i] - a[i] for i in (rng.randrange(n) for _ in range(n)))
               / n for _ in range(trials))
    return d[int(0.025 * trials)], d[int(0.975 * trials)]


if __name__ == "__main__":
    asked, strict = marks("asked"), marks("strict")
    lo, hi = paired(asked, strict)
    print(f"  value AND unit right, {len(asked)} cases, 3 trials averaged")
    print(f"  within each case:\n")
    print(f"    asked   {sum(asked)/len(asked):.3f}")
    print(f"    strict  {sum(strict)/len(strict):.3f}")
    d = (sum(strict) - sum(asked)) / len(asked)
    print(f"    strict - asked  {d:+.3f}")
    print(f"    95% interval    {lo:+.3f} to {hi:+.3f}")
    print("\n  the cases either mode got wrong:\n")
    for i, (cid, q, doc, val, unit) in enumerate(sorted(CASES)):
        if asked[i] < 1.0 or strict[i] < 1.0:
            print(f"    {cid}  key {val!r} {unit!r}"
                  f"   asked {asked[i]:.2f}  strict {strict[i]:.2f}")
```

```text
  value AND unit right, 20 cases, 3 trials averaged
  within each case:

    asked   0.900
    strict  0.900
    strict - asked  +0.000
    95% interval    +0.000 to +0.000

  the cases either mode got wrong:

    c19  key '10' 'working days'   asked 0.00  strict 0.00
    c20  key '10' 'working days'   asked 0.00  strict 0.00
```

**Read the interval the way chapter 41 taught and not the way it looks.** Nought to nought is not
a tight result and it is not proof that the two modes are equivalent. It is perfect agreement:
every one of the twenty cases got the same mark under both modes, so there is nothing for the
bootstrap to vary and by chapter 20's rule the honest reading is *cannot tell*. What it does
establish is narrower and still useful — on this task the enforced format changed no answer at
all, which is the thing chapter 22 says people fail to check.

**And both modes are wrong in exactly the same two places, which are the two places step 1
predicted.** The cases whose true unit is *working days* came back as `days` under both. Here is
the asked mode's reply to c19, which is also the strict mode's:

```text
  {"value": "10","unit": "days","found": true}
```

`found` is `true`, the value is right, and the unit has quietly lost the word that turns ten days into a
fortnight. Ten
working days is a fortnight, and the field that was supposed to carry the distinction has a
closed set of six members with no room for it.

**So the damage from a schema too narrow to hold the answer does not need a strict mode.** Chapter
22 derives it from masking — the mask deletes the right answer because you forbade it — and the
derivation is correct, but it is not the only route to the same place. Enumerating the six units in
a prompt got the same wrong answer as compiling them into a grammar. The narrowness is in the
schema, which I wrote. The enforcement only makes it certain.

### The same fault, made large on purpose

Two cases in twenty is small enough to argue about. So impose the fault deliberately, using the
one keyword in this schema that bounds a value's size, and see what a satisfied schema looks like
when it cannot hold the truth.

```python
"""A schema the right answer cannot satisfy, and what comes back.

Chapter 22 names two ways a strict format makes an answer worse and
says the commoner one is arithmetic: a schema too narrow to express
the right answer. This is that, imposed on purpose, measured.
"""

import copy
import json

import ask as client
from schema import CASES, JSON_SCHEMA, validate


def one(question, doc_id, limit):
    s = copy.deepcopy(JSON_SCHEMA)
    s["properties"]["value"]["maxLength"] = limit
    doc = (client.CORPUS / f"{doc_id}.md").read_text()
    body = {"model": client.MODEL,
            "messages": [{"role": "user", "content": client.PROMPT.format(
                doc=doc, q=question)}],
            "max_tokens": 80, "temperature": 0,
            "response_format": {"type": "json_schema",
                                "json_schema": {"name": "answer",
                                                "strict": True, "schema": s}}}
    d = client.post(body)
    return d["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print("  maxLength 1 on `value`, strict mode on, 20 cases:\n")
    valid = wrong = 0
    for cid, q, doc, val, unit in CASES:
        text = one(q, doc, 1)
        ok, why = validate(text)
        got = json.loads(text)["value"] if ok else "-"
        valid += ok
        bad = ok and got != val
        wrong += bad
        if bad:
            print(f"    {cid}  key {val!r:7} got {got!r}"
                  f"   {len(val)} characters into {len(got)}")
    print(f"\n  {valid} of {len(CASES)} replies passed the validator")
    print(f"  {wrong} of those carried a wrong value")
```

```text
  maxLength 1 on `value`, strict mode on, 20 cases:

    c01  key '30'    got '3'   2 characters into 1
    c02  key '14'    got '1'   2 characters into 1
    c03  key '14'    got '1'   2 characters into 1
    c04  key '20'    got '2'   2 characters into 1
    c05  key '3.99'  got '3'   4 characters into 1
    c06  key '5.99'  got '5'   4 characters into 1
    c07  key '7.99'  got '7'   4 characters into 1
    c08  key '19.99' got '£'   5 characters into 1
    c09  key '9.50'  got '9'   4 characters into 1
    c10  key '6.50'  got '6'   4 characters into 1
    c11  key '48'    got '0'   2 characters into 1
    c12  key '21'    got '2'   2 characters into 1
    c13  key '90'    got '0'   2 characters into 1
    c15  key '29'    got '2'   2 characters into 1
    c18  key '4.50'  got '4'   4 characters into 1
    c19  key '10'    got '1'   2 characters into 1
    c20  key '10'    got '1'   2 characters into 1
```

```text
  20 of 20 replies passed the validator
  17 of those carried a wrong value
```

**Twenty of twenty valid, and seventeen of them wrong.** A validation failure rate of zero, over twenty
replies, every one of which satisfies three fields, a type, an enum and a length bound — and
eighty-five per cent of them carrying a value that is not the answer. If you wanted one line for
what chapter 21 means by *a schema check tells you the answer is shaped like an answer*, this is
the run to quote.

**Three cases are missing from that list, and the reason is the whole mechanism.** c14, c16 and
c17 expect `2`, `3` and `7` — answers that are already one character long, so the bound they were
given can hold them. Everything else was asked for a number and given room for one digit of it.

**Then look at the two rows that are not truncations.** c11 expects `48` and returned `0`; c13
expects `90` and returned `0`. Neither is the first character of the right answer, so the model
was not cut off mid-number — it chose a single character, and on those two it chose the wrong one.
And c08, which expects `19.99`, returned `£`, a currency symbol, from a prompt that says *digits
only, no unit*. A one-character field is not a shorter answer. It is a different question, and the
model answered the different question.

> **Warning:** The bound here is absurd on purpose and the fault it causes is not. A `maxLength`
> of 40 on a field that sometimes needs 60, a two-member enum where the honest answer is a third
> thing, a required field a case has no value for: each of those produces exactly this result,
> which is a reply your validator accepts and your database records and nobody ever reads beside
> the document it came from. The failure has no fingerprints, which is what chapter 21 says about
> the silent default and is true of a narrow schema for the same reason.

## Step 5: One Tool, Constrained Three Ways

The second half of the chapter, and the thing people say a schema cannot reach. The corpus
documents its own identifier grammar: codes have the form `HL-nnnn-x`, where the four digits are
the product and the letter is a variant. That grammar is a pattern, and a pattern is a thing a
strict mode can enforce — so the honest way to find out what it buys is the way steps 2 to 4 did
it, by turning it on and looking, three times.

```python
"""One tool the model can ask for and cannot take.

Chapter 23 owns the five steps and walked them on proposals written
out by hand. This runs step 2 against a real model three times, with
the argument constrained three different ways, and keeps steps 1, 3,
4 and 5 where that chapter put them: in your code.
"""

import copy
import json
import os
import re
import urllib.request

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 120

# The catalogue. sku-conventions.md documents the grammar HL-nnnn-x;
# this is the part of it your code will actually order, which is one
# line of data and the only thing that knows HL-2209-A is nothing.
PARTS = {
    "HL-2208-F": "limescale filter for the HL-2208 kettle",
}

CODE = r"^HL-[0-9]{4}-[A-Z]$"

TOOL = {
    "type": "function",
    "function": {
        "name": "order_part",
        "description": ("Order one replacement part for a customer. "
                        "Use the part code, not a description."),
        "parameters": {
            "type": "object",
            "properties": {
                "part_code": {"type": "string", "pattern": CODE},
                "order_id":  {"type": "string"},
            },
            "required": ["part_code", "order_id"],
            "additionalProperties": False,
        },
    },
}

# Three ways to constrain one argument. The first is the tool as
# chapter 23 would write it; the second declares it strict, which is
# what makes the pattern bind; the third replaces the pattern with
# the catalogue itself.
MODES = (("documented", False, "pattern"),
         ("enforced",   True,  "pattern"),
         ("catalogue",  True,  "enum"))

SYSTEM = ("You handle Harbour Lane customer messages. Part codes have "
          "the form HL-nnnn-x, where nnnn is the product number and x "
          "is a one-letter variant. Order the part the customer needs.")

MESSAGES = [
 ("m1", "Order 8812. The limescale filter in my HL-2208 kettle "
  "is clogged."),
 ("m2", "Order 8813. The crumb tray on my HL-2209 toaster is cracked."),
 ("m3", "Order 8814. The shade on my HL-3310 lamp has a tear in it."),
 ("m4", "Order 8815. One castor has snapped off my HL-5512 chair."),
 ("m5", "Order 8816. Please send a new filter for the kettle, code "
  "HL-2208-F."),
 ("m6", "Order 8817. What are your opening hours?"),
]


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def spec(strict, constraint, pattern=CODE):
    s = copy.deepcopy(TOOL)
    p = s["function"]["parameters"]["properties"]["part_code"]
    if constraint == "enum":
        p.pop("pattern", None)
        p["enum"] = list(PARTS)
    else:
        p["pattern"] = pattern
    if strict:
        s["function"]["strict"] = True
    return s


def propose(text, toolspec):
    """Step 2, and only step 2. Returns (name, arguments, model)."""
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": text}],
        "tools": [toolspec], "max_tokens": 120, "temperature": 0,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    m = d["choices"][0]["message"]
    calls = m.get("tool_calls") or []
    if not calls:
        return None, m.get("content") or "", d["model"]
    f = calls[0]["function"]
    return f["name"], f["arguments"], d["model"]


def decide(name, arguments):
    """Step 3. Five checks, in order, and the order matters. Return a
    (code, detail) pair: the code is what you group a log on and the
    detail is what you read. One string does neither job well."""
    if name != "order_part":
        return "unknown-tool", str(name)
    try:
        args = json.loads(arguments)
    except json.JSONDecodeError:
        return "unparsed-arguments", arguments[:30]
    for field in ("part_code", "order_id"):
        if field not in args:
            return "missing-argument", field
    code = args["part_code"]
    if not re.match(CODE, code):
        return "not-a-part-code", code
    if code not in PARTS:
        return "no-such-part", code
    return None, code


def wrong(mid, code):
    """Is this the part that message asked about? m1 and m5 are the
    only two messages about the kettle; the rest are other products,
    and m6 is about nothing."""
    return code in PARTS and mid not in ("m1", "m5")


if __name__ == "__main__":
    print(f"  does an undeclared pattern bind? ^ZZ- on m1:\n")
    for strict in (False, True):
        _, args, _ = propose(MESSAGES[0][1],
                             spec(strict, "pattern",
                                  r"^ZZ-[0-9]{4}-[A-Z]$"))
        got = json.loads(args)["part_code"]
        note = "the pattern did nothing" if not got.startswith("ZZ") \
            else "the pattern chose the prefix"
        print(f"    strict {str(strict):5} -> {got:11} {note}")

    # Truncate and write the header once, so a second run does not
    # double every count and `tail -n +2` means what it says.
    with open("proposals.tsv", "w") as f:
        f.write("message\tmode\ttool\targuments\treason\tmodel\n")

    rows, refused, misordered = {}, {}, {}
    for name, strict, constraint in MODES:
        s = spec(strict, constraint)
        refused[name] = misordered[name] = 0
        for mid, text in MESSAGES:
            tool, args, model = propose(text, s)
            code, detail = decide(tool, args)
            rows.setdefault(mid, {})[name] = detail
            refused[name] += code is not None
            misordered[name] += code is None and wrong(mid, detail)
            with open("proposals.tsv", "a") as f:
                f.write(f"{mid}\t{name}\t{tool}\t{args}\t"
                        f"{code or 'would-run'}\t{model}\n")

    print(f"\n  part_code by mode, {len(MESSAGES)} messages:\n")
    print(("  msg  " + "  ".join(f"{n:11}" for n, _, _ in MODES)).rstrip())
    for mid, _ in MESSAGES:
        line = f"  {mid}   " + "  ".join(f"{rows[mid][n]:11}"
                                        for n, _, _ in MODES)
        print(line.rstrip())
    print(f"\n  refused by `decide`, of {len(MESSAGES)}:\n")
    for name, _, _ in MODES:
        extra = (f"   and {misordered[name]} would order the wrong part"
                 if misordered[name] else "")
        print(f"    {name:11} {refused[name]}{extra}")
    print("\n  wrote proposals.tsv")
```

```text
  does an undeclared pattern bind? ^ZZ- on m1:

    strict False -> HL-8812-A   the pattern did nothing
    strict True  -> ZZ-8812-A   the pattern chose the prefix

  part_code by mode, 6 messages:

  msg  documented   enforced     catalogue
  m1   HL-2208-A    HL-2208-A    HL-2208-F
  m2   HL-2209-A    HL-2209-A    HL-2208-F
  m3   HL-8814-A    HL-8814-A    HL-2208-F
  m4   HL-5512-A    HL-5512-A    HL-2208-F
  m5   HL-2208-F    HL-2208-F    HL-2208-F
  m6   HL-8817-A    HL-8817-A    HL-2208-F

  refused by `decide`, of 6:

    documented  5
    enforced    5
    catalogue   0   and 4 would order the wrong part

  wrote proposals.tsv
```

**Start with the two lines at the top, because they settle something about the first mode before
any of its results can be read.** The tool as chapter 23 would write it carries a `pattern`, and
nothing enforces it: given a pattern demanding a `ZZ-` prefix, the model returned `HL-8812-A`
cheerfully. Declare the same tool strict and it returns `ZZ-8812-A`. **So a pattern you did not
declare strict is documentation and nothing more**, and the six compliant codes in the `documented`
column are the model following the system message — which is chapter 23's third reason put the
other way round: compliance is a correlation, and this one happens to be a correlation with
something true. The check that *held* the shape in that column is `re.match` in your code.

**Then read the three columns across, because the pattern's being enforced changed nothing that
mattered.** `documented` and `enforced` refuse the same five proposals, because every invented code
already satisfies the grammar. `HL-2209-A` is a perfectly formed code for a product that exists and
a variant that does not, and no amount of enforcement touches it. **Chapter 23's `drop_table` was a
tool that did not exist and looked plausible; this is the same failure one level down**, inside an
argument, where the invented value is grammatical, well-typed, pattern-valid, and about the very
product the customer named.

**And then the third column, which is the one worth the step.** Replace the pattern with the
catalogue itself — `"enum": list(PARTS)` — and the engine will not let the model emit a code that
does not exist. The existence of a part *is* expressible in a grammar, by copying your catalogue
into the request, and `decide` refuses nothing in that column. Look at what it ordered. The toaster,
the lamp, the chair and the opening-hours question all came back asking for the kettle's limescale
filter, because with one member in the enum there was nothing else to emit. **Chapter 22's lab
step 3 is this exact result**: a schema whose enum has one member is not a format constraint,
because you have stopped constraining the format and started choosing the answer.

So the rule is not that a grammar cannot express existence. It is that the grammar which does is a
worse instrument than the two lines of Python that refused those five proposals. Call the check that refused those five
proposals an **existence check** — the question of whether an identifier the model supplied names
something your system actually holds — and the reason it belongs in your code is threefold: the
enum is a *copy* of your catalogue and goes stale the moment a part is added, it cannot refuse but
only redirect, and it is sent on every call, which chapter 23 priced. Your code can say *no*. A
grammar can only say *something else*.

> **Warning:** The pattern I wrote is itself too narrow, in exactly the way step 4 is about, and I
> did not notice until the third mode made me read it. `sku-conventions.md` says an item with only
> one variant has no letter, and gives `HL-5512` as its example — which is m4's chair, and which
> `^HL-[0-9]{4}-[A-Z]$` rejects. Under enforcement that pattern cannot emit a code the corpus
> documents as valid. One optional group, `^HL-[0-9]{4}(-[A-Z])?$`, fixes it. Step 4's fault does
> not stay in step 4's keyword: `maxLength`, an enum and a `pattern` are three ways of writing
> down what you will accept, and all three are a claim you can get wrong.

**Read the codes themselves last, because the failures are not random.** The model was told the
grammar in the system message and used it correctly every time. For the kettle filter in m1 it
produced `HL-2208-A` — the right product number and an invented variant letter, where the corpus
says the filter is `HL-2208-F`. In m3 it took `8814` — the *order* number from the customer's first
sentence — and used it as a product number, for a message about an HL-3310 lamp. In m6 it did the
same with `8817`, for a message that asks about opening hours and requests no part at all.

> **Warning:** m6 is partly my doing and the division of blame matters. The system message ends
> *Order the part the customer needs*, which is an instruction to order, and the model obeyed it on
> a message where the honest answer is that no part is needed. That is a prompt defect, and chapter
> 36 is where a tool and its description are designed so that a model uses them well. What it is
> not is a limit: the prompt caused the proposal and the code refused it, which is the division
> chapter 23 insists on. Fix the prompt *and* keep the check.

**Notice last what this program does not have: a function to run.** `PARTS` maps a code to a
description, not to anything callable, and nothing in the file can place an order. That is the
whole of *an action the model can ask for but not take*, and it is worth seeing once in a lab where
no real system is listening. In a real one, chapter 23's step 4 would follow the `would-run` rows
and step 5 would send a result or the refusal text back.

## Step 6: The Log, and the Checks You Did Not Write

The proposals are in a file, with the reason code, the arguments and the model snapshot that
produced them. Read it, which is chapter 30's method and the thing chapter 41 spent a whole step
on. Start by grouping the reasons, which is why `decide` returns a code and a detail rather than
one sentence.

```text
  cut -f2,5 proposals.tsv | tail -n +2 | sort | uniq -c

     6  catalogue   would-run
     5  documented  no-such-part
     1  documented  would-run
     5  enforced    no-such-part
     1  enforced    would-run
```

**Five of one reason is one systematic defect, not five problems.** That is the whole value of a
groupable code: *no-such-part* five times says the model is inventing the variant letter, which is
a prompt and a catalogue question you can act on. Had `decide` returned only its detail — *no such
part: HL-2209-A* and four more like it — the same file would have grouped into five rows of one and
read as five unrelated incidents. The detail is what you read; the code is what you count. Chapter
23's advice to send the specific reason back to the model is about the message, not about the
column you alarm on, and the two want different strings.

Then the arguments, where the other half of the lesson is.

```text
  awk -F'\t' '$2=="documented"' proposals.tsv | cut -f1,4

  m1  {"part_code":"HL-2208-A","order_id":"8812"}
  m2  {"part_code":"HL-2209-A","order_id":"8813"}
  m3  {"part_code":"HL-8814-A","order_id":"HL-3310"}
  m4  {"part_code":"HL-5512-A","order_id":"8815"}
  m5  {"part_code":"HL-2208-F","order_id":"8816"}
  m6  {"part_code":"HL-8817-A","order_id":"8817"}
```

**Read the second argument down the column, which is the one the chapter has not been about.**
`order_id` has no pattern, no enum and no existence check: the schema says `"type": "string"` and
that is all my code ever asks of it. So m3's order id is `HL-3310`, a product code in the field
meant for an order number — a half-swap, since the part code in the same proposal is `HL-8814-A`
and not the lamp's code either. It is the only unconstrained field in the tool, and it is the field
that went wrong in a way nothing reported.

All six messages gave an order number in their first sentence and five of the six arrived intact.
That is not reassurance; it is chapter 23's third reason again. A field with no check on it has no
limit on it, whatever this run happens to show — and on another run m6 came back with the word
`customer-request` in that field, with `8817` sitting in the sentence in front of it.

**So the log earns its place twice over.** It is where you find the failure your checks do not
cover, and it is the only record that a refusal happened at all. A refused proposal leaves no trace
anywhere else: no row is written, no part is ordered, nothing is raised, and five of these six
messages would have left a system looking as though nothing had happened. Record the proposal, the
reason code, the detail and the model snapshot, and you have a file that says the model invents
variant letters under this prompt and this snapshot — which is a thing you can fix, and which no
error rate would ever have shown you.

> **Note:** The snapshot column is not decoration. Every figure in steps 3 to 6 is a figure about
> `gpt-4o-mini-2024-07-18` and about nothing else, and chapter 54 owns what happens when the name
> you asked for starts serving something else. `rate.py` writes the same column into `replies.tsv`
> for the same reason, which is the cheapest possible insurance against a measurement whose
> subject changed under it.

## What To Actually Do

1. **Write the schema from the data, not from your idea of the data.** Open the documents and
   check that every answer you will ask for can be expressed. Two of these twenty could not, and
   the schema was written first.
2. **Keep the validator when the provider enforces the schema.** It covers the keywords the
   engine did not compile, and it is the only thing that catches a reply cut off at the token cap.
3. **Report the rule of three, never a bootstrap interval, when nothing failed.** Zero in sixty is
   one in twenty, and one in twenty is not a guarantee.
4. **Make the validator fire once on purpose**, with a token cap small enough to cut a reply in
   half, so that its silence afterwards means something.
5. **Measure the answers as well as the format**, paired on the same cases. They fail
   independently, and the rate being zero says nothing about the second.
6. **Declare a constraint strict, or know it is documentation.** A `pattern` on a tool argument
   that the request does not declare strict enforces nothing, and the compliance you see is the
   model agreeing with you.
7. **Check that an identifier exists in your own code**, separately from checking its shape — not
   because a grammar cannot express existence, but because compiling your catalogue into the
   request gives you a stale copy that redirects instead of refusing.
8. **Log every proposal with a reason code and a detail**, because a refusal is invisible
   everywhere else, the code is what you group on and the detail is what you read — and put the
   model snapshot in the same row.

## Summary, Key Terms, and Review Questions

### Summary

Twenty extraction cases from the corpus, a three-field schema, and the same thing asked two ways:
the format requested in the prompt, and the format enforced by the provider during generation. The
**validation failure rate** — the proportion of real replies the schema rejects — was **zero out of sixty
on both**, so the bootstrap had nothing to resample and reported 0.000 to 0.000, and what you
report instead is chapter 21's rule of three: **one in twenty**, which is far weaker than it
feels and is what a lab-sized run buys. That measurement cannot tell the two modes apart, and the
thing the enforced format gives you is not on the table at all, being a claim about every future
reply rather than about sixty past ones. **One format failure survives the guarantee**: a reply cut
off at the token cap, where every token emitted was legal and the object is still unparseable
because the reply stopped before the grammar was finished — `finish_reason` is `length` rather
than `stop`, which is the signal chapter 21 named. Then the second measurement, which chapter 22
says people skip: the answers, paired on the same cases. **0.900 both ways, a difference of
+0.000 with an interval of zero width** — which chapter 41's lesson says to read as perfect
agreement and not as proof, since every case got the same mark both ways. **Both modes were wrong
in the same two places, and step 1 had already found them**: the corpus states two figures in
*working days* and the unit enum has six members with no room for it, so `days` came back for an
interval four days longer. **The damage from a schema too narrow to hold the answer does not
need a strict mode** — enumerating the units in a prompt got the same wrong answer as compiling
them into a grammar, because the narrowness is in the schema, which you wrote. Imposed on purpose
with a `maxLength` of 1, that fault gives **twenty of twenty replies valid and seventeen of them
wrong**, including two that are not truncations (`48` returned as `0`, `90` as `0`) and one that
came back as a currency symbol from a prompt asking for digits. Then one tool, constrained three
ways on the same six customer messages. **A pattern you did not declare strict enforces nothing**:
against a pattern demanding a `ZZ-` prefix the model returned `HL-8812-A`, and only the declared
version returned `ZZ-8812-A` — so the six compliant codes in the first column are the model
following the system message, and what held the shape is `re.match` in your code. **Enforcing the
pattern changed nothing that mattered**, because every invented code already satisfies the
grammar: `HL-2209-A` is a well-formed code for a real product and a variant that does not exist,
and the same five proposals were refused either way. **Compiling the catalogue in as an enum did
make existence enforceable, and turned the constraint into the answer**: nothing was refused and
all six came back ordering the kettle's filter, four of them for a message that was not about the
kettle, including one about a chair and one asking about opening hours — chapter 22's one-member
enum on a real proposal. So an **existence
check** belongs in your code not because a grammar cannot express it but because a grammar can
only redirect where your code can refuse — and the enum is a copy of your catalogue, sent on every
call, going stale. The pattern this chapter shipped was itself too narrow, rejecting the letterless
`HL-5512` the corpus documents, which is step 4's fault in a third keyword. And the log is where
the rest of it shows: grouping on a reason *code* gives five of one defect where grouping on the
detail would have given five unrelated incidents, the one unconstrained argument is the one that
came back holding a product code, and a refused proposal leaves no trace anywhere else — so five
of these six messages would otherwise have left a system looking as though nothing had happened.

### Key Terms

| Term | Meaning |
|---|---|
| **Validation failure rate** | The proportion of real replies your schema rejects, measured over calls you made. Zero over sixty is one in twenty by the rule of three, and says nothing about whether the answers are right |
| **Existence check** | The check that an identifier the model supplied names something your system actually holds. A grammar can express it, by compiling your catalogue into the request as an enum — and that copy goes stale, is sent on every call, and can only redirect the model rather than refuse it. The check belongs where the refusal can happen |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Two measurements, not one | The validation failure rate, and the answers paired against the other way of asking. They fail independently |
| Zero failures in 60 | One in twenty, by the rule of three. A guarantee is a different kind of claim from a measurement |
| The failure a guarantee misses | A reply cut off at the token cap. Every token legal, the object unparseable, `finish_reason` `length` |
| A schema too narrow | `maxLength` 1 under enforcement gave 20 of 20 valid and 17 wrong, because the local validator still allowed 20. The silence is the gap between the two copies |
| And it needs no enforcement | A unit enum with no member for *working days* got the same wrong answer from a prompt as from a grammar |
| Shape against existence | A pattern says a code could exist. Only your catalogue says it does |
| What to log | Every proposal, its verdict and its message. A refusal leaves no other trace |

### Review Questions

1. Your validation failure rate over sixty replies is zero. What are you entitled to say?
2. You turn on your provider's strict mode and the format problem goes away. What have you not
   measured?
3. A reply satisfies your schema on every field and the number in it is wrong. Name two ways that
   happens.
4. The model proposes a tool call whose arguments are all the right type and shape. What is left to
   check?
5. Why log a proposal your code refused?

### Review Answers

1. That the rate is low, not that it is zero, and the number to quote is the rule of three: with
no failures in sixty tries the rate may still be about one in twenty. The bootstrap is no help and
will say 0.000 to 0.000, because it is resampling a list with no failure in it — chapter 21's most
confident possible way of being wrong. The second thing to say is that the validator has never
fired, so it has never been tested: feed it a reply truncated by a small token cap and watch it
report `not JSON` before you trust its silence. And the third, if the question is really about
whether to turn a strict mode on, is that a measurement over sixty past replies and a guarantee
about every future one are different kinds of claim, and sixty clean replies cannot establish the
second.
2. The answers. Turning the format constraint on changes what the model emits, so it is a change
like any other and chapter 20 applies: both versions, the same cases, paired, with an interval on
the difference. On this chapter's task the answer was that nothing moved — 0.900 both ways, every
case scoring the same under both — but that is a result you have to go and get, and it was
obtained on the same one hundred and twenty replies the rate came from. The thing to add is that
the validation failure rate and the answers fail independently, and the rate can be perfect while the
answers are worse, which is exactly the shape of a complaint that a strict mode made things worse.
3. First, a schema too narrow to hold the right answer. A closed set of units with no member for
*working days* turns ten working days into ten days and the validator passes it, because the reply
satisfies every claim you made. Pushed to an extreme — a `maxLength` of 1 on a numeric field — that
gives twenty valid replies of which seventeen carry the wrong number, and two of them are not even
truncations: a model given room for one character of `48` returned `0`. Second, chapter 21's fourth
layer: the values can simply be untrue, and no schema reaches that at all, because a schema check
tells you the answer is shaped like an answer. The two need different machinery — the first is
fixed by reading your own data before you write the schema, and the second by a measurement of
correctness over cases with known answers.
4. Whether the things the arguments name exist. A type is a claim about what kind of JSON value
arrived and a pattern is a claim about its characters, and both are satisfiable by a value that
refers to nothing — this
chapter's six proposals all matched a pattern taken from the corpus's own documented code grammar,
and five of them named a part that does not exist. Say the thing about the pattern too, because it
is where people stop short: a pattern a request does not declare strict is not enforced at all, and
the chapter proves it by demanding a `ZZ-` prefix and getting `HL-8812-A` back. So the remaining check is an existence check
against your own catalogue, and the useful thing to add is that a grammar *can* express it —
compile the catalogue into the request as an enum and the engine will not emit anything else — and
that this is a worse instrument rather than a better one. A copy of your catalogue goes stale, it
is sent on every call, and it cannot refuse: with one member in the enum, all six of this
chapter's messages came back ordering a kettle filter, four of them wrongly — including one about a
chair and one that asked about opening hours. Your code can say no; a grammar can only say something else. Chapter 23
states the same limit for a tool *name* and names the registry as what refuses an invented one. The
other thing left to check is any field you did not constrain at all, which in this chapter was the
order id — and that is the field that came back holding a product code.
5. Because a refusal leaves no other trace. Nothing was ordered, no row was written, no error was
raised, and a system that refused five proposals out of six looks from the outside exactly like a
system to which nothing happened. The log is also where the pattern is, and it only shows if you
logged the right two things: a reason *code* you can group on and a detail you can read. Five rows
of `no-such-part` is one systematic defect — a model inventing a variant letter because nothing
told it the real one — where five rows of *no such part: HL-2209-A* and four more like it group
into five rows of one and read as five unrelated incidents. And the log is where you find the
failures your checks do not cover, since a field with no check on it cannot appear in a refusal at
all. Log the model snapshot beside them, because every one of those findings is a finding about
one snapshot.

> **You understand this when** you can say what a zero validation failure rate over sixty replies
> entitles you to, and why an existence check belongs in your code even though a grammar can
> express it.
