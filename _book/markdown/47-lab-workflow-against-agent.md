# Lab: Workflow Against Agent

Chapter 34 gave a rule for when an agent is warranted and an order to try designs in. Chapter 38
gave the way to measure one. This chapter puts them together on the smallest honest experiment
there is: **one step, built twice, measured the same way.** The step is the one chapter 46 left
uncovered — answering a question whose answer needs two documents — and the two builds are chapter
45's pipeline and chapter 4's loop. It ends with three builds rather than two, and the third one
is the chapter: the first two differed in a second way I had argued myself into, and a comparison
between arms that differ in two ways answers neither question.

*The problem.* Everyone has an opinion about agents. I want numbers from my own system.

*The question.* On one step of my own system, what does the loop buy over the path my code
controls — and what does it cost?

**Why this step.** Chapter 46's error analysis produced six failure modes and closed one of them
with three code checks. The mode it could not touch was *Answers for one case when two apply* —
four failures, the mode the first forty answers called largest, and a row in the needs table with
no code check and no judge behind it. An agent is the obvious thing to reach for, because the
obvious diagnosis is that one retrieval cannot see both halves. **This chapter is that hunch,
measured.**

**What this lab does not do.** It names no new pattern, and it re-teaches none of the measures it
runs on: chapter 34 owns the five fixed paths and the four-column rule, chapter 4 owns the agent,
the step, the stopping condition and compounding error, chapter 38 owns the task, the grader, the
final state, the transcript, pass@k and pass\^k, and chapter 20 owns the interval. It does name
**two figures of its own**, in Key Terms, and both are arithmetic on those measures rather than
new ones: what a success costs, and how often a loop took the cheapest path open to it. It does not evaluate a multi-agent arrangement
(chapter 37) or build a second judge (chapters 31 and 46). It grades the final answer and [**not
the transcript**]{.noindex}, which is chapter 38's second object and a decision this chapter makes
explicitly rather than by omission — step 4 says what that costs. It is not a cost model (chapter
53) and it reduces nothing (chapter 49): the tokens and the seconds here are a measurement of two
designs and not a bill.

**What you need.** Chapter 46's folder, which already holds chapter 45's pipeline. Copy it:

```text
  cp -r ~/sandbox/ch46 ~/sandbox/ch47 && cd ~/sandbox/ch47
```

That brings `corpus/`, `parse.py`, `index.py`, `search.py`, `key.py` and `answer.py` with it, and
none of them is edited. Set `OPENAI_API_KEY`. Five new programs, in order:

| Save as | What it does | Imports |
|---|---|---|
| `tasks.py` | twelve tasks needing two documents each, and a code grader | nothing |
| `designs.py` | the same step as a fixed path and as two loops | `answer`, `search`, `tasks` |
| `run.py` | every design over every task, three trials each | `search`, `designs`, `tasks` |
| `read.py` | six readings of the runs | `designs`, `run`, `tasks` |
| `why.py` | three counts that say why the loops lost | `search`, `designs`, `read`, `run`, `tasks` |

> **Note:** What this costs. 108 runs: 36 of the fixed path at one chat call each, and 72 of the
> two loops at as many as seven. That came to 189 chat calls and 117 embeddings, which is a few
> pence on a small model. Only the first of those three numbers could be written down in advance,
> and that is the point of the chapter: the fixed path's bill is 36 times a known number, and a
> loop's is not knowable until it has run. The lab as first built was 72 runs and 115 chat calls;
> the third design is why those figures are not the ones above.

> **Note:** The `text` blocks are one real run on 30 October 2026. Chapter 45's warning applies:
> your figures will differ. **What is stable is the shape** — a fixed path that is cheap and
> predictable, a loop that costs more per answer that passes, and a difference in success that the
> interval has something to say about. **What moves is which individual task lands where**, and
> with twelve tasks and three trials a single task changing its mind moves the headline by three
> points.

## Step 1: Twelve Tasks the Fixed Path Should Find Hard

Chapter 38's unit is a [**task**]{.noindex}: a starting state, a goal, and a condition checkable when the run
ends. Here the starting state is the corpus, the goal is an answer, and the condition is a code
grader — which is chapter 31's rule, because the thing being compared is whether two literal
values appear.

```python
"""Twelve tasks whose answers need two documents, and a code grader.

Chapter 46 ended with a mode it could not check: *Answers for one case
when two apply*, four failures, the mode the first forty called
largest, and a row in the needs table with no code check and no judge
behind it. These twelve tasks are that mode's territory on purpose.
Every question needs a value from one document and a value from
another, so an answer that takes one and stops is wrong in a way a
program can see.

`needs` is a list of REQUIREMENTS, and each requirement is a set of
phrasings that satisfy it. The answer passes when it contains at least
one phrasing from every requirement. That is chapter 41's exact-match
grader with two changes it names itself: the match is containment
rather than equality, because these answers are sentences, and the
normalisation is declared as a set of alternatives rather than hidden
in a regular expression.

`docs` names the documents the two values live in. The assertion at the
bottom is chapter 41's: a requirement no document satisfies is a task
about nothing, and this is the cheapest moment to find out.
"""
import os
import pathlib
import re
import sys

CORPUS = pathlib.Path(os.environ.get("CORPUS", "corpus")) / "docs"

#  question, the two requirements, the documents they live in
TASKS = [
 ("What does standard delivery cost on a 20 pound order going to an "
  "IV postcode?",
  [{"3.99"}, {"9.50"}],
  ("delivery-fees", "delivery-exceptions")),
 ("How long do I have to return a standard item, and how long for a "
  "clearance item?",
  [{"30 days", "thirty days"}, {"14 days", "fourteen days"}],
  ("returns-standard", "returns-clearance")),
 ("Your refunds policy and your refunds FAQ give different numbers "
  "for how long a refund takes. What are both of them?",
  [{"14 days", "fourteen days"}, {"30 days", "thirty days"}],
  ("refunds-policy", "refunds-faq")),
 ("What is the Northern Ireland surcharge, and what does named-day "
  "delivery cost?",
  [{"6.50"}, {"5.99"}],
  ("delivery-exceptions", "delivery-fees")),
 ("What does next-day delivery cost, and who delivers a next-day "
  "parcel?",
  [{"7.99"}, {"carrick express"}],
  ("delivery-fees", "shipping-partners")),
 ("How many years of warranty does Harbour Plus give, and how many "
  "years does an item carry without it?",
  [{"three years", "3 years"}, {"two-year", "two years", "2 years"}],
  ("plan-harbour-plus", "warranty-summary")),
 ("What does Harbour Plus cost a year, and what does next-day "
  "delivery cost?",
  [{"29"}, {"7.99"}],
  ("plan-harbour-plus", "delivery-fees")),
 ("How long do I have to return a clearance item, and how long is a "
  "return postage label valid for?",
  [{"14 days", "fourteen days"}, {"21 days", "twenty-one days"}],
  ("returns-clearance", "return-postage-labels")),
 ("How long is a repair covered for, and how long does a stage-two "
  "complaint take to answer?",
  [{"ninety days", "90 days"}, {"ten working days", "10 working days"}],
  ("warranty-full", "complaints-process")),
 ("What is the most you will pay as goodwill per order, and what is "
  "the standard delivery charge on an order under 40 pounds?",
  [{"20 pounds", "20 per order"}, {"3.99"}],
  ("refunds-policy", "delivery-fees")),
 ("How long do I have to report a missing item, and how long to "
  "report cosmetic damage?",
  [{"14 days", "fourteen days"}, {"48 hours", "forty-eight hours"}],
  ("missing-item-in-a-parcel", "damaged-on-arrival")),
 ("How wide are the toaster's slots, and what is the kettle's "
  "capacity in litres?",
  [{"34 mm", "34mm", "34 millimetres"}, {"1.7"}],
  ("product-toaster-hl-2209", "product-kettle-hl-2208")),
]


#  Units a quantity can be written against, with the singular that a
#  hyphenated form uses. `variants` turns one phrasing into the three
#  a model actually writes, so a requirement is declared once.
UNITS = {"days": "day", "years": "year", "hours": "hour",
         "pounds": "pound", "working days": "working day"}


def norm(s):
    """The declared normalisation: case, whitespace, markdown emphasis
    and the pound sign. No more than that, so a reader can predict
    every verdict from the phrasing sets above. `str` because a model
    asked for a string sometimes returns an object."""
    s = str(s).lower().replace("*", "").replace("`", "").replace("£", "")
    return re.sub(r"\s+", " ", s).strip()


def variants(phrase):
    """One phrasing, every form of it a model writes. `30 days` also
    accepts `30-day` and `30 day`, because *a 30-day window* is the
    same claim. This is the repair step 4 earned, and it is written as
    a RULE rather than as a list: chapter 41's lesson is that a
    hand-written normaliser is a pile of special cases until somebody
    makes it a rule, and a quantity with a unit is the rule here."""
    out = {phrase}
    for plural, singular in UNITS.items():
        tail = " " + plural
        if phrase.endswith(tail):
            head = phrase[: -len(tail)]
            out |= {f"{head}-{singular}", f"{head} {singular}"}
    return out


def met(answer, requirement):
    a = norm(answer)
    return any(norm(v) in a
               for p in requirement for v in variants(p))


def grade(answer, needs):
    """Pass when every requirement is met. The grader returns the
    per-requirement verdicts too, because 'half right' is this
    chapter's subject and a single boolean hides it."""
    hits = [met(answer, r) for r in needs]
    return all(hits), hits


def cases():
    return [(f"t{i:02d}", q, needs, docs)
            for i, (q, needs, docs) in enumerate(TASKS, 1)]


if __name__ == "__main__":
    bad = []
    for tid, q, needs, docs in cases():
        body = " ".join((CORPUS / f"{d}.md").read_text() for d in docs)
        whole = " ".join(p.read_text() for p in sorted(CORPUS.glob("*.md")))
        for j, r in enumerate(needs, 1):
            if not met(body, r):
                bad.append((tid, j, r, "not in its own documents"))
            elif met(whole.replace(body, ""), r):
                pass  # satisfiable elsewhere too; not an error
        # and the point of the set: neither document alone is enough
        for d in docs:
            one = (CORPUS / f"{d}.md").read_text()
            if all(met(one, r) for r in needs):
                bad.append((tid, 0, d, "one document answers it all"))

    print(f"  {len(cases())} tasks, each needing two documents")
    print(f"  {len({d for _, _, _, ds in cases() for d in ds})}"
          f" documents between them\n")
    if bad:
        print(f"  {len(bad)} problem(s):")
        for tid, j, r, why in bad:
            print(f"    {tid} requirement {j}: {why}  {r}")
        sys.exit(1)
    print("  every requirement is satisfied by its own two documents")
    print("  and by NEITHER of them alone, which is what makes these")
    print("  tasks about two documents rather than about one\n")

    print("  the grader on three answers to task 1, to show what it")
    print("  counts:\n")
    q, needs = TASKS[0][0], TASKS[0][1]
    for a in ("Standard delivery is 3.99 pounds on orders under 40.",
              "The surcharge for IV postcodes is 9.50 pounds.",
              "3.99 plus a 9.50 surcharge, so 13.49."):
        ok, hits = grade(a, needs)
        marks = "".join("y" if h else "-" for h in hits)
        print(f"    [{marks}] {'PASS' if ok else 'FAIL'}  {a[:46]}")
    print("\n  Half an answer fails, which is the whole point of the")
    print("  set. Chapter 46's mode was answers that take one of two")
    print("  cases and stop; a grader that accepted either value")
    print("  would score those as passes and measure nothing.")
```

```text
  12 tasks, each needing two documents
  16 documents between them

  every requirement is satisfied by its own two documents
  and by NEITHER of them alone, which is what makes these
  tasks about two documents rather than about one

  the grader on three answers to task 1, to show what it
  counts:

    [y-] FAIL  Standard delivery is 3.99 pounds on orders und
    [-y] FAIL  The surcharge for IV postcodes is 9.50 pounds.
    [yy] PASS  3.99 plus a 9.50 surcharge, so 13.49.

  Half an answer fails, which is the whole point of the
  set. Chapter 46's mode was answers that take one of two
  cases and stop; a grader that accepted either value
  would score those as passes and measure nothing.
```

**Every task needs two documents, and the assertion is what makes that a fact rather than an
intention.** It checks two things per task: that both requirements are satisfied by the two
documents named, and that **neither document alone satisfies both**. The second half is the one
that matters, and it failed five times while this set was being written — a surcharge and a
transit time that both live in the delivery exceptions, a goodwill cap and a transfer window that
are two sections of one refunds policy. Each of those would have been a task about one document
wearing a two-part question, and the comparison would have measured nothing.

**The grader is chapter 41's exact-match grader with two changes it names itself.** The match is
containment rather than equality, because these answers are sentences. And the normalisation is a
declared set of phrasings per requirement — `{"30 days", "thirty days"}` — rather than a regular
expression nobody can predict. Chapter 41's lesson was that a score is a measurement of its
normaliser as much as of the model, so the normaliser is written where it can be read.

**And the three worked answers at the end are the whole reason the set exists.** Half an answer
fails. An answer giving 3.99 and stopping fails; an answer giving 9.50 and stopping fails. **A
grader that accepted either value would score chapter 46's entire mode as passing and measure
nothing at all.**

**What this grader is, and is not.** It is an evaluation grader with a key: *I* wrote the two
requirements per task, by reading the documents. Chapter 46's needs table put that mode's check
under judgement and named the hard part — *deciding how many cases a question has* — and nothing
here decides that. **So the gap chapter 46 left is not closed by this chapter**; what this
chapter has is a measurement of the mode on a set where somebody has already done the deciding,
which is enough to compare two designs and not enough to ship.

> **Tip:** Write the `docs` column while you write the question, and let the assertion tell you
> whether you have a two-document task. The five it caught here all looked right: in each case I
> had two values in mind and had not checked they were in two files. A question with two parts is
> not the same thing as a task needing two sources, and only the corpus can tell you which you
> have.
## Step 2: The Same Step, Built Twice

Chapter 34's first section is a table of six designs and what selects the next step in each. The
two ends of that table are the two builds here. **The fixed path is chapter 45's pipeline
unchanged**: one dense retrieval, fill a 2,500-character budget by rank and stop, one answer call.
**The agent is chapter 4's loop**: one tool, and a model that decides what to search for, how many
times, and when it has enough.

```python
"""One step, built three ways.

The step is answering a question whose answer needs two documents.

FIXED is chapter 45's pipeline unchanged: one dense retrieval over the
176 chunks, fill a 2,500-character budget by rank and stop, one answer
call. Chapter 34's table calls this a single call with retrieval in
front of it, and its call count is known before you run it: one
embedding and one chat, every time, for every question.

AGENT is chapter 4's loop. The model is given one tool - search - and
decides what to search for, how many times, and when it has enough. Its
call count is not known in advance, which is the whole of what chapter
34's last column is about.

The three stopping conditions are chapter 4's and all three are here:
the model saying it is done (it returns an answer), a step limit, and
your code refusing (a reply that is neither a search nor an answer).

WIDE is the agent again at the fixed path's per-search budget, and it
exists because the first version of this lab did not have it. AGENT
was built with the smaller 1,200-character budget on the reasoning
that a loop accumulates several searches' worth and so sees more in
total - so a loop seeing more was not an unfair advantage, it was the
advantage being measured.

That reasoning was a prediction about behaviour, and the behaviour was
the thing under measurement. On 29 of AGENT's 36 runs it searched
once, so the smaller budget bought it nothing to trade: it was a
handicap, and a handicap is a second difference between two arms.

So WIDE removes it. Same loop, same tool, same instruction, same step
limit, the fixed path's budget. Three arms make the two questions
separable - FIXED against WIDE is the design, AGENT against WIDE is
the budget - and neither question can be asked of two arms that
differ in two ways.
"""
import json
import time

import answer
import search

MODEL = answer.MODEL
FIXED_BUDGET = 2500
STEP_BUDGET = 1200
STEP_LIMIT = 6

#  Chapter 18's rule is to change one thing, so that a difference can
#  be attributed. Here the one thing is the DESIGN, which means the two
#  instructions have to say the same thing about the task and differ
#  only in the mechanics they cannot share. TASK below is that shared
#  sentence, word for word in both.
#
#  What cannot be equalised: a design with a tool has to be told it has
#  one. That residue is named rather than hidden, and it is why the
#  agent's instruction is the longer of the two by the length of a
#  protocol.
TASK = (
    "The question may have more than one part. Answer every part, and "
    "answer only from passages you have been given."
)

FIXED_INSTRUCTION = (
    f"{TASK}\n\n"
    "Reply as JSON: {\"answer\": \"...\"}"
)

AGENT_INSTRUCTION = (
    f"{TASK}\n\n"
    "Reply with JSON, exactly one of:\n"
    "  {\"search\": \"<query>\"}   to search the documents\n"
    "  {\"answer\": \"<text>\"}    when you can answer\n\n"
    "Each search returns the passages that best match your query. You "
    "may search more than once."
)
assert TASK in FIXED_INSTRUCTION and TASK in AGENT_INSTRUCTION


def retrieve(query, cache, budget):
    """The same retrieval for every design: chapter 45's dense ranking,
    filled by rank and stopped, which is chapter 28's greedy-fill
    warning obeyed."""
    order, _ = search.dense(query, cache)
    kept, left = [], budget
    for cid in order:
        block = f"[{cid}] {search.BY_ID[cid]['text']}\n"
        if len(block) > left:
            break
        kept.append(cid)
        left -= len(block)
    return kept


def passages(kept):
    return "\n".join(f"[{c}] {search.BY_ID[c]['text']}" for c in kept)


def _chat(messages, max_tokens):
    import os
    import urllib.request
    body = json.dumps({
        "model": MODEL, "messages": messages,
        "response_format": {"type": "json_object"},
        "max_tokens": max_tokens, "temperature": 0,
    }).encode()
    req = urllib.request.Request(answer.URL, body, {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=answer.TIMEOUT) as r:
        return json.load(r)


def as_text(v):
    """A model asked for {"answer": "..."} sometimes returns
    {"answer": {"part1": ..., "part2": ...}}, which is valid JSON and
    not the shape asked for. The request sets JSON mode, so what the
    engine compiled is *this is JSON* and nothing about the type of
    that field - which is chapter 22's own list of what a guaranteed
    format never buys: the parts of your schema the engine did not
    compile. Chapter 21 supplies the rule that follows from it, that
    a program never trusts prose. This is the cheap half of both:
    serialise what came back rather than crash on it, and count it as
    the answer it is."""
    return v if isinstance(v, str) else json.dumps(v, sort_keys=True)


def reply_of(d):
    raw = d["choices"][0]["message"]["content"]
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError:
        return {}, raw


def fixed(question, cache):
    """One retrieval, one answer. Two calls, always."""
    t0 = time.monotonic()
    kept = retrieve(question, cache, FIXED_BUDGET)
    prompt = (f"{FIXED_INSTRUCTION}\n\nPassages:\n{passages(kept)}\n\n"
              f"Question: {question}")
    d = _chat([{"role": "user", "content": prompt}], 400)
    got, raw = reply_of(d)
    return {
        "design": "fixed",
        "budget": FIXED_BUDGET,
        "answer": as_text(got.get("answer", raw)),
        "steps": 1,
        "searches": 1,
        "queries": [question],
        "passages": kept,
        "prompt_tokens": d["usage"]["prompt_tokens"],
        "output_tokens": d["usage"]["completion_tokens"],
        "chat_calls": 1,
        "seconds": round(time.monotonic() - t0, 2),
        "ended": "answered",
        "model": d["model"],
    }


def agent(question, cache, budget=STEP_BUDGET, name="agent"):
    """The loop. Your code runs every step; the model picks each one."""
    t0 = time.monotonic()
    messages = [{"role": "user",
                 "content": f"{AGENT_INSTRUCTION}\n\nQuestion: {question}"}]
    tin = tout = chats = 0
    queries, seen, ended, text = [], [], None, ""
    for step in range(1, STEP_LIMIT + 1):
        d = _chat(messages, 400)
        chats += 1
        tin += d["usage"]["prompt_tokens"]
        tout += d["usage"]["completion_tokens"]
        got, raw = reply_of(d)
        messages.append({"role": "assistant", "content": raw})
        if "answer" in got:
            text, ended = as_text(got["answer"]), "answered"
            break
        if "search" in got:
            q = str(got["search"])
            queries.append(q)
            kept = retrieve(q, cache, budget)
            seen += [c for c in kept if c not in seen]
            messages.append({"role": "user",
                             "content": f"Passages:\n{passages(kept)}"})
            continue
        # Chapter 4's third stopping condition: your code refuses.
        ended, text = "refused", as_text(raw)
        break
    else:
        ended, text = "step limit", text
    return {
        "design": name,
        "budget": budget,
        "answer": text,
        "steps": chats,
        "searches": len(queries),
        "queries": queries,
        "passages": seen,
        "prompt_tokens": tin,
        "output_tokens": tout,
        "chat_calls": chats,
        "seconds": round(time.monotonic() - t0, 2),
        "ended": ended,
        "model": MODEL,
    }


def wide(question, cache):
    """The same loop at the fixed path's per-search budget.

    AGENT with one line changed. Read the module docstring for why it
    is here: without it, the design and the budget cannot be told
    apart.
    """
    return agent(question, cache, budget=FIXED_BUDGET, name="wide")


DESIGNS = {"fixed": fixed, "agent": agent, "wide": wide}

if __name__ == "__main__":
    from tasks import cases, grade
    cache = search.vectors()
    tid, q, needs, docs = cases()[0]
    print(f"  one task, {len(DESIGNS)} designs. {tid}:")
    print(answer.wrap(q, "    ", "    ", 60))
    print()
    for name, fn in DESIGNS.items():
        r = fn(q, cache)
        print(f"  {name}")
        print(f"    chat calls   {r['chat_calls']}")
        print(f"    searches     {r['searches']}")
        for s in r["queries"]:
            print(answer.wrap(f'"{s}"', "               ",
                              "               ", 58))
        print(f"    passages     {len(r['passages'])}")
        print(f"    tokens       {r['prompt_tokens']} in,"
              f" {r['output_tokens']} out")
        print(f"    seconds      {r['seconds']}")
        print(f"    ended        {r['ended']}")
        print(answer.wrap(r["answer"], "    answer       ",
                          "                 ", 60))
        #  The grade, from the same grader step 3 uses. One run of one
        #  task is not evidence about a design, and printing the
        #  verdict here is what makes that visible rather than
        #  assumed: whichever design wins this line, the next program
        #  is the one that can say anything.
        ok, hits = grade(r["answer"], needs)
        got = sum(hits)
        print(f"    graded       {'passed' if ok else 'FAILED'}"
              f" - {got} of {len(needs)} requirement(s)")
        print()
    print("  The fixed path made one search because that is what its")
    print("  code does. What either loop did on one question is a")
    print("  measurement and not a property of the design, which is")
    print(f"  why the next program runs all {len(DESIGNS)} twelve times over.")
    print("  Read the graded lines above and then disbelieve them:")
    print("  one run of one task is one of chapter 20's trials, and a")
    print("  single trial is the thing chapter 38 says never to")
    print("  report.")
```

```text
  one task, 3 designs. t01:
    What does standard delivery cost on a 20 pound order
    going to an IV postcode?

  fixed
    chat calls   1
    searches     1
               "What does standard delivery cost on a 20
               pound order going to an IV postcode?"
    passages     5
    tokens       646 in, 40 out
    seconds      5.36
    ended        answered
    answer       The standard delivery cost on a 20 pound
                 order going to an IV postcode is 9.50
                 pounds, as it falls under the surcharge
                 for the Scottish Highlands and islands.
    graded       FAILED - 1 of 2 requirement(s)

  agent
    chat calls   2
    searches     1
               "standard delivery cost 20 pound order IV
               postcode"
    passages     3
    tokens       469 in, 67 out
    seconds      6.63
    ended        answered
    answer       The standard delivery cost on a 20 pound
                 order going to an IV postcode is 13.49
                 pounds, which includes the standard
                 delivery fee of 3.99 pounds plus a
                 surcharge of 9.50 pounds for the IV
                 postcode.
    graded       passed - 2 of 2 requirement(s)

  wide
    chat calls   2
    searches     1
               "standard delivery cost 20 pound order IV
               postcode"
    passages     7
    tokens       866 in, 81 out
    seconds      3.83
    ended        answered
    answer       The standard delivery cost on a 20 pound
                 order going to an IV postcode is 3.99
                 pounds, but there is an additional
                 surcharge of 9.50 pounds for that
                 postcode. Therefore, the total cost would
                 be 3.99 pounds + 9.50 pounds = 13.49
                 pounds.
    graded       passed - 2 of 2 requirement(s)

  The fixed path made one search because that is what its
  code does. What either loop did on one question is a
  measurement and not a property of the design, which is
  why the next program runs all 3 twelve times over.
  Read the graded lines above and then disbelieve them:
  one run of one task is one of chapter 20's trials, and a
  single trial is the thing chapter 38 says never to
  report.
```

> **Warning:** Read the three graded lines and then distrust them. On this one run the fixed path
> failed and both loops passed — the reverse of what twelve tasks and three trials say, where the
> fixed path passes 33 of 36 runs and the agent 17. **A single run of a single task is one of
> chapter 20's trials, and one trial is the figure chapter 38 says never to report.** It is printed
> here because the alternative is worse: a walkthrough that quietly shows the design the chapter
> goes on to prefer giving the better answer would be reporting a trial and calling it a
> demonstration. This is what one trial is worth, and the rest of the chapter is why.

**Chapter 18's rule is to change one thing, and the one thing here has to be the design.** So the
two instructions share their task sentence word for word — *the question may have more than one
part, answer every part, and answer only from passages you have been given* — and differ only in
the mechanics. **What cannot be equalised is named in the program rather than hidden**: a design
with a tool has to be told it has one, so the agent's instruction is longer by the length of a
protocol. That residue is the floor on how clean this comparison can be, and it is worth saying
out loud, because a comparison between an agent and a workflow where the agent also got better
instructions is the commonest version of this experiment and it measures the instructions.

**The second difference is the one that turned out to matter, and the first version of this lab
got it wrong.** The fixed path sees one 2,500-character context. The agent was built to see 1,200
characters per search, on the reasoning that a loop accumulates several searches' worth and so
sees more in total. The step limit is six chat calls, so a run that ends by answering can search
at most five times.

**That reasoning assumed the loop would search more than once, and it is an assumption rather
than a design property.** It mostly did not, which made the smaller budget a handicap and not a
trade — and a handicap is a confound in a comparison of designs. **So there is a third design**,
`wide`: the same loop, the same tool, the same instruction, at the fixed path's budget. Three
designs make the two questions separable. **Fixed against wide is the design. Agent against wide
is the budget.**

**All three of chapter 4's stopping conditions are in the loop and all three are reachable.** The
model saying it is done, which is a reply with an `answer` in it. A step limit, which is six. And
[**your code refusing**]{.noindex} — a reply that is neither a search nor an answer ends the run, because a
loop that keeps going on a reply it could not parse is a loop with two stopping conditions and not
three.

> **Note:** The first run of this lab crashed, and the reason is worth a program comment rather
> than a silent fix. Asked for `{"answer": "..."}` the model sometimes returns
> `{"answer": {"part1": …, "part2": …}}` — valid JSON, and not the shape asked for. The request
> sets JSON mode, so what the engine compiled is *this is JSON* and nothing about the type of that
> field, which is on chapter 22's own list of what a guaranteed format never buys: the parts of
> your schema the engine did not compile. Chapter 21 supplies the rule that follows — a program
> must never trust prose. `as_text` serialises what came back instead of crashing on it, so a run
> that answers in the wrong shape is graded on what it said rather than lost.

> **Tip:** `run.py` writes `runs.json` after every task rather than at the end. The crash above is
> why: a run that saves only on success loses everything when it fails part-way through, and the
> cost of the rule is one line inside the loop instead of one after it. **And it reads that file
> ever after**, which is the matching trap: edit a design, run this again, and it reports the old
> data without a word. Move the file aside when you change a design.
## Step 3: Run Every Design Twelve Times Over

Chapter 38's instruction is the cheapest thing you can do to an agent's evaluation: run every task
more than once and write down the per-task counts rather than the total. Three trials, three
designs, twelve tasks.

```python
"""Run every design over every task, three times each, and save it.

12 tasks x 3 designs x 3 trials = 108 runs. Chapter 38's rule is that
one run of one task is one of chapter 20's trials and that the per-task
counts are what you write down, so every trial is a row here and
nothing is averaged on the way in.

Chapter 20's other rule applies too: the set is fixed before the
comparison. tasks.py was written and asserted before either design
ran a single question.

    python3 run.py        writes runs.json

It writes that file once and READS IT EVER AFTER. So editing a design
and running this again reports the old data with no warning, which is
a trap worth knowing about in a program whose whole job is comparing
designs: delete runs.json, or move it aside, when you change one.
"""
import json
import pathlib
import time

import search
from designs import DESIGNS
from tasks import cases, grade

OUT = pathlib.Path("runs.json")
TRIALS = 3


def run():
    cache = search.vectors()
    cs = cases()
    total = len(cs) * len(DESIGNS) * TRIALS
    rows, done = [], 0
    for tid, q, needs, docs in cs:
        for name, fn in DESIGNS.items():
            for trial in range(1, TRIALS + 1):
                r = fn(q, cache)
                ok, hits = grade(r["answer"], needs)
                r.update({"task": tid, "question": q, "trial": trial,
                          "passed": ok, "parts": hits,
                          "docs": list(docs)})
                rows.append(r)
                done += 1
        # Written after every task, not at the end: defect 69's lesson
        # is that a run saving only on success loses a run that fails.
        OUT.write_text(json.dumps(rows, indent=1))
        print(f"  {tid} {done:3d}/{total}", flush=True)
    return rows


def runs():
    return json.loads(OUT.read_text()) if OUT.exists() else run()


if __name__ == "__main__":
    rs = runs()
    print(f"\n  {len(rs)} runs, model {rs[0]['model']}\n")
    print("  design  chat calls  searches   in-tokens  out   seconds")
    for name in DESIGNS:
        d = [r for r in rs if r["design"] == name]
        print(f"  {name:7s} {sum(r['chat_calls'] for r in d):10d}"
              f" {sum(r['searches'] for r in d):9d}"
              f" {sum(r['prompt_tokens'] for r in d):11d}"
              f" {sum(r['output_tokens'] for r in d):5d}"
              f" {sum(r['seconds'] for r in d):9.1f}")
    print("\n  Nothing is graded in this table and that is on purpose.")
    print("  These are the three columns people quote about an agent")
    print("  before anybody asks whether it did the task - and the")
    print("  next program is the one that asks.")
```

```text

  108 runs, model gpt-4o-mini-2024-07-18

  design  chat calls  searches   in-tokens  out   seconds
  fixed           36        36       23493  1029     112.3
  agent           79        43       22363  1734     147.8
  wide            74        38       32750  1828     172.1

  Nothing is graded in this table and that is on purpose.
  These are the three columns people quote about an agent
  before anybody asks whether it did the task - and the
  next program is the one that asks.
```

**Nothing in that table is graded, which is the point of printing it.** Chat calls, tokens,
seconds: these are the columns an agent gets described by before anybody asks whether it did the
task. The fixed path made 36 chat calls; the agent made 79 and the wide agent 74.

**And the token column tells three different stories, none of them about whether the work got
done.** The agent sent *fewer* input tokens than the fixed path — 22,363 against 23,493 — because
its per-search budget is smaller and it mostly searched once. The wide agent, the same loop at the
fixed path's budget, sent 32,750. **So the design that looks cheapest on tokens is the one being
starved**, and the figure would have read as an economy.

> **Warning:** `runs.json` is written after every task and [**read ever after**]{.noindex}. Edit a design, run
> this again, and it reports the old data without a word. That is how the `wide` design came to
> exist here at all — the file had to be moved aside and all 108 runs made again, because mixing a
> fresh third design with a cached two-design run would have been a worse defect than the one it
> was fixing.

## Step 4: Read It Six Ways, In This Order

```python
"""Read the runs. Six questions, in the order they have to be asked.

Chapter 38 is the method: an agent's unit is a task, one run of a task
is one of chapter 20's trials, and a grid of tasks and trials yields
three different figures, any of which somebody would report as the
success rate. Chapter 20 supplies the interval. Chapter 34 supplies the
question the figures are for.

Nothing here is averaged before it is reported. The per-task counts
come first, because chapter 38's cheapest instruction is to write those
down rather than the total.
"""
import random

from designs import DESIGNS, FIXED_BUDGET, STEP_BUDGET, STEP_LIMIT
from run import TRIALS, runs
from tasks import cases, grade

BUDGETS = {"fixed": FIXED_BUDGET, "agent": STEP_BUDGET,
           "wide": FIXED_BUDGET}

RESAMPLES = 10_000
SEED = 47


def regrade(rs):
    """Grade every stored answer with the CURRENT grader, rather than
    trusting the verdict recorded when the run happened.

    The grader changed once already - `variants` was added after the
    first run's failures were read - and chapter 41 is explicit about
    what makes that legitimate: the repair has to be justified by the
    documents rather than by which design lost. These runs were made
    with the repaired grader, so this should move nothing, and a
    function that says so is worth more than an assurance."""
    need = {t: n for t, _, n, _ in cases()}
    moved = []
    for r in rs:
        ok, hits = grade(r["answer"], need[r["task"]])
        if ok != r["passed"]:
            moved.append((r["task"], r["design"], r["trial"], ok))
        r["passed"], r["parts"] = ok, hits
    return moved


def grid(rs):
    """task -> design -> list of pass/fail over the trials."""
    out = {}
    for r in rs:
        out.setdefault(r["task"], {}).setdefault(r["design"], []) \
            .append(r["passed"])
    return out


def three_ways(cols):
    """Chapter 38's three readings of one grid."""
    n = len(cols)
    trials = sum(sum(v) for v in cols.values())
    runs_ = sum(len(v) for v in cols.values())
    ever = sum(1 for v in cols.values() if any(v))
    always = sum(1 for v in cols.values() if all(v))
    return trials / runs_, ever / n, always / n


def per_task(rs, design, field):
    out = {}
    for r in rs:
        if r["design"] == design:
            out.setdefault(r["task"], []).append(r[field])
    return {k: sum(v) / len(v) for k, v in out.items()}


def interval(pairs, rounds=RESAMPLES, seed=SEED):
    """Chapter 20's paired bootstrap. The method is 20's; the pairing
    is one task's mean over its trials under each design, so one task
    stays one row."""
    r = random.Random(seed)
    k = len(pairs)
    diffs = []
    for _ in range(rounds):
        s = [pairs[r.randrange(k)] for _ in range(k)]
        diffs.append(sum(b - a for a, b in s) / k)
    diffs.sort()
    return diffs[int(0.025 * rounds)], diffs[int(0.975 * rounds)]


if __name__ == "__main__":
    rs = runs()
    as_run = {(r["task"], r["design"], r["trial"]): r["passed"] for r in rs}
    moved = regrade(rs)
    g = grid(rs)
    tasks = sorted(g)
    qs = {t: q for t, q, _, _ in cases()}
    order = list(DESIGNS)
    loops = [d for d in order if d != "fixed"]

    print(f"  {len(tasks)} tasks, {len(order)} designs,"
          f" {TRIALS} trials each = {len(rs)} runs")
    print("  per-search budget: "
          + ", ".join(f"{d} {BUDGETS[d]}" for d in order))
    print()

    print("  0. THE GRADER. It was repaired once, after the first run")
    print("     of this lab, and these runs were made with the repair")
    print("     in place - so re-applying it should move nothing, and")
    print("     the check is here because `should` is not a")
    print("     measurement.\n")
    print(f"     verdicts that move on re-grading: {len(moved)}"
          f" of {len(rs)}")
    if moved:
        for tid, design, trial, ok in moved:
            print(f"       {tid} {design} t{trial} -> {ok}")
    print()
    print("     What the repair was: the fixed path answered *a")
    print("     three-year warranty* where the key wanted *three")
    print("     years*, and `plan-harbour-plus` says *making three")
    print("     years rather than two*, so the two phrasings are the")
    print("     same claim and the key was wrong. `variants` accepts")
    print("     the hyphenated singular of any quantity-and-unit")
    print("     phrase, which is a rule rather than a special case.")
    print("     On the first run it moved three verdicts, all of them")
    print("     the fixed path's - the direction that makes a late")
    print("     repair credible. On this run it moves what the line")
    print("     above says.\n")

    print("  1. THE PER-TASK COUNTS, which chapter 38 says to write")
    print("     down instead of the total.\n")
    print("     task  " + "  ".join(f"{d:>6s}" for d in order)
          + "   question")
    for t in tasks:
        cells = "  ".join(f"{sum(g[t][d])} of {TRIALS}" for d in order)
        print(f"     {t}  {cells}   {qs[t][:26]}")

    print("\n  2. THE SAME GRID, READ THREE WAYS. Chapter 38's point")
    print("     is that all three are properly computed and they")
    print("     answer different questions.\n")
    print("     design   trials passed   pass@3   pass^3")
    for name in order:
        cols = {t: g[t][name] for t in tasks}
        a, b, c = three_ways(cols)
        print(f"     {name:8s} {a:12.2f} {b:8.2f} {c:8.2f}")
    spread = {}
    for name in order:
        cols = {t: g[t][name] for t in tasks}
        a, b, c = three_ways(cols)
        spread[name] = max(a, b, c) - min(a, b, c)
    flat = [d for d in order if spread[d] == 0]
    print(f"\n     the three readings are identical for"
          f" {', '.join(flat) if flat else '(none)'}")
    print("     and spread by "
          + ", ".join(f"{spread[d]:.2f} for {d}"
                      for d in order if spread[d]) + "\n")

    print("  3. WHAT THE FAILURES LOOK LIKE, because chapter 46's")
    print("     mode is half an answer and a rate cannot see it.\n")
    print("     design   failed   exactly one part met   neither")
    for name in order:
        bad = [r for r in rs if r["design"] == name and not r["passed"]]
        half = [r for r in bad if sum(r["parts"]) == 1]
        none_ = [r for r in bad if sum(r["parts"]) == 0]
        print(f"     {name:8s} {len(bad):6d} {len(half):21d}"
              f" {len(none_):9d}")

    print("\n  4. COST AND TIME, and then the only figure that puts")
    print("     them together.\n")
    print("     design   chats  in-tok  out-tok   secs  per run")
    for name in order:
        d = [r for r in rs if r["design"] == name]
        print(f"     {name:8s} {sum(r['chat_calls'] for r in d):5d}"
              f" {sum(r['prompt_tokens'] for r in d):7d}"
              f" {sum(r['output_tokens'] for r in d):8d}"
              f" {sum(r['seconds'] for r in d):6.0f}"
              f" {sum(r['seconds'] for r in d)/len(d):8.1f}")
    print()
    print("     design   passed   input tokens per passed run")
    for name in order:
        d = [r for r in rs if r["design"] == name]
        ok = [r for r in d if r["passed"]]
        per = sum(r["prompt_tokens"] for r in d) / len(ok) if ok else 0
        print(f"     {name:8s} {len(ok):6d} {per:28.0f}")

    print("\n  5. IS EACH DIFFERENCE REAL. Chapter 20's paired")
    print("     bootstrap, one task to a row, trials averaged within")
    print("     the task, resampling tasks.\n")
    mean_of = {d: per_task(rs, d, "passed") for d in order}
    PAIRS = [("fixed", "agent", "design and budget together"),
             ("fixed", "wide", "the design, budget held"),
             ("agent", "wide", "the budget, design held")]
    PAIRS = [p for p in PAIRS
             if p[0] in mean_of and p[1] in mean_of]
    print(f"     {len(PAIRS)} pairs over {len(order)} designs,"
          f" {len(tasks)} tasks each.\n")
    print("     comparison            diff   95% interval      says")
    cleared = []
    for a_name, b_name, what in PAIRS:
        pairs = [(mean_of[a_name][t], mean_of[b_name][t]) for t in tasks]
        lo, hi = interval(pairs)
        mean = sum(b - a for a, b in pairs) / len(pairs)
        verdict = (b_name if lo > 0 else a_name if hi < 0
                   else "cannot tell")
        if verdict != "cannot tell":
            cleared.append((a_name, b_name, what))
        print(f"     {b_name} - {a_name:8s} {mean:+.3f}"
              f"  {lo:+.3f} to {hi:+.3f}  {verdict}")
        print(f"       isolates: {what}")
    print()
    for name in order:
        m = mean_of[name]
        print(f"     {name:8s} {sum(m.values())/len(m):.3f}")
    gap = (sum(mean_of["fixed"].values()) - sum(mean_of["agent"].values())) \
        / len(tasks)
    budget = (sum(mean_of["wide"].values())
              - sum(mean_of["agent"].values())) / len(tasks)
    design = (sum(mean_of["fixed"].values())
              - sum(mean_of["wide"].values())) / len(tasks)
    print(f"\n     So the {gap:.0%} between the fixed path and the agent")
    print(f"     as first built splits into {budget:.0%} of budget and")
    print(f"     {design:.0%} of design - and read the interval column")
    print(f"     again. {len(cleared)} of the {len(PAIRS)} comparisons clears zero:")
    for a_name, b_name, what in cleared:
        print(f"       {b_name} - {a_name} ({what})")
    if [c[2] for c in cleared] == ["design and budget together"]:
        print("     The one comparison that gives a verdict is the")
        print("     one that confounds the two, and neither half of")
        print("     it gives a verdict on its own.\n")
    else:
        print("     Read which they are before taking anything from")
        print("     the split above.\n")
    print("     IF each difference were the size measured above,")
    print(f"     how often {len(tasks)} tasks' worth of evidence would")
    print("     clear zero - resampling these tasks with replacement")
    print("     and reading the share of resamples whose interval")
    print("     clears zero. This is conditional on the measured")
    print("     effect, and the intervals above say that effect is")
    print("     not pinned down. It is not a forecast of what more")
    print("     tasks would show.\n")
    print("     tasks   fixed vs wide   wide vs agent")
    import random as _r
    for n in (12, 24, 48, 96, 192):
        line = []
        for a_name, b_name in (("fixed", "wide"), ("agent", "wide")):
            base = [(mean_of[a_name][t], mean_of[b_name][t])
                    for t in tasks]
            rng = _r.Random(SEED)
            clears = 0
            for _ in range(400):
                drawn = [base[rng.randrange(len(base))]
                         for _ in range(n)]
                lo2, hi2 = interval(drawn, rounds=400,
                                    seed=rng.randrange(1 << 30))
                clears += lo2 > 0 or hi2 < 0
            line.append(clears / 400)
        print(f"     {n:5d} {line[0]:14.0%} {line[1]:15.0%}")
        if n == len(tasks):
            at_n = line
    print()
    #  The two separable questions, which is what the table covers -
    #  not the confounded comparison, which is not a question anyone
    #  wanted the answer to.
    SPLIT = [("fixed", "wide"), ("agent", "wide")]
    open_ = [(a, b) for a, b in SPLIT
             if not any(c[0] == a and c[1] == b for c in cleared)]
    print(f"     {len(open_)} of the {len(SPLIT)} separable questions"
          f" {'is' if len(open_) == 1 else 'are'}")
    print(f"     unsettled by {len(tasks)} tasks, and the top row is why:"
          f" at")
    print("     the effects measured here, that many tasks clears")
    print(f"     zero in {max(at_n):.0%} of resamples at best. Read the"
          f" table")
    print("     as what would follow IF those effects are the real")
    print("     ones, and run this arithmetic before a comparison")
    print(f"     rather than after - doing it after is how a")
    print(f"     confounded {gap:.0%} gets reported as a finding about")
    print("     architecture.\n")

    print("  6. HOW EACH LOOP'S RUNS ENDED, which is chapter 4's")
    print("     three stopping conditions counted.\n")
    for name in loops:
        d = [r for r in rs if r["design"] == name]
        ends = {}
        for r in d:
            ends[r["ended"]] = ends.get(r["ended"], 0) + 1
        print(f"     {name}: " + ", ".join(
            f"{k} {v} of {len(d)}" for k, v in
            sorted(ends.items(), key=lambda kv: -kv[1])))
    print(f"     step limit is {STEP_LIMIT} chat calls, so a run that")
    print(f"     answers can search at most {STEP_LIMIT - 1} times\n")
    print("     design   searches  runs  of those, passed")
    for name in loops:
        bys = {}
        for r in rs:
            if r["design"] == name:
                bys.setdefault(r["searches"], []).append(r["passed"])
        for s in sorted(bys):
            v = bys[s]
            print(f"     {name:8s} {s:8d} {len(v):5d} {sum(v):17d}")
```

```text
  12 tasks, 3 designs, 3 trials each = 108 runs
  per-search budget: fixed 2500, agent 1200, wide 2500

  0. THE GRADER. It was repaired once, after the first run
     of this lab, and these runs were made with the repair
     in place - so re-applying it should move nothing, and
     the check is here because `should` is not a
     measurement.

     verdicts that move on re-grading: 0 of 108

     What the repair was: the fixed path answered *a
     three-year warranty* where the key wanted *three
     years*, and `plan-harbour-plus` says *making three
     years rather than two*, so the two phrasings are the
     same claim and the key was wrong. `variants` accepts
     the hyphenated singular of any quantity-and-unit
     phrase, which is a rule rather than a special case.
     On the first run it moved three verdicts, all of them
     the fixed path's - the direction that makes a late
     repair credible. On this run it moves what the line
     above says.

  1. THE PER-TASK COUNTS, which chapter 38 says to write
     down instead of the total.

     task   fixed   agent    wide   question
     t01  0 of 3  0 of 3  3 of 3   What does standard deliver
     t02  3 of 3  3 of 3  3 of 3   How long do I have to retu
     t03  3 of 3  2 of 3  3 of 3   Your refunds policy and yo
     t04  3 of 3  0 of 3  0 of 3   What is the Northern Irela
     t05  3 of 3  1 of 3  3 of 3   What does next-day deliver
     t06  3 of 3  2 of 3  3 of 3   How many years of warranty
     t07  3 of 3  3 of 3  3 of 3   What does Harbour Plus cos
     t08  3 of 3  0 of 3  0 of 3   How long do I have to retu
     t09  3 of 3  3 of 3  0 of 3   How long is a repair cover
     t10  3 of 3  0 of 3  3 of 3   What is the most you will 
     t11  3 of 3  0 of 3  3 of 3   How long do I have to repo
     t12  3 of 3  3 of 3  3 of 3   How wide are the toaster's

  2. THE SAME GRID, READ THREE WAYS. Chapter 38's point
     is that all three are properly computed and they
     answer different questions.

     design   trials passed   pass@3   pass^3
     fixed            0.92     0.92     0.92
     agent            0.47     0.58     0.33
     wide             0.75     0.75     0.75

     the three readings are identical for fixed, wide
     and spread by 0.25 for agent

  3. WHAT THE FAILURES LOOK LIKE, because chapter 46's
     mode is half an answer and a rate cannot see it.

     design   failed   exactly one part met   neither
     fixed         3                     3         0
     agent        19                    19         0
     wide          9                     9         0

  4. COST AND TIME, and then the only figure that puts
     them together.

     design   chats  in-tok  out-tok   secs  per run
     fixed       36   23493     1029    112      3.1
     agent       79   22363     1734    148      4.1
     wide        74   32750     1828    172      4.8

     design   passed   input tokens per passed run
     fixed        33                          712
     agent        17                         1315
     wide         27                         1213

  5. IS EACH DIFFERENCE REAL. Chapter 20's paired
     bootstrap, one task to a row, trials averaged within
     the task, resampling tasks.

     3 pairs over 3 designs, 12 tasks each.

     comparison            diff   95% interval      says
     agent - fixed    -0.444  -0.694 to -0.194  fixed
       isolates: design and budget together
     wide - fixed    -0.167  -0.500 to +0.167  cannot tell
       isolates: the design, budget held
     wide - agent    +0.278  -0.056 to +0.583  cannot tell
       isolates: the budget, design held

     fixed    0.917
     agent    0.472
     wide     0.750

     So the 44% between the fixed path and the agent
     as first built splits into 28% of budget and
     17% of design - and read the interval column
     again. 1 of the 3 comparisons clears zero:
       agent - fixed (design and budget together)
     The one comparison that gives a verdict is the
     one that confounds the two, and neither half of
     it gives a verdict on its own.

     IF each difference were the size measured above,
     how often 12 tasks' worth of evidence would
     clear zero - resampling these tasks with replacement
     and reading the share of resamples whose interval
     clears zero. This is conditional on the measured
     effect, and the intervals above say that effect is
     not pinned down. It is not a forecast of what more
     tasks would show.

     tasks   fixed vs wide   wide vs agent
        12            18%             42%
        24            30%             67%
        48            51%             91%
        96            79%            100%
       192            98%            100%

     2 of the 2 separable questions are
     unsettled by 12 tasks, and the top row is why: at
     the effects measured here, that many tasks clears
     zero in 42% of resamples at best. Read the table
     as what would follow IF those effects are the real
     ones, and run this arithmetic before a comparison
     rather than after - doing it after is how a
     confounded 44% gets reported as a finding about
     architecture.

  6. HOW EACH LOOP'S RUNS ENDED, which is chapter 4's
     three stopping conditions counted.

     agent: answered 36 of 36
     wide: answered 36 of 36
     step limit is 6 chat calls, so a run that
     answers can search at most 5 times

     design   searches  runs  of those, passed
     agent           1    29                11
     agent           2     7                 6
     wide            1    34                25
     wide            2     2                 2
```

**Section 0 is the grader, and this time it moves nothing.** It was repaired after the first run of
this lab — the fixed path answered *a three-year warranty* where the key wanted *three years*, and
`plan-harbour-plus` says *making three years rather than two*, so the two phrasings are the same
claim and the key was wrong. The repair is written as a rule and not a special case: a quantity's
unit also accepts its hyphenated singular. **These runs were made with the repair in place, so
re-applying it moves 0 of 108 verdicts** — which is what should happen and is worth a line because
*should* is not a measurement. On the first run it moved three, all of them the fixed path's, which
is the direction that makes a late repair credible.

**Then the per-task counts, and they are the reason chapter 38 asks for them.** The fixed path is
3 of 3 on eleven tasks and 0 of 3 on `t01`. The wide agent is 3 of 3 on nine, 0 of 3 on three. And
**read `t01` and `t09` against each other**: the wide agent passes the one task the fixed path
cannot, and fails a task both other designs pass three times out of three. Four tasks separate
those two designs, and they do not all point the same way.

**Section 2 is chapter 38's three readings, and two of the three designs have no spread at all.**
The fixed path reads 0.92, 0.92, 0.92 and the wide agent 0.75, 0.75, 0.75 — trials passed, pass@3
and pass\^3 identical, because every task came out the same way all three times. The agent spreads
0.25, from 0.47 to 0.58 to 0.33. **The gap between chapter 38's three figures is a measurement of
unreliability**, so on a design that never varies they carry no information, and the moment they
separate they are telling you about variance rather than capability. Note what the identical rows
are and are not: a measurement of these designs on this set, not a property of fixed paths —
chapter 13 is explicit that temperature zero is not a guarantee, so any of these could vary and two
of them did not.

> **Note:** The agent's `pass@3` of 0.58 is a number to be careful with, and chapter 38 says why.
> pass@k is a capability only when something can tell a good attempt from a bad one, because three
> attempts are worth nothing to a user who cannot see which worked. Nothing in either loop selects
> among its three trials, so **0.58 is not what this agent can do** — it is what three independent
> draws of it contain between them.

**Section 3 is the most striking line in the chapter and it took one `sum`.** Thirty-one runs failed
across three designs, and **every single one of them met exactly one of the two requirements. Not
one met neither.** Chapter 46 named *Answers for one case when two apply* from four failures in
eighty answers and built no check for it; here it is one hundred per cent of the failure surface of
one hundred and eight runs.

**Section 4 is where the token column stops flattering anybody.** Per *passed* run the fixed path
costs 712 input tokens, the wide agent 1,213 and the agent 1,315. **The cheapest design on the
total is the dearest per answer that is right.**

That quotient is the **cost per success**: what a run costs divided by the runs that passed, rather
than by the runs you made. **It is the only one of a comparison's cost columns that is a
comparison**, because a success rate says nothing about what the successes cost and a token count
says nothing about whether they worked.

**Section 5 is where this chapter changed its mind, and it is the part worth the forty minutes.**
Three designs ask two questions, so there are three comparisons:

- **Agent against the fixed path: −0.444, interval −0.694 to −0.194.** Clears zero. This is the
  comparison the lab was built to make, and on its own it reads as *the fixed path wins by 44
  points*.
- **Wide agent against the fixed path, which holds the budget and isolates the design: −0.167,
  interval −0.500 to +0.167. Cannot tell.**
- **Wide agent against the agent, which holds the design and isolates the budget: +0.278, interval
  −0.056 to +0.583. Cannot tell.**

**So the 44 points split into 28 of budget and 17 of design, and neither half clears zero.** The
only comparison in the chapter that gives a verdict is the one that confounds the two things it is
asking about. **Had this lab stopped at two designs it would have reported a confounded 44 points
as a finding about architecture**, and the arithmetic that stops it is chapter 20's and nothing
cleverer.

**And section 5 ends with the question chapter 20 says to ask before the comparison rather than
after it.** Resampling these twelve tasks, the share of resamples in which each isolated
comparison clears zero: the design question gets there 18 per cent of the time at twelve tasks, 51
per cent at forty-eight and 98 per cent at a hundred and ninety-two. The budget question reaches
91 per cent at forty-eight.

**Read that table with its condition attached, because the condition is doing most of the work.**
Every row resamples the twelve tasks I have, so every row assumes the difference is the size those
twelve measured — 17 points of design, 28 of budget. The intervals three paragraphs up say that
assumption is exactly what is not established: the design difference is somewhere from −50 to +17
points, and zero is inside it. So the table does not say *a hundred and ninety-two tasks would
settle the design question*. It says *if the difference really is 17 points, a hundred and ninety-two
tasks would show it about always* — and if it is really zero, a hundred and ninety-two tasks clear
zero about five per cent of the time, which is what a 95 per cent interval means. **A resample
cannot tell you what more data would show, because it only has the data you have.** What it can
tell you is which of your questions twelve tasks was never going to answer, and both of these
were.

**Section 6 is chapter 4's three stopping conditions, counted — and only one of them ever fired,
for either loop.** All 72 loop runs ended by answering. The step limit of six chat calls was never
reached, so neither was the code's refusal. **Neither loop ran away; both stopped early.** The agent
searched once on 29 of 36 runs and the wide agent on 34 of 36.

That is **declined freedom**: a loop that does not use the freedom its design gives it, so it
behaves as the pattern below it at the loop's price. It is measurable as the share of runs that
took the cheapest path available — 63 of 72 here, with a tool and four unused steps in hand — and
it is what a success rate cannot show you, because a loop behaving as a single call and a single
call are the same system from the outside.

> **Tip:** Print the budget beside the design name, as `read.py`'s header does. The confound in this
> chapter survived a first draft, a full run and a careful read of the output, and what would have
> caught it at a glance is the one line that says what each design was given.
## Step 5: Where the Retrieval Went, Counted

A verdict is not a diagnosis, and section 5 left both of its questions open. Three counts that say
where each design lost what it lost.

```python
"""Why the agent lost. Three questions the table in step 4 cannot
answer, each a count rather than a reading.

The first asks what the agent searched for. The second asks whether it
knew it was missing something. The third is the one that decides what
kind of failure this is at all: when a requirement was missed, was the
value the answer needed actually in the passages that design was
given? If it was, no amount of searching is the fix, and the
architecture is not the lever.
"""
import search
from designs import DESIGNS
from read import regrade
from run import runs
from tasks import cases, met, norm

DESIGN_ORDER = list(DESIGNS)

ABSENT = ("not specified", "no specific", "not mentioned",
          "no information", "not provided", "not available in",
          "does not provide", "do not provide")


def missing_value_was_present(r, needs):
    """For each requirement this run missed, was a phrasing of it in
    the passages the run was given? A requirement whose value was in
    front of the model is not a retrieval failure."""
    body = " ".join(search.BY_ID[c]["text"] for c in r["passages"])
    out = []
    for i, hit in enumerate(r["parts"]):
        if not hit:
            out.append(met(body, needs[i]))
    return out


if __name__ == "__main__":
    rs = runs()
    # The same re-grading read.py does, for the same reason: the
    # grader changed after the run, and two programs disagreeing
    # about how many runs failed would be a defect of this chapter
    # and not a finding about either design.
    regrade(rs)
    need = {t: n for t, _, n, _ in cases()}
    qs = {t: q for t, q, _, _ in cases()}

    print("  1. WHAT THE AGENT SEARCHED FOR, on the tasks it never")
    print("     passed. The question is above, the query below.\n")
    loops = [d for d in DESIGN_ORDER if d != "fixed"]
    never = sorted({r["task"] for r in rs if r["design"] in loops}
                   - {r["task"] for r in rs
                      if r["design"] in loops and r["passed"]})
    for t in never:
        r = next(x for x in rs if x["task"] == t
                 and x["design"] == loops[0] and x["trial"] == 1)
        print(f"     {t}")
        print(f"        asked:    {qs[t][:46]}")
        for q in r["queries"]:
            print(f"        searched: {q[:46]}")
    picked = [next(x for x in rs if x["task"] == t
                   and x["design"] == loops[0] and x["trial"] == 1)
              for t in never]
    shorter = sum(1 for t, r in zip(never, picked) for q in r["queries"]
                  if len(q) < len(qs[t]) / 2)
    queries = sum(len(r["queries"]) for r in picked)
    print()
    print(f"     {shorter} of those {queries} queries are under half the")
    print("     length of the question they were written from. The")
    print("     fixed path's query IS the question, word for word,")
    print("     because that is what its code sends.\n")

    print("  2. DID IT KNOW. Failures whose own answer says the")
    print("     information was not in the passages.\n")
    for name in DESIGN_ORDER:
        bad = [r for r in rs if r["design"] == name and not r["passed"]]
        said = [r for r in bad
                if any(p in norm(r["answer"]) for p in ABSENT)]
        one = [r for r in said if r["searches"] == 1]
        print(f"     {name:6s} {len(said)} of {len(bad)} failures say so,"
              f" {len(one)} of them after")
        print(f"            a single search")
    print()
    allone = [r for r in rs if r["design"] in loops
              and not r["passed"]
              and any(p in norm(r["answer"]) for p in ABSENT)]
    once = [r for r in allone if r["searches"] == 1]
    if allone and len(once) == len(allone):
        print("     Every one of those announced the gap after a")
        print("     SINGLE search, with the tool used once and the")
        print("     step limit untouched.")
    elif allone:
        print(f"     {len(once)} of those {len(allone)} announced the gap after a")
        print("     single search; the rest had searched more than")
        print("     once.")
    print("     That is not a retrieval problem and it is not a cost")
    print("     problem. It is a loop declining the thing a loop is")
    print("     for.\n")

    print("  3. WHAT KIND OF FAILURE IT IS. For every missed")
    print("     requirement, was the value in the passages that run")
    print("     was given?\n")
    print("     design   missed reqs   value WAS present   absent")
    for name in DESIGN_ORDER:
        present = absent = 0
        for r in rs:
            if r["design"] != name or r["passed"]:
                continue
            for was in missing_value_was_present(r, need[r["task"]]):
                present += was
                absent += not was
        print(f"     {name:8s} {present + absent:11d}"
              f" {present:18d} {absent:8d}")
    print()
    print("     And the same question asked of every requirement,")
    print("     met or missed, which is the stronger figure:\n")
    print("     design   requirements   in the passages it was given")
    for name in DESIGN_ORDER:
        tot = had = 0
        for r in rs:
            if r["design"] != name:
                continue
            body = " ".join(search.BY_ID[c]["text"]
                            for c in r["passages"])
            for req in need[r["task"]]:
                tot += 1
                had += met(body, req)
        print(f"     {name:8s} {tot:12d} {had:24d}")
    print()
    rows_ = {}
    for name in DESIGN_ORDER:
        present = absent = 0
        for r in rs:
            if r["design"] != name or r["passed"]:
                continue
            for was in missing_value_was_present(r, need[r["task"]]):
                present += was
                absent += not was
        rows_[name] = (present, absent)
    p_f, a_f = rows_["fixed"]
    print("     And chapter 20's interval on that count, because a")
    print("     second measure quoted without one is the thing this")
    print("     book keeps warning about. One task to a row, the")
    print("     share of its requirements present, averaged over its")
    print("     trials:\n")
    from read import interval
    share = {}
    for name in DESIGN_ORDER:
        per = {}
        for r in rs:
            if r["design"] != name:
                continue
            body = " ".join(search.BY_ID[c]["text"]
                            for c in r["passages"])
            reqs = need[r["task"]]
            per.setdefault(r["task"], []).append(
                sum(met(body, q) for q in reqs) / len(reqs))
        share[name] = {k: sum(v) / len(v) for k, v in per.items()}
    tids = sorted(share["fixed"])
    print("     comparison            diff   95% interval")
    for a_name, b_name in (("fixed", "wide"), ("agent", "wide"),
                           ("fixed", "agent")):
        if a_name not in share or b_name not in share:
            continue
        pairs = [(share[a_name][k], share[b_name][k]) for k in tids]
        lo, hi = interval(pairs)
        mean = sum(b - a for a, b in pairs) / len(pairs)
        says = (b_name if lo > 0 else a_name if hi < 0
                else "cannot tell")
        print(f"     {b_name} - {a_name:8s} {mean:+.3f}"
              f"  {lo:+.3f} to {hi:+.3f}  {says}")
    print()
    print("     This is a count of what reached the model and not a")
    print("     count of right answers, so it is a diagnosis rather")
    print("     than a second verdict on the designs. Where it")
    print("     clears zero it says where the retrieval went, which")
    print("     is the question the grade cannot answer at twelve")
    print("     tasks.\n")
    if a_f == 0 and p_f:
        failed_on = sorted({r["task"] for r in rs
                            if r["design"] == "fixed" and not r["passed"]})
        print("     Read the fixed path's row first. Every requirement")
        print(f"     it missed was in front of it, on"
              f" {len(failed_on)} task(s)")
        print(f"     ({', '.join(failed_on)}) - so searching again could")
        print("     not have fixed any of them, and no architecture is")
        print("     the lever on them.\n")
    else:
        print(f"     The fixed path missed {a_f} requirement(s) it had")
        print(f"     never been given and {p_f} it had.\n")
    for name in DESIGN_ORDER[1:]:
        pr, ab = rows_[name]
        if pr and ab:
            print(f"     {name}'s row SPLITS - {pr} it had been given and")
            print(f"     {ab} it had not - which is the honest picture of")
            print("     what a loop is for.")
        elif ab:
            print(f"     {name} missed {ab} requirement(s) and had been")
            print("     given none of them: all of its failures are")
            print("     failures to look.")
        elif pr:
            print(f"     {name} had been given every one of the {pr} it")
            print("     missed, so none of its failures is a retrieval")
            print("     failure either.")
```

```text
  1. WHAT THE AGENT SEARCHED FOR, on the tasks it never
     passed. The question is above, the query below.

     t04
        asked:    What is the Northern Ireland surcharge, and wh
        searched: Northern Ireland surcharge
     t08
        asked:    How long do I have to return a clearance item,
        searched: return clearance item policy

     2 of those 2 queries are under half the
     length of the question they were written from. The
     fixed path's query IS the question, word for word,
     because that is what its code sends.

  2. DID IT KNOW. Failures whose own answer says the
     information was not in the passages.

     fixed  0 of 3 failures say so, 0 of them after
            a single search
     agent  7 of 19 failures say so, 6 of them after
            a single search
     wide   2 of 9 failures say so, 2 of them after
            a single search

     8 of those 9 announced the gap after a
     single search; the rest had searched more than
     once.
     That is not a retrieval problem and it is not a cost
     problem. It is a loop declining the thing a loop is
     for.

  3. WHAT KIND OF FAILURE IT IS. For every missed
     requirement, was the value in the passages that run
     was given?

     design   missed reqs   value WAS present   absent
     fixed              3                  3        0
     agent             19                  3       16
     wide               9                  0        9

     And the same question asked of every requirement,
     met or missed, which is the stronger figure:

     design   requirements   in the passages it was given
     fixed              72                       72
     agent              72                       54
     wide               72                       63

     And chapter 20's interval on that count, because a
     second measure quoted without one is the thing this
     book keeps warning about. One task to a row, the
     share of its requirements present, averaged over its
     trials:

     comparison            diff   95% interval
     wide - fixed    -0.125  -0.250 to +0.000  cannot tell
     wide - agent    +0.125  -0.042 to +0.278  cannot tell
     agent - fixed    -0.250  -0.375 to -0.125  fixed

     This is a count of what reached the model and not a
     count of right answers, so it is a diagnosis rather
     than a second verdict on the designs. Where it
     clears zero it says where the retrieval went, which
     is the question the grade cannot answer at twelve
     tasks.

     Read the fixed path's row first. Every requirement
     it missed was in front of it, on 1 task(s)
     (t01) - so searching again could
     not have fixed any of them, and no architecture is
     the lever on them.

     agent's row SPLITS - 3 it had been given and
     16 it had not - which is the honest picture of
     what a loop is for.
     wide missed 9 requirement(s) and had been
     given none of them: all of its failures are
     failures to look.
```

**The first section is two tasks and two queries.** On the tasks no loop ever passed, both queries
are under half the length of the question they were written from: asked the Northern Ireland
surcharge *and* the named-day charge, the loop searched *Northern Ireland surcharge*. **The fixed
path's query is the question, word for word, because that is what its code sends.**

**The second section is the part that is hard to look at.** Seven of the agent's nineteen failures
and two of the wide agent's nine contain, in their own answer, a sentence saying the information
was not in the passages. Eight of those nine came after a single search, **with a search tool
already used once, four more steps of the limit unspent, and no reason not to look again.**

**The third section is the measurement I would now want from any comparison of designs, and it is
the one that answers section 5's question.** For every requirement of every run — met or missed —
was a phrasing of it in the passages that run was given?

- **The fixed path: 72 of 72.** Every value it was asked for was in front of it, every time. Its
  one failing task is therefore not a retrieval failure at all: it was handed 3.99 and 9.50 and
  answered 9.50. **No architecture is the lever on that one.**
- **The wide agent: 63 of 72**, at the fixed path's budget. The nine it missed it had never been
  given, so every one of its failures is a failure to look rather than a failure to use.
- **The agent: 54 of 72.**

**Put chapter 20's interval on that count and it says the same thing the grade did, which is the
useful part.** Wide against fixed is −0.125 with an interval of −0.250 to +0.000 — *cannot tell*,
by a hair. Wide against the agent is +0.125 at −0.042 to +0.278 — *cannot tell*. Agent against the
fixed path is −0.250 at −0.375 to −0.125, which clears zero and is again the confounded pair.
**Two measures, three comparisons each, and only the confounded one has a verdict in either.**

**But the counts themselves are a diagnosis and they do split cleanly**, which is what a diagnosis
is for. Nine requirements lost to the budget, nine to the query, and the fixed path losing none.
That is not a verdict about designs and it is the thing to act on: **both loops lose requirements
by writing a narrower query than the one they were handed**, and the wider budget bought back
exactly half of what the narrow one had cost.

> **Warning:** The budget is why the step-5 Warning in this chapter's first draft was wrong. It
> said the two designs shared their retrieval and differed only in the query, and the budget made
> that false. **A comparison of designs has to say what each design was *given*, not only what it
> said** — and the line that says it is the one in `read.py`'s header, which was added after the
> confound was found rather than before.

## Step 6: What Chapter 34's Rule Said, Before Any of This

A hundred and eight model runs, three designs, six readings and a diagnosis. Now go back to
chapter 34's four columns and fill them in for this task, which takes a minute and a sheet of
paper.

**Can you enumerate the paths?** Yes. Search; possibly search again; answer. There are not forty of
them and they do not depend on what a previous system said — they depend on how many parts the
question has, which you can count. **On chapter 34's rule that is the end of the enquiry**: if you
can write the paths down, one of the five patterns runs them and you keep a known call count, a
reviewable shape and a bill you can predict.

**What is the shape?** *Pieces* — the question's parts. Chapter 34's table maps that to
parallelisation. **And here is a tension worth naming rather than stepping over**: chapter 34's own
nine worked tasks include *answer a support question* with the shape *sequence*, which it files as
a chain. This task is answering a support question, and the reclassification to *pieces* is a
judgement about a question with two parts in it rather than a correction of chapter 34. A reader who
turns back will find the other verdict, and both are defensible: it is a chain if you think of the
work as retrieve-then-answer, and pieces if you think of it as one retrieval per part.

**So chapter 34's rule says: a pattern, and specifically not an agent.** It said so before a single
call was made. **And the honest report of the measurement is that it cannot confirm it.** Once the
budget is held constant, twelve tasks and three trials cannot separate the loop from the fixed
path, in either the grade or the requirements it retrieved. What the measurement *can* say is
narrower and still worth having:

- The loop [**as first built**]{.noindex} was 44 points worse, and 28 of those points were a handicap I gave it.
- Both loops write narrower queries than the question they are handed, and lose requirements for it
  — nine of seventy-two even at the matched budget.
- Neither loop used the freedom the design exists for: 63 of 72 runs searched once, and eight of
  the nine failures that announced a gap did so after a single search.
- The fixed path costs 712 input tokens per right answer against 1,213 and 1,315.
- And twelve tasks was never going to answer either isolated question: if the differences are the
  size these twelve measured, forty-eight tasks reach a verdict on the design about half the time.
  That is a condition, not a forecast.

**That is the answer to the interview question, and the shape of it matters more than the numbers.**
Not *we tried an agent and it was worse*. Rather: the rule said a pattern; I measured it against
the loop on twelve tasks and three trials; the loop was 44 points worse; **and when I isolated the
two things that differed, neither half of the gap cleared zero, because 28 points of it were a
budget I had set without thinking about it.** The usable findings are the diagnosis and the sample
size, not the verdict.

**And it points at the design to measure next, which is none of these three.** The fixed path's one
failure had both values in front of it. Both loops lose requirements to a narrow query. Both are
answered by the same rung of chapter 34's ladder: **split the question, search once per part,
answer from both sets** — parallelisation, which is the fourth rung and which nothing here tried.
Chapter 34's order is to climb from the bottom and stop when the evaluation set passes; this chapter
started at the top because that is where the hunch pointed, and **the rungs between were never
tried at all.**

> **Note:** This is one task, one corpus, one model, twelve tasks and three trials. It establishes
> nothing about agents in general and is not meant to: chapter 34's rule is the general claim and
> this is a measurement of it on one step of one system, which came out underpowered. **What
> generalises is the procedure** — build the step every way you are comparing, hold everything you
> can and say what you could not, grade in code, run it more than once, read the cost per success,
> and isolate every difference you are tempted to explain.

> **Tip:** If you do this on your own system, the two cheapest things to add are step 5's third
> section and `read.py`'s header. *Was the value in the passages it was given?* separates a
> retrieval failure from a generation failure in one line of code. And printing what each design
> was given, beside its name, is what would have caught this chapter's confound before it was run
> rather than after.
## Summary, Key Terms, and Review Questions

### Summary

One step of chapter 45's system, built three ways and measured the same way. **The step is the one
chapter 46 could not check** — a question whose answer needs two documents — and the hunch is that
an agent fixes it, because one retrieval cannot see both halves.

**Twelve tasks, each asserted to need two documents and to be answerable by neither alone.** The
second assertion failed five times while the set was being written, each time on a two-part
question about one document. The grader is chapter 41's with containment instead of equality and a
declared set of phrasings per requirement, so **half an answer fails** — and what it is, is an
evaluation key somebody wrote by reading the documents, not the production check chapter 46 lacked.

**The two designs became three, and that is the chapter.** The fixed path is chapter 45's pipeline:
one dense retrieval, a 2,500-character budget, one answer call. The agent is chapter 4's loop with
one search tool, built at 1,200 characters per search on the reasoning that a loop accumulates
several searches' worth. **It searched once on 29 of 36 runs, so the smaller budget was never a
trade — it was a handicap, and a handicap is a confound.** So `wide` is the same loop at the fixed
path's budget. Three designs make the two questions separable: fixed against wide is the design,
agent against wide is the budget.

**Chapter 18's rule is to change one thing**, so the two instructions share their task sentence
word for word and the residue that cannot be equalised is named: a design with a tool has to be
told it has one. All three of chapter 4's stopping conditions are in the loop; the limit is six
chat calls, so a run that answers can search at most five times.

**Twelve tasks, three trials, three designs: 108 runs.** The fixed path made 36 chat calls, the
agent 79, the wide agent 74. **The token column tells three stories and none is about the work**:
the agent sent fewer input tokens than the fixed path, because it is the design being starved.

**The grader was repaired once and moves nothing here.** The fixed path had answered *a three-year
warranty* against a key wanting *three years*; `plan-harbour-plus` says *making three years rather
than two*, so the key was wrong. Written as a rule — a quantity's unit also accepts its hyphenated
singular — it moved three verdicts on the first run, all the fixed path's, and **0 of 108 on these.**

**Per task, the fixed path is 3 of 3 on eleven and 0 of 3 on one; the wide agent 3 of 3 on nine.**
And the two differ on four tasks that do not point the same way: **the wide agent passes the one
task the fixed path cannot, and fails one that both other designs pass three times out of three.**

**Chapter 38's three readings are identical for two of the designs** — 0.92, 0.92, 0.92 and 0.75,
0.75, 0.75 — because every task came out the same way all three times, and spread 0.25 for the
agent. **The gap between the three figures measures unreliability**, so on a design that never
varies they carry no information. That is a fact about these runs and not about fixed paths:
chapter 13 is explicit that temperature zero is not a guarantee.

**Thirty-one runs failed across three designs and every one of them met exactly one of the two
requirements.** None met neither. Chapter 46 named that mode from four failures in eighty answers;
here it is the whole failure surface of a hundred and eight runs.

**Per passed run the fixed path costs 712 input tokens, the wide agent 1,213 and the agent 1,315.**
The cheapest design on the total is the dearest per answer that is right.

**And then the part that changed this chapter's mind.** Three comparisons: the agent against the
fixed path is −0.444 at −0.694 to −0.194 and clears zero; the wide agent against the fixed path,
which isolates the **design**, is −0.167 at −0.500 to +0.167 and **cannot tell**; the wide agent
against the agent, which isolates the **budget**, is +0.278 at −0.056 to +0.583 and **cannot
tell.** **So the 44 points split into 28 of budget and 17 of design, and neither half clears zero.
The only comparison that gives a verdict is the one that confounds the two.** Had the lab stopped
at two designs it would have reported a confounded 44 points as a finding about architecture.

**Resampling the twelve says what twelve was never going to settle, not what more would show.**
The design question clears zero in 18 per cent of resamples at twelve tasks, 51 at forty-eight and
98 at a hundred and ninety-two — every row of that conditional on the difference being the 17
points these twelve measured, which the interval says is not established. **A resample only has
the data you already have.** What it establishes is that neither isolated question was answerable
at twelve tasks, and that is a result you can act on where the 44 points was not.

**All 72 loop runs ended by answering.** The step limit never fired and neither did the code's
refusal. **Neither loop ran away; both stopped early**, 63 of 72 runs searching once.

**Why they lost is three counts.** The queries on the tasks no loop passed are under half the length
of the question. Nine failures say in their own answer that the information was missing, eight of
them after a single search. And for every requirement of every run, met or missed: **the fixed path
was given 72 of 72, the wide agent 63 and the agent 54** — so the budget cost nine requirements and
the query cost nine, and the fixed path lost none. Chapter 20's interval on that count says the same
as it said about the grade: only the confounded pair has a verdict. **But the counts split cleanly,
and a diagnosis is what you act on.** Both loops lose requirements by writing a narrower query than
the one they were handed.

**Last, chapter 34's rule, filled in before any of this and in a minute.** The paths can be
enumerated and the shape is *pieces*, so the rule says a pattern and not an agent. **The
measurement cannot confirm it** — twelve tasks cannot separate the loop from the fixed path once
the budget is held — and what it can say is narrower and still worth having: the loop as first
built was 44 points worse, 28 of them a handicap; both loops write narrower queries; neither used
the freedom the design exists for; the fixed path is cheaper per right answer; and the design
question needs about forty-eight tasks. **And all of it points at the rung nothing here tried**:
split the question, search once per part, answer from both.

### Key Terms

| Term | Meaning |
|---|---|
| **Cost per success** | What a run costs divided by the runs that passed, rather than by the runs you made. The only one of a comparison's cost columns that is a comparison: here the agent sent fewer input tokens in total than the fixed path and the most per answer that was right. A success rate and a token count are two numbers, and neither of them is this one |
| **Declined freedom** | A loop that does not use the freedom its design gives it, so it behaves as the pattern below it at the loop's price. Measured as the share of runs that took the cheapest path available: 63 of 72 searched once with a tool and four unused steps in hand, and nine failures say in their own answer that something was missing |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The comparison to make | One step, every design you are choosing between, one grader, repeated trials. Hold everything you can, say what you could not, and **isolate every difference you are tempted to explain** — two designs that differ in two ways give one verdict about neither |
| What a confound costs | 44 points between a fixed path and a loop split into 28 of budget and 17 of design, and **neither half cleared zero**. The only comparison with a verdict was the one confounding both |
| What chapter 38's three readings are worth | Identical on a design that never varied: 0.92, 0.92, 0.92. Spread 0.25 on one that did. The spread measures unreliability, not capability — and pass@k is a capability only when something selects among the attempts |
| Cost per success | Input tokens per *passed* run. 712, 1,213 and 1,315 — and the design with the lowest total was the highest here |
| Where a loop's advantage went | 63 of 72 runs searched once, with four steps unused; of the nine failures that announced a gap, eight had searched once |
| What separates a retrieval failure from a generation failure | Was the value in the passages that run was given? Across every requirement of every run: 72 of 72, 63 of 72, 54 of 72 |
| What a resample can and cannot tell you about sample size | Resample your tasks and read the share that clear zero: here the design question 18 per cent at 12 tasks, 51 at 48, 98 at 192. **Every row assumes the effect is the one you measured**, so it tells you what twelve was never going to settle, not what more tasks would show — **arithmetic to do before the comparison and not after** |
| The rule against the measurement | Chapter 34's four columns said *a pattern, not an agent* in a minute on paper. A hundred and eight runs could not confirm it, and found a confound of their own instead |

### Review Questions

1. You measured a fixed path against an agent on the same task. What did you find?
2. Your agent succeeds on 47 per cent of trials and your workflow on 92. What do you check before
   believing it?
3. How do you make a comparison between two designs fair?
4. Your agent's total token count is lower than your workflow's. Is it cheaper?
5. The loop lost. Does that mean a loop is the wrong design for this kind of task?

### Review Answers

1. I took the one step our error analysis had named and could not check — a question whose answer
needs two documents — and built it as the pipeline we had and as a loop with a search tool. Twelve
tasks asserted to need two documents and to be answerable by neither alone, a code grader requiring
both values so half an answer fails, three trials each. **The loop came out 44 points worse**, 0.47
of trials against 0.92, with chapter 20's paired interval at −0.694 to −0.194. **And then I found
that I had built it with a smaller retrieval budget than the fixed path**, on an assumption about
how often it would search that turned out to be wrong — it searched once on 29 of 36 runs — so I
ran a third design, the same loop at the fixed path's budget. **The 44 points split into 28 of
budget and 17 of design, and neither half clears zero on twelve tasks.** So the only comparison in
the whole exercise with a verdict in it is the one that confounded the two things I was asking
about. What I can report is the diagnosis rather than the verdict: both loops write queries under
half the length of the question they are handed and lose requirements for it — 72 of 72 values
reached the fixed path against 63 and 54 — nine failures say in their own answer that something was
missing, eight of those nine after a single search; the fixed path costs 712 input tokens per
right answer against 1,213 and 1,315; and twelve tasks was never going to settle either isolated
question — at the differences these twelve measured, the design question needs about forty-eight
tasks for an even chance of a verdict. **Chapter 34's rule said *a pattern, not an
agent* in a minute on paper and the measurement could not confirm it**, which is the honest
sentence and the one I would lead with.
2. What the grader counted, what each design was *given*, and then whether the difference is one
difference. **The grader first**: read every failure, and where the key is wrong fix it, declare
the fix and report what it moved — on the first run of this lab that was three verdicts, all the
design that was already ahead, which is the direction that makes a late repair credible. **Then
what each design was given**, which is the check I would not now run a comparison without: for
every requirement a run missed, was the value in its passages? The fixed path had every one; the
loops had not, and that is a different kind of failure with a different fix. **Then whether the two
designs differ in one thing or two.** Mine differed in the design *and* the per-search budget, and
isolating them turned a 44-point verdict into two comparisons that cannot tell. **Then chapter 20's
interval**, paired, one task to a row with trials averaged within it, and resampling tasks — and if
it does not clear zero, resample to find out how many tasks would. **And then chapter 38's three
readings**, because 47 is one of three figures the same grid yields: this agent reads 0.47, 0.58 or
0.33, and pass@k is a capability only when something selects among the attempts, which nothing here
does.
3. By changing one thing, naming what you could not, and **printing what each design was given
beside its name**. These three share the corpus, the retrieval function, the ranking, the model and
snapshot, the temperature, the max tokens, the response format, the grader and the task set, and
the two instructions share their task sentence word for word — so neither design is told to answer
every part more clearly than the other. Then name the residue, because there always is one: a
design with a tool has to be told it has a tool. **And then look for the difference you did not
mean to introduce**, which is the one this chapter missed on its first pass: the per-search budget
differed, it was not a trade because the loop did not search twice, and it accounted for more of
the gap than the design did. The cheapest defence is a header line saying what each design gets —
the confound here survived a full run and a careful read of the output, and one printed line would
have caught it at a glance.
4. No, and the token total is the wrong column. The agent sent 22,363 input tokens against the
fixed path's 23,493 — genuinely fewer — because its per-search budget was smaller and it mostly
searched once. **Divide by the runs that passed and it is 1,315 against 712.** The wide agent, the
same loop at the fixed path's budget, sent 32,750 and costs 1,213 per passed run. So the design
that looks cheapest on the total is the one being starved, and **the total was measuring the
handicap rather than the design.** Two things to add before quoting any of it: chapter 53 owns cost
as a method and chapter 52's prefix caching means a re-sent prefix is cheaper to process than a
fresh one, so none of these is a bill; and chapter 34's arithmetic says a loop's token count has a
square in it as the run lengthens — these runs are two or three steps, so the quadratic never
arrives, and a loop that did use its freedom would cost more than this one rather than less.
5. It means the loop **as I built it** was worse, and that is a weaker claim than it sounds. Hold the
budget constant and twelve tasks cannot separate the loop from the fixed path, in the grade or in
the requirements each design was given. What makes the answer *a pattern* is not the measurement but
chapter 34's rule, whose first column decides it: the paths here can be enumerated — search,
possibly search again, answer — and the shape is the question's parts, which the rule maps to
parallelisation. **If you can write the paths down, a pattern runs them and you keep a known call
count, a reviewable shape and a predictable bill**, and a loop buys nothing you need. The
measurement's contribution is three things the rule cannot give you: the cost per success, the fact
that neither loop used the freedom it was built for, and the number of tasks it would take to answer
the design question properly. And it points at the design none of the three is: split the question,
search once per part, answer from both — the rung above a single call is a chain and parallelisation
is the fourth, and **this chapter started at the top and tried none of the rungs between.**

> **You understand this when** you can say which column of a design comparison is the only one that
> is a comparison, and why two designs that differ in two ways give you one verdict about neither.
