# Calling a Model Reliably

Chapter 18 was about what you send. This is about the call itself, and it is the chapter that
separates a script from a system. Everything in it is ordinary engineering — retries, limits,
concurrency, resumption — applied to a component with two properties that make it unusual: it
is slow, and it answers a piece at a time.

*The problem.* My script works for ten documents. For ten thousand it dies on a 429, and I
can't tell how far it got.

*The question.* What goes wrong when you call a model ten thousand times instead of ten, and
what does the code have to do about each of those things?

## Streaming

Chapter 15 explained why a reply arrives in pieces. This is how you receive them.

A streaming response is a long-lived HTTP connection down which the server sends small events
as it produces them, in a format called **server-sent events** — a line per event, each one a
`data:` line holding a small piece of JSON, with a blank line between events. The last line
is not JSON but a plain marker, so whatever reads the stream has to allow for it:

```text
  data: {"delta": "The"}

  data: {"delta": " cat"}

  data: {"delta": " sat"}

  data: [DONE]
```

Each piece is a **delta** — what to add to what you have so far, not the whole answer again.
Your code appends them. That is nearly the whole protocol, and it is deliberately dull. What
the last event looks like — the `[DONE]` marker above, or a typed event, or simply the
connection closing — is one of the things each provider decides for itself.

**What streaming buys you is a number you can feel.** The time to the first word falls to
whatever prefill takes, instead of the whole generation. Chapter 1 said two systems with the
same total time can feel completely different; this is the mechanism for the one that feels
fast.

**And now the thing that catches people**, and it follows from Chapter 13. A reply stops for
one of several reasons — the model finished, it hit your maximum, a stop condition fired — and
only the response itself says which. A truncated reply looks exactly like text. So the only way
to know you are holding a whole answer is to have reached the end of it.

**You cannot stream a response that you must validate as a whole.** If your code has to check
the answer before acting on it — that it is valid JSON, that it names a real product, that it
does not contain something forbidden — then you need all of it to run the check. And once you
have all of it, you have waited for the whole generation, so streaming has saved you no time
at all and has given you a more complicated code path for it.

Worse, if you stream it *to a user* and then your check fails, you have already shown them
the thing you were going to reject.

**The edge of that rule is worth knowing, because it shows why the rule holds.** If the answer
is a *sequence of independent units* — one JSON object per line, one row at a time — then each
unit is whole the moment it lands, so you can validate it and act on it while the rest is still
arriving. Streaming is fine there. What you cannot do is act on part of something that is only
valid in one piece.

And a stream gives you one thing a validator can use even then: if the first few tokens are
already wrong, you can close the connection instead of paying for the remaining nine hundred.

```text
  to a person                yes - reading, not checking
  one whole answer to check  no  - you must wait for the end
  independent units          yes - each is whole on arrival
```

So the rule is: **stream when the consumer can use a piece, and do not when it needs the
whole.** A person reading can use a piece. A check that only makes sense over the entire answer
cannot. Chapter 21 is where validation gets its own chapter, and the two decisions are
connected.

**Cancellation.** A streaming connection is open while the model generates, so you can close
it. A user navigates away, a timeout fires, a better answer arrives from somewhere else — shut
the connection and the generation normally stops. You are usually billed for what was produced
before you stopped, which is less than the whole. You can abandon a non-streaming call too, but
you have nothing to show for the time already spent, and no natural point at which to stop.

> **Tip:** The cancellation point is the one people forget to build. If your interface lets a
> user ask a second question before the first has finished, and you do not cancel the first,
> you are paying for an answer nobody will read — on every impatient user, forever.

## Rate Limits and 429s

A provider limits how fast you may call. The limits are usually two: requests per minute, and
tokens per minute. When you exceed one, the response is **HTTP 429** — *too many requests* —
and it is not an error in your code.

This is the commonest way a working script dies at scale, and the reason is arithmetic. Ten
documents at one a second is inside any limit. Ten thousand, loosed as fast as your machine can
open connections, is not.

**A 429 usually comes with a header saying how long to wait.** Use it when it is there. The
rest of this section is what to do when it is not, and what to do about the other failures
that look like it.

**Read the body of the error, not only the status.** The same 429 is returned when you are
going too fast, which waiting fixes, and when your account has run out of credit, which waiting
never fixes. The status cannot tell them apart; the error body usually can, and that is where
to look.

| What you get back | What it means | What to do |
|---|---|---|
| 429 | Too fast | Wait and retry |
| 429 with an exhausted quota | You are out of credit | **Do not retry.** Pay or ask for more |
| 500, 502, 503 | Their side broke | Wait and retry |
| Timeout, connection reset | Something in between broke | Wait and retry |
| 400 | Your request is malformed | **Do not retry.** Fix it |
| 401, 403 | Your key is wrong or lacks permission | **Do not retry** |
| 413, context length | You sent too much | **Do not retry.** Send less |

**The line down the middle of that table is the whole decision.** Retrying something
retryable costs a wait. Retrying something that will never succeed costs the same wait, every
time, forever — and a 400 retried five times with backoff spends the whole retry budget, on
every malformed request, learning nothing.

## Retries: Backoff and Jitter

Retry immediately and you make the problem worse: you were called too fast, so you call again
at once. The fix has two halves and both matter.

**Exponential backoff** doubles the wait after each failure. **Jitter** picks a random wait
*up to* that amount rather than exactly it.

```python
backoff = min(cap, base * 2 ** attempt)
wait = random.uniform(0, backoff)
```

Backoff keeps you from hammering a system that is struggling. Jitter keeps your ten thousand
parallel workers from retrying *in step* — without it, everything that failed at the same
moment retries at the same moment, which is the original problem again with extra steps.

Here is the whole thing, in a new empty folder as `retry.py`:

```python
import random

class RateLimited(Exception):
    pass

def call(attempt_log, fail_times):
    """Stands in for the API call. Fails the first `fail_times` times."""
    attempt_log.append(len(attempt_log) + 1)
    if len(attempt_log) <= fail_times:
        raise RateLimited("429")
    return "ok"

def with_retry(fail_times, tries=5, base=0.5, cap=8.0):
    log, waits = [], []
    for attempt in range(tries):
        try:
            return call(log, fail_times), waits
        except RateLimited:
            if attempt == tries - 1:
                raise
            backoff = min(cap, base * 2 ** attempt)
            waits.append(round(random.uniform(0, backoff), 2))
    raise RuntimeError("unreachable")

random.seed(19)
for fails in (0, 3):
    result, waits = with_retry(fails)
    print(f"failed {fails} time(s) -> {result} after waits {waits}")
```

```text
failed 0 time(s) -> ok after waits []
failed 3 time(s) -> ok after waits [0.34, 0.78, 1.04]
```

The real code would `time.sleep(wait)`; the example collects the waits instead so the output
is instant and the same for every reader. The ceiling those waits are drawn from doubles each
attempt and then stops:

```text
  attempt 1 fails: wait up to 0.5s
  attempt 2 fails: wait up to 1.0s
  attempt 3 fails: wait up to 2.0s
  attempt 4 fails: wait up to 4.0s
  attempt 5 fails: give up
```

**Five attempts, four waits.** The last attempt has nothing to wait for, which is easy to get
wrong when you are counting. The worst case is 0.5 + 1 + 2 + 4 = 7.5 seconds of sleeping, and
about half of that on average, because each wait is drawn from zero up to its ceiling. That is
a reasonable place to stop and tell somebody.

The cap never binds at five attempts; `min(cap, …)` is there so that a larger `tries` cannot
put you to sleep for an hour. At eight attempts the ceilings would be 0.5, 1, 2, 4, 8, 8, 8.

> **Warning:** Retries hide problems as well as solving them. A pipeline that retries
> everything three times and logs nothing looks healthy at three times the cost and a third of
> the speed. Count your retries, and alarm on the rate rather than on individual failures.

## Timeouts

Every call needs one, and the default is usually wrong.

The reason is Chapter 15's: a model's response time depends on the length of the reply and on
how busy the provider is, neither of which you control. A call that normally takes three seconds
can take sixty, and without a timeout one stuck connection holds a worker forever.

**Three timeouts, not one**, and this is where people get caught. A **connect** timeout — how
long to wait for the server to answer at all — can be short, a few seconds. A **read** timeout,
in most HTTP libraries, is *not* a budget for the whole response: it is the longest gap allowed
between one piece of the body and the next. That is the right tool for noticing a dead
connection, and it is useless for capping a long generation, because a model that sends a token
every half second never trips a thirty-second read timeout however long it talks. The cap on
the whole call is a third, **total timeout** — and some libraries do not have one, so you build
it yourself by wrapping the call, with `asyncio.timeout` or the equivalent.

**It is the total timeout you derive from the token cap.** If you cap the reply at 1,000 tokens
and tokens arrive at about twenty a second, fifty seconds is the floor.

> **Tip:** `max_tokens / 20 + 10` is a crude rule and it is far better than the 30 you were
> going to write, because it makes the relationship explicit to whoever reads the code next.
> Check which of the three knobs your library's `timeout=` argument actually sets. The names
> are not consistent between libraries, and the default is usually wrong for this work.

> **Note:** Several numbers in this chapter are the shape of the thing rather than the thing:
> how many limits a provider publishes, whether a 429 carries a retry-after header, how a
> cancelled stream is billed, whether idempotency keys are supported, and twenty tokens a
> second. All of them vary by provider and all of them move. Measure yours; the reasoning is
> what carries over.

## Concurrency, From Zero

Ten thousand documents at three seconds each is eight hours if you do them one at a time. You
do not have to.

The calls spend nearly all of that time waiting for a reply, so they can wait at the same
time. Python's `asyncio` is how you do that in one process, and the whole of what you need is
three ideas.

**`async def` makes a function that can be paused.** Calling it does not run it; it hands you
a coroutine, which is a job that has not started.

**`await` runs one and waits for it** — and while it waits, the program is free to run other
jobs. This is the whole point: `await` is where control is handed back.

**`asyncio.gather` runs many at once** and gives you the results in order.

That is enough to write it:

```python
import asyncio, time

async def fetch(doc, limiter):
    async with limiter:
        await asyncio.sleep(0.1)          # stands in for the call
        return f"done {doc}"

async def main(n, at_once):
    limiter = asyncio.Semaphore(at_once)
    started = time.perf_counter()
    results = await asyncio.gather(*(fetch(d, limiter) for d in range(n)))
    assert results == [f"done {d}" for d in range(n)]      # in order, always
    elapsed = time.perf_counter() - started
    print(f"{n} documents, {at_once} at once: {elapsed:.1f}s")

for at_once in (1, 4, 20):
    asyncio.run(main(20, at_once))
```

```text
20 documents, 1 at once: 2.0s
20 documents, 4 at once: 0.5s
20 documents, 20 at once: 0.1s
```

Twenty documents at a tenth of a second each: two seconds in a row, half a second four at a
time, a tenth of a second all at once. The arithmetic is exactly what you would expect, which
is the point of running it. The `assert` is doing real work — it is the claim that `gather`
hands back results in the order you asked for them, whatever order they finished in, and the
program would stop if that were not so.

**And now the line that matters.** A **semaphore** is a counter that bounds how many jobs may
be inside a block at the same time. `asyncio.Semaphore(at_once)` makes one. The statement
`async with limiter` takes a unit and gives it back at the end of the block, and when none is
left the next job waits. It is three words of code and it is what stands between you and the
previous
section.

**Without it, `gather` over ten thousand documents opens ten thousand connections at once**,
and every one of them comes back 429. The semaphore is not an optimisation. It is the
difference between concurrency and a denial-of-service attack on your own account.

**Work the number out from the provider's limit, not from your machine.** The rate you produce
is the bound divided by how long a call takes: 3 at once at 3 seconds each is one a second, or
60 a minute. So the bound you want is *rate × duration* — 60 a minute is one a second, times 3
seconds, is 3.

**But a semaphore bounds concurrency, not rate**, and the difference is the thing to say out
loud in an interview. If your calls come back faster than you assumed, the same bound produces
a higher rate and you are over the limit again — 3 at once at 1 second each is 180 a minute.
That is why you leave a margin, and it is why a tool that limits *rate* directly, a token
bucket, is the better answer when the limit is the one that actually hurts.

**One more thing about `gather`, and it is this chapter's own subject.** If any one job raises,
`gather` raises too — and the caller gets *nothing*, including the results of the jobs that
had already finished. Ten thousand documents, one failure at document four thousand, and you
are back at the problem this chapter opened with, caused by the tool that was meant to solve
it.

The fix is one argument:

```python
results = await asyncio.gather(*jobs, return_exceptions=True)
```

Now a failure arrives as an exception *object* in the results list, in the position of the job
that raised it, and every other result is intact. You walk the list, keep what worked, and
decide what to do about the rest — which is exactly what the record in *When It Dies Half-Way*,
two sections below, is for.

## Batch Endpoints

There is a second way to do ten thousand documents, and it is often the right one.

Providers offer a **batch endpoint**: you upload a file of requests, come back later, and
download a file of results. It is slower to finish — hours rather than minutes — and
substantially cheaper. Chapter 15 is the reason it can be: a batch reads each parameter once
and shares it across every request in the batch, so a full batch costs much less than the same
requests sent one at a time — up to a point, as that chapter is careful to say. Work you let the
provider schedule is work they can use
to fill a batch that would otherwise run half empty, and the discount is what they pay you for
the flexibility.

| | Many concurrent calls | Batch endpoint |
|---|---|---|
| Finishes in | Minutes | Hours |
| Costs | Full price | Substantially less |
| Rate limits | Yours to manage | Theirs |
| Good for | Anything a person is waiting for | Anything overnight |

**The question to ask is whether anybody is waiting.** Re-processing an archive, generating
embeddings for a corpus, scoring last month's conversations — nobody is waiting, and paying
full price for speed you will not use is a decision somebody should make deliberately rather
than by default.

> **Note:** The discount, the turnaround time and even the existence of a batch endpoint are
> provider-specific and they move. The question — *is anybody waiting?* — does not.

## Idempotency

An operation is **idempotent** if doing it twice has the same effect as doing it once.

This matters here because of the retry section. When a call times out, you do not know whether
it arrived. Retrying a request that actually succeeded means paying twice; if the request did
something in the world, it means doing that thing twice.

Two defences, and you want both.

**An idempotency key.** You generate an identifier, send it with the request, and the provider
undertakes to return the first response rather than doing the work again if it sees the same
key. Generate it from the *content* — a hash of the document and the prompt — so that a retry
of the same work produces the same key and a different piece of work does not.

**A record of what you have done.** Before you act on a result, check whether you already have
one for this input. That is a dictionary, a file or a table, and it is the same thing as the
next section's.

One caution, because it bites immediately. A key is for a retry of a call you believe failed.
It is not for a *deliberate* re-run: if you send the same prompt five times on purpose — to see
how much the answers vary, which is the next chapter — a content-derived key may hand you the
first answer five times and tell you the model is perfectly consistent.

> **Warning:** The expensive case is not the doubled API bill. It is the pipeline step that
> sends an email, charges a card or writes a row — where a retry after a timeout does the
> thing twice and nothing in the model's world knows it happened. Chapter 4 said approval
> points belong in code; so does this.

## When It Dies Half-Way

The opening problem, and the last piece. Ten thousand documents, a failure at four thousand,
and no idea which four thousand.

**The fix is to write down what you have finished, as you finish it.** Not at the end — at the
end there is nothing to write, because you crashed. One line per completed item, flushed, in a
file you can read back.

```python
import json, pathlib

DOCS = [f"doc-{i:03d}" for i in range(10)]
DONE = pathlib.Path("done.jsonl")
FIXED = False                      # set to True for the second run

def already_done():
    if not DONE.exists():
        return set()
    with DONE.open() as f:
        return {json.loads(line)["doc"] for line in f}

def process(doc):
    if doc == "doc-004" and not FIXED:
        raise RuntimeError("the API fell over")
    return doc.upper()

def run():
    done = already_done()
    print(f"  starting with {len(done)} already done")
    with DONE.open("a") as f:
        for doc in DOCS:
            if doc in done:
                continue
            try:
                result = process(doc)
            except RuntimeError as e:
                print(f"  stopped at {doc}: {e}")
                return False
            f.write(json.dumps({"doc": doc, "result": result}) + "\n")
            f.flush()
    print("  all done")
    return True

run()
```

Run it once with `FIXED = False`:

```text
  starting with 0 already done
  stopped at doc-004: the API fell over
```

Then set `FIXED = True` — standing in for whatever you had to repair — and run it again,
without deleting `done.jsonl`:

```text
  starting with 4 already done
  all done
```

**Four things make that work**, and all four are easy to leave out.

**One line per item, appended.** Not a list held in memory and written at the end. A crash
loses memory and keeps the file.

**Flushed.** Be precise about what `f.flush()` buys, because the common version of this claim
is wrong. An ordinary exception loses nothing: the `with` block closes the file on the way out,
and closing flushes. What `flush()` protects you against is the process being *killed* — out of
memory, a container stopped, a `kill -9` — where nothing runs on the way out. And what you lose
then is not the last line or two: it is everything still sitting in the buffer, which is
thousands of bytes, so it can be a great many records. One word of code.

> **Note:** Flushing is still not durability. `flush()` hands the bytes to the operating
> system, not to the disk, so if the machine itself loses power they can go with it.
> `os.fsync(f.fileno())` is what waits for the disk, and it is slow enough that you would not do
> it per record without a reason — which is a real decision to make, not a detail.

**Keyed by input, not by position.** "I did the first four thousand" breaks the moment the
input list changes order. "I did these four thousand identifiers" does not.

**And the results are in it.** The file is both a record of what is done *and* the output. A
separate "progress" file that does not hold the answers means a crash costs you the answers
anyway.

> **Tip:** This file is also your idempotency record from the last section, and it is where
> you will look when somebody asks why document 7,214 is wrong. One file, three jobs. Build it
> on day one; it is twenty lines and it never stops being useful.

## When the Pipeline Has Stages

The last section does one job to many items. Real work is usually a pipeline: extract the text,
embed it, score it. That changes the question, because now a failure lands *between* stages, and
"I got to document four thousand" does not say which stage document four thousand got to.

**So the key is the pair, not the item.** One line per `(document, stage)`, and the resume
skips a step only if that document has been through that stage.

```python
import json, pathlib

DOCS = [f"doc-{i:03d}" for i in range(5)]
STAGES = ["extract", "embed", "score"]
LEDGER = pathlib.Path("stages.jsonl")
BROKEN = True                      # set to False for the second run

def done_steps():
    if not LEDGER.exists():
        return set()
    with LEDGER.open() as f:
        return {(r["doc"], r["stage"]) for r in map(json.loads, f)}

def work(doc, stage):
    if stage == "embed" and doc == "doc-002" and BROKEN:
        raise RuntimeError("the embedding API fell over")
    return f"{stage}:{doc}"

def run():
    done = done_steps()
    total = len(DOCS) * len(STAGES)
    print(f"  {len(done)} of {total} steps already done")
    with LEDGER.open("a") as f:
        for stage in STAGES:
            for doc in DOCS:
                if (doc, stage) in done:
                    continue
                try:
                    result = work(doc, stage)
                except RuntimeError as e:
                    print(f"  stopped at {stage} of {doc}: {e}")
                    return
                f.write(json.dumps({"doc": doc, "stage": stage,
                                    "result": result}) + "\n")
                f.flush()
    print(f"  all {total} steps done")

run()
```

Five documents, three stages, fifteen steps. The first run:

```text
  0 of 15 steps already done
  stopped at embed of doc-002: the embedding API fell over
```

Then `BROKEN = False`, and run it again:

```text
  7 of 15 steps already done
  all 15 steps done
```

**Seven is the number to look at.** Five extracts and two embeds had got through, and the second
run did not repeat one of them — which is the entire point, because extraction was the slow part.
A ledger keyed by document alone could not have expressed "extracted but not embedded".

**Stage at a time, or item at a time?** The program above finishes every document's extraction
before it starts embedding. The other order — each document all the way through before the next
one begins — is equally easy to write and behaves differently:

| | Stage at a time | Item at a time |
|---|---|---|
| First complete result | After the last stage | Early |
| A stage you can batch | Yes, all of it together | One at a time |
| A broken stage | Fails everything at once, visibly | Fails one item, then the next |
| Re-running one stage | Delete its lines, run again | Same, but interleaved with the rest |

Stage at a time for bulk work you are going to batch; item at a time when somebody is waiting
for the first answers, or when the items are independent enough that one bad document should not
stop the others.

**And now the part that is actually hard.** A stage that only computes is safe to retry. A stage
with an *external* effect — it sends the email, it writes the row, it charges the card — is not,
and a resume will do that effect twice unless you have done the work in the last section but one:
make the stage idempotent, key it by content, and write its ledger line *after* the effect has
landed rather than before.

> **Warning:** The failure mode here is quiet. A pipeline whose every stage only computes
> re-runs cleanly for a week and teaches you to trust the resume. Add a notification stage and
> the ledger looks no different, but a crash now costs a duplicate email for whatever was in
> flight — one, with the ledger line written after the effect, and every message in the batch if
> somebody writes it before. The day it is thousands is the day somebody re-runs the stage on
> purpose to fix something else.

**Keep each stage's output, not just a tick.** The ledger above stores `result` beside the pair,
which means a stage can be re-run on its own: change the scorer, delete the `score` lines, and
run again — the extracts and embeddings are still there. If the ledger held only "done", you
would have to start from the beginning to change the last step.

## Lab: Make a Fragile Script Robust

Four programs, all pure Python with nothing to install and no account anywhere. Forty minutes,
and there is a key for every step. Work in a new empty folder.

**Step 1.** Save the retry program from this chapter as `retry.py` and run it.

*Expected result:* exactly this, because the seed is fixed.

```text
failed 0 time(s) -> ok after waits []
failed 3 time(s) -> ok after waits [0.34, 0.78, 1.04]
```

**Step 2.** Make the call fail five times: change the last loop to `for fails in (0, 5)`. What
happens, and why is that right?

*Expected result:* the first line still prints, and then `RateLimited` comes out as an uncaught
traceback and the program exits 1. Five attempts means four retries, and the call is still
failing on the fifth, so the code gives up — which is what you want, because something that has
failed five times with growing waits is not going to succeed on the sixth. The alternative,
retrying forever, is a pipeline that never finishes and never tells you. In real code you would
catch it at the top and record which document it was.

**Step 3.** Remove the jitter — use `wait = backoff` instead of `random.uniform(0, backoff)`.
What breaks, and when would you notice?

*Expected result:* nothing breaks in this program, because there is only one caller. You would
notice with a thousand workers: they all failed at the same moment, so without jitter they all
wait the same 0.5 seconds and all retry at the same moment, and the provider sees the same
spike again. Jitter spreads them. **The defect is invisible at the scale you test at**, which
is the general shape of everything in this chapter.

**Step 4.** Save the concurrency program as `concur.py` and run it. Then change
`asyncio.Semaphore(at_once)` to `asyncio.Semaphore(20)`, leaving the loop alone, and say what
you have done.

*Expected result:* the first run gives about 2.0s, 0.5s and 0.1s. With the bound hard-coded to 20 it
no longer varies, so all three lines print about 0.1s — you have removed the bound while leaving
code that still looks as though it is there, which is how most unbounded pipelines come to
exist. Note that the `assert` keeps passing: ordering has nothing to do with the bound.

**Step 5.** Your provider allows 120 requests a minute. A call takes 2 seconds. How many
should you run at once?

*Expected result:* `\(120 / 60 = 2\)`{=latex} requests a second, and each occupies a worker for
2 seconds, so four at once keeps you at the limit. Go to 8 and you are asking for 240 a minute
and you will spend half your time in backoff. The formula is *rate × duration*, and it is worth
writing in a comment next to the number.

**Step 6.** Save the resume program as `resume.py` and run it. Then set `FIXED = True` and run
it again, without deleting `done.jsonl`.

*Expected result:* the two runs from the chapter — stopped at `doc-004` with none done, then
starting with four already done and finishing. Check `done.jsonl`: ten lines, each with its
document and its result.

**Step 7.** Delete the `f.flush()`, delete `done.jsonl`, and run both runs again. Does anything
change? Then make the process die without running anything on the way out: set `FIXED = True`,
delete `done.jsonl`, `import os`, and put `os.kill(os.getpid(), 9)` as the last line inside the
`with` block, after the loop. Count the lines in `done.jsonl` — once with the flush, once
without.

*Expected result:* deleting the flush changes nothing in the ordinary runs, because the `with`
block closes the file on the way out and closing flushes — an exception is not what `flush`
protects you from. Under `kill -9` the difference is total: with the flush you keep every line
written so far, and without it you can lose all of them, because the buffer is thousands of
bytes and ten short records never fill it. That is why the bug survives into production: the
only thing that exposes it is the one event you do not test. Put the flush back.

**Step 8.** You are processing 10,000 documents. Your code streams each response, validates it
as JSON, and writes a progress file with the index of the last document completed. Name three
things wrong with that.

*Expected result:* streaming saves no time here, because the answer has to be valid JSON as a
whole and you cannot check that until it has all arrived. All it buys is the chance to give up
early on an answer that is already malformed. The progress file holds an index
rather than identifiers, so it breaks if the input list is ever reordered or filtered. And it
holds no results, so a crash at document 9,000 means you know where you were and have lost the
answers. There are two more if you spotted them: nothing said anything about a bound on
concurrency, and nothing said what happens when one document fails.

**Step 9.** Save the stages program as `stages.py`. Run it, set `BROKEN = False`, run it again.
Then answer this: why is seven the interesting number, and what would break if the ledger were
keyed by document alone?

*Expected result:* `0 of 15` and then `stopped at embed of doc-002`; on the second run,
`7 of 15 steps already done` and `all 15 steps done`. Seven is five extractions plus two
embeddings — work the resume
did not repeat. Keyed by document alone the ledger could only say "doc-000: done", which is
false (it has been extracted and embedded but not scored) or useless (it is not finished, so
redo all three stages). The pair is what makes a partial document expressible.

**Step 10.** In `concur.py`, make `fetch` raise on one document: put the line
`if doc == 7: raise RuntimeError("boom")` before the sleep, and run it. Then add
`return_exceptions=True` to the `gather` call and run it again.

*Expected result:* first the whole program dies with that `RuntimeError` and prints no timing
line at all — not even for the documents that had already finished before doc 7 ran, whose
results are simply gone. The `assert` never even runs. With `return_exceptions=True` the call
returns, and the `assert` fails instead, because `results[7]` is a `RuntimeError` object rather
than `"done 7"`. Both failures teach something: the first throws away good work, and the second
shows you that dealing with the exception objects is now *your* job.

## Summary, Key Terms, and Review Questions

### Summary

A streaming response is **server-sent events** carrying **deltas** your code appends, and it
buys a shorter wait before the first word — but **you cannot stream a response you must
validate as a whole**, because the check needs all of it, so stream when the consumer can use a
piece and not when it needs the whole; a sequence of independent units is the case where it
works. Streaming also gives you a cancellation point, which is the saving people forget to
build. **429** means too fast and is not an error in your code; it is retryable, as are 500s
and timeouts, while a malformed request, a bad key, an over-length request and a 429 raised by
an exhausted quota are not, so read the error's body and not only its status. Retry with
**exponential backoff** so you stop hammering a struggling system, and **jitter** so your
workers do not retry in step; five attempts make four waits. Every call wants three timeouts —
connect, read between chunks, and a **total** derived from the token cap, which is the only one
that caps a long generation. `asyncio` lets calls wait at the same time, and a **semaphore**
bounds how many: without it, `gather` over ten thousand documents opens ten thousand
connections and every one comes back 429. But a semaphore bounds concurrency, not rate, so
leave a margin or use a **token bucket**; and `gather` throws away every good result when one
job raises, unless you pass `return_exceptions=True`. A **batch endpoint** is slower and
substantially cheaper, and the question it turns on is whether anybody is waiting.
**Idempotency** matters because a timed-out call may have succeeded: use a content-derived key,
keep a record, and do not let that key defeat a re-run you meant. And write down what you have
finished as you finish it — one flushed line per item for one job over many items, one per
`(item, stage)` for a pipeline, keyed by input and holding the results.

### Key Terms

| Term | Meaning |
|---|---|
| **Server-sent events** | A long-lived HTTP response carrying one small event per line as the server produces them. How a streamed reply arrives |
| **Delta** | One streamed piece: what to add to what you have, not the whole answer again |
| **429** | *Too many requests.* The provider's rate limit, on requests per minute and on tokens per minute. Retryable when you are going too fast; the same status comes back when the account is out of credit, which no wait fixes |
| **Exponential backoff** | Doubling the wait after each failed attempt, up to a cap, so a struggling system is not hammered |
| **Jitter** | Waiting a random amount up to the backoff rather than exactly it, so many workers do not retry in step |
| **Total timeout** | The cap on a whole call, as distinct from the gap between chunks that most libraries call the read timeout. Derived from the token cap |
| **Semaphore** | A counter that bounds how many jobs run at once. Three words of code, and the difference between concurrency and attacking your own account |
| **Token bucket** | A limiter on the *rate* rather than on how many run at once, for when the requests-per-minute limit is the one that hurts |
| **Batch endpoint** | Upload requests, collect results hours later, pay substantially less. For work nobody is waiting on |
| **Idempotency** | Doing an operation twice has the same effect as doing it once. What makes a retry after a timeout safe |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Backoff with jitter | `wait = random.uniform(0, min(cap, base * 2 ** attempt))` |
| Attempts and waits | *n* attempts make *n* − 1 waits. Five attempts at base 0.5 is 7.5 s at worst |
| How many at once | rate × duration — 120 a minute at 2 seconds each is 4. It bounds concurrency, not rate, so leave a margin |
| Timeouts | Three: connect, read between chunks, total. Derive the *total* from the token cap |
| Retryable | 429, 5xx, timeouts. *Not* a malformed request, a bad key, an over-length one, or a 429 from an exhausted quota |
| What to stream | To a person, yes. One answer you must validate whole, no. Independent units, yes |
| `asyncio.gather` | One failure loses every result unless you pass `return_exceptions=True` |
| The resume file | One flushed line per item, or per `(item, stage)` for a pipeline. Keyed by input, holding the result |

### Review Questions

1. Your script works on ten documents and dies on a 429 at document four thousand of ten thousand. What do you do?
2. Why can you not stream a response that you have to validate?
3. What is idempotency, and where does it matter in a pipeline like this?
4. Why is jitter necessary when backoff alone seems to solve the problem?
5. Your provider allows 300 requests a minute and a call takes 4 seconds. How many do you run at once, and how did you get that?
6. When would you use a batch endpoint instead of running many calls yourself?
7. A multi-step pipeline fails half way. How do you resume it?

### Review Answers

1. Four things, and the order matters. First, make the failure survivable: write one flushed
line per completed document, keyed by the document's identifier and holding its result, so a
crash costs you one document rather than four thousand. Second, stop causing the 429: bound the
concurrency with a semaphore set from the provider's limit — rate times duration — rather than
letting `gather` open as many connections as it likes, and pass `return_exceptions=True` so one
failure does not discard the rest. Third, retry what is retryable with exponential backoff and
jitter, and do not retry a malformed request at all. Fourth, give every call a total timeout
derived from the token cap, so one stuck connection cannot hold a worker for ever. Then re-run
it; it starts from where it stopped.
2. Because the check only makes sense over the whole answer — that it parses, that it has the
fields you need, that it says something permissible — and you cannot run it until the whole
answer has arrived. Once it has, you have waited for the entire generation, which is what
streaming was supposed to avoid, so you have taken on a more complicated code path and saved no
time by it. Worse, if you streamed it to a user as well, you have already shown them the answer
you are about to reject. The edge is worth giving too, because it shows why the rule holds: if
the output is a sequence of independent units, each one is whole as it lands, so you can
validate and act on them one at a time and streaming is fine.
3. An operation is idempotent if doing it twice has the same effect as doing it once. It
matters because a timed-out call may well have succeeded — you have no way to tell — so every
retry risks doing the work twice. For a model call that means paying twice. For a pipeline step
that sends an email, charges a card or writes a row, it means doing that thing twice. The
defences are an idempotency key derived from the content, so the same work produces the same
key, and a record of what you have already done, checked before you act. The thing to add
unprompted is that the key is for a retry of a call you think failed, not for a re-run you
meant: send the same prompt five times on purpose under a content key and you may get the first
answer five times.
4. Because backoff alone is a *per-worker* fix and the problem is usually *across* workers. A
thousand callers that all failed at the same moment will all wait the same half second and all
retry at the same moment, so the provider sees the same spike it rejected, and the cycle
repeats with longer gaps. Jitter spreads the retries over the interval instead. The reason it
is easy to leave out is that it makes no difference at all with one caller, which is the scale
you test at.
5. Twenty at once, or sixteen with a margin. The arithmetic is rate times duration:
`\(300/60 = 5\)`{=latex} requests a second, each occupying a worker for 4 seconds, so
`\(5 \times 4 = 20\)`{=latex} in flight holds you at the limit. The margin is the part worth
saying out loud: a semaphore bounds concurrency, not rate, so twenty in flight only produces
300 a minute while calls really take 4 seconds. Sixteen buys you a fifth of headroom for being
a little wrong about that. It does not buy you much more than that, and it is worth saying so:
if a burst of calls comes back in 2 seconds, sixteen in flight is 480 a minute and you are over
anyway. No concurrency bound fixes that, because the quantity it bounds is not the quantity the
provider limits. A token bucket does.
6. When nobody is waiting. Re-processing an archive, embedding a corpus, scoring last month's
conversations — work that has to be done by tomorrow rather than in the next minute. The batch
endpoint takes hours instead of minutes and costs substantially less, because work the provider
can schedule is work they can use to fill a batch that would otherwise run half empty. Paying
full price for speed nobody will use should be a decision somebody made, not the default that
happened because the synchronous call was the one in the example.
7. Key the record by the pair, not the item: one line per `(item, stage)`, so the resume skips
a step only when that item has been through that stage. A ledger keyed by the item alone cannot
express "extracted and embedded but not scored", which is exactly the state a half-way failure
leaves. Store each stage's output beside the pair, not just a tick, so a later stage can be
re-run on its own without redoing the earlier ones. Then say the hard part before you are
asked: a stage that only computes is safe to repeat, but a stage with an external effect — it
sends the email, it charges the card — is not, so it needs the idempotency work, and its ledger
line must be written after the effect has landed rather than before. Decide also whether to run
a stage at a time, which batches well and fails visibly, or an item at a time, which gets the
first complete results out early.

> **You understand this when** you can take a script that calls a model in a loop and name
> the four things it needs before it can be run on ten thousand inputs.
