# Agent Patterns, and When an Agent Is Warranted

Chapter 4 said what an agent is — a system in which the model decides what to do next,
repeatedly — and that freedom is a dial rather than a switch, with a middle setting where your
code offers a short menu and the model picks. This chapter is that middle. It names the five
arrangements people build there, says what each is for, and then answers the question the word
*agent* makes hard to ask: when do you need the dial turned all the way up, and what does turning
it cost you?

*The problem.* Everything is called an agent. Mine loops forever and costs a fortune, so I'd like
to know when I even need one.

*The question.* Which of these designs does my problem need, and how would I know?

## Five Fixed Paths

A **fixed path** is a design in which the sequence lives in your code — your code runs every
step, whatever selected it, and the order they come in is written down. There
are five shapes worth having names for, and the names are worth having because they are what the
people you work with will say.

```python
"""The five fixed paths, as code, with a stub in place of the model.

`call` stands in for a model call. It returns a canned string and
counts itself, which is all this program needs: the question is who
decides what happens next, and how many calls that takes.

The task throughout is the same - turn a document into a one-line
headline - so the only thing changing between patterns is the shape
of the code around it.
"""

CALLS = []

def call(tag, text=""):
    """One model call. Returns something canned; records that it ran."""
    CALLS.append(tag)
    return {
        "classify":  "policy",
        "extract":   "refunds are issued within 14 days",
        "compress":  "Refunds in 14 days",
        "polish":    "Refunds issued within 14 days",
        "news":      "Refunds change announced",
        "policy":    "Refunds issued within 14 days",
        "map":       f"point from {text}",
        "reduce":    "Refunds issued within 14 days",
        "plan":      "intro|body|appendix",
        "write":     f"section {text}",
        "draft":     "Refund timing explained in detail at length",
        "judge":     "too long",
        "judge2":    "ok",
        "revise":    "Refunds issued within 14 days",
    }[tag]

DOC = ["chunk A", "chunk B", "chunk C"]

# ----------------------------------------------------- the five paths
def chaining():
    """Fixed sequence. Each call's output is the next call's input."""
    a = call("extract")
    b = call("compress", a)
    return call("polish", b)

def routing():
    """One call picks a branch from a menu YOUR CODE wrote. Your code
    then runs that branch - the model never reaches the branch table."""
    kind = call("classify")
    assert kind in ("news", "policy")
    return call(kind)

def parallelisation():
    """One call per piece, where the pieces come from the INPUT, then
    one call to put them together."""
    parts = [call("map", c) for c in DOC]
    return call("reduce", "".join(parts))

def orchestrator_workers():
    """One call decides what the pieces ARE, then one per piece, then
    one to combine. Your code still runs every step - but the number
    of steps came out of a model."""
    plan = call("plan").split("|")
    parts = [call("write", p) for p in plan]
    return call("reduce", "".join(parts))

def evaluator_optimiser(limit=3):
    """Produce, judge, revise, until the judge passes or your code
    gives up. Again your code runs the loop; the number of turns
    through it is decided at run time."""
    out = call("draft")
    for i in range(limit):
        verdict = call("judge" if i == 0 else "judge2")
        if verdict == "ok":
            return out
        out = call("revise")
    return out

#                                            what selects the next step
PATTERNS = [
    ("single call",          lambda: call("polish"), "nothing follows"),
    ("prompt chaining",      chaining,               "your code"),
    ("routing",              routing,                "a model's label"),
    ("parallelisation",      parallelisation,        "your code"),
    ("orchestrator-workers", orchestrator_workers,   "a model's plan"),
    ("evaluator-optimiser",  evaluator_optimiser,    "a judge's verdict"),
]

if __name__ == "__main__":
    print("  Every one of these is a fixed path: your code RUNS")
    print("  every step. What SELECTS the next one varies, which")
    print("  is the middle column, and the last column is the one")
    print("  that matters.\n")
    print("  pattern              calls  selected by      known?")
    rows = []
    for name, fn, decider in PATTERNS:
        CALLS.clear()
        fn()
        n = len(CALLS)
        # Known in advance when the call count depends only on the
        # input, not on anything a model returned.
        known = name not in ("orchestrator-workers",
                             "evaluator-optimiser")
        rows.append((name, n, known))
        print(f"  {name:21s}{n:4d}  {decider:17s}"
              f"{'yes' if known else 'NO':>5s}")

    known_n = sum(1 for _, _, k in rows if k)
    print(f"\n  Read the last column first. {known_n} of the {len(rows)}"
          f" have a call")
    print("  count you can work out before you run them: one,")
    print("  three, two, and one per chunk plus one. For those, the")
    print("  bill and the number of chances to go wrong are both")
    print("  written down in advance.\n")

    print("  The other two are the interesting ones, and they are")
    print("  usually filed alongside the first four as though they")
    print("  were the same kind of thing. In orchestrator-workers a")
    print("  MODEL decided there were three sections, so the call")
    print("  count came out of a model's answer. In")
    print("  evaluator-optimiser the loop runs until a judge is")
    print("  satisfied or your code gives up. Both are fixed in")
    print("  SHAPE and not in LENGTH.\n")

    unknown_n = len(rows) - known_n
    print("  That distinction is the chapter's first point. 'Your")
    print("  code controls the path' and 'you know what the run")
    print("  will cost' are two different properties, and")
    print(f"  {unknown_n} of these {len(rows)} have the first without"
          f" the second.")
    print("  Chapter 4's dial is about who decides; this column is")
    print("  about what you can predict.")
```

```text
  Every one of these is a fixed path: your code RUNS
  every step. What SELECTS the next one varies, which
  is the middle column, and the last column is the one
  that matters.

  pattern              calls  selected by      known?
  single call             1  nothing follows    yes
  prompt chaining         3  your code          yes
  routing                 2  a model's label    yes
  parallelisation         4  your code          yes
  orchestrator-workers    5  a model's plan      NO
  evaluator-optimiser     4  a judge's verdict   NO

  Read the last column first. 4 of the 6 have a call
  count you can work out before you run them: one,
  three, two, and one per chunk plus one. For those, the
  bill and the number of chances to go wrong are both
  written down in advance.

  The other two are the interesting ones, and they are
  usually filed alongside the first four as though they
  were the same kind of thing. In orchestrator-workers a
  MODEL decided there were three sections, so the call
  count came out of a model's answer. In
  evaluator-optimiser the loop runs until a judge is
  satisfied or your code gives up. Both are fixed in
  SHAPE and not in LENGTH.

  That distinction is the chapter's first point. 'Your
  code controls the path' and 'you know what the run
  will cost' are two different properties, and
  2 of these 6 have the first without the second.
  Chapter 4's dial is about who decides; this column is
  about what you can predict.
```

**Prompt chaining** is a sequence: each call's output is the next call's input. You use it when
the work has stages you can name — extract, then compress, then check the format — and each stage
is easier to get right asked on its own than asked all at once.

**Routing** is one call that picks a branch from a menu your code wrote, after which your code
runs that branch. (Chapter 52 uses the word for a different thing — sending a request to a
cheaper or a stronger model — and the two do not interfere.) The model sees the list of labels and never the code behind them, and that is
the point: adding a branch
is a code change you can review, not a sentence in an instruction you hope was read.

**Parallelisation** is one call per piece, where the pieces come from the input, then one call to
put the results together. The pieces are independent, so the calls can run at once and the whole
thing takes about as long as the slowest one.

**Orchestrator–workers** is parallelisation where a model decides what the pieces *are*. One call
produces a plan, your code runs one call per item in it, and a last call combines them.

**Evaluator–optimiser** is produce, judge, revise, until the judge is satisfied or your code gives
up. The judge is Chapter 31's, with everything that chapter said about establishing one before
believing it.

**The middle column is where the usual account goes wrong**: in three of the six, what selects
the next step is a model's output — a label, a plan, a verdict — and your code's job is to run
it. That is still a fixed path, because the sequence lives in code somebody can read.

**And then the column that matters, which is not the one the names suggest.** Four of the six designs
in the table have a call count you can work out before you run them. The last two do not:
orchestrator–workers because a model decided there were three sections, and evaluator–optimiser
because the loop runs until a judge passes. **They are fixed in shape and not in length.**

So "your code controls the path" and "you know what the run will cost" are two different
properties, and two of these six have the first without the second. Chapter 4's dial measures who
decides; this column measures what you can predict, and the two do not move together.

> **Note:** All five are often listed as *workflows* against *agents*, as though the line were
> between them and the loop. The line that does more work is the one in the table: whether the
> number of model calls is settled by your input or by something a model said. On that line,
> orchestrator–workers sits with the agent and not with the chain.

> **Tip:** The patterns compose, and most real systems are a composition. A router whose branches
> are chains; a chain with one parallelised stage; an orchestrator whose workers are single calls.
> Build the composition out of the shapes rather than reaching for the loop because the shape you
> need has no name yet.

## What a Loop Costs

Chapter 4 established the reliability side of the bill: errors compound across a run, and ten
steps at nine-in-ten is a run that works a third of the time. Here is the other side, which is
arithmetic about the design rather than about the model.

```python
"""What a loop costs against a fixed path of the same length.

Both designs make the same number of model calls. The difference is
what each call has to send. A fixed path hands one step's output to
the next; a loop re-sends everything that has happened so far,
because that is what lets the model decide what to do next.

Numbers chosen to be round, not measured: an instruction of 400
tokens, a question of 100, and 200 tokens added to the record by each
step - its decision plus whatever came back.
"""
INSTRUCTION, QUESTION, PER_STEP = 400, 100, 200

def fixed_path(n):
    """Each call sends the instruction, the question and the ONE
    output it is working from."""
    return sum(INSTRUCTION + QUESTION + (PER_STEP if i else 0)
               for i in range(n))

def loop(n):
    """Step i sends the instruction, the question and every step
    before it."""
    return sum(INSTRUCTION + QUESTION + PER_STEP * i for i in range(n))

if __name__ == "__main__":
    print("  Tokens sent across a whole run, both designs making the")
    print("  same number of calls.\n")
    print("   steps   fixed path        loop     loop / fixed")
    for n in (1, 2, 5, 10, 20, 40):
        f, l = fixed_path(n), loop(n)
        print(f"   {n:5d} {f:11,d} {l:11,d} {l/f:14.1f}")

    print("\n  The fixed path is a straight line: every call sends")
    print("  the same thing after the first, so the total grows in")
    print("  step with the number of calls. The loop does not,")
    print("  because the k-th")
    print("  step sends k-1 steps' worth of record, and adding")
    print("  those up puts a square in the total.\n")

    print("  What that means in practice is the row-to-row")
    print("  arithmetic, not the formula:")
    for a, b in ((10, 20), (20, 40)):
        print(f"    {a} steps to {b}: calls double,"
              f" tokens go up {loop(b)/loop(a):.1f} times")
    print("\n  So a step limit is not a cap on the bill in")
    print("  proportion to itself. Doubling the limit you are")
    print("  willing to pay for more than doubles what you might")
    print("  pay, and the worst case is the one that bills you.\n")

    print("  Two things this is NOT saying. It is not a cost model:")
    print("  chapter 53 owns that, and chapter 52's prompt-prefix")
    print("  caching makes a re-sent prefix much cheaper to process")
    print("  than a fresh one, so the PRICE does not rise with the")
    print("  token count the way this table does. What caching does")
    print("  not change is the count itself - and the count is what")
    print("  fills chapter 16's window, which is the wall the")
    print("  arithmetic runs into whatever the price per token.\n")

    window = 128_000
    budget = INSTRUCTION + QUESTION
    steps = 0
    while budget + PER_STEP * steps <= window:
        steps += 1
    print(f"  On a {window:,}-token window the record stops")
    print(f"  fitting at step {steps}. Which is the useful finding,")
    print("  and it is not the one people expect: a loop does not")
    print("  stop because it runs out of window - not at 200")
    print("  tokens a step. Chapter 4 cites a study in which 68")
    print("  per cent of deployed agents ran at most ten steps")
    print("  BEFORE A PERSON INTERVENED, which measures when")
    print(f"  people step in and not where a run would end. {steps} is")
    print("  nowhere near it either way.\n")
    print("  But turn the lever and the wall moves a long way:")
    for ps in (2_000, 10_000):
        s = 0
        while INSTRUCTION + QUESTION + ps * s <= window:
            s += 1
        print(f"    {ps:,} tokens a step: the wall is at step {s}")
    print("\n  A step that reads a long file, or a dozen retrieved")
    print("  passages, is thousands of tokens and not 200 - and at")
    print("  10,000 the wall lands just past the ten steps the")
    print("  study reports, instead of hundreds of steps away. So")
    print("  the window stops a TERSE loop at no useful point and")
    print("  a fat-stepped one in the range where step limits get")
    print("  set, and which you have is a measurement rather than")
    print("  a guess.\n")
    print("  What should BOUND a loop is the cost above and the")
    print("  compounding error chapter 4 works out. A loop does not")
    print("  stop FOR either of those - chapter 4 lists the three")
    print("  ways a run actually ends - so they are reasons to set")
    print("  a limit, which is the point.")
```

```text
  Tokens sent across a whole run, both designs making the
  same number of calls.

   steps   fixed path        loop     loop / fixed
       1         500         500            1.0
       2       1,200       1,200            1.0
       5       3,300       4,500            1.4
      10       6,800      14,000            2.1
      20      13,800      48,000            3.5
      40      27,800     176,000            6.3

  The fixed path is a straight line: every call sends
  the same thing after the first, so the total grows in
  step with the number of calls. The loop does not,
  because the k-th
  step sends k-1 steps' worth of record, and adding
  those up puts a square in the total.

  What that means in practice is the row-to-row
  arithmetic, not the formula:
    10 steps to 20: calls double, tokens go up 3.4 times
    20 steps to 40: calls double, tokens go up 3.7 times

  So a step limit is not a cap on the bill in
  proportion to itself. Doubling the limit you are
  willing to pay for more than doubles what you might
  pay, and the worst case is the one that bills you.

  Two things this is NOT saying. It is not a cost model:
  chapter 53 owns that, and chapter 52's prompt-prefix
  caching makes a re-sent prefix much cheaper to process
  than a fresh one, so the PRICE does not rise with the
  token count the way this table does. What caching does
  not change is the count itself - and the count is what
  fills chapter 16's window, which is the wall the
  arithmetic runs into whatever the price per token.

  On a 128,000-token window the record stops
  fitting at step 638. Which is the useful finding,
  and it is not the one people expect: a loop does not
  stop because it runs out of window - not at 200
  tokens a step. Chapter 4 cites a study in which 68
  per cent of deployed agents ran at most ten steps
  BEFORE A PERSON INTERVENED, which measures when
  people step in and not where a run would end. 638 is
  nowhere near it either way.

  But turn the lever and the wall moves a long way:
    2,000 tokens a step: the wall is at step 64
    10,000 tokens a step: the wall is at step 13

  A step that reads a long file, or a dozen retrieved
  passages, is thousands of tokens and not 200 - and at
  10,000 the wall lands just past the ten steps the
  study reports, instead of hundreds of steps away. So
  the window stops a TERSE loop at no useful point and
  a fat-stepped one in the range where step limits get
  set, and which you have is a measurement rather than
  a guess.

  What should BOUND a loop is the cost above and the
  compounding error chapter 4 works out. A loop does not
  stop FOR either of those - chapter 4 lists the three
  ways a run actually ends - so they are reasons to set
  a limit, which is the point.
```

**A fixed path and a loop can make the same number of calls and not cost the same**, because they
do not send the same thing. A chain hands one step's output to the next. A loop re-sends
everything that has happened so far — it has to, because that record is what the model reads in
order to decide what to do next. Add those up and the total has a square in it.

**The row-to-row arithmetic is the part to carry.** Going from ten steps to twenty doubles the
calls and multiplies the tokens by 3.4. Twenty to forty doubles them again and multiplies by 3.7.
**So a step limit does not cap the bill in proportion to itself**: doubling the limit you are
willing to pay for more than doubles what you might pay, and the worst case is the one that bills
you.

**Two things this is not.** It is not a cost model — Chapter 53 owns that — and Chapter 52's
prompt-prefix caching makes a re-sent prefix much cheaper to process than a fresh one, so the
*price* does not rise the way the token count does. What caching does not change is the count.

**And the count runs into a wall that is further away than people think.** On a
128,000-token window and these numbers, the record stops fitting at step 638. Chapter 4 cites a
study in which 68 per cent of deployed agents ran at most ten steps *before a person
intervened* — which measures when people step in, not where an unsupervised run would end, so it
makes the point about supervision rather than about windows.

**And the wall moves a long way when you turn the one lever that decides it.** At 2,000 tokens a
step it is step 64; at 10,000 — a step that reads a long file, or a dozen retrieved passages — it
is step 13, which is just past the ten steps the study reports instead of hundreds of steps away.
**So the window stops a terse loop at no useful point and a fat-stepped one in the range where
step limits are actually set**, and which you have is a measurement rather than a guess.
What should *bound* a loop is the cost above and Chapter 4's compounding error; a loop does not
*stop* for either, because Chapter 4 lists the three ways a run actually ends.

> **Warning:** The quadratic is why a loop that is *nearly* working is the expensive kind. A run
> that finishes in four steps sends 3,200 tokens on these numbers; the same loop failing its way
> to a step limit of thirty sends 102,000, which is thirty-two times as much. So the runs you learn least from are the ones
> you pay most for, and a step limit you picked without arithmetic is a number you will meet on
> an invoice.

## When an Agent Is Warranted

The patterns answer *which fixed path*. This answers whether you need one at all.

```python
"""When an agent is warranted, worked on nine real-sounding tasks.

Four columns, recorded by a person who thought about each task for a
minute. `paths` is whether you can write down in advance the
sequences the work might take. `check` is whether a wrong result can
be caught cheaply. `undo` is whether a wrong step can be reversed.
`shape` is what the work looks like. A shape can be known even when the
sequences are not: *pieces a model names* is the orchestrator's case,
where you know the work splits and only a model can say into what.

The verdicts are computed from those columns, so the rule is visible
rather than asserted.
"""

#                                       paths  check   undo   shape
TASKS = [
    ("summarise each of 200 documents",  True,  True,  True, "pieces"),
    ("answer a support question",        True,  True,  True, "sequence"),
    ("route a ticket to one of five",    True,  True,  True, "one of a few"),
    ("write a release note",             True,  True,  True, "pieces"),
    ("redraft a reply until it fits",    True,  True,  True, "until good"),
    ("find why one order is late",      False,  True,  True, "-"),
    ("reconcile a month, post fixes",   False,  True, False, "-"),
    ("choose which supplier to pay",    False, False, False, "-"),
    ("write a report on a topic",       False,  True,  True,
     "pieces a model names"),
]

PATTERN = {
    "pieces":       "parallelise",
    "sequence":     "chain",
    "one of a few": "route",
    "until good":   "evaluator-optimiser",
    "pieces a model names": "orchestrator-workers",
}

def verdict(paths, check, undo, shape):
    """The rule. The check is asked about only where the paths
    cannot be written down - a scope worth noticing rather than a
    hole: an unchecked FIXED path is a bad idea too, and it is a bad
    idea the same way an unchecked single call is. What the check
    vetoes here is letting a model choose outside a list your code
    wrote."""
    if paths:
        return PATTERN[shape]
    if shape in PATTERN:
        return PATTERN[shape] if check else "not warranted"
    if not check:
        return "not warranted"
    if not undo:
        return "agent + approval point"
    return "agent"

if __name__ == "__main__":
    print("  task                            paths check undo")
    for name, paths, check, undo, shape in TASKS:
        print(f"  {name:32s}"
              f" {'y' if paths else 'n':^5s}"
              f" {'y' if check else 'n':^5s}"
              f" {'y' if undo else 'n':^4s}".rstrip())

    print("\n  The verdict each one gets:\n")
    for name, *props in TASKS:
        print(f"    {name:32s} {verdict(*props)}")

    pat = [t for t in TASKS if verdict(*t[1:]) in PATTERN.values()]
    agents = [t for t in TASKS if verdict(*t[1:]).startswith("agent")]
    none = [t for t in TASKS if verdict(*t[1:]) == "not warranted"]
    assert len(pat) + len(agents) + len(none) == len(TASKS)
    print(f"\n  {len(pat)} get a pattern, {len(agents)} get an agent,"
          f" {len(none)} neither.\n")

    print("  The report is the row worth pausing on. Its paths")
    print("  column is 'n' - only a model can say what the")
    print("  sections are - and it still gets a pattern, because")
    print("  the SHAPE is known even though the sequences are not.")
    print("  That is what an orchestrator is, and it is why 'a")
    print("  model chooses something' and 'you need a loop' are")
    print("  not the same question.\n")
    print("  The first column does most of the work, and it is the")
    print("  only one that can make a LOOP necessary. If you can")
    print("  write the paths down, a pattern runs them and you")
    print("  keep what a fixed path gives you. You cannot write")
    print("  them down for the late order, because what you do")
    print("  third depends on what the second system said and there")
    print("  are more combinations than anybody would enumerate.\n")

    print("  The second column is a veto rather than a reason.")
    print("  Nothing in the first column makes an agent safe to")
    print("  use; the check does. An agent whose output nobody can")
    print("  check produces confident work of unknown quality,")
    print("  which is why the supplier task comes out as neither:")
    print("  it is a judgement, and it belongs to a person for")
    print("  reasons that are not technical.\n")

    print("  The third column does not decide whether to use an")
    print("  agent. It decides whether a person has to be in the")
    print("  loop, which is chapter 4's approval point and which")
    print("  goes in your code.\n")

    print("  Notice what is NOT a column. How hard the task is,")
    print("  how good the model is, whether anybody would be")
    print("  impressed. The questions are whether the paths can")
    print("  be written down, whether the shape can be even if")
    print("  they cannot, and whether you would know if the answer")
    print("  were wrong.")
```

```text
  task                            paths check undo
  summarise each of 200 documents    y     y    y
  answer a support question          y     y    y
  route a ticket to one of five      y     y    y
  write a release note               y     y    y
  redraft a reply until it fits      y     y    y
  find why one order is late         n     y    y
  reconcile a month, post fixes      n     y    n
  choose which supplier to pay       n     n    n
  write a report on a topic          n     y    y

  The verdict each one gets:

    summarise each of 200 documents  parallelise
    answer a support question        chain
    route a ticket to one of five    route
    write a release note             parallelise
    redraft a reply until it fits    evaluator-optimiser
    find why one order is late       agent
    reconcile a month, post fixes    agent + approval point
    choose which supplier to pay     not warranted
    write a report on a topic        orchestrator-workers

  6 get a pattern, 2 get an agent, 1 neither.

  The report is the row worth pausing on. Its paths
  column is 'n' - only a model can say what the
  sections are - and it still gets a pattern, because
  the SHAPE is known even though the sequences are not.
  That is what an orchestrator is, and it is why 'a
  model chooses something' and 'you need a loop' are
  not the same question.

  The first column does most of the work, and it is the
  only one that can make a LOOP necessary. If you can
  write the paths down, a pattern runs them and you
  keep what a fixed path gives you. You cannot write
  them down for the late order, because what you do
  third depends on what the second system said and there
  are more combinations than anybody would enumerate.

  The second column is a veto rather than a reason.
  Nothing in the first column makes an agent safe to
  use; the check does. An agent whose output nobody can
  check produces confident work of unknown quality,
  which is why the supplier task comes out as neither:
  it is a judgement, and it belongs to a person for
  reasons that are not technical.

  The third column does not decide whether to use an
  agent. It decides whether a person has to be in the
  loop, which is chapter 4's approval point and which
  goes in your code.

  Notice what is NOT a column. How hard the task is,
  how good the model is, whether anybody would be
  impressed. The questions are whether the paths can
  be written down, whether the shape can be even if
  they cannot, and whether you would know if the answer
  were wrong.
```

**The first column is the only one that can make an agent necessary.** If you can write the paths
down, a pattern runs them and you keep everything a fixed path gives you — a known
call count, a reviewable branch table, a bill you can predict. You cannot write them down for the
late order, because what you do third depends on what the second system said, and the
combinations outrun anybody's patience for enumerating them.

**The second column is a veto rather than a reason**, and what it vetoes is letting a model
choose outside a list your code wrote. Nothing in the first column makes an agent safe to use;
the check does. Note the scope, because the rule only asks about the check where the paths cannot
be written down: an unchecked fixed path is
also a bad idea, and it is a bad idea in the ordinary way an unchecked single call is, which this
rule does not price. An agent whose output nobody can check produces confident work of
unknown quality at a cost you cannot predict, which is the arrangement the rule exists to refuse.
That is why the supplier task comes out as neither: it is a judgement, and it belongs to a person for
reasons that are not technical.

**The third column decides something different.** It does not change whether to use an agent — it
changes whether a person has to be in the loop, which is Chapter 4's approval point and which
lives in your code. **And the fourth is the shape**: paths you cannot enumerate still get a
pattern when you know the work splits and only a model can say into what, which is an
orchestrator. On nine tasks that fourth column is what keeps one of them out of the agent column
altogether.

**And notice what is not a column.** How hard the task is, how good the model is, whether anybody
would be impressed. Those are the reasons people actually reach for an agent, and none of them
appears in a rule that works.

> **Note:** "You cannot write the paths down" is a claim about *you and this task today*, not a
> permanent property. The commonest honest version of it is that you could enumerate the paths
> and there are forty of them, most of which happen twice a year. An agent is then a way of not
> writing thirty-eight branches — a real reason, and a different one from the task being
> impossible to specify. It also means that as you learn the task, branches you once called
> unenumerable become a router, which is the direction this usually travels.

## Start With the Simplest Thing That Works

Chapter 4's conclusion was the least freedom that solves the problem. The practical form of it is
an order to try things in. It is close to the first section's table read top to bottom, and the
difference is worth naming: it is an order of *added machinery*, not of freedom. Routing gives
the model more say than parallelisation does, and sits above it here because a router is less
machinery, not because it is more cautious.

**One call first.** A good many tasks people reach for an agent on are one call with a better
instruction, and Chapter 18 is the whole of what *better* means. The test is not whether a single
call is elegant; it is whether it passes your evaluation set.

**Then a chain, if the work has named stages.** Each stage asked on its own is easier than the
whole thing asked at once, and you get a place to put a check between them.

**Then a router, if the input arrives in kinds.** Branches in code are cheaper to get right than
branches in prose.

**Then parallelisation, if the pieces are independent.** This is the one people skip, and it is
often what the thing they were calling an agent actually needed.

**Then an orchestrator, if a model has to decide what the pieces are** — knowing you have given
up a predictable call count to get it.

**Then an evaluator–optimiser, if what you need is another attempt rather than another stage** —
and with a limit, which is the whole of what keeps it a pattern.

**Then, and only then, a loop** — if the paths cannot be written down and there is a check.

> **Tip:** The cheapest way to find out which rung you need is to climb from the bottom and stop
> when your evaluation set passes. The expensive way is to start at the top, because a loop that
> works tells you nothing about whether a chain would also have worked — and you will not go back
> and find out.

## What To Actually Do

1. **Write down whether you can enumerate the paths.** If you can, you are choosing between five
   patterns and not deciding whether to build an agent.
2. **Write down the check.** What would tell you the result is wrong, and what it costs to run. No
   check means no agent, whatever the first answer was.
3. **Write down whether a wrong step can be undone.** If it cannot, the design needs an approval
   point before it needs anything else.
4. **Pick the lowest pattern that fits** — one call, chain, router, parallelise, orchestrator,
   evaluator–optimiser, loop — and run your evaluation set on it before climbing.
5. **For every design, work out the call count.** If you cannot, you have an orchestrator, an
   evaluator–optimiser or a loop, and you should know which.
6. **Do the token arithmetic for the step limit you are considering**, not for the typical run.
   The worst case is what you will be billed for.
7. **Set the step limit from that arithmetic** and log every run that hits it, which is Chapter
   4's instruction and the reason this one is cheap to follow.
8. **Compose rather than escalate.** A router of chains is a fixed path. Reaching for a loop
   because your shape has no name is how the predictable properties get thrown away.
9. **Re-ask the first question as you learn the task.** Paths you could not enumerate in month one
   are often a router by month six.
10. **Keep the comparison.** When you climb a rung, keep the result of the one below, because
    "the loop works" is not evidence that the chain did not.

> **Warning:** Steps 1 to 3 are a sheet of paper and they decide the architecture. Most of the
> expensive agent projects described in practitioner reports commonly start by skipping them, and
> the tell is that nobody can say what the check is.

## Lab: Six Shapes and a Decision

Three programs, pure Python, nothing to install. About forty-five minutes, and there is a key for
every step. Work in a new empty folder. None imports another:

| Save as | Which block |
|---|---|
| `patterns.py` | the first |
| `cost.py` | the second |
| `warranted.py` | the third |

**Step 1.** Save `patterns.py` and run it. Read the six functions before the output; each is four
lines or fewer.

*Expected result:* call counts of 1, 3, 2, 4, 5 and 4, with the last two marked `NO` in the
known-before-the-run column.

**Step 2.** Give the orchestrator more work: change `"plan"` in `call`'s table to return
`"intro|body|appendix|index|notes"`.

*Expected result:* orchestrator–workers goes from 5 calls to 7, and nothing else moves. **The call
count of a fixed path changed because a canned model answer changed**, which is the whole of what
the `NO` column means.

**Step 3.** Put it back. Now make the evaluator stubborn: change `"judge2"` to return
`"too long"`.

*Expected result:* evaluator–optimiser goes from 4 calls to 7 — the limit of 3 revisions, each
with a judge call, plus the draft. The pattern did not change and the cost doubled, decided by a
judge rather than by your code.

**Step 4.** Keep step 3's stubborn judge, and now take the guard away: change
`for i in range(limit):` to `while True:`, and the line below it to `verdict = call("judge")`.

*Expected result:* it does not return. Leave it a few seconds and stop it. **A judge that never
passes and a loop with no limit is a pattern that does not terminate**, and `limit=3` is the
whole of what stood between them — which is why step 3, with the same stubborn judge and the
limit left in, finished at 7 calls. Put both edits back.

**Step 5.** Save `cost.py` and run it. Then change `PER_STEP` from 200 to 50 — a terser agent,
same number of steps.

*Expected result:* the loop-to-fixed ratio at 40 steps falls from 6.3 to 2.7, and the window wall
moves from step 638 to 2,551. **The quadratic is in the record you accumulate, not in the
loop**, which is why Chapter 35's compaction is a lever on cost and not only on fitting.

**Step 6.** Put it back and set `INSTRUCTION` to 4,000 — a long system prompt, which is the
commonest real shape.

*Expected result:* the ratio at 40 steps falls to 1.9, because a large fixed prefix dominates both
designs. A loop's extra cost is only visible when the per-step record is large next to the
instruction, and this is where Chapter 52's prefix caching does the most for you.

**Step 7.** Put it back, then turn the lever the other way: set `PER_STEP` to 10,000 — one step
that reads a long file or a dozen retrieved passages.

*Expected result:* the window wall moves from step 638 to *step 13*, which is inside the
ten-step picture the chapter quotes. **This is the step that decides whether the section's
conclusion holds for your loop**, and it is the one the other two do not reach: at 200 tokens a
step the window never stops you, and at 10,000 it is in the same range as the step limits people
actually set.

**Step 8.** Save `warranted.py` and run it. Then change the late-order task's `check` to `False`.

*Expected result:* its verdict changes from `agent` to `not warranted`. One column, and the task
that most obviously wanted an agent stops qualifying.

**Step 9.** Change the supplier task's `paths` to `True` and give it the shape `"one of a few"`.

*Expected result:* `route`. **A task with no check and no undo now gets a pattern**, because the
rule asks about the check only where the paths cannot be written down. That is a scope and not a
hole: an
unchecked router is a bad idea for the ordinary reason an unchecked single call is, and this rule
is about whether to hand over the choosing. What it does mean is that passing the rule is not a
licence: step 2 of *What To Actually Do* asks for the check whatever the first answer was.

**Step 10.** Add a task of your own with `paths=False`, `check=True`, `undo=True` and
`shape="-"` — five fields, because the shape column is one of them.

*Expected result:* `agent`. Then write one sentence saying what the check actually is. If you
cannot, change `check` to `False` and read the verdict again.

**Step 11.** Take a task somebody has described to you as needing an agent and fill in the four
columns.

*Expected result:* most of the time, a pattern. The useful outcome is the second column being
blank, because that is a conversation to have before any of the rest.

## Summary, Key Terms, and Review Questions

### Summary

Chapter 4's dial has a middle, and this chapter names the five arrangements people build there.
**Prompt chaining** is stages in sequence, each easier asked alone. **Routing** is one call
picking from a menu your code wrote, so adding a branch is a reviewable code change rather than a
sentence in an instruction. **Parallelisation** is one call per piece with the pieces from the
input, and a call to combine. **Orchestrator–workers** is that, with a model deciding what the
pieces are. **Evaluator–optimiser** is produce, judge, revise, until a judge passes or your code
gives up — with Chapter 31's warnings about the judge attached.

**The distinction worth more than the names is which designs have a call count you can work out
before you run them.** Four of the chapter's six do; orchestrator–workers and
evaluator–optimiser do not, because a model decides how many pieces there are and a judge decides
when to stop. **They are fixed in shape and not in length**, so "your code controls the path" and
"you know what the run will cost" are two different properties and two of six have the first
without the second.

**A loop's price is arithmetic about the design.** A fixed path hands one output forward; a loop
re-sends everything, because that record is what the model reads to decide. Add it up and the
total has a square in it: ten steps to twenty doubles the calls and multiplies tokens by 3.4,
twenty to forty by 3.7. **A step limit does not cap the bill in proportion to itself.** Chapter 53
owns cost as a method and Chapter 52's prefix caching makes the re-sent prefix cheap to process,
so the price does not track the count — but the count is real, and on a 128,000-token window it
stops fitting at step 638 — but only at 200 tokens a step. At 10,000, which is what a step that
reads a long file costs, the wall is at step 13 — just past the ten steps the study reports.
**So the window stops a terse loop at no useful point and a fat-stepped one in the range where
step limits are actually set**, and which you have is a measurement. Chapter 4's study has 68 per
cent of deployed agents running at most ten steps *before a person intervened*, which is about
supervision rather than windows. What should *bound* a loop is the cost and Chapter 4's
compounding error — a loop does not *stop* for either, since Chapter 4 lists the three ways a run
ends.

**Whether an agent is warranted comes down to four columns and two of them are not what people
expect.** Can you enumerate the paths — the only column that can make an agent *necessary*. Is
there a cheap check — a veto rather than a reason, because nothing makes an agent safe except
being able to tell when it was wrong. Can a wrong step be undone — which decides whether a person
has to be in the loop, not whether to build the agent. **What is not a column:** how hard the task
is, how good the model is, whether anybody would be impressed. On nine tasks the rule gives six
patterns, two agents and one that belongs to a person.

**And the order to try things in is close to the table read top to bottom, as an order of added
machinery rather than of freedom** — one call, chain, router, parallelise, orchestrator,
evaluator–optimiser, loop — climbing only when the evaluation set fails. Starting at the top
is expensive twice over: once in tokens, and once because a loop that works tells you nothing
about whether a chain would have worked, and nobody goes back to find out.

### Key Terms

| Term | Meaning |
|---|---|
| **Fixed path** | A design in which the sequence lives in your code: your code runs every step, whatever selected it, and the order is written down rather than decided as the run goes. Five shapes: chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser |
| **Prompt chaining** | Stages in sequence, each call's output the next one's input. Used when the work has nameable stages that are easier asked separately |
| **Routing** | One call picks a branch from a menu your code wrote; your code runs the branch. The model sees the labels and never the code behind them. Chapter 52's routing is a different thing — choosing between models for one request |
| **Parallelisation** | One call per piece, the pieces coming from the input, then one call to combine. Independent, so they can run at once |
| **Orchestrator–workers** | Parallelisation where a model decides what the pieces are, so the call count is settled at run time |
| **Evaluator–optimiser** | Produce, judge, revise, until the judge passes or your code gives up. Fixed in shape, not in length |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The five fixed paths | Chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser |
| The column that matters | Whether the call count is settled by your input or by something a model said. 4 of the chapter's 6 designs, not 6 |
| Which patterns are not fixed in length | Orchestrator–workers and evaluator–optimiser — a model decides the pieces, a judge decides when to stop |
| Why a loop costs more than a chain of the same length | It re-sends the whole record each step, so the total has a square in it |
| The step-limit arithmetic | 10 steps to 20 doubles the calls and multiplies tokens by 3.4; 20 to 40 by 3.7 |
| Where the window wall is | On a 128,000-token window: step 638 at 200 tokens a step, step 13 at 10,000. The window stops a terse loop nowhere useful and a fat-stepped one in the range where step limits are set |
| When an agent is warranted | You cannot enumerate the paths **or the shape** — if the shape is one of the five you have a pattern, not an agent — **and** there is a cheap check. The second is a veto on letting a model choose outside a list your code wrote, not a reason for it |
| What decides the approval point | Whether a wrong step can be undone — not whether to use an agent |
| The order to try | One call, chain, router, parallelise, orchestrator, evaluator–optimiser, loop. An order of added machinery, not of freedom. Climb when the evaluation set fails |

### Review Questions

1. When is an agent warranted instead of a path your code controls?
2. Name the fixed-path patterns and say what each is for.
3. Two of the five patterns are usually listed with the others and behave differently. Which, and
   how?
4. Your agent's step limit is 30 and the finance team wants the bill halved. What do you tell
   them?
5. Somebody proposes replacing a working router with an agent, because the router has grown to
   twelve branches. What do you ask?

### Review Answers

1. When you cannot enumerate the paths the work might take **or even the shape of the work**, and
there is a cheap check on the result. The shape clause is the one people miss: if you know the
work splits into pieces and only a model can say into what, that is an orchestrator and not an
agent. The other two halves do different jobs, and getting that wrong is the commonest mistake. The first
is the only condition that can make an agent *necessary*: if you can write the paths down, one of
the five patterns runs them and you keep a known call count, a branch table somebody can review,
and a bill you can predict. The second is a **veto rather than a reason** — nothing about
unenumerable paths makes an agent safe, and an agent whose output nobody can check produces
confident work of unknown quality at a cost you cannot predict, which is the worst arrangement
available. A third question decides something else: if a wrong step cannot be undone, the design
needs Chapter 4's approval point, and that is independent of whether to use an agent at all. Two
details show the rule has been used rather than recited. What is *not* in it: how hard the task
is, how good the model is, whether anybody would be impressed — which are the reasons people
actually reach for one. And "cannot enumerate the paths" is a claim about you and this task today:
the honest version is often that you could enumerate forty paths, most of which happen twice a
year, so the agent is a way of not writing thirty-eight branches. That is a real reason and a
different one, and it means the answer changes as you learn the task.
2. Five, and each is a different answer to "what does my code do after the call?" **Prompt
chaining** is a sequence, each call's output feeding the next; it is for work with nameable
stages, because a stage asked on its own is easier to get right than the whole thing asked at
once, and you get somewhere to put a check between them. **Routing** is one call that picks a
branch from a menu your code wrote, after which your code runs the branch — the model never sees
the branch table, so adding a branch is a code change somebody reviews rather than a sentence in
an instruction you hope was read. **Parallelisation** is one call per piece with the pieces coming
from the input, then one call to combine; the pieces are independent, so the calls run at once and
the whole takes about as long as the slowest. **Orchestrator–workers** is parallelisation in which
a model decides what the pieces are: one call plans, one runs per item, one combines.
**Evaluator–optimiser** is produce, judge, revise, until the judge is satisfied or your code gives
up, with everything Chapter 31 said about establishing a judge before believing it. They compose,
and most real systems are a composition — a router whose branches are chains, a chain with one
parallelised stage — which is worth saying because reaching for a loop when your shape has no
name is how the predictable properties get thrown away.
3. **Orchestrator–workers and evaluator–optimiser**, and the difference is that their call count
is not settled before the run. In the chapter's table four of six designs have a count you can
work out in advance — one, three, two, and one per chunk plus one — while the orchestrator's count
came out of a model's plan and the evaluator–optimiser's came out of a judge deciding when to
stop. **They are fixed in shape and not in length.** That matters because "your code controls the
path" and "you know what the run will cost" are two different properties, and these two have the
first without the second: your code still runs every step and still decides when to give up, but
the bill and the number of chances to go wrong are decided at run time. The lab makes it concrete
in one edit — change the canned plan from three sections to five and the orchestrator goes from 5
calls to 7 with no code touched, and make the judge stubborn and the evaluator–optimiser goes from
4 to 7. So the line usually drawn between *workflows* and *agents* puts these two on the wrong
side; the line that does more work is whether a model's answer sets the number of calls, and on
that line the orchestrator sits with the loop.
4. That halving the limit does rather more than halve the bill, and that the number to look at is
the worst case rather than the typical run. A loop re-sends its whole record every step, so the
tokens across a run have a square in them: on the chapter's numbers, going from twenty steps to
forty doubles the calls and multiplies the tokens by 3.7, so the reverse is also true and cutting
the limit from thirty buys more than it looks like. Then two things to put beside it before
anybody decides. Chapter 52's prompt-prefix caching makes a re-sent prefix much cheaper to process
than a fresh one, so the *price* does not rise the way the token count does, and the saving from a
lower limit is smaller than the token table suggests; Chapter 53 owns the arithmetic that turns
one into the other. And the runs that hit the limit are the expensive ones that taught you least,
so the right question is not only "what limit" but "which tasks are hitting it" — Chapter 4's
instruction to log every run that hits the limit is what makes that answerable. Lastly, the
cheapest halving may not be the limit at all: if the per-step record is large next to the
instruction, Chapter 35's compaction cuts the quadratic term directly, and if the paths turn out
to be enumerable the right answer is a pattern rather than a smaller loop.
5. Whether the twelve branches are hard to *maintain* or hard to *choose between* — because the
answer points in opposite directions. Twelve branches in code is not a problem an agent solves;
it is twelve things somebody can read, review and test, and replacing them with a loop trades all
of that for a call count nobody can predict. The chapter's rule asks whether the paths can be
enumerated, and twelve enumerated branches is the clearest possible yes. So the first question is
what is actually going wrong. If the *classifier* is picking the wrong branch, that is a routing
problem with a measurement attached — Chapter 30's error analysis on the misroutes, and the fix is
probably the menu or the instruction rather than the architecture. If the branches have grown
because the work genuinely has forty paths and twelve of them were worth writing, that is the
honest case for a loop, and then the second column decides it: what is the check, and what does it
cost to run? And if the answer is that the router is fine but the team wants to say they have an
agent, the arithmetic in this chapter is the reply — a predictable bill and a reviewable branch
table are what is being given up, and nothing is being bought.

> **You understand this when** you can say which two of the five patterns have a cost you cannot
> predict, and give the two conditions an agent needs without naming the model.
