# Multi-Agent Systems

A **multi-agent system** is one in which several agents run on one task — each with its own
context and its own stopping condition, as Chapter 35's sub-agent has — with your code or one of
them coordinating. Chapter 35 sent two things here: dividing a problem among specialists, and
the arithmetic on running several sub-agents at once. Both turn out to rest on one question asked before either of
them, and this chapter asks it first. Then it prices the answer, which goes the opposite way
from the story everybody tells. Then it says what the evidence on all of this actually is, which
is less than you will hear and more interesting than nothing.

*The problem.* Five agents sounded better than one. It cost six times as much and finished
nothing.

*The question.* When do several agents help, how do they fail, and what does a multi-agent
system actually cost?

## Does the Work Come Apart?

Everything else in this chapter depends on this, and it is answerable with a pencil before any
code exists.

```python
"""Which work splits, and which only looks as though it does.

Chapter 34 owns parallelisation and orchestrator-workers as fixed
paths; chapter 35 owns the sub-agent. This asks the question before
either of them: does the work come apart at all?

Each task below is written as pieces with the pieces each one needs
first. That part is a judgement about the task. Everything after it
is computed: the longest chain through the dependencies is the
shortest the task can take however many agents you have.

One assumption, and it matters for the middle rows. Pieces divided
by chain is a count, and reading it as a speed-up needs the pieces
to be of roughly similar size. The two tasks that score 1.0 are
right whatever the sizes - a chain is a chain - but a 2.0 could be
3.0 or 1.2 if one piece dominates the rest.
"""
TASKS = {
    "summarise 8 documents": {
        f"doc{i}": [] for i in range(1, 9)
    },
    "triage 20 tickets": {
        f"t{i}": [] for i in range(1, 21)
    },
    "research 5 sources, then reconcile": {
        "s1": [], "s2": [], "s3": [], "s4": [], "s5": [],
        "reconcile": ["s1", "s2", "s3", "s4", "s5"],
    },
    "write a report with 4 sections": {
        "outline": [],
        "sec1": ["outline"], "sec2": ["outline"],
        "sec3": ["outline"], "sec4": ["outline"],
        "join": ["sec1", "sec2", "sec3", "sec4"],
    },
    "refactor a module, then fix its tests": {
        "refactor": [], "tests": ["refactor"],
    },
    "plan a trip": {
        "dates": [], "flights": ["dates"],
        "hotel": ["flights"], "dinner": ["hotel"],
    },
}


def depth(piece, deps, seen=None):
    """The number of pieces in the longest chain ending at this one,
    counting itself. Not how many must finish first: `join` below
    has five prerequisites and a depth of 3."""
    seen = seen or set()
    assert piece not in seen, f"cycle at {piece}"
    if not deps[piece]:
        return 1
    return 1 + max(depth(d, deps, seen | {piece}) for d in deps[piece])


def width(deps):
    """The most pieces that can be in flight at once: the largest
    number sharing one level of the graph."""
    at = {}  # pieces grouped by the level they sit at
    for piece in deps:
        at.setdefault(depth(piece, deps), []).append(piece)
    return max(len(v) for v in at.values())


def table():
    print("  Six tasks, written as pieces and what each needs")
    print("  first. The longest chain is the shortest the task")
    print("  can take, however many agents you have.\n")
    print("  task                        pieces chain width  up")
    rows = []
    for name, deps in TASKS.items():
        n = len(deps)
        chain = max(depth(p, deps) for p in deps)
        w = width(deps)
        rows.append((name, n, chain, w, n / chain))
        short = name if len(name) <= 27 else name[:26] + "\u2026"
        print(f"  {short:<28}{n:>6}{chain:>6}{w:>6}{n / chain:>5.1f}")
    return rows


def verdicts(rows):
    print("\n  The last column is pieces divided by chain: how much")
    print("  of the work could be happening at once. It is the")
    print("  column that answers the question.\n")
    for name, n, chain, w, sp in rows:
        v = ("splits" if sp >= 4 else
             "splits in part" if sp > 1.5 else "DOES NOT SPLIT")
        print(f"    {sp:>4.1f}x  {v:<15}{name}")
    good = [r for r in rows if r[4] >= 4]
    bad = [r for r in rows if r[4] <= 1.5]
    print(f"\n  {len(good)} of {len(rows)} split well, "
          f"{len(bad)} not at all. And the two that do")
    print("  not have the same shape: every piece needs the one")
    print("  before it, so the chain IS the task and a second agent")
    print("  has nothing to do until the first has finished.")


def cost(rows):
    print("\n  Now the part that makes a wrong answer expensive.")
    print("  You pay for agents, not for speed-up. One agent a")
    print("  piece is what people reach for; the number that")
    print("  earns its place is the width.\n")
    print("  task                        one each  paid   width  paid")
    for name, n, chain, w, sp in rows:
        short = name if len(name) <= 27 else name[:26] + "\u2026"
        print(f"  {short:<28}{n:>8}{n / sp:>6.1f}x{w:>7}"
              f"{w / sp:>6.1f}x")
    worst = max(rows, key=lambda r: r[1] / r[4])
    print(f"\n  Paid is agents divided by speed-up: what one unit of")
    print("  parallelism cost you. At 1.0 every agent earned its")
    print(f"  place. {worst[0]} is the worst of the six at")
    print(f"  {worst[1] / worst[4]:.1f} times: {worst[1]} agents and no speed-up"
          f" at all. And")
    print("  the right column is the same six tasks with the agents")
    print("  the shape actually supports.")


if __name__ == "__main__":
    r = table()
    verdicts(r)
    cost(r)
```

```text
  Six tasks, written as pieces and what each needs
  first. The longest chain is the shortest the task
  can take, however many agents you have.

  task                        pieces chain width  up
  summarise 8 documents            8     1     8  8.0
  triage 20 tickets               20     1    20 20.0
  research 5 sources, then r…      6     2     5  3.0
  write a report with 4 sect…      6     3     4  2.0
  refactor a module, then fi…      2     2     1  1.0
  plan a trip                      4     4     1  1.0

  The last column is pieces divided by chain: how much
  of the work could be happening at once. It is the
  column that answers the question.

     8.0x  splits         summarise 8 documents
    20.0x  splits         triage 20 tickets
     3.0x  splits in part research 5 sources, then reconcile
     2.0x  splits in part write a report with 4 sections
     1.0x  DOES NOT SPLIT refactor a module, then fix its tests
     1.0x  DOES NOT SPLIT plan a trip

  2 of 6 split well, 2 not at all. And the two that do
  not have the same shape: every piece needs the one
  before it, so the chain IS the task and a second agent
  has nothing to do until the first has finished.

  Now the part that makes a wrong answer expensive.
  You pay for agents, not for speed-up. One agent a
  piece is what people reach for; the number that
  earns its place is the width.

  task                        one each  paid   width  paid
  summarise 8 documents              8   1.0x      8   1.0x
  triage 20 tickets                 20   1.0x     20   1.0x
  research 5 sources, then r…        6   2.0x      5   1.7x
  write a report with 4 sect…        6   3.0x      4   2.0x
  refactor a module, then fi…        2   2.0x      1   1.0x
  plan a trip                        4   4.0x      1   1.0x

  Paid is agents divided by speed-up: what one unit of
  parallelism cost you. At 1.0 every agent earned its
  place. plan a trip is the worst of the six at
  4.0 times: 4 agents and no speed-up at all. And
  the right column is the same six tasks with the agents
  the shape actually supports.
```

**Two of six split well and two do not split at all.** The ones that do are the ones people
already know about: a pile of documents, a queue of tickets. Many independent things of the same
kind.

A **coupled task** is one whose pieces each need the one before, and the two in the table are
that shape. *Plan a trip* has four pieces and a chain of four: you cannot book a hotel before
you know the flight. A second agent has nothing to do until the first has finished, so the run
takes as long as one agent would take and you are paying for four.

**The number that answers the question is pieces divided by the chain**, with one assumption
stated: reading that count as a speed-up needs the pieces to be of roughly similar size, and a
2.0 could be 3.0 or 1.2 if one piece dominates the rest. The two rows that score 1.0 are right
whatever the sizes, because a chain is a chain. And the chain has a name worth having. The **critical path** is the longest sequence of pieces that must happen in
order, and it is the shortest the task can take however many agents you buy. Four pieces in a
chain of four is a speed-up of one.

**And the agents that earn their place are the parallel width, not one per piece.** The
**parallel width** is the most pieces that can be in flight at once. *Write a report with four
sections* has six pieces and a width of four, because the outline has to come first and the
joining has to come last — so one agent per piece pays three times for two times the speed, and
four agents pay twice.

> **Note:** Those dependency lists are a judgement about each task, and they are written into
> the file so you can disagree with one. What is computed from them is not a judgement: given
> the pieces and what each needs first, the critical path and the width follow, and the `assert`
> in `depth` is what stops a dependency list that loops back on itself from being scored at all.

> **Warning:** The shape of the work is a property of the work and not of your design, so no
> amount of better orchestration moves it. This is a [**derivation**]{.noindex} in Chapter 6's sense — the
> row that sits off its ladder, because you can check it yourself and it does not date: if piece B needs piece A's output, nothing that runs B earlier can
> be correct. What a better design can do is notice, and use the width instead of the count.

## What Several Agents Actually Cost

Now the bill, and it is the opposite of the folk claim.

```python
"""Where the tokens go when one agent becomes several.

Chapter 35 sent the arithmetic on running several sub-agents here.
The answer turns on one thing, and it is not the number of agents.

Every call sends the same four things: the instruction, the tool
block, whatever material the agent had to read to start, and the
record so far. The record grows by PER_STEP a step, which is
chapter 34's model and the reason a run has a square in it. Chapter
34 owns why; this applies it to runs of different lengths. The
constants are this file's own, not chapter 34's.
"""
INSTRUCTION = 1_200
TOOL_DEFS = 650
SHARED = 6_000     # material an agent reads before it can start
BRIEF = 250        # what the orchestrator writes to one agent
SUMMARY = 400      # what one agent hands back
PER_STEP = 1_600   # a decision plus what came back
PIECES = 12        # steps of real work, however they are divided


def agent_run(steps, shared=SHARED):
    """Input tokens one agent sends across `steps` calls. Each call
    re-sends the fixed block, the shared material and the record."""
    fixed = INSTRUCTION + TOOL_DEFS + shared
    return sum(fixed + PER_STEP * i for i in range(steps))


def orchestrator(k):
    """k calls, its record growing by one summary each time, plus a
    brief written down to each agent."""
    fixed = INSTRUCTION + TOOL_DEFS
    return sum(fixed + SUMMARY * i for i in range(k)) + k * BRIEF


def divide(k, shared=SHARED, steps=None):
    """k agents with the work divided among them."""
    m = steps if steps else PIECES // k
    return k * agent_run(m, shared) + orchestrator(k)


def duplicate(k, shared=SHARED):
    """k agents each doing the whole task."""
    return k * agent_run(PIECES, shared) + orchestrator(k)


def both():
    base = divide(1)
    print(f"  {PIECES} steps of work. One agent sends {base:,} tokens")
    print("  in all. Now put k agents on it, two ways.\n")
    print("     k    divided   against      duplicated   against")
    print("                     one agent                one agent")
    for k in (1, 2, 3, 4, 6, 12):
        d, u = divide(k), duplicate(k)
        print(f"  {k:>4}{d:>11,}{d / base:>9.2f}x{u:>15,}"
              f"{u / base:>9.2f}x")
    return base


def findings(base):
    d6, u6 = divide(6), duplicate(6)
    print("\n  Read the two 'against one agent' columns together.\n")
    print(f"  Divided, six agents cost {d6 / base:.2f} times one. They are")
    print("  CHEAPER, and chapter 34 is why: the square is over the")
    print("  length of a run, so six two-step runs make six small")
    print("  squares where one twelve-step run makes a large one.")
    print(f"\n  Duplicated, the same six agents cost "
          f"{u6 / base:.2f} times one.")
    print("  That is the opening problem, and the multiplier is")
    print("  just the number of agents: each one does the whole")
    print("  task, so each one sends what the single agent sent.")
    print("\n  Token multiplication is that second column. It is")
    print("  not what having several agents costs. It is what")
    print("  having several agents that do not divide the work")
    print("  costs, and the first section of this chapter is how")
    print("  you tell in advance which one you have.")


def shared_does_not_decide():
    print("\n  And it is not the shared material either, which is")
    print("  the explanation that sounds right. Hold the design")
    print("  fixed and turn only how much every agent must read:\n")
    print("    shared   divided by 6   duplicated by 6")
    for sh in (0, 6_000, 20_000, 50_000):
        b = divide(1, sh)
        print(f"  {sh:>8,}{divide(6, sh) / b:>14.2f}x"
              f"{duplicate(6, sh) / b:>17.2f}x")
    print("\n  The duplicated column does not move at all: 6.05 to")
    print("  6.01. The divided column does move towards 1.0, and")
    print("  the reason is dilution rather than cost: the twelve")
    print("  steps re-send the shared material the same number of")
    print("  times either way, so it is added in equal measure to")
    print("  both sides and the ratio between them narrows. So")
    print("  shared material can take away the")
    print("  saving from dividing the work. It cannot produce the")
    print("  multiplier, and nothing but duplication does.")


def not_stopping(base):
    print("\n  One more thing can move, and it is the other half of")
    print("  the opening problem. Six agents and an orchestrator is")
    print("  seven stopping conditions, and any one can fail to")
    print("  fire. Six agents that DO divide the work, and then run")
    print("  on to a step limit instead of stopping:\n")
    print("     limit        total   against one agent")
    for limit in (2, 5, 10, 20):
        t = divide(6, steps=limit)
        print(f"  {limit:>8}{t:>13,}{t / base:>14.2f}x")
    print("\n  Two steps is the work finishing. Twenty is six agents")
    print("  that never decided they were done. The division of")
    print("  labour is correct in every row; only the stopping")
    print("  changes, and it spans a factor of twenty.")
    print("\n  So there are two ways to pay several times over, and")
    print("  neither is the number of agents: not dividing the")
    print("  work, and not stopping.")


if __name__ == "__main__":
    b = both()
    findings(b)
    shared_does_not_decide()
    not_stopping(b)
```

```text
  12 steps of work. One agent sends 201,900 tokens
  in all. Now put k agents on it, two ways.

     k    divided   against      duplicated   against
                     one agent                one agent
     1    201,900     1.00x        201,900     1.00x
     2    146,800     0.73x        404,200     2.00x
     3    130,500     0.65x        606,900     3.01x
     4    124,200     0.62x        810,000     4.01x
     6    122,400     0.61x      1,217,400     6.03x
    12    145,800     0.72x      2,449,200    12.13x

  Read the two 'against one agent' columns together.

  Divided, six agents cost 0.61 times one. They are
  CHEAPER, and chapter 34 is why: the square is over the
  length of a run, so six two-step runs make six small
  squares where one twelve-step run makes a large one.

  Duplicated, the same six agents cost 6.03 times one.
  That is the opening problem, and the multiplier is
  just the number of agents: each one does the whole
  task, so each one sends what the single agent sent.

  Token multiplication is that second column. It is
  not what having several agents costs. It is what
  having several agents that do not divide the work
  costs, and the first section of this chapter is how
  you tell in advance which one you have.

  And it is not the shared material either, which is
  the explanation that sounds right. Hold the design
  fixed and turn only how much every agent must read:

    shared   divided by 6   duplicated by 6
         0          0.39x             6.05x
     6,000          0.61x             6.03x
    20,000          0.79x             6.02x
    50,000          0.89x             6.01x

  The duplicated column does not move at all: 6.05 to
  6.01. The divided column does move towards 1.0, and
  the reason is dilution rather than cost: the twelve
  steps re-send the shared material the same number of
  times either way, so it is added in equal measure to
  both sides and the ratio between them narrows. So
  shared material can take away the
  saving from dividing the work. It cannot produce the
  multiplier, and nothing but duplication does.

  One more thing can move, and it is the other half of
  the opening problem. Six agents and an orchestrator is
  seven stopping conditions, and any one can fail to
  fire. Six agents that DO divide the work, and then run
  on to a step limit instead of stopping:

     limit        total   against one agent
         2      122,400          0.61x
         5      350,100          1.73x
        10      921,600          4.56x
        20    2,784,600         13.79x

  Two steps is the work finishing. Twenty is six agents
  that never decided they were done. The division of
  labour is correct in every row; only the stopping
  changes, and it spans a factor of twenty.

  So there are two ways to pay several times over, and
  neither is the number of agents: not dividing the
  work, and not stopping.
```

**There are two ways to put six agents on a task, and they do not cost the same.** Divided —
each agent taking two of the twelve steps — six agents cost [**0.61 times**]{.noindex} what one costs. They
are cheaper, and Chapter 34 is why: its square is over the length of a run, so six two-step runs
make six small squares where one twelve-step run makes a large one.

**Duplicated — each agent doing the whole task — the same six agents cost 6.03 times one.** That
is the opening problem, and the multiplier is simply the number of agents. Each one sends what
the single agent sent, and the orchestrator is a rounding error on top of that.

**Token multiplication** is that second column. It is not the price of having several agents; it
is the price of having several that do not divide the work. Which of the two you have is the
first section's question, answered before anything runs — because a task whose critical path is
the whole task cannot be divided, so agents put on it duplicate by construction.

**And it is not the shared material, which is the explanation that sounds right.** Turn only how
much every agent has to read before it can start and the duplicated column does not move: 6.05
to 6.01. The divided column does move towards 1.0, and the reason is dilution rather than cost —
one agent and six that divide the work make the same twelve agent calls, so they re-send that
material the same number of times and it is added in equal measure to both sides, narrowing the
ratio between them. Six that duplicate make seventy-two calls, which is why their column does
not move at all: the material multiplies with everything else. Shared material
can take the saving away. It cannot produce the multiplier.

**Then the other half of the opening problem.** Six agents and an orchestrator is seven stopping
conditions, and any one of them can fail to fire. Six agents that *do* divide the work and then
run on to a ten-step limit cost [**4.56 times**]{.noindex} a single agent; at a twenty-step limit, [**13.79
times**]{.noindex}. The division of labour is correct in every one of those rows. Only the stopping changes.

> **Note:** This counts tokens sent and it is not a bill — Chapter 53 owns that — and the
> distinction matters more here than usual, because Chapter 52's prompt-prefix caching does not
> fall evenly on the two designs. One agent's twelve calls share one growing prefix, so much of
> what it re-sends is a cache hit; six agents have six separate prefixes, each reused across two
> calls. So the count says dividing is cheaper and the bill may not. The figure that survives any
> caching arrangement is the duplication one, because it is about the number of agents rather
> than about what they re-send.

> **Warning:** None of this says six agents are *better* than one. It says where the cost is,
> and the answer is that it is not in the headcount: it is in duplication and in not stopping,
> and both of those are design faults with names rather than a tax on having several agents.


## Three Ways They Fail

The failures sort into three kinds, and the sort is not this book's: it comes from the study the
next section is about. What is this book's is the mechanism under each one, because every one of
the three is something an earlier chapter already explained.

[**System design**]{.noindex}, which the study's third version calls *system design issues* and its second
called *specification issues*. The pieces were wrong, or the specification the agents were
working from was. The first section of this chapter is one member of that family worked out in
advance: a chain scored as though it were a pile. The study's own category is wider — its five
members are an agent disobeying the task or the role it was given, repeating a step, losing the
conversation so far, and not noticing a condition that should have ended it — and it is careful
about something this chapter has to be careful about too. Its own sentence is that failures here
*often manifest during execution but reflect flaws in pre-execution design choices*, which is
the difference between where a fault shows up and where it was made. So *settled before anything
runs* is true of where this chapter's member comes from, and not of when you will see it.

**Inter-agent misalignment**, which is one agent's output not being what the next one needed.
The mechanism is Chapter 35's: a hand-off is a summary, a summary loses silently, and the
receiving agent cannot see what the sending one saw. So a wrong fact arrives as an established
one with nothing left to contradict it — Chapter 4's compounding error, and worse here than
inside one loop, because inside a loop the earlier result is still in the context and a later
step can disagree with it.

**Task verification.** Nobody decided when it was done, or nobody checked what was done. Chapter
4 owns the stopping condition and says a loop needs all three of its reasons to end; a system of
*k* agents has *k* plus one sets of them, and a run that nobody stops is the arithmetic above at
thirteen times. This is the category that produces *finished nothing*, and it is also the one
that produces the bill.

> **Note:** Specialisation is the other argument for several agents, and it is an argument
> about quality rather than about time. Five specialised agents on a chain of five do the five
> steps better and still take as long as one agent would, at five times the fixed cost — which
> may well be worth it, and is a different claim from the one usually made for it. The chain is
> arithmetic; whether specialists do better work is a measurement, and Chapter 20 is how to take
> it.

> **Tip:** The order to debug in is the order above, and it is not the order people try. The
> instinct is to improve the prompts, which is the second category, and to add a reviewing
> agent, which is the third category made heavier. Ask first whether the work splits, because if
> it does not then nothing in the other two columns was ever going to work.


## What the Evidence Is, and How Strong

Those three categories came from somewhere, and the honest answer about where is worth more in
an interview than the categories are.


```python
"""What the evidence on multi-agent failure actually is.

The study everybody cites is "Why Do Multi-Agent LLM Systems Fail?",
arXiv:2503.13657, posted 17 March 2025, revised to a third version
on 26 October 2025, and presented at NeurIPS 2025 as a spotlight
poster.

One source, four artefacts, and they do not say the same thing. Two
versions of the paper, each with an abstract page that is shorter
than its own text, and a conference page that is the only one of the
four to say where the work was presented.
"""
ARTEFACTS = {
    "frameworks": {
        "v2 text": "5 for the taxonomy; 7 for the dataset",
        "v3 text": "7 in the introduction, six in a figure "
                   "caption, on benchmarks it says are not "
                   "directly comparable",
        "v3 abstract": "7",
    },
    "traces annotated": {
        "v2 text": "200+",
        "v3 text": "1,642",
        "v3 abstract": "1,600+",
    },
    "who annotated them": {
        "v2 text": "six expert humans; an LLM annotator was "
                   "then validated against them at kappa 0.77",
        "v3 text": "the same, scaled by that annotator",
        "v3 abstract": "expert humans for the taxonomy, and an "
                       "LLM-as-a-Judge pipeline to scale it",
    },
    "the kappa 0.88": {
        "v2 text": "three humans agreeing with each other on 15 "
                   "traces, while the taxonomy was being refined",
        "v3 text": "the same",
        "v3 abstract": "high inter-annotator agreement",
    },
    "name of the first category": {
        "v2 text": "Specification Issues",
        "v3 text": "System Design Issues",
        "v3 abstract": "-",
    },
    "shares by category": {
        "v2 text": "41.77, 36.94, 21.30 per cent",
        "v3 text": "not stated; the per-mode shares are, and "
                   "they sum to the three below",
        "v3 abstract": "not stated",
    },
    "failure rate across frameworks": {
        "v2 text": "-",
        "v3 text": "41 to 86.7 per cent",
        "v3 abstract": "-",
    },
    "where it was presented": {
        "v2 text": "-",
        "v3 text": "-",
        "v3 abstract": "no venue line",
    },
}

# version 3's printed per-mode shares, by category
MODES_V3 = {
    "FC1": [11.8, 1.5, 15.7, 2.80, 12.4],
    "FC2": [2.20, 6.80, 7.40, 0.85, 1.90, 13.2],
    "FC3": [6.20, 8.20, 9.10],
}

CLAIMS = [
    ("three categories of failure", "in the paper, both versions"),
    ("14 failure modes", "in the paper, both versions"),
    ("gains over single-agent frameworks are often minimal",
     "in the paper's introduction, both versions; NOT in "
     "version 3's abstract, which drops the comparison"),
    ("five frameworks were analysed",
     "in the paper: the five the taxonomy came from"),
    ("seven frameworks were analysed",
     "in the paper: the seven the dataset spans"),
    ("41.8 / 36.9 / 21.3 per cent by category",
     "in the paper, version 2's text"),
    ("44.2 / 32.3 / 23.5 per cent by category",
     "version 3's per-mode shares sum to these"),
    ("step repetition is commonest, at 17.14 per cent",
     "in the paper, version 2; version 3 prints 15.7 and it "
     "is still the largest"),
    ("18 failure modes", "in neither version"),
    ("41 to 86 per cent of them fail in production",
     "the RANGE is version 3's. 'In production' is not: it "
     "measured benchmark runs"),
]


def _wrap(s, n):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    out.append(line)
    return out


def artefacts():
    print("  One source, four artefacts.\n")
    for fact, said in ARTEFACTS.items():
        print(f"    {fact}")
        for col in ("v2 text", "v3 text", "v3 abstract"):
            v = said[col]
            if v == "-":
                continue
            first = True
            for line in _wrap(v, 34):
                print(f"      {col if first else '':<14}{line}")
                first = False
        print()


def sums():
    print("  Version 3 prints no shares by category. It prints")
    print("  fourteen shares by mode, and they add up:\n")
    for cat, vals in MODES_V3.items():
        joined = " + ".join(f"{v}" for v in vals)
        for i, line in enumerate(_wrap(joined, 40)):
            head = f"    {cat}  " if i == 0 else "          "
            print(f"{head}{line}")
        print(f"          = {sum(vals):.2f}")
    print("\n  So the second split in circulation is version 3's,")
    print("  derivable from its own text, and the first is version")
    print("  2's, printed in it. They are one paper at two moments.")


def claims():
    print("\n  Ten claims about it that are in circulation.\n")
    for text, status in CLAIMS:
        print(f"    {text}")
        for line in _wrap(status, 44):
            print(f"      -> {line}")
    n = len(CLAIMS)
    paper = sum(1 for _, s in CLAIMS if s.startswith("in the paper")
                or s.startswith("version 3"))
    print(f"\n  {paper} of {n} are the paper's. One is in neither")
    print("  version. And one is the interesting case: the number")
    print("  is the paper's and the words around it are not.")
    print("\n  That last one is the shape to expect. The failure")
    print("  rate is real and it was measured on benchmark runs")
    print("  that version 3 says are not directly comparable, over")
    print("  a count its own text and its own figure caption")
    print("  disagree about. 'Fail in production' is a different")
    print("  claim, and nothing measured it.")


def ladder():
    print("\n  Where it sits on chapter 6's ladder: ONE STUDY -")
    print("  measured, in one setting, with one set of choices. It")
    print("  supports that it worked there, which here means that")
    print("  these fourteen modes were found in these frameworks.")
    print("\n  Being a spotlight at a large conference does not move")
    print("  it up. Chapter 6's tell for settled practice is")
    print("  failure modes written down by many independent teams")
    print("  over years, and peer review is one team's work being")
    print("  checked rather than many teams' being compared.")
    print("\n  And read the two kappas apart. A kappa is an")
    print("  agreement coefficient running to 1.0. The 0.88 is")
    print("  three people agreeing with each other about fifteen")
    print("  traces; the 0.77 is a model agreeing with those")
    print("  people, which is what let the dataset become large.")
    print("  Neither is a correctness figure.")


if __name__ == "__main__":
    artefacts()
    sums()
    claims()
    ladder()
```

```text
  One source, four artefacts.

    frameworks
      v2 text       5 for the taxonomy; 7 for the
                    dataset
      v3 text       7 in the introduction, six in a
                    figure caption, on benchmarks it
                    says are not directly comparable
      v3 abstract   7

    traces annotated
      v2 text       200+
      v3 text       1,642
      v3 abstract   1,600+

    who annotated them
      v2 text       six expert humans; an LLM
                    annotator was then validated
                    against them at kappa 0.77
      v3 text       the same, scaled by that annotator
      v3 abstract   expert humans for the taxonomy,
                    and an LLM-as-a-Judge pipeline to
                    scale it

    the kappa 0.88
      v2 text       three humans agreeing with each
                    other on 15 traces, while the
                    taxonomy was being refined
      v3 text       the same
      v3 abstract   high inter-annotator agreement

    name of the first category
      v2 text       Specification Issues
      v3 text       System Design Issues

    shares by category
      v2 text       41.77, 36.94, 21.30 per cent
      v3 text       not stated; the per-mode shares
                    are, and they sum to the three
                    below
      v3 abstract   not stated

    failure rate across frameworks
      v3 text       41 to 86.7 per cent

    where it was presented
      v3 abstract   no venue line

  Version 3 prints no shares by category. It prints
  fourteen shares by mode, and they add up:

    FC1  11.8 + 1.5 + 15.7 + 2.8 + 12.4
          = 44.20
    FC2  2.2 + 6.8 + 7.4 + 0.85 + 1.9 + 13.2
          = 32.35
    FC3  6.2 + 8.2 + 9.1
          = 23.50

  So the second split in circulation is version 3's,
  derivable from its own text, and the first is version
  2's, printed in it. They are one paper at two moments.

  Ten claims about it that are in circulation.

    three categories of failure
      -> in the paper, both versions
    14 failure modes
      -> in the paper, both versions
    gains over single-agent frameworks are often minimal
      -> in the paper's introduction, both versions;
      -> NOT in version 3's abstract, which drops the
      -> comparison
    five frameworks were analysed
      -> in the paper: the five the taxonomy came
      -> from
    seven frameworks were analysed
      -> in the paper: the seven the dataset spans
    41.8 / 36.9 / 21.3 per cent by category
      -> in the paper, version 2's text
    44.2 / 32.3 / 23.5 per cent by category
      -> version 3's per-mode shares sum to these
    step repetition is commonest, at 17.14 per cent
      -> in the paper, version 2; version 3 prints
      -> 15.7 and it is still the largest
    18 failure modes
      -> in neither version
    41 to 86 per cent of them fail in production
      -> the RANGE is version 3's. 'In production' is
      -> not: it measured benchmark runs

  8 of 10 are the paper's. One is in neither
  version. And one is the interesting case: the number
  is the paper's and the words around it are not.

  That last one is the shape to expect. The failure
  rate is real and it was measured on benchmark runs
  that version 3 says are not directly comparable, over
  a count its own text and its own figure caption
  disagree about. 'Fail in production' is a different
  claim, and nothing measured it.

  Where it sits on chapter 6's ladder: ONE STUDY -
  measured, in one setting, with one set of choices. It
  supports that it worked there, which here means that
  these fourteen modes were found in these frameworks.

  Being a spotlight at a large conference does not move
  it up. Chapter 6's tell for settled practice is
  failure modes written down by many independent teams
  over years, and peer review is one team's work being
  checked rather than many teams' being compared.

  And read the two kappas apart. A kappa is an
  agreement coefficient running to 1.0. The 0.88 is
  three people agreeing with each other about fifteen
  traces; the 0.77 is a model agreeing with those
  people, which is what let the dataset become large.
  Neither is a correctness figure.
```

**Eight of the ten claims in circulation are the paper's.** That is the opposite of what the
shape of the question suggests, and it is the useful finding: the trouble with the figures going
round is not that somebody invented them.

**The two splits that look like a contradiction are one paper at two moments.** 41.8 / 36.9 /
21.3 is printed in its second version. The third version prints no shares by category at all —
it prints fourteen shares by mode, and they sum to 44.2, 32.35 and 23.5, which is the other
split in circulation. Its dataset grew from two hundred traces to sixteen hundred between the
two, so a share quoted without a version number is not a wrong figure; it is an unfinished one.

**One claim is in neither version**, and one is the case worth carrying into an interview: the
failure rate. *41 to 86 per cent* is the paper's own range, in its third version's introduction,
and *in production* is not. It measured runs against benchmarks that the paper itself says are
not directly comparable, across a number of systems its text and its own figure caption disagree
about. So the number is sound and the sentence built on it is not — which is a harder thing to
spot than an invented figure, and commoner.

**And the category names moved too.** What the third version calls *system design issues* the
second called *specification issues*. Nothing about the category changed; a reader comparing two
write-ups that quote different versions would reasonably conclude the taxonomy had.

**On Chapter 6's ladder this is one study.** Measured, in one setting, with one set of choices,
supporting *that it worked there* — which here means that these fourteen modes were found in
these frameworks. Being a spotlight at a large conference does not move it up, because Chapter
6's tell for settled practice is failure modes written down by many independent teams over
years, and peer review is one team's work being checked rather than many teams' being compared.

**And read the two agreement figures apart.** A **kappa** is an agreement coefficient running to
1.0. The 0.88 is three people agreeing with each other about fifteen traces while the taxonomy
was still being refined; the 0.77 is a model agreeing with those people, which is what let the
dataset become large. Neither is a correctness figure: Chapter 31's point about a judge
generalises. It measures one judge against itself, which is a different measurement from two
people against each other — what carries across is the distinction and not the figure.

> **Tip:** When an interviewer quotes a multi-agent failure rate, the answer is not a
> counter-figure and it is not a refusal. It is: that range is the paper's own, measured on
> benchmark runs the paper says are not directly comparable, and the words *in production* are
> not the paper's. Then the rest of it — one study, presented at NeurIPS in 2025, a fourteen-mode
> taxonomy in three categories built from traces of five frameworks and tested on two more,
> whose shares by category and whose category names both moved between versions. Knowing which
> part of a quoted claim is sound is a better answer than doubting all of it.


## What To Actually Do

1. **Draw the pieces and what each needs first**, before writing anything. Pieces divided by the
   critical path is the most parallelism the work contains.
2. **Buy agents equal to the parallel width**, not one per piece.
3. **If the chain is the whole task, use one agent.** A coupled task given several agents pays
   for every one of them and finishes no sooner.
4. **Do not reach for the shared material as the explanation.** Dividing the work makes the
   same number of agent calls as one agent would, so the material is re-sent the same number of
   times and dilutes the difference rather than causing it. Duplication can, and so can not stopping.
5. **Give the system one stopping condition that outranks the rest**, in your code, at the
   orchestrator. Seven places to decide when to stop is seven places to forget.
6. **Check the hand-offs the way you check a summary** — Chapter 35's must-keep list, applied to
   what one agent tells the next.
7. **Quote the evidence as what it is**, with a version number. One study at NeurIPS 2025, a
   fourteen-mode taxonomy in three categories, built from five frameworks and tested on two
   more, whose shares by category moved between versions.

> **Warning:** Nothing above makes several agents better than one, and the arithmetic will not
> settle that either. What it settles is the cost, and the cost turned out to be the weaker
> objection: on these numbers six agents that divide the work are cheaper than one, and it is
> duplication and non-termination that cost several times over. The real question is Chapter 38's — whether the system does the task — and
> this chapter's contribution to it is that the first way it fails is *made* before any agent
> runs, whenever you will see it, and the exposure to the second is settled in the design too.

## Lab: Score a Multi-Agent Design

Pen and paper, then the three programs. Twenty-five minutes, and there is a key for every step.

**Step 1.** A colleague proposes five agents for this task: read a specification, write the
code, write the tests, run the tests, fix what failed. Score it.

*Expected result:* five pieces, a chain of five, a width of one, so a speed-up of 1.0 and five
agents paying five times for nothing. Every piece needs the one before it. The only thing that
could run alongside is writing the tests, if they are written from the specification rather than
from the code — which is a decision about the work, not about the agents, and it would take the
width to two.

**Step 2.** The same colleague says the agents will be faster because each one is specialised.
What do you say?

*Expected result:* specialisation is an argument about quality, not about time, and the critical
path is unmoved by it. If five specialised agents each do their piece better, you have five
sequential steps done better, at five times the fixed cost — which may be worth it, and is a
different claim from the one they made. The chain is arithmetic; the quality is a measurement,
and Chapter 20 is how to take it.

**Step 3.** Your six agents each need to read a 20,000-token policy pack. Using the table, what
does the system cost against one agent — and what do you need to know before you can answer?

*Expected result:* you need to know whether the six divide the work or duplicate it, and the
table gives both: 0.79 times if they divide it, 6.02 if they each do the whole task. Note which
way the first one cuts — at 0.79 the system is *cheaper* than one agent even with 20,000 tokens
in front of every agent, because dividing the work makes the same twelve agent calls that one
agent would, so the material is re-sent the same number of times.
If you had guessed sixfold from the policy pack alone you would have been arguing against the
design on grounds the arithmetic does not support.

**Step 4.** Of the three failure categories, which would you expect in a system whose agents
each rewrite the shared plan as they go?

*Expected result:* inter-agent misalignment, and for the reason Chapter 35 gives — each rewrite
is a summary, each summary drops what it did not narrate, and the next agent cannot see what the
last one saw. The second-order effect is the third category, because a plan that keeps changing
is a system with nothing to compare against when deciding it is done.

**Step 5.** An interviewer says 80 per cent of multi-agent systems fail in production. What do
you say?

*Expected result:* ask where the figure comes from, and say what the actual evidence is: one
study presented at NeurIPS in 2025, with a fourteen-mode taxonomy in three categories built
from traces of five frameworks and tested on two more, whose own abstract says gains over
single-agent frameworks are often minimal.
Figures in that range circulate without a primary source. This is not pedantry in an interview;
it is the difference between having read about the field and having read the field.

**Step 6.** You are given one change to a failing six-agent system. What do you make?

*Expected result:* a single stopping condition at the orchestrator that outranks the agents'. By
the arithmetic it is worth more than everything else on the list: it is the difference between
0.61 times a single agent and 13.79 times, and it is the category that produces *finished
nothing*.
The honest second answer is to check first whether the work splits at all, because if it does
not then the right change is to use one agent and the question was wrong.

## Summary, Key Terms, and Review Questions

### Summary

Ask whether the work comes apart before anything else, because the answer is arithmetic. Write
the task as pieces and what each needs first; the **critical path** is the longest chain through
them, and it is the shortest the task can take however many agents you buy. Pieces divided by the
critical path is the most parallelism the work contains — 20 for a queue of tickets, 1.0 for
planning a trip — and the agents that earn their place are the **parallel width**, the most
pieces that can be in flight at once, not one per piece. A **coupled task**, whose pieces each
need the one before, pays for every agent and finishes no sooner. Then the cost, which runs the
other way from the story. **Token multiplication** is real, and it is not what having several
agents costs: the re-send cost *falls* when a run is split, because Chapter 34's square is over
the length of a run and six short runs make six small squares. On the worked numbers six agents that *divide* the work cost 0.61 times one, and
six that *duplicate* it — each doing the whole task — cost 6.03 times, which is the opening
problem and is simply the number of agents. **Token multiplication** is that second number: the
price not of having several agents but of having several that do not divide the work. Shared
material dilutes the saving and cannot produce the multiplier. The other way to pay several
times over is the stopping: six agents and an orchestrator is seven stopping conditions, and the
same divided work run to a ten-step limit costs 4.56 times a single agent and to a twenty-step
limit 13.79 times. Neither the instruction block nor the shared material rises with the number
of agents while the work is divided, because the number of agent calls does not change. The failures sort into three kinds —
system design, **inter-agent misalignment** and task verification — and each has a mechanism an
earlier chapter gave: a chain scored as a pile, a hand-off that is a summary and loses silently,
and a loop nobody stops. Those mechanisms are this book's; the study's own first category is
wider than the one worked here and three of the things in it happen at run time, so *settled
before anything runs* is true of the mechanism and not of the category. And the evidence for
all of it is **one study**, presented at NeurIPS in 2025: fourteen modes in three categories,
built from traces of five frameworks and tested on two more. One study is where it sits on
Chapter 6's ladder, and a spotlight does not move it up. Of ten claims about it in circulation
eight are in the paper; the two per-category splits that look like a contradiction are one
paper's figures at two versions, because its dataset grew, so a share quoted without a version
number says nothing; and the only claim with no primary source at all is the production failure
rate. A **kappa** — an agreement coefficient running to 1.0 — of 0.88 says three people agreed
with each other about fifteen traces while the taxonomy was being refined, and 0.77 says a model
agreed with those people. Neither is a statement about being right.

### Key Terms

| Term | Meaning |
|---|---|
| **Multi-agent system** | A design in which several agents run on one task, each with its own context and stopping condition, coordinated by your code or by one of them. Chapter 4 owns the agent and Chapter 35 the sub-agent; this is the arrangement of several |
| **Critical path** | The longest chain of pieces that must happen in order. The shortest a task can take however many agents you have, so pieces divided by it is the most parallelism the work contains |
| **Parallel width** | The most pieces that can be in flight at once, and therefore the number of agents that earn their place. Chapter 9's *width* is a different thing — the size of a model's vectors |
| **Coupled task** | One whose pieces each need the one before, so the chain is the whole task. Given several agents it pays for all of them and finishes no sooner |
| **Token multiplication** | What several agents cost when they *duplicate* the work rather than divide it, which is simply their number: six agents each doing the whole task cost 6.03 times one. Dividing the work costs less than one agent, because the re-send cost falls with the length of a run. Neither the instruction block nor the shared material rises with the number of agents while the work is divided |
| **Kappa** | An agreement coefficient running to 1.0, used to say how far two labellers agree. Not a correctness figure: the study's 0.88 is three people agreeing with each other, and its 0.77 is a model agreeing with those people |
| **Inter-agent misalignment** | One agent's output not being what the next one needed. The middle of the three failure categories, and Chapter 35's summary problem with no shared context to catch it |

### Worth Memorising

| Item | Value or formula |
|---|---|
| The most parallelism available | Pieces divided by the critical path, if the pieces are of similar size |
| How many agents to buy | The parallel width, not one per piece |
| Worked: planning a trip | 4 pieces, a chain of 4, a width of 1 — four agents buy nothing |
| When several agents cost more | When they duplicate the work rather than divide it — and then the multiplier is just their number: 6.03 at six agents, against 0.61 divided |
| What a non-stopping system costs | 4.56 times a single agent at a 10-step limit, 13.79 at 20 |
| The three failure categories | System design, inter-agent misalignment, task verification |
| What the evidence is | One study, NeurIPS 2025: 14 modes in 3 categories, from 5 frameworks and tested on 2 more. The shares by category moved between versions |

### Review Questions

1. How do you decide whether a task should be given to several agents, and what is the number that decides it?
2. Why does buying one agent per piece of work usually overpay, and what is the right number?
3. Several agents cost more than one. Is that true, and what does it actually depend on?
4. Name the three ways multi-agent systems fail, and give the mechanism for each.
5. An interviewer says most multi-agent systems fail in production. What do you say?
6. You can make one change to a failing six-agent system. What is it, and why that one?

### Review Answers

1. Write the task as pieces and what each piece needs before it can start, then take the longest
chain through the dependencies — the critical path. Pieces divided by that chain is the most
parallelism the work contains, and it is a property of the work rather than of your design: if
piece B needs piece A's output, nothing that runs B earlier is correct. On the six tasks worked
here a queue of twenty tickets scores 20, five sources then a reconciliation scores 3.0, and
planning a trip scores 1.0 — four pieces in a chain of four, where a second agent has nothing to
do until the first has finished.
2. Because the number of pieces and the number that can be in flight at once are different
numbers. The parallel width is the most pieces at any one level of the dependency graph, and it
is what to buy. *Write a report with four sections* has six pieces and a width of four, because
the outline comes first and the joining comes last: one agent per piece pays three times for two
times the speed, and four agents pay twice. Any agent beyond the width is an agent that waits.
3. Not necessarily, and what it depends on is whether they divide the work or duplicate it.
Divided — six agents taking two of twelve steps each — six cost 0.61 times one, because Chapter
34's square is over the length of a run and six two-step runs make six small squares instead of
one large one. Duplicated, with each agent doing the whole task, the same six cost 6.03 times,
and that multiplier is simply their number. Shared material does not decide it: it is re-sent
the same number of times when the work is divided as when one agent does it, so it dilutes that
saving rather than causing it, and it leaves the duplication figure untouched. The other way to pay several times over is the stopping — seven
stopping conditions instead of one, and the same divided work run to a ten-step limit costs 4.56
times a single agent. One caution: that is a count of tokens, not a bill, and Chapter 52's
prefix caching falls unevenly on one long prefix against six short ones.
4. System design — *system design issues* in the study's third version, *specification issues*
in its second — where the pieces were wrong or the specification was, and the member of that
family this chapter works out is the critical path scored as though it were a pile. The study's
category is wider, and its own sentence about it is that failures here often show up during
execution while reflecting flaws made before it. Inter-agent
misalignment — one agent's output is not what the next needed, and the mechanism is Chapter 35's:
a hand-off is a summary, a summary loses silently, and the receiving agent cannot see what the
sender saw, so a wrong fact arrives as an established one with nothing to contradict it. Task
verification — nobody decided when it was done, or nobody checked what was done, which is
Chapter 4's stopping condition multiplied by the number of agents plus one. The mechanism under
the first is settled before anything runs and the exposure to the second is too, though a
misalignment itself happens at run time; the third is the one that produces both *finished
nothing* and the bill.
5. Ask where the number comes from, then say what the evidence is. There is one well-known
study, first posted in March 2025 and presented at NeurIPS that year; it built a fourteen-mode
taxonomy in three categories from traces of five frameworks and tested it on two more. Its own
abstract says gains over single-agent frameworks are often minimal. Production failure rates in
the range of 41 to 86 per cent circulate with no primary source that a search turns up. The two
per-category splits being repeated are not a contradiction: one is the paper's second version,
the dataset grew afterwards, and a share quoted without a version number says nothing. On
Chapter 6's ladder this is one study and not settled practice — a spotlight is one team's work
being checked, not many teams' being compared — and a kappa of 0.88 means three annotators agreed
with each other rather than that they were right.
6. One stopping condition at the orchestrator that outranks the agents', enforced in your code.
By the arithmetic it is worth more than anything else available: it is the difference between
0.61 times a single agent and 13.79 times, and it is the failure category that produces *finished
nothing*. The honest second answer is that before making any change you check whether the work
splits at all, because if the critical path is the whole task then the right change is to use one
agent and the six-agent design was the wrong question.

> **You understand this when** you can take a proposed multi-agent design, score its critical
> path on paper, and say which of the three failure categories it is already in.
