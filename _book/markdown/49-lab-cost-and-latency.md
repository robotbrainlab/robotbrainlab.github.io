# Lab: Measure and Reduce Cost and Latency

Chapter 1 said the wait has two phases and you feel them separately. Chapter 15 said why, from
the inside: prefill does the whole prompt in one pass and is limited by arithmetic, decode does
one token at a time and is limited by reading the parameters out of memory. It named both numbers
— [**time to first token**]{.noindex} and [**time per token**]{.noindex} — and then said plainly
where the levers live and
that this is not it.

So this chapter pulls three of them and watches the numbers move. It is the first chapter in the
book where the question is not *what is true of these systems* but *what is true of mine*, and the
difference turns out to matter more than I expected: of the three levers, one does nothing at all
on this system's own traffic, and the reason is a property of the traffic rather than of the lever.

*The problem.* I know what the levers are. I have never pulled one and watched the number move.

*What is not in scope, and who owns it.* Chapter 15 owns prefill, decode, the key–value cache,
batching, quantisation, mixture of experts, active parameters, memory-bound and compute-bound, and
it owns the arithmetic underneath every figure here; this chapter measures from the outside and
opens nothing. Chapter 1 owns latency and the two-phase wait. Chapter 52 owns the menu of levers in
production — what to measure, prompt-prefix caching and ordering for it, routing and cascades,
application-level response caching, and, if you serve models yourself, continuous batching, a
paged cache, speculative decoding and quantisation. **This chapter pulls the three its own Covers
list names and no more**, and because it comes first it owns the two terms it needs to pull them:
**prompt-prefix cache** and **cascade**. Chapter 52 uses both and introduces neither.
**Chapter 53 owns the bill as a product constraint and will measure against the baseline this
chapter produces**, which is the one thing here that is meant to be quoted later. No judge: every
check is code. No retrieval measurement — Chapters 44 and 45 settled that pipeline and this
chapter reuses it without re-arguing it. And no quantisation and no self-hosting: both are
levers you can only pull on a machine you run, and this lab calls a hosted service.

## Step 1: The Workload, and Why Three Shapes

A lever is worth what it is worth on your own traffic. So the baseline is a real request from the
system this book has been building — Chapter 45's pipeline on the shipped corpus, dense retrieval
over the 176 chunks, a context filled by rank and stopped — rather than a prompt invented to show
a lever working.

Three shapes, and the third is here for a reason that only became clear once the first two were
measured.

`grounded` is the system's own traffic: the eight corpus queries with their retrieved
passages, a context of about 2,300 characters, a short answer.

`essay` is the same retrieval asked for a long answer. The same input, far more output. It
exists because Chapter 15's two halves respond to different things, and a single shape cannot show
that: holding the input and changing the output is the only way to find out whether time per token
is really about the output.

`upfront` is the arrangement Chapter 35 priced and rejected — the whole policy library in front
of every request instead of opening a document when a step needs it. It is here because of a
number nobody mentions in the same breath as prefix caching: **the provider's prompt cache has a
minimum prompt length, and this system's retrieved requests are under it.**

```python
"""The workload every measurement in this chapter runs on.

A lever is only worth what it is worth on your own traffic, so the
baseline has to be a real request from a real system rather than a
prompt invented to show a lever working. This is chapter 45's
pipeline on the shipped corpus: dense retrieval over the 176 chunks,
a context filled by rank and stopped, one answer call.

THREE SHAPES, because chapter 15's two halves respond to different
things, and because one of this chapter's levers turns out not to
apply to the first two at all.

  grounded  the 8 corpus queries with their retrieved passages.
            A 2,300-character context and a short answer.
  essay     the same retrieval, asked for a long answer. Nearly
            the same input - 4 per cent more, because the
            instruction is longer - and nine times the output.
  upfront   no retrieval: the eight policy documents in front of
            every request, and the question after them. Four times
            the input, and 23 per cent FEWER output tokens, because
            a model given the whole library answers more briefly.

What is held across the shapes is the instruction and the token cap,
not the realised lengths. The figures above are in order.py's own
table, and they are reported because "holds the input" and "holds
the output" are approximations - large enough to name, far smaller
than the multipliers the comparisons turn on.

The first two are chapter 45's pipeline, which is this book's own
system. The third is the arrangement chapter 35 priced and rejected -
loading the library rather than opening a document when a step needs
it - and it is here for a reason the next programs make plain: the
provider's prompt cache has a MINIMUM prompt length, this system's
retrieved requests are under it, and the up-front design is over it.
So the lever that makes a prompt cheaper to send again applies to
the design chapter 35 showed was more expensive to send at all.
"""
import json
import pathlib

import search
from key import queries

OUT = pathlib.Path("work.json")
BUDGET = 2500

POLICIES = ("refunds-policy", "returns-clearance",
            "delivery-exceptions", "delivery-fees",
            "refund-to-a-closed-card", "refunds-faq",
            "returns-standard", "where-is-my-refund")
DOCS = pathlib.Path("corpus/docs")


def library():
    """Every policy document, in a fixed order. The order is fixed
    because a prefix that is reused has to be byte-identical, and a
    set iterated in a different order on the next request is the
    commonest way to lose a cache hit without changing a word."""
    return "\n\n".join((DOCS / f"{d}.md").read_text()
                        for d in POLICIES)


SHORT = (
    "Answer the question using only the passages below. Answer in "
    "one or two sentences."
)
LONG = (
    "Answer the question using only the passages below. Explain the "
    "rule in full, give every condition and exception the passages "
    "state, and say what a customer should do next and why. Write "
    "at least three paragraphs."
)
INSTRUCTION = {"grounded": SHORT, "essay": LONG, "upfront": SHORT}
CAP = {"grounded": 120, "essay": 700, "upfront": 120}
SHAPES = tuple(INSTRUCTION)


def passages(question, cache, budget=BUDGET):
    """Chapter 28's fill: by rank, and it stops."""
    order, _ = search.dense(question, cache)
    kept, left = [], budget
    for cid in order:
        block = f"[{cid}] {search.BY_ID[cid]['text']}\n"
        if len(block) > left:
            break
        kept.append(cid)
        left -= len(block)
    return kept


def build():
    cache = search.vectors()
    out = []
    for qid, q in sorted(queries().items()):
        kept = passages(q, cache)
        body = "\n".join(f"[{c}] {search.BY_ID[c]['text']}"
                         for c in kept)
        out.append({"query_id": qid, "question": q,
                    "passages": kept, "body": body})
    OUT.write_text(json.dumps(out, indent=1))
    return out


def requests():
    return json.loads(OUT.read_text()) if OUT.exists() else build()


def messages(row, shape, order="stable-first"):
    """One request, assembled in one of two orders.

    stable-first  instruction, then passages, then the question
    question-first  the question, then the instruction and passages

    The two hold the same text and differ only in where the part
    that changes between requests sits. That is the whole of the
    reordering lever, and `order.py` is what it is worth.
    """
    instr = INSTRUCTION[shape]
    body = library() if shape == "upfront" else row["body"]
    if order == "stable-first":
        content = f"{instr}\n\n{body}\n\nQuestion: {row['question']}"
    elif order == "question-first":
        content = f"Question: {row['question']}\n\n{instr}\n\n{body}"
    else:
        raise ValueError(order)
    return [{"role": "user", "content": content}]


if __name__ == "__main__":
    rs = requests()
    print(f"  {len(rs)} requests, the corpus's own 8 queries.\n")
    print("  id   passages   context chars   question")
    for r in rs:
        print(f"  {r['query_id']:<5}{len(r['passages']):>8}"
              f"{len(r['body']):>15}   {r['question'][:28]}")
    body = sum(len(r["body"]) for r in rs) / len(rs)
    print(f"\n  Mean context: {body:,.0f} characters, about"
          f" {body / 4:,.0f} tokens")
    print("  by chapter 10's rule - which this chapter does not need,")
    print("  because every token count below is the provider's own.\n")
    MIN = 1024
    print("  shape      chars   ~tokens   cap   over the cache's")
    print("                                      minimum of 1,024?")
    for shape in SHAPES:
        n = sum(len(messages(r, shape)[0]["content"]) for r in rs)
        mean = n / len(rs)
        approx = mean / 4
        print(f"  {shape:<11}{mean:>6,.0f}{approx:>10,.0f}"
              f"{CAP[shape]:>6}   "
              f"{'yes' if approx > MIN else 'NO'}")
    print("\n  The approximation is chapter 10's four characters to")
    print("  the token and it is only used to say which side of the")
    print("  minimum a shape is on. Every token count in the rest of")
    print("  this chapter is the provider's own.\n")
    for shape in SHAPES:
        a = len(messages(rs[0], shape)[0]["content"])
        b = len(messages(rs[0], shape, "question-first")[0]["content"])
        print(f"  {shape}: {a:,} characters either way ({a == b})")
    same = {len(messages(rs[i], s)[0]["content"])
            == len(messages(rs[i], s, "question-first")[0]["content"])
            for i in range(len(rs)) for s in SHAPES}
    print(f"\n  Every request holds the same text in both orders:"
          f" {same == {True}}")
    print("  So a difference the next programs find is about WHERE")
    print("  the part that changes sits, and not about length.")
```

```text
  8 requests, the corpus's own 8 queries.

  id   passages   context chars   question
  q1          8           2366   How long do I have to return
  q2         11           2422   Why is my refund taking so l
  q3          6           2353   How much does delivery cost 
  q4          5           1899   What is HL-2208?
  q5         10           2453   Is a refund 14 days or 30 da
  q6          8           2297   My parcel arrived damaged. W
  q7         10           2122   What does Harbour Plus inclu
  q8         11           2368   Can I return a clearance ite

  Mean context: 2,285 characters, about 571 tokens
  by chapter 10's rule - which this chapter does not need,
  because every token count below is the provider's own.

  shape      chars   ~tokens   cap   over the cache's
                                      minimum of 1,024?
  grounded    2,415       604   120   NO
  essay       2,545       636   700   NO
  upfront    10,447     2,612   120   yes

  The approximation is chapter 10's four characters to
  the token and it is only used to say which side of the
  minimum a shape is on. Every token count in the rest of
  this chapter is the provider's own.

  grounded: 2,501 characters either way (True)
  essay: 2,631 characters either way (True)
  upfront: 10,452 characters either way (True)

  Every request holds the same text in both orders: True
  So a difference the next programs find is about WHERE
  the part that changes sits, and not about length.
```

**The retrieved requests are about 600 tokens and the cache's minimum is 1,024.** So the lever this
chapter was going to demonstrate does not apply to the traffic this book has spent nine chapters
building, and no amount of reordering will change that. That is the first thing to find out about
a lever and it is not the thing a chapter about levers usually tells you. The up-front shape is
over the minimum at about 2,600 tokens, so the lever can be measured there — and the design it
can be measured on is the one Chapter 35 showed costs more to send in the first place. Step 3 is
what that is worth.

**Every request holds the same text in both orders, and the program asserts it.** That is what
makes the next two steps about *where the part that changes sits* rather than about length: the
instruction, the passages and the question are the same characters, moved.

> **Note:** The token counts in that table are Chapter 10's four-characters-to-the-token rule, and
> they are used for exactly one thing — saying which side of the minimum a shape is on. Every
> other token count in this chapter is the provider's own, out of the usage block, because the
> whole chapter is about a bill and an estimate is not a bill.

> **Warning:** The document order inside the up-front shape is fixed in the program and that is
> load-bearing. A prefix is reused only if it is identical, so a set of documents iterated in a
> different order on the next request is the same text and a different prefix — and the cache
> silently misses. It is the easiest way to lose this lever without changing a word of your
> prompt, and the fix is a tuple rather than a set.

## Step 2: The Two Halves of the Wait

Chapter 15 names both numbers and explains them from the inside, and that explanation makes a
prediction this program can test from the outside without opening anything:

- [**time to first token**]{.noindex} should move with the *input*, because prefill handles the
  whole prompt
  before a word comes back — Chapter 1 puts it as *send more, wait longer*;
- [**time per token**]{.noindex} should not, because decode does one position at a time whatever
  the prompt
  was.

The three shapes make the test possible, one change at a time. `essay` against `grounded` changes
the output and holds the input. `upfront` against `grounded` quadruples the input and holds the
output. That is Chapter 18's change-one-thing applied to a measurement, and Chapter 47's lesson —
two arms differing in two ways answer neither question.

```python
"""Two ways to make one call, because they measure different things.

`timed` streams and records TIME TO FIRST TOKEN and TIME PER TOKEN -
chapter 15's two halves of the wait, which it names and explains from
the inside. Streaming is chapter 19's: server-sent events and a
delta per chunk.

`priced` does not stream, because a streamed response does not carry
the usage block, and the usage block is where the CACHED token count
lives. So the lab pays for both: the same request twice, once for the
clock and once for the bill. That is a cost of measuring and it is
reported rather than hidden - see bill.py.

Every model id is pinned and dated, so a figure here can be told
apart from the same figure on a later version of the same name.
The key is read from the environment and never printed.
"""
import json
import os
import time
import urllib.request

CHEAP = "gpt-4o-mini-2024-07-18"
CAPABLE = "gpt-4o-2024-08-06"
URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 180

#  Dollars per million tokens, read from the provider's price page on
#  2026-10-30 and WRITTEN DOWN HERE rather than fetched, so every
#  figure in this chapter can be recomputed from the token counts
#  when the prices change. Chapter 53 owns the bill; this is the one
#  arithmetic the lab needs to turn tokens into money.
PRICE = {
    CHEAP:   {"in": 0.150, "cached": 0.075, "out": 0.600},
    CAPABLE: {"in": 2.500, "cached": 1.250, "out": 10.000},
}


def _request(payload):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return urllib.request.Request(
        URL, json.dumps(payload).encode(),
        {"Authorization": f"Bearer {key}",
         "Content-Type": "application/json"})


def timed(messages, model=CHEAP, max_tokens=300, temperature=0):
    """Stream one call and time the two halves of the wait.

    time to first token  the wait before anything appears
    time per token       the gap between tokens after that

    The second is computed from the tokens AFTER the first, because
    the first one's gap is the first number and counting it twice
    would flatter the stream.
    """
    payload = {"model": model, "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature,
               "stream": True}
    t0 = time.monotonic()
    first = None
    stamps, parts = [], []
    req = _request(payload)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data: "):
                continue
            body = line[6:]
            if body == "[DONE]":
                break
            d = json.loads(body)
            delta = d["choices"][0]["delta"].get("content")
            if not delta:
                continue
            now = time.monotonic()
            if first is None:
                first = now - t0
            stamps.append(now)
            parts.append(delta)
    total = time.monotonic() - t0
    after = len(stamps) - 1
    per = ((stamps[-1] - stamps[0]) / after) if after > 0 else None
    #  Every gap between chunks, kept so that the time per token can
    #  be computed more than one way. A short reply has few gaps and
    #  a long one has many, so a mean over all of them weights the
    #  stream's first moments differently in the two - which is a
    #  property of the measurement and not of the model, and the
    #  only way to tell the two apart is to recompute without them.
    gaps = [round(b - a, 6) for a, b in zip(stamps, stamps[1:])]
    return {"model": model,
            "text": "".join(parts),
            "chunks": len(stamps),
            "ttft_s": round(first, 4) if first is not None else None,
            "tpt_s": round(per, 5) if per else None,
            "gaps": gaps,
            "total_s": round(total, 4)}


def priced(messages, model=CHEAP, max_tokens=300, temperature=0):
    """One call, not streamed, for the usage block.

    `cached_tokens` is inside prompt_tokens_details and is the one
    number that says whether a prefix was reused. It is reported by
    the provider and not computed here, which is worth saying: this
    lab can measure the EFFECT of reordering a prompt and cannot see
    the cache itself.
    """
    payload = {"model": model, "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature}
    t0 = time.monotonic()
    with urllib.request.urlopen(_request(payload), timeout=TIMEOUT) as r:
        d = json.load(r)
    total = time.monotonic() - t0
    u = d["usage"]
    cached = u.get("prompt_tokens_details", {}).get("cached_tokens", 0)
    return {"model": d["model"],
            "text": d["choices"][0]["message"]["content"] or "",
            "finish_reason": d["choices"][0]["finish_reason"],
            "in_tokens": u["prompt_tokens"],
            "cached_tokens": cached,
            "out_tokens": u["completion_tokens"],
            "total_s": round(total, 4)}


def dollars(model, in_tokens, cached_tokens, out_tokens):
    """What one call cost, with the cached part priced separately.

    Cached input is cheaper and not free, which is the arithmetic
    the chapter turns on: a prefix hit discounts the tokens it
    covers rather than removing them.
    """
    p = PRICE[model]
    fresh = in_tokens - cached_tokens
    return (fresh * p["in"] + cached_tokens * p["cached"]
            + out_tokens * p["out"]) / 1_000_000
```

```python
"""Time to first token and time per token, measured.

Chapter 15 names both and explains them from the inside: prefill
does the input in one pass and decode does the output one token at a
time. That makes a prediction this program can test from the
outside, without opening the model:

  time to first token should move with the INPUT
  time per token should not

Three shapes from work.py make the test possible. `grounded` and
`essay` hold NEARLY the same input and differ in how much output
they ask for; `upfront` holds four times the input at a similar
output. Nearly and similar, because what is held is the instruction
and the cap rather than the realised lengths: `essay` carries 4 per
cent more input than `grounded` and `upfront` produces 23 per cent
fewer output tokens. Both slips are far smaller than the four and
nine times the comparison turns on, and saying so is better than
claiming the arms are identical. So:

  essay against grounded     changes the output, holds the input
  upfront against grounded   changes the input, holds the output

Which is chapter 18's change-one-thing applied to a measurement
rather than to a prompt - and chapter 47's lesson, that two arms
differing in two ways answer neither question.

TRIALS repeats because a network is not a clock. Chapter 20 supplies
the interval and its rule about where repeats go: they are averaged
within a request and never recorded as extra rows.

AND THE SHAPES ARE INTERLEAVED, which the first version of this
program did not do. It ran all of `grounded`, then all of `essay`,
then all of `upfront` - so the shape a call belonged to and the
moment it ran were the same variable. It reported that asking for a
longer answer made the FIRST token arrive sooner, by 0.23 seconds
with an interval clear of zero, which is not a thing a longer answer
can do. What it had measured is that the first shape ran first, on a
cold connection. A confound in a timing measurement does not look
like a confound; it looks like a result with a tight interval.

So every call now carries its own sequence number, and `drift()`
reports whether time to first token trends with it. That turns the
confound from something to be careful about into something the
program checks.
"""
import json
import pathlib
import random
import statistics

import clock
import work

OUT = pathlib.Path("wait.json")
#  The first interleaved run, kept rather than thrown away: it is
#  the only evidence for how much this comparison moves between
#  runs, and a chapter quoting an earlier run from memory is
#  quoting a figure nobody can check.
RUN1 = pathlib.Path("wait-run1.json")
TRIALS = 3
RESAMPLES = 10_000
SEED = 49


def run():
    rows = []
    seq = 0
    for trial in range(1, TRIALS + 1):
        for row in work.requests():
            for shape in work.SHAPES:
                m = work.messages(row, shape)
                r = clock.timed(m, model=clock.CHEAP,
                                max_tokens=work.CAP[shape])
                seq += 1
                rows.append({"shape": shape,
                             "query_id": row["query_id"],
                             "trial": trial, "seq": seq, **r})
                OUT.write_text(json.dumps(rows, indent=1))
                print(f"    {seq:>3} {shape:<9} {row['query_id']}"
                      f" t{trial}: ttft {r['ttft_s']}s"
                      f"  tpt {r['tpt_s']}s  {r['chunks']} chunks")
    return rows


def rows():
    if not OUT.exists():
        return run()
    have = json.loads(OUT.read_text())
    #  A cached file from before the shapes were interleaved has no
    #  `seq`, and its figures are the confounded ones. Checking the
    #  file against what the program now records is chapter 35's
    #  Tip: a run that reads its own cache reports the old data
    #  without a word.
    if ({r["shape"] for r in have} != set(work.SHAPES)
            or any("seq" not in r or "gaps" not in r for r in have)):
        return run()
    return have


def per_request(rs, shape, field):
    """One number per request, trials averaged within it - chapter
    20's rule about where repeats go. The request is the unit the
    interval resamples, because the eight queries are what a
    different workload would have drawn differently."""
    out = {}
    for row in work.requests():
        vals = [r[field] for r in rs
                if r["shape"] == shape and r["query_id"] == row["query_id"]
                and r[field] is not None]
        if vals:
            out[row["query_id"]] = statistics.fmean(vals)
    return out


def interval(pairs, rounds=RESAMPLES, seed=SEED):
    rng = random.Random(seed)
    n = len(pairs)
    means = sorted(
        sum(b - a for a, b in (pairs[rng.randrange(n)]
                               for _ in range(n))) / n
        for _ in range(rounds))
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


def compare(rs, a, b, field):
    pa, pb = per_request(rs, a, field), per_request(rs, b, field)
    keys = [k for k in pa if k in pb]
    pairs = [(pa[k], pb[k]) for k in keys]
    lo, hi = interval(pairs)
    return (statistics.fmean(pb[k] - pa[k] for k in keys), lo, hi,
            len(keys))


def drift(rs):
    """Does time to first token trend with WHEN the call ran?

    The first half of the sequence against the second, on the same
    shapes. If the two halves differ, the order calls ran in is a
    variable and every comparison above has to be read with that in
    mind - which is what the first version of this program found
    out the hard way.
    """
    half = max(r["seq"] for r in rs) / 2
    out = {}
    for shape in work.SHAPES:
        sel = [r for r in rs if r["shape"] == shape]
        early = [r["ttft_s"] for r in sel if r["seq"] <= half]
        late = [r["ttft_s"] for r in sel if r["seq"] > half]
        out[shape] = (statistics.fmean(early) if early else None,
                      statistics.fmean(late) if late else None)
    return out


if __name__ == "__main__":
    rs = rows()
    print(f"  {len(rs)} streamed calls: {len(work.SHAPES)} shapes x"
          f" {len(work.requests())} requests x {TRIALS} trials.")
    print(f"  Model {clock.CHEAP}.\n")

    print("  1. THE TWO HALVES OF THE WAIT.\n")
    print("  shape      in-tok  out-tok   ttft s   tpt ms   total s")
    for shape in work.SHAPES:
        sel = [r for r in rs if r["shape"] == shape]
        tpt = [r["tpt_s"] for r in sel if r["tpt_s"]]
        print(f"  {shape:<11}{'?':>6}"
              f"{statistics.fmean(r['chunks'] for r in sel):>9.0f}"
              f"{statistics.fmean(r['ttft_s'] for r in sel):>9.3f}"
              f"{statistics.fmean(tpt) * 1000:>9.2f}"
              f"{statistics.fmean(r['total_s'] for r in sel):>10.3f}")
    print("\n  The output column is CHUNKS, not tokens: a streamed")
    print("  response carries no usage block, so this program counts")
    print("  what arrived. bill.py has the provider's token counts")
    print("  and the two are not the same number.\n")

    print("  2. DID WHEN A CALL RAN MATTER. The first half of the")
    print("     sequence against the second, within each shape.\n")
    print("     shape       early ttft   late ttft   change")
    for shape, (early, late) in drift(rs).items():
        if early and late:
            print(f"     {shape:<12}{early:>10.3f}{late:>12.3f}"
                  f"{late - early:>+9.3f}")
    print("\n     The shapes are interleaved, so this is a check")
    print("     rather than a correction. It is here because the")
    print("     first version of this program ran the shapes in")
    print("     blocks and reported a 0.23-second effect that was")
    print("     the running order.\n")

    #  Is a chunk a token? The streamed response does not say, so
    #  every "time per token" above is really a time per CHUNK.
    #  order.py's priced calls carry the provider's own output
    #  token count for the same shapes, so the ratio is computed
    #  rather than assumed - and if it were not near one, nothing
    #  above would be a time per token at all.
    try:
        import order
        priced = order.rows()
    except Exception:
        priced = []
    if priced:
        print("  3. IS A CHUNK A TOKEN. The streamed calls count")
        print("     chunks; order.py's priced calls have the")
        print("     provider's own output token count for the same")
        print("     shapes.\n")
        print("     shape      chunks   out-tokens   tokens/chunk")
        ratios = []
        for shape in work.SHAPES:
            ch = statistics.fmean(r["chunks"] for r in rs
                                  if r["shape"] == shape)
            ot = [r["out_tokens"] for r in priced
                  if r["shape"] == shape
                  and r["order"] == "stable-first"]
            if not ot:
                continue
            m = statistics.fmean(ot)
            ratios.append(m / ch)
            print(f"     {shape:<11}{ch:>7.1f}{m:>13.1f}"
                  f"{m / ch:>15.2f}")
        near = all(0.9 <= x <= 1.1 for x in ratios)
        print(f"\n     Every ratio within a tenth of one: {near}.")
        if near:
            print("     So a chunk is a token on this service and")
            print("     the figures above are times per token. It")
            print("     is checked rather than assumed, because if")
            print("     a long reply packed more tokens into each")
            print("     chunk then a smaller gap between chunks")
            print("     would not be a faster token.\n")
        else:
            print("     So the gaps above are times per CHUNK and")
            print("     not per token, and nothing here measures a")
            print("     time per token.\n")

    print("  4. IS THE TIME-PER-TOKEN FINDING AN ARTEFACT OF THE")
    print("     MEASUREMENT. A short reply has few gaps between")
    print("     chunks and a long one has many, so a mean over all")
    print("     of them weights the stream's first moments")
    print("     differently in the two. Recomputing without the")
    print("     early gaps is how you tell.\n")
    print("     drop first   grounded   essay   upfront   diff")
    for drop in (0, 1, 3, 10):
        cells = []
        for shape in work.SHAPES:
            sel = [r for r in rs if r["shape"] == shape]
            vals = [statistics.fmean(r["gaps"][drop:])
                    for r in sel if len(r["gaps"]) > drop + 1]
            cells.append(statistics.fmean(vals) * 1000 if vals
                         else float("nan"))
        print(f"     {drop:>10}{cells[0]:>11.2f}{cells[1]:>8.2f}"
              f"{cells[2]:>10.2f}{cells[1] - cells[0]:>+8.2f}")
    print("\n     Figures are milliseconds. And that test is")
    print("     ASYMMETRIC by construction, which is why the")
    print("     difference growing does not settle it: dropping")
    print("     ten gaps removes a quarter of a 36-gap reply and")
    print("     three per cent of a 341-gap one, so the two")
    print("     columns are not being treated alike.\n")
    #  The test that does follow: compare the SAME gap positions in
    #  both arms. The first version of this program dropped early
    #  gaps from both and read a growing difference as evidence,
    #  when the growth is almost entirely the short arm's mean
    #  moving while the long arm's does not.
    short = min(len(r["gaps"]) for r in rs
                if r["shape"] in ("grounded", "essay"))
    print(f"     Matched positions instead - the first {short} gaps")
    print("     of both arms, which is as many as the shorter one")
    print("     has:\n")
    print("     shape       first-" + str(short) + " mean")
    cells = {}
    for shape in ("grounded", "essay"):
        vals = [statistics.fmean(r["gaps"][:short]) for r in rs
                if r["shape"] == shape and len(r["gaps"]) >= short]
        cells[shape] = statistics.fmean(vals) * 1000
        print(f"     {shape:<12}{cells[shape]:>10.2f}")
    #  Paired by request, which is the unit everywhere else here.
    pa, pb = {}, {}
    for row in work.requests():
        q = row["query_id"]
        for shape, into in (("grounded", pa), ("essay", pb)):
            v = [statistics.fmean(r["gaps"][:short]) for r in rs
                 if r["shape"] == shape and r["query_id"] == q
                 and len(r["gaps"]) >= short]
            if v:
                into[q] = statistics.fmean(v)
    keys = [k for k in pa if k in pb]
    lo, hi = interval([(pa[k], pb[k]) for k in keys])
    d = statistics.fmean(pb[k] - pa[k] for k in keys)
    print(f"\n     essay - grounded  {d * 1000:+.2f} ms"
          f"  {lo * 1000:+.2f} to {hi * 1000:+.2f}")
    print(f"     over {len(keys)} paired requests."
          f" {'Clears zero.' if (lo > 0 or hi < 0) else 'Cannot tell.'}")
    print("     That is the test the chapter rests the finding on.\n")

    print("  5. THE SAME COMPARISON ON AN EARLIER RUN, because")
    print("     one run cannot say how much a number moves between")
    print("     runs, and that is the question here.\n")
    if RUN1.exists():
        earlier = json.loads(RUN1.read_text())
        print("     run     g->upfront ttft   95% interval")
        for label, data in (("first", earlier), ("this", rs)):
            pa = per_request(data, "grounded", "ttft_s")
            pb = per_request(data, "upfront", "ttft_s")
            keys = [k for k in pa if k in pb]
            pairs = [(pa[k], pb[k]) for k in keys]
            lo, hi = interval(pairs)
            d = statistics.fmean(pb[k] - pa[k] for k in keys)
            print(f"     {label:<8}{d:>13.2f}   {lo:+.2f} to {hi:+.2f}")
        print("\n     Neither clears zero, and the point estimates")
        print("     are 0.17 apart on eight paired requests each.")
        print("     Both files are in the lab.\n")
    else:
        print("     wait-run1.json is not here, so this chapter has")
        print("     one run and cannot say how much it moves.\n")

    print("  6. CHAPTER 15'S PREDICTION, ONE CHANGE AT A TIME.")
    print("     Paired by request, trials averaged within it.\n")
    print("     change             moves    diff   95% interval")
    TESTS = [("grounded", "essay", "the OUTPUT, input held"),
             ("grounded", "upfront", "the INPUT, output held")]
    for a, b, what in TESTS:
        for field, unit, scale in (("ttft_s", "ttft s", 1),
                                   ("tpt_s", "tpt ms", 1000)):
            d, lo, hi, n = compare(rs, a, b, field)
            says = ("up" if lo > 0 else "down" if hi < 0
                    else "cannot tell")
            print(f"     {a[:5]}->{b[:7]:<9}{unit:>7}"
                  f"{d * scale:>+8.2f}"
                  f"  {lo * scale:+.2f} to {hi * scale:+.2f}"
                  f"  {says[:6]}")
        print(f"       changes {what}")
    print()
```

```text
  72 streamed calls: 3 shapes x 8 requests x 3 trials.
  Model gpt-4o-mini-2024-07-18.

  1. THE TWO HALVES OF THE WAIT.

  shape      in-tok  out-tok   ttft s   tpt ms   total s
  grounded        ?       37    0.836    10.65     1.226
  essay           ?      342    0.829     7.89     3.538
  upfront         ?       29    0.995    11.24     1.313

  The output column is CHUNKS, not tokens: a streamed
  response carries no usage block, so this program counts
  what arrived. bill.py has the provider's token counts
  and the two are not the same number.

  2. DID WHEN A CALL RAN MATTER. The first half of the
     sequence against the second, within each shape.

     shape       early ttft   late ttft   change
     grounded         0.883       0.789   -0.094
     essay            0.909       0.749   -0.160
     upfront          0.861       1.130   +0.269

     The shapes are interleaved, so this is a check
     rather than a correction. It is here because the
     first version of this program ran the shapes in
     blocks and reported a 0.23-second effect that was
     the running order.

  3. IS A CHUNK A TOKEN. The streamed calls count
     chunks; order.py's priced calls have the
     provider's own output token count for the same
     shapes.

     shape      chunks   out-tokens   tokens/chunk
     grounded      36.6         38.0           1.04
     essay        342.4        342.1           1.00
     upfront       29.3         29.3           1.00

     Every ratio within a tenth of one: True.
     So a chunk is a token on this service and
     the figures above are times per token. It
     is checked rather than assumed, because if
     a long reply packed more tokens into each
     chunk then a smaller gap between chunks
     would not be a faster token.

  4. IS THE TIME-PER-TOKEN FINDING AN ARTEFACT OF THE
     MEASUREMENT. A short reply has few gaps between
     chunks and a long one has many, so a mean over all
     of them weights the stream's first moments
     differently in the two. Recomputing without the
     early gaps is how you tell.

     drop first   grounded   essay   upfront   diff
              0      10.65    7.89     11.24   -2.77
              1      10.99    7.91     11.69   -3.08
              3      11.34    7.93     12.08   -3.41
             10      11.72    7.89     13.90   -3.83

     Figures are milliseconds. And that test is
     ASYMMETRIC by construction, which is why the
     difference growing does not settle it: dropping
     ten gaps removes a quarter of a 36-gap reply and
     three per cent of a 341-gap one, so the two
     columns are not being treated alike.

     Matched positions instead - the first 21 gaps
     of both arms, which is as many as the shorter one
     has:

     shape       first-21 mean
     grounded         11.34
     essay             9.56

     essay - grounded  -1.79 ms  -3.64 to -0.03
     over 8 paired requests. Clears zero.
     That is the test the chapter rests the finding on.

  5. THE SAME COMPARISON ON AN EARLIER RUN, because
     one run cannot say how much a number moves between
     runs, and that is the question here.

     run     g->upfront ttft   95% interval
     first           -0.01   -0.08 to +0.07
     this             0.16   -0.04 to +0.34

     Neither clears zero, and the point estimates
     are 0.17 apart on eight paired requests each.
     Both files are in the lab.

  6. CHAPTER 15'S PREDICTION, ONE CHANGE AT A TIME.
     Paired by request, trials averaged within it.

     change             moves    diff   95% interval
     groun->essay     ttft s   -0.01  -0.07 to +0.07  cannot
     groun->essay     tpt ms   -2.77  -3.91 to -1.68  down
       changes the OUTPUT, input held
     groun->upfront   ttft s   +0.16  -0.04 to +0.34  cannot
     groun->upfront   tpt ms   +0.59  -1.33 to +2.62  cannot
       changes the INPUT, output held
```

**Neither prediction survives, and they fail in different ways.** Quadrupling the input — 612
tokens to 2,458, by the provider's own count — changes time to first token by +0.16 seconds with
95 per cent from −0.04 to +0.34, which does not clear zero. *Eight paired requests*, trials
averaged within each, which is Chapter 20's rule about where repeats go.

**And that +0.16 is one trial of three.** Taken a trial at a time the same difference reads −0.07,
+0.47 and +0.09: the whole of it is the second trial's `upfront` calls. The first interleaved run
of this program is kept in the lab beside the second, and on the same comparison it gives −0.01
from −0.08 to +0.07 — two runs of eight paired requests, point estimates 0.17 apart, neither
clearing zero, and section 5 computes both from their own files rather than quoting one from
memory. **A number whose point estimate ranges over half a second inside one run is not measuring
a property of the prompt.** *Send more, wait longer* is not measurable here, and the honest form of
that is **I could not detect it**, not *it is not there*.

**And time per token, which was supposed to stay still, moves — in the direction Chapter 15 says
it should not.** Asking for nine times the output makes each token arrive 2.77 milliseconds
*sooner*, 7.9 against 10.7, with 95 per cent from −3.91 to −1.68. Chapter 15 says each token takes
roughly the same time as the one before and names the drift it expects, which is *upward* as the
cache grows. This is the other way.

**Chapter 15 contains the explanation and does not quite say it.** Its own arithmetic is why: at a
thousand tokens the squared attention term is one part in twenty of prefill, so a prompt four times
longer is a few milliseconds of extra computation on a machine built for this. And its batching
section says the rest — *if the system is busy, your request waits to join a batch.* So the 0.84
seconds is overwhelmingly queueing, scheduling and the network, and the computation Chapter 15
describes is a rounding error inside it. **At the prompt lengths this system sends, the mechanism
that dominates your measured time to first token is not the one the prefill arithmetic
describes.** Where that stops being
true is Chapter 15's arithmetic rather than this lab's measurement: its own table puts the
crossover, where attention's squared term matches the rest of prefill, at 19,200 tokens. This lab
failed to detect an effect at 2,458 tokens with eight paired requests on one service on one day,
which locates no boundary at all.

That is not a correction to Chapter 15. It is the difference between knowing why a thing is slow
and knowing what *your* slow thing is, which is the whole reason this chapter exists.

> **Warning:** The first version of this program got a result and the result was the running order.
> It ran all eight `grounded` requests, then all eight `essay`, then all eight `upfront` — so the
> shape a call belonged to and the moment it ran were the same variable. It reported that asking
> for a longer answer made the *first* token arrive 0.23 seconds sooner, with an interval from
> −0.46 to −0.03 that cleared zero. A longer answer cannot do that; a cold connection can.
> **A confound in a timing measurement does not look like a confound. It looks like a result with
> a tight interval**, because the thing that drifts — load, routing, a warming connection — drifts
> smoothly, and a smooth drift aligned with your arms is indistinguishable from an effect.
>
> **Interleaving did not remove the drift and does not claim to.** Section 2 of the output reports
> the first half of the sequence against the second: `grounded` and `essay` are about a tenth of a
> second faster late, and `upfront` is slower late. So the drift is *not* spread evenly over the
> arms — it sits on one of them, which is exactly how it ends up in the difference rather than in
> the width, and it is the whole of the +0.16 above. **Interleaving buys the ability to see the
> drift. It does not buy a measurement free of it**, and nothing short of more runs does. The
> trial-by-trial spread is the thing to read here, not the pooled interval.

**Before believing that, two things had to be ruled out, and the program does both.**

**Is a chunk a token?** A streamed response carries no usage block, so every figure above is really
a time per *chunk*, and a long reply packing more tokens into each chunk would produce a smaller
gap without a faster token. The priced calls have the provider's own output token count for the
same shapes: the ratio is 1.04, 1.00 and 1.00. A chunk is a token here, so these are times per
token — checked rather than assumed.

**Is it the stream settling?** A 37-chunk reply has 36 gaps to average and a 342-chunk reply has
341, so the first moments of the stream weigh nine times as heavily in the short one. Dropping the
first gap, then the first three, then the first ten makes the difference *grow* — −2.77, −3.08,
−3.41, −3.83 — and that is *not* the test it looks like. Dropping ten gaps removes a quarter of
the short reply's gaps and three per cent of the long one's, so the two columns are not being
treated alike, and almost all of the growth is the short arm's mean moving while the long arm's
does not budge. An asymmetric test cannot settle a question about asymmetry.

**The test that does follow is matched positions**: the first twenty-one gaps of both arms, which
is as many as the shorter one has. There the difference is **−1.79 milliseconds with 95 per cent
from −3.64 to −0.03**, over eight paired requests. It clears zero, and only just — against −2.77
from the unmatched comparison. So the finding survives the right test at about two thirds of the
size the wrong test gave it, and that smaller figure is the one to carry.

**What is left is a small real difference whose mechanism this lab cannot see.** The honest candidate is
the serving arrangement rather than the model: a request that will produce three hundred tokens
and one that will produce thirty are scheduled differently, and Chapter 15's batching section is
the half of this that is about the machine being shared — *if the system is busy, your request
waits to join a batch.* Under an arrangement that adds and removes requests continuously, that
waiting is per token rather than once. Chapter 15 describes that arrangement without naming it and
gives it to Chapter 52. **This chapter measures it from the outside and stops there**, because the
next step would be a claim about a machine I cannot look inside.

> **Note:** `clock.py` has two functions because of the usage block, and that means this lab pays
> for every request twice — once streamed for the clock and once priced for the bill. That is a
> cost of measuring and step 5 reports it rather than hiding it.

## Step 3: Move One Sentence, and Read the Bill

The lever: put the part that does not change between requests at the front of the prompt, and the
part that does at the back. A **prompt-prefix cache** is a provider reusing the leading tokens of a
request that match a request it has already served — the *leading* tokens, which is the whole of
why order matters, because a question at the top means every request begins differently and there
is nothing to reuse.

Two orders, holding the same text. The instruction, the passages and the question are the same
characters in both, which `work.py` asserts — so a difference here is about *where the part that
changes sits* and not about length.

```python
"""The same prompt in two orders, and what the cache pays for it.

The lever: put the part that does not change between requests at the
FRONT, and the part that does at the back. A provider's prompt cache
matches a prefix, so a question at the top of the prompt means every
request has a different first token and nothing to reuse.

What this program can and cannot see. It cannot see the cache. What
it reads is `cached_tokens` in the usage block, which the provider
reports, and the time the call took. So it measures the EFFECT of an
ordering on a bill and a clock, and infers nothing about how the
cache works.

Not streamed, and that is the trade: a streamed response carries no
usage block, so the cached count and the time to first token cannot
be had from one call. These are the priced calls; wait.py has the
streamed ones.

ORDER MATTERS WITHIN A RUN, so the two orders are run INTERLEAVED,
request by request, rather than one order and then the other. A
cache is warm or cold depending on what ran a moment ago, and
running all of one arm first would hand the second arm whatever the
first left behind.

AND THE TRIALS HAVE TO BE READ APART, which is the thing this
program found out. Repeating eight requests three times means that
on trials 2 and 3 a question-first request can reuse ITS OWN earlier
self, because the same question was asked an hour ago with the same
text after it. Pooled over three trials that reads as 66 per cent
cached for an arrangement that should cache nothing, and the pooled
figure is an artefact of asking the same question three times.
Normal traffic does not do that; a verbatim repeat is chapter 52's
application-level response cache and this lab's declared non-scope.

So trial 1 is the measurement - every request new - and trials 2 and
3 say what a verbatim repeat is worth. Both are printed.
"""
import json
import pathlib
import random
import statistics

import clock
import work

OUT = pathlib.Path("order.json")
TRIALS = 3
RESAMPLES = 10_000
SEED = 49
ORDERS = ("stable-first", "question-first")


def run():
    rows = []
    for shape in work.SHAPES:
        for trial in range(1, TRIALS + 1):
            for row in work.requests():
                for order in ORDERS:
                    m = work.messages(row, shape, order)
                    r = clock.priced(m, model=clock.CHEAP,
                                     max_tokens=work.CAP[shape])
                    cost = clock.dollars(r["model"], r["in_tokens"],
                                         r["cached_tokens"],
                                         r["out_tokens"])
                    rows.append({"shape": shape, "order": order,
                                 "query_id": row["query_id"],
                                 "trial": trial, "dollars": cost,
                                 **{k: v for k, v in r.items()
                                    if k != "text"}})
                    OUT.write_text(json.dumps(rows, indent=1))
            print(f"    {shape} trial {trial} done "
                  f"({len(rows)} calls)")
    return rows


def rows():
    if not OUT.exists():
        return run()
    have = json.loads(OUT.read_text())
    if {r["shape"] for r in have} != set(work.SHAPES):
        return run()
    return have


def per_request(rs, shape, order, field):
    out = {}
    for row in work.requests():
        vals = [r[field] for r in rs if r["shape"] == shape
                and r["order"] == order
                and r["query_id"] == row["query_id"]]
        if vals:
            out[row["query_id"]] = statistics.fmean(vals)
    return out


def interval(pairs, rounds=RESAMPLES, seed=SEED):
    rng = random.Random(seed)
    n = len(pairs)
    means = sorted(
        sum(b - a for a, b in (pairs[rng.randrange(n)]
                               for _ in range(n))) / n
        for _ in range(rounds))
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


if __name__ == "__main__":
    rs = rows()
    print(f"  {len(rs)} priced calls: {len(work.SHAPES)} shapes x"
          f" {len(ORDERS)} orders x")
    print(f"  {len(work.requests())} requests x {TRIALS} trials,"
          f" interleaved.\n")

    print("  1. WHAT THE PROVIDER SAYS IT REUSED, BY TRIAL.")
    print("     Trial 1 is the measurement: every request new.")
    print("     Trials 2 and 3 repeat the same eight questions.\n")
    print("  shape     order            in-tok   t1     t2     t3")
    for shape in work.SHAPES:
        for order in ORDERS:
            sel = [r for r in rs if r["shape"] == shape
                   and r["order"] == order]
            it = statistics.fmean(r["in_tokens"] for r in sel)
            cells = []
            for trial in (1, 2, 3):
                c = [r["cached_tokens"] for r in sel
                     if r["trial"] == trial]
                cells.append(statistics.fmean(c) / it if c else 0)
            print(f"  {shape:<10}{order:<16}{it:>7.0f}"
                  + "".join(f"{x:>7.0%}" for x in cells))
    print()
    #  The two readings of the one shape the lever reaches, computed
    #  rather than asserted, because the whole point is that they
    #  are different numbers.
    up = [r for r in rs if r["shape"] == "upfront"]
    cold = {o: [r["cached_tokens"] for r in up
                if r["order"] == o and r["trial"] == 1]
            for o in ORDERS}
    print("     On trial 1, with every request new:")
    for o in ORDERS:
        z = sum(1 for x in cold[o] if x == 0)
        print(f"       {o:<16}{statistics.fmean(cold[o]):>7.0f}"
              f" cached, zero on {z} of {len(cold[o])}")
    print("\n     That is the lever, and it is total rather than")
    print("     partial. With the stable part first, request q2")
    print("     reuses what q1 left - DIFFERENT requests share a")
    print("     prefix, which is the whole point. With the question")
    print("     first, a request can only reuse its own earlier")
    print("     self, and on its first outing there is no earlier")
    print("     self. The 66 per cent that arm shows pooled over")
    print("     three trials is three identical questions and not")
    print("     a property of the ordering.\n")
    under = [s for s in work.SHAPES
             if max(r["cached_tokens"] for r in rs
                    if r["shape"] == s) == 0]
    if under:
        print(f"  {len(under)} of {len(work.SHAPES)} shapes never got"
              f" a single cached token in")
        print(f"  EITHER order: {', '.join(under)}. Their prompts are")
        print("  under the provider's minimum, so the lever does not")
        print("  apply to them at all - which is the first thing to")
        print("  find out about a lever and is not what a chapter")
        print("  about levers usually tells you.\n")

    print("  2. WHAT IT COST, ON FIRST-OUTING TRAFFIC AND")
    print("     POOLED OVER REPEATS.\n")
    print("  shape     order            t1 $/1k   all $/1k   secs")
    for shape in work.SHAPES:
        for order in ORDERS:
            sel = [r for r in rs if r["shape"] == shape
                   and r["order"] == order]
            one = [r["dollars"] for r in sel if r["trial"] == 1]
            d1 = statistics.fmean(one) * 1000
            d = statistics.fmean(r["dollars"] for r in sel) * 1000
            s = statistics.fmean(r["total_s"] for r in sel)
            print(f"  {shape:<10}{order:<16}{d1:>8.2f}{d:>11.2f}"
                  f"{s:>7.2f}")
    print("\n     The first column is the one to price the lever")
    print("     off. The second pools three askings of the same")
    print("     eight questions, which is the contamination")
    print("     section 1 identifies - and pricing off it")
    print("     understates the lever, because the arm it")
    print("     flatters is the arm without it.\n")

    print("\n  3. IS THE DIFFERENCE REAL. One REQUEST to a row,")
    print("     trials averaged within it, paired because every")
    print("     request is asked both ways.\n")
    #  Trial 1 only, for the same reason section 2 gives: a
    #  repeated question warms the arm that should have nothing to
    #  reuse, so pooling the trials prices the lever against a
    #  version of itself.
    rs = [r for r in rs if r["trial"] == 1]
    print("     Trial 1 only - every request new.\n")
    for field, label, scale, dp in (
            ("cached_tokens", "cached tokens", 1, 0),
            ("dollars", "cost per 1,000", 1000, 3),
            ("total_s", "seconds", 1, 2)):
        print(f"     {label}")
        print("       shape      diff   95% interval        says")
        for shape in work.SHAPES:
            a = per_request(rs, shape, "question-first", field)
            b = per_request(rs, shape, "stable-first", field)
            keys = [k for k in a if k in b]
            pairs = [(a[k], b[k]) for k in keys]
            lo, hi = interval(pairs)
            d = statistics.fmean(b[k] - a[k] for k in keys)
            better_lower = field in ("dollars", "total_s")
            if lo > 0:
                says = "question" if better_lower else "stable"
            elif hi < 0:
                says = "stable" if better_lower else "question"
            else:
                says = "cannot"
            flat = " flat" if hi == lo else ""
            print(f"       {shape:<9}{d * scale:>+9.{dp}f}"
                  f"{lo * scale:>+9.{dp}f} to"
                  f" {hi * scale:+.{dp}f} {says[:6]}{flat}")
        print()
    print("     A zero-width interval is not precision. Where")
    print("     every request gives the same number there is")
    print("     nothing for a resample to vary, so it reports no")
    print("     spread - which is the absence of evidence about")
    print("     spread and not certainty about the value.")
    print("\n     The sign convention: the difference is")
    print("     stable-first MINUS question-first, so a negative")
    print("     cost or time is the lever helping and a positive")
    print("     cached-token count is.")
```

```text
  144 priced calls: 3 shapes x 2 orders x
  8 requests x 3 trials, interleaved.

  1. WHAT THE PROVIDER SAYS IT REUSED, BY TRIAL.
     Trial 1 is the measurement: every request new.
     Trials 2 and 3 repeat the same eight questions.

  shape     order            in-tok   t1     t2     t3
  grounded  stable-first        612     0%     0%     0%
  grounded  question-first      612     0%     0%     0%
  essay     stable-first        637     0%     0%     0%
  essay     question-first      637     0%     0%     0%
  upfront   stable-first       2458    99%    99%    99%
  upfront   question-first     2458     0%    99%    99%

     On trial 1, with every request new:
       stable-first       2432 cached, zero on 0 of 8
       question-first        0 cached, zero on 8 of 8

     That is the lever, and it is total rather than
     partial. With the stable part first, request q2
     reuses what q1 left - DIFFERENT requests share a
     prefix, which is the whole point. With the question
     first, a request can only reuse its own earlier
     self, and on its first outing there is no earlier
     self. The 66 per cent that arm shows pooled over
     three trials is three identical questions and not
     a property of the ordering.

  2 of 3 shapes never got a single cached token in
  EITHER order: grounded, essay. Their prompts are
  under the provider's minimum, so the lever does not
  apply to them at all - which is the first thing to
  find out about a lever and is not what a chapter
  about levers usually tells you.

  2. WHAT IT COST, ON FIRST-OUTING TRAFFIC AND
     POOLED OVER REPEATS.

  shape     order            t1 $/1k   all $/1k   secs
  grounded  stable-first        0.11       0.11   1.74
  grounded  question-first      0.12       0.12   1.27
  essay     stable-first        0.30       0.30   4.17
  essay     question-first      0.31       0.30   4.02
  upfront   stable-first        0.20       0.20   1.28
  upfront   question-first      0.39       0.27   1.34

     The first column is the one to price the lever
     off. The second pools three askings of the same
     eight questions, which is the contamination
     section 1 identifies - and pricing off it
     understates the lever, because the arm it
     flatters is the arm without it.


  3. IS THE DIFFERENCE REAL. One REQUEST to a row,
     trials averaged within it, paired because every
     request is asked both ways.

     Trial 1 only - every request new.

     cached tokens
       shape      diff   95% interval        says
       grounded        +0       +0 to +0 cannot flat
       essay           +0       +0 to +0 cannot flat
       upfront      +2432    +2432 to +2432 stable flat

     cost per 1,000
       shape      diff   95% interval        says
       grounded    -0.001   -0.002 to +0.001 cannot
       essay       -0.002   -0.012 to +0.009 cannot
       upfront     -0.187   -0.193 to -0.182 stable

     seconds
       shape      diff   95% interval        says
       grounded     -0.15    -0.29 to -0.03 stable
       essay        -0.33    -1.22 to +0.55 cannot
       upfront      -0.06    -0.30 to +0.20 cannot

     A zero-width interval is not precision. Where
     every request gives the same number there is
     nothing for a resample to vary, so it reports no
     spread - which is the absence of evidence about
     spread and not certainty about the value.

     The sign convention: the difference is
     stable-first MINUS question-first, so a negative
     cost or time is the lever helping and a positive
     cached-token count is.
```

**On the shape the lever reaches, it is total rather than partial.** With the stable part first,
2,432 of 2,458 input tokens come back marked cached — on the very first trial, on every one of the
eight requests. With the question first, zero, on all eight. Not a smaller saving: none.

**And the reason is the thing worth carrying, because it is not what "cache your prompt" sounds
like.** With the stable part first, request `q2` reuses what `q1` left behind: **different
requests share a prefix.** With the question first, a request can only ever reuse its own earlier
self. So the lever is not really about repetition at all — it is about making unrelated requests
begin with the same bytes.

**The pooled figure hides that, and it hid it from me.** Over three trials the question-first arm
reads 66 per cent cached, which looks like a lever working at two thirds strength. It is three
identical questions: trial 1 caches nothing and trials 2 and 3 reuse trial 1. A verbatim repeat is
Chapter 52's application-level response cache and this chapter's declared non-scope, and normal
traffic does not ask the same question three times an hour. Reading the trials apart is what turns
66 per cent into the two numbers that mean something, 0 and 99.

**What it is worth in money is $0.19 per thousand requests**, 95 per cent from −0.193 to −0.182:
$0.20 against $0.39 on first-outing traffic. About half off the input bill of that shape.

**And the first draft of this paragraph said $0.07, because it priced the lever off the arm it had
just finished condemning.** The pooled question-first figure is $0.27, not $0.39, precisely because
two of its three trials were reusing their own earlier selves — so pricing against it compares the
lever with a contaminated version of itself and understates it by a factor of nearly three. Having
identified the contamination two paragraphs earlier and then priced off it anyway is the kind of
mistake that survives a reading: the argument is right and the number comes from somewhere else.

**And what it is worth in time is nothing measurable on this shape**, −0.06 seconds with 95 per
cent from −0.30 to +0.20. Which follows from step 2: if the wait is a queue rather than a
computation, removing computation does not shorten it. The `grounded` shape's time row does clear
zero at −0.15 seconds, and that one is noise of the kind step 2 is about — it has no cached tokens
in either order, so there is no mechanism by which ordering could have moved it.

**Then the part that makes this a lab and not a demonstration.** Two of the three shapes got no
cached tokens in either order, because their prompts are about 612 and 637 tokens and the
provider's minimum is 1,024. **The lever does not apply to the traffic this book has spent nine
chapters building.** And the shape it does apply to is the up-front design, which costs **3.4
times the baseline before the lever and 1.8 times after it** — Chapter 35 measured why and chose
against it. So the lever that makes a prompt cheaper to send again only reaches the design that was
more expensive to send at all: $0.11 per thousand for the baseline, $0.39 for the up-front shape
unordered, $0.20 ordered. The lever is worth $0.19, and the design still costs $0.09 per thousand
more than the one you started with.

> **Warning:** The document order inside the up-front block is a tuple in the program and that is
> load-bearing rather than tidy. A prefix is reused only if it is byte-identical, so the same eight
> documents iterated in a different order are the same text and a different prefix, and the cache
> misses without a word of your prompt changing. A `set` where a `tuple` belongs is the cheapest
> way to lose this lever.

> **Note:** A zero-width interval appears twice in that output and it is not precision. Where every
> request returns the same number there is nothing for a resample to vary, so it reports no spread
> — which is the absence of evidence about spread rather than certainty about the value. Chapter 46
> met the same thing on a rate with no discriminating cases.

## Step 4: Send the Easy Ones to the Cheap Model

The third lever: a **cascade** — run the cheap model, and escalate to the expensive one when your
code judges the cheap answer unusable. It costs *both* calls on every escalation, which is the
property that decides whether it is worth building. Three arms, because two cannot separate the
two questions: cheap against capable is what the money buys, and the cascade against capable is
what the *routing* buys.

**The escalation rule is code and not a judge.** Chapter 23's point is that your code is the only
participant that can refuse, and Chapter 31's judge is this chapter's declared non-scope. So the
rule is three checks a program can make without knowing the right answer: the reply says it cannot
answer, the reply names no figure where the question asked for one, or the reply is shorter than a
sentence. A rule that could consult the answer key would be a router that already knows which
cases are hard, which is the one thing a router never knows.

```python
"""A cheap model on the easy cases, and what the routing is worth.

Three arms, because two cannot separate the two questions:

  cheap     every request to the cheap model
  capable   every request to the capable model
  cascade   the cheap model first; escalate to the capable one when
            YOUR CODE says the cheap answer is not usable

cheap against capable is what the money buys. cascade against
capable is what the routing buys, which is the question actually
being asked - and chapter 47's lesson is that an arm differing in
two ways answers neither.

THE ESCALATION RULE IS CODE AND NOT A JUDGE. Chapter 23's point is
that your code is the only participant that can refuse, and chapter
31's judge is this lab's declared non-scope. So the rule is three
checks a program can make without knowing the right answer:

  the reply holds a phrase from a list meant to catch a
    decline - "cannot", "does not", "not specify" and so on
  the reply names no figure where the question asks for one
  the reply is shorter than a sentence

A rule that could consult the answer key would be a router that
already knows which cases are hard, which is the one thing a router
never knows.
"""
import json
import pathlib
import random
import re
import statistics

import clock
import work

OUT = pathlib.Path("route.json")
TRIALS = 3
RESAMPLES = 10_000
SEED = 49
ARMS = ("cheap", "capable", "cascade")

#  question, phrases a right answer carries (any one counts), and
#  whether the question asks for a figure. The phrase sets are
#  chapter 41's exact-match grader with normalisation, and they were
#  written from the documents before any answer existed.
CASES = [
    ("r01", "How many days do I have to return a clearance item?",
     {"14 day", "fourteen day"}, True),
    ("r02", "Who pays return postage on a clearance item?",
     {"customer pays", "paid by the customer", "you pay",
      "at your own cost", "your own expense",
      "the customer is responsible"}, False),
    ("r03", "What surcharge applies to a delivery to an IV postcode?",
     {"9.50"}, True),
    ("r04", "How long after my return arrives is a refund issued?",
     {"14 day", "fourteen day"}, True),
    ("r05", "What is the cap on a goodwill payment?",
     {"20 pound", "20 GBP", "twenty pound", "£20"}, True),
    ("r06", "My card is closed. How long does a bank transfer take?",
     {"10 working day", "ten working day"}, True),
    ("r07", "Can I return a personalised item?",
     {"cannot be returned", "can't be returned", "not be returned",
      "cannot return", "are excluded", "is excluded",
      "not returnable"}, False),
    ("r08", "Is the delivery charge refunded if I send back one "
            "item of three?",
     {"not refunded", "is not refunded", "will not be refunded",
      "not be refunded", "does not refund"}, False),
    #  The next four need two documents, which is the mode chapter
    #  47 built its tasks around. They are the ones a cheap model
    #  should find hardest, and whether it does is a measurement.
    ("r09", "What does standard delivery cost on a 20 pound order "
            "going to an IV postcode?",
     {"13.49", "3.99 and 9.50", "3.99 plus 9.50",
      "3.99 + 9.50"}, True),
    #  This key was WRONG and both models were right. It demanded
    #  "bank transfer", which refund-to-a-closed-card makes the
    #  OPT-IN alternative: account credit is the documented default
    #  ("we issue account credit instead, which is immediate, does
    #  not expire"). Both models gave the default, and the chapter
    #  called this "a question neither model can do" on the
    #  strength of a key asking for the wrong half of the document.
    #  Chapter 41's condition is met - the repair is justified by
    #  the source, and it helps both arms equally.
    ("r10", "I am returning a clearance kettle and my card is "
            "closed. Who pays the postage and how do I get the "
            "money?",
     {"account credit", "bank transfer", "transfer"}, False),
    ("r11", "A clearance item was delivered 20 days ago. Can I "
            "return it, and what is the standard window?",
     {"no", "cannot", "too late", "expired", "outside"}, False),
    ("r12", "How long could a refund take in total, from posting "
            "the parcel to the money showing?",
     {"17 day", "seventeen day", "two and a half week",
      "14 day", "fourteen day"}, True),
]

#  Phrases meant to catch a reply that declines to answer. What
#  they ALSO catch is a reply that answers in the negative - "No,
#  personalised goods cannot be returned" - because "cannot" and
#  "does not" are how a correct refusal is worded. Every escalation
#  in this lab is that collision and not a decline, which the
#  reason string now reports rather than the chapter guessing.
CANNOT = ("do not", "does not", "cannot", "not specify", "not state",
          "no information", "not provided", "not mention",
          "unable to", "not contain", "not available in the")
FIGURE = re.compile(r"\d")


def hinges(cid):
    return next(c for c in CASES if c[0] == cid)


def norm(s):
    return re.sub(r"\s+", " ", str(s)).lower()


def passes(answer, want):
    body = norm(answer)
    return any(norm(p) in body for p in want)


def escalate(answer, wants_figure):
    """Your code deciding the cheap answer is not usable.

    Returns the reason, or None to keep it. Three checks, and the
    first is the one that fires: a reply that says it cannot answer
    is the cheapest possible signal and needs no key.
    """
    body = norm(answer)
    #  Tested in the order the docstring lists them, because the
    #  rules are not mutually exclusive and whichever runs first
    #  decides the reason you are told. The first version tested
    #  shortness first while its own docstring said otherwise.
    hit = next((p for p in CANNOT if p in body), None)
    if hit:
        return f"matched {hit!r}"
    if wants_figure and not FIGURE.search(body):
        return "no figure where the question asks for one"
    if len(body.split()) < 5:
        return "shorter than a sentence"
    return None


def ask(case, model, cache):
    cid, q, want, figure = case
    row = {"query_id": cid, "question": q,
           "passages": work.passages(q, cache), "body": ""}
    row["body"] = "\n".join(
        f"[{c}] {__import__('search').BY_ID[c]['text']}"
        for c in row["passages"])
    m = work.messages(row, "grounded")
    r = clock.priced(m, model=model, max_tokens=work.CAP["grounded"])
    return r


def run():
    import search
    cache = search.vectors()
    rows = []
    for trial in range(1, TRIALS + 1):
        for case in CASES:
            cid, q, want, figure = case
            cheap = ask(case, clock.CHEAP, cache)
            why = escalate(cheap["text"], figure)
            rec = {"case": cid, "trial": trial,
                   "cheap_passed": passes(cheap["text"], want),
                   "cheap_dollars": clock.dollars(
                       cheap["model"], cheap["in_tokens"],
                       cheap["cached_tokens"], cheap["out_tokens"]),
                   "cheap_s": cheap["total_s"],
                   "cheap_answer": cheap["text"],
                   "escalated": why}
            cap = ask(case, clock.CAPABLE, cache)
            rec.update({
                "capable_passed": passes(cap["text"], want),
                "capable_dollars": clock.dollars(
                    cap["model"], cap["in_tokens"],
                    cap["cached_tokens"], cap["out_tokens"]),
                "capable_s": cap["total_s"],
                "capable_answer": cap["text"]})
            #  The cascade spends the cheap call ALWAYS and the
            #  capable one only on escalation, so its cost is the
            #  sum where it escalated. That is what a cascade costs
            #  and it is why a cascade can cost more than either.
            if why:
                rec["cascade_passed"] = rec["capable_passed"]
                rec["cascade_dollars"] = (rec["cheap_dollars"]
                                          + rec["capable_dollars"])
                rec["cascade_s"] = rec["cheap_s"] + rec["capable_s"]
            else:
                rec["cascade_passed"] = rec["cheap_passed"]
                rec["cascade_dollars"] = rec["cheap_dollars"]
                rec["cascade_s"] = rec["cheap_s"]
            rows.append(rec)
            OUT.write_text(json.dumps(rows, indent=1))
            print(f"    {cid} t{trial}: cheap "
                  f"{'ok  ' if rec['cheap_passed'] else 'FAIL'}"
                  f" capable "
                  f"{'ok  ' if rec['capable_passed'] else 'FAIL'}"
                  f" {'ESCALATED' if why else 'kept'}")
    return rows


def rows():
    """The stored runs, RE-GRADED with the current grader.

    Chapter 45's habit, and the reason it is worth keeping: the key
    for r10 was repaired after these runs, and trusting the verdict
    written when the run happened would report the broken one. Every
    escalation decision is recomputed too, because the reason string
    changed with it. Nothing is re-called; only the grading moves.
    """
    if not OUT.exists():
        return run()
    have = json.loads(OUT.read_text())
    moved = []
    for r in have:
        _, _, want, figure = hinges(r["case"])
        for arm in ("cheap", "capable"):
            now = passes(r[f"{arm}_answer"], want)
            if now != r[f"{arm}_passed"]:
                moved.append((r["case"], r["trial"], arm,
                              r[f"{arm}_passed"], now))
            r[f"{arm}_passed"] = now
        r["escalated"] = escalate(r["cheap_answer"], figure)
        if r["escalated"]:
            r["cascade_passed"] = r["capable_passed"]
        else:
            r["cascade_passed"] = r["cheap_passed"]
    if moved:
        print(f"  Re-graded with the current keys:"
              f" {len(moved)} of {2 * len(have)} verdicts move.")
        import collections
        for (case, arm), k in sorted(collections.Counter(
                (m[0], m[2]) for m in moved).items()):
            print(f"    {case} {arm}: {k} trial(s)"
                  f" FAIL -> pass")
        print()
    return have


def per_case(rs, field):
    out = {}
    for cid, *_ in CASES:
        vals = [r[field] for r in rs if r["case"] == cid]
        if vals:
            out[cid] = statistics.fmean(float(v) for v in vals)
    return out


def interval(pairs, rounds=RESAMPLES, seed=SEED):
    rng = random.Random(seed)
    n = len(pairs)
    means = sorted(
        sum(b - a for a, b in (pairs[rng.randrange(n)]
                               for _ in range(n))) / n
        for _ in range(rounds))
    return means[int(0.025 * rounds)], means[int(0.975 * rounds)]


if __name__ == "__main__":
    rs = rows()
    n = len(rs)
    ids = sorted({r["case"] for r in rs})
    first = {c: [r for r in rs if r["case"] == c][0] for c in ids}
    print(f"  {n} runs: {len(CASES)} questions x {TRIALS} trials,"
          f" each asked of")
    print(f"  both models. {clock.CHEAP} and {clock.CAPABLE}.\n")
    #  How much evidence is here, which is NOT the number of runs.
    #  Chapter 20's rule is that repeats are averaged within a case
    #  and never recorded as extra rows - and this data is why the
    #  rule exists: the cheap model returned the same answer, byte
    #  for byte, on all three trials of every case.
    ident = sum(1 for c in ids
                if len({r["cheap_answer"] for r in rs
                        if r["case"] == c}) == 1)
    identc = sum(1 for c in ids
                 if len({r["capable_answer"] for r in rs
                         if r["case"] == c}) == 1)
    print(f"  Cases whose {TRIALS} answers are byte-identical:"
          f" {ident} of {len(ids)}")
    print(f"  cheap, {identc} of {len(ids)} capable. So the evidence"
          f" is {len(ids)} cases")
    print(f"  and not {n} rows, and every count below is per CASE,")
    print("  scored on the first trial.\n")

    print("  1. WHAT EACH ARM GOT RIGHT, AND WHAT IT COST.\n")
    print("  arm        passed   $/1k req   seconds   $ per pass")
    for arm in ARMS:
        ok = sum(first[c][f"{arm}_passed"] for c in ids)
        d = statistics.fmean(r[f"{arm}_dollars"] for r in rs)
        s = statistics.fmean(r[f"{arm}_s"] for r in rs)
        per = (d * len(ids) / ok) if ok else float("nan")
        print(f"  {arm:<11}{ok:>4}/{len(ids):<4}{d * 1000:>9.2f}"
              f"{s:>10.2f}{per * 1000:>12.2f}")
    print("\n  The last column is chapter 47's cost per success:")
    print("  input and output priced, divided by the answers that")
    print("  passed rather than by the requests made.\n")

    import textwrap
    print("  2. WHERE THE ESCALATION FIRED, AND WHY.\n")
    esc = [c for c in ids if first[c]["escalated"]]
    print(f"     {len(esc)} of {len(ids)} cases escalated, with the")
    print("     phrase that fired and the reply it fired on:\n")
    for c in esc:
        print(f"       {c}  {first[c]['escalated']}")
        for line in textwrap.wrap(first[c]["cheap_answer"], 46)[:3]:
            print(f"            {line}")
    print("\n     Read those replies. Not one declines to answer:")
    print("     they are correct answers worded in the negative,")
    print("     and 'cannot' is how a refusal is worded. The rule")
    print("     was built to catch a model saying it does not know")
    print("     and it catches a model saying no.\n")
    print("     escalated?   cheap right   cheap wrong")
    for flag, label in ((True, "yes"), (False, "no")):
        sel = [c for c in ids if bool(first[c]["escalated"]) is flag]
        right = sum(first[c]["cheap_passed"] for c in sel)
        print(f"     {label:<13}{right:>10}{len(sel) - right:>14}")
    needless = sum(1 for c in ids if first[c]["escalated"]
                   and first[c]["cheap_passed"])
    wrong_kept = sum(1 for c in ids if not first[c]["escalated"]
                     and not first[c]["cheap_passed"])
    print(f"\n     A router's two mistakes are the {needless}"
          f" escalations it did")
    print(f"     not need and the {wrong_kept} wrong answers it"
          f" kept.")
    if wrong_kept == 0:
        print("     Only one cell is populated, so nothing here")
        print("     says what the rule does with a wrong answer:")
        print("     it never met one it let through.\n")
    else:
        print()

    print("  3. IS THE DIFFERENCE REAL. One CASE to a row, trials")
    print("     averaged within it, paired because every case is")
    print("     asked of every arm.\n")
    PAIRS = [("cheap", "capable"), ("cheap", "cascade"),
             ("cascade", "capable")]
    for field, label, scale in (("passed", "answers right", 1),
                                ("dollars", "$ per 1,000", 1000)):
        print(f"     {label}")
        print("       comparison          diff   95% interval")
        for a, b in PAIRS:
            pa = per_case(rs, f"{a}_{field}")
            pb = per_case(rs, f"{b}_{field}")
            keys = sorted(pa)
            pairs = [(pa[k], pb[k]) for k in keys]
            lo, hi = interval(pairs)
            d = statistics.fmean(pb[k] - pa[k] for k in keys)
            says = "clears" if (lo > 0 or hi < 0) else "cannot"
            print(f"       {b[:7]}-{a[:7]:<8}{d * scale:>+8.2f}"
                  f" {lo * scale:+.2f} to {hi * scale:+.2f}"
                  f"  {says}")
        print()
```

```text
  Re-graded with the current keys: 6 of 72 verdicts move.
    r10 capable: 3 trial(s) FAIL -> pass
    r10 cheap: 3 trial(s) FAIL -> pass

  36 runs: 12 questions x 3 trials, each asked of
  both models. gpt-4o-mini-2024-07-18 and gpt-4o-2024-08-06.

  Cases whose 3 answers are byte-identical: 12 of 12
  cheap, 10 of 12 capable. So the evidence is 12 cases
  and not 36 rows, and every count below is per CASE,
  scored on the first trial.

  1. WHAT EACH ARM GOT RIGHT, AND WHAT IT COST.

  arm        passed   $/1k req   seconds   $ per pass
  cheap        12/12       0.11      1.14        0.11
  capable      12/12       1.78      1.20        1.78
  cascade      12/12       0.58      1.44        0.58

  The last column is chapter 47's cost per success:
  input and output priced, divided by the answers that
  passed rather than by the requests made.

  2. WHERE THE ESCALATION FIRED, AND WHY.

     3 of 12 cases escalated, with the
     phrase that fired and the reply it fired on:

       r07  matched 'cannot'
            No, personalised goods cannot be returned
            under this policy.
       r10  matched 'does not'
            You, as the customer, pay the return postage
            for the clearance kettle. Since your card is
            closed, the refund will be issued as account
       r11  matched 'cannot'
            You cannot return the clearance item because
            the return window is 14 days, and it has been
            20 days since delivery. The standard return

     Read those replies. Not one declines to answer:
     they are correct answers worded in the negative,
     and 'cannot' is how a refusal is worded. The rule
     was built to catch a model saying it does not know
     and it catches a model saying no.

     escalated?   cheap right   cheap wrong
     yes                   3             0
     no                    9             0

     A router's two mistakes are the 3 escalations it did
     not need and the 0 wrong answers it kept.
     Only one cell is populated, so nothing here
     says what the rule does with a wrong answer:
     it never met one it let through.

  3. IS THE DIFFERENCE REAL. One CASE to a row, trials
     averaged within it, paired because every case is
     asked of every arm.

     answers right
       comparison          diff   95% interval
       capable-cheap      +0.00 +0.00 to +0.00  cannot
       cascade-cheap      +0.00 +0.00 to +0.00  cannot
       capable-cascade    +0.00 +0.00 to +0.00  cannot

     $ per 1,000
       comparison          diff   95% interval
       capable-cheap      +1.67 +1.56 to +1.78  clears
       cascade-cheap      +0.47 +0.00 to +0.97  cannot
       capable-cascade    +1.20 +0.72 to +1.61  clears
```

**First, how much evidence is here, because it is not thirty-six of anything.** The cheap model
returned the *same answer, byte for byte*, on all three trials of every one of the twelve cases;
the capable model did on ten of twelve. So the repeats bought almost nothing, which is Chapter 20's
rule arriving as a fact about this data — repeats are averaged within a case and never recorded as
extra rows. Every count below is per case, and the first draft of this step reported all of them
tripled.

**The two models got the same number right: 12 of 12.** Both. The paired interval on the difference
is +0.000 from +0.000 to +0.000, because there is no case where one passed and the other failed.
The capable model costs sixteen times as much per thousand requests, $1.78 against $0.11, and on
these twelve questions it buys nothing at all.

**One of those twelve was mine to be embarrassed by.** The two-part question about a closed card
and a clearance return was marked failed by both models, and the chapter's first draft called it
*the one question neither model can do*. The answer key demanded a bank transfer. The documents
make account credit the default — *we issue account credit instead, which is immediate, does not
expire* — and a transfer the opt-in alternative, which is what you ask for if you would rather have
the money. Both models gave the documented default. The key was wrong and the models were right,
and re-grading the stored answers moved six verdicts without a single new call.

**So the cascade pays for a second call and gets nothing for it.** It costs $0.58 per thousand —
5.4 times the cheap model — and answers 12 of 12, which is what the cheap model answered on its
own. Its cost per success is $0.58 against the cheap model's $0.11. **A cascade is worth building
when the expensive model is better on the cases you escalate**, and the first thing to measure is
whether it is, before building anything. The chapter's own interval is softer than that sentence:
cascade minus cheap is +0.47 per thousand from +0.00 to +0.97, which does not clear zero on twelve
cases. The point estimate is a fivefold cost increase and the interval will not swear to it, and
both halves of that belong in the answer.

**The escalation table is where to look, and the reason the rule fired is not the one I expected.**
Three of twelve cases escalated. Every one is a correct answer, and every one fired on a phrase
from a list built to catch a model *declining* to answer:

- *No, personalised goods* `cannot` *be returned under this policy.*
- *You* `cannot` *return the clearance item because the return window is 14 days…*
- *…the refund will be issued as account credit, which* `does not` *expire…*

None of them declines anything. They are correct answers worded in the negative, and `cannot` is
how a refusal is worded. **The rule was built to catch a model saying it does not know, and what it
catches is a model saying no.**

**That is a sharper failure than the one the idea of a cascade warns you about.** It is not that the
router cannot tell a hard case from an easy one — it is that the signal it uses is a *word*, and
the word belongs to two different things. Every question in this set whose right answer is a
refusal escalates, by construction, for ever, at full price. A keyword list cannot be made to tell
*I cannot answer* from *you cannot do that*, because the difference is who the subject is.

**And only one of the router's two mistakes is visible here.** It made three escalations it did not
need and kept zero wrong answers — because there were no wrong answers to keep. So nothing in this
data says what the rule does with a confidently wrong reply, which is the failure that actually
costs you something, and the chapter's first draft asserted it anyway.

> **Note:** Chapter 47 built its whole task set around questions needing two documents, and this
> set has four of them. All four are answered correctly by both models — so the mode Chapter 47
> found hardest is not what separates these arms, and nothing here contradicts Chapter 47 either,
> whose own ledger row warns against blaming retrieval for a two-part question. What separated
> them, before the key was fixed, was my key.

> **Warning:** Twelve questions cannot establish that two models are equally good, and the
> zero-width interval is the proof rather than the problem: there is no case where they differ, so
> the resample has nothing to vary and reports no spread. Chapter 46 met the same thing and gave it
> the right name — the absence of evidence about spread, not certainty about the value. What this
> measurement establishes is narrower and still worth having: **on this system's own traffic, with
> these twelve questions, the expensive model is not better**, so the cascade has nothing to route
> to *here*. It establishes that because all twelve are at the ceiling, which is also why it can
> establish nothing about the difference — a comparison needs cases the arms disagree on, and
> finding those is the work Chapter 20's method is for.

## Step 5: The Bill, and What the Levers Add To

Five whole designs rather than three savings, because savings from different levers on different
traffic do not add up and a table of them invites exactly that mistake. The sixth design the
levers suggest — the library in front *and* the cascade — is not priced, and the program says so
rather than promising it: it would need a third data set, and Step 4's verdict is that the cascade
buys nothing, so the combination would cost more than either half for the same answers.

```python
"""Cost per request, before and after, and what the levers add to.

The three levers in this chapter are not independent and cannot be
added up, which is the thing a table of savings hides. So this
program prices five whole designs rather than three savings:

  baseline      retrieval, stable part first, cheap model
  upfront       the library in front of every request, cheap
                model - the shape the cache can reach
  cheap only    the routing questions, cheap model
  capable only  the routing questions, capable model
  cascade       the routing questions, cheap then capable

The design the chapter's own levers suggest - the library in front
AND the cascade - is NOT priced, and saying so is better than a
docstring that promises it. It would need the routing questions run
against the up-front shape, a third data set; and section 2's
verdict is that the cascade buys nothing, so the combination would
cost more than either half and buy the same.

Every figure is the provider's own token count from a priced call
and the price list in clock.py, which is written down rather than
fetched so the arithmetic can be redone when the prices change.

Chapter 53 owns the bill as a product constraint and will measure
against this baseline. What this program owns is the baseline.
"""
import json
import pathlib
import statistics

import clock
import order
import route
import work


def read(path):
    p = pathlib.Path(path)
    return json.loads(p.read_text()) if p.exists() else []


def mean(rows, field):
    vals = [r[field] for r in rows]
    return statistics.fmean(vals) if vals else 0.0


if __name__ == "__main__":
    ords = order.rows()
    rts = route.rows()

    print("  Every figure below is the provider's own token count")
    print("  and the price list in clock.py, read on 2026-10-30:")
    for model, p in clock.PRICE.items():
        print(f"    {model}")
        print(f"      ${p['in']:.3f} in, ${p['cached']:.3f} cached,"
              f" ${p['out']:.3f} out per million")
    print()

    print("  1. WHAT ONE REQUEST COSTS, five whole designs.")
    print("     A MEDIAN beside the mean, because one baseline")
    print("     call took 11 seconds and a mean of 24 hides it.\n")
    base = [r for r in ords if r["shape"] == "grounded"
            and r["order"] == "stable-first"]
    secs = sorted(r["total_s"] for r in base)
    up = [r for r in ords if r["shape"] == "upfront"
          and r["order"] == "stable-first"]
    rows = [("baseline", clock.CHEAP, mean(base, "dollars"),
             mean(base, "cached_tokens") / max(mean(base, "in_tokens"), 1),
             mean(base, "total_s")),
            ("upfront", clock.CHEAP, mean(up, "dollars"),
             mean(up, "cached_tokens") / max(mean(up, "in_tokens"), 1),
             mean(up, "total_s"))]
    for arm, label, model in (("cheap", "cheap only", clock.CHEAP),
                              ("capable", "capable only",
                               clock.CAPABLE),
                              ("cascade", "cascade", "both")):
        rows.append((label, model, mean(rts, f"{arm}_dollars"),
                     None, mean(rts, f"{arm}_s")))
    print("  design        model   $/1k req  cached  mean  med")
    for name, model, d, cached, s in rows:
        short = ("mini" if model == clock.CHEAP
                 else "4o" if model == clock.CAPABLE else "both")
        group = (base if name == "baseline"
                 else up if name == "upfront" else None)
        if group is not None:
            med = statistics.median(r["total_s"] for r in group)
        else:
            key = ("cheap" if name == "cheap only" else
                   "capable" if name == "capable only"
                   else "cascade")
            med = statistics.median(r[f"{key}_s"] for r in rts)
        cell = ("      -" if cached is None else f"{cached:>7.0%}")
        print(f"  {name:<14}{short:<8}{d * 1000:>8.2f}{cell}"
              f"{s:>6.2f}{med:>5.2f}")
    print(f"\n  The baseline's {len(secs)} calls run from"
          f" {secs[0]:.2f} to {secs[-1]:.2f} seconds,")
    print(f"  median {statistics.median(secs):.2f}. One took"
          f" {secs[-1]:.2f}, which is"
          f" {secs[-1] / statistics.median(secs):.0f} times")
    print("  the median - and is the best evidence in this chapter")
    print("  for what step 2 concluded, that the wait is a queue.")
    print("  QUOTE THE MEDIAN. A mean of 24 calls with an")
    print("  11-second outlier is not a cost per request.")
    print("\n  The cached column is a measurement for the first two")
    print("  rows and a dash for the routing rows, because")
    print("  route.json stores no cached count: those prompts are")
    print("  the short retrieved ones, under the cache's minimum,")
    print("  so there is nothing to store. A zero would have read")
    print("  as a measurement.")
    print("\n  The routing rows are the 12 routing questions and the")
    print("  first two are the 8 corpus queries, so the two groups")
    print("  are not the same requests and their costs are not")
    print("  subtractable. That is why this is five designs rather")
    print("  than a saving per lever.")

    print("\n  2. WHAT EACH LEVER WAS WORTH HERE.\n")
    b = mean(base, "dollars")
    u = mean(up, "dollars")
    ch = mean(rts, "cheap_dollars")
    ca = mean(rts, "capable_dollars")
    cs = mean(rts, "cascade_dollars")
    print(f"     the reordering lever on the baseline shape:"
          f" nothing")
    print(f"       its prompts are under the cache's minimum")
    print(f"     the reordering lever on the up-front shape:"
          f" it works")
    print(f"       and the up-front shape costs"
          f" {u / b:.1f} times the baseline")
    print(f"       anyway, so the design the lever helps is the")
    print(f"       one you would not have chosen")
    print(f"     the cascade against the capable model:"
          f" {cs / ca:.2f} of its cost")
    print(f"     the cascade against the cheap model:"
          f" {cs / ch:.2f} of its cost")
    #  The verdict, computed. Three levers and the program says
    #  which of them this system should take rather than leaving a
    #  reader to add up savings that do not add up.
    #  Per CASE, not per row. route.py's own output says why: the
    #  cheap model's three trials are byte-identical on every case,
    #  so 36 rows are 12 cases three times and counting rows
    #  triples the evidence. Chapter 20's rule, and this program
    #  was the one place the per-case fix did not reach.
    ids = sorted({r["case"] for r in rts})
    firsts = {c: [r for r in rts if r["case"] == c][0] for c in ids}
    ok_cheap = sum(firsts[c]["cheap_passed"] for c in ids)
    ok_cap = sum(firsts[c]["capable_passed"] for c in ids)
    ok_cas = sum(firsts[c]["cascade_passed"] for c in ids)
    print(f"\n     And the quality the money bought:"
          f" {ok_cheap}, {ok_cap} and {ok_cas}")
    print(f"     of {len(ids)} CASES for cheap, capable and the"
          f" cascade.")
    if ok_cap <= ok_cheap:
        print("\n     So the routing lever has nothing to route TO.")
        print("     A cascade is worth building when the expensive")
        print("     model is better on the cases you escalate, and")
        print("     on these twelve questions it is not better on")
        print("     any case at all - so the cascade pays for a")
        print(f"     second call {cs / ch:.1f} times over and buys"
              f" nothing.")
    else:
        print("\n     The capable model is better, so the cascade's")
        print("     cost has something to be weighed against.")
    print("\n     Which leaves this system with no lever from this")
    print("     chapter that it should pull, and that is the")
    print("     result. Two of the three do not apply to its")
    print("     traffic and the third buys no quality. The baseline")
    print("     at the top of the first table is what chapter 53")
    print("     will measure against, and it is the design the")
    print("     system already had.")

    print("\n  3. WHAT THE MEASURING COST.\n")
    streamed = read("wait.json")
    priced = len(ords) + 2 * len(rts)
    print(f"     {len(streamed)} streamed calls for the clock")
    print(f"     {len(ords)} priced calls for the orders")
    print(f"     {2 * len(rts)} priced calls for the routing, because")
    print("       every case is asked of both models")
    print(f"     {len(streamed) + priced} calls in all")
    total = (sum(r["dollars"] for r in ords)
             + sum(r["cheap_dollars"] + r["capable_dollars"]
                   for r in rts))
    print(f"\n     The priced calls came to ${total:.4f}. The")
    print("     streamed ones carry no usage block, so this")
    print("     program cannot price them - which is the same")
    print("     limitation clock.py is built around and is worth")
    print("     saying twice: the clock and the bill cannot be read")
    print("     off one call.")
```

```text
  Re-graded with the current keys: 6 of 72 verdicts move.
    r10 capable: 3 trial(s) FAIL -> pass
    r10 cheap: 3 trial(s) FAIL -> pass

  Every figure below is the provider's own token count
  and the price list in clock.py, read on 2026-10-30:
    gpt-4o-mini-2024-07-18
      $0.150 in, $0.075 cached, $0.600 out per million
    gpt-4o-2024-08-06
      $2.500 in, $1.250 cached, $10.000 out per million

  1. WHAT ONE REQUEST COSTS, five whole designs.
     A MEDIAN beside the mean, because one baseline
     call took 11 seconds and a mean of 24 hides it.

  design        model   $/1k req  cached  mean  med
  baseline      mini        0.11     0%  1.74 1.31
  upfront       mini        0.20    99%  1.28 1.14
  cheap only    mini        0.11      -  1.14 1.11
  capable only  4o          1.78      -  1.20 1.11
  cascade       both        0.58      -  1.44 1.21

  The baseline's 24 calls run from 0.98 to 11.01 seconds,
  median 1.31. One took 11.01, which is 8 times
  the median - and is the best evidence in this chapter
  for what step 2 concluded, that the wait is a queue.
  QUOTE THE MEDIAN. A mean of 24 calls with an
  11-second outlier is not a cost per request.

  The cached column is a measurement for the first two
  rows and a dash for the routing rows, because
  route.json stores no cached count: those prompts are
  the short retrieved ones, under the cache's minimum,
  so there is nothing to store. A zero would have read
  as a measurement.

  The routing rows are the 12 routing questions and the
  first two are the 8 corpus queries, so the two groups
  are not the same requests and their costs are not
  subtractable. That is why this is five designs rather
  than a saving per lever.

  2. WHAT EACH LEVER WAS WORTH HERE.

     the reordering lever on the baseline shape: nothing
       its prompts are under the cache's minimum
     the reordering lever on the up-front shape: it works
       and the up-front shape costs 1.8 times the baseline
       anyway, so the design the lever helps is the
       one you would not have chosen
     the cascade against the capable model: 0.32 of its cost
     the cascade against the cheap model: 5.41 of its cost

     And the quality the money bought: 12, 12 and 12
     of 12 CASES for cheap, capable and the cascade.

     So the routing lever has nothing to route TO.
     A cascade is worth building when the expensive
     model is better on the cases you escalate, and
     on these twelve questions it is not better on
     any case at all - so the cascade pays for a
     second call 5.4 times over and buys nothing.

     Which leaves this system with no lever from this
     chapter that it should pull, and that is the
     result. Two of the three do not apply to its
     traffic and the third buys no quality. The baseline
     at the top of the first table is what chapter 53
     will measure against, and it is the design the
     system already had.

  3. WHAT THE MEASURING COST.

     72 streamed calls for the clock
     144 priced calls for the orders
     72 priced calls for the routing, because
       every case is asked of both models
     288 calls in all

     The priced calls came to $0.0992. The
     streamed ones carry no usage block, so this
     program cannot price them - which is the same
     limitation clock.py is built around and is worth
     saying twice: the clock and the bill cannot be read
     off one call.
```

**The baseline is $0.11 per thousand requests, and its latency is a median of 1.31 seconds** —
not the mean of 1.74, which is one call in twenty-four that took 11.01 seconds, eight times the
median. Those are the numbers Chapter 53 measures against, and the median is the one to quote.
It is the design the system already had.

**That 11-second call is the best evidence in the chapter for what step 2 concluded.** Nothing
about that request is unusual: the same eight requests, the same text, the same model. The same
request, trial three, measured two other ways in the same lab: *1.00 seconds* with the question
first, and *0.99 seconds* streamed. If the wait were the
computation, the computation would have to have been eight times harder for one call out of
twenty-four. It was a queue.

**Three levers, and this system should pull none of them.**

- *Reordering the prompt* does nothing, because the retrieved requests are under the cache's
  minimum length. On the one shape it reaches it is worth $0.19 per thousand, about half that
  shape's input bill — but the shape costs 3.4 times the baseline before the lever and 1.8 times
  after it, so taking both together still costs $0.09 per thousand more than the design you
  started with.
- *Routing to a cheap model* has nothing to route to: the expensive model answers the same 12 of
  12. The cascade costs 5.4 times the cheap model by the point estimate — +0.47 per thousand from
  +0.00 to +0.97, which does not clear zero on twelve cases — and answers what the cheap model
  answered alone.
- *Shortening the prompt for speed* is the lever step 2 finds nothing for: the wait is a queue at
  these lengths, so there is no computation to remove that you could feel.

**That is the result, and it is worth being blunt about how it reads.** A chapter called *measure and
reduce* ends with nothing reduced. What it has instead is a baseline somebody can be held to, three
levers priced on this system's own traffic rather than on an example chosen to show them working,
and the reason each one failed — which is the part that transfers, because the reasons are
properties of the traffic and the next system will have different ones.

> **Note:** The 1,024-token minimum is the one number in this chapter that is **not** measured. It
> is a constant in the program, taken from the provider's published figure, and what the
> measurement does is bracket it: nothing cached at 637 tokens, almost everything at 2,458. So the
> chapter can say the lever does not reach this traffic and cannot say where the threshold is. If
> you are relying on it, measure your own shapes rather than the documentation — the bracketing is
> four lines of code and the figure is the provider's to change.

> **Warning:** Every price here is dated. The two models' rates were read on 30 October 2026 and
> written into `clock.py` rather than fetched, so every figure in this chapter can be recomputed
> from the token counts when the rates change — and they will, which Chapter 1 says in so many
> words. What does not change is that output costs several times input, that a cached prefix is
> discounted rather than free, and that a model sixteen times the price has to be sixteen times
> something to be worth it.

## Step 6: What Three Levers Taught About Measuring One

Three measurements, three failures, and the failures have one shape.

**Each lever failed for a reason that is a property of this traffic, not of the lever.** The
prompt cache has a minimum and these prompts are short. The queue dominates the wait and these
prompts are not long enough for prefill to matter. The cheap model is already right and these
questions are not hard enough to need the expensive one. **Every one of those is a fact about
the workload that you can only get by measuring the workload**, and none of them is a reason the
lever is bad.

**And twice the measurement nearly produced the wrong answer, in the two ways a measurement does.**
The timing run had a confound that looked like a result with a tight interval, and it was the
running order. The ordering run had a pooled figure — 66 per cent cached for an arrangement that
caches nothing — that was three identical questions and not a lever at two-thirds strength. Both
were caught by splitting something: the first by interleaving and recording the sequence, the
second by reading the trials apart. **A lever measurement is a comparison, so everything this book
has said about comparisons applies**, and the thing that makes these two harder than most is that
the nuisance variable is *time* — and time is the one variable that cannot be held constant,
because the measurement takes some.

> **Note:** The two levers this chapter did not pull are the two it could not. Quantisation and
> self-hosted serving are levers on a machine you run, and this lab calls a hosted service, so
> Chapter 15's arithmetic for them stays arithmetic here. Chapter 52 owns the rest of the menu —
> application-level response caching, speculative decoding, continuous batching, a paged cache —
> and Chapter 53 owns what to do about the bill this chapter measured.

## Summary, Key Terms, and Review Questions

### Summary

Three levers pulled on this book's own system, and the point of the chapter is what measuring them
on real traffic does to each. **Time to first token does not move measurably with the prompt
here**: quadrupling the input from 612 to 2,458 tokens gives +0.16 seconds with 95 per cent from
−0.04 to +0.34, and an earlier run of the same comparison gave −0.01 from −0.08 to +0.07 — two
runs, point estimates 0.17 seconds apart, neither clearing zero, which is what a noise-dominated
number looks like. Chapter 15's own arithmetic says why the computation is not what you are
waiting for at this length, and its batching section says what is. **Time per token moves in the
direction Chapter 15 says it should not**, and the figure to carry is the smaller one. Over all
the gaps, nine times the output makes each token arrive 2.77 milliseconds sooner; over **matched
positions** — the first twenty-one gaps of both arms, which is the only comparison that treats
them alike — it is **−1.79 milliseconds with 95 per cent from −3.64 to −0.03**, clearing zero and
only just. Dropping the early gaps from both arms makes the difference *grow*, and that proves
nothing, because it removes a quarter of the short reply's gaps and three per cent of the long
one's. What does hold the finding up is the matched comparison, plus a check that a chunk is a
token here at all — ratios 1.04, 1.00 and 1.00 against the provider's own output counts. The
mechanism is outside what this lab can see.
**Reordering the prompt so the stable part comes first is total where it applies and does not
apply here**: on the up-front shape, 2,432 of 2,458 input tokens come back cached on the first
trial against zero for the question-first order, worth $0.19 per thousand requests from −0.193 to
−0.182 on first-outing traffic and nothing measurable in time — and the two retrieved shapes get no
cached tokens in either order, because their prompts are about 612 and 637 tokens against the
provider's 1,024 minimum. **The lever reaches only the design Chapter 35 priced and rejected**,
which costs 3.4 times the baseline before the lever and 1.8 times after it, so taking both still
costs $0.09 per thousand more than the baseline. **And routing has nothing to route to**: the
cheap and the capable model both answer 12 of 12 — the evidence is twelve cases and not
thirty-six rows, because the cheap model's three trials are byte-identical on every one — with a
paired difference of zero and no case where one passes and the other fails. The cascade costs 5.3
times the cheap model by the point estimate, on an interval from +0.00 to +0.97 that does not
clear zero. Three of twelve cases escalated, **all three of them correct answers**, every one
because a phrase list built to catch a model declining to answer matched a correct refusal. Two
phrases did it, `cannot` and `does not`, inside *No, personalised goods cannot be returned*, *You
cannot return the clearance item* and *account credit, which does not expire*. The baseline is **$0.11 per thousand
requests with a median latency of 1.31 seconds** — the mean of 1.74 is one call of twenty-four
that took 11.01, which is the chapter's own sharpest evidence that the wait is a queue — and those
are the figures Chapter 53 measures against. Two mistakes are on the record because they
are the chapter's real subject: a confound that was the running order and read as a 0.23-second
effect with an interval clear of zero, and a pooled cache figure of 66 per cent that was three
identical questions.

### Key Terms

| Term | Meaning |
|---|---|
| **Prompt-prefix cache** | A provider's reuse of the leading tokens of a request that match a request it has already served. Matches a *prefix*, so it is destroyed by anything that changes the first bytes — and it has a minimum prompt length, below which it never fires at all. Discounts the tokens it covers rather than removing them |
| **Cascade** | Running a cheap model first and escalating to an expensive one when your code judges the cheap answer unusable. Costs both calls on every escalation, so it is worth building only where the expensive model is measurably better on the cases that escalate |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The first thing to ask of a lever | Whether it applies to your traffic at all. Two of three did not here |
| Why prompt caching can do nothing | A minimum prompt length. 612 and 637 tokens against a 1,024 minimum |
| What the ordering lever really buys | *Different* requests sharing a prefix — not a request reusing its own earlier self, which is a response cache |
| Worked: reordering | 2,432 of 2,458 tokens cached against 0, and $0.19 per 1,000 requests — priced on first-outing traffic, because pricing it against repeats of the same question understates it by a factor of 2.8 |
| What a cascade needs before you build it | Evidence the expensive model is better on the cases that escalate. Here both answered 12 of 12 |
| A cascade's cost | Both calls on every escalation: 5.4x the cheap model for the same answers, on an interval that does not clear zero at 12 cases |
| Time to first token, measured | 0.84 s on the baseline shape, and no effect this could detect from a 4x prompt or a 9x reply — on 8 paired requests, with the point estimate ranging −0.07 to +0.47 across three trials |
| The baseline this chapter hands on | $0.11 per 1,000 requests; latency **median 1.31 s**, mean 1.74 s over 24 calls because one took 11.01. Quote the median |
| What a decline-detector catches | A correct refusal. `cannot` is how both are worded, so every question whose right answer is *no* escalates for ever |
| What a timing confound looks like | A result with a tight interval. Interleave the arms and record the sequence — which lets you *see* the drift and does not remove it |

### Review Questions

1. How did you reduce cost per request, and what did it cost you in quality?
2. You are asked to make a system faster. What do you measure first, and what do you expect to find?
3. What is prompt-prefix caching, and how do you order a prompt for it?
4. When is a cascade worth building, and how would you find out before building one?
5. You measure a lever and it helps by an amount with a tight interval. What would make you distrust that?
6. Chapter 15 says the wait before the first token grows with the prompt. You measure it and it does not. Who is wrong?

### Review Answers

1. I did not reduce it, and the measurement is the answer. Three levers priced on this system's own
traffic: reordering the prompt for the provider's cache, routing easy cases to a cheap model, and
shortening the prompt for speed. **The first does not apply** — the retrieved requests are about
612 tokens and the cache's minimum is 1,024, so no ordering changes anything; on the one shape long
enough to reach it the lever is worth $0.19 per thousand, and that shape costs 3.4 times the
baseline before the lever and 1.8 times after, so taking both still costs $0.09 per thousand more
than the design I had. **The second has nothing to route to** — the sixteen-times-dearer model
answers the same 12 of 12, with no case where one passes and the other fails, so the cascade costs
five times the cheap model for the same answers. **The third is removed by the first measurement** —
at these prompt lengths the wait is a queue rather than prefill, which one call in twenty-four
taking eight times the median shows plainly. So the quality cost is nothing, because nothing was
traded: the baseline is $0.11 per thousand at a median 1.31 seconds and it is what the system
already had.

That is the answer I would give, and the reason it is a better answer than a reduction story is
that every one of the three failures is a **fact about this traffic** rather than about the lever:
a minimum prompt length, a question set the cheap model already handles, prompts too short for
prefill to matter. Name those and an interviewer learns what you measured and what you would
measure next. The things that would change it: longer prompts, where both the cache and prefill
start to bite; harder questions, where the capable model might earn its price; and higher volume,
where $0.09 per thousand stops being a rounding error.
2. The two halves separately, on your own traffic, with repeats — time to first token and time per
token, which Chapter 15 names and explains. What to expect is that the halves answer to different
things and that neither may be what you assumed. On this system, quadrupling the prompt did not
move time to first token by an amount two runs could agree on, because at 2,458 tokens the prefill
computation is a few milliseconds and the 0.84 seconds is a queue. So the first thing the
measurement buys is knowing which lever is pointless: shortening a prompt that is already short
cannot help a wait you are not spending on prefill. And measure on your own requests rather than
on a long example, because the length of your traffic is what decides which half you are in.
3. It is the provider reusing the leading tokens of your request when they match a request it has
already served. It matches a *prefix*, so you order the prompt with everything stable at the
front — the instruction, the documents, the examples — and the part that changes at the back,
which is usually the user's question. What that buys is *different* requests sharing a prefix:
here, with the stable part first, 2,432 of 2,458 input tokens came back cached on the very first
trial because request two reused what request one left behind. With the question first, zero. Two
things to say next. It has a minimum prompt length — 1,024 tokens on the service used here, which is the provider's published figure rather
than something this lab measured —
so on short requests it never fires whatever you do, and two of this lab's three shapes got
nothing in either order. And a prefix must be byte-identical, so a set of documents iterated in a
different order is the same text and a different prefix.
4. When the expensive model is better on the cases that escalate — and you find out by measuring
both models on your own cases *before* building anything, which costs one run of each. A cascade
pays for both calls on every escalation, so if the expensive model is not better the cascade is
strictly worse than the cheap model on cost, on latency and on nothing gained. That is what
happened here: both models answered 12 of 12 with no case where one passed and the other failed,
and the cascade cost 5.4 times the cheap model by the point estimate, on an interval that does not
clear zero. The escalation table is the thing to look at rather than the rate, because its two
wrong cells are different mistakes: escalations that were not needed — three of three here — and
cheap answers that were wrong and kept, of which this data has none, so it says nothing about the
second. And look at *why* the three fired. Every one is a correct answer worded in the negative,
matched by a phrase list built to catch a model declining to answer: `cannot` is how a refusal is
worded, so every question whose right answer is a refusal escalates for ever at full price. A
keyword cannot tell *I cannot answer* from *you cannot do that*, because the difference is who the
subject is.
5. That the nuisance variable in a timing measurement is time itself, and it cannot be held
constant because measuring takes some. The specific thing to distrust is an arm that ran in a
block: load, routing and a warming connection all drift smoothly, and a smooth drift aligned with
your arms is indistinguishable from an effect. This chapter's first timing run reported that a
longer answer made the *first* token arrive 0.23 seconds sooner, with 95 per cent from −0.46 to
−0.03, and that was the running order. Interleave the arms, record each call's sequence number,
and report whether the number trends with it — which does not remove the drift but moves it from
the difference into the width of the interval. The second thing to distrust is a figure pooled
over repeats of the same input: this chapter's cache measurement read 66 per cent for an
arrangement that caches nothing, because the same eight questions were asked three times.
6. Neither, and the question is the wrong shape. Chapter 15 is about the computation: prefill
handles the whole prompt before a token comes back, so the arithmetic grows with the prompt and
its attention part faster than proportionally. That is true and it is not what you are waiting
for at 2,458 tokens, because the arithmetic there is milliseconds and the wait is most of a
second. Chapter 15 supplies both halves of the resolution itself — its own table shows the squared
term is one part in twenty at a thousand tokens, and its batching section says your request waits
to join a batch when the system is busy. So the measurement and the mechanism agree: the mechanism
that dominates a measured time to first token is not the one the prefill arithmetic describes,
until the prompt is long enough for the arithmetic to be worth noticing. The useful form of the
answer is that knowing why a thing is slow and knowing what your slow thing is are two different
pieces of work, and only the second tells you which lever to pull.

> **You understand this when** you can name a lever that is popular, say what it would need to be
> true of your own traffic to help, and say how you would find out in one afternoon.
