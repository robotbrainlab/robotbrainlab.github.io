# Lab: Call a Model and Measure It

Part II measured a great deal and watched none of it. Chapter 1 said a model is charged by the
amount of text moved and answers after a noticeable wait. Chapter 10 gave the unit and a rule of
thumb for estimating it. Chapter 13 gave four reasons temperature zero is not a guarantee.
Chapter 1 also split the wait in two, and Chapter 15 said why the halves differ. Chapter 20 said a single run is not a score. Every one of those
is now a claim you can put a number on, with your own key, in about forty minutes.

This is the first lab, so it also sets the shape of the ten that follow: a folder, a pinned
model, nothing secret in a file, and a measurement you could defend.

*The problem.* I've read about tokens, cost and variance. I've never watched any of them happen.

*The question.* What do the numbers actually look like, and which of them are facts about the
model rather than about my network?

> **Note:** Every `text` block below is [**one real run**]{.noindex}, on one day, from one place.
> **Three kinds of figure appear in them and only one is stable.** The token counts come from a
> pinned model and a fixed vocabulary, so they should match yours exactly. The timings will not:
> they carry the internet and the provider's load as well as the model. And in step 5 the *replies
> themselves* will not match either — which is that step's subject. So the prose below quotes the
> token counts and describes the other two by shape, and where a figure is the network's rather
> than the model's it says so.

## Step 1: A Folder, a Key From the Environment, and a Pinned Model

Make a folder, make a virtual environment, and install nothing. Every program in this chapter uses
the standard library, which is deliberate: a lab whose first instruction is `pip install` cannot be
run by somebody who does not yet trust the package.

```text
  mkdir -p ~/sandbox/ch40 && cd ~/sandbox/ch40
  python3 -m venv .venv
  source .venv/bin/activate
  export OPENAI_API_KEY="sk-..."   # never in a file here
```

> **Note:** What this chapter costs you to run, before you run it. Four of the five programs are
> dominated by *input* tokens and are negligible. Step 4 is the exception: it asks for about 1,600
> output tokens across its repeats, against a few hundred of input, and output is the dearer half
> everywhere. The whole chapter is still a fraction of a cent on a small model — but step 4 is the
> one to think about before you put it in a loop, and noticing which half of a workload dominates
> is Chapter 53's habit starting early.

Save this as `call.py`. It is the only file that knows how to reach a model, and every later
program imports it.

```python
"""One function that calls a model, and nothing else.

The key is read from the environment and appears nowhere else: not
in this file, not in a file beside it, not in output, not in a
commit. If OPENAI_API_KEY is not set, this stops rather than
guessing.

The model is pinned to a dated snapshot. "gpt-4o-mini" is a name
that moves; "gpt-4o-mini-2024-07-18" is a name that does not, and
step 2 shows what the difference is worth.
"""

import json
import os
import urllib.error
import urllib.request

MODEL = "gpt-4o-mini-2024-07-18"
URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 120                      # seconds, whole request


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def call(prompt, max_tokens=100, temperature=0.0, model=MODEL):
    """Send one prompt. Return the whole reply, parsed.

    Chapter 19 owns retries, backoff and the three timeouts. A lab
    gets one timeout and no retry, because a lab that quietly
    retries is measuring something other than what it claims.
    """
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def text(reply):
    return reply["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    print(f"  model asked for   {MODEL}")
    print(f"  key               {'set' if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}")
    try:
        r = call("Reply with one word: ready", max_tokens=5)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"  HTTP {e.code}: {e.read().decode()[:120]}")
    print(f"  model that replied {r['model']}")
    print(f"  reply             {text(r)!r}")
```

```text
  model asked for   gpt-4o-mini-2024-07-18
  key               set
  model that replied gpt-4o-mini-2024-07-18
  reply             'Ready.'
```

Three things in that file are the point of the step.

**The key comes from the environment and appears nowhere else.** Not in the source, not in a file
beside the source, not in output, not in a commit. The function raises if it is missing rather than
sending an unauthenticated request and reporting a confusing failure two layers down.

**The model is pinned to a dated snapshot.** A **model snapshot** is a model name with a date in
it: `gpt-4o-mini-2024-07-18` rather than `gpt-4o-mini`. The second one is a name the provider is
free to point somewhere else, and step 2 shows what that is worth.

**There is one timeout and no retry.** Chapter 19 owns retries, backoff and the three timeouts, and
anything in production wants all of them. A *lab* wants none, because a lab that quietly retries is
measuring something other than what it claims.

> **Warning:** `export` puts the key in the environment of that shell only. Do not solve the
> inconvenience by writing it into a file in the lab folder — that is the one place it is most
> likely to be committed. A shell profile or a secret manager outside the project is the right
> home, and Chapter 51 is where this becomes a subject rather than an aside.

## Step 2: One Call, and Which Model Answered

Save this as `first.py`. The answer is one word; everything else in the reply is the step.

```python
"""One call, and everything the reply says that is not the answer.

The answer is one word. The rest of the object is the chapter.
"""

from call import MODEL, call, text

if __name__ == "__main__":
    r = call("Name the capital of France. One word.", max_tokens=10)

    print(f"  reply            {text(r)!r}\n")
    u = r["usage"]
    print(f"  prompt tokens    {u['prompt_tokens']}")
    print(f"  reply tokens     {u['completion_tokens']}")
    print(f"  total            {u['total_tokens']}")
    print(f"  ended because    {r['choices'][0]['finish_reason']}\n")

    print("  Two sub-counts that are zero now and will not always")
    print("  be. Both are chapters of their own:\n")
    print(f"    cached prompt tokens   "
          f"{u['prompt_tokens_details']['cached_tokens']}")
    print(f"    reasoning tokens       "
          f"{u['completion_tokens_details']['reasoning_tokens']}")
    print("\n  The first is a discount on text the provider has")
    print("  already read, which is chapter 52's; the second is")
    print("  output you pay for and never see, which is chapter")
    print("  53's. Knowing the fields exist is this chapter's job.\n")

    print("  And now the field worth the whole step. Ask for the")
    print("  name that moves, and read what answered:\n")
    floating = MODEL.rsplit("-", 3)[0]
    r2 = call("Reply with one word: ready", max_tokens=5, model=floating)
    print(f"    asked for   {floating}")
    print(f"    replied     {r2['model']}")
    print(f"\n  The provider resolved the moving name to a dated one")
    print("  and told you which. So a floating name is not unsafe")
    print("  because you cannot know what served you - it is")
    print("  unsafe because the answer can change between two")
    print("  runs and nothing warns you. Pin the dated name, and")
    print("  read this field back anyway: chapter 54 owns why a")
    print("  silent version change is the hardest failure to")
    print("  attribute, and this is the one line that catches it.")
```

```text
  reply            'Paris.'

  prompt tokens    16
  reply tokens     2
  total            18
  ended because    stop

  Two sub-counts that are zero now and will not always
  be. Both are chapters of their own:

    cached prompt tokens   0
    reasoning tokens       0

  The first is a discount on text the provider has
  already read, which is chapter 52's; the second is
  output you pay for and never see, which is chapter
  53's. Knowing the fields exist is this chapter's job.

  And now the field worth the whole step. Ask for the
  name that moves, and read what answered:

    asked for   gpt-4o-mini
    replied     gpt-4o-mini-2024-07-18

  The provider resolved the moving name to a dated one
  and told you which. So a floating name is not unsafe
  because you cannot know what served you - it is
  unsafe because the answer can change between two
  runs and nothing warns you. Pin the dated name, and
  read this field back anyway: chapter 54 owns why a
  silent version change is the hardest failure to
  attribute, and this is the one line that catches it.
```

**The usage block is the bill, itemised**, and two of its sub-counts are worth knowing exist even
while they read zero. `cached_tokens` is a discount on input the provider has already read, which
is Chapter 52's prompt-prefix caching showing up as a field you can watch. `reasoning_tokens` is
output you pay for and never see, which is Chapter 53's. Neither is this chapter's subject; both
are things you would otherwise discover from an invoice.

**Then the field that earns the step.** Ask for `gpt-4o-mini` and the reply says
`gpt-4o-mini-2024-07-18`. So the provider resolved the moving name to a dated one *and told you
which*. That changes the argument for pinning: a floating name is not dangerous because you cannot
find out what served you — it is dangerous because the answer can differ between two runs and
nothing raises. **Pin the dated name, and read the field back anyway.** Chapter 54 owns why a
silent version change is the hardest failure to attribute, and this is the one line that catches
it.

> **Tip:** Log the `model` field with every result you intend to keep. It costs a column, and it
> is the difference between "the score dropped in March" and "the score dropped in March, when the
> model we were served changed".

## Step 3: Count the Tokens Three Ways

Chapter 10's rule of thumb is about four characters to a token. Check it against the count that
decides the bill — and then against the same provider's *other* vocabulary, which disagrees.

```python
"""Counting tokens two ways, and then a third that disagrees.

Way one is chapter 10's rule of thumb: about four characters to a
token. Way two is the provider's own count, which is the one that
decides the bill. Way three is the same provider's OTHER vocabulary,
reached through the embeddings endpoint with the same key - and on
one of these strings it disagrees by a factor of three.
"""

import json
import os
import urllib.request

from call import call, key

CHAT = "gpt-4o-mini-2024-07-18"
EMBED = "text-embedding-3-small"

# (label, text). The label is what gets printed: the last string is
# Tamil and this book's font has no Tamil glyphs, so printing it
# would put missing characters in the PDF. The escape is also an
# exact record of what was measured.
PROMPTS = [
    ("catalyst", "catalyst"),
    ("an English question", "What is the capital of France?"),
    ("a line of Python", "def f(x): return x**2 + 3*x - 1"),
    ("the same question in Tamil",
     "\u0baa\u0bbe\u0bb0\u0bbf\u0bb8\u0bcd "
     "\u0b8e\u0b99\u0bcd\u0b95\u0bc1 "
     "\u0b89\u0bb3\u0bcd\u0bb3\u0ba4\u0bc1\u003f"),
]


def billed(text):
    """What the chat model charges for this prompt."""
    return call(text, max_tokens=1)["usage"]["prompt_tokens"]


def embed_billed(text):
    """What the embedding model charges. No message wrapper here."""
    body = json.dumps({"model": EMBED, "input": text}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings", body,
        {"Authorization": f"Bearer {key()}",
         "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["usage"]["prompt_tokens"]


if __name__ == "__main__":
    print(f"  Chat  {CHAT}")
    print(f"  Embed {EMBED}\n")
    print("  The rule of thumb against the bill.\n")
    print("    prompt                        chars  chars/4  billed")
    for label, p in PROMPTS:
        print(f"    {label:<28} {len(p):>5} {len(p)/4:>8.1f} {billed(p):>7}")

    print("\n  Something is being added. Find it by adding one known")
    print("  token at a time and reading the slope:\n")
    print("    prompt          billed   change")
    prev = None
    for k in (1, 2, 3, 4, 5):
        n = billed(" ".join(["cat"] * k))
        print(f"    {k} x 'cat'{'':<7} {n:>5}   "
              f"{'' if prev is None else format(n - prev, '+d')}".rstrip())
        prev = n

    one = billed("cat")
    overhead = one - 1
    print(f"\n  Each extra 'cat' costs exactly 1, so a marginal 'cat'")
    print(f"  is 1 token. That is the SLOPE, and on its own it does")
    print(f"  not fix the intercept: if the first 'cat' cost 2, the")
    print(f"  slope would still be 1. So measure the intercept")
    print(f"  directly, by sending nothing at all:\n")
    empty = billed("")
    print(f"    an empty prompt bills      {empty}")
    print(f"    'cat' bills                {one}")
    print(f"    the difference             {one - empty}")
    print(f"\n  {empty} tokens for no text, and one more for one token of")
    print("  text. That is the chat template - the markup the")
    print("  provider wraps round your text so the model sees a")
    print("  conversation turn - and you pay for it every call.\n")

    print("    prompt                      yours  template  per char")
    for label, p in PROMPTS:
        mine = billed(p) - overhead
        print(f"    {label:<27} {mine:>5} {overhead:>9} {len(p)/mine:>9.2f}")

    short = billed(PROMPTS[0][1]) - overhead
    print(f"\n  {overhead} of the {short + overhead} tokens on the first row are not your")
    print(f"  prompt: {overhead/(short+overhead):.0%} of that call. A short prompt is dearer")
    print("  per useful token than its length suggests, which is an")
    print("  argument for putting several questions in one call.\n")

    print("  Now the third count. The same strings, same key, same")
    print("  provider - through the embeddings endpoint, which uses")
    print("  an older vocabulary:\n")
    print("    prompt                      chat  embed   ratio")
    rows = []
    for label, p in PROMPTS:
        a = billed(p) - overhead
        b = embed_billed(p)
        rows.append((label, a, b))
        print(f"    {label:<27} {a:>4} {b:>6} {b/a:>7.2f}")

    same = [r for r in rows if r[1] == r[2]]
    diff = [r for r in rows if r[1] != r[2]]
    print(f"\n  {len(same)} rows agree exactly and {len(diff)} does not.")
    for label, a, b in diff:
        print(f"  {label} is {a} tokens to the chat")
        print(f"  model and {b} to the embedding model: the same string")
        print(f"  costing {b/a:.2f} times as much depending on which")
        print("  vocabulary reads it.\n")
    print("  And notice what the same column proves twice over.")
    print("  The embeddings endpoint wraps nothing round your text,")
    print("  so its counts ARE your tokens - and on the three rows")
    print("  that agree, they match the chat model's figures after")
    print(f"  the {overhead}-token template comes off. That is a second")
    print("  measurement of the intercept, independent of the")
    print("  slope and of the empty prompt.\n")
    print("  So a characters-per-token figure does NOT transfer")
    print("  between vocabularies, and one provider ships more")
    print("  than one of them. Three of these four strings cost the")
    print("  same under both, so the figure is not arbitrary - it")
    print("  is just not something you may carry across a model")
    print("  boundary without checking. Chapter 10's rule holds")
    print("  here for English prose, which is what its vocabulary")
    print("  was built from; carry the method, never the number.")
```

```text
  Chat  gpt-4o-mini-2024-07-18
  Embed text-embedding-3-small

  The rule of thumb against the bill.

    prompt                        chars  chars/4  billed
    catalyst                         8      2.0      10
    an English question             30      7.5      14
    a line of Python                31      7.8      22
    the same question in Tamil      20      5.0      15

  Something is being added. Find it by adding one known
  token at a time and reading the slope:

    prompt          billed   change
    1 x 'cat'            8
    2 x 'cat'            9   +1
    3 x 'cat'           10   +1
    4 x 'cat'           11   +1
    5 x 'cat'           12   +1

  Each extra 'cat' costs exactly 1, so a marginal 'cat'
  is 1 token. That is the SLOPE, and on its own it does
  not fix the intercept: if the first 'cat' cost 2, the
  slope would still be 1. So measure the intercept
  directly, by sending nothing at all:

    an empty prompt bills      7
    'cat' bills                8
    the difference             1

  7 tokens for no text, and one more for one token of
  text. That is the chat template - the markup the
  provider wraps round your text so the model sees a
  conversation turn - and you pay for it every call.

    prompt                      yours  template  per char
    catalyst                        3         7      2.67
    an English question             7         7      4.29
    a line of Python               15         7      2.07
    the same question in Tamil      8         7      2.50

  7 of the 10 tokens on the first row are not your
  prompt: 70% of that call. A short prompt is dearer
  per useful token than its length suggests, which is an
  argument for putting several questions in one call.

  Now the third count. The same strings, same key, same
  provider - through the embeddings endpoint, which uses
  an older vocabulary:

    prompt                      chat  embed   ratio
    catalyst                       3      3    1.00
    an English question            7      7    1.00
    a line of Python              15     15    1.00
    the same question in Tamil     8     26    3.25

  3 rows agree exactly and 1 does not.
  the same question in Tamil is 8 tokens to the chat
  model and 26 to the embedding model: the same string
  costing 3.25 times as much depending on which
  vocabulary reads it.

  And notice what the same column proves twice over.
  The embeddings endpoint wraps nothing round your text,
  so its counts ARE your tokens - and on the three rows
  that agree, they match the chat model's figures after
  the 7-token template comes off. That is a second
  measurement of the intercept, independent of the
  slope and of the empty prompt.

  So a characters-per-token figure does NOT transfer
  between vocabularies, and one provider ships more
  than one of them. Three of these four strings cost the
  same under both, so the figure is not arbitrary - it
  is just not something you may carry across a model
  boundary without checking. Chapter 10's rule holds
  here for English prose, which is what its vocabulary
  was built from; carry the method, never the number.
```

**The first table looks like the rule failing.** Eight characters of `catalyst` should be about two
tokens and the bill says ten. The second table finds why — and it is careful about how.

Adding one more `cat` raises the count by exactly one, four times running. **That measures the
slope, and a slope does not fix an intercept**: if the first `cat` had cost two tokens the slope
would still be one, and extrapolating back would give the wrong answer. So the program measures
the intercept directly, by sending no text at all, and gets the same figure. That is the **chat
template** — the markup the provider wraps round your text so the model sees a conversation turn —
and you pay for it every call. Seven of ten tokens, 70 per cent of that short call, are not your
question.

> **Note:** This is not Chapter 36's [**prompt template**]{.noindex}, and the two are easier to confuse than
> they look. Chapter 36's is a templated message or workflow an MCP server offers to [**users**]{.noindex},
> and its own row adds "not a tool, and not something the model selects" — which is the contrast
> that matters: somebody published it for a person to choose. This one is markup you never write and never
> see, added by the provider between your string and the model, and its only visible trace is the
> seven tokens on your bill. One is a thing you choose to use; the other is a thing you are
> charged for.

The third table confirms the figure a third time, from a direction the first two cannot reach: the
embeddings endpoint wraps nothing round your text, so its counts *are* your tokens — and on every
row where the two vocabularies agree, they agree with the chat model's figure once the template
comes off.

**The third table is the one to carry.** The same four strings, the same key, the same provider —
counted by the embeddings endpoint, which uses an older vocabulary. Three rows agree *exactly*.
The Tamil question is 8 tokens to the chat model and 26 to the embedding model: **the same string
costing 3.25 times as much depending on which vocabulary reads it.**

So the lesson is not that non-Latin scripts cost more. It is that **a characters-per-token figure
does not transfer between vocabularies**, and that one provider ships more than one of them. Note
what the three agreeing rows do and do not license: three strings of different kinds agreed
exactly, so the figure is not arbitrary — but three strings establish nothing about *most* text,
and the claim is about crossing a model boundary rather than about the figure being meaningless. Chapter 10's rule is a rule about English prose
under a vocabulary built mostly from English prose, and it holds here almost exactly, at 4.29
characters to the token. Carry the method, never the number.

> **Note:** The Tamil string is in the program as a `\uXXXX` escape and the table prints an English
> label, because this book's font has no Tamil glyphs — printing it put sixty-eight missing
> characters in the PDF the first time. The escape is also an exact record of what was measured,
> which a glyph in a listing is not.

> **Warning:** Chapters 43 and 44 compare embedding models, and chapter 53 budgets tokens. Both
> inherit this: a corpus you priced with one model's vocabulary can cost three times as much under
> another's, and nothing in either API warns you. Price with the vocabulary you will actually use.

## Step 4: Find Where the Time Goes

A local server will tell you how long it spent reading the input and how long writing the reply. A
hosted one tells you neither, so you measure from outside: start a clock, stream the reply, and
note when the first token lands.

```python
"""Where the time goes, when the server will not tell you.

A local server reports how long it spent reading the input and how
long writing the reply. A hosted one reports neither, so you measure
from outside: start a clock, stream the reply, and note when the
first token lands. That gap and the pace after it are the two
numbers chapter 52 works with, and chapter 15 is why they differ.
"""

import json
import random
import statistics
import time
import urllib.request

from call import MODEL, TIMEOUT, URL, key

LONG = "Write 400 words about the sea. Do not stop early."
SHORT = "List three colours."


def stream(prompt, max_tokens):
    """Return (ms to first token, gaps between tokens, count, why).

    The gaps are a list, not an average. A short reply arrives in
    one burst, so (total - first) / count is near zero and measures
    the network's buffering rather than the model's pace. A median
    gap over a reply long enough to have gaps is the honest figure.
    """
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0, "stream": True,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    start = time.perf_counter()
    first = None
    last = None
    gaps = []
    seen = 0
    why = None
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data: ") or line.endswith("[DONE]"):
                continue
            chunk = json.loads(line[6:])["choices"][0]
            if chunk.get("delta", {}).get("content"):
                now = time.perf_counter()
                seen += 1
                if first is None:
                    first = (now - start) * 1000
                else:
                    gaps.append((now - last) * 1000)
                last = now
            if chunk.get("finish_reason"):
                why = chunk["finish_reason"]
    return first, gaps, seen, why


REPEATS = 3

if __name__ == "__main__":
    for _ in range(2):
        stream(SHORT, 5)                   # warm the connection

    print(f"  Model {MODEL}.")
    print(f"  Each row is {REPEATS} runs; the figures are medians of")
    print("  those runs. The gap columns are over every gap seen.")
    print("  The caps are visited in a SHUFFLED order, so that the")
    print("  provider's load drifting over the loop cannot be")
    print("  mistaken for an effect of the cap.\n")
    print("    asked   got   first token   mean gap   median   max")
    ttfts, means, maxes, medians = [], [], [], []
    caps = [1, 25, 100, 400]
    random.Random(40).shuffle(caps)
    rows = []
    for cap in caps:
        runs = [stream(LONG, cap) for _ in range(REPEATS)]
        t = statistics.median(r[0] for r in runs)
        g = [x for r in runs for x in r[1]]
        seen = statistics.median(r[2] for r in runs)
        ttfts.append(t)
        if g:
            means.append(sum(g) / len(g))
            maxes.append(max(g))
            medians.append(statistics.median(g))
            rows.append((cap, seen, t, sum(g)/len(g),
                         statistics.median(g), max(g)))
        else:
            rows.append((cap, seen, t, None, None, None))
    for cap, seen, t, mean, med, mx in sorted(rows):
        if mean is None:
            print(f"    {cap:>5} {seen:>5.0f} {t:>13.0f}"
                  f" {'-':>10} {'-':>8} {'-':>5}")
        else:
            print(f"    {cap:>5} {seen:>5.0f} {t:>13.0f}"
                  f" {mean:>10.1f} {med:>8.1f} {mx:>5.0f}")

    print(f"\n  Three things. First, the first-token column spans")
    print(f"  {min(ttfts):.0f} to {max(ttfts):.0f} ms and does not trend with how much was")
    print("  asked for. It is the wait before anything comes back")
    print("  and it does not know what follows; the spread is the")
    print("  network and the provider's load.\n")
    print(f"  Second, the mean gap holds near {sum(means)/len(means):.0f} ms across a")
    print("  sixteen-fold change in output length. That is the")
    print("  per-token pace, and it is the number to carry.\n")
    mean_gap = sum(means) / len(means)
    print("  Third, and this is the one you would not guess: the")
    span = (f"{min(medians):.1f}" if min(medians) == max(medians)
            else f"{min(medians):.1f} to {max(medians):.1f}")
    print(f"  median gap is {span} where the mean is {mean_gap:.1f},")
    print(f"  and the largest gap is {max(maxes)/mean_gap:.0f} times that")
    print("  mean. Tokens do not arrive evenly - they arrive in")
    print("  bursts, with most of them landing in the same network")
    print("  read as their neighbour. So a median is the wrong")
    print("  statistic here, and a progress bar that assumes a")
    print("  steady stream will stutter.\n")
    print("  Chapter 15 says why the two behave differently -")
    print("  reading the input can work on all of it at once and")
    print("  writing cannot - and chapter 52 owns both metrics in")
    print("  production. This is them, from outside, with a clock.\n")

    print("  One more thing, because it is easy to mismeasure.")
    print("  Raise the cap on a question the model wants to")
    print("  finish:\n")
    print("    asked   got   ended because")
    for cap in (2, 10, 50):
        _, _, seen, why = stream(SHORT, cap)
        print(f"    {cap:>5} {seen:>5}   {why}")
    print("\n  The cap is a CEILING and not a length. Past the point")
    print("  where the model has finished, raising it changes")
    print("  nothing, and the reason reported changes with it -")
    print("  chapter 13 owns those endings and this is two of them.")
    print("  Measure a per-token rate on a reply that stopped")
    print("  because of the cap, never one that stopped on its own.")
```

```text
  Model gpt-4o-mini-2024-07-18.
  Each row is 3 runs; the figures are medians of
  those runs. The gap columns are over every gap seen.
  The caps are visited in a SHUFFLED order, so that the
  provider's load drifting over the loop cannot be
  mistaken for an effect of the cap.

    asked   got   first token   mean gap   median   max
        1     1           719          -        -     -
       25    25          1133        9.9      0.0   163
      100   100           822       10.6      0.0   140
      400   400           665       10.1      0.1   123

  Three things. First, the first-token column spans
  665 to 1133 ms and does not trend with how much was
  asked for. It is the wait before anything comes back
  and it does not know what follows; the spread is the
  network and the provider's load.

  Second, the mean gap holds near 10 ms across a
  sixteen-fold change in output length. That is the
  per-token pace, and it is the number to carry.

  Third, and this is the one you would not guess: the
  median gap is 0.0 to 0.1 where the mean is 10.2,
  and the largest gap is 16 times that
  mean. Tokens do not arrive evenly - they arrive in
  bursts, with most of them landing in the same network
  read as their neighbour. So a median is the wrong
  statistic here, and a progress bar that assumes a
  steady stream will stutter.

  Chapter 15 says why the two behave differently -
  reading the input can work on all of it at once and
  writing cannot - and chapter 52 owns both metrics in
  production. This is them, from outside, with a clock.

  One more thing, because it is easy to mismeasure.
  Raise the cap on a question the model wants to
  finish:

    asked   got   ended because
        2     2   length
       10     6   stop
       50     6   stop

  The cap is a CEILING and not a length. Past the point
  where the model has finished, raising it changes
  nothing, and the reason reported changes with it -
  chapter 13 owns those endings and this is two of them.
  Measure a per-token rate on a reply that stopped
  because of the cap, never one that stopped on its own.
```

**The first-token column does not trend with how much you asked for**, which is the right shape:
it is the wait before anything comes back, and it cannot know what follows. The spread inside it
is the network and the provider's load — not your request and not the model. Expect your own
figures to differ from the printed ones; nothing here measures by how much.

The program visits the caps in a shuffled order on purpose. Walk them in increasing order and the
provider's load drifting over the half-minute the loop takes is indistinguishable from an effect
of the cap — one of my own runs came out monotonically increasing, which on a tidier presentation
would have read as a trend that is not there.

**Be exact about what the shuffle buys, because it is less than it sounds.** The seed is fixed so
the order is reproducible, and on this seed it is 25, 1, 100, 400 — which still leaves the two
largest caps last. The three repeats of each cap are also consecutive rather than interleaved. So
the shuffle breaks the correlation between a cap and its *position* and does not break the
correlation between a cap and the particular half-minute it was measured in. What makes the claim
worth anything is the repetition, and the honest statement is that no run has shown a trend rather
than that a trend has been ruled out.

**The mean gap holds steady across the same sixteen-fold change**, and that is the per-token pace
— which is Chapter 15's [**time per token**]{.noindex}, measured from outside rather than reported by the
server. The first column is its [**time to first token**]{.noindex}. Chapter 15 named both and said why they
behave differently: reading the input can work on all of it at once and writing cannot, because
each output token is chosen from the ones already written. Chapter 52 owns both in production;
this is them, with a clock.

**And the last two columns are the ones you would not guess.** The *median* gap sits at or near
zero while the mean is around ten milliseconds, and the largest single gap is more than a dozen
times that mean. **Tokens do not arrive evenly — they arrive in bursts**, most of them landing in
the same network read as their neighbour. Two consequences: a median is the wrong statistic for
this quantity, and a progress bar built on the assumption of a steady stream will stutter whatever
you do to it.

> **Note:** Do not read the bursting as the model producing tokens in clumps. Nothing here shows
> that, and nothing here could: a median of zero between deltas is equally consistent with the
> model emitting evenly and something between it and your socket batching what it sends. Which of
> those it is, this measurement cannot say. What follows either way is that the mean gap — the
> total divided by the count, and so immune to the clumping — is the figure that corresponds to a
> pace, and the median is not.

**Then the detour, which is here because it is easy to mismeasure.** Raise the cap on a question
the model wants to finish and nothing happens: six tokens whether you allow ten or fifty, and the
reason reported changes from `length` to `stop`. **The cap is a ceiling, not a length** — two of
Chapter 13's endings, and the reason you measure a per-token rate on a reply the cap stopped rather
than one that stopped on its own.

## Step 5: Run It Twenty Times

Chapter 20 said one run is not a score. Chapter 13 said temperature zero is not a guarantee and
gave four reasons. Three of those four need a shared, hosted service — and now you are on one.

```python
"""The same prompt twenty times, against a provider.

Chapter 13 gives four reasons temperature 0 is not a guarantee.
Three of them need a shared, hosted service, and this is one. So
unlike a model on your own machine, there is something here to see.
"""

import statistics
import time
from collections import Counter

from call import MODEL, call, text

RUNS = 20
PROMPT = "Name one colour. One word only."


def normalise(reply):
    """Strip what is not an answer. Counting distinct replies without
    this measures your own string handling as well as the model."""
    return reply.strip().strip(".").strip().lower()


if __name__ == "__main__":
    call("warm up", max_tokens=1)

    replies, times = [], []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        r = call(PROMPT, max_tokens=5, temperature=0.0)
        times.append((time.perf_counter() - t0) * 1000)
        replies.append(text(r))

    raw = Counter(replies)
    norm = Counter(normalise(x) for x in replies)

    print(f"  Model {MODEL}.")
    print(f"  {RUNS} identical calls, temperature 0.\n")
    print(f"    distinct replies, as returned   {len(raw)}")
    for k, n in raw.most_common():
        print(f"        {k!r:<12} {n:>2}")
    print(f"    distinct replies, normalised    {len(norm)}")
    for k, n in norm.most_common():
        print(f"        {k!r:<12} {n:>2}")

    print(f"\n    fastest {min(times):7.0f} ms")
    print(f"    slowest {max(times):7.0f} ms")
    print(f"    median  {statistics.median(times):7.0f} ms")
    print(f"    slowest / fastest  {max(times)/min(times):.2f}\n")

    if len(norm) > 1:
        top = norm.most_common(1)[0]
        print(f"  Temperature 0 and {len(norm)} different answers in {RUNS}")
        print(f"  calls. The commonest came back {top[1]} times out of {RUNS},")
        print(f"  so a single call would have shown you one answer")
        print(f"  {top[1]/RUNS:.0%} of the time and the other one otherwise.")
        print("  Chapter 13 said temperature 0 is not a guarantee and")
        print("  gave four reasons; three of them need a shared")
        print("  hosted service, and you are on one. Nothing here is")
        print("  randomness in the sampler - the sampler was asked")
        print("  for the top token every time.\n")
    else:
        print(f"  All {RUNS} agreed this time, which proves nothing:")
        print("  chapter 13's four reasons are about what CAN move,")
        print("  and a run where nothing moved is one sample.\n")

    print(f"  The clock moved too, by a factor of {max(times)/min(times):.1f} on the")
    print("  same call. A single timing is not a latency: quote a")
    print("  range and say how many runs it came from.\n")

    if len(raw) > len(norm):
        print(f"  And read the two distinct counts against each other.")
        print(f"  Raw says {len(raw)} and normalised says {len(norm)}: a full stop")
        print("  made one answer look like two. A distinct-reply")
        print("  count measures your normalising as much as it")
        print("  measures the model, and every later lab in this")
        print("  part counts something.")
    else:
        print("  The two distinct counts agree here, so normalising")
        print("  changed nothing this time. Keep it anyway: it costs")
        print("  one function and it is the difference between")
        print("  measuring the model and measuring your own strings.")
```

```text
  Model gpt-4o-mini-2024-07-18.
  20 identical calls, temperature 0.

    distinct replies, as returned   2
        'Azure.'     12
        'Blue.'       8
    distinct replies, normalised    2
        'azure'      12
        'blue'        8

    fastest     746 ms
    slowest    2029 ms
    median      897 ms
    slowest / fastest  2.72

  Temperature 0 and 2 different answers in 20
  calls. The commonest came back 12 times out of 20,
  so a single call would have shown you one answer
  60% of the time and the other one otherwise.
  Chapter 13 said temperature 0 is not a guarantee and
  gave four reasons; three of them need a shared
  hosted service, and you are on one. Nothing here is
  randomness in the sampler - the sampler was asked
  for the top token every time.

  The clock moved too, by a factor of 2.7 on the
  same call. A single timing is not a latency: quote a
  range and say how many runs it came from.

  The two distinct counts agree here, so normalising
  changed nothing this time. Keep it anyway: it costs
  one function and it is the difference between
  measuring the model and measuring your own strings.
```

**Temperature zero, twenty identical calls, two different answers.** Twelve `Azure.` and eight
`Blue.` on the run printed above, so a single call would have shown you the commoner one most of
the time and the other one otherwise — and the split itself moves between runs, which is the
point rather than a flaw in it. **This is Chapter 13's claim happening rather than being argued**, and it is worth
sitting with: nothing here is randomness in the sampler, which was asked for the top token every
time. The causes are the ones Chapter 13 named — what else is in the batch, and what the provider
changed under you — and they are properties of a shared service rather than of your code.

[**The clock moved too**]{.noindex}, by a factor of two or more on the same call — read the
fastest and slowest in the block. A single timing is not a latency: quote a range and say how many
runs it came from.

**And the program reports both distinct counts on purpose**, even on the runs where they agree —
as they do here, because both replies happen to end in a full stop. The branch is there because
the two counts *can* differ by nothing more than punctuation, and when they do, the raw figure is
measuring your string handling rather than the model. Every later lab in this part counts
something, and that is the cheapest possible place to learn the habit.

> **Warning:** This is the result that should change how you read a demonstration. Somebody shows
> you a prompt that works, at temperature zero, once. On these numbers that evidence is consistent
> with a prompt that works three times in five. Chapter 20's fixed set and paired comparison
> exist for exactly this, and you have just watched the reason.

## Step 6: Break It on Purpose

No program. Four small failures, because knowing what each looks like is worth more than a clean
run.

[**Unset the key**]{.noindex} — `unset OPENAI_API_KEY` in a fresh shell — and run `call.py`. You
get the message the file raises, not a traceback through `urllib` and not a confusing 401.

[**Corrupt the key**]{.noindex} — `OPENAI_API_KEY=sk-nonsense python3 call.py` — and you get
HTTP 401 with a body that says the key is invalid. Read the body, not just the status: Chapter 19's
rule that a status alone is not a diagnosis starts here.

[**Ask for a model that does not exist**]{.noindex} — change `MODEL` to
`gpt-4o-mini-2099-01-01` — and you get a 404 naming the model. That is the failure a pinned
snapshot gives you when the provider retires it, and it is the good case: loud, immediate and
specific. The bad case is a floating name that keeps working and means something different, which
is step 2.

[**Set `max_tokens` to 1**]{.noindex} and ask something that needs a sentence. You get one token
and `finish_reason` of `length`. Nothing is wrong and nothing warns you; the reply is simply cut
off. A pipeline that does not check `finish_reason` will carry that truncation forward as though it
were an answer.

## What To Actually Do

1. **Pin the model to a dated snapshot**, and write the pin in the one file that calls the model.
2. **Read the key from the environment**, raise if it is missing, and never let it reach a file in
   the project or a line of output.
3. **Read the `model` field back on every result you keep.** It is one column and it is the only
   thing that catches a silent version change.
4. **Find your template's size with the slope trick** — add one known token at a time — and budget
   it once per call rather than once per token.
5. **Estimate your own text with Chapter 10's rule, then add the template.** Check the rule against
   the vocabulary you will actually use; the same string cost 3.25 times as much under the other
   one here.
6. **Measure time to first token separately from the pace after it**, and report the mean gap rather
   than the median, because the stream arrives in bursts.
7. **Treat the output cap as a ceiling** and check `finish_reason`, not just the length.
8. **Report a range and a count of runs**, never one timing.
9. **Normalise before you count distinct anything.**
10. **Say which of your numbers are the model's and which are the network's.** The token counts are
    the model's; every millisecond above carries the internet.

## Summary, Key Terms, and Review Questions

### Summary

The first lab installs nothing: a folder, a virtual environment, the standard library and a key in
the environment. `call.py` is the only file that reaches a model, it raises if the key is absent,
and it pins a **model snapshot** — a dated name like `gpt-4o-mini-2024-07-18` rather than the
floating `gpt-4o-mini`. One timeout and no retry, because a lab that retries measures something
else. **The reply's `usage` block is the bill itemised**, and two sub-counts matter later even at
zero: `cached_tokens` is Chapter 52's prefix caching as a field, `reasoning_tokens` is Chapter 53's
invisible output. **Asking for the floating name returned the dated one**, so pinning is not about
being unable to find out what served you — it is that the answer can change between runs and
nothing raises; read the `model` field back regardless, which is Chapter 54's subject in one line.
**Counting tokens finds the chat template.** Chapter 10's rule says `catalyst` is about two tokens
and the bill says ten; adding one `cat` at a time raises it by exactly one, so the slope is one and
the intercept is **7 tokens of chat template, charged every call** — 70 per cent of that short call
is not the question. Then the same four strings through the embeddings endpoint, which uses an older
vocabulary: three rows agree exactly and the Tamil question is 8 tokens against 26, **the same
string costing 3.25 times as much depending on which vocabulary reads it.** A characters-per-token
figure does not transfer between vocabularies, and one provider ships more than one.
**Time to first token does not trend with output length**, because it is the wait before anything
returns, and the caps are visited in a shuffled order so the provider's drift cannot be read as an
effect of the cap; the **mean inter-token gap holds steady** across a sixteen-fold change, and that
is Chapter 15's time per token measured from outside. The **median gap sits near zero while the
largest is more than a dozen times the mean**: tokens arrive in bursts — a property of delivery,
not of generation — so a median is the wrong statistic and a steady progress bar will stutter. **The output cap is a ceiling, not a length** — six tokens whether you allow ten
or fifty, with the reason moving from `length` to `stop`, which are two of Chapter 13's endings.
**Twenty identical calls at temperature 0 returned two different answers**, and the split moves
between runs: Chapter 13's claim happening rather than argued, with three of its four causes live
because the service is shared. The clock moved by a factor of two or more on the same call, so a
single timing is not a latency.

### Key Terms

| Term | Meaning |
|---|---|
| **Chat template** | The markup a provider wraps round your text so the model sees a conversation turn. A fixed number of tokens — 7 for this model — charged on every call, and not Chapter 36's prompt template |
| **Model snapshot** | A model name with a date in it, as against a family name the provider may repoint. The thing to pin, and the thing to read back out of the reply |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Finding a chat template's size | Add one known token at a time; the slope is 1 and the intercept is the template |
| What a short prompt really costs | Your tokens plus the template. Three plus seven means 70 per cent of the call is not your prompt |
| What a chars-per-token figure belongs to | Not a language, and not transferable. The same string was 8 tokens to one vocabulary and 26 to another from the same provider, while English and code were identical under both |
| The two latency numbers | Time to first token, then the mean gap after it. The first does not depend on output length; the second is the pace |
| Why the median gap is useless | Tokens arrive in bursts, so the median sits near zero while the largest gap is more than a dozen times the mean. Report the mean |
| What the output cap is | A ceiling, not a length. Check `finish_reason`, not only the length |
| What temperature 0 buys from a provider | Not repeatability. Twenty identical calls gave two different answers, on a split that moves between runs |
| What to report for a latency | A range and the number of runs, never one timing |
| Before counting distinct replies | Normalise |

### Review Questions

1. Why pin a model to a dated name when the reply tells you which model answered anyway?
2. Your prompt is eight characters and you are billed ten tokens. Where did the other seven come
from, and how would you find that out for a model you have never used?
3. You priced a corpus at 1.2 million tokens using your chat model, then embedded it and the bill
was three times what you expected. What happened?
4. Which of time-to-first-token and the per-token pace depends on how much output you asked for,
and why?
5. You run the same prompt twenty times at temperature 0 against a provider and get two different
answers. What may you conclude, and what does it do to "I tried the prompt and it worked"?
6. A colleague reports a latency of 800 ms. What do you ask?

### Review Answers

1. Because the reply telling you is a check and not a control. A floating name can resolve to one
snapshot today and another tomorrow, and nothing raises when it changes — you find out from a score
that moved. Pinning the dated name makes the change *loud*: when the provider retires that snapshot
you get a 404 naming it, which is immediate and specific and happens at a moment you choose to deal
with. Then read the `model` field back anyway, and log it with anything you keep, because that one
column is the difference between "the score dropped in March" and "the score dropped in March, when
the model changed". Chapter 54 owns why a silent version change is the hardest kind of failure to
attribute.
2. They are the **chat template** — the markup the provider wraps round your text so the model sees
a conversation turn. You pay for it on every call, it does not grow with your prompt, and it is
this model's number rather than a general one. To find it for a model you have never used, send a
prompt of one known token, then the same token twice, three times, four: if the bill rises by
exactly one each time, the slope is one token and whatever is left after subtracting your own
tokens is the template. The consequence is that a short prompt is much dearer per useful token than
its length suggests — seven of ten here — which is a real argument for putting several questions in
one call.
3. The two models do not share a vocabulary. Measured on the same four strings with the same key,
English prose and a line of Python came out *identical* under both, and a Tamil question came out 8
tokens to the chat model and 26 to the embedding model — the same string costing 3.25 times as much.
So a token count does not transfer between vocabularies, and a corpus priced with one model can
cost several times more under another. Nothing in either API warns you. Note what the identical
rows mean for the rule: the Python line is not English prose and carried exactly, so the thing
that failed to carry was a script one vocabulary knows and the other does not — which you cannot
tell by looking at your corpus. **So price with the vocabulary you will actually use**, and do not
carry a characters-per-token figure across a model boundary at all, whatever your corpus is made
of.
4. Neither depends on it in the way people expect. **Time to first token does not**: it moved
around across a sixteen-fold change in requested output without trending with it, because it is
the wait before anything comes back and cannot know what follows — its spread is the network and
the provider's load, which is also why the caps have to be visited in a shuffled order before the
claim means anything. **The per-token pace does not either**: the mean gap held steady across the
same range.
What depends on output length is the *total*, which is the first number plus the second times the
number of tokens. The reason the two behave differently is Chapter 15's: reading the input can work
on all of it at once and writing cannot, because each output token is chosen from the ones already
written. One more thing worth saying: report the mean gap and not the median, because the median
sits at or near zero while the mean is around ten milliseconds — tokens arrive in bursts, so the
median is measuring the clumping and not the pace.
5. You may conclude that temperature zero is not repeatability, which is exactly what Chapter 13
said and gave four reasons for; three of them need a shared hosted service and you are on one, so
what moved is what else was in the batch and what the provider changed, not randomness in the
sampler — it was asked for the top token every time. What it does to "I tried it and it worked" is
most of the damage: the commoner answer came back a majority of twenty times, so one successful
call is consistent with a prompt that fails a substantial minority of the time. That is why Chapter 20 insists on a
fixed set of cases and a paired comparison, and this is the cheapest place in the book to watch the
reason.
6. How many runs it came from, and whether it is a mean, a median or the one they happened to see.
Then whether the first call was included, and whether it is time to first token or time to the
whole reply — those are different quantities and only one of them depends on the output length.
Twenty identical calls here spanned a factor of two or more, so any single figure from that
distribution is a sample. And then the question that decides whether the number means
anything: what was the output length, because the total is the first token plus the pace times the
tokens after it.

> **You understand this when** somebody shows you a prompt that worked at temperature zero and your
> first question is how many times they ran it.
